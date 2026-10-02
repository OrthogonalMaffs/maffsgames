#!/usr/bin/env python3
"""Independent verification for Six Sevens, Bruv (games/six-sevens-bruv/), built 30 Sep 2026.

WHY THIS READS THE LIVE PAGE
-------------------------------------------------------------------------------
Same reasoning as verify-log-laws.py / verify-graph-transformer.py: a Python copy of
the game's logic could drift from it and would then only be verifying itself. The
game keeps every decision a student sees -- the facts, the question forms, the hints,
the session queue, which grid cells are lit -- on window.SSB as plain functions, and
its own UI calls them through SSB. This script launches the stub server, loads the
page under Playwright and drives THOSE functions, then recomputes every answer here,
in Python, from the numbers the page shows.

WHAT IT ASSERTS
-------------------------------------------------------------------------------
  Facts      exactly the 78 unordered pairs a x b, 1 <= a <= b <= 12, each product
             equal to a*b recomputed here; the 12 x1 facts and only those start gold.
  Questions  every fact, both orientations, every form the game allows it: exactly
             one '?', never "c = ? x ?", the displayed product equals x*y, and exactly
             one integer in 0..1000 satisfies the displayed equation -- the stored
             answer. Square facts are product-form only (the missing-factor form would
             print its own answer). 3000 randomly built questions pass the same test.
  Hints      every x in 1..12, y in 1..12: the rule used is the one for whichever
             factor comes first in Jon's priority order (x1, x2, x10, x5, x4, x3, x6,
             x8, x9, x11, x12, x7); each step's value recomputed from its operation and
             operands; the last step equals x*y; every step value and the product appear
             in the hint text, and the text opens with "x x y".
  Lighting   for many gold sets, a cell shows a number iff its unordered fact is gold,
             and the number is r*c -- so both commutative cells light together and an
             unearned product is never displayed.
  Sessions   1,200 simulated sessions (24 seeds by default) (fresh / partial / nearly-full grids; 20, 40 and
             clear-the-grid; always right, always wrong, 30%, 70%, wrong-first-time):
             every session terminates; 20/40 serve exactly 20/40; clear-the-grid ends
             with the grid gold or at its safety ceiling; no fact is served while gold;
             every miss returns 3-5 questions later (earlier only once every fact in
             the pool has already been served) unless the session ended first.
  Boards     a 20-question session submits exactly one score, to level q20; a
             clear-the-grid session submits nothing and records history and its
             personal best under 'clear'.
  Analytics  every event carries level 'all' and mode q20 / q40 / clear, with the
             canon 1.3 parameters (question_index 1..n, correct, score,
             questions_answered, questions_correct, previous_best).
  UI         a real session played through the keyboard with the Firebase SDK
             blocked: MaffsInitials exists, a correct answer lights both cells in the
             DOM, no unearned cell shows text, a wrong answer shows the full x-by-y
             array, the hint and a Next control, the missed fact comes back, no gold
             fact repeats, and the named grid saves, resumes and deletes. Then again
             with storage blocked: the game runs session-only and says so.

FAULT-INJECTION SELF-TEST (runs every time; --no-selftest skips it)
-------------------------------------------------------------------------------
Each fault is patched into a FRESH page at run time (never into the file) and the
same checks must FAIL:  a wrong product in SSB.FACTS;  a wrong x9 hint rule;  hints
taken from the right-hand factor instead of the easier one;  a session that re-queues
a fact after it turns gold;  a session that forgets to bring a missed fact back.

USAGE
    python scripts/verify-six-sevens.py
    python scripts/verify-six-sevens.py --no-selftest
"""
import argparse
import os
import random
import re
import sys
import time
from urllib.parse import urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import bank_common as bc  # noqa: E402  (start_stub_server: checked start, free port)
SLUG = "six-sevens-bruv"
PORT = None  # set by main() to the free port the stub server got
MAX = 12
ALL_FACTS = {(a, b) for a in range(1, MAX + 1) for b in range(a, MAX + 1)}

_FAILURES = []


def fail(msg):
    _FAILURES.append(msg)
    print("FAIL: " + msg)


def key_of(x, y):
    a, b = min(x, y), max(x, y)
    return "%dx%d" % (a, b)


def parse_key(k):
    a, b = k.split("x")
    return int(a), int(b)


# ---------------------------------------------------------------- checks (pure)

