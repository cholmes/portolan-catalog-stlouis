# AGENTS.md — 2024 Market Value Analysis

The Market Value Analysis (MVA) is an in-depth study and mapping of a community's housing market. It reveals the mosaic of market conditions in St. Louis.

314 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/housing/market-value-analysis/market-value-analysis.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/housing/market-value-analysis/market-value-analysis.pmtiles` (layer `market-value-analysis`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `geoid` — census block group GEOID
- `MVACluster` — market cluster A (strongest) - I (weakest)

Full schema: `table:columns` in collection.json.

## Quirks

Reinvestment Fund 2024 MVA at block-group level; ~30 market indicator columns.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/housing/market-value-analysis/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/housing/market-value-analysis/) — rendered README and file listing
- [Source dataset](https://stlcity.maps.arcgis.com/home/item.html?id=e71e3ebca1f345a4b7db134d30c5d9ff) on the City of St. Louis open data portal

## Provenance

Mirror of [2024 Market Value Analysis](https://stlcity.maps.arcgis.com/home/item.html?id=e71e3ebca1f345a4b7db134d30c5d9ff) from the City of St. Louis; source: https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/2024_Market_Value_Analysis/FeatureServer. No explicit license is published — see the source page. Synced 2026-08-14T11:21:05+00:00.
