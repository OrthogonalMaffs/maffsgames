#!/usr/bin/env python3
# ci-line: B4 | Trig Worms (every generator outcome recomputed exactly, its diagram measured from the canvas, every option marked in Chromium) |
"""Trig Worms: every outcome of the generator recomputed exactly, its diagram measured, every option marked.

The game generates its questions: find an angle (SOH, CAH or TOA), the opposite or adjacent side, or the
hypotenuse, from a right-angled triangle drawn on the canvas. The tranche 1 audit of 6 Oct 2026 found that 49% of
angle questions offered, as a wrong option, the angle worked out correctly from two other sides printed on the
diagram (whole-degree keys from givens rounded to 1 d.p., no precision stated: SR-1), keys that the stated
method rounds differently, explanations claiming "= 15°" when the stated working gives 15.3°, and "Find the
adjacent side" drawing O=? with A printed as the answer.

Every outcome the page can serve is enumerated here (the page's own POOL: angle 15-85 in fives except 45,
hypotenuse 8-22, each ratio) and each is built by the page's own questionFrom() in Chromium, then:
  Givens: the opposite and adjacent shown are the triangle's sides rounded half up to 1 d.p. (mpmath, 50 digits).
  Key: computed exactly from the values shown, rounded half up as the question states ("to the nearest degree",
    "to 1 decimal place"; SR-1). The question must state that precision.
  Distractors: each is recomputed from its stated named error; it must differ from the key and the others as
    shown, and the only valid route (the givens and the ratio) gives the key, so no distractor is a correct
    answer (SR-4, SR-16). The pool must be exactly the outcomes that have three distinct named errors.
  Explanation: its unrounded figure and its key are recomputed.
  Diagram: only the two given sides are labelled, with the values shown in the question, and the asked side
    carries "?" (a third labelled side gave a second valid answer). The canvas calls are recorded: the drawn
    triangle's angle at θ equals the angle of the given sides (one scale for both legs), and the labels drawn
    are exactly those.
  Marking (Chromium, 390x844): through the game's own loadQ() and guess(), the key is marked a hit and every
    distractor a miss whose feedback names its error.
A self-test plants three of the audit's faults back into a copy of the page (the adjacent question labelled
O=?, an angle key that ignores the shown sides, an angle question with no stated precision); each must FAIL.

    python scripts/verify-trig-worms.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'trig-worms'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
mp.mp.dps = 50
ANGLES = [15, 20, 25, 30, 35, 40, 50, 55, 60, 65, 70, 75, 80, 85]


def half_up(v, places):
    q = Decimal(1).scaleb(-places)
    return Decimal(mp.nstr(v, 40)).quantize(q, rounding=ROUND_HALF_UP)


def deg(v):
    return '%s°' % half_up(v, 0)


def dp1(v):
    return str(half_up(v, 1))


def rad(d):
    return mp.mpf(d) * mp.pi / 180


def todeg(r):
    return r * 180 / mp.pi


def expect(type_, angle, hyp, ratio):
    """What the question must be: shown sides, key, named errors (name -> shown value), labels, precision."""
    # a given is written as JavaScript writes the number: 9, not 9.0
    opp = half_up(hyp * mp.sin(rad(angle)), 1)
    adj = half_up(hyp * mp.cos(rad(angle)), 1)
    opp, adj = [d.to_integral() if d == d.to_integral() else d for d in (opp, adj)]
    O, A, H = mp.mpf(str(opp)), mp.mpf(str(adj)), mp.mpf(hyp)
    S, C, T = mp.sin(rad(angle)), mp.cos(rad(angle)), mp.tan(rad(angle))
    if type_ == 'angle':
        if ratio == 'SOH':
            g1, g2, fn, theta, labels = O, H, 'sin', todeg(mp.asin(O / H)), {'O': 'O=%s' % opp, 'H': 'H=%d' % hyp}
        elif ratio == 'CAH':
            g1, g2, fn, theta, labels = A, H, 'cos', todeg(mp.acos(A / H)), {'A': 'A=%s' % adj, 'H': 'H=%d' % hyp}
        else:
            g1, g2, fn, theta, labels = O, A, 'tan', todeg(mp.atan(O / A)), {'O': 'O=%s' % opp, 'A': 'A=%s' % adj}
        r, small = g1 / g2, min(g1, g2) / max(g1, g2)
        if ratio == 'TOA':
            named = [('ratio upside down: tan⁻¹(A/O)', todeg(mp.atan(g2 / g1))),
                     ('sin⁻¹ instead of tan⁻¹', todeg(mp.asin(small))), ('cos⁻¹ instead of tan⁻¹', todeg(mp.acos(small))),
                     ('ratio rounded to 1 d.p. before tan⁻¹', todeg(mp.atan(mp.mpf(str(half_up(r, 1))))))]
        else:
            other = 'cos' if fn == 'sin' else 'sin'
            named = [(other + '⁻¹ instead of ' + fn + '⁻¹', todeg(mp.acos(r) if fn == 'sin' else mp.asin(r))),
                     ('tan⁻¹ instead of ' + fn + '⁻¹', todeg(mp.atan(r))),
                     ('tan⁻¹ of the ratio upside down', todeg(mp.atan(1 / r))),
                     ('ratio rounded to 1 d.p. before ' + fn + '⁻¹',
                      todeg((mp.asin if fn == 'sin' else mp.acos)(mp.mpf(str(half_up(r, 1))))))]
        named.append(('the other acute angle: 90° − θ', 90 - theta))
        named = [(w, deg(v)) for w, v in named if deg(v) not in ('0°', '90°')]
        named.append(('calculator in radians', '%s°' % half_up(theta * mp.pi / 180, 2)))
        key, prec, unrounded = deg(theta), 'to the nearest degree', half_up(theta, 1)
    elif type_ == 'side':
        if ratio == 'SOH':
            v, named, labels = H * S, [('cos instead of sin', H * C), ('tan instead of sin', H * T),
                                       ('divided by sin instead of multiplying', H / S)], {'H': 'H=%d' % hyp, 'O': 'O=?'}
        else:
            v, named, labels = H * C, [('sin instead of cos', H * S), ('tan instead of cos', H * T),
                                       ('divided by cos instead of multiplying', H / C)], {'H': 'H=%d' % hyp, 'A': 'A=?'}
        key, prec, unrounded = dp1(v), 'to 1 decimal place', None
        named = [(w, dp1(x)) for w, x in named]
    else:
        v = O / S
        named = [('multiplied by sin instead of dividing', dp1(O * S)), ('cos instead of sin', dp1(O / C)),
                 ('tan instead of sin', dp1(O / T))]
        key, prec, unrounded, labels = dp1(v), 'to 1 decimal place', None, {'O': 'O=%s' % opp, 'H': 'H=?'}
    wrong, why, seen = [], [], {key}
    for w, x in named:
        if len(wrong) < 3 and x not in seen:
            seen.add(x)
            wrong.append(x)
            why.append(w)
    return {'opp': str(opp), 'adj': str(adj), 'key': key, 'wrong': wrong, 'why': why, 'labels': labels,
            'prec': prec, 'unrounded': unrounded}


def outcomes():
    for t in ('angle', 'side', 'hypotenuse'):
        for a in ANGLES:
            for h in range(8, 23):
                for r in (['SOH', 'CAH', 'TOA'] if t == 'angle' else ['SOH', 'CAH'] if t == 'side' else ['SOH']):
                    yield t, a, h, r


# Build every outcome with the page's questionFrom(), draw it with the game's drawScene() while recording the
# canvas, and mark the key and every distractor through loadQ()/guess().
SWEEP_JS = r"""(cases) => {
  window.setInterval = () => 0; window.setTimeout = () => 0;   // no shot animation, no advance
  const C = CanvasRenderingContext2D.prototype, rec = [];
  for (const k of ['moveTo','lineTo','fillText','strokeText']) { const f = C[k]; C[k] = function(...a){ rec.push([k, ...a]); return f.apply(this, a); }; }
  const out = [];
  for (const [t, a, h, r] of cases) {
    const q = questionFrom(t, a, h, r);
    rec.length = 0; drawScene(q);
    const path = rec.filter(c => c[0] === 'moveTo' || c[0] === 'lineTo');
    const texts = rec.filter(c => c[0] === 'fillText').map(c => c[1]);
    // the triangle: the moveTo followed by two lineTos that the diagram draws (the first such triple whose
    // second point is level with the first and third directly above the second)
    let tri = null;
    for (let i = 0; i + 2 < path.length; i++) {
      const [p0, p1, p2] = [path[i], path[i+1], path[i+2]];
      if (p0[0] === 'moveTo' && p1[0] === 'lineTo' && p2[0] === 'lineTo' && Math.abs(p1[2]-p0[2]) < 1e-9 && Math.abs(p2[1]-p1[1]) < 1e-9 && p2[2] < p1[2]) { tri = [p0, p1, p2]; break; }
    }
    const marks = [];
    for (const pick of [q.correct, ...q.wrong]) {
      questions = [q]; qNum = 0; loadQ();
      const btn = [...document.querySelectorAll('#choices .choice-btn')].find(b => b.textContent === pick);
      if (!btn) { marks.push([pick, null, '']); continue; }
      btn.click();
      marks.push([pick, document.getElementById('feedback').className, document.getElementById('expText').textContent]);
    }
    const shown = (questions = [q], qNum = 0, loadQ(), [...document.querySelectorAll('#choices .choice-btn')].map(b => b.textContent));
    out.push({t, a, h, r, q, tri: tri && tri.map(p => [p[1], p[2]]), texts, marks, shown});
  }
  return out;
}"""


def check(fails, html, label=''):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    n = 0
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
            page.wait_for_function('typeof questionFrom === "function" && typeof POOL === "object"', timeout=8000)
            pool = page.evaluate('() => POOL')
            page.evaluate('() => startGame()')
            cases = list(outcomes())
            res = page.evaluate(SWEEP_JS, cases)
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
    finally:
        proc.terminate()
        proc.wait()
    want_pool = {t: [] for t in ('angle', 'side', 'hypotenuse')}
    for o in res:
        t, a, h, r, q = o['t'], o['a'], o['h'], o['r'], o['q']
        e = expect(t, a, h, r)
        if len(e['wrong']) == 3:
            want_pool[t].append([a, h, r])
        where = '%s %d° H=%d %s' % (t, a, h, r)
        if len(e['wrong']) < 3:
            continue          # not servable: the pool check below holds the page to that
        n += 1
        if (q['opp'], q['adj']) != (float(e['opp']), float(e['adj'])):
            fails.append('%s: shows O=%s A=%s, the sides rounded to 1 d.p. are %s, %s' % (where, q['opp'], q['adj'], e['opp'], e['adj']))
        if q['correct'] != e['key']:
            fails.append('%s (trig-worms-t1-001/003): key %s, recomputed from the shown values %s' % (where, q['correct'], e['key']))
        if e['prec'] not in q['qText']:
            fails.append('%s (trig-worms-t1-001): the question does not state "%s": %r' % (where, e['prec'], q['qText']))
        if q['wrong'] != e['wrong'] or q['why'] != e['why']:
            fails.append('%s: distractors %s (%s), recomputed %s (%s)' % (where, q['wrong'], q['why'], e['wrong'], e['why']))
        if len(set(o['shown'])) != 4 or e['key'] not in o['shown']:
            fails.append('%s: the options shown are %s' % (where, o['shown']))
        if e['unrounded'] is not None and ('= %s°' % e['unrounded']) not in q['exp']:
            fails.append('%s (trig-worms-t1-004): the explanation does not give θ = %s° (%r)' % (where, e['unrounded'], q['exp']))
        if not q['exp'].endswith(e['key']) and not q['exp'].endswith(e['key'] + ' to the nearest degree'):
            fails.append('%s: the explanation does not end at the key %s: %r' % (where, e['key'], q['exp']))
        if q['labels'] != e['labels']:
            fails.append('%s (trig-worms-t1-001/002): the diagram labels %s, expected only the givens and the asked side %s'
                         % (where, q['labels'], e['labels']))
        drawn = sorted(x for x in o['texts'] if re.match(r'^[OAH]=', x))
        if drawn != sorted(e['labels'].values()):
            fails.append('%s: the canvas draws the labels %s, expected %s' % (where, drawn, sorted(e['labels'].values())))
        if o['tri'] is None:
            fails.append('%s: no right-angled triangle found among the canvas calls' % where)
        else:
            (x0, y0), (x1, y1), (x2, y2) = o['tri']
            got = mp.atan((y1 - y2) / (x1 - x0))
            want = mp.atan(mp.mpf(e['opp']) / mp.mpf(e['adj']))
            if abs(todeg(got - want)) > 1e-6:
                fails.append('%s: the drawn angle is %.2f°, the given sides make %.2f°' % (where, todeg(got), todeg(want)))
        for pick, cls, exp_text in o['marks']:
            right = pick == e['key']
            if cls is None:
                fails.append('%s: option %s is not on screen' % (where, pick))
            elif ('correct' in cls) != right:
                fails.append('%s: picking %s was marked %s' % (where, pick, cls))
            elif not right and pick in e['wrong'] and e['why'][e['wrong'].index(pick)] not in exp_text:
                fails.append('%s: the feedback for %s does not name its error' % (where, pick))
    if pool != want_pool:
        for t in want_pool:
            extra = [p for p in pool[t] if p not in want_pool[t]]
            missing = [p for p in want_pool[t] if p not in pool[t]]
            if extra or missing:
                fails.append('POOL %s: serves %d outcomes without three named errors (%s...), leaves out %d that have them'
                             % (t, len(extra), extra[:3], len(missing)))
    return n


PLANTS = [
    ("the adjacent question labelled O=? (t1-002)", "labels={H:'H='+hyp,A:'A=?'}", "labels={H:'H='+hyp,O:'O=?'}"),
    ("an angle key that ignores the shown sides (t1-001, t1-003)", "    correct=deg(theta);\n", "    correct=angle+'°';\n"),
    ("an angle question with no stated precision (t1-001)", "\\nFind angle θ to the nearest degree.`", "\\nFind angle θ.`"),
]


def check_legacy(fails, html):
    """A page without questionFrom() (main before this fix): sample its generator and name the audit faults."""
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context()
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)   # MaffsLock's 300 ms window: the sweep answers at once
            ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
            ctx.route(lambda url: url.split('?')[0].endswith('/games/%s/' % SLUG), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            qs = page.evaluate('() => Array.from({length: 1000}, (_, i) => generateQuestion(i % 10))')
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    seen = set()
    for q in qs:
        kind = 'angle' if 'ANGLE' in q['qType'] else 'hypotenuse' if 'HYPOTENUSE' in q['qType'] else 'side'
        ratio = q['ratio'] if kind != 'side' else ('CAH' if 'adjacent' in q['qText'] else 'SOH')
        e = expect(kind, q['angle'], q['hyp'], ratio)
        where = '%s %d° H=%d %s' % (kind, q['angle'], q['hyp'], ratio)
        if kind == 'angle':
            valid = {deg(todeg(f(mp.mpf(str(a)) / mp.mpf(str(b))))) for f, a, b in
                     ((mp.asin, q['opp'], q['hyp']), (mp.acos, q['adj'], q['hyp']), (mp.atan, q['opp'], q['adj']))}
            for w in q['wrong']:
                if w in valid and ('t1-001', where) not in seen:
                    seen.add(('t1-001', where))
                    fails.append('%s (trig-worms-t1-001): wrong option %s is the angle from two sides on the diagram' % (where, w))
            if q['correct'] != e['key']:
                fails.append('%s (trig-worms-t1-003): key %s, the stated method gives %s' % (where, q['correct'], e['key']))
            if 'nearest degree' not in q['qText']:
                fails.append('%s (trig-worms-t1-001): no precision stated' % where)
            m = re.search(r'= (\d+)°$', q['exp'])
            if m and e['unrounded'] is not None and str(e['unrounded']) != m.group(1):
                fails.append('%s (trig-worms-t1-004): the explanation says θ = %s°, the working gives %s°' % (where, m.group(1), e['unrounded']))
        if kind == 'side' and ratio == 'CAH' and q['findSide'] != 'adjacent':
            fails.append('%s (trig-worms-t1-002): "Find the adjacent side" draws %s=?' % (where, q['findSide']))
    return len(qs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    if 'function questionFrom(' in html:
        n = check(fails, html)
    else:
        n = check_legacy(fails, html)
    print('%s: %d servable outcomes recomputed (mpmath), drawn and marked in Chromium at 390px' % (SLUG, n))
    ok = True
    if not args.no_selftest and not args.against:
        for what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-58s *** CANNOT PLANT ***' % what)
                ok = False
                continue
            rep = []
            check(rep, html.replace(old, new))
            ok = ok and bool(rep)
            print('  self-test %-58s %s' % (what, ('caught: ' + rep[0][:100]) if rep else '*** MISSED ***'))
    for f in fails[:60]:
        print('FAIL  ' + f)
    if len(fails) > 60:
        print('FAIL  ... and %d more' % (len(fails) - 60))
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
