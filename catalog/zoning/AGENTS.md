# AGENTS.md — Zoning

Strategic land use (SLUP),parcel, and zoning data

126,945 rows; geometry: MultiPolygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/zoning/zoning.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/zoning/zoning.pmtiles` (layer `zoning`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `LAYER` — district letter A-L; official names are in the default style legend (from the city's renderer)

Full schema: `table:columns` in collection.json.

## Quirks

Parcel-level zoning (126,945 features). Overlay districts (CUP/FBD/SUD) live on a separate service layer not mirrored here yet.

## Joins

Spatial join to parcels, or parcels.Zoning carries a code per parcel record.

## Provenance

Mirror of [Zoning](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=78) from the City of St. Louis open data portal; source: https://maps9.stlouis-mo.gov/arcgis/rest/services/PDA/Zoning/MapServer. No explicit license is published — see the portal page. Synced 2026-08-05T04:46:13+00:00.