def check_facts(facts, start_gold, out):
    seen = {}
    for f in facts:
        pair = (f["a"], f["b"])
        if f["key"] != key_of(*pair):
            out.append("fact %r has key %r, expected %r" % (pair, f["key"], key_of(*pair)))
        if pair in seen:
            out.append("fact %r appears twice" % (pair,))
        seen[pair] = f
        if f["product"] != f["a"] * f["b"]:
            out.append("fact %d x %d stores product %r, but %d x %d = %d"
                       % (f["a"], f["b"], f["product"], f["a"], f["b"], f["a"] * f["b"]))
    if set(seen) != ALL_FACTS:
        out.append("facts are not exactly the 78 pairs 1<=a<=b<=12 (missing %s, extra %s)"
                   % (sorted(ALL_FACTS - set(seen))[:5], sorted(set(seen) - ALL_FACTS)[:5]))
    want = {key_of(1, b) for b in range(1, MAX + 1)}
    if set(start_gold) != want:
        out.append("start gold is %s, expected the 12 x1 facts" % sorted(start_gold))


def solve_displayed(parts):
    """Every integer in 0..1000 that makes the displayed equation true."""
    if len(parts) != 5 or parts[1] != "×" or parts[3] != "=":
        return None
    slots = [p for p in (parts[0], parts[2], parts[4])]
    if slots.count("?") != 1:
        return None
    def val(p, k):
        return k if p == "?" else int(p)
    return [k for k in range(0, 1001) if val(slots[0], k) * val(slots[1], k) == val(slots[2], k)]


def check_question(q, out, where):
    parts = q["parts"]
    if parts.count("?") != 1:
        out.append("%s: %r does not have exactly one '?'" % (where, parts))
        return
    if parts[4] == "?" and q["form"] != "product":
        out.append("%s: form %s but the product is the unknown" % (where, q["form"]))
    if len(parts) != 5 or parts[1] != "×" or parts[3] != "=":
        out.append("%s: malformed question %r" % (where, parts))
        return
    x, y = q["x"], q["y"]
    if key_of(x, y) != q["key"]:
        out.append("%s: shows %d x %d but is fact %s" % (where, x, y, q["key"]))
    if parts[4] != "?" and int(parts[4]) != x * y:
        out.append("%s: %r shows product %s, but %d x %d = %d" % (where, parts, parts[4], x, y, x * y))
    sols = solve_displayed(parts)
    if sols != [q["answer"]]:
        out.append("%s: %r marks %r correct; the integers that satisfy it are %s"
                   % (where, parts, q["answer"], sols))
    if x == y and q["form"] != "product":
        out.append("%s: square fact %d x %d asked as %s, which prints its own answer" % (where, x, y, q["form"]))


def recompute_step(st):
    op, a = st["op"], st["args"]
    if op == "mul":
        return a[0] * a[1]
    if op == "add":
        return a[0] + a[1]
    if op == "sub":
        return a[0] - a[1]
    if op == "double":
        return 2 * a[0]
    if op == "half":
        return a[0] // 2 if a[0] % 2 == 0 else None
    return None


HINT_PRIORITY = [1, 2, 10, 5, 4, 3, 6, 8, 9, 11, 12, 7]   # Jon, 30 Sep 2026: the easier rule wins


def expected_factor(x, y):
    return x if HINT_PRIORITY.index(x) <= HINT_PRIORITY.index(y) else y


def check_hint(h, out):
    x, y = h["x"], h["y"]
    tag = "hint %d x %d (%s)" % (x, y, h.get("rule"))
    want = expected_factor(x, y)
    if h.get("factor") != want:
        out.append("%s: uses the x%s rule, but the priority order says x%d" % (tag, h.get("factor"), want))
    steps = h.get("steps") or []
    if not steps:
        out.append("%s: no steps" % tag)
        return
    for st in steps:
        v = recompute_step(st)
        if v is None or v != st["value"]:
            out.append("%s: step %s%r gives %r, hint says %r" % (tag, st["op"], st["args"], v, st["value"]))
    if steps[-1]["value"] != x * y:
        out.append("%s: ends at %r, but %d x %d = %d" % (tag, steps[-1]["value"], x, y, x * y))
    nums = set(int(n) for n in re.findall(r"\d+", h["text"]))
    for st in steps:
        if st["value"] not in nums:
            out.append("%s: step value %r is not in the text %r" % (tag, st["value"], h["text"]))
    if x * y not in nums:
        out.append("%s: product %d is not in the text" % (tag, x * y))
    if not h["text"].startswith("%d × %d" % (x, y)):
        out.append("%s: text does not open with the fact: %r" % (tag, h["text"][:30]))


