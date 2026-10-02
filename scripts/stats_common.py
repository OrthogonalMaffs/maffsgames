#!/usr/bin/env python3
"""Shared statistics for the answer-key verifiers (todo §1.26, 30 Sep 2026).

Every stats verifier used to carry its own copy of the same maths: exact binomial
and Poisson, the Normal, the PMCC and its critical values, and half-up rounding.
This module is the one copy. Nothing in it comes from, or reads, any game: a
verifier that asked the game for a value would only prove the game agrees with
itself.

    Binomial(n, p)          exact, via fractions.Fraction
    Poisson(lam)            Decimal at PREC significant figures
    Z / NormalDist          statistics.NormalDist (calculator values)
    region_prob()           P(X < a), P(X > a), P(a < X < b), P(outside)
    r_two_tail_p()          P(|R| >= r) under rho = 0, from the exact null
    r_critical()            distribution of r (regularised incomplete beta)
    pmcc_from_sums()        r, b and a from n, sum x, sum y, sum x^2, sum y^2, sum xy
    pmcc(), least_squares() the same from raw (x, y) data
    rnd(), fmt(), rhu()     round half up, exactly

Run `python scripts/stats_common.py --selftest` for the unit tests against
textbook values (formula-booklet tables and worked examples); CI runs it.
"""
import math
import re
import sys
from decimal import Decimal, ROUND_HALF_UP, localcontext
from fractions import Fraction
from statistics import NormalDist

PREC = 60
Z = NormalDist()


# --------------------------------------------------------------------------
#  exact numbers and rounding
# --------------------------------------------------------------------------
def D(x):
    """Decimal from a JSON number/str without going through a binary float's repr noise."""
    return Decimal(str(x))


def F(x):
    return Fraction(str(x))


def to_dec(v):
    if isinstance(v, Fraction):
        with localcontext() as c:
            c.prec = PREC
            return Decimal(v.numerator) / Decimal(v.denominator)
    if isinstance(v, float):
        return Decimal(repr(v))
    return Decimal(v)


def as_dec(v):
    return to_dec(v) if isinstance(v, Fraction) else v


def rnd(v, dp):
    """Round half up, exactly, to dp places; returns a Decimal."""
    q = Decimal(1).scaleb(-dp)
    with localcontext() as c:
        c.prec = PREC
        return to_dec(v).quantize(q, rounding=ROUND_HALF_UP)


def fmt(v, dp):
    return format(rnd(v, dp), 'f')


def rhu(x, d):
    """round-half-up of a Decimal or float to d places, as a Decimal"""
    if not isinstance(x, Decimal):
        x = Decimal(repr(float(x)))
    return x.quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP)


def decimals(tok):
    """decimal places printed in a numeric token: '0.9772' -> 4, '45' -> 0"""
    return len(tok.split('.')[1]) if '.' in tok else 0


def half_ulp(d):
    return 0.5 * 10 ** (-d)


def within_rounding(tok, true_val):
    """A printed number is right if the true value is within half its last unit."""
    return abs(float(tok) - true_val) <= half_ulp(decimals(tok)) + 1e-12


# --------------------------------------------------------------------------
#  discrete distributions
# --------------------------------------------------------------------------
class Binomial:
    def __init__(self, n, p):
        self.n, self.p = n, F(p)
        self.pmf = [Fraction(math.comb(n, k)) * self.p ** k * (1 - self.p) ** (n - k) for k in range(n + 1)]
        self.top = n

    def le(self, k):
        return sum(self.pmf[:max(0, min(k, self.n) + 1)], Fraction(0))

    def ge(self, k):
        return sum(self.pmf[max(0, k):], Fraction(0)) if k <= self.n else Fraction(0)

    def mean(self):
        return self.n * self.p


