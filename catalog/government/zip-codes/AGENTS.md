# AGENTS.md — ZIP Codes

ZIP code areas from the city's boundaries map service.

30 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/government/zip-codes/zip-codes.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/government/zip-codes/zip-codes.pmtiles` (layer `zip-codes`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/government/zip-codes/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/government/zip-codes/) — rendered README and file listing
- [Source dataset](https://maps8.stlouis-mo.gov/arcgis/rest/services/STLOUIS/BOUNDARIES/MapServer) on the City of St. Louis open data portal

## Provenance

Mirror of [ZIP Codes](https://maps8.stlouis-mo.gov/arcgis/rest/services/STLOUIS/BOUNDARIES/MapServer) from the City of St. Louis; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/STLOUIS/BOUNDARIES/MapServer. No explicit license is published — see the source page. Synced 2026-08-05T19:58:51+00:00.
