# AGENTS.md — CDC PLACES Health Measures

CDC PLACES Health Measures

104 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/cdc-places/cdc-places.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/cdc-places/cdc-places.pmtiles` (layer `cdc-places`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `geoid` — 11-digit tract GEOID
- `foodinsecu` — food insecurity, % of adults (with _lo/_hi 95% confidence limits)
- `lacktrpt` — lacked reliable transportation, % of adults
- `casthma` — current asthma, % of adults
- `access2` — no health insurance 18-64 — cross-check acs-tracts.pct_uninsured

Full schema: `table:columns` in collection.json.

## Quirks

CDC model-based small-area estimates, not direct measurements of St. Louis residents: use for ranking tracts and pattern-finding, not as precise local values. Every measure has _lo/_hi 95% confidence limits. Measure data years mix 2022 and 2023 (see column descriptions).

## Joins

geoid = acs-tracts.geoid = acs-block-groups.tract.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/demographics/cdc-places/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/demographics/cdc-places/) — rendered README and file listing
- [Centers for Disease Control and Prevention documentation](https://www.cdc.gov/places/)

## Provenance

Published by Centers for Disease Control and Prevention — **not** City of St. Louis data; St. Louis extract by this mirror. Source: https://data.cdc.gov/resource/cwsq-ngmh. License: other (https://www.cdc.gov/other/agencymaterials.html). Synced 2026-08-14T12:21:16+00:00.
