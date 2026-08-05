# AGENTS.md — Street Sweeping Schedule

Street sweeping area schedules from the Streets Division.

84 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/streets/street-sweeping/street-sweeping.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/streets/street-sweeping/street-sweeping.pmtiles` (layer `street-sweeping`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Provenance

Mirror of [Street Sweeping Schedule](https://maps8.stlouis-mo.gov/arcgis/rest/services/STREETS/Street_Sweeping/MapServer) from the City of St. Louis open data portal; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/STREETS/Street_Sweeping/MapServer. No explicit license is published — see the portal page. Synced 2026-08-05T19:58:51+00:00.
