"""Generate and verify the escape rooms' variant libraries.

Every lock carries a library of number sets so a room can be replayed without
being the same room. A variant is only allowed out of here if it passes the
same tests the lock bank is held to:

  * exactly one setting on the instrument's own grid solves it
    (docs/escape-puzzle-bank.md: "a lock with two answers is not a lock")
  * the answer is actually settable — on the step, inside the range
  * the misconception is settable too, and is not the answer
    (an unreachable misconception means that response never fires)
  * no number printed in the clue equals the answer — the trap the checker
    in check-lock-bank.py explicitly cannot see

Those tests, and each lock's instrument, clue figures and solver, live in
scripts/escape_set_checks.py, which check-escape-rooms.py also runs on every
set in CI (contract ESCAPE-SET-CHECKS, 11 Oct 2026). A new lock adds its entry
there first. What stays here is the search, and the spread rule in keep().

The first variant of every lock reproduces the audited bank exactly. Later
variants are found by search under the same rules.

Writes escape-rooms/variants.json and fills each room.js, in this checkout.
Run scripts/check-escape-rooms.py after.
"""
import json, math, pathlib, random
from fractions import Fraction
from math import gcd, factorial

from escape_set_checks import COMPASS, LOCKS, check, is_prime, factor_count, pence, prime_count

ROOMS = pathlib.Path(__file__).resolve().parent.parent / "escape-rooms"
OUT = ROOMS / "variants.json"
WANT = 10         # variants per lock, where the maths allows that many
rejected = []


# ---------------------------------------------------------------- helpers
def shuffled(cands):
    """Bank variant first, the rest drawn from across the whole space.
    Seeded, so the library is the same every time this is run."""
    head, tail = cands[:1], cands[1:]
    random.Random(20260831).shuffle(tail)
    return head + tail


def keep(store, lock, var, minsep=0.0):
    """Admit a variant only if it survives every test (escape_set_checks.check)
    and is not too close to one already kept."""
    reason = check(lock, var)
    if reason:
        rejected.append((lock, var, reason)); return
    lo, hi, step = LOCKS[lock].ins
    a = var["answer"]
    sep = minsep or (hi - lo) * 0.05
    # the tolerance matters: 1.2 - 1.0 is 0.19999999999999996 in binary, so a
    # bare `< sep` throws away every answer that is exactly one gap apart
    if any(abs(x["answer"] - a) < sep - 1e-9 for x in store):
        return          # too close to one already kept: a library wants spread
    store.append(var)


V = {}

# ---------------------------------------------------- C1 sector area (dial 10-360/10)
# answer = 360K/r^2. Misconception: the pi is dropped on one side only, so the
# fraction is computed as K over the decimal area and lands one notch out.
store = []
for r, K in shuffled([(12, 48)] + [(r, K) for r in range(5, 26) for K in range(5, 301)]):
    if r * r == 0 or (360 * K) % (r * r):
        continue
    ans = 360 * K // (r * r)
    miss = int(round(360 * K / (math.pi * r * r) / 10.0)) * 10
    if not (20 <= ans <= 350):
        continue
    keep(store, "sprinkler-sector-area",
         {"r": r, "K": K, "answer": ans, "miss": miss})
    if len(store) >= WANT:
        break
V["sprinkler-sector-area"] = store

# ---------------------------------------------------- C2 inverse proportion (dial 0-100)
store = []
cands = shuffled([(20, 60, 25)] + [(v1, p1, v2) for v1 in range(10, 61, 2)
                          for p1 in range(30, 101, 5)
                          for v2 in range(12, 81, 2) if v2 > v1])
for v1, p1, v2 in cands:
    if (p1 * v1) % v2 or (p1 * v2) % v1:
        continue
    ans, miss = p1 * v1 // v2, p1 * v2 // v1
    if not (10 <= ans <= 90 and 0 <= miss <= 100):
        continue
    keep(store, "dodgeball-pressure-boyle",
         {"V1": v1, "P1": p1, "V2": v2, "answer": ans, "miss": miss})
    if len(store) >= WANT:
        break
V["dodgeball-pressure-boyle"] = store

# ---------------------------------------------------- C3 linear sequence (dial 0-99)
# Three non-consecutive days. Misconception: treat the last written day as
# yesterday and add the gap between the first two entries (reproduces 88).
store = []
cands = shuffled([(3, 7, 12, 15, 5, 23)] + [(d1, d2, d3, dT, s, c1)
                                   for s in range(3, 8)
                                   for d1 in range(2, 5)
                                   for d2 in range(d1 + 3, d1 + 6)
                                   for d3 in range(d2 + 4, d2 + 7)
                                   for dT in range(d3 + 2, d3 + 5)
                                   for c1 in range(11, 30)])
for d1, d2, d3, dT, s, c1 in cands:
    c2, c3 = c1 + s * (d2 - d1), c1 + s * (d3 - d1)
    ans = c1 + s * (dT - d1)
    miss = c3 + (c2 - c1)
    if not (ans <= 99 and miss <= 99):
        continue
    keep(store, "locker-nth-term",
         {"d1": d1, "c1": c1, "d2": d2, "c2": c2, "d3": d3, "c3": c3,
          "dT": dT, "step": s, "answer": ans, "miss": miss})
    if len(store) >= WANT:
        break
V["locker-nth-term"] = store

# ---------------------------------------------------- D1 reverse percentage (keypad 4)
store = []
cands = shuffled([(2160, 20)] + [(t, p) for p in (10, 15, 20, 25, 40, 50)
                        for t in range(1100, 9000, 2)])
for total, pct in cands:
    if (total * 100) % (100 + pct):
        continue
    ans = total * 100 // (100 + pct)
    miss = total - total * pct // 100 if (total * pct) % 100 == 0 else None
    if miss is None or not (1000 <= ans <= 9999):
        continue
    keep(store, "finance-reverse-percentage",
         {"total": total, "pct": pct, "answer": ans, "miss": miss})
    if len(store) >= WANT:
        break
V["finance-reverse-percentage"] = store

# ---------------------------------------------------- D2 compound growth (slider 1-20)
# Misconception: read the interest as a flat amount each year.
store = []
cands = shuffled([(1000, 10, 5)] + [(d, r, y) for d in (500, 600, 800, 1000, 1200, 1500, 2000, 2500)
                           for r in (5, 10, 15, 20, 25) for y in range(2, 13)])
for dep, rate, yrs in cands:
    bal = Fraction(dep) * Fraction(100 + rate, 100) ** yrs
    if (bal * 100).denominator != 1:          # must land on whole pence
        continue
    interest = bal - dep
    flat = Fraction(dep * rate, 100)
    miss = int(round(float(interest / flat)))
    if not (1 <= miss <= 20):
        continue
    keep(store, "dj-deposit-compound",
         {"dep": dep, "rate": rate,
          "bal": f"{float(bal):.2f}", "answer": yrs, "miss": miss}, minsep=1)
    if len(store) >= WANT:
        break
V["dj-deposit-compound"] = store

# ---------------------------------------------------- D3 Venn overlap (dial 0-100)
store = []
cands = shuffled([(80, 48, 37, 12)] + [(t, a, b, n) for t in range(60, 101, 5)
                              for a in range(30, 90, 3)
                              for b in range(25, 90, 3)
                              for n in range(5, 25, 2)])
for total, A, B, neither in cands:
    both = A + B - (total - neither)
    if not (2 <= both <= min(A, B) - 2) or A > total or B > total:
        continue
    keep(store, "wifi-venn-router",
         {"total": total, "A": A, "B": B, "neither": neither,
          "answer": both, "miss": 0})
    if len(store) >= WANT:
        break
V["wifi-venn-router"] = store

