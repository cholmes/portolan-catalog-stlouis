# AGENTS.md — Forestry

Department sub-catalog with 2 collections. Access pattern for each:

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
-- City Trees (Planting Sites)
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/forestry/city-trees/city-trees.parquet' LIMIT 5;
-- Forest Park Trees
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/forestry/forest-park-trees/forest-park-trees.parquet' LIMIT 5;
```

Each collection has its own AGENTS.md with fields, quirks, and joins. Root catalog: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/catalog.json`.
