# AGENTS.md — Historic Districts

Data on St. Louis certified local historic districts

109 rows; geometry: MultiPolygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/historic-districts/historic-districts.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/historic-districts/historic-districts.pmtiles` (layer `historic-districts`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `DISNAME` — district name
- `DIS_TYPE` — National (85) / Local / Certified Local / Landmark

Full schema: `table:columns` in collection.json.

## Provenance

Mirror of [Historic Districts](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=73) from the City of St. Louis open data portal; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/Historic_Districts/MapServer. No explicit license is published — see the portal page. Synced 2026-08-05T17:48:01+00:00.
