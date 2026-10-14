#!/usr/bin/env python3
# ci-line: Quadratic Factoriser (every pooled item recomputed, SymPy; every Higher item's six guided steps played in Chromium, each split, factor and line recomputed; Formula roots on the keypad with a minus key) |
# ci-line: Quadratic Factoriser self-test (the old split and eight other faults planted in the guided steps and the keypad; each must fail) | --selftest
"""Layers C + D verification for quadratic-factoriser (docs/quadratic-factoriser-spec.md,
item 5). Grows with each build phase; this version covers Phase 1 ('gcse'), Phase 2
('higher') and Phase 3 ('formula').

WHY THIS READS THE LIVE PAGE, NOT A HAND-COPY OF THE POOL PARAMETERS
---------------------------------------------------------------------
The spec requires the pool to be "exported from the game as a JSON-able config, not
duplicated by hand" -- a Python re-implementation of the enumeration could drift from
the real one and would then be verifying itself, not the game. The game exposes its
pools on window.QF_POOLS after load (see games/quadratic-factoriser/index.html); this
script launches the stub server (CLAUDE.md's "ALWAYS use the stub server" rule),
loads the page under Playwright, reads window.QF_POOLS back, and checks THAT data
with SymPy.

WHAT "PER STAGE" MEANS HERE
----------------------------
docs/quadratic-factoriser-spec.md section 2.2 records the corrected floor: >= 40 items
per LEVEL (checked against the level's whole combined pool), not per stage. The
per-stage property that actually matters -- that a single session can never repeat a
question -- is asserted as what it reduces to under this game's sampling design
(one combined, deduplicated pool per level, shuffled and sliced without replacement,
exactly like `better-value`): the level's pool must contain no duplicate (a,b,c)
question. That single assertion is a stronger, always-sufficient guarantee than any
per-stage size floor, and it is what makes the 12-item DOTS stage safe without any
special-casing.

THE GUIDED STEPS (SWEEP-1, Jon's ruling 13 Oct 2026)
----------------------------------------------------
Every Higher item, and the tutorial example, is played through its six guided steps in
Chromium (Guided mode and "Show me the method" render the same steps): every option on
every step is tried, and what the page accepts is recomputed here. Each step has exactly one
accepted option and no other option is also right (SR-24); the step 3 split multiplies to
ac and adds to b; the step 4 line equals the quadratic on screen, its middle terms the
accepted split; step 5's first pair equals the factor times the bracket, and the accepted
second-pair factor times the bracket equals the second pair; step 6's accepted
factorisation equals the quadratic; the figures in the tutorial's narration and in each
misconception message are recomputed. The Formula level's root boxes are on the shared
phone keypad (MaffsKeypad) with a minus key: roots can be negative and a phone's decimal
pad (iOS) has none.

USAGE
-----
    python scripts/verify-quadratic-factoriser.py
    python scripts/verify-quadratic-factoriser.py --selftest   # planted faults must fail
"""
import asyncio
import math
import os
import re
import sys

import sympy as sp
from urllib.parse import urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import bank_common as bc  # noqa: E402  (start_stub_server: checked start, free port)
SLUG = "quadratic-factoriser"
PORT = None  # set by main() to the free port the stub server got

_FAILURES = []


def fail(msg):
    _FAILURES.append(msg)
    print("FAIL: " + msg)


PAGE = os.path.join(ROOT, "games", SLUG, "index.html")

