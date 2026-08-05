# AGENTS.md — Police District Boundaries

GIS data for police district boundaries

6 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/police-districts/police-districts.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/police-districts/police-districts.pmtiles` (layer `police-districts`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `DISTNO` — district number 1-6 (string)

Full schema: `table:columns` in collection.json.

## Provenance

Mirror of [Police District Boundaries](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=83) from the City of St. Louis open data portal; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/STLOUIS/POLICE_DISTRICT/FeatureServer. No explicit license is published — see the portal page. Synced 2026-08-05T04:46:13+00:00.
