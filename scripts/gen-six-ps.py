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
            and re.search(r"decimal place|d\.p\.", q["stem"], re.I)):
        f.append("the stem asks for decimal places but the answer has no dp (schema: write dp on every such number answer; significant figures are checked with the rounding)")
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


# ───────────────────────────── authored questions and worked lines (data/six-ps/) ─────────────────────────────
# Project Claude's two data files (25 Oct 2026): authored.json holds questions in the schema for the topics the games
# cannot fill (source.game "authored"); worked-lines.json holds the worked lines for the sequences items the template
# does not cover, and the choice versions and worked lines for equation-builder's forming-equations items and
# probability-pioneer's stage-1 items. The script merges them into their banks and checks them like any other item.
DATA_DIR = os.path.join(ROOT, "data", "six-ps")
NUMBER = re.compile(r"(?<![\w.])-?\d+(?:\.\d+)?")


def load_data(name):
    with open(os.path.join(DATA_DIR, name), encoding="utf-8") as f:
        return json.load(f)


def numbers_in(s):
    """The numbers written in a string (a minus sign belongs to the number it touches), as Fractions."""
    return [Fraction(x) for x in NUMBER.findall(s.replace("\u2212", "-"))]


def tex_to_sympy(s, positive=False):
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
    t = s.replace("\\dfrac", "\\frac").replace("\u2212", "-").replace("\u00f7", "/").replace("\u00d7", "*")
    t = t.replace("\\times", "*").replace("\\left", "").replace("\\right", "")
    for sym, letter in (("\\Delta T", "Z"), ("\\rho", "W")):      # a one-letter stand-in, only where that letter is free
        if sym in t:
            assert letter not in t, ("tex_to_sympy: %s needs a free %s" % (sym, letter), s)
            t = t.replace(sym, letter)
    t = t.replace("\\pi", " pi ")
    for _ in range(6):                                           # innermost first: a fraction in a root in a fraction
        t = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", t)
        t = re.sub(r"\\sqrt\[(\d)\]\{([^{}]*)\}", r" ((\2)**(1/\1)) ", t)
        t = re.sub(r"\\sqrt\{([^{}]*)\}", r" sqrt(\1) ", t)
    t = t.replace("{", "(").replace("}", ")").replace("^", "**")
    # a run of letters is a product of one-letter symbols ("as" is a Python keyword and must not reach the parser whole)
    t = re.sub(r"[A-Za-z]{2,}", lambda m: m.group(0) if m.group(0) in ("pi", "sqrt") else "*".join(m.group(0)), t)
    tr = standard_transformations + (implicit_multiplication_application,)
    import sympy
    local = {c: (sympy.Symbol(c, positive=True) if positive else sympy.Symbol(c)) for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"}   # S, N, C, E, I, Q are letters here
    local["pi"] = sympy.pi
    return parse_expr(t, local_dict=local, transformations=tr)


def same_equation(a, b):
    """Two equations (strings 'L = R', TeX allowed) say the same thing: L1 - R1 equals L2 - R2."""
    import sympy
    la, ra = a.split("=")
    lb, rb = b.split("=")
    return sympy.simplify((tex_to_sympy(la) - tex_to_sympy(ra)) - (tex_to_sympy(lb) - tex_to_sympy(rb))) == 0


# --- the sequences worked lines: filled by bank id, every number in a line recomputed from the sequence ---
def seq_allowed(stem):
    seq = re.search(r"sequence: \\\((.*?)\\\)", stem).group(1)
    t = [Fraction(x) for x in re.findall(r"-?\d+(?:\.\d+)?", seq.replace("\\ldots", ""))]
    ok = set(t)
    diffs = [t[i + 1] - t[i] for i in range(len(t) - 1)]
    ok |= set(diffs) | {abs(x) for x in diffs}
    d2 = [diffs[i + 1] - diffs[i] for i in range(len(diffs) - 1)]
    ok |= set(d2) | {abs(x) for x in d2}
    if t[0]:
        ok |= {t[1] / t[0]}
    d = diffs[0]
    c = t[0] - d
    ok |= {c, -c, t[0], d, -d, Fraction(1)}
    for q in numbers_in(stem.split("\\)")[-1]):                     # the target (the 10th term, equals 41)
        ok.add(q)
        ok |= {q - c, (q - c) / d if d else 0, d * q, d * q + c, d * q - d + t[0]}
    ok |= {Fraction(i) for i in range(1, len(t) + 4)}
    return ok


def apply_sequence_lines(qs):
    lines = load_data("worked-lines.json")["sequences_worked_by_id"]
    byid = {q["id"]: q for q in qs}
    for qid, worked in lines.items():
        q = byid.get(qid)
        if q is None:
            raise AssertionError("worked-lines.json: no sequences question %s" % qid)
        if q["worked"]:
            raise AssertionError("worked-lines.json: %s already has worked lines" % qid)
        allowed = seq_allowed(q["stem"]) | {Fraction(q["answer"]["value"])} if q["format"] == "number" else None
        for w in worked:
            if allowed is not None:
                for n in numbers_in(w):
                    if n in allowed:
                        continue
                    # a prime sequence's line may name the numbers between the last term and the next prime: each must
                    # be a whole number in that gap and not prime
                    seq_t = [Fraction(x) for x in re.findall(r"-?\d+(?:\.\d+)?", re.search(r"sequence: \\\((.*?)\\\)", q["stem"]).group(1).replace("\\ldots", ""))]
                    gap = n.denominator == 1 and "prime" in w and seq_t[-1] < n < Fraction(q["answer"]["value"]) \
                        and any(n % p == 0 for p in range(2, int(n)))
                    assert gap, ("sequences worked line quotes %s, not from the sequence" % n, qid, w)
        q["worked"] = list(worked)
        MISSING_WORKED[:] = [m for m in MISSING_WORKED if m != ("sequences", q["source"]["ref"])]
    return qs


# --- equation-builder: the forming-equations items as choice ---
EB_BAND = 3


async def eb_questions(h, topic):
    pg = await h.page("equation-builder", "level=ks3")
    items = await pg.evaluate("() => QUESTIONS")
    spec = load_data("worked-lines.json")["equation_builder_ks3"]
    out = []
    for ref, s in spec.items():
        i = int(re.fullmatch(r"QUESTIONS\[(\d+)\]", ref).group(1))
        g = items[i]
        assert g["level"] == "ks3" and g["topic"] == "Forming Equations", ("equation-builder", ref)
        # the answer the game builds from its slots is the answer label, recomputed
        game_eq = " ".join(g["slots"])
        assert same_equation(game_eq, s["answer_label"]), ("equation-builder", ref, game_eq, s["answer_label"])
        labels = [tex(s["answer_label"])] + [tex(w["label"]) for w in s["wrong"]]
        assert len(set(labels)) == 4, ("equation-builder: options not distinct", ref)
        opts, ans = choice("eb-" + ref, labels[0], labels[1:])
        slips = [{"answer": {"val": next(o["val"] for o in opts if o["label"] == tex(w["label"]))}, "line": w["line"]}
                 for w in s["wrong"]]
        stem = s.get("stem_override") or g["text"]
        # every number in the worked lines is one of the question's own
        words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
                 "ten": 10, "eleven": 11, "twelve": 12, "twice": 2, "double": 2, "doubled": 2, "half": 2, "quarter": 4,
                 "third": 3, "fifth": 5, "eighth": 8, "eighths": 8, "thirds": 3, "fifths": 5, "quarters": 4}
        stem_words = {Fraction(words[w]) for w in re.findall(r"[a-z]+", stem.lower()) if w in words}
        own = set(numbers_in(stem)) | stem_words | {n for l in labels for n in numbers_in(l)} | {Fraction(1), Fraction(2)}
        for w in s["worked"]:
            for n in numbers_in(w):
                assert n in own, ("equation-builder worked line quotes %s, not from the question" % n, ref, w)
        out.append(mk(topic, "equation-builder", ref, EB_BAND, False, stem, "choice", ans, options=opts,
                      worked=s["worked"], slip=slips))
    return out


