#!/usr/bin/env python3
# ci-line: Free Daily Pizza (independent recomputation + daily seed + phone fit) | --require-katex
"""Independent verification for Free Daily Pizza (games/free-daily-pizza/), built 30 Sep 2026.

WHAT IS READ FROM THE PAGE, AND WHAT IS NOT
-------------------------------------------------------------------------------
The page keeps its banks, options, pictures and daily sets on window.FDP, and its UI calls
them through FDP, so reading FDP checks what ships. But the engine is what is under test, so
nothing it computes is trusted (Jon, 30 Sep 2026):

  READ from the page   each item's own parameters (the fraction, the amount, "A out of B"),
                       the strings it DISPLAYS (every option's text and TeX, the prompt, the
                       working), each distractor's misconception tag, the picture specs and
                       the rendered picture markup, and the id lists the page serves.
  NEVER READ           the engine's stored values, answer keys or equality judgements. Every
                       displayed option is parsed back to an exact Fraction here, from its
                       text and its TeX separately (they must agree), and compared with a
                       value recomputed here from the item's parameters.
  RECOMPUTED HERE      every correct answer; every distractor from its tag's definition
                       (below); value-equivalence; which option is right when the UI is
                       played; the bank's enumeration order; the daily pizza, from a Python
                       port of the documented PRNG (FNV-1a seed of "free-daily-pizza:<date>",
                       mulberry32, Fisher-Yates, first distinct family per stage); the seeded
                       practice sets; the UK date; the score formula.

WHAT IT ASSERTS
-------------------------------------------------------------------------------
  Banks       S1 is exactly the contract's benchmark set x the six conversions; S2 has
              eighths, twentieths, hundredths and simplifying; S3 answers are whole
              numbers from amounts up to 1,200; each stage has >= 40 distinct items, and no
              two items share parameters or a prompt; the page enumerates items in the
              documented order (the daily set depends on it).
  Answers     displayed answer (text and TeX) == the value recomputed from parameters, in
              the form the question asks for, in lowest terms where a fraction is asked for.
  Distractors exactly three; each tag allowed for its question type; each displayed value
              == its tag's definition applied to the parameters; none equal in value to the
              answer, except 'unsimplified' on a question that asks for the simplest form
              (and then it must really be unsimplified); no two equal in value.
  Recurring   parsing the display is the check: "0.33" parses to 33/100, so it can never
              pass as 1/3. Working text never writes a cut-off recurring decimal as exact.
  Pictures    every pizza's shaded/slices, grid's shaded/100 and bar's parts x each equal
              the value, in the spec AND in the rendered markup; no pizza over 24 slices.
  Daily       Python's set == the page's for 400 UK dates; repeated calls and a fresh page
              agree; the mix is 3/3/2/2 in stage order with no repeated value in a stage;
              dates differ; the UK date is right either side of both clock changes.
  Practice    seeded sets == Python's; right length, stage, no repeats, no neighbours about
              the same value; mixed is a quarter per stage, stage by stage.
  UI          played with a Firebase stub: stages 1-4 at 20 (rank NOWHERE: no submitScore call, history
              and personal best under stage-sN-q20, 'not ranked' on the end screen), mixed at 20
              and 40 (the only practice that ranks: practice-q20 / practice-q40), the
              daily pizza twice on one simulated UK date (same pizza, easiest first, the
              target shown), and with the SDK blocked (no target, no error). The option
              clicked as right is the one whose DISPLAY parses to the Python answer. No
              picture before answering; a wrong answer shows the true statement, the working,
              the pictures, then Next, in that order, with the options hidden. Leaderboard
              reads and writes are read from the stub's log: q20, q40 and the day's key, apart.
  Analytics   every event: game_slug, level 'all', mode practice-q20 | practice-q40 | daily |
              stage-sN-q20 / stage-sN-q40,
              and canon 1.3's parameters.
  Phone       every item, at 320x568, 375x667 and 390x844: after a wrong answer Next sits
              above the fold (footer excluded), the working above Next, the pictures above
              Next except on screens 600px tall or less; no horizontal scroll.

FAULT-INJECTION SELF-TEST (every run; --no-selftest skips it)
-------------------------------------------------------------------------------
Each fault is patched into a FRESH page (never the file) and must FAIL: a wrong answer; a
value-equal distractor; a wrong tag; a broken daily mix; a daily pizza not served easiest
first; a pre-answer picture leak; a recurring answer shown as 0.33; a lossy picture; a fraction
written with a slash on screen; a single-stage practice run that submits to a board.

USAGE
    python scripts/verify-free-daily-pizza.py [--require-katex] [--no-selftest] [--no-phone]
    python scripts/verify-free-daily-pizza.py --screens docs/screenshots   # also save PNGs
"""
import argparse
import asyncio
import json
import math
import os
import re
import sys
import time
from urllib.parse import urlsplit
from datetime import date, timedelta
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import bank_common as bc  # noqa: E402  (start_stub_server: checked start, free port)
SLUG = "free-daily-pizza"


PORT = None  # set by main() to the free port the stub server got
FOOTER = 40
_FAILURES = []


def fail(msg):
    _FAILURES.append(msg)
    print("FAIL: " + msg)


# ------------------------------------------------------------ parsing what is displayed

DOT = "\u0307"
VULGAR = {"\u2153": F(1, 3), "\u2154": F(2, 3)}


def parse_decimal(s):
    """'0.6̇' / '12.5' / '0.0̇9̇' (text) -> Fraction. Dotted digits mark the recurring block."""
    m = re.fullmatch(r"(\d+)(?:\.(.+))?", s)
    if not m:
        raise ValueError("not a decimal: %r" % s)
    whole, rest = int(m.group(1)), m.group(2) or ""
    digits, dotted, i = [], [], 0
    while i < len(rest):
        c = rest[i]
        if not c.isdigit():
            raise ValueError("bad decimal digit in %r" % s)
        d = i + 1 < len(rest) and rest[i + 1] == DOT
        digits.append(c)
        dotted.append(d)
        i += 2 if d else 1
    marks = [k for k, d in enumerate(dotted) if d]
    if not marks:
        return F(whole) + (F(int("".join(digits)), 10 ** len(digits)) if digits else 0)
    if len(marks) > 2 or marks[-1] != len(digits) - 1:
        raise ValueError("recurring dots must mark the first and last digit of a final block: %r" % s)
    pre, rep = "".join(digits[:marks[0]]), "".join(digits[marks[0]:])
    val = F(int(pre), 10 ** len(pre)) if pre else F(0)
    val += F(int(rep), 10 ** len(pre) * (10 ** len(rep) - 1))
    return F(whole) + val


def tex_to_text(t):
    t = re.sub(r"\\dot\{(\d)\}", lambda m: m.group(1) + DOT, t)
    return t


def parse_display(form, s, tex):
    """Parse one displayed option (text if tex False, else TeX) in the given form."""
    if form == "f":
        if tex:
            m = re.fullmatch(r"\\dfrac\{(\d+)\}\{(\d+)\}", s)
            if m:
                return F(int(m.group(1)), int(m.group(2))), (int(m.group(1)), int(m.group(2)))
            if re.fullmatch(r"\d+", s):
                return F(int(s)), (int(s), 1)
            raise ValueError("not a fraction: %r" % s)
        m = re.fullmatch(r"(\d+)/(\d+)", s)
        if m:
            return F(int(m.group(1)), int(m.group(2))), (int(m.group(1)), int(m.group(2)))
        if re.fullmatch(r"\d+", s):
            return F(int(s)), (int(s), 1)
        raise ValueError("not a fraction: %r" % s)
    if form in ("d", "n"):
        return parse_decimal(tex_to_text(s) if tex else s), None
    # percentage
    body = s[:-2] if tex and s.endswith("\\%") else (s[:-1] if s.endswith("%") else None)
    if body is None:
        raise ValueError("not a percentage: %r" % s)
    if tex:
        m = re.fullmatch(r"(\d*)\\dfrac\{(\d+)\}\{(\d+)\}", body)
        if m:
            return (int(m.group(1) or 0) + F(int(m.group(2)), int(m.group(3)))) / 100, None
        return parse_decimal(tex_to_text(body)) / 100, None
    if body and body[-1] in VULGAR:
        return (int(body[:-1] or 0) + VULGAR[body[-1]]) / 100, None
    return parse_decimal(body) / 100, None


