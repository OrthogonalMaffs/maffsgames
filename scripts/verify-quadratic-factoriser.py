#!/usr/bin/env python3
# ci-line: Quadratic Factoriser (every pooled item recomputed, SymPy) |
"""Layers C + D verification for quadratic-factoriser (docs/quadratic-factoriser-spec.md,
item 5). Grows with each build phase; this version covers Phase 1 ('gcse'), Phase 2
('higher') and Phase 3 ('formula').

WHY THIS READS THE LIVE PAGE, NOT A HAND-COPY OF THE POOL PARAMETERS
---------------------------------------------------------------------
The spec requires the pool to be "exported from the game as a JSON-able config, not
duplicated by hand" -- a Python re-implementation of the enumeration could drift from
the real one and would then be verifying itself, not the game. The game exposes its
pools on window.QF_POOLS after load (see games/quadratic-factoriser/index.html); this
script launches the stub server (CLAUDE.md's "ALWAYS use the stub server" rule),
loads the page under Playwright, reads window.QF_POOLS back, and checks THAT data
with SymPy.

WHAT "PER STAGE" MEANS HERE
----------------------------
docs/quadratic-factoriser-spec.md section 2.2 records the corrected floor: >= 40 items
per LEVEL (checked against the level's whole combined pool), not per stage. The
per-stage property that actually matters -- that a single session can never repeat a
question -- is asserted as what it reduces to under this game's sampling design
(one combined, deduplicated pool per level, shuffled and sliced without replacement,
exactly like `better-value`): the level's pool must contain no duplicate (a,b,c)
question. That single assertion is a stronger, always-sufficient guarantee than any
per-stage size floor, and it is what makes the 12-item DOTS stage safe without any
special-casing.

USAGE
-----
    python scripts/verify-quadratic-factoriser.py
"""
import asyncio
import math
import os
import sys

import sympy as sp
from urllib.parse import urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import bank_common as bc  # noqa: E402  (start_stub_server: checked start, free port)
SLUG = "quadratic-factoriser"
PORT = None  # set by main() to the free port the stub server got

_FAILURES = []


def fail(msg):
    _FAILURES.append(msg)
    print("FAIL: " + msg)


async def fetch_pools():
    from playwright.async_api import async_playwright

    base = "http://127.0.0.1:%d" % PORT
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        await page.goto(base + "/games/" + SLUG + "/?cb=verify", wait_until="load", timeout=20000)
        await page.wait_for_timeout(300)
        pools = await page.evaluate("() => window.QF_POOLS || null")
        await browser.close()
        return pools


def verify_gcse(level):
    x = sp.symbols("x")
    pool = level["pool"]
    stages = level["stages"]
    stage_order = level["stageOrder"]

    # C: every factorised form expands to its own quadratic.
    for item in pool:
        p, q, b, c = item["p"], item["q"], item["b"], item["c"]
        lhs = sp.expand((x + p) * (x + q))
        rhs = x**2 + b * x + c
        if sp.simplify(lhs - rhs) != 0:
            fail("gcse item p=%r q=%r does not expand to x^2+%rx+%r (got %s)"
                 % (p, q, b, c, lhs))

    # D: no duplicate (b,c) in the level's combined pool -- see module docstring for
    # why this is the real "no session ever repeats a question" guarantee under this
    # game's shuffle-the-whole-pool-then-slice sampling, and why it supersedes any
    # per-stage size floor.
    seen = {}
    for item in pool:
        key = (item["b"], item["c"])
        if key in seen:
            fail("gcse pool has duplicate (b,c)=%r (stages %r and %r)"
                 % (key, seen[key], item["stage"]))
        else:
            seen[key] = item["stage"]

    # Per-level floor (spec 2.2): the level's total pool, not any one stage.
    if len(pool) < 40:
        fail("gcse level pool has %d items, needs >= 40" % len(pool))

    # Stage sizes, reported for visibility, and the one pinned invariant: DOTS is an
    # exhaustive enumeration (k=1..12) and must stay exactly 12 -- not a floor, a check
    # that nothing accidentally changed its population.
    sizes = {name: len(stages.get(name, [])) for name in stage_order}
    print("  gcse stage sizes: %s (total %d)" % (sizes, len(pool)))
    if sizes.get("dots") != 12:
        fail("gcse dots stage has %d items, expected exactly 12 (k=1..12, its full "
             "exhaustive population)" % sizes.get("dots", -1))
    for name in ("bothPos", "oneNeg", "bothNeg"):
        if sizes.get(name, 0) == 0:
            fail("gcse stage %r is empty" % name)

    # Every stage's own (b,c) values must themselves already be unique -- if a stage
    # produced an internal duplicate the cross-stage check above wouldn't necessarily
    # catch it if two DIFFERENT items happened to collide only within one stage.
    for name in stage_order:
        stage_seen = set()
        for item in stages.get(name, []):
            key = (item["b"], item["c"])
            if key in stage_seen:
                fail("gcse stage %r has an internal duplicate (b,c)=%r" % (name, key))
            stage_seen.add(key)


