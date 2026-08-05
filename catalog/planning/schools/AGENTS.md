# AGENTS.md — City Public Schools

City of St. Louis public school information including school name, school address, grades, and ages.

133 rows; geometry: Point (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/planning/schools/schools.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/planning/schools/schools.pmtiles` (layer `schools`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/planning/schools/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/planning/schools/) — rendered README and file listing
- [Source dataset](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=125) on the City of St. Louis open data portal

## Provenance

Mirror of [City Public Schools](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=125) from the City of St. Louis; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/Schools/FeatureServer. No explicit license is published — see the source page. Synced 2026-08-05T19:58:51+00:00.
