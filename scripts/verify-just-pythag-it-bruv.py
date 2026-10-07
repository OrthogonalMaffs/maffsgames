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
  Positions   (Jon, 4 Oct 2026) the abstract triangles of rounds 1-2, read from the drawing: every session
              has the hypotenuse along the bottom (right angle at the top), up a side, and sloping both
              ways, with the right angle in all four corners; no position or group of positions is over
              40%; round 1 alone has the bottom, a side and both slopes.
  Tap step    round 1 only: one tap target per side, lying on that side; every side drawn at least 44px
              at 320px, and the middle 44px of it, from 6px inside to 22px outside, registers as that
              side by this script's nearest-side test and the page's; only the hypotenuse is accepted;
              every side label is styled alike (the unknown is "?" in round 1), in the markup and as
              rendered.
  Diagram     (Jon, 4 Oct 2026: it was a third of the card's width) JPIB.box sizes the drawing from the
              figure's width: the box is that width, labels 15-18px; the triangle with its labels
              reaches the box's edges (at least 90% of it in the tighter direction) and the triangle
              alone at least 70%, at 320, 375 and 390px and on a desktop; on screen the SVG is the
              figure's full width and 1:1 (one viewBox unit per pixel).
  Header      the standard header (58 games, todo 3.20): "← Back to Games" linking ../../ on every
              screen, above it; Aa on the start screen only, overlapping nothing, at every size.
  Calculator  every question's text ends "Use a calculator."; the shared calculator (MaffsCalc) is on the
              page, closed at first, and shows only while the answer box does; the play-through
              works one question out on its keys; using it sends no event.
  UI          a full session played with the Firebase SDK blocked (round 1 tapped with real pointer
              clicks: a leg first, which gets the message and no event, then the hypotenuse; once by
              keyboard); the start screen shows
              "Foundation" and "Calculator required"; the page is noindex; a format answer is not
              marked and sends no event; the first three add errors show the worked example (with
              the Next control's fallback timer off), the fourth and fifth the nudge; other wrong
              answers show the worked solution; the four canon 1.3 events carry their parameters
              at level 'ks3'; one score is submitted, to 'ks3', for 20 questions.
  Phone       at 320x568, 375x667 and 390x844, every question shape (all 14 triangles of round 1 as
              both types, both types of round 2, every situation's variants): the feedback for a
              wrong answer (for 'short', the longest: the worked example) keeps Next above the
              footer, the page never scrolls sideways, and triangle labels render at 12px or more
              without overlapping. Every question is measured with the calculator closed and then
              open: opening it moves nothing above it (the answer box and Check stay put, above the
              fold), the panel sits below the answer row inside the card with every key at least
              44px, and the page still never scrolls sideways; the feedback (with the panel left
              open, so hidden) still keeps Next above the fold. The SVG is the figure's full width
              at 1:1, and Aa overlaps nothing.
  Desktop     (Jon, 4 Oct 2026) the same pass at 1280x720, 1366x768 and 1920x1080: the open calculator
              docks right of the card, level with its top, never over it, and opening it moves nothing.
  Feedback    after Check, at all six sizes, with the calculator open on even questions and closed on
              odd ones, for wrong answers (the worked example), "Spotted it?" and the quick tick: the
              whole feedback in the window once the page settles; on a desktop without any scrolling.
              On phones Check is also pressed from scrolled positions (the answer box at the top of the
              window, or all the way down at the calculator). Once per size the feedback is pushed out
              of view: a phone must glide back to it, a desktop must not scroll.
  Layout      seven planted faults, each run at 1366x768 and 320x568 on a short question set, must
  faults      fail: no glide, the feedback pushed below the fold, the calculator not docked, docked
              over the column, the dock pushing the column, docked on a phone, a desktop scrolling.

FAULT-INJECTION SELF-TEST (runs every time; --no-selftest skips it)
-------------------------------------------------------------------------------
Each fault is patched into a FRESH page at run time (never into the file) and the session checks
must FAIL: keys truncated instead of rounded; the hypotenuse label moved to a leg; the rounds out
of order; a run of three; too few 'short' questions; the add check switched off; the add check
firing on 'hyp' questions; a wrong scale word; a wrong base triple; an implausible ladder; the
right-angle mark at the wrong vertex; the nudge never replacing the worked example; tap targets
mapped to the wrong side; a leg accepted as the hypotenuse; thin round-1 triangles not widened; the
unknown's label styled differently; no hypotenuse along the bottom; one position over 40%; the
hypotenuse sloping one way only; the box ignoring the figure's width; the triangle not grown to the box.

USAGE
    python scripts/verify-just-pythag-it-bruv.py
    python scripts/verify-just-pythag-it-bruv.py --no-selftest --seeds 50
    python scripts/verify-just-pythag-it-bruv.py --part 1         # CI job C1 (C2, C3: --part 2, 3)
    python scripts/verify-just-pythag-it-bruv.py --part-selftest  # the parts are the whole run
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
PHONES = [(320, 568), (375, 667), (390, 844), (412, 915)]
# Jon's ruling (option B, 4 Oct 2026): with the keypad open, everything fits one screen at 412x915, and
# rounds 1-2 at 390x844; elsewhere the answer row, Check and the keypad fit the window together.
FULL_FIT = {(412, 915): "abc", (390, 844): "ab"}
COMPACT_MIN_H = 150       # round 3's compact triangle stays readable
OPS = ["(", ")", "÷", "√", "×", "x²", "−", "+", "="]
DESKTOPS = [(1280, 720), (1366, 768), (1920, 1080)]
DESKTOP_MIN_W = 1000      # these sizes must dock the calculator; the phones must not
COMPACT_H = {"a": 180, "b": 160, "c": 160}   # JPIB.BOX_H_COMPACT, re-read from the page in run_all
TAP_RADIUS_PX = 22        # half a 44px fingertip
TAP_TOL_PX = 40           # the page counts a tap for the nearest side within this distance
SCALE_320 = 0.75          # screen px per viewBox unit at 320px wide; measured in run_all, this is the floor
TAP_WRONG = "The hypotenuse is opposite the right angle, and always the longest side."
FOOTER = 40
MIN_LABEL_PX = 12
DIAGRAM_SIZES = [(276, 568, False), (331, 667, False), (346, 844, False), (654, 1000, False),
                 (276, 568, True), (346, 844, True), (368, 915, True)]   # figure width, window height, compact
FILL_DRAWING = 0.90       # the drawing, labels included, spans this much of its box in the tighter direction
FILL_TRIANGLE = 0.70      # the triangle alone
CALC_NOTE = "Use a calculator."

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
        if t in ("x", "?"):
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
    thin = min(P, Qn) / max(P, Qn) < (0.5 if q["stage"] == "a" else 0.25)   # round 1 widens thin ones to tap
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


def position(q):
    """Where the hypotenuse is drawn, read from the drawing (SVG y runs down):
    Hb/Ht horizontal with the right angle above/below it; Vl/Vr vertical on the left/right;
    BL/BR/TL/TR legs horizontal and vertical with the right angle in that corner; 'other' else."""
    L = q["layout"]
    O, A, B = L["O"], L["A"], L["B"]
    dx, dy = B[0] - A[0], B[1] - A[1]
    ln = math.hypot(dx, dy)
    if abs(dy) < 1e-6 * ln:
        return "Hb" if O[1] < A[1] else "Ht"
    if abs(dx) < 1e-6 * ln:
        return "Vl" if O[0] > A[0] else "Vr"
    def axis(P):
        ex, ey = P[0] - O[0], P[1] - O[1]
        e = math.hypot(ex, ey)
        return abs(ex) < 1e-6 * e or abs(ey) < 1e-6 * e
    if not (axis(A) and axis(B)):
        return "other"
    mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
    return ("B" if O[1] > my else "T") + ("L" if O[0] < mx else "R")


def slope(pos):
    """'down' if the hypotenuse runs down to the right, 'up' if up to the right."""
    return {"BL": "down", "TR": "down", "BR": "up", "TL": "up"}.get(pos)


GROUP = {"Hb": "horizontal", "Ht": "horizontal", "Vl": "vertical", "Vr": "vertical",
         "BL": "sloping", "BR": "sloping", "TL": "sloping", "TR": "sloping"}


def check_positions(qs, out, tag):
    """Jon, 4 Oct 2026: every session's abstract triangles (rounds 1 and 2) include the hypotenuse
    along the bottom (right angle at the top), up a side, and sloping both ways, with the right angle
    in every corner; no position, and no group of positions, is more than 40% of them. Round 1, where
    the tap step is, has the bottom, a side and both slopes on its own."""
    ab = [position(q) for q in qs if q["stage"] in "ab"]
    a = [position(q) for q in qs if q["stage"] == "a"]
    if "other" in ab:
        out.append("%s: a triangle in rounds 1-2 is drawn in no defined position" % tag)
    for name, ps in (("rounds 1-2", ab), ("round 1", a)):
        miss = []
        if "Hb" not in ps:
            miss.append("hypotenuse along the bottom")
        if not ({"Vl", "Vr"} & set(ps)):
            miss.append("hypotenuse up a side")
        if {slope(x) for x in ps} < {"down", "up"}:
            miss.append("sloping both ways")
        if miss:
            out.append("%s: %s has no %s (%s)" % (tag, name, ", no ".join(miss), " ".join(ps)))
    if not {"BL", "BR", "TL", "TR"} <= set(ab):
        out.append("%s: the right angle is not in all four corners (%s)" % (tag, " ".join(ab)))
    n = len(ab)
    for key, label in ((lambda x: x, "position"), (lambda x: GROUP.get(x, x), "group")):
        counts = {}
        for x in ab:
            counts[key(x)] = counts.get(key(x), 0) + 1
        top = max(counts.items(), key=lambda kv: kv[1])
        if top[1] > 0.4 * n:
            out.append("%s: hypotenuse %s %s is %d of %d abstract triangles (over 40%%)" % (tag, label, top[0], top[1], n))


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
    check_positions(qs, out, tag)
    adds = []
    for q in qs:
        adds.append(check_question(q, out, "%s q%d" % (tag, q["index"])))
    return adds


# ---------------------------------------------------------------- page side

COLLECT_JS = """(seeds) => seeds.map(seed => {
  const s = JPIB.buildSession(seed);
  s.questions.forEach(q => {
    q.layout = JPIB.layout(q);
    // a phone with the calculator open: the compact triangle, which round 1's tap step must also work on
    if (q.stage === 'a') q.layoutC = JPIB.layout(q, JPIB.box(q, JPIB.REF.w, JPIB.REF.vh, true));
    q.worked = JPIB.worked(q);
    q.example = q.type === 'short' ? JPIB.addExample(q) : null;
    q.svg = JPIB.svg(q).html;
  });
  return s;
})"""

# The drawing sized to the figure: the box is the width it is given, the labels a legible fixed size, and
# the triangle grown until the drawing meets the box. Returns failures (the first few), not data.
DIAGRAM_JS = """([seeds, sizes, fillD, fillT]) => { const out = [];
  seeds.forEach(sd => JPIB.buildSession(sd).questions.forEach(q => sizes.forEach(([w, vh, c]) => {
    if (out.length > 5) return;
    const b = JPIB.box(q, w, vh, c), L = JPIB.layout(q, b), at = 'seed ' + sd + ' q' + q.index + ' at ' + w + 'px' + (c ? ' (compact)' : '');
    if (Math.abs(b.w - w) > 0.01 || L.vb[0] !== b.w || L.vb[1] !== b.h) { out.push(at + ': the box is ' + L.vb + ', not the figure width'); return; }
    if (b.font < 15 || b.font > 18 || L.font !== b.font) { out.push(at + ': labels at ' + L.font + 'px'); return; }
    const xs = [L.O[0], L.A[0], L.B[0]], ys = [L.O[1], L.A[1], L.B[1]];
    const tri = Math.max((Math.max(...xs) - Math.min(...xs)) / b.w, (Math.max(...ys) - Math.min(...ys)) / b.h);
    let x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
    L.labels.forEach(l => { x0 = Math.min(x0, l.x - l.w / 2); x1 = Math.max(x1, l.x + l.w / 2);
      y0 = Math.min(y0, l.y - l.h / 2); y1 = Math.max(y1, l.y + l.h / 2); });
    const all = Math.max((x1 - x0) / b.w, (y1 - y0) / b.h);
    if (all < fillD || tri < fillT) out.push(at + ': the drawing spans ' + (100 * all).toFixed(0) + '% of its box and the triangle ' +
      (100 * tri).toFixed(0) + '% (want ' + Math.round(100 * fillD) + '% and ' + Math.round(100 * fillT) + '%)');
    if (x0 < -0.01 || y0 < -0.01 || x1 > b.w + 0.01 || y1 > b.h + 0.01) out.push(at + ': the drawing spills out of its box');
  })));
  return out; }"""

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


LABEL_TAG = re.compile(r"<text\b([^>]*)>")
HIT_TAG = re.compile(r'<line class="tri-hit" data-side="([pqr])"[^>]*x1="([-\d.]+)" y1="([-\d.]+)" x2="([-\d.]+)" y2="([-\d.]+)"')


def check_svg(q, out, where):
    """Label styling identical for every side (Jon: styling must never give the hypotenuse away), and
    in round 1 exactly one tap target per side, lying on that side."""
    attrs = [re.sub(r'\s(data-side|x|y)="[^"]*"', "", a) for a in LABEL_TAG.findall(q["svg"])]
    if len(attrs) != 3 or len(set(attrs)) != 1:
        out.append("%s: the side labels are not styled identically: %r" % (where, attrs))
    hits = HIT_TAG.findall(q["svg"])
    if q["stage"] != "a":
        if hits:
            out.append("%s: tap targets outside round 1" % where)
        return
    L = q["layout"]
    ends = {"p": (L["O"], L["A"]), "q": (L["O"], L["B"]), "r": (L["A"], L["B"])}
    if sorted(h[0] for h in hits) != ["p", "q", "r"]:
        out.append("%s: tap targets %r, expected one per side" % (where, [h[0] for h in hits]))
    for k, x1, y1, x2, y2 in hits:
        a, b = ends[k]
        got = sorted([(round(float(x1), 1), round(float(y1), 1)), (round(float(x2), 1), round(float(y2), 1))])
        want = sorted([(round(a[0], 1), round(a[1], 1)), (round(b[0], 1), round(b[1], 1))])
        if any(abs(g[0] - w[0]) > 0.11 or abs(g[1] - w[1]) > 0.11 for g, w in zip(got, want)):
            out.append("%s: the tap target for side %s does not lie on that side" % (where, k))


TAP_JS = """(items) => items.map(it => {
  const q = JPIB.buildSession(it.seed).questions[it.i];
  const L = it.compact ? JPIB.layout(q, JPIB.box(q, JPIB.REF.w, JPIB.REF.vh, true)) : JPIB.layout(q);
  return it.pts.map(p => { const h = JPIB.sideAt(L, p[0], p[1]); return [h.side, h.dist]; });
})"""


def seg_dist(P, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = max(0.0, min(1.0, ((P[0] - a[0]) * dx + (P[1] - a[1]) * dy) / (dx * dx + dy * dy)))
    return math.hypot(P[0] - a[0] - t * dx, P[1] - a[1] - t * dy)


async def check_taps(page, taps, scale, out, key="layout"):
    """Every side of every round-1 triangle is a finger-sized target at 320px: drawn at least 44px long,
    and the 44px stretch at its middle, from 6px inside the line to 22px outside (where a finger
    aimed at the line lands), maps to that side by this script's nearest-side test and the page's own."""
    if not taps:
        return
    u = 1.0 / scale                                   # viewBox units per screen px
    items, want = [], []
    tag = " (compact, calculator open)" if key == "layoutC" else ""
    for seed, i, q in taps:
        L = q[key]
        O, A, B = L["O"], L["A"], L["B"]
        ends = {"p": (O, A), "q": (O, B), "r": (A, B)}
        opp = {"p": B, "q": A, "r": O}
        pts, exp = [], []
        bad = False
        for k, (a, b) in ends.items():
            ln = math.hypot(b[0] - a[0], b[1] - a[1])
            if ln * scale < 2 * TAP_RADIUS_PX and not bad:
                out.append("seed %d q%d (%s)%s: side %s is drawn %.0fpx long at 320px, under %dpx"
                           % (seed, q["index"], position(q), tag, k, ln * scale, 2 * TAP_RADIUS_PX))
                bad = True
            tx, ty = (b[0] - a[0]) / ln, (b[1] - a[1]) / ln
            nx, ny = -ty, tx
            mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            if (opp[k][0] - mid[0]) * nx + (opp[k][1] - mid[1]) * ny > 0:
                nx, ny = -nx, -ny                       # outward
            for t in (-22, -11, 0, 11, 22):
                for n in (-6, 0, 11, 22):
                    P = (mid[0] + (t * tx + n * nx) * u, mid[1] + (t * ty + n * ny) * u)
                    d = {kk: seg_dist(P, aa, bb) for kk, (aa, bb) in ends.items()}
                    near = min(d, key=d.get)
                    if near != k and not bad:
                        out.append("seed %d q%d (%s)%s: a tap %dpx along and %dpx out from side %s's middle is "
                                   "nearer side %s" % (seed, q["index"], position(q), tag, t, n, k, near))
                        bad = True
                    pts.append(P)
                    exp.append(k)
        items.append({"seed": seed, "i": i, "pts": pts, "compact": key == "layoutC"})
        want.append((seed, q, exp))
    got = await page.evaluate(TAP_JS, items)
    tol = TAP_TOL_PX / scale
    for (seed, q, exp), res in zip(want, got):
        for k, (side, dist) in zip(exp, res):
            if side != k or dist > tol:
                out.append("seed %d q%d%s: a tap on side %s registers as %s (%.1f units away)" % (seed, q["index"], tag, k, side, dist))
                break


async def collect_and_check(page, seeds, scale=None):
    scale = scale or SCALE_320
    out = []
    data = await page.evaluate(COLLECT_JS, list(range(1, seeds + 1)))
    items, expect = [], []
    taps = []
    for sess in data:
        adds = check_session(sess, out, "seed %d" % sess["seed"]) or []
        for i, q in enumerate(sess["questions"]):
            check_svg(q, out, "seed %d q%d" % (sess["seed"], q["index"]))
            if q["stage"] == "a":
                taps.append((sess["seed"], i, q))
            add = adds[i] if i < len(adds) else None
            raws = probes(q, add)
            items.append({"seed": sess["seed"], "i": i, "raws": raws})
            expect.append((sess["seed"], q, raws, add))
    await check_taps(page, taps, scale, out)
    await check_taps(page, taps, 1.0, out, key="layoutC")      # drawn 1:1 on a phone
    if await page.evaluate("['p','q','r'].map(k => JPIB.isHypTap(k))") != [False, False, True]:
        out.append("isHypTap accepts a leg, or refuses the hypotenuse")
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
    out.extend(await page.evaluate(DIAGRAM_JS, [list(range(1, min(seeds, 60) + 1)), DIAGRAM_SIZES,
                                                FILL_DRAWING, FILL_TRIANGLE]))
    helps = await page.evaluate("[1,2,3,4,5,9].map(n => JPIB.helpFor(n))")
    if helps != ["example"] * 3 + ["nudge"] * 3:
        out.append("helpFor(1..5, 9) gave %r: the first three get the example, then the nudge" % helps)
    return out, data


# ---------------------------------------------------------------- browser

async def new_page(browser, viewport=(1200, 1000), touch=False):
    """touch: a phone (pointer: coarse), where the calculator's keypad types the answer."""
    ctx = await browser.new_context(viewport={"width": viewport[0], "height": viewport[1]},
                                    has_touch=touch, is_mobile=touch)
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
        "(p) => { const s = JPIB.ui.state(); return s === 'done' || "
        "((s === 'asking' || s === 'tap') && JPIB.ui.index() > p); }",
        arg=prev, timeout=15000)


# The screen point just outside a side's midpoint (off px along its outward normal): where a finger lands.
CLICK_PT = """([k, off]) => { const L = JPIB.ui.layout();
  const svg = document.querySelector('#fig svg'), r = svg.getBoundingClientRect(), s = r.width / L.vb[0];
  const e = {p: [L.O, L.A], q: [L.O, L.B], r: [L.A, L.B]}[k], opp = {p: L.B, q: L.A, r: L.O}[k];
  const mx = (e[0][0] + e[1][0]) / 2, my = (e[0][1] + e[1][1]) / 2;
  let nx = -(e[1][1] - e[0][1]), ny = e[1][0] - e[0][0]; const n = Math.hypot(nx, ny); nx /= n; ny /= n;
  if ((opp[0] - mx) * nx + (opp[1] - my) * ny > 0) { nx = -nx; ny = -ny; }
  return [r.left + mx * s + nx * off, r.top + my * s + ny * off]; }"""

LABEL_STYLES = """() => [...document.querySelectorAll('#fig text.tri-label')].map(t => { const c = getComputedStyle(t);
  return [t.getAttribute('class'), c.fill, c.fontStyle, c.fontWeight, c.fontSize, c.fontFamily, c.textDecorationLine].join('|'); })"""


async def tap_step(page, q, out, where, wrong_first=False, keyboard=False):
    """Round 1: the answer box is hidden until the hypotenuse is tapped; a leg gets the message, no
    event, no change of state; the hypotenuse opens the answer box. Real pointer events on real pixels."""
    if await page.evaluate("JPIB.ui.state()") != "tap":
        out.append("%s: round 1 question opened without the tap step" % where)
        return
    if await page.is_visible("#answer"):
        out.append("%s: the answer box shows before the hypotenuse is tapped" % where)
    nev = len(await page.evaluate("window.__events || []"))
    if wrong_first:
        leg = "p" if q["unknown"] != "p" else "q"
        x, y = await page.evaluate(CLICK_PT, [leg, 12])
        await page.mouse.click(x, y)
        if await page.evaluate("JPIB.ui.state()") != "tap":
            out.append("%s: tapping a leg moved on" % where)
        msg = (await page.inner_text("#msg")).strip()
        if msg != TAP_WRONG:
            out.append("%s: a wrong tap says %r" % (where, msg))
        if await page.is_visible("#answer"):
            out.append("%s: a wrong tap opened the answer box" % where)
    if keyboard:
        await page.focus('#fig .tri-hit[data-side="r"]')
        await page.keyboard.press("Enter")
    else:
        x, y = await page.evaluate(CLICK_PT, ["r", 12])
        await page.mouse.click(x, y)
    if await page.evaluate("JPIB.ui.state()") != "asking":
        out.append("%s: tapping the hypotenuse did not open the answer box" % where)
        return
    if not await page.is_visible("#answer"):
        out.append("%s: the answer box is hidden after the hypotenuse tap" % where)
    picked = await page.evaluate("[...document.querySelectorAll('#fig .tri-side.picked')].map(l => l.dataset.side)")
    if picked != ["r"]:
        out.append("%s: highlighted %r after the tap" % (where, picked))
    if len(await page.evaluate("window.__events || []")) != nev:
        out.append("%s: the tap step sent an analytics event" % where)


HEADER_JS = """() => { const vis = e => e && e.offsetParent !== null;
  const back = [...document.querySelectorAll('a.back-link')].filter(vis);
  const aa = document.getElementById('a11yToggle'), r = vis(aa) ? aa.getBoundingClientRect() : null;
  const hits = [];
  if (r) document.querySelectorAll('body *').forEach(e => {
    if (e === aa || e.contains(aa) || aa.contains(e) || !vis(e)) return;
    if ([...e.childNodes].every(n => n.nodeType !== 3 || !n.textContent.trim()) && e.children.length) return;   // boxes only via their text
    const b = e.getBoundingClientRect();
    if (b.width && b.height && r.left < b.right - 0.5 && b.left < r.right - 0.5 && r.top < b.bottom - 0.5 && b.top < r.bottom - 0.5)
      hits.push(e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.className && typeof e.className === 'string' ? '.' + e.className.split(' ')[0] : ''));
  });
  const scr = document.querySelector('.screen.active');
  return { back: back.map(a => [a.getAttribute('href'), a.textContent.trim()]), aa: !!r, hits: hits,
           backAbove: !!(back.length && scr && back[0].getBoundingClientRect().bottom <= scr.getBoundingClientRect().top + 0.5) }; }"""


async def check_header(page, where, aa=False):
    """The standard header: one "← Back to Games" to ../../, above the screen; Aa on the start screen
    only, overlapping nothing."""
    out = []
    h = await page.evaluate(HEADER_JS)
    if h["back"] != [["../../", "← Back to Games"]]:
        out.append("%s: back links %r, expected one '← Back to Games' to ../../" % (where, h["back"]))
    elif not h["backAbove"]:
        out.append("%s: the back link is not above the screen" % where)
    if h["aa"] != aa:
        out.append("%s: Aa is %s" % (where, "missing" if aa else "shown (it belongs on the start screen only)"))
    if h["hits"]:
        out.append("%s: Aa overlaps %s" % (where, ", ".join(h["hits"][:4])))
    return out


async def use_calculator(page, q, out, where):
    """Open the calculator and work the unknown side out on its keys (square root of a sum or difference
    of squares), as a student with no calculator of their own does. No event may fire; it closes again."""
    nev = len(await page.evaluate("window.__events || []"))
    if await page.evaluate("JPIB.ui.calc().isOpen()"):
        out.append("%s: the calculator starts open" % where)
    await page.click(".maffs-calc-toggle")
    if not await page.is_visible(".maffs-calc-panel"):
        out.append("%s: the Calculator button does not open the panel" % where)
        return
    g = q["given"]
    if q["type"] == "hyp":
        seq = [g["p"], "x²", "+", g["q"], "x²"]
    else:
        seq = [g["r"], "x²", "−", g["p"] if g["p"] is not None else g["q"], "x²"]
    await page.click('.maffs-calc-key[data-act="clear"]')
    await page.click('.maffs-calc-key[data-val="√("]')
    for tok in seq:
        if tok in ("x²", "+", "−"):
            await page.click('.maffs-calc-key >> text="%s"' % tok)
        else:
            for ch in tok:
                await page.click('.maffs-calc-key[data-val="%s"]' % ch)
    await page.click('.maffs-calc-key[data-act="eq"]')
    shown = await page.evaluate("JPIB.ui.calc().display().result")
    q = dict(q, layout=await page.evaluate("JPIB.ui.layout()"))
    want = math.sqrt(float(true_unknown_sq(q, sides_of(q))))
    try:
        ok = abs(float(shown) - float("%.10g" % want)) <= 1e-9 * want
    except ValueError:
        ok = False
    if not ok:
        out.append("%s: the calculator shows %r for the unknown side, expected %.10g" % (where, shown, want))
    if len(await page.evaluate("window.__events || []")) != nev:
        out.append("%s: using the calculator sent an analytics event" % where)
    await page.click(".maffs-calc-toggle")
    if await page.is_visible(".maffs-calc-panel"):
        out.append("%s: the Calculator button does not close the panel" % where)


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
        out.extend(await check_header(page, "UI start screen", aa=True))
        if await page.evaluate("typeof window.MaffsCalc") != "object":
            out.append("UI: the shared calculator (MaffsCalc) is not loaded")
        if (await page.inner_text("#levelTag")).strip() != "Foundation":
            out.append("UI: the level is not labelled Foundation")
        if (await page.inner_text("#sessionSelect")).split() != ["20"]:
            out.append("UI: session buttons are %r" % (await page.inner_text("#sessionSelect")))
        await page.evaluate(STUBS)
        await page.evaluate("(s) => { JPIB.newSeed = () => s; }", seed)
        await page.click("#startBtn")
        await wait_next_question(page, 0)
        n_add, right, answered, expected_correct = 0, 0, [], []
        format_done = unread_done = calc_done = False
        taps_done = 0
        while await page.evaluate("JPIB.ui.state()") in ("asking", "tap"):
            q = await page.evaluate("JPIB.ui.question()")
            i = q["index"]
            styles = await page.evaluate(LABEL_STYLES)
            if len(styles) != 3 or len(set(styles)) != 1:
                out.append("UI q%d: side labels styled differently: %r" % (i, styles))
            if i == 1:
                out.extend(await check_header(page, "UI q1"))
                fig = await page.evaluate(FIG_JS)
                if abs(fig[0] - fig[1]) > 1 or abs(fig[1] - fig[2]) > 1:
                    out.append("UI q1 (desktop): the figure is %.0fpx wide, the SVG %.0fpx, its viewBox %.0f"
                               % (fig[0], fig[1], fig[2]))
            if q["stage"] == "a":
                await tap_step(page, q, out, "UI q%d" % i, wrong_first=taps_done < 2, keyboard=taps_done == 2)
                taps_done += 1
            elif await page.evaluate("document.querySelectorAll('#fig .tri-hit').length"):
                out.append("UI q%d: tap targets outside round 1" % i)
            # every question ends "Use a calculator." (after round 1's tap step, which has its own prompt)
            shown = await page.evaluate("(() => { const p = document.getElementById('prompt'), n = p.querySelector('.calc-note');"
                                        " return [p.textContent.trim(), n && n.offsetParent !== null ? n.textContent : null]; })()")
            if shown != [q["prompt"] + " " + CALC_NOTE, CALC_NOTE]:
                out.append("UI q%d: the question reads %r, not the prompt then %r" % (i, shown[0][-60:], CALC_NOTE))
            if q["stage"] == "b" and not calc_done:
                calc_done = True
                await use_calculator(page, q, out, "UI q%d" % i)
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
        if not calc_done:
            out.append("UI: the play-through never used the calculator")
        out.extend(await check_header(page, "UI results screen"))
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


FIG_JS = """() => { const f = document.getElementById('fig'), s = f.querySelector('svg');
  return [f.getBoundingClientRect().width, s.getBoundingClientRect().width, s.viewBox.baseVal.width]; }"""

# The answer box and the keypad's state (a phone types the answer on the keypad).
ANSWER_JS = """() => { const a = document.getElementById('answer'), c = JPIB.ui.calc(), vis = e => !!e && e.offsetParent !== null;
  const keys = [...document.querySelectorAll('.maffs-calc-key')].map(k => k.getBoundingClientRect());
  const svg = document.querySelector('#fig svg'), k = svg.getBoundingClientRect().width / svg.viewBox.baseVal.width;
  const row = document.getElementById('answerForm').getBoundingClientRect(), p = document.querySelector('.maffs-calc-panel').getBoundingClientRect();
  return { mode: c.answerMode(), ro: a.readOnly, im: a.getAttribute('inputmode'), focused: document.activeElement === a,
    open: c.isOpen(), target: c.target(), selected: a.classList.contains('maffs-calc-selected'),
    cue: vis(document.querySelector('.maffs-calc-cue-answer')), screenSel: document.querySelector('.maffs-calc-screen').classList.contains('maffs-calc-selected'),
    disabled: [...document.querySelectorAll('.maffs-calc-key:disabled')].map(k => k.textContent),
    toggle: vis(document.querySelector('.maffs-calc-toggle')), close: vis(document.querySelector('.maffs-calc-close')),
    keyH: Math.min(...keys.map(r => r.height)), keyW: Math.min(...keys.map(r => r.width)),
    svgH: svg.getBoundingClientRect().height,
    label: Math.min(...[...svg.querySelectorAll('text')].map(t => parseFloat(t.getAttribute('font-size')) * k)),
    scrollY: scrollY, rowTopV: row.top, panelBottomV: p.bottom }; }"""

# Page coordinates (as at scroll 0): clicking the toggle may scroll the page to it.
CALC_JS = """() => { const R = e => { const r = e.getBoundingClientRect(), y = scrollY, x = scrollX;
    return [r.left + x, r.top + y, r.right + x, r.bottom + y]; };
  const docked = JPIB.ui.calc().isDocked(), cw = document.documentElement.clientWidth;
  const p = document.querySelector('.maffs-calc-panel'), open = p && p.offsetParent !== null;
  const keys = [...document.querySelectorAll('.maffs-calc-key')].map(k => k.getBoundingClientRect());
  return { panel: open ? R(p) : null, row: R(document.getElementById('answer')), check: R(document.getElementById('submitBtn')),
    card: R(document.getElementById('qcard')),
    key: open ? [Math.min(...keys.map(k => k.width)), Math.min(...keys.map(k => k.height))] : null,
    scroll: document.documentElement.scrollWidth, inner: innerWidth, docked: docked, cw: cw }; }"""

# After Check: wait until the page stops scrolling (a phone glides to the feedback), then measure the
# feedback in the window. null if it has already gone (a quick tick moves on after 1.1s).
SETTLED_FB_JS = """() => new Promise(res => { let last = -1, n = 0; const t0 = performance.now();
  (function f() { const y = scrollY; n = y === last ? n + 1 : 0; last = y;
    if (n < 4 && performance.now() - t0 < 900) return requestAnimationFrame(f);
    const fb = document.querySelector('#feedback .fb, #feedback .fb-quick');
    if (!fb) return res(null);
    const r = fb.getBoundingClientRect(), nx = document.querySelector('#feedback .maffs-next');
    const p = document.querySelector('.maffs-calc-panel');
    res({ top: r.top, bottom: Math.max(r.bottom, nx ? nx.getBoundingClientRect().bottom : 0),
          next: nx ? nx.getBoundingClientRect().bottom : 0, scrollY: scrollY,
          calc: !!(p && p.offsetParent !== null), sw: document.documentElement.scrollWidth, iw: innerWidth }); })(); })"""


async def apply_patch(page, patch):
    kind, code = patch
    if kind == "style":
        await page.add_style_tag(content=code)
    else:
        await page.evaluate(code)


async def phone_fit(browser, out, sizes=None, only=None, patch=None, report=True):
    """Every question shape at three phone and three desktop sizes: the asking screen with the calculator
    closed then open, then the feedback after Check (wrong: the worked example for 'short'; right: the
    quick tick or "Spotted it?"), which must be fully in view. only: a JS filter (q, i) for a short run;
    patch: a planted fault, applied before the game starts."""
    sizes = sizes or PHONES + DESKTOPS
    measured, worst, tapworst, calcworst, checkworst, fbworst, glided = 0, {}, {}, {}, {}, {}, set()
    compactworst, switched = {}, set()
    for (w, h) in sizes:
        ctx, page, errors = await new_page(browser, (w, h), touch=w < DESKTOP_MIN_W)
        try:
            await page.evaluate(STUBS)
            if patch:
                await apply_patch(page, patch)
            await page.evaluate("""() => {
              const ONLY = __ONLY__;
              const J = JPIB, rng = J.mulberry32(99), qs = [];
              const P = J.POSITIONS; let n = 0;
              // round 1: every triangle, both types, the positions dealt in turn; then the thinnest
              // triangles (7-24-25, 5-12-13) in all eight positions, where the tap targets are smallest
              J.TRIPLES.forEach(t => { qs.push(J.buildStageA('hyp', t, rng, P[n++ % 8]));
                qs.push(J.buildStageA('short', t, rng, P[n++ % 8])); });
              J.TRIPLES.filter(t => t.k === 1 && (t.base[0] === 7 || t.base[0] === 5)).forEach(t =>
                P.forEach(pos => qs.push(J.buildStageA('short', t, rng, pos))));
              // round 2: the longest labels and answers, in all eight positions
              const lastH = J.POOL_B.hyp[J.POOL_B.hyp.length - 1], lastS = J.POOL_B.short[J.POOL_B.short.length - 1];
              P.forEach(pos => qs.push(J.buildStageB('hyp', lastH, rng, pos), J.buildStageB('short', lastS, rng, pos)));
              J.CONTEXT_IDS.forEach(id => ['hyp', 'short'].forEach(t => {
                const kinds = {};
                J.CONTEXTS[id].pool[t].forEach(e => { const k = String(e[2] || ''); (kinds[k] = kinds[k] || []).push(e); });
                Object.keys(kinds).forEach(k => { let best = null;
                  kinds[k].forEach(e => { const q = J.buildContext(id, t, e, J.mulberry32(5));
                    if (!best || q.prompt.length > best.prompt.length) best = q; });
                  qs.push(best); });
              }));
              const keep = ONLY ? qs.filter(ONLY) : qs;
              keep.forEach((q, i) => { q.index = i + 1; });
              J.buildSession = () => ({ seed: 0, types: keep.map(q => q.type), questions: keep });
              J.helpFor = () => 'example';   // measure the longest feedback a 'short' question can show
            }""".replace("__ONLY__", only or "null"))
            out.extend(await check_header(page, "%dx%d start screen" % (w, h), aa=True))
            await page.click("#startBtn")
            await wait_next_question(page, 0)
            out.extend(await check_header(page, "%dx%d question 1" % (w, h)))
            while await page.evaluate("JPIB.ui.state()") in ("asking", "tap"):
                q = await page.evaluate("JPIB.ui.question()")
                i = q["index"]
                where = "%dx%d %s%s %s q%d" % (w, h, q["stage"], ("/" + q["context"]) if q["context"] else "",
                                              q["type"], i)
                desk = w >= DESKTOP_MIN_W
                compact_tap = not desk and q["stage"] == "a" and i % 2 == 0
                # measure closed first; a phone keeps it open for every other round-1 tap step (compact triangle)
                await page.evaluate("JPIB.ui.calc().%s()" % ("open" if compact_tap else "close"))
                fig = await page.evaluate(FIG_JS)
                if compact_tap:
                    svgh = await page.evaluate("document.querySelector('#fig svg').getBoundingClientRect().height")
                    if svgh > COMPACT_H["a"] + 0.5:
                        out.append("%s: with the calculator open the tap-step triangle is %.0fpx tall, not compact" % (where, svgh))
                if abs(fig[0] - fig[1]) > 1 or abs(fig[1] - fig[2]) > 1:
                    out.append("%s: the figure is %.0fpx wide, the SVG %.0fpx, its viewBox %.0f: not full width at 1:1"
                               % (where, fig[0], fig[1], fig[2]))
                if q["stage"] == "a":
                    # the whole triangle above the fold to tap, then the answer box and Check after it
                    svgb = await page.evaluate("document.querySelector('#fig svg').getBoundingClientRect().bottom")
                    if svgb > h - FOOTER:
                        out.append("%s: the triangle ends at %.0fpx, below the fold, during the tap step" % (where, svgb))
                    await tap_step(page, q, out, where, wrong_first=True)
                    chk = await page.evaluate("document.querySelector('#submitBtn').getBoundingClientRect().bottom")
                    # one line with room to spare: a wider fallback font (CI's) must not wrap Check below
                    row = await page.evaluate("""() => { const r = document.querySelector('#answerForm');
                      const kids = [...r.children].filter(e => e.offsetParent !== null);
                      const tops = kids.map(e => Math.round(e.getBoundingClientRect().top + e.getBoundingClientRect().height / 2));
                      // the fixed parts at their own width, plus the input at its minimum
                      const used = kids.reduce((a, e) => a + (e.tagName === 'INPUT'
                          ? parseFloat(getComputedStyle(e).minWidth) : e.getBoundingClientRect().width), 0)
                        + parseFloat(getComputedStyle(r).columnGap || 0) * (kids.length - 1);
                      return [Math.max(...tops) - Math.min(...tops), r.getBoundingClientRect().width - used]; }""")
                    if row[0] > 4 or row[1] < 20:
                        out.append("%s: the answer row is not one line with 20px spare (centres %dpx apart, %.0fpx spare)"
                                   % (where, row[0], row[1]))
                    tapworst[(w, h)] = max(tapworst.get((w, h), 0), max(svgb, chk))
                    if chk > h - FOOTER:
                        out.append("%s: Check ends at %.0fpx, below the fold, after the tap" % (where, chk))
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
                calc_open = i % 2 == 0
                if q["spot"] or i % 5 == 0:
                    raw, kind = q["keyText"], ("spot" if q["spot"] else "quick")
                else:
                    raw, kind = (q["add"]["k1Text"] if q["type"] == "short" else str(int(F(q["keyText"])) + 3)), "wrong"
                if desk:
                    # Desktops: docked right of the card, level with its top, never over it; the card does not move;
                    # the answer box is an ordinary input (no answer target).
                    await page.evaluate("JPIB.ui.calc().close()")
                    if not await page.evaluate("document.activeElement === document.getElementById('answer')"):
                        out.append("%s: on a desktop the answer box is not focused when the question opens" % where)
                    closed = await page.evaluate(CALC_JS)
                    await page.click(".maffs-calc-toggle")
                    opened = await page.evaluate(CALC_JS)
                    a = await page.evaluate(ANSWER_JS)
                    if a["mode"] or a["ro"] or a["im"] == "none":
                        out.append("%s: a desktop answer box is read-only or keypad-only (mode %s, readOnly %s, inputmode %r)"
                                   % (where, a["mode"], a["ro"], a["im"]))
                    checkworst[(w, h)] = max(checkworst.get((w, h), 0), opened["check"][3])
                    if closed["panel"] is not None:
                        out.append("%s: the calculator panel shows before it is opened" % where)
                    if opened["panel"] is None:
                        out.append("%s: the Calculator button does not open the panel" % where)
                    else:
                        calcworst[(w, h)] = max(calcworst.get((w, h), 0), opened["panel"][3])
                        if any(abs(x - y) > 0.5 for x, y in zip(closed["row"] + closed["check"] + closed["card"][:3],
                                                                 opened["row"] + opened["check"] + opened["card"][:3])):
                            out.append("%s: opening the calculator moved the card, the answer box or Check" % where)
                        if opened["check"][3] > h - FOOTER:
                            out.append("%s: with the calculator open, Check ends at %.0fpx, below the fold" % (where, opened["check"][3]))
                        if opened["key"][0] < 44 or opened["key"][1] < 44:
                            out.append("%s: a calculator key is %.0fx%.0fpx, under 44" % (where, opened["key"][0], opened["key"][1]))
                        if opened["scroll"] > opened["inner"]:
                            out.append("%s: with the calculator open the page is %dpx wide" % (where, opened["scroll"]))
                        P, C = opened["panel"], opened["card"]
                        if not opened["docked"]:
                            out.append("%s: the calculator is not docked beside the card" % where)
                        else:
                            if P[0] < C[2] + 4:
                                out.append("%s: the docked calculator starts at x=%.0f, over the card (right edge %.0f)" % (where, P[0], C[2]))
                            if P[2] > opened["cw"]:
                                out.append("%s: the docked calculator runs past the window (x=%.0f > %d)" % (where, P[2], opened["cw"]))
                            if abs(P[1] - C[1]) > 2:
                                out.append("%s: the docked calculator's top (%.0f) is not level with the card's (%.0f)" % (where, P[1], C[1]))
                    if not calc_open:
                        await page.evaluate("JPIB.ui.calc().close()")
                    await page.fill("#answer", raw)
                else:
                    # Phones: a tap on the answer box opens the keypad on it. No system keyboard: read-only,
                    # inputmode none, never focused. The keypad types the answer; the operators are disabled.
                    await page.evaluate("JPIB.ui.calc().close()")
                    await page.tap("#answer")
                    a = await page.evaluate(ANSWER_JS)
                    o = await page.evaluate(CALC_JS)
                    if not (a["mode"] and a["ro"] and a["im"] == "none"):
                        out.append("%s: on a phone the answer box could open the system keyboard (keypad mode %s, readOnly %s, "
                                   "inputmode %r)" % (where, a["mode"], a["ro"], a["im"]))
                    if a["focused"]:
                        out.append("%s: tapping the answer box focused it (the system keyboard would open)" % where)
                    if not a["open"] or a["target"] != "answer":
                        out.append("%s: tapping the answer box did not open the keypad on it (open %s, target %r)" % (where, a["open"], a["target"]))
                    if not (a["selected"] and a["cue"]) or a["screenSel"]:
                        out.append("%s: the answer box is not marked as selected (border %s, 'typing here' %s; display marked %s)"
                                   % (where, a["selected"], a["cue"], a["screenSel"]))
                    if a["disabled"] != OPS:
                        out.append("%s: typing the answer, the disabled keys are %r, expected %r" % (where, a["disabled"], OPS))
                    if a["toggle"] or not a["close"]:
                        out.append("%s: the Calculator button is not inside the panel (button shown %s, close key %s)" % (where, a["toggle"], a["close"]))
                    if a["keyH"] < 47.5 or a["keyW"] < 44:
                        out.append("%s: the smallest key is %.0fx%.0fpx (want 48px tall, 44px wide at least)" % (where, a["keyW"], a["keyH"]))
                    if a["svgH"] > COMPACT_H[q["stage"]] + 0.5 or a["svgH"] < COMPACT_MIN_H - 0.5:
                        out.append("%s: with the keypad open the triangle is %.0fpx tall (compact: %d-%dpx)"
                                   % (where, a["svgH"], COMPACT_MIN_H, COMPACT_H[q["stage"]]))
                    if a["label"] < 15:
                        out.append("%s: with the keypad open a triangle label is %.1fpx" % (where, a["label"]))
                    if o["scroll"] > o["inner"]:
                        out.append("%s: with the keypad open the page is %dpx wide" % (where, o["scroll"]))
                    if o["panel"] and (o["panel"][1] < o["row"][3] - 0.5 or o["panel"][0] < o["card"][0] - 0.5
                                       or o["panel"][2] > o["card"][2] + 0.5):
                        out.append("%s: the keypad is not under the answer row inside the card" % where)
                    # the fit (Jon's option B)
                    fold = h - FOOTER
                    if o["panel"]:
                        full = q["stage"] in FULL_FIT.get((w, h), "")
                        key = (w, h, "full" if full else "together")
                        if full:
                            compactworst[key] = max(compactworst.get(key, 0), o["panel"][3])
                            if o["panel"][3] > fold or a["scrollY"] > 0.5:
                                out.append("%s: with the keypad open the page needs scrolling (keypad ends at %.0fpx, fold %d, "
                                           "scrolled %.0f): question to keypad must fit one screen" % (where, o["panel"][3], fold, a["scrollY"]))
                        else:
                            span = o["panel"][3] - o["row"][1]
                            compactworst[key] = max(compactworst.get(key, 0), span)
                            if span > fold:
                                out.append("%s: the answer row to the keypad's bottom is %.0fpx, taller than the window (%d)" % (where, span, fold))
                        if a["rowTopV"] < -0.5 or a["panelBottomV"] > fold + 0.5:
                            out.append("%s: after the tap the answer row and keypad are not in view together (y=%.0f..%.0f, fold %d)"
                                       % (where, a["rowTopV"], a["panelBottomV"], fold))
                    if (w, h) not in switched:
                        # switching: the display takes the keys, the operators come back, the answer is untouched
                        switched.add((w, h))
                        await page.tap(".maffs-calc-lines")
                        b = await page.evaluate(ANSWER_JS)
                        if b["target"] != "calc" or b["disabled"] or not b["screenSel"] or b["selected"]:
                            out.append("%s: tapping the calculator display did not select it (target %r, disabled %r)" % (where, b["target"], b["disabled"]))
                        await page.tap('.maffs-calc-key[data-val="7"]')
                        await page.tap('.maffs-calc-key[data-val="×"]')
                        await page.tap('.maffs-calc-key[data-val="6"]')
                        await page.tap('.maffs-calc-key[data-act="eq"]')
                        c = await page.evaluate("[JPIB.ui.calc().display().result, document.getElementById('answer').value]")
                        if c != ["42", ""]:
                            out.append("%s: with the display selected, 7 × 6 = gave %r (calculator, answer)" % (where, c))
                        await page.tap("#answer")
                        if (await page.evaluate(ANSWER_JS))["target"] != "answer":
                            out.append("%s: tapping the answer box again did not select it" % where)
                    for ch in raw:
                        await page.tap('.maffs-calc-key[data-val="%s"]' % ch)
                    typed = await page.evaluate("document.getElementById('answer').value")
                    if typed != raw:
                        out.append("%s: typing %r on the keypad put %r in the answer box" % (where, raw, typed))
                    if not calc_open:
                        await page.tap(".maffs-calc-close")
                # Check, with the calculator open on even questions and closed on odd ones. Right answers too:
                # "Spotted it?" (round 1 triples) and, every fifth question, the quick tick.
                if not desk and calc_open and i % 3 != 2:
                    # The student scrolled down to use the calculator and pressed Check from there: with the
                    # answer box at the top of the window and the calculator below it (the usual case), or
                    # all the way down. The question text folds away on Check, so the feedback moves.
                    await page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)" if i % 3 else
                                        "window.scrollTo(0, document.getElementById('answerForm').getBoundingClientRect().top + scrollY - 8)")
                    await page.evaluate("document.getElementById('submitBtn').click()")
                elif desk:
                    await page.click("#submitBtn")
                else:
                    await page.tap("#submitBtn")
                await page.wait_for_selector("#feedback .fb-quick" if kind == "quick" else "#feedback .maffs-next")
                fb = await page.evaluate(SETTLED_FB_JS)
                where_fb = "%s, %s answer, calculator %s" % (where, kind, "open" if calc_open else "closed")
                if fb is None:
                    out.append("%s: the feedback was gone before it could be measured" % where_fb)
                else:
                    fbworst[(w, h)] = max(fbworst.get((w, h), 0), fb["bottom"])
                    if fb["top"] < -0.5 or fb["bottom"] > h - FOOTER + 0.5:
                        out.append("%s: the feedback is at y=%.0f..%.0f, not fully in view (fold %d)"
                                   % (where_fb, fb["top"], fb["bottom"], h - FOOTER))
                    if desk and fb["scrollY"] > 0.5:
                        out.append("%s: the page is scrolled %.0fpx (a desktop must show the feedback without scrolling)"
                                   % (where_fb, fb["scrollY"]))
                    if fb["sw"] > fb["iw"]:
                        out.append("%s: the page is %dpx wide" % (where_fb, fb["sw"]))
                    if kind != "quick":
                        if fb["calc"] and not desk:
                            out.append("%s: the calculator shows with the feedback on a phone" % where_fb)
                        if desk and calc_open and not fb["calc"]:
                            out.append("%s: the docked calculator vanished with the feedback" % where_fb)
                        worst[(w, h)] = max(worst.get((w, h), 0), fb["next"])
                        if fb["next"] > h - FOOTER:
                            out.append("%s: Next ends at %.0fpx, below the fold (%dpx)" % (where_fb, fb["next"], h - FOOTER))
                if kind == "wrong" and (w, h) not in glided:
                    # The safety net, once per size: push the feedback out of view (a spacer makes the page
                    # long enough) and ask the page to bring it back. Phones glide to it; a desktop, where
                    # the layout guarantees it, never scrolls.
                    glided.add((w, h))
                    await page.evaluate("""() => { const d = document.createElement('div'); d.id = '__spacer';
                      d.style.height = '3000px'; document.body.appendChild(d);
                      const r = document.querySelector('#feedback .fb').getBoundingClientRect();
                      document.documentElement.scrollTop = r.bottom + scrollY + 200; }""")
                    before_y = await page.evaluate("scrollY")
                    await page.evaluate("JPIB.ui.feedbackInView()")
                    g = await page.evaluate(SETTLED_FB_JS)
                    if desk:
                        if abs(g["scrollY"] - before_y) > 0.5:
                            out.append("%s: on a desktop the page scrolled to the feedback (only phones may)" % where_fb)
                    elif g["top"] < -0.5 or g["bottom"] > h - FOOTER + 0.5:
                        out.append("%s: pushed out of view, the feedback was not brought back (y=%.0f..%.0f)"
                                   % (where_fb, g["top"], g["bottom"]))
                    await page.evaluate("document.getElementById('__spacer').remove(); document.documentElement.scrollTop = 0")
                measured += 1
                if kind == "quick":
                    await wait_next_question(page, i)
                else:
                    await page.click("#feedback .maffs-next")
                    await wait_next_question(page, i)
            for e in errors:
                out.append("%dx%d page error: %s" % (w, h, e))
        finally:
            await ctx.close()
    if not report:
        return measured
    print("Phone, keypad open: " + ", ".join(
        ("%dx%d %s %.0fpx" % (k[0], k[1], "keypad bottom (fold %d)" % (k[1] - FOOTER) if k[2] == "full" else "answer row to keypad (window %d)" % (k[1] - FOOTER), v))
        for k, v in sorted(compactworst.items())))
    print("Feedback after Check, lowest bottom: " + ", ".join("%dx%d %.0fpx (fold %d)" % (w, h, v, h - FOOTER)
                                                              for (w, h), v in sorted(fbworst.items())))
    print("Lowest Next: " + ", ".join("%dx%d %.0fpx (fold %d)" % (w, h, v, h - FOOTER) for (w, h), v in sorted(worst.items())))
    print("Tap step, lowest of triangle/Check: " + ", ".join("%dx%d %.0fpx" % (w, h, v) for (w, h), v in sorted(tapworst.items())))
    print("Asking, lowest Check (calculator open or closed, as at scroll 0): " +
          ", ".join("%dx%d %.0fpx (fold %d)" % (w, h, v, h - FOOTER) for (w, h), v in sorted(checkworst.items())))
    print("Calculator open, lowest panel bottom (phones: the page scrolls to it; desktops: docked): " +
          ", ".join("%dx%d %.0fpx" % (w, h, v) for (w, h), v in sorted(calcworst.items())))
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
    ("tap targets mapped to the wrong side",
     "(function(){ var o = JPIB.sideAt; JPIB.sideAt = function (L, x, y) { var h = o(L, x, y);"
     " if (h.side === 'p') h.side = 'r'; else if (h.side === 'r') h.side = 'p'; return h; }; })();"),
    ("a leg accepted as the hypotenuse",
     "JPIB.isHypTap = function () { return true; };"),
    ("thin round-1 triangles not widened (targets too small)",
     "JPIB.MIN_RATIO_TAP = 0.25;"),
    ("unknown side's label styled differently",
     "(function(){ var o = JPIB.svg; JPIB.svg = function (q) { var r = o(q);"
     " r.html = r.html.replace(/<text class=\"tri-label\"([^>]*)>(x|\\?)</, '<text class=\"tri-label unknown\"$1>$2<');"
     " return r; }; })();"),
    ("no hypotenuse along the bottom",
     "(function(){ var o = JPIB.positionPlan; JPIB.positionPlan = function (rng) { var p = o(rng);"
     " var f = function (x) { return x === 'Hb' ? 'Ht' : x; }; return { a: p.a.map(f), b: p.b.map(f) }; }; })();"),
    ("one position over 40%",
     "(function(){ var o = JPIB.positionPlan; JPIB.positionPlan = function (rng) { var p = o(rng);"
     " var f = function (x) { return x === 'Ht' || x === 'Vr' ? 'Hb' : x; }; return { a: p.a.map(f), b: p.b.map(f) }; }; })();"),
    ("the box ignores the figure's width",
     "JPIB.box = function (Q) { return { w: 360, h: 230, font: 19 }; };"),
    ("the triangle not grown to the box",
     "(function(){ var o = JPIB.layout; JPIB.layout = function (q, b) { b = b || JPIB.box(q, JPIB.REF.w, JPIB.REF.vh);"
     " var L = o(q, { w: b.w * 0.6, h: b.h * 0.6, font: b.font }); L.vb = [b.w, b.h]; return L; }; })();"),
    ("round 1's compact triangle too small to tap",
     "JPIB.BOX_H_COMPACT = { a: 60, b: 165, c: 165 };"),
    ("the hypotenuse slopes one way only",
     "(function(){ var o = JPIB.positionPlan; JPIB.positionPlan = function (rng) { var p = o(rng);"
     " var f = function (x) { return x === 'BR' || x === 'TL' ? 'BL' : x; }; return { a: p.a.map(f), b: p.b.map(f) }; }; })();"),
]


