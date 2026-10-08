#!/usr/bin/env python3
# ci-line: B2 | Spot the Muppet (every equation in the advice and the keys recomputed; every key recomputed from its own givens; no distractor ends on the key's value (SR-16); answer once and Next once, played in Chromium) |
"""Spot the Muppet: the maths every item shows, recomputed; one mark per question; Next once.

Each item is a character's advice and four options, one keyed correct. A question has two picks: a first wrong pick is a
retry and marks nothing; the question is marked once, when it is right or at the second wrong pick. The bank is read
from the live page, then:

  Bank: 18 KS3, 20 GCSE, 12 Core items; ids unique; four distinct options, exactly one keyed correct.
  Arithmetic: every equation chain in the advice and in the key ("a = b = c", "a ≈ b") holds, a written decimal to its
    own places. A muppet's deliberate wrong sum is in MUPPET_SUMS with its reason (a stale entry fails), so a slip in
    the working a student reads is caught (spot-the-muppet-t2-009: £1,000 × 1.05 × 20 was "£21,050").
  Keys: every item is in KEYS (its answer recomputed here from the item's own givens) or CONCEPT (no numeric answer;
    reviewed, with a reason), so a new item cannot skip review. The key states each value at the places it is written.
  SR-16 (a true statement is never a wrong option): no distractor ends on the key's value(s) (spot-the-muppet-t2-002,
    t2-003: the right value by a wrong method).
  Stated conventions: the topic field is never shown, so an item whose key depends on a convention says it in the
    advice (CONVENTIONS; spot-the-muppet-t2-001: core_004 never said compound, so simple interest was true).
  The loan (Jon, 8 Oct 2026; spot-the-muppet-t2-006): the advice says APR; the key states the monthly rate, the
    payment and the total to the penny, recomputed as a repayment loan (APR the effective annual rate, interest only on
    what is still owed); the distractors are the muppet's £333.33 and the two old keys, each with its method named
    (compound or simple interest on the whole sum for 3 years).
  Jokes: core_003 no longer prescribes televisions to patients (spot-the-muppet-t2-008, SR-14 tier (c)).
  Arguments: a muppet's argument the key condemns must be invalid. core_002 (spot-the-muppet-t2-004): the advice may
    not compare the extra volume's price with the small bottle's price for its volume (a valid marginal argument).
  Chromium: every item played three ways: the key first (scores 1, logged once, attempts 1); a wrong pick then the key
    (the first pick marks nothing; scores 1, logged once, attempts 2); two wrong picks (scores 0, logged once, the key
    revealed; then every option clicked and pressed with Enter changes nothing). With MaffsLock's real fresh window
    (spot-the-muppet-t2-005): Next's second click landing on the new question's option marks nothing; a double click on
    Next moves on once; a double click on a first wrong pick spends one pick; the session ends once.
KNOWN_OPEN holds register entries this script detects but this PR does not fix (reported, never failed; a stale one fails).
A self-test plants eight faults back into a copy of the page; each must FAIL naming its entry.

    python scripts/verify-spot-the-muppet.py [--no-selftest] [--against FILE]
"""
import argparse
import math
import os
import re
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'spot-the-muppet'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNTS = {'ks3': 18, 'gcse': 20, 'core': 12}
TAG = 'spot-the-muppet-'


def amortised(p, apr, months):
    """The monthly repayment of a loan of p at an annual percentage rate apr, repaid over months."""
    r = (1 + apr) ** (1 / 12) - 1
    return p * r / (1 - (1 + r) ** -months)


