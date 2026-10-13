#!/usr/bin/env python3
# ci-line: Stat Attack (keys recomputed from each question's table) |
"""Independent verification of stat-attack's keys (todo §1.36; audit §1.2 items 6-8, 22).

Every key in every scenario is recomputed from the scenario's own classes and
frequencies, in exact rational arithmetic, and compared with what the game stores:

  - midpoints from the class strings ((lower + upper) / 2), and fx, x², fx², Σfx, Σfx²;
  - the modal class (the one class with the highest frequency);
  - the median class, found from n/2 (Jon, 2 Oct 2026): the first class whose cumulative
    frequency reaches n/2;
  - the mean: the key must be the true mean, correctly rounded at the precision it is
    stored to. It is asked to 3 s.f. and marked there (stat-attack-s1-002): the page works
    the 3 s.f. key from the table's sums and marks it with MaffsAnswer.decimal();
  - the variance, Σfx²/Σf − (Σfx/Σf)²: the on-screen formula substitutes the table's own
    sums, unrounded, so the stored key must be the true variance, correctly rounded at its
    stored precision; it is asked, and marked by the page, to 3 s.f. (Jon, 13 Oct 2026);
  - the standard deviation, asked "to 3 significant figures" from "your unrounded
    variance": the stored key must be √(true variance) to 3 s.f., and √ of the stored
    variance key must round to the same 3 s.f. value.

What the student reads must agree with the keys. Every number in a scenario's closing
line (contextLine) and its interpretation options must be the mean key, the SD key or
mean ± SD at the precision it is printed to (×1000 where the unit is thousands), or a
figure from the question itself (a class boundary or n).

The marking is then played in the page through the game's own render and check
functions: the true modal class, the n/2 median class, and the 3 s.f. mean, variance and
SD must each be marked correct; one unit away in the third significant figure must not be
(the variance asked to 3 s.f. and the SD from the unrounded variance, Jon, 13 Oct 2026), and the true value written to more figures gets the format
message, unmarked (SWEEP-1, stat-attack-s1-002; SR-1, SR-3). The midpoint, fx, x² and fx²
columns are marked exactly: the true column is right, and a non-integer entry rounded to a
whole number is not (s1-005). The median prompt states the n/2 rule (s1-001, SR-17), and a
wrong median class must be answered with the n/2 position, never (n+1)/2.

A fault-injection self-test (a wrong variance, a wrong SD, a wrong median class, a wrong
Σfx², stale prose, and the old mean, SD and fx marking and median prompt played in the page)
must FAIL each time; it runs unless --no-selftest.

    python scripts/verify-stat-attack.py [--verbose] [--no-selftest]
"""
import argparse
import copy
import math
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'stat-attack'
CLASS_RE = re.compile(r'^\s*([\d.]+)\s*≤\s*x\s*<\s*([\d.]+)\s*$')
NUM_RE = re.compile(r'\d[\d,]*(?:\.\d+)?')


class Report:
    def __init__(self):
        self.fails = []

    def fail(self, sid, what, detail):
        self.fails.append('%s %s: %s' % (sid, what, detail))


def F(x):
    return Fraction(str(x))


def decimals(x):
    """Decimal places the literal is stored to (JSON number -> repr)."""
    s = repr(float(x)) if not isinstance(x, int) else str(x)
    if 'e' in s or 'E' in s:
        s = format(Decimal(s), 'f')
    if s.endswith('.0'):
        return 0
    return len(s.split('.')[1]) if '.' in s else 0


def round_dp(fr, dp):
    return (Decimal(fr.numerator) / Decimal(fr.denominator)).quantize(Decimal(1).scaleb(-dp), rounding=ROUND_HALF_UP)


def round_sf(x, n):
    """x (float or Fraction) to n significant figures, half up, as a Decimal."""
    d = Decimal(x.numerator) / Decimal(x.denominator) if isinstance(x, Fraction) else Decimal(repr(x))
    if d == 0:
        return d
    e = d.adjusted()
    return d.quantize(Decimal(1).scaleb(e - n + 1), rounding=ROUND_HALF_UP)


