#!/usr/bin/env python3
# ci-line: Top scores panel (contract TOP-SCORES: the 11 panel games, played to their end with Firebase blocked in an en-US browser, each record kept by score-history.js; the panel shows the best five, British dates, no 0; five plants caught) | && --selftest
# ci-deps: schools/assets/score-history.js
"""The Chromium half of the top-scores check (contract TOP-SCORES, Jon, 25 Oct 2026; the rules and the static half
are in scripts/check-top-scores.py).

    python scripts/test-top-scores.py               # the panel games in Chromium
    python scripts/test-top-scores.py --game factor-race
    python scripts/test-top-scores.py --selftest    # each planted fault must fail

Locale en-US, the clock set to 25 Oct 2026, firebase-leaderboard.js blocked so window.MaffsLeaderboard is undefined;
KaTeX is served from the repo's copy (scripts/fonts/katex). Each panel game (PANEL in check-top-scores.py) is opened
and its own end-of-game function run once a session for the scores 30, 0, 50, 10, 40, 20, 10, 5 in turn (score set,
MaffsLock.newSession(), the function called):
  - every score is in its last-10 history (a game records whether or not Firebase loads);
  - after each game, its top key and the panel hold the best five scores so far above 0, highest first (after 30
    and 0: 30 alone; at the end 50, 40, 30, 20, 10), the 10 kept being the first one (a tie keeps the earlier);
  - #lbList ends with five rows, #1 to #5, those scores, each dated 25/10/2026.
Plants (--selftest), on percentage-flip: a zero stored and shown; a sixth-best score displacing the top five (the
newest five kept); a tie keeping the later score; the renderer's date in the browser's locale; the game's record()
back inside its Firebase check. Each must fail.
"""
import argparse
import asyncio
import importlib.util
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

_spec = importlib.util.spec_from_file_location("check_top_scores", os.path.join(HERE, "check-top-scores.py"))
CT = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(CT)
PANEL, ASSET = CT.PANEL, CT.ASSET

SEQ = [30, 0, 50, 10, 40, 20, 10, 5]
WANT = [50, 40, 30, 20, 10]
NOW_MS = 1792929600000            # 25 Oct 2026, 12:00 UTC
WANT_DATE = "25/10/2026"          # en-US would show 10/25/2026


def expected(scores):
    """The rule, independently: the best five scores above 0, highest first (a tie keeps the earlier: sorted is stable)."""
    return sorted((x for x in scores if x > 0), key=lambda x: -x)[:5]


CLOCK = """(() => { const real = Date.now.bind(Date); const off = %d - real(); Date.now = () => real() + off; })();""" % NOW_MS
PLAY = """async ([fn, seq]) => {
  const errs = [], steps = [];
  for (const s of seq) {
    try { MaffsLock.newSession(); score = s; window[fn] ? window[fn]() : eval(fn + '()'); }
    catch (e) { errs.push(s + ': ' + e.message); }
    await new Promise(r => setTimeout(r, 15));
    const t = Object.keys(localStorage).filter(k => k.indexOf('mfg_top_v1::') === 0).map(k => JSON.parse(localStorage.getItem(k)));
    steps.push({ top: t.length === 1 ? t[0].map(e => e.score) : null,
                 shown: Array.from(document.querySelectorAll('#lbList .lb-score')).map(c => c.textContent.trim()) });
  }
  const keys = Object.keys(localStorage);
  const read = p => keys.filter(k => k.indexOf(p) === 0).map(k => [k, JSON.parse(localStorage.getItem(k))]);
  const rows = Array.from(document.querySelectorAll('#lbList .lb-row')).map(r => Array.from(r.children).map(c => c.textContent.trim()));
  return { errs, steps, hist: read('mfg_hist_v1::'), top: read('mfg_top_v1::'), rows, lb: typeof window.MaffsLeaderboard };
}"""


KATEX = os.path.join(ROOT, "scripts", "fonts", "katex", "dist")


async def katex_local(route, *_):
    """KaTeX from the repo's own copy (scripts/fonts/katex), so a page renders with no CDN reached; else the CDN."""
    rel = route.request.url.split("/dist/", 1)[1].split("?")[0]
    p = os.path.normpath(os.path.join(KATEX, rel))
    if p.startswith(KATEX) and os.path.isfile(p):
        ctype = {".js": "application/javascript", ".css": "text/css", ".woff2": "font/woff2"}.get(os.path.splitext(p)[1], "application/octet-stream")
        await route.fulfill(status=200, content_type=ctype, body=open(p, "rb").read())
    else:
        await route.continue_()


