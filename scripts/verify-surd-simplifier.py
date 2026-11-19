#!/usr/bin/env python3
# ci-line: Surd Simplifier (every key recomputed from its stem with SymPy, in simplest form; every option marked in Chromium) |
"""Surd Simplifier: every key recomputed exactly from the expression the student is shown; every option clicked.

The game (100 multiple-choice items: gcse 50, alevel 50) asks the student to simplify a surd, rationalise a
denominator, expand surd brackets or turn a recurring decimal into a fraction. Each item's stem IS the
expression, so its answer needs no table: the stem is read as TeX (recurring decimals by their dots) and
compared with the key exactly in SymPy. The bank was keyed by hand with no verifier; the tranche 1 audit of
6 Oct 2026 found two wrong keys (contract LISTED-HIGH, 9 Oct 2026):
  surd-simplifier-t1-001  gcse[33] 8/sqrt(32), "Rationalise and simplify", keyed sqrt(2).sqrt(2) = 2; it is sqrt(2).
  surd-simplifier-t1-002  alevel[35] 0.4(16 recurring), keyed 137/330 = 0.41515...; it is 412/990 = 206/495.

Every item, both levels:
  the key equals the stem in value (symbols a and x are positive: sqrt(x^4) = x^2);
  the key is in simplest form (the form every ask names): each surd's radicand square-free, no surd in a
  denominator, a fraction in lowest terms with a denominator above 1, no unexpanded product or unevaluated sum;
  a wrong option equal in value to the key is allowed only when it is not in simplest form, so the ask tells
  them apart (SR-4); every other wrong option differs from the key in value (SR-16);
  no two wrong options are equal in value unless the pair is listed as a form question in
  checker-allowlist.json (SR-4; B11-CLEAR, 12 Oct 2026);
  four distinct option strings; and, in Chromium (390x844), every item shown through showQ() and every option
  clicked through handle(): the key marked right, the others wrong.
The worked solution shown on a wrong answer (contract SURD-WORKING, 19 Nov 2026), read from the page's own
workingFor(), templates and data alike, every item at both levels:
  every line read in SymPy: each top-level \\text{...} is words, the maths between is checked; in each maths run,
  every "="-separated part is equal (a part with a decimal within 10^-6, the 6th place; a line opening with "="
  continues the line before); in a recurring-decimal item x is the key, elsewhere a, b and x are positive symbols;
  the last part of the last line equals the key;
  a square-factor template's first line names the biggest square factor of n (recomputed here), and its last part
  is the key as written; the templates cover exactly the items the contract lists, and every data key names an item;
  in Chromium, a wrong answer shows that item's lines, rendered, in the "How to get there" box before Next, and a
  right answer shows no box.
A self-test plants each audit fault back into a copy of the page; each must FAIL naming its item.

    python scripts/verify-surd-simplifier.py [--no-selftest] [--against FILE] [--katex-dir DIR]
"""
import argparse
import json
import os
import re
import sys
from math import gcd

import sympy as sp
from sympy.parsing.sympy_parser import (implicit_multiplication_application, parse_expr,
                                        standard_transformations)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'surd-simplifier'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNTS = {'gcse': 50, 'alevel': 50}
SYMS = {'a': sp.Symbol('a', positive=True), 'x': sp.Symbol('x', positive=True)}
WSYMS = dict(SYMS, b=sp.Symbol('b', positive=True))
TRANSFORMS = standard_transformations + (implicit_multiplication_application,)
AUDIT = {('gcse', 33): 'surd-simplifier-t1-001', ('alevel', 35): 'surd-simplifier-t1-002'}


def group(s, i):
    """The text inside the brace group opening at s[i], and the index after it."""
    d = 0
    for j in range(i, len(s)):
        d += (s[j] == '{') - (s[j] == '}')
        if d == 0:
            return s[i + 1:j], j + 1
    raise ValueError('unbalanced braces in %r' % s)