# Every item with a numeric answer: the values the key must state, recomputed from the item's own givens.
KEYS = {
    'stm_ks3_001': (F(30, 100) * 80,),                       # 30% of 80
    'stm_ks3_002': (F(60, 5) * 2, F(60, 5) * 3),             # 60 in 2:3
    'stm_ks3_003': (F(1, 2) + F(1, 3),),
    'stm_ks3_004': (F(400) * F(11, 10) * F(9, 10),),         # up 10% then down 10%
    'stm_ks3_005': (F(3 + 7 + 8 + 2 + 10, 5),),
    'stm_ks3_006': (F(300, 4) * 7,),
    'stm_ks3_007': (F(1, 2) * 8 * 5,),
    'stm_ks3_008': ((1 - F(8, 10) * F(7, 10)) * 100,),       # 20% then 30% off: the total % off
    'stm_ks3_009': (F(16 * 2),),                             # doubling
    'stm_ks3_010': (F(3, 4) * 48,),
    'stm_ks3_011': (F(3 * 25000, 100),),                     # 3 cm at 1:25,000, in metres
    'stm_ks3_012': (F(180 - 80 - 60),),
    'stm_ks3_013': (F(24 * 15),),
    'stm_ks3_015': (F(2 * (9 + 4)),),
    'stm_ks3_016': (F(350, 7) * 2, F(350, 7) * 5),
    'stm_ks3_018': (F(3), F(7)),                             # the two modes
    'stm_gcse_001': (F(85) / F(85, 100),),
    'stm_gcse_002': (F(500) * F(104, 100) ** 3,),
    'stm_gcse_003': (F(3), F(4)),                            # 2x + y = 10, x + y = 7
    'stm_gcse_004': (F(50, 200) * 100,),
    'stm_gcse_005': (1 - F(5, 6) ** 6,),
    'stm_gcse_006': (F(240, 100) + F(5, 100),),              # 2.4 m to the nearest 10 cm: upper bound
    'stm_gcse_007': (F(5), F(-5)),
    'stm_gcse_008': (F(715, 650), F(480, 400)),              # pence per gram, 650 g and 400 g
    'stm_gcse_010': (F(5),),                                 # |(3, 4)|
    'stm_gcse_011': (math.pi * 5 ** 2,),
    'stm_gcse_012': (F(7 - 3, 6 - 2),),
    'stm_gcse_014': (math.degrees(math.asin(0.6)),),
    'stm_gcse_017': (F(13),),                                # sqrt(5^2 + 12^2)
    'stm_gcse_018': (F(1, 2) * F(1, 6),),
    'stm_gcse_020': (F(4), F(2)),                            # 3x + 2y = 16, x + 2y = 8
    'stm_core_001': (F(10) * F(1, 10) - 2,),                 # expected profit per game
    'stm_core_002': (F(350, 500), F(480, 750)),              # pence per ml, 500 ml and 750 ml
    'stm_core_004': (1000 * 1.05 ** 20,),                    # compound, 20 years
    'stm_core_005': (F(40), F(60)),
    'stm_core_007': (F(60 * 25 + 80 * 75, 100),),
    'stm_core_008': (F(120) / F(120, 100),),
    'stm_core_009': (F(2000, 15 - 5),),
    'stm_core_012': (amortised(12000, 0.06, 36),),           # the monthly repayment
}

# Items with no numeric answer to recompute: reviewed (8 Oct 2026), the reason the key is the one true option.
CONCEPT = {
    'stm_ks3_014': 'independent flips: P(tails) stays 0.5 (gambler\'s fallacy)',
    'stm_ks3_017': '3,400,000 = 3.4 x 10^6; the first number must be at least 1 and less than 10',
    'stm_gcse_009': 'x^3 x x^4 = x^7: add the indices',
    'stm_gcse_013': 'x^2 + 5x + 6 = (x + 2)(x + 3)',
    'stm_gcse_015': '(x + 3)^2 = x^2 + 6x + 9',
    'stm_gcse_016': '5, 8, 11, 14: nth term 3n + 2',
    'stm_gcse_019': '(3 x 10^4)(2 x 10^3) = 6 x 10^7',
    'stm_core_003': 'TVs and life expectancy: wealth drives both',
    'stm_core_006': 'an index of 115 is a 15% rise on the base year, not a price',
    'stm_core_010': 'a least-squares line passes through the mean point, not the origin',
    'stm_core_011': 'bias towards heads is a one-tailed test',
}

# A muppet's deliberate wrong sum in the advice: (item, the equation as written) -> why it is wrong on purpose.
MUPPET_SUMS = {
    ('stm_ks3_003', '½ + ⅓ = 2/5'): 'adds the tops and the bottoms',
    ('stm_gcse_019', '(3 × 10⁴) × (2 × 10³) = 6 × 10¹²'): 'multiplies the powers',
}

# The topic field is never shown: a convention the key depends on is said in the advice.
CONVENTIONS = {
    'stm_core_004': ('compound', TAG + 't2-001'),
    'stm_gcse_002': ('compound', None),
}

# A distractor ending on the key's value: the register entry it was filed as.
SR16_ENTRY = {'stm_core_008': TAG + 't2-002', 'stm_ks3_005': TAG + 't2-003'}

# Register entries detected here and left open by this PR (Jon's call): reported, never failed. Stale fails.
KNOWN_OPEN = {}

# The loan (Jon, 8 Oct 2026; spot-the-muppet-t2-006): APR is the effective annual rate, repaid monthly on the shrinking
# balance. The key states the payment and the total to the penny; each distractor is one named figure, with its method.
LOAN = {'stm_core_012': (12000, 0.06, 36, TAG + 't2-006')}


