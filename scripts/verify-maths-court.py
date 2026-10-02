#!/usr/bin/env python3
"""Independent verification of maths-court's statistics (todo §1.26).

Each case is a problem and three arguments, one correct. The Core Maths cases on
distributions and expectation (mc_core_001, 002, 006, 009) state values that had
never been recomputed: mc_core_009's binomial tail probability was the one §1.26
named. This script recomputes each from the numbers in its own problem text, with
scripts/stats_common.py; nothing numeric is read from the game but what the player
sees (problem, working lines, conclusions, which argument is marked correct).

Every case (all levels):
  - at least one argument is correct (some cases have several correct routes, and the
    court judges reasoning, so a wrong argument may share the right conclusion);
  - no draft prose in the problem, the correct arguments or the judge's summary
    (check-banks' B6 list);
  - every '=' chain in the correct argument's working and in the judge's summary is
    arithmetically true (stats_common.arith_problems). The wrong arguments are wrong
    on purpose and are not checked.
Every statistics case: SPECS below says what is asked, from the problem text; the
text must still print those numbers, every value the correct argument states must be
the recomputed one, and the correct argument must be the one the recomputation backs.

The page is then rendered case by case through the game's own loadQuestion(): before
a verdict no card is marked and the judge's summary is hidden; after tapping the
correct argument it is marked and the summary shows.

A fault-injection self-test (a wrong value, a wrong key, a pre-answer leak) must FAIL
each time; it runs unless --no-selftest.

    python scripts/verify-maths-court.py [--verbose] [--no-selftest]
"""
import argparse
import copy
import importlib.util
import os
import re
import sys
from fractions import Fraction
from statistics import NormalDist

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402
import stats_common as st  # noqa: E402

SLUG = 'maths-court'


