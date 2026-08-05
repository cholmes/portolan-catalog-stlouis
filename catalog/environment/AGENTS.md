# AGENTS.md — Environment

Department sub-catalog with 4 collections. Access pattern for each:

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
-- Floodplain
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/environment/floodplain/floodplain.parquet' LIMIT 5;
-- Flood Controls
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/environment/flood-controls/flood-controls.parquet' LIMIT 5;
-- City Trees (Planting Sites)
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/environment/city-trees/city-trees.parquet' LIMIT 5;
-- Forest Park Trees
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/environment/forest-park-trees/forest-park-trees.parquet' LIMIT 5;
```

Each collection has its own AGENTS.md with fields, quirks, and joins. Root catalog: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/catalog.json`.
