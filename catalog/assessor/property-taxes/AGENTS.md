# AGENTS.md — Property Taxes

Property tax records by parcel

135,969 rows; tabular (no geometry).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/assessor/property-taxes/property-taxes.parquet' LIMIT 5;
```

Full schema: `table:columns` in collection.json.

## Reproduce the geometry join

This collection is published as plain (non-geo) Parquet, exactly as the city publishes it; its map layer (`property-taxes.pmtiles`) is materialized by joining to `parcels`. To build your own GeoParquet:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
COPY (
  SELECT t.AsrParcelId, t.AsdTotal, t.AsdLand, t.AsdImprove, t.BillYear, t.OwnerName, p.geometry
  FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/assessor/property-taxes/property-taxes.parquet' t
  JOIN 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/assessor/parcels/parcels.parquet' p
    ON t.AsrParcelId = p.ParcelId
) TO 'property-taxes-geo.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);
```

Then convert as needed:

```bash
gpio convert geoparquet property-taxes-geo.parquet property-taxes-geo-optimized.parquet
gpio convert geopackage property-taxes-geo.parquet property-taxes.gpkg
gpio convert shapefile property-taxes-geo.parquet property-taxes.shp
```

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/assessor/property-taxes/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/assessor/property-taxes/) — rendered README and file listing
- [Source dataset](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=3) on the City of St. Louis open data portal

## Provenance

Mirror of [Property Taxes](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=3) from the City of St. Louis; source: https://www.stlouis-mo.gov/data/upload/data-files/prcl.zip. No explicit license is published — see the source page. Synced 2026-08-05T19:58:51+00:00.
