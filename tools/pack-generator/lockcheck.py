"""Independent recomputation of every escape-room lock a pack prints, keyed by the audited bank's lock id.

A pack prints each set's answer, its common wrong answer and the figures of its worked solution. They come from
escape-rooms/variants.json, which scripts/gen-escape-variants.py generates and scripts/escape_set_checks.py admits.
This module recomputes them a SEPARATE way, from the variant's own givens only, and imports neither of those files,
so a fault in the generator cannot be copied into the check (agent-workflow §4.2: a check that reuses the game's own
formula is not independent).

Each function takes one variant (its givens and its stored values) and returns the values it expects, by key. The
generator compares each returned key with the variant's own; any difference fails the build. A room's pack builds only
when every lock in it has an entry here: a new room's locks are added here, by lock id, with their own method.

A lock whose pack asks for its answer in another unit than the room's (a config's "answer_units", contract
CAR-TRAP-PACK) also returns, under the key PRINTED, {"unit", "answer", "miss"}: its answer and common wrong answer
worked in that unit here, which the generator compares with the figures it prints. It is not a stored key.
"""
from fractions import Fraction
from math import gcd, isqrt


def _sensor_limit(v):
    """kiln-sensor-limit: the highest multiple of k that is not above the limit L, found by counting up in k.
    The common wrong answer is the first multiple past L; the worked line lists the multiple below, the answer and
    the one past."""
    k, L = v["k"], v["L"]
    reached = [m for m in range(k, L + 1) if m % k == 0]          # every multiple of k up to L, by enumeration
    answer = reached[-1]
    past = next(m for m in range(L + 1, L + k + 1) if m % k == 0)  # the first multiple above L
    return {"answer": answer, "miss": past, "mults": "%d, %d, %d" % (answer - k, answer, past)}


def _fan_restart(v):
    """kiln-fan-restart: the lowest common multiple of the two cycles, found by listing the multiples of the first
    until one is also a multiple of the second. The common wrong answer is the product; the worked lines list each
    cycle's multiples up to the answer."""
    a, b = v["a"], v["b"]
    m = a
    while m % b:
        m += a
    return {"answer": m, "miss": a * b,
            "multA": ", ".join(str(x) for x in range(a, m + 1, a)),
            "multB": ", ".join(str(x) for x in range(b, m + 1, b))}


def _cancel_check(v):
    """kiln-cancel-check: a + b / c with the division first. The common wrong answer works left to right,
    (a + b) / c. Exact arithmetic: a value that is not a whole number is returned as a Fraction and fails the
    comparison with the stored whole number."""
    a, b, c = v["a"], v["b"], v["c"]
    q = Fraction(b, c)
    ans, miss = a + q, Fraction(a + b, c)
    whole = lambda x: int(x) if x.denominator == 1 else x
    return {"answer": whole(ans), "miss": whole(miss), "quot": whole(q)}


def _christmas_cold_store(v):
    """Count whole hours against the scaled temperature inequality, including the wrong-sign starting point."""
    start, minimum, gain, hours = (v[k] for k in ("start", "min", "g", "h"))
    def first_hour(initial):
        t = 0
        while initial * hours + gain * t < minimum * hours:
            t += 1
        return t
    return {"answer": first_hour(start), "miss": first_hour(abs(start)),
            "rate": Fraction(gain, hours), "rise": minimum - start,
            "abs": abs(start), "short": minimum - abs(start)}


