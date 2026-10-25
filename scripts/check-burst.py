#!/usr/bin/env python3
# ci-line: Burst mode (canon 7.5.6: burst.js loaded once in each adopted game and nowhere else; a 5-answer burst in Chromium shows the return bar after the 5th answer only, with the right score in its link; no score or history written; nothing changes without ?burst; four planted faults caught) |
# ci-deps: schools/assets/burst.js schools/assets/firebase-leaderboard.js schools/assets/score-history.js scripts/check-answer-lock.py
"""Browser check for burst mode (contract BURST, 24 Oct 2026; canon 7.5.6; schools/assets/burst.js).

    python scripts/check-burst.py                    # every adopted game, then the plants
    python scripts/check-burst.py --no-plants
    python scripts/check-burst.py --game split-it    # one game

A burst is a short run launched from The 6 P's: /games/<slug>/?burst=5&from=six-ps&topic=<id>[&level=][&mode=].

  static    burst.js is loaded once, with `defer`, after analytics.js, by every adopted game and by no other game;
            a game that cannot be adopted (it reports no question_answered) is listed in NOT_ADOPTED with its reason
  play      each adopted game is opened with ?burst=5 at its first roster level (the game takes it: MaffsLevel.fromUrl) (and, where it has stage buttons, at
            a stage named by ?mode=: only that button is pressed), the answer-lock driver (check-answer-lock.py)
            plays five answers: no bar after the first four, the bar after the fifth, reading
            "That's 5. Back to The 6 P's (R of 5)", linking to /the-6-ps/?done=<topic>&r=R&n=5 where R is the number of
            right answers the page itself reported; controls at least 44 px; the page keeps room for the bar
  nothing   a burst session writes nothing: MaffsLeaderboard.submitScore returns at once (no initials overlay) and
            MaffsScoreHistory.record keeps nothing
  without   with no ?burst the page is untouched: no bar, mfg() not wrapped, MaffsBurst.active() false, and the
            page's DOM identical to the page with burst.js stubbed out

  plants    the bar after four answers; a score submitted in a burst; the right count miscounted; burst.js active
            without ?burst: each must FAIL
"""
import argparse
import asyncio
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402


def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


AL = _load("answer_lock", "check-answer-lock.py")

ADOPTED = """split-it better-value index-laws squared-squirrel linear-equation-solver sequence-solver angle-ace
negative-number-line free-daily-pizza factor-race how-many-parts distinctly-average take-a-walk think-of-a-number
trig-worms given-that simultaneous-solver shape-shifter like-terms-collector probability-pioneer formula-plug-in
standard-form-blitz quadratic-factoriser estimation-engine unit-converter component-crusher equation-builder
decimal-detective just-pythag-it-bruv formula-unlocked four-quadrant-explorer""".split()
# Named in the contract but not adopted: it never reports question_answered (non-scored, canon 9), so a shared module
# watching mfg() cannot count its answers and per-game counting is ruled out (Jon, 24 Oct 2026).
NOT_ADOPTED = {"constructions-lab": "reports no question_answered"}
# Staged games the contract names. A game with no [data-mode] stage buttons on its start screen cannot be opened at a
# stage by burst.js's shared ?mode= mechanism and is listed, not hacked.
STAGED = ["how-many-parts", "take-a-walk", "squared-squirrel", "free-daily-pizza", "simultaneous-solver"]
# Staged games whose stage buttons are not [data-mode] buttons (found by probing every declared level's start screen,
# 24 Oct 2026): burst.js presses [data-mode] only, so these open at their level, and a stage cannot be named. Listed, not hacked.
# BURST-STAGE (25 Oct 2026): the buttons of free-daily-pizza and simultaneous-solver are button[data-stage], opened by
# &stage= (checked in STAGE_CASES below), so they are no longer listed here.
NO_MODE = {
    "how-many-parts": "Foundation (ks3) stages are data-mode and work; Advanced (gcse) stages a-f are not buttons at all (list items)",
}
TOPIC = "fractions-add"
BURST = 5
WORKERS = 4
LINE = re.compile(r'^[ \t]*<script src="(?:\.\./\.\./|/)schools/assets/burst\.js" defer></script>\r?$', re.M)
ANALYTICS = re.compile(r'<script src="(?:\.\./\.\./|/)schools/assets/analytics\.js"[^>]*></script>')

