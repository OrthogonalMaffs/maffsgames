#!/usr/bin/env python3
"""Cold-font sweep for the scroll-once fault class (SCROLL-REVEAL, 27 Oct 2026). Not run in CI: a report, run by hand.

For each game, at 375 x 667 (touch), with every font file held back until the answer is in, answer questions wrong and
right and read, after the fonts have arrived and the page has settled, whether the feedback's verdict and Next are in
view (above the fixed 40 px footer, below the top of the window). Run it against two trees to get before and after:

    python scripts/serve-stubbed.py 8765                          # this tree (after)
    python scripts/sweep-cold-font-scroll.py --base http://127.0.0.1:8765 --games the-6-ps,decimal-detective

The driver is measure-phone-fit.py's (its page scripts and answer routine are imported, not copied): it reaches
question 1 generically, then answers by whatever the question offers, alternating options so both verdicts turn up.
Each game gets --runs fresh browsers, because a font face is cold only the first time a page uses it.
"""
import argparse
import asyncio
import importlib.util
import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402


def load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


cs = load("check_site", "check-site.py")
pf = load("measure_phone_fit", "measure-phone-fit.py")

FOLD_PX = 40
GAMES = ["decimal-detective", "estimation-engine", "how-many-parts", "just-pythag-it-bruv", "squared-squirrel",
         "take-a-walk", "truth-buster", "screening-room", "simultaneous-solver"]

# Where the verdict and Next are, in page terms: the Next control the games share, or a continue-like button; the
# verdict is the first of these that is visible and not part of the question card.
READ_JS = r"""() => {
  const vis = el => { if (!el) return false; const r = el.getBoundingClientRect(), s = getComputedStyle(el);
    return r.width > 2 && r.height > 2 && s.display !== 'none' && s.visibility !== 'hidden'; };
  let next = [...document.querySelectorAll('.maffs-next')].find(vis);
  if (!next) next = [...document.querySelectorAll('button')].find(b => vis(b) && /^(next|continue|next question|keep going|start the questions|show the next step)/i.test((b.textContent || '').trim()));
  const verdict = [...document.querySelectorAll('.fb-verdict, .verdict, #feedback, #fb, [class*="fb-"]')].find(vis);
  const rect = el => { if (!el) return null; const r = el.getBoundingClientRect(); return { top: Math.round(r.top), bottom: Math.round(r.bottom) }; };
  return { next: rect(next), verdict: rect(verdict), nextLabel: next ? (next.textContent || '').trim().slice(0, 24) : '',
           fold: window.innerHeight - %d, y: Math.round(window.scrollY) };
}""" % FOLD_PX


def in_view(rect, fold):
    return bool(rect) and rect["top"] >= 0 and rect["bottom"] <= fold


