#!/usr/bin/env python3
# ci-line: B2 | Complex Converter (every key equal to its given number, the principal argument stated and keyed, no option a second form of the key; every option marked in Chromium) |
"""Complex Converter: every Form Roulette key is the given number, in the one form the question asks for.

Form Roulette (55 items, Level 4 and Further Maths share one bank) shows a complex number in one form and asks
for it in another: Cartesian, polar (r∠θ°) or exponential (re^{jθ}). The tranche 6 audit of 7 Oct 2026 found
3 − 4j keyed 5∠−53.13° with 5∠306.87°, the same number, among the wrong options, and no angle range stated
(complex-converter-t6-001, HIGH). Contract LISTED-HIGH (Jon, 9 Oct 2026): state the convention, θ with
−180° < θ ≤ 180° (the principal argument), on every item, and no item's options may hold two forms of the
same number. Matching Triples draws its polar and exponential cards from each item's stored argDeg and argRad,
so those follow the convention too.

Every option is read as a complex number (TeX: \\dfrac, \\sqrt, \\pi, j; polar angles in degrees, exponential
in radians). Then, for every item: the key equals the given number (to the bank's rounding); no wrong option
does; a polar or exponential key's angle is principal; the stored re, im, r, argDeg and argRad are the given
number, with principal angles; no context asks for another range ("positive angle"). In Chromium (390x844)
every item is shown through showRouletteQ() and every option clicked through rouletteAnswer(): the key marked
right, the others wrong, and a polar or exponential question's target line states the range.
A self-test plants the audit's item and one item's old positive-angle key back into a copy of the page; each
must FAIL naming its item.

    python scripts/verify-complex-converter.py [--no-selftest] [--against FILE] [--katex-dir DIR]
"""
import argparse
import cmath
import math
import os
import re
import sys

import sympy as sp
from sympy.parsing.sympy_parser import (implicit_multiplication_application, parse_expr,
                                        standard_transformations)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'complex-converter'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNT = 55
J = sp.Symbol('J')
TRANSFORMS = standard_transformations + (implicit_multiplication_application,)
RANGE_WORDS = {'polar': '−180° < θ ≤ 180°', 'exponential': '−π < θ ≤ π'}


def group(s, i):
    d = 0
    for k in range(i, len(s)):
        d += (s[k] == '{') - (s[k] == '}')
        if d == 0:
            return s[i + 1:k], k + 1
    raise ValueError('unbalanced braces in %r' % s)


def to_py(s):
    out, i = '', 0
    while i < len(s):
        m = re.match(r'\\[dt]?frac\{', s[i:])
        if m:
            p, k = group(s, i + m.end() - 1)
            q, n = group(s, k)
            out, i = out + '((%s)/(%s))' % (to_py(p), to_py(q)), n
            continue
        if s.startswith('\\sqrt{', i):
            p, k = group(s, i + 5)
            out, i = out + ' sqrt(%s)' % to_py(p), k
            continue
        if s.startswith('\\pi', i):
            out, i = out + ' pi ', i + 3
            continue
        if s.startswith('\\cdot', i):
            out, i = out + '*', i + 5
            continue
        if s[i] == '\\':
            raise ValueError('unknown TeX in %r' % s)
        out, i = out + {'j': ' J ', '{': '(', '}': ')', '°': ''}.get(s[i], s[i]), i + 1
    return out


def real(s):
    s = s.strip()
    if s in ('', '+'):
        return 1.0
    if s == '-':
        return -1.0
    return float(parse_expr(to_py(s), local_dict={'pi': sp.pi, 'sqrt': sp.sqrt}, transformations=TRANSFORMS))


def value(s):
    """(complex value, form, angle as written or None). ValueError when it cannot be read."""
    t = s.strip()
    if '\\angle' in t:
        r, th = t.split('\\angle')
        deg = real(th)
        return real(r) * cmath.exp(1j * math.radians(deg)), 'polar', deg
    m = re.fullmatch(r'(.*?)e\^\{(.*)\}', t)
    if m:
        ex = m.group(2).replace('\\cdot', '').replace(' ', '')
        sign = -1 if ex.startswith('-') else 1
        rad = sign * real(ex.lstrip('-').replace('j', '', 1))
        return real(m.group(1)) * cmath.exp(1j * rad), 'exponential', rad
    e = parse_expr(to_py(t), local_dict={'J': J, 'pi': sp.pi, 'sqrt': sp.sqrt}, transformations=TRANSFORMS)
    e = sp.expand(e)
    return complex(float(e.subs(J, 0)), float(e.coeff(J))), 'cartesian', None


def close(a, b):
    return abs(a - b) <= 0.002 * max(1.0, abs(a))


def principal(form, angle):
    if form == 'polar':
        return -180 < angle <= 180
    if form == 'exponential':
        return -math.pi < angle <= math.pi + 1e-9
    return True


