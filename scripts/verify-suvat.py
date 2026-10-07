#!/usr/bin/env python3
# ci-line: E | SUVAT Selector (every key from the data both ways, at its stated precision; marking through MaffsAnswer in Chromium) |
"""SUVAT Selector: every typed key recomputed from the data, at the precision the step states, marked by MaffsAnswer.

The tranche 5 audit (6 Oct 2026) found a sprinter with no real solution keyed u = 4 (level4[7]), a signed v_y keyed
positive (ALEVEL[34]), an item whose "find" was also a known (ALEVEL[39]), answers rounded early (ALEVEL[18], [41],
[48]), a launch height that never said the particle lands (ALEVEL[22]), local parseFloat-and-tolerance marking with no
precision stated (SR-1), multi-step items logged from their last step only, and wrong answers on fixed timers.
Project Claude supplied replacement data for level4[7] and ALEVEL[39] (7 Oct 2026).

Keys. Each step is solved again from its own data with SymPy (the item's equation, solved for its unknown), by two
  routes: from the exact data (a component from its speed and angle), and from the values the student is shown (the
  rounded components on the chips, the previous step's key). A step that states a precision (dp) must have both
  routes round, half up, to its key at dp; a step that states none must have both routes equal the key exactly.
  Second steps follow SECOND (each step's own formula as its prompt states it). Level 4 keys are exact.
Phase 0. u_x and u_y are the speed's components, to 2 d.p.
Working. Every step's key, as the step states it, appears in the item's working.
Chromium (390x844, both levels). Every step of every item is played through the game's own handler: the key at its
  precision is marked right; the key one unit out in its last place is marked wrong and waits for Next (MaffsNext);
  an unrounded answer (where a precision is stated) is not marked at all ('format'), and nor is "abc"; the prompt
  states the precision. Every phase 0 too.

A self-test plants two of the audit's own faults back (t5-002: v_y keyed +0.32; t5-007: the range keyed 103.5 to
1 d.p.); each must FAIL naming its item.

    python scripts/verify-suvat.py [--no-selftest] [--against FILE] [--katex-dir DIR]
"""
import argparse
import os
import re
import sys
from decimal import ROUND_HALF_UP, Decimal

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'suvat'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
s_, u_, v_, a_, t_ = sp.symbols('s u v a t')
EQ = {'v = u + at': sp.Eq(v_, u_ + a_ * t_), 's = ut + ½at²': sp.Eq(s_, u_ * t_ + a_ * t_ ** 2 / 2),
      'v² = u² + 2as': sp.Eq(v_ ** 2, u_ ** 2 + 2 * a_ * s_), 's = ½(u+v)t': sp.Eq(s_, (u_ + v_) * t_ / 2),
      's = vt − ½at²': sp.Eq(s_, v_ * t_ - a_ * t_ ** 2 / 2)}
V = {'s': s_, 'u': u_, 'v': v_, 'a': a_, 't': t_}
TAGS = {('l4', 7): 't5-001', ('al', 34): 't5-002', ('al', 39): 't5-003', ('al', 18): 't5-007', ('al', 41): 't5-007',
        ('al', 48): 't5-007', ('al', 22): 't5-008'}
# Items asking for a magnitude (the prompt says |...| or "Give magnitude"): the key is the size of the solution
SIGNED = {('al', 34, 0)}        # v_y asked with its sign


def where(lvl, i, j=None):
    t = TAGS.get((lvl, i))
    return '%s[%d]%s%s' % ({'al': 'ALEVEL', 'l4': 'LEVEL4'}[lvl], i, '' if j is None else ' step %d' % (j + 1),
                           ' (suvat-%s)' % t if t else '')


def rnd(x, dp):
    return Decimal(str(sp.N(x, 40))).quantize(Decimal(1).scaleb(-dp), ROUND_HALF_UP)


def ux(q, exact):
    p = q['phase0']
    return p['speed'] * sp.cos(sp.rad(p['angle'])) if exact else sp.nsimplify(p['ux'])


