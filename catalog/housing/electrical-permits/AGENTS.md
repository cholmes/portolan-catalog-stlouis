# AGENTS.md — Electrical Permits

Data on commercial, industrial, and residential electrical permits in the City of St. Louis

296,930 rows; tabular (no geometry).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/housing/electrical-permits/electrical-permits.parquet' LIMIT 5;
```

Full schema: `table:columns` in collection.json.

## Reproduce the geometry join

This collection is published as plain (non-geo) Parquet, exactly as the city publishes it; its map layer (`electrical-permits.pmtiles`) is materialized by joining to `parcels`. To build your own GeoParquet:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
COPY (
  SELECT t.HANDLE, t.APPTYPE, t.APPDESCRIPTION, TRY_CAST(substr(t.ISSUEDATE, 1, 4) AS INT) AS PERMIT_YEAR, TRY_CAST(t.ESTPROJECTCOST AS DOUBLE) AS ESTPROJECTCOST, p.geometry
  FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/housing/electrical-permits/electrical-permits.parquet' t
  JOIN 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/parcels/parcels.parquet' p
    ON t.HANDLE = p.HANDLE
) TO 'electrical-permits-geo.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);
```

Then convert as needed:

```bash
gpio convert geoparquet electrical-permits-geo.parquet electrical-permits-geo-optimized.parquet
gpio convert geopackage electrical-permits-geo.parquet electrical-permits.gpkg
gpio convert shapefile electrical-permits-geo.parquet electrical-permits.shp
```

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/housing/electrical-permits/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/housing/electrical-permits/) — rendered README and file listing
- [Source dataset](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=51) on the City of St. Louis open data portal

## Provenance

Mirror of [Electrical Permits](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=51) from the City of St. Louis; source: https://www.stlouis-mo.gov/data/upload/data-files/electrical-permits.zip. No explicit license is published — see the source page. Synced 2026-08-14T12:21:16+00:00.
