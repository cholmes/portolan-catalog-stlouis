#!/usr/bin/env python3
"""Generate AGENTS.md for the catalog root and every collection.

Structure: overview (portal text) → access (runnable DuckDB against the
published URL) → key fields → quirks → joins/related. The per-collection
NOTES below hold the human knowledge gathered during the build (profiling
results, join keys, source quirks); everything else templates from
collection.json.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sources import SOURCES

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"
BASE = "https://data.source.coop/tge-labs/st-louis-open-data-mirror"
DESCRIPTIONS = json.loads((ROOT / "docs" / "portal-descriptions.json").read_text())

# fields: worth-knowing columns; quirks: caveats found in profiling;
# joins: cross-collection recipes; example: an extra worked query.
NOTES = {
    "parcels": {
        "fields": {
            "HANDLE": "assessor parcel handle — the city-wide parcel join key",
            "ParcelId": "10-digit parcel id (same as AsrParcelId elsewhere)",
            "OWNERNAME": "current owner",
            "AsdTotal": "total assessed value (dollars)",
            "VacantLot": "Access-style boolean: -1 vacant, 0 not",
            "FirstYearBuilt": "0 means unknown (28k parcels)",
            "NBRHD": "neighborhood number (joins neighborhoods.NHD_NUM)",
            "WARD": "current ward number",
            "Zoning": "zoning code on the parcel record",
        },
        "quirks": "134,362 parcels. Owner addresses and legal descriptions are "
                  "as-recorded by the assessor; casing is inconsistent. Many "
                  "numeric codes (OwnerCode, AsrClassCode, SpecParcelType) have "
                  "no published decode.",
        "joins": "property-sales.AsrParcelId = parcels.ParcelId; "
                 "tax-abated-parcels and lra-property share HANDLE; "
                 "neighborhoods via NBRHD = NHD_NUM; wards via WARD.",
    },
    "zoning": {
        "fields": {"LAYER": "district letter A-L; official names are in the "
                            "default style legend (from the city's renderer)"},
        "quirks": "Parcel-level zoning (126,945 features). Overlay districts "
                  "(CUP/FBD/SUD) live on a separate service layer not mirrored "
                  "here yet.",
        "joins": "Spatial join to parcels, or parcels.Zoning carries a code "
                 "per parcel record.",
    },
    "city-trees": {
        "fields": {
            "COMMON": "common name; the literal value 'Vacant' marks an empty "
                      "planting site (30,935 of them)",
            "DBH": "trunk diameter (inches) at breast height",
            "CONDITION": "Excellent..Dead, Stump; N/A mostly = vacant sites",
            "LOCATION_TYPE": "Easement (street trees), Park, Median",
        },
        "quirks": "134,588 records = trees AND empty planting sites; filter "
                  "COMMON <> 'Vacant' for actual trees.",
        "joins": "Address fields (STREET_NUM, STREET) join loosely to parcel "
                 "situs addresses.",
    },
    "csb-311-requests": {
        "fields": {
            "REQUESTID": "request id",
            "DATETIMEINIT": "opened (2008-09 through present)",
            "GROUP": "category (37 values; trash/debris is the biggest)",
            "STATUS": "CLOSED/CANCEL/open-ish states; case varies by era",
            "PROBADDRESS": "problem address",
            "NEIGHBORHOOD": "neighborhood number (joins neighborhoods.NHD_NUM)",
            "WARD": "ward at time of request",
        },
        "quirks": "1,477,057 rows; 18,132 have no usable coordinates (geometry "
                  "IS NULL) — they remain in the table, so tabular counts and "
                  "map counts differ. Coordinates were Web-Mercator SRX/SRY in "
                  "the source, reprojected to WGS84; ~450 out-of-city points "
                  "were nulled. Status casing varies (CLOSED vs Closed).",
        "joins": "PROBADDRESS matches parcel situs addresses (fuzzy); "
                 "NEIGHBORHOOD = neighborhoods.NHD_NUM; WARD = wards.district.",
    },
    "property-sales": {
        "fields": {
            "AsrParcelId": "parcel id — joins parcels.ParcelId",
            "SaleDate": "text m/d/yy from the source MDB",
            "SalePrice": "dollars; 0 on many non-market transfers",
            "SaleType": "code; SaleTypeDescr carries the source's own decode",
        },
        "quirks": "191,829 sales from the assessor's Access database "
                  "(PrclSale table). Dates are 2-digit-year strings — parse "
                  "with strptime('%m/%d/%y %H:%M:%S') and sanity-check the "
                  "century. No geometry: join to parcels for mapping.",
        "joins": "parcels via AsrParcelId = ParcelId (10-digit, zero-padded).",
        "example": (
            "-- median sale price by neighborhood, 2020s market sales\n"
            f"SELECT n.NHD_NAME, median(s.SalePrice) mp, count(*) n_sales\n"
            f"FROM '{BASE}/property-sales/property-sales.parquet' s\n"
            f"JOIN '{BASE}/parcels/parcels.parquet' p ON s.AsrParcelId = p.ParcelId\n"
            f"JOIN '{BASE}/neighborhoods/neighborhoods.parquet' n ON p.NBRHD = n.NHD_NUM\n"
            "WHERE s.SalePrice > 1000 AND strptime(s.SaleDate, '%m/%d/%y %H:%M:%S') >= DATE '2020-01-01'\n"
            "GROUP BY 1 ORDER BY 2 DESC LIMIT 15;"),
    },
    "lra-property": {
        "fields": {
            "Handle": "parcel handle — joins parcels.HANDLE",
            "Status": "Available (8,762) / holds / SOLD / Unavailable",
            "Usage": "Vacant Lot vs Residential etc. — case varies, use ILIKE",
            "Property_Source": "how the LRA acquired it (Tax Suit dominates)",
        },
        "quirks": "The source service layer contains every city parcel with an "
                  "LRA flag; this collection is the LRA='YES' subset (9,467).",
        "joins": "parcels via Handle = HANDLE.",
    },
    "neighborhoods": {
        "fields": {"NHD_NUM": "official number", "NHD_NAME": "official name"},
        "joins": "parcels.NBRHD, csb-311-requests.NEIGHBORHOOD, and "
                 "city-blocks.NBRHD all carry NHD_NUM.",
    },
    "wards": {
        "fields": {"district": "ward number as string", "name": "ward name",
                   "population": "2020 census population, with race columns"},
        "quirks": "The 10 wards from 2020 redistricting (effective 2023); "
                  "older datasets reference the previous 28 wards (WARD10 "
                  "columns elsewhere).",
    },
    "streets": {
        "fields": {"Street_Name_Full": "full name",
                   "Class": "source class code (A31/A41/A6x/A73, no published decode)"},
    },
    "tif-districts": {
        "fields": {"Incentive_Status": "Active (110) / Terminated / Retired / "
                                       "Never Approved / On Hold / MODESA"},
    },
    "tax-abated-parcels": {
        "fields": {"HANDLE": "joins parcels.HANDLE",
                   "AbatementStartYear": "2001-2025",
                   "AbatementEndYear": "when the abatement runs out"},
    },
    "historic-districts": {
        "fields": {"DISNAME": "district name",
                   "DIS_TYPE": "National (85) / Local / Certified Local / Landmark"},
    },
    "election-precincts": {
        "fields": {"name": "'W <ward> P <precinct>'"},
        "quirks": "The BOE FeatureServers reject paged queries, so this comes "
                  "from the static shapefile (reprojected from MO State Plane "
                  "East to WGS84).",
    },
    "parks": {"fields": {"TEXT_": "park name", "ACRES": "official acreage",
                         "NEW_CLASS": "park classification"}},
    "city-blocks": {
        "fields": {"Name": "city block number (string); numbering grew "
                           "outward from the riverfront",
                   "BLOCK_HANDLE": "block handle; parcels.CityBlock relates"},
    },
    "community-improvement-districts": {
        "fields": {"Name": "district name", "Active": "Y (70) / N (21) / blank"}},
    "special-business-districts": {
        "fields": {"Name": "district name", "Active": "Y/N"}},
    "opportunity-zones": {"fields": {"District_Name": "zone name"}},
    "police-districts": {"fields": {"DISTNO": "district number 1-6 (string)"}},
    "city-boundary": {"quirks": "One polygon. St. Louis is an independent "
                                "city — inside no county since 1876."},
}


def collection_agents(coll_id: str) -> str:
    src = SOURCES[coll_id]
    coll = json.loads((CATALOG / coll_id / "collection.json").read_text())
    notes = NOTES.get(coll_id, {})
    desc = DESCRIPTIONS.get(coll_id, {}).get("description", "")
    n = coll.get("table:row_count", "?")
    geom = coll.get("geoparquet:geometry_type")
    url = f"{BASE}/{coll_id}/{coll_id}.parquet"

    out = [f"# AGENTS.md — {src['title']}", ""]
    out += [f"{desc}" if desc else src["title"], ""]
    out += [f"{n:,} rows" .replace(",", " ") if isinstance(n, int) else str(n)]
    out[-1] = (f"{n:,} rows; geometry: {geom} (WGS84 lon/lat unless noted)."
               if geom else f"{n:,} rows; tabular (no geometry).")
    out += ["", "## Access", "", "```sql",
            "INSTALL httpfs; LOAD httpfs;  -- DuckDB",
            f"SELECT * FROM '{url}' LIMIT 5;", "```", ""]
    if geom:
        out += [f"PMTiles for maps: `{BASE}/{coll_id}/{coll_id}.pmtiles` "
                f"(layer `{coll_id}`), styled by `styles/*.json` — "
                "`styles/default.json` is the default.", ""]
    fields = notes.get("fields")
    if fields:
        out += ["## Key fields", ""]
        out += [f"- `{k}` — {v}" for k, v in fields.items()]
        out += [""]
    out += ["Full schema: `table:columns` in collection.json.", ""]
    if notes.get("quirks"):
        out += ["## Quirks", "", notes["quirks"], ""]
    if notes.get("joins"):
        out += ["## Joins", "", notes["joins"], ""]
    if notes.get("example"):
        out += ["## Example", "", "```sql", notes["example"], "```", ""]
    out += ["## Provenance", "",
            f"Mirror of [{src['title']}]({src['portal_page']}) from the City "
            f"of St. Louis open data portal; source: {src.get('service') or src.get('url')}. "
            "No explicit license is published — see the portal page. "
            f"Synced {coll.get('updated', '')}.", ""]
    return "\n".join(out)


ROOT_AGENTS = f"""# AGENTS.md — City of St. Louis Open Data (Cloud-Native Mirror)

