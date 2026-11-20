#!/usr/bin/env python3
"""Repair child links in group README files after `portolan readme`.

The CLI builds each child link from the collection id. The id carries the
group prefix (`business-and-industry/business-licenses`), and the README
already sits in the group directory, so the generated href doubles the
prefix and resolves to nothing. The correct relative href from a group
README is the collection directory name alone.

Run after `portolan readme` (pipeline step 7). Idempotent.
Upstream report: the portolan-cli readme generator.
"""

import re
import sys
from pathlib import Path

CATALOG = Path(__file__).resolve().parent.parent / "catalog"


def fix_group_readme(readme: Path) -> int:
    group = readme.parent.name
    text = readme.read_text()

    def repl(m: re.Match) -> str:
        href = m.group(1)
        parts = [p for p in href.strip("/").split("/") if p]
        # Drop every leading repeat of the group id, keep the leaf dir.
        while len(parts) > 1 and parts[0] == group:
            parts.pop(0)
        return f"]({'/'.join(parts)}/)"

    fixed = re.sub(r"\]\(((?:[\w-]+/)+)\)", repl, text)
    if fixed != text:
        readme.write_text(fixed)
        return 1
    return 0


def main() -> int:
    n = 0
    for readme in sorted(CATALOG.glob("*/README.md")):
        n += fix_group_readme(readme)
    print(f"fixed child links in {n} group README(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
