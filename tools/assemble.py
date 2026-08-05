#!/usr/bin/env python3
"""Assemble catalog/<id>/<id>.parquet from staged sources.

Every output is converted with gpio (geoparquet.io) to spec-conformant
GeoParquet: zstd, covering bbox with stats, Hilbert row order. Tabular
sources get plain Parquet via gpio --allow-no-geometry. Exception: the
311 CSV still goes through ogr2ogr because gpio's CSV reader drops rows
with empty lat/lon and we deliberately keep the ~18k coordinate-less
requests as null-geometry rows. City renderer styles extracted from ArcGIS are copied
into catalog/<id>/styles/city-renderer.json for make_styles.py to finish
(it injects the pmtiles source URL and legend layers).

Usage: python3 tools/assemble.py [collection-id ...]   (default: all)
"""

import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sources import SOURCES

ROOT = Path(__file__).resolve().parent.parent
STAGING = ROOT / "staging"
CATALOG = ROOT / "catalog"

GEO_LCO = [
    "-lco", "COMPRESSION=ZSTD",
    "-lco", "WRITE_COVERING_BBOX=YES",
    "-lco", "SORT_BY_BBOX=YES",
    "-lco", "ROW_GROUP_SIZE=20000",
]


def run(cmd: list) -> None:
    proc = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"{' '.join(str(c) for c in cmd)}\n{proc.stderr[-800:]}")


def restore_stats(path) -> None:
    """Rewrite with pyarrow to guarantee row-group min/max statistics.

    GDAL's Parquet writer drops stats on the bbox covering column when any
    rows have null geometry (spec/rashid PTL-DAT-007 requires them). pyarrow
    preserves the `geo` schema metadata and row order.
    """
    import pyarrow.parquet as pq
    t = pq.read_table(path)
    pq.write_table(t, path, compression="zstd", row_group_size=20000,
                   write_statistics=True)


def rename_geom(path) -> None:
    """Rename gpio's shapefile geometry column "geom" to "geometry".

    Note: `gpio convert reproject` output can arrive without `geo` schema
    metadata; downstream (make_pmtiles, gpio geojson) requires it. If it is
    missing after the rename, rebuild a minimal GeoParquet 1.1 block."""
    import json as _json
    import pyarrow.parquet as pq
    t = pq.read_table(path)
    if "geom" not in t.schema.names:
        return
    t = t.rename_columns(["geometry" if n == "geom" else n
                          for n in t.schema.names])
    meta = dict(t.schema.metadata or {})
    if b"geo" in meta:
        geo = _json.loads(meta[b"geo"])
        if "geom" in geo.get("columns", {}):
            geo["columns"]["geometry"] = geo["columns"].pop("geom")
        if geo.get("primary_column") == "geom":
            geo["primary_column"] = "geometry"
    else:
        s = None
        # NB: the file on disk still has the pre-rename column name "geom"
        for inner in (f"SELECT ST_GeomFromWKB(geom) g FROM read_parquet('{path}')",
                      f"SELECT geom g FROM read_parquet('{path}')"):
            stats = subprocess.run(
                ["duckdb", "-json", "-c",
                 "INSTALL spatial; LOAD spatial; "
                 "SELECT min(ST_XMin(g)) a, min(ST_YMin(g)) b, "
                 "max(ST_XMax(g)) c, max(ST_YMax(g)) d, "
                 "list(DISTINCT ST_GeometryType(g))::VARCHAR gt "
                 f"FROM ({inner})"],
                capture_output=True, text=True)
            if stats.returncode == 0 and stats.stdout.strip():
                s = _json.loads(stats.stdout)[0]
                break
        if s is None:
            raise RuntimeError(f"geometry stats failed for {path}: {stats.stderr[-200:]}")
        gtypes = sorted({("Multi" + x.strip().upper().replace("MULTI", "").title()
                          if "MULTI" in x.upper() else x.strip().title())
                         for x in s["gt"].strip("[]").split(",")})
        geo = {"version": "1.1.0", "primary_column": "geometry",
               "columns": {"geometry": {
                   "encoding": "WKB", "geometry_types": gtypes, "crs": None,
                   "bbox": [s["a"], s["b"], s["c"], s["d"]],
                   "covering": {"bbox": {
                       "xmin": ["bbox", "xmin"], "ymin": ["bbox", "ymin"],
                       "xmax": ["bbox", "xmax"], "ymax": ["bbox", "ymax"]}}}}}
    meta[b"geo"] = _json.dumps(geo).encode()
    t = t.replace_schema_metadata(meta)
    pq.write_table(t, path, compression="zstd", row_group_size=20000,
                   write_statistics=True)


