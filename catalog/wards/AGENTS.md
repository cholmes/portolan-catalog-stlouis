# AGENTS.md — Ward Boundaries (2020)

Boundaries of City of St. Louis wards

10 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/wards/wards.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/wards/wards.pmtiles` (layer `wards`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `district` — ward number as string
- `name` — ward name
- `population` — 2020 census population, with race columns

Full schema: `table:columns` in collection.json.

## Quirks

The 10 wards from 2020 redistricting (effective 2023); older datasets reference the previous 28 wards (WARD10 columns elsewhere).

## Provenance

Mirror of [Ward Boundaries (2020)](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=131) from the City of St. Louis open data portal; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/Hosted/City_of_St__Louis_Ward_Boundaries/FeatureServer. No explicit license is published — see the portal page. Synced 2026-08-05T01:13:22+00:00.