# Plays one Higher item's six guided steps: renders each step as the page does (hfRenderStep), then tries
# every option the step offers (its own onclick), noting whether the page accepts it ("Correct!") and any
# misconception message it shows. Every LaTeX string is read back from KaTeX's annotation, as rendered.
GUIDED_JS = r"""(indices) => {
  const items = [higherTutorialExample].concat(window.QF_POOLS.higher.pool);
  const ann = el => el ? [...el.querySelectorAll('annotation')].map(a => a.textContent) : [];
  const out = [];
  for (const i of indices) {
    for (const mode of (i === 0 ? ['tutorial', 'guided'] : ['guided'])) {
      const item = items[i];
      currentQ = item; hfMode = mode; hfViaShowMethod = false;
      const rec = { i, mode, a: item.a, b: item.b, c: item.c, steps: [] };
      for (let st = 1; st <= 6; st++) {
        hfStep = st; hfRenderStep();
        const panel = hfPanel(), body = document.getElementById('hfStepBody');
        const step = { quad: ann(panel.querySelector('.hf-quadratic')),
          prompts: [...body.querySelectorAll('.hf-note, .hf-step-prompt')].map(ann), opts: [] };
        const calls = [...body.querySelectorAll('.hf-choice-btn:not(.hf-continue-btn)')]
          .map(b => ({ call: b.getAttribute('onclick'), tex: ann(b) }));
        for (const o of calls) {
          MaffsLock.fresh(panel);
          const fb = document.getElementById('hfFeedback');
          fb.textContent = ''; fb.className = 'hf-feedback';
          body.querySelectorAll('.hf-misconception').forEach(m => m.remove());
          (0, eval)(o.call);
          const mis = body.querySelector('.hf-misconception');
          step.opts.push({ call: o.call, tex: o.tex, accepted: fb.textContent === 'Correct!',
            mis: mis ? { name: mis.dataset.misconception, tex: ann(mis), text: mis.textContent } : null });
        }
        rec.steps.push(step);
      }
      out.push(rec);
    }
  }
  MaffsLock.clearTimers();
  return out;
}"""

# The Formula level on a phone: its root boxes are on MaffsKeypad, with a minus key that types.
KEYPAD_JS = r"""async () => {
  currentLevel = 'formula'; startGame();
  await new Promise(r => setTimeout(r, MaffsLock.FRESH_MS + 100));   // past the new question's fresh window
  const r1 = document.getElementById('fRoot1'), r2 = document.getElementById('fRoot2');
  const keys = [...document.querySelectorAll('#fKeypad .maffs-keypad-key')].filter(k => k.offsetParent !== null);
  const minus = keys.filter(k => k.dataset.act === 'minus')[0];
  const press = act_val => { const k = keys.filter(k => k.dataset.act + ':' + k.dataset.val === act_val)[0]; if (k) k.click(); };
  if (minus) { press('minus:-'); press('in:1'); press('in:.'); press('in:5'); }
  return { keys: keys.length, minus: !!minus, typed: r1 ? r1.value : null,
           inputmode: [r1, r2].map(t => t && t.getAttribute('inputmode')), readOnly: [r1, r2].map(t => t && t.readOnly) };
}"""


PAGES = 4   # the guided steps are played on this many pages at once (each its own renderer process)


async def fetch_pools(html=None, every=1):
    """Reads window.QF_POOLS, plays the Higher items' guided steps (every one, or every `every`-th with the tutorial
    example: the self-test's sample), and checks the Formula keypad on a phone. html, when given, is served in
    place of the page (the self-test's planted copies)."""
    from playwright.async_api import async_playwright

    base = "http://127.0.0.1:%d" % PORT
    url = base + "/games/" + SLUG + "/?cb=verify"
    page_re = re.compile(r"/games/" + SLUG + r"/(\?[^/]*)?$")

    async def open_page(ctx):
        await ctx.route(lambda u: bc.is_font_cdn(u), bc.serve_real_font_async)   # KaTeX from the pinned local copy
        if html is not None:
            await ctx.route(lambda u: bool(page_re.search(u)), lambda route: route.fulfill(
                status=200, content_type="text/html; charset=utf-8", body=html))
        page = await ctx.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        await page.goto(url, wait_until="load", timeout=30000)
        await page.wait_for_timeout(300)
        return page, errors

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page, errors = await open_page(await browser.new_context())
        pools = await page.evaluate("() => window.QF_POOLS || null")
        guided = []
        if pools and "higher" in pools:
            todo = list(range(0, len(pools["higher"]["pool"]) + 1, every))

            async def play(share):
                pg, errs = await open_page(await browser.new_context())
                got = []
                for start in range(0, len(share), 300):
                    got += await pg.evaluate(GUIDED_JS, share[start:start + 300])
                errors.extend(errs)
                return got

            for got in await asyncio.gather(*[play(todo[k::PAGES]) for k in range(PAGES)]):
                guided += got
            guided.sort(key=lambda r: (r["i"], r["mode"]))
        phone = await open_page(await browser.new_context(
            viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True))
        keypad = await phone[0].evaluate(KEYPAD_JS)
        await browser.close()
        return pools, guided, keypad, errors + phone[1]