def loan_distractors(p, apr, months):
    """(figure, the word naming its method, places as written): the old keys and the muppet's own figure."""
    return [(F(p) / months, 'is correct', 2),                                   # Lenny: no interest
            (F(p) * (1 + F(apr).limit_denominator()) ** 3 / months, 'compound', 0),  # the whole sum, compounded 3 years
            (F(p) * (1 + F(apr).limit_denominator() * 3) / months, 'simple', 2)]     # the whole sum, simple, 3 years


def check_loan(fails, q, p, apr, months, tag):
    pay = amortised(p, apr, months)
    key = next(o['text'] for o in q['options'] if o['correct'])
    if 'apr' not in q['advice'].lower():
        fails.append('%s %s: the advice does not say APR, the convention the key\'s repayment depends on: "%s"'
                     % (tag, q['id'], q['advice']))
    got = numbers(key)
    for what, v in (('the monthly payment', pay), ('the total repaid', pay * months)):
        if not any(g[1] == 2 and same(g, v) for g in got):
            fails.append('%s %s: the key does not state %s, %.2f to the penny (APR %g%%, %d months, on the shrinking '
                         'balance): "%s"' % (tag, q['id'], what, v, apr * 100, months, key))
    rate = (1 + apr) ** (1 / 12) - 1
    if not any(same(g, rate * 100) for g in got if g[1] == 3):
        fails.append('%s %s: the key does not state the monthly rate, %.3f%%: "%s"' % (tag, q['id'], rate * 100, key))
    wrong = [o['text'] for o in q['options'] if not o['correct']]
    for v, word, places in loan_distractors(p, apr, months):
        hit = [t for t in wrong if word in t and any(g[1] == places and same(g, v) for g in numbers(t))]
        if len(hit) != 1:
            fails.append('%s %s: no single distractor gives %s a month (%s) with its method named: %s'
                         % (tag, q['id'], round(float(v), places), word, wrong))

# ---------------------------------------------------------------------------------------------------- arithmetic
SUPS = dict(zip('⁰¹²³⁴⁵⁶⁷⁸⁹', '0123456789'))
VULGAR = {'½': F(1, 2), '⅓': F(1, 3), '⅔': F(2, 3), '¼': F(1, 4), '¾': F(3, 4), '⅕': F(1, 5), '⅖': F(2, 5),
          '⅗': F(3, 5), '⅘': F(4, 5), '⅙': F(1, 6), '⅚': F(5, 6), '⅛': F(1, 8), '⅜': F(3, 8), '⅝': F(5, 8), '⅞': F(7, 8)}
UNITS = {'cm', 'm', 'km', 'ml', 'g', 'kg', 'p', 'mph', 'kWh'}
NUM_RE = re.compile(r'\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?')


def tokens(text):
    """[(kind, value, start, end)]: NUM, OP, LP, RP, SUP, SQRT, PI, EQ, UNIT (a unit glued to a number), ALG (a
    variable glued to a number), WORD, BREAK. £ is dropped; % is a unit."""
    out, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if c.isspace() or c == '£':
            i += 1
            continue
        m = NUM_RE.match(text, i)
        if m and not (i and text[i - 1].isalpha()):
            out.append(('NUM', F(m.group().replace(',', '')), i, m.end()))
            i = m.end()
            continue
        if c in VULGAR:
            out.append(('NUM', VULGAR[c], i, i + 1)); i += 1; continue
        if c in SUPS and out and out[-1][0] in ('NUM', 'RP', 'PI') and out[-1][3] == i:
            j = i
            while j < n and text[j] in SUPS:
                j += 1
            out.append(('SUP', int(''.join(SUPS[ch] for ch in text[i:j])), i, j)); i = j; continue
        if c.isalpha() or c in SUPS or c in '⁻̄':
            j = i
            while j < n and (text[j].isalpha() or text[j] in SUPS or text[j] in '⁻̄'):
                j += 1
            word = text[i:j]
            if word == 'π':
                out.append(('PI', None, i, j))
            elif out and out[-1][0] == 'NUM' and out[-1][3] == i:
                out.append(('UNIT' if word in UNITS else 'ALG', word, i, j))
            else:
                out.append(('WORD', word, i, j))
            i = j
            continue
        kind = {'+': 'OP', '-': 'OP', '−': 'OP', '×': 'OP', '÷': 'OP', '/': 'OP', '(': 'LP', ')': 'RP', '√': 'SQRT',
                '=': 'EQ', '≈': 'EQ', '%': 'UNIT'}.get(c, 'BREAK')
        out.append((kind, c, i, i + 1))
        i += 1
    return out


