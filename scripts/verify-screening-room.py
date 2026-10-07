#!/usr/bin/env python3
# ci-line: E | Screening Room (every count, band and key from the stated rates; every figure from the data; all 70 items marked in Chromium) |  && --selftest
"""Independent verification of Screening Room: every count, answer, band and figure from the stated rates.

Until Oct 2026 every item's counts, answer and gut-check band were typed in beside its rates (tranche 4 audit,
docs/audits/findings/screening-room.yml): 20 of 70 bands excluded the item's own answer, alevel_16's false
positives were 130 where its rates give 147, rounded counts were never stated (the exact Bayes answer was
marked wrong), an absolute 0.005 tolerance marked 0 correct on small probabilities, and six real-world rates were
wrong (quoted-statistics audit, PR #68). The page now stores only each item's population, base rate and test
rates, and computes everything else; this script recomputes it all with exact fractions:

  - COUNTS: N x base, then each test's true and false positives, are whole numbers (an item marked rounded must
    say "rounded to the nearest whole number"), and equal the page's.
  - ANSWER AND BAND: P = true positives / positives (a rounded item: the exact Bayes value from the rates). The
    band is the button whose label contains P (Over 75 / 25-75 / 5-25 / Under 5; a boundary value goes to the
    label that contains it; exactly 25% is ambiguous and fails). The page's band must match; no item literal
    may carry a hand-keyed band, answer or count.
  - PRECISION AND KEYS: a percentage to 1 d.p. (2 d.p. under 1%, 3 d.p. under 0.1%), rounded half up; the page's
    keys must match (a rounded item also accepts the count ratio).
  - SOURCES: every real-world rate credited to a real test, programme or population is a SOURCES entry with its
    source text and URL, and an item reads it.
  - EVERY DISPLAYED FIGURE: the scenario and explanation templates type no digit beyond the item's textNumbers
    (ages, a year group); every number in the rendered scenario, explanation, answer line and Bayes working is
    one the data gives (a count, a stated rate, the answer, a "1 in N").
  - IN CHROMIUM (reduced motion), every item is played: the band's button is marked correct and the next one
    wrong; the icon array (N <= 10,000) draws exactly its true positives, false positives and missed cases; the
    prompt states the precision; the key as a percentage and as a decimal are marked correct, one unit off and 0
    are wrong; an over-precise answer, a fraction, "abc" and a percentage without % are never marked (no score,
    no event, the input stays open, the message is shown); the explanation shows the data's text, and the Bayes
    box shows at A-Level.

    python scripts/verify-screening-room.py [--file PATH] [--selftest]

--selftest plants faults in copies of the page (a hand-keyed band, alevel_16's old 130 false positives in the
engine and typed into its explanation, marking that accepts 0) and requires each to be caught.
"""
import argparse
import os
import re
import sys
import tempfile
from collections import defaultdict
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'screening-room'
PAGE = os.path.join(bc.GAMES_DIR, SLUG, 'index.html')
LEVELS = ['gcse', 'alevel', 'core', 'level4']
BANDS = [('very_likely', 'Over 75%'), ('likely', '25 – 75%'), ('unlikely', '5 – 25%'), ('very_unlikely', 'Under 5%')]
NUM = re.compile(r'(?<![\w.])\d[\d,]*(?:\.\d+)?')

READ = """() => {
  const out = {};
  for (const lv in QUESTIONS) out[lv] = QUESTIONS[lv].map(q => ({
    id: q.id, N: q.N, base: String(q.base), tests: q.tests.map(t => t.map(String)), rounded: !!q.rounded,
    alt: q.alt ? String(q.alt.base) : null, textNumbers: q.textNumbers || [],
    scenario: q.scenario, explanation: q.explanation, scenarioText: q.scenarioText, explanationText: q.explanationText,
    answerTex: q.answerTex, bayesTex: q.bayesTex, population: q.population, count: q.condition.count,
    tp: q.testPositive.truePositive, fp: q.testPositive.falsePositive, pos: q.testPositive.total,
    gut: q.gutCheckCorrect, dp: q.dp, keys: q.keys }));
  return out;
}"""

