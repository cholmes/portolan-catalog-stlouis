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
| id | string | Overture feature ID — per the schema, 'a feature ID. This may be an ID associated with the Global Entity Reference System (GERS) if—and-only-if the feature represents an entity that is part of GERS.' GERS IDs are intended to be stable across Overture's monthly releases, which makes this the key for attaching your own data to an Overture feature and for joining to any other GERS-enabled dataset. See [https://docs.overturemaps.org/gers/](https://docs.overturemaps.org/gers/) |
| names | struct<primary: string, common: map<string, string ('common')>, rules: list<element: struct<variant: string, language: string, perspectives: struct<mode: string, countries: list<element: string>>, value: string, between: list<element: double>, side: string>>> | Names of the feature. `primary` is the most commonly used name; `common` holds translations keyed by IETF BCP-47 language tag; `rules` carries the variants that cannot be expressed as a simple common name (official, alternate, short), each optionally scoped to a `between` range along the geometry or to one `side` of a road. |
| subtype | string | Broad category of the transportation segment: road, rail or water. Null on connector rows. |
| class | string | For a road segment, the kind of road and its position in the road network hierarchy: motorway, trunk, primary, secondary, tertiary, residential, living_street, unclassified, service, pedestrian, footway, steps, path, track, cycleway, bridleway or unknown. For a rail segment: funicular, light_rail, monorail, narrow_gauge, standard_gauge, subway, tram or unknown. |
| subclass | string | Refines the expected usage of the segment; the values must not overlap: link, sidewalk, crosswalk, parking_aisle, driveway, alley or cycle_crossing. |
| subclass_rules | list<element: struct<value: string, between: list<element: double>>> | Subclass values scoped to part of the segment, for a segment whose usage changes partway along. Each rule pairs a `value` with a `between` pair of linearly-referenced positions — fractions of the distance from the start of the geometry, so [0.25, 0.5] is the stretch from a quarter to half way along. |
| connectors | list<element: struct<connector_id: string, at: double>> | The connectors this segment is physically connected to and their relative location along it. Each connector is a possible routing decision point: a place along the segment where a traveller can transition to other segments sharing the same connector. `connector_id` joins to the connector rows in this collection; `at` is the linearly-referenced position, 0 at the start of the geometry and 1 at the end. |
| road_surface | list<element: struct<value: string, between: list<element: double>>> | Physical surface of the road — unknown, paved, unpaved, gravel, dirt, paving_stones or metal — as an array of rules, each optionally scoped to a `between` range along the segment. |
| road_flags | list<element: struct<values: list<element: string>, between: list<element: double>>> | Boolean attributes of a road segment, which may overlap and describe physical characteristics: is_bridge, is_link, is_tunnel, is_under_construction, is_abandoned, is_covered, is_indoor. Each entry is a set of `values` optionally scoped to a `between` range along the segment. |
| rail_flags | list<element: struct<values: list<element: string>, between: list<element: double>>> | Boolean attributes of a railway segment, which may overlap and describe physical characteristics: is_bridge, is_tunnel, is_under_construction, is_abandoned, is_covered, is_passenger, is_freight, is_disused. Each entry is a set of `values` optionally scoped to a `between` range along the segment. |
| width_rules | list<element: struct<value: double, between: list<element: double>>> | Edge-to-edge width of the road modeled by this segment, in meters, scoped along the segment. A carriageway segment's width includes any shoulder; a sidewalk segment's is the width of the sidewalk; a segment modelling a combined sidewalk and carriageway measures across both. |
| level_rules | list<element: struct<value: int32, between: list<element: double>>> | Z-order (stacking order) of the road segment, as rules rather than a single value so the level can change partway along — how a road that dips under a bridge midway is modeled. Each rule is a `value` with an optional `between` range. |
| access_restrictions | list<element: struct<access_type: string, when: struct<during: string, heading: string, using: list<element: string>, recognized: list<element: string>, mode: list<element: string>, vehicle: list<element: struct<dimension: string, comparison: string, value: double, unit: string>>>, between: list<element: double>>> | Rules governing access to this road segment. Each rule gives an `access_type` (allowed, denied or designated) and, in `when`, the scopes it applies under: travel `mode` (vehicle, motor_vehicle, car, truck, motorcycle, foot, bicycle, bus, hgv, hov, emergency), `heading` along the geometry, purpose of use, the traveller's `recognized` status, `vehicle` dimension tests such as height or weight, and `during`, a time span in the OpenStreetMap opening-hours syntax. This is where 'no trucks over 2 tonnes' and 'buses may travel the wrong way' live. |
| speed_limits | list<element: struct<min_speed: struct<value: int32, unit: string>, max_speed: struct<value: int32, unit: string>, is_max_speed_variable: bool, when: struct<during: string, heading: string, using: list<element: string>, recognized: list<element: string>, mode: list<element: string>, vehicle: list<element: struct<dimension: string, comparison: string, value: double, unit: string>>>, between: list<element: double>>> | Rules governing speed on this road segment: `min_speed` and `max_speed`, each a value with a unit, plus `is_max_speed_variable` for a variable speed corridor. The same `when` scoping as access_restrictions lets a limit apply only to certain modes, headings, vehicles or times of day, and `between` scopes it to part of the segment. |
| prohibited_transitions | list<element: struct<sequence: list<element: struct<connector_id: string, segment_id: string>>, final_heading: string, when: struct<heading: string, during: string, using: list<element: string>, recognized: list<element: string>, mode: list<element: string>, vehicle: list<element: struct<dimension: string, comparison: string, value: double, unit: string>>>, between: list<element: double>>> | Turn restrictions: rules preventing a transition from this segment to another. Each rule gives the ordered `sequence` of connector and segment ids that may not be followed, the `final_heading` prohibited on the destination segment, and the `when` scopes (mode, time, heading, vehicle) under which the prohibition applies. |
| routes | list<element: struct<name: string, network: string, ref: string, symbol: string, wikidata: string, between: list<element: double>>> | The named or numbered routes this segment belongs to — for each, the route's full `name`, the `network` (highway system) it belongs to, the `ref` code or number used to reference it, a `symbol` describing its signage, and a `wikidata` id. |
| destinations | list<element: struct<labels: list<element: struct<value: string, type: string>>, symbols: list<element: string>, from_connector_id: string, to_segment_id: string, to_connector_id: string, when: struct<heading: string>, final_heading: string>> | Where following this segment gets you, described the way the objects are described on signposts or ground writing that a traveller on the segment would actually observe — so a navigation system can name the signs the driver sees. Each entry has `labels` (a value plus its type: street, country, route_ref or toward_route_ref), sign `symbols`, the connector it applies from, the segment and connector it leads to, and the heading it applies in. |
| sources | list<element: struct<property: string, dataset: string, license: string, record_id: string, update_time: string, confidence: double, between: list<element: double>>> | Per-property provenance. An array of source records, each naming the `property` it covers in JSON Pointer notation plus the source `dataset`, its `license` (an SPDX identifier where one is available; null means contact the data provider for terms), the `record_id` used, an `update_time`, and for ML-derived data a `confidence`. Every feature carries a root-level entry that is the default source for any property without a more specific one. |
| version | int32 | Version number of the feature, incremented in each Overture release where the geometry or attributes of this feature changed. |
| overture_type | string | Which of the transportation theme's two feature types this row is — `segment` (a path that can be travelled) or `connector` (a point where segments physically connect, i.e. a routing decision point). Connector rows carry only id, geometry, version and sources; every segment attribute is null on them. Not an Overture schema column: this mirror merges the theme's feature types into one collection and records the type here. |
| geometry | binary | Segment geometry is a LineString and connector geometry is a Point, both as WKB in EPSG:4326. Lines crossing the edge of the St. Louis bounding box were clipped to it, which can shorten a segment relative to Overture's. |
| bbox | struct<xmin: double, ymin: double, xmax: double, ymax: double> | Covering bounding box (xmin, ymin, xmax, ymax) for the row's geometry. Not an Overture schema column: Overture's own bbox was dropped and this one rebuilt by gpio during conversion, with row-group statistics, so a spatial filter can skip most of the file over the network. |

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
