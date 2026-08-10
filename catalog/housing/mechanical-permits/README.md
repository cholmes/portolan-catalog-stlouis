# Mechanical Permits

Mechanical permit information by property type, year, neighborhood, ward, and project type. Mirrored from [the city's open data portal](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=52); explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/housing/mechanical-permits/collection.json).

![st-louis](https://img.shields.io/badge/st--louis-blue) ![missouri](https://img.shields.io/badge/missouri-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![mechanical](https://img.shields.io/badge/mechanical-blue) ![permits](https://img.shields.io/badge/permits-blue)

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
| APPDATE | string | Date the permit application was filed; ISSUEDATE/COMPLETEDATE/CANCELDATE are the issue, completion and cancellation dates. |
| APPDESCRIPTION | string | Free-text description of the permitted work. |
| APPNUM | string | Permit application number. |
| APPTYPE | string | Permit application type code; 'AM' (Mechanical) in this dataset (city 'Permit Application Type' vocabulary). |
| ASRNBRHD | string |  |
| CANCELDATE | string |  |
| CANCELTYPE | string | Cancellation code; only 'C' appears and no decode is published. |
| CAREOFADDR | string |  |
| CAREOFCITY | string |  |
| CAREOFNAME | string | 'Care of' contact name on the application (CAREOFADDR/CAREOFCITY/CAREOFSTATE/CAREOFZIP are that contact's address). |
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
| MAINSTRUCTYPE | string | Main structure type code (city 'Permit Structure Type' vocabulary; STRUCTYPE1-3 are additional). |
| NBRHD | string |  |
| NBROFUNITS | string | Number of units covered by the permit. |
| NLC | string |  |
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
| PROJECTTYPE | string | Project type: 1 New Construction, 2 Addition, 3 Alteration, 4 Repair, 5 Replacement, 6 Demolition, 9 Other (city 'Permit Project Type' vocabulary). |
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
| ./mechanical-permits.parquet | 4.2 MB | 1220220e6613... |
| ./mechanical-permits.pmtiles | 10.7 MB | 1220443a5a77... |
| ./thumbnail.png | 391.6 KB | 12201051d41c... |
| ./styles/default.json | 1.4 KB | 12203a6a7a0f... |
| ./styles/style-recent.json | 1.0 KB | 122042891edb... |
| ./styles/style-solid.json | 534 B | 12204341e887... |
| https://www.stlouis-mo.gov/data/upload/data-files/mechanical-permits.zip | 6.3 MB | 1220953fd7d3... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./mechanical-permits.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://www.stlouis-mo.gov/data/upload/data-files/mechanical-permits.zip](https://www.stlouis-mo.gov/data/upload/data-files/mechanical-permits.zip)

## Processing Notes

Mirrored from the City of St. Louis open data portal (https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=52). Nothing was added to the data and no features were dropped except where noted below.

Downloaded from the city's portal: https://www.stlouis-mo.gov/data/upload/data-files/mechanical-permits.zip (zipped CSV).

Converted to Parquet with gpio (zstd), keeping the source's own columns. The city publishes this without geometry, so it stays that way here.

The map layer is a derived product: the PMTiles were built by actually running the documented join against the `parcels` collection on parcel handle, so the data can be mapped without anyone having to run the join first. The Parquet is unjoined. The exact query is in AGENTS.md.

The city's own file(s) are published as `source` assets on this collection, linked directly to stlouis-mo.gov — this mirror never becomes the only way to reach the original.


## Attribution

City of St. Louis — Building Commissioner

## License

[other](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=52)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
