# AGENTS.md — City Boundary

St. Louis City limits

1 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/city-boundary/city-boundary.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/city-boundary/city-boundary.pmtiles` (layer `city-boundary`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Quirks

One polygon. St. Louis is an independent city — inside no county since 1876.

## Provenance

Mirror of [City Boundary](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=67) from the City of St. Louis open data portal; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/STLOUIS/BOUNDARIES/MapServer. No explicit license is published — see the portal page. Synced 2026-08-05T17:00:27+00:00.
