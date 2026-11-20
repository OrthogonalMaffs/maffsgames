#!/usr/bin/env python3
# ci-line: MaffsCards (tools/maffscards/check.py: all 48 cards' six values recomputed by a second method, pi's 1,000 decimals by Machin's formula and the generator's spigot, every value equal to the contract's table and to data/maffscards.json byte for byte; games/maffscards/cards.json the same data plus 288 how lines, each ending on its value; four planted faults caught: one pi count off by one, 1 counted as prime, a hand edit in the JSON, a how line ending on the wrong value; no PDF built in CI) |
# ci-deps: tools/maffscards/ data/maffscards.json games/maffscards/ printables/index.html scripts/plant_common.py
"""CI's entry to the MaffsCards check (contract MAFFSCARDS-DATA, 19 Nov 2026).

CI finds its lines only in scripts/*.py headers (scripts/ci-groups.py), and the check lives in tools/maffscards/, so
this file is the line and nothing more, on scripts/test-loop-cards.py's pattern: it runs `check.py`, then
`check.py --selftest`, and fails if either does. Neither builds the PDF.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(ROOT, "tools", "maffscards", "check.py")

if __name__ == "__main__":
    a = subprocess.call([sys.executable, "-X", "utf8", CHECK])
    b = subprocess.call([sys.executable, "-X", "utf8", CHECK, "--selftest"])
    sys.exit(1 if a or b else 0)
