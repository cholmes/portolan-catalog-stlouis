# November 2024 Election Results by Precinct

This is the detailed vote extract (dve) from the November 5, 2024, General Municipal Election for the City of St. Louis. Mirrored from [the city's open data portal](https://stlcity.maps.arcgis.com/home/item.html?id=6e72fa855cd445f7af37d79615f602d0); explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/government/election-results-nov-2024/collection.json).

![st-louis](https://img.shields.io/badge/st--louis-blue) ![missouri](https://img.shields.io/badge/missouri-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![election](https://img.shields.io/badge/election-blue) ![results](https://img.shields.io/badge/results-blue) ![nov](https://img.shields.io/badge/nov-blue) ![2024](https://img.shields.io/badge/2024-blue)

## Spatial Coverage

- **Bounding Box**: [-90.320522, 38.531907, -90.166409, 38.774362]

## Temporal Coverage

- **Start**: 2024-11-05T00:00:00Z
- **End**: 2024-11-05T00:00:00Z

## Schema

| Column | Type | Description |
|--------|------|-------------|
| F_Precinct | string | Precinct label as reported in the November 2024 canvass file. |
| Precinct_ID | int64 | Precinct identifier. |
| Precinct_Reporting | string | Whether/what share of the precinct had reported. |
| Registered_Voters | int64 | Registered voters in the precinct. |
| Ballots_Cast | int64 | Ballots cast in the precinct; Turnout_Percentage is Ballots_Cast over Registered_Voters. |
| Turnout_Percentage | double |  |
| Contest_Title | string | Name of the contest (office or question); Contest_ID and Contest_Party identify it and its party where applicable. |
| Contest_ID | int64 |  |
| Contest_Party | json |  |
| Choice_Name | string | Candidate or ballot-choice name; Choice_ID and Choice_Party identify it. |
| Choice_ID | int64 |  |
| Choice_Party | string |  |
| Total_Votes | int64 | Total votes for the choice in the precinct across all voting modes. |
| Total_Overvotes | int64 | Overvotes — ballots where more choices were marked than allowed, so no vote counted (standard U.S. election tabulation term). |
| Total_Undervotes | int64 | Undervotes — ballots where fewer choices were marked than allowed (including blank), so a potential vote was not cast. |
| Total_Invalid_Votes | int64 |  |
| Absentee_Voting_Votes | int64 | Votes for the choice cast by mail absentee; the parallel *_Overvotes/*_Undervotes/*_Invalid_Votes columns break those measures out per voting mode. |
| Absentee_Voting_Overvotes | int64 |  |
| Absentee_Voting_Undervotes | int64 |  |
| Absentee_Voting_Invalid_Votes | int64 |  |
| Absentee_Voting___In_Person_Vot | int64 | Votes cast by in-person (no-excuse) absentee voting (column name truncated by the source; the __Ove/__Und/__Inv companions are its overvote/undervote/invalid counts). |
| Absentee_Voting___In_Person_Ove | int64 |  |
| Absentee_Voting___In_Person_Und | int64 |  |
| Absentee_Voting___In_Person_Inv | int64 |  |
| Election_Day_Voting_Votes | int64 | Votes for the choice cast at the polls on election day. |
| Election_Day_Voting_Overvotes | int64 |  |
| Election_Day_Voting_Undervotes | int64 |  |
| Election_Day_Voting_Invalid_Vot | int64 |  |
| Provisional_Voting_Votes | int64 | Votes for the choice cast on provisional ballots. |
| Provisional_Voting_Overvotes | int64 |  |
| Provisional_Voting_Undervotes | int64 |  |
| Provisional_Voting_Invalid_Vote | int64 |  |
| House_Votes_Votes | int64 |  |
| House_Votes_Overvotes | int64 |  |
| House_Votes_Undervotes | int64 |  |
| House_Votes_Invalid_Votes | int64 |  |
| ObjectId | int64 |  |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./election-results-nov-2024.parquet | 318.9 KB | 1220e10febd3... |
| ./election-results-nov-2024.pmtiles | 482.6 KB | 122077fec398... |
| ./thumbnail.png | 377.7 KB | 12209d524265... |
| ./styles/default.json | 1.6 KB | 1220e244bdbb... |
| ./styles/style-ballots.json | 1.2 KB | 1220a466882d... |
| ./styles/style-presidential.json | 1.6 KB | 1220a85d668f... |
| ./styles/style-registered.json | 1.3 KB | 12203cc4b6de... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./election-results-nov-2024.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/Nov24_Detailed_Vote_Totals_Test/FeatureServer](https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/Nov24_Detailed_Vote_Totals_Test/FeatureServer)

## Processing Notes

Mirrored from the City of St. Louis open data portal (https://stlcity.maps.arcgis.com/home/item.html?id=6e72fa855cd445f7af37d79615f602d0).
Source: https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/Nov24_Detailed_Vote_Totals_Test/FeatureServer (ArcGIS REST service),
converted to GeoParquet (zstd, spatially ordered, covering bbox) and PMTiles.


## Attribution

City of St. Louis — Board of Election Commissioners

## License

[other](https://stlcity.maps.arcgis.com/home/item.html?id=6e72fa855cd445f7af37d79615f602d0)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
