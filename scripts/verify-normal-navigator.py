#!/usr/bin/env python3
# ci-line: B2 | Normal Navigator (independent recomputation + rendered labels) |
"""Independent verification for normal-navigator (docs/todo.md §1.26).

WHY THIS EXISTS
----------------------------------------------------------------------------
normal-navigator's 47-question bank hand-types every Normal-distribution value
(probabilities to 4 d.p., z-values, inverse-normal answers, solved mu/sigma) and
nothing ever recomputed them. Its history shows the bank is not trustworthy as
authored: :222 was unanswerable and :241 keyed to the wrong integer (fixed 24 Sep
via correct_override), and three QUESTIONS[n] = ... patches overwrote good
questions until 25 Sep. Test the Claim, built the same way, had 16 of 48 items
wrong. This is the same fix pattern as scripts/verify-test-the-claim.py.

INDEPENDENCE
----------------------------------------------------------------------------
Nothing is taken from the game except the bank literal itself. The game's phi()
(an Abramowitz-Stegun approximation) is never called or copied; every value here
comes from statistics.NormalDist and decimal.Decimal. The bank is read
statically from the HTML with esprima (bank_common), including any
QUESTIONS[n] = ... patches, which are themselves a FAIL.

What each question MEANS is written down below, in SPECS, from its prose alone:
the kind of question, the region or condition it describes, and nothing numeric
the game computed. SPECS is keyed by the question's exact `ctx` string, so an
edited or added question fails until its spec is written: nothing is ever
silently unchecked. The distribution itself is parsed out of the `ctx` text
(`N(50, 8²)`, `B(100, 0.3)`), never read from the question's `mu`/`sigma` fields
-- those are drawing parameters, and are checked AGAINST the text.

WHAT IT CHECKS, PER QUESTION
----------------------------------------------------------------------------
  answer       recomputed from the prose; the effective key (correct, or
               correct_override if present) must equal it at the key's own
               displayed precision (|key - true| <= half a unit in its last place)
  conditions   inverse questions (find mu, find sigma, find both): solved from the
               stated conditions, and the KEYED answer must satisfy EVERY stated
               condition at the condition's printed precision -- not just one
  options      the key is an option exactly once; no two options are equal as
               values; no distractor equals the true answer at its own precision
  graph        the bell-info text prints mu and sigma: each must be the true value
               at its printed precision, and a solved mu must be the answer's;
               each finite shade bound must sit on the true boundary of the
               question's region to within 0.025 sd (about 1.5 px of the 440 px
               plotting width, which spans 7 sd)
  worked steps every "a = b = c" chain in steps, misconception, options and prompt
               is evaluated: an arithmetic side must round to the literal that
               follows it (so "0.8413 - 0.1587 = 0.6827" FAILS: it is 0.6826); two
               expressions must agree within the rounding of their inputs; Φ(), φ(),
               √ and P(X < a) / P(a < Z < b) are evaluated from the question's own
               distribution; every "a > b" is tested. A number that is not part of
               a checked chain must match a value this script derives for the
               question (a stated input, a z, a Φ, an inverse-Φ, the answer, ...)
  prose        no draft markers (check-banks' B6 list, plus "actually", "closest",
               "recheck" and a trailing "...")
  bank         no duplicate questions, textually or by what they ask; no
               QUESTIONS[n] = ... patch; no correct_override (todo §1.26: folded
               into `correct`, so the drift shape cannot recur here)

  rendered     the page is loaded (stub server + Playwright) and every question is
               drawn the way a student sees it: before answering, the mu/sigma
               labels under the curve must not show any number of the answer that
               is not in every option (the answer leak: "Find mu" with "mu = 58"
               printed under the curve); after answering they show the question's
               mu and sigma; and the number of shaded regions drawn is the number
               the question's region has (a two-tail region shades BOTH tails).
               The picture is checked as well as the labels: no pre-answer tick
               label may sit on a shading boundary (or inside a narrow marker
               window) whose value, as z or as x, is the answer; a question whose
               answer IS a boundary (find z, find k, the continuity-corrected z)
               shows no tick labels or tick marks at all before answering, since
               one hidden label between two visible ones is still readable; and a
               question about two distributions draws both curves, labelled, or
               none -- never just one of them

Output: `FAIL <id> <field>: stated <a>, computed <b>`. Exit 1 on any FAIL. A
fault-injection self-test runs first on every invocation and the run aborts if any
injected fault is NOT caught.

    python scripts/verify-normal-navigator.py              # verify + self-test
    python scripts/verify-normal-navigator.py --verbose    # also print each answer
    python scripts/verify-normal-navigator.py --page X.html  # verify another copy
                                                   # (the bank only: not rendered)
"""
import argparse
import copy
import importlib.util
import math
import os
import re
import sys
from decimal import Decimal, getcontext
from statistics import NormalDist

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402
from stats_common import decimals, half_ulp, rhu, region_prob  # noqa: E402

PAGE = os.path.join(ROOT, 'games', 'normal-navigator', 'index.html')
SLUG = 'normal-navigator'
getcontext().prec = 50
Z = NormalDist()
INF = math.inf
SHADE_TOL = 0.025      # sd; 1 px = 7 sd / 440 px = 0.016 sd
INFINITE_Z = 3.5       # drawBell clips its x-axis at mu +/- 3.5 sd


