#!/usr/bin/env python3
"""Extract St. Louis subsets of Overture Maps themes into staging/extracts/.

Each Overture collection is a bbox extract (the city-boundary collection's
bounds — the rectangle keeps the Illinois shore for context, matching how the
thumbnails frame the city) pulled straight from Overture's release bucket
with DuckDB, using the bbox covering column so only intersecting row groups
travel. Multi-type collections (buildings + building_part, segment +
connector, the three divisions types) are merged UNION ALL BY NAME with an
`overture_type` column, the same pattern as the multi-layer ArcGIS merges'
`source_layer`.

Overture's own `bbox` covering column is dropped here: gpio rebuilds a
GeoParquet 1.1 covering with row-group stats during assembly, and two
same-named covering columns would collide.

Usage: python3 tools/fetch_overture.py [collection-id ...]   (default: all
overture collections). Normally invoked via tools/fetch.py.
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sources import OVERTURE_S3, SOURCES

ROOT = Path(__file__).resolve().parent.parent
STAGING = ROOT / "staging"

# The city-boundary collection's bbox — the catalog's own extent.
BBOX = (-90.32051856117901, 38.53199630293254,
        -90.16630892212817, 38.77434671879855)


def type_select(theme: str, otype: str, tag: bool) -> str:
    path = f"{OVERTURE_S3}/theme={theme}/type={otype}/*.parquet"
    extra = f", '{otype}' AS overture_type" if tag else ""
    box = f"ST_MakeEnvelope({BBOX[0]}, {BBOX[1]}, {BBOX[2]}, {BBOX[3]})"
    # With spatial loaded, DuckDB reads the GeoParquet geometry column as
    # GEOMETRY directly — no WKB rehydration needed. Geometries crossing the
    # edge of the box are clipped to it: without the clip, any feature whose
    # bbox merely touches the box arrives whole — the full USA polygon via
    # divisions, continental WorldCover polygons via land_cover — dragging
    # the collection's extent across the hemisphere.
    return (
        f"SELECT * FROM ("
        f"SELECT * EXCLUDE (bbox, geometry){extra}, "
        f"CASE WHEN ST_Within(geometry, {box}) THEN geometry "
        f"ELSE ST_Intersection(geometry, {box}) END AS geometry "
        f"FROM read_parquet('{path}', hive_partitioning=0) "
        f"WHERE bbox.xmin < {BBOX[2]} AND bbox.xmax > {BBOX[0]} "
        f"AND bbox.ymin < {BBOX[3]} AND bbox.ymax > {BBOX[1]}"
        f") WHERE NOT ST_IsEmpty(geometry)"
    )


def fetch_overture(coll_id: str, src: dict) -> dict:
    out_dir = STAGING / "extracts" / coll_id
    if out_dir.exists():
        import shutil
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    out = out_dir / f"{coll_id}.parquet"
    tag = len(src["types"]) > 1
    selects = " UNION ALL BY NAME ".join(
        type_select(src["theme"], t, tag) for t in src["types"])
    sql = (
        "INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs; "
        "SET s3_region='us-west-2'; "
        f"COPY ({selects}) TO '{out}' "
        "(FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 20000)"
    )
    print(f"→ {coll_id}: extracting theme={src['theme']} "
          f"types={','.join(src['types'])}")
    proc = subprocess.run(["duckdb", "-c", sql], capture_output=True, text=True)
    if proc.returncode != 0:
        return {"status": "failed", "error": proc.stderr[-500:]}
    n = subprocess.run(
        ["duckdb", "-csv", "-noheader", "-c", f"SELECT count(*) FROM '{out}'"],
        capture_output=True, text=True).stdout.strip()
    return {"status": "ok", "rows": int(n),
            "parquets": [str(out.relative_to(ROOT))]}


def main() -> int:
    only = set(sys.argv[1:])
    failures = []
    for coll_id, src in SOURCES.items():
        if src["type"] != "overture" or (only and coll_id not in only):
            continue
        info = fetch_overture(coll_id, src)
        ok = info["status"] == "ok"
        print(f"  {'✓' if ok else '✗'} {coll_id}: "
              f"{info.get('rows', info.get('error'))}")
        if not ok:
            failures.append(coll_id)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
