#!/usr/bin/env python3
"""Fetch the census family into staging/extracts/ (one parquet each).

ACS 2020-2024 5-year estimates come from the table-based Summary File, not
the Census Data API: the API now requires a key on every data request, while
the summary-file .dat files are plain HTTPS. Each national table file is one
row per geography with estimate and margin-of-error side by side
(GEO_ID|B19013_E001|B19013_M001); St. Louis city rows are the ones whose
GEO_ID starts 1500000US29510 (block groups) / 1400000US29510 (tracts).

Every published estimate keeps its margin of error (Census publishes MOEs at
the 90% confidence level). Derived percentages propagate MOEs with the
Census's own formulas (ACS Accuracy of the Data): sums add in quadrature,
proportions use the subset formula with the ratio formula as fallback when
the radicand goes negative. Headline medians and rates also get a
coefficient of variation column (cv = moe/1.645/estimate) so consumers can
grey out unreliable geographies. Jam values (-666666666 and friends) become
NULL, never numbers.

Line numbers are pinned against the release's own table-shells file at fetch
time: a vintage bump that moves a line fails loudly instead of publishing a
mislabeled column.

Geometries are the 2024 cartographic boundary files (GENZ2024, 500k), not
TIGER/Line: TIGER extends block groups into the Mississippi channel, the CB
files clip to the shoreline. The 2024 vintage matches ACS 2020-2024.

LODES 8 (2023) job counts are aggregated census block -> block group by
GEOID prefix (a block's block group is the first 12 characters of its
15-character geocode). HOLC grades come from the Mapping Inequality
GeoParquet on Source Cooperative; CDC PLACES tract estimates from the
Socrata API at data.cdc.gov.

Usage: python3 tools/fetch_census.py [collection-id ...]   (default: all)
"""

import csv
import io
import json
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
import zipfile
from math import sqrt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sources import (ACS_RELEASE, ACS_SF, CB_SHP, HOLC_PARQUET, LODES_BASE,
                     LODES_YEAR, PLACES_API, SOURCES)

ROOT = Path(__file__).resolve().parent.parent
STAGING = ROOT / "staging"
CACHE = STAGING / "census-cache"

STL = "29510"  # Missouri (29) + St. Louis city, its own county-equivalent (510)
BG_PREFIX = "1500000US" + STL
TRACT_PREFIX = "1400000US" + STL
Z90 = 1.645  # ACS margins of error are published at the 90% confidence level
JAM = -111111111  # any value at or below this is an ACS jam code, not data


# ---------------------------------------------------------------------------
# Downloads (cached across collections — the ACS .dat files serve both the
# block-group and tract collections, the CB tract parquet serves cdc-places)
# ---------------------------------------------------------------------------

def cached(url: str, name: str | None = None) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    dest = CACHE / (name or url.rsplit("/", 1)[-1])
    if not dest.exists():
        print(f"  ↓ {url}")
        tmp = dest.with_suffix(dest.suffix + ".part")
        urllib.request.urlretrieve(url, tmp)
        tmp.rename(dest)
    return dest


def cb_parquet(level: str) -> Path:
    """Cartographic boundary shapefile -> EPSG:4326 GeoParquet, city only.

    ogr2ogr does the reprojection so the GeoParquet CRS metadata is written
    by GDAL (DuckDB's ST_Transform computes correct coordinates but stamps
    the wrong CRS — the TriMet catalog hit exactly that).
    """
    zip_path = cached(f"{CB_SHP}/cb_2024_29_{level}_500k.zip")
    out = CACHE / f"cb_2024_stl_{level}_4326.parquet"
    if not out.exists():
        shp_dir = CACHE / f"cb_2024_29_{level}_500k"
        if not shp_dir.exists():
            with zipfile.ZipFile(zip_path) as z:
                z.extractall(shp_dir)
        shp = next(shp_dir.glob("*.shp"))
        subprocess.run(
            ["ogr2ogr", "-f", "Parquet", str(out), str(shp),
             "-t_srs", "EPSG:4326", "-where", "COUNTYFP='510'",
             "-select", "GEOID",
             "-lco", "COMPRESSION=ZSTD", "-lco", "GEOMETRY_NAME=geometry"],
            check=True)
    return out


# ---------------------------------------------------------------------------
# ACS summary file
# ---------------------------------------------------------------------------

