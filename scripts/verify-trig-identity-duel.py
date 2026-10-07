#!/usr/bin/env python3
# ci-line: B4 | Trig Identity Duel (every option read into SymPy: exactly one equals the key, compound-angle and triangle keys recomputed, marking in Chromium) |
"""Trig Identity Duel: every key and every option evaluated with SymPy; every item marked in Chromium.

The game (99 multiple-choice items: gcse 50, alevel 49) asks for exact values, sine and cosine rule results,
areas, identities and simplifications. Its bank was keyed by hand; the tranche 2 audit of 6 Oct 2026 found the
7, 9, 11 triangle's largest angle keyed 86.2° (it is 85.9°), all three compound-angle items for sin A = 3/5,
cos B = 5/13 keyed with another item's value (the right value offered as a wrong option), "expand and simplify"
items whose wrong option was identical to the key, an angle with a second valid answer, and an
under-specified kite.

Every option is read from its TeX into SymPy (tex() below; an option it cannot read FAILS: extend tex(), never
skip), and TARGETS below says what each item asks for: an exact value (the item's own expression), an identity
(an option identical to the expression, or, for "Which is NOT equivalent?", the one option that is not), a value
computed from the context's numbers (rounded half up where the ask states d.p.), a count of solutions, or a
reviewed verdict. Then:
  the key equals the target, at the stated precision where there is one (SR-1: an ask whose target is not exact
  must state its precision); no wrong option equals the target (SR-4, SR-16); the four options are distinct in
  value unless the ask names the form; and in Chromium (390x844) every item is shown through the game's own
  showQ() and every option clicked through handle(): the key marked right, the others wrong.
A self-test plants three of the audit's own faults back into a copy of the page (t2-001: 86.2°; t2-002: sin(A+B)
keyed 56/65; t2-005: the identical option 1 + 2 sin x cos x); each must FAIL naming its item.

    python scripts/verify-trig-identity-duel.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import random
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

import sympy as sp
from sympy.parsing.sympy_parser import (implicit_multiplication_application, parse_expr, rationalize,
                                        standard_transformations)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'trig-identity-duel'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNTS = {'gcse': 50, 'alevel': 49}
theta, x, A, B = sp.symbols('theta x A B')
LOCAL = {'theta': theta, 'x': x, 'A': A, 'B': B, 'pi': sp.pi, 'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
         'sec': sp.sec, 'csc': sp.csc, 'cot': sp.cot, 'asin': sp.asin, 'acos': sp.acos, 'sqrt': sp.sqrt}
TRANS = standard_transformations + (implicit_multiplication_application, rationalize)
FUNCS = ('sin', 'cos', 'tan', 'sec', 'csc', 'cot')


def group(s, i, o, c):
    """s[i] is the opening bracket o: return (inner text, index after the closing bracket)."""
    d = 0
    for j in range(i, len(s)):
        d += (s[j] == o) - (s[j] == c)
        if d == 0:
            return s[i + 1:j], j + 1
    raise ValueError('unbalanced %s in %r' % (o, s))


def tex(s):
    """An option's TeX (or plain text) as a SymPy expression; ValueError if it cannot be read."""
    s = s.replace('\u2212', '-').replace('\\left', '').replace('\\right', '').replace('\\,', ' ').strip()
    s = re.sub(r'(\d+(?:\.\d+)?)\s*\u00b0', r'(\1*\\pi/180)', s)
    out, i = '', 0
    while i < len(s):
        m = re.match(r'\\[dt]?frac\{', s[i:])
        if m:
            num, j = group(s, i + m.end() - 1, '{', '}')
            den, k = group(s, j, '{', '}')
            out += '((%s)/(%s))' % (tex(num), tex(den))
            i = k
            continue
        if s.startswith('\\sqrt{', i):
            inner, j = group(s, i + 5, '{', '}')
            out += 'sqrt(%s)' % tex(inner)
            i = j
            continue
        m = re.match(r'\\(sin|cos|tan|sec|csc|cot)', s[i:])
        if m:
            f, i = m.group(1), i + m.end()
            power = None
            if s.startswith('^{-1}', i):
                f, i = 'a' + f, i + 5
            elif s.startswith('^', i):
                pm = re.match(r'\^(\{[^}]*\}|\d)', s[i:])
                power, i = pm.group(1).strip('{}'), i + pm.end()
            while i < len(s) and s[i] == ' ':
                i += 1
            if s.startswith('(', i):
                arg, i = group(s, i, '(', ')')
                arg = tex(arg)
            elif s.startswith('\\dfrac', i) or s.startswith('\\frac', i):
                m2 = re.match(r'\\[dt]?frac\{', s[i:])
                num, j = group(s, i + m2.end() - 1, '{', '}')
                den, k = group(s, j, '{', '}')
                arg, i = '(%s)/(%s)' % (tex(num), tex(den)), k
            else:
                am = re.match(r'(\d*)\s*(\\theta|\\pi|[xAB])', s[i:])
                if not am:
                    raise ValueError('no argument after \\%s in %r' % (f, s))
                arg, i = (am.group(1) + '*' if am.group(1) else '') + am.group(2).lstrip('\\'), i + am.end()
            call = '%s(%s)' % (f, arg)
            out += '(%s)**(%s)' % (call, power) if power else call
            continue
        if s.startswith('\\theta', i):
            out, i = out + ' theta ', i + 6
            continue
        if s.startswith('\\pi', i):
            out, i = out + ' pi ', i + 3
            continue
        if s.startswith('\\cdot', i):
            out, i = out + '*', i + 5
            continue
        if s[i] == '{':
            inner, j = group(s, i, '{', '}')
            out, i = out + '(%s)' % tex(inner), j
            continue
        if s[i] == '\\':
            raise ValueError('unknown TeX command in %r' % s)
        out += '**' if s[i] == '^' else s[i]
        i += 1
    try:
        return parse_expr(out, local_dict=LOCAL, transformations=TRANS)
    except Exception as e:
        raise ValueError('cannot read %r (%s): %s' % (s, out, e))