def poly(latex):
    """A LaTeX polynomial or product as the page writes it ('6x^2 + 4x + -3x - 2', '2x(3x + 4)',
    '2(2x - 1)(3x + 4)', '-6') -> its exact coefficients {power: int}, zeros dropped. A small parser of its
    own, not SymPy's: it reads about 60,000 expressions a run, and these are integer polynomials in x."""
    toks = re.findall(r"\d+|[x()+\-^]|\S", re.sub(r"\\(left|right|,|;|!)|\\ |[{}]", " ", latex))
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def take():
        pos[0] += 1
        return toks[pos[0] - 1]

    def mul(p1, p2):
        out = {}
        for i, u in p1.items():
            for j, v in p2.items():
                out[i + j] = out.get(i + j, 0) + u * v
        return out

    def add(p1, p2, sign=1):
        out = dict(p1)
        for i, v in p2.items():
            out[i] = out.get(i, 0) + sign * v
        return out

    def atom():
        t = take()
        if t == "(":
            e = expr()
            if take() != ")":
                raise ValueError("unbalanced bracket in %r" % latex)
            base = e
        elif t == "x":
            base = {1: 1}
        elif t is not None and t.isdigit():
            base = {0: int(t)}
        else:
            raise ValueError("cannot read %r in %r" % (t, latex))
        if peek() == "^":
            take()
            n = take()
            if not n.isdigit():
                raise ValueError("cannot read the power in %r" % latex)
            out = {0: 1}
            for _ in range(int(n)):
                out = mul(out, base)
            base = out
        return base

    def term():
        sign = 1
        while peek() in ("+", "-"):
            sign = -sign if take() == "-" else sign
        out = {0: sign}
        while peek() not in (None, "+", "-", ")"):
            out = mul(out, atom())   # juxtaposition is multiplication: 2x(3x + 4)
        return out

    def expr():
        out = term()
        while peek() in ("+", "-"):
            sign = -1 if take() == "-" else 1
            out = add(out, term(), sign)
        return out

    e = expr()
    if peek() is not None:
        raise ValueError("cannot read %r" % latex)
    return {i: v for i, v in e.items() if v}


def pmul(p1, p2):
    out = {}
    for i, u in p1.items():
        for j, v in p2.items():
            out[i + j] = out.get(i + j, 0) + u * v
    return {i: v for i, v in out.items() if v}


def args_of(call):
    """hfStep3Pick(6,-4) -> [6, -4]; hfStep6Pick('2(x + 1)(3x - 4)') -> ['2(x + 1)(3x - 4)']."""
    inner = call[call.index("(") + 1:call.rindex(")")]
    if inner.startswith("'"):
        return [inner[1:-1].replace("\\'", "'")]
    return [int(v) for v in inner.split(",")]