# The answer-lock harness's page script, with its mfg recorder made safe for a wrapper: it logs the outermost call
# only (burst.js wraps window.mfg and calls through, and the harness's own recorder would otherwise run twice).
RECORDER_OLD = """  let real = null;
  Object.defineProperty(window, 'mfg', { configurable: true,
    get() { return function (e, p) {
      try { window.__lockEvents.push({ e: e, correct: p && p.correct, i: p && p.question_index, f: window.__lockFreshCalls }); } catch (x) {}
      if (typeof real === 'function') { try { return real.apply(this, arguments); } catch (x) {} }
    }; },
    set(v) { real = v; } });"""
RECORDER_NEW = """  let real = null, depth = 0;
  Object.defineProperty(window, 'mfg', { configurable: true,
    get() { const cur = real; const f = function (e, p) {
      if (!depth) { try { window.__lockEvents.push({ e: e, correct: p && p.correct, i: p && p.question_index, lv: p && p.level, f: window.__lockFreshCalls }); } catch (x) {} }
      depth++;
      try { if (typeof cur === 'function') { try { return cur.apply(this, arguments); } catch (x) {} } } finally { depth--; }
    }; f.__recorder = true; f.__inner = cur; return f; },
    set(v) { real = v; } });
  window.__modeClicks = [];
  window.addEventListener('click', function (e) {
    const b = e.target && e.target.closest ? e.target.closest('[data-mode]') : null;
    if (b) window.__modeClicks.push(b.getAttribute('data-mode'));
  }, true);"""


def init_script():
    src = AL.INIT
    assert RECORDER_OLD in src, "check-burst: the answer-lock page script changed; update RECORDER_OLD"
    return src.replace(RECORDER_OLD, RECORDER_NEW)


def static_faults(roster):
    out = []
    for slug in sorted(os.listdir(os.path.join(ROOT, "games"))):
        p = os.path.join(ROOT, "games", slug, "index.html")
        if not os.path.exists(p):
            continue
        html = open(p, encoding="utf-8").read()
        n = len(re.findall(r"burst\.js", html))
        if slug in ADOPTED:
            if n != 1 or not LINE.search(html):
                out.append("%s: burst.js must be loaded exactly once, as <script src=\".../schools/assets/burst.js\" defer></script> (found %d)" % (slug, n))
            else:
                a, b = ANALYTICS.search(html), LINE.search(html)
                if not a or a.start() > b.start():
                    out.append("%s: burst.js must come after analytics.js (it wraps mfg())" % slug)
        elif n:
            out.append("%s: loads burst.js but is not an adopted game (ADOPTED in scripts/check-burst.py)" % slug)
    for s in ADOPTED:
        if not os.path.exists(os.path.join(ROOT, "games", s, "index.html")):
            out.append("%s: adopted but has no page" % s)
    for s, why in NOT_ADOPTED.items():
        if s in ADOPTED:
            out.append("%s: on both ADOPTED and NOT_ADOPTED" % s)
    if not os.path.exists(os.path.join(ROOT, "schools", "assets", "burst.js")):
        out.append("schools/assets/burst.js is missing")
    return out


def url_for(base, slug, level, mode, burst=True):
    q = []
    if level:
        q.append("level=%s" % level)
    if burst:
        q += ["burst=%d" % BURST, "from=six-ps", "topic=%s" % TOPIC]
    if mode:
        q.append("mode=%s" % mode)
    return base + "/games/%s/" % slug + (("?" + "&".join(q)) if q else "")


