# Overture Infrastructure

Infrastructure features from the Overture base theme: real-world infrastructure entities such as bridges, airports, runways, aerialways, communication towers, power lines, and transit features like bus stops, platforms, and stations. All features are pulled from OpenStreetMap and converted to the Overture schema, classified by `subtype` and `class`.
Unlike everything else in this catalog, this is **not** City of St. Louis data: it comes from the [Overture Maps Foundation](https://overturemaps.org/), a collaborative project building open, interoperable map data for the world. This collection is a St. Louis extract of that global dataset — everything inside the city's bounding box, which also takes in the Illinois shore of the Mississippi (East St. Louis, Cahokia Heights) — included here to demonstrate how a city's open-data catalog can blend in other St. Louis-relevant open data alongside the city's own. The GeoParquet was extracted from Overture release 2026-07-22.0; the map tiles reference Overture's own global PMTiles for the same release, the tiles behind [explore.overturemaps.org](https://explore.overturemaps.org/). Explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/transportation-infrastructure-and-utilities/overture-infrastructure/collection.json).

![overture](https://img.shields.io/badge/overture-blue) ![overture-maps](https://img.shields.io/badge/overture--maps-blue) ![base](https://img.shields.io/badge/base-blue) ![st-louis](https://img.shields.io/badge/st--louis-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![infrastructure](https://img.shields.io/badge/infrastructure-blue)

## Spatial Coverage

- **Bounding Box**: [-90.32051856117901, 38.53199630293254, -90.16630892212817, 38.77434671879855]

## Temporal Coverage

- **Start**: 2026-07-22T00:00:00Z
- **End**: 2026-07-22T00:00:00Z

## Schema

| Column | Type | Description |
|--------|------|-------------|
| id | string | Overture feature ID — per the schema, 'a feature ID. This may be an ID associated with the Global Entity Reference System (GERS) if—and-only-if the feature represents an entity that is part of GERS.' GERS IDs are intended to be stable across Overture's monthly releases, which makes this the key for attaching your own data to an Overture feature and for joining to any other GERS-enabled dataset. See [https://docs.overturemaps.org/gers/](https://docs.overturemaps.org/gers/) |
| sources | list<element: struct<property: string, dataset: string, license: string, record_id: string, update_time: string, confidence: double, between: list<element: double>>> | Per-property provenance. An array of source records, each naming the `property` it covers in JSON Pointer notation plus the source `dataset`, its `license` (an SPDX identifier where one is available; null means contact the data provider for terms), the `record_id` used, an `update_time`, and for ML-derived data a `confidence`. Every feature carries a root-level entry that is the default source for any property without a more specific one. |
| names | struct<primary: string, common: map<string, string ('common')>, rules: list<element: struct<variant: string, language: string, perspectives: struct<mode: string, countries: list<element: string>>, value: string, between: list<element: double>, side: string>>> | Names of the feature. `primary` is the most commonly used name; `common` holds translations keyed by IETF BCP-47 language tag; `rules` carries the variants that cannot be expressed as a simple common name (official, alternate, short), each optionally scoped to a `between` range along the geometry or to one `side` of a road. |
| level | int32 | Z-order of the feature, where 0 is visual level — a stacking hint for rendering overlapping features. Not an above-or-below-ground flag: negative values may still be above ground. |
| wikidata | string | Wikidata item ID for the feature if available, as found on [https://www.wikidata.org/](https://www.wikidata.org/) — the OpenStreetMap `wikidata` tag lifted to a top-level Overture property. |
| source_tags | map<string, string ('source_tags')> | Attributes from the original OpenStreetMap feature passed straight through as a string-to-string map. The base theme lifts the tags it models into typed columns (`height`, `surface`, `wikidata` and the rest); whatever is left but still relevant stays here. |
| subtype | string | Broad category of the infrastructure feature: aerialway, airport, barrier, bridge, communication, emergency, manhole, pedestrian, pier, power, quay, recreation, tower, transit, transportation, utility, waste_management or water. |
| class | string | Further classification of the infrastructure type — the finer of the two levels, a long list of values including bus_stop, platform, bus_station, railway_station, subway_station, runway, taxiway, terminal, helipad, bridge, viaduct, power_line, power_tower, substation, communication_tower, water_tower, fire_hydrant, street_lamp, fence, gate, bollard and parking. |
| height | double | Height of the feature in meters, parsed and normalized from the OpenStreetMap `height` tag. |
| surface | string | Surface material of the feature, mostly from the OpenStreetMap `surface` tag with some normalization — asphalt, cobblestone, compacted, concrete, dirt, earth, grass, gravel, ground, paved, paving_stones, sand, sett, unpaved, wood and similar values. |
| version | int32 | Version number of the feature, incremented in each Overture release where the geometry or attributes of this feature changed. |
| geometry | binary | WKB geometry in EPSG:4326. Infrastructure features are points, lines or polygons depending on what they are — a bus stop is a point, a power line or bridge a line, an airport apron a polygon. Geometries crossing the edge of the St. Louis bounding box were clipped to it. |
| bbox | struct<xmin: double, ymin: double, xmax: double, ymax: double> | Covering bounding box (xmin, ymin, xmax, ymax) for the row's geometry. Not an Overture schema column: Overture's own bbox was dropped and this one rebuilt by gpio during conversion, with row-group statistics, so a spatial filter can skip most of the file over the network. |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./overture-infrastructure.parquet | 7.7 MB | 1220e3b509c9... |
| https://overturemaps-extras-us-west-2.s3.us-west-2.amazonaws.com/tiles/2026-07-22.0/base.pmtiles | 181.9 GB | - |
| ./styles/default.json | 4.7 KB | 12206fd5e4b1... |
| ./styles/style-grid.json | 2.6 KB | 12209ed067b6... |
| ./thumbnail.png | 366.3 KB | 1220daeab5f5... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./overture-infrastructure.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[s3://overturemaps-us-west-2/release/2026-07-22.0/theme=base](s3://overturemaps-us-west-2/release/2026-07-22.0/theme=base)

## Processing Notes

Extracted from Overture Maps release 2026-07-22.0 with DuckDB, reading the release's GeoParquet straight from Overture's public S3 bucket:

      s3://overturemaps-us-west-2/release/2026-07-22.0/theme=base/type=infrastructure/*.parquet

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
