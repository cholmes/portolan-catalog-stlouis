# Electrical Permits

Data on commercial, industrial, and residential electrical permits in the City of St. Louis Mirrored from [the city's open data portal](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=51); explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/housing/electrical-permits/collection.json).

![st-louis](https://img.shields.io/badge/st--louis-blue) ![missouri](https://img.shields.io/badge/missouri-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![electrical](https://img.shields.io/badge/electrical-blue) ![permits](https://img.shields.io/badge/permits-blue)

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
| APPDATE | string | Date the permit application was filed. |
| APPDESCRIPTION | string | Free-text description of the permitted work. |
| APPNUM | string | Permit application number. |
| APPTYPE | string | Permit application type code; always 'AE' (Electrical) in this dataset — codes come from the city 'Permit Application Type' vocabulary (AB Building, AD Demolition, AE Electrical, AM Mechanical, AO Occupancy, AP Plumbing, etc.). |
| ASRNBRHD | string |  |
| CANCELDATE | string | Date the application was cancelled, if it was. |
| CANCELTYPE | string | Cancellation code; only the value 'C' (cancelled) appears in the data and the city publishes no decode for it. |
| CDADIST | string |  |
| CDASUBDIST | string |  |
| CENSBLOCK00 | string |  |
| CITYBLOCK | string | City block number of the permitted parcel; PARCEL is the parcel number within the block, PARCEL9 the nine-digit CityBlock+Parcel root. |
| COMPLETEDATE | string | Date the permitted work was completed/finaled. |
| ESTPROJECTCOST | string | Estimated project cost in dollars as declared on the application. |
| FIRSTDATE | string | Date the record first appeared in the extract; LASTDATE is its last update (name-based). |
| GEOCITYBLOCKPART | string |  |
| HANDLE | string | Citywide parcel handle the permit is attached to (join key to the parcels collections). |
| ISSUEDATE | string | Date the permit was issued. |
| LASTDATE | string |  |
| MAINSTRUCTYPE | string | Main structure type code, e.g. 1 One-or-Two Family, 2 Multi Family, 3 Hotel, 19 Industrial, 20 Commercial, 23 Garage (city 'Permit Structure Type' vocabulary); STRUCTYPE1-3 carry additional structure types. |
| NBRHD | string | City neighborhood number (city 'Neighborhood' vocabulary); ASRNBRHD is the assessor's neighborhood. |
| NBROFUNITS | string | Number of dwelling/occupancy units covered by the permit. |
| NLC | string |  |
| OWNERADDR | string |  |
| OWNERCITY | string |  |
| OWNERCODE | string | Taxing-status component of the parcel key (see parcels.OwnerCode decode). |
| OWNERNAME | string | Property owner of record at permit time (OWNERADDR/OWNERCITY/OWNERSTATE/OWNERZIP are the owner's mailing address). |
| OWNERSTATE | string |  |
| OWNERZIP | string |  |
| PARCEL | string |  |
| PARCEL9 | string |  |
| PARITY | string |  |
| POLICEDIST | string |  |
| PRCLERR | string | Parcel geocoding match/error code from the city's address-matching system (decode table CdPrclErr in the city's ComCode.mdb, e.g. 1-5 matches to non-LRMS addresses, 9 Outside City). |
| PRECINCT02 | string |  |
| PROJECTTYPE | string | Project type code: 1 New Construction, 2 Addition, 3 Alteration, 4 Repair, 5 Replacement, 6 Demolition, 7 Occupancy, 8 Blasting, 9 Other (city 'Permit Project Type' vocabulary). |
| STDIR | string |  |
| STNAME | string |  |
| STRUCTYPE1 | string |  |
| STRUCTYPE2 | string |  |
| STRUCTYPE3 | string |  |
| STTYPE | string |  |
| TMPCITYBLOCK | string |  |
| TMPPARCEL | string |  |
| UNITNUM | string |  |
| UPDATEGEO | string | Date/flag of the last geocoding update for the record (name-based). |
| WARD00 | string |  |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./electrical-permits.parquet | 13.6 MB | 122027f01174... |
| ./electrical-permits.pmtiles | 21.0 MB | 12206760edd2... |
| ./thumbnail.png | 393.1 KB | 122007b790b2... |
| ./styles/default.json | 1.4 KB | 122065ccc8c8... |
| ./styles/style-recent.json | 1.0 KB | 122064658524... |
| ./styles/style-solid.json | 534 B | 12204cb9eef2... |
| https://www.stlouis-mo.gov/data/upload/data-files/electrical-permits.zip | 21.6 MB | 1220c5debafd... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./electrical-permits.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://www.stlouis-mo.gov/data/upload/data-files/electrical-permits.zip](https://www.stlouis-mo.gov/data/upload/data-files/electrical-permits.zip)

## Processing Notes

Mirrored from the City of St. Louis open data portal (https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=51). Nothing was added to the data and no features were dropped except where noted below.

Downloaded from the city's portal: https://www.stlouis-mo.gov/data/upload/data-files/electrical-permits.zip (zipped CSV).

Converted to Parquet with gpio (zstd), keeping the source's own columns. The city publishes this without geometry, so it stays that way here.

The map layer is a derived product: the PMTiles were built by actually running the documented join against the `parcels` collection on parcel handle, so the data can be mapped without anyone having to run the join first. The Parquet is unjoined. The exact query is in AGENTS.md.

The city's own file(s) are published as `source` assets on this collection, linked directly to stlouis-mo.gov — this mirror never becomes the only way to reach the original.


## Attribution

City of St. Louis — Building Commissioner

## License

[other](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=51)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