class Parse:
    def __init__(self, toks):
        self.t, self.i = toks, 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else (None, None, 0, 0)

    def take(self):
        self.i += 1
        return self.t[self.i - 1]

    def expr(self):
        v = self.term()
        while self.peek()[0] == 'OP' and self.peek()[1] in '+-−':
            op = self.take()[1]
            w = self.term()
            v = v + w if op == '+' else v - w
        return v

    def term(self):
        v = self.factor()
        while True:
            k, val = self.peek()[:2]
            if k == 'OP' and val in '×÷/':
                self.take()
                w = self.factor()
                v = v * w if val == '×' else v / w
            elif k in ('LP', 'PI', 'SQRT'):        # implicit multiplication: 2(3), 2π
                v = v * self.factor()
            else:
                return v

    def factor(self):
        if self.peek()[0] == 'OP' and self.peek()[1] in '-−':
            self.take()
            return -self.factor()
        v = self.atom()
        while self.peek()[0] == 'SUP':
            v = v ** self.take()[1]
        return v

    def atom(self):
        k = self.peek()[0]
        if k == 'NUM':
            return self.take()[1]
        if k == 'PI':
            self.take()
            return math.pi
        if k == 'SQRT':
            self.take()
            v = self.atom()
            while self.peek()[0] == 'SUP':
                v = v ** self.take()[1]
            return math.sqrt(v)
        if k == 'LP':
            self.take()
            v = self.expr()
            if self.take()[0] != 'RP':
                raise ValueError('bracket')
            return v
        raise ValueError('atom')


def evaluate(toks, givens=''):
    """(value, places, rel) of a piece: places is the written decimal places when the piece is one written decimal
    (a vulgar fraction is exact: None), else None; rel is the relative rounding a decimal in the piece carries when
    that decimal is not one of the item's givens (an intermediate rounded by the writer, as 1.05²⁰ = 2.653)."""
    if not toks or any(t[0] in ('ALG',) for t in toks):
        return None
    body = [t for t in toks if t[0] != 'UNIT']
    p = Parse(body)
    try:
        v = p.expr()
    except (ValueError, ZeroDivisionError, IndexError, TypeError):
        return None
    if p.i != len(body):
        return None
    lit = [t for t in body if t[0] != 'OP']
    places = None
    if len(lit) == 1 and lit[0][0] == 'NUM' and all(t[0] == 'OP' and t[1] in '-−' for t in body[:-1]):
        s = NUM_RE.match(TEXT[0], lit[0][2])
        places = (len(s.group().split('.')[1]) if '.' in s.group() else 0) if s else None
    rel = 0.0
    for t in body:
        w = TEXT[0][t[2]:t[3]] if t[0] == 'NUM' else ''
        if '.' in w and w not in givens and t[1]:
            rel = max(rel, 0.5 / 10 ** len(w.split('.')[1]) / abs(float(t[1])))
    return v, places, rel


TEXT = ['']   # the text being parsed, for a literal's written places


def equations(text, givens=None):
    """[(written, [pieces as (value, places, rel) or None])]: every chain of pieces joined by = or ≈ in text. givens is
    the item's own text (the advice): a decimal in it is a given, never a rounded intermediate (default: text)."""
    givens = text if givens is None else givens
    TEXT[0] = text
    toks = tokens(text)
    out, run = [], []
    for t in toks + [('BREAK', None, len(text), len(text))]:
        if t[0] in ('NUM', 'OP', 'LP', 'RP', 'SUP', 'SQRT', 'PI', 'EQ', 'UNIT', 'ALG'):
            run.append(t)
            if t[0] in ('UNIT', 'ALG'):
                out.append(run); run = []
            continue
        if run:
            out.append(run)
        run = []
    chains = []
    for run in out:
        if not any(t[0] == 'EQ' for t in run):
            continue
        pieces, cur = [], []
        for t in run:
            if t[0] == 'EQ':
                pieces.append(cur); cur = []
            else:
                cur.append(t)
        pieces.append(cur)
        before = text[:run[0][2]].rstrip('£')
        vals = [evaluate(p, givens) for p in pieces]
        # money: a piece written in pounds (£) equal to one in pence (a glued "p") compares in pence
        pounds = ['£' in text[max(0, p[0][2] - 1):p[-1][3]] if p else False for p in pieces]
        pence = [any(t[0] == 'UNIT' and t[1] == 'p' for t in p) for p in pieces]
        if any(pounds) and any(pence):
            vals = [(v[0] * 100,) + tuple(v[1:]) if v and pd else v for v, pd in zip(vals, pounds)]
        glued = before and (before[-1].isalpha() or before[-1] in SUPS or before[-1] in '⁻')
        if glued or re.search(r'\b(of|year)\s*$', before):
            vals[0] = None                       # "cos⁻¹(0.6) = ...", "10% of £440 = £44": the first piece is a fragment
        chains.append((text[run[0][2]:run[-1][3]].strip(), vals))
    return chains


