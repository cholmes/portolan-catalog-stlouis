# AGENTS.md — Overture Places

Point representations of real-world entities from the Overture places theme: schools, businesses, hospitals, religious organizations, landmarks, and much more. Overture defines a place as a concrete, physically identifiable, stationary destination in a publicly observable space. The theme is published under the CDLA Permissive 2.0 and Apache 2.0 licenses, contains no OpenStreetMap data, and carries none of the share-alike obligations of the ODbL. Each place has a category from Overture's taxonomy and a confidence score for how certain Overture is that the place exists and is current. Overture documents this data well: the [places theme guide](https://docs.overturemaps.org/guides/places/) covers what the theme models, how Overture builds it, and how to query it, and the schema reference gives every field of its feature type — [`place`](https://docs.overturemaps.org/schema/reference/places/place/).

Unlike everything else in this catalog, this is **not** City of St. Louis data: it comes from the [Overture Maps Foundation](https://overturemaps.org/), a collaborative project building open, interoperable map data for the world. This collection is a St. Louis extract of that global dataset — everything inside the city's bounding box, which also takes in the Illinois shore of the Mississippi (East St. Louis, Cahokia Heights) — included here to demonstrate how a city's open-data catalog can blend in other St. Louis-relevant open data alongside the city's own. The GeoParquet was extracted from Overture release 2026-07-22.0; the map tiles reference Overture's own global PMTiles for the same release, the tiles behind [explore.overturemaps.org](https://explore.overturemaps.org/).

20,968 rows; geometry: Point (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/business-and-industry/overture-places/overture-places.parquet' LIMIT 5;
```

PMTiles for maps: Overture's own global theme tiles at `https://overturemaps-extras-us-west-2.s3.us-west-2.amazonaws.com/tiles/2026-07-22.0/places.pmtiles` (layers `place`), styled by `styles/*.json` — `styles/default.json` is the default. Not clipped to St. Louis: only the Parquet is the extract.

## Key fields

- `basic_category` — flat category (restaurant, bar…)
- `confidence` — 0-1 — Overture's certainty the place exists
- `operating_status` — open / closed markers

Full schema: `table:columns` in collection.json.

## Quirks

Overture Maps Foundation data, not the city's — see the description. `id` is a GERS id (stable across Overture releases); `sources` records the upstream dataset per feature; struct/list columns (names, sources) are nested Parquet — DuckDB reads them natively. Geometries crossing the bbox edge are clipped to it. Compare against the city's business-licenses collection for ground truth.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/business-and-industry/overture-places/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/business-and-industry/overture-places/) — rendered README and file listing
- [Overture places theme guide](https://docs.overturemaps.org/guides/places/) — what the theme models, how Overture builds it, how to query it
- [Overture schema reference: place](https://docs.overturemaps.org/schema/reference/places/place/) — every field of the `place` feature type

## Provenance

St. Louis-bbox extract of the [Overture Maps Foundation](https://overturemaps.org/) places theme, release 2026-07-22.0 (`s3://overturemaps-us-west-2/release/2026-07-22.0/theme=places/`) — **not** City of St. Louis data. License: other (see [Overture attribution](https://docs.overturemaps.org/attribution/)). Synced 2026-08-14T12:21:16+00:00.