Twenty collections mirrored from https://www.stlouis-mo.gov/data/ as
GeoParquet (+ PMTiles for the 19 geospatial ones). Everything is
range-readable over HTTPS — no download needed.

## Access pattern

```sql
INSTALL httpfs; LOAD httpfs; INSTALL spatial; LOAD spatial;  -- DuckDB
SELECT * FROM '{BASE}/parcels/parcels.parquet' LIMIT 5;
```

Catalog root: `{BASE}/catalog.json`. Every collection has its own
AGENTS.md with fields, quirks, and joins.

## The join graph

`parcels` is the hub (134,362 rows):

- `property-sales.AsrParcelId` = `parcels.ParcelId`
- `lra-property.Handle` / `tax-abated-parcels.HANDLE` = `parcels.HANDLE`
- `parcels.NBRHD` = `neighborhoods.NHD_NUM` = `csb-311-requests.NEIGHBORHOOD`
- `parcels.WARD` = `wards.district`; spatial joins work for everything else

## Read this first

- All geometry is WGS84 lon/lat (EPSG:4326).
- `csb-311-requests` has 18k rows with NULL geometry — table counts ≠ map counts.
- Access-style booleans appear as 0/-1 (e.g. `parcels.VacantLot`: -1 = vacant).
- No explicit data license is published by the city; each collection's
  `rel: license` link points at its portal page.
- The catalog is a mirror, not an official city service. `updated` on each
  object is the sync time.
"""


def main() -> None:
    (CATALOG / "AGENTS.md").write_text(ROOT_AGENTS)
    print("✓ catalog AGENTS.md")
    for coll_id in SOURCES:
        d = CATALOG / coll_id
        if not (d / "collection.json").exists():
            continue
        (d / "AGENTS.md").write_text(collection_agents(coll_id))
        print(f"✓ {coll_id}")


if __name__ == "__main__":
    main()
