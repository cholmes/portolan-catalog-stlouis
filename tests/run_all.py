#!/usr/bin/env python3
"""Run every gate. Exit non-zero if any fails."""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAILED = []

for test in sorted(HERE.glob("test_*.py")):
    r = subprocess.run([sys.executable, str(test)])
    if r.returncode != 0:
        FAILED.append(test.name)

# rashid conformance, when available
if subprocess.run(["which", "rashid"], capture_output=True).returncode == 0:
    r = subprocess.run(["rashid", "check", str(HERE.parent / "catalog")])
    if r.returncode != 0:
        FAILED.append("rashid check")
else:
    print("(rashid not installed — conformance gate skipped)")

if FAILED:
    print("FAILED:", ", ".join(FAILED))
    raise SystemExit(1)
print("all gates passed")
