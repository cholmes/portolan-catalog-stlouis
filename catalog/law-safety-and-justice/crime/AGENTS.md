# AGENTS.md — Crime (NIBRS)

Downloadable NIBRS crime data published by the St. Louis Metropolitan Police Department.

367,449 rows; geometry: Point (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/law-safety-and-justice/crime/crime.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/law-safety-and-justice/crime/crime.pmtiles` (layer `crime`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/law-safety-and-justice/crime/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/law-safety-and-justice/crime/) — rendered README and file listing
- [Source dataset](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=69) on the City of St. Louis open data portal

## Provenance

Mirror of [Crime (NIBRS)](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=69) from the City of St. Louis; source: https://www.slmpd.org/crime_stats.shtml. No explicit license is published — see the source page. Synced 2026-08-14T12:21:16+00:00.
