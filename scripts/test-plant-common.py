#!/usr/bin/env python3
# ci-line: Planted-fault helper (scripts/plant_common.py: a plant whose target is missing, repeated or unchanged is a STALE PLANT, an error is never a catch) |
"""Tests for scripts/plant_common.py (contract STALE-PLANTS, 28 Oct 2026). No browser.

    python scripts/test-plant-common.py
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plant_common as pc

bad = []


def case(name, ok):
    print("  %s  %s" % ("PASS" if ok else "FAIL", name))
    if not ok:
        bad.append(name)


def raises_stale(fn, *words):
    try:
        fn()
    except pc.StalePlant as exc:
        return str(exc).startswith("STALE PLANT: ") and all(w in str(exc) for w in words)
    except Exception:
        return False
    return False


SRC = "alpha beta beta gamma"
case("apply_plant: one occurrence is replaced", pc.apply_plant(SRC, "alpha", "ALPHA", "n") == "ALPHA beta beta gamma")
case("apply_plant: an absent target is a STALE PLANT naming the plant", raises_stale(lambda: pc.apply_plant(SRC, "delta", "x", "my plant"), "my plant", "not in the source"))
case("apply_plant: a repeated target is a STALE PLANT", raises_stale(lambda: pc.apply_plant(SRC, "beta", "x", "p"), "2 times"))
case("apply_plant: a repeated target is fine when allowed", pc.apply_plant(SRC, "beta", "B", "p", allow_multiple=True) == "alpha B B gamma")
case("apply_plant: new equal to old is a STALE PLANT", raises_stale(lambda: pc.apply_plant(SRC, "alpha", "alpha", "p"), "equals the original"))
case("apply_re_plant: a match is replaced", pc.apply_re_plant("a\n  grade: 4,\nb", r"\n  grade: \d+,", "", "p") == "a\nb")
case("apply_re_plant: no match is a STALE PLANT", raises_stale(lambda: pc.apply_re_plant("abc", r"\d+", "", "p"), "matches nothing"))
case("apply_re_plant: a match that changes nothing is a STALE PLANT", raises_stale(lambda: pc.apply_re_plant("abc", "b", "b", "p"), "changed nothing"))
case("is_caught: findings and no error is a catch", pc.is_caught(["x"], None) is True)
case("is_caught: findings WITH an error is not a catch", pc.is_caught(["the page broke"], "boom") is False)
case("is_caught: no findings is not a catch", pc.is_caught([], None) is False)
case("is_caught: an error alone is not a catch", pc.is_caught([], "boom") is False)


class Page:
    def __init__(self, exc=None):
        self.exc, self.seen = exc, []

    async def evaluate(self, code):
        self.seen.append(code)
        if self.exc:
            raise self.exc
        return 7

    def evaluate_sync(self, code):
        return None


async def js():
    ok_page, bad_page = Page(), Page(Exception("TypeError: Cannot read properties of undefined (reading 'x')\n at ..."))
    r = await pc.apply_js(ok_page, "p", "1+1")
    try:
        await pc.apply_js(bad_page, "B25 old pair", "q.x[0]=1")
    except pc.StalePlant as exc:
        return r == 7 and "STALE PLANT: B25 old pair" in str(exc) and "Cannot read properties" in str(exc)
    return False


case("apply_js: a patch that applies returns its value; one that throws is a STALE PLANT", asyncio.run(js()))
print("plant_common: %s" % ("FAILED: " + ", ".join(bad) if bad else "all green"))
sys.exit(1 if bad else 0)
