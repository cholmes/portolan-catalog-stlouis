# ACS Demographics — Tracts

Indicators the U.S. Census Bureau publishes only at census-tract level — health insurance coverage, disability, nativity, group-quarters population, and race-iterated income and poverty — for all 104 census tracts in the City of St. Louis, from the American Community Survey (ACS) 2020–2024 5-year estimates. The Census Bureau describes the ACS as "an ongoing survey that provides vital information on a yearly basis about our nation and its people." The companion `acs-block-groups` collection carries the finer-grained indicators; this collection exists because tables like B27001 (health insurance), B18101 (disability), B05002 (nativity), B26001 (group quarters) and the race-iterated B19013B/B17020B have no block-group release. Population and median household income are repeated here as more statistically stable tract-level variants. Every estimate ships with its 90%-confidence margin of error (`*_moe`) and headline rates with a coefficient of variation (`*_cv`); jam values are nulls; each column's description names its ACS table.
Unlike the city's own datasets in this catalog, this is **not** City of St. Louis data: it is federal survey data published by the U.S. Census Bureau, extracted for St. Louis city (FIPS 29510) from the ACS table-based Summary File and joined to the Bureau's 2024 cartographic boundary geometries (1:500,000 scale, clipped to the Mississippi shoreline). Explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/demographics/acs-tracts/collection.json).

![census](https://img.shields.io/badge/census-blue) ![acs](https://img.shields.io/badge/acs-blue) ![demographics](https://img.shields.io/badge/demographics-blue) ![health-insurance](https://img.shields.io/badge/health--insurance-blue) ![disability](https://img.shields.io/badge/disability-blue) ![tracts](https://img.shields.io/badge/tracts-blue) ![st-louis](https://img.shields.io/badge/st--louis-blue) ![open-data](https://img.shields.io/badge/open--data-blue)

## Spatial Coverage

- **Bounding Box**: [-90.32051589533225, 38.532001591520135, -90.16671561256314, 38.77428387126793]

## Temporal Coverage

- **Start**: 2020-01-01T00:00:00Z
- **End**: 2024-12-31T23:59:59Z

## Schema

| Column | Type | Description |
|--------|------|-------------|
| geoid | string | 11-digit census tract GEOID (state 29 + county 510 + tract). Join key; equals the first 11 characters of a block-group geoid. |
| population | int64 | Total population. ACS table B01003. |
| population_moe | double | Margin of error for population at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| median_hh_income | double | Median household income in the past 12 months, in 2024 inflation-adjusted dollars. ACS table B19013. |
| median_hh_income_moe | double | Margin of error for median_hh_income at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| median_hh_income_cv | double | Coefficient of variation for median_hh_income (moe / 1.645 / estimate): at or below 0.15 is reliable, 0.15–0.30 use with caution, above 0.30 unreliable. |
| pct_below_poverty | double | Percent of the population for whom poverty status is determined with income below the poverty level (income-to-poverty ratio under 1.00). ACS table C17002. |
| pct_below_poverty_moe | double | Margin of error for pct_below_poverty at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_below_poverty_cv | double | Coefficient of variation for pct_below_poverty (moe / 1.645 / estimate): at or below 0.15 is reliable, 0.15–0.30 use with caution, above 0.30 unreliable. |
| pct_uninsured | double | Percent of the civilian noninstitutionalized population with no health insurance coverage. ACS table B27001. |
| pct_uninsured_moe | double | Margin of error for pct_uninsured at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_uninsured_cv | double | Coefficient of variation for pct_uninsured (moe / 1.645 / estimate): at or below 0.15 is reliable, 0.15–0.30 use with caution, above 0.30 unreliable. |
| pct_with_disability | double | Percent of the civilian noninstitutionalized population with a disability. ACS table B18101. |
| pct_with_disability_moe | double | Margin of error for pct_with_disability at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_with_disability_cv | double | Coefficient of variation for pct_with_disability (moe / 1.645 / estimate): at or below 0.15 is reliable, 0.15–0.30 use with caution, above 0.30 unreliable. |
| pct_foreign_born | double | Percent of the population that is foreign-born. ACS table B05002. |
| pct_foreign_born_moe | double | Margin of error for pct_foreign_born at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| group_quarters_pop | int64 | Population living in group quarters (dormitories, prisons, nursing facilities and similar) — flag tracts where this is large before computing per-capita rates from household-based columns. ACS table B26001. |
| group_quarters_pop_moe | double | Margin of error for group_quarters_pop at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| median_hh_income_black | double | Median household income in the past 12 months (2024 inflation-adjusted dollars) for households with a Black or African American alone householder. ACS table B19013B. |
| median_hh_income_black_moe | double | Margin of error for median_hh_income_black at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| median_hh_income_black_cv | double | Coefficient of variation for median_hh_income_black (moe / 1.645 / estimate): at or below 0.15 is reliable, 0.15–0.30 use with caution, above 0.30 unreliable. |
| pct_below_poverty_black | double | Percent of the Black or African American alone population for whom poverty status is determined with income below the poverty level. ACS table B17020B. |
| pct_below_poverty_black_moe | double | Margin of error for pct_below_poverty_black at the 90% confidence level (the level the Census Bureau publishes for ACS). |
| pct_below_poverty_black_cv | double | Coefficient of variation for pct_below_poverty_black (moe / 1.645 / estimate): at or below 0.15 is reliable, 0.15–0.30 use with caution, above 0.30 unreliable. |
| geometry | binary |  |
| bbox | struct<xmin: double, ymin: double, xmax: double, ymax: double> |  |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./acs-tracts.parquet | 42.8 KB | 1220744e3dfd... |
| ./acs-tracts.pmtiles | 195.8 KB | 12201944945d... |
| ./styles/default.json | 1.6 KB | 12208f66a1ff... |
| ./styles/disability.json | 1.6 KB | 1220884c08e0... |
| ./thumbnail.png | 321.5 KB | 1220dea51917... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./acs-tracts.parquet")
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

Geometries are the Census Bureau's 2024 cartographic boundary tracts (1:500,000), reprojected to EPSG:4326 with ogr2ogr, filtered to county 510, and joined on GEOID. TIGER/Line was deliberately not used: it extends tracts into the Mississippi river channel, the cartographic files clip to the shoreline.

Converted to GeoParquet with gpio — zstd compression, Hilbert row order, and a covering bbox column with row-group statistics — and tiled to PMTiles with tippecanoe.


## Attribution

U.S. Census Bureau

## License

[other](https://www.census.gov/topics/research/research-transparency-public-access/open-data.html)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