def truth(s):
    """Everything recomputed from the scenario's own classes and frequencies."""
    bounds = []
    for c in s['classes']:
        m = CLASS_RE.match(c)
        if not m:
            return None, 'class %r is not "a ≤ x < b"' % c
        bounds.append((F(m.group(1)), F(m.group(2))))
    f = [int(x) for x in s['freqs']]
    n = sum(f)
    mid = [(a + b) / 2 for a, b in bounds]
    fx = [fi * x for fi, x in zip(f, mid)]
    x2 = [x * x for x in mid]
    fx2 = [fi * x * x for fi, x in zip(f, mid)]
    sfx, sfx2 = sum(fx), sum(fx2)
    mean = sfx / n
    var = sfx2 / n - mean * mean
    top = max(f)
    modal = [k for k, fi in enumerate(f) if fi == top]
    half, cum, median = Fraction(n, 2), 0, None
    for k, fi in enumerate(f):
        cum += fi
        if cum >= half:
            median = k
            break
    return dict(bounds=bounds, n=n, mid=mid, fx=fx, x2=x2, fx2=fx2, sfx=sfx, sfx2=sfx2,
                mean=mean, var=var, sd=math.sqrt(float(var)), modal=modal, median=median), None


def same_at_stored_precision(key, true_fr):
    """The key is true_fr correctly rounded at the decimals the key is stored to."""
    dp = decimals(key)
    return Decimal(repr(float(key))).quantize(Decimal(1).scaleb(-dp)) == round_dp(true_fr, dp)


def explained(num_text, s, t, sd_key):
    """A printed number is the mean key, the SD key, mean ± SD, a class boundary or n."""
    raw = num_text.replace(',', '')
    dp = len(raw.split('.')[1]) if '.' in raw else 0
    val = Decimal(raw)
    mean = F(s['mean'])
    sd = F(sd_key)
    cands = [mean, sd, mean - sd, mean + sd]
    for scale in (1, 1000):
        for c in cands:
            if round_dp(c * scale, dp) == val:
                return True
    data = [b for pair in t['bounds'] for b in pair] + [t['n']]
    return any(F(raw) == F(x) for x in data)


def check_scenario(rep, s, verbose=False):
    sid = s['id']
    t, err = truth(s)
    if err:
        rep.fail(sid, 'classes', err)
        return
    k = len(s['classes'])
    for name in ('freqs', 'midpoints', 'fx', 'x2', 'fx2'):
        if len(s[name]) != k:
            rep.fail(sid, name, '%d entries for %d classes' % (len(s[name]), k))
            return
    for name, true in (('midpoints', t['mid']), ('fx', t['fx']), ('x2', t['x2']), ('fx2', t['fx2'])):
        for i, (got, want) in enumerate(zip(s[name], true)):
            if F(got) != want:
                rep.fail(sid, '%s[%d]' % (name, i), 'stored %s, recomputed %s' % (got, float(want)))
    for name, want in (('sumFx', t['sfx']), ('sumFx2', t['sfx2'])):
        if F(s[name]) != want:
            rep.fail(sid, name, 'stored %s, recomputed %s' % (s[name], float(want)))
    if len(t['modal']) != 1:
        rep.fail(sid, 'modalClass', 'no single modal class (frequencies %s)' % s['freqs'])
    elif s['modalClass'] != s['classes'][t['modal'][0]]:
        rep.fail(sid, 'modalClass', 'keyed %r, recomputed %r' % (s['modalClass'], s['classes'][t['modal'][0]]))
    if s['medianClass'] != s['classes'][t['median']]:
        rep.fail(sid, 'medianClass', 'keyed %r, recomputed from n/2 = %s: %r'
                 % (s['medianClass'], Fraction(t['n'], 2), s['classes'][t['median']]))
    if not same_at_stored_precision(s['mean'], t['mean']):
        rep.fail(sid, 'mean', 'keyed %s, true %s' % (s['mean'], float(t['mean'])))
    if not same_at_stored_precision(s['variance'], t['var']):
        rep.fail(sid, 'variance', 'keyed %s, true %.6f (%s at the key\'s %d d.p.)'
                 % (s['variance'], float(t['var']), round_dp(t['var'], decimals(s['variance'])), decimals(s['variance'])))
    sd3 = round_sf(t['sd'], 3)
    if Decimal(repr(float(s['sd']))) != sd3:
        rep.fail(sid, 'sd', 'keyed %s, true %.6f -> %s to 3 s.f.' % (s['sd'], t['sd'], sd3))
    shown = round_sf(math.sqrt(float(s['variance'])), 3)
    if shown != Decimal(repr(float(s['sd']))):
        rep.fail(sid, 'sd line', 'the SD step prints sqrt(%s) = %s to 3 s.f., but the key is %s'
                 % (s['variance'], shown, s['sd']))
    texts = [('contextLine', s.get('contextLine') or '')]
    texts += [('option %d' % i, o['text']) for i, o in enumerate(s.get('interpretOptions') or [])]
    for where, text in texts:
        for m in NUM_RE.finditer(text):
            if not explained(m.group(0), s, t, s['sd']):
                rep.fail(sid, where, '%s is not the mean %s, the SD %s or mean ± SD at its printed precision: %r'
                         % (m.group(0), s['mean'], s['sd'], text))
    if verbose:
        print('  %-5s n=%-3d mean %-8s var %-10s sd %-6s median %s'
              % (sid, t['n'], s['mean'], s['variance'], s['sd'], s['medianClass']))