# Planted layout faults: each must fail the fit run. Round 1's first triangles (a "Spotted it?"), the
# roofs and the fields (the longest prompts, both types: the worked example) and a spread of the rest.
# Each planted layout fault runs on a short question set at the sizes it concerns: round 1's first
# triangles (a "Spotted it?"), every twelfth shape, and the roofs (the longest prompts, both types).
UI_FAULT_ONLY = "(q, i) => i % 12 === 0 || q.context === 'roof'"
DESK, PHONE, SMALL = [(1366, 768)], [(390, 844)], [(320, 568)]
UI_FAULTS = [
    ("phone: no glide to the feedback", SMALL,
     ("script", "window.scrollTo = function (a, b) { if (a === 0 && b === 0 && typeof a === 'number') document.documentElement.scrollTop = 0; };")),
    ("desktop: the page scrolls to the feedback", DESK, ("script", "JPIB.ui.calc().isDocked = function () { return false; };")),
    ("desktop: the feedback pushed below the fold", DESK,
     ("style", "@media (max-height:800px){.qcard.fb-open .fig-wrap{order:0!important}.qcard.fb-open .prompt{display:block!important}}"
               ".qcard.fb-open .fig svg{max-height:none!important}")),
    ("desktop: the calculator not docked", DESK, ("script", "MaffsCalc.DOCK.min = 5000;")),
    ("desktop: docked over the game column", DESK, ("style", ".maffs-calc.docked .maffs-calc-rail{left:40%!important}")),
    ("desktop: the dock pushes the column", DESK, ("style", ".maffs-calc.docked .maffs-calc-rail{position:static!important}")),
    ("desktop: the answer box no longer focused", DESK,
     ("script", "JPIB.ui.calc().answerMode = function () { return true; };")),
    ("phone: the calculator docked", SMALL, ("script", "MaffsCalc.DOCK.min = -1000;")),
    ("phone: the answer box can open the system keyboard", PHONE,
     ("script", "MaffsCalc.ANSWER.readOnly = false; MaffsCalc.ANSWER.inputmode = false; JPIB.ui.calc().redock();")),
    ("phone: tapping the answer box focuses it", PHONE, ("script", "MaffsCalc.ANSWER.blur = false;")),
    ("phone: operator keys live while typing the answer", PHONE, ("script", "MaffsCalc.ANSWER.disableOps = false;")),
    ("phone: no 'typing here' cue", PHONE, ("script", "MaffsCalc.ANSWER.cue = false;")),
    ("phone: the keys type into the calculator", PHONE, ("script", "MaffsCalc.ANSWER.route = false;")),
    ("phone: tapping the display does not select it", PHONE,
     ("script", "document.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('.maffs-calc-lines')) e.stopPropagation(); }, true);")),
    ("phone: full-size triangle with the keypad open", PHONE, ("script", "JPIB.BOX_H_COMPACT = { a: 999, b: 999, c: 999 };")),
    ("phone: the Calculator button keeps its own row", PHONE,
     ("style", ".maffs-calc.compact.open .maffs-calc-toggle{display:inline-block!important}")),
    ("phone: keys under 48px", PHONE, ("style", ".maffs-calc.compact .maffs-calc-key{min-height:42px!important}")),
]


