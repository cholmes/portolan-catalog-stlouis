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

import json
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

    # 311 requests carry Web-Mercator SRX/SRY columns — promote to points
    if coll_id == "csb-311-requests":
        cmd = ["ogr2ogr", "-f", "Parquet", out, src, "-nln", coll_id,
               "-oo", "X_POSSIBLE_NAMES=SRX", "-oo", "Y_POSSIBLE_NAMES=SRY",
               "-oo", "AUTODETECT_TYPE=YES", "-oo", "EMPTY_STRING_AS_NULL=YES",
               "-a_srs", "EPSG:3857"] + GEO_LCO
        run(cmd)
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