def ac_splits(a, b, c):
    """Every unordered {m,n} with m*n = a*c and m+n = b -- re-derived independently in
    Python (not read from the game's own acSplits()), because this is exactly the
    property item 5 requires the verifier to prove from scratch."""
    ac = a * c
    out = set()
    bound = max(1, abs(ac))
    for m in range(-bound, bound + 1):
        if m == 0 or ac % m != 0:
            continue
        n = ac // m
        if m + n == b:
            out.add((m, n) if m <= n else (n, m))
    return out


def verify_higher(level):
    x = sp.symbols("x")
    pool = level["pool"]
    stages = level["stages"]
    stage_order = level["stageOrder"]

    for item in pool:
        p, q, r, s = item["p"], item["q"], item["r"], item["s"]
        a, b, c = item["a"], item["b"], item["c"]
        k = item.get("k") or 1

        # C: every factorised form expands to its own quadratic.
        lhs = sp.expand(k * (p * x + q) * (r * x + s))
        rhs = a * x**2 + b * x + c
        if sp.simplify(lhs - rhs) != 0:
            fail("higher item %r does not expand to %r (got %s)" % (item, rhs, lhs))

        # D: exactly one unordered {m,n} split with mn=ac, m+n=b -- the AC-method step 3
        # the tutorial teaches must have exactly one right answer.
        splits = ac_splits(a, b, c)
        if len(splits) != 1:
            fail("higher item %r has %d AC-splits (mn=ac, m+n=b), expected exactly 1: %r"
                 % (item, len(splits), splits))

        # D: no non-HCF (base) item has a common factor across a,b,c -- item 5's explicit
        # requirement, and the reason gcd(p,q)=gcd(r,s)=1 is imposed at generation time.
        if item["stage"] == "base":
            g = math.gcd(math.gcd(abs(a), abs(b)), abs(c))
            if g != 1:
                fail("higher base item %r has a common factor %d across a,b,c" % (item, g))

    # No duplicate (a,b,c) anywhere in the level's combined pool -- same "no session ever
    # repeats a question" guarantee as gcse (spec 2.2), checked across BOTH stages: a base
    # item and an HCF item could in principle expand to the same trinomial via a different
    # (p,q,r,s,k) (e.g. base p=2,r=6 and HCF k=2,p=1,r=6 both give a=12) even though no
    # such collision actually occurs in this parameter range (confirmed separately) --
    # this assertion is what would catch it if the parameters ever changed.
    seen = {}
    for item in pool:
        key = (item["a"], item["b"], item["c"])
        if key in seen:
            fail("higher pool has duplicate (a,b,c)=%r (stages %r and %r)"
                 % (key, seen[key], item["stage"]))
        else:
            seen[key] = item["stage"]

    if len(pool) < 40:
        fail("higher level pool has %d items, needs >= 40" % len(pool))

    sizes = {name: len(stages.get(name, [])) for name in stage_order}
    print("  higher stage sizes: %s (total %d)" % (sizes, len(pool)))
    for name in stage_order:
        if sizes.get(name, 0) == 0:
            fail("higher stage %r is empty" % name)


def _is_near_rounding_boundary(root):
    k = math.floor(root * 100 - 0.5 + 0.5)  # round-half-up, matching the game's Math.round
    boundary = (k + 0.5) / 100
    return abs(root - boundary) < 1e-6


