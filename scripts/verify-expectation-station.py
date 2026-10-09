#!/usr/bin/env python3
# ci-line: Expectation Station (every table, E(X) and explanation figure exact; all 480 Stage 3 cards reviewed against the distribution; Stage 1 has exactly one completion; every stage played in Chromium) |
"""Expectation Station: every distribution, product, E(X), Stage 3 card and explanation checked; every item played.

The game (120 items: core 40, gcse 40, alevel 40) has three stages: complete the probability table from tiles,
place the products x·P(X = x) to build E(X), then pick the interpretation of E(X) from four cards. The tranche 2
audit of 6 Oct 2026 found Stage 3 "wrong" cards that are true statements (6 of the 10 A-Level items: the median
of X really is 3, X = 1 really is the most likely value, P(profit) really is 0.5 ...), Stage 1 marked with a
0.001 tolerance that accepted the wrong tile 0.0004 for 0.0001, a "biased" coin whose table is a fair coin's,
E(X) = £2.50 keyed where X was the die score, and a left-skewed distribution called right-skewed.

The bank is read from the live page, then for every item:
  Table: every probability exact (k resolved from the table: the coefficients times k sum to 1, as the item's
    kExplanation says); they sum to 1; the stored answer is E(X) at the places it is written.
  Stage 1 tiles: the missing values are among the tiles (as a multiset).
  Stage 1 has exactly one completion (expectation-station-pc-001; Jon's ruling B, 7 Oct 2026). The game marks
    each cell by exact match, so an item whose tiles fit the table two ways marks a right answer wrong. CLUES
    holds, for every item, what the item states beyond "the probabilities sum to 1" (a ratio or difference of two
    missing cells, E(X), or a probability function); its words must be in the context. Every placement of the
    tiles into the missing cells is tried: exactly one may sum to 1 and satisfy the CLUES entry, and it must be the
    keyed one. 33 of the original 45 items had two such completions until each was given a stated relation.
  Stage 3: CARDS below holds a reviewed verdict for every card, with a check computed from the distribution
    wherever the card makes a checkable claim (a probability, the mode, the median, the variance ...). Exactly
    one card is true, and it is the keyed one (SR-16: a true statement is never a wrong option). "Most" in a
    card means more than half; a card that leans on "the most common" is written that way.
  Explanation: every relation sign (=, ≈, <, >, ≥) in it lies inside a claim listed in FIGURES, and each claim
    is recomputed exactly.
  Chromium (390x844), through the game's own stages: the right tiles complete the table; on es_alevel_006 the
    wrong tile 0.0004 placed for 0.0001 is marked wrong (audit t2-012); the right products complete E(X), and
    the E(X) shown is the exact sum; every wrong card is marked wrong and the true card right.
A self-test plants four faults back into a copy of the page (t2-002: the true card "The median of X is 3"; t2-012:
the 0.001 tolerance; t2-013: "A biased coin"; pc-001: es_core_001 without its stated relation, CLUES ('none',));
each must FAIL naming its item.

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
COUNTS = {'core': 40, 'gcse': 40, 'alevel': 40}
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

    # The 75 items added on 8 Oct 2026 (Project Claude's bundle of 7 Oct, Jon's ruling B).
# exact distribution when generated: exactly one T per item, every W false.

    'es_core_021': [
        T('On average, there are 1.6 repairs per hour', lambda s: s.E == F('1.6')),
        W('Every hour has exactly 1.6 repairs', lambda s: s.P(lambda x: x == F('1.6')) == 1),
        W('1.6 is the most likely number of repairs', lambda s: F('1.6') in s.modes()),
        W('Most hours have exactly 2 repairs', lambda s: s.most(2)),
    ],
    'es_core_022': [
        T('On average, there are 1.05 ambulances per 10-minute period', lambda s: s.E == F('1.05')),
        W('1.05 is the most likely number of ambulances', lambda s: F('1.05') in s.modes()),
        W('Most 10-minute periods have exactly 1 ambulance', lambda s: s.most(1)),
        W('There are never more than 2 ambulances per 10-minute period', lambda s: s.P(lambda x: x <= 2) == 1),
    ],
    'es_core_024': [
        T('On average, there are 0.85 missed sessions per term', lambda s: s.E == F('0.85')),
        W('0.85 is the most likely number of missed sessions', lambda s: F('0.85') in s.modes()),
        W('Most terms have no missed sessions', lambda s: s.most(0)),
        W('There are never more than 2 missed sessions per term', lambda s: s.P(lambda x: x <= 2) == 1),
    ],
    'es_core_025': [
        T('On average, there are 1.5 late returns per day', lambda s: s.E == F('1.5')),
        W('There are never more than 3 late returns per day', lambda s: s.P(lambda x: x <= 3) == 1),
        W('Half of all days have more than 1.5 late returns', lambda s: s.P(lambda x: x > F('1.5')) == F(1, 2)),
        W('Every day has exactly 1.5 late returns', lambda s: s.P(lambda x: x == F('1.5')) == 1),
    ],
    'es_core_026': [
        T('On average, there are 0.6 missed bins per street', lambda s: s.E == F('0.6')),
        W('There are never more than 2 missed bins per street', lambda s: s.P(lambda x: x <= 2) == 1),
        W('Half of all streets have more than 0.6 missed bins', lambda s: s.P(lambda x: x > F('0.6')) == F(1, 2)),
        W('Every street has exactly 0.6 missed bins', lambda s: s.P(lambda x: x == F('0.6')) == 1),
    ],
    'es_core_027': [
        T('On average, there are 1.75 new memberships per day', lambda s: s.E == F('1.75')),
        W('Every day has exactly 1.75 new memberships', lambda s: s.P(lambda x: x == F('1.75')) == 1),
        W('1.75 is the most likely number of new memberships', lambda s: F('1.75') in s.modes()),
        W('Most days have exactly 1 new membership', lambda s: s.most(1)),
    ],
    'es_core_028': [
        T('On average, there are 0.75 power cuts per year', lambda s: s.E == F('0.75')),
        W('Every year has exactly 0.75 power cuts', lambda s: s.P(lambda x: x == F('0.75')) == 1),
        W('75% of years have at least one power cut', lambda s: s.P(lambda x: x >= 1) == F('0.75')),
        W('0.75 is the most likely number of power cuts', lambda s: F('0.75') in s.modes()),
    ],
    'es_core_029': [
        T('On average, there are 0.9 cancellations per day', lambda s: s.E == F('0.9')),
        W('90% of days have at least one cancellation', lambda s: s.P(lambda x: x >= 1) == F('0.9')),
        W('0.9 is the most likely number of cancellations', lambda s: F('0.9') in s.modes()),
        W('Most days have no cancellations', lambda s: s.most(0)),
    ],
    'es_core_031': [
        T('On average, there are 1.4 no-show tables per evening', lambda s: s.E == F('1.4')),
        W('There are never more than 3 no-show tables per evening', lambda s: s.P(lambda x: x <= 3) == 1),
        W('Half of all evenings have more than 1.4 no-show tables', lambda s: s.P(lambda x: x > F('1.4')) == F(1, 2)),
        W('Every evening has exactly 1.4 no-show tables', lambda s: s.P(lambda x: x == F('1.4')) == 1),
    ],
    'es_core_032': [
        T('On average, there are 0.7 overdue books per borrower', lambda s: s.E == F('0.7')),
        W('There are never more than 2 overdue books per borrower', lambda s: s.P(lambda x: x <= 2) == 1),
        W('Half of all borrowers have more than 0.7 overdue books', lambda s: s.P(lambda x: x > F('0.7')) == F(1, 2)),
        W('Every borrower has exactly 0.7 overdue books', lambda s: s.P(lambda x: x == F('0.7')) == 1),
    ],
    'es_core_033': [
        T('On average, there are 0.95 uncollected parcels per day', lambda s: s.E == F('0.95')),
        W('There are never more than 2 uncollected parcels per day', lambda s: s.P(lambda x: x <= 2) == 1),
        W('Half of all days have more than 0.95 uncollected parcels', lambda s: s.P(lambda x: x > F('0.95')) == F(1, 2)),
        W('Every day has exactly 0.95 uncollected parcels', lambda s: s.P(lambda x: x == F('0.95')) == 1),
    ],
    'es_core_034': [
        T('On average, there are 0.55 fillings per check-up', lambda s: s.E == F('0.55')),
        W('Half of all check-ups have more than 0.55 fillings', lambda s: s.P(lambda x: x > F('0.55')) == F(1, 2)),
        W('Every check-up has exactly 0.55 fillings', lambda s: s.P(lambda x: x == F('0.55')) == 1),
        W('55% of check-ups have at least one filling', lambda s: s.P(lambda x: x >= 1) == F('0.55')),
    ],
    'es_core_035': [
        T('On average, there are 1.05 cancelled rides per shift', lambda s: s.E == F('1.05')),
        W('Most shifts have exactly 1 cancelled ride', lambda s: s.most(1)),
        W('There are never more than 2 cancelled rides per shift', lambda s: s.P(lambda x: x <= 2) == 1),
        W('Half of all shifts have more than 1.05 cancelled rides', lambda s: s.P(lambda x: x > F('1.05')) == F(1, 2)),
    ],
    'es_core_036': [
        T('On average, there are 1.8 referrals per hour', lambda s: s.E == F('1.8')),
        W('There are never more than 3 referrals per hour', lambda s: s.P(lambda x: x <= 3) == 1),
        W('Half of all hours have more than 1.8 referrals', lambda s: s.P(lambda x: x > F('1.8')) == F(1, 2)),
        W('Every hour has exactly 1.8 referrals', lambda s: s.P(lambda x: x == F('1.8')) == 1),
    ],
    'es_core_038': [
        T('On average, there are 1.65 attempts per apprentice', lambda s: s.E == F('1.65')),
        W('Half of all apprentices have more than 1.65 attempts', lambda s: s.P(lambda x: x > F('1.65')) == F(1, 2)),
        W('Every apprentice has exactly 1.65 attempts', lambda s: s.P(lambda x: x == F('1.65')) == 1),
        W('1.65 is the most likely number of attempts', lambda s: F('1.65') in s.modes()),
    ],
    'es_core_039': [
        T('On average, there are 0.75 top-ups per month', lambda s: s.E == F('0.75')),
        W('Most months have no top-ups', lambda s: s.most(0)),
        W('There are never more than 2 top-ups per month', lambda s: s.P(lambda x: x <= 2) == 1),
        W('Every month has exactly 0.75 top-ups', lambda s: s.P(lambda x: x == F('0.75')) == 1),
    ],
    'es_core_040': [
        T('On average, there are 2.05 free beds per morning', lambda s: s.E == F('2.05')),
        W('2.05 is the most likely number of free beds', lambda s: F('2.05') in s.modes()),
        W('Most mornings have exactly 2 free beds', lambda s: s.most(2)),
        W('There are never more than 3 free beds per morning', lambda s: s.P(lambda x: x <= 3) == 1),
    ],
    'es_core_023': [
        T('On average, a customer receives £27.50, less than the £30 cost, so the shop makes money in the long run', lambda s: s.E == F('27.5') and s.E < 30),
        W('Every customer receives exactly £27.50', lambda s: s.P(lambda x: x == F('27.5')) == 1),
        W('£27.50 is the most common payout', lambda s: F('27.5') in s.modes()),
        W('Every customer gets back at least the £30 they paid', lambda s: s.P(lambda x: x >= 30) == 1),
    ],
    'es_core_030': [
        T('On average, a player wins £1.20, less than the £2 cost, so the seller makes money in the long run', lambda s: s.E == F('1.2') and s.E < 2),
        W('Every player wins exactly £1.20', lambda s: s.P(lambda x: x == F('1.2')) == 1),
        W('£1.20 is the most common prize', lambda s: F('1.2') in s.modes()),
        W('Every player gets back at least the £2 they paid', lambda s: s.P(lambda x: x >= 2) == 1),
    ],
    'es_core_037': [
        T('On average, a player wins £1.05, more than the £1 cost, so players come out ahead and the charity loses money in the long run', lambda s: s.E == F('1.05') and s.E > 1),
        W('Every player wins exactly £1.05', lambda s: s.P(lambda x: x == F('1.05')) == 1),
        W('£1.05 is the most common prize', lambda s: F('1.05') in s.modes()),
        W('Every player gets back at least the £1 they paid', lambda s: s.P(lambda x: x >= 1) == 1),
    ],
    'es_gcse_023': [
        T('On average, a ticket holder wins £0.60, less than the £1 cost, so the school makes money in the long run', lambda s: s.E == F('0.6') and s.E < 1),
        W('Every ticket holder wins exactly £0.60', lambda s: s.P(lambda x: x == F('0.6')) == 1),
        W('£0.60 is the most common prize', lambda s: F('0.6') in s.modes()),
        W('Every ticket holder gets back at least the £1 they paid', lambda s: s.P(lambda x: x >= 1) == 1),
    ],
    'es_gcse_018': [
        T('On average, there are 1.2 buses per 10-minute period', lambda s: s.E == F('1.2')),
        W('Most 10-minute periods have exactly 1 bus', lambda s: s.most(1)),
        W('There are never more than 2 buses per 10-minute period', lambda s: s.P(lambda x: x <= 2) == 1),
        W('Half of all 10-minute periods have more than 1.2 buses', lambda s: s.P(lambda x: x > F('1.2')) == F(1, 2)),
    ],
    'es_gcse_019': [
        T('On average, there are 1.4 goals per match', lambda s: s.E == F('1.4')),
        W('There are never more than 3 goals per match', lambda s: s.P(lambda x: x <= 3) == 1),
        W('Half of all matches have more than 1.4 goals', lambda s: s.P(lambda x: x > F('1.4')) == F(1, 2)),
        W('Every match has exactly 1.4 goals', lambda s: s.P(lambda x: x == F('1.4')) == 1),
    ],
    'es_gcse_020': [
        T('On average, there are 0.9 saves per shootout', lambda s: s.E == F('0.9')),
        W('90% of shootouts have at least one save', lambda s: s.P(lambda x: x >= 1) == F('0.9')),
        W('0.9 is the most likely number of saves', lambda s: F('0.9') in s.modes()),
        W('Most shootouts have no saves', lambda s: s.most(0)),
    ],
    'es_gcse_021': [
        T('On average, there is 1 console per home', lambda s: s.E == 1),
        W('Every home has exactly 1 console', lambda s: s.P(lambda x: x == 1) == 1),
        W('Most homes have exactly 1 console', lambda s: s.most(1)),
        W('There are never more than 2 consoles per home', lambda s: s.P(lambda x: x <= 2) == 1),
    ],
    'es_gcse_022': [
        T('On average, there are 1.35 hours of homework per night', lambda s: s.E == F('1.35')),
        W('1.35 is the most likely number of hours of homework', lambda s: F('1.35') in s.modes()),
        W('Most nights have exactly 1 hour of homework', lambda s: s.most(1)),
        W('There are never more than 2 hours of homework per night', lambda s: s.P(lambda x: x <= 2) == 1),
    ],
    'es_gcse_025': [
        T('On average, there are 1.9 baskets per set of 3 throws', lambda s: s.E == F('1.9')),
        W('Most sets of 3 throws have exactly 2 baskets', lambda s: s.most(2)),
        W('There are never more than 2 baskets per set of 3 throws', lambda s: s.P(lambda x: x <= 2) == 1),
        W('Half of all sets of 3 throws have more than 1.9 baskets', lambda s: s.P(lambda x: x > F('1.9')) == F(1, 2)),
    ],
    'es_gcse_026': [
        T('On average, there are 1.95 red lights per journey', lambda s: s.E == F('1.95')),
        W('There are never more than 3 red lights per journey', lambda s: s.P(lambda x: x <= 3) == 1),
        W('Half of all journeys have more than 1.95 red lights', lambda s: s.P(lambda x: x > F('1.95')) == F(1, 2)),
        W('Every journey has exactly 1.95 red lights', lambda s: s.P(lambda x: x == F('1.95')) == 1),
    ],
    'es_gcse_027': [
        T('On average, there are 1.75 messages per hour', lambda s: s.E == F('1.75')),
        W('Half of all hours have more than 1.75 messages', lambda s: s.P(lambda x: x > F('1.75')) == F(1, 2)),
        W('Every hour has exactly 1.75 messages', lambda s: s.P(lambda x: x == F('1.75')) == 1),
        W('1.75 is the most likely number of messages', lambda s: F('1.75') in s.modes()),
    ],
    'es_gcse_028': [
        T('On average, there is 1 fish per trip', lambda s: s.E == 1),
        W('Every trip has exactly 1 fish', lambda s: s.P(lambda x: x == 1) == 1),
        W('Most trips have exactly 1 fish', lambda s: s.most(1)),
        W('There are never more than 2 fish per trip', lambda s: s.P(lambda x: x <= 2) == 1),
    ],
    'es_gcse_030': [
        T('On average, there are 1.3 unsold cakes per day', lambda s: s.E == F('1.3')),
        W('1.3 is the most likely number of unsold cakes', lambda s: F('1.3') in s.modes()),
        W('Most days have exactly 1 unsold cake', lambda s: s.most(1)),
        W('There are never more than 2 unsold cakes per day', lambda s: s.P(lambda x: x <= 2) == 1),
    ],
    'es_gcse_031': [
        T('On average, there are 1.65 charges per day', lambda s: s.E == F('1.65')),
        W('Most days have exactly 1 charge', lambda s: s.most(1)),
        W('There are never more than 2 charges per day', lambda s: s.P(lambda x: x <= 2) == 1),
        W('Every day has exactly 1.65 charges', lambda s: s.P(lambda x: x == F('1.65')) == 1),
    ],
    'es_gcse_032': [
        T('On average, there are 1.1 goals per match', lambda s: s.E == F('1.1')),
        W('There are never more than 2 goals per match', lambda s: s.P(lambda x: x <= 2) == 1),
        W('Half of all matches have more than 1.1 goals', lambda s: s.P(lambda x: x > F('1.1')) == F(1, 2)),
        W('Every match has exactly 1.1 goals', lambda s: s.P(lambda x: x == F('1.1')) == 1),
    ],
    'es_gcse_033': [
        T('On average, there are 1.7 cups of tea per day', lambda s: s.E == F('1.7')),
        W('Half of all days have more than 1.7 cups of tea', lambda s: s.P(lambda x: x > F('1.7')) == F(1, 2)),
        W('Every day has exactly 1.7 cups of tea', lambda s: s.P(lambda x: x == F('1.7')) == 1),
        W('1.7 is the most likely number of cups of tea', lambda s: F('1.7') in s.modes()),
    ],
    'es_gcse_034': [
        T('On average, there are 2.2 hatched eggs per batch of 3', lambda s: s.E == F('2.2')),
        W('Every batch of 3 has exactly 2.2 hatched eggs', lambda s: s.P(lambda x: x == F('2.2')) == 1),
        W('2.2 is the most likely number of hatched eggs', lambda s: F('2.2') in s.modes()),
        W('Most batches of 3 have exactly 3 hatched eggs', lambda s: s.most(3)),
    ],
    'es_gcse_035': [
        T('On average, there are 1.4 tries per match', lambda s: s.E == F('1.4')),
        W('1.4 is the most likely number of tries', lambda s: F('1.4') in s.modes()),
        W('Most matches have exactly 1 try', lambda s: s.most(1)),
        W('There are never more than 2 tries per match', lambda s: s.P(lambda x: x <= 2) == 1),
    ],
    'es_gcse_036': [
        T('On average, there are 2.35 tickets per go', lambda s: s.E == F('2.35')),
        W('Most goes have exactly 1 ticket', lambda s: s.most(1)),
        W('There are never more than 5 tickets per go', lambda s: s.P(lambda x: x <= 5) == 1),
        W('Half of all goes have more than 2.35 tickets', lambda s: s.P(lambda x: x > F('2.35')) == F(1, 2)),
    ],
    'es_gcse_037': [
        T('On average, there are 1.15 correct answers per quiz', lambda s: s.E == F('1.15')),
        W('There are never more than 3 correct answers per quiz', lambda s: s.P(lambda x: x <= 3) == 1),
        W('Half of all quizzes have more than 1.15 correct answers', lambda s: s.P(lambda x: x > F('1.15')) == F(1, 2)),
        W('Every quiz has exactly 1.15 correct answers', lambda s: s.P(lambda x: x == F('1.15')) == 1),
    ],
    'es_gcse_038': [
        T('On average, there are 0.85 rainy days per weekend', lambda s: s.E == F('0.85')),
        W('There are never more than 1 rainy day per weekend', lambda s: s.P(lambda x: x <= 1) == 1),
        W('Half of all weekends have more than 0.85 rainy days', lambda s: s.P(lambda x: x > F('0.85')) == F(1, 2)),
        W('Every weekend has exactly 0.85 rainy days', lambda s: s.P(lambda x: x == F('0.85')) == 1),
    ],
    'es_gcse_039': [
        T('On average, there are 1.25 pieces of fruit per day', lambda s: s.E == F('1.25')),
        W('Every day has exactly 1.25 pieces of fruit', lambda s: s.P(lambda x: x == F('1.25')) == 1),
        W('1.25 is the most likely number of pieces of fruit', lambda s: F('1.25') in s.modes()),
        W('Most days have exactly 1 piece of fruit', lambda s: s.most(1)),
    ],
    'es_gcse_040': [
        T('On average, there are 0.8 strikes per game', lambda s: s.E == F('0.8')),
        W('Every game has exactly 0.8 strikes', lambda s: s.P(lambda x: x == F('0.8')) == 1),
        W('80% of games have at least one strike', lambda s: s.P(lambda x: x >= 1) == F('0.8')),
        W('0.8 is the most likely number of strikes', lambda s: F('0.8') in s.modes()),
    ],
    'es_gcse_016': [
        T('Over many spins, the mean score is 3', lambda s: s.E == 3),
        W('More than half of all spins score 4', lambda s: s.most(4)),
        W('No spin ever scores more than 3', lambda s: s.P(lambda x: x <= 3) == 1),
        W('Half of all spins score more than 3', lambda s: s.P(lambda x: x > 3) == F(1, 2)),
    ],
    'es_gcse_017': [
        T('Over many picks, the mean score is 2.1', lambda s: s.E == F('2.1')),
        W('No pick ever scores more than 2', lambda s: s.P(lambda x: x <= 2) == 1),
        W('Half of all picks score more than 2.1', lambda s: s.P(lambda x: x > F('2.1')) == F(1, 2)),
        W('Every pick scores exactly 2.1', lambda s: s.P(lambda x: x == F('2.1')) == 1),
    ],
    'es_gcse_024': [
        T('Over many throws, the mean score is 11.5', lambda s: s.E == F('11.5')),
        W('Half of all throws score more than 11.5', lambda s: s.P(lambda x: x > F('11.5')) == F(1, 2)),
        W('Every throw scores exactly 11.5', lambda s: s.P(lambda x: x == F('11.5')) == 1),
        W('11.5 is the most likely score', lambda s: F('11.5') in s.modes()),
    ],
    'es_gcse_029': [
        T('Over many spins, the mean score is 2.2', lambda s: s.E == F('2.2')),
        W('Every spin scores exactly 2.2', lambda s: s.P(lambda x: x == F('2.2')) == 1),
        W('2.2 is the most likely score', lambda s: F('2.2') in s.modes()),
        W('More than half of all spins score 1', lambda s: s.most(1)),
    ],
    'es_alevel_011': [
        T('E(X) = 2, the long-run mean value of X', lambda s: s.E == 2),
        W('The most likely value of X is 2', lambda s: 2 in s.modes()),
        W('P(X > 2) = 0.5, because the mean is the middle value', lambda s: s.P(lambda x: x > 2) == F(1, 2)),
        W('X never exceeds 2', lambda s: s.P(lambda x: x <= 2) == 1),
    ],
    'es_alevel_012': [
        T('E(X) = 2, the long-run mean value of X', lambda s: s.E == 2),
        W('The variance of X is 2', lambda s: s.V == 2),
        W('The median of X is 1', lambda s: s.median() == 1),
        W('The most likely value of X is 2', lambda s: 2 in s.modes()),
    ],
    'es_alevel_013': [
        T('E(X) = 1.5, the long-run mean value of X', lambda s: s.E == F('1.5')),
        W('The median of X is 1', lambda s: s.median() == 1),
        W('The most likely value of X is 1', lambda s: 1 in s.modes()),
        W('P(X > 1.5) = 0.5, because the mean is the middle value', lambda s: s.P(lambda x: x > F('1.5')) == F(1, 2)),
    ],
    'es_alevel_014': [
        T('E(X) = 1, the long-run mean value of X', lambda s: s.E == 1),
        W('The most likely value of X is 1', lambda s: 1 in s.modes()),
        W('P(X > 1) = 0.5, because the mean is the middle value', lambda s: s.P(lambda x: x > 1) == F(1, 2)),
        W('X never exceeds 1', lambda s: s.P(lambda x: x <= 1) == 1),
    ],
    'es_alevel_015': [
        T('E(X) = 3, the long-run mean value of X', lambda s: s.E == 3),
        W('The variance of X is 3', lambda s: s.V == 3),
        W('The median of X is 2', lambda s: s.median() == 2),
        W('The most likely value of X is 3', lambda s: 3 in s.modes()),
    ],
    'es_alevel_016': [
        T('E(X) = 3.8, the long-run mean value of X', lambda s: s.E == F('3.8')),
        W('The most likely value of X is 3', lambda s: 3 in s.modes()),
        W('X = 3.8 is the most likely value', lambda s: F('3.8') in s.modes()),
        W('X never exceeds 3.8', lambda s: s.P(lambda x: x <= F('3.8')) == 1),
    ],
    'es_alevel_017': [
        T('E(X) = 0, the long-run mean value of X', lambda s: s.E == 0),
        W('The most likely value of X is 0', lambda s: 0 in s.modes()),
        W('P(X > 0) = 0.5, because the mean is the middle value', lambda s: s.P(lambda x: x > 0) == F(1, 2)),
        W('X never exceeds 0', lambda s: s.P(lambda x: x <= 0) == 1),
    ],
    'es_alevel_018': [
        T('E(X) = 0, the long-run mean value of X', lambda s: s.E == 0),
        W('The variance of X is 0', lambda s: s.V == 0),
        W('The median of X is −1', lambda s: s.median() == -1),
        W('The most likely value of X is 0', lambda s: 0 in s.modes()),
    ],
    'es_alevel_019': [
        T('E(X) = 7, the long-run mean value of X', lambda s: s.E == 7),
        W('The median of X is 6', lambda s: s.median() == 6),
        W('The most likely value of X is 7', lambda s: 7 in s.modes()),
        W('P(X > 7) = 0.5, because the mean is the middle value', lambda s: s.P(lambda x: x > 7) == F(1, 2)),
    ],
    'es_alevel_020': [
        T('E(X) = 0, the long-run mean value of X', lambda s: s.E == 0),
        W('X = 0 is the most likely value', lambda s: 0 in s.modes()),
        W('X never exceeds 0', lambda s: s.P(lambda x: x <= 0) == 1),
        W('The variance of X is 0', lambda s: s.V == 0),
    ],
    'es_alevel_021': [
        T('E(X) = 2.7, the long-run mean value of X', lambda s: s.E == F('2.7')),
        W('The variance of X is 2.7', lambda s: s.V == F('2.7')),
        W('The median of X is 2', lambda s: s.median() == 2),
        W('The most likely value of X is 2', lambda s: 2 in s.modes()),
    ],
    'es_alevel_022': [
        T('E(X) = 1.25, the long-run mean value of X', lambda s: s.E == F('1.25')),
        W('The median of X is 2', lambda s: s.median() == 2),
        W('The most likely value of X is 2', lambda s: 2 in s.modes()),
        W('P(X > 1.25) = 0.5, because the mean is the middle value', lambda s: s.P(lambda x: x > F('1.25')) == F(1, 2)),
    ],
    'es_alevel_023': [
        T('E(X) = 0.4, the long-run mean value of X', lambda s: s.E == F('0.4')),
        W('X = 0.4 is the most likely value', lambda s: F('0.4') in s.modes()),
        W('X never exceeds 0.4', lambda s: s.P(lambda x: x <= F('0.4')) == 1),
        W('The variance of X is 0.4', lambda s: s.V == F('0.4')),
    ],
    'es_alevel_024': [
        T('E(X) = 3.05, the long-run mean value of X', lambda s: s.E == F('3.05')),
        W('The variance of X is 3.05', lambda s: s.V == F('3.05')),
        W('The median of X is 4', lambda s: s.median() == 4),
        W('The most likely value of X is 4', lambda s: 4 in s.modes()),
    ],
    'es_alevel_025': [
        T('E(X) = 5.3, the long-run mean value of X', lambda s: s.E == F('5.3')),
        W('The median of X is 4', lambda s: s.median() == 4),
        W('The most likely value of X is 4', lambda s: 4 in s.modes()),
        W('P(X > 5.3) = 0.5, because the mean is the middle value', lambda s: s.P(lambda x: x > F('5.3')) == F(1, 2)),
    ],
    'es_alevel_026': [
        T('E(X) = 2.15, the long-run mean value of X', lambda s: s.E == F('2.15')),
        W('The most likely value of X is 3', lambda s: 3 in s.modes()),
        W('P(X > 2.15) = 0.5, because the mean is the middle value', lambda s: s.P(lambda x: x > F('2.15')) == F(1, 2)),
        W('X = 2.15 is the most likely value', lambda s: F('2.15') in s.modes()),
    ],
    'es_alevel_027': [
        T('E(X) = 17, the long-run mean value of X', lambda s: s.E == 17),
        W('The variance of X is 17', lambda s: s.V == 17),
        W('The most likely value of X is 20', lambda s: 20 in s.modes()),
        W('X = 17 is the most likely value', lambda s: 17 in s.modes()),
    ],
    'es_alevel_028': [
        T('E(X) = 0.3, the long-run mean value of X', lambda s: s.E == F('0.3')),
        W('The median of X is 1', lambda s: s.median() == 1),
        W('The most likely value of X is 1', lambda s: 1 in s.modes()),
        W('P(X > 0.3) = 0.5, because the mean is the middle value', lambda s: s.P(lambda x: x > F('0.3')) == F(1, 2)),
    ],
    'es_alevel_029': [
        T('E(X) = 1.75, the long-run mean value of X', lambda s: s.E == F('1.75')),
        W('The most likely value of X is 2', lambda s: 2 in s.modes()),
        W('P(X > 1.75) = 0.5, because the mean is the middle value', lambda s: s.P(lambda x: x > F('1.75')) == F(1, 2)),
        W('X = 1.75 is the most likely value', lambda s: F('1.75') in s.modes()),
    ],
    'es_alevel_030': [
        T('E(X) = 5.5, the long-run mean value of X', lambda s: s.E == F('5.5')),
        W('The variance of X is 5.5', lambda s: s.V == F('5.5')),
        W('The median of X is 10', lambda s: s.median() == 10),
        W('The most likely value of X is 5', lambda s: 5 in s.modes()),
    ],
    'es_alevel_031': [
        T('E(X) = 0.9, the long-run mean value of X', lambda s: s.E == F('0.9')),
        W('The median of X is 0', lambda s: s.median() == 0),
        W('The most likely value of X is 0', lambda s: 0 in s.modes()),
        W('P(X > 0.9) = 0.5, because the mean is the middle value', lambda s: s.P(lambda x: x > F('0.9')) == F(1, 2)),
    ],
    'es_alevel_032': [
        T('E(X) = 0.61, the long-run mean value of X', lambda s: s.E == F('0.61')),
        W('The most likely value of X is 1', lambda s: 1 in s.modes()),
        W('P(X > 0.61) = 0.5, because the mean is the middle value', lambda s: s.P(lambda x: x > F('0.61')) == F(1, 2)),
        W('X = 0.61 is the most likely value', lambda s: F('0.61') in s.modes()),
    ],
    'es_alevel_033': [
        T('E(X) = 0.42, the long-run mean value of X', lambda s: s.E == F('0.42')),
        W('The variance of X is 0.42', lambda s: s.V == F('0.42')),
        W('The median of X is 1', lambda s: s.median() == 1),
        W('The most likely value of X is 1', lambda s: 1 in s.modes()),
    ],
    'es_alevel_034': [
        T('E(X) = 2.25, the long-run mean value of X', lambda s: s.E == F('2.25')),
        W('The median of X is 3', lambda s: s.median() == 3),
        W('The most likely value of X is 3', lambda s: 3 in s.modes()),
        W('P(X > 2.25) = 0.5, because the mean is the middle value', lambda s: s.P(lambda x: x > F('2.25')) == F(1, 2)),
    ],
    'es_alevel_035': [
        T('E(X) = 10.15, the long-run mean value of X', lambda s: s.E == F('10.15')),
        W('The most likely value of X is 11', lambda s: 11 in s.modes()),
        W('P(X > 10.15) = 0.5, because the mean is the middle value', lambda s: s.P(lambda x: x > F('10.15')) == F(1, 2)),
        W('X = 10.15 is the most likely value', lambda s: F('10.15') in s.modes()),
    ],
    'es_alevel_036': [
        T('E(X) = 0.65, the long-run mean value of X', lambda s: s.E == F('0.65')),
        W('The variance of X is 0.65', lambda s: s.V == F('0.65')),
        W('The median of X is 1', lambda s: s.median() == 1),
        W('The most likely value of X is 1', lambda s: 1 in s.modes()),
    ],
    'es_alevel_037': [
        T('E(X) = 1.8, the long-run mean value of X', lambda s: s.E == F('1.8')),
        W('The median of X is 1', lambda s: s.median() == 1),
        W('The most likely value of X is 2', lambda s: 2 in s.modes()),
        W('P(X > 1.8) = 0.5, because the mean is the middle value', lambda s: s.P(lambda x: x > F('1.8')) == F(1, 2)),
    ],
    'es_alevel_038': [
        T('E(X) = 4.25, the long-run mean value of X', lambda s: s.E == F('4.25')),
        W('The most likely value of X is 0', lambda s: 0 in s.modes()),
        W('P(X > 4.25) = 0.5, because the mean is the middle value', lambda s: s.P(lambda x: x > F('4.25')) == F(1, 2)),
        W('X = 4.25 is the most likely value', lambda s: F('4.25') in s.modes()),
    ],
    'es_alevel_039': [
        T('E(X) = 1.25, the long-run mean value of X', lambda s: s.E == F('1.25')),
        W('The variance of X is 1.25', lambda s: s.V == F('1.25')),
        W('The median of X is 2', lambda s: s.median() == 2),
        W('The most likely value of X is 2', lambda s: 2 in s.modes()),
    ],
    'es_alevel_040': [
        T('E(X) = 1.7, the long-run mean value of X', lambda s: s.E == F('1.7')),
        W('The median of X is 1', lambda s: s.median() == 1),
        W('The most likely value of X is 1', lambda s: 1 in s.modes()),
        W('P(X > 1.7) = 0.5, because the mean is the middle value', lambda s: s.P(lambda x: x > F('1.7')) == F(1, 2)),
    ],
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

    # The 75 items added on 8 Oct 2026.
    'es_core_021': [
        ('1 − 0.50 = 0.50', lambda s: 1 - F('0.5') == F('0.5')),
        ('P(X = 2) = 4 × P(X = 0)', lambda s: dict(s.d)[2] == 4 * dict(s.d)[0]),
        ('5 × P(X = 0) = 0.50', lambda s: 5 * F('0.1') == F('0.5')),
        ('P(X = 0) = 0.10', lambda s: dict(s.d)[0] == F('0.1')),
        ('P(X = 2) = 0.40', lambda s: dict(s.d)[2] == F('0.4')),
        ('E(X) = 0 × 0.10 + 1 × 0.35 + 2 × 0.40 + 3 × 0.15 = 1.6', lambda s: 0 * F('0.1') + 1 * F('0.35') + 2 * F('0.4') + 3 * F('0.15') == s.E == F('1.6')),
    ],
    'es_core_022': [
        ('1 − 0.55 = 0.45', lambda s: 1 - F('0.55') == F('0.45')),
        ('P(X = 0) = 2 × P(X = 2)', lambda s: dict(s.d)[0] == 2 * dict(s.d)[2]),
        ('3 × P(X = 2) = 0.45', lambda s: 3 * F('0.15') == F('0.45')),
        ('P(X = 2) = 0.15', lambda s: dict(s.d)[2] == F('0.15')),
        ('P(X = 0) = 0.30', lambda s: dict(s.d)[0] == F('0.3')),
        ('E(X) = 0 × 0.30 + 1 × 0.45 + 2 × 0.15 + 3 × 0.10 = 1.05', lambda s: 0 * F('0.3') + 1 * F('0.45') + 2 * F('0.15') + 3 * F('0.1') == s.E == F('1.05')),
    ],
    'es_core_024': [
        ('1 − 0.65 = 0.35', lambda s: 1 - F('0.65') == F('0.35')),
        ('P(X = 1) = P(X = 3) + 0.25', lambda s: dict(s.d)[1] == dict(s.d)[3] + F('0.25')),
        ('2 × P(X = 3) + 0.25 = 0.35', lambda s: 2 * F('0.05') + F('0.25') == F('0.35')),
        ('P(X = 3) = 0.05', lambda s: dict(s.d)[3] == F('0.05')),
        ('P(X = 1) = 0.30', lambda s: dict(s.d)[1] == F('0.3')),
        ('E(X) = 0 × 0.45 + 1 × 0.30 + 2 × 0.20 + 3 × 0.05 = 0.85', lambda s: 0 * F('0.45') + 1 * F('0.3') + 2 * F('0.2') + 3 * F('0.05') == s.E == F('0.85')),
    ],
    'es_core_025': [
        ('1 − 0.50 = 0.50', lambda s: 1 - F('0.5') == F('0.5')),
        ('P(X = 1) = P(X = 3) + 0.20', lambda s: dict(s.d)[1] == dict(s.d)[3] + F('0.2')),
        ('2 × P(X = 3) + 0.20 = 0.50', lambda s: 2 * F('0.15') + F('0.2') == F('0.5')),
        ('P(X = 3) = 0.15', lambda s: dict(s.d)[3] == F('0.15')),
        ('P(X = 1) = 0.35', lambda s: dict(s.d)[1] == F('0.35')),
        ('E(X) = 0 × 0.20 + 1 × 0.35 + 2 × 0.25 + 3 × 0.15 + 4 × 0.05 = 1.5', lambda s: 0 * F('0.2') + 1 * F('0.35') + 2 * F('0.25') + 3 * F('0.15') + 4 * F('0.05') == s.E == F('1.5')),
    ],
    'es_core_026': [
        ('1 − 0.85 = 0.15', lambda s: 1 - F('0.85') == F('0.15')),
        ('P(X = 2) = 2 × P(X = 3)', lambda s: dict(s.d)[2] == 2 * dict(s.d)[3]),
        ('3 × P(X = 3) = 0.15', lambda s: 3 * F('0.05') == F('0.15')),
        ('P(X = 3) = 0.05', lambda s: dict(s.d)[3] == F('0.05')),
        ('P(X = 2) = 0.10', lambda s: dict(s.d)[2] == F('0.1')),
        ('E(X) = 0 × 0.60 + 1 × 0.25 + 2 × 0.10 + 3 × 0.05 = 0.6', lambda s: 0 * F('0.6') + 1 * F('0.25') + 2 * F('0.1') + 3 * F('0.05') == s.E == F('0.6')),
    ],
    'es_core_027': [
        ('1 − 0.75 = 0.25', lambda s: 1 - F('0.75') == F('0.25')),
        ('P(X = 0) = P(X = 4) + 0.05', lambda s: dict(s.d)[0] == dict(s.d)[4] + F('0.05')),
        ('2 × P(X = 4) + 0.05 = 0.25', lambda s: 2 * F('0.1') + F('0.05') == F('0.25')),
        ('P(X = 4) = 0.10', lambda s: dict(s.d)[4] == F('0.1')),
        ('P(X = 0) = 0.15', lambda s: dict(s.d)[0] == F('0.15')),
        ('E(X) = 0 × 0.15 + 1 × 0.30 + 2 × 0.30 + 3 × 0.15 + 4 × 0.10 = 1.75', lambda s: 0 * F('0.15') + 1 * F('0.3') + 2 * F('0.3') + 3 * F('0.15') + 4 * F('0.1') == s.E == F('1.75')),
    ],
    'es_core_028': [
        ('1 − 0.35 = 0.65', lambda s: 1 - F('0.35') == F('0.65')),
        ('P(X = 0) = P(X = 2) + 0.35', lambda s: dict(s.d)[0] == dict(s.d)[2] + F('0.35')),
        ('2 × P(X = 2) + 0.35 = 0.65', lambda s: 2 * F('0.15') + F('0.35') == F('0.65')),
        ('P(X = 2) = 0.15', lambda s: dict(s.d)[2] == F('0.15')),
        ('P(X = 0) = 0.50', lambda s: dict(s.d)[0] == F('0.5')),
        ('E(X) = 0 × 0.50 + 1 × 0.30 + 2 × 0.15 + 3 × 0.05 = 0.75', lambda s: 0 * F('0.5') + 1 * F('0.3') + 2 * F('0.15') + 3 * F('0.05') == s.E == F('0.75')),
    ],
    'es_core_029': [
        ('1 − 0.60 = 0.40', lambda s: 1 - F('0.6') == F('0.4')),
        ('P(X = 1) = P(X = 3) + 0.30', lambda s: dict(s.d)[1] == dict(s.d)[3] + F('0.3')),
        ('2 × P(X = 3) + 0.30 = 0.40', lambda s: 2 * F('0.05') + F('0.3') == F('0.4')),
        ('P(X = 3) = 0.05', lambda s: dict(s.d)[3] == F('0.05')),
        ('P(X = 1) = 0.35', lambda s: dict(s.d)[1] == F('0.35')),
        ('E(X) = 0 × 0.40 + 1 × 0.35 + 2 × 0.20 + 3 × 0.05 = 0.9', lambda s: 0 * F('0.4') + 1 * F('0.35') + 2 * F('0.2') + 3 * F('0.05') == s.E == F('0.9')),
    ],
    'es_core_031': [
        ('1 − 0.80 = 0.20', lambda s: 1 - F('0.8') == F('0.2')),
        ('P(X = 3) = 3 × P(X = 4)', lambda s: dict(s.d)[3] == 3 * dict(s.d)[4]),
        ('4 × P(X = 4) = 0.20', lambda s: 4 * F('0.05') == F('0.2')),
        ('P(X = 4) = 0.05', lambda s: dict(s.d)[4] == F('0.05')),
        ('P(X = 3) = 0.15', lambda s: dict(s.d)[3] == F('0.15')),
        ('E(X) = 0 × 0.25 + 1 × 0.35 + 2 × 0.20 + 3 × 0.15 + 4 × 0.05 = 1.4', lambda s: 0 * F('0.25') + 1 * F('0.35') + 2 * F('0.2') + 3 * F('0.15') + 4 * F('0.05') == s.E == F('1.4')),
    ],
    'es_core_032': [
        ('1 − 0.60 = 0.40', lambda s: 1 - F('0.6') == F('0.4')),
        ('P(X = 1) = P(X = 2) + 0.10', lambda s: dict(s.d)[1] == dict(s.d)[2] + F('0.1')),
        ('2 × P(X = 2) + 0.10 = 0.40', lambda s: 2 * F('0.15') + F('0.1') == F('0.4')),
        ('P(X = 2) = 0.15', lambda s: dict(s.d)[2] == F('0.15')),
        ('P(X = 1) = 0.25', lambda s: dict(s.d)[1] == F('0.25')),
        ('E(X) = 0 × 0.55 + 1 × 0.25 + 2 × 0.15 + 3 × 0.05 = 0.7', lambda s: 0 * F('0.55') + 1 * F('0.25') + 2 * F('0.15') + 3 * F('0.05') == s.E == F('0.7')),
    ],
    'es_core_033': [
        ('1 − 0.60 = 0.40', lambda s: 1 - F('0.6') == F('0.4')),
        ('P(X = 0) = P(X = 3) + 0.30', lambda s: dict(s.d)[0] == dict(s.d)[3] + F('0.3')),
        ('2 × P(X = 3) + 0.30 = 0.40', lambda s: 2 * F('0.05') + F('0.3') == F('0.4')),
        ('P(X = 3) = 0.05', lambda s: dict(s.d)[3] == F('0.05')),
        ('P(X = 0) = 0.35', lambda s: dict(s.d)[0] == F('0.35')),
        ('E(X) = 0 × 0.35 + 1 × 0.40 + 2 × 0.20 + 3 × 0.05 = 0.95', lambda s: 0 * F('0.35') + 1 * F('0.4') + 2 * F('0.2') + 3 * F('0.05') == s.E == F('0.95')),
    ],
    'es_core_034': [
        ('1 − 0.75 = 0.25', lambda s: 1 - F('0.75') == F('0.25')),
        ('P(X = 1) = 4 × P(X = 3)', lambda s: dict(s.d)[1] == 4 * dict(s.d)[3]),
        ('5 × P(X = 3) = 0.25', lambda s: 5 * F('0.05') == F('0.25')),
        ('P(X = 3) = 0.05', lambda s: dict(s.d)[3] == F('0.05')),
        ('P(X = 1) = 0.20', lambda s: dict(s.d)[1] == F('0.2')),
        ('E(X) = 0 × 0.65 + 1 × 0.20 + 2 × 0.10 + 3 × 0.05 = 0.55', lambda s: 0 * F('0.65') + 1 * F('0.2') + 2 * F('0.1') + 3 * F('0.05') == s.E == F('0.55')),
    ],
    'es_core_035': [
        ('1 − 0.70 = 0.30', lambda s: 1 - F('0.7') == F('0.3')),
        ('P(X = 2) = P(X = 3) + 0.20', lambda s: dict(s.d)[2] == dict(s.d)[3] + F('0.2')),
        ('2 × P(X = 3) + 0.20 = 0.30', lambda s: 2 * F('0.05') + F('0.2') == F('0.3')),
        ('P(X = 3) = 0.05', lambda s: dict(s.d)[3] == F('0.05')),
        ('P(X = 2) = 0.25', lambda s: dict(s.d)[2] == F('0.25')),
        ('E(X) = 0 × 0.30 + 1 × 0.40 + 2 × 0.25 + 3 × 0.05 = 1.05', lambda s: 0 * F('0.3') + 1 * F('0.4') + 2 * F('0.25') + 3 * F('0.05') == s.E == F('1.05')),
    ],
    'es_core_036': [
        ('1 − 0.70 = 0.30', lambda s: 1 - F('0.7') == F('0.3')),
        ('P(X = 3) = 2 × P(X = 0)', lambda s: dict(s.d)[3] == 2 * dict(s.d)[0]),
        ('3 × P(X = 0) = 0.30', lambda s: 3 * F('0.1') == F('0.3')),
        ('P(X = 0) = 0.10', lambda s: dict(s.d)[0] == F('0.1')),
        ('P(X = 3) = 0.20', lambda s: dict(s.d)[3] == F('0.2')),
        ('E(X) = 0 × 0.10 + 1 × 0.30 + 2 × 0.35 + 3 × 0.20 + 4 × 0.05 = 1.8', lambda s: 0 * F('0.1') + 1 * F('0.3') + 2 * F('0.35') + 3 * F('0.2') + 4 * F('0.05') == s.E == F('1.8')),
    ],
    'es_core_038': [
        ('1 − 0.85 = 0.15', lambda s: 1 - F('0.85') == F('0.15')),
        ('P(X = 3) = 2 × P(X = 4)', lambda s: dict(s.d)[3] == 2 * dict(s.d)[4]),
        ('3 × P(X = 4) = 0.15', lambda s: 3 * F('0.05') == F('0.15')),
        ('P(X = 4) = 0.05', lambda s: dict(s.d)[4] == F('0.05')),
        ('P(X = 3) = 0.10', lambda s: dict(s.d)[3] == F('0.1')),
        ('E(X) = 1 × 0.55 + 2 × 0.30 + 3 × 0.10 + 4 × 0.05 = 1.65', lambda s: 1 * F('0.55') + 2 * F('0.3') + 3 * F('0.1') + 4 * F('0.05') == s.E == F('1.65')),
    ],
    'es_core_039': [
        ('1 − 0.65 = 0.35', lambda s: 1 - F('0.65') == F('0.35')),
        ('P(X = 1) = P(X = 3) + 0.25', lambda s: dict(s.d)[1] == dict(s.d)[3] + F('0.25')),
        ('2 × P(X = 3) + 0.25 = 0.35', lambda s: 2 * F('0.05') + F('0.25') == F('0.35')),
        ('P(X = 3) = 0.05', lambda s: dict(s.d)[3] == F('0.05')),
        ('P(X = 1) = 0.30', lambda s: dict(s.d)[1] == F('0.3')),
        ('E(X) = 0 × 0.50 + 1 × 0.30 + 2 × 0.15 + 3 × 0.05 = 0.75', lambda s: 0 * F('0.5') + 1 * F('0.3') + 2 * F('0.15') + 3 * F('0.05') == s.E == F('0.75')),
    ],
    'es_core_040': [
        ('1 − 0.70 = 0.30', lambda s: 1 - F('0.7') == F('0.3')),
        ('P(X = 1) = 2 × P(X = 4)', lambda s: dict(s.d)[1] == 2 * dict(s.d)[4]),
        ('3 × P(X = 4) = 0.30', lambda s: 3 * F('0.1') == F('0.3')),
        ('P(X = 4) = 0.10', lambda s: dict(s.d)[4] == F('0.1')),
        ('P(X = 1) = 0.20', lambda s: dict(s.d)[1] == F('0.2')),
        ('E(X) = 0 × 0.10 + 1 × 0.20 + 2 × 0.35 + 3 × 0.25 + 4 × 0.10 = 2.05', lambda s: 0 * F('0.1') + 1 * F('0.2') + 2 * F('0.35') + 3 * F('0.25') + 4 * F('0.1') == s.E == F('2.05')),
    ],
    'es_core_023': [
        ('1 − 0.80 = 0.20', lambda s: 1 - F('0.8') == F('0.2')),
        ('P(X = 100) = 3 × P(X = 250)', lambda s: dict(s.d)[100] == 3 * dict(s.d)[250]),
        ('4 × P(X = 250) = 0.20', lambda s: 4 * F('0.05') == F('0.2')),
        ('P(X = 250) = 0.05', lambda s: dict(s.d)[250] == F('0.05')),
        ('P(X = 100) = 0.15', lambda s: dict(s.d)[100] == F('0.15')),
        ('E(X) = 0 × 0.80 + 100 × 0.15 + 250 × 0.05 = £27.50', lambda s: 0 * F('0.8') + 100 * F('0.15') + 250 * F('0.05') == s.E == F('27.5')),
    ],
    'es_core_030': [
        ('1 − 0.90 = 0.10', lambda s: 1 - F('0.9') == F('0.1')),
        ('P(X = 5) = 4 × P(X = 20)', lambda s: dict(s.d)[5] == 4 * dict(s.d)[20]),
        ('5 × P(X = 20) = 0.10', lambda s: 5 * F('0.02') == F('0.1')),
        ('P(X = 20) = 0.02', lambda s: dict(s.d)[20] == F('0.02')),
        ('P(X = 5) = 0.08', lambda s: dict(s.d)[5] == F('0.08')),
        ('E(X) = 0 × 0.70 + 2 × 0.20 + 5 × 0.08 + 20 × 0.02 = £1.20', lambda s: 0 * F('0.7') + 2 * F('0.2') + 5 * F('0.08') + 20 * F('0.02') == s.E == F('1.2')),
    ],
    'es_core_037': [
        ('1 − 0.85 = 0.15', lambda s: 1 - F('0.85') == F('0.15')),
        ('P(X = 3) = 2 × P(X = 10)', lambda s: dict(s.d)[3] == 2 * dict(s.d)[10]),
        ('3 × P(X = 10) = 0.15', lambda s: 3 * F('0.05') == F('0.15')),
        ('P(X = 10) = 0.05', lambda s: dict(s.d)[10] == F('0.05')),
        ('P(X = 3) = 0.10', lambda s: dict(s.d)[3] == F('0.1')),
        ('E(X) = 0 × 0.60 + 1 × 0.25 + 3 × 0.10 + 10 × 0.05 = £1.05', lambda s: 0 * F('0.6') + 1 * F('0.25') + 3 * F('0.1') + 10 * F('0.05') == s.E == F('1.05')),
    ],
    'es_gcse_023': [
        ('1 − 0.95 = 0.05', lambda s: 1 - F('0.95') == F('0.05')),
        ('P(X = 5) = 4 × P(X = 20)', lambda s: dict(s.d)[5] == 4 * dict(s.d)[20]),
        ('5 × P(X = 20) = 0.05', lambda s: 5 * F('0.01') == F('0.05')),
        ('P(X = 20) = 0.01', lambda s: dict(s.d)[20] == F('0.01')),
        ('P(X = 5) = 0.04', lambda s: dict(s.d)[5] == F('0.04')),
        ('E(X) = 0 × 0.85 + 2 × 0.10 + 5 × 0.04 + 20 × 0.01 = £0.60', lambda s: 0 * F('0.85') + 2 * F('0.1') + 5 * F('0.04') + 20 * F('0.01') == s.E == F('0.6')),
    ],
    'es_gcse_018': [
        ('1 − 0.70 = 0.30', lambda s: 1 - F('0.7') == F('0.3')),
        ('P(X = 2) = 2 × P(X = 3)', lambda s: dict(s.d)[2] == 2 * dict(s.d)[3]),
        ('3 × P(X = 3) = 0.30', lambda s: 3 * F('0.1') == F('0.3')),
        ('P(X = 3) = 0.10', lambda s: dict(s.d)[3] == F('0.1')),
        ('P(X = 2) = 0.20', lambda s: dict(s.d)[2] == F('0.2')),
        ('E(X) = 0 × 0.20 + 1 × 0.50 + 2 × 0.20 + 3 × 0.10 = 1.2', lambda s: 0 * F('0.2') + 1 * F('0.5') + 2 * F('0.2') + 3 * F('0.1') == s.E == F('1.2')),
    ],
    'es_gcse_019': [
        ('1 − 0.70 = 0.30', lambda s: 1 - F('0.7') == F('0.3')),
        ('P(X = 0) = P(X = 4) + 0.20', lambda s: dict(s.d)[0] == dict(s.d)[4] + F('0.2')),
        ('2 × P(X = 4) + 0.20 = 0.30', lambda s: 2 * F('0.05') + F('0.2') == F('0.3')),
        ('P(X = 4) = 0.05', lambda s: dict(s.d)[4] == F('0.05')),
        ('P(X = 0) = 0.25', lambda s: dict(s.d)[0] == F('0.25')),
        ('E(X) = 0 × 0.25 + 1 × 0.35 + 2 × 0.20 + 3 × 0.15 + 4 × 0.05 = 1.4', lambda s: 0 * F('0.25') + 1 * F('0.35') + 2 * F('0.2') + 3 * F('0.15') + 4 * F('0.05') == s.E == F('1.4')),
    ],
    'es_gcse_020': [
        ('1 − 0.45 = 0.55', lambda s: 1 - F('0.45') == F('0.55')),
        ('P(X = 1) = P(X = 2) + 0.15', lambda s: dict(s.d)[1] == dict(s.d)[2] + F('0.15')),
        ('2 × P(X = 2) + 0.15 = 0.55', lambda s: 2 * F('0.2') + F('0.15') == F('0.55')),
        ('P(X = 2) = 0.20', lambda s: dict(s.d)[2] == F('0.2')),
        ('P(X = 1) = 0.35', lambda s: dict(s.d)[1] == F('0.35')),
        ('E(X) = 0 × 0.40 + 1 × 0.35 + 2 × 0.20 + 3 × 0.05 = 0.9', lambda s: 0 * F('0.4') + 1 * F('0.35') + 2 * F('0.2') + 3 * F('0.05') == s.E == F('0.9')),
    ],
    'es_gcse_021': [
        ('1 − 0.65 = 0.35', lambda s: 1 - F('0.65') == F('0.35')),
        ('P(X = 0) = P(X = 3) + 0.25', lambda s: dict(s.d)[0] == dict(s.d)[3] + F('0.25')),
        ('2 × P(X = 3) + 0.25 = 0.35', lambda s: 2 * F('0.05') + F('0.25') == F('0.35')),
        ('P(X = 3) = 0.05', lambda s: dict(s.d)[3] == F('0.05')),
        ('P(X = 0) = 0.30', lambda s: dict(s.d)[0] == F('0.3')),
        ('E(X) = 0 × 0.30 + 1 × 0.45 + 2 × 0.20 + 3 × 0.05 = 1', lambda s: 0 * F('0.3') + 1 * F('0.45') + 2 * F('0.2') + 3 * F('0.05') == s.E == 1),
    ],
    'es_gcse_022': [
        ('1 − 0.60 = 0.40', lambda s: 1 - F('0.6') == F('0.4')),
        ('P(X = 2) = 3 × P(X = 3)', lambda s: dict(s.d)[2] == 3 * dict(s.d)[3]),
        ('4 × P(X = 3) = 0.40', lambda s: 4 * F('0.1') == F('0.4')),
        ('P(X = 3) = 0.10', lambda s: dict(s.d)[3] == F('0.1')),
        ('P(X = 2) = 0.30', lambda s: dict(s.d)[2] == F('0.3')),
        ('E(X) = 0 × 0.15 + 1 × 0.45 + 2 × 0.30 + 3 × 0.10 = 1.35', lambda s: 0 * F('0.15') + 1 * F('0.45') + 2 * F('0.3') + 3 * F('0.1') == s.E == F('1.35')),
    ],
    'es_gcse_025': [
        ('1 − 0.70 = 0.30', lambda s: 1 - F('0.7') == F('0.3')),
        ('P(X = 1) = 2 × P(X = 0)', lambda s: dict(s.d)[1] == 2 * dict(s.d)[0]),
        ('3 × P(X = 0) = 0.30', lambda s: 3 * F('0.1') == F('0.3')),
        ('P(X = 0) = 0.10', lambda s: dict(s.d)[0] == F('0.1')),
        ('P(X = 1) = 0.20', lambda s: dict(s.d)[1] == F('0.2')),
        ('E(X) = 0 × 0.10 + 1 × 0.20 + 2 × 0.40 + 3 × 0.30 = 1.9', lambda s: 0 * F('0.1') + 1 * F('0.2') + 2 * F('0.4') + 3 * F('0.3') == s.E == F('1.9')),
    ],
    'es_gcse_026': [
        ('1 − 0.70 = 0.30', lambda s: 1 - F('0.7') == F('0.3')),
        ('P(X = 3) = 2 × P(X = 4)', lambda s: dict(s.d)[3] == 2 * dict(s.d)[4]),
        ('3 × P(X = 4) = 0.30', lambda s: 3 * F('0.1') == F('0.3')),
        ('P(X = 4) = 0.10', lambda s: dict(s.d)[4] == F('0.1')),
        ('P(X = 3) = 0.20', lambda s: dict(s.d)[3] == F('0.2')),
        ('E(X) = 0 × 0.10 + 1 × 0.25 + 2 × 0.35 + 3 × 0.20 + 4 × 0.10 = 1.95', lambda s: 0 * F('0.1') + 1 * F('0.25') + 2 * F('0.35') + 3 * F('0.2') + 4 * F('0.1') == s.E == F('1.95')),
    ],
    'es_gcse_027': [
        ('1 − 0.60 = 0.40', lambda s: 1 - F('0.6') == F('0.4')),
        ('P(X = 2) = 3 × P(X = 4)', lambda s: dict(s.d)[2] == 3 * dict(s.d)[4]),
        ('4 × P(X = 4) = 0.40', lambda s: 4 * F('0.1') == F('0.4')),
        ('P(X = 4) = 0.10', lambda s: dict(s.d)[4] == F('0.1')),
        ('P(X = 2) = 0.30', lambda s: dict(s.d)[2] == F('0.3')),
        ('E(X) = 0 × 0.15 + 1 × 0.30 + 2 × 0.30 + 3 × 0.15 + 4 × 0.10 = 1.75', lambda s: 0 * F('0.15') + 1 * F('0.3') + 2 * F('0.3') + 3 * F('0.15') + 4 * F('0.1') == s.E == F('1.75')),
    ],
    'es_gcse_028': [
        ('1 − 0.55 = 0.45', lambda s: 1 - F('0.55') == F('0.45')),
        ('P(X = 0) = P(X = 3) + 0.25', lambda s: dict(s.d)[0] == dict(s.d)[3] + F('0.25')),
        ('2 × P(X = 3) + 0.25 = 0.45', lambda s: 2 * F('0.1') + F('0.25') == F('0.45')),
        ('P(X = 3) = 0.10', lambda s: dict(s.d)[3] == F('0.1')),
        ('P(X = 0) = 0.35', lambda s: dict(s.d)[0] == F('0.35')),
        ('E(X) = 0 × 0.35 + 1 × 0.40 + 2 × 0.15 + 3 × 0.10 = 1', lambda s: 0 * F('0.35') + 1 * F('0.4') + 2 * F('0.15') + 3 * F('0.1') == s.E == 1),
    ],
    'es_gcse_030': [
        ('1 − 0.50 = 0.50', lambda s: 1 - F('0.5') == F('0.5')),
        ('P(X = 1) = 4 × P(X = 3)', lambda s: dict(s.d)[1] == 4 * dict(s.d)[3]),
        ('5 × P(X = 3) = 0.50', lambda s: 5 * F('0.1') == F('0.5')),
        ('P(X = 3) = 0.10', lambda s: dict(s.d)[3] == F('0.1')),
        ('P(X = 1) = 0.40', lambda s: dict(s.d)[1] == F('0.4')),
        ('E(X) = 0 × 0.20 + 1 × 0.40 + 2 × 0.30 + 3 × 0.10 = 1.3', lambda s: 0 * F('0.2') + 1 * F('0.4') + 2 * F('0.3') + 3 * F('0.1') == s.E == F('1.3')),
    ],
    'es_gcse_031': [
        ('1 − 0.50 = 0.50', lambda s: 1 - F('0.5') == F('0.5')),
        ('P(X = 2) = P(X = 3) + 0.20', lambda s: dict(s.d)[2] == dict(s.d)[3] + F('0.2')),
        ('2 × P(X = 3) + 0.20 = 0.50', lambda s: 2 * F('0.15') + F('0.2') == F('0.5')),
        ('P(X = 3) = 0.15', lambda s: dict(s.d)[3] == F('0.15')),
        ('P(X = 2) = 0.35', lambda s: dict(s.d)[2] == F('0.35')),
        ('E(X) = 1 × 0.50 + 2 × 0.35 + 3 × 0.15 = 1.65', lambda s: 1 * F('0.5') + 2 * F('0.35') + 3 * F('0.15') == s.E == F('1.65')),
    ],
    'es_gcse_032': [
        ('1 − 0.70 = 0.30', lambda s: 1 - F('0.7') == F('0.3')),
        ('P(X = 2) = 2 × P(X = 3)', lambda s: dict(s.d)[2] == 2 * dict(s.d)[3]),
        ('3 × P(X = 3) = 0.30', lambda s: 3 * F('0.1') == F('0.3')),
        ('P(X = 3) = 0.10', lambda s: dict(s.d)[3] == F('0.1')),
        ('P(X = 2) = 0.20', lambda s: dict(s.d)[2] == F('0.2')),
        ('E(X) = 0 × 0.30 + 1 × 0.40 + 2 × 0.20 + 3 × 0.10 = 1.1', lambda s: 0 * F('0.3') + 1 * F('0.4') + 2 * F('0.2') + 3 * F('0.1') == s.E == F('1.1')),
    ],
    'es_gcse_033': [
        ('1 − 0.70 = 0.30', lambda s: 1 - F('0.7') == F('0.3')),
        ('P(X = 0) = 2 × P(X = 4)', lambda s: dict(s.d)[0] == 2 * dict(s.d)[4]),
        ('3 × P(X = 4) = 0.30', lambda s: 3 * F('0.1') == F('0.3')),
        ('P(X = 4) = 0.10', lambda s: dict(s.d)[4] == F('0.1')),
        ('P(X = 0) = 0.20', lambda s: dict(s.d)[0] == F('0.2')),
        ('E(X) = 0 × 0.20 + 1 × 0.25 + 2 × 0.30 + 3 × 0.15 + 4 × 0.10 = 1.7', lambda s: 0 * F('0.2') + 1 * F('0.25') + 2 * F('0.3') + 3 * F('0.15') + 4 * F('0.1') == s.E == F('1.7')),
    ],
    'es_gcse_034': [
        ('1 − 0.80 = 0.20', lambda s: 1 - F('0.8') == F('0.2')),
        ('P(X = 1) = 3 × P(X = 0)', lambda s: dict(s.d)[1] == 3 * dict(s.d)[0]),
        ('4 × P(X = 0) = 0.20', lambda s: 4 * F('0.05') == F('0.2')),
        ('P(X = 0) = 0.05', lambda s: dict(s.d)[0] == F('0.05')),
        ('P(X = 1) = 0.15', lambda s: dict(s.d)[1] == F('0.15')),
        ('E(X) = 0 × 0.05 + 1 × 0.15 + 2 × 0.35 + 3 × 0.45 = 2.2', lambda s: 0 * F('0.05') + 1 * F('0.15') + 2 * F('0.35') + 3 * F('0.45') == s.E == F('2.2')),
    ],
    'es_gcse_035': [
        ('1 − 0.50 = 0.50', lambda s: 1 - F('0.5') == F('0.5')),
        ('P(X = 1) = P(X = 3) + 0.20', lambda s: dict(s.d)[1] == dict(s.d)[3] + F('0.2')),
        ('2 × P(X = 3) + 0.20 = 0.50', lambda s: 2 * F('0.15') + F('0.2') == F('0.5')),
        ('P(X = 3) = 0.15', lambda s: dict(s.d)[3] == F('0.15')),
        ('P(X = 1) = 0.35', lambda s: dict(s.d)[1] == F('0.35')),
        ('E(X) = 0 × 0.20 + 1 × 0.35 + 2 × 0.30 + 3 × 0.15 = 1.4', lambda s: 0 * F('0.2') + 1 * F('0.35') + 2 * F('0.3') + 3 * F('0.15') == s.E == F('1.4')),
    ],
    'es_gcse_036': [
        ('1 − 0.80 = 0.20', lambda s: 1 - F('0.8') == F('0.2')),
        ('P(X = 5) = 3 × P(X = 10)', lambda s: dict(s.d)[5] == 3 * dict(s.d)[10]),
        ('4 × P(X = 10) = 0.20', lambda s: 4 * F('0.05') == F('0.2')),
        ('P(X = 10) = 0.05', lambda s: dict(s.d)[10] == F('0.05')),
        ('P(X = 5) = 0.15', lambda s: dict(s.d)[5] == F('0.15')),
        ('E(X) = 1 × 0.50 + 2 × 0.30 + 5 × 0.15 + 10 × 0.05 = 2.35', lambda s: 1 * F('0.5') + 2 * F('0.3') + 5 * F('0.15') + 10 * F('0.05') == s.E == F('2.35')),
    ],
    'es_gcse_037': [
        ('1 − 0.50 = 0.50', lambda s: 1 - F('0.5') == F('0.5')),
        ('P(X = 0) = P(X = 2) + 0.10', lambda s: dict(s.d)[0] == dict(s.d)[2] + F('0.1')),
        ('2 × P(X = 2) + 0.10 = 0.50', lambda s: 2 * F('0.2') + F('0.1') == F('0.5')),
        ('P(X = 2) = 0.20', lambda s: dict(s.d)[2] == F('0.2')),
        ('P(X = 0) = 0.30', lambda s: dict(s.d)[0] == F('0.3')),
        ('E(X) = 0 × 0.30 + 1 × 0.40 + 2 × 0.20 + 3 × 0.05 + 4 × 0.05 = 1.15', lambda s: 0 * F('0.3') + 1 * F('0.4') + 2 * F('0.2') + 3 * F('0.05') + 4 * F('0.05') == s.E == F('1.15')),
    ],
    'es_gcse_038': [
        ('1 − 0.40 = 0.60', lambda s: 1 - F('0.4') == F('0.6')),
        ('P(X = 1) = P(X = 2) + 0.10', lambda s: dict(s.d)[1] == dict(s.d)[2] + F('0.1')),
        ('2 × P(X = 2) + 0.10 = 0.60', lambda s: 2 * F('0.25') + F('0.1') == F('0.6')),
        ('P(X = 2) = 0.25', lambda s: dict(s.d)[2] == F('0.25')),
        ('P(X = 1) = 0.35', lambda s: dict(s.d)[1] == F('0.35')),
        ('E(X) = 0 × 0.40 + 1 × 0.35 + 2 × 0.25 = 0.85', lambda s: 0 * F('0.4') + 1 * F('0.35') + 2 * F('0.25') == s.E == F('0.85')),
    ],
    'es_gcse_039': [
        ('1 − 0.60 = 0.40', lambda s: 1 - F('0.6') == F('0.4')),
        ('P(X = 2) = 3 × P(X = 3)', lambda s: dict(s.d)[2] == 3 * dict(s.d)[3]),
        ('4 × P(X = 3) = 0.40', lambda s: 4 * F('0.1') == F('0.4')),
        ('P(X = 3) = 0.10', lambda s: dict(s.d)[3] == F('0.1')),
        ('P(X = 2) = 0.30', lambda s: dict(s.d)[2] == F('0.3')),
        ('E(X) = 0 × 0.25 + 1 × 0.35 + 2 × 0.30 + 3 × 0.10 = 1.25', lambda s: 0 * F('0.25') + 1 * F('0.35') + 2 * F('0.3') + 3 * F('0.1') == s.E == F('1.25')),
    ],
    'es_gcse_040': [
        ('1 − 0.80 = 0.20', lambda s: 1 - F('0.8') == F('0.2')),
        ('P(X = 2) = 3 × P(X = 3)', lambda s: dict(s.d)[2] == 3 * dict(s.d)[3]),
        ('4 × P(X = 3) = 0.20', lambda s: 4 * F('0.05') == F('0.2')),
        ('P(X = 3) = 0.05', lambda s: dict(s.d)[3] == F('0.05')),
        ('P(X = 2) = 0.15', lambda s: dict(s.d)[2] == F('0.15')),
        ('E(X) = 0 × 0.45 + 1 × 0.35 + 2 × 0.15 + 3 × 0.05 = 0.8', lambda s: 0 * F('0.45') + 1 * F('0.35') + 2 * F('0.15') + 3 * F('0.05') == s.E == F('0.8')),
    ],
    'es_gcse_016': [
        ('1 − 0.50 = 0.50', lambda s: 1 - F('0.5') == F('0.5')),
        ('P(X = 4) = 4 × P(X = 1)', lambda s: dict(s.d)[4] == 4 * dict(s.d)[1]),
        ('5 × P(X = 1) = 0.50', lambda s: 5 * F('0.1') == F('0.5')),
        ('P(X = 1) = 0.10', lambda s: dict(s.d)[1] == F('0.1')),
        ('P(X = 4) = 0.40', lambda s: dict(s.d)[4] == F('0.4')),
        ('E(X) = 1 × 0.10 + 2 × 0.20 + 3 × 0.30 + 4 × 0.40 = 3', lambda s: 1 * F('0.1') + 2 * F('0.2') + 3 * F('0.3') + 4 * F('0.4') == s.E == 3),
    ],
    'es_gcse_017': [
        ('1 − 0.50 = 0.50', lambda s: 1 - F('0.5') == F('0.5')),
        ('P(X = 2) = P(X = 5) + 0.10', lambda s: dict(s.d)[2] == dict(s.d)[5] + F('0.1')),
        ('2 × P(X = 5) + 0.10 = 0.50', lambda s: 2 * F('0.2') + F('0.1') == F('0.5')),
        ('P(X = 5) = 0.20', lambda s: dict(s.d)[5] == F('0.2')),
        ('P(X = 2) = 0.30', lambda s: dict(s.d)[2] == F('0.3')),
        ('E(X) = 1 × 0.50 + 2 × 0.30 + 5 × 0.20 = 2.1', lambda s: 1 * F('0.5') + 2 * F('0.3') + 5 * F('0.2') == s.E == F('2.1')),
    ],
    'es_gcse_024': [
        ('1 − 0.65 = 0.35', lambda s: 1 - F('0.65') == F('0.35')),
        ('P(X = 0) = P(X = 50) + 0.25', lambda s: dict(s.d)[0] == dict(s.d)[50] + F('0.25')),
        ('2 × P(X = 50) + 0.25 = 0.35', lambda s: 2 * F('0.05') + F('0.25') == F('0.35')),
        ('P(X = 50) = 0.05', lambda s: dict(s.d)[50] == F('0.05')),
        ('P(X = 0) = 0.30', lambda s: dict(s.d)[0] == F('0.3')),
        ('E(X) = 0 × 0.30 + 10 × 0.40 + 20 × 0.25 + 50 × 0.05 = 11.5', lambda s: 0 * F('0.3') + 10 * F('0.4') + 20 * F('0.25') + 50 * F('0.05') == s.E == F('11.5')),
    ],
    'es_gcse_029': [
        ('1 − 0.40 = 0.60', lambda s: 1 - F('0.4') == F('0.6')),
        ('P(X = 1) = 2 × P(X = 3)', lambda s: dict(s.d)[1] == 2 * dict(s.d)[3]),
        ('3 × P(X = 3) = 0.60', lambda s: 3 * F('0.2') == F('0.6')),
        ('P(X = 3) = 0.20', lambda s: dict(s.d)[3] == F('0.2')),
        ('P(X = 1) = 0.40', lambda s: dict(s.d)[1] == F('0.4')),
        ('E(X) = 1 × 0.40 + 2 × 0.30 + 3 × 0.20 + 6 × 0.10 = 2.2', lambda s: 1 * F('0.4') + 2 * F('0.3') + 3 * F('0.2') + 6 * F('0.1') == s.E == F('2.2')),
    ],
    'es_alevel_011': [
        ('k(1 + 2 + 3 + 4) = 10k = 1', lambda s: sum(p for _, p in s.d) == 1),
        ('k = 0.1', lambda s: all(p == F(1,10)*(x+1) for x, p in s.d)),
        ('P(X = 0) = 0.10', lambda s: dict(s.d)[0] == F('0.1')),
        ('P(X = 2) = 0.30', lambda s: dict(s.d)[2] == F('0.3')),
        ('E(X) = 0 × 0.10 + 1 × 0.20 + 2 × 0.30 + 3 × 0.40 = 2', lambda s: 0 * F('0.1') + 1 * F('0.2') + 2 * F('0.3') + 3 * F('0.4') == s.E == 2),
    ],
    'es_alevel_012': [
        ('k(4 + 3 + 2 + 1) = 10k = 1', lambda s: sum(p for _, p in s.d) == 1),
        ('k = 0.1', lambda s: all(p == F(1,10)*(5-x) for x, p in s.d)),
        ('P(X = 2) = 0.30', lambda s: dict(s.d)[2] == F('0.3')),
        ('P(X = 4) = 0.10', lambda s: dict(s.d)[4] == F('0.1')),
        ('E(X) = 1 × 0.40 + 2 × 0.30 + 3 × 0.20 + 4 × 0.10 = 2', lambda s: 1 * F('0.4') + 2 * F('0.3') + 3 * F('0.2') + 4 * F('0.1') == s.E == 2),
    ],
    'es_alevel_013': [
        ('k(1 + 2 + 5) = 8k = 1', lambda s: sum(p for _, p in s.d) == 1),
        ('k = 0.125', lambda s: all(p == F(1,8)*(x*x+1) for x, p in s.d)),
        ('P(X = 0) = 0.125', lambda s: dict(s.d)[0] == F('0.125')),
        ('P(X = 2) = 0.625', lambda s: dict(s.d)[2] == F('0.625')),
        ('E(X) = 0 × 0.125 + 1 × 0.25 + 2 × 0.625 = 1.5', lambda s: 0 * F('0.125') + 1 * F('0.25') + 2 * F('0.625') == s.E == F('1.5')),
    ],
    'es_alevel_014': [
        ('k(1 + 2 + 3 + 4) = 10k = 1', lambda s: sum(p for _, p in s.d) == 1),
        ('k = 0.1', lambda s: all(p == F(1,10)*(x+2) for x, p in s.d)),
        ('P(X = 0) = 0.20', lambda s: dict(s.d)[0] == F('0.2')),
        ('P(X = 2) = 0.40', lambda s: dict(s.d)[2] == F('0.4')),
        ('E(X) = (−1) × 0.10 + 0 × 0.20 + 1 × 0.30 + 2 × 0.40 = 1', lambda s: -1 * F('0.1') + 0 * F('0.2') + 1 * F('0.3') + 2 * F('0.4') == s.E == 1),
    ],
    'es_alevel_015': [
        ('k(4 + 3 + 2 + 1) = 10k = 1', lambda s: sum(p for _, p in s.d) == 1),
        ('k = 0.1', lambda s: all(p == F(1,10)*(6-x) for x, p in s.d)),
        ('P(X = 2) = 0.40', lambda s: dict(s.d)[2] == F('0.4')),
        ('P(X = 4) = 0.20', lambda s: dict(s.d)[4] == F('0.2')),
        ('E(X) = 2 × 0.40 + 3 × 0.30 + 4 × 0.20 + 5 × 0.10 = 3', lambda s: 2 * F('0.4') + 3 * F('0.3') + 4 * F('0.2') + 5 * F('0.1') == s.E == 3),
    ],
    'es_alevel_016': [
        ('k(2 + 3 + 5) = 10k = 1', lambda s: sum(p for _, p in s.d) == 1),
        ('k = 0.1', lambda s: all(p == F(1,10)*x for x, p in s.d)),
        ('P(X = 2) = 0.20', lambda s: dict(s.d)[2] == F('0.2')),
        ('P(X = 3) = 0.30', lambda s: dict(s.d)[3] == F('0.3')),
        ('E(X) = 2 × 0.20 + 3 × 0.30 + 5 × 0.50 = 3.8', lambda s: 2 * F('0.2') + 3 * F('0.3') + 5 * F('0.5') == s.E == F('3.8')),
    ],
    'es_alevel_017': [
        ('k(2 + 1 + 2) = 5k = 1', lambda s: sum(p for _, p in s.d) == 1),
        ('k = 0.2', lambda s: all(p == F(1,5)*(x*x+1) for x, p in s.d)),
        ('P(X = −1) = 0.40', lambda s: dict(s.d)[-1] == F('0.4')),
        ('P(X = 0) = 0.20', lambda s: dict(s.d)[0] == F('0.2')),
        ('E(X) = (−1) × 0.40 + 0 × 0.20 + 1 × 0.40 = 0', lambda s: -1 * F('0.4') + 0 * F('0.2') + 1 * F('0.4') == s.E == 0),
    ],
    'es_alevel_018': [
        ('k(1 + 2 + 3 + 4) = 10k = 1', lambda s: sum(p for _, p in s.d) == 1),
        ('k = 0.1', lambda s: all(p == F(1,10)*(x+3) for x, p in s.d)),
        ('P(X = −2) = 0.10', lambda s: dict(s.d)[-2] == F('0.1')),
        ('P(X = 1) = 0.40', lambda s: dict(s.d)[1] == F('0.4')),
        ('E(X) = (−2) × 0.10 + (−1) × 0.20 + 0 × 0.30 + 1 × 0.40 = 0', lambda s: -2 * F('0.1') + -1 * F('0.2') + 0 * F('0.3') + 1 * F('0.4') == s.E == 0),
    ],
    'es_alevel_019': [
        ('k(4 + 3 + 2 + 1) = 10k = 1', lambda s: sum(p for _, p in s.d) == 1),
        ('k = 0.1', lambda s: all(p == F(1,10)*(10-x) for x, p in s.d)),
        ('P(X = 7) = 0.30', lambda s: dict(s.d)[7] == F('0.3')),
        ('P(X = 8) = 0.20', lambda s: dict(s.d)[8] == F('0.2')),
        ('E(X) = 6 × 0.40 + 7 × 0.30 + 8 × 0.20 + 9 × 0.10 = 7', lambda s: 6 * F('0.4') + 7 * F('0.3') + 8 * F('0.2') + 9 * F('0.1') == s.E == 7),
    ],
    'es_alevel_020': [
        ('k(4 + 1 + 1 + 4) = 10k = 1', lambda s: sum(p for _, p in s.d) == 1),
        ('k = 0.1', lambda s: all(p == F(1,10)*x*x for x, p in s.d)),
        ('P(X = −1) = 0.10', lambda s: dict(s.d)[-1] == F('0.1')),
        ('P(X = 2) = 0.40', lambda s: dict(s.d)[2] == F('0.4')),
        ('E(X) = (−2) × 0.40 + (−1) × 0.10 + 1 × 0.10 + 2 × 0.40 = 0', lambda s: -2 * F('0.4') + -1 * F('0.1') + 1 * F('0.1') + 2 * F('0.4') == s.E == 0),
    ],
    'es_alevel_021': [
        ('p + q = 1 − 0.30 = 0.70', lambda s: dict(s.d)[2] + dict(s.d)[3] == 1 - F('0.3') == F('0.7')),
        ('2p + 3q = 2.7 − 0.9 = 1.8', lambda s: 2 * dict(s.d)[2] + 3 * dict(s.d)[3] == s.E - F('0.9') == F('1.8')),
        ('p = 0.30', lambda s: dict(s.d)[2] == F('0.3')),
        ('q = 0.40', lambda s: dict(s.d)[3] == F('0.4')),
        ('E(X) = 1 × 0.10 + 2 × 0.30 + 3 × 0.40 + 4 × 0.20 = 2.7', lambda s: 1 * F('0.1') + 2 * F('0.3') + 3 * F('0.4') + 4 * F('0.2') == s.E == F('2.7')),
    ],
    'es_alevel_022': [
        ('p + q = 1 − 0.65 = 0.35', lambda s: dict(s.d)[0] + dict(s.d)[3] == 1 - F('0.65') == F('0.35')),
        ('3q = 1.25 − 0.95 = 0.3', lambda s: 0 * dict(s.d)[0] + 3 * dict(s.d)[3] == s.E - F('0.95') == F('0.3')),
        ('p = 0.25', lambda s: dict(s.d)[0] == F('0.25')),
        ('q = 0.10', lambda s: dict(s.d)[3] == F('0.1')),
        ('E(X) = 0 × 0.25 + 1 × 0.35 + 2 × 0.30 + 3 × 0.10 = 1.25', lambda s: 0 * F('0.25') + 1 * F('0.35') + 2 * F('0.3') + 3 * F('0.1') == s.E == F('1.25')),
    ],
    'es_alevel_023': [
        ('p + q = 1 − 0.70 = 0.30', lambda s: dict(s.d)[-1] + dict(s.d)[2] == 1 - F('0.7') == F('0.3')),
        ('−p + 2q = 0.4 − 0.4 = 0', lambda s: -1 * dict(s.d)[-1] + 2 * dict(s.d)[2] == s.E - F('0.4') == 0),
        ('p = 0.20', lambda s: dict(s.d)[-1] == F('0.2')),
        ('q = 0.10', lambda s: dict(s.d)[2] == F('0.1')),
        ('E(X) = (−1) × 0.20 + 0 × 0.30 + 1 × 0.40 + 2 × 0.10 = 0.4', lambda s: -1 * F('0.2') + 0 * F('0.3') + 1 * F('0.4') + 2 * F('0.1') == s.E == F('0.4')),
    ],
    'es_alevel_024': [
        ('p + q = 1 − 0.55 = 0.45', lambda s: dict(s.d)[2] + dict(s.d)[4] == 1 - F('0.55') == F('0.45')),
        ('2p + 4q = 3.05 − 1.75 = 1.3', lambda s: 2 * dict(s.d)[2] + 4 * dict(s.d)[4] == s.E - F('1.75') == F('1.3')),
        ('p = 0.25', lambda s: dict(s.d)[2] == F('0.25')),
        ('q = 0.20', lambda s: dict(s.d)[4] == F('0.2')),
        ('E(X) = 1 × 0.10 + 2 × 0.25 + 3 × 0.30 + 4 × 0.20 + 5 × 0.15 = 3.05', lambda s: 1 * F('0.1') + 2 * F('0.25') + 3 * F('0.3') + 4 * F('0.2') + 5 * F('0.15') == s.E == F('3.05')),
    ],
    'es_alevel_025': [
        ('p + q = 1 − 0.45 = 0.55', lambda s: dict(s.d)[2] + dict(s.d)[6] == 1 - F('0.45') == F('0.55')),
        ('2p + 6q = 5.3 − 2.6 = 2.7', lambda s: 2 * dict(s.d)[2] + 6 * dict(s.d)[6] == s.E - F('2.6') == F('2.7')),
        ('p = 0.15', lambda s: dict(s.d)[2] == F('0.15')),
        ('q = 0.40', lambda s: dict(s.d)[6] == F('0.4')),
        ('E(X) = 2 × 0.15 + 4 × 0.25 + 6 × 0.40 + 8 × 0.20 = 5.3', lambda s: 2 * F('0.15') + 4 * F('0.25') + 6 * F('0.4') + 8 * F('0.2') == s.E == F('5.3')),
    ],
    'es_alevel_026': [
        ('p + q = 1 − 0.65 = 0.35', lambda s: dict(s.d)[3] + dict(s.d)[4] == 1 - F('0.65') == F('0.35')),
        ('3p + 4q = 2.15 − 1 = 1.15', lambda s: 3 * dict(s.d)[3] + 4 * dict(s.d)[4] == s.E - 1 == F('1.15')),
        ('p = 0.25', lambda s: dict(s.d)[3] == F('0.25')),
        ('q = 0.10', lambda s: dict(s.d)[4] == F('0.1')),
        ('E(X) = 0 × 0.05 + 1 × 0.20 + 2 × 0.40 + 3 × 0.25 + 4 × 0.10 = 2.15', lambda s: 0 * F('0.05') + 1 * F('0.2') + 2 * F('0.4') + 3 * F('0.25') + 4 * F('0.1') == s.E == F('2.15')),
    ],
    'es_alevel_027': [
        ('p + q = 1 − 0.20 = 0.80', lambda s: dict(s.d)[10] + dict(s.d)[20] == 1 - F('0.2') == F('0.8')),
        ('10p + 20q = 17 − 6 = 11', lambda s: 10 * dict(s.d)[10] + 20 * dict(s.d)[20] == s.E - 6 == 11),
        ('p = 0.50', lambda s: dict(s.d)[10] == F('0.5')),
        ('q = 0.30', lambda s: dict(s.d)[20] == F('0.3')),
        ('E(X) = 10 × 0.50 + 20 × 0.30 + 30 × 0.20 = 17', lambda s: 10 * F('0.5') + 20 * F('0.3') + 30 * F('0.2') == s.E == 17),
    ],
    'es_alevel_028': [
        ('p + q = 1 − 0.65 = 0.35', lambda s: dict(s.d)[-1] + dict(s.d)[2] == 1 - F('0.65') == F('0.35')),
        ('−p + 2q = 0.3 − 0.05 = 0.25', lambda s: -1 * dict(s.d)[-1] + 2 * dict(s.d)[2] == s.E - F('0.05') == F('0.25')),
        ('p = 0.15', lambda s: dict(s.d)[-1] == F('0.15')),
        ('q = 0.20', lambda s: dict(s.d)[2] == F('0.2')),
        ('E(X) = (−2) × 0.10 + (−1) × 0.15 + 0 × 0.30 + 1 × 0.25 + 2 × 0.20 = 0.3', lambda s: -2 * F('0.1') + -1 * F('0.15') + 0 * F('0.3') + 1 * F('0.25') + 2 * F('0.2') == s.E == F('0.3')),
    ],
    'es_alevel_029': [
        ('p + q = 1 − 0.35 = 0.65', lambda s: dict(s.d)[1] + dict(s.d)[3] == 1 - F('0.35') == F('0.65')),
        ('p + 3q = 1.75 − 0.7 = 1.05', lambda s: 1 * dict(s.d)[1] + 3 * dict(s.d)[3] == s.E - F('0.7') == F('1.05')),
        ('p = 0.45', lambda s: dict(s.d)[1] == F('0.45')),
        ('q = 0.20', lambda s: dict(s.d)[3] == F('0.2')),
        ('E(X) = 1 × 0.45 + 2 × 0.35 + 3 × 0.20 = 1.75', lambda s: 1 * F('0.45') + 2 * F('0.35') + 3 * F('0.2') == s.E == F('1.75')),
    ],
    'es_alevel_030': [
        ('p + q = 1 − 0.70 = 0.30', lambda s: dict(s.d)[10] + dict(s.d)[20] == 1 - F('0.7') == F('0.3')),
        ('10p + 20q = 5.5 − 1.5 = 4', lambda s: 10 * dict(s.d)[10] + 20 * dict(s.d)[20] == s.E - F('1.5') == 4),
        ('p = 0.20', lambda s: dict(s.d)[10] == F('0.2')),
        ('q = 0.10', lambda s: dict(s.d)[20] == F('0.1')),
        ('E(X) = 0 × 0.40 + 5 × 0.30 + 10 × 0.20 + 20 × 0.10 = 5.5', lambda s: 0 * F('0.4') + 5 * F('0.3') + 10 * F('0.2') + 20 * F('0.1') == s.E == F('5.5')),
    ],
    'es_alevel_031': [
        ('1 − 0.85 = 0.15', lambda s: 1 - F('0.85') == F('0.15')),
        ('P(X = 3) = 2 × P(X = −2)', lambda s: dict(s.d)[3] == 2 * dict(s.d)[-2]),
        ('3 × P(X = −2) = 0.15', lambda s: 3 * F('0.05') == F('0.15')),
        ('P(X = −2) = 0.05', lambda s: dict(s.d)[-2] == F('0.05')),
        ('P(X = 3) = 0.10', lambda s: dict(s.d)[3] == F('0.1')),
        ('E(X) = (−2) × 0.05 + (−1) × 0.10 + 0 × 0.20 + 1 × 0.30 + 2 × 0.25 + 3 × 0.10 = 0.9', lambda s: -2 * F('0.05') + -1 * F('0.1') + 0 * F('0.2') + 1 * F('0.3') + 2 * F('0.25') + 3 * F('0.1') == s.E == F('0.9')),
    ],
    'es_alevel_032': [
        ('1 − 0.95 = 0.05', lambda s: 1 - F('0.95') == F('0.05')),
        ('P(X = 3) = 4 × P(X = 4)', lambda s: dict(s.d)[3] == 4 * dict(s.d)[4]),
        ('5 × P(X = 4) = 0.05', lambda s: 5 * F('0.01') == F('0.05')),
        ('P(X = 4) = 0.01', lambda s: dict(s.d)[4] == F('0.01')),
        ('P(X = 3) = 0.04', lambda s: dict(s.d)[3] == F('0.04')),
        ('E(X) = 0 × 0.60 + 1 × 0.25 + 2 × 0.10 + 3 × 0.04 + 4 × 0.01 = 0.61', lambda s: 0 * F('0.6') + 1 * F('0.25') + 2 * F('0.1') + 3 * F('0.04') + 4 * F('0.01') == s.E == F('0.61')),
    ],
    'es_alevel_033': [
        ('1 − 0.72 = 0.28', lambda s: 1 - F('0.72') == F('0.28')),
        ('P(X = 1) = P(X = 2) + 0.12', lambda s: dict(s.d)[1] == dict(s.d)[2] + F('0.12')),
        ('2 × P(X = 2) + 0.12 = 0.28', lambda s: 2 * F('0.08') + F('0.12') == F('0.28')),
        ('P(X = 2) = 0.08', lambda s: dict(s.d)[2] == F('0.08')),
        ('P(X = 1) = 0.20', lambda s: dict(s.d)[1] == F('0.2')),
        ('E(X) = 0 × 0.70 + 1 × 0.20 + 2 × 0.08 + 3 × 0.02 = 0.42', lambda s: 0 * F('0.7') + 1 * F('0.2') + 2 * F('0.08') + 3 * F('0.02') == s.E == F('0.42')),
    ],
    'es_alevel_034': [
        ('1 − 0.80 = 0.20', lambda s: 1 - F('0.8') == F('0.2')),
        ('P(X = 4) = 3 × P(X = 5)', lambda s: dict(s.d)[4] == 3 * dict(s.d)[5]),
        ('4 × P(X = 5) = 0.20', lambda s: 4 * F('0.05') == F('0.2')),
        ('P(X = 5) = 0.05', lambda s: dict(s.d)[5] == F('0.05')),
        ('P(X = 4) = 0.15', lambda s: dict(s.d)[4] == F('0.15')),
        ('E(X) = 0 × 0.10 + 1 × 0.20 + 2 × 0.30 + 3 × 0.20 + 4 × 0.15 + 5 × 0.05 = 2.25', lambda s: 0 * F('0.1') + 1 * F('0.2') + 2 * F('0.3') + 3 * F('0.2') + 4 * F('0.15') + 5 * F('0.05') == s.E == F('2.25')),
    ],
    'es_alevel_035': [
        ('1 − 0.70 = 0.30', lambda s: 1 - F('0.7') == F('0.3')),
        ('P(X = 11) = 2 × P(X = 12)', lambda s: dict(s.d)[11] == 2 * dict(s.d)[12]),
        ('3 × P(X = 12) = 0.30', lambda s: 3 * F('0.1') == F('0.3')),
        ('P(X = 12) = 0.10', lambda s: dict(s.d)[12] == F('0.1')),
        ('P(X = 11) = 0.20', lambda s: dict(s.d)[11] == F('0.2')),
        ('E(X) = 8 × 0.05 + 9 × 0.15 + 10 × 0.50 + 11 × 0.20 + 12 × 0.10 = 10.15', lambda s: 8 * F('0.05') + 9 * F('0.15') + 10 * F('0.5') + 11 * F('0.2') + 12 * F('0.1') == s.E == F('10.15')),
    ],
    'es_alevel_036': [
        ('1 − 0.85 = 0.15', lambda s: 1 - F('0.85') == F('0.15')),
        ('P(X = 2) = 2 × P(X = 3)', lambda s: dict(s.d)[2] == 2 * dict(s.d)[3]),
        ('3 × P(X = 3) = 0.15', lambda s: 3 * F('0.05') == F('0.15')),
        ('P(X = 3) = 0.05', lambda s: dict(s.d)[3] == F('0.05')),
        ('P(X = 2) = 0.10', lambda s: dict(s.d)[2] == F('0.1')),
        ('E(X) = 0 × 0.55 + 1 × 0.30 + 2 × 0.10 + 3 × 0.05 = 0.65', lambda s: 0 * F('0.55') + 1 * F('0.3') + 2 * F('0.1') + 3 * F('0.05') == s.E == F('0.65')),
    ],
    'es_alevel_037': [
        ('1 − 0.70 = 0.30', lambda s: 1 - F('0.7') == F('0.3')),
        ('P(X = 3) = 2 × P(X = 4)', lambda s: dict(s.d)[3] == 2 * dict(s.d)[4]),
        ('3 × P(X = 4) = 0.30', lambda s: 3 * F('0.1') == F('0.3')),
        ('P(X = 4) = 0.10', lambda s: dict(s.d)[4] == F('0.1')),
        ('P(X = 3) = 0.20', lambda s: dict(s.d)[3] == F('0.2')),
        ('E(X) = 0 × 0.15 + 1 × 0.30 + 2 × 0.25 + 3 × 0.20 + 4 × 0.10 = 1.8', lambda s: 0 * F('0.15') + 1 * F('0.3') + 2 * F('0.25') + 3 * F('0.2') + 4 * F('0.1') == s.E == F('1.8')),
    ],
    'es_alevel_038': [
        ('1 − 0.65 = 0.35', lambda s: 1 - F('0.65') == F('0.35')),
        ('P(X = 10) = P(X = −5) + 0.15', lambda s: dict(s.d)[10] == dict(s.d)[-5] + F('0.15')),
        ('2 × P(X = −5) + 0.15 = 0.35', lambda s: 2 * F('0.1') + F('0.15') == F('0.35')),
        ('P(X = −5) = 0.10', lambda s: dict(s.d)[-5] == F('0.1')),
        ('P(X = 10) = 0.25', lambda s: dict(s.d)[10] == F('0.25')),
        ('E(X) = (−5) × 0.10 + 0 × 0.20 + 5 × 0.45 + 10 × 0.25 = 4.25', lambda s: -5 * F('0.1') + 0 * F('0.2') + 5 * F('0.45') + 10 * F('0.25') == s.E == F('4.25')),
    ],
    'es_alevel_039': [
        ('1 − 0.85 = 0.15', lambda s: 1 - F('0.85') == F('0.15')),
        ('P(X = 3) = 2 × P(X = 4)', lambda s: dict(s.d)[3] == 2 * dict(s.d)[4]),
        ('3 × P(X = 4) = 0.15', lambda s: 3 * F('0.05') == F('0.15')),
        ('P(X = 4) = 0.05', lambda s: dict(s.d)[4] == F('0.05')),
        ('P(X = 3) = 0.10', lambda s: dict(s.d)[3] == F('0.1')),
        ('E(X) = 0 × 0.30 + 1 × 0.35 + 2 × 0.20 + 3 × 0.10 + 4 × 0.05 = 1.25', lambda s: 0 * F('0.3') + 1 * F('0.35') + 2 * F('0.2') + 3 * F('0.1') + 4 * F('0.05') == s.E == F('1.25')),
    ],
    'es_alevel_040': [
        ('1 − 0.70 = 0.30', lambda s: 1 - F('0.7') == F('0.3')),
        ('P(X = 3) = 2 × P(X = 0)', lambda s: dict(s.d)[3] == 2 * dict(s.d)[0]),
        ('3 × P(X = 0) = 0.30', lambda s: 3 * F('0.1') == F('0.3')),
        ('P(X = 0) = 0.10', lambda s: dict(s.d)[0] == F('0.1')),
        ('P(X = 3) = 0.20', lambda s: dict(s.d)[3] == F('0.2')),
        ('E(X) = 0 × 0.10 + 1 × 0.30 + 2 × 0.40 + 3 × 0.20 = 1.7', lambda s: 0 * F('0.1') + 1 * F('0.3') + 2 * F('0.4') + 3 * F('0.2') == s.E == F('1.7')),
    ],
}

# The 33 items whose Stage 1 had two answers (expectation-station-pc-001) now open their explanation with the
# working from their stated relation; those claims are added to each item's entry.
FIGURES_ADDED = {
    'es_core_001': [  # add to the existing entry
        ('1 − 0.45 = 0.55', lambda s: 1 - F('0.45') == F('0.55')),
        ('P(X = 2) = P(X = 4) + 0.05', lambda s: dict(s.d)[2] == dict(s.d)[4] + F('0.05')),
        ('2 × P(X = 4) + 0.05 = 0.55', lambda s: 2 * dict(s.d)[4] + F('0.05') == F('0.55')),
        ('P(X = 4) = 0.25', lambda s: dict(s.d)[4] == F('0.25')),
        ('P(X = 2) = 0.30', lambda s: dict(s.d)[2] == F('0.30')),
    ],
    'es_core_002': [  # add to the existing entry
        ('1 − 0.65 = 0.35', lambda s: 1 - F('0.65') == F('0.35')),
        ('P(X = 1) = P(X = 5) + 0.15', lambda s: dict(s.d)[1] == dict(s.d)[5] + F('0.15')),
        ('2 × P(X = 5) + 0.15 = 0.35', lambda s: 2 * dict(s.d)[5] + F('0.15') == F('0.35')),
        ('P(X = 5) = 0.10', lambda s: dict(s.d)[5] == F('0.10')),
        ('P(X = 1) = 0.25', lambda s: dict(s.d)[1] == F('0.25')),
    ],
    'es_core_003': [  # add to the existing entry
        ('1 − 0.50 = 0.50', lambda s: 1 - F('0.50') == F('0.50')),
        ('P(X = 0) = 4 × P(X = 3)', lambda s: dict(s.d)[0] == 4 * dict(s.d)[3]),
        ('5 × P(X = 3) = 0.50', lambda s: 5 * dict(s.d)[3] == F('0.50')),
        ('P(X = 3) = 0.10', lambda s: dict(s.d)[3] == F('0.10')),
        ('P(X = 0) = 0.40', lambda s: dict(s.d)[0] == F('0.40')),
    ],
    'es_core_004': [  # add to the existing entry
        ('1 − 0.75 = 0.25', lambda s: 1 - F('0.75') == F('0.25')),
        ('P(X = 1) = 4 × P(X = 3)', lambda s: dict(s.d)[1] == 4 * dict(s.d)[3]),
        ('5 × P(X = 3) = 0.25', lambda s: 5 * dict(s.d)[3] == F('0.25')),
        ('P(X = 3) = 0.05', lambda s: dict(s.d)[3] == F('0.05')),
        ('P(X = 1) = 0.20', lambda s: dict(s.d)[1] == F('0.20')),
    ],
    'es_core_005': [  # add to the existing entry
        ('1 − 0.25 = 0.75', lambda s: 1 - F('0.25') == F('0.75')),
        ('P(X = 0) = P(X = 3) + 0.69', lambda s: dict(s.d)[0] == dict(s.d)[3] + F('0.69')),
        ('2 × P(X = 3) + 0.69 = 0.75', lambda s: 2 * dict(s.d)[3] + F('0.69') == F('0.75')),
        ('P(X = 3) = 0.03', lambda s: dict(s.d)[3] == F('0.03')),
        ('P(X = 0) = 0.72', lambda s: dict(s.d)[0] == F('0.72')),
    ],
    'es_core_006': [  # add to the existing entry
        ('1 − 0.45 = 0.55', lambda s: 1 - F('0.45') == F('0.55')),
        ('P(X = 5) = P(X = 15) + 0.15', lambda s: dict(s.d)[5] == dict(s.d)[15] + F('0.15')),
        ('2 × P(X = 15) + 0.15 = 0.55', lambda s: 2 * dict(s.d)[15] + F('0.15') == F('0.55')),
        ('P(X = 15) = 0.20', lambda s: dict(s.d)[15] == F('0.20')),
        ('P(X = 5) = 0.35', lambda s: dict(s.d)[5] == F('0.35')),
    ],
    'es_core_007': [  # add to the existing entry
        ('1 − 0.70 = 0.30', lambda s: 1 - F('0.70') == F('0.30')),
        ('P(X = 2) = P(X = 4) + 0.20', lambda s: dict(s.d)[2] == dict(s.d)[4] + F('0.20')),
        ('2 × P(X = 4) + 0.20 = 0.30', lambda s: 2 * dict(s.d)[4] + F('0.20') == F('0.30')),
        ('P(X = 4) = 0.05', lambda s: dict(s.d)[4] == F('0.05')),
        ('P(X = 2) = 0.25', lambda s: dict(s.d)[2] == F('0.25')),
    ],
    'es_core_008': [  # add to the existing entry
        ('1 − 0.40 = 0.60', lambda s: 1 - F('0.40') == F('0.60')),
        ('P(X = 0) = 3 × P(X = 2)', lambda s: dict(s.d)[0] == 3 * dict(s.d)[2]),
        ('4 × P(X = 2) = 0.60', lambda s: 4 * dict(s.d)[2] == F('0.60')),
        ('P(X = 2) = 0.15', lambda s: dict(s.d)[2] == F('0.15')),
        ('P(X = 0) = 0.45', lambda s: dict(s.d)[0] == F('0.45')),
    ],
    'es_core_009': [  # add to the existing entry
        ('1 − 0.65 = 0.35', lambda s: 1 - F('0.65') == F('0.35')),
        ('P(X = 1) = P(X = 3) + 0.25', lambda s: dict(s.d)[1] == dict(s.d)[3] + F('0.25')),
        ('2 × P(X = 3) + 0.25 = 0.35', lambda s: 2 * dict(s.d)[3] + F('0.25') == F('0.35')),
        ('P(X = 3) = 0.05', lambda s: dict(s.d)[3] == F('0.05')),
        ('P(X = 1) = 0.30', lambda s: dict(s.d)[1] == F('0.30')),
    ],
    'es_core_010': [  # add to the existing entry
        ('1 − 0.65 = 0.35', lambda s: 1 - F('0.65') == F('0.35')),
        ('P(X = 0) = P(X = 3) + 0.05', lambda s: dict(s.d)[0] == dict(s.d)[3] + F('0.05')),
        ('2 × P(X = 3) + 0.05 = 0.35', lambda s: 2 * dict(s.d)[3] + F('0.05') == F('0.35')),
        ('P(X = 3) = 0.15', lambda s: dict(s.d)[3] == F('0.15')),
        ('P(X = 0) = 0.20', lambda s: dict(s.d)[0] == F('0.20')),
    ],
    'es_core_011': [  # add to the existing entry
        ('1 − 0.50 = 0.50', lambda s: 1 - F('0.50') == F('0.50')),
        ('P(X = 1) = 4 × P(X = 3)', lambda s: dict(s.d)[1] == 4 * dict(s.d)[3]),
        ('5 × P(X = 3) = 0.50', lambda s: 5 * dict(s.d)[3] == F('0.50')),
        ('P(X = 3) = 0.10', lambda s: dict(s.d)[3] == F('0.10')),
        ('P(X = 1) = 0.40', lambda s: dict(s.d)[1] == F('0.40')),
    ],
    'es_core_012': [  # add to the existing entry
        ('1 − 0.17 = 0.83', lambda s: 1 - F('0.17') == F('0.83')),
        ('P(X = 0) = P(X = 3) + 0.77', lambda s: dict(s.d)[0] == dict(s.d)[3] + F('0.77')),
        ('2 × P(X = 3) + 0.77 = 0.83', lambda s: 2 * dict(s.d)[3] + F('0.77') == F('0.83')),
        ('P(X = 3) = 0.03', lambda s: dict(s.d)[3] == F('0.03')),
        ('P(X = 0) = 0.80', lambda s: dict(s.d)[0] == F('0.80')),
    ],
    'es_core_014': [  # add to the existing entry
        ('1 − 0.70 = 0.30', lambda s: 1 - F('0.70') == F('0.30')),
        ('P(X = 4) = 2 × P(X = 1)', lambda s: dict(s.d)[4] == 2 * dict(s.d)[1]),
        ('3 × P(X = 1) = 0.30', lambda s: 3 * dict(s.d)[1] == F('0.30')),
        ('P(X = 1) = 0.10', lambda s: dict(s.d)[1] == F('0.10')),
        ('P(X = 4) = 0.20', lambda s: dict(s.d)[4] == F('0.20')),
    ],
    'es_core_015': [  # add to the existing entry
        ('1 − 0.50 = 0.50', lambda s: 1 - F('0.50') == F('0.50')),
        ('P(X = 2) = P(X = 4) + 0.10', lambda s: dict(s.d)[2] == dict(s.d)[4] + F('0.10')),
        ('2 × P(X = 4) + 0.10 = 0.50', lambda s: 2 * dict(s.d)[4] + F('0.10') == F('0.50')),
        ('P(X = 4) = 0.20', lambda s: dict(s.d)[4] == F('0.20')),
        ('P(X = 2) = 0.30', lambda s: dict(s.d)[2] == F('0.30')),
    ],
    'es_core_016': [  # add to the existing entry
        ('1 − 0.60 = 0.40', lambda s: 1 - F('0.60') == F('0.40')),
        ('P(X = 0) = P(X = 3) + 0.10', lambda s: dict(s.d)[0] == dict(s.d)[3] + F('0.10')),
        ('2 × P(X = 3) + 0.10 = 0.40', lambda s: 2 * dict(s.d)[3] + F('0.10') == F('0.40')),
        ('P(X = 3) = 0.15', lambda s: dict(s.d)[3] == F('0.15')),
        ('P(X = 0) = 0.25', lambda s: dict(s.d)[0] == F('0.25')),
    ],
    'es_core_017': [  # add to the existing entry
        ('1 − 0.50 = 0.50', lambda s: 1 - F('0.50') == F('0.50')),
        ('P(X = 3) = P(X = 5) + 0.10', lambda s: dict(s.d)[3] == dict(s.d)[5] + F('0.10')),
        ('2 × P(X = 5) + 0.10 = 0.50', lambda s: 2 * dict(s.d)[5] + F('0.10') == F('0.50')),
        ('P(X = 5) = 0.20', lambda s: dict(s.d)[5] == F('0.20')),
        ('P(X = 3) = 0.30', lambda s: dict(s.d)[3] == F('0.30')),
    ],
    'es_core_018': [  # add to the existing entry
        ('1 − 0.70 = 0.30', lambda s: 1 - F('0.70') == F('0.30')),
        ('P(X = 1) = P(X = 3) + 0.20', lambda s: dict(s.d)[1] == dict(s.d)[3] + F('0.20')),
        ('2 × P(X = 3) + 0.20 = 0.30', lambda s: 2 * dict(s.d)[3] + F('0.20') == F('0.30')),
        ('P(X = 3) = 0.05', lambda s: dict(s.d)[3] == F('0.05')),
        ('P(X = 1) = 0.25', lambda s: dict(s.d)[1] == F('0.25')),
    ],
    'es_core_019': [  # add to the existing entry
        ('1 − 0.65 = 0.35', lambda s: 1 - F('0.65') == F('0.35')),
        ('P(X = 0) = P(X = 3) + 0.05', lambda s: dict(s.d)[0] == dict(s.d)[3] + F('0.05')),
        ('2 × P(X = 3) + 0.05 = 0.35', lambda s: 2 * dict(s.d)[3] + F('0.05') == F('0.35')),
        ('P(X = 3) = 0.15', lambda s: dict(s.d)[3] == F('0.15')),
        ('P(X = 0) = 0.20', lambda s: dict(s.d)[0] == F('0.20')),
    ],
    'es_core_020': [  # add to the existing entry
        ('1 − 0.60 = 0.40', lambda s: 1 - F('0.60') == F('0.40')),
        ('P(X = 2) = 3 × P(X = 4)', lambda s: dict(s.d)[2] == 3 * dict(s.d)[4]),
        ('4 × P(X = 4) = 0.40', lambda s: 4 * dict(s.d)[4] == F('0.40')),
        ('P(X = 4) = 0.10', lambda s: dict(s.d)[4] == F('0.10')),
        ('P(X = 2) = 0.30', lambda s: dict(s.d)[2] == F('0.30')),
    ],
    'es_gcse_002': [  # add to the existing entry
        ('1 − 0.40 = 0.60', lambda s: 1 - F('0.40') == F('0.60')),
        ('P(X = 4) = P(X = 5) + 0.10', lambda s: dict(s.d)[4] == dict(s.d)[5] + F('0.10')),
        ('2 × P(X = 5) + 0.10 = 0.60', lambda s: 2 * dict(s.d)[5] + F('0.10') == F('0.60')),
        ('P(X = 5) = 0.25', lambda s: dict(s.d)[5] == F('0.25')),
        ('P(X = 4) = 0.35', lambda s: dict(s.d)[4] == F('0.35')),
    ],
    'es_gcse_004': [  # add to the existing entry
        ('1 − 0.60 = 0.40', lambda s: 1 - F('0.60') == F('0.40')),
        ('P(X = 0) = 3 × P(X = 3)', lambda s: dict(s.d)[0] == 3 * dict(s.d)[3]),
        ('4 × P(X = 3) = 0.40', lambda s: 4 * dict(s.d)[3] == F('0.40')),
        ('P(X = 3) = 0.10', lambda s: dict(s.d)[3] == F('0.10')),
        ('P(X = 0) = 0.30', lambda s: dict(s.d)[0] == F('0.30')),
    ],
    'es_gcse_007': [  # add to the existing entry
        ('1 − 0.45 = 0.55', lambda s: 1 - F('0.45') == F('0.55')),
        ('P(X = 1) = P(X = 2) + 0.15', lambda s: dict(s.d)[1] == dict(s.d)[2] + F('0.15')),
        ('2 × P(X = 2) + 0.15 = 0.55', lambda s: 2 * dict(s.d)[2] + F('0.15') == F('0.55')),
        ('P(X = 2) = 0.20', lambda s: dict(s.d)[2] == F('0.20')),
        ('P(X = 1) = 0.35', lambda s: dict(s.d)[1] == F('0.35')),
    ],
    'es_gcse_008': [  # add to the existing entry
        ('1 − 1/2 = 1/2', lambda s: 1 - F(1, 2) == F(1, 2)),
        ('P(X = 2) = 2 × P(X = 3)', lambda s: dict(s.d)[2] == 2 * dict(s.d)[3]),
        ('3 × P(X = 3) = 1/2', lambda s: 3 * dict(s.d)[3] == F(1, 2)),
        ('P(X = 3) = 1/6', lambda s: dict(s.d)[3] == F('1/6')),
        ('P(X = 2) = 1/3', lambda s: dict(s.d)[2] == F('1/3')),
    ],
    'es_gcse_009': [  # add to the existing entry
        ('1 − 0.45 = 0.55', lambda s: 1 - F('0.45') == F('0.55')),
        ('P(X = 0) = P(X = 3) + 0.45', lambda s: dict(s.d)[0] == dict(s.d)[3] + F('0.45')),
        ('2 × P(X = 3) + 0.45 = 0.55', lambda s: 2 * dict(s.d)[3] + F('0.45') == F('0.55')),
        ('P(X = 3) = 0.05', lambda s: dict(s.d)[3] == F('0.05')),
        ('P(X = 0) = 0.50', lambda s: dict(s.d)[0] == F('0.50')),
    ],
    'es_gcse_010': [  # add to the existing entry
        ('1 − 0.50 = 0.50', lambda s: 1 - F('0.50') == F('0.50')),
        ('P(X = 6) = P(X = 8) + 0.10', lambda s: dict(s.d)[6] == dict(s.d)[8] + F('0.10')),
        ('2 × P(X = 8) + 0.10 = 0.50', lambda s: 2 * dict(s.d)[8] + F('0.10') == F('0.50')),
        ('P(X = 8) = 0.20', lambda s: dict(s.d)[8] == F('0.20')),
        ('P(X = 6) = 0.30', lambda s: dict(s.d)[6] == F('0.30')),
    ],
    'es_gcse_011': [  # add to the existing entry
        ('1 − 0.35 = 0.65', lambda s: 1 - F('0.35') == F('0.65')),
        ('P(X = 0) = P(X = 3) + 0.55', lambda s: dict(s.d)[0] == dict(s.d)[3] + F('0.55')),
        ('2 × P(X = 3) + 0.55 = 0.65', lambda s: 2 * dict(s.d)[3] + F('0.55') == F('0.65')),
        ('P(X = 3) = 0.05', lambda s: dict(s.d)[3] == F('0.05')),
        ('P(X = 0) = 0.60', lambda s: dict(s.d)[0] == F('0.60')),
    ],
    'es_gcse_012': [  # add to the existing entry
        ('1 − 0.60 = 0.40', lambda s: 1 - F('0.60') == F('0.40')),
        ('P(X = 1) = 3 × P(X = 3)', lambda s: dict(s.d)[1] == 3 * dict(s.d)[3]),
        ('4 × P(X = 3) = 0.40', lambda s: 4 * dict(s.d)[3] == F('0.40')),
        ('P(X = 3) = 0.10', lambda s: dict(s.d)[3] == F('0.10')),
        ('P(X = 1) = 0.30', lambda s: dict(s.d)[1] == F('0.30')),
    ],
    'es_gcse_013': [  # add to the existing entry
        ('1 − 0.70 = 0.30', lambda s: 1 - F('0.70') == F('0.30')),
        ('P(X = 0) = 2 × P(X = 3)', lambda s: dict(s.d)[0] == 2 * dict(s.d)[3]),
        ('3 × P(X = 3) = 0.30', lambda s: 3 * dict(s.d)[3] == F('0.30')),
        ('P(X = 3) = 0.10', lambda s: dict(s.d)[3] == F('0.10')),
        ('P(X = 0) = 0.20', lambda s: dict(s.d)[0] == F('0.20')),
    ],
    'es_gcse_015': [  # add to the existing entry
        ('1 − 0.60 = 0.40', lambda s: 1 - F('0.60') == F('0.40')),
        ('P(X = 0) = 3 × P(X = 3)', lambda s: dict(s.d)[0] == 3 * dict(s.d)[3]),
        ('4 × P(X = 3) = 0.40', lambda s: 4 * dict(s.d)[3] == F('0.40')),
        ('P(X = 3) = 0.10', lambda s: dict(s.d)[3] == F('0.10')),
        ('P(X = 0) = 0.30', lambda s: dict(s.d)[0] == F('0.30')),
    ],
    'es_alevel_001': [  # add to the existing entry
        ('1 − 0.70 = 0.30', lambda s: 1 - F('0.70') == F('0.30')),
        ('P(X = 2) = 2 × P(X = 1)', lambda s: dict(s.d)[2] == 2 * dict(s.d)[1]),
        ('3 × P(X = 1) = 0.30', lambda s: 3 * dict(s.d)[1] == F('0.30')),
        ('P(X = 1) = 0.10', lambda s: dict(s.d)[1] == F('0.10')),
        ('P(X = 2) = 0.20', lambda s: dict(s.d)[2] == F('0.20')),
    ],
    'es_alevel_002': [  # add to the existing entry
        ('1 − 0.60 = 0.40', lambda s: 1 - F('0.60') == F('0.40')),
        ('P(X = 0) = 3 × P(X = 3)', lambda s: dict(s.d)[0] == 3 * dict(s.d)[3]),
        ('4 × P(X = 3) = 0.40', lambda s: 4 * dict(s.d)[3] == F('0.40')),
        ('P(X = 3) = 0.10', lambda s: dict(s.d)[3] == F('0.10')),
        ('P(X = 0) = 0.30', lambda s: dict(s.d)[0] == F('0.30')),
    ],
    'es_alevel_004': [  # add to the existing entry
        ('1 − 0.65 = 0.35', lambda s: 1 - F('0.65') == F('0.35')),
        ('P(X = 1) = P(X = 3) + 0.25', lambda s: dict(s.d)[1] == dict(s.d)[3] + F('0.25')),
        ('2 × P(X = 3) + 0.25 = 0.35', lambda s: 2 * dict(s.d)[3] + F('0.25') == F('0.35')),
        ('P(X = 3) = 0.05', lambda s: dict(s.d)[3] == F('0.05')),
        ('P(X = 1) = 0.30', lambda s: dict(s.d)[1] == F('0.30')),
    ],
    'es_alevel_007': [  # add to the existing entry
        ('1 − 0.70 = 0.30', lambda s: 1 - F('0.70') == F('0.30')),
        ('P(X = 7) = 2 × P(X = 1)', lambda s: dict(s.d)[7] == 2 * dict(s.d)[1]),
        ('3 × P(X = 1) = 0.30', lambda s: 3 * dict(s.d)[1] == F('0.30')),
        ('P(X = 1) = 0.10', lambda s: dict(s.d)[1] == F('0.10')),
        ('P(X = 7) = 0.20', lambda s: dict(s.d)[7] == F('0.20')),
    ],
}
# Each E(X)-given A-Level item (es_alevel_021 to 030) opens by naming its two unknowns: a definition, true by
# construction. The claims that follow it are in the item's own entry. (Added on 8 Oct 2026; not in the bundle.)
FIGURES_ADDED.update({
    'es_alevel_021': [('Let P(X = 2) = p and P(X = 3) = q', lambda s: True)],
    'es_alevel_022': [('Let P(X = 0) = p and P(X = 3) = q', lambda s: True)],
    'es_alevel_023': [('Let P(X = −1) = p and P(X = 2) = q', lambda s: True)],
    'es_alevel_024': [('Let P(X = 2) = p and P(X = 4) = q', lambda s: True)],
    'es_alevel_025': [('Let P(X = 2) = p and P(X = 6) = q', lambda s: True)],
    'es_alevel_026': [('Let P(X = 3) = p and P(X = 4) = q', lambda s: True)],
    'es_alevel_027': [('Let P(X = 10) = p and P(X = 20) = q', lambda s: True)],
    'es_alevel_028': [('Let P(X = −1) = p and P(X = 2) = q', lambda s: True)],
    'es_alevel_029': [('Let P(X = 1) = p and P(X = 3) = q', lambda s: True)],
    'es_alevel_030': [('Let P(X = 10) = p and P(X = 20) = q', lambda s: True)],
})
for _qid, _extra in FIGURES_ADDED.items():
    FIGURES[_qid] = FIGURES[_qid] + _extra


# Stage 1 (expectation-station-pc-001, Jon's ruling B, 7 Oct 2026): what the item states, beyond "the probabilities
# sum to 1", that fixes the missing cells. Every item has an entry; the uniqueness check in check_bank uses it.
#   ('none',)                  nothing more is needed: one missing cell, or the missing values are equal
#   ('ratio', xa, xb, k)       P(X = xa) = k * P(X = xb), stated in the context as "P(X = xa) is twice P(X = xb)"
#                              (three times, four times)
#   ('diff', xa, xb, d)        P(X = xa) = P(X = xb) + d, stated as "P(X = xa) is d more than P(X = xb)"
#   ('mean', E)                E(X) = E, stated as "E(X) = E"
#   ('func', 'expr in x')      P(X = x) = expr for every x in the table (F and comb available)
CLUES = {
    # The 33 items given a relation by Project Claude's bundle (7 Oct 2026).
    'es_core_001': ('diff', 2, 4, F('0.05')),
    'es_core_002': ('diff', 1, 5, F('0.15')),
    'es_core_003': ('ratio', 0, 3, 4),
    'es_core_004': ('ratio', 1, 3, 4),
    'es_core_005': ('diff', 0, 3, F('0.69')),
    'es_core_006': ('diff', 5, 15, F('0.15')),
    'es_core_007': ('diff', 2, 4, F('0.20')),
    'es_core_008': ('ratio', 0, 2, 3),
    'es_core_009': ('diff', 1, 3, F('0.25')),
    'es_core_010': ('diff', 0, 3, F('0.05')),
    'es_core_011': ('ratio', 1, 3, 4),
    'es_core_012': ('diff', 0, 3, F('0.77')),
    'es_core_014': ('ratio', 4, 1, 2),
    'es_core_015': ('diff', 2, 4, F('0.10')),
    'es_core_016': ('diff', 0, 3, F('0.10')),
    'es_core_017': ('diff', 3, 5, F('0.10')),
    'es_core_018': ('diff', 1, 3, F('0.20')),
    'es_core_019': ('diff', 0, 3, F('0.05')),
    'es_core_020': ('ratio', 2, 4, 3),
    'es_gcse_002': ('diff', 4, 5, F('0.10')),
    'es_gcse_004': ('ratio', 0, 3, 3),
    'es_gcse_007': ('diff', 1, 2, F('0.15')),
    'es_gcse_008': ('ratio', 2, 3, 2),
    'es_gcse_009': ('diff', 0, 3, F('0.45')),
    'es_gcse_010': ('diff', 6, 8, F('0.10')),
    'es_gcse_011': ('diff', 0, 3, F('0.55')),
    'es_gcse_012': ('ratio', 1, 3, 3),
    'es_gcse_013': ('ratio', 0, 3, 2),
    'es_gcse_015': ('ratio', 0, 3, 3),
    'es_alevel_001': ('ratio', 2, 1, 2),
    'es_alevel_002': ('ratio', 0, 3, 3),
    'es_alevel_004': ('diff', 1, 3, F('0.25')),
    'es_alevel_007': ('ratio', 7, 1, 2),
    # The 75 items added on 8 Oct 2026.
    'es_core_021': ('ratio', 2, 0, 4),
    'es_core_022': ('ratio', 0, 2, 2),
    'es_core_024': ('diff', 1, 3, F('0.25')),
    'es_core_025': ('diff', 1, 3, F('0.2')),
    'es_core_026': ('ratio', 2, 3, 2),
    'es_core_027': ('diff', 0, 4, F('0.05')),
    'es_core_028': ('diff', 0, 2, F('0.35')),
    'es_core_029': ('diff', 1, 3, F('0.3')),
    'es_core_031': ('ratio', 3, 4, 3),
    'es_core_032': ('diff', 1, 2, F('0.1')),
    'es_core_033': ('diff', 0, 3, F('0.3')),
    'es_core_034': ('ratio', 1, 3, 4),
    'es_core_035': ('diff', 2, 3, F('0.2')),
    'es_core_036': ('ratio', 3, 0, 2),
    'es_core_038': ('ratio', 3, 4, 2),
    'es_core_039': ('diff', 1, 3, F('0.25')),
    'es_core_040': ('ratio', 1, 4, 2),
    'es_core_023': ('ratio', 100, 250, 3),
    'es_core_030': ('ratio', 5, 20, 4),
    'es_core_037': ('ratio', 3, 10, 2),
    'es_gcse_018': ('ratio', 2, 3, 2),
    'es_gcse_019': ('diff', 0, 4, F('0.2')),
    'es_gcse_020': ('diff', 1, 2, F('0.15')),
    'es_gcse_021': ('diff', 0, 3, F('0.25')),
    'es_gcse_022': ('ratio', 2, 3, 3),
    'es_gcse_025': ('ratio', 1, 0, 2),
    'es_gcse_026': ('ratio', 3, 4, 2),
    'es_gcse_027': ('ratio', 2, 4, 3),
    'es_gcse_028': ('diff', 0, 3, F('0.25')),
    'es_gcse_030': ('ratio', 1, 3, 4),
    'es_gcse_031': ('diff', 2, 3, F('0.2')),
    'es_gcse_032': ('ratio', 2, 3, 2),
    'es_gcse_033': ('ratio', 0, 4, 2),
    'es_gcse_034': ('ratio', 1, 0, 3),
    'es_gcse_035': ('diff', 1, 3, F('0.2')),
    'es_gcse_036': ('ratio', 5, 10, 3),
    'es_gcse_037': ('diff', 0, 2, F('0.1')),
    'es_gcse_038': ('diff', 1, 2, F('0.1')),
    'es_gcse_039': ('ratio', 2, 3, 3),
    'es_gcse_040': ('ratio', 2, 3, 3),
    'es_gcse_023': ('ratio', 5, 20, 4),
    'es_gcse_016': ('ratio', 4, 1, 4),
    'es_gcse_017': ('diff', 2, 5, F('0.1')),
    'es_gcse_024': ('diff', 0, 50, F('0.25')),
    'es_gcse_029': ('ratio', 1, 3, 2),
    'es_alevel_031': ('ratio', 3, -2, 2),
    'es_alevel_032': ('ratio', 3, 4, 4),
    'es_alevel_033': ('diff', 1, 2, F('0.12')),
    'es_alevel_034': ('ratio', 4, 5, 3),
    'es_alevel_035': ('ratio', 11, 12, 2),
    'es_alevel_036': ('ratio', 2, 3, 2),
    'es_alevel_037': ('ratio', 3, 4, 2),
    'es_alevel_038': ('diff', 10, -5, F('0.15')),
    'es_alevel_039': ('ratio', 3, 4, 2),
    'es_alevel_040': ('ratio', 3, 0, 2),
    'es_alevel_011': ('func', 'F(1,10)*(x+1)'),
    'es_alevel_012': ('func', 'F(1,10)*(5-x)'),
    'es_alevel_013': ('func', 'F(1,8)*(x*x+1)'),
    'es_alevel_014': ('func', 'F(1,10)*(x+2)'),
    'es_alevel_015': ('func', 'F(1,10)*(6-x)'),
    'es_alevel_016': ('func', 'F(1,10)*x'),
    'es_alevel_017': ('func', 'F(1,5)*(x*x+1)'),
    'es_alevel_018': ('func', 'F(1,10)*(x+3)'),
    'es_alevel_019': ('func', 'F(1,10)*(10-x)'),
    'es_alevel_020': ('func', 'F(1,10)*x*x'),
    'es_alevel_021': ('mean', F('2.7')),
    'es_alevel_022': ('mean', F('1.25')),
    'es_alevel_023': ('mean', F('0.4')),
    'es_alevel_024': ('mean', F('3.05')),
    'es_alevel_025': ('mean', F('5.3')),
    'es_alevel_026': ('mean', F('2.15')),
    'es_alevel_027': ('mean', 17),
    'es_alevel_028': ('mean', F('0.3')),
    'es_alevel_029': ('mean', F('1.75')),
    'es_alevel_030': ('mean', F('5.5')),
    # The other 12, read from their own context.
    'es_core_013': ('none',),       # the missing 2nd and 1st prizes are both 0.01
    'es_gcse_001': ('none',),
    'es_gcse_003': ('none',),
    'es_gcse_005': ('func', 'F(comb(3, int(x)), 8)'),       # a fair coin flipped 3 times
    'es_gcse_006': ('none',),
    'es_gcse_014': ('none',),
    'es_alevel_003': ('none',),
    'es_alevel_005': ('none',),
    'es_alevel_006': ('func', 'comb(4, int(x)) * F(1, 10) ** int(x) * F(9, 10) ** (4 - int(x))'),   # Bin(4, 0.1)
    'es_alevel_008': ('none',),
    'es_alevel_009': ('func', 'x / 10'),
    'es_alevel_010': ('none',),
}

TIMES = {2: 'twice', 3: 'three times', 4: 'four times'}


def xs(x):
    """x as the page writes it: a minus sign, not a hyphen."""
    return ('−%s' % -x) if x < 0 else str(x)


def clue_holds(clue, table):
    """True if the completed table {x: p} satisfies the item's stated relation."""
    kind = clue[0]
    if kind == 'none':
        return True
    if kind == 'ratio':
        return table[F(clue[1])] == clue[3] * table[F(clue[2])]
    if kind == 'diff':
        return table[F(clue[1])] == table[F(clue[2])] + clue[3]
    if kind == 'mean':
        return sum(x * p for x, p in table.items()) == clue[1]
    if kind == 'func':
        return all(p == F(eval(clue[1], {'F': F, 'comb': math.comb}, {'x': x})) for x, p in table.items())
    raise ValueError(kind)