def check_cells(cases, out):
    for gold, grid in cases:
        gset = set(gold)
        for r in range(1, MAX + 1):
            for c in range(1, MAX + 1):
                v = grid[r - 1][c - 1]
                lit = key_of(r, c) in gset
                if lit and v != r * c:
                    out.append("cell (%d,%d) is gold but shows %r, expected %d" % (r, c, v, r * c))
                if not lit and v is not None:
                    out.append("cell (%d,%d) is not earned but shows %r" % (r, c, v))


def check_sessions(scenarios, results, out, limit=8):
    before = len(out)
    for sc, res in zip(scenarios, results):
        tag = "session[%s len=%s policy=%s seed=%d]" % (sc["name"], sc["length"], sc["policy"], sc["seed"])
        pool = set(k for k in (key_of(a, b) for a, b in ALL_FACTS) if k not in set(sc["gold"]))
        if res["guardHit"] or not res["done"]:
            out.append("%s: did not terminate (guard hit=%s, done=%s)" % (tag, res["guardHit"], res["done"]))
            continue
        trace = res["trace"]
        if [t[0] for t in trace] != list(range(1, len(trace) + 1)):
            out.append("%s: question indices are not 1..n" % tag)
        gold = set(sc["gold"])
        first = {}
        for i, k, ok in trace:
            if k in gold:
                out.append("%s: q%d served %s, which was already gold" % (tag, i, k))
            if k not in pool:
                out.append("%s: q%d served %s, which is not in the session pool" % (tag, i, k))
            first.setdefault(k, i)
            if ok:
                gold.add(k)
        if set(res["gold"]) != gold:
            out.append("%s: engine's gold set differs from the answers given" % tag)
        n = len(trace)
        if sc["length"] == "clear":
            cap = 5 * len(pool)
            if n > cap:
                out.append("%s: served %d, over the ceiling %d" % (tag, n, cap))
            if not (pool <= gold or n == cap):
                out.append("%s: clear-the-grid stopped at %d with the grid not gold and the ceiling not reached" % (tag, n))
        else:
            if n != sc["length"]:
                out.append("%s: served %d questions, the button says %d" % (tag, n, sc["length"]))
        by_key = {}
        for i, k, ok in trace:
            by_key.setdefault(k, []).append((i, ok))
        all_first_before = lambda j: all(first.get(p, 10 ** 9) < j for p in pool)
        for k, seq in by_key.items():
            for idx, (i, ok) in enumerate(seq):
                if ok:
                    if idx + 1 < len(seq):
                        out.append("%s: %s served again at q%d after it was answered right at q%d"
                                   % (tag, k, seq[idx + 1][0], i))
                    continue
                if idx + 1 < len(seq):
                    j = seq[idx + 1][0]
                    gap = j - i
                    if gap > 5:
                        out.append("%s: %s missed at q%d came back at q%d (gap %d > 5)" % (tag, k, i, j, gap))
                    elif gap < 3 and not all_first_before(j):
                        out.append("%s: %s missed at q%d came back at q%d (gap %d < 3) while new facts were waiting"
                                   % (tag, k, i, j, gap))
                elif n >= i + 5:
                    out.append("%s: %s missed at q%d never came back (session ran to q%d)" % (tag, k, i, n))
        if len(out) - before > limit:
            out.append("... further session failures suppressed")
            return


# ---------------------------------------------------------------- page-side collection

SIM_JS = r"""
(args) => {
  const out = [];
  for (const sc of args) {
    const gold = {}; sc.gold.forEach(k => { gold[k] = true; });
    const s = SSB.createSession({ gold: gold, length: sc.length, rng: SSB.mulberry32(sc.seed * 7 + 1) });
    const prng = SSB.mulberry32(sc.seed * 13 + 5);
    const seen = {}; const trace = []; let guard = 0, guardHit = false;
    for (;;) {
      if (++guard > 20000) { guardHit = true; break; }
      const k = SSB.sessionNext(s);
      if (k === null) break;
      let ok;
      if (sc.policy === 'right') ok = true;
      else if (sc.policy === 'wrong') ok = false;
      else if (sc.policy === 'p30') ok = prng() < 0.3;
      else if (sc.policy === 'p70') ok = prng() < 0.7;
      else ok = !!seen[k];
      seen[k] = true;
      SSB.sessionAnswer(s, ok);
      trace.push([s.served, k, ok]);
    }
    out.push({ trace: trace, done: SSB.sessionDone(s), guardHit: guardHit, gold: Object.keys(s.gold) });
  }
  return out;
}
"""