def check_bank(rep, bank, verbose=False):
    scenarios = [s for lvl in bank.values() for s in lvl]
    ids = [s['id'] for s in scenarios]
    for d in sorted({i for i in ids if ids.count(i) > 1}):
        rep.fail(d, 'id', 'used by more than one scenario')
    for s in scenarios:
        check_scenario(rep, s, verbose)
    return scenarios


# --------------------------------------------------------------------------
#  the marking, played through the game's own render and check functions
# --------------------------------------------------------------------------
PLAY_JS = """async (a) => {
  const all = Object.values(SCENARIOS).flat();
  const q = all.find(s => s.id === a.id);
  const area = document.getElementById('qArea');
  G.questions = [q]; G.qIdx = 0;
  // A correct answer schedules a re-render a second later; it must not land inside a
  // later step or scenario, so timers are held off while the steps are played.
  const realTimeout = window.setTimeout;
  window.setTimeout = () => 0;
  const wait = () => Promise.resolve();
  const out = {};
  async function run(render, input, value, check, fb) {
    render(q, area); await wait();
    document.getElementById(input).value = value;
    check(); await wait();
    const el = document.getElementById(fb);
    return el ? el.textContent : '';
  }
  out.modal = await run(renderModalQ, 'modalInput', a.modal, checkModal, 'modalFb');
  renderMedianQ(q, area); out.medianPrompt = area.querySelector('.q-prompt').textContent;
  out.median = await run(renderMedianQ, 'medianInput', a.median, checkMedian, 'medianFb');
  out.medianAlt = await run(renderMedianQ, 'medianInput', a.medianAlt, checkMedian, 'medianFb');
  for (const [k, v] of Object.entries(a.means)) out['mean_' + k] = await run(renderMeanQ, 'meanInput', v, checkMean, 'meanFb');
  for (const [k, v] of Object.entries(a.sds)) out['sd_' + k] = await run(renderSD_final, 'sdInput', v, checkSD, 'sdFb');
  for (const [k, v] of Object.entries(a.variances)) out['var_' + k] = await run(renderSD_variance, 'varInput', v, checkVariance, 'sdFb');
  renderSD_variance(q, area); out.varPrompt = area.querySelector('.q-prompt').textContent;
  renderSD_final(q, area); out.sdPrompt = area.querySelector('.q-prompt').textContent;
  for (const [k, vals] of Object.entries(a.cols)) {
    const [render, check, id] = {mp: [renderSD_midpoints, checkMidpoints, 'mp'], fx: [renderSD_fx, checkFx, 'fx'],
      x2: [renderSD_x2, checkX2, 'x2_'], fx2: [renderSD_fx2, checkFx2, 'fx2_']}[k.split(':')[0]];
    render(q, area); await wait();
    vals.forEach((v, i) => { document.getElementById(id + i).value = v; });
    check(); await wait();
    out['col_' + k] = document.getElementById('sdFb').textContent;
  }
  out.medianWrong = await run(renderMedianQ, 'medianInput', a.notMedian, checkMedian, 'medianFb');
  out.variance = await run(renderSD_variance, 'varInput', a.variance, checkVariance, 'sdFb');
  out.sd = await run(renderSD_final, 'sdInput', a.sd, checkSD, 'sdFb');
  window.setTimeout = realTimeout;
  return out;
}"""


