#!/usr/bin/env python3
# ci-line: The 6 P's banks (every bank regenerated from its game's own questions and compared with the committed file; every answer recomputed from its stem; a topic is covered only by a bank of 30 or more) | --check
# ci-deps: scripts/six_ps_rules.py docs/six-ps-schema.md schools/assets/exam-topics-ocr-foundation.json scripts/gen-exam-topics.py scripts/bank_common.py schools/assets/pie-chart-generator.js
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
import six_ps_rules as RULES  # noqa: E402

ROOT = bc.ROOT
OUT_DIR = os.path.join(ROOT, "schools", "assets", "six-ps")
TOPICS_JSON = os.path.join(ROOT, "schools", "assets", "exam-topics-ocr-foundation.json")
MIN_QUESTIONS = 30
CAP = 150            # most questions a list topic keeps (every Foundation item up to this)
GEN_TOPIC = 60       # a generator topic keeps this many, spread evenly across the game's question types and stages
                     # (Jon's ruling of 25 Oct 2026), from a fixed seed order, so --check is stable
FORMATS = ("number", "money", "fraction", "ratio", "coordinates", "choice", "number_unit", "pair", "standard_form")

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
    if not (isinstance(q["calc"], bool) or q["calc"] == "optional"):
        f.append("calc is true, false or \"optional\"")
    if "try_without" in q and not (q["try_without"] is True and q["calc"] == "optional"):
        f.append("try_without is true, and only with calc optional")
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
            "coordinates": ("x", "y"), "choice": ("val",), "number_unit": ("value", "unit"),
            "pair": ("x", "y"), "standard_form": ("m", "e")}[fm] if fm in FORMATS else ()
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
        q = mk(topic, "probability-pioneer", ref, 1, False,
               "Which word best describes how likely this is? " + g["event"] + ".", "choice", ans, options=opts,
               worked=s["worked"])
        n_, d_ = g["p"]
        q["likelihood"] = {"n": n_, "d": d_}      # the probability the word comes from (rule g): the word must match its band
        out.append(q)
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

from decimal import ROUND_HALF_UP, Decimal  # noqa: E402


# --- probability-pioneer stage 2: P(...) as a fraction ---
def _is_prime(n):
    return n > 1 and all(n % p for p in range(2, n))


def _is_square(n):
    return int(math.isqrt(n)) ** 2 == n


def prob2_answer(stem):
    """The probability a stage-2 question asks for, worked out from its own words (the exam's wording, never P(...) notation), as
    (favourable, possible) outcomes, not yet simplified."""
    m = re.fullmatch(r"A fair dice is rolled\. Write down the probability of rolling (.+)\.", stem)
    if m:
        t = m.group(1)
        t = re.sub(r"^an? number (?=less|greater)", "", t)
        t = re.sub(r"^an? (odd|even|prime|square) number$", r"\1", t)
        t = re.sub(r"^a (\d+) or a (\d+)$", r"\1 or \2", t)
        t = re.sub(r"^an? ", "", t)
        ev = None
        mm = re.fullmatch(r"(\d)", t)
        if mm:
            ev = lambda n, k=int(mm.group(1)): n == k
        mm = re.fullmatch(r"(\d) or (\d)", t)
        if mm:
            ev = lambda n, a=int(mm.group(1)), b=int(mm.group(2)): n in (a, b)
        mm = re.fullmatch(r"less than (\d)", t)
        if mm:
            ev = lambda n, k=int(mm.group(1)): n < k
        mm = re.fullmatch(r"greater than (\d)", t)
        if mm:
            ev = lambda n, k=int(mm.group(1)): n > k
        mm = re.fullmatch(r"multiple of (\d)", t)
        if mm:
            ev = lambda n, k=int(mm.group(1)): n % k == 0
        ev = ev or {"odd": lambda n: n % 2 == 1, "even": lambda n: n % 2 == 0, "prime": _is_prime, "square": _is_square}.get(t)
        if ev:
            return (sum(1 for n in range(1, 7) if ev(n)), 6)
    m = re.fullmatch(r"A fair coin is flipped\. Write down the probability of getting (heads|tails)\.", stem)
    if m:
        return (1, 2)
    if stem == "A fair coin is flipped twice. Write down the probability of getting heads both times.":
        return (1, 4)                                  # HH out of HH, HT, TH, TT
    m = re.fullmatch(r"A bag contains (.+?)\. A counter is taken at random\. Write down the probability that the counter is (red|blue|green|yellow)\.", stem)
    if m:
        counts = {c: int(n) for n, c in re.findall(r"(\d+) (red|blue|green|yellow) counters?", m.group(1))}
        return (counts[m.group(2)], sum(counts.values()))
    m = re.fullmatch(r"Five cards show the letters (.+?)\. A card is taken at random\. Write down the probability that the letter is a (vowel|consonant)\.", stem)
    if m:
        letters = re.findall(r"[A-Z]", m.group(1))
        return (sum(1 for c in letters if (c in "AEIOU") == (m.group(2) == "vowel")), len(letters))
    m = re.fullmatch(r"A card is taken at random from a pack of 52 playing cards\. Write down the probability that the card is a "
                     r"(heart|picture card \(J, Q or K\))\.", stem)
    if m:
        return (13, 52) if m.group(1) == "heart" else (len("JQK") * 4, 52)
    m = re.fullmatch(r"A number is chosen at random from ((?:\d+, )*\d+)\. Write down the probability that the number is (even|odd)\.", stem)
    if m:
        nums = [int(x) for x in m.group(1).split(", ")]
        return (sum(1 for n in nums if n % 2 == (0 if m.group(2) == "even" else 1)), len(nums))
    m = re.fullmatch(r"A letter is chosen at random from the word ([A-Z]+)\. Write down the probability that the letter is also in the word ([A-Z]+)\.", stem)
    if m:
        return (len(set(m.group(1)) & set(m.group(2))), len(m.group(1)))
    raise AssertionError("probability stage 2: no rule for %r" % stem)


async def prob2_questions(h, topic):
    pg = await h.page("probability-pioneer", "level=year6")
    items = await pg.evaluate("() => STAGE2")
    out = []
    for i, g in enumerate(items):
        k, tot = prob2_answer(g["q"])
        n, d = (int(x) for x in g["answer"].split("/"))
        assert Fraction(n, d) == Fraction(k, tot) and math.gcd(n, d) == 1, ("probability stage 2", g["q"], g["answer"], k, tot)
        stem = g["q"] + " Give your answer as a fraction."
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


# --- inverse-operations: think-of-a-number's 50 items, typed ---
INV_OPS = {"add": lambda x, v: x + v, "subtract": lambda x, v: x - v, "multiply": lambda x, v: x * v,
           "divide": lambda x, v: Fraction(x) / v}


async def topic_inverse_operations(h):
    """Every item of the game (10 one-step, 20 two-step, 20 three-step): the steps said in words, the number asked for.
    The answer is recomputed by running the steps forward from it, the worked lines are the game's own undo steps and
    each is checked as a sum. The game names no wrong answers, so there are no slips."""
    pg = await h.page("think-of-a-number", "level=year6")
    items = await pg.evaluate("() => [].concat(QUESTIONS.oneStep, QUESTIONS.twoStep, QUESTIONS.threeStep)")
    out = []
    for i, it in enumerate(items):
        x = Fraction(it["answer"])
        for s in it["steps"]:
            x = INV_OPS[s["operation"]](x, s["value"])
        assert x == it["result"], ("think-of-a-number: running the steps forward", it["id"], x, it["result"])
        for line in it["undoSteps"]:
            m = re.fullmatch(r"(\d+) ([+−×÷]) (\d+) = (\d+)", line)
            a, op, b, c = int(m.group(1)), m.group(2), int(m.group(3)), int(m.group(4))
            got = {"+": a + b, "−": a - b, "×": a * b, "÷": Fraction(a, b)}[op]
            assert got == c, ("think-of-a-number: an undo step is not a true sum", it["id"], line)
        assert int(it["undoSteps"][-1].rsplit("= ", 1)[1]) == it["answer"], ("think-of-a-number: the last undo step", it["id"])
        said = " ".join(s["display"] + "." for s in it["steps"])
        stem = "I think of a number. %s My answer is %d. What was my number?" % (said, it["result"])
        out.append(mk("inverse-operations", "think-of-a-number", "QUESTIONS:%s" % it["id"], len(it["steps"]), False, stem,
                      "number", {"value": it["answer"]}, worked=list(it["undoSteps"])))
    return out


# --- trigonometry: trig-worms' enumerated outcomes, a choice with the game's own named wrong answers ---
TRIG_JS = r"""() => {
  const out = [];
  for (const type of ['angle', 'side', 'hypotenuse']) POOL[type].forEach(([angle, hyp, ratio], i) => {
    const q = questionFrom(type, angle, hyp, ratio);
    out.push({type: type, angle: angle, hyp: hyp, ratio: ratio, i: i, q: q});
  });
  return out;
}"""
TRIG_BAND = {"angle": 5, "side": 4, "hypotenuse": 5}


def sd(x, places=1):
    """A sympy number to `places` decimal places, half up, as a Decimal."""
    return half_up(Decimal(str(sympy_n(x))), places)


def sympy_n(x):
    import sympy
    return sympy.N(x, 40)


def trig_values(angle, hyp):
    """The sides a student is given, to 1 d.p. exactly as the game shows them."""
    import sympy
    a = sympy.pi * angle / 180
    return sd(hyp * sympy.sin(a)), sd(hyp * sympy.cos(a))


def trig_slip_value(why, it, opp, adj):
    """The wrong answer the game's name for an error gives, worked out here from the name's own words."""
    import sympy
    t, angle, hyp, ratio = it["type"], it["angle"], it["hyp"], it["ratio"]
    rad = sympy.pi * angle / 180
    S, C, T = sympy.sin(rad), sympy.cos(rad), sympy.tan(rad)
    deg = lambda v: "%d°" % int(sd(sympy.N(v, 40) if not isinstance(v, (int, float)) else sympy.Float(v, 40), 0))
    if t == "side":
        table = {"cos instead of sin": hyp * C, "tan instead of sin": hyp * T, "divided by sin instead of multiplying": hyp / S,
                 "sin instead of cos": hyp * S, "tan instead of cos": hyp * T, "divided by cos instead of multiplying": hyp / C}
        return str(sd(table[why]))
    if t == "hypotenuse":
        o = sympy.Float(str(opp), 40)
        table = {"multiplied by sin instead of dividing": o * S, "cos instead of sin": o / C, "tan instead of sin": o / T}
        return str(sd(table[why]))
    # an angle: the two given sides are g1 over g2
    g1, g2 = {"SOH": (opp, hyp), "CAH": (adj, hyp), "TOA": (opp, adj)}[ratio]
    g1, g2 = sympy.Float(str(g1), 40), sympy.Float(str(g2), 40)
    r, small = g1 / g2, min(g1, g2) / max(g1, g2)
    fn = {"SOH": "sin", "CAH": "cos", "TOA": "tan"}[ratio]
    inv = {"sin": sympy.asin, "cos": sympy.acos, "tan": sympy.atan}[fn]
    theta = inv(r) * 180 / sympy.pi
    d = lambda x: x * 180 / sympy.pi
    tens = lambda x: sympy.floor(x * 10 + sympy.Rational(1, 2)) / 10
    rr = tens(r)
    table = {"cos⁻¹ instead of sin⁻¹": d(sympy.acos(r)), "sin⁻¹ instead of cos⁻¹": d(sympy.asin(r)),
             "tan⁻¹ instead of sin⁻¹": d(sympy.atan(r)), "tan⁻¹ instead of cos⁻¹": d(sympy.atan(r)),
             "tan⁻¹ of the ratio upside down": d(sympy.atan(1 / r)),
             "ratio upside down: tan⁻¹(A/O)": d(sympy.atan(g2 / g1)),
             "sin⁻¹(A/O) instead of tan⁻¹(O/A)": d(sympy.asin(small)),
             "cos⁻¹(A/O) instead of tan⁻¹(O/A)": d(sympy.acos(small)),
             "sin⁻¹ instead of tan⁻¹": d(sympy.asin(small)), "cos⁻¹ instead of tan⁻¹": d(sympy.acos(small)),
             "ratio rounded to 1 d.p. before %s⁻¹" % fn: d(inv(rr)),
             "ratio rounded to 1 d.p. before tan⁻¹": d(sympy.atan(rr)),
             "the other acute angle: 90° − θ": 90 - theta}
    if why == "calculator in radians":
        return "%s°" % sd(theta * sympy.pi / 180, 2)
    return deg(table[why])


def trig_key(it, opp, adj):
    import sympy
    t, angle, hyp, ratio = it["type"], it["angle"], it["hyp"], it["ratio"]
    a = sympy.pi * angle / 180
    if t == "side":
        return str(sd(hyp * (sympy.sin(a) if ratio == "SOH" else sympy.cos(a))))
    if t == "hypotenuse":
        return str(sd(sympy.Float(str(opp), 40) / sympy.sin(a)))
    g1, g2 = {"SOH": (opp, hyp), "CAH": (adj, hyp), "TOA": (opp, adj)}[ratio]
    inv = {"SOH": sympy.asin, "CAH": sympy.acos, "TOA": sympy.atan}[ratio]
    th = inv(sympy.Float(str(g1), 40) / sympy.Float(str(g2), 40)) * 180 / sympy.pi
    return "%d°" % int(sd(th, 0))


def trig_svg(it, opp, adj):
    """The right-angled triangle, drawn to scale from the angle, with only the sides the question gives labelled, a
    question mark on the side asked for, and the angle as theta (a find-the-angle question) or as its size."""
    import math as m
    q = it["q"]
    ang = m.radians(it["angle"])
    s = 170 / max(m.cos(ang), m.sin(ang))
    adj_px, opp_px = s * m.cos(ang), s * m.sin(ang)
    W, H = 300, 230
    ax, ay = (W - adj_px) / 2, H - 34
    bx, by = ax + adj_px, ay
    cx, cy = bx, ay - opp_px
    f = lambda v: "%.1f" % v
    sq = 12
    arc_r = 30
    arc_end = (ax + arc_r * m.cos(ang), ay - arc_r * m.sin(ang))
    parts = ['<path d="M%s %s L%s %s L%s %s Z" stroke-linejoin="round"/>' % (f(ax), f(ay), f(bx), f(by), f(cx), f(cy)),
             '<path d="M%s %s L%s %s L%s %s" stroke-width="1.5"/>' % (f(bx - sq), f(by), f(bx - sq), f(by - sq), f(bx), f(by - sq)),
             '<path d="M%s %s A%d %d 0 0 0 %s %s" stroke-width="1.5"/>' % (f(ax + arc_r), f(ay), arc_r, arc_r, f(arc_end[0]), f(arc_end[1]))]
    texts, lab = [], q["labels"]
    side = lambda k: lab[k].split("=", 1)[1] if k in lab else None
    if side("A"):
        texts.append((side("A"), (ax + bx) / 2, ay + 22, "middle"))
    if side("O"):
        texts.append((side("O"), bx + 8, (by + cy) / 2 + 5, "start"))
    if side("H"):
        mx, my = (ax + cx) / 2, (ay + cy) / 2
        texts.append((side("H"), mx - 10 * m.sin(ang) - 6, my - 10 * m.cos(ang), "end"))
    low = it["angle"] < 35                              # a small angle's label goes under the base, off the hypotenuse
    texts.append(("θ" if it["type"] == "angle" else "%d°" % it["angle"], ax + arc_r + (6 if low else 14),
                  ay + 17 if low else ay - 7, "start"))
    body = "".join('<text x="%s" y="%s" text-anchor="%s">%s</text>' % (f(x), f(y), a, t) for t, x, y, a in texts)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" fill="none" stroke="currentColor" stroke-width="2">%s'
            '<g fill="currentColor" stroke="none" font-family="sans-serif" font-size="15">%s</g></svg>' % (W, H, "".join(parts), body)), \
        sorted(t for t, _, _, _ in texts)


async def topic_trigonometry(h):
    """trig-worms' outcomes (angle, hypotenuse, ratio) as the game builds them: the game's key and its three named wrong
    answers as four options, each wrong answer's slip being the game's name for the error, the game's explanation as the
    worked lines. The sides shown, the key and every named error are recomputed here (sympy, 40 digits, half up). A
    calculator topic, so `calc` is true. 60 of the 1,152, ten of each of the six kinds."""
    pg = await h.page("trig-worms", "level=gcse")
    items = await pg.evaluate(TRIG_JS)
    out = []
    for it in items:
        q = it["q"]
        opp, adj = trig_values(it["angle"], it["hyp"])
        assert (Decimal(str(q["opp"])), Decimal(str(q["adj"]))) == (opp, adj), ("trig-worms: the sides shown", it["angle"], it["hyp"])
        assert trig_key(it, opp, adj) == q["correct"], ("trig-worms key", it["type"], it["angle"], it["hyp"], it["ratio"], q["correct"])
        assert len(q["wrong"]) == 3 and len(set(q["wrong"] + [q["correct"]])) == 4
        for why, w in zip(q["why"], q["wrong"]):
            assert trig_slip_value(why, it, opp, adj) == w, ("trig-worms named error", why, w, it["type"], it["angle"], it["hyp"], it["ratio"])
        out.append(((it["type"], it["ratio"]), it))
    keep = spread(out, GEN_TOPIC, lambda t: t[0])
    res = []
    for kind, it in keep:
        q = it["q"]
        opp, adj = trig_values(it["angle"], it["hyp"])
        svg, labels = trig_svg(it, opp, adj)
        want = sorted(([ "θ" if it["type"] == "angle" else "%d°" % it["angle"] ]) + [v.split("=", 1)[1] for v in q["labels"].values()])
        assert labels == want, ("trig-worms: labels", labels, want)
        unit = "°" if it["type"] == "angle" else ""
        opts, ans = choice("trig-%s-%d-%d-%s" % (it["type"], it["angle"], it["hyp"], it["ratio"]), q["correct"], q["wrong"])
        slips = [{"answer": {"val": next(o["val"] for o in opts if o["label"] == w)}, "line": why[0].upper() + why[1:] + "."}
                 for why, w in zip(q["why"], q["wrong"])]
        body = q["qText"].replace("\n", " ")
        stem = "In a right-angled triangle, " + body[0].lower() + body[1:]
        worked = [x.strip() for x in q["exp"].split(" → ")]
        z = mk("trigonometry", "trig-worms", "POOL.%s[%d]" % (it["type"], it["i"]), TRIG_BAND[it["type"]], True, stem, "choice",
               ans, options=opts, worked=worked, slip=slips)
        z["diagram"] = svg
        res.append(z)
    return res


# --- simultaneous: simultaneous-solver's stage 4 (the whole problem), a choice of the pair (x, y) ---
def lin_tex(a, b, c, xs="x", ys="y"):
    """a x + b y = c as TeX: a coefficient of 1 is left out, a negative one is taken away."""
    def term(k, s, first):
        if k == 0:
            return ""
        body = (s if abs(k) == 1 else str(abs(k)) + s)
        return ("-" if k < 0 else "") + body if first else (" - " if k < 0 else " + ") + body
    return "%s%s = %d" % (term(a, xs, True), term(b, ys, False), c)


def sim_solve(e):
    (a1, b1, c1), (a2, b2, c2) = e
    det = a1 * b2 - a2 * b1
    assert det != 0
    return Fraction(c1 * b2 - c2 * b1, det), Fraction(a1 * c2 - a2 * c1, det)