def acs_table(table: str, prefix: str) -> dict[str, dict[str, float | None]]:
    """One ACS table -> {geoid: {"E003": v, "M003": v, ...}} for one level.

    Estimates and MOEs at or below the jam threshold become None. An MOE of
    -555555555 means the estimate is controlled (effectively zero error);
    that too becomes None rather than a fake number.
    """
    path = cached(f"{ACS_SF}/data/5YRData/acsdt5y{ACS_RELEASE}-"
                  f"{table.lower()}.dat")
    out = {}
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter="|")
        header = next(reader)
        cols = {name: i for i, name in enumerate(header)}
        for row in reader:
            geo = row[cols["GEO_ID"]]
            if not geo.startswith(prefix):
                continue
            vals = {}
            for name, i in cols.items():
                if name == "GEO_ID":
                    continue
                # B19013_E001 -> key "E001"
                key = name.split("_", 1)[1]
                raw = row[i].strip()
                v = float(raw) if raw not in ("", ".") else None
                if v is not None and v <= JAM:
                    v = None
                vals[key] = v
            out[geo.split("US", 1)[1]] = vals
    return out


def shell_lines(table: str, label_substr: str) -> list[int]:
    """Line numbers in `table` whose shell label contains `label_substr`."""
    shells = cached(f"{ACS_SF}/documentation/"
                    f"ACS{ACS_RELEASE}5YR_Table_Shells.txt")
    lines = []
    with open(shells, encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="|"):
            if row[0] == table and label_substr in row[4]:
                lines.append(int(float(row[1])))
    return lines


def check_shell(table: str, line: int, label_substr: str) -> None:
    """Fail loudly if a pinned line's label moved in this vintage."""
    if line not in shell_lines(table, label_substr):
        raise RuntimeError(
            f"{table} line {line} no longer matches {label_substr!r} in the "
            f"ACS {ACS_RELEASE} table shells — the vintage moved a line")


# Age component lines appear once per sex, so each label resolves to two
# lines; derive them from the shells rather than hardcoding 20 numbers.
UNDER_18_LABELS = ["Under 5 years", "5 to 9 years", "10 to 14 years",
                   "15 to 17 years"]
OVER_65_LABELS = ["65 and 66 years", "67 to 69 years", "70 to 74 years",
                  "75 to 79 years", "80 to 84 years", "85 years and over"]


def age_lines(labels: list[str]) -> list[int]:
    out = []
    for lab in labels:
        found = shell_lines("B01001", lab)
        if len(found) != 2:  # one male + one female line
            raise RuntimeError(f"B01001 {lab!r}: expected 2 lines, "
                               f"got {found}")
        out += found
    return out