def recurring(s):
    """'0.4\\dot{1}\\dot{6}' -> Rational; None when s is not a recurring decimal."""
    m = re.fullmatch(r'0\.((?:\d|\\dot\{\d\})+)', s)
    if not m or '\\dot' not in s:
        return None
    digits, dotted = [], []
    for d, dd in re.findall(r'\\dot\{(\d)\}|(\d)', m.group(1)):
        digits.append(d or dd)
        dotted.append(bool(d))
    first = dotted.index(True)
    last = len(dotted) - 1 - dotted[::-1].index(True)
    if last != len(digits) - 1:
        raise ValueError('digits after the recurring block in %r' % s)
    pre, rep = ''.join(digits[:first]), ''.join(digits[first:])
    return sp.Rational(int(pre + rep) - int(pre or '0'), 10 ** len(pre) * (10 ** len(rep) - 1))


def to_py(s):
    """TeX -> a SymPy-parsable string."""
    out, i = '', 0
    while i < len(s):
        m = re.match(r'\\[dt]?frac\{', s[i:])
        if m:
            p, j = group(s, i + m.end() - 1)
            q, k = group(s, j)
            out, i = out + '((%s)/(%s))' % (to_py(p), to_py(q)), k
            continue
        if s.startswith('\\sqrt{', i):
            p, j = group(s, i + 5)
            out, i = out + ' sqrt(%s)' % to_py(p), j
            continue
        m = re.match(r'\\(times|cdot)', s[i:])
        if m:
            out, i = out + '*', i + m.end()
            continue
        if s[i] == '\\':
            raise ValueError('unknown TeX in %r' % s)
        if s[i] == '^':
            if s.startswith('^{', i):
                p, j = group(s, i + 1)
                out, i = out + '**(%s)' % to_py(p), j
            else:
                out, i = out + '**' + s[i + 1], i + 2
            continue
        out, i = out + {'{': '(', '}': ')'}.get(s[i], s[i]), i + 1
    return out


def value(s):
    """The exact value of a stem or an option; ValueError when it cannot be read."""
    s = s.strip()
    r = recurring(s)
    if r is not None:
        return r
    try:
        return parse_expr(to_py(s), local_dict=dict(SYMS, sqrt=sp.sqrt), transformations=TRANSFORMS)
    except Exception as e:
        raise ValueError('cannot read %r: %s' % (s, e))


def raw(s):
    """The expression as written: nothing evaluated, so sqrt(2)*sqrt(2) and 5+2 keep their shape."""
    with sp.evaluate(False):
        return parse_expr(to_py(s.strip()), local_dict=dict(SYMS, sqrt=sp.sqrt), transformations=TRANSFORMS,
                          evaluate=False)


def unsimplified(s):
    """Why the TeX s is not in simplest form, or '' when it is. Read from the written shape, not the value."""
    t = s.strip()
    if '\\cdot' in t or '\\times' in t:
        return 'an unevaluated product'
    for m in re.finditer(r'\\sqrt\{', t):
        rad, _ = group(t, m.end() - 1)
        try:
            v = value(rad)
        except ValueError:
            continue
        if v.is_Integer:
            n = int(v)
            if n < 2 or any(n % (k * k) == 0 for k in range(2, int(n ** 0.5) + 1)):
                return 'sqrt(%d) has a square factor' % n
        elif v.is_Pow and v.exp.is_Integer and v.exp >= 2:
            return 'sqrt(%s) has a square factor' % v
    if t.startswith('\\dfrac{'):
        num, j = group(t, 6)
        den, k = group(t, j)
        if k == len(t):
            if '\\sqrt' in den:
                return 'a surd in the denominator'
            dv = value(den)
            if not dv.is_Integer:
                return 'a denominator that is not a whole number'
            if dv == 1:
                return 'a denominator of 1'
            nv = sp.expand(value(num))
            coeffs = [c for c, _ in (term.as_coeff_Mul() for term in sp.Add.make_args(nv))]
            if not all(c.is_Integer for c in coeffs):
                return 'a numerator that is not whole'
            g = 0
            for c in coeffs:
                g = gcd(g, int(c))
            if gcd(g, int(dv)) > 1:
                return 'numerator and denominator share the factor %d' % gcd(g, int(dv))
            if '\\dfrac' in num or '\\dfrac' in den:
                return 'a fraction inside a fraction'
            return unsimplified_terms(num, bracket_ok=True)   # 3(sqrt(5)+1)/4: a factor kept over the denominator
    if '\\dfrac' in t:
        return 'a fraction not written as one fraction'
    return unsimplified_terms(t)


