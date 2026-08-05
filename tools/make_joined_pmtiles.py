#!/usr/bin/env python3
"""Materialize join-derived PMTiles for tabular collections.

The catalog keeps parcel/precinct-joinable datasets as plain (non-geo)
Parquet — exactly what the source publishes — but each ships a PMTiles
visual built by actually performing the documented join, so the map shows
the data without anyone having to run the join themselves. AGENTS.md in
each collection spells out the same join for reproducing a GeoParquet /
GeoPackage / Shapefile.

Join modes:
  rows      — one feature per table row, geometry from the joined collection
  summary   — one feature per geometry, carrying per-geometry attributes
              that repeat across rows (e.g. precinct turnout)
  aggregate — one feature per geometry with a computed row count

Usage: python3 tools/make_joined_pmtiles.py [collection-id ...]
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"
SCRATCH = ROOT / "staging" / "joined"

PERMIT_SELECT = ("t.HANDLE, t.APPTYPE, t.APPDESCRIPTION, "
                 "TRY_CAST(substr(t.ISSUEDATE, 1, 4) AS INT) AS PERMIT_YEAR, "
                 "TRY_CAST(t.ESTPROJECTCOST AS DOUBLE) AS ESTPROJECTCOST")

JOINS = {
    "property-taxes": dict(
        mode="rows", right="parcels", dedupe_key="ParcelId",
        on="t.AsrParcelId = p.ParcelId",
        select="t.AsrParcelId, t.AsdTotal, t.AsdLand, t.AsdImprove, "
               "t.BillYear, t.OwnerName"),
    "property-sales": dict(
        mode="rows", right="parcels", dedupe_key="ParcelId",
        on="t.AsrParcelId = p.ParcelId",
        select="t.AsrParcelId, t.SalePrice, t.SaleTypeDescr, "
               "TRY_CAST(substr(strptime(t.SaleDate, '%m/%d/%y %H:%M:%S')::VARCHAR, 1, 4) AS INT) AS SALE_YEAR"),
    "electrical-permits": dict(mode="rows", right="parcels", dedupe_key="HANDLE",
                               on="t.HANDLE = p.HANDLE", select=PERMIT_SELECT),
    "mechanical-permits": dict(mode="rows", right="parcels", dedupe_key="HANDLE",
                               on="t.HANDLE = p.HANDLE", select=PERMIT_SELECT),
    "plumbing-permits": dict(mode="rows", right="parcels", dedupe_key="HANDLE",
                             on="t.HANDLE = p.HANDLE", select=PERMIT_SELECT),
    "occupancy-permits": dict(mode="rows", right="parcels", dedupe_key="HANDLE",
                              on="t.HANDLE = p.HANDLE", select=PERMIT_SELECT),
    "street-permits": dict(
        mode="aggregate", right="neighborhoods",
        on="t.NEIGHBORHOOD = p.NHD_NAME",
        select="p.NHD_NAME, count(*) AS n_permits"),
    "election-results-nov-2024": dict(
        mode="summary", right="election-precincts",
        on="TRY_CAST(regexp_extract(t.F_Precinct, 'Ward (\\d+)', 1) AS INT) = "
           "TRY_CAST(regexp_extract(p.name, 'W (\\d+) P', 1) AS INT) AND "
           "TRY_CAST(regexp_extract(t.F_Precinct, 'Precinct (\\d+)', 1) AS INT) = "
           "TRY_CAST(regexp_extract(p.name, 'P (\\d+)', 1) AS INT)",
        select="p.name, any_value(t.Registered_Voters) AS Registered_Voters, "
               "any_value(t.Ballots_Cast) AS Ballots_Cast, "
               "TRY_CAST(any_value(t.Turnout_Percentage) AS DOUBLE) AS Turnout_Percentage",
        group="p.name, p.geometry"),
}


def make(coll_id: str) -> None:
    spec = JOINS[coll_id]
    left = CATALOG / coll_id / f"{coll_id}.parquet"
    right = CATALOG / spec["right"] / f"{spec['right']}.parquet"
    SCRATCH.mkdir(parents=True, exist_ok=True)
    joined = SCRATCH / f"{coll_id}-joined.parquet"

    if spec["mode"] == "rows":
        # Parcels can repeat a join key (condo/sub-account rows share a
        # HANDLE) — dedupe to one geometry per key so the join cannot fan out.
        dk = spec.get("dedupe_key")
        right_rel = (f"(SELECT {dk}, any_value(geometry) AS geometry "
                     f"FROM '{right}' GROUP BY {dk})" if dk else f"'{right}'")
        sql = (f"SELECT {spec['select']}, p.geometry FROM '{left}' t "
               f"JOIN {right_rel} p ON {spec['on']}")
    elif spec["mode"] == "aggregate":
        sql = (f"SELECT {spec['select']}, p.geometry FROM '{left}' t "
               f"JOIN '{right}' p ON {spec['on']} "
               f"GROUP BY p.NHD_NAME, p.geometry")
    else:  # summary
        sql = (f"SELECT {spec['select']}, p.geometry FROM '{left}' t "
               f"JOIN '{right}' p ON {spec['on']} GROUP BY {spec['group']}")

    run = subprocess.run(
        ["duckdb", "-c",
         f"INSTALL spatial; LOAD spatial; COPY ({sql}) TO '{joined}' "
         "(FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 20000)"],
        capture_output=True, text=True)
    if run.returncode != 0:
        raise RuntimeError(f"{coll_id} join: {run.stderr[-400:]}")

    counts = subprocess.run(
        ["duckdb", "-noheader", "-list", "-c",
         f"SELECT count(*) FROM '{joined}'"], capture_output=True, text=True)
    n_joined = int(counts.stdout.strip())
    n_left = int(subprocess.run(
        ["duckdb", "-noheader", "-list", "-c",
         f"SELECT count(*) FROM '{left}'"],
        capture_output=True, text=True).stdout.strip())

    out = CATALOG / coll_id / f"{coll_id}.pmtiles"
    tmp = CATALOG / coll_id / f".{coll_id}.tmp.pmtiles"
    gpio = subprocess.Popen(["gpio", "convert", "geojson", str(joined)],
                            stdout=subprocess.PIPE)
    tc = subprocess.run(
        ["tippecanoe", "-P", "-q", "-o", str(tmp), "--force", "-l", coll_id,
         "-Z", "0", "-z", "15", "--maximum-tile-bytes=800000",
         "--drop-densest-as-needed", "--no-simplification-of-shared-nodes",
         "--attribution=City of St. Louis"],
        stdin=gpio.stdout, capture_output=True, text=True)
    gpio.stdout.close()
    gpio.wait()
    if tc.returncode != 0 or gpio.returncode != 0:
        tmp.unlink(missing_ok=True)
        raise RuntimeError(f"{coll_id} tiles: {tc.stderr[-400:]}")
    tmp.replace(out)
    print(f"✓ {coll_id}: {n_joined}/{n_left} rows joined → "
          f"{out.stat().st_size/1e6:.1f} MB")


def main() -> int:
    only = set(sys.argv[1:])
    failed = []
    for coll_id in JOINS:
        if only and coll_id not in only:
            continue
        try:
            make(coll_id)
        except Exception as e:  # noqa: BLE001
            failed.append(coll_id)
            print(f"✗ {coll_id}: {e}")
    if failed:
        print("FAILED:", ", ".join(failed))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