# Play one item: phase 1 (two buttons), phase 2 (icon counts), phase 3 (each probe on a fresh phase 3).
PLAY = """([lv, id, gutRight, gutWrong, probes]) => {
  const q = QUESTIONS[lv].find(x => x.id === id);
  const events = [];
  const realMfg = window.mfg;
  window.mfg = function (name, p) { events.push(name + ':' + (p && p.phase)); };
  const realST = window.setTimeout;
  window.setTimeout = function (fn) { fn(); return 0; };       // phase 1 -> 2 at once (no 1.2 s wait)
  const out = { gut: {}, probes: [] };
  try {
    currentLevel = lv;
    startGame();
    sessionQuestions = [q, q, q, q, q, q, q, q];
    qIdx = 0;
    for (const [key, which] of [[gutRight, 'right'], [gutWrong, 'wrong']]) {
      showQuestion();
      out.scenarioShown = document.getElementById('qScenario').textContent;
      const before = totalScore;
      document.querySelector('.gut-btn[data-gut="' + key + '"]').click();
      out.gut[which] = { text: document.getElementById('gutResult').textContent, gained: totalScore - before };
    }
    const grid = document.getElementById('iconGrid');
    out.icons = { tp: grid.querySelectorAll('.true-positive').length, fp: grid.querySelectorAll('.false-positive').length,
                  cond: grid.querySelectorAll('.condition').length, all: grid.children.length };
    out.summary = document.getElementById('iconSummary').textContent;
    for (const raw of probes) {
      showPhase3();
      out.prompt = document.getElementById('calcPrompt').textContent;
      out.hint = document.getElementById('calcHint').textContent;
      const before = totalScore, ev = events.length;
      document.getElementById('calcInput').value = raw;
      document.getElementById('calcSubmit').click();
      const res = document.getElementById('calcResult');
      out.probes.push({ raw: raw, shown: res.style.display !== 'none', title: document.getElementById('calcResultTitle').textContent,
        gained: totalScore - before, events: events.length - ev, open: !document.getElementById('calcInput').disabled,
        msg: document.getElementById('calcMsg').style.display !== 'none' ? document.getElementById('calcMsg').textContent : '',
        expl: document.getElementById('calcExplanation').textContent,
        bayes: document.getElementById('bayesBox').style.display !== 'none' });
    }
  } finally {
    window.setTimeout = realST;
    window.mfg = realMfg;
  }
  return out;
}"""


def fr(x):
    return F(str(x))


def pct_text(rate):
    s = f'{float(rate * 100):.6f}'.rstrip('0').rstrip('.')
    return s


def band_of(p):
    pc = p * 100
    if pc > 75:
        return 'very_likely'
    if pc >= 25:
        return 'likely'
    if pc >= 5:
        return 'unlikely'
    return 'very_unlikely'


def half_up_pct(p, dp):
    """p (a Fraction) as a percentage, rounded half up to dp places, as an integer count of 10^-dp percent."""
    x = p * 100 * 10 ** dp
    q, r = divmod(x.numerator, x.denominator)
    return q + (1 if 2 * r >= x.denominator else 0)


def expected(q):
    N, base = q['N'], fr(q['base'])
    tests = [(fr(a), fr(b)) for a, b in q['tests']]
    c = N * base
    tp, fp, steps = c, N - c, []
    for se, sp in tests:
        tp, fp = tp * se, fp * (1 - sp)
        steps.append((tp, fp))
    exact = tp / (tp + fp)
    e = {'c': c, 'tp': tp, 'fp': fp, 'steps': steps, 'exact': exact, 'tests': tests, 'base': base}
    counts = [c] + [x for s in steps for x in s]
    e['whole'] = all(x.denominator == 1 for x in counts)
    rnd = lambda x: int(x + F(1, 2)) if x >= 0 else -int(-x + F(1, 2))  # noqa: E731
    e['tpi'], e['fpi'], e['ci'] = rnd(tp), rnd(fp), rnd(c)
    e['pos'] = e['tpi'] + e['fpi']
    ratio = F(e['tpi'], e['pos'])
    p = exact if q['rounded'] else ratio
    e['p'] = p
    pc = p * 100
    e['dp'] = 1 if pc >= 1 else 2 if pc >= F(1, 10) else 3
    keys = {half_up_pct(p, e['dp'])}
    if q['rounded']:
        keys.add(half_up_pct(ratio, e['dp']))
    e['keys'] = keys
    e['band'] = band_of(p)
    return e


def num_set(*vals):
    out = set()
    for v in vals:
        if v is None:
            continue
        out.add(F(v).limit_denominator(10 ** 9) if not isinstance(v, F) else v)
    return out