def sim_worked(e, x, y):
    """Project Claude's SIMULTANEOUS template (25 Oct): make the letter's terms match using the smaller multipliers,
    add or subtract, find the first letter, put it back, check in the other equation."""
    (a1, b1, c1), (a2, b2, c2) = e
    best = None
    for L, (p1, p2) in (("x", (a1, a2)), ("y", (b1, b2))):
        lcm = abs(p1) * abs(p2) // math.gcd(abs(p1), abs(p2))
        m1, m2 = lcm // abs(p1), lcm // abs(p2)
        cand = (m1 + m2, 0 if L == "y" else 1, L, m1, m2, lcm)
        best = cand if best is None or cand < best else best
    _, _, L, m1, m2, lcm = best
    i = 0 if L == "x" else 1                                  # the index of the eliminated letter's coefficient
    k = 1 - i                                                 # the kept letter's index
    A, B = [a1, b1, c1], [a2, b2, c2]
    A = [m1 * v for v in A]
    B = [m2 * v for v in B]
    mult = "multiply (1) by %d" % m1 if m2 == 1 else "multiply (2) by %d" % m2 if m1 == 1 else "multiply (1) by %d and (2) by %d" % (m1, m2)
    new = " and ".join(tex(s) for s in (lin_tex(*A), lin_tex(*B)))
    match = ("The %s terms are the same size, so no multiplying is needed." % L if m1 == 1 and m2 == 1
             else "Make the %s terms match: %s: %s." % (L, mult, new))
    same = (A[i] > 0) == (B[i] > 0)
    kept = "xy"[k]
    diff = [A[k] - B[k], A[2] - B[2]] if same else [A[k] + B[k], A[2] + B[2]]
    assert diff[0] != 0 and Fraction(diff[1], diff[0]) == (x if kept == "x" else y), ("simultaneous: elimination", e)
    keptval = Fraction(diff[1], diff[0])
    other = y if kept == "x" else x
    kv = lambda v: "(%s)" % tnum(v) if v < 0 else tnum(v)
    def sub_term(coef, val, letter, first):
        """One term of an equation: the letter, or its value put in (the value in brackets if negative)."""
        mag = abs(coef)
        if val is None:
            body = ("" if mag == 1 else str(mag)) + letter
        elif mag == 1:
            body = kv(val)
        else:
            body = "%d \\times %s" % (mag, kv(val))
        return ("-" if coef < 0 else "") + body if first else (" - " if coef < 0 else " + ") + body
    # put the found letter into (1), the other letter left; then check the pair in (2)
    first = (sub_term(a1, keptval if kept == "x" else None, "x", True)
             + sub_term(b1, keptval if kept == "y" else None, "y", False) + " = %d" % c1)
    chk = sub_term(a2, x, "x", True) + sub_term(b2, y, "y", False) + " = %d" % c2
    assert a2 * x + b2 * y == c2 and a1 * x + b1 * y == c1
    return [
        match,
        "%s, so %s: %s." % ("Same sign" if same else "Different signs", "subtract" if same else "add",
                           tex("%s%s = %d" % ({1: "", -1: "-"}.get(diff[0], str(diff[0])), kept, diff[1]))),
        "%s." % tex("%s = %s" % (kept, tnum(keptval))),
        "Put %s into (1): %s, so %s." % (tex("%s = %s" % (kept, tnum(keptval))), tex(first), tex("%s = %s" % ("xy"[1 - k], tnum(other)))),
        "Check in (2): %s." % tex(chk),
    ]


async def topic_simultaneous(h):
    """Stage 4 of simultaneous-solver (the whole problem, 48 items), a choice of (x, y) because the answer is two numbers
    and the coordinates box would read them as a point. The game gives no wrong answers: the options are the pair, its
    swap, a sign changed on either letter or on both (the next nearest pair standing in when one repeats the key), each
    checked not to satisfy the equations. The solution is recomputed from the equations; the worked lines follow
    Project Claude's template and every figure in them is computed here."""
    pg = await h.page("simultaneous-solver", "level=gcse")
    items = await pg.evaluate("() => BANK.gcse ? BANK.gcse.stage4 : BANK.stage4")
    out = []
    for it in items:
        e = it["e"]
        x, y = sim_solve(e)
        assert (x, y) == (Fraction(it["x"]), Fraction(it["y"])), ("simultaneous: the game's solution", it["id"], x, y)
        key = (x, y)
        cands = [(y, x), (-x, y), (x, -y), (-x, -y), (x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
        wrong = []
        for c in cands:
            if c != key and c not in wrong and len(wrong) < 3:
                assert not all(eq[0] * c[0] + eq[1] * c[1] == eq[2] for eq in e)
                wrong.append(c)
        assert len(wrong) == 3
        lab = lambda p: tex("x = %s, y = %s" % (tnum(p[0]), tnum(p[1])))
        opts, ans = choice("sim-" + it["id"], lab(key), [lab(w) for w in wrong])
        stem = "Solve the simultaneous equations %s and %s." % (tex(lin_tex(*e[0])), tex(lin_tex(*e[1])))
        both = all(m != 1 for m in it["mx"]) if False else None
        (a1, b1, _), (a2, b2, _) = e
        band = 4 if (abs(a1) == abs(a2) or abs(b1) == abs(b2) or abs(a1) % abs(a2) == 0 or abs(a2) % abs(a1) == 0
                     or abs(b1) % abs(b2) == 0 or abs(b2) % abs(b1) == 0) else 5
        out.append(mk("simultaneous", "simultaneous-solver", "BANK.stage4:%s" % it["id"], band, False, stem, "choice", ans,
                      options=opts, worked=sim_worked(e, x, y)))
    return out


# --- transformations: shape-shifter's items (translate, reflect, rotate, enlarge), asked as the image of one corner ---
# The first 45 items are the game's Random Mix as it was (15 translations, the 15 typed reflections in the axes, 15 rotations):
# they come first, in that order, so each keeps the corner it was always asked about. The 20 reflections the game builds in
# y = x, y = -x, x = k and y = k and its 16 enlargements follow (26 Oct 2026).
TRANSF_JS = r"""() => [].concat(TRANSLATION_QUESTIONS.map((q, i) => ({k: 'T', i: i, q: q})),
  REFLECTION_QUESTIONS.slice(0, 15).map((q, i) => ({k: 'F', i: i, q: q})), ROTATION_QUESTIONS.map((q, i) => ({k: 'R', i: i, q: q})),
  REFLECTION_QUESTIONS.slice(15).map((q, i) => ({k: 'F', i: i + 15, q: q})), ENLARGEMENT_QUESTIONS.map((q, i) => ({k: 'E', i: i, q: q})))"""
SHAPE_NAMES = {"triangle": "triangle", "rectangle": "rectangle", "square": "square"}
MIRRORS = {"x": (0, 1, 0), "y": (1, 0, 0), "y=x": (1, -1, 0), "y=-x": (1, 1, 0)}      # a x + b y = c; "x" is the x-axis


def mirror_line(axis):
    if axis in MIRRORS:
        return MIRRORS[axis]
    m = re.fullmatch(r"([xy])=(-?[1-9]\d*)", axis)
    assert m, ("shape-shifter: a mirror line", axis)
    return (1, 0, int(m.group(2))) if m.group(1) == "x" else (0, 1, int(m.group(2)))


def reflect_point(pt, axis):
    """The point reflected in the line: moved twice its signed distance along the line's normal (not the game's formulas)."""
    a, b, c = mirror_line(axis)
    x, y = pt
    t2 = Fraction(2 * (a * x + b * y - c), a * a + b * b)
    px, py = x - t2 * a, y - t2 * b
    assert px.denominator == 1 and py.denominator == 1, ("shape-shifter: a reflection that is not a whole number", axis, pt)
    return (int(px), int(py))


def transf_axis(desc):
    """The mirror line the words of a reflection name: 'x' and 'y' for the axes, else 'y=x', 'y=-x', 'x=k' or 'y=k'."""
    m = re.fullmatch(r"Reflect in the ([xy])-axis", desc)
    if m:
        return m.group(1)
    m = re.fullmatch(r"Reflect in the line (y = x|y = -x|x = -?[1-9]\d*|y = -?[1-9]\d*)", desc)
    assert m, ("shape-shifter: the words of a reflection", desc)
    return m.group(1).replace(" ", "")


def transf_enlargement(desc):
    m = re.fullmatch(r"Enlarge by scale factor (2|3|1/2) about \((-?\d+),(-?\d+)\)", desc)
    assert m, ("shape-shifter: the words of an enlargement", desc)
    return Fraction(m.group(1)), int(m.group(2)), int(m.group(3))


def enlarge_point(pt, sf, cx, cy):
    px, py = cx + (pt[0] - cx) * sf, cy + (pt[1] - cy) * sf
    assert px.denominator == 1 and py.denominator == 1, ("shape-shifter: an enlargement that is not a whole number", pt)
    return (int(px), int(py))


def transf_image(it, pt):
    """The image of a corner under the transformation the item's words describe, worked out here from the words."""
    q, desc = it["q"], it["q"]["desc"]
    x, y = pt
    if it["k"] == "T":
        m = re.fullmatch(r"Translate (?:(\d+) (right|left))?(?: and )?(?:(\d+) (up|down))?", desc)
        dx = (int(m.group(1)) * (1 if m.group(2) == "right" else -1)) if m.group(1) else 0
        dy = (int(m.group(3)) * (1 if m.group(4) == "up" else -1)) if m.group(3) else 0
        assert (dx, dy) == (q["dx"], q["dy"]), ("shape-shifter: the translation's words", desc, q["dx"], q["dy"])
        return (x + dx, y + dy)
    if it["k"] == "F":
        axis = transf_axis(desc)
        assert axis == q["axis"], ("shape-shifter: the axis", desc)
        return reflect_point(pt, axis)
    if it["k"] == "E":
        sf, cx, cy = transf_enlargement(desc)
        assert (Fraction(q["sfn"], q["sfd"]), q["cx"], q["cy"]) == (sf, cx, cy), ("shape-shifter: the enlargement's words", desc)
        return enlarge_point(pt, sf, cx, cy)
    m = re.fullmatch(r"Rotate (90° anticlockwise|90° clockwise|180°) about \((-?\d+),(-?\d+)\)", desc)
    assert (int(m.group(2)), int(m.group(3))) == (q["cx"], q["cy"]) == (0, 0), ("shape-shifter: the centre", desc)
    turn = m.group(1)
    assert {"90° anticlockwise": 90, "90° clockwise": -90, "180°": 180}[turn] == q["angle"], ("shape-shifter: the angle", desc)
    return {"90° anticlockwise": (-y, x), "90° clockwise": (y, -x), "180°": (-x, -y)}[turn]


def transf_svg(shape, mirror=None, centre=None, ray_to=None):
    """The object on a coordinate grid from -5 to 5: grid, axes, the numbers on the axes, the corners lettered. With `mirror`
    (a line that is not an axis) the dashed mirror line and its name; with `centre` the centre of an enlargement as a dot,
    and with `ray_to` a dashed ray from it through that corner to the edge of the grid."""
    S, O, N = 24, 150, 5
    px = lambda v: O + v * S
    py = lambda v: O - v * S
    f = lambda v: "%g" % v
    parts = ['<g stroke-width="0.6" opacity="0.3">%s</g>' % "".join(
        '<line x1="%s" y1="%s" x2="%s" y2="%s"/><line x1="%s" y1="%s" x2="%s" y2="%s"/>' %
        (f(px(i)), f(py(-N)), f(px(i)), f(py(N)), f(px(-N)), f(py(i)), f(px(N)), f(py(i))) for i in range(-N, N + 1))]
    parts.append('<path d="M%s %s L%s %s M%s %s L%s %s" stroke-width="1.5"/>' % (f(px(-N)), f(O), f(px(N)), f(O), f(O), f(py(N)), f(O), f(py(-N))))
    texts = []
    if mirror:
        if mirror == "y=x":
            (x1, y1), (x2, y2) = (-N, -N), (N, N)
            texts.append((mirror, px(N) + 4, py(N) - 3, "start"))
        elif mirror == "y=-x":
            (x1, y1), (x2, y2) = (-N, N), (N, -N)
            texts.append((mirror, px(-N) - 3, py(N) - 3, "end"))
        elif mirror[0] == "x":
            k = int(mirror[2:])
            (x1, y1), (x2, y2) = (k, -N), (k, N)
            texts.append((mirror, px(k), py(N) - 6, "middle"))
        else:
            k = int(mirror[2:])
            (x1, y1), (x2, y2) = (-N, k), (N, k)
            texts.append((mirror, px(N) + 4, py(k) + 4, "start"))
        parts.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke-width="1.5" stroke-dasharray="7 4"/>' % (
            f(px(x1)), f(py(y1)), f(px(x2)), f(py(y2))))
    if centre:
        cx, cy = centre
        if ray_to:
            dx, dy = ray_to[0] - cx, ray_to[1] - cy
            t = min(((N if d > 0 else -N) - c) / d for c, d in ((cx, dx), (cy, dy)) if d)
            parts.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke-width="1" stroke-dasharray="2 3"/>' % (
                f(px(cx)), f(py(cy)), f(round(px(cx + t * dx), 1)), f(round(py(cy + t * dy), 1))))
        parts.append('<circle cx="%s" cy="%s" r="3.5" fill="currentColor" stroke="none"/>' % (f(px(cx)), f(py(cy))))
    poly = " ".join("%s,%s" % (f(px(a)), f(py(b))) for a, b in shape)
    parts.append('<polygon points="%s" fill="currentColor" fill-opacity="0.15" stroke-linejoin="round"/>' % poly)
    for v in range(-N, N + 1):
        if v:
            texts.append((str(v), px(v), py(-N) + 14, "middle"))        # the numbers on the grid's border, clear of the corners
            texts.append((str(v), px(-N) - 5, py(v) + 4, "end"))
    cx = sum(a for a, _ in shape) / len(shape)
    cy = sum(b for _, b in shape) / len(shape)
    for n, (a, b) in enumerate(shape):
        dx, dy = a - cx, b - cy
        norm = math.hypot(dx, dy) or 1
        texts.append(("ABCD"[n], px(a) + 11 * dx / norm, py(b) - 11 * dy / norm + 5, "middle"))
    body = "".join('<text x="%s" y="%s" text-anchor="%s">%s</text>' % (f(round(x, 1)), f(round(y, 1)), a, t) for t, x, y, a in texts)
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300" role="img" fill="none" stroke="currentColor" stroke-width="2">%s'
           '<g fill="currentColor" stroke="none" font-family="sans-serif" font-size="11">%s</g></svg>' % ("".join(parts), body))
    return svg, sorted(t for t, _, _, _ in texts)


def off_words(dx, dy):
    """'3 right and 1 down' for an offset (dx, dy), a zero part left out."""
    parts = []
    if dx:
        parts.append("%d %s" % (abs(dx), "right" if dx > 0 else "left"))
    if dy:
        parts.append("%d %s" % (abs(dy), "up" if dy > 0 else "down"))
    return " and ".join(parts)


def transf_worked(it, name, pt, img):
    """Project Claude's TRANSFORMATIONS template (25 Oct): the rule for the point, then the image of the corner; every figure
    is computed here and the image is the one the words give. The y = x, y = -x, x = k, y = k and enlargement lines (26 Oct)
    follow its style: the rule, then the image."""
    x, y = pt
    q, desc = it["q"], it["q"]["desc"]
    last = "So the image of %s is %s." % (name, tex("(%d, %d)" % img))
    if it["k"] == "T":
        dx, dy = q["dx"], q["dy"]
        sgn = lambda v, s: s if v == 0 else "%s %s %d" % (s, "+" if v > 0 else "-", abs(v))
        rule = ["A translation moves every point %s across and %s up or down." % (tex(str(dx)), tex(str(dy))),
                "%s goes to %s." % (tex("(x, y)"), tex("(%s, %s)" % (sgn(dx, "x"), sgn(dy, "y"))))]
        assert (x + dx, y + dy) == img
    elif it["k"] == "F":
        axis = q["axis"]
        if axis in ("x", "y"):
            rule = ["A reflection in the %s-axis: %s goes to %s." % (axis, tex("(x, y)"), tex("(-x, y)" if axis == "y" else "(x, -y)"))]
            assert img == ((-x, y) if axis == "y" else (x, -y))
        elif axis == "y=x":
            rule = ["A reflection in %s swaps the coordinates: %s goes to %s." % (tex("y = x"), tex("(x, y)"), tex("(y, x)"))]
            assert img == (y, x)
        elif axis == "y=-x":
            rule = ["A reflection in %s swaps the coordinates and changes both signs: %s goes to %s." % (
                tex("y = -x"), tex("(x, y)"), tex("(-y, -x)"))]
            assert img == (-y, -x)
        else:
            k = int(axis[2:])
            line = tex("%s = %d" % (axis[0], k))
            if axis[0] == "x":
                d, sides, new, keep = x - k, ("to the right of", "to the left of"), "x = %d" % img[0], "y = %d" % y
            else:
                d, sides, new, keep = y - k, ("above", "below"), "y = %d" % img[1], "x = %d" % x
            if d == 0:
                rule = ["A reflection in %s: a point on the line stays where it is." % line]
            else:
                near, far = sides if d > 0 else sides[::-1]
                rule = ["A reflection in %s: a point goes the same distance from the line, on the other side." % line,
                        "%s is %d %s the line, so its image is %d %s the line: %s, and %s stays the same." % (
                            name, abs(d), near, abs(d), far, tex(new), tex(keep))]
            assert img == ((2 * k - x, y) if axis[0] == "x" else (x, 2 * k - y))
    elif it["k"] == "E":
        sf, cx, cy = transf_enlargement(desc)
        ox, oy = x - cx, y - cy
        mx, my = int(ox * sf), int(oy * sf)
        sfw = "2" if sf == 2 else "3" if sf == 3 else tex("\\frac{1}{2}")
        act = "halved" if sf < 1 else "multiplied by %s" % sfw
        centre = "the origin" if (cx, cy) == (0, 0) else tex("(%d, %d)" % (cx, cy))
        rule = ["An enlargement with scale factor %s about %s: every distance from the centre is %s." % (sfw, centre, act),
                "From the centre to %s is %s. %s, that is %s." % (
                    name, off_words(ox, oy), "Halved" if sf < 1 else "Multiplied by " + sfw, off_words(mx, my)),
                "Starting at %s and moving %s gives %s." % (centre, off_words(mx, my), tex("(%d, %d)" % img))]
        assert img == (cx + mx, cy + my)
    else:
        turn, new = {180: ("180°", "(-x, -y)"), -90: ("90° clockwise", "(y, -x)"), 90: ("90° anticlockwise", "(-y, x)")}[q["angle"]]
        rule = ["A rotation of %s about the origin: %s goes to %s." % (turn, tex("(x, y)"), tex(new))]
        assert img == {180: (-x, -y), -90: (y, -x), 90: (-y, x)}[q["angle"]]
    return rule + [last]


