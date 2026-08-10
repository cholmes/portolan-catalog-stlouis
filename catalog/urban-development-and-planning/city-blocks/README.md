# City Blocks

Information about city blocks. A city block, residential block, urban block, or simply "block" is a central element of urban planning and urban design. Mirrored from [the city's open data portal](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=12); explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/urban-development-and-planning/city-blocks/collection.json).

![st-louis](https://img.shields.io/badge/st--louis-blue) ![missouri](https://img.shields.io/badge/missouri-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![city](https://img.shields.io/badge/city-blue) ![blocks](https://img.shields.io/badge/blocks-blue)

## Spatial Coverage

- **Bounding Box**: [-90.32058220569718, 38.53358364730386, -90.1753971881761, 38.774362902635474]

## Temporal Coverage

- **Start**: open
- **End**: ongoing

## Schema

| Column | Type | Description |
|--------|------|-------------|
| OBJECTID | int64 |  |
| Join_Count | int32 |  |
| TARGET_FID | int32 |  |
| Name | string |  |
| BLOCK_HANDLE | string | Handle identifier of the city block (block-level analogue of the parcel HANDLE). |
| GeoCityBlockPart | double | Sub-part designator when a GIS city block is split into parts. |
| WARD10 | int16 |  |
| PRECINCT10 | int16 |  |
| INSPAREA10 | int16 |  |
| Ward00 | int16 |  |
| PRECINCT02 | int16 |  |
| PRECINCT04 | int16 |  |
| NBRHD | int16 | City neighborhood number (city 'Neighborhood' vocabulary); WARD10/Ward20/Ward00/Ward90 and the PRECINCT*/CensTract*/CensBlock* columns are the block's assignments in each redistricting/census cycle. |
| CDADIST | int16 |  |
| CDASUBDIST | int16 |  |
| POLICEDIST | int16 | SLMPD police district containing the block. |
| CensTract10 | double |  |
| CensBlock10 | int16 |  |
| CensBlock00 | double |  |
| Ward90 | int16 |  |
| Precinct90 | int16 |  |
| CensBlock90 | double |  |
| HouseConsDist | int16 | Housing Conservation District the block falls in (city 'Housing Conservation District' vocabulary). |
| ASRNBRHD | int16 |  |
| EntZone | int16 |  |
| IMPACTAREA | int16 |  |
| CTDArea | int16 |  |
| OnFloodBlock | int16 | Flag that the block touches a floodplain. |
| SpecBusDist3 | int16 |  |
| Ward20 | int16 |  |
| Precinct20 | int16 |  |
| InspArea20 | int16 |  |
| CensTract20 | int16 |  |
| CensBlock20 | int16 |  |
| MaintZoneWC | int16 |  |
| TransDevDist | int16 |  |
| Shape | binary |  |
| Shape_Length | double |  |
| Shape_Area | double |  |
| geometry | binary |  |
| geometry_bbox | struct<xmin: float not null, ymin: float not null, xmax: float not null, ymax: float not null> |  |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./city-blocks.parquet | 6.9 MB | 122047a49613... |
| ./city-blocks.pmtiles | 2.3 MB | 122036a2ad24... |
| ./styles/city-renderer.json | 533 B | 1220d9fd7162... |
| ./styles/default.json | 1.4 KB | 1220b391f63b... |
| ./styles/style-block-number.json | 1.4 KB | 12205bcd2c5f... |
| ./styles/style-tint.json | 511 B | 1220bb0e5e3f... |
| ./thumbnail.png | 401.3 KB | 12202499d034... |
| ./styles/style-by-census-tract.json | 2.1 KB | 1220f78c4c11... |
| ./styles/style-by-precinct.json | 1.9 KB | 1220f90efd1b... |
| ./styles/style-by-ward.json | 1.9 KB | 12209819ca16... |
| https://www.stlouis-mo.gov/data/upload/data-files/blocks_shape.zip | 6.1 MB | 122078f48b9a... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./city-blocks.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://maps8.stlouis-mo.gov/arcgis/rest/services/STLOUIS/BOUNDARIES/MapServer](https://maps8.stlouis-mo.gov/arcgis/rest/services/STLOUIS/BOUNDARIES/MapServer)

## Processing Notes

Mirrored from the City of St. Louis open data portal (https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=12). Nothing was added to the data and no features were dropped except where noted below.

Extracted from the city's own ArcGIS REST service with the Portolan CLI:

    portolan extract arcgis \
      https://maps8.stlouis-mo.gov/arcgis/rest/services/STLOUIS/BOUNDARIES/MapServer --layers "City Blocks" --raw

That pages the service's `/query` endpoint for every feature, so this is the whole layer rather than the display-capped sample a browser request returns, and it carries across the service's field aliases. The service's own ESRI renderer was captured at the same time and is republished here as `styles/city-renderer.json`, so the map can be drawn in the city's own symbology.

Converted to GeoParquet with gpio — zstd compression, Hilbert row order, and a covering bbox column with row-group statistics, so a spatial filter can skip most of the file over the network — and tiled to PMTiles with tippecanoe.

The city's own file(s) are published as `source` assets on this collection, linked directly to stlouis-mo.gov — this mirror never becomes the only way to reach the original.


## Attribution

City of St. Louis — Assessor's Office

## License

[other](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=12)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