class Poisson:
    def __init__(self, lam):
        self.lam = D(lam)
        self.top = int(self.lam + 12 * self.lam.sqrt() + 40)
        with localcontext() as c:
            c.prec = PREC
            term = (-self.lam).exp()
            self.pmf = []
            for k in range(self.top + 1):
                self.pmf.append(term)
                term = term * self.lam / (k + 1)

    def le(self, k):
        with localcontext() as c:
            c.prec = PREC
            return sum(self.pmf[:max(0, min(k, self.top) + 1)], Decimal(0))

    def ge(self, k):
        with localcontext() as c:
            c.prec = PREC
            return Decimal(1) - self.le(k - 1) if k > 0 else Decimal(1)

    def mean(self):
        return self.lam


def lower_cr(dist, alpha):
    """Largest c with P(X<=c) <= alpha, or None."""
    a, c = to_dec(alpha), None
    for k in range(0, dist.top + 1):
        if as_dec(dist.le(k)) <= a:
            c = k
        else:
            break
    return c


def upper_cr(dist, alpha):
    """Smallest c with P(X>=c) <= alpha, or None (binomial: region must be inside 0..n)."""
    a = to_dec(alpha)
    for k in range(dist.top, -1, -1):
        if as_dec(dist.ge(k)) > a:
            return k + 1 if k + 1 <= dist.top else None
    return 0


def tail_prob(dist, d, k):
    return dist.le(k) if d == 'leq' else dist.ge(k)


# --------------------------------------------------------------------------
#  the Normal
# --------------------------------------------------------------------------
def region_prob(dist, region):
    """region: ('lt', a) | ('gt', a) | ('between', a, b) | ('outside', a, b)"""
    kind = region[0]
    if kind == 'lt':
        return dist.cdf(region[1])
    if kind == 'gt':
        return 1 - dist.cdf(region[1])
    if kind == 'between':
        return dist.cdf(region[2]) - dist.cdf(region[1])
    if kind == 'outside':
        return 1 - (dist.cdf(region[2]) - dist.cdf(region[1]))
    raise ValueError(region)


# --------------------------------------------------------------------------
#  null distribution of Pearson's r  (exact, via the regularised incomplete beta)
# --------------------------------------------------------------------------
def _betacf(a, b, x):
    tiny, eps = 1e-300, 3e-16
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / (tiny if abs(d) < tiny else d)
    h = d
    for m in range(1, 501):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d
        d = 1 / (tiny if abs(d) < tiny else d)
        c = 1 + aa / c
        c = tiny if abs(c) < tiny else c
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d
        d = 1 / (tiny if abs(d) < tiny else d)
        c = 1 + aa / c
        c = tiny if abs(c) < tiny else c
        de = d * c
        h *= de
        if abs(de - 1) < eps:
            break
    return h


