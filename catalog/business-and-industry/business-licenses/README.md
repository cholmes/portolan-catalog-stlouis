# Business Licenses

Business licenses as of October 2025, from SLDC. Mirrored from [the city's open data portal](https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Business_Licenses_as_of_October_2025/FeatureServer); explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/business-and-industry/business-licenses/collection.json).

![st-louis](https://img.shields.io/badge/st--louis-blue) ![missouri](https://img.shields.io/badge/missouri-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![business](https://img.shields.io/badge/business-blue) ![licenses](https://img.shields.io/badge/licenses-blue)

## Spatial Coverage

- **Bounding Box**: [-90.31803288233131, 38.537709831821836, -90.18101621192292, 38.76869128000458]

## Temporal Coverage

- **Start**: open
- **End**: ongoing

## Schema

| Column | Type | Description |
|--------|------|-------------|
| OBJECTID | int64 |  |
| Score | double |  |
| Match_type | string |  |
| Match_addr | string |  |
| IN_SingleLine | string | The city's service labels this field 'Single Line Input'. |
| USER_Doc_Nbr_ | int32 | The city's service labels this field 'Doc Nbr.'. |
| USER_Tax_Year | int32 | The city's service labels this field 'Tax Year'. |
| USER_Status_Cd_ | int32 | The city's service labels this field 'Status Cd.'. |
| USER_Trade_Name | string | The city's service labels this field 'Trade Name'. |
| USER_DocType | string | The city's service labels this field 'DocType'. |
| USER_Tax_Period | int32 | The city's service labels this field 'Tax Period'. |
| USER_Date_Business_Started | string | The city's service labels this field 'Date Business Started'. |
| USER_House_Nbr_ | int32 | The city's service labels this field 'House Nbr.'. |
| USER_House_Sfx_ | string | The city's service labels this field 'House Sfx.'. |
| USER_House_Unit | string | The city's service labels this field 'House Unit'. |
| USER_St__Dir_ | string | The city's service labels this field 'St. Dir.'. |
| USER_Property_St__Name | string | The city's service labels this field 'Property St. Name'. |
| USER_St__Type | string | The city's service labels this field 'St. Type'. |
| USER_Zip_Cd_ | int32 | The city's service labels this field 'Zip Cd.'. |
| USER_Street_Address | string | The city's service labels this field 'Street Address'. |
| USER_HQ_Owner_Cd_ | string | The city's service labels this field 'HQ Owner Cd.'. |
| USER_Owner_Business_HQ_Name | string | The city's service labels this field 'Owner/Business HQ Name'. |
| USER_Mailing_Address_Line_1 | string | The city's service labels this field 'Mailing Address Line 1'. |
| USER_Mailing_Address_Line_2 | string | The city's service labels this field 'Mailing Address Line 2'. |
| USER_Mailing_Address_Line_3 | string | The city's service labels this field 'Mailing Address Line 3'. |
| USER_Ward_Nbr_ | int32 | The city's service labels this field 'Ward Nbr.'. |
| USER_City_Block | int32 | The city's service labels this field 'City Block'. |
| USER_CDA_Neighborhood | int32 | The city's service labels this field 'CDA Neighborhood'. |
| USER_CDA_Subdistrict | int32 | The city's service labels this field 'CDA Subdistrict'. |
| USER_Nbr__Of_Employees | int32 | The city's service labels this field 'Nbr. Of Employees'. |
| USER_Space_Use_Cd_ | int32 | The city's service labels this field 'Space Use Cd.'. |
| USER_Business_Phone | string | The city's service labels this field 'Business Phone'. |
| USER_Contact_Name | string | The city's service labels this field 'Contact Name'. |
| USER_Business_E_Mail | string | The city's service labels this field 'Business E-Mail'. |
| geometry | binary | Feature geometry (WGS84, WKB encoding). |
| bbox | struct<xmin: double, ymin: double, xmax: double, ymax: double> | Per-row bounding box of the geometry (the GeoParquet covering column). |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./business-licenses.parquet | 787.3 KB | 1220ecb0208e... |
| ./business-licenses.pmtiles | 9.3 MB | 122037dea341... |
| ./styles/city-renderer.json | 618 B | 122013a4e551... |
| ./styles/default.json | 823 B | 1220d8f7e518... |
| ./styles/style-bold.json | 810 B | 1220e49e649b... |
| ./styles/style-plain.json | 726 B | 122030df7de8... |
| ./thumbnail.png | 241.1 KB | 12201c56836f... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./business-licenses.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Business_Licenses_as_of_October_2025/FeatureServer](https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Business_Licenses_as_of_October_2025/FeatureServer)

## Processing Notes

Mirrored from the City of St. Louis open data portal (https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Business_Licenses_as_of_October_2025/FeatureServer). Nothing was added to the data and no features were dropped except where noted below.

Extracted from the city's own ArcGIS REST service with the Portolan CLI:

    portolan extract arcgis \
      https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Business_Licenses_as_of_October_2025/FeatureServer --raw

That pages the service's `/query` endpoint for every feature, so this is the whole layer rather than the display-capped sample a browser request returns, and it carries across the service's field aliases. The service's own ESRI renderer was captured at the same time and is republished here as `styles/city-renderer.json`, so the map can be drawn in the city's own symbology.

The service publishes field aliases and coded-value domains but no field descriptions. The schema descriptions here come from those aliases and domains plus researched notes; a column without a description has no documentation at the source.

Converted to GeoParquet with gpio — zstd compression, Hilbert row order, and a covering bbox column with row-group statistics, so a spatial filter can skip most of the file over the network — and tiled to PMTiles with tippecanoe.


## Attribution

City of St. Louis — St. Louis Development Corporation

## License

[other](https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Business_Licenses_as_of_October_2025/FeatureServer)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