# Column spec. kind:
#   count  — sum of lines; MOE adds in quadrature
#   median — single line published as-is (medians never aggregate)
#   pct    — 100 * sum(num) / den; MOE via the Census proportion formula
# den is (table, plus_lines, minus_lines) — minus for denominators like
# B25070's "excluding rent not computed". check pins one line per column
# against the shells. cv adds a coefficient-of-variation column.
BG_SPEC = [
    ("population", "count", "B01003", [1], None,
     ("B01003", 1, "Total"), False),
    ("median_age", "median", "B01002", [1], None,
     ("B01002", 1, "Total"), False),
    ("pct_under_18", "pct", "B01001", "UNDER18", ("B01001", [1], []),
     ("B01001", 1, "Total"), False),
    ("pct_65_plus", "pct", "B01001", "OVER65", ("B01001", [1], []),
     ("B01001", 1, "Total"), False),
    ("pct_white_nh", "pct", "B03002", [3], ("B03002", [1], []),
     ("B03002", 3, "White alone"), False),
    ("pct_black", "pct", "B03002", [4], ("B03002", [1], []),
     ("B03002", 4, "Black or African American alone"), False),
    ("pct_hispanic", "pct", "B03002", [12], ("B03002", [1], []),
     ("B03002", 12, "Hispanic or Latino"), False),
    ("pct_bachelors_plus", "pct", "B15003", [22, 23, 24, 25],
     ("B15003", [1], []), ("B15003", 22, "Bachelor's degree"), False),
    ("median_hh_income", "median", "B19013", [1], None,
     ("B19013", 1, "Median household income"), True),
    ("per_capita_income", "median", "B19301", [1], None,
     ("B19301", 1, "Per capita income"), False),
    ("pct_below_poverty", "pct", "C17002", [2, 3], ("C17002", [1], []),
     ("C17002", 2, "Under .50"), True),
    ("pct_below_2x_poverty", "pct", "C17002", [2, 3, 4, 5, 6, 7],
     ("C17002", [1], []), ("C17002", 8, "2.00 and over"), False),
    ("pct_snap", "pct", "B22010", [2], ("B22010", [1], []),
     ("B22010", 2, "Household received Food Stamps/SNAP"), False),
    ("pct_unemployed", "pct", "B23025", [5], ("B23025", [3], []),
     ("B23025", 5, "Unemployed"), False),
    ("housing_units", "count", "B25002", [1], None,
     ("B25002", 1, "Total"), False),
    ("pct_vacant_units", "pct", "B25002", [3], ("B25002", [1], []),
     ("B25002", 3, "Vacant"), False),
    ("households", "count", "B25003", [1], None,
     ("B25003", 1, "Total"), False),
    ("pct_owner_occupied", "pct", "B25003", [2], ("B25003", [1], []),
     ("B25003", 2, "Owner occupied"), False),
    ("median_gross_rent", "median", "B25064", [1], None,
     ("B25064", 1, "Median gross rent"), True),
    ("pct_rent_burdened", "pct", "B25070", [7, 8, 9, 10],
     ("B25070", [1], [11]), ("B25070", 7, "30.0 to 34.9 percent"), True),
    ("pct_severely_rent_burdened", "pct", "B25070", [10],
     ("B25070", [1], [11]), ("B25070", 10, "50.0 percent or more"), False),
    ("median_home_value", "median", "B25077", [1], None,
     ("B25077", 1, "Median value"), True),
    ("pct_built_pre_1940", "pct", "B25034", [11], ("B25034", [1], []),
     ("B25034", 11, "Built 1939 or earlier"), False),
    ("pct_single_family", "pct", "B25024", [2, 3], ("B25024", [1], []),
     ("B25024", 2, "1, detached"), False),
    ("hh_no_vehicle", "count", "B25044", [3, 10], None,
     ("B25044", 3, "No vehicle available"), False),
    ("pct_hh_no_vehicle", "pct", "B25044", [3, 10], ("B25044", [1], []),
     ("B25044", 10, "No vehicle available"), True),
    ("pct_commute_drive_alone", "pct", "B08301", [3], ("B08301", [1], []),
     ("B08301", 3, "Drove alone"), False),
    ("pct_commute_transit", "pct", "B08301", [10], ("B08301", [1], []),
     ("B08301", 10, "Public transportation"), True),
    ("pct_commute_walk_bike", "pct", "B08301", [18, 19],
     ("B08301", [1], []), ("B08301", 19, "Walked"), False),
    ("pct_work_from_home", "pct", "B08301", [21], ("B08301", [1], []),
     ("B08301", 21, "Worked from home"), False),
    ("pct_commute_45min_plus", "pct", "B08303", [11, 12, 13],
     ("B08303", [1], []), ("B08303", 11, "45 to 59 minutes"), False),
    ("pct_no_internet", "pct", "B28002", [13], ("B28002", [1], []),
     ("B28002", 13, "No Internet access"), True),
    ("pct_no_computer", "pct", "B28001", [11], ("B28001", [1], []),
     ("B28001", 11, "No Computer"), False),
]

TRACT_SPEC = [
    ("population", "count", "B01003", [1], None,
     ("B01003", 1, "Total"), False),
    ("median_hh_income", "median", "B19013", [1], None,
     ("B19013", 1, "Median household income"), True),
    ("pct_below_poverty", "pct", "C17002", [2, 3], ("C17002", [1], []),
     ("C17002", 2, "Under .50"), True),
    ("pct_uninsured", "pct", "B27001", "NOINS", ("B27001", [1], []),
     ("B27001", 1, "Total"), True),
    ("pct_with_disability", "pct", "B18101", "DISAB", ("B18101", [1], []),
     ("B18101", 1, "Total"), True),
    ("pct_foreign_born", "pct", "B05002", [13], ("B05002", [1], []),
     ("B05002", 13, "Foreign-born"), False),
    ("group_quarters_pop", "count", "B26001", [1], None,
     ("B26001", 1, "Total"), False),
    ("median_hh_income_black", "median", "B19013B", [1], None,
     ("B19013B", 1, "Median household income"), True),
    ("pct_below_poverty_black", "pct", "B17020B", [2], ("B17020B", [1], []),
     ("B17020B", 2, "below poverty level"), True),
]


