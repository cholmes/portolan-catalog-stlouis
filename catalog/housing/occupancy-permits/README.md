# Occupancy Permits

Commercial, industrial, and occupancy building permits in the City of St. Louis Mirrored from [the city's open data portal](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=6); explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/housing/occupancy-permits/collection.json).

![st-louis](https://img.shields.io/badge/st--louis-blue) ![missouri](https://img.shields.io/badge/missouri-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![occupancy](https://img.shields.io/badge/occupancy-blue) ![permits](https://img.shields.io/badge/permits-blue)

## Spatial Coverage

- **Bounding Box**: [-90.320522, 38.531907, -90.166409, 38.774362]

## Temporal Coverage

- **Start**: open
- **End**: ongoing

## Schema

| Column | Type | Description |
|--------|------|-------------|
| ADDRADJUSTED | string |  |
| ADDRNUM | string |  |
| ADDRSUF | string |  |
| APPDATE | string | Date the occupancy-permit application was filed; ISSUEDATE/COMPLETEDATE/CANCELDATE are the issue, completion and cancellation dates. |
| APPDESCRIPTION | string |  |
| APPNUM | string | Permit application number. |
| APPTYPE | string | Permit application type code; 'AO' Occupancy (or 'AX' Occupancy-Old) per the city 'Permit Application Type' vocabulary. |
| ASRNBRHD | string |  |
| CANCELDATE | string |  |
| CANCELTYPE | string | Cancellation code; only 'C' appears and no decode is published. |
| CAREOFADDR | string |  |
| CAREOFCITY | string |  |
| CAREOFNAME | string |  |
| CAREOFSTATE | string |  |
| CAREOFZIP | string |  |
| CDADIST | string |  |
| CDASUBDIST | string |  |
| CENSBLOCK00 | string |  |
| CITYBLOCK | string |  |
| COMPLETEDATE | string |  |
| ESTPROJECTCOST | string | Estimated project cost in dollars. |
| FIRSTDATE | string |  |
| GEOCITYBLOCKPART | string |  |
| HANDLE | string | Citywide parcel handle (join key to parcels). |
| ISSUEDATE | string |  |
| LASTDATE | string |  |
| MAINSTRUCTYPE | string | Main structure type code (city 'Permit Structure Type' vocabulary). |
| NBRHD | string |  |
| NBROFUNITS | string | Number of units covered by the permit. |
| NEWUSE | string | Text description of the new (proposed) use of the structure. |
| NEWUSEGROUP1 | string | Building-code use group of the new use, e.g. A Assembly, B Business, E Educational, F Factory, H Hazardous, I Institutional, M Mercantile, R Residential, S Storage, U Utility with numeric subgroups like R-2, F-1 (city 'Permit Use Group' vocabulary); NEWUSEGROUP2-3 are additional groups. |
| NEWUSEGROUP2 | string |  |
| NEWUSEGROUP3 | string |  |
| NLC | string |  |
| OCCNAME | string | Name of the occupant/business applying for occupancy (name-based). |
| OLDUSE | string | Text description of the previous use of the structure. |
| OLDUSEGROUP1 | string | Building-code use group of the previous use (same vocabulary; OLDUSEGROUP2-3 additional). |
| OLDUSEGROUP2 | string |  |
| OLDUSEGROUP3 | string |  |
| OWNERADDR | string |  |
| OWNERCITY | string |  |
| OWNERCODE | string | Taxing-status component of the parcel key (see parcels.OwnerCode). |
| OWNERNAME | string |  |
| OWNERSTATE | string |  |
| OWNERZIP | string |  |
| PARCEL | string |  |
| PARCEL9 | string |  |
| PARITY | string |  |
| POLICEDIST | string |  |
| PRCLERR | string | Parcel geocoding match/error code (city ComCode.mdb CdPrclErr). |
| PRECINCT02 | string |  |
| PROJECTTYPE | string | Project type code; occupancy permits are type 7 'Occupancy' (city 'Permit Project Type' vocabulary). |
| STDIR | string |  |
| STNAME | string |  |
| STRUCTYPE1 | string |  |
| STRUCTYPE2 | string |  |
| STRUCTYPE3 | string |  |
| STTYPE | string |  |
| TMPCITYBLOCK | string |  |
| TMPPARCEL | string |  |
| UNITNUM | string |  |
| UPDATEGEO | string |  |
| WARD00 | string |  |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./occupancy-permits.parquet | 6.9 MB | 122038d953bc... |
| ./occupancy-permits.pmtiles | 10.9 MB | 122060527898... |
| ./thumbnail.png | 392.9 KB | 122072bae056... |
| ./styles/default.json | 1.4 KB | 1220b3aab725... |
| ./styles/style-recent.json | 1.0 KB | 1220d657de5c... |
| ./styles/style-solid.json | 532 B | 12203d9a9eb3... |
| https://www.stlouis-mo.gov/data/upload/data-files/occupancy-permits.zip | 9.9 MB | 12203522888d... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./occupancy-permits.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://www.stlouis-mo.gov/data/upload/data-files/occupancy-permits.zip](https://www.stlouis-mo.gov/data/upload/data-files/occupancy-permits.zip)

## Processing Notes

Mirrored from the City of St. Louis open data portal (https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=6). Nothing was added to the data and no features were dropped except where noted below.

Downloaded from the city's portal: https://www.stlouis-mo.gov/data/upload/data-files/occupancy-permits.zip (zipped CSV).

Converted to Parquet with gpio (zstd), keeping the source's own columns. The city publishes this without geometry, so it stays that way here.

The map layer is a derived product: the PMTiles were built by actually running the documented join against the `parcels` collection on parcel handle, so the data can be mapped without anyone having to run the join first. The Parquet is unjoined. The exact query is in AGENTS.md.

The city's own file(s) are published as `source` assets on this collection, linked directly to stlouis-mo.gov — this mirror never becomes the only way to reach the original.


## Attribution

City of St. Louis — Building Commissioner

## License

[other](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=6)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
