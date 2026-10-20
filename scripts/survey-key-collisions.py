#!/usr/bin/env python3
"""Key-collision survey (contract KEY-COLLISION-SURVEY, Jon, 20 Oct 2026). REPORT ONLY, not wired into CI.

In every game that generates its questions, find each question it can produce where a named or common error,
rounded as the game rounds its key, gives the key: a student using that wrong method is marked right (a typed
answer is marked by value; in multiple choice the student picks the key). Just Pythag It, Bruv is the control: it
had 7 such questions before #453 and must report zero now.

How it works. Each game's page is loaded through the stub server (scripts/serve-stubbed.py: no analytics leave the
machine) and its question space is read from the page itself: the game's own pools, or its own generator driven
through every choice it can make (choice-tree enumeration: rInt / randInt / Math.random are replaced by a counter,
and every path is walked depth first). The keys and every error are then recomputed HERE, in Python, with exact
arithmetic (fractions; integer square roots), from the numbers the question shows, and rounded exactly as the game
rounds its key. Nothing in any game, verifier or shared file is changed.

    python scripts/survey-key-collisions.py            # every game; prints the report's tables (Markdown)
    python scripts/survey-key-collisions.py --game split-it
"""
import argparse
import json
import math
import os
import re
import sys
from fractions import Fraction
from math import gcd, isqrt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

ROOT = os.path.dirname(HERE)

# Listed or not: read from the roster (a game in its Unlisted or Withdrawn section is not listed).
def listed_games():
    text = open(os.path.join(ROOT, ".claude", "rules", "game-roster.md"), encoding="utf-8").read()
    out, section = set(), None
    for line in text.splitlines():
        if line.startswith("## "):
            section = line
        m = re.match(r"^\| ?([0-9]+) \| [^|]+ \| `([a-z0-9-]+)` \|", line)
        if m and section and not section.startswith(("## Unlisted", "## Withdrawn")):
            out.add(m.group(2))
    return out


# ---------------------------------------------------------------- exact rounding

def round_half_up(x, dp):
    """x (a Fraction) rounded half up to dp places, as a Fraction (negative values: half away from zero)."""
    x = Fraction(x)
    s = -1 if x < 0 else 1
    q = abs(x) * Fraction(10) ** dp
    return s * math.floor(q + Fraction(1, 2)) / Fraction(10) ** dp


