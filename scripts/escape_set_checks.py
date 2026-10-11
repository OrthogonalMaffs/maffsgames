"""The escape rooms' per-set checks: one copy, used where sets are made and where they are served.

Every lock carries a library of number sets (escape-rooms/variants.json). A set is correct when it passes
the tests the lock bank is held to:

  * exactly one setting on the instrument's own grid solves it
    (docs/escape-puzzle-bank.md: "a lock with two answers is not a lock")
  * the answer is actually settable: on the step, inside the range
  * the misconception is settable too, and is not the answer
    (an unreachable misconception means that response never fires)
  * no number printed in the clue equals the answer: the trap the checker
    in check-lock-bank.py explicitly cannot see
  * the answer does not sit at the end of a dial's or slider's travel (a keypad has none)

Two importers (contract ESCAPE-SET-CHECKS, 11 Oct 2026):
  scripts/gen-escape-variants.py   admits a candidate set only if check() passes (then applies its own
                                   spread rule, which is about the library, not the set)
  scripts/check-escape-rooms.py    runs check() on every set of every live room in CI

Until then these tests lived only in the generator, which is run by hand, so an edited or new set in
variants.json could pass CI unchecked. They moved here unchanged: keep()'s per-set tests became check_set(),
each lock's instrument, clue figures and solver became its entry in LOCKS, and the two locks with two
instruments, which the generator checked inline, became check_rugby_bases() and check_cookie_simultaneous().

A lock with no entry here has no check: check() says so, and check-escape-rooms.py fails a live room that
has one. A new lock adds its entry here, and the generator then uses it.

Pure functions, no file I/O.
"""
import itertools, math
from collections import namedtuple
from fractions import Fraction
from math import gcd, factorial


# ---------------------------------------------------------------- instruments
def grid(lo, hi, step):
    """Every value the instrument can actually be set to."""
    n = int(round((hi - lo) / step))
    return [round(lo + i * step, 6) for i in range(n + 1)]


class Keypad(tuple):
    """An instrument range that is a keypad: check_set() skips its end-of-travel rule (see keypad())."""


def keypad(n):
    """A keypad as an instrument range, for either mode (canon §11): `digits: n` takes exactly n
    digits (60 entered as 060), `maxDigits: n` takes 1 to n digits, no leading zero, Set to submit
    (KEYPAD-VARIABLE). Both set exactly the whole numbers 0 to 10^n - 1, so check_set()'s on_grid test is the
    settable rule for both: the answer and the misconception must each fit in n digits (a four-digit
    misconception needs n >= 4). What differs is the display, not what can be entered.

    A keypad has no travel: nothing starts at an end, and no answer is reached by pushing a needle to a
    stop, so check_set()'s end-of-travel rule does not apply to it (LIBRARY-JAM-BUILD, Jon 10 Oct 2026). Under
    that rule a four-digit keypad rejected every answer under 400, so a two-digit answer with a four-digit
    misconception (54 against 5400) could never be built. Lifting it changed no existing library."""
    return Keypad((0, 10 ** n - 1, 1))


def on_grid(v, lo, hi, step):
    if v < lo - 1e-9 or v > hi + 1e-9:
        return False
    return abs((v - lo) / step - round((v - lo) / step)) < 1e-6


def unique(solutions, answer):
    return len(solutions) == 1 and abs(solutions[0] - answer) < 1e-9


