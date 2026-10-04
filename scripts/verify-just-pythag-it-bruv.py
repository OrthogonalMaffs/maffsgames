#!/usr/bin/env python3
"""Independent verification for Just Pythag It, Bruv (games/just-pythag-it-bruv/), built 4 Oct 2026.

WHY THIS READS THE LIVE PAGE
-------------------------------------------------------------------------------
Same reasoning as verify-six-sevens.py: a Python copy of the game's logic could drift from it and
would then only be verifying itself. The game keeps every decision a student sees -- the order of
question types, every triangle and its drawing, every key, the worked solutions, the "Spotted it?"
line and the add-instead-of-subtract check -- on window.JPIB as plain functions, and its own UI
calls them through JPIB. This script loads the page under Playwright, drives THOSE functions, and
recomputes every answer here, in Python, with exact fractions, from the numbers the page shows.

WHAT IT ASSERTS (Jon's contract, docs/next-contract-just-pythag-it-bruv.md, point 8)
-------------------------------------------------------------------------------
  Sessions    SEEDS sessions (default 300): exactly 20 questions; rounds a (7), b (7), c (6) in
              that order; at least 12 find-a-shorter-side ('short') questions and never three of
              one type in a row; a question's type matches its unknown side.
  Triangles   every side read from the labels the page draws. The hypotenuse is the longest side;
              in the drawing the marked right angle is 90 degrees, at the vertex opposite the side
              labelled as the hypotenuse, and that side is the longest drawn; the legs are drawn in
              their true ratio unless the page says "Not drawn to scale" (and only then); labels
              sit inside the picture, clear of each other and of every side.
  Keys        round 1: the unknown is a whole number, recomputed exactly, no rounding asked; rounds
              2 and 3: never exact, the prompt says "Give your answer to 1 decimal place." and the
              key is the exact value rounded half up (SR-1). The worked solution adds for the
              hypotenuse and subtracts for a shorter side, shows the exact square, and ends on the key.
  Spotted it? round 1 only: a multiple of 3-4-5 or 5-12-13 (found here with gcd) names its sides,
              that base triangle and the scale factor (doubled, tripled, multiplied by k); any
              other triangle has no line (Jon's addendum, 4 Oct 2026).
  Add error   on every 'short' question the add-instead-of-subtract value sits at least 0.1 (1 d.p.)
              or 1 (whole numbers) from the key, so the two never round alike; the page's check
              fires on exactly the probes it should (the add value at 1 d.p., unrounded, and as a
              whole number on a round-1 question) and on nothing else (the key, the key +/- 0.1,
              the hypotenuse, any 'hyp' question); the first three per session get the worked
              example, later ones the nudge.
  Contexts    every number plausible: ladder at 65-80 degrees to the ground, 2.5-7 m long; 16:9 TV
              screens 70-200 cm across the diagonal; ramps 1:15 to 1:20 with a run up to 5 m (the
              ramp is a hypotenuse question only); fields 0.4-1 times as wide as long; roofs pitched
              20-50 degrees, slope 3-6 m. Every given number is in the prompt with its unit; all
              five situations appear in every session; the hypotenuse is drawn in at least three
              different directions in every session's rounds 1 and 2.
  UI          a full session played with the Firebase SDK blocked: the start screen shows
              "Foundation" and "Calculator required"; the page is noindex; a format answer is not
              marked and sends no event; the first three add errors show the worked example (with
              the Next control's fallback timer off), the fourth and fifth the nudge; other wrong
              answers show the worked solution; the four canon 1.3 events carry their parameters
              at level 'ks3'; one score is submitted, to 'ks3', for 20 questions.
  Phone       at 320x568, 375x667 and 390x844, every question shape (all 14 triangles of round 1 as
              both types, both types of round 2, every situation's variants): the feedback for a
              wrong answer (for 'short', the longest: the worked example) keeps Next above the
              footer, the page never scrolls sideways, and triangle labels render at 12px or more
              without overlapping.

FAULT-INJECTION SELF-TEST (runs every time; --no-selftest skips it)
-------------------------------------------------------------------------------
Each fault is patched into a FRESH page at run time (never into the file) and the session checks
must FAIL: keys truncated instead of rounded; the hypotenuse label moved to a leg; the rounds out
of order; a run of three; too few 'short' questions; the add check switched off; the add check
firing on 'hyp' questions; a wrong scale word; a wrong base triple; an implausible ladder; the
right-angle mark at the wrong vertex; the nudge never replacing the worked example.

USAGE
    python scripts/verify-just-pythag-it-bruv.py
    python scripts/verify-just-pythag-it-bruv.py --no-selftest --seeds 50
"""
import argparse
import math
import os
import re
import sys
import time
from fractions import Fraction
from math import gcd, isqrt
from urllib.parse import urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import bank_common as bc  # noqa: E402  (start_stub_server: checked start, free port)