def betainc(a, b, x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(lbeta + a * math.log(x) + b * math.log(1 - x))
    if x < (a + 1) / (a + b + 2):
        return front * _betacf(a, b, x) / a
    return 1 - front * _betacf(b, a, 1 - x) / b


def r_two_tail_p(n, r0):
    """P(|R| >= r0) for n pairs under rho = 0. (Cross-checked against mpmath quadrature
    of the density of r on every correlation item, 30 Sep 2026: agreement to 8 s.f.)"""
    return betainc((n - 2) / 2, 0.5, 1 - r0 * r0)


def r_critical(n, alpha_two):
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if r_two_tail_p(n, mid) > alpha_two:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def r_cv_txt(n, alpha_two):
    """The critical value as the formula booklet prints it: 4 d.p."""
    return fmt(Decimal(repr(r_critical(n, alpha_two))), 4)


# --------------------------------------------------------------------------
#  PMCC and least-squares regression
# --------------------------------------------------------------------------
class SumsError(ValueError):
    """Summary statistics that no real data set can have."""


def pmcc_from_sums(n, sx, sy, sx2, sy2, sxy):
    """{'Sxx','Syy','Sxy','b','a' (Fractions), 'r' (float)} of y = a + bx from the six sums.

    Raises SumsError if Sxx or Syy is not positive, or if Sxy^2 > Sxx*Syy (|r| > 1):
    Cauchy-Schwarz says no set of real numbers has those sums."""
    n, sx, sy, sx2, sy2, sxy = (F(v) for v in (n, sx, sy, sx2, sy2, sxy))
    Sxx, Syy, Sxy = sx2 - sx * sx / n, sy2 - sy * sy / n, sxy - sx * sy / n
    if Sxx <= 0 or Syy <= 0:
        raise SumsError('Sxx = %s, Syy = %s: a spread cannot be zero or negative' % (Sxx, Syy))
    if Sxy * Sxy > Sxx * Syy:
        raise SumsError('Sxy^2 > Sxx*Syy, so |r| = %.4f > 1' % (abs(Sxy) / math.sqrt(Sxx * Syy)))
    b = Sxy / Sxx
    return {'Sxx': Sxx, 'Syy': Syy, 'Sxy': Sxy, 'b': b, 'a': sy / n - b * sx / n,
            'r': float(Sxy) / math.sqrt(Sxx * Syy)}


def sums(xs, ys):
    xs, ys = [F(x) for x in xs], [F(y) for y in ys]
    return (len(xs), sum(xs), sum(ys), sum(x * x for x in xs), sum(y * y for y in ys),
            sum(x * y for x, y in zip(xs, ys)))


def pmcc(xs, ys):
    return pmcc_from_sums(*sums(xs, ys))['r']


def least_squares(xs, ys):
    """(a, b) of the least-squares line y = a + bx, as Fractions."""
    s = pmcc_from_sums(*sums(xs, ys))
    return s['a'], s['b']


# --------------------------------------------------------------------------
#  worked-step arithmetic: every "a op b = c" chain in a line of working
# --------------------------------------------------------------------------
# A chain "x = (195 − 180) ÷ 10 = 15 ÷ 10 = 1.5" is split at '='; each pair of
# neighbouring pieces that are both pure arithmetic must agree. A bare printed number
# is allowed its own rounding (half its last unit); two expressions must agree exactly.
# '≈' ends a chain (an approximation is not an equality), and so does any piece with
# a letter in it (P(Z < 1.2), 'SD', 'c'). A tuple '(a, b)' compares element by element.
_ARITH_OK = re.compile(r'^[\d\s.+\-*/()^]+%?$')


def _arith_clean(s):
    s = (s.replace('−', '-').replace('–', '-').replace('×', '*').replace('÷', '/')
         .replace('£', '').replace(' ', ' ').replace(' ', ' ').replace('²', '^2'))
    s = re.sub(r'(?<=\d),(?=\d{3}\b)', '', s)                     # 5,000 -> 5000
    s = re.sub(r'√\s*(\d+(?:\.\d+)?)', r'(\1)^(1/2)', s)      # √100 -> (100)^(1/2)
    s = re.sub(r'(?<=[\d)])\s*\(', '*(', s)                         # 4.5(12) -> 4.5*(12)
    return s


def _arith_readings(piece):
    """Every value a piece can mean: a percentage '10.56%' is 0.1056, but in '... x 100 = 200%'
    the other side is already in percent, so both readings are offered."""
    v = _arith_value(piece)
    if v is None:
        return []
    out = [v]
    if piece.strip().rstrip('.').strip().endswith('%'):
        out.append((v[0] * 100, None if v[1] is None else v[1] - 2))
    return out


def _arith_value(piece):
    """(Fraction or float, printed decimals or None for an expression), or None"""
    p = piece.strip().rstrip('.').strip()
    if not p or not _ARITH_OK.match(p) or not re.search(r'\d', p):
        return None
    pct = p.endswith('%')
    body = p[:-1].strip() if pct else p
    lit = re.fullmatch(r'-?\d+(?:\.\d+)?', body)
    try:
        if lit:
            v = F(body)
        elif '^' in body:
            v = eval(body.replace('^', '**'), {'__builtins__': {}}, {})    # noqa: S307 (digits and operators only)
        else:
            v = eval(re.sub(r'(\d+(?:\.\d+)?)', r'F("\1")', body), {'__builtins__': {}}, {'F': F})  # noqa: S307
    except (SyntaxError, ZeroDivisionError, TypeError, ValueError):
        return None
    if pct:
        v = v / 100
    return v, ((decimals(body) + (2 if pct else 0)) if lit else None)


def arith_problems(text):
    """[(left, right, why)] for every neighbouring pair in an '=' chain that disagrees."""
    out = []
    for sentence in re.split(r'\.(?=\s|$)|\n|;|→', _arith_clean(text)):
        for chain in sentence.split('≈'):
            pieces = chain.split('=')
            for a, b in zip(pieces, pieces[1:]):
                ta, tb = re.fullmatch(r'\s*\((.*,.*)\)\s*\.?\s*', a), re.fullmatch(r'\s*\((.*,.*)\)\s*\.?\s*', b)
                pairs = (list(zip(ta.group(1).split(','), tb.group(1).split(','))) if ta and tb
                         else [(a, b)])
                for x, y in pairs:
                    rx, ry = _arith_readings(x), _arith_readings(y)
                    if not rx or not ry:
                        continue

                    def agree(vx, vy):
                        dps = [d for d in (vx[1], vy[1]) if d is not None]
                        tol = half_ulp(min(dps)) if dps else 1e-9
                        return abs(float(vx[0]) - float(vy[0])) <= tol + 1e-12
                    if not any(agree(vx, vy) for vx in rx for vy in ry):
                        out.append((x.strip(), y.strip(), '%s vs %s' % (float(rx[0][0]), float(ry[0][0]))))
    return out


# --------------------------------------------------------------------------
#  unit tests against textbook values
# --------------------------------------------------------------------------
def selftest():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    fails = []

    def eq(name, got, want):
        ok = got == want
        print('%-4s %-58s got %-12s want %s' % ('OK' if ok else 'FAIL', name, got, want))
        if not ok:
            fails.append(name)

    def raises(name, fn):
        try:
            fn()
        except SumsError:
            print('OK   %-58s raises SumsError' % name)
            return
        print('FAIL %-58s did not raise' % name)
        fails.append(name)

    # Normal: the booklet's Phi table and percentage points, calculator values
    eq('Phi(1.2)', fmt(Z.cdf(1.2), 4), '0.8849')
    eq('Phi(1.96)', fmt(Z.cdf(1.96), 4), '0.9750')
    eq('Phi(-1.25)', fmt(Z.cdf(-1.25), 4), '0.1056')
    eq('Phi(-2.25)', fmt(Z.cdf(-2.25), 4), '0.0122')
    eq('P(-1 < Z < 1)', fmt(region_prob(Z, ('between', -1, 1)), 4), '0.6827')
    eq('invPhi(0.975)', fmt(Z.inv_cdf(0.975), 4), '1.9600')
    eq('invPhi(0.95)', fmt(Z.inv_cdf(0.95), 4), '1.6449')
    eq('invPhi(0.995)', fmt(Z.inv_cdf(0.995), 4), '2.5758')
    eq('N(50, 8^2): P(X > 60.2528) = 0.1', fmt(1 - NormalDist(50, 8).cdf(50 + 1.2816 * 8), 3), '0.100')
    # Binomial and Poisson: cumulative tables
    eq('B(20, 0.5): P(X >= 15)', fmt(Binomial(20, 0.5).ge(15), 4), '0.0207')
    eq('B(10, 0.3): P(X <= 2)', fmt(Binomial(10, 0.3).le(2), 4), '0.3828')
    eq('B(60, 1/6) mean', Binomial(60, Fraction(1, 6)).mean(), 10)
    eq('B(20, 0.3): lower 5% critical value', lower_cr(Binomial(20, 0.3), Fraction(5, 100)), 2)
    eq('B(20, 0.3): upper 5% critical value', upper_cr(Binomial(20, 0.3), Fraction(5, 100)), 10)
    eq('Po(3): P(X <= 2)', fmt(Poisson(3).le(2), 4), '0.4232')
    eq('Po(2.5): P(X >= 5)', fmt(Poisson(2.5).ge(5), 4), '0.1088')
    # PMCC critical values, 5% two-tail (formula booklet Table 8)
    for n, want in ((10, '0.6319'), (12, '0.5760'), (15, '0.5140'), (18, '0.4683'),
                    (20, '0.4438'), (25, '0.3961'), (30, '0.3610')):
        eq('PMCC critical value n = %d, 5%% two-tail' % n, r_cv_txt(n, 0.05), want)
    eq('PMCC critical value n = 10, 1% two-tail', r_cv_txt(10, 0.01), '0.7646')
    # PMCC and regression, a worked example: x = 1..5, y = 2, 4, 5, 4, 5
    xs, ys = [1, 2, 3, 4, 5], [2, 4, 5, 4, 5]
    eq('r of (1..5; 2,4,5,4,5)', fmt(pmcc(xs, ys), 4), '0.7746')
    eq('least squares a, b', least_squares(xs, ys), (Fraction(11, 5), Fraction(3, 5)))
    eq('from sums = from data', pmcc_from_sums(*sums(xs, ys))['r'], pmcc(xs, ys))
    raises('sums with |r| > 1 (n=10, 850, 142, 74750, 2156, 12840)',
           lambda: pmcc_from_sums(10, 850, 142, 74750, 2156, 12840))
    raises('sums with Sxx = 0', lambda: pmcc_from_sums(3, 6, 6, 12, 14, 12))
    # rounding
    eq('rnd(2.675, 2) half up, exactly', fmt(Fraction(2675, 1000), 2), '2.68')
    eq('rhu(0.045500, 3)', str(rhu(Decimal('0.0455'), 3)), '0.046')
    eq('within_rounding("0.0455", 0.04550026)', within_rounding('0.0455', 0.04550026), True)
    eq('within_rounding("0.0456", 0.04550026)', within_rounding('0.0456', 0.04550026), False)
    # worked-step arithmetic
    eq('arith: z = (195 − 180) ÷ 10 = 15 ÷ 10 = 1.5', arith_problems('z = (195 − 180) ÷ 10 = 15 ÷ 10 = 1.5.'), [])
    eq('arith: SE = 20 ÷ √100 = 2', arith_problems('SE = 20 ÷ √100 = 2.'), [])
    eq('arith: 1.96 × 3 = 5.88; 0.1056 = 10.56%', arith_problems('1.96 × 3 = 5.88. 0.1056 = 10.56%.'), [])
    eq('arith: CI (135 − 3.92, 135 + 3.92) = (131.08, 138.92)',
       arith_problems('CI: (135 − 3.92, 135 + 3.92) = (131.08, 138.92).'), [])
    eq('arith: z = 2.47 ÷ 1.5 = 1.647 ≈ 1.645 (≈ not checked)', arith_problems('z = 2.47 ÷ 1.5 = 1.647 ≈ 1.645.'), [])
    eq('arith: 85 = 4.5(12) + c -> c = 85 − 54 = 31', arith_problems('85 = 4.5(12) + c → c = 85 − 54 = 31.'), [])
    eq('arith catches: 1000 × 0.0122 = 122', len(arith_problems('1000 × 0.0122 = 122')), 1)
    eq('arith catches: (60 − 50) ÷ 5 = 2.5', len(arith_problems('(60 − 50) ÷ 5 = 2.5')), 1)
    eq('arith: 0.0122 × 5,000 = 61', arith_problems('0.0122 × 5,000 = 61'), [])
    eq('arith: (160000 ÷ 80000) × 100 = 200%', arith_problems('(160000 ÷ 80000) × 100 = 200%'), [])
    eq('arith catches: 0.25 = 2.5%', len(arith_problems('0.25 = 2.5%')), 1)
    print('\n%s: %d unit test(s) failed' % ('FAILED' if fails else 'ALL PASS', len(fails)))
    return not fails


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(0 if selftest() else 1)
    print(__doc__)
