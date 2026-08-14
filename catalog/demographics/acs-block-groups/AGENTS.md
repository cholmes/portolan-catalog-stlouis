# AGENTS.md — ACS Demographics — Block Groups

ACS Demographics — Block Groups

314 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/acs-block-groups/acs-block-groups.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/acs-block-groups/acs-block-groups.pmtiles` (layer `acs-block-groups`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `geoid` — 12-digit block group GEOID — the family's join key
- `tract` — 11-digit tract GEOID, joins acs-tracts and cdc-places
- `median_hh_income` — with _moe and _cv companions (B19013)
- `pct_hh_no_vehicle` — zero-vehicle households, % (B25044)
- `pct_people_of_color` — 100 − pct_white_nh (B03002)
- `pct_below_poverty` — income-to-poverty ratio < 1.00 (C17002)
- `pct_rent_burdened` — renters paying 30%+ of income (B25070)
- `pct_no_internet` — households with no internet (B28002)

Full schema: `table:columns` in collection.json.

## Quirks

Federal or third-party data, not the city's — see the description. GEOID join keys: a block group id is 12 digits, its tract is the first 11 (`left(geoid, 11)`), and everything in the city starts `29510`. ACS estimates carry `*_moe` margins of error at the 90% confidence level — at block-group scale the margin often rivals the estimate, so treat any `*_cv` above 0.30 as unreliable and aggregate before concluding. Suppressed estimates are NULL (never zero): exclude them, don't count them. Medians cannot be summed or averaged into larger areas. 53 of 314 block groups have NULL median income (too few sample households). Block groups with large group quarters (dorms, prisons) distort household rates — check acs-tracts.group_quarters_pop.

## Joins

Spatially join city points (crime, 311, permits via parcels) with ST_Within(pt, geometry), then GROUP BY geoid. `tract` joins acs-tracts and cdc-places without geometry. lodes-jobs and lodes-commutes share `geoid`.

## Example

```sql
-- Income quintile vs. car-free households: the equity gradient
SELECT income_q, round(avg(pct_hh_no_vehicle), 1) AS pct_no_car
FROM (
  SELECT ntile(5) OVER (ORDER BY median_hh_income) AS income_q,
         pct_hh_no_vehicle
  FROM read_parquet('acs-block-groups.parquet')
  WHERE median_hh_income IS NOT NULL)
GROUP BY income_q ORDER BY income_q;
```

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/demographics/acs-block-groups/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/demographics/acs-block-groups/) — rendered README and file listing
- [U.S. Census Bureau documentation](https://www.census.gov/programs-surveys/acs.html)

## Provenance

Published by U.S. Census Bureau — **not** City of St. Louis data; St. Louis extract by this mirror. Source: https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/. License: other (https://www.census.gov/topics/research/research-transparency-public-access/open-data.html). Synced 2026-08-14T12:21:16+00:00.
