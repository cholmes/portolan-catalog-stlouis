# AGENTS.md — Overture Transportation

The Overture transportation theme is a model of how the world's roads, rails, and waterways connect: traversable segments (roads, railways, ferries) and connectors (intersections) representing how people and objects travel, built from OpenStreetMap and enhanced with data from TomTom and other local and regional authoritative sources. It is simple at its core but expressive enough to capture speed limits that change by time of day, one-way streets that allow buses the wrong way, and weight-restricted bridges. Both feature types are merged here, with an `overture_type` column telling segments from connectors. Overture documents this data well: the [transportation theme guide](https://docs.overturemaps.org/guides/transportation/) covers what the theme models, how Overture builds it, and how to query it, and the schema reference gives every field of the feature types merged here — [`segment`](https://docs.overturemaps.org/schema/reference/transportation/segment/), [`connector`](https://docs.overturemaps.org/schema/reference/transportation/connector/).

Unlike everything else in this catalog, this is **not** City of St. Louis data: it comes from the [Overture Maps Foundation](https://overturemaps.org/), a collaborative project building open, interoperable map data for the world. This collection is a St. Louis extract of that global dataset — everything inside the city's bounding box, which also takes in the Illinois shore of the Mississippi (East St. Louis, Cahokia Heights) — included here to demonstrate how a city's open-data catalog can blend in other St. Louis-relevant open data alongside the city's own. The GeoParquet was extracted from Overture release 2026-07-22.0; the map tiles reference Overture's own global PMTiles for the same release, the tiles behind [explore.overturemaps.org](https://explore.overturemaps.org/).

184,137 rows; geometry: LineString (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/transportation-infrastructure-and-utilities/overture-transportation/overture-transportation.parquet' LIMIT 5;
```

PMTiles for maps: Overture's own global theme tiles at `https://overturemaps-extras-us-west-2.s3.us-west-2.amazonaws.com/tiles/2026-07-22.0/transportation.pmtiles` (layers `segment`, `connector`), styled by `styles/*.json` — `styles/default.json` is the default. Not clipped to St. Louis: only the Parquet is the extract.

## Key fields

- `overture_type` — segment (roads/rail, lines) or connector (intersections, points)
- `class` — road class (motorway…footway) or rail gauge
- `connectors` — list of connector GERS ids along each segment — the routing graph
- `speed_limits` — nested speed rules, possibly time-scoped

Full schema: `table:columns` in collection.json.

## Quirks

Overture Maps Foundation data, not the city's — see the description. `id` is a GERS id (stable across Overture releases); `sources` records the upstream dataset per feature; struct/list columns (names, sources) are nested Parquet — DuckDB reads them natively. Geometries crossing the bbox edge are clipped to it. Connectors carry almost no attributes; the graph meaning lives on segments.

## Joins

segment.connectors[] = connector.id rebuilds the graph.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/transportation-infrastructure-and-utilities/overture-transportation/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/transportation-infrastructure-and-utilities/overture-transportation/) — rendered README and file listing
- [Overture transportation theme guide](https://docs.overturemaps.org/guides/transportation/) — what the theme models, how Overture builds it, how to query it
- [Overture schema reference: segment](https://docs.overturemaps.org/schema/reference/transportation/segment/) — every field of the `segment` feature type
- [Overture schema reference: connector](https://docs.overturemaps.org/schema/reference/transportation/connector/) — every field of the `connector` feature type

## Provenance

St. Louis-bbox extract of the [Overture Maps Foundation](https://overturemaps.org/) transportation theme, release 2026-07-22.0 (`s3://overturemaps-us-west-2/release/2026-07-22.0/theme=transportation/`) — **not** City of St. Louis data. License: ODbL-1.0 (see [Overture attribution](https://docs.overturemaps.org/attribution/)). Synced 2026-08-14T12:21:16+00:00.
