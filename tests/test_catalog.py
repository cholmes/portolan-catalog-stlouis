#!/usr/bin/env python3
"""Catalog consistency gates. Dependency-free; run via tests/run_all.py.

Checks the published tree against the Portolan rules this repo targets:
links resolve, no self links, providers host-last, exactly one default
style per styled collection, legend layers on data-driven styles,
collection-level table:columns, checksummed assets, pmtiles link fields.
"""

import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"
# CI has no parquet/pmtiles (gitignored artifacts): skip file-backed checks
LIGHT = os.environ.get("CI_LIGHT") == "1"
PORTOLAN_SCHEMA = "https://schemas.portolan-sdi.org/portolan/v0.1.0/schema.json"

errors = []


def err(msg):
    errors.append(msg)


def check_collection(coll_dir: Path):
    cid = coll_dir.name
    coll = json.loads((coll_dir / "collection.json").read_text())

    if any(l["rel"] == "self" for l in coll["links"]):
        err(f"{cid}: has self link")
    if PORTOLAN_SCHEMA not in coll.get("stac_extensions", []):
        err(f"{cid}: missing portolan schema pin")
    if not coll.get("title") or coll.get("description", "").startswith("Collection:"):
        err(f"{cid}: placeholder title/description")
    if coll.get("license") != "other":
        err(f"{cid}: license is {coll.get('license')!r}, expected 'other'")
    provs = coll.get("providers", [])
    if not provs or "host" not in provs[-1].get("roles", []):
        err(f"{cid}: providers must end with host")
    if not any("producer" in p.get("roles", []) for p in provs):
        err(f"{cid}: no producer provider")
    if not coll.get("updated"):
        err(f"{cid}: mirror missing top-level updated")
    if not any(l["rel"] == "via" for l in coll["links"]):
        err(f"{cid}: missing via link")
    if not any(l["rel"] == "license" for l in coll["links"]):
        err(f"{cid}: missing license link")
    if "table:columns" not in coll:
        err(f"{cid}: missing collection-level table:columns")

    for l in coll["links"]:
        if l["rel"] == "pmtiles" and not l.get("pmtiles:layers"):
            err(f"{cid}: pmtiles link missing pmtiles:layers")
        if "type" not in l:
            err(f"{cid}: link {l['rel']} missing type")
        if l["href"].startswith("./") or l["href"].startswith("../"):
            if not (coll_dir / l["href"]).resolve().exists():
                if not (LIGHT and l["href"].endswith((".pmtiles", ".parquet"))):
                    err(f"{cid}: link {l['rel']} -> {l['href']} does not resolve")

    # Assets
    defaults = []
    for key, a in coll.get("assets", {}).items():
        p = (coll_dir / a["href"]).resolve()
        if not p.exists():
            if not LIGHT:
                err(f"{cid}: asset {key} missing file {a['href']}")
            if "style" in a.get("roles", []) and "default" in a.get("roles", []):
                defaults.append(key)
            continue
        if "file:size" in a and p.stat().st_size != a["file:size"]:
            err(f"{cid}: asset {key} stale file:size")
        if a["href"].endswith(".parquet") and a.get("type") != "application/vnd.apache.parquet":
            err(f"{cid}: asset {key} wrong parquet media type {a.get('type')}")
        if "roles" not in a or not a["roles"]:
            err(f"{cid}: asset {key} has no roles")
        if "style" in a.get("roles", []) and "default" in a.get("roles", []):
            defaults.append(key)
        if "file:checksum" in a and not LIGHT:
            h = hashlib.sha256()
            with open(p, "rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    h.update(chunk)
            if "1220" + h.hexdigest() != a["file:checksum"]:
                err(f"{cid}: asset {key} stale file:checksum")

    style_assets = [k for k, a in coll.get("assets", {}).items()
                    if "style" in a.get("roles", [])]
    if style_assets and len(defaults) != 1:
        err(f"{cid}: expected exactly 1 default style, got {defaults}")

    # Styles: structure + legend rule
    for sf in sorted((coll_dir / "styles").glob("*.json")) if (coll_dir / "styles").exists() else []:
        s = json.loads(sf.read_text())
        if s.get("version") != 8:
            err(f"{cid}/{sf.name}: not version 8")
        src = s.get("sources", {}).get("data", {})
        if src.get("type") == "vector" and src.get("url") != f"pmtiles://../{cid}.pmtiles":
            err(f"{cid}/{sf.name}: bad pmtiles url {src.get('url')}")
        for layer in s.get("layers", []):
            if layer.get("source-layer") != cid:
                err(f"{cid}/{sf.name}: layer {layer.get('id')} source-layer != {cid}")
        # any data-driven color must be visible to the legend extractor:
        # first fill layer's fill-color is a match/step expression
        def is_expr(v):
            return isinstance(v, list) and v and v[0] in ("match", "step")
        data_driven = any(
            is_expr(layer.get("paint", {}).get(prop))
            for layer in s.get("layers", [])
            for prop in ("fill-color", "line-color", "circle-color"))
        if data_driven:
            first_fill = next((layer for layer in s["layers"] if layer["type"] == "fill"), None)
            if not first_fill or not is_expr(first_fill.get("paint", {}).get("fill-color")):
                err(f"{cid}/{sf.name}: data-driven style lacks legend fill layer")


def main() -> int:
    cat = json.loads((CATALOG / "catalog.json").read_text())
    if any(l["rel"] == "self" for l in cat["links"]):
        err("catalog: has self link")
    if PORTOLAN_SCHEMA not in cat.get("stac_extensions", []):
        err("catalog: missing portolan schema pin")
    children = [l for l in cat["links"] if l["rel"] == "child"]
    for l in children:
        if not l.get("title"):
            err(f"catalog: child {l['href']} missing title")
        if not (CATALOG / l["href"]).resolve().exists():
            err(f"catalog: child {l['href']} does not resolve")
    if len(children) != 43:
        err(f"catalog: expected 43 children, got {len(children)}")

    for coll_dir in sorted(CATALOG.iterdir()):
        if (coll_dir / "collection.json").exists():
            check_collection(coll_dir)

    if errors:
        print(f"FAIL ({len(errors)}):")
        for e in errors:
            print("  -", e)
        return 1
    print("test_catalog: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
