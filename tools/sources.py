"""Source manifest for the St. Louis open data mirror.

Single source of truth mapping each collection to where its data comes from.
Every dataset traces back to a page on https://www.stlouis-mo.gov/data/ —
`portal_page` is that page; extraction pulls from the city's ArcGIS servers
where a live service exists (better metadata + the city's own symbology),
otherwise from the portal's static download.
"""

import re

PORTAL = "https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id="

# type: "arcgis" → portolan extract arcgis --raw; "static" → download.sh
SOURCES = {
    "parcels": {
        "title": "Parcels",
        "type": "arcgis",
        "service": "https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/PARCELS_PUBLIC/MapServer",
        "layers": None,  # single-layer service
        "portal_page": PORTAL + "82",
        "department": "Assessor's Office",
    },
    "neighborhoods": {
        "title": "Neighborhood Boundaries",
        "type": "arcgis",
        "service": "https://maps6.stlouis-mo.gov/arcgis/rest/services/PublicDataStore/NEIGHBORHOOD_BOUNDARIES/FeatureServer",
        "layers": None,
        "portal_page": PORTAL + "85",
        "department": "Planning and Urban Design",
    },
    "wards": {
        "title": "Ward Boundaries (2020)",
        # The Hosted ward FeatureServer is incomplete (10 of 14 wards);
        # the portal's shapefile download has all 14.
        "type": "static",
        "url": "https://static.stlouis-mo.gov/open-data/planning/wards/wards_2020.zip",
        "portal_page": PORTAL + "131",
        "department": "Planning and Urban Design",
    },
    "city-boundary": {
        "title": "City Boundary",
        "type": "arcgis",
        "service": "https://maps8.stlouis-mo.gov/arcgis/rest/services/STLOUIS/BOUNDARIES/MapServer",
        "layers": "City Limits",
        "portal_page": PORTAL + "67",
        "department": "Information Technology Services Agency",
    },
    "city-blocks": {
        "title": "City Blocks",
        "type": "arcgis",
        "service": "https://maps8.stlouis-mo.gov/arcgis/rest/services/STLOUIS/BOUNDARIES/MapServer",
        "layers": "City Blocks",
        "portal_page": PORTAL + "12",
        "department": "Assessor's Office",
    },
    "streets": {
        "title": "City Streets",
        "type": "arcgis",
        "service": "https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Streets/FeatureServer",
        "layers": "STREETS",
        "portal_page": PORTAL + "68",
        "department": "Streets - Director's Office",
    },
    "parks": {
        "title": "City Parks",
        "type": "arcgis",
        "service": "https://maps9.stlouis-mo.gov/arcgis/rest/services/PARKS/Reservable_Park_Amenities/FeatureServer",
        "layers": "Parks",
        "portal_page": PORTAL + "46",
        "department": "Parks",
    },
    "police-districts": {
        "title": "Police District Boundaries",
        "type": "arcgis",
        "service": "https://maps8.stlouis-mo.gov/arcgis/rest/services/STLOUIS/POLICE_DISTRICT/FeatureServer",
        "layers": None,
        "portal_page": PORTAL + "83",
        "department": "Police Department",
    },
    "election-precincts": {
        "title": "Election Wards & Precincts",
        "type": "static",
        "url": "https://static.stlouis-mo.gov/open-data/BOEC/Precincts_Current.zip",
        "portal_page": PORTAL + "124",
        "department": "Board of Election Commissioners",
    },
    "zoning": {
        "title": "Zoning",
        "type": "arcgis",
        "service": "https://maps9.stlouis-mo.gov/arcgis/rest/services/PDA/Zoning/MapServer",
        "layers": "Zoning",
        "portal_page": PORTAL + "78",
        "department": "Planning and Urban Design",
    },
    "historic-districts": {
        "title": "Historic Districts",
        "type": "arcgis",
        "service": "https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/Historic_Districts/MapServer",
        "layers": None,
        "portal_page": PORTAL + "73",
        "department": "Planning and Urban Design",
    },
    "city-trees": {
        "title": "City Trees (Planting Sites)",
        "type": "arcgis",
        "service": "https://maps9.stlouis-mo.gov/arcgis/rest/services/FORESTRY/FORESTRY_TREES/MapServer",
        "layers": "CITY_TREES_ALL_SITES",
        "portal_page": PORTAL + "121",
        "department": "Forestry",
    },
    "tif-districts": {
        "title": "Tax Increment Financing (TIF) Districts",
        "type": "arcgis",
        "service": "https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/TIF_Districts/FeatureServer",
        "layers": "Districts TIF",
        "portal_page": PORTAL + "56",
        "department": "St. Louis Development Corporation",
    },
    "opportunity-zones": {
        "title": "Qualified Opportunity Zones",
        "type": "arcgis",
        "service": "https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Opportunity_Zones/FeatureServer",
        "layers": "Opportunity Zones",
        "portal_page": PORTAL + "59",
        "department": "St. Louis Development Corporation",
    },
    "lra-property": {
        "title": "LRA Property",
        "type": "arcgis",
        "service": "https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/SLDC_Real_Estate/FeatureServer",
        "layers": "LRA Inventory",
        "portal_page": PORTAL + "30",
        "department": "St. Louis Development Corporation",
    },
    "community-improvement-districts": {
        "title": "Community Improvement Districts (CIDs)",
        "type": "static",
        "url": "https://static.stlouis-mo.gov/open-data/SLDC/TAXING-DISTRICTS/CID/STLCIDs.geojson",
        "portal_page": PORTAL + "58",
        "department": "St. Louis Development Corporation",
    },
    "special-business-districts": {
        "title": "Special Business Districts (SBDs)",
        "type": "static",
        "url": "https://static.stlouis-mo.gov/open-data/SLDC/TAXING-DISTRICTS/SBD/STLSBDs_Shapefile.zip",
        "portal_page": PORTAL + "62",
        "department": "St. Louis Development Corporation",
    },
    "tax-abated-parcels": {
        "title": "Tax-abated Parcels",
        "type": "static",
        "url": "https://static.stlouis-mo.gov/open-data/SLDC/TAX-ABATEMENT/taxabatedparcels.geojson",
        "portal_page": PORTAL + "61",
        "department": "St. Louis Development Corporation",
    },
    "csb-311-requests": {
        "title": "CSB Service Requests (311)",
        "type": "static",
        "url": "https://www.stlouis-mo.gov/data/upload/data-files/csb.zip",
        "portal_page": PORTAL + "5",
        "department": "Neighborhood Stabilization / CSB",
    },
    "bike-infrastructure": {
        "title": "Bike Infrastructure",
        "type": "arcgis",
        "service": "https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/Biking_Infrastructure_Map/MapServer",
        "layers": None,  # all five layers, merged with a source_layer column
        "portal_page": "https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/Biking_Infrastructure_Map/MapServer",
        "department": "Planning and Urban Design",
    },
    "forest-park-trees": {
        "title": 'Forest Park Trees',
        "type": 'arcgis',
        "service": 'https://maps8.stlouis-mo.gov/arcgis/rest/services/FORESTRY/FOREST_PARK_TREES/FeatureServer',
        "layers": 'FOREST_PARK_TREES',
        "portal_page": 'https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=123',
        "department": 'Forestry',
    },
    "siren-locations": {
        "title": 'Siren Locations',
        "type": 'arcgis',
        # maps6 STREETS/Sirens is stopped; the BPS firehouses+sirens service
        # carries the same siren points.
        "service": 'https://maps8.stlouis-mo.gov/arcgis/rest/services/BPS/City_of_St__Louis_Firehouses_and_Outdoor_Warning_Sirens1/MapServer',
        "layers": 'Outdoor Warning Siren Locations',
        "portal_page": 'https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=132',
        "department": 'City Emergency Management Agency',
    },
    "schools": {
        "title": 'City Public Schools',
        "type": 'arcgis',
        "service": 'https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/Schools/FeatureServer',
        "layers": None,
        "portal_page": 'https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=125',
        "department": 'Planning and Urban Design',
    },
    "floodplain": {
        "title": 'Floodplain',
        "type": 'arcgis',
        "service": 'https://maps8.stlouis-mo.gov/arcgis/rest/services/STLOUIS/Floodplain/MapServer',
        "layers": None,
        "portal_page": 'https://maps8.stlouis-mo.gov/arcgis/rest/services/STLOUIS/Floodplain/MapServer',
        "department": 'Information Technology Services Agency',
    },
    "port-authority-district": {
        "title": 'Port Authority District',
        "type": 'arcgis',
        "service": 'https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Port_Authority_District_Boundary/FeatureServer',
        "layers": None,
        "portal_page": 'https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=55',
        "department": 'St. Louis Development Corporation',
    },
    "wards-2010": {
        "title": 'Ward Boundaries (2010)',
        "type": 'static',
        "url": 'https://static.stlouis-mo.gov/open-data/planning/wards/wards_2010.zip',
        "portal_page": 'https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=131',
        "department": 'Planning and Urban Design',
    },
    "land-use": {
        "title": 'Strategic Land Use Plan',
        "type": 'arcgis',
        "service": 'https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/Strategic_Land_Use_Plan/FeatureServer',
        "layers": None,
        "portal_page": 'https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=78',
        "department": 'Planning and Urban Design',
    },
    "lead-service-lines": {
        "title": 'Lead Service Line Inventory',
        "type": 'arcgis',
        "service": 'https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/STLWD_LSLI__Read_Only_View/FeatureServer',
        "layers": None,
        "portal_page": 'https://stlcity.maps.arcgis.com/home/item.html?id=80c69343cc2d418fb1796a342a863aac',
        "department": 'Water Division',
    },
    "market-value-analysis": {
        "title": '2024 Market Value Analysis',
        "type": 'arcgis',
        "service": 'https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/2024_Market_Value_Analysis/FeatureServer',
        "layers": None,
        "portal_page": 'https://stlcity.maps.arcgis.com/home/item.html?id=e71e3ebca1f345a4b7db134d30c5d9ff',
        "department": 'Community Development Administration',
    },
    "vacancy-composite": {
        "title": 'Parcel Vacancy Composite',
        "type": 'arcgis',
        "service": 'https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/SLDC_SLDC_Tol_Def_Vac_NP/FeatureServer',
        "layers": None,
        "portal_page": 'https://stlcity.maps.arcgis.com/home/item.html?id=98a6f429617546be9d9b467c5ad1dafc',
        "department": 'St. Louis Development Corporation',
    },
    "polling-places": {
        "title": 'Polling Centers',
        "type": 'arcgis',
        "service": 'https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/Polling_Centers_WFL1/FeatureServer',
        "layers": None,
        "portal_page": 'https://stlcity.maps.arcgis.com/home/item.html?id=87bc5cf8db58428295792e690397ed75',
        "department": 'Board of Election Commissioners',
    },
    "election-results-nov-2024": {
        "title": 'November 2024 Election Results by Precinct',
        "type": 'arcgis',
        # the geocoded dve layer carries no attribute data; the vote-totals
        # table has the real per-precinct, per-contest results (tabular,
        # joins election-precincts by precinct name).
        "service": 'https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/Nov24_Detailed_Vote_Totals_Test/FeatureServer',
        "layers": None,
        "table": True,
        "portal_page": 'https://stlcity.maps.arcgis.com/home/item.html?id=6e72fa855cd445f7af37d79615f602d0',
        "department": 'Board of Election Commissioners',
    },
    "tornado-damage-2025": {
        "title": 'May 2025 Tornado Damage',
        "type": 'arcgis',
        "service": 'https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/NS_Tornado_Map_WFL1/FeatureServer',
        "layers": None,
        "portal_page": 'https://stlcity.maps.arcgis.com/home/item.html?id=d2f73ad3cd2b434b91c6eacaef94df32',
        "department": 'City Emergency Management Agency',
    },
    "flood-controls": {
        "title": 'Flood Controls',
        "type": 'arcgis',
        "service": 'https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/Flood_Controls_WFL1/FeatureServer',
        "layers": None,
        "portal_page": 'https://stlcity.maps.arcgis.com/home/item.html?id=4a08499ad4054caca42215e4c51aac0e',
        "department": 'Board of Public Service',
    },
    "neighborhood-organizations": {
        "title": 'Neighborhood Organizations',
        "type": 'arcgis',
        "service": 'https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/Neighborhood_Organizations/FeatureServer',
        "layers": None,
        "portal_page": 'https://stlcity.maps.arcgis.com/home/item.html?id=ac198aeb9592458b8591c7258e719ad1',
        "department": 'Neighborhood Stabilization / CSB',
    },
    "property-taxes": {
        "title": 'Property Taxes',
        "type": "static",
        "url": 'https://www.stlouis-mo.gov/data/upload/data-files/prcl.zip',
        "portal_page": "https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=3",
        "department": "Assessor's Office",
    },
    "electrical-permits": {
        "title": 'Electrical Permits',
        "type": "static",
        "url": 'https://www.stlouis-mo.gov/data/upload/data-files/electrical-permits.zip',
        "portal_page": "https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=51",
        "department": 'Building Commissioner',
    },
    "mechanical-permits": {
        "title": 'Mechanical Permits',
        "type": "static",
        "url": 'https://www.stlouis-mo.gov/data/upload/data-files/mechanical-permits.zip',
        "portal_page": "https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=52",
        "department": 'Building Commissioner',
    },
    "plumbing-permits": {
        "title": 'Plumbing Permits',
        "type": "static",
        "url": 'https://www.stlouis-mo.gov/data/upload/data-files/plumbing-permits.zip',
        "portal_page": "https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=53",
        "department": 'Building Commissioner',
    },
    "street-permits": {
        "title": 'Street Permits',
        "type": "static",
        "url": 'https://www.stlouis-mo.gov/data/upload/data-files/streets/street-permits.csv',
        "portal_page": "https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=17",
        "department": 'Streets - Street Division',
    },
    "occupancy-permits": {
        "title": 'Occupancy Permits',
        "type": "static",
        "url": 'https://www.stlouis-mo.gov/data/upload/data-files/occupancy-permits.zip',
        "portal_page": "https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=6",
        "department": 'Building Commissioner',
    },
    "animal-bites": {
        "title": 'Animal Bites',
        "type": "static",
        "url": 'https://static.stlouis-mo.gov/open-data/HEALTH/ANIMAL-CONTROL/ANIMAL_BITES.csv',
        "portal_page": "https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=130",
        "department": 'Environmental Health Services',
    },
    "parcels-history": {
        "title": "Parcels (Historical, 1997-2020)",
        "type": "static",
        "urls": ["https://www.stlouis-mo.gov/data/upload/data-files/stl_parcels_1997-2000.zip",
                 "https://www.stlouis-mo.gov/data/upload/data-files/stl_parcels_2001-2005.zip",
                 "https://www.stlouis-mo.gov/data/upload/data-files/stl_parcels_2006-2010.zip",
                 "https://www.stlouis-mo.gov/data/upload/data-files/stl_parcels_2011-2015.zip",
                 "https://www.stlouis-mo.gov/data/upload/data-files/stl_parcels_2016-2020.zip"],
        "url": "https://www.stlouis-mo.gov/data/upload/data-files/stl_parcels_1997-2000.zip",
        "portal_page": "https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=82",
        "department": "Assessor's Office",
    },
    "crime": {
        "title": "Crime (NIBRS)",
        "type": "static",
        "url": "https://www.slmpd.org/crime_stats.shtml",
        "crime_scrape": True,
        "portal_page": "https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=69",
        "department": "Metropolitan Police Department",
    },
    "historic-landmarks": {
        "title": "Historic Landmarks",
        "type": "arcgis",
        "service": "https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/Historic_Landmarks/FeatureServer",
        "layers": "Historic Sites",
        "portal_page": "https://maps8.stlouis-mo.gov/arcgis/rest/services/PDA/Historic_Landmarks/FeatureServer",
        "department": "Planning and Urban Design",
    },
    "zip-codes": {
        "title": "ZIP Codes",
        "type": "arcgis",
        "service": "https://maps8.stlouis-mo.gov/arcgis/rest/services/STLOUIS/BOUNDARIES/MapServer",
        "layers": "Zip Codes",
        "portal_page": "https://maps8.stlouis-mo.gov/arcgis/rest/services/STLOUIS/BOUNDARIES/MapServer",
        "department": "Information Technology Services Agency",
    },
    "parking-meters": {
        "title": "Parking Meters",
        "type": "arcgis",
        "service": "https://maps8.stlouis-mo.gov/arcgis/rest/services/STREETS/ParkingServices/MapServer",
        "layers": "PARKING_METERS",
        "portal_page": "https://maps8.stlouis-mo.gov/arcgis/rest/services/STREETS/ParkingServices/MapServer",
        "department": "Streets - Director's Office",
    },
    "street-sweeping": {
        "title": "Street Sweeping Schedule",
        "type": "arcgis",
        "service": "https://maps8.stlouis-mo.gov/arcgis/rest/services/STREETS/Street_Sweeping/MapServer",
        "layers": "Street Sweeping Area Schedule",
        "portal_page": "https://maps8.stlouis-mo.gov/arcgis/rest/services/STREETS/Street_Sweeping/MapServer",
        "department": "Streets - Street Division",
    },
    "business-licenses": {
        "title": "Business Licenses",
        "type": "arcgis",
        "service": "https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Business_Licenses_as_of_October_2025/FeatureServer",
        "layers": None,
        "portal_page": "https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Business_Licenses_as_of_October_2025/FeatureServer",
        "department": "St. Louis Development Corporation",
    },
    "tax-sales": {
        "title": "Tax Sales",
        "type": "arcgis",
        "service": "https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Tax_Sales/FeatureServer",
        "layers": "Tax Sales",
        "portal_page": "https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Tax_Sales/FeatureServer",
        "department": "St. Louis Development Corporation",
    },
    "property-sales": {
        "title": "Property Sales",
        "type": "static",
        "url": "https://www.stlouis-mo.gov/data/upload/data-files/prclsale.zip",
        "portal_page": PORTAL + "31",
        "department": "Assessor's Office",
    },
}