# A second step, as its prompt states it: (first step's value, item, exact route?) -> value
SECOND = {
    18: lambda r, q, x: 30 / r,                                       # u_x = 30 / t
    23: lambda r, q, x: sp.Rational(1, 2) * sp.Rational(98, 10) * r ** 2,   # h = 1/2 (9.8) t^2
    24: lambda r, q, x: sp.sqrt(10 ** 2 + r ** 2),                    # speed from v_x = 10
    25: lambda r, q, x: sp.sqrt(18 ** 2 + r ** 2),
    27: lambda r, q, x: 40 / r,
    34: lambda r, q, x: sp.sqrt(ux(q, x) ** 2 + r ** 2),
    37: lambda r, q, x: ux(q, x) * r,
    39: lambda r, q, x: ux(q, x),                                     # at the top the speed is u_x
    41: lambda r, q, x: ux(q, x) * r,
    42: lambda r, q, x: sp.asin(r / 24) * 180 / sp.pi,
    45: lambda r, q, x: sp.sqrt(ux(q, x) ** 2 + r ** 2),
    48: lambda r, q, x: ux(q, x) * r,
    49: lambda r, q, x: r / sp.sin(sp.pi / 3),
}


def first(q, exact):
    kn = dict(q['known'])
    if exact and 'phase0' in q:
        p = q['phase0']
        uy = p['speed'] * sp.sin(sp.rad(p['angle']))
        if 'u' in kn and abs(float(kn['u']) - float(uy)) < 0.01:
            kn['u'] = uy
    e = EQ[q['equation']].subs({V[k]: (x if isinstance(x, sp.Basic) else sp.nsimplify(x)) for k, x in kn.items()})
    return [r for r in sp.solve(e, V[q['find']]) if r.is_real and r != 0]


def fmt(key, dp):
    return str(key) if dp is None else ('%.' + str(dp) + 'f') % float(key)


def check_step(fails, w, key, dp, e, r):
    if dp is None:
        if not (sp.simplify(e - r) == 0 and sp.nsimplify(key) == sp.nsimplify(e)):
            fails.append('%s: keyed %s exactly, but its data gives %s (from the values shown: %s); a rounded answer '
                         'must state its precision (SR-1)' % (w, key, sp.N(e, 8), sp.N(r, 8)))
        return
    k = Decimal(str(key)).quantize(Decimal(1).scaleb(-dp))
    if rnd(e, dp) != rnd(r, dp):
        fails.append('%s: to %d d.p. the exact data gives %s but the values shown give %s: state a precision at '
                     'which they agree' % (w, dp, rnd(e, dp), rnd(r, dp)))
    elif rnd(e, dp) != k:
        fails.append('%s: keyed %s; its data gives %s to %d d.p. (%s)' % (w, key, rnd(e, dp), dp, sp.N(e, 8)))


