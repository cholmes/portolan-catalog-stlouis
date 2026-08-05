# AGENTS.md — Forest Park Trees

Forest Park Trees data

15,450 rows; geometry: Point (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/environment/forest-park-trees/forest-park-trees.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/environment/forest-park-trees/forest-park-trees.pmtiles` (layer `forest-park-trees`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/environment/forest-park-trees/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/environment/forest-park-trees/) — rendered README and file listing
- [Source dataset](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=123) on the City of St. Louis open data portal

## Provenance

Mirror of [Forest Park Trees](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=123) from the City of St. Louis; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/FORESTRY/FOREST_PARK_TREES/FeatureServer. No explicit license is published — see the source page. Synced 2026-08-05T19:58:51+00:00.
