# CDC PLACES Health Measures

Forty model-based health measures for all 104 census tracts in the City of St. Louis, from the CDC's PLACES project. CDC describes PLACES as providing "health and health-related data using small area estimation for counties, incorporated and census designated places, census tracts, and ZIP Code Tabulation Areas (ZCTAs) across the United States," with "model-based estimates based on data from the Behavioral Risk Factor Surveillance System (BRFSS), Census decennial population counts and annual county population estimates, and the American Community Survey (ACS) 5-year estimates." Measures span health outcomes (asthma, diabetes, obesity, depression), prevention (checkups, screenings, insurance), health risk behaviors (smoking, binge drinking), disabilities, and health-related social needs (food insecurity, housing insecurity, transportation barriers, utility shut-off risk). Each measure is a crude-prevalence percentage of adults with 95% confidence limits in `*_lo`/`*_hi` columns; column descriptions carry each measure's full name and data year (2022 or 2023 depending on the measure, per the PLACES 2025 release).
These are **modeled estimates, not direct survey measurements of St. Louis residents** — CDC's small-area models combine national survey responses with local population characteristics, so tract values are best used for ranking and pattern-finding, not as precise local measurements. Unlike the city's own datasets in this catalog, this is **not** City of St. Louis data: it is published by the Centers for Disease Control and Prevention, extracted for St. Louis city (FIPS 29510) from the PLACES tract-level release and joined to the Census Bureau's 2024 cartographic boundary geometries. Explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/demographics/cdc-places/collection.json).

