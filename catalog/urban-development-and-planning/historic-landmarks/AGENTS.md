# AGENTS.md — Historic Landmarks

Historic sites and landmarks from the city's Historic Landmarks map service.

512 rows; geometry: Point (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/historic-landmarks/historic-landmarks.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/historic-landmarks/historic-landmarks.pmtiles` (layer `historic-landmarks`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/urban-development-and-planning/historic-landmarks/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/historic-landmarks/) — rendered README and file listing
- [Source dataset](https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/Historic_Landmarks/FeatureServer) on the City of St. Louis open data portal

## Provenance

Mirror of [Historic Landmarks](https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/Historic_Landmarks/FeatureServer) from the City of St. Louis; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/Historic_Landmarks/FeatureServer. No explicit license is published — see the source page. Synced 2026-08-14T11:21:05+00:00.
