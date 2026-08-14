# ACS Demographics — Block Groups

Curated demographic, economic, housing and transportation indicators for all 314 census block groups in the City of St. Louis, from the U.S. Census Bureau's American Community Survey (ACS) 2020–2024 5-year estimates. The Census Bureau describes the ACS as "an ongoing survey that provides vital information on a yearly basis about our nation and its people" and "the premier source of detailed information about the nation's people and housing." Every indicator ships with its margin of error (`*_moe` — the Census Bureau publishes ACS margins at the 90% confidence level), and the headline medians and rates also carry a coefficient of variation (`*_cv`) so small-area noise can be flagged instead of mapped as if certain: at block-group scale margins are often large (one St. Louis block group's median household income is $76,466 ± $20,097). Derived percentages propagate error with the Census Bureau's own formulas from the ACS Accuracy of the Data documentation; ACS jam values for suppressed estimates are nulls here, never numbers; medians are published as-is and cannot be aggregated to larger areas. Each column's description names the exact ACS table it comes from.
Unlike the city's own datasets in this catalog, this is **not** City of St. Louis data: it is federal survey data published by the U.S. Census Bureau, extracted for St. Louis city (FIPS 29510) from the ACS table-based Summary File and joined to the Bureau's 2024 cartographic boundary geometries (1:500,000 scale, clipped to the Mississippi shoreline — TIGER/Line extends block groups into the river channel). It is included to show how a city catalog can blend federal demographic context alongside the city's own data. Explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/demographics/acs-block-groups/collection.json).