async def one_run(browser, base, slug, seed):
    """One fresh cold browser: reach question 1, answer up to three questions, return the readings."""
    ctx = await browser.new_context(viewport={"width": 375, "height": 667}, has_touch=True, is_mobile=True)
    await ctx.add_init_script(cs.PHONE_SEED)
    await ctx.add_init_script(cs.TIER3_INIT)
    await ctx.add_init_script(pf.CORRECT_INIT)
    page = await ctx.new_page()
    released = asyncio.Event()
    held = []

    async def route(r):
        url = r.request.url
        try:
            if bc.is_font_cdn(url):
                got = bc.real_font_response(url)
                if not got:
                    return await r.abort()
                if "woff" in url or "ttf" in url:
                    held.append(url)
                    try:
                        await asyncio.wait_for(released.wait(), timeout=40)    # the font is cold until the answer is in
                    except asyncio.TimeoutError:
                        pass
                return await r.fulfill(**got)
            if cs.block_reason(url):
                return await r.abort()
            return await r.continue_()
        except Exception:
            pass
    await page.route("**/*", route)

    async def ev(js, arg=None):
        return await asyncio.wait_for(page.evaluate(js, arg), timeout=10)

    out = {"slug": slug, "answers": [], "note": "", "held": 0}
    try:
        slugpath = "the-6-ps/" if slug == "the-6-ps" else "games/%s/index.html" % slug
        cb = "?cb=%d%d" % (int(time.time() * 1000), random.randint(1000, 9999))
        await page.goto(base + "/" + slugpath + cb, wait_until="domcontentloaded", timeout=20000)
        await pf.settle(page)
        picked = False
        for _ in range(5):
            if (await ev("window.__mfgStats()"))["started"]:
                break
            if not picked and (await ev("window.__mfgProbe()"))["n"] >= 2:
                await ev("window.__mfgClickOpt(0)"); picked = True
            elif await ev("window.__mfgHasStart()"):
                await ev("window.__mfgClickStart()")
            elif (await ev("window.__mfgProbe()"))["n"] >= 2:
                await ev("window.__mfgClickOpt(0)")
            else:
                break
            await pf.settle(page)
        if not (await ev("window.__mfgStats()"))["started"]:
            try:
                hint = pf.declared_start(slug) if slug != "the-6-ps" else ""
                if hint:
                    await asyncio.wait_for(page.evaluate("async () => { %s }" % hint), timeout=15)
            except Exception:
                pass
        await pf.settle(page)
        for k in range(3):
            before = (await ev("window.__pfLastAnswer()"))["n"]
            got = False
            for phase in range(3):
                p = await ev("window.__mfgProbe()")
                if p["n"] >= 2:
                    await ev("(i) => window.__mfgClickOpt(i)", (seed + k + phase) % p["n"])
                    got = await mark(page, ev, before)
                    if got: break
                if await ev("window.__pfSubmit()"):
                    got = await mark(page, ev, before)
                    if got: break
                if await ev("window.__mfgHasInput()"):
                    await ev("(v) => window.__mfgTypeAnswer(v)", "1")
                    got = await mark(page, ev, before)
                    if got: break
                if p["n"] < 2 and not await ev("window.__mfgHasInput()"):
                    break
            if not got:
                out["note"] = "could not get answer %d marked" % (k + 1)
                break
            last = await ev("window.__pfLastAnswer()")
            released.set()                                    # the fonts arrive now, after the first scroll
            await page.wait_for_timeout(1800)
            await pf.settle(page)
            r = await ev(READ_JS)
            out["answers"].append({"correct": last["c"], "next_ok": in_view(r["next"], r["fold"]), "verdict_ok": r["verdict"] is None or r["verdict"]["top"] >= 0,
                                   "next": r["next"], "verdict": r["verdict"], "fold": r["fold"], "label": r["nextLabel"], "cold": k == 0})
            # on to the next question
            for _ in range(16):
                await page.wait_for_timeout(250)
                p2 = await ev("window.__mfgProbe()")
                if (await ev("window.__mfgStats()"))["completed"] or p2["atEnd"]:
                    break
                if p2["n"] >= 2 or await ev("window.__mfgHasInput()"):
                    break
                await ev("window.__mfgClickContinue()")
        out["held"] = len(held)
    except Exception as exc:
        out["note"] = "driver: " + str(exc).split("\n")[0][:90]
    finally:
        await ctx.close()
    return out


async def mark(page, ev, before, ms=2500):
    waited = 0
    while waited < ms:
        await page.wait_for_timeout(250)
        waited += 250
        if (await ev("window.__pfLastAnswer()"))["n"] > before:
            return True
    return False


async def main_async(a):
    from playwright.async_api import async_playwright
    games = a.games.split(",") if a.games else GAMES + ["the-6-ps"]
    rows = []
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        for g in games:
            runs = [await one_run(browser, a.base, g, s) for s in range(a.runs)]
            ans = [x for r in runs for x in r["answers"]]
            bad = [x for x in ans if not x["next_ok"] or not x["verdict_ok"]]
            right = sum(1 for x in ans if x["correct"] is True)
            wrong = sum(1 for x in ans if x["correct"] is False)
            cold = [x for x in ans if x["cold"]]
            notes = sorted({r["note"] for r in runs if r["note"]})
            held = max((r["held"] for r in runs), default=0)
            rows.append({"game": g, "answers": len(ans), "right": right, "wrong": wrong, "fails": len(bad),
                         "cold_fails": sum(1 for x in cold if not x["next_ok"] or not x["verdict_ok"]), "cold_answers": len(cold),
                         "font_files_held": held, "notes": notes, "bad": bad[:2]})
            r = rows[-1]
            print("%-22s answers %2d (right %d, wrong %d)  cold %d/%d bad  all %d bad  font files held %d  %s" % (
                g, r["answers"], right, wrong, r["cold_fails"], r["cold_answers"], r["fails"], held, "; ".join(notes)), flush=True)
            for b in r["bad"]:
                print("    e.g. next %s verdict %s fold %s (%s)" % (b["next"], b["verdict"], b["fold"], b["label"]), flush=True)
        await browser.close()
    if a.json:
        json.dump(rows, open(a.json, "w"), indent=1)
    return 1 if any(r["fails"] for r in rows) else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", required=True, help="a tree served by scripts/serve-stubbed.py, e.g. http://127.0.0.1:8765")
    ap.add_argument("--games", help="comma-separated slugs (default: the nine games and the-6-ps)")
    ap.add_argument("--runs", type=int, default=3, help="fresh cold browsers per game (default 3)")
    ap.add_argument("--json")
    return asyncio.run(main_async(ap.parse_args()))


if __name__ == "__main__":
    sys.exit(main())
