# AGENTS.md — Transportation, Infrastructure, and Utilities

Department sub-catalog with 7 collections. Access pattern for each:

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
-- City Streets
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/transportation-infrastructure-and-utilities/streets/streets.parquet' LIMIT 5;
-- Street Permits
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/transportation-infrastructure-and-utilities/street-permits/street-permits.parquet' LIMIT 5;
-- Parking Meters
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/transportation-infrastructure-and-utilities/parking-meters/parking-meters.parquet' LIMIT 5;
-- Street Sweeping Schedule
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/transportation-infrastructure-and-utilities/street-sweeping/street-sweeping.parquet' LIMIT 5;
-- Bike Infrastructure
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/transportation-infrastructure-and-utilities/bike-infrastructure/bike-infrastructure.parquet' LIMIT 5;
-- Overture Transportation
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/transportation-infrastructure-and-utilities/overture-transportation/overture-transportation.parquet' LIMIT 5;
-- Overture Infrastructure
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/transportation-infrastructure-and-utilities/overture-infrastructure/overture-infrastructure.parquet' LIMIT 5;
```

Each collection has its own AGENTS.md with fields, quirks, and joins. Root catalog: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/catalog.json`.
