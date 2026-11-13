#!/usr/bin/env python3
# ci-line: Pack generator (tools/pack-generator/build_pack.py --selftest: every room with a pack config gets VALID sets, distinct answers per lock and one final-padlock shape, every value recomputed independently; forty-two planted faults caught (answers, draws, URL, score sheet, final padlock, penalties, answer-box hints, stakes placement, page-1 length, repeated rules, shape or calculator on a student page, an unfriendly product, DRAFT and approval, a broken caption or caption override, a print override on a red herring, an ungraded lock); no PDF is ever built in CI) |
# ci-deps: tools/pack-generator/ escape-rooms/ escape-rooms/variants.json scripts/check-escape-rooms.py scripts/escape_set_checks.py scripts/plant_common.py scripts/bank_common.py CNAME
"""CI's entry to the printable-pack generator's self-test (contract PACK-GENERATOR, 4 Nov 2026).

CI finds its lines only in scripts/*.py headers (scripts/ci-groups.py), and the generator lives in tools/pack-generator/,
so this file is the line and nothing more: it runs `build_pack.py --selftest` and returns its exit status. The
self-test builds no PDF: the pack is the product, and never a CI artifact.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "tools", "pack-generator", "build_pack.py")

if __name__ == "__main__":
    sys.exit(subprocess.call([sys.executable, "-X", "utf8", BUILD, "--selftest"]))
