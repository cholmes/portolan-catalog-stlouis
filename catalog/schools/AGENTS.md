# AGENTS.md — City Public Schools

City of St. Louis public school information including school name, school address, grades, and ages.

133 rows; geometry: Point (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/schools/schools.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/schools/schools.pmtiles` (layer `schools`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Provenance

Mirror of [City Public Schools](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=125) from the City of St. Louis open data portal; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/Schools/FeatureServer. No explicit license is published — see the portal page. Synced 2026-08-05T17:48:01+00:00.