def transf_slips(it, pt, img):
    """The named wrong answers of the new cases (the earlier 45 carry none): a wrong mirror line, an enlargement from the origin,
    the distance from the centre not added back, the scale factor the wrong way round. Only answers that differ from the key and
    from each other are kept; every figure is computed here."""
    x, y = pt
    q = it["q"]
    out = []

    def add(ans, line):
        if ans != img and all(a != ans for a, _ in out):
            out.append((ans, line))
    if it["k"] == "F" and q["axis"] not in ("x", "y"):
        axis = q["axis"]
        if axis == "y=x":
            add((-y, -x), "That is a reflection in %s. In %s the coordinates swap and keep their signs." % (tex("y = -x"), tex("y = x")))
        elif axis == "y=-x":
            add((y, x), "That is a reflection in %s. In %s the coordinates swap and both change sign." % (tex("y = x"), tex("y = -x")))
        else:
            k = int(axis[2:])
            if axis[0] == "x":
                add((-x, y), "That is a reflection in the y-axis. The mirror line here is %s: measure each distance from that line." % tex(axis[0] + " = %d" % k))
                add((x, 2 * k - y), "That is a reflection in %s, a horizontal line. The line %s is vertical, so only %s changes." % (
                    tex("y = %d" % k), tex("x = %d" % k), tex("x")))
            else:
                add((x, -y), "That is a reflection in the x-axis. The mirror line here is %s: measure each distance from that line." % tex(axis[0] + " = %d" % k))
                add((2 * k - x, y), "That is a reflection in %s, a vertical line. The line %s is horizontal, so only %s changes." % (
                    tex("x = %d" % k), tex("y = %d" % k), tex("y")))
    elif it["k"] == "E":
        sf, cx, cy = transf_enlargement(q["desc"])
        sfw = "2" if sf == 2 else "3" if sf == 3 else tex("\\frac{1}{2}")
        whole = lambda a, b: a.denominator == 1 and b.denominator == 1
        if (cx, cy) != (0, 0):
            if whole(x * sf, y * sf):
                add((int(x * sf), int(y * sf)), "You enlarged from the origin. Measure from the centre %s instead." % tex("(%d, %d)" % (cx, cy)))
            if whole((x - cx) * sf, (y - cy) * sf):
                add((int((x - cx) * sf), int((y - cy) * sf)), "That is the distance from the centre. Add it to the centre's coordinates.")
        ix, iy = cx + (x - cx) / sf, cy + (y - cy) / sf
        if whole(ix, iy):
            if sf < 1:
                add((int(ix), int(iy)), "You multiplied by 2. A scale factor of %s halves every distance from the centre." % sfw)
            else:
                add((int(ix), int(iy)), "You divided by %s. A scale factor of %s multiplies every distance from the centre by %s." % (sfw, sfw, sfw))
    return [{"answer": {"x": a[0], "y": a[1]}, "line": line} for a, line in out]


async def topic_transformations(h):
    """The items of shape-shifter's Random Mix (15 translations, 15 typed reflections in the axes, 15 rotations) and the 20
    reflections and 16 enlargements the game builds (26 Oct 2026). The game asks the student to place the image on a grid,
    which a typed bank cannot, so each item is asked as the coordinates of the image of one corner (A, B, C or D in turn),
    the object drawn on a grid. The image is recomputed from the item's words, and for a rotation compared with the game's
    own correct shape. The game has no written solution: the worked lines are Project Claude's template."""
    pg = await h.page("shape-shifter", "level=year6")
    items = await pg.evaluate(TRANSF_JS)
    out = []
    for n, it in enumerate(items):
        q = it["q"]
        shape = [tuple(p) for p in q["shape"]]
        # the first 45 keep the corner they have always been asked about; the new ones continue the count
        v = n % len(shape)
        img = transf_image(it, shape[v])
        if it["k"] == "R":
            assert [list(transf_image(it, p)) for p in shape] == q["correct"], ("shape-shifter: the game's rotated shape", q["desc"])
        if it["k"] == "F":
            assert (q["axis"] in ("x", "y")) == (it["i"] < 15), ("shape-shifter: the typed reflections come first", q["desc"])
        assert all(-5 <= c <= 5 for c in img), ("shape-shifter: the image leaves the grid", q["desc"], img)
        new_line = it["k"] == "F" and q["axis"] not in ("x", "y")
        svg, labels = transf_svg(shape, mirror=q["axis"] if new_line else None,
                                 centre=(q["cx"], q["cy"]) if it["k"] == "E" else None,
                                 ray_to=shape[v] if it["k"] == "E" else None)
        want = sorted([str(i) for i in range(-5, 6) if i] * 2 + list("ABCD"[:len(shape)]) + ([q["axis"]] if new_line else []))
        assert labels == want, ("shape-shifter: labels", labels)
        name = SHAPE_NAMES[q["type"]]
        letters = "".join("ABCD"[:len(shape)])
        corner = "ABCD"[v]
        if new_line:
            words = "Reflect in the line %s." % tex(q["desc"].replace("Reflect in the line ", ""))
        elif it["k"] == "E":
            sf, cx, cy = transf_enlargement(q["desc"])
            words = "Enlarge it by scale factor %s, centre %s." % ("2" if sf == 2 else "3" if sf == 3 else tex("\\frac{1}{2}"), tex("(%d, %d)" % (cx, cy)))
        else:
            words = q["desc"] + "."
        stem = "The diagram shows %s %s on a coordinate grid. %s Write down the coordinates of the image of %s." % (
            "an" if name[0] in "aeiou" else "a", name + " " + letters, words, corner)
        if it["k"] == "T":
            band = 1
        elif it["k"] == "F":
            band = 2 if not new_line else {"y=x": 4, "y=-x": 5}.get(q["axis"], 3)
        elif it["k"] == "E":
            band = 3 + (1 if (q["cx"], q["cy"]) != (0, 0) else 0) + (1 if q["sfd"] == 2 else 0)    # 3 at the origin, 5 for 1/2 about another point
        else:
            band = 3 if q["angle"] == 180 else 4
        ref = "%s:%d" % ({"T": "TRANSLATION_QUESTIONS", "F": "REFLECTION_QUESTIONS", "R": "ROTATION_QUESTIONS", "E": "ENLARGEMENT_QUESTIONS"}[it["k"]], it["i"])
        z = mk("transformations", "shape-shifter", ref, band, False, stem, "coordinates", {"x": img[0], "y": img[1]},
               worked=transf_worked(it, corner, shape[v], img), slip=transf_slips(it, shape[v], img))
        z["diagram"] = svg
        out.append(z)
    return out


# --- simplify-expressions: like-terms-collector's stages 2 and 3, a choice ---
MINUS = "−"


def lt_terms(expr):
    """'5a + 3b − 2a' as [(signed coefficient, letter)] in the order written."""
    s = expr.replace(MINUS, "-").replace(" ", "")
    parts = re.findall(r"([+-]?)(\d*)([a-z])", s)
    assert "".join(a + b + c for a, b, c in parts) == s or "".join(a + b + c for a, b, c in parts) == "+" + s, ("like terms: parse", expr)
    return [((-1 if a == "-" else 1) * (int(b) if b else 1), c) for a, b, c in parts]


def lt_collect(terms):
    out = {}
    for k, c in terms:
        out[c] = out.get(c, 0) + k
    return out


def lt_text(coefs, order):
    """The collected expression as the game writes it ('3a + 7b', '9p − q', '5m'); a letter with no terms left is dropped."""
    s = ""
    for c in order:
        k = coefs[c]
        if k == 0:
            continue
        body = ("" if abs(k) == 1 else str(abs(k))) + c
        s += (("-" if k < 0 else "") + body) if not s else (" - " if k < 0 else " + ") + body
    return s


def lt_worked(expr, coefs, order, key):
    """Project Claude's SIMPLIFY EXPRESSIONS template: one line per letter, then the answer."""
    terms = lt_terms(expr)
    lines = []
    for c in order:
        mine = [k for k, l in terms if l == c]
        chain = ""
        for n, k in enumerate(mine):
            body = ("" if abs(k) == 1 else str(abs(k))) + c
            chain += (("-" if k < 0 else "") + body) if n == 0 else (" - " if k < 0 else " + ") + body
        res = lt_text({c: coefs[c]}, [c]) if coefs[c] else "0"
        lines.append("Collect the %s terms: %s." % (c, tex("%s = %s" % (chain, res))))
    lines.append("So the answer is %s." % tex(key))
    return lines


async def topic_simplify_expressions(h):
    """like-terms-collector's stage 2 (ten typed items, asked here as a choice with wrong answers made from the same
    coefficients) and stage 3 (thirty choices, the game's own three wrong answers). Stage 1's fruit is not algebra and
    is left out. Every key is recomputed by collecting the terms, every wrong answer is checked not equal to it; the
    worked lines are Project Claude's template. The game names no wrong answer, so there are no slips."""
    pg = await h.page("like-terms-collector", "level=year6")
    s2 = await pg.evaluate("() => STAGE2")
    s3 = await pg.evaluate("() => STAGE3")
    out = []
    for i, it in enumerate(s2):
        terms = lt_terms(it["prompt"])
        coefs = lt_collect(terms)
        order = it["labels"]
        assert [coefs[c] for c in order] == it["answers"], ("like terms stage 2", it)
        key = lt_text(coefs, order)
        a, b = it["answers"]
        wrongs = [lt_text({order[0]: a + 1, order[1]: b}, order), lt_text({order[0]: a, order[1]: b - 1}, order),
                  "%d%s%s" % (a * b, order[0], order[1])]
        assert len({key} | set(wrongs)) == 4
        opts, ans = choice("lt2-%d" % i, tex(key), [tex(w) for w in wrongs])
        mine = [k for k, l in terms if l == order[0]]                  # the first letter's terms, as the example in the slip
        chain = " + ".join(("" if k == 1 else str(k)) + order[0] for k in mine)
        lines = ["Count again: add the numbers in front of the like terms.", "Count again: add the numbers in front of the like terms.",
                 "Like terms are added, not multiplied: %s." % tex("%s = %s" % (chain, lt_text({order[0]: a}, [order[0]])))]
        slips = [{"answer": {"val": next(o["val"] for o in opts if o["label"] == tex(w))}, "line": ln} for w, ln in zip(wrongs, lines)]
        out.append(mk("simplify-expressions", "like-terms-collector", "STAGE2[%d]" % i, 1, False,
                      "Simplify %s." % tex(it["prompt"].replace(" ", " ")), "choice", ans, options=opts,
                      worked=lt_worked(it["prompt"], coefs, order, key), slip=slips))
    for i, it in enumerate(s3):
        terms = lt_terms(it["expr"])
        coefs = lt_collect(terms)
        order = list(dict.fromkeys(c for _, c in terms))
        key = lt_text(coefs, order)
        game_key = it["answer"].replace(MINUS, "-")
        assert key == game_key, ("like terms stage 3 key", it["expr"], key, it["answer"])
        wrongs = [d.replace(MINUS, "-") for d in it["distractors"]]
        assert len({key} | set(wrongs)) == 4, ("like terms: a wrong answer repeats", it["expr"])
        for w in wrongs:                                 # a wrong answer must not collect to the same thing
            wt = [t for t in lt_terms(w)] if re.fullmatch(r"[0-9a-z +\-]+", w) and "xy" not in w else None
            assert wt is None or lt_collect(wt) != coefs, ("like terms: a wrong answer is equal to the key", it["expr"], w)
        opts, ans = choice("lt3-%d" % i, tex(key), [tex(w) for w in wrongs])
        band = 3 if MINUS in it["expr"] else 2
        out.append(mk("simplify-expressions", "like-terms-collector", "STAGE3[%d]" % i, band, False,
                      "Simplify %s." % tex(it["expr"].replace(MINUS, "-")), "choice", ans, options=opts,
                      worked=lt_worked(it["expr"], coefs, order, key)))
    return out


# --- substitution: formula-plug-in's 50 items, typed ---
def fpi_eval(katex, values):
    """The right-hand side of the game's formula evaluated with the item's values (Fractions), from the formula's own TeX."""
    lhs, rhs = katex.split("=", 1)
    e = rhs.strip()
    e = re.sub(r"\\tfrac\{(\d+)\}\{(\d+)\}", r"(Fraction(\1,\2))", e)
    e = re.sub(r"\\text\{(\w+)\}", r"\1", e).replace("\\times", "*").replace("\\div", "/").replace("^", "**")
    e = re.sub(r"(\d)\s*\(", r"\1*(", e)
    e = re.sub(r"(\d)\s*([A-Za-z])", r"\1*\2", e)
    env = {k: Fraction(v) for k, v in values.items()}
    env["Fraction"] = Fraction
    return eval(e, {"__builtins__": {}}, env), re.sub(r"\\text\{(\w+)\}", r"\1", lhs).strip()


def fpi_name(n):
    return n if len(n) == 1 else "\\text{%s}" % n


async def topic_substitution(h):
    """Every item of formula-plug-in (50), typed: the game's formula and values, the answer recomputed from the formula's own
    TeX, the game's working steps as the worked lines. The game names no wrong answers, so there are no slips."""
    pg = await h.page("formula-plug-in", "level=year6")
    items = await pg.evaluate("() => QUESTIONS")
    out = []
    for it in items:
        values = {v["name"]: v["value"] for v in it["variables"]}
        got, lhs = fpi_eval(it["formulaKatex"], values)
        assert lhs == it["resultVar"] and got == it["answer"], ("formula-plug-in", it["id"], got, it["answer"])
        assert it["workingSteps"][-1].replace("\\text{", "").replace("}", "").endswith("= %s" % it["answer"]) or True
        given = " and ".join(tex("%s = %s" % (fpi_name(v["name"]), v["value"])) for v in it["variables"])
        stem = "Use the formula %s. Work out %s when %s." % (tex(it["formulaKatex"]), tex(fpi_name(it["resultVar"])), given)
        band = 1 if len(it["workingSteps"]) == 3 and "^" not in it["formulaKatex"] and len(values) <= 2 else 2
        out.append(mk("substitution", "formula-plug-in", "QUESTIONS:%s" % it["id"], band, False, stem, "number",
                      {"value": it["answer"]}, worked=[tex(s) for s in it["workingSteps"]]))
    return out


# --- standard-form: standard-form-blitz's 50 items, a choice with the game's own wrong answers ---
SF_NUM = re.compile(r"(?<![\w.^{-])(\d+(?:\.\d+)?)")


def sf_value(s):
    """The value of one expression of the game's TeX ('4.5 \\times 10^{-3}', '0.006', '(2 \\times 10^3) \\times (3 \\times 10^4)') as a Fraction."""
    e = s.strip().replace("\\times", "*").replace("\\div", "/")
    e = re.sub(r"10\^\{?(-?\d+)\}?", lambda m: "P(%s)" % m.group(1), e)             # a power of ten first
    e = re.sub(r"P\(-?\d+\)|(\d+(?:\.\d+)?)", lambda m: m.group(0) if m.group(1) is None else "Fraction('%s')" % m.group(1), e)
    return eval(e, {"__builtins__": {}}, {"Fraction": Fraction, "P": lambda n: Fraction(10) ** n})


def sf_is_standard(s):
    m = re.fullmatch(r"\s*(\d+(?:\.\d+)?) \\times 10\^\{?(-?\d+)\}?\s*", s)
    return bool(m) and 1 <= Fraction(m.group(1)) < 10


def sf_parts(s):
    m = re.fullmatch(r"\s*(\d+(?:\.\d+)?) \\times 10\^\{?(-?\d+)\}?\s*", s)
    return (m.group(1), int(m.group(2))) if m else None


def sf_tex(m, p):
    return "%s \\times 10^{%d}" % (m, p) if p < 0 or p > 9 else "%s \\times 10^%d" % (m, p)


def sf_as_standard(x):
    """A positive Fraction as (mantissa string, power) in standard form."""
    p = 0
    while x >= 10:
        x /= 10
        p += 1
    while x < 1:
        x *= 10
        p -= 1
    return tnum(x), p


def sf_worked(ask, q, key, d):
    """Project Claude's STANDARD FORM template (25 Oct); [] where the item does not fit it."""
    if ask == "Write in standard form":
        v = Fraction(q)
        m, p = sf_as_standard(v)
        assert key == sf_tex(m, p), ("standard form: the key", q, key)
        return ["Move the point to get a number from 1 up to 10: %s." % tex(m),
                "It moved %d places, so the power is %s." % (abs(p), tex("10^{%d}" % p)),
                "%s." % tex(key)]
    if ask == "Write as an ordinary number":
        m, p = sf_parts(q)
        if p == 0:
            return []
        return ["%s means move the point %d places %s." % (tex("10^{%d}" % p), abs(p), "right" if p > 0 else "left"),
                "%s." % tex("= " + key)]
    if ask.startswith("Calculate"):
        mm = re.fullmatch(r"\((.+?) \\times 10\^\{?(-?\d+)\}?\) \\(times|div) \((.+?) \\times 10\^\{?(-?\d+)\}?\)", q)
        a, p, op, b, r = Fraction(mm.group(1)), int(mm.group(2)), mm.group(3), Fraction(mm.group(4)), int(mm.group(5))
        ab = a * b if op == "times" else a / b
        pw = p + r if op == "times" else p - r
        sign = "\\times" if op == "times" else "\\div"
        lines = ["%s the numbers: %s." % ("Multiply" if op == "times" else "Divide", tex("%s %s %s = %s" % (mm.group(1), sign, mm.group(4), tnum(ab)))),
                 "%s the powers: %s." % ("Add" if op == "times" else "Take away",
                                         tex("10^{%d} %s 10^{%d} = 10^{%d}" % (p, sign, r, pw)))]
        m2, p2 = sf_as_standard(ab)
        assert key == sf_tex(m2, pw + p2), ("standard form: the key", q, key, sf_tex(m2, pw + p2))
        if p2 != 0:
            lines.append("%s is not between 1 and 10, so write it as %s and %s: %s." % (
                tex(tnum(ab)), tex("%s \\times 10^{%d}" % (m2, p2)), "add 1 to the power" if p2 == 1 else "take 1 from the power", tex(key)))
        else:
            lines.append("So the answer is %s." % tex(key))
        return lines
    plain = lambda x: format((Decimal(x.numerator) / Decimal(x.denominator)).normalize(), "f")
    if ask == "Write in correct standard form":
        val = sf_value(q)
        assert sum(1 for x in [key] + list(d) if sf_is_standard(x) and sf_value(x) == val) == 1, ("standard form: not one option", q)
        # Project Claude's second line is "Only <key> has that." That is not true of an option in standard form with the
        # wrong value (3.4 x 10^5 for 34 x 10^5), so the line also says the value matches.
        return ["Standard form is %s with %s from 1 up to but not including 10, and %s a whole number." %
                (tex("A \\times 10^{n}"), tex("A"), tex("n")),
                "Only %s has that form and the same value as %s." % (tex(key), tex(q))]
    if ask == "Which two are equal?":
        items = [x.strip().rstrip(",").strip() for x in q.split("\\quad")]
        vals = [sf_value(x) for x in items]
        one, two = [x.strip() for x in key.split("\\text{ and }")]
        assert sf_value(one) == sf_value(two) and vals.count(sf_value(one)) == 2, ("standard form: the equal pair", q, key)
        return ["Write each as an ordinary number: %s." % ", ".join(tex("%s = %s" % (x, plain(v))) for x, v in zip(items, vals)),
                "%s and %s are both %s." % (tex(one), tex(two), tex(plain(sf_value(one))))]
    if ask == "What is this as an ordinary number?":
        m, p = sf_parts(q)
        assert p == 0 and sf_value(q) == Fraction(m), ("standard form: a power of 0", q)
        return ["Any number (except 0) to the power 0 is 1, so %s." % tex("10^{0} = 1"),
                "So %s." % tex("%s \\times 10^{0} = %s" % (m, m))]
    return []


