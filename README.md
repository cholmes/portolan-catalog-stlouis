# City of St. Louis Open Data — Cloud-Native Mirror

**[🗺️ Open the St. Louis data browser](https://cholmes.github.io/stlouis-data-browser/)** — map
preview, legends, schema, and direct downloads for all 61 collections ·
[Browse on Source Cooperative](https://source.coop/tge-labs/st-louis-open-data-mirror)

A cloud-native mirror of the most-used datasets from the
[City of St. Louis open data portal](https://www.stlouis-mo.gov/data/):
parcels, boundaries, streets, trees, development districts, 311 requests,
and property sales as **GeoParquet** + **PMTiles** with **STAC** metadata,
following the [Portolan spec](https://github.com/portolan-sdi/portolan-spec).
Not an official city service.

- Catalog root: `https://data.source.coop/tge-labs/st-louis-open-data-mirror/catalog.json`
- 61 collections in 11 topic catalogs: 51 city datasets (geospatial +
  parcel-joinable tabular, including 1.48M geocoded 311 requests) plus 10
  `overture-*` collections
- The `overture-*` collections are St. Louis-bbox extracts of the
  [Overture Maps Foundation](https://overturemaps.org/) global datasets
  (buildings, transportation, places, addresses, divisions, and the base
  theme) — **not city data**, included to demonstrate blending other
  St. Louis-relevant open data into the catalog. Their map tiles reference
  Overture's own release-pinned global PMTiles rather than files built here
  (except `overture-addresses`, tiled locally — Overture's global address
  tiles have no St. Louis coverage).
- Every geo collection ships 2–5 MapLibre styles with legends — including
  the city's own ArcGIS renderer where the source was a live service, and
  Overture-Explorer-derived palettes for the Overture layers
- Roadmap to mirror *everything* geo and parcel-joinable:
  [docs/full-ingestion-plan.md](docs/full-ingestion-plan.md)

## Quick start

```sql
-- DuckDB: LRA-owned vacant lots by neighborhood, no download needed
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
WITH lots AS (
  SELECT ST_Centroid(geometry) AS pt
  FROM 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/lra-property/lra-property.parquet'
  WHERE Usage ILIKE 'vacant lot'
)
SELECT n.NHD_NAME, count(*) AS lra_vacant_lots
FROM lots
JOIN 'https://data.source.coop/tge-labs/st-louis-open-data-mirror/neighborhoods/neighborhoods.parquet' n
  ON ST_Intersects(lots.pt, n.geometry)
GROUP BY 1 ORDER BY 2 DESC LIMIT 10;
```

## Repository layout

| Path | Purpose |
|---|---|
| `catalog/` | The published tree — synced 1:1 to Source Cooperative. Parquet/PMTiles are generated, gitignored artifacts. |
| `staging/` | Per-dataset provenance: `dataset-info.json`, downloaded sources (gitignored) |
| `tools/` | The pipeline (see below) |
| `tests/` | Conformance and consistency gates |
| `docs/` | Source inventories, data profile, the full-ingestion plan |

## Pipeline

Run from the repo root, in order:

| Step | Command | What it does |
|---|---|---|
| 1 | `python3 tools/fetch.py` | ArcGIS extracts (`portolan extract arcgis --raw`, incl. city renderer styles + field metadata), static downloads, and Overture DuckDB bbox extracts (`tools/fetch_overture.py`) into `staging/` |
| 1b | `python3 tools/fetch_source_meta.py` | Size + sha2-256 of the city's own source files → `sources/source_checksums.json` (bytes streamed and discarded) |
| 2 | `python3 tools/assemble.py` | Normalize everything to spec GeoParquet (zstd, covering bbox, Hilbert order) at `catalog/<id>/<id>.parquet` |
| 3 | `portolan add . --pmtiles --datetime <sync>` (in `catalog/`) | STAC collections + PMTiles |
| 4 | `python3 tools/write_metadata.py` | `.portolan/metadata.yaml` from portal text (verbatim descriptions) |
| 5 | `python3 tools/make_styles.py` | 63 MapLibre styles with legends (see the file's docstring for the legend mechanism) |
| 6 | `python3 tools/finalize_stac.py` | Providers, license/via links, default-style roles, checksums, `source` assets pointing upstream, tabular collection |
| 7 | `portolan readme` (in `catalog/`) | Generated READMEs + AGENTS.md |
| 8 | `bash tools/make_thumbnails.sh` | chiitiler renders of each default style |
| 9 | `python3 tests/run_all.py` | Gates |
| 10 | `portolan push` (in `catalog/`) | Publish to Source Cooperative |

## Licensing

⚠️ The City of St. Louis publishes **no explicit license** for this data.
Each collection links its portal dataset page (`rel: license` / `rel: via`);
consult those pages and the departments for terms. This mirror declares
`license: "other"` throughout.

## Related

- Browser: [cholmes/stlouis-data-browser](https://github.com/cholmes/stlouis-data-browser)
- Pattern siblings: [portolan-catalog-trimet](https://github.com/cholmes/portolan-catalog-trimet),
  [portolan-nl-catalog](https://github.com/cholmes/portolan-nl-catalog)
