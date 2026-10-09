#!/usr/bin/env python3
# ci-line: Core Maths Paper 2A (independent recomputation + rendered page) |
"""Independent verification of core-maths-paper2a's statistics (todo §1.26).

The game is 36 fixed multiple-choice questions. §3.5 (Normal), §3.6 (confidence
intervals) and §3.7 (correlation and regression) carry hand-typed values that had
never been recomputed. This script recomputes every one from the numbers printed in
its own stem, with scripts/stats_common.py; nothing numeric is read from the game
except what the student sees (stem, options, the key's position, the working).

Per item (every one of the 36):
  - the options are distinct, by text and by value;
  - no distractor equals the key in value;
  - no draft prose in the stem, options or working (check-banks' B6 list);
  - every '=' chain in the working is arithmetically true (stats_common.arith_problems).
Per statistics item (§3.5-§3.7, Q10-Q36): SPECS below says what is asked, from the
stem; the stem must still print those numbers, and the key must be the recomputed
answer. 'Approximately' items key the option nearest the true value, and it must be
the only nearest one. Given table values ("Using P(Z <= 1.2) = 0.8849") must be the
table's (Phi to 4 d.p.).

The page is then rendered, item by item, through the game's own showQuestion():
before answering, no option is marked and the working is hidden; after choosing the
key, the key is marked correct and the working shows. Q1's bar chart must draw the
four percentages its stem states.

A fault-injection self-test (a wrong value, a wrong key, a pre-answer leak and a
mis-drawn bar) must FAIL each time; it runs unless --no-selftest.

    python scripts/verify-core-maths-paper2a.py [--verbose] [--no-selftest]
"""
import argparse
import copy
import importlib.util
import math
import os
import re
import sys
from statistics import NormalDist

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402
import stats_common as st  # noqa: E402

SLUG = 'core-maths-paper2a'


