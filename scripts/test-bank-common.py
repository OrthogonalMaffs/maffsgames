#!/usr/bin/env python3
"""B11's value comparison (bank_common.parse_value / equal / value_equal_pairs) on the shapes
the tranche 5 and 6 audits found it blind to (contract F0, 7 Oct 2026).

    python scripts/test-bank-common.py

Each EQUAL fixture is an option pair taken from the audit item that showed it, with the item's
own game and text, and must come back value-equal. Each UNEQUAL fixture is a look-alike that
must not: a range stated, a vector the item does not ask for up to scale, a Boolean rule in a
game that is not Boolean, a prose option that must never be read as a product. Until F0 every
EQUAL fixture here failed: parse_value returned None for one side, so B11 skipped the pair.

REGEX_GUARDS (7 Oct, queue item 0b): a render site guarded by a regex literal's .test() must be
decided per value; until the fix the evaluator raised on it (the cloud lane's note in #115).

No browser, no bank data: stdlib + SymPy. CI runs it in the Tier 4 layer A job.
"""
import inspect
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_common as bc  # noqa: E402

# (game, item text, a, b, where the audit found it)
EQUAL = [
    # Juxtaposed products (tranche 5, NEW-A).
    ("differentiation-duel", r"\dfrac{e^x}{x^2}",
     r"\dfrac{x^2 e^x - 2xe^x}{x^4}", r"\dfrac{e^x(x - 2)}{x^3}",
     "differentiation-duel-t5-001, games/differentiation-duel/index.html:820"),
    ("differentiation-duel", r"e^y = x^2 + 1",
     r"\dfrac{2x}{e^y}", r"2xe^{-y}",
     "differentiation-duel-t5-002, :848"),
    # \binom.
    ("binomial-blaster", r"\binom{5}{2} + \binom{5}{3}",
     "20", r"\binom{6}{3}",
     "binomial-blaster-t5-002, :134"),
    # A trig function of a constant, in degrees.
    ("force-resolver", "Horizontal component",
     r"12 \text{ N}", r"12\cos 0° \text{ N}",
     "force-resolver-t5-006, :118"),
    ("force-resolver", r"mg\cos\theta",
     r"25\sqrt{3} \approx 43.3 \text{ N}", r"50\cos 30° \text{ N}",
     "force-resolver-t5-005, :138"),
    # SI prefixes on units.
    ("moments-master", r"T = 50 \text{ Nm}, \; \omega = 100 \text{ rad/s}",
     r"5000 \text{ W}", r"5 \text{ kW}",
     "moments-master-t5-004, :180"),
    # Vectors equal up to a non-zero scalar: the game asks for an eigenvector (its prompt, :147).
    ("eigenvector-engine", "",
     r"\begin{pmatrix} 1 \\ -2 \end{pmatrix}", r"\begin{pmatrix} -1 \\ 2 \end{pmatrix}",
     "eigenvector-engine-t6-001, :117 (sign twins)"),
    ("eigenvector-engine", "",
     r"\begin{pmatrix} -1 \\ 1 \end{pmatrix}", r"\begin{pmatrix} 1 \\ -1 \end{pmatrix}",
     "eigenvector-engine-t6-001, :128 (sign twins)"),
    # Angles equal mod 360 degrees, no range stated.
    ("complex-converter", "This capacitive impedance has negative imaginary part. Find polar form.",
     r"5\angle -53.13°", r"5\angle 306.87°",
     "complex-converter-t6-001, :331 (id 21)"),
    ("complex-converter", "Convert this capacitive reactance to exponential form.",
     r"8e^{-j\pi/2}", r"-8e^{j\pi/2}",
     "complex-converter-t6-002, :350 (id 40)"),
    # Boolean expressions with the same truth table.
    ("boolean-blitz", "",
     "B(A + C)", "AB + BC",
     "boolean-blitz-t6-002, :584"),
    ("boolean-blitz", "",
     "A(B + C)", "AB + AC",
     "boolean-blitz-t6-003, :744"),
]