def _christmas_scale_clearance(v):
    """Convert every height to integer millimetres before subtracting the tree and stand."""
    ceiling_mm = int(Fraction(str(v["c"])) * 1000)
    tree_mm = v["d"] * v["k"] * 10
    stand_mm = v["s"] * 10
    if (ceiling_mm - tree_mm - stand_mm) % 10:
        raise ValueError("clearance is not a whole centimetre")
    return {"answer": (ceiling_mm - tree_mm - stand_mm) // 10,
            "miss": (ceiling_mm - tree_mm) // 10,
            "tree": tree_mm // 10, "total": (tree_mm + stand_mm) // 10,
            "ccm": ceiling_mm // 10}


def _christmas_combined_ratios(v):
    """Enumerate positive B, T, U triples and derive the displayed simplest ratio from the sole solution."""
    a, b, c, d, total = (v[k] for k in ("a", "b", "c", "d", "N"))
    matches = [(B, T, total - B - T)
               for B in range(1, total - 1)
               for T in range(1, total - B)
               if B * b == T * a and T * d == (total - B - T) * c]
    if len(matches) != 1:
        raise ValueError("combined ratios have %d positive solutions" % len(matches))
    B, T, U = matches[0]
    common = gcd(gcd(B, T), U)
    r1, r2, r3 = B // common, T // common, U // common
    miss = Fraction(total * d, a + b + d)
    return {"answer": U, "miss": int(miss) if miss.denominator == 1 else miss,
            "r1": r1, "r2": r2, "r3": r3,
            "parts": r1 + r2 + r3, "each": common}


def _divisors_by_pairs(N):
    """Every divisor of N, by trial pairs i x N/i for i up to the square root; a square's root is counted once."""
    found, i = set(), 1
    while i * i <= N:
        if N % i == 0:
            found.add(i)
            found.add(N // i)
        i += 1
    return sorted(found)


def _chokey_factor_count(v):
    """chokey-factor-count: the divisors of N by trial pairs up to its square root. The common wrong answer is one
    pair missed, so two fewer; the worked line lists every factor."""
    fac = _divisors_by_pairs(v["N"])
    return {"answer": len(fac), "miss": len(fac) - 2, "facN": ", ".join(str(x) for x in fac)}


def _chokey_prime_volumes(v):
    """chokey-prime-volumes: the primes up to V by a sieve of Eratosthenes. The common wrong answer counts 1 as a
    prime, so one more; the worked line lists the primes."""
    V = v["V"]
    alive = [False, False] + [True] * (V - 1)
    for i in range(2, V + 1):
        if alive[i]:
            for m in range(i * i, V + 1, i):
                alive[m] = False
    primes = [i for i in range(V + 1) if alive[i]]
    return {"answer": len(primes), "miss": len(primes) + 1, "primes": ", ".join(str(x) for x in primes)}


def _chokey_hcf_bundles(v):
    """chokey-hcf-bundles: the highest common factor by repeated subtraction (Euclid's first form, not math.gcd).
    The common wrong answer is the lowest common multiple, found by listing multiples of the larger number until
    one is a multiple of the smaller; the worked lines list each number's factors."""
    a, b = v["a"], v["b"]
    x, y = a, b
    while x != y:
        if x > y:
            x -= y
        else:
            y -= x
    big, small = max(a, b), min(a, b)
    m = big
    while m % small:
        m += big
    return {"answer": x, "miss": m,
            "facA": ", ".join(str(d) for d in _divisors_by_pairs(a)),
            "facB": ", ".join(str(d) for d in _divisors_by_pairs(b))}


def _dewey_sort_arm(v):
    """dewey-sort-arm: every book's decimal part as a whole number scaled to a common number of decimal places
    (.4 and .07 become 40 and 7 in hundredths), so the order is integer order. The answer is the held book's
    1-based slot, smallest first; the common wrong answer is its slot when the parts are read as whole numbers
    (.07 as 7, .4 as 4). The worked lines rebuild the drop order and the sorted shelf."""
    shelf, parts = v["shelf"], v["parts"]
    held_shelf, _, held = v["book"].partition(".")
    if held_shelf != shelf or held not in parts or parts.count(held) != 1:
        raise ValueError("the held book %r is not one book on shelf %s" % (v["book"], shelf))
    places = max(len(d) for d in parts)
    scaled = {d: int(d) * 10 ** (places - len(d)) for d in parts}
    if len(set(scaled.values())) != len(parts) or len({int(d) for d in parts}) != len(parts):
        raise ValueError("two books on shelf %s are equal" % shelf)
    by_value = sorted(parts, key=lambda d: scaled[d])
    by_whole = sorted(parts, key=int)
    return {"answer": by_value.index(held) + 1, "miss": by_whole.index(held) + 1,
            "list": ", ".join("%s.%s" % (shelf, d) for d in parts),
            "sorted": ", ".join("%s.%s" % (shelf, d) for d in by_value)}


def _deflector_straight_line(v):
    """deflector-straight-line: angles on a straight line make a half turn, 180 degrees, so the other angle is
    180 - x. The common wrong answer takes them as a right angle, a quarter turn: 90 - x."""
    half, quarter = 360 // 2, 360 // 4
    return {"answer": half - v["x"], "miss": quarter - v["x"], "half": half, "quarter": quarter}


def _fines_pence_to_pounds(v):
    """fines-pence-to-pounds: p pence a day for d days is the fine for one book; times n books is the total in
    pence; pounds by divmod by 100, which must leave no pence. The common wrong answer is the pence total typed
    as pounds."""
    each = v["p"] * v["d"]
    total = each * v["n"]
    pounds, pennies = divmod(total, 100)
    if pennies:
        raise ValueError("the fine %dp is not a whole number of pounds" % total)
    return {"answer": pounds, "miss": total, "each": each, "hundred": 100}


PRINTED = "printed"   # a function's optional extra key: its answer and common wrong answer in a pack's printed unit


def _metres(cm):
    """A whole number of centimetres written in metres to two decimal places: 235 is "2.35"."""
    return "%d.%02d" % divmod(cm, 100)


def _head_bay_lower_bound(v):
    """head-bay-lower-bound: the smallest width that is written down as W m to the nearest ten centimetres, worked
    in whole centimetres so that no decimal is ever subtracted. W is a whole number of tens of centimetres; half of
    ten centimetres is 5 cm; the bounds are W x 100 - 5 and W x 100 + 5. The common wrong answer is W itself, the
    width on the sheet taken as exact. The stored figures are in metres: each is rebuilt from its centimetres, the
    numbers by reading their two-decimal text. The pack asks for this lock in centimetres, so the function also
    gives its own centimetre figures (PRINTED), which the generator compares with what it prints."""
    w_cm = Fraction(str(v["W"])) * 100
    if w_cm.denominator != 1 or w_cm % 10:
        raise ValueError("the width %r m is not a whole number of tens of centimetres" % v["W"])
    w_cm, step_cm = int(w_cm), 10
    half_cm = step_cm // 2
    low_cm, high_cm = w_cm - half_cm, w_cm + half_cm
    return {"answer": float(_metres(low_cm)), "miss": float(_metres(w_cm)),
            "half": _metres(half_cm), "lb": _metres(low_cm), "ub": _metres(high_cm),
            "aTxt": _metres(low_cm), "mTxt": _metres(w_cm),
            PRINTED: {"unit": "cm", "answer": low_cm, "miss": w_cm}}


def _boom_gate_sector(v):
    """boom-gate-sector: the tip travels an arc of k pi metres on a circle of radius r, whose circumference is
    2 pi r = (2r) pi metres. The pi is in both, so the fraction of a full turn is k / (2r), exactly, and the angle
    is 360 x k / (2r). k is read from the arc as the clue prints it ("0.75&pi;"; "&pi;" alone is 1 pi), never from
    the stored angle. The common wrong answer, by the room's rule (its missSays): the circle worked out as pi x r,
    half the circumference, which gives 360 x k / r, twice the angle. The worked line's figures are the
    circumference's multiple of pi and how many of the arc make a full turn."""
    arc = v["kpi"]
    if not arc.endswith("&pi;"):
        raise ValueError("the arc %r is not a multiple of pi" % arc)
    k = Fraction(arc[:-len("&pi;")] or "1")
    r = v["r"]
    circ = 2 * r                                  # the circumference is circ x pi
    angle = 360 * k / circ
    half_circle = 360 * k / r                     # the same arc against pi x r
    turns = Fraction(circ) / k                    # arcs in a full turn
    for name, x in (("angle", angle), ("common wrong angle", half_circle), ("arcs in a full turn", turns)):
        if x.denominator != 1:
            raise ValueError("the %s, %s, is not a whole number" % (name, x))
    return {"answer": int(angle), "miss": int(half_circle), "th": int(angle), "circ": circ, "turns": int(turns)}


def _ev_charger_quadratic(v):
    """ev-charger-quadratic: the currents at which x^2 - bx + c is zero, found by trying every whole current the
    dial has, 0 to 15. There must be exactly two, one at or under the alarm limit and one over it: the answer is the
    one not above the limit, the common wrong answer the other. The two are then confirmed a second way that tries
    nothing: the quadratic formula in whole numbers, (b -/+ root(b^2 - 4c)) / 2, the discriminant a perfect square."""
    b, c, lim = v["b"], v["c"], v["lim"]
    zeros = [x for x in range(0, 16) if x * x - b * x + c == 0]
    inside = [x for x in zeros if x <= lim]
    outside = [x for x in zeros if x > lim]
    if len(zeros) != 2 or len(inside) != 1 or len(outside) != 1:
        raise ValueError("x^2 - %dx + %d has zeros %s on the dial, not one each side of %d A" % (b, c, zeros, lim))
    disc = b * b - 4 * c
    root = isqrt(disc) if disc >= 0 else -1
    if root * root != disc or (b - root) % 2 or [(b - root) // 2, (b + root) // 2] != zeros:
        raise ValueError("the quadratic formula does not give the zeros %s of x^2 - %dx + %d" % (zeros, b, c))
    return {"answer": inside[0], "miss": outside[0]}


RECOMPUTE = {
    "head-bay-lower-bound": _head_bay_lower_bound,
    "boom-gate-sector": _boom_gate_sector,
    "ev-charger-quadratic": _ev_charger_quadratic,
    "kiln-sensor-limit": _sensor_limit,
    "kiln-fan-restart": _fan_restart,
    "kiln-cancel-check": _cancel_check,
    "christmas-cold-store": _christmas_cold_store,
    "christmas-scale-clearance": _christmas_scale_clearance,
    "christmas-combined-ratios": _christmas_combined_ratios,
    "chokey-factor-count": _chokey_factor_count,
    "chokey-prime-volumes": _chokey_prime_volumes,
    "chokey-hcf-bundles": _chokey_hcf_bundles,
    "dewey-sort-arm": _dewey_sort_arm,
    "deflector-straight-line": _deflector_straight_line,
    "fines-pence-to-pounds": _fines_pence_to_pounds,
}


# ---- the final padlock (Amendment 5): an evaluator and a search of its own, sharing nothing with final.py -----------
import ast as _ast
import itertools as _it

_TO_PY = {"×": "*", "÷": "/", "−": "-", "+": "+"}


def _parse(text):
    """The printed expression (x / + - in the pack's symbols) as a Python expression tree; brackets are refused."""
    if "(" in text or ")" in text:
        raise ValueError("brackets")
    py = "".join(_TO_PY.get(ch, ch) for ch in text)
    tree = _ast.parse(py, mode="eval").body
    for node in _ast.walk(tree):
        if not isinstance(node, (_ast.BinOp, _ast.Constant, _ast.Add, _ast.Sub, _ast.Mult, _ast.Div)):
            raise ValueError("not + - x / on numbers: %s" % type(node).__name__)
    return tree


def _eval(node):
    """Python's own precedence (x and / before + and -, left to right), in exact fractions."""
    if isinstance(node, _ast.Constant):
        return Fraction(str(node.value))
    a, b = _eval(node.left), _eval(node.right)
    if isinstance(node.op, _ast.Add):
        return a + b
    if isinstance(node.op, _ast.Sub):
        return a - b
    if isinstance(node.op, _ast.Mult):
        return a * b
    return a / b


def _flatten(node):
    """The expression's class: its signed terms, each its factors with their exponents, as sorted tuples."""
    def terms(n, sign):
        if isinstance(n, _ast.BinOp) and isinstance(n.op, (_ast.Add, _ast.Sub)):
            return terms(n.left, sign) + terms(n.right, sign if isinstance(n.op, _ast.Add) else -sign)
        return [(sign, tuple(sorted(factors(n, 1))))]

    def factors(n, e):
        if isinstance(n, _ast.BinOp) and isinstance(n.op, (_ast.Mult, _ast.Div)):
            return factors(n.left, e) + factors(n.right, e if isinstance(n.op, _ast.Mult) else -e)
        return [(e, Fraction(str(n.value)))]
    return tuple(sorted(terms(node, 1)))


def final_value(text):
    return _eval(_parse(text))


def final_classes(nums, target):
    """Every distinct expression of nums (each once, + - x /, no brackets) whose value is target."""
    hits = set()
    for perm in _it.permutations(nums):
        for ops in _it.product("+−×÷", repeat=len(nums) - 1):
            text = str(perm[0]) + "".join(" %s %s" % (o, x) for o, x in zip(ops, perm[1:]))
            tree = _parse(text)
            if _eval(tree) == target:
                hits.add(_flatten(tree))
    return hits


# The pack's shape (Amendment 7), counted here from the parse tree's own operator nodes.
SHAPE_OPS = {
    "times-and-plus-or-minus": lambda m, d, a, s: m == 1 and d == 0 and a + s == 1,
    "plus-and-minus": lambda m, d, a, s: m == 0 and d == 0 and a == 1 and s == 1,
}


def _ops(tree):
    kinds = [type(n.op) for n in _ast.walk(tree) if isinstance(n, _ast.BinOp)]
    return (kinds.count(_ast.Mult), kinds.count(_ast.Div), kinds.count(_ast.Add), kinds.count(_ast.Sub))


def final_problems(letter, nums, final, shape):
    """Problems with one set's final padlock, checked from its printed target and expression alone: a whole number,
    each answer once, the pack's shape, the value, and exactly one expression of any shape reaching it."""
    out, t, expr = [], final["target"], final["expr"]
    if not (isinstance(t, int) and t >= 0):
        out.append("set %s: target %r is not a whole number" % (letter, t))
    if t == sum(nums):
        out.append("set %s: target %s is just the sum of the answers" % (letter, t))
    if t in nums:
        out.append("set %s: target %s is one of the set's own answers" % (letter, t))
    try:
        got = final_value(expr)
        used = sorted(Fraction(str(n.value)) for n in _ast.walk(_parse(expr)) if isinstance(n, _ast.Constant))
    except (ValueError, SyntaxError) as e:
        return out + ["set %s: expression %r cannot be read (%s)" % (letter, expr, e)]
    if shape not in SHAPE_OPS:
        out.append("set %s: the pack's shape %r is unknown" % (letter, shape))
    elif not SHAPE_OPS[shape](*_ops(_parse(expr))):
        out.append("set %s: expression %r is not the pack's shape (%s)" % (letter, expr, shape))
    for node in _ast.walk(_parse(expr)):            # Amendment 11: every product mental- or quick-method friendly
        if isinstance(node, _ast.BinOp) and isinstance(node.op, _ast.Mult) \
                and isinstance(node.left, _ast.Constant) and isinstance(node.right, _ast.Constant):
            a, b = node.left.value, node.right.value
            if not (a % 5 == 0 or b % 5 == 0 or a <= 12 or b <= 12):
                out.append("set %s: product %s x %s has no factor a multiple of 5 or 12 or less" % (letter, a, b))
    if used != sorted(Fraction(str(n)) for n in nums):
        out.append("set %s: expression %r does not use each answer %s exactly once" % (letter, expr, list(nums)))
    if got != t:
        out.append("set %s: expression %r makes %s, not the target %s" % (letter, expr, got, t))
    n = len(final_classes(nums, t))
    if n != 1:
        out.append("set %s: %d expressions reach the target %s, not exactly one" % (letter, n, t))
    return out