# ---------------------------------------------------- E1 circumference/RPM (slider 0-500)
store = []
cands = shuffled([(20, 120)] + [(d, d * k) for d in range(10, 41, 2) for k in range(3, 9)])
for d, K in cands:
    if K % d:
        continue
    per_s = K // d
    ans = per_s * 60
    if not (60 <= ans <= 500):
        continue
    keep(store, "hamster-wheel-rpm",
         {"d": d, "K": K, "answer": ans, "miss": per_s})
    if len(store) >= WANT:
        break
V["hamster-wheel-rpm"] = store

# ---------------------------------------------------- E2 lower bounds (slider 0-1000)
# CHANGED 2026-09-08, Jon's catch. This lock used to ask for the GREATEST volume
# the hopper could hold, which is X * (D + 0.5) -- and that is not a volume the
# hopper can have. A depth recorded as D cm to the nearest centimetre lies in
# [D - 0.5, D + 0.5), so D + 0.5 is the supremum and is NOT attained: a depth of
# exactly 15.5 rounds to 16, not 15, so it could never have been written down as
# 15 in the first place. The bank's own AHA line admitted it -- "even though
# nothing measures exactly that" -- and papered over it.
#
# The LOWER bound does not have this problem. D - 0.5 rounds up to D, so it is a
# depth the hopper can genuinely have, and the smallest volume is a real minimum
# that is actually reached. The lock now asks for the smallest volume.
#
# X stays even so X * (D - 0.5) lands on the slider's whole-number grid.
store = []
cands = shuffled([(40, 15)] + [(x, dpt) for x in range(10, 81, 2) for dpt in range(8, 25)])
for X, D in cands:
    if (X * (2 * D - 1)) % 2:
        continue
    ans = X * (2 * D - 1) // 2
    miss = X * D
    if not (100 <= ans <= 1000):
        continue
    keep(store, "hamster-feeder-bounds",
         {"X": X, "D": D, "answer": ans, "miss": miss})
    if len(store) >= WANT:
        break
V["hamster-feeder-bounds"] = store

# ---------------------------------------------------- E3 gradient (slider 0-20 by 0.1)
store = []
cands = shuffled([(4, 21, 16, 39)] + [(t1, T1, t1 + run, T1 + rise)
                             for t1 in range(2, 8) for T1 in range(15, 26)
                             for run in (8, 10, 12, 14, 15, 16, 20)
                             for rise in range(6, 21)])
for t1, T1, t2, T2 in cands:
    rise, run = T2 - T1, t2 - t1
    g = Fraction(rise, run)
    if (g * 10).denominator != 1:
        continue
    ans = float(g)
    if not (0.5 <= ans <= 5) or rise > 20:
        continue
    keep(store, "heat-lamp-gradient",
         {"t1": t1, "T1": T1, "t2": t2, "T2": T2,
          "rise": rise, "run": run,
          "answer": round(ans, 1), "miss": float(rise)}, minsep=0.2)
    if len(store) >= WANT:
        break
V["heat-lamp-gradient"] = store

