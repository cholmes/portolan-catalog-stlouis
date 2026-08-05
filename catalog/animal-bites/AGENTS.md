# AGENTS.md — Animal Bites

Animal bite reports made to the City of Saint Louis Department of Health and its Animal Care and Control section.

6,359 rows; geometry: Point (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/animal-bites/animal-bites.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/animal-bites/animal-bites.pmtiles` (layer `animal-bites`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Provenance

Mirror of [Animal Bites](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=130) from the City of St. Louis open data portal; source: https://static.stlouis-mo.gov/open-data/HEALTH/ANIMAL-CONTROL/ANIMAL_BITES.csv. No explicit license is published — see the portal page. Synced 2026-08-05T17:48:01+00:00.
