#!/usr/bin/env python3
"""Does each game fit a phone? A report with one gate (canon §7.6.1, the phone rule).

    python scripts/measure-phone-fit.py                 # every roster game -> docs/phone-fit-report.md
    python scripts/measure-phone-fit.py --aa            # the same in Aa (OpenDyslexic) mode
    python scripts/measure-phone-fit.py --laptop        # 1366x768 and 1280x720, normal mode (ruling R2)
    python scripts/measure-phone-fit.py --only new-shapes
    python scripts/measure-phone-fit.py --workers 6
    python scripts/measure-phone-fit.py --selftest      # the classification, planted cases (no browser)

THE GATE (canon 7.6.1; Jon's rulings of 26 Oct 2026): in normal mode at every size, and in Aa mode at 375x667 and
390x844, the LAST answer option must end above the fold, so a student never chooses from three of four options
without knowing it. In Aa mode at 320x568, the recorded exception (OpenDyslexic cannot fit a long GCSE prompt and
its feedback on that screen), the options must START above the fold, and an overflow beyond that is WARN.
--laptop (ruling R2): at 1366x768 and 1280x720, normal mode, the last answer option AND Next after a wrong answer
end above the fold. In every mode the page must not scroll sideways, on the asking screen or after a wrong answer.
A canvas question (no option group, input or submit) is measured by the canvas's own box and the buttons beside it.
The lists in scripts/phone-fit-state.json, per mode ("normal", "aa", "laptop"), grow only when the measurement itself
improves, with Jon's ruling, never because of a new fault: "known-failures" (each game with the entries at which it
fails the gate: reported, never failed), "sideways" (each game with the sizes at which it scrolls sideways) and
"unmeasurable" (the games this driver cannot measure, so they never read as passing). A failure not on its list, a
listed entry that now passes or now measures, and an unmeasurable game not on its list each make the run exit 1. On a
phone, Next below the fold is FAIL: reported, not a gate. Not run in CI yet (a later contract).

For every game on the roster, at 320x568, 375x667 and 390x844, it loads the game
(bare URL, so its default level), gets to the first question and records:

  ASKING  are the answer controls above the fold?  The controls are the option
          group tier 3 finds by behaviour (a keypad is a group too), plus a typed
          input and its submit control where the game has them.
  WRONG   after a wrong answer, is Next above the fold?  It answers until the
          game itself reports `question_answered` with `correct: false`, then
          looks for `.maffs-next` or a continue-like control (tier 3's rule).

The fold is the viewport height minus the fixed site footer, measured from the
top of the page: what a student sees without scrolling. It also records whether
the page scrolls sideways.

UNMEASURABLE is not a failure. It means the driver could not reach that state
(a drag game, a canvas, a second phase it cannot complete, or a wrong answer it
could not produce), exactly as tier 3's UNSUPPORTED. "no Next" means a wrong
answer was produced and no Next control appeared: the game auto-advances or
waits on something else, which is canon §7.6's business, not this report's.

What it cannot see: the on-screen keyboard over a native text input (headless
Chromium has none), any level but the default, and any question but the first
few. A pass here is a floor, not a warranty. Aa (OpenDyslexic) mode is measured
only when asked: --aa sets the shared toggle's stored preference (localStorage
`mfg_accessible`) before the page loads, so the game starts in Aa mode exactly
as it would for a student who had turned it on.

It reuses tier 3's page-side driver and its network guard from check-site.py, so
nothing it does can write to the Events sheet or the leaderboard. Two options
exist only for a sandbox that cannot reach the CDNs directly; CI needs neither:
--katex-dir serves cdn.jsdelivr.net's KaTeX 0.16.9 from a local copy of the npm
package's dist/, and --proxy-from-env routes Chromium through $HTTPS_PROXY
(which re-signs TLS, so certificate errors are ignored when it is used).
--chromium names a browser binary when Playwright's own build is not installed.
"""
import argparse
import asyncio
import datetime
import importlib.util
import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

_spec = importlib.util.spec_from_file_location("check_site", os.path.join(HERE, "check-site.py"))
cs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cs)

ROOT = bc.ROOT
SIZES = [(320, 568), (375, 667), (390, 844)]
LAPTOP_SIZES = [(1366, 768), (1280, 720)]   # ruling R2 (Jon, 26 Oct 2026): judged with --laptop, normal mode
KATEX_PREFIX = "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/"
DEFAULT_OUT = os.path.join(ROOT, "docs", "phone-fit-report.md")