# ---------------------------------------------------- F1 area scale factor (dial 1-100)
store = []
cands = shuffled([(15, 90, 5)] + [(L1, A1, L1 // k) for k in (2, 3, 4, 5)
                         for L1 in range(8, 41, 2) if L1 % k == 0
                         for A1 in range(16, 101, 2)])
for L1, A1, L2 in cands:
    k = L1 // L2
    if A1 % (k * k) or A1 % k:
        continue
    ans, miss = A1 // (k * k), A1 // k
    if not (2 <= ans <= 60) or miss > 100:
        continue
    keep(store, "elbow-patch-scale",
         {"L1": L1, "A1": A1, "L2": L2, "k": k, "answer": ans, "miss": miss}, minsep=4)
    if len(store) >= WANT:
        break
V["elbow-patch-scale"] = store

# ---------------------------------------------------- F2 combined rates (dial 1-60)
store = []
cands = shuffled([(20, 30)] + [(a, b) for a in range(6, 60, 2) for b in range(8, 90, 2) if b > a])
for a, b in cands:
    if (a * b) % (a + b) or (a + b) % 2:
        continue
    ans, miss = a * b // (a + b), (a + b) // 2
    if not (3 <= ans <= 55) or miss > 60:
        continue
    keep(store, "sprinkler-flow-rates",
         {"a": a, "b": b, "answer": ans, "miss": miss}, minsep=2)
    if len(store) >= WANT:
        break
V["sprinkler-flow-rates"] = store

# ---------------------------------------------------- F3 index laws (two dials 0-100)
# 2^H x 4^A = 2^N with A = H + diff, so H + 2A = N.
# Misconception: read 4^A as 2^A, take A = N and H = N - diff.
store = []
for N, diff in [(17, 4)] + [(n, d) for n in range(11, 40) for d in range(2, 9)]:
    if (N - 2 * diff) % 3:
        continue
    H = (N - 2 * diff) // 3
    A = H + diff
    if not (1 <= H <= 20 and A <= 40):
        continue
    var = {"N": N, "diff": diff, "H": H, "A": A,
           "missH": N - diff, "missA": N,
           "answer": [H, A], "miss": [N - diff, N]}
    reason = check("rugby-scoreboard-bases", var)      # two dials: escape_set_checks.check_rugby_bases
    if reason:
        rejected.append(("rugby-scoreboard-bases", var, reason)); continue
    if any(x["answer"] == [H, A] for x in store):
        continue
    store.append(var)
    if len(store) >= WANT:
        break
V["rugby-scoreboard-bases"] = store

# ---------------------------------------------------- G1 arrangements (dial 1-100)
# n! / repeats. n stays at 4 because the misconception (n!) has to be settable
# on a 1-100 dial, and 5! is 120.
store = []
for keys, reps in [("A, A, B, C", [2, 1, 1]), ("A, A, B, B", [2, 2]), ("A, A, A, B", [3, 1])]:
    n = sum(reps)
    denom = 1
    for r in reps:
        denom *= factorial(r)
    ans = factorial(n) // denom
    var = {"keys": keys, "n": n, "denom": denom, "answer": ans, "miss": factorial(n)}
    keep(store, "mechanical-keyboard-perms", var, minsep=1)
V["mechanical-keyboard-perms"] = store

# ---------------------------------------------------- G2 quadratic vertex (slider 0-5 by 0.1)
# h = -a t^2 + b t + c, peak at t = b/2a. Misconception: set the time, not the height.
store = []
cands = shuffled([(2, Fraction(24, 5), Fraction(3, 25))] + [
    (a, Fraction(2 * a * ts, 10), Fraction(c10, 100))
    for a in (2, 3, 4)
    for ts in range(8, 17)
    for c10 in range(4, 45, 2)])
for a, b, c in cands:
    t_star = b / (2 * a)
    h_star = c + b * b / (4 * a)
    if (t_star * 10).denominator != 1 or (h_star * 10).denominator != 1:
        continue
    t_f, h_f = float(t_star), float(h_star)
    if not (0.8 <= t_f <= 2.0 and 1.5 <= h_f <= 4.5):
        continue
    var = {"a": a, "b": f"{float(b):g}", "c": f"{float(c):g}",
           "t": round(t_f, 1), "answer": round(h_f, 1), "miss": round(t_f, 1)}
    keep(store, "vault-trajectory-vertex", var)
    if len(store) >= WANT:
        break
V["vault-trajectory-vertex"] = store

# ---------------------------------------------------- G3 HCF tiling (slider 0.1-5 by 0.1)
# Misconception: a common factor that tiles, but not the largest one.
store = []
cands = shuffled([(48, 72)] + [(w, l) for w in range(20, 121, 2) for l in range(24, 145, 2) if l > w])
for w10, l10 in cands:
    g = gcd(w10, l10)
    if g % 2 or not (10 <= g <= 50):
        continue
    ans, miss = g / 10, (g // 2) / 10
    if w10 // g < 2 or l10 // g < 2:
        continue
    keep(store, "mat-tiling-hcf",
         {"W": f"{w10/10:g}", "L": f"{l10/10:g}", "w10": w10, "l10": l10,
          "across": w10 // g, "along": l10 // g,
          "answer": round(ans, 1), "miss": round(miss, 1)})
    if len(store) >= WANT:
        break
V["mat-tiling-hcf"] = store

# ---------------------------------------------------- H1 LCM (slider 1-200)
store = []
cands = shuffled([(12, 15, 18)] + [(a, b, c) for a in range(4, 25) for b in range(a + 1, 31)
                          for c in range(b + 1, 37)])
for a, b, c in cands:
    l = a * b // gcd(a, b)
    l = l * c // gcd(l, c)
    if not (40 <= l <= 200):
        continue
    miss = a + b + c
    keep(store, "patrol-lcm-timer",
         {"a": a, "b": b, "c": c, "answer": l, "miss": miss}, minsep=14)
    if len(store) >= WANT:
        break
V["patrol-lcm-timer"] = store

# ---------------------------------------------------- H2 cube SA -> V (keypad 4)
store = []
for e in [15] + list(range(10, 22)):
    sa, vol, face = 6 * e * e, e ** 3, e * e
    if not (1000 <= vol <= 9999):
        continue
    keep(store, "cube-surface-volume",
         {"SA": sa, "edge": e, "face": face, "answer": vol, "miss": face})
    if len(store) >= WANT:
        break
V["cube-surface-volume"] = store

# ---------------------------------------------------- H3 inequality + prime (dial 0-50)
store = []


cands = shuffled([(20, 3, 5, 32)] + [(lo, m, k, hi) for m in (2, 3, 4)
                            for k in range(2, 12)
                            for lo in range(8, 60)
                            for hi in range(lo + 6, lo + 26)])
for lo, m, k, hi in cands:
    band = [f for f in range(0, 51) if lo < m * f - k < hi]
    primes = [f for f in band if is_prime(f)]
    if len(band) < 3 or len(band) > 5 or len(primes) != 1:
        continue
    ans, miss = primes[0], max(band)
    if miss == ans:
        continue
    keep(store, "canteen-freezer-inequality",
         {"lo": lo, "m": m, "k": k, "hi": hi,
          "band": ", ".join(str(x) for x in band),
          "low": f"{(lo+k)/m:.2f}".rstrip("0").rstrip("."),
          "high": f"{(hi+k)/m:.2f}".rstrip("0").rstrip("."),
          "answer": ans, "miss": miss})
    if len(store) >= WANT:
        break
V["canteen-freezer-inequality"] = store


# ---------------------------------------------------- I1 mean averages (slider 0-1000)
# answer = 5T minus the four already entered. Misconception: the target mean itself,
# entered as though the missing item had to be average.
store = []
cands = [(520, 480, 550, 600, 450)]
for T in range(350, 601, 25):
    for ans in range(60, 941, 20):
        S = 5 * T - ans
        if S < 900:
            continue
        q = (S // 40) * 10
        for offs in ((30, -30, 60), (-40, 20, 90), (0, 50, -50), (70, -20, 10)):
            e1, e2, e3 = q + offs[0], q + offs[1], q + offs[2]
            e4 = S - e1 - e2 - e3
            if len({e1, e2, e3, e4}) != 4 or e4 % 10:
                continue
            if not all(180 <= e <= 900 for e in (e1, e2, e3, e4)):
                continue
            if ans > min(e1, e2, e3, e4) - 40:
                continue          # the dummy item has to read as the healthy one
            cands.append((e1, e2, e3, e4, T))
for e1, e2, e3, e4, T in shuffled(cands):
    keep(store, "canteen-mean-calories",
         {"e1": e1, "e2": e2, "e3": e3, "e4": e4, "T": T,
          "answer": 5 * T - (e1 + e2 + e3 + e4), "miss": T}, minsep=40)
    if len(store) >= WANT:
        break
V["canteen-mean-calories"] = store

# ---------------------------------------------------- I2 simultaneous equations (two tags 0-10)
# a1 C + b1 P = t1 and a2 C + b2 P = t2, eliminated by scaling the second by mult.
# Misconception: the right pair of numbers on the wrong two tags.
store = []
cands = [(3, 2, 1, 4, 2, 3)]
for C in range(1, 10):
    for P in range(1, 10):
        if P <= C:
            continue          # the pizza is the dearer item, on any receipt
        for a1 in range(2, 5):
            for b1 in range(1, 5):
                for a2 in range(1, 4):
                    for b2 in range(1, 6):
                        if a1 == b1 or a2 == b2:
                            continue      # the swap has to fail on the first line too
                        if b1 == b2:
                            continue      # else one item cancels by plain subtraction and
                                          # the hint ladder is teaching the long way round
                        if b2 > 4 or a1 * b2 == a2 * b1 or a1 % a2 or a1 == a2:
                            continue
                        cands.append((a1, b1, a2, b2, C, P))
for a1, b1, a2, b2, C, P in shuffled(cands):
    mult = a1 // a2
    t1, t2 = a1 * C + b1 * P, a2 * C + b2 * P
    var = {"a1": a1, "b1": b1, "t1": t1, "a2": a2, "b2": b2, "t2": t2,
           "C": C, "P": P, "mult": mult,
           "answer": [C, P], "miss": [P, C]}
    reason = check("cookie-price-simultaneous", var)   # two tags: escape_set_checks.check_cookie_simultaneous
    if reason:
        rejected.append(("cookie-price-simultaneous", var, reason)); continue
    if any(abs(C - x["answer"][0]) + abs(P - x["answer"][1]) < 2 for x in store):
        continue
    store.append(var)
    if len(store) >= WANT:
        break
V["cookie-price-simultaneous"] = store

# ---------------------------------------------------- I3 fractions of an amount (dial 0-200)
# The fraction names what stays; the dial wants what goes.
# Misconception: setting the chute to the amount that was meant to remain.
store = []
cands = shuffled([(180, 2, 9)] + [(N, n, d) for N in range(40, 201, 10)
                                  for d in range(3, 13) for n in range(1, d)])
for N, n, d in cands:
    if N % d or gcd(n, d) != 1 or 2 * n >= d:
        continue
    kept = N * n // d
    keep(store, "kale-fraction-drain",
         {"N": N, "n": n, "d": d, "kept": kept, "answer": N - kept, "miss": kept})
    if len(store) >= WANT:
        break
V["kale-fraction-drain"] = store

# ---------------------------------------------------- J1 lower bounds (dial 0-20 by 0.25)
# Both measurements are to the nearest metre, so both bounds end in .5 and every
# product lands on a quarter. Misconception: multiplying the stated figures.
store = []
cands = shuffled([(6, 3)] + [(L, W) for L in range(3, 13) for W in range(2, 13) if L >= W])
for L, W in cands:
    if L * W > 20:
        continue
    keep(store, "visitor-space-bounds",
         {"L": L, "W": W, "answer": (L - 0.5) * (W - 0.5), "miss": float(L * W)})
    if len(store) >= WANT:
        break
V["visitor-space-bounds"] = store

# ---------------------------------------------------- J1 (2026-10) lower bound of one width (slider 2.00-3.00 by 0.01)
# Replaces visitor-space-bounds in the rewritten car-trap room (contract CAR-TRAP-BUILD; bank batch 8);
# the library above is kept as history. The width is stated to the nearest 0.1 m (written "ten
# centimetres" in the prose, so the 10 is no clue figure). The answer is the smallest setting on the
# grid that rounds, half up, to W; misconception: W itself, the stated width taken as exact.
store = []


for W in shuffled([2.4, 2.2, 2.3, 2.5, 2.6, 2.7, 2.8, 2.9]):
    keep(store, "head-bay-lower-bound",
         {"W": W, "answer": round(W - 0.05, 2), "miss": W})
    if len(store) >= WANT:
        break
V["head-bay-lower-bound"] = store

# ---------------------------------------------------- J2 arc length (dial 0-180 by 5)
# arc = (th/360) x 2 pi r, quoted as k pi so the pi cancels. Misconception: the
# radius used where the circumference needs the diameter, which doubles the angle.
store = []
cands = shuffled([(3, 45)] + [(r, th) for r in range(2, 10) for th in range(10, 91, 5)])
for r, th in cands:
    if 360 % th or (th * r * 100) % 180:
        continue
    k = th * r / 180.0
    if not (0.25 <= k <= 5):
        continue
    keep(store, "boom-gate-sector",
         {"r": r, "th": th, "k": f"{k:g}", "answer": th, "miss": 2 * th}, minsep=5)
    if len(store) >= WANT:
        break
V["boom-gate-sector"] = store

# ---------------------------------------------------- J3 quadratic with a constraint (dial 0-15)
# Two roots, one of them above the alarm limit. Misconception: the other root,
# taken without reading the limit - the same shape as canteen-freezer-inequality.
store = []
cands = shuffled([(5, 7, 6)] + [(p, q, lim) for p in range(1, 13)
                                for q in range(p + 2, 16) for lim in range(p + 1, q)])
for p, q, lim in cands:
    b, c = p + q, p * q
    if c > 120 or b > 24 or p < 3 or q - p > 6:
        continue
    keep(store, "ev-charger-quadratic",
         {"p": p, "q": q, "b": b, "c": c, "lim": lim, "answer": p, "miss": q})
    if len(store) >= WANT:
        break
V["ev-charger-quadratic"] = store

# ---------------------------------------------------- K1 factor count (dial 0-20)
# Misconception: one factor pair missed. N is never square, so its factors pair
# off exactly and the count is always even - under 100 that allows only 6, 8, 10
# and 12, and the spread rule caps the library at four. Accepted.
store = []
for N in shuffled([24] + [n for n in range(20, 100) if n != 24]):
    if is_prime(N) or math.isqrt(N) ** 2 == N or factor_count(N) < 6:
        continue
    keep(store, "chokey-factor-count",
         {"N": N, "answer": factor_count(N), "miss": factor_count(N) - 2})
    if len(store) >= WANT:
        break
V["chokey-factor-count"] = store

# ---------------------------------------------------- K2 primes up to V (dial 0-30)
# Misconception: 1 counted as prime. Answers sit one apart across the pool, so
# this lock sets its own gap of 1 rather than the dial's default 1.5.
store = []
for Vol in shuffled([30, 20, 25, 35, 40, 45, 50, 55, 60]):
    keep(store, "chokey-prime-volumes",
         {"V": Vol, "answer": prime_count(Vol), "miss": prime_count(Vol) + 1}, minsep=1)
    if len(store) >= WANT:
        break
V["chokey-prime-volumes"] = store

# ---------------------------------------------------- K3 HCF bundles (slider 0-120)
# Misconception: the LCM given for the HCF, so the LCM has to fit on the slider.
# HCFs of 5-15 are too close for the default gap of 6 on this travel; gap of 1.
store = []
cands = shuffled([(18, 45)] + [(a, b) for b in range(2, 61) for a in range(1, b)
                               if (a, b) != (18, 45)])
for a, b in cands:
    g = gcd(a, b)
    lcm = a * b // g
    if not (5 <= g <= 15) or g in (a, b) or lcm > 120:
        continue
    keep(store, "chokey-hcf-bundles",
         {"a": a, "b": b, "answer": g, "miss": lcm}, minsep=1)
    if len(store) >= WANT:
        break
V["chokey-hcf-bundles"] = store

# ---------------------------------------------------- L1 largest multiple under a limit (keypad 0-99)
# Misconception: the first multiple past the limit, so that has to fit on two digits,
# and at most 96 so it never sits at the very top of the keypad.
store = []
cands = shuffled([(9, 85)] + [(k, L) for k in range(6, 14) for L in range(30, 100)
                              if L % k and (k, L) != (9, 85)])
for k, L in cands:
    ans = (L // k) * k
    miss = ans + k
    if ans < 20 or miss > 96:
        continue
    keep(store, "kiln-sensor-limit",
         {"k": k, "L": L, "answer": ans, "miss": miss})
    if len(store) >= WANT:
        break
V["kiln-sensor-limit"] = store

# ---------------------------------------------------- L2 LCM of two cycles (dial 0-120)
# Misconception: the two cycles multiplied, so the product has to fit on the dial.
# A shared factor keeps the LCM off the product; neither dividing the other keeps
# it off the longer cycle.
store = []
cands = shuffled([(6, 14)] + [(a, b) for a in range(4, 21) for b in range(a + 1, 21)
                              if (a, b) != (6, 14)])
for a, b in cands:
    if gcd(a, b) == 1 or b % a == 0 or a * b > 120:
        continue
    keep(store, "kiln-fan-restart",
         {"a": a, "b": b, "answer": a * b // gcd(a, b), "miss": a * b})
    if len(store) >= WANT:
        break
V["kiln-fan-restart"] = store

# ---------------------------------------------------- L3 order of operations (slider 0-60)
# a + b / c. Misconception: left to right, (a + b) / c, so a is a multiple of c too.
# Non-calculator: b is capped at 60 so the division stays mental arithmetic.
# b / c is at least 2, or the division does no work, and a != b, which reads
# like a typo rather than a calculation.
store = []
cands = shuffled([(21, 45, 3)] + [(a, b, c) for c in range(2, 10)
                                  for a in range(c, 56, c) for b in range(c, 61, c)
                                  if (a, b, c) != (21, 45, 3)])
for a, b, c in cands:
    ans, miss = a + b // c, (a + b) // c
    if not (20 <= ans <= 55) or miss == ans or b // c < 2 or a == b:
        continue
    keep(store, "kiln-cancel-check",
         {"a": a, "b": b, "c": c, "answer": ans, "miss": miss})
    if len(store) >= WANT:
        break
V["kiln-cancel-check"] = store

# ---------------------------------------------------- M1 (2026-10) product rule, no repeats (keypad, maxDigits 3)
# The Rightful King (contract RIGHTFUL-KING-BUILD; bank batch 9). The passcode is L different keys from a
# pad of k, so the count is k(k-1)...(L factors). Misconception: k^L, the same key allowed again. Jon's
# ruling 2: k = 5 to 9 with L = 3 on a maxDigits keypad (k = 5 gives 60, which maxDigits makes settable);
# variant 0 is k = 7 (210, miss 343), because 120 is printed in the audit's variant-0 clue. The solver
# counts the passcodes outright rather than restating the formula.
store = []
for k, L in shuffled([(7, 3), (5, 3), (6, 3), (8, 3), (9, 3)]):
    keep(store, "admin-passcode-product-rule",
         {"k": k, "L": L, "answer": math.perm(k, L), "miss": k ** L})
    if len(store) >= WANT:
        break
V["admin-passcode-product-rule"] = store

# ---------------------------------------------------- M2 (2026-10) decay by iteration (dial 1-20)
# r% of the records still left are replaced each minute, so (1 - r/100)^n survive after n minutes; the
# answer is the first whole minute with fewer than f left, in exact fractions. Misconception: r% of the
# ORIGINAL each minute, so fewer than f are left after (1 - f) x 100 / r minutes, rounded up. Rejected:
# answer = miss; an exact hit (1 - r/100)^n = f; answers of 2 or less; and (Jon's ruling 3) any set where
# r divides (1 - f) x 100, because there a strict linear reader lands one minute later, which for 25% and
# a half is the right answer: the lock would mark the wrong method right.
# The library is the draft's ten sets, in its order (Jon's ruling 3: "the draft's ten-set library"); each
# still has to pass every rule below and keep(), so an edit here cannot slip a bad set in.
store = []
HALF, QUARTER = Fraction(1, 2), Fraction(1, 4)
cands = [(20, HALF), (8, QUARTER), (29, QUARTER), (20, QUARTER), (7, HALF), (9, HALF), (40, QUARTER),
         (11, QUARTER), (12, QUARTER), (9, QUARTER)]
for r, f in cands:
    m = 1 - Fraction(r, 100)
    if any(m ** n == f for n in range(1, 41)):
        continue
    ans = next(n for n in range(1, 200) if m ** n < f)
    if (1 - f) * 100 % r == 0:
        continue
    miss = math.ceil((1 - f) * 100 / r)
    if ans <= 2 or ans == miss:
        continue
    keep(store, "vote-log-overwrite",
         {"r": r, "f": str(f), "answer": ans, "miss": miss})
    if len(store) >= WANT:
        break
V["vote-log-overwrite"] = store

# ---------------------------------------------------- M3 (2026-10) Venn diagram, conditional probability (keypad, digits 2)
# N voters, V for him, S opened the ballot page, `neither` did neither. Inside the circles: N - neither;
# both = V + S - (N - neither). Answer: both as a percentage of S. Misconception: both out of all N (the
# wrong denominator). Jon's ruling 4, the draft's story rules: V/N 30-60%, S/N 20-60%, P(V | S) at least
# twenty points above P(V | not S), the four clue figures all different, S != 100 (dividing by 100 does
# nothing). Variant 0 is 120, 50, 40, 60.
# The library is the draft's seven sets, in its order (N in tens from 100 to 240; V, S and neither in
# fives); each still has to pass every rule below and keep().
store = []
cands = [(120, 50, 40, 60), (200, 100, 50, 90), (240, 80, 120, 100), (230, 130, 125, 90), (100, 40, 50, 45),
         (120, 45, 50, 55), (150, 45, 75, 60)]
for N, Vv, S, nb in cands:
    both = Vv + S - (N - nb)
    if not (0 < both < min(Vv, S)) or S == 100 or len({N, Vv, S, nb}) < 4:
        continue
    if (100 * both) % S or (100 * both) % N:
        continue
    ans, miss = 100 * both // S, 100 * both // N
    if not (10 <= ans <= 99 and 10 <= miss <= 99):
        continue
    if not (Fraction(3, 10) <= Fraction(Vv, N) <= Fraction(3, 5) and Fraction(1, 5) <= Fraction(S, N) <= Fraction(3, 5)):
        continue
    if Fraction(both, S) - Fraction(Vv - both, N - S) < Fraction(1, 5):
        continue
    keep(store, "leak-audit-conditional",
         {"N": N, "V": Vv, "S": S, "neither": nb, "answer": ans, "miss": miss})
    if len(store) >= WANT:
        break
V["leak-audit-conditional"] = store

# ---------------------------------------------------- N1 (2026-10) ordering decimals (dial 1-8)
# The Library Jam (contract LIBRARY-JAM-BUILD; bank batch 10). Five or six books on one Dewey shelf, in the
# order they were dropped in; the arm holds one and wants its slot, smallest first. Misconception: the digits
# after the point read as a whole number (a longer decimal taken as bigger). The library is the draft's eight
# shelves, in its order; each still has to pass the draft's rules below and keep(). Spread is off for this
# lock (minsep 1e-9): the slots repeat across shelves, one variant per shelf (the draft's rule).
store = []
DEWEY = [("520", "stars and planets", ["35", "5", "15", "62", "4"], "4"),
         ("567", "dinosaurs", ["6", "4", "07", "13", "86", "65"], "6"),
         ("641", "cooking", ["3", "7", "8", "18", "97"], "7"),
         ("551", "volcanoes and weather", ["9", "3", "06", "77", "76"], "9"),
         ("942", "British history", ["4", "1", "8", "9", "63", "77"], "9"),
         ("796", "sport", ["8", "2", "37", "61", "39"], "8"),
         ("598", "birds", ["1", "6", "8", "63", "58", "59"], "6"),
         ("821", "poetry", ["5", "7", "2", "8", "16", "53"], "5")]
for shelf, subject, parts, book in DEWEY:
    vals = [Fraction(int(d), 10 ** len(d)) for d in parts]
    reads = [int(d) for d in parts]                      # the misconception reads .07 as 7, .4 as 4
    lens = [len(d) for d in parts]
    if not (5 <= len(parts) <= 6 and lens.count(1) >= 2 and lens.count(2) >= 2):
        continue
    if any(d.endswith("0") for d in parts) or len(set(reads)) < len(reads) or len(book) != 1:
        continue
    if vals in (sorted(vals), sorted(vals, reverse=True)):  # the drop order is never already sorted
        continue
    b = parts.index(book)
    ans = sorted(vals).index(vals[b]) + 1
    miss = sorted(reads).index(reads[b]) + 1
    if ans == 1 or ans == miss:
        continue
    keep(store, "dewey-sort-arm",
         {"shelf": shelf, "subject": subject, "parts": parts, "book": f"{shelf}.{book}", "answer": ans, "miss": miss}, minsep=1e-9)
V["dewey-sort-arm"] = store

# ---------------------------------------------------- N2 (2026-10) angles on a straight line (dial 0-180)
# answer = 180 - x; misconception: 90 - x, the angles making a right angle. x from 20 to 70, never a multiple
# of 5. The library is the draft's eight angles, in its order, with the five-degree spread (Jon's ruling 4).
store = []
for x in [37, 46, 63, 68, 24, 56, 32, 51]:
    if not (20 <= x <= 70) or x % 5 == 0:
        continue
    keep(store, "deflector-straight-line", {"x": x, "answer": 180 - x, "miss": 90 - x}, minsep=5)
V["deflector-straight-line"] = store

# ---------------------------------------------------- N3 (2026-10) pence to pounds (keypad, maxDigits 4)
# p pence a day for d days, for each of n books: p x d x n pence, entered in pounds. Misconception: the
# pence total entered as pounds (5400 for 54), which a maxDigits 4 keypad can set (Jon's ruling 2). p in
# {5, 10, 15, 20} (non-calculator), d 5 to 20, n 20 to 32 (a class), p, d and n all different; the answer
# a whole number of pounds, 10 to 99. The library is the draft's ten sets, in its order (variant 0 is Jon's
# example: 15p, 12 days, 30 books, 54). minsep 1: the answers only have to differ, as the draft rules; the
# default spread is 5% of the keypad's 0-9999.
store = []
for p, d, n in [(15, 12, 30), (20, 15, 26), (20, 15, 32), (20, 10, 24), (10, 20, 28), (5, 8, 30), (10, 14, 20),
                (15, 14, 20), (10, 20, 31), (5, 15, 32)]:
    total = p * d * n
    if p not in (5, 10, 15, 20) or not (5 <= d <= 20 and 20 <= n <= 32) or len({p, d, n}) < 3:
        continue
    if total % 100 or not (10 <= total // 100 <= 99):
        continue
    keep(store, "fines-pence-to-pounds", {"p": p, "d": d, "n": n, "answer": total // 100, "miss": total}, minsep=1)   # answers distinct (the draft's rule)
V["fines-pence-to-pounds"] = store

# ---------------------------------------------------- N4 (2026-10) probability with modifiers (keypad, 3 digits)
# Roll for Initiative, the gate (contract DND-ROOM-BUILD; bank batch 11). Climb: DC dcc, Strength bonus str, and a
# drizzle penalty wet taken off the climb only. Persuade: DC dcp, Charisma bonus cha. A check is a twenty-sided die
# plus the bonus, meet or beat the DC, so a path needing n or more succeeds on 21 - n faces of 20. answer = the
# better path's chance, a multiple of 5; miss = the climb's chance with the drizzle forgotten. The draft's rules
# (Jon, 15 Oct 2026): DCs 10-16, bonuses 1-4, penalty 1-3; every required roll between 2 and 20, the forgotten-
# penalty roll included; the two chances differ; forgetting the drizzle makes the WORSE path look better, which
# with a climb-only penalty means persuasion is the better path in every set; and Mrs Rogers's approved line
# ("the lower number isn't the better bet") is true, so the climb has the lower DC. The library is the draft's
# nine sets, in its order (variant 0 is Jon's: DC 12 and 14, +2 and +3, drizzle -2). Nine is every distinct
# answer the rules allow; spread is off (minsep 1e-9) because the answers are distinct by construction.
store = []
for dcc, st, wet, dcp, cha in [(12, 2, 2, 14, 3), (11, 1, 3, 13, 1), (11, 2, 2, 13, 3), (13, 1, 2, 14, 1),
                               (13, 1, 3, 16, 2), (14, 1, 3, 16, 1), (11, 3, 2, 12, 3), (10, 3, 2, 11, 3),
                               (10, 4, 2, 11, 4)]:
    need_c, need_p, need_dry = dcc - st + wet, dcp - cha, dcc - st
    if not (10 <= dcc <= 16 and 10 <= dcp <= 16 and 1 <= st <= 4 and 1 <= cha <= 4 and 1 <= wet <= 3):
        continue
    if not all(2 <= n <= 20 for n in (need_c, need_p, need_dry)):
        continue
    pc, pp, p0 = (21 - need_c) * 5, (21 - need_p) * 5, (21 - need_dry) * 5
    if not (pc < pp < p0) or not dcc < dcp:
        continue
    keep(store, "gate-modifiers-probability",
         {"dcc": dcc, "str": st, "wet": wet, "dcp": dcp, "cha": cha, "pc": pc, "pp": pp,
          "answer": pp, "miss": p0}, minsep=1e-9)
V["gate-modifiers-probability"] = store

# ---------------------------------------------------- N5 (2026-10) scale drawings (keypad, 4 digits)
# Roll for Initiative, Strictmane's plans. A corridor of L cm on a 1 : S plan is L x S cm = L x S / 100 m; the
# club's square is fixed at 2 m (it is the same square lock 3 uses), so answer = L x S / 200 squares.
# miss = L x S / 2, the centimetres taken straight into squares (100 times the answer, so a four-digit keypad).
# The draft's rules: S in 100, 200, 250, 500; L a whole 2-9 cm; answer a whole number 4-30 and never L (which
# excludes every 1 : 200 plan, where 1 cm is exactly one square). The library is the draft's seven sets.
store = []
for S, L in [(500, 4), (100, 8), (250, 4), (250, 8), (500, 2), (500, 6), (500, 8)]:
    if S not in (100, 200, 250, 500) or not 2 <= L <= 9 or (L * S) % 200:
        continue
    ans = L * S // 200
    if not 4 <= ans <= 30 or ans == L:
        continue
    keep(store, "fortress-plan-scale", {"S": S, "L": L, "sq": 2, "answer": ans, "miss": L * S // 2}, minsep=1e-9)
V["fortress-plan-scale"] = store

# ---------------------------------------------------- N6 (2026-10) area of a circle (keypad, 3 digits)
# Roll for Initiative, the fireball. A blast of radius r (a whole even number of metres, 4-12, so whole squares at
# 2 m) covers pi x r squared, to the nearest square metre. The rule (Jon, 15 Oct 2026): the whole number must be the
# SAME whether pi or 3.14 is used, and a radius where the two round differently is rejected here (and by the
# solver in escape_set_checks.py). miss = the circumference 2 x pi x r, rounded. The library is the draft's five.
store = []
for r in [6, 4, 8, 10, 12]:
    a_pi, a_314 = math.floor(math.pi * r * r + 0.5), math.floor(3.14 * r * r + 0.5)
    if r % 2 or not 4 <= r <= 12 or a_pi != a_314:
        rejected.append(("fireball-circle-area", {"r": r}, "pi and 3.14 round differently")); continue
    keep(store, "fireball-circle-area", {"r": r, "answer": a_pi, "miss": math.floor(2 * math.pi * r + 0.5)}, minsep=1e-9)
V["fireball-circle-area"] = store

# ---------------------------------------------------- O1 (2026-10) coordinates, first quadrant (keypad, maxDigits 2)
# Big School Begins, the hall map (contract BSB-ROOM-BUILD; bank batch 12). The library is drawn where grid line x
# along crosses grid line y up; the code is x then y. Misconception: y then x (the map gives "up" before "along" on
# purpose, draft item 14). The draft's rules: x and y 1-9, x != y; no 5 in either and no x of 1, so no answer or
# misconception ends in 0 or 5 or falls in lock C's hours; no two sets each other's reversal. The library is the
# draft's ten sets, in its order (variant 0 is the draft's 37).
store = []
for x, y in [(3, 7), (6, 2), (8, 4), (2, 9), (4, 6), (9, 3), (7, 1), (6, 8), (2, 4), (4, 9)]:
    if not (1 <= x <= 9 and 1 <= y <= 9) or x == y or 5 in (x, y) or x == 1:
        continue
    if any((v["x"], v["y"]) == (y, x) for v in store):
        continue
    keep(store, "school-map-coordinates", {"x": x, "y": y, "answer": 10 * x + y, "miss": 10 * y + x}, minsep=1e-9)
V["school-map-coordinates"] = store

# ---------------------------------------------------- O2 (2026-10) turns in eighths (dial 0-360 by 45, sweep 360)
# Big School Begins, Bibby's directions. Face `from`, turn clockwise to `to`: answer = the clockwise steps round the
# eight-point rose x 45. Misconception: the anticlockwise turn, 360 - answer. The draft's rules: never 180 (the two
# directions agree); every point the start once. Only six answers exist, so answers repeat from different starting
# points and spread is off (minsep 1e-9; the Library Jam lock-A precedent). The library is the draft's eight.
store = []
for frm, to in [("south", "west"), ("north", "north-west"), ("north-east", "north-west"), ("east", "south-west"),
                ("south-east", "north"), ("south-west", "west"), ("west", "north"), ("north-west", "south-west")]:
    steps = (COMPASS.index(to) - COMPASS.index(frm)) % 8
    if steps in (0, 4) or any(v["from"] == frm for v in store):
        continue
    keep(store, "library-compass-turn", {"from": frm, "to": to, "steps": steps, "answer": 45 * steps,
                                         "miss": 360 - 45 * steps}, minsep=1e-9)
V["library-compass-turn"] = store

# ---------------------------------------------------- O3 (2026-10) durations across the hour (keypad, maxDigits 4)
# Big School Begins, William's lesson. A lesson starting hh:mm and lasting m minutes ends at the time typed as four
# digits, no colon. Misconception: the start read as a number plus m (1035 + 55 = 1090), a time that cannot exist.
# The rules (the draft's, with Jon's ruling 7 of 16 Oct 2026): start 10:00-11:30 in fives (before the lunch bell
# that ends the hunt); m is 45, 50 or 55; the lesson crosses exactly one hour and mm + m stays under 100, so the
# misconception always has more than fifty-nine minutes and is the answer less 40. Sets 0, 1, 4, 5 and 6 are the
# draft's; sets 2, 3, 7, 8 and 9 replace its 35-, 65- and 70-minute lessons (ruling 7), chosen for distinct start
# times and a spread of lengths. All ten answers distinct (minsep 1). Variant 0 is Jon's example, 10:35 + 55.
store = []
for hh, mm, m in [(10, 35, 55), (10, 15, 50), (10, 25, 45), (11, 25, 45), (11, 20, 45), (11, 30, 50), (11, 5, 55),
                  (10, 20, 55), (10, 30, 50), (10, 40, 55)]:
    if m not in (45, 50, 55) or mm % 5 or not (10 * 60 <= hh * 60 + mm <= 11 * 60 + 30):
        continue
    if not 60 <= mm + m < 100:
        continue
    end = hh * 60 + mm + m
    keep(store, "taster-lesson-end-time", {"hh": hh, "mm": mm, "m": m, "answer": 100 * (end // 60) + end % 60,
                                           "miss": 100 * hh + mm + m}, minsep=1)
V["taster-lesson-end-time"] = store

# ---------------------------------------------------- O4 (2026-10) change with exchanges (keypad, maxDigits 3)
# Big School Begins, the lunch card. Three prices off a card of five pounds: answer = 500 - total, in pence.
# Misconception: smaller from larger in every column of 500 - total. The draft's rules: prices in multiples of 5p;
# total 200-450 with units digit 5 and a non-zero tens digit (both columns exchange, and the misconception is never
# the answer); prices of a pound or more printed in pounds, under a pound in pence; no price, in pence, equal to its
# set's answer (the solver's clue figures carry every price in pence too, draft item 16); no item priced twice
# across the library. The library is the draft's ten trays, in its order (variant 0 is Jon's total, 365).
def price(p):
    return f"&pound;{p // 100}.{p % 100:02d}" if p >= 100 else f"{p}p"


store = []
for tray in [(("a pasta pot", 185), ("a fruit cup", 60), ("a carton of milk", 120)),
             (("a sandwich", 175), ("an apple", 40), ("a bottle of water", 30)),
             (("a slice of pizza", 210), ("a hot chocolate", 135), ("a cookie", 70)),
             (("a jacket potato", 190), ("a yoghurt", 85), ("a carton of apple juice", 50)),
             (("a bowl of soup", 155), ("a bread roll", 40), ("a rice pudding", 90)),
             (("a hot dinner", 245), ("a flapjack", 80), ("a smoothie", 110)),
             (("a wrap", 205), ("a bag of crisps", 55), ("a carton of orange juice", 115)),
             (("a cheese toastie", 150), ("a carton of squash", 70), ("a biscuit", 45)),
             (("a plate of curry and rice", 225), ("a piece of garlic bread", 60), ("a carton of fruit juice", 110)),
             (("a pasta bake", 140), ("a salad pot", 50), ("a banana", 35))]:
    total = sum(p for _, p in tray)
    if any(p % 5 for _, p in tray) or not (200 <= total <= 450 and total % 10 == 5 and total // 10 % 10):
        continue
    names = [i for i, _ in tray]
    if any(i in (v[k] for v in store for k in ("i1", "i2", "i3")) for i in names):
        continue
    var = {"card": 500, "answer": 500 - total,
           "miss": 100 * (5 - total // 100) + 10 * (total // 10 % 10) + total % 10}
    for n, (item, p) in enumerate(tray, 1):
        var[f"i{n}"], var[f"p{n}"] = item, price(p)
    assert sum(pence(var[k]) for k in ("p1", "p2", "p3")) == total
    keep(store, "lunch-card-change", var, minsep=1)
V["lunch-card-change"] = store

# ------------------------------------------------- derived tokens
# Values the prose wants to quote but that are not parameters: a squared
# radius, a reduced fraction, a prime factorisation. Deriving them here keeps
# the hint ladders honest — they cannot disagree with the answer.
def sup(n):
    # Real superscripts for every index, never a caret. fill() inserts tokens
    # as HTML, so <sup> renders; one form for all indices keeps 2<sup>4</sup>
    # and 3<sup>2</sup> matched when they sit in the same factorisation.
    return "" if n == 1 else "<sup>" + str(n) + "</sup>"


def factorise(n):
    out, d = [], 2
    while d * d <= n:
        p = 0
        while n % d == 0:
            n //= d; p += 1
        if p:
            out.append(str(d) + sup(p))
        d += 1
    if n > 1:
        out.append(str(n))
    return " &times; ".join(out)


for v in V["sprinkler-sector-area"]:
    g = gcd(v["K"], v["r"] ** 2)
    v["r2"] = v["r"] ** 2
    v["frac"] = f"{v['K']//g}/{v['r']**2//g}"
for v in V["dodgeball-pressure-boyle"]:
    v["k"] = v["V1"] * v["P1"]
for v in V["locker-nth-term"]:
    v["span"] = v["d3"] - v["d1"]
    v["rise"] = v["c3"] - v["c1"]
    v["ahead"] = v["dT"] - v["d3"]
    v["check"] = v["d2"] - v["d1"]
for v in V["finance-reverse-percentage"]:
    v["whole"] = 100 + v["pct"]
    v["onepct"] = f"{v[chr(34)+chr(34)] if False else v['total'] / (100 + v['pct']):.2f}".rstrip("0").rstrip(".")
for v in V["dj-deposit-compound"]:
    v["mult"] = f"{1 + v['rate']/100:g}"
    v["interest"] = f"{float(v['bal']) - v['dep']:.2f}"
for v in V["wifi-venn-router"]:
    v["atleast"] = v["total"] - v["neither"]
    v["sum"] = v["A"] + v["B"]
for v in V["elbow-patch-scale"]:
    v["k2"] = v["k"] ** 2
for v in V["patrol-lcm-timer"]:
    v["factors"] = (f"{v['a']} = {factorise(v['a'])}, {v['b']} = {factorise(v['b'])}, "
                    f"{v['c']} = {factorise(v['c'])}")
    v["lcmfactors"] = factorise(v["answer"])
for v in V["canteen-freezer-inequality"]:
    v["lok"] = v["lo"] + v["k"]
    v["hik"] = v["hi"] + v["k"]

for v in V["canteen-mean-calories"]:
    v["total"] = 5 * v["T"]
    v["sum4"] = v["e1"] + v["e2"] + v["e3"] + v["e4"]
for v in V["cookie-price-simultaneous"]:
    v["eC"] = v["a2"] * v["mult"]
    v["eP"] = v["b2"] * v["mult"]
    v["eT"] = v["t2"] * v["mult"]
    v["pcoef"] = v["b2"] * v["mult"] - v["b1"]
    v["ptot"] = v["t2"] * v["mult"] - v["t1"]
for v in V["kale-fraction-drain"]:
    v["one"] = v["N"] // v["d"]
for v in V["visitor-space-bounds"]:
    v["lbL"] = f"{v['L'] - 0.5:g}"
    v["lbW"] = f"{v['W'] - 0.5:g}"
for v in V["head-bay-lower-bound"]:
    v["half"] = "0.05"
    v["lb"] = f"{v['answer']:.2f}"
    v["ub"] = f"{v['W'] + 0.05:.2f}"
for v in V["hamster-feeder-bounds"]:
    # the prose needs "14.5", not "15" with a ".5" glued on: for D = 15 the lower
    # bound is 14.5, so the old {{bnd.D}}.5 trick does not work downwards
    v["lb"] = f"{v['D'] - 0.5:g}"
for v in V["boom-gate-sector"]:
    v["circ"] = 2 * v["r"]
    v["frac"] = str(Fraction(v["th"], 360))
    v["kpi"] = ("" if v["k"] == "1" else v["k"]) + "&pi;"
    v["turns"] = 360 // v["th"]
# comic-caper solve lines list every factor or prime, so the lists come from here
for v in V["chokey-factor-count"]:
    v["facN"] = ", ".join(str(d) for d in range(1, v["N"] + 1) if v["N"] % d == 0)
for v in V["chokey-prime-volumes"]:
    v["primes"] = ", ".join(str(p) for p in range(2, v["V"] + 1) if is_prime(p))
for v in V["chokey-hcf-bundles"]:
    v["facA"] = ", ".join(str(d) for d in range(1, v["a"] + 1) if v["a"] % d == 0)
    v["facB"] = ", ".join(str(d) for d in range(1, v["b"] + 1) if v["b"] % d == 0)
# kiln-disaster solve lines list the multiples, so the lists come from here
for v in V["kiln-sensor-limit"]:
    v["mults"] = f"{v['answer'] - v['k']}, {v['answer']}, {v['miss']}"
for v in V["kiln-fan-restart"]:
    v["multA"] = ", ".join(str(m) for m in range(v["a"], v["answer"] + 1, v["a"]))
    v["multB"] = ", ".join(str(m) for m in range(v["b"], v["answer"] + 1, v["b"]))
for v in V["kiln-cancel-check"]:
    v["quot"] = v["b"] // v["c"]
# rightful-king: the passcode's product, the overwrite's powers, the audit's counts
for v in V["admin-passcode-product-rule"]:
    v["prod"] = " &times; ".join(str(v["k"] - i) for i in range(v["L"]))
for v in V["vote-log-overwrite"]:
    f, m = Fraction(v["f"]), 1 - Fraction(v["r"], 100)
    v["part"] = {"1/2": "half", "1/4": "a quarter"}[v["f"]]
    v["fdec"] = {"1/2": "0.5", "1/4": "0.25"}[v["f"]]
    v["keep"] = 100 - v["r"]
    v["mult"] = f"{float(m):g}"
    v["prev"] = v["answer"] - 1
    v["prevval"] = f"{float(m ** v['prev']):.3f}"
    v["ansval"] = f"{float(m ** v['answer']):.3f}"
    # the rounded figures must say what the exact ones do: not yet below f, then below it
    assert Fraction(v["prevval"]) >= f > Fraction(v["ansval"]), v
for v in V["leak-audit-conditional"]:
    v["inside"] = v["N"] - v["neither"]
    v["both"] = v["V"] + v["S"] - v["inside"]
    p = Fraction(100 * (v["V"] - v["both"]), v["N"] - v["S"])
    v["notS"] = f"{p}%" if p.denominator == 1 else f"about {round(p)}%"
# library-jam: the trolley as dropped and as shelved, the straight line's constants, the fines' working
for v in V["dewey-sort-arm"]:
    v["list"] = ", ".join(f"{v['shelf']}.{d}" for d in v["parts"])
    v["sorted"] = ", ".join(f"{v['shelf']}.{d}" for d in sorted(v["parts"], key=lambda d: Fraction(int(d), 10 ** len(d))))
for v in V["deflector-straight-line"]:
    v["half"], v["quarter"] = 180, 90
for v in V["fines-pence-to-pounds"]:
    v["each"] = v["p"] * v["d"]
    v["hundred"] = 100
# roll-for-initiative: the die's faces, the rolls each path needs and the faces that win, the square size and the
# centimetres in a metre (constant in every set), the circle's radius in squares and its exact area
for v in V["gate-modifiers-probability"]:
    v["die"] = 20
    v["needC"] = v["dcc"] - v["str"] + v["wet"]
    v["needP"] = v["dcp"] - v["cha"]
    v["chC"] = 21 - v["needC"]
    v["chP"] = 21 - v["needP"]
for v in V["fortress-plan-scale"]:
    v["cm"] = v["L"] * v["S"]
    v["real"] = v["cm"] // 100
    v["cmperm"] = 100
for v in V["fireball-circle-area"]:
    v["rsq"] = v["r"] // 2
    v["exact"] = f"{math.pi * v['r'] ** 2:.2f}"
# big-school-begins: the card's capitals, the rose's constants, the lesson's times and jumps, the tray's total
for v in V["library-compass-turn"]:
    v["fromU"], v["toU"] = v["from"].upper(), v["to"].upper()
    v["whole"], v["eighth"] = 360, 45
for v in V["taster-lesson-end-time"]:
    end = v["hh"] * 60 + v["mm"] + v["m"]
    v["start"] = f"{v['hh']}:{v['mm']:02d}"
    v["end"] = f"{end // 60}:{end % 60:02d}"
    v["next"] = f"{v['hh'] + 1}:00"
    v["tohour"] = 60 - v["mm"]
    v["rest"] = v["mm"] + v["m"] - 60
    v["hourmins"] = 60
for v in V["lunch-card-change"]:
    v["total"] = v["card"] - v["answer"]
    v["totalP"] = price(v["total"])

# ------------------------------------------------- display tokens
# Instruments that read to one decimal place need their numbers written the
# same way in the prose as on the dial: "2.0 degrees a minute", never "2".
for lock in ("heat-lamp-gradient", "vault-trajectory-vertex", "mat-tiling-hcf"):
    for var in V[lock]:
        var["aTxt"] = f"{float(var['answer']):.1f}"
        if var.get("miss") is not None:
            var["mTxt"] = f"{float(var['miss']):.1f}"
for var in V["visitor-space-bounds"]:
    var["aTxt"] = f"{float(var['answer']):.2f}"
    var["mTxt"] = f"{float(var['miss']):.2f}"
for var in V["head-bay-lower-bound"]:
    var["aTxt"] = f"{float(var['answer']):.2f}"
    var["mTxt"] = f"{float(var['miss']):.2f}"

# ------------------------------------------------- inject into the rooms
# room.js holds `variants: [],` as a placeholder; this fills it in. Re-running
# replaces whatever is there, so the libraries always match this file.
def inject(path):
    txt = path.read_text(encoding="utf-8")
    out, i, filled = [], 0, 0
    while True:
        j = txt.find("variants: [", i)
        if j < 0:
            out.append(txt[i:]); break
        lock = None
        for lid in V:
            k = txt.rfind("id: '" + lid + "'", 0, j)
            if k >= 0 and (lock is None or k > lock[1]):
                lock = (lid, k)
        depth, end = 0, txt.index("[", j)
        for pos in range(end, len(txt)):
            if txt[pos] == "[":
                depth += 1
            elif txt[pos] == "]":
                depth -= 1
                if depth == 0:
                    end = pos; break
        raw = json.dumps(V[lock[0]], indent=2, ensure_ascii=False).rstrip()
        body = chr(10).join((" " * 6 + ln) if n else ln
                            for n, ln in enumerate(raw.splitlines()))
        out.append(txt[i:j] + "variants: " + body)
        i = end + 1
        filled += 1
    path.write_text("".join(out), encoding="utf-8", newline='')
    return filled


for rj in sorted(ROOMS.glob("*/room.js")):
    n = inject(rj)
    print(f"   injected {n} libraries into {rj.parent.name}/room.js")

# ---------------------------------------------------------------- report
OUT.write_text(json.dumps(V, indent=1), encoding="utf-8", newline='')
total = 0
for k, v in V.items():
    total += len(v)
    print(f"{len(v):>2}  {k:<32} answers: {[x['answer'] for x in v]}")
print(f"\n{total} verified variants across {len(V)} locks")
print(f"{len(rejected)} candidates rejected in the process")
