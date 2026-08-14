# AGENTS.md — Demographics

Department sub-catalog with 6 collections. Access pattern for each:

```sql
INSTALL httpfs; LOAD httpfs;  -- DuckDB
-- ACS Demographics — Block Groups
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/acs-block-groups/acs-block-groups.parquet' LIMIT 5;
-- ACS Demographics — Tracts
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/acs-tracts/acs-tracts.parquet' LIMIT 5;
-- LODES Jobs
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/lodes-jobs/lodes-jobs.parquet' LIMIT 5;
-- LODES Commute Flows
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/lodes-commutes/lodes-commutes.parquet' LIMIT 5;
-- HOLC Redlining Grades (1930s)
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/holc-redlining/holc-redlining.parquet' LIMIT 5;
-- CDC PLACES Health Measures
SELECT * FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/cdc-places/cdc-places.parquet' LIMIT 5;
```

Each collection has its own AGENTS.md with fields, quirks, and joins. Root catalog: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/catalog.json`.

## Cross-dataset analysis

The point of this group: census context turns the city's own data into
answers about equity. Every query below runs as-is in DuckDB and was
validated against the published files. Two ground rules first:

- **Distances**: geometry is WGS84 lon/lat. DuckDB's `ST_Distance_Sphere`
  reads coordinates in the wrong axis order for these files (it treated a
  longitude step as latitude in testing), so for meters, transform to UTM
  15N first: `ST_Transform(geom, 'EPSG:4326', 'EPSG:26915', always_xy :=
  true)` — then `ST_Distance`/`ST_DWithin` are in meters.
- **Reliability**: ACS block-group estimates are noisy. Check `*_cv`
  (over 0.30 = unreliable) before leaning on any single block group;
  quintile/grade aggregates like the ones below are the safe pattern.

### 1. Is the LRA land bank racially and economically concentrated?

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
WITH lra AS (
  SELECT ST_Centroid(geometry) AS pt
  FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/housing/lra-property/lra-property.parquet'
  WHERE geometry IS NOT NULL),
bg AS (
  SELECT geoid, geometry, population, pct_black, median_hh_income,
         ntile(5) OVER (ORDER BY median_hh_income) AS income_q
  FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/acs-block-groups/acs-block-groups.parquet'
  WHERE median_hh_income IS NOT NULL AND population > 0),
counts AS (
  SELECT bg.geoid, any_value(bg.income_q) AS income_q,
         any_value(bg.pct_black) AS pct_black,
         any_value(bg.population) AS population, count(lra.pt) AS n
  FROM bg LEFT JOIN lra ON ST_Within(lra.pt, bg.geometry)
  GROUP BY bg.geoid)
SELECT income_q AS income_quintile,
       round(avg(pct_black), 1) AS avg_pct_black,
       sum(n) AS lra_parcels,
       round(1000.0 * sum(n) / sum(population), 1) AS lra_per_1000_residents
FROM counts GROUP BY 1 ORDER BY 1;
-- 2026-08 sync: quintile 1 (avg 75.6% Black) holds 117.1 LRA parcels per
-- 1,000 residents; quintile 5 (15.6% Black) holds 1.1 — a 100x gradient.
```

### 2. Does 311 response time track income?

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
WITH bg AS (
  SELECT geoid, geometry, median_hh_income,
         ntile(5) OVER (ORDER BY median_hh_income) AS income_q
  FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/acs-block-groups/acs-block-groups.parquet'
  WHERE median_hh_income IS NOT NULL),
req AS (
  SELECT geometry,
         date_diff('day', DATETIMEINIT, DATETIMECLOSED) AS days_to_close
  FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/government/csb-311-requests/csb-311-requests.parquet'
  WHERE geometry IS NOT NULL AND DATETIMECLOSED IS NOT NULL
    AND DATETIMEINIT >= TIMESTAMP '2023-01-01'
    AND "GROUP" = 'Trash/Debris/Green Waste')
SELECT bg.income_q, count(*) AS requests,
       round(median(req.days_to_close), 1) AS median_days,
       round(avg(req.days_to_close), 1) AS avg_days
FROM req JOIN bg ON ST_Within(req.geometry, bg.geometry)
GROUP BY 1 ORDER BY 1;
-- 2026-08 sync: the median is 3 days in every quintile — but the mean runs
-- 17.2 days (poorest) to 10.6 (richest). Typical service is equal; the
-- long tail of unresolved cases concentrates in poor block groups. Always
-- control for request category: the mix differs by neighborhood.
```

### 3. Where do building permits go?

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
WITH bg AS (
  SELECT geoid, geometry, housing_units, median_hh_income,
         ntile(5) OVER (ORDER BY median_hh_income) AS income_q
  FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/acs-block-groups/acs-block-groups.parquet'
  WHERE median_hh_income IS NOT NULL AND housing_units > 0),
located AS (
  SELECT ST_Centroid(par.geometry) AS pt,
         try_cast(pm.ESTPROJECTCOST AS DOUBLE) AS cost
  FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/housing/electrical-permits/electrical-permits.parquet' pm
  JOIN 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/urban-development-and-planning/parcels/parcels.parquet' par
    ON pm.HANDLE = par.HANDLE
  WHERE try_cast(pm.APPDATE AS TIMESTAMP) >= TIMESTAMP '2020-01-01'
    AND try_cast(pm.ESTPROJECTCOST AS DOUBLE) > 0
    AND par.geometry IS NOT NULL),
per_bg AS (
  SELECT bg.geoid, any_value(bg.income_q) AS income_q,
         any_value(bg.housing_units) AS housing_units,
         count(l.pt) AS permits, coalesce(sum(l.cost), 0) AS invested
  FROM bg LEFT JOIN located l ON ST_Within(l.pt, bg.geometry)
  GROUP BY bg.geoid)
SELECT income_q, sum(permits) AS permits,
       round(sum(invested) / 1e6, 1) AS total_millions,
       round(sum(invested) / sum(housing_units)) AS dollars_per_unit
FROM per_bg GROUP BY 1 ORDER BY 1;
-- 2026-08 sync: 6,170 electrical permits since 2020 in the poorest
-- quintile vs 16,431 in the fourth. Dollar totals are lumpier — one
-- hospital project outweighs a neighborhood — so read counts, not dollars,
-- as the disinvestment signal. Same pattern works for plumbing-permits,
-- mechanical-permits, occupancy-permits.
```

