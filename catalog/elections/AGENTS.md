# AGENTS.md — Elections

Department sub-catalog with 3 collections. Access pattern for each:

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
-- Election Wards & Precincts
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/elections/election-precincts/election-precincts.parquet' LIMIT 5;
-- Polling Centers
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/elections/polling-places/polling-places.parquet' LIMIT 5;
-- November 2024 Election Results by Precinct
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/elections/election-results-nov-2024/election-results-nov-2024.parquet' LIMIT 5;
```

Each collection has its own AGENTS.md with fields, quirks, and joins. Root catalog: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/catalog.json`.