def numbers_in(text):
    return [F(m.replace(',', '')) for m in NUM.findall(text.replace('{,}', ','))]


def check_item(lv, q, src_block, rep):
    iid = q['id']
    e = expected(q)
    # counts
    if not e['whole'] and not q['rounded']:
        rep[('counts', iid)].append(f"a count is not whole: c={e['c']}, steps={[(str(a), str(b)) for a, b in e['steps']]}")
    if q['rounded'] and 'rounded to the nearest whole number' not in q['explanationText']:
        rep[('counts', iid)].append('rounded counts not stated as rounded')
    if q['rounded'] and e['whole']:
        rep[('counts', iid)].append('marked rounded but every count is whole')
    for name, mine, page in (('population', q['N'], q['population']), ('condition', e['ci'], q['count']),
                             ('true positives', e['tpi'], q['tp']), ('false positives', e['fpi'], q['fp']),
                             ('positives', e['pos'], q['pos'])):
        if mine != page:
            rep[('counts', iid)].append(f'{name}: page {page}, rates give {mine}')
    # band, precision, keys
    if e['p'] * 100 == 25:
        rep[('band', iid)].append('the answer is exactly 25%, on two buttons\' labels')
    if q['gut'] != e['band']:
        rep[('band', iid)].append(f"page band {q['gut']}, answer {float(e['p'] * 100):.3f}% is in {e['band']}")
    if q['dp'] != e['dp']:
        rep[('precision', iid)].append(f"page asks {q['dp']} d.p., expected {e['dp']}")
    if set(q['keys']) != e['keys']:
        rep[('keys', iid)].append(f"page keys {q['keys']}, expected {sorted(e['keys'])} (x10^-{e['dp']} %)")
    # templates type no digit beyond textNumbers
    allowed_lit = {F(str(x)) for x in q['textNumbers']}
    for field in ('scenario', 'explanation'):
        for n in numbers_in(re.sub(r'\{\w+\}', ' ', q[field])):
            if n not in allowed_lit:
                rep[('typed figure', iid)].append(f'the {field} template types {n} (not from the data)')
        if re.search(r'\{\w+\}', q[field + 'Text']):
            rep[('typed figure', iid)].append(f'an unfilled token in the {field}')
    # every rendered number is one the data gives
    se1, sp1 = e['tests'][0]
    vals = {F(q['N']), F(e['ci']), F(q['N'] - e['ci']), F(e['tpi']), F(e['fpi']), F(e['ci'] - e['tpi']),
            F(q['N'] - e['ci'] - e['fpi']), F(e['pos']), F(q['N'] - e['pos']), F(1)}
    for a, b in e['steps']:
        r = lambda x: int(x + F(1, 2))  # noqa: E731
        vals |= {F(r(a)), F(r(b)), F(r(a) + r(b))}
    rates = [e['base'], se1, sp1, 1 - sp1] + [x for se, sp in e['tests'][1:] for x in (se, sp, 1 - sp)]
    vals |= {x * 100 for x in rates} | {round(1 / x) for x in rates if x}
    vals |= {F(half_up_pct(e['p'], e['dp']), 10 ** e['dp'])}
    vals |= {F(round(F(e['pos'], q['N']) * 100))}
    if q['alt']:
        a = fr(q['alt'])
        alt = se1 * a / (se1 * a + (1 - sp1) * (1 - a))
        vals |= {a * 100, F(half_up_pct(alt, 1), 10)}
    vals |= allowed_lit
    for field in ('scenarioText', 'explanationText'):
        for n in numbers_in(q[field]):
            if n not in vals:
                rep[('displayed figure', iid)].append(f'{field} shows {n}, which the data does not give')
    # answer line and Bayes working: counts, the simplified fraction, the stated rates and the answer
    g = __import__('math').gcd(e['tpi'], e['pos'])
    tex_vals = vals | {F(e['tpi'] // g), F(e['pos'] // g), F(e['tpi'] + e['fpi'])}
    tex_vals |= {x for x in rates} | {1 - e['base']} | {F(half_up_pct(e['p'], e['dp']), 10 ** (e['dp'] + 2))}
    tex_vals |= {F(r(a)) for a, b in e['steps']} | {F(r(b)) for a, b in e['steps']}
    for field in ('answerTex', 'bayesTex'):
        text = re.sub(r'\\[a-zA-Z]+', ' ', q[field] or '')
        for n in numbers_in(text):
            if n not in tex_vals:
                rep[('displayed figure', iid)].append(f'{field} shows {n}, which the data does not give')


def probes_for(e):
    dp = e['dp']
    k = min(e['keys'])
    pct = f'{k / 10 ** dp:.{dp}f}'
    dec = f'{k / 10 ** (dp + 2):.{dp + 2}f}'
    off = f'{(k + 1) / 10 ** dp:.{dp}f}'
    exact = e['p'] * 100
    over = f'{float(exact):.{dp + 2}f}'
    over_ok = half_up_pct(F(over) / 100, dp) in e['keys'] and F(over) != F(k, 10 ** dp)
    frac = f"{e['tpi']}/{e['pos']}"
    probes = [(pct + '%', 'correct'), (dec, 'correct'), (off + '%', 'wrong'), ('0', 'wrong'), ('abc', 'unmarked'),
              (frac, 'unmarked'), (pct, 'unmarked' if F(pct) > 1 else 'decimal-form')]
    if over_ok:
        probes.append((over + '%', 'unmarked'))
    return [p for p in probes if p[1] != 'decimal-form']


def check_play(page, lv, q, e, rep):
    iid = q['id']
    order = [b for b, _ in BANDS]
    wrong = order[(order.index(e['band']) + 1) % 4]
    probes = probes_for(e)
    r = page.evaluate(PLAY, [lv, iid, e['band'], wrong, [p for p, _ in probes]])
    if r['scenarioShown'] != q['scenarioText']:
        rep[('chromium', iid)].append('phase 1 does not show the data\'s scenario')
    if r['gut']['right']['gained'] != 1 or not r['gut']['right']['text'].startswith('Correct'):
        rep[('chromium', iid)].append(f"the {e['band']} button is not marked correct: {r['gut']['right']}")
    if r['gut']['wrong']['gained'] != 0 or r['gut']['wrong']['text'].startswith('Correct'):
        rep[('chromium', iid)].append(f"the {wrong} button is marked correct")
    if q['N'] <= 10000:
        want = {'tp': e['tpi'], 'fp': e['fpi'], 'cond': e['ci'] - e['tpi'], 'all': q['N']}
        if r['icons'] != want:
            rep[('icon array', iid)].append(f"drawn {r['icons']}, data {want}")
    for n, want in zip(numbers_in(r['summary']), (e['tpi'], e['fpi'], e['pos'])):
        if n != want:
            rep[('icon array', iid)].append(f"summary shows {n}, data {want}")
    if f"{e['pos']:,}" not in r['prompt']:
        rep[('chromium', iid)].append('the prompt does not show the number of positives')
    if f"to {e['dp']} decimal place" not in r['hint'] or f"to {e['dp'] + 2} decimal places" not in r['hint']:
        rep[('chromium', iid)].append(f"the precision is not stated: {r['hint']!r}")
    for (raw, want), got in zip(probes, r['probes']):
        if want == 'correct':
            ok = got['shown'] and got['title'].startswith('Correct') and got['gained'] == 3 and got['events'] == 1
        elif want == 'wrong':
            ok = got['shown'] and got['title'].startswith('Not quite') and got['gained'] == 0 and got['events'] == 1
        else:
            ok = (not got['shown']) and got['gained'] == 0 and got['events'] == 0 and got['open'] and got['msg']
        if not ok:
            rep[('marking', iid)].append(f'{raw!r} should be {want}: {got}')
        if want in ('correct', 'wrong') and got['shown']:
            if q['explanationText'] not in got['expl']:
                rep[('chromium', iid)].append('the explanation is not the data\'s text')
            if got['bayes'] != (lv == 'alevel'):
                rep[('chromium', iid)].append(f"Bayes box shown={got['bayes']} at {lv}")
    return r


def run(path, play=True, only=None):
    from playwright.sync_api import sync_playwright
    rep = defaultdict(list)
    counts = defaultdict(int)
    src = open(path, encoding='utf-8').read()
    block = re.search(r'var QUESTIONS = \{.*?\n\};', src, re.S)
    block = block.group(0) if block else ''
    for field in ('gutCheckCorrect', 'answer', 'testPositive', 'testNegative', 'count', 'answerFraction', 'bayesWorking'):
        for m in re.finditer(r'[{,]\s*' + field + r'\s*:', block):
            line = block[:m.start()].count('\n')
            rep[('hand-keyed', f'item line {line}')].append(f'an item literal carries {field}: it must be computed')
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            ctx = browser.new_context(reduced_motion='reduce', viewport={'width': 1280, 'height': 900})
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            if os.path.abspath(path) != os.path.abspath(PAGE):
                page.route(f'**/games/{SLUG}/', lambda route: route.fulfill(
                    status=200, content_type='text/html; charset=utf-8', body=src))
            page.goto(f'{base.rstrip("/")}/games/{SLUG}/')
            data = page.evaluate(READ)
            sources = page.evaluate("() => typeof SOURCES === 'undefined' ? null : SOURCES")
            if not sources:
                rep[('sources', 'SOURCES')].append('no SOURCES list: every real-world rate is stored with its source')
            for name, f in (sources or {}).items():
                if not isinstance(f.get('value'), (int, float)) or not f.get('text') or not re.match(r'https?://', f.get('url', '')):
                    rep[('sources', name)].append('a stored rate needs a value, a source text and a URL')
                if not re.search(r'SOURCES\.' + re.escape(name) + r'\.value', block):
                    rep[('sources', name)].append('no item reads it')
            for lv in LEVELS:
                for q in data.get(lv, []):
                    counts['items'] += 1
                    check_item(lv, q, block, rep)
                    if play and (only is None or q['id'] in only):
                        check_play(page, lv, q, expected(q), rep)
                        counts['played'] += 1
            browser.close()
            for e in errors:
                rep[('page', 'script error')].append(e)
    finally:
        proc.terminate()
        proc.wait()
    return rep, counts


def report(rep, counts):
    print(f'{SLUG}: ' + ', '.join(f'{v} {k}' for k, v in counts.items()))
    for (kind, where), msgs in sorted(rep.items()):
        for m in msgs:
            print(f'  FAIL [{kind}] {where}: {m}')
    print('PASS' if not rep else f'FAILED: {sum(len(v) for v in rep.values())} problem(s)')
    return 1 if rep else 0


def plant(src, old, new):
    assert src.count(old) == 1, f'self-test anchor not found once: {old[:70]}'
    return src.replace(old, new)


def selftest():
    src = open(PAGE, encoding='utf-8').read()
    cases = [
        ('a hand-keyed band in an item literal', 'hand-keyed', None,
         lambda s: plant(s, '{id:"gcse_01",', '{id:"gcse_01",gutCheckCorrect:"unlikely",')),
        ('a hand-keyed band in the engine (gcse_01 keyed unlikely)', 'gcse_01', None,
         lambda s: plant(s, 'q.gutCheckCorrect = gutBand(q.answer);',
                         "q.gutCheckCorrect = q.id === 'gcse_01' ? 'unlikely' : gutBand(q.answer);")),
        ("alevel_16's old 130 false positives in the engine", 'alevel_16', None,
         lambda s: plant(s, '  var exact = tp / (tp + fp);', "  if (q.id === 'alevel_16') fp = 130;\n  var exact = tp / (tp + fp);")),
        ("alevel_16's old 130 typed into its explanation", 'alevel_16', None,
         lambda s: plant(s, 'After Test B, {tp} true and {fp} false positives remain', 'After Test B, {tp} true and 130 false positives remain')),
        ('marking that accepts 0 (the old absolute tolerance)', 'alevel_12', {'alevel_12'},
         lambda s: plant(s, "  if (v === null) return { result: 'unreadable', msg: hint };",
                         "  if (v === null) return { result: 'unreadable', msg: hint };\n  if (v === 0) return { result: 'correct' };")),
    ]
    failed = 0
    for label, where, only, mutate in cases:
        with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8', newline='\n') as t:
            t.write(mutate(src))
            tmp = t.name
        try:
            rep, _ = run(tmp, play=only is not None, only=only)
        finally:
            os.unlink(tmp)
        hit = any(k == where or w == where for (k, w) in rep)
        print(f'  {"caught" if hit else "MISSED"}: {label}')
        failed += not hit
    print(f'self-test: {len(cases) - failed}/{len(cases)} planted faults caught')
    return 1 if failed else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--file', help='check another copy of the page')
    ap.add_argument('--selftest', action='store_true', help='plant faults and require each to be caught')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    return report(*run(a.file or PAGE))


if __name__ == '__main__':
    sys.exit(main())
