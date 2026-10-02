#!/usr/bin/env python3
"""Check that an escape-room lock has EXACTLY ONE answer.

A lock with two answers is not a lock. This is the check that Gemini's puzzle
bank needed and did not get - three of its twenty concepts were unbuildable for
this reason, and two more had answers that failed their own stated constraint.

Run it before building any puzzle into a room. Add a function per lock.
"""
from itertools import product
from math import tan, radians, atan, degrees


def report(name, solutions, expected=None):
    n = len(solutions)
    verdict = "OK" if n == 1 else ("NO SOLUTION" if n == 0 else "%d SOLUTIONS" % n)
    print("%-34s %-14s %s" % (name, verdict, solutions[:6]))
    if expected is not None and solutions and solutions[0] != expected:
        print("%-34s  ^ expected %s" % ("", expected))


# --- Gemini bank -------------------------------------------------------------
report("vending (as written)",
       [(x, y) for y in range(8) for x in [(37 - 5 * y) // 2]
        if (37 - 5 * y) % 2 == 0 and x >= 0 and (x + y) % 2 == 1])

report("vending (repaired: fewest coins)",
       sorted([(x, y) for y in range(8) for x in [(37 - 5 * y) // 2]
               if (37 - 5 * y) % 2 == 0 and x >= 0 and (x + y) % 2 == 1],
              key=lambda t: sum(t))[:1])

report("lever (as written)",
       [(round(a, 1), round(b, 1))
        for a in [i / 10 for i in range(1, 21)]
        for b in [i / 10 for i in range(1, 21)]
        if abs(30 * a + 40 * b - 120) < 1e-9])

report("lever (repaired: 30N pinned at 2.0m)",
       [round(d, 1) for d in [i / 10 for i in range(1, 21)]
        if abs(40 * d - (120 - 60)) < 1e-9])

report("fuseboard",
       [(s, b) for s in range(60) for b in range(60)
        if s + 3 * b == 48 and 2 * s + b == 46])

report("channel congruences",
       [n for n in range(50, 151) if n % 4 == 3 and n % 5 == 2 and n % 7 == 4])

report("prime hash 2500-2600",
       [2 ** a * 3 ** b * 7 ** c
        for a, b, c in product(range(13), range(9), range(5))
        if 2500 < 2 ** a * 3 ** b * 7 ** c < 2600
        and (2 ** a * 3 ** b * 7 ** c) % 9 == 0])

report("drone drop-zone (max 2x+3y)",
       [max(((2 * x + 3 * y), (x, y)) for x in range(9) for y in range(1, 9)
            if y <= 2 * x + 2 and x + y <= 8)])

# --- the-perfect-prank -------------------------------------------------------
report("prank: drawer",
       [n for n in range(100, 1000)
        if len(set(str(n))) == 3
        and sum(int(d) for d in str(n)) == 9
        and n % 2 == 0
        and int(str(n)[0]) == int(str(n)[2]) * 2
        and n < 500])

report("prank: chair notch",
       [n for n in (28, 35, 42, 49, 56) if 52 * 0.75 <= n < 60 * 0.75])

report("prank: clock angle 105deg",
       [m for m in range(60) if abs(min(abs(m * 6 - (60 + m * 0.5)),
                                        360 - abs(m * 6 - (60 + m * 0.5))) - 105) < 1e-9])

# --- bounds and rounding traps ----------------------------------------------
print()
print("bounds: 145 x 2.45 = %s  (bank says 355.225)" % (145 * 2.45))
d = 3.2 / tan(radians(28))
print("ramp:   exact %.4f m; at 6.0 m the incline is %.2f deg, limit is 28"
      % (d, degrees(atan(3.2 / 6.0))))
print("ramp:   at 6.1 m the incline is %.2f deg - inside the limit"
      % degrees(atan(3.2 / 6.1)))
