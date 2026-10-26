#!/usr/bin/env python3
"""Does each game fit a phone? A report with one gate (canon §7.6.1, the phone rule).

    python scripts/measure-phone-fit.py                 # every roster game -> docs/phone-fit-report.md
    python scripts/measure-phone-fit.py --aa            # the same in Aa (OpenDyslexic) mode
    python scripts/measure-phone-fit.py --only new-shapes
    python scripts/measure-phone-fit.py --workers 6
    python scripts/measure-phone-fit.py --selftest      # the classification, planted cases (no browser)

THE GATE (canon 7.6.1; Jon's rulings of 26 Oct 2026): in normal mode at every size, and in Aa mode at 375x667 and
390x844, the LAST answer option must end above the fold, so a student never chooses from three of four options
without knowing it. In Aa mode at 320x568, the recorded exception (OpenDyslexic cannot fit a long GCSE prompt and
its feedback on that screen), the options must START above the fold, and an overflow beyond that is WARN.
Two lists in scripts/phone-fit-state.json may only shrink: "known-failures" (per mode, each game with the sizes at
which it fails the gate: reported, never failed) and "unmeasurable" (per mode, the games this driver cannot measure,
so they never read as passing). A gate failure not on the list, a listed entry that now passes or now measures, and
an unmeasurable game not on its list each make the run exit 1. Every other overflow (Next below the fold, sideways
scroll) is FAIL: reported, not a gate. Not run in CI yet (a later contract).

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
KATEX_PREFIX = "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/"
DEFAULT_OUT = os.path.join(ROOT, "docs", "phone-fit-report.md")

# Runs after TIER3_INIT. Tier 3 records which event fired and its question index;
# this report also needs whether the answer was right, so mfg's accessor is
# replaced by one that records `correct` too. Same contract as tier 3's: whatever
# the page assigns to window.mfg is kept and still called.
CORRECT_INIT = r"""
(() => {
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
    return {
      n: els.length,
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
        await page.wait_for_timeout(800)
        try:
            await asyncio.wait_for(page.evaluate("document.fonts.ready.then(() => 1)"), timeout=8)
        except Exception:
            pass

        # Getting to question 1: tier 3's sequence, step for step (check-site.py, play_one).
        for _ in range(4):
            if (await ev("window.__mfgStats()"))["started"]:
                break
            if await ev("window.__mfgHasStart()"):
                await ev("window.__mfgClickStart()")
            elif (await ev("window.__mfgProbe()"))["n"] >= 2:
                await ev("window.__mfgClickOpt(0)")
            else:
                break
            await page.wait_for_timeout(700)
        if not (await ev("window.__mfgStats()"))["started"]:
            try:
                await ev("typeof window.startGame === 'function' && window.startGame()")
                await page.wait_for_timeout(700)
            except Exception:
                pass
        await page.wait_for_timeout(300)

        await ev("window.scrollTo(0, 0)")
        ask = await ev("window.__pfAsking()")
        if not ask["n"]:
            out["note"] = "no answer controls found"
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
                await page.wait_for_timeout(700)
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


def gate_sizes(rows, aa=False):
    """The sizes at which a game fails THE GATE (canon 7.6.1, Jon's rulings of 26 Oct 2026). The LAST answer control
    must end above the fold, in normal mode at every size and in Aa mode at 375x667 and 390x844. In Aa at 320x568, the
    recorded exception, the controls must START above the fold. A size whose asking screen was not reached is not
    judged here (UNMEASURABLE is the game-level case)."""
    out = []
    for r in rows:
        a = r["ask"]
        if not a:
            continue
        if aa and r["w"] == 320:
            bad = a.get("top") is not None and a["top"] > a["fold"]
        else:
            bad = a["bottom"] > a["fold"]
        if bad:
            out.append(size_key(r))
    return out


def classify(rows, aa=False, known=(), unmeasurable_listed=False):
    """One game's three sizes in one mode -> (status, severity, detail).

    THE GATE (gate_sizes). A failure at a size not on the game's known-failures entry (phone-fit-state.json) is
    HARD_FAIL; a listed size that now passes is STALE (take it off: the list only shrinks); failures that are all
    listed are KNOWN_FAIL, reported, never failed. A game the driver cannot measure must be on the unmeasurable list
    (UNMEASURABLE), or it is UNMEASURABLE_NEW: it never reads as passing. HARD_FAIL, STALE and UNMEASURABLE_NEW make
    the run exit 1. Beyond the gate, Next below the fold and sideways scroll are FAIL: reported, not a gate. In Aa at
    320x568 an overflow that keeps the options starting above the fold is WARN (Aa at 320)."""
    known = set(known or ())
    asks = [r for r in rows if r["ask"]]
    wrongs = [r for r in rows if r["wrong"]]
    if not asks:
        why = rows[0]["note"] or "asking screen not reached"
        if known:
            return STALE, -10 ** 3, "unmeasurable, but on the known-failures list: take it off (the list only shrinks)"
        if unmeasurable_listed:
            return UNMEASURABLE, -10 ** 7, why
        return UNMEASURABLE_NEW, -10 ** 3, why + " (not on the unmeasurable list: it never reads as passing)"
    if unmeasurable_listed:
        return STALE, -10 ** 3, "measured, but on the unmeasurable list: take it off (the list only shrinks)"

    def edge(r):
        a = r["ask"]
        if aa and r["w"] == 320:
            return "%s (options start %d / %d)" % (size_key(r), a["top"], a["fold"])
        return "%s (last option %d / %d)" % (size_key(r), a["bottom"], a["fold"])
    by = {size_key(r): r for r in asks}
    gate = gate_sizes(rows, aa)
    sev = max([by[k]["ask"]["bottom"] - by[k]["ask"]["fold"] for k in gate] + [0])
    new = [k for k in gate if k not in known]
    if new:
        return HARD_FAIL, sev, "below the fold, not on the known-failures list: " + ", ".join(edge(by[k]) for k in new)
    stale = sorted(known - set(gate))
    if stale:
        return STALE, -10 ** 3, "on the known-failures list at %s but passes there: take it off (the list only shrinks)" % (
            ", ".join(stale))
    if gate:
        return KNOWN_FAIL, sev, "known failure: " + ", ".join(edge(by[k]) for k in gate)

    scrolls = lambda r: aa and r["w"] == 320           # canon 7.6.1: Aa at 320 x 568 may scroll
    over_next = [r["wrong"]["bottom"] - r["wrong"]["fold"] for r in wrongs if r["wrong"]["found"] and not scrolls(r)]
    warn = [r for r in rows if scrolls(r) and ((r["ask"] and r["ask"]["bottom"] > r["ask"]["fold"]) or
            (r["wrong"] and r["wrong"]["found"] and r["wrong"]["bottom"] > r["wrong"]["fold"]))]
    hscroll = any((r["ask"] and r["ask"]["sw"] > r["ask"]["vw"]) or
                  (r["wrong"] and r["wrong"]["sw"] > r["wrong"]["vw"]) for r in rows)
    fails = []
    if any(o > 0 for o in over_next):
        fails.append("Next below fold")
    if hscroll:
        fails.append("sideways scroll")
    worst = max(over_next + [-10 ** 6])
    if fails:
        # Ranked by how far past the fold the worst edge is; a game that only
        # scrolls sideways ranks after every fold failure.
        return "FAIL", max(worst, 0), "; ".join(fails)
    if warn:
        return WARN_AA, -10 ** 4, "Aa at 320x568 scrolls; the options start above the fold"
    if len(wrongs) < len(rows):
        return "PASS (asking only)", -10 ** 6, next((r["note"] for r in rows if r["note"]), "")
    if not over_next:
        return "PASS (no Next)", -10 ** 5, "wrong answer shows no Next control"
    return "PASS", worst, ""


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


def load_state(aa):
    with open(STATE, encoding="utf-8") as fh:
        st = json.load(fh)
    mode = "aa" if aa else "normal"
    return st["known-failures"][mode], set(st["unmeasurable"][mode])

# --aa: the stored preference every game's Aa toggle reads on load.
AA_INIT = "try { localStorage.setItem('mfg_accessible', 'true'); } catch (e) {}"


def write_report(results, path, elapsed, aa=False, only=None):
    known, unmeasurable = load_state(aa)
    by = {}
    for r in results:
        by.setdefault(r["slug"], []).append(r)
    games = []
    # A list entry for a game no longer on the roster is stale too (a full run only).
    for slug in sorted((set(known) | unmeasurable) - set(by)) if not only else []:
        games.append((STALE, -10 ** 3, slug, [], "on a phone-fit list but not measured (not on the roster): take it off"))
    for slug, rows in by.items():
        rows.sort(key=lambda r: r["w"])
        st, sev, detail = classify(rows, aa, known.get(slug, ()), slug in unmeasurable)
        games.append((st, sev, slug, rows, detail))
    order = {HARD_FAIL: -4, STALE: -3, UNMEASURABLE_NEW: -2, KNOWN_FAIL: -1, "FAIL": 0, WARN_AA: 1, "PASS (no Next)": 2,
             "PASS (asking only)": 3, "PASS": 4, UNMEASURABLE: 5}
    games.sort(key=lambda g: (order[g[0]], -g[1], g[2]))

    counts = {}
    for g in games:
        counts[g[0]] = counts.get(g[0], 0) + 1
    lines = [
        "# Phone fit report",
        "",
        "Generated by `scripts/measure-phone-fit.py` on %s (%d games, %.0f min). **A report, with one gate** (canon §7.6.1,"
        " 26 Oct 2026): the last answer option ends above the fold (Aa at 320: the options start above it). A failure"
        " not on `scripts/phone-fit-state.json`'s known-failures list (HARD FAIL), a listed entry that now passes"
        " (STALE) or an unmeasurable game not on its list makes the run exit 1; KNOWN FAIL is reported, never failed."
        % (datetime.date.today().isoformat(), len(games), elapsed / 60),
        "The standard is canon §7.6.1, the phone rule. Regenerate it with the same command; do not edit it by hand.",
        "",
    ] + (["**Aa (OpenDyslexic) mode on** (`--aa`).", ""] if aa else []) + [
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
    lines += ["", "| Game | Status | Asking 320×568 | Asking 375×667 | Asking 390×844 | Wrong 320×568 | "
                  "Wrong 375×667 | Wrong 390×844 | Sideways at 320 | Notes |",
              "|---|---|---|---|---|---|---|---|---|---|"]
    for st, sev, slug, rows, detail in games:
        side = "–"
        for r in rows:
            if r["w"] != 320:
                continue
            ms = [m for m in (r["ask"], r["wrong"]) if m]
            if ms:
                side = "**yes**" if any(m["sw"] > m["vw"] for m in ms) else "no"
        cells = (["`%s`" % slug, st] + ([cell(r["ask"]) for r in rows] or ["–"] * 3)
                 + ([cell(r["wrong"]) for r in rows] or ["–"] * 3) + [side, detail.replace("|", "/")])
        lines.append("| " + " | ".join(cells) + " |")
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
            jobs = [(s, sz) for s in slugs for sz in SIZES]

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
    games = write_report(results, args.out, time.time() - t0, args.aa, args.only)
    for st, sev, slug, rows, detail in games:
        print("  %-20s %-28s %s" % (st, slug, detail))
    print("wrote", args.out)
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
        # (name, rows, aa, known sizes, on the unmeasurable list, wanted status)
        ("everything above the fold", fits, False, (), False, "PASS"),
        ("options start below the fold at 375", [fits[0], row(375, 640, 700, 800), fits[2]], False, (), False, HARD_FAIL),
        ("options start below the fold in Aa at 320", [row(320, 540, 600, 700), fits[1], fits[2]], True, (), False, HARD_FAIL),
        ("normal 320: the last option below, the first above", [row(320, 500, 600, 400), fits[1], fits[2]], False, (), False, HARD_FAIL),
        ("normal 390: the last option below, the first above", [fits[0], fits[1], row(390, 700, 820, 500)], False, (), False, HARD_FAIL),
        ("Aa 375: the last option below, the first above", [fits[0], row(375, 600, 700, 500), fits[2]], True, (), False, HARD_FAIL),
        ("Aa 320: the last option below, the first above", [row(320, 500, 600, 700), fits[1], fits[2]], True, (), False, WARN_AA),
        ("Aa 320: Next below, options start above", [row(320, 300, 520, 700), fits[1], fits[2]], True, (), False, WARN_AA),
        ("normal 320: last option below, listed", [row(320, 500, 600, 400), fits[1], fits[2]], False, ("320x568",), False, KNOWN_FAIL),
        ("normal: listed at 320, fails at 320 and 375", [row(320, 500, 600, 400), row(375, 600, 700, 400), fits[2]], False,
         ("320x568",), False, HARD_FAIL),
        ("normal: listed at 320 and 375, fails at 320 only", [row(320, 500, 600, 400), fits[1], fits[2]], False,
         ("320x568", "375x667"), False, STALE),
        ("listed at 320 but passes", fits, False, ("320x568",), False, STALE),
        ("unmeasurable, listed", gone, False, (), True, UNMEASURABLE),
        ("unmeasurable, not listed", gone, True, (), False, UNMEASURABLE_NEW),
        ("on the unmeasurable list but measured", fits, False, (), True, STALE),
        ("normal 320: Next below the fold (reported)", [row(320, 300, 400, 700), fits[1], fits[2]], False, (), False, "FAIL"),
        ("Aa 375: Next below the fold (reported)", [fits[0], row(375, 300, 400, 700), fits[2]], True, (), False, "FAIL"),
        ("Aa 320 scrolling sideways", [row(320, 300, 400, 500, sw=360), fits[1], fits[2]], True, (), False, "FAIL"),
    ]
    ok = True
    for name, rows, aa, known, unl, want in cases:
        got = classify(rows, aa, known, unl)[0]
        print("  %s  %-52s %s" % ("ok  " if got == want else "FAIL", name, got))
        ok = ok and got == want
    with open(STATE, encoding="utf-8") as fh:
        st = json.load(fh)
    for mode in ("normal", "aa"):
        for slug, sizes in st["known-failures"][mode].items():
            if not sizes or set(sizes) - {"%dx%d" % s for s in SIZES}:
                print("  FAIL  phone-fit-state.json: %s/%s has no sizes or an unknown one" % (mode, slug))
                ok = False
    print("selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


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
    args = ap.parse_args()
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
