# Agent guide — portolan-catalog-stlouis

Cloud-native mirror of City of St. Louis open data. The published catalog
lives in `catalog/` and is synced 1:1 to
`s3://us-west-2.opendata.source.coop/tge-labs/st-louis-open-data-mirror`
(public: `https://data.source.coop/tge-labs/st-louis-open-data-mirror`).

## The rules

1. **`catalog/` is generated.** STAC json, READMEs, styles, thumbnails all
   come from the pipeline (`tools/`, run order in README.md). Fix the
   generator, not the output.
2. **Never invent metadata.** Descriptions come verbatim from the portal
   (`docs/portal-descriptions.json`); zoning district names come from the
   city's own ArcGIS renderer labels. If a fact isn't in the source, leave
   it out.
3. **`tools/sources.py` is the source of truth** for what each collection
   is and where it comes from. Change sources there, then re-run
   fetch → assemble → add → finalize.
   `SOURCE_FILES` in the same file lists the city's own downloadable
   originals per collection; they become `source`-role assets whose hrefs
   point at stlouis-mo.gov, not at this mirror. Only list files that really
   are that layer — the portal bundles unrelated downloads on shared dataset
   pages. A live ArcGIS service is an API, not a download, so it gets a
   `rel: via` link instead; pinning a checksum to a query endpoint would
   rot on the next upstream edit. After changing `SOURCE_FILES`, re-run
   `tools/fetch_source_meta.py` — remote assets carry the size and digest of
   the bytes the city actually served, never a guess.
4. **Spec target**: Portolan v0.1.0 plus PR #97 (one style asset per
   collection carries `roles: ["style","default"]`) and PR #124
   (collection-level `table:columns`/`table:row_count`/`table:primary_geometry`).
5. **Legends**: portolan-browser reads only the first `fill` layer's
   `fill-color` (`match`/`step`). Data-driven styles must lead with an
   inert `fill-opacity: 0` legend layer — `tools/make_styles.py` does this;
   keep it that way.
