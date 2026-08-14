# AGENTS.md — ACS Demographics — Tracts

ACS Demographics — Tracts

104 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/acs-tracts/acs-tracts.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/acs-tracts/acs-tracts.pmtiles` (layer `acs-tracts`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `geoid` — 11-digit tract GEOID
- `pct_uninsured` — no health insurance coverage (B27001)
- `pct_with_disability` — civilian noninstitutionalized (B18101)
- `group_quarters_pop` — institutional population flag (B26001)
- `median_hh_income_black` — race-iterated income (B19013B) — tract is the finest level it exists

Full schema: `table:columns` in collection.json.

## Quirks

Federal or third-party data, not the city's — see the description. GEOID join keys: a block group id is 12 digits, its tract is the first 11 (`left(geoid, 11)`), and everything in the city starts `29510`. ACS estimates carry `*_moe` margins of error at the 90% confidence level — at block-group scale the margin often rivals the estimate, so treat any `*_cv` above 0.30 as unreliable and aggregate before concluding. Suppressed estimates are NULL (never zero): exclude them, don't count them. Medians cannot be summed or averaged into larger areas. This collection exists because these tables have no block-group release. Race-iterated medians are noisy even at tract level — check the _cv.

## Joins

acs-block-groups.tract = geoid; cdc-places.geoid = geoid.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/demographics/acs-tracts/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/demographics/acs-tracts/) — rendered README and file listing
- [U.S. Census Bureau documentation](https://www.census.gov/programs-surveys/acs.html)

## Provenance

Published by U.S. Census Bureau — **not** City of St. Louis data; St. Louis extract by this mirror. Source: https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/. License: other (https://www.census.gov/topics/research/research-transparency-public-access/open-data.html). Synced 2026-08-14T12:21:16+00:00.
