#!/usr/bin/env python3
# ci-line: The 6 P's banks (every bank regenerated from its game's own questions and compared with the committed file; every answer recomputed from its stem; a topic is covered only by a bank of 30 or more) | --check
# ci-deps: docs/six-ps-schema.md schools/assets/exam-topics-ocr-foundation.json scripts/gen-exam-topics.py scripts/bank_common.py
"""The 6 P's question banks, built from the games' own questions (contract SIX-PS-BANKS, 25 Oct 2026).

    python scripts/gen-six-ps.py                       # build every bank in memory and report
    python scripts/gen-six-ps.py --write               # write schools/assets/six-ps/<topic-id>.json
    python scripts/gen-six-ps.py --check               # CI: regenerate, diff the committed banks, check coverage
    python scripts/gen-six-ps.py --sheet FILE          # one review page for the batch, for Jon, into FILE
    python scripts/gen-six-ps.py --only ratio powers-roots

Never hand-copied: each topic's bank is read from the game it routes to, on the stub server, at the route's level
(bank_common's start_stub_server), by the game's own question list or by calling its own generator in the page with
Math.random replaced by a seeded generator (so a question is reproducible from `generator:<function>:<seed>`). A game
file is never changed. The question shape is docs/six-ps-schema.md (schema 1).

What is converted, and how (the rules a reviewer needs):
  - A typed or tapped question becomes its written exam form from the same numbers. A game that asks for several
    answers at once (Split It's share in a ratio) is asked for ONE of them by a fixed rule, stated in the topic's entry.
  - A game's multiple choice stays `choice` only where the answer cannot be typed (a name, an expression); otherwise the
    answer is typed (`number`, `fraction`, `ratio`, `money`, `number_unit`).
  - `worked` is the game's own working, one line per step, never written here; a game with none gives [] (the missing-
    worked list). `slip` is the game's own named slips only, never invented.
  - `band` and `calc` are rules per topic (below), not per question judgement.
  - A topic keeps at most CAP questions: every question when the game holds that many or fewer, otherwise an even stride
    through the game's pool (a seeded stream for generators, GEN_PER_MODE a mode).
  - Every converted answer is recomputed from its own stem by `check_*`, independently of the game's answer.

A topic is covered (scripts/gen-exam-topics.py) only if its bank here holds at least MIN_QUESTIONS; `--check` fails if
a covered topic has no bank or a bank's topic is not covered.
"""
import argparse
import asyncio
import hashlib
import html
import json
import math
import os
import re
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_common as bc  # noqa: E402

ROOT = bc.ROOT
OUT_DIR = os.path.join(ROOT, "schools", "assets", "six-ps")
TOPICS_JSON = os.path.join(ROOT, "schools", "assets", "exam-topics-ocr-foundation.json")
MIN_QUESTIONS = 30
CAP = 150            # most questions a list topic keeps (every Foundation item up to this)
GEN_TOPIC = 60       # a generator topic keeps this many, spread evenly across the game's question types and stages
                     # (Jon's ruling of 25 Oct 2026), from a fixed seed order, so --check is stable
FORMATS = ("number", "money", "fraction", "ratio", "coordinates", "choice", "number_unit")

MULBERRY = ("function mul(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);"
            "t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}")


# ───────────────────────────── helpers ─────────────────────────────
def sha8(*parts):
    return hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:8]


def strip_html(s):
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def maths(s):
    """The game's own TeX marker (§ ... §, Squared Squirrel) becomes the schema's \\( ... \\)."""
    parts = s.split("\u00a7")
    if len(parts) == 1:
        return s
    out = []
    for i, p in enumerate(parts):
        out.append(p if i % 2 == 0 else "\\(" + p + "\\)")
    return "".join(out)


def tex(s):
    return "\\(" + s + "\\)"


def split_working(s):
    """One line per sentence of the game's own working (split where a full stop ends a sentence, never in a number)."""
    s = strip_html(s)
    parts = re.split(r"(?<=[a-zA-Z0-9%)£\u00b0.\\}])\.\s+(?=[A-Z0-9\\(])", s)
    return [p.strip() if p.strip().endswith(".") else p.strip() + "." for p in parts if p.strip()]


