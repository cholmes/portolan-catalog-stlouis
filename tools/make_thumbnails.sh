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

FRAME_LIST="$(mktemp)"
CATALOG_DIR="$CATALOG_DIR" python3 - > "$FRAME_LIST" <<'PYLIST'
import json, math, os, pathlib

# Thumbnail framing per collection so the cards do not all show the same
# tall skinny city sliver. Boundary and city-wide layers keep the full data
# extent. Subset layers get a card-shaped landscape window over the bulk of
# the data. Detail layers get a fixed close-up window. All non-extent
# windows use ASPECT so the image matches the browser card shape.
# NB: keep apostrophes and unbalanced parens out of this heredoc.
ASPECT = 1.7          # rendered width / height
COS = math.cos(math.radians(38.63))

def landscape(cx, cy, half_lat):
    half_lon = ASPECT * half_lat / COS
    return cx - half_lon, cy - half_lat, cx + half_lon, cy + half_lat

# collection -> (center_lon, center_lat, half_lat_degrees)
# The Overture places and addresses tiles only exist at z14, and buildings
# only read well close up, so those get downtown/neighborhood close-ups.
DETAIL = {
    "city-blocks": (-90.195, 38.630, 0.011),
    "parcels": (-90.2525, 38.6115, 0.0055),
    "streets": (-90.230, 38.640, 0.016),
    "tif-districts": (-90.220, 38.655, 0.035),
    "overture-buildings": (-90.1935, 38.6280, 0.0075),
    "overture-places": (-90.1990, 38.6320, 0.0060),
    "overture-addresses": (-90.2530, 38.6110, 0.0045),
    "overture-transportation": (-90.2200, 38.6350, 0.0330),
}
FILL = {"historic-districts", "opportunity-zones",
        "lra-property", "tax-abated-parcels", "community-improvement-districts",
        "special-business-districts", "bike-infrastructure", "parks",
        "city-trees", "forest-park-trees", "schools", "floodplain",
        "port-authority-district", "land-use", "lead-service-lines",
        "market-value-analysis", "vacancy-composite", "polling-places",
        "tornado-damage-2025", "flood-controls", "neighborhood-organizations",
        "siren-locations", "property-taxes", "property-sales",
        "electrical-permits", "mechanical-permits", "plumbing-permits",
        "occupancy-permits", "street-permits", "election-results-nov-2024",
        "animal-bites", "parcels-history", "crime", "historic-landmarks",
        "zip-codes", "parking-meters", "street-sweeping",
        "business-licenses", "tax-sales",
        "overture-transportation", "overture-infrastructure",
        "overture-land", "overture-land-use", "overture-water"}

cat = pathlib.Path(os.environ["CATALOG_DIR"])
for cj in sorted(cat.glob("*/*/collection.json")):
    coll = cj.parent
    c = json.loads(cj.read_text())
    cid = c["id"].split("/")[-1]
    try:
        w, s, e, n = c["extent"]["spatial"]["bbox"][0]
    except Exception:
        continue
    if cid in DETAIL:
        w, s, e, n = landscape(*DETAIL[cid])
    elif cid in FILL:
        cx, cy = (w + e) / 2, (s + n) / 2
        w, s, e, n = landscape(cx, cy, (n - s) * 0.30)
    pad = max(e - w, n - s) * 0.02
    print(f'{cid}|{w-pad:.6f},{s-pad:.6f},{e+pad:.6f},{n+pad:.6f}')
PYLIST

WANTED=("$@")
COUNT=0

while IFS='|' read -r CID BBOX; do
    if [ ${#WANTED[@]} -gt 0 ]; then
        found=0
        for w in "${WANTED[@]}"; do [ "$w" = "$CID" ] && found=1 || true; done
        [ $found -eq 1 ] || continue
    fi
    DIR="$(find "$CATALOG_DIR" -maxdepth 2 -type d -name "$CID" | head -1)"
    PM="$DIR/$CID.pmtiles"
    STYLE="$DIR/styles/default.json"
    [ -f "$STYLE" ] || { echo "skip $CID (missing style)"; continue; }
    # Overture collections have no local tiles; their style already points at
    # the remote theme archive, which chiitiler can also read.
    if [ -f "$PM" ]; then
        PMTILES_PATH="$(cd "$DIR" && pwd)/$CID.pmtiles"
    elif grep -q 'pmtiles://http' "$STYLE"; then
        PMTILES_PATH=""
    else
        echo "skip $CID (missing pmtiles)"; continue
    fi
    RENDER="$DIR/.render-style.json"

    PMTILES_PATH="$PMTILES_PATH" BASEMAP_URL="$BASEMAP_URL" \
    STYLE="$STYLE" RENDER="$RENDER" python3 - <<'PYSTYLE'
import json, os
style = json.load(open(os.environ['STYLE']))
pm = os.environ.get('PMTILES_PATH', '')
if pm:
    data = {'type': 'vector', 'tiles': ['pmtiles://%s/{z}/{x}/{y}' % pm]}
else:
    # Remote Overture archive: keep its URL, but as a tiles template with an
    # explicit maxzoom so overzoomed close-ups still fetch the deepest tiles.
    url = style['sources']['data']['url'][len('pmtiles://'):]
    data = {'type': 'vector', 'tiles': ['pmtiles://%s/{z}/{x}/{y}' % url]}
    theme = url.rsplit('/', 1)[-1].split('.')[0]
    data['maxzoom'] = {'addresses': 14, 'base': 13, 'buildings': 14,
                      'divisions': 12, 'places': 14,
                      'transportation': 14}.get(theme, 14)
style['sources'] = {
    'basemap': {'type': 'raster', 'tiles': [os.environ['BASEMAP_URL']], 'tileSize': 256},
    'data': data,
}
style['layers'] = [{'id': 'basemap', 'type': 'raster', 'source': 'basemap'}] + style.get('layers', [])
# Labels need a glyph source. Styles that name one keep their text; for any
# that do not, drop the symbol layers rather than have them render blank.
if not style.get('glyphs'):
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
done < "$FRAME_LIST"
rm -f "$FRAME_LIST"


echo "Done: $COUNT thumbnails rendered as PNG"
