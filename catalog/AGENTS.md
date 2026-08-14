# AGENTS.md — City of St. Louis Open Data (Cloud-Native Mirror)

61 collections mirrored from the [City of St. Louis open data
portal](https://www.stlouis-mo.gov/data/) as GeoParquet, 52 of them also as PMTiles. Everything is
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
- `parcels.WARD` = `wards.DISTRICT`; spatial joins work for everything else

## Read this first

- All geometry is WGS84 lon/lat (EPSG:4326).
- `csb-311-requests` has 18k rows with NULL geometry — table counts ≠ map counts.
- Access-style booleans appear as 0/-1 (e.g. `parcels.VacantLot`: -1 = vacant).
- No explicit data license is published by the city; each collection's
  `rel: license` link points at its portal page.
- The 10 `overture-*` collections are NOT city data: they are St. Louis
  bbox extracts of Overture Maps Foundation global datasets (keyword
  `overture`), included to show the catalog blending in outside data. Their
  PMTiles are Overture's own global theme tiles, not files in this catalog
  (except `overture-addresses`, tiled locally — the global addresses
  tileset has no St. Louis coverage).
- The catalog is a mirror, not an official city service. `updated` on each
  object is the sync time.