def unsimplified_terms(t, bracket_ok=False):
    """A sum or product written out: integer arithmetic left undone, like surds not collected, a bracket left."""
    if not bracket_ok and re.search(r'\d\s*\(|\)\s*\(', t):
        return 'a bracket left unexpanded'
    e = raw(t)
    terms = sp.Add.make_args(e)
    if len(terms) > 1:
        rational = [x for x in terms if sp.sympify(x).doit().is_Rational]
        if len(rational) > 1:
            return 'whole numbers left unadded'
        surds = [sp.sympify(x).doit().as_coeff_Mul()[1] for x in terms if not sp.sympify(x).doit().is_Rational]
        if len(surds) != len(set(surds)):
            return 'like surds not collected'
    return ''


def item_name(lv, i, q):
    return '%s[%d] (%s | %s)%s' % (lv, i, q['q'], q['ask'], ' (%s)' % AUDIT[(lv, i)] if (lv, i) in AUDIT else '')


def listed_pairs():
    """Pairs of wrong options equal in value that checker-allowlist.json lists as form questions for this game (the
    ask names the form: both are the key's value unsimplified, or one wrong value written two ways), as
    (level, index, frozenset(pair))."""
    path = os.path.join(HERE, 'checker-allowlist.json')
    out = set()
    for e in json.load(open(path, encoding='utf-8'))['b11_form_questions']:
        m = re.fullmatch(r'surd-simplifier QUESTIONS\.(\w+)\[(\d+)\]', e['where'])
        if m:
            out.add((m.group(1), int(m.group(2)), frozenset(e['pair'])))
    return out


def check_bank(fails, bank):
    listed = listed_pairs()
    counts = {lv: len(bank.get(lv, [])) for lv in COUNTS}
    if counts != COUNTS:
        fails.append('bank: %s items by level, expected %s' % (counts, COUNTS))
    for lv in COUNTS:
        for i, q in enumerate(bank.get(lv, [])):
            w = item_name(lv, i, q)
            opts = [q['correct']] + list(q['d'])
            if len(opts) != 4 or len(set(opts)) != 4:
                fails.append('%s: the options %s are not four distinct strings' % (w, opts))
            try:
                target = sp.simplify(value(q['q']))
                vals = [sp.simplify(value(o)) for o in opts]
            except ValueError as e:
                fails.append('%s: %s (extend value())' % (w, e))
                continue
            if sp.simplify(vals[0] - target) != 0:
                fails.append('%s: keyed %s = %s, the answer is %s' % (w, q['correct'], vals[0], target))
            why = unsimplified(q['correct'])
            if why:
                fails.append('%s: the key %s is not in simplest form (%s)' % (w, q['correct'], why))
            for o, v in zip(opts[1:], vals[1:]):
                if sp.simplify(v - target) == 0 and not unsimplified(o):
                    fails.append('%s: the wrong option %s equals the answer and is in simplest form (SR-16)'
                                 % (w, o))
            # SR-4 (B11-CLEAR, 12 Oct 2026): two wrong options equal in value leave the student three choices, unless
            # the pair is a listed form question (checker-allowlist.json b11_form_questions).
            for x in range(1, 4):
                for y in range(x + 1, 4):
                    if sp.simplify(vals[x] - vals[y]) == 0 and (lv, i, frozenset((opts[x], opts[y]))) not in listed:
                        fails.append('%s: the wrong options %s and %s are equal in value and not a listed form '
                                     'question (SR-4)' % (w, opts[x], opts[y]))