def verify_guided(guided, n_pool, every=1):
    """Jon, 13 Oct 2026: every guided step's key, split, factor and line recomputed (canon: verifiers
    recompute explanation and hint figures)."""
    want = len(range(0, n_pool + 1, every)) + 1   # the items in Guided mode, and the tutorial example narrated too
    if len(guided) != want:
        fail("guided steps: played %d item-modes, expected %d" % (len(guided), want))
    bad = []

    def note(rec, msg):
        if len(bad) < 40:
            bad.append("guided steps, %s, item %d (%dx^2 %+dx %+d): %s"
                       % (rec["mode"], rec["i"], rec["a"], rec["b"], rec["c"], msg))
        else:
            bad.append(None)

    for rec in guided:
        a, b, c = rec["a"], rec["b"], rec["c"]
        Q = {i: v for i, v in {2: a, 1: b, 0: c}.items() if v}
        steps = rec["steps"]
        if len(steps) != 6:
            note(rec, "%d steps rendered, not 6" % len(steps)); continue
        try:
            for st in steps:
                if len(st["quad"]) != 1 or poly(st["quad"][0]) != Q:
                    raise ValueError("the quadratic on screen %r is not %dx^2 %+dx %+d" % (st["quad"], a, b, c))
        except ValueError as e:
            note(rec, str(e)); continue

        def one_accepted(k, right):
            opts = steps[k - 1]["opts"]
            acc = [o for o in opts if o["accepted"]]
            if len(acc) != 1:
                note(rec, "step %d accepts %d of its %d options" % (k, len(acc), len(opts)))
                return None
            for o in opts:
                if right(o) != o["accepted"]:
                    note(rec, "step %d: %s is %s but the page %s it" % (
                        k, o["call"], "right" if right(o) else "wrong",
                        "accepts" if o["accepted"] else "refuses"))
            return acc[0]

        # Step 1: a, b and c.
        one_accepted(1, lambda o: args_of(o["call"]) == [a, b, c])
        # Step 2: a x c.
        one_accepted(2, lambda o: args_of(o["call"]) == [a * c])
        # Step 3: the pair that multiplies to ac and adds to b; each option's own sums shown right.
        for o in steps[2]["opts"]:
            m, n = args_of(o["call"])
            t = " ".join(o["tex"])
            nums = [int(v) for v in re.findall(r"-?\d+", t)]
            if nums != [m, n, m * n, m, n, m + n]:
                note(rec, "step 3 option %r does not show m x n and m + n correctly" % t)
            if re.search(r"(?:\\times|\+) -", t):   # s1-004 (R1): a negative second number is bracketed
                note(rec, "step 3 option %r writes a negative number straight after a sign" % t)
            if o["mis"]:
                mt = re.findall(r"-?\d+", " ".join(o["mis"]["tex"]))
                if m * n != c or [int(v) for v in mt[:1]] != [c] or str(a * c) not in mt:
                    note(rec, "step 3's misconception for %r states %r" % (o["call"], o["mis"]["text"]))
        acc3 = one_accepted(3, lambda o: (lambda m, n: m * n == a * c and m + n == b)(*args_of(o["call"])))
        if rec["mode"] == "tutorial":
            lead = " ".join(steps[2]["prompts"][0])
            if "ac = %d" % (a * c) not in lead or "b = %d" % b not in lead:
                note(rec, "the tutorial's step 3 states %r, not ac = %d and b = %d" % (lead, a * c, b))
        # Step 4: the split line equals the quadratic, and its middle terms are the accepted split.
        line = [t for p in steps[3]["prompts"] for t in p if "x^2" in t]
        mid = re.match(r"^\d*x\^2 ([+-]) (\d*)x ([+-]) (\d*)x ", line[0]) if len(line) == 1 else None
        if not mid:
            note(rec, "step 4's line %r is not read" % line); continue
        # s1-004, s1-007 (R1): a difference is written as one ("- 16x", never "+ -16x") and a coefficient of 1 is left out
        if re.search(r"\+ -|(?<![\d])1x", line[0]):
            note(rec, "step 4's line %r writes a negative term after a plus or a coefficient of 1" % line[0])
        m1 = (-1 if mid.group(1) == "-" else 1) * (int(mid.group(2)) if mid.group(2) else 1)
        n1 = (-1 if mid.group(3) == "-" else 1) * (int(mid.group(4)) if mid.group(4) else 1)
        if poly(line[0]) != Q:
            note(rec, "step 4's line %s does not equal the quadratic" % line[0])
        if acc3 and sorted([m1, n1]) != sorted(args_of(acc3["call"])):
            note(rec, "step 4 splits into %dx and %dx, not the accepted pair %s" % (m1, n1, acc3["call"]))
        # Step 5: the first pair is the factor times the bracket; the accepted factor x bracket is the second pair.
        fp = [t for p in steps[4]["prompts"] for t in p if re.match(r"^-?\d*x\(.*\)$", t)]
        if len(fp) != 1:
            note(rec, "step 5's first-pair factorisation is not read (%r)" % steps[4]["prompts"]); continue
        fm = re.match(r"^(-?\d*x)\((.*)\)$", fp[0])
        F, B = poly(fm.group(1)), poly(fm.group(2))
        if pmul(F, B) != {i: v for i, v in {2: a, 1: m1}.items() if v}:
            note(rec, "step 5: the first pair %dx^2 %+dx is not %s" % (a, m1, fp[0]))
        second = {i: v for i, v in {1: n1, 0: c}.items() if v}
        one_accepted(5, lambda o: pmul({0: args_of(o["call"])[0]}, B) == second)
        for o in steps[4]["opts"]:
            if o["mis"]:
                mt = o["mis"]["tex"]
                if len(mt) < 2 or pmul(poly(mt[0]), poly(mt[1])) != second:
                    note(rec, "step 5's misconception for %s states %r" % (o["call"], o["mis"]["text"]))
        # Step 6: the accepted factorisation equals the quadratic, and no other option does.
        one_accepted(6, lambda o: poly(args_of(o["call"])[0]) == Q)
    shown = [m for m in bad if m]
    for m in shown:
        fail(m)
    if len(bad) > len(shown):
        fail("guided steps: %d more" % (len(bad) - len(shown)))
    if not bad:
        print("  guided steps: %d item-modes, every step's key, split, line and factor recomputed" % len(guided))


