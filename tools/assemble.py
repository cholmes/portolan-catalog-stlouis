#!/usr/bin/env python3
"""Assemble catalog/<id>/<id>.parquet from staged sources.

Every output is rewritten with ogr2ogr to spec-conformant GeoParquet:
zstd compression, covering bbox column with stats, Hilbert row order,
row groups well under the 150k limit. Tabular sources (no geometry) get
plain zstd Parquet. City renderer styles extracted from ArcGIS are copied
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
TAB_LCO = ["-lco", "COMPRESSION=ZSTD", "-lco", "ROW_GROUP_SIZE=20000"]


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
    hits = sorted((STAGING / "extracts" / coll_id).rglob("*.parquet"))
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
    lco = TAB_LCO if is_tabular else GEO_LCO
    cmd = ["ogr2ogr", "-f", "Parquet", out, src, "-nln", coll_id] + lco
    # The SLDC "LRA Inventory" service layer carries every city parcel with an
    # LRA yes/no flag; the LRA inventory is the flagged subset.
    if coll_id == "lra-property":
        cmd += ["-where", "LRA = 'YES'"]
    if src.suffix == ".csv":
        cmd += ["-oo", "AUTODETECT_TYPE=YES", "-oo", "EMPTY_STRING_AS_NULL=YES"]
    run(cmd)
    if not is_tabular:
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