def prepare_csb(dest: Path) -> None:
    """Merge the per-year 311 CSVs into one WGS84 CSV.

    Web-Mercator SRX/SRY become lon/lat; points outside the buffered city
    boundary (requires catalog/city-boundary to be assembled first) are
    nulled but their rows kept. Assumes staging/csb-311-requests/data/csb/
    holds encoding-normalized per-year CSVs merged to csb-merged.csv by
    tools/fetch.py.
    """
    merged = dest.parent / "csb-merged.csv"
    boundary = CATALOG / "city-boundary" / "city-boundary.parquet"
    if not boundary.exists():
        raise RuntimeError("assemble city-boundary before csb-311-requests")
    run(["duckdb", "-c", f"""
        INSTALL spatial; LOAD spatial;
        CREATE TEMP TABLE city AS
          SELECT ST_Buffer(geometry, 0.005) g FROM '{boundary}';
        COPY (
          SELECT * EXCLUDE (SRX, SRY, lon, lat),
            CASE WHEN keep THEN round(lon, 7) END AS lon,
            CASE WHEN keep THEN round(lat, 7) END AS lat
          FROM (
            SELECT *, lon IS NOT NULL AND lat IS NOT NULL
                   AND ST_Contains((SELECT g FROM city), ST_Point(lon, lat)) AS keep
            FROM (
              SELECT *,
                CASE WHEN TRY_CAST(SRX AS DOUBLE) IS NOT NULL AND TRY_CAST(SRY AS DOUBLE) IS NOT NULL AND TRY_CAST(SRX AS DOUBLE) <> 0
                     THEN ST_X(ST_Transform(ST_Point(TRY_CAST(SRX AS DOUBLE), TRY_CAST(SRY AS DOUBLE)), 'EPSG:3857', 'EPSG:4326', always_xy := true)) END AS lon,
                CASE WHEN TRY_CAST(SRX AS DOUBLE) IS NOT NULL AND TRY_CAST(SRY AS DOUBLE) IS NOT NULL AND TRY_CAST(SRX AS DOUBLE) <> 0
                     THEN ST_Y(ST_Transform(ST_Point(TRY_CAST(SRX AS DOUBLE), TRY_CAST(SRY AS DOUBLE)), 'EPSG:3857', 'EPSG:4326', always_xy := true)) END AS lat
              FROM read_csv('{merged}', header=true, all_varchar=true)
            )
          )
        ) TO '{dest}' (HEADER);
    """])


def find_extract_parquet(coll_id: str) -> Path:
    hits = sorted(p for p in (STAGING / "extracts" / coll_id).rglob("*.parquet")
                  if not p.name.endswith("_filtered.parquet"))
    if not hits:
        raise FileNotFoundError(f"no extracted parquet for {coll_id}")
    if len(hits) > 1:
        raise RuntimeError(f"multiple parquets for {coll_id}: {hits}")
    return hits[0]


def static_source_file(coll_id: str) -> Path:
    """Locate the usable source file among downloaded/unpacked statics."""
    data = STAGING / coll_id / "data"
    # 311 requests ship as per-year CSVs with mixed encodings; fetch step
    # normalizes and merges them into one UTF-8 CSV.
    if coll_id == "csb-311-requests":
        return data / "csb-merged.csv"
    for pattern in ("*.geojson", "*.shp", "*.dbf", "*.csv"):
        hits = sorted(data.rglob(pattern))
        # Ignore macOS zip cruft
        hits = [h for h in hits if "__MACOSX" not in str(h)]
        if hits:
            return hits[0]
    raise FileNotFoundError(f"no usable source file under {data}")