def answers_for(s):
    t, err = truth(s)
    if err:
        return None
    other = (t['median'] + 1) % len(s['classes'])
    m3, sd3 = round_sf(t['mean'], 3), round_sf(t['sd'], 3)
    unit = lambda d: Decimal(1).scaleb(d.adjusted() - 2)  # noqa: E731  one unit in the 3rd s.f.
    means = {'right': format(m3, 'f'), 'up': format(m3 + unit(m3), 'f'), 'down': format(m3 - unit(m3), 'f')}
    # the true value to 9 s.f. (more figures than asked, never a double rounding), where it differs from the key
    if round_sf(t['mean'], 9) != m3:
        means['long'] = format(round_sf(t['mean'], 9), 'f')
    v3 = round_sf(t['var'], 3)
    variances = {'right': format(v3, 'f'), 'up': format(v3 + unit(v3), 'f'), 'down': format(v3 - unit(v3), 'f')}
    if round_sf(t['var'], 9) != v3:
        variances['long'] = format(round_sf(t['var'], 9), 'f')
    sds = {'right': format(sd3, 'f'), 'up': format(sd3 + unit(sd3), 'f'), 'down': format(sd3 - unit(sd3), 'f')}
    if round_sf(t['sd'], 9) != sd3:
        sds['long'] = format(round_sf(t['sd'], 9), 'f')
    exact = lambda xs: [format(Decimal(x.numerator) / Decimal(x.denominator), 'f') for x in xs]  # noqa: E731
    cols = {'mp:right': exact(t['mid']), 'fx:right': exact(t['fx']), 'x2:right': exact(t['x2']), 'fx2:right': exact(t['fx2'])}
    for k in ('fx', 'x2'):
        if any(x.denominator != 1 for x in t[k]):
            cols[k + ':rounded'] = [str(int(round_dp(x, 0))) for x in t[k]]
    return dict(id=s['id'], modal=s['classes'][t['modal'][0]], median=s['classes'][t['median']],
                notMedian=s['classes'][other], means=means, sds=sds, variances=variances, cols=cols,
                # the same class with its bounds written plainly ("3 ≤ x < 4" for "3.0 ≤ x < 4.0", s1-006)
                medianAlt='%s ≤ x < %s' % tuple(format(Decimal(b.numerator) / Decimal(b.denominator), 'f')
                                                for b in t['bounds'][t['median']]),
                variance=format(v3, 'f'), sd=format(sd3, 'f'), n=t['n'])


