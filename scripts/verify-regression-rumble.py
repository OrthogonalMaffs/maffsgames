#!/usr/bin/env python3
# ci-held: regression-rumble is withdrawn; 37 of 40 scenarios fail, held for the data ruling (todo 1.26)
"""Independent verification of regression-rumble's statistics (todo §1.26).

NOT IN CI YET, and the game is WITHDRAWN (30 Sep 2026): it reads the kept game at
games/regression-rumble/_withdrawn.html, not the holding page. The first run (30 Sep 2026) failed far more than 10% of scenarios,
which is the contract's STOP IF: the failures are itemised for Jon, and correcting
them means authoring new data, which is his ruling. Wire this into CI with the fix.

Every scenario (core 12, alevel 14, level4 14) is recomputed with
scripts/stats_common.py from its own parameters:
  - Level 4 states n and the five sums the student works from. Those sums must be
    possible (Sxx, Syy > 0 and |r| <= 1), and the r stated beside them (shown later,
    in "Describe the correlation") must be the r they give, to 2 d.p.
  - Core and A-level state r and the line y = a + bx, and draw a scatter the game
    generates from its seed. The drawn points are regenerated here with a Python port
    of the page's Park-Miller generator (the engine is not asked); their r must be
    within 0.10 of the stated r and in the same strength band, and their own
    least-squares line must be the stated one (b within 10%).
  - The critical value must be the exact 5% two-tailed PMCC value for n (4 d.p.),
    and `sig` must be |r| > cv.
  - The prediction predictY must be a + b * predictX, and sq4Type must say whether
    sq4X lies inside xRange.
The page is rendered at every level, logging what the canvas writes: before the
student is asked to calculate b and a (Level 4, first sub-question), the line's
equation must not be on screen.

    python scripts/verify-regression-rumble.py [--no-selftest]
"""
import argparse
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402
import stats_common as st  # noqa: E402

SLUG = 'regression-rumble'
R_TOL = 0.10          # drawn-points r against stated r
B_TOL = 0.10          # drawn least-squares gradient against stated b, relative


def band(r):
    a = abs(r)
    return 'weak' if a < 0.4 else 'moderate' if a < 0.7 else 'strong' if a < 0.9 else 'very strong'


# ----- the page's scatter generator, ported (seeded Park-Miller; nothing read from the engine)
def park_miller(seed):
    def nxt():
        nonlocal seed
        seed = (seed * 16807) % 2147483647
        return (seed - 1) / 2147483646
    return nxt


def drawn_points(sc):
    rng = park_miller(sc['seed'])
    (x0, x1), (y0, y1) = sc['xRange'], sc['yRange']
    step = (x1 - x0) / sc['n']
    out = []
    for i in range(sc['n']):
        x = x0 + step * i + rng() * step * 0.8
        y_ideal = sc['equation']['a'] + sc['equation']['b'] * x
        spread = (1 - abs(sc['r'])) * (y1 - y0) * 0.15
        y = y_ideal + (rng() - 0.5) * 2 * spread
        out.append((x, max(y0, min(y1, y))))
    return out


class Report:
    def __init__(self):
        self.fails = []

    def fail(self, sid, what, detail):
        self.fails.append('%s %s: %s' % (sid, what, detail))


def check_scenario(rep, level, sc):
    sid = sc['id']
    n = sc['n']
    if level == 'level4':
        try:
            s = st.pmcc_from_sums(n, sc['sumX'], sc['sumY'], sc['sumX2'], sc['sumY2'], sc['sumXY'])
        except st.SumsError as e:
            rep.fail(sid, 'sums', 'impossible: %s (stated r = %s)' % (e, sc['r']))
            return
        r_true, a, b = s['r'], float(s['a']), float(s['b'])
        if st.fmt(r_true, 2) != st.fmt(sc['r'], 2):
            rep.fail(sid, 'r', 'stated %s, the sums give %s' % (sc['r'], st.fmt(r_true, 4)))
    else:
        a, b = sc['equation']['a'], sc['equation']['b']
        pts = drawn_points(sc)
        r_drawn = st.pmcc([p[0] for p in pts], [p[1] for p in pts])
        a_d, b_d = (float(v) for v in st.least_squares([p[0] for p in pts], [p[1] for p in pts]))
        if abs(r_drawn - sc['r']) > R_TOL or band(r_drawn) != band(sc['r']):
            rep.fail(sid, 'scatter', 'stated r = %s (%s), the drawn points have r = %.3f (%s)'
                     % (sc['r'], band(sc['r']), r_drawn, band(r_drawn)))
        if abs(b_d - b) > B_TOL * abs(b):
            rep.fail(sid, 'scatter', 'stated line y = %s + %sx, the drawn points fit y = %.3f + %.4fx' % (a, b, a_d, b_d))
        clipped = sum(1 for _, y in pts if y in sc['yRange'])
        if clipped:
            rep.fail(sid, 'scatter', '%d of %d points clipped to the edge of the y-axis' % (clipped, n))
        r_true = sc['r']
        if (b > 0) != (r_true > 0):
            rep.fail(sid, 'sign', 'r = %s but gradient b = %s' % (r_true, b))
    if 'cv' in sc:
        want = st.r_cv_txt(n, 0.05)
        if st.fmt(sc['cv'], 4) != want:
            rep.fail(sid, 'critical value', 'stated %s, exact 5%% two-tail for n = %d is %s' % (sc['cv'], n, want))
        if bool(sc.get('sig')) != (abs(r_true) > sc['cv']):
            rep.fail(sid, 'significance', 'sig = %s, but |r| = %.4f vs cv %s' % (sc.get('sig'), abs(r_true), sc['cv']))
    if abs((a + b * sc['predictX']) - sc['predictY']) > 0.05:
        rep.fail(sid, 'prediction', 'predictY = %s, a + b x %s = %.3f' % (sc['predictY'], sc['predictX'], a + b * sc['predictX']))
    inside = sc['xRange'][0] <= sc['sq4X'] <= sc['xRange'][1]
    if (sc['sq4Type'] == 'interpolation') != inside:
        rep.fail(sid, 'reliability', 'sq4Type %s, but x = %s is %s %s' % (sc['sq4Type'], sc['sq4X'],
                                                                          'inside' if inside else 'outside', sc['xRange']))


