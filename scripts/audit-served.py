#!/usr/bin/env python3
# ci-held: a hand-run audit that plays whole sessions of every game, far longer than any CI budget (contract B4-SERVED-AUDIT: report only, never in CI; results in docs/audits/)
"""How many different questions does each game's level actually serve? (contract B4-SERVED-AUDIT, 23 Nov 2026)

    python -X utf8 scripts/audit-served.py --selftest            # the three self-tests; run these first
    python -X utf8 scripts/audit-served.py --list-blocks         # fix (once) and print the block split
    python -X utf8 scripts/audit-served.py --block 1             # run one block (Amendment 2: at most 90 minutes)
    python -X utf8 scripts/audit-served.py --only scale-factor   # substring filter on slug, all roster levels

SAVED AS IT GOES (Amendment 2): each level's row is merged into docs/audits/served-2026-11.json, keyed by
(slug, level), the moment the level finishes (a temporary file, then os.replace), and the markdown is regenerated
from the whole JSON, so a stopped run keeps every level it finished. Rows for other levels, the stored estimate,
the block split and the self-tests are kept.

BLOCKS (Amendment 2): the in-scope levels (scope C less prisoners-dilemma) are split once, from the stored
one-session estimate, into blocks of at most BLOCK_MINUTES (90) at --workers 4, and the split is written to the
JSON ("blocks") before block 1 runs. A level's projected cost is its one-session time times
min(MAX_SESSIONS, 2 * ceil(40 / questions in that session) + SATURATION_RUN) sessions (one session for a level tier
3 cannot drive or whose session hit the cap). Each block runs with a BLOCK_HOURS (2) backstop; a level cut off is
UNFINISHED and is moved into the next block, and the split records the move.

Run scripts/extract-banks.py first: the B4 column is read from data/banks/<slug>.json (gitignored), as
check-banks.py reads it. Without it the column says "not extracted".

WHY. B4 (check-banks.py) compares a level's extracted "count" with 40, and extract-banks.py counts every question
group on the page at that level's query unless a group's path names the level. A game that keeps its levels in
named arrays and chooses among them in its own start code is counted as the whole page at every level, so B4
passes a level that serves fewer than 40 (scale-factor-scaling's GCSE: 46 counted, 38 served). This script
measures what is served instead, by playing.

THE DRIVER is tier 3's, imported from check-site.py, not copied: play_one plays a session in a fresh page with
TIER3_INIT (option finding, option identity, start, continue and submit controls) and KaTeX's hook, against
serve-stubbed.py's handler (analytics stubbed; check-site.py's network guard blocks every write). Each session is
play_one asked for up to MAX_QUESTIONS questions: it stops when the game says it has ended (game_completed, or a
"play again" control with no question on screen). A session that reaches MAX_QUESTIONS without ending is reported
as one that never ends.

THREE INIT SCRIPTS ARE ADDED, and none of them changes what tier 3 clicks:
  - the seed: PHONE_SEED's own text (check-site.py, mulberry32) with its path hash replaced by the session number
    1, 2, 3, ..., so sessions differ from one another and every run of this script is repeatable;
  - a fixed clock: Date.now() and new Date() return 2026-11-23 12:00 UTC (performance.now and timers run as
    normal), so a visible count-up or a score that includes time cannot make one question read as two;
  - the recorder (RECORD_INIT): wraps tier 3's window.__mfgClickOpt and window.__mfgTypeAnswer, and on each call
    after game_started reads what is on screen and passes it out; and wraps mfg to note game_started's level
    and mode, so the audit shows which level and mode the driver actually reached.

A SERVED QUESTION'S IDENTITY (the rule, as the audit states it):
  - its option set: tier 3's own option keys (window.__mfgOptKey: dataset.val, else the KaTeX annotation, else the
    text without .katex-mathml), sorted, so the order a game shuffles them into does not matter; empty for a typed
    question;
  - joined with its prompt: starting from the option group's parent (a typed question: the input's parent), walk
    up to the first ancestor holding visible text outside the options, and take that text. Left out: text in
    header, footer, nav, button, a, select, textarea, script, style or .katex-mathml; text inside an element whose
    id or class names a score, timer, clock, streak, lives, progress, counter, question number, points or HUD
    (VOLATILE_RE); and a piece reading as a counter ("Question 3", "3 of 10", "Score: 20"; COUNTER_RE).
  - one question per answer the game marks: the first answer the driver gives while the game's
    question_answered count stands at k is question k; a second phase of the same question (an equation picked,
    then a value typed) is not a new question. A game that never fires question_answered falls back to a change
    of identity starting a new question.
Two questions with the same options and the same prompt are one question to this rule (undercounting); a prompt
carrying text that differs between sessions for the same question would make one question two (overcounting).
The audit therefore also gives the count by option set alone, and lists every level where the prompt alone takes
a level from under 40 to 40 or more.

THE STOP RULE (Amendment 2), checked after each session: 40 or more distinct ends the level, 40+ (its verdict can
no longer change); otherwise SATURATION_RUN (8) sessions in a row adding no new question ends it (saturated), and
MAX_SESSIONS (40) ends it. A session still running at MAX_QUESTIONS (100) ends the level as UNMEASURED ("session
over 100 questions: driver plays this game's shape badly"). A level whose first session tier 3 cannot drive
(UNSUPPORTED) is played once and reported UNMEASURED with tier 3's reason. In-session repeats are recorded for
every session played, so a 40+ level was checked for them only in the sessions it took to reach 40: not a full
repeat check.

VERDICT: UNDER 40 (saturated, distinct < 40), 40+ (distinct >= 40), UNSATURATED (40 sessions, distinct < 40),
UNFINISHED (the block's backstop came first), UNMEASURED (tier 3 cannot play it, or the session cap). A question served twice in one session is listed with game, level, seed and
question (and whether the two were consecutive, which may be a game's deliberate retry).

--selftest plays three page copies at fixed commits, served in place of the live page (contract step 3):
formula-unlocked at 38895242 (A-Level: UNDER 40, 25 or fewer, an in-session repeat), scale-factor-scaling at
65ae674 (GCSE: UNDER 40, exactly 38) and formula-unlocked at 28be68a (A-Level: 40 or more, no repeat).
"""
import argparse
import asyncio
import functools
import http.server
import importlib.util
import json
import os
import re
import statistics
import subprocess
import sys
import threading
import time
from urllib.parse import urlsplit

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)


