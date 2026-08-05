# AGENTS.md — November 2024 Election Results by Precinct

This is the detailed vote extract (dve) from the November 5, 2024, General Municipal Election for the City of St. Louis.

24,030 rows; tabular (no geometry).

## Access

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/elections/election-results-nov-2024/election-results-nov-2024.parquet' LIMIT 5;
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

## Reproduce the geometry join

This collection is published as plain (non-geo) Parquet, exactly as the city publishes it; its map layer (`election-results-nov-2024.pmtiles`) is materialized by joining to `election-precincts`. To build your own GeoParquet:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
COPY (
  SELECT p.name, any_value(t.Registered_Voters) AS Registered_Voters, any_value(t.Ballots_Cast) AS Ballots_Cast, TRY_CAST(any_value(t.Turnout_Percentage) AS DOUBLE) AS Turnout_Percentage, sum(t.Total_Votes) FILTER (t.Choice_Name LIKE '%HARRIS%') AS Pres_Harris, sum(t.Total_Votes) FILTER (t.Choice_Name LIKE '%TRUMP%') AS Pres_Trump, round(sum(t.Total_Votes) FILTER (t.Choice_Name LIKE '%HARRIS%') * 1.0 / NULLIF(sum(t.Total_Votes) FILTER (t.Choice_Name LIKE '%HARRIS%') + sum(t.Total_Votes) FILTER (t.Choice_Name LIKE '%TRUMP%'), 0), 4) AS Pres_Dem_TwoPartyShare, p.geometry
  FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/elections/election-results-nov-2024/election-results-nov-2024.parquet' t
  JOIN 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/elections/election-precincts/election-precincts.parquet' p
    ON TRY_CAST(regexp_extract(t.F_Precinct, 'Ward (\d+)', 1) AS INT) = TRY_CAST(regexp_extract(p.name, 'W (\d+) P', 1) AS INT) AND TRY_CAST(regexp_extract(t.F_Precinct, 'Precinct (\d+)', 1) AS INT) = TRY_CAST(regexp_extract(p.name, 'P (\d+)', 1) AS INT)
  GROUP BY p.name, p.geometry
) TO 'election-results-nov-2024-geo.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);
```

Then convert as needed:

```bash
gpio convert geoparquet election-results-nov-2024-geo.parquet election-results-nov-2024-geo-optimized.parquet
gpio convert geopackage election-results-nov-2024-geo.parquet election-results-nov-2024.gpkg
gpio convert shapefile election-results-nov-2024-geo.parquet election-results-nov-2024.shp
```

## Links

- [View on the data browser](https://cholmes.github.io/stlouis-data-browser/#/elections/election-results-nov-2024/collection.json) — map, styles, legends, downloads
- [Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror/elections/election-results-nov-2024/) — rendered README and file listing
- [Source dataset](https://stlcity.maps.arcgis.com/home/item.html?id=6e72fa855cd445f7af37d79615f602d0) on the City of St. Louis open data portal

## Provenance

Mirror of [November 2024 Election Results by Precinct](https://stlcity.maps.arcgis.com/home/item.html?id=6e72fa855cd445f7af37d79615f602d0) from the City of St. Louis; source: https://services6.arcgis.com/HZXbCkpCSqbGd0vK/arcgis/rest/services/Nov24_Detailed_Vote_Totals_Test/FeatureServer. No explicit license is published — see the source page. Synced 2026-08-05T19:58:51+00:00.