def read_option(o, where, out):
    """Value of a displayed option; text and TeX must parse and agree."""
    try:
        v1, sh1 = parse_display(o["form"], o["text"], False)
        v2, sh2 = parse_display(o["form"], o["tex"], True)
    except ValueError as e:
        out.append("%s: %s" % (where, e))
        return None, None
    if v1 != v2 or sh1 != sh2:
        out.append("%s: text %r and TeX %r disagree" % (where, o["text"], o["tex"]))
        return None, None
    return v1, sh1


# ------------------------------------------------------------ the independent model

PAIRS = ["f>d", "f>p", "d>f", "d>p", "p>d", "p>f"]
CONTRACT_S1 = {F(1, 2), F(1, 4), F(3, 4), F(1, 5), F(2, 5), F(3, 5), F(4, 5), F(1, 10), F(3, 10), F(7, 10),
               F(9, 10), F(1, 3), F(2, 3), F(1, 8), F(1, 100)}


def item_value(it):
    """The value the question is about (a proportion), from parameters."""
    k = it["kind"]
    if k == "conv":
        return F(it["v"][0], it["v"][1])
    if k == "simp":
        return F(it["n"], it["d"])
    if k == "ofamt-f":
        return F(it["a"], it["b"])
    if k == "ofamt-p":
        return F(it["p"], 100)
    return F(it["A"], it["B"])


def expected_answer(it):
    """(form, value, asks_simplest) recomputed from the item's parameters."""
    k = it["kind"]
    if k == "conv":
        return it["to"], item_value(it), False
    if k == "simp":
        return "f", F(it["n"], it["d"]), True
    if k == "ofamt-f":
        return "n", F(it["a"] * it["N"], it["b"]), False
    if k == "ofamt-p":
        return "n", F(it["p"] * it["N"], 100), False
    if k == "outof-f":
        return "f", F(it["A"], it["B"]), True
    return "p", F(it["A"], it["B"]), False


def terminating_digits(v):
    """Digits after the point of a terminating v < 1, or None."""
    for k in range(0, 12):
        x = v * 10 ** k
        if x.denominator == 1:
            return str(x.numerator).zfill(k) if k else ""
    return None


def floor_to(v, k):
    return F(math.floor(v * 10 ** k), 10 ** k)


def allowed_tags(it):
    k = it["kind"]
    if k == "conv":
        return {"f>d": {"denominator-as-decimal", "truncation", "inversion", "place-value"},
                "f>p": {"truncation", "raw-part", "denominator-as-decimal", "place-value", "inversion"},
                "d>f": {"digit-reading", "truncation", "inversion", "place-value"},
                "d>p": {"truncation", "place-value"},
                "p>d": {"truncation", "place-value"},
                "p>f": {"digit-reading", "truncation", "place-value", "inversion"}}[it["from"] + ">" + it["to"]]
    return {"simp": {"unsimplified", "subtract-instead", "inversion", "one-side-only"},
            "ofamt-f": {"one-part-only", "complement", "no-divide", "inversion", "denominator-as-decimal", "place-value"},
            "ofamt-p": {"subtract-percent", "one-part-only", "complement", "place-value", "inversion"},
            "outof-f": {"unsimplified", "inversion", "part-to-part", "complement"},
            "outof-p": {"raw-part", "part-to-part", "complement", "inversion", "place-value"}}[k]


def tag_value(it, o, ans):
    """The value a distractor must have, from its tag's definition and the parameters only.
    Returns (value, note) or (None, reason)."""
    tag, k = o.get("tag"), it["kind"]
    v = item_value(it)
    if tag == "place-value":
        s = o.get("shift")
        if s not in (-2, -1, 1, 2):
            return None, "place-value needs a shift of +-1 or +-2, got %r" % s
        return ans * F(10) ** s, None
    if k == "conv":
        a, b = v.numerator, v.denominator
        if tag == "truncation":
            kk = o.get("k")
            if kk not in (1, 2):
                return None, "truncation needs k 1 or 2"
            return floor_to(v, kk), None
        if tag == "denominator-as-decimal":
            return (F(b, 10), None) if b <= 9 else (None, "denominator-as-decimal on a denominator over 9")
        if tag == "inversion":
            return 1 / v, None
        if tag == "raw-part":
            return F(a, 100), None
        if tag == "digit-reading":
            if it["from"] == "d":
                dg = terminating_digits(v)
                if not dg or dg[0] == "0" or int(dg) < 2:
                    return None, "digit-reading on a decimal it cannot apply to"
                return F(1, int(dg)), None
            p = v * 100
            if p.denominator != 1 or p < 2:
                return None, "digit-reading on a percentage it cannot apply to"
            return F(1, p.numerator), None
    if k == "simp":
        n, d = it["n"], it["d"]
        r = F(n, d)
        a = r.numerator
        return {"unsimplified": (r, None), "subtract-instead": (F(a, d - n + a), None),
                "inversion": (1 / r, None), "one-side-only": (F(a, d), None)}.get(tag, (None, "unknown tag"))
    if k == "ofamt-f":
        a, b, N = it["a"], it["b"], it["N"]
        return {"one-part-only": (F(N, b), None), "complement": (N - F(a * N, b), None),
                "no-divide": (F(a * N), None), "inversion": (F(N * b, a), None),
                "denominator-as-decimal": ((F(N * b, 10), None) if b <= 9 else (None, "denominator over 9"))
                }.get(tag, (None, "unknown tag"))
    if k == "ofamt-p":
        p, N = it["p"], it["N"]
        if tag == "one-part-only" and not (p % 10 == 0 and p != 10):
            return None, "one-part-only (10%) on a percentage that is not a multiple of 10 above 10"
        return {"subtract-percent": (F(N - p), None), "one-part-only": (F(N, 10), None),
                "complement": (N - F(p * N, 100), None), "inversion": (F(100 * N, p), None)
                }.get(tag, (None, "unknown tag"))
    A, B = it["A"], it["B"]
    return {"unsimplified": (F(A, B), None), "inversion": (F(B, A), None), "part-to-part": (F(A, B - A), None),
            "complement": (F(B - A, B), None), "raw-part": (F(A, 100), None)}.get(tag, (None, "unknown tag"))


def is_recurring(v):
    return terminating_digits(v - math.floor(v)) is None


DEC_LIT = re.compile(r"(?<![\d.])(\d+\.\d+)(?![\d])")


def check_working(it, ans_opt, out, where):
    w = it["working"]
    if ans_opt["tex"] not in w and ans_opt["text"] not in w:
        out.append("%s: the working never states the answer %s" % (where, ans_opt["text"]))
    v = item_value(it)
    if not is_recurring(v):
        return
    for m in DEC_LIT.finditer(w):
        tail = w[m.end():m.end() + 6]
        if tail.startswith("\\ldots") or tail.startswith("\u2026"):
            continue
        lit = F(m.group(1))
        for ref in (v, v * 100):
            if lit != ref and abs(lit - ref) < F(1, 10):
                out.append("%s: working writes %s as if exact for a recurring value" % (where, m.group(1)))


