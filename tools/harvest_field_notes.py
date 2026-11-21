#!/usr/bin/env python3
"""Harvest column notes from the city's own ArcGIS field metadata.

The extracts under staging/extracts/<id>/layer-metadata.json carry the
service's field aliases and coded-value domains. Both are the city's own
statements about its fields, so they can become `table:columns`
descriptions without inventing anything. Output goes to
docs/column-notes-arcgis.json; finalize_stac uses it only where the
researched docs/column-notes.json has no entry.

Run after fetch (step 1). Idempotent.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXTRACTS = ROOT / "staging" / "extracts"
OUT = ROOT / "docs" / "column-notes-arcgis.json"

# ESRI's computed geometry fields: the alias is the SQL function name, which
# is better glossed in words.
ESRI_GEOM = {
    "Shape__Area": ("Feature area as computed by the service "
                    "(ESRI Shape.STArea(), in the service's projection "
                    "units)."),
    "Shape__Length": ("Feature perimeter or length as computed by the "
                      "service (ESRI Shape.STLength(), in the service's "
                      "projection units)."),
}


def norm(x: str) -> str:
    return re.sub(r"[^a-z0-9]", "", x.lower())


def domain_note(domain: dict) -> str | None:
    coded = (domain or {}).get("codedValues") or []
    pairs = [(c.get("code"), c.get("name")) for c in coded
             if c.get("name") is not None]
    # A domain where every name repeats its code says nothing.
    pairs = [(c, n) for c, n in pairs if norm(str(c)) != norm(str(n))]
    if not pairs:
        return None
    shown = "; ".join(f"{c} = {n}" for c, n in pairs[:10])
    more = f"; … ({len(pairs)} values)" if len(pairs) > 10 else ""
    return f"Coded values from the city's service: {shown}{more}."


def main() -> int:
    out: dict = {}
    for d in sorted(EXTRACTS.iterdir()):
        lm = d / "layer-metadata.json"
        if not lm.exists():
            continue
        fields = json.loads(lm.read_text()).get("fields") or []
        notes = {}
        for f in fields:
            name, alias = f.get("name"), f.get("alias")
            if not name:
                continue
            if name in ESRI_GEOM:
                notes[name] = ESRI_GEOM[name]
                continue
            dn = domain_note(f.get("domain"))
            if dn:
                notes[name] = dn
            elif alias and norm(alias) != norm(name):
                notes[name] = f"The city's service labels this field '{alias}'."
        if notes:
            out[d.name] = notes
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    total = sum(len(v) for v in out.values())
    print(f"wrote {OUT.relative_to(ROOT)}: {total} notes "
          f"across {len(out)} collections")
    return 0


if __name__ == "__main__":
    sys.exit(main())