# Runs after TIER3_INIT. Tier 3 records which event fired and its question index;
# this report also needs whether the answer was right, so mfg's accessor is
# replaced by one that records `correct` too. Same contract as tier 3's: whatever
# the page assigns to window.mfg is kept and still called.
CORRECT_INIT = r"""
(() => {
  // Timed changes still to come, for settle() (contract PHONE-FIT-DRIVER): a one-shot setTimeout of 200 ms to 5 s
  // (a section banner, a reveal, MaffsNext's floor) is pending until it fires or is cleared. A timer armed again by
  // its own callback with the same delay is a clock or an animation loop, not a change to wait for, and is ignored.
  const pendingTimers = new Map();
  let firingDelay = null;
  const oSet = window.setTimeout, oClear = window.clearTimeout;
  window.setTimeout = function (fn, delay) {
    const d = Number(delay) || 0;
    const chained = firingDelay !== null && firingDelay === d;
    const rest = Array.prototype.slice.call(arguments, 2);
    let id;
    const wrapped = function () {
      pendingTimers.delete(id);
      const prev = firingDelay; firingDelay = d;
      try { return typeof fn === 'function' ? fn.apply(this, rest) : (0, eval)(String(fn)); }
      finally { firingDelay = prev; }
    };
    id = oSet.call(window, wrapped, delay);
    if (d >= 200 && d <= 5000 && !chained) pendingTimers.set(id, Date.now() + d);
    return id;
  };
  window.clearTimeout = function (id) { pendingTimers.delete(id); return oClear.call(window, id); };
  window.__pfPending = function () {
    const now = Date.now(); let n = 0;
    pendingTimers.forEach(function (due, id) { if (due >= now - 50) n++; else pendingTimers.delete(id); });
    return n;
  };

  let real = null;
  try {
    Object.defineProperty(window, 'mfg', {
      configurable: true,
      get: function () {
        return function () {
          try {
            const d = arguments[1] || {};
            window.__mfgEvents.push({ e: arguments[0], i: d.question_index,
                                      c: (typeof d.correct === 'boolean') ? d.correct : null });
          } catch (err) {}
          if (typeof real === 'function') { try { return real.apply(this, arguments); } catch (err) {} }
        };
      },
      set: function (v) { real = v; }
    });
  } catch (err) {}

  window.__pfLastAnswer = function () {
    const ev = (window.__mfgEvents || []).filter(function (r) { return r.e === 'question_answered'; });
    return ev.length ? { n: ev.length, c: ev[ev.length - 1].c } : { n: 0, c: null };
  };

  function vis(el) {
    if (!el) return false;
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) return false;
    const s = getComputedStyle(el);
    return s.display !== 'none' && s.visibility !== 'hidden' && s.opacity !== '0';
  }
  function bottom(el) { return Math.round(el.getBoundingClientRect().bottom + window.scrollY); }
  function top(el) { return Math.round(el.getBoundingClientRect().top + window.scrollY); }
  function fold() {
    const f = document.querySelector('.site-footer');
    const fixed = f && getComputedStyle(f).position === 'fixed' && vis(f);
    return window.innerHeight - (fixed ? Math.round(f.getBoundingClientRect().height) : 0);
  }
  const SUBMIT_RE = /^(check|submit|answer|enter|go|calculate|confirm|done|finish)\b/;
  const CONTINUE_RE = /^(got it|next|continue|carry on|onward|ok|okay)\b/;
  function txt(el) { return (el.textContent || '').trim().replace(/\s+/g, ' ').toLowerCase(); }
  function clickables() {
    return [...document.querySelectorAll('button, a, [role="button"], input[type="submit"], input[type="button"]')]
      .filter(function (el) { return vis(el) && !el.closest('.site-footer, header'); });
  }

  // The answer controls on the asking screen, by tier 3's own reading of the page.
  window.__pfAsking = function () {
    window.__mfgProbe();
    const els = (window.__mfgGroup || []).filter(vis);
    document.querySelectorAll('input, textarea, [contenteditable="true"]').forEach(function (el) {
      const t = (el.getAttribute('type') || 'text').toLowerCase();
      if (el.disabled || el.readOnly || !vis(el)) return;
      if (el.tagName === 'INPUT' && ['text', 'number', 'tel', ''].indexOf(t) === -1) return;
      els.push(el);
    });
    clickables().forEach(function (el) {
      if (els.indexOf(el) === -1 && SUBMIT_RE.test(txt(el))) els.push(el);
    });
    // A canvas question (contract FOLD-COMPONENTS, Jon 26 Oct 2026): the answer is a tap on the canvas, so with no
    // option group, input or submit the canvas's own box is the answer area, with the controls next to it: every
    // visible button that starts at or below the canvas's top (Fire, Undo, Check), never a link or the header's.
    let canvas = false;
    if (!els.length) {
      const cv = [...document.querySelectorAll('canvas')].filter(function (el) { return vis(el) && !el.closest('.site-footer, header'); });
      if (cv.length) {
        canvas = true;
        const t0 = Math.min.apply(null, cv.map(top));
        cv.forEach(function (el) { els.push(el); });
        clickables().forEach(function (el) {
          if (el.tagName !== 'A' && els.indexOf(el) === -1 && top(el) >= t0) els.push(el);
        });
      }
    }
    return {
      n: els.length, canvas: canvas,
      bottom: els.length ? Math.max.apply(null, els.map(bottom)) : null,
      top: els.length ? Math.min.apply(null, els.map(top)) : null,
      fold: fold(),
      sw: document.documentElement.scrollWidth, vw: window.innerWidth
    };
  };

  // tier 3's __mfgClickSubmit skips the option group, because a submit inside a
  // group of answers is usually an answer. A keypad is the exception: its Enter
  // sits in the same grid as its digits (new-shapes, six-sevens-bruv). This one
  // looks everywhere, and is only used after a press has failed to be marked.
  window.__pfSubmit = function () {
    let hit = null;
    clickables().forEach(function (c) {
      if (!hit && !c.disabled && SUBMIT_RE.test(txt(c))) hit = c;
    });
    if (!hit) return '';
    hit.click();
    return (hit.textContent || '').trim().slice(0, 20);
  };

  // The layout's signature, for settle(): every visible control's box and the page's size. Text is left out on
  // purpose: a ticking clock changes text every second without moving anything a student must reach.
  window.__pfSig = function () {
    const parts = [document.documentElement.scrollHeight, document.documentElement.scrollWidth];
    document.querySelectorAll('button, a, input, select, textarea, canvas, svg, [role="button"]').forEach(function (el) {
      if (!vis(el)) return;
      const r = el.getBoundingClientRect();
      parts.push(Math.round(r.left) + ',' + Math.round(r.top + window.scrollY) + ',' + Math.round(r.width) + ',' + Math.round(r.height));
    });
    return parts.join('|');
  };

  // The start screen, reported, never judged (Jon's correction, 26 Oct 2026): where the level picker (the option
  // group tier 3 finds on the start screen) and the Start control end against the fold.
  window.__pfStart = function () {
    window.__mfgProbe();
    const picker = (window.__mfgGroup || []).filter(vis);
    const start = (window.__mfgStartEls ? window.__mfgStartEls() : []).filter(vis);
    const f = fold();
    return {
      picker: picker.length ? { n: picker.length, top: Math.min.apply(null, picker.map(top)), bottom: Math.max.apply(null, picker.map(bottom)), fold: f } : null,
      start: start.length ? { top: top(start[0]), bottom: bottom(start[0]), fold: f, label: (start[0].textContent || '').trim().slice(0, 20) } : null,
      fold: f, sw: document.documentElement.scrollWidth, vw: window.innerWidth
    };
  };

  window.__pfNext = function () {
    let el = document.querySelector('.maffs-next');
    if (!vis(el)) {
      el = null;
      const grp = window.__mfgGroup || [];
      clickables().forEach(function (c) {
        if (el || grp.indexOf(c) !== -1) return;
        const t = txt(c);
        if (CONTINUE_RE.test(t) || t.indexOf('next question') !== -1) el = c;
      });
    }
    return {
      found: !!el, bottom: el ? bottom(el) : null, fold: fold(),
      label: el ? (el.textContent || '').trim().slice(0, 30) : '',
      sw: document.documentElement.scrollWidth, vw: window.innerWidth
    };
  };
})();
"""


QUIET_MS, CEILING_MS, STEP_MS = 500, 5000, 100


def settle_point(samples, quiet=QUIET_MS, ceiling=CEILING_MS):
    """samples: [(t_ms, layout signature, timed changes pending), ...] in time order from the navigation. The time at
    which the layout has been unchanged for `quiet` ms with no timed change still due, with True; or the ceiling,
    with False (measured anyway). None: keep sampling. A banner that sits still for two seconds is stable to the eye
    and to the layout, so the pending timer that will remove it is what keeps the wait going. Pure, so --selftest
    plants a two-second banner through it."""
    last_change, prev = 0, object()
    for t, sig, pending in samples:
        if sig != prev:
            last_change, prev = t, sig
        if t - last_change >= quiet and not pending:
            return t, True
        if t >= ceiling:
            return t, False
    return None


