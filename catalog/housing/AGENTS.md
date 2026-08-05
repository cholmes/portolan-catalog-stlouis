# AGENTS.md — Housing

Department sub-catalog with 7 collections. Access pattern for each:

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
-- LRA Property
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/housing/lra-property/lra-property.parquet' LIMIT 5;
-- Property Sales
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/housing/property-sales/property-sales.parquet' LIMIT 5;
-- 2024 Market Value Analysis
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/housing/market-value-analysis/market-value-analysis.parquet' LIMIT 5;
-- Electrical Permits
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/housing/electrical-permits/electrical-permits.parquet' LIMIT 5;
-- Mechanical Permits
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/housing/mechanical-permits/mechanical-permits.parquet' LIMIT 5;
-- Plumbing Permits
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/housing/plumbing-permits/plumbing-permits.parquet' LIMIT 5;
-- Occupancy Permits
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/housing/occupancy-permits/occupancy-permits.parquet' LIMIT 5;
```

Each collection has its own AGENTS.md with fields, quirks, and joins. Root catalog: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/catalog.json`.
