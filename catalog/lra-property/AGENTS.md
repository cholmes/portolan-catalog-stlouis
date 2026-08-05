# AGENTS.md — LRA Property

Land Reutilization Authority data and search.

9,467 rows; geometry: MultiPolygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/lra-property/lra-property.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/lra-property/lra-property.pmtiles` (layer `lra-property`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `Handle` — parcel handle — joins parcels.HANDLE
- `Status` — Available (8,762) / holds / SOLD / Unavailable
- `Usage` — Vacant Lot vs Residential etc. — case varies, use ILIKE
- `Property_Source` — how the LRA acquired it (Tax Suit dominates)

Full schema: `table:columns` in collection.json.

## Quirks

The source service layer contains every city parcel with an LRA flag; this collection is the LRA='YES' subset (9,467).

## Joins

parcels via Handle = HANDLE.

## Provenance

Mirror of [LRA Property](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=30) from the City of St. Louis open data portal; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/SLDC_Real_Estate/FeatureServer. No explicit license is published — see the portal page. Synced 2026-08-05T17:48:01+00:00.