COLLECT_JS = r"""
() => {
  const facts = SSB.FACTS.map(f => ({ key: f.key, a: f.a, b: f.b, product: f.product }));
  const startGold = Object.keys(SSB.startGold());
  const questions = [];
  SSB.FACTS.forEach(f => {
    SSB.formsFor(f).forEach(form => {
      [false, true].forEach(swap => { if (!swap || f.a !== f.b) questions.push(SSB.makeQuestion(f, swap, form)); });
    });
  });
  const rng = SSB.mulberry32(20260930);
  const sampled = [];
  for (let i = 0; i < 3000; i++) {
    const f = SSB.FACTS[Math.floor(rng() * SSB.FACTS.length)];
    sampled.push(SSB.buildQuestion(f.key, rng));
  }
  const hints = [];
  for (let x = 1; x <= 12; x++) for (let y = 1; y <= 12; y++) hints.push(SSB.hint(x, y));
  return { facts, startGold, questions: JSON.parse(JSON.stringify(questions)),
           sampled: JSON.parse(JSON.stringify(sampled)), hints: JSON.parse(JSON.stringify(hints)) };
}
"""

CELLS_JS = r"""
(golds) => golds.map(g => {
  const gold = {}; g.forEach(k => { gold[k] = true; });
  const grid = [];
  for (let r = 1; r <= 12; r++) { const row = []; for (let c = 1; c <= 12; c++) row.push(SSB.cellValue(r, c, gold)); grid.push(row); }
  return [g, grid];
})
"""


def gold_sets(seed):
    rnd = random.Random(seed)
    keys = sorted(key_of(a, b) for a, b in ALL_FACTS)
    x1 = [key_of(1, b) for b in range(1, MAX + 1)]
    sets = [[], x1, keys]
    for _ in range(12):
        sets.append(rnd.sample(keys, rnd.randint(1, 77)))
    return sets


def scenarios(seeds):
    keys = sorted(key_of(a, b) for a, b in ALL_FACTS)
    x1 = [key_of(1, b) for b in range(1, MAX + 1)]
    rest = [k for k in keys if k not in x1]
    out = []
    for seed in range(seeds):
        rnd = random.Random(1000 + seed)
        starts = {
            "fresh": x1,
            "partial": x1 + rnd.sample(rest, 36),       # pool 30
            "pool45": x1 + rnd.sample(rest, 21),        # pool 45
            "pool5": x1 + rnd.sample(rest, 61),
            "pool1": x1 + rnd.sample(rest, 65),
        }
        for name, gold in starts.items():
            pool = 78 - len(set(gold))
            lengths = [n for n in (20, 40) if n < pool] + ["clear"]
            for length in lengths:
                for policy in ("right", "wrong", "p30", "p70", "wrongFirst"):
                    out.append({"name": name, "gold": gold, "length": length, "policy": policy, "seed": seed})
    return out


async def new_page(browser, block_storage=False):
    ctx = await browser.new_context(viewport={"width": 1200, "height": 1000})
    await bc.no_next_floor(ctx)      # content checks; the floor is tested in test-next-control.py

    async def route(r):
        url = r.request.url
        if url.startswith("http://127.0.0.1:%d/" % PORT):
            await r.continue_()
        else:
            await r.abort()          # GA, Apps Script, Firebase SDK, fonts: nothing leaves the runner
    await ctx.route("**/*", route)
    if block_storage:
        await ctx.add_init_script("""
          Object.defineProperty(window, 'localStorage', { configurable: true,
            get: function () { throw new DOMException('blocked for test', 'SecurityError'); } });""")
    page = await ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    await page.goto("http://127.0.0.1:%d/games/%s/?cb=%d" % (PORT, SLUG, int(time.time() * 1000)),
                    wait_until="load", timeout=20000)
    await page.wait_for_function("!!window.SSB && !!window.SSB.ui", timeout=8000)
    return ctx, page, errors


