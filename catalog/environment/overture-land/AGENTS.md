# AGENTS.md — Overture Land

Land features from the Overture base theme: representations of physical land surfaces, sourced from OpenStreetMap — global land derived from the inverse of OSM coastlines, plus translations of OSM `natural` tags (forests, grass, sand, wetlands, peaks, and more), classified by `subtype` and `class`.

Unlike everything else in this catalog, this is **not** City of St. Louis data: it comes from the [Overture Maps Foundation](https://overturemaps.org/), a collaborative project building open, interoperable map data for the world. This collection is a St. Louis extract of that global dataset — everything inside the city's bounding box, which also takes in the Illinois shore of the Mississippi (East St. Louis, Cahokia Heights) — included here to demonstrate how a city's open-data catalog can blend in other St. Louis-relevant open data alongside the city's own. The GeoParquet was extracted from Overture release 2026-07-22.0; the map tiles reference Overture's own global PMTiles for the same release, the tiles behind [explore.overturemaps.org](https://explore.overturemaps.org/).

64,469 rows; geometry: LineString (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/environment/overture-land/overture-land.parquet' LIMIT 5;
```

PMTiles for maps: Overture's own global theme tiles at `https://overturemaps-extras-us-west-2.s3.us-west-2.amazonaws.com/tiles/2026-07-22.0/base.pmtiles` (layers `land`), styled by `styles/*.json` — `styles/default.json` is the default. Not clipped to St. Louis: only the Parquet is the extract.

## Key fields

- `subtype` — tree, forest, shrub, grass, sand, rock, wetland
- `class` — finer class

Full schema: `table:columns` in collection.json.

## Quirks

Overture Maps Foundation data, not the city's — see the description. `id` is a GERS id (stable across Overture releases); `sources` records the upstream dataset per feature; struct/list columns (names, sources) are nested Parquet — DuckDB reads them natively. Geometries crossing the bbox edge are clipped to it. 61k of the 64k features are individual tree points from OSM.

## Joins

Compare tree points with city-trees and forest-park-trees (Forestry's inventories).

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/environment/overture-land/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/environment/overture-land/) — rendered README and file listing
- [Overture base theme guide](https://docs.overturemaps.org/guides/base/)

## Provenance

St. Louis-bbox extract of the [Overture Maps Foundation](https://overturemaps.org/) base theme, release 2026-07-22.0 (`s3://overturemaps-us-west-2/release/2026-07-22.0/theme=base/`) — **not** City of St. Louis data. License: ODbL-1.0 (see [Overture attribution](https://docs.overturemaps.org/attribution/)). Synced 2026-08-14T12:21:16+00:00.