6. **Overture collections are not city data.** The 10 `overture-*`
   collections are St. Louis-bbox extracts of Overture Maps Foundation
   releases (`OVERTURE_SOURCES` in `tools/sources.py`, extracted by
   `tools/fetch_overture.py`; geometries clipped to the box). Their PMTiles
   are Overture's own release-pinned global theme tiles referenced by URL —
   don't build local tiles for them, and never hash the remote archives
   (19–195 GB). One exception, `OVERTURE_LOCAL` in `tools/make_pmtiles.py`:
   `overture-addresses` is tiled locally from its clipped parquet like a
   city collection — the global addresses tileset only exists at z14 and is
   as good as empty here. The gap is in the theme itself: Overture has no
   address data for the City of St. Louis proper; the extract's ~99k points
   are the county/Illinois fringe inside the bbox (densest around
   Wellston), which is why its styles, thumbnail frame, and description all
   point there. Bumping `OVERTURE_RELEASE` means re-running
   fetch_overture → assemble → finalize so parquet, tile URLs, and styles
   move in lockstep. Descriptions live in `docs/overture-descriptions.json`
   (wording from Overture's docs — same never-invent rule) and every
   description says plainly that the data is Overture's, not the city's.
7. **Census-family collections are not city data either.** The 6
   `demographics/` collections (`CENSUS_SOURCES` in `tools/sources.py`,
   fetched by `tools/fetch_census.py`) are federal/third-party: ACS
   2020–2024 5-year (block groups + tracts), LODES 2023, HOLC redlining
   (Mapping Inequality, CC BY-NC-SA — the one non-commercial license
   here), CDC PLACES. Unlike Overture they build **local** PMTiles like
   city collections. Non-negotiables: every ACS estimate ships with its
   `*_moe` (90% confidence level) and headline columns a `*_cv`; jam
   values become NULL, never numbers; medians are never aggregated;
   derived rates propagate MOE with the Census Bureau's formulas, not
   naive division. ACS comes from the table-based Summary File (no API
   key — the Data API now requires one); fetch_census pins every table
   line number against the release's own table-shells file, so a vintage
   bump that moves a line fails loudly. Bumping `ACS_RELEASE` /
   `LODES_YEAR` / geometry vintage means re-running
   fetch_census → assemble → make_pmtiles → finalize in lockstep, and the
   CB geometry vintage must match the ACS vintage (GENZ2024 for 2020–2024;
   cartographic boundaries, not TIGER — TIGER extends block groups into
   the Mississippi). Descriptions live in `docs/census-descriptions.json`
   (wording from the agencies' own docs — same never-invent rule); column
   glosses carry their ACS table id in `docs/column-notes.json`.

## Data quirks discovered during the build

- BOE precinct FeatureServers 400 on paged queries — precincts use the
  static shapefile.
- The SLDC "LRA Inventory" service layer contains **every** city parcel
  with an `LRA` yes/no flag; the real inventory is the `LRA='YES'` subset
  (filtered in `tools/assemble.py`).
- 311 CSVs are per-year with mixed encodings (utf-8/cp1252) and ~450 rows
  of garbage coordinates; `tools/fetch.py`/`assemble.py` normalize, merge,
  reproject Web-Mercator SRX/SRY to 4326, and null out-of-bbox points.
- `prclsale.zip` is an Access MDB → `mdb-export` (mdbtools), with the
  MDB's own CdSaleType lookup joined in as `SaleTypeDescr`.
- Parcel join key: `HANDLE` / `ParcelId` on parcels; `AsrParcelId` on
  property-sales.
- `static.stlouis-mo.gov` and `www.stlouis-mo.gov` drop TLS handshakes under
  sustained load — the same URL 200s one minute and fails to connect the
  next, and it stays unhappy for a while after a big pull. Not a block on any
  particular path. `tools/fetch_source_meta.py --retries N` rides it out.
- A dropped connection reads as a clean EOF, so a truncated download hashes
  fine and lies. `hash_url` checks the byte count against `Content-Length`;
  rashid's PTL-DAT-001/002 catch anything that slips past.
- `catalog/health/animal-bites`: 6,359 rows but only 217 non-null geometries.
  The city-boundary clip in `assemble.py` nulls ~96% of the geocoded points —
  either the clip is wrong or the source coordinates are not what we assume.
  Unresolved; it predates the source-asset work.
- DuckDB spatial's `ST_Distance_Sphere` read these files' lon/lat in the
  wrong axis order in testing (a longitude step measured as latitude). For
  meters, `ST_Transform(geom, 'EPSG:4326', 'EPSG:26915', always_xy :=
  true)` first, then `ST_Distance`/`ST_DWithin` — the demographics
  AGENTS.md documents this for consumers too.
- Race-iterated ACS tables (B-tables with A–I suffixes) are inconsistently
  published at block-group level: B25003B yes, but B19013B/B17020B/B01001B
  are tract-only. Test empirically (grep the summary-file .dat for
  `^1500000US`) before assuming.
- `portolan add <dir>/ --pmtiles` on a geometry-less parquet drops a stray
  `versions.json` at the catalog root instead of tracking the collection
  (the CLI can't track tabular parquet); lodes-commutes is hand-authored by
  `finalize_stac.build_tabular` like property-sales, and the stray dir was
  deleted.
- `portolan add --pmtiles` builds z0–z8 tiles; the census choropleths need
  z12 for crisp block-group edges, so `tools/make_pmtiles.py` re-tiles
  them (it also skips Overture — rule 6 — and carries per-family
  `--attribution`).

## Environment

`portolan` CLI (uv tool, editable from ~/repos/portolan-cli, with
gpio-pmtiles), GDAL ≥ 3.9 with Parquet driver (conda-forge; Ubuntu's
gdal-bin lacks it), tippecanoe, duckdb, mdbtools, Node 20/22/24 (not 23)
for chiitiler thumbnails.