async def new_ctx(browser, base, routes, init=True, **kw):
    ctx = await browser.new_context(**kw)
    await ctx.add_init_script(AL.CHECK_SITE.TIER3_INIT)
    if init:
        await ctx.add_init_script(init_script() % {"scale": AL.TIME_SCALE, "seed": AL.SEED})
    await ctx.route(lambda u: not u.startswith(base) and "/katex@" not in u, lambda r: r.abort())
    for pat, body, ctype in routes:
        def serve(b, c):
            return lambda route, *_: route.fulfill(status=200, content_type=c, body=b)
        await ctx.route(re.compile(pat), serve(body, ctype))
    return ctx


BAR = """() => { const b = document.getElementById('mfg-burst-bar'); if (!b) return null; const a = b.querySelector('a');
  const r = b.getBoundingClientRect(), ar = a ? a.getBoundingClientRect() : null;
  return { text: b.textContent, href: a ? a.getAttribute('href') : null, aw: ar ? ar.width : 0, ah: ar ? ar.height : 0,
           bottom: r.bottom, vh: innerHeight, pad: parseFloat(getComputedStyle(document.body).paddingBottom) || 0, h: r.height }; }"""


async def discover(browser, base, slug):
    """The mode this game is opened at (a [data-mode] stage button on its start screen, or None) and its level."""
    levels, _ = bc.roster_levels()
    lv = (levels.get(slug) or [None])[0]
    hint = AL.read_hint(open(os.path.join(ROOT, "games", slug, "index.html"), encoding="utf-8").read())[0]
    lv = hint.get("level", lv)
    ctx = await new_ctx(browser, base, [], init=False, viewport={"width": 1280, "height": 900})
    try:
        page = await ctx.new_page()
        await page.goto(url_for(base, slug, lv, None, burst=False), wait_until="load", timeout=20000)
        await page.wait_for_timeout(300)
        modes = await page.evaluate("() => Array.from(document.querySelectorAll('[data-mode]')).filter(b => b.offsetParent !== null).map(b => b.getAttribute('data-mode'))")
    finally:
        await ctx.close()
    mode = None
    if slug in STAGED and modes:
        mode = modes[1] if len(modes) > 1 else modes[0]      # a stage that is not the default
    return lv, mode, modes


async def play_burst(browser, base, slug, lv, mode, routes):
    f = []
    ctx = await new_ctx(browser, base, routes, viewport={"width": 1280, "height": 900})
    try:
        page = await ctx.new_page()
        await page.goto(url_for(base, slug, lv, mode), wait_until="load", timeout=20000)
        await page.wait_for_timeout(1200 if mode else 300)
        hint = AL.read_hint(open(os.path.join(ROOT, "games", slug, "index.html"), encoding="utf-8").read())[0]
        d = AL.Driver(page, slug, hint)
        if mode:
            clicks = await page.evaluate("() => window.__modeClicks")
            if clicks != [mode]:
                f.append("%s: ?mode=%s pressed %r, want exactly [%r]" % (slug, mode, clicks, mode))
        if not await d.start():
            return f + ["%s: UNPLAYABLE (no question reached)" % slug]
        if await page.evaluate("() => !!document.getElementById('mfg-burst-bar')"):
            f.append("%s: the bar is up before any answer" % slug)
        sn = None
        for k in range(BURST):
            s = None
            for attempt in range(14):         # a game may take several taps (sub-parts, a step to continue) to make one answer
                s = await d.answer(k * 14 + attempt, ms=1500)
                if s is not None:
                    break
                c = await d.ev("() => __lockContinue()")
                if c and c["ready"]:
                    await d.tap(c["rect"], False)
            if s is None:
                return f + ["%s: answer %d was not recorded (driver)" % (slug, k + 1)]
            sn = s
            bar = await page.evaluate(BAR)
            if k < BURST - 1:
                if bar:
                    f.append("%s: the bar is up after answer %d of %d" % (slug, k + 1, BURST))
                    break
                await d.to_next(s["lastFresh"])
            else:
                if not bar:
                    f.append("%s: no bar after answer %d" % (slug, BURST))
                    break
                right = s["correct"]
                want_text = "That's %d.Back to The 6 P's (%d of %d)" % (BURST, right, BURST)
                if bar["text"] != want_text:
                    f.append("%s: the bar reads %r, want %r" % (slug, bar["text"], want_text))
                want_href = "/the-6-ps/?done=%s&r=%d&n=%d" % (TOPIC, right, BURST)
                if bar["href"] != want_href:
                    f.append("%s: the bar links to %r, want %r" % (slug, bar["href"], want_href))
                if bar["ah"] < 44 or bar["aw"] < 44:
                    f.append("%s: the bar's link is %dx%d px, want at least 44" % (slug, bar["aw"], bar["ah"]))
                if bar["bottom"] < bar["vh"] - 1:
                    f.append("%s: the bar is not at the foot of the screen" % slug)
                if bar["pad"] < bar["h"] - 1:
                    f.append("%s: the page keeps no room for the bar (body padding %d < %d)" % (slug, bar["pad"], bar["h"]))
        dec = await page.evaluate("() => (window.MaffsLevel && MaffsLevel.declared) ? MaffsLevel.declared(%s) : null" % json.dumps(slug))
        if lv and (not dec or dec.get("fromUrl") is not True):
            f.append("%s: the game did not take ?level=%s from the link (MaffsLevel.declared: %r)" % (slug, lv, dec))
    finally:
        await ctx.close()
    return f


