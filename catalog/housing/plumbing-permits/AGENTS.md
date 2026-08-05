# AGENTS.md — Plumbing Permits

Plumbing permit information by property type, year, neighborhood, ward, and project type.

209,983 rows; tabular (no geometry).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/housing/plumbing-permits/plumbing-permits.parquet' LIMIT 5;
```

Full schema: `table:columns` in collection.json.

## Reproduce the geometry join

This collection is published as plain (non-geo) Parquet, exactly as the city publishes it; its map layer (`plumbing-permits.pmtiles`) is materialized by joining to `parcels`. To build your own GeoParquet:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
COPY (
  SELECT t.HANDLE, t.APPTYPE, t.APPDESCRIPTION, TRY_CAST(substr(t.ISSUEDATE, 1, 4) AS INT) AS PERMIT_YEAR, TRY_CAST(t.ESTPROJECTCOST AS DOUBLE) AS ESTPROJECTCOST, p.geometry
  FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/housing/plumbing-permits/plumbing-permits.parquet' t
  JOIN 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/parcels/parcels.parquet' p
    ON t.HANDLE = p.HANDLE
) TO 'plumbing-permits-geo.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);
```

Then convert as needed:

```bash
gpio convert geoparquet plumbing-permits-geo.parquet plumbing-permits-geo-optimized.parquet
gpio convert geopackage plumbing-permits-geo.parquet plumbing-permits.gpkg
gpio convert shapefile plumbing-permits-geo.parquet plumbing-permits.shp
```

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/housing/plumbing-permits/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/housing/plumbing-permits/) — rendered README and file listing
- [Source dataset](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=53) on the City of St. Louis open data portal

## Provenance

Mirror of [Plumbing Permits](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=53) from the City of St. Louis; source: https://www.stlouis-mo.gov/data/upload/data-files/plumbing-permits.zip. No explicit license is published — see the source page. Synced 2026-08-05T19:58:51+00:00.
