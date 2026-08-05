# AGENTS.md — Floodplain

Floodplain areas for the City of St. Louis, from the city's Floodplain map service.

329 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/citywide/floodplain/floodplain.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/citywide/floodplain/floodplain.pmtiles` (layer `floodplain`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Provenance

Mirror of [Floodplain](https://maps8.stlouis-mo.gov/arcgis/rest/services/STLOUIS/Floodplain/MapServer) from the City of St. Louis open data portal; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/STLOUIS/Floodplain/MapServer. No explicit license is published — see the portal page. Synced 2026-08-05T19:58:51+00:00.