SLUG = "just-pythag-it-bruv"
LEVEL = "ks3"
PORT = None
STAGE_ORDER = ["a"] * 7 + ["b"] * 7 + ["c"] * 6
ROUND_ASK = "Give your answer to 1 decimal place."
SPOT_BASES = {(3, 4, 5): "3-4-5", (5, 12, 13): "5-12-13"}
NUDGE = "Is the side you're finding the longest one?"
PHONES = [(320, 568), (375, 667), (390, 844)]
FOOTER = 40
MIN_LABEL_PX = 12

_FAILURES = []


def fail(msg):
    _FAILURES.append(msg)
    print("FAIL: " + msg)


# ---------------------------------------------------------------- exact arithmetic

def F(s):
    return Fraction(s)


def is_square(x):
    x = Fraction(x)
    n, d = x.numerator, x.denominator
    return n >= 0 and isqrt(n) ** 2 == n and isqrt(d) ** 2 == d


def exact_sqrt(x):
    x = Fraction(x)
    return Fraction(isqrt(x.numerator), isqrt(x.denominator))


def round_sqrt(S, dp):
    """sqrt(S) rounded half up to dp places, S a positive Fraction: the largest K with
    (K - 1/2) <= 10^dp sqrt(S), i.e. (2K - 1)^2 <= 4 * 100^dp * S."""
    T = 4 * S * 10 ** (2 * dp)
    m = isqrt(T.numerator // T.denominator)
    return Fraction((m + 1) // 2, 10 ** dp)


def round_half_up(x, dp):
    x = Fraction(x) * 10 ** dp
    return Fraction(math.floor(x + Fraction(1, 2)), 10 ** dp)


def fmt1(x):
    return "%.1f" % float(x)


NUM = re.compile(r"^\s*[+-]?(\d+(\.\d*)?|\.\d+)\s*$")


def py_mark(q, raw):
    """canon 7.1.3, independently: 'correct' / 'format' / 'wrong' / 'unreadable'."""
    if not NUM.match(raw):
        return "unreadable"
    v, key = F(raw.strip()), F(q["keyText"])
    if v == key:
        return "correct"
    if q["dp"] == 1 and round_half_up(v, 1) == key:
        return "format"
    return "wrong"


def py_is_add(q, raw, add):
    if q["type"] != "short" or py_mark(q, raw) != "wrong":
        return False
    v = F(raw.strip())
    k1 = round_sqrt(add, 1)
    if v == k1 or round_half_up(v, 1) == k1:
        return True
    return q["dp"] == 0 and v == round_sqrt(add, 0)


def angle_deg(opp, adj):
    return math.degrees(math.atan2(float(opp), float(adj)))


# ---------------------------------------------------------------- per-question checks

def sides_of(q):
    """{p, q, r}: Fractions for the given sides, None for the unknown, read from the labels."""
    out = {}
    for lab in q["layout"]["labels"]:
        t = lab["text"]
        if t == "x":
            out[lab["side"]] = None
        else:
            m = re.match(r"^(\d+(?:\.\d+)?) (cm|m|mm)$", t)
            out[lab["side"]] = F(m.group(1)) if m else "BAD:" + t
    return out


def seg_hits_rect(p0, p1, rect):
    """Liang-Barsky: does the segment p0-p1 enter the rectangle (x0, y0, x1, y1)?"""
    x0, y0, x1, y1 = rect
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    t0, t1 = 0.0, 1.0
    for p, qv in ((-dx, p0[0] - x0), (dx, x1 - p0[0]), (-dy, p0[1] - y0), (dy, y1 - p0[1])):
        if p == 0:
            if qv < 0:
                return False
        else:
            t = qv / p
            if p < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                return False
    return True


def check_layout(q, s, out, where):
    L = q["layout"]
    O, A, B = L["O"], L["A"], L["B"]
    va, vb = (A[0] - O[0], A[1] - O[1]), (B[0] - O[0], B[1] - O[1])
    la, lb = math.hypot(*va), math.hypot(*vb)
    lr = math.hypot(B[0] - A[0], B[1] - A[1])
    if abs(va[0] * vb[0] + va[1] * vb[1]) > 1e-6 * la * lb:
        out.append("%s: the drawn angle at the right-angle vertex is not 90 degrees" % where)
    if not (lr > la and lr > lb):
        out.append("%s: the side opposite the right angle is not the longest drawn" % where)
    mk = L["mark"]
    # the mark is a square on the two legs at O: corner 0 on OA, corner 2 on OB, corner 1 = sum
    def on_ray(pt, v, ln):
        w = (pt[0] - O[0], pt[1] - O[1])
        cross = w[0] * v[1] - w[1] * v[0]
        dot = w[0] * v[0] + w[1] * v[1]
        return abs(cross) < 1e-6 * ln * max(1.0, math.hypot(*w)) and 0 < dot < ln * ln
    if not (on_ray(mk[0], va, la) and on_ray(mk[2], vb, lb)
            and abs(mk[1][0] - (mk[0][0] + mk[2][0] - O[0])) < 1e-6
            and abs(mk[1][1] - (mk[0][1] + mk[2][1] - O[1])) < 1e-6):
        out.append("%s: the right-angle mark is not a square on the two legs at the right angle" % where)
    # true ratio, unless (and only if) it says "Not drawn to scale"
    def true_len(k):
        if s[k] is not None:
            return float(s[k])
        return math.sqrt(float(true_unknown_sq(q, s)))
    P, Qn = true_len("p"), true_len("q")
    thin = min(P, Qn) / max(P, Qn) < 0.25
    if bool(L["notToScale"]) != thin:
        out.append("%s: notToScale=%r for legs %.3g and %.3g" % (where, L["notToScale"], P, Qn))
    if not thin and abs(la / lb - P / Qn) > 1e-6 * (P / Qn):
        out.append("%s: legs drawn %.3f:%.3f, true %.3f:%.3f" % (where, la, lb, P, Qn))
    # labels: inside the picture, clear of each other and of every side
    W, H = L["vb"]
    rects = []
    for lab in L["labels"]:
        r = (lab["x"] - lab["w"] / 2, lab["y"] - lab["h"] / 2, lab["x"] + lab["w"] / 2, lab["y"] + lab["h"] / 2)
        rects.append((lab["side"], r))
        if r[0] < 0 or r[1] < 0 or r[2] > W or r[3] > H:
            out.append("%s: label %r is outside the picture" % (where, lab["text"]))
        for p0, p1 in ((O, A), (O, B), (A, B)):
            if seg_hits_rect(p0, p1, r):
                out.append("%s: label %r crosses a side of the triangle" % (where, lab["text"]))
                break
    for i in range(len(rects)):
        for j in range(i + 1, len(rects)):
            a, b = rects[i][1], rects[j][1]
            if a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]:
                out.append("%s: labels for %s and %s overlap" % (where, rects[i][0], rects[j][0]))


def true_unknown_sq(q, s):
    if s["r"] is None:
        return s["p"] ** 2 + s["q"] ** 2
    other = s["q"] if s["p"] is None else s["p"]
    return s["r"] ** 2 - other ** 2


def check_question(q, out, where):
    s = sides_of(q)
    if any(isinstance(v, str) for v in s.values()):
        out.append("%s: unreadable side label %r" % (where, s))
        return None
    unknowns = [k for k in "pqr" if s[k] is None]
    if len(unknowns) != 1:
        out.append("%s: %d sides marked x" % (where, len(unknowns)))
        return None
    u = unknowns[0]
    if (u == "r") != (q["type"] == "hyp"):
        out.append("%s: type %s but the unknown is %s" % (where, q["type"], u))
        return None
    for k in "pqr":
        if s[k] is not None and q["given"][k] is not None and F(q["given"][k]) != s[k]:
            out.append("%s: label for %s reads %s, the question holds %s" % (where, k, s[k], q["given"][k]))
    S = true_unknown_sq(q, s)
    if S <= 0:
        out.append("%s: no triangle (unknown squared = %s)" % (where, S))
        return None
    if s["r"] is not None and not (s["r"] > s["p" if u == "q" else "q"]):
        out.append("%s: the hypotenuse %s is not the longest side" % (where, s["r"]))
    check_layout(q, s, out, where)

    # keys
    ask = q["prompt"].count(ROUND_ASK)
    if q["stage"] == "a":
        if q["dp"] != 0 or not is_square(S):
            out.append("%s: round 1 unknown is not a whole number (x^2 = %s)" % (where, S))
        else:
            x = exact_sqrt(S)
            if x.denominator != 1 or F(q["keyText"]) != x:
                out.append("%s: key %s, exact answer %s" % (where, q["keyText"], x))
            tri = [s["p"] if s["p"] is not None else x, s["q"] if s["q"] is not None else x,
                   s["r"] if s["r"] is not None else x]
            if any(t.denominator != 1 for t in tri) or tri[0] ** 2 + tri[1] ** 2 != tri[2] ** 2:
                out.append("%s: round 1 triangle %r is not a Pythagorean triple" % (where, tri))
            check_spot(q, sorted(int(t) for t in tri), out, where)
        if ask:
            out.append("%s: round 1 asks for rounding" % where)
    else:
        if q["dp"] != 1 or is_square(S):
            out.append("%s: round %s answer is exact (x^2 = %s); it must need rounding" % (where, q["stage"], S))
        want = round_sqrt(S, 1)
        if F(q["keyText"]) != want or q["keyText"] != fmt1(want):
            out.append("%s: key %s, exact value rounded half up is %s" % (where, q["keyText"], fmt1(want)))
        if ask != 1:
            out.append("%s: prompt states 1 d.p. %d times" % (where, ask))
        if q["spot"]:
            out.append("%s: a 'Spotted it?' line outside round 1" % where)
    check_worked(q, s, S, out, where)

    add = None
    if q["type"] == "short":
        other = s["q"] if u == "p" else s["p"]
        add = s["r"] ** 2 + other ** 2
        key = F(q["keyText"])
        if q["dp"] == 1:
            if round_sqrt(add, 1) == key or math.sqrt(add) - math.sqrt(S) < 0.1:
                out.append("%s: the add value %s is too close to the key %s" % (where, fmt1(round_sqrt(add, 1)), key))
        else:
            if round_sqrt(add, 0) == key or round_sqrt(add, 1) == key or math.sqrt(add) - math.sqrt(S) < 1:
                out.append("%s: the add value is too close to the key %s" % (where, key))
    if q["stage"] == "c":
        check_context(q, s, S, out, where)
    return add


def check_spot(q, tri, out, where):
    g = gcd(gcd(tri[0], tri[1]), tri[2])
    prim = tuple(t // g for t in tri)
    if prim in SPOT_BASES:
        word = {1: "", 2: " doubled", 3: " tripled"}.get(g, " multiplied by %d" % g)
        want = "Spotted it? %d, %d, %d is the %s triangle%s. No calculation needed." % (
            tri[0], tri[1], tri[2], SPOT_BASES[prim], word)
        if q["spot"] != want:
            out.append("%s: %r should read %r" % (where, q["spot"], want))
    elif q["spot"]:
        out.append("%s: %s has a 'Spotted it?' line but is not a 3-4-5 or 5-12-13 multiple: %r"
                   % (where, tri, q["spot"]))


def tex_numbers(t):
    return [F(x) for x in re.findall(r"\d+(?:\.\d+)?", t.replace("\\ldots", ""))]


def check_worked(q, s, S, out, where):
    w = q["worked"]
    ids = [l for l in w if l.get("role") == "id"]
    texs = [l["tex"] for l in w if l["kind"] == "tex"]
    if len(ids) != 1 or w[0].get("role") != "id":
        out.append("%s: the worked solution does not start by identifying the hypotenuse" % where)
    elif q["type"] == "short" and (q["given"]["r"] + " " + q["unit"]) not in ids[0]["text"]:
        out.append("%s: the hypotenuse line does not name the given hypotenuse" % where)
    if len(texs) != 2:
        out.append("%s: %d working lines" % (where, len(texs)))
        return
    sign = " + " if q["type"] == "hyp" else " - "
    first = texs[0].split("=")
    if len(first) < 2 or sign not in first[1]:
        out.append("%s: working %r does not %s" % (where, texs[0], "add" if q["type"] == "hyp" else "subtract"))
    if tex_numbers(texs[0])[-1:] != [S]:
        out.append("%s: working %r should end on x^2 = %s" % (where, texs[0], S))
    if not texs[1].rstrip().endswith("= " + q["keyText"]):
        out.append("%s: working %r should end on the key %s" % (where, texs[1], q["keyText"]))


def check_context(q, s, S, out, where):
    x = Fraction(math.sqrt(S)) if not is_square(S) else exact_sqrt(S)
    v = {k: (s[k] if s[k] is not None else x) for k in "pqr"}
    P, Qn, R = float(v["p"]), float(v["q"]), float(v["r"])
    c, unit = q["context"], q["unit"]
    bad = None
    if c == "ladder":
        a = angle_deg(Qn, P)
        if unit != "m" or not (65 <= a <= 80) or not (2.5 <= R <= 7.0):
            bad = "ladder %.2f m, foot %.2f m, angle %.1f deg" % (R, P, a)
    elif c == "tv":
        if unit != "cm" or not (70 <= R <= 200) or not (1.70 <= P / Qn <= 1.85):
            bad = "screen %.1f x %.1f cm, diagonal %.1f" % (P, Qn, R)
    elif c == "ramp":
        if (unit != "cm" or q["type"] != "hyp" or not (15 <= Qn <= 60) or not (15 <= P / Qn <= 20)
                or P > 500):
            bad = "ramp rise %.0f cm, run %.0f cm (1:%.1f)" % (Qn, P, P / Qn)
    elif c == "field":
        if unit != "m" or not (50 <= P <= 200) or not (0.4 <= Qn / P <= 1):
            bad = "field %.1f x %.1f m" % (P, Qn)
    elif c == "roof":
        a = angle_deg(Qn, P)
        if unit != "m" or not (20 <= a <= 50) or not (3.0 <= R <= 6.0):
            bad = "roof slope %.2f m at %.1f deg" % (R, a)
    else:
        bad = "unknown situation %r" % c
    if bad:
        out.append("%s: implausible: %s" % (where, bad))
    for k in "pqr":
        if q["given"][k] is not None and (q["given"][k] + " " + unit) not in q["prompt"]:
            out.append("%s: the prompt does not state %s %s" % (where, q["given"][k], unit))
    rest = q["prompt"]
    for k in "pqr":
        if q["given"][k] is not None:
            rest = rest.replace(q["given"][k] + " " + unit, "")
    if re.search(r"(?<![\d.])%s(?!\d)" % re.escape(q["keyText"]), rest):
        out.append("%s: the prompt shows the answer %s" % (where, q["keyText"]))


def octant(q):
    L = q["layout"]
    O, A, B = L["O"], L["A"], L["B"]
    mx, my = (A[0] + B[0]) / 2 - O[0], (A[1] + B[1]) / 2 - O[1]
    return int(((math.degrees(math.atan2(my, mx)) + 360) % 360) // 45)


def check_session(sess, out, tag):
    qs = sess["questions"]
    if len(qs) != 20:
        out.append("%s: %d questions" % (tag, len(qs)))
        return
    if [q["stage"] for q in qs] != STAGE_ORDER:
        out.append("%s: rounds in the order %s" % (tag, "".join(q["stage"] for q in qs)))
    if [q["index"] for q in qs] != list(range(1, 21)):
        out.append("%s: question indexes %r" % (tag, [q["index"] for q in qs]))
    types = [q["type"] for q in qs]
    if types.count("short") < 12:
        out.append("%s: only %d of 20 are find-a-shorter-side" % (tag, types.count("short")))
    for i in range(18):
        if types[i] == types[i + 1] == types[i + 2]:
            out.append("%s: three %s questions in a row from question %d" % (tag, types[i], i + 1))
            break
    ctx = {q["context"] for q in qs if q["stage"] == "c"}
    if ctx != {"ladder", "tv", "ramp", "field", "roof"}:
        out.append("%s: round 3 used %s" % (tag, sorted(c for c in ctx if c)))
    octs = {octant(q) for q in qs if q["stage"] in "ab"}
    if len(octs) < 3:
        out.append("%s: the hypotenuse is drawn in only %d direction(s) in rounds 1-2" % (tag, len(octs)))
    adds = []
    for q in qs:
        adds.append(check_question(q, out, "%s q%d" % (tag, q["index"])))
    return adds


# ---------------------------------------------------------------- page side

COLLECT_JS = """(seeds) => seeds.map(seed => {
  const s = JPIB.buildSession(seed);
  s.questions.forEach(q => {
    q.layout = JPIB.layout(q);
    q.worked = JPIB.worked(q);
    q.example = q.type === 'short' ? JPIB.addExample(q) : null;
  });
  return s;
})"""

PROBE_JS = """(items) => items.map(it => {
  const s = JPIB.buildSession(it.seed), q = s.questions[it.i];
  return it.raws.map(r => [JPIB.mark(q, r), JPIB.isAddError(q, r)]);
})"""


def probes(q, add):
    key = F(q["keyText"])
    raws = [q["keyText"], fmt1(key + Fraction(1, 10)), fmt1(key - Fraction(1, 10)),
            q["given"]["r"] or "1", "abc", str(int(key) + 1)]
    if add is not None:
        k1 = round_sqrt(add, 1)
        raws += [fmt1(k1), "%.2f" % float(round_sqrt(add, 2)), "%.4f" % math.sqrt(float(add)),
                 str(int(round_sqrt(add, 0)))]
    return raws


async def collect_and_check(page, seeds):
    out = []
    data = await page.evaluate(COLLECT_JS, list(range(1, seeds + 1)))
    items, expect = [], []
    oct_counts = [0] * 8
    for sess in data:
        adds = check_session(sess, out, "seed %d" % sess["seed"]) or []
        for i, q in enumerate(sess["questions"]):
            if q["stage"] in "ab":
                oct_counts[octant(q)] += 1
            add = adds[i] if i < len(adds) else None
            raws = probes(q, add)
            items.append({"seed": sess["seed"], "i": i, "raws": raws})
            expect.append((sess["seed"], q, raws, add))
    total = sum(oct_counts)
    if total and min(oct_counts) < 0.05 * total:
        out.append("the hypotenuse direction is lopsided across rounds 1-2: %r" % oct_counts)
    got = await page.evaluate(PROBE_JS, items)
    for (seed, q, raws, add), res in zip(expect, got):
        for raw, (m, isadd) in zip(raws, res):
            pm = py_mark(q, raw)
            if m != pm:
                out.append("seed %d q%d: %r marked %s, expected %s" % (seed, q["index"], raw, m, pm))
            want = py_is_add(q, raw, add) if add is not None else False
            if isadd != want:
                out.append("seed %d q%d (%s): add-instead-of-subtract check gave %s for %r, expected %s"
                           % (seed, q["index"], q["type"], isadd, raw, want))
        if add is not None and not any(py_is_add(q, r, add) for r in raws):
            out.append("seed %d q%d: no probe is the add error" % (seed, q["index"]))
    helps = await page.evaluate("[1,2,3,4,5,9].map(n => JPIB.helpFor(n))")
    if helps != ["example"] * 3 + ["nudge"] * 3:
        out.append("helpFor(1..5, 9) gave %r: the first three get the example, then the nudge" % helps)
    return out, data


# ---------------------------------------------------------------- browser

async def new_page(browser, viewport=(1200, 1000)):
    ctx = await browser.new_context(viewport={"width": viewport[0], "height": viewport[1]})
    await bc.no_next_floor(ctx)

    async def route(r):
        url = r.request.url
        if url.startswith("http://127.0.0.1:%d/" % PORT) or url.startswith("https://cdn.jsdelivr.net/npm/katex"):
            await r.continue_()
        else:
            await r.abort()          # GA, Apps Script, Firebase SDK, fonts: nothing leaves the runner
    await ctx.route("**/*", route)
    page = await ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    await page.goto("http://127.0.0.1:%d/games/%s/?cb=%d" % (PORT, SLUG, int(time.time() * 1000)),
                    wait_until="load", timeout=20000)
    await page.wait_for_function("!!window.JPIB && !!window.JPIB.ui", timeout=8000)
    return ctx, page, errors


STUBS = """() => { window.__submits = []; window.__events = []; window.__next = [];
  window.mfg = function (name, params) { window.__events.push([name, params]); };
  window.MaffsLeaderboard.submitScore = function (slug, level, score, n) {
    window.__submits.push([slug, level, score, n]); return Promise.resolve({}); };
  const w = MaffsNext.wrong;
  MaffsNext.wrong = function (o) { window.__next.push(o.fallbackMs === undefined ? null : o.fallbackMs); return w(o); }; }"""


async def wait_next_question(page, prev):
    await page.wait_for_function(
        "(p) => { const s = JPIB.ui.state(); return s === 'done' || (s === 'asking' && JPIB.ui.index() > p); }",
        arg=prev, timeout=15000)


async def ui_playthrough(browser, out, seed=4242):
    ctx, page, errors = await new_page(browser)
    try:
        html = await page.content()
        if not re.search(r'<meta name="robots" content="noindex', html):
            out.append("UI: the page is not noindex")
        if await page.evaluate("typeof window.firebase") != "undefined":
            out.append("UI: the Firebase SDK was meant to be blocked but loaded")
        badge = await page.evaluate("(() => { const b = document.querySelector('.calc-badge'); return b ? "
                                    "[b.textContent.trim(), b.dataset.calc, b.offsetParent !== null] : null; })()")
        if badge != ["Calculator required", "required", True]:
            out.append("UI: calculator badge on the start screen is %r" % (badge,))
        if (await page.inner_text("#levelTag")).strip() != "Foundation":
            out.append("UI: the level is not labelled Foundation")
        if (await page.inner_text("#sessionSelect")).split() != ["20"]:
            out.append("UI: session buttons are %r" % (await page.inner_text("#sessionSelect")))
        await page.evaluate(STUBS)
        await page.evaluate("(s) => { JPIB.newSeed = () => s; }", seed)
        await page.click("#startBtn")
        await wait_next_question(page, 0)
        n_add, right, answered, expected_correct = 0, 0, [], []
        format_done = unread_done = False
        while await page.evaluate("JPIB.ui.state()") == "asking":
            q = await page.evaluate("JPIB.ui.question()")
            i = q["index"]
            if q["dp"] == 1 and not format_done:
                format_done = True
                # the right value at 2 d.p. when 1 d.p. is asked: format, never marked (SR-3)
                await page.fill("#answer", "%.2f" % (F(q["keyText"]) + Fraction(4, 100)))
                await page.click("#submitBtn")
                st = await page.evaluate("JPIB.ui.state()")
                msg = await page.inner_text("#msg")
                if st != "asking" or "decimal place" not in msg:
                    out.append("UI: a 2 d.p. answer was marked (state %s, message %r)" % (st, msg))
                nq = sum(1 for e in await page.evaluate("window.__events") if e[0] == "question_answered")
                if nq != len(answered):
                    out.append("UI: a format answer sent a question_answered event")
            if not unread_done:
                unread_done = True
                await page.fill("#answer", "12 cm")
                await page.click("#submitBtn")
                if await page.evaluate("JPIB.ui.state()") != "asking":
                    out.append("UI: '12 cm' was marked")
            if q["type"] == "short" and n_add < 5:
                raw, kind = q["add"]["k1Text"], "add"
                n_add += 1
            elif i % 3 == 0:
                raw, kind = q["keyText"], "right"
            else:
                raw, kind = str(int(F(q["keyText"])) + 3), "wrong"
            await page.fill("#answer", raw)
            await page.click("#submitBtn")
            answered.append(i)
            expected_correct.append(kind == "right")
            if kind == "right":
                right += 1
                if q["spot"]:
                    await page.wait_for_selector("#feedback .maffs-next")
                    fb = await page.inner_text("#feedback")
                    if q["spot"] not in fb:
                        out.append("UI q%d: right answer to a triple does not show %r" % (i, q["spot"]))
                    await page.click("#feedback .maffs-next")
            else:
                await page.wait_for_selector("#feedback .maffs-next")
                fb = await page.inner_text("#feedback")
                helped = await page.evaluate("(() => { const h = document.querySelector('#feedback [data-help]');"
                                             " return h ? h.dataset.help : null; })()")
                want = None
                if kind == "add":
                    want = "example" if n_add <= 3 else "nudge"
                if helped != want:
                    out.append("UI q%d (%s, add error %d): help shown %r, expected %r" % (i, kind, n_add, helped, want))
                if want == "example":
                    for frag in (q["given"]["r"] + " " + q["unit"], "so subtract"):
                        if frag not in fb:
                            out.append("UI q%d: the worked example does not show %r" % (i, frag))
                    fbk = (await page.evaluate("window.__next"))[-1]
                    if fbk is None or fbk < 2 ** 31 - 1:
                        out.append("UI q%d: the worked example's Next has a fallback timer (%r)" % (i, fbk))
                if want == "nudge" and NUDGE not in fb:
                    out.append("UI q%d: the nudge is missing" % i)
                if q["keyText"] not in fb or "opposite the right angle" not in fb:
                    out.append("UI q%d: the wrong-answer screen does not show the worked solution" % i)
                if q["spot"] and q["spot"] not in fb:
                    out.append("UI q%d: the 'Spotted it?' line is missing" % i)
                await page.click("#feedback .maffs-next")
            await wait_next_question(page, i)
        evs = await page.evaluate("window.__events")
        names = [e[0] for e in evs]
        for name, p in evs:
            if p.get("game_slug") != SLUG or p.get("level") != LEVEL:
                out.append("UI: %s sent game_slug=%r level=%r" % (name, p.get("game_slug"), p.get("level")))
        if names.count("game_started") != 1 or names.count("game_completed") != 1:
            out.append("UI: events %r" % sorted(set(names)))
        qa = [p for nm, p in evs if nm == "question_answered"]
        if [p.get("question_index") for p in qa] != list(range(1, 21)):
            out.append("UI: question_index sequence %r" % [p.get("question_index") for p in qa])
        if [p.get("correct") for p in qa] != expected_correct:
            out.append("UI: 'correct' flags %r, expected %r" % ([p.get("correct") for p in qa], expected_correct))
        gc = [p for nm, p in evs if nm == "game_completed"]
        if gc and (gc[0].get("questions_answered") != 20 or gc[0].get("questions_correct") != right
                   or not isinstance(gc[0].get("score"), int)):
            out.append("UI: game_completed carried %r" % gc[0])
        pbs = [p for nm, p in evs if nm == "personal_best_set"]
        if right and (len(pbs) != 1 or pbs[0].get("previous_best") != 0 or pbs[0].get("score") != gc[0].get("score")):
            out.append("UI: personal_best_set %r" % pbs)
        subs = await page.evaluate("window.__submits")
        if len(subs) != 1 or subs[0][0] != SLUG or subs[0][1] != LEVEL or subs[0][3] != 20:
            out.append("UI: submitted %r; expected one score to %s for 20 questions" % (subs, LEVEL))
        hist = await page.evaluate("localStorage.getItem('mfg_hist_v1::%s::%s')" % (SLUG, LEVEL))
        if not hist:
            out.append("UI: no score-history record under level %s" % LEVEL)
        for e in errors:
            out.append("UI page error: " + e)
        return n_add
    finally:
        await ctx.close()


async def phone_fit(browser, out):
    """Every question shape, wrong-answer feedback (the worked example for 'short'), at three sizes."""
    measured, worst = 0, {}
    for (w, h) in PHONES:
        ctx, page, errors = await new_page(browser, (w, h))
        try:
            await page.evaluate(STUBS)
            await page.evaluate("""() => {
              const J = JPIB, rng = J.mulberry32(99), qs = [];
              J.TRIPLES.forEach(t => { qs.push(J.buildStageA('hyp', t, rng)); qs.push(J.buildStageA('short', t, rng)); });
              const lastH = J.POOL_B.hyp[J.POOL_B.hyp.length - 1], lastS = J.POOL_B.short[J.POOL_B.short.length - 1];
              qs.push(J.buildStageB('hyp', lastH, rng), J.buildStageB('short', lastS, rng));
              J.CONTEXT_IDS.forEach(id => ['hyp', 'short'].forEach(t => {
                const kinds = {};
                J.CONTEXTS[id].pool[t].forEach(e => { const k = String(e[2] || ''); (kinds[k] = kinds[k] || []).push(e); });
                Object.keys(kinds).forEach(k => { let best = null;
                  kinds[k].forEach(e => { const q = J.buildContext(id, t, e, J.mulberry32(5));
                    if (!best || q.prompt.length > best.prompt.length) best = q; });
                  qs.push(best); });
              }));
              qs.forEach((q, i) => { q.index = i + 1; });
              J.buildSession = () => ({ seed: 0, types: qs.map(q => q.type), questions: qs });
              J.helpFor = () => 'example';   // measure the longest feedback a 'short' question can show
            }""")
            await page.click("#startBtn")
            await wait_next_question(page, 0)
            while await page.evaluate("JPIB.ui.state()") == "asking":
                q = await page.evaluate("JPIB.ui.question()")
                i = q["index"]
                where = "%dx%d %s%s %s q%d" % (w, h, q["stage"], ("/" + q["context"]) if q["context"] else "",
                                              q["type"], i)
                lab = await page.evaluate("""() => { const svg = document.querySelector('#fig svg');
                  const k = svg.getBoundingClientRect().width / svg.viewBox.baseVal.width;
                  const rs = [...svg.querySelectorAll('text')].map(t => { const r = t.getBoundingClientRect();
                    return [r.left, r.top, r.right, r.bottom, parseFloat(t.getAttribute('font-size')) * k]; });
                  return rs; }""")
                for j, a in enumerate(lab):
                    if a[4] < MIN_LABEL_PX:
                        out.append("%s: a triangle label renders at %.1fpx" % (where, a[4]))
                        break
                    for b in lab[j + 1:]:
                        if a[0] < b[2] - 0.5 and b[0] < a[2] - 0.5 and a[1] < b[3] - 0.5 and b[1] < a[3] - 0.5:
                            out.append("%s: two triangle labels overlap on screen" % where)
                raw = q["add"]["k1Text"] if q["type"] == "short" else str(int(F(q["keyText"])) + 3)
                await page.fill("#answer", raw)
                await page.click("#submitBtn")
                await page.wait_for_selector("#feedback .maffs-next")
                m = await page.evaluate("""() => { const b = document.querySelector('#feedback .maffs-next').getBoundingClientRect();
                  return [b.bottom, document.documentElement.scrollWidth, window.innerWidth]; }""")
                worst[(w, h)] = max(worst.get((w, h), 0), m[0])
                if m[0] > h - FOOTER:
                    out.append("%s: Next ends at %.0fpx, below the fold (%dpx)" % (where, m[0], h - FOOTER))
                if m[1] > m[2]:
                    out.append("%s: the page is %dpx wide" % (where, m[1]))
                measured += 1
                await page.click("#feedback .maffs-next")
                await wait_next_question(page, i)
            for e in errors:
                out.append("phone %dx%d page error: %s" % (w, h, e))
        finally:
            await ctx.close()
    print("Lowest Next: " + ", ".join("%dx%d %.0fpx (fold %d)" % (w, h, v, h - FOOTER) for (w, h), v in sorted(worst.items())))
    return measured


# ---------------------------------------------------------------- self-test

FAULTS = [
    ("keys truncated, not rounded half up",
     "JPIB.roundSqrt = function (S, D, dp) { return Math.floor((dp === 1 ? 10 : 1) * Math.sqrt(S) / D); };"),
    ("hypotenuse label moved to a leg",
     "(function(){ var o = JPIB.layout; JPIB.layout = function (q) { var L = o(q);"
     " var a = L.labels[0].text; L.labels[0].text = L.labels[2].text; L.labels[2].text = a; return L; }; })();"),
    ("rounds out of order",
     "JPIB.STAGES = [JPIB.STAGES[1], JPIB.STAGES[0], JPIB.STAGES[2]];"),
    ("a run of three",
     "(function(){ var o = JPIB.typeSequence; JPIB.typeSequence = function (rng) { var t = o(rng);"
     " t[0] = t[1] = t[2] = 'short'; return t; }; })();"),
    ("too few find-a-shorter-side questions",
     "JPIB.H_COUNTS = [10];"),
    ("add check switched off",
     "JPIB.isAddError = function () { return false; };"),
    ("add check fires on hypotenuse questions",
     "(function(){ var o = JPIB.isAddError; JPIB.isAddError = function (q, r) {"
     " return q.type === 'hyp' ? JPIB.mark(q, r) === 'wrong' : o(q, r); }; })();"),
    ("wrong scale word",
     "JPIB.scaleWord = function (k) { return k === 1 ? '' : k === 2 ? ' tripled' : ' doubled'; };"),
    ("wrong base triple named",
     "(function(){ var o = JPIB.spotLine; JPIB.spotLine = function (t) { var s = o(t);"
     " return s && s.replace('5-12-13', '3-4-5'); }; })();"),
    ("implausible ladder (85 degrees)",
     "JPIB.CONTEXTS.ladder.pool.short = [[70, 6, 'height']];"),
    ("right-angle mark at the wrong vertex",
     "(function(){ var o = JPIB.layout; JPIB.layout = function (q) { var L = o(q);"
     " L.mark = [L.A, L.A, L.A]; return L; }; })();"),
    ("the nudge never replaces the worked example",
     "JPIB.helpFor = function () { return 'example'; };"),
]


async def selftest(browser):
    lines, ok = [], True
    for name, patch in FAULTS:
        ctx, page, _ = await new_page(browser)
        try:
            await page.evaluate(patch)
            found, _ = await collect_and_check(page, seeds=30)
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
        found, data = await collect_and_check(page, seeds=args.seeds)
        await ctx.close()
        for f in found:
            fail(f)
        for e in errors:
            fail("page error: " + e)
        nq = sum(len(s["questions"]) for s in data)
        ns = sum(1 for s in data for q in s["questions"] if q["type"] == "short")
        print("Sessions: %d   questions: %d (%d find-a-shorter-side, %.1f%%)" % (len(data), nq, ns, 100.0 * ns / nq))

        ui_out = []
        n_add = await ui_playthrough(browser, ui_out)
        for f in ui_out:
            fail(f)
        print("UI play-through (Firebase SDK blocked): 20 questions, %d add errors (3 worked examples, then "
              "the nudge); format and unreadable answers not marked; events and one score to %s" % (n_add, LEVEL))

        if not args.no_phone:
            ph_out = []
            n = await phone_fit(browser, ph_out)
            for f in ph_out:
                fail(f)
            print("Phone fit: %d wrong-answer screens at %s" % (n, ", ".join("%dx%d" % p for p in PHONES)))

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
    ap.add_argument("--no-phone", action="store_true", help="skip the phone-fit measurement")
    ap.add_argument("--seeds", type=int, default=300, help="sessions to check (default 300)")
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
