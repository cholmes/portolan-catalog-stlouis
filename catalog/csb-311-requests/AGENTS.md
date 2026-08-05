# AGENTS.md — CSB Service Requests (311)

The Citizens' Service Bureau (CSB) is the customer service department for the City of St. Louis. This dataset provides access to some of the data collected when services are requested. The X/Y coordinates are in WGS 84 Web Mercator (EPSG:3857). File new service request here: https://www.stlouis-mo.gov/government/departments/public-safety/neighborhood-stabilization-office/citizens-service-bureau/csb-request-submit.cfm

1,477,057 rows; geometry: Point (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/csb-311-requests/csb-311-requests.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/csb-311-requests/csb-311-requests.pmtiles` (layer `csb-311-requests`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `REQUESTID` — request id
- `DATETIMEINIT` — opened (2008-09 through present)
- `GROUP` — category (37 values; trash/debris is the biggest)
- `STATUS` — CLOSED/CANCEL/open-ish states; case varies by era
- `PROBADDRESS` — problem address
- `NEIGHBORHOOD` — neighborhood number (joins neighborhoods.NHD_NUM)
- `WARD` — ward at time of request

Full schema: `table:columns` in collection.json.

## Quirks

1,477,057 rows; 18,177 have no usable coordinates (geometry IS NULL) — they remain in the table, so tabular counts and map counts differ. Coordinates were Web-Mercator SRX/SRY in the source, reprojected to WGS84; ~500 points falling outside the (buffered) city boundary were nulled. Status casing varies (CLOSED vs Closed).

## Joins

PROBADDRESS matches parcel situs addresses (fuzzy); NEIGHBORHOOD = neighborhoods.NHD_NUM; WARD = wards.DISTRICT.

## Provenance

Mirror of [CSB Service Requests (311)](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=5) from the City of St. Louis open data portal; source: https://www.stlouis-mo.gov/data/upload/data-files/csb.zip. No explicit license is published — see the portal page. Synced 2026-08-05T04:46:13+00:00.