async def collect_and_check(page, seeds):
    out = []
    data = await page.evaluate(COLLECT_JS)
    check_facts(data["facts"], data["startGold"], out)
    for i, q in enumerate(data["questions"]):
        check_question(q, out, "question %d" % i)
    for i, q in enumerate(data["sampled"]):
        check_question(q, out, "sampled question %d" % i)
    for h in data["hints"]:
        check_hint(h, out)
    cells = await page.evaluate(CELLS_JS, gold_sets(7))
    check_cells(cells, out)
    scs = scenarios(seeds)
    res = await page.evaluate(SIM_JS, scs)
    check_sessions(scs, res, out)
    return out, data, len(scs)


# ---------------------------------------------------------------- UI play-through

async def ui_state(page):
    return await page.evaluate("SSB.ui.state()")


async def wait_asking_or_done(page, prev_index):
    await page.wait_for_function(
        "(p) => { const s = SSB.ui.state(); const x = SSB.ui.session();"
        " return s === 'done' || (s === 'asking' && x && x.served > p); }", arg=prev_index, timeout=15000)


async def dom_cells(page):
    return await page.evaluate("""() => { const o = {};
      document.querySelectorAll('#gameGridWrap td').forEach(td => {
        o[td.dataset.r + ',' + td.dataset.c] = td.textContent; }); return o; }""")


def check_events(events, mode, n, right, out, tag):
    """Canon 1.3: level 'all' on every event, the session length as mode, and the
    required parameters (Jon, 30 Sep 2026)."""
    names = [e[0] for e in events]
    for name, p in events:
        if p.get("game_slug") != "six-sevens-bruv" or p.get("level") != "all" or p.get("mode") != mode:
            out.append("%s: %s sent game_slug=%r level=%r mode=%r; expected six-sevens-bruv/all/%s"
                       % (tag, name, p.get("game_slug"), p.get("level"), p.get("mode"), mode))
    if names.count("game_started") != 1 or names.count("game_completed") != 1:
        out.append("%s: events were %r" % (tag, sorted(set(names))))
    qa = [p for name, p in events if name == "question_answered"]
    if [p.get("question_index") for p in qa] != list(range(1, n + 1)):
        out.append("%s: question_index sequence %r" % (tag, [p.get("question_index") for p in qa][:25]))
    if any(not isinstance(p.get("correct"), bool) for p in qa):
        out.append("%s: question_answered without a boolean 'correct'" % tag)
    gc = [p for name, p in events if name == "game_completed"]
    if gc and (gc[0].get("questions_answered") != n or gc[0].get("questions_correct") != right
               or not isinstance(gc[0].get("score"), int)):
        out.append("%s: game_completed carried %r" % (tag, gc[0]))
    for name, p in events:
        if name == "personal_best_set" and not isinstance(p.get("previous_best"), int):
            out.append("%s: personal_best_set without previous_best" % tag)