![census](https://img.shields.io/badge/census-blue) ![acs](https://img.shields.io/badge/acs-blue) ![demographics](https://img.shields.io/badge/demographics-blue) ![income](https://img.shields.io/badge/income-blue) ![poverty](https://img.shields.io/badge/poverty-blue) ![equity](https://img.shields.io/badge/equity-blue) ![block-groups](https://img.shields.io/badge/block--groups-blue) ![st-louis](https://img.shields.io/badge/st--louis-blue) ![open-data](https://img.shields.io/badge/open--data-blue)

## Spatial Coverage

- **Bounding Box**: [-90.32051589533225, 38.532001591520135, -90.16671561256314, 38.77428387126793]

## Temporal Coverage

- **Start**: 2020-01-01T00:00:00Z
- **End**: 2024-12-31T23:59:59Z

## Schema

| Column | Type | Description |
|--------|------|-------------|
| geoid | string | 12-digit census block group GEOID (state 29 + county 510 + tract + block group). Join key across the census family. |
| population | int64 | Total population. ACS table B01003. |
| population_moe | double | Margin of error for population at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| median_age | double | Median age in years. ACS table B01002. |
| median_age_moe | double | Margin of error for median_age at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_under_18 | double | Percent of the population under 18 years old. ACS table B01001. |
| pct_under_18_moe | double | Margin of error for pct_under_18 at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_65_plus | double | Percent of the population 65 years and over. ACS table B01001. |
| pct_65_plus_moe | double | Margin of error for pct_65_plus at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_white_nh | double | Percent of the population that is White alone, not Hispanic or Latino. ACS table B03002. |
| pct_white_nh_moe | double | Margin of error for pct_white_nh at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_black | double | Percent of the population that is Black or African American alone, not Hispanic or Latino. ACS table B03002. |
| pct_black_moe | double | Margin of error for pct_black at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_hispanic | double | Percent of the population that is Hispanic or Latino, of any race. ACS table B03002. |
| pct_hispanic_moe | double | Margin of error for pct_hispanic at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_bachelors_plus | double | Percent of the population 25 years and over holding a bachelor's degree or higher. ACS table B15003. |
| pct_bachelors_plus_moe | double | Margin of error for pct_bachelors_plus at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| median_hh_income | double | Median household income in the past 12 months, in 2024 inflation-adjusted dollars. ACS table B19013. |
| median_hh_income_moe | double | Margin of error for median_hh_income at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| median_hh_income_cv | double | Coefficient of variation for median_hh_income (moe / 1.645 / estimate): at or below 0.15 is reliable, 0.15–0.30 use with caution, above 0.30 unreliable. |
| per_capita_income | double | Per capita income in the past 12 months, in 2024 inflation-adjusted dollars. ACS table B19301. |
| per_capita_income_moe | double | Margin of error for per_capita_income at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_below_poverty | double | Percent of the population for whom poverty status is determined with income below the poverty level (income-to-poverty ratio under 1.00). ACS table C17002. |
| pct_below_poverty_moe | double | Margin of error for pct_below_poverty at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_below_poverty_cv | double | Coefficient of variation for pct_below_poverty (moe / 1.645 / estimate): at or below 0.15 is reliable, 0.15–0.30 use with caution, above 0.30 unreliable. |
| pct_below_2x_poverty | double | Percent of the population with an income-to-poverty ratio under 2.00. ACS table C17002. |
| pct_below_2x_poverty_moe | double | Margin of error for pct_below_2x_poverty at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_snap | double | Percent of households that received Food Stamps/SNAP in the past 12 months. ACS table B22010. |
| pct_snap_moe | double | Margin of error for pct_snap at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_unemployed | double | Unemployed as a percent of the civilian labor force (population 16 years and over). ACS table B23025. |
| pct_unemployed_moe | double | Margin of error for pct_unemployed at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| housing_units | int64 | Total housing units. ACS table B25002. |
| housing_units_moe | double | Margin of error for housing_units at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_vacant_units | double | Percent of housing units vacant. The ACS counts for-sale, for-rent and seasonal units as vacant — this is not the city's abandonment measure. ACS table B25002. |
| pct_vacant_units_moe | double | Margin of error for pct_vacant_units at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| households | int64 | Occupied housing units (households). ACS table B25003. |
| households_moe | double | Margin of error for households at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_owner_occupied | double | Percent of occupied housing units that are owner-occupied. ACS table B25003. |
| pct_owner_occupied_moe | double | Margin of error for pct_owner_occupied at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| median_gross_rent | double | Median gross rent in dollars per month. ACS table B25064. |
| median_gross_rent_moe | double | Margin of error for median_gross_rent at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| median_gross_rent_cv | double | Coefficient of variation for median_gross_rent (moe / 1.645 / estimate): at or below 0.15 is reliable, 0.15–0.30 use with caution, above 0.30 unreliable. |
| pct_rent_burdened | double | Percent of renter households paying 30 percent or more of household income on gross rent, excluding households where the ratio cannot be computed. ACS table B25070. |
| pct_rent_burdened_moe | double | Margin of error for pct_rent_burdened at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_rent_burdened_cv | double | Coefficient of variation for pct_rent_burdened (moe / 1.645 / estimate): at or below 0.15 is reliable, 0.15–0.30 use with caution, above 0.30 unreliable. |
| pct_severely_rent_burdened | double | Percent of renter households paying 50 percent or more of household income on gross rent, excluding households where the ratio cannot be computed. ACS table B25070. |
| pct_severely_rent_burdened_moe | double | Margin of error for pct_severely_rent_burdened at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| median_home_value | double | Median value of owner-occupied housing units in dollars. ACS table B25077. |
| median_home_value_moe | double | Margin of error for median_home_value at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| median_home_value_cv | double | Coefficient of variation for median_home_value (moe / 1.645 / estimate): at or below 0.15 is reliable, 0.15–0.30 use with caution, above 0.30 unreliable. |
| pct_built_pre_1940 | double | Percent of housing units built 1939 or earlier. ACS table B25034. |
| pct_built_pre_1940_moe | double | Margin of error for pct_built_pre_1940 at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_single_family | double | Percent of housing units that are single-family (1 unit, detached or attached). ACS table B25024. |
| pct_single_family_moe | double | Margin of error for pct_single_family at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| hh_no_vehicle | int64 | Occupied housing units with no vehicle available, owner- and renter-occupied combined. ACS table B25044. |
| hh_no_vehicle_moe | double | Margin of error for hh_no_vehicle at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_hh_no_vehicle | double | Percent of occupied housing units with no vehicle available. ACS table B25044. |
| pct_hh_no_vehicle_moe | double | Margin of error for pct_hh_no_vehicle at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_hh_no_vehicle_cv | double | Coefficient of variation for pct_hh_no_vehicle (moe / 1.645 / estimate): at or below 0.15 is reliable, 0.15–0.30 use with caution, above 0.30 unreliable. |
| pct_commute_drive_alone | double | Percent of workers 16 years and over who drove alone to work (car, truck, or van). ACS table B08301. |
| pct_commute_drive_alone_moe | double | Margin of error for pct_commute_drive_alone at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_commute_transit | double | Percent of workers 16 years and over who commuted by public transportation, excluding taxicab. ACS table B08301. |
| pct_commute_transit_moe | double | Margin of error for pct_commute_transit at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_commute_transit_cv | double | Coefficient of variation for pct_commute_transit (moe / 1.645 / estimate): at or below 0.15 is reliable, 0.15–0.30 use with caution, above 0.30 unreliable. |
| pct_commute_walk_bike | double | Percent of workers 16 years and over who walked or bicycled to work. ACS table B08301. |
| pct_commute_walk_bike_moe | double | Margin of error for pct_commute_walk_bike at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_work_from_home | double | Percent of workers 16 years and over who worked from home. ACS table B08301. |
| pct_work_from_home_moe | double | Margin of error for pct_work_from_home at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_commute_45min_plus | double | Percent of workers 16 years and over (not working at home) with a travel time to work of 45 minutes or more. ACS table B08303. |
| pct_commute_45min_plus_moe | double | Margin of error for pct_commute_45min_plus at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_no_internet | double | Percent of households with no internet access. ACS table B28002. |
| pct_no_internet_moe | double | Margin of error for pct_no_internet at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_no_internet_cv | double | Coefficient of variation for pct_no_internet (moe / 1.645 / estimate): at or below 0.15 is reliable, 0.15–0.30 use with caution, above 0.30 unreliable. |
| pct_no_computer | double | Percent of households with no computer. ACS table B28001. |
| pct_no_computer_moe | double | Margin of error for pct_no_computer at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_people_of_color | double | Percent of the population that is not White-alone non-Hispanic (the complement of pct_white_nh). ACS table B03002. |
| pct_people_of_color_moe | double | Margin of error for pct_people_of_color at the 90% confidence level (a complement carries the same error as pct_white_nh). |
| tract | string | 11-digit census tract GEOID (the first 11 characters of geoid); joins acs-tracts and cdc-places. |
| geometry | binary |  |
| bbox | struct<xmin: double, ymin: double, xmax: double, ymax: double> |  |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./acs-block-groups.parquet | 155.7 KB | 1220552647b0... |
| ./acs-block-groups.pmtiles | 1015.9 KB | 1220edc02983... |
| ./styles/default.json | 2.1 KB | 122021da37a1... |
| ./styles/internet.json | 1.6 KB | 12204ee76fc3... |
| ./styles/no-vehicle.json | 1.7 KB | 12201d5a9895... |
| ./styles/poverty.json | 1.6 KB | 1220638e99ad... |
| ./styles/race.json | 1.6 KB | 1220ea01a469... |
| ./styles/rent-burden.json | 1.6 KB | 12200707b5f8... |
| ./styles/transit-commute.json | 1.7 KB | 1220dfb079bc... |
| ./thumbnail.png | 333.6 KB | 12205bb63df9... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./acs-block-groups.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/](https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/)

