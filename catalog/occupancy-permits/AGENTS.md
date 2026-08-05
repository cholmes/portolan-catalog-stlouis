# AGENTS.md — Occupancy Permits

Commercial, industrial, and occupancy building permits in the City of St. Louis

76,393 rows; tabular (no geometry).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/occupancy-permits/occupancy-permits.parquet' LIMIT 5;
```

Full schema: `table:columns` in collection.json.

## Reproduce the geometry join

This collection is published as plain (non-geo) Parquet, exactly as the city publishes it; its map layer (`occupancy-permits.pmtiles`) is materialized by joining to `parcels`. To build your own GeoParquet:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
COPY (
  SELECT t.HANDLE, t.APPTYPE, t.APPDESCRIPTION, TRY_CAST(substr(t.ISSUEDATE, 1, 4) AS INT) AS PERMIT_YEAR, TRY_CAST(t.ESTPROJECTCOST AS DOUBLE) AS ESTPROJECTCOST, p.geometry
  FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/occupancy-permits/occupancy-permits.parquet' t
  JOIN 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/parcels/parcels.parquet' p
    ON t.HANDLE = p.HANDLE
) TO 'occupancy-permits-geo.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);
```

Then convert as needed:

```bash
gpio convert geoparquet occupancy-permits-geo.parquet occupancy-permits-geo-optimized.parquet
gpio convert geopackage occupancy-permits-geo.parquet occupancy-permits.gpkg
gpio convert shapefile occupancy-permits-geo.parquet occupancy-permits.shp
```

## Provenance

Mirror of [Occupancy Permits](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=6) from the City of St. Louis open data portal; source: https://www.stlouis-mo.gov/data/upload/data-files/occupancy-permits.zip. No explicit license is published — see the portal page. Synced 2026-08-05T17:48:01+00:00.