# --- probability-pioneer stage 1: the five words, the answer and the three nearest ---
PROB_WORDS = ["Impossible", "Unlikely", "Even chance", "Likely", "Certain"]


def prob_words(answer, ref):
    a = PROB_WORDS.index(answer)
    others = [w for w in PROB_WORDS if w != answer]
    side = int(sha8("prob", ref), 16) % 2          # a tie between two equally far words is broken by the item's own hash
    others.sort(key=lambda w: (abs(PROB_WORDS.index(w) - a), (PROB_WORDS.index(w) - a) * (1 if side else -1) < 0))
    return [answer] + others[:3]


async def prob_questions(h, topic):
    pg = await h.page("probability-pioneer", "level=year6")
    s1 = await pg.evaluate("() => STAGE1")
    spec = load_data("worked-lines.json")["probability_stage1"]
    assert spec["words"] == PROB_WORDS
    out = []
    for ref, s in spec["items"].items():
        i = int(re.fullmatch(r"STAGE1\[(\d+)\]", ref).group(1))
        g = s1[i]
        game_word = g["label"].split(":")[0].strip()      # the game adds its reason after a colon
        assert game_word.lower() == s["answer_label"].lower(), ("probability: the game labels it %s, not %s" % (game_word, s["answer_label"]), ref)
        words = prob_words(s["answer_label"], ref)
        assert len(set(words)) == 4
        opts, ans = choice("prob-" + ref, words[0], words[1:])
        out.append(mk(topic, "probability-pioneer", ref, 1, False,
                      "Which word best describes how likely this is? " + g["event"] + ".", "choice", ans, options=opts,
                      worked=s["worked"]))
    return out


# --- authored questions: schema, distinct options, and a recomputation per topic ---
def half_up(x, places):
    from decimal import Decimal, ROUND_HALF_UP
    return Decimal(x).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)


def check_rounding(q):
    import sympy
    from decimal import Decimal, ROUND_HALF_UP
    stem = q["stem"]
    m = re.search(r"\\\((.*?)\\\)", stem)
    if m:                                                      # a calculator expression
        x = Decimal(str(sympy.N(tex_to_sympy(m.group(1)), 40)))
    else:
        x = Decimal(re.match(r"Round ([\d ]+(?:\.\d+)?)", stem).group(1).replace(" ", ""))
    near = re.search(r"to the nearest (\d+)", stem)
    whole = "to the nearest whole number" in stem
    dpm = re.search(r"to (\d+) decimal place", stem)
    sfm = re.search(r"to (\d+) significant figure", stem)
    if near or whole:
        n = int(near.group(1)) if near else 1
        want = (x / n).quantize(Decimal(1), rounding=ROUND_HALF_UP) * n
        want_dp = None
    elif dpm:
        want_dp = int(dpm.group(1))
        want = half_up(x, want_dp)
    else:
        sf = int(sfm.group(1))
        places = sf - 1 - x.adjusted()                         # x.adjusted() is the power of ten of the first digit
        if places >= 0:
            want = half_up(x, places)
        else:
            unit = Decimal(10) ** (-places)
            want = (x / unit).quantize(Decimal(1), rounding=ROUND_HALF_UP) * unit
        want_dp = places if places > 0 else None
    f = []
    a = q["answer"]
    if Decimal(str(a["value"])) != want:
        f.append("rounding: the answer is %s, round-half-up gives %s" % (a["value"], want))
    if (a.get("dp") or None) != want_dp:
        f.append("rounding: dp is %r, the stem gives %r" % (a.get("dp"), want_dp))
    for s in q["slip"]:
        if want_dp is not None and Decimal(str(s["answer"]["value"])) != want and \
                half_up(Decimal(str(s["answer"]["value"])), want_dp) == want:
            f.append("a slip (%s) would only get the format message under dp" % s["answer"]["value"])
    return f


def parse_vec(s):
    m = re.findall(r"\\mathbf\{(\w)\} = \\begin\{pmatrix\} (-?\d+) \\\\ (-?\d+) \\end\{pmatrix\}", s)
    return {k: (int(x), int(y)) for k, x, y in m}


def label_vec(lbl):
    m = re.fullmatch(r"\\\(\\begin\{pmatrix\} (-?\d+) \\\\ (-?\d+) \\end\{pmatrix\}\\\)", lbl)
    return (int(m.group(1)), int(m.group(2)))


def check_vectors(q):
    stem = q["stem"]
    v = parse_vec(stem)
    sign = {"right": 1, "left": -1, "up": 1, "down": -1}
    if v:
        expr = re.search(r"\\\((.*)\\\)", stem.split("Work out")[1]).group(1)
        e = re.sub(r"(\d+)\\mathbf\{(\w)\}", r"\1*\\mathbf{\2}", expr)
        e = re.sub(r"\\mathbf\{(\w)\}", lambda m: "v" + m.group(1), e)
        want = tuple(eval(e, {"__builtins__": {}}, {"v" + n: p[k] for n, p in v.items()}) for k in (0, 1))
    else:
        m = re.search(r"moved (\d+) squares? (right|left|up|down) and (\d+) squares? (right|left|up|down)", stem)
        pos = {"right": 0, "left": 0, "up": 1, "down": 1}
        comp = [0, 0]
        comp[pos[m.group(2)]] = int(m.group(1)) * sign[m.group(2)]
        comp[pos[m.group(4)]] = int(m.group(3)) * sign[m.group(4)]
        want = tuple(comp)
    key = next(o for o in q["options"] if o["val"] == q["answer"]["val"])
    f = []
    if label_vec(key["label"]) != want:
        f.append("vectors: the key is %s, recomputed %s" % (label_vec(key["label"]), want))
    for o in q["options"]:
        if o["val"] != q["answer"]["val"] and label_vec(o["label"]) == want:
            f.append("vectors: another option also equals the answer")
    return f