UNEQUAL = [
    # A range is stated: compared exactly, so 233.13 and -126.87 differ (complex-converter id 20).
    ("complex-converter", "Convert to polar form. Give angle as positive.",
     r"5\angle 233.13°", r"5\angle -126.87°", "range stated"),
    # Different angles, and a decimal angle is never 'nearly' equal.
    ("complex-converter", "Find polar form.", r"5\angle 53.13°", r"5\angle -53.13°", "different angles"),
    # Vectors outside an eigenvector or direction item are compared exactly.
    ("vector-game", "Find the position vector of B.",
     r"\begin{pmatrix} 1 \\ 2 \end{pmatrix}", r"\begin{pmatrix} 2 \\ 4 \end{pmatrix}", "no direction asked"),
    # Even in the eigenvector game, a vector that is not a multiple stays unequal.
    ("eigenvector-engine", "", r"\begin{pmatrix} 1 \\ 2 \end{pmatrix}", r"\begin{pmatrix} 2 \\ 1 \end{pmatrix}",
     "not parallel"),
    # Absorption holds in Boolean algebra only: outside a Boolean game A + AB is not A.
    ("algebra-game", "Simplify", "A + AB", "A", "not a Boolean game"),
    ("boolean-blitz", "", "A + BC", "(A + B)(A + C)", None),   # equal: distributes in Boolean algebra
    ("boolean-blitz", "", "AB", "A + B", "different truth tables"),
    # Prefixes are exact: 5 kW is 5000 W, not 500 W; and a prefix on a different unit is a different unit.
    ("moments-master", "", r"500 \text{ W}", r"5 \text{ kW}", "500 W"),
    ("moments-master", "", r"5 \text{ kW}", r"5 \text{ kN}", "different units"),
    # Trig of a constant, exactly: cos 30° is not 0.866.
    ("force-resolver", "", r"10\cos 30° \text{ N}", r"8.66 \text{ N}", "rounded"),
    ("force-resolver", "", r"12\cos 0° \text{ N}", r"12\sin 0° \text{ N}", "cos vs sin"),
    # Prose is never a product of letters.
    ("any-game", "", "Yes", "sYe", "prose"),
    ("any-game", "", "AB", "BA", "line names, no operator"),
    # Found by the first full run of the new parser (7 Oct 2026), both misreads:
    ("curling-friction", "", "22.5 m vs 22.5 m", "45 m vs 11.25 m", "'vs' is a word, not v times s"),
    ("proof-builder", "", "1! = 1", "2! - 1 = 1", "statements, not values"),
]
# The one UNEQUAL row with why=None is in fact an EQUAL Boolean identity; move it.
EQUAL += [(g, t, a, b, "Boolean distributive law over AND (distinct from ring algebra)")
          for g, t, a, b, why in UNEQUAL if why is None]
UNEQUAL = [r for r in UNEQUAL if r[4] is not None]

# Render-site guards that are a regex literal's .test() (the cloud lane's note, #102/#105/#115:
# `AttributeError: 'tuple' object has no attribute 'search'`). Each guard must be decided per
# value: (why, script, the sources that must reach KaTeX).
REGEX_GUARDS = [
    ("an if guard: /[\\^_{}]/.test(q.a) (Proof Builder's shape)",
     "function show(q, el){\n"
     "  if (/[\\\\^_{}]/.test(q.a)) katex.render(q.a, el);\n"
     "  else el.textContent = q.a;\n}\n",
     {"x^2"}),
    ("a ternary inside a template literal (Component Crusher's shape)",
     "function show(q, el){\n"
     "  el.innerHTML = `<b>${/\\^/.test(q.a) ? katex.renderToString(q.a) : q.a}</b>`;\n}\n",
     {"x^2"}),
]
REGEX_BANK = {"generator": False, "levels": {"default": {"groups": [
    {"variable": "QUESTIONS", "path": [], "in_pool": True,
     "questions": [{"a": "x^2"}, {"a": "seven"}]}]}}}


def regex_guard_reaches(script):
    _w, sites = bc.katex_render_sites("<script>\n" + script + "</script>")
    reached, unres = set(), []
    for st in sites:
        r = bc.resolve_render_site(st, REGEX_BANK)
        unres += [r["unresolved"]] if r["unresolved"] else []
        reached |= {it["source"] for it in r["items"].values() if "source" in it}
    return reached, unres


def pairs(game, text, a, b):
    """value_equal_pairs on [a, b] with the item's context, if this bank_common takes one."""
    fn = bc.value_equal_pairs
    if "ctx" in inspect.signature(fn).parameters:
        return fn([a, b], ctx=bc.item_context(game, {"q": text} if text else {}))
    return fn([a, b])


def main():
    fails = 0
    for game, text, a, b, where in EQUAL:
        try:
            got = bool(pairs(game, text, a, b))
        except Exception as exc:          # a crash is a failure, never a pass
            got, where = False, "%s (raised %s)" % (where, exc)
        print("%-4s equal    %-34r %-34r %s" % ("OK" if got else "FAIL", a, b, where))
        fails += not got
    for game, text, a, b, why in UNEQUAL:
        try:
            got = not pairs(game, text, a, b)
        except Exception as exc:
            got, why = False, "%s (raised %s)" % (why, exc)
        print("%-4s unequal  %-34r %-34r %s" % ("OK" if got else "FAIL", a, b, why))
        fails += not got
    for why, script, want in REGEX_GUARDS:
        try:
            reached, unres = regex_guard_reaches(script)
            got = reached == want and not unres
            detail = "reaches %s%s" % (sorted(reached), " (unresolved: %s)" % unres[0] if unres else "")
        except Exception as exc:
            got, detail = False, "raised %r" % exc
        print("%-4s guard    %s: %s" % ("OK" if got else "FAIL", why, detail))
        fails += not got
    total = len(EQUAL) + len(UNEQUAL) + len(REGEX_GUARDS)
    print("\n%s: %d fixtures, %d failed" % ("PASS" if not fails else "FAILED", total, fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