# A Firebase SDK that does nothing, so submitScore gets as far as asking for initials when nothing stops it.
FAKE_SDK = """window.firebase = { apps: [], initializeApp: function () { return {}; },
  database: function () { return { ref: function () { return { push: function () { return Promise.resolve(); },
    once: function () { return Promise.resolve({ val: function () { return null; } }); } }; } }; } };"""


async def nothing_written(browser, base, slug, lv, routes, control=False):
    """In a burst, submitScore returns at once (no initials overlay) and MaffsScoreHistory.record keeps nothing."""
    f = []
    ctx = await new_ctx(browser, base, routes, init=False, viewport={"width": 1280, "height": 900})
    await ctx.add_init_script(FAKE_SDK)
    try:
        page = await ctx.new_page()
        warns, errs = [], []
        page.on("console", lambda m: warns.append(m.text) if m.type == "warning" else None)
        page.on("pageerror", lambda e: errs.append(str(e)[:100]) if "onclick" not in str(e) else None)
        await page.goto(url_for(base, slug, lv, None, burst=not control), wait_until="load", timeout=20000)
        await page.wait_for_timeout(300)
        have = await page.evaluate("() => ({lb: !!(window.MaffsLeaderboard && MaffsLeaderboard.submitScore), h: !!(window.MaffsScoreHistory && MaffsScoreHistory.record)})")
        src = open(os.path.join(ROOT, "games", slug, "index.html"), encoding="utf-8").read()
        if errs:
            f.append("%s: page error: %s" % (slug, errs[0]))
        if "firebase-leaderboard.js" in src and not have["lb"]:
            f.append("%s: loads firebase-leaderboard.js but MaffsLeaderboard is not defined (the script failed?)" % slug)
        if "score-history.js" in src and not have["h"]:
            f.append("%s: loads score-history.js but MaffsScoreHistory is not defined (the script failed?)" % slug)
        if have["h"]:
            await page.evaluate("() => MaffsScoreHistory.record('%s', '%s', 7)" % (slug, lv or "all"))
            kept = await page.evaluate("() => Object.keys(localStorage).filter(k => k.indexOf('mfg_hist_v1') === 0).length")
            if (kept == 0) == control:
                f.append("%s: MaffsScoreHistory.record %s" % (slug, "kept a score in a burst" if control is False else "wrote nothing without a burst"))
        if have["lb"]:
            await page.evaluate("() => { window.__r = 'pending'; MaffsLeaderboard.submitScore('%s', '%s', 7, 7).then(r => { window.__r = r; }); }" % (slug, lv or "all"))
            await page.wait_for_timeout(250)
            overlay = await page.evaluate("() => !!document.getElementById('mfg-initials-overlay')")
            if control and not overlay:
                f.append("%s: control: submitScore without a burst did not ask for initials (the check cannot see it)" % slug)
            if not control:
                res = await page.evaluate("() => window.__r")
                if overlay:
                    f.append("%s: submitScore asked for initials in a burst (a score would be submitted)" % slug)
                if res == "pending" or res is None or res.get("percentile") is not None:
                    f.append("%s: submitScore did not return at once in a burst (%r)" % (slug, res))
                if not any("burst session" in w for w in warns):
                    f.append("%s: submitScore did not say why it submitted nothing" % slug)
    finally:
        await ctx.close()
    return f


