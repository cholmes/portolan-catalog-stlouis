# AGENTS.md — Neighborhood Organizations

Neighborhood Organizations as exported 6-20-20

103 rows; geometry: MultiPolygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/community/neighborhood-organizations/neighborhood-organizations.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/community/neighborhood-organizations/neighborhood-organizations.pmtiles` (layer `neighborhood-organizations`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Quirks

A 2020 snapshot (source: 'as exported 6-20-20'); contacts and activity status age accordingly.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/community/neighborhood-organizations/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/community/neighborhood-organizations/) — rendered README and file listing
- [Source dataset](https://stlcity.maps.arcgis.com/home/item.html?id=ac198aeb9592458b8591c7258e719ad1) on the City of St. Louis open data portal

## Provenance

Mirror of [Neighborhood Organizations](https://stlcity.maps.arcgis.com/home/item.html?id=ac198aeb9592458b8591c7258e719ad1) from the City of St. Louis; source: https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/Neighborhood_Organizations/FeatureServer. No explicit license is published — see the source page. Synced 2026-08-14T11:21:05+00:00.