# Which template each item's working comes from when it has no data entry (contract SURD-WORKING, 3(a)), 1-based.
TEMPLATE_ITEMS = {
    'surd': {'gcse': set(range(1, 17)), 'alevel': {1, 2, 3}},
    'recurring': {'gcse': set(range(36, 51)), 'alevel': set(range(31, 41)) - {39}},
}
SURD_STEM = re.compile(r'(\d+)?\\sqrt\{(\d+)\}')
SQ_LINE = re.compile(r'\\text\{Biggest square factor of \} (\d+) \\text\{ is \} (\d+)')


def math_runs(line):
    """The maths of one working line: the runs between its top-level \\text{...} groups."""
    runs, cur, i = [], '', 0
    while i < len(line):
        if line.startswith('\\text{', i):
            _, i = group(line, i + 5)
            runs.append(cur)
            cur = ''
            continue
        cur += line[i]
        i += 1
    runs.append(cur)
    return [r for r in (x.replace('\\ldots', '').replace('\\;', ' ').replace('\\,', ' ').strip() for x in runs) if r]


def wvalue(tex, x):
    """A part of a working line, exactly: decimals as fractions; x is the key in a recurring item."""
    tex = re.sub(r'(\d+)\.(\d+)', lambda m: '\\dfrac{%d}{%d}' % (int(m.group(1) + m.group(2)), 10 ** len(m.group(2))), tex)
    loc = dict(WSYMS, sqrt=sp.sqrt)
    if x is not None:
        loc['x'] = x
    try:
        return parse_expr(to_py(tex), local_dict=loc, transformations=TRANSFORMS)
    except Exception as e:
        raise ValueError('cannot read %r: %s' % (tex, e))


def biggest_square(n):
    return max(k * k for k in range(1, int(n ** 0.5) + 1) if n % (k * k) == 0)


def check_working(fails, bank, work, data_keys):
    """Contract SURD-WORKING item 5: every line's parts equal, the last part the key; templates as listed."""
    for k in data_keys:
        m = re.fullmatch(r'(gcse|alevel)-(\d+)', k)
        if not m or not 1 <= int(m.group(2)) <= len(bank.get(m.group(1), [])):
            fails.append('working: the data key %r names no item' % k)
    for lv in COUNTS:
        for i, q in enumerate(bank.get(lv, [])):
            w = item_name(lv, i, q)
            lines = (work.get(lv) or [])[i] if i < len(work.get(lv) or []) else []
            if not lines:
                fails.append('%s: no working' % w)
                continue
            n1 = i + 1
            data = '%s-%d' % (lv, n1) in data_keys
            if not data:
                kind = [t for t, by in TEMPLATE_ITEMS.items() if n1 in by[lv]]
                if not kind:
                    fails.append('%s: working from a template, but the contract lists no template for it' % w)
            elif any(n1 in by[lv] for by in TEMPLATE_ITEMS.values()) and (lv, n1) != ('alevel', 39):
                fails.append('%s: a data entry overrides its template; the contract lists only alevel-39' % w)
            r = recurring(q['q'].strip())
            x = r if r is not None else None
            prev, last = None, None
            try:
                for li, line in enumerate(lines):
                    for ri, run in enumerate(math_runs(line)):
                        parts = [t.strip() for t in run.split('=')]
                        if ri == 0 and parts[0] == '' and prev is not None:
                            parts[0] = prev
                        elif parts[0] == '':
                            raise ValueError('line %d opens with "=" and nothing before it' % (li + 1))
                        vals = [wvalue(t, x) for t in parts]
                        for a in range(1, len(parts)):
                            dec = bool(re.search(r'\d\.\d', parts[a - 1] + parts[a]))
                            d = sp.simplify(vals[a - 1] - vals[a])
                            ok = (d.is_number and abs(d) <= sp.Rational(1, 10 ** 6)) if dec else d == 0
                            if not ok:
                                fails.append('%s: working line %d: %s = %s is false (%s)'
                                             % (w, li + 1, parts[a - 1], parts[a], lines[li]))
                        prev = parts[-1]
                        last = vals[-1]
                if last is None or sp.simplify(last - value(q['correct'])) != 0:
                    fails.append('%s: the working ends on %s, the key is %s' % (w, prev, q['correct']))
            except ValueError as e:
                fails.append('%s: working: %s (extend wvalue())' % (w, e))
                continue
            m = SURD_STEM.fullmatch(q['q'].strip())
            if not data and m and n1 in TEMPLATE_ITEMS['surd'][lv]:
                n = int(m.group(2))
                s1 = SQ_LINE.fullmatch(lines[0])
                if not s1 or int(s1.group(1)) != n:
                    fails.append('%s: the square-factor template does not open by naming the factor of %d' % (w, n))
                elif int(s1.group(2)) != biggest_square(n):
                    fails.append('%s: the working names %s as the biggest square factor of %d; it is %d'
                                 % (w, s1.group(2), n, biggest_square(n)))
                if prev != q['correct']:
                    fails.append('%s: the square-factor template ends on %s, not the key as written %s'
                                 % (w, prev, q['correct']))


