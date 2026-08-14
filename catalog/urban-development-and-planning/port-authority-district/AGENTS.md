# AGENTS.md — Port Authority District

This feature represents the District boundary for the St. Louis Port Authority. It was created from Section One text in Ordinance 71179 from May 15, 2020.

1 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/port-authority-district/port-authority-district.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/port-authority-district/port-authority-district.pmtiles` (layer `port-authority-district`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/urban-development-and-planning/port-authority-district/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/port-authority-district/) — rendered README and file listing
- [Source dataset](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=55) on the City of St. Louis open data portal

## Provenance

Mirror of [Port Authority District](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=55) from the City of St. Louis; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Port_Authority_District_Boundary/FeatureServer. No explicit license is published — see the source page. Synced 2026-08-14T12:21:16+00:00.