def check_change_subject(q):
    import sympy
    m = re.search(r"Make \\\((\w)\\\) the subject of \\\((.*)\\\)", q["stem"])
    var, eq = m.group(1), m.group(2)
    left, right = eq.split("=")
    sol = sympy.solve(sympy.Eq(tex_to_sympy(left), tex_to_sympy(right)), sympy.Symbol(var))
    assert len(sol) == 1, ("change-subject", eq, sol)
    f = []
    for o in q["options"]:
        ol = re.fullmatch(r"\\\((\w) = (.*)\\\)", o["label"])
        same = bool(ol) and ol.group(1) == var and sympy.simplify(tex_to_sympy(ol.group(2)) - sol[0]) == 0
        if o["val"] == q["answer"]["val"] and not same:
            f.append("change-subject: the key %s is not %s" % (o["label"], sol[0]))
        if o["val"] != q["answer"]["val"] and same:
            f.append("change-subject: option %s also equals the answer" % o["val"])
    return f


def authored_for(topic):
    """The authored questions of a topic, each checked; a fault stops the build."""
    data = load_data("authored.json")
    out = []
    for q in data["questions"]:
        if q["topic"] != topic:
            continue
        faults = validate(q)
        if q["id"] != "%s-%s" % (topic, sha8(q["source"]["game"], q["source"]["ref"])):
            faults.append("id is not topic-hash of its source")
        if q["source"]["game"] != "authored":
            faults.append("source.game is not authored")
        if q["format"] == "choice":
            for s in q["slip"]:
                if s["answer"] == q["answer"] or s["answer"].get("val") not in list("abcd"):
                    faults.append("a slip names the key or no option")
        if q["format"] == "number" and "dp" in q["answer"] and not (isinstance(q["answer"]["dp"], int) and q["answer"]["dp"] >= 0):
            faults.append("dp is not a whole number")
        if topic == "rounding":
            faults += check_rounding(q)
        elif topic == "vectors":
            faults += check_vectors(q)
        elif topic == "change-subject":
            faults += check_change_subject(q)
        if faults:
            raise AssertionError("authored %s: %s" % (q["id"], "; ".join(faults)))
        if not q["worked"]:
            MISSING_WORKED.append((topic, q["source"]["ref"]))
        out.append(q)
    return out


async def topic_sequences_full(h):
    return apply_sequence_lines(await topic_sequences(h))


async def topic_form_expressions(h):
    return await eb_questions(h, "form-expressions") + authored_for("form-expressions")


# ───────────────────────────── the games' own items for the four topics under 30 ─────────────────────────────
# probability-pioneer stages 2 and 3, decimal-detective, formula-unlocked, component-crusher (25 Oct 2026). Authored
# questions (data/six-ps/authored.json) are merged after them. Each answer is recomputed from its own stem.

from decimal import Decimal  # noqa: E402


# --- probability-pioneer stage 2: P(...) as a fraction ---
def _is_prime(n):
    return n > 1 and all(n % p for p in range(2, n))


def _is_square(n):
    return int(math.isqrt(n)) ** 2 == n


def prob2_answer(inner):
    """The probability a stage-2 'P(...)' names, worked out from the words, as (favourable, possible) outcomes,
    not yet simplified."""
    m = re.fullmatch(r"rolling a (\d) on a fair die", inner)
    if m:
        return (1 if 1 <= int(m.group(1)) <= 6 else 0, 6)
    die = {"rolling less than 3 on a die": lambda n: n < 3, "rolling greater than 4 on a dice": lambda n: n > 4,
           "odd on a die": lambda n: n % 2 == 1, "multiple of 3 on a die": lambda n: n % 3 == 0,
           "prime on a die": _is_prime, "square number on a die": _is_square,
           "rolling 1 or 2 on a fair die": lambda n: n in (1, 2)}
    if inner in die:
        return (sum(1 for n in range(1, 7) if die[inner](n)), 6)
    if inner == "flipping tails on a fair coin":
        return (1, 2)
    if inner == "heads twice in a row with a fair coin":
        return (1, 4)                                  # HH out of HH, HT, TH, TT
    if inner == "heart from 52 cards":
        return (13, 52)                       # one suit of four, thirteen cards
    m = re.fullmatch(r"(?:picking )?(\w+) from ((?:\d+ \w+(?:, )?)+)", inner)
    if m:
        counts = {c: int(n) for n, c in re.findall(r"(\d+) (\w+)", m.group(2))}
        return (counts[m.group(1)], sum(counts.values()))
    m = re.fullmatch(r"(vowel|consonant) from ([A-Z](?:, [A-Z])*)", inner)
    if m:
        letters = m.group(2).split(", ")
        return (sum(1 for c in letters if (c in "AEIOU") == (m.group(1) == "vowel")), len(letters))
    if inner == "picture card (J, Q or K) from a pack of 52":
        return (len("JQK") * 4, 52)
    m = re.fullmatch(r"even from (\d+)\u2013(\d+)", inner)
    if m:
        nums = range(int(m.group(1)), int(m.group(2)) + 1)
        return (sum(1 for n in nums if n % 2 == 0), len(nums))
    m = re.fullmatch(r"letter in ([A-Z]+) also in ([A-Z]+)", inner)
    if m:
        return (len(set(m.group(1)) & set(m.group(2))), len(m.group(1)))
    raise AssertionError("probability stage 2: no rule for %r" % inner)


async def prob2_questions(h, topic):
    pg = await h.page("probability-pioneer", "level=year6")
    items = await pg.evaluate("() => STAGE2")
    out = []
    for i, g in enumerate(items):
        inner = re.fullmatch(r"P\((.*)\)", g["q"]).group(1)
        k, tot = prob2_answer(inner)
        n, d = (int(x) for x in g["answer"].split("/"))
        assert Fraction(n, d) == Fraction(k, tot) and math.gcd(n, d) == 1, ("probability stage 2", g["q"], g["answer"], k, tot)
        stem = "Work out " + tex("P(\\text{%s})" % inner) + ". Give your answer as a fraction."
        # Project Claude's template (25 Oct): "There are k <outcome> out of n equally likely outcomes, so P = k/n", then
        # "= simplified" when it simplifies
        eq = "P = \\frac{%d}{%d}" % (k, tot) + (" = \\frac{%d}{%d}" % (n, d) if (k, tot) != (n, d) else "")
        worked = ["There %s %d favourable %s out of %d equally likely outcomes, so %s." %
                  ("is" if k == 1 else "are", k, "outcome" if k == 1 else "outcomes", tot, tex(eq))]
        out.append(mk(topic, "probability-pioneer", "STAGE2[%d]" % i, 2, False, stem, "fraction", {"n": n, "d": d},
                      accept={"rule": "equivalent"}, worked=worked))
    return out


# --- probability-pioneer stage 3: the true statements, asked as "which of these statements is true" ---
async def prob3_questions(h, topic):
    """Each of the game's true statements is the key of one question (never asked as "which is false"). The three wrong
    options are false statements of the game's own, picked by the key's hash; the worked line is the game's explanation
    of the key and each wrong option's slip is the game's explanation of why that statement is false. False statements
    are used only as wrong options. Nothing is written here."""
    pg = await h.page("probability-pioneer", "level=year6")
    items = await pg.evaluate("() => STAGE3")
    clean = lambda e: re.sub(r"^Correct\.\s*", "", strip_html(e))
    falses = [j for j, t in enumerate(items) if not t["answer"]]
    out = []
    for i, g in enumerate(items):
        if not g["answer"]:
            continue
        picks = shuffled(falses, "prob3-%d" % i)[:3]
        assert len(picks) == 3
        labels = [g["statement"]] + [items[j]["statement"] for j in picks]
        opts, ans = choice("prob3-%d" % i, labels[0], labels[1:])
        slips = [{"answer": {"val": next(o["val"] for o in opts if o["label"] == items[j]["statement"])},
                  "line": clean(items[j]["explanation"])} for j in picks]
        out.append(mk(topic, "probability-pioneer", "STAGE3[%d]" % i, 3, False,
                      "Which of these statements is true?", "choice", ans, options=opts,
                      worked=split_working(clean(g["explanation"])), slip=slips))
    # the numbers the statements and explanations quote (the rest are statements of principle, the game's own truth values)
    assert Fraction(1) - Fraction(3, 10) == Fraction(7, 10) and Fraction(7, 6) > 1
    return out


