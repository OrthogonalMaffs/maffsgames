#!/usr/bin/env python3
# ci-line: B1 | Graph Transformer (BFS reachability + par verification) |
"""Verifies every Graph Transformer puzzle is solvable with its tier's buttons and
correctly parred (docs/snagging-list.md snag #7's par-verification pass, promoted
to CI so an unsolvable or misparred puzzle cannot ship again).

WHY THIS RUNS THE BFS INSIDE THE PAGE, NOT AS A PYTHON RE-IMPLEMENTATION
-------------------------------------------------------------------------------
A Python re-implementation of the button effects and the curve-match rule could
drift from the game and would then be verifying itself -- the same reasoning as
verify-log-laws.py / verify-distinctly-average.py. Instead games/graph-transformer/
index.html exports window.GT_VERIFY, whose bfsCheck(level, puzzlesOverride) runs a
breadth-first search using the tier's ACTUAL button definitions
(transformButtonDefs), the ACTUAL move-merging rule (mirroring recomputeMoveCount:
a run of consecutive clicks on the same mergeable button is one move; every other
click is its own move -- replayed by calling the real button closures against the
real `state` object), and the ACTUAL curve comparison (curvesMatch/evalState) for
the goal test. curveDupPairs(puzzles) flags two puzzles in a tier whose target
curves agree at every sample point, using the same tolerance rule curvesMatch
uses, generalised across a pair of (possibly different) base functions.

WHAT IT ASSERTS
-------------------------------------------------------------------------------
For every puzzle in every tier (gcse, alevel):
  - the target is reachable within MAX_MOVES (6 -- the largest known par is 4,
    so this leaves comfortable headroom without letting the search run away);
  - the stored par equals the BFS minimum exactly -- too low OR too high both fail.
And for every tier as a whole:
  - no two puzzles share an identical target curve, except a pair recorded in
    KNOWN_DUP_PAIRS below (tracked, not failed -- same pattern as
    scripts/checker-allowlist.json and verify-distinctly-average.py's
    SIGNATURE_ALLOWLIST: a stale entry that no longer reproduces is itself a
    failure, so the list cannot silently rot into a blanket exemption).

FAULT-INJECTION SELF-TEST
-------------------------------------------------------------------------------
Runs on every CI pass (--no-selftest skips it): clones a real A-level puzzle and
sets its amplitude to 3 (unreachable -- the only y-scale buttons are Stretch x2/
Stretch x1/2 in y, which only ever reach +/-2^n) and requires bfsCheck to report it
unreachable; clones another and mutates its stored par by +1 and requires bfsCheck
to report a par mismatch. Both go through bfsCheck's puzzlesOverride parameter, so
neither mutation ever touches the real bank or the file on disk.

USAGE
-------------------------------------------------------------------------------
    python scripts/verify-graph-transformer.py
    python scripts/verify-graph-transformer.py --no-selftest
"""
import argparse
import asyncio
import copy
import os
import sys
import time
from urllib.parse import urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import bank_common as bc  # noqa: E402  (start_stub_server: checked start, free port)
SLUG = "graph-transformer"
PORT = None  # set by main() to the free port the stub server got
LEVELS = ("gcse", "alevel")

# Known, reported-not-fixed duplicate-target pairs: (level, 0-indexed i, 0-indexed j) -> reason.
# Found by this script's own curveDupPairs check, not one of the three named puzzles this
# task fixed, so left as Jon's call (per the task's STOP IF) rather than fixed here.
KNOWN_DUP_PAIRS = {
    ("gcse", 10, 11): "x^3 is odd, so reflecting in the x-axis (a=-1, giving -x^3) and reflecting in "
                      "the y-axis (b=-1, giving (-x)^3 = -x^3) are the identical curve -- the same "
                      "reflect-x/reflect-y aliasing-on-an-odd-function class as the A-level match-check "
                      "bug fixed 29 Sep 2026 (docs/snagging-list.md #7), here showing up as a duplicate "
                      "puzzle rather than a wrongly-rejected route. Reported to Jon 29 Sep 2026 (this "
                      "session's par-verification build), tracked not fixed on his ruling.",
}

_FAILURES = []


def fail(msg):
    _FAILURES.append(msg)
    print("FAIL: " + msg)


async def run_bfs_on(page, lvl, puzzles):
    return await page.evaluate("(a) => window.GT_VERIFY.bfsCheck(a.l, a.p)", {"l": lvl, "p": puzzles})


