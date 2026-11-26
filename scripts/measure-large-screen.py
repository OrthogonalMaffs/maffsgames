#!/usr/bin/env python3
"""Measure each MIGRATED page's height need and write data/large-screen.json (contract LARGE-SCREEN-LAYER, 26 Nov
2026). The file is this script's output and is never edited by hand; scripts/apply-large-screen.py copies each need
into the page's tag and scripts/check-large-screen.py holds the three in step.

    python -X utf8 scripts/measure-large-screen.py                     # every MIGRATED page
    python -X utf8 scripts/measure-large-screen.py --only base-60      # pages whose path holds this text (the rest kept)
    python -X utf8 scripts/measure-large-screen.py --workers 4

THE NEED is the height, in CSS px, a window must have for the page's answer controls on every question, and Next
after every answer, to end above the fold: the lowest bottom edge found, plus the pinned site footer where there is
one. Rule d of the layer (schools/assets/large-screen.js) keeps window height / zoom at or above it.

HOW IT IS MEASURED. With the layer's script not served (so nothing is zoomed), in Chromium with the real fonts, each
page is played to its results screen by scripts/check-large-screen.py's walk (the game's own lock-hint, wrong answers
three times in four), once for each of SEEDS (each seed plays different questions) at each window in a small grid:

  width   1200, the effective width the layer never goes below (rule b), so the narrowest and tallest layout a
          zoomed page is ever drawn at; and the first px of each of the page's own width regimes above 1200.
  height  the first px of each of the page's own height regimes from FLOOR to TOP: 600 itself, then T for every
          min-height:T (or height < T) and T + 1 for every max-height:T (or height > T) in between. Rule c keeps a
          zoomed page in the height regime of its real window, so each regime is measured where it is tightest: at
          its lowest height. (Content centred in a taller window ends lower on the page without needing more room;
          measuring at the regime's floor keeps that out of the number.)

The need is the largest reading over the grid. What it cannot see: a question no seed served, and a level or mode
other than the one the lock-hint starts. The check plays one more session per page, on a seed this never uses.
"""
import argparse
import asyncio
import importlib.util
import json
import math
import pathlib
import sys

BASE = pathlib.Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("check_large_screen", BASE / "scripts" / "check-large-screen.py")
cl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cl)

SEEDS = [1, 2, 3]
WIDTH, FLOOR, TOP, WIDE = 1200, 600, 1400, 2560
ABOUT = ("Written by scripts/measure-large-screen.py; never edit by hand. need: the height in CSS px each page's answer "
         "controls and Next need (schools/assets/large-screen.js, rule d).")


def regime_floors(facts, dim, lo, hi):
    """The first px of each of the page's own regimes of this dimension in (lo, hi], with lo itself."""
    out = {lo}
    for d, kind, t in facts["thresholds"]:
        if d != dim:
            continue
        b = math.ceil(t) if kind in ("ge", "lt") else math.floor(t) + 1
        if lo < b <= hi:
            out.add(b)
    return sorted(out)


async def measure(browser, base, rel, sem):
    facts = cl.page_facts(BASE, rel)
    widths, heights = regime_floors(facts, "width", WIDTH, WIDE), regime_floors(facts, "height", FLOOR, TOP)
    best = {"need": 0}
    counts = {"question": 0, "answered": 0, "wrong": 0, "sessions": 0}
    notes = []
    route = cl.route_for(BASE, rel)
    how = "ROUTES in check-large-screen.py" if rel in cl.ROUTES else ("the page's lock-hint" if route.get("answer") else "the generic driver")
    for w in widths:
        for h in heights:
            for seed in SEEDS:
                async with sem:
                    ctx, page = await cl.open_page(browser, base, rel, (w, h), seed, layer=False)
                    try:
                        async def on(kind, r, info, w=w, h=h, seed=seed):
                            if kind not in ("question", "answered") or r["bottom"] is None:
                                return
                            counts[kind] += 1
                            if kind == "answered" and info.get("correct") is False:
                                counts["wrong"] += 1
                            need = r["bottom"] + r["inset"]
                            if need > best["need"]:
                                best.update(need=need, what="the answer controls" if kind == "question" else "Next after an answer",
                                            question=info.get("q"), seed=seed, window=[w, h])
                        note = await cl.walk(page, BASE, rel, on)
                    finally:
                        await ctx.close()
                counts["sessions"] += 1
                if note:
                    notes.append("%dx%d seed %d: %s" % (w, h, seed, note))
    entry = {
        "need": int(math.ceil(best["need"] - 1e-6)),
        "thresholds": facts["thresholds"],
        "measured": {"how": how, "widths": widths, "heights": heights, "seeds": SEEDS, "sessions": counts["sessions"],
                     "questions": counts["question"], "answers": counts["answered"], "wrong_answers": counts["wrong"],
                     "tallest": {k: best[k] for k in ("what", "question", "seed", "window") if k in best}},
    }
    return rel, entry, notes


async def run(pages, workers):
    from playwright.async_api import async_playwright
    bc = cl.mpf().bc
    proc, base = bc.start_stub_server()
    try:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            sem = asyncio.Semaphore(workers)
            got = await asyncio.gather(*(measure(browser, base, rel, sem) for rel in pages))
            await browser.close()
    finally:
        proc.terminate()
    return got


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="pages whose path holds this text; the other entries are kept as they are")
    ap.add_argument("--workers", type=int, default=3)
    args = ap.parse_args()
    pages = [p for p in cl.MIGRATED if not args.only or args.only in p]
    if not pages:
        print("no MIGRATED page matches %r" % args.only)
        return 1
    old = cl.load_data(BASE)
    got = asyncio.run(run(pages, args.workers))
    bad = False
    for rel, entry, notes in got:
        m = entry["measured"]
        print("%s: need %d px (%s, question %s, seed %s, at %s); %d sessions, %d questions, %d answers (%d wrong); heights %s"
              % (rel, entry["need"], m["tallest"].get("what"), m["tallest"].get("question"), m["tallest"].get("seed"),
                 "x".join(map(str, m["tallest"].get("window", []))), m["sessions"], m["questions"], m["answers"], m["wrong_answers"], m["heights"]))
        for n in notes:
            print("  NOT MEASURED TO THE END: " + n)
            bad = True
        if entry["need"] <= 0:
            print("  NOTHING MEASURED")
            bad = True
    if bad:
        print("measure-large-screen: FAILED, %s not written" % cl.DATA)
        return 1
    pages_out = {rel: old[rel] for rel in cl.MIGRATED if rel in old}
    pages_out.update({rel: entry for rel, entry, _ in got})
    out = {"about": ABOUT, "pages": {rel: pages_out[rel] for rel in cl.MIGRATED if rel in pages_out}}
    with open(BASE / cl.DATA, "w", encoding="utf-8", newline="") as f:
        f.write(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print("measure-large-screen: wrote %s (%d pages)" % (cl.DATA, len(out["pages"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