async def topic_probability(h):
    return (await prob_questions(h, "basic-probability") + await prob2_questions(h, "basic-probability")
            + await prob3_questions(h, "basic-probability"))


# --- rounding: decimal-detective's rounding items, typed (the game's four choices are not shown) ---
ROUND_FORMS = {"Round to the nearest whole number": ("to the nearest whole number", 1),
               "Round to the nearest tenth": ("to 1 decimal place", 2),
               "Round to 2 decimal places": ("to 2 decimal places", 2),
               "Round to 1 significant figure": ("to 1 significant figure", 3)}


def round_worked(value, form, answer):
    """Project Claude's ROUNDING template (25 Oct): the digit after the place, then up or down."""
    x = Decimal(value)
    quantum = {"to the nearest whole number": 0, "to 1 decimal place": -1, "to 2 decimal places": -2}.get(form)
    if quantum is None:                                 # 1 significant figure: the place of the first digit
        assert form == "to 1 significant figure"
        quantum = abs(x).adjusted()
    digit = int(abs(x) / Decimal(10) ** (quantum - 1)) % 10
    up = digit >= 5
    return ["Look at the digit after the place you are rounding to: %s." % tex(str(digit)),
            "%s is %s, so round %s: %s." % (tex(str(digit)), "5 or more" if up else "less than 5", "up" if up else "down", tex(answer))]


async def topic_rounding(h):
    pg = await h.page("decimal-detective", "level=year6")
    items = await pg.evaluate("() => ROUNDUP_QUESTIONS")
    out = []
    for i, it in enumerate(items):
        form, band = ROUND_FORMS[it["instruction"]]
        stem = "Round %s %s." % (it["value"], form)
        a = {"value": numval(Decimal(it["answer"]))}
        q = mk("rounding", "decimal-detective", "ROUNDUP_QUESTIONS[%d]" % i, band, False, stem, "number", a,
               worked=round_worked(it["value"], form, it["answer"]))
        dp = re.search(r"to (\d) decimal place", stem)
        if dp:
            a["dp"] = int(dp.group(1))
        elif "significant" in stem:
            x = Decimal(it["value"])
            places = 1 - 1 - x.adjusted()
            if places > 0:
                a["dp"] = places
        faults = check_rounding(q)                      # round-half-up from the stem, and dp from the stem
        assert not faults, ("rounding", it, faults)
        assert Decimal(str(a["value"])) == Decimal(it["answer"]), ("rounding: the game's answer", it)
        out.append(q)
    return out + authored_for("rounding")


