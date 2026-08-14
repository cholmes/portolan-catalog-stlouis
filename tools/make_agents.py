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
from sources import SOURCES, coll_rel

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"
BASE = "https://data.source.coop/tge-labs/st-louis-open-data-mirror"
# Human-facing markdown links use source.coop so pages render in the browser
BROWSE = "https://source.coop/tge-labs/st-louis-open-data-mirror"
BROWSER = "https://cholmes.github.io/stlouis-data-browser"
DESCRIPTIONS = json.loads((ROOT / "docs" / "portal-descriptions.json").read_text())
DESCRIPTIONS.update(json.loads(
    (ROOT / "docs" / "overture-descriptions.json").read_text()))

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
        "quirks": "1,477,057 rows; 18,177 have no usable coordinates (geometry "
                  "IS NULL) — they remain in the table, so tabular counts and "
                  "map counts differ. Coordinates were Web-Mercator SRX/SRY in "
                  "the source, reprojected to WGS84; ~500 points falling "
                  "outside the (buffered) city boundary were nulled. Status "
                  "casing varies (CLOSED vs Closed).",
        "joins": "PROBADDRESS matches parcel situs addresses (fuzzy); "
                 "NEIGHBORHOOD = neighborhoods.NHD_NUM; WARD = wards.DISTRICT.",
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
        "fields": {"DISTRICT": "ward number as string", "NAME": "ward name",
                   "POPULATION": "2020 census population, with race columns"},
        "quirks": "The 14 wards from 2020 redistricting (effective 2023); "
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
    "lead-service-lines": {
        "fields": {
            "address": "service address",
            "utilstatus": "utility-side status, domain-coded: 0 Unknown, 1 Lead, 2 Non-Lead, 3 Galvanized Requiring Replacement",
            "custstatus": "customer-side status, same domain",
            "utilmaterial": "pipe material, domain-coded (109 Lead, 84 Copper, 89 Galvanized, 0 Unknown...)",
        },
        "quirks": "EPA-mandated lead service line inventory from the Water "
                  "Division AGOL org; 112,950 address points, actively "
                  "maintained. Material/status fields are numeric domain "
                  "codes — the decode lives in the default styles and in "
                  "staging/extracts/lead-service-lines/layer-metadata.json.",
        "joins": "address matches parcel situs addresses (fuzzy).",
    },
    "election-results-nov-2024": {
        "fields": {
            "F_Precinct": "precinct name",
            "Contest_Title": "contest",
            "Choice_Name": "candidate/choice",
            "Total_Votes": "votes (also Election_Day/Absentee/Provisional splits)",
            "Turnout_Percentage": "precinct turnout",
        },
        "quirks": "24,030 rows = precinct x contest x choice for the "
                  "November 5, 2024 general election. Tabular — join "
                  "election-precincts on precinct name for mapping.",
        "joins": "election-precincts.name relates to F_Precinct (both use "
                 "'W <ward> P <precinct>' style names; normalize whitespace).",
    },
    "vacancy-composite": {
        "fields": {"STREET_ADD": "address", "PROPERTY_T": "Land or Structure",
                   "TOLEMI_DEF": "vacancy classification", "PID1": "parcel id"},
        "quirks": "SLDC/Tolemi BuildingBlocks export (2025-01); 20,694 "
                  "parcels flagged vacant by at least one indicator.",
        "joins": "PID1/PID2 relate to parcels.ParcelId.",
    },
    "market-value-analysis": {
        "fields": {"geoid": "census block group GEOID",
                   "MVACluster": "market cluster A (strongest) - I (weakest)"},
        "quirks": "Reinvestment Fund 2024 MVA at block-group level; ~30 "
                  "market indicator columns.",
    },
    "wards-2010": {
        "quirks": "The 28-ward map in force 2011-2022 — the geography that "
                  "WARD10 columns elsewhere (city-blocks, parcels) reference."},
    "neighborhood-organizations": {
        "quirks": "A 2020 snapshot (source: 'as exported 6-20-20'); "
                  "contacts and activity status age accordingly."},
    "tornado-damage-2025": {
        "quirks": "NWS Damage Assessment Toolkit record of the May 16, 2025 "
                  "EF-3 tornado: one damage-path polygon plus 286 surveyed "
                  "points (source_layer distinguishes them)."},
}

