# AGENTS.md — Historic Landmarks

Historic sites and landmarks from the city's Historic Landmarks map service.

512 rows; geometry: Point (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/planning/historic-landmarks/historic-landmarks.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/planning/historic-landmarks/historic-landmarks.pmtiles` (layer `historic-landmarks`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Provenance

Mirror of [Historic Landmarks](https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/Historic_Landmarks/FeatureServer) from the City of St. Louis open data portal; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/Historic_Landmarks/FeatureServer. No explicit license is published — see the portal page. Synced 2026-08-05T19:58:51+00:00.
