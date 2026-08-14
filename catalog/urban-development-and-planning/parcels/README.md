# Parcels

Current and historic parcel data Mirrored from [the city's open data portal](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=82); explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/urban-development-and-planning/parcels/collection.json).

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
| LowerAsrParcelId | string | The Assessor's post-2021 parcel ID carried in lowercase/unformatted form (variant of AsrParcelId; not separately documented on the portal). |
| ColParcelId | string | Unformatted Collector of Revenue parcel ID — the pre-2021 parcel numbering scheme used across many city departments (portal field definition). |
| ColCityBlock | int32 | Collector of Revenue's city block number (portal field definition). |
| ColParcel | int32 | Collector of Revenue's parcel number, unique only within its parent city block (portal field definition). |
| PrimAddrRecNum | int16 | Record number of the parcel's primary address among its address records (name-based). |
| AddrType | string | Address-record type: 1 Assessor Legal Address, 2 Assessor Low/High Address, 3 Assessor Legal and Low/High Address, A Corrected/Added, L LRMS Address, P Permit non-Assessor Address, X Non-Assessor Parcel, plus dummy/retired codes Z/V/G/D/Q (city controlled vocabulary 'Address Type'). |
| LowAddrNum | int32 | Lowest house number that can be used to reference this parcel on its primary street (portal field definition). |
| LowAddrSuf | string |  |
| HighAddrNum | int32 | Highest house number that can be used to reference this parcel on its primary street (portal field definition). |
| HighAddrSuf | string |  |
| NLC | double | The city's internal numeric street code ('NLC') identifying the parcel's primary street in St. Louis address databases; street-name decode not published (type codes exist in the city's corcode.mdb CdNLCType table). |
| PARITY | string | Odd/even parity of the parcel's address numbers, i.e. which side of the street the parcel is on (name-based). |
| StPreDir | string |  |
| StName | string |  |
| StType | string |  |
| StSufDir | string |  |
| StdUnitNum | string |  |
| OWNERNAME | string | Owner name of record; OWNERADDR/OWNERCITY/OWNERSTATE/OWNERZIP are the owner's registered mailing address (portal field definitions for the historical extract). |
| OWNERNAME2 | string |  |
| OWNERADDR | string |  |
| OWNERCITY | string |  |
| OWNERSTATE | string |  |
| OwnerCountry | string |  |
| OWNERZIP | string |  |
| OwnerRank | string |  |
| LegalDesc1 | string | First line of the parcel's legal description (LegalDesc2-5 continue it). |
| LegalDesc2 | string |  |
| LegalDesc3 | string |  |
| LegalDesc4 | string |  |
| LegalDesc5 | string |  |
| AsrClassCode | int16 | Assessor's owner-class code identifying the type of owner, e.g. 100 Individual, 200 Company, 49 Land Re-Utilization (LRA), 14 State of Missouri, 2 MSD, plus many church/institution codes (city controlled vocabulary 'Assessor Class Code'). |
| AsrLandUse1 | int16 | Assessor's primary land-use code from the city's official 'Assessor Land Use' vocabulary (922 codes), e.g. 1110 Single Family Units, 1010 Vacant Residential Lot, 1120 Two Family Unit, 1130 Three Family Unit, 1140 Four Family Unit, 1115 Condominium (>6 units/bldg), 2000 Manufacturing, 3000 Industrial, 4000 Transportation/Communication/Utilities, 5000 Trade, 6000 Services, 7000 Cultural/Entertainment/Recreational, 9000 Undeveloped Land and Water Areas. |
| AsrLanduse2 | int16 | Assessor's secondary land-use code from the same vocabulary as AsrLandUse1; per the portal field definition it is 'present, if necessary, otherwise 0'. |
| RedevPhase | int16 | Redevelopment-abatement phase the parcel is in (city abatement programs are Chapter 99, Chapter 100, Chapter 353 and Enterprise Zone per the 'Abatement Type' vocabulary); phase decode not published. |
| RedevYearEnd | int16 | Year the parcel's current redevelopment phase ends. |
| RedevPhase2 | int16 |  |
| RedevYearEnd2 | int16 |  |
| VacantLot | int16 | 0/1 flag marking the parcel as a vacant lot (counterpart of the Y/N 'Vacant Land' field the portal documents for the historical parcels extract). |
| SpecBusDist | int16 | Special Business District / CID number the parcel falls in (city controlled vocabulary 'Special Business District CID'). |
| SpecBusDist2 | int16 |  |
| TIFDist | int16 | Tax Increment Financing district number the parcel falls in (city controlled vocabulary 'TIF District'). |
| LendingAgcy | int16 |  |
| Condominium | int16 | Condominium flag on the parcel record (legacy documentation shows it as a 0-or-8 component folded into HANDLE; inferred). |
| NbrOfUnits | int16 | Number of dwelling/occupancy units on the parcel. |
| NbrOfApts | int16 | Number of apartment units on the parcel (name-based). |
| FRONTAGE | double | Street frontage of the parcel, in feet (assessor lot dimension; portal label 'Frontage'). |
| LANDAREA | int32 | Assessor-recorded lot area in square feet (values match the parcel polygon's area computed in the foot-based state-plane geometry). |
| RecDailyDate | timestamp[ms] |  |
| RecDailyNum | int32 |  |
| RecBookNum | string |  |
| RecPageNum | int16 |  |
| AsdLand | double | Assessed value of the land portion of the parcel in dollars (in Missouri, assessed value is a statutory percentage of appraised value by property class: 19% residential, 32% commercial, 12% agricultural — RSMo 137.115). |
| AsdImprove | double | Assessed value of improvements (buildings) in dollars. |
| AsdTotal | double | Total assessed value (land + improvements) in dollars. |
| BillLand | double | Land assessed value as carried on the tax bill; the Asd*/Bill* distinction (current working assessment vs. billed assessment) is not formally documented on the portal. |
| BillImprove | double | Improvement assessed value as carried on the tax bill (see BillLand note). |
| BillTotal | double | Total assessed value as carried on the tax bill (see BillLand note). |
| AprLand | double | Appraised (market) value of the land in dollars, from which the assessed value is derived. |
| CostAprImprove | double | Cost-approach appraised value of improvements in dollars (name-based; no formal portal definition found). |
| AsmtAppealYear | int16 |  |
| AsmtAppealNum | int32 |  |
| AsmtAppealType | string |  |
| PriorAsdDate | timestamp[ms] |  |
| PriorAsdLand | double |  |
| PriorAsdImprove | double |  |
| PriorAsdTotal | double |  |
| PriorTaxAmt | double |  |
| CDALandUse1 | int16 | Land-use classification assigned by the CDA (Community Development Administration) planning scheme; no public decode table was found on the portal. |
| CDALandUse2 | int16 | Secondary CDA land-use classification; no public decode table was found on the portal. |
| LRMSUnitNum | string |  |
| Zoning | string | Zoning district code for the parcel (city controlled vocabulary 'Zoning Code'; see the zoning collection's LAYER letters for district names). |
| NbrOfBldgsRes | int16 |  |
| NbrOfBldgsCom | int16 |  |
| FirstYearBuilt | int16 | Year the oldest building on the parcel was built. |
| LastYearBuilt | int16 | Year the newest building on the parcel was built. |
| ResSalePrice | double | Most recent residential sale price for the parcel in dollars (name-based). |
| ResSaleDate | timestamp[ms] | Date of the most recent residential sale (name-based). |
| VacBldgYear | int16 | Year the property entered the vacant-building registry (counterpart of VACBLDGYR in the historical extract; name-based). |
| GeoCityBlockPart | double |  |
| WARD10 | int16 |  |
| PRECINCT10 | int16 |  |
| INSPAREA10 | int16 |  |
| Ward00 | int16 |  |
| PRECINCT02 | int16 |  |
| PRECINCT04 | int16 |  |
| NBRHD | int16 | City neighborhood number 1-79 (city controlled vocabulary 'Neighborhood'). |
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
| ASRNBRHD | int16 | Assessor's neighborhood number (assessment neighborhood, distinct from the citizen neighborhood in NBRHD). |
| EntZone | int16 |  |
| IMPACTAREA | int16 |  |
| CTDArea | int16 |  |
| LEAFAREA | int16 |  |
| ZIP | int32 |  |
| OnFloodBlock | int16 | Flag that the parcel's city block touches a floodplain (name-based; see the FloodPlain codes in property-taxes). |
| SpecParcelType | string | Special-parcel type: C Condo Master (Res/Mixed), K Condo Master (Non-Res), H Highway ROW, R Other ROW, S Special Account, W Water, X Non-parcel Area (city PrclCode.mdb CdSpecParcelType table). |
| SubParcelType | string | Sub-parcel type: A Account Separation, B Back Taxes Owed, C Condo, G Garage/Parking Condo, K Commercial Condo, I Industrial Condo, M Multi-Owner (e.g. leasehold), X Other (incl. signs, air/ground rights), plus bookkeeping codes D/E/P/Q/R/Y (city PrclCode.mdb CdSubParcelType / controlled vocabulary 'Parcel Sub Type'). |
| NbrOfSubAccts | int16 |  |
| NbrOfCondos | int16 |  |
| LRMSParcel | int16 |  |
| AcctPrimary | int16 |  |
| HANDLE | string | Zero-padded citywide parcel identifier used as the common join key across St. Louis parcel datasets; the portal's field notes describe it as 'a numbering schema originally introduced to aid in the handling of condominiums' and mark it DEPRECATED. |
| OWNEROCC | string | Owner-occupancy code giving the dwelling type of an owner-occupied parcel: 1 Single Family, 2 Two-Family, 4 Three-or-Four Family, 5 Five-plus Family, C Condo, X Other (city PrclCode.mdb CdOwnerOccCode table); null means not flagged owner-occupied. |
| FirstDate | timestamp[ms] |  |
| LastDate | timestamp[ms] |  |
| OwnerUpdate | timestamp[ms] |  |
| OwnerCode | int16 | Third component of the parcel key, a taxing-status code: 0 Standard, 1 Redevelopment Taxable Portion, 2 Redevelopment Exempt Portion, 3 In Lieu of Payment, 4 Charitable Exempt Portion, 5 Charitable Taxable Portion, 6 Mixed Use Residential Portion, 7 Mixed Use Commercial Portion, 8 Sign, 9 Demo/Maintenance Charge (city PrclCode.mdb CdOwnerCode table). |
| SITEADDR | string | Main address used for the parcel within city records (portal field definition). |
| SQFT | int32 | Parcel area in square feet (matches the GIS polygon area; essentially duplicates LANDAREA where both are populated). |
| ParcelId | string | Unformatted parcel ID in the numbering schema introduced by the Assessor's office in 2021 (portal field definition). |
| WARD | int16 | Current aldermanic ward number; Ward20/Ward10/Ward00/Ward90 columns carry the 2020/2010/2000/1990 ward definitions respectively. |
| TaxBalance | double | Outstanding (unpaid) property-tax balance for the parcel in dollars (name-based; no formal portal definition found). |
| PropertyClassCode | int16 | Statutory property classification: 10 Agricultural, 12 Commercial, 15 Residential, 17 Exempt, and combination codes 11/13/14/16 for mixed classifications (city controlled vocabulary 'Property Class Code'). |
| IsAbatedProperty | int16 | 0/1 flag indicating the parcel currently has a tax abatement (see AbatementStartYear/AbatementEndYear). |
| AbatementStartYear | int16 | First tax year of the parcel's tax-abatement period. |
| AbatementEndYear | int16 | Last tax year of the parcel's tax-abatement period. |
| SpecBusDist3 | int16 |  |
| Ward20 | int16 |  |
| Precinct20 | int16 |  |
| InspArea20 | int16 |  |
| CensTract20 | int16 |  |
| CensBlock20 | int16 |  |
| MaintZoneWC | int16 |  |
| TransDevDist | int16 |  |
| SHAPE | binary |  |
| CityBlock | double | City block number component of the parcel key (portal: 'key fields: CITYBLOCK, PARCEL, OWNERCODE'); a float-like identifier where the decimal part distinguishes block subdivisions. |
| Parcel | double | Parcel number within the city block, the second component of the CityBlock/Parcel/OwnerCode parcel key. |
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
| https://static.stlouis-mo.gov/open-data/ASSESSOR/PARCELS.zip | 37.2 MB | 12208764dc57... |
| https://static.stlouis-mo.gov/open-data/PLANNING/parcels/parcels-basic-info.csv | 14.5 MB | 122070546fdf... |

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

Mirrored from the City of St. Louis open data portal (https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=82). Nothing was added to the data and no features were dropped except where noted below.

Extracted from the city's own ArcGIS REST service with the Portolan CLI:

    portolan extract arcgis \
      https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/PARCELS_PUBLIC/MapServer --raw

That pages the service's `/query` endpoint for every feature, so this is the whole layer rather than the display-capped sample a browser request returns, and it carries across the service's field aliases. The service's own ESRI renderer was captured at the same time and is republished here as `styles/city-renderer.json`, so the map can be drawn in the city's own symbology.

Converted to GeoParquet with gpio — zstd compression, Hilbert row order, and a covering bbox column with row-group statistics, so a spatial filter can skip most of the file over the network — and tiled to PMTiles with tippecanoe.

The city's own file(s) are published as `source` assets on this collection, linked directly to stlouis-mo.gov — this mirror never becomes the only way to reach the original.


## Attribution

City of St. Louis — Assessor's Office

## License

[other](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=82)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
