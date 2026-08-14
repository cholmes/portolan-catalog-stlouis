# AGENTS.md — Tax-abated Parcels

Parcels within the City of Saint Louis that have obtained and activated an abatement on real estate taxes.

1,440 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/business-and-industry/tax-abated-parcels/tax-abated-parcels.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/business-and-industry/tax-abated-parcels/tax-abated-parcels.pmtiles` (layer `tax-abated-parcels`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `HANDLE` — joins parcels.HANDLE
- `AbatementStartYear` — 2001-2025
- `AbatementEndYear` — when the abatement runs out

Full schema: `table:columns` in collection.json.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/business-and-industry/tax-abated-parcels/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/business-and-industry/tax-abated-parcels/) — rendered README and file listing
- [Source dataset](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=61) on the City of St. Louis open data portal

## Provenance

Mirror of [Tax-abated Parcels](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=61) from the City of St. Louis; source: https://static.stlouis-mo.gov/open-data/SLDC/TAX-ABATEMENT/taxabatedparcels.geojson. No explicit license is published — see the source page. Synced 2026-08-14T11:21:05+00:00.