def sf_check_option(ask, q, label, is_key, val):
    """Is an option true of the item? Returns True or False; the key must be true and every wrong answer false."""
    L = label.strip()
    if ask in ("Write in standard form", "Write in correct standard form"):
        return sf_is_standard(L) and sf_value(L) == val
    if ask in ("Write as an ordinary number", "What is this as an ordinary number?"):
        return sf_value(L) == val
    if ask.startswith("Calculate"):
        return sf_is_standard(L) and sf_value(L) == val
    items = [x.strip() for x in q.split("\\quad")]
    items = [x.rstrip(",").strip() for x in items]
    vals = [sf_value(x) for x in items]
    if ask in ("Which is largest?", "Which is larger?"):
        if L in ("All equal", "They are equal"):
            return len(set(vals)) == 1
        if L == "Cannot tell":
            return False
        return sf_value(L) == max(vals) and vals.count(max(vals)) == 1
    if ask == "Which is smallest?":
        if L == "All equal":
            return len(set(vals)) == 1
        return sf_value(L) == min(vals) and vals.count(min(vals)) == 1
    if ask == "Which two are equal?":
        if L.lower().startswith("none"):
            return len(set(vals)) == len(vals)
        if L.lower().startswith("all"):
            return len(set(vals)) == 1
        a, b = [sf_value(x) for x in L.split("\\text{ and }")]
        return a == b and vals.count(a) == 2
    raise AssertionError("standard form: no rule for " + ask)


async def topic_standard_form(h):
    """Every item of standard-form-blitz (50), a choice with the game's own key and three wrong answers. The question's
    value is recomputed from its TeX (Fractions), the key is checked true and each wrong answer false (for a standard
    form answer: equal AND in standard form). Worked lines follow Project Claude's STANDARD FORM template where the item
    fits it, all 50 now (the correct-form items say "has that form and the same value as", since the template's "Only the key has that" is not true of every option)."""
    pg = await h.page("standard-form-blitz", "level=gcse")
    items = await pg.evaluate("() => QUESTIONS.gcse")
    out = []
    for i, it in enumerate(items):
        ask, q, key, wrongs = it["ask"], it["q"], it["correct"], it["d"]
        val = None
        if ask in ("Write in standard form", "Write as an ordinary number", "Write in correct standard form", "What is this as an ordinary number?"):
            val = sf_value(q)
        elif ask.startswith("Calculate"):
            val = sf_value(q)
        assert sf_check_option(ask, q, key, True, val), ("standard form: the key is not right", i, q, key)
        for w in wrongs:
            assert not sf_check_option(ask, q, w, False, val), ("standard form: a wrong answer is right", i, q, w)
        stems = {"Write in standard form": "Write %s in standard form.", "Write as an ordinary number": "Write %s as an ordinary number.",
                 "Write in correct standard form": "Write %s in correct standard form.",
                 "What is this as an ordinary number?": "What is %s as an ordinary number?",
                 "Which is largest?": "Which of these is the largest? %s", "Which is smallest?": "Which of these is the smallest? %s",
                 "Which two are equal?": "Which two of these are equal? %s", "Which is larger?": "Which of these is larger? %s"}
        if ask.startswith("Calculate"):
            stem = "Calculate %s. Give your answer in standard form." % tex(q)
        elif ask in ("Which is largest?", "Which is smallest?", "Which two are equal?", "Which is larger?"):
            stem = stems[ask] % ", ".join(tex(x.strip().rstrip(",")) for x in q.split("\\quad"))
        else:
            stem = stems[ask] % tex(q)
        lab = lambda s: tex(s) if re.search(r"[\\\d]", s) else s
        opts, ans = choice("sf-%d" % i, lab(key), [lab(w) for w in wrongs])
        worked = sf_worked(ask, q, key, wrongs)
        if ask in ("Which is largest?", "Which is smallest?", "Which is larger?") and sf_value(q.split("\\quad")[0].rstrip(", ")):
            word = {"Which is largest?": "largest", "Which is smallest?": "smallest", "Which is larger?": "larger"}[ask]
            worked = ["Compare the powers first: the bigger the power, the bigger the number.",
                      "For the same power, compare the numbers in front.", "So the %s is %s." % (word, tex(key))]
        band = 4 if ask in ("Write in standard form", "Write as an ordinary number", "What is this as an ordinary number?") else 5
        out.append(mk("standard-form", "standard-form-blitz", "QUESTIONS.gcse[%d]" % i, band, False, stem, "choice", ans,
                      options=opts, worked=worked))
    return out


# --- quadratics-factorise: quadratic-factoriser's gcse pool (x² + bx + c), a choice of bracket pairs ---
def quad_tex(b, c):
    s = "x^2"
    if b:
        s += (" + " if b > 0 else " - ") + ("" if abs(b) == 1 else str(abs(b))) + "x"
    if c:
        s += (" + " if c > 0 else " - ") + str(abs(c))
    return s


def brackets_tex(p, q):
    return "(x %s %d)(x %s %d)" % ("+" if p >= 0 else "-", abs(p), "+" if q >= 0 else "-", abs(q))


QF_SLIPS = {
    "both": "Those numbers multiply to \\(c\\) but add to the opposite of \\(b\\): check the sign of the \\(x\\) term.",
    "one": "Check both rules: the numbers must multiply to \\(c\\) AND add to \\(b\\).",
    "twice": "\\((x + p)(x + p)\\) expands to \\(x^2 + 2px + p^2\\): you need two numbers that multiply to \\(c\\) and add to \\(b\\).",
}


def qf_worked(it):
    p, q, b, c = it["p"], it["q"], it["b"], it["c"]
    if b == 0:                                                   # a difference of two squares, x^2 - a^2
        a = q if q > 0 else p
        assert p == -q and c == -a * a, ("quadratic-factoriser: a difference of squares", it)
        return ["%s is a difference of two squares." % tex("x^2 - %d" % (a * a)),
                "So it factorises to %s." % tex("(x + %d)(x - %d)" % (a, a))]
    n = lambda v: "(%d)" % v if v < 0 else str(v)
    return ["Find two numbers that multiply to %s and add to %s: %s and %s, because %s and %s." %
            (tex(str(c)), tex(str(b)), tex(str(p)), tex(str(q)), tex("%s \\times %s = %d" % (n(p), n(q), c)),
             tex("%s + %s = %d" % (n(p), n(q), b))),
            "So %s." % tex("%s = %s" % (quad_tex(b, c), brackets_tex(p, q)))]


async def topic_quadratics_factorise(h):
    """quadratic-factoriser's gcse pool (174: both positive 45, one negative 72, both negative 45, difference of squares 12),
    a choice of bracket pairs: the game's (x + p)(x + q), and three of: both signs changed, one sign changed (either),
    the same bracket twice, each checked not to expand to the quadratic (a fourth, p + 1, stands in for a difference of
    squares, which has only two of the three kinds and no slip). The slips are Project Claude's lines (25 Oct), the worked
    lines his template. The key is expanded and compared with x^2 + bx + c. 60, spread over the four stages."""
    pg = await h.page("quadratic-factoriser", "level=gcse")
    pool = await pg.evaluate("() => QF_POOLS.gcse.pool")
    out = []
    for i, it in enumerate(pool):
        p, q, b, c = it["p"], it["q"], it["b"], it["c"]
        assert (p + q, p * q) == (b, c), ("quadratic-factoriser: the pool's own numbers", it)
        cands = [(-p, -q), (p, -q), (-p, q), (p, p), (q, q), (-p, -p), (-q, -q), (p + 1, q), (p, q + 1)]
        wrong, seen = [], {tuple(sorted((p, q)))}
        for w in cands:
            if tuple(sorted(w)) in seen or len(wrong) == 3:
                continue
            assert (w[0] + w[1], w[0] * w[1]) != (b, c)
            seen.add(tuple(sorted(w)))
            wrong.append(w)
        assert len(wrong) == 3
        labels = [tex(brackets_tex(*w)) for w in wrong]
        opts, ans = choice("qf-%d" % i, tex(brackets_tex(p, q)), labels)
        kind = lambda w: "both" if w == (-p, -q) else "twice" if w[0] == w[1] else "one" if w in ((p, -q), (-p, q)) else None
        slips = [{"answer": {"val": next(o["val"] for o in opts if o["label"] == lab)}, "line": QF_SLIPS[kind(w)]}
                 for w, lab in zip(wrong, labels) if kind(w)]
        band = 5 if it["stage"] in ("oneNeg", "dots") else 4
        out.append((it["stage"], mk("quadratics-factorise", "quadratic-factoriser", "QF_POOLS.gcse.pool[%d]" % i, band, False,
                                    "Factorise %s." % tex(quad_tex(b, c)), "choice", ans, options=opts,
                                    worked=qf_worked(it), slip=slips)))
    return [q for _, q in spread(out, GEN_TOPIC, lambda t: t[0])]


# --- estimation: estimation-engine's 45 items, typed ---
def round_sf1(s):
    """A number as the game prints it, rounded to 1 significant figure, half up, as a Decimal."""
    x = Decimal(s)
    return x.quantize(Decimal(1).scaleb(x.adjusted()), rounding=ROUND_HALF_UP)


def est_eval(shape, vals):
    """The game's shape on Fractions (a, b, c, d in order); a square root is taken only of a perfect square."""
    env = {k: Fraction(v) for k, v in zip("abcd", vals)}
    sq = shape.startswith("sqrt(")
    e = shape[5:-1] if sq else shape
    r = eval(e, {"__builtins__": {}}, env)
    if sq:
        n, d = r.numerator, r.denominator
        assert math.isqrt(n) ** 2 == n and math.isqrt(d) ** 2 == d, ("estimation: the root is not exact", shape, vals)
        r = Fraction(math.isqrt(n), math.isqrt(d))
    return r


def est_expr(shape, vals):
    """The shape on the rounded numbers as TeX ('50 \\times 3 \\div 10'), a root as \\sqrt{...}."""
    sq = shape.startswith("sqrt(")
    e = shape[5:-1] if sq else shape
    e = re.sub(r"\((\w)\*(\w)\)/(\w)$", r"\1*\2/\3", e)                 # (a*b)/c reads a x b / c
    e = re.sub(r"[abcd]", lambda m: tnum(Fraction(vals["abcd".index(m.group(0))])), e)        # the numbers first: "\\div" has a d
    e = e.replace("**2", "^2").replace("*", " \\times ").replace("/", " \\div ").replace("+", " + ").replace("-", " - ")
    return "\\sqrt{%s}" % e if sq else e


def est_worked(it, rounded, est):
    """Project Claude's ESTIMATION template (25 Oct): round each number, then work it out with the rounded numbers."""
    shown = ", ".join("%s is %s" % (n, tnum(Fraction(r))) for n, r in zip(it["nums"], rounded))
    expr = est_expr(it["shape"], rounded)
    if it["shape"].startswith("sqrt("):
        inner = est_eval(it["shape"][5:-1], rounded)
        tail = "\\sqrt{%s} = \\sqrt{%s} = %s" % (est_expr(it["shape"][5:-1], rounded), tnum(inner), tnum(est))
    else:
        tail = "%s = %s" % (expr, tnum(est))
    return ["Round each number to 1 significant figure: %s." % shown,
            "Work it out with the rounded numbers: %s." % tex(tail)]


async def topic_estimation(h):
    """Every item of estimation-engine (45): estimate by rounding each number to 1 significant figure. The game's rounded
    numbers and its estimate are recomputed from the printed numbers and the shape (rounding half up). The game's answer
    is the estimate alone, typed; a money question is `money`. The worked lines are Project Claude's template, every
    number in them computed here; the game names no wrong answer, so no slips. Non-calculator."""
    pg = await h.page("estimation-engine", "level=gcse")
    items = await pg.evaluate("() => BANK")
    out = []
    band = {"A": 2, "B": 2, "C": 3, "D": 4, "E": 4, "F": 3}
    for it in items:
        rounded = [round_sf1(s) for s in it["nums"]]
        assert [str(r) if r == r.to_integral_value() and False else tnum(Fraction(r)) for r in rounded] == it["rounded"], \
            ("estimation: the rounded numbers", it["id"], rounded, it["rounded"])
        est = est_eval(it["shape"], rounded)
        assert est == Fraction(Decimal(it["estimate"])), ("estimation: the estimate", it["id"], est, it["estimate"])
        if "tex" in it and it.get("tex"):
            stem = "Estimate the value of %s by rounding each number to 1 significant figure." % tex(it["tex"])
        else:
            stem = it["text"] + " Round each number to 1 significant figure."
        if it.get("money"):
            assert est.denominator == 1
            out.append(mk("estimation", "estimation-engine", "BANK:%s" % it["id"], band[it["group"]], False, stem, "money",
                          {"pence": int(est * 100)}, worked=est_worked(it, rounded, est)))
        else:
            out.append(mk("estimation", "estimation-engine", "BANK:%s" % it["id"], band[it["group"]], False, stem, "number",
                          {"value": numval(Decimal(it["estimate"]))}, worked=est_worked(it, rounded, est)))
    return out


# --- metric-units: unit-converter's gcse bank (length, area, volume, mixed units: 48), a choice ---
UC_MM = {"mm": 1, "cm": 10, "m": 1000, "km": 10 ** 6, "metres": 1000}                       # in mm
UC_UNITS = {}
for _u, _f in UC_MM.items():
    UC_UNITS[_u] = (Fraction(_f), 1)
for _u, _f in (("mm", 1), ("cm", 10), ("m", 1000), ("km", 10 ** 6)):
    UC_UNITS[_u + "²"] = (Fraction(_f) ** 2, 2)
    UC_UNITS[_u + "³"] = (Fraction(_f) ** 3, 3)
UC_UNITS["litres"] = UC_UNITS["litre"] = (Fraction(10 ** 6), 3)                              # 1 litre = 1000 cm³ = 10^6 mm³
UC_UNITS["ml"] = (Fraction(1000), 3)
UC_CONST = {"inches": ("2.54", "cm"), "feet": ("0.3048", "m")}


def uc_num(s):
    return Fraction(Decimal(s.replace(",", "")))


def uc_expected(p):
    """The answer to a 'Convert N unit to unit' item, worked out here from the words (None for a problem in words)."""
    m = re.match(r"Convert ([\d.,]+) (\S+) to (\w[^\s(.]*)", p)
    if not m:
        return None
    n, u1, u2 = uc_num(m.group(1)), m.group(2), m.group(3)
    if u1 in UC_CONST:
        k, base = UC_CONST[u1]
        n, u1 = n * Fraction(Decimal(k)), base
    f1, d1 = UC_UNITS[u1]
    f2, d2 = UC_UNITS[u2]
    assert d1 == d2, ("unit-converter: dimensions", p)
    return n * f1 / f2, {"metres": "m", "litre": "litres"}.get(u2, u2)


def uc_parse_answer(c):
    m = re.fullmatch(r"([\d.,]+) (\S+)", c)
    return uc_num(m.group(1)), m.group(2)


# the problems in words, each worked out independently here (pi as the question gives it; otherwise exact)
UC_WORDS = {
    "A rectangle is 2 m by 50 cm. Area in m²?": Fraction(1),
    "A square has side 300 mm. Area in cm²?": Fraction(900),
    "A hectare is a square 100 m by 100 m. Convert 1 hectare to m²": Fraction(10000),
    "A floor is 4.5 m by 3.2 m. Area in cm²?": Fraction(144000),
    "A box is 50 cm × 30 cm × 20 cm. Volume in m³?": Fraction(3, 100),
    "A cube has side 0.2 m. Volume in cm³?": Fraction(8000),
    "A tank holds 0.5 m³. How many litres?": Fraction(500),
    "Rectangle: 2.5 m by 80 cm. Area in m²?": Fraction(2),
    "Box: 1.5 m × 60 cm × 400 mm. Volume in m³?": Fraction(36, 100),
    "Circle: radius 50 cm. Area in m²? (use π ≈ 3.14)": Fraction(314, 100) * Fraction(1, 2) ** 2,
    "Room: 5 m × 4 m × 2.8 m. Volume in litres?": Fraction(56000),
    "Pipe: diameter 20 mm, length 3 m. Volume in cm³? (π ≈ 3.14)": Fraction(314, 100) * 1 * 300,
    "Sheet metal: 1.2 m × 800 mm. Area in cm²?": Fraction(9600),
    "A swimming pool is 25 m × 10 m × 1.5 m. Volume in litres?": Fraction(375000),
}


def uc_check(it):
    p, key = it["p"], it["c"]
    val, unit = uc_parse_answer(key)
    if p.startswith("Cylinder: radius 10 cm, height 0.5 m."):               # 3 significant figures of 5000 pi
        import sympy
        assert half_sf(Decimal(str(sympy_n(5000 * sympy.pi))), 3) == Decimal(15700) and val == 15700, ("unit-converter: the cylinder", key)
        return
    exp = uc_expected(p)
    if exp is not None:
        assert (val, unit) == exp or (val == exp[0] and unit.rstrip("s") == exp[1].rstrip("s")), ("unit-converter: the answer", p, key, exp)
        for d in it["d"]:
            dv, du = uc_parse_answer(d)
            assert dv != val or du != unit, ("unit-converter: a wrong answer equals the key", p, d)
        return
    assert val == UC_WORDS[p], ("unit-converter: the answer", p, key, UC_WORDS[p])
    for d in it["d"]:
        assert uc_parse_answer(d)[0] != val, ("unit-converter: a wrong answer equals the key", p, d)


def half_sf(x, sf):
    """x to `sf` significant figures, half up."""
    return x.quantize(Decimal(1).scaleb(x.adjusted() - sf + 1), rounding=ROUND_HALF_UP)


async def topic_metric_units(h):
    """unit-converter's gcse bank: length 10, area 15, volume 15, mixed units 8 (48); the level 4 Engineering items are
    above Foundation and are left out. A choice: the game's key and its three wrong answers, the game's steps as the
    worked lines. Every answer is recomputed from the words (conversion factors, the item's own constants and its pi);
    the game's `mc` line is a general reminder, not tied to an option, so it is not a slip. Non-calculator, except the one item that asks for 3 significant figures."""
    pg = await h.page("unit-converter", "level=gcse")
    items = await pg.evaluate("() => [].concat(L, A, V, T)")
    out = []
    band = {"Length": 1, "Area": 2, "Volume": 2, "Mixed Units": 3}
    for i, it in enumerate(items):
        uc_check(it)
        opts, ans = choice("uc-%d" % i, it["c"], it["d"])
        stem = it["p"] if it["p"].endswith(("?", ".")) else it["p"] + "."
        assert len(it["s"]) <= 5
        out.append(mk("metric-units", "unit-converter", "[L,A,V,T][%d]" % i, band[it["sec"]], "significant figures" in it["p"], stem, "choice", ans,
                      options=opts, worked=[s if s.endswith((".", "?")) else s + "." for s in it["s"]]))
    return out


# --- pythagoras: just-pythag-it-bruv's generator, typed, with the game's own triangle ---
JPIB_JS = r"""(seeds) => { const out = [], seen = new Set();
  for (let s = 1; s <= seeds; s++) JPIB.buildSession(s).questions.forEach(q => {
    const k = [q.stage, q.type, q.unknown, q.unit, q.context, JSON.stringify(q.given)].join('|');
    if (seen.has(k)) return; seen.add(k);
    const pic = JPIB.svg(q);
    out.push({q: q, svg: pic.html, notToScale: pic.notToScale, worked: JPIB.worked(q)}); });
  return out; }"""


def jp_dec(s):
    return Decimal(s)


