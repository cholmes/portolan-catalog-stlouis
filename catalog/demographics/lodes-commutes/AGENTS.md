# AGENTS.md — LODES Commute Flows

LODES Commute Flows

149,566 rows; tabular (no geometry).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/lodes-commutes/lodes-commutes.parquet' LIMIT 5;
```

## Key fields

- `home_geoid` — where the workers live (12-digit BG)
- `work_geoid` — where their jobs are (12-digit BG)
- `jobs` — workers with this home→work pair (S000)
- `home_in_city` — with work_in_city, splits inbound/outbound/internal flows

Full schema: `table:columns` in collection.json.

## Quirks

Federal or third-party data, not the city's — see the description. GEOID join keys: a block group id is 12 digits, its tract is the first 11 (`left(geoid, 11)`), and everything in the city starts `29510`. ACS estimates carry `*_moe` margins of error at the 90% confidence level — at block-group scale the margin often rivals the estimate, so treat any `*_cv` above 0.30 as unreliable and aggregate before concluding. Suppressed estimates are NULL (never zero): exclude them, don't count them. Medians cannot be summed or averaged into larger areas. Tabular — join a geoid to acs-block-groups for geometry. Includes out-of-state residents working in Missouri (Illinois commuters), but NOT St. Louis residents working out of state, per the LODES file structure.

## Joins

home_geoid / work_geoid = acs-block-groups.geoid = lodes-jobs.geoid.

## Example

```sql
-- Where do low-earnings workers employed downtown live?
SELECT home_geoid, sum(jobs_earn_low) AS low_wage_workers
FROM read_parquet('lodes-commutes.parquet')
WHERE work_geoid LIKE '295101256%'  -- downtown tracts
GROUP BY 1 ORDER BY 2 DESC LIMIT 10;
```

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/demographics/lodes-commutes/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/demographics/lodes-commutes/) — rendered README and file listing
- [U.S. Census Bureau documentation](https://lehd.ces.census.gov/data/)

## Provenance

Published by U.S. Census Bureau — **not** City of St. Louis data; St. Louis extract by this mirror. Source: https://lehd.ces.census.gov/data/lodes/LODES8/mo. License: other (https://www.census.gov/topics/research/research-transparency-public-access/open-data.html). Synced 2026-08-14T12:21:16+00:00.