def check_bank(fails, bank):
    for lvl in ('l4', 'al'):
        for i, q in enumerate(bank[lvl]):
            try:
                sols = first(q, True)
                sols_r = first(q, False)
            except Exception as ex:   # noqa: BLE001
                fails.append('%s: cannot be solved (%s)' % (where(lvl, i), ex))
                continue
            if not sols:
                fails.append('%s: the equation has no real solution for %s from this data' % (where(lvl, i), q['find']))
                continue
            steps = q['steps'] if lvl == 'al' else [{'answer': q['answer'], 'dp': q.get('dp'), 'prompt': q['find']}]
            if lvl == 'al' and 'tol' in steps[0] or lvl == 'l4' and 'tol' in q:
                fails.append('%s: marked by a tolerance, not at a stated precision (suvat-t5-006)' % where(lvl, i))
            k1 = steps[0]['answer']
            signed = (lvl, i, 0) in SIGNED
            pick = lambda ss: min(ss, key=lambda r: abs(float(r) - k1) if signed else abs(abs(float(r)) - abs(k1)))
            e1, r1 = pick(sols), pick(sols_r)
            if not signed:
                e1, r1 = abs(e1), abs(r1)
            if q['find'] in q['known']:
                fails.append('%s: the unknown %s is also given' % (where(lvl, i), q['find']))
            for j, st in enumerate(steps):
                w = where(lvl, i, j if lvl == 'al' and len(steps) > 1 else None)
                if j == 0:
                    e, r = e1, r1
                elif i in SECOND:
                    e = SECOND[i](abs(e1), q, True)
                    r = SECOND[i](abs(sp.nsimplify(k1)), q, False)
                else:
                    fails.append('%s: a second step with no formula in SECOND' % w)
                    continue
                check_step(fails, w, st['answer'], st.get('dp'), e, r)
                # the working quotes the key as the step states it
                shown = fmt(st['answer'], st.get('dp'))
                if not re.search(r'(?<![\d.])' + re.escape(shown.lstrip('-')) + r'(?![\d])', q.get('working', '')):
                    fails.append('%s: the working does not give the key %s' % (w, shown))
            if 'phase0' in q:
                p = q['phase0']
                for name, val in (('u_x', p['speed'] * sp.cos(sp.rad(p['angle']))),
                                  ('u_y', p['speed'] * sp.sin(sp.rad(p['angle'])))):
                    key = p['ux'] if name == 'u_x' else p['uy']
                    if rnd(val, 2) != Decimal(str(key)).quantize(Decimal('0.01')):
                        fails.append('%s: phase 0 %s keyed %s; %s to 2 d.p.' % (where(lvl, i), name, key, rnd(val, 2)))
                if 'tol' in p:
                    fails.append('%s: phase 0 marked by a tolerance (suvat-t5-006)' % where(lvl, i))
    sc = bank['al'][22]['scenario']
    if 'lands' not in sc:
        fails.append('%s: the launch height needs the particle to land at 3 s; the scenario never says so' % where('al', 22))


# ------------------------------------------------------------------ Chromium
SWEEP_JS = r"""(lvl) => {
  const out = [];
  const realTimeout = window.setTimeout; window.setTimeout = () => 0;
  const pool = lvl === 'al' ? QUESTIONS_ALEVEL : QUESTIONS_LEVEL4;
  const btnOf = id => document.querySelector('#' + id + ' .calc-btn');
  try {
    startGame();
    pool.forEach((q, i) => {
      const steps = lvl === 'al' ? q.steps : [{answer: q.answer, dp: q.dp}];
      steps.forEach((st, j) => {
        const fmt = (x, dp) => dp === undefined ? String(x) : Number(x).toFixed(dp);
        const unit = st.dp === undefined ? 1 : Math.pow(10, -st.dp);
        const tries = [['key', fmt(st.answer, st.dp)], ['off', fmt(Number(st.answer) + unit, st.dp)], ['abc', 'abc']];
        if (st.dp !== undefined) tries.push(['unrounded', fmt(Number(st.answer) + unit / 10 * 3, st.dp + 1)]);
        tries.forEach(([kind, typed]) => {
          currentQ = q; questions = [q, q]; qNum = 1; currentStep = j; _svQOk = true;
          const before = score, counted = _svCorrectCount;
          if (lvl === 'al') { showPhase2AL(); currentStep = j; loadStep(); } else showPhase2L4(false);
          btnOf('phase2').disabled = false;
          const prompt = document.getElementById('calcQ').textContent;
          document.getElementById('calcInput').value = typed;
          submitCalc();
          const fb = document.getElementById('fb2');
          out.push([i, j, kind, typed, fb.className, fb.textContent, !!document.querySelector('#exp2 .maffs-next-wrap'),
                    score - before, prompt]);
          if (window.MaffsNext) MaffsNext.clear(document.getElementById('exp2'));
          btnOf('phase2').disabled = false;
        });
      });
      if (q.phase0) {
        [['key', q.phase0.ux.toFixed(2), q.phase0.uy.toFixed(2)], ['off', (q.phase0.ux + 0.01).toFixed(2), q.phase0.uy.toFixed(2)]]
          .forEach(([kind, x, y]) => {
            currentQ = q; questions = [q, q]; qNum = 1; showPhase0();
            btnOf('phase0').disabled = false;
            document.getElementById('p0ux').value = x; document.getElementById('p0uy').value = y;
            submitPhase0();
            const fb = document.getElementById('fb0');
            out.push([i, -1, kind, x + ',' + y, fb.className, fb.textContent, !!document.querySelector('#phase0 .maffs-next-wrap'), 0, '']);
            if (window.MaffsNext) MaffsNext.clear(document.getElementById('phase0'));
            btnOf('phase0').disabled = false;
          });
      }
    });
  } finally { window.setTimeout = realTimeout; }
  return out;
}"""

