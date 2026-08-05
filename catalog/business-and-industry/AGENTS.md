# AGENTS.md — Business and Industry

Department sub-catalog with 7 collections. Access pattern for each:

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
-- Tax Increment Financing (TIF) Districts
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/business-and-industry/tif-districts/tif-districts.parquet' LIMIT 5;
-- Qualified Opportunity Zones
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/business-and-industry/opportunity-zones/opportunity-zones.parquet' LIMIT 5;
-- Special Business Districts (SBDs)
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/business-and-industry/special-business-districts/special-business-districts.parquet' LIMIT 5;
-- Tax-abated Parcels
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/business-and-industry/tax-abated-parcels/tax-abated-parcels.parquet' LIMIT 5;
-- Business Licenses
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/business-and-industry/business-licenses/business-licenses.parquet' LIMIT 5;
-- Tax Sales
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/business-and-industry/tax-sales/tax-sales.parquet' LIMIT 5;
-- Community Improvement Districts (CIDs)
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/business-and-industry/community-improvement-districts/community-improvement-districts.parquet' LIMIT 5;
```

Each collection has its own AGENTS.md with fields, quirks, and joins. Root catalog: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/catalog.json`.
