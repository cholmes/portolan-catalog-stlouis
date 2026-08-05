# AGENTS.md — Bike Infrastructure

Bicycle infrastructure from the city's Biking Infrastructure Map service: existing bike facilities by type, the Brickline Greenway and Hodiamont Trail, park paths, multi-use paths, and planned and funded major bike facility projects.

2,387 rows; geometry: LineString (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/bike-infrastructure/bike-infrastructure.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/bike-infrastructure/bike-infrastructure.pmtiles` (layer `bike-infrastructure`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Provenance

Mirror of [Bike Infrastructure](https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/Biking_Infrastructure_Map/MapServer) from the City of St. Louis open data portal; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/Biking_Infrastructure_Map/MapServer. No explicit license is published — see the portal page. Synced 2026-08-05T04:46:13+00:00.