# ---------------------------------------------------------------------------
# The city's own files, published as `source`-role assets on each collection.
#
# formats.md: "A mirror SHOULD also include the original data as an asset when
# it is directly downloadable (not just an API)." So a Shapefile zip, GeoJSON
# or CSV the city serves gets an asset pointing straight at stlouis-mo.gov —
# the mirror never becomes the only way to reach the original. An ArcGIS
# service is an API, not a download, so it stays a `rel: via` link instead;
# pinning size and checksum to a live query endpoint would rot on the next
# upstream edit.
#
# `primary: True` marks the file this collection was actually built from
# (cross-checked against SOURCES by tests/test_catalog.py). The rest are the
# city's alternate distributions of the same layer, listed because a consumer
# may want the Shapefile's exact field widths or the CSV's raw text.
#
# Only files that are genuinely THIS layer are listed. The portal bundles
# unrelated downloads on shared dataset pages — par.zip and codes.zip (lookup
# tables) on the zoning page, LRA_OFFERS.csv on the LRA page, CADDrawings.zip
# on the blocks page — and those belong to other datasets or to no collection
# here, so listing them as this collection's source would be a lie. Two
# candidates were dropped because the city no longer serves them:
# STLSBDs.geojson (404) and STL-Police-Districts-2014-2.zip (0-byte HTML).
# ---------------------------------------------------------------------------

