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
from sources import SOURCES, GROUPS, GROUP_TITLES, GROUP_OF, coll_rel, linkify

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
DESCRIPTIONS.update(json.loads(
    (ROOT / "docs" / "overture-descriptions.json").read_text()))
DESCRIPTIONS.update(json.loads(
    (ROOT / "docs" / "census-descriptions.json").read_text()))
_cn = ROOT / "docs" / "column-notes.json"
COLUMN_NOTES = json.loads(_cn.read_text()) if _cn.exists() else {}

# The Overture themes share most of their schema, so their glosses live in
# their own file with three scopes — _shared, _base_theme, per-collection —
# merged by overture_notes() below rather than repeated ten times.
_ocn = ROOT / "docs" / "overture-column-notes.json"
OVERTURE_COLUMN_NOTES = json.loads(_ocn.read_text()) if _ocn.exists() else {}


def overture_notes(coll_id: str, theme: str) -> dict:
    """Column glosses for one Overture collection, most specific winning."""
    notes = dict(OVERTURE_COLUMN_NOTES.get("_shared", {}))
    if theme == "base":
        notes.update(OVERTURE_COLUMN_NOTES.get("_base_theme", {}))
    notes.update(OVERTURE_COLUMN_NOTES.get(coll_id, {}))
    return notes

# The city's own files, with the size and checksum of the bytes it served at
# sync time (tools/fetch_source_meta.py). Absent on a fresh clone that has not
# run that script yet, in which case collections simply get no source assets.
_sc = ROOT / "sources" / "source_checksums.json"
SOURCE_CHECKSUMS = json.loads(_sc.read_text())["collections"] if _sc.exists() else {}

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


def portal_link_title(url: str) -> str:
    """Name the page honestly — a third of these are not dataset.cfm pages."""
    if "dataset.cfm" in url:
        return "Dataset page on the City of St. Louis open data portal"
    if "maps.arcgis.com" in url:
        return "Dataset page in the city's ArcGIS Online organization"
    return "Source ArcGIS service — this layer has no portal dataset page"


