# AGENTS.md — Neighborhood Organizations

Neighborhood Organizations as exported 6-20-20

103 rows; geometry: MultiPolygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/neighborhood-organizations/neighborhood-organizations.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/neighborhood-organizations/neighborhood-organizations.pmtiles` (layer `neighborhood-organizations`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Quirks

A 2020 snapshot (source: 'as exported 6-20-20'); contacts and activity status age accordingly.

## Provenance

Mirror of [Neighborhood Organizations](https://stlcity.maps.arcgis.com/home/item.html?id=ac198aeb9592458b8591c7258e719ad1) from the City of St. Louis open data portal; source: https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/Neighborhood_Organizations/FeatureServer. No explicit license is published — see the portal page. Synced 2026-08-05T17:00:27+00:00.
