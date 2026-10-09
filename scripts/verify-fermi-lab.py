#!/usr/bin/env python3
# ci-line: Fermi Lab (every chain multiplies to its key, Brilliant in Chromium; every stored figure sourced and green at its step) |  && --selftest
"""Independent verification of Fermi Lab's chains and its stored real-world figures.

Until Oct 2026, 19 of Fermi Lab's 65 items had a model chain that did not multiply to the item's own key: a
step changed unit (400 W x 8,760 h is 3,504,000 Wh, keyed 3,500 kWh) or a subtotal was multiplied in, so a
student who entered every reference exactly was rated Poor. Four real-world figures, typed in by hand with no
source, marked a true answer down (coach fuel, UK energy per person, packed lunches, SMS a day), and hints
stated wrong figures (docs/audits/quoted-statistics-2026-10.md).

The page is loaded in Chromium and its QUESTIONS and FIG read back, then:
  - CHAINS: every item's model chain (each step's reference, multiplied or divided as the step says) is
    recomputed with exact fractions and must rate Brilliant against acceptedAnswer (within a factor of 2,
    the game's getFinalRating). Every reference and key is a positive number.
  - FIGURES: every FIG entry has a value, a source text, a source URL and the source's figures. A step that
    names a figure (fig, figScale) has reference = value x figScale, and each source figure x figScale scores
    green at that step (the game's withinFactor with the step's green band); an item whose answer is a figure
    (answerFig, answerFigScale) rates Brilliant for each source figure. Every FIG entry is read by some item.
  - BUILT WORDS: an item that names a figure states it in its hint or note (as the value, the scaled value, a
    percentage or "1 in N"), and the item's line in the page source never types it: the words are built
    from FIG, so changing the figure changes the words.
  - IN CHROMIUM: every item is played on the page: each reference typed into its step and locked (every light
    green), then Calculate Estimate, and the cascade must read Brilliant. Each step that names a figure is then
    played again with each source figure typed in: its light must be green.

    python scripts/verify-fermi-lab.py [--file PATH] [--selftest]

--file checks another copy of the page (served in place of the real one). --selftest plants faults in a copy
(a chain that changes unit, a hint that types its figure, a figure its source no longer supports) and
requires each to be caught.
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

SLUG = 'fermi-lab'
PAGE = os.path.join(bc.GAMES_DIR, SLUG, 'index.html')

READ = """() => {
  const out = {fig: FIG, items: []};
  for (const tier in QUESTIONS) for (const q of QUESTIONS[tier]) out.items.push(Object.assign({tier: tier}, q));
  return out;
}"""

PLAY = """async ([tier, id, values]) => {
  currentTier = tier;
  startGame(0);
  const q = QUESTIONS[tier].find(x => x.id === id);
  sessionQuestions = [q]; sessionLength = 1; qIndex = 0;
  loadQuestion();
  const lights = [];
  for (let i = 0; i < values.length; i++) {
    const input = document.getElementById('input-' + i);
    input.value = values[i];
    document.getElementById('submitBtn-' + i).click();
    lights.push(document.getElementById('light-' + i).className.replace('step-light', '').trim());
  }
  const btn = document.getElementById('chainSubmitBtn');
  if (btn.disabled) return {lights: lights, rating: null};
  btn.click();
  return {lights: lights, rating: document.getElementById('cascadeRating').textContent};
}"""


def frac(x):
    return F(repr(float(x))) if not isinstance(x, int) else F(x)


def within(player, ref, factor):
    r = frac(player) / frac(ref)
    return F(1) / frac(factor) <= r <= frac(factor)


def model_product(q):
    m = frac(q['chain'][0]['reference'])
    for s in q['chain'][1:]:
        m = m / frac(s['reference']) if s.get('operation') == 'divide' else m * frac(s['reference'])
    return m


def factor_of(a, b):
    return max(a / b, b / a)


def js_num(x):
    """How a student would type the value: plain digits, or e-notation for very large and small numbers."""
    x = float(x)
    if x != 0 and (abs(x) >= 1e15 or abs(x) < 1e-4):
        return f'{x:.6e}'.replace('e+', 'e')
    s = f'{x:.10f}'.rstrip('0').rstrip('.')
    return s


def fig_text(v):
    """The page's figText: thousands separated by commas, decimals as JavaScript's String() writes them."""
    v = float(v)
    s = str(int(v)) if v == int(v) else repr(round(v, 12))
    whole, dot, frac_part = s.partition('.')
    return re.sub(r'\B(?=(\d{3})+(?!\d))', ',', whole) + dot + frac_part


def item_line(src, iid):
    m = re.search(r'^\{id:"' + re.escape(iid) + r'",.*$', src, re.M)
    return m.group(0) if m else ''


def check_data(data, src, rep):
    fig = data['fig']
    used = set()
    for name, f in fig.items():
        s = f.get('source') if isinstance(f.get('source'), dict) else {}
        if not isinstance(f.get('value'), (int, float)) or f['value'] <= 0:
            rep[('figure', name)].append('no positive value')
        if not s.get('text') or not re.match(r'https?://', s.get('url', '')):
            rep[('figure', name)].append('no source text or URL')
        if not s.get('figures') or not all(isinstance(v, (int, float)) and v > 0 for v in s['figures']):
            rep[('figure', name)].append("no source figures")
    for q in data['items']:
        iid = q['id']
        if not q['chain'] or not all(isinstance(s.get('reference'), (int, float)) and s['reference'] > 0 for s in q['chain']):
            rep[('chain', iid)].append('a step has no positive reference')
            continue
        if not isinstance(q.get('acceptedAnswer'), (int, float)) or q['acceptedAnswer'] <= 0:
            rep[('chain', iid)].append('no positive acceptedAnswer')
            continue
        m = model_product(q)
        k = frac(q['acceptedAnswer'])
        if factor_of(m, k) > 2:
            rep[('chain', iid)].append(f'model chain gives {float(m):.6g}, key {float(k):.6g}: factor '
                                        f'{float(factor_of(m, k)):.3g}, not Brilliant')
        named = []
        for i, s in enumerate(q['chain']):
            if 'fig' not in s:
                continue
            name, scale = s['fig'], s.get('figScale', 1)
            named.append((name, scale))
            if name not in fig:
                rep[('figure use', iid)].append(f'step {i} names unknown figure {name}')
                continue
            used.add(name)
            want = frac(fig[name]['value']) * frac(scale)
            if abs(frac(s['reference']) - want) > want * F(1, 10**9):
                rep[('figure use', iid)].append(f'step {i} reference {s["reference"]} is not {name} x {scale}')
            for v in fig[name]['source']['figures']:
                if not within(frac(v) * frac(scale), s['reference'], s['tolerance']['green']):
                    rep[('source figure', iid)].append(f'step {i}: the source figure {v} ({name}) is not green '
                                                       f'against {s["reference"]} (band {s["tolerance"]["green"]})')
        if 'answerFig' in q:
            name, scale = q['answerFig'], q.get('answerFigScale', 1)
            named.append((name, scale))
            if name not in fig:
                rep[('figure use', iid)].append(f'answer names unknown figure {name}')
            else:
                used.add(name)
                for v in fig[name]['source']['figures']:
                    if factor_of(frac(v) * frac(scale), k) > 2:
                        rep[('source figure', iid)].append(f'the source figure {v} ({name}) is not Brilliant '
                                                           f'against the key {q["acceptedAnswer"]}')
        # built words: stated in the hint or note, never typed on the item's line
        words = ' '.join([s['hint'] for s in q['chain']] + [q.get('answerNote', ''), q.get('eval_answer', '')])
        line = item_line(src, iid)
        for name, scale in named:
            if name not in fig:
                continue
            v = fig[name]['value']
            forms = {fig_text(v), fig_text(v * scale)}
            if v < 1:
                forms |= {str(round(v * 100)) + '%', '1 in ' + str(round(1 / v))}
            for x in (v, v * scale):
                if x >= 1e9:
                    forms.add(fig_text(x / 1e9) + ' billion')
                elif x >= 1e6:
                    forms.add(fig_text(x / 1e6) + ' million')
            if not any(f in words for f in forms):
                rep[('built words', iid)].append(f'no hint or note states {name} ({sorted(forms)})')
            for f in forms:
                if re.search(r'(?<![\d.,])' + re.escape(f) + r'(?![\d,]|\.\d)', line):
                    rep[('built words', iid)].append(f'the page types "{f}" ({name}) instead of building it from FIG')
    for name in fig:
        if name not in used and not re.search(r'FIG\.' + re.escape(name) + r'\b', src.split('// ─── QUESTION BANK ───', 1)[-1]):
            rep[('figure', name)].append('no item reads it')


def play(page, data, rep, counts):
    fig = data['fig']
    for q in data['items']:
        values = [js_num(s['reference']) for s in q['chain']]
        r = page.evaluate(PLAY, [q['tier'], q['id'], values])
        counts['played'] += 1
        if any(l != 'green' for l in r['lights']):
            rep[('chromium', q['id'])].append(f'references typed in: lights {r["lights"]}')
        if not r['rating'] or not r['rating'].startswith('Brilliant'):
            rep[('chromium', q['id'])].append(f'references typed in: rated {r["rating"]!r}, not Brilliant')
        for i, s in enumerate(q['chain']):
            if 'fig' not in s or s['fig'] not in fig:
                continue
            for v in fig[s['fig']]['source']['figures']:
                vals = list(values)
                vals[i] = js_num(float(frac(v) * frac(s.get('figScale', 1))))
                r2 = page.evaluate(PLAY, [q['tier'], q['id'], vals])
                counts['source figures played'] += 1
                if r2['lights'][i] != 'green':
                    rep[('chromium', q['id'])].append(f'step {i}: the source figure {vals[i]} lights {r2["lights"][i]!r}')


def run(path, browser_play=True):
    from playwright.sync_api import sync_playwright
    rep = defaultdict(list)
    counts = defaultdict(int)
    src = open(path, encoding='utf-8').read()
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.add_init_script(bc.NO_LOCK_FRESH_INIT)   # PLAY presses Lock as soon as loadQuestion() renders
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            if os.path.abspath(path) != os.path.abspath(PAGE):
                page.route(f'**/games/{SLUG}/', lambda route: route.fulfill(
                    status=200, content_type='text/html; charset=utf-8', body=src))
            page.goto(f'{base.rstrip("/")}/games/{SLUG}/')
            data = page.evaluate(READ)
            counts['items'] = len(data['items'])
            counts['figures'] = len(data['fig'])
            check_data(data, src, rep)
            if browser_play:
                play(page, data, rep, counts)
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
    return 1 if rep else 0


def plant(src, old, new):
    assert src.count(old) == 1, f'self-test anchor not found once: {old[:60]}'
    return src.replace(old, new)


def selftest():
    src = open(PAGE, encoding='utf-8').read()
    cases = [
        ('a chain that changes unit (household electricity in watts)', 'household-electricity-kwh',
         lambda s: plant(s, 'unit:"kW",reference:0.4,', 'unit:"watts",reference:400,')),
        ('a hint that types its figure', 'eq_sleep_loss',
         lambda s: plant(s, 'hint:"About " + figText(FIG.gcseCohortEngland.value) + " students in England sit',
                         'hint:"About 600,000 students in England sit')),
        ('a figure its source does not support (coach fuel 8 L/100 km)', 'eq_school_trip',
         lambda s: plant(s, 'coachFuelPer100km: {value:20,', 'coachFuelPer100km: {value:8,')),
        ('a stored figure with no source URL', 'ukPowerPerPerson',
         lambda s: plant(s, 'url:"https://www.gov.uk/government/statistics/energy-consumption-in-the-uk-2025/energy-consumption-in-the-uk-ecuk-2025"}},\npackedLunchShare',
                         'url:""}},\npackedLunchShare')),
    ]
    failed = 0
    for label, where, mutate in cases:
        with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8', newline='\n') as t:
            t.write(mutate(src))
            tmp = t.name
        try:
            rep, _ = run(tmp, browser_play=False)
        finally:
            os.unlink(tmp)
        hit = any(w == where for (_, w) in rep)
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
