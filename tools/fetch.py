#!/usr/bin/env python3
"""Fetch all sources into staging/.

ArcGIS sources: `portolan extract arcgis --raw` into staging/extracts/<id>/,
also pulling the layer's ESRI renderer as the city's own style and the layer
metadata JSON. Static sources: downloaded into staging/<id>/data/.

Writes staging/<id>/dataset-info.json (provenance record) and
staging/synced.txt (the sync timestamp stamped into collection `updated`).

Usage: python3 tools/fetch.py [collection-id ...]   (default: all)
"""

import hashlib
import json
import shutil
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sources import SOURCES

ROOT = Path(__file__).resolve().parent.parent
STAGING = ROOT / "staging"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_json(url: str):
    with urllib.request.urlopen(url + ("&" if "?" in url else "?") + "f=json", timeout=60) as r:
        return json.load(r)


def fetch_arcgis_table(coll_id: str, src: dict) -> dict:
    """Page an ArcGIS table (no geometry) into staging as JSONL.

    `portolan extract arcgis` only handles spatial layers; election vote
    totals live in a FeatureServer *table*.
    """
    out = STAGING / "extracts" / coll_id
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    base = f"{src['service'].rstrip('/')}/{src.get('table_layer', 0)}/query"
    rows, offset = [], 0
    while True:
        url = (f"{base}?where=1%3D1&outFields=*&returnGeometry=false"
               f"&resultOffset={offset}&resultRecordCount=2000&f=json")
        data = json.load(urllib.request.urlopen(url, timeout=120))
        feats = data.get("features", [])
        rows += [f["attributes"] for f in feats]
        if not data.get("exceededTransferLimit") and len(feats) < 2000:
            break
        offset += len(feats)
    jl = out / f"{coll_id}.jsonl"
    with open(jl, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    pq = out / f"{coll_id}.parquet"
    subprocess.run(["duckdb", "-c",
                    f"COPY (SELECT * FROM read_json_auto('{jl}')) TO '{pq}' "
                    "(FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 20000)"],
                   check=True, capture_output=True)
    return {"status": "ok", "rows": len(rows),
            "parquets": [str(pq.relative_to(ROOT))]}


def fetch_arcgis(coll_id: str, src: dict) -> dict:
    if src.get("table"):
        return fetch_arcgis_table(coll_id, src)
    out = STAGING / "extracts" / coll_id
    if out.exists():
        shutil.rmtree(out)
    cmd = ["portolan", "extract", "arcgis", src["service"], str(out), "--raw"]
    if src.get("layers"):
        cmd += ["--layers", src["layers"]]
    print(f"→ {coll_id}: extracting {src['service']}")
    proc = subprocess.run(cmd, input="y\n", capture_output=True, text=True)
    if proc.returncode != 0:
        return {"status": "failed", "error": proc.stdout[-500:] + proc.stderr[-500:]}

    parquets = sorted(out.rglob("*.parquet"))
    if not parquets:
        return {"status": "failed", "error": "no parquet produced"}

    # Layer metadata + renderer style, straight from the service
    info: dict = {"status": "ok", "parquets": [str(p.relative_to(ROOT)) for p in parquets]}
    try:
        svc = fetch_json(src["service"])
        layers = svc.get("layers", [])
        want = src.get("layers")
        match = [
            l for l in layers
            if want is None or l["name"] == want
        ] or layers[:1]
        if match:
            layer_url = f"{src['service'].rstrip('/')}/{match[0]['id']}"
            layer_json = fetch_json(layer_url)
            (out / "layer-metadata.json").write_text(json.dumps(layer_json, indent=1))
            info["layer_url"] = layer_url
            info["layer_description"] = layer_json.get("description") or None
            info["fields"] = [
                {"name": f["name"], "alias": f.get("alias"), "type": f.get("type")}
                for f in layer_json.get("fields", [])
            ]
            from portolan_cli.extract.common.styles import extract_esri_style
            style = extract_esri_style(
                layer_url=layer_url, collection_path=out, source_layer=coll_id,
                style_name="city-renderer",
            )
            if style:
                info["city_style"] = str(style.path.relative_to(ROOT))
    except Exception as e:  # noqa: BLE001 — provenance capture is best-effort
        info["metadata_warning"] = str(e)
    return info


def fetch_crime(coll_id: str, src: dict) -> dict:
    """Scrape slmpd.org for the NIBRS CSV links and download them all."""
    data_dir = STAGING / coll_id / "data" / "csv"
    data_dir.mkdir(parents=True, exist_ok=True)
    import re
    # slmpd.org 403s the default urllib user-agent
    ua = {"User-Agent": "Mozilla/5.0 (Macintosh) AppleWebKit/537.36"}

    def get(url):
        return urllib.request.urlopen(
            urllib.request.Request(url, headers=ua), timeout=120).read()

    page = get(src["url"]).decode("utf8", "ignore")
    urls = sorted(set(re.findall(r'href="(https?://[^"]+\.csv[^"]*)"', page)))
    got = 0
    for u in urls:
        name = u.rsplit("/", 1)[-1]
        try:
            (data_dir / name).write_bytes(get(u))
            got += 1
        except Exception as e:  # noqa: BLE001
            print(f"    ⚠ {name}: {e}")
    return {"status": "ok" if got else "failed", "files": got, "urls": len(urls)}


def fetch_static(coll_id: str, src: dict) -> dict:
    if src.get("crime_scrape"):
        return fetch_crime(coll_id, src)
    if src.get("urls"):
        data_dir = STAGING / coll_id / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        infos = []
        for u in src["urls"]:
            fname = u.rsplit("/", 1)[-1]
            dest = data_dir / fname
            print(f"→ {coll_id}: downloading {u}")
            try:
                urllib.request.urlretrieve(u, dest)
            except Exception as e:  # noqa: BLE001
                return {"status": "failed", "error": f"{fname}: {e}"}
            if fname.endswith(".zip"):
                shutil.unpack_archive(dest, data_dir / fname[:-4])
            infos.append(fname)
        return {"status": "ok", "files": infos}
    data_dir = STAGING / coll_id / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    fname = src["url"].rsplit("/", 1)[-1]
    dest = data_dir / fname
    print(f"→ {coll_id}: downloading {src['url']}")
    try:
        urllib.request.urlretrieve(src["url"], dest)
    except Exception as e:  # noqa: BLE001
        return {"status": "failed", "error": str(e)}
    info = {"status": "ok", "file": fname, "sha256": sha256(dest), "bytes": dest.stat().st_size}
    if fname.endswith(".zip"):
        shutil.unpack_archive(dest, data_dir / fname[:-4])
        info["unpacked"] = sorted(p.name for p in (data_dir / fname[:-4]).rglob("*") if p.is_file())[:20]
    return info


def main() -> int:
    only = set(sys.argv[1:])
    synced = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    failures = []
    for coll_id, src in SOURCES.items():
        if only and coll_id not in only:
            continue
        try:
            if src["type"] == "arcgis":
                result = fetch_arcgis(coll_id, src)
            elif src["type"] == "overture":
                from fetch_overture import fetch_overture
                result = fetch_overture(coll_id, src)
            else:
                result = fetch_static(coll_id, src)
        except Exception as e:  # noqa: BLE001
            result = {"status": "failed", "error": str(e)[:300]}
        d = STAGING / coll_id
        d.mkdir(parents=True, exist_ok=True)
        (d / "dataset-info.json").write_text(json.dumps({
            "collection": coll_id,
            "title": src["title"],
            "portal_page": src.get("portal_page") or src.get("docs"),
            "department": src.get("department", "Overture Maps Foundation"),
            "source": src.get("service") or src.get("url")
                      or src.get("theme") and f"Overture theme={src['theme']}",
            "source_type": src["type"],
            "synced": synced,
            "fetch": result,
        }, indent=1) + "\n")
        status = result["status"]
        print(f"  {'✓' if status == 'ok' else '✗'} {coll_id}: {status}")
        if status != "ok":
            failures.append((coll_id, result.get("error", "")[:200]))
    (STAGING / "synced.txt").write_text(synced + "\n")
    if failures:
        print("\nFAILURES:")
        for cid, err in failures:
            print(f"  {cid}: {err}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
