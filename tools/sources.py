"""Source manifest for the St. Louis open data mirror.

Single source of truth mapping each collection to where its data comes from.
Every dataset traces back to a page on https://www.stlouis-mo.gov/data/ —
`portal_page` is that page; extraction pulls from the city's ArcGIS servers
where a live service exists (better metadata + the city's own symbology),
otherwise from the portal's static download.
"""

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
    "property-sales": {
        "title": "Property Sales",
        "type": "static",
        "url": "https://www.stlouis-mo.gov/data/upload/data-files/prclsale.zip",
        "portal_page": PORTAL + "31",
        "department": "Assessor's Office",
    },
}