async def settle(page):
    """Wait until the layout has been still for 500 ms with no timed change due (ceiling 5 s), sampling every 100 ms."""
    samples, t0 = [], time.monotonic()
    while True:
        try:
            sig, pending = await asyncio.wait_for(page.evaluate(
                "[window.__pfSig ? window.__pfSig() : '', window.__pfPending ? window.__pfPending() : 0]"), timeout=5)
        except Exception:
            sig, pending = None, 0
        samples.append((int((time.monotonic() - t0) * 1000), sig, pending))
        got = settle_point(samples)
        if got:
            return got
        await page.wait_for_timeout(STEP_MS)


# Why a game could not be measured, in the driver's own words: whether it started and what it could press.
SEEN_JS = r"""() => {
  const st = window.__mfgStats ? window.__mfgStats() : {};
  const vis = el => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
    return r.width > 2 && r.height > 2 && s.display !== 'none' && s.visibility !== 'hidden' && !el.closest('.site-footer, header'); };
  const seen = [...document.querySelectorAll('button, [role="button"], canvas, svg')].filter(vis)
    .map(el => el.tagName === 'CANVAS' ? 'a canvas' : el.tagName.toLowerCase() === 'svg' ? 'a drawing' :
         '"' + (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 24) + '"')
    .filter((x, i, a) => a.indexOf(x) === i).slice(0, 4);
  return (st.started ? 'started; ' : 'not started; ') + 'no option group, input or submit; it shows ' + (seen.join(', ') || 'nothing to press');
}"""


_spec_al = importlib.util.spec_from_file_location("check_answer_lock", os.path.join(HERE, "check-answer-lock.py"))
_al = None


def declared_start(slug):
    """The game's own 'start' from its maffs-lock-hint (canon 7.6.0), or ''. Read with check-answer-lock.py's parser."""
    global _al
    if _al is None:
        _al = importlib.util.module_from_spec(_spec_al)
        _spec_al.loader.exec_module(_al)
    with open(os.path.join(ROOT, "games", slug, "index.html"), encoding="utf-8") as fh:
        hint, faults = _al.read_hint(fh.read())
    return "" if faults else hint.get("start", "")


def roster_slugs():
    return [s for s in bc.roster_levels()[1]
            if os.path.isfile(os.path.join(ROOT, "games", s, "index.html"))]


async def measure_one(browser, base, slug, size, args):
    w, h = size
    out = {"slug": slug, "w": w, "h": h, "ask": None, "wrong": None, "note": ""}
    ctx = await browser.new_context(viewport={"width": w, "height": h},
                                    ignore_https_errors=bool(args.proxy_from_env))
    # Seeded as tier 1's phone pass is (cs.PHONE_SEED: Math.random from the page's own path), so every run measures the
    # same first question and two runs, such as --fonts real and --fonts fallback, compare cell by cell.
    await ctx.add_init_script(cs.PHONE_SEED)
    await ctx.add_init_script(cs.TIER3_INIT)
    await ctx.add_init_script(CORRECT_INIT)
    if args.aa:
        await ctx.add_init_script(AA_INIT)
    page = await ctx.new_page()
    escaped = []
    page.on("requestfinished", lambda r: escaped.append(r.url) if cs.is_write_host(r.url) else None)

    async def route(r):
        url = r.request.url
        try:
            # The fonts students see (FONT-FIT): KaTeX and Google Fonts from their pinned copies, never the network.
            # --fonts fallback is the old way, for comparison: Google Fonts blocked, KaTeX still real.
            if bc.is_font_cdn(url):
                if args.fonts == "fallback" and not url.startswith(bc.KATEX_CDN):
                    return await r.abort()
                got = bc.real_font_response(url)
                return await (r.fulfill(**got) if got else r.abort())
            if args.katex_dir and url.startswith(KATEX_PREFIX):
                p = os.path.join(args.katex_dir, url[len(KATEX_PREFIX):].split("?")[0])
                if os.path.isfile(p):
                    return await r.fulfill(path=p)
            if cs.block_reason(url):
                return await r.abort()
            return await r.continue_()
        except Exception:
            pass
    await page.route("**/*", route)

    async def ev(js, arg=None):
        return await asyncio.wait_for(page.evaluate(js, arg), timeout=10)

    try:
        cb = "?cb=%d%d" % (int(time.time() * 1000), random.randint(1000, 9999))
        await page.goto(base + "/games/%s/index.html%s" % (slug, cb),
                        wait_until="domcontentloaded", timeout=20000)
        try:
            await asyncio.wait_for(page.evaluate("document.fonts.ready.then(() => 1)"), timeout=8)
        except Exception:
            pass
        await settle(page)

        # The start screen, as it first shows, for the report (never judged): measured before anything is pressed.
        if not (await ev("window.__mfgStats()"))["started"]:
            await ev("window.scrollTo(0, 0)")
            out["start"] = await ev("window.__pfStart()")

        # Getting to question 1, generically (contract PHONE-FIT-DRIVER): the first level or option, then Start,
        # waiting for the layout to settle after every press, so a timed banner (the Core Maths papers' two-second
        # section card) is over before anything is measured.
        picked = False
        for _ in range(5):
            if (await ev("window.__mfgStats()"))["started"]:
                break
            if not picked and (await ev("window.__mfgProbe()"))["n"] >= 2:
                await ev("window.__mfgClickOpt(0)")
                picked = True
            elif await ev("window.__mfgHasStart()"):
                await ev("window.__mfgClickStart()")
            elif (await ev("window.__mfgProbe()"))["n"] >= 2:
                await ev("window.__mfgClickOpt(0)")
            else:
                break
            await settle(page)
        if not (await ev("window.__mfgStats()"))["started"]:
            try:
                await ev("typeof window.startGame === 'function' && window.startGame()")
            except Exception:
                pass
        await settle(page)

        await ev("window.scrollTo(0, 0)")
        ask = await ev("window.__pfAsking()")
        on_start = out.get("start") and out["start"].get("picker") and ask["n"] and ask.get("top") == out["start"]["picker"]["top"]
        hint = declared_start(slug)
        if (not ask["n"] or not (await ev("window.__mfgStats()"))["started"] or on_start) and hint:
            # The generic route reached no question; the page's own declared start (its maffs-lock-hint, canon 7.6.0).
            try:
                await asyncio.wait_for(page.evaluate("async () => { %s }" % hint), timeout=15)
            except Exception:
                pass
            await settle(page)
            await ev("window.scrollTo(0, 0)")
            ask = await ev("window.__pfAsking()")
            out["route"] = "declared start"
            on_start = out.get("start") and out["start"].get("picker") and ask["n"] and ask.get("top") == out["start"]["picker"]["top"]
        if on_start:
            # Still the start screen: what would be measured is the level picker, not a question.
            out["note"] = ("the start screen does not lead to a question generically (its first option, then %s); "
                           "no declared start" % ("'%s'" % out["start"]["start"]["label"] if out["start"].get("start") else "no Start control"))
            return out
        if not ask["n"]:
            out["note"] = await ev(SEEN_JS)
            return out
        out["ask"] = ask

        # A wrong answer, produced generically: answer by whatever the question
        # offers, read the game's own verdict, and on a right answer move on and
        # try a different option. Never more than five questions.
        for attempt in range(5):
            before = (await ev("window.__pfLastAnswer()"))["n"]
            probe = await ev("window.__mfgProbe()")

            async def marked(ms=2500):
                waited = 0
                while waited < ms:
                    await page.wait_for_timeout(250)
                    waited += 250
                    if (await ev("window.__pfLastAnswer()"))["n"] > before:
                        return True
                return False

            # A question may take more than one press before the game marks it:
            # a keypad wants digits then Enter, angle-ace wants the angle and then
            # the reason. Up to three phases, each answered by whatever it offers.
            got = False
            for phase in range(3):
                p = await ev("window.__mfgProbe()")
                if p["n"] >= 2:
                    await ev("(i) => window.__mfgClickOpt(i)", (attempt + 1 + phase) % p["n"])
                    if await marked():
                        got = True
                        break
                if await ev("window.__pfSubmit()"):
                    if await marked():
                        got = True
                        break
                if await ev("window.__mfgHasInput()"):
                    await ev("(v) => window.__mfgTypeAnswer(v)", "1")
                    if await marked():
                        got = True
                        break
                if p["n"] < 2 and not await ev("window.__mfgHasInput()"):
                    break
            if not got:
                out["note"] = "could not get an answer marked"
                break
            last = await ev("window.__pfLastAnswer()")
            if last["c"] is None:
                out["note"] = "the game does not report correct/incorrect"
                break
            if last["c"] is False:
                await settle(page)
                await ev("window.scrollTo(0, 0)")
                out["wrong"] = await ev("window.__pfNext()")
                break
            # Right by chance: carry on to the next question and try again.
            keys = probe["keys"]
            for _ in range(16):
                await page.wait_for_timeout(250)
                p2 = await ev("window.__mfgProbe()")
                if (await ev("window.__mfgStats()"))["completed"] or p2["atEnd"]:
                    break
                if (p2["n"] >= 2 and p2["keys"] != keys) or (not p2["n"] and await ev("window.__mfgHasInput()")):
                    break
                await ev("window.__mfgClickContinue()")
        else:
            out["note"] = "five answers, none wrong"
    except Exception as exc:
        out["note"] = "driver: " + str(exc).split("\n")[0][:90]
    finally:
        out["escaped"] = escaped
        await ctx.close()
    return out


