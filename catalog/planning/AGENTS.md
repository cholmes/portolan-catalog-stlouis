# AGENTS.md — Planning and Urban Design

Department sub-catalog with 9 collections. Access pattern for each:

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
-- Neighborhood Boundaries
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/planning/neighborhoods/neighborhoods.parquet' LIMIT 5;
-- Ward Boundaries (2020)
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/planning/wards/wards.parquet' LIMIT 5;
-- Ward Boundaries (2010)
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/planning/wards-2010/wards-2010.parquet' LIMIT 5;
-- Zoning
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/planning/zoning/zoning.parquet' LIMIT 5;
-- Strategic Land Use Plan
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/planning/land-use/land-use.parquet' LIMIT 5;
-- Historic Districts
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/planning/historic-districts/historic-districts.parquet' LIMIT 5;
-- Historic Landmarks
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/planning/historic-landmarks/historic-landmarks.parquet' LIMIT 5;
-- City Public Schools
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/planning/schools/schools.parquet' LIMIT 5;
-- Bike Infrastructure
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/planning/bike-infrastructure/bike-infrastructure.parquet' LIMIT 5;
```

Each collection has its own AGENTS.md with fields, quirks, and joins. Root catalog: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/catalog.json`.