def holds(a, b):
    """a = b as written: a written decimal to its own places; two expressions within the rounding of an intermediate
    decimal the writer rounded (rel), else exactly."""
    tol = max([F(1, 2 * 10 ** x[1]) for x in (a, b) if x[1] is not None] or [0])
    if a[1] is None and b[1] is None:
        tol = max(a[2], b[2]) * abs(float(b[0]))
    return abs(float(a[0]) - float(b[0])) <= float(tol) + 1e-9 * max(1, abs(float(b[0])))


def numbers(text):
    """Every number written in text, in order: £ and units dropped, a minus glued to it kept, a/b and ½ read."""
    out = []
    for m in re.finditer(r'([−-])?£?(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)(?:/(\d+))?|([%s])' % ''.join(VULGAR), text):
        if m.group(4):
            out.append((VULGAR[m.group(4)], None)); continue
        if m.start() and text[m.start() - 1].isalpha():
            continue
        v = F(m.group(2).replace(',', ''))
        places = len(m.group(2).split('.')[1]) if '.' in m.group(2) else 0
        if m.group(3):
            v, places = v / int(m.group(3)), None
        out.append((-v if m.group(1) else v, places))
    return out


def same(written, exact):
    """written (value, places) states exact: exactly, or rounded to its places. A whole number under 10 never stands
    for a value that is not whole (the 1 in "not 1" is not 0.665 rounded)."""
    v, places = written
    if places is None or abs(float(exact) - round(float(exact))) < 1e-9:
        return abs(float(v) - float(exact)) <= 1e-9 * max(1, abs(float(exact)))
    if places == 0 and abs(float(exact)) < 10:
        return False
    return abs(float(v) - float(exact)) <= 0.5 / 10 ** places + 1e-9 * max(1, abs(float(exact)))


def check_bank(fails, opens, bank):
    counts = {lv: sum(1 for q in bank if q['level'] == lv) for lv in COUNTS}
    if counts != COUNTS:
        fails.append('bank: %s items by level, expected %s' % (counts, COUNTS))
    ids = [q['id'] for q in bank]
    if len(set(ids)) != len(ids):
        fails.append('bank: duplicate ids')
    seen_sums, open_seen = set(), set()
    for q in bank:
        qid, opts = q['id'], q['options']
        keys = [o for o in opts if o['correct']]
        if len(opts) != 4 or len(keys) != 1 or len({o['text'] for o in opts}) != 4:
            fails.append('%s: %d options, %d keyed correct, %d distinct (4, 1, 4)' % (qid, len(opts), len(keys), len({o['text'] for o in opts})))
            continue
        key = keys[0]['text']
        # arithmetic in the advice and the key
        for where, text in (('advice', q['advice']), ('key', key)):
            for written, vals in equations(text, q['advice']):
                for a, b in zip(vals, vals[1:]):
                    if a is None or b is None or holds(a, b):
                        continue
                    if where == 'advice' and (qid, written) in MUPPET_SUMS:
                        seen_sums.add((qid, written))
                        continue
                    tag = TAG + 't2-009 ' if qid == 'stm_core_004' else ''
                    fails.append('%s%s: the %s says "%s", which does not hold (%s vs %s)'
                                 % (tag, qid, where, written, round(float(a[0]), 4), round(float(b[0]), 4)))
        # the key's values, recomputed
        if qid in KEYS:
            want = KEYS[qid]
            got = numbers(key)
            missing = [w for w in want if not any(same(g, w) for g in got)]
            # each value as the key writes it (for SR-16: a distractor equal to that, not merely near the exact value)
            written = [next((g[0] for g in got if same(g, w)), None) for w in want]
            if missing:
                if qid in KNOWN_OPEN:
                    open_seen.add(qid)
                    opens.append('%s %s: %s' % (KNOWN_OPEN[qid][0], qid, KNOWN_OPEN[qid][1]))
                else:
                    fails.append('%s: the key does not state %s (recomputed from the item): "%s"'
                                 % (qid, ', '.join(str(round(float(w), 4)) for w in missing), key))
            # SR-16: no distractor ends on the key's value(s)
            for o in opts:
                if o['correct']:
                    continue
                tail = numbers(o['text'])[-len(want):]
                if None not in written and len(tail) == len(want) and all(g[0] == w for g, w in zip(tail, written)):
                    tag = SR16_ENTRY.get(qid, 'SR-16')
                    fails.append('%s %s: the distractor "%s" ends on the key\'s value %s, by a wrong method; a true '
                                 'statement is never a wrong option' % (tag, qid, o['text'], ', '.join(str(float(w)) for w in want)))
        elif qid not in CONCEPT:
            fails.append('%s: in neither KEYS nor CONCEPT: recompute its answer, or review it and give the reason' % qid)
        # conventions said in the advice
        if qid in CONVENTIONS:
            word, tag = CONVENTIONS[qid]
            if word not in q['advice'].lower():
                fails.append('%s%s: the key depends on %s interest, but the advice never says so (the topic field is '
                             'not shown), so a true simple-interest statement is marked wrong: "%s"'
                             % (tag + ' ' if tag else '', qid, word, q['advice']))
        # a muppet's "is correct — V" repeats the advice's own V
        for o in opts:
            if not o['correct'] and re.search(r' is correct \u2014', o['text']):
                adv = numbers(q['advice'])
                for g in numbers(o['text']):
                    if not any(same(a, g[0]) and a[1] == g[1] for a in adv):
                        fails.append('%s: "%s" states %s, which the advice never says' % (qid, o['text'], float(g[0])))
    for q in bank:
        if q['id'] in LOAN:
            check_loan(fails, q, *LOAN[q['id']])
    # core_003 (Jon, 8 Oct 2026; spot-the-muppet-t2-008, SR-14 tier (c)): the joke is a bigger telly, not patients
    for q in bank:
        if q['id'] == 'stm_core_003' and re.search(r'patient|prescrib', q['advice'], re.I):
            fails.append('%s stm_core_003: the advice still prescribes televisions to patients (SR-14 tier (c)): "%s"'
                         % (TAG + 't2-008', q['advice']))
    # core_002: the muppet's argument must be invalid (spot-the-muppet-t2-004)
    for q in bank:
        if q['id'] != 'stm_core_002':
            continue
        extra = re.search(r'£([\d.]+) for (\d+)ml extra', q['advice'])
        small = re.search(r'paying £([\d.]+) for (\d+)ml', q['advice'])
        if extra and small and F(extra.group(1)) / int(extra.group(2)) < F(small.group(1)) / int(small.group(2)):
            fails.append('%s %s: the advice compares %sp/ml for the extra %sml with %sp/ml for the small bottle: a valid '
                         'marginal argument, which the key calls the wrong method'
                         % (TAG + 't2-004', q['id'], float(F(extra.group(1)) * 100 / int(extra.group(2))), extra.group(2),
                            float(F(small.group(1)) * 100 / int(small.group(2)))))
    for k in set(MUPPET_SUMS) - seen_sums:
        fails.append('MUPPET_SUMS %s "%s" is stale: no such wrong sum in the advice' % k)
    for qid in set(KNOWN_OPEN) - open_seen:
        fails.append('KNOWN_OPEN %s (%s) no longer reproduces: close it in the register and remove it here' % (qid, KNOWN_OPEN[qid][0]))


