#!/usr/bin/env python3
"""Generate PMTiles for every geo collection with bounded tile sizes.

gpio-pmtiles (what `portolan add --pmtiles` runs) passes tippecanoe
--no-tile-size-limit, which produced multi-MB tiles for the dense
collections (parcels served an 11 MB tile and browsers fell over).
This generator keeps tippecanoe's default 500 KB tile cap and lets
--drop-densest-as-needed thin features to fit; shared polygon borders
stay unsimplified so adjacent parcels/blocks don't develop slivers.

Usage: python3 tools/make_pmtiles.py [collection-id ...]   (default: all geo)
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sources import SOURCES

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"


def make(coll_id: str) -> None:
    pq = CATALOG / coll_id / f"{coll_id}.parquet"
    out = CATALOG / coll_id / f"{coll_id}.pmtiles"
    tmp = out.with_suffix(".pmtiles.tmp")
    gpio = subprocess.Popen(
        ["gpio", "convert", "geojson", str(pq)], stdout=subprocess.PIPE)
    tc = subprocess.run(
        ["tippecanoe", "-P", "-q", "-o", str(tmp), "--force",
         "-l", coll_id,
         "-Z", "0", "-z", "14",
         "--drop-densest-as-needed",
         "--no-simplification-of-shared-nodes",
         "--attribution=City of St. Louis"],
        stdin=gpio.stdout, capture_output=True, text=True)
    gpio.stdout.close()
    gpio.wait()
    if tc.returncode != 0 or gpio.returncode != 0:
        tmp.unlink(missing_ok=True)
        raise RuntimeError(f"{coll_id}: {tc.stderr[-400:]}")
    tmp.replace(out)
    mb = out.stat().st_size / 1e6
    print(f"✓ {coll_id}: {mb:.1f} MB")


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