def resolve_lines(spec_lines, table: str) -> list[int]:
    """Expand the named line groups that are derived from the shells."""
    if spec_lines == "UNDER18":
        return age_lines(UNDER_18_LABELS)
    if spec_lines == "OVER65":
        return age_lines(OVER_65_LABELS)
    if spec_lines == "NOINS":
        lines = shell_lines(table, "No health insurance coverage")
        if len(lines) != 18:  # 9 age groups x 2 sexes
            raise RuntimeError(f"B27001: expected 18 no-coverage lines, "
                               f"got {len(lines)}")
        return lines
    if spec_lines == "DISAB":
        lines = shell_lines(table, "With a disability")
        if len(lines) != 12:  # 6 age groups x 2 sexes
            raise RuntimeError(f"B18101: expected 12 disability lines, "
                               f"got {len(lines)}")
        return lines
    return spec_lines


def moe_sum(moes: list[float | None]) -> float | None:
    known = [m for m in moes if m is not None]
    if not known:
        return None
    return sqrt(sum(m * m for m in known))


def cell(vals: dict, kind: str, line: int) -> float | None:
    return vals.get(f"{kind}{line:03d}")


def agg(vals: dict, lines: list[int]) -> tuple[float | None, float | None]:
    """Sum of estimate lines with MOE added in quadrature."""
    ests = [cell(vals, "E", n) for n in lines]
    if all(e is None for e in ests):
        return None, None
    est = sum(e for e in ests if e is not None)
    return est, moe_sum([cell(vals, "M", n) for n in lines])


def pct_moe(num: float, num_moe: float | None, den: float,
            den_moe: float | None) -> float | None:
    """Census proportion formula; ratio formula when the radicand < 0."""
    if num_moe is None or den_moe is None or den == 0:
        return None
    p = num / den
    radicand = num_moe ** 2 - p * p * den_moe ** 2
    if radicand < 0:
        radicand = num_moe ** 2 + p * p * den_moe ** 2
    return 100 * sqrt(radicand) / den


def build_acs(spec, tables: dict[str, dict]) -> tuple[list[str], list[dict]]:
    """Apply a column spec to loaded tables -> (column order, rows)."""
    for name, kind, table, lines, den, check, cv in spec:
        check_shell(*check)

    geoids = sorted(tables[spec[0][2]].keys())
    columns, rows = ["geoid"], []
    for name, kind, table, lines, den, check, cv in spec:
        columns.append(name)
        columns.append(f"{name}_moe")
        if cv:
            columns.append(f"{name}_cv")
    # People of color is the complement of non-Hispanic white; the MOE is the
    # white-alone-NH share's own (a complement has the same error).
    if any(name == "pct_white_nh" for name, *_ in spec):
        columns += ["pct_people_of_color", "pct_people_of_color_moe"]

    for geoid in geoids:
        row = {"geoid": geoid}
        for name, kind, table, lines, den, check, cv in spec:
            vals = tables[table].get(geoid, {})
            lines = resolve_lines(lines, table)
            if kind in ("count", "median"):
                est, moe = agg(vals, lines)
                if kind == "count" and est is not None:
                    est = int(est)
                row[name], row[f"{name}_moe"] = est, moe
            else:  # pct
                den_table, plus, minus = den
                dvals = tables[den_table].get(geoid, {})
                num, num_moe = agg(vals, lines)
                dplus = [cell(dvals, "E", n) for n in plus]
                dminus = [cell(dvals, "E", n) for n in minus]
                if num is None or any(v is None for v in dplus):
                    row[name] = row[f"{name}_moe"] = None
                else:
                    dest = (sum(dplus)
                            - sum(v for v in dminus if v is not None))
                    dmoe = moe_sum([cell(dvals, "M", n)
                                    for n in plus + minus])
                    if dest <= 0:
                        row[name] = row[f"{name}_moe"] = None
                    else:
                        row[name] = round(100 * num / dest, 2)
                        m = pct_moe(num, num_moe, dest, dmoe)
                        row[f"{name}_moe"] = (None if m is None
                                              else round(m, 2))
            if cv:
                est, moe = row[name], row[f"{name}_moe"]
                row[f"{name}_cv"] = (
                    None if not est or moe is None
                    else round((moe / Z90) / est, 3))
        if "pct_white_nh" in row:
            w = row["pct_white_nh"]
            row["pct_people_of_color"] = (None if w is None
                                          else round(100 - w, 2))
            row["pct_people_of_color_moe"] = row["pct_white_nh_moe"]
        rows.append(row)
    return columns, rows


