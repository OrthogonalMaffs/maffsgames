#!/usr/bin/env python3
# ci-line: E | Gradient Hunter (every chord gradient exact from its own points; stated tangents are the drawn curve's; one true interpretation; answer once and Next once, played in Chromium) |
"""Gradient Hunter: every gradient a student is shown or told, against the points the game plots; answer once.

The game draws each item's points as a cardinal spline (drawSmoothCurve, tension 0.3) and asks either for the gradient
of the chord between two plotted points (Calculate: the student clicks A then B) or what a stated chord gradient means
(Reading), then four interpretations, one keyed correct. The bank is read from the live page, then for every item:

  Points: A and B (or the chord's ends) are plotted points, so the drawn curve passes through them.
  Keys: a Calculate item's gradient is (yB - yA)/(xB - xA) at the 2 d.p. the game shows; a Reading item's
    gradientShown is its chord's gradient at the places written; any "chord ... gradient X" in the context is X.
  Tangents (gradient-hunter-t2-002): a "tangent at t=K has gradient Y" in the context is the DRAWN curve's slope at
    the plotted point K, to the hundredth (or at Y's own places where the context says "about" Y). A cardinal spline's slope at a knot is (y[i+1] - y[i-1])/(x[i+1] - x[i-1]) (one-sided at an
    end), whatever its tension; "steeper" / "less steep" than the chord must hold for that slope.
  Interpretations: exactly one is keyed correct, and it states the chord's gradient (to the nearest whole, or as
    written); an option that gives an instantaneous or marginal rate at a point is keyed correct exactly when it
    equals the tangent there (SR-16: a true statement is never a wrong option).
  Chromium: every item played through the page (its two points taken, its keyed option marked right). After a wrong
    pick on a Reading and a Calculate item, the revealed correct option clicked and pressed with Enter changes
    nothing (gradient-hunter-t2-001: it re-scored, without limit, onto the leaderboard), and Next double-clicked
    moves on once.
A self-test plants two of the audit's faults back into a copy of the page (t2-001: no lock on the options; t2-002:
gh_alevel_009's "steeper gradient of 150"); each must FAIL naming its entry.

    python scripts/verify-gradient-hunter.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'gradient-hunter'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNTS = {'core': 20, 'gcse': 15, 'alevel': 10}


def num(s):
    return F(s.replace(',', ''))


def places(s):
    return len(s.split('.')[1]) if '.' in s else 0


def close(stated, exact):
    """stated (a string) is exact at the places it is written."""
    p = places(stated)
    return abs(num(stated) - exact) <= F(1, 2 * 10 ** p)


def knot_slope(pts, x):
    """The drawn curve's slope at the plotted point x (cardinal spline: the neighbours' gradient)."""
    xs = [F(str(p[0])) for p in pts]
    i = xs.index(F(str(x)))
    a, b = pts[max(0, i - 1)], pts[min(len(pts) - 1, i + 1)]
    return (F(str(b[1])) - F(str(a[1]))) / (F(str(b[0])) - F(str(a[0])))


def check_bank(fails, bank):
    counts = {lv: len(bank.get(lv, [])) for lv in COUNTS}
    if counts != COUNTS:
        fails.append('bank: %s items by level, expected %s' % (counts, COUNTS))
    for lv in COUNTS:
        for q in bank.get(lv, []):
            qid, pts = q['id'], q['points']
            plotted = {(F(str(x)), F(str(y))) for x, y in pts}
            a, b = (q['pointA'], q['pointB']) if q['type'] == 'calculate' else (q['chordA'], q['chordB'])
            for p in (a, b):
                if (F(str(p['x'])), F(str(p['y']))) not in plotted:
                    fails.append('%s: %s (%s, %s) is not a plotted point, so the drawn curve misses it' % (qid, p['label'], p['x'], p['y']))
            chord = (F(str(b['y'])) - F(str(a['y']))) / (F(str(b['x'])) - F(str(a['x'])))
            shown = q['gradient'] if q['type'] == 'calculate' else q['gradientShown']
            if not close(str(shown), chord) and not (q['type'] == 'calculate' and abs(F(str(shown)) - chord) <= F(1, 200)):
                fails.append('%s: gradient %s, but the chord from (%s, %s) to (%s, %s) is %s' % (qid, shown, a['x'], a['y'], b['x'], b['y'], float(chord)))
            ctx = q['context']
            for m in re.finditer(r'[Cc]hord[^.]*?gradient (?:of )?(-?\d+(?:\.\d+)?)', ctx):
                if not close(m.group(1), chord):
                    fails.append('%s: the context gives the chord gradient %s; it is %s' % (qid, m.group(1), float(chord)))
            for m in re.finditer(r'tangent at [tx]\s*=\s*(-?\d+(?:\.\d+)?)([^.]*?)gradient (?:of )?(-?\d+(?:\.\d+)?)([^.]*)', ctx):
                k, y = m.group(1), m.group(3)
                try:
                    slope = knot_slope(pts, k)
                except ValueError:
                    fails.append('%s: the tangent at %s is not at a plotted point (its slope cannot be read off the drawing)' % (qid, k))
                    continue
                words = m.group(2) + m.group(4)
                # a plain "has gradient Y" claims Y itself (to the hundredth); "about Y" claims it at Y's places
                exact = close(y, slope) if re.search(r'approximately|about|roughly|around', words) else abs(num(y) - slope) < F(1, 200)
                if not exact:
                    fails.append('gradient-hunter-t2-002 %s: the context says the tangent at %s has gradient %s; the drawn '
                                 'curve\'s is %s' % (qid, k, y, float(slope)))
                if 'steeper' in words and not slope > chord:
                    fails.append('gradient-hunter-t2-002 %s: "steeper" than the chord (%s), but the tangent is %s' % (qid, float(chord), float(slope)))
                if 'less steep' in words and not slope < chord:
                    fails.append('gradient-hunter-t2-002 %s: "less steep" than the chord (%s), but the tangent is %s' % (qid, float(chord), float(slope)))
            opts = q['interpretations']
            keyed = [o for o in opts if o['correct']]
            if len(keyed) != 1:
                fails.append('%s: %d interpretations keyed correct (exactly one)' % (qid, len(keyed)))
                continue
            if len({o['text'] for o in opts}) != len(opts):
                fails.append('%s: two interpretations have the same text' % qid)
            vals = [num(v) for v in re.findall(r'(?<![\w.])(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)', keyed[0]['text'])]
            # its size (a fall reads "loses 10"), as written or rounded (within 0.5%), in the axis units or x1000
            size = abs(chord)
            if not any(abs(v - size * u) <= max(F(1, 2), size * u / 200) for v in vals for u in (1, 1000)):
                fails.append('%s: the keyed interpretation does not give the chord gradient %s: %r' % (qid, float(chord), keyed[0]['text']))
            for o in opts:
                m = re.search(r'(instantaneous|marginal)[^.]*?at (?:[tx]\s*=\s*)?(\d+(?:\.\d+)?)[^.]*? is (-?\d+(?:\.\d+)?)', o['text'])
                if not m:
                    continue
                try:
                    slope = knot_slope(pts, m.group(2))
                except ValueError:
                    continue
                # a plain "is V" claims V itself (to the hundredth); "approximately V" claims V at its own places
                hedged = re.search(r'approximately|about|roughly|around', o['text'])
                true = close(m.group(3), slope) if hedged else abs(num(m.group(3)) - slope) < F(1, 200)
                if true != o['correct']:
                    fails.append('%s: "%s" is %s (the tangent at %s is %s) but keyed %s (SR-16)'
                                 % (qid, o['text'], 'true' if true else 'false', m.group(2), float(slope), o['correct']))


INIT = r"""(() => {
  try { localStorage.clear(); } catch (e) {}
})();"""

PICK = """(want) => { const q = G.questions[G.qIdx];
  if (q.type === 'calculate' && (G.phase === 'clickA' || G.phase === 'clickB')) {
    G.phase = 'interpret'; stopPulse(); disableCanvas(); onBothPointsClicked(q); }
  const b = [...document.querySelectorAll('#optionsGrid .opt-btn')].find(b => q.interpretations.find(o => o.text === b.textContent).correct === want);
  b.click(); return b.textContent; }"""

HUD = "() => [document.getElementById('hudScore').textContent, document.getElementById('hudQ').textContent, (window.__qa || []).length]"


def start(page, level, items=None):
    page.evaluate("""([lv, ids]) => {
        window.__qa = []; if (!window.__hooked) { window.__hooked = true; const m = window.mfg;
          window.mfg = function (e, p) { if (e === 'question_answered') window.__qa.push(p); return m && m.apply(this, arguments); }; }
        document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
        document.getElementById('menuScreen').classList.add('active');
        G.level = lv; G.sessionLen = ids ? ids.length : QUESTIONS[lv].length;
        startGame();
        if (ids) { G.questions = ids.map(id => QUESTIONS[lv].find(q => q.id === id)); G.qIdx = 0; loadQuestion(); }
      }""", [level, items])


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
            ctx.add_init_script(INIT)
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
            ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
            pat = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda u: not u.startswith(base), lambda r: r.abort())
            ctx.route(lambda u: bool(pat.search(u)), lambda r: r.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function("typeof QUESTIONS !== 'undefined' && typeof startGame === 'function'", timeout=8000)
            bank = page.evaluate('() => QUESTIONS')
            # Every item: its keyed option marks right
            for lv in COUNTS:
                start(page, lv)
                for _ in range(len(bank[lv])):
                    qid = page.evaluate('() => G.questions[G.qIdx].id')
                    page.evaluate(PICK, True)
                    fb = page.evaluate("() => (document.querySelector('#readFeedback .feedback, #interpFeedback .feedback') || {}).className || ''")
                    if 'correct' not in fb.split():
                        fails.append('%s in Chromium: its keyed interpretation was not marked right (%s)' % (qid, fb))
                    page.evaluate("() => { const b = [...document.querySelectorAll('#interactionArea button')].pop(); b.click(); }")
            # Answer once, Next once (t2-001): a Reading and a Calculate item
            for lv in COUNTS:
                for kind in ('reading', 'calculate'):
                    item = next((q for q in bank[lv] if q['type'] == kind), None)
                    if not item:
                        continue
                    nxt = next(q['id'] for q in bank[lv] if q['id'] != item['id'])
                    start(page, lv, [item['id'], nxt])
                    page.evaluate(PICK, False)
                    before = page.evaluate(HUD)
                    # the revealed correct option, pressed twice (Enter on a button is a click)
                    page.evaluate("() => { const b = document.querySelector('#optionsGrid .correct-choice'); b.click(); b.click(); }")
                    after = page.evaluate(HUD)
                    if after[0] != before[0] or after[2] != before[2]:
                        fails.append('gradient-hunter-t2-001 %s (%s): clicking the revealed correct option after a wrong pick '
                                     'changed the score %s -> %s and question_answered %d -> %d'
                                     % (item['id'], kind, before[0], after[0], before[2], after[2]))
                    nb = page.query_selector('#interactionArea .maffs-next, #interactionArea .next-btn')
                    if nb:
                        page.wait_for_function("() => { const b = document.querySelector('#interactionArea .maffs-next, #interactionArea .next-btn'); return b && !b.disabled; }", timeout=5000)
                        nb.dblclick()
                        page.wait_for_timeout(150)
                        q = page.evaluate('() => G.qIdx')
                        if q != 1:
                            fails.append('%s: a double click on Next moved %d questions (once)' % (item['id'], q))
                    else:
                        fails.append('%s: no Next after a wrong answer' % item['id'])
            errs = [e for e in errors if 'firebase' not in e.lower() and 'katex' not in e.lower()]
            if errs:
                fails.append('page errors: %s' % '; '.join(errs[:3]))
            browser.close()
            return bank
    finally:
        proc.terminate()
        proc.wait()


PLANTS = [
    ('gradient-hunter-t2-001', 't2-001: no lock on the options', '      if (!MaffsLock.lock(grid)) return;\n', ''),
    ('gradient-hunter-t2-002', 't2-002: "a steeper gradient of 150"',
     'The tangent at t=3 has a gradient of 110, a little less steep than the chord.',
     'The tangent at t=3 has a steeper gradient of 150.'),
]


def run(html):
    fails = []
    bank = play(fails, html)
    if bank:
        check_bank(fails, bank)
    return fails, bank


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    html = open(args.against or GAME, encoding='utf-8').read()
    fails, bank = run(html)
    print('%s: %d items: chord gradients from their points, stated tangents from the drawn curve, one true '
          'interpretation; every item played in Chromium; answer once and Next once'
          % (SLUG, sum(len(bank.get(lv, [])) for lv in COUNTS) if bank else 0))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-40s *** CANNOT PLANT ***' % what)
                ok = False
                continue
            hit = [f for f in run(html.replace(old, new))[0] if f.startswith(tag)]
            ok = ok and bool(hit)
            print('  self-test %-40s %s' % (what, ('caught: ' + hit[0][:110]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