def size_key(r):
    return "%dx%d" % (r["w"], r["h"])


def gate_sizes(rows, mode="normal"):
    """The entries at which a game fails THE GATE (canon 7.6.1, Jon's rulings of 26 Oct 2026). Phones (modes "normal"
    and "aa"): the LAST answer control must end above the fold, in normal mode at every size and in Aa mode at 375x667
    and 390x844; in Aa at 320x568, the recorded exception, the controls must START above the fold; an entry is the
    size, "320x568". Laptops (mode "laptop", ruling R2): at 1366x768 and 1280x720 the last answer control AND Next after
    a wrong answer end above the fold; an entry is the size and the control, "1280x720 option" or "1280x720 next".
    A size whose asking screen was not reached is not judged here (UNMEASURABLE is the game-level case)."""
    out = []
    for r in rows:
        a = r["ask"]
        if not a:
            continue
        if mode == "laptop":
            if a["bottom"] > a["fold"]:
                out.append(size_key(r) + " option")
            n = r["wrong"]
            if n and n.get("found") and n["bottom"] > n["fold"]:
                out.append(size_key(r) + " next")
            continue
        if mode == "aa" and r["w"] == 320:
            bad = a.get("top") is not None and a["top"] > a["fold"]
        else:
            bad = a["bottom"] > a["fold"]
        if bad:
            out.append(size_key(r))
    return out


def sideways_sizes(rows):
    """The sizes at which the page scrolls sideways, on the asking screen or after a wrong answer (contract
    FOLD-COMPONENTS, Jon 26 Oct 2026: a gate in every mode, with its own list). The start screen is report-only (R4)."""
    return [size_key(r) for r in rows
            if any(m and m["sw"] > m["vw"] for m in (r["ask"], r["wrong"]))]


