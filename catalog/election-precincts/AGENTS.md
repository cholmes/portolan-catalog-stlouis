# AGENTS.md — Election Wards & Precincts

Wards & current election precincts for the City of St. Louis.

209 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/election-precincts/election-precincts.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/election-precincts/election-precincts.pmtiles` (layer `election-precincts`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `name` — 'W <ward> P <precinct>'

Full schema: `table:columns` in collection.json.

## Quirks

The BOE FeatureServers reject paged queries, so this comes from the static shapefile (reprojected from MO State Plane East to WGS84).

## Provenance

Mirror of [Election Wards & Precincts](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=124) from the City of St. Louis open data portal; source: https://static.stlouis-mo.gov/open-data/BOEC/Precincts_Current.zip. No explicit license is published — see the portal page. Synced 2026-08-05T04:46:13+00:00.
