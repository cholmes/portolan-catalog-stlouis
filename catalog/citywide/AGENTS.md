# AGENTS.md — Citywide Reference

Department sub-catalog with 3 collections. Access pattern for each:

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
-- City Boundary
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/citywide/city-boundary/city-boundary.parquet' LIMIT 5;
-- Floodplain
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/citywide/floodplain/floodplain.parquet' LIMIT 5;
-- ZIP Codes
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/citywide/zip-codes/zip-codes.parquet' LIMIT 5;
```

Each collection has its own AGENTS.md with fields, quirks, and joins. Root catalog: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/catalog.json`.
