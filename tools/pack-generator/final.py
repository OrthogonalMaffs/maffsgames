"""The final padlock (Amendment 5, Jon, 4 Nov 2026): the generator's side.

Each set's lock answers are used exactly once, with + - x and / and no brackets (x and / before + and -, left to right),
to make the set's target. An expression with no brackets is a sum of signed terms, each a product of factors, some
divided; two expressions are the SAME when they have the same signed terms with the same factors, in any order
(commutativity of + and x applied throughout: a + b and b + a, a - b + c and a + c - b, a x b / c and b x a / c).
"Reachable by exactly one expression" counts these classes, over EVERY expression, in exact fractions: a route through
a fractional step still counts, so no second answer can hide.

A target, per set (or --target for every set), is a whole number from 10 to 999, reached by exactly one expression,
never the plain sum of the answers. Two rules of the generator's own: the target is never one of the set's own answers
(72 + 28 - 50 = 50 would give it away), and its expression works out in whole, non-negative steps (so the key's
working never needs a fraction). Targets whose expression uses x or / are preferred.

tools/pack-generator/lockcheck.py checks every target again by its own evaluator and search (independent of this file).
"""
import itertools
import random
from collections import defaultdict
from fractions import Fraction

LOW, HIGH = 10, 999
SYM = {"+": "+", "-": "−", "*": "×", "/": "÷"}


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


def uses_mul_div(form):
    return any(len(factors) > 1 for _, factors in form)


def candidates(nums):
    """{target: (form, tokens, steps)} for every target the rules allow, from these numbers."""
    plain_sum = sum(nums)
    out = {}
    for v, fs in forms(nums).items():
        if v.denominator != 1 or not LOW <= v <= HIGH or len(fs) != 1 or v == plain_sum or v in nums:
            continue
        form = next(iter(fs))
        w = writing(form)
        if w:
            out[int(v)] = (form, w[0], w[1])
    return out


def why_not(nums, t):
    """Why target t is not allowed for these numbers, in words."""
    if not (LOW <= t <= HIGH):
        return "%s is outside %d to %d" % (t, LOW, HIGH)
    fs = forms(nums).get(Fraction(t), set())
    if not fs:
        return "no expression makes %s" % t
    if len(fs) > 1:
        return "%d expressions make %s, not exactly one" % (len(fs), t)
    if t == sum(nums):
        return "%s is just the sum of the answers" % t
    if t in nums:
        return "%s is one of the set's own answers" % t
    return "the one expression that makes %s needs a fraction or a negative step" % t


def choose(nums, seed, letter, forced=None):
    """The set's final padlock {target, tokens, expr, steps, mul_div}, or (None, reason)."""
    c = candidates(nums)
    if forced is not None:
        if forced not in c:
            return None, why_not(nums, forced)
        pick = forced
    else:
        if not c:
            return None, "no target from %d to %d can be reached by exactly one expression" % (LOW, HIGH)
        preferred = sorted(t for t, (f, _, _) in c.items() if uses_mul_div(f))
        pool = preferred or sorted(c)
        pick = random.Random("%s-%s" % (seed, letter)).choice(pool)
    form, tokens, steps = c[pick]
    return {"target": pick, "tokens": tokens, "expr": show(tokens), "steps": steps,
            "mul_div": uses_mul_div(form)}, None
