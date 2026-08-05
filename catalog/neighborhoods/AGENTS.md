# AGENTS.md — Neighborhood Boundaries

ESRI shapefiles for city neighborhoods

88 rows; geometry: MultiPolygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/neighborhoods/neighborhoods.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/neighborhoods/neighborhoods.pmtiles` (layer `neighborhoods`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `NHD_NUM` — official number
- `NHD_NAME` — official name

Full schema: `table:columns` in collection.json.

## Joins

parcels.NBRHD, csb-311-requests.NEIGHBORHOOD, and city-blocks.NBRHD all carry NHD_NUM.

## Provenance

Mirror of [Neighborhood Boundaries](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=85) from the City of St. Louis open data portal; source: https://maps6.stlouis-mo.gov/arcgis/rest/services/PublicDataStore/NEIGHBORHOOD_BOUNDARIES/FeatureServer. No explicit license is published — see the portal page. Synced 2026-08-05T17:00:27+00:00.