def write_with_geometry(rows: list[dict], columns: list[str],
                        geo_parquet: Path, out: Path,
                        tract_col: bool = False) -> int:
    """Attribute rows + CB geometry -> one staged GeoParquet via DuckDB."""
    import duckdb

    attrs = out.parent / "attrs.csv"
    with open(attrs, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columns)
        w.writeheader()
        w.writerows(rows)
    tract = (", substr(a.geoid, 1, 11) AS tract" if tract_col else "")
    con = duckdb.connect()
    con.execute("INSTALL spatial; LOAD spatial;")
    con.execute(f"""
        COPY (
            SELECT a.* {tract}, g.geometry
            FROM read_csv('{attrs}', header=true, nullstr='',
                          types={{'geoid': 'VARCHAR'}}) a
            JOIN read_parquet('{geo_parquet}') g ON a.geoid = g.GEOID
            ORDER BY a.geoid
        ) TO '{out}' (FORMAT PARQUET, COMPRESSION ZSTD,
                      ROW_GROUP_SIZE 20000)
        """)
    n = con.execute(f"SELECT count(*) FROM read_parquet('{out}')").fetchone()[0]
    con.close()
    attrs.unlink()
    return n


# ---------------------------------------------------------------------------
# Per-dataset fetchers
# ---------------------------------------------------------------------------

def fetch_acs(coll_id: str, level: str, out_dir: Path) -> int:
    spec = BG_SPEC if level == "bg" else TRACT_SPEC
    prefix = BG_PREFIX if level == "bg" else TRACT_PREFIX
    tables = {}
    for _, _, table, _, den, _, _ in spec:
        for t in {table} | ({den[0]} if den else set()):
            if t not in tables:
                tables[t] = acs_table(t, prefix)
    columns, rows = build_acs(spec, tables)
    return write_with_geometry(rows, columns, cb_parquet(level),
                               out_dir / f"{coll_id}.parquet",
                               tract_col=(level == "bg"))


def lodes_url(kind: str, name: str) -> str:
    return f"{LODES_BASE}/{kind}/{name}"