def verify_keypad(keypad):
    """The Formula level's roots can be negative: on a phone they are typed on MaffsKeypad with its minus key."""
    if not keypad["minus"] or keypad["typed"] != "-1.5":
        fail("formula: on a phone the root boxes are not on the keypad with a minus key that types "
             "(keys %d, minus %s, typed %r, inputmode %r)" % (keypad["keys"], keypad["minus"], keypad["typed"],
                                                              keypad["inputmode"]))
    elif keypad["inputmode"] != ["none", "none"] or keypad["readOnly"] != [True, True]:
        fail("formula: on a phone the root boxes would open the system keyboard (inputmode %r, readOnly %r)"
             % (keypad["inputmode"], keypad["readOnly"]))
    else:
        print("  formula keypad: %d keys on a phone, minus types; boxes read-only, inputmode none" % keypad["keys"])


def verify_gcse(level):
    x = sp.symbols("x")
    pool = level["pool"]
    stages = level["stages"]
    stage_order = level["stageOrder"]

    # C: every factorised form expands to its own quadratic.
    for item in pool:
        p, q, b, c = item["p"], item["q"], item["b"], item["c"]
        lhs = sp.expand((x + p) * (x + q))
        rhs = x**2 + b * x + c
        if sp.simplify(lhs - rhs) != 0:
            fail("gcse item p=%r q=%r does not expand to x^2+%rx+%r (got %s)"
                 % (p, q, b, c, lhs))

    # D: no duplicate (b,c) in the level's combined pool -- see module docstring for
    # why this is the real "no session ever repeats a question" guarantee under this
    # game's shuffle-the-whole-pool-then-slice sampling, and why it supersedes any
    # per-stage size floor.
    seen = {}
    for item in pool:
        key = (item["b"], item["c"])
        if key in seen:
            fail("gcse pool has duplicate (b,c)=%r (stages %r and %r)"
                 % (key, seen[key], item["stage"]))
        else:
            seen[key] = item["stage"]

    # Per-level floor (spec 2.2): the level's total pool, not any one stage.
    if len(pool) < 40:
        fail("gcse level pool has %d items, needs >= 40" % len(pool))

    # Stage sizes, reported for visibility, and the one pinned invariant: DOTS is an
    # exhaustive enumeration (k=1..12) and must stay exactly 12 -- not a floor, a check
    # that nothing accidentally changed its population.
    sizes = {name: len(stages.get(name, [])) for name in stage_order}
    print("  gcse stage sizes: %s (total %d)" % (sizes, len(pool)))
    if sizes.get("dots") != 12:
        fail("gcse dots stage has %d items, expected exactly 12 (k=1..12, its full "
             "exhaustive population)" % sizes.get("dots", -1))
    for name in ("bothPos", "oneNeg", "bothNeg"):
        if sizes.get(name, 0) == 0:
            fail("gcse stage %r is empty" % name)

    # Every stage's own (b,c) values must themselves already be unique -- if a stage
    # produced an internal duplicate the cross-stage check above wouldn't necessarily
    # catch it if two DIFFERENT items happened to collide only within one stage.
    for name in stage_order:
        stage_seen = set()
        for item in stages.get(name, []):
            key = (item["b"], item["c"])
            if key in stage_seen:
                fail("gcse stage %r has an internal duplicate (b,c)=%r" % (name, key))
            stage_seen.add(key)


