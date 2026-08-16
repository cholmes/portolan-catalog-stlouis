# Overture Divisions

Point, line, and polygon representations of human settlements from the Overture divisions theme: recognized areas for governance, culture, or organization, from countries and regions down to counties, cities, and neighborhoods. Three feature types are merged here with an `overture_type` column: `division` (label points with population and hierarchy), `division_area` (the land or maritime polygon belonging to a division), and `division_boundary` (shared borders between divisions). For the St. Louis box that means the city itself, surrounding counties and municipalities on both sides of the river, and Overture's neighborhood set. Overture documents this data well: the [divisions theme guide](https://docs.overturemaps.org/guides/divisions/) covers what the theme models, how Overture builds it, and how to query it, and the schema reference gives every field of the feature types merged here — [`division`](https://docs.overturemaps.org/schema/reference/divisions/division/), [`division_area`](https://docs.overturemaps.org/schema/reference/divisions/division_area/), [`division_boundary`](https://docs.overturemaps.org/schema/reference/divisions/division_boundary/).
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
| id | string | Overture feature ID — per the schema, 'a feature ID. This may be an ID associated with the Global Entity Reference System (GERS) if—and-only-if the feature represents an entity that is part of GERS.' GERS IDs are intended to be stable across Overture's monthly releases, which makes this the key for attaching your own data to an Overture feature and for joining to any other GERS-enabled dataset. See the [GERS overview](https://docs.overturemaps.org/gers/). |
| country | string | ISO 3166-1 alpha-2 country code of the country or country-like entity this division represents or belongs to. Where the entity has no code of its own, it carries the code of the first division found by walking the `parent_division_id` chain toward the root — so New York City is 'US'. Schema reference: [country_code_alpha2](https://docs.overturemaps.org/schema/reference/system/country_code_alpha2/). |
| sources | list<element: struct<property: string, dataset: string, license: string, record_id: string, update_time: string, confidence: double, between: list<element: double>>> | Per-property provenance. An array of source records, each naming the `property` it covers in JSON Pointer notation plus the source `dataset`, its `license` (an SPDX identifier where one is available; null means contact the data provider for terms), the `record_id` used, an `update_time`, and for ML-derived data a `confidence`. Every feature carries a root-level entry that is the default source for any property without a more specific one. Schema reference: [sources](https://docs.overturemaps.org/schema/reference/common/sources/). |
| subtype | string | Category of the division, from a finite, hierarchical, ordered list similar to a Who's on First placetype: country, dependency, macroregion, region (a state or province — the largest sub-country unit in most countries), macrocounty, county, localadmin, locality (a populated place, which may or may not have its own administrative authority), borough, macrohood, neighborhood, microhood. Schema reference: [division_subtype](https://docs.overturemaps.org/schema/reference/divisions/types/division_subtype/). |
| admin_level | int32 | This division's position in its country's administrative hierarchy, lower numbers being higher-level units. Typically the number of ancestors in the division's primary hierarchy, so a country is 0 and a region is 1. Schema reference: [admin_level](https://docs.overturemaps.org/schema/reference/divisions/types/admin_level/). |
| class | string | For a division, the settlement size: megacity, city, town, village or hamlet. For a division_area or division_boundary, whether the geometry is `land` (it does not extend beyond the coastline) or `maritime` (it does, in most cases out to the territorial sea). Schema reference: [division_class](https://docs.overturemaps.org/schema/reference/divisions/types/division_class/), [area_class](https://docs.overturemaps.org/schema/reference/divisions/types/area_class/), [boundary_class](https://docs.overturemaps.org/schema/reference/divisions/types/boundary_class/). |
| names | struct<primary: string, common: map<string, string ('common')>, rules: list<element: struct<variant: string, language: string, perspectives: struct<mode: string, countries: list<element: string>>, value: string, between: list<element: double>, side: string>>> | Names of the feature. `primary` is the most commonly used name; `common` holds translations keyed by IETF BCP-47 language tag; `rules` carries the variants that cannot be expressed as a simple common name (official, alternate, short), each optionally scoped to a `between` range along the geometry or to one `side` of a road. Schema reference: [names](https://docs.overturemaps.org/schema/reference/common/names/). |
| wikidata | string | Wikidata item ID for the feature if available, as found on [wikidata.org](https://www.wikidata.org/). Schema reference: [wikidata_id](https://docs.overturemaps.org/schema/reference/system/wikidata_id/). |
| perspectives | struct<mode: string, countries: list<element: string>> | Political perspectives from which this division is considered an accurate representation. Absent means the division is not known to be disputed by anyone. When present, `mode` is accepted_by or disputed_by and `countries` lists the holders — a map drawn for a given country takes the undisputed divisions, adds those it explicitly accepts, then those it does not explicitly dispute. Schema reference: [perspectives](https://docs.overturemaps.org/schema/reference/common/perspectives/). |
| local_type | map<string, string ('local_type')> | The local name for the `subtype`, optionally localized — Quebec has subtype 'region' but is locally a province; the Swiss top-level subdivision is subtype 'region' but is a canton, kanton, cantone or chantun depending on the language. Schema reference: [common_names](https://docs.overturemaps.org/schema/reference/common/common_names/). |
| region | string | ISO 3166-2 principal subdivision code of the subdivision-like entity this division represents or belongs to, inherited up the parent chain the same way `country` is — 'US-MO' for everything on the Missouri side here, 'US-IL' across the river. |
| hierarchies | list<element: list<element: struct<division_id: string, subtype: string, name: string>>> | The hierarchies this division participates in, each an ordered array running from a country down to this division, with a division_id, name and subtype at every step. Most divisions participate in exactly one; more than one means the division or an ancestor is claimed by different parents from different political perspectives. The first hierarchy is the default one. Schema reference: [hierarchy](https://docs.overturemaps.org/schema/reference/divisions/types/hierarchy/). |
| parent_division_id | string | Division id of this division's parent — absent on countries and required on everything else. It is the parent as seen from the default political perspective; `hierarchies` holds the exhaustive list. |
| norms | struct<driving_side: string> | Local norms and rules within the division that are useful for mapping — currently `driving_side`, the side of the road vehicles drive on. A division without this may inherit it from its nearest ancestor that has it. Schema reference: [norms](https://docs.overturemaps.org/schema/reference/divisions/types/norms/). |
| population | int32 | Population of the division. |
| capital_division_ids | list<element: string> | Division ids of this division's capitals — the capital cities, county seats and the like of the division. |
| capital_of_divisions | list<element: struct<division_id: string, subtype: string>> | The divisions this division is the capital of, each as a division_id with its subtype. Schema reference: [capital_of_division_item](https://docs.overturemaps.org/schema/reference/divisions/types/capital_of_division_item/). |
| cartography | struct<prominence: int32, min_zoom: int32, max_zoom: int32, sort_key: int32> | Cartographic hints for map-making: `prominence` is Overture's view of the feature's significance on a 1–100 scale, derived from factors including population, capital status, place tags and type; `min_zoom` and `max_zoom` are the recommended Slippy Map tile zooms; `sort_key` is the recommended draw order, with lower numbers drawn on top. Schema reference: [cartographic_hints](https://docs.overturemaps.org/schema/reference/common/cartographic_hints/). |
| version | int32 | Version number of the feature, incremented in each Overture release where the geometry or attributes of this feature changed. Schema reference: [feature_version](https://docs.overturemaps.org/schema/reference/common/feature_version/). |
| overture_type | string | Which of the divisions theme's three feature types this row is — `division` (the entity itself, as a label point with population and hierarchy), `division_area` (the land or maritime polygon belonging to a division) or `division_boundary` (a border line shared by two divisions of the same subtype). Not an Overture schema column: this mirror merges the theme's feature types into one collection and records the type here. Schema reference: [division](https://docs.overturemaps.org/schema/reference/divisions/division/), [division_area](https://docs.overturemaps.org/schema/reference/divisions/division_area/), [division_boundary](https://docs.overturemaps.org/schema/reference/divisions/division_boundary/). |
| geometry | binary | WKB geometry in EPSG:4326, and its type follows `overture_type`: a Point for a division (the approximate location commonly associated with the entity), a Polygon or MultiPolygon for a division_area, a LineString or MultiLineString for a division_boundary. Geometries crossing the edge of the St. Louis bounding box were clipped to it, so the county and state areas here are fragments. |
| is_land | bool | Whether this geometry is the land-clipped, non-maritime version, meant for map rendering and cartographic display. |
| is_territorial | bool | Whether this geometry is Overture's best approximation of the entity's maritime boundary, which for a coastal place includes the water area. Meant for data processing and reverse-geocoding rather than display. |
| division_id | string | On a division_area, the id of the division whose area this polygon is. Join it to the `id` of the matching division row. |
| division_ids | list<element: string> | On a division_boundary, the ids of the two divisions on either side of the line: the first is the division to the left and the second to the right, as seen by someone standing on the line facing the direction the geometry runs. |
| is_disputed | bool | On a division_boundary, whether any entity disputes this border; the disputing entities should appear in `perspectives`. Also true where the border between two entities is unclear and the line is a best guess — true with no perspectives is a signal to distrust the line but use it in the absence of anything better. |
| bbox | struct<xmin: double, ymin: double, xmax: double, ymax: double> | Covering bounding box (xmin, ymin, xmax, ymax) for the row's geometry. Not an Overture schema column: Overture's own bbox was dropped and this one rebuilt by gpio during conversion, with row-group statistics, so a spatial filter can skip most of the file over the network. |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./overture-divisions.parquet | 162.0 KB | 1220451a1345... |
| https://overturemaps-extras-us-west-2.s3.us-west-2.amazonaws.com/tiles/2026-07-22.0/divisions.pmtiles | 18.2 GB | - |
| ./styles/default.json | 2.9 KB | 12203dfc74dc... |
| ./styles/style-neighborhoods.json | 2.5 KB | 1220fcde50ef... |
| ./thumbnail.png | 365.2 KB | 1220a78a968a... |

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