WORK_JS = r"""() => ({keys: Object.keys(WORKING),
  work: Object.fromEntries(['gcse', 'alevel'].map(lv => [lv, QUESTIONS[lv].map((q, i) => workingFor(lv, i))]))})"""


SWEEP_JS = r"""() => {
  window.setTimeout = () => 0; window.setInterval = () => 0;
  const out = [];
  for (const lv of ['gcse', 'alevel']) QUESTIONS[lv].forEach((q, i) => {
    for (const pick of [q.correct, ...q.d]) {
      questions = [q]; qIdx = 0; totalQ = 1; level = lv; score = 0; correctCount = 0; streak = 0;
      document.getElementById('progress').innerHTML = '<div class="pip current"></div>';
      showQ();
      const shown = [...document.querySelectorAll('#options .opt-btn')];
      if (shown.length !== 4) out.push([lv, i, pick, shown.length + ' options on screen']);
      const btn = shown.find(x => x.dataset.val === pick);
      if (!btn) { out.push([lv, i, pick, 'not on screen']); continue; }
      btn.click();
      const right = btn.classList.contains('correct');
      if (right !== (pick === q.correct)) out.push([lv, i, pick, right ? 'marked right' : 'marked wrong']);
      // SURD-WORKING: a wrong answer shows the item's working before Next; a right one shows none.
      const box = document.getElementById('working');
      const boxShown = box && !box.hidden && getComputedStyle(box).display !== 'none';   // the sweep never shows #game, so no offsetHeight
      const want = workingFor(lv, i).length;
      const got = boxShown ? box.querySelectorAll('.wl').length : 0;
      const next = document.querySelector('#nextMount .maffs-next');
      if (pick !== q.correct) {
        if (!boxShown || got !== want || !want)
          out.push([lv, i, pick, 'answered wrong: the working box shows ' + got + ' of ' + want + ' lines']);
        else if (box.querySelector('.katex-error') || [...box.querySelectorAll('.wl')].some(l => !l.textContent.trim()))
          out.push([lv, i, pick, 'answered wrong: a working line does not render']);
        else if (!box.querySelector('h3') || box.querySelector('h3').textContent !== 'How to get there')
          out.push([lv, i, pick, 'answered wrong: the working box is not titled "How to get there"']);
        if (!next) out.push([lv, i, pick, 'answered wrong: no Next']);
      } else if (boxShown) out.push([lv, i, pick, 'answered right: the working box is shown']);
    }
  });
  return out;
}"""
KATEX_DIR = None
WORK_SEEN = [None, None]   # the last page's (working by level, WORKING's keys), set by play()


