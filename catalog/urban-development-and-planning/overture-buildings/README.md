# Overture Buildings

Building footprints and building parts from the Overture Maps buildings theme, which describes human-made structures with roofs or interior spaces that are permanently or semi-permanently in one place. Overture's goal is to provide the world's most comprehensive set of building structures compiled from the best available open data sources. Where known, buildings carry height, number of floors, and facade and roof attributes, supporting 2D and 3D visualization, data enrichment via GERS IDs, and spatial analysis. Both feature types are merged here, with an `overture_type` column telling buildings from building parts.
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
| id | string |  |
| names | struct<primary: string, common: map<string, string ('common')>, rules: list<element: struct<variant: string, language: string, perspectives: struct<mode: string, countries: list<element: string>>, value: string, between: list<element: double>, side: string>>> |  |
| sources | list<element: struct<property: string, dataset: string, license: string, record_id: string, update_time: string, confidence: double, between: list<element: double>>> |  |
| level | int32 |  |
| height | double |  |
| min_height | double |  |
| is_underground | bool |  |
| num_floors | int32 |  |
| num_floors_underground | int32 |  |
| min_floor | int32 |  |
| subtype | string |  |
| class | string |  |
| facade_color | string |  |
| facade_material | string |  |
| roof_material | string |  |
| roof_shape | string |  |
| roof_direction | double |  |
| roof_orientation | string |  |
| roof_color | string |  |
| roof_height | double |  |
| has_parts | bool |  |
| version | int32 |  |
| overture_type | string |  |
| geometry | binary |  |
| building_id | string |  |
| bbox | struct<xmin: double, ymin: double, xmax: double, ymax: double> |  |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./overture-buildings.parquet | 26.0 MB | 12204eb40c6d... |
| https://overturemaps-extras-us-west-2.s3.us-west-2.amazonaws.com/tiles/2026-07-22.0/buildings.pmtiles | 167.1 GB | - |
| ./styles/default.json | 2.6 KB | 12201668641d... |
| ./styles/style-explorer.json | 1.3 KB | 1220d4269665... |
| ./styles/style-subtype.json | 2.3 KB | 1220798fa302... |

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