def round_sqrt(S, dp):
    """sqrt(S) rounded half up to dp places, S a non-negative Fraction: the largest K with (2K-1)^2 <= 4*100^dp*S."""
    S = Fraction(S)
    T = 4 * S * 10 ** (2 * dp)
    m = isqrt(T.numerator // T.denominator)
    return Fraction((m + 1) // 2, 10 ** dp)


def sig3(x):
    """x rounded to 3 significant figures, half up (as Number(v.toPrecision(3)) does for a float not on a tie)."""
    if x == 0:
        return Fraction(0)
    x = Fraction(x)
    e = math.floor(math.log10(abs(float(x))))
    return round_half_up(x, 2 - e)


# ---------------------------------------------------------------- the browser

class Pages:
    """One Chromium, one stub server; page(slug) loads games/<slug>/ with nothing leaving the machine."""

    def __init__(self):
        from playwright.sync_api import sync_playwright
        self.proc, self.base = bc.start_stub_server()
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch()

    def page(self, slug, ready, query=""):
        ctx = self.browser.new_context()
        base = self.base
        ctx.route("**/*", lambda r: r.continue_() if r.request.url.startswith(base) else r.abort())
        ctx.route(lambda u: bc.is_font_cdn(u), bc.serve_real_font)
        p = ctx.new_page()
        p.goto("%s/games/%s/%s" % (base, slug, query), wait_until="load", timeout=30000)
        p.wait_for_function(ready, timeout=15000)
        return ctx, p

    def close(self):
        self.browser.close()
        self.pw.stop()
        self.proc.terminate()


# Choice-tree enumeration in the page. RAND names the page's integer draw (rInt, randInt); Math.random is answered
# 0.25 or 0.75 (a two-way choice: every Math.random() test in the generators enumerated this way compares with a
# threshold strictly between those). A path deeper than MAX choices (a redraw loop) is cut off; its siblings are
# still walked, so every question a redraw can reach is reached. Returns the distinct questions (by JSON).
ENUM_JS = r"""([RAND, CALL, MAX]) => {
  const realRandom = Math.random, realRand = window[RAND];
  const out = [], seen = new Set(), stack = [[]];
  let paths = 0, cut = 0;
  try {
    while (stack.length) {
      const prefix = stack.pop(), arity = [], chosen = [];
      let pos = 0;
      const next = n => { if (pos >= MAX) throw 'deep';
        const c = pos < prefix.length ? prefix[pos] : 0; arity[pos] = n; chosen[pos] = c; pos++; return c; };
      window[RAND] = (a, b) => a + next(b - a + 1);
      Math.random = () => next(2) === 0 ? 0.25 : 0.75;
      let q = null;
      try { q = (0, eval)(CALL); } catch (e) { if (e !== 'deep') throw e; cut++; }
      paths++;
      for (let i = chosen.length - 1; i >= prefix.length; i--)
        for (let c = arity[i] - 1; c >= 1; c--) stack.push(chosen.slice(0, i).concat([c]));
      if (q) { const k = JSON.stringify(q); if (!seen.has(k)) { seen.add(k); out.push(q); } }
    }
  } finally { Math.random = realRandom; window[RAND] = realRand; }
  return { questions: out, paths: paths, cut: cut };
}"""


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s or "")


def nums(s):
    return [Fraction(x) for x in re.findall(r"\d+(?:\.\d+)?", strip_tags(s))]


# ---------------------------------------------------------------- results

class Result:
    def __init__(self, slug, part, space, method, marking):
        self.slug, self.part, self.space, self.method, self.marking = slug, part, space, method, marking
        self.errors = []          # (name, kind, how many questions it applies to, collisions, [examples])
        self.members = {}         # row name -> every colliding question (the self-test reads it)
        self.reclassified = 0     # coincidences moved to 'agree (identity)' by their group (COLLISION-IDENTITIES)
        self.precision = 0        # collisions of a precision slip, 'agree (precision)' by its type (Jon, 20 Oct)
        self.notes = []

    def add(self, name, applies, hits, example_fmt, kind="coincidence", group=None, universe=None, label=str):
        """kind: 'coincidence' (a wrong formula whose value happens to equal the key), 'agree' (on these questions
        the wrong method is the same calculation as the right one, so no question of this shape can tell them
        apart), 'agree (precision)' (a precision slip, such as rounding too early: where it changes the answer the
        student is already marked wrong; Jon's ruling (2), 20 Oct 2026, classes it by type, grouped or not), or
        'two-way' (a rule of thumb's agreement with a two-way choice: not a collision, not counted).

        group, universe (contract COLLISION-IDENTITIES, Jon, 20 Oct 2026): group(q) is the question parameter an
        identity would be about (b, for a mod b), universe every question the error applies to. A coincidence is
        an identity, and moves to 'agree (identity)', when the error equals the key on EVERY question of its group
        and the group has at least two questions (one question alone is no evidence of an identity). label(g) names
        the group in the report. Only exact identities are grouped: an error that holds across a group only at the
        marking precision (trig-worms' upside-down ratio at cos 80 deg) stays a coincidence (Jon's ruling (2)), so
        trig-worms passes no group."""
        if group is not None and kind == "coincidence" and hits:
            hit = {id(h) for h in hits}
            groups = {}
            for q in universe:
                groups.setdefault(group(q), []).append(q)
            whole = {g for g, qs in groups.items() if len(qs) >= 2 and all(id(q) in hit for q in qs)}
            ident = [h for h in hits if group(h) in whole]
            if ident:
                gname = "%s [identity: %s]" % (name, "; ".join(label(g) for g in sorted(whole, key=str)))
                self.errors.append((gname, "agree (identity)", applies, len(ident), [example_fmt(h) for h in ident[:5]]))
                self.members[gname] = ident
                self.reclassified += len(ident)
                hits = [h for h in hits if group(h) not in whole]
        if kind == "agree (precision)":
            self.precision += len(hits)
        self.errors.append((name, kind, applies, len(hits), [example_fmt(h) for h in hits[:5]]))
        self.members[name] = hits

    @property
    def collisions(self):
        return sum(e[3] for e in self.errors if e[1] != "two-way")

    def by_kind(self, kind):
        """'agree' counts every agree class: plain, identity and precision."""
        return sum(e[3] for e in self.errors if e[1] == kind or e[1].startswith(kind + " ("))


# ---------------------------------------------------------------- just-pythag-it-bruv (the control)

def survey_jpib(pages):
    ctx, p = pages.page("just-pythag-it-bruv", "!!window.JPIB && !!JPIB.CONTEXTS")
    d = p.evaluate("""() => { const J = JPIB, ctx = {};
      J.CONTEXT_IDS.forEach(id => { const C = J.CONTEXTS[id]; ctx[id] = { D: C.D, pool: C.pool }; });
      return { triples: J.TRIPLES.map(t => t.base.map(x => x * t.k)), b: J.POOL_B, ctx: ctx }; }""")
    ctx.close()
    qs = []   # (where, kind, x, y, dp): x, y exact in the question's units; hyp: the legs; short: hypotenuse, leg
    for t in d["triples"]:
        a, b, c = (Fraction(v) for v in t)
        qs += [("round 1 %s" % t, "hyp", a, b, 0), ("round 1 %s" % t, "short", c, a, 0),
               ("round 1 %s" % t, "short", c, b, 0)]
    for kind in ("hyp", "short"):
        qs += [("round 2 %s %s" % (kind, e), kind, Fraction(e[0]), Fraction(e[1]), 1) for e in d["b"][kind]]
        for cid, c in sorted(d["ctx"].items()):
            qs += [("round 3 %s %s %s" % (cid, kind, e[:2]), kind, Fraction(e[0], c["D"]), Fraction(e[1], c["D"]), 1)
                   for e in c["pool"][kind]]
    rd = round_half_up
    errs = {
        "hyp": [("sqrt(|b^2-a^2|): subtract instead of add", lambda x, y, dp: round_sqrt(abs(y * y - x * x), dp)),
                ("a^2+b^2: no square root", lambda x, y, dp: rd(x * x + y * y, dp)),
                ("a+b: add the sides", lambda x, y, dp: rd(x + y, dp)),
                ("sqrt(2a+2b): double instead of square", lambda x, y, dp: round_sqrt(2 * (x + y), dp))],
        "short": [("sqrt(c^2+a^2): add instead of subtract (the game's own diagnosis)",
                   lambda x, y, dp: round_sqrt(x * x + y * y, dp)),
                  ("c^2-a^2: no square root", lambda x, y, dp: rd(x * x - y * y, dp)),
                  ("c-a: subtract the sides", lambda x, y, dp: rd(x - y, dp)),
                  ("sqrt(2c-2a): double instead of square", lambda x, y, dp: round_sqrt(2 * (x - y), dp))],
    }
    r = Result("just-pythag-it-bruv", "all three rounds (control)", "%d questions (every pool entry, every variant)"
               % len(qs), "enumerated (pools read from window.JPIB)",
               "typed; round 1 exact whole number, rounds 2-3 to 1 d.p. half up (MaffsAnswer)")
    for kind in ("hyp", "short"):
        for name, f in errs[kind]:
            sub = [q for q in qs if q[1] == kind]
            hits = []
            for where, _, x, y, dp in sub:
                key = round_sqrt(x * x + y * y if kind == "hyp" else x * x - y * y, dp)
                if f(x, y, dp) == key:
                    hits.append((where, key))
            r.add("%s (%s)" % (name, kind), len(sub), hits, lambda h: "%s: key %s" % (h[0], float(h[1])))
    return [r]


# ---------------------------------------------------------------- how-many-parts (contract HOW-MANY-PARTS, 20 Oct 2026)

def survey_how_many_parts(pages):
    """Stages 1-3 (adding and taking away): every pool entry, every named error written out here from the contract's
    words. The game filters its pools so none equals its key (as PR 453), so every count here should be 0."""
    ctx, p = pages.page("how-many-parts", "!!window.HMP && !!HMP.POOLS")
    pools = p.evaluate("() => ({ a: HMP.POOLS.a, b: HMP.POOLS.b, c: HMP.POOLS.c })")
    ctx.close()

    def lcm(x, y):
        return x * y // gcd(x, y)

    def frac(n, m):
        return Fraction(n, m) if n > 0 and m > 0 else None
    errs = (("adding (taking away) the tops and the bottoms", lambda a, b, s, c, d: frac(a + s * c, b + s * d)),
            ("changing a denominator without its numerator",
             lambda a, b, s, c, d: frac(a + s * c, lcm(b, d)) if b != d else None),
            ("adding the numerators and keeping the larger denominator",
             lambda a, b, s, c, d: frac(a + s * c, max(b, d)) if b != d else None),
            ("multiplying the denominators but adding the numerators", lambda a, b, s, c, d: frac(a + s * c, b * d)),
            ("multiplying the fractions", lambda a, b, s, c, d: frac(a * c, b * d)),
            ("the other operation", lambda a, b, s, c, d: abs(Fraction(a, b) - s * Fraction(c, d)) or None))
    results = []
    for st, label in (("a", "stage 1, same denominator"), ("b", "stage 2, one denominator a multiple of the other"),
                      ("c", "stage 3, different denominators")):
        qs = pools[st]
        r = Result("how-many-parts", label, "%d questions (the whole pool)" % len(qs), "enumerated (HMP.POOLS)",
                   "multiple choice, by dataset.val: the exact value in its simplest form")
        for name, f in errs:
            applies, hits = 0, []
            for q in qs:
                sg = 1 if q["op"] == "+" else -1
                key = Fraction(q["a"], q["b"]) + sg * Fraction(q["c"], q["d"])
                v = f(q["a"], q["b"], sg, q["c"], q["d"])
                if v is None:
                    continue
                applies += 1
                if v == key:
                    hits.append(q)
            r.add(name, applies, hits, lambda h: "%d/%d %s %d/%d" % (h["a"], h["b"], h["op"], h["c"], h["d"]))
        results.append(r)
    return results


# ---------------------------------------------------------------- six-sevens-bruv

def survey_ssb(pages):
    ctx, p = pages.page("six-sevens-bruv", "!!window.SSB && !!SSB.FACTS")
    # Every question: the facts not gold at the start (x1 facts start gold), each swap and form the game allows.
    qs = p.evaluate("""() => { const out = [], gold = SSB.startGold();
      SSB.FACTS.forEach(f => { if (gold[f.key]) return;
        [false, true].forEach(sw => { if (sw && f.a === f.b) return;
          SSB.formsFor(f).forEach(form => out.push(SSB.makeQuestion(f, sw, form))); }); });
      return out; }""")
    ctx.close()
    r = Result("six-sevens-bruv", "times tables 2-12", "%d questions (66 facts x swap x form)" % len(qs),
               "enumerated (SSB.FACTS, SSB.formsFor, SSB.makeQuestion)", "typed whole number, exact (parseInt === answer)")
    prod = [q for q in qs if q["form"] == "product"]
    miss = [q for q in qs if q["form"] != "product"]
    def ex(h):
        return "%s: key %d" % (" ".join(h["parts"]), h["answer"])
    r.add("x+y: add instead of multiply (product form)", len(prod),
          [q for q in prod if q["x"] + q["y"] == q["c"]], ex)
    r.add("x(y-1) or (x-1)y: one lot short (product form)", len(prod),
          [q for q in prod if q["c"] in (q["x"] * (q["y"] - 1), (q["x"] - 1) * q["y"])], ex)
    r.add("x(y+1) or (x+1)y: one lot over (product form)", len(prod),
          [q for q in prod if q["c"] in (q["x"] * (q["y"] + 1), (q["x"] + 1) * q["y"])], ex)
    given = lambda q: q["y"] if q["form"] == "left" else q["x"]
    r.add("c - given: subtract instead of divide (missing factor)", len(miss),
          [q for q in miss if q["c"] - given(q) == q["answer"]], ex)
    r.add("c x given: multiply instead of divide (missing factor)", len(miss),
          [q for q in miss if q["c"] * given(q) == q["answer"]], ex)
    r.add("the given factor copied (missing factor)", len(miss),
          [q for q in miss if given(q) == q["answer"]], ex)
    return [r]


# ---------------------------------------------------------------- split-it

def survey_split_it(pages):
    ctx, p = pages.page("split-it", "typeof generators === 'object' && typeof rInt === 'function'")
    results = []
    for mode in ("simplify", "equivalent", "divide", "fractions", "scale", "unitary"):
        for level in ("ks3", "gcse"):
            e = p.evaluate(ENUM_JS, ["rInt", "generators[%s](%s)" % (json.dumps(mode), json.dumps(level)), 14])
            qs = e["questions"]
            r = Result("split-it", "%s, %s" % (mode, level), "%d distinct questions (%d paths walked, %d redraw paths cut)"
                       % (len(qs), e["paths"], e["cut"]), "enumerated (generators[mode] driven through every rInt and "
                       "Math.random choice)", "typed, every box must be right (MaffsAnswer.exact / .money / .decimal 1 d.p.;"
                       " fractions exact numerator and denominator)")
            survey_split_mode(r, mode, level, qs)
            results.append(r)
    ctx.close()
    return results


def survey_split_mode(r, mode, level, qs):
    ex = lambda h: "%s: key %s" % (strip_tags(h["prompt"]).replace("\n", " ")[:90],
                                    ":".join(str(a) for a in h["answers"]))
    A = lambda q: [Fraction(str(a)) for a in q["answers"]]
    if mode == "simplify":
        def given(q):
            return nums(q["prompt"])[:3 if q["type"] == "ratio3" else 2]
        r.add("parts in the wrong order (reversed)", len(qs),
              [q for q in qs if list(reversed(A(q))) == A(q)], ex, "agree")
        def halved(q):
            g = given(q)
            return [x / 2 for x in g] if all(x % 2 == 0 for x in g) else None
        r.add("halved once (divided by 2 only)", len(qs), [q for q in qs if halved(q) == A(q)], ex, "agree")
        if level == "gcse":
            def first_two(q):
                a, b, c = (int(x) for x in given(q))
                h = gcd(a, b)
                return [Fraction(a, h), Fraction(b, h), Fraction(c, h)]
            r.add("divided by the HCF of the first two parts only", len(qs), [q for q in qs if first_two(q) == A(q)], ex, "agree")
    elif mode == "equivalent":
        # ks3: "a : b = ak : ?" (key bk) or "a : b = ? : bk" (key ak); gcse: "a : b = x : bk" (key ak)
        def additive(q):
            t = strip_tags(q["prompt"])
            n = nums(q["prompt"])
            a, b = n[0], n[1]
            if re.search(r"= \d+ : \?", t):
                return [b + (n[2] - a)]          # adds the change in the first term to the second
            return [a + (n[2] - b)]              # adds the change in the second term to the first
        r.add("additive: add the difference instead of multiplying", len(qs), [q for q in qs if additive(q) == A(q)], ex, "agree")
    elif mode == "divide":
        def halves(q):
            return [Fraction(q["total"], len(q["ratio"]))] * len(q["ratio"])
        r.add("shared equally (amount / number of parts)", len(qs), [q for q in qs if halves(q) == A(q)], ex, "agree")
        def per_part(q):
            return [Fraction(q["total"], x) for x in q["ratio"]]
        r.add("amount / each ratio part (divide by one part, not the total)", len(qs),
              [q for q in qs if per_part(q) == A(q)], ex, group=lambda q: tuple(q["ratio"]), universe=qs,
              label=lambda g: "ratio %s, every amount" % ":".join(map(str, g)))
    elif mode == "fractions":
        def over_other(q):
            parts = nums(q["prompt"])                    # the ratio's parts, in order
            tp = sum(parts)
            num = A(q)[0] * tp / A(q)[1]                 # the asked part, from the key
            rest = tp - num
            g = gcd(int(num), int(rest))
            return [num / g, rest / g]
        r.add("part over the other part(s), not over the total", len(qs), [q for q in qs if over_other(q) == A(q)], ex)
    elif mode == "scale":
        def additive(q):
            d = q["targetServes"] - q["origServes"]
            return [Fraction(i["v"]) + d for i in q["items"]]
        r.add("additive: add the change in servings to each amount", len(qs), [q for q in qs if additive(q) == A(q)], ex)
        def times_target(q):
            return [Fraction(i["v"]) * q["targetServes"] for i in q["items"]]
        r.add("multiplied by the new servings, not the scale factor", len(qs), [q for q in qs if times_target(q) == A(q)], ex)
    elif mode == "unitary":
        def parse(q):
            t = strip_tags(q["prompt"])
            return t, nums(q["prompt"])
        sub = [q for q in qs if q["type"] != "bestvalue"]
        def inverse(q):
            t, n = parse(q)
            if "travels" in t:     # d in t hours, how far in t2:   d x t / t2 (inverted)
                d, t1, t2 = n[0], n[1], n[2]
                return [round_half_up(d * t1 / t2, 1)]
            if "Convert" in t:     # GBP -> EUR: divide by the rate instead of multiplying
                rate, amt = n[1], n[2]
                return [round_half_up(amt / rate, 2)]
            nn, cost, m = n[0], n[1], n[2]
            return [round_half_up(cost / m * nn, 2)]
        r.add("inverse operation (divide where it multiplies, or n/m for m/n)", len(sub), [q for q in sub if inverse(q) == A(q)], ex)
        def no_unit(q):
            t, n = parse(q)
            if "travels" in t:
                return [n[0] * n[2]]
            if "Convert" in t:
                return [n[2]]
            return [n[1] * n[2]]
        r.add("skipped the unit step (multiplied the total by the new quantity)", len(sub),
              [q for q in sub if no_unit(q) == A(q)], ex)
        bv = [q for q in qs if q["type"] == "bestvalue"]
        if bv:
            agree = [q for q in bv if ("A" if q["nA"] > q["nB"] else "B") == q["answers"][0]]
            r.add("best value: the bigger pack (two-way choice; chance is about half)", len(bv), agree,
                  lambda h: "A %d for %dp, B %d for %dp: key %s" % (h["nA"], h["pA"], h["nB"], h["pB"], h["answers"][0]), "two-way")
            agree2 = [q for q in bv if ("A" if q["pA"] < q["pB"] else "B") == q["answers"][0]]
            r.add("best value: the cheaper pack overall (two-way choice)", len(bv), agree2,
                  lambda h: "A %d for %dp, B %d for %dp: key %s" % (h["nA"], h["pA"], h["nB"], h["pB"], h["answers"][0]), "two-way")


# ---------------------------------------------------------------- free-daily-pizza

def survey_fdp(pages):
    ctx, p = pages.page("free-daily-pizza", "!!window.FDP && !!FDP.BANK")
    bank = p.evaluate("""() => { const out = [];
      [1, 2, 3, 4].forEach(s => FDP.BANK[s].forEach(it => out.push({ id: it.id, stage: s, kind: it.kind, from: it.from,
        to: it.to, v: it.v, n: it.n, d: it.d, a: it.a, b: it.b, N: it.N, p: it.p, A: it.A, B: it.B,
        asksSimplest: it.asksSimplest, answer: { form: it.answer.form, value: it.answer.value, shown: it.answer.shown || null },
        offered: it.distractors.map(o => o.tag) })));
      return out; }""")
    ctx.close()
    F_ = lambda n, d=1: Fraction(n, d)
    # Each misconception, defined from FDP.TAGS' words and recomputed here from the item's numbers; each returns the
    # value the student would arrive at, or None where it does not apply. Marking compares the option's key: the form
    # and the value, and for a fraction asked in its simplest form the numbers shown (so an unsimplified fraction is
    # a different option even though it is the same value).
    def mis(it):
        k, out = it["kind"], []
        if k == "conv":
            a, b = it["v"]
            v = F_(a, b)
            if b <= 9:
                out.append(("denominator-as-decimal: the bottom number read as the decimal (b/10)", F_(b, 10)))
            out.append(("inversion: the fraction turned upside down", F_(b, a)))
            for s in (1, -1, 2, -2):
                out.append(("place-value: %s by %d" % ("x" if s > 0 else "/", 10 ** abs(s)), v * F_(10) ** s))
            if it["to"] == "p":
                out.append(("raw-part: the top number as the percentage (a%)", F_(a, 100)))
            if it["from"] == "d" and it["to"] == "f":
                digits = str(float(v)).split(".")[1] if "." in str(float(v)) else ""
                if digits and digits[0] != "0" and len(digits) <= 3 and int(digits) >= 2:
                    out.append(("digit-reading: the digits after the point as a denominator (1/digits)", F_(1, int(digits))))
            if it["from"] == "p" and it["to"] == "f" and (v * 100).denominator == 1 and v * 100 >= 2:
                out.append(("digit-reading: the percentage number as a denominator (1/p)", F_(1, int(v * 100))))
        elif k == "simp":
            n, d = it["n"], it["d"]
            g = gcd(n, d); a, b = n // g, d // g
            out.append(("subtract-instead: the same number taken off top and bottom", (a, d - n + a)))
            out.append(("inversion: upside down", (b, a)))
            out.append(("one-side-only: the top divided, not the bottom", (a, d)))
        elif k == "ofamt-f":
            a, b, N = it["a"], it["b"], it["N"]
            out += [("one-part-only: N/b, not scaled up", F_(N, b)),
                    ("complement: the part left over", F_(N * (b - a), b)),
                    ("no-divide: multiplied by the top only", F_(a * N)),
                    ("inversion: divided by the fraction", F_(N * b, a)),
                    ("place-value: x10", F_(a * N, b) * 10), ("place-value: /10", F_(a * N, b) / 10)]
            if b <= 9:
                out.append(("denominator-as-decimal: N x b/10", F_(N * b, 10)))
        elif k == "ofamt-p":
            pc, N = it["p"], it["N"]
            out += [("subtract-percent: N - p", F_(N - pc)),
                    ("one-part-only: 10% only (N/10)", F_(N, 10)),
                    ("complement: the part left over", F_(N * (100 - pc), 100)),
                    ("inversion: N divided by p%", F_(100 * N, pc)),
                    ("place-value: x10", F_(pc * N, 100) * 10), ("place-value: /10", F_(pc * N, 100) / 10)]
        else:   # outof-f, outof-p
            A, B = it["A"], it["B"]
            out += [("inversion: the whole over the part", F_(B, A)),
                    ("part-to-part: the part over the rest", F_(A, B - A)),
                    ("complement: the rest over the whole", F_(B - A, B))]
            if k == "outof-p":
                out += [("raw-part: the part as the percentage (A%)", F_(A, 100)),
                        ("place-value: x10", F_(A, B) * 10), ("place-value: /10", F_(A, B) / 10)]
        return out
    def ans_of(it):
        a = it["answer"]
        if a["form"] == "f" and it["asksSimplest"]:
            return tuple(a["shown"] or a["value"])
        return F_(*a["value"])
    def as_key(it, m):
        if isinstance(m, tuple):          # a shown fraction (simplest-form questions)
            return m if it["asksSimplest"] else F_(*m)
        if it["answer"]["form"] == "f" and it["asksSimplest"]:
            return (m.numerator, m.denominator)
        return m
    results = []
    for stage in (1, 2, 3, 4):
        items = [it for it in bank if it["stage"] == stage]
        r = Result("free-daily-pizza", "stage %d" % stage, "%d items (the whole bank)" % len(items),
                   "enumerated (FDP.BANK, built by FDP.buildBank from its parameter lists)",
                   "multiple choice, the option's key (form and exact value; a simplest-form fraction by the numbers shown)")
        names = {}
        for it in items:
            for name, m in mis(it):
                names.setdefault(name, [0, []])
                names[name][0] += 1
                if as_key(it, m) == ans_of(it):
                    names[name][1].append(it)
        for name, (applies, hits) in names.items():
            kind = "agree" if name.startswith(("raw-part", "complement", "one-part-only")) else "coincidence"
            # An identity on an of-an-amount item holds at one percentage or fraction for every amount N; the other
            # kinds have no free parameter (the item is its numbers), so they are not grouped.
            uni = [it for it in items if any(n == name for n, _ in mis(it))]
            amt = all(it["kind"] in ("ofamt-p", "ofamt-f") for it in uni)
            r.add(name, applies, hits, lambda h: "%s (offered: %s)" % (h["id"], ", ".join(h["offered"])), kind,
                  group=(lambda it: (it["kind"], it["p"], it["a"], it["b"])) if amt else None, universe=uni,
                  label=lambda g: ("p = %s%%" % g[1] if g[0] == "ofamt-p" else "%s/%s" % (g[2], g[3])) + ", every amount")
        results.append(r)
    return results


# ---------------------------------------------------------------- trig-worms

def survey_trig_worms(pages):
    import mpmath
    mpmath.mp.dps = 50
    ctx, p = pages.page("trig-worms", "typeof questionFrom === 'function' && typeof POOL === 'object'")
    pool = p.evaluate("() => POOL")
    ctx.close()
    D = lambda a: mpmath.radians(a)
    deg = lambda r: mpmath.degrees(r)
    def r1(x):      # half up to 1 d.p., as Math.round(n*10+1e-9)/10 (the nudge only settles exact ties upward)
        return Fraction(int(mpmath.floor(x * 10 + mpmath.mpf("0.5") + mpmath.mpf("1e-30"))), 10)
    def r0(x):
        return int(mpmath.floor(x + mpmath.mpf("0.5") + mpmath.mpf("1e-30")))
    results = []
    for typ in ("angle", "side", "hypotenuse"):
        rows = pool[typ]
        r = Result("trig-worms", "find the %s" % typ, "%d questions (POOL: every angle, hypotenuse and ratio served)" % len(rows),
                   "enumerated (POOL, read from the page)", "multiple choice; angles to the nearest degree, sides to 1 d.p."
                   " (half up), each computed from the sides as shown (1 d.p.)")
        errs = {}
        for angle, hyp, ratio in rows:
            hyp_ = mpmath.mpf(hyp)
            opp, adj = r1(hyp_ * mpmath.sin(D(angle))), r1(hyp_ * mpmath.cos(D(angle)))
            O, A, H = (mpmath.mpf(opp.numerator) / opp.denominator, mpmath.mpf(adj.numerator) / adj.denominator, hyp_)
            where = "%s %d deg, hyp %d, %s" % (typ, angle, hyp, ratio)
            if typ == "angle":
                g1, g2, fn = {"SOH": (O, H, mpmath.asin), "CAH": (A, H, mpmath.acos), "TOA": (O, A, mpmath.atan)}[ratio]
                ratio_v = g1 / g2
                key = r0(deg(fn(ratio_v)))
                cands = [("other inverse: sin<->cos (or sin/cos for tan)", lambda: deg(mpmath.acos(ratio_v)) if ratio == "SOH"
                          else deg(mpmath.asin(ratio_v)) if ratio == "CAH" else deg(mpmath.asin(min(g1, g2) / max(g1, g2)))),
                         ("tan-1 of the ratio (wrong inverse)", lambda: deg(mpmath.atan(ratio_v)) if ratio != "TOA" else None),
                         ("cos-1 instead of tan-1 (of the smaller over the larger)", lambda: deg(mpmath.acos(min(g1, g2) / max(g1, g2)))
                          if ratio == "TOA" else None),
                         ("ratio upside down", lambda: deg(mpmath.atan(1 / ratio_v)) if ratio != "SOH" or True else None),
                         # only where the ratio has more than one decimal place: otherwise rounding it changes nothing
                         ("ratio rounded to 1 d.p. first", lambda: deg(fn(mpmath.mpf(r1(ratio_v).numerator) / r1(ratio_v).denominator))
                          if (abs(r1(ratio_v)) <= 1 or ratio == "TOA") and abs(ratio_v - mpmath.mpf(r1(ratio_v).numerator)
                                                                             / r1(ratio_v).denominator) > mpmath.mpf("1e-40") else None),
                         ("the other angle: 90 - theta", lambda: 90 - deg(fn(ratio_v))),
                         ("calculator in radians (radians read as degrees)", lambda: fn(ratio_v))]
                for name, f in cands:
                    v = f()
                    if v is None:
                        continue
                    q = (ratio, angle, hyp, "%s: key %d deg" % (where, key))
                    errs.setdefault(name, [[], []])
                    errs[name][0].append(q)
                    if r0(v) == key and name != "calculator in radians (radians read as degrees)":
                        errs[name][1].append(q)
                    elif name == "calculator in radians (radians read as degrees)" and r1(v * 10) / 10 == key:
                        errs[name][1].append(q)
            else:
                if typ == "side":
                    fn = mpmath.sin if ratio == "SOH" else mpmath.cos
                    key = r1(H * fn(D(angle)))
                    other = mpmath.cos if ratio == "SOH" else mpmath.sin
                    cands = [("the other ratio (sin<->cos)", H * other(D(angle))), ("tan instead", H * mpmath.tan(D(angle))),
                             ("divided instead of multiplied", H / fn(D(angle))),
                             ("calculator in radians", H * fn(mpmath.mpf(angle)))]
                else:
                    key = r1(O / mpmath.sin(D(angle)))
                    cands = [("multiplied instead of divided", O * mpmath.sin(D(angle))), ("cos instead of sin", O / mpmath.cos(D(angle))),
                             ("tan instead of sin", O / mpmath.tan(D(angle))), ("calculator in radians", O / mpmath.sin(mpmath.mpf(angle)))]
                for name, v in cands:
                    q = (ratio, angle, hyp, "%s: key %s" % (where, float(key)))
                    errs.setdefault(name, [[], []])
                    errs[name][0].append(q)
                    if r1(v) == key:
                        errs[name][1].append(q)
        # Classed by the error's type, never grouped (Jon's ruling (2), 20 Oct 2026): rounding the ratio before the
        # inverse is a precision slip ('agree (precision)'; where it changes the degree the student is already
        # marked wrong); a wrong function or the ratio upside down landing on the key is a coincidence, even where
        # it does so for every hypotenuse at one angle (cos 80 and 85 deg upside down).
        for name, (uni, hits) in errs.items():
            r.add(name, len(uni), hits, lambda h: h[3], "agree (precision)" if name.startswith("ratio rounded") else "coincidence")
        results.append(r)
    return results


# ---------------------------------------------------------------- distinctly-average

def survey_distinctly_average(pages):
    ctx, p = pages.page("distinctly-average", "!!window.DA_ITEMS")
    items = p.evaluate("() => window.DA_ITEMS.gcse")     # gcse = every ks3 item plus the GCSE-only ones
    ctx.close()
    def f1(x):           # a value as the game shows it: a whole number, or 1 d.p. half up
        x = round_half_up(Fraction(x), 1)
        return str(x.numerator) if x.denominator == 1 else "%.1f" % float(x)
    def half(x):
        x = Fraction(x)
        return str(x.numerator) if x.denominator == 1 else "%d.5" % math.floor(x)
    def median(v):
        s = sorted(v); n = len(s)
        return Fraction(s[n // 2]) if n % 2 else Fraction(s[n // 2 - 1] + s[n // 2], 2)
    def modes(v):
        c = {x: v.count(x) for x in v}; top = max(c.values())
        return sorted(x for x in c if c[x] == top), top
    def pair(a, b):
        return "%d and %d" % (min(a, b), max(a, b))
    errs = {}
    def test(cat, name, applies, hit, it, kind="coincidence"):
        e = errs.setdefault(cat, {}).setdefault(name, [0, [], kind])
        if applies:
            e[0] += 1
            if hit:
                e[1].append("%s: data %s, key %s" % (it["id"], json.dumps(it["data"])[:60], it["correct"]))
    for it in items:
        cat, d, key = it["cat"], it["data"], it["correct"]
        if cat in ("mean", "median", "modeUnique", "modeBimodal", "range"):
            v, n = d, len(d)
            s = sum(v); md, mt = modes(v)
            mid = d[(n - 1) // 2] if n % 2 else None
            if cat == "mean":
                test(cat, "the total, not divided", True, str(s) == key, it)
                test(cat, "divided by n - 1", True, f1(Fraction(s, n - 1)) == key, it)
                test(cat, "divided by n + 1", True, f1(Fraction(s, n + 1)) == key, it)
                test(cat, "the median instead of the mean", True, half(median(v)) == key, it, "agree")
                test(cat, "the mode instead of the mean", len(md) == 1, len(md) == 1 and str(md[0]) == key, it, "agree")
                test(cat, "the largest value", True, str(max(v)) == key, it)
            elif cat == "median":
                srt = sorted(v)
                um = d[n // 2] if n % 2 else Fraction(d[n // 2 - 1] + d[n // 2], 2)
                test(cat, "middle of the list as given (not sorted)", True, half(um) == key, it)
                test(cat, "the position (n+1)/2, not the value", True, half(Fraction(n + 1, 2)) == key, it)
                test(cat, "the mean instead of the median", True, f1(Fraction(s, n)) == key, it, "agree")
                test(cat, "one of the two middle values (even n)", n % 2 == 0,
                     n % 2 == 0 and key in (str(srt[n // 2 - 1]), str(srt[n // 2])), it, "agree")
                test(cat, "the mode instead of the median", len(md) == 1, len(md) == 1 and str(md[0]) == key, it, "agree")
            elif cat == "modeUnique":
                test(cat, "the frequency, not the value", True, str(mt) == key, it)
                test(cat, "the largest value", True, str(max(v)) == key, it)
                test(cat, "the smallest value", True, str(min(v)) == key, it)
                test(cat, "the median instead of the mode", True, half(median(v)) == key, it, "agree")
                test(cat, "the mean instead of the mode", True, f1(Fraction(s, n)) == key, it, "agree")
            elif cat == "modeBimodal":
                distinct = sorted(set(v))
                test(cat, "the two largest values", True, pair(distinct[-1], distinct[-2]) == key, it)
                test(cat, "the two smallest values", True, pair(distinct[0], distinct[1]) == key, it)
            else:
                test(cat, "the largest value", True, str(max(v)) == key, it)
                test(cat, "the smallest value", True, str(min(v)) == key, it)
                test(cat, "the mean instead of the range", True, f1(Fraction(s, n)) == key, it)
                test(cat, "last minus first, in the order given", True, str(abs(d[-1] - d[0])) == key, it, "agree")
        elif cat in ("freqMean", "freqMedian"):
            vals, fr = d["values"], d["freqs"]
            N = sum(fr); fx = sum(a * b for a, b in zip(vals, fr))
            full = [a for a, b in zip(vals, fr) for _ in range(b)]
            if cat == "freqMean":
                test(cat, "ignored the frequencies (mean of the values)", True, f1(Fraction(sum(vals), len(vals))) == key, it)
                test(cat, "sum of fx, not divided", True, f1(fx) == key, it)
                test(cat, "divided by the number of rows", True, f1(Fraction(fx, len(vals))) == key, it)
                test(cat, "mean of the frequencies", True, f1(Fraction(N, len(vals))) == key, it)
                test(cat, "the median instead of the mean", True, half(median(full)) == key, it, "agree")
                test(cat, "the modal value instead of the mean", True, str(vals[fr.index(max(fr))]) == key and fr.count(max(fr)) == 1, it, "agree")
            else:
                test(cat, "the middle row's value (ignored the frequencies)", True,
                     half(median(vals)) == key, it, "agree")
                test(cat, "the position (n+1)/2, not the value", True, half(Fraction(N + 1, 2)) == key, it)
                test(cat, "the mean instead of the median", True, f1(Fraction(fx, N)) == key, it, "agree")
                test(cat, "the modal value instead of the median", fr.count(max(fr)) == 1,
                     fr.count(max(fr)) == 1 and str(vals[fr.index(max(fr))]) == key, it, "agree")
        elif cat == "missing":
            mean = Fraction(it["meanStr"]); n = it["n"]; s = sum(d)
            test(cat, "the mean itself", True, f1(mean) == key, it, "agree")
            test(cat, "the total of the known values", True, str(s) == key, it)
            test(cat, "mean x (n - 1) minus the knowns", True, f1(mean * (n - 1) - s) == key, it)
            test(cat, "mean x n (the total, not less the knowns)", True, f1(mean * n) == key, it)
        elif cat == "compareMean":
            a, b = d["a"], d["b"]
            def which(x, y):
                return "A" if x > y else "B" if y > x else "They are the same"
            test(cat, "compared the medians", True, which(median(a), median(b)) == key, it, "agree")
            test(cat, "compared the totals", True, which(sum(a), sum(b)) == key, it, "agree")
            test(cat, "compared the largest values", True, which(max(a), max(b)) == key, it, "agree")
        elif cat == "compareRange":
            a, b = d["a"], d["b"]
            ra, rb = max(a) - min(a), max(b) - min(b)
            test(cat, "picked the bigger range", True, ("A" if ra > rb else "B" if rb > ra else "They are the same") == key, it, "agree")
            test(cat, "compared the means (lower = more consistent)", True,
                 ("A" if sum(a) < sum(b) else "B" if sum(b) < sum(a) else "They are the same") == key, it, "agree")
        elif cat == "outlierId":
            test(cat, "picked the largest value", True, str(max(d)) == key, it, "agree")
            test(cat, "picked the smallest value", True, str(min(d)) == key, it, "agree")
        # outlierMean and outlierCompare: three worded options about the mean and the median; their errors are the
        # game's own named ones (mean_unaffected, mean_direction_reversed, mean_thought_robust, ...), each a different
        # word from the key by construction, so they cannot coincide with it. Not recomputed here.
    results = []
    for cat, es in errs.items():
        n_items = len([it for it in items if it["cat"] == cat])
        r = Result("distinctly-average", cat, "%d items (the whole pool, KS3 and GCSE)" % n_items,
                   "enumerated (window.DA_ITEMS: the items the page itself builds)", "multiple choice, by dataset.val string")
        for name, (applies, hits, kind) in es.items():
            r.add(name, applies, hits, lambda h: h, kind)
        results.append(r)
    r = Result("distinctly-average", "outlierMean, outlierCompare", "%d items" % len([it for it in items if it["cat"] in
               ("outlierMean", "outlierCompare")]), "enumerated (window.DA_ITEMS)", "multiple choice, worded options")
    r.notes.append("not recomputed: three worded options, each wrong one a named error that is a different word from the key")
    results.append(r)
    return results


# ---------------------------------------------------------------- quadratic-factoriser

def survey_quadratic_factoriser(pages):
    import mpmath
    mpmath.mp.dps = 50
    ctx, p = pages.page("quadratic-factoriser", "!!window.QF_POOLS && !!QF_POOLS.formula && !!QF_POOLS.higher")
    pools = p.evaluate("() => ({ gcse: QF_POOLS.gcse.pool, higher: QF_POOLS.higher.pool, formula: QF_POOLS.formula.pool })")
    ctx.close()
    results = []
    # gcse: x^2 + bx + c = (x + p)(x + q); the answer is the pair {p, q}, in either order, picked from -12..12
    g = pools["gcse"]
    r = Result("quadratic-factoriser", "GCSE, x^2 + bx + c = (x + p)(x + q)", "%d questions (the whole pool)" % len(g),
               "enumerated (QF_POOLS.gcse)", "the pair p, q picked from a grid, exact, either order")
    key = lambda it: sorted([it["p"], it["q"]])
    r.add("signs flipped: the roots, not the factors (-p, -q)", len(g), [it for it in g if sorted([-it["p"], -it["q"]]) == key(it)],
          lambda h: "x^2 %+dx %+d = (x %+d)(x %+d)" % (h["b"], h["c"], h["p"], h["q"]), "agree")
    def sum_prod_swapped(it):      # p + q = c and pq = b: the integer pair, if any
        out = []
        for a in range(-12, 13):
            for b in range(a, 13):
                if a + b == it["c"] and a * b == it["b"]:
                    out.append([a, b])
        return out
    r.add("sum and product swapped (p + q = c, pq = b)", len(g), [it for it in g if key(it) in sum_prod_swapped(it)],
          lambda h: "x^2 %+dx %+d = (x %+d)(x %+d)" % (h["b"], h["c"], h["p"], h["q"]))
    results.append(r)
    # higher: ax^2 + bx + c = (px + q)(rx + s), the HCF stage k(px + q)(rx + s)
    h = pools["higher"]
    r = Result("quadratic-factoriser", "GCSE Higher, ax^2 + bx + c", "%d questions (the whole pool, base and HCF)" % len(h),
               "enumerated (QF_POOLS.higher)", "guided steps (multiple choice), then the factors")
    def same(f1, f2):
        return sorted(map(tuple, f1)) == sorted(map(tuple, f2))
    kf = lambda it: [(it["p"], it["q"]), (it["r"], it["s"])]
    r.add("the two constants swapped: (px + s)(rx + q)", len(h), [it for it in h if same([(it["p"], it["s"]), (it["r"], it["q"])], kf(it))],
          lambda x: "%dx^2 %+dx %+d = (%dx %+d)(%dx %+d)" % (x["a"], x["b"], x["c"], x["p"], x["q"], x["r"], x["s"]), "agree")
    r.add("both signs flipped: (px - q)(rx - s)", len(h), [it for it in h if same([(it["p"], -it["q"]), (it["r"], -it["s"])], kf(it))],
          lambda x: "(%dx %+d)(%dx %+d)" % (x["p"], x["q"], x["r"], x["s"]))
    base = [it for it in h if it["stage"] == "base"]
    # Each is grouped by the two coefficients its comparison with ac turns on, so an identity holds for every value
    # of the third: a x b = ac turns on b and c (a cancels), b x c on a and b (c cancels), a + c and a - c on a and c.
    by = {"b, c": lambda it: ("b, c", it["b"], it["c"]), "a, b": lambda it: ("a, b", it["a"], it["b"]),
          "a, c": lambda it: ("a, c", it["a"], it["c"])}
    free = {"b, c": "a", "a, b": "c", "a, c": "b"}
    for name, f, kind, g in (("step 2 (find ac): a x b", lambda a, b, c: a * b, "coincidence", "b, c"),
                             ("step 2 (find ac): b x c", lambda a, b, c: b * c, "coincidence", "a, b"),
                             ("step 2 (find ac): a + c", lambda a, b, c: a + c, "coincidence", "a, c"),
                             ("step 2 (find ac): a - c", lambda a, b, c: a - c, "coincidence", "a, c")):
        r.add(name, len(base), [it for it in base if f(it["a"], it["b"], it["c"]) == it["a"] * it["c"]],
              lambda x: "%dx^2 %+dx %+d: ac = %d" % (x["a"], x["b"], x["c"], x["a"] * x["c"]), kind,
              group=by[g], universe=base, label=lambda k: "%s = %d, %d, every %s" % (k[0], k[1], k[2], free[k[0]]))
    results.append(r)
    # formula: two typed roots, each rounded with round2 = Math.round(x*100)/100 (half up, towards +infinity), either order
    f = pools["formula"]
    def rnd2(x):
        return int(mpmath.floor(x * 100 + mpmath.mpf("0.5")))
    def roots(a, b, c, disc, div):
        if disc < 0:
            return None
        sq = mpmath.sqrt(disc)
        return sorted([rnd2((-b + sq) / div), rnd2((-b - sq) / div)])
    r = Result("quadratic-factoriser", "the quadratic formula", "%d questions (the whole pool: %d real, %d no real roots)"
               % (len(f), sum(1 for x in f if not x["noReal"]), sum(1 for x in f if x["noReal"])),
               "enumerated (QF_POOLS.formula)", "two typed roots, each round2 (2 d.p., Math.round), either order; or 'No real "
               "solutions'")
    def key_of(it):
        return "none" if it["noReal"] else roots(it["a"], it["b"], it["c"], it["b"] ** 2 - 4 * it["a"] * it["c"], 2 * it["a"])
    def err_of(name, it):
        a, b, c = it["a"], it["b"], it["c"]
        d = b * b - 4 * a * c
        if name.startswith("+b"):
            v = None if d < 0 else sorted([rnd2((b + mpmath.sqrt(d)) / (2 * a)), rnd2((b - mpmath.sqrt(d)) / (2 * a))])
        elif name.startswith("only"):
            v = None if d < 0 else sorted([rnd2(-b + mpmath.sqrt(d) / (2 * a)), rnd2(-b - mpmath.sqrt(d) / (2 * a))])
        elif name.startswith("divided by a"):
            v = roots(a, b, c, d, a)
        elif name.startswith("b^2 taken"):
            v = roots(a, b, c, -b * b - 4 * a * c, 2 * a)
        else:    # b^2 + 4ac
            v = roots(a, b, c, b * b + 4 * a * c, 2 * a)
        return "none" if v is None else v
    names = ("+b instead of -b (the game's own diagnosis)", "only the square root divided by 2a (the game's own diagnosis)",
             "divided by a, not 2a (the game's own diagnosis)", "b^2 taken as negative (the game's own diagnosis)",
             "b^2 + 4ac (sign of 4ac slipped)")
    real, none_ = [it for it in f if not it["noReal"]], [it for it in f if it["noReal"]]
    for name in names:
        r.add(name + ", real roots", len(real), [it for it in real if err_of(name, it) == key_of(it)],
              lambda x: "%dx^2 %+dx %+d: key %s" % (x["a"], x["b"], x["c"], [k / 100 for k in key_of(x)]))
    for name in names:
        # On a no-real-roots item an error that leaves b^2 - 4ac negative still ends at 'No real solutions'.
        r.add(name + ", no real roots", len(none_), [it for it in none_ if err_of(name, it) == "none"],
              lambda x: "%dx^2 %+dx %+d: no real roots" % (x["a"], x["b"], x["c"]), "agree")
    results.append(r)
    return results


# ---------------------------------------------------------------- modular-battle

def survey_modular_battle(pages):
    ctx, p = pages.page("modular-battle", "typeof generateQ === 'function' && typeof randInt === 'function'")
    e = p.evaluate(ENUM_JS, ["randInt", "generateQ()", 6])
    ctx.close()
    return [modular_result(e["questions"], "%d questions (%d paths walked)" % (len(e["questions"]), e["paths"]))]


def modular_result(qs, space):
    """The four errors for a mod b. The game offers residues 0..b-1 only, so an error applies to a question when
    its value is one of them (a value outside that range cannot be picked, so it cannot be marked right). Each is
    grouped by b: an error that gives the key for every question with that b is an identity there."""
    r = Result("modular-battle", "a mod b", space, "enumerated (generateQ driven through every randInt choice)",
               "multiple choice of residues 0..b-1 (random others, none named); exact")
    r.notes.append("accepted, not filtered (Jon's ruling (3), 20 Oct 2026): the coincidences left are 7.5% per error per "
                   "question (123 / (4 x 408)), below the 1 in 9 at which a random residue hits the key at b = 9, so no "
                   "method beats guessing; filtering would remove about 30% of the questions and teach that b/2 is never "
                   "the answer")
    ex = lambda h: "%d mod %d: key %d" % (h["a"], h["b"], h["ans"])
    def dec_digit(q):
        fr = Fraction(q["a"], q["b"]) - q["a"] // q["b"]
        return None if fr == 0 else int(fr * 10)
    errs = (("the quotient instead of the remainder", lambda q: q["a"] // q["b"]),
            ("b - r (counted the other way)", lambda q: q["b"] - q["ans"]),
            ("the last digit of a", lambda q: q["a"] % 10),
            ("the first digit after the point of a / b", dec_digit))
    for name, f in errs:
        uni = [q for q in qs if f(q) is not None and 0 <= f(q) < q["b"]]
        r.add(name, len(uni), [q for q in uni if f(q) == q["ans"]], ex,
              group=lambda q: q["b"], universe=uni, label=lambda g: "b = %d" % g)
    return r


# ---------------------------------------------------------------- factor-race and fraction-equivalence (two-way)

def survey_factor_race(pages):
    ctx, p = pages.page("factor-race", "typeof VALID_PAIRS === 'object'", "?level=ks3")
    pairs = p.evaluate("() => VALID_PAIRS")
    ctx.close()
    nf = lambda n: sum(1 for k in range(1, n + 1) if n % k == 0)
    r = Result("factor-race", "KS3/GCSE pairs", "%d ordered pairs (VALID_PAIRS)" % len(pairs), "enumerated (VALID_PAIRS)",
               "two cards: which has more factors (exact counts)")
    key = lambda a, b: a if nf(a) > nf(b) else b
    r.add("the bigger number has more factors", len(pairs), [x for x in pairs if max(x) == key(*x)],
          lambda x: "%d v %d" % tuple(x), "two-way")
    par = [x for x in pairs if (x[0] % 2) != (x[1] % 2)]
    r.add("the even number has more factors (pairs of mixed parity)", len(par),
          [x for x in par if (x[0] if x[0] % 2 == 0 else x[1]) == key(*x)], lambda x: "%d v %d" % tuple(x), "two-way")
    return [r]


def survey_fraction_equivalence(pages):
    ctx, p = pages.page("fraction-equivalence", "typeof generateQ === 'function' && typeof randInt === 'function'")
    e = p.evaluate(ENUM_JS, ["randInt", "generateQ()", 12])
    ctx.close()
    qs = e["questions"]
    r = Result("fraction-equivalence", "KS3/GCSE", "%d distinct questions (%d paths walked)" % (len(qs), e["paths"]),
               "enumerated (generateQ driven through every randInt and Math.random choice)", "Yes / No: equivalent?")
    say = lambda q, yes: q["equiv"] == yes
    r.add("additive: equivalent when top and bottom differ by the same amount", len(qs),
          [q for q in qs if say(q, q["d2"] - q["n2"] == q["d1"] - q["n1"])],
          lambda q: "%d/%d v %d/%d: key %s" % (q["n1"], q["d1"], q["n2"], q["d2"], q["equiv"]), "two-way")
    r.add("only the tops checked (numerator a multiple: always yes)", len(qs), [q for q in qs if say(q, q["n2"] % q["n1"] == 0)],
          lambda q: "%d/%d v %d/%d" % (q["n1"], q["d1"], q["n2"], q["d2"]), "two-way")
    return [r]


# ---------------------------------------------------------------- bearing-blitz

def survey_bearing_blitz(pages):
    ctx, p = pages.page("bearing-blitz", "typeof generateBearings === 'function'")
    fixed = p.evaluate("""() => { const real = Math.random; Math.random = () => 0; try { generateBearings(); }
      finally { Math.random = real; } return bearings.slice(0, 16).sort((a, b) => a - b).concat(['random', TOLERANCE]); }""")
    ctx.close()
    tol = fixed[-1]
    every = list(range(360))
    near = lambda x, y: min((x - y) % 360, (y - x) % 360) <= tol
    errs = [("anticlockwise from north (360 - b)", lambda b: (360 - b) % 360, "agree"),
            ("the back bearing (b + 180)", lambda b: (b + 180) % 360, "coincidence"),
            ("the maths angle: anticlockwise from east (90 - b)", lambda b: (90 - b) % 360, "agree"),
            ("clockwise from east (b - 90)", lambda b: (b - 90) % 360, "coincidence")]
    out = []
    from_page = sorted(set(fixed[:16]))
    for part, space in (("the 16 fixed bearings (in every game)", from_page), ("every bearing 0-359 (the 8 random ones per game)", every)):
        r = Result("bearing-blitz", part, "%d bearings" % len(space), "enumerated (generateBearings' fixed list read from the "
                   "page; the random ones are Math.floor(Math.random()*360))", "needle within %d degrees (TOLERANCE)" % tol)
        for name, f, kind in errs:
            r.add(name, len(space), [b for b in space if near(f(b), b)], lambda b: "target %03d" % b, kind)
        out.append(r)
    return out


# ---------------------------------------------------------------- shape-shifter (rotation)

def survey_shape_shifter(pages):
    ctx, p = pages.page("shape-shifter", "typeof ROTATION_QUESTIONS === 'object'")
    qs = p.evaluate("() => ROTATION_QUESTIONS")
    ctx.close()
    def rot(sh, cx, cy, ang):
        out = []
        for x, y in sh:
            dx, dy = x - cx, y - cy
            if ang % 360 == 90:
                out.append((cx - dy, cy + dx))
            elif ang % 360 == 270:
                out.append((cx + dy, cy - dx))
            else:
                out.append((cx - dx, cy - dy))
        return sorted(out)
    key = lambda q: sorted(map(tuple, q["correct"]))
    r = Result("shape-shifter", "Rotation", "%d questions (ROTATION_QUESTIONS, built once at load)" % len(qs),
               "enumerated", "multiple choice of 4 shapes (named-error options)")
    ex = lambda q: q["desc"] + " " + json.dumps(q["shape"])
    tests = [("wrong direction (-angle)", lambda q: rot(q["shape"], q["cx"], q["cy"], -q["angle"])),
             ("reflected in the y-axis", lambda q: sorted((-x, y) for x, y in q["shape"])),
             ("reflected in the x-axis", lambda q: sorted((x, -y) for x, y in q["shape"])),
             ("wrong centre (1, 1)", lambda q: rot(q["shape"], 1, 1, q["angle"])),
             ("90 for 180, or 180 for 90", lambda q: rot(q["shape"], q["cx"], q["cy"], 180 if abs(q["angle"]) == 90 else 90))]
    for name, f in tests:
        r.add(name, len(qs), [q for q in qs if f(q) == key(q)], ex)
    return [r]


# ---------------------------------------------------------------- equatle

def survey_equatle(pages):
    ctx, p = pages.page("equatle", "typeof getBank === 'function'")
    bank = p.evaluate("() => getBank()")
    ctx.close()
    def tokens(lhs):
        return re.findall(r"\d+|[+\-*/]", lhs)
    def ltr(tok):
        v = Fraction(int(tok[0]))
        for i in range(1, len(tok), 2):
            o, x = tok[i], Fraction(int(tok[i + 1]))
            v = v + x if o == "+" else v - x if o == "-" else v * x if o == "*" else (v / x if x else None)
            if v is None:
                return None
        return v
    mixed = []
    for eq in bank:
        lhs, rhs = eq.split("=")
        tok = tokens(lhs)
        ops = tok[1::2]
        if any(o in "+-" for o in ops) and any(o in "*/" for o in ops):
            mixed.append((eq, tok, int(rhs)))
    r = Result("equatle", "the equation bank", "%d equations (getBank(); %d mix + or - with x or /)" % (len(bank), len(mixed)),
               "enumerated (getBank)", "the guess must be a true equation (JavaScript precedence) and the exact target string")
    r.add("left to right, ignoring x and / first (mixed-operation equations)", len(mixed),
          [m for m in mixed if ltr(m[1]) == m[2]], lambda m: m[0], "agree")
    return [r]


# ---------------------------------------------------------------- log-laws (Solve mode)

def survey_log_laws(pages):
    import mpmath
    mpmath.mp.dps = 50
    ctx, p = pages.page("log-laws", "!!window.LL_SOLVE && !!LL_SOLVE.families")
    fams = p.evaluate("() => LL_SOLVE.families.map(f => ({ id: f.id, items: f.items.map(i => ({ id: i.id, answer: i.answer, "
                      "mis: i.mis.map(m => ({ id: m.id, v: m.v })) })) }))")
    ctx.close()
    ln, lg = mpmath.log, mpmath.log10
    M = mpmath.mpf
    def num(s):                          # an id's number: '2', '-2', '2.2', or a tex fraction
        m = re.match(r"\\dfrac\{(\d+)\}\{(\d+)\}", s)
        return M(int(m.group(1))) / int(m.group(2)) if m else M(s)
    def s3(v):                           # to 3 s.f., half up (Number(v.toPrecision(3)))
        return sig3(Fraction(mpmath.nstr(v, 40, min_fixed=-100, max_fixed=100)))
    results = []
    for f in fams:
        if f["id"] == "F5":
            r = Result("log-laws", "Solve, F5 (product law)", "%d items" % len(f["items"]), "enumerated (LL_SOLVE.families)",
                       "multiple choice: x = r, x = -s or both")
            r.notes.append("not recomputed: the three options are different roots or 'both'; the game's own misRoot (keeping the "
                           "negative root) is the option 'both' or x = -s, never the key")
            results.append(r)
            continue
        r = Result("log-laws", "Solve, %s" % f["id"], "%d items (the whole family)" % len(f["items"]),
                   "enumerated (LL_SOLVE.families, built from parameter lists; no random draw)",
                   "typed, to 3 significant figures (an unrounded value is a format notice, not marked)")
        errs = {}
        def hit(name, it, v, kind="coincidence"):
            name = name if kind == "coincidence" else name + " [where it is the same calculation]"
            e = errs.setdefault(name, [0, [], kind])
            if v is None:
                return
            e[0] += 1
            if s3(v) == s3(M(it["answer"])):
                e[1].append("%s: key %s" % (it["id"], float(s3(M(it["answer"])))))
        for it in f["items"]:
            # The game's own diagnosed errors (misDivide, misK), recomputed from their definitions (log-laws
            # index.html, misDivide and the misK lines of buildF1-buildF3), not read from it.mis: the page drops a
            # misconception from it.mis when it rounds to the answer, which is exactly the case this survey counts.
            parts = it["id"].split("-")
            if f["id"] == "F1":
                a, b = M(parts[1]), M(parts[2])
                hit("the game's own misDivide: log(b/a) (base 10)", it, lg(b / a))
                hit("the game's own misDivide: ln(b/a)", it, ln(b / a))
                hit("ratio upside down: log a / log b", it, ln(a) / ln(b))
                hit("no logs: b / a", it, b / a)
                hit("log for ln, mixed: log b / ln a", it, lg(b) / ln(a))
                hit("subtracted the logs: log b - log a", it, lg(b) - lg(a))
            elif f["id"] == "F2" and parts[1] == "kx":
                a, k, b = M(parts[2]), M(parts[3]), M(parts[4])
                hit("the game's own misDivide: log(b/a) / k (base 10)", it, lg(b / a) / k)
                hit("the game's own misDivide: ln(b/a) / k", it, ln(b / a) / k)
                hit("the game's own misK: k left out", it, ln(b) / ln(a))
                hit("multiplied by k instead of dividing", it, k * ln(b) / ln(a))
                hit("ratio upside down: k log a / log b", it, k * ln(a) / ln(b))
                hit("log for ln, mixed: log b / (k ln a)", it, lg(b) / (k * ln(a)))
            elif f["id"] == "F2":
                m_ = re.match(r"F2-shift-(\d+)-(-?\d+)-(\d+)$", it["id"])
                a, k, b = M(m_.group(1)), M(m_.group(2)), M(m_.group(3))
                hit("the game's own misDivide: log(b/a) - k (base 10)", it, lg(b / a) - k)
                hit("the game's own misDivide: ln(b/a) - k", it, ln(b / a) - k)
                hit("the game's own misK: the shift left out", it, ln(b) / ln(a))
                hit("the shift's sign slipped (+k for -k)", it, ln(b) / ln(a) + k)
                hit("ratio upside down, then the shift", it, ln(a) / ln(b) - k)
            elif f["id"] == "F3" and parts[1] == "e":
                m_ = re.match(r"F3-e-(-?\d+)-(.*)$", it["id"])
                k, b = M(m_.group(1)), num(m_.group(2))
                hit("the game's own misK: k left out (ln b)", it, ln(b), "agree" if k == 1 else "coincidence")
                hit("multiplied by k instead of dividing", it, k * ln(b), "agree" if abs(k) == 1 else "coincidence")
                hit("log for ln: log b / k", it, lg(b) / k)
                if k < 0:
                    hit("the sign of k dropped (k negative)", it, ln(b) / abs(k))
            elif f["id"] == "F3":
                m_ = re.match(r"F3-rc-(\d+)-(.+)-(.+)-(\d+)$", it["id"])
                V0, Vn, R, C = M(m_.group(1)), num(m_.group(2)), num(m_.group(3)), M(m_.group(4))
                RC = R * C / 1000
                hit("the game's own misK: the time constant left out (-ln(V/V0))", it, -ln(Vn / V0),
                    "agree" if RC == 1 else "coincidence")
                hit("the minus sign dropped: RC ln(V/V0)", it, RC * ln(Vn / V0))
                hit("log for ln: -RC log(V/V0)", it, -RC * lg(Vn / V0))
                hit("RC taken as R x C without the powers of ten", it, -R * C * ln(Vn / V0))
            elif f["id"] == "F4":
                a, b = M(parts[2]), M(parts[3])
                hit("the -1 dropped: x = a / b", it, a / b)
                hit("multiplied instead of divided: x = a(b - 1)", it, a * (b - 1), "agree" if b == 2 else "coincidence")
                hit("the quotient upside down: x/(x + a) = b", it, a * b / (1 - b))
            elif f["id"] == "F6":
                a, b, k = M(parts[1]), M(parts[2]), M(parts[3])
                key = k * ln(b) / (ln(b) - ln(a))
                hit("a sign slipped (the answer's sign)", it, -key)
                hit("k dropped", it, ln(b) / (ln(b) - ln(a)), "agree" if k == 1 else "coincidence")
                hit("ln a + ln b in the denominator", it, k * ln(b) / (ln(b) + ln(a)))
                hit("ln(a/b) read as ln a / ln b", it, -k * ln(b) / (ln(a) / ln(b)))
        for name, (applies, hits, kind) in errs.items():
            r.add(name, applies, hits, lambda h: h, kind)
        results.append(r)
    return results


SURVEYS = {
    "just-pythag-it-bruv": survey_jpib,
    "six-sevens-bruv": survey_ssb,
    "split-it": survey_split_it,
    "free-daily-pizza": survey_fdp,
    "trig-worms": survey_trig_worms,
    "distinctly-average": survey_distinctly_average,
    "quadratic-factoriser": survey_quadratic_factoriser,
    "modular-battle": survey_modular_battle,
    "factor-race": survey_factor_race,
    "fraction-equivalence": survey_fraction_equivalence,
    "bearing-blitz": survey_bearing_blitz,
    "shape-shifter": survey_shape_shifter,
    "equatle": survey_equatle,
    "log-laws": survey_log_laws,
    "how-many-parts": survey_how_many_parts,
}


def row_of(r, a, b):
    """The kind of the row holding the question a mod b among r's collisions, or None if it collides nowhere."""
    for name, kind, _, _, _ in r.errors:
        if any(q["a"] == a and q["b"] == b for q in r.members[name]):
            yield name, kind


def selftest():
    """Contract COLLISION-IDENTITIES' fixtures: the identity rule on a mod b over generateQ's own ranges (a 10..60,
    b 2..9; no browser needed), trig-worms classed by type (Jon's ruling (2)), and the control, Just Pythag It,
    Bruv, still at 0."""
    qs = [{"a": a, "b": b, "ans": a % b} for a in range(10, 61) for b in range(2, 10)]
    r = modular_result(qs, "fixture")
    want = ((11, 2, "b - r", "agree (identity)"), (13, 5, "the last digit of a", "agree (identity)"),
            (12, 9, "the first digit after the point", "agree (identity)"), (12, 5, "the quotient", "coincidence"))
    bad = 0
    for a, b, err, kind in want:
        got = [k for name, k in row_of(r, a, b) if name.startswith(err)]
        ok = got == [kind]
        bad += not ok
        print("%s %d mod %d / %s -> %s (got %s)" % ("PASS" if ok else "FAIL", a, b, err, kind, got or "no collision"))
    pages = Pages()
    try:
        c = sum(x.collisions for x in survey_jpib(pages))
        tw = [x for x in survey_trig_worms(pages) if x.part == "find the angle"][0]
    finally:
        pages.close()
    # Jon's ruling (2): trig-worms by error type. The upside-down ratio at cos 80 deg holds for every hypotenuse at
    # the nearest degree and is still a coincidence; rounding the ratio first is 'agree (precision)', TOA 65 deg too.
    for ratio, angle, err, kind in (("CAH", 80, "ratio upside down", "coincidence"),
                                    ("TOA", 65, "ratio rounded to 1 d.p. first", "agree (precision)")):
        got = sorted({k for name, k, _, _, _ in tw.errors if name.startswith(err)
                      and any(q[0] == ratio and q[1] == angle for q in tw.members[name])})
        ok = got == [kind]
        bad += not ok
        print("%s trig-worms %s %d deg / %s -> %s (got %s)" % ("PASS" if ok else "FAIL", ratio, angle, err, kind, got or "no collision"))
    print("%s the control, just-pythag-it-bruv: %d collisions (want 0)" % ("PASS" if c == 0 else "FAIL", c))
    bad += c != 0
    print("selftest: %s" % ("PASS" if not bad else "FAIL (%d)" % bad))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", action="append", help="survey only these games")
    ap.add_argument("--json", help="also write the results here")
    ap.add_argument("--selftest", action="store_true", help="run the identity rule's fixtures and the control, then stop")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if args.selftest:
        return selftest()
    listed = listed_games()
    pages = Pages()
    results = []
    try:
        for slug, f in SURVEYS.items():
            if args.game and slug not in args.game:
                continue
            results += f(pages)
    finally:
        pages.close()
    for r in results:
        print("### %s: %s%s" % (r.slug, r.part, "" if r.slug in listed else " (unlisted)"))
        print("- question space: %s; %s" % (r.space, r.method))
        print("- marking: %s" % r.marking)
        print("- collisions with the key: **%d**" % r.collisions)
        print()
        print("| error tested | kind | questions it applies to | collisions |")
        print("|---|---|---|---|")
        for name, kind, applies, n, exs in r.errors:
            print("| %s | %s | %d | %d |" % (name.replace("|", "\\|"), kind, applies, n))
        for name, kind, applies, n, exs in r.errors:
            for e in exs:
                print("  - %s: %s" % (name, e))
        for n in r.notes:
            print("- note: %s" % n)
        print()
    tot = {}
    for r in results:
        c, a, parts, rc, pr = tot.get(r.slug, (0, 0, 0, 0, 0))
        tot[r.slug] = (c + r.by_kind("coincidence"), a + r.by_kind("agree"), parts + 1, rc + r.reclassified,
                       pr + r.precision)
    print("## Headline (this script's output)")
    print()
    print("Before = coincidences as first counted (#458); identities = exact identities, the error equal to the key on every"
          " question of its group; precision = precision slips, by type; both moved to methods agree; after = the"
          " coincidences left.")
    print()
    print("| game | listed | parts surveyed | coincidence before | identities | precision | coincidence after |"
          " methods-agree collisions |")
    print("|---|---|---|---|---|---|---|---|")
    for k, v in tot.items():
        print("| %s | %s | %d | %d | %d | %d | %d | %d |" % (k, "yes" if k in listed else "no", v[2], v[0] + v[3] + v[4],
                                                             v[3], v[4], v[0], v[1]))
    S = lambda i: sum(v[i] for v in tot.values())
    print("| **all** | | %d | **%d** | **%d** | **%d** | **%d** | **%d** |" % (S(2), S(0) + S(3) + S(4), S(3), S(4), S(0), S(1)))
    print()
    print("TOTALS (coincidence before, after; methods agree): " +
          "; ".join("%s %d, %d; %d" % (k, v[0] + v[3] + v[4], v[0], v[1]) for k, v in tot.items()))
    if args.json:
        with open(args.json, "w", encoding="utf-8", newline="") as fh:
            json.dump([r.__dict__ for r in results], fh, indent=1, default=str)
    return 0


if __name__ == "__main__":
    sys.exit(main())
