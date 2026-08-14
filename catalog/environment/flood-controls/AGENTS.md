# AGENTS.md — Flood Controls

Floods Controls

71 rows; geometry: LineString (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/environment/flood-controls/flood-controls.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/environment/flood-controls/flood-controls.pmtiles` (layer `flood-controls`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/environment/flood-controls/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/environment/flood-controls/) — rendered README and file listing
- [Source dataset](https://stlcity.maps.arcgis.com/home/item.html?id=4a08499ad4054caca42215e4c51aac0e) on the City of St. Louis open data portal

## Provenance

Mirror of [Flood Controls](https://stlcity.maps.arcgis.com/home/item.html?id=4a08499ad4054caca42215e4c51aac0e) from the City of St. Louis; source: https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/Flood_Controls_WFL1/FeatureServer. No explicit license is published — see the source page. Synced 2026-08-14T12:21:16+00:00.
