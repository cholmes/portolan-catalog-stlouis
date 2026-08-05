# AGENTS.md — City Parks

A database containing information on city parks, park amenities, and amenity attributes

117 rows; geometry: MultiPolygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/leisure-and-culture/parks/parks.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/leisure-and-culture/parks/parks.pmtiles` (layer `parks`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `TEXT_` — park name
- `ACRES` — official acreage
- `NEW_CLASS` — park classification

Full schema: `table:columns` in collection.json.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/leisure-and-culture/parks/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/leisure-and-culture/parks/) — rendered README and file listing
- [Source dataset](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=46) on the City of St. Louis open data portal

## Provenance

Mirror of [City Parks](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=46) from the City of St. Louis; source: https://maps9.stlouis-mo.gov/arcgis/rest/services/PARKS/Reservable_Park_Amenities/FeatureServer. No explicit license is published — see the source page. Synced 2026-08-05T19:58:51+00:00.
