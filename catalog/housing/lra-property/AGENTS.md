# AGENTS.md — LRA Property

Land Reutilization Authority data and search.

9,467 rows; geometry: MultiPolygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/housing/lra-property/lra-property.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/housing/lra-property/lra-property.pmtiles` (layer `lra-property`), styled by `styles/*.json` — `styles/default.json` is the default.

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

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/housing/lra-property/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/housing/lra-property/) — rendered README and file listing
- [Source dataset](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=30) on the City of St. Louis open data portal

## Provenance

Mirror of [LRA Property](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=30) from the City of St. Louis; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/SLDC_Real_Estate/FeatureServer. No explicit license is published — see the source page. Synced 2026-08-05T19:58:51+00:00.
