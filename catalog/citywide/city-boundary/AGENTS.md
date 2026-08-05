# AGENTS.md — City Boundary

St. Louis City limits

1 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/citywide/city-boundary/city-boundary.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/citywide/city-boundary/city-boundary.pmtiles` (layer `city-boundary`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Quirks

One polygon. St. Louis is an independent city — inside no county since 1876.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/citywide/city-boundary/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/citywide/city-boundary/) — rendered README and file listing
- [Source dataset](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=67) on the City of St. Louis open data portal

## Provenance

Mirror of [City Boundary](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=67) from the City of St. Louis; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/STLOUIS/BOUNDARIES/MapServer. No explicit license is published — see the source page. Synced 2026-08-05T19:58:51+00:00.
