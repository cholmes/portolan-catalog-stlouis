# AGENTS.md — Tax Sales

Tax sale parcels from SLDC.

2,200 rows; geometry: MultiPolygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/development/tax-sales/tax-sales.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/development/tax-sales/tax-sales.pmtiles` (layer `tax-sales`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Provenance

Mirror of [Tax Sales](https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Tax_Sales/FeatureServer) from the City of St. Louis open data portal; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Tax_Sales/FeatureServer. No explicit license is published — see the portal page. Synced 2026-08-05T19:58:51+00:00.