def fetch_lodes_jobs(coll_id: str, out_dir: Path) -> int:
    import duckdb

    wac = cached(lodes_url("wac", f"mo_wac_S000_JT00_{LODES_YEAR}.csv.gz"))
    rac = cached(lodes_url("rac", f"mo_rac_S000_JT00_{LODES_YEAR}.csv.gz"))
    out = out_dir / f"{coll_id}.parquet"
    con = duckdb.connect()
    con.execute("INSTALL spatial; LOAD spatial;")
    # A block's block group is the first 12 characters of its 15-character
    # geocode. LODES omits blocks with zero jobs, so absent means 0 —
    # COALESCE keeps all 314 block groups in the output.
    con.execute(f"""
        CREATE TEMP TABLE w AS
        SELECT substr(w_geocode, 1, 12) AS geoid,
               sum(C000)::BIGINT AS jobs_total,
               sum(CE01)::BIGINT AS jobs_earn_low,
               sum(CE02)::BIGINT AS jobs_earn_mid,
               sum(CE03)::BIGINT AS jobs_earn_high,
               sum(CNS05)::BIGINT AS jobs_manufacturing,
               sum(CNS07)::BIGINT AS jobs_retail,
               sum(CNS15)::BIGINT AS jobs_education,
               sum(CNS16)::BIGINT AS jobs_healthcare,
               sum(CNS18)::BIGINT AS jobs_food_accomm
        FROM read_csv('{wac}', types={{'w_geocode': 'VARCHAR'}})
        WHERE substr(w_geocode, 1, 5) = '{STL}' GROUP BY 1
        """)
    con.execute(f"""
        CREATE TEMP TABLE r AS
        SELECT substr(h_geocode, 1, 12) AS geoid,
               sum(C000)::BIGINT AS workers_resident,
               sum(CE01)::BIGINT AS workers_resident_earn_low,
               sum(CE02)::BIGINT AS workers_resident_earn_mid,
               sum(CE03)::BIGINT AS workers_resident_earn_high
        FROM read_csv('{rac}', types={{'h_geocode': 'VARCHAR'}})
        WHERE substr(h_geocode, 1, 5) = '{STL}' GROUP BY 1
        """)
    con.execute(f"""
        COPY (
            SELECT g.GEOID AS geoid,
                   coalesce(w.jobs_total, 0) AS jobs_total,
                   coalesce(w.jobs_earn_low, 0) AS jobs_earn_low,
                   coalesce(w.jobs_earn_mid, 0) AS jobs_earn_mid,
                   coalesce(w.jobs_earn_high, 0) AS jobs_earn_high,
                   coalesce(w.jobs_manufacturing, 0) AS jobs_manufacturing,
                   coalesce(w.jobs_retail, 0) AS jobs_retail,
                   coalesce(w.jobs_education, 0) AS jobs_education,
                   coalesce(w.jobs_healthcare, 0) AS jobs_healthcare,
                   coalesce(w.jobs_food_accomm, 0) AS jobs_food_accomm,
                   coalesce(r.workers_resident, 0) AS workers_resident,
                   coalesce(r.workers_resident_earn_low, 0)
                       AS workers_resident_earn_low,
                   coalesce(r.workers_resident_earn_mid, 0)
                       AS workers_resident_earn_mid,
                   coalesce(r.workers_resident_earn_high, 0)
                       AS workers_resident_earn_high,
                   g.geometry
            FROM read_parquet('{cb_parquet("bg")}') g
            LEFT JOIN w ON w.geoid = g.GEOID
            LEFT JOIN r ON r.geoid = g.GEOID
            ORDER BY g.GEOID
        ) TO '{out_dir / f"{coll_id}.parquet"}'
          (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 20000)
        """)
    n = con.execute(f"SELECT count(*) FROM read_parquet('{out}')").fetchone()[0]
    con.close()
    return n


def fetch_lodes_od(coll_id: str, out_dir: Path) -> int:
    import duckdb

    main = cached(lodes_url("od", f"mo_od_main_JT00_{LODES_YEAR}.csv.gz"))
    aux = cached(lodes_url("od", f"mo_od_aux_JT00_{LODES_YEAR}.csv.gz"))
    out = out_dir / f"{coll_id}.parquet"
    con = duckdb.connect()
    # od_main: home and work both in Missouri. od_aux: work in Missouri,
    # home out of state. Keep flows that touch the city on either end.
    con.execute(f"""
        COPY (
            SELECT substr(h_geocode, 1, 12) AS home_geoid,
                   substr(w_geocode, 1, 12) AS work_geoid,
                   substr(h_geocode, 1, 5) = '{STL}' AS home_in_city,
                   substr(w_geocode, 1, 5) = '{STL}' AS work_in_city,
                   sum(S000)::BIGINT AS jobs,
                   sum(SE01)::BIGINT AS jobs_earn_low,
                   sum(SE02)::BIGINT AS jobs_earn_mid,
                   sum(SE03)::BIGINT AS jobs_earn_high
            FROM read_csv(['{main}', '{aux}'],
                          types={{'h_geocode': 'VARCHAR',
                                  'w_geocode': 'VARCHAR'}})
            WHERE substr(h_geocode, 1, 5) = '{STL}'
               OR substr(w_geocode, 1, 5) = '{STL}'
            GROUP BY 1, 2, 3, 4
            ORDER BY jobs DESC
        ) TO '{out}' (FORMAT PARQUET, COMPRESSION ZSTD,
                      ROW_GROUP_SIZE 20000)
        """)
    n = con.execute(f"SELECT count(*) FROM read_parquet('{out}')").fetchone()[0]
    con.close()
    return n