def same(a, b):
    """Equal in value: exactly for constants, at random points for expressions."""
    d = sp.simplify(a - b) if not (a.free_symbols or b.free_symbols) else None
    if d is not None:
        return d == 0 or abs(sp.N(a - b, 50)) < 1e-40
    rng = random.Random(7)
    syms = sorted(a.free_symbols | b.free_symbols, key=str)
    hits = 0
    for _ in range(12):
        pt = {v: sp.Rational(rng.randint(5, 140), 100) for v in syms}
        try:
            av, bv = complex(sp.N(a.subs(pt), 30)), complex(sp.N(b.subs(pt), 30))
        except (TypeError, ZeroDivisionError):
            continue
        if abs(av - bv) > 1e-9:
            return False
        hits += 1
    return hits >= 8


def deg(v):
    return sp.N(v * 180 / sp.pi, 40)


def D(d):
    return d * sp.pi / 180


def law_angle(a, b, c):        # the angle opposite c, in degrees
    return deg(sp.acos(sp.Rational(a * a + b * b - c * c, 2 * a * b)))


# What each item asks for, in bank order. ('value',) the item's own expression; ('ident',) an option identical
# to it; ('ident', expr) identical to expr; ('notequiv',); ('num', target, dp, unit); ('count', n); ('verdict', key, why).
S30, S45, S60 = sp.sin(D(30)), sp.sin(D(45)), sp.sin(D(60))
TARGETS = {
    'gcse': [('value',)] * 12 + [
        ('num', 5 * sp.sin(D(45)) / sp.sin(D(30)), 1, ''), ('num', 8 * sp.sin(D(60)) / sp.sin(D(40)), 1, ''),
        ('num', 10 * sp.Rational(8, 10) / sp.Rational(1, 2), None, ''), ('num', 6 * sp.sin(D(90)) / sp.sin(D(30)), None, ''),
        ('num', 10 * sp.sin(D(60)) / sp.sin(D(45)), 1, ''), ('num', deg(sp.asin(8 * sp.sin(D(50)) / 12)), 1, '°'),
        ('num', 7 * sp.sin(D(80)) / sp.sin(D(60)), 1, ''), ('num', 9 * sp.sin(D(70)) / sp.sin(D(35)), 1, ''),
        ('num', 15 * sp.sin(D(55)) / sp.sin(D(40)), 1, ''), ('num', 20 * sp.sin(D(45)) / sp.sin(D(65)), 1, ''),
        ('num', 40, None, '°'), ('num', 30, None, '°'),
        ('num', sp.sqrt(25 + 49 - 70 * sp.cos(D(60))), 1, ''), ('num', sp.sqrt(64 + 36 - 96 * sp.cos(D(90))), None, ''),
        ('num', sp.sqrt(9 + 16 - 24 * sp.cos(D(120))), 1, ''), ('num', law_angle(10, 12, 15), 1, '°'),
        ('num', law_angle(7, 9, 11), 1, '°'), ('num', sp.sqrt(25 + 25 - 50 * sp.cos(D(60))), None, ''),
        ('num', 16 + 36 - 48 * sp.cos(D(45)), None, ''), ('num', sp.sqrt(64 + 64 - 128 * sp.cos(D(120))), 1, ''),
        ('num', law_angle(10, 8, 6), 1, '°'), ('num', law_angle(3, 5, 7), 1, '°'),
        ('verdict', 'Yes', '5² + 12² = 13²'), ('verdict', 'Yes', '12² = 144 > 7² + 8² = 113'),
        ('num', sp.Rational(1, 2) * 6 * 8 * S30, None, ''), ('num', sp.Rational(1, 2) * 10 * 7, None, ''),
        ('num', sp.Rational(1, 2) * 5 * 12 * S60, None, ''), ('num', sp.Rational(1, 2) * 64 * S45, None, ''),
        ('num', sp.Rational(1, 2) * 4 * 9 * sp.sin(D(150)), None, ''), ('num', sp.Rational(1, 2) * 100 * sp.sin(D(120)), None, ''),
        ('num', 6 * 10 * S30, None, ''), ('num', sp.Rational(20, 40), None, ''), ('num', 30, None, '°'),
        ('num', sp.Rational(1, 2) * 14 * 9 * S60, 1, ''), ('num', sp.Rational(1, 2) * 36 * S60, None, ''),
        ('num', sp.Rational(25, 2), None, ''), ('num', 6, None, ''), ('num', 2 * sp.Rational(1, 2) * 64 * S60, None, ''),
    ],
    'alevel': [('value',)] * 8 + [
        ('ident',), ('notequiv',), ('ident', sp.sin(theta) ** 2), ('ident', sp.cos(theta) ** 2),
        ('num', 2 * sp.Rational(3, 5) * sp.Rational(4, 5), None, ''), ('num', 2 * sp.Rational(16, 25) - 1, None, ''),
        ('num', sp.sin(2 * sp.pi / 4), None, ''), ('ident',), ('num', 1 - 2 * sp.Rational(25, 169), None, ''),
        ('ident',), ('ident',), ('ident',), ('ident',), ('ident',), ('ident',), ('ident',), ('ident',),
        ('value',), ('value',), ('value',), ('value',), ('ident',), ('ident',),
        ('num', sp.Rational(3, 5) * sp.Rational(5, 13) + sp.Rational(4, 5) * sp.Rational(12, 13), None, ''),
        ('num', sp.Rational(4, 5) * sp.Rational(5, 13) - sp.Rational(3, 5) * sp.Rational(12, 13), None, ''),
        ('num', sp.Rational(4, 5) * sp.Rational(5, 13) + sp.Rational(3, 5) * sp.Rational(12, 13), None, ''),
        ('ident',), ('ident',), ('ident',), ('ident',), ('ident',), ('ident',), ('ident',), ('ident',), ('ident',),
        ('ident',),
        ('count', len(sp.solveset(sp.sin(2 * theta), theta, sp.Interval(0, 2 * sp.pi)))),
        ('count', len(sp.solveset(sp.cos(2 * x) - 1, x, sp.Interval(0, 2 * sp.pi)))),
        ('ident',), ('ident',), ('ident',),
    ],
}
# What the context of a context item must say (so the table above reads the numbers the student is given).
CONTEXT = {
    ('gcse', 16): 'A = 45°, a = 10 cm, B = 60°', ('gcse', 28): 'a = 7, b = 9, c = 11', ('gcse', 44): 'angle C is acute', ('gcse', 49): 'each with sides 8 and 8',
    ('alevel', 31): 'sin A = 3/5, cos B = 5/13', ('alevel', 32): 'sin A = 3/5, cos B = 5/13', ('alevel', 33): 'sin A = 3/5, cos B = 5/13',
}
AUDIT = {('gcse', 28): 't2-001', ('alevel', 31): 't2-002', ('alevel', 32): 't2-003', ('alevel', 33): 't2-004',
         ('alevel', 47): 't2-005', ('alevel', 48): 't2-006', ('gcse', 44): 't2-008', ('gcse', 49): 't2-009'}