def check_played(rep, scenarios, played):
    for s in scenarios:
        a, r = answers_for(s), played.get(s['id'])
        if a is None or r is None:
            continue
        for step, typed in (('modal', a['modal']), ('median', a['median']),
                            ('variance', a['variance']), ('sd', a['sd'])):
            if 'Correct' not in r[step]:
                rep.fail(s['id'], 'marking (%s)' % step, 'typed the true answer %s; the game said %r'
                         % (typed, r[step].strip()[:100]))
        if 'Correct' not in r['medianAlt']:
            rep.fail(s['id'], 'marking (median, plain bounds)', 'typed %r; the game said %r'
                     % (a['medianAlt'], r['medianAlt'].strip()[:100]))
        for step, want in (('mean_right', 'Correct'), ('sd_right', 'Correct')):
            if want not in r[step]:
                rep.fail(s['id'], 'marking (%s)' % step, 'typed %s; the game said %r'
                         % (a['means' if step.startswith('mean') else 'sds']['right'], r[step].strip()[:100]))
        group = {'mean': 'means', 'sd': 'sds', 'var': 'variances'}
        for step in ('mean_up', 'mean_down', 'sd_up', 'sd_down', 'var_up', 'var_down'):
            if 'Correct' in r[step]:
                rep.fail(s['id'], 'marking (%s)' % step, 'typed %s, one unit off at 3 s.f.; the game marked it correct'
                         % a[group[step.split('_')[0]]][step.split('_')[1]])
        if 'Correct' not in r['var_right']:
            rep.fail(s['id'], 'marking (var_right)', 'typed %s; the game said %r' % (a['variances']['right'], r['var_right'].strip()[:100]))
        # Jon, 13 Oct 2026 (stat-attack-s1-003): the variance is asked to 3 s.f., and the SD from the unrounded variance
        if '3 significant figures' not in r['varPrompt']:
            rep.fail(s['id'], 'variance prompt', 'does not ask for 3 significant figures: %r' % r['varPrompt'].strip()[:100])
        if 'Use your unrounded variance' not in r['sdPrompt']:
            rep.fail(s['id'], 'SD prompt', 'does not say "Use your unrounded variance": %r' % r['sdPrompt'].strip()[:100])
        for step in ('mean_long', 'sd_long', 'var_long'):
            if step in r and 'significant figures' not in r[step]:
                rep.fail(s['id'], 'marking (%s)' % step, 'typed the true value to 9 s.f.; it should get the 3 s.f. format '
                         'message, unmarked (SR-3); the game said %r' % r[step].strip()[:100])
        for k in a['cols']:
            right = k.endswith(':right')
            if right != ('correct' in r['col_' + k]):
                rep.fail(s['id'], 'marking (%s column)' % k, 'typed %s; the game said %r'
                         % (a['cols'][k], r['col_' + k].strip()[:100]))
        pos = Fraction(a['n'], 2)
        want = '%sth value' % (pos.numerator if pos.denominator == 1 else float(pos))
        half = '%s' % (pos.numerator if pos.denominator == 1 else float(pos))
        if ('n ÷ 2 = %s' % half) not in r['medianPrompt'] or 'first class whose cumulative frequency reaches' not in r['medianPrompt']:
            rep.fail(s['id'], 'median prompt', 'does not state the n/2 rule (SR-17): %r' % r['medianPrompt'].strip()[:120])
        if want not in r['medianWrong']:
            rep.fail(s['id'], 'median feedback', 'a wrong class should be told the n/2 position (%r); it said %r'
                     % (want, r['medianWrong'].strip()[:100]))


def load(patch_js=None):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/' + SLUG + '/?cb=verify', wait_until='load', timeout=20000)
            page.wait_for_function('typeof SCENARIOS !== "undefined" && typeof checkSD === "function"', timeout=8000)
            if patch_js:
                page.evaluate(patch_js)
            bank = page.evaluate('JSON.parse(JSON.stringify(SCENARIOS))')
            scenarios = [s for lvl in bank.values() for s in lvl]
            played = {}
            for s in scenarios:
                a = answers_for(s)
                if a:
                    played[s['id']] = page.evaluate(PLAY_JS, a)
            browser.close()
            if errors:
                sys.exit('page errors while playing: %s' % '; '.join(errors))
            return bank, played
    finally:
        proc.terminate()
        proc.wait()


