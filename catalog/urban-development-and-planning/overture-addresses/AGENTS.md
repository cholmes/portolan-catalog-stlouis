# AGENTS.md — Overture Addresses

Address points from the Overture addresses theme (currently in Alpha). An address represents a physical place through a series of attributes — street number, street name, unit, address levels, postal code, and/or country — together with a point geometry giving the approximate location most commonly associated with it. The theme aggregates open government address datasets, each carrying its own permissive open license, recorded per feature in the `sources` column. Useful for geocoding, validation, and conflation with buildings and places. Overture documents this data well: the [addresses theme guide](https://docs.overturemaps.org/guides/addresses/) covers what the theme models, how Overture builds it, and how to query it, and the schema reference gives every field of its feature type — [`address`](https://docs.overturemaps.org/schema/reference/addresses/address/).

Unlike everything else in this catalog, this is **not** City of St. Louis data: it comes from the [Overture Maps Foundation](https://overturemaps.org/), a collaborative project building open, interoperable map data for the world. This collection is a St. Louis extract of that global dataset — everything inside the city's bounding box, which also takes in the Illinois shore of the Mississippi (East St. Louis, Cahokia Heights) — included here to demonstrate how a city's open-data catalog can blend in other St. Louis-relevant open data alongside the city's own. The GeoParquet was extracted from Overture release 2026-07-22.0. **Coverage caveat:** the theme's aggregated government datasets do not yet include the City of St. Louis itself — the ~99,000 points here are the St. Louis County and Illinois fringe that falls inside the bounding box (Wellston, Ferguson, Jennings, Cahokia, and neighbors), with almost nothing between the city limits. Uniquely among the Overture collections here, the map tiles are built locally from this extract: Overture's own global address tiles are just as empty for St. Louis, and only exist at z14.

99,070 rows; geometry: Point (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/overture-addresses/overture-addresses.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/overture-addresses/overture-addresses.pmtiles` (layer `overture-addresses`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `number` — street number
- `street` — street name
- `postcode` — ZIP
- `unit` — unit where present

Full schema: `table:columns` in collection.json.

## Quirks

Overture Maps Foundation data, not the city's — see the description. `id` is a GERS id (stable across Overture releases); `sources` records the upstream dataset per feature; struct/list columns (names, sources) are nested Parquet — DuckDB reads them natively. Geometries crossing the bbox edge are clipped to it.

## Joins

Spatial join to parcels or overture-buildings; fuzzy-match street+number against city permit tables.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/urban-development-and-planning/overture-addresses/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/overture-addresses/) — rendered README and file listing
- [Overture addresses theme guide](https://docs.overturemaps.org/guides/addresses/) — what the theme models, how Overture builds it, how to query it
- [Overture schema reference: address](https://docs.overturemaps.org/schema/reference/addresses/address/) — every field of the `address` feature type

## Provenance

St. Louis-bbox extract of the [Overture Maps Foundation](https://overturemaps.org/) addresses theme, release 2026-07-22.0 (`s3://overturemaps-us-west-2/release/2026-07-22.0/theme=addresses/`) — **not** City of St. Louis data. License: other (see [Overture attribution](https://docs.overturemaps.org/attribution/)). Synced 2026-08-14T12:21:16+00:00.
