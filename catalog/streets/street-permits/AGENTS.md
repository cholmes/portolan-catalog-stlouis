# AGENTS.md — Street Permits

Permits issued by the Street Department to allow for blocking of the right of way, excavation in the right of way, overdimensional vehicles, and food trucks

72,473 rows; tabular (no geometry).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/streets/street-permits/street-permits.parquet' LIMIT 5;
```

Full schema: `table:columns` in collection.json.

## Reproduce the geometry join

This collection is published as plain (non-geo) Parquet, exactly as the city publishes it; its map layer (`street-permits.pmtiles`) is materialized by joining to `neighborhoods`. To build your own GeoParquet:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
COPY (
  SELECT p.NHD_NAME, count(*) AS n_permits, p.geometry
  FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/streets/street-permits/street-permits.parquet' t
  JOIN 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/planning/neighborhoods/neighborhoods.parquet' p
    ON t.NEIGHBORHOOD = p.NHD_NAME
  GROUP BY p.NHD_NAME, p.geometry
) TO 'street-permits-geo.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);
```

Then convert as needed:

```bash
gpio convert geoparquet street-permits-geo.parquet street-permits-geo-optimized.parquet
gpio convert geopackage street-permits-geo.parquet street-permits.gpkg
gpio convert shapefile street-permits-geo.parquet street-permits.shp
```

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/streets/street-permits/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/streets/street-permits/) — rendered README and file listing
- [Source dataset](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=17) on the City of St. Louis open data portal

## Provenance

Mirror of [Street Permits](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=17) from the City of St. Louis; source: https://www.stlouis-mo.gov/data/upload/data-files/streets/street-permits.csv. No explicit license is published — see the source page. Synced 2026-08-05T19:58:51+00:00.