def ac_splits(a, b, c):
    """Every unordered {m,n} with m*n = a*c and m+n = b -- re-derived independently in
    Python (not read from the game's own acSplits()), because this is exactly the
    property item 5 requires the verifier to prove from scratch."""
    ac = a * c
    out = set()
    bound = max(1, abs(ac))
    for m in range(-bound, bound + 1):
        if m == 0 or ac % m != 0:
            continue
        n = ac // m
        if m + n == b:
            out.add((m, n) if m <= n else (n, m))
    return out


def verify_higher(level):
    x = sp.symbols("x")
    pool = level["pool"]
    stages = level["stages"]
    stage_order = level["stageOrder"]

    for item in pool:
        p, q, r, s = item["p"], item["q"], item["r"], item["s"]
        a, b, c = item["a"], item["b"], item["c"]
        k = item.get("k") or 1

        # C: every factorised form expands to its own quadratic.
        lhs = sp.expand(k * (p * x + q) * (r * x + s))
        rhs = a * x**2 + b * x + c
        if sp.simplify(lhs - rhs) != 0:
            fail("higher item %r does not expand to %r (got %s)" % (item, rhs, lhs))

        # D: exactly one unordered {m,n} split with mn=ac, m+n=b -- the AC-method step 3
        # the tutorial teaches must have exactly one right answer.
        splits = ac_splits(a, b, c)
        if len(splits) != 1:
            fail("higher item %r has %d AC-splits (mn=ac, m+n=b), expected exactly 1: %r"
                 % (item, len(splits), splits))

        # D: no non-HCF (base) item has a common factor across a,b,c -- item 5's explicit
        # requirement, and the reason gcd(p,q)=gcd(r,s)=1 is imposed at generation time.
        if item["stage"] == "base":
            g = math.gcd(math.gcd(abs(a), abs(b)), abs(c))
            if g != 1:
                fail("higher base item %r has a common factor %d across a,b,c" % (item, g))

    # No duplicate (a,b,c) anywhere in the level's combined pool -- same "no session ever
    # repeats a question" guarantee as gcse (spec 2.2), checked across BOTH stages: a base
    # item and an HCF item could in principle expand to the same trinomial via a different
    # (p,q,r,s,k) (e.g. base p=2,r=6 and HCF k=2,p=1,r=6 both give a=12) even though no
    # such collision actually occurs in this parameter range (confirmed separately) --
    # this assertion is what would catch it if the parameters ever changed.
    seen = {}
    for item in pool:
        key = (item["a"], item["b"], item["c"])
        if key in seen:
            fail("higher pool has duplicate (a,b,c)=%r (stages %r and %r)"
                 % (key, seen[key], item["stage"]))
        else:
            seen[key] = item["stage"]

    if len(pool) < 40:
        fail("higher level pool has %d items, needs >= 40" % len(pool))

    sizes = {name: len(stages.get(name, [])) for name in stage_order}
    print("  higher stage sizes: %s (total %d)" % (sizes, len(pool)))
    for name in stage_order:
        if sizes.get(name, 0) == 0:
            fail("higher stage %r is empty" % name)


def _is_near_rounding_boundary(root):
    k = math.floor(root * 100 - 0.5 + 0.5)  # round-half-up, matching the game's Math.round
    boundary = (k + 0.5) / 100
    return abs(root - boundary) < 1e-6


