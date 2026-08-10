#!/usr/bin/env python3
"""Record size + sha256 for the city's own source files.

Every `source`-role asset points at a file on stlouis-mo.gov that this repo
does not host, but the Portolan spec still wants `file:size` and
`file:checksum` on it — and requires that they match the bytes the href
resolves to. So the numbers have to come from the real upstream file, never
from a guess.

Bytes are streamed and discarded; only the size and digest are kept, in
`sources/source_checksums.json`. That matters for parcels-history alone,
whose five era zips are half a gigabyte we have no reason to keep twice.

    python3 tools/fetch_source_meta.py                 # fill in what's missing
    python3 tools/fetch_source_meta.py --refresh       # re-hash everything
    python3 tools/fetch_source_meta.py wards ...       # only these collections
    python3 tools/fetch_source_meta.py --retries 12    # ride out a flaky host

The digests pin what the city served at the sync time recorded in each
collection's `updated`. When the city republishes a file, its digest changes
and this needs re-running — which is exactly the signal that the mirror is
behind.
"""

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sources import SOURCE_FILES, source_files

ROOT = Path(__file__).resolve().parent.parent
SIDECAR = ROOT / "sources" / "source_checksums.json"

# stlouis-mo.gov is fine with the default urllib agent; slmpd.org 403s it.
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) AppleWebKit/537.36"}
CRIME_INDEX = "https://www.slmpd.org/crime_stats.shtml"


def multihash(sha256_hex: str) -> str:
    """sha2-256 multihash: 0x12 code, 0x20 length, then the digest."""
    return "1220" + sha256_hex


def hash_url(url: str) -> tuple:
    """Stream a URL, returning (size, sha256hex). The bytes are discarded.

    A connection that drops mid-transfer looks exactly like a clean EOF to
    `read()`, so a truncated download would otherwise be recorded as a
    perfectly valid checksum of the wrong bytes — the worst possible outcome
    for a field whose whole job is to prove what the city served. Where the
    server declares a length, hold it to it.
    """
    h = hashlib.sha256()
    size = 0
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=300) as r:
        declared = r.headers.get("Content-Length")
        encoded = r.headers.get("Content-Encoding")
        while chunk := r.read(1 << 20):
            h.update(chunk)
            size += len(chunk)
    # A declared length describes the encoded body, so it is only comparable
    # when the body came through as-is.
    if declared is not None and not encoded and size != int(declared):
        raise OSError(
            f"truncated: read {size:,} bytes, Content-Length said {int(declared):,}")
    return size, h.hexdigest()


# Note: `staging/<id>/dataset-info.json` already holds a sha256 for most of
# these, and reusing it would save a gigabyte of transfer. Don't. That digest
# describes the bytes the city served at sync time, while `file:checksum` has
# to match the bytes the href resolves to *now* — and the city quietly
# republishes. Reusing the staged value shipped two checksums that rashid
# immediately caught as wrong (property-sales, parcels-history). Hashing the
# live file is the only value that can be true.


MONTHS = ["january", "february", "march", "april", "may", "june", "july",
          "august", "september", "october", "november", "december"]


def crime_label(filename: str) -> tuple:
    """(asset key, human title) for one SLMPD file.

    SLMPD names these inconsistently — `May2025.csv`, but also
    `Downloadable-NIBRS-Crime-File-April-2024-CSV.csv` and a `2021-2023.csv`
    backfile. Keys are normalized to `source-YYYY-MM` so they sort by period
    rather than by the department's filing habits.
    """
    stem = filename.removesuffix(".csv")
    low = stem.lower()
    year = re.search(r"(20\d\d)", stem)
    month = next((i for i, m in enumerate(MONTHS, 1) if m in low), None)
    if year and month:
        y = year.group(1)
        return (f"source-{y}-{month:02d}",
                f"SLMPD NIBRS crime incidents — {MONTHS[month - 1].title()} {y}")
    span = re.fullmatch(r"(20\d\d)-(20\d\d)", stem)
    if span:
        return (f"source-{span.group(1)}-{span.group(2)}",
                f"SLMPD NIBRS crime incidents — {span.group(1)}–{span.group(2)}")
    return (f"source-{re.sub(r'[^a-z0-9]+', '-', low).strip('-')}",
            f"SLMPD NIBRS crime incidents — {stem}")


