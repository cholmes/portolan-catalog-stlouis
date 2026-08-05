# AGENTS.md — November 2024 Election Results by Precinct

This is the detailed vote extract (dve) from the November 5, 2024, General Municipal Election for the City of St. Louis.

24,030 rows; tabular (no geometry).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/election-results-nov-2024/election-results-nov-2024.parquet' LIMIT 5;
```

## Key fields

- `F_Precinct` — precinct name
- `Contest_Title` — contest
- `Choice_Name` — candidate/choice
- `Total_Votes` — votes (also Election_Day/Absentee/Provisional splits)
- `Turnout_Percentage` — precinct turnout

Full schema: `table:columns` in collection.json.

## Quirks

24,030 rows = precinct x contest x choice for the November 5, 2024 general election. Tabular — join election-precincts on precinct name for mapping.

## Joins

election-precincts.name relates to F_Precinct (both use 'W <ward> P <precinct>' style names; normalize whitespace).

## Provenance

Mirror of [November 2024 Election Results by Precinct](https://stlcity.maps.arcgis.com/home/item.html?id=6e72fa855cd445f7af37d79615f602d0) from the City of St. Louis open data portal; source: https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/Nov24_Detailed_Vote_Totals_Test/FeatureServer. No explicit license is published — see the portal page. Synced 2026-08-05T17:00:27+00:00.
