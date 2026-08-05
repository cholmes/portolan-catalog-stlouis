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


def fetch_arcgis(coll_id: str, src: dict) -> dict:
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


def fetch_static(coll_id: str, src: dict) -> dict:
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
        result = fetch_arcgis(coll_id, src) if src["type"] == "arcgis" else fetch_static(coll_id, src)
        d = STAGING / coll_id
        d.mkdir(parents=True, exist_ok=True)
        (d / "dataset-info.json").write_text(json.dumps({
            "collection": coll_id,
            "title": src["title"],
            "portal_page": src["portal_page"],
            "department": src["department"],
            "source": src.get("service") or src.get("url"),
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