def opt_value(o, unit):
    o = o.rstrip('\u00b0') if unit == '°' else o
    return tex(o)


def check_bank(fails, bank):
    counts = {lv: len(bank.get(lv, [])) for lv in COUNTS}
    if counts != COUNTS:
        fails.append('bank: %s items by level, expected %s (a change needs TARGETS reviewed)' % (counts, COUNTS))
        return
    for lv in COUNTS:
        for i, q in enumerate(bank[lv]):
            w = '%s[%d] (%s | %s)%s' % (lv, i, q['ctx'] or q['q'], q['ask'],
                                       ' (trig-identity-duel-%s)' % AUDIT[(lv, i)] if (lv, i) in AUDIT else '')
            t = TARGETS[lv][i]
            if (lv, i) in CONTEXT and CONTEXT[(lv, i)] not in q['ctx']:
                fails.append('%s: the context must state "%s"' % (w, CONTEXT[(lv, i)]))
            opts = [q['correct']] + q['d']
            if t[0] == 'verdict':
                if q['correct'] != t[1]:
                    fails.append('%s: keyed %s, reviewed %s (%s)' % (w, q['correct'], t[1], t[2]))
                continue
            unit = t[3] if t[0] == 'num' else ''
            try:
                vals = [opt_value(o, unit) for o in opts]
            except ValueError as e:
                fails.append('%s: %s (extend tex())' % (w, e))
                continue
            if t[0] == 'count':
                target, dp = sp.Integer(t[1]), None
            elif t[0] == 'num':
                target, dp = t[1], t[2]
            elif t[0] == 'value':
                target, dp = tex(q['q']), None
            elif t[0] == 'ident':
                target, dp = (t[1] if len(t) > 1 else tex(q['q'])), None
            target = sp.sympify(target) if t[0] != 'notequiv' else None
            if t[0] == 'notequiv':
                base = tex(q['q'])
                bad = [o for o, v in zip(opts, vals) if not same(v, base)]
                if bad != [q['correct']]:
                    fails.append('%s: the options not equivalent to %s are %s; the key is %s' % (w, q['q'], bad, q['correct']))
                continue
            if dp is not None:
                if 'd.p.' not in q['ask']:
                    fails.append('%s: the answer is not exact and the ask states no precision (SR-1)' % w)
                key_ok = Decimal(str(sp.N(vals[0], 30))) == Decimal(str(sp.N(target, 40))).quantize(
                    Decimal(1).scaleb(-dp), rounding=ROUND_HALF_UP) and len(opts[0].rstrip('°').split('.')[-1]) == dp
                hits = [o for o, v in zip(opts[1:], vals[1:])
                        if Decimal(str(sp.N(v, 30))).quantize(Decimal(1).scaleb(-dp), rounding=ROUND_HALF_UP)
                        == Decimal(str(sp.N(target, 40))).quantize(Decimal(1).scaleb(-dp), rounding=ROUND_HALF_UP)]
            else:
                if not target.free_symbols and not sp.nsimplify(target).is_Rational and 'exact' not in q['ask'].lower() \
                        and t[0] in ('num',) and not re.search(r'\\sqrt|\\pi', q['correct']):
                    fails.append('%s: the answer is not exact and the ask states no precision (SR-1)' % w)
                key_ok = same(vals[0], target)
                hits = [o for o, v in zip(opts[1:], vals[1:]) if same(v, target)]
            if not key_ok:
                fails.append('%s: keyed %s, the answer is %s' % (w, q['correct'], sp.N(target, 6) if not target.free_symbols else target))
            for h in hits:
                fails.append('%s: the wrong option %s is also right (SR-16)' % (w, h))
            for a in range(len(vals)):
                for b in range(a + 1, len(vals)):
                    if same(vals[a], vals[b]):
                        fails.append('%s: options %s and %s are equal in value' % (w, opts[a], opts[b]))


