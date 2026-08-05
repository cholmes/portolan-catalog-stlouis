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
from sources import SOURCES, coll_rel, linkify

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"
DESCRIPTIONS = json.loads((ROOT / "docs" / "portal-descriptions.json").read_text())

CONTACT = 'contact:\n  name: "Chris Holmes"\n  email: "cholmes@9eo.org"\n'

ROOT_YAML = f"""\
title: "City of St. Louis Open Data (Cloud-Native Mirror)"
description: |
  Cloud-native mirror of 51 datasets from the
  [City of St. Louis open data portal](https://www.stlouis-mo.gov/data/),
  the city's public ArcGIS servers, and its
  [ArcGIS Online organization](https://stlcity.maps.arcgis.com/): about 6.6
  million features as GeoParquet and PMTiles with STAC metadata, organized
  into 13 department catalogs. Explore it in the
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
  GeoParquet and PMTiles. The city publishes no explicit data license;
  see each dataset's page on the portal for its terms and context.
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


def collection_yaml(coll_id: str) -> str:
    src = SOURCES[coll_id]
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
        "processing_notes: |",
        f"  Mirrored from the City of St. Louis open data portal"
        f" ({src['portal_page']}).",
        f"  Source: {src.get('service') or src.get('url')}"
        f" ({'ArcGIS REST service' if src['type'] == 'arcgis' else 'portal download'}),",
        "  converted to GeoParquet (zstd, spatially ordered, covering bbox)"
        " and PMTiles.",
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