async def untouched(browser, base, slug, lv, plant_routes):
    """With no ?burst the page is as if burst.js were not there."""
    f = []
    stub = [(r"/schools/assets/burst\.js(\?.*)?$", "window.MaffsBurst = { active: function () { return false; } };", "application/javascript")]
    snaps = []
    for routes in (plant_routes, stub):
        ctx = await new_ctx(browser, base, routes, viewport={"width": 1280, "height": 900})
        try:
            page = await ctx.new_page()
            await page.goto(url_for(base, slug, lv, None, burst=False), wait_until="load", timeout=20000)
            await page.wait_for_timeout(500)
            snaps.append(await page.evaluate("""() => ({
              html: document.documentElement.outerHTML, bar: !!document.getElementById('mfg-burst-bar'),
              active: !!(window.MaffsBurst && MaffsBurst.active()), wrapped: !!(window.mfg && (window.mfg.__maffsBurst || (window.mfg.__inner && window.mfg.__inner.__maffsBurst)))
            })"""))
        finally:
            await ctx.close()
    a, b = snaps
    if a["bar"]:
        f.append("%s: a bar without ?burst" % slug)
    if a["active"]:
        f.append("%s: MaffsBurst.active() is true without ?burst" % slug)
    if a["wrapped"]:
        f.append("%s: mfg() is wrapped without ?burst" % slug)
    if a["html"] != b["html"]:
        f.append("%s: the start screen differs from the page without burst.js" % slug)
    return f


async def run(games, routes, phases=("play", "nothing", "without"), control=True):
    from playwright.async_api import async_playwright
    proc, base = bc.start_stub_server()
    fails, listing = [], {}
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            sem = asyncio.Semaphore(WORKERS)

            async def one(slug):
                async with sem:
                    try:
                        lv, mode, modes = await discover(browser, base, slug)
                        listing[slug] = (lv, mode, modes)
                        out = []
                        if "play" in phases:
                            out += await asyncio.wait_for(play_burst(browser, base, slug, lv, mode, routes), 240)
                        if "nothing" in phases:
                            out += await nothing_written(browser, base, slug, lv, routes)
                        if "without" in phases:
                            out += await untouched(browser, base, slug, lv, routes)
                        return out
                    except Exception as e:
                        return ["%s: driver error: %s" % (slug, str(e).splitlines()[0][:140])]
            res = await asyncio.gather(*(one(s) for s in games))
            if control and "nothing" in phases and "split-it" in games:
                fails += await nothing_written(browser, base, "split-it", listing.get("split-it", (None,))[0], routes, control=True)
            await browser.close()
    finally:
        proc.terminate()
        proc.wait()
    for r in res:
        fails += r
    return fails, listing