def assemble(coll_id: str) -> dict:
    src_def = SOURCES[coll_id]
    out_dir = CATALOG / coll_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{coll_id}.parquet"

    # Permit families ship as per-year CSVs with mixed encodings — normalize
    # and merge, then plain tabular parquet.
    MULTI_CSV = {"electrical-permits", "mechanical-permits",
                 "plumbing-permits", "occupancy-permits"}
    if coll_id in MULTI_CSV:
        data = STAGING / coll_id / "data"
        src_dir = next(d for d in data.iterdir() if d.is_dir())
        norm = data / "utf8"
        norm.mkdir(exist_ok=True)
        for fcsv in sorted(src_dir.glob("*.csv")):
            raw = fcsv.read_bytes()
            try:
                txt = raw.decode("utf-8")
            except UnicodeDecodeError:
                txt = raw.decode("cp1252", errors="replace")
            (norm / fcsv.name).write_text(txt, encoding="utf-8")
        run(["duckdb", "-c",
             f"COPY (SELECT * FROM read_csv('{norm}/*.csv', union_by_name=true, "
             f"all_varchar=true)) TO '{out}' "
             "(FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 20000)"])
        n = subprocess.run(
            ["duckdb", "-noheader", "-list", "-c", f"SELECT count(*) FROM '{out}'"],
            capture_output=True, text=True).stdout.strip()
        return {"rows": int(n), "tabular": True,
                "source_file": f"{len(list(norm.glob('*.csv')))} yearly CSVs merged"}

    # Animal bites carry Web-Mercator SRX/SRY like the 311 data — promote to
    # points, nulling coordinates outside the buffered city boundary.
    if coll_id == "animal-bites":
        data = STAGING / coll_id / "data"
        boundary = CATALOG / "city-boundary" / "city-boundary.parquet"
        prepped = data / "animal-bites-4326.csv"
        run(["duckdb", "-c", f"""
            INSTALL spatial; LOAD spatial;
            CREATE TEMP TABLE city AS
              SELECT ST_Buffer(geometry, 0.005) g FROM '{boundary}';
            COPY (
              SELECT * EXCLUDE (SRX, SRY, lon, lat),
                CASE WHEN keep THEN round(lon, 7) END AS lon,
                CASE WHEN keep THEN round(lat, 7) END AS lat
              FROM (
                SELECT *, lon IS NOT NULL AND lat IS NOT NULL
                       AND ST_Contains((SELECT g FROM city), ST_Point(lon, lat)) AS keep
                FROM (
                  SELECT *,
                    CASE WHEN TRY_CAST(SRX AS DOUBLE) IS NOT NULL AND TRY_CAST(SRY AS DOUBLE) IS NOT NULL AND TRY_CAST(SRX AS DOUBLE) <> 0
                         THEN ST_X(ST_Transform(ST_Point(TRY_CAST(SRX AS DOUBLE), TRY_CAST(SRY AS DOUBLE)), 'EPSG:3857', 'EPSG:4326', always_xy := true)) END AS lon,
                    CASE WHEN TRY_CAST(SRX AS DOUBLE) IS NOT NULL AND TRY_CAST(SRY AS DOUBLE) IS NOT NULL AND TRY_CAST(SRX AS DOUBLE) <> 0
                         THEN ST_Y(ST_Transform(ST_Point(TRY_CAST(SRX AS DOUBLE), TRY_CAST(SRY AS DOUBLE)), 'EPSG:3857', 'EPSG:4326', always_xy := true)) END AS lat
                  FROM read_csv('{data}/ANIMAL_BITES.csv', header=true, all_varchar=true)
                )
              )
            ) TO '{prepped}' (HEADER);
        """])
        run(["ogr2ogr", "-f", "Parquet", out, prepped, "-nln", coll_id,
             "-oo", "X_POSSIBLE_NAMES=lon", "-oo", "Y_POSSIBLE_NAMES=lat",
             "-oo", "KEEP_GEOM_COLUMNS=NO",
             "-oo", "AUTODETECT_TYPE=YES", "-oo", "EMPTY_STRING_AS_NULL=YES",
             "-a_srs", "EPSG:4326"] + GEO_LCO)
        restore_stats(out)
        n = subprocess.run(
            ["duckdb", "-noheader", "-list", "-c", f"SELECT count(*) FROM '{out}'"],
            capture_output=True, text=True).stdout.strip()
        return {"rows": int(n), "tabular": False,
                "source_file": "data/ANIMAL_BITES.csv"}

    # Street permits: single CSV with cp1252 bytes — normalize then tabular.
    if coll_id == "street-permits":
        data = STAGING / coll_id / "data"
        raw = (data / "street-permits.csv").read_bytes()
        try:
            txt = raw.decode("utf-8")
        except UnicodeDecodeError:
            txt = raw.decode("cp1252", errors="replace")
        norm = data / "street-permits-utf8.csv"
        norm.write_text(txt, encoding="utf-8")
        run(["duckdb", "-c",
             f"COPY (SELECT * FROM read_csv('{norm}', header=true, all_varchar=true)) "
             f"TO '{out}' (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 20000)"])
        n = subprocess.run(
            ["duckdb", "-noheader", "-list", "-c", f"SELECT count(*) FROM '{out}'"],
            capture_output=True, text=True).stdout.strip()
        return {"rows": int(n), "tabular": True, "source_file": "data/street-permits.csv"}

    # Property taxes: the assessor's Access DB — export the primary Prcl table.
    if coll_id == "property-taxes":
        data = STAGING / coll_id / "data"
        mdb = next(data.rglob("prcl.mdb"))
        with open(data / "Prcl.csv", "w") as f:
            subprocess.run(["mdb-export", str(mdb), "Prcl"], stdout=f, check=True)
        run(["duckdb", "-c",
             f"COPY (SELECT * FROM read_csv('{data}/Prcl.csv', header=true)) "
             f"TO '{out}' (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 20000)"])
        n = subprocess.run(
            ["duckdb", "-noheader", "-list", "-c", f"SELECT count(*) FROM '{out}'"],
            capture_output=True, text=True).stdout.strip()
        return {"rows": int(n), "tabular": True,
                "source_file": str(mdb.relative_to(ROOT))}

    # Property sales ship as an Access MDB: export the PrclSale table with
    # the MDB's own CdSaleType lookup joined in (source-faithful decode).
    if coll_id == "property-sales":
        data = STAGING / coll_id / "data"
        mdb = data / "prclsale.mdb"
        if not mdb.exists():
            run(["unzip", "-o", data / "prclsale.zip", "-d", data])
        for t in ("PrclSale", "CdSaleType"):
            with open(data / f"{t}.csv", "w") as f:
                subprocess.run(["mdb-export", str(mdb), t], stdout=f, check=True)
        run(["duckdb", "-c", f"""
            COPY (
              SELECT s.*, t.Descr AS SaleTypeDescr
              FROM read_csv('{data}/PrclSale.csv', header=true) s
              LEFT JOIN read_csv('{data}/CdSaleType.csv', header=true) t USING (SaleType)
            ) TO '{out}' (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 20000)
        """])
        n = subprocess.run(
            ["duckdb", "-noheader", "-list", "-c", f"SELECT count(*) FROM '{out}'"],
            capture_output=True, text=True).stdout.strip()
        return {"rows": int(n), "tabular": True, "source_file": str(mdb.relative_to(ROOT))}

    # Multi-layer services (bike infrastructure, tornado damage, flood
    # controls…) become one collection: merge the layers with a source_layer
    # column carrying each layer's title.
    n_parts = len([p for p in (STAGING / "extracts" / coll_id).rglob("*.parquet")
                   if not p.name.endswith(("_filtered.parquet", "_merged.parquet"))
                   and p.name != "bike_merged.parquet"]) if src_def["type"] == "arcgis" else 0
    if n_parts > 1:
        parts = sorted(p for p in (STAGING / "extracts" / coll_id).rglob("*.parquet")
                       if not p.name.endswith(("_filtered.parquet", "_merged.parquet"))
                       and p.name != "bike_merged.parquet")
        selects = " UNION ALL BY NAME ".join(
            f"SELECT *, '{p.parent.name.replace('_', ' ').title()}' AS source_layer "
            f"FROM '{p}' WHERE geometry IS NOT NULL AND NOT ST_IsEmpty(geometry)"
            for p in parts)
        merged = STAGING / "extracts" / coll_id / f"{coll_id.replace(chr(45), chr(95))}_merged.parquet"
        run(["duckdb", "-c",
             f"INSTALL spatial; LOAD spatial; COPY ({selects}) TO '{merged}' "
             "(FORMAT PARQUET, COMPRESSION ZSTD)"])
        run(["gpio", "convert", "geoparquet", merged, out])
        restore_stats(out)
        city_style = STAGING / "extracts" / coll_id / "styles" / "city-renderer.json"
        if city_style.exists():
            (out_dir / "styles").mkdir(exist_ok=True)
            shutil.copy(city_style, out_dir / "styles" / "city-renderer.json")
        n = subprocess.run(
            ["duckdb", "-noheader", "-list", "-c", f"SELECT count(*) FROM '{out}'"],
            capture_output=True, text=True).stdout.strip()
        return {"rows": int(n), "tabular": False,
                "source_file": f"{len(parts)} layers merged"}

    if src_def["type"] == "arcgis":
        src = find_extract_parquet(coll_id)
    else:
        src = static_source_file(coll_id)

    # 311 requests carry Web-Mercator SRX/SRY columns — promote to points.
    # The fetch step writes csb-4326.csv: encodings normalized, years merged,
    # coords reprojected to WGS84, and points outside the buffered city
    # boundary nulled (rows kept). lon/lat feed the geometry and are dropped.
    if coll_id == "csb-311-requests":
        src = STAGING / coll_id / "data" / "csb-4326.csv"
        if not src.exists():
            prepare_csb(src)
        cmd = ["ogr2ogr", "-f", "Parquet", out, src, "-nln", coll_id,
               "-oo", "X_POSSIBLE_NAMES=lon", "-oo", "Y_POSSIBLE_NAMES=lat",
               "-oo", "KEEP_GEOM_COLUMNS=NO",
               "-oo", "AUTODETECT_TYPE=YES", "-oo", "EMPTY_STRING_AS_NULL=YES",
               "-a_srs", "EPSG:4326"] + GEO_LCO
        run(cmd)
        restore_stats(out)
        n_check = subprocess.run(
            ["duckdb", "-noheader", "-list", "-c", f"SELECT count(*) FROM '{out}'"],
            capture_output=True, text=True).stdout.strip()
        return {"rows": int(n_check), "tabular": False, "source_file": str(src.relative_to(ROOT))}

    is_tabular = src.suffix in (".dbf", ".csv")
    if not is_tabular and src.suffix == ".parquet":
        # ArcGIS tables arrive as geometry-less parquet
        import pyarrow.parquet as _pq
        names = _pq.read_schema(src).names
        is_tabular = "geometry" not in names and "geom" not in names

    # The SLDC "LRA Inventory" service layer carries every city parcel with
    # an LRA yes/no flag; the LRA inventory is the flagged subset — filter
    # the extract before conversion (plain column filter keeps WKB + geo
    # metadata intact for gpio).
    if coll_id == "lra-property":
        filtered = src.parent / "lra_filtered.parquet"
        # Rehydrate WKB to a GEOMETRY column so duckdb writes proper
        # GeoParquet metadata that gpio can read.
        # LOAD spatial so duckdb reads/writes the geometry column as GEOMETRY
        # with GeoParquet metadata (without it, geometry degrades to BLOB).
        run(["duckdb", "-c",
             "INSTALL spatial; LOAD spatial; "
             f"COPY (SELECT * FROM '{src}' WHERE LRA = 'YES') TO '{filtered}' "
             "(FORMAT PARQUET, COMPRESSION ZSTD)"])
        src = filtered

    if is_tabular:
        run(["gpio", "convert", "geoparquet", src, out,
             "--allow-no-geometry", "--skip-hilbert"])
    else:
        run(["gpio", "convert", "geoparquet", src, out])
        # gpio's parquet→parquet convert does not re-order rows; guarantee
        # Hilbert ordering explicitly (spec PTL-DAT-006).
        if src.suffix == ".parquet":
            tmp_sorted = out.parent / f".{out.stem}.sorted.parquet"
            run(["gpio", "sort", "hilbert", out, tmp_sorted])
            tmp_sorted.replace(out)
        # City shapefiles ship in MO State Plane East; normalize to WGS84
        # like the service extracts. gpio names shapefile geometry "geom" —
        # rename to "geometry" for cross-catalog consistency.
        if src.suffix == ".shp":
            tmp = out.with_suffix(".4326.parquet")
            run(["gpio", "convert", "reproject", out, tmp, "-d", "EPSG:4326"])
            tmp.replace(out)
            rename_geom(out)
        restore_stats(out)

    # Carry the extracted city renderer style along, if there is one
    city_style = STAGING / "extracts" / coll_id / "styles" / "city-renderer.json"
    if city_style.exists():
        styles_dir = out_dir / "styles"
        styles_dir.mkdir(exist_ok=True)
        shutil.copy(city_style, styles_dir / "city-renderer.json")

    n = subprocess.run(
        ["duckdb", "-noheader", "-list", "-c", f"SELECT count(*) FROM '{out}'"],
        capture_output=True, text=True,
    ).stdout.strip()
    return {"rows": int(n), "tabular": is_tabular, "source_file": str(src.relative_to(ROOT))}


def main() -> int:
    only = set(sys.argv[1:])
    failures = []
    for coll_id in SOURCES:
        if only and coll_id not in only:
            continue
        try:
            info = assemble(coll_id)
            print(f"✓ {coll_id}: {info['rows']} rows"
                  f"{' (tabular)' if info['tabular'] else ''}  ← {info['source_file']}")
        except Exception as e:  # noqa: BLE001
            failures.append(coll_id)
            print(f"✗ {coll_id}: {e}")
    if failures:
        print(f"\nFAILED: {', '.join(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