def _load_check_banks():
    spec = importlib.util.spec_from_file_location('check_banks', os.path.join(HERE, 'check-banks.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# check-banks' own B6 draft-prose rule, reused rather than re-listed, plus the
# markers this bank's history actually showed ("16.6... hmm", "Let me recheck").
DRAFT_PATTERNS = list(_load_check_banks().DRAFT_PATTERNS) + [
    (m, re.compile(r'\b' + m + r'\b', re.IGNORECASE)) for m in ('actually', 'closest', 'recheck')
] + [('...', re.compile(r'\.\.\.|…'))]


# --------------------------------------------------------------------------
#  SPECS: what each question asks, from its prose. Nothing numeric the game
#  computed appears here -- only the numbers printed in the question itself.
#
#  kind      z            z-score of x
#            prob         P(X in region)
#            percent      P(X in region), keyed as a percentage
#            count        n * P(X in region), to the nearest integer
#            inv          k with P(X < k) = p_below
#            invz         z with P(Z < z) = p_below
#            iqr          Q3 - Q1
#            find_sigma   sigma from one condition, mu stated
#            find_mu      mu from one condition, sigma stated
#            find_both    mu and sigma from two conditions
#            empirical    the 68-95-99.7 option nearest the true percentage
#            binom_params mu = np, sigma = sqrt(npq) of the approximation
#            cc_z         continuity-corrected z for the stated binomial event
#            compare      which of two probabilities is larger (keyed by text)
#            density      which pdf is taller at x (keyed by text)
#  region    ('lt', a) ('gt', a) ('between', a, b) ('outside', a, b)
#            ('point', x) -- a marker at x: a tail from x, or a window round it
#  graph     which stated distribution the drawing shows (default: the only one)
# --------------------------------------------------------------------------
SPECS = [
    # --- standardisation ---
    dict(ctx="X ~ N(50, 8²). Find the z-score for x = 66.", kind='z', x=66, region=('point', 66)),
    dict(ctx="X ~ N(100, 15²). Find the z-score for x = 130.", kind='z', x=130, region=('point', 130)),
    dict(ctx="X ~ N(20, 4²). Find the z-score for x = 14.", kind='z', x=14, region=('point', 14)),
    dict(ctx="X ~ N(0, 1). This IS the standard normal.", kind='prob', region=('lt', 0)),
    dict(ctx="X ~ N(75, 10²). Standardise x = 75.", kind='z', x=75, region=('point', 75)),
    # --- P(X < k) ---
    dict(ctx="X ~ N(50, 8²). Find P(X < 66).", kind='prob', region=('lt', 66)),
    dict(ctx="X ~ N(100, 15²). Find P(X < 85).", kind='prob', region=('lt', 85)),
    dict(ctx="X ~ N(40, 5²). Find P(X < 47.5).", kind='prob', region=('lt', 47.5)),
    dict(ctx="X ~ N(200, 25²). Find P(X < 150).", kind='prob', region=('lt', 150)),
    dict(ctx="X ~ N(60, 12²). Find P(X < 60).", kind='prob', region=('lt', 60)),
    # --- P(X > k) ---
    dict(ctx="X ~ N(50, 8²). Find P(X > 58).", kind='prob', region=('gt', 58)),
    dict(ctx="X ~ N(170, 10²). Heights of adults. P(height > 190)?", kind='prob', region=('gt', 190)),
    dict(ctx="X ~ N(500, 100²). Exam marks. P(score > 650)?", kind='prob', region=('gt', 650)),
    dict(ctx="X ~ N(30, 6²). P(X > 18)?", kind='prob', region=('gt', 18)),
    # --- P(a < X < b) ---
    dict(ctx="X ~ N(50, 8²). Find P(42 < X < 58).", kind='prob', region=('between', 42, 58)),
    dict(ctx="X ~ N(100, 15²). P(70 < X < 130)?", kind='prob', region=('between', 70, 130)),
    dict(ctx="X ~ N(80, 10²). P(65 < X < 95)?", kind='prob', region=('between', 65, 95)),
    dict(ctx="X ~ N(0, 1). P(−1.96 < Z < 1.96)?", kind='prob', region=('between', -1.96, 1.96)),
    # --- inverse normal ---
    dict(ctx="X ~ N(50, 8²). Find k such that P(X < k) = 0.9.", kind='inv', p_below=0.9, tail='lt'),
    dict(ctx="X ~ N(100, 15²). Find k such that P(X > k) = 0.05.", kind='inv', p_below=0.95, tail='gt'),
    dict(ctx="X ~ N(200, 25²). The top 10% get an A. Find the minimum mark.", kind='inv', p_below=0.90, tail='gt'),
    dict(ctx="X ~ N(170, 10²). Find the height exceeded by 2.5% of people.", kind='inv', p_below=0.975, tail='gt'),
    dict(ctx="X ~ N(500, 80²). Find the interquartile range.", kind='iqr'),
    # --- context ---
    dict(ctx="Bolts have length X ~ N(50, 0.5²) mm. A bolt is rejected if outside 49–51mm.", kind='prob',
         region=('outside', 49, 51)),
    dict(ctx="IQ scores: X ~ N(100, 15²). Mensa requires top 2%.", kind='inv', p_below=0.98, tail='gt'),
    dict(ctx="A machine fills bottles with X ~ N(500, 8²) ml. A bottle is underfilled if < 490ml.", kind='prob',
         region=('lt', 490)),
    dict(ctx="Delivery times: X ~ N(30, 5²) minutes. A pizza is free if > 45 min.", kind='prob', region=('gt', 45)),
    dict(ctx="Exam marks: X ~ N(65, 12²). The pass mark is set so 80% pass.", kind='inv', p_below=0.20, tail='gt'),
    dict(ctx="Battery life: X ~ N(48, 4²) hours. A battery is 'premium' if it lasts > 54 hours.", kind='percent',
         region=('gt', 54)),
    # --- combined / harder ---
    dict(ctx="X ~ N(μ, σ²). P(X < 20) = 0.1587 and P(X > 35) = 0.0228.", kind='find_both',
         conds=[(20, 'lt'), (35, 'gt')], region=('outside', 20, 35)),
    dict(ctx="X ~ N(50, σ²). P(X < 44) = 0.0668.", kind='find_sigma', conds=[(44, 'lt')], region=('lt', 44)),
    dict(ctx="X ~ N(μ, 6²). P(X > 70) = 0.0228.", kind='find_mu', conds=[(70, 'gt')], region=('gt', 70)),
    # --- empirical rule (symbolic; drawn as the standard normal) ---
    dict(ctx="X ~ N(μ, σ²). Approximately what percentage of data falls within 1 standard deviation of the mean?",
         kind='empirical', k=1, inside=True, region=('between', -1, 1)),
    dict(ctx="X ~ N(μ, σ²). What percentage of data is more than 2 standard deviations from the mean?",
         kind='empirical', k=2, inside=False, region=('outside', -2, 2)),
    # --- normal approximation to the binomial ---
    dict(ctx="X ~ B(100, 0.3). Use a normal approximation.", kind='binom_params', region=None),
    dict(ctx="X ~ B(200, 0.45). Using normal approx, find P(X ≥ 100).", kind='cc_z', boundary=99.5,
         region=('gt', 99.5), extra=[100.5]),  # 100.5: the misconception's P(X > 100) case
    # --- quality control ---
    dict(ctx="A process produces items with mass X ~ N(250, 3²)g. Items outside 244–256g are rejected.",
         kind='prob', region=('between', 244, 256)),
    dict(ctx="Items have mass X ~ N(250, 3²)g and are rejected if outside 244–256g. 1000 items are produced.",
         kind='count', n=1000, region=('outside', 244, 256), extra=[45]),  # 45: the truncation distractor its misconception names
    # --- harder context ---
    dict(ctx="Heights of men: X ~ N(175, 7²)cm. Heights of women: Y ~ N(162, 6²)cm. A randomly chosen person is 168cm. "
             "Assume equal numbers of men and women.",
         kind='density', x=168, labels={'X': 'Man', 'Y': 'Woman'}, region=('point', 168), graph='X'),
    dict(ctx="A Normal distribution has P(X < 10) = 0.1 and P(X < 20) = 0.75.", kind='find_both',
         conds=[(10, 'lt'), (20, 'lt')], asks='mu', region=('between', 10, 20)),
    # --- straightforward ---
    dict(ctx="Z ~ N(0,1). Find P(Z > 1.64).", kind='prob', region=('gt', 1.64)),
    dict(ctx="Z ~ N(0,1). Find the value z such that P(Z < z) = 0.975.", kind='invz', p_below=0.975, tail='lt'),
    dict(ctx="Z ~ N(0,1). Find z such that P(Z > z) = 0.01.", kind='invz', p_below=0.99, tail='gt'),
    dict(ctx="X ~ N(120, 20²). In a sample of 400, how many would you expect below 100?", kind='count', n=400,
         region=('lt', 100)),
    dict(ctx="Weights: X ~ N(70, 8²)kg. What weight is at the 90th percentile?", kind='inv', p_below=0.90, tail='lt'),
    dict(ctx="X ~ N(60, σ²). P(X > 72) = 0.0668.", kind='find_sigma', conds=[(72, 'gt')], region=('gt', 72)),
    dict(ctx="Two events: P(A) = P(Z > 1.5) and P(B) = P(Z < −2). Which is more likely?", kind='compare',
         a=('gt', 1.5), b=('lt', -2), labels={'gt': 'P(A) > P(B)', 'lt': 'P(A) < P(B)', 'eq': 'P(A) = P(B)'},
         region=('multi', ('gt', 1.5), ('lt', -2))),
]

# --------------------------------------------------------------------------
#  numbers and rounding
# --------------------------------------------------------------------------
def clean(s):
    return (s.replace('−', '-').replace('–', '-').replace('×', '*').replace('÷', '/')
            .replace('·', '*').replace(' ', ' ').replace(' ', ' '))


NUM_RE = re.compile(r'-?\d+(?:\.\d+)?')


def matches(stated_tok, true_val):
    """a printed number is right if the true value is within half its last unit"""
    v = float(clean(stated_tok).rstrip('%'))
    return abs(v - true_val) <= half_ulp(decimals(clean(stated_tok).rstrip('%'))) + 1e-12


def parse_value(opt):
    """the numeric value of a plain numeric option ('0.9772', '−1.5', '6.68%'), else None"""
    s = clean(opt).strip()
    m = re.fullmatch(r'(-?\d+(?:\.\d+)?)(%?)', s)
    if not m:
        return None
    return float(m.group(1)), m.group(1), m.group(2) == '%'


def parse_mu_sigma(opt):
    s = clean(opt)
    mu = re.search(r'μ\s*=\s*(-?\d+(?:\.\d+)?)', s)
    sg = re.search(r'σ\s*=\s*(?:√\d+\s*≈\s*)?(-?\d+(?:\.\d+)?)', s)
    if not (mu and sg):
        return None
    return (float(mu.group(1)), mu.group(1)), (float(sg.group(1)), sg.group(1))


# --------------------------------------------------------------------------
#  distributions stated in the prose
# --------------------------------------------------------------------------
def parse_dists(ctx):
    """{'X': (mu, sigma, source)} from 'X ~ N(a, b²)' / 'X ~ B(n, p)'. A symbolic
    parameter is None. N(a, v) with no ² is read as a variance, and is only
    accepted for v = 1 (N(0, 1)): anything else is sigma-vs-variance ambiguous."""
    out, problems = {}, []
    for m in re.finditer(r'([A-Z])\s*~\s*N\(\s*([^,]+?)\s*,\s*([^)]+?)\s*\)', ctx):
        var, a, b = m.group(1), clean(m.group(2)), clean(m.group(3))
        mu = None if a == 'μ' else float(a)
        if b.endswith('²'):
            base = b[:-1]
            sigma = None if base == 'σ' else float(base)
        elif b == '1':
            sigma = 1.0
        else:
            problems.append('N(%s, %s): variance or standard deviation?' % (a, b))
            sigma = None
        out[var] = (mu, sigma, 'N')
    for m in re.finditer(r'([A-Z])\s*~\s*B\(\s*(\d+)\s*,\s*([\d.]+)\s*\)', ctx):
        n, p = int(m.group(2)), float(m.group(3))
        out[m.group(1)] = (n * p, math.sqrt(n * p * (1 - p)), 'B', n, p)
    return out, problems


def cond_probs(ctx):
    """the stated conditions 'P(X < 20) = 0.1587' in a ctx: [(x, 'lt'|'gt', p, p_token)]"""
    out = []
    for m in re.finditer(r'P\(\s*X\s*([<>])\s*(-?\d+(?:\.\d+)?)\s*\)\s*=\s*(\d+(?:\.\d+)?)', clean(ctx)):
        out.append((float(m.group(2)), 'lt' if m.group(1) == '<' else 'gt', float(m.group(3)), m.group(3)))
    return out


# --------------------------------------------------------------------------
#  a tiny evaluator for the arithmetic in worked steps
# --------------------------------------------------------------------------
class NonNumeric(Exception):
    pass


class Val:
    """point: Decimal (the arithmetic a student does with the printed numbers);
    lo/hi: float interval allowing each printed decimal its rounding."""
    __slots__ = ('pt', 'lo', 'hi')

    def __init__(self, pt, lo, hi):
        self.pt, self.lo, self.hi = pt, lo, hi

    @staticmethod
    def exact(x):
        return Val(Decimal(repr(float(x))), float(x), float(x))


def _ival_mul(a, b):
    ps = [a.lo * b.lo, a.lo * b.hi, a.hi * b.lo, a.hi * b.hi]
    return min(ps), max(ps)


class Expr:
    def __init__(self, s, dists):
        self.s = s
        self.i = 0
        self.dists = dists

    def peek(self):
        while self.i < len(self.s) and self.s[self.i] == ' ':
            self.i += 1
        return self.s[self.i] if self.i < len(self.s) else ''

    def parse(self):
        v = self.sum()
        if self.peek() != '':
            raise NonNumeric(self.s[self.i:])
        return v

    def sum(self):
        v = self.term()
        while self.peek() in ('+', '-'):
            op = self.s[self.i]
            self.i += 1
            w = self.term()
            if op == '+':
                v = Val(v.pt + w.pt, v.lo + w.lo, v.hi + w.hi)
            else:
                v = Val(v.pt - w.pt, v.lo - w.hi, v.hi - w.lo)
        return v

    def term(self):
        v = self.unary()
        while True:
            c = self.peek()
            if c in ('*', '/'):
                self.i += 1
                w = self.unary()
            elif c and (c.isdigit() or c in '(Φφ√P'):   # implicit multiplication: 0.6745(5.11), (1/6)φ(1)
                w = self.unary()
                c = '*'
            else:
                return v
            if c == '*':
                lo, hi = _ival_mul(v, w)
                v = Val(v.pt * w.pt, lo, hi)
            else:
                if w.lo <= 0 <= w.hi:
                    raise NonNumeric('division by an interval containing 0')
                lo, hi = _ival_mul(v, Val(Decimal(1), 1 / w.hi, 1 / w.lo))
                v = Val(v.pt / w.pt, lo, hi)

    def unary(self):
        if self.peek() == '-':
            self.i += 1
            v = self.unary()
            return Val(-v.pt, -v.hi, -v.lo)
        if self.peek() == '+':
            self.i += 1
        return self.power()

    def power(self):
        v = self.primary()
        while self.peek() == '²':
            self.i += 1
            lo, hi = sorted([v.lo * v.lo, v.hi * v.hi])
            if v.lo <= 0 <= v.hi:
                lo = 0.0
            v = Val(v.pt * v.pt, lo, hi)
        return v

    def _group(self):
        if self.peek() != '(':
            raise NonNumeric('expected (')
        depth, j = 0, self.i
        while j < len(self.s):
            if self.s[j] == '(':
                depth += 1
            elif self.s[j] == ')':
                depth -= 1
                if depth == 0:
                    break
            j += 1
        if depth != 0:
            raise NonNumeric('unbalanced')
        inner = self.s[self.i + 1:j]
        self.i = j + 1
        return inner

    def primary(self):
        c = self.peek()
        if c == '(':
            return Expr(self._group(), self.dists).parse()
        if c.isdigit():
            m = re.match(r'\d+(?:\.\d+)?', self.s[self.i:])
            tok = m.group(0)
            self.i += len(tok)
            d = decimals(tok)
            if self.peek() == '%':
                self.i += 1
                x = Decimal(tok) / 100
                h = half_ulp(d) / 100 if d else 0.0
                return Val(x, float(x) - h, float(x) + h)
            h = half_ulp(d) if d else 0.0
            return Val(Decimal(tok), float(tok) - h, float(tok) + h)
        if c == '√':
            self.i += 1
            v = self.primary()
            if v.lo < 0:
                raise NonNumeric('sqrt of negative')
            return Val(v.pt.sqrt(), math.sqrt(v.lo), math.sqrt(v.hi))
        if c in 'Φφ':
            self.i += 1
            v = Expr(self._group(), self.dists).parse()
            if c == 'Φ':
                return Val(Decimal(repr(Z.cdf(float(v.pt)))), Z.cdf(v.lo), Z.cdf(v.hi))
            vals = [Z.pdf(v.lo), Z.pdf(v.hi)]
            top = Z.pdf(0.0) if v.lo <= 0 <= v.hi else max(vals)
            return Val(Decimal(repr(Z.pdf(float(v.pt)))), min(vals), top)
        if c == 'P' and self.s[self.i:self.i + 2] == 'P(':
            self.i += 1
            return self.prob(self._group())
        raise NonNumeric(self.s[self.i:])

    def prob(self, inner):
        s = inner.replace(' ', '').replace('≤', '<').replace('≥', '>')
        m = re.fullmatch(r'(-?\d+(?:\.\d+)?)<([XYZ])<(-?\d+(?:\.\d+)?)', s)
        if m:
            d = self.dist(m.group(2))
            p = d.cdf(float(m.group(3))) - d.cdf(float(m.group(1)))
            return Val.exact(p)
        m = re.fullmatch(r'([XYZ])([<>])(-?\d+(?:\.\d+)?)', s)
        if m:
            d = self.dist(m.group(1))
            c = d.cdf(float(m.group(3)))
            return Val.exact(c if m.group(2) == '<' else 1 - c)
        raise NonNumeric('P(' + inner + ')')

    def dist(self, var):
        if var == 'Z':
            return Z
        d = self.dists.get(var)
        if d is None or d[0] is None or d[1] is None:
            raise NonNumeric('no numeric distribution for ' + var)
        return NormalDist(d[0], d[1])


def split_top(s, seps):
    """split s on any of seps, outside parentheses"""
    out, depth, cur, i = [], 0, '', 0
    while i < len(s):
        ch = s[i]
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        if depth == 0:
            hit = next((sp for sp in seps if s.startswith(sp, i)), None)
            if hit:
                out.append((cur, hit))
                cur = ''
                i += len(hit)
                continue
        cur += ch
        i += 1
    out.append((cur, None))
    return out


def evaluate_side(side, dists):
    t = side.strip().rstrip('✓ .').strip()
    if not t or re.search(r'[A-Za-zμσ±|]', re.sub(r'P\(|Φ|φ|√', '', t)):
        raise NonNumeric(t)
    return Expr(t, dists).parse()


def single_literal(side):
    t = clean(side).strip().rstrip('✓ .').strip()
    m = re.fullmatch(r'(-?\d+(?:\.\d+)?)(%?)', t)
    if not m:
        return None
    tok = m.group(1)
    d = decimals(tok) + (2 if m.group(2) else 0)
    val = Decimal(tok) / (100 if m.group(2) else 1)
    return val, d


NET_NUM = re.compile(r'(?<![A-Za-z_\d.₀-₉¹²³⁰-₟])(\d+(?:\.\d+)?)(%?)')


def check_text(text, dists, known, where, fail):
    """every chain in `text`; numbers outside a checked chain go through the net"""
    stray = []
    for stmt, _ in split_top(clean(text), ['→', ';', ', ', ': ', ' so ', ' and ']):
        parts = split_top(stmt, ['≈', '=', '>', '<', '≥', '≤'])
        sides = [p for p, _ in parts]
        # "(0.6745 + 1.282)σ = 1.9565σ": a symbol that is a trailing factor of a
        # side is set aside, and only sides with the SAME factor are compared --
        # so c1·σ = c2·σ checks c1 = c2, and "10 = (...)σ" is left alone
        factor = [''] * len(sides)
        for k, sd in enumerate(sides):
            t = sd.rstrip()
            for sym in ('σ', 'μ'):
                if t.endswith(sym) and re.search(r'[\d)]$', t[:-1].rstrip()):
                    sides[k], factor[k] = t[:-1], sym
        rels = [r for _, r in parts[:-1]]
        vals = []
        for sd in sides:
            try:
                vals.append(evaluate_side(sd, dists))
            except NonNumeric:
                vals.append(None)
        used = [False] * len(sides)
        for k, rel in enumerate(rels):
            a, b = vals[k], vals[k + 1]
            if a is None or b is None or factor[k] != factor[k + 1]:
                continue
            used[k] = used[k + 1] = True
            la, lb = single_literal(sides[k]), single_literal(sides[k + 1])
            if rel in ('>', '<', '≥', '≤'):
                ok = {'>': a.pt > b.pt, '<': a.pt < b.pt, '≥': a.pt >= b.pt, '≤': a.pt <= b.pt}[rel]
                if not ok:
                    fail(where, '"%s %s %s" is false' % (sides[k].strip(), rel, sides[k + 1].strip()),
                         '%s vs %s' % (a.pt, b.pt))
                continue
            if lb and not la:
                ok = rhu(a.pt, lb[1]) == rhu(lb[0], lb[1])
                got = rhu(a.pt, lb[1])
            elif la and not lb:
                ok = rhu(b.pt, la[1]) == rhu(la[0], la[1])
                got = rhu(b.pt, la[1])
            elif la and lb:
                d = min(la[1], lb[1])
                ok = rhu(la[0], d) == rhu(lb[0], d)
                got = rhu(la[0], d)
            else:
                ok = a.lo <= b.hi + 1e-12 and b.lo <= a.hi + 1e-12
                got = '%.6g' % float(a.pt)
            if not ok:
                fail(where, '"%s %s %s"' % (sides[k].strip(), rel, sides[k + 1].strip()),
                     'left side is %s' % got)
        for k, sd in enumerate(sides):
            if not used[k]:
                stray.append(sd)
    for sd in stray:
        for m in NET_NUM.finditer(sd):
            tok, pct = m.group(1), m.group(2)
            v = float(tok) / (100 if pct else 1)
            d = decimals(tok) + (2 if pct else 0)
            if not any(abs(abs(v) - abs(k)) <= half_ulp(d) + 1e-9 for k in known):
                fail(where, 'number %s%s' % (tok, pct), 'matches nothing derivable from the question')


# --------------------------------------------------------------------------
#  per-question verification
# --------------------------------------------------------------------------
class Report:
    def __init__(self):
        self.fails = []

    def fail(self, qid, field, stated, computed=None):
        self.fails.append('FAIL %s %s: stated %s%s' % (qid, field, stated,
                                                       '' if computed is None else ', computed %s' % computed))


def known_values(q, dists, spec, true_mu, true_sigma, extras):
    text = ' '.join([q.get('ctx', ''), q.get('q', '')])
    k = set([0, 1, 2, 3, 4, 68, 95, 99.7])
    base = [float(t) for t in NUM_RE.findall(clean(text))]
    base += [abs(b) for b in base]
    k.update(base)
    probs = [b for b in base if 0 < b < 1]
    alltext = clean(' '.join([text, q.get('misconception', '')] + list(q.get('steps', []))))
    probs += [float(t) / 100 for t in re.findall(r'(\d+(?:\.\d+)?)%', alltext)]
    for d in dists.values():
        for v in d[:2]:
            if v is not None:
                k.update([v, v * v])
        if d[2] == 'B':
            n, p = d[3], d[4]
            k.update([n, p, 1 - p, n * p, n * p * (1 - p)])
    xs = list(base) + list(extras)
    if true_mu is not None:
        k.update([true_mu, true_sigma, true_sigma ** 2])
        for x in xs:
            z = (x - true_mu) / true_sigma
            k.update([z, Z.cdf(z), 1 - Z.cdf(z), x - true_mu])
            probs += [Z.cdf(z), 1 - Z.cdf(z)]
    for x in xs:
        k.update([Z.cdf(x), 1 - Z.cdf(x)])
    for p in probs + list(extras):
        for pp in (p, 1 - p, p / 2, 2 * p):
            if 0 < pp < 1:
                k.add(pp)
                z = Z.inv_cdf(pp)
                k.update([z, 2 * z])
                if true_sigma:
                    k.update([z * true_sigma, true_mu + z * true_sigma if true_mu is not None else z])
    k.update(extras)
    return k


def verify_question(rep, i, q, line, spec, verbose):
    qid = '%s::QUESTIONS[%d] (:%d)' % (SLUG, i, line)
    ctx = q.get('ctx', '')
    dists, problems = parse_dists(ctx)
    for p in problems:
        rep.fail(qid, 'ctx', p)
    kind = spec['kind']
    key = q.get('correct_override') or q.get('correct')
    opts = list(q.get('opts', []))
    if 'correct_override' in q:
        rep.fail(qid, 'correct_override', repr(q['correct_override']),
                 'fold into `correct` (todo §1.26; check-banks B10)')
    if not key:
        rep.fail(qid, 'correct', 'missing')
        return
    if opts.count(key) != 1:
        rep.fail(qid, 'opts', 'key %r appears %d times in %r' % (key, opts.count(key), opts))
    if len(set(opts)) != len(opts):
        rep.fail(qid, 'opts', 'duplicate option strings %r' % opts)

    # the distribution the question is about
    var = spec.get('graph', 'X' if 'X' in dists else (next(iter(dists)) if dists else None))
    d = dists.get(var) if var else None
    mu = d[0] if d else None
    sigma = d[1] if d else None
    if var is None and ctx.startswith('Z ') is False and kind not in ('empirical', 'compare', 'find_both'):
        rep.fail(qid, 'ctx', 'states no distribution (the pool is shuffled, so it cannot lean on another question)')
    if ctx.startswith('Z ~') or kind == 'compare':
        mu, sigma = 0.0, 1.0
    if kind == 'empirical':
        mu, sigma = 0.0, 1.0   # symbolic: drawn and worked as the standard normal
    extras = list(spec.get('extra', []))
    answer = None           # the true value of the key (float), or tuple, or label
    answer_region = spec.get('region')
    solved = {}

    try:
        if kind in ('z', 'prob', 'percent', 'count', 'inv', 'iqr', 'cc_z') and (mu is None or sigma is None):
            raise NonNumeric('no distribution')
        if kind == 'z':
            answer = (spec['x'] - mu) / sigma
        elif kind in ('prob', 'percent', 'count'):
            p = region_prob(NormalDist(mu, sigma), spec['region'])
            answer = {'prob': p, 'percent': 100 * p, 'count': spec.get('n', 1) * p}[kind]
            extras += [p, 1 - p, spec.get('n', 1) * p]
            if kind == 'count':
                # "how many would you expect" is keyed to the nearest whole item
                answer = float(rhu(Decimal(repr(answer)), 0))
        elif kind == 'inv':
            answer = NormalDist(mu, sigma).inv_cdf(spec['p_below'])
            answer_region = (spec['tail'], answer)
        elif kind == 'invz':
            answer = Z.inv_cdf(spec['p_below'])
            answer_region = (spec['tail'], answer)
        elif kind == 'iqr':
            nd = NormalDist(mu, sigma)
            q1, q3 = nd.inv_cdf(0.25), nd.inv_cdf(0.75)
            answer = q3 - q1
            answer_region = ('between', q1, q3)
            extras += [q1, q3]
        elif kind == 'cc_z':
            answer = (spec['boundary'] - mu) / sigma
            extras += [spec['boundary']]
        elif kind == 'binom_params':
            answer = (mu, sigma)
        elif kind == 'empirical':
            p = region_prob(Z, ('between', -spec['k'], spec['k']))
            answer = 100 * (p if spec['inside'] else 1 - p)
        elif kind == 'compare':
            pa, pb = region_prob(Z, spec['a']), region_prob(Z, spec['b'])
            answer = spec['labels']['gt' if pa > pb else 'lt' if pa < pb else 'eq']
            extras += [pa, pb]
        elif kind == 'density':
            dens = {v: NormalDist(dd[0], dd[1]).pdf(spec['x']) for v, dd in dists.items()}
            best = max(dens, key=dens.get)
            answer = spec['labels'][best]
            for v, dd in dists.items():
                extras.append((spec['x'] - dd[0]) / dd[1])
        elif kind in ('find_sigma', 'find_mu', 'find_both'):
            conds = cond_probs(ctx)
            if [(c[0], c[1]) for c in conds] != [tuple(c) for c in spec['conds']]:
                rep.fail(qid, 'ctx', 'conditions %r' % conds, 'spec %r' % spec['conds'])
                return
            zs = [Z.inv_cdf(p if t == 'lt' else 1 - p) for x, t, p, _ in conds]
            if kind == 'find_sigma':
                s_ = (conds[0][0] - mu) / zs[0]
                solved = {'mu': mu, 'sigma': s_}
                answer = s_
            elif kind == 'find_mu':
                m_ = conds[0][0] - zs[0] * sigma
                solved = {'mu': m_, 'sigma': sigma}
                answer = m_
            else:
                (x1, _, _, _), (x2, _, _, _) = conds
                s_ = (x2 - x1) / (zs[1] - zs[0])
                m_ = x1 - zs[0] * s_
                solved = {'mu': m_, 'sigma': s_}
                answer = m_ if spec.get('asks') == 'mu' else (m_, s_)
                extras += [zs[1] - zs[0], zs[0] * s_, zs[1] * s_]
            mu, sigma = solved['mu'], solved['sigma']
        else:
            raise ValueError(kind)
    except NonNumeric as e:
        rep.fail(qid, 'answer', 'cannot be computed from the question as written', str(e))
        return

    # ---- the key against the true answer ------------------------------
    if verbose:
        print('  [%d] %-12s key %-28r true %r' % (i, kind, key, answer))
    if kind in ('compare', 'density'):
        # keyed by label; an option may explain itself after the label
        hits = [o for o in opts if o == answer or o.startswith(answer + ' ')]
        if not (key == answer or key.startswith(answer + ' ')) or len(hits) != 1:
            rep.fail(qid, 'correct', repr(key), repr(answer))
    elif kind == 'empirical':
        vals = [(abs(parse_value(o)[0] - answer), o) for o in opts if parse_value(o)]
        nearest = min(vals)[1]
        if key != nearest:
            rep.fail(qid, 'correct', repr(key), 'nearest option to %.2f%% is %r' % (answer, nearest))
    elif kind == 'cc_z':
        toks = NUM_RE.findall(clean(key))
        if not toks or not matches(toks[-1], answer) or float(toks[0]) != spec['boundary']:
            rep.fail(qid, 'correct', repr(key), 'z = (%g − μ)/σ = %.4f' % (spec['boundary'], answer))
        zs = [NUM_RE.findall(clean(o))[-1] for o in opts]
        for a_ in range(len(zs)):
            for b_ in range(a_ + 1, len(zs)):
                if float(zs[a_]) == float(zs[b_]):
                    rep.fail(qid, 'opts', 'options %r and %r give the same z' % (opts[a_], opts[b_]))
    elif kind in ('binom_params',) or (kind == 'find_both' and spec.get('asks') != 'mu'):
        pm = parse_mu_sigma(key)
        if not pm:
            rep.fail(qid, 'correct', repr(key), 'not a "μ = a, σ = b" answer')
        else:
            (km, kmt), (ks, kst) = pm
            if not (matches(kmt, answer[0]) and matches(kst, answer[1])):
                rep.fail(qid, 'correct', repr(key), 'μ = %.4f, σ = %.4f' % answer)
            if kind == 'find_both':
                # the keyed pair must satisfy EVERY stated condition, at its printed precision
                for x, t, p, ptok in cond_probs(ctx):
                    c = NormalDist(km, ks).cdf(x)
                    got = c if t == 'lt' else 1 - c
                    if not matches(ptok, got):
                        rep.fail(qid, 'correct', '%r gives P(X %s %g) = %.4f' % (key, '<' if t == 'lt' else '>', x, got),
                                 'the question states %s' % ptok)
            pairs = [parse_mu_sigma(o) for o in opts]
            seen = {}
            for o, pr in zip(opts, pairs):
                if pr is None:
                    rep.fail(qid, 'opts', 'option %r is not a "μ = a, σ = b" pair' % o)
                    continue
                sig = (pr[0][0], pr[1][0])
                if sig in seen:
                    rep.fail(qid, 'opts', 'options %r and %r are the same pair' % (seen[sig], o))
                seen[sig] = o
                if o != key and matches(pr[0][1], answer[0]) and matches(pr[1][1], answer[1]):
                    rep.fail(qid, 'opts', 'distractor %r equals the answer' % o)
    else:
        pv = parse_value(key)
        if pv is None:
            rep.fail(qid, 'correct', repr(key), 'not a number')
        else:
            v, tok, pct = pv
            if not matches(tok, answer):
                d_ = decimals(tok)
                rep.fail(qid, 'correct', repr(key), '%s%s (%.6f)' % (rhu(answer, d_), '%' if pct else '', answer))
            if kind in ('find_sigma', 'find_mu'):
                km = v if kind == 'find_mu' else mu
                ks = v if kind == 'find_sigma' else sigma
                for x, t, p, ptok in cond_probs(ctx):
                    c = NormalDist(km, ks).cdf(x)
                    got = c if t == 'lt' else 1 - c
                    if not matches(ptok, got):
                        rep.fail(qid, 'correct', '%r gives P(X %s %g) = %.4f' % (key, '<' if t == 'lt' else '>', x, got),
                                 'the question states %s' % ptok)
        vals = []
        for o in opts:
            po = parse_value(o)
            if po is None:
                rep.fail(qid, 'opts', 'option %r is not a number like its key' % o)
                continue
            vals.append((po[0], o))
            # a distractor collides with the answer if it IS the answer at the
            # precision it is printed to. An exact answer (z = -1.5) is only a
            # different number from a coarser distractor (-2), so for exact
            # answers the comparison is at the key's precision instead.
            exact = abs(answer - float(rhu(answer, 6))) < 1e-9 and pv and abs(float(pv[1]) - answer) < 1e-9
            d_show = max(decimals(pv[1]), decimals(po[1])) if exact else decimals(po[1])
            if o != key and rhu(answer, d_show) == rhu(Decimal(po[1]), d_show):
                rep.fail(qid, 'opts', 'distractor %r' % o, 'equals the true answer %.6f at its precision' % answer)
        for a_ in range(len(vals)):
            for b_ in range(a_ + 1, len(vals)):
                if vals[a_][0] == vals[b_][0]:
                    rep.fail(qid, 'opts', 'options %r and %r are equal' % (vals[a_][1], vals[b_][1]))

    # ---- the drawing -----------------------------------------------------
    gmu, gsig = q.get('mu'), q.get('sigma')
    if mu is not None and sigma is not None:
        if kind in ('find_mu',) or (kind == 'find_both'):
            want_mu = float(parse_mu_sigma(key)[0][0]) if kind == 'find_both' and spec.get('asks') != 'mu' \
                else float(parse_value(key)[0]) if parse_value(key) else mu
            if gmu != want_mu:
                rep.fail(qid, 'mu (graph)', gmu, 'the answer\'s μ, %g' % want_mu)
        if not matches(repr(gmu), mu):
            rep.fail(qid, 'mu (graph)', gmu, '%.4f' % mu)
        if not matches(repr(gsig), sigma):
            rep.fail(qid, 'sigma (graph)', gsig, '%.4f' % sigma)
        reg = answer_region
        sh = q.get('shade') or []
        if reg is not None and len(sh) == 2 and gsig:
            check_shade(rep, qid, ctx, reg, sh, gmu, gsig)

    # ---- worked steps and every other printed string ---------------------
    known = known_values(q, dists, spec, mu, sigma, extras + [answer] * (isinstance(answer, float))
                         + (list(answer) if isinstance(answer, tuple) else []))
    steps = []
    for st in q.get('steps', []):
        if st.lstrip().startswith('=') and steps:
            steps[-1] += ' ' + st
        else:
            steps.append(st)
    ev_dists = dict(dists)
    if 'Y' not in ev_dists and 'X' in ev_dists:
        ev_dists['Y'] = ev_dists['X']     # 'P(Y > 99.5)': the approximating normal
    if solved:
        ev_dists = {}                    # conditions in terms of unknown μ, σ: not evaluable
    fields = [('steps', s) for s in steps] + [('misconception', q.get('misconception', ''))]
    fields += [('opts', o) for o in opts if kind == 'cc_z']
    fields += [('q', q.get('q', ''))]
    if not solved:
        fields += [('ctx', ctx)]
    for fname, text in fields:
        if text:
            check_text(text, ev_dists, known, fname,
                       lambda where, what, why: rep.fail(qid, where, what, why))
    for fname in ('ctx', 'q', 'misconception'):
        check_draft(rep, qid, fname, q.get(fname, ''))
    for st in q.get('steps', []):
        check_draft(rep, qid, 'steps', st)
    for o in opts:
        check_draft(rep, qid, 'opts', o)


def check_draft(rep, qid, field, text):
    for marker, pat in DRAFT_PATTERNS:
        if text and pat.search(text):
            rep.fail(qid, field, 'draft marker %r in %r' % (marker, text))


def check_shade(rep, qid, ctx, reg, sh, gmu, gsig):
    def z_of(b):
        if b in (-999, 999):
            return -INF if b < 0 else INF
        return (b - gmu) / gsig

    def at(bound, target):
        zb, zt = z_of(bound), (target - gmu) / gsig if abs(target) != INF else target
        if abs(zt) == INF:
            return zb == zt or (abs(zb) >= INFINITE_Z and (zb > 0) == (zt > 0))
        return abs(zb - zt) <= SHADE_TOL

    # shade is [L, R] for one region, or [[L, R], [L, R]] for a two-region question
    drawn = [tuple(r) for r in sh] if sh and isinstance(sh[0], list) else [tuple(sh)]

    def interval_ok(iv, lo, hi):
        return len(iv) == 2 and at(iv[0], lo) and at(iv[1], hi)

    def one(lo, hi):
        return len(drawn) == 1 and interval_ok(drawn[0], lo, hi)

    k = reg[0]
    if k == 'lt':
        ok = one(-INF, reg[1])
    elif k == 'gt':
        ok = one(reg[1], INF)
    elif k == 'between':
        ok = one(reg[1], reg[2])
    elif k == 'point':
        x = reg[1]
        zx = (x - gmu) / gsig
        ok = one(x, INF) or one(-INF, x) or (len(drawn) == 1 and z_of(drawn[0][0]) <= zx <= z_of(drawn[0][1])
                                             and z_of(drawn[0][1]) - z_of(drawn[0][0]) <= 0.5)
    elif k in ('outside', 'multi'):
        # every part of the region shaded, and nothing else: a one-tail drawing
        # of a two-tail region shows the student half the question
        parts = [(-INF, reg[1]), (reg[2], INF)] if k == 'outside' else \
            [(-INF, r[1]) if r[0] == 'lt' else (r[1], INF) for r in reg[1:]]
        ok = len(drawn) == len(parts) and all(any(interval_ok(iv, *p) for iv in drawn) for p in parts)
    else:
        raise ValueError(reg)
    if not ok:
        want = {'lt': '[-∞, %g]', 'gt': '[%g, ∞]'}.get(k)
        rep.fail(qid, 'shade', sh, (want % reg[1]) if want else repr(reg))


# --------------------------------------------------------------------------
#  what the student sees: the page, rendered
# --------------------------------------------------------------------------
RENDER_JS = """(i) => {
  const svg = () => {
    const s = document.getElementById('bellSvg');
    return {
      labels: [...s.querySelectorAll('text')].map(t => ({text: t.textContent, x: parseFloat(t.getAttribute('x'))})),
      ticks: [...s.querySelectorAll('line')].filter(l => l.getAttribute('x1') === l.getAttribute('x2')).length,
      shades: [...s.querySelectorAll('path.shade')].map(p => { const b = p.getBBox(); return [b.x, b.x + b.width]; }),
      curves: s.querySelectorAll('path:not(.shade)').length,
    };
  };
  pool = [QUESTIONS[i]]; qIdx = 0; total = 0;
  show('game'); nextQ();
  const pre = document.getElementById('bellInfo').textContent;
  const paths = document.querySelectorAll('#bellSvg path.shade').length;
  const svgPre = svg();
  document.querySelector('#options .opt-btn').click();
  const post = document.getElementById('bellInfo').textContent;
  return {pre: pre, post: post, paths: paths, svgPre: svgPre, svgPost: svg()};
}"""

# answers that ARE a position on the x-axis: the shading boundary is the answer
BOUNDARY_KINDS = ('z', 'inv', 'invz', 'cc_z')
TICK_RE = re.compile(r'^μ(?:([+-])(\d+)σ)?$')


def render_all(n):
    """{i: {pre, post, paths}} for every question, drawn by the real page"""
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/' + SLUG + '/?cb=verify', wait_until='load', timeout=20000)
            out = {i: page.evaluate(RENDER_JS, i) for i in range(n)}
            browser.close()
            if errors:
                sys.exit('page errors while rendering: %s' % '; '.join(errors))
            return out
    finally:
        proc.terminate()
        proc.wait()


def tick_value(text):
    """'μ+2σ' -> 2, 'μ' -> 0, 'μ−1σ' -> -1; None for any other text"""
    m = TICK_RE.match(clean(text).strip())
    if not m:
        return None
    return 0 if m.group(1) is None else (int(m.group(2)) * (1 if m.group(1) == '+' else -1))


def check_picture(rep, qid, q, spec, r):
    key = q.get('correct_override') or q.get('correct') or ''
    kind = spec['kind'] if spec else None
    pre, post = r['svgPre'], r['svgPost']
    ticks = [(tick_value(l['text']), l['x']) for l in pre['labels'] if tick_value(l['text']) is not None]
    # a labelled tick on a shading boundary, or inside a narrow marker window,
    # names that boundary: if its value (as z, or as x = mu + k sigma) is the
    # answer, the picture gives the answer away
    nums = NUM_RE.findall(clean(key))
    if nums and ticks and len(ticks) > 1:
        tok = nums[-1]
        px_per_sd = abs(ticks[1][1] - ticks[0][1]) / abs(ticks[1][0] - ticks[0][0])
        for k, x in ticks:
            marked = any(abs(x - a) <= 2 or abs(x - b) <= 2 or (a <= x <= b and b - a <= 0.5 * px_per_sd)
                         for a, b in pre['shades'])
            if marked and (matches(tok, k) or matches(tok, q['mu'] + k * q['sigma'])):
                rep.fail(qid, 'picture (before answering)', 'tick %r marks a shading boundary' %
                         next(l['text'] for l in pre['labels'] if l['x'] == x), 'that is the answer %r' % key)
    if kind in BOUNDARY_KINDS:
        if pre['ticks'] or ticks:
            rep.fail(qid, 'picture (before answering)', '%d tick marks, %d tick labels' % (pre['ticks'], len(ticks)),
                     'none: the answer is a boundary, and ticks either side of it read it off')
        n_post = sum(1 for l in post['labels'] if tick_value(l['text']) is not None)
        if n_post != 7 or post['ticks'] != 7:
            rep.fail(qid, 'picture (after answering)', '%d tick marks, %d tick labels' % (post['ticks'], n_post),
                     '7 of each, revealed once answered')
    if kind == 'density':
        for when, st in (('before', pre), ('after', post)):
            text = ' '.join(l['text'] for l in st['labels']).lower()
            ok = st['curves'] == 0 or (st['curves'] == 2 and 'men' in text.replace('women', '') and 'women' in text)
            if not ok:
                rep.fail(qid, 'picture (%s answering)' % when, '%d curve(s) drawn' % st['curves'],
                         'both distributions\' curves, labelled, or none')


def check_rendered(rep, bank, lines, rendered):
    by_ctx = {sp['ctx']: sp for sp in SPECS}
    for i, q in enumerate(bank):
        qid = '%s::QUESTIONS[%d] (:%d)' % (SLUG, i, lines[i])
        r = rendered.get(i)
        if r is None:
            rep.fail(qid, 'render', 'not rendered')
            continue
        check_picture(rep, qid, q, by_ctx.get(q.get('ctx')), r)
        key = q.get('correct_override') or q.get('correct') or ''
        opts = q.get('opts', [])
        # an answer number printed in the labels before answering, unless every
        # option carries it too (then it tells the student nothing)
        opt_nums = [set(float(t) for t in NUM_RE.findall(clean(o))) for o in opts]
        telling = {float(t) for t in NUM_RE.findall(clean(key))
                   if not all(float(t) in on for on in opt_nums)}
        shown = {float(t) for t in NUM_RE.findall(clean(r['pre']))}
        leak = sorted(telling & shown)
        if leak:
            rep.fail(qid, 'labels (before answering)', repr(r['pre'].strip()),
                     'shows %s from the answer %r' % (', '.join('%g' % v for v in leak), key))
        post = {float(t) for t in NUM_RE.findall(clean(r['post']))}
        if not {float(q.get('mu')), float(q.get('sigma'))} <= post:
            rep.fail(qid, 'labels (after answering)', repr(r['post'].strip()),
                     'μ = %s, σ = %s' % (q.get('mu'), q.get('sigma')))
        sh = q.get('shade') or []
        want = len(sh) if sh and isinstance(sh[0], list) else 1
        if q.get('noCurve'):
            want = 0                     # two distributions: no curve, so nothing to shade
        if r['paths'] != want:
            rep.fail(qid, 'shaded regions drawn', r['paths'], want)


# --------------------------------------------------------------------------
#  the bank
# --------------------------------------------------------------------------
def load_bank(page):
    with open(page, encoding='utf-8') as f:
        html = f.read()
    tree, src = bc.parse_game_source(html)
    if tree is None:
        sys.exit('could not parse %s' % page)
    decl = [init for name, init, _ in bc.top_level_declarations(tree) if name == 'QUESTIONS']
    if len(decl) != 1:
        sys.exit('expected exactly one top-level QUESTIONS literal, found %d' % len(decl))
    value = bc.static_bank_value('QUESTIONS', decl[0], tree)
    if value is None:
        sys.exit('QUESTIONS is not a static literal: the verifier cannot read it')
    lines = [bc.line_of(src, el.range[0]) for el in decl[0].elements]
    patches = [bc.line_of(src, a.range[0]) for n, a in bc.find_index_patches(tree) if n == 'QUESTIONS']
    return value, lines, patches


def norm_text(s):
    return re.sub(r'\s+', ' ', clean(s).lower()).strip()


def verify(bank, lines, patches, verbose=False, rendered=None):
    rep = Report()
    for ln in patches:
        rep.fail('%s (:%d)' % (SLUG, ln), 'QUESTIONS[n] = ...', 'hand-written index patch after the bank literal')
    by_ctx = {}
    for s in SPECS:
        if s['ctx'] in by_ctx:
            sys.exit('two specs for one ctx: %r' % s['ctx'])
        by_ctx[s['ctx']] = s
    seen_text, seen_maths, used = {}, {}, set()
    for i, q in enumerate(bank):
        qid = '%s::QUESTIONS[%d] (:%d)' % (SLUG, i, lines[i])
        t = norm_text(q.get('ctx', '') + ' | ' + q.get('q', ''))
        if t in seen_text:
            rep.fail(qid, 'ctx/q', 'duplicate of QUESTIONS[%d]' % seen_text[t])
        seen_text[t] = i
        spec = by_ctx.get(q.get('ctx'))
        if spec is None:
            rep.fail(qid, 'ctx', repr(q.get('ctx')), 'no spec: write one in SPECS before this question can ship')
            continue
        if q.get('ctx') in used:
            rep.fail(qid, 'ctx', 'second question with the same ctx')
        used.add(q.get('ctx'))
        dists, _ = parse_dists(q.get('ctx', ''))
        m = (spec['kind'], repr(sorted(dists.items())), repr(spec.get('region')), spec.get('x'),
             spec.get('p_below'), repr(spec.get('conds')), spec.get('n'))
        if m in seen_maths:
            rep.fail(qid, 'ctx', 'asks the same thing as QUESTIONS[%d]' % seen_maths[m])
        seen_maths[m] = i
        verify_question(rep, i, q, lines[i], spec, verbose)
    for ctx in set(by_ctx) - used:
        rep.fail(SLUG, 'SPECS', 'spec for a question no longer in the bank: %r' % ctx)
    if rendered is not None:
        check_rendered(rep, bank, lines, rendered)
    return rep


# --------------------------------------------------------------------------
#  fault injection: each must FAIL on the named question and field
# --------------------------------------------------------------------------
def _find(bank, prefix):
    for i, q in enumerate(bank):
        if q.get('ctx', '').startswith(prefix):
            return i
    raise KeyError(prefix)


def _swap_key(q, new):
    old = q.get('correct_override') or q['correct']
    q.pop('correct_override', None)
    q['correct'] = new
    q['opts'] = [new if o == old else o for o in q['opts']]


def selftest(bank, lines, rendered):
    faults = []

    def f_prob(b):                       # a probability, keyed 1 in the 4th d.p. out
        _swap_key(b[_find(b, 'X ~ N(50, 8²). Find P(X < 66)')], '0.9773')
    faults.append(('probability', 'X ~ N(50, 8²). Find P(X < 66)', 'correct', f_prob))

    def f_both(b):                       # satisfies μ − σ = 20 only, not P(X > 35) = 0.0228
        _swap_key(b[_find(b, 'X ~ N(μ, σ²). P(X < 20)')], 'μ = 22, σ = 2')
    faults.append(('inverse, one condition only', 'X ~ N(μ, σ²). P(X < 20)', 'correct', f_both))

    def f_graph(b):                      # the drawn μ is not the answer's
        b[_find(b, 'X ~ N(μ, 6²). P(X > 70)')]['mu'] = 60
    faults.append(('graph μ', 'X ~ N(μ, 6²). P(X > 70)', 'mu (graph)', f_graph))

    def f_step(b):                       # worked-step arithmetic that does not close
        q = b[_find(b, 'X ~ N(50, 8²). Find P(X > 58)')]
        q['steps'] = [s.replace('= 0.1587', '= 0.1578') for s in q['steps']]
    faults.append(('step arithmetic', 'X ~ N(50, 8²). Find P(X > 58)', 'steps', f_step))

    def f_distractor(b):                 # a distractor equal to the answer at its precision
        q = b[_find(b, 'X ~ N(100, 15²). Find P(X < 85)')]
        q['opts'] = [q['opts'][0], '0.159', q['opts'][2], q['opts'][3]]
    faults.append(('distractor = answer', 'X ~ N(100, 15²). Find P(X < 85)', 'opts', f_distractor))

    def f_draft(b):
        b[_find(b, 'X ~ N(200, 25²). Find P(X < 150)')]['steps'].append('Actually, wait: check this')
    faults.append(('draft prose', 'X ~ N(200, 25²). Find P(X < 150)', 'steps', f_draft))

    def f_dup(b):
        b.append(copy.deepcopy(b[0]))
    faults.append(('duplicate question', None, 'ctx/q', f_dup))

    def f_override(b):
        b[_find(b, 'X ~ N(60, 12²)')]['correct_override'] = '0.5'
    faults.append(('correct_override', 'X ~ N(60, 12²)', 'correct_override', f_override))

    def f_one_tail(b):                   # a two-tail region drawn as one tail
        b[_find(b, 'Bolts have length')]['shade'] = [-999, 49]
    faults.append(('two-tail region, one tail', 'Bolts have length', 'shade', f_one_tail))

    if rendered is not None:
        def f_leak(b, r):                # "Find μ" with the answer printed under the curve
            i = _find(b, 'X ~ N(μ, 6²). P(X > 70)')
            r[i] = dict(r[i], pre=r[i]['post'])
        faults.append(('answer in labels', 'X ~ N(μ, 6²). P(X > 70)', 'labels (before answering)', f_leak))

        def f_paths(b, r):               # the page draws one region for a two-region question
            i = _find(b, 'Bolts have length')
            r[i] = dict(r[i], paths=1)
        faults.append(('regions drawn', 'Bolts have length', 'shaded regions drawn', f_paths))

        def f_ticks(b, r):               # "find z" with the answer's tick labelled at the boundary
            i = _find(b, 'X ~ N(50, 8²). Find the z-score')
            r[i] = dict(r[i], svgPre=r[i]['svgPost'])
        faults.append(('answer tick at boundary', 'X ~ N(50, 8²). Find the z-score', 'picture (before answering)',
                       f_ticks))

        def f_one_curve(b, r):           # men and women, but only the men's curve drawn
            i = _find(b, 'Heights of men')
            r[i] = dict(r[i], svgPre=dict(r[i]['svgPre'], curves=1))
        faults.append(('one of two curves', 'Heights of men', 'picture (before answering)', f_one_curve))

    base = verify(bank, lines, [], False, rendered)
    base_fails = set(base.fails)
    missed = []
    for name, prefix, field, inject in faults:
        b = copy.deepcopy(bank)
        r = copy.deepcopy(rendered)
        if inject.__code__.co_argcount == 2:
            inject(b, r)
        else:
            inject(b)
        ln = list(lines) + [lines[-1]] * (len(b) - len(lines))
        if r is not None:
            for k in range(len(rendered), len(b)):
                r[k] = r[0]
        new = [f for f in verify(b, ln, [], False, r).fails if f not in base_fails]
        idx = _find(b, prefix) if prefix else len(b) - 1
        tag = 'QUESTIONS[%d] ' % idx
        hit = [f for f in new if tag in f and (' %s:' % field) in f]
        print('  self-test %-28s %s' % (name, ('caught: ' + hit[0][:110]) if hit else 'NOT CAUGHT'))
        if not hit:
            missed.append(name)
    return missed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--page', default=PAGE)
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--no-selftest', action='store_true', help=argparse.SUPPRESS)
    args = ap.parse_args()
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    bank, lines, patches = load_bank(args.page)
    print('normal-navigator: %d questions read from %s' % (len(bank), args.page))
    # the page is only rendered when it is the real one: a --page copy is not served
    rendered = render_all(len(bank)) if os.path.abspath(args.page) == os.path.abspath(PAGE) else None
    if not args.no_selftest:
        missed = selftest(bank, lines, rendered)
        if missed:
            print('SELF-TEST FAILED: injected faults not caught: %s' % ', '.join(missed))
            return 2
    rep = verify(bank, lines, patches, args.verbose, rendered)
    for f in rep.fails:
        print(f)
    failing_q = sorted({re.search(r'QUESTIONS\[(\d+)\]', f).group(1) for f in rep.fails if 'QUESTIONS[' in f}, key=int)
    print('%s: %d FAIL across %d of %d questions%s' % (
        'FAIL' if rep.fails else 'PASS', len(rep.fails), len(failing_q), len(bank),
        '' if rendered is not None else ' (bank only, not rendered)'))
    return 1 if rep.fails else 0


if __name__ == '__main__':
    sys.exit(main())