# BURST-STAGE: &stage= presses button[data-stage="<value>"] (after &mode= when both are given). Each case loads the link,
# checks that exactly the wanted buttons were pressed and the page warned (or not) as stated, then presses the game's own
# Start button and reads the game's game_started event: its `mode` is the proof the game started at that stage.
# (slug, extra query, start button, buttons pressed, warnings, game_started mode)
STAGE_CASES = [
    ("free-daily-pizza", "stage=1", "startBtn", [], 0, "stage-s1-q20"),
    ("free-daily-pizza", "stage=2", "startBtn", [], 0, "stage-s2-q20"),
    ("free-daily-pizza", "stage=3", "startBtn", [], 0, "stage-s3-q20"),
    ("free-daily-pizza", "stage=4", "startBtn", [], 0, "stage-s4-q20"),
    ("free-daily-pizza", "stage=mixed", "startBtn", [], 0, "practice-q20"),   # mixed is the default pick: weak, but the press is checked below
    ("simultaneous-solver", "stage=stage4", "startBtn", [], 0, "stage4"),
    ("how-many-parts", "level=ks3&mode=stage3", "startBtn", ["stage3"], 0, "stage3"),
    ("how-many-parts", "level=ks3&mode=stage3&stage=none", "startBtn", ["stage3"], 1, "stage3"),
    ("free-daily-pizza", "stage=99", "startBtn", [], 1, "practice-q20"),
]
STAGE_INIT = """(function () {
  let real = null, depth = 0;
  window.__ev = []; window.__warns = []; window.__modeClicks = [];
  Object.defineProperty(window, 'mfg', { configurable: true,
    get() { const cur = real; const f = function (e, p) {
      if (!depth) { try { window.__ev.push({ e: e, p: p }); } catch (x) {} }
      depth++;
      try { if (typeof cur === 'function') { try { return cur.apply(this, arguments); } catch (x) {} } } finally { depth--; }
    }; return f; },
    set(v) { real = v; } });
  const w = console.warn; console.warn = function () { window.__warns.push(Array.prototype.join.call(arguments, ' ')); return w.apply(console, arguments); };
  window.addEventListener('click', function (e) {
    const b = e.target && e.target.closest ? e.target.closest('[data-mode]') : null;
    if (b) window.__modeClicks.push(b.getAttribute('data-mode'));
  }, true);
})();"""


async def stage_cases(browser, base, routes):
    f = []
    for slug, extra, start, want_modes, want_warns, want_mode in STAGE_CASES:
        ctx = await new_ctx(browser, base, routes, init=False, viewport={"width": 1280, "height": 900})
        try:
            await ctx.add_init_script(STAGE_INIT)
            page = await ctx.new_page()
            errs = []
            page.on("pageerror", lambda e: errs.append(str(e)))
            q = "burst=%d&from=six-ps&topic=%s&%s" % (BURST, TOPIC, extra)
            await page.goto(base + "/games/%s/?%s" % (slug, q), wait_until="load", timeout=20000)
            await page.wait_for_timeout(4200 if want_warns else 1500)
            tag = "%s ?%s" % (slug, extra)
            got = await page.evaluate("() => ({ modes: __modeClicks, warns: __warns.filter(w => w.indexOf('MaffsBurst') === 0) })")
            if got["modes"] != want_modes:
                f.append("%s: pressed data-mode %r, want %r" % (tag, got["modes"], want_modes))
            if len(got["warns"]) != want_warns:
                f.append("%s: %d MaffsBurst warnings %r, want %d" % (tag, len(got["warns"]), got["warns"], want_warns))
            if want_warns and got["warns"] and "stage=" not in got["warns"][0]:
                f.append("%s: the warning does not name the parameter: %r" % (tag, got["warns"][0]))
            await page.evaluate("(id) => document.getElementById(id).click()", start)
            await page.wait_for_timeout(600)
            ev = await page.evaluate("() => __ev.filter(x => x.e === 'game_started').map(x => x.p && x.p.mode)")
            if ev != [want_mode]:
                f.append("%s: game_started mode %r, want [%r]" % (tag, ev, want_mode))
            if errs:
                f.append("%s: page error %s" % (tag, errs[0][:100]))
        finally:
            await ctx.close()
    return f


