#!/usr/bin/env python3
# ci-line: E2 | Screening Room (every count, band and key from the stated rates; every figure from the data; all 70 items marked in Chromium) |  && --selftest
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

  - SR-21 (Jon's contract and rulings, 8 Oct 2026):
    t4-005: with MaffsLock's real window, Next then a click on the new question's gut check, and a double click on
      Next, after a right and a wrong answer: one advance, the new gut check unanswered; the session ends once.
    t4-006: ?level=constructor, __proto__, toString, xyz, l4: the start screen at the default level, nothing thrown,
      served or logged.
    t4-008 (Project Claude's rule): over 10,000, k = gcd(N, condition, true and false positives) if N / k fits 10,000
      icons, else the least whole k that fits; each group drawn as exactly count / k (whole icons and one part-icon);
      the note says "1 icon = k <unit>" and gives every exact count.
    t4-013: at 390x844 (touch), every item's phases 1-3 and its answer scroll no wider than 390 px; Next wholly on screen.
    t4-015: phase 3 keeps the scenario and the icon array above the question, Continue gone.
    t4-016 (fixed on main by #92, pinned): the prompt counts no "people"; the hint's examples are no item's answer.

    python scripts/verify-screening-room.py [--file PATH] [--selftest]

--selftest plants 13 faults in copies of the page (a hand-keyed band, alevel_16's old 130 false positives in the
engine and typed into its explanation, marking that accepts 0, and one or two for each SR-21 entry) and requires each
to be caught.
"""
import argparse
import math
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
    gut: q.gutCheckCorrect, dp: q.dp, keys: q.keys, unit: q.unit || null, answerText: q.answerText }));
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
    showPhase2();   // the game moves on through MaffsLock.timer, which a synchronous setTimeout cannot run
    const grid = document.getElementById('iconGrid');
    const note = document.getElementById('iconScale');
    out.note = note && note.style.display !== 'none' ? note.textContent : '';
    // each group's drawn share: a whole icon is 1, a part-icon its data-part (rem/k)
    out.shares = {};
    [...grid.children].forEach(el => { const c = ['true-positive', 'condition', 'false-positive'].find(x => el.classList.contains(x)) || 'neither';
      const p = el.dataset.part; out.shares[c] = out.shares[c] || []; out.shares[c].push(p || '1'); });
    out.icons = { tp: grid.querySelectorAll('.true-positive').length, fp: grid.querySelectorAll('.false-positive').length,
                  cond: grid.querySelectorAll('.condition').length, all: grid.children.length };
    out.summary = document.getElementById('iconSummary').textContent;
    for (const raw of probes) {
      showPhase3();
      const p2 = document.getElementById('phase2'), p3 = document.getElementById('phase3');
      out.phase3 = { p2shown: p2.style.display !== 'none' && p2.getBoundingClientRect().height > 0,
        scenario: document.getElementById('qScenario2').textContent, icons: document.getElementById('iconGrid').children.length,
        above: p2.getBoundingClientRect().top < p3.getBoundingClientRect().top,
        cont: getComputedStyle(document.getElementById('continueBtn')).display !== 'none' &&
              document.getElementById('continueBtn').classList.contains('visible') };
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
    # t4-008 (Project Claude's rule, 8 Oct 2026): over 10,000, one icon stands for k: the largest k dividing N and every
    # count drawn that keeps the array within 10,000 icons, else the least whole k that fits; each group is drawn as its
    # count / k exactly (whole icons, and one part-icon for a remainder), never rounded; a note gives k in the
    # scenario's unit and each group's exact count
    if q['N'] > 10000:
        groups = {'true-positive': e['tpi'], 'condition': e['ci'] - e['tpi'], 'false-positive': e['fpi'],
                  'neither': q['N'] - e['ci'] - e['fpi']}
        g = q['N']
        for v in (e['ci'], e['tpi'], e['fpi']):
            g = math.gcd(g, v)
        k = g if q['N'] // g <= 10000 else -(-q['N'] // 10000)
        unit = q.get('unit') or 'people'
        if f'1 icon = {k:,} {unit}.' not in r['note'] or not all(f'{v:,}' in r['note'] for v in groups.values()):
            rep[('screening-room-t4-008', iid)].append(f"N = {q['N']:,} is drawn scaled, but the note does not say '1 icon = "
                                                       f"{k:,} {unit}' and give every group's count {sorted(groups.values())}: {r['note']!r}")
        for cls, count in groups.items():
            drawn = sum((F(x) for x in r['shares'].get(cls, [])), F(0))
            if drawn != F(count, k):
                rep[('screening-room-t4-008', iid)].append(f"{cls}: drawn {drawn} icons, {count:,} / {k:,} = {F(count, k)}")
    elif r['note']:
        rep[('screening-room-t4-008', iid)].append(f"N = {q['N']:,} is drawn in full, but a scale note shows: {r['note']!r}")
    # t4-015 (Jon, 8 Oct 2026): phase 3 keeps the scenario and the array, above the question; Continue gone
    p3 = r.get('phase3') or {}
    if not (p3.get('p2shown') and p3.get('scenario') == q['scenarioText'] and p3.get('icons') and p3.get('above')) or p3.get('cont'):
        rep[('screening-room-t4-015', iid)].append(f'phase 3 does not show the scenario and the icon array above the '
                                                   f'question (Continue gone): {p3}')
    # t4-016 (fixed on main by #92; pinned): the prompt names no unit, and says nothing of "people"
    if re.search(r'\bpeople\b|Out of', r['prompt']):
        rep[('screening-room-t4-016', iid)].append(f"the prompt counts people: {r['prompt']!r}")
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


def open_page(browser, base, src, path, query='', viewport=(1280, 900), fresh=False, mobile=False):
    """A page of the game (the file at path), with MaffsLock's real fresh window if fresh, else answering at once."""
    ctx = browser.new_context(reduced_motion='reduce', viewport={'width': viewport[0], 'height': viewport[1]},
                              is_mobile=mobile, has_touch=mobile)
    if not fresh:
        ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    ctx.add_init_script("""(() => { window.__ev = []; let inner; Object.defineProperty(window, 'mfg', { configurable: true,
      get() { return function (e, p) { window.__ev.push([e, p]); return inner && inner.apply(this, arguments); }; },
      set(v) { inner = v; } }); })();""")
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.route(f'**/games/{SLUG}/**', lambda route: route.fulfill(status=200, content_type='text/html; charset=utf-8', body=src))
    page.goto(f'{base.rstrip("/")}/games/{SLUG}/{query}')
    page.wait_for_function("typeof QUESTIONS !== 'undefined' && typeof startGame === 'function'")
    return ctx, page, errors


# Play the current question to its result: a gut band, phase 2 drawn, a typed answer (key, or key + 1 unit).
TO_RESULT = """(right) => {
  const q = currentQ, order = ['very_likely', 'likely', 'unlikely', 'very_unlikely'];
  document.querySelector('.gut-btn[data-gut="' + (right ? q.gutCheckCorrect : order[(order.indexOf(q.gutCheckCorrect) + 1) % 4]) + '"]').click();
  showPhase2(); showPhase3();
}"""

SUBMIT = """(right) => {
  const q = currentQ;
  document.getElementById('calcInput').value = ((q.keys[0] + (right ? 0 : 1)) / Math.pow(10, q.dp)).toFixed(q.dp) + '%';
  document.getElementById('calcSubmit').click();
}"""


def extra_checks(browser, base, src, path, data, rep, only):
    items = [(lv, q) for lv in LEVELS for q in data.get(lv, []) if only is None or q['id'] in only]
    # t4-006: a level key that is not one of the game's own levels is ignored: the start screen, the default level,
    # nothing thrown, served or logged
    for bad in ('constructor', '__proto__', 'toString', 'xyz', 'l4'):
        ctx, page, errors = open_page(browser, base, src, path, '?level=' + bad)
        st = page.evaluate("""() => ({start: document.getElementById('startScreen').classList.contains('active'),
          level: currentLevel, logged: window.__ev.filter(e => e[0] === 'game_started').length})""")
        served = None
        try:
            page.evaluate("() => startGame()")
        except Exception as ex:          # main's page threw here (t4-006)
            errors.append(str(ex).splitlines()[0])
        if not errors:
            served = page.evaluate("""() => ({level: (window.__ev.find(e => e[0] === 'game_started') || [0, {}])[1].level,
              gcse: sessionQuestions.every(q => QUESTIONS.gcse.indexOf(q) >= 0)})""")
        if errors or not st['start'] or st['level'] != 'gcse' or st['logged'] or served != {'level': 'gcse', 'gcse': True}:
            rep[('screening-room-t4-006', '?level=' + bad)].append(
                f"start screen {st['start']}, level {st['level']!r}, logged on load {st['logged']}; Start served {served}; "
                f"errors {errors[:1]} (the default level, nothing thrown or logged)")
        ctx.close()
    # t4-013: at 390x844 no phase scrolls sideways, and Next is wholly on screen
    ctx, page, errors = open_page(browser, base, src, path, '', (390, 844), mobile=True)
    for lv, q in items:
        page.evaluate("([lv, id]) => { currentLevel = lv; startGame(); const q = QUESTIONS[lv].find(x => x.id === id); "
                      "sessionQuestions = [q, q, q, q, q, q, q, q]; qIdx = 0; showQuestion(); }", [lv, q['id']])
        widths = [page.evaluate('document.documentElement.scrollWidth')]
        page.evaluate("() => { const q = currentQ; document.querySelector('.gut-btn[data-gut=\"' + q.gutCheckCorrect + '\"]').click(); showPhase2(); }")
        widths.append(page.evaluate('document.documentElement.scrollWidth'))
        page.evaluate("() => { showPhase3(); }")
        widths.append(page.evaluate('document.documentElement.scrollWidth'))
        page.evaluate("() => { const q = currentQ; document.getElementById('calcInput').value = ((q.keys[0] + 1) / Math.pow(10, q.dp)).toFixed(q.dp) + '%'; document.getElementById('calcSubmit').click(); }")
        widths.append(page.evaluate('document.documentElement.scrollWidth'))
        nx = page.evaluate("""() => { const b = document.querySelector('#nextWrap .maffs-next') || document.getElementById('nextQuestionBtn');
          const r = b.getBoundingClientRect(); return [r.left, r.right, r.width]; }""")
        if max(widths) > 390 or nx[0] < 0 or nx[1] > 390 or not nx[2]:
            rep[('screening-room-t4-013', q['id'])].append(
                f'at 390x844 the page is {widths} px wide in phases 1, 2, 3 and after the answer (390), Next spans '
                f'{nx[0]:.0f}-{nx[1]:.0f} px')
    ctx.close()
    # t4-005: with MaffsLock's real window, a double click on Next moves on once and answers nothing on the new
    # question; a right and a wrong answer alike; the session ends once
    ctx, page, errors = open_page(browser, base, src, path, '', fresh=True)
    settle = "() => !window.MaffsLock || !MaffsLock.isFresh()"
    for right in (True, False):
        page.evaluate("() => { currentLevel = 'gcse'; startGame(); }")
        page.wait_for_function(settle)
        page.evaluate(TO_RESULT, right)
        page.wait_for_function(settle)
        page.evaluate(SUBMIT, right)
        page.wait_for_function("() => { const b = document.querySelector('#nextWrap .maffs-next') || document.getElementById('nextQuestionBtn'); "
                               "return b && b.offsetParent && !b.disabled; }")
        before = page.evaluate("() => ({qIdx: qIdx, gut: phase1Scores.length})")
        # Next, then at once a click on the new question's gut check: it must not be answered unseen
        nsel = '#nextWrap .maffs-next' if not right and page.query_selector('#nextWrap .maffs-next') else '#nextQuestionBtn'
        page.evaluate("(s) => { document.querySelector(s).click(); document.querySelector('.gut-btn').click(); }", nsel)
        once_ = page.evaluate("() => ({qIdx: qIdx, gut: phase1Scores.length, marked: document.querySelectorAll('.gut-btn.correct, .gut-btn.incorrect').length})")
        if once_['qIdx'] != before['qIdx'] + 1 or once_['gut'] != before['gut'] or once_['marked']:
            rep[('screening-room-t4-005', ('right' if right else 'wrong') + ', click')].append(
                f"Next, then a click on the new question's gut check: question {before['qIdx']} -> {once_['qIdx']}, "
                f"gut checks {before['gut']} -> {once_['gut']} (the new gut check answered unseen)")
        # and a real double click on Next, from a fresh start
        page.evaluate("() => { currentLevel = 'gcse'; startGame(); }")
        page.wait_for_function(settle)
        page.evaluate(TO_RESULT, right)
        page.wait_for_function(settle)
        page.evaluate(SUBMIT, right)
        page.wait_for_function("() => { const b = document.querySelector('#nextWrap .maffs-next') || document.getElementById('nextQuestionBtn'); "
                               "return b && b.offsetParent && !b.disabled; }")
        before = page.evaluate("() => ({qIdx: qIdx, gut: phase1Scores.length})")
        sel = '#nextWrap .maffs-next' if not right and page.query_selector('#nextWrap .maffs-next') else '#nextQuestionBtn'
        page.dblclick(sel)
        page.wait_for_timeout(150)
        after = page.evaluate("() => ({qIdx: qIdx, gut: phase1Scores.length, marked: document.querySelectorAll('.gut-btn.correct, .gut-btn.incorrect').length})")
        if after['qIdx'] != before['qIdx'] + 1 or after['gut'] != before['gut'] or after['marked']:
            rep[('screening-room-t4-005', 'right' if right else 'wrong')].append(
                f"a double click on Next after a {'right' if right else 'wrong'} answer: question {before['qIdx']} -> "
                f"{after['qIdx']}, gut checks {before['gut']} -> {after['gut']}, {after['marked']} gut buttons marked "
                f"(one advance; the new gut check unanswered)")
    page.evaluate("() => { window.__ev.length = 0; endGame(); endGame(); }")
    n = page.evaluate("() => window.__ev.filter(e => e[0] === 'game_completed').length")
    if n != 1:
        rep[('screening-room-t4-005', 'end')].append(f'the session ended {n} times (once)')
    ctx.close()
    # t4-016 (fixed on main by #92; pinned): the hint's examples, as the page shows them at each precision, are no
    # item's answer
    answers = {q['answerText'] for lv in LEVELS for q in data.get(lv, [])}
    ctx, page, errors = open_page(browser, base, src, path)
    for dp in (1, 2, 3):
        hit = next(((lv, q) for lv in LEVELS for q in data.get(lv, []) if q['dp'] == dp), None)
        if not hit:
            continue
        hint = page.evaluate("([lv, id]) => { currentLevel = lv; startGame(); const q = QUESTIONS[lv].find(x => x.id === id); "
                             "sessionQuestions = [q, q, q, q, q, q, q, q]; qIdx = 0; showQuestion(); showPhase3(); "
                             "return document.getElementById('calcHint').textContent; }", [hit[0], hit[1]['id']])
        for ex in re.findall(r'e\.g\. ([\d.]+%)', hint):
            if ex in answers:
                rep[('screening-room-t4-016', 'hint')].append(f'the input hint gives {ex}, which is an item\'s answer: {hint!r}')
    ctx.close()


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
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
            ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
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
            if play:
                extra_checks(browser, base, src, path, data, rep, only)
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
        ('t4-006: prototype keys accepted as levels', 'screening-room-t4-006', {'gcse_01'},
         lambda s: plant(s, "if (Object.prototype.hasOwnProperty.call(QUESTIONS, pa.get('level') || '')) {",
                         "if (pa.get('level') && QUESTIONS[pa.get('level')]) {")),
        ('t4-008: a remainder rounded to whole icons', 'screening-room-t4-008', {'alevel_04'},
         lambda s: plant(s, '    if (g[1] % k) plan.push([g[0], g[1] % k]);', '    if (2 * (g[1] % k) >= k) plan.push([g[0], 0]);')),
        ('t4-008: no scale note', 'screening-room-t4-008', {'alevel_01'},
         lambda s: plant(s, "    note.style.display = 'block';", "    note.style.display = 'none';")),
        ('t4-015: phase 3 hides the array', 'screening-room-t4-015', {'gcse_01'},
         lambda s: plant(s, "  document.getElementById('phase2').style.display = 'flex';\n", '')),
        ('t4-013: the phone CSS removed', 'screening-room-t4-013', {'gcse_01', 'alevel_01'},
         lambda s: plant(plant(plant(s, '#phase1,#phase2,#phase3{flex-direction:column;gap:16px;width:100%}\n.icon-grid{max-width:100%}\n', ''),
                               '@media(max-width:500px){\n  .icon-grid.grid-25{width:100%}\n  .icon-array-container,.question-card,.calc-card{padding:16px}\n  .calc-input{min-width:0;width:100%}\n}\n', ''),
                         '<div id="nextWrap" style="align-self:center">', '<div id="nextWrap" style="flex:0 0 auto">')),
        ('t4-005: no fresh window on a new question', 'screening-room-t4-005', {'gcse_01'},
         lambda s: plant(s, "  MaffsLock.fresh(document.getElementById('gutOptions'));\n  MaffsLock.fresh(document.getElementById('gameScreen'));\n}",
                         "  MaffsLock.fresh(document.getElementById('gutOptions'), 0);\n}")),
        ('t4-016 (pinned): the prompt counts people', 'screening-room-t4-016', {'gcse_01'},
         lambda s: plant(s, "'Of the <strong>' + numFmt(q.testPositive.total) + '</strong> positive results",
                         "'Out of <strong>' + numFmt(q.testPositive.total) + '</strong> people who tested positive")),
        ("t4-016 (pinned): the hint's example is an item's answer", 'screening-room-t4-016', {'gcse_01'},
         lambda s: plant(s, "['12.5%', '0.125']", "['25.8%', '0.258']")),
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
