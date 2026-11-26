#!/usr/bin/env python3
"""d by dx? Why?: question bank generator, Phase 1, differentiation (Project Claude, 26 Nov 2026). Deterministic: no randomness.

Five stages of 12 items, Level 3 (EAL AME3-004, assessment 004C). Built to the item TYPES of Jon's paper, never its wording
or numbers. Every expression is held as a list of terms; TeX is written from the terms here, and the page shows only the
TeX. Every distractor comes from a named error (canon SR-4) and carries that error's key, so the page can show its line.

Term kinds (coefficients and powers are exact fractions, written "p" or "p/q"):
  ["pow", c, n]      c * v^n           ["const", c]        c
  ["sin", c, a]      c * sin(a v)      ["cos", c, a]       c * cos(a v)
  ["exp", c, a]      c * e^(a v)       ["ln", c, a]        c * ln(a v)
  ["over", c, d]     c / (d v)         ["recipln", c, a]   c / ln(a v)
  ["xexp", c, a]     c * v * e^(a v - 1)   ["overpow", c, d, m]   c / (d v^m)
Options are TeX strings; dataset.val is the answer's or decoy's "tex" exactly.
"""
import hashlib
import json
import math
import sys
from fractions import Fraction as F

STAGES = {1: "Power terms", 2: "Rewrite first", 3: "Sin and cos", 4: "e and ln", 5: "Sums of terms"}
FORMS = ["wrt", "bare", "fn"]


