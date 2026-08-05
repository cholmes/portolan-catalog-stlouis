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

Mirrored from the City of St. Louis open data portal (https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=69).
Source: https://www.slmpd.org/crime_stats.shtml (portal download),
converted to GeoParquet (zstd, spatially ordered, covering bbox) and PMTiles.


## Attribution

City of St. Louis — Metropolitan Police Department

## License

[other](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=69)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