def _load(name, filename):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cs = _load("check_site", "check-site.py")          # tier 3's driver: play_one, TIER3_INIT, PHONE_SEED, the guard
bc = cs.bc                                          # bank_common, as check-site.py imports it
stubbed = _load("serve_stubbed", "serve-stubbed.py")

OUT_JSON = os.path.join(ROOT, "docs", "audits", "served-2026-11.json")
OUT_MD = os.path.join(ROOT, "docs", "audits", "served-2026-11.md")

SATURATION_RUN = 8
MAX_SESSIONS = 40
MAX_QUESTIONS = 100
TIMEOUT_MS = 20000
ADVANCE_MS = 6000

# PHONE_SEED, seeded with the session number in place of the path hash. The replacement is checked, so a change
# to PHONE_SEED's text fails here loudly instead of silently seeding every session alike.
_SEED_LINE = "let s = h;"
if cs.PHONE_SEED.count(_SEED_LINE) != 1:
    raise SystemExit("audit-served: check-site.py's PHONE_SEED no longer has exactly one %r; update session_seed()"
                     % _SEED_LINE)


def session_seed(n):
    return cs.PHONE_SEED.replace(_SEED_LINE, "let s = %d >>> 0;" % n)


FIXED_CLOCK = r"""
(() => {
  const RealDate = Date;
  const T = RealDate.UTC(2026, 10, 23, 12, 0, 0);
  function FixedDate(...a) {
    if (!new.target) return new RealDate(T).toString();
    return a.length ? new RealDate(...a) : new RealDate(T);
  }
  FixedDate.prototype = RealDate.prototype;
  FixedDate.now = function () { return T; };
  FixedDate.UTC = RealDate.UTC;
  FixedDate.parse = RealDate.parse;
  window.Date = FixedDate;
})();
"""

# Added after TIER3_INIT, so its window.__mfgClickOpt / __mfgTypeAnswer / __mfgOptKey / __mfgStats exist to wrap.
RECORD_INIT = r"""
(() => {
  const push = function (rec) { try { window.__auditPush(rec); } catch (e) { /* page closing */ } };

  const d = Object.getOwnPropertyDescriptor(window, 'mfg');
  if (d && d.get && d.configurable) {
    Object.defineProperty(window, 'mfg', {
      configurable: true,
      get: function () {
        const f = d.get.call(window);
        return function () {
          try {
            if (arguments[0] === 'game_started' && arguments[1]) {
              push({ t: 'start', level: String(arguments[1].level),
                     mode: arguments[1].mode === undefined ? null : String(arguments[1].mode) });
            }
          } catch (e) {}
          return f.apply(this, arguments);
        };
      },
      set: function (v) { d.set.call(window, v); }
    });
  }

  const SKIP = 'header, footer, nav, button, a, select, textarea, script, style, noscript, .katex-mathml, [role="button"]';
  const VOLATILE_RE = /(score|timer|clock|streak|lives|progress|counter|qnum|q-num|qcount|q-count|questionnum|question-num|questioncount|question-count|points|hud)/i;
  const COUNTER_RE = /^(?:(?:question|q|round|score|streak|lives?|best|points?|pts|correct)\b\s*[:#.]?\s*\d[\d\s\/of]*|\d+\s+of\s+\d+|\d+\s*\/\s*\d+\s+(?:questions?|correct|answered))$/i;

  function volatile(el, stop) {
    for (let a = el; a && a !== stop.parentElement; a = a.parentElement) {
      const mark = (a.id || '') + ' ' + (typeof a.className === 'string' ? a.className
                                         : (a.className && a.className.baseVal) || '');
      if (VOLATILE_RE.test(mark)) return true;
      if (a === stop) break;
    }
    return false;
  }

  function shown(el) {
    if (typeof el.checkVisibility === 'function') {
      return el.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true });
    }
    return el.getClientRects().length > 0;
  }

  function residual(anc, anchors) {
    const out = [];
    const w = document.createTreeWalker(anc, NodeFilter.SHOW_TEXT);
    for (let n = w.nextNode(); n; n = w.nextNode()) {
      const t = (n.nodeValue || '').trim().replace(/\s+/g, ' ');
      if (!t) continue;
      const el = n.parentElement;
      if (!el || el.closest(SKIP)) continue;
      if (anchors.some(function (a) { return a.contains(n); })) continue;
      if (!shown(el)) continue;
      if (volatile(el, anc)) continue;
      out.push(t);
    }
    // An ancestor holding nothing but a counter ("Score:" and "20" as two nodes) has no prompt.
    if (COUNTER_RE.test(out.join(' ').trim())) return '';
    return out.filter(function (t) { return !COUNTER_RE.test(t); }).join(' ').trim();
  }

  function prompt(anchors) {
    if (!anchors.length || !anchors[0].parentElement) return '';
    for (let a = anchors[0].parentElement; a && a !== document.documentElement; a = a.parentElement) {
      const r = residual(a, anchors);
      if (r) return r;
      if (a === document.body) break;
    }
    return '';
  }

  function record(kind) {
    let s;
    try { s = window.__mfgStats(); } catch (e) { return; }
    if (!s.started) return;
    const grp = (window.__mfgGroup || []).filter(function (e) { return e.isConnected; });
    let opts = [], anchors = [];
    if (kind === 'opt' && grp.length >= 2) {
      opts = grp.map(window.__mfgOptKey).sort();
      anchors = grp;
    } else {
      const inp = [...document.querySelectorAll('input, [contenteditable="true"]')].filter(shown);
      anchors = inp.slice(0, 1);
    }
    push({ t: 'q', kind: kind, k: s.answered, opts: opts, prompt: prompt(anchors).slice(0, 600) });
  }

  // Tier 3 taps as soon as a new question is on screen, inside MaffsLock's fresh window (answer-lock.js: every
  // input on a container is ignored for FRESH_MS, 300 ms, after fresh()), so the tap is dropped and the game reads
  // as one tier 3 cannot drive. A student's tap comes later. Wait the window out before each tap, as
  // check-answer-lock.py does (MaffsLock.isFresh); the page's clock (performance.now) runs during the wait.
  function waitFresh() {
    const ml = window.MaffsLock;
    if (!ml || typeof ml.isFresh !== 'function') return;
    const t0 = performance.now();
    while (ml.isFresh() && performance.now() - t0 < 1500) { /* the window is at most FRESH_MS */ }
  }

  const origClick = window.__mfgClickOpt;
  window.__mfgClickOpt = function (i) { waitFresh(); record('opt'); return origClick(i); };
  const origType = window.__mfgTypeAnswer;
  window.__mfgTypeAnswer = function (v) { waitFresh(); record('typed'); return origType(v); };
  const origSubmit = window.__mfgClickSubmit;
  window.__mfgClickSubmit = function () { waitFresh(); return origSubmit(); };
})();
"""