async def run_stage(routes):
    from playwright.async_api import async_playwright
    proc, base = bc.start_stub_server()
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            try:
                return await stage_cases(browser, base, routes)
            finally:
                await browser.close()
    finally:
        proc.terminate()
        proc.wait()


def plants():
    js = open(os.path.join(ROOT, "schools", "assets", "burst.js"), encoding="utf-8").read()
    lb = open(os.path.join(ROOT, "schools", "assets", "firebase-leaderboard.js"), encoding="utf-8").read()

    def sub(src, old, new, what):
        assert old in src, "plant: %s not found" % what
        return src.replace(old, new, 1)
    bar4 = sub(js, "if (answered >= cfg.n) { shown = true; bar(); }", "if (answered >= cfg.n - 1) { shown = true; bar(); }", "the bar trigger")
    miscount = sub(js, "if (p && p.correct === true) right++;", "right++;", "the right count")
    always = sub(js, "var cfg = read();", "var cfg = read() || { n: 5, topic: 'x', mode: null };", "the cfg line")
    guard = lb[lb.index("    // BURST (24 Oct 2026)"):lb.index("    // LEVEL-RESOLVER")]
    submit = lb.replace(guard, "", 1)
    jsr = r"/schools/assets/burst\.js(\?.*)?$"
    lbr = r"/schools/assets/firebase-leaderboard\.js(\?.*)?$"
    mime = "application/javascript; charset=utf-8"
    nostage = sub(js, "if (!cfg.stage) return;", "return;", "the stage line")
    return [
        ("stage= ignored", [(jsr, nostage, mime)], None, ("stage",)),
        ("the bar after four answers", [(jsr, bar4, mime)], ["split-it"], ("play",)),
        ("a score submitted in a burst", [(lbr, submit, mime)], ["split-it"], ("nothing",)),
        ("the right count miscounted", [(jsr, miscount, mime)], ["split-it"], ("play",)),
        ("burst.js active without ?burst", [(jsr, always, mime)], ["split-it"], ("without",)),
    ]


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-plants", action="store_true")
    ap.add_argument("--game", nargs="*")
    a = ap.parse_args()
    AL.CHECK_SITE = AL.load_check_site()
    games = a.game or ADOPTED
    stat = static_faults(None)
    print("Burst mode (BURST): %d adopted games; not adopted: %s" % (len(ADOPTED), ", ".join("%s (%s)" % kv for kv in NOT_ADOPTED.items())))
    print("  %s  burst.js loaded once, after analytics.js, in exactly the adopted games%s" % ("FAIL" if stat else "ok  ", (": " + "; ".join(stat)) if stat else ""))
    fails, listing = asyncio.run(run(games, []))
    sf = asyncio.run(run_stage([]))
    print("  %s  &stage= presses button[data-stage] (%d cases: free-daily-pizza 1, 2, 3 and mixed, simultaneous-solver stage4, how-many-parts ?mode= unchanged, no match warns once)%s"
          % ("FAIL" if sf else "ok  ", len(STAGE_CASES), (":\n    " + "\n    ".join(sf)) if sf else ""))
    fails = fails + sf
    print("  %s  a %d-answer burst, nothing written, nothing changed without ?burst (%d games)%s"
          % ("FAIL" if fails else "ok  ", BURST, len(games), (":\n    " + "\n    ".join(fails[:40])) if fails else ""))
    for s, why in NO_MODE.items():
        print("  note  %s cannot be opened at a stage by ?mode=: %s" % (s, why))
    ok = not stat and not fails
    if not a.no_plants:
        for name, routes, subset, phases in plants():
            if phases == ("stage",):
                pf = asyncio.run(run_stage(routes))
            else:
                pf, _ = asyncio.run(run(subset, routes, phases, control=False))
            print("plant (%s): %s" % (name, ("CAUGHT: " + "; ".join(pf[:2])) if pf else "MISSED"))
            ok = ok and bool(pf)
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
