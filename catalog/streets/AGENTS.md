# AGENTS.md — Streets

Department sub-catalog with 4 collections. Access pattern for each:

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
-- City Streets
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/streets/streets/streets.parquet' LIMIT 5;
-- Street Permits
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/streets/street-permits/street-permits.parquet' LIMIT 5;
-- Parking Meters
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/streets/parking-meters/parking-meters.parquet' LIMIT 5;
-- Street Sweeping Schedule
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/streets/street-sweeping/street-sweeping.parquet' LIMIT 5;
```

Each collection has its own AGENTS.md with fields, quirks, and joins. Root catalog: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/catalog.json`.
