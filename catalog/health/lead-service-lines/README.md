# Lead Service Line Inventory

Lead Service Line Inventory Feature Layer Service Mirrored from [the city's open data portal](https://stlcity.maps.arcgis.com/home/item.html?id=80c69343cc2d418fb1796a342a863aac); explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/health/lead-service-lines/collection.json).

![st-louis](https://img.shields.io/badge/st--louis-blue) ![missouri](https://img.shields.io/badge/missouri-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![lead](https://img.shields.io/badge/lead-blue) ![service](https://img.shields.io/badge/service-blue) ![lines](https://img.shields.io/badge/lines-blue)

## Spatial Coverage

- **Bounding Box**: [-90.3196726708832, 38.5340158845404, -90.1810161864447, 38.7645417490548]

## Temporal Coverage

- **Start**: open
- **End**: ongoing

## Schema

| Column | Type | Description |
|--------|------|-------------|
| address | string | Street address of the water service connection (layer field alias 'Address'). |
| utilmaterial | int16 | Pipe material of the utility-owned (public right-of-way) side of the service line, coded: 0 Unknown, 81 Asbestos Cement, 83 Cast Iron, 84 Copper, 88 Ductile Iron, 89 Galvanized Pipe, 93 Polyethylene, 94 PVC, 109 Lead, 110 Brass (ArcGIS coded-value domain; alias 'Right of Way Material'). |
| utilsource | int16 | How the right-of-way side's material was determined: 1 Existing Records, 2 Test Results, 3 Visual Confirmation, 5 Assumed (ArcGIS coded-value domain 'Utility_Source') — the material-determination basis EPA's Lead and Copper Rule Revisions service-line inventories require. |
| utilstatus | int16 | Lead classification of the right-of-way side: 0 Unknown, 1 Lead, 2 Non-Lead, 3 Galvanized Requiring Replacement (ArcGIS domain; these are the four service-line categories of the EPA LCRR service line inventory). |
| custmaterial | int16 | Pipe material of the customer-owned (building) side of the service line, same material codes as utilmaterial (ArcGIS domain 'Water_Service_Material'; alias 'Building Side Material'). |
| custsource | int16 | How the building side's material was determined: 1 Existing Records, 2 Test Results, 3 Visual Confirmation, 4 Notified by Customer, 5 Assumed (ArcGIS domain 'Customer_Source'). |
| custstatus | int16 | Lead classification of the building side: 0 Unknown, 1 Lead, 2 Non-Lead, 3 Galvanized Requiring Replacement (ArcGIS domain 'Status'; EPA LCRR inventory categories). |
| OBJECTID | int64 | ArcGIS feature object ID. |
| GlobalID | string | ArcGIS global unique identifier for the feature. |
| geometry | binary |  |
| bbox | struct<xmin: double, ymin: double, xmax: double, ymax: double> |  |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./lead-service-lines.parquet | 8.5 MB | 12205a267c78... |
| ./lead-service-lines.pmtiles | 2.2 MB | 12208189bee6... |
| ./styles/city-renderer.json | 551 B | 1220f6a2278d... |
| ./styles/default.json | 1.8 KB | 122090dd0be2... |
| ./styles/style-customer-side.json | 1.7 KB | 1220e2ad8bc9... |
| ./styles/style-material.json | 2.2 KB | 1220b6416e1b... |
| ./thumbnail.png | 379.8 KB | 1220af3eb899... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./lead-service-lines.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/STLWD_LSLI__Read_Only_View/FeatureServer](https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/STLWD_LSLI__Read_Only_View/FeatureServer)

## Processing Notes

Mirrored from the City of St. Louis open data portal (https://stlcity.maps.arcgis.com/home/item.html?id=80c69343cc2d418fb1796a342a863aac). Nothing was added to the data and no features were dropped except where noted below.

Extracted from the city's own ArcGIS REST service with the Portolan CLI:

    portolan extract arcgis \
      https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/STLWD_LSLI__Read_Only_View/FeatureServer --raw

That pages the service's `/query` endpoint for every feature, so this is the whole layer rather than the display-capped sample a browser request returns, and it carries across the service's field aliases. The service's own ESRI renderer was captured at the same time and is republished here as `styles/city-renderer.json`, so the map can be drawn in the city's own symbology.

The service returns coded domain values; the material and status codes were decoded to their labels using the service's own domain definitions, alongside the raw codes.

Converted to GeoParquet with gpio — zstd compression, Hilbert row order, and a covering bbox column with row-group statistics, so a spatial filter can skip most of the file over the network — and tiled to PMTiles with tippecanoe.


## Attribution

City of St. Louis — Water Division

## License

[other](https://stlcity.maps.arcgis.com/home/item.html?id=80c69343cc2d418fb1796a342a863aac)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
