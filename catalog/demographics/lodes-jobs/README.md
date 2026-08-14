# LODES Jobs

Jobs by workplace and employed residents by home location for every census block group in the City of St. Louis, from the U.S. Census Bureau's LEHD Origin-Destination Employment Statistics (LODES) version 8, data year 2023. LODES is the block-level jobs data behind the Bureau's OnTheMap tool; "Version 8 of LODES was enumerated by 2020 census blocks." Workplace Area Characteristics (jobs located in the block group, `jobs_*`) and Residence Area Characteristics (employed people living in the block group, `workers_resident*`) are aggregated here from census blocks to block groups — a block's block group is the first 12 characters of its 15-character geocode — with breakdowns by earnings band and selected NAICS sectors. LEHD notes that "the data released by LEHD are based on tabulated and modeled administrative data, which are subject to error"; these are administrative tabulations, not survey estimates, so no margins of error apply.
Unlike the city's own datasets in this catalog, this is **not** City of St. Louis data: it is federal administrative data published by the U.S. Census Bureau's Longitudinal Employer-Household Dynamics program, extracted for St. Louis city (FIPS 29510) and joined to the Bureau's 2024 cartographic boundary geometries. Pair it with `acs-block-groups` to compare daytime (working) and residential population, or with `lodes-commutes` for the underlying home→work flows. Explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/demographics/lodes-jobs/collection.json).

![census](https://img.shields.io/badge/census-blue) ![lehd](https://img.shields.io/badge/lehd-blue) ![lodes](https://img.shields.io/badge/lodes-blue) ![jobs](https://img.shields.io/badge/jobs-blue) ![employment](https://img.shields.io/badge/employment-blue) ![block-groups](https://img.shields.io/badge/block--groups-blue) ![st-louis](https://img.shields.io/badge/st--louis-blue) ![open-data](https://img.shields.io/badge/open--data-blue)

## Spatial Coverage

- **Bounding Box**: [-90.32051589533225, 38.532001591520135, -90.16671561256314, 38.77428387126793]

## Temporal Coverage

- **Start**: 2023-01-01T00:00:00Z
- **End**: 2023-12-31T23:59:59Z

## Schema

| Column | Type | Description |
|--------|------|-------------|
| geoid | string | 12-digit census block group GEOID. Join key to acs-block-groups and lodes-commutes. |
| jobs_total | int64 | All jobs located in the block group (LODES WAC column C000), aggregated from census blocks. |
| jobs_earn_low | int64 | Jobs with earnings of $1,250/month or less (LODES CE01). |
| jobs_earn_mid | int64 | Jobs with earnings of $1,251 to $3,333/month (LODES CE02). |
| jobs_earn_high | int64 | Jobs with earnings greater than $3,333/month (LODES CE03). |
| jobs_manufacturing | int64 | Jobs in Manufacturing, NAICS sectors 31-33 (LODES CNS05). |
| jobs_retail | int64 | Jobs in Retail Trade, NAICS sectors 44-45 (LODES CNS07). |
| jobs_education | int64 | Jobs in Educational Services, NAICS sector 61 (LODES CNS15). |
| jobs_healthcare | int64 | Jobs in Health Care and Social Assistance, NAICS sector 62 (LODES CNS16). |
| jobs_food_accomm | int64 | Jobs in Accommodation and Food Services, NAICS sector 72 (LODES CNS18). |
| workers_resident | int64 | Employed people living in the block group, wherever they work (LODES RAC column C000). |
| workers_resident_earn_low | int64 | Employed residents earning $1,250/month or less (LODES RAC CE01). |
| workers_resident_earn_mid | int64 | Employed residents earning $1,251 to $3,333/month (LODES RAC CE02). |
| workers_resident_earn_high | int64 | Employed residents earning more than $3,333/month (LODES RAC CE03). |
| geometry | binary |  |
| bbox | struct<xmin: double, ymin: double, xmax: double, ymax: double> |  |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./lodes-jobs.parquet | 48.5 KB | 1220d44aae0c... |
| ./lodes-jobs.pmtiles | 182.1 KB | 122015712857... |
| ./styles/default.json | 1.6 KB | 1220f7462951... |
| ./styles/balance.json | 2.3 KB | 1220c79df5de... |
| ./thumbnail.png | 333.6 KB | 1220091152ed... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./lodes-jobs.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://lehd.ces.census.gov/data/lodes/LODES8/mo](https://lehd.ces.census.gov/data/lodes/LODES8/mo)

## Processing Notes

Built from LODES 8 Workplace Area Characteristics and Residence Area Characteristics for Missouri, 2023 (https://lehd.ces.census.gov/data/lodes/LODES8/mo/wac/, https://lehd.ces.census.gov/data/lodes/LODES8/mo/rac/, segment S000, job type JT00 — all jobs). Block-level counts were aggregated to block groups by GEOID prefix (a block's block group is the first 12 characters of its 15-character geocode) and joined to the 2024 cartographic boundary block groups. LODES omits blocks with zero jobs, so absent means zero — every one of the city's 314 block groups is present, zero-filled where LODES has no rows.

Converted to GeoParquet with gpio and tiled to PMTiles with tippecanoe.


## Attribution

U.S. Census Bureau

## License

[other](https://www.census.gov/topics/research/research-transparency-public-access/open-data.html)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
