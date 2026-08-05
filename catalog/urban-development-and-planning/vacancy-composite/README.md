# Parcel Vacancy Composite

Parcel-level vacancy indicators for St. Louis: vacant buildings, condemnations, tax delinquency, LRA ownership, and private vacancy, compiled by SLDC. Mirrored from [the city's open data portal](https://stlcity.maps.arcgis.com/home/item.html?id=98a6f429617546be9d9b467c5ad1dafc); explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/urban-development-and-planning/vacancy-composite/collection.json).

![st-louis](https://img.shields.io/badge/st--louis-blue) ![missouri](https://img.shields.io/badge/missouri-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![vacancy](https://img.shields.io/badge/vacancy-blue) ![composite](https://img.shields.io/badge/composite-blue)

## Spatial Coverage

- **Bounding Box**: [-90.3170069711414, 38.5357964169723, -90.1790919682017, 38.7728451074772]

## Temporal Coverage

- **Start**: open
- **End**: ongoing

## Schema

| Column | Type | Description |
|--------|------|-------------|
| OBJECTID | int64 |  |
| TOLEMI_ID | double | Property identifier assigned by Tolemi (the BuildingBlocks data platform SLDC uses to assemble its vacancy composite; the source layer is SLDC.SLDC.Tol_Def_Vac_NP). |
| PID1 | double | First parcel identifier for the property as carried in the Tolemi composite (exact scheme not documented; PID2 is a second identifier). |
| PID2 | double |  |
| STREET_ADD | string | Street address of the property (shapefile-truncated name). |
| PROPERTY_T | string | Property type (shapefile-truncated 'PROPERTY_TYPE'; no decode published). |
| TOLEMI_DEF | string | Tolemi 'definite vacancy' determination for the property — the flag/category under which the parcel qualified for this definite-vacant composite (layer name Tol_Def_Vac; no public decode found). |
| LRA_OWNED_ | int32 | Whether the property is owned by the Land Reutilization Authority (shapefile-truncated flag). |
| LRA_RORE | int32 | LRA inventory attribute (untruncated meaning not documented; no public decode found). |
| VACANT_BUI | int32 | Vacant-building indicator (shapefile-truncated 'VACANT_BUILDING', i.e. on the city vacant building registry). |
| CONDEMNATI | int32 | Condemnation indicator for the structure (shapefile-truncated 'CONDEMNATION'). |
| NSR_OWNED_ | int32 | Flag for ownership recorded in the city's vacancy pipeline under 'NSR' (not expanded in any public documentation found). |
| LRA_OWNE_1 | int32 |  |
| PRIVATE_VA | int32 | Privately-owned vacant indicator (shapefile-truncated 'PRIVATE_VACANT'). |
| NSR_OWNE_1 | int32 |  |
| LAND_SIZE | double | Land area of the parcel (units not documented in the source; city parcel land areas are square feet). |
| STRUCTUREA | string | Structure area (shapefile-truncated; likely 'STRUCTURE_AREA'). |
| YEAR_BUILT | double | Year the structure was built. |
| BUILDING_S | string |  |
| NUMBER_OF_ | double |  |
| BUILDING_1 | double |  |
| OWNER_NAME | string | Owner name of record; OWNER_ADDR is the owner's mailing address. |
| OWNER_ADDR | string |  |
| OWNER_TENU | string | Owner tenure (shapefile-truncated 'OWNER_TENURE'; no decode published). |
| TAX_DELINQ | string | Tax delinquency indicator for the property. |
| OWNER_PROP | double |  |
| OWNER_VAC_ | double |  |
| BUILDING_F | double |  |
| FOREST_FEE | double |  |
| LRA_STATUS | string | Status of the property within the LRA inventory; LRA_DATE is the associated date. |
| LRA_DATE | string |  |
| BISA_SCORE | double | Building Inspection/condition score carried in the composite ('BISA' not expanded in public documentation). |
| ECON_INVES | double |  |
| PROB_PROP_ | double |  |
| PUBLIC_HEA | double |  |
| COLPARCELI | double |  |
| HANDLE | double | Citywide parcel handle (join key to parcels); COLPARCELI is the truncated Collector parcel ID. |
| NBRHD | double | City neighborhood number (city 'Neighborhood' vocabulary). |
| ZONING | string | Zoning district code (city 'Zoning Code' vocabulary). |
| CENSBLOCK2 | string | 2020 census block (shapefile-truncated 'CENSBLOCK20'). |
| WARD20 | double | 2020-cycle aldermanic ward number. |
| LATITUDE | double |  |
| LONGITUDE | double |  |
| SHAPE_1 | string |  |
| SHAPE_1_GE | string |  |
| Shape__Area | double |  |
| Shape__Length | double |  |
| geometry | binary |  |
| bbox | struct<xmin: double, ymin: double, xmax: double, ymax: double> |  |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./vacancy-composite.parquet | 6.1 MB | 1220dd137697... |
| ./vacancy-composite.pmtiles | 19.3 MB | 1220b92eac1d... |
| ./styles/city-renderer.json | 545 B | 12202c85b3ae... |
| ./styles/default.json | 1.2 KB | 122007e90173... |
| ./styles/style-source.json | 1.8 KB | 1220926cbf53... |
| ./styles/style-year-built.json | 1.4 KB | 122017a8967b... |
| ./thumbnail.png | 376.3 KB | 1220c8252c3a... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./vacancy-composite.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/SLDC_SLDC_Tol_Def_Vac_NP/FeatureServer](https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/SLDC_SLDC_Tol_Def_Vac_NP/FeatureServer)

## Processing Notes

Mirrored from the City of St. Louis open data portal (https://stlcity.maps.arcgis.com/home/item.html?id=98a6f429617546be9d9b467c5ad1dafc).
Source: https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/SLDC_SLDC_Tol_Def_Vac_NP/FeatureServer (ArcGIS REST service),
converted to GeoParquet (zstd, spatially ordered, covering bbox) and PMTiles.


## Attribution

City of St. Louis — St. Louis Development Corporation

## License

[other](https://stlcity.maps.arcgis.com/home/item.html?id=98a6f429617546be9d9b467c5ad1dafc)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
