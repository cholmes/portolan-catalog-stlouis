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


def tile_fields(pmtiles: Path) -> set:
    """Attribute names present in a PMTiles archive's vector layers."""
    from pmtiles.reader import MmapSource, Reader
    with open(pmtiles, "rb") as f:
        meta = Reader(MmapSource(f)).metadata()
    layers = meta.get("vector_layers") or json.loads(
        meta.get("json", "{}")).get("vector_layers", [])
    return {k for l in layers for k in (l.get("fields") or {})}


def style_fields(node, out: set) -> set:
    """Every attribute a style reads, i.e. the target of every ["get", …]."""
    if isinstance(node, list):
        if len(node) == 2 and node[0] == "get" and isinstance(node[1], str):
            out.add(node[1])
        for x in node:
            style_fields(x, out)
    elif isinstance(node, dict):
        for x in node.values():
            style_fields(x, out)
    return out


def overture_source(cid: str) -> dict | None:
    """The sources.py entry when cid is an Overture collection, else None."""
    import sys
    sys.path.insert(0, str(ROOT / "tools"))
    from sources import SOURCES
    src = SOURCES.get(cid)
    return src if src and src["type"] == "overture" else None


def census_source(cid: str) -> dict | None:
    """The sources.py entry when cid is a census-family collection."""
    import sys
    sys.path.insert(0, str(ROOT / "tools"))
    from sources import SOURCES
    src = SOURCES.get(cid)
    return src if src and src["type"] == "census" else None


def check_collection(coll_dir: Path):
    cid = coll_dir.name  # leaf id: tile layers and style refs use this
    path_id = f"{coll_dir.parent.name}/{cid}"
    coll = json.loads((coll_dir / "collection.json").read_text())
    ov = overture_source(cid)
    cen = census_source(cid)

    if coll.get("id") != path_id:
        err(f"{cid}: id is {coll.get('id')!r}, expected {path_id!r}")
    if any(l["rel"] == "self" for l in coll["links"]):
        err(f"{cid}: has self link")
    if PORTOLAN_SCHEMA not in coll.get("stac_extensions", []):
        err(f"{cid}: missing portolan schema pin")
    if not coll.get("title") or coll.get("description", "").startswith("Collection:"):
        err(f"{cid}: placeholder title/description")
    # City data carries no explicit license ("other"); Overture themes and
    # census-family collections carry their own ("other" for US-government
    # public-domain works, CC-BY-NC-SA-4.0 for Mapping Inequality).
    expected_license = (ov or cen)["license"] if (ov or cen) else "other"
    if coll.get("license") != expected_license:
        err(f"{cid}: license is {coll.get('license')!r}, "
            f"expected {expected_license!r}")
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
    # A row count that outlives its file is worse than none: it is the number
    # every README, AGENTS.md and catalog total is computed from.
    pq = coll_dir / f"{cid.split('/')[-1]}.parquet"
    if pq.exists() and not LIGHT:
        import duckdb
        n = duckdb.sql(f"SELECT count(*) FROM '{pq}'").fetchone()[0]
        if coll.get("table:row_count") != n:
            err(f"{cid}: table:row_count {coll.get('table:row_count')} "
                f"!= {n} rows in the parquet")
        fc = coll.get("geoparquet:feature_count")
        if fc is not None and fc != n:
            err(f"{cid}: geoparquet:feature_count {fc} != {n} rows")

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
        if a["href"].startswith("http"):
            if not a["href"].startswith("https://"):
                err(f"{cid}: asset {key} remote href is not https")
            # Overture collections reference Overture's own release-pinned
            # global theme tiles as their visual asset: size is recorded but
            # a checksum of a 19-195 GB file this catalog neither serves nor
            # re-hashes would be an unverifiable claim in the other
            # direction, so none is required.
            if ov and a["href"].endswith(".pmtiles"):
                if "visual" not in a.get("roles", []):
                    err(f"{cid}: remote tiles asset {key} must be visual")
                if "file:size" not in a:
                    err(f"{cid}: remote tiles asset {key} missing file:size")
                continue
            # A `source` asset points at the city's own copy on a server we
            # do not control, so there is no local file to compare against.
            # What we can insist on is that it is fetchable over https and
            # that it carries the size and digest of the bytes it served —
            # an unpinned remote asset is an unverifiable claim.
            if "source" not in a.get("roles", []):
                err(f"{cid}: remote asset {key} must carry the source role")
            for field in ("file:size", "file:checksum"):
                if field not in a:
                    err(f"{cid}: remote asset {key} missing {field}")
            continue
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

    # A style that reads an attribute the tiles don't carry silently paints
    # every feature its fallback color — the map looks fine but says nothing.
    pmtiles = coll_dir / f"{cid}.pmtiles"
    have = tile_fields(pmtiles) if pmtiles.exists() and not LIGHT else None

    # Styles: structure + legend rule
    for sf in sorted((coll_dir / "styles").glob("*.json")) if (coll_dir / "styles").exists() else []:
        s = json.loads(sf.read_text())
        if have is not None:
            missing = sorted(style_fields(s.get("layers", []), set()) - have)
            if missing:
                err(f"{cid}/{sf.name}: reads fields absent from the tiles: {missing}")
        if s.get("version") != 8:
            err(f"{cid}/{sf.name}: not version 8")
        src = s.get("sources", {}).get("data", {})
        if ov:
            # Overture styles read the remote theme tiles and their layers
            # name the Overture types — except collections tiled locally
            # (OVERTURE_LOCAL in make_pmtiles.py: the global addresses
            # tileset has no St. Louis coverage), which follow the city
            # collections' local form. The style's own URL says which.
            from sources import OVERTURE_TILES
            local_url = f"pmtiles://../{cid}.pmtiles"
            want_url = f"pmtiles://{OVERTURE_TILES}/{ov['theme']}.pmtiles"
            if src.get("url") == local_url:
                for layer in s.get("layers", []):
                    if layer.get("source-layer") != cid:
                        err(f"{cid}/{sf.name}: layer {layer.get('id')} "
                            f"source-layer != {cid}")
            else:
                if src.get("type") == "vector" and src.get("url") != want_url:
                    err(f"{cid}/{sf.name}: bad pmtiles url {src.get('url')}")
                for layer in s.get("layers", []):
                    if layer.get("source-layer") not in ov["types"]:
                        err(f"{cid}/{sf.name}: layer {layer.get('id')} "
                            f"source-layer not in {ov['types']}")
        else:
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