# --------------------------------------------------------------------------
#  fault injection: each must FAIL
# --------------------------------------------------------------------------
def selftest(bank, played):
    lines, ok = [], True
    base = Report()
    check_played(base, check_bank(base, bank), played)

    def expect(name, fn):
        nonlocal ok
        rep = Report()
        fn(rep)
        rep.fails = [f for f in rep.fails if f not in base.fails]
        caught = bool(rep.fails)
        ok = ok and caught
        lines.append('  self-test %-36s %s' % (name, ('caught: ' + rep.fails[0][:110]) if caught else '*** MISSED ***'))

    def mutated(fn):
        b = copy.deepcopy(bank)
        fn({s['id']: s for lvl in b.values() for s in lvl})
        return b

    def bump(field, delta):
        def f(by):
            s = next(iter(by.values()))
            s[field] = round(s[field] + delta, 6)
        return f

    expect('wrong variance (+2.5)', lambda rep: check_bank(rep, mutated(bump('variance', 2.5))))
    expect('wrong SD (+0.3)', lambda rep: check_bank(rep, mutated(bump('sd', 0.3))))
    expect('wrong sumFx2 (+0.75)', lambda rep: check_bank(rep, mutated(bump('sumFx2', 0.75))))

    def wrong_median(by):
        s = next(iter(by.values()))
        t, _ = truth(s)
        s['medianClass'] = s['classes'][(t['median'] + 1) % len(s['classes'])]
    expect('wrong median class', lambda rep: check_bank(rep, mutated(wrong_median)))

    def stale_prose(by):
        s = next(iter(by.values()))
        s['contextLine'] += ' The standard deviation is %s.' % round(s['sd'] + 0.7, 2)
    expect('stale SD in the prose', lambda rep: check_bank(rep, mutated(stale_prose)))

    # Lie about a key the page then marks against, in a scenario that is clean on its own,
    # so the failure cannot be mistaken for one the run already reported.
    clean = [s['id'] for lvl in bank.values() for s in lvl
             if not any(f.startswith(s['id'] + ' ') for f in base.fails)]
    if not clean:
        lines.append('  self-test %-36s %s' % ('variance marked against a wrong key', 'skipped: no clean scenario'))
        return False, lines
    sid = clean[0]
    _, lie = load("""(() => { const all = Object.values(SCENARIOS).flat();
        const q = all.find(s => s.id === %r); q.sumFx2 = q.sumFx2 + 300; })()""" % sid)
    expect('variance marked against a wrong key', lambda rep: check_played(
        rep, [s for lvl in bank.values() for s in lvl if s['id'] == sid], lie))
    old_marking = load("""(() => {
        checkMean = function () { const q = G.questions[G.qIdx]; const v = parseFloat($('meanInput').value);
          $('meanFb').innerHTML = Math.abs(v - q.mean) <= 0.15 ? 'Correct!' : 'Incorrect.'; };
        checkSD = function () { const q = G.questions[G.qIdx]; const v = parseFloat($('sdInput').value);
          $('sdFb').innerHTML = Math.abs(v - q.sd) <= Math.max(0.1, q.sd * 0.01) ? 'Correct!' : 'Incorrect.'; };
        checkVariance = function () { const q = G.questions[G.qIdx]; const v = parseFloat($('varInput').value);
          $('sdFb').innerHTML = Math.abs(v - q.variance) <= Math.max(0.5, q.variance * 0.005) ? 'Correct!' : 'Incorrect.'; };
        checkFx = function () { const q = G.questions[G.qIdx]; let ok = true;
          for (let i = 0; i < q.classes.length; i++) if (Math.abs(parseFloat($('fx' + i).value) - q.fx[i]) > 0.5) ok = false;
          $('sdFb').innerHTML = ok ? 'fx correct!' : 'Check.'; };
        const orig = renderMedianQ;
        renderMedianQ = function (q, area) { orig(q, area); area.querySelector('.q-prompt').textContent =
          'Identify the class interval containing the median. (n = ' + q.freqs.reduce((a, b) => a + b, 0) + ')'; };
      })()""")[1]
    all_s = [s for lvl in bank.values() for s in lvl]
    for name, pick in (('old mean band (G10, 106 rejected)', 'G10 marking (mean_right)'),
                       ('old SD band (G10, 54.5 accepted)', 'G10 marking (sd_up)'),
                       ('old variance band (L4_7, 1.10 accepted)', 'L4_7 marking (var_up)'),
                       ('old fx band (L4_7, 7 for 7.5)', 'L4_7 marking (fx:rounded column)'),
                       ('old median prompt (G4, no n/2 rule)', 'G4 median prompt')):
        rep = Report()
        check_played(rep, all_s, old_marking)
        caught = any(f.startswith(pick) for f in rep.fails)
        ok = ok and caught
        lines.append('  self-test %-36s %s' % (name, 'caught' if caught else '*** MISSED ***'))
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

    bank, played = load()
    rep = Report()
    scenarios = check_bank(rep, bank, args.verbose)
    check_played(rep, scenarios, played)
    for f in rep.fails:
        print('FAIL ' + f)
    ok = not rep.fails
    if not args.no_selftest:
        s_ok, lines = selftest(bank, played)
        print('\nFault-injection self-test (patched copies; the file is never touched):')
        for ln in lines:
            print(ln)
        ok = ok and s_ok
    bad = {f.split(' ', 1)[0] for f in rep.fails}
    print('\n%s: %d FAIL(s) across %d of %d scenarios' % ('PASS' if ok else 'FAILED', len(rep.fails), len(bad), len(scenarios)))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