async def ui_playthrough(browser, out):
    ctx, page, errors = await new_page(browser)
    try:
        if await page.evaluate("typeof window.firebase") != "undefined":
            out.append("UI: the Firebase SDK was meant to be blocked but loaded")
        if await page.evaluate("typeof window.MaffsInitials") != "object":
            out.append("UI: MaffsInitials missing with the Firebase SDK blocked")
        await page.click("#newGridBtn")
        await page.fill("#iniInput", "ass")
        await page.click("#iniCreate")
        if "not allowed" not in (await page.inner_text("#iniError")):
            out.append("UI: blocked initials ASS were accepted for a grid")
        await page.fill("#iniInput", "jfx")
        await page.click("#iniCreate")
        g = await page.evaluate("SSB.ui.grid()")
        if not g or g["initials"] != "JFX" or not g["saved"]:
            out.append("UI: new grid JFX not created and saved (%r)" % g)
        lens = (await page.inner_text("#sessionSelect")).split()
        if "20" not in lens or "40" not in lens or "Clear" not in lens:
            out.append("UI: session buttons are %r" % lens)
        await page.evaluate("""() => { window.__submits = []; window.__events = [];
          window.mfg = function (name, params) { window.__events.push([name, params]); };
          window.MaffsLeaderboard.submitScore = function (slug, level, score, n) {
            window.__submits.push([slug, level, score, n]); return Promise.resolve({}); }; }""")
        await page.click(".session-btn[data-count='20']")
        await page.click("#startBtn")
        await wait_asking_or_done(page, 0)

        trace, seen, prev = [], set(), 0
        while await ui_state(page) == "asking":
            q = await page.evaluate("SSB.ui.question()")
            sess = await page.evaluate("SSB.ui.session()")
            i = sess["served"]
            if q["key"] in set(sess["gold"]):
                out.append("UI: q%d served %s, which is gold" % (i, q["key"]))
            right = q["key"] in seen
            seen.add(q["key"])
            await page.keyboard.type(str(q["answer"] if right else q["answer"] + 1))
            await page.keyboard.press("Enter")
            trace.append((i, q["key"], right))
            if right:
                cells = await dom_cells(page)
                a, b = parse_key(q["key"])
                for rc in ((a, b), (b, a)):
                    if cells.get("%d,%d" % rc) != str(a * b):
                        out.append("UI: after %s right, cell %r shows %r" % (q["key"], rc, cells.get("%d,%d" % rc)))
                gold = set((await page.evaluate("SSB.ui.session()"))["gold"])
                for pos, txt in cells.items():
                    r, c = map(int, pos.split(","))
                    if txt and key_of(r, c) not in gold:
                        out.append("UI: unearned cell (%d,%d) shows %r" % (r, c, txt))
                    if txt and txt != str(r * c):
                        out.append("UI: cell (%d,%d) shows %r" % (r, c, txt))
            else:
                await page.wait_for_selector("#feedback .maffs-next", timeout=5000)
                slot = await page.evaluate("""() => { const s = document.querySelector('#qline .slot');
                  const d = s && s.querySelector('del'); return s ? { text: s.firstChild.textContent,
                  del: d ? d.textContent : null, cls: s.className } : null; }""")
                if not slot or slot["text"] != str(q["answer"]) or slot["del"] != str(q["answer"] + 1):
                    out.append("UI: after a wrong answer to %s the slot reads %r; it must show the correct %d "
                               "with the student's %d struck through" % (q["parts"], slot, q["answer"], q["answer"] + 1))
                for sel in ("#gameHeader h1", "#a11yToggle"):
                    if not await page.is_visible(sel):
                        out.append("UI: %s is not visible during play" % sel)
                dots = await page.evaluate("document.querySelectorAll('#feedback .dot').length")
                if dots != q["x"] * q["y"]:
                    out.append("UI: array for %d x %d has %d dots" % (q["x"], q["y"], dots))
                hint = await page.evaluate("(q) => SSB.hint(q.x, q.y).text", q)
                if hint not in await page.inner_text("#feedback"):
                    out.append("UI: wrong-answer screen does not show the hint for %s" % q["key"])
                if str(q["x"] * q["y"]) not in await page.inner_text("#feedback .fb-fact"):
                    out.append("UI: wrong-answer screen does not show the fact")
                await page.click("#feedback .maffs-next")
            await wait_asking_or_done(page, i)
            prev = i
        if len(trace) != 20:
            out.append("UI: a 20-question session served %d" % len(trace))
        missed = [t for t in trace if not t[2]]
        back = [t for t in missed if any(u[1] == t[1] and u[0] > t[0] for u in trace)]
        if missed and not back:
            out.append("UI: no missed fact ever came back")
        for i, k, _ in missed:
            later = [u[0] for u in trace if u[1] == k and u[0] > i]
            if later and not 3 <= later[0] - i <= 5:
                out.append("UI: %s missed at q%d came back at q%d" % (k, i, later[0]))
            if not later and len(trace) >= i + 5:
                out.append("UI: %s missed at q%d never came back" % (k, i))
        await page.wait_for_selector("#results.active", timeout=5000)
        check_events(await page.evaluate("window.__events"), "q20", len(trace),
                     sum(1 for t in trace if t[2]), out, "UI 20-question session")
        subs = await page.evaluate("window.__submits")
        if [(x[0], x[1]) for x in subs] != [("six-sevens-bruv", "q20")]:
            out.append("UI: a 20-question session submitted %r, expected one score to six-sevens-bruv/q20" % subs)
        for sel in ("#gameHeader h1", "#a11yToggle"):
            if not await page.is_visible(sel):
                out.append("UI: %s is not visible on the results screen" % sel)

        # Persisted, then resumed after a reload, then deleted.
        saved = set((await page.evaluate("SSB.ui.grid()"))["gold"])
        await page.reload()
        await page.wait_for_function("!!window.SSB && !!window.SSB.ui", timeout=8000)
        listing = await page.inner_text("#gridList")
        if "JFX — %d gold" % len(saved) not in listing:
            out.append("UI: after reload the list reads %r, expected JFX — %d gold" % (listing, len(saved)))
        resumed = await page.evaluate("SSB.ui.grid()")
        if not resumed or set(resumed["gold"]) != saved:
            out.append("UI: resumed grid differs from the saved one")
        await page.click(".grid-del")
        await page.click(".confirm-row .btn:not(.quiet)")
        if await page.evaluate("localStorage.getItem('mfg_progress_v1::six-sevens-bruv::JFX')") is not None:
            out.append("UI: deleted grid is still in storage")
        if "JFX" in await page.inner_text("#gridList"):
            out.append("UI: deleted grid is still listed")
        for e in errors:
            out.append("UI page error: " + e)
        return len(trace), len(missed), len(back)
    finally:
        await ctx.close()


