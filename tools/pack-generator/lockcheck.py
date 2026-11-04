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
