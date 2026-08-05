# AGENTS.md — Tax-abated Parcels

Parcels within the City of Saint Louis that have obtained and activated an abatement on real estate taxes.

1,440 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/tax-abated-parcels/tax-abated-parcels.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/tax-abated-parcels/tax-abated-parcels.pmtiles` (layer `tax-abated-parcels`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `HANDLE` — joins parcels.HANDLE
- `AbatementStartYear` — 2001-2025
- `AbatementEndYear` — when the abatement runs out

Full schema: `table:columns` in collection.json.

## Provenance

Mirror of [Tax-abated Parcels](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=61) from the City of St. Louis open data portal; source: https://static.stlouis-mo.gov/open-data/SLDC/TAX-ABATEMENT/taxabatedparcels.geojson. No explicit license is published — see the portal page. Synced 2026-08-05T04:46:13+00:00.
