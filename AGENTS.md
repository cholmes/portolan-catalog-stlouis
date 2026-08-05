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

## Environment

`portolan` CLI (uv tool, editable from ~/repos/portolan-cli, with
gpio-pmtiles), GDAL ≥ 3.9 with Parquet driver (conda-forge; Ubuntu's
gdal-bin lacks it), tippecanoe, duckdb, mdbtools, Node 20/22/24 (not 23)
for chiitiler thumbnails.