def verify_formula(level):
    pool = level["pool"]
    stages = level["stages"]
    stage_order = level["stageOrder"]

    x = sp.symbols("x")
    for item in pool:
        a, b, c = item["a"], item["b"], item["c"]
        d = b * b - 4 * a * c
        true_roots = sp.solve(sp.Eq(a * x**2 + b * x + c, 0), x)
        true_roots = [complex(r) for r in true_roots]

        if d < 0:
            # D: negative-discriminant items are flagged as such.
            if not item["noReal"]:
                fail("formula item %r has d=%d (<0) but noReal is not true" % (item, d))
            if item["root1"] is not None or item["root2"] is not None:
                fail("formula item %r has d<0 but carries non-null roots" % item)
            if item["stage"] != "neg":
                fail("formula item %r has d<0 but stage=%r, expected 'neg'" % (item, item["stage"]))
            if any(abs(r.imag) < 1e-9 for r in true_roots):
                fail("formula item %r: SymPy found a real root for a claimed-negative discriminant" % item)
            continue

        if item["noReal"] or item["stage"] != "nonNeg":
            fail("formula item %r has d=%d (>=0) but noReal=%r stage=%r"
                 % (item, d, item["noReal"], item["stage"]))

        # C: every root matches SymPy's own root to 1e-9.
        game_roots = sorted([item["root1"], item["root2"]])
        sym_roots = sorted([r.real for r in true_roots])
        for gr, sr in zip(game_roots, sym_roots):
            if abs(gr - sr) > 1e-9:
                fail("formula item %r: game root %.12f vs SymPy root %.12f differ by more than 1e-9"
                     % (item, gr, sr))

        # D: no item sits on a rounding boundary.
        if _is_near_rounding_boundary(item["root1"]) or _is_near_rounding_boundary(item["root2"]):
            fail("formula item %r has a root within 1e-6 of a 2 d.p. rounding boundary" % item)

    # No duplicate (a,b,c) anywhere in the level's combined pool (spec 2.2's no-repeat
    # guarantee, same as gcse/higher).
    seen = set()
    for item in pool:
        key = (item["a"], item["b"], item["c"])
        if key in seen:
            fail("formula pool has duplicate (a,b,c)=%r" % (key,))
        seen.add(key)

    if len(pool) < 40:
        fail("formula level pool has %d items, needs >= 40" % len(pool))

    sizes = {name: len(stages.get(name, [])) for name in stage_order}
    neg_pct = 100.0 * sizes.get("neg", 0) / len(pool) if pool else 0
    print("  formula stage sizes: %s (total %d, %.1f%% negative discriminant)"
          % (sizes, len(pool), neg_pct))
    # Spec item 2: "~15% negative discriminant" -- a soft target, not an exact one; a wide
    # 10-20% band catches accidental drift (e.g. someone changing the curation thinning)
    # without being brittle to the exact count.
    if not (10.0 <= neg_pct <= 20.0):
        fail("formula pool's negative-discriminant share is %.1f%%, expected roughly 15%% "
             "(10-20%% band)" % neg_pct)
    for name in stage_order:
        if sizes.get(name, 0) == 0:
            fail("formula stage %r is empty" % name)

    # Spec item 2: "mostly non-square discriminants" among the real-root items.
    square_count = 0
    for item in stages.get("nonNeg", []):
        d = item["b"] * item["b"] - 4 * item["a"] * item["c"]
        if math.isqrt(d) ** 2 == d:
            square_count += 1
    nonneg_n = max(1, sizes.get("nonNeg", 0))
    square_pct = 100.0 * square_count / nonneg_n
    print("  formula perfect-square discriminant among real-root items: %d/%d (%.1f%%)"
          % (square_count, nonneg_n, square_pct))
    if square_pct > 50.0:
        fail("formula real-root items are %.1f%% perfect-square discriminant, expected a "
             "minority ('mostly non-square')" % square_pct)


def run(html=None, every=1, pools_too=True):
    """Every check, on the page as served (or on html in its place). Returns the failures. pools_too=False (the
    self-test's plants) leaves out the SymPy pool checks, which no plant touches."""
    global PORT
    del _FAILURES[:]
    # A free port chosen per run; raises bc.StubServerError, naming the cause, if the
    # stub server cannot start.
    server, base = bc.start_stub_server()
    PORT = urlsplit(base).port
    try:
        pools, guided, keypad, errors = asyncio.run(fetch_pools(html, every))
    finally:
        server.terminate()

    if not pools:
        fail("could not read window.QF_POOLS from the live page")
        return list(_FAILURES)
    for e in errors[:3]:
        fail("page error: " + e)

    if not pools_too:
        verify_guided(guided, len(pools["higher"]["pool"]), every)
        verify_keypad(keypad)
        return list(_FAILURES)

    if "gcse" in pools:
        print("Verifying 'gcse'...")
        verify_gcse(pools["gcse"])
    else:
        fail("window.QF_POOLS.gcse is missing")

    if "higher" in pools:
        print("Verifying 'higher'...")
        verify_higher(pools["higher"])
        verify_guided(guided, len(pools["higher"]["pool"]), every)
    else:
        fail("window.QF_POOLS.higher is missing")

    if "formula" in pools:
        print("Verifying 'formula'...")
        verify_formula(pools["formula"])
        verify_keypad(keypad)
    else:
        fail("window.QF_POOLS.formula is missing")
    return list(_FAILURES)


