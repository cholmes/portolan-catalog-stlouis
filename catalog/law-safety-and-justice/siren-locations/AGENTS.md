# AGENTS.md — Siren Locations

Public emergency siren locations. While these sirens are generally thought of as "tornado sirens" they can be used in other circumstances/emergencies.

58 rows; geometry: Point (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/law-safety-and-justice/siren-locations/siren-locations.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/law-safety-and-justice/siren-locations/siren-locations.pmtiles` (layer `siren-locations`), styled by `styles/*.json` — `styles/default.json` is the default.

Full schema: `table:columns` in collection.json.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/law-safety-and-justice/siren-locations/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/law-safety-and-justice/siren-locations/) — rendered README and file listing
- [Source dataset](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=132) on the City of St. Louis open data portal

## Provenance

Mirror of [Siren Locations](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=132) from the City of St. Louis; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/BPS/City_of_St__Louis_Firehouses_and_Outdoor_Warning_Sirens1/MapServer. No explicit license is published — see the source page. Synced 2026-08-05T19:58:51+00:00.