# ---------------------------------------------------------------------------------------------------- Chromium
INIT = r"""(() => {
  try { localStorage.clear(); } catch (e) {}
  window.__ev = [];
  let inner;
  Object.defineProperty(window, 'mfg', { configurable: true,
    get() { return function (e, p) { window.__ev.push([e, p]); return inner && inner.apply(this, arguments); }; },
    set(v) { inner = v; } });
})();"""

LOAD = """([lv, ids]) => {
  window.__ev.length = 0;
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.getElementById('startScreen').classList.add('active');
  currentLevel = lv; sessionLength = ids.length;
  startGame();
  sessionQuestions = ids.map(id => QUESTIONS.find(q => q.id === id));
  currentIndex = 0; score = 0;
  document.getElementById('scoreNum').textContent = '0';
  showQuestion();
  window.__ev.length = 0;
}"""

STATE = """() => ({score: score, idx: currentIndex,
  qa: window.__ev.filter(e => e[0] === 'question_answered').map(e => e[1]),
  done: window.__ev.filter(e => e[0] === 'game_completed').length,
  marked: document.querySelectorAll('#optionsGrid .option-card.correct, #optionsGrid .option-card.incorrect').length,
  open: [...document.querySelectorAll('#optionsGrid .option-card')].filter(c => !c.disabled && !c.classList.contains('disabled')).length})"""

PICK = """(want) => { const q = sessionQuestions[currentIndex];
  const c = [...document.querySelectorAll('#optionsGrid .option-card')].find(c => !c.disabled
    && !c.classList.contains('disabled') && q.options.find(o => o.text === c.textContent).correct === want);
  c.click(); return c.textContent; }"""

AGAIN = """() => { document.querySelectorAll('#optionsGrid .option-card').forEach(c => {
  c.click(); c.focus();
  ['keydown', 'keypress', 'keyup'].forEach(t => c.dispatchEvent(new KeyboardEvent(t, {key: 'Enter', bubbles: true})));
  c.click(); }); }"""