def identity(rec):
    return json.dumps([rec["opts"], rec["prompt"]], ensure_ascii=False)


def servings(records):
    """[(identity, options-only identity)], one per question the game served, from a session's 'q' records."""
    qs = [r for r in records if r.get("t") == "q"]
    out, last_k, last_id = [], None, None
    narrates = any(r["k"] > 0 for r in qs)
    for r in qs:
        ident = identity(r)
        new = (r["k"] != last_k) if narrates else (ident != last_id)
        if new:
            out.append((ident, json.dumps(r["opts"], ensure_ascii=False)))
        last_k, last_id = r["k"], ident
    return out


# --------------------------------------------------------------------------- the server

def start_server(overrides=None):
    """serve-stubbed.py's handler, in-process, on a free port; overrides maps a URL path to bytes served instead."""
    overrides = overrides or {}

    class Handler(stubbed.Handler):
        def do_GET(self):
            path = self.path.split("?")[0]
            if path in overrides:
                body = overrides[path]
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            super().do_GET()

    srv = stubbed.Server(("127.0.0.1", 0), functools.partial(Handler, directory=ROOT))
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, "http://127.0.0.1:%d" % srv.server_address[1]


# --------------------------------------------------------------------------- playing

class _OfflineContext:
    """The context play_one is handed: the real one, except that each page's routes are wrapped so nothing off this
    machine is fetched. play_one's own route handler (the network guard) still sees every other request. KaTeX and
    Google Fonts are answered from the pinned copies in scripts/fonts/ (bank_common.real_font_response, the bytes the
    CDNs serve); any other off-machine URL (the Firebase SDK from www.gstatic.com) is aborted with the guard's own
    net::ERR_FAILED, which tier 3 reads as guard noise. Why: this audit must not depend on what a container's network
    allows (a cloud session's proxy refuses cdn.jsdelivr.net and www.gstatic.com), and nothing it measures needs them."""

    def __init__(self, ctx, base):
        self._ctx, self._base = ctx, base

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    async def new_page(self):
        page = await self._ctx.new_page()
        real_route = page.route
        base = self._base

        async def route(pattern, handler, **kw):
            async def wrapped(r):
                url = r.request.url
                if url.startswith(base) or urlsplit(url).scheme in ("data", "blob", "about"):
                    return await handler(r)
                if cs.block_reason(url):
                    return await handler(r)          # the guard records and aborts it, as in tier 3
                got = bc.real_font_response(url)
                try:
                    await (r.fulfill(**got) if got else r.abort())
                except Exception:
                    pass
            return await real_route(pattern, wrapped, **kw)

        page.route = route
        return page


async def play_session(browser, base, slug, level, n):
    """One session (seed n) in a fresh context: (play_one's result, the recorder's records)."""
    records = []
    ctx = await browser.new_context()
    try:
        await ctx.expose_function("__auditPush", lambda rec: records.append(rec))
        await ctx.add_init_script(session_seed(n))
        await ctx.add_init_script(FIXED_CLOCK)
        await ctx.add_init_script(cs.TIER3_INIT)
        await ctx.add_init_script(bc.KATEX_HOOK_INIT)
        await ctx.add_init_script(RECORD_INIT)

        async def ws_handler(ws):
            await ws.close()
        await ctx.route_web_socket(lambda url: cs.block_reason(url) is not None, ws_handler)
        res = await cs.play_one(_OfflineContext(ctx, base), base, "game:" + slug, "games/%s/index.html" % slug, "?level=" + level,
                                False, TIMEOUT_MS, MAX_QUESTIONS, ADVANCE_MS, {})
    finally:
        await ctx.close()
    return res, records


def b4_count(slug, level):
    path = os.path.join(bc.BANKS_DIR, slug + ".json")
    if not os.path.exists(path):
        return "not extracted"
    with open(path, "r", encoding="utf-8") as fh:
        bank = json.load(fh)
    if bank.get("generator"):
        return "generator"
    info = bank.get("levels", {}).get(level)
    return info["count"] if info else "no level"


SESSION_CAP_REASON = "session over 100 questions: driver plays this game's shape badly"
TARGET = 40
BLOCK_MINUTES = 90
BLOCK_HOURS = 2
NOT_QUESTION_GAMES = {
    "prisoners-dilemma": "not a question game: 20 rounds of a choice with no right answer (index.html:31, :314)",
}
DEADLINE = [None]  # time.time() after which no new session starts (--hours); None for no limit


