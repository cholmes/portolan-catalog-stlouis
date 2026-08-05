# AGENTS.md — Property Sales

Dataset describes real estate sale prices for recent property sales in the city. A separate table describes codes for different type of sales.

191,829 rows; tabular (no geometry).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/property-sales/property-sales.parquet' LIMIT 5;
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

## Provenance

Mirror of [Property Sales](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=31) from the City of St. Louis open data portal; source: https://www.stlouis-mo.gov/data/upload/data-files/prclsale.zip. No explicit license is published — see the portal page. Synced 2026-08-05T17:00:27+00:00.