async def ui_clear_the_grid(browser, out):
    """A grid with 3 facts left offers only 'clear the grid'; finishing it must submit nothing."""
    ctx, page, errors = await new_page(browser)
    try:
        keys = sorted(key_of(a, b) for a, b in ALL_FACTS)
        left = ["7x8", "6x7", "8x9"]
        gold = [k for k in keys if k not in left]
        await page.evaluate("""(g) => localStorage.setItem('mfg_progress_v1::six-sevens-bruv::TST',
          JSON.stringify({ v: 1, updated: Date.now(), summary: { gold: g.length }, data: { gold: g } }))""", gold)
        await page.reload()
        await page.wait_for_function("!!window.SSB && !!window.SSB.ui", timeout=8000)
        await page.evaluate("""() => { window.__submits = []; window.__events = [];
          window.mfg = function (name, params) { window.__events.push([name, params]); };
          window.MaffsLeaderboard.submitScore = function (slug, level) {
            window.__submits.push([slug, level]); return Promise.resolve({}); }; }""")
        lens = await page.inner_text("#sessionSelect")
        if "Clear the grid (3)" not in lens or "20" in lens.split():
            out.append("clear-the-grid: with 3 facts left the buttons read %r" % lens)
        await page.click("#startBtn")
        await wait_asking_or_done(page, 0)
        while await ui_state(page) == "asking":
            q = await page.evaluate("SSB.ui.question()")
            i = (await page.evaluate("SSB.ui.session()"))["served"]
            await page.keyboard.type(str(q["answer"]))
            await page.keyboard.press("Enter")
            await wait_asking_or_done(page, i)
        await page.wait_for_selector("#results.active", timeout=5000)
        evs = await page.evaluate("window.__events")
        nq = sum(1 for e in evs if e[0] == "question_answered")
        check_events(evs, "clear", nq, nq, out, "clear-the-grid session")
        if not any(e[0] == "personal_best_set" for e in evs):
            out.append("clear-the-grid: first session on this device set no personal best")
        pb = await page.evaluate("localStorage.getItem('ssb_best_clear')")
        if pb is None:
            out.append("clear-the-grid: personal best not kept under ssb_best_clear")
        subs = await page.evaluate("window.__submits")
        if subs:
            out.append("clear-the-grid: submitted %r; it must not submit to any board" % subs)
        hist = await page.evaluate("localStorage.getItem('mfg_hist_v1::six-sevens-bruv::clear')")
        if not hist:
            out.append("clear-the-grid: no score-history record under level 'clear'")
        for e in errors:
            out.append("clear-the-grid page error: " + e)
    finally:
        await ctx.close()