# Overture collections share most quirks; per-collection extras below.
_OVERTURE_COMMON = (
    "Overture Maps Foundation data, not the city's — see the description. "
    "`id` is a GERS id (stable across Overture releases); `sources` records "
    "the upstream dataset per feature; struct/list columns (names, sources) "
    "are nested Parquet — DuckDB reads them natively. Geometries crossing "
    "the bbox edge are clipped to it.")
NOTES.update({
    "overture-buildings": {
        "fields": {
            "height": "measured height in meters — present on ~89% of "
                      "St. Louis footprints (median 4.4 m)",
            "num_floors": "floor count where known",
            "subtype": "building use (residential, commercial…) — mostly "
                       "null here",
            "overture_type": "building or building_part",
            "has_parts": "true when building_part rows carry the detail",
        },
        "quirks": _OVERTURE_COMMON,
        "joins": "Spatial join to parcels for assessor attributes; "
                 "overture-addresses points fall inside most footprints.",
    },
    "overture-transportation": {
        "fields": {
            "overture_type": "segment (roads/rail, lines) or connector "
                             "(intersections, points)",
            "class": "road class (motorway…footway) or rail gauge",
            "connectors": "list of connector GERS ids along each segment — "
                          "the routing graph",
            "speed_limits": "nested speed rules, possibly time-scoped",
        },
        "quirks": _OVERTURE_COMMON + " Connectors carry almost no "
                  "attributes; the graph meaning lives on segments.",
        "joins": "segment.connectors[] = connector.id rebuilds the graph.",
    },
    "overture-places": {
        "fields": {
            "basic_category": "flat category (restaurant, bar…)",
            "confidence": "0-1 — Overture's certainty the place exists",
            "operating_status": "open / closed markers",
        },
        "quirks": _OVERTURE_COMMON + " Compare against the city's "
                  "business-licenses collection for ground truth.",
    },
    "overture-addresses": {
        "fields": {"number": "street number", "street": "street name",
                   "postcode": "ZIP", "unit": "unit where present"},
        "quirks": _OVERTURE_COMMON,
        "joins": "Spatial join to parcels or overture-buildings; "
                 "fuzzy-match street+number against city permit tables.",
    },
    "overture-divisions": {
        "fields": {
            "overture_type": "division (label point) / division_area "
                             "(polygon) / division_boundary (line)",
            "subtype": "country, region, county, locality, neighborhood, "
                       "microhood",
            "population": "on division points where known",
        },
        "quirks": _OVERTURE_COMMON + " The country and region areas are "
                  "bbox clips of the full US/Missouri/Illinois polygons.",
        "joins": "Compare neighborhood areas with the city's neighborhoods "
                 "collection (spatial join).",
    },
    "overture-infrastructure": {
        "fields": {"subtype": "transportation, barrier, transit, power…",
                   "class": "finer class within the subtype"},
        "quirks": _OVERTURE_COMMON,
    },
    "overture-land": {
        "fields": {"subtype": "tree, forest, shrub, grass, sand, rock, "
                              "wetland", "class": "finer class"},
        "quirks": _OVERTURE_COMMON + " 61k of the 64k features are "
                  "individual tree points from OSM.",
        "joins": "Compare tree points with city-trees and "
                 "forest-park-trees (Forestry's inventories).",
    },
    "overture-land-cover": {
        "fields": {"subtype": "forest, shrub, grass, crop, wetland, "
                              "barren, urban"},
        "quirks": _OVERTURE_COMMON + " Derived from ESA WorldCover 10m "
                  "rasters, so polygons are pixel-edged.",
    },
    "overture-land-use": {
        "fields": {"subtype": "park, managed, residential, golf…",
                   "class": "the underlying OSM landuse value"},
        "quirks": _OVERTURE_COMMON,
        "joins": "Contrast with the city's own land-use (Strategic Land "
                 "Use Plan) and zoning collections.",
    },
    "overture-water": {
        "fields": {"subtype": "river, lake, pond, stream, canal, "
                              "human_made (pools)…",
                   "is_intermittent": "seasonal water",
                   "is_salt": "salt water"},
        "quirks": _OVERTURE_COMMON,
    },
})


