# AGENTS.md — Overture Divisions

Point, line, and polygon representations of human settlements from the Overture divisions theme: recognized areas for governance, culture, or organization, from countries and regions down to counties, cities, and neighborhoods. Three feature types are merged here with an `overture_type` column: `division` (label points with population and hierarchy), `division_area` (the land or maritime polygon belonging to a division), and `division_boundary` (shared borders between divisions). For the St. Louis box that means the city itself, surrounding counties and municipalities on both sides of the river, and Overture's neighborhood set.

Unlike everything else in this catalog, this is **not** City of St. Louis data: it comes from the [Overture Maps Foundation](https://overturemaps.org/), a collaborative project building open, interoperable map data for the world. This collection is a St. Louis extract of that global dataset — everything inside the city's bounding box, which also takes in the Illinois shore of the Mississippi (East St. Louis, Cahokia Heights) — included here to demonstrate how a city's open-data catalog can blend in other St. Louis-relevant open data alongside the city's own. The GeoParquet was extracted from Overture release 2026-07-22.0; the map tiles reference Overture's own global PMTiles for the same release, the tiles behind [explore.overturemaps.org](https://explore.overturemaps.org/).

283 rows; geometry: LineString (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/government/overture-divisions/overture-divisions.parquet' LIMIT 5;
```

PMTiles for maps: Overture's own global theme tiles at `https://overturemaps-extras-us-west-2.s3.us-west-2.amazonaws.com/tiles/2026-07-22.0/divisions.pmtiles` (layers `division`, `division_area`, `division_boundary`), styled by `styles/*.json` — `styles/default.json` is the default. Not clipped to St. Louis: only the Parquet is the extract.

## Key fields

- `overture_type` — division (label point) / division_area (polygon) / division_boundary (line)
- `subtype` — country, region, county, locality, neighborhood, microhood
- `population` — on division points where known

Full schema: `table:columns` in collection.json.

## Quirks

Overture Maps Foundation data, not the city's — see the description. `id` is a GERS id (stable across Overture releases); `sources` records the upstream dataset per feature; struct/list columns (names, sources) are nested Parquet — DuckDB reads them natively. Geometries crossing the bbox edge are clipped to it. The country and region areas are bbox clips of the full US/Missouri/Illinois polygons.

## Joins

Compare neighborhood areas with the city's neighborhoods collection (spatial join).

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/government/overture-divisions/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/government/overture-divisions/) — rendered README and file listing
- [Overture divisions theme guide](https://docs.overturemaps.org/guides/divisions/)

## Provenance

St. Louis-bbox extract of the [Overture Maps Foundation](https://overturemaps.org/) divisions theme, release 2026-07-22.0 (`s3://overturemaps-us-west-2/release/2026-07-22.0/theme=divisions/`) — **not** City of St. Louis data. License: ODbL-1.0 (see [Overture attribution](https://docs.overturemaps.org/attribution/)). Synced 2026-08-14T12:21:16+00:00.
