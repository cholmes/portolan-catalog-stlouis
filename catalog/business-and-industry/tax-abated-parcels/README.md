# Tax-abated Parcels

Parcels within the City of Saint Louis that have obtained and activated an abatement on real estate taxes. Mirrored from [the city's open data portal](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=61); explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/business-and-industry/tax-abated-parcels/collection.json).

![st-louis](https://img.shields.io/badge/st--louis-blue) ![missouri](https://img.shields.io/badge/missouri-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![tax](https://img.shields.io/badge/tax-blue) ![abated](https://img.shields.io/badge/abated-blue) ![parcels](https://img.shields.io/badge/parcels-blue)

## Spatial Coverage

- **Bounding Box**: [-90.31351928596133, 38.53498170097803, -90.18332955134359, 38.748069216321845]

## Temporal Coverage

- **Start**: open
- **End**: ongoing

## Schema

| Column | Type | Description |
|--------|------|-------------|
| OBJECTID | int32 |  |
| LowerAsrParcelId | string |  |
| ColParcelId | string |  |
| ColCityBlock | int32 |  |
| ColParcel | int32 |  |
| PrimAddrRecNum | int32 |  |
| AddrType | string |  |
| LowAddrNum | int32 |  |
| LowAddrSuf | string |  |
| HighAddrNum | int32 |  |
| HighAddrSuf | string |  |
| NLC | int32 |  |
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
| AsrClassCode | int32 |  |
| AsrLandUse1 | int32 | Assessor land-use code (city 'Assessor Land Use' vocabulary; see parcels.AsrLandUse1). |
| AsrLanduse2 | int32 |  |
| RedevPhase | int32 |  |
| RedevYearEnd | int32 |  |
| RedevPhase2 | int32 |  |
| RedevYearEnd2 | int32 |  |
| VacantLot | int32 |  |
| SpecBusDist | int32 |  |
| SpecBusDist2 | int32 |  |
| TIFDist | int32 |  |
| LendingAgcy | int32 |  |
| Condominium | int32 |  |
| NbrOfUnits | int32 |  |
| NbrOfApts | int32 |  |
| FRONTAGE | double |  |
| LANDAREA | int32 |  |
| RecDailyDate | int64 |  |
| RecDailyNum | int32 |  |
| RecBookNum | string |  |
| RecPageNum | int32 |  |
| AsdLand | int32 |  |
| AsdImprove | int32 |  |
| AsdTotal | int32 |  |
| BillLand | int32 |  |
| BillImprove | int32 |  |
| BillTotal | int32 |  |
| AprLand | int32 |  |
| CostAprImprove | int32 |  |
| AsmtAppealYear | int32 |  |
| AsmtAppealNum | int32 |  |
| AsmtAppealType | string |  |
| PriorAsdDate | string |  |
| PriorAsdLand | int32 |  |
| PriorAsdImprove | int32 |  |
| PriorAsdTotal | int32 |  |
| PriorTaxAmt | int32 |  |
| CDALandUse1 | int32 |  |
| CDALandUse2 | int32 |  |
| LRMSUnitNum | string |  |
| Zoning | string |  |
| NbrOfBldgsRes | int32 |  |
| NbrOfBldgsCom | int32 |  |
| FirstYearBuilt | int32 |  |
| LastYearBuilt | int32 |  |
| ResSalePrice | int32 |  |
| ResSaleDate | int64 |  |
| VacBldgYear | int32 |  |
| GeoCityBlockPart | double |  |
| WARD10 | int32 |  |
| PRECINCT10 | int32 |  |
| INSPAREA10 | int32 |  |
| Ward00 | int32 |  |
| PRECINCT02 | int32 |  |
| PRECINCT04 | int32 |  |
| NBRHD | int32 |  |
| CDADIST | int32 |  |
| CDASUBDIST | int32 |  |
| POLICEDIST | int32 |  |
| CensTract10 | double |  |
| CensBlock10 | int32 |  |
| CensBlock00 | double |  |
| Ward90 | int32 |  |
| Precinct90 | int32 |  |
| CensBlock90 | double |  |
| HouseConsDist | int32 |  |
| ASRNBRHD | int32 |  |
| EntZone | int32 |  |
| IMPACTAREA | int32 |  |
| CTDArea | int32 |  |
| LEAFAREA | int32 |  |
| ZIP | int32 |  |
| OnFloodBlock | int32 |  |
| SpecParcelType | string |  |
| SubParcelType | string |  |
| NbrOfSubAccts | int32 |  |
| NbrOfCondos | int32 |  |
| LRMSParcel | int32 |  |
| AcctPrimary | int32 |  |
| HANDLE | string | Citywide parcel handle (join key to the parcels collections). |
| OWNEROCC | string |  |
| FirstDate | int64 |  |
| LastDate | int64 |  |
| OwnerUpdate | int64 |  |
| OwnerCode | int32 |  |
| SITEADDR | string |  |
| SQFT | int32 |  |
| ParcelId | string |  |
| WARD | int32 |  |
| TaxBalance | double |  |
| PropertyClassCode | int32 |  |
| IsAbatedProperty | int32 | Flag that the parcel has an active tax abatement (this collection shares the full assessor parcel schema — see the parcels collection for the other columns). |
| AbatementStartYear | int32 | First tax year of the abatement period. |
| AbatementEndYear | int32 | Last tax year of the abatement period. |
| SpecBusDist3 | int32 |  |
| Ward20 | int32 |  |
| Precinct20 | int32 |  |
| InspArea20 | int32 |  |
| CensTract20 | int32 |  |
| CensBlock20 | int32 |  |
| MaintZoneWC | int32 |  |
| TransDevDist | int32 |  |
| CityBlock | double |  |
| Parcel | int32 |  |
| Shape.STArea() | double |  |
| Shape.STLength() | double |  |
| geometry | binary |  |
| geometry_bbox | struct<xmin: float not null, ymin: float not null, xmax: float not null, ymax: float not null> |  |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./tax-abated-parcels.parquet | 457.2 KB | 1220d389acc8... |
| ./tax-abated-parcels.pmtiles | 316.3 KB | 1220ff680fc3... |
| ./styles/default.json | 1.3 KB | 1220ded37ced... |
| ./styles/style-expiring.json | 1.1 KB | 1220b7b8a843... |
| ./styles/style-solid.json | 548 B | 12204ac43989... |
| ./thumbnail.png | 369.5 KB | 12200794c846... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./tax-abated-parcels.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://static.stlouis-mo.gov/open-data/SLDC/TAX-ABATEMENT/taxabatedparcels.geojson](https://static.stlouis-mo.gov/open-data/SLDC/TAX-ABATEMENT/taxabatedparcels.geojson)

## Processing Notes

Mirrored from the City of St. Louis open data portal (https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=61).
Source: https://static.stlouis-mo.gov/open-data/SLDC/TAX-ABATEMENT/taxabatedparcels.geojson (portal download),
converted to GeoParquet (zstd, spatially ordered, covering bbox) and PMTiles.


## Attribution

City of St. Louis — St. Louis Development Corporation

## License

[other](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=61)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
