# Overture Addresses

Address points from the Overture addresses theme (currently in Alpha). An address represents a physical place through a series of attributes — street number, street name, unit, address levels, postal code, and/or country — together with a point geometry giving the approximate location most commonly associated with it. The theme aggregates open government address datasets, each carrying its own permissive open license, recorded per feature in the `sources` column. Useful for geocoding, validation, and conflation with buildings and places. Overture documents this data well: the [addresses theme guide](https://docs.overturemaps.org/guides/addresses/) covers what the theme models, how Overture builds it, and how to query it, and the schema reference gives every field of its feature type — [`address`](https://docs.overturemaps.org/schema/reference/addresses/address/).
Unlike everything else in this catalog, this is **not** City of St. Louis data: it comes from the [Overture Maps Foundation](https://overturemaps.org/), a collaborative project building open, interoperable map data for the world. This collection is a St. Louis extract of that global dataset — everything inside the city's bounding box, which also takes in the Illinois shore of the Mississippi (East St. Louis, Cahokia Heights) — included here to demonstrate how a city's open-data catalog can blend in other St. Louis-relevant open data alongside the city's own. The GeoParquet was extracted from Overture release 2026-07-22.0. **Coverage caveat:** the theme's aggregated government datasets do not yet include the City of St. Louis itself — the ~99,000 points here are the St. Louis County and Illinois fringe that falls inside the bounding box (Wellston, Ferguson, Jennings, Cahokia, and neighbors), with almost nothing between the city limits. Uniquely among the Overture collections here, the map tiles are built locally from this extract: Overture's own global address tiles are just as empty for St. Louis, and only exist at z14. Explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/urban-development-and-planning/overture-addresses/collection.json).

![overture](https://img.shields.io/badge/overture-blue) ![overture-maps](https://img.shields.io/badge/overture--maps-blue) ![addresses](https://img.shields.io/badge/addresses-blue) ![st-louis](https://img.shields.io/badge/st--louis-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![address](https://img.shields.io/badge/address-blue)

## Spatial Coverage

- **Bounding Box**: [-90.3205182695672, 38.53199954005468, -90.16631356713408, 38.774346652337805]

## Temporal Coverage

- **Start**: 2026-07-22T00:00:00Z
- **End**: 2026-07-22T00:00:00Z

## Schema

| Column | Type | Description |
|--------|------|-------------|
| id | string | Overture feature ID — per the schema, 'a feature ID. This may be an ID associated with the Global Entity Reference System (GERS) if—and-only-if the feature represents an entity that is part of GERS.' GERS IDs are intended to be stable across Overture's monthly releases, which makes this the key for attaching your own data to an Overture feature and for joining to any other GERS-enabled dataset. See the [GERS overview](https://docs.overturemaps.org/gers/). |
| street | string | The street name for this address, which can include the street type or suffix, as in Main Street. Ideally fully spelled out, though many source datasets abbreviate it. |
| number | string | The house number for this address. Not strictly a number: values such as 74B, 189 1/2 and 208.5 are common as the number part of an address, and they are not part of the `unit`. |
| unit | string | The suite, unit, apartment or floor number. |
| postcode | string | The postcode for the address. |
| postal_city | string | The alternate city name a mailing address needs when it differs from the city that actually contains the address coordinates — for example 716 East County Road, Winchester, Indiana takes 'Ridgeville' as its postal city in the US National Address Database. |
| address_levels | list<element: struct<value: string>> | The administrative levels present in the address, ordered highest first, with up to 5 entries. How many there are and what they mean is country-dependent: in the United States two are expected, the state and the municipality. A level the data provider did not supply is present as an entry with no `value`. Schema reference: [address_level](https://docs.overturemaps.org/schema/reference/addresses/types/address_level/). |
| country | string | ISO 3166-1 alpha-2 country code for the address. Schema reference: [country_code_alpha2](https://docs.overturemaps.org/schema/reference/system/country_code_alpha2/). |
| sources | list<element: struct<property: string, dataset: string, license: string, record_id: string, update_time: string, confidence: double, between: list<element: double>>> | Per-property provenance, and the place to look for this collection's licensing: the addresses theme aggregates over 175 independent open datasets, each keeping its own license, so the applicable terms are the `license` recorded here per feature rather than one license for the collection. Each record also names the `property` it covers in JSON Pointer notation, the source `dataset`, the `record_id` used and an `update_time`. |
| version | int32 | Version number of the feature, incremented in each Overture release where the geometry or attributes of this feature changed. Schema reference: [feature_version](https://docs.overturemaps.org/schema/reference/common/feature_version/). |
| geometry | binary | The address's location as a WKB Point in EPSG:4326 — the approximate location most commonly associated with the address. |
| bbox | struct<xmin: double, ymin: double, xmax: double, ymax: double> | Covering bounding box (xmin, ymin, xmax, ymax) for the row's geometry. Not an Overture schema column: Overture's own bbox was dropped and this one rebuilt by gpio during conversion, with row-group statistics, so a spatial filter can skip most of the file over the network. |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./overture-addresses.parquet | 7.0 MB | 1220cd113806... |
| ./overture-addresses.pmtiles | 1.7 MB | 1220ffdb0c48... |
| ./styles/default.json | 990 B | 12205e647e07... |
| ./styles/style-postcode.json | 2.2 KB | 12205232b851... |
| ./thumbnail.png | 325.0 KB | 1220eba27dfa... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./overture-addresses.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[s3://overturemaps-us-west-2/release/2026-07-22.0/theme=addresses](s3://overturemaps-us-west-2/release/2026-07-22.0/theme=addresses)

## Processing Notes

Extracted from Overture Maps release 2026-07-22.0 with DuckDB, reading the release's GeoParquet straight from Overture's public S3 bucket:

      s3://overturemaps-us-west-2/release/2026-07-22.0/theme=addresses/type=address/*.parquet

The extract keeps every feature that intersects the city-boundary collection's bbox (-90.3205, 38.5320, -90.1663, 38.7743) — a rectangle, so the Illinois shore of the Mississippi is included. Geometries that cross the edge of the box are clipped to it (otherwise a feature whose bounding box merely touches St. Louis arrives whole — the full United States polygon, in the divisions theme's case). No other filtering, and no columns were altered; Overture's own `bbox` covering column was dropped and rebuilt during conversion.

Converted to GeoParquet with gpio — zstd compression, Hilbert row order, and a covering bbox column with row-group statistics, so a spatial filter can skip most of the file over the network.

The PMTiles are not built by this mirror: the tiles asset points at Overture's own release-pinned global tiles for the `addresses` theme — the tiles behind explore.overturemaps.org — served from Overture's public bucket. The styles here select just this collection's layers from them. The tiles cover the whole world, so zooming out shows global data even though the Parquet in this collection is only the St. Louis extract.


## Attribution

Overture Maps Foundation

## License

[other](https://docs.overturemaps.org/attribution/)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
