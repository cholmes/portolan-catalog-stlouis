# AGENTS.md — Siren Locations

Public emergency siren locations. While these sirens are generally thought of as "tornado sirens" they can be used in other circumstances/emergencies.

58 rows; geometry: Point (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/siren-locations/siren-locations.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/siren-locations/siren-locations.pmtiles` (layer `siren-locations`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Provenance

Mirror of [Siren Locations](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=132) from the City of St. Louis open data portal; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/BPS/City_of_St__Louis_Firehouses_and_Outdoor_Warning_Sirens1/MapServer. No explicit license is published — see the portal page. Synced 2026-08-05T17:00:27+00:00.
