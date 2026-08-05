# AGENTS.md — Parcels

Current and historic parcel data

134,362 rows; geometry: MultiPolygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/parcels/parcels.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/parcels/parcels.pmtiles` (layer `parcels`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `HANDLE` — assessor parcel handle — the city-wide parcel join key
- `ParcelId` — 10-digit parcel id (same as AsrParcelId elsewhere)
- `OWNERNAME` — current owner
- `AsdTotal` — total assessed value (dollars)
- `VacantLot` — Access-style boolean: -1 vacant, 0 not
- `FirstYearBuilt` — 0 means unknown (28k parcels)
- `NBRHD` — neighborhood number (joins neighborhoods.NHD_NUM)
- `WARD` — current ward number
- `Zoning` — zoning code on the parcel record

Full schema: `table:columns` in collection.json.

## Quirks

134,362 parcels. Owner addresses and legal descriptions are as-recorded by the assessor; casing is inconsistent. Many numeric codes (OwnerCode, AsrClassCode, SpecParcelType) have no published decode.

## Joins

property-sales.AsrParcelId = parcels.ParcelId; tax-abated-parcels and lra-property share HANDLE; neighborhoods via NBRHD = NHD_NUM; wards via WARD.

## Provenance

Mirror of [Parcels](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=82) from the City of St. Louis open data portal; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/PARCELS_PUBLIC/MapServer. No explicit license is published — see the portal page. Synced 2026-08-05T04:46:13+00:00.
