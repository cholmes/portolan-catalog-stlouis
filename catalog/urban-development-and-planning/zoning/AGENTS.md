# AGENTS.md — Zoning

Strategic land use (SLUP),parcel, and zoning data

126,945 rows; geometry: MultiPolygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/zoning/zoning.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/zoning/zoning.pmtiles` (layer `zoning`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `LAYER` — district letter A-L; official names are in the default style legend (from the city's renderer)

Full schema: `table:columns` in collection.json.

## Quirks

Parcel-level zoning (126,945 features). Overlay districts (CUP/FBD/SUD) live on a separate service layer not mirrored here yet.

## Joins

Spatial join to parcels, or parcels.Zoning carries a code per parcel record.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/urban-development-and-planning/zoning/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/zoning/) — rendered README and file listing
- [Source dataset](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=78) on the City of St. Louis open data portal

## Provenance

Mirror of [Zoning](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=78) from the City of St. Louis; source: https://maps9.stlouis-mo.gov/arcgis/rest/services/PDA/Zoning/MapServer. No explicit license is published — see the source page. Synced 2026-08-14T12:21:16+00:00.
