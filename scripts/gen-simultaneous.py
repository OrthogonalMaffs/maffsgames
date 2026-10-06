#!/usr/bin/env python3
"""Simultaneous Solver, Foundation Stages 1-4: generate the problem banks (offline, deterministic).

    python scripts/gen-simultaneous.py            # print the bank and its statistics
    python scripts/gen-simultaneous.py --write    # paste it into the page between the GENERATED BANK markers
    python scripts/gen-simultaneous.py --check    # exit 1 if the page's bank is not what this script generates

Every problem is a pair of linear equations ax + by = c with one integer solution. The game teaches
elimination one step at a time (scale, add or subtract, solve, substitute), so the bank is built for the
method, not just the answer:

  - solutions are whole numbers from -10 to 10 (never 0, so the substitution step always has work in it);
  - every coefficient is 1 to 12 in size, the x coefficient of equation (1) is positive, and no equation
    has a common factor (2x + 4y = 6 is not exam-like);
  - the neatest multipliers (the LCM pair) for the letter being eliminated are at most 5. Stage 4 lets the
    student choose the letter, so there both letters' neatest pairs are at most 5;
  - constants are at most 60 in size; after the neatest scaling no constant passes 150 and the combined
    equation's coefficient is at most 30 in size;
  - Stage 1 is filled to quotas of multiplier shapes: x1 and x1, x1 and xk, and both scaled;
  - no letter is eliminated in more than 28 of a stage's 48 problems (Stages 1-3), and at most 6 problems
    in Stages 2-4 need no scaling at all (x1 and x1);
  - Stages 2-4 are filled to quotas of negative work, worked out on the neatest scaling with equation (1)
    first: subtracting a negative, adding two negatives, a negative result (a quarter each), and a
    quarter with no negative anywhere. scripts/verify-simultaneous-solver.py holds every rule.

No rejection sampling (CLAUDE.md): the candidate pool is enumerated, shuffled with a fixed seed by a bounded
Fisher-Yates, and sliced into quotas. The output is the same on every run.
"""
import argparse
import json
import math
import os
import random
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "games", "simultaneous-solver", "index.html")
START, END = "/* GENERATED BANK START */", "/* GENERATED BANK END */"
SEED = 20261006
PER_STAGE = 48
SOL_RANGE = [v for v in range(-10, 11) if v != 0]
COEF_MAX, CONST_MAX, SCALED_MAX, COMBINED_MAX, MULT_MAX = 12, 60, 150, 30, 5

# Stage 1 quotas, by the shape of the neatest pair.
STAGE1_QUOTA = [("equal", 4), ("one", 18), ("both", 26)]
# Stages 2-4 quotas, by the problem's primary kind of negative work (see kind()).
NEG_QUOTA = [("add_negs", 12), ("sub_neg", 12), ("neg_result", 12), ("positive", 12)]
LETTER_CAP, UNSCALED_CAP = 28, 6