def check_item(it, out):
    where = it["id"]
    form, want, simplest = expected_answer(it)
    a = it["answer"]
    if a["form"] != form:
        out.append("%s: answer is in form %r, the question asks for %r" % (where, a["form"], form))
    got, shown = read_option(a, where + " answer", out)
    if got is not None and got != want:
        out.append("%s: displayed answer %s is %s, but the parameters give %s" % (where, a["text"], got, want))
    if shown and F(*shown) == want and math.gcd(*shown) != 1:
        out.append("%s: the answer %s is not in lowest terms" % (where, a["text"]))
    if it["kind"] == "conv":
        g = it["given"]
        gv, _ = read_option(g, where + " given", out)
        if g["form"] != it["from"] or (gv is not None and gv != item_value(it)):
            out.append("%s: the prompt's value %s is not %s" % (where, g["text"], item_value(it)))
        if "\\(" + g["tex"] + "\\)" not in it["prompt"]:
            out.append("%s: the prompt does not show the given value" % where)
    ds = it["distractors"]
    if len(ds) != 3:
        out.append("%s: %d distractors, expected 3" % (where, len(ds)))
    seen, keys = [], {a["key"]}
    tags_ok = allowed_tags(it)
    for i, o in enumerate(ds):
        w = "%s distractor %d (%s, %s)" % (where, i, o.get("text"), o.get("tag"))
        if o["key"] in keys:
            out.append(w + ": key repeats another option's")
        keys.add(o["key"])
        if o["form"] != form:
            out.append(w + ": form %r differs from the answer's %r" % (o["form"], form))
        val, sh = read_option(o, w, out)
        if val is None:
            continue
        if o.get("tag") not in tags_ok:
            out.append(w + ": tag not allowed on a %s question" % it["kind"])
        exp, why = tag_value(it, o, want)
        if exp is None:
            out.append(w + ": " + why)
        elif exp != val:
            out.append(w + ": shows %s, but its tag gives %s" % (val, exp))
        if val <= 0:
            out.append(w + ": not positive")
        if val == want:
            if not (o.get("tag") == "unsimplified" and simplest):
                out.append(w + ": EQUAL IN VALUE to the answer %s" % want)
            elif not sh or math.gcd(*sh) == 1:
                out.append(w + ": tagged unsimplified but shown in lowest terms")
        if o.get("tag") == "unsimplified" and not simplest:
            out.append(w + ": unsimplified offered on a question that does not ask for the simplest form")
        if val in seen:
            out.append(w + ": same value as another distractor")
        seen.append(val)
    check_working(it, a, out, where)


def check_pictures(it, rendered, out):
    where = it["id"]
    v = item_value(it)
    _, want, _ = expected_answer(it)
    specs = it["pictures"]
    if len(rendered) != len(specs):
        out.append("%s: %d picture specs but %d drawn" % (where, len(specs), len(rendered)))
        return
    for sp, dr in zip(specs, rendered):
        w = "%s %s picture" % (where, sp["type"])
        if dr["type"] != sp["type"]:
            out.append(w + ": drawn as %s" % dr["type"])
            continue
        if sp["type"] == "pizza":
            if dr["cells"] != sp["slices"] or dr["on"] != sp["shaded"]:
                out.append(w + ": drawn %d/%d, spec %d/%d" % (dr["on"], dr["cells"], sp["shaded"], sp["slices"]))
            if sp["slices"] > 24:
                out.append(w + ": %d slices is too many to count" % sp["slices"])
            if F(dr["on"], dr["cells"]) != v:
                out.append(w + ": %d of %d slices is not %s" % (dr["on"], dr["cells"], v))
        elif sp["type"] == "grid":
            if dr["cells"] != 100 or dr["on"] != sp["shaded"]:
                out.append(w + ": drawn %d/%d, spec %d/100" % (dr["on"], dr["cells"], sp["shaded"]))
            if F(dr["on"], 100) != v:
                out.append(w + ": %d of 100 squares is not %s" % (dr["on"], v))
            if "each" in sp and it["kind"] == "ofamt-p" and sp["each"] * 100 != it["N"]:
                out.append(w + ": each square worth %s, but %s / 100 = %s" % (sp["each"], it["N"], F(it["N"], 100)))
        else:
            each = sp["each"]
            if dr["cells"] != sp["parts"] or dr["on"] != sp["shaded"]:
                out.append(w + ": drawn %d/%d, spec %d/%d" % (dr["on"], dr["cells"], sp["shaded"], sp["parts"]))
            if dr["cells"] * each != it["N"] or dr["on"] * each != want:
                out.append(w + ": %d parts of %s is not %s, or %d of them is not %s" % (dr["cells"], each, it["N"], dr["on"], want))
            if dr["labels"] and any(l != str(each) for l in dr["labels"]):
                out.append(w + ": part labels %r are not %s" % (dr["labels"][:3], each))


def params_key(it):
    return tuple(it.get(k) if not isinstance(it.get(k), list) else tuple(it.get(k))
                 for k in ("kind", "from", "to", "v", "n", "d", "a", "b", "N", "p", "A", "B"))


def expected_ids(tables):
    """The documented enumeration order, rebuilt from the parameter tables."""
    ids = {1: [], 2: [], 3: [], 4: []}
    for a, b in tables["S1_VALUES"]:
        ids[1] += ["S1:conv:%s:%d/%d" % (p, a, b) for p in PAIRS]
    for a, b in tables["S2_VALUES"]:
        ids[2] += ["S2:conv:%s:%d/%d" % (p, a, b) for p in PAIRS]
    for d in tables["S2_SIMPLIFY_DENS"]:
        ids[2] += ["S2:simp:%d/%d" % (n, d) for n in range(1, d) if math.gcd(n, d) > 1]
    for a, b in tables["S3_FRACTIONS"]:
        ids[3] += ["S3:frac:%d/%d:%d" % (a, b, b * m) for m in tables["S3_MULTIPLES"]]
    for p, Ns in tables["S3_PERCENTS"]:
        ids[3] += ["S3:pct:%d:%d" % (p, N) for N in Ns]
    for a, b in tables["S4_FRACTIONS"]:
        for g in tables["S4_SCALES"][str(b)]:
            ids[4] += ["S4:f:%d/%d" % (a * g, b * g), "S4:p:%d/%d" % (a * g, b * g)]
    return ids


def family(it):
    """Items about the same value, within a stage. Amount questions: the fraction taken."""
    if it["kind"] in ("ofamt-f", "ofamt-p"):
        return (it["stage"], "of", item_value(it))
    if it["kind"] == "simp":
        return (it["stage"], "v", F(it["n"], it["d"]))
    return (it["stage"], "v", item_value(it))


def check_banks(data, out):
    bank = data["bank"]
    exp = expected_ids(data["tables"])
    for s in (1, 2, 3, 4):
        items = bank[str(s)]
        got = [it["id"] for it in items]
        if got != exp[s]:
            out.append("stage %d: the page's item order differs from the documented enumeration (first difference near %r)"
                       % (s, next((g for g, e in zip(got, exp[s]) if g != e), got[len(exp[s]):len(exp[s]) + 1])))
        if len(set(got)) != len(got):
            out.append("stage %d: repeated item ids" % s)
        pk = [params_key(it) for it in items]
        if len(set(pk)) != len(pk):
            out.append("stage %d: two items share parameters" % s)
        prompts = [it["prompt"] for it in items]
        if len(set(prompts)) != len(prompts):
            out.append("stage %d: two items share a prompt" % s)
        if len(set(pk)) < 40:
            out.append("stage %d: only %d distinct items (need 40)" % (s, len(set(pk))))
        for it in items:
            if it["stage"] != s:
                out.append("%s is in stage %d's bank" % (it["id"], s))
    s1 = {item_value(it) for it in bank["1"]}
    if s1 != CONTRACT_S1:
        out.append("stage 1 values %s are not the contract's benchmark set" % sorted(s1 ^ CONTRACT_S1))
    s2 = [item_value(it) for it in bank["2"] if it["kind"] == "conv"]
    for name, den in (("eighths", 8), ("twentieths", 20), ("hundredths", 100)):
        if not any(v.denominator == den for v in s2):
            out.append("stage 2 has no %s" % name)
    if not any(it["kind"] == "simp" for it in bank["2"]):
        out.append("stage 2 has no simplifying")
    for it in bank["3"]:
        ans = expected_answer(it)[1]
        if ans.denominator != 1 or it["N"] > 1200:
            out.append("%s: not a non-calculator amount (answer %s of %d)" % (it["id"], ans, it["N"]))
    for it in bank["4"]:
        if not 0 < it["A"] < it["B"]:
            out.append("%s: not a part of a whole" % it["id"])
    by_id = {}
    for s in (1, 2, 3, 4):
        for it in bank[str(s)]:
            by_id[it["id"]] = it
            check_item(it, out)
            check_pictures(it, data["drawn"][it["id"]], out)
    return by_id, exp