# ---------------------------------------------------------------- the solvers' arithmetic
def is_prime(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def bay_sols(W):
    """Every setting on the slider that rounds, half up, to W at 0.1 m (the draft's solver)."""
    return [x for x in grid(2, 3, 0.01) if (round(x * 100) + 5) // 10 == round(W * 10)]


def factor_count(n):
    return sum(1 for d in range(1, n + 1) if n % d == 0)


def prime_count(v):
    return sum(1 for p in range(2, v + 1) if is_prime(p))


def passcodes(k, L):
    return sum(1 for t in itertools.product(range(k), repeat=L) if len(set(t)) == L)


# ---------------------------------------------------------------- one instrument
def check_set(var, ins, clue_numbers, solver):
    """The first test a set fails, or None if it passes every one."""
    lo, hi, step = ins
    a, m = var["answer"], var.get("miss")
    if not on_grid(a, lo, hi, step):
        return "answer not settable"
    if m is not None and not on_grid(m, lo, hi, step):
        return "misconception not settable"
    if m is not None and abs(a - m) < 1e-9:
        return "misconception equals answer"
    sols = [v for v in grid(lo, hi, step) if solver(v, var)]
    if not unique(sols, a):
        return f"{len(sols)} solutions"
    if any(abs(n - a) < 1e-9 for n in clue_numbers(var)):
        return "answer is printed in its own clue"
    edge = (hi - lo) * 0.04
    if not isinstance(ins, Keypad) and not (lo + edge <= a <= hi - edge):   # a keypad has no travel
        return "answer sits at the end of the travel"
    return None


# ---------------------------------------------------------------- two instruments
# These two locks' answers are pairs, so the generator checked them inline rather than through keep().
# The answer and misconception are read from the set as served; the generator builds them from the same
# parameters, so for every set it makes this is the test it always ran.
def check_rugby_bases(var):
    """F3 index laws, two dials 0-100: 2^H x 4^A = 2^N with A = H + diff, so H + 2A = N.
    Misconception: read 4^A as 2^A, take A = N and H = N - diff."""
    N, diff = var["N"], var["diff"]
    H, A = var["answer"]
    mH, mA = var["miss"]
    sols = [(h, a) for h in range(101) for a in range(101) if h + 2 * a == N and a == h + diff]
    if len(sols) != 1 or sols[0] != (H, A):
        return f"{len(sols)} solutions"
    if mH > 100 or mA > 100:
        return "misconception off the dials"
    if H == mH and A == mA:
        return "misconception equals answer"
    return None


def check_cookie_simultaneous(var):
    """I2 simultaneous equations, two tags 0-10: a1 C + b1 P = t1 and a2 C + b2 P = t2, eliminated by
    scaling the second by mult. Misconception: the right pair of numbers on the wrong two tags."""
    a1, b1, t1, a2, b2, t2, mult = (var[k] for k in ("a1", "b1", "t1", "a2", "b2", "t2", "mult"))
    C, P = var["answer"]
    if b2 * mult - b1 <= 0 or t1 > 30 or t2 > 30 or t1 == t2:
        return "not a tidy elimination"
    sols = [(c, p) for c in range(11) for p in range(11)
            if a1 * c + b1 * p == t1 and a2 * c + b2 * p == t2]
    if len(sols) != 1 or sols[0] != (C, P):
        return f"{len(sols)} solutions"
    return None


# ---------------------------------------------------------------- every lock
# ins: the instrument (lo, hi, step), or keypad(n). clue_numbers(v): the figures the clue prints.
# solver(x, v): True when setting x opens the lock.
Lock = namedtuple("Lock", "ins clue_numbers solver")

LOCKS = {
    "sprinkler-sector-area": Lock(
        (10, 360, 10),
        lambda v: [v["r"], v["K"]],
        lambda x, v: x * v["r"] * v["r"] == 360 * v["K"]),
    "dodgeball-pressure-boyle": Lock(
        (0, 100, 1),
        lambda v: [v["V1"], v["P1"], v["V2"]],
        lambda x, v: x * v["V2"] == v["P1"] * v["V1"]),
    "locker-nth-term": Lock(
        (0, 99, 1),
        lambda v: [v["d1"], v["c1"], v["d2"], v["c2"], v["d3"], v["c3"], v["dT"]],
        lambda x, v: (x - v["c1"]) * (v["d3"] - v["d1"]) ==
            (v["c3"] - v["c1"]) * (v["dT"] - v["d1"])),
    "finance-reverse-percentage": Lock(
        keypad(4),
        lambda v: [v["total"], v["pct"]],
        lambda x, v: x * (100 + v["pct"]) == v["total"] * 100),
    "dj-deposit-compound": Lock(
        (1, 20, 1),
        lambda v: [v["dep"], v["rate"], float(v["bal"])],
        lambda x, v: Fraction(v["dep"]) * Fraction(100 + v["rate"], 100) ** int(x)
            == Fraction(v["bal"])),
    "wifi-venn-router": Lock(
        (0, 100, 1),
        lambda v: [v["total"], v["A"], v["B"], v["neither"]],
        lambda x, v: v["A"] + v["B"] - x + v["neither"] == v["total"]),
    "hamster-wheel-rpm": Lock(
        (0, 500, 1),
        lambda v: [v["d"], v["K"]],
        lambda x, v: x * v["d"] == v["K"] * 60),
    "hamster-feeder-bounds": Lock(
        (0, 1000, 1),
        lambda v: [v["X"], v["D"]],
        lambda x, v: 2 * x == v["X"] * (2 * v["D"] - 1)),
    "heat-lamp-gradient": Lock(
        (0, 20, 0.1),
        lambda v: [v["t1"], v["T1"], v["t2"], v["T2"]],
        lambda x, v: abs(x * (v["t2"] - v["t1"]) - (v["T2"] - v["T1"])) < 1e-6),
    "elbow-patch-scale": Lock(
        (1, 100, 1),
        lambda v: [v["L1"], v["A1"], v["L2"]],
        lambda x, v: x * v["L1"] * v["L1"] == v["A1"] * v["L2"] * v["L2"]),
    "sprinkler-flow-rates": Lock(
        (1, 60, 1),
        lambda v: [v["a"], v["b"]],
        lambda x, v: x * v["a"] + x * v["b"] == v["a"] * v["b"]),
    "mechanical-keyboard-perms": Lock(
        (1, 100, 1),
        lambda v: [v["n"]],
        lambda x, v: x * v["denom"] == factorial(v["n"])),
    "vault-trajectory-vertex": Lock(
        (0, 5, 0.1),
        lambda v: [],       # the equation prints coefficients, not the height
        lambda x, v: abs(x - (float(v["c"]) + float(v["b"]) ** 2 / (4 * v["a"]))) < 1e-9),
    "mat-tiling-hcf": Lock(
        (0.1, 5, 0.1),
        lambda v: [],
        lambda x, v: (v["w10"] % round(x * 10) == 0 and v["l10"] % round(x * 10) == 0
            and round(x * 10) == gcd(v["w10"], v["l10"]))),
    "patrol-lcm-timer": Lock(
        (1, 200, 1),
        lambda v: [v["a"], v["b"], v["c"]],
        lambda x, v: x % v["a"] == 0 and x % v["b"] == 0 and x % v["c"] == 0),
    "cube-surface-volume": Lock(
        keypad(4),
        lambda v: [v["SA"]],
        lambda x, v: any(x == n ** 3 and 6 * n * n == v["SA"] for n in range(1, 50))),
    "canteen-freezer-inequality": Lock(
        (0, 50, 1),
        lambda v: [v["lo"], v["m"], v["k"], v["hi"]],
        lambda x, v: v["lo"] < v["m"] * x - v["k"] < v["hi"] and is_prime(int(x))),
    "canteen-mean-calories": Lock(
        (0, 1000, 1),
        lambda v: [v["e1"], v["e2"], v["e3"], v["e4"], v["T"]],
        lambda x, v: v["e1"] + v["e2"] + v["e3"] + v["e4"] + x == 5 * v["T"]),
    "kale-fraction-drain": Lock(
        (0, 200, 1),
        lambda v: [v["N"], v["n"], v["d"]],
        lambda x, v: v["d"] * (v["N"] - x) == v["n"] * v["N"]),
    "visitor-space-bounds": Lock(
        (0, 20, 0.25),
        lambda v: [v["L"], v["W"]],
        lambda x, v: abs(x - (v["L"] - 0.5) * (v["W"] - 0.5)) < 1e-9),
    "head-bay-lower-bound": Lock(
        (2, 3, 0.01),
        lambda v: [v["W"]],
        lambda x, v: abs(x - min(bay_sols(v["W"]))) < 1e-9),
    "boom-gate-sector": Lock(
        (0, 180, 5),
        lambda v: [v["r"], float(v["k"])],
        lambda x, v: abs(x * v["r"] - 180 * float(v["k"])) < 1e-9),
    "ev-charger-quadratic": Lock(
        (0, 15, 1),
        lambda v: [2, v["b"], v["c"], v["lim"]],
        lambda x, v: x * x - v["b"] * x + v["c"] == 0 and x <= v["lim"]),
    "chokey-factor-count": Lock(
        (0, 20, 1),
        lambda v: [v["N"]],
        lambda x, v: x == factor_count(v["N"])),
    "chokey-prime-volumes": Lock(
        (0, 30, 1),
        lambda v: [1, v["V"]],
        lambda x, v: x == prime_count(v["V"])),
    "chokey-hcf-bundles": Lock(
        (0, 120, 1),
        lambda v: [v["a"], v["b"]],
        lambda x, v: x == gcd(v["a"], v["b"])),
    "kiln-sensor-limit": Lock(
        keypad(2),
        lambda v: [v["k"], v["L"]],
        lambda x, v: x < v["L"] and x % v["k"] == 0 and x + v["k"] >= v["L"]),
    "kiln-fan-restart": Lock(
        (0, 120, 1),
        lambda v: [v["a"], v["b"]],
        lambda x, v: (x > 0 and x % v["a"] == 0 and x % v["b"] == 0
            and not any(y % v["a"] == 0 and y % v["b"] == 0 for y in range(1, int(x))))),
    "kiln-cancel-check": Lock(
        (0, 60, 1),
        lambda v: [v["a"], v["b"], v["c"]],
        lambda x, v: x == v["a"] + v["b"] // v["c"]),
    "admin-passcode-product-rule": Lock(
        keypad(3),
        lambda v: [v["k"], v["L"]],
        lambda x, v: x == passcodes(v["k"], v["L"])),
    "vote-log-overwrite": Lock(
        (1, 20, 1),
        lambda v: [v["r"]],
        lambda x, v: (1 - Fraction(v["r"], 100)) ** x < Fraction(v["f"])
            <= (1 - Fraction(v["r"], 100)) ** (x - 1)),
    "leak-audit-conditional": Lock(
        keypad(2),
        lambda v: [v["N"], v["V"], v["S"], v["neither"]],
        lambda x, v: x * v["S"] == 100 * (v["V"] + v["S"] - (v["N"] - v["neither"]))),
    "dewey-sort-arm": Lock(
        (1, 8, 1),
        lambda v: [float(f"{v['shelf']}.{d}") for d in v["parts"]],
        lambda x, v: x == 1 + sorted(Fraction(int(d), 10 ** len(d)) for d in v["parts"]).index(
            Fraction(int(v["book"].split(".")[1]), 10 ** len(v["book"].split(".")[1])))),
    "deflector-straight-line": Lock(
        (0, 180, 1),
        lambda v: [v["x"]],
        lambda a, v: a + v["x"] == 180),
    "fines-pence-to-pounds": Lock(
        keypad(4),
        lambda v: [v["p"], v["d"], v["n"]],
        lambda x, v: x * 100 == v["p"] * v["d"] * v["n"]),
}

TWO_INSTRUMENTS = {
    "rugby-scoreboard-bases": check_rugby_bases,
    "cookie-price-simultaneous": check_cookie_simultaneous,
}

NO_CHECK = "no shared check for this lock"


def covered(lock):
    return lock in LOCKS or lock in TWO_INSTRUMENTS


def check(lock, var):
    """The first test this lock's set fails, or None if it passes every one."""
    if lock in TWO_INSTRUMENTS:
        return TWO_INSTRUMENTS[lock](var)
    if lock in LOCKS:
        return check_set(var, *LOCKS[lock])
    return NO_CHECK
