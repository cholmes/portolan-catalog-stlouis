# AGENTS.md — Strategic Land Use Plan

Strategic land use (SLUP),parcel, and zoning data

11,567 rows; geometry: MultiPolygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/land-use/land-use.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/land-use/land-use.pmtiles` (layer `land-use`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Provenance

Mirror of [Strategic Land Use Plan](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=78) from the City of St. Louis open data portal; source: https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/Strategic_Land_Use_Plan/FeatureServer. No explicit license is published — see the portal page. Synced 2026-08-05T17:00:27+00:00.