# Documented joins for the tabular collections whose PMTiles are
# join-materialized (kept in sync with tools/make_joined_pmtiles.py JOINS).
from make_joined_pmtiles import JOINS  # noqa: E402


def join_section(coll_id: str) -> list:
    if coll_id not in JOINS:
        return []
    spec = JOINS[coll_id]
    right = spec["right"]
    right_url = f"{BASE}/{coll_rel(right)}/{right}.parquet"
    left_url = f"{BASE}/{coll_rel(coll_id)}/{coll_id}.parquet"
    sql = (
        f"INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;\n"
        f"COPY (\n"
        f"  SELECT {spec['select']}, p.geometry\n"
        f"  FROM '{left_url}' t\n"
        f"  JOIN '{right_url}' p\n"
        f"    ON {spec['on']}\n")
    if spec["mode"] == "aggregate":
        sql += "  GROUP BY p.NHD_NAME, p.geometry\n"
    elif spec["mode"] == "summary":
        sql += f"  GROUP BY {spec['group']}\n"
    sql += f") TO '{coll_id}-geo.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);"
    return [
        "## Reproduce the geometry join",
        "",
        "This collection is published as plain (non-geo) Parquet, exactly as "
        f"the city publishes it; its map layer (`{coll_id}.pmtiles`) is "
        f"materialized by joining to `{right}`. To build your own GeoParquet:",
        "",
        "```sql", sql, "```",
        "",
        "Then convert as needed:",
        "",
        "```bash",
        f"gpio convert geoparquet {coll_id}-geo.parquet {coll_id}-geo-optimized.parquet",
        f"gpio convert geopackage {coll_id}-geo.parquet {coll_id}.gpkg",
        f"gpio convert shapefile {coll_id}-geo.parquet {coll_id}.shp",
        "```",
        "",
    ]


