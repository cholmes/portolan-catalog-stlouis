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

## Environment

`portolan` CLI (uv tool, editable from ~/repos/portolan-cli, with
gpio-pmtiles), GDAL ≥ 3.9 with Parquet driver (conda-forge; Ubuntu's
gdal-bin lacks it), tippecanoe, duckdb, mdbtools, Node 20/22/24 (not 23)
for chiitiler thumbnails.