def source_assets(coll_id: str) -> dict:
    """The city's own files as `source`-role assets, pointing upstream.

    `source` and not `data`: core.md scopes `data` to the cloud-native
    primary, and a client filtering on it should land on the GeoParquet, not
    on a zipped Shapefile. The role also tells rashid these bytes live on a
    server this catalog does not control, so the cloud-native format and
    range-request checks do not apply to them.
    """
    out = {}
    for e in SOURCE_CHECKSUMS.get(coll_id, []):
        a = {
            "href": e["url"],
            "type": e["type"],
            "title": e["title"],
            "roles": ["source"],
            "file:size": e["size"],
            "file:checksum": e["checksum"],
        }
        note = e.get("description")
        origin = ("The file this collection was built from."
                  if e.get("primary") else
                  "The city's own alternate distribution of this layer.")
        # Not everything the city publishes sits on a city domain — the crime
        # files are SLMPD's own, on slmpd.org.
        host = e["url"].split("/")[2]
        a["description"] = (
            f"{note + ' ' if note else ''}{origin} Served upstream by "
            f"{host}, not by this mirror; size and checksum are of the bytes "
            f"it served at the sync time in `updated`.")
        out[e["key"]] = a
    return out


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
             **({"description": linkify(COLUMN_NOTES[cid][c["n"]])}
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


OVERTURE_ATTRIBUTION = "https://docs.overturemaps.org/attribution/"
_ov_tile_sizes: dict = {}


def overture_tile_size(theme: str) -> int | None:
    """Content-Length of Overture's remote theme pmtiles (cached per theme)."""
    from sources import OVERTURE_TILES
    if theme not in _ov_tile_sizes:
        import urllib.request
        req = urllib.request.Request(f"{OVERTURE_TILES}/{theme}.pmtiles",
                                     method="HEAD")
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                _ov_tile_sizes[theme] = int(r.headers["Content-Length"])
        except Exception:  # noqa: BLE001 — size is nice-to-have
            _ov_tile_sizes[theme] = None
    return _ov_tile_sizes[theme]


def finalize_collection(coll_id: str) -> None:
    coll_dir = CATALOG / coll_rel(coll_id)
    f = coll_dir / "collection.json"
    coll = json.loads(f.read_text())
    src = SOURCES[coll_id]
    if src["type"] == "overture":
        finalize_overture(coll_id, coll_dir, f, coll, src)
        return
    if src["type"] == "census":
        finalize_census(coll_id, coll_dir, f, coll, src)
        return
    meta_desc = linkify(DESCRIPTIONS.get(coll_id, {}).get("description") or "")

    coll["id"] = coll_rel(coll_id)
    coll["title"] = src["title"]
    if meta_desc:
        coll["description"] = meta_desc
    elif coll.get("description", "").startswith("Collection:"):
        coll["description"] = src["title"]

    ext = set(coll.get("stac_extensions", []))
    ext.update({PORTOLAN_SCHEMA, FILE_EXT, TABLE_EXT})
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
    themes = []
    if topics:
        themes.append({
            "scheme": TOPIC_SCHEME,
            "concepts": [{"id": slugify(t), "title": t} for t in sorted(topics)],
        })
    # Department preserved as a second scheme now that the hierarchy is
    # topic-based — plus a keyword, so the tag filter answers
    # "everything from the Assessor's Office".
    dept = src["department"]
    themes.append({
        "scheme": "https://www.stlouis-mo.gov/government/departments/",
        "concepts": [{"id": slugify(dept), "title": dept}],
    })
    coll["themes"] = themes
    tags = list(PORTAL_TAGS.get(coll_id, {}).get("tags", []))
    if dept not in tags:
        tags.append(dept)
    coll["keywords"] = tags

    # Researched column meanings (docs/column-notes.json) → table:columns
    notes = COLUMN_NOTES.get(coll_id, {})
    if notes and coll.get("table:columns"):
        for col in coll["table:columns"]:
            if col["name"] in notes:
                col["description"] = linkify(notes[col["name"]])

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
    # Same reason as the extent above: the count the CLI tracked can outlive
    # the file. Wards said 10 long after the source moved off the Hosted
    # FeatureServer (10 of 14 wards) to the portal shapefile that has all 14.
    if pq.exists():
        rc = duck(f"SELECT count(*) AS n FROM '{pq}'")
        if rc:
            coll["table:row_count"] = rc[0]["n"]
            # Counts every row in the GeoParquet, including the ones kept
            # deliberately with null geometry (311 has ~18k requests the city
            # never geocoded), so it tracks the row count rather than the
            # number of non-null geometries.
            if "geoparquet:feature_count" in coll:
                coll["geoparquet:feature_count"] = rc[0]["n"]
    coll["providers"] = [
        {"name": f"City of St. Louis — {src['department']}",
         "roles": ["producer", "licensor"],
         "url": src["portal_page"]},
        HOST,
    ]

    # `via` is rebuilt from scratch rather than topped up: when a collection
    # switches source (wards moved off the Hosted FeatureServer, which only
    # carried 10 of 14 wards, to the portal shapefile), a merely-additive
    # ensure_link would leave the abandoned service linked as the origin.
    links = [l for l in coll.get("links", [])
             if l["rel"] not in ("self", "via")]
    ensure_link(links, "describedby", "./README.md", "text/markdown")
    ensure_link(links, "agents", "./AGENTS.md", "text/markdown")
    ensure_link(links, "license", src["portal_page"], "text/html",
                portal_link_title(src["portal_page"]))
    ensure_link(links, "via", src["portal_page"], "text/html",
                portal_link_title(src["portal_page"]))
    if src["type"] == "arcgis" and src["service"] != src["portal_page"]:
        ensure_link(links, "via", src["service"], "text/html",
                    "Source ArcGIS service")
    if src.get("crime_scrape"):
        # The real origin is SLMPD's own index, not the portal page that
        # points at it; without this the published record names neither.
        ensure_link(links, "via", src["url"], "text/html",
                    "SLMPD crime statistics — the monthly NIBRS CSV index")
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
    # A README asset would list its own checksum in its own Files table, so
    # it goes stale the moment `portolan readme` runs — and it duplicated the
    # `describedby` link, which is how the spec exposes the README anyway.
    # Only 3 of the 51 ever had one; now none do.
    assets.pop("documentation", None)
    # Rebuilt, not merged, so a file the city stops serving stops being
    # advertised here (STLSBDs.geojson went 404 between syncs).
    assets = {k: v for k, v in assets.items() if not k.startswith("source")}
    src_assets = source_assets(coll_id)
    assets.update(src_assets)
    coll["assets"] = assets

    f.write_text(json.dumps(coll, indent=2) + "\n")
    n_styles = len(style_files)
    print(f"✓ {coll_id}: {n_styles} style assets, "
          f"{len(src_assets)} source files, "
          f"{'pmtiles' if has_pmtiles else 'tabular'}")


def finalize_overture(coll_id: str, coll_dir, f, coll: dict, src: dict) -> None:
    """Overture collections: Overture provider/license, remote theme PMTiles.

    The tiles asset points at Overture's own release-pinned global tiles —
    nothing tiled locally — so it gets the S3-reported size but no checksum
    (the files run 19-195 GB; a checksum of bytes this catalog neither
    serves nor could re-hash would be theater).
    """
    from sources import OVERTURE_RELEASE, OVERTURE_S3, OVERTURE_TILES
    coll["id"] = coll_rel(coll_id)
    coll["title"] = src["title"]
    coll["description"] = DESCRIPTIONS[coll_id]["description"]

    ext = set(coll.get("stac_extensions", []))
    ext.update({PORTOLAN_SCHEMA, FILE_EXT, TABLE_EXT, THEMES_EXT, WML_EXT})
    coll["stac_extensions"] = sorted(ext)

    coll["license"] = src["license"]
    coll["updated"] = SYNC
    # The data is a snapshot of one Overture release; its date is the
    # collection's temporal extent.
    rel_date = OVERTURE_RELEASE.split(".")[0]
    coll.setdefault("extent", {})["temporal"] = {
        "interval": [[f"{rel_date}T00:00:00Z", f"{rel_date}T00:00:00Z"]]}

    # Topic theme = the catalog this collection lives in (our assignment —
    # these are not portal datasets), plus the Overture theme as its own
    # scheme so "everything from Overture's base theme" is answerable.
    group_title = GROUP_TITLES[GROUP_OF[coll_id]]
    coll["themes"] = [
        {"scheme": TOPIC_SCHEME,
         "concepts": [{"id": slugify(group_title), "title": group_title}]},
        {"scheme": "https://docs.overturemaps.org/guides/",
         "concepts": [{"id": src["theme"],
                       "title": f"Overture {src['theme']} theme"}]},
    ]
    coll["keywords"] = ["overture", "Overture Maps Foundation", src["theme"]] + [
        t.replace("_", " ") for t in src["types"]]

    # Researched column meanings (docs/overture-column-notes.json), wording
    # from Overture's own schema and theme guides.
    notes = overture_notes(coll_id, src["theme"])
    missing = []
    for col in coll.get("table:columns", []):
        if col["name"] in notes:
            col["description"] = linkify(notes[col["name"]])
        else:
            missing.append(col["name"])
    if missing:
        # A vintage bump that adds a column should say so rather than ship a
        # blank Description cell in the README.
        print(f"  ! {coll_id}: no column note for {', '.join(missing)}")

    pq = coll_dir / f"{coll_id}.parquet"
    if pq.exists():
        bb = duck(
            "INSTALL spatial; LOAD spatial; "
            f"SELECT min(ST_XMin(geometry)) a, min(ST_YMin(geometry)) b, "
            f"max(ST_XMax(geometry)) c, max(ST_YMax(geometry)) d "
            f"FROM '{pq}' WHERE geometry IS NOT NULL")
        if bb and bb[0].get("a") is not None:
            coll.setdefault("extent", {}).setdefault("spatial", {})["bbox"] = [
                [bb[0]["a"], bb[0]["b"], bb[0]["c"], bb[0]["d"]]]
        rc = duck(f"SELECT count(*) AS n FROM '{pq}'")
        if rc:
            coll["table:row_count"] = rc[0]["n"]
            if "geoparquet:feature_count" in coll:
                coll["geoparquet:feature_count"] = rc[0]["n"]

    coll["providers"] = [
        {"name": "Overture Maps Foundation",
         "roles": ["producer", "licensor"],
         "url": "https://overturemaps.org/"},
        HOST,
    ]

    # Addresses is the one Overture collection with locally built tiles —
    # the global addresses tileset has no St. Louis coverage (see
    # OVERTURE_LOCAL in make_pmtiles.py). Local archive present ⇒ local
    # link/asset, exactly like a city collection.
    local_pm = coll_dir / f"{coll_id}.pmtiles"
    if local_pm.exists():
        tiles_url = f"./{coll_id}.pmtiles"
        pm_layers = [coll_id]
    else:
        tiles_url = f"{OVERTURE_TILES}/{src['theme']}.pmtiles"
        pm_layers = list(src["types"])
    links = [l for l in coll.get("links", [])
             if l["rel"] not in ("self", "via", "pmtiles")]
    ensure_link(links, "describedby", "./README.md", "text/markdown")
    ensure_link(links, "agents", "./AGENTS.md", "text/markdown")
    ensure_link(links, "license", OVERTURE_ATTRIBUTION, "text/html",
                "Overture attribution and licensing")
    ensure_link(links, "via", src["docs"], "text/html",
                f"Overture {src['theme']} theme guide")
    # rashid's PTL-PRO-001 requires text/html on every via link, even when
    # the target is a parquet prefix rather than a page.
    ensure_link(links, "via",
                f"{OVERTURE_S3}/theme={src['theme']}/",
                "text/html",
                f"Overture release {OVERTURE_RELEASE} GeoParquet "
                f"(theme={src['theme']}) on S3")
    links.append({"rel": "pmtiles", "href": tiles_url,
                  "type": "application/vnd.pmtiles",
                  "pmtiles:layers": pm_layers})
    for l in links:
        if l["rel"] == "root":
            l["href"] = "../../catalog.json"
            l.setdefault("type", "application/json")
            l["title"] = "City of St. Louis Open Data (Cloud-Native Mirror)"
        if l["rel"] == "parent":
            l["href"] = "../catalog.json"
            l.setdefault("type", "application/json")
            l["title"] = GROUP_TITLES[GROUP_OF[coll_id]]
    coll["links"] = links

    assets = coll.get("assets", {})
    if local_pm.exists():
        tiles = {
            "href": tiles_url,
            "type": "application/vnd.pmtiles",
            "roles": ["visual"],
            "title": f"{src['title']} (PMTiles)",
            "description": (
                "Vector tiles built from this collection's own clipped "
                "GeoParquet — Overture's global addresses tileset has no "
                "St. Louis coverage, so this mirror tiles the theme "
                "locally."),
        }
        stamp_asset(coll_dir, tiles_url, tiles)
    else:
        tiles = {
            "href": tiles_url,
            "type": "application/vnd.pmtiles",
            "roles": ["visual"],
            "title": f"Overture {src['theme']} theme (PMTiles, global)",
            "description": (
                "Overture's own release-pinned global vector tiles for the "
                f"{src['theme']} theme, served from the Overture Maps "
                "Foundation's public bucket — not from this mirror, and not "
                "clipped to St. Louis. The styles select this collection's "
                f"layers ({', '.join(src['types'])}) from them."),
        }
        size = overture_tile_size(src["theme"])
        if size:
            tiles["file:size"] = size
    assets[f"{coll_id}-tiles"] = tiles
    if (coll_dir / "thumbnail.png").exists() and "thumbnail" not in assets:
        assets["thumbnail"] = {
            "href": "./thumbnail.png", "type": "image/png",
            "roles": ["thumbnail"],
            "title": f"{src['title']} rendered with the default style",
        }
    styles_dir = coll_dir / "styles"
    style_files = sorted(styles_dir.glob("*.json")) if styles_dir.exists() else []
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
    origin = "local" if local_pm.exists() else "remote Overture"
    print(f"✓ {coll_id}: {len(style_files)} style assets, {origin} "
          f"pmtiles ({src['theme']})")


# Per-dataset facts for the census family. Temporal extents are the data's
# own reference periods: ACS 5-year estimates describe 2020-2024, LODES the
# 2023 job year, PLACES models BRFSS 2022-2023 responses, and the HOLC maps
# were created in the 1930s.
CENSUS_META = {
    "acs-bg": {
        "provider": ("U.S. Census Bureau",
                     "https://www.census.gov/programs-surveys/acs.html"),
        "interval": ["2020-01-01T00:00:00Z", "2024-12-31T23:59:59Z"],
        "program": ("acs", "American Community Survey"),
        "keywords": ["census", "ACS", "American Community Survey",
                     "demographics", "income", "poverty", "equity"],
    },
    "acs-tract": {
        "provider": ("U.S. Census Bureau",
                     "https://www.census.gov/programs-surveys/acs.html"),
        "interval": ["2020-01-01T00:00:00Z", "2024-12-31T23:59:59Z"],
        "program": ("acs", "American Community Survey"),
        "keywords": ["census", "ACS", "American Community Survey",
                     "health insurance", "disability", "demographics"],
    },
    "lodes-jobs": {
        "provider": ("U.S. Census Bureau — Longitudinal Employer-Household "
                     "Dynamics", "https://lehd.ces.census.gov/"),
        "interval": ["2023-01-01T00:00:00Z", "2023-12-31T23:59:59Z"],
        "program": ("lodes", "LEHD Origin-Destination Employment Statistics"),
        "keywords": ["census", "LEHD", "LODES", "jobs", "employment"],
    },
    "lodes-od": {
        "provider": ("U.S. Census Bureau — Longitudinal Employer-Household "
                     "Dynamics", "https://lehd.ces.census.gov/"),
        "interval": ["2023-01-01T00:00:00Z", "2023-12-31T23:59:59Z"],
        "program": ("lodes", "LEHD Origin-Destination Employment Statistics"),
        "keywords": ["census", "LEHD", "LODES", "commutes",
                     "origin-destination"],
    },
    "holc": {
        "provider": ("Mapping Inequality, Digital Scholarship Lab, "
                     "University of Richmond",
                     "https://dsl.richmond.edu/panorama/redlining/"),
        "interval": ["1930-01-01T00:00:00Z", "1939-12-31T23:59:59Z"],
        "program": ("mapping-inequality", "Mapping Inequality"),
        "keywords": ["redlining", "HOLC", "Mapping Inequality", "history",
                     "equity"],
    },
    "places": {
        "provider": ("Centers for Disease Control and Prevention",
                     "https://www.cdc.gov/places/"),
        "interval": ["2022-01-01T00:00:00Z", "2023-12-31T23:59:59Z"],
        "program": ("places", "CDC PLACES"),
        "keywords": ["CDC", "PLACES", "health", "small-area estimation"],
    },
}


def finalize_census(coll_id: str, coll_dir, f, coll: dict, src: dict) -> None:
    """Census-family collections: federal/third-party provider and license,
    local PMTiles like city collections (except the tabular commute flows),
    reference-period temporal extents, column notes into table:columns.
    """
    meta = CENSUS_META[src["dataset"]]
    coll["id"] = coll_rel(coll_id)
    coll["title"] = src["title"]
    coll["description"] = DESCRIPTIONS[coll_id]["description"]

    has_pmtiles = (coll_dir / f"{coll_id}.pmtiles").exists()
    ext = set(coll.get("stac_extensions", []))
    ext.update({PORTOLAN_SCHEMA, FILE_EXT, TABLE_EXT, THEMES_EXT})
    if has_pmtiles:
        ext.add(WML_EXT)
    coll["stac_extensions"] = sorted(ext)

    coll["license"] = src["license"]
    coll["updated"] = SYNC
    coll.setdefault("extent", {})["temporal"] = {
        "interval": [list(meta["interval"])]}

    group_title = GROUP_TITLES[GROUP_OF[coll_id]]
    prog_id, prog_title = meta["program"]
    coll["themes"] = [
        {"scheme": TOPIC_SCHEME,
         "concepts": [{"id": slugify(group_title), "title": group_title}]},
        {"scheme": src["docs"],
         "concepts": [{"id": prog_id, "title": prog_title}]},
    ]
    coll["keywords"] = meta["keywords"]

    notes = COLUMN_NOTES.get(coll_id, {})
    if notes and coll.get("table:columns"):
        for col in coll["table:columns"]:
            if col["name"] in notes:
                col["description"] = linkify(notes[col["name"]])

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
    if pq.exists():
        rc = duck(f"SELECT count(*) AS n FROM '{pq}'")
        if rc:
            coll["table:row_count"] = rc[0]["n"]
            if "geoparquet:feature_count" in coll:
                coll["geoparquet:feature_count"] = rc[0]["n"]

    name, url = meta["provider"]
    coll["providers"] = [
        {"name": name, "roles": ["producer", "licensor"], "url": url},
        HOST,
    ]

    links = [l for l in coll.get("links", [])
             if l["rel"] not in ("self", "via")]
    ensure_link(links, "describedby", "./README.md", "text/markdown")
    ensure_link(links, "agents", "./AGENTS.md", "text/markdown")
    ensure_link(links, "license", src["license_url"], "text/html",
                f"{name} — data license and terms")
    ensure_link(links, "via", src["docs"], "text/html",
                f"{prog_title} documentation")
    from write_metadata import census_source_url
    data_url = census_source_url(src["dataset"])
    if data_url != src["docs"]:
        # text/html even for a parquet target: rashid's PTL-PRO-001 requires
        # it on every via link.
        ensure_link(links, "via", data_url, "text/html",
                    f"{prog_title} source data")
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
            l["title"] = group_title
    coll["links"] = links

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
    # Same reasoning as the city path: a README asset lists its own checksum
    # in its own Files table, so it goes stale the moment `portolan readme`
    # runs — the `describedby` link is how the spec exposes the README.
    assets.pop("documentation", None)
    coll["assets"] = assets

    f.write_text(json.dumps(coll, indent=2) + "\n")
    print(f"✓ {coll_id}: {len(style_files)} style assets, "
          f"{'local pmtiles' if has_pmtiles else 'tabular'} (census)")


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
    # Catalog logo per portolan-spec#136: the city's own fleur-de-lis, the
    # same SVG the data browser uses for its wordmark and favicon.
    ensure_link(links, "icon", "./_assets/fleur-de-lis.svg", "image/svg+xml",
                "City of St. Louis")
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
    from sources import GROUP_CAPTIONS
    f = CATALOG / group / "catalog.json"
    if not f.exists():
        return
    cat = json.loads(f.read_text())
    cat["stac_extensions"] = sorted(set(cat.get("stac_extensions", [])) | {PORTOLAN_SCHEMA})
    cat["updated"] = SYNC
    # A group catalog created bare by `portolan add` arrives with no title
    # and a "Catalog: <slug>" description; fill both from sources.py so a
    # new group (demographics) matches the established ones.
    cat["title"] = GROUP_TITLES[group]
    if not cat.get("description") or cat["description"].startswith("Catalog:"):
        cat["description"] = GROUP_CAPTIONS[group]
    links = [l for l in cat["links"] if l["rel"] not in ("child", "self")]
    ensure_link(links, "describedby", "./README.md", "text/markdown")
    ensure_link(links, "agents", "./AGENTS.md", "text/markdown")
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