# --- vectors: component-crusher's gcse scenarios, written out from the same numbers ---
class Vec:
    def __init__(self, x, y):
        self.x, self.y = Fraction(x), Fraction(y)

    def __add__(self, o):
        return Vec(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return Vec(self.x - o.x, self.y - o.y)

    def __neg__(self):
        return Vec(-self.x, -self.y)

    def __mul__(self, k):
        return Vec(self.x * k, self.y * k)

    __rmul__ = __mul__

    def __pos__(self):
        return self

    def __eq__(self, o):
        return isinstance(o, Vec) and (self.x, self.y) == (o.x, o.y)

    def __hash__(self):
        return hash((self.x, self.y))


def col(v):
    return "\\(\\begin{pmatrix} %s \\\\ %s \\end{pmatrix}\\)" % (tnum(v.x), tnum(v.y))


def col_in(v):
    return "\\begin{pmatrix} %s \\\\ %s \\end{pmatrix}" % (tnum(v.x), tnum(v.y))


def pt(p):
    return "\\((%s, %s)\\)" % (tnum(p[0]), tnum(p[1]))


def scenario_names(sc):
    """The vectors and points a scenario draws, by the names its prompts use."""
    vecs, pts = {}, {p["l"]: tuple(p["c"]) for p in sc.get("points", [])}
    for v in sc["vectors"]:
        d = Vec(v["to"][0] - v["from"][0], v["to"][1] - v["from"][1])
        for name in v["label"].split("="):
            if name and not name.startswith("-"):
                vecs[name] = d
    return vecs, pts


def vec_value(name, vecs, pts):
    if name in vecs:
        return vecs[name]
    if len(name) == 2 and name[0] in pts and name[1] in pts:
        return Vec(pts[name[1]][0] - pts[name[0]][0], pts[name[1]][1] - pts[name[0]][1])
    raise AssertionError("component-crusher: no vector %s" % name)


def expr_python(tx):
    """A prompt's TeX expression as Python over the names v_<name>."""
    e = re.sub(r"\\frac\{(\d+)\}\{(\d+)\}", r"Fraction(\1,\2)", tx)
    e = re.sub(r"\\mathbf\{(\w)\}", r"v_\1", e)
    e = re.sub(r"\\overrightarrow\{(\w+)\}", r"v_\1", e)
    return re.sub(r"(\d|\))(?=v_)", r"\1*", e)


def eval_vec(py, vecs, pts):
    names = {"v_" + n for n in re.findall(r"v_(\w+)", py)}
    env = {n: vec_value(n[2:], vecs, pts) for n in names}
    env["Fraction"] = Fraction
    return eval(py, {"__builtins__": {}}, env)


def vec_wrongs(py, key, vecs, pts):
    """Three wrong column vectors: the expression with its + and - exchanged, the components swapped, then a sign
    flipped (the next flip standing in when two coincide or one equals the key). All four are checked distinct."""
    cands = []
    swapped_ops = py.replace("+", "\u0000").replace("-", "+").replace("\u0000", "-")
    if swapped_ops != py:
        cands.append(eval_vec(swapped_ops, vecs, pts))
    cands += [Vec(key.y, key.x), Vec(-key.x, key.y), Vec(key.x, -key.y), -key, Vec(-key.y, key.x), Vec(key.y, -key.x),
              Vec(key.x + 1, key.y), Vec(key.x, key.y + 1)]
    wrong = []
    for c in cands:
        if c != key and c not in wrong and len(wrong) < 3:
            wrong.append(c)
    assert len(wrong) == 3 and len({(v.x, v.y) for v in wrong + [key]}) == 4
    return wrong


def vec_preamble(prompt, sc, vecs, pts):
    """What the written question must say that the picture showed: the vectors or points its prompt uses."""
    names = list(dict.fromkeys(re.findall(r"\\mathbf\{(\w)\}", prompt)))
    plist = list(dict.fromkeys(l for pair in re.findall(r"\\overrightarrow\{(\w+)\}", prompt) for l in pair if l in pts))
    if not names and not plist and pts and "collinear" in prompt:
        plist = [l for l in pts if l != "O"]
    out = []
    if names:
        bits = ["\\(\\mathbf{%s} = %s\\)" % (n, col_in(vecs[n])) for n in names]
        out.append(" and ".join(bits) + ".")
    if plist:
        bits = ["%s is the point %s" % (l, pt(pts[l])) for l in plist]
        out.append((", ".join(bits[:-1]) + " and " + bits[-1] if len(bits) > 1 else bits[0]) + ".")
    return " ".join(out)


def vec_band(prompt, is_mcq, is_mag):
    tx = re.search(r"\\\((.*?)\\\)", prompt)
    py = expr_python(tx.group(1)) if tx else ""
    tokens = len(re.findall(r"v_", py))
    coef = bool(re.search(r"\d\*v_|\)\*v_", py))
    return 4 if is_mcq or is_mag or tokens >= 3 or (tokens >= 2 and coef) else 3


def brk(x):
    return "(%s)" % tnum(x) if x < 0 else tnum(x)


def coef_tex(k):
    k = Fraction(k)
    return tnum(k) if k.denominator == 1 else "\\frac{%d}{%d}" % (k.numerator, k.denominator)


def vec_terms(py):
    """'2*v_a-v_b' as [(coefficient, name)]: the signed coefficient of each vector the expression uses."""
    py = py.replace(" ", "")
    terms = re.findall(r"([+-]?)(?:(Fraction\(\d+,\d+\)|\d+)\*)?v_(\w+)", py)
    assert "".join((s + (c + "*" if c else "") + "v_" + n) for s, c, n in terms) == py, ("vector expression", py)
    return [((-1 if s == "-" else 1) * (eval(c, {"Fraction": Fraction}) if c else Fraction(1)), n) for s, c, n in terms]


def vec_worked(label, py, key, vecs, pts):
    """One line per row, as the authored items: the template Project Claude gave for component-crusher's items. Every
    number in every line is computed here and the last line's column is the key."""
    terms = vec_terms(py)
    assert len(terms) <= 2, ("vector worked: more than two terms", py)
    vs = [(k, vec_value(n, vecs, pts)) for k, n in terms]
    rows = (("top", lambda v: v.x), ("bottom", lambda v: v.y))
    last = "So " + tex("%s = %s" % (label, col_in(key))) + "."
    if len(vs) == 1:
        k, v = vs[0]
        lines = []
        for r, get in rows:
            lines.append("Multiply the %s number by %s: %s." % (r, tex(coef_tex(k)), tex("%s \\times %s = %s" % (brk(k) if k.denominator == 1 else coef_tex(k), brk(get(v)), tnum(k * get(v))))))
        return lines + [last]
    (k1, v1), (k2, v2) = vs
    assert k1 > 0, ("vector worked: a leading minus on two terms", py)
    plain = k1 == 1 and abs(k2) == 1
    minus = k2 < 0
    ans = {"top": key.x, "bottom": key.y}
    if plain:
        verb = "Take away" if minus else "Add"
        lines = []
        for r, get in rows:
            a, b = get(v1), get(v2)
            res = a - b if minus else a + b
            assert res == ans[r]
            lines.append("%s the %s numbers: %s." % (verb, r, tex("%s %s %s = %s" % (brk(a), "-" if minus else "+", brk(b), tnum(res)))))
        return lines + [last]
    # a multiple on one or both vectors: the multiples first, then the rows together
    first = " and ".join(tex("%s = %s" % (nm, col_in(v))) for nm, v in
                         [(("%s\\mathbf{%s}" % ("" if abs(k) == 1 else coef_tex(abs(k)), n)), abs(k) * vec_value(n, vecs, pts))
                          for k, n in terms])
    lines = [first + "."]
    rowtxt = []
    for r, get in rows:
        a, b = k1 * get(v1), abs(k2) * get(v2)
        res = a - b if minus else a + b
        assert res == ans[r]
        rowtxt.append("%s %s" % (r, tex("%s %s %s = %s" % (brk(a), "-" if minus else "+", brk(b), tnum(res)))))
    lines.append("%s: %s, %s." % ("Take away" if minus else "Add them", rowtxt[0], rowtxt[1]))
    return lines + [last]


def vec_move_worked(start, end, key, what):
    """The two numbers of a move from one point to another, one line each, and the column."""
    dx, dy = Fraction(end[0]) - Fraction(start[0]), Fraction(end[1]) - Fraction(start[1])
    assert (dx, dy) == (key.x, key.y)
    return ["Take the start away from the end. Top number: %s." % tex("%s - %s = %s" % (brk(Fraction(end[0])), brk(Fraction(start[0])), tnum(dx))),
            "Bottom number: %s." % tex("%s - %s = %s" % (brk(Fraction(end[1])), brk(Fraction(start[1])), tnum(dy))),
            "So %s is %s." % (what, tex(col_in(key)))]


async def topic_vectors(h):
    """Foundation only (Project Claude, 25 Oct): component-crusher's column-vector items, adding, taking away, multiplying
    by a number and writing a translation. Magnitudes, the midpoint, collinearity and the reasoning items are above
    Foundation and are left out. Worked lines follow the VECTORS template."""
    pg = await h.page("component-crusher", "level=gcse")
    scenarios = await pg.evaluate("() => SCENARIOS.gcse")
    out = []
    for si, sc in enumerate(scenarios):
        vecs, pts = scenario_names(sc)
        for qi, sq in enumerate(sc["sqs"]):
            ref = "SCENARIOS.gcse[%d].sqs[%d]" % (si, qi)
            prompt = sq["prompt"]
            if sq["type"] != "vec2" or "(M is midpoint)" in prompt or prompt.startswith("State the position of M"):
                continue
            first = re.search(r"\\\((.*?)\\\)", prompt)
            if prompt.startswith("Write down vector"):                       # G1: a, read from the origin
                v = vec_value("a", vecs, pts)
                src = sc["vectors"][0]
                assert src["from"] == [0, 0] and [v.x, v.y] == [Fraction(x) for x in sq["answers"]]
                stem = "The vector \\(\\mathbf{a}\\) goes from the origin to the point %s. Write down \\(\\mathbf{a}\\) as a column vector." \
                       % pt(src["to"])
                key, py = v, "v_a"
                worked = vec_move_worked((0, 0), src["to"], key, tex("\\mathbf{a}"))
            elif sc["id"] == "G6":                                            # a translation, said as two points
                a, b = sc["vectors"][0]["from"], sc["vectors"][0]["to"]
                if qi == 0:
                    key = Vec(b[0] - a[0], b[1] - a[1])
                    stem = "A translation takes the point %s to the point %s. Write down the column vector of the translation." % (pt(a), pt(b))
                    worked = vec_move_worked(a, b, key, "the translation")
                else:
                    key = Vec(a[0] - b[0], a[1] - b[1])
                    stem = "A translation takes the point %s to the point %s. What translation takes %s back to %s?" % (pt(a), pt(b), pt(b), pt(a))
                    worked = vec_move_worked(b, a, key, "the translation back")
                py = None
            else:
                tx = first.group(1).lstrip("= ").strip()
                assert not (tx.startswith("|") and tx.endswith("|")), ("magnitude", ref)
                py = expr_python(tx)
                if py.count("v_") > 2:                                        # a path of three terms: above Foundation
                    continue
                pre = vec_preamble(prompt, sc, vecs, pts)
                stem = (pre + " " + prompt).strip()
                key = eval_vec(py, vecs, pts)
                if re.fullmatch(r"v_[A-Z]{2}", py):                          # AB from two points
                    worked = vec_move_worked(pts[py[2]], pts[py[3]], key, tex("\\overrightarrow{%s}" % py[2:]))
                else:
                    worked = vec_worked(tx, py, key, vecs, pts)
            assert sq["type"] == "vec2" and [key.x, key.y] == [Fraction(str(x)) for x in sq["answers"]], \
                ("vector answer", ref, key.x, key.y, sq["answers"])
            wrongs = vec_wrongs(py, key, vecs, pts) if py else vec_wrongs("v_t", key, {"t": key}, {})
            opts, ans = choice("cc-" + ref, col(key), [col(w) for w in wrongs])
            band = vec_band(prompt, False, False) if py and sc["id"] != "G6" else 3
            out.append(mk("vectors", "component-crusher", ref, band, False, stem, "choice", ans, options=opts, worked=worked))
    return out + authored_for("vectors")


def k_first_positive(terms):
    return terms[0][0] > 0


# --- change-subject: formula-unlocked's gcse set (29), choice ---
def fu_tex(s):
    return s.replace("\\dfrac", "\\frac")


def subject_holds(formula, target, label):
    """The option '<target> = <expression>' makes the formula an identity (every letter taken positive, so a square root
    is the positive one)."""
    import sympy
    left, right = formula.split("=", 1)
    opt = re.fullmatch(r"\s*(.+?)\s*=\s*(.+)", label)
    assert opt and opt.group(1).strip() == target.strip(), ("change-subject: option is not for the target", label)
    sub = {tex_to_sympy(target, True): tex_to_sympy(opt.group(2), True)}
    return sympy.simplify(tex_to_sympy(left, True).subs(sub) - tex_to_sympy(right, True).subs(sub)) == 0


def conv_subject(i, it):
    f, tgt = fu_tex(it["formula"]), it["target"]
    correct, wrong = fu_tex(it["correct"]), [fu_tex(x) for x in it["d"]]
    assert subject_holds(f, tgt, correct), ("change-subject: the key does not rearrange the formula", i)
    assert tex_to_sympy(tgt) not in tex_to_sympy(correct.split("=", 1)[1]).free_symbols, ("key still has the target", i)
    for w in wrong:
        assert not subject_holds(f, tgt, w), ("change-subject: a wrong option also rearranges the formula", i, w)
    assert fu_tex(it["steps"][-1]) == correct, ("change-subject: the last step is not the key", i)
    labels = [tex(correct)] + [tex(w) for w in wrong]
    opts, ans = choice("subject-%d" % i, labels[0], labels[1:])
    return mk("change-subject", "formula-unlocked", "Q_GCSE[%d]" % i, 4 if it["stage"] <= 2 else 5, False,
              "Make %s the subject of %s." % (tex(tgt), tex(f)), "choice", ans, options=opts,
              worked=[tex(fu_tex(s)) for s in it["steps"]])


async def topic_change_subject(h):
    pg = await h.page("formula-unlocked", "level=gcse")
    items = await pg.evaluate("() => Q_GCSE")
    authored = authored_for("change-subject")
    asked = {q["stem"] for q in authored}
    # a game item that asks what an authored question already asks is left out (the authored one carries the slips):
    # Q_GCSE[10], "Make t the subject of v = u + at"
    game = [q for q in (conv_subject(i, it) for i, it in enumerate(items)) if q["stem"] not in asked]
    return game + authored


# --- number-vocabulary: factor-race's own numbers, asked as "how many factors does n have" ---
async def topic_number_vocabulary(h):
    """The game asks which of two numbers has more factors and has no written solution. Every number that appears in its
    pairs (VALID_PAIRS) or its Year 6 bank is asked once as "How many factors does n have?" (a typed number, Project
    Claude's ruling of 25 Oct); the factors come from the game's own getFactors and are recomputed here. Band by size
    (to 20, to 40, above), the topic's band range being 1 to 3."""
    pg = await h.page("factor-race", "level=ks3")
    nums = await pg.evaluate("() => [...new Set([...VALID_PAIRS.flat(), ...YEAR6_BANK.flatMap(q => [q.a, q.b])])].sort((x, y) => x - y)")
    out = []
    for n in nums:
        facs = await pg.evaluate("(n) => getFactors(n)", n)
        want = [d for d in range(1, n + 1) if n % d == 0]
        assert facs == want, ("factor-race getFactors", n, facs, want)
        line = "The factors of %d are %s: that is %d factors." % (n, ", ".join(str(d) for d in want), len(want))
        out.append(mk("number-vocabulary", "factor-race", "number:%d" % n, 1 if n <= 20 else 2 if n <= 40 else 3, False,
                      "How many factors does %d have?" % n, "number", {"value": len(want)}, worked=[line]))
    return out


# --- fraction-operations: how-many-parts' Foundation stage 3 (add or take away, different bottom numbers) ---
HMP_STAGE3_JS = r"""() => {
  const pool = HMP.fpool('stage3'), out = [];
  for (let i = 0; i < pool.length; i++) {
    let s = i * 2654435761 + 12345;
    const rng = () => { s |= 0; s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
    const q = HMP.makeQuestion(pool[i], 'c', rng);
    out.push({a: q.a, b: q.b, op: q.op, c: q.c, d: q.d, keyVal: q.keyVal, keyTex: q.keyTex, sumTex: q.sumTex,
      choices: q.choices.map(c => ({val: c.val, tex: c.tex, err: c.err, name: HMP.ERR[c.err].name(q)})),
      steps: HMP.steps(q).map(s => s.text)});
  }
  return out;
}"""


def frac_of(s):
    return Fraction(s)                                  # "5/6", or "1" for a whole number


def frac_err_value(err, a, b, op, c, d):
    """The value the game's named error gives, worked out here from the error's own words."""
    sg = 1 if op == "+" else -1
    L = b * d // math.gcd(b, d)
    if err == "TB":                                     # added or took away the tops and the bottoms
        return Fraction(a + sg * c, b + sg * d)
    if err == "MD":                                     # multiplied the bottoms, added the tops as they were
        return Fraction(a + c, b * d)
    if err == "DN":                                     # changed the bottom (to the common one) but not the top
        return Fraction(a + sg * c, L)
    if err == "OP":                                     # took away instead of adding, or the reverse
        return Fraction(abs(a * (L // b) - sg * c * (L // d)), L)
    raise AssertionError("fraction-operations: no rule for the error %s" % err)


async def topic_fraction_operations(h):
    """Stage 3 of how-many-parts, a choice: the game's own key and three of its named errors (the game picks them with
    its seeded pickErrors), each wrong option's slip being the game's name for that error, the worked lines being
    HMP.steps. The key and every error are recomputed here. 60, spread evenly between adding and taking away."""
    pg = await h.page("how-many-parts", "level=ks3")
    items = await pg.evaluate(HMP_STAGE3_JS)
    out = []
    for i, it in enumerate(items):
        a, b, c, d, op = it["a"], it["b"], it["c"], it["d"], it["op"]
        key = Fraction(a, b) + Fraction(c, d) if op == "+" else Fraction(a, b) - Fraction(c, d)
        assert frac_of(it["keyVal"]) == key, ("fraction-operations key", it)
        if len(it["choices"]) < 3:                      # the game shows these with two wrong answers: no four options
            continue
        assert len(it["choices"]) == 3 and all(frac_of(x["val"]) != key for x in it["choices"]), ("fraction-operations options", it)
        assert len({x["val"] for x in it["choices"]}) == 3, ("fraction-operations options repeat", it)
        for x in it["choices"]:
            assert frac_of(x["val"]) == frac_err_value(x["err"], a, b, op, c, d), ("fraction-operations error", it, x)
        stem = "Work out %s." % tex("\\frac{%d}{%d} %s \\frac{%d}{%d}" % (a, b, "+" if op == "+" else "-", c, d))
        labels = [tex(it["keyTex"].replace("\\dfrac", "\\frac"))] + [tex(x["tex"].replace("\\dfrac", "\\frac")) for x in it["choices"]]
        opts, ans = choice("hmp-%d" % i, labels[0], labels[1:])
        slips = [{"answer": {"val": next(o["val"] for o in opts if o["label"] == tex(x["tex"].replace("\\dfrac", "\\frac")))},
                  "line": x["name"] + "."} for x in it["choices"]]
        worked = [maths(s).replace("\\dfrac", "\\frac") for s in it["steps"]]
        out.append((op, mk("fraction-operations", "how-many-parts", "fpool:stage3:%d" % i, 2 if op == "+" else 3, False,
                           stem, "choice", ans, options=opts, worked=worked, slip=slips)))
    return [q for _, q in spread(out, GEN_TOPIC, lambda x: x[0])]


# --- averages: distinctly-average's Foundation (ks3) pool, a choice with the game's own named wrong answers ---
DA_JS = r"""() => DA_ITEMS.ks3.map((x, i) => ({x: x, prompt: DA_PROMPTS.ks3[i], expl: explainHTML(x),
  slips: x.distractors.map(d => MC[d.misconception])}))"""
DA_BAND = {"range": 1, "modeUnique": 1, "mean": 2, "modeBimodal": 2}


def da_key(cat, data):
    """The right answer as the game writes it, worked out from the data."""
    n = len(data)
    s = sorted(data)
    counts = {v: data.count(v) for v in set(data)}
    top = max(counts.values())
    modes = sorted(v for v, c in counts.items() if c == top)
    if cat == "mean":
        return Fraction(sum(data), n)
    if cat == "median":
        return Fraction(s[n // 2]) if n % 2 else Fraction(s[n // 2 - 1] + s[n // 2], 2)
    if cat == "range":
        return Fraction(s[-1] - s[0])
    if cat == "modeUnique":
        assert len(modes) == 1, ("distinctly-average: a unique mode has ties", data)
        return Fraction(modes[0])
    if cat == "modeBimodal":
        assert len(modes) == 2, ("distinctly-average: a bimodal set needs two modes", data)
        return modes
    raise AssertionError("distinctly-average: no rule for " + cat)


def da_text(v):
    """A value as the game writes it ('2', '2.5', '1 and 3')."""
    if isinstance(v, list):
        return " and ".join(str(x) for x in v)
    return tnum(v)


def da_slip_ok(cat, mis, val, data):
    """Does the distractor's value fit the misconception the game names for it? (None: no rule here.)"""
    n, s = len(data), sorted(data)
    counts = {v: data.count(v) for v in set(data)}
    mean = Fraction(sum(data), n)
    f = lambda t: Fraction(t) if re.fullmatch(r"-?\d+(\.\d+)?", t) else None
    v = f(val)
    if mis == "sum_not_divided":
        return v == sum(data)
    if mis == "value_not_mean":
        return v is not None and v in data
    if mis == "position_not_value":
        return v == Fraction(n + 1, 2) or v == Fraction(n, 2) or v == Fraction(n + 1, 2) - Fraction(1, 2)
    if mis == "unsorted_median":                        # the middle of the list as it was given
        mid = Fraction(data[n // 2]) if n % 2 else Fraction(data[n // 2 - 1] + data[n // 2], 2)
        return v == mid
    if mis == "mean_not_median" or mis == "mean_not_range":
        return v is not None and abs(v - mean) < Fraction(1, 10)
    if mis == "range_as_max":
        return v == s[-1]
    if mis == "range_as_min":
        return v == s[0]
    if mis == "mode_as_frequency":
        return v == max(counts.values())
    if mis == "wrong_value_picked":
        return v is not None and v in data
    if mis == "only_one_mode":
        return v is not None and counts.get(int(v), 0) == max(counts.values())
    if mis == "mode_and_wrong_value":
        return " and " in val
    return None


async def topic_averages(h):
    """Foundation (ks3) of distinctly-average: the game's key and its three named wrong answers as four options, the
    game's explanation as the worked lines, and the game's one-line reading of each wrong answer as its slip. The key is
    recomputed from the data and every named wrong answer is checked against the misconception it is named for. A pool
    built at load, so 60, spread evenly between the five kinds (the median split by odd and even)."""
    pg = await h.page("distinctly-average", "level=ks3")
    items = await pg.evaluate(DA_JS)
    out = []
    for i, it in enumerate(items):
        x = it["x"]
        cat, data = x["cat"], x["data"]
        want = da_key(cat, data)
        assert da_text(want) == x["correct"], ("distinctly-average key", x["id"], x["correct"], want)
        vals = [x["correct"]] + [d["val"] for d in x["distractors"]]
        assert len(set(vals)) == 4, ("distinctly-average: options repeat or equal the key", x["id"], vals)
        for d in x["distractors"]:
            ok = da_slip_ok(cat, d["misconception"], d["val"], data)
            assert ok is not False, ("distinctly-average: the wrong answer does not fit its misconception", x["id"], d)
        prompt = strip_html(it["prompt"])
        stem = "Here is a data set: %s. %s" % (", ".join(str(v) for v in data), prompt)
        opts, ans = choice("da-%d" % i, vals[0], vals[1:])
        slips = [{"answer": {"val": next(o["val"] for o in opts if o["label"] == d["val"])}, "line": line}
                 for d, line in zip(x["distractors"], it["slips"])]
        worked = [strip_html(p) for p in re.findall(r"<p>(.*?)</p>", it["expl"])]
        band = DA_BAND.get(cat) or (2 if x["parity"] == "odd" else 3)
        out.append(((cat, x.get("parity")), mk("averages", "distinctly-average", "DA_ITEMS.ks3[%d]" % i, band, False, stem,
                                               "choice", ans, options=opts, worked=worked, slip=slips)))
    return [q for _, q in spread(out, GEN_TOPIC, lambda t: t[0])]


# --- area and perimeter: take-a-walk's shapes, drawn as one shared SVG from the game's own geometry ---
TAW_JS = r"""(args) => {
  const P = TAW.pools(), out = [];
  args.stages.forEach(st => P[st].forEach((q, i) => { if (q.ask !== args.ask) return;
    out.push({stage: st, i: i, fam: q.fam, text: q.text, thing: q.thing, key: q.key, unit: q.unit, dp: q.dp, shape: q.shape,
      errors: q.errors, lines: q.errors.map(e => TAW.LINES[e.id][0]),
      steps: TAW.steps(q).map(s => ({text: s.text, last: !!s.last})), svg: TAW.draw(q, {})});
  }));
  return out;
}"""
TAW_BAND = {"sq": 1, "rect": 1}


def taw_svg(it):
    """The game's own drawing of the shape as a self-contained SVG: the outline, the dashed lines and the labels, in
    currentColor with the styling the game puts in its stylesheet written as attributes."""
    s = it["svg"]
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    shape = re.search(r'<path class="shape" d="([^"]+)"', s).group(1)
    parts = ['<path d="%s" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>' % shape]
    for cls in ("join", "dim"):
        for m in re.finditer(r'<line class="%s[^"]*"[^>]*?x1="([^"]+)" y1="([^"]+)" x2="([^"]+)" y2="([^"]+)"' % cls, s):
            parts.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 4"/>' % m.groups())
    texts = []
    for m in re.finditer(r'<text class="lab[^"]*" text-anchor="(\w+)"[^>]*? x="([^"]+)" y="([^"]+)">([^<]*)</text>', s):
        texts.append('<text x="%s" y="%s" text-anchor="%s">%s</text>' % (m.group(2), m.group(3), m.group(1), m.group(4)))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" fill="none" stroke="currentColor">%s'
            '<g fill="currentColor" stroke="none" font-family="sans-serif" font-size="13">%s</g></svg>'
            % (vb, "".join(parts), "".join(texts)))


def taw_labels(svg):
    return sorted(re.findall(r"<text[^>]*>([^<]*)</text>", svg))


def taw_check(it):
    """The key recomputed from the shape's own corners (shoelace for the area, the sides for the perimeter) and every
    labelled side checked against its length."""
    sh = it["shape"]
    pts = []
    for p in sh["path"]:
        assert p["t"] == "L", ("take-a-walk: a curved side in a Foundation shape", it["stage"], it["fam"])
        pts.append((Fraction(p["a"][0]), Fraction(p["a"][1])))
        if p["lab"] is not None:
            ln = math.hypot(p["b"][0] - p["a"][0], p["b"][1] - p["a"][1])
            assert abs(ln - p["lab"]) < 1e-9, ("take-a-walk: a label is not its side's length", it["fam"], p)
    ends = [(Fraction(p["b"][0]), Fraction(p["b"][1])) for p in sh["path"]]
    assert ends[:-1] == pts[1:] and ends[-1] == pts[0], ("take-a-walk: the sides do not close", it["fam"])
    area = abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]))) / 2
    per = sum(math.hypot(p["b"][0] - p["a"][0], p["b"][1] - p["a"][1]) for p in sh["path"])
    return area if it["unit"] == "m2" else per


def taw_worked(steps):
    lines = [maths(s["text"]) for s in steps if not s["last"]]
    if len(lines) > 5:                                  # the parts' lines (Rectangle: ..., Triangle: ...) as one
        merged, run = [], []
        for ln in lines + [""]:
            if re.match(r"(Rectangle|Triangle):", ln):
                run.append(ln)
                continue
            if run:
                merged.append(" ".join(run))
                run = []
            if ln:
                merged.append(ln)
        lines = merged
    assert len(lines) <= 5, ("take-a-walk: more than five worked lines", lines)
    return lines


async def taw_questions(h, topic, ask, stages):
    pg = await h.page("take-a-walk", "level=ks3")
    items = await pg.evaluate(TAW_JS, {"ask": ask, "stages": stages})
    out = []
    for n, it in enumerate(items):
        want = taw_check(it)
        assert abs(want - it["key"]) < 1e-9 and it["dp"] == 0 and float(it["key"]).is_integer(), \
            ("take-a-walk key", it["stage"], it["fam"], it["key"], want)
        svg = taw_svg(it)
        sh = it["shape"]
        want_labels = sorted([("%s m" % p["lab"]) for p in sh["path"] if p["lab"] is not None]
                             + [("%s m" % d["val"]) for d in sh["dims"] if d["val"] is not None])
        assert taw_labels(svg) == want_labels, ("take-a-walk: labels", it["stage"], it["fam"], taw_labels(svg), want_labels)
        rect = all(p["a"][0] == p["b"][0] or p["a"][1] == p["b"][1] for p in sh["path"])
        stem = "The diagram shows the %s, drawn to scale. %s%s%s" % (
            it["thing"], "All the corners are right angles. " if rect else "",
            "The dashed line is the perpendicular height. " if sh["dims"] else "", it["text"])
        slips, seen = [], {int(it["key"])}
        for e, line in zip(it["errors"], it["lines"]):
            v = round(e["v"], 6)
            v = int(v) if float(v).is_integer() else v
            if v in seen:
                continue
            seen.add(v)
            slips.append({"answer": {"value": v}, "line": line})
        band = 1 if it["stage"] == "stage-1" and it["fam"] in TAW_BAND else 2 if it["stage"] == "stage-1" else 3 if it["stage"] == "stage-2" else 4
        q = mk(topic, "take-a-walk", "TAW.pools()[%s][%d]" % (it["stage"], it["i"]), band, False, stem, "number",
               {"value": int(it["key"])}, unit="m²" if it["unit"] == "m2" else "m",
               worked=taw_worked(it["steps"]), slip=slips)
        q["diagram"] = svg
        out.append(((it["stage"], it["fam"]), q))
    return [q for _, q in spread(out, GEN_TOPIC, lambda t: t[0])]


async def topic_area(h):
    return await taw_questions(h, "area", "A", ["stage-1", "stage-2", "stage-3"])


async def topic_perimeter(h):
    return await taw_questions(h, "perimeter", "P", ["stage-1"])


# ───────────────────────────── the registry ─────────────────────────────
# topic id -> (builder, rule notes). Topics not here have no bank yet (coming soon).
BUILDERS = {
    "ratio": topic_ratio,
    "direct-proportion": topic_direct,
    "powers-roots": topic_powers,
    "compound-measures": topic_compound,
    "linear-equations": topic_linear,
    "sequences": topic_sequences_full,
    "angles": topic_angles,
    "arithmetic-negatives": topic_negatives,
    "fdp-convert": topic_fdp_convert,
    "fraction-percentage-of-amount": topic_fdp_amount,
    "form-expressions": topic_form_expressions,
    "basic-probability": topic_probability,
    "rounding": topic_rounding,
    "vectors": topic_vectors,
    "change-subject": topic_change_subject,
    "number-vocabulary": topic_number_vocabulary,
    "fraction-operations": topic_fraction_operations,
    "averages": topic_averages,
    "area": topic_area,
    "perimeter": topic_perimeter,
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
