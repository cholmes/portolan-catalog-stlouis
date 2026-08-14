#!/usr/bin/env python3
"""Write .portolan/metadata.yaml for the catalog root and every collection.

Descriptions come verbatim from the city's dataset pages
(docs/portal-descriptions.json, scraped from the portal) — nothing invented.
The portal publishes no explicit data license, so license is "other" with
license_url pointing at each dataset's portal page.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sources import SOURCES, SOURCE_FILES, coll_rel, linkify, source_files

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"
DESCRIPTIONS = json.loads((ROOT / "docs" / "portal-descriptions.json").read_text())
# Overture collections get their own description file — wording drawn from
# Overture's documentation plus the not-city-data demonstration paragraph.
DESCRIPTIONS.update(json.loads(
    (ROOT / "docs" / "overture-descriptions.json").read_text()))

CONTACT = 'contact:\n  name: "Chris Holmes"\n  email: "cholmes@9eo.org"\n'

ROOT_YAML = f"""\
title: "City of St. Louis Open Data (Cloud-Native Mirror)"
description: |
  Cloud-native mirror of 51 datasets from the
  [City of St. Louis open data portal](https://www.stlouis-mo.gov/data/),
  the city's public ArcGIS servers, and its
  [ArcGIS Online organization](https://stlcity.maps.arcgis.com/): about 6.6
  million features as GeoParquet and PMTiles with STAC metadata, organized
  into 11 topic catalogs. Alongside the city's own data, 10 collections
  tagged `overture` carry St. Louis extracts of the
  [Overture Maps Foundation](https://overturemaps.org/) global datasets —
  buildings, transportation, places, addresses, and more — demonstrating how
  a city catalog can blend in other locally relevant open data. Explore it
  in the
  [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/),
  [browse the files on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror),
  or query any file directly with DuckDB — no download needed. Not an
  official city service.
{CONTACT}license: "other"
license_url: "https://www.stlouis-mo.gov/data/"
attribution: "City of St. Louis"
source_url: "https://www.stlouis-mo.gov/data/"
keywords: [st-louis, missouri, open-data, city-government, parcels, boundaries, cloud-native, geoparquet, stac, pmtiles]
processing_notes: |
  Mirrored from the City of St. Louis open data portal and the city's public
  ArcGIS REST services (maps6/maps8/maps9.stlouis-mo.gov). Source formats
  (ArcGIS layers, Shapefile, GeoJSON, CSV, DBF) converted to cloud-native
  GeoParquet and PMTiles.

  Every collection says where its data came from and what was done to it, in
  its own processing notes. Where the city serves a downloadable file, that
  file is published as a `source` asset pointing straight at stlouis-mo.gov,
  with the size and checksum of the bytes it served at sync time — so the
  original stays one click away and this mirror never becomes the only route
  to it. Where the origin is a live ArcGIS service there is no file to link,
  so it is recorded as a `via` link and the extraction command is written out
  in the collection's notes.

  The city publishes no explicit data license; see each dataset's page on the
  portal for its terms and context.
examples:
  - engine: duckdb
    description: "LRA-owned vacant lots per neighborhood, joining two collections remotely"
    code: |
      INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
      WITH lots AS (
        SELECT ST_Centroid(geometry) AS pt
        FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/development/lra-property/lra-property.parquet'
        WHERE Usage ILIKE 'vacant lot')
      SELECT n.NHD_NAME, count(*) AS lra_vacant_lots
      FROM lots
      JOIN 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/planning/neighborhoods/neighborhoods.parquet' n
        ON ST_Intersects(lots.pt, n.geometry)
      GROUP BY 1 ORDER BY 2 DESC LIMIT 10;
"""


def yq(s: str) -> str:
    """YAML-safe double-quoted scalar."""
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


BASE = "https://data.source.coop/tge-labs/st-louis-open-data-mirror"
BROWSE = "https://source.coop/tge-labs/st-louis-open-data-mirror"
BROWSER = "https://cholmes.github.io/stlouis-data-browser"

# The column that best summarizes each collection, for the generated
# quick-start example (fallback: plain preview).
EXAMPLE_COL = {
    "parcels": "Zoning", "zoning": "LAYER", "city-trees": "CONDITION",
    "csb-311-requests": '"GROUP"', "streets": "Class",
    "parks": "NEW_CLASS", "historic-districts": "DIS_TYPE",
    "tif-districts": "Incentive_Status", "lra-property": "Status",
    "community-improvement-districts": "Active",
    "special-business-districts": "Active", "wards": "NAME",
    "crime": "NIBRSCategory", "lead-service-lines": "utilstatus_desc",
    "market-value-analysis": "MVACluster", "vacancy-composite": "TOLEMI_DEF",
    "land-use": "SLUP_LATES", "forest-park-trees": "Condition",
    "neighborhood-organizations": "active", "floodplain": "FLD_ZONE",
    "historic-landmarks": "SITE_TYPE", "street-sweeping": "Day_Wk",
    "animal-bites": "ANIMAL_TYPE", "property-sales": "SaleTypeDescr",
    "property-taxes": "BillYear", "electrical-permits": "APPTYPE",
    "mechanical-permits": "APPTYPE", "plumbing-permits": "APPTYPE",
    "occupancy-permits": "APPTYPE", "street-permits": "TYPE",
    "election-results-nov-2024": "Contest_Title",
    "parcels-history": "era", "tornado-damage-2025": "efscale",
    "polling-places": "Early_Voting_Available",
    "business-licenses": None, "tax-sales": None,
    "overture-buildings": "subtype", "overture-transportation": "class",
    "overture-places": "basic_category", "overture-addresses": "postcode",
    "overture-divisions": "subtype", "overture-infrastructure": "subtype",
    "overture-land": "subtype", "overture-land-cover": "subtype",
    "overture-land-use": "subtype", "overture-water": "subtype",
}


def example_block(coll_id: str) -> str:
    from sources import coll_rel
    url = f"{BASE}/{coll_rel(coll_id)}/{coll_id}.parquet"
    col = EXAMPLE_COL.get(coll_id)
    if col:
        code = (f"INSTALL httpfs; LOAD httpfs;\n"
                f"SELECT {col}, count(*) AS n\n"
                f"FROM '{url}'\n"
                f"GROUP BY 1 ORDER BY 2 DESC LIMIT 10;")
        what = f"Count rows by {col.strip(chr(34))}, straight off the published file"
    else:
        code = (f"INSTALL httpfs; LOAD httpfs;\n"
                f"SELECT * FROM '{url}' LIMIT 5;")
        what = "Preview the first rows, straight off the published file"
    lines = ["examples:", "  - engine: duckdb",
             f"    description: {yq(what)}", "    code: |"]
    lines += [f"      {ln}" for ln in code.split("\n")]
    return "\n".join(lines)


# What actually happened to each dataset between the city's server and the
# published Parquet, beyond the common convert-and-tile. Anything that
# changed row counts, column values or coordinates has to be stated, or the
# mirror quietly misrepresents the city's data.
PROCESSING_EXTRA = {
    "parcels-history": "The five era archives were unpacked and concatenated "
        "into one collection with an added `era` column, so a parcel can be "
        "followed across the 1997-2020 series in a single query.",
    "crime": "The monthly files arrive in mixed encodings, so each was "
        "normalized to UTF-8 before they were merged into one table.",
    "csb-311-requests": "The yearly CSVs arrive in mixed UTF-8 and "
        "Windows-1252 and were normalized to UTF-8. Coordinates come as Web "
        "Mercator `SRX`/`SRY` columns and were reprojected to EPSG:4326; "
        "points falling outside the city were set to null rather than "
        "dropped, and the roughly 18,000 requests with no coordinates at all "
        "are kept as null-geometry rows so the counts still match the city's.",
    "property-taxes": "The Access database was unpacked and its `Prcl` table "
        "exported with `mdb-export` before conversion.",
    "property-sales": "The Access database was unpacked and its `PrclSale` "
        "table exported with `mdb-export`, then left-joined to the database's "
        "own `CdSaleType` lookup table so each sale carries a readable "
        "`SaleTypeDescr` instead of a bare code.",
    "street-permits": "The CSV arrives in Windows-1252 and was normalized to "
        "UTF-8.",
    "lra-property": "The SLDC service carries every parcel in the city, not "
        "just the LRA's; this collection is the `LRA = 'YES'` subset.",
    "lead-service-lines": "The service returns coded domain values; the "
        "material and status codes were decoded to their labels using the "
        "service's own domain definitions, alongside the raw codes.",
    "animal-bites": "The city geocodes these to addresses; a handful land "
        "well outside the city, so points were clipped to the city boundary "
        "with a small buffer.",
    "bike-infrastructure": "The service splits the network across five "
        "layers; all five were extracted and merged, with a `source_layer` "
        "column recording which one each feature came from.",
    "election-results-nov-2024": "This is a FeatureServer table rather than a "
        "map layer, so it was paged through `/query` with "
        "`returnGeometry=false` and written straight to Parquet.",
    "land-use": "This mirrors the 2025 Strategic Land Use Plan from the live "
        "service. The 2019 shapefile edition the portal still offers is "
        "linked as a source asset but is not what this collection contains.",
    "wards": "The city's Hosted ward FeatureServer carries only 10 of the 14 "
        "wards, so this collection is built from the portal's shapefile "
        "download, which has all 14.",
}

# Collections whose Parquet has no geometry of its own, and whose map layer is
# therefore built by running the documented join against a geometry
# collection (tools/make_joined_pmtiles.py).
JOIN_NOTE = {
    "property-taxes": ("parcels", "parcel id"),
    "property-sales": ("parcels", "parcel id"),
    "electrical-permits": ("parcels", "parcel handle"),
    "mechanical-permits": ("parcels", "parcel handle"),
    "plumbing-permits": ("parcels", "parcel handle"),
    "occupancy-permits": ("parcels", "parcel handle"),
    "street-permits": ("neighborhoods", "neighborhood name"),
    "election-results-nov-2024": ("election-precincts", "ward and precinct"),
}


def format_phrase(coll_id: str) -> str:
    """"zipped Shapefile", "GeoJSON", ... — from the source file's own title."""
    for e in source_files(coll_id):
        if e["primary"] and "(" in e["title"]:
            return e["title"].rsplit("(", 1)[1].rstrip(")")
    return "portal download"


def overture_processing_notes(coll_id: str) -> str:
    from sources import OVERTURE_RELEASE, OVERTURE_S3
    src = SOURCES[coll_id]
    types = src["types"]
    globs = "\n".join(
        f"      {OVERTURE_S3}/theme={src['theme']}/type={t}/*.parquet"
        for t in types)
    paras = [
        f"Extracted from Overture Maps release {OVERTURE_RELEASE} with "
        f"DuckDB, reading the release's GeoParquet straight from Overture's "
        f"public S3 bucket:\n\n{globs}\n\nThe extract keeps every feature "
        f"that intersects the city-boundary collection's bbox "
        f"(-90.3205, 38.5320, -90.1663, 38.7743) — a rectangle, so the "
        f"Illinois shore of the Mississippi is included. Geometries that "
        f"cross the edge of the box are clipped to it (otherwise a feature "
        f"whose bounding box merely touches St. Louis arrives whole — the "
        f"full United States polygon, in the divisions theme's case). No "
        f"other filtering, and no columns were altered; Overture's own "
        f"`bbox` covering column was dropped and rebuilt during conversion."]
    if len(types) > 1:
        paras.append(
            f"The theme's {len(types)} feature types "
            f"({', '.join(types)}) are merged into one collection with an "
            f"`overture_type` column recording which type each feature is.")
    paras.append(
        "Converted to GeoParquet with gpio — zstd compression, Hilbert row "
        "order, and a covering bbox column with row-group statistics, so a "
        "spatial filter can skip most of the file over the network.")
    paras.append(
        "The PMTiles are not built by this mirror: the tiles asset points at "
        "Overture's own release-pinned global tiles for the "
        f"`{src['theme']}` theme — the tiles behind explore.overturemaps.org "
        "— served from Overture's public bucket. The styles here select just "
        "this collection's layers from them. The tiles cover the whole "
        "world, so zooming out shows global data even though the Parquet in "
        "this collection is only the St. Louis extract.")
    return "\n\n".join(paras)


def processing_notes(coll_id: str) -> str:
    src = SOURCES[coll_id]
    if src["type"] == "overture":
        return overture_processing_notes(coll_id)
    origin = src.get("service") or src.get("url")
    paras = [
        f"Mirrored from the City of St. Louis open data portal "
        f"({src['portal_page']}). Nothing was added to the data and no "
        f"features were dropped except where noted below."
    ]
    if src["type"] == "arcgis":
        layers = f' --layers "{src["layers"]}"' if src.get("layers") else ""
        paras.append(
            "Extracted from the city's own ArcGIS REST service with the "
            "Portolan CLI:\n\n"
            f"    portolan extract arcgis \\\n      {origin}{layers} --raw\n\n"
            "That pages the service's `/query` endpoint for every feature, so "
            "this is the whole layer rather than the display-capped sample a "
            "browser request returns, and it carries across the service's "
            "field aliases. The service's own ESRI renderer was captured at "
            "the same time and is republished here as "
            "`styles/city-renderer.json`, so the map can be drawn in the "
            "city's own symbology.")
    elif src.get("crime_scrape"):
        paras.append(
            f"SLMPD does not publish a single file or a service — it posts "
            f"one CSV per month on {origin}, and the portal's dataset page "
            f"just points there. The index is read and every CSV it links is "
            f"downloaded, so the mirror carries whatever months were "
            f"published at sync time.")
    else:
        paras.append(
            f"Downloaded from the city's portal: {origin} "
            f"({format_phrase(coll_id)}).")
    if coll_id in PROCESSING_EXTRA:
        paras.append(PROCESSING_EXTRA[coll_id])
    paras.append(
        "Converted to GeoParquet with gpio — zstd compression, Hilbert row "
        "order, and a covering bbox column with row-group statistics, so a "
        "spatial filter can skip most of the file over the network — and "
        "tiled to PMTiles with tippecanoe."
        if coll_id not in JOIN_NOTE else
        "Converted to Parquet with gpio (zstd), keeping the source's own "
        "columns. The city publishes this without geometry, so it stays that "
        "way here.")
    if coll_id in JOIN_NOTE:
        other, key = JOIN_NOTE[coll_id]
        paras.append(
            f"The map layer is a derived product: the PMTiles were built by "
            f"actually running the documented join against the `{other}` "
            f"collection on {key}, so the data can be mapped without anyone "
            f"having to run the join first. The Parquet is unjoined. The "
            f"exact query is in AGENTS.md.")
    if SOURCE_FILES.get(coll_id):
        paras.append(
            "The city's own file(s) are published as `source` assets on this "
            "collection, linked directly to stlouis-mo.gov — this mirror "
            "never becomes the only way to reach the original.")
    return "\n\n".join(paras)


def indent_block(key: str, text: str) -> str:
    lines = [f"{key}: |"]
    for para in text.split("\n"):
        lines.append(f"  {para}" if para else "")
    return "\n".join(lines)


OVERTURE_ATTRIBUTION_URL = "https://docs.overturemaps.org/attribution/"


def overture_yaml(coll_id: str) -> str:
    from sources import OVERTURE_S3, coll_rel
    src = SOURCES[coll_id]
    desc = DESCRIPTIONS[coll_id]["description"]
    linked = (f"{desc} Explore it in the [St. Louis data browser]"
              f"({BROWSER}/#/{coll_rel(coll_id)}/collection.json).")
    kw = ["overture", "overture-maps", src["theme"], "st-louis",
          "open-data"] + [t.replace("_", "-") for t in src["types"]]
    lines = [
        f"title: {yq(src['title'])}",
        f"description: {yq(linked)}",
        CONTACT.rstrip(),
        f"license: {yq(src['license'])}",
        f"license_url: {yq(OVERTURE_ATTRIBUTION_URL)}",
        'attribution: "Overture Maps Foundation"',
        f"source_url: {yq(OVERTURE_S3 + '/theme=' + src['theme'])}",
        f"keywords: [{', '.join(dict.fromkeys(kw))}]",
        indent_block("processing_notes", processing_notes(coll_id)),
        example_block(coll_id),
    ]
    return "\n".join(l for l in lines if l) + "\n"


def collection_yaml(coll_id: str) -> str:
    src = SOURCES[coll_id]
    if src["type"] == "overture":
        return overture_yaml(coll_id)
    desc = DESCRIPTIONS.get(coll_id, {}).get("description", "")
    dept = src["department"]
    kw = ["st-louis", "missouri", "open-data"] + coll_id.split("-")
    from sources import coll_rel
    linked = (f"{linkify(desc)} Mirrored from [the city's open data portal]"
              f"({src['portal_page']}); explore it in the "
              f"[St. Louis data browser]({BROWSER}/#/{coll_rel(coll_id)}/collection.json).")
    lines = [
        f"title: {yq(src['title'])}",
        f"description: {yq(linked if desc else src['title'])}",
        CONTACT.rstrip(),
        'license: "other"',
        f"license_url: {yq(src['portal_page'])}",
        f"attribution: {yq('City of St. Louis — ' + dept)}",
        f"source_url: {yq(src.get('service') or src.get('url'))}",
        f"keywords: [{', '.join(dict.fromkeys(kw))}]",
        indent_block("processing_notes", processing_notes(coll_id)),
        example_block(coll_id),
    ]
    return "\n".join(l for l in lines if l) + "\n"


def main() -> None:
    d = CATALOG / ".portolan"
    d.mkdir(exist_ok=True)
    (d / "metadata.yaml").write_text(ROOT_YAML)
    print("✓ catalog root metadata.yaml")
    for coll_id in SOURCES:
        cd = CATALOG / coll_rel(coll_id) / ".portolan"
        if not (CATALOG / coll_rel(coll_id)).exists():
            print(f"✗ missing collection dir: {coll_id}")
            continue
        cd.mkdir(exist_ok=True)
        (cd / "metadata.yaml").write_text(collection_yaml(coll_id))
        print(f"✓ {coll_id}")


if __name__ == "__main__":
    main()