def classify(rows, mode="normal", known=(), unmeasurable_listed=False, sideways=()):
    """One game's sizes in one mode -> (status, severity, detail).

    THE GATE (gate_sizes) and SIDEWAYS SCROLL (sideways_sizes), each against its own list in phone-fit-state.json. A
    failure not on the game's list is HARD_FAIL; a listed entry that now passes is STALE (take it off: the lists only
    shrink, canon 7.6.1); failures that are all listed are KNOWN_FAIL, reported, never failed. A game the driver cannot
    measure must be on the unmeasurable list (UNMEASURABLE), or it is UNMEASURABLE_NEW: it never reads as passing.
    HARD_FAIL, STALE and UNMEASURABLE_NEW make the run exit 1. On a phone, Next below the fold is FAIL: reported, not a
    gate (on a laptop it is the gate). In Aa at 320x568 an overflow that keeps the options starting above the fold is
    WARN (Aa at 320)."""
    known, sideways = set(known or ()), set(sideways or ())
    aa = mode == "aa"
    asks = [r for r in rows if r["ask"]]
    wrongs = [r for r in rows if r["wrong"]]
    if not asks:
        why = rows[0]["note"] or "asking screen not reached"
        if known or sideways:
            return STALE, -10 ** 3, "unmeasurable, but on a known-failures list: take it off (the lists only shrink)"
        if unmeasurable_listed:
            return UNMEASURABLE, -10 ** 7, why
        return UNMEASURABLE_NEW, -10 ** 3, why + " (not on the unmeasurable list: it never reads as passing)"
    if unmeasurable_listed:
        return STALE, -10 ** 3, "measured, but on the unmeasurable list: take it off (the lists only shrink)"

    by = {size_key(r): r for r in rows}
    canvas = " (a canvas: its box and the controls beside it)" if any(r["ask"].get("canvas") for r in asks) else ""

    def edge(k):
        size, _, what = k.partition(" ")
        r = by[size]
        if what == "next":
            return "%s (Next %d / %d)" % (size, r["wrong"]["bottom"], r["wrong"]["fold"])
        a = r["ask"]
        if aa and r["w"] == 320:
            return "%s (options start %d / %d)" % (size, a["top"], a["fold"])
        return "%s (last option %d / %d)" % (size, a["bottom"], a["fold"])

    def over(k):
        size, _, what = k.partition(" ")
        m = by[size]["wrong"] if what == "next" else by[size]["ask"]
        return m["bottom"] - m["fold"]
    gate, side = gate_sizes(rows, mode), sideways_sizes(rows)
    sev = max([over(k) for k in gate] + [0])
    new = [k for k in gate if k not in known]
    new_side = [k for k in side if k not in sideways]
    if new or new_side:
        parts = (["below the fold, not on the known-failures list: " + ", ".join(edge(k) for k in new)] if new else []) + (
            ["scrolls sideways, not on the sideways list: " + ", ".join(new_side)] if new_side else [])
        return HARD_FAIL, sev, "; ".join(parts) + canvas
    stale = sorted(known - set(gate))
    stale_side = sorted(sideways - set(side))
    if stale or stale_side:
        parts = (["on the known-failures list at %s but passes there" % ", ".join(stale)] if stale else []) + (
            ["on the sideways list at %s but does not scroll sideways there" % ", ".join(stale_side)] if stale_side else [])
        return STALE, -10 ** 3, "; ".join(parts) + ": take it off (the lists only shrink)"
    if gate or side:
        parts = (["known failure: " + ", ".join(edge(k) for k in gate)] if gate else []) + (
            ["known sideways scroll: " + ", ".join(side)] if side else [])
        return KNOWN_FAIL, sev, "; ".join(parts) + canvas

    scrolls = lambda r: aa and r["w"] == 320           # canon 7.6.1: Aa at 320 x 568 may scroll
    over_next = [r["wrong"]["bottom"] - r["wrong"]["fold"] for r in wrongs if r["wrong"]["found"] and not scrolls(r)]
    warn = [r for r in rows if scrolls(r) and ((r["ask"] and r["ask"]["bottom"] > r["ask"]["fold"]) or
            (r["wrong"] and r["wrong"]["found"] and r["wrong"]["bottom"] > r["wrong"]["fold"]))]
    worst = max(over_next + [-10 ** 6])
    if any(o > 0 for o in over_next):
        return "FAIL", max(worst, 0), "Next below fold" + canvas
    if warn:
        return WARN_AA, -10 ** 4, "Aa at 320x568 scrolls; the options start above the fold"
    if len(wrongs) < len(rows):
        return "PASS (asking only)", -10 ** 6, (next((r["note"] for r in rows if r["note"]), "") + canvas).strip()
    if not over_next:
        return "PASS (no Next)", -10 ** 5, "wrong answer shows no Next control" + canvas
    return "PASS", worst, canvas.strip()


def cell(m, key="bottom"):
    if not m:
        return "–"
    if m.get("found") is False:
        return "no Next"
    v = m[key] - m["fold"]
    return "%d / %d %s" % (m[key], m["fold"], "✗" if v > 0 else "✓")


HARD_FAIL = "HARD FAIL"
STALE = "STALE (take it off the list)"
UNMEASURABLE_NEW = "UNMEASURABLE (not listed)"
KNOWN_FAIL = "KNOWN FAIL"
UNMEASURABLE = "UNMEASURABLE"
WARN_AA = "WARN (Aa at 320)"
GATE_FAILS = (HARD_FAIL, STALE, UNMEASURABLE_NEW)

# The two lists that may only shrink (canon 7.6.1, Jon's ruling of 26 Oct 2026), per mode: "known-failures" maps a
# game to the sizes at which it fails the gate; "unmeasurable" lists the games the driver cannot measure.
STATE = os.path.join(HERE, "phone-fit-state.json")


def load_state(mode):
    """(known failures, unmeasurable games, sideways list) for one mode: "normal", "aa" or "laptop"."""
    with open(STATE, encoding="utf-8") as fh:
        st = json.load(fh)
    return st["known-failures"][mode], set(st["unmeasurable"][mode]), st["sideways"][mode]

# --aa: the stored preference every game's Aa toggle reads on load.
AA_INIT = "try { localStorage.setItem('mfg_accessible', 'true'); } catch (e) {}"


BELOW_REPORT = "BELOW FOLD (report)"