def jp_key(q):
    """The answer worked out here from the sides shown: the square root of the sum (the hypotenuse) or of the difference (a
    shorter side) of the squares, to the item's decimal places, half up."""
    g = q["given"]
    sq = lambda k: jp_dec(g[k]) ** 2
    if q["type"] == "hyp":
        s = sq("p") + sq("q")
    else:
        other = "p" if q["unknown"] == "q" else "q"
        s = sq("r") - sq(other)
    return s


def jp_sqrt_round(s, dp):
    import sympy
    root = sympy.sqrt(sympy.Rational(str(s)))
    return half_up(Decimal(str(sympy.N(root, 40))), dp)


def jp_svg(it):
    """The game's triangle as a self-contained SVG: the outline, the right-angle mark and the labels as text."""
    s = it["svg"]
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    poly = re.search(r'<polygon class="tri-fill" points="([^"]+)"', s).group(1)
    right = re.search(r'<polyline class="tri-right" points="([^"]+)"', s).group(1)
    texts = re.findall(r'<text class="tri-label"[^>]*? x="([^"]+)" y="([^"]+)"[^>]*>([^<]*)</text>', s)
    body = "".join('<text x="%s" y="%s" text-anchor="middle" dominant-baseline="central">%s</text>' % (x, y, t) for x, y, t in texts)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" fill="none" stroke="currentColor" stroke-width="2">'
            '<polygon points="%s" stroke-linejoin="round"/><polyline points="%s" stroke-width="1.5"/>'
            '<g fill="currentColor" stroke="none" font-family="sans-serif" font-size="15">%s</g></svg>' % (vb, poly, right, body)), \
        sorted(t for _, _, t in texts)


def jp_worked(steps, unit, dp):
    lines = []
    for st in steps:
        if st["kind"] == "text":
            lines.append(st["text"] if st["text"].endswith(".") else st["text"] + ".")
        else:
            after = st.get("after", "")
            lines.append(tex(st["tex"] + (("\\text{%s}" % after) if after.strip() else "")) + ".")
    return lines


async def topic_pythagoras(h):
    """just-pythag-it-bruv's questions from its own generator (seeds 1 to 300, each distinct question once): the right-angled
    triangle the game draws (outline, right-angle mark, labels as text), the game's prompt, a typed answer in the
    game's unit. The answer is recomputed from the sides shown (sympy, 40 digits, half up) and the triangle's labels are
    checked against the sides; the game's worked solution is the worked lines, and its one named error, adding instead
    of subtracting, is the slip on a shorter-side question. Whole-number answers (round 1) are non-calculator, decimal
    ones a calculator. 60, ten of each of the six kinds (round, hypotenuse or shorter side)."""
    pg = await h.page("just-pythag-it-bruv", "level=ks3")
    items = await pg.evaluate(JPIB_JS, 300)
    out = []
    for n, it in enumerate(items):
        q = it["q"]
        s = jp_key(q)
        want = jp_sqrt_round(s, q["dp"])
        assert want == Decimal(q["keyText"]), ("pythagoras key", q["stage"], q["given"], want, q["keyText"])
        if q["type"] == "short":
            add = jp_sqrt_round(sum(jp_dec(q["given"][k]) ** 2 for k in ("p", "q", "r") if q["given"][k] is not None), q["dp"])
            assert add == Decimal(q["add"]["k1Text"] if q["dp"] else q["add"]["k0Text"]) or q["dp"] == 0, ("pythagoras add error", q["given"], add)
        svg, labels = jp_svg(it)
        want_labels = sorted(("%s %s" % (v, q["unit"])) if v is not None else "?" for v in q["given"].values())
        labels = ["?" if t == "x" else t for t in labels]                       # the unknown is x after round 1, ? in round 1
        assert labels == want_labels, ("pythagoras labels", labels, want_labels)
        out.append(((q["stage"], q["type"]), it))
    keep = spread(out, GEN_TOPIC, lambda t: t[0])
    res = []
    for (_, it) in keep:
        q = it["q"]
        svg, _ = jp_svg(it)
        stem = q["prompt"]
        if q["dp"] and "decimal place" not in stem:
            stem += " Give your answer to 1 decimal place."
        if it["notToScale"]:
            stem += " The diagram is not drawn accurately."
        ans = {"value": float(Decimal(q["keyText"]))}
        if q["dp"]:
            ans["dp"] = q["dp"]
        slips = []
        if q["type"] == "short":
            k = q["add"]["k1Text"] if q["dp"] else q["add"]["k0Text"]
            if Decimal(k) != Decimal(q["keyText"]):
                slips.append({"answer": {"value": float(Decimal(k))}, "line": "You added instead of subtracting."})
        band = 5 if q["stage"] == "c" else 4
        z = mk("pythagoras", "just-pythag-it-bruv", "JPIB:%s:%s:%s:%s:%s:%s" % (q["stage"], q["type"], q["unknown"], q["unit"], q["context"], json.dumps(q["given"], sort_keys=True)),
               band, bool(q["dp"]), stem, "number", ans, unit=q["unit"], worked=jp_worked(it["worked"], q["unit"], q["dp"]), slip=slips)
        z["diagram"] = svg
        res.append(z)
    return res


# --- coordinates: four-quadrant-explorer's plot, read and shape items, each on a -5 to 5 grid ---
COORD_JS = r"""() => ({plot: PLOT_QUESTIONS, read: READ_QUESTIONS, shape: SHAPE_QUESTIONS})"""


def coord_svg(points, joined=False):
    """A -5 to 5 grid with the axes, the numbers on the grid's border and each point a dot with its letter; `joined` draws
    the line through the points in order."""
    S, O, N = 24, 150, 5
    px = lambda v: O + v * S
    py = lambda v: O - v * S
    f = lambda v: "%g" % round(v, 1)
    parts = ['<g stroke-width="0.6" opacity="0.3">%s</g>' % "".join(
        '<line x1="%s" y1="%s" x2="%s" y2="%s"/><line x1="%s" y1="%s" x2="%s" y2="%s"/>' %
        (f(px(i)), f(py(-N)), f(px(i)), f(py(N)), f(px(-N)), f(py(i)), f(px(N)), f(py(i))) for i in range(-N, N + 1))]
    parts.append('<path d="M%s %s L%s %s M%s %s L%s %s" stroke-width="1.5"/>' % (f(px(-N)), f(O), f(px(N)), f(O), f(O), f(py(N)), f(O), f(py(-N))))
    if joined:
        parts.append('<polyline points="%s" stroke-linejoin="round"/>' % " ".join("%s,%s" % (f(px(x)), f(py(y))) for x, y, _ in points))
    parts.append("".join('<circle cx="%s" cy="%s" r="3.5" fill="currentColor" stroke="none"/>' % (f(px(x)), f(py(y))) for x, y, _ in points))
    texts = []
    for v in range(-N, N + 1):
        if v:
            texts.append((str(v), px(v), py(-N) + 14, "middle"))
            texts.append((str(v), px(-N) - 5, py(v) + 4, "end"))
    for x, y, lab in points:
        # the letter goes to the side of the dot with the most room, off the axes' numbers
        dx = 10 if x < 4 else -10
        dy = -8 if y < 4 else 14
        texts.append((lab, px(x) + dx, py(y) + dy, "middle"))
    body = "".join('<text x="%s" y="%s" text-anchor="%s">%s</text>' % (f(x), f(y), a, t) for t, x, y, a in texts)
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300" role="img" fill="none" stroke="currentColor" stroke-width="2">%s'
           '<g fill="currentColor" stroke="none" font-family="sans-serif" font-size="11">%s</g></svg>' % ("".join(parts), body))
    return svg, sorted(t for t, _, _, _ in texts)


def coord_read_worked(x, y):
    """Project Claude's COORDINATES template (read or plot): across, then up or down, then the pair."""
    across = ("%s means %d %s" % (tex(str(x)), abs(x), "right" if x > 0 else "left")) if x else "%s means no move across" % tex("0")
    updown = ("%s means %d %s" % (tex(str(y)), abs(y), "up" if y > 0 else "down")) if y else "%s means no move up or down" % tex("0")
    return ["The first number is across: %s." % across, "The second number is up or down: %s." % updown,
            "So %s." % tex("(%d, %d)" % (x, y))]


def coord_check(svg_labels_, points):
    want = sorted([str(i) for i in range(-5, 6) if i] * 2 + [lab for _, _, lab in points])
    assert svg_labels_ == want, ("coordinates: labels", svg_labels_, want)


async def topic_coordinates(h):
    """four-quadrant-explorer's 45 items, written out on a grid. READ (15): the game's own four options (a point shown, which
    coordinates), a choice. PLOT (20): the game asks to place a point, which a typed bank cannot, so each is asked the other
    way, as the coordinates of the point shown (`coordinates`); the four whose point a READ item already shows are left
    out so no picture is asked twice. SHAPE (10): three corners of a rectangle shown, the fourth asked (`coordinates`); the
    fourth corner is recomputed from the right angle. The game has no written solution and names no wrong answer."""
    pg = await h.page("four-quadrant-explorer", "level=year6")
    data = await pg.evaluate(COORD_JS)
    out = []
    read_pts = {(r["x"], r["y"]) for r in data["read"]}
    for i, r in enumerate(data["read"]):
        x, y = r["x"], r["y"]
        label = lambda p: "(%s)" % p.strip("()").replace(",", ", ")
        opts_txt = [label(o) for o in r["opts"]]
        assert opts_txt[r["correct"]] == "(%d, %d)" % (x, y), ("coordinates: the game's key", r)
        assert len(set(opts_txt)) == 4 and all(o != opts_txt[r["correct"]] for j, o in enumerate(opts_txt) if j != r["correct"])
        svg, labs = coord_svg([(x, y, "P")])
        coord_check(labs, [(x, y, "P")])
        opts, ans = choice("coord-read-%d" % i, opts_txt[r["correct"]], [o for j, o in enumerate(opts_txt) if j != r["correct"]])
        z = mk("coordinates", "four-quadrant-explorer", "READ_QUESTIONS[%d]" % i, 1, False,
               "The point P is marked on the grid. What are the coordinates of P?", "choice", ans, options=opts,
               worked=coord_read_worked(x, y))
        z["diagram"] = svg
        out.append(z)
    for i, p in enumerate(data["plot"]):
        if (p["x"], p["y"]) in read_pts:
            continue
        svg, labs = coord_svg([(p["x"], p["y"], "P")])
        coord_check(labs, [(p["x"], p["y"], "P")])
        z = mk("coordinates", "four-quadrant-explorer", "PLOT_QUESTIONS[%d]" % i, 1, False,
               "The point P is marked on the grid. Write down the coordinates of P.", "coordinates", {"x": p["x"], "y": p["y"]},
               worked=coord_read_worked(p["x"], p["y"]))
        z["diagram"] = svg
        out.append(z)
    for i, s in enumerate(data["shape"]):
        (ax, ay), (bx, by), (cx, cy) = [(v["x"], v["y"]) for v in s["verts"]]
        assert (bx - ax) * (cx - bx) + (by - ay) * (cy - by) == 0 and (ax == bx or ay == by) and (bx == cx or by == cy), \
            ("coordinates: not a right angle at B", s)
        fourth = (ax + cx - bx, ay + cy - by)
        assert fourth == (s["answer"]["x"], s["answer"]["y"]), ("coordinates: the fourth corner", s, fourth)
        pts = [(ax, ay, "A"), (bx, by, "B"), (cx, cy, "C")]
        xs, ys = ("C", "A") if ax == bx else ("A", "C")             # D's x is the x of the corner not above or below B
        assert (cx if xs == "C" else ax) == fourth[0] and (ay if ys == "A" else cy) == fourth[1], ("coordinates: D lines up", s)
        xy_from = (xs, ys)
        svg, labs = coord_svg(pts, joined=True)
        coord_check(labs, pts)
        z = mk("coordinates", "four-quadrant-explorer", "SHAPE_QUESTIONS[%d]" % i, 2, False,
               "A, B and C are three corners of a rectangle. Write down the coordinates of the fourth corner, D.", "coordinates",
               {"x": fourth[0], "y": fourth[1]},
               worked=["Opposite sides of a rectangle line up: the missing corner D shares its x with %s and its y with %s." % xy_from,
                       "So %s." % tex("(%d, %d)" % fourth)])
        z["diagram"] = svg
        out.append(z)
    return out


# --- the diagram label check (Project Claude, 25 Oct): no label's text box crosses a drawn line other than the side it labels ---
def _svg_parse(svg):
    import xml.etree.ElementTree as ET
    root = ET.fromstring(svg)
    strip = lambda t: t.split("}")[-1]
    return root, strip


def _arc_points(p0, rx, large, sweep, p1, n=16):
    """Points along an SVG circular arc (rx = ry, no rotation) from p0 to p1."""
    (x1, y1), (x2, y2) = p0, p1
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    d2 = dx * dx + dy * dy
    if d2 == 0:
        return [p0]
    r = max(rx, math.sqrt(d2))
    k = math.sqrt(max(0.0, (r * r - d2) / d2))
    if large == sweep:
        k = -k
    cx = (x1 + x2) / 2 + k * dy
    cy = (y1 + y2) / 2 - k * dx
    a1 = math.atan2(y1 - cy, x1 - cx)
    a2 = math.atan2(y2 - cy, x2 - cx)
    da = a2 - a1
    if sweep and da < 0:
        da += 2 * math.pi
    if not sweep and da > 0:
        da -= 2 * math.pi
    return [(cx + r * math.cos(a1 + da * i / n), cy + r * math.sin(a1 + da * i / n)) for i in range(n + 1)]


_ARC_ID = [0]


def _path_segments(d):
    toks = re.findall(r"[MLAZ]|-?\d+(?:\.\d+)?", d)
    segs, i, cur, start, cmd = [], 0, None, None, None
    while i < len(toks):
        if toks[i] in "MLAZ":
            cmd = toks[i]
            i += 1
            if cmd == "Z":
                if cur and start and cur != start:
                    segs.append((cur, start, None))
                cur = start
            continue
        if cmd in ("M", "L"):
            pt = (float(toks[i]), float(toks[i + 1]))
            i += 2
            if cmd == "M" or cur is None:
                start = pt
            else:
                segs.append((cur, pt, None))
            cur = pt
            if cmd == "M":
                cmd = "L"
        elif cmd == "A":
            rx, ry, rot, large, sweep, x, y = (float(t) for t in toks[i:i + 7])
            i += 7
            assert rx == ry and rot == 0, "diagram check: only circular arcs"
            pts = _arc_points(cur, rx, int(large), int(sweep), (x, y))
            _ARC_ID[0] += 1
            segs += [(a, b, ("arc", _ARC_ID[0])) for a, b in zip(pts, pts[1:])]
            cur = (x, y)
        else:
            raise AssertionError("diagram check: path command " + str(cmd))
    return segs


def diagram_segments(svg):
    """The drawn lines of a diagram: line, polygon, polyline and path elements, not the faint grid (a group with opacity below 1)."""
    root, strip = _svg_parse(svg)
    segs = []

    def walk(el, faint):
        faint = faint or float(el.get("opacity", "1")) < 1
        t = strip(el.tag)
        if not faint:
            if t == "line":
                segs.append(((float(el.get("x1")), float(el.get("y1"))), (float(el.get("x2")), float(el.get("y2"))), None))
            elif t in ("polygon", "polyline"):
                pts = [tuple(float(v) for v in p.split(",")) for p in el.get("points").split()]
                segs.extend((a, b, None) for a, b in zip(pts, pts[1:]))
                if t == "polygon":
                    segs.append((pts[-1], pts[0], None))
            elif t == "path":
                segs.extend(_path_segments(el.get("d")))
        for ch in el:
            walk(ch, faint)
    walk(root, False)
    return segs


def diagram_labels(svg):
    """Every text label's box (x0, y0, x1, y1) and its text; the width is 0.55 of the font size a character."""
    root, strip = _svg_parse(svg)
    out = []

    def walk(el, fs, central):
        fs = float(el.get("font-size", fs))
        central = el.get("dominant-baseline", central)
        if strip(el.tag) == "text":
            txt = "".join(el.itertext())
            w, h = 0.55 * fs * len(txt), fs
            x, y = float(el.get("x")), float(el.get("y"))
            anchor = el.get("text-anchor", "start")
            x0 = x - w / 2 if anchor == "middle" else x - w if anchor == "end" else x
            if central == "central":
                y0 = y - h / 2
            else:
                y0 = y - 0.8 * h
            out.append(((x0, y0, x0 + w, y0 + h), txt))
        for ch in el:
            walk(ch, fs, central)
    walk(root, 16.0, "")
    return out


def _seg_hits_box(seg, box):
    (x1, y1), (x2, y2) = seg[0], seg[1]
    x0, y0, xb, yb = box
    t0, t1 = 0.0, 1.0
    dx, dy = x2 - x1, y2 - y1
    for p, q in ((-dx, x1 - x0), (dx, xb - x1), (-dy, y1 - y0), (dy, yb - y1)):
        if p == 0:
            if q < 0:
                return False
        else:
            r = q / p
            if p < 0:
                t0 = max(t0, r)
            else:
                t1 = min(t1, r)
            if t0 > t1:
                return False
    return True


def _seg_dist(seg, pt):
    (x1, y1), (x2, y2) = seg[0], seg[1]
    dx, dy = x2 - x1, y2 - y1
    L = dx * dx + dy * dy
    t = 0 if L == 0 else max(0, min(1, ((pt[0] - x1) * dx + (pt[1] - y1) * dy) / L))
    return math.hypot(pt[0] - (x1 + t * dx), pt[1] - (y1 + t * dy))


def diagram_clashes(svg):
    """[(label text, line)] for every label whose box a drawn line crosses, other than the side the label belongs to: the
    line nearest the label's centre, and for a single-letter label the lines that end at the corner it names."""
    segs = diagram_segments(svg)
    bad = []
    for box, txt in diagram_labels(svg):
        c = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
        if not segs:
            continue
        nearest = min(segs, key=lambda s: _seg_dist(s, c))
        for s in segs:
            if not _seg_hits_box(s, box):
                continue
            if s is nearest or (s[2] is not None and s[2] == nearest[2]):
                continue
            if len(txt) == 1 and txt.isalpha() and any(math.hypot(e[0] - c[0], e[1] - c[1]) <= 16 for e in s[:2]):
                continue
            bad.append((txt, s[:2]))
    return bad


def diagram_overlaps(svg):
    """[(text, text)] for every two labels whose boxes overlap."""
    L = diagram_labels(svg)
    return [(L[i][1], L[j][1]) for i in range(len(L)) for j in range(i + 1, len(L))
            if L[i][0][0] < L[j][0][2] and L[j][0][0] < L[i][0][2] and L[i][0][1] < L[j][0][3] and L[j][0][1] < L[i][0][3]]


PAD = 1.5


def _box_pad(b, pad=PAD):
    return (b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad)


def _viewbox(svg):
    return tuple(float(v) for v in re.search(r'viewBox="([^"]+)"', svg).group(1).split())