def scope(slug, level, n_levels):
    """Amendment 1 (option C): a level is in scope when its game serves more than one level and its B4 count is
    not scoped to that level (scoped_to_level false), whether the game keeps named arrays or one array filtered
    by a field. Returns (in_scope, reason)."""
    if slug in NOT_QUESTION_GAMES:
        return False, NOT_QUESTION_GAMES[slug]
    if n_levels < 2:
        return False, "single-level game"
    path = os.path.join(bc.BANKS_DIR, slug + ".json")
    if not os.path.exists(path):
        return False, "no extraction (B4 has no count)"
    with open(path, "r", encoding="utf-8") as fh:
        bank = json.load(fh)
    if bank.get("generator"):
        return False, "generator (B4 has no count)"
    info = bank.get("levels", {}).get(level)
    if not info:
        return False, "level not in the extraction (B4 has no count)"
    if info.get("scoped_to_level"):
        return False, "B4 count scoped to the level"
    return True, ""


async def measure_level(browser, base, slug, level, log=print):
    t0 = time.time()
    seen, seen_opts = {}, set()
    per_session, statuses, repeats, started = [], [], [], []
    never_ended, stale, stop = 0, 0, ""
    unsupported_detail = ""
    first_option_sets = None
    n = 0
    for n in range(1, MAX_SESSIONS + 1):
        if DEADLINE[0] is not None and time.time() > DEADLINE[0]:
            stop = "time limit"
            break
        res, records = await play_session(browser, base, slug, level, n)
        statuses.append(res["status"])
        started.extend((r["level"], r["mode"]) for r in records if r.get("t") == "start")
        sv = servings(records)
        if res["status"] == "UNSUPPORTED" and n == 1:
            unsupported_detail = res["detail"]
            per_session.append(len(sv))
            for ident, oid in sv:
                seen.setdefault(ident, (n, 0))
                seen_opts.add(oid)
            stop = "unsupported"
            break
        if res["status"] == "FAIL" and n == 1 and not sv:
            unsupported_detail = "FAIL: " + res["detail"]
            per_session.append(0)
            stop = "fail"
            break
        if res["played"] >= MAX_QUESTIONS and "game ended" not in res.get("detail", ""):
            never_ended += 1
            per_session.append(len(sv))
            unsupported_detail = SESSION_CAP_REASON
            stop = "session cap"
            break
        per_session.append(len(sv))
        if first_option_sets is None:
            first_option_sets = sorted({oid for _, oid in sv})
        added = 0
        pos = {}
        for i, (ident, oid) in enumerate(sv):
            if ident in pos:
                repeats.append({"seed": n, "question": json.loads(ident), "first": pos[ident] + 1, "again": i + 1,
                                "consecutive": i == pos[ident] + 1})
            else:
                pos[ident] = i
            if ident not in seen:
                seen[ident] = (n, i + 1)
                added += 1
            seen_opts.add(oid)
        stale = 0 if added else stale + 1
        if len(seen) >= TARGET:
            stop = "reached 40"
            break
        if stale >= SATURATION_RUN:
            stop = "saturated"
            break
    else:
        stop = "max sessions"

    distinct = len(seen)
    if stop in ("unsupported", "fail", "session cap"):
        verdict = "UNMEASURED"
    elif distinct >= 40:
        verdict = "40+"
    elif stop == "saturated":
        verdict = "UNDER 40"
    elif stop == "time limit":
        verdict = "UNFINISHED"
    else:
        verdict = "UNSATURATED"
    lv_modes = sorted({"%s/%s" % (a, b) if b is not None else a for a, b in started})
    samples = sorted(seen, key=lambda k: seen[k])
    row = {
        "slug": slug, "level": level, "b4": b4_count(slug, level), "verdict": verdict,
        "distinct": distinct, "distinct_options_only": len(seen_opts),
        "sessions": len(per_session), "questions_per_session": per_session,
        "saturated": stop == "saturated", "stop": stop, "never_ended_sessions": never_ended,
        "statuses": {s: statuses.count(s) for s in sorted(set(statuses))},
        "tier3_reason": unsupported_detail, "started_as": lv_modes,
        "in_session_repeats": repeats,
        "first_session_option_sets": len(first_option_sets) if first_option_sets is not None else None,
        "first_session_typed_only": first_option_sets == [json.dumps([])] if first_option_sets else False,
        "questions": [json.loads(k) for k in (samples if distinct < 60 else samples[:12])],
        "seconds": round(time.time() - t0, 1),
    }
    log("  %-30s %-8s %-12s distinct %3d (options only %3d) in %2d session(s), %s, B4 %s, %ds%s"
        % (slug, level, verdict, distinct, len(seen_opts), len(per_session), stop, row["b4"], row["seconds"],
           ("; %d in-session repeat(s)" % len(repeats)) if repeats else ""))
    return row


