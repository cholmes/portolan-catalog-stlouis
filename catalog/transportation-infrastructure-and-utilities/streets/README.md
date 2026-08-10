# City Streets

City street GIS data Mirrored from [the city's open data portal](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=68); explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/transportation-infrastructure-and-utilities/streets/collection.json).

![st-louis](https://img.shields.io/badge/st--louis-blue) ![missouri](https://img.shields.io/badge/missouri-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![streets](https://img.shields.io/badge/streets-blue)

## Spatial Coverage

- **Bounding Box**: [-90.31916903735433, 38.53323504055748, -90.16789351152435, 38.774692111816165]

## Temporal Coverage

- **Start**: open
- **End**: ongoing

## Schema

| Column | Type | Description |
|--------|------|-------------|
| OBJECTID | int64 |  |
| FULLNAME | string |  |
| Road_Segment_ID | string |  |
| From_Stree | string |  |
| To_Street | string |  |
| Street | string |  |
| Street_Name_Pre_Directional | string |  |
| Street_Name_Post_Type | string |  |
| Street_Name_Post_Direction | string |  |
| FromLeft | double |  |
| ToLeft | double |  |
| FromRight | double |  |
| ToRight | double |  |
| Class | string |  |
| County | string |  |
| Notes | string |  |
| NHD_NUM | string |  |
| NHD_NAME | string |  |
| NHD_NUMTXT | string |  |
| ANGLE | string |  |
| PRECINCT | string |  |
| ZIP_CODE | string |  |
| ZCTA | string |  |
| WARD | string |  |
| Road_Type | string |  |
| Width_Min | double |  |
| Width_Max | double |  |
| Access_Typ | string |  |
| FUNC_CLASS | string |  |
| SPEED_LIMI | int32 |  |
| LANE_COUNT | int32 |  |
| BI_DIRECTI | int32 |  |
| OVERPASS | int32 |  |
| X | int32 |  |
| Y | int32 |  |
| Bus_Truck | int32 |  |
| State_Stre | int32 |  |
| P_Type | string |  |
| Date_Insta | timestamp[ms] |  |
| Date_Rated | timestamp[ms] |  |
| PCR | int32 |  |
| MoDOT_MJR | string |  |
| Snow_Prior | string |  |
| Snow_Type | string |  |
| Volume | string |  |
| Honorary_N | string |  |
| Vacated | int32 |  |
| Vac_Ordinance | string |  |
| Google_Ima | timestamp[ms] |  |
| Commercial | int32 |  |
| Loc_rd_cls | string |  |
| HONORARY_1 | string |  |
| HN_TYPE | string |  |
| Hon_Ord_Nu | string |  |
| HON_BOARD_ | string |  |
| DIRECTION | string |  |
| LEVEL_ | int32 |  |
| RECLENGTH | double |  |
| Shape_Leng | double |  |
| created_user | string |  |
| created_date | timestamp[ms] |  |
| last_edited_user | string |  |
| last_edited_date | timestamp[ms] |  |
| OneWayCode | string |  |
| FromElevation | int32 |  |
| ToElevation | int32 |  |
| Time | double |  |
| Shape__Length | double |  |
| geometry | binary |  |
| geometry_bbox | struct<xmin: float not null, ymin: float not null, xmax: float not null, ymax: float not null> |  |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./streets.parquet | 2.7 MB | 122095f87ccb... |
| ./streets.pmtiles | 1.7 MB | 122031261e80... |
| ./styles/city-renderer.json | 1.0 KB | 1220938df4be... |
| ./styles/default.json | 821 B | 12209f5280d2... |
| ./styles/style-class.json | 1.7 KB | 1220bed65a39... |
| ./styles/style-suffix.json | 1.6 KB | 1220ce5fb432... |
| ./thumbnail.png | 513.0 KB | 122006eefa04... |
| https://www.stlouis-mo.gov/data/upload/data-files/streets.zip | 1.7 MB | 12208b47bac0... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./streets.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Streets/FeatureServer](https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Streets/FeatureServer)

## Processing Notes

Mirrored from the City of St. Louis open data portal (https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=68). Nothing was added to the data and no features were dropped except where noted below.

Extracted from the city's own ArcGIS REST service with the Portolan CLI:

    portolan extract arcgis \
      https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Streets/FeatureServer --layers "STREETS" --raw

That pages the service's `/query` endpoint for every feature, so this is the whole layer rather than the display-capped sample a browser request returns, and it carries across the service's field aliases. The service's own ESRI renderer was captured at the same time and is republished here as `styles/city-renderer.json`, so the map can be drawn in the city's own symbology.

Converted to GeoParquet with gpio — zstd compression, Hilbert row order, and a covering bbox column with row-group statistics, so a spatial filter can skip most of the file over the network — and tiled to PMTiles with tippecanoe.

The city's own file(s) are published as `source` assets on this collection, linked directly to stlouis-mo.gov — this mirror never becomes the only way to reach the original.


## Attribution

City of St. Louis — Streets - Director's Office

## License

[other](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=68)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
