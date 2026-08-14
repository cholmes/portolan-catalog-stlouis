# AGENTS.md — Overture Addresses

Address points from the Overture addresses theme (currently in Alpha). An address represents a physical place through a series of attributes — street number, street name, unit, address levels, postal code, and/or country — together with a point geometry giving the approximate location most commonly associated with it. The theme aggregates open government address datasets, each carrying its own permissive open license, recorded per feature in the `sources` column. Useful for geocoding, validation, and conflation with buildings and places.

Unlike everything else in this catalog, this is **not** City of St. Louis data: it comes from the [Overture Maps Foundation](https://overturemaps.org/), a collaborative project building open, interoperable map data for the world. This collection is a St. Louis extract of that global dataset — everything inside the city's bounding box, which also takes in the Illinois shore of the Mississippi (East St. Louis, Cahokia Heights) — included here to demonstrate how a city's open-data catalog can blend in other St. Louis-relevant open data alongside the city's own. The GeoParquet was extracted from Overture release 2026-07-22.0; the map tiles reference Overture's own global PMTiles for the same release, the tiles behind [explore.overturemaps.org](https://explore.overturemaps.org/).

99,070 rows; geometry: Point (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/overture-addresses/overture-addresses.parquet' LIMIT 5;
```

PMTiles for maps: Overture's own global theme tiles at `https://overturemaps-extras-us-west-2.s3.us-west-2.amazonaws.com/tiles/2026-07-22.0/addresses.pmtiles` (layers `address`), styled by `styles/*.json` — `styles/default.json` is the default. Not clipped to St. Louis: only the Parquet is the extract.

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
- [Overture addresses theme guide](https://docs.overturemaps.org/guides/addresses/)

## Provenance

St. Louis-bbox extract of the [Overture Maps Foundation](https://overturemaps.org/) addresses theme, release 2026-07-22.0 (`s3://overturemaps-us-west-2/release/2026-07-22.0/theme=addresses/`) — **not** City of St. Louis data. License: other (see [Overture attribution](https://docs.overturemaps.org/attribution/)). Synced 2026-08-14T11:21:05+00:00.