def fetch_holc(coll_id: str, out_dir: Path) -> int:
    import duckdb

    out = out_dir / f"{coll_id}.parquet"
    con = duckdb.connect()
    con.execute("INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;")
    con.execute(f"""
        COPY (
            SELECT area_id, city, state, category, grade, label,
                   residential, commercial, industrial, fill,
                   geom AS geometry
            FROM read_parquet('{HOLC_PARQUET}')
            WHERE city = 'St. Louis' AND state = 'MO'
            ORDER BY label
        ) TO '{out}' (FORMAT PARQUET, COMPRESSION ZSTD,
                      ROW_GROUP_SIZE 20000)
        """)
    n = con.execute(f"SELECT count(*) FROM read_parquet('{out}')").fetchone()[0]
    con.close()
    if n == 0:
        raise RuntimeError("HOLC query returned 0 St. Louis polygons — "
                           "did the city/state values change upstream?")
    return n


def fetch_places(coll_id: str, out_dir: Path) -> int:
    import duckdb

    # Socrata paginates; 104 tracts x 40 measures = 4160 rows, one page.
    q = urllib.parse.urlencode({
        "$limit": "10000", "countyfips": STL,
        "$select": "locationname,measureid,short_question_text,measure,year,"
                   "data_value,low_confidence_limit,high_confidence_limit,"
                   "totalpopulation,datavaluetypeid"})
    with urllib.request.urlopen(f"{PLACES_API}.json?{q}", timeout=120) as r:
        records = json.load(r)
    if not records:
        raise RuntimeError("CDC PLACES returned 0 rows for St. Louis")

    tracts: dict[str, dict] = {}
    meta = {}
    for rec in records:
        # Tract-level PLACES publishes crude prevalence only; a second
        # data-value type would silently double rows, so fail if one appears.
        if rec.get("datavaluetypeid") != "CrdPrv":
            raise RuntimeError(f"unexpected PLACES value type: {rec}")
        geoid = rec["locationname"]
        col = rec["measureid"].lower()
        row = tracts.setdefault(geoid, {"geoid": geoid})
        row["total_population"] = int(rec["totalpopulation"])
        for key, suffix in (("data_value", ""), ("low_confidence_limit", "_lo"),
                            ("high_confidence_limit", "_hi")):
            v = rec.get(key)
            row[f"{col}{suffix}"] = float(v) if v not in (None, "") else None
        meta[col] = {"measure": rec["measure"],
                     "short": rec["short_question_text"],
                     "year": rec["year"]}

    (out_dir / "measures.json").write_text(
        json.dumps(dict(sorted(meta.items())), indent=1) + "\n")
    measure_cols = [f"{c}{s}" for c in sorted(meta)
                    for s in ("", "_lo", "_hi")]
    columns = ["geoid", "total_population"] + measure_cols
    rows = [dict.fromkeys(columns) | t for t in
            (tracts[g] for g in sorted(tracts))]
    return write_with_geometry(rows, columns, cb_parquet("tract"),
                               out_dir / f"{coll_id}.parquet")


def fetch_census(coll_id: str, src: dict) -> dict:
    out_dir = STAGING / "extracts" / coll_id
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    dataset = src["dataset"]
    print(f"→ {coll_id}: fetching ({dataset})")
    if dataset == "acs-bg":
        rows = fetch_acs(coll_id, "bg", out_dir)
    elif dataset == "acs-tract":
        rows = fetch_acs(coll_id, "tract", out_dir)
    elif dataset == "lodes-jobs":
        rows = fetch_lodes_jobs(coll_id, out_dir)
    elif dataset == "lodes-od":
        rows = fetch_lodes_od(coll_id, out_dir)
    elif dataset == "holc":
        rows = fetch_holc(coll_id, out_dir)
    elif dataset == "places":
        rows = fetch_places(coll_id, out_dir)
    else:
        raise ValueError(f"unknown census dataset: {dataset}")
    print(f"   {rows} rows")
    return {"status": "ok", "rows": rows,
            "parquets": [str(out_dir / f"{coll_id}.parquet")]}


def main() -> int:
    only = set(sys.argv[1:])
    failures = []
    for coll_id, src in SOURCES.items():
        if src["type"] != "census" or (only and coll_id not in only):
            continue
        try:
            fetch_census(coll_id, src)
        except Exception as e:  # noqa: BLE001
            print(f"  ✗ {coll_id}: {e}")
            failures.append(coll_id)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
