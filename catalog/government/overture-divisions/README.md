# Overture Divisions

Point, line, and polygon representations of human settlements from the Overture divisions theme: recognized areas for governance, culture, or organization, from countries and regions down to counties, cities, and neighborhoods. Three feature types are merged here with an `overture_type` column: `division` (label points with population and hierarchy), `division_area` (the land or maritime polygon belonging to a division), and `division_boundary` (shared borders between divisions). For the St. Louis box that means the city itself, surrounding counties and municipalities on both sides of the river, and Overture's neighborhood set.
Unlike everything else in this catalog, this is **not** City of St. Louis data: it comes from the [Overture Maps Foundation](https://overturemaps.org/), a collaborative project building open, interoperable map data for the world. This collection is a St. Louis extract of that global dataset — everything inside the city's bounding box, which also takes in the Illinois shore of the Mississippi (East St. Louis, Cahokia Heights) — included here to demonstrate how a city's open-data catalog can blend in other St. Louis-relevant open data alongside the city's own. The GeoParquet was extracted from Overture release 2026-07-22.0; the map tiles reference Overture's own global PMTiles for the same release, the tiles behind [explore.overturemaps.org](https://explore.overturemaps.org/). Explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/government/overture-divisions/collection.json).

![overture](https://img.shields.io/badge/overture-blue) ![overture-maps](https://img.shields.io/badge/overture--maps-blue) ![divisions](https://img.shields.io/badge/divisions-blue) ![st-louis](https://img.shields.io/badge/st--louis-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![division](https://img.shields.io/badge/division-blue) ![division-area](https://img.shields.io/badge/division--area-blue) ![division-boundary](https://img.shields.io/badge/division--boundary-blue)

## Spatial Coverage

- **Bounding Box**: [-90.32051856117901, 38.53199630293254, -90.16630892212817, 38.77434671879855]

## Temporal Coverage

- **Start**: 2026-07-22T00:00:00Z
- **End**: 2026-07-22T00:00:00Z

## Schema

| Column | Type | Description |
|--------|------|-------------|
| id | string |  |
| country | string |  |
| sources | list<element: struct<property: string, dataset: string, license: string, record_id: string, update_time: string, confidence: double, between: list<element: double>>> |  |
| subtype | string |  |
| admin_level | int32 |  |
| class | string |  |
| names | struct<primary: string, common: map<string, string ('common')>, rules: list<element: struct<variant: string, language: string, perspectives: struct<mode: string, countries: list<element: string>>, value: string, between: list<element: double>, side: string>>> |  |
| wikidata | string |  |
| perspectives | struct<mode: string, countries: list<element: string>> |  |
| local_type | map<string, string ('local_type')> |  |
| region | string |  |
| hierarchies | list<element: list<element: struct<division_id: string, subtype: string, name: string>>> |  |
| parent_division_id | string |  |
| norms | struct<driving_side: string> |  |
| population | int32 |  |
| capital_division_ids | list<element: string> |  |
| capital_of_divisions | list<element: struct<division_id: string, subtype: string>> |  |
| cartography | struct<prominence: int32, min_zoom: int32, max_zoom: int32, sort_key: int32> |  |
| version | int32 |  |
| overture_type | string |  |
| geometry | binary |  |
| is_land | bool |  |
| is_territorial | bool |  |
| division_id | string |  |
| division_ids | list<element: string> |  |
| is_disputed | bool |  |
| bbox | struct<xmin: double, ymin: double, xmax: double, ymax: double> |  |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./overture-divisions.parquet | 162.0 KB | 1220451a1345... |
| https://overturemaps-extras-us-west-2.s3.us-west-2.amazonaws.com/tiles/2026-07-22.0/divisions.pmtiles | 18.2 GB | - |
| ./styles/default.json | 2.6 KB | 1220326f6e1f... |
| ./styles/style-neighborhoods.json | 2.5 KB | 1220fcde50ef... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./overture-divisions.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[s3://overturemaps-us-west-2/release/2026-07-22.0/theme=divisions](s3://overturemaps-us-west-2/release/2026-07-22.0/theme=divisions)

## Processing Notes

Extracted from Overture Maps release 2026-07-22.0 with DuckDB, reading the release's GeoParquet straight from Overture's public S3 bucket:

      s3://overturemaps-us-west-2/release/2026-07-22.0/theme=divisions/type=division/*.parquet
      s3://overturemaps-us-west-2/release/2026-07-22.0/theme=divisions/type=division_area/*.parquet
      s3://overturemaps-us-west-2/release/2026-07-22.0/theme=divisions/type=division_boundary/*.parquet

The extract keeps every feature that intersects the city-boundary collection's bbox (-90.3205, 38.5320, -90.1663, 38.7743) — a rectangle, so the Illinois shore of the Mississippi is included. Geometries that cross the edge of the box are clipped to it (otherwise a feature whose bounding box merely touches St. Louis arrives whole — the full United States polygon, in the divisions theme's case). No other filtering, and no columns were altered; Overture's own `bbox` covering column was dropped and rebuilt during conversion.

The theme's 3 feature types (division, division_area, division_boundary) are merged into one collection with an `overture_type` column recording which type each feature is.

Converted to GeoParquet with gpio — zstd compression, Hilbert row order, and a covering bbox column with row-group statistics, so a spatial filter can skip most of the file over the network.

The PMTiles are not built by this mirror: the tiles asset points at Overture's own release-pinned global tiles for the `divisions` theme — the tiles behind explore.overturemaps.org — served from Overture's public bucket. The styles here select just this collection's layers from them. The tiles cover the whole world, so zooming out shows global data even though the Parquet in this collection is only the St. Louis extract.


## Attribution

Overture Maps Foundation

## License

[ODbL-1.0](https://docs.overturemaps.org/attribution/)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