def check_source_manifest() -> None:
    """SOURCE_FILES must not drift from the sources it claims to mirror.

    The primary entries duplicate SOURCES' `url`/`urls` so each file can carry
    its own title, and a duplicate that stops matching would advertise the
    wrong origin — the one thing a source asset exists to get right.
    """
    import sys
    sys.path.insert(0, str(ROOT / "tools"))
    from sources import SOURCES, SOURCE_FILES, source_files

    for cid, src in SOURCES.items():
        # parcels-history carries both: `urls` is the real set, `url` is its
        # first element, kept as the single-source display value.
        expected = set()
        if src.get("urls"):
            expected = set(src["urls"])
        elif src.get("url") and not src.get("crime_scrape"):
            expected = {src["url"]}
        listed = {e["url"] for e in source_files(cid) if e["primary"]}
        if expected != listed:
            err(f"{cid}: SOURCE_FILES primaries {sorted(listed)} "
                f"!= SOURCES {sorted(expected)}")
        if expected and not listed and SOURCE_FILES.get(cid) != "scrape":
            err(f"{cid}: downloadable source is not published as an asset")

    sc = ROOT / "sources" / "source_checksums.json"
    if not sc.exists():
        err("sources/source_checksums.json missing "
            "(run tools/fetch_source_meta.py)")
        return
    have = json.loads(sc.read_text())["collections"]
    for cid in SOURCE_FILES:
        if not have.get(cid):
            err(f"{cid}: no source checksums recorded")


def main() -> int:
    check_source_manifest()
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
    if len(children) != 12:
        err(f"catalog: expected 12 topic children, got {len(children)}")

    n_colls = 0
    for group_dir in sorted(CATALOG.iterdir()):
        if not group_dir.is_dir() or not (group_dir / "catalog.json").exists():
            continue
        gcat = json.loads((group_dir / "catalog.json").read_text())
        for l in gcat["links"]:
            if l["rel"] == "child" and not (group_dir / l["href"]).resolve().exists():
                err(f"{group_dir.name}: child {l['href']} does not resolve")
        for coll_dir in sorted(group_dir.iterdir()):
            if coll_dir.is_dir() and (coll_dir / "collection.json").exists():
                n_colls += 1
                check_collection(coll_dir)
    if n_colls != 67:
        err(f"expected 67 collections across groups, got {n_colls}")

    if errors:
        print(f"FAIL ({len(errors)}):")
        for e in errors:
            print("  -", e)
        return 1
    print("test_catalog: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
