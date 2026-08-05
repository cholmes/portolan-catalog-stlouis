# AGENTS.md — Ward Boundaries (2010)

Boundaries of City of St. Louis wards

28 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/planning/wards-2010/wards-2010.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/planning/wards-2010/wards-2010.pmtiles` (layer `wards-2010`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Quirks

The 28-ward map in force 2011-2022 — the geography that WARD10 columns elsewhere (city-blocks, parcels) reference.

## Provenance

Mirror of [Ward Boundaries (2010)](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=131) from the City of St. Louis open data portal; source: https://static.stlouis-mo.gov/open-data/planning/wards/wards_2010.zip. No explicit license is published — see the portal page. Synced 2026-08-05T19:58:51+00:00.
