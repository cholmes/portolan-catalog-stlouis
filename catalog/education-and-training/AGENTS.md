# AGENTS.md — Education and Training

Department sub-catalog with 1 collections. Access pattern for each:

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
-- City Public Schools
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/education-and-training/schools/schools.parquet' LIMIT 5;
```

Each collection has its own AGENTS.md with fields, quirks, and joins. Root catalog: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/catalog.json`.