def write_report(results, path, elapsed, mode="normal", only=None, sizes=None, report=False):
    """report=True (--sizes, not the canon sizes): nothing is judged against the lists and nothing fails the run."""
    sizes = sizes or SIZES
    aa = mode == "aa"
    known, unmeasurable, sideways = ({}, set(), {}) if report else load_state(mode)
    by = {}
    for r in results:
        by.setdefault(r["slug"], []).append(r)
    games = []
    # A list entry for a game no longer on the roster is stale too (a full run only).
    for slug in sorted((set(known) | unmeasurable | set(sideways)) - set(by)) if not only else []:
        games.append((STALE, -10 ** 3, slug, [], "on a phone-fit list but not measured (not on the roster): take it off"))
    for slug, rows in by.items():
        rows.sort(key=lambda r: r["w"])
        st, sev, detail = classify(rows, mode, known.get(slug, ()), slug in unmeasurable, sideways.get(slug, ()))
        if report:
            st = {HARD_FAIL: BELOW_REPORT, UNMEASURABLE_NEW: UNMEASURABLE}.get(st, st)
        games.append((st, sev, slug, rows, detail))
    order = {HARD_FAIL: -4, BELOW_REPORT: -4, STALE: -3, UNMEASURABLE_NEW: -2, KNOWN_FAIL: -1, "FAIL": 0, WARN_AA: 1, "PASS (no Next)": 2,
             "PASS (asking only)": 3, "PASS": 4, UNMEASURABLE: 5}
    games.sort(key=lambda g: (order[g[0]], -g[1], g[2]))

    counts = {}
    for g in games:
        counts[g[0]] = counts.get(g[0], 0) + 1
    lines = [
        "# Phone fit report",
        "",
        "Generated by `scripts/measure-phone-fit.py` on %s (%d games, %.0f min). **A report, with two gates** (canon §7.6.1,"
        " Jon's rulings of 26 Oct 2026): the last answer option ends above the fold (Aa at 320: the options start above it;"
        " on a laptop, Next after a wrong answer too), and the page never scrolls sideways. A failure"
        " not on its list in `scripts/phone-fit-state.json` (HARD FAIL), a listed entry that now passes"
        " (STALE) or an unmeasurable game not on its list makes the run exit 1; KNOWN FAIL is reported, never failed."
        % (datetime.date.today().isoformat(), len(games), elapsed / 60),
        "The standard is canon §7.6.1, the phone rule. Regenerate it with the same command; do not edit it by hand.",
        "",
    ] + (["**Aa (OpenDyslexic) mode on** (`--aa`).", ""] if aa else []) + (
        ["**Laptop and projector sizes** (`--laptop`, ruling R2): the last answer option and Next both end above the fold.", ""]
        if mode == "laptop" else []) + (
        ["**Report mode** (`--sizes`): measured at %s, judged against nothing; nothing here fails the run." %
         ", ".join("%d×%d" % sz for sz in sizes), ""] if report else []) + [
        "Each cell is `bottom edge / fold` in CSS pixels from the top of the page, ✓ above the fold, ✗ below it.",
        "The fold is the viewport height minus the fixed site footer (40px; a page without one keeps the full",
        "height). **Asking**: the lowest answer control",
        "(option group, keypad, typed input and its submit) on the first question. **Wrong**: the Next control after",
        "the first wrong answer the driver could produce. `no Next` means a wrong answer was produced and no Next",
        "control appeared (the game auto-advances or waits on something else). `–` means the driver could not reach",
        "that state: **UNMEASURABLE is not a failure**, it is the edge of what a generic driver can do (tier 3's rule).",
        "",
        "Each size loads the game afresh, so a game that shuffles is measured on a different first question at each",
        "size: one sample, not every question. Not measured: the on-screen keyboard over a native text input,",
        "any level but the default, Aa mode unless `--aa` is given. Worst first: FAIL rows are ordered by how far past the fold the worst edge is;",
        "a game that only scrolls sideways comes after them.",
        "",
        "| Status | Count |", "|---|---|",
    ]
    for k in sorted(counts, key=lambda k: order[k]):
        lines.append("| %s | %d |" % (k, counts[k]))
    szs = ["%d×%d" % sz for sz in sizes]
    lines += ["", "| Game | Status | " + " | ".join("Asking " + z for z in szs) + " | " + " | ".join("Wrong " + z for z in szs)
              + " | Sideways at %d | Notes |" % sizes[0][0], "|---|---|" + "---|" * (2 * len(szs)) + "---|---|"]
    for st, sev, slug, rows, detail in games:
        side = "–"
        for r in rows:
            if r["w"] != sizes[0][0]:
                continue
            ms = [m for m in (r["ask"], r["wrong"]) if m]
            if ms:
                side = "**yes**" if any(m["sw"] > m["vw"] for m in ms) else "no"
        cells = (["`%s`" % slug, st] + ([cell(r["ask"]) for r in rows] or ["–"] * len(szs))
                 + ([cell(r["wrong"]) for r in rows] or ["–"] * len(szs)) + [side, detail.replace("|", "/")])
        lines.append("| " + " | ".join(cells) + " |")

    # The start screen, measured and reported, never judged (Jon's correction to PHONE-FIT-DRIVER, 26 Oct 2026: a
    # start-screen rule is his to rule on). A game that opens straight on its first question has no row.
    starts = [(g[2], g[3]) for g in games if any(r.get("start") for r in g[3])]
    lines += ["", "## Start screen (report only: no pass or fail until Jon rules on a start-screen rule)", "",
              "Where the level picker (the option group on the start screen, if any) and the Start control end, as "
              "`bottom edge / fold`, before anything is pressed. `–`: none on that screen.", "",
              "| Game | " + " | ".join("Picker " + z for z in szs) + " | " + " | ".join("Start " + z for z in szs) + " |",
              "|---|" + "---|" * (2 * len(szs))]
    for slug, rows in sorted(starts):
        lines.append("| `%s` | " % slug + " | ".join(cell((r.get("start") or {}).get("picker")) for r in rows) + " | "
                     + " | ".join(cell((r.get("start") or {}).get("start")) for r in rows) + " |")
    with open(path, "w", encoding="utf-8", newline='') as fh:
        fh.write("\n".join(lines) + "\n")
    return games


async def run(args):
    from playwright.async_api import async_playwright
    slugs = roster_slugs()
    if args.only:
        slugs = [s for s in slugs if s == args.only]
        if not slugs:
            sys.exit("no roster game named %r" % args.only)
    proc, base = bc.start_stub_server()
    t0 = time.time()
    try:
        async with async_playwright() as p:
            launch = {}
            if args.proxy_from_env:
                launch["proxy"] = {"server": os.environ["HTTPS_PROXY"], "bypass": "127.0.0.1,localhost"}
            if args.chromium:
                launch["executable_path"] = args.chromium
            browser = await p.chromium.launch(**launch)
            sem = asyncio.Semaphore(args.workers)
            done = [0]
            jobs = [(s, sz) for s in slugs for sz in args.sizes]

            async def job(s, sz):
                async with sem:
                    r = await measure_one(browser, base, s, sz, args)
                    done[0] += 1
                    if done[0] % 15 == 0 or args.only:
                        print("  %d/%d measured" % (done[0], len(jobs)), flush=True)
                    return r
            results = await asyncio.gather(*(job(s, sz) for s, sz in jobs))
            await browser.close()
    finally:
        proc.terminate()

    escaped = sorted({u for r in results for u in r.get("escaped", [])})
    if escaped:
        print("NETWORK GUARD BREACHED -- a write request completed:", escaped[:5])
        sys.exit(2)
    if args.json:
        with open(args.json, "w", encoding="utf-8", newline='') as fh:
            json.dump(results, fh)
    report = args.sizes not in (SIZES, LAPTOP_SIZES)
    mode = "laptop" if args.laptop else "aa" if args.aa else "normal"
    games = write_report(results, args.out, time.time() - t0, mode, args.only, args.sizes, report)
    for st, sev, slug, rows, detail in games:
        print("  %-20s %-28s %s" % (st, slug, detail))
    print("wrote", args.out)
    if report:
        print("report mode (--sizes): nothing judged")
        return
    print("known failures (reported, never failed): %d game(s); unmeasurable and listed: %d" % (
        sum(1 for g in games if g[0] == KNOWN_FAIL), sum(1 for g in games if g[0] == UNMEASURABLE)))
    bad = [g for g in games if g[0] in GATE_FAILS]
    if bad:
        for st, sev, slug, rows, detail in bad:
            print("GATE %s: %s: %s" % (st, slug, detail))
        sys.exit(1)


