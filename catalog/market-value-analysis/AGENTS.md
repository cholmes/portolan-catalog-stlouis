# AGENTS.md — 2024 Market Value Analysis

The Market Value Analysis (MVA) is an in-depth study and mapping of a community's housing market. It reveals the mosaic of market conditions in St. Louis.

314 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/market-value-analysis/market-value-analysis.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/market-value-analysis/market-value-analysis.pmtiles` (layer `market-value-analysis`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `geoid` — census block group GEOID
- `MVACluster` — market cluster A (strongest) - I (weakest)

Full schema: `table:columns` in collection.json.

## Quirks

Reinvestment Fund 2024 MVA at block-group level; ~30 market indicator columns.

## Provenance

Mirror of [2024 Market Value Analysis](https://stlcity.maps.arcgis.com/home/item.html?id=e71e3ebca1f345a4b7db134d30c5d9ff) from the City of St. Louis open data portal; source: https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/2024_Market_Value_Analysis/FeatureServer. No explicit license is published — see the portal page. Synced 2026-08-05T17:48:01+00:00.
