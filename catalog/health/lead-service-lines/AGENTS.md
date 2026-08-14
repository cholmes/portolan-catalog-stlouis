# AGENTS.md — Lead Service Line Inventory

Lead Service Line Inventory Feature Layer Service

112,950 rows; geometry: Point (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/health/lead-service-lines/lead-service-lines.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/health/lead-service-lines/lead-service-lines.pmtiles` (layer `lead-service-lines`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `address` — service address
- `utilstatus` — utility-side status, domain-coded: 0 Unknown, 1 Lead, 2 Non-Lead, 3 Galvanized Requiring Replacement
- `custstatus` — customer-side status, same domain
- `utilmaterial` — pipe material, domain-coded (109 Lead, 84 Copper, 89 Galvanized, 0 Unknown...)

Full schema: `table:columns` in collection.json.

## Quirks

EPA-mandated lead service line inventory from the Water Division AGOL org; 112,950 address points, actively maintained. Material/status fields are numeric domain codes — the decode lives in the default styles and in staging/extracts/lead-service-lines/layer-metadata.json.

## Joins

address matches parcel situs addresses (fuzzy).

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/health/lead-service-lines/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/health/lead-service-lines/) — rendered README and file listing
- [Source dataset](https://stlcity.maps.arcgis.com/home/item.html?id=80c69343cc2d418fb1796a342a863aac) on the City of St. Louis open data portal

## Provenance

Mirror of [Lead Service Line Inventory](https://stlcity.maps.arcgis.com/home/item.html?id=80c69343cc2d418fb1796a342a863aac) from the City of St. Louis; source: https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/STLWD_LSLI__Read_Only_View/FeatureServer. No explicit license is published — see the source page. Synced 2026-08-14T12:21:16+00:00.