def verify_formula(level):
    pool = level["pool"]
    stages = level["stages"]
    stage_order = level["stageOrder"]

    x = sp.symbols("x")
    for item in pool:
        a, b, c = item["a"], item["b"], item["c"]
        d = b * b - 4 * a * c
        true_roots = sp.solve(sp.Eq(a * x**2 + b * x + c, 0), x)
        true_roots = [complex(r) for r in true_roots]

        if d < 0:
            # D: negative-discriminant items are flagged as such.
            if not item["noReal"]:
                fail("formula item %r has d=%d (<0) but noReal is not true" % (item, d))
            if item["root1"] is not None or item["root2"] is not None:
                fail("formula item %r has d<0 but carries non-null roots" % item)
            if item["stage"] != "neg":
                fail("formula item %r has d<0 but stage=%r, expected 'neg'" % (item, item["stage"]))
            if any(abs(r.imag) < 1e-9 for r in true_roots):
                fail("formula item %r: SymPy found a real root for a claimed-negative discriminant" % item)
            continue

        if item["noReal"] or item["stage"] != "nonNeg":
            fail("formula item %r has d=%d (>=0) but noReal=%r stage=%r"
                 % (item, d, item["noReal"], item["stage"]))

        # C: every root matches SymPy's own root to 1e-9.
        game_roots = sorted([item["root1"], item["root2"]])
        sym_roots = sorted([r.real for r in true_roots])
        for gr, sr in zip(game_roots, sym_roots):
            if abs(gr - sr) > 1e-9:
                fail("formula item %r: game root %.12f vs SymPy root %.12f differ by more than 1e-9"
                     % (item, gr, sr))

        # D: no item sits on a rounding boundary.
        if _is_near_rounding_boundary(item["root1"]) or _is_near_rounding_boundary(item["root2"]):
            fail("formula item %r has a root within 1e-6 of a 2 d.p. rounding boundary" % item)

    # No duplicate (a,b,c) anywhere in the level's combined pool (spec 2.2's no-repeat
    # guarantee, same as gcse/higher).
    seen = set()
    for item in pool:
        key = (item["a"], item["b"], item["c"])
        if key in seen:
            fail("formula pool has duplicate (a,b,c)=%r" % (key,))
        seen.add(key)

    if len(pool) < 40:
        fail("formula level pool has %d items, needs >= 40" % len(pool))

    sizes = {name: len(stages.get(name, [])) for name in stage_order}
    neg_pct = 100.0 * sizes.get("neg", 0) / len(pool) if pool else 0
    print("  formula stage sizes: %s (total %d, %.1f%% negative discriminant)"
          % (sizes, len(pool), neg_pct))
    # Spec item 2: "~15% negative discriminant" -- a soft target, not an exact one; a wide
    # 10-20% band catches accidental drift (e.g. someone changing the curation thinning)
    # without being brittle to the exact count.
    if not (10.0 <= neg_pct <= 20.0):
        fail("formula pool's negative-discriminant share is %.1f%%, expected roughly 15%% "
             "(10-20%% band)" % neg_pct)
    for name in stage_order:
        if sizes.get(name, 0) == 0:
            fail("formula stage %r is empty" % name)

    # Spec item 2: "mostly non-square discriminants" among the real-root items.
    square_count = 0
    for item in stages.get("nonNeg", []):
        d = item["b"] * item["b"] - 4 * item["a"] * item["c"]
        if math.isqrt(d) ** 2 == d:
            square_count += 1
    nonneg_n = max(1, sizes.get("nonNeg", 0))
    square_pct = 100.0 * square_count / nonneg_n
    print("  formula perfect-square discriminant among real-root items: %d/%d (%.1f%%)"
          % (square_count, nonneg_n, square_pct))
    if square_pct > 50.0:
        fail("formula real-root items are %.1f%% perfect-square discriminant, expected a "
             "minority ('mostly non-square')" % square_pct)


def main():
    global PORT
    # A free port chosen per run; raises bc.StubServerError, naming the cause, if the
    # stub server cannot start.
    server, base = bc.start_stub_server()
    PORT = urlsplit(base).port
    try:
        pools = asyncio.run(fetch_pools())
    finally:
        server.terminate()

    if not pools:
        print("FAIL: could not read window.QF_POOLS from the live page")
        return 1

    if "gcse" in pools:
        print("Verifying 'gcse'...")
        verify_gcse(pools["gcse"])
    else:
        fail("window.QF_POOLS.gcse is missing")

    if "higher" in pools:
        print("Verifying 'higher'...")
        verify_higher(pools["higher"])
    else:
        fail("window.QF_POOLS.higher is missing")

    if "formula" in pools:
        print("Verifying 'formula'...")
        verify_formula(pools["formula"])
    else:
        fail("window.QF_POOLS.formula is missing")

    print()
    if _FAILURES:
        print("%d FAILURE(S)" % len(_FAILURES))
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
