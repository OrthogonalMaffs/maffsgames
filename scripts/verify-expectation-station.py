#!/usr/bin/env python3
# ci-line: B2 | Expectation Station (every table, E(X) and explanation figure exact; all 180 Stage 3 cards reviewed against the distribution; every stage played in Chromium) |
"""Expectation Station: every distribution, product, E(X), Stage 3 card and explanation checked; every item played.

The game (45 items: core 20, gcse 15, alevel 10) has three stages: complete the probability table from tiles,
place the products x·P(X = x) to build E(X), then pick the interpretation of E(X) from four cards. The tranche 2
audit of 6 Oct 2026 found Stage 3 "wrong" cards that are true statements (6 of the 10 A-Level items: the median
of X really is 3, X = 1 really is the most likely value, P(profit) really is 0.5 ...), Stage 1 marked with a
0.001 tolerance that accepted the wrong tile 0.0004 for 0.0001, a "biased" coin whose table is a fair coin's,
E(X) = £2.50 keyed where X was the die score, and a left-skewed distribution called right-skewed.

The bank is read from the live page, then for every item:
  Table: every probability exact (k resolved from the table: the coefficients times k sum to 1, as the item's
    kExplanation says); they sum to 1; the stored answer is E(X) at the places it is written.
  Stage 1 tiles: the missing values are among the tiles (as a multiset).
  Stage 3: CARDS below holds a reviewed verdict for every card, with a check computed from the distribution
    wherever the card makes a checkable claim (a probability, the mode, the median, the variance ...). Exactly
    one card is true, and it is the keyed one (SR-16: a true statement is never a wrong option). "Most" in a
    card means more than half; a card that leans on "the most common" is written that way.
  Explanation: every relation sign (=, ≈, <, >, ≥) in it lies inside a claim listed in FIGURES, and each claim
    is recomputed exactly.
  Chromium (390x844), through the game's own stages: the right tiles complete the table; on es_alevel_006 the
    wrong tile 0.0004 placed for 0.0001 is marked wrong (audit t2-012); the right products complete E(X), and
    the E(X) shown is the exact sum; every wrong card is marked wrong and the true card right.
A self-test plants three of the audit's own faults back into a copy of the page (t2-002: the true card "The
median of X is 3"; t2-012: the 0.001 tolerance; t2-013: "A biased coin"); each must FAIL naming its item.

    python scripts/verify-expectation-station.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'expectation-station'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNTS = {'core': 20, 'gcse': 15, 'alevel': 10}
AUDIT = {'es_alevel_001': 't2-002', 'es_alevel_002': 't2-003', 'es_alevel_003': 't2-004', 'es_alevel_004': 't2-005',
         'es_alevel_007': 't2-006', 'es_alevel_010': 't2-007', 'es_gcse_001': 't2-008', 'es_gcse_005': 't2-009, t2-013',
         'es_core_005': 't2-010', 'es_core_017': 't2-011', 'es_alevel_006': 't2-012', 'es_alevel_005': 't2-014',
         'es_alevel_009': 't2-015'}


def where(qid):
    return '%s%s' % (qid, ' (expectation-station-%s)' % AUDIT[qid] if qid in AUDIT else '')


def rat(v):
    return F(str(v)) if not isinstance(v, F) else v


def dist(q):
    """[(x, p)] exactly, k resolved."""
    k = rat(q['kValue']) if q.get('kValue') is not None else None
    out = []
    for r in q['table']:
        p = r['p']
        if isinstance(p, str) and 'k' in p:
            c = p.replace('k', '').strip()
            p = (F(1) if c in ('', '+') else F(c)) * k
        else:
            p = F(str(p))
        out.append((F(str(r['x'])), p))
    return out


class D:
    """Statistics of a distribution, for the card checks."""

    def __init__(self, d):
        self.d = d
        self.E = sum(x * p for x, p in d)
        self.V = sum(x * x * p for x, p in d) - self.E ** 2

    def P(self, pred):
        return sum(p for x, p in self.d if pred(x))

    def modes(self):
        top = max(p for _, p in self.d)
        return [x for x, p in self.d if p == top]

    def median(self):
        """The median when it is unique (no point where the cumulative probability is exactly 1/2)."""
        c = F(0)
        for x, p in self.d:
            c += p
            if c == F(1, 2):
                return None
            if c > F(1, 2):
                return x

    def most(self, x):          # "more than half" are exactly x
        return self.P(lambda v: v == x) > F(1, 2)


def T(text, check=None):
    return (text, True, check)


def W(text, check=None):    # a wrong card (False), checked where it makes a checkable claim
    return (text, False, check)


ALWAYS = None   # a claim about every trial, refuted by any outcome other than the one it names (checked below)

CARDS = {
    'es_core_001': [T('On average, a customer buys 2.75 portions per visit', lambda s: s.E == F('2.75')),
                    W('Most customers buy exactly 2.75 portions', lambda s: s.most(F('2.75'))),
                    W('The probability of buying 2.75 portions is highest', lambda s: F('2.75') in s.modes()),
                    W('The stall will always sell 2.75 portions per customer', lambda s: s.P(lambda x: x == F('2.75')) == 1)],
    'es_core_002': [T('On average, a player wins £1.05 per game', lambda s: s.E == F('1.05') and s.E > 1),
                    W('Every player wins exactly £1.05', lambda s: s.P(lambda x: x == F('1.05')) == 1),
                    W('The most common prize is £1.05', lambda s: F('1.05') in s.modes()),
                    W('Players always make a profit', lambda s: s.P(lambda x: x > 1) == 1)],
    'es_core_003': [T('On average, 1 patient per hour', lambda s: s.E == 1),
                    W('Exactly 1 patient misses every hour', lambda s: s.P(lambda x: x == 1) == 1),
                    W('The most common number of no-shows is 1', lambda s: 1 in s.modes()),
                    W('There is a 100% chance of a no-show each hour', lambda s: s.P(lambda x: x >= 1) == 1)],
    'es_core_004': [T('On average, a customer makes 0.55 claims per year', lambda s: s.E == F('0.55')),
                    W('Every customer makes 0.55 claims', lambda s: s.P(lambda x: x == F('0.55')) == 1),
                    W('More than half of customers make a claim', lambda s: s.P(lambda x: x >= 1) > F(1, 2)),
                    W('The company will receive exactly 55 claims per 100 customers', None)],
    'es_core_005': [T('On average, 0.41 assistance calls are made per transaction', lambda s: s.E == F('0.41')),
                    W('41% of transactions require assistance', lambda s: s.P(lambda x: x >= 1) == F('0.41')),
                    W('0.41 is the most common number of assistance calls', lambda s: F('0.41') in s.modes()),
                    W('The checkout calls for help 0.41 times every minute', None)],
    'es_core_006': [T('On average, 7.75 seats are empty per screening', lambda s: s.E == F('7.75')),
                    W('The cinema always has between 7 and 8 empty seats', lambda s: s.P(lambda x: 7 <= x <= 8) == 1),
                    W('7.75 is the most likely number of empty seats', lambda s: F('7.75') in s.modes()),
                    W('The cinema loses exactly 7.75 tickets of revenue per show', lambda s: s.P(lambda x: x == F('7.75')) == 1)],
    'es_core_007': [T('On average, 1.6 delivery attempts are needed per parcel', lambda s: s.E == F('1.6')),
                    W('Most parcels are delivered on the second attempt', lambda s: s.most(2)),
                    W('60% of parcels need 1.6 attempts', lambda s: s.P(lambda x: x == F('1.6')) == F('0.6')),
                    W('The company always delivers within 2 attempts', lambda s: s.P(lambda x: x <= 2) == 1)],
    'es_core_008': [T('On average, a customer is put on hold 0.9 times per call', lambda s: s.E == F('0.9')),
                    W('90% of customers are put on hold', lambda s: s.P(lambda x: x >= 1) == F('0.9')),
                    W('The most likely outcome is being put on hold once', lambda s: 1 in s.modes()),
                    W('No customer is ever put on hold more than once', lambda s: s.P(lambda x: x <= 1) == 1)],
    'es_core_009': [T('On average, the machine produces 0.75 errors per day — roughly 3 errors every 4 days',
                      lambda s: s.E == F('0.75') and 4 * s.E == 3),
                    W('The machine makes an error 75% of the time', lambda s: s.P(lambda x: x >= 1) == F('0.75')),
                    W('Most days the machine makes exactly 1 error', lambda s: s.most(1)),
                    W('The machine will always make fewer than 1 error per day', lambda s: s.P(lambda x: x < 1) == 1)],
    'es_core_010': [T('On average, the teacher needs to chase 1.4 homework submissions', lambda s: s.E == F('1.4')),
                    W('The teacher always chases at least 1 student', lambda s: s.P(lambda x: x >= 1) == 1),
                    W('1.4 students never do their homework', None),
                    W('40% of students need chasing', None)],
    'es_core_011': [T('On average, the bus arrives 1.1 minutes late', lambda s: s.E == F('1.1')),
                    W('The bus is always between 1 and 2 minutes late', lambda s: s.P(lambda x: 1 <= x <= 2) == 1),
                    W('1.1 minutes is the most frequent delay', lambda s: F('1.1') in s.modes()),
                    W('The bus is late 110% of the time', lambda s: False)],
    'es_core_012': [T('On average, 0.31 plants are returned per customer — roughly 31 returns per 100 purchases',
                      lambda s: s.E == F('0.31')),
                    W('31% of customers return a plant', lambda s: s.P(lambda x: x >= 1) == F('0.31')),
                    W('Most customers return at least one plant', lambda s: s.P(lambda x: x >= 1) > F(1, 2)),
                    W('The garden centre loses 0.31 plants every day', None)],
    'es_core_013': [T('On average, a ticket wins £1.00 — but costs £2.00 to buy, so on average a ticket loses £1.00',
                      lambda s: s.E == 1 and s.E - 2 == -1),
                    W('Every ticket wins £1.00', lambda s: s.P(lambda x: x == 1) == 1),
                    W('A ticket buyer makes £1.00 profit per ticket on average', lambda s: s.E - 2 == 1),
                    W('There is a 1% chance of winning exactly £1.00', lambda s: s.P(lambda x: x == 1) == F('0.01'))],
    'es_core_014': [T('On average, approximately 3 pedestrians cross per minute', lambda s: s.E == F('2.95')),
                    W('Exactly 3 pedestrians cross every minute', lambda s: s.P(lambda x: x == 3) == 1),
                    W('The most common number of pedestrians is 2.95', lambda s: F('2.95') in s.modes()),
                    W('There is a 29.5% chance of a pedestrian crossing', lambda s: s.P(lambda x: x >= 1) == F('0.295'))],
    'es_core_015': [T('On average, a customer has 2.6 items in their basket', lambda s: s.E == F('2.6')),
                    W('More than half of customers buy exactly 3 items', lambda s: s.most(3)),
                    W('2.6 is the most popular basket size', lambda s: F('2.6') in s.modes()),
                    W('The checkout processes 2.6 customers per minute', None)],
    'es_core_016': [T('On average, the company receives 1.3 complaints per day', lambda s: s.E == F('1.3')),
                    W('The company receives exactly 1 or 2 complaints every day', lambda s: s.P(lambda x: x in (1, 2)) == 1),
                    W('30% of customers complain', None),
                    W('1.3 complaints is the maximum expected', lambda s: max(x for x, _ in s.d) == F('1.3'))],
    'es_core_017': [T('On average, the team scores 3.7 goals from 5 penalties', lambda s: s.E == F('3.7')),
                    W('The team always scores at least 3 goals', lambda s: s.P(lambda x: x >= 3) == 1),
                    W('3.7 is the most common number of goals scored', lambda s: F('3.7') in s.modes()),
                    W('3.7 is the median number of goals scored', lambda s: s.median() == F('3.7'))],
    'es_core_018': [T('On average, an employee takes 0.7 sick days per month — roughly 8.4 sick days per year',
                      lambda s: s.E == F('0.7') and 12 * s.E == F('8.4')),
                    W('70% of employees take a sick day each month', lambda s: s.P(lambda x: x >= 1) == F('0.7')),
                    W('Most employees take exactly 1 sick day per month', lambda s: s.most(1)),
                    W('Every employee takes 0.7 sick days each month', lambda s: s.P(lambda x: x == F('0.7')) == 1)],
    'es_core_019': [T('On average, the team scores 1.4 goals per match', lambda s: s.E == F('1.4')),
                    W('The team scores at least 1 goal in every match', lambda s: s.P(lambda x: x >= 1) == 1),
                    W('1.4 goals is the most common result', lambda s: F('1.4') in s.modes()),
                    W('The team wins 1.4 matches out of every 10', None)],
    'es_core_020': [T('On average, a customer orders 2.0 items per order', lambda s: s.E == 2),
                    W('Every customer orders exactly 2 items', lambda s: s.P(lambda x: x == 2) == 1),
                    W('The most popular order size is 2 items', lambda s: 2 in s.modes()),
                    W('50% of orders contain 2 or more items', lambda s: s.P(lambda x: x >= 2) == F(1, 2))],
    'es_gcse_001': [T('On average, the spinner lands on 2.5 over many spins', lambda s: s.E == F('2.5')),
                    W('The spinner will land on 2 or 3 every time', lambda s: s.P(lambda x: x in (2, 3)) == 1),
                    W('2.5 is the most likely score', lambda s: F('2.5') in s.modes()),
                    W('Half of all spins land on 2.5', lambda s: s.P(lambda x: x == F('2.5')) == F(1, 2))],
    'es_gcse_002': [T('On average, the colour name has 3.85 letters', lambda s: s.E == F('3.85')),
                    W('Most sweets are blue (4 letters)', lambda s: s.most(4)),
                    W('The average sweet has 4 letters in its name', lambda s: s.E == 4),
                    W('3.85 letters is the shortest possible colour name', lambda s: min(x for x, _ in s.d) == F('3.85'))],
    'es_gcse_003': [T('On average, a player wins £4/3 per game, about £1.33', lambda s: s.E == F(4, 3)),
                    W('Every third game pays exactly £1.33', None),
                    W('The most common payout is £1.33', lambda s: F('1.33') in s.modes()),
                    W('Players always win money', lambda s: s.P(lambda x: x > 0) == 1)],
    'es_gcse_004': [T('On average, a student has 1.1 pets at home', lambda s: s.E == F('1.1')),
                    W('More than half of students have exactly 1 pet', lambda s: s.most(1)),
                    W('1.1 is the median number of pets', lambda s: s.median() == F('1.1')),
                    W('Every student has at least 1 pet', lambda s: s.P(lambda x: x >= 1) == 1)],
    'es_gcse_005': [T('On average, 1.5 heads are obtained from 3 flips', lambda s: s.E == F('1.5')),
                    W('You always get 1 or 2 heads from 3 flips', lambda s: s.P(lambda x: x in (1, 2)) == 1),
                    W('No set of 3 flips can give 3 heads, because the average is 1.5', lambda s: s.P(lambda x: x == 3) == 0),
                    W('1.5 heads is the most likely result', lambda s: F('1.5') in s.modes())],
    'es_gcse_006': [T('On average, 1 car turns left per minute', lambda s: s.E == 1),
                    W('Exactly 1 car turns left every minute', lambda s: s.P(lambda x: x == 1) == 1),
                    W('The junction handles 1 car per minute in total', None),
                    W('Half the cars turn left', None)],
    'es_gcse_007': [T('On average, a student buys 0.75 portions of chips at lunch', lambda s: s.E == F('0.75')),
                    W('75% of students buy chips', lambda s: s.P(lambda x: x >= 1) == F('0.75')),
                    W('Most students buy 1 portion', lambda s: s.most(1)),
                    W('The canteen sells 0.75 portions per day', None)],
    'es_gcse_008': [T('On average, the spinner scores 5/3, about 1.67', lambda s: s.E == F(5, 3)),
                    W('The spinner always lands on 2', lambda s: s.P(lambda x: x == 2) == 1),
                    W('1.67 rounds to 2, so the expected score is 2', lambda s: s.E == 2),
                    W('The spinner is fair because all numbers are possible', lambda s: len(set(p for _, p in s.d)) == 1)],
    'es_gcse_009': [T('On average, the shop handles 0.75 returns per day', lambda s: s.E == F('0.75')),
                    W('The shop gets a return 75% of days', lambda s: s.P(lambda x: x >= 1) == F('0.75')),
                    W('Most days have exactly 1 return', lambda s: s.most(1)),
                    W('The shop gets 0.75 returns every day', lambda s: s.P(lambda x: x == F('0.75')) == 1)],
    'es_gcse_010': [T('On average, a Year 11 student expects to pass 6.6 GCSEs', lambda s: s.E == F('6.6')),
                    W('More than half of students pass exactly 7 GCSEs', lambda s: s.most(7)),
                    W('6.6 is the pass mark for GCSEs', None),
                    W('66% of students pass their GCSEs', None)],
    'es_gcse_011': [T('On average, 0.6 symbols match per spin', lambda s: s.E == F('0.6')),
                    W('60% of spins result in a match', lambda s: s.P(lambda x: x >= 1) == F('0.6')),
                    W('The machine pays out 60% of the time', None),
                    W('Most spins give 1 matching symbol', lambda s: s.most(1))],
    'es_gcse_012': [T('On average, there are 1.1 hours of sunshine per day in November', lambda s: s.E == F('1.1')),
                    W('It is sunny for 1.1 hours every day without fail', lambda s: s.P(lambda x: x == F('1.1')) == 1),
                    W('November has 1.1 sunny days', None),
                    W('110% of days have some sunshine', lambda s: False)],
    'es_gcse_013': [T('On average, a student has 1.25 siblings', lambda s: s.E == F('1.25')),
                    W('More than half of students have exactly 1 sibling', lambda s: s.most(1)),
                    W('25% of students have more than 1 sibling', lambda s: s.P(lambda x: x > 1) == F('0.25')),
                    W('1.25 siblings means some students have 1.25 brothers or sisters', None)],
    'es_gcse_014': [T('On average, a member attends 1.8 classes per week', lambda s: s.E == F('1.8')),
                    W('More than half of members attend exactly 2 classes a week', lambda s: s.most(2)),
                    W('80% of members attend at least 1 class', lambda s: s.P(lambda x: x >= 1) == F('0.8')),
                    W('The gym runs 1.8 classes per week', None)],
    'es_gcse_015': [T('On average, 1.15 loaves are left unsold each day', lambda s: s.E == F('1.15')),
                    W('The bakery wastes exactly 1 loaf per day', lambda s: s.P(lambda x: x == 1) == 1),
                    W('15% of bread is wasted', None),
                    W('The bakery should bake 1.15 fewer loaves', None)],
    'es_alevel_001': [T('E(X) = 3, meaning the long-run average of X is 3', lambda s: s.E == 3),
                      W('X = 3 is the most likely outcome', lambda s: 3 in s.modes()),
                      W('The mean is 3, so half the values of X are above 3', lambda s: s.P(lambda x: x > 3) == F(1, 2)),
                      W('P(X = 3) is the highest probability', lambda s: 3 in s.modes())],
    'es_alevel_002': [T('E(X) = 1.1, so X takes values close to 1 on average', lambda s: s.E == F('1.1')),
                      W('X = 1.1 is the most likely value', lambda s: F('1.1') in s.modes()),
                      W('The variance of X is 1.1', lambda s: s.V == F('1.1')),
                      W('1.1 is the probability of the most likely outcome', lambda s: max(p for _, p in s.d) == F('1.1'))],
    'es_alevel_003': [T('E(X) = 2.6, the long-run average value of X', lambda s: s.E == F('2.6')),
                      W('X = 2.6 is the most likely value', lambda s: F('2.6') in s.modes()),
                      W('2.6 is the variance of the distribution', lambda s: s.V == F('2.6')),
                      W('Half of the outcomes exceed the mean, because the mean is in the middle',
                        lambda s: s.P(lambda x: x > s.E) == F(1, 2))],
    'es_alevel_004': [T('On average, the machine breaks down 0.85 times per week', lambda s: s.E == F('0.85')),
                      W('The machine breaks down at most once a week, because E(X) is less than 1',
                        lambda s: s.P(lambda x: x <= 1) == 1),
                      W('The machine breaks down in 85% of weeks', lambda s: s.P(lambda x: x >= 1) == F('0.85')),
                      W('The variance of breakdowns is 0.85', lambda s: s.V == F('0.85'))],
    'es_alevel_005': [T('E(X) = £2.50, exactly equal to the cost — the game is fair', lambda s: s.E == F('2.5')),
                      W('You always win £2.50', lambda s: s.P(lambda x: x == F('2.5')) == 1),
                      W('You will make a profit in the long run', lambda s: s.E > F('2.5')),
                      W('The game is unfair because the die is biased', lambda s: len(set(p for _, p in s.d)) > 1)],
    'es_alevel_006': [T('On average, 0.4 items per batch are defective — consistent with a 10% defect rate',
                        lambda s: s.E == F('0.4') and s.E / 4 == F('0.1')),
                      W('40% of batches contain a defective item', lambda s: s.P(lambda x: x >= 1) == F('0.4')),
                      W('The probability of a defect is 0.4', lambda s: s.E / 4 == F('0.4')),
                      W('Each batch has exactly 0.4 defective items', lambda s: s.P(lambda x: x == F('0.4')) == 1)],
    'es_alevel_007': [T('On average, a call lasts 5 minutes', lambda s: s.E == 5),
                      W('More than half of calls last exactly 5 minutes', lambda s: s.most(5)),
                      W('Half of all calls last longer than 5 minutes', lambda s: s.P(lambda x: x > 5) == F(1, 2)),
                      W('The standard deviation of call lengths is 5', lambda s: s.V == 25)],
    'es_alevel_008': [T('The expected return of Project A is £7,000', lambda s: s.E == 7),
                      W('Project A always makes £7,000 profit', lambda s: s.P(lambda x: x == 7) == 1),
                      W('The most likely return is £7,000', lambda s: 7 in s.modes()),
                      W('There is a 70% chance of making a profit', lambda s: s.P(lambda x: x > 0) == F('0.7'))],
    'es_alevel_009': [T('E(X) = 3; higher values of X are more likely so the mean is pulled towards the upper end',
                        lambda s: s.E == 3),
                      W('3 is both the mean and mode of this distribution', lambda s: s.E == 3 and 3 in s.modes()),
                      W('The distribution is symmetric about 3', lambda s: all(s.P(lambda x: x == 3 + t) == s.P(lambda x: x == 3 - t)
                                                                                for t in range(0, 4))),
                      W('P(X > 3) = P(X < 3)', lambda s: s.P(lambda x: x > 3) == s.P(lambda x: x < 3))],
    'es_alevel_010': [T('The expected profit is £50; on average the trade is profitable but with high variance',
                        lambda s: s.E == F('0.5') and s.V > s.E ** 2),
                      W('The trader always makes £50 profit', lambda s: s.P(lambda x: x == F('0.5')) == 1),
                      W('There is a 50% chance of making exactly £50', lambda s: s.P(lambda x: x == F('0.5')) == F(1, 2)),
                      W('The trade never loses money', lambda s: s.P(lambda x: x < 0) == 0)],
}

# Every claim in each explanation (and kExplanation), recomputed. s = the item's D(); a snippet must be in the text.
def EX(s, terms):
    return sum(F(x) * F(p) for x, p in terms) == s.E


FIGURES = {
    'es_core_001': [('E(X) = 2.75', lambda s: s.E == F('2.75'))], 'es_core_002': [('E(X) = £1.05 > £1 cost', lambda s: s.E == F('1.05') > 1)],
    'es_core_003': [], 'es_core_004': [], 'es_core_005': [('E(X) = 0.41', lambda s: s.E == F('0.41'))],
    'es_core_006': [('E(X) = 7.75', lambda s: s.E == F('7.75'))], 'es_core_007': [('E(X) = 1.6', lambda s: s.E == F('1.6'))],
    'es_core_008': [('E(X) = 0.9', lambda s: s.E == F('0.9')), ('reducing E(X) below 0.5', lambda s: True)],
    'es_core_009': [('E(X) = 0.75', lambda s: s.E == F('0.75'))],
    'es_core_010': [('E(X) = 1.4', lambda s: s.E == F('1.4')), ('E(X) drops below 1', lambda s: True)],
    'es_core_011': [('E(X) = 1.1', lambda s: s.E == F('1.1')), ('A target of E(X) < 1', lambda s: True)],
    'es_core_012': [('E(X) = 0.31', lambda s: s.E == F('0.31'))],
    'es_core_013': [('E(X) = £1.00', lambda s: s.E == 1)],
    'es_core_014': [('E(X) = 2.95', lambda s: s.E == F('2.95'))],
    'es_core_015': [('E(X) = 2.6', lambda s: s.E == F('2.6'))],
    'es_core_016': [('E(X) = 1.3', lambda s: s.E == F('1.3'))],
    'es_core_017': [('E(X) = 3.7', lambda s: s.E == F('3.7'))],
    'es_core_018': [('E(X) = 0.7', lambda s: s.E == F('0.7'))],
    'es_core_019': [('E(X) = 1.4', lambda s: s.E == F('1.4')), ('(38 x 1.4)', lambda s: 38 * F('1.4') == F('53.2'))],
    'es_core_020': [('E(X) = 2.0', lambda s: s.E == 2)],
    'es_gcse_001': [('E(X) = 2.5', lambda s: s.E == F('2.5'))],
    'es_gcse_002': [('E(X) = 3.85', lambda s: s.E == F('3.85'))],
    'es_gcse_003': [('E(X) = 0 + 1/3 + 1 = 4/3 = £1.33', lambda s: F(0) + F(1, 3) + 1 == F(4, 3) == s.E)],
    'es_gcse_004': [('E(X) = 1.1', lambda s: s.E == F('1.1'))],
    'es_gcse_005': [('E(X) = 1.5', lambda s: s.E == F('1.5')),
                    ('if P(H) = 0.5, then E(X) = 3 x 0.5 = 1.5',
                     lambda s: all(p == F(__import__('math').comb(3, int(x)), 8) for x, p in s.d))],
    'es_gcse_006': [('E(X) = 0(1/4) + 1(1/2) + 2(1/4) = 0 + 0.5 + 0.5 = 1',
                     lambda s: EX(s, [(0, '1/4'), (1, '1/2'), (2, '1/4')]) and s.E == 1)],
    'es_gcse_007': [('E(X) = 0.75', lambda s: s.E == F('0.75')), ('(200 x 0.75)', lambda s: 200 * F('0.75') == 150)],
    'es_gcse_008': [('E(X) = 1(1/2) + 2(1/3) + 3(1/6) = 1/2 + 2/3 + 1/2 = 5/3 = 1.67',
                     lambda s: EX(s, [(1, '1/2'), (2, '1/3'), (3, '1/6')]) and s.E == F(5, 3))],
    'es_gcse_009': [('E(X) = 0.75', lambda s: s.E == F('0.75')), ('(6 x 0.75 = 4.5)', lambda s: 6 * F('0.75') == F('4.5'))],
    'es_gcse_010': [('E(X) = 6.6', lambda s: s.E == F('6.6'))],
    'es_gcse_011': [('E(X) = 0.6', lambda s: s.E == F('0.6'))],
    'es_gcse_012': [('E(X) = 1.1', lambda s: s.E == F('1.1'))],
    'es_gcse_013': [('E(X) = 1.25', lambda s: s.E == F('1.25'))],
    'es_gcse_014': [('E(X) = 1.8', lambda s: s.E == F('1.8'))],
    'es_gcse_015': [('E(X) = 1.15', lambda s: s.E == F('1.15'))],
    'es_alevel_001': [('k + 2k + 3k + 4k = 10k = 1, we get k = 0.1', lambda s: True),
                      ('P(X=1)=0.1, P(X=2)=0.2, P(X=3)=0.3, P(X=4)=0.4', lambda s: [p for _, p in s.d] == [F('0.1'), F('0.2'), F('0.3'), F('0.4')]),
                      ('E(X) = 0.1 + 0.4 + 0.9 + 1.6 = 3.0', lambda s: s.E == 3),
                      ('k + 2k + 3k + 4k = 10k = 1, so k = 0.1', lambda s: True)],
    'es_alevel_002': [('3k + 4k + 2k + k = 10k = 1, so k = 0.1', lambda s: True),
                      ('E(X) = 0(0.3) + 1(0.4) + 2(0.2) + 3(0.1) = 0 + 0.4 + 0.4 + 0.3 = 1.1',
                       lambda s: EX(s, [(0, '0.3'), (1, '0.4'), (2, '0.2'), (3, '0.1')]) and s.E == F('1.1'))],
    'es_alevel_003': [('k + k + 2k + k = 5k = 1, so k = 0.2', lambda s: True),
                      ('E(X) = 1(0.2) + 2(0.2) + 3(0.4) + 4(0.2) = 0.2 + 0.4 + 1.2 + 0.8 = 2.6',
                       lambda s: EX(s, [(1, '0.2'), (2, '0.2'), (3, '0.4'), (4, '0.2')]) and s.E == F('2.6'))],
    'es_alevel_004': [('E(X) = 0(0.45) + 1(0.30) + 2(0.20) + 3(0.05) = 0.85',
                       lambda s: EX(s, [(0, '0.45'), (1, '0.30'), (2, '0.20'), (3, '0.05')]) and s.E == F('0.85')),
                      ('P(X >= 1) = 0.55', lambda s: s.P(lambda x: x >= 1) == F('0.55'))],
    'es_alevel_005': [('E(X) = (0+1+2+3+4+5)/6 = 15/6 = 2.50', lambda s: F(15, 6) == s.E == F('2.5'))],
    'es_alevel_006': [('E(X) = 0.4', lambda s: s.E == F('0.4')), ('E(X) = np = 4(0.1) = 0.4', lambda s: 4 * F('0.1') == s.E),
                      ('Bin(4, 0.1)', lambda s: all(p == __import__('math').comb(4, int(x)) * F(1, 10) ** int(x) * F(9, 10) ** (4 - int(x))
                                                    for x, p in s.d))],
    'es_alevel_007': [('E(X) = 1(0.10) + 3(0.25) + 5(0.35) + 7(0.20) + 10(0.10) = 0.10 + 0.75 + 1.75 + 1.40 + 1.00 = 5.00',
                       lambda s: EX(s, [(1, '0.10'), (3, '0.25'), (5, '0.35'), (7, '0.20'), (10, '0.10')]) and s.E == 5)],
    'es_alevel_008': [('E(X) = -10(0.15) + 0(0.25) + 10(0.35) + 20(0.25) = -1.5 + 0 + 3.5 + 5.0 = 7.0',
                       lambda s: EX(s, [(-10, '0.15'), (0, '0.25'), (10, '0.35'), (20, '0.25')]) and s.E == 7)],
    'es_alevel_009': [('E(X) = 1(0.1) + 2(0.2) + 3(0.3) + 4(0.4) = 0.1 + 0.4 + 0.9 + 1.6 = 3.0',
                       lambda s: EX(s, [(1, '0.1'), (2, '0.2'), (3, '0.3'), (4, '0.4')]) and s.E == 3),
                      ('negatively (left-) skewed distribution with E(X) = 3',
                       lambda s: sum((x - s.E) ** 3 * p for x, p in s.d) < 0)],
    'es_alevel_010': [('E(X) = -2(0.20) + 0(0.30) + 1(0.30) + 3(0.20) = -0.40 + 0 + 0.30 + 0.60 = 0.50',
                       lambda s: EX(s, [(-2, '0.20'), (0, '0.30'), (1, '0.30'), (3, '0.20')]) and s.E == F('0.5')),
                      ('P(loss) = 0.20', lambda s: s.P(lambda x: x < 0) == F('0.2'))],
}


# Where the model rests on the words of the context, the words the context must carry, and a check that the table
# is that model.
import math  # noqa: E402
CONTEXT = {
    'es_gcse_001': ('A fair spinner', lambda s: len({p for _, p in s.d}) == 1),
    'es_gcse_005': ('A fair coin is flipped 3 times', lambda s: all(p == F(math.comb(3, int(x)), 8) for x, p in s.d)),
    'es_gcse_008': ('The spinner is biased', lambda s: len({p for _, p in s.d}) > 1),
    'es_gcse_003': ('standard die', lambda s: all(p == F(1, 3) for _, p in s.d)),
    'es_alevel_005': ('Let X be your winnings in pounds', lambda s: [x for x, _ in s.d] == list(range(6))
                      and all(p == F(1, 6) for _, p in s.d)),
    'es_alevel_006': ('defective items in a batch of 4', lambda s: True),
    'es_alevel_009': ('P(X = x) = x/10 for x = 1, 2, 3, 4', lambda s: all(p == x / 10 for x, p in s.d)),
}


def check_bank(fails, bank):
    counts = {lv: len(bank.get(lv, [])) for lv in COUNTS}
    if counts != COUNTS:
        fails.append('bank: %s items by level, expected %s (a change needs CARDS reviewed)' % (counts, COUNTS))
    items = [q for lv in COUNTS for q in bank.get(lv, [])]
    for qid in sorted(set(CARDS) - {q['id'] for q in items}):
        fails.append('%s: in CARDS but not in the bank' % qid)
    for q in items:
        qid, w = q['id'], where(q['id'])
        d = dist(q)
        s = D(d)
        if sum(p for _, p in d) != 1:
            fails.append('%s: the probabilities sum to %s' % (w, sum(p for _, p in d)))
        places = len(str(q['answer']).split('.')[1]) if '.' in str(q['answer']) else 0
        if round(float(s.E), places) != float(q['answer']) and not (places == 0 and s.E == q['answer']):
            fails.append('%s: answer %s, E(X) = %s' % (w, q['answer'], s.E))
        missing = sorted(p for (x, p), r in zip(d, q['table']) if not r['given'])
        tiles = [F(t) for t in q['stage1Tiles']]
        for p in missing:
            if p not in tiles:
                fails.append('%s: the missing value %s is not among the tiles %s' % (w, p, q['stage1Tiles']))
            else:
                tiles.remove(p)
        if qid in CONTEXT:
            phrase, chk = CONTEXT[qid]
            if phrase not in q['context']:
                fails.append('%s: the context must say "%s" for the table to be its model: %r' % (w, phrase, q['context']))
            elif not chk(s):
                fails.append('%s: the table is not the model "%s"' % (w, phrase))
        # Stage 3
        cards = CARDS.get(qid)
        if cards is None:
            fails.append('%s: no reviewed CARDS entry (review the item and add it; never skip)' % qid)
            continue
        texts = [c['text'] for c in q['interpretations']]
        keyed = [c['text'] for c in q['interpretations'] if c['correct']]
        if len(keyed) != 1:
            fails.append('%s: %d cards keyed correct' % (w, len(keyed)))
        matched = set()
        for start, truth, chk in cards:
            hits = [t for t in texts if t.startswith(start)]
            if len(hits) != 1:
                fails.append('%s: the reviewed card "%s" is not on the item' % (w, start))
                continue
            matched.add(hits[0])
            if truth != (hits[0] in keyed):
                fails.append('%s: "%s" is keyed %s, reviewed as %s' % (w, hits[0], hits[0] in keyed, truth))
            if chk is not None and bool(chk(s)) != truth:
                fails.append('%s: the card "%s" is %s for this distribution (SR-16: a true statement is never a '
                             'wrong option)' % (w, hits[0], 'true' if chk(s) else 'false'))
        for t in texts:
            if t not in matched:
                fails.append('%s: the card "%s" has no reviewed verdict in CARDS' % (w, t))
        # Explanation figures
        text = q['explanation'] + ' || ' + q.get('kExplanation', '')
        covered = [False] * len(text)
        for snip, chk in FIGURES.get(qid, []):
            idx = [m.start() for m in re.finditer(re.escape(snip), text)]
            if not idx:
                fails.append('%s: the reviewed claim "%s" is not in the explanation' % (w, snip))
                continue
            for i in idx:
                covered[i:i + len(snip)] = [True] * len(snip)
            if not chk(s):
                fails.append('%s explanation: "%s" is false' % (w, snip))
        for m in re.finditer(r'[=≈<>≥≤]', text):
            if not covered[m.start()]:
                a = max(0, m.start() - 30)
                fails.append('%s explanation: "...%s..." has no check in FIGURES' % (w, text[a:m.end() + 20]))


SWEEP_JS = r"""() => {
  // The game's pauses run when drain() is called, a bounded number of rounds (a timer that re-arms itself, such
  // as the KaTeX wait, is never run into a loop).
  const queue = []; window.setTimeout = (f) => { queue.push(f); return 0; };
  MaffsLock.timer = (f) => { queue.push(f); return 0; };   // MaffsLock's timers too (they go through setTimeout)
  const drain = () => { for (let n = 0; n < 3; n++) queue.splice(0).forEach(f => { try { f(); } catch (e) {} }); };
  const out = [];
  const items = [...QUESTIONS.core, ...QUESTIONS.gcse, ...QUESTIONS.alevel];
  const fb = () => document.getElementById('stageFeedback').textContent;
  for (const q of items) {
    const r = {id: q.id, problems: [], ex: null};
    const start = () => { questionQueue = [q]; currentQIndex = 0; totalScore = 0; maxScore = 0; loadQuestion(); };
    const fill1 = (vals) => { vals.forEach(([i, v]) => { selectedCell = i; placeTileInCell(v, 0); }); checkStage1(); drain(); };
    const missing = q.table.map((row, i) => [i, row]).filter(([i, row]) => !row.given).map(([i]) => i);
    const val = (i) => { const p = completedTable[i].pr; return q.stage1Tiles.find(t => ratKey(ratFromString(t)) === ratKey(p)); };
    // a wrong tile for one cell (the first tile not equal in value to that cell), marked wrong
    start();
    const wrongTile = q.stage1Tiles.find(t => ratKey(ratFromString(t)) !== ratKey(completedTable[missing[0]].pr));
    if (wrongTile !== undefined) {
      fill1(missing.map(i => [i, i === missing[0] ? wrongTile : val(i)]));
      if (currentStage !== 1 || /complete/i.test(fb())) r.problems.push('Stage 1 accepted the wrong tile ' + wrongTile + ' for x = ' + q.table[missing[0]].x);
    }
    if (q.id === 'es_alevel_006') {
      start();
      const four = missing.find(i => q.table[i].x === 4);
      fill1(missing.map(i => [i, i === four ? '0.0004' : val(i)]));
      if (currentStage !== 1 || /complete/i.test(fb())) r.problems.push('Stage 1 accepted the tile 0.0004 for P(X = 4) = 0.0001');
    }
    // the right tiles
    start();
    fill1(missing.map(i => [i, val(i)]));
    if (currentStage !== 2) { r.problems.push('the right tiles did not complete the table'); out.push(r); continue; }
    const prods = productRats();
    prods.forEach((p, i) => { selectedSlot = i; placeTileInSlot(ratKey(p), 0); });
    checkStage2(); drain();
    if (currentStage !== 3) { r.problems.push('the right products did not complete E(X)'); out.push(r); continue; }
    r.ex = ratKey(exactEX());
    r.exShown = document.getElementById('exResultValue').textContent;
    // every card: the wrong ones marked wrong, the true one right (two attempts per question, so re-render)
    for (let j = 0; j < q.interpretations.length; j++) {
      stage3Attempts = 0; MaffsLock.fresh(document.getElementById('stage3Wrap')); renderStage3();   // a new attempt, so a fresh lock
      const k = currentQ._shuffledInterps.findIndex(c => c.text === q.interpretations[j].text);
      document.getElementById('interp_' + k).click();
      checkStage3(); drain();
      const ok = /^Correct/.test(fb());
      if (ok !== q.interpretations[j].correct) r.problems.push('the card "' + q.interpretations[j].text + '" was marked ' + (ok ? 'right' : 'wrong'));
      stage3Correct = false; currentStage = 3;
      document.getElementById('nextBtn').style.display = 'none';
    }
    out.push(r);
  }
  return out;
}"""


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)   # MaffsLock's 300 ms window: the sweep answers at once
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof loadQuestion === "function"', timeout=8000)
            bank = page.evaluate('() => QUESTIONS')
            for r in page.evaluate(SWEEP_JS):
                for p in r['problems']:
                    fails.append('%s in Chromium: %s' % (where(r['id']), p))
                if r['ex'] is not None:
                    q = next(q for lv in COUNTS for q in bank[lv] if q['id'] == r['id'])
                    n, dd = r['ex'].split('/')
                    if F(int(n), int(dd)) != D(dist(q)).E:
                        fails.append('%s in Chromium: E(X) shown as %s, exactly %s' % (where(r['id']), r['exShown'], D(dist(q)).E))
            browser.close()
            game_errors = [e for e in errors if 'firebase' not in e.lower()]
            if game_errors:
                fails.append('page errors: %s' % '; '.join(game_errors[:3]))
            return bank
    finally:
        proc.terminate()
        proc.wait()


def u(s):
    return ''.join('\\u%04x' % ord(c) if ord(c) > 126 else c for c in s)


PLANTS = [
    ('es_alevel_001', 't2-002: the true card "The median of X is 3"',
     'The mean is 3, so half the values of X are above 3', 'The median of X is 3'),
    ('es_alevel_006', 't2-012: Stage 1 marked to within 0.001',
     'if (ratKey(ratFromString(filledCells[i])) === ratKey(completedTable[i].pr)) {',
     'if (Math.abs(parseFrac(filledCells[i]) - completedTable[i].p) < 0.001) {'),
    ('es_gcse_005', 't2-013: "A biased coin" with a fair coin\'s table', 'A fair coin is flipped 3 times.',
     'A biased coin is flipped 3 times.'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    bank = play(fails, html)
    if bank is not None:
        check_bank(fails, bank)
    print('%s: %d items: tables, E(X), %d Stage 3 cards and the explanations recomputed; every item played in Chromium'
          % (SLUG, sum(len(bank[lv]) for lv in COUNTS) if bank else 0, sum(len(v) for v in CARDS.values())))
    ok = True
    if not args.no_selftest and not args.against:
        for qid, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-52s *** CANNOT PLANT ***' % what)
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(old, new))
            if planted is not None:
                check_bank(rep, planted)
            hit = [f for f in rep if f.startswith(qid)]
            ok = ok and bool(hit)
            print('  self-test %-52s %s' % (what, ('caught: ' + hit[0][:110]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
