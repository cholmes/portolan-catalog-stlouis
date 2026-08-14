# AGENTS.md — Ward Boundaries (2020)

Boundaries of City of St. Louis wards

14 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/government/wards/wards.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/government/wards/wards.pmtiles` (layer `wards`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `DISTRICT` — ward number as string
- `NAME` — ward name
- `POPULATION` — 2020 census population, with race columns

Full schema: `table:columns` in collection.json.

## Quirks

The 14 wards from 2020 redistricting (effective 2023); older datasets reference the previous 28 wards (WARD10 columns elsewhere).

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/government/wards/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/government/wards/) — rendered README and file listing
- [Source dataset](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=131) on the City of St. Louis open data portal

## Provenance

Mirror of [Ward Boundaries (2020)](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=131) from the City of St. Louis; source: https://static.stlouis-mo.gov/open-data/planning/wards/wards_2020.zip. No explicit license is published — see the source page. Synced 2026-08-14T11:21:05+00:00.
