# AGENTS.md — Parcels (Historical, 1997-2020)

Current and historic parcel data

3,106,506 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/parcels-history/parcels-history.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/parcels-history/parcels-history.pmtiles` (layer `parcels-history`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/urban-development-and-planning/parcels-history/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/parcels-history/) — rendered README and file listing
- [Source dataset](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=82) on the City of St. Louis open data portal

## Provenance

Mirror of [Parcels (Historical, 1997-2020)](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=82) from the City of St. Louis; source: https://www.stlouis-mo.gov/data/upload/data-files/stl_parcels_1997-2000.zip. No explicit license is published — see the source page. Synced 2026-08-14T11:21:05+00:00.
