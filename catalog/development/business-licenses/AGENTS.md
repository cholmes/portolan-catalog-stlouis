# AGENTS.md — Business Licenses

Business licenses as of October 2025, from SLDC.

6,239 rows; geometry: Point (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/development/business-licenses/business-licenses.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/development/business-licenses/business-licenses.pmtiles` (layer `business-licenses`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Provenance

Mirror of [Business Licenses](https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Business_Licenses_as_of_October_2025/FeatureServer) from the City of St. Louis open data portal; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Business_Licenses_as_of_October_2025/FeatureServer. No explicit license is published — see the portal page. Synced 2026-08-05T19:58:51+00:00.