def check_bank(rep, bank):
    for level, scs in bank.items():
        for sc in scs:
            check_scenario(rep, level, sc)


RENDER_JS = """async (level) => {
  window.__texts = [];
  const orig = CanvasRenderingContext2D.prototype.fillText;
  CanvasRenderingContext2D.prototype.fillText = function (t, x, y) { window.__texts.push(String(t)); return orig.apply(this, arguments); };
  const out = [];
  for (const sc of SCENARIOS[level]) {
    state.level = level; state.scenarios = [sc]; state.currentIdx = 0; state.score = 0;
    window.__texts = [];
    try { loadScenario(); } catch (e) { out.push({id: sc.id, error: String(e)}); continue; }
    const first = state.subQuestions[0];
    out.push({id: sc.id, firstLabel: first.label, texts: window.__texts.slice()});
  }
  CanvasRenderingContext2D.prototype.fillText = orig;
  return out;
}"""


def check_rendered(rep, rendered):
    for level, rows in rendered.items():
        for row in rows:
            if row.get('error'):
                rep.fail(row['id'], 'render', row['error'])
                continue
            asks_line = row['firstLabel'] == 'Calculate b and a'
            eq = [t for t in row['texts'] if t.startswith('y = ')]
            if asks_line and eq:
                rep.fail(row['id'], 'picture (before answering)',
                         'the first question asks for b and a, and the canvas already shows %r' % eq[0])


def load_and_render(patch_js=None):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/' + SLUG + '/_withdrawn.html?cb=verify', wait_until='load', timeout=20000)
            page.wait_for_function('typeof SCENARIOS !== "undefined" && typeof loadScenario === "function"', timeout=8000)
            if patch_js:
                page.evaluate(patch_js)
            bank = page.evaluate('JSON.parse(JSON.stringify(SCENARIOS))')
            rendered = {lv: page.evaluate(RENDER_JS, lv) for lv in bank}
            browser.close()
            if errors:
                sys.exit('page errors while rendering: %s' % '; '.join(errors))
            return bank, rendered
    finally:
        proc.terminate()
        proc.wait()


def selftest(bank, rendered):
    lines, ok = [], True
    base = Report()
    check_bank(base, bank)
    check_rendered(base, rendered)

    def expect(name, rep_fn):
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

    def wrong_cv(b):
        b['alevel'][0]['cv'] = 0.4683           # AL1, n = 20: the n = 18 value
    expect('wrong value (AL1 cv = 0.4683)', lambda rep: check_bank(rep, mutated(wrong_cv)))

    def wrong_key(b):
        b['alevel'][5]['sig'] = True            # AL6: |r| 0.44 < 0.5760, keyed significant
    expect('wrong key (AL6 sig = true)', lambda rep: check_bank(rep, mutated(wrong_key)))

    def wrong_pred(b):
        b['core'][0]['predictY'] = 84.2
    expect('wrong prediction (CM1 84.2)', lambda rep: check_bank(rep, mutated(wrong_pred)))

    leak = copy.deepcopy(rendered)
    for row in leak['alevel']:
        row['firstLabel'] = 'Calculate b and a'   # an A-level round asking for the line it draws
    expect('pre-answer leak (line drawn, then asked)', lambda rep: check_rendered(rep, leak))
    return ok, lines


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    args = ap.parse_args()
    bank, rendered = load_and_render()
    rep = Report()
    check_bank(rep, bank)
    check_rendered(rep, rendered)
    for f in rep.fails:
        print('FAIL ' + f)
    ok = not rep.fails
    if not args.no_selftest:
        s_ok, lines = selftest(bank, rendered)
        print('\nFault-injection self-test (patched copies; the file is never touched):')
        for ln in lines:
            print(ln)
        ok = ok and s_ok
    total = sum(len(v) for v in bank.values())
    bad = {f.split(' ', 1)[0] for f in rep.fails}
    print('\n%s: %d FAIL(s) across %d of %d scenarios' % ('PASS' if ok else 'FAILED', len(rep.fails), len(bad), total))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
