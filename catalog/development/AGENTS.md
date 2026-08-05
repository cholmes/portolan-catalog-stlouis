# AGENTS.md — Development (SLDC & CDA)

Department sub-catalog with 11 collections. Access pattern for each:

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
-- Tax Increment Financing (TIF) Districts
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/development/tif-districts/tif-districts.parquet' LIMIT 5;
-- Qualified Opportunity Zones
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/development/opportunity-zones/opportunity-zones.parquet' LIMIT 5;
-- LRA Property
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/development/lra-property/lra-property.parquet' LIMIT 5;
-- Community Improvement Districts (CIDs)
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/development/community-improvement-districts/community-improvement-districts.parquet' LIMIT 5;
-- Special Business Districts (SBDs)
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/development/special-business-districts/special-business-districts.parquet' LIMIT 5;
-- Tax-abated Parcels
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/development/tax-abated-parcels/tax-abated-parcels.parquet' LIMIT 5;
-- Port Authority District
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/development/port-authority-district/port-authority-district.parquet' LIMIT 5;
-- Parcel Vacancy Composite
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/development/vacancy-composite/vacancy-composite.parquet' LIMIT 5;
-- Business Licenses
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/development/business-licenses/business-licenses.parquet' LIMIT 5;
-- Tax Sales
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/development/tax-sales/tax-sales.parquet' LIMIT 5;
-- 2024 Market Value Analysis
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/development/market-value-analysis/market-value-analysis.parquet' LIMIT 5;
```

Each collection has its own AGENTS.md with fields, quirks, and joins. Root catalog: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/catalog.json`.