def text_fails(html):
    """SWEEP-1 rulings (13 Oct 2026): R7, the timer policy lists this game under Hidden Count-Up, so the HUD shows no running Time."""
    out = []
    if re.search(r'class="hud-label">Time<', html) or 'id="timer"' in html:
        out.append('hud: the running Time is on the HUD; Hidden Count-Up means it is never shown (R7, surd-simplifier-s1-003)')
    return out


def play(fails, html):
    fails.extend(text_fails(html))
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)   # MaffsLock's 300 ms window: the sweep answers at once
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            bc.offline(ctx, base)
            if KATEX_DIR:
                ctx.route(lambda url: '/katex@0.16.9/dist/' in url, lambda route: route.fulfill(
                    path=os.path.join(KATEX_DIR, route.request.url.split('/dist/', 1)[1].split('?')[0])))
            else:
                ctx.route(lambda url: bc.is_font_cdn(url), bc.serve_real_font)     # KaTeX from the pinned local copy
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof katex !== "undefined"', timeout=15000)
            bank = page.evaluate('() => QUESTIONS')
            got = page.evaluate(WORK_JS)
            WORK_SEEN[:] = [got['work'], set(got['keys'])]
            for lv, i, pick, what in page.evaluate(SWEEP_JS):
                fails.append('%s in Chromium: option %s %s' % (item_name(lv, i, bank[lv][i]), pick, what))
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            return bank
    finally:
        proc.terminate()
        proc.wait()


# (the item the failure must name, what is planted, today's text, main's text before LISTED-HIGH).
PLANTS = [
    ('hud:', 's1-003: the HUD Time back', '<div class="hud-item"><div class="hud-label">Streak</div>',
     '<div class="hud-item"><div class="hud-label">Time</div><div class="hud-val" id="timer">0s</div></div><div class="hud-item"><div class="hud-label">Streak</div>'),
    ('gcse[33]', 't1-001: 8/sqrt(32) keyed sqrt(2).sqrt(2)',
     "correct:'\\\\sqrt{2}',d:['2\\\\sqrt{2}','4','\\\\sqrt{2} \\\\cdot \\\\sqrt{2}']",
     "correct:'\\\\sqrt{2} \\\\cdot \\\\sqrt{2}',d:['2\\\\sqrt{2}','4','\\\\dfrac{8\\\\sqrt{32}}{32}']"),
    ('alevel[35]', 't1-002: 0.4(16) keyed 137/330',
     "correct:'\\\\dfrac{206}{495}'", "correct:'\\\\dfrac{137}{330}'"),
    ('gcse[38]', 'SR-4: two wrong options equal in value (1/5 and 2/10), not listed',
     "d:['\\\\dfrac{2}{99}','\\\\dfrac{2}{10}','\\\\dfrac{1}{4}']", "d:['\\\\dfrac{1}{5}','\\\\dfrac{2}{10}','\\\\dfrac{1}{4}']"),
    ('gcse[36]', 'a key not in lowest terms (6/9 for 0.(6))',
     "correct:'\\\\dfrac{2}{3}',d:['\\\\dfrac{6}{10}','\\\\dfrac{2}{9}','\\\\dfrac{6}{9}']}",
     "correct:'\\\\dfrac{6}{9}',d:['\\\\dfrac{6}{10}','\\\\dfrac{2}{9}','\\\\dfrac{2}{3}']}"),
    ('start screen', 's1-001: "nested surds" listed, none in the bank',
     "expand surd brackets\n", "expand surd brackets, nested surds\n"),
    # SURD-WORKING (19 Nov 2026): a false line, a wrong biggest square factor, and no box on a wrong answer.
    ('gcse[0]', 'working: sqrt(4) x sqrt(5) in gcse item 1',
     "'}\\\\times\\\\sqrt{'+b+'}',", "'}\\\\times\\\\sqrt{'+(n===12&&!k?5:b)+'}',", 'is false'),
    ('gcse[4]', 'working: a square factor, not the biggest',
     "if(n%(j*j)===0)a=j;", "if(n%(j*j)===0&&a===1)a=j;", 'biggest square factor'),
    ('gcse[0]', 'working: no box on a wrong answer',
     "else{showWorking(q);MaffsNext.wrong(", "else{MaffsNext.wrong(", 'working box shows 0'),
]