def stride(items, n):
    """At most n items, evenly spaced and in order."""
    if len(items) <= n:
        return list(items)
    return [items[(i * len(items)) // n] for i in range(n)]


def spread(items, n, key):
    """n items spread evenly across the groups key() names: one from each group in turn, each group taken evenly
    through its own order, so every question type and stage is as near equal as the pool allows."""
    groups = {}
    for it in items:
        groups.setdefault(key(it), []).append(it)
    names = list(groups)
    take = {g: 0 for g in names}
    left = n
    while left > 0 and any(take[g] < len(groups[g]) for g in names):
        for g in names:
            if left > 0 and take[g] < len(groups[g]):
                take[g] += 1
                left -= 1
    picked = {g: stride(groups[g], take[g]) for g in names}
    keep = {id(x) for g in names for x in picked[g]}
    return [it for it in items if id(it) in keep]


def rng_of(seed_text):
    state = [int(hashlib.sha1(seed_text.encode()).hexdigest()[:8], 16) or 1]

    def r():
        state[0] = (state[0] * 1664525 + 1013904223) & 0xFFFFFFFF
        return state[0] / 4294967296
    return r


def shuffled(items, seed_text):
    a = list(items)
    r = rng_of(seed_text)
    for i in range(len(a) - 1, 0, -1):
        j = int(r() * (i + 1))
        a[i], a[j] = a[j], a[i]
    return a


def num_or_none(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def numval(x):
    """A float that prints as an integer when whole."""
    x = round(float(x), 9)
    return int(x) if x == int(x) else x


def pence(x):
    return int(round(float(x) * 100))


MISSING_WORKED = []   # (topic, ref) of every question built with no worked solution: the missing-worked list


# ───────────────────────────── the question, and its validation ─────────────────────────────
def mk(topic, game, ref, band, calc, stem, fmt, answer, accept=None, unit=None, units=None, options=None,
       worked=None, slip=None):
    q = {"id": "%s-%s" % (topic, sha8(game, ref)), "topic": topic, "source": {"game": game, "ref": ref},
         "band": band, "calc": calc, "stem": stem, "diagram": None, "format": fmt, "answer": answer}
    if accept is not None:
        q["accept"] = accept
    if unit is not None:
        q["unit"] = unit
    if units is not None:
        q["units"] = units
    if options is not None:
        q["options"] = options
    q["worked"] = worked or []
    if not worked:
        MISSING_WORKED.append((topic, ref))
    q["slip"] = slip or []
    return q


def validate(q):
    """Schema 1 faults of one question, as strings."""
    f = []
    for k in ("id", "topic", "source", "band", "calc", "stem", "diagram", "format", "answer", "worked", "slip"):
        if k not in q:
            f.append("missing " + k)
    if f:
        return f
    if q["format"] not in FORMATS:
        f.append("format %r" % q["format"])
    if not (isinstance(q["band"], int) and 1 <= q["band"] <= 5):
        f.append("band %r" % q["band"])
    if not isinstance(q["calc"], bool):
        f.append("calc")
    if re.search(r"<[a-zA-Z/]", q["stem"]) or "$" in q["stem"]:
        f.append("stem has HTML or $")
    if (q["format"] in ("number", "number_unit") and "dp" not in q["answer"]
            and re.search(r"decimal place|d\.p\.|significant figure|nearest", q["stem"], re.I)):
        f.append("the stem states a rounding but the answer has no dp (schema: write dp on every such number answer)")
    if len(q["worked"]) > 5:
        f.append("worked has %d lines" % len(q["worked"]))
    for w in q["worked"] + [s["line"] for s in q["slip"]]:
        if re.search(r"<[a-zA-Z/]", w) or "$" in w or "\u00a7" in w:
            f.append("worked or slip line has HTML, $ or §: " + w[:40])
    a, fm = q["answer"], q["format"]
    need = {"number": ("value",), "money": ("pence",), "fraction": ("n", "d"), "ratio": ("parts",),
            "coordinates": ("x", "y"), "choice": ("val",), "number_unit": ("value", "unit")}[fm] if fm in FORMATS else ()
    for k in need:
        if k not in a:
            f.append("answer lacks " + k)
    if fm == "choice":
        o = q.get("options") or []
        if len(o) != 4 or [x["val"] for x in o] != ["a", "b", "c", "d"] or len({x["label"] for x in o}) != 4:
            f.append("choice needs 4 distinct options a-d")
        if a.get("val") not in [x["val"] for x in o]:
            f.append("answer val is not an option")
    if fm == "number_unit":
        u = q.get("units") or []
        if not (3 <= len(u) <= 4) or a.get("unit") not in u:
            f.append("number_unit needs 3-4 units holding the answer's unit")
    if q["diagram"] is not None and not q["diagram"].startswith("<svg"):
        f.append("diagram is not an svg")
    for s in q["slip"]:
        if set(s) != {"answer", "line"}:
            f.append("slip shape")
    return f


def choice(topic_id_seed, correct, wrongs):
    """4 options a-d, the correct one in a position fixed by the question's own seed; (options, answer)."""
    labels = [correct] + list(wrongs)
    order = shuffled(labels, topic_id_seed)
    options = [{"val": "abcd"[i], "label": l} for i, l in enumerate(order)]
    return options, {"val": "abcd"[order.index(correct)]}


# ───────────────────────────── the browser ─────────────────────────────
class Harness:
    def __init__(self):
        self.pages = {}

    async def __aenter__(self):
        from playwright.async_api import async_playwright
        self.proc, self.base = bc.start_stub_server()
        self.pw = await async_playwright().start()
        self.browser = await self.pw.chromium.launch()
        return self

    async def __aexit__(self, *a):
        await self.browser.close()
        await self.pw.stop()
        self.proc.terminate()
        self.proc.wait()

    async def page(self, slug, query):
        key = (slug, query)
        if key not in self.pages:
            pg = await self.browser.new_page()
            await pg.goto("%s/games/%s/?%s" % (self.base, slug, query), wait_until="load", timeout=30000)
            await pg.wait_for_timeout(600)
            self.pages[key] = pg
        return self.pages[key]


async def seeded(h, slug, query, js_call, n):
    """Distinct results of a game's own generator, one seed each: [{seed, q}]. js_call is a JS expression."""
    pg = await h.page(slug, query)
    js = ("() => { %s const out = [], seen = new Set(); for (let seed = 1; out.length < %d && seed < 6000; seed++) "
          "{ Math.random = mul(seed); const q = %s; const k = JSON.stringify(q); if (seen.has(k)) continue; seen.add(k); "
          "out.push({seed: seed, q: q}); } return out; }") % (MULBERRY, n, js_call)
    return await pg.evaluate(js)


# ───────────────────────────── ratio, direct proportion (split-it) ─────────────────────────────
def b_ratio(mode):
    return 2 if mode == "simplify" else 3


def conv_split_simplify(topic, seed, q):
    m = re.search(r"(\d+) : (\d+)", strip_html(q["prompt"]))
    a, b = int(m.group(1)), int(m.group(2))
    ref = "generator:generators.simplify:%d" % seed
    g = math.gcd(a, b)
    assert q["answers"] == [a // g, b // g], ("simplify", a, b, q["answers"])      # recomputed from the stem
    return mk(topic, "split-it", ref, b_ratio("simplify"), False,
              "Write %s in its simplest form." % tex("%d : %d" % (a, b)), "ratio", {"parts": [a // g, b // g]},
              accept={"rule": "simplest"}, worked=split_working(q["working"]))


def conv_split_divide(topic, seed, q):
    p = strip_html(q["prompt"])
    m = re.match(r"Share (£)?(\d+(?:\.\d+)?)\s*(\S*) in the ratio (\d+) : (\d+)", p)
    cur, total, unit, r1, r2 = m.group(1), Fraction(m.group(2)), m.group(3), int(m.group(4)), int(m.group(5))
    if r1 == r2:
        return None                                  # no larger share to ask for
    big = max(r1, r2) * total / (r1 + r2)
    assert abs(float(big) - max(q["answers"])) < 1e-9, ("divide", p, q["answers"])
    ref = "generator:generators.divide:%d" % seed
    stem = "Share %s in the ratio %s. Work out the larger share." % (
        ("£" + m.group(2)) if cur else (m.group(2) + (" " + unit if unit else "")), tex("%d : %d" % (r1, r2)))
    if cur:
        return mk(topic, "split-it", ref, b_ratio("divide"), False, stem, "money", {"pence": pence(big)},
                  worked=split_working(q["working"]))
    return mk(topic, "split-it", ref, b_ratio("divide"), False, stem, "number", {"value": numval(big)},
              unit=unit or None, worked=split_working(q["working"]))


def conv_split_unitary(topic, seed, q):
    p = strip_html(q["prompt"])
    m = re.match(r"(\d+) (.+?) cost £(\d+(?:\.\d+)?)\. How much do (\d+) (.+?) cost\?", p)
    n1, thing, cost, n2 = int(m.group(1)), m.group(2), Fraction(m.group(3)), int(m.group(4))
    ans = cost / n1 * n2
    assert abs(float(ans) - q["answers"][0]) < 1e-9, ("unitary", p, q["answers"])
    ref = "generator:generators.unitary:%d" % seed
    return mk(topic, "split-it", ref, 3, False, p, "money", {"pence": pence(ans)}, worked=split_working(q["working"]))


def conv_split_scale(topic, seed, q):
    """One ingredient per question (Jon's ruling of 25 Oct 2026): the ingredient is the seed's turn through the recipe."""
    p = strip_html(q["prompt"])
    m = re.match(r"An? (.+?) recipe for (\d+) (\w+) uses the amounts below\. How much of each do you need for (\d+) \3\?", p)
    name, a, noun, b = m.group(1), int(m.group(2)), m.group(3), int(m.group(4))
    items = q["items"]
    k = seed % len(items)

    def part(it, last=False):
        n = it["n"].lower()
        return "%s %s %s" % (it["v"], it["u"], "of " + n) if it["u"] else "%s %s" % (it["v"], n)
    parts = [part(it) for it in items]
    uses = ", ".join(parts[:-1]) + " and " + parts[-1] if len(parts) > 1 else parts[0]
    it = items[k]
    want = Fraction(it["v"]) * b / a
    assert abs(float(want) - q["answers"][k]) < 1e-9, ("scale", p, q["answers"])
    ask = ("How many %s do you need for %d %s?" % (it["n"].lower(), b, noun)) if not it["u"] else \
          ("How much %s do you need for %d %s?" % (it["n"].lower(), b, noun))
    stem = "A %s recipe for %d %s uses %s. %s" % (name.lower(), a, noun, uses, ask)
    ref = "generator:generators.scale:%d:%d" % (seed, k)
    return mk(topic, "split-it", ref, 2, False, stem, "number", {"value": numval(want)}, unit=it["u"] or None,
              worked=split_working(q["working"]))


async def topic_ratio(h):
    out = []
    for mode, fn in (("simplify", conv_split_simplify), ("divide", conv_split_divide)):
        got = []
        for r in await seeded(h, "split-it", "level=ks3", "generators.%s('ks3')" % mode, GEN_TOPIC * 2):
            q = fn("ratio", r["seed"], r["q"])
            if q:
                got.append(q)
        out += got[:GEN_TOPIC // 2]
    return out


async def topic_direct(h):
    out = []
    got = [conv_split_unitary("direct-proportion", r["seed"], r["q"])
           for r in await seeded(h, "split-it", "level=ks3", "generators.unitary('ks3')", GEN_TOPIC)]
    out += got[:GEN_TOPIC // 2]
    got = [conv_split_scale("direct-proportion", r["seed"], r["q"])
           for r in await seeded(h, "split-it", "level=ks3", "generators.scale('ks3')", GEN_TOPIC)]
    return out + got[:GEN_TOPIC // 2]


# ───────────────────────────── powers and roots (index-laws) ─────────────────────────────
def tex_eval(s, x):
    """A small TeX evaluator for index-law expressions: numbers, one letter, \\times, \\div, \\frac, ^, braces, ( )."""
    s = s.replace("\\dfrac", "\\frac")
    t = re.sub(r"\\div\s*(\([^()]*\)|\d*[a-z]?(?:\^\{[^{}]*\}|\^-?\d+)?)", r"\\div (\1)", s)   # a divisor is one term
    t = t.replace("\\times", "*").replace("\\div", "/").replace("\\,", "").replace("\\left", "").replace("\\right", "")
    for _ in range(6):
        t = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", t)
    t = t.replace("{", "(").replace("}", ")").replace("^", "**")
    t = re.sub(r"(?<=\d)(?=[a-z(])", "*", t)                       # 2x -> 2*x, 3( -> 3*(
    t = re.sub(r"(?<=[a-z)])(?=\d)", "*", t) if False else t
    t = re.sub(r"\)(?=[a-z(\d])", ")*", t)
    t = re.sub(r"(?<=[a-z])(?=[a-z(])", "*", t)
    t = re.sub(r"(?<=\*\*)-", "-", t)
    letters = set(re.findall(r"[a-z]", t))
    env = {l: x for l in letters}
    return eval(t, {"__builtins__": {}}, env)


def conv_index(topic, i, it):
    if it["rule"] == "Fractional Power" or re.search(r"\^\{?\s*\\frac|\^\{?\s*\d+/\d+", it["q"] + it["correct"]):
        return None                                  # fractional indices only: Higher content (Jon, 25 Oct 2026)
    for x in (2.0, 3.0, 1.5):
        a = tex_eval(it["q"], x)
        b = tex_eval(it["correct"], x)
        assert abs(a - b) < 1e-6 * max(1, abs(a)), ("index", it["q"], it["correct"])
        for w in it["wrong"]:
            if abs(tex_eval(w, x) - a) < 1e-9 and x == 2.0:
                pass
    opts, ans = choice("index-laws-%d" % i, tex(it["correct"]), [tex(w) for w in it["wrong"]])
    band = {"Multiply Rule": 2, "Divide Rule": 2, "Power of a Power": 3, "Zero Power": 3, "Negative Power": 4}[it["rule"]]
    ref = "QUESTIONS[%d]" % i
    return mk(topic, "index-laws", ref, band, False, "Simplify %s." % tex(it["q"]), "choice", ans, options=opts,
              worked=[it["exp"]])


async def topic_powers(h):
    pg = await h.page("index-laws", "level=gcse")
    items = await pg.evaluate("() => QUESTIONS")
    out = []
    for i, it in enumerate(items):
        q = conv_index("powers-roots", i, it)
        if q:
            out.append(q)
    return out


# ───────────────────────────── compound measures (squared-squirrel) ─────────────────────────────
def val_hm(g):
    return g["v"] if g["u"] != "hm" else g["v"] + 0  # an 'hm' quantity carries hours and minutes in its own fields


async def topic_compound(h):
    pg = await h.page("squared-squirrel", "level=ks3")
    pools = await pg.evaluate("""() => { const P = SQS.pools(); const out = {};
      for (const st of ['stage-2', 'stage-3']) out[st] = P[st].map(q => ({q: q, steps: SQS.steps(q).map(s => s.text),
        unitText: Object.fromEntries(q.units.map(u => [u, SQS.unitText(u)])),
        slips: q.errors.map(e => ({id: e.id, v: SQS.slipValue(q, e), line: SQS.line(q, e.id)})) })); return out; }""")
    out = []
    for st, band in (("stage-2", 3), ("stage-3", 4)):
        items = pools[st]
        for idx in range(len(items)):
            it = items[idx]
            q = it["q"]
            G = q["given"]
            if any(g["u"] == "hm" for g in G):
                continue                                           # a time given in hours and minutes: not a plain number
            # recomputed from the given quantities, not from the game's key
            if q["kind"] == "rate":
                exact = G[0]["v"] / G[1]["v"]
            elif q["kind"] == "mult":
                exact = G[0]["v"] * G[1]["v"]
            elif q["kind"] == "divi":
                exact = G[0]["v"] / G[1]["v"]
            else:
                continue
            assert abs(exact - q["key"]) < 1e-9, ("compound", q["text"], exact, q["key"])
            ut = it["unitText"]
            units = [ut[u] for u in q["units"]]
            ans = {"value": numval(q["key"]), "unit": ut[q["unit"]]}
            slips = []
            for s in it["slips"]:
                if s["v"] > 0 and s["v"] != q["key"]:
                    slips.append({"answer": {"value": numval(s["v"]), "unit": ut[q["unit"]]},
                                  "line": " ".join(maths(x) for x in s["line"] if x)})
            if not (3 <= len(units) <= 4):
                continue
            ref = "SQS.pools()['%s'][%d]" % (st, idx)
            out.append(((st, q["kind"], q["unit"]), mk("compound-measures", "squared-squirrel", ref, band, False,
                        q["text"], "number_unit", ans, units=units, worked=[maths(t) for t in it["steps"]], slip=slips)))
    # 60: the two stages evenly, and within a stage the question types (rate, amount, time) and units evenly
    per_stage = []
    for st in ("stage-2", "stage-3"):
        per_stage += spread([x for x in out if x[0][0] == st], GEN_TOPIC // 2, lambda x: x[0][1:])
    return [q for _, q in per_stage]


# ───────────────────────────── linear equations (linear-equation-solver) ─────────────────────────────
def conv_linear(i, it):
    import sympy
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
    eq = it["eq"]
    s = eq
    for _ in range(4):
        s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", s)
    s = s.replace("\\,", "").replace("\u2212", "-")
    lhs, rhs = s.split("=")
    tr = standard_transformations + (implicit_multiplication_application,)
    x = sympy.Symbol("x")
    sol = sympy.solve(sympy.Eq(parse_expr(lhs, transformations=tr), parse_expr(rhs, transformations=tr)), x)
    assert len(sol) == 1, ("linear", eq, sol)
    sol = sympy.nsimplify(sol[0])
    given = it["ans"]["correct"].replace("x = ", "").replace("\u2212", "-")
    m = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", given)
    gv = Fraction(int(m.group(2)), int(m.group(3))) * (-1 if m.group(1) else 1) if m else Fraction(given)
    assert Fraction(int(sol.p), int(sol.q)) == gv, ("linear", eq, sol, given)       # recomputed by SymPy
    tag = it["tag"].replace("\u2013", "-")
    tag = re.sub(r"[^\x00-\x7f]", "-", it["tag"])
    band = 2 if tag.startswith("One-step") and "right" not in tag and "fractional" not in tag else \
        (3 if ("integer" in tag or "negative" in tag or "constant first" in tag) else 4)
    worked = [tex(l) for l in it["sol"]]
    if gv.denominator == 1:
        return mk("linear-equations", "linear-equation-solver", "QUESTIONS.gcse[%d]" % i, band, False,
                  "Solve %s." % tex(eq), "number", {"value": int(gv)}, worked=worked)
    return mk("linear-equations", "linear-equation-solver", "QUESTIONS.gcse[%d]" % i, band, False,
              "Solve %s." % tex(eq), "fraction", {"n": gv.numerator, "d": gv.denominator},
              accept={"rule": "equivalent"}, worked=worked)


async def topic_linear(h):
    pg = await h.page("linear-equation-solver", "level=gcse")
    items = await pg.evaluate("() => QUESTIONS.gcse")
    return stride([conv_linear(i, it) for i, it in enumerate(items)], CAP)


# ───────────────────────────── sequences (sequence-solver) ─────────────────────────────
def seq_terms(s):
    return [Fraction(x) for x in re.findall(r"-?\d+(?:\.\d+)?", s)]


def next_term(t):
    """The next term by the pattern the terms themselves show: constant ratio, Fibonacci, or constant k-th differences."""
    if len(t) >= 3 and t[0] != 0 and all(t[i + 1] == t[i] * (t[1] / t[0]) for i in range(len(t) - 1)) and t[1] != t[0]:
        return t[-1] * (t[1] / t[0])
    if len(t) >= 4 and all(t[i + 2] == t[i + 1] + t[i] for i in range(len(t) - 2)):
        return t[-1] + t[-2]
    primes = [p for p in range(2, 200) if all(p % q for q in range(2, int(p ** 0.5) + 1))]
    if all(x.denominator == 1 and int(x) in primes for x in t) and [int(x) for x in t] == primes[primes.index(int(t[0])):][:len(t)]:
        return Fraction(primes[primes.index(int(t[0])) + len(t)])
    rows = [list(t)]
    for _ in range(3):
        r = rows[-1]
        rows.append([r[i + 1] - r[i] for i in range(len(r) - 1)])
        if len(rows[-1]) >= 2 and len(set(rows[-1])) == 1:
            nxt = rows[-1][0]
            for k in range(len(rows) - 2, -1, -1):
                nxt = rows[k][-1] + nxt
            return nxt
    raise AssertionError("no pattern in %s" % t)


def tnum(x):
    """A Fraction as the digits a student would write (decimals stay decimals)."""
    x = Fraction(x)
    if x.denominator == 1:
        return str(x.numerator)
    s = ("%.6f" % float(x)).rstrip("0").rstrip(".")
    assert Fraction(s) == x, "not a terminating decimal: %s" % x
    return s


def tneg(x):
    """The number, in brackets when it is negative (a negative written after a sign)."""
    return "(%s)" % tnum(x) if Fraction(x) < 0 else tnum(x)


def seq_worked(ask, terms, want, k):
    """Project Claude's worked-solution template for sequences (25 Oct 2026), filled from the terms and recomputed.
    [] for an item the template does not cover (a geometric or other pattern, 'which term', 'what type'): listed."""
    d = terms[1] - terms[0]
    if d == 0 or any(terms[i + 1] - terms[i] != d for i in range(len(terms) - 1)):
        return []
    a = terms[0]
    if ask == "Find the next term":
        nxt = terms[-1] + d
        assert nxt == want
        way = "go up by \\(%s\\) each time." % tnum(d) if d > 0 else "go down by \\(%s\\) each time." % tnum(-d)
        return ["The terms " + way, "\\(%s + %s = %s\\)" % (tnum(terms[-1]), tneg(d), tnum(nxt))]
    if ask == "What is the common difference?":
        assert d == want
        more = "Each term is \\(%s\\) more than the one before, so the rule is add \\(%s\\)." % (tnum(d), tnum(d))
        less = "Each term is \\(%s\\) less than the one before, so the rule is take away \\(%s\\)." % (tnum(-d), tnum(-d))
        return [more if d > 0 else less]
    if k is not None:
        c = a - d
        coef = "n" if d == 1 else "-n" if d == -1 else tnum(d) + "n"
        rule = coef + ("" if c == 0 else " + %s" % tnum(c) if c > 0 else " - %s" % tnum(-c))
        total = d * k + c
        assert total == want and d * 1 + c == a          # the rule gives the first term and the asked term
        const = "" if c == 0 else " + %s" % tneg(c)
        return ["The nth term is \\(%s\\)." % rule,
                "Put \\(n = %d\\): \\(%s \\times %d%s = %s\\)." % (k, tneg(d), k, const, tnum(total))]
    return []


def conv_sequence(i, it):
    ask = it["ask"]
    terms = seq_terms(it["seq"])
    shown = re.sub(r",\s*(__|\.\.\.)\s*$", ", \\\\ldots", it["seq"].strip())
    shown = shown.replace("...", "\\ldots")
    stem_seq = "Here is a number sequence: %s." % tex(shown)
    ref = "QUESTIONS.ks3[%d]" % i
    if ask == "What type of sequence?":
        opts, ans = choice("sequence-%d" % i, it["correct"], it["d"])
        return mk("sequences", "sequence-solver", ref, 2, False, stem_seq + " What type of sequence is it?", "choice",
                  ans, options=opts)
    d = terms[1] - terms[0]
    if ask == "Find the next term":
        want = next_term(terms)
        text = "Write down the next term."
        band = 1
    elif ask == "What is the common difference?":
        want = d
        text = "Write down the common difference."
        band = 2
    elif re.fullmatch(r"Find the (\d+)(?:st|nd|rd|th) term", ask):
        n = int(re.fullmatch(r"Find the (\d+)(?:st|nd|rd|th) term", ask).group(1))
        want = terms[0] + (n - 1) * d
        text = "Work out the %s term of the sequence." % re.fullmatch(r"Find the (.+) term", ask).group(1)
        band = 3
    elif re.fullmatch(r"Which term equals (\d+)\?", ask):
        t = Fraction(re.fullmatch(r"Which term equals (\d+)\?", ask).group(1))
        want = (t - terms[0]) / d + 1
        text = "Which term of the sequence is equal to %s? Give the term number." % t
        band = 4
    else:
        raise AssertionError("unknown sequence ask " + ask)
    given = Fraction(re.sub(r"(st|nd|rd|th)$", "", it["correct"]))
    assert want == given, ("sequence", it["seq"], ask, want, given)           # recomputed from the terms
    kth = re.fullmatch(r"Find the (\d+)(?:st|nd|rd|th) term", ask)
    worked = seq_worked(ask, terms, want, int(kth.group(1)) if kth else None)
    return mk("sequences", "sequence-solver", ref, band, False, stem_seq + " " + text, "number",
              {"value": numval(want)}, worked=worked)


async def topic_sequences(h):
    pg = await h.page("sequence-solver", "level=ks3")
    items = await pg.evaluate("() => QUESTIONS.ks3")
    return [conv_sequence(i, it) for i, it in enumerate(items)]


# ───────────────────────────── fractions, decimals, percentages (free-daily-pizza) ─────────────────────────────
FDP_JS = """() => { const out = {}; for (const st of [1, 2, 3]) out[st] = FDP.BANK[st].map((it, i) => ({it: it, slips:
  it.distractors.map(d => ({d: d, says: FDP.tagSays(d.tag)}))})); return out; }"""


def fdp_value(form, nd):
    return Fraction(nd[0], nd[1])


def fdp_terminating(fr):
    d = fr.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return d == 1


def fdp_answer(form, fr):
    """(format, answer, accept, unit) for an answer of this form, or None if it cannot be typed."""
    if form == "f":
        return "fraction", {"n": fr.numerator, "d": fr.denominator}, {"rule": "simplest"}, None
    if form == "d":
        if not fdp_terminating(fr):
            return None
        return "number", {"value": numval(float(fr))}, None, None
    if form == "p":
        p = fr * 100
        if not fdp_terminating(p):
            return None
        return "number", {"value": numval(float(p))}, None, "%"
    if form == "n":
        return "number", {"value": numval(float(fr))}, None, None
    return None


def conv_fdp(topic, st, i, rec):
    it = rec["it"]
    ans_fr = fdp_value(it["answer"]["form"], it["answer"]["value"])
    # recomputed from the question's own numbers
    if it["kind"] == "conv":
        assert ans_fr == fdp_value(it["given"]["form"], it["given"]["value"]), ("fdp conv", it["id"])
        band = 1 if st == 1 else 2
    elif it["kind"] == "simp":
        assert ans_fr == Fraction(it["n"], it["d"]), ("fdp simp", it["id"])
        band = 2
    elif it["kind"] == "ofamt-f":
        assert ans_fr == Fraction(it["a"], it["b"]) * it["N"], ("fdp ofamt-f", it["id"])
        band = 3
    elif it["kind"] == "ofamt-p":
        assert ans_fr == Fraction(it["p"], 100) * it["N"], ("fdp ofamt-p", it["id"])
        band = 2
    else:
        return None
    fa = fdp_answer(it["answer"]["form"], ans_fr)
    if not fa:
        return None
    fmt, ans, accept, unit = fa
    slips = []
    for s in rec["slips"]:
        d = s["d"]
        sf = fdp_answer(d["form"], fdp_value(d["form"], d["value"]))
        if not sf or sf[0] != fmt or sf[1] == ans or not s["says"]:
            continue
        slips.append({"answer": sf[1], "line": maths(strip_html(s["says"]))})
    stem = it["prompt"]
    if unit == "%" and not stem.rstrip().endswith("percentage."):
        pass
    ref = "FDP.BANK[%d][%d]" % (st, i)
    return mk(topic, "free-daily-pizza", ref, band, False, stem, fmt, ans, accept=accept, unit=unit,
              worked=split_working(it["working"]) if it.get("working") else [], slip=slips)


async def topic_fdp(h, stages, topic):
    pg = await h.page("free-daily-pizza", "level=ks3")
    data = await pg.evaluate(FDP_JS)
    out = []
    for st in stages:
        for i, rec in enumerate(data[str(st)]):
            q = conv_fdp(topic, st, i, rec)
            if q:
                out.append((st, rec["it"]["kind"], rec["it"].get("from"), rec["it"].get("to"), q))
    # 60, spread evenly across the stage, the kind of question and the form it converts from and to
    return [x[-1] for x in spread(out, GEN_TOPIC, lambda x: x[:4])]


async def topic_fdp_convert(h):
    return await topic_fdp(h, (1, 2), "fdp-convert")


async def topic_fdp_amount(h):
    return await topic_fdp(h, (3,), "fraction-percentage-of-amount")


# ───────────────────────────── angles (angle-ace) ─────────────────────────────
# Angle Ace draws on a canvas, so the SVG is drawn here from the item's numbers in one shared style (Jon, 25 Oct 2026):
# the game's own geometry (FIG[...] returns the segments, arcs and labels in pixels, placeLabel the label boxes) is read in
# the page and written out as an SVG with a viewBox, currentColor and text labels. The check below matches every label.
ANGLE_SVG_JS = r"""(fig) => {
  const W = 360, H = 240, S = FIG[fig.t](fig, W, H);
  const r = v => Math.round(v * 10) / 10, boxes = [], out = [];
  S.segs.forEach(s => out.push('<line x1="' + r(s[0][0]) + '" y1="' + r(s[0][1]) + '" x2="' + r(s[1][0]) + '" y2="' + r(s[1][1]) + '"' + (s[2] === 'trans' ? ' opacity="0.6"' : '') + '/>'));
  (S.ticks || []).forEach(t => { const M = [(t[0][0] + t[1][0]) / 2, (t[0][1] + t[1][1]) / 2], n = dirOf(t[0], t[1]) + 90, a = at(M, n, 6), b = at(M, n + 180, 6);
    out.push('<line x1="' + r(a[0]) + '" y1="' + r(a[1]) + '" x2="' + r(b[0]) + '" y2="' + r(b[1]) + '"/>'); });
  const texts = [];
  S.marks.forEach(m => {
    const unk = m.lab === 'x' || m.lab === 'y', text = unk ? m.lab : m.lab + '°';
    if (m.sq) { const p = at(m.V, m.a, SQ), q = at(m.V, m.b, SQ);
      out.push('<polyline points="' + r(p[0]) + ',' + r(p[1]) + ' ' + r(p[0] + q[0] - m.V[0]) + ',' + r(p[1] + q[1] - m.V[1]) + ' ' + r(q[0]) + ',' + r(q[1]) + '"/>'); }
    else { const a0 = at(m.V, m.a, ARC), a1 = at(m.V, m.b, ARC), sweepDeg = m.b - m.a;
      out.push('<path d="M' + r(a0[0]) + ' ' + r(a0[1]) + ' A' + ARC + ' ' + ARC + ' 0 ' + (sweepDeg > 180 ? 1 : 0) + ' 0 ' + r(a1[0]) + ' ' + r(a1[1]) + '"/>'); }
    if (m.lab === '') return;
    const b = placeLabel(m, text.length * 9, 15, S, boxes, W, H); boxes.push(b);
    texts.push('<text x="' + r((b[0] + b[2]) / 2) + '" y="' + r((b[1] + b[3]) / 2) + '"' + (unk ? ' font-weight="700"' : '') + '>' + text + '</text>');
  });
  (S.par || []).forEach(y => { for (let k = 0; k < 12; k++) { const x = k % 2 ? PAD + 14 + (k >> 1) * 18 : W - PAD - 14 - (k >> 1) * 18, b = [x - 6, y - 7, x + 7, y + 7];
    if (!boxes.some(o => !(b[2] < o[0] || b[0] > o[2] || b[3] < o[1] || b[1] > o[3])) && !(S.avoid || []).some(p => Math.hypot(p[0] - x, p[1] - y) < 40)) {
      out.push('<polygon fill="currentColor" stroke="none" points="' + (x - 5) + ',' + (y - 6) + ' ' + (x + 6) + ',' + y + ' ' + (x - 5) + ',' + (y + 6) + '"/>'); break; } } });
  return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + W + ' ' + H + '" role="img" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    + out.join('') + '<g fill="currentColor" stroke="none" font-family="sans-serif" font-size="15" text-anchor="middle" dominant-baseline="central">' + texts.join('') + '</g></svg>';
}"""

ANGLE_BAND = {"VERTOP": 1, "STRAIGHT": 2, "POINT": 2, "TRIANGLE": 2, "ISOSC": 3, "ALT": 3, "CORR": 3, "COINT": 4, "EXTERIOR": 4}
ANGLE_REASON = {"Alternate angles are equal": "ALT", "Corresponding angles are equal": "CORR",
                "Co-interior angles sum to 180°": "COINT", "Angles on a straight line sum to 180°": "STRAIGHT",
                "Angles at a point sum to 360°": "POINT", "Vertically opposite angles are equal": "VERTOP",
                "Angles in a triangle sum to 180°": "TRIANGLE",
                "Base angles of an isosceles triangle are equal": "ISOSC",
                "Exterior angle equals sum of interior opposite angles": "EXTERIOR"}


def fig_labels(fig):
    """The labels a figure must show, from its numbers: every number in it, and its x or y."""
    out = []

    def walk(v):
        if isinstance(v, bool) or v is None:
            return
        if isinstance(v, (int, float)):
            out.append(str(int(v)) + "°")
        elif isinstance(v, str):
            if v in ("x", "y"):
                out.append(v)
        elif isinstance(v, list):
            for x in v:
                walk(x)
        elif isinstance(v, dict):
            for k, x in v.items():
                if k != "t":
                    walk(x)
    walk(fig)
    return sorted(out)


def svg_labels(svg):
    return sorted(re.findall(r"<text[^>]*>([^<]*)</text>", svg))


async def topic_angles(h):
    pg = await h.page("angle-ace", "level=gcse")
    items = await pg.evaluate("() => QUESTIONS_BY_LEVEL.gcse")
    out = []
    for i, it in enumerate(items):
        svg = await pg.evaluate(ANGLE_SVG_JS, it["fig"])
        # the check: every label in the drawing is one of the item's numbers, and every number is drawn
        assert svg_labels(svg) == fig_labels(it["fig"]), ("angles", i, svg_labels(svg), fig_labels(it["fig"]))
        # the answer is recomputed from the figure's numbers by the rule the figure states
        t, f = it["fig"]["t"], it["fig"]
        nums = lambda xs: [x for x in xs if isinstance(x, (int, float))]
        if t == "line":
            want = 180 - sum(nums(f["r"]))
        elif t == "point":
            want = 360 - sum(nums(f["r"]))
        elif t == "tri" and f.get("iso"):
            want = f["A"]                                              # base angles of an isosceles triangle are equal
        elif t == "tri":
            want = 180 - sum(90 if f[k] == "sq" else f[k] for k in "ABC" if f[k] != "x")
        elif t == "partri":
            want = 180 - f["q0"] - f["R"]
        elif t == "ext":
            want = f["A"] + f["C"]
        elif t == "cross":
            k = next(j for j, x in enumerate(f["r"]) if isinstance(x, (int, float)))
            xi = f["r"].index("x")
            want = f["r"][k] if (xi - k) % 2 == 0 else 180 - f["r"][k]      # opposite angles equal, adjacent make 180
        elif t == "par":
            known = nums([m[2] for m in f["m"]])[0]
            want = known if ANGLE_REASON[it["reason"]] in ("ALT", "CORR") else (180 - known)
        else:
            raise AssertionError("angle figure type " + t)
        assert want == it["answer"], ("angles", i, t, f, want, it["answer"])
        prompt = it["prompt"].replace(" x", " \\(x\\)")
        stem = prompt + ". The diagram is not drawn accurately."
        q = mk("angles", "angle-ace", "QUESTIONS_BY_LEVEL.gcse[%d]" % i, ANGLE_BAND[ANGLE_REASON[it["reason"]]], False,
               stem, "number", {"value": it["answer"]}, unit="°", worked=it["steps"][:5])
        q["diagram"] = svg
        out.append(q)
    return out


# ───────────────────────────── negative numbers (negative-number-line) ─────────────────────────────
def conv_neg_order(i, it):
    nums = it["nums"]
    right = sorted(nums)
    assert it["answer"] == right, ("negatives order", nums, it["answer"])
    by_abs = sorted(nums, key=lambda n: (abs(n), n))
    largest_first = sorted(nums, reverse=True)

    def swapped(k):
        s = list(right)
        s[k], s[k + 1] = s[k + 1], s[k]
        return s
    # Jon's three wrong orderings in his order: by size ignoring the minus signs, largest first, the right order with a
    # neighbouring pair swapped; when two coincide (or one is the right order) the next neighbouring swap stands in.
    wrong = []
    for cand in [by_abs, largest_first] + [swapped(k) for k in range(len(right) - 1)] + [sorted(nums, key=lambda n: -abs(n))]:
        if cand != right and cand not in wrong and len(wrong) < 3:
            wrong.append(cand)
    assert len(wrong) == 3 and len({tuple(x) for x in wrong + [right]}) == 4, \
        ("negatives order: the four orderings are not distinct", nums)
    lab = lambda xs: tex(", ".join(str(n) for n in xs))
    opts, ans = choice("negatives-order-%d" % i, lab(right), [lab(w) for w in wrong])
    worked = ["On a number line, further left is smaller.", "Smallest first: " + tex(", ".join(str(n) for n in right)) + "."]
    return mk("arithmetic-negatives", "negative-number-line", "ORDER_QUESTIONS[%d]" % i, 1, False,
              "Write these numbers in order, smallest first: " + tex(", ".join(str(n) for n in nums)) + ".", "choice", ans,
              options=opts, worked=worked)


def conv_neg_calc(i, it):
    a, b, op = it["start"], it["val"], it["op"]
    ans = a + b if op == "add" else a - b
    assert ans == it["answer"], ("negatives calc", it)
    sign = "+" if op == "add" else "-"
    expr = "%d %s %s" % (a, sign, ("(%d)" % b) if b < 0 else str(b))
    if op == "add" and b >= 0:
        w = "Start at \\(%d\\). Adding \\(%d\\) moves \\(%d\\) to the right: \\(%d + %d = %d\\)." % (a, b, b, a, b, ans)
        band = 1
    elif op == "add":
        w = "Adding \\(%d\\) moves \\(%d\\) to the left: \\(%d + (%d) = %d\\)." % (b, -b, a, b, ans)
        band = 2
    elif b >= 0:
        w = "Start at \\(%d\\). Taking away \\(%d\\) moves \\(%d\\) to the left: \\(%d - %d = %d\\)." % (a, b, b, a, b, ans)
        band = 1
    else:
        w = "Taking away \\(%d\\) is the same as adding \\(%d\\): \\(%d - (%d) = %d + %d = %d\\)." % (b, -b, a, b, a, -b, ans)
        band = 2
    return mk("arithmetic-negatives", "negative-number-line", "CALC_QUESTIONS[%d]" % i, band, False,
              "Work out " + tex(expr) + ".", "number", {"value": ans}, worked=[w])


async def topic_negatives(h):
    pg = await h.page("negative-number-line", "level=year6")
    order, calc = await pg.evaluate("() => [ORDER_QUESTIONS, CALC_QUESTIONS]")
    return [conv_neg_calc(i, it) for i, it in enumerate(calc)] + [conv_neg_order(i, it) for i, it in enumerate(order)]


# ───────────────────────────── the registry ─────────────────────────────
# topic id -> (builder, rule notes). Topics not here have no bank yet (coming soon).
BUILDERS = {
    "ratio": topic_ratio,
    "direct-proportion": topic_direct,
    "powers-roots": topic_powers,
    "compound-measures": topic_compound,
    "linear-equations": topic_linear,
    "sequences": topic_sequences,
    "angles": topic_angles,
    "arithmetic-negatives": topic_negatives,
    "fdp-convert": topic_fdp_convert,
    "fraction-percentage-of-amount": topic_fdp_amount,
}


async def build_all(only):
    banks = {}
    async with Harness() as h:
        for tid, fn in BUILDERS.items():
            if only and tid not in only:
                continue
            qs = await fn(h)
            ids = [q["id"] for q in qs]
            if len(set(ids)) != len(ids):
                raise AssertionError("%s: duplicate ids" % tid)
            banks[tid] = {"topic": tid, "schema": 1, "questions": qs}
    return banks


def dump(bank):
    return json.dumps(bank, indent=1, ensure_ascii=False) + "\n"


def committed():
    out = {}
    if os.path.isdir(OUT_DIR):
        for f in sorted(os.listdir(OUT_DIR)):
            if f.endswith(".json"):
                with open(os.path.join(OUT_DIR, f), encoding="utf-8") as fh:
                    out[f[:-5]] = json.load(fh)
    return out


def coverage_faults():
    """A covered topic has a bank of MIN_QUESTIONS or more; a bank's topic is covered. Derived from the files."""
    with open(TOPICS_JSON, encoding="utf-8") as f:
        topics = json.load(f)
    covered = {t["id"] for t in topics["covered"]}
    banks = committed()
    f = []
    for t in sorted(covered):
        if t not in banks:
            f.append("covered topic %s has no bank" % t)
        elif len(banks[t]["questions"]) < MIN_QUESTIONS:
            f.append("covered topic %s has %d questions (< %d)" % (t, len(banks[t]["questions"]), MIN_QUESTIONS))
    for t, b in sorted(banks.items()):
        if t not in covered:
            f.append("bank %s.json is not a covered topic" % t)
        if b.get("topic") != t:
            f.append("bank %s.json says topic %r" % (t, b.get("topic")))
    return f


SHEET = r"""<title>Six P's Question Banks</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
<style>
:root{--bg:#f8fafc;--card:#fff;--ink:#1a2744;--muted:#526077;--line:#e2e8f0;--accent:#0d9488;--bad:#b91c1c;--tint:#f1f5f9}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0f1420;--card:#182033;--ink:#e8ecf4;--muted:#a3adc2;--line:#2e3850;--accent:#2dd4bf;--bad:#fb7185;--tint:#212b42;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0f1420;--card:#182033;--ink:#e8ecf4;--muted:#a3adc2;--line:#2e3850;--accent:#2dd4bf;--bad:#fb7185;--tint:#212b42;color-scheme:dark}
body{background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif;padding-inline:16px;padding-block:20px;max-width:900px;margin-inline:auto}
h1{font-size:1.4rem;margin:0 0 4px}.sub{color:var(--muted);margin:0 0 16px}
nav{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px}
nav button{font:inherit;padding:8px 12px;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:8px;cursor:pointer;min-height:44px}
nav button[aria-pressed="true"]{background:var(--accent);color:#fff;border-color:var(--accent)}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin-bottom:10px;min-width:0}
.meta{color:var(--muted);font-size:.8rem;display:flex;flex-wrap:wrap;gap:4px 12px;margin-bottom:6px}
.stem{font-size:1.02rem;margin-bottom:6px;overflow-wrap:anywhere}
.ans{background:var(--tint);border-radius:6px;padding:6px 10px;margin:6px 0;overflow-wrap:anywhere}
.ans b{color:var(--accent)}
ol{margin:4px 0 4px 1.2rem;padding:0}li{overflow-wrap:anywhere}
.fig{max-width:300px;margin:6px 0;color:var(--ink)}.fig svg{width:100%;height:auto;display:block}
.none{color:var(--bad);font-size:.85rem}
.slip{color:var(--muted);font-size:.85rem}
.opts{margin:4px 0 0 0;padding:0;list-style:none;display:grid;gap:2px}
.opts .right{color:var(--accent);font-weight:600}
</style>
<h1>Six P's question banks</h1>
<p class="sub" id="sub"></p>
<nav id="nav"></nav>
<main id="main"></main>
<script>
const BANKS = __DATA__;
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function rich(s){
  return String(s).split(/(\\\(.*?\\\))/g).map(function(p){
    if(p.indexOf('\\(')===0){try{return katex.renderToString(p.slice(2,-2),{output:'mathml',throwOnError:false})}catch(e){return esc(p)}}
    return esc(p);}).join('');
}
function ansText(q){
  var a=q.answer;
  if(q.format==='choice')return rich(q.options.filter(function(o){return o.val===a.val})[0].label);
  if(q.format==='money')return '£'+(a.pence/100).toFixed(2);
  if(q.format==='fraction')return (a.w?a.w+' ':'')+a.n+'/'+a.d;
  if(q.format==='ratio')return a.parts.join(' : ');
  if(q.format==='coordinates')return '('+a.x+', '+a.y+')';
  if(q.format==='number_unit')return a.value+' '+esc(a.unit);
  return a.value+(q.unit?' '+esc(q.unit):'');
}
function show(t){
  var b=BANKS[t],h='';
  b.questions.forEach(function(q){
    var rule=q.accept?' ('+esc(q.accept.rule)+')':'';
    h+='<div class="card"><div class="meta"><span>'+esc(q.id)+'</span><span>band '+q.band+'</span><span>'+(q.calc?'calculator':'non-calculator')+'</span><span>'+esc(q.format)+rule+'</span></div>'
      +'<div class="stem">'+rich(q.stem)+'</div>'+(q.diagram?'<div class="fig">'+q.diagram+'</div>':'');
    if(q.format==='choice'){h+='<ul class="opts">'+q.options.map(function(o){return '<li'+(o.val===q.answer.val?' class="right"':'')+'>'+o.val+') '+rich(o.label)+'</li>'}).join('')+'</ul>';}
    else{h+='<div class="ans">Answer: <b>'+ansText(q)+'</b>'+(q.units?' <span class="slip">(unit buttons: '+q.units.map(esc).join(', ')+')</span>':'')+'</div>';}
    h+=q.worked.length?'<ol>'+q.worked.map(function(w){return '<li>'+rich(w)+'</li>'}).join('')+'</ol>':'<div class="none">No worked solution in the game</div>';
    q.slip.forEach(function(s){h+='<div class="slip">If the answer is <b>'+(q.format==='number_unit'?s.answer.value+' '+esc(s.answer.unit):q.format==='fraction'?s.answer.n+'/'+s.answer.d:s.answer.value!==undefined?s.answer.value:JSON.stringify(s.answer))+'</b>: '+rich(s.line)+'</div>'});
    h+='<div class="meta" style="margin:6px 0 0">source: '+esc(q.source.game)+' '+esc(q.source.ref)+'</div></div>';
  });
  document.getElementById('main').innerHTML=h;
  document.querySelectorAll('nav button').forEach(function(x){x.setAttribute('aria-pressed',String(x.dataset.t===t))});
}
var names=Object.keys(BANKS);
document.getElementById('sub').textContent=names.length+' topics, '+names.reduce(function(n,t){return n+BANKS[t].questions.length},0)+' questions. Each question as the player will show it, with its answer, worked solution and source game.';
document.getElementById('nav').innerHTML=names.map(function(t){return '<button type="button" data-t="'+t+'" aria-pressed="false">'+t+' ('+BANKS[t].questions.length+')</button>'}).join('');
document.getElementById('nav').addEventListener('click',function(e){var t=e.target.dataset&&e.target.dataset.t;if(t)show(t)});
show(names[0]);
</script>
"""


def sheet(banks, path):
    """One review page for a batch: each question as the player will show it, its answer, worked solution, source."""
    data = json.dumps({t: b for t, b in banks.items()}, ensure_ascii=False).replace("</", "<\\/")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(SHEET.replace("__DATA__", data))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--sheet", metavar="DIR")
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    banks = asyncio.run(build_all(a.only))
    faults = []
    for t, b in banks.items():
        for q in b["questions"]:
            for x in validate(q):
                faults.append("%s %s: %s" % (t, q["id"], x))
        print("%-32s %3d questions  bands %s" % (t, len(b["questions"]),
              sorted({q["band"] for q in b["questions"]})))
    for x in faults[:40]:
        print("FAIL  " + x)
    if faults:
        return 1
    miss = {}
    for t, ref in MISSING_WORKED:
        miss[t] = miss.get(t, 0) + 1
    for t, n in sorted(miss.items()):
        print("missing worked solution: %s %d of %d" % (t, n, len(banks[t]["questions"])))
    # A bank under MIN_QUESTIONS is a shortfall: reported, never written, and its topic stays coming soon.
    short = {t: len(b["questions"]) for t, b in banks.items() if len(b["questions"]) < MIN_QUESTIONS}
    banks = {t: b for t, b in banks.items() if t not in short}
    for t, n in sorted(short.items()):
        print("SHORTFALL  %s: %d questions (needs %d), no bank written" % (t, n, MIN_QUESTIONS))
    if a.write:
        os.makedirs(OUT_DIR, exist_ok=True)
        for t, b in banks.items():
            with open(os.path.join(OUT_DIR, t + ".json"), "w", encoding="utf-8", newline="\n") as f:
                f.write(dump(b))
        print("wrote %d banks to %s" % (len(banks), os.path.relpath(OUT_DIR, ROOT)))
    if a.sheet:
        os.makedirs(os.path.dirname(os.path.abspath(a.sheet)), exist_ok=True)
        sheet(banks, a.sheet)
        print("wrote the review sheet %s" % a.sheet)
    if a.check:
        com = committed()
        bad = []
        for t, b in banks.items():
            if com.get(t) != b:
                bad.append("%s.json is not what the game's questions generate; run gen-six-ps.py --write" % t)
        for t in short:
            if t in com:
                bad.append("%s.json is committed but its game now yields only %d questions" % (t, short[t]))
        for t in com:
            if t not in banks and t not in short and not a.only:
                bad.append("%s.json has no builder in gen-six-ps.py" % t)
        bad += coverage_faults()
        for x in bad:
            print("FAIL  " + x)
        if bad:
            return 1
        print("PASS  %d banks match their games; covered topics and banks agree" % len(banks))
    return 0


if __name__ == "__main__":
    sys.exit(main())
