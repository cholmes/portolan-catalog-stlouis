# Crime (NIBRS)

Downloadable NIBRS crime data published by the St. Louis Metropolitan Police Department. Mirrored from [the city's open data portal](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=69); explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/law-safety-and-justice/crime/collection.json).

![st-louis](https://img.shields.io/badge/st--louis-blue) ![missouri](https://img.shields.io/badge/missouri-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![crime](https://img.shields.io/badge/crime-blue)

## Spatial Coverage

- **Bounding Box**: [-90.325252, 38.530218, -90.17843, 38.777615]

## Temporal Coverage

- **Start**: open
- **End**: ongoing

## Schema

| Column | Type | Description |
|--------|------|-------------|
| IncidentDate | date32[day] | Date the incident was reported/recorded by SLMPD. |
| OccurredFromTime | string | Date/time the offense began (NIBRS incidents record an occurred-from time). |
| IncidentNum | string | SLMPD incident (complaint) number; multiple offense rows can share one incident. |
| Offense | string | SLMPD's Missouri statutory offense description for the charge (e.g. 'MURDER 1ST DEGREE', 'STEALING - MOTOR VEHICLE'). |
| NIBRS | string | FBI NIBRS offense code for the offense, e.g. 09A Murder/Nonnegligent Manslaughter, 13A Aggravated Assault, 23G Theft of Motor Vehicle Parts, 240 Motor Vehicle Theft, 290 Destruction/Damage/Vandalism (FBI NIBRS offense code list). |
| NIBRSCategory | string | FBI NIBRS offense category name corresponding to the NIBRS code (e.g. 'Motor Vehicle Theft', 'Aggravated Assault'). |
| SRS_UCR | string | Legacy FBI Summary Reporting System (SRS/UCR) Part I offense class for the offense: 01 Criminal Homicide, 02 Rape, 03 Robbery, 04 Aggravated Assault, 05 Burglary, 06 Larceny-Theft, 07 Motor Vehicle Theft, 08 Arson (null for non-Part-I offenses). |
| CrimeAgainst | string | NIBRS 'Crimes Against' classification of the offense: Person, Property, or Society (FBI NIBRS groups every offense this way); 'Unspecified' appears for some records. |
| FelMisdCit | string | Charge-severity flag: F felony, M misdemeanor, with C and I also present (per the column name 'Fel/Misd/Cit' C is presumably citation and I infraction; SLMPD publishes no decode). |
| IncidentTopSRS_UCR | string | SRS/UCR class of the most serious offense in the incident (the SRS hierarchy rule reports only the highest offense; inferred from the field name and the SRS hierarchy convention). |
| IncidentLocation | string | Street address or block-level location of the incident. |
| IntersectionOtherLoc | string | Intersection or other non-address location description for the incident. |
| District | string | SLMPD police district number where the incident occurred. |
| Neighborhood | string | City neighborhood name of the incident location; NbhdNum is the corresponding neighborhood number (1-79 per the city 'Neighborhood' vocabulary). |
| NbhdNum | string |  |
| IncidentSupplemented | string | Yes/No — whether the incident record has been supplemented (updated) since the original report. |
| LastSuppDate | string | Date of the most recent supplement to the incident record. |
| VictimNum | string | Victim record identifier assigned by SLMPD (an ID shared by rows describing the same victim, not a count of victims — verified against the data). |
| FirearmUsed | string | Whether a firearm was used in the offense. |
| IncidentNature | string | Nature-of-incident text as recorded by SLMPD. |
| keep | bool | Flag added by this mirror's pipeline: true when the record had valid coordinates falling inside the city boundary (geometry is null when false). |
| geometry | binary |  |
| geometry_bbox | struct<xmin: float not null, ymin: float not null, xmax: float not null, ymax: float not null> |  |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./crime.parquet | 10.4 MB | 122030b8ecad... |
| ./crime.pmtiles | 5.3 MB | 122085d2f723... |
| ./styles/default.json | 1.7 KB | 122064c26483... |
| ./styles/style-category.json | 2.0 KB | 122069865461... |
| ./styles/style-firearm.json | 1.2 KB | 12203d45cd2a... |
| ./thumbnail.png | 430.4 KB | 122073d5e0b2... |
| https://slmpd.org/wp-content/uploads/2024/03/2021-2023.csv | 41.4 MB | 122064ea4355... |
| https://slmpd.org/wp-content/uploads/2024/03/January2024.csv | 1.4 MB | 1220dc14e9c3... |
| https://slmpd.org/wp-content/uploads/2024/03/February2024.csv | 1.2 MB | 1220a826a72c... |
| https://slmpd.org/wp-content/uploads/2024/05/Downloadable-NIBRS-Crime-File-March-2024-CSV.csv | 1.5 MB | 122059dce0c5... |
| https://slmpd.org/wp-content/uploads/2024/05/Downloadable-NIBRS-Crime-File-April-2024-CSV.csv | 1.7 MB | 1220ed5b261d... |
| https://slmpd.org/wp-content/uploads/2024/06/May2024.csv | 1.8 MB | 1220408b5ae5... |
| https://slmpd.org/wp-content/uploads/2024/07/June2024.csv | 1.8 MB | 12201bee7fbd... |
| https://slmpd.org/wp-content/uploads/2024/08/July2024.csv | 1.8 MB | 1220987e6ff9... |
| https://slmpd.org/wp-content/uploads/2024/09/August2024.csv | 1.8 MB | 122059c33702... |
| https://slmpd.org/wp-content/uploads/2024/10/September2024.csv | 1.7 MB | 12200e572515... |
| https://slmpd.org/wp-content/uploads/2024/11/October2024.csv | 1.7 MB | 1220ef80bd79... |
| https://slmpd.org/wp-content/uploads/2024/12/November2024.csv | 1.6 MB | 1220a871b166... |
| https://slmpd.org/wp-content/uploads/2025/01/December2024.csv | 1.5 MB | 122013d6498e... |
| https://slmpd.org/wp-content/uploads/2025/02/January2025.csv | 1.5 MB | 12200ebf3af9... |
| https://slmpd.org/wp-content/uploads/2025/03/February2025.csv | 1.4 MB | 122013681129... |
| https://slmpd.org/wp-content/uploads/2025/04/March2025.csv | 1.5 MB | 1220b12b07cf... |
| https://slmpd.org/wp-content/uploads/2025/05/April2025.csv | 1.6 MB | 1220fe9662e6... |
| https://slmpd.org/wp-content/uploads/2025/06/May2025.csv | 1.7 MB | 12207864d40f... |
| https://slmpd.org/wp-content/uploads/2025/07/June2025.csv | 1.8 MB | 12202a85e89f... |
| https://slmpd.org/wp-content/uploads/2025/08/July2025.csv | 1.8 MB | 12208e870130... |
| https://slmpd.org/wp-content/uploads/2025/09/August2025.csv | 1.8 MB | 1220fe5548bf... |
| https://slmpd.org/wp-content/uploads/2025/10/September2025.csv | 1.7 MB | 1220cbbe9363... |
| https://slmpd.org/wp-content/uploads/2025/11/October2025.csv | 1.7 MB | 122078ea24ea... |
| https://slmpd.org/wp-content/uploads/2025/12/November2025.csv | 1.6 MB | 1220dad2d292... |
| https://slmpd.org/wp-content/uploads/2026/01/December2025.csv | 1.5 MB | 122062e115e6... |
| https://slmpd.org/wp-content/uploads/2026/02/January2026.csv | 1.6 MB | 122043f70b3c... |
| https://slmpd.org/wp-content/uploads/2026/03/February2026.csv | 1.4 MB | 122014f8f59c... |
| https://slmpd.org/wp-content/uploads/2026/04/March2026.csv | 1.5 MB | 1220a335ae5f... |
| https://slmpd.org/wp-content/uploads/2026/05/April2026.csv | 1.6 MB | 122069151ea9... |
| https://slmpd.org/wp-content/uploads/2026/06/May2026.csv | 1.6 MB | 12201b982a62... |
| https://slmpd.org/wp-content/uploads/2026/07/June2026.csv | 1.5 MB | 122087b1db93... |
| https://slmpd.org/wp-content/uploads/2026/08/July2026.csv | 1.6 MB | 1220928070fb... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./crime.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://www.slmpd.org/crime_stats.shtml](https://www.slmpd.org/crime_stats.shtml)

## Processing Notes

Mirrored from the City of St. Louis open data portal (https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=69). Nothing was added to the data and no features were dropped except where noted below.

SLMPD does not publish a single file or a service — it posts one CSV per month on https://www.slmpd.org/crime_stats.shtml, and the portal's dataset page just points there. The index is read and every CSV it links is downloaded, so the mirror carries whatever months were published at sync time.

The monthly files arrive in mixed encodings, so each was normalized to UTF-8 before they were merged into one table.

Converted to GeoParquet with gpio — zstd compression, Hilbert row order, and a covering bbox column with row-group statistics, so a spatial filter can skip most of the file over the network — and tiled to PMTiles with tippecanoe.

The city's own file(s) are published as `source` assets on this collection, linked directly to stlouis-mo.gov — this mirror never becomes the only way to reach the original.


## Attribution

City of St. Louis — Metropolitan Police Department

## License

[other](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=69)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
