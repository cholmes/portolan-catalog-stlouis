# AGENTS.md — Overture Buildings

Building footprints and building parts from the Overture Maps buildings theme, which describes human-made structures with roofs or interior spaces that are permanently or semi-permanently in one place. Overture's goal is to provide the world's most comprehensive set of building structures compiled from the best available open data sources. Where known, buildings carry height, number of floors, and facade and roof attributes, supporting 2D and 3D visualization, data enrichment via GERS IDs, and spatial analysis. Both feature types are merged here, with an `overture_type` column telling buildings from building parts. Overture documents this data well: the [buildings theme guide](https://docs.overturemaps.org/guides/buildings/) covers what the theme models, how Overture builds it, and how to query it, and the schema reference gives every field of the feature types merged here — [`building`](https://docs.overturemaps.org/schema/reference/buildings/building/), [`building_part`](https://docs.overturemaps.org/schema/reference/buildings/building_part/).

Unlike everything else in this catalog, this is **not** City of St. Louis data: it comes from the [Overture Maps Foundation](https://overturemaps.org/), a collaborative project building open, interoperable map data for the world. This collection is a St. Louis extract of that global dataset — everything inside the city's bounding box, which also takes in the Illinois shore of the Mississippi (East St. Louis, Cahokia Heights) — included here to demonstrate how a city's open-data catalog can blend in other St. Louis-relevant open data alongside the city's own. The GeoParquet was extracted from Overture release 2026-07-22.0; the map tiles reference Overture's own global PMTiles for the same release, the tiles behind [explore.overturemaps.org](https://explore.overturemaps.org/).

194,132 rows; geometry: MultiPolygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/overture-buildings/overture-buildings.parquet' LIMIT 5;
```

PMTiles for maps: Overture's own global theme tiles at `https://overturemaps-extras-us-west-2.s3.us-west-2.amazonaws.com/tiles/2026-07-22.0/buildings.pmtiles` (layers `building`, `building_part`), styled by `styles/*.json` — `styles/default.json` is the default. Not clipped to St. Louis: only the Parquet is the extract.

## Key fields

- `height` — measured height in meters — present on ~89% of St. Louis footprints (median 4.4 m)
- `num_floors` — floor count where known
- `subtype` — building use (residential, commercial…) — mostly null here
- `overture_type` — building or building_part
- `has_parts` — true when building_part rows carry the detail

Full schema: `table:columns` in collection.json.

## Quirks

Overture Maps Foundation data, not the city's — see the description. `id` is a GERS id (stable across Overture releases); `sources` records the upstream dataset per feature; struct/list columns (names, sources) are nested Parquet — DuckDB reads them natively. Geometries crossing the bbox edge are clipped to it.

## Joins

Spatial join to parcels for assessor attributes; overture-addresses points fall inside most footprints.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/urban-development-and-planning/overture-buildings/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/overture-buildings/) — rendered README and file listing
- [Overture buildings theme guide](https://docs.overturemaps.org/guides/buildings/) — what the theme models, how Overture builds it, how to query it
- [Overture schema reference: building](https://docs.overturemaps.org/schema/reference/buildings/building/) — every field of the `building` feature type
- [Overture schema reference: building_part](https://docs.overturemaps.org/schema/reference/buildings/building_part/) — every field of the `building_part` feature type

## Provenance

St. Louis-bbox extract of the [Overture Maps Foundation](https://overturemaps.org/) buildings theme, release 2026-07-22.0 (`s3://overturemaps-us-west-2/release/2026-07-22.0/theme=buildings/`) — **not** City of St. Louis data. License: ODbL-1.0 (see [Overture attribution](https://docs.overturemaps.org/attribution/)). Synced 2026-08-14T12:21:16+00:00.