async def run_selftest(page, all_puzzles):
    """Mutate one puzzle's amplitude to 3 (unreachable) and another's par by +1
    (mismatch), via bfsCheck's puzzlesOverride. The real bank is never touched."""
    ok = True
    lines = []
    lvl, pool = "alevel", all_puzzles["alevel"]

    amp = copy.deepcopy(pool[0])
    amp["target"]["a"] = 3
    res = (await run_bfs_on(page, lvl, [amp]))[0]
    caught = not res["reachable"]
    ok = ok and caught
    lines.append("  amplitude -> 3 on %-42s %s" %
                 (amp["desc"], "CAUGHT (unreachable)" if caught else "*** MISSED ***"))

    src = next((p for p in pool if p is not pool[0]), pool[0])
    par_item = copy.deepcopy(src)
    par_item["par"] = par_item["par"] + 1
    res2 = (await run_bfs_on(page, lvl, [par_item]))[0]
    caught2 = res2["reachable"] and res2["minMoves"] != par_item["par"]
    ok = ok and caught2
    lines.append("  par +1 on %-46s %s" %
                 (par_item["desc"], "CAUGHT (par mismatch)" if caught2 else "*** MISSED ***"))

    return ok, lines


async def run_all(no_selftest):
    from playwright.async_api import async_playwright

    base = "http://127.0.0.1:%d" % PORT
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        await page.goto(base + "/games/" + SLUG + "/?cb=verify%d" % int(time.time()),
                        wait_until="load", timeout=20000)
        await page.wait_for_function("!!window.GT_VERIFY", timeout=8000)

        results, all_puzzles, dup_pairs = {}, {}, {}
        for lvl in LEVELS:
            results[lvl] = await page.evaluate("(l) => window.GT_VERIFY.bfsCheck(l)", lvl)
            all_puzzles[lvl] = await page.evaluate("(l) => window.GT_VERIFY.allPuzzles(l)", lvl)
            dup_pairs[lvl] = await page.evaluate(
                "(l) => window.GT_VERIFY.curveDupPairs(window.GT_VERIFY.allPuzzles(l))", lvl)

        selftest_ok, selftest_lines = True, []
        if not no_selftest:
            selftest_ok, selftest_lines = await run_selftest(page, all_puzzles)

        await browser.close()
        return results, all_puzzles, dup_pairs, errors, selftest_ok, selftest_lines


def check_results(lvl, results):
    for i, r in enumerate(results):
        tag = "%s #%d (%s, %s)" % (lvl, i + 1, r["base"], r["desc"])
        if not r["reachable"]:
            fail("%s: target %r is UNREACHABLE with this tier's buttons (BFS bounded at %d moves)"
                 % (tag, r["target"], r["boundedAt"]))
            continue
        if r["minMoves"] != r["par"]:
            fail("%s: stored par %d != true minimum %d moves" % (tag, r["par"], r["minMoves"]))


def check_dups(lvl, puzzles, pairs):
    seen = set()
    for i, j in pairs:
        key = (lvl, i, j)
        seen.add(key)
        if key in KNOWN_DUP_PAIRS:
            print("  tracked, not failed: %s #%d/#%d share a target curve (%s...)"
                 % (lvl, i + 1, j + 1, KNOWN_DUP_PAIRS[key][:60]))
            continue
        fail("%s: puzzle #%d (%s) and #%d (%s) share an identical target curve"
             % (lvl, i + 1, puzzles[i]["desc"], j + 1, puzzles[j]["desc"]))
    for key in KNOWN_DUP_PAIRS:
        if key[0] == lvl and key not in seen:
            fail("KNOWN_DUP_PAIRS lists %s #%d/#%d but it no longer occurs -- remove the stale entry"
                 % key)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-selftest", action="store_true", help="skip the fault-injection self-test")
    args = ap.parse_args()

    global PORT
    # A free port chosen per run; raises bc.StubServerError, naming the cause, if the
    # stub server cannot start.
    server, base = bc.start_stub_server()
    PORT = urlsplit(base).port
    try:
        results, all_puzzles, dup_pairs, errors, selftest_ok, selftest_lines = asyncio.run(
            run_all(args.no_selftest))
    finally:
        server.terminate()

    for e in errors:
        fail("page error: " + e)

    for lvl in LEVELS:
        print("Verifying %s: %d puzzles" % (lvl, len(results[lvl])))
        check_results(lvl, results[lvl])
        check_dups(lvl, all_puzzles[lvl], dup_pairs[lvl])

    if not args.no_selftest:
        print()
        print("Fault-injection self-test (mutations must be caught; the real bank is never touched):")
        for ln in selftest_lines:
            print(ln)
        if not selftest_ok:
            fail("fault-injection self-test: at least one mutation was not caught")

    print()
    if _FAILURES:
        print("%d FAILURE(S)" % len(_FAILURES))
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