def crime_entries() -> list:
    """SLMPD posts one NIBRS CSV per month; mirror whatever is up there now."""
    req = urllib.request.Request(CRIME_INDEX, headers=UA)
    page = urllib.request.urlopen(req, timeout=120).read().decode("utf8", "ignore")
    urls = sorted(set(re.findall(r'href="(https?://[^"]+\.csv[^"]*)"', page)))
    out = []
    for u in urls:
        key, title = crime_label(u.rsplit("/", 1)[-1])
        out.append({"key": key, "url": u, "title": title,
                    "type": "text/csv", "primary": True})
    return sorted(out, key=lambda e: e["key"])


def entries_for(coll_id: str) -> list:
    if SOURCE_FILES.get(coll_id) == "scrape":
        return crime_entries()
    return source_files(coll_id)


def load() -> dict:
    return json.loads(SIDECAR.read_text())["collections"] if SIDECAR.exists() else {}


def save(collections: dict) -> None:
    SIDECAR.parent.mkdir(exist_ok=True)
    SIDECAR.write_text(json.dumps({
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "note": "Size and sha2-256 multihash of the City of St. Louis source "
                "files each collection mirrors, as served at the time above. "
                "Written by tools/fetch_source_meta.py; consumed by "
                "tools/finalize_stac.py to emit `source`-role assets.",
        "collections": collections,
    }, indent=2) + "\n")
    n = sum(len(v) for v in collections.values())
    print(f"\n✓ {SIDECAR.relative_to(ROOT)}: {n} source files "
          f"across {len(collections)} collections")


def incomplete(coll_ids: list) -> dict:
    """{collection: how many of its source files still have no digest}."""
    have = load()
    out = {}
    for cid in coll_ids:
        if cid not in SOURCE_FILES:
            continue
        # A scraped list can't be counted without hitting the network again;
        # treat an empty result as the only failure worth reporting.
        want = len(SOURCE_FILES[cid]) if SOURCE_FILES[cid] != "scrape" else 1
        got = len(have.get(cid, []))
        if got < want:
            out[cid] = want - got
    return out


def one_pass(todo: list, refresh: bool) -> None:
    prev = load()
    out = dict(prev)
    for coll_id in todo:
        if coll_id not in SOURCE_FILES:
            continue
        try:
            entries = entries_for(coll_id)
        except Exception as e:  # noqa: BLE001
            print(f"✗ {coll_id}: listing failed: {e}")
            continue
        done = {} if refresh else {e["url"]: e for e in prev.get(coll_id, [])}

        def resolve(e):
            cached = done.get(e["url"])
            if cached and cached.get("checksum"):
                return {**e, "size": cached["size"], "checksum": cached["checksum"]}
            try:
                size, sha = hash_url(e["url"])
            except Exception as ex:  # noqa: BLE001
                print(f"    ⚠ {e['key']}: {ex}")
                return None
            print(f"    ✓ {e['key']:26s} {size:>12,} B")
            return {**e, "size": size, "checksum": multihash(sha)}

        print(f"→ {coll_id} ({len(entries)} file{'s' if len(entries) != 1 else ''})")
        with ThreadPoolExecutor(4) as ex:
            out[coll_id] = [r for r in ex.map(resolve, entries) if r]
        save(out)  # durable after every collection, not just at the end


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("collections", nargs="*", help="default: all")
    ap.add_argument("--refresh", action="store_true",
                    help="re-hash even entries already in the sidecar")
    # stlouis-mo.gov drops TLS connections under sustained load — the same URL
    # will 200 one minute and fail to handshake the next. Nothing to do but
    # come back later, so the tool does that itself rather than needing a
    # person to babysit it.
    ap.add_argument("--retries", type=int, default=0,
                    help="passes to make over anything still missing")
    ap.add_argument("--retry-wait", type=int, default=300,
                    help="seconds between passes (default 300)")
    args = ap.parse_args()

    todo = args.collections or list(SOURCE_FILES)
    for coll_id in todo:
        if coll_id not in SOURCE_FILES:
            print(f"✗ {coll_id}: not in SOURCE_FILES")

    refresh = args.refresh
    for attempt in range(args.retries + 1):
        if attempt:
            missing = incomplete(todo)
            if not missing:
                break
            print(f"\n… {sum(missing.values())} file(s) still missing in "
                  f"{len(missing)} collection(s); waiting {args.retry_wait}s")
            time.sleep(args.retry_wait)
            todo = list(missing)
        one_pass(todo, refresh)
        refresh = False  # a refresh is for the first pass only

    left = incomplete(todo)
    if left:
        print("\n⚠ still missing: "
              + ", ".join(f"{c} ({n})" for c, n in sorted(left.items())))


if __name__ == "__main__":
    main()