SF_STATIC = "https://static.stlouis-mo.gov/open-data"
SF_FILES = "https://www.stlouis-mo.gov/data/upload/data-files"

SOURCE_FILES = {
    "parcels": [
        {"key": "source-shapefile", "url": f"{SF_STATIC}/ASSESSOR/PARCELS.zip",
         "title": "Parcels — the Assessor's zipped Shapefile"},
        {"key": "source-csv", "url": f"{SF_STATIC}/PLANNING/parcels/parcels-basic-info.csv",
         "title": "Parcels — basic info as CSV",
         "description": "One row per parcel with the headline attributes, no geometry."},
    ],
    "parcels-history": [
        {"key": "source-1997-2000", "primary": True,
         "url": f"{SF_FILES}/stl_parcels_1997-2000.zip",
         "title": "Historical parcels 1997–2000 (zipped Shapefiles)"},
        {"key": "source-2001-2005", "primary": True,
         "url": f"{SF_FILES}/stl_parcels_2001-2005.zip",
         "title": "Historical parcels 2001–2005 (zipped Shapefiles)"},
        {"key": "source-2006-2010", "primary": True,
         "url": f"{SF_FILES}/stl_parcels_2006-2010.zip",
         "title": "Historical parcels 2006–2010 (zipped Shapefiles)"},
        {"key": "source-2011-2015", "primary": True,
         "url": f"{SF_FILES}/stl_parcels_2011-2015.zip",
         "title": "Historical parcels 2011–2015 (zipped Shapefiles)"},
        {"key": "source-2016-2020", "primary": True,
         "url": f"{SF_FILES}/stl_parcels_2016-2020.zip",
         "title": "Historical parcels 2016–2020 (zipped Shapefiles)"},
        {"key": "source-csv-2017-2025", "url": f"{SF_STATIC}/assessor/Parcels-CSV-2017-2025.zip",
         "title": "Parcel attributes 2017–2025 (zipped CSVs)",
         "description": "The later, CSV-only continuation of the series; not "
                        "merged into this collection, which stops at 2020."},
    ],
    "neighborhoods": [
        {"key": "source-shapefile", "url": f"{SF_STATIC}/planning/neighborhoods/neighborhoods.zip",
         "title": "Neighborhood boundaries (zipped Shapefile)"},
    ],
    "city-boundary": [
        {"key": "source-shapefile", "url": f"{SF_FILES}/stl_boundary.zip",
         "title": "City boundary (zipped Shapefile)"},
    ],
    "city-blocks": [
        {"key": "source-shapefile", "url": f"{SF_FILES}/blocks_shape.zip",
         "title": "City blocks (zipped Shapefile)"},
    ],
    "streets": [
        {"key": "source-shapefile", "url": f"{SF_FILES}/streets.zip",
         "title": "City streets (zipped Shapefile)"},
    ],
    "parks": [
        {"key": "source-shapefile", "url": f"{SF_FILES}/parks.zip",
         "title": "City parks (zipped Shapefile)"},
    ],
    "zoning": [
        {"key": "source-shapefile", "url": f"{SF_FILES}/zoning.zip",
         "title": "Zoning districts (zipped Shapefile)"},
    ],
    "land-use": [
        {"key": "source-shapefile", "url": f"{SF_FILES}/SLUPShapefiles2019.zip",
         "title": "Strategic Land Use Plan 2019 (zipped Shapefiles)",
         "description": "The 2019 SLUP shapefiles. The collection itself "
                        "mirrors the 2025 plan from the live service."},
    ],
    "historic-districts": [
        {"key": "source-shapefile", "url": f"{SF_FILES}/historic_dist.zip",
         "title": "Historic districts (zipped Shapefile)"},
    ],
    "city-trees": [
        {"key": "source-geojson", "url": f"{SF_STATIC}/FORESTRY/CITY_TREES.geojson",
         "title": "City trees (GeoJSON)"},
        {"key": "source-shapefile", "url": f"{SF_STATIC}/FORESTRY/CITY_TREES.zip",
         "title": "City trees (zipped Shapefile)"},
    ],
    "tif-districts": [
        {"key": "source-geojson", "url": f"{SF_STATIC}/SLDC/INCENTIVES/TIF/STLTIFs.geojson",
         "title": "TIF districts (GeoJSON)"},
        {"key": "source-shapefile", "url": f"{SF_STATIC}/SLDC/INCENTIVES/TIF/STLTIFs_Shapefile.zip",
         "title": "TIF districts (zipped Shapefile)"},
        {"key": "source-csv", "url": f"{SF_STATIC}/SLDC/INCENTIVES/TIF/STLTIFs.csv",
         "title": "TIF districts (CSV, no geometry)"},
    ],
    "opportunity-zones": [
        {"key": "source-geojson", "url": f"{SF_FILES}/OpportunityZones.geojson",
         "title": "Opportunity zones (GeoJSON)"},
        {"key": "source-shapefile", "url": f"{SF_FILES}/OpportunityZones.zip",
         "title": "Opportunity zones (zipped Shapefile)"},
    ],
    "lra-property": [
        {"key": "source-csv", "url": f"{SF_STATIC}/SLDC/REAL-ESTATE/LRA_INVENTORY.csv",
         "title": "LRA inventory (CSV, no geometry)"},
        {"key": "source-csv-available", "url": f"{SF_STATIC}/SLDC/REAL-ESTATE/LRA_INVENTORY_AVAILABLE.csv",
         "title": "LRA inventory — available properties only (CSV, no geometry)"},
    ],
    "community-improvement-districts": [
        {"key": "source", "primary": True,
         "url": f"{SF_STATIC}/SLDC/TAXING-DISTRICTS/CID/STLCIDs.geojson",
         "title": "Community improvement districts (GeoJSON)"},
        {"key": "source-shapefile", "url": f"{SF_STATIC}/SLDC/TAXING-DISTRICTS/CID/STLCIDs_Shapefile.zip",
         "title": "Community improvement districts (zipped Shapefile)"},
    ],
    "special-business-districts": [
        {"key": "source", "primary": True,
         "url": f"{SF_STATIC}/SLDC/TAXING-DISTRICTS/SBD/STLSBDs_Shapefile.zip",
         "title": "Special business districts (zipped Shapefile)"},
    ],
    "tax-abated-parcels": [
        {"key": "source", "primary": True,
         "url": f"{SF_STATIC}/SLDC/TAX-ABATEMENT/taxabatedparcels.geojson",
         "title": "Tax-abated parcels (GeoJSON)"},
        {"key": "source-shapefile", "url": f"{SF_STATIC}/SLDC/TAX-ABATEMENT/taxabatedparcels.zip",
         "title": "Tax-abated parcels (zipped Shapefile)"},
    ],
    "wards": [
        {"key": "source", "primary": True,
         "url": f"{SF_STATIC}/planning/wards/wards_2020.zip",
         "title": "Ward boundaries 2020 (zipped Shapefile)"},
    ],
    "wards-2010": [
        {"key": "source", "primary": True,
         "url": f"{SF_STATIC}/planning/wards/wards_2010.zip",
         "title": "Ward boundaries 2010 (zipped Shapefile)"},
    ],
    "election-precincts": [
        {"key": "source", "primary": True,
         "url": f"{SF_STATIC}/BOEC/Precincts_Current.zip",
         "title": "Current election precincts (zipped Shapefile)"},
    ],
    "csb-311-requests": [
        {"key": "source", "primary": True, "url": f"{SF_FILES}/csb.zip",
         "title": "Citizens' Service Bureau requests (zipped CSVs, one per year)"},
    ],
    "property-taxes": [
        {"key": "source", "primary": True, "url": f"{SF_FILES}/prcl.zip",
         "title": "Property taxes (zipped Microsoft Access database)"},
    ],
    "property-sales": [
        {"key": "source", "primary": True, "url": f"{SF_FILES}/prclsale.zip",
         "title": "Property sales (zipped Microsoft Access database)"},
    ],
    "electrical-permits": [
        {"key": "source", "primary": True, "url": f"{SF_FILES}/electrical-permits.zip",
         "title": "Electrical permits (zipped CSV)"},
    ],
    "mechanical-permits": [
        {"key": "source", "primary": True, "url": f"{SF_FILES}/mechanical-permits.zip",
         "title": "Mechanical permits (zipped CSV)"},
    ],
    "plumbing-permits": [
        {"key": "source", "primary": True, "url": f"{SF_FILES}/plumbing-permits.zip",
         "title": "Plumbing permits (zipped CSV)"},
    ],
    "occupancy-permits": [
        {"key": "source", "primary": True, "url": f"{SF_FILES}/occupancy-permits.zip",
         "title": "Occupancy permits (zipped CSV)"},
    ],
    "street-permits": [
        {"key": "source", "primary": True, "url": f"{SF_FILES}/streets/street-permits.csv",
         "title": "Street permits (CSV)"},
    ],
    "animal-bites": [
        {"key": "source", "primary": True,
         "url": f"{SF_STATIC}/HEALTH/ANIMAL-CONTROL/ANIMAL_BITES.csv",
         "title": "Animal bites (CSV)"},
    ],
    # Crime is the one collection whose source file list is not fixed: SLMPD
    # posts a new monthly CSV on crime_stats.shtml and the mirror picks up
    # whatever is there at sync time. tools/fetch_source_meta.py scrapes the
    # index and writes the month-by-month entries into the checksum sidecar.
    "crime": "scrape",
}