def new_page(browser, base, html, fresh_zero):
    ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
    ctx.add_init_script(INIT)
    if fresh_zero:
        ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    pat = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda u: not u.startswith(base), lambda r: r.abort())
    ctx.route(lambda u: bool(pat.search(u)), lambda r: r.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
    page.wait_for_function("typeof QUESTIONS !== 'undefined' && typeof startGame === 'function'", timeout=8000)
    return ctx, page, errors


def sweep(fails, page, bank):
    """Every item: right first; wrong then right; wrong twice, then every option again."""
    for q in bank:
        qid, lv = q['id'], q['level']
        other = next(x['id'] for x in bank if x['level'] == lv and x['id'] != qid)
        # right first
        page.evaluate(LOAD, [lv, [qid, other]])
        page.evaluate(PICK, True)
        s = page.evaluate(STATE)
        if s['score'] != 1 or len(s['qa']) != 1 or not s['qa'][0]['correct'] or s['qa'][0].get('attempts') != 1:
            fails.append('%s: its key, picked first: score %d, logged %s (1; once, correct, attempts 1)' % (qid, s['score'], s['qa']))
        # wrong, then right
        page.evaluate(LOAD, [lv, [qid, other]])
        page.evaluate(PICK, False)
        s = page.evaluate(STATE)
        if s['score'] != 0 or s['qa'] or s['open'] != 3:
            fails.append('answer once %s: a first wrong pick (a retry) logged %s, score %d, %d options left (nothing, 0, 3)'
                         % (qid, s['qa'], s['score'], s['open']))
        page.evaluate(PICK, True)
        s = page.evaluate(STATE)
        if s['score'] != 1 or len(s['qa']) != 1 or not s['qa'][0]['correct'] or s['qa'][0].get('attempts') != 2:
            fails.append('%s: a wrong pick then its key: score %d, logged %s (1; once, correct, attempts 2)' % (qid, s['score'], s['qa']))
        # wrong twice, then every option clicked and pressed with Enter
        page.evaluate(LOAD, [lv, [qid, other]])
        page.evaluate(PICK, False)
        page.evaluate(PICK, False)
        s0 = page.evaluate(STATE)
        if s0['score'] != 0 or len(s0['qa']) != 1 or s0['qa'][0]['correct'] or s0['open']:
            fails.append('%s: two wrong picks: score %d, logged %s, %d options open (0; once, wrong; none)'
                         % (qid, s0['score'], s0['qa'], s0['open']))
        revealed = page.evaluate("() => { const q = sessionQuestions[currentIndex]; return [...document.querySelectorAll('#optionsGrid .option-card.correct')].map(c => q.options.find(o => o.text === c.textContent).correct); }")
        if revealed != [True]:
            fails.append('%s: after two wrong picks the revealed option(s) are %s (the key, once)' % (qid, revealed))
        page.evaluate(AGAIN)
        s1 = page.evaluate(STATE)
        if (s1['score'], len(s1['qa']), s1['done']) != (s0['score'], len(s0['qa']), s0['done']):
            fails.append('%s %s: clicking and pressing Enter on the marked question\'s options changed score %d -> %d, '
                         'question_answered %d -> %d' % (TAG + 't2-005', qid, s0['score'], s1['score'], len(s0['qa']), len(s1['qa'])))


def next_shown(page):
    page.wait_for_function("() => document.getElementById('nextBtn').style.display === 'block'", timeout=8000)


def lock_window(fails, page, bank):
    """With MaffsLock's real fresh window (spot-the-muppet-t2-005)."""
    tag = TAG + 't2-005'
    gcse = [q['id'] for q in bank if q['level'] == 'gcse']
    # Next's second click lands on the new question's option
    page.evaluate(LOAD, ['gcse', gcse[:3]])
    page.wait_for_timeout(350)
    page.evaluate(PICK, True)
    next_shown(page)
    before = page.evaluate(STATE)
    page.evaluate("() => { document.getElementById('nextBtn').click(); document.querySelector('#optionsGrid .option-card').click(); }")
    after = page.evaluate(STATE)
    if after['idx'] != 1 or after['marked'] or len(after['qa']) != len(before['qa']) or after['open'] != 4:
        fails.append('%s: the second click of a double click on Next, landing on the new question\'s option, %s'
                     % (tag, 'answered it unseen (logged %s)' % after['qa'][len(before['qa']):] if len(after['qa']) > len(before['qa'])
                        else 'spent a pick (%d of 4 options open)' % after['open']))
    # a real double click on Next: one advance
    page.evaluate(LOAD, ['gcse', gcse[:3]])
    page.wait_for_timeout(350)
    page.evaluate(PICK, True)
    next_shown(page)
    page.dblclick('#nextBtn')
    page.wait_for_timeout(100)
    s = page.evaluate(STATE)
    if s['idx'] != 1 or s['marked']:
        fails.append('%s: a double click on Next moved %d questions and marked %d options (1, 0)' % (tag, s['idx'], s['marked']))
    # a double click on a first wrong pick spends one pick
    page.wait_for_timeout(350)
    page.evaluate('() => { window.__ev.length = 0; }')
    wrong = page.evaluate("() => { const q = sessionQuestions[currentIndex]; return [...document.querySelectorAll('#optionsGrid .option-card')].findIndex(c => !q.options.find(o => o.text === c.textContent).correct); }")
    page.dblclick('#optionsGrid .option-card >> nth=%d' % wrong)
    page.wait_for_timeout(100)
    s = page.evaluate(STATE)
    if s['open'] != 3 or s['qa']:
        fails.append('answer once: a double click on a first wrong pick left %d options open and logged %s (3, nothing)' % (s['open'], s['qa']))
    # the session ends once
    page.evaluate(LOAD, ['gcse', gcse[:1]])
    page.wait_for_timeout(350)
    page.evaluate(PICK, True)
    next_shown(page)
    page.evaluate("() => { const b = document.getElementById('nextBtn'); b.click(); b.click(); nextQuestion(); }")
    s = page.evaluate(STATE)
    if s['done'] != 1:
        fails.append('the session ended %d times (once: game_completed and submitScore)' % s['done'])


def run(html):
    from playwright.sync_api import sync_playwright
    fails, opens = [], []
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx, page, errors = new_page(browser, base, html, True)
            bank = page.evaluate('() => QUESTIONS')
            check_bank(fails, opens, bank)
            sweep(fails, page, bank)
            ctx.close()
            ctx, page, errors2 = new_page(browser, base, html, False)
            lock_window(fails, page, bank)
            ctx.close()
            errs = [e for e in errors + errors2 if 'firebase' not in e.lower()]
            if errs:
                fails.append('page errors: %s' % '; '.join(errs[:3]))
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return fails, opens, bank


V = '\\u2014'
PLANTS = [
    (TAG + 't2-005', 't2-005: no fresh window on a new question',
     "  MaffsLock.fresh(document.getElementById('gameScreen'));\n", ''),
    (TAG + 't2-001', 't2-001: core_004 never says compound',
     '\\u00a31,000 at 5% compound interest for 20 years', '\\u00a31,000 at 5% for 20 years'),
    (TAG + 't2-002', 't2-002: core_008 £120 - £20 = £100',
     'pre-VAT = \\u00a3120 \\u00d7 1.20 = \\u00a3144', 'pre-VAT = \\u00a3120 \\u2212 \\u00a320 = \\u00a3100'),
    (TAG + 't2-003', 't2-003: ks3_005 (2+10)/2 = 6',
     'mean = (3+7+8+2+10) \\u00f7 4 = 7.5', 'mean = (2+10) \\u00f7 2 = 6, same answer, different method'),
    (TAG + 't2-004', 't2-004: core_002 a valid marginal argument',
     'The big one only costs \\u00a31.30 more, and \\u00a31.30 is less than \\u00a33.50, so obviously the big bottle wins.',
     'Difference: \\u00a31.30 for 250ml extra. That\\\'s better than paying \\u00a33.50 for 500ml so obviously big bottle wins.'),
    (TAG + 't2-009', 't2-009: core_004 1,000 x 1.05 x 20 = 21,050',
     '\\u00d7 1.05 \\u00d7 20 = \\u00a321,000.', '\\u00d7 1.05 \\u00d7 20 = \\u00a321,050.'),
    (TAG + 't2-006', 't2-006: core_012 the key gives about £397 a month',
     '\\u2248 \\u00a3364.20 a month (total \\u00a313,111.19)', '\\u2248 \\u00a3397 a month (total \\u00a314,292.19)'),
    (TAG + 't2-008', 't2-008: core_003 prescribing televisions',
     "I\\'m telling everyone I know to buy a bigger telly.", "I\\'m prescribing televisions to all my patients."),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    html = open(args.against or GAME, encoding='utf-8').read()
    fails, opens, bank = run(html)
    print('%s: %d items: every equation in the advice and the keys, every key recomputed, no distractor on the key\'s '
          'value; each item played three ways in Chromium; Next and the fresh window' % (SLUG, len(bank)))
    for o in opens:
        print('open  ' + o)
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-46s *** CANNOT PLANT ***' % what)
                ok = False
                continue
            hit = [f for f in run(html.replace(old, new))[0] if f.startswith(tag)]
            ok = ok and bool(hit)
            print('  self-test %-46s %s' % (what, ('caught: ' + hit[0][:100]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
