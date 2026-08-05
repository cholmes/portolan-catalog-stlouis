# AGENTS.md — Community Improvement Districts (CIDs)

Community improvement districts (CIDs) within the City of Saint Louis. CIDs are established by the section of Missouri statute known as the "Community Improvement District Act". More info: http://revisor.mo.gov/main/OneSection.aspx?section=67.1401&bid=3019&hl=

98 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/community-improvement-districts/community-improvement-districts.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/community-improvement-districts/community-improvement-districts.pmtiles` (layer `community-improvement-districts`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `Name` — district name
- `Active` — Y (70) / N (21) / blank

Full schema: `table:columns` in collection.json.

## Provenance

Mirror of [Community Improvement Districts (CIDs)](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=58) from the City of St. Louis open data portal; source: https://static.stlouis-mo.gov/open-data/SLDC/TAXING-DISTRICTS/CID/STLCIDs.geojson. No explicit license is published — see the portal page. Synced 2026-08-05T17:00:27+00:00.
