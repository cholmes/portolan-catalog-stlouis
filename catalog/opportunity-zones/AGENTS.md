# AGENTS.md — Qualified Opportunity Zones

Qualified Opportunity Zones (QOZs) within the City of Saint Louis. Qualified Opportunity Zones are nominated for that designation by the state and that nomination has been certified by the Secretary of the U.S. Treasury via his delegation authority to the Internal Revenue Service. More Info: https://www.irs.gov/newsroom/opportunity-zones-frequently-asked-questions https://www.cdfifund.gov/Pages/Opportunity-Zones.aspx

16 rows; geometry: Polygon (WGS84 lon/lat unless noted).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/opportunity-zones/opportunity-zones.parquet' LIMIT 5;
```

PMTiles for maps: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/opportunity-zones/opportunity-zones.pmtiles` (layer `opportunity-zones`), styled by `styles/*.json` — `styles/default.json` is the default.

## Key fields

- `District_Name` — zone name

Full schema: `table:columns` in collection.json.

## Provenance

Mirror of [Qualified Opportunity Zones](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=59) from the City of St. Louis open data portal; source: https://maps8.stlouis-mo.gov/arcgis/rest/services/SLDC/Opportunity_Zones/FeatureServer. No explicit license is published — see the portal page. Synced 2026-08-05T04:46:13+00:00.
