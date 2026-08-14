# Overture Places

Point representations of real-world entities from the Overture places theme: schools, businesses, hospitals, religious organizations, landmarks, and much more. Overture defines a place as a concrete, physically identifiable, stationary destination in a publicly observable space. The theme is published under the CDLA Permissive 2.0 and Apache 2.0 licenses, contains no OpenStreetMap data, and carries none of the share-alike obligations of the ODbL. Each place has a category from Overture's taxonomy and a confidence score for how certain Overture is that the place exists and is current.
Unlike everything else in this catalog, this is **not** City of St. Louis data: it comes from the [Overture Maps Foundation](https://overturemaps.org/), a collaborative project building open, interoperable map data for the world. This collection is a St. Louis extract of that global dataset — everything inside the city's bounding box, which also takes in the Illinois shore of the Mississippi (East St. Louis, Cahokia Heights) — included here to demonstrate how a city's open-data catalog can blend in other St. Louis-relevant open data alongside the city's own. The GeoParquet was extracted from Overture release 2026-07-22.0; the map tiles reference Overture's own global PMTiles for the same release, the tiles behind [explore.overturemaps.org](https://explore.overturemaps.org/). Explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/business-and-industry/overture-places/collection.json).

![overture](https://img.shields.io/badge/overture-blue) ![overture-maps](https://img.shields.io/badge/overture--maps-blue) ![places](https://img.shields.io/badge/places-blue) ![st-louis](https://img.shields.io/badge/st--louis-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![place](https://img.shields.io/badge/place-blue)

## Spatial Coverage

- **Bounding Box**: [-90.32051595, 38.532093, -90.16632, 38.77434060906825]

## Temporal Coverage

- **Start**: 2026-07-22T00:00:00Z
- **End**: 2026-07-22T00:00:00Z

## Schema

| Column | Type | Description |
|--------|------|-------------|
| id | string |  |
| categories | struct<primary: string, alternate: list<element: string>> |  |
| confidence | double |  |
| websites | list<element: string> |  |
| emails | list<element: string> |  |
| socials | list<element: string> |  |
| phones | list<element: string> |  |
| brand | struct<wikidata: string, names: struct<primary: string, common: map<string, string ('common')>, rules: list<element: struct<variant: string, language: string, perspectives: struct<mode: string, countries: list<element: string>>, value: string, between: list<element: double>, side: string>>>> |  |
| addresses | list<element: struct<freeform: string, locality: string, postcode: string, region: string, country: string>> |  |
| names | struct<primary: string, common: map<string, string ('common')>, rules: list<element: struct<variant: string, language: string, perspectives: struct<mode: string, countries: list<element: string>>, value: string, between: list<element: double>, side: string>>> |  |
| sources | list<element: struct<property: string, dataset: string, license: string, record_id: string, update_time: string, confidence: double, between: list<element: double>>> |  |
| operating_status | string |  |
| basic_category | string |  |
| taxonomy | struct<primary: string, hierarchy: list<element: string>, alternates: list<element: string>> |  |
| version | int32 |  |
| geometry | binary |  |
| bbox | struct<xmin: double, ymin: double, xmax: double, ymax: double> |  |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./overture-places.parquet | 4.6 MB | 12201d35c925... |
| https://overturemaps-extras-us-west-2.s3.us-west-2.amazonaws.com/tiles/2026-07-22.0/places.pmtiles | 18.0 GB | - |
| ./styles/default.json | 3.1 KB | 1220f48c03fd... |
| ./styles/style-confidence.json | 1.6 KB | 12206b968f68... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./overture-places.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[s3://overturemaps-us-west-2/release/2026-07-22.0/theme=places](s3://overturemaps-us-west-2/release/2026-07-22.0/theme=places)

## Processing Notes

Extracted from Overture Maps release 2026-07-22.0 with DuckDB, reading the release's GeoParquet straight from Overture's public S3 bucket:

      s3://overturemaps-us-west-2/release/2026-07-22.0/theme=places/type=place/*.parquet

The extract keeps every feature that intersects the city-boundary collection's bbox (-90.3205, 38.5320, -90.1663, 38.7743) — a rectangle, so the Illinois shore of the Mississippi is included. Geometries that cross the edge of the box are clipped to it (otherwise a feature whose bounding box merely touches St. Louis arrives whole — the full United States polygon, in the divisions theme's case). No other filtering, and no columns were altered; Overture's own `bbox` covering column was dropped and rebuilt during conversion.

Converted to GeoParquet with gpio — zstd compression, Hilbert row order, and a covering bbox column with row-group statistics, so a spatial filter can skip most of the file over the network.

The PMTiles are not built by this mirror: the tiles asset points at Overture's own release-pinned global tiles for the `places` theme — the tiles behind explore.overturemaps.org — served from Overture's public bucket. The styles here select just this collection's layers from them. The tiles cover the whole world, so zooming out shows global data even though the Parquet in this collection is only the St. Louis extract.


## Attribution

Overture Maps Foundation

## License

[other](https://docs.overturemaps.org/attribution/)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
