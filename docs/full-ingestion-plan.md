# Full ingestion plan: every geo and geo-adjacent St. Louis dataset

The initial catalog mirrors the top 20 datasets from
[stlouis-mo.gov/data](https://www.stlouis-mo.gov/data/). This document is the
executable roadmap for the rest: all remaining geospatial data, plus the
"geo-adjacent" tabular datasets that join to parcels or addresses. Source
inventories live alongside this file:

- `portal-datasets.json` — all 72 datasets on the portal with their data links
- `arcgis-inventory.json` — every service and layer on maps6/maps8/maps9.stlouis-mo.gov
- `portal-descriptions.json` — verbatim portal descriptions for mirrored datasets

Ground rules carried over from the initial build: descriptions come verbatim
from the portal, license stays `other` + link (the city publishes no explicit
license), providers are producer=department + host, every collection gets
collection-level `table:columns` (spec PR #124), ≥3 legend-bearing styles,
PNG thumbnail from the default style, PMTiles + GeoParquet per the Portolan
spec, and ArcGIS services are preferred over static downloads (renderer
styles + field aliases come free). Sources that refuse paged queries
(BOE precincts did) fall back to the portal's static downloads.

## Wave 1 — remaining static/service geo datasets (~12 collections)

| collection | portal id | source | notes |
|---|---|---|---|
| forest-park-trees | 123 | maps8 `FORESTRY/FOREST_PARK_TREES/FeatureServer` layer 2 | point layer, species-rich |
| siren-locations | 132 | maps6 `STREETS/Sirens/MapServer` | small point set |
| wards-2010 | 131 | static `planning/wards/wards_2010.zip` (maps8 `WARDS/Wards_2010` for style) | historical boundaries |
| police-districts-pre-2014 | 83 | static `boundaries/upload/STL-Police-Districts-pre-2014.zip` | historical boundaries |
| land-use | 78 | static `data-files/SLUPShapefiles2019.zip` | strategic land use plan (SLUP 2019) |
| nrsa-areas | 60 | portal page 60 downloads | Neighborhood Revitalization Strategy Areas |
| port-authority-district | 55 | maps8 `SLDC/Port_Authority_District_Boundary/FeatureServer` | single polygon |
| transportation-dev-districts | 57 | portal page 57 downloads | TDDs |
| lcra-property | 128 | maps8 `SLDC/LRA_and_LCRA_Properties/MapServer` (LCRA subset) | companion to lra-property |
| milkweed-gardens | 63 | portal page 63 (re-check for live source) | Milkweed for Monarchs |
| schools | 125 | maps8 `PDA/Schools/FeatureServer` | city public schools, points |
| floodplain | — | maps8 `STLOUIS/Floodplain/MapServer` | not on the portal; service-only |
| recycling-centers | — | maps8 `STLOUIS/Recycling_Centers_in_the_city_of_St_Louis/MapServer` | service-only |
| firehouses-sirens | — | maps8 `BPS/City_of_St__Louis_Firehouses_and_Outdoor_Warning_Sirens1/MapServer` | service-only |

Plus the **parcel historical series** (portal id 82): five era shapefile sets
(1997–2000, 2001–2005, 2006–2010, 2011–2015, 2016–2020 at
`data-files/stl_parcels_*.zip`) and the 2017–2025 CSV bundle
(`static…/assessor/Parcels-CSV-2017-2025.zip`). Model as one
`parcels-history` collection with one item per era (items carry
`table:columns` in properties per PR #124); partition with the partition
extension if any era exceeds ~2 GB. maps8
`Hosted/Archival_Parcel_Points/FeatureServer` has per-era point layers
(1997/2000/2005/2010/2015/2020/2025) as an alternative service source.

## Wave 2 — ArcGIS service sweep for layers with no portal page

Enumerate from `arcgis-inventory.json` (snapshot: maps6 = 128 services/33
folders, maps8 = 253/29, maps9 = 10/31), dedupe against waves 0–1, and
extract layers that exist nowhere else. Candidates already spotted:

- `STLOUIS/BOUNDARIES` extras: Zip Codes (5), Local Taxing Districts (10),
  Climate & Economic Justice Analysis (12), Response Zones (19)
- `PDA/Historic_Landmarks` (Historic Sites points), `PDA/Street_Design_Framework`
  (street typology), `PDA/Zoning_Signage_Overlays`
- `SLDC/Tax_Sales`, `SLDC/Recommended_Abatement_Map`, `SLDC/Business_Licenses_as_of_October_2025`
- `STREETS/Street_Sweeping`, `STREETS/ParkingServices` (parking meters),
  `STREETS/One_Call` (street lights), `STREETS/Drop_Off_Recycling_Location`
- `CDA/*` investment point layers, `BPS/*` capital project layers (selectively —
  many are one-off project maps)

Run `portolan extract arcgis <folder-url> --dry-run` per folder, review layer
lists, extract in batches. Skip: `CUSTOM_BASEMAPS`, `PRINT_SERVICES`,
`GEOCODERS`, `Utilities`, `TESTING`, `CITYWORKS` (internal), duplicate
copies of layers already mirrored.

## Wave 3 — geo-adjacent joinable tabular family

The parcel-keyed and address-keyed datasets. Parcels is the hub: the
`parcels` collection carries `LowerAsrParcelId`/`ColParcelId` (assessor
"handle") and full situs addresses. Every wave-3 collection documents its
join key and ships a runnable DuckDB join recipe in its README/AGENTS.md.

| collection | portal id | source | join key |
|---|---|---|---|
| property-taxes | 3 | `data-files/prcl.zip` (Access/DBF) | parcel handle |
| building-permits | 1 | portal page 1 downloads | parcel/address |
| demolition-permits | 24 | portal page 24 | parcel/address |
| electrical-permits | 51 | portal page 51 | parcel/address |
| mechanical-permits | 52 | portal page 52 | parcel/address |
| plumbing-permits | 53 | portal page 53 | parcel/address |
| sprinkler-permits | 107 | portal page 107 | parcel/address |
| street-permits | 17 | portal page 17 | address/block |
| occupancy-permits | 6 | `data-files/occupancy-permits.zip`, `static…/BUILDING/certificates_of_inspection.csv` | parcel/address |
| commercial-occupancy | 110 | portal page 110 | parcel/address |
| building-inspections | 11 | portal page 11 | parcel/address |
| housing-conservation-inspections | 113 | portal page 113 | parcel/address |
| vacant-buildings | 108 | portal page 108 (no direct link found — re-scrape or ask dept) | parcel |
| food-inspections | 71 | portal page 71 (no direct link found) | address |
| animal-bites | 130 | portal page 130 | address |
| lra-inventory-csv | 30 | `static…/SLDC/REAL-ESTATE/LRA_INVENTORY.csv` + offers/garden-permit CSVs | parcel handle |
| crime | 69 | slmpd.org monthly CSVs (external producer — note in providers) | address/block |

Tabular collections follow the spec's tabular pattern: collection-level
`data` asset, informational spatial extent, `table:columns` with
descriptions, documented joins. Where a table carries usable coordinates
(as 311 did with Web-Mercator SRX/SRY), promote it to a point geo collection.

## Wave 4 — organization and scale

1. **Nested sub-catalogs by department**, mirroring the portal's "Data by
   Department": `assessor/`, `planning/`, `sldc/`, `forestry/`, `streets/`,
   `public-safety/`, `boe/`, `health/`, `parks/`. Collection ids become POSIX
   paths from the catalog root (`assessor/parcels`) per the spec's
   nested-catalogs-flat-collections rule. Do this as one migration commit
   once wave 3 lands, updating all links/ids together.
2. `portolan stac-geoparquet` once total assets exceed ~1000.
3. Partition anything over ~2 GB (partition extension, 200 MB–1 GB files).
4. **Refresh cadence**: most city sets update monthly or quarterly; 311 and
   permits update continuously. Wire `tools/fetch.py` + `tools/assemble.py`
   into a scheduled CI job (monthly), re-running `portolan add` + `readme`
   + `push` and bumping `updated` from `staging/synced.txt`.

## Explicit exclusions

Portal entries that are not data or not city-published data: dashboards,
external websites (fly314.com, CityStat), PDF-only reports (HMDA), census
summaries that only link to census.gov, COVID/HIV/health surveillance pages
without downloadable structured data, and the Geocode Service (a live API,
not a dataset — document it in the catalog README instead).
