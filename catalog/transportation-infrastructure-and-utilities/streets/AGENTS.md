# AGENTS.md — City Streets

City street GIS data

19,858 rows; geometry: MultiLineString (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/transportation-infrastructure-and-utilities/streets/streets.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/transportation-infrastructure-and-utilities/streets/streets.pmtiles` (layer `streets`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `Street_Name_Full` — full name
- `Class` — source class code (A31/A41/A6x/A73, no published decode)

Full schema: `table:columns` in collection.json.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/transportation-infrastructure-and-utilities/streets/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/transportation-infrastructure-and-utilities/streets/) — rendered README and file listing
- [Source dataset](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=68) on the City of St. Louis open data portal

## Provenance

Mirror of [City Streets](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=68) from the City of St. Louis; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Streets/FeatureServer. No explicit license is published — see the source page. Synced 2026-08-14T12:21:16+00:00.
