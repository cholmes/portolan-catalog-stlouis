# Overture Buildings

Building footprints and building parts from the Overture Maps buildings theme, which describes human-made structures with roofs or interior spaces that are permanently or semi-permanently in one place. Overture's goal is to provide the world's most comprehensive set of building structures compiled from the best available open data sources. Where known, buildings carry height, number of floors, and facade and roof attributes, supporting 2D and 3D visualization, data enrichment via GERS IDs, and spatial analysis. Both feature types are merged here, with an `overture_type` column telling buildings from building parts. Overture documents this data well: the [buildings theme guide](https://docs.overturemaps.org/guides/buildings/) covers what the theme models, how Overture builds it, and how to query it, and the schema reference gives every field of the feature types merged here — [`building`](https://docs.overturemaps.org/schema/reference/buildings/building/), [`building_part`](https://docs.overturemaps.org/schema/reference/buildings/building_part/).
Unlike everything else in this catalog, this is **not** City of St. Louis data: it comes from the [Overture Maps Foundation](https://overturemaps.org/), a collaborative project building open, interoperable map data for the world. This collection is a St. Louis extract of that global dataset — everything inside the city's bounding box, which also takes in the Illinois shore of the Mississippi (East St. Louis, Cahokia Heights) — included here to demonstrate how a city's open-data catalog can blend in other St. Louis-relevant open data alongside the city's own. The GeoParquet was extracted from Overture release 2026-07-22.0; the map tiles reference Overture's own global PMTiles for the same release, the tiles behind [explore.overturemaps.org](https://explore.overturemaps.org/). Explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/urban-development-and-planning/overture-buildings/collection.json).

![overture](https://img.shields.io/badge/overture-blue) ![overture-maps](https://img.shields.io/badge/overture--maps-blue) ![buildings](https://img.shields.io/badge/buildings-blue) ![st-louis](https://img.shields.io/badge/st--louis-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![building](https://img.shields.io/badge/building-blue) ![building-part](https://img.shields.io/badge/building--part-blue)

## Spatial Coverage

- **Bounding Box**: [-90.32051856117901, 38.53199630293254, -90.16630892212817, 38.77434671879855]

## Temporal Coverage

- **Start**: 2026-07-22T00:00:00Z
- **End**: 2026-07-22T00:00:00Z

## Schema

| Column | Type | Description |
|--------|------|-------------|
| id | string | Overture feature ID — per the schema, 'a feature ID. This may be an ID associated with the Global Entity Reference System (GERS) if—and-only-if the feature represents an entity that is part of GERS.' GERS IDs are intended to be stable across Overture's monthly releases, which makes this the key for attaching your own data to an Overture feature and for joining to any other GERS-enabled dataset. See the [GERS overview](https://docs.overturemaps.org/gers/). |
| names | struct<primary: string, common: map<string, string ('common')>, rules: list<element: struct<variant: string, language: string, perspectives: struct<mode: string, countries: list<element: string>>, value: string, between: list<element: double>, side: string>>> | Names of the feature. `primary` is the most commonly used name; `common` holds translations keyed by IETF BCP-47 language tag; `rules` carries the variants that cannot be expressed as a simple common name (official, alternate, short), each optionally scoped to a `between` range along the geometry or to one `side` of a road. Schema reference: [names](https://docs.overturemaps.org/schema/reference/common/names/). |
| sources | list<element: struct<property: string, dataset: string, license: string, record_id: string, update_time: string, confidence: double, between: list<element: double>>> | Per-property provenance. An array of source records, each naming the `property` it covers in JSON Pointer notation plus the source `dataset`, its `license` (an SPDX identifier where one is available; null means contact the data provider for terms), the `record_id` used, an `update_time`, and for ML-derived data a `confidence`. Every feature carries a root-level entry that is the default source for any property without a more specific one. Schema reference: [sources](https://docs.overturemaps.org/schema/reference/common/sources/). |
| level | int32 | Z-order of the feature, where 0 is visual level — a stacking hint for rendering overlapping features. Not an above-or-below-ground flag: negative values may still be above ground. Schema reference: [level](https://docs.overturemaps.org/schema/reference/common/level/). |
| height | double | Height of the building or part in meters — the distance from its lowest point to its highest point. |
| min_height | double | The height of the bottom of the building or part in meters, used when it starts above ground level. |
| is_underground | bool | Whether the entire building or part is completely below ground. Useful for rendering, which typically omits these or styles them differently because they are not visible above ground. Distinct from `level`, which is a z-ordering hint whose negative values may still be above ground. |
| num_floors | int32 | Number of above-ground floors of the building or part. |
| num_floors_underground | int32 | Number of below-ground floors of the building or part. |
| min_floor | int32 | The 'start' floor of the building or part, indicating that it floats with its bottom-most floor above ground level — usually because it is part of a larger building where other parts do reach the ground, such as a wing bridging over an entry road into a courtyard. Sometimes populated when `min_height` is missing, in which case it can stand in for it. |
| subtype | string | A broad category of the building type or purpose; where the current use of the building does not match the built purpose, the subtype represents the current use. One of agricultural, civic, commercial, education, entertainment, industrial, medical, military, outbuilding, religious, residential, service, transportation. Schema reference: [building_subtype](https://docs.overturemaps.org/schema/reference/buildings/types/building_subtype/). |
| class | string | Further delineation of the building's built purpose — the finer of the two classification levels, a long list of values including house, detached, apartments, terrace, garage, shed, retail, office, warehouse, factory, church, school, university, hospital, hotel, stadium, parking and hangar. Schema reference: [building_class](https://docs.overturemaps.org/schema/reference/buildings/types/building_class/). |
| facade_color | string | The color of the facade of the building or part, as a name or a hexadecimal color triplet. |
| facade_material | string | The outer surface material of the building facade: brick, cement_block, clay, concrete, glass, metal, plaster, plastic, stone, timber_framing or wood. Schema reference: [facade_material](https://docs.overturemaps.org/schema/reference/buildings/types/facade_material/). |
| roof_material | string | The outermost material of the roof: concrete, copper, eternit, glass, grass, gravel, metal, plastic, roof_tiles, slate, solar_panels, thatch, tar_paper or wood. Schema reference: [roof_material](https://docs.overturemaps.org/schema/reference/buildings/types/roof_material/). |
| roof_shape | string | The shape of the roof: dome, flat, gabled, gambrel, half_hipped, hipped, mansard, onion, pyramidal, round, saltbox, sawtooth, skillion or spherical. Schema reference: [roof_shape](https://docs.overturemaps.org/schema/reference/buildings/types/roof_shape/). |
| roof_direction | double | Bearing of the roof ridge line, in degrees from 0 up to 360. |
| roof_orientation | string | Orientation of the roof shape relative to the footprint shape — `along` or `across`. Schema reference: [roof_orientation](https://docs.overturemaps.org/schema/reference/buildings/types/roof_orientation/). |
| roof_color | string | The color of the roof of the building or part, as a name or a hexadecimal color triplet. |
| roof_height | double | Height of the roof in meters — the distance from the base of the roof to its highest point. |
| has_parts | bool | Flag indicating whether the building has parts. Where true, the matching part rows in this collection (`overture_type` = 'building_part') carry this building's id in `building_id`. |
| version | int32 | Version number of the feature, incremented in each Overture release where the geometry or attributes of this feature changed. Schema reference: [feature_version](https://docs.overturemaps.org/schema/reference/common/feature_version/). |
| overture_type | string | Which of the buildings theme's two feature types this row is — `building` (a whole structure) or `building_part` (a distinct section of one, carrying its own height, materials or roof shape). Not an Overture schema column: this mirror merges the theme's feature types into one collection and records the type here. Schema reference: [building](https://docs.overturemaps.org/schema/reference/buildings/building/), [building_part](https://docs.overturemaps.org/schema/reference/buildings/building_part/). |
| geometry | binary | Building geometry as WKB in EPSG:4326: a building's footprint, or its roofprint where the outline was traced from aerial or satellite imagery. A building part's geometry is the polygon of that part. Polygons crossing the edge of the St. Louis bounding box were clipped to it. |
| building_id | string | On a building part, the id of the building the part belongs to; null on whole-building rows. Join it back to `id` to assemble a building and its parts. Schema reference: [building_part](https://docs.overturemaps.org/schema/reference/buildings/building_part/). |
| bbox | struct<xmin: double, ymin: double, xmax: double, ymax: double> | Covering bounding box (xmin, ymin, xmax, ymax) for the row's geometry. Not an Overture schema column: Overture's own bbox was dropped and this one rebuilt by gpio during conversion, with row-group statistics, so a spatial filter can skip most of the file over the network. |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./overture-buildings.parquet | 26.0 MB | 12204eb40c6d... |
| https://overturemaps-extras-us-west-2.s3.us-west-2.amazonaws.com/tiles/2026-07-22.0/buildings.pmtiles | 167.1 GB | - |
| ./styles/default.json | 2.6 KB | 12201668641d... |
| ./styles/style-explorer.json | 1.3 KB | 1220d4269665... |
| ./styles/style-subtype.json | 2.3 KB | 1220798fa302... |
| ./thumbnail.png | 401.4 KB | 1220248a7001... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./overture-buildings.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[s3://overturemaps-us-west-2/release/2026-07-22.0/theme=buildings](s3://overturemaps-us-west-2/release/2026-07-22.0/theme=buildings)

## Processing Notes

Extracted from Overture Maps release 2026-07-22.0 with DuckDB, reading the release's GeoParquet straight from Overture's public S3 bucket:

      s3://overturemaps-us-west-2/release/2026-07-22.0/theme=buildings/type=building/*.parquet
      s3://overturemaps-us-west-2/release/2026-07-22.0/theme=buildings/type=building_part/*.parquet

The extract keeps every feature that intersects the city-boundary collection's bbox (-90.3205, 38.5320, -90.1663, 38.7743) — a rectangle, so the Illinois shore of the Mississippi is included. Geometries that cross the edge of the box are clipped to it (otherwise a feature whose bounding box merely touches St. Louis arrives whole — the full United States polygon, in the divisions theme's case). No other filtering, and no columns were altered; Overture's own `bbox` covering column was dropped and rebuilt during conversion.

The theme's 2 feature types (building, building_part) are merged into one collection with an `overture_type` column recording which type each feature is.

Converted to GeoParquet with gpio — zstd compression, Hilbert row order, and a covering bbox column with row-group statistics, so a spatial filter can skip most of the file over the network.

The PMTiles are not built by this mirror: the tiles asset points at Overture's own release-pinned global tiles for the `buildings` theme — the tiles behind explore.overturemaps.org — served from Overture's public bucket. The styles here select just this collection's layers from them. The tiles cover the whole world, so zooming out shows global data even though the Parquet in this collection is only the St. Louis extract.


## Attribution

Overture Maps Foundation

## License

[ODbL-1.0](https://docs.overturemaps.org/attribution/)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
