# AGENTS.md — Flood Controls

Floods Controls

71 rows; geometry: LineString (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/flood-controls/flood-controls.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/flood-controls/flood-controls.pmtiles` (layer `flood-controls`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Provenance

Mirror of [Flood Controls](https://stlcity.maps.arcgis.com/home/item.html?id=4a08499ad4054caca42215e4c51aac0e) from the City of St. Louis open data portal; source: https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/Flood_Controls_WFL1/FeatureServer. No explicit license is published — see the portal page. Synced 2026-08-05T17:48:01+00:00.
