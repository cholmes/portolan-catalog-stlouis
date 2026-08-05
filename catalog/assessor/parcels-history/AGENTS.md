# AGENTS.md — Parcels (Historical, 1997-2020)

Current and historic parcel data

3,106,506 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/assessor/parcels-history/parcels-history.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/assessor/parcels-history/parcels-history.pmtiles` (layer `parcels-history`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Provenance

Mirror of [Parcels (Historical, 1997-2020)](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=82) from the City of St. Louis open data portal; source: https://www.stlouis-mo.gov/data/upload/data-files/stl_parcels_1997-2000.zip. No explicit license is published — see the portal page. Synced 2026-08-05T19:58:51+00:00.
