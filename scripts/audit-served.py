#!/usr/bin/env python3
# ci-held: a hand-run audit that plays whole sessions of every game, far longer than any CI budget (contract B4-SERVED-AUDIT: report only, never in CI; results in docs/audits/)
"""How many different questions does each game's level actually serve? (contract B4-SERVED-AUDIT, 23 Nov 2026)

    python -X utf8 scripts/audit-served.py --selftest            # the three self-tests; run these first
    python -X utf8 scripts/audit-served.py --workers 4           # every roster game and level
    python -X utf8 scripts/audit-served.py --only scale-factor   # substring filter on slug

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

THE STOP RULE: a level stops when SATURATION_RUN (8) sessions in a row add no new question (saturated), or at
MAX_SESSIONS (40). A level whose first session tier 3 cannot drive (UNSUPPORTED) is played once and reported
UNMEASURED with tier 3's reason.

VERDICT: UNDER 40 (saturated, distinct < 40), 40+ (distinct >= 40), UNSATURATED (40 sessions, distinct < 40),
UNMEASURED (tier 3 cannot play it). A question served twice in one session is listed with game, level, seed and
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

  const origClick = window.__mfgClickOpt;
  window.__mfgClickOpt = function (i) { record('opt'); return origClick(i); };
  const origType = window.__mfgTypeAnswer;
  window.__mfgTypeAnswer = function (v) { record('typed'); return origType(v); };
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
        res = await cs.play_one(ctx, base, "game:" + slug, "games/%s/index.html" % slug, "?level=" + level,
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


async def measure_level(browser, base, slug, level, log=print):
    t0 = time.time()
    seen, seen_opts = {}, set()
    per_session, statuses, repeats, started = [], [], [], []
    never_ended, stale, stop = 0, 0, ""
    unsupported_detail = ""
    n = 0
    for n in range(1, MAX_SESSIONS + 1):
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
        if stale >= SATURATION_RUN:
            stop = "saturated"
            break
    else:
        stop = "max sessions"

    distinct = len(seen)
    if stop in ("unsupported", "fail"):
        verdict = "UNMEASURED"
    elif distinct >= 40:
        verdict = "40+"
    elif stop == "saturated":
        verdict = "UNDER 40"
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
        "questions": [json.loads(k) for k in (samples if distinct < 60 else samples[:12])],
        "seconds": round(time.time() - t0, 1),
    }
    log("  %-30s %-8s %-12s distinct %3d (options only %3d) in %2d session(s), %s, B4 %s, %ds%s"
        % (slug, level, verdict, distinct, len(seen_opts), len(per_session), stop, row["b4"], row["seconds"],
           ("; %d in-session repeat(s)" % len(repeats)) if repeats else ""))
    return row


async def run_levels(jobs, workers, overrides=None, log=print):
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
                        rows.append(await measure_level(browser, base, slug, level, log))
                    except Exception as exc:  # a driver crash is a row, never a lost level
                        rows.append({"slug": slug, "level": level, "b4": b4_count(slug, level),
                                     "verdict": "UNMEASURED", "tier3_reason": "audit error: %s" % str(exc)[:200],
                                     "distinct": 0, "distinct_options_only": 0, "sessions": 0,
                                     "questions_per_session": [], "saturated": False, "stop": "error",
                                     "never_ended_sessions": 0, "statuses": {}, "started_as": [],
                                     "in_session_repeats": [], "questions": [], "seconds": 0})
                        log("  %-30s %-8s audit error: %s" % (slug, level, str(exc)[:120]))
            await asyncio.gather(*(one(s, lv) for s, lv in jobs))
            await browser.close()
    finally:
        srv.shutdown()
    order = {j: i for i, j in enumerate(jobs)}
    return sorted(rows, key=lambda r: order[(r["slug"], r["level"])])


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


def selftest(workers):
    results = []
    for tag, slug, commit, level, want, ok in SELFTESTS:
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
    bad = [r for r in results if not r["passed"]]
    print("self-tests: %d of %d pass" % (len(results) - len(bad), len(results)))
    return results


# --------------------------------------------------------------------------- report

def write_outputs(rows, tests, seconds, workers):
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    data = {"contract": "B4-SERVED-AUDIT", "generated_by": "scripts/audit-served.py", "date": "2026-11-23",
            "commit": subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True,
                                     text=True).stdout.strip(),
            "rule": {"saturation_run": SATURATION_RUN, "max_sessions": MAX_SESSIONS, "max_questions": MAX_QUESTIONS},
            "seconds": round(seconds), "workers": workers, "selftests": tests, "levels": rows}
    with open(OUT_JSON, "w", encoding="utf-8", newline="") as fh:
        json.dump(data, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print("wrote %s" % os.path.relpath(OUT_JSON, ROOT))


def main():
    ap = argparse.ArgumentParser(description="Measure how many different questions each game's level serves.")
    ap.add_argument("--only", help="substring filter on slug")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--selftest", action="store_true", help="the three self-tests (contract step 3) only")
    ap.add_argument("--no-write", action="store_true", help="print only; write no JSON")
    args = ap.parse_args()

    tests = selftest(args.workers) if args.selftest else []
    if args.selftest:
        return 0 if all(t["passed"] for t in tests) else 1

    levels, order = bc.roster_levels()
    jobs = [(s, lv) for s in order for lv in levels.get(s, [])
            if not args.only or args.only in s]
    print("audit-served: %d level(s) across %d game(s), %d worker(s)" % (len(jobs), len({s for s, _ in jobs}),
                                                                        args.workers))
    t0 = time.time()
    rows = asyncio.run(run_levels(jobs, args.workers))
    secs = time.time() - t0
    counts = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    print("\n%s  (%.0fs)" % (", ".join("%s %d" % kv for kv in sorted(counts.items())), secs))
    if not args.no_write:
        write_outputs(rows, tests, secs, args.workers)
    return 0


if __name__ == "__main__":
    sys.exit(main())
