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
| id | string | Overture feature ID — per the schema, 'a feature ID. This may be an ID associated with the Global Entity Reference System (GERS) if—and-only-if the feature represents an entity that is part of GERS.' GERS IDs are intended to be stable across Overture's monthly releases, which makes this the key for attaching your own data to an Overture feature and for joining to any other GERS-enabled dataset. See [https://docs.overturemaps.org/gers/](https://docs.overturemaps.org/gers/) |
| categories | struct<primary: string, alternate: list<element: string>> | The place's categories in Overture's original category taxonomy: `primary` is the main category (it can be empty) and `alternate` lists further categories that also apply, for a place that is, say, both a book store and a coffee shop. Overture is deprecating this property in favour of `taxonomy`; see [https://docs.overturemaps.org/guides/places/](https://docs.overturemaps.org/guides/places/) |
| confidence | double | Overture's confidence that the place exists and is current, between 0 and 1: 0 means Overture is sure the place no longer exists, 1 that it is sure it does. Null means no confidence information is available. Places marked closed in `operating_status` score 0. |
| websites | list<element: string> | The websites of the place. |
| emails | list<element: string> | The email addresses of the place. |
| socials | list<element: string> | The social media URLs of the place. |
| phones | list<element: string> | The phone numbers of the place. |
| brand | struct<wikidata: string, names: struct<primary: string, common: map<string, string ('common')>, rules: list<element: struct<variant: string, language: string, perspectives: struct<mode: string, countries: list<element: string>>, value: string, between: list<element: double>, side: string>>>> | The brand of the place, with the brand's own names and Wikidata id. A location carrying multiple brands is modeled as multiple separate places, each with its own brand. |
| addresses | list<element: struct<freeform: string, locality: string, postcode: string, region: string, country: string>> | The addresses of the place: `freeform` street address, `locality` (city or neighborhood), `postcode`, `region` as an ISO 3166-2 subdivision code and `country` as an ISO 3166-1 alpha-2 code. |
| names | struct<primary: string, common: map<string, string ('common')>, rules: list<element: struct<variant: string, language: string, perspectives: struct<mode: string, countries: list<element: string>>, value: string, between: list<element: double>, side: string>>> | Names of the feature. `primary` is the most commonly used name; `common` holds translations keyed by IETF BCP-47 language tag; `rules` carries the variants that cannot be expressed as a simple common name (official, alternate, short), each optionally scoped to a `between` range along the geometry or to one `side` of a road. |
| sources | list<element: struct<property: string, dataset: string, license: string, record_id: string, update_time: string, confidence: double, between: list<element: double>>> | Per-property provenance. An array of source records, each naming the `property` it covers in JSON Pointer notation plus the source `dataset`, its `license` (an SPDX identifier where one is available; null means contact the data provider for terms), the `record_id` used, an `update_time`, and for ML-derived data a `confidence`. Every feature carries a root-level entry that is the default source for any property without a more specific one. |
| operating_status | string | Whether the place is open, permanently_closed or temporarily_closed. This is not an indication of opening hours, nor of whether the place happens to be open at the current time of day or day of week. |
| basic_category | string | The basic level category of the place — a simplified name mapped from `categories.primary`, either one-to-one or many-to-one, and empty when that is empty. Basic level categories come from a cognitive science model used in taxonomy and ontology work: the broadest, most general category name, the one most often found in the middle of a general-to-specific hierarchy. Full list at [https://docs.overturemaps.org/guides/places/](https://docs.overturemaps.org/guides/places/) |
| taxonomy | struct<primary: string, hierarchy: list<element: string>, alternates: list<element: string>> | The place's category in Overture's current taxonomy: `primary` is the most specific category, `hierarchy` is the full ordered path from most general to most specific, and `alternates` holds additional categories that apply but are not the primary classification. |
| version | int32 | Version number of the feature, incremented in each Overture release where the geometry or attributes of this feature changed. |
| geometry | binary | The place's location as a WKB Point in EPSG:4326 — a point representation of a real-world facility, service or amenity, not its footprint. To get the structure a place sits in, join it to overture-buildings spatially — a place and a building are separate entities with separate GERS ids. |
| bbox | struct<xmin: double, ymin: double, xmax: double, ymax: double> | Covering bounding box (xmin, ymin, xmax, ymax) for the row's geometry. Not an Overture schema column: Overture's own bbox was dropped and this one rebuilt by gpio during conversion, with row-group statistics, so a spatial filter can skip most of the file over the network. |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./overture-places.parquet | 4.6 MB | 12201d35c925... |
| https://overturemaps-extras-us-west-2.s3.us-west-2.amazonaws.com/tiles/2026-07-22.0/places.pmtiles | 18.0 GB | - |
| ./styles/default.json | 3.1 KB | 1220f48c03fd... |
| ./styles/style-confidence.json | 1.6 KB | 12206b968f68... |
| ./thumbnail.png | 475.5 KB | 122040a97510... |

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