async def play(browser, base, slug, routes=()):
    ctx = await browser.new_context(locale="en-US", timezone_id="Europe/London", viewport={"width": 1280, "height": 900})
    await ctx.add_init_script(CLOCK)
    await ctx.route(lambda u: not u.startswith(base) and "/katex@" not in u, lambda r: r.abort())
    await ctx.route(re.compile(r"/katex@[^/]+/dist/"), katex_local)
    await ctx.route(re.compile(r"/schools/assets/firebase-leaderboard\.js(\?.*)?$"), lambda r: r.abort())
    for pat, body, ctype in routes:
        def serve(b, c):
            return lambda route, *_: route.fulfill(status=200, content_type=c, body=b)
        await ctx.route(re.compile(pat), serve(body, ctype))
    page = await ctx.new_page()
    perr = []
    page.on("pageerror", lambda e: perr.append(str(e)))
    out = []
    try:
        await page.goto("%s/games/%s/?cb=%d" % (base, slug, int(time.time() * 1000)), wait_until="load", timeout=30000)
        fn = PANEL[slug]
        await page.wait_for_function("() => { try { return typeof %s === 'function' && !!window.MaffsLock; } catch (e) { return false; } }" % fn, timeout=15000)
        r = await page.evaluate(PLAY, [fn, SEQ])
    except Exception as e:
        await ctx.close()
        return ["%s: could not be played to its end: %s" % (slug, str(e).splitlines()[0])]
    await ctx.close()
    if r["lb"] != "undefined":
        out.append("%s: window.MaffsLeaderboard is defined with firebase-leaderboard.js blocked" % slug)
    if r["errs"]:
        out.append("%s: its end-of-game function threw: %s" % (slug, "; ".join(r["errs"][:2])))
    if len(r["hist"]) != 1:
        out.append("%s: %d score-history keys (want 1): a game records whether or not Firebase loads" % (slug, len(r["hist"])))
        return out
    hk, hist = r["hist"][0]
    if [e["score"] for e in hist] != SEQ[::-1]:
        out.append("%s: history %s, want %s (newest first)" % (slug, [e["score"] for e in hist], SEQ[::-1]))
        return out
    level = hk.split("::", 2)[2]
    tk = "mfg_top_v1::%s::%s" % (slug, level)
    top = dict(r["top"]).get(tk)
    if top is None:
        out.append("%s: no %s key" % (slug, tk))
        return out
    if [e["score"] for e in top] != WANT:
        out.append("%s: top key holds %s, want %s (best five, no 0)" % (slug, [e["score"] for e in top], WANT))
    first10 = [e["timestamp"] for e in hist if e["score"] == 10][-1]       # history is newest first
    tens = [e["timestamp"] for e in top if e["score"] == 10]
    if tens and tens[0] != first10:
        out.append("%s: the tied 10 kept is the later one (a tie keeps the earlier)" % slug)
    for i, st in enumerate(r["steps"]):
        want = expected(SEQ[:i + 1])
        if st["top"] != want or st["shown"] != [str(x) for x in want]:
            out.append("%s: after the scores %s the top key holds %s and the panel shows %s, want %s"
                       % (slug, SEQ[:i + 1], st["top"], st["shown"], want))
            break
    want_rows = [["#%d" % (i + 1), WANT_DATE, str(s)] for i, s in enumerate(WANT)]
    if r["rows"] != want_rows:
        out.append("%s: #lbList shows %s, want %s" % (slug, r["rows"], want_rows))
    if perr:
        out.append("%s: page error: %s" % (slug, perr[0][:120]))
    return out


async def run(games, routes=()):
    import bank_common as bc
    from playwright.async_api import async_playwright
    proc, base = bc.start_stub_server()
    fails = []
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            for slug in games:
                f = await play(browser, base, slug, routes)
                print("  %s  %s%s" % ("FAIL" if f else "ok  ", slug, (": " + "; ".join(f)) if f else ""))
                fails += f
            await browser.close()
    finally:
        proc.terminate()
    return fails


def _sub(src, old, new, what):
    assert src.count(old) == 1, "plant: %s not found exactly once" % what
    return src.replace(old, new)


def plants():
    js = open(os.path.join(ROOT, ASSET), encoding="utf-8").read()
    pf = open(os.path.join(ROOT, "games", "percentage-flip", "index.html"), encoding="utf-8").read()
    jsr, mime = r"/schools/assets/score-history\.js(\?.*)?$", "application/javascript; charset=utf-8"
    pgr, html = r"/games/percentage-flip/(\?.*)?$", "text/html; charset=utf-8"
    zero = _sub(_sub(js, "if (!(typeof score === 'number' && score > 0)) return;", "", "the zero guard"),
                "typeof e.score === 'number' && e.score > 0", "true", "the zero filter")
    newest = _sub(js, "localStorage.setItem(k, JSON.stringify(best(arr, TOP_N)));",
                  "localStorage.setItem(k, JSON.stringify(arr.slice(-TOP_N)));", "the top-five write")
    later = _sub(js, "(a.timestamp - b.timestamp)", "(b.timestamp - a.timestamp)", "the tie order")
    bare = _sub(js, "toLocaleDateString('en-GB')", "toLocaleDateString()", "the renderer's date")
    rec = "if(window.MaffsScoreHistory){MaffsScoreHistory.record('percentage-flip',gameLevel,score);}"
    sub_ = "MaffsLeaderboard.submitScore('percentage-flip',gameLevel,score,10).catch(function(){});"
    guarded = _sub(pf, rec + "if(window.MaffsLeaderboard){" + sub_ + "}",
                   "if(window.MaffsLeaderboard){" + sub_ + rec + "}", "percentage-flip's record call")
    return [
        ("a zero stored and shown", [(jsr, zero, mime)]),
        ("a sixth-best score displacing the top five", [(jsr, newest, mime)]),
        ("a tie keeping the later score", [(jsr, later, mime)]),
        ("the renderer's date in the browser's locale", [(jsr, bare, mime)]),
        ("record() only when Firebase loads", [(pgr, guarded, html)]),
    ]


def selftest():
    ok = True
    for name, routes in plants():
        f = asyncio.run(run(["percentage-flip"], routes))
        print("plant (%s): %s" % (name, ("CAUGHT: " + f[0][:160]) if f else "MISSED"))
        ok = ok and bool(f)
    print("selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--game", nargs="*")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    games = a.game or list(PANEL)
    print("Top scores in Chromium (TOP-SCORES): %d games, Firebase blocked, en-US, scores %s" % (len(games), SEQ))
    f = asyncio.run(run(games))
    print("PASS" if not f else "FAIL")
    return 1 if f else 0


if __name__ == "__main__":
    sys.exit(main())
