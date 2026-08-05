# AGENTS.md — Police District Boundaries

GIS data for police district boundaries

6 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/law-safety-and-justice/police-districts/police-districts.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/law-safety-and-justice/police-districts/police-districts.pmtiles` (layer `police-districts`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `DISTNO` — district number 1-6 (string)

Full schema: `table:columns` in collection.json.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/law-safety-and-justice/police-districts/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/law-safety-and-justice/police-districts/) — rendered README and file listing
- [Source dataset](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=83) on the City of St. Louis open data portal

## Provenance

Mirror of [Police District Boundaries](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=83) from the City of St. Louis; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/STLOUIS/POLICE_DISTRICT/FeatureServer. No explicit license is published — see the source page. Synced 2026-08-05T19:58:51+00:00.
