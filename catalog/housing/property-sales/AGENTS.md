# AGENTS.md — Property Sales

Dataset describes real estate sale prices for recent property sales in the city. A separate table describes codes for different type of sales.

191,829 rows; tabular (no geometry).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/housing/property-sales/property-sales.parquet' LIMIT 5;
```

## Key fields

- `AsrParcelId` — parcel id — joins parcels.ParcelId
- `SaleDate` — text m/d/yy from the source MDB
- `SalePrice` — dollars; 0 on many non-market transfers
- `SaleType` — code; SaleTypeDescr carries the source's own decode

Full schema: `table:columns` in collection.json.

## Quirks

191,829 sales from the assessor's Access database (PrclSale table). Dates are 2-digit-year strings — parse with strptime('%m/%d/%y %H:%M:%S') and sanity-check the century. No geometry: join to parcels for mapping.

## Joins

parcels via AsrParcelId = ParcelId (10-digit, zero-padded).

## Reproduce the geometry join

This collection is published as plain (non-geo) Parquet, exactly as the city publishes it; its map layer (`property-sales.pmtiles`) is materialized by joining to `parcels`. To build your own GeoParquet:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
COPY (
  SELECT t.AsrParcelId, t.SalePrice, t.SaleTypeDescr, TRY_CAST(substr(strptime(t.SaleDate, '%m/%d/%y %H:%M:%S')::VARCHAR, 1, 4) AS INT) AS SALE_YEAR, round(t.SalePrice / NULLIF(p.LANDAREA, 0), 2) AS PricePerSqFt, p.geometry
  FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/housing/property-sales/property-sales.parquet' t
  JOIN 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/parcels/parcels.parquet' p
    ON t.AsrParcelId = p.ParcelId
) TO 'property-sales-geo.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);
```

Then convert as needed:

```bash
gpio convert geoparquet property-sales-geo.parquet property-sales-geo-optimized.parquet
gpio convert geopackage property-sales-geo.parquet property-sales.gpkg
gpio convert shapefile property-sales-geo.parquet property-sales.shp
```

## Example

```sql
-- median sale price by neighborhood, 2020s market sales
SELECT n.NHD_NAME, median(s.SalePrice) mp, count(*) n_sales
FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/property-sales/property-sales.parquet' s
JOIN 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/parcels/parcels.parquet' p ON s.AsrParcelId = p.ParcelId
JOIN 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/neighborhoods/neighborhoods.parquet' n ON p.NBRHD = n.NHD_NUM
WHERE s.SalePrice > 1000 AND strptime(s.SaleDate, '%m/%d/%y %H:%M:%S') >= DATE '2020-01-01'
GROUP BY 1 ORDER BY 2 DESC LIMIT 15;
```

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/housing/property-sales/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/housing/property-sales/) — rendered README and file listing
- [Source dataset](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=31) on the City of St. Louis open data portal

## Provenance

Mirror of [Property Sales](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=31) from the City of St. Louis; source: https://www.stlouis-mo.gov/data/upload/data-files/prclsale.zip. No explicit license is published — see the source page. Synced 2026-08-14T12:21:16+00:00.
