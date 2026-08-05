# AGENTS.md — Water Division

Department sub-catalog with 1 collections. Access pattern for each:

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
-- Lead Service Line Inventory
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/water/lead-service-lines/lead-service-lines.parquet' LIMIT 5;
```

Each collection has its own AGENTS.md with fields, quirks, and joins. Root catalog: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/catalog.json`.
