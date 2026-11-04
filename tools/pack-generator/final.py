"""The final padlock (Amendments 5 and 7, Jon, 4 Nov 2026): the generator's side.

Each set's lock answers are used exactly once, with no brackets (x and / before + and -, left to right), to make the
set's target. An expression with no brackets is a sum of signed terms, each a product of factors, some divided; two
expressions are the SAME when they have the same signed terms with the same factors, in any order (commutativity of
+ and x applied throughout: a + b and b + a, a - b + c and a + c - b, a x b and b x a). "Reachable in exactly one way"
counts these classes over EVERY expression with + - x /, in exact fractions, whatever the pack's shape: a second route,
in any shape or through a fractional step, would make the key ambiguous, so none may exist.

Every set in a pack uses the same SHAPE (Amendment 7: sets race each other, so the final padlock is equally hard for
all): by default one x and one + or - (Option B, "plus-and-minus": one + and one -, set by the room's config). A target
is a whole number of any size, never one of the set's own answers, never the plain sum, and its expression works out
in whole, non-negative steps (the generator's two rules, kept by Amendment 7); its product has a factor that is a
multiple of 5 or 12 or less (Amendment 11), and students are never told the shape. A set with no such target fails the
build: there is no fallback to an easier shape.

tools/pack-generator/lockcheck.py checks every target again by its own evaluator, search and shape count.
"""
import itertools
import random
from collections import defaultdict
from fractions import Fraction

SYM = {"+": "+", "-": "−", "*": "×", "/": "÷"}
SHAPES = {   # name: (the rule as the locks page says it, the operator counts it allows)
    "times-and-plus-or-minus": ("one &times; and one + or &minus;",
                                lambda c: c["*"] == 1 and c["/"] == 0 and c["+"] + c["-"] == 1),
    "plus-and-minus": ("one + and one &minus;",
                       lambda c: c["*"] == 0 and c["/"] == 0 and c["+"] == 1 and c["-"] == 1),
}
DEFAULT_SHAPE = "times-and-plus-or-minus"
# Amendment 11: students are told only "each answer once, any of + - x /, no brackets, no calculator"; the shape is
# never printed for them. Every product in a set's one solution must be friendly for mental or quick written methods.


def friendly(form):
    """True when every product in the class has a factor that is a multiple of 5 or is 12 or less (Amendment 11)."""
    for _, factors in form:
        mult = [x for e, x in factors if e == 1]
        if len(mult) > 1 and not any(x % 5 == 0 or x <= 12 for x in mult):
            return False
    return True


def canon(perm, ops):
    """The class of one written expression: a sorted tuple of (sign, sorted factors), a factor being (exponent, number)."""
    terms, cur, sign = [], [(1, perm[0])], 1
    for op, x in zip(ops, perm[1:]):
        if op in "*/":
            cur.append((1 if op == "*" else -1, x))
        else:
            terms.append((sign, tuple(sorted(cur))))
            cur, sign = [(1, x)], (1 if op == "+" else -1)
    terms.append((sign, tuple(sorted(cur))))
    return tuple(sorted(terms))


def value(form):
    total = Fraction(0)
    for sign, factors in form:
        t = Fraction(1)
        for e, x in factors:
            t = t * x if e == 1 else t / x
        total += sign * t
    return total


def op_counts(form):
    """How many of each operator any writing of the class uses (a positive term first, a multiplied factor first)."""
    c = {"+": -1, "-": 0, "*": 0, "/": 0}
    for sign, factors in form:
        c["+" if sign == 1 else "-"] += 1
        c["*"] += sum(1 for e, _ in factors if e == 1) - 1
        c["/"] += sum(1 for e, _ in factors if e == -1)
    return c


def forms(nums):
    """{value: set of classes} over every expression of nums."""
    out = defaultdict(set)
    for perm in itertools.permutations(nums):
        for ops in itertools.product("+-*/", repeat=len(nums) - 1):
            f = canon(perm, ops)
            out[value(f)].add(f)
    return out