def collection_agents(coll_id: str) -> str:
    src = SOURCES[coll_id]
    coll = json.loads((CATALOG / coll_rel(coll_id) / "collection.json").read_text())
    notes = NOTES.get(coll_id, {})
    desc = DESCRIPTIONS.get(coll_id, {}).get("description", "")
    n = coll.get("table:row_count", "?")
    geom = coll.get("geoparquet:geometry_type")
    url = f"{BASE}/{coll_rel(coll_id)}/{coll_id}.parquet"

    out = [f"# AGENTS.md — {src['title']}", ""]
    out += [f"{desc}" if desc else src["title"], ""]
    out += [f"{n:,} rows" .replace(",", " ") if isinstance(n, int) else str(n)]
    out[-1] = (f"{n:,} rows; geometry: {geom} (WGS84 lon/lat unless noted)."
               if geom else f"{n:,} rows; tabular (no geometry).")
    out += ["", "## Access", "", "```sql",
            "INSTALL httpfs; LOAD httpfs;  -- DuckDB",
            f"SELECT * FROM '{url}' LIMIT 5;", "```", ""]
    local_pm = CATALOG / coll_rel(coll_id) / f"{coll_id}.pmtiles"
    if geom and src["type"] == "overture" and not local_pm.exists():
        from sources import OVERTURE_TILES
        out += [f"PMTiles for maps: Overture's own global theme tiles at "
                f"`{OVERTURE_TILES}/{src['theme']}.pmtiles` "
                f"(layers {', '.join('`' + t + '`' for t in src['types'])}), "
                f"styled by `styles/*.json` — `styles/default.json` is the "
                "default. Not clipped to St. Louis: only the Parquet is the "
                "extract.", ""]
    elif geom:
        out += [f"PMTiles for maps: `{BASE}/{coll_rel(coll_id)}/{coll_id}.pmtiles` "
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
    out += join_section(coll_id)
    if notes.get("example"):
        out += ["## Example", "", "```sql", notes["example"], "```", ""]
    rel = coll_rel(coll_id)
    if src["type"] == "overture":
        from sources import OVERTURE_RELEASE, OVERTURE_S3
        out += ["## Links", "",
                f"- [View on the data browser]({BROWSER}/#/{rel}/collection.json) "
                "— map, styles, legends, downloads",
                f"- [Browse on Source Cooperative]({BROWSE}/{rel}/) — rendered "
                "README and file listing",
                f"- [Overture {src['theme']} theme guide]({src['docs']})",
                "", "## Provenance", "",
                f"St. Louis-bbox extract of the [Overture Maps Foundation]"
                f"(https://overturemaps.org/) {src['theme']} theme, release "
                f"{OVERTURE_RELEASE} "
                f"(`{OVERTURE_S3}/theme={src['theme']}/`) — **not** City of "
                f"St. Louis data. License: {src['license']} (see "
                "[Overture attribution](https://docs.overturemaps.org/attribution/)). "
                f"Synced {coll.get('updated', '')}.", ""]
        return "\n".join(out)
    out += ["## Links", "",
            f"- [View on the data browser]({BROWSER}/#/{rel}/collection.json) "
            "— map, styles, legends, downloads",
            f"- [Browse on Source Cooperative]({BROWSE}/{rel}/) — rendered "
            "README and file listing",
            f"- [Source dataset]({src['portal_page']}) on the City of "
            "St. Louis open data portal",
            "", "## Provenance", "",
            f"Mirror of [{src['title']}]({src['portal_page']}) from the City "
            f"of St. Louis; source: {src.get('service') or src.get('url')}. "
            "No explicit license is published — see the source page. "
            f"Synced {coll.get('updated', '')}.", ""]
    return "\n".join(out)


# Counted rather than stated: the catalog has grown from the original 20.
N_COLLECTIONS = len(list(CATALOG.glob("*/*/collection.json")))
N_TILED = len(list(CATALOG.glob("*/*/*.pmtiles")))
FORMATS = ("GeoParquet and PMTiles" if N_TILED == N_COLLECTIONS
           else f"GeoParquet, {N_TILED} of them also as PMTiles")

ROOT_AGENTS = f"""# AGENTS.md — City of St. Louis Open Data (Cloud-Native Mirror)

{N_COLLECTIONS} collections mirrored from the [City of St. Louis open data
portal](https://www.stlouis-mo.gov/data/) as {FORMATS}. Everything is
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
- `parcels.WARD` = `wards.DISTRICT`; spatial joins work for everything else

## Read this first

- All geometry is WGS84 lon/lat (EPSG:4326).
- `csb-311-requests` has 18k rows with NULL geometry — table counts ≠ map counts.
- Access-style booleans appear as 0/-1 (e.g. `parcels.VacantLot`: -1 = vacant).
- No explicit data license is published by the city; each collection's
  `rel: license` link points at its portal page.
- The 10 `overture-*` collections are NOT city data: they are St. Louis
  bbox extracts of Overture Maps Foundation global datasets (keyword
  `overture`), included to show the catalog blending in outside data. Their
  PMTiles are Overture's own global theme tiles, not files in this catalog
  (except `overture-addresses`, tiled locally — the global addresses
  tileset has no St. Louis coverage).
- The catalog is a mirror, not an official city service. `updated` on each
  object is the sync time.
"""


def group_agents(group: str) -> str:
    from sources import GROUPS, GROUP_TITLES
    lines = [f"# AGENTS.md — {GROUP_TITLES[group]}", "",
             f"Department sub-catalog with {len(GROUPS[group])} collections. "
             "Access pattern for each:", "", "```sql",
             "INSTALL httpfs; LOAD httpfs;  -- DuckDB"]
    for cid in GROUPS[group]:
        lines.append(f"-- {SOURCES[cid]['title']}")
        lines.append(f"SELECT * FROM '{BASE}/{group}/{cid}/{cid}.parquet' LIMIT 5;")
    lines += ["```", "",
              "Each collection has its own AGENTS.md with fields, quirks, "
              "and joins. Root catalog: "
              f"`{BASE}/catalog.json`.", ""]
    return "\n".join(lines)


def main() -> None:
    from sources import GROUPS
    (CATALOG / "AGENTS.md").write_text(ROOT_AGENTS)
    print("✓ catalog AGENTS.md")
    for group in GROUPS:
        if (CATALOG / group / "catalog.json").exists():
            (CATALOG / group / "AGENTS.md").write_text(group_agents(group))
    print("✓ group AGENTS.md x13")
    for coll_id in SOURCES:
        d = CATALOG / coll_rel(coll_id)
        if not (d / "collection.json").exists():
            continue
        (d / "AGENTS.md").write_text(collection_agents(coll_id))
        print(f"✓ {coll_id}")


if __name__ == "__main__":
    main()