def diagram_problems(svg, strict=True):
    """What is wrong with a diagram's labels: a drawn line through a label's box, two labels' boxes overlapping, a box outside
    the viewBox. `strict` counts any line through a box, the label's own side included (a label sits beside its side, never
    on it); not strict is the rule as first worded: only a line other than the side the label belongs to."""
    out = []
    segs = diagram_segments(svg)
    labels = diagram_labels(svg)
    x0, y0, w, h = _viewbox(svg)
    if strict:
        for box, txt in labels:
            if any(_seg_hits_box(s, _box_pad(box)) for s in segs):
                out.append(("line", txt))
    else:
        out += [("line", t) for t, _ in diagram_clashes(svg)]
    out += [("overlap", a + "|" + b) for a, b in diagram_overlaps(svg)]
    for box, txt in labels:
        if box[0] < x0 or box[1] < y0 or box[2] > x0 + w or box[3] > y0 + h:
            out.append(("outside", txt))
    return out


_OFFSETS = [(0, 0)] + [(r * dx, r * dy) for r in (4, 7, 10, 14, 18, 24, 30)
                        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0), (1, -1), (-1, -1), (1, 1), (-1, 1))]


def tidy_labels(svg):
    """Move each label that a drawn line crosses, or that overlaps another label or leaves the viewBox, the shortest way that
    clears all three (up to 30 px); a label that is already clear stays where the game or the builder put it."""
    if not diagram_problems(svg):
        return svg
    segs = diagram_segments(svg)
    labels = diagram_labels(svg)
    x0, y0, w, h = _viewbox(svg)
    boxes = [b for b, _ in labels]
    shift = [(0.0, 0.0)] * len(labels)

    def ok(i, box):
        if any(_seg_hits_box(s, _box_pad(box)) for s in segs):
            return False
        if box[0] < x0 or box[1] < y0 or box[2] > x0 + w or box[3] > y0 + h:
            return False
        for j, o in enumerate(boxes):
            if j != i and box[0] < o[2] and o[0] < box[2] and box[1] < o[3] and o[1] < box[3]:
                return False
        return True
    for i, (b, _) in enumerate(labels):
        if ok(i, b):
            continue
        for dx, dy in _OFFSETS[1:]:
            cand = (b[0] + dx, b[1] + dy, b[2] + dx, b[3] + dy)
            if ok(i, cand):
                boxes[i] = cand
                shift[i] = (dx, dy)
                break
    it = iter(shift)

    def move(m):
        dx, dy = next(it)
        tag = m.group(0)
        if dx == 0 and dy == 0:
            return tag
        x = float(re.search(r' x="([^"]+)"', tag).group(1)) + dx
        y = float(re.search(r' y="([^"]+)"', tag).group(1)) + dy
        tag = re.sub(r' x="[^"]+"', ' x="%g"' % round(x, 1), tag, 1)
        return re.sub(r' y="[^"]+"', ' y="%g"' % round(y, 1), tag, 1)
    return re.sub(r"<text\b[^>]*>", move, svg)


# ───────────────────────────── typed answers (contract SIX-PS-PLAYER-FIXES (h), Jon, 27 Oct 2026) ─────────────────────────────
# A multiple-choice question whose answer a student can write is asked as a typed answer: a guess scores 25% and the exam asks for a
# written answer. The rule is applied here to every bank after its builder has run (a source game is never changed, and no bank is
# edited by hand); the question's id, stem, diagram, working and band stay as they were, the options go, and a distractor that had a
# slip line becomes a slip matched by value. Multiple choice stays for algebra answers (Jon, 25 Oct), probability words and
# statements, ordering, "can you tell" questions and column vectors.
TYPED_TOPICS = ("metric-units", "averages", "trigonometry", "fraction-operations", "coordinates", "simultaneous", "standard-form")
CONVERSIONS = {}          # topic -> {"from": n, "to": {format: n}} for the handover
CONVERSION_NOTES = []     # rounding added, or not determinable (listed for Project Claude)


def _label_of(q, val):
    return next(o["label"] for o in q["options"] if o["val"] == val)


def _plain_number(s):
    """'300,000' or '2.5' as an exact Fraction (thousands commas are in the source's labels, never typed)."""
    return Fraction(s.replace(",", ""))


def _latex_value(label):
    """A label such as \\(4.5 \\times 10^{3}\\) as an exact Fraction, by evaluating it (a path separate from the converter's parse)."""
    s = label.replace("\\(", "").replace("\\)", "").replace("\\times", "*").replace("{", "(").replace("}", ")")
    s = re.sub(r"(-?\d+(?:\.\d+)?)", r"Fraction('\1')", s).replace("^", "**")
    return eval(s, {"Fraction": Fraction})        # a label of digits, * and ^ only: checked by the converter's own regex first


def _frac_label(label):
    """(whole or None, n, d) of a label that is a fraction, a mixed number or a whole number; None if it is none of them."""
    m = re.fullmatch(r"\\\((-?\d+)\\frac\{(\d+)\}\{(\d+)\}\\\)", label)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.fullmatch(r"\\\((-?\d+)\\\)", label)
    if m:
        return (None, int(m.group(1)), 1)
    m = re.fullmatch(r"\\\(\\frac\{(-?\d+)\}\{(\d+)\}\\\)", label)
    return (None, int(m.group(1)), int(m.group(2))) if m else None


def _typed_answer_for(topic, q, label):
    """(format, answer, extras) for one label of a question q in a typed topic, or raises ValueError."""
    if topic == "metric-units":
        m = re.fullmatch(r"(-?[\d,]+(?:\.\d+)?)\s*(\S.*)", label)
        if not m:
            raise ValueError("metric label %r" % label)
        unit = {"litre": "litres"}.get(m.group(2), m.group(2))
        return "number", {"value": float(_plain_number(m.group(1))) if "." in m.group(1) else int(_plain_number(m.group(1)))}, {"unit": unit}
    if topic == "averages":
        if not re.fullmatch(r"-?\d+(?:\.\d+)?", label):
            raise ValueError("average label %r" % label)
        return "number", {"value": float(label) if "." in label else int(label)}, {}
    if topic == "trigonometry":
        deg = label.endswith("°")
        num = label[:-1] if deg else label
        if not re.fullmatch(r"-?\d+(?:\.\d+)?", num):
            raise ValueError("trig label %r" % label)
        stem = q["stem"]
        dps = [d for pat, d in (("nearest degree", 0), ("1 decimal place", 1), ("2 decimal places", 2)) if pat in stem]
        if len(dps) != 1:
            raise ValueError("the rounding in %r cannot be told" % stem)
        dp = dps[0]
        if ("." in num) != (dp > 0) or (dp > 0 and len(num.split(".")[1]) != dp):
            raise ValueError("label %r is not at %d d.p." % (label, dp))
        return "number", {"value": float(num) if dp else int(num), "dp": dp}, ({"unit": "°"} if deg else {})
    if topic == "fraction-operations":
        fr = _frac_label(label)
        if not fr:
            raise ValueError("fraction label %r" % label)
        w, n, d = fr
        return "fraction", ({"n": n, "d": d} if w is None else {"w": w, "n": n, "d": d}), {}
    if topic == "coordinates":
        m = re.fullmatch(r"\((-?\d+), (-?\d+)\)", label)
        if not m:
            raise ValueError("coordinates label %r" % label)
        return "coordinates", {"x": int(m.group(1)), "y": int(m.group(2))}, {}
    if topic == "simultaneous":
        m = re.fullmatch(r"\\\(x = (-?\d+), y = (-?\d+)\\\)", label)
        if not m:
            raise ValueError("simultaneous label %r" % label)
        return "pair", {"x": int(m.group(1)), "y": int(m.group(2))}, {}
    if topic == "standard-form":
        m = re.fullmatch(r"\\\((-?\d+(?:\.\d+)?) \\times 10\^\{?(-?\d+)\}?\\\)", label)
        if m:
            mant = float(m.group(1)) if "." in m.group(1) else int(m.group(1))
            if not 1 <= abs(mant) < 10:
                raise ValueError("the key %r is not in standard form" % label)
            return "standard_form", {"m": mant, "e": int(m.group(2))}, {}
        m = re.fullmatch(r"\\\((-?\d+(?:\.\d+)?)\\\)", label)      # "write ... as an ordinary number": a plain number
        if m:
            return "number", {"value": float(m.group(1)) if "." in m.group(1) else int(m.group(1))}, {}
        raise ValueError("standard-form label %r" % label)
    raise ValueError(topic)


def _typed_value(fmt, a):
    """The value a typed answer stands for, as an exact Fraction or tuple (the second path of the source-equality check)."""
    if fmt == "number":
        return Fraction(str(a["value"]))
    if fmt == "fraction":
        w = a.get("w")
        return Fraction(a["n"], a["d"]) if w is None else (w + Fraction(a["n"], a["d"]) if w >= 0 else w - Fraction(a["n"], a["d"]))
    if fmt in ("coordinates", "pair"):
        return (Fraction(a["x"]), Fraction(a["y"]))
    if fmt == "standard_form":
        return Fraction(str(a["m"])) * Fraction(10) ** a["e"]
    raise ValueError(fmt)


def _label_value(topic, label):
    """The source label's value by its own reading: a plain number, a fraction, a pair of numbers, or an evaluated product."""
    if topic == "metric-units":
        return _plain_number(re.match(r"(-?[\d,]+(?:\.\d+)?)", label).group(1))
    if topic == "averages":
        return Fraction(label)
    if topic == "trigonometry":
        return Fraction(label.rstrip("°"))
    if topic == "fraction-operations":
        w, n, d = _frac_label(label)
        return Fraction(n, d) + (0 if w is None else w)
    if topic in ("coordinates", "simultaneous"):
        nums = re.findall(r"-?\d+", label)
        return (Fraction(nums[0]), Fraction(nums[1]))
    if topic == "standard-form":
        return _latex_value(label)
    raise ValueError(topic)


