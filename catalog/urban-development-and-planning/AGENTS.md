# AGENTS.md — Urban Development and Planning

Department sub-catalog with 14 collections. Access pattern for each:

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
-- Parcels
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/parcels/parcels.parquet' LIMIT 5;
-- Parcels (Historical, 1997-2020)
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/parcels-history/parcels-history.parquet' LIMIT 5;
-- City Blocks
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/city-blocks/city-blocks.parquet' LIMIT 5;
-- Zoning
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/zoning/zoning.parquet' LIMIT 5;
-- Strategic Land Use Plan
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/land-use/land-use.parquet' LIMIT 5;
-- Neighborhood Boundaries
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/neighborhoods/neighborhoods.parquet' LIMIT 5;
-- Historic Districts
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/historic-districts/historic-districts.parquet' LIMIT 5;
-- Historic Landmarks
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/historic-landmarks/historic-landmarks.parquet' LIMIT 5;
-- Port Authority District
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/port-authority-district/port-authority-district.parquet' LIMIT 5;
-- Parcel Vacancy Composite
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/vacancy-composite/vacancy-composite.parquet' LIMIT 5;
-- City Boundary
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/city-boundary/city-boundary.parquet' LIMIT 5;
-- Overture Buildings
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/overture-buildings/overture-buildings.parquet' LIMIT 5;
-- Overture Addresses
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/overture-addresses/overture-addresses.parquet' LIMIT 5;
-- Overture Land Use
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/overture-land-use/overture-land-use.parquet' LIMIT 5;
```

Each collection has its own AGENTS.md with fields, quirks, and joins. Root catalog: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/catalog.json`.
