# AGENTS.md — Law, Safety, and Justice

Department sub-catalog with 4 collections. Access pattern for each:

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
-- Police District Boundaries
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/law-safety-and-justice/police-districts/police-districts.parquet' LIMIT 5;
-- Crime (NIBRS)
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/law-safety-and-justice/crime/crime.parquet' LIMIT 5;
-- Siren Locations
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/law-safety-and-justice/siren-locations/siren-locations.parquet' LIMIT 5;
-- May 2025 Tornado Damage
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/law-safety-and-justice/tornado-damage-2025/tornado-damage-2025.parquet' LIMIT 5;
```

Each collection has its own AGENTS.md with fields, quirks, and joins. Root catalog: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/catalog.json`.