![cdc](https://img.shields.io/badge/cdc-blue) ![places](https://img.shields.io/badge/places-blue) ![health](https://img.shields.io/badge/health-blue) ![small-area-estimates](https://img.shields.io/badge/small--area--estimates-blue) ![tracts](https://img.shields.io/badge/tracts-blue) ![st-louis](https://img.shields.io/badge/st--louis-blue) ![open-data](https://img.shields.io/badge/open--data-blue)

## Spatial Coverage

- **Bounding Box**: [-90.32051589533225, 38.532001591520135, -90.16671561256314, 38.77428387126793]

## Temporal Coverage

- **Start**: 2022-01-01T00:00:00Z
- **End**: 2023-12-31T23:59:59Z

## Schema

| Column | Type | Description |
|--------|------|-------------|
| geoid | string | 11-digit census tract GEOID. Joins acs-tracts.geoid and the tract prefix of acs-block-groups. |
| total_population | int64 | Tract total population as carried in the PLACES release. |
| access2 | double | Current lack of health insurance among adults aged 18-64 years — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| access2_lo | double | Lower 95% confidence limit for access2. |
| access2_hi | double | Upper 95% confidence limit for access2. |
| arthritis | double | Arthritis among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| arthritis_lo | double | Lower 95% confidence limit for arthritis. |
| arthritis_hi | double | Upper 95% confidence limit for arthritis. |
| binge | double | Binge drinking among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| binge_lo | double | Lower 95% confidence limit for binge. |
| binge_hi | double | Upper 95% confidence limit for binge. |
| bphigh | double | High blood pressure among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| bphigh_lo | double | Lower 95% confidence limit for bphigh. |
| bphigh_hi | double | Upper 95% confidence limit for bphigh. |
| bpmed | double | Taking medicine to control high blood pressure among adults with high blood pressure — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| bpmed_lo | double | Lower 95% confidence limit for bpmed. |
| bpmed_hi | double | Upper 95% confidence limit for bpmed. |
| cancer | double | Cancer (non-skin) or melanoma among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| cancer_lo | double | Lower 95% confidence limit for cancer. |
| cancer_hi | double | Upper 95% confidence limit for cancer. |
| casthma | double | Current asthma among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| casthma_lo | double | Lower 95% confidence limit for casthma. |
| casthma_hi | double | Upper 95% confidence limit for casthma. |
| chd | double | Coronary heart disease among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| chd_lo | double | Lower 95% confidence limit for chd. |
| chd_hi | double | Upper 95% confidence limit for chd. |
| checkup | double | Visits to doctor for routine checkup within the past year among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| checkup_lo | double | Lower 95% confidence limit for checkup. |
| checkup_hi | double | Upper 95% confidence limit for checkup. |
| cholscreen | double | Cholesterol screening among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| cholscreen_lo | double | Lower 95% confidence limit for cholscreen. |
| cholscreen_hi | double | Upper 95% confidence limit for cholscreen. |
| cognition | double | Cognitive disability among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| cognition_lo | double | Lower 95% confidence limit for cognition. |
| cognition_hi | double | Upper 95% confidence limit for cognition. |
| colon_screen | double | Colorectal cancer screening among adults aged 45–75 years — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2022). |
| colon_screen_lo | double | Lower 95% confidence limit for colon_screen. |
| colon_screen_hi | double | Upper 95% confidence limit for colon_screen. |
| copd | double | Chronic obstructive pulmonary disease among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| copd_lo | double | Lower 95% confidence limit for copd. |
| copd_hi | double | Upper 95% confidence limit for copd. |
| csmoking | double | Current cigarette smoking among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| csmoking_lo | double | Lower 95% confidence limit for csmoking. |
| csmoking_hi | double | Upper 95% confidence limit for csmoking. |
| dental | double | Visited dentist or dental clinic in the past year among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2022). |
| dental_lo | double | Lower 95% confidence limit for dental. |
| dental_hi | double | Upper 95% confidence limit for dental. |
| depression | double | Depression among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| depression_lo | double | Lower 95% confidence limit for depression. |
| depression_hi | double | Upper 95% confidence limit for depression. |
| diabetes | double | Diagnosed diabetes among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| diabetes_lo | double | Lower 95% confidence limit for diabetes. |
| diabetes_hi | double | Upper 95% confidence limit for diabetes. |
| disability | double | Any disability among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| disability_lo | double | Lower 95% confidence limit for disability. |
| disability_hi | double | Upper 95% confidence limit for disability. |
| emotionspt | double | Lack of social and emotional support among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| emotionspt_lo | double | Lower 95% confidence limit for emotionspt. |
| emotionspt_hi | double | Upper 95% confidence limit for emotionspt. |
| foodinsecu | double | Food insecurity in the past 12 months among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| foodinsecu_lo | double | Lower 95% confidence limit for foodinsecu. |
| foodinsecu_hi | double | Upper 95% confidence limit for foodinsecu. |
| foodstamp | double | Received food stamps in the past 12 months among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| foodstamp_lo | double | Lower 95% confidence limit for foodstamp. |
| foodstamp_hi | double | Upper 95% confidence limit for foodstamp. |
| ghlth | double | Fair or poor self-rated health status among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| ghlth_lo | double | Lower 95% confidence limit for ghlth. |
| ghlth_hi | double | Upper 95% confidence limit for ghlth. |
| hearing | double | Hearing disability among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| hearing_lo | double | Lower 95% confidence limit for hearing. |
| hearing_hi | double | Upper 95% confidence limit for hearing. |
| highchol | double | High cholesterol among adults who have ever been screened — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| highchol_lo | double | Lower 95% confidence limit for highchol. |
| highchol_hi | double | Upper 95% confidence limit for highchol. |
| housinsecu | double | Housing insecurity in the past 12 months among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| housinsecu_lo | double | Lower 95% confidence limit for housinsecu. |
| housinsecu_hi | double | Upper 95% confidence limit for housinsecu. |
| indeplive | double | Independent living disability among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| indeplive_lo | double | Lower 95% confidence limit for indeplive. |
| indeplive_hi | double | Upper 95% confidence limit for indeplive. |
| lacktrpt | double | Lack of reliable transportation in the past 12 months among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| lacktrpt_lo | double | Lower 95% confidence limit for lacktrpt. |
| lacktrpt_hi | double | Upper 95% confidence limit for lacktrpt. |
| loneliness | double | Loneliness among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| loneliness_lo | double | Lower 95% confidence limit for loneliness. |
| loneliness_hi | double | Upper 95% confidence limit for loneliness. |
| lpa | double | No leisure-time physical activity among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| lpa_lo | double | Lower 95% confidence limit for lpa. |
| lpa_hi | double | Upper 95% confidence limit for lpa. |
| mammouse | double | Mammography use among women aged 50-74 years — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2022). |
| mammouse_lo | double | Lower 95% confidence limit for mammouse. |
| mammouse_hi | double | Upper 95% confidence limit for mammouse. |
| mhlth | double | Frequent mental distress among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| mhlth_lo | double | Lower 95% confidence limit for mhlth. |
| mhlth_hi | double | Upper 95% confidence limit for mhlth. |
| mobility | double | Mobility disability among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| mobility_lo | double | Lower 95% confidence limit for mobility. |
| mobility_hi | double | Upper 95% confidence limit for mobility. |
| obesity | double | Obesity among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| obesity_lo | double | Lower 95% confidence limit for obesity. |
| obesity_hi | double | Upper 95% confidence limit for obesity. |
| phlth | double | Frequent physical distress among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| phlth_lo | double | Lower 95% confidence limit for phlth. |
| phlth_hi | double | Upper 95% confidence limit for phlth. |
| selfcare | double | Self-care disability among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| selfcare_lo | double | Lower 95% confidence limit for selfcare. |
| selfcare_hi | double | Upper 95% confidence limit for selfcare. |
| shututility | double | Utility services shut-off threat in the past 12 months among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| shututility_lo | double | Lower 95% confidence limit for shututility. |
| shututility_hi | double | Upper 95% confidence limit for shututility. |
| sleep | double | Short sleep duration among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2022). |
| sleep_lo | double | Lower 95% confidence limit for sleep. |
| sleep_hi | double | Upper 95% confidence limit for sleep. |
| stroke | double | Stroke among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| stroke_lo | double | Lower 95% confidence limit for stroke. |
| stroke_hi | double | Upper 95% confidence limit for stroke. |
| teethlost | double | All teeth lost among adults aged >=65 years — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2022). |
| teethlost_lo | double | Lower 95% confidence limit for teethlost. |
| teethlost_hi | double | Upper 95% confidence limit for teethlost. |
| vision | double | Vision disability among adults — model-based crude prevalence, percent of adults (CDC PLACES, BRFSS 2023). |
| vision_lo | double | Lower 95% confidence limit for vision. |
| vision_hi | double | Upper 95% confidence limit for vision. |
| geometry | binary |  |
| bbox | struct<xmin: double, ymin: double, xmax: double, ymax: double> |  |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./cdc-places.parquet | 99.4 KB | 122037c3cad4... |
| ./cdc-places.pmtiles | 473.3 KB | 1220405aa15d... |
| ./styles/default.json | 1.6 KB | 12200db3f5a1... |
| ./styles/asthma.json | 1.6 KB | 12204d3da7a3... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./cdc-places.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://data.cdc.gov/resource/cwsq-ngmh](https://data.cdc.gov/resource/cwsq-ngmh)

## Processing Notes

Fetched from the CDC PLACES census-tract release via the Socrata API (https://data.cdc.gov/resource/cwsq-ngmh, dataset cwsq-ngmh) filtered to county FIPS 29510, then pivoted from one-row-per-measure to one-row-per-tract with a value, lower and upper 95% confidence limit column per measure. All rows are crude prevalence (the only value type CDC publishes at tract level; the fetch asserts this). Joined to the 2024 cartographic boundary tracts on GEOID.

Converted to GeoParquet with gpio and tiled to PMTiles with tippecanoe.


## Attribution

Centers for Disease Control and Prevention

## License

[other](https://www.cdc.gov/other/agencymaterials.html)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
