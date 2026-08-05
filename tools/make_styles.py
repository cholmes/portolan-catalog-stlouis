#!/usr/bin/env python3
"""Generate MapLibre styles for every geo collection.

Each collection gets 3-5 styles: a default, data-driven variants surfacing
the attributes found in profiling (docs/data-profile.json), and — where the
city's ArcGIS renderer was extracted — the city's own cartography. Style
choices are documented per style in metadata.description.

Legend rule: portolan-browser derives a legend from the FIRST `fill` layer's
`fill-color` expression (match/step only — never line-color/circle-color, and
never interpolate). Every data-driven style therefore leads with an inert
legend layer: a fill with the classification expression and fill-opacity 0.
Constant-color styles carry no legend (nothing to classify). Same workaround
as portolan-catalog-trimet and portolan-nl (portolan-browser#13).

Zoning district names come from the city's own ArcGIS renderer labels; street
class codes are left as codes (the source does not decode them).
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sources import coll_rel

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"

# City palette, sampled from stlouis-mo.gov
BLUE = "#1e526b"
DARK = "#174054"
RED = "#c03221"
GREEN = "#538400"
LIGHTBLUE = "#a8d4e8"
ORANGE = "#e89d07"
INK = "#1A1A1A"
GRAY = "#9aa3a8"
LIGHT = "#dfe6ea"

# Categorical ramp anchored on the city palette
CAT = [BLUE, RED, GREEN, ORANGE, "#7c5295", "#4a9d9c", "#b5651d", "#8b3a62",
       LIGHTBLUE, "#6b7f2a", "#c98bab", "#585f63"]

# Distinct-fill palette for adjacent polygons (repeating sets): mid-saturation
# so white boundaries and labels stay readable.
POLY = ["#7fb3d0", "#e2a76f", "#95c68f", "#d98d8d", "#a99bd0",
        "#c9b970", "#8fc6c0", "#d093b5", "#b0a377", "#9cb0e0",
        "#e0b394", "#88b8a3", "#c99ac0", "#adc487"]

# Bolder, saturated palette (wards) so wards and precincts read differently.
BOLD = ["#1e6f9c", "#c0392b", "#1e8449", "#d68910", "#6c3483",
        "#148f77", "#a04000", "#884ea0", "#2874a6", "#7d8f2f",
        "#b03a5b", "#3b6f43", "#b7752c", "#4a5d8f"]


def repeat_fill(prop_num_expr, n=10):
    """Repeating color sets keyed on a numeric expression modulo n."""
    expr = ["match", ["%", prop_num_expr, n]]
    for i in range(n):
        expr += [i, POLY[i % len(POLY)]]
    expr.append(GRAY)
    return expr


def match(prop, mapping, fallback=GRAY):
    expr = ["match", ["get", prop]]
    for k, v in mapping.items():
        expr += [k, v]
    expr.append(fallback)
    return expr


def step(prop, base, stops, to_number=False):
    """stops: flat [threshold, color, ...] applied at >= threshold."""
    inp = ["to-number", ["get", prop]] if to_number else ["get", prop]
    expr = ["step", inp, base]
    for i in range(0, len(stops), 2):
        expr += [stops[i], stops[i + 1]]
    return expr


def style(coll_id, name, description, layers, legend=None, no_legend=False):
    """no_legend marks styles whose colors are deliberately arbitrary
    (repeating sets to tell neighbors apart) — nothing to put in a legend."""
    if legend is not None:
        layers = [{
            "id": f"{coll_id}-legend",
            "type": "fill",
            "source": "data",
            "source-layer": coll_id,
            "paint": {"fill-color": legend, "fill-opacity": 0},
        }] + layers
    meta = {"description": description}
    if no_legend:
        meta["legend"] = "none"
    return {
        "version": 8,
        "name": name,
        "metadata": meta,
        "sources": {"data": {"type": "vector",
                             "url": f"pmtiles://../{coll_id}.pmtiles"}},
        "layers": layers,
    }


def fill(coll_id, color, opacity=0.55, outline=INK, lid="fill"):
    return {"id": lid, "type": "fill", "source": "data", "source-layer": coll_id,
            "paint": {"fill-color": color, "fill-opacity": opacity,
                      "fill-outline-color": outline}}


def line(coll_id, color, width=1.5, lid="line", dash=None, opacity=1.0):
    paint = {"line-color": color, "line-width": width, "line-opacity": opacity}
    if dash:
        paint["line-dasharray"] = dash
    return {"id": lid, "type": "line", "source": "data", "source-layer": coll_id,
            "paint": paint}


def circle(coll_id, color, radius=3, lid="circle", opacity=0.85, stroke=None):
    paint = {"circle-color": color, "circle-radius": radius,
             "circle-opacity": opacity}
    if stroke:
        paint["circle-stroke-color"] = stroke
        paint["circle-stroke-width"] = 0.5
    return {"id": lid, "type": "circle", "source": "data",
            "source-layer": coll_id, "paint": paint}


def label(coll_id, prop, size=11, minzoom=10):
    return {"id": "labels", "type": "symbol", "source": "data",
            "source-layer": coll_id, "minzoom": minzoom,
            "layout": {"text-field": ["get", prop],
                       "text-font": ["Noto Sans Regular"],
                       "text-size": size, "text-max-width": 9},
            "paint": {"text-color": INK, "text-halo-color": "#FFFFFF",
                      "text-halo-width": 1.2}}


def zoom_radius(base):
    return ["interpolate", ["linear"], ["zoom"],
            10, base * 0.4, 13, base, 16, base * 2.2]


STYLES = {}  # coll_id -> {filename(no .json): (style_obj, is_default)}


def emit(coll_id, filename, obj, default=False):
    STYLES.setdefault(coll_id, {})[filename] = (obj, default)


# --------------------------------------------------------------------------
# parcels — 134,362 polygons; assessed value, vacancy, year built
# --------------------------------------------------------------------------
ASD = step("AsdTotal", "#eef3f6",
           [1600, "#c6dbe8", 7700, "#8fbdd6", 25600, "#5591b5",
            44400, "#2d6a8e", 91300, DARK])
YEAR = ["step", ["get", "FirstYearBuilt"], "#d9dee1",
        1800, "#4a2d78", 1900, "#7c5295", 1946, "#b085c9",
        1976, "#e0a8e0", 2001, RED]
# VacantLot uses Access-style booleans: -1 true, 0 false
VAC = ["match", ["get", "VacantLot"], 0, LIGHT, -1, RED, GRAY]

emit("parcels", "default", style(
    "parcels", "All parcels",
    "Every parcel in the city: quiet fill with hairline lot lines — the "
    "base reference view of the assessor's parcel layer.",
    [fill("parcels", "#f4f1ea", 0.85, "#b8b2a6"),
     line("parcels", "#8f8878", 0.3, lid="lots")]), default=True)
emit("parcels", "style-assessed-value", style(
    "parcels", "Assessed value",
    "Total assessed value (AsdTotal) in quintile steps — the city's wealth "
    "geography, from north-side disinvestment to the Central West End.",
    [fill("parcels", ASD, 0.8, "#ffffff00")], legend=ASD))
emit("parcels", "style-vacant-lots", style(
    "parcels", "Vacant lots",
    "The assessor's VacantLot flag (23,238 parcels): the vacancy crescent in "
    "red against occupied parcels.",
    [fill("parcels", VAC, 0.75)], legend=VAC))
emit("parcels", "style-year-built", style(
    "parcels", "Year built",
    "FirstYearBuilt in era steps (unknown, pre-1900, 1900-45, 1946-75, "
    "1976-2000, 2001+): the city's growth rings.",
    [fill("parcels", YEAR, 0.8)], legend=YEAR))
CITY_PARCELS = fill("parcels", "#e9ffbe", 1.0, "#6e6e6e")
emit("parcels", "style-city-assessor", style(
    "parcels", "City assessor map",
    "The city's own parcel symbology, extracted from the "
    "PDA/PARCELS_PUBLIC ArcGIS renderer.",
    [CITY_PARCELS]))

# --------------------------------------------------------------------------
# zoning — 126,945 polygons; LAYER = district letter, names from city renderer
# --------------------------------------------------------------------------
ZONE_NAMES = {  # verbatim from the city's ArcGIS renderer labels
    "A": "A Single-Family Residential Dwelling District",
    "B": "B Two-Family Dwelling District",
    "C": "C Multiple-Family Dwelling District",
    "D": "D Multiple-Family Dwelling District",
    "E": "E Multiple-Family Dwelling District",
    "F": "F Neighborhood Commercial District",
    "G": "G Local Commercial and Office District",
    "H": "H Area Commercial District",
    "I": "I Central Business District",
    "J": "J Industrial District",
    "K": "K Unrestricted District",
    "L": "L Jefferson Memorial District",
}
ZONE_COLORS = {
    "A": "#a6c96a", "B": "#7fb356", "C": "#538400", "D": "#3f6600",
    "E": "#2d4a00", "F": "#e9b84e", "G": "#e89d07", "H": "#c97b1d",
    "I": RED, "J": "#7c5295", "K": "#8b6f5e", "L": LIGHTBLUE,
}
ZONE = match("LAYER", ZONE_COLORS)

# parcels carry the same zoning letters on the assessor record
PARCEL_ZONE = match("Zoning", ZONE_COLORS)
emit("parcels", "style-zoning", style(
    "parcels", "Zoning district",
    "Each parcel colored by its zoning letter from the assessor record, "
    "using the city's official district names (A Single-Family through "
    "L Jefferson Memorial).",
    [fill("parcels", PARCEL_ZONE, 0.75, "#ffffff00")], legend=PARCEL_ZONE))
ZGROUP = ["match", ["get", "LAYER"],
          "A", GREEN, "B", GREEN, "C", GREEN, "D", GREEN, "E", GREEN,
          "F", ORANGE, "G", ORANGE, "H", ORANGE,
          "I", RED, "J", "#7c5295", "K", "#8b6f5e", "L", LIGHTBLUE, GRAY]

emit("zoning", "default", style(
    "zoning", "Zoning districts",
    "Parcel-level zoning colored by the twelve district letters, with the "
    "city's official district names (from the city's own map renderer) in "
    "the legend.",
    [fill("zoning", ZONE, 0.75, "#ffffff00")], legend=ZONE), default=True)
emit("zoning", "style-broad-use", style(
    "zoning", "Residential / commercial / industrial",
    "Districts grouped into broad uses: residential A-E green, commercial "
    "F-H orange, Central Business red, Industrial purple, Unrestricted "
    "brown, Jefferson Memorial light blue.",
    [fill("zoning", ZGROUP, 0.7, "#ffffff00")], legend=ZGROUP))
emit("zoning", "style-boundaries", style(
    "zoning", "District boundaries",
    "Zoning outlines only, for overlaying on imagery or the parcel fabric.",
    [line("zoning", DARK, 0.6)]))

# --------------------------------------------------------------------------
# city-trees — 134,588 points; condition, size, species, planting sites
# --------------------------------------------------------------------------
COND = match("CONDITION", {
    "Excellent": "#1a6b1a", "Very Good": "#2e8b2e", "Good": GREEN,
    "Fair": "#c9c93e", "Poor": ORANGE, "Critical": "#d05f27",
    "Dead": RED, "Stump": "#8b6f5e", "N/A": LIGHT})
SIZE_COLOR = step("DBH", "#c8e6c9", [2, "#8fce8f", 6, GREEN, 14, "#2d6a2d", 24, "#0f3d0f"])
PLANT = match("COMMON", {"Vacant": ORANGE}, GREEN)
SPECIES = match("COMMON", {
    "Maple, Red": RED, "Pear, Callery": "#e8c4d8", "Oak, Pin": "#7c5295",
    "Maple, Sugar": ORANGE, "Redbud": "#c98bab", "Linden, Littleleaf": "#4a9d9c",
    "Ash, Green": GREEN, "Ash, White": "#a6c96a", "Vacant": LIGHT})

emit("city-trees", "default", style(
    "city-trees", "Street trees",
    "All 134,588 tree and planting sites managed by Forestry, sized by zoom.",
    [circle("city-trees", GREEN, zoom_radius(2.5), stroke="#FFFFFF")]),
    default=True)
emit("city-trees", "style-condition", style(
    "city-trees", "Tree condition",
    "Forestry's condition rating from Excellent (dark green) through Dead "
    "(red) and Stump (brown); N/A is mostly vacant planting sites.",
    [circle("city-trees", COND, zoom_radius(2.5), stroke="#FFFFFF")],
    legend=COND))
emit("city-trees", "style-size", style(
    "city-trees", "Trunk diameter",
    "DBH (diameter at breast height, inches) in quartile steps 2/6/14/24 — "
    "darker means older, bigger canopy.",
    [circle("city-trees", SIZE_COLOR, zoom_radius(2.5), stroke="#FFFFFF")],
    legend=SIZE_COLOR))
emit("city-trees", "style-planting-sites", style(
    "city-trees", "Vacant planting sites",
    "30,935 sites recorded as Vacant (orange) against existing trees "
    "(green) — where the next street tree could go.",
    [circle("city-trees", PLANT, zoom_radius(2.5))], legend=PLANT))
emit("city-trees", "style-species", style(
    "city-trees", "Common species",
    "The eight most common species; everything else gray. Callery pear and "
    "green ash tell maintenance stories (invasives, emerald ash borer).",
    [circle("city-trees", SPECIES, zoom_radius(2.5))], legend=SPECIES))

# --------------------------------------------------------------------------
# csb-311-requests — 1.48M points since 2008
# --------------------------------------------------------------------------
GROUPS = match("GROUP", {
    "Trash/Debris/Green Waste": "#8b6f5e", "Right of Way Issues": GRAY,
    "Trees": GREEN, "Vehicles": "#7c5295", "Street Lights": ORANGE,
    "Weeds/Grass": "#a6c96a", "Animals": "#c98bab",
    "Street Sign/Painting": LIGHTBLUE}, LIGHT)
OPEN = ["match", ["get", "STATUS"],
        "CLOSED", LIGHT, "Closed", LIGHT, "CANCEL", "#cfd6da",
        "Cancel", "#cfd6da", RED]
CALLER = match("CALLERTYPE", {
    "WEB": BLUE, "PHONE": GREEN, "NSO": ORANGE, "INDETERMINATE": LIGHT,
    "TWITTER": LIGHTBLUE, "EMAIL": "#7c5295"}, GRAY)

emit("csb-311-requests", "default", style(
    "csb-311-requests", "311 service requests",
    "1.48 million Citizens' Service Bureau requests since 2008, as a dense "
    "point field.",
    [circle("csb-311-requests", BLUE,
            ["interpolate", ["linear"], ["zoom"], 8, 1.6, 12, 2.2, 16, 4.5],
            opacity=0.75, stroke="#FFFFFF")]), default=True)
emit("csb-311-requests", "style-category", style(
    "csb-311-requests", "Request category",
    "The eight biggest request groups — trash/debris leads with 400k, then "
    "right-of-way, trees, vehicles, street lights.",
    [circle("csb-311-requests", GROUPS, zoom_radius(1.8), opacity=0.6)],
    legend=GROUPS))
emit("csb-311-requests", "style-open", style(
    "csb-311-requests", "Open vs. resolved",
    "Requests not yet closed or cancelled in red — the live backlog against "
    "1.4M resolved (light).",
    [circle("csb-311-requests", OPEN, zoom_radius(1.8), opacity=0.55)],
    legend=OPEN))
emit("csb-311-requests", "style-channel", style(
    "csb-311-requests", "Reporting channel",
    "How requests arrive: web vs. phone vs. NSO staff vs. the Twitter era.",
    [circle("csb-311-requests", CALLER, zoom_radius(1.8), opacity=0.55)],
    legend=CALLER))

# --------------------------------------------------------------------------
# streets — 19,858 lines; Class codes, suffix
# --------------------------------------------------------------------------
CLASSW = ["match", ["get", "Class"],
          "A31", 3.0, "A41", 1.2, "A61", 2.0, "A62", 2.0, "A63", 2.0,
          "A73", 2.4, 1.0]
CLASSC = match("Class", {
    "A31": RED, "A41": GRAY, "A61": ORANGE, "A62": ORANGE,
    "A63": ORANGE, "A73": BLUE})
SUFFIX = match("Street_Name_Post_Type", {
    "AVE": BLUE, "ST": RED, "BLVD": ORANGE, "DR": GREEN,
    "PL": "#7c5295", "RD": "#8b6f5e", "LN": "#4a9d9c", "CT": "#c98bab"}, LIGHT)

emit("streets", "default", style(
    "streets", "City streets",
    "The street centerline network, weighted by the source Class code "
    "(arterials heavier).",
    [line("streets", DARK, CLASSW)]), default=True)
emit("streets", "style-class", style(
    "streets", "Street class",
    "The source Class codes as-is (A31 red, A73 blue, A6x orange, A41 local "
    "gray). The city does not publish a decode; codes follow Census "
    "feature-class conventions.",
    [line("streets", CLASSC, CLASSW)], legend=CLASSC))
emit("streets", "style-suffix", style(
    "streets", "Avenue, Street, or Boulevard?",
    "Streets colored by their name suffix — St. Louis's east-west Avenues "
    "vs. north-south Streets grid pattern pops out.",
    [line("streets", SUFFIX, 1.4)], legend=SUFFIX))

# --------------------------------------------------------------------------
# parks — 117 polygons; class, acreage
# --------------------------------------------------------------------------
PCLASS = match("NEW_CLASS", {
    "Neighborhood": GREEN, "Community": "#2e8b2e", "Regional": "#0f5d0f",
    "Mini": "#a6c96a", "Special Use": ORANGE, "Cemetery": "#8b6f5e",
    "Independent": "#4a9d9c", "Commemorative": "#c98bab", "Not City": GRAY})
PSIZE = step("ACRES", "#c8e6c9", [4, "#8fce8f", 14, GREEN, 100, "#0f3d0f"])

emit("parks", "default", style(
    "parks", "City parks",
    "All 117 city parks in park green with labels.",
    [fill("parks", GREEN, 0.6, "#2d4a00"), label("parks", "TEXT_", 11, 11)]),
    default=True)
emit("parks", "style-class", style(
    "parks", "Park classification",
    "The Parks Department's classification: neighborhood, community, "
    "regional, mini, special-use, cemeteries.",
    [fill("parks", PCLASS, 0.7, "#ffffff00")], legend=PCLASS))
emit("parks", "style-size", style(
    "parks", "Park size",
    "Acreage steps (4 / 14 / 100+): Forest Park's 1,293 acres anchors the "
    "dark end.",
    [fill("parks", PSIZE, 0.75, "#ffffff00")], legend=PSIZE))

# --------------------------------------------------------------------------
# neighborhoods — 88 polygons
# --------------------------------------------------------------------------
NBR_NUM = ["step", ["to-number", ["get", "NHD_NUM"]], "#dbe8f0",
           20, "#a8d4e8", 40, "#6ba3c4", 60, "#3d7a9e", 80, DARK]

NBR_FILL = repeat_fill(["get", "NHD_NUM"], 10)
emit("neighborhoods", "default", style(
    "neighborhoods", "Neighborhoods",
    "The 88 official neighborhoods, each tinted from a repeating ten-color "
    "set so adjacent neighborhoods read apart, with name labels. Colors "
    "carry no meaning.",
    [fill("neighborhoods", NBR_FILL, 0.65, "#FFFFFF"),
     line("neighborhoods", "#FFFFFF", 1.2),
     label("neighborhoods", "NHD_NAME", 11, 10)], no_legend=True),
    default=True)
emit("neighborhoods", "style-number", style(
    "neighborhoods", "Neighborhood number",
    "Official neighborhood numbers in steps of 20 — numbering runs roughly "
    "south to north, so the gradient traces the city's geography.",
    [fill("neighborhoods", NBR_NUM, 0.75, "#ffffff"),
     line("neighborhoods", "#FFFFFF", 0.8)], legend=NBR_NUM))
emit("neighborhoods", "style-boundaries", style(
    "neighborhoods", "Boundaries only",
    "Just the lines, for overlays.",
    [line("neighborhoods", BLUE, 2.0)]))

# --------------------------------------------------------------------------
# wards — 14 polygons (2020 redistricting, effective 2023)
# --------------------------------------------------------------------------
def ward_match(get_expr):
    expr = ["match", get_expr]
    for i in range(14):
        expr += [str(i + 1), POLY[i]]
    expr.append(GRAY)
    return expr


def ward_match_bold(get_expr):
    expr = ["match", get_expr]
    for i in range(14):
        expr += [str(i + 1), BOLD[i]]
    expr.append(GRAY)
    return expr


WARD = ward_match_bold(["get", "DISTRICT"])
emit("wards", "default", style(
    "wards", "Wards (2020)",
    "The fourteen wards from 2020 redistricting in bold saturated colors "
    "with heavy dark borders, labeled — deliberately weightier than the "
    "pastel precinct map.",
    [fill("wards", WARD, 0.72, DARK), line("wards", DARK, 2.5),
     label("wards", "NAME", 13, 9)], legend=WARD), default=True)
emit("wards", "style-boundaries", style(
    "wards", "Ward boundaries",
    "Outlines only.", [line("wards", RED, 2.0)]))
emit("wards", "style-subtle", style(
    "wards", "Subtle wards",
    "Light tint for use under other data.",
    [fill("wards", LIGHTBLUE, 0.18, BLUE), line("wards", BLUE, 1.0)]))

# --------------------------------------------------------------------------
# city-boundary — 1 polygon
# --------------------------------------------------------------------------
emit("city-boundary", "default", style(
    "city-boundary", "City boundary",
    "The city limits — St. Louis is an independent city, in no county "
    "since 1876.",
    [line("city-boundary", RED, 2.5)]), default=True)
emit("city-boundary", "style-filled", style(
    "city-boundary", "Filled",
    "Boundary with a light tint.",
    [fill("city-boundary", LIGHTBLUE, 0.2, RED), line("city-boundary", RED, 2.0)]))
emit("city-boundary", "style-dashed", style(
    "city-boundary", "Dashed context line",
    "Dashed outline for basemap-heavy contexts.",
    [line("city-boundary", DARK, 2.0, dash=[3, 2])]))

# --------------------------------------------------------------------------
# city-blocks — 5,857 polygons; historic block numbering
# --------------------------------------------------------------------------
BLOCKNUM = ["step", ["to-number", ["get", "Name"]], "#e3ecf1",
            1000, "#b9d3e2", 2500, "#88b3cd", 4000, "#5591b5", 5500, DARK]
emit("city-blocks", "default", style(
    "city-blocks", "City blocks",
    "Every numbered block as a readable unit: semi-transparent city-blue "
    "fill, white borders, and the block number labeled at high zoom.",
    [fill("city-blocks", "#5b8db0", 0.45, "#FFFFFF"),
     line("city-blocks", "#FFFFFF", 1.0),
     label("city-blocks", "Name", 10, 14)]), default=True)
emit("city-blocks", "style-block-number", style(
    "city-blocks", "Block numbering",
    "Block numbers in steps — numbering began downtown by the river and "
    "grew outward, so the gradient replays the city's expansion.",
    [fill("city-blocks", BLOCKNUM, 0.8, "#FFFFFF")], legend=BLOCKNUM))
emit("city-blocks", "style-by-ward", style(
    "city-blocks", "Blocks by ward (2010)",
    "Blocks tinted by their 2010 ward (WARD10, repeating colors) with "
    "block-number labels — see which ward each block sat in.",
    [fill("city-blocks", repeat_fill(["get", "WARD10"], 10), 0.65, "#FFFFFF"),
     line("city-blocks", "#FFFFFF", 0.6),
     label("city-blocks", "Name", 10, 14)], no_legend=True))
emit("city-blocks", "style-by-precinct", style(
    "city-blocks", "Blocks by precinct (2010)",
    "Blocks tinted by 2010 precinct (PRECINCT10, repeating colors), "
    "labeled with the block number.",
    [fill("city-blocks", repeat_fill(["get", "PRECINCT10"], 12), 0.65, "#FFFFFF"),
     line("city-blocks", "#FFFFFF", 0.6),
     label("city-blocks", "Name", 10, 14)], no_legend=True))
emit("city-blocks", "style-by-census-tract", style(
    "city-blocks", "Blocks by census tract (2010)",
    "Blocks tinted by 2010 census tract (CensTract10, repeating colors), "
    "labeled with the block number.",
    [fill("city-blocks", repeat_fill(["to-number", ["get", "CensTract10"]], 14), 0.65, "#FFFFFF"),
     line("city-blocks", "#FFFFFF", 0.6),
     label("city-blocks", "Name", 10, 14)], no_legend=True))

# --------------------------------------------------------------------------
# police-districts — 6 polygons
# --------------------------------------------------------------------------
PD = match("DISTNO", {"1": CAT[0], "2": CAT[1], "3": CAT[2],
                      "4": CAT[3], "5": CAT[4], "6": CAT[5]})
emit("police-districts", "default", style(
    "police-districts", "Police districts",
    "The six SLMPD districts, one color each, labeled by number.",
    [fill("police-districts", PD, 0.5, "#FFFFFF"),
     line("police-districts", "#FFFFFF", 1.2),
     label("police-districts", "DISTNO", 14, 9)], legend=PD), default=True)
emit("police-districts", "style-boundaries", style(
    "police-districts", "District boundaries",
    "Outlines only.", [line("police-districts", DARK, 2.0)]))
emit("police-districts", "style-subtle", style(
    "police-districts", "Subtle districts",
    "Light tint for underlays.",
    [fill("police-districts", LIGHTBLUE, 0.2, BLUE), line("police-districts", BLUE, 1.0)]))

# --------------------------------------------------------------------------
# election-precincts — 209 polygons; names like "W 8 P 5"
# --------------------------------------------------------------------------
# Precinct names encode the ward: "W 8 P 5" → ward "8". slice/index-of are
# valid style-spec v8 string expressions (MapLibre GL JS and Native).
PRECINCT_WARD = ward_match(
    ["slice", ["get", "name"], 2, ["index-of", " P", ["get", "name"]]])
emit("election-precincts", "default", style(
    "election-precincts", "Precincts by ward",
    "The 209 current voting precincts colored by their ward (from the "
    "precinct name, 'W <ward> P <precinct>'), labeled. Same ward colors as "
    "the wards collection.",
    [fill("election-precincts", PRECINCT_WARD, 0.6, "#FFFFFF"),
     line("election-precincts", "#FFFFFF", 0.8),
     label("election-precincts", "name", 10, 12)], legend=PRECINCT_WARD),
    default=True)
emit("election-precincts", "style-boundaries", style(
    "election-precincts", "Precinct boundaries",
    "Outlines only.", [line("election-precincts", "#7c5295", 1.2)]))
emit("election-precincts", "style-tint", style(
    "election-precincts", "Tinted precincts",
    "Solid light fill for reference.",
    [fill("election-precincts", "#e8e0f0", 0.6, "#7c5295")]))

# --------------------------------------------------------------------------
# historic-districts — 109 polygons; DIS_TYPE
# --------------------------------------------------------------------------
HD = match("DIS_TYPE", {"National": BLUE, "Local": RED,
                        "Certified Local": ORANGE, "Landmark": "#7c5295"})
HD_LOCAL = match("DIS_TYPE", {"National": LIGHT, "Local": RED,
                              "Certified Local": RED, "Landmark": RED})
emit("historic-districts", "default", style(
    "historic-districts", "Historic districts",
    "All 109 districts by designation: National Register (85), Local, "
    "Certified Local, Landmark.",
    [fill("historic-districts", HD, 0.55, "#FFFFFF")], legend=HD),
    default=True)
emit("historic-districts", "style-local-protection", style(
    "historic-districts", "Local protection",
    "Districts with local regulatory teeth (local/certified/landmark) in "
    "red against advisory National Register listings (light).",
    [fill("historic-districts", HD_LOCAL, 0.6, GRAY)], legend=HD_LOCAL))
emit("historic-districts", "style-boundaries", style(
    "historic-districts", "District boundaries",
    "Outlines with labels.",
    [line("historic-districts", "#7c5295", 1.5),
     label("historic-districts", "DISNAME", 10, 12)]))

# --------------------------------------------------------------------------
# tif-districts — 191 polygons; Incentive_Status
# --------------------------------------------------------------------------
TIF = match("Incentive_Status", {
    "Active": GREEN, "Terminated": GRAY, "Retired": LIGHTBLUE,
    "Never Approved": LIGHT, "On Hold": ORANGE, "MODESA": "#7c5295"})
TIF_ACTIVE = match("Incentive_Status", {"Active": RED}, LIGHT)
emit("tif-districts", "default", style(
    "tif-districts", "TIF districts by status",
    "All 191 tax-increment-financing districts: 110 active (green), plus "
    "terminated, retired, never-approved, on-hold, and one MODESA.",
    [fill("tif-districts", TIF, 0.6, "#FFFFFF")], legend=TIF), default=True)
emit("tif-districts", "style-active", style(
    "tif-districts", "Active TIFs",
    "Just the 110 active districts in red — where increment capture is "
    "happening now.",
    [fill("tif-districts", TIF_ACTIVE, 0.6, GRAY)], legend=TIF_ACTIVE))
emit("tif-districts", "style-boundaries", style(
    "tif-districts", "District boundaries",
    "Outlines only.", [line("tif-districts", ORANGE, 1.5)]))

# --------------------------------------------------------------------------
# opportunity-zones — 16 polygons
# --------------------------------------------------------------------------
emit("opportunity-zones", "default", style(
    "opportunity-zones", "Opportunity zones",
    "The 16 federally designated Qualified Opportunity Zone tracts.",
    [fill("opportunity-zones", ORANGE, 0.5, "#b57506"),
     line("opportunity-zones", "#b57506", 1.2)]), default=True)
emit("opportunity-zones", "style-labeled", style(
    "opportunity-zones", "Labeled zones",
    "Zones with their district names.",
    [fill("opportunity-zones", ORANGE, 0.4, "#b57506"),
     label("opportunity-zones", "District_Name", 10, 10)]))
emit("opportunity-zones", "style-boundaries", style(
    "opportunity-zones", "Zone boundaries",
    "Outlines only.", [line("opportunity-zones", ORANGE, 2.0)]))

# --------------------------------------------------------------------------
# community-improvement-districts — 98 polygons; Active flag
# --------------------------------------------------------------------------
CID = match("Active", {"Y": GREEN, "N": GRAY}, LIGHT)
emit("community-improvement-districts", "default", style(
    "community-improvement-districts", "CIDs by status",
    "The 98 community improvement districts: 70 active (green), 21 "
    "inactive (gray), 7 unrecorded (light).",
    [fill("community-improvement-districts", CID, 0.6, "#FFFFFF")],
    legend=CID), default=True)
emit("community-improvement-districts", "style-labeled", style(
    "community-improvement-districts", "Labeled CIDs",
    "Districts with names.",
    [fill("community-improvement-districts", GREEN, 0.4, "#2d4a00"),
     label("community-improvement-districts", "Name", 10, 11)]))
emit("community-improvement-districts", "style-boundaries", style(
    "community-improvement-districts", "District boundaries",
    "Outlines only.", [line("community-improvement-districts", GREEN, 1.5)]))

# --------------------------------------------------------------------------
# special-business-districts — 22 polygons; Active flag
# --------------------------------------------------------------------------
SBD = match("Active", {"Y": BLUE, "N": GRAY}, LIGHT)
emit("special-business-districts", "default", style(
    "special-business-districts", "SBDs by status",
    "The 22 special business districts by active status.",
    [fill("special-business-districts", SBD, 0.6, "#FFFFFF")], legend=SBD),
    default=True)
emit("special-business-districts", "style-labeled", style(
    "special-business-districts", "Labeled SBDs",
    "Districts with names.",
    [fill("special-business-districts", BLUE, 0.4, DARK),
     label("special-business-districts", "Name", 10, 11)]))
emit("special-business-districts", "style-boundaries", style(
    "special-business-districts", "District boundaries",
    "Outlines only.", [line("special-business-districts", BLUE, 1.5)]))

# --------------------------------------------------------------------------
# tax-abated-parcels — 1,440 polygons; abatement years 2001-2025
# --------------------------------------------------------------------------
ABATE_START = step("AbatementStartYear", LIGHT,
                   [2001, "#c6dbe8", 2011, "#8fbdd6", 2016, "#5591b5",
                    2021, DARK])
ABATE_END = step("AbatementEndYear", GRAY, [2026, GREEN])
emit("tax-abated-parcels", "default", style(
    "tax-abated-parcels", "Abatements by start year",
    "1,440 parcels with active real-estate tax abatements, stepped by when "
    "the abatement began (2001-2025).",
    [fill("tax-abated-parcels", ABATE_START, 0.75, "#FFFFFF")],
    legend=ABATE_START), default=True)
emit("tax-abated-parcels", "style-expiring", style(
    "tax-abated-parcels", "Still abated after 2026?",
    "Green where the abatement runs past 2026, gray where it has expired "
    "or expires this year.",
    [fill("tax-abated-parcels", ABATE_END, 0.75, "#FFFFFF")],
    legend=ABATE_END))
emit("tax-abated-parcels", "style-solid", style(
    "tax-abated-parcels", "All abated parcels",
    "Every abated parcel in one color, for overlay on the parcel fabric.",
    [fill("tax-abated-parcels", RED, 0.6, "#FFFFFF")]))

# --------------------------------------------------------------------------
# lra-property — 9,467 polygons; Status / Usage / Property_Source
# --------------------------------------------------------------------------
LRA_STATUS = match("Status", {
    "Available": GREEN, "Greenspace Hold": "#4a9d9c", "CDA Option": ORANGE,
    "Development Hold": ORANGE, "Legal Hold": "#7c5295", "SOLD": LIGHTBLUE,
    "SOLD (RORE)": LIGHTBLUE, "Unavailable": GRAY})
LRA_USE = match("Usage", {
    "Vacant Lot": ORANGE, "vacant lot": ORANGE, "Residential": BLUE,
    "residential": BLUE, "Mixed-Use": "#7c5295", "Commercial": RED,
    "Condo": LIGHTBLUE})
LRA_SRC = match("Property_Source", {
    "Tax Suit": BLUE, "Donations": GREEN, "Donation": GREEN,
    "Tax Sale": ORANGE, "TAX SALE": ORANGE, "CDA": "#7c5295",
    "HUD Donations": "#4a9d9c"})
emit("lra-property", "default", style(
    "lra-property", "LRA inventory by status",
    "The Land Reutilization Authority's 9,467 parcels — the nation's "
    "oldest land bank — mostly Available (green), with holds, options, "
    "and recent sales.",
    [fill("lra-property", LRA_STATUS, 0.7, "#FFFFFF")], legend=LRA_STATUS),
    default=True)
emit("lra-property", "style-usage", style(
    "lra-property", "Lot usage",
    "What sits on each LRA parcel: 8,000 vacant lots (orange) vs. "
    "residential structures (blue), commercial (red), mixed-use (purple).",
    [fill("lra-property", LRA_USE, 0.7, "#FFFFFF")], legend=LRA_USE))
emit("lra-property", "style-source", style(
    "lra-property", "How the LRA got it",
    "Acquisition path: tax foreclosure suits dominate (blue), plus "
    "donations (green), tax sales (orange), CDA transfers (purple).",
    [fill("lra-property", LRA_SRC, 0.7, "#FFFFFF")], legend=LRA_SRC))
emit("lra-property", "style-solid", style(
    "lra-property", "All LRA parcels",
    "One color for overlaying on other data.",
    [fill("lra-property", RED, 0.55, "#FFFFFF")]))


def normalize_city_renderers() -> None:
    """Finish the styles extracted from the city's ArcGIS renderers.

    The extractor writes the renderer's layers but no tile source URL, and
    knows nothing about the browser's legend mechanism. Inject the pmtiles
    source and, for data-driven renderers, the inert legend fill layer.
    """
    for f in sorted(CATALOG.glob("*/*/styles/city-renderer.json")):
        coll_id = f.parent.parent.name
        s = json.loads(f.read_text())
        s.setdefault("sources", {}).setdefault("data", {})
        s["sources"]["data"] = {"type": "vector",
                                "url": f"pmtiles://../{coll_id}.pmtiles"}
        s.setdefault("metadata", {}).setdefault(
            "description",
            "The city's own symbology, extracted from the source ArcGIS "
            "renderer.")
        s["name"] = s.get("name") or "City renderer"
        if s["name"] in ("Simple Style", "Categorical Style"):
            s["name"] = "City renderer"

        def expr(layer, prop):
            v = layer.get("paint", {}).get(prop)
            return v if isinstance(v, list) and v and v[0] in ("match", "step") else None

        legend = None
        for layer in s.get("layers", []):
            layer["source-layer"] = coll_id
            layer.setdefault("source", "data")
            for prop in ("fill-color", "line-color", "circle-color"):
                legend = legend or expr(layer, prop)
        first = s["layers"][0] if s.get("layers") else None
        needs_legend = legend is not None and not (
            first and first.get("type") == "fill" and expr(first, "fill-color"))
        if needs_legend:
            s["layers"] = [{
                "id": f"{coll_id}-legend", "type": "fill", "source": "data",
                "source-layer": coll_id,
                "paint": {"fill-color": legend, "fill-opacity": 0},
            }] + s["layers"]
        f.write_text(json.dumps(s, indent=2) + "\n")
        print(f"✓ normalized {coll_id}/styles/city-renderer.json")


def main() -> None:
    total = 0
    for coll_id, styles in STYLES.items():
        d = CATALOG / coll_rel(coll_id) / "styles"
        if not (CATALOG / coll_rel(coll_id)).exists():
            print(f"✗ no collection dir: {coll_id}")
            continue
        d.mkdir(exist_ok=True)
        defaults = [f for f, (_, dflt) in styles.items() if dflt]
        assert len(defaults) == 1, f"{coll_id}: need exactly 1 default, got {defaults}"
        for fname, (obj, _) in styles.items():
            (d / f"{fname}.json").write_text(json.dumps(obj, indent=2) + "\n")
            total += 1
        print(f"✓ {coll_id}: {len(styles)} styles (default: {defaults[0]})")
    print(f"{total} styles written")
    normalize_city_renderers()


# --------------------------------------------------------------------------
# bike-infrastructure — 2,387 lines across five source layers
# --------------------------------------------------------------------------
BIKE_TYPE = match("BikeFacilityType", {
    "Separated Bike Lane": "#0f5d0f", "Buffered Bike Lane": GREEN,
    "Bike Lane": "#7fb356", "Bike Blvd": "#4a9d9c",
    "Multi-Use Path": "#7c5295", "Shared Lane Markings": ORANGE,
    "Shared Lane": "#e2a76f", "Climbing Lane": LIGHTBLUE,
    "Share the Road Sign": GRAY}, "#b0a377")
BIKE_NET = match("source_layer", {
    "Bike Facilities": BLUE, "Brickline Greenway And Hodiamont Trail": RED,
    "Park Paths": GREEN, "Multi Use Path": "#7c5295",
    "Planned And Funded Major Bike Facility Projects": ORANGE})
BIKE_PLANNED = match("source_layer", {
    "Planned And Funded Major Bike Facility Projects": RED}, LIGHT)

emit("bike-infrastructure", "default", style(
    "bike-infrastructure", "Bike facilities by type",
    "Every bike facility colored by the city's own facility types — from "
    "separated and buffered lanes (greens) through paint-only shared-lane "
    "markings (orange). Protection level reads as green-to-orange.",
    [line("bike-infrastructure", BIKE_TYPE, 2.2)], legend=BIKE_TYPE),
    default=True)
emit("bike-infrastructure", "style-network", style(
    "bike-infrastructure", "Network layers",
    "The five source layers: street bike facilities, the Brickline Greenway "
    "and Hodiamont Trail, park paths, multi-use paths, and planned/funded "
    "major projects.",
    [line("bike-infrastructure", BIKE_NET, 2.2)], legend=BIKE_NET))
emit("bike-infrastructure", "style-planned", style(
    "bike-infrastructure", "Planned projects",
    "The nine planned and funded major bike facility projects in red over "
    "the existing network (light).",
    [line("bike-infrastructure", BIKE_PLANNED, 2.4)], legend=BIKE_PLANNED))

# --------------------------------------------------------------------------
# Wave 2 collections (2026-08): AGOL finds + remaining portal datasets
# --------------------------------------------------------------------------

# lead-service-lines — 112,950 address points; domain codes from the service
LSLI_STATUS_LABELS = {  # verbatim ArcGIS domain: code → name
    0: "Unknown", 1: "Lead", 2: "Non-Lead",
    3: "Galvanized Requiring Replacement"}
LSLI_STATUS = match("utilstatus_desc", {
    "Lead": RED, "Galvanized Requiring Replacement": ORANGE,
    "Non-Lead": GREEN, "Unknown": GRAY}, LIGHT)
LSLI_CUST = match("custstatus_desc", {
    "Lead": RED, "Galvanized Requiring Replacement": ORANGE,
    "Non-Lead": GREEN, "Unknown": GRAY}, LIGHT)
LSLI_MAT = match("utilmaterial_desc", {
    "Lead": RED, "Galvanized Pipe": ORANGE, "Copper": GREEN,
    "Ductile Iron": "#4a9d9c", "Cast Iron": "#7c5295",
    "Polyvinyl Chloride": LIGHTBLUE, "Polyethylene": "#a6c96a",
    "Asbestos Cement": "#8b6f5e", "Brass": "#c98bab",
    "Unknown": GRAY}, LIGHT)
emit("lead-service-lines", "default", style(
    "lead-service-lines", "Utility-side service line status",
    "Every water service line by the utility-side status from the Water "
    "Division's EPA lead inventory: Lead red, Galvanized-requiring-"
    "replacement orange, Non-Lead green, Unknown gray (names decoded "
    "from the service's own coded-value domain).",
    [circle("lead-service-lines", LSLI_STATUS, zoom_radius(2.2),
            stroke="#FFFFFF")], legend=LSLI_STATUS), default=True)
emit("lead-service-lines", "style-customer-side", style(
    "lead-service-lines", "Customer-side status",
    "Same classification for the customer-owned side of each service line.",
    [circle("lead-service-lines", LSLI_CUST, zoom_radius(2.2),
            stroke="#FFFFFF")], legend=LSLI_CUST))
emit("lead-service-lines", "style-material", style(
    "lead-service-lines", "Pipe material",
    "Utility-side pipe material, decoded from the service's own domain: "
    "Lead red, Galvanized orange, Copper green, iron teal/purple, "
    "plastics light, Unknown gray.",
    [circle("lead-service-lines", LSLI_MAT, zoom_radius(2.2))],
    legend=LSLI_MAT))

# market-value-analysis — 314 block groups, MVA clusters A (strongest) - I
MVA = match("MVACluster", {
    "A": "#1a6b1a", "B": "#2e8b2e", "C": "#7fb356", "D": "#c9c93e",
    "E": "#e8c46a", "F": ORANGE, "G": "#d0752e", "H": "#c0392b", "I": "#8b1a1a"})
emit("market-value-analysis", "default", style(
    "market-value-analysis", "MVA cluster",
    "The 2024 Market Value Analysis housing-market clusters, A (strongest "
    "markets, dark green) through I (most distressed, dark red), by census "
    "block group.",
    [fill("market-value-analysis", MVA, 0.72, "#FFFFFF"),
     line("market-value-analysis", "#FFFFFF", 0.8)], legend=MVA), default=True)
MVA_PRICE = step("MSP2123_CA", "#eef3f6",
                 [50000, "#c6dbe8", 100000, "#8fbdd6", 175000, "#5591b5",
                  250000, "#2d6a8e", 350000, DARK])
emit("market-value-analysis", "style-sale-price", style(
    "market-value-analysis", "Median sale price 2021-23",
    "Census-adjusted median sale price (MSP2123_CA) in steps from under "
    "$50k to over $350k.",
    [fill("market-value-analysis", MVA_PRICE, 0.8, "#FFFFFF")],
    legend=MVA_PRICE))
MVA_VAC = step("PVacBuild", "#eef3f6",
               [0.02, "#e8c46a", 0.05, ORANGE, 0.1, "#d0752e", 0.2, RED])
emit("market-value-analysis", "style-vacancy-rate", style(
    "market-value-analysis", "Vacant building share",
    "Share of buildings vacant (PVacBuild) in steps: under 2 percent "
    "through over 20 percent.",
    [fill("market-value-analysis", MVA_VAC, 0.8, "#FFFFFF")],
    legend=MVA_VAC))

# vacancy-composite — 20,694 parcels, Tolemi vacancy classification
VAC_TYPE = match("PROPERTY_T", {"Land": ORANGE, "Structure": RED})
VAC_DEF = match("TOLEMI_DEF", {
    "LRA-Owned Vacant Lot": "#e2a76f",
    "Private Vacant Lot": ORANGE,
    "Northside Regeneration Vacant Lot": "#c9b970",
    "BD Vacant Building Registry - Residential": RED,
    "Structural Condemnation and No Occupancy": "#8b1a1a",
    "LRA-Owned Building": "#c0392b"}, GRAY)
emit("vacancy-composite", "default", style(
    "vacancy-composite", "Vacant land vs structures",
    "SLDC's parcel-level vacancy composite: 13,987 vacant lots (orange) "
    "and 6,707 vacant structures (red).",
    [fill("vacancy-composite", VAC_TYPE, 0.75, "#FFFFFF")],
    legend=VAC_TYPE), default=True)
emit("vacancy-composite", "style-source", style(
    "vacancy-composite", "Vacancy classification",
    "The composite's own top classes: LRA lots, private lots, Northside "
    "Regeneration lots, vacant-building registry, condemnations; smaller "
    "combined classes gray.",
    [fill("vacancy-composite", VAC_DEF, 0.75, "#FFFFFF")], legend=VAC_DEF))
VAC_YEAR = ["step", ["get", "YEAR_BUILT"], "#d9dee1",
            1, "#4a2d78", 1880, "#7c5295", 1900, "#b085c9", 1930, "#e0a8e0",
            1960, RED]
emit("vacancy-composite", "style-year-built", style(
    "vacancy-composite", "Vacant stock by year built",
    "Year built of the vacant stock in era steps; 0 or unknown light gray "
    "— most of the vacancy crescent predates 1930.",
    [fill("vacancy-composite", VAC_YEAR, 0.75, "#FFFFFF")], legend=VAC_YEAR))

# land-use — 11,567 SLUP polygons
SLUP = match("SLUP_LATES", {
    "NPA": "#a6c96a", "NCA": GREEN, "NDA": "#3f6600", "IPDA": "#7c5295",
    "SMUA": ORANGE, "BIPA": "#e8c46a", "BIDA": "#d0752e", "ROSPDA": "#4a9d9c",
    "OGPA": "#88b8a3", "SPCA": LIGHTBLUE}, GRAY)
emit("land-use", "default", style(
    "land-use", "Strategic land use categories",
    "The Strategic Land Use Plan by its category codes (NPA neighborhood "
    "preservation is the bulk; the source publishes codes only).",
    [fill("land-use", SLUP, 0.72, "#ffffff00")], legend=SLUP), default=True)
SLUP_STATUS = match("Status", {"Original": LIGHT, "Amended": ORANGE,
                               "Amendment": RED})
emit("land-use", "style-amendments", style(
    "land-use", "Plan amendments",
    "Where the 2005 plan has been amended (orange/red) against untouched "
    "Original designations (light).",
    [fill("land-use", SLUP_STATUS, 0.72, "#ffffff00")], legend=SLUP_STATUS))
emit("land-use", "style-boundaries", style(
    "land-use", "Category boundaries",
    "Outlines only.", [line("land-use", DARK, 0.6)]))

# forest-park-trees — 15,450 trees
FP_COND = match("Condition", {
    "Excellent": "#1a6b1a", "Very Good": "#2e8b2e", "Good": GREEN,
    "Fair": "#c9c93e", "Poor": ORANGE, "Critical": "#d05f27",
    "Dead": RED, "Stump": "#8b6f5e"}, LIGHT)
FP_SIZE = step("DBH", "#c8e6c9", [6, "#8fce8f", 15, GREEN, 30, "#2d6a2d"])
emit("forest-park-trees", "default", style(
    "forest-park-trees", "Forest Park trees",
    "All 15,450 inventoried trees in Forest Park, sized by zoom.",
    [circle("forest-park-trees", GREEN, zoom_radius(2.2), stroke="#FFFFFF")]),
    default=True)
emit("forest-park-trees", "style-condition", style(
    "forest-park-trees", "Tree condition",
    "Condition rating from Excellent (dark green) to Dead (red).",
    [circle("forest-park-trees", FP_COND, zoom_radius(2.2),
            stroke="#FFFFFF")], legend=FP_COND))
emit("forest-park-trees", "style-size", style(
    "forest-park-trees", "Trunk diameter",
    "DBH steps at 6, 15, and 30 inches — the park's veteran canopy in "
    "dark green.",
    [circle("forest-park-trees", FP_SIZE, zoom_radius(2.2),
            stroke="#FFFFFF")], legend=FP_SIZE))

# schools — 133 points
SCHOOLS_SYS = match("USER_School_System", {
    "SLPS": BLUE, "Charter": ORANGE, "Private": "#7c5295"}, GRAY)
emit("schools", "default", style(
    "schools", "City schools",
    "The 133 school locations, labeled.",
    [circle("schools", BLUE, zoom_radius(4), stroke="#FFFFFF"),
     label("schools", "USER_School_Name", 10, 12)]), default=True)
emit("schools", "style-system", style(
    "schools", "By school system",
    "Colored by the source's school-system field.",
    [circle("schools", SCHOOLS_SYS, zoom_radius(4), stroke="#FFFFFF")],
    legend=SCHOOLS_SYS))
emit("schools", "style-plain", style(
    "schools", "Locations only",
    "Unlabeled points for overlays.",
    [circle("schools", DARK, zoom_radius(3.5), stroke="#FFFFFF")]))

# floodplain — 329 FEMA zones
FLOOD = match("FLD_ZONE", {
    "AE": BLUE, "0.2 PCT ANNUAL CHANCE FLOOD HAZARD": LIGHTBLUE,
    "X PROTECTED BY LEVEE": "#4a9d9c"}, GRAY)
emit("floodplain", "default", style(
    "floodplain", "Flood zones",
    "FEMA flood zones: AE 1-percent-annual-chance in blue, 0.2-percent in "
    "light blue, levee-protected X zones teal.",
    [fill("floodplain", FLOOD, 0.55, "#FFFFFF")], legend=FLOOD), default=True)
emit("floodplain", "style-sfha", style(
    "floodplain", "Special flood hazard area",
    "Just the regulatory SFHA (SFHA_TF = T) in blue against the rest.",
    [fill("floodplain", ["match", ["get", "SFHA_TF"], "T", BLUE, LIGHT],
          0.6, "#FFFFFF")],
    legend=["match", ["get", "SFHA_TF"], "T", BLUE, LIGHT]))
emit("floodplain", "style-boundaries", style(
    "floodplain", "Zone boundaries",
    "Outlines only.", [line("floodplain", BLUE, 1.2)]))

# port-authority-district — 1 polygon
emit("port-authority-district", "default", style(
    "port-authority-district", "Port Authority District",
    "The Port Authority District boundary along the Mississippi riverfront.",
    [fill("port-authority-district", "#4a9d9c", 0.4, "#2d6a68"),
     line("port-authority-district", "#2d6a68", 2.0)]), default=True)
emit("port-authority-district", "style-outline", style(
    "port-authority-district", "Outline",
    "Boundary line only.", [line("port-authority-district", "#2d6a68", 2.5)]))
emit("port-authority-district", "style-dashed", style(
    "port-authority-district", "Dashed context line",
    "Dashed outline for overlays.",
    [line("port-authority-district", "#2d6a68", 2.0, dash=[3, 2])]))

# wards-2010 — the previous 28 wards
W10 = repeat_fill(["get", "Ward"], 14)
emit("wards-2010", "default", style(
    "wards-2010", "Wards (2010)",
    "The 28 aldermanic wards in force 2011-2022, repeating colors, labeled "
    "— the geography most older city datasets (WARD10 columns) reference.",
    [fill("wards-2010", W10, 0.6, "#FFFFFF"), line("wards-2010", "#FFFFFF", 1.0),
     label("wards-2010", "Ward", 11, 10)], no_legend=True), default=True)
emit("wards-2010", "style-boundaries", style(
    "wards-2010", "Ward boundaries",
    "Outlines only.", [line("wards-2010", "#7c5295", 1.6)]))
emit("wards-2010", "style-subtle", style(
    "wards-2010", "Subtle wards",
    "Light tint for underlays.",
    [fill("wards-2010", LIGHT, 0.3, "#7c5295"), line("wards-2010", "#7c5295", 0.8)]))

# siren-locations — 58 outdoor warning sirens
emit("siren-locations", "default", style(
    "siren-locations", "Outdoor warning sirens",
    "The 58 outdoor warning sirens, in alert red.",
    [circle("siren-locations", RED, zoom_radius(5), stroke="#FFFFFF")]),
    default=True)
SIREN_OWNER = ["match", ["get", "PROPERTY_OWNER"],
               "CITY OF ST LOUIS", BLUE, "City of St Louis", BLUE, ORANGE]
emit("siren-locations", "style-ownership", style(
    "siren-locations", "Site ownership",
    "Sirens on city-owned property (blue) vs. other owners (orange).",
    [circle("siren-locations", SIREN_OWNER, zoom_radius(5),
            stroke="#FFFFFF")], legend=SIREN_OWNER))
emit("siren-locations", "style-plain", style(
    "siren-locations", "Locations only",
    "Neutral points for overlays.",
    [circle("siren-locations", DARK, zoom_radius(4), stroke="#FFFFFF")]))

# polling-places — 152 polling centers
POLL_ACCESS = match("disabledentry", {"Yes": GREEN, "No": RED}, GRAY)
POLL_CITYWIDE = match("cityWideVoting", {"Yes": BLUE}, LIGHT)
emit("polling-places", "default", style(
    "polling-places", "Polling centers",
    "The 152 polling centers, labeled.",
    [circle("polling-places", "#7c5295", zoom_radius(4.5), stroke="#FFFFFF"),
     label("polling-places", "pollingPlace", 10, 12)]), default=True)
emit("polling-places", "style-accessible", style(
    "polling-places", "Accessible entry",
    "Sites with a marked accessible entrance (green) vs. not (red); "
    "unrecorded gray.",
    [circle("polling-places", POLL_ACCESS, zoom_radius(4.5),
            stroke="#FFFFFF")], legend=POLL_ACCESS))
emit("polling-places", "style-citywide", style(
    "polling-places", "Citywide voting sites",
    "Centers where any city voter can vote (blue) against precinct-bound "
    "sites (light).",
    [circle("polling-places", POLL_CITYWIDE, zoom_radius(4.5),
            stroke="#FFFFFF")], legend=POLL_CITYWIDE))

# tornado-damage-2025 — NWS damage path + 286 survey points
TORN_EF = ["match", ["get", "efscale"],
           "EF0", "#c9c93e", "EF1", ORANGE, "EF2", "#d0752e", "EF3", RED,
           "EF4", "#8b1a1a", GRAY]
emit("tornado-damage-2025", "default", style(
    "tornado-damage-2025", "Damage survey",
    "The NWS damage-assessment record of the May 16, 2025 tornado: the "
    "damage path with 286 surveyed damage points colored by EF-scale "
    "rating.",
    [fill("tornado-damage-2025", "#e8c46a", 0.25, "#b57506"),
     line("tornado-damage-2025", "#b57506", 1.5),
     circle("tornado-damage-2025", TORN_EF, zoom_radius(3.5),
            stroke="#FFFFFF")], legend=TORN_EF), default=True)
TORN_LAYER = match("source_layer", {
    "Nws Dat Damage Paths": ORANGE, "Nws Dat Damage Pnts": RED})
emit("tornado-damage-2025", "style-layers", style(
    "tornado-damage-2025", "Path vs points",
    "The damage path polygon (orange) and the individual survey points "
    "(red).",
    [fill("tornado-damage-2025", "#e8c46a", 0.3, "#b57506"),
     circle("tornado-damage-2025", RED, zoom_radius(3))], legend=TORN_LAYER))
emit("tornado-damage-2025", "style-path", style(
    "tornado-damage-2025", "Damage path",
    "The tornado track alone.",
    [fill("tornado-damage-2025", ORANGE, 0.35, "#b57506"),
     line("tornado-damage-2025", "#b57506", 2.0)]))

# flood-controls — 42 floodwall segments + 29 closure points
FLOODC = match("source_layer", {
    "Stlouis Gis Floodwall": BLUE, "Streets Dbo Flood Control": RED})
emit("flood-controls", "default", style(
    "flood-controls", "Floodwall and closures",
    "The riverfront floodwall (blue lines) with its 29 closure structures "
    "(red points).",
    [line("flood-controls", BLUE, 2.5),
     circle("flood-controls", RED, zoom_radius(4), stroke="#FFFFFF")],
    legend=FLOODC), default=True)
FLOOD_STAGE = ["step", ["to-number", ["get", "FLOOD_STAGE"]], GRAY,
               1, GREEN, 30, "#c9c93e", 38, ORANGE, 46, RED]
emit("flood-controls", "style-closing-stage", style(
    "flood-controls", "Closure flood stage",
    "Closure structures stepped by the river stage at which they close "
    "(feet on the St. Louis gage).",
    [circle("flood-controls", FLOOD_STAGE, zoom_radius(4.5),
            stroke="#FFFFFF"), line("flood-controls", LIGHT, 1.5)],
    legend=FLOOD_STAGE))
emit("flood-controls", "style-plain", style(
    "flood-controls", "Structures only",
    "Neutral rendering for overlays.",
    [line("flood-controls", DARK, 2.0),
     circle("flood-controls", DARK, zoom_radius(3.5))]))

# neighborhood-organizations — 103 org boundaries (2020 snapshot)
ORG_ACTIVE = match("active", {"Yes": GREEN, "No": RED, "Unknown": GRAY}, LIGHT)
ORG_501 = match("F501c3", {"Yes": BLUE, "No": ORANGE}, GRAY)
emit("neighborhood-organizations", "default", style(
    "neighborhood-organizations", "Organizations by activity",
    "The 103 neighborhood organizations as of the 2020 export: active "
    "(green), inactive (red), unknown (gray).",
    [fill("neighborhood-organizations", ORG_ACTIVE, 0.55, "#FFFFFF"),
     label("neighborhood-organizations", "labelForMap", 10, 12)],
    legend=ORG_ACTIVE), default=True)
emit("neighborhood-organizations", "style-501c3", style(
    "neighborhood-organizations", "501(c)(3) status",
    "Organizations with nonprofit status (blue) vs. without (orange).",
    [fill("neighborhood-organizations", ORG_501, 0.55, "#FFFFFF")],
    legend=ORG_501))
emit("neighborhood-organizations", "style-boundaries", style(
    "neighborhood-organizations", "Coverage boundaries",
    "Outlines only.", [line("neighborhood-organizations", "#7c5295", 1.4)]))

# --------------------------------------------------------------------------
# Wave 3 (2026-08): joined-PMTiles tabular collections + animal bites
# The tabular collections keep non-geo parquet as their data asset; these
# styles drive the join-materialized PMTiles (tools/make_joined_pmtiles.py).
# --------------------------------------------------------------------------

PERMIT_YEAR = ["step", ["get", "PERMIT_YEAR"], LIGHT,
               1990, "#c6dbe8", 2000, "#8fbdd6", 2010, "#5591b5",
               2015, "#2d6a8e", 2020, DARK]
PERMIT_RECENT = ["step", ["get", "PERMIT_YEAR"], LIGHT, 2020, RED]

def permit_styles(cid, what):
    emit(cid, "default", style(
        cid, f"{what} by year",
        f"Parcels with {what.lower()}, stepped by permit year (joined to "
        "the parcels layer on HANDLE; a parcel appears once per permit).",
        [fill(cid, PERMIT_YEAR, 0.7, "#ffffff00")], legend=PERMIT_YEAR),
        default=True)
    emit(cid, "style-recent", style(
        cid, "Permits since 2020",
        "Parcels with activity since 2020 in red against the older record.",
        [fill(cid, PERMIT_RECENT, 0.7, "#ffffff00")], legend=PERMIT_RECENT))
    emit(cid, "style-solid", style(
        cid, "All permitted parcels",
        "Every joined parcel in one color, for overlays.",
        [fill(cid, BLUE, 0.55, "#ffffff00")]))

permit_styles("electrical-permits", "Electrical permits")
permit_styles("mechanical-permits", "Mechanical permits")
permit_styles("plumbing-permits", "Plumbing permits")
permit_styles("occupancy-permits", "Occupancy permits")

TAX_ASD = step("AsdTotal", "#eef3f6",
               [1600, "#c6dbe8", 7700, "#8fbdd6", 25600, "#5591b5",
                44400, "#2d6a8e", 91300, DARK])
TAX_LAND = step("AsdLand", "#eef3f6",
                [500, "#d9f0d3", 2000, "#a6dba0", 5000, "#5aae61",
                 15000, "#1b7837"])
emit("property-taxes", "default", style(
    "property-taxes", "Assessed total",
    "The assessor's tax roll joined to parcel geometry: total assessed "
    "value in quintile steps.",
    [fill("property-taxes", TAX_ASD, 0.8, "#ffffff00")], legend=TAX_ASD),
    default=True)
emit("property-taxes", "style-land-value", style(
    "property-taxes", "Assessed land value",
    "Land-only assessed value (AsdLand) in steps — land value geography "
    "without improvements.",
    [fill("property-taxes", TAX_LAND, 0.8, "#ffffff00")], legend=TAX_LAND))
emit("property-taxes", "style-solid", style(
    "property-taxes", "Tax roll parcels",
    "Every joined parcel in one color.",
    [fill("property-taxes", BLUE, 0.5, "#ffffff00")]))

SALE_PRICE = step("SalePrice", "#eef3f6",
                  [10000, "#c6dbe8", 60000, "#8fbdd6", 150000, "#5591b5",
                   300000, "#2d6a8e", 600000, DARK])
SALE_YEAR = ["step", ["get", "SALE_YEAR"], LIGHT,
             1990, "#c6dbe8", 2000, "#8fbdd6", 2010, "#5591b5", 2020, RED]
emit("property-sales", "default", style(
    "property-sales", "Sale price",
    "Recorded sales joined to parcel geometry, stepped by sale price; a "
    "parcel appears once per sale.",
    [fill("property-sales", SALE_PRICE, 0.75, "#ffffff00")],
    legend=SALE_PRICE), default=True)
emit("property-sales", "style-year", style(
    "property-sales", "Sale year",
    "Sales stepped by decade, 2020s in red.",
    [fill("property-sales", SALE_YEAR, 0.75, "#ffffff00")], legend=SALE_YEAR))
PPSF = step("PricePerSqFt", "#eef3f6",
            [1, "#c6dbe8", 4, "#8fbdd6", 10, "#5591b5", 25, "#2d6a8e",
             60, DARK], to_number=True)
emit("property-sales", "style-price-per-sqft", style(
    "property-sales", "Price per square foot",
    "Sale price divided by the parcel's lot area — the cleanest way to "
    "compare land value across parcel sizes (steps at $1, $4, $10, $25, "
    "$60 per sq ft of lot).",
    [fill("property-sales", PPSF, 0.78, "#ffffff00")], legend=PPSF))
emit("property-sales", "style-solid", style(
    "property-sales", "All sold parcels",
    "Every parcel with a recorded sale.",
    [fill("property-sales", GREEN, 0.5, "#ffffff00")]))

STREET_N = step("n_permits", "#eef3f6",
                [50, "#c6dbe8", 250, "#8fbdd6", 750, "#5591b5", 1500, DARK])
emit("street-permits", "default", style(
    "street-permits", "Street permits by neighborhood",
    "Street-permit records aggregated to neighborhoods (the source lists "
    "neighborhood names, not parcels): count of permits per neighborhood.",
    [fill("street-permits", STREET_N, 0.75, "#FFFFFF"),
     line("street-permits", "#FFFFFF", 0.8)], legend=STREET_N), default=True)
emit("street-permits", "style-boundaries", style(
    "street-permits", "Neighborhood outlines",
    "Outlines only.", [line("street-permits", BLUE, 1.2)]))
emit("street-permits", "style-solid", style(
    "street-permits", "Covered neighborhoods",
    "Neighborhoods with any street permit.",
    [fill("street-permits", LIGHTBLUE, 0.4, BLUE)]))

TURNOUT = ["step", ["get", "Turnout_Percentage"], "#f5e6e6",
           30, "#e8c4c4", 45, "#c98b8b", 55, "#8b3a3a", 65, "#5a1a1a"]
REGV = step("Registered_Voters", "#eef3f6",
            [500, "#c6dbe8", 1000, "#8fbdd6", 1500, "#5591b5", 2000, DARK])
emit("election-results-nov-2024", "default", style(
    "election-results-nov-2024", "Turnout by precinct",
    "November 2024 general election turnout percentage by precinct "
    "(precinct-level summary of the vote-totals table, joined to precinct "
    "geometry).",
    [fill("election-results-nov-2024", TURNOUT, 0.78, "#FFFFFF"),
     line("election-results-nov-2024", "#FFFFFF", 0.6)], legend=TURNOUT),
    default=True)
PRES_SHARE = ["step", ["get", "Pres_Dem_TwoPartyShare"], "#8b1a1a",
              0.5, "#e8c4c4", 0.7, "#a8c4e0", 0.85, "#4575b4", 0.95, "#1a3a6b"]
emit("election-results-nov-2024", "style-presidential", style(
    "election-results-nov-2024", "Presidential two-party share",
    "Harris share of the two-party presidential vote by precinct (Harris "
    "and Trump votes only; steps at 50, 70, 85, and 95 percent — red "
    "below 50).",
    [fill("election-results-nov-2024", PRES_SHARE, 0.8, "#FFFFFF"),
     line("election-results-nov-2024", "#FFFFFF", 0.6)], legend=PRES_SHARE))
emit("election-results-nov-2024", "style-registered", style(
    "election-results-nov-2024", "Registered voters",
    "Registered voters per precinct in steps.",
    [fill("election-results-nov-2024", REGV, 0.78, "#FFFFFF")], legend=REGV))
emit("election-results-nov-2024", "style-ballots", style(
    "election-results-nov-2024", "Ballots cast",
    "Ballots cast per precinct.",
    [fill("election-results-nov-2024",
          step("Ballots_Cast", "#eef3f6",
               [300, "#c6dbe8", 600, "#8fbdd6", 900, "#5591b5", 1200, DARK]),
          0.78, "#FFFFFF")],
    legend=step("Ballots_Cast", "#eef3f6",
                [300, "#c6dbe8", 600, "#8fbdd6", 900, "#5591b5", 1200, DARK])))

BITES = match("ANIMAL_TYPE", {
    "Dog": "#8b3a2e", "dog": "#8b3a2e", "small dog": "#8b3a2e",
    "Cat": ORANGE, "Wildlife": GREEN,
    "Unknown or not provided": GRAY}, GRAY)
emit("animal-bites", "default", style(
    "animal-bites", "Animal bites",
    "Reported animal bites since 2008 as points (Web-Mercator coordinates "
    "in the source, reprojected).",
    [circle("animal-bites", "#8b3a2e", zoom_radius(2.6), stroke="#FFFFFF")]),
    default=True)
emit("animal-bites", "style-animal", style(
    "animal-bites", "By animal",
    "Dogs (brown, 5,300+), cats (orange), wildlife (green), unknown gray.",
    [circle("animal-bites", BITES, zoom_radius(2.6), stroke="#FFFFFF")],
    legend=BITES))
emit("animal-bites", "style-plain", style(
    "animal-bites", "Locations only",
    "Neutral points for overlays.",
    [circle("animal-bites", DARK, zoom_radius(2.2))]))

# --------------------------------------------------------------------------
# Final wave (2026-08): parcels history, crime, sweep picks
# --------------------------------------------------------------------------

ERA = match("era", {"1997": "#4a2d78", "2000": "#7c5295", "2005": "#b085c9",
                    "2010": "#5591b5", "2015": "#2d6a8e",
                    "2016-2020": DARK}, LIGHT)
emit("parcels-history", "default", style(
    "parcels-history", "Parcels by era",
    "Five-year snapshots of the city's parcel boundaries (the map shows "
    "1997, 2000, 2005, 2010, 2015, and 2016-2020; the full Parquet holds "
    "every yearly snapshot, 3.1M rows).",
    [line("parcels-history", ERA, 0.5)], legend=ERA), default=True)
emit("parcels-history", "style-1997", style(
    "parcels-history", "Parcels in 1997",
    "The oldest snapshot alone — compare against the current parcels "
    "collection to see consolidation and demolition.",
    [line("parcels-history",
          ["match", ["get", "era"], "1997", "#4a2d78", "#00000000"], 0.7)],
    legend=["match", ["get", "era"], "1997", "#4a2d78", "#00000000"]))
emit("parcels-history", "style-2020", style(
    "parcels-history", "Parcels in 2016-2020",
    "The newest snapshot in the archive (published as a single 2016-2020 "
    "era file).",
    [line("parcels-history",
          ["match", ["get", "era"], "2016-2020", DARK, "#00000000"], 0.7)],
    legend=["match", ["get", "era"], "2016-2020", DARK, "#00000000"]))

HIST_ZONE_1997 = ["case",
    ["==", ["get", "era"], "1997"],
    match("ZONING1", ZONE_COLORS), "#00000000"]
emit("parcels-history", "style-zoning-1997", style(
    "parcels-history", "Zoning in 1997",
    "Each 1997 parcel filled by its zoning letter — compare with the "
    "current parcels collection's zoning view to see three decades of "
    "rezoning.",
    [fill("parcels-history", HIST_ZONE_1997, 0.75, "#ffffff00")],
    legend=match("ZONING1", ZONE_COLORS)))

CRIME_AGAINST = match("CrimeAgainst", {
    "Person": RED, "Property": ORANGE, "Society": "#7c5295",
    "Unspecified": GRAY, "NULL": LIGHT}, LIGHT)
CRIME_CAT = match("NIBRSCategory", {
    "Destruction/Damage/Vandalism of Property": ORANGE,
    "Weapons Law Violations": "#7c5295",
    "Motor Vehicle Theft": "#b5651d",
    "Aggravated Assault": RED,
    "Theft From Motor Vehicle": "#e2a76f",
    "Simple Assault": "#d98d8d",
    "All Other Larceny": "#c9b970",
    "All Other Offenses": GRAY}, LIGHT)
CRIME_GUN = match("FirearmUsed", {"Yes": RED, "No": LIGHT}, GRAY)
emit("crime", "default", style(
    "crime", "Crime against person / property / society",
    "367k NIBRS incidents since 2021, colored by the crime-against "
    "classification: person red, property orange, society purple.",
    [circle("crime", CRIME_AGAINST,
            ["interpolate", ["linear"], ["zoom"], 9, 1.4, 12, 2.2, 16, 4.5],
            opacity=0.65, stroke="#FFFFFF")], legend=CRIME_AGAINST),
    default=True)
emit("crime", "style-category", style(
    "crime", "Offense category",
    "The eight largest NIBRS categories; everything else light gray.",
    [circle("crime", CRIME_CAT,
            ["interpolate", ["linear"], ["zoom"], 9, 1.4, 12, 2.2, 16, 4.5],
            opacity=0.65)], legend=CRIME_CAT))
emit("crime", "style-firearm", style(
    "crime", "Firearm involved",
    "Incidents where a firearm was used, in red.",
    [circle("crime", CRIME_GUN,
            ["interpolate", ["linear"], ["zoom"], 9, 1.4, 12, 2.2, 16, 4.5],
            opacity=0.6)], legend=CRIME_GUN))

LANDMARK = match("SITE_TYPE", {
    "NR_SITE": BLUE, "CLM_SITE": RED, "NLM_SITE": "#7c5295"}, GRAY)
emit("historic-landmarks", "default", style(
    "historic-landmarks", "Historic sites",
    "512 historic sites: National Register (blue), City Landmarks (red), "
    "National Landmarks (purple) — codes from the source layer.",
    [circle("historic-landmarks", LANDMARK, zoom_radius(4),
            stroke="#FFFFFF")], legend=LANDMARK), default=True)
emit("historic-landmarks", "style-plain", style(
    "historic-landmarks", "Locations only",
    "Neutral points for overlays.",
    [circle("historic-landmarks", "#7c5295", zoom_radius(3.5))]))
emit("historic-landmarks", "style-national-register", style(
    "historic-landmarks", "National Register sites",
    "Just the NR-listed sites.",
    [circle("historic-landmarks",
            ["match", ["get", "SITE_TYPE"], "NR_SITE", BLUE, "#00000000"],
            zoom_radius(4))],
    legend=["match", ["get", "SITE_TYPE"], "NR_SITE", BLUE, "#00000000"]))

emit("zip-codes", "default", style(
    "zip-codes", "ZIP codes",
    "The 30 ZIP code areas touching the city, repeating colors, labeled.",
    [fill("zip-codes", repeat_fill(["to-number", ["get", "ZIP"]], 10), 0.55,
          "#FFFFFF"),
     line("zip-codes", "#FFFFFF", 1.0),
     label("zip-codes", "ZIP", 11, 10)], no_legend=True), default=True)
emit("zip-codes", "style-boundaries", style(
    "zip-codes", "ZIP boundaries",
    "Outlines only.", [line("zip-codes", DARK, 1.5)]))
emit("zip-codes", "style-subtle", style(
    "zip-codes", "Subtle tint",
    "Light fill for underlays.",
    [fill("zip-codes", LIGHT, 0.3, GRAY)]))

emit("parking-meters", "default", style(
    "parking-meters", "Parking meters",
    "981 parking meters.",
    [circle("parking-meters", BLUE, zoom_radius(2.8), stroke="#FFFFFF")]),
    default=True)
emit("parking-meters", "style-plain", style(
    "parking-meters", "Locations only",
    "Neutral points.", [circle("parking-meters", DARK, zoom_radius(2.4))]))
emit("parking-meters", "style-bold", style(
    "parking-meters", "High-visibility",
    "Larger orange markers.",
    [circle("parking-meters", ORANGE, zoom_radius(4), stroke="#FFFFFF")]))

SWEEP_DAY = match("Day_Wk", {
    "Monday": BLUE, "Tuesday": GREEN, "Wednesday": ORANGE,
    "Thursday": "#7c5295", "Friday": RED}, GRAY)
emit("street-sweeping", "default", style(
    "street-sweeping", "Sweeping day",
    "Street sweeping areas colored by their scheduled weekday.",
    [fill("street-sweeping", SWEEP_DAY, 0.55, "#FFFFFF"),
     line("street-sweeping", "#FFFFFF", 0.8)], legend=SWEEP_DAY),
    default=True)
emit("street-sweeping", "style-boundaries", style(
    "street-sweeping", "Area boundaries",
    "Outlines only.", [line("street-sweeping", GREEN, 1.2)]))
emit("street-sweeping", "style-labeled", style(
    "street-sweeping", "Routes labeled",
    "Areas with route labels.",
    [fill("street-sweeping", LIGHT, 0.4, GRAY),
     label("street-sweeping", "Route", 10, 12)]))

emit("business-licenses", "default", style(
    "business-licenses", "Business licenses",
    "6,239 licensed businesses as of October 2025.",
    [circle("business-licenses", GREEN, zoom_radius(2.6), stroke="#FFFFFF")]),
    default=True)
emit("business-licenses", "style-plain", style(
    "business-licenses", "Locations only",
    "Neutral points.", [circle("business-licenses", DARK, zoom_radius(2.2))]))
emit("business-licenses", "style-bold", style(
    "business-licenses", "High-visibility",
    "Larger blue markers.",
    [circle("business-licenses", BLUE, zoom_radius(3.6), stroke="#FFFFFF")]))

TAXSALE_BID = step("Opening_Bid", "#eef3f6",
                   [1000, "#c6dbe8", 3000, "#8fbdd6", 7500, "#5591b5",
                    15000, DARK], to_number=True)
emit("tax-sales", "default", style(
    "tax-sales", "Tax sale parcels by opening bid",
    "2,200 parcels in tax sale proceedings, stepped by opening bid.",
    [fill("tax-sales", TAXSALE_BID, 0.75, "#FFFFFF")], legend=TAXSALE_BID),
    default=True)
emit("tax-sales", "style-solid", style(
    "tax-sales", "All tax-sale parcels",
    "One color for overlays.",
    [fill("tax-sales", RED, 0.6, "#FFFFFF")]))
emit("tax-sales", "style-boundaries", style(
    "tax-sales", "Parcel outlines",
    "Outlines only.", [line("tax-sales", RED, 1.0)]))

if __name__ == "__main__":
    main()
