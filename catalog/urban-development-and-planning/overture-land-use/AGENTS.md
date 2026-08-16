# AGENTS.md — Overture Land Use

Land use features from the Overture base theme: the predominant human use of an area of land — commercial activity, recreation, farming, housing, education, or military use. Overture's land use data is a translation of the `landuse` tag from OpenStreetMap, classified by `subtype` and `class`. Overture documents this data well: the [base theme guide](https://docs.overturemaps.org/guides/base/) covers what the theme models, how Overture builds it, and how to query it, and the schema reference gives every field of its feature type — [`land_use`](https://docs.overturemaps.org/schema/reference/base/land_use/).

Unlike everything else in this catalog, this is **not** City of St. Louis data: it comes from the [Overture Maps Foundation](https://overturemaps.org/), a collaborative project building open, interoperable map data for the world. This collection is a St. Louis extract of that global dataset — everything inside the city's bounding box, which also takes in the Illinois shore of the Mississippi (East St. Louis, Cahokia Heights) — included here to demonstrate how a city's open-data catalog can blend in other St. Louis-relevant open data alongside the city's own. The GeoParquet was extracted from Overture release 2026-07-22.0; the map tiles reference Overture's own global PMTiles for the same release, the tiles behind [explore.overturemaps.org](https://explore.overturemaps.org/).

22,067 rows; geometry: LineString (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/overture-land-use/overture-land-use.parquet' LIMIT 5;
```

PMTiles for maps: Overture's own global theme tiles at `https://overturemaps-extras-us-west-2.s3.us-west-2.amazonaws.com/tiles/2026-07-22.0/base.pmtiles` (layers `land_use`), styled by `styles/*.json` — `styles/default.json` is the default. Not clipped to St. Louis: only the Parquet is the extract.

## Key fields

- `subtype` — park, managed, residential, golf…
- `class` — the underlying OSM landuse value

Full schema: `table:columns` in collection.json.

## Quirks

Overture Maps Foundation data, not the city's — see the description. `id` is a GERS id (stable across Overture releases); `sources` records the upstream dataset per feature; struct/list columns (names, sources) are nested Parquet — DuckDB reads them natively. Geometries crossing the bbox edge are clipped to it.

## Joins

Contrast with the city's own land-use (Strategic Land Use Plan) and zoning collections.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/urban-development-and-planning/overture-land-use/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/overture-land-use/) — rendered README and file listing
- [Overture base theme guide](https://docs.overturemaps.org/guides/base/) — what the theme models, how Overture builds it, how to query it
- [Overture schema reference: land_use](https://docs.overturemaps.org/schema/reference/base/land_use/) — every field of the `land_use` feature type

## Provenance

St. Louis-bbox extract of the [Overture Maps Foundation](https://overturemaps.org/) base theme, release 2026-07-22.0 (`s3://overturemaps-us-west-2/release/2026-07-22.0/theme=base/`) — **not** City of St. Louis data. License: ODbL-1.0 (see [Overture attribution](https://docs.overturemaps.org/attribution/)). Synced 2026-08-14T12:21:16+00:00.
