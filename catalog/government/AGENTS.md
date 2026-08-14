# AGENTS.md — Government

Department sub-catalog with 9 collections. Access pattern for each:

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
-- Ward Boundaries (2020)
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/government/wards/wards.parquet' LIMIT 5;
-- Ward Boundaries (2010)
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/government/wards-2010/wards-2010.parquet' LIMIT 5;
-- Election Wards & Precincts
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/government/election-precincts/election-precincts.parquet' LIMIT 5;
-- Polling Centers
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/government/polling-places/polling-places.parquet' LIMIT 5;
-- November 2024 Election Results by Precinct
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/government/election-results-nov-2024/election-results-nov-2024.parquet' LIMIT 5;
-- CSB Service Requests (311)
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/government/csb-311-requests/csb-311-requests.parquet' LIMIT 5;
-- ZIP Codes
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/government/zip-codes/zip-codes.parquet' LIMIT 5;
-- Property Taxes
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/government/property-taxes/property-taxes.parquet' LIMIT 5;
-- Overture Divisions
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/government/overture-divisions/overture-divisions.parquet' LIMIT 5;
```

Each collection has its own AGENTS.md with fields, quirks, and joins. Root catalog: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/catalog.json`.