async def webkit_answer_box(pw, out):
    """The answer box in WebKit (Safari's engine) on the game page: a touch phone types through the keypad
    (read-only, inputmode none, never focused, the keypad opens on a tap, operators disabled, Check marks
    the typed answer); a desktop keeps an ordinary, focused input. WebKit cannot show a system keyboard
    here either, so this confirms the behaviour that keeps it shut, not the keyboard itself."""
    try:
        wk = await pw.webkit.launch()
    except Exception as exc:
        out.append("WebKit would not start: %s" % str(exc).splitlines()[0])
        return
    try:
        for (w, h), touch in (((390, 844), True), ((1280, 720), False)):
            at = "WebKit %dx%d %s" % (w, h, "touch" if touch else "mouse")
            ctx, page, errors = await new_page(wk, (w, h), touch=touch)
            try:
                page.set_default_timeout(8000)
                await page.evaluate(STUBS)
                await page.evaluate("JPIB.newSeed = () => 4242")
                await (page.tap if touch else page.click)("#startBtn")
                await wait_next_question(page, 0)
                await page.evaluate("JPIB.ui.tap('r')")
                q = await page.evaluate("JPIB.ui.question()")
                if touch:
                    await page.tap("#answer")
                    a = await page.evaluate(ANSWER_JS)
                    if not (a["mode"] and a["ro"] and a["im"] == "none") or a["focused"]:
                        out.append("%s: the answer box could open the system keyboard (keypad mode %s, readOnly %s, inputmode %r, focused %s)"
                                   % (at, a["mode"], a["ro"], a["im"], a["focused"]))
                    if not a["open"] or a["target"] != "answer" or a["disabled"] != OPS:
                        out.append("%s: a tap on the answer box did not open the keypad on it (open %s, target %r, disabled %r)"
                                   % (at, a["open"], a["target"], a["disabled"]))
                    for ch in q["keyText"]:
                        await page.tap('.maffs-calc-key[data-val="%s"]' % ch)
                    await page.tap("#submitBtn")
                else:
                    a = await page.evaluate(ANSWER_JS)
                    if a["mode"] or a["ro"] or a["im"] == "none" or not a["focused"]:
                        out.append("%s: the desktop answer box is not an ordinary focused input (keypad mode %s, readOnly %s, inputmode %r, focused %s)"
                                   % (at, a["mode"], a["ro"], a["im"], a["focused"]))
                    await page.keyboard.type(q["keyText"])
                    await page.keyboard.press("Enter")
                await page.wait_for_function("JPIB.ui.state() !== 'asking'")
                if await page.evaluate("JPIB.ui.state()") != "right":
                    out.append("%s: the right answer, typed, was not marked right (state %s)" % (at, await page.evaluate("JPIB.ui.state()")))
                for e in errors:
                    out.append("%s page error: %s" % (at, e))
            except Exception as exc:
                out.append("%s: broke: %s" % (at, str(exc).splitlines()[0]))
            finally:
                await ctx.close()
    finally:
        await wk.close()


