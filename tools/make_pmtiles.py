#!/usr/bin/env python3
"""Generate PMTiles for every geo collection with bounded tile sizes.

Three rules learned the hard way:
- Never --no-tile-size-limit (gpio-pmtiles default): parcels grew an 11 MB
  tile and browsers OOMed.
- Dense collections carry only the attributes their styles and popups need
  (parcels has ~130 columns; shipping them in every tile is what actually
  eats browser memory).
- Dense collections get a maxzoom high enough that a maxzoom tile holds a
  neighborhood, not a district — so nothing needs to be thinned away at
  maxzoom and the data is complete when zoomed in. --drop-densest-as-needed
  only bites at middle zooms, where thinning is visually invisible.

Usage: python3 tools/make_pmtiles.py [collection-id ...]   (default: all geo)
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sources import SOURCES

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"

# Per-collection tiling: maxzoom, tile byte cap, attribute allowlist
# (None = keep every attribute; fine for small collections).
DEFAULTS = {"maxzoom": 14, "cap": 500_000, "columns": None}
TILING = {
    "parcels": {
        "maxzoom": 16, "cap": 800_000,
        "columns": ["HANDLE", "ParcelId", "SITEADDR", "OWNERNAME", "AsdTotal",
                    "VacantLot", "FirstYearBuilt", "NBRHD", "WARD", "Zoning",
                    "LANDAREA"]},
    "zoning": {"maxzoom": 15, "cap": 800_000, "columns": ["LAYER"]},
    "city-trees": {
        "maxzoom": 15, "cap": 800_000,
        "columns": ["COMMON", "DBH", "CONDITION", "LOCATION_TYPE",
                    "STREET_NUM", "STREET", "ELIGIBLE"]},
    "csb-311-requests": {
        "maxzoom": 15, "cap": 800_000,
        "columns": ["REQUESTID", "GROUP", "STATUS", "CALLERTYPE",
                    "PROBADDRESS", "NEIGHBORHOOD", "WARD", "DATETIMEINIT"]},
    "city-blocks": {
        "maxzoom": 15, "cap": 800_000,
        "columns": ["Name", "BLOCK_HANDLE", "WARD10", "PRECINCT10",
                    "CensTract10", "NBRHD"]},
    "streets": {
        "maxzoom": 15, "cap": 800_000,
        "columns": ["Street_Name_Full", "Street_Name_Base", "Class",
                    "Street_Name_Pre_Directional", "Street_Name_Post_Type",
                    "Street_Name_Post_Direction"]},
    "lra-property": {
        "maxzoom": 15, "cap": 800_000,
        "columns": ["Handle", "Address", "Status", "Usage", "Property_Source",
                    "Cost", "LRA_PRICING", "SQFT", "NEIGHBORHOOD_NUM", "WARD"]},
    "lead-service-lines": {
        "maxzoom": 15, "cap": 800_000,
        "columns": ["address", "utilmaterial", "utilstatus", "custmaterial",
                    "custstatus", "utilsource", "custsource"]},
    "vacancy-composite": {"maxzoom": 15, "cap": 800_000, "columns": None},
    "land-use": {"maxzoom": 15, "cap": 800_000, "columns": None},
    "tax-abated-parcels": {
        "maxzoom": 15, "cap": 800_000,
        "columns": ["HANDLE", "SITEADDR", "AbatementStartYear",
                    "AbatementEndYear", "WARD", "NBRHD"]},
}


def make(coll_id: str) -> None:
    cfg = {**DEFAULTS, **TILING.get(coll_id, {})}
    pq = CATALOG / coll_id / f"{coll_id}.parquet"
    out = CATALOG / coll_id / f"{coll_id}.pmtiles"
    # tippecanoe picks its output format from the extension, so the temp
    # file must still end in .pmtiles (a .tmp suffix silently yields MBTiles)
    tmp = CATALOG / coll_id / f".{coll_id}.tmp.pmtiles"
    tc_cmd = ["tippecanoe", "-P", "-q", "-o", str(tmp), "--force",
              "-l", coll_id,
              "-Z", "0", "-z", str(cfg["maxzoom"]),
              f"--maximum-tile-bytes={cfg['cap']}",
              "--drop-densest-as-needed",
              "--no-simplification-of-shared-nodes",
              "--attribution=City of St. Louis"]
    for col in cfg["columns"] or []:
        tc_cmd += ["-y", col]
    gpio = subprocess.Popen(
        ["gpio", "convert", "geojson", str(pq)], stdout=subprocess.PIPE)
    tc = subprocess.run(tc_cmd, stdin=gpio.stdout, capture_output=True, text=True)
    gpio.stdout.close()
    gpio.wait()
    if tc.returncode != 0 or gpio.returncode != 0:
        tmp.unlink(missing_ok=True)
        raise RuntimeError(f"{coll_id}: {tc.stderr[-400:]}")
    tmp.replace(out)
    mb = out.stat().st_size / 1e6
    print(f"✓ {coll_id}: {mb:.1f} MB (z{cfg['maxzoom']})")


def main() -> int:
    only = set(sys.argv[1:])
    failed = []
    for coll_id in SOURCES:
        if only and coll_id not in only:
            continue
        if coll_id == "property-sales":  # tabular, no tiles
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