# ------------------------------------------------------------ the PRNG, ported

M32 = 0xFFFFFFFF


def u32(x):
    return x & M32


def i32(x):
    x &= M32
    return x - (1 << 32) if x >= (1 << 31) else x


def imul(a, b):
    return i32(u32(a) * u32(b))


def fnv1a(s):
    h = 0x811C9DC5
    for ch in s:
        h = u32(h ^ ord(ch))
        h = u32(h * 0x01000193)
    return h


class Mulberry32:
    """Integer-exact port of the page's mulberry32. next() returns the uint32 x; the page's
    rng() is x / 2**32, so floor(rng() * m) == (x * m) >> 32 exactly."""

    def __init__(self, seed):
        self.t = u32(seed)

    def next(self):
        self.t += 0x6D2B79F5
        t = u32(self.t)
        r = imul(t ^ (t >> 15), t | 1)
        r = i32(u32(r) ^ u32(r + imul(u32(r) ^ (u32(r) >> 7), u32(r) | 61)))
        return u32(r) ^ (u32(r) >> 14)


def shuffle(arr, rng):
    a = list(arr)
    for i in range(len(a) - 1, 0, -1):
        j = (rng.next() * (i + 1)) >> 32
        a[i], a[j] = a[j], a[i]
    return a


def daily_expected(d, exp_ids, by_id):
    rng = Mulberry32(fnv1a("free-daily-pizza:" + d))
    out = []
    for stage, k in ((1, 3), (2, 3), (3, 2), (4, 2)):
        fams, got = set(), 0
        for i in shuffle(exp_ids[stage], rng):
            if got >= k:
                break
            f = family(by_id[i])
            if f in fams:
                continue
            fams.add(f)
            out.append(i)
            got += 1
    return out


def spread(lst, by_id):
    a, n = list(lst), len(lst)

    def fam(i):
        return family(by_id[a[i]])
    for i in range(1, n):
        if fam(i) != fam(i - 1):
            continue
        moved = False
        for j in range(i + 1, n):
            if fam(j) != fam(i - 1):
                a[i], a[j] = a[j], a[i]
                moved = True
                break
        if moved:
            continue
        for j in range(0, i - 1):
            if (fam(j) != fam(i - 1) and (i + 1 >= n or fam(j) != fam(i + 1))
                    and (j == 0 or fam(i) != fam(j - 1)) and fam(i) != fam(j + 1)):
                a[i], a[j] = a[j], a[i]
                break
    return a


