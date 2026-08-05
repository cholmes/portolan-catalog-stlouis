# AGENTS.md — Port Authority District

This feature represents the District boundary for the St. Louis Port Authority. It was created from Section One text in Ordinance 71179 from May 15, 2020.

1 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/port-authority-district/port-authority-district.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/port-authority-district/port-authority-district.pmtiles` (layer `port-authority-district`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Provenance

Mirror of [Port Authority District](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=55) from the City of St. Louis open data portal; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Port_Authority_District_Boundary/FeatureServer. No explicit license is published — see the portal page. Synced 2026-08-05T17:00:27+00:00.