def _load_check_banks():
    spec = importlib.util.spec_from_file_location('check_banks', os.path.join(HERE, 'check-banks.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


DRAFT_PATTERNS = list(_load_check_banks().DRAFT_PATTERNS) + [
    (m, re.compile(r'\b' + m + r'\b', re.IGNORECASE)) for m in ('actually', 'recheck', 'hmm')
]


def clean(s):
    return (s.replace('−', '-').replace('–', '-').replace('—', '-')
            .replace(' ', ' ').replace(' ', ' '))


def value(opt):
    """numeric value of an option: 0.8849, '68%' -> 0.68, '(131.08, 138.92)' -> tuple; else None"""
    s = clean(opt).strip()
    m = re.fullmatch(r'(-?\d+(?:\.\d+)?)(%?)', s)
    if m:
        return float(m.group(1)) / (100 if m.group(2) else 1)
    m = re.fullmatch(r'\((-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)\)', s)
    if m:
        return (float(m.group(1)), float(m.group(2)))
    return None


def token(opt):
    """the printed number of a plain numeric option, without %"""
    return clean(opt).strip().rstrip('%')


def N(mu, sd):
    return NormalDist(mu, sd)


# --------------------------------------------------------------------------
#  SPECS: what each statistics item asks, from its own stem.
#  has    substrings the stem must still contain (the numbers the spec uses)
#  kind   exact    the key's printed value is the true value, within its rounding
#         approx   the key is the option nearest the true value, uniquely
#         tuple    the key is the interval, each end within its rounding
#         text     a conceptual key, fixed by the recomputed fact in `why`
#  true   the recomputed value (a float, a tuple, or for 'text' the key's opening)
#  given  table values the stem quotes: [(printed, true)]
#  extra  further facts that must hold: [(description, bool)]
# --------------------------------------------------------------------------
def _specs():
    Z = st.Z
    ci = lambda xbar, sd, n, z: (xbar - z * sd / math.sqrt(n), xbar + z * sd / math.sqrt(n))  # noqa: E731
    half = (60.47 - 55.53) / 2
    z24 = half / (15 / math.sqrt(100))
    table_z = {'90%': 1.645, '95%': 1.96, '99%': 2.576}
    lvl24 = min(table_z, key=lambda k: abs(table_z[k] - z24))
    return {
        9: dict(has=['mean 163', 'standard deviation 7', '156', '170'], kind='approx',
                true=st.region_prob(N(163, 7), ('between', 156, 170))),
        10: dict(has=['X ~ N(50, 16)'], kind='exact', true=math.sqrt(16)),
        11: dict(has=['X ~ N(180, 100)', '195'], kind='exact', true=(195 - 180) / math.sqrt(100)),
        12: dict(has=['X ~ N(120, 25)', 'P(Z ≤ 1.2) = 0.8849', 'P(X ≤ 126)'], kind='exact',
                 true=Z.cdf((126 - 120) / math.sqrt(25)), given=[('0.8849', Z.cdf(1.2))],
                 extra=[('the quoted z, 1.2, is (126 - 120) / 5', (126 - 120) / 5 == 1.2)]),
        # The stem names the 68-95-99.7 rule (Jon, 30 Sep 2026), so the key is the rule's value
        # exactly: 42 is mu - 2 sigma, and half of the 5% outside mu +/- 2 sigma is below it.
        # (The calculator value, 2.28%, is not what the question asks for.)
        13: dict(has=['mean 58', 'standard deviation 8', 'under 42', 'Using the 68–95–99.7 rule'],
                 kind='exact', true=(1 - 0.95) / 2,
                 extra=[('42 is mu - 2 sigma', 58 - 2 * 8 == 42)]),
        14: dict(has=['mean 1000', 'standard deviation 12', 'less than 985', 'P(Z ≤ −1.25) = 0.1056'],
                 kind='exact', true=N(1000, 12).cdf(985), given=[('0.1056', Z.cdf(-1.25))],
                 extra=[('the quoted z, -1.25, is (985 - 1000) / 12', (985 - 1000) / 12 == -1.25)]),
        15: dict(has=['X ~ N(65, 144)', 'between 53 and 77'], kind='approx',
                 true=st.region_prob(N(65, 12), ('between', 53, 77))),
        16: dict(has=['mean of 500 ml', 'standard deviation 4 ml', 'less than 491 ml',
                      'P(Z ≤ −2.25) = 0.0122', 'batch of 5,000'], kind='approx',
                 true=5000 * N(500, 4).cdf(491), given=[('0.0122', Z.cdf(-2.25))],
                 extra=[('the quoted z, -2.25, is (491 - 500) / 4', (491 - 500) / 4 == -2.25),
                        ('the table route, 0.0122 x 5000, rounds to the same count',
                         round(0.0122 * 5000) == round(5000 * N(500, 4).cdf(491)))]),
        17: dict(has=['N(50, 9)', 'N(50, 1)', 'between 47 mm and 53 mm'], kind='text',
                 true='Factory B',
                 why='P(47 < X < 53): A (sd 3) %.4f, B (sd 1) %.4f' % (
                     st.region_prob(N(50, 3), ('between', 47, 53)), st.region_prob(N(50, 1), ('between', 47, 53))),
                 extra=[('B covers more',
                         st.region_prob(N(50, 1), ('between', 47, 53)) > st.region_prob(N(50, 3), ('between', 47, 53)))]),
        18: dict(has=['sample of 25', 'σ² = 100'], kind='exact', true=math.sqrt(100) / math.sqrt(25)),
        19: dict(has=['z = 1.96', 'standard error is 3'], kind='exact', true=1.96 * 3),
        20: dict(has=['sample of 100', 'σ = 20', 'sample mean is 135', 'z = 1.96'], kind='tuple',
                 true=ci(135, 20, 100, 1.96)),
        21: dict(has=['(42.1, 47.9)'], kind='exact', true=(42.1 + 47.9) / 2),
        22: dict(has=['sample of 64', 'mean of 200', 'standard deviation 16', '(196.08, 203.92)'], kind='text',
                 true='No — the population mean is fixed',
                 why='a confidence level is a property of the method, not of one interval',
                 extra=[('the stem\'s interval is 200 +/- 1.96 x 16/8',
                         all(abs(a - b) <= 0.005 for a, b in zip(ci(200, 16, 64, 1.96), (196.08, 203.92))))]),
        23: dict(has=['(55.53, 60.47)', 'n = 100', 'standard deviation is 15', 'z = 1.645 for 90%'], kind='text',
                 true=lvl24, why='half-width / SE = %.4f, nearest table z is %s' % (z24, table_z[lvl24]),
                 extra=[('the interval at that z rounds to (55.53, 60.47)',
                         tuple(round(v, 2) for v in ci(58, 15, 100, table_z[lvl24])) == (55.53, 60.47))]),
        24: dict(has=['(102, 118)', 'sample size 25', '(106, 114)', 'sample size 100'], kind='text',
                 true='Interval Q gives a more precise estimate',
                 why='width 16 vs 8: ratio 2 = sqrt(100/25); same centre 110',
                 extra=[('widths scale as 1/sqrt(n)', (118 - 102) / (114 - 106) == math.sqrt(100 / 25)),
                        ('same centre', (102 + 118) / 2 == (106 + 114) / 2)]),
        25: dict(has=['sample of 49', 'mean lifetime of 987', 'known to be 35', '1,000 hours'], kind='text',
                 true='Challenges — the CI is (977.2, 996.8)', why='987 +/- 1.96 x 35/7 = (977.2, 996.8), all below 1000',
                 extra=[('the CI is (977.2, 996.8)',
                         tuple(round(v, 1) for v in ci(987, 35, 49, 1.96)) == (977.2, 996.8)),
                        ('1000 lies above the interval', ci(987, 35, 49, 1.96)[1] < 1000)]),
        26: dict(has=['from 25 to 100'], kind='text', true='It halves',
                 why='width scales as 1/sqrt(n): sqrt(25/100) = 1/2',
                 extra=[('factor is 1/2', math.sqrt(25 / 100) == 0.5)]),
        27: dict(has=['r = −0.87'], kind='text', true='Strong negative correlation',
                 why='|r| = 0.87 is in 0.70-0.89 (strong), r < 0'),
        28: dict(has=['ŷ = 3.2x + 14.5', 'gradient 3.2'], kind='text',
                 true='The predicted increase in exam score for each additional hour', why='gradient = change in y per unit x'),
        29: dict(has=['x̄ = 12', 'ȳ = 85', 'ŷ = 4.5x + c'], kind='exact', true=85 - 4.5 * 12),
        30: dict(has=['ŷ = 2.8x + 5.3', 'from 10 to 50', 'x = 25'], kind='exact', true=2.8 * 25 + 5.3,
                 extra=[('x = 25 is inside 10-50 (interpolation, as the working says)', 10 <= 25 <= 50)]),
        31: dict(has=['r = 0.93'], kind='text', true='There is a strong correlation but it does not imply causation',
                 why='correlation is not causation'),
        32: dict(has=['8 data points'], kind='text', true='Outliers should be investigated',
                 why='investigate before including or excluding'),
        33: dict(has=['ŷ = 1.4x − 2.8', 'from 5 to 30', 'x = 150'], kind='text',
                 true='This is extrapolation', why='150 is outside 5-30',
                 extra=[('150 is outside 5-30', not 5 <= 150 <= 30),
                        ('the "negative answer" distractor is false: 1.4 x 150 - 2.8 > 0', 1.4 * 150 - 2.8 > 0)]),
        34: dict(has=['ŷ = 8.2x + 21.4', 'sleeps 7 hours scores 78'], kind='exact', true=78 - (8.2 * 7 + 21.4)),
        35: dict(has=['r = 0.62, n = 8', 'r = 0.62, n = 80'], kind='text',
                 true='Dataset Q',
                 why='5%% two-tail critical value: n = 8 %s, n = 80 %s' % (st.r_cv_txt(8, 0.05), st.r_cv_txt(80, 0.05)),
                 extra=[('n = 8: 0.62 is below the critical value', 0.62 < st.r_critical(8, 0.05)),
                        ('n = 80: 0.62 is above the critical value', 0.62 > st.r_critical(80, 0.05))]),
    }


SPECS = _specs()
STATS_FROM = 9      # Q10, the first §3.5 item


class Report:
    def __init__(self):
        self.fails = []

    def fail(self, qi, what, detail):
        self.fails.append('Q%d %s: %s' % (qi + 1, what, detail))


def check_item(rep, qi, q, verbose=False):
    opts, key = q['options'], q['correct']
    if not isinstance(key, int) or not 0 <= key < len(opts):
        rep.fail(qi, 'key', 'correct = %r is not an option index' % key)
        return
    # generic: distinct options, no value-equal distractor
    norm = [clean(o).strip().lower() for o in opts]
    if len(set(norm)) != len(norm):
        rep.fail(qi, 'options', 'two options are the same text')
    vals = [value(o) for o in opts]
    for i, v in enumerate(vals):
        for j in range(i + 1, len(vals)):
            if v is not None and vals[j] is not None and v == vals[j]:
                rep.fail(qi, 'options', '%r and %r are equal in value' % (opts[i], opts[j]))
    # draft prose
    for field in ('stem', 'working'):
        for name, pat in DRAFT_PATTERNS:
            if pat.search(q.get(field, '')):
                rep.fail(qi, 'draft prose', '%s contains %r' % (field, name))
    for o in opts:
        for name, pat in DRAFT_PATTERNS:
            if pat.search(o):
                rep.fail(qi, 'draft prose', 'option %r contains %r' % (o, name))
    # worked-step arithmetic
    for left, right, why in st.arith_problems(q.get('working', '')):
        rep.fail(qi, 'working', '"%s = %s" is false (%s)' % (left, right, why))
    if qi < STATS_FROM:
        return
    spec = SPECS.get(qi)
    if spec is None:
        rep.fail(qi, 'spec', 'no SPECS entry for a statistics item')
        return
    for h in spec['has']:
        if h not in q['stem']:
            rep.fail(qi, 'stem', 'no longer says %r: the spec must be re-derived from the new stem' % h)
    for printed, true in spec.get('given', []):
        if not st.within_rounding(printed, true):
            rep.fail(qi, 'given table value', 'stem quotes %s, table value is %s' % (printed, st.fmt(true, 4)))
    for desc, ok in spec.get('extra', []):
        if not ok:
            rep.fail(qi, 'fact', desc + ' does not hold')
    kind, true = spec['kind'], spec['true']
    k_opt = opts[key]
    if kind == 'exact':
        kv = value(k_opt)
        if kv is None or isinstance(kv, tuple):
            rep.fail(qi, 'key', 'key %r is not a number' % k_opt)
        elif not st.within_rounding(token(k_opt), true * (100 if k_opt.strip().endswith('%') else 1)):
            rep.fail(qi, 'key', 'stated %r, computed %s' % (k_opt, repr(round(true, 6))))
        others = [o for i, o in enumerate(opts) if i != key and value(o) is not None and not isinstance(value(o), tuple)
                  and st.within_rounding(token(o), true * (100 if o.strip().endswith('%') else 1))]
        for o in others:
            rep.fail(qi, 'distractor', '%r also equals the computed %s' % (o, round(true, 6)))
    elif kind == 'approx':
        dist = [(abs(value(o) - true), i) for i, o in enumerate(opts) if isinstance(value(o), float)]
        dist.sort()
        if not dist or dist[0][1] != key:
            rep.fail(qi, 'key', 'stated %r, nearest to the computed %s is %r' % (
                k_opt, round(true, 6), opts[dist[0][1]] if dist else None))
        elif len(dist) > 1 and math.isclose(dist[0][0], dist[1][0]):
            rep.fail(qi, 'key', 'two options are equally near the computed %s' % round(true, 6))
    elif kind == 'tuple':
        kv = value(k_opt)
        if not isinstance(kv, tuple) or any(not st.within_rounding(t, v) for t, v in
                                            zip(re.findall(r'-?\d+(?:\.\d+)?', clean(k_opt)), true)):
            rep.fail(qi, 'key', 'stated %r, computed (%s, %s)' % (k_opt, round(true[0], 4), round(true[1], 4)))
    elif kind == 'text':
        if not clean(k_opt).startswith(clean(true)):
            rep.fail(qi, 'key', 'stated %r, recomputed key begins %r (%s)' % (k_opt, true, spec.get('why', '')))
        hits = [o for i, o in enumerate(opts) if i != key and clean(o).startswith(clean(true))]
        for o in hits:
            rep.fail(qi, 'distractor', '%r also begins with the key %r' % (o, true))
    if verbose:
        print('  Q%-2d %-6s key %-44r computed %s' % (qi + 1, kind, k_opt[:44],
                                                        spec.get('why') or (round(true, 6) if isinstance(true, float) else true)))


def check_bank(rep, bank, verbose=False):
    if len(bank) != 36:
        rep.fail(-1, 'bank', '%d questions, the game says 36' % len(bank))
    for qi, q in enumerate(bank):
        check_item(rep, qi, q, verbose)


# --------------------------------------------------------------------------
#  what the student sees: every question, rendered by the game's own code
# --------------------------------------------------------------------------
RENDER_JS = """(i) => {
  showScreen('gameScreen');
  document.getElementById('sectionBanner').style.display = 'none';
  document.getElementById('questionArea').style.display = 'block';
  currentQ = i; answered = false;
  showQuestion();
  const btns = [...document.querySelectorAll('#optionsContainer .option-btn')];
  const note = document.getElementById('workingNote');
  const pre = {
    marked: btns.filter(b => /\\b(correct|reveal|incorrect)\\b/.test(b.className)).length,
    working: note.classList.contains('visible') && getComputedStyle(note).display !== 'none'
             && note.textContent.trim().length > 0,
    texts: btns.map(b => b.querySelector('.option-text').textContent),
    svg: document.querySelector('#qStem svg') ? document.querySelector('#qStem svg').outerHTML : null,
  };
  selectAnswer(QUESTIONS[i].correct);
  const post = {
    keyMarked: btns[QUESTIONS[i].correct].classList.contains('correct'),
    working: note.classList.contains('visible') && note.textContent.trim().length > 0,
  };
  return {pre: pre, post: post};
}"""


def bars_from_svg(svg):
    """{label: value} read off the drawing: bar tops mapped through the y-axis tick labels."""
    ticks = [(float(v), float(y) - 4) for y, v in
             re.findall(r'<text x="[\d.]+" y="([\d.]+)"[^>]*text-anchor="end">(\d+(?:\.\d+)?)%</text>', svg)]
    if len(ticks) < 2:
        return None
    (v0, y0), (v1, y1) = ticks[0], ticks[-1]
    to_val = lambda y: v0 + (y - y0) * (v1 - v0) / (y1 - y0)  # noqa: E731
    rects = [(float(x), float(y), float(w)) for x, y, w in
             re.findall(r'<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)"', svg)]
    labels = re.findall(r'font-size="11" text-anchor="middle">([A-Z])</text>', svg)
    if len(rects) != len(labels):
        return None
    return {lab: round(to_val(y), 6) for lab, (x, y, w) in zip(labels, rects)}


def check_rendered(rep, bank, rendered):
    for qi, q in enumerate(bank):
        r = rendered[qi]
        pre, post = r['pre'], r['post']
        if pre['marked']:
            rep.fail(qi, 'picture (before answering)', '%d option(s) already marked' % pre['marked'])
        if pre['working']:
            rep.fail(qi, 'picture (before answering)', 'the working is visible before an answer is chosen')
        if [clean(t) for t in pre['texts']] != [clean(o) for o in q['options']]:
            rep.fail(qi, 'options drawn', 'drawn %r, bank %r' % (pre['texts'], q['options']))
        if not post['keyMarked']:
            rep.fail(qi, 'after answering', 'choosing the key did not mark it correct')
        if not post['working']:
            rep.fail(qi, 'after answering', 'the working did not show')
        if q.get('svg') == 'barchart_q1':
            stated = {m.group(1): float(m.group(2)) for m in re.finditer(r'School ([A-D]): (\d+(?:\.\d+)?)%', q['stem'])}
            drawn = bars_from_svg(pre['svg'] or '')
            if not drawn or set(drawn) != set(stated) or any(abs(drawn[k] - stated[k]) > 0.05 for k in stated):
                rep.fail(qi, 'bar chart', 'stem states %s, drawing shows %s' % (stated, drawn))
            axis = re.search(r'y-axis starts at (\d+)%', q['stem'])
            if axis and pre['svg'] and ('>%s%%</text>' % axis.group(1)) not in pre['svg']:
                rep.fail(qi, 'bar chart', 'stem says the axis starts at %s%%, the drawing does not' % axis.group(1))


def load_and_render(patch_js=None):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/' + SLUG + '/?cb=verify', wait_until='load', timeout=20000)
            page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof showQuestion === "function"', timeout=8000)
            if patch_js:
                page.evaluate(patch_js)
            bank = page.evaluate('JSON.parse(JSON.stringify(QUESTIONS))')
            rendered = [page.evaluate(RENDER_JS, i) for i in range(len(bank))]
            browser.close()
            if errors:
                sys.exit('page errors while rendering: %s' % '; '.join(errors))
            return bank, rendered
    finally:
        proc.terminate()
        proc.wait()


# --------------------------------------------------------------------------
#  fault injection: each must FAIL
# --------------------------------------------------------------------------
def selftest(bank, rendered):
    lines, ok = [], True
    base = Report()
    check_bank(base, bank)
    check_rendered(base, bank, rendered)

    def expect(name, rep_fn):
        # caught only by a failure the fault itself caused, not by one already on the clean bank
        nonlocal ok
        rep = Report()
        rep_fn(rep)
        rep.fails = [f for f in rep.fails if f not in base.fails]
        caught = bool(rep.fails)
        ok = ok and caught
        lines.append('  self-test %-34s %s' % (name, ('caught: ' + rep.fails[0][:110]) if caught else '*** MISSED ***'))

    def mutated(fn):
        b = copy.deepcopy(bank)
        fn(b)
        return b

    def wrong_value(b):
        b[11]['options'][b[11]['correct']] = '1.6'           # Q12 z-score 1.5 -> 1.6
    expect('wrong value (Q12 z = 1.6)', lambda rep: check_bank(rep, mutated(wrong_value)))

    def wrong_key(b):
        b[12]['correct'] = 3                                 # Q13 keyed on 0.9772
    expect('wrong key (Q13 -> 0.9772)', lambda rep: check_bank(rep, mutated(wrong_key)))

    def wrong_working(b):
        b[16]['working'] = b[16]['working'].replace('= 61', '= 62')
    expect('wrong working (Q17 0.0122 x 5000 = 62)', lambda rep: check_bank(rep, mutated(wrong_working)))

    # a pre-answer leak and a mis-drawn bar: patched into the live page, the file is never touched
    leak_bank, leak_rendered = load_and_render("""(() => {
      const orig = showQuestion;
      showQuestion = function () { orig(); const n = document.getElementById('workingNote');
        n.textContent = QUESTIONS[currentQ].working; n.classList.add('visible'); };
    })()""")
    expect('pre-answer leak (working shown)', lambda rep: check_rendered(rep, leak_bank, leak_rendered))
    bar_bank, bar_rendered = load_and_render("""(() => {
      const orig = renderBarChart;
      const vals = [72, 68, 76, 71];   // plot height 145px from y = 15, axis 60-78%
      renderBarChart = (function (o) { return function () {
        let i = 0; return o().replace(/<rect x="([\\d.]+)" y="([\\d.]+)" width="([\\d.]+)" height="([\\d.]+)"/g,
          (m, x, y, w, h) => { const v = vals[i++]; const nh = (v - 60) / 18 * 145;
            return '<rect x="' + x + '" y="' + (15 + 145 - nh) + '" width="' + w + '" height="' + nh + '"'; }); }; })(orig);
    })()""")
    expect('mis-drawn bar (C drawn at 76%)', lambda rep: check_rendered(rep, bar_bank, bar_rendered))
    return ok, lines


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--no-selftest', action='store_true')
    args = ap.parse_args()

    bank, rendered = load_and_render()
    rep = Report()
    check_bank(rep, bank, args.verbose)
    check_rendered(rep, bank, rendered)
    for f in rep.fails:
        print('FAIL ' + f)
    ok = not rep.fails
    if not args.no_selftest:
        s_ok, lines = selftest(bank, rendered)
        print('\nFault-injection self-test (patched copies; the file is never touched):')
        for ln in lines:
            print(ln)
        ok = ok and s_ok
    bad = {f.split(' ', 1)[0] for f in rep.fails}
    print('\n%s: %d FAIL(s) across %d of %d questions (%d statistics items recomputed)'
          % ('PASS' if ok else 'FAILED', len(rep.fails), len(bad), len(bank), len(SPECS)))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
