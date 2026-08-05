# AGENTS.md — Historic Districts

Data on St. Louis certified local historic districts

109 rows; geometry: MultiPolygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/planning/historic-districts/historic-districts.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/planning/historic-districts/historic-districts.pmtiles` (layer `historic-districts`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `DISNAME` — district name
- `DIS_TYPE` — National (85) / Local / Certified Local / Landmark

Full schema: `table:columns` in collection.json.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/planning/historic-districts/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/planning/historic-districts/) — rendered README and file listing
- [Source dataset](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=73) on the City of St. Louis open data portal

## Provenance

Mirror of [Historic Districts](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=73) from the City of St. Louis; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/Historic_Districts/MapServer. No explicit license is published — see the source page. Synced 2026-08-05T19:58:51+00:00.
