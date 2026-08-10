# LRA Property

Land Reutilization Authority data and search. Mirrored from [the city's open data portal](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=30); explore it in the [St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/#/housing/lra-property/collection.json).

![st-louis](https://img.shields.io/badge/st--louis-blue) ![missouri](https://img.shields.io/badge/missouri-blue) ![open-data](https://img.shields.io/badge/open--data-blue) ![lra](https://img.shields.io/badge/lra-blue) ![property](https://img.shields.io/badge/property-blue)

## Spatial Coverage

- **Bounding Box**: [-90.31412389098493, 38.539680481705595, -90.18167883554807, 38.765807022637496]

## Temporal Coverage

- **Start**: open
- **End**: ongoing

## Schema

| Column | Type | Description |
|--------|------|-------------|
| PropNS_Status | string | Status of the property in the Proposition NS program (the voter-approved Neighborhood Stabilization bond program that stabilizes LRA-owned vacant buildings). |
| Case_Status | string |  |
| Address | string |  |
| AddrNum | string |  |
| LowAddrNum | int32 |  |
| LowAddrSuf | string |  |
| HighAddrNum | int32 |  |
| HighAddrSuf | string |  |
| StPreDir | string |  |
| StName | string |  |
| StType | string |  |
| StSufDir | string |  |
| Handle | string | Citywide parcel handle (join key to the parcels collections); CityBlock/Parcel/ParcelId are the parcel key fields. |
| CityBlock | double |  |
| Parcel | int32 |  |
| ParcelId | string |  |
| GUID | string |  |
| LRA | string | Flag/identifier that the property is in the Land Reutilization Authority (LRA) inventory — the city land bank's holdings. |
| WARD | int16 |  |
| NEIGHBORHOOD_NUM | int16 |  |
| ZipCode | double |  |
| SQFT | int32 |  |
| Suit_Number | string |  |
| Cost | double |  |
| Property_Source | string |  |
| Irregular_Lot | string |  |
| Description | string |  |
| Acres | double |  |
| Status | string | Inventory status of the LRA property. |
| Usage | string | Current/intended usage classification of the property in the LRA inventory. |
| Demolition | string | Demolition status/flag for the structure. |
| Environmental | string |  |
| Value | int32 |  |
| Value_Estimated | int32 |  |
| Class | string |  |
| AppraisedVal | string | Appraised value of the property; AssessorsTotal is the assessor's total assessed value. |
| LRA_PRICING | double | LRA pricing category or price for the property. |
| Featured | string |  |
| ACQUISITION_DATE | timestamp[ms] | Date the LRA acquired the property. |
| AssessorsTotal | double |  |
| Frontage | double |  |
| NbrOfUnits | int16 |  |
| LegalDescription | string |  |
| AssessorsNbrhdNum | int16 |  |
| LOCATION | string |  |
| Sequence | int32 |  |
| Notes | string |  |
| PublicNotice | string |  |
| BuildingCount | int16 |  |
| GreenLienStatus | string | Status of any 'green lien' (vacant-lot greening assessment) on the property (name-based). |
| BuriedMaterials | string |  |
| PropertyType | string |  |
| SideLotEligible | string | Whether the lot qualifies for the LRA side-lot program (sale of vacant lots to adjacent owners). |
| Stories | float |  |
| CDBG_Source | string |  |
| CDBG_Amount | int32 |  |
| SALEPRICE | double | Sale price when the property was sold out of the inventory; CLOSING_COMPLETED marks completed closings. |
| CLOSING_COMPLETED | timestamp[ms] |  |
| CASE_NUMBER | string |  |
| Maintenance | string |  |
| PCA_Date | timestamp[ms] | Date of the property condition assessment (name-based). |
| OBJECTID | int64 |  |
| Shape__Area | double |  |
| Shape__Length | double |  |
| geometry | binary |  |
| geometry_bbox | struct<xmin: float not null, ymin: float not null, xmax: float not null, ymax: float not null> |  |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./lra-property.parquet | 1.9 MB | 1220ca4cfc3e... |
| ./lra-property.pmtiles | 1.8 MB | 122042d4e49c... |
| ./styles/city-renderer.json | 1.2 KB | 1220c00f954b... |
| ./styles/default.json | 1.7 KB | 12207f98eac2... |
| ./styles/style-solid.json | 506 B | 122033c6a1f3... |
| ./styles/style-source.json | 1.6 KB | 12201a65e0c5... |
| ./styles/style-usage.json | 1.6 KB | 1220b6d23480... |
| ./thumbnail.png | 368.0 KB | 12202bfba8bd... |
| https://static.stlouis-mo.gov/open-data/SLDC/REAL-ESTATE/LRA_INVENTORY.csv | 2.8 MB | 1220d7b16705... |
| https://static.stlouis-mo.gov/open-data/SLDC/REAL-ESTATE/LRA_INVENTORY_AVAILABLE.csv | 1.7 MB | 1220486039eb... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("./lra-property.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/SLDC_Real_Estate/FeatureServer](https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/SLDC_Real_Estate/FeatureServer)

## Processing Notes

Mirrored from the City of St. Louis open data portal (https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=30). Nothing was added to the data and no features were dropped except where noted below.

Extracted from the city's own ArcGIS REST service with the Portolan CLI:

    portolan extract arcgis \
      https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/SLDC_Real_Estate/FeatureServer --layers "LRA Inventory" --raw

That pages the service's `/query` endpoint for every feature, so this is the whole layer rather than the display-capped sample a browser request returns, and it carries across the service's field aliases. The service's own ESRI renderer was captured at the same time and is republished here as `styles/city-renderer.json`, so the map can be drawn in the city's own symbology.

The SLDC service carries every parcel in the city, not just the LRA's; this collection is the `LRA = 'YES'` subset.

Converted to GeoParquet with gpio — zstd compression, Hilbert row order, and a covering bbox column with row-group statistics, so a spatial filter can skip most of the file over the network — and tiled to PMTiles with tippecanoe.

The city's own file(s) are published as `source` assets on this collection, linked directly to stlouis-mo.gov — this mirror never becomes the only way to reach the original.


## Attribution

City of St. Louis — St. Louis Development Corporation

## License

[other](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=30)

## Contact

Chris Holmes <cholmes@9eo.org>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