def clue_stated(clue, context):
    """(True/False, the words looked for): does the context state the relation to the student? A 'func' entry is
    held by CONTEXT (es_gcse_005, es_alevel_009) or by the item's own k(...) wording, so it is not read here."""
    kind = clue[0]
    if kind == 'ratio':
        w = 'P(X = %s) is %s P(X = %s)' % (xs(clue[1]), TIMES[clue[3]], xs(clue[2]))
        return w in context, w
    if kind == 'diff':
        pre, post = 'P(X = %s) is ' % xs(clue[1]), ' more than P(X = %s)' % xs(clue[2])
        m = re.search(re.escape(pre) + r'(\d+(?:\.\d+)?)' + re.escape(post), context)
        return bool(m) and F(m.group(1)) == clue[3], '%s%s%s' % (pre, float(clue[3]), post)
    if kind == 'mean':
        m = re.search(r'E\(X\) = (\d+(?:\.\d+)?)', context)
        return bool(m) and F(m.group(1)) == clue[1], 'E(X) = %s' % float(clue[1])
    return None, None


def stage1_completions(q, d):
    """Every distinct way the tiles fill the missing cells that sums to 1 and satisfies the item's CLUES entry."""
    from itertools import permutations
    missing = [i for i, r in enumerate(q['table']) if not r['given']]
    tiles = [F(t) for t in q['stage1Tiles']]
    found = set()
    for pick in permutations(range(len(tiles)), len(missing)):
        vals = tuple(tiles[t] for t in pick)
        if vals in found:
            continue
        table = {x: p for x, p in d}
        for i, v in zip(missing, vals):
            table[d[i][0]] = v
        if sum(table.values()) == 1 and clue_holds(CLUES[q['id']], table):
            found.add(vals)
    return missing, found


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
    'es_alevel_006': ('Each item is defective independently with probability 0.1',   # approved by Project Claude, 8 Oct
                      lambda s: all(p == math.comb(4, int(x)) * F(1, 10) ** int(x) * F(9, 10) ** (4 - int(x)) for x, p in s.d)),
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
        # Stage 1 has exactly one completion (expectation-station-pc-001): of every placement of the tiles into the
        # missing cells, exactly one sums to 1 and satisfies what the item states, and it is the keyed one.
        clue = CLUES.get(qid)
        if clue is None:
            fails.append('%s: no CLUES entry (say what fixes its Stage 1; never skip)' % w)
        else:
            stated, words = clue_stated(clue, q['context'])
            if stated is False:
                fails.append('%s Stage 1: the context does not state "%s": %r' % (w, words, q['context']))
            idx, found = stage1_completions(q, d)
            keyed = tuple(d[i][1] for i in idx)
            if found != {keyed}:
                shown = sorted('(%s)' % ', '.join(str(v) for v in f) for f in found)
                fails.append('%s Stage 1: %d completion(s) fit the sum to 1 and what the item states, %s; exactly one, '
                             'the keyed (%s), may' % (w, len(found), ', '.join(shown) or 'none',
                                                      ', '.join(str(v) for v in keyed)))
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
    # pc-001: es_core_001 as it was, with no stated relation, so its two missing tiles can swap
    ('es_core_001', 'pc-001: es_core_001 with no relation (two completions)',
     ' P(X = 2) is 0.05 more than P(X = 4).\'', '\'', {'es_core_001': ('none',)}),
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
        for qid, what, old, new, *clues in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-52s *** CANNOT PLANT ***' % what)
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(old, new))
            saved = dict(CLUES)
            CLUES.update(clues[0] if clues else {})   # a plant may also change what the verifier is told is stated
            try:
                if planted is not None:
                    check_bank(rep, planted)
            finally:
                CLUES.clear()
                CLUES.update(saved)
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