def _load_check_banks():
    spec = importlib.util.spec_from_file_location('check_banks', os.path.join(HERE, 'check-banks.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


DRAFT_PATTERNS = list(_load_check_banks().DRAFT_PATTERNS) + [
    (m, re.compile(r'\b' + m + r'\b', re.IGNORECASE)) for m in ('actually', 'recheck', 'hmm')
]


def correct_arg(case):
    return [a for a in case['arguments'] if a['correct']]


# --------------------------------------------------------------------------
#  SPECS: what each statistics case asks, from its own problem text.
#  has      substrings the problem must still contain (the numbers the spec uses)
#  key      the conclusion the recomputation backs
#  stated   values the correct argument prints: [(pattern capturing the number, true value)]
#  extra    further facts that must hold: [(description, bool)]
#  h1       the alternative hypothesis the correct argument must state (matches the question's direction)
# --------------------------------------------------------------------------
def _specs():
    b60 = st.Binomial(60, Fraction(1, 6))
    b20 = st.Binomial(20, Fraction(1, 2))
    p_le8 = b60.le(8)
    p_ge15 = b20.ge(15)
    return {
        'mc_core_001': dict(
            has=['P(win £5) = 0.3', 'P(win £0) = 0.7', 'costs £2'],
            key='Not worth playing', why='E(X) = 5 x 0.3 + 0 x 0.7 = 1.50 < 2',
            stated=[(r'E\(X\) = [^=]+= £(\d+\.\d+)', 5 * 0.3 + 0 * 0.7),
                    (r'Expected loss = £(\d+\.\d+)', 2 - (5 * 0.3 + 0 * 0.7))],
            extra=[('probabilities sum to 1', 0.3 + 0.7 == 1), ('E(X) < cost', 5 * 0.3 < 2)]),
        'mc_core_002': dict(
            has=['mean 65', 'SD 12', 'between 53 and 77'],
            key='Approximately 68%', why='P(53 < X < 77) = %.4f' % st.region_prob(NormalDist(65, 12), ('between', 53, 77)),
            nearest=st.region_prob(NormalDist(65, 12), ('between', 53, 77))),
        'mc_core_006': dict(
            has=['rolled 60 times', 'expected number of sixes is 10', 'You get 8 sixes'],
            key='Not necessarily unfair', why='B(60, 1/6): P(X <= 8) = %s, not unusual' % st.fmt(p_le8, 4),
            stated=[(r'Expected value = [^=]+= (\d+)', b60.mean())],
            extra=[('the stated expectation is 60 x 1/6', b60.mean() == 10),
                   ('8 sixes is not significant at 5%, either tail', st.to_dec(p_le8) * 2 > st.D('0.05'))]),
        'mc_core_009': dict(
            # "biased towards heads" (Jon, 30 Sep 2026; it was "Is the coin fair?", which reads
            # two-tailed) matches the one-tailed H1: p > 0.5 the correct argument tests.
            has=['flipped 20 times', '15 heads', 'biased towards heads', '5% significance'],
            key='Significant evidence the coin is biased',
            why='B(20, 0.5): P(X >= 15) = %s < 0.05' % st.fmt(p_ge15, 4),
            stated=[(r'P\(X ≥ 15\) = (\d+\.\d+)', p_ge15)],
            extra=[('P(X >= 15) < 0.05', st.to_dec(p_ge15) < st.D('0.05')),
                   ('the verdict is the same two-tailed (2 x %s < 0.05)' % st.fmt(p_ge15, 4),
                    2 * st.to_dec(p_ge15) < st.D('0.05'))],
            h1=r'H₁: p > 0\.5'),
    }


SPECS = _specs()


class Report:
    def __init__(self):
        self.fails, self.warns = [], []

    def fail(self, cid, what, detail):
        self.fails.append('%s %s: %s' % (cid, what, detail))


def pct(text):
    m = re.search(r'(\d+(?:\.\d+)?)%', text)
    return float(m.group(1)) / 100 if m else None


def check_case(rep, case, verbose=False):
    # Several arguments may be correct (mc_gcse_004 has three routes to one answer), two
    # wrong arguments may share a conclusion, and a wrong argument may even reach the right
    # answer by bad reasoning (mc_ks3_002): the court judges the reasoning. So the only
    # structural rule is that some argument is correct. Wrong arguments are wrong on
    # purpose ("... no wait."), so only the problem, the correct arguments and the
    # judge's summary are read for draft prose and arithmetic.
    cid = case['id']
    args = case['arguments']
    goods = correct_arg(case)
    if not goods:
        rep.fail(cid, 'key', 'no argument is marked correct')
        return
    texts = [('problem', case['problem']), ('judgesSummary', case['judgesSummary'])]
    for a in goods:
        texts += [(a['name'] + ' working', w) for w in a['working']] + [(a['name'] + ' conclusion', a['conclusion'])]
    for where, t in texts:
        for name, pat in DRAFT_PATTERNS:
            if pat.search(t):
                rep.fail(cid, 'draft prose', '%s contains %r' % (where, name))
    for where, t in ([(a['name'] + "'s working", '\n'.join(a['working'])) for a in goods]
                     + [("judge's summary", case['judgesSummary'])]):
        for left, right_, why in st.arith_problems(t):
            rep.fail(cid, where, '"%s = %s" is false (%s)' % (left, right_, why))
    spec = SPECS.get(cid)
    if spec is None:
        return
    for h in spec['has']:
        if h not in case['problem']:
            rep.fail(cid, 'problem', 'no longer says %r: the spec must be re-derived from the new text' % h)
    if len(goods) != 1 or goods[0]['conclusion'] != spec['key']:
        rep.fail(cid, 'key', 'marked %r, recomputed %r (%s)' % ([a['conclusion'] for a in goods], spec['key'], spec['why']))
    good = goods[0]
    shown = '\n'.join(good['working'])
    for pattern, true in spec.get('stated', []):
        m = re.search(pattern, shown)
        if not m:
            rep.fail(cid, 'working', 'the correct argument no longer states a value matching %s' % pattern)
        elif not st.within_rounding(m.group(1), float(true)):
            rep.fail(cid, 'value', 'stated %s, computed %s' % (m.group(1), st.fmt(true, 6)))
    if 'nearest' in spec:
        opts = [(abs(pct(a['conclusion']) - spec['nearest']), a['conclusion']) for a in args
                if pct(a['conclusion']) is not None]
        opts.sort()
        if not opts or opts[0][1] != spec['key'] or (len(opts) > 1 and opts[0][0] == opts[1][0]):
            rep.fail(cid, 'key', 'nearest conclusion to %.4f is %r' % (spec['nearest'], opts[0][1] if opts else None))
    for desc, ok in spec.get('extra', []):
        if not ok:
            rep.fail(cid, 'fact', desc + ' does not hold')
    if spec.get('h1') and not re.search(spec['h1'], shown):
        rep.fail(cid, 'hypotheses', 'the question is one-tailed; the correct argument must test %s' % spec['h1'])
    if verbose:
        print('  %-12s key %-42r %s' % (cid, good['conclusion'], spec['why']))


def check_bank(rep, bank, verbose=False):
    cases = [c for lvl in bank.values() for c in lvl]
    seen = {c['id'] for c in cases}
    for cid in SPECS:
        if cid not in seen:
            rep.fail(cid, 'spec', 'no case with this id any more')
    for c in cases:
        check_case(rep, c, verbose)
    return cases


# --------------------------------------------------------------------------
#  what the player sees: each case, rendered by the game's own loadQuestion()
# --------------------------------------------------------------------------
RENDER_JS = """async (id) => {
  const all = Object.values(QUESTIONS).flat();
  const q = all.find(c => c.id === id);
  showScreen('gameScreen');
  sessionQuestions = [q]; qIndex = 0; sessionLength = 1; score = 0;
  loadQuestion();
  const cards = [...document.querySelectorAll('#argumentsRow .argument-card')];
  const js = document.getElementById('judgesSummary');
  const pre = {
    cards: cards.length,
    marked: cards.filter(c => /correct-reveal|incorrect-reveal/.test(c.className)).length,
    summary: js.classList.contains('show'),
  };
  const good = cards.find(c => q.arguments[parseInt(c.dataset.idx)].correct);
  handleTap(good, parseInt(good.dataset.idx));
  await new Promise(r => setTimeout(r, 600));
  return {pre: pre, post: {keyMarked: good.classList.contains('correct-reveal'), summary: js.classList.contains('show')}};
}"""


def check_rendered(rep, cases, rendered):
    for c in cases:
        r = rendered[c['id']]
        pre, post = r['pre'], r['post']
        if pre['cards'] != 3:
            rep.fail(c['id'], 'picture', '%d argument cards drawn' % pre['cards'])
        if pre['marked']:
            rep.fail(c['id'], 'picture (before the verdict)', '%d card(s) already marked' % pre['marked'])
        if pre['summary']:
            rep.fail(c['id'], 'picture (before the verdict)', "the judge's summary is showing")
        if not post['keyMarked']:
            rep.fail(c['id'], 'after the verdict', 'tapping the correct argument did not mark it')
        if not post['summary']:
            rep.fail(c['id'], 'after the verdict', "the judge's summary did not show")


def load_and_render(patch_js=None, only=None):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/' + SLUG + '/?cb=verify', wait_until='load', timeout=20000)
            page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof loadQuestion === "function"', timeout=8000)
            if patch_js:
                page.evaluate(patch_js)
            bank = page.evaluate('JSON.parse(JSON.stringify(QUESTIONS))')
            ids = [c['id'] for lvl in bank.values() for c in lvl if not only or c['id'] in only]
            rendered = {i: page.evaluate(RENDER_JS, i) for i in ids}
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
    cases = check_bank(base, bank)
    check_rendered(base, cases, rendered)

    def expect(name, rep_fn):
        nonlocal ok
        rep = Report()
        rep_fn(rep)
        rep.fails = [f for f in rep.fails if f not in base.fails]
        caught = bool(rep.fails)
        ok = ok and caught
        lines.append('  self-test %-34s %s' % (name, ('caught: ' + rep.fails[0][:110]) if caught else '*** MISSED ***'))

    def find(b, cid):
        return next(c for lvl in b.values() for c in lvl if c['id'] == cid)

    def mutated(fn):
        b = copy.deepcopy(bank)
        fn(b)
        return b

    def wrong_value(b):
        a = correct_arg(find(b, 'mc_core_009'))[0]
        a['working'] = [w.replace('0.0207', '0.0270') for w in a['working']]
    expect('wrong value (mc_core_009 0.0270)', lambda rep: check_bank(rep, mutated(wrong_value)))

    def wrong_key(b):
        for a in find(b, 'mc_core_002')['arguments']:
            a['correct'] = a['conclusion'] == 'Approximately 95%'
    expect('wrong key (mc_core_002 -> 95%)', lambda rep: check_bank(rep, mutated(wrong_key)))

    def wrong_working(b):
        a = correct_arg(find(b, 'mc_core_001'))[0]
        a['working'] = [w.replace('= £1.50', '= £1.80') for w in a['working']]
    expect('wrong working (mc_core_001 = 1.80)', lambda rep: check_bank(rep, mutated(wrong_working)))

    leak_bank, leak_rendered = load_and_render("""(() => {
      const orig = loadQuestion;
      loadQuestion = function () { orig();
        const q = sessionQuestions[qIndex];
        document.querySelectorAll('#argumentsRow .argument-card').forEach(c => {
          if (q.arguments[parseInt(c.dataset.idx)].correct) c.classList.add('correct-reveal'); }); };
    })()""", only=set(SPECS))
    leak_cases = [c for lvl in leak_bank.values() for c in lvl if c['id'] in leak_rendered]
    expect('pre-answer leak (correct card marked)', lambda rep: check_rendered(rep, leak_cases, leak_rendered))
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
    cases = check_bank(rep, bank, args.verbose)
    check_rendered(rep, cases, rendered)
    for f in rep.fails:
        print('FAIL ' + f)
    for w in rep.warns:
        print('WARN ' + w)
    ok = not rep.fails
    if not args.no_selftest:
        s_ok, lines = selftest(bank, rendered)
        print('\nFault-injection self-test (patched copies; the file is never touched):')
        for ln in lines:
            print(ln)
        ok = ok and s_ok
    bad = {f.split(' ', 1)[0] for f in rep.fails}
    print('\n%s: %d FAIL(s), %d WARN(s) across %d of %d cases (%d statistics cases recomputed)'
          % ('PASS' if ok else 'FAILED', len(rep.fails), len(rep.warns), len(bad), len(cases), len(SPECS)))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