async def measure_scale(browser):
    """Screen px per viewBox unit of a round-1 triangle on a 320px phone: what the tap test is held to."""
    ctx, page, _ = await new_page(browser, (320, 568))
    try:
        await page.evaluate(STUBS)
        await page.click("#startBtn")
        await wait_next_question(page, 0)
        return await page.evaluate("(() => { const s = document.querySelector('#fig svg');"
                                   " return s.getBoundingClientRect().width / s.viewBox.baseVal.width; })()")
    finally:
        await ctx.close()


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


# ---------------------------------------------------------------- parts (CI runs three in parallel)
#
# Since 7 Oct 2026 CI runs this script as three jobs, `--part 1` .. `--part 3` (one job took 9m41s on
# main, the critical path of every full run). Every check is a task in exactly one part, dealt by
# measured cost (7 Oct 2026, about 2.5 to 3 minutes each): the fit pass at 320 and 375 in part 1, at 390
# and 412 in part 2, at the three desktop sizes in part 3; the planted layout faults dealt in turn
# across parts 1, 2, 3 in list order; the sessions, WebKit, the play-through and the fault-injection
# self-test in part 3. Every part first reads the page's scale and compact heights, which the checks
# are held to. With no --part, every task runs, as before. --part-selftest proves that the parts
# together are exactly the unsplit task list, nothing twice, and that the workflow runs every part.
PARTS = ("1", "2", "3")
FIT_PART = {(320, 568): "1", (375, 667): "1", (390, 844): "2", (412, 915): "2",
            (1280, 720): "3", (1366, 768): "3", (1920, 1080): "3"}
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "check-site.yml")


