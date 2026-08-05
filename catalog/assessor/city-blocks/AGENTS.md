# AGENTS.md — City Blocks

Information about city blocks. A city block, residential block, urban block, or simply "block" is a central element of urban planning and urban design.

5,857 rows; geometry: MultiPolygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/assessor/city-blocks/city-blocks.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/assessor/city-blocks/city-blocks.pmtiles` (layer `city-blocks`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `Name` — city block number (string); numbering grew outward from the riverfront
- `BLOCK_HANDLE` — block handle; parcels.CityBlock relates

Full schema: `table:columns` in collection.json.

## Provenance

Mirror of [City Blocks](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=12) from the City of St. Louis open data portal; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/STLOUIS/BOUNDARIES/MapServer. No explicit license is published — see the portal page. Synced 2026-08-05T19:58:51+00:00.