SWEEP_JS = r"""() => {
  window.setTimeout = () => 0; window.setInterval = () => 0;
  if (window.MaffsLock) MaffsLock.FRESH_MS = 0;
  const out = [];
  for (const lv of ['gcse', 'alevel']) QUESTIONS[lv].forEach((q, i) => {
    for (const pick of [q.correct, ...q.d]) {
      questions = [q]; qIdx = 0; totalQ = 1; level = lv; score = 0; correctCount = 0; streak = 0;
      const pr = document.getElementById('progress'); pr.innerHTML = '<div class="pip current"></div>';
      showQ();
      const b = [...document.querySelectorAll('#options .opt-btn')].find(x => x.dataset.val === pick);
      if (!b) { out.push([lv, i, pick, 'not on screen']); continue; }
      b.click();
      const right = b.classList.contains('correct');
      if (right !== (pick === q.correct)) out.push([lv, i, pick, right ? 'marked right' : 'marked wrong']);
    }
  });
  return out;
}"""


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base) and '/katex@' not in url, lambda route: route.abort())
            if KATEX_DIR:
                ctx.route(lambda url: '/katex@0.16.9/dist/' in url, lambda route: route.fulfill(
                    path=os.path.join(KATEX_DIR, route.request.url.split('/dist/', 1)[1].split('?')[0])))
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof katex !== "undefined"', timeout=15000)
            bank = page.evaluate('() => QUESTIONS')
            tm = page.evaluate(TIMER_JS)
            if tm['clock']:
                fails.append('a clock shows during play (trig-identity-duel-t2-010; timer-policy: hidden count-up)')
            if tm['score'] != 100:
                fails.append('a key clicked after 60 s scores %d, not 100: time feeds the score (trig-identity-duel-t2-010)'
                             % tm['score'])
            if 'Time' not in tm['stats']:
                fails.append('the results do not show the time (%r; trig-identity-duel-t2-010)' % tm['stats'])
            if tm['correct'] != 1:
                fails.append('the key clicked, then Enter three times on it, counted %d times (trig-identity-duel-t2-007)'
                             % tm['correct'])
            if tm['submits'] != 1:
                fails.append('the results screen submitted %d scores (MaffsLock.finishOnce)' % tm['submits'])
            page.reload(wait_until='load')
            page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof katex !== "undefined"', timeout=15000)
            for lv, i, pick, what in page.evaluate(SWEEP_JS):
                fails.append('%s[%d] in Chromium: option %s %s' % (lv, i, pick, what))
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            return bank
    finally:
        proc.terminate()
        proc.wait()