def check_bank(fails, bank):
    if len(bank) != COUNT:
        fails.append('bank: %d items, expected %d' % (len(bank), COUNT))
    for q in bank:
        w = 'id %d (%s → %s, %s)' % (q['id'], q['source'], q['target'], q['givenLatex'])
        opts = [q['correctLatex']] + list(q['distractors'])
        if q['correct'] != q['correctLatex'] or len(set(opts)) != 4:
            fails.append('%s: the options %s are not four distinct strings with one key' % (w, opts))
        try:
            z = value(q['givenLatex'])[0]
            vals = [value(o) for o in opts]
        except Exception as e:
            fails.append('%s: cannot read: %s' % (w, e))
            continue
        key, form, angle = vals[0]
        if form != q['target']:
            fails.append('%s: the key %s is %s form, the question asks for %s' % (w, opts[0], form, q['target']))
        if not close(key, z):
            fails.append('%s: keyed %s = %.4f%+.4fj, the given number is %.4f%+.4fj'
                         % (w, opts[0], key.real, key.imag, z.real, z.imag))
        if angle is not None and not principal(form, angle):
            fails.append('%s: the key %s is not the principal argument (%s)' % (w, opts[0], RANGE_WORDS[form]))
        for o, (v, _, _) in zip(opts[1:], vals[1:]):
            if close(v, z):
                fails.append('%s: the wrong option %s is the same number as the key %s' % (w, o, opts[0]))
        stored = q['r'] * cmath.exp(1j * math.radians(q['argDeg']))
        if not (close(complex(q['re'], q['im']), z) and close(stored, z)
                and abs(math.radians(q['argDeg']) - q['argRad']) < 0.002):
            fails.append('%s: stored re %s, im %s, r %s, argDeg %s, argRad %s are not the given number'
                         % (w, q['re'], q['im'], q['r'], q['argDeg'], q['argRad']))
        if not (-180 < q['argDeg'] <= 180 and -math.pi < q['argRad'] <= 3.1416):
            fails.append('%s: stored argDeg %s / argRad %s are not principal (Triples shows them)'
                         % (w, q['argDeg'], q['argRad']))
        if 'positive' in (q.get('context') or '').lower():
            fails.append('%s: the context asks for another range: %r' % (w, q['context']))


SWEEP_JS = r"""(words) => {
  window.setTimeout = () => 0;
  const out = [];
  QUESTIONS.level4.forEach(q => {
    for (const pick of [q.correctLatex, ...q.distractors]) {
      rQuestions = [q]; rIndex = 0; rScore = 0; rCorrect = 0; rTimes = []; rDirStats = {};
      showScreen('rouletteScreen');
      showRouletteQ();
      const target = document.getElementById('rTarget').textContent;
      if (words[q.target] && !target.includes(words[q.target])) out.push([q.id, pick, 'target line "' + target + '" does not state the range']);
      const shown = [...document.querySelectorAll('#rOptions .opt-btn')];
      if (shown.length !== 4) out.push([q.id, pick, shown.length + ' options on screen']);
      const btn = shown.find(x => x.dataset.val === pick);
      if (!btn) { out.push([q.id, pick, 'not on screen']); continue; }
      btn.click();
      const right = btn.classList.contains('correct');
      if (right !== (pick === q.correctLatex)) out.push([q.id, pick, right ? 'marked right' : 'marked wrong']);
    }
  });
  return out;
}"""
KATEX_DIR = None


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base) and '/katex@' not in url, lambda route: route.abort())
            if KATEX_DIR:
                ctx.route(lambda url: '/katex@' in url and '/dist/' in url, lambda route: route.fulfill(
                    path=os.path.join(KATEX_DIR, route.request.url.split('/dist/', 1)[1].split('?')[0])))
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?level=level4&cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof katex !== "undefined"', timeout=15000)
            bank = page.evaluate('() => QUESTIONS.level4')
            for qid, pick, what in page.evaluate(SWEEP_JS, RANGE_WORDS):
                fails.append('id %d in Chromium: option %s %s' % (qid, pick, what))
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            return bank
    finally:
        proc.terminate()
        proc.wait()


# (the item the failure must name, what is planted, today's text, main's text before LISTED-HIGH).
PLANTS = [
    ('id 21 ', 't6-001: 5∠306.87° beside the key 5∠−53.13°',
     'distractors:["5\\\\angle 53.13°","5\\\\angle 126.87°","5\\\\angle -126.87°"]',
     'distractors:["5\\\\angle 53.13°","5\\\\angle 306.87°","5\\\\angle -126.87°"]'),
    ('id 20 ', 'the old positive-angle key 5∠233.13°',
     'correct:"5\\\\angle -126.87°",correctLatex:"5\\\\angle -126.87°"',
     'correct:"5\\\\angle 233.13°",correctLatex:"5\\\\angle 233.13°"'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    ap.add_argument('--katex-dir', help='serve KaTeX from this local dist/ folder')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    global KATEX_DIR
    KATEX_DIR = args.katex_dir
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    bank = play(fails, html)
    if bank is not None:
        check_bank(fails, bank)
    print('%s: %d Form Roulette items, every option read as a number and clicked in Chromium'
          % (SLUG, len(bank or [])))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, new, old in PLANTS:
            if html.count(new) != 1:
                print('  self-test %-46s *** CANNOT PLANT (%d) ***' % (what, html.count(new)))
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(new, old))
            if planted is not None:
                check_bank(rep, planted)
            hit = [f for f in rep if f.startswith(tag)]
            ok = ok and bool(hit)
            print('  self-test %-46s %s' % (what, ('caught: ' + hit[0][:110]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