def selftest():
    """Planted rows through classify(): each must land on its status."""
    def row(w, top, bottom, nxt, sw=None):
        h = {320: 568, 375: 667, 390: 844}[w]
        fold = h - 40
        sw = w if sw is None else sw
        return {"w": w, "h": h, "note": "", "ask": {"top": top, "bottom": bottom, "fold": fold, "sw": sw, "vw": w},
                "wrong": {"found": True, "bottom": nxt, "fold": fold, "sw": sw, "vw": w}}
    none = lambda w: {"w": w, "h": {320: 568, 375: 667, 390: 844}[w], "note": "no answer controls found",
                      "ask": None, "wrong": None}
    fits = [row(320, 300, 400, 500), row(375, 300, 400, 500), row(390, 300, 400, 500)]
    gone = [none(320), none(375), none(390)]
    cases = [
        # (name, rows, mode, known entries, on the unmeasurable list, wanted status)
        ("everything above the fold", fits, "normal", (), False, "PASS"),
        ("options start below the fold at 375", [fits[0], row(375, 640, 700, 800), fits[2]], "normal", (), False, HARD_FAIL),
        ("options start below the fold in Aa at 320", [row(320, 540, 600, 700), fits[1], fits[2]], "aa", (), False, HARD_FAIL),
        ("normal 320: the last option below, the first above", [row(320, 500, 600, 400), fits[1], fits[2]], "normal", (), False, HARD_FAIL),
        ("normal 390: the last option below, the first above", [fits[0], fits[1], row(390, 700, 820, 500)], "normal", (), False, HARD_FAIL),
        ("Aa 375: the last option below, the first above", [fits[0], row(375, 600, 700, 500), fits[2]], "aa", (), False, HARD_FAIL),
        ("Aa 320: the last option below, the first above", [row(320, 500, 600, 700), fits[1], fits[2]], "aa", (), False, WARN_AA),
        ("Aa 320: Next below, options start above", [row(320, 300, 520, 700), fits[1], fits[2]], "aa", (), False, WARN_AA),
        ("normal 320: last option below, listed", [row(320, 500, 600, 400), fits[1], fits[2]], "normal", ("320x568",), False, KNOWN_FAIL),
        ("normal: listed at 320, fails at 320 and 375", [row(320, 500, 600, 400), row(375, 600, 700, 400), fits[2]], "normal",
         ("320x568",), False, HARD_FAIL),
        ("normal: listed at 320 and 375, fails at 320 only", [row(320, 500, 600, 400), fits[1], fits[2]], "normal",
         ("320x568", "375x667"), False, STALE),
        ("listed at 320 but passes", fits, "normal", ("320x568",), False, STALE),
        ("unmeasurable, listed", gone, "normal", (), True, UNMEASURABLE),
        ("unmeasurable, not listed", gone, "aa", (), False, UNMEASURABLE_NEW),
        ("on the unmeasurable list but measured", fits, "normal", (), True, STALE),
        ("normal 320: Next below the fold (reported)", [row(320, 300, 400, 700), fits[1], fits[2]], "normal", (), False, "FAIL"),
        ("Aa 375: Next below the fold (reported)", [fits[0], row(375, 300, 400, 700), fits[2]], "aa", (), False, "FAIL"),
        ("Aa 320 scrolling sideways, not listed", [row(320, 300, 400, 500, sw=360), fits[1], fits[2]], "aa", (), False, HARD_FAIL),
    ]
    # The start screen is measured for the report, never judged (Jon's correction, 26 Oct 2026).
    def with_start(rows, picker_bottom):
        out = []
        for r in rows:
            r = dict(r); f = r["ask"]["fold"]
            r["start"] = {"picker": {"n": 3, "top": 200, "bottom": picker_bottom, "fold": f},
                          "start": {"top": picker_bottom + 10, "bottom": picker_bottom + 54, "fold": f, "label": "Start"}}
            out.append(r)
        return out
    cases += [
        ("start screen fits, question below the fold at 320", with_start([row(320, 500, 600, 400), fits[1], fits[2]], 300),
         "normal", (), False, HARD_FAIL),
        ("start screen below the fold, question fits (report only)", with_start(fits, 900), "normal", (), False, "PASS"),
    ]
    # Sideways scroll, a gate with its own list (contract FOLD-COMPONENTS, Jon 26 Oct 2026). Planted: (name, rows, mode,
    # known entries, unmeasurable listed, wanted status, sideways list).
    side = [row(320, 300, 400, 500, sw=410), fits[1], fits[2]]
    side_cases = [
        ("normal 320 scrolls sideways, not listed", side, "normal", (), False, HARD_FAIL, ()),
        ("normal 320 scrolls sideways, listed", side, "normal", (), False, KNOWN_FAIL, ("320x568",)),
        ("listed as sideways at 320 but does not scroll", fits, "normal", (), False, STALE, ("320x568",)),
        ("sideways listed, a new size scrolls too", [side[0], row(375, 300, 400, 500, sw=420), fits[2]], "normal", (), False,
         HARD_FAIL, ("320x568",)),
    ]
    # The laptop rule, R2: the last option AND Next above the fold at 1366x768 and 1280x720.
    def lap(w, bottom, nxt, found=True):
        h = {1366: 768, 1280: 720}[w]
        return {"w": w, "h": h, "note": "", "ask": {"top": 300, "bottom": bottom, "fold": h - 40, "sw": w, "vw": w},
                "wrong": {"found": found, "bottom": nxt, "fold": h - 40, "sw": w, "vw": w}}
    lfit = [lap(1366, 500, 600), lap(1280, 500, 600)]
    lap_cases = [
        ("laptop: everything above the fold", lfit, "laptop", (), False, "PASS", ()),
        ("laptop 1280: the last option below the fold", [lfit[0], lap(1280, 700, 600)], "laptop", (), False, HARD_FAIL, ()),
        ("laptop 1366: Next below the fold (the gate here)", [lap(1366, 500, 760), lfit[1]], "laptop", (), False, HARD_FAIL, ()),
        ("laptop 1366: Next below, listed", [lap(1366, 500, 760), lfit[1]], "laptop", ("1366x768 next",), False, KNOWN_FAIL, ()),
        ("laptop: Next listed at 1366 but fits", lfit, "laptop", ("1366x768 next",), False, STALE, ()),
        ("laptop: no Next control is not judged", [lap(1366, 500, 0, found=False), lap(1280, 500, 0, found=False)], "laptop", (),
         False, "PASS (no Next)", ()),
    ]
    # A canvas question measured by its box (classification; the page side is planted in Chromium below).
    def cv(r):
        r = dict(r); r["ask"] = dict(r["ask"], canvas=True); return r
    canvas_cases = [
        ("canvas: its box and controls above the fold", [cv(r) for r in fits], "normal", (), False, "PASS", ()),
        ("canvas: its Fire button below the fold at 320", [cv(row(320, 200, 560, 400)), cv(fits[1]), cv(fits[2])], "normal", (),
         False, HARD_FAIL, ()),
        ("canvas: measured now, still on the unmeasurable list", [cv(r) for r in fits], "normal", (), True, STALE, ()),
    ]
    ok = True
    for name, rows, mode, known, unl, want, sw in side_cases + lap_cases + canvas_cases:
        got = classify(rows, mode, known, unl, sw)[0]
        print("  %s  %-52s %s" % ("ok  " if got == want else "FAIL", name, got))
        ok = ok and got == want
    for name, rows, aa, known, unl, want in cases:
        got = classify(rows, aa, known, unl)[0]
        print("  %s  %-52s %s" % ("ok  " if got == want else "FAIL", name, got))
        ok = ok and got == want

    # A two-second banner (the Core Maths papers' section card): still for two seconds, with the timer that removes it
    # pending. settle() must measure the question after it, never the banner; the planted wait that watches the
    # layout alone measures the banner and is caught.
    banner = [(t, "banner" if t < 2000 else "question", 1 if t < 2000 else 0) for t in range(0, 4000, 100)]
    got = settle_point(banner)
    sig_at = next(sig for t, sig, _ in reversed(banner) if t <= got[0]) if got else None
    good = bool(got) and got[1] and got[0] >= 2500 and sig_at == "question"
    print("  %s  %-52s %s" % ("ok  " if good else "FAIL", "a 2 s banner: measured after it, on the question", got))
    planted = settle_point([(t, sig, 0) for t, sig, _ in banner])
    caught = bool(planted) and planted[0] < 2000
    print("  %s  %-52s %s" % ("ok  " if caught else "FAIL", "plant: a wait on the layout alone measures the banner",
                              "caught (it settles at %d ms, on the banner)" % planted[0] if caught else planted))
    clock = [(t, "q|%d" % (t // 1000), 0) for t in range(0, 6000, 100)]   # a ticking clock changes text, not layout
    still = settle_point([(t, "q", 0) for t, _, _ in clock])
    print("  %s  %-52s %s" % ("ok  " if still == (500, True) else "FAIL", "a still question settles after 500 ms", still))
    ceiling = settle_point([(t, "move%d" % t, 0) for t in range(0, 6000, 100)])
    print("  %s  %-52s %s" % ("ok  " if ceiling == (5000, False) else "FAIL", "a layout that never settles: the 5 s ceiling", ceiling))
    ok = ok and good and caught and still == (500, True) and ceiling == (5000, False)
    with open(STATE, encoding="utf-8") as fh:
        st = json.load(fh)
    phone = {"%dx%d" % s for s in SIZES}
    laptop = {"%dx%d" % s for s in LAPTOP_SIZES}
    allowed = {"normal": phone, "aa": phone, "laptop": {k + " " + c for k in laptop for c in ("option", "next")}}
    for mode in ("normal", "aa", "laptop"):
        for slug, sizes in st["known-failures"][mode].items():
            if not sizes or set(sizes) - allowed[mode]:
                print("  FAIL  phone-fit-state.json: known-failures %s/%s has no entries or an unknown one" % (mode, slug))
                ok = False
        for slug, sizes in st["sideways"][mode].items():
            if not sizes or set(sizes) - (laptop if mode == "laptop" else phone):
                print("  FAIL  phone-fit-state.json: sideways %s/%s has no sizes or an unknown one" % (mode, slug))
                ok = False
    ok = canvas_plant() and ok
    print("selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def canvas_plant():
    """The page side of the canvas measurement, in Chromium on planted pages: a canvas question whose Fire button ends
    below the fold is measured by the canvas and the button and fails; one that fits passes; a page with an option
    group never falls back to the canvas. No per-game code: the same __pfAsking every game runs."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  FAIL  canvas plant: Playwright is not installed")
        return False
    page_html = ("<!doctype html><html><head><meta name='viewport' content='width=device-width'></head>"
                 "<body style='margin:0'><header style='height:60px'><a href='#'>Back</a></header>"
                 "<canvas width='300' height='%d' style='display:block;width:300px;height:%dpx'></canvas>"
                 "<button onclick='1'>Fire</button>%s</body></html>")
    plants = [
        ("canvas plant: Fire below the fold, measured and over", page_html % (520, 520, ""), lambda a: a["canvas"] and a["bottom"] > a["fold"]),
        ("canvas plant: canvas and Fire fit", page_html % (300, 300, ""), lambda a: a["canvas"] and a["bottom"] <= a["fold"]),
        ("canvas plant: an option group wins over the canvas", page_html % (300, 300,
         "<div><button onclick='1'>12</button><button onclick='1'>15</button><button onclick='1'>18</button></div>"),
         lambda a: not a["canvas"]),
    ]
    ok = True
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, html, want in plants:
            pg = b.new_page(viewport={"width": 320, "height": 568})
            pg.set_content(html)
            pg.evaluate(cs.TIER3_INIT)
            pg.evaluate(CORRECT_INIT)
            a = pg.evaluate("window.__pfAsking()")
            good = bool(a["n"]) and want(a)
            print("  %s  %-52s %s" % ("ok  " if good else "FAIL", name, "canvas=%s bottom %s / %s" % (a["canvas"], a["bottom"], a["fold"])))
            ok = ok and good
            pg.close()
        b.close()
    return ok


def parse_sizes(text):
    sizes = []
    for part in text.split(","):
        w, h = part.lower().strip().split("x")
        sizes.append((int(w), int(h)))
    return sizes


def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", help="one game slug")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--katex-dir", help="serve KaTeX 0.16.9 from this local dist/ (sandbox only)")
    ap.add_argument("--fonts", choices=("real", "fallback"), default="real",
                    help="real (default): KaTeX and Google Fonts served from scripts/fonts/, the faces students see; "
                         "fallback: Google Fonts blocked, the old measure in the runner's fallback font")
    ap.add_argument("--proxy-from-env", action="store_true",
                    help="route Chromium through $HTTPS_PROXY (sandbox only)")
    ap.add_argument("--aa", action="store_true",
                    help="measure with Aa (OpenDyslexic) mode on; use with --out, the default report is normal mode")
    ap.add_argument("--chromium", help="launch this Chromium binary instead of Playwright's own")
    ap.add_argument("--laptop", action="store_true",
                    help="judge the laptop and projector sizes, 1366x768 and 1280x720, normal mode (ruling R2)")
    ap.add_argument("--sizes", type=parse_sizes, default=SIZES,
                    help="WxH,WxH,... (report mode: measured, judged against nothing, never exits 1), e.g. 1366x768,1280x720")
    ap.add_argument("--json", help="also write every raw measurement to this file")
    args = ap.parse_args()
    if args.laptop:
        if args.aa:
            sys.exit("--laptop judges normal mode only (ruling R2); drop --aa")
        args.sizes = LAPTOP_SIZES
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