# Extension → media type for the source assets above.
SOURCE_MEDIA_TYPES = {
    ".zip": "application/zip",
    ".geojson": "application/geo+json",
    ".json": "application/json",
    ".csv": "text/csv",
}


def source_media_type(url: str) -> str:
    for ext, mt in SOURCE_MEDIA_TYPES.items():
        if url.lower().split("?")[0].endswith(ext):
            return mt
    return "application/octet-stream"


def source_files(cid: str) -> list:
    """The city's downloadable originals for a collection, primary first.

    Returns [] for the collections that only exist as a live ArcGIS service —
    those get a `rel: via` link instead, since an API is not a download.
    """
    entries = SOURCE_FILES.get(cid)
    if not entries or entries == "scrape":
        return []
    out = [dict(e) for e in entries]
    for e in out:
        e.setdefault("primary", False)
        e["type"] = source_media_type(e["url"])
    return sorted(out, key=lambda e: not e["primary"])


# ---------------------------------------------------------------------------
# Department sub-catalogs (wave 4). Collection ids become POSIX paths
# ("assessor/parcels") per the Portolan nested-catalogs-flat-collections rule.
# ---------------------------------------------------------------------------

GROUPS = {
    "urban-development-and-planning": [
        "parcels", "parcels-history", "city-blocks", "zoning", "land-use",
        "neighborhoods", "historic-districts", "historic-landmarks",
        "port-authority-district", "vacancy-composite", "city-boundary"],
    "government": [
        "wards", "wards-2010", "election-precincts", "polling-places",
        "election-results-nov-2024", "csb-311-requests", "zip-codes",
        "property-taxes"],
    "housing": [
        "lra-property", "property-sales", "market-value-analysis",
        "electrical-permits", "mechanical-permits", "plumbing-permits",
        "occupancy-permits"],
    "business-and-industry": [
        "tif-districts", "opportunity-zones", "special-business-districts",
        "tax-abated-parcels", "business-licenses", "tax-sales",
        "community-improvement-districts"],
    "transportation-infrastructure-and-utilities": [
        "streets", "street-permits", "parking-meters", "street-sweeping",
        "bike-infrastructure"],
    "law-safety-and-justice": [
        "police-districts", "crime", "siren-locations",
        "tornado-damage-2025"],
    "environment": [
        "floodplain", "flood-controls", "city-trees", "forest-park-trees"],
    "leisure-and-culture": ["parks"],
    "health": ["animal-bites", "lead-service-lines"],
    "community": ["neighborhood-organizations"],
    "education-and-training": ["schools"],
}