def writing(form):
    """(tokens, steps) writing a class with every step whole and non-negative, or None if no order of it does: the
    positive terms first (largest first), then the negative; in each term, an order of its factors that starts with a
    multiplied one and keeps each step whole."""
    def term_order(factors):
        for order in itertools.permutations(factors):
            if order[0][0] != 1:
                continue
            acc, ok, steps = Fraction(order[0][1]), True, []
            for e, x in order[1:]:
                nxt = acc * x if e == 1 else acc / x
                if nxt.denominator != 1 or nxt < 0:
                    ok = False
                    break
                steps.append("%s %s %s = %s" % (fmt(acc), SYM["*" if e == 1 else "/"], fmt(x), fmt(nxt)))
                acc = nxt
            if ok:
                return order, acc, steps
        return None

    done = []
    for sign, factors in form:
        t = term_order(factors)
        if t is None:
            return None
        done.append((sign, t))
    if not any(s == 1 for s, _ in done):
        return None
    done.sort(key=lambda st: (-st[0], -st[1][1]))
    tokens, steps, run = [], [], None
    for i, (sign, (order, val, tsteps)) in enumerate(done):
        if i:
            tokens.append("+" if sign == 1 else "-")
        tokens.append(order[0][1])
        for e, x in order[1:]:
            tokens += ["*" if e == 1 else "/", x]
        steps += tsteps
        if run is None:
            run = val
        else:
            nxt = run + sign * val
            if nxt < 0:
                return None
            steps.append("%s %s %s = %s" % (fmt(run), SYM["+" if sign == 1 else "-"], fmt(val), fmt(nxt)))
            run = nxt
    return tokens, steps


def fmt(x):
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else "%s/%s" % (x.numerator, x.denominator)


def show(tokens):
    return " ".join(SYM[t] if isinstance(t, str) else fmt(t) for t in tokens)


def candidates(nums, shape):
    """{target: (form, tokens, steps)} for every target the rules allow, from these numbers, in this shape."""
    allowed = SHAPES[shape][1]
    out = {}
    for v, fs in forms(nums).items():
        if v.denominator != 1 or v < 0 or len(fs) != 1 or v == sum(nums) or v in nums:
            continue
        form = next(iter(fs))
        if not allowed(op_counts(form)) or not friendly(form):
            continue
        w = writing(form)
        if w:
            out[int(v)] = (form, w[0], w[1])
    return out


def why_not(nums, t, shape):
    """Why target t is not allowed for these numbers in this shape, in words."""
    fs = forms(nums).get(Fraction(t), set())
    if t < 0:
        return "%s is not a whole number" % t
    if not fs:
        return "no expression makes %s" % t
    if len(fs) > 1:
        return "%d expressions make %s, not exactly one" % (len(fs), t)
    if t == sum(nums):
        return "%s is just the sum of the answers" % t
    if t in nums:
        return "%s is one of the set's own answers" % t
    if not SHAPES[shape][1](op_counts(next(iter(fs)))):
        return "the one expression that makes %s is not the pack's shape" % t
    if not friendly(next(iter(fs))):
        return "the one expression that makes %s has a product with no factor a multiple of 5 or 12 or less" % t
    return "the one expression that makes %s needs a fraction or a negative step" % t


def choose(nums, seed, letter, shape=DEFAULT_SHAPE, forced=None):
    """The set's final padlock {target, tokens, expr, steps, shape}, or (None, reason)."""
    if shape not in SHAPES:
        return None, "unknown final-padlock shape %r (one of %s)" % (shape, sorted(SHAPES))
    if len(nums) != 3:
        return None, "the final padlock's shapes need exactly 3 lock answers, and this room has %d" % len(nums)
    c = candidates(nums, shape)
    if forced is not None:
        if forced not in c:
            return None, why_not(nums, forced, shape)
        pick = forced
    else:
        if not c:
            return None, "no target can be made in exactly one way in the pack's shape (%s)" % shape
        pick = random.Random("%s-%s" % (seed, letter)).choice(sorted(c))
    form, tokens, steps = c[pick]
    return {"target": pick, "tokens": tokens, "expr": show(tokens), "steps": steps, "shape": shape}, None
