# AGENTS.md — Parcel Vacancy Composite

Parcel-level vacancy indicators for St. Louis: vacant buildings, condemnations, tax delinquency, LRA ownership, and private vacancy, compiled by SLDC.

20,694 rows; geometry: MultiPolygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/development/vacancy-composite/vacancy-composite.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/development/vacancy-composite/vacancy-composite.pmtiles` (layer `vacancy-composite`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `STREET_ADD` — address
- `PROPERTY_T` — Land or Structure
- `TOLEMI_DEF` — vacancy classification
- `PID1` — parcel id

Full schema: `table:columns` in collection.json.

## Quirks

SLDC/Tolemi BuildingBlocks export (2025-01); 20,694 parcels flagged vacant by at least one indicator.

## Joins

PID1/PID2 relate to parcels.ParcelId.

## Provenance

Mirror of [Parcel Vacancy Composite](https://stlcity.maps.arcgis.com/home/item.html?id=98a6f429617546be9d9b467c5ad1dafc) from the City of St. Louis open data portal; source: https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/SLDC_SLDC_Tol_Def_Vac_NP/FeatureServer. No explicit license is published — see the portal page. Synced 2026-08-05T19:58:51+00:00.