# A hidden count-up with no marks for speed (timer-policy.md, canon SR-23; trig-identity-duel-t2-010): a key clicked a
# minute after the question appears scores 100, no clock shows during play, and the results show the time. Answer
# once (MaffsLock; t2-007): the key clicked, then Enter three times on it, counts once; the results submit once.
TIMER_JS = r"""async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  let submits = 0;
  window.MaffsLeaderboard = { submitScore: () => { submits++; return Promise.resolve(); } };
  const q = QUESTIONS.gcse[16];
  startGame();
  questions = [q, q]; qIdx = 0; totalQ = 2; score = 0; correctCount = 0;
  showQ();
  const clock = [...document.querySelectorAll('#game .hud-label')].map(e => e.textContent).filter(t => /time/i.test(t)).length;
  await wait((window.MaffsLock ? MaffsLock.FRESH_MS : 0) + 50);
  const realNow = Date.now; Date.now = () => realNow() + 60000;
  const key = [...document.querySelectorAll('#options .opt-btn')].find(b => b.dataset.val === q.correct);
  key.click(); key.focus();
  for (let k = 0; k < 3; k++) { key.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true })); key.click(); }
  const res = { clock, score, correct: correctCount };
  Date.now = realNow;
  if (window.MaffsLock) MaffsLock.clearTimers();
  end(); end();
  res.submits = submits;
  res.stats = document.getElementById('statsLine').textContent;
  return res;
}"""

KATEX_DIR = None


def u(s):
    return ''.join('\\u%04x' % ord(c) if ord(c) > 126 else c for c in s)


PLANTS = [
    ('gcse[28]', 't2-001: the largest angle keyed 86.2°', u("correct:'85.9°'"), u("correct:'86.2°'")),
    ('alevel[31]', 't2-002: sin(A+B) keyed 56/65',
     "ask:'Find sin(A+B)',correct:'\\\\dfrac{63}{65}'", "ask:'Find sin(A+B)',correct:'\\\\dfrac{56}{65}'"),
    ('alevel[47]', 't2-005: the identical option 1 + 2 sin x cos x',
     "'1 + \\\\cos 2x']", "'1 + 2\\\\sin x\\\\cos x']"),
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
    if bank is not None:
        check_bank(fails, bank)
    print('%s: %d items, every option evaluated (SymPy) and clicked in Chromium' % (SLUG, sum(len(bank[k]) for k in COUNTS) if bank else 0))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-48s *** CANNOT PLANT (%d) ***' % (what, html.count(old)))
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(old, new))
            if planted is not None:
                check_bank(rep, planted)
            hit = [f for f in rep if f.startswith(tag)]
            ok = ok and bool(hit)
            print('  self-test %-48s %s' % (what, ('caught: ' + hit[0][:110]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
