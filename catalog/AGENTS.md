# AGENTS.md — City of St. Louis Open Data (Cloud-Native Mirror)

Twenty collections mirrored from https://www.stlouis-mo.gov/data/ as
GeoParquet (+ PMTiles for the 19 geospatial ones). Everything is
range-readable over HTTPS — no download needed.

## Access pattern

```sql
INSTALL httpfs; LOAD httpfs; INSTALL spatial; LOAD spatial;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/parcels/parcels.parquet' LIMIT 5;
```

Catalog root: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/catalog.json`. Every collection has its own
AGENTS.md with fields, quirks, and joins.

## The join graph

`parcels` is the hub (134,362 rows):

- `property-sales.AsrParcelId` = `parcels.ParcelId`
- `lra-property.Handle` / `tax-abated-parcels.HANDLE` = `parcels.HANDLE`
- `parcels.NBRHD` = `neighborhoods.NHD_NUM` = `csb-311-requests.NEIGHBORHOOD`
- `parcels.WARD` = `wards.district`; spatial joins work for everything else

## Read this first

- All geometry is WGS84 lon/lat (EPSG:4326).
- `csb-311-requests` has 18k rows with NULL geometry — table counts ≠ map counts.
- Access-style booleans appear as 0/-1 (e.g. `parcels.VacantLot`: -1 = vacant).
- No explicit data license is published by the city; each collection's
  `rel: license` link points at its portal page.
- The catalog is a mirror, not an official city service. `updated` on each
  object is the sync time.
