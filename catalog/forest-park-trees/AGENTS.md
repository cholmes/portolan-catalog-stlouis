# AGENTS.md — Forest Park Trees

Forest Park Trees data

15,450 rows; geometry: Point (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/forest-park-trees/forest-park-trees.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/forest-park-trees/forest-park-trees.pmtiles` (layer `forest-park-trees`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Provenance

Mirror of [Forest Park Trees](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=123) from the City of St. Louis open data portal; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/FORESTRY/FOREST_PARK_TREES/FeatureServer. No explicit license is published — see the portal page. Synced 2026-08-05T17:00:27+00:00.