def _load_json():
    if os.path.exists(OUT_JSON):
        with open(OUT_JSON, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def _save_json(data):
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    tmp = OUT_JSON + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as fh:
        json.dump(data, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    os.replace(tmp, OUT_JSON)


def save_row(row):
    """Amendment 2 step 4: merge one finished level into the JSON by (slug, level), then regenerate the md."""
    data = _load_json()
    data.setdefault("contract", "B4-SERVED-AUDIT")
    data["generated_by"] = "scripts/audit-served.py"
    data["rule"] = {"target": TARGET, "saturation_run": SATURATION_RUN, "max_sessions": MAX_SESSIONS,
                    "max_questions": MAX_QUESTIONS}
    key = (row["slug"], row["level"])
    levels = [r for r in data.get("levels", []) if (r["slug"], r["level"]) != key]
    row = dict(row, measured=time.strftime("%Y-%m-%d %H:%M"), commit=subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip())
    levels.append(row)
    data["levels"] = levels
    _save_json(data)
    write_md(data)


async def run_levels(jobs, workers, overrides=None, log=print, save=False):
    from playwright.async_api import async_playwright
    srv, base = start_server(overrides)
    rows = []
    try:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            sem = asyncio.Semaphore(workers)

            async def one(slug, level):
                async with sem:
                    try:
                        row = await measure_level(browser, base, slug, level, log)
                    except Exception as exc:  # a driver crash is a row, never a lost level
                        row = {"slug": slug, "level": level, "b4": b4_count(slug, level),
                               "verdict": "UNMEASURED", "tier3_reason": "audit error: %s" % str(exc)[:200],
                               "distinct": 0, "distinct_options_only": 0, "sessions": 0,
                               "questions_per_session": [], "saturated": False, "stop": "error",
                               "never_ended_sessions": 0, "statuses": {}, "started_as": [],
                               "in_session_repeats": [], "first_session_option_sets": None,
                               "first_session_typed_only": False, "questions": [], "seconds": 0}
                        log("  %-30s %-8s audit error: %s" % (slug, level, str(exc)[:120]))
                    rows.append(row)
                    if save:
                        save_row(row)
            await asyncio.gather(*(one(s, lv) for s, lv in jobs))
            await browser.close()
    finally:
        srv.shutdown()
    order = {j: i for i, j in enumerate(jobs)}
    return sorted(rows, key=lambda r: order[(r["slug"], r["level"])])


# --------------------------------------------------------------------------- the time estimate

async def estimate_levels(jobs, workers, log=print):
    """One session (seed 1) per level: its status, questions and seconds (contract STOP IF: a full run over 90
    minutes at --workers 4 is reported, with the slowest games first, before it is started)."""
    from playwright.async_api import async_playwright
    srv, base = start_server()
    rows = []
    try:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            sem = asyncio.Semaphore(workers)

            async def one(slug, level):
                async with sem:
                    t0 = time.time()
                    try:
                        res, records = await play_session(browser, base, slug, level, 1)
                        status, detail, n = res["status"], res["detail"], len(servings(records))
                    except Exception as exc:
                        status, detail, n = "ERROR", str(exc)[:200], 0
                    row = {"slug": slug, "level": level, "status": status, "detail": detail, "questions": n,
                           "seconds": round(time.time() - t0, 1)}
                    rows.append(row)
                    log("  %-30s %-8s %-11s %3d q %5.0fs  %s" % (slug, level, status, n, row["seconds"],
                                                                 cs.ascii_safe(detail)[:70]))
            await asyncio.gather(*(one(s, lv) for s, lv in jobs))
            await browser.close()
    finally:
        srv.shutdown()
    return rows


def project(rows, workers=4):
    """(best, worst) wall seconds of a full run: a drivable level plays SATURATION_RUN + 1 sessions at best and
    MAX_SESSIONS at worst, an undrivable one plays one; levels are dealt longest first to `workers` lanes."""
    def wall(costs):
        lanes = [0.0] * workers
        for c in sorted(costs, reverse=True):
            lanes[lanes.index(min(lanes))] += c
        return max(lanes) if lanes else 0.0
    drivable = lambda r: r["status"] in ("PASS", "WARN") and r["questions"] > 0
    best = [r["seconds"] * (SATURATION_RUN + 1) if drivable(r) else r["seconds"] for r in rows]
    worst = [r["seconds"] * MAX_SESSIONS if drivable(r) else r["seconds"] for r in rows]
    return wall(best), wall(worst)


# --------------------------------------------------------------------------- self-tests

SELFTESTS = [
    ("a", "formula-unlocked", "38895242", "alevel",
     "UNDER 40, distinct 25 or fewer, at least one in-session repeat",
     lambda r: r["verdict"] == "UNDER 40" and r["distinct"] <= 25 and len(r["in_session_repeats"]) >= 1),
    ("b", "scale-factor-scaling", "65ae674", "gcse", "UNDER 40, distinct exactly 38",
     lambda r: r["verdict"] == "UNDER 40" and r["distinct"] == 38),
    ("c", "formula-unlocked", "28be68a", "alevel", "distinct 40 or more, no in-session repeat",
     lambda r: r["distinct"] >= 40 and not r["in_session_repeats"]),
]


def page_at(commit, slug):
    return subprocess.run(["git", "show", "%s:games/%s/index.html" % (commit, slug)], cwd=ROOT,
                          capture_output=True, check=True).stdout


def selftest(workers, which="abc"):
    results = []
    for tag, slug, commit, level, want, ok in SELFTESTS:
        if tag not in which:
            continue
        body = page_at(commit, slug)
        overrides = {"/games/%s/index.html" % slug: body, "/games/%s/" % slug: body}
        print("self-test %s: %s at %s, level %s (want: %s)" % (tag, slug, commit, level, want))
        row = asyncio.run(run_levels([(slug, level)], 1, overrides))[0]
        passed = bool(ok(row))
        results.append({"test": tag, "slug": slug, "commit": commit, "level": level, "want": want,
                        "passed": passed, "verdict": row["verdict"], "distinct": row["distinct"],
                        "distinct_options_only": row["distinct_options_only"], "sessions": row["sessions"],
                        "saturated": row["saturated"], "in_session_repeats": len(row["in_session_repeats"]),
                        "started_as": row["started_as"], "questions_per_session": row["questions_per_session"]})
        print("  -> %s\n" % ("PASS" if passed else "FAIL"))
    if results:
        data = {}
        if os.path.exists(OUT_JSON):
            with open(OUT_JSON, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        kept = {t["test"]: t for t in data.get("selftests", [])}
        kept.update({t["test"]: dict(t, measured=time.strftime("%Y-%m-%d %H:%M")) for t in results})
        data["selftests"] = [kept[k] for k in sorted(kept)]
        _save_json(data)
        if data.get("levels") or data.get("blocks"):
            write_md(data)
    bad = [r for r in results if not r["passed"]]
    print("self-tests: %d of %d pass" % (len(results) - len(bad), len(results)))
    return results


# --------------------------------------------------------------------------- scope and blocks

def scoped_jobs():
    """(in-scope jobs in roster order, out-of-scope rows), Amendment 1's scope C less prisoners-dilemma."""
    levels, order = bc.roster_levels()
    est = {(r["slug"], r["level"]): r for r in _load_json().get("estimate", {}).get("levels", [])}
    jobs, out = [], []
    for s in order:
        for lv in levels.get(s, []):
            ok, why = scope(s, lv, len(levels.get(s, [])))
            if ok:
                jobs.append((s, lv))
            else:
                e = est.get((s, lv), {})
                out.append({"slug": s, "level": lv, "b4": b4_count(s, lv), "reason": why,
                            "tier3_estimate": ("%s: %s" % (e["status"], e["detail"])) if e else "not run"})
    return jobs, out


def projected_cost(e):
    """Seconds one level is projected to take under Amendment 2's stop rule, from its one-session estimate."""
    if not e:
        return 60.0 * SATURATION_RUN  # no estimate: a guess, flagged in the split
    q = e.get("questions") or 0
    capped = e["detail"].startswith("played %d question" % MAX_QUESTIONS)  # the session cap ends it at once
    if e["status"] not in ("PASS", "WARN") or q == 0 or capped:
        return float(e["seconds"])
    sessions = min(MAX_SESSIONS, 2 * -(-TARGET // q) + SATURATION_RUN)
    return float(e["seconds"]) * sessions


def lanes_wall(costs, workers=4):
    lanes = [0.0] * workers
    for c in sorted(costs, reverse=True):
        lanes[lanes.index(min(lanes))] += c
    return max(lanes) if costs else 0.0


def make_split(jobs, workers=4):
    est = {(r["slug"], r["level"]): r for r in _load_json().get("estimate", {}).get("levels", [])}
    cost = {j: projected_cost(est.get(j)) for j in jobs}
    blocks = []
    for j in sorted(jobs, key=lambda j: -cost[j]):  # first fit, longest first
        for b in blocks:
            if lanes_wall([cost[x] for x in b] + [cost[j]], workers) <= BLOCK_MINUTES * 60:
                b.append(j)
                break
        else:
            blocks.append([j])
    return [{"block": i + 1, "levels": [list(j) for j in b],
             "projected_minutes": round(lanes_wall([cost[x] for x in b], workers) / 60, 1),
             "level_minutes": {"%s/%s" % j: round(cost[j] / 60, 1) for j in b},
             "status": "pending", "moved_in": [], "moved_out": []} for i, b in enumerate(blocks)]


def fixed_split():
    """The split, written to the JSON the first time it is asked for and never recomputed (Amendment 2 step 5)."""
    data = _load_json()
    if not data.get("blocks"):
        jobs, out = scoped_jobs()
        data["blocks"] = make_split(jobs)
        data["out_of_scope"] = out
        data["scope"] = "c less prisoners-dilemma (Amendments 1 and 2)"
        _save_json(data)
        write_md(data)
    return data["blocks"]


# --------------------------------------------------------------------------- report

VERDICT_ORDER = {"UNDER 40": 0, "UNSATURATED": 1, "UNFINISHED": 2, "UNMEASURED": 3, "40+": 4}


def _cell(text):
    return str(text).replace("|", "/").replace("\n", " ")


def write_md(data):
    """Amendment 2 step 8: the summary so far, the rule, the self-tests, the split, every level measured, the
    in-session repeats, the known and allowed repeat, the out-of-scope levels. Regenerated from the whole JSON."""
    rows = sorted(data.get("levels", []), key=lambda r: (VERDICT_ORDER.get(r["verdict"], 9), r["slug"], r["level"]))
    blocks = data.get("blocks", [])
    oos = data.get("out_of_scope", [])
    in_scope = {tuple(j) for b in blocks for j in b["levels"]}
    counts = {v: sum(1 for r in rows if r["verdict"] == v) for v in VERDICT_ORDER}
    disagree = [r for r in rows if r["verdict"] == "UNDER 40" and isinstance(r["b4"], int) and r["b4"] >= 40]
    reps = [(r, x) for r in rows for x in r.get("in_session_repeats", [])]
    notes = data.get("notes", [])
    noted = {(n["slug"], n["level"]) for n in notes}
    one_set = [r for r in rows if r.get("first_session_option_sets") == 1 and (r["slug"], r["level"]) not in noted]
    done = [b for b in blocks if b["status"] == "done"]
    capped = [r for r in rows if r.get("stop") == "session cap"]
    t3 = [r for r in rows if r["verdict"] == "UNMEASURED" and r.get("stop") != "session cap"]
    measured = [r for r in rows if r["verdict"] != "UNFINISHED"]
    out = ["# Served-question audit, November 2026 (B4-SERVED-AUDIT)", "",
           "Generated by `scripts/audit-served.py`. Report only: no game and no check changed.", "",
           "## Summary so far", "",
           "- Blocks done: %d of %d." % (len(done), len(blocks)),
           "- Levels measured so far: %d of %d in scope, in %d game(s)%s." % (
               len(measured), len(in_scope), len({r["slug"] for r in measured}),
               "; every in-scope level is covered" if blocks and len(done) == len(blocks)
               and {(r["slug"], r["level"]) for r in measured} >= in_scope else ""),
           "- Verdicts so far: %s." % ", ".join("%s %d" % (v, counts[v]) for v in VERDICT_ORDER),
           "- Of the UNMEASURED: %d by tier 3 (it cannot play the level), %d by the session cap." % (
               len(t3), len(capped)),
           "- Levels where B4 counts 40 or more but the level serves under 40: %d." % len(disagree)]
    out += ["  - `%s` %s: B4 %s, served %d" % (r["slug"], r["level"], r["b4"], r["distinct"]) for r in disagree]
    out += ["- In-session repeats so far: %d in %d level(s) (listed below)." % (
        len(reps), len({(r["slug"], r["level"]) for r, _ in reps})),
        "- Possibly not a question game (first session showed one option set; played as normal, for Project "
        "Claude to rule on): %d level(s)." % len(one_set)]
    out += ["  - `%s` %s%s" % (r["slug"], r["level"], " (typed answers: no options on screen)"
                               if r.get("first_session_typed_only") else "") for r in one_set]
    reasons = {}
    for o in oos:
        reasons.setdefault(o["reason"], []).append(o)
    out += ["", "## Scope", "",
            "In scope (Amendment 1, option C, less prisoners-dilemma by Amendment 2): every level of a game that "
            "serves more than one level whose B4 count is not scoped to that level (`scoped_to_level` false in the "
            "extraction), whether the game keeps named arrays or one array filtered by a field: %d level(s). "
            "Out of scope: %d level(s):" % (len(in_scope), len(oos)), ""]
    out += ["- %s: %d level(s)" % (k, len(v)) for k, v in sorted(reasons.items())]
    out += ["", "Every out-of-scope level is listed at the end with tier 3's one-session result from the "
            "estimate pass.", "",
            "## The rule", "",
            "A served question's identity is its option set (the sorted option identities as tier 3 reads them: "
            "dataset.val, else the KaTeX annotation, else the stripped text) joined with the visible prompt text "
            "(the nearest ancestor of the options with text of its own, leaving out buttons, links, header, footer "
            "and score, timer, streak, lives and progress readouts). Each session is a fresh page with Math.random "
            "replaced by PHONE_SEED's mulberry32 seeded with the session number.", "",
            "Stop rule, checked after each session: %d or more distinct ends the level as 40+; otherwise %d "
            "sessions in a row adding no new question ends it (saturated), and %d sessions ends it. A session "
            "still running at %d questions ends the level as UNMEASURED (\"%s\")." % (
                TARGET, SATURATION_RUN, MAX_SESSIONS, MAX_QUESTIONS, SESSION_CAP_REASON), "",
            "**In-session repeats are recorded for every session played, so a 40+ level was checked for them only "
            "in the sessions it took to reach 40. This is not a full repeat check.**", "",
            "Verdicts: UNDER 40 (saturated, distinct < 40), 40+ (distinct >= 40), UNSATURATED (40 sessions, "
            "distinct < 40), UNFINISHED (the block's %d-hour backstop came first; moved to a later block), "
            "UNMEASURED (tier 3 cannot play it, or the session cap; the reason given)." % BLOCK_HOURS, "",
            "## Self-tests", "", "| Test | Game at commit, level | Want | Measured | Result |",
            "|---|---|---|---|---|"]
    for t in data.get("selftests", []):
        out.append("| %s | `%s` at %s, %s | %s | %s, distinct %d (options only %d), %d sessions, %d in-session "
                   "repeat(s) | %s |" % (t["test"], t["slug"], t["commit"], t["level"], _cell(t["want"]), t["verdict"],
                                         t["distinct"], t["distinct_options_only"], t["sessions"],
                                         t["in_session_repeats"], "PASS" if t["passed"] else "FAIL"))
    out += ["", "## Block split (fixed before block 1)", "",
            "Each level's projected cost is its one-session estimate times min(%d, 2 x ceil(40 / questions in "
            "that session) + %d) sessions; one session for a level tier 3 cannot drive or whose session hit the "
            "cap. Blocks are filled longest first to at most %d minutes at 4 workers." % (
                MAX_SESSIONS, SATURATION_RUN, BLOCK_MINUTES), "",
            "| Block | Projected minutes | Levels | Status | Moves |", "|---|---|---|---|---|"]
    for b in blocks:
        moves = "; ".join(["in: " + ", ".join(m) for m in [b.get("moved_in", [])] if m]
                          + ["out: " + ", ".join(m) for m in [b.get("moved_out", [])] if m])
        out.append("| %d | %s | %s | %s | %s |" % (b["block"], b["projected_minutes"], ", ".join(
            "`%s` %s" % tuple(j) for j in b["levels"]), b["status"], moves))
    out += ["", "## Every level measured", "",
            "| Game | Level | B4 count | Distinct served | Sessions | Ended by | Verdict | Note |",
            "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        out.append("| `%s` | %s | %s | %s | %s | %s | %s | %s |" % (
            r["slug"], r["level"], r["b4"], r["distinct"] if r["verdict"] != "UNMEASURED" else "-", r["sessions"],
            r.get("stop", ""), r["verdict"], _cell(r.get("tier3_reason") or "")[:140]))
    out += ["", "## In-session repeats", "", "%d repeat(s) in %d level(s)." % (
        len(reps), len({(r["slug"], r["level"]) for r, _ in reps})), ""]
    if reps:
        out += ["| Game | Level | Seed | Question | First served | Again |", "|---|---|---|---|---|---|"]
        out += ["| `%s` | %s | %s | %s | %s | %s |" % (r["slug"], r["level"], x["seed"], _cell(x["question"])[:120],
                                                       x["first"], x["again"]) for r, x in reps]
    out += ["", "## Known and allowed: expectation-station's repeated tiles", "",
            "Tier 3 WARNs that expectation-station shows one value twice (A-Level: 5, 5.1, 5.5, 6, 6; Core: 0, 0.3, "
            "0.3, 0.35, 0.45, 0.55). These are tile banks, not pick-one groups. Stage 2's bank is every correct "
            "product x times P(X = x) plus distractors, and `generateProductDistractors` never offers a key already "
            "used (index.html:1506-1519), so a value appears twice only when two cells of the products table are "
            "equal and both correct. Both WARNs are such items: A-Level es_alevel_027 (products 5, 6, 6; "
            "distractors 5.1, 5.5) and Core es_core_022 (products 0, 0.45, 0.3, 0.3; distractors 0.35, 0.55). "
            "scripts/checker-allowlist.json's `tier3_exceptions` records the same shape for Stage 1 (es_gcse_001, "
            "two cells of 0.25). Known and allowed, not a finding."]
    out += ["", "## Notes (Project Claude's rulings)", ""]
    if notes:
        out += ["| Game | Level | Ruling | Reason | Date |", "|---|---|---|---|---|"]
        out += ["| `%s` | %s | %s | %s | %s |" % (n["slug"], n["level"], _cell(n["ruling"]), _cell(n["reason"]), n["date"])
                for n in notes]
    else:
        out.append("None.")
    if oos:
        out += ["", "## Out of scope", "", "| Game | Level | B4 count | Why out of scope | Tier 3, one session |",
                "|---|---|---|---|---|"]
        out += ["| `%s` | %s | %s | %s | %s |" % (o["slug"], o["level"], o["b4"], o["reason"],
                                                 _cell(o["tier3_estimate"])[:110]) for o in oos]
    with open(OUT_MD, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(out) + "\n")


def finish_block(n, rows):
    """Mark block n done; move every UNFINISHED level into block n + 1 (made if needed) and record the move."""
    data = _load_json()
    blocks = data["blocks"]
    b = blocks[n - 1]
    cut = [[r["slug"], r["level"]] for r in rows if r["verdict"] == "UNFINISHED"]
    b["status"] = "done"
    b["ran"] = time.strftime("%Y-%m-%d %H:%M")
    if cut:
        b["moved_out"] = ["%s/%s" % tuple(j) for j in cut]
        if len(blocks) == n:
            blocks.append({"block": n + 1, "levels": [], "projected_minutes": None, "level_minutes": {},
                           "status": "pending", "moved_in": [], "moved_out": []})
        nxt = blocks[n]
        nxt["levels"] += [j for j in cut if j not in nxt["levels"]]
        nxt["moved_in"] += ["%s/%s (from block %d)" % (j[0], j[1], n) for j in cut]
    _save_json(data)
    write_md(data)
    return cut


def main():
    ap = argparse.ArgumentParser(description="Measure how many different questions each game's level serves.")
    ap.add_argument("--only", help="substring filter on slug, over every roster level (rows still saved)")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--selftest", nargs="?", const="abc", metavar="TESTS",
                    help="the self-tests only; optionally which, e.g. --selftest c")
    ap.add_argument("--estimate", metavar="FILE",
                    help="play one session per level and write the time estimate to FILE (no audit output)")
    ap.add_argument("--list-blocks", action="store_true", help="fix the split (first time only) and print it")
    ap.add_argument("--block", type=int, help="run block N of the fixed split")
    ap.add_argument("--hours", type=float, help="start no new session after this many hours (UNFINISHED rows); "
                                                "--block defaults to %d" % BLOCK_HOURS)
    args = ap.parse_args()

    if args.selftest:
        tests = selftest(args.workers, args.selftest)
        return 0 if tests and all(t["passed"] for t in tests) else 1

    if args.list_blocks or args.block:
        blocks = fixed_split()
        for b in blocks:
            print("block %d: %s min projected, %d level(s), %s: %s" % (
                b["block"], b["projected_minutes"], len(b["levels"]), b["status"],
                ", ".join("%s/%s" % tuple(j) for j in b["levels"])))
        if not args.block:
            return 0
        if not 1 <= args.block <= len(blocks):
            print("no block %d (the split has %d)" % (args.block, len(blocks)))
            return 2
        jobs = [tuple(j) for j in blocks[args.block - 1]["levels"]]
        est = {(r["slug"], r["level"]): r for r in _load_json().get("estimate", {}).get("levels", [])}
        jobs.sort(key=lambda j: -projected_cost(est.get(j)))
        DEADLINE[0] = time.time() + (args.hours or BLOCK_HOURS) * 3600
        print("block %d: %d level(s), %d worker(s), backstop %.1f h" % (
            args.block, len(jobs), args.workers, args.hours or BLOCK_HOURS))
        t0 = time.time()
        rows = asyncio.run(run_levels(jobs, args.workers, save=True))
        cut = finish_block(args.block, rows)
        counts = {}
        for r in rows:
            counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
        print("\nblock %d done in %.0fs: %s%s" % (args.block, time.time() - t0, ", ".join(
            "%s %d" % kv for kv in sorted(counts.items())), ("; moved to block %d: %s" % (
                args.block + 1, ", ".join("%s/%s" % tuple(j) for j in cut))) if cut else ""))
        return 0

    levels, order = bc.roster_levels()
    jobs = [(s, lv) for s in order for lv in levels.get(s, []) if not args.only or args.only in s]
    if not args.estimate and not args.only:
        print("give --block N, --list-blocks, --only <slug>, --estimate FILE or --selftest")
        return 2
    print("audit-served: %d level(s) across %d game(s), %d worker(s)" % (len(jobs), len({s for s, _ in jobs}),
                                                                        args.workers))
    t0 = time.time()
    if args.estimate:
        rows = asyncio.run(estimate_levels(jobs, args.workers))
        best, worst = project(rows, 4)
        with open(args.estimate, "w", encoding="utf-8", newline="") as fh:
            json.dump({"seconds": round(time.time() - t0), "workers": args.workers,
                       "projected_seconds_at_4_workers": {"best": round(best), "worst": round(worst)},
                       "levels": sorted(rows, key=lambda r: -r["seconds"])}, fh, indent=1, ensure_ascii=False)
        print("\nestimate pass: %.0fs; a full run at --workers 4 projects to %.0f to %.0f minutes; wrote %s"
              % (time.time() - t0, best / 60, worst / 60, args.estimate))
        return 0
    if args.hours:
        DEADLINE[0] = time.time() + args.hours * 3600
    rows = asyncio.run(run_levels(jobs, args.workers, save=True))
    print("\n%d level(s) saved (%.0fs)" % (len(rows), time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
