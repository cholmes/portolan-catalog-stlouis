# AGENTS.md — City Streets

City street GIS data

19,858 rows; geometry: MultiLineString (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/streets/streets.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/streets/streets.pmtiles` (layer `streets`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `Street_Name_Full` — full name
- `Class` — source class code (A31/A41/A6x/A73, no published decode)

Full schema: `table:columns` in collection.json.

## Provenance

Mirror of [City Streets](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=68) from the City of St. Louis open data portal; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Streets/FeatureServer. No explicit license is published — see the portal page. Synced 2026-08-05T04:46:13+00:00.
