# AGENTS.md — Tax Sales

Tax sale parcels from SLDC.

2,200 rows; geometry: MultiPolygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/business-and-industry/tax-sales/tax-sales.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/business-and-industry/tax-sales/tax-sales.pmtiles` (layer `tax-sales`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/business-and-industry/tax-sales/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/business-and-industry/tax-sales/) — rendered README and file listing
- [Source dataset](https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Tax_Sales/FeatureServer) on the City of St. Louis open data portal

## Provenance

Mirror of [Tax Sales](https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Tax_Sales/FeatureServer) from the City of St. Louis; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Tax_Sales/FeatureServer. No explicit license is published — see the source page. Synced 2026-08-05T19:58:51+00:00.
