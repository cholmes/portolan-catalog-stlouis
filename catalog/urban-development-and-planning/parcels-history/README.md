# Parcels (Historical, 1997-2020)

Current and historic parcel data Mirrored from [the city's open data portal](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=82); explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/urban-development-and-planning/parcels-history/collection.json).

![st-louis](https://img.shields.io/badge/st--louis-blue) ![missouri](https://img.shields.io/badge/missouri-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![parcels](https://img.shields.io/badge/parcels-blue) ![history](https://img.shields.io/badge/history-blue)

## Spatial Coverage

- **Bounding Box**: [-90.32057687721576, 38.532670087845, -90.17512199644693, 38.77435160356174]

## Temporal Coverage

- **Start**: open
- **End**: ongoing

## Schema

| Column | Type | Description |
|--------|------|-------------|
| OBJECTID | int64 |  |
| HANDLE | string | Zero-padded handle identifier for parcels (official portal field definition for this dataset) — the join key across city parcel data. |
| COUNT_ | decimal128(18, 11) |  |
| SHAPE_Leng | decimal128(18, 11) |  |
| SHAPE_Area | decimal128(18, 11) |  |
| HANDLE_1 | string |  |
| UPDATED | date32[day] | Date the source snapshot record was updated (portal label 'UPDATED'). |
| SITEADDR | string | Site address of the parcel (portal label). |
| OWNERNAME | string | Owner name of record (OWNERNAME2 is the overflow line). |
| OWNERNAME2 | string |  |
| OWNERADDR | string | Owner's house number and street name mailing address (portal field definition); OWNERCITY/OWNERSTATE/OWNERZIP/OWNERCNTRY are the rest of the registered mailing address. |
| OWNERCITY | string |  |
| OWNERSTATE | string |  |
| OWNERCNTRY | string |  |
| OWNERZIP | string |  |
| OWNERGROUP | string | Owner grouping assigned in the source extract (portal label only; no decode published). |
| NUMUNITS | int64 | Number of units on the parcel (portal label). |
| ZONING1 | string | Zoning district code decoded by the city's 'Zoning Code' vocabulary (ZONING2-3 are additional districts where the parcel spans zones). |
| ZONING2 | string |  |
| ZONING3 | string |  |
| VACANTLAND | string | Vacant-land flag, 'Y' or 'N' (portal field definition). |
| ASMTLAND | decimal128(18, 11) | Assessment (assessed value) of land in dollars (portal label 'Assessment Land'). |
| ASMTIMPROV | decimal128(18, 11) | Assessment of improvements in dollars (portal label 'Assessment Improvements'). |
| ASMTTOTAL | decimal128(18, 11) | Total assessed value in dollars (portal label 'Assessment Total'). |
| LANDUSE1 | int32 | Land-use code decoded by the city's official 'Assessor Land Use' vocabulary, e.g. 1110 Single Family Units, 1010 Vacant Residential Lot (LANDUSE2-4 are additional codes; the portal maps these columns to that vocabulary). |
| LANDUSE2 | int32 |  |
| LANDUSE3 | int32 |  |
| LANDUSE4 | int32 |  |
| ASRUSE1 | int32 | Assessor use code (portal label 'Assessor Use Code'); the portal publishes no decode vocabulary for this column (ASRUSE2-4 likewise). |
| ASRUSE2 | int32 |  |
| ASRUSE3 | int32 |  |
| ASRUSE4 | int32 |  |
| ASRCLASS1 | int32 | Assessor class code — owner-type classification, decoded by the city's 'Assessor Class Code' vocabulary (ASRCLASS2-4 are additional codes). |
| ASRCLASS2 | int32 |  |
| ASRCLASS3 | int32 |  |
| ASRCLASS4 | int32 |  |
| LEGAL1 | string | First line of the legal description (LEGAL2-5 continue it; portal labels 'Legal Description'). |
| LEGAL2 | string |  |
| LEGAL3 | string |  |
| LEGAL4 | string |  |
| LEGAL5 | string |  |
| NUMBLDGS | int32 | Number of buildings on the parcel (portal label). |
| LANDAREA | decimal128(30, 11) | Lot area in square feet (portal label 'Land Area'; units per the current parcels extract where values match polygon areas in feet). |
| FRONTAGE | decimal128(18, 11) | Street frontage in feet (portal label 'Frontage'). |
| DAILYDATE | date32[day] | Recorder of Deeds daily-record date of the latest recorded instrument (portal label 'Daily Date'); DAILYNUM, BOOKNUM and BOOKPAGE are the daily number and deed book/page references. |
| DAILYNUM | string |  |
| BOOKNUM | string |  |
| BOOKPAGE | string |  |
| BDG1YEAR | int32 | Year built of building 1 (portal label 'Building 1 Year'); BDG1AREA is its area and BDG1EXWALL its exterior-wall code. |
| BDG1AREA | decimal128(30, 11) |  |
| BDG1EXWALL | int32 |  |
| BDG1STRYCD | int32 |  |
| BDG1OCCCD | int32 |  |
| CITYBLOCK | decimal128(18, 11) | City block number of the parcel key; PARCEL is the parcel number within the block. |
| PARCEL | int32 |  |
| PARITY | string |  |
| ADDRNUM | decimal128(30, 11) |  |
| ADDRSUF | string |  |
| STREETPRE | string |  |
| STREETNAME | string |  |
| STREETSUF | string |  |
| STRSUFDIR | string |  |
| UNITNUM | string |  |
| CDADIST | int32 |  |
| CDASUBDIST | int32 |  |
| WARD | int32 |  |
| PRECINCT | int32 |  |
| NBRHD | int32 | City neighborhood number (city 'Neighborhood' vocabulary). |
| CENSBLOCK | string |  |
| POLICEDIST | int32 |  |
| ZIP | decimal128(30, 11) |  |
| IMPACTAREA | int32 |  |
| HSCONSERV | int32 |  |
| PARCEL10 | string | Ten-digit parcel identifier (CityBlock+Parcel+OwnerCode form; see the legacy BBBBbbPPPO schema); PARCEL9 is the nine-digit CityBlock+Parcel root. |
| geometry | binary |  |
| geometry_bbox | struct<xmin: float, ymin: float, xmax: float, ymax: float> |  |
| era | string | Snapshot vintage added by this mirror: which yearly source extract (1997-2015 single years, plus a combined 2016-2020 file) the row came from. |
| OWNEROCC | string | Owner-occupancy dwelling-type code: 1 Single Family, 2 Two-Family, 4 Three-or-Four Family, 5 Five-plus Family, C Condo, X Other (city PrclCode.mdb CdOwnerOccCode). |
| VACBLDGYR | int32 | Year the property entered the vacant building registry (name-based). |
| ASRNBRHD | int32 | Assessor's assessment-neighborhood number. |
| PRECINCT02 | int32 |  |
| PRECINCT04 | int32 |  |
| UPDATED_1 | date32[day] |  |
| PARCEL9 | int64 |  |
| PRECINCT10 | int32 |  |
| INSPAREA10 | int32 |  |
| Shape_len | decimal128(18, 11) |  |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./parcels-history.parquet | 142.0 MB | 12200fff4bfb... |
| ./parcels-history.pmtiles | 33.2 MB | 1220f9b01b0c... |
| ./styles/default.json | 1.5 KB | 1220689b28ba... |
| ./styles/style-1997.json | 1.1 KB | 122005ebd500... |
| ./styles/style-2020.json | 1.0 KB | 1220cdd8fb56... |
| ./thumbnail.png | 598.8 KB | 12205e8080d7... |
| ./styles/style-zoning-1997.json | 2.1 KB | 122034b4142c... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./parcels-history.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://www.stlouis-mo.gov/data/upload/data-files/stl_parcels_1997-2000.zip](https://www.stlouis-mo.gov/data/upload/data-files/stl_parcels_1997-2000.zip)

## Processing Notes

Mirrored from the City of St. Louis open data portal (https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=82).
Source: https://www.stlouis-mo.gov/data/upload/data-files/stl_parcels_1997-2000.zip (portal download),
converted to GeoParquet (zstd, spatially ordered, covering bbox) and PMTiles.


## Attribution

City of St. Louis — Assessor's Office

## License

[other](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=82)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
