# AGENTS.md — Special Business Districts (SBDs)

Special business districts (SBDs) within the City of Saint Louis. SBDs are established by Missouri statute. More Info: http://revisor.mo.gov/main/OneChapter.aspx?chapter=67

22 rows; geometry: Polygon Z (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/development/special-business-districts/special-business-districts.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/development/special-business-districts/special-business-districts.pmtiles` (layer `special-business-districts`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `Name` — district name
- `Active` — Y/N

Full schema: `table:columns` in collection.json.

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/development/special-business-districts/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/development/special-business-districts/) — rendered README and file listing
- [Source dataset](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=62) on the City of St. Louis open data portal

## Provenance

Mirror of [Special Business Districts (SBDs)](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=62) from the City of St. Louis; source: https://static.stlouis-mo.gov/open-data/SLDC/TAXING-DISTRICTS/SBD/STLSBDs_Shapefile.zip. No explicit license is published — see the source page. Synced 2026-08-05T19:58:51+00:00.
