# Parcels

Current and historic parcel data Mirrored from [the city's open data portal](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=82); explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/assessor/parcels/collection.json).

![st-louis](https://img.shields.io/badge/st--louis-blue) ![missouri](https://img.shields.io/badge/missouri-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![parcels](https://img.shields.io/badge/parcels-blue)

## Spatial Coverage

- **Bounding Box**: [-90.32058220569718, 38.53308187377711, -90.17536578502329, 38.774362902635474]

## Temporal Coverage

- **Start**: open
- **End**: ongoing

## Schema

| Column | Type | Description |
|--------|------|-------------|
| OBJECTID | int64 |  |
| LowerAsrParcelId | string |  |
| ColParcelId | string |  |
| ColCityBlock | int32 |  |
| ColParcel | int32 |  |
| PrimAddrRecNum | int16 |  |
| AddrType | string |  |
| LowAddrNum | int32 |  |
| LowAddrSuf | string |  |
| HighAddrNum | int32 |  |
| HighAddrSuf | string |  |
| NLC | double |  |
| PARITY | string |  |
| StPreDir | string |  |
| StName | string |  |
| StType | string |  |
| StSufDir | string |  |
| StdUnitNum | string |  |
| OWNERNAME | string |  |
| OWNERNAME2 | string |  |
| OWNERADDR | string |  |
| OWNERCITY | string |  |
| OWNERSTATE | string |  |
| OwnerCountry | string |  |
| OWNERZIP | string |  |
| OwnerRank | string |  |
| LegalDesc1 | string |  |
| LegalDesc2 | string |  |
| LegalDesc3 | string |  |
| LegalDesc4 | string |  |
| LegalDesc5 | string |  |
| AsrClassCode | int16 |  |
| AsrLandUse1 | int16 |  |
| AsrLanduse2 | int16 |  |
| RedevPhase | int16 |  |
| RedevYearEnd | int16 |  |
| RedevPhase2 | int16 |  |
| RedevYearEnd2 | int16 |  |
| VacantLot | int16 |  |
| SpecBusDist | int16 |  |
| SpecBusDist2 | int16 |  |
| TIFDist | int16 |  |
| LendingAgcy | int16 |  |
| Condominium | int16 |  |
| NbrOfUnits | int16 |  |
| NbrOfApts | int16 |  |
| FRONTAGE | double |  |
| LANDAREA | int32 |  |
| RecDailyDate | timestamp[ms] |  |
| RecDailyNum | int32 |  |
| RecBookNum | string |  |
| RecPageNum | int16 |  |
| AsdLand | double |  |
| AsdImprove | double |  |
| AsdTotal | double |  |
| BillLand | double |  |
| BillImprove | double |  |
| BillTotal | double |  |
| AprLand | double |  |
| CostAprImprove | double |  |
| AsmtAppealYear | int16 |  |
| AsmtAppealNum | int32 |  |
| AsmtAppealType | string |  |
| PriorAsdDate | timestamp[ms] |  |
| PriorAsdLand | double |  |
| PriorAsdImprove | double |  |
| PriorAsdTotal | double |  |
| PriorTaxAmt | double |  |
| CDALandUse1 | int16 |  |
| CDALandUse2 | int16 |  |
| LRMSUnitNum | string |  |
| Zoning | string |  |
| NbrOfBldgsRes | int16 |  |
| NbrOfBldgsCom | int16 |  |
| FirstYearBuilt | int16 |  |
| LastYearBuilt | int16 |  |
| ResSalePrice | double |  |
| ResSaleDate | timestamp[ms] |  |
| VacBldgYear | int16 |  |
| GeoCityBlockPart | double |  |
| WARD10 | int16 |  |
| PRECINCT10 | int16 |  |
| INSPAREA10 | int16 |  |
| Ward00 | int16 |  |
| PRECINCT02 | int16 |  |
| PRECINCT04 | int16 |  |
| NBRHD | int16 |  |
| CDADIST | int16 |  |
| CDASUBDIST | int16 |  |
| POLICEDIST | int16 |  |
| CensTract10 | double |  |
| CensBlock10 | int16 |  |
| CensBlock00 | double |  |
| Ward90 | int16 |  |
| Precinct90 | int16 |  |
| CensBlock90 | double |  |
| HouseConsDist | int16 |  |
| ASRNBRHD | int16 |  |
| EntZone | int16 |  |
| IMPACTAREA | int16 |  |
| CTDArea | int16 |  |
| LEAFAREA | int16 |  |
| ZIP | int32 |  |
| OnFloodBlock | int16 |  |
| SpecParcelType | string |  |
| SubParcelType | string |  |
| NbrOfSubAccts | int16 |  |
| NbrOfCondos | int16 |  |
| LRMSParcel | int16 |  |
| AcctPrimary | int16 |  |
| HANDLE | string |  |
| OWNEROCC | string |  |
| FirstDate | timestamp[ms] |  |
| LastDate | timestamp[ms] |  |
| OwnerUpdate | timestamp[ms] |  |
| OwnerCode | int16 |  |
| SITEADDR | string |  |
| SQFT | int32 |  |
| ParcelId | string |  |
| WARD | int16 |  |
| TaxBalance | double |  |
| PropertyClassCode | int16 |  |
| IsAbatedProperty | int16 |  |
| AbatementStartYear | int16 |  |
| AbatementEndYear | int16 |  |
| SpecBusDist3 | int16 |  |
| Ward20 | int16 |  |
| Precinct20 | int16 |  |
| InspArea20 | int16 |  |
| CensTract20 | int16 |  |
| CensBlock20 | int16 |  |
| MaintZoneWC | int16 |  |
| TransDevDist | int16 |  |
| SHAPE | binary |  |
| CityBlock | double |  |
| Parcel | double |  |
| SHAPE.STArea() | double |  |
| SHAPE.STLength() | double |  |
| geometry | binary |  |
| geometry_bbox | struct<xmin: float not null, ymin: float not null, xmax: float not null, ymax: float not null> |  |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./parcels.parquet | 29.9 MB | 122004b0a978... |
| ./parcels.pmtiles | 34.4 MB | 1220e8854ee2... |
| ./styles/city-renderer.json | 525 B | 1220d4ff4909... |
| ./styles/default.json | 801 B | 12207be6f755... |
| ./styles/style-assessed-value.json | 1.4 KB | 1220fd5b0b12... |
| ./styles/style-city-assessor.json | 545 B | 12200930a396... |
| ./styles/style-vacant-lots.json | 1.1 KB | 122092b73432... |
| ./styles/style-year-built.json | 1.3 KB | 122071ceff97... |
| ./thumbnail.png | 378.5 KB | 1220875a6b28... |
| ./styles/style-zoning.json | 1.9 KB | 1220d402120c... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./parcels.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/PARCELS_PUBLIC/MapServer](https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/PARCELS_PUBLIC/MapServer)

## Processing Notes

Mirrored from the City of St. Louis open data portal (https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=82).
Source: https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/PARCELS_PUBLIC/MapServer (ArcGIS REST service),
converted to GeoParquet (zstd, spatially ordered, covering bbox) and PMTiles.


## Attribution

City of St. Louis — Assessor's Office

## License

[other](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=82)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