def start_screen_fails(html, bank):
    """The start screen says what the bank holds (SWEEP-1, surd-simplifier-s1-001): it names nested surds only when an
    A-Level item has a root inside a root."""
    if bank is None or 'nested surd' not in html:
        return []
    nested = [q for q in bank.get('alevel', []) if re.search(r'\\sqrt\{[^{}]*\\sqrt', q.get('q', ''))]
    return [] if nested else ['start screen: it lists "nested surds" but no A-Level item has a root inside a root']


def selftest_shapes():
    """The form reader on the shapes the bank uses; a wrong verdict here fails before any page is read."""
    simplest = ['\\sqrt{2}', '2\\sqrt{3}', '\\dfrac{\\sqrt{3}}{3}', '\\dfrac{3(\\sqrt{5}+1)}{4}', '8-4\\sqrt{3}',
                '\\dfrac{7+2\\sqrt{10}}{3}', '\\dfrac{206}{495}', 'x^2', 'a', '-2', '7+4\\sqrt{3}', '1']
    not_simplest = ['\\sqrt{2} \\cdot \\sqrt{2}', '\\dfrac{8\\sqrt{32}}{32}', '\\dfrac{4+2\\sqrt{3}}{2}',
                    '\\dfrac{\\sqrt{2}-1}{1}', '4(2-\\sqrt{3})', '5+2', '2\\sqrt{3}+3\\sqrt{3}', '\\sqrt{16}',
                    '\\dfrac{1}{\\sqrt{3}}', '\\dfrac{3}{9}', '\\sqrt{a^2}', '3\\sqrt{4}-\\sqrt{16}', '\\dfrac{9}{9}']
    bad = [s for s in simplest if unsimplified(s)] + [s for s in not_simplest if not unsimplified(s)]
    if recurring('0.4\\dot{1}\\dot{6}') != sp.Rational(206, 495) or recurring('0.08\\dot{3}') != sp.Rational(1, 12):
        bad.append('recurring()')
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    ap.add_argument('--katex-dir', help='serve KaTeX from this local dist/ folder')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    global KATEX_DIR
    KATEX_DIR = args.katex_dir
    fails = ['form reader misjudges %s' % s for s in selftest_shapes()]
    html = open(args.against or GAME, encoding='utf-8').read()
    bank = play(fails, html)
    if bank is not None:
        check_bank(fails, bank)
        check_working(fails, bank, *WORK_SEEN)
    fails += start_screen_fails(html, bank)
    print('%s: %d items, every key recomputed from its stem, every option read and clicked in Chromium'
          % (SLUG, sum(len(bank.get(k, [])) for k in COUNTS) if bank else 0))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, new, old, *need in PLANTS:
            need = need[0] if need else ''
            if html.count(new) != 1:
                print('  self-test %-46s *** CANNOT PLANT (%d) ***' % (what, html.count(new)))
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(new, old))
            if planted is not None:
                check_bank(rep, planted)
                check_working(rep, planted, *WORK_SEEN)
            rep += start_screen_fails(html.replace(new, old), planted)
            hit = [f for f in rep if f.startswith(tag) and need in f]
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