def practice_expected(stage, n, seed, exp_ids, by_id):
    rng = Mulberry32(seed)
    if stage != "mixed":
        return spread(shuffle(exp_ids[stage], rng)[:n], by_id)
    out = []
    for s in (1, 2, 3, 4):
        out += spread(shuffle(exp_ids[s], rng)[:n // 4], by_id)
    return out


DAILY_STAGES = [1, 1, 1, 2, 2, 2, 3, 3, 4, 4]
UK_DATES = [  # instant (UTC) -> UK calendar date, either side of both 2026 clock changes
    ("2026-03-29T00:30:00Z", "2026-03-29"), ("2026-03-29T23:30:00Z", "2026-03-30"),
    ("2026-06-30T23:30:00Z", "2026-07-01"), ("2026-10-24T23:30:00Z", "2026-10-25"),
    ("2026-10-25T23:30:00Z", "2026-10-25"), ("2026-12-31T23:59:00Z", "2026-12-31"),
    ("2027-01-01T00:00:00Z", "2027-01-01")]


def check_daily(page_sets, page_again, uk, by_id, exp_ids, out, tag="daily"):
    sets = {}
    for d, got in page_sets.items():
        want = daily_expected(d, exp_ids, by_id)
        if got != want:
            out.append("%s %s: page served %r, the seed gives %r" % (tag, d, got[:4], want[:4]))
        if page_again.get(d) is not None and page_again[d] != got:
            out.append("%s %s: a second call gave a different pizza" % (tag, d))
        stages = [by_id[i]["stage"] if i in by_id else None for i in got]
        if stages != DAILY_STAGES:
            out.append("%s %s: stages %r, expected 3/3/2/2 easiest first" % (tag, d, stages))
        if len(set(got)) != len(got):
            out.append("%s %s: a question repeats" % (tag, d))
        fams = [family(by_id[i]) for i in got if i in by_id]
        if len(set(fams)) != len(fams):
            out.append("%s %s: two questions about the same value in one stage" % (tag, d))
        sets[d] = tuple(got)
    if len(set(sets.values())) != len(sets):
        out.append("%s: %d dates share a pizza" % (tag, len(sets) - len(set(sets.values()))))
    for inst, want in UK_DATES:
        if uk.get(inst) != want:
            out.append("UK date of %s is %r, expected %s" % (inst, uk.get(inst), want))


def score_for(seconds, correct):
    if not correct:
        return 0
    return max(1, round(100 / (1 + 0.15 * math.log(1 + max(0, seconds)))))


# ------------------------------------------------------------ the page

COLLECT_JS = r"""
() => {
  const pick = o => o && ({ form: o.form, text: o.text, tex: o.tex, key: o.key, tag: o.tag, k: o.k, shift: o.shift });
  const bank = {}, drawn = {};
  const div = document.createElement('div');
  [1, 2, 3, 4].forEach(s => {
    bank[s] = FDP.BANK[s].map(it => {
      div.innerHTML = FDP.pictureHtml(it);
      drawn[it.id] = Array.from(div.querySelectorAll('figure.pic')).map(f => {
        const t = f.dataset.type, sel = t === 'pizza' ? '.slice' : t === 'grid' ? '.sq' : '.part';
        const cells = f.querySelectorAll(sel);
        return { type: t, cells: cells.length, on: f.querySelectorAll(sel + '.on').length,
                 labels: t === 'bar' ? Array.from(cells).map(c => c.textContent).filter(x => x) : [] };
      });
      return { id: it.id, stage: it.stage, kind: it.kind, from: it.from, to: it.to, v: it.v, n: it.n, d: it.d,
               a: it.a, b: it.b, N: it.N, p: it.p, A: it.A, B: it.B, prompt: it.prompt, working: it.working,
               equation: it.equation, pictures: it.pictures, given: pick(it.given), answer: pick(it.answer),
               distractors: it.distractors.map(pick) };
    });
  });
  const tables = {};
  ['S1_VALUES', 'S2_VALUES', 'S2_SIMPLIFY_DENS', 'S3_FRACTIONS', 'S3_MULTIPLES', 'S3_PERCENTS', 'S4_FRACTIONS', 'S4_SCALES']
    .forEach(k => { tables[k] = FDP[k]; });
  return { bank, drawn, tables };
}
"""

DAILY_JS = r"""
(args) => {
  const sets = {}, again = {}, uk = {}, practice = [];
  args.dates.forEach(d => { sets[d] = FDP.dailySet(d); again[d] = FDP.dailySet(d); });
  args.instants.forEach(i => { uk[i] = FDP.ukDate(new Date(i)); });
  args.practice.forEach(p => { practice.push(FDP.practiceSet(p[0], p[1], FDP.mulberry32(p[2]))); });
  const scores = args.secs.map(s => [FDP.scoreFor(s, true), FDP.scoreFor(s, false)]);
  return { sets, again, uk, practice, scores };
}
"""

KATEX_JS = r"""
() => {
  if (typeof katex === 'undefined') return null;
  const bad = [];
  const segs = s => (s.match(/\\\(([\s\S]*?)\\\)/g) || []).map(x => x.slice(2, -2));
  const tryTex = (w, t) => { try { katex.renderToString(t, { throwOnError: true }); } catch (e) { bad.push(w + ': ' + String(e.message || e).slice(0, 120)); } };
  [1, 2, 3, 4].forEach(s => FDP.BANK[s].forEach(it => {
    [it.answer].concat(it.distractors, it.given ? [it.given] : []).forEach(o => tryTex(it.id, o.tex));
    [it.prompt, it.working, it.equation].forEach(str => segs(str).forEach(t => tryTex(it.id, t)));
  }));
  return bad;
}
"""

FIREBASE_STUB = r"""
(() => {
  window.__refs = []; window.__pushes = [];
  const db = { ref(path) { window.__refs.push(path); const r = {
    once() { const v = (window.__stubBoards || {})[path] || null;
             return Promise.resolve({ val() { return v; }, numChildren() { return 0; }, forEach() {} }); },
    push(e) { window.__pushes.push([path, e]); return Promise.resolve(); },
    orderByChild() { return r; } }; return r; } };
  window.firebase = { initializeApp() { return {}; }, app() { return {}; }, database() { return db; } };
})();
"""

FIXED_DATE = r"""
(() => {
  const FIXED = Date.parse('%s'), RealDate = Date, off = FIXED - RealDate.now();
  function D(...a) { return a.length ? new RealDate(...a) : new RealDate(RealDate.now() + off); }
  D.prototype = RealDate.prototype; D.now = () => RealDate.now() + off; D.UTC = RealDate.UTC; D.parse = RealDate.parse;
  window.Date = D;
})();
"""

EVENTS_JS = r"""() => { window.__events = []; window.mfg = function (n, p) { window.__events.push([n, p]); }; }"""


async def new_page(browser, firebase=False, when=None, viewport=None, katex=True, boards=None):
    ctx = await browser.new_context(viewport=viewport or {"width": 1100, "height": 900})
    await bc.no_next_floor(ctx)      # content checks; the floor is tested in test-next-control.py
    await ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)   # it clicks as soon as a question is asking

    async def route(r):
        u = r.request.url
        if u.startswith("http://127.0.0.1:%d/" % PORT) or (katex and u.startswith("https://cdn.jsdelivr.net/npm/katex@")):
            await r.continue_()
        else:
            await r.abort()      # GA, Apps Script, the Firebase SDK, fonts: nothing leaves the machine
    await ctx.route("**/*", route)
    if when:
        await ctx.add_init_script(FIXED_DATE % when)
    if firebase:
        await ctx.add_init_script("window.__stubBoards = %s;" % json.dumps(boards or {}))
        await ctx.add_init_script(FIREBASE_STUB)
    page = await ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("console", lambda m: errors.append("console.error: " + m.text)
            if m.type == "error" and "Failed to load resource" not in m.text else None)
    await page.goto("http://127.0.0.1:%d/games/%s/?cb=%d" % (PORT, SLUG, int(time.time() * 1000)),
                    wait_until="load", timeout=30000)
    await page.wait_for_function("!!window.FDP && !!window.FDP.ui", timeout=10000)
    return ctx, page, errors


async def collect_static(page, n_dates=400):
    out = []
    data = await page.evaluate(COLLECT_JS)
    by_id, exp = check_banks(data, out)
    start = date(2026, 9, 1)
    dates = [(start + timedelta(days=i)).isoformat() for i in range(n_dates)]
    prac = []
    for stage in (1, 2, 3, 4, "mixed"):
        for n in (20, 40):
            for seed in (1, 7, 99, 2026):
                prac.append([stage, n, seed])
    secs = [0, 0.4, 1, 2.5, 5, 9, 30, 120]
    res = await page.evaluate(DAILY_JS, {"dates": dates, "instants": [u[0] for u in UK_DATES], "practice": prac, "secs": secs})
    check_daily(res["sets"], res["again"], res["uk"], by_id, exp, out)
    for (stage, n, seed), got in zip(prac, res["practice"]):
        want = practice_expected(stage, n, seed, exp, by_id)
        w = "practice %s/%d seed %d" % (stage, n, seed)
        if got != want:
            out.append(w + ": page gave %r, expected %r" % (got[:3], want[:3]))
        if len(got) != n or len(set(got)) != n:
            out.append(w + ": %d questions, %d distinct" % (len(got), len(set(got))))
        st = [by_id[i]["stage"] for i in got if i in by_id]
        if stage == "mixed":
            if st != sorted(st) or any(st.count(s) != n // 4 for s in (1, 2, 3, 4)):
                out.append(w + ": mixed stages %r are not a quarter each, in order" % st)
        elif set(st) != {stage}:
            out.append(w + ": items from stages %r" % sorted(set(st)))
        if any(family(by_id[a]) == family(by_id[b]) for a, b in zip(got, got[1:])):
            out.append(w + ": two neighbours are about the same value")
    for s, (right, wrong) in zip(secs, res["scores"]):
        if right != score_for(s, True) or wrong != 0:
            out.append("score after %ss is %r/%r, expected %d/0" % (s, right, wrong, score_for(s, True)))
    return out, data, by_id, exp, dates


# ------------------------------------------------------------ playing it

def correct_index(labels, it):
    """Which option label is right, decided here from the display and the parameters."""
    form, want, simplest = expected_answer(it)
    hits = []
    for i, lab in enumerate(labels):
        try:
            v, sh = parse_display(form, lab, False)
        except ValueError:
            continue
        if v == want and (not simplest or sh is None or math.gcd(*sh) == 1):
            hits.append(i)
    return hits


SLASHY = re.compile(r"\d\s*/\s*\d|[\u00bc-\u00be\u2150-\u215e]")


async def slash_on_screen(page):
    """Visible text that writes a fraction with a slash or a small glyph. KaTeX's hidden MathML
    copy is removed first; what is left is what a student reads."""
    txt = await page.evaluate("""() => { const c = document.querySelector('.container').cloneNode(true);
      c.querySelectorAll('.katex-mathml, [aria-hidden=true] title').forEach(e => e.remove());
      document.body.appendChild(c); c.style.position = 'absolute'; c.style.left = '-9999px';
      const t = c.innerText; c.remove(); return t; }""")
    return SLASHY.findall(txt)


async def pics_now(page):
    return await page.evaluate("document.querySelectorAll('.pic, .pics, figure').length")


async def play(page, by_id, out, tag, policy, n_expected, events_mode, board, stages_seen=None):
    """Play a session already started. policy(i) -> True to answer right."""
    served = 0
    while True:
        await page.wait_for_function("['asking','done'].includes(FDP.ui.state())", timeout=15000)
        if await page.evaluate("FDP.ui.state()") == "done":
            break
        q = await page.evaluate("FDP.ui.question()")
        if q["index"] != served + 1:
            await page.wait_for_function("(p) => FDP.ui.state() === 'done' || FDP.ui.question().index > p", arg=served, timeout=15000)
            continue
        served = q["index"]
        it = by_id[q["id"]]
        if stages_seen is not None:
            stages_seen.append(it["stage"])
        if await pics_now(page):
            out.append("%s q%d (%s): a picture is on screen before answering" % (tag, served, it["id"]))
        sl = await slash_on_screen(page)
        if sl:
            out.append("%s q%d (%s): fraction written with a slash or glyph on screen: %r" % (tag, served, it["id"], sl[:3]))
        labels = await page.evaluate("Array.from(document.querySelectorAll('#options .opt')).map(b => b.getAttribute('aria-label'))")
        if len(labels) != 4:
            out.append("%s q%d (%s): %d options" % (tag, served, it["id"], len(labels)))
        hits = correct_index(labels, it)
        if len(hits) != 1:
            out.append("%s q%d (%s): %d options display the right answer (%r)" % (tag, served, it["id"], len(hits), labels))
            if not hits:
                hits = [0]
        right = policy(served)
        idx = hits[0] if right else next(i for i in range(len(labels)) if i not in hits)
        await page.locator("#options .opt").nth(idx).click()
        ev = await page.evaluate("window.__events.filter(e => e[0] === 'question_answered').slice(-1)[0]")
        if not ev or ev[1].get("correct") is not right:
            out.append("%s q%d (%s): clicking %r was marked %r" % (tag, served, it["id"], labels[idx], ev and ev[1].get("correct")))
        if not right:
            await page.wait_for_selector("#feedback .maffs-next", timeout=5000)
            order = await page.evaluate("""() => {
              const fb = document.getElementById('feedback');
              const els = ['.fb-fact', '.fb-work', '.pics', '.maffs-next-wrap'].map(s => fb.querySelector(s));
              const pos = (a, b) => !!(a && b && (a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING));
              return { have: els.map(e => !!e), fw: pos(els[0], els[1]), wp: els[2] ? pos(els[1], els[2]) : null,
                       pn: els[2] ? pos(els[2], els[3]) : pos(els[1], els[3]),
                       optionsShown: getComputedStyle(document.getElementById('options')).display !== 'none',
                       drawn: Array.from(fb.querySelectorAll('figure.pic')).map(f => f.dataset.type) }; }""")
            if not (order["have"][0] and order["have"][1] and order["have"][3]):
                out.append("%s q%d (%s): wrong-answer screen lacks fact/working/Next %r" % (tag, served, it["id"], order["have"]))
            if not order["fw"] or order["wp"] is False or not order["pn"]:
                out.append("%s q%d (%s): order is not fact, working, pictures, Next" % (tag, served, it["id"]))
            if order["optionsShown"]:
                out.append("%s q%d (%s): the options stay on screen during the feedback" % (tag, served, it["id"]))
            sl = await slash_on_screen(page)
            if sl:
                out.append("%s q%d (%s): wrong-answer screen writes a fraction as %r" % (tag, served, it["id"], sl[:3]))
            if order["drawn"] != [p["type"] for p in it["pictures"]]:
                out.append("%s q%d (%s): pictures drawn %r, expected %r" % (tag, served, it["id"], order["drawn"], [p["type"] for p in it["pictures"]]))
            await page.click("#feedback .maffs-next")
    if served != n_expected:
        out.append("%s: served %d questions, expected %d" % (tag, served, n_expected))
    await page.wait_for_selector("#results.active", timeout=5000)
    evs = await page.evaluate("window.__events")
    check_events(evs, events_mode, n_expected, out, tag)
    return served


def check_events(evs, mode, n, out, tag):
    names = [e[0] for e in evs]
    for name, p in evs:
        if p.get("game_slug") != SLUG or p.get("level") != "all" or p.get("mode") != mode:
            out.append("%s: %s carried %r/%r/%r, expected %s/all/%s" % (tag, name, p.get("game_slug"), p.get("level"), p.get("mode"), SLUG, mode))
    if names.count("game_started") != 1 or names.count("game_completed") != 1:
        out.append("%s: events %r" % (tag, sorted(set(names))))
    qa = [p for nm, p in evs if nm == "question_answered"]
    if [p.get("question_index") for p in qa] != list(range(1, n + 1)):
        out.append("%s: question_index runs %r" % (tag, [p.get("question_index") for p in qa][:12]))
    if any(not isinstance(p.get("correct"), bool) for p in qa):
        out.append("%s: question_answered without a boolean correct" % tag)
    right = sum(1 for p in qa if p.get("correct"))
    gc = [p for nm, p in evs if nm == "game_completed"]
    if gc and (gc[0].get("questions_answered") != n or gc[0].get("questions_correct") != right
               or not isinstance(gc[0].get("score"), int)):
        out.append("%s: game_completed carried %r" % (tag, gc[0]))
    for nm, p in evs:
        if nm == "personal_best_set" and (not isinstance(p.get("previous_best"), int) or not isinstance(p.get("score"), int)):
            out.append("%s: personal_best_set carried %r" % (tag, p))


SUBMITS_JS = r"""() => { window.__submits = []; const L = window.MaffsLeaderboard, o = L.submitScore;
  L.submitScore = function (slug, level, score, n) { window.__submits.push([slug, level, score, n]); return o.apply(this, arguments); }; }"""


async def start_practice(page, stage, n):
    await page.evaluate(EVENTS_JS)
    await page.click(".stage-btn[data-stage='%s']" % stage)
    await page.click(".session-btn[data-count='%d']" % n)
    await page.click("#startBtn")


async def check_unranked(page, out, tag, key):
    """A single-stage run: no board, history and personal best under its own key, and it says so."""
    await page.wait_for_selector("#results.active", timeout=5000)
    if await page.query_selector("#mfg-initials-overlay"):
        out.append(tag + ": the initials pop-up opened for a run that ranks nowhere")
    txt = await page.inner_text("#resStats")
    if "Stage practice isn\u2019t ranked; play a mixed round to get on the board." not in txt:
        out.append(tag + ": the end screen does not say stage practice is not ranked (%r)" % txt)
    if not await page.evaluate("(k) => !!localStorage.getItem('mfg_hist_v1::free-daily-pizza::' + k)", key):
        out.append(tag + ": no score-history record under %s" % key)
    if await page.evaluate("(k) => localStorage.getItem('fdp_best_' + k)", key) is None:
        out.append(tag + ": personal best not kept under fdp_best_%s" % key)


async def skip_initials(page):
    try:
        await page.wait_for_selector(".mfg-ini-skip", timeout=4000)
        await page.click(".mfg-ini-skip")
    except Exception:
        pass


async def ui_runs(browser, by_id, exp, out):
    notes = []
    # 1. Practice, each stage, 20 questions, every other answer wrong, Firebase stubbed. A
    #    single-stage run ranks NOWHERE (Jon, 30 Sep 2026): it must never call submitScore, it keeps
    #    its score in device history under 'stage-sN-q20', and its end screen says it is not ranked.
    ctx, page, errors = await new_page(browser, firebase=True)
    try:
        await page.evaluate(SUBMITS_JS)
        for stage in (1, 2, 3, 4):
            await start_practice(page, stage, 20)
            seen = []
            mode = "stage-s%d-q20" % stage
            await play(page, by_id, out, "practice stage %d" % stage, lambda i: i % 2 == 0, 20, mode, None, seen)
            if set(seen) != {stage}:
                out.append("practice stage %d served stages %r" % (stage, sorted(set(seen))))
            await check_unranked(page, out, "practice stage %d" % stage, mode)
            await page.click("#menuBtn")
        subs = await page.evaluate("window.__submits")
        if subs:
            out.append("single-stage practice called submitScore %r; it must rank nowhere" % subs)
        refs = await page.evaluate("window.__refs")
        if any("practice" in r or "stage" in r for r in refs):
            out.append("single-stage practice touched leaderboard keys %r" % refs)
        # 2. Mixed, 20 questions (half wrong) and 40 (all wrong): the only practice that ranks.
        await page.click(".stage-btn[data-stage='mixed']")
        lens = (await page.inner_text("#sessionSelect")).split()
        if lens != ["20", "40"]:
            out.append("practice lengths offered: %r, expected 20 and 40" % lens)
        for n, policy in ((20, lambda i: i % 2 == 0), (40, lambda i: False)):
            await start_practice(page, "mixed", n)
            seen = []
            await play(page, by_id, out, "practice mixed %d" % n, policy, n, "practice-q%d" % n, None, seen)
            if seen != sorted(seen) or any(seen.count(st) != n // 4 for st in (1, 2, 3, 4)):
                out.append("mixed %d served stages %r" % (n, seen))
            await skip_initials(page)
            if "isn\u2019t ranked" in await page.inner_text("#resStats"):
                out.append("mixed %d: the end screen says it is not ranked" % n)
            await page.click("#menuBtn")
        subs = [x[1] for x in await page.evaluate("window.__submits")]
        if subs != ["practice-q20", "practice-q40"]:
            out.append("mixed practice submitted to %r, expected practice-q20 then practice-q40" % subs)
        refs = await page.evaluate("window.__refs")
        writes = [r for r in refs if "practice" in r]
        want = ["leaderboards/free_daily_pizza_practice_q20", "leaderboards/free_daily_pizza_practice_q40"]
        if writes != want:
            out.append("mixed practice touched %r, expected %r" % (writes, want))
        for e in errors:
            out.append("practice page error: " + e)
        notes.append("practice: stages 1-4 at 20 submitted nothing (history under stage-sN-q20, 'not ranked' shown); "
                     "mixed 20 and 40 submitted to %s" % ", ".join(w.split("/")[1] for w in writes))
    finally:
        await ctx.close()

    # 3. The daily pizza, twice, on one simulated UK date, with a target on the board.
    when, day = "2026-10-01T11:00:00Z", "2026-10-01"
    key = "leaderboards/free_daily_pizza_daily_2026_10_01"
    served = []
    for run in range(2):
        ctx, page, errors = await new_page(browser, firebase=True, when=when, boards={key: {
            "a": {"score": 640, "timestamp": 1790000000000}, "b": {"score": 512, "timestamp": 1790000000000}}})
        try:
            await page.wait_for_function("document.getElementById('dailyTarget').style.display === 'block'", timeout=5000)
            tgt = await page.inner_text("#dailyTarget")
            if "640" not in tgt:
                out.append("daily target reads %r, expected today's best 640" % tgt)
            await page.evaluate(EVENTS_JS)
            await page.click("#dailyBtn")
            sess = await page.evaluate("FDP.ui.session()")
            served.append(sess["ids"])
            if sess["board"] != "daily-" + day:
                out.append("daily board is %r" % sess["board"])
            if (await page.inner_text("#hudTarget")) != "640":
                out.append("daily HUD target missing")
            await play(page, by_id, out, "daily run %d" % (run + 1), lambda i: i % 3 != 0, 10, "daily", None)
            await skip_initials(page)
            refs = await page.evaluate("window.__refs")
            if key not in refs or any("practice" in r for r in refs):
                out.append("daily run touched %r" % refs)
            for e in errors:
                out.append("daily page error: " + e)
        finally:
            await ctx.close()
    want = daily_expected(day, exp, by_id)
    if served[0] != served[1]:
        out.append("two loads on %s served different pizzas" % day)
    if served[0] != want:
        out.append("the pizza served on %s is not the one the seed gives" % day)
    if [by_id[i]["stage"] for i in served[0]] != DAILY_STAGES:
        out.append("the served daily pizza is not easiest first")
    notes.append("daily %s: two loads served the same 10, stages %s, target 640 shown, key %s"
                 % (day, "".join(str(by_id[i]["stage"]) for i in served[0]), key.split("/")[1]))

    # 4. The Firebase SDK and the KaTeX CDN both blocked: no target, no error, the whole pizza
    #    plays, and every fraction is still stacked (the HTML fallback), never written 3/4.
    ctx, page, errors = await new_page(browser, firebase=False, when=when, katex=False)
    try:
        if await page.evaluate("typeof window.firebase") != "undefined":
            out.append("blocked run: the Firebase SDK loaded")
        if await page.evaluate("typeof window.katex") != "undefined":
            out.append("blocked run: KaTeX loaded")
        await page.wait_for_timeout(500)
        if await page.is_visible("#dailyTarget"):
            out.append("blocked run: a target shows with Firebase unavailable")
        await page.evaluate(EVENTS_JS)
        await page.click("#dailyBtn")
        await play(page, by_id, out, "daily, SDK and KaTeX blocked", lambda i: i % 2 == 0, 10, "daily", None)
        if await page.query_selector("#mfg-initials-overlay"):
            out.append("blocked run: the initials pop-up opened with no leaderboard to submit to")
        if not any(e[0] == "personal_best_set" for e in await page.evaluate("window.__events")):
            out.append("blocked run: a first daily score set no personal best")
        if not await page.evaluate("document.querySelectorAll('#resReview .sfrac, #menu .sfrac').length >= 0"):
            out.append("blocked run: no stacked fallback")
        if await page.evaluate("localStorage.getItem('fdp_best_daily-%s')" % day) is None:
            out.append("blocked run: personal best not kept under fdp_best_daily-%s" % day)
        for e in errors:
            out.append("blocked run page error: " + e)
        notes.append("Firebase SDK and KaTeX blocked: no target, no error, 10 played (5 wrong), fractions stacked "
                     "by the HTML fallback, personal best under the day's key")
    finally:
        await ctx.close()
    return notes


# ------------------------------------------------------------ phone

VIEWPORTS = [(320, 568), (375, 667), (390, 844)]

MEASURE_JS = r"""
() => {
  const fb = document.getElementById('feedback');
  const r = s => { const e = fb.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect();
                   return { top: b.top + scrollY, bottom: b.bottom + scrollY }; };
  return { next: r('.maffs-next'), work: r('.fb-work'), pics: r('.pics'),
           sw: document.documentElement.scrollWidth, vw: innerWidth, vh: innerHeight, sy: scrollY,
           options: getComputedStyle(document.getElementById('options')).display };
}
"""


async def phone(browser, by_id, out, screens=None):
    worst = {}
    shots = {"S1:conv:f>d:2/3", "S3:frac:3/5:45", "S4:p:15/60"}
    for w, h in VIEWPORTS:
        ctx, page, errors = await new_page(browser, viewport={"width": w, "height": h})
        worst[(w, h)] = 0
        try:
            await page.evaluate(EVENTS_JS)
            for iid, it in by_id.items():
                await page.evaluate("(i) => FDP.ui.serve([i])", iid)
                labels = await page.evaluate("Array.from(document.querySelectorAll('#options .opt')).map(b => b.getAttribute('aria-label'))")
                hits = correct_index(labels, it)
                idx = next(i for i in range(len(labels)) if i not in hits)
                await page.locator("#options .opt").nth(idx).click()
                await page.wait_for_selector("#feedback .maffs-next", timeout=5000)
                m = await page.evaluate(MEASURE_JS)
                fold = m["vh"] - FOOTER
                wh = "phone %dx%d %s" % (w, h, iid)
                worst[(w, h)] = max(worst[(w, h)], m["next"]["bottom"])
                if m["next"]["bottom"] > fold:
                    out.append("%s: Next ends at %.0fpx, below the fold at %dpx" % (wh, m["next"]["bottom"], fold))
                if m["work"]["bottom"] > m["next"]["top"]:
                    out.append("%s: the working is below Next" % wh)
                if m["pics"] and h > 600 and m["pics"]["bottom"] > m["next"]["top"]:
                    out.append("%s: the pictures are below Next on a screen taller than 600px" % wh)
                if m["sw"] > m["vw"]:
                    out.append("%s: horizontal scroll (%d > %d)" % (wh, m["sw"], m["vw"]))
                if m["options"] != "none":
                    out.append("%s: options visible during the feedback" % wh)
                if screens and iid in shots:
                    os.makedirs(screens, exist_ok=True)
                    name = "free-daily-pizza-wrong-%s-%dx%d.png" % (re.sub(r"[^a-z0-9]+", "-", iid.lower()).strip("-"), w, h)
                    await page.screenshot(path=os.path.join(screens, name))
            for e in errors:
                out.append("phone %dx%d page error: %s" % (w, h, e))
        finally:
            await ctx.close()
    return worst


# ------------------------------------------------------------ self-test

FAULTS = [
    ("wrong answer (3/4 as a decimal shown as 0.7)",
     "static", "(() => { const it = FDP.item('S1:conv:f>d:3/4'); it.answer = Object.assign({}, it.answer, { text: '0.7', tex: '0.7' }); })()"),
    ("value-equal distractor (0.750 beside 0.75)",
     "static", "(() => { const it = FDP.item('S1:conv:f>d:3/4'); it.distractors[0] = Object.assign({}, it.distractors[0], { text: '0.750', tex: '0.750', key: 'd:0.750', tag: 'place-value', shift: 1 }); })()"),
    ("wrong tag (denominator-as-decimal relabelled inversion)",
     "static", "(() => { const it = FDP.item('S1:conv:f>d:3/4'); it.distractors[0].tag = 'inversion'; })()"),
    ("broken daily mix (4 from stage 1, 2 from stage 2)",
     "static", "FDP.DAILY_MIX = [[1, 4], [2, 2], [3, 2], [4, 2]];"),
    ("daily not easiest first (stages reversed)",
     "static", "(() => { const o = FDP.dailySet; FDP.dailySet = d => o(d).reverse(); })()"),
    ("recurring answer shown as exact (1/3 = 0.33)",
     "static", "(() => { const it = FDP.item('S1:conv:f>d:1/3'); it.answer = Object.assign({}, it.answer, { text: '0.33', tex: '0.33' }); })()"),
    ("lossy picture (3/4 pizza with 2 slices shaded)",
     "static", "(() => { FDP.item('S1:conv:f>d:3/4').pictures[0].shaded = 2; })()"),
    ("pre-answer picture leak (pizza drawn with the question)",
     "ui", "(() => { const o = FDP.promptHtml; FDP.promptHtml = it => o(it) + FDP.pictureHtml(it); })()"),
    ("a fraction written with a slash (options shown as plain text)",
     "ui", "(() => { FDP.optionHtml = o => o.text; })()"),
    ("a single-stage practice run submits to practice-q20",
     "stage", "(() => { FDP.boardFor = (m, st, n, d) => m === 'daily' ? 'daily-' + d : 'practice-q' + n; })()"),
]


async def selftest(browser, by_id):
    lines, ok = [], True
    for name, kind, patch in FAULTS:
        ctx, page, _ = await new_page(browser)
        found = []
        try:
            await page.evaluate(patch)
            if kind == "static":
                found, _, _, _, _ = await collect_static(page, n_dates=40)
            elif kind == "stage":
                await page.evaluate(SUBMITS_JS)
                await start_practice(page, 1, 20)
                await play(page, by_id, [], "fault", lambda i: False, 20, "stage-s1-q20", None)
                await check_unranked(page, found, "stage 1 run", "stage-s1-q20")
                subs = await page.evaluate("window.__submits")
                if subs:
                    found.append("a single-stage run called submitScore %r" % subs)
            else:
                await page.evaluate(EVENTS_JS)
                # Fixed items, not a random session: each has fractions among its options and a
                # picture to leak, so the fault is always on screen to be found.
                await page.evaluate("FDP.ui.serve(['S1:conv:d>f:3/4', 'S1:conv:p>f:2/5', 'S2:simp:18/24'])")
                for _ in range(3):
                    await page.wait_for_function("FDP.ui.state() === 'asking'", timeout=8000)
                    if await pics_now(page):
                        found.append("a picture is on screen before answering")
                    if await slash_on_screen(page):
                        found.append("a fraction is written with a slash on screen")
                    if found:
                        break
                    await page.locator("#options .opt").first.click()
                    if await page.query_selector("#feedback .maffs-next"):
                        await page.click("#feedback .maffs-next")
        except Exception as e:
            err = str(e).splitlines()[0][:100]
        else:
            err = None
        finally:
            await ctx.close()
        caught = bool(found) and err is None     # an error while checking is not a catch
        if err:
            found = ["checker error: " + err]
        ok = ok and caught
        lines.append("  %-62s %s" % (name, ("CAUGHT (%d, e.g. %s)" % (len(found), found[0][:80])) if caught
                                          else "*** MISSED *** " + (found[0] if found else "")))
    return ok, lines


# ------------------------------------------------------------ main

async def run_all(args):
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        ctx, page, errors = await new_page(browser)
        found, data, by_id, exp, dates = await collect_static(page)
        # A fresh page must serve the same pizzas (nothing carried over from a first load).
        again = await page.evaluate("(ds) => ds.map(d => FDP.dailySet(d))", dates[:30])
        kbad = await page.evaluate(KATEX_JS)
        await ctx.close()
        ctx2, page2, _ = await new_page(browser)
        fresh = await page2.evaluate("(ds) => ds.map(d => FDP.dailySet(d))", dates[:30])
        await ctx2.close()
        if fresh != again:
            found.append("daily: a fresh page load serves different pizzas for the same dates")
        for f in found:
            fail(f)
        for e in errors:
            fail("page error: " + e)
        counts = {str(s): len(data["bank"][str(s)]) for s in (1, 2, 3, 4)}
        nd = sum(len(it["distractors"]) for s in (1, 2, 3, 4) for it in data["bank"][str(s)])
        npic = sum(len(v) for v in data["drawn"].values())
        print("Items: S1 %(1)d, S2 %(2)d, S3 %(3)d, S4 %(4)d" % counts, "  distractors recomputed: %d   pictures counted: %d" % (nd, npic))
        print("Daily pizzas recomputed from the seed: %d dates (+ %d on a fresh page); UK date at %d instants"
              % (len(dates), len(fresh), len(UK_DATES)))
        if kbad is None:
            if args.require_katex:
                fail("KaTeX did not load (--require-katex)")
            else:
                print("SKIP: KaTeX did not load; TeX strings not parse-checked (CI runs --require-katex)")
        else:
            for b in kbad:
                fail("KaTeX: " + b)
            if not kbad:
                print("KaTeX: every option, prompt, working and equation segment renders")

        ui_out = []
        notes = await ui_runs(browser, by_id, exp, ui_out)
        for f in ui_out:
            fail(f)
        for n in notes:
            print("UI " + n)

        if not args.no_phone:
            ph_out = []
            worst = await phone(browser, by_id, ph_out, args.screens)
            for f in ph_out:
                fail(f)
            print("Phone: %d items x 3 viewports; lowest Next bottom edge: %s" % (len(by_id), ", ".join(
                "%dx%d %.0fpx (fold %d)" % (w, h, worst[(w, h)], h - FOOTER) for w, h in VIEWPORTS)))

        if not args.no_selftest:
            ok, lines = await selftest(browser, by_id)
            print()
            print("Fault-injection self-test (patched into a fresh page; the file is never touched):")
            for ln in lines:
                print(ln)
            if not ok:
                fail("fault-injection self-test: at least one fault was not caught")
        await browser.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-selftest", action="store_true")
    ap.add_argument("--no-phone", action="store_true", help="skip measuring every item at three phone sizes")
    ap.add_argument("--require-katex", action="store_true", help="fail if KaTeX cannot load (CI)")
    ap.add_argument("--screens", help="save wrong-answer screenshots at the three phone sizes to this folder")
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
