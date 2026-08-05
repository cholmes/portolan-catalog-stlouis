#!/usr/bin/env python3
"""Write .portolan/metadata.yaml for the catalog root and every collection.

Descriptions come verbatim from the city's dataset pages
(docs/portal-descriptions.json, scraped from the portal) — nothing invented.
The portal publishes no explicit data license, so license is "other" with
license_url pointing at each dataset's portal page.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sources import SOURCES

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"
DESCRIPTIONS = json.loads((ROOT / "docs" / "portal-descriptions.json").read_text())

CONTACT = 'contact:\n  name: "Chris Holmes"\n  email: "cholmes@9eo.org"\n'

ROOT_YAML = f"""\
title: "City of St. Louis Open Data (Cloud-Native Mirror)"
description: |
  Cloud-native mirror of datasets from the
  [City of St. Louis open data portal](https://www.stlouis-mo.gov/data/):
  GeoParquet, PMTiles, and STAC metadata for the city's most-used geospatial
  and parcel-joinable datasets. Not an official city service.
{CONTACT}license: "other"
license_url: "https://www.stlouis-mo.gov/data/"
attribution: "City of St. Louis"
source_url: "https://www.stlouis-mo.gov/data/"
keywords: [st-louis, missouri, open-data, city-government, parcels, boundaries, cloud-native, geoparquet, stac, pmtiles]
processing_notes: |
  Mirrored from the City of St. Louis open data portal and the city's public
  ArcGIS REST services (maps6/maps8/maps9.stlouis-mo.gov). Source formats
  (ArcGIS layers, Shapefile, GeoJSON, CSV, DBF) converted to cloud-native
  GeoParquet and PMTiles. The city publishes no explicit data license;
  see each dataset's page on the portal for its terms and context.
"""


def yq(s: str) -> str:
    """YAML-safe double-quoted scalar."""
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def collection_yaml(coll_id: str) -> str:
    src = SOURCES[coll_id]
    desc = DESCRIPTIONS.get(coll_id, {}).get("description", "")
    dept = src["department"]
    kw = ["st-louis", "missouri", "open-data"] + coll_id.split("-")
    lines = [
        f"title: {yq(src['title'])}",
        f"description: {yq(desc)}" if desc else None,
        CONTACT.rstrip(),
        'license: "other"',
        f"license_url: {yq(src['portal_page'])}",
        f"attribution: {yq('City of St. Louis — ' + dept)}",
        f"source_url: {yq(src.get('service') or src.get('url'))}",
        f"keywords: [{', '.join(dict.fromkeys(kw))}]",
        "processing_notes: |",
        f"  Mirrored from the City of St. Louis open data portal"
        f" ({src['portal_page']}).",
        f"  Source: {src.get('service') or src.get('url')}"
        f" ({'ArcGIS REST service' if src['type'] == 'arcgis' else 'portal download'}),",
        "  converted to GeoParquet (zstd, spatially ordered, covering bbox)"
        " and PMTiles.",
    ]
    return "\n".join(l for l in lines if l) + "\n"


def main() -> None:
    d = CATALOG / ".portolan"
    d.mkdir(exist_ok=True)
    (d / "metadata.yaml").write_text(ROOT_YAML)
    print("✓ catalog root metadata.yaml")
    for coll_id in SOURCES:
        cd = CATALOG / coll_id / ".portolan"
        if not (CATALOG / coll_id).exists():
            print(f"✗ missing collection dir: {coll_id}")
            continue
        cd.mkdir(exist_ok=True)
        (cd / "metadata.yaml").write_text(collection_yaml(coll_id))
        print(f"✓ {coll_id}")


if __name__ == "__main__":
    main()
