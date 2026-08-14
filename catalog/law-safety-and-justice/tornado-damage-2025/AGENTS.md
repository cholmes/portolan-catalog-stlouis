# AGENTS.md — May 2025 Tornado Damage

NWS/NOAA damage assessment data for the May 2025 St. Louis tornado, with Prop NS property stabilization and sales status.

287 rows; geometry: LineString (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/law-safety-and-justice/tornado-damage-2025/tornado-damage-2025.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/law-safety-and-justice/tornado-damage-2025/tornado-damage-2025.pmtiles` (layer `tornado-damage-2025`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Quirks

NWS Damage Assessment Toolkit record of the May 16, 2025 EF-3 tornado: one damage-path polygon plus 286 surveyed points (source_layer distinguishes them).

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/law-safety-and-justice/tornado-damage-2025/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/law-safety-and-justice/tornado-damage-2025/) — rendered README and file listing
- [Source dataset](https://stlcity.maps.arcgis.com/home/item.html?id=d2f73ad3cd2b434b91c6eacaef94df32) on the City of St. Louis open data portal

## Provenance

Mirror of [May 2025 Tornado Damage](https://stlcity.maps.arcgis.com/home/item.html?id=d2f73ad3cd2b434b91c6eacaef94df32) from the City of St. Louis; source: https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/NS_Tornado_Map_WFL1/FeatureServer. No explicit license is published — see the source page. Synced 2026-08-14T11:21:05+00:00.