## Processing Notes

Built from the ACS 2020–2024 5-year table-based Summary File (https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/): each national table file is one row per geography with estimate and margin of error side by side, and St. Louis city's rows are the ones whose GEO_ID starts with the city's FIPS code. No API key is involved — the Data API now requires one, the summary file does not.

ACS jam values (sentinels like -666666666 for a median that cannot be computed) were converted to nulls. Derived percentages propagate margins of error using the Census Bureau's own formulas from the ACS Accuracy of the Data documentation: sums add in quadrature, proportions use the subset formula with the ratio formula as fallback. Headline columns carry a coefficient of variation (moe / 1.645 / estimate). Every table line number used is checked against the release's own table-shells file at fetch time, so a vintage bump that moves a line fails loudly instead of publishing a mislabeled column.

Geometries are the Census Bureau's 2024 cartographic boundary block groups (1:500,000), reprojected to EPSG:4326 with ogr2ogr, filtered to county 510, and joined on GEOID. TIGER/Line was deliberately not used: it extends block groups into the Mississippi river channel, the cartographic files clip to the shoreline.

Converted to GeoParquet with gpio — zstd compression, Hilbert row order, and a covering bbox column with row-group statistics — and tiled to PMTiles with tippecanoe.


## Attribution

U.S. Census Bureau

## License

[other](https://www.census.gov/topics/research/research-transparency-public-access/open-data.html)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
