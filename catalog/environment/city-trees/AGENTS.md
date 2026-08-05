# AGENTS.md — City Trees (Planting Sites)

All mapped planting sites within the city for tree plantings managed by the Forestry Division. Street tree planting sites are re-used, while park tree sites tend not to be. This data contains vacant sites, as well.

134,588 rows; geometry: Point (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/environment/city-trees/city-trees.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/environment/city-trees/city-trees.pmtiles` (layer `city-trees`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `COMMON` — common name; the literal value 'Vacant' marks an empty planting site (30,935 of them)
- `DBH` — trunk diameter (inches) at breast height
- `CONDITION` — Excellent..Dead, Stump; N/A mostly = vacant sites
- `LOCATION_TYPE` — Easement (street trees), Park, Median

Full schema: `table:columns` in collection.json.

## Quirks

134,588 records = trees AND empty planting sites; filter COMMON <> 'Vacant' for actual trees.

## Joins

Address fields (STREET_NUM, STREET) join loosely to parcel situs addresses.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/environment/city-trees/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/environment/city-trees/) — rendered README and file listing
- [Source dataset](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=121) on the City of St. Louis open data portal

## Provenance

Mirror of [City Trees (Planting Sites)](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=121) from the City of St. Louis; source: https://maps9.stlouis-mo.gov/arcgis/rest/services/FORESTRY/FORESTRY_TREES/MapServer. No explicit license is published — see the source page. Synced 2026-08-05T19:58:51+00:00.
