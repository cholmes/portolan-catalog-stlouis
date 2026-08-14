# AGENTS.md — Parking Meters

Parking meters from the Streets Division parking services map.

981 rows; geometry: Point (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/transportation-infrastructure-and-utilities/parking-meters/parking-meters.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/transportation-infrastructure-and-utilities/parking-meters/parking-meters.pmtiles` (layer `parking-meters`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/transportation-infrastructure-and-utilities/parking-meters/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/transportation-infrastructure-and-utilities/parking-meters/) — rendered README and file listing
- [Source dataset](https://maps8.stlouis-mo.gov/arcgis/rest/services/STREETS/ParkingServices/MapServer) on the City of St. Louis open data portal

## Provenance

Mirror of [Parking Meters](https://maps8.stlouis-mo.gov/arcgis/rest/services/STREETS/ParkingServices/MapServer) from the City of St. Louis; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/STREETS/ParkingServices/MapServer. No explicit license is published — see the source page. Synced 2026-08-14T11:21:05+00:00.
