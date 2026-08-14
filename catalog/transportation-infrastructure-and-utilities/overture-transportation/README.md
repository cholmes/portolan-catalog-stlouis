# Overture Transportation

The Overture transportation theme is a model of how the world's roads, rails, and waterways connect: traversable segments (roads, railways, ferries) and connectors (intersections) representing how people and objects travel, built from OpenStreetMap and enhanced with data from TomTom and other local and regional authoritative sources. It is simple at its core but expressive enough to capture speed limits that change by time of day, one-way streets that allow buses the wrong way, and weight-restricted bridges. Both feature types are merged here, with an `overture_type` column telling segments from connectors.
Unlike everything else in this catalog, this is **not** City of St. Louis data: it comes from the [Overture Maps Foundation](https://overturemaps.org/), a collaborative project building open, interoperable map data for the world. This collection is a St. Louis extract of that global dataset — everything inside the city's bounding box, which also takes in the Illinois shore of the Mississippi (East St. Louis, Cahokia Heights) — included here to demonstrate how a city's open-data catalog can blend in other St. Louis-relevant open data alongside the city's own. The GeoParquet was extracted from Overture release 2026-07-22.0; the map tiles reference Overture's own global PMTiles for the same release, the tiles behind [explore.overturemaps.org](https://explore.overturemaps.org/). Explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/transportation-infrastructure-and-utilities/overture-transportation/collection.json).

![overture](https://img.shields.io/badge/overture-blue) ![overture-maps](https://img.shields.io/badge/overture--maps-blue) ![transportation](https://img.shields.io/badge/transportation-blue) ![st-louis](https://img.shields.io/badge/st--louis-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![segment](https://img.shields.io/badge/segment-blue) ![connector](https://img.shields.io/badge/connector-blue)

## Spatial Coverage

- **Bounding Box**: [-90.32051856117901, 38.53199630293254, -90.16630892212817, 38.77434671879855]

## Temporal Coverage

- **Start**: 2026-07-22T00:00:00Z
- **End**: 2026-07-22T00:00:00Z

## Schema

| Column | Type | Description |
|--------|------|-------------|
| id | string |  |
| names | struct<primary: string, common: map<string, string ('common')>, rules: list<element: struct<variant: string, language: string, perspectives: struct<mode: string, countries: list<element: string>>, value: string, between: list<element: double>, side: string>>> |  |
| subtype | string |  |
| class | string |  |
| subclass | string |  |
| subclass_rules | list<element: struct<value: string, between: list<element: double>>> |  |
| connectors | list<element: struct<connector_id: string, at: double>> |  |
| road_surface | list<element: struct<value: string, between: list<element: double>>> |  |
| road_flags | list<element: struct<values: list<element: string>, between: list<element: double>>> |  |
| rail_flags | list<element: struct<values: list<element: string>, between: list<element: double>>> |  |
| width_rules | list<element: struct<value: double, between: list<element: double>>> |  |
| level_rules | list<element: struct<value: int32, between: list<element: double>>> |  |
| access_restrictions | list<element: struct<access_type: string, when: struct<during: string, heading: string, using: list<element: string>, recognized: list<element: string>, mode: list<element: string>, vehicle: list<element: struct<dimension: string, comparison: string, value: double, unit: string>>>, between: list<element: double>>> |  |
| speed_limits | list<element: struct<min_speed: struct<value: int32, unit: string>, max_speed: struct<value: int32, unit: string>, is_max_speed_variable: bool, when: struct<during: string, heading: string, using: list<element: string>, recognized: list<element: string>, mode: list<element: string>, vehicle: list<element: struct<dimension: string, comparison: string, value: double, unit: string>>>, between: list<element: double>>> |  |
| prohibited_transitions | list<element: struct<sequence: list<element: struct<connector_id: string, segment_id: string>>, final_heading: string, when: struct<heading: string, during: string, using: list<element: string>, recognized: list<element: string>, mode: list<element: string>, vehicle: list<element: struct<dimension: string, comparison: string, value: double, unit: string>>>, between: list<element: double>>> |  |
| routes | list<element: struct<name: string, network: string, ref: string, symbol: string, wikidata: string, between: list<element: double>>> |  |
| destinations | list<element: struct<labels: list<element: struct<value: string, type: string>>, symbols: list<element: string>, from_connector_id: string, to_segment_id: string, to_connector_id: string, when: struct<heading: string>, final_heading: string>> |  |
| sources | list<element: struct<property: string, dataset: string, license: string, record_id: string, update_time: string, confidence: double, between: list<element: double>>> |  |
| version | int32 |  |
| overture_type | string |  |
| geometry | binary |  |
| bbox | struct<xmin: double, ymin: double, xmax: double, ymax: double> |  |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./overture-transportation.parquet | 20.8 MB | 122021d42923... |
| https://overturemaps-extras-us-west-2.s3.us-west-2.amazonaws.com/tiles/2026-07-22.0/transportation.pmtiles | 121.4 GB | - |
| ./styles/default.json | 3.1 KB | 1220c4e55069... |
| ./styles/style-network.json | 1.2 KB | 12205149fb8d... |
| ./styles/style-topology.json | 1.2 KB | 12206538e9c1... |
| ./thumbnail.png | 447.0 KB | 1220a4fb9705... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./overture-transportation.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[s3://overturemaps-us-west-2/release/2026-07-22.0/theme=transportation](s3://overturemaps-us-west-2/release/2026-07-22.0/theme=transportation)

## Processing Notes

Extracted from Overture Maps release 2026-07-22.0 with DuckDB, reading the release's GeoParquet straight from Overture's public S3 bucket:

      s3://overturemaps-us-west-2/release/2026-07-22.0/theme=transportation/type=segment/*.parquet
      s3://overturemaps-us-west-2/release/2026-07-22.0/theme=transportation/type=connector/*.parquet

The extract keeps every feature that intersects the city-boundary collection's bbox (-90.3205, 38.5320, -90.1663, 38.7743) — a rectangle, so the Illinois shore of the Mississippi is included. Geometries that cross the edge of the box are clipped to it (otherwise a feature whose bounding box merely touches St. Louis arrives whole — the full United States polygon, in the divisions theme's case). No other filtering, and no columns were altered; Overture's own `bbox` covering column was dropped and rebuilt during conversion.

The theme's 2 feature types (segment, connector) are merged into one collection with an `overture_type` column recording which type each feature is.

Converted to GeoParquet with gpio — zstd compression, Hilbert row order, and a covering bbox column with row-group statistics, so a spatial filter can skip most of the file over the network.

The PMTiles are not built by this mirror: the tiles asset points at Overture's own release-pinned global tiles for the `transportation` theme — the tiles behind explore.overturemaps.org — served from Overture's public bucket. The styles here select just this collection's layers from them. The tiles cover the whole world, so zooming out shows global data even though the Parquet in this collection is only the St. Louis extract.


## Attribution

Overture Maps Foundation

## License

[ODbL-1.0](https://docs.overturemaps.org/attribution/)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