# The portal's own topic names and captions (from stlouis-mo.gov/data)
GROUP_TITLES = {
    "urban-development-and-planning": "Urban Development and Planning",
    "government": "Government",
    "housing": "Housing",
    "business-and-industry": "Business and Industry",
    "transportation-infrastructure-and-utilities":
        "Transportation, Infrastructure, and Utilities",
    "law-safety-and-justice": "Law, Safety, and Justice",
    "environment": "Environment",
    "leisure-and-culture": "Leisure and Culture",
    "health": "Health",
    "community": "Community",
    "education-and-training": "Education and Training",
}

GROUP_CAPTIONS = {
    "urban-development-and-planning": "Land Acquisition, Planning, Preservation, Zoning",
    "government": "Departments, Elected Officials, Voting, Services, Records",
    "housing": "Owning, Renting, Homelessness, Repairs, Financing Programs",
    "business-and-industry": "Assistance, Incentives, Licenses, Regulations, Bids",
    "transportation-infrastructure-and-utilities":
        "Airports, Rail, Public Transit, Vehicles, Utilities, Streets",
    "law-safety-and-justice": "Courts, Emergency Services, Police, Fire, Legal Assistance",
    "environment": "Waste, Recycling, Sustainability, Hazardous Materials",
    "leisure-and-culture": "Arts, Entertainment, Tourism, Cultural Venues, Sports",
    "health": "Immunizations, Nutrition, Animal Control, Preventative Care",
    "community": "Neighborhoods, Marriage, Birth, Immigration, Support",
    "education-and-training": "Adult, Schools, Special and Higher Education, Homeschooling",
}

GROUP_OF = {cid: g for g, cids in GROUPS.items() for cid in cids}


def coll_rel(cid: str) -> str:
    """Collection directory path relative to the catalog root."""
    return f"{GROUP_OF[cid]}/{cid}"


# The city writes URLs as bare text in its portal descriptions ("File new
# service request here: https://..."). STAC descriptions and READMEs are
# markdown, and the browser and source.coop render them as such, so a bare URL
# shows up as dead text. Wrap it as a markdown link, keeping the URL as its own
# label so nothing is invented. Skips URLs already linked or in angle brackets.
BARE_URL = re.compile(r"""(?<![(<\[\]])\bhttps?://[^\s<>()\[\]"']+""")


def linkify(text: str) -> str:
    def wrap(m):
        url = m.group(0)
        # Sentence punctuation trailing the URL is not part of it.
        trail = ""
        while url and url[-1] in ".,;:!?":
            trail, url = url[-1] + trail, url[:-1]
        return f"[{url}]({url}){trail}"

    return BARE_URL.sub(wrap, text) if text else text