def plan(no_phone=False, no_selftest=False):
    """[(task, part)] in the order the unsplit script ran them."""
    tasks = [("sessions", "3"), ("webkit", "3"), ("play-through", "3")]
    if not no_phone:
        tasks += [("fit %dx%d" % sz, FIT_PART[sz]) for sz in PHONES + DESKTOPS]
    if not no_selftest and not no_phone:
        tasks += [("layout fault: " + name, PARTS[i % len(PARTS)]) for i, (name, _, _) in enumerate(UI_FAULTS)]
    if not no_selftest:
        tasks += [("fault-injection self-test", "3")]
    return tasks


def split_faults(every, parts):
    """What is wrong with `parts` ({part: [task]}) as a split of `every` ([(task, part)]): [] if nothing."""
    fails, seen = [], {}
    for p, tasks in sorted(parts.items()):
        for t in tasks:
            if t in seen:
                fails.append("%s is in part %s and part %s" % (t, seen[t], p))
            seen[t] = p
    dropped = [t for t, _ in every if t not in seen]
    if dropped:
        fails.append("in no part: %s" % ", ".join(dropped))
    extra = [t for t in seen if t not in {t for t, _ in every}]
    if extra:
        fails.append("not in the unsplit run: %s" % ", ".join(extra))
    if len({t for t, _ in every}) != len(every):
        fails.append("a task is listed twice in the unsplit run")
    return fails