KATEX_DIR = None


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    bank = {}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            for lvl, q in (('al', 'alevel'), ('l4', 'level4')):
                ctx = browser.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True)
                page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
                ctx.route(lambda url: not url.startswith(base) and '/katex@' not in url, lambda route: route.abort())
                if KATEX_DIR:
                    ctx.route(lambda url: '/katex@0.16.9/dist/' in url, lambda route: route.fulfill(
                        path=os.path.join(KATEX_DIR, route.request.url.split('/dist/', 1)[1].split('?')[0])))
                ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                    status=200, content_type='text/html; charset=utf-8', body=html))
                ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
                page = ctx.new_page()
                errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.goto(base + '/games/%s/?level=%s&cb=verify' % (SLUG, q), wait_until='load', timeout=20000)
                page.wait_for_function('typeof QUESTIONS_ALEVEL !== "undefined"', timeout=15000)
                bank = page.evaluate('({al: QUESTIONS_ALEVEL, l4: QUESTIONS_LEVEL4})')
                if page.evaluate('typeof MaffsAnswer === "undefined" || typeof markTyped === "undefined"'):
                    fails.append('typed answers are not marked by MaffsAnswer at a stated precision (suvat-t5-006)')
                    ctx.close()
                    continue
                rows = page.evaluate(SWEEP_JS, lvl)
                for i, j, kind, typed, cls, text, nxt, gained, prompt in rows:
                    w = where(lvl, i, j if j >= 0 else None) + (' phase 0' if j < 0 else '')
                    item = bank[lvl][i]
                    st = (item['steps'][j] if lvl == 'al' else {'dp': item.get('dp')}) if j >= 0 else {'dp': 2}
                    if kind == 'key' and 'correct' not in cls:
                        fails.append('%s: the key %s is not marked right (%r)' % (w, typed, text))
                    if kind == 'off' and ('wrong' not in cls or not nxt):
                        fails.append('%s: %s is not marked wrong with Next (%r)' % (w, typed, text))
                    if kind in ('unrounded', 'abc') and ('correct' in cls or 'wrong' in cls or gained):
                        fails.append('%s: %s (%s) was marked; it should get the message and no mark' % (w, typed, kind))
                    if j >= 0 and kind == 'key' and st.get('dp') is not None:
                        want = 'nearest whole number' if st['dp'] == 0 else '%d d.p.' % st['dp']
                        if want not in prompt:
                            fails.append('%s: the prompt does not state the precision (%r)' % (w, prompt))
                if errors:
                    fails.append('page errors: %s' % '; '.join(errors[:3]))
                ctx.close()
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return bank


PLANTS = [
    ('ALEVEL[34] step 1', 't5-002: v_y keyed +0.32', 'answer:-0.32,dp:2', 'answer:0.32,dp:2'),
    ('ALEVEL[48] step 2', 't5-007: the range keyed 103.5 to 1 d.p.', 'answer:103,dp:0', 'answer:103.5,dp:1'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    ap.add_argument('--katex-dir', help='serve KaTeX from this local dist/ folder')
    args = ap.parse_args()
    global KATEX_DIR
    KATEX_DIR = args.katex_dir
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    bank = play(fails, html)
    if bank:
        check_bank(fails, bank)
    print('%s: every key from the data both ways, at its stated precision; marking through MaffsAnswer in Chromium'
          % SLUG)
    ok = True
    if not args.no_selftest and not args.against:
        for prefix, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-44s *** CANNOT PLANT (%d) ***' % (what, html.count(old)))
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(old, new))
            if planted:
                check_bank(rep, planted)
            hit = [f for f in rep if f.startswith(prefix)]
            ok = ok and bool(hit)
            print('  self-test %-44s %s' % (what, ('caught: ' + hit[0][:100]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
