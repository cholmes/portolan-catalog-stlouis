# AGENTS.md — Health

Department sub-catalog with 2 collections. Access pattern for each:

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
-- Animal Bites
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/health/animal-bites/animal-bites.parquet' LIMIT 5;
-- Lead Service Line Inventory
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/health/lead-service-lines/lead-service-lines.parquet' LIMIT 5;
```

Each collection has its own AGENTS.md with fields, quirks, and joins. Root catalog: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/catalog.json`.
