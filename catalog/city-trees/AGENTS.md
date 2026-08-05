# AGENTS.md — City Trees (Planting Sites)

All mapped planting sites within the city for tree plantings managed by the Forestry Division. Street tree planting sites are re-used, while park tree sites tend not to be. This data contains vacant sites, as well.

134,588 rows; geometry: Point (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/city-trees/city-trees.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/city-trees/city-trees.pmtiles` (layer `city-trees`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `COMMON` — common name; the literal value 'Vacant' marks an empty planting site (30,935 of them)
- `DBH` — trunk diameter (inches) at breast height
- `CONDITION` — Excellent..Dead, Stump; N/A mostly = vacant sites
- `LOCATION_TYPE` — Easement (street trees), Park, Median

Full schema: `table:columns` in collection.json.

## Quirks

134,588 records = trees AND empty planting sites; filter COMMON <> 'Vacant' for actual trees.

## Joins

Address fields (STREET_NUM, STREET) join loosely to parcel situs addresses.

## Provenance

Mirror of [City Trees (Planting Sites)](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=121) from the City of St. Louis open data portal; source: https://maps9.stlouis-mo.gov/arcgis/rest/services/FORESTRY/FORESTRY_TREES/MapServer. No explicit license is published — see the portal page. Synced 2026-08-05T17:48:01+00:00.
