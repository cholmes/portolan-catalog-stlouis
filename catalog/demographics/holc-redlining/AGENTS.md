# AGENTS.md — HOLC Redlining Grades (1930s)

HOLC Redlining Grades (1930s)

127 rows; geometry: MultiPolygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/holc-redlining/holc-redlining.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/holc-redlining/holc-redlining.pmtiles` (layer `holc-redlining`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `grade` — A best / B still desirable / C declining / D hazardous (redlined); one polygon is ungraded NULL
- `label` — area id from the original map sheet (e.g. D4)
- `fill` — the 1930s map's own hex color for the grade

Full schema: `table:columns` in collection.json.

## Quirks

Mapping Inequality (University of Richmond) data, not the city's — 1930s HOLC survey polygons, CC BY-NC-SA 4.0 (non-commercial; the one collection here with a restrictive license). Boundaries were hand-drawn on 1930s street maps: expect slivers against modern geographies.

## Joins

Spatial: ST_Within(ST_Centroid(bg.geometry), holc.geometry) assigns each modern block group its 1930s grade for persistence analysis.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/demographics/holc-redlining/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/demographics/holc-redlining/) — rendered README and file listing
- [Mapping Inequality, Digital Scholarship Lab, University of Richmond documentation](https://dsl.richmond.edu/panorama/redlining/)

## Provenance

Published by Mapping Inequality, Digital Scholarship Lab, University of Richmond — **not** City of St. Louis data; St. Louis extract by this mirror. Source: https://data.source.coop/cboettig/mappinginequality/mappinginequality.parquet. License: CC-BY-NC-SA-4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/). Synced 2026-08-14T12:21:16+00:00.
