# CSB Service Requests (311)

The Citizens' Service Bureau (CSB) is the customer service department for the City of St. Louis. This dataset provides access to some of the data collected when services are requested. The X/Y coordinates are in WGS 84 Web Mercator (EPSG:3857). File new service request here: [https://www.stlouis-mo.gov/government/departments/public-safety/neighborhood-stabilization-office/citizens-service-bureau/csb-request-submit.cfm](https://www.stlouis-mo.gov/government/departments/public-safety/neighborhood-stabilization-office/citizens-service-bureau/csb-request-submit.cfm) Mirrored from [the city's open data portal](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=5); explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/government/csb-311-requests/collection.json).

![st-louis](https://img.shields.io/badge/st--louis-blue) ![missouri](https://img.shields.io/badge/missouri-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![csb](https://img.shields.io/badge/csb-blue) ![311](https://img.shields.io/badge/311-blue) ![requests](https://img.shields.io/badge/requests-blue)

## Spatial Coverage

- **Bounding Box**: [-90.3196727, 38.5338176, -90.1808012, 38.7741115]

## Temporal Coverage

- **Start**: open
- **End**: ongoing

## Schema

| Column | Type | Description |
|--------|------|-------------|
| CALLERTYPE | string | Method used by the customer to report the issue — Phone, Web, Twitter, CSB LTR, CSB VCML, etc. (portal field definition). |
| CITY | string |  |
| DATECANCELLED | timestamp[ms] | Date cancelled — indicates the request was a duplicate, cancelled by the caller, or entered in error (portal field definition). |
| DATEINVTDONE | timestamp[ms] | Date the investigation/inspection was done, which may differ from when a clerk closed the request (portal field definition). |
| DATETIMECLOSED | timestamp[ms] | Date/time the request was closed, auto-stamped when an employee closed it (portal field definition). |
| DATETIMEINIT | timestamp[ms] | Date/time the request was initiated, auto-stamped when saved or submitted online (portal field definition). |
| DESCRIPTION | string | Same as the problem code or a more specific explanation of it (portal field definition). |
| EXPLANATION | string | Additional details about the problem code, including the conditions under which it should be used (portal field definition). |
| GRANDPARENT_ID | int32 |  |
| GRANDPARENT_NODE | string |  |
| GROUP | string | Category the Citizens' Service Bureau currently groups that request type within (portal field definition). |
| NEIGHBORHOOD | string | City neighborhood number 1-79 of the problem location (portal field definition, city 'Neighborhood' vocabulary). |
| PARENT_ID | int32 | Identifier of the parent problem-code node in the CSB problem-code hierarchy (GRANDPARENT_ID/PARENT_NODE/GRANDPARENT_NODE are the higher levels; inferred from names — not in the portal field list). |
| PARENT_NODE | string |  |
| PLAIN_ENGLISH_NAME_FOR_PROBLEMCODE | string |  |
| PRJCOMPLETEDATE | timestamp[ms] | Projected completion date — the date by which the responsible division (SUBMITTO) should have the initial inspection completed (portal field definition). |
| PROBADDRESS | string | Address or intersection where the problem is occurring (portal field definition). |
| PROBADDTYPE | string | Problem address type: A = Parcel, B = Intersection (portal field definition). |
| PROBLEMCODE | string | Type of report — the CSB problem code (portal field definition); PLAIN_ENGLISH_NAME_FOR_PROBLEMCODE is its public title. |
| PROBLEMSID | int32 | Internal identifier of the problem record (name-based; not in the portal field list). |
| PROBZIP | string | ZIP code of the problem location, often blank (portal field definition). |
| PUBLICRESOLUTION | string | Public-facing resolution text recorded when the request was resolved (name-based; not in the portal field list). |
| REQUESTID | int32 | System-generated unique record number for the service request (portal field definition). |
| STATUS | string | Status of the request (portal field definition). |
| SUBMITTO | string | City division or department responsible for handling the request (portal field definition). |
| WARD | string | Ward number of the problem location (portal field definition). |
| geometry | binary |  |
| geometry_bbox | struct<xmin: float not null, ymin: float not null, xmax: float not null, ymax: float not null> |  |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./csb-311-requests.parquet | 77.6 MB | 122050da5a4f... |
| ./csb-311-requests.pmtiles | 52.4 MB | 122089ff9f7b... |
| ./styles/default.json | 845 B | 1220cbed61a9... |
| ./styles/style-category.json | 2.0 KB | 122020fe23e1... |
| ./styles/style-channel.json | 1.7 KB | 12201e1515b0... |
| ./styles/style-open.json | 1.5 KB | 1220181d4924... |
| ./thumbnail.png | 369.3 KB | 1220dca6c185... |
| https://www.stlouis-mo.gov/data/upload/data-files/csb.zip | 120.4 MB | 1220dd704169... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./csb-311-requests.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://www.stlouis-mo.gov/data/upload/data-files/csb.zip](https://www.stlouis-mo.gov/data/upload/data-files/csb.zip)

## Processing Notes

Mirrored from the City of St. Louis open data portal (https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=5). Nothing was added to the data and no features were dropped except where noted below.

Downloaded from the city's portal: https://www.stlouis-mo.gov/data/upload/data-files/csb.zip (zipped CSVs, one per year).

The yearly CSVs arrive in mixed UTF-8 and Windows-1252 and were normalized to UTF-8. Coordinates come as Web Mercator `SRX`/`SRY` columns and were reprojected to EPSG:4326; points falling outside the city were set to null rather than dropped, and the roughly 18,000 requests with no coordinates at all are kept as null-geometry rows so the counts still match the city's.

Converted to GeoParquet with gpio — zstd compression, Hilbert row order, and a covering bbox column with row-group statistics, so a spatial filter can skip most of the file over the network — and tiled to PMTiles with tippecanoe.

The city's own file(s) are published as `source` assets on this collection, linked directly to stlouis-mo.gov — this mirror never becomes the only way to reach the original.


## Attribution

City of St. Louis — Neighborhood Stabilization / CSB

## License

[other](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=5)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
