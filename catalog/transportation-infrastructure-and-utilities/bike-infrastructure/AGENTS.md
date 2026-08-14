# AGENTS.md — Bike Infrastructure

Bicycle infrastructure from the city's Biking Infrastructure Map service: existing bike facilities by type, the Brickline Greenway and Hodiamont Trail, park paths, multi-use paths, and planned and funded major bike facility projects.

2,387 rows; geometry: LineString (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/transportation-infrastructure-and-utilities/bike-infrastructure/bike-infrastructure.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/transportation-infrastructure-and-utilities/bike-infrastructure/bike-infrastructure.pmtiles` (layer `bike-infrastructure`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/transportation-infrastructure-and-utilities/bike-infrastructure/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/transportation-infrastructure-and-utilities/bike-infrastructure/) — rendered README and file listing
- [Source dataset](https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/Biking_Infrastructure_Map/MapServer) on the City of St. Louis open data portal

## Provenance

Mirror of [Bike Infrastructure](https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/Biking_Infrastructure_Map/MapServer) from the City of St. Louis; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/Biking_Infrastructure_Map/MapServer. No explicit license is published — see the source page. Synced 2026-08-14T11:21:05+00:00.