def part_selftest():
    fails = []
    for flags in ((False, False), (True, False), (False, True), (True, True)):
        every = plan(*flags)
        for f in split_faults(every, {p: [t for t, q in every if q == p] for p in PARTS}):
            fails.append("with --no-phone %s --no-selftest %s: %s" % (flags + (f,)))
    every = plan()
    parts = {p: [t for t, q in every if q == p] for p in PARTS}
    print("Parts: %s" % "; ".join("part %s %d tasks" % (p, len(parts[p])) for p in PARTS))
    # Planted faults, each must be caught: a task dropped from part 1, a part-1 task copied into part 2.
    for name, bad in (("a task dropped", dict(parts, **{"1": parts["1"][1:]})),
                      ("a task in two parts", dict(parts, **{"2": parts["2"] + parts["1"][:1]}))):
        caught = bool(split_faults(every, bad))
        print("  planted: %-22s %s" % (name, "caught" if caught else "*** MISSED ***"))
        if not caught:
            fails.append("self-test: %s was not caught" % name)
    if os.path.exists(WORKFLOW):
        with open(WORKFLOW, encoding="utf-8") as fh:
            runs = re.findall(r"python scripts/verify-just-pythag-it-bruv\.py\b([^\n|&]*)", fh.read())
        got = sorted(m.group(1) for m in (re.search(r"--part (\w+)", r) for r in runs) if m)
        whole = [r.strip() for r in runs if "--part" not in r]
        if got != sorted(PARTS):
            fails.append("the workflow runs parts %s, not %s" % (got, sorted(PARTS)))
        if whole:
            fails.append("the workflow also runs the unsplit script: %s" % whole)
        print("  workflow runs parts: %s" % (", ".join(got) or "none"))
    for f in fails:
        print("FAIL  " + f)
    print("Part self-test: %s" % ("FAILED" if fails else "PASS"))
    return 1 if fails else 0


