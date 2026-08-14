# AGENTS.md — LODES Jobs

LODES Jobs

314 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/lodes-jobs/lodes-jobs.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/lodes-jobs/lodes-jobs.pmtiles` (layer `lodes-jobs`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `geoid` — 12-digit block group GEOID
- `jobs_total` — jobs located here (workplace side, WAC C000)
- `workers_resident` — employed residents (residence side, RAC)
- `jobs_earn_low` — ≤ $1,250/month; _mid, _high for the rest

Full schema: `table:columns` in collection.json.

## Quirks

Federal or third-party data, not the city's — see the description. GEOID join keys: a block group id is 12 digits, its tract is the first 11 (`left(geoid, 11)`), and everything in the city starts `29510`. ACS estimates carry `*_moe` margins of error at the 90% confidence level — at block-group scale the margin often rivals the estimate, so treat any `*_cv` above 0.30 as unreliable and aggregate before concluding. Suppressed estimates are NULL (never zero): exclude them, don't count them. Medians cannot be summed or averaged into larger areas. Administrative counts, not survey estimates — no MOEs. Zero-filled: every block group is present. jobs_total ≫ workers_resident marks a job center whose daytime population dwarfs its census count.

## Joins

geoid = acs-block-groups.geoid — divide anything by residents + jobs for ambient-population rates.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/demographics/lodes-jobs/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/demographics/lodes-jobs/) — rendered README and file listing
- [U.S. Census Bureau documentation](https://lehd.ces.census.gov/data/)

## Provenance

Published by U.S. Census Bureau — **not** City of St. Louis data; St. Louis extract by this mirror. Source: https://lehd.ces.census.gov/data/lodes/LODES8/mo. License: other (https://www.census.gov/topics/research/research-transparency-public-access/open-data.html). Synced 2026-08-14T12:21:16+00:00.
