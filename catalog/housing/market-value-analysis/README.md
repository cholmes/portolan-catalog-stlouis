# 2024 Market Value Analysis

The Market Value Analysis (MVA) is an in-depth study and mapping of a community's housing market. It reveals the mosaic of market conditions in St. Louis. Mirrored from [the city's open data portal](https://stlcity.maps.arcgis.com/home/item.html?id=e71e3ebca1f345a4b7db134d30c5d9ff); explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/housing/market-value-analysis/collection.json).

![st-louis](https://img.shields.io/badge/st--louis-blue) ![missouri](https://img.shields.io/badge/missouri-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![market](https://img.shields.io/badge/market-blue) ![value](https://img.shields.io/badge/value-blue) ![analysis](https://img.shields.io/badge/analysis-blue)

## Spatial Coverage

- **Bounding Box**: [-90.3205212204446, 38.5320191205876, -90.1667231932123, 38.7742951688267]

## Temporal Coverage

- **Start**: open
- **End**: ongoing

## Schema

| Column | Type | Description |
|--------|------|-------------|
| OBJECTID | int64 |  |
| geoid | string | Census 2020 block group code (AGOL layer documentation). |
| MVACluster | string | Market cluster letter assigned to the block group by Reinvestment Fund's 2024 Market Value Analysis of St. Louis — clusters group block groups with similar housing-market conditions. |
| MSP2123_CA | int32 | Median sales price of residential home sales 2021-2023, excluding sales under $1,000, condo-adjusted (AGOL layer documentation). |
| MSPVar2123 | float | Variation of home values 2021-2023 (standard deviation divided by average value). |
| PHHOO | float | Households that reported owning their home as a share of all households, ACS 2018-2022. |
| CHHOO | int32 | Count of households that reported owning their homes, ACS 2018-2022 (documented as 'CHOO' in the layer description). |
| CHH | int32 | Count of all households, ACS 2018-2022 (documented as 'CHIH' in the layer description). |
| PPerm10k | float | Share of residential parcels with renovation/addition permits June 2022-June 2024 whose total permit value exceeded $10,000 (excluding demolitions). |
| CPerm10k | int32 | Count of residential parcels with such >$10,000 renovation/addition permits, June 2022-June 2024. |
| CResPcl | int32 | Count of residential parcels in the block group (denominator for the parcel-share indicators; AGOL description text is garbled for this field). |
| PDSale2123 | float | Distressed residential sales (foreclosures, sheriff sales, tax sales, bank-sold) as a share of residential transactions 2021-2023. |
| CDSale2123 | int32 | Count of distressed residential home sales 2021-2023. |
| CSales2123 | int32 | Count of residential home sales 2021-2023. |
| PVacBuild | float | Vacant housing units as a share of all housing units, 2024. |
| CVacBuild | int32 | Count of vacant housing units. |
| CHU_All | int32 | Count of all housing units. |
| PVResLand | float | Vacant residential land as a share of all residential land, 2024. |
| VacLotAcre | double | Vacant residential land area in acres. |
| PclResAcre | double | Residential land area in acres. |
| PResArea | float | Residential land area as a share of all land area, 2024. |
| PclAcres | double | All land area in acres. |
| Subsidy | float | Share of households with a housing subsidy (LIHTC, Public Housing, Housing Choice Voucher, Multifamily), from the National Housing Preservation Database/HUD-POSH/St. Louis Housing Authority. |
| CSubHH | double | Count of households with a housing subsidy (same sources as Subsidy). |
| CHHRO | int32 | Count of renter households, ACS 2018-2022. |
| CPOP | int32 | Total population count, ACS 2018-2022. |
| CPOPWH | int32 | Non-Hispanic white population count, ACS 2018-2022. |
| CPOPBK | int32 | Non-Hispanic Black population count, ACS 2018-2022. |
| CPOPAS | int32 | Non-Hispanic Asian population count, ACS 2018-2022. |
| CPOPHISP | int32 | Hispanic population count, ACS 2018-2022. |
| CPOPOTH | int32 | Other-race population count, ACS 2018-2022. |
| Shape__Area | double |  |
| Shape__Length | double |  |
| geometry | binary |  |
| bbox | struct<xmin: double, ymin: double, xmax: double, ymax: double> |  |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./market-value-analysis.parquet | 278.2 KB | 1220d62d2583... |
| ./market-value-analysis.pmtiles | 772.2 KB | 1220441ae2d6... |
| ./styles/city-renderer.json | 1007 B | 1220e783c4b1... |
| ./styles/default.json | 1.9 KB | 12203597c5ea... |
| ./styles/style-sale-price.json | 1.4 KB | 12205fef56c8... |
| ./styles/style-vacancy-rate.json | 1.3 KB | 12208dfc0c19... |
| ./thumbnail.png | 402.7 KB | 122008bcb57c... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./market-value-analysis.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/2024_Market_Value_Analysis/FeatureServer](https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/2024_Market_Value_Analysis/FeatureServer)

## Processing Notes

Mirrored from the City of St. Louis open data portal (https://stlcity.maps.arcgis.com/home/item.html?id=e71e3ebca1f345a4b7db134d30c5d9ff). Nothing was added to the data and no features were dropped except where noted below.

Extracted from the city's own ArcGIS REST service with the Portolan CLI:

    portolan extract arcgis \
      https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/2024_Market_Value_Analysis/FeatureServer --raw

That pages the service's `/query` endpoint for every feature, so this is the whole layer rather than the display-capped sample a browser request returns, and it carries across the service's field aliases. The service's own ESRI renderer was captured at the same time and is republished here as `styles/city-renderer.json`, so the map can be drawn in the city's own symbology.

Converted to GeoParquet with gpio — zstd compression, Hilbert row order, and a covering bbox column with row-group statistics, so a spatial filter can skip most of the file over the network — and tiled to PMTiles with tippecanoe.


## Attribution

City of St. Louis — Community Development Administration

## License

[other](https://stlcity.maps.arcgis.com/home/item.html?id=e71e3ebca1f345a4b7db134d30c5d9ff)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