# Planted faults: each must fail (the self-test). The first is the old split, fixed 13 Oct 2026.
PLANTS = [
    ("the old split (base ps, qr on an HCF item)",
     "function hfCorrectSplit(item) { const k = hfK(item); return { m: k * item.p * item.s, n: k * item.q * item.r }; }",
     "function hfCorrectSplit(item) { return { m: item.p * item.s, n: item.q * item.r }; }"),
    ("step 5's first-pair factor without k",
     "const factor = `${k * p === 1 ? '' : k * p}x`;", "const factor = `${p === 1 ? '' : p}x`;"),
    ("step 5 accepting q, not kq",
     "if (v === hfK(currentQ) * q) { hfStepCorrectAdvance(6); return; }", "if (v === q) { hfStepCorrectAdvance(6); return; }"),
    ("step 5 offering q and -q",
     "const opts = MaffsOptions.shuffle([k * q, -k * q]);", "const opts = MaffsOptions.shuffle([q, -q]);"),
    ("step 3 accepting the pair that multiplies to c",
     "if (pairsEqual([m, n], [split.m, split.n])) { hfStepCorrectAdvance(4); return; }",
     "if (pairsEqual([m, n], [split.m, split.n]) || m * n === currentQ.c) { hfStepCorrectAdvance(4); return; }"),
    ("step 4's line with the wrong constant",
     "const line = `${a === 1 ? '' : a}x^2${hfLaterTerm(split.m, 'x')}${hfLaterTerm(split.n, 'x')}${hfLaterTerm(c, '')}`;",
     "const line = `${a === 1 ? '' : a}x^2${hfLaterTerm(split.m, 'x')}${hfLaterTerm(split.n, 'x')}${hfLaterTerm(c + 1, '')}`;"),
    ("s1-004: step 4 back to \"+ -16x\" and \"1x\"",
     "function hfLaterTerm(coef, v) { return ` ${coef < 0 ? '-' : '+'} ${v && Math.abs(coef) === 1 ? '' : Math.abs(coef)}${v}`; }",
     "function hfLaterTerm(coef, v) { return ` + ${coef}${v}`; }"),
    ("s1-004: step 3's negative number unbracketed",
     "${m} \\\\times ${n < 0 ? `(${n})` : n} = ${m * n},\\\\ \\\\ ${m} + ${n < 0 ? `(${n})` : n} = ${m + n}",
     "${m} \\\\times ${n} = ${m * n},\\\\ \\\\ ${m} + ${n} = ${m + n}"),
    ("step 5's misconception with the wrong bracket",
     "const wrongR = -r, wrongS = -s;", "const wrongR = -r, wrongS = s;"),
    ("the Formula roots without the keypad (the decimal pad: no minus on iOS)",
     "  if (window.MaffsKeypad) {\n    MaffsKeypad.mount(", "  if (false) {\n    MaffsKeypad.mount("),
    ("the keypad without its minus key",
     "keys: { minus: true }, keepInView", "keys: { minus: false }, keepInView"),
]


SAMPLE = 40   # the self-test plays every 40th Higher item (base and HCF items both); the full run plays them all


def selftest():
    src = open(PAGE, encoding="utf-8").read()
    bad = []
    clean = run(None, SAMPLE, pools_too=False)
    if clean:
        bad.append("the page as served fails (%d)" % len(clean))
    for name, old, new in PLANTS:
        if src.count(old) != 1:
            bad.append(name + " (the plant no longer matches the page)")
            continue
        print("\nselftest plant: " + name)
        if not run(src.replace(old, new), SAMPLE, pools_too=False):
            bad.append(name + " (passed)")
    print()
    print("selftest: %s" % ("FAILED: " + "; ".join(bad) if bad else "PASS (%d plants fail)" % len(PLANTS)))
    return 1 if bad else 0


def main():
    if "--selftest" in sys.argv[1:]:
        return selftest()
    fails = run(None)
    print()
    if fails:
        print("%d FAILURE(S)" % len(fails))
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