async def ui_storage_blocked(browser, out):
    ctx, page, errors = await new_page(browser, block_storage=True)
    try:
        if await page.evaluate("SSB.ui.canSave()"):
            out.append("storage-blocked: the game believes it can save")
        note = await page.inner_text("#storageNote")
        if "not keeping data" not in note or "Nothing is saved" not in note:
            out.append("storage-blocked: the menu does not say the grid will not be kept (%r)" % note)
        if await page.query_selector("#newGridBtn"):
            out.append("storage-blocked: a New grid (saved) control is offered")
        await page.click("#startBtn")
        await wait_asking_or_done(page, 0)
        for _ in range(3):
            q = await page.evaluate("SSB.ui.question()")
            i = (await page.evaluate("SSB.ui.session()"))["served"]
            await page.keyboard.type(str(q["answer"]))
            await page.keyboard.press("Enter")
            await wait_asking_or_done(page, i)
        g = await page.evaluate("SSB.ui.grid()")
        if len(g["gold"]) != 15:
            out.append("storage-blocked: 3 right answers left %d gold, expected 15" % len(g["gold"]))
        for e in errors:
            out.append("storage-blocked page error: " + e)
    finally:
        await ctx.close()


# ---------------------------------------------------------------- self-test

FAULTS = [
    ("wrong product (7 x 8 stored as 57)",
     "SSB.fact('7x8').product = 57;"),
    ("wrong x9 hint (takes away 1, not one lot)",
     "SSB.HINT_RULES[9] = function (x) { return { rule: 'x9', steps: ["
     "{op:'mul',args:[x,10],value:10*x},{op:'sub',args:[10*x,1],value:10*x-1}],"
     "text: x + ' × 9 is ' + (10*x) + ' take away 1: ' + (10*x-1) + '.' }; };"),
    ("hint from the right-hand factor, not the easier one",
     "(function(){ var o = SSB.hintFactor; SSB.hintFactor = function (x, y) { return y; }; })();"),
    ("gold fact re-queued after a right answer",
     "(function(){ var o = SSB.sessionAnswer; SSB.sessionAnswer = function (s, ok) {"
     " var k = s.current; o(s, ok); if (ok) s.queue.push(k); }; })();"),
    ("missed fact never returns",
     "(function(){ var o = SSB.sessionAnswer; SSB.sessionAnswer = function (s, ok) {"
     " o(s, ok); if (!ok) s.returns.pop(); }; })();"),
]


async def selftest(browser):
    lines, ok = [], True
    for name, patch in FAULTS:
        ctx, page, _ = await new_page(browser)
        try:
            await page.evaluate(patch)
            found, _, _ = await collect_and_check(page, seeds=2)
        finally:
            await ctx.close()
        caught = bool(found)
        ok = ok and caught
        lines.append("  %-48s %s" % (name, ("CAUGHT (%d failures, e.g. %s)" % (len(found), found[0][:90]))
                                         if caught else "*** MISSED ***"))
    return ok, lines


async def run_all(args):
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        ctx, page, errors = await new_page(browser)
        found, data, nscen = await collect_and_check(page, seeds=args.seeds)
        await ctx.close()
        for f in found:
            fail(f)
        for e in errors:
            fail("page error: " + e)
        print("Facts: %d   questions (every fact, orientation, form): %d   sampled: %d   hints: %d"
              % (len(data["facts"]), len(data["questions"]), len(data["sampled"]), len(data["hints"])))
        print("Simulated sessions: %d" % nscen)

        ui_out = []
        played = await ui_playthrough(browser, ui_out)
        await ui_clear_the_grid(browser, ui_out)
        await ui_storage_blocked(browser, ui_out)
        for f in ui_out:
            fail(f)
        print("UI play-through (Firebase SDK blocked): %d questions, %d missed, %d came back; "
              "one score to q20; grid saved, resumed and deleted; clear-the-grid submitted nothing; "
              "storage-blocked mode run" % played)

        if not args.no_selftest:
            ok, lines = await selftest(browser)
            print()
            print("Fault-injection self-test (patched into a fresh page; the file is never touched):")
            for ln in lines:
                print(ln)
            if not ok:
                fail("fault-injection self-test: at least one fault was not caught")
        await browser.close()


def main():
    import asyncio
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-selftest", action="store_true", help="skip the fault-injection self-test")
    ap.add_argument("--seeds", type=int, default=24, help="seeds per session scenario (default 24)")
    args = ap.parse_args()
    global PORT
    try:
        server, base = bc.start_stub_server()
    except bc.StubServerError as exc:
        fail("stub server did not start: %s" % exc)
    else:
        PORT = urlsplit(base).port
        try:
            asyncio.run(run_all(args))
        finally:
            server.terminate()
    print()
    if _FAILURES:
        print("%d FAILURE(S)" % len(_FAILURES))
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