async def run_all(args):
    from playwright.async_api import async_playwright
    todo = [t for t, q in plan(args.no_phone, args.no_selftest) if args.part in (None, q)]
    if args.part:
        print("Part %s: %d of %d tasks" % (args.part, len(todo), len(plan(args.no_phone, args.no_selftest))))
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        global SCALE_320
        SCALE_320 = await measure_scale(browser)
        ctx0, page0, _ = await new_page(browser)
        page_h = await page0.evaluate("JPIB.BOX_H_COMPACT")
        await ctx0.close()
        if page_h != COMPACT_H:
            fail("the page's compact triangle heights %r differ from this script's COMPACT_H %r: update both" % (page_h, COMPACT_H))
        print("Round-1 triangle at 320px: %.3f px per unit (tap target: the middle %dpx of each side, 6px in to 22px out)"
              % (SCALE_320, 2 * TAP_RADIUS_PX))
        if "sessions" in todo:
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

        if "webkit" in todo:
            wk_out = []
            await webkit_answer_box(pw, wk_out)
            for f in wk_out:
                fail(f)
            print("WebKit: the answer box on a touch phone (keypad only, never focused) and on a desktop (ordinary input)")

        if "play-through" in todo:
            ui_out = []
            n_add = await ui_playthrough(browser, ui_out)
            for f in ui_out:
                fail(f)
            print("UI play-through (Firebase SDK blocked): 20 questions, %d add errors (3 worked examples, then "
                  "the nudge); format and unreadable answers not marked; events and one score to %s" % (n_add, LEVEL))

        sizes = [sz for sz in PHONES + DESKTOPS if "fit %dx%d" % sz in todo]
        if sizes:
            ph_out = []
            n = await phone_fit(browser, ph_out, sizes=sizes)
            for f in ph_out:
                fail(f)
            print("Fit: %d feedback screens (wrong, quick tick, Spotted it?; calculator open and closed) at %s"
                  % (n, ", ".join("%dx%d" % p for p in sizes)))

        faults = [(name, sizes, patch) for name, sizes, patch in UI_FAULTS if "layout fault: " + name in todo]
        if faults:
            print()
            print("Layout faults (a short run at the size each concerns, each patched into a fresh page):")
            for name, sizes, patch in faults:
                found = []
                try:
                    await phone_fit(browser, found, sizes=sizes, only=UI_FAULT_ONLY, patch=patch, report=False)
                except Exception as exc:          # a fault that breaks the page outright is caught too
                    found.append("the run broke: %s" % str(exc).splitlines()[0])
                print("  %-48s %s" % (name, ("CAUGHT (%d failures, e.g. %s)" % (len(found), found[0][:90])) if found else "*** MISSED ***"))
                if not found:
                    fail("layout fault not caught: " + name)

        if "fault-injection self-test" in todo:
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
    ap.add_argument("--part", choices=PARTS, help="run one of the three parts CI runs in parallel (default: all)")
    ap.add_argument("--part-selftest", action="store_true",
                    help="prove the parts together run every task once, and the workflow runs every part; no browser")
    args = ap.parse_args()
    if args.part_selftest:
        return part_selftest()
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
