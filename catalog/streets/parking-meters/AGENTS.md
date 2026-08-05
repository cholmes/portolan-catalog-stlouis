# AGENTS.md — Parking Meters

Parking meters from the Streets Division parking services map.

981 rows; geometry: Point (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/streets/parking-meters/parking-meters.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/streets/parking-meters/parking-meters.pmtiles` (layer `parking-meters`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Provenance

Mirror of [Parking Meters](https://maps8.stlouis-mo.gov/arcgis/rest/services/STREETS/ParkingServices/MapServer) from the City of St. Louis open data portal; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/STREETS/ParkingServices/MapServer. No explicit license is published — see the portal page. Synced 2026-08-05T19:58:51+00:00.
