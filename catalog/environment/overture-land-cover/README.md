# Overture Land Cover

Land cover features from the Overture base theme: the primary natural or artificial surface material covering a land area — vegetation like forests and crops, built environments, and natural surfaces like wetlands or barren ground. Derived from ESA WorldCover, high-resolution optical Earth observation data. Land cover is the physical thing covering the land, while land use is the human use the land is put to. Overture documents this data well: the [base theme guide](https://docs.overturemaps.org/guides/base/) covers what the theme models, how Overture builds it, and how to query it, and the schema reference gives every field of its feature type — [`land_cover`](https://docs.overturemaps.org/schema/reference/base/land_cover/).
Unlike everything else in this catalog, this is **not** City of St. Louis data: it comes from the [Overture Maps Foundation](https://overturemaps.org/), a collaborative project building open, interoperable map data for the world. This collection is a St. Louis extract of that global dataset — everything inside the city's bounding box, which also takes in the Illinois shore of the Mississippi (East St. Louis, Cahokia Heights) — included here to demonstrate how a city's open-data catalog can blend in other St. Louis-relevant open data alongside the city's own. The GeoParquet was extracted from Overture release 2026-07-22.0; the map tiles reference Overture's own global PMTiles for the same release, the tiles behind [explore.overturemaps.org](https://explore.overturemaps.org/). Explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/environment/overture-land-cover/collection.json).

![overture](https://img.shields.io/badge/overture-blue) ![overture-maps](https://img.shields.io/badge/overture--maps-blue) ![base](https://img.shields.io/badge/base-blue) ![st-louis](https://img.shields.io/badge/st--louis-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![land-cover](https://img.shields.io/badge/land--cover-blue)

## Spatial Coverage

- **Bounding Box**: [-90.32051856117901, 38.53199630293254, -90.16630892212817, 38.77434671879855]

## Temporal Coverage

- **Start**: 2026-07-22T00:00:00Z
- **End**: 2026-07-22T00:00:00Z

## Schema

| Column | Type | Description |
|--------|------|-------------|
| id | string | Overture feature ID — per the schema, 'a feature ID. This may be an ID associated with the Global Entity Reference System (GERS) if—and-only-if the feature represents an entity that is part of GERS.' GERS IDs are intended to be stable across Overture's monthly releases, which makes this the key for attaching your own data to an Overture feature and for joining to any other GERS-enabled dataset. See the [GERS overview](https://docs.overturemaps.org/gers/). |
| subtype | string | Type of surface represented: barren, crop, forest, grass, mangrove, moss, shrub, snow, urban or wetland. This is the only classification column in the theme — land cover has no `class`. Derived from ESA WorldCover, high-resolution optical Earth observation data, so it records the physical thing covering the land, not the human use it is put to (that is overture-land-use). Schema reference: [land_cover_subtype](https://docs.overturemaps.org/schema/reference/base/types/land_cover_subtype/). |
| cartography | struct<prominence: int32, min_zoom: int32, max_zoom: int32, sort_key: int32> | Cartographic hints for map-making: `prominence` is Overture's view of the feature's significance on a 1–100 scale, derived from factors including population, capital status, place tags and type; `min_zoom` and `max_zoom` are the recommended Slippy Map tile zooms; `sort_key` is the recommended draw order, with lower numbers drawn on top. Schema reference: [cartographic_hints](https://docs.overturemaps.org/schema/reference/common/cartographic_hints/). |
| sources | list<element: struct<property: string, dataset: string, license: string, record_id: string, update_time: string, confidence: double, between: list<element: double>>> | Per-property provenance. An array of source records, each naming the `property` it covers in JSON Pointer notation plus the source `dataset`, its `license` (an SPDX identifier where one is available; null means contact the data provider for terms), the `record_id` used, an `update_time`, and for ML-derived data a `confidence`. Every feature carries a root-level entry that is the default source for any property without a more specific one. Schema reference: [sources](https://docs.overturemaps.org/schema/reference/common/sources/). |
| version | int32 | Version number of the feature, incremented in each Overture release where the geometry or attributes of this feature changed. Schema reference: [feature_version](https://docs.overturemaps.org/schema/reference/common/feature_version/). |
| geometry | binary | WKB polygon in EPSG:4326 covering the area of a single cover class, derived from ESA WorldCover Earth observation data and clipped to the St. Louis bounding box. |
| bbox | struct<xmin: double, ymin: double, xmax: double, ymax: double> | Covering bounding box (xmin, ymin, xmax, ymax) for the row's geometry. Not an Overture schema column: Overture's own bbox was dropped and this one rebuilt by gpio during conversion, with row-group statistics, so a spatial filter can skip most of the file over the network. |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./overture-land-cover.parquet | 644.0 KB | 12202b8961d7... |
| https://overturemaps-extras-us-west-2.s3.us-west-2.amazonaws.com/tiles/2026-07-22.0/base.pmtiles | 181.9 GB | - |
| ./styles/default.json | 1.9 KB | 12205914fc83... |
| ./thumbnail.png | 366.6 KB | 122054ac21ce... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./overture-land-cover.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[s3://overturemaps-us-west-2/release/2026-07-22.0/theme=base](s3://overturemaps-us-west-2/release/2026-07-22.0/theme=base)

## Processing Notes

Extracted from Overture Maps release 2026-07-22.0 with DuckDB, reading the release's GeoParquet straight from Overture's public S3 bucket:

      s3://overturemaps-us-west-2/release/2026-07-22.0/theme=base/type=land_cover/*.parquet

The extract keeps every feature that intersects the city-boundary collection's bbox (-90.3205, 38.5320, -90.1663, 38.7743) — a rectangle, so the Illinois shore of the Mississippi is included. Geometries that cross the edge of the box are clipped to it (otherwise a feature whose bounding box merely touches St. Louis arrives whole — the full United States polygon, in the divisions theme's case). No other filtering, and no columns were altered; Overture's own `bbox` covering column was dropped and rebuilt during conversion.

Converted to GeoParquet with gpio — zstd compression, Hilbert row order, and a covering bbox column with row-group statistics, so a spatial filter can skip most of the file over the network.

The PMTiles are not built by this mirror: the tiles asset points at Overture's own release-pinned global tiles for the `base` theme — the tiles behind explore.overturemaps.org — served from Overture's public bucket. The styles here select just this collection's layers from them. The tiles cover the whole world, so zooming out shows global data even though the Parquet in this collection is only the St. Louis extract.


## Attribution

Overture Maps Foundation

## License

[ODbL-1.0](https://docs.overturemaps.org/attribution/)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
