"""Independent recomputation of every escape-room lock a pack prints, keyed by the audited bank's lock id.

A pack prints each set's answer, its common wrong answer and the figures of its worked solution. They come from
escape-rooms/variants.json, which scripts/gen-escape-variants.py generates and scripts/escape_set_checks.py admits.
This module recomputes them a SEPARATE way, from the variant's own givens only, and imports neither of those files,
so a fault in the generator cannot be copied into the check (agent-workflow §4.2: a check that reuses the game's own
formula is not independent).

Each function takes one variant (its givens and its stored values) and returns the values it expects, by key. The
generator compares each returned key with the variant's own; any difference fails the build. A room's pack builds only
when every lock in it has an entry here: a new room's locks are added here, by lock id, with their own method.
"""
from fractions import Fraction


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


RECOMPUTE = {
    "kiln-sensor-limit": _sensor_limit,
    "kiln-fan-restart": _fan_restart,
    "kiln-cancel-check": _cancel_check,
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
