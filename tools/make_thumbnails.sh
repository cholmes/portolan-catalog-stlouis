#!/usr/bin/env bash
# Render thumbnail.png per collection by drawing its styles/default.json with
# chiitiler (MapLibre GL Native) over a light basemap. The spec asks that the
# thumbnail come from the default style, so this renders the real style file.
# Adapted from portolan-catalog-trimet/tools/make_thumbnails.sh (PNG-only —
# the spec's reference thumbnails are PNG; no WebP step here).
#
#   bash tools/make_thumbnails.sh [collection ...]
#
# Requires Node 20/22/24 (MapLibre GL Native ABI; not 23). Clones chiitiler
# into $CHIITILER_DIR on first run.
set -euo pipefail

# Prefer a MapLibre-Native-compatible Node if present
for NV in 24 22 20; do
    if [ -d "/opt/homebrew/opt/node@$NV/bin" ]; then
        export PATH="/opt/homebrew/opt/node@$NV/bin:$PATH"
        break
    fi
done

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CATALOG_DIR="$ROOT/catalog"
CHIITILER_DIR="${CHIITILER_DIR:-/tmp/chiitiler}"
PORT="${PORT:-13579}"
SIZE="${SIZE:-800}"
DEFAULT_BASEMAP_URL='https://basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png'
BASEMAP_URL="${BASEMAP_URL:-$DEFAULT_BASEMAP_URL}"

fsize() { stat -f%z "$1" 2>/dev/null || stat -c%s "$1"; }

if [ ! -d "$CHIITILER_DIR/node_modules" ]; then
    echo "Installing chiitiler into $CHIITILER_DIR ..."
    rm -rf "$CHIITILER_DIR"
    git clone --depth 1 https://github.com/Kanahiro/chiitiler "$CHIITILER_DIR"
    (cd "$CHIITILER_DIR" && npm install --silent)
fi

echo "Starting chiitiler on :$PORT ..."
(cd "$CHIITILER_DIR" && CHIITILER_PROCESSES=0 npx tsx src/main.ts tile-server \
    --port "$PORT" --cache memory > /tmp/chiitiler.log 2>&1) &
SERVER_PID=$!
trap 'kill $SERVER_PID 2>/dev/null || true' EXIT

for _ in $(seq 1 40); do
    if curl -sf "http://localhost:$PORT/health" >/dev/null 2>&1; then break; fi
    if curl -s "http://localhost:$PORT/" >/dev/null 2>&1; then break; fi
    sleep 1
done
if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo "ERROR: chiitiler failed to start; see /tmp/chiitiler.log" >&2
    exit 1
fi

WANTED=("$@")
COUNT=0

while IFS='|' read -r CID BBOX; do
    if [ ${#WANTED[@]} -gt 0 ]; then
        found=0
        for w in "${WANTED[@]}"; do [ "$w" = "$CID" ] && found=1 || true; done
        [ $found -eq 1 ] || continue
    fi
    DIR="$CATALOG_DIR/$CID"
    PM="$DIR/$CID.pmtiles"
    STYLE="$DIR/styles/default.json"
    [ -f "$PM" ] && [ -f "$STYLE" ] || { echo "skip $CID (missing pmtiles or style)"; continue; }

    PMTILES_PATH="$(cd "$DIR" && pwd)/$CID.pmtiles"
    RENDER="$DIR/.render-style.json"

    PMTILES_PATH="$PMTILES_PATH" BASEMAP_URL="$BASEMAP_URL" \
    STYLE="$STYLE" RENDER="$RENDER" python3 - <<'PYSTYLE'
import json, os
style = json.load(open(os.environ['STYLE']))
style['sources'] = {
    'basemap': {'type': 'raster', 'tiles': [os.environ['BASEMAP_URL']], 'tileSize': 256},
    'data': {'type': 'vector',
             'tiles': ['pmtiles://%s/{z}/{x}/{y}' % os.environ['PMTILES_PATH']]},
}
style['layers'] = [{'id': 'basemap', 'type': 'raster', 'source': 'basemap'}] + style.get('layers', [])
# chiitiler has no glyph server configured, so drop text from the render.
style['layers'] = [l for l in style['layers'] if l.get('type') != 'symbol']
json.dump(style, open(os.environ['RENDER'], 'w'))
PYSTYLE

    OUT="$DIR/thumbnail.png"
    TMP="$DIR/.thumbnail.png.tmp"
    curl -s -X POST "http://localhost:$PORT/clip.png?bbox=${BBOX}&size=${SIZE}" \
        -H "Content-Type: application/json" \
        -d "{\"style\": $(cat "$RENDER")}" -o "$TMP"
    rm -f "$RENDER"

    if [ -f "$TMP" ] && [ "$(fsize "$TMP")" -gt 5000 ]; then
        mv "$TMP" "$OUT"
        echo "  ok   $CID  ($(fsize "$OUT") bytes)"
        COUNT=$((COUNT + 1))
    else
        echo "  FAIL $CID: $(head -c 200 "$TMP" 2>/dev/null)"
        rm -f "$TMP"
    fi
done < <(CATALOG_DIR="$CATALOG_DIR" python3 - <<'PYLIST'
import json, os, pathlib

# Thumbnail framing per collection, so the cards don't all show the same
# tall skinny city sliver:
#   extent — full data extent (boundaries and city-wide continuous layers)
#   fill   — square window over the central bulk of the data ("get most of
#            it"), cropping the north/south tips
#   (w,s,e,n) — explicit detail window for layers that read best zoomed in
DETAIL = {
    "city-blocks": (-90.215, 38.615, -90.175, 38.645),   # downtown blocks
    "parcels": (-90.27, 38.60, -90.23, 38.63),           # Shaw/Tower Grove
    "streets": (-90.26, 38.62, -90.20, 38.66),           # midtown grid
}
FILL = {"historic-districts", "tif-districts", "opportunity-zones",
        "lra-property", "tax-abated-parcels", "community-improvement-districts",
        "special-business-districts", "bike-infrastructure", "parks",
        "city-trees"}

cat = pathlib.Path(os.environ["CATALOG_DIR"])
for coll in sorted(cat.iterdir()):
    cj = coll / "collection.json"
    if not cj.exists():
        continue
    c = json.loads(cj.read_text())
    cid = c["id"]
    try:
        w, s, e, n = c["extent"]["spatial"]["bbox"][0]
    except Exception:
        continue
    if cid in DETAIL:
        w, s, e, n = DETAIL[cid]
    elif cid in FILL:
        cx, cy = (w + e) / 2, (s + n) / 2
        half = max(e - w, n - s) * 0.30
        w, e, s, n = cx - half, cx + half, cy - half, cy + half
    pad = max(e - w, n - s) * 0.04
    print(f'{cid}|{w-pad:.6f},{s-pad:.6f},{e+pad:.6f},{n+pad:.6f}')
PYLIST
)

echo "Done: $COUNT thumbnails rendered as PNG"
