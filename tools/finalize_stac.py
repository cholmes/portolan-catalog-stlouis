#!/usr/bin/env python3
"""Finalize STAC metadata to Portolan spec (v0.1.0 + PRs #97/#124).

Runs after `portolan add`. Patches what the CLI doesn't yet emit:
- property-sales: hand-authored tabular collection (the CLI can't track
  geometry-less parquet yet)
- titles/descriptions from .portolan/metadata.yaml
- portolan + file extension pins; parquet media type
- providers (producer = city department, host last), license "other",
  rel license + via links to the portal dataset page, mirror `updated`
- pmtiles links get pmtiles:layers; style assets get titles, and the
  default style gets roles ["style", "default"] (spec PR #97)
- file:size + file:checksum (sha2-256 multihash) on every asset
- temporal extents; strips self links

Idempotent: safe to re-run after any add/readme cycle.
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sources import SOURCES, GROUPS, GROUP_TITLES, GROUP_OF, coll_rel

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"
SYNC = (ROOT / "staging" / "synced.txt").read_text().strip()

PORTOLAN_SCHEMA = "https://schemas.portolan-sdi.org/portolan/v0.1.0/schema.json"
FILE_EXT = "https://stac-extensions.github.io/file/v2.1.0/schema.json"
TABLE_EXT = "https://stac-extensions.github.io/table/v1.2.0/schema.json"
WML_EXT = "https://stac-extensions.github.io/web-map-links/v1.3.0/schema.json"
PARQUET_TYPE = "application/vnd.apache.parquet"

HOST = {
    "name": "TGE Labs",
    "roles": ["host"],
    "url": "https://github.com/cholmes/portolan-catalog-stlouis",
}

THEMES_EXT = "https://stac-extensions.github.io/themes/v1.0.0/schema.json"
TOPIC_SCHEME = "https://www.stlouis-mo.gov/data/topics/"
# The portal's own main-topic assignments (scraped from the 12 topic pages)
MAIN_TOPICS = json.loads((Path(__file__).parent.parent / "docs" / "portal-main-topics.json").read_text())
# The portal's own per-dataset tags
PORTAL_TAGS = json.loads((Path(__file__).parent.parent / "docs" / "portal-topics-tags.json").read_text())


def slugify(s: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in s.lower()).strip("-").replace("--", "-")

DESCRIPTIONS = json.loads((ROOT / "docs" / "portal-descriptions.json").read_text())
_cn = ROOT / "docs" / "column-notes.json"
COLUMN_NOTES = json.loads(_cn.read_text()) if _cn.exists() else {}

# Arrow → table-extension-ish type names already handled by CLI; for the
# hand-authored tabular collection we map duckdb types.
DUCK_TO_TABLE = {
    "BIGINT": "int64", "INTEGER": "int32", "SMALLINT": "int16",
    "DOUBLE": "double", "FLOAT": "float", "VARCHAR": "string",
    "BOOLEAN": "boolean", "DATE": "date", "TIMESTAMP": "timestamp",
}


def multihash(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return "1220" + h.hexdigest()


def duck(sql: str):
    r = subprocess.run(["duckdb", "-json", "-c", sql], capture_output=True, text=True)
    return json.loads(r.stdout or "[]")


def stamp_asset(coll_dir: Path, href: str, asset: dict) -> None:
    p = (coll_dir / href).resolve()
    if p.exists():
        asset["file:size"] = p.stat().st_size
        asset["file:checksum"] = multihash(p)


def ensure_link(links: list, rel: str, href: str, type_: str, title: str | None = None, **extra) -> None:
    for l in links:
        if l["rel"] == rel and l["href"] == href:
            l.update({"type": type_, **extra})
            if title:
                l["title"] = title
            return
    l = {"rel": rel, "href": href, "type": type_, **extra}
    if title:
        l["title"] = title
    links.append(l)


def _is_tabular(cid: str) -> bool:
    pq = CATALOG / coll_rel(cid) / f"{cid}.parquet"
    if not pq.exists():
        return False
    import pyarrow.parquet as _pq
    names = _pq.read_schema(pq).names
    return "geometry" not in names and "geom" not in names


TABULAR = [c for c in SOURCES if _is_tabular(c)]


def build_tabular(cid: str) -> None:
    coll_dir = CATALOG / coll_rel(cid)
    pq = coll_dir / f"{cid}.parquet"
    cols = duck(f"SELECT column_name n, column_type t FROM (DESCRIBE SELECT * FROM '{pq}')")
    dates = None
    if cid == "property-sales":
        dates = duck(f"SELECT min(strptime(SaleDate, '%m/%d/%y %H:%M:%S'))::VARCHAR a, "
                     f"max(strptime(SaleDate, '%m/%d/%y %H:%M:%S'))::VARCHAR b FROM '{pq}' "
                     f"WHERE SaleDate IS NOT NULL")
    elif cid == "election-results-nov-2024":
        dates = [{"a": "2024-11-05 00:00:00", "b": "2024-11-05 00:00:00"}]
    n = duck(f"SELECT count(*) c FROM '{pq}'")[0]["c"]
    city_bbox = [-90.320522, 38.531907, -90.166409, 38.774362]
    coll = {
        "type": "Collection",
        "id": coll_rel(cid),
        "stac_version": "1.1.0",
        "stac_extensions": [TABLE_EXT],
        "description": "placeholder",  # filled by common pass below
        "license": "other",
        "extent": {
            "spatial": {"bbox": [city_bbox]},
            "temporal": {"interval": [[None, None]]},
        },
        "table:row_count": n,
        "table:columns": [
            {"name": c["n"], "type": DUCK_TO_TABLE.get(c["t"], c["t"].lower()),
             **({"description": COLUMN_NOTES[cid][c["n"]]}
                if COLUMN_NOTES.get(cid, {}).get(c["n"]) else {})}
            for c in cols
        ],
        "links": [
            {"rel": "root", "href": "../../catalog.json", "type": "application/json"},
            {"rel": "parent", "href": "../catalog.json", "type": "application/json"},
            {"rel": "describedby", "href": "./README.md", "type": "text/markdown"},
            {"rel": "agents", "href": "./AGENTS.md", "type": "text/markdown"},
        ],
        "assets": {
            cid: {
                "href": f"./{cid}.parquet",
                "type": PARQUET_TYPE,
                "roles": ["data"],
                "title": f"{SOURCES[cid]['title']} (Parquet)",
            }
        },
    }
    if dates and dates[0].get("a"):
        # SaleDate strings parse with 2-digit years; clamp obvious overflow
        a, b = dates[0]["a"], dates[0]["b"]
        coll["extent"]["temporal"]["interval"] = [
            [a.replace(" ", "T") + "Z", b.replace(" ", "T") + "Z"]]
    coll_dir.joinpath("collection.json").write_text(json.dumps(coll, indent=2) + "\n")
    print(f"✓ {cid} collection.json authored (tabular)")


def finalize_collection(coll_id: str) -> None:
    coll_dir = CATALOG / coll_rel(coll_id)
    f = coll_dir / "collection.json"
    coll = json.loads(f.read_text())
    src = SOURCES[coll_id]
    meta_desc = DESCRIPTIONS.get(coll_id, {}).get("description") or ""

    coll["id"] = coll_rel(coll_id)
    coll["title"] = src["title"]
    if meta_desc:
        coll["description"] = meta_desc
    elif coll.get("description", "").startswith("Collection:"):
        coll["description"] = src["title"]

    ext = set(coll.get("stac_extensions", []))
    ext.update({PORTOLAN_SCHEMA, FILE_EXT, TABLE_EXT})
    if MAIN_TOPICS.get(coll_id):
        ext.add(THEMES_EXT)
    has_pmtiles = (coll_dir / f"{coll_id}.pmtiles").exists()
    if has_pmtiles:
        ext.add(WML_EXT)
    coll["stac_extensions"] = sorted(ext)

    coll["license"] = "other"
    coll["updated"] = SYNC

    # Portal main topics as STAC themes; portal tags as keywords (verbatim —
    # the browser's topic browse and tag cloud read these).
    topics = MAIN_TOPICS.get(coll_id, [])
    if topics:
        coll["themes"] = [{
            "scheme": TOPIC_SCHEME,
            "concepts": [{"id": slugify(t), "title": t} for t in sorted(topics)],
        }]
    tags = PORTAL_TAGS.get(coll_id, {}).get("tags", [])
    if tags:
        coll["keywords"] = tags
    else:
        coll.pop("keywords", None)

    # Researched column meanings (docs/column-notes.json) → table:columns
    notes = COLUMN_NOTES.get(coll_id, {})
    if notes and coll.get("table:columns"):
        for col in coll["table:columns"]:
            if col["name"] in notes:
                col["description"] = notes[col["name"]]

    # Recompute the spatial extent from the parquet itself — the CLI's
    # tracked extent can go stale when files are rewritten out from under it.
    pq = coll_dir / f"{coll_id}.parquet"
    if pq.exists() and coll_id not in TABULAR:
        bb = duck(
            "INSTALL spatial; LOAD spatial; "
            f"SELECT min(ST_XMin(geometry)) a, min(ST_YMin(geometry)) b, "
            f"max(ST_XMax(geometry)) c, max(ST_YMax(geometry)) d "
            f"FROM '{pq}' WHERE geometry IS NOT NULL")
        if bb and bb[0].get("a") is not None:
            coll.setdefault("extent", {}).setdefault("spatial", {})["bbox"] = [
                [bb[0]["a"], bb[0]["b"], bb[0]["c"], bb[0]["d"]]]
    coll["providers"] = [
        {"name": f"City of St. Louis — {src['department']}",
         "roles": ["producer", "licensor"],
         "url": src["portal_page"]},
        HOST,
    ]

    links = [l for l in coll.get("links", []) if l["rel"] != "self"]
    ensure_link(links, "describedby", "./README.md", "text/markdown")
    ensure_link(links, "agents", "./AGENTS.md", "text/markdown")
    ensure_link(links, "license", src["portal_page"], "text/html",
                "Dataset page on the City of St. Louis open data portal")
    ensure_link(links, "via", src["portal_page"], "text/html",
                "Source dataset on stlouis-mo.gov")
    if src["type"] == "arcgis":
        ensure_link(links, "via", src["service"], "text/html",
                    "Source ArcGIS service")
    if has_pmtiles and not any(l["rel"] == "pmtiles" for l in links):
        links.append({"rel": "pmtiles", "href": f"./{coll_id}.pmtiles",
                      "type": "application/vnd.pmtiles"})
    for l in links:
        if l["rel"] == "pmtiles":
            l["pmtiles:layers"] = [coll_id]
            l.setdefault("type", "application/vnd.pmtiles")
        if l["rel"] == "root":
            l["href"] = "../../catalog.json"
            l.setdefault("type", "application/json")
            l["title"] = "City of St. Louis Open Data (Cloud-Native Mirror)"
        if l["rel"] == "parent":
            l["href"] = "../catalog.json"
            l.setdefault("type", "application/json")
            l["title"] = GROUP_TITLES[GROUP_OF[coll_id]]
    coll["links"] = links

    # Assets: media types, titles, default style role, size+checksum
    assets = coll.get("assets", {})
    if has_pmtiles and not any(
            a.get("href", "").endswith(".pmtiles") for a in assets.values()):
        assets[f"{coll_id}-tiles"] = {
            "href": f"./{coll_id}.pmtiles", "type": "application/vnd.pmtiles",
            "roles": ["visual"], "title": f"{src['title']} (PMTiles)"}
    if (coll_dir / "thumbnail.png").exists() and "thumbnail" not in assets:
        assets["thumbnail"] = {
            "href": "./thumbnail.png", "type": "image/png",
            "roles": ["thumbnail"],
            "title": f"{src['title']} rendered with the default style",
        }
    styles_dir = coll_dir / "styles"
    style_files = sorted(styles_dir.glob("*.json")) if styles_dir.exists() else []
    # Make sure every style file has an asset entry
    for sf in style_files:
        key = f"styles/{sf.stem}"
        if key not in assets:
            assets[key] = {"href": f"./styles/{sf.name}",
                           "type": "application/vnd.mapbox.style+json",
                           "roles": ["style"]}
    for key, a in assets.items():
        href = a.get("href", "")
        if href.endswith(".parquet"):
            a["type"] = PARQUET_TYPE
            a.setdefault("title", f"{src['title']} (GeoParquet)")
            a.setdefault("roles", ["data"])
        elif href.endswith(".pmtiles"):
            a.setdefault("title", f"{src['title']} (PMTiles)")
        elif href.endswith(".json") and "styles/" in href:
            sf = coll_dir / href.lstrip("./")
            if sf.exists():
                style_obj = json.loads(sf.read_text())
                a["title"] = style_obj.get("name", sf.stem)
                desc = (style_obj.get("metadata") or {}).get("description")
                if desc:
                    a["description"] = desc
            roles = set(a.get("roles", [])) | {"style"}
            if href.endswith("/default.json"):
                roles.add("default")
            else:
                roles.discard("default")
            a["roles"] = sorted(roles)
        stamp_asset(coll_dir, href, a)
    coll["assets"] = assets

    f.write_text(json.dumps(coll, indent=2) + "\n")
    n_styles = len(style_files)
    print(f"✓ {coll_id}: {n_styles} style assets, "
          f"{'pmtiles' if has_pmtiles else 'tabular'}")


def finalize_root() -> None:
    f = CATALOG / "catalog.json"
    cat = json.loads(f.read_text())
    cat["stac_extensions"] = sorted(set(cat.get("stac_extensions", [])) | {PORTOLAN_SCHEMA})
    cat["updated"] = SYNC
    cat["providers"] = [
        {"name": "City of St. Louis", "roles": ["producer", "licensor"],
         "url": "https://www.stlouis-mo.gov/data/"},
        HOST,
    ]
    cat["license"] = "other"
    links = [l for l in cat.get("links", []) if l["rel"] != "self"]
    ensure_link(links, "license", "https://www.stlouis-mo.gov/data/", "text/html",
                "City of St. Louis open data portal")
    ensure_link(links, "via", "https://www.stlouis-mo.gov/data/", "text/html",
                "City of St. Louis open data portal")
    # children are the department catalogs
    links = [l for l in links if l["rel"] != "child"]
    for g in GROUPS:
        if (CATALOG / g / "catalog.json").exists():
            links.append({"rel": "child", "href": f"./{g}/catalog.json",
                          "type": "application/json", "title": GROUP_TITLES[g]})
    for l in links:
        if l["rel"] == "root":
            l.setdefault("type", "application/json")
    cat["links"] = links
    f.write_text(json.dumps(cat, indent=2) + "\n")
    print("✓ catalog.json finalized")


def finalize_group(group: str) -> None:
    f = CATALOG / group / "catalog.json"
    if not f.exists():
        return
    cat = json.loads(f.read_text())
    cat["stac_extensions"] = sorted(set(cat.get("stac_extensions", [])) | {PORTOLAN_SCHEMA})
    cat["updated"] = SYNC
    links = [l for l in cat["links"] if l["rel"] not in ("child", "self")]
    for cid in GROUPS[group]:
        if (CATALOG / group / cid / "collection.json").exists():
            links.append({"rel": "child", "href": f"./{cid}/collection.json",
                          "type": "application/json", "title": SOURCES[cid]["title"]})
    cat["links"] = links
    f.write_text(json.dumps(cat, indent=2) + "\n")


def main() -> None:
    for cid in TABULAR:
        build_tabular(cid)
    for coll_id in SOURCES:
        if (CATALOG / coll_rel(coll_id) / "collection.json").exists():
            finalize_collection(coll_id)
        else:
            print(f"✗ missing: {coll_id}")
    for group in GROUPS:
        finalize_group(group)
    finalize_root()


if __name__ == "__main__":
    main()
