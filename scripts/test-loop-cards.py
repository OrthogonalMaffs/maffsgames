#!/usr/bin/env python3
# ci-line: Loop cards (tools/loop-cards/build_deck.py --selftest: all three loop-card packs, Six Sevens, Bruv, Like Terms Collector and Free Daily Pizza, pass every check as built, with the DRAFT badge following approval both ways; twenty-three planted faults caught (a duplicated answer, a back with no front, two loops in one deck, a card asking its own answer, a back not mirrored, text past the safe zone, a string-similar answer, a card from another deck, a long teacher step, no 6 × 7, a shout on the wrong card or back, a shout in Like Terms, a face without the web address, an 11-table card in SS-24, a 2-times card in SS-16, SS-32 with 8 cards off the core tables, a Free Daily Pizza value on two cards, a back asking for the form it gives, a front in the wrong form, FP-24 missing an S1 value, 0.33 printed for 1/3, an unapproved --final); no PDF is ever built in CI) |
# ci-deps: tools/loop-cards/ tools/pack-generator/ games/like-terms-collector/ games/free-daily-pizza/ scripts/bank_common.py scripts/plant_common.py scripts/escape_set_checks.py scripts/ci_shards.py scripts/fonts/ schools/assets/m_plus_logo.svg
"""CI's entry to the loop-card generator's self-test (contract SIX-SEVENS-WEIGHTING, 13 Nov 2026).

CI finds its lines only in scripts/*.py headers (scripts/ci-groups.py), and the generator lives in tools/loop-cards/,
so this file is the line and nothing more, on scripts/test-pack-generator.py's pattern: it runs
`build_deck.py --selftest` and returns its exit status. The self-test builds no PDF: the pack is the product, and
never a CI artifact.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "tools", "loop-cards", "build_deck.py")

if __name__ == "__main__":
    sys.exit(subprocess.call([sys.executable, "-X", "utf8", BUILD, "--selftest"]))
