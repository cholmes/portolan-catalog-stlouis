# AGENTS.md — Building Division

Department sub-catalog with 4 collections. Access pattern for each:

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
-- Electrical Permits
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/building/electrical-permits/electrical-permits.parquet' LIMIT 5;
-- Mechanical Permits
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/building/mechanical-permits/mechanical-permits.parquet' LIMIT 5;
-- Plumbing Permits
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/building/plumbing-permits/plumbing-permits.parquet' LIMIT 5;
-- Occupancy Permits
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/building/occupancy-permits/occupancy-permits.parquet' LIMIT 5;
```

Each collection has its own AGENTS.md with fields, quirks, and joins. Root catalog: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/catalog.json`.
