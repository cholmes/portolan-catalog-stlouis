# AGENTS.md — Polling Centers

Polling Centers

152 rows; geometry: Point (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/government/polling-places/polling-places.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/government/polling-places/polling-places.pmtiles` (layer `polling-places`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/government/polling-places/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/government/polling-places/) — rendered README and file listing
- [Source dataset](https://stlcity.maps.arcgis.com/home/item.html?id=87bc5cf8db58428295792e690397ed75) on the City of St. Louis open data portal

## Provenance

Mirror of [Polling Centers](https://stlcity.maps.arcgis.com/home/item.html?id=87bc5cf8db58428295792e690397ed75) from the City of St. Louis; source: https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/Polling_Centers_WFL1/FeatureServer. No explicit license is published — see the source page. Synced 2026-08-05T19:58:51+00:00.