### 4. How far are car-free households from food stores?

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
WITH stores AS (
  SELECT ST_Transform(geometry, 'EPSG:4326', 'EPSG:26915',
                      always_xy := true) AS g
  FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/business-and-industry/overture-places/overture-places.parquet'
  WHERE basic_category = 'food_and_beverage_store'),
bg AS (
  SELECT geoid, households, pct_hh_no_vehicle,
         ST_Transform(ST_Centroid(geometry), 'EPSG:4326', 'EPSG:26915',
                      always_xy := true) AS c
  FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/acs-block-groups/acs-block-groups.parquet'
  WHERE households > 0 AND pct_hh_no_vehicle IS NOT NULL),
nearest AS (
  SELECT bg.geoid, any_value(bg.pct_hh_no_vehicle) AS no_veh,
         min(ST_Distance(bg.c, s.g)) AS dist_m
  FROM bg CROSS JOIN stores s GROUP BY bg.geoid)
SELECT CASE WHEN no_veh >= 20 THEN '20%+ car-free' ELSE 'under 20%' END
         AS bucket,
       count(*) AS bgs,
       round(median(dist_m)) AS median_m_to_food_store,
       round(100.0 * count(*) FILTER (WHERE dist_m <= 400) / count(*), 1)
         AS pct_within_400m
FROM nearest GROUP BY 1 ORDER BY 1;
-- 2026-08 sync: car-free-heavy block groups sit slightly CLOSER to food
-- stores (median 339 m vs 379 m) — car-freeness tracks density. Caveat:
-- Overture's category lumps corner stores with supermarkets, so this
-- measures proximity to any food retail, not to a full grocery.
```

### 5. Do the 1930s redlining grades still predict outcomes?

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT h.grade,
       count(*) AS block_groups,
       round(avg(bg.median_hh_income)) AS avg_median_income,
       round(avg(bg.median_home_value)) AS avg_home_value,
       round(avg(bg.pct_vacant_units), 1) AS avg_pct_vacant
FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/acs-block-groups/acs-block-groups.parquet' bg
JOIN 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/holc-redlining/holc-redlining.parquet' h
  ON ST_Within(ST_Centroid(bg.geometry), h.geometry)
WHERE h.grade IS NOT NULL
GROUP BY 1 ORDER BY 1;
-- 2026-08 sync: A-graded areas average $81,467 median income today,
-- D-graded $54,155 — nine decades after the maps were drawn. ACS vacancy
-- runs 7.7% (A) to 21.7% (C). D's home values are pulled up by
-- now-gentrified downtown-adjacent areas — worth its own follow-up query.
```

### 6. Crime rates without the daytime-population lie

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
WITH cr AS (
  SELECT geometry
  FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/law-safety-and-justice/crime/crime.parquet'
  WHERE geometry IS NOT NULL AND CrimeAgainst = 'Person'),
bg AS (
  SELECT a.geoid, a.geometry, a.population, j.jobs_total
  FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/acs-block-groups/acs-block-groups.parquet' a
  JOIN 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/demographics/lodes-jobs/lodes-jobs.parquet' j USING (geoid)),
counts AS (
  SELECT bg.geoid, any_value(bg.population) AS pop,
         any_value(bg.jobs_total) AS jobs, count(cr.geometry) AS crimes
  FROM bg LEFT JOIN cr ON ST_Within(cr.geometry, bg.geometry)
  GROUP BY bg.geoid)
SELECT geoid, crimes, pop, jobs,
       round(1000.0 * crimes / nullif(pop, 0)) AS per_1000_residents,
       round(1000.0 * crimes / (pop + jobs)) AS per_1000_ambient
FROM counts
ORDER BY per_1000_residents DESC NULLS LAST LIMIT 8;
-- 2026-08 sync: block group 295101270002 (341 residents, 2,759 jobs)
-- drops from 1,261 crimes per 1,000 residents to 139 per 1,000 ambient
-- population — a 9x correction. Per-capita crime maps overstate job
-- centers; LODES is the fix.
```

Other angles these collections support: 311 reporting rate vs
`pct_no_internet` (digital-divide bias in complaint data), commute-flow
maps from `lodes-commutes` joined to block-group geometry, CDC PLACES
`lacktrpt`/`foodinsecu` against transit and vacancy layers, and
`acs-tracts.pct_uninsured` against `cdc-places.access2` (survey vs model
on the same question).
