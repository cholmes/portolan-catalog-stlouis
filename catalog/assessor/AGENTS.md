# AGENTS.md — Assessor's Office

Department sub-catalog with 5 collections. Access pattern for each:

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
-- Parcels
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/assessor/parcels/parcels.parquet' LIMIT 5;
-- Parcels (Historical, 1997-2020)
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/assessor/parcels-history/parcels-history.parquet' LIMIT 5;
-- City Blocks
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/assessor/city-blocks/city-blocks.parquet' LIMIT 5;
-- Property Sales
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/assessor/property-sales/property-sales.parquet' LIMIT 5;
-- Property Taxes
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/assessor/property-taxes/property-taxes.parquet' LIMIT 5;
```

Each collection has its own AGENTS.md with fields, quirks, and joins. Root catalog: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/catalog.json`.
