# Property Taxes

Property tax records by parcel Mirrored from [the city's open data portal](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=3); explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/government/property-taxes/collection.json).

![st-louis](https://img.shields.io/badge/st--louis-blue) ![missouri](https://img.shields.io/badge/missouri-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![property](https://img.shields.io/badge/property-blue) ![taxes](https://img.shields.io/badge/taxes-blue)

## Spatial Coverage

- **Bounding Box**: [-90.320522, 38.531907, -90.166409, 38.774362]

## Temporal Coverage

- **Start**: open
- **End**: ongoing

## Schema

| Column | Type | Description |
|--------|------|-------------|
| CityBlock | double | City block number, first component of the parcel key (portal: 'key fields: CITYBLOCK, PARCEL, OWNERCODE'). |
| Parcel | int64 | Parcel number within the city block, second component of the parcel key. |
| OwnerCode | int64 | Taxing-status component of the parcel key: 0 Standard, 1 Redev Taxable, 2 Redev Exempt, 3 In Lieu of Payment, 4 Charity Exempt, 5 Charity Taxable, 6 Mixed Res, 7 Mixed Comm, 8 Sign, 9 Demo/Maintenance Charge (city PrclCode.mdb CdOwnerCode). |
| AsrParcelId | string | The Assessor's parcel ID in the numbering schema introduced in 2021 (portal field definition for ParcelId). |
| ColParcelId | string | Unformatted Collector of Revenue parcel ID — the pre-2021 numbering scheme used across many city departments (portal field definition). |
| ColCityBlock | int64 |  |
| ColParcel | int64 |  |
| ParcelId | string | Unformatted parcel ID in the Assessor's 2021 numbering schema (portal field definition). |
| PrimAddrRecNum | int64 |  |
| AddrType | string |  |
| LowAddrNum | int64 | Lowest house number referencing this parcel on its primary street (portal field definition); HighAddrNum is the highest. |
| LowAddrSuf | string |  |
| HighAddrNum | int64 |  |
| HighAddrSuf | string |  |
| NLC | int64 | City internal numeric street code for the parcel's primary street (see parcels.NLC). |
| Parity | string |  |
| StPreDir | string |  |
| StName | string |  |
| StType | string |  |
| StSufDir | string |  |
| StdUnitNum | string |  |
| OwnerName | string |  |
| OwnerName2 | string |  |
| OwnerAddr | string |  |
| OwnerCity | string |  |
| OwnerState | string |  |
| OwnerCountry | string |  |
| OwnerZIP | string |  |
| OwnerRank | int64 |  |
| LegalDesc1 | string |  |
| LegalDesc2 | string |  |
| LegalDesc3 | string |  |
| LegalDesc4 | string |  |
| LegalDesc5 | string |  |
| AsrClassCode | int64 | Assessor's owner-class code (100 Individual, 200 Company, 49 Land Re-Utilization, etc.; city controlled vocabulary 'Assessor Class Code'). |
| PropertyClassCode | int64 | Statutory property classification: 10 Agricultural, 12 Commercial, 15 Residential, 17 Exempt, plus mixed-class combination codes (city controlled vocabulary 'Property Class Code'). |
| AsrLandUse1 | int64 | Assessor's primary land-use code (city controlled vocabulary 'Assessor Land Use'; e.g. 1110 Single Family Units, 1010 Vacant Residential Lot, 5000 Trade — see parcels.AsrLandUse1 for more codes). |
| AsrLanduse2 | int64 | Secondary land-use code, 'present, if necessary, otherwise 0' (portal field definition). |
| IsAbatedProperty | int64 | 0/1 flag that the parcel has a tax abatement. |
| AbatementType | string | Program under which the abatement was granted: CH99 Chapter 99, CH100 Chapter 100, CH353 Chapter 353, EEZ Enterprise Zone (city controlled vocabulary 'Abatement Type'). |
| AbatementStartYear | int64 | First tax year of the abatement period. |
| AbatementEndYear | int64 | Last tax year of the abatement period. |
| RedevPhase | int64 |  |
| RedevYearEnd | int64 |  |
| RedevPhase2 | int64 |  |
| RedevYearEnd2 | int64 |  |
| VacantLot | int64 | 0/1 vacant-lot flag (see parcels.VacantLot). |
| SpecBusDist | int64 |  |
| SpecBusDist2 | int64 |  |
| SpecBusDist3 | int64 |  |
| TIFDist | int64 |  |
| LendingAgcy | int64 |  |
| Condominium | int64 |  |
| NbrOfUnitsSource | int64 | Source system for the NbrOfUnits value: 1 DevNet Building Apartment Data, 2/3 DevNet Land Use with/without Building Rec, 10 Permits, 50 Pre-DevNet Parcel Unit Data, 110/120 overrides, 20 Other (city controlled vocabulary 'Number Of Units Source'). |
| NbrOfUnits | int64 |  |
| NbrOfApts | int64 |  |
| Frontage | double |  |
| LandArea | int64 |  |
| RecDailyDate | string | Recorder of Deeds daily-record date for the latest recorded instrument; RecDailyNum, RecBookNum and RecPageNum are the daily number and book/page references. |
| RecDailyNum | int64 |  |
| RecBookNum | string |  |
| RecPageNum | int64 |  |
| AsdLand | double | Assessed value of land in dollars (Missouri assessed value = 19% residential / 32% commercial / 12% agricultural of appraised value, RSMo 137.115). |
| AsdImprove | double | Assessed value of improvements in dollars. |
| AsdTotal | double | Total assessed value in dollars. |
| AsdResLand | double | Assessed land value attributed to the residential class portion (AsdResImprove, AsdComLand, AsdComImprove, AsdAgrLand, AsdAgrImprove are the parallel class-portion splits). |
| AsdResImprove | double |  |
| AsdComLand | double |  |
| AsdComImprove | double |  |
| AsdAgrLand | double |  |
| AsdAgrImprove | double |  |
| BillYear | int64 | Tax year of the bill the Bill* fields refer to. |
| BillSuffix | int64 |  |
| BillLand | double | Land assessed value as billed for BillYear; the Asd* vs Bill* distinction (current assessment vs billed assessment) is not formally documented on the portal. |
| BillImprove | double | Improvement assessed value as billed for BillYear. |
| BillTotal | double | Total assessed value as billed for BillYear. |
| BillResLand | double |  |
| BillResImprove | double |  |
| BillComLand | double |  |
| BillComImprove | double |  |
| BillAgrLand | double |  |
| BillAgrImprove | double |  |
| BillTaxAmt | double | Total tax amount billed for BillYear in dollars (name-based). |
| TaxBalDue | double | Outstanding tax balance due in dollars (name-based). |
| AprLand | double | Appraised (market) value of land in dollars; AprResLand/AprResImprove/AprComLand/AprComImprove/AprAgrLand/AprAgrImprove split it by property class, and AprExemptLand/AprExemptImprove carry exempt portions. |
| AprResLand | double |  |
| AprResImprove | double |  |
| AprComLand | double |  |
| AprComImprove | double |  |
| AprAgrLand | double |  |
| AprAgrImprove | double |  |
| AprExemptLand | double |  |
| AprExemptImprove | double |  |
| CostAprImprove | double | Cost-approach appraised value of improvements (name-based). |
| AsmtAppealYear | int64 |  |
| AsmtAppealNum | int64 |  |
| AsmtAppealType | string | Type of assessment appeal filed (city controlled vocabulary 'Assessment Appeal Type'). |
| PriorAsdDate | timestamp |  |
| PriorAsdLand | double | Assessed land value from the prior assessment (PriorAsdImprove/PriorAsdTotal/PriorAsdDate/PriorTaxAmt are the matching prior-cycle values). |
| PriorAsdImprove | double |  |
| PriorAsdTotal | double |  |
| PriorTaxAmt | double |  |
| CDALandUse1 | int64 |  |
| CDALandUse2 | int64 |  |
| LRMSUnitNum | string |  |
| Zoning | string |  |
| FormBasedDist1 | int64 |  |
| FormBasedType1 | string |  |
| FormBasedDist2 | int64 |  |
| FormBasedType2 | string |  |
| CUPArea | int64 |  |
| PUDArea | int64 |  |
| SPDArea | int64 |  |
| SUDArea | int64 |  |
| TODArea | int64 |  |
| NbrOfBldgsRes | int64 |  |
| NbrOfBldgsCom | int64 |  |
| FirstYearBuilt | int64 |  |
| LastYearBuilt | int64 |  |
| ResSalePrice | double |  |
| ResSaleDate | string |  |
| VacBldgYear | int64 |  |
| GeoCityBlockPart | double |  |
| Ward20 | int64 |  |
| Precinct20 | int64 |  |
| InspArea20 | int64 |  |
| Ward10 | int64 |  |
| Precinct10 | int64 |  |
| InspArea10 | int64 |  |
| Ward00 | int64 |  |
| Precinct02 | int64 |  |
| Precinct04 | int64 |  |
| Nbrhd | int64 |  |
| CDADist | int64 |  |
| CDASubDist | int64 |  |
| PoliceDist | int64 |  |
| IsHUDQualifiedTract | int64 | Flag that the parcel lies in a HUD Qualified Census Tract (name-based). |
| ComNeedGrantCode | int64 |  |
| CensTract20 | double |  |
| CensBlock20 | int64 |  |
| CensTract10 | double |  |
| CensBlock10 | int64 |  |
| CensBlock00 | double |  |
| Ward90 | int64 |  |
| Precinct90 | int64 |  |
| CensBlock90 | double |  |
| HouseConsDist | int64 |  |
| AsrNbrhd | int64 |  |
| EntZone | int64 |  |
| ImpactArea | int64 |  |
| CTDArea | int64 |  |
| LeafArea | int64 |  |
| MaintZoneWC | int64 |  |
| TransDevDist | int64 |  |
| BedBreakfastDist | int64 |  |
| CORTEXArea | int64 |  |
| Ch99Area | double |  |
| Ch100Area | int64 |  |
| Ch353Area | int64 |  |
| ParkNum | int64 |  |
| CityLandmark | int64 |  |
| CityLandmarkDist | int64 |  |
| CertLocalHistDist | int64 |  |
| LocalHistDist | int64 |  |
| NatHistDist | int64 |  |
| NatHistLandmark | int64 |  |
| NatRegSite | int64 |  |
| PresRevDist | int64 |  |
| ZIP | int64 |  |
| FloodPlain | int64 | Floodplain status of the parcel: 10/11 100-Year Flood all/part in, 50/51 500-Year Flood all/part in, 30/31 Levee all/part in (city controlled vocabulary 'Flood Plain Type'). |
| OnFloodBlock | int64 |  |
| SpecParcelType | string | Special-parcel type: C/K Condo Master, H Highway ROW, R Other ROW, S Special Account, W Water, X Non-parcel Area (city PrclCode.mdb CdSpecParcelType). |
| SubParcelType | string | Sub-parcel type code (A Account Separation, B Back Taxes Owed, C Condo, G Garage/Parking Condo, K Commercial Condo, M Multi-Owner, X Other, plus retirement codes; city 'Parcel Sub Type' vocabulary). |
| NbrOfSubAccts | int64 | Number of sub-accounts under this parcel (e.g. condo units billed separately; name-based). |
| NbrOfCondos | int64 | Number of condominium units associated with the parcel (name-based). |
| LRMSParcel | int64 | Flag/identifier linking the parcel to the city's LRMS land-records system (the LRMS acronym appears throughout city address vocabularies without an expansion; not formally documented). |
| AcctPrimary | int64 | Flag marking the primary account record for the parcel (name-based). |
| GisPrimary | int64 | Flag marking the record that represents the parcel in GIS when multiple accounts share a parcel (name-based); GisCityBLock/GisParcel/GisOwnerCode are the GIS-side key components. |
| GisCityBLock | double |  |
| GisParcel | int64 |  |
| GisOwnerCode | int64 |  |
| Handle | int64 | Citywide parcel join key (see parcels.HANDLE); the portal marks the numbering schema DEPRECATED. |
| Parcel9 | int64 | Nine-digit parcel root built from CityBlock and Parcel (schema BBBBbbPPP), described in legacy city documentation as the 'root of all taxable info'. |
| OwnerOcc | string | Owner-occupancy dwelling-type code: 1 Single Family, 2 Two-Family, 4 Three-or-Four Family, 5 Five-plus Family, C Condo, X Other (city PrclCode.mdb CdOwnerOccCode). |
| FirstDate | string | Date the record first appeared in the extract (name-based; not formally documented). |
| LastDate | timestamp | Date the record was last updated in the extract (name-based; not formally documented). |
| OwnerUpdate | string | Date of the last ownership update on the record (name-based; not formally documented). |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./property-taxes.parquet | 13.7 MB | 1220badeef09... |
| ./property-taxes.pmtiles | 22.6 MB | 12209e0adce7... |
| ./thumbnail.png | 382.7 KB | 1220bd41a282... |
| ./styles/default.json | 1.3 KB | 1220b7f6be0a... |
| ./styles/style-land-value.json | 1.3 KB | 122019ca0a76... |
| ./styles/style-solid.json | 506 B | 1220fa3a2804... |
| https://www.stlouis-mo.gov/data/upload/data-files/prcl.zip | 107.5 MB | 12202249855b... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./property-taxes.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://www.stlouis-mo.gov/data/upload/data-files/prcl.zip](https://www.stlouis-mo.gov/data/upload/data-files/prcl.zip)

## Processing Notes

Mirrored from the City of St. Louis open data portal (https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=3). Nothing was added to the data and no features were dropped except where noted below.

Downloaded from the city's portal: https://www.stlouis-mo.gov/data/upload/data-files/prcl.zip (zipped Microsoft Access database).

The Access database was unpacked and its `Prcl` table exported with `mdb-export` before conversion.

Converted to Parquet with gpio (zstd), keeping the source's own columns. The city publishes this without geometry, so it stays that way here.

The map layer is a derived product: the PMTiles were built by actually running the documented join against the `parcels` collection on parcel id, so the data can be mapped without anyone having to run the join first. The Parquet is unjoined. The exact query is in AGENTS.md.

The city's own file(s) are published as `source` assets on this collection, linked directly to stlouis-mo.gov — this mirror never becomes the only way to reach the original.


## Attribution

City of St. Louis — Assessor's Office

## License

[other](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=3)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