def neat(p, q):
    """The neatest (LCM) multipliers that make coefficients p and q equal in size."""
    l = abs(p) * abs(q) // math.gcd(abs(p), abs(q))
    return [l // abs(p), l // abs(q)]


def solve(e):
    """(x, y) as exact fractions, or None when the pair has no single solution."""
    from fractions import Fraction
    (a1, b1, c1), (a2, b2, c2) = e
    det = a1 * b2 - a2 * b1
    if det == 0:
        return None
    return Fraction(c1 * b2 - c2 * b1, det), Fraction(a1 * c2 - a2 * c1, det)


def eliminate(e, letter, m):
    """Scale by m and combine (equation (1) first). Returns (op, scaled, combined) where combined is
    [K, C]: K times the other letter equals C."""
    i = 0 if letter == "x" else 1
    s = [[m[0] * v for v in e[0]], [m[1] * v for v in e[1]]]
    op = "sub" if (s[0][i] > 0) == (s[1][i] > 0) else "add"
    sign = -1 if op == "sub" else 1
    comb = [s[0][k] + sign * s[1][k] for k in range(3)]
    return op, s, [comb[1 - i], comb[2]]


def letter_cost(e, letter):
    """How heavy eliminating this letter is: the LCM it scales to, then how many equations need scaling."""
    i = 0 if letter == "x" else 1
    m = neat(e[0][i], e[1][i])
    return (abs(e[0][i]) * m[0], sum(1 for v in m if v != 1))


def neater(e):
    cx, cy = letter_cost(e, "x"), letter_cost(e, "y")
    return "x" if cx < cy else "y" if cy < cx else "either"


def kind(e, letter):
    """The problem's primary kind of negative work, on the neatest scaling with equation (1) first."""
    i = 0 if letter == "x" else 1
    op, s, comb = eliminate(e, letter, neat(e[0][i], e[1][i]))
    cols = list(zip(s[0], s[1]))
    if op == "add" and any(u < 0 and v < 0 for u, v in cols):
        return "add_negs"
    if op == "sub" and any(v < 0 for u, v in cols):
        return "sub_neg"
    if comb[0] < 0 or comb[1] < 0:
        return "neg_result"
    if any(v < 0 for row in e for v in row):
        return "neg_other"
    return "positive"


def stage1_kind(e, letter):
    i = 0 if letter == "x" else 1
    m = neat(e[0][i], e[1][i])
    return "equal" if m == [1, 1] else "one" if 1 in m else "both"


def fits(e, letter):
    """The scaling and combining limits for eliminating this letter."""
    i = 0 if letter == "x" else 1
    m = neat(e[0][i], e[1][i])
    if max(m) > MULT_MAX:
        return False
    op, s, comb = eliminate(e, letter, m)
    if any(abs(row[2]) > SCALED_MAX for row in s):
        return False
    return comb[0] != 0 and abs(comb[0]) <= COMBINED_MAX


def shuffled(rng, items):
    items = list(items)
    for k in range(len(items) - 1, 0, -1):     # bounded Fisher-Yates
        j = rng.randrange(k + 1)
        items[k], items[j] = items[j], items[k]
    return items


def candidates(rng, stage):
    """Every coefficient pair, shuffled; each given the first solution (from a shuffled list, at most
    len(SOL) tries, bounded) that keeps the constants small and the equations without a common factor."""
    coefs = [c for c in range(-COEF_MAX, COEF_MAX + 1) if c]
    pairs = [(a1, b1, a2, b2) for a1 in range(1, COEF_MAX + 1) for b1 in coefs for a2 in coefs for b2 in coefs
             if a1 * b2 - a2 * b1 != 0]
    sols = shuffled(rng, [(x, y) for x in SOL_RANGE for y in SOL_RANGE])
    out = []
    for n, (a1, b1, a2, b2) in enumerate(shuffled(rng, pairs)):
        # Exam-like: equation (2) usually leads with a positive x too (a quarter of the pool may not).
        if a2 < 0 and n % 4:
            continue
        if stage == 4:
            if not (fits_pair(a1, b1, a2, b2, "x") and fits_pair(a1, b1, a2, b2, "y")):
                continue
            letter = None
        else:
            letter = "x" if n % 2 else "y"
            if not fits_pair(a1, b1, a2, b2, letter):
                continue
        start = n % len(sols)
        for t in range(len(sols)):
            x, y = sols[(start + t) % len(sols)]
            c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
            if abs(c1) > CONST_MAX or abs(c2) > CONST_MAX:
                continue
            if math.gcd(math.gcd(a1, b1), c1) != 1 or math.gcd(math.gcd(a2, b2), c2) != 1:
                continue
            e = [[a1, b1, c1], [a2, b2, c2]]
            if all(fits(e, L) for L in ([letter] if letter else ["x", "y"])):
                out.append((e, x, y, letter))
                break
        if len(out) >= 8000:
            break
    return out


def fits_pair(a1, b1, a2, b2, letter):
    p, q = (a1, a2) if letter == "x" else (b1, b2)
    return max(neat(p, q)) <= MULT_MAX


def key(e):
    return tuple(sorted(tuple(r) for r in e))


def build_stage(stage):
    rng = random.Random(SEED + stage)
    pool = candidates(rng, stage)
    quota = STAGE1_QUOTA if stage == 1 else NEG_QUOTA
    buckets = {name: [] for name, _ in quota}
    seen = set()
    for e, x, y, letter in pool:
        k = key(e)
        if k in seen:
            continue
        seen.add(k)
        if stage == 1:
            b = stage1_kind(e, letter)
        elif stage == 4:
            n = neater(e)
            b = kind(e, n if n != "either" else "x")
        else:
            b = kind(e, letter)
        buckets.setdefault(b, []).append((e, x, y, letter))
    # Fill each quota in pool order, within two caps: no letter more than LETTER_CAP times (stages 1-3),
    # and at most UNSCALED_CAP problems needing no scaling at all (x1 and x1) in stages 2-4.
    chosen, letters, unscaled = [], {"x": 0, "y": 0}, 0
    for name, want in quota:
        got = 0
        for e, x, y, letter in buckets[name]:
            if got == want:
                break
            if letter and letters[letter] >= LETTER_CAP:
                continue
            m = neat(e[0][0], e[1][0]) if (letter or neater(e)) == "x" else neat(e[0][1], e[1][1])
            if stage > 1 and m == [1, 1]:
                if unscaled >= UNSCALED_CAP:
                    continue
                unscaled += 1
            if letter:
                letters[letter] += 1
            chosen.append((e, x, y, letter))
            got += 1
        if got < want:
            raise SystemExit("gen-simultaneous: stage %d has only %d '%s' problems within the caps (needs %d)"
                             % (stage, got, name, want))
    chosen = shuffled(rng, chosen)
    out = []
    for n, (e, x, y, letter) in enumerate(chosen, 1):
        item = {"id": "s%d_%02d" % (stage, n), "e": e, "x": x, "y": y}
        if stage == 4:
            item["mx"] = neat(e[0][0], e[1][0])
            item["my"] = neat(e[0][1], e[1][1])
            item["neat"] = neater(e)
        else:
            i = 0 if letter == "x" else 1
            item["elim"] = letter
            item["m"] = neat(e[0][i], e[1][i])
        out.append(item)
    return out


def build():
    return {"stage%d" % s: build_stage(s) for s in (1, 2, 3, 4)}


def render(bank):
    lines = ["var BANK = {"]
    for si, (name, items) in enumerate(bank.items()):
        lines.append('  "%s": [' % name)
        for k, it in enumerate(items):
            lines.append("    " + json.dumps(it, separators=(", ", ": ")) + ("," if k < len(items) - 1 else ""))
        lines.append("  ]" + ("," if si < len(bank) - 1 else ""))
    lines.append("};")
    return "\n".join(lines)


def page_block(src):
    m = re.search(re.escape(START) + r"\n(.*?)\n" + re.escape(END), src, re.S)
    return m.group(1) if m else None


def stats(bank):
    rows = []
    for s in (1, 2, 3, 4):
        items = bank["stage%d" % s]
        if s == 1:
            c = {}
            for it in items:
                k = stage1_kind(it["e"], it["elim"])
                c[k] = c.get(k, 0) + 1
            rows.append("stage1: %d problems; neatest pair %s" % (len(items), c))
        else:
            c, neg = {}, 0
            for it in items:
                L = it.get("elim") or (it["neat"] if it["neat"] != "either" else "x")
                k = kind(it["e"], L)
                c[k] = c.get(k, 0) + 1
                neg += k != "positive"
            rows.append("stage%d: %d problems; with a negative %d/%d (%.0f%%); %s"
                        % (s, len(items), neg, len(items), 100.0 * neg / len(items), c))
    return "\n".join(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="paste the bank into the page")
    ap.add_argument("--check", action="store_true", help="fail if the page's bank differs from this output")
    args = ap.parse_args()
    bank = build()
    text = render(bank)
    if args.write or args.check:
        src = open(PAGE, encoding="utf-8").read()
        cur = page_block(src)
        if cur is None:
            raise SystemExit("gen-simultaneous: no %s ... %s block in %s" % (START, END, PAGE))
        if args.check:
            if cur != text:
                print("FAIL: the page's bank is not what scripts/gen-simultaneous.py generates; run it with --write")
                return 1
            print("ok: the page's bank matches the generator")
            return 0
        src = src.replace(START + "\n" + cur + "\n" + END, START + "\n" + text + "\n" + END)
        with open(PAGE, "w", encoding="utf-8", newline="\n") as f:
            f.write(src)
        print("wrote the bank into %s" % os.path.relpath(PAGE, ROOT))
    else:
        print(text)
    print(stats(bank), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