def fs(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def T(kind, *args):
    return [kind] + [fs(a) for a in args]


# ------------------------------------------------------------------------------------------------ TeX
def frac_tex(x):
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    return ("-" if x < 0 else "") + r"\frac{%d}{%d}" % (abs(x.numerator), x.denominator)


def coef(c, lead, attach=True):
    c = F(c)
    sign = "-" if c < 0 else ("" if lead else "+")
    a = abs(c)
    if a == 1 and attach:
        return sign
    return sign + frac_tex(a)


def ang(a, v):
    a = F(a)
    return v if a == 1 else f"{frac_tex(a)}{v}"


def term_tex(t, v, lead):
    k, args = t[0], [F(x) for x in t[1:]]
    c = args[0]
    if k == "const":
        return coef(c, lead, attach=False)
    if k == "pow":
        n = args[1]
        if n == 0:
            return coef(c, lead, attach=False)
        return coef(c, lead) + (v if n == 1 else f"{v}^{{{frac_tex(n)}}}")
    if k in ("sin", "cos"):
        return coef(c, lead) + rf"\{k} {ang(args[1], v)}"
    if k == "exp":
        return coef(c, lead) + f"e^{{{ang(args[1], v)}}}"
    if k == "ln":
        return coef(c, lead) + rf"\ln {ang(args[1], v)}"
    if k == "xexp":
        return coef(c, lead) + f"{v}e^{{{ang(args[1], v)}-1}}"
    sign = "-" if c < 0 else ("" if lead else "+")
    if k == "over":
        d = args[1]
        return sign + r"\frac{%s}{%s}" % (frac_tex(abs(c)), v if d == 1 else f"{frac_tex(d)}{v}")
    if k == "overpow":
        d, m = args[1], args[2]
        return sign + r"\frac{%s}{%s%s}" % (frac_tex(abs(c)), frac_tex(d), v if m == 1 else f"{v}^{{{frac_tex(m)}}}")
    if k == "recipln":
        return sign + r"\frac{%s}{\ln %s}" % (frac_tex(abs(c)), ang(args[1], v))
    raise ValueError(k)


def tex(terms, v):
    return "".join(term_tex(t, v, i == 0) for i, t in enumerate(terms))


# ------------------------------------------------------------------------------------------------ values (for the checks)
def value(terms, x):
    s = 0.0
    for t in terms:
        k, a = t[0], [float(F(y)) for y in t[1:]]
        c = a[0]
        s += {"const": lambda: c, "pow": lambda: c * x ** a[1], "sin": lambda: c * math.sin(a[1] * x),
              "cos": lambda: c * math.cos(a[1] * x), "exp": lambda: c * math.exp(a[1] * x),
              "ln": lambda: c * math.log(a[1] * x), "over": lambda: c / (a[1] * x),
              "recipln": lambda: c / math.log(a[1] * x), "overpow": lambda: c / (a[1] * x ** a[2]), "xexp": lambda: c * x * math.exp(a[1] * x - 1)}[k]()
    return s


POINTS = (0.37, 0.61, 1.7, 2.3)   # positive, away from ln's zero at a v = 1 for every a used


# ------------------------------------------------------------------------------------------------ prompts and working
def prompt(form, v, q):
    if form == "wrt":
        return rf"Differentiate with respect to \({v}\): \(y = {q}\)"
    if form == "bare":
        return rf"Differentiate: \({q}\)"
    return rf"If \(f({v}) = {q}\), find \(f'({v})\)"


def answer_line(form, v, q, ans):
    if form == "wrt":
        return rf"\(\dfrac{{dy}}{{d{v}}} = {ans}\)"
    if form == "fn":
        return rf"\(f'({v}) = {ans}\)"
    return rf"\(\dfrac{{d}}{{d{v}}}\left({q}\right) = {ans}\)"


def pow_steps(c, n, v):
    """The two power-rule lines: bring the power down, take one off."""
    return [rf"Bring the power down: \({frac_tex(c)} \times {'(' + frac_tex(n) + ')' if n < 0 else frac_tex(n)} = {frac_tex(c * n)}\)",
            rf"Take one off the power: \({frac_tex(n)} - 1 = {frac_tex(n - 1)}\)"]


# ------------------------------------------------------------------------------------------------ the bank
items = []


def add(stage, v, form, q_terms, q_tex, answer, decoys, working, rows):
    n = sum(1 for i in items if i["stage"] == stage) + 1
    qt = q_tex if q_tex is not None else tex(q_terms, v)
    ans_tex = tex(answer, v)
    items.append({"id": f"s{stage}-{n:02d}", "stage": stage, "var": v, "form": form, "q": q_terms, "qtex": qt,
                  "prompt": prompt(form, v, qt),
                  "answer": {"tex": ans_tex, "terms": answer},
                  "decoys": [{"err": e, "tex": tex(t, v), "terms": t} for e, t in decoys],
                  "rows": rows,
                  "working": working + [answer_line(form, v, qt, ans_tex)]})


def stage1():
    for i, (v, a, n) in enumerate([("x", 5, 4), ("t", 3, 5), ("r", 7, 2), ("x", 6, 3), ("t", 2, 6), ("r", 4, 5),
                                   ("z", 9, 2), ("x", -3, 4), ("t", 8, 3)]):
        add(1, v, FORMS[i % 3], [T("pow", a, n)], None, [T("pow", a * n, n - 1)],
            [("power_kept", [T("pow", a * n, n)]), ("coeff_lost", [T("pow", n, n - 1)]),
             ("new_power_used", [T("pow", a * (n - 1), n - 1)])],
            pow_steps(F(a), F(n), v), ["axn"])
    for i, (v, a) in enumerate([("x", 7), ("t", 12), ("r", -5)]):
        add(1, v, FORMS[(i + 1) % 3], [T("pow", a, 1)], None, [T("const", a)],
            [("kept_variable", [T("pow", a, 1)]), ("coeff_lost", [T("const", 1)]), ("treated_as_constant", [T("const", 0)])],
            [rf"\({v}\) on its own differentiates to \(1\), so the \({v}\) goes and the number stays: \({frac_tex(a)} \times 1 = {frac_tex(a)}\)"],
            ["x"])


def stage2():
    for i, (v, a, n) in enumerate([("x", 3, 2), ("t", 4, 3), ("r", 6, 1), ("x", 5, 4), ("z", 8, 2), ("t", -2, 3)]):
        den = v if n == 1 else f"{v}^{n}"
        qt = (r"\frac{%d}{%s}" % (a, den)) if a > 0 else (r"-\frac{%d}{%s}" % (-a, den))
        bottom = [T("overpow", a, n, n - 1)] if n > 1 else [T("const", a)]
        add(2, v, FORMS[i % 3], [T("pow", a, -n)], qt, [T("pow", -a * n, -n - 1)],
            [("sign_lost", [T("pow", a * n, -n - 1)]), ("power_wrong_way", [T("pow", -a * n, -n + 1)]),
             ("bottom_differentiated", bottom)],
            [rf"Rewrite first: \({qt} = {tex([T('pow', a, -n)], v)}\)"] + pow_steps(F(a), F(-n), v), ["axn"])
    for i, (v, c, m, k) in enumerate([("x", 1, 5, 2), ("r", 1, 2, 3), ("t", 4, 3, 2), ("x", 1, 7, 2), ("r", 6, 4, 3),
                                      ("t", 2, 5, 3)]):
        root = (r"\sqrt{%s^{%d}}" % (v, m)) if k == 2 else (r"\sqrt[%d]{%s^{%d}}" % (k, v, m))
        qt = ("" if c == 1 else str(c)) + root
        p = F(m, k)
        add(2, v, FORMS[(i + 1) % 3], [T("pow", c, p)], qt, [T("pow", c * p, p - 1)],
            [("root_upside_down", [T("pow", F(c) / p, 1 / p - 1)]), ("power_kept", [T("pow", c * p, p)]),
             ("power_wrong_way", [T("pow", c * p, p + 1)])],
            [rf"Rewrite first: \({qt} = {tex([T('pow', c, p)], v)}\) (the root's number goes on the bottom of the power)"]
            + pow_steps(F(c), p, v), ["axn"])


def stage3():
    for i, (f, v, c, a) in enumerate([("sin", "x", 1, 4), ("cos", "t", 1, 5), ("sin", "t", 3, 2), ("cos", "x", 2, 6),
                                      ("sin", "r", 5, 3), ("cos", "t", 4, 2), ("sin", "x", 1, 7), ("cos", "z", 1, 8),
                                      ("sin", "t", 2, 10), ("cos", "r", 3, 4), ("sin", "x", 6, 5), ("cos", "t", 5, 3)]):
        g, s = ("cos", 1) if f == "sin" else ("sin", -1)
        rule = (rf"\(\sin a{v} \to a\cos a{v}\): the \({a}\) comes out front and stays in the angle"
                if f == "sin" else
                rf"\(\cos a{v} \to -a\sin a{v}\): the \({a}\) comes out front, stays in the angle, and cos gives a minus")
        work = [rule] + ([rf"\({c} \times {a} = {c * a}\)"] if c != 1 else [])
        add(3, v, FORMS[i % 3], [T(f, c, a)], None, [T(g, s * c * a, a)],
            [("a_forgotten", [T(g, s * c, a)]), ("sign_slip", [T(g, -s * c * a, a)]),
             ("a_dropped_from_angle", [T(g, s * c * a, 1)])], work, [f])


def stage4():
    for i, (v, c, a) in enumerate([("x", 1, 3), ("t", 2, 4), ("z", 5, 2), ("x", 3, 6), ("t", 1, 7), ("r", 4, 3)]):
        work = [rf"\(e^{{a{v}}} \to ae^{{a{v}}}\): the \({a}\) comes down and the power stays the same"] + \
               ([rf"\({c} \times {a} = {c * a}\)"] if c != 1 else [])
        add(4, v, FORMS[i % 3], [T("exp", c, a)], None, [T("exp", c * a, a)],
            [("a_forgotten", [T("exp", c, a)]), ("integrated_instead", [T("exp", F(c, a), a)]),
             ("power_rule_used", [T("xexp", c * a, a)])], work, ["exp"])
    for i, (v, c, a) in enumerate([("x", 1, 4), ("t", 3, 2), ("x", 2, 5), ("r", 6, 3), ("t", 1, 9), ("z", 4, 7)]):
        work = [rf"\(\ln a{v} \to \frac{{1}}{{{v}}}\): the \({a}\) cancels out, \(\frac{{{a}}}{{{a}{v}}} = \frac{{1}}{{{v}}}\)"] + \
               ([rf"\({c} \times \frac{{1}}{{{v}}} = \frac{{{c}}}{{{v}}}\)"] if c != 1 else [])
        add(4, v, FORMS[(i + 1) % 3], [T("ln", c, a)], None, [T("over", c, 1)],
            [("a_kept", [T("over", c * a, 1)]), ("a_divided", [T("over", c, a)]), ("ln_flipped", [T("recipln", c, a)])],
            work, ["ln"])


def stage5():
    for i, (v, p, q, n, k) in enumerate([("t", 5, 2, 3, None), ("t", 4, 3, 2, None), ("x", 2, 5, 4, None),
                                         ("t", 7, 2, 5, None), ("r", 3, 4, 3, None), ("t", 6, 2, 4, None),
                                         ("t", 2, 3, 3, 9), ("x", 8, 2, 2, 4), ("t", 5, 6, 2, -3), ("t", 9, 1, 4, 7),
                                         ("z", 4, 5, 3, None), ("t", 3, 7, 2, -8)]):
        qt = [T("pow", p, 1), T("pow", q, n)] + ([T("const", k)] if k is not None else [])
        ans = [T("const", p), T("pow", q * n, n - 1)]
        decoys = [("kept_variable", [T("pow", p, 1), T("pow", q * n, n - 1)]), ("power_kept", [T("const", p), T("pow", q * n, n)])]
        decoys.append(("constant_kept", ans + [T("const", k)]) if k is not None else ("coeff_lost", [T("const", p), T("pow", n, n - 1)]))
        work = [r"Differentiate each term on its own:",
                rf"\({tex([T('pow', p, 1)], v)} \to {p}\)",
                rf"\({tex([T('pow', q, n)], v)} \to {tex([T('pow', q * n, n - 1)], v)}\)"]
        if k is not None:
            work.append(rf"\({k}\) on its own is a constant: it doesn't change, so it differentiates to \(0\)")
        add(5, v, "fn" if i % 4 != 3 else "wrt", qt, None, ans, decoys, work, ["x", "axn"])


# Which stages each named error may appear in: a key's feedback line is written for these stages only.
ERR_STAGES = {
    "power_kept": {1, 2, 5}, "coeff_lost": {1, 5}, "new_power_used": {1}, "kept_variable": {1, 5}, "treated_as_constant": {1},
    "sign_lost": {2}, "power_wrong_way": {2}, "bottom_differentiated": {2}, "root_upside_down": {2},
    "a_forgotten": {3, 4}, "sign_slip": {3}, "a_dropped_from_angle": {3},
    "integrated_instead": {4}, "power_rule_used": {4}, "a_kept": {4}, "a_divided": {4}, "ln_flipped": {4},
    "constant_kept": {5},
}
ROWS = ["x", "axn", "sin", "cos", "exp", "ln"]


def bank():
    items.clear()
    stage1(); stage2(); stage3(); stage4(); stage5()
    return list(items)


# ------------------------------------------------------------------------------------------------ checks
def check(bank_items):
    from collections import Counter
    assert Counter(i["stage"] for i in bank_items) == {1: 12, 2: 12, 3: 12, 4: 12, 5: 12}
    assert len({i["id"] for i in bank_items}) == 60 and len({i["prompt"] for i in bank_items}) == 60
    for it in bank_items:
        opts = [it["answer"]] + it["decoys"]
        assert len(it["decoys"]) == 3 and len({o["tex"] for o in opts}) == 4, it["id"]
        for x in POINTS:
            h = 1e-6
            d = (value(it["q"], x + h) - value(it["q"], x - h)) / (2 * h)
            assert abs(d - value(it["answer"]["terms"], x)) < 1e-4 * max(1, abs(d)), (it["id"], x)
        for i in range(4):
            for j in range(i + 1, 4):
                gap = max(abs(value(opts[i]["terms"], x) - value(opts[j]["terms"], x)) for x in POINTS)
                assert gap > 1e-3, (it["id"], opts[i]["tex"], opts[j]["tex"])
        for d in it["decoys"]:
            assert it["stage"] in ERR_STAGES[d["err"]], (it["id"], d["err"])
        assert it["rows"] and set(it["rows"]) <= set(ROWS)
    return True


if __name__ == "__main__":
    b = bank()
    check(b)
    blob = "".join(json.dumps(i, separators=(",", ":"), ensure_ascii=False) + "\n" for i in b)
    print("total", len(b))
    print("sha256", hashlib.sha256(blob.encode("utf-8")).hexdigest())
    if "--out" in sys.argv:
        open(sys.argv[sys.argv.index("--out") + 1], "w", encoding="utf-8", newline="\n").write(blob)
    if "--show" in sys.argv:
        for i in b:
            print(i["id"], "|", i["prompt"], "|", i["answer"]["tex"], "|", [(d["err"], d["tex"]) for d in i["decoys"]])
            for w in i["working"]:
                print("     ", w)