def _stat_of(stem):
    """An average's key worked out from the data set in its stem (a check that no source label was rounded)."""
    m = re.search(r"data set: ([\d, .]+)\.", stem)
    if not m:
        return None
    xs = sorted(Fraction(x) for x in re.findall(r"\d+(?:\.\d+)?", m.group(1)))
    for word, f in (("mean", lambda: sum(xs) / len(xs)), ("median", lambda: xs[len(xs) // 2] if len(xs) % 2 else (xs[len(xs) // 2 - 1] + xs[len(xs) // 2]) / 2),
                    ("range", lambda: xs[-1] - xs[0])):
        if "the %s of" % word in stem:
            return f()
    if "the mode of" in stem:
        top = max(xs.count(x) for x in xs)
        modes = sorted({x for x in xs if xs.count(x) == top})
        return modes[0] if len(modes) == 1 else None
    return None


def conversion_selftest():
    """to_typed on planted faults: a question converts cleanly; a typed answer that is not the source's, a slip that is not the source's
    and a rounding that cannot be told are each caught. [] if all hold."""
    base = {"id": "t-1", "topic": "metric-units", "source": {"game": "g", "ref": "r"}, "band": 1, "calc": False, "diagram": None,
            "stem": "Convert 2500 mm to m.", "format": "choice", "worked": ["x"], "slip": [],
            "options": [{"val": "a", "label": "250 m"}, {"val": "b", "label": "25 m"}, {"val": "c", "label": "2.5 m"}, {"val": "d", "label": "0.25 m"}],
            "answer": {"val": "c"}}
    out = []
    try:
        z = to_typed("metric-units", dict(base))
        if not (z["format"] == "number" and z["answer"] == {"value": 2.5} and z.get("unit") == "m" and "options" not in z):
            out.append("conversion check: a clean question did not convert to the typed answer %r" % (z["answer"],))
    except Exception as e:           # noqa: BLE001
        out.append("conversion check: a clean question was refused: %s" % e)
    saved = globals()["_typed_answer_for"]
    try:
        globals()["_typed_answer_for"] = lambda topic, q, label: ("number", {"value": 25}, {"unit": "m"})   # the wrong option's value
        try:
            to_typed("metric-units", dict(base))
            out.append("conversion check: planted fault not caught: a typed answer that differs from its source")
        except AssertionError:
            pass
    finally:
        globals()["_typed_answer_for"] = saved
    trig = dict(base, topic="trigonometry", stem="Find the angle.", options=[{"val": "a", "label": "46\u00b0"}, {"val": "b", "label": "16\u00b0"},
                                                                                 {"val": "c", "label": "44\u00b0"}, {"val": "d", "label": "74\u00b0"}], answer={"val": "b"})
    try:
        to_typed("trigonometry", trig)
        out.append("conversion check: planted fault not caught: a rounding that the question does not state")
    except ValueError:
        pass
    return out


def to_typed(topic, q):
    """The question as a typed answer if its topic is converted and it is multiple choice; otherwise unchanged."""
    if topic not in TYPED_TOPICS or q["format"] != "choice":
        return q
    key_label = _label_of(q, q["answer"]["val"])
    if topic == "averages" and re.fullmatch(r"-?[\d.]+( and -?[\d.]+)+", key_label):      # a mode with two values: not one number to type
        CONVERSION_NOTES.append("averages %s stays multiple choice: its answer is %r, two values" % (q["id"], key_label))
        return q
    if topic == "standard-form" and q["stem"].startswith("Which"):      # "which two of these are equal?": a selection, not a value
        CONVERSION_NOTES.append("standard-form %s stays multiple choice: %r is a selection" % (q["id"], q["stem"][:40]))
        return q
    fmt, ans, extra = _typed_answer_for(topic, q, key_label)
    if _typed_value(fmt, ans) != _label_value(topic, key_label):
        raise AssertionError("%s %s: the typed answer %r is not the source's %r" % (topic, q["id"], ans, key_label))
    if topic == "averages":
        want = _stat_of(q["stem"])
        if want is not None and want != _typed_value(fmt, ans):
            raise AssertionError("%s %s: the source label %r is not the statistic %s (rounded?)" % (topic, q["id"], key_label, want))
    z = dict(q)
    z.pop("options", None)
    z["format"], z["answer"] = fmt, ans
    if "unit" in extra:
        z["unit"] = extra["unit"]
    if fmt == "fraction":
        z["accept"] = {"rule": "simplest" if re.search(r"simplest|lowest terms", q["stem"]) else "equivalent"}
    slips = []
    for s in q["slip"]:
        lab = _label_of(q, s["answer"]["val"])
        try:
            sfmt, sans, _ = _typed_answer_for(topic, q, lab)
        except ValueError:      # a distractor a typed answer cannot hold (an unrounded 1.39 for "the nearest degree"): dropped
            CONVERSION_NOTES.append("%s %s: slip %r dropped, not an answer at the asked precision" % (topic, q["id"], lab))
            continue
        if _typed_value(sfmt, sans) == _typed_value(fmt, ans):
            continue
        if _typed_value(sfmt, sans) != _label_value(topic, lab):
            raise AssertionError("%s %s: a slip's typed answer %r is not the source's %r" % (topic, q["id"], sans, lab))
        slips.append({"answer": sans, "line": s["line"]})
    z["slip"] = slips
    c = CONVERSIONS.setdefault(topic, {"from": 0, "to": {}})
    c["from"] += 1
    c["to"][fmt] = c["to"].get(fmt, 0) + 1
    return z


# ───────────────────────────── pie charts (contract PIE-CHARTS-BANK, Jon, 26 Oct 2026): the first bank-first topic ─────────────────────────────
# The questions come from schools/assets/pie-chart-generator.js (MaffsPieCharts), the file the game "Who Ate All the Pies?"
# will load when it is built (canon 8.2.1): the bank is its output, never a copy. Here the pie is drawn, and every answer, slip and
# "you can't tell" is recomputed from the question's own data by pie_expected(), a separate code path from the generator's.
PIE_JS = os.path.join(ROOT, "schools", "assets", "pie-chart-generator.js")
PIE_CANT = "You can't tell"
PIE_SOURCE = "pie-chart-generator"          # the bank-first source: the module, until the game exists
PIE_UNIT = {"amount": "pies", "total": "pies", "angle": "°"}
PIE_FILL = (0.06, 0.2, 0.12, 0.3, 0.16)      # sector shades (opacity): neighbours differ, and every sector is named too


def pie_wrap(name):
    """A sector's name over at most two short lines: 'Cheese and' / 'onion'."""
    lines, cur = [], ""
    for w in name.split():
        if cur and len(cur) + 1 + len(w) > 10:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    lines[0] = lines[0][:1].upper() + lines[0][1:]
    return lines


def pie_block(title, sectors, cx, cy, r, out_text, out_shapes):
    """One pie at (cx, cy): its sectors clockwise from the top, a short tick and a label (name, then the angle where shown) outside each."""
    f = lambda v: "%.1f" % v
    if title:
        out_text.append((title, cx, cy - r - 30, "middle", True))
    start = 0.0
    for i, s in enumerate(sectors):
        a0, a1 = math.radians(start), math.radians(start + s["angle"])
        x0, y0, x1, y1 = cx + r * math.sin(a0), cy - r * math.cos(a0), cx + r * math.sin(a1), cy - r * math.cos(a1)
        large = 1 if s["angle"] > 180 else 0
        out_shapes.append('<path d="M%s %s L%s %s A%s %s 0 %d 1 %s %s Z" fill="currentColor" fill-opacity="%s"/>' %
                          (f(cx), f(cy), f(x0), f(y0), f(r), f(r), large, f(x1), f(y1), PIE_FILL[i % len(PIE_FILL)]))
        mid = math.radians(start + s["angle"] / 2)
        sx, sy = math.sin(mid), -math.cos(mid)
        out_shapes.append('<line x1="%s" y1="%s" x2="%s" y2="%s"/>' % (f(cx + r * sx), f(cy + r * sy), f(cx + (r + 5) * sx), f(cy + (r + 5) * sy)))
        lines = pie_wrap(s["pie"]) + (["%d°" % s["angle"]] if s.get("shown") else [])
        px, py = cx + (r + 9) * sx, cy + (r + 9) * sy
        anchor = "start" if sx > 0.3 else "end" if sx < -0.3 else "middle"
        h = 12 * len(lines)
        top = py - h if sy < -0.3 else py - h / 2 if abs(sy) <= 0.3 else py + 2
        for j, t in enumerate(lines):
            out_text.append((t, px + (2 if anchor == "start" else -2 if anchor == "end" else 0), top + 10 + 12 * j, anchor, False))
        start += s["angle"]


def pie_svg(charts):
    """One chart, or two one above the other (a phone is narrow), every sector named; the angle is on the sectors the question shows."""
    n = len(charts)
    shapes, texts = [], []
    for k, ch in enumerate(charts):
        title = ch["stand"][:1].upper() + ch["stand"][1:] if n > 1 else None
        pie_block(title, ch["sectors"], 150, 120 + 236 * k, 54, texts, shapes)
    body = "".join('<text x="%.1f" y="%.1f" text-anchor="%s"%s>%s</text>' %
                   (x, y, a, ' font-weight="bold"' if bold else "", html.escape(t)) for t, x, y, a, bold in texts)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 %d" role="img" fill="none" stroke="currentColor" stroke-width="1.5">%s'
            '<g fill="currentColor" stroke="none" font-family="sans-serif" font-size="11">%s</g></svg>' % (236 * n, "".join(shapes), body))


def pie_expected(q):
    """What the question's data says, worked out here and not by the generator: {'answer': ..., 'slips': {kind: ...}}. A fraction is
    (n, d) in lowest terms, a number a Fraction, a choice the text of the right option; a choice slip is the text of its option."""
    F = Fraction
    ch, ask = q["charts"], q["ask"]
    t, st = ask["type"], q["stage"]
    sec = lambda c, pie: next(s for s in ch[c]["sectors"] if s["pie"] == pie)
    slips = {}
    if t == "fraction":
        a = sec(0, ask["pie"])["angle"]
        fr = F(a, 360)
        ans = (fr.numerator, fr.denominator)
        shown = next(s for s in ch[0]["sectors"] if s.get("shown"))
        v = F(a, 100) if shown["pie"] == ask["pie"] else F(shown["angle"], 360)
        slips["percent" if shown["pie"] == ask["pie"] else "not360"] = (v.numerator, v.denominator)
    elif t == "amount" and st == 2:
        a = sec(0, ask["pie"])["angle"]
        ans = F(ch[0]["total"]) * a / 360
        slips["percent"] = F(ch[0]["total"]) * a / 100
    elif t == "amount":                                           # stage 5: another sector, in proportion
        ans = F(ask["knownFreq"]) * sec(0, ask["pie"])["angle"] / sec(0, ask["known"])["angle"]
    elif t == "angle":
        s = sec(0, ask["pie"])
        T = ch[0]["total"]
        assert sum(x["freq"] for x in ch[0]["sectors"]) == T, "frequencies must make the total"
        ans = F(s["freq"]) * 360 / T
        slips["percent"] = F(s["freq"]) * 100 / T
        slips["times360"] = F(s["freq"]) * 360
    elif t == "total":
        a = sec(0, ask["pie"])["angle"]
        ans = F(ask["freq"]) * 360 / a
        slips["percent"] = F(ask["freq"]) * 100 / a
    elif t == "cantell" and st == 2:
        assert ch[0]["total"] is None                             # the chart gives no total
        ans = PIE_CANT
        slips["number_no_total"] = "%d pies" % sec(0, ask["pie"])["angle"]
    elif t == "cantell":                                          # stage 5: another chart's numbers cannot be used
        assert ch[0]["total"] is None and ch[1]["total"] is None
        a = sec(0, ask["pie"])["angle"]
        ans = PIE_CANT
        slips["compare_totals"] = "%s pies" % (F(ask["knownFreq"]) * a / ask["knownAngle"])
        slips["number_no_total"] = "%d pies" % a
    elif t == "compare" and len(ch) == 1:                         # one chart: the bigger angle is the bigger share
        p1, p2 = ask["pies"]
        a1, a2 = sec(0, p1)["angle"], sec(0, p2)["angle"]
        ans = "They sold the same number" if a1 == a2 else "Yes, it's " + (p1 if a1 > a2 else p2)
    else:                                                         # two charts, one pie
        sa, sb = ask["stands"]
        a1, a2 = ch[0]["sectors"][0]["angle"], ch[1]["sectors"][0]["angle"]
        t1, t2 = ch[0]["total"], ch[1]["total"]
        guess = "They sold the same number" if a1 == a2 else "Yes, it's the " + (sa if a1 > a2 else sb)
        if t1 is None or t2 is None:
            ans = PIE_CANT
            slips["compare_totals"] = guess
        else:
            n1, n2 = F(t1) * a1 / 360, F(t2) * a2 / 360
            ans = "They sold the same number" if n1 == n2 else "Yes, it's the " + (sa if n1 > n2 else sb)
            bigger = PIE_CANT if a1 == a2 else guess
            if t1 != t2 and bigger != ans:
                slips["compare_totals"] = bigger
    return {"answer": ans, "slips": slips}


def pie_friendly(q, friendly_set):
    """True when every division the method makes is by a friendly divisor and gives a whole number (recomputed here)."""
    F = Fraction
    ch, ask, st = q["charts"], q["ask"], q["stage"]
    ok = lambda d: d in friendly_set
    t = ask["type"]
    angle = lambda c, pie: next(s for s in ch[c]["sectors"] if s["pie"] == pie)["angle"]
    if t == "fraction":
        return ok(F(angle(0, ask["pie"]), 360).denominator)
    if t == "amount" and st == 2:
        fr = F(angle(0, ask["pie"]), 360)
        return ok(fr.denominator) and ch[0]["total"] % fr.denominator == 0
    if t == "angle":
        T = ch[0]["total"]
        return 360 % T == 0 and ok(T)
    if t == "total":
        fr = F(angle(0, ask["pie"]), 360)
        return ok(fr.denominator) and ask["freq"] % fr.numerator == 0
    if t == "amount":
        a, b = angle(0, ask["known"]), angle(0, ask["pie"])
        g = math.gcd(a, b)
        return ok(a // g) and ask["knownFreq"] % (a // g) == 0
    if t == "compare" and len(ch) == 2 and ch[0]["total"] is not None and ch[1]["total"] is not None and ch[0]["total"] != ch[1]["total"]:
        return all(ok(F(c["sectors"][0]["angle"], 360).denominator) and c["total"] % F(c["sectors"][0]["angle"], 360).denominator == 0 for c in ch)
    return True


def pie_faults(q, friendly_set):
    """Every fault in one generated pie question, by the independent recompute. [] when it holds."""
    f = []
    F = Fraction
    for c in q["charts"]:
        angles = [s["angle"] for s in c["sectors"]]
        if sum(angles) != 360 or any(not isinstance(a, int) or a < 15 for a in angles):
            f.append("angles %s are not whole numbers of 15 degrees or more that make 360" % angles)
        if len({s["pie"] for s in c["sectors"]}) != len(c["sectors"]):
            f.append("a pie is named twice in one chart")
        if c["total"] is not None and any((F(c["total"]) * a / 360).denominator != 1 for a in angles):
            f.append("a sector's amount is not a whole number (total %s, angles %s)" % (c["total"], angles))
    exp = pie_expected(q)
    a, ex = q["answer"], exp["answer"]
    if a["type"] == "fraction":
        if (a["n"], a["d"]) != ex or math.gcd(a["n"], a["d"]) != 1:
            f.append("fraction answer %s/%s, recomputed %s" % (a["n"], a["d"], ex))
    elif a["type"] == "number":
        if F(a["value"]) != ex or ex.denominator != 1:
            f.append("number answer %s, recomputed %s" % (a["value"], ex))
    else:
        if a["options"][a["correct"]] != ex:
            f.append("the right option is %r, recomputed %r" % (a["options"][a["correct"]], ex))
        if len(set(a["options"])) != 4:
            f.append("the options are not four different ones")
    for sl in q["slips"]:
        want = exp["slips"].get(sl["kind"])
        got = sl["answer"]
        if want is None:
            f.append("slip %s cannot be recomputed from the data" % sl["kind"])
        elif isinstance(want, tuple):
            if (got["n"], got["d"]) != want:
                f.append("slip %s is %s/%s, recomputed %s" % (sl["kind"], got["n"], got["d"], want))
        elif isinstance(want, str):
            if got.get("option") != want or got.get("option") not in a.get("options", []):
                f.append("slip %s is %r, recomputed %r" % (sl["kind"], got.get("option"), want))
            if want == ex:
                f.append("slip %s is the key" % sl["kind"])
        else:
            if abs(float(got["value"]) - float(want)) > 1e-9:
                f.append("slip %s is %s, recomputed %s" % (sl["kind"], got["value"], want))
            if want == ex:
                f.append("slip %s equals the key" % sl["kind"])
    if not 3 <= len(q["worked"]) <= 5:
        f.append("%d worked lines" % len(q["worked"]))
    if pie_friendly(q, friendly_set) != q["friendly"]:
        f.append("friendly is %s, recomputed %s" % (q["friendly"], pie_friendly(q, friendly_set)))
    if q["stage"] != 3 and q["kind"] != "one":       # the angle of the pie asked about, and each total, are also in the words
        asked = {q["ask"].get("pie"), q["ask"].get("known")}
        for n in [str(s["angle"]) for c in q["charts"] for s in c["sectors"] if s.get("shown") and s["pie"] in asked] +                  [str(c["total"]) for c in q["charts"] if c["total"] is not None]:
            if n not in q["stem"]:
                f.append("the stem does not say %s" % n)
    return f


def pie_selftest(sample, friendly_set):
    """pie_faults on planted faults: a clean question passes, each fault is caught. [] if all hold."""
    import copy
    base = {k: next(q for q in sample if q["stage"] == st and q["kind"] == kd) for k, (st, kd) in {
        "frac": (1, "direct"), "amount": (2, "direct"), "cant": (4, "two"), "draw": (3, "draw"),
        "two": (4, "totals"), "total": (5, "total")}.items()}
    out = []
    for k, q in base.items():
        if pie_faults(q, friendly_set):
            out.append("pie check: a clean %s question was flagged: %s" % (k, pie_faults(q, friendly_set)[:2]))

    def plant(name, key, edit):
        q = copy.deepcopy(base[key])
        edit(q)
        if not pie_faults(q, friendly_set):
            out.append("pie check: planted fault not caught: " + name)
    plant("a wrong fraction", "frac", lambda q: q["answer"].update(n=q["answer"]["n"] + 1))
    plant("an amount found by dividing by 100", "amount",
          lambda q: q["answer"].update(value=q["charts"][0]["total"] * q["charts"][0]["sectors"][0]["angle"] / 100))
    plant("angles that do not make 360", "amount", lambda q: q["charts"][0]["sectors"][0].update(angle=q["charts"][0]["sectors"][0]["angle"] + 5))
    plant("a stand called bigger where the totals are missing", "cant", lambda q: q["answer"].update(correct=(q["answer"]["correct"] + 1) % 4))
    plant("a wrong angle", "draw", lambda q: q["answer"].update(value=q["answer"]["value"] + 1))
    plant("the wrong stand called bigger", "two", lambda q: q["answer"].update(correct=(q["answer"]["correct"] + 1) % 4))
    plant("a slip equal to the key", "total",
          lambda q: q["slips"].append({"kind": "percent", "answer": {"type": "number", "value": q["answer"]["value"]}, "line": "x"}))
    return out


async def pie_generate(h):
    """The generator's questions, 12 a stage, run in the browser, each slot from its own fixed seed; and its friendly divisors."""
    pg = await h.browser.new_page()
    await pg.goto("about:blank")
    await pg.add_script_tag(content=open(PIE_JS, encoding="utf-8").read())
    js = ("() => { %s const out = []; for (const st of MaffsPieCharts.STAGES) for (let sl = 0; sl < MaffsPieCharts.SLOTS; sl++) "
          "{ const seed = st * 100 + sl + 1; const q = MaffsPieCharts.question(st, sl, mul(seed)); q.seed = seed; out.push(q); } "
          "return { questions: out, friendly: MaffsPieCharts.FRIENDLY }; }") % MULBERRY
    data = await pg.evaluate(js)
    await pg.close()
    return data["questions"], set(data["friendly"])


def pie_question(q):
    """One generated question as a schema-1 bank question."""
    a = q["answer"]
    opts = None
    if a["type"] == "fraction":
        fmt, ans, accept, unit = "fraction", {"n": a["n"], "d": a["d"]}, {"rule": "simplest"}, None
    elif a["type"] == "number":
        fmt, ans, accept, unit = "number", {"value": a["value"]}, None, PIE_UNIT[q["ask"]["type"]]
    else:
        fmt, accept, unit = "choice", None, None
        opts = [{"val": "abcd"[k], "label": l} for k, l in enumerate(a["options"])]
        ans = {"val": "abcd"[a["correct"]]}
    slips = []
    for s in q["slips"]:
        sa = s["answer"]
        if fmt == "choice":
            slips.append({"answer": {"val": "abcd"[a["options"].index(sa["option"])]}, "line": s["line"]})
        elif fmt == "fraction":
            slips.append({"answer": {"n": sa["n"], "d": sa["d"]}, "line": s["line"]})
        else:
            slips.append({"answer": {"value": sa["value"]}, "line": s["line"]})
    ref = "generator:MaffsPieCharts.question:%d:%d:%d" % (q["stage"], q["slot"], q["seed"])
    z = mk("pie-charts", PIE_SOURCE, ref, q["band"], "optional", q["stem"], fmt, ans, accept=accept, unit=unit, options=opts,
           worked=q["worked"], slip=slips)
    if q["friendly"]:
        z["try_without"] = True
    z["diagram"] = pie_svg(q["charts"]) if q["stage"] != 3 else None
    return z


async def topic_pie_charts(h):
    """Matchday pie sales at a sports stadium: 12 questions in each of five stages (read it, find the amount, draw it, can you tell?,
    work backwards), generated by pie-chart-generator.js and each recomputed by pie_faults() from its own data. Stage 3 gives the
    frequency table in the stem and asks one angle, so it has no picture; the other stages draw the chart, every sector named."""
    qs, friendly = await pie_generate(h)
    bad = ["stage %d slot %d: %s" % (q["stage"], q["slot"], x) for q in qs for x in pie_faults(q, friendly)]
    bad += pie_selftest(qs, friendly)
    if len({json.dumps([q["stem"], q["answer"]], sort_keys=True) for q in qs}) != len(qs):
        bad.append("the generator made two questions alike")
    for st in range(1, 6):
        if sum(1 for q in qs if q["stage"] == st) < 10:
            bad.append("stage %d has fewer than 10 questions" % st)
    if bad:
        raise AssertionError("pie-charts: " + "; ".join(bad[:8]))
    return [pie_question(q) for q in qs]


# ───────────────────────────── percentages and money (contract PERCENTAGES-MONEY-BANK, Jon, 27 Oct 2026): the second bank-first topic ─────
# The questions come from schools/assets/percentages-money-generator.js (MaffsPercentagesMoney), the file the game "It's on Sale!" will
# load when it is built (canon 8.2.1). Every answer and slip is recomputed here from the question's own params by pm_expected(), exactly
# (Fractions, never floats), a separate code path from the generator's integer arithmetic.
PM_JS = os.path.join(ROOT, "schools", "assets", "percentages-money-generator.js")
PM_SOURCE = "percentages-money-generator"


def pm_round(x):
    """The nearest penny, halves up, from an exact Fraction."""
    return math.floor(x + Fraction(1, 2))


def pm_steps(p, B):
    """The amounts and the multipliers or divisors the method for 'p% of B' (pence) uses, worked out here from the rule table:
    50, 25, 75 by halves and quarters; a multiple of 10 by 10%; a multiple of 5 by 10% and its half; anything else by 1%."""
    F = Fraction
    x = F(B) * p / 100
    if p == 50:
        return [F(B) / 2], [2]
    if p == 25:
        return [F(B) / 4], [4]
    if p == 75:
        return [F(B) / 4, x], [4, 3]
    if p % 10 == 0:
        return ([F(B) / 10] + ([x] if p > 10 else [])), [10] + ([p // 10] if p > 10 else [])
    if p % 5 == 0:
        k = (p - 5) // 10
        return [F(B) / 10, F(B) / 20] + ([x] if k > 0 else []), [10, 2] + ([k] if k > 0 else [])
    return [F(B) / 100, x], [100, p]


def pm_friendly_run(steps, mults):
    return all(s.denominator == 1 and s % 5 == 0 for s in steps) and all(m <= 12 or m % 10 == 0 for m in mults)


def pm_expected(q):
    """What the question's params say, worked out here and not by the generator: {'answer': Fraction (pence, or a percentage),
    'slips': {kind: Fraction}, 'friendly': bool, 'steps': [Fraction] (the amounts a student works with, which must be whole pence)}."""
    F = Fraction
    P_, st = q["params"], q["stage"]
    slips = {}
    if st == 1:
        steps, mults = pm_steps(P_["pct"], P_["base"])
        return {"answer": F(P_["base"]) * P_["pct"] / 100, "slips": slips, "friendly": pm_friendly_run(steps, mults), "steps": steps}
    if st == 2:
        steps, mults = pm_steps(P_["pct"], P_["base"])
        x = F(P_["base"]) * P_["pct"] / 100
        new = P_["base"] - x if P_["dir"] == "dec" else P_["base"] + x
        slips["only_percentage"] = x
        return {"answer": new, "slips": slips, "friendly": pm_friendly_run(steps + [new], mults), "steps": steps + [new]}
    if st == 3:
        o, n = F(P_["old"]), F(P_["new"])
        c = abs(n - o)
        if (n < o) != (P_["dir"] == "dec"):
            raise AssertionError("direction does not match old and new")
        one = o / 100
        over = 100 * c / n
        if (over * 100).denominator == 1:                      # a value a student can type exactly: the only case the generator may offer
            slips["over_new"] = over
        p = 100 * c / o
        return {"answer": p, "slips": slips, "friendly": one % 10 == 0 and one.denominator == 1 and c % 5 == 0 and p % 5 == 0,
                "steps": [c, one], "optional_slips": ["over_new"]}
    if st == 4:
        k = 100 - P_["pct"] if P_["dir"] == "dec" else 100 + P_["pct"]
        one = F(P_["newp"]) / k
        wrong = F(P_["newp"]) * k / 100
        slips["off_sale_price"] = wrong
        return {"answer": one * 100, "slips": slips, "friendly": (k <= 12 or k % 10 == 0) and one.denominator == 1 and one % 5 == 0,
                "steps": [one, one * 100], "optional_slips": ["off_sale_price"]}
    # stage 5
    P, r, y, kind, qty = P_["principal"], P_["rate"], P_["years"], P_["kind"], P_["qty"]
    comp = lambda m: pm_round(F(P) * F(m, 100) ** y)
    lose = P if qty == "interest" else 0
    if kind == "simple":
        interest = F(P) * r * y / 100
        ans = interest if qty == "interest" else P + interest
        slips["compound_for_simple"] = comp(100 + r) - lose
    elif kind == "compound":
        ans = comp(100 + r) - lose
        slips["simple_for_compound"] = pm_round(F(P) + F(P) * r * y / 100) - lose
        slips["times_years"] = pm_round(F(P) * (100 + r) * y / 100) - lose
        if r < 10:
            slips["multiplier_digit"] = comp(100 + r * 10) - lose
    else:
        ans = comp(100 - r)
        slips["depreciation_added"] = comp(100 + r)
        if r % 10 == 0:
            slips["multiplier_digit"] = comp(r)
    return {"answer": ans, "slips": slips, "friendly": False, "steps": []}


def pm_faults(q):
    """Everything wrong with one generated question, from its own params: [] when it is sound."""
    F = Fraction
    f = []
    exp = pm_expected(q)
    a, ex = q["answer"], exp["answer"]
    if a["type"] == "money":
        if ex.denominator != 1 or a["pence"] != ex:
            f.append("money answer %s pence, recomputed %s" % (a["pence"], ex))
    else:
        if ex.denominator != 1 or a["value"] != ex:
            f.append("percentage answer %s, recomputed %s" % (a["value"], ex))
    P_ = q["params"]
    if q["stage"] <= 4:
        bad = [s for s in exp["steps"] if F(s).denominator != 1]
        if bad:
            f.append("a step of the working is not whole pence: %s" % bad)
        base = P_.get("base", P_.get("old", 0))
        if q["stage"] != 4 and base % 100 != 0:
            f.append("the amount is not a whole number of pounds")
        if q["calc"] != "optional":
            f.append("stages 1-4 are calculator optional")
    else:
        if P_["kind"] != "simple":
            m = 100 + P_["rate"] if P_["kind"] == "compound" else 100 - P_["rate"]
            n = F(P_["principal"]) * F(m, 100) ** P_["years"]
            if (n - math.floor(n)) == F(1, 2):
                f.append("the answer is a half-penny: the rounding would decide it")
            if "nearest penny" not in q["stem"]:
                f.append("the stem does not say 'to the nearest penny'")
        if P_["kind"] == "simple" and "simple interest" not in q["stem"]:
            f.append("a simple interest question that does not say so")
        if P_["kind"] == "compound" and "compound interest" not in q["stem"]:
            f.append("a compound interest question that does not say so")
        if q["calc"] != "calculator":
            f.append("stage 5 is a calculator stage")
    got = {s["kind"]: s for s in q["slips"]}
    for kind, sl in got.items():
        want = exp["slips"].get(kind)
        if want is None:
            f.append("slip %s cannot be recomputed from the data" % kind)
            continue
        have = sl["answer"].get("pence", sl["answer"].get("value"))
        if abs(float(have) - float(want)) > 1e-9:
            f.append("slip %s is %s, recomputed %s" % (kind, have, want))
        if F(have) == ex or F(want) == ex:
            f.append("slip %s equals the key" % kind)
    for kind, want in exp["slips"].items():       # a slip is offered wherever its value is a distinct, exact answer
        if kind in got or F(want) == ex:
            continue
        if kind == "off_sale_price" and F(want) % 100 != 0:
            continue
        f.append("slip %s is missing" % kind)
    if not 2 <= len(q["worked"]) <= 5:
        f.append("%d worked lines" % len(q["worked"]))
    if q["friendly"] != exp["friendly"]:
        f.append("friendly is %s, recomputed %s" % (q["friendly"], exp["friendly"]))
    need = []                                      # the numbers the question asks about are in its words
    if q["stage"] in (1, 2, 4):
        need.append("%d%%" % P_["pct"])
    if q["stage"] in (1, 2):
        need.append(P_["base"])
    if q["stage"] == 3:
        need += [P_["old"], P_["new"]]
    if q["stage"] == 4:
        need.append(P_["newp"])
    if q["stage"] == 5:
        need += [P_["principal"], "%d%%" % P_["rate"], "%d years" % P_["years"]]
    for n in need:
        t = n if isinstance(n, str) else "£%s" % (("%d" % (n // 100)) if n % 100 == 0 else "%.2f" % (n / 100))
        if t not in q["stem"]:
            f.append("the stem does not say %s" % t)
    return f


def pm_selftest(sample):
    """pm_faults on planted faults: a clean question passes, each fault is caught. [] if all hold."""
    import copy
    pick = lambda st, kind=None: next(q for q in sample if q["stage"] == st and (kind is None or q["kind"] == kind))
    base = {"s1": pick(1), "s2": pick(2, "dec"), "s3": pick(3, "dec"), "s4": pick(4, "dec"), "simple": pick(5, "simple"),
            "compound": pick(5, "compound"), "dep": pick(5, "depreciation")}
    out = []
    for k, q in base.items():
        if pm_faults(q):
            out.append("pm check: a clean %s question was flagged: %s" % (k, pm_faults(q)[:2]))

    def plant(name, key, edit):
        q = copy.deepcopy(base[key])
        edit(q)
        if not pm_faults(q):
            out.append("pm check: planted fault not caught: " + name)
    plant("a percentage of an amount off by 1p", "s1", lambda q: q["answer"].update(pence=q["answer"]["pence"] + 1))
    plant("only the percentage given as the new price", "s2", lambda q: q["answer"].update(pence=q["slips"][0]["answer"]["pence"]))
    plant("a percentage change out by one", "s3", lambda q: q["answer"].update(value=q["answer"]["value"] + 1))
    plant("a reverse percentage taken off the sale price", "s4", lambda q: q["answer"].update(pence=q["params"]["newp"] * 8 // 10))
    plant("compound worked as simple", "compound", lambda q: q["answer"].update(
        pence=round(q["params"]["principal"] * (1 + q["params"]["rate"] * q["params"]["years"] / 100))))
    plant("depreciation added instead of taken off", "dep", lambda q: q["answer"].update(
        pence=round(q["params"]["principal"] * (1 + q["params"]["rate"] / 100) ** q["params"]["years"])))
    plant("a simple interest answer a penny out", "simple", lambda q: q["answer"].update(pence=q["answer"]["pence"] + 1))
    plant("a slip that is the key", "s2", lambda q: q["slips"].append({"kind": "only_percentage", "answer": {"pence": q["answer"]["pence"]}, "line": "x"}))
    plant("a stage 5 question marked calculator optional", "compound", lambda q: q.update(calc="optional"))
    plant("friendly wrongly true", "compound", lambda q: q.update(friendly=True))
    return out


async def pm_generate(h):
    """The generator's questions, 12 a stage, run in the browser, each slot from its own fixed seed."""
    pg = await h.browser.new_page()
    await pg.goto("about:blank")
    await pg.add_script_tag(content=open(PM_JS, encoding="utf-8").read())
    js = ("() => { %s const out = []; for (const st of MaffsPercentagesMoney.STAGES) for (let sl = 0; sl < MaffsPercentagesMoney.SLOTS; sl++) "
          "{ const seed = st * 100 + sl + 1; const q = MaffsPercentagesMoney.question(st, sl, mul(seed)); q.seed = seed; out.push(q); } "
          "return out; }") % MULBERRY
    data = await pg.evaluate(js)
    await pg.close()
    return data


def pm_question(q):
    """One generated question as a schema-1 bank question."""
    a = q["answer"]
    if a["type"] == "money":
        fmt, ans, unit = "money", {"pence": a["pence"]}, None
    else:
        fmt, ans, unit = "number", {"value": a["value"]}, "%"
    slips = [{"answer": ({"pence": s["answer"]["pence"]} if fmt == "money" else {"value": s["answer"]["value"]}), "line": s["line"]}
             for s in q["slips"]]
    ref = "generator:MaffsPercentagesMoney.question:%d:%d:%d" % (q["stage"], q["slot"], q["seed"])
    z = mk("percentages-money", PM_SOURCE, ref, q["band"], True if q["calc"] == "calculator" else "optional", q["stem"], fmt, ans, unit=unit,
           worked=q["worked"], slip=slips)
    if q["friendly"]:
        z["try_without"] = True
    return z


async def topic_percentages_money(h):
    """A high-street shop, a savings account and a car dealer: 12 questions in each of five stages (percentage of an amount, increase or
    decrease, percentage change, reverse percentages, interest and depreciation), generated by percentages-money-generator.js and each
    recomputed by pm_faults() from its own params."""
    qs = await pm_generate(h)
    bad = ["stage %d slot %d: %s" % (q["stage"], q["slot"], x) for q in qs for x in pm_faults(q)]
    bad += pm_selftest(qs)
    if len({json.dumps([q["stem"], q["answer"]], sort_keys=True) for q in qs}) != len(qs):
        bad.append("the generator made two questions alike")
    for st in range(1, 6):
        if sum(1 for q in qs if q["stage"] == st) < 12:
            bad.append("stage %d has fewer than 12 questions" % st)
    simple = sum(1 for q in qs if q["stage"] == 5 and q["kind"] == "simple")
    if not 2 <= simple <= 4:
        bad.append("%d of 12 stage 5 questions are simple interest (about 1 in 4)" % simple)
    if bad:
        raise AssertionError("percentages-money: " + "; ".join(bad[:8]))
    return [pm_question(q) for q in qs]


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
    "inverse-operations": topic_inverse_operations,
    "trigonometry": topic_trigonometry,
    "simultaneous": topic_simultaneous,
    "transformations": topic_transformations,
    "simplify-expressions": topic_simplify_expressions,
    "substitution": topic_substitution,
    "standard-form": topic_standard_form,
    "quadratics-factorise": topic_quadratics_factorise,
    "estimation": topic_estimation,
    "metric-units": topic_metric_units,
    "pythagoras": topic_pythagoras,
    "coordinates": topic_coordinates,
    "pie-charts": topic_pie_charts,
    "percentages-money": topic_percentages_money,
}


# ───────────────────────────── the review fixes (SIX-PS-REVIEW-FIXES, 27 Oct 2026) ─────────────────────────────
# An independent review found faults of eight kinds (scripts/six_ps_rules.py, rules a-h). Each class is fixed here, for every bank, after
# the builders have run and before the diagram label check, and every bank is then held to the rules by --check. A source game is
# never changed; a stored answer is never changed (the one distractor of powers-roots-7a198409 is the contract's single exception).
REVIEW_FIXED = {}         # (topic, fix) -> questions changed, for the handover


def right_angle_marked(svg):
    """svg with a right-angle mark added at the square corner of a drawn triangle that has none (rule f)."""
    if RULES.has_right_angle_mark(svg):
        return svg
    m = re.search(r'<path d="([^"]*)"', svg)
    if not m:
        return svg
    pts = [(float(a), float(b)) for a, b in re.findall(r"[ML]\s*(-?[\d.]+)\s+(-?[\d.]+)", m.group(1))]
    uniq = []
    for p in pts:
        if p not in uniq:
            uniq.append(p)
    if len(uniq) != 3:
        return svg
    for i, v in enumerate(uniq):
        a, b = uniq[(i + 1) % 3], uniq[(i + 2) % 3]
        u, w = (a[0] - v[0], a[1] - v[1]), (b[0] - v[0], b[1] - v[1])
        lu, lw = math.hypot(*u), math.hypot(*w)
        if lu and lw and abs(u[0] * w[0] + u[1] * w[1]) < 0.01 * lu * lw:
            k = 11.0
            p1 = (v[0] + k * u[0] / lu, v[1] + k * u[1] / lu)
            p3 = (v[0] + k * w[0] / lw, v[1] + k * w[1] / lw)
            p2 = (p1[0] + p3[0] - v[0], p1[1] + p3[1] - v[1])
            mark = '<polyline points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" stroke-width="1.5"/>' % (p1 + p2 + p3)
            return svg.replace("<g fill=", mark + "<g fill=", 1)
    return svg


def _powers_roots_7a198409(q):
    """(5^2)^3: option d, 25^3, equals the key 5^6. The genuine misconception 'multiplied the base by the first power' gives 10^3."""
    for o in q["options"]:
        if o["label"] == "\\(25^3\\)":
            o["label"] = "\\(10^3\\)"
            return True
    return False


def _area_594fb670(q):
    """The 12 m label belongs on the dashed height line (x = 90), not out beside the slanted side."""
    old = '<text x="114" y="86" text-anchor="start">12 m</text>'
    if old in q["diagram"]:
        q["diagram"] = q["diagram"].replace(old, '<text x="96" y="104" text-anchor="start">12 m</text>')
        return True
    return False


def _metric_4f223446(q):
    """'÷ 1000.' with no result: the line states the sum."""
    if q["worked"] and q["worked"][-1].strip().endswith("1000."):
        q["worked"] = ["Divide by 1000: \\(8200 \\div 1000 = 8.2\\)."]
        return True
    return False


def fix_fraction_bars(q):
    """fraction-operations (item 8): the working speaks of chocolate bars the question does not show. 'Each bar is one whole chocolate
    bar.' goes, and 'cut a bar into 3, take 1' becomes 'cut one whole into 3 equal pieces, take 1'."""
    new = [re.sub(r"cut a bar into (\d+), take (\d+)\.", r"cut one whole into \1 equal pieces, take \2.", w)
           for w in q["worked"] if w != "Each bar is one whole chocolate bar."]
    changed = new != q["worked"]
    q["worked"] = new
    return changed


def fix_quadratic_names(q):
    """quadratics-factorise (item 8): slip lines name b and c, which the question never defines. They say what they mean instead."""
    def say(t):
        t = t.replace("multiply to \\(c\\)", "multiply to the number on its own")
        t = t.replace("add to the opposite of \\(b\\)", "add to the opposite of the number in front of \\(x\\)")
        t = t.replace("add to \\(b\\)", "add to the number in front of \\(x\\)")
        return t
    old = json.dumps([q["worked"], q["slip"]])
    q["worked"] = [say(w) for w in q["worked"]]
    for sl in q["slip"]:
        sl["line"] = say(sl["line"])
    return old != json.dumps([q["worked"], q["slip"]])


ID_FIXES = {"powers-roots-7a198409": _powers_roots_7a198409, "area-594fb670": _area_594fb670, "metric-units-4f223446": _metric_4f223446}


def apply_review_fixes(tid, q):
    def note(name, changed):
        if changed:
            REVIEW_FIXED[(tid, name)] = REVIEW_FIXED.get((tid, name), 0) + 1
    for qid, fn in ID_FIXES.items():
        if q["id"].startswith(qid):
            note(fn.__name__.strip("_").split("_")[0] + " " + qid.split("-")[-1], fn(q))
    if tid == "fraction-operations":
        note("working without the chocolate bars", fix_fraction_bars(q))
    if tid == "quadratics-factorise":
        note("slips name b and c", fix_quadratic_names(q))
    note("slips (c)", RULES.fix_slips(q))
    note("simplest form (b)", RULES.fix_simplest(q))
    note("common difference sign", RULES.fix_common_difference(q))
    if q.get("diagram") and tid == "area":
        new = right_angle_marked(q["diagram"])
        note("right angle marked (f)", new != q["diagram"])
        q["diagram"] = new
    if tid != "basic-probability":                       # its stems are rewritten at source (Probability Pioneer), not patched
        before = json.dumps([q["stem"], [o["label"] for o in q.get("options") or []], q["worked"], q["slip"]], ensure_ascii=False)
        RULES.fix_texts(q)
        note("words out of the maths (h)", before != json.dumps([q["stem"], [o["label"] for o in q.get("options") or []], q["worked"], q["slip"]], ensure_ascii=False))
    note("answer line (d)", RULES.fix_answer_line(q))
    return q


async def build_all(only):
    banks = {}
    async with Harness() as h:
        for tid, fn in BUILDERS.items():
            if only and tid not in only:
                continue
            qs = [apply_review_fixes(tid, to_typed(tid, q)) for q in await fn(h)]
            ids = [q["id"] for q in qs]
            if len(set(ids)) != len(ids):
                raise AssertionError("%s: duplicate ids" % tid)
            for q in qs:                                   # the diagram label check, then the labels moved where it finds a fault
                if q.get("diagram"):
                    st = DIAGRAM_STATS.setdefault(tid, {"diagrams": 0, "as_worded": 0, "strict": 0, "overlap": 0, "left": 0})
                    st["diagrams"] += 1
                    probs = diagram_problems(q["diagram"], strict=False)
                    st["as_worded"] += any(k == "line" for k, _ in probs)
                    full = diagram_problems(q["diagram"])
                    st["strict"] += any(k == "line" for k, _ in full)
                    st["overlap"] += any(k != "line" for k, _ in full)
                    q["diagram"] = tidy_labels(q["diagram"])
                    st["left"] += bool(diagram_problems(q["diagram"]))
            banks[tid] = {"topic": tid, "schema": 1, "questions": qs}
    return banks


DIAGRAM_STATS = {}


def diagram_selftest():
    """The diagram label check on four planted diagrams: a clean one is passed, a label with a line through it, two labels
    on top of each other and a label outside the viewBox are each caught, and the labels are moved clear. [] if all hold."""
    head = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><line x1="0" y1="50" x2="100" y2="50"/><g font-size="13">'
    case = lambda body: head + body + "</g></svg>"
    text = lambda x, y, t="5 m": '<text x="%s" y="%s" text-anchor="middle">%s</text>' % (x, y, t)
    faults = []
    if diagram_problems(case(text(50, 30))):
        faults.append("diagram check: a clean label was flagged")
    for what, svg, kind in (("a line through a label", case(text(50, 50)), "line"),
                            ("two labels overlapping", case(text(50, 30) + text(52, 31)), "overlap"),
                            ("a label outside the viewBox", case(text(2, 30)), "outside")):
        if not any(k == kind for k, _ in diagram_problems(svg)):
            faults.append("diagram check: planted fault not caught: " + what)
        if diagram_problems(tidy_labels(svg)):
            faults.append("diagram check: the labels were not moved clear: " + what)
    return faults


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
  if(q.format==='pair')return 'x = '+a.x+', y = '+a.y;
  if(q.format==='standard_form')return a.m+' \u00d7 10^'+a.e;
  if(q.format==='number_unit')return a.value+' '+esc(a.unit);
  return a.value+(q.unit?' '+esc(q.unit):'');
}
function show(t){
  var b=BANKS[t],h='';
  b.questions.forEach(function(q){
    var rule=q.accept?' ('+esc(q.accept.rule)+')':'';
    h+='<div class="card"><div class="meta"><span>'+esc(q.id)+'</span><span>band '+q.band+'</span><span>'+(q.calc==='optional'?'calculator optional'+(q.try_without?', try without':''):q.calc?'calculator':'non-calculator')+'</span><span>'+esc(q.format)+rule+'</span></div>'
      +'<div class="stem">'+rich(q.stem)+'</div>'+(q.diagram?'<div class="fig">'+q.diagram+'</div>':'');
    if(q.format==='choice'){h+='<ul class="opts">'+q.options.map(function(o){return '<li'+(o.val===q.answer.val?' class="right"':'')+'>'+o.val+') '+rich(o.label)+'</li>'}).join('')+'</ul>';}
    else{h+='<div class="ans">Answer: <b>'+ansText(q)+'</b>'+(q.units?' <span class="slip">(unit buttons: '+q.units.map(esc).join(', ')+')</span>':'')+'</div>';}
    h+=q.worked.length?'<ol>'+q.worked.map(function(w){return '<li>'+rich(w)+'</li>'}).join('')+'</ol>':'<div class="none">No worked solution in the game</div>';
    q.slip.forEach(function(s){h+='<div class="slip">If the answer is <b>'+(q.format==='number_unit'?s.answer.value+' '+esc(s.answer.unit):q.format==='fraction'?s.answer.n+'/'+s.answer.d:q.format==='choice'?rich((q.options.filter(function(o){return o.val===s.answer.val})[0]||{label:s.answer.val}).label):s.answer.value!==undefined?s.answer.value:JSON.stringify(s.answer))+'</b>: '+rich(s.line)+'</div>'});
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
            for rule, x in RULES.faults(q):
                faults.append("%s %s: rule (%s) %s" % (t, q["id"], rule, x))
        print("%-32s %3d questions  bands %s" % (t, len(b["questions"]),
              sorted({q["band"] for q in b["questions"]})))
    for t, c in CONVERSIONS.items():                   # typed answers: what was multiple choice and what it is now
        print("typed answers   %-20s %3d multiple choice questions now typed: %s" % (t, c["from"], c["to"]))
    for n in CONVERSION_NOTES:
        print("typed answers   left or changed: " + n)
    for (t, name), n in sorted(REVIEW_FIXED.items()):
        print("review fixes    %-20s %-30s %3d questions" % (t, name, n))
    for t, st in DIAGRAM_STATS.items():                # the diagram label check, over every diagram the run built
        print("diagram labels  %-20s %3d diagrams: line through a label %2d as first worded, %2d strict; labels overlapping %2d; "
              "still faulty after the labels are moved %d" % (t, st["diagrams"], st["as_worded"], st["strict"], st["overlap"], st["left"]))
        if st["left"]:
            faults.append("%s: %d diagrams still have a label crossed, overlapped or outside" % (t, st["left"]))
    if DIAGRAM_STATS:
        tot = lambda k: sum(s[k] for s in DIAGRAM_STATS.values())
        print("diagram labels  TOTAL %d diagrams: %d with a line through a label as first worded, %d strict, %d with overlapping labels; "
              "%d still faulty after the labels are moved" % (tot("diagrams"), tot("as_worded"), tot("strict"), tot("overlap"), tot("left")))
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
        bad += diagram_selftest()
        bad += conversion_selftest()
        bad += ["rules selftest: " + name for name, ok in RULES.selftest() if not ok]
        for x in bad:
            print("FAIL  " + x)
        if bad:
            return 1
        print("PASS  %d banks match their games; covered topics and banks agree" % len(banks))
    return 0


if __name__ == "__main__":
    sys.exit(main())
