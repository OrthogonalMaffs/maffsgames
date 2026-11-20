#!/usr/bin/env python3
# ci-line: Standard Form Blitz (all 100 keys recomputed exactly from the question's own TeX; every option classified; every option pressed in Chromium) |
"""Standard Form Blitz: multiple choice on standard form, 50 GCSE and 50 A-Level items, 20 a session, four options each.

Static bank, read from the page as served: `QUESTIONS.gcse` and `QUESTIONS.alevel`, each item `{q, ask, correct, d}` where `q`
and every option are TeX (or plain text) and the three `d` are the distractors. The mark is `button.dataset.val === q.correct`.

Checks, independent of the game's code (the TeX of each question is read here into a SymPy expression with exact rationals;
nothing is floated except to print):
  Value: `q` is worked out exactly (conversions, products and quotients, powers, roots, sums and differences, fractions) or,
    for the context problems, from the numbers in its own text with the operation the question asks for; a comparison
    (largest, smallest, middle, larger, bigger, which two are equal) is decided from the values listed; a "Find n" / "Find a"
    equation is tried with each option.
  Key: it equals that value at the precision the question states ("to 3 s.f.", "to 1 s.f.", "nearest £", "(3 s.f.)", an
    approximation to a whole number) and, where the question says standard form, it is in standard form: 1 <= a < 10, with
    exactly the stated number of significant figures.
  Options: exactly four, all different strings; exactly one is right (equal to the value, and in standard form where that is
    asked: a distractor that is numerically equal but not in standard form, like 45 x 10^3, is legitimately wrong; where the
    question does not ask for standard form, ANY option equal to the key in value fails the item, SR-4/SR-16); no two
    options are equal in value (SR-4; B11-CLEAR, 12 Oct 2026, none expected) except, where standard form is asked,
    options equal to the key's value in other forms (they test the form); a
    comparison's "All equal", "They are equal", "Cannot tell" and "None are equal" are false claims, and each pair claimed
    equal is tested.
  Render: every question and option is parsed by KaTeX (throwOnError) from the pinned local copy, and the rendered TeX
    annotation of each displayed question and option is the source.
  Sessions: startGame() at each level, dealt three times: 20 different questions, all from that level's bank.
  Marking, in Chromium (390x844), through the game's own buttons: every item is shown by showQ() and each of its four
    options pressed; the key is marked right (class correct, +100, streak 1), any other wrong (class wrong on the pressed
    button, class correct on the key, no score, streak 0, the Next control mounted).
  Working (contract SFB-WORKING-GCSE, 19 Nov 2026): the page's working(q), read for every item: each GCSE item has lines
    and each A-Level item none; every "=" chain outside \\text{} words is true, worked here exactly in SymPy; a "Write in
    standard form" item names the key's coefficient and the places moved, in the direction its power's sign says; for every
    kind but a comparison the last part of the last line is the key as written (braces aside), and a comparison ends
    "So <the key>". In Chromium every GCSE item answered with each wrong option shows its lines in the card "How to get
    there" (collapsed "Working"), before Next, both copies alike; a right answer, and any A-Level answer, shows no card.
  The card's place (WORKING-CARD's rule, run once, not in the self-test): at each size in LAYOUT_SIZES, normal and Aa, every
    GCSE item answered wrong in each of its three option pairings: with the open card, Next's bottom in page coordinates is
    within the fold (the viewport less the fixed footer); with the collapsed card, Next ends exactly where it ends with no
    card (the card costs no height, Jon's ruling of 19 Nov 2026).
No analytics or leaderboard request leaves the stub server (every other request is aborted).

    python scripts/verify-standard-form-blitz.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP, getcontext

import sympy
from sympy import Rational, sympify

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'standard-form-blitz'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
getcontext().prec = 80
SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁻', '0123456789-')
STD_ASKS = ('Write in standard form', 'Write in correct standard form', 'Calculate. Give your answer in standard form',
            'Estimate to 1 s.f., in standard form.')
COMPARE_ASKS = ('Which is largest?', 'Which is smallest?', 'Which is larger?', 'Which is in the middle?')
WORD_CLAIMS = re.compile(r'^(All equal|They are equal|Cannot tell|None|All three|undefined)', re.I)
NUM_RE = re.compile(r'(\d+(?:\.\d+)?) \\times 10\^\{?(-?\d+)\}?')


# ---- TeX to exact numbers -------------------------------------------------------------------------------------------
def group(s, i):
    """The {...} group starting at s[i]; returns (inside, index after)."""
    assert s[i] == '{'
    depth, j = 0, i
    while j < len(s):
        if s[j] == '{':
            depth += 1
        elif s[j] == '}':
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    raise ValueError('unbalanced braces in %r' % s)


def conv(s):
    out, i = '', 0
    while i < len(s):
        c = s[i]
        if s.startswith('\\dfrac', i):
            a, i = group(s, s.index('{', i))
            b, i = group(s, i)
            out += '((%s)/(%s))' % (conv(a), conv(b))
        elif s.startswith('\\sqrt', i):
            a, i = group(s, s.index('{', i))
            out += 'sqrt(%s)' % conv(a)
        elif s.startswith('\\times', i):
            out += '*'
            i += 6
        elif s.startswith('\\div', i):
            out += '/'
            i += 4
        elif c == '^':
            i += 1
            if s[i] == '{':
                a, i = group(s, i)
                out += '**(%s)' % conv(a)
            else:
                m = re.match(r'-?\d+|[a-z]', s[i:])
                out += '**(%s)' % m.group(0)
                i += len(m.group(0))
        elif c in '{} ':
            i += 1
        elif c == '\\':
            raise ValueError('unknown TeX command in %r' % s)
        else:
            out += c
            i += 1
    return re.sub(r'\)\s*\(', ')*(', out)


def tex_value(tex, **subs):
    return sympify(conv(tex), rational=True).subs(subs)


def opt_info(s):
    """(value as a sympy number or None, standard-form flag, significant figures written) of an option's string."""
    t = re.sub(r'\\text\{[^}]*\}', '', s).replace('£', '').replace('\\approx', '').strip()
    m = re.fullmatch(r'(-?[\d.]+)\s*\\times\s*10\^\{?(-?\d+)\}?', t)
    if m:
        a = Rational(m.group(1))
        return a * Rational(10) ** int(m.group(2)), 1 <= abs(a) < 10, sig_figs(m.group(1))
    m = re.fullmatch(r'10\^\{?(-?\d+)\}?', t)
    if m:
        return Rational(10) ** int(m.group(1)), True, 1
    if re.fullmatch(r'-?\d+(\.\d+)?', t):
        return Rational(t), False, sig_figs(t)
    return None, False, 0


def sig_figs(a):
    d = a.lstrip('-').replace('.', '').lstrip('0')
    return len(d)


def to_decimal(x):
    x = sympify(x)
    if x.is_Rational:
        return Decimal(int(x.p)) / Decimal(int(x.q))
    return Decimal(str(sympy.N(x, 70)))


def round_sf(x, n):
    d = to_decimal(x)
    if d == 0:
        return d
    return d.quantize(Decimal(1).scaleb(d.adjusted() - n + 1), rounding=ROUND_HALF_UP)


def round_int(x):
    return to_decimal(x).quantize(Decimal(1), rounding=ROUND_HALF_UP)


# ---- the context problems: the operation each asks for, on the numbers in its own text -------------------------------
def nums(q):
    return [Rational(a) * Rational(10) ** int(b) for a, b in NUM_RE.findall(q)]


CONTEXT = [
    ('\\text{Distance to Sun', lambda n, ask: n[0] / n[1], None),
    ('\\text{Mass of proton', lambda n, ask: 1 / n[0], ('sf', 3)),
    ('\\text{UK national debt', lambda n, ask: n[0] / n[1], ('int', 0)),
    ('\\text{Hair width', lambda n, ask: n[0] / n[1], None),
    ('\\text{Earth mass', lambda n, ask: n[0] / n[1], ('int', 0)),
    ('\\text{Bacteria', lambda n, ask: n[0] * n[1], None),
    ('\\text{Wavelength of red light', lambda n, ask: n[0] / Rational(10) ** int(re.search(r'10([⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)', ask).group(1).translate(SUP)), None),
    ('\\text{Observable universe', lambda n, ask: n[0] / 1000, None),
    ('\\text{A hard drive', lambda n, ask: n[0] / n[1], None),
]


def precision(ask):
    m = re.search(r'to (\d) s\.f\.|\((\d) s\.f\.\)', ask)
    if m:
        return ('sf', int(m.group(1) or m.group(2)))
    return None


def fits(optv, value, prec):
    if optv is None:
        return False
    if prec is None:
        return sympy.simplify(optv - value) == 0
    kind, n = prec
    return to_decimal(optv) == (round_sf(value, n) if kind == 'sf' else round_int(value))


# Distractors a sweep named (SR-4: from a nameable error): {(the ask, the distractor): the error}.
NAMED_ERRORS = {('Time for light to reach Earth (s)', '2 \\times 10^{-3}'): 'speed divided by distance, the inverse'}


def check_item(fails, where, q):
    key, d = q['correct'], q['d']
    opts = [key] + list(d)
    if len(d) != 3 or len(set(opts)) != 4:
        fails.append('options: %s: %d options, %d different strings' % (where, len(opts), len(set(opts))))
        return
    ask, tex = q['ask'], q['q']
    info = [opt_info(o) for o in opts]
    # SR-1 (SWEEP-1, standard-form-blitz-s1-001): an approximate key states the precision it is rounded to.
    if '\\approx' in key and not re.search(r'nearest|s\.f\.|d\.p\.|significant|decimal place', ask):
        fails.append('precision: %s: the key %r is approximate but the question states no precision (SR-1)' % (where, key))
    # SR-4 (SWEEP-1, standard-form-blitz-s1-002): each named error's distractor, where one option made two errors.
    for words, wrong in NAMED_ERRORS:
        if ask == words and wrong not in d:
            fails.append('options: %s: the distractor %r (%s) is missing (SR-4)' % (where, wrong, NAMED_ERRORS[(words, wrong)]))
    # SR-4 (B11-CLEAR, 12 Oct 2026): no two options equal in value, none expected. The one exception is a question that
    # asks for standard form, where options equal to the key's value in other forms test the form (45 x 10^3 and
    # 0.45 x 10^5 beside 4.5 x 10^4); two wrong values equal to each other are never allowed.
    need_std_form = any(ask.startswith(a) for a in STD_ASKS)
    for x in range(4):
        for y in range(x + 1, 4):
            vx, vy = info[x][0], info[y][0]
            if vx is None or vy is None or sympy.simplify(vx - vy) != 0:
                continue
            if need_std_form and info[0][0] is not None and sympy.simplify(vx - info[0][0]) == 0:
                continue
            fails.append('options: %s: the options %r and %r are equal in value (SR-4)' % (where, opts[x], opts[y]))
    # comparisons
    if ask in COMPARE_ASKS or tex.startswith('\\text{Which is bigger') or ask == 'Which two are equal?' or tex.startswith('\\text{Arrange'):
        body = re.sub(r'\\text\{[^}]*\}', ',', tex)
        pieces = [p for p in re.split(r'\\quad|,|\\;|\?', body) if p.strip()]
        listed = [opt_info(p.strip())[0] for p in pieces]
        if None in listed or len(listed) < 2:
            fails.append('key: %s: cannot read the listed numbers from %r' % (where, tex))
            return
        if ask == 'Which two are equal?':
            def truth(o):
                if o.startswith('None'):
                    return not any(listed[i] == listed[j] for i in range(len(listed)) for j in range(i + 1, len(listed)))
                if o.startswith('All'):
                    return all(v == listed[0] for v in listed)
                parts = [opt_info(p.strip())[0] for p in o.split('\\text{ and }')]
                if len(parts) != 2 or None in parts or parts[0] != parts[1]:
                    return False
                idx = [i for i, v in enumerate(listed) if v == parts[0]]
                return len(idx) >= 2
        else:
            ordered = sorted(listed)
            target = ordered[0] if ask == 'Which is smallest?' else ordered[len(ordered) // 2] if ask in ('Which is in the middle?',) else ordered[-1]

            def truth(o):
                v = opt_info(o)[0]
                if v is None:
                    return False          # "All equal", "They are equal", "Cannot tell": false for numbers that differ
                return v == target and v in listed
        right = [o for o in opts if truth(o)]
        if right != [key]:
            fails.append('options: %s: the true option(s) are %r, the key is %r' % (where, right, key))
        return
    # equations: try each option
    if ask in ('Find n', 'Find a'):
        lhs, rhs = tex.split(' = ')
        sym = 'n' if ask == 'Find n' else 'a'
        good = []
        for o in opts:
            v = opt_info(o)[0]
            if v is not None and sympy.simplify(tex_value(lhs, **{sym: v}) - tex_value(rhs, **{sym: v})) == 0:
                good.append(o)
        if good != [key]:
            fails.append('key: %s: the options that solve it are %r, the key is %r' % (where, good, key))
        return
    # value
    prec = precision(ask)
    ctx = next((c for c in CONTEXT if tex.startswith(c[0])), None)
    if ctx:
        value = sympify(ctx[1](nums(tex), ask))
        prec = ctx[2] or prec
    elif tex.startswith('\\text{Estimate'):
        a, b = nums(tex)[:2]
        value = Rational(str(round_sf(a, 1))) * Rational(str(round_sf(b, 1)))
        prec = ('sf', 1)
        if round_sf(a * b, 1) != to_decimal(value):
            fails.append('key: %s: estimating each factor to 1 s.f. and the product to 1 s.f. differ' % where)
    else:
        value = tex_value(tex)
    if prec is None and not value.is_rational:
        fails.append('key: %s: the value is irrational (%s) but no precision is stated' % (where, sympy.N(value, 8)))
        return
    need_std = any(ask.startswith(a) for a in STD_ASKS)
    keyv, keystd, keysf = info[0]
    if not fits(keyv, value, prec):
        fails.append('key: %s: %r is keyed but the value is %s' % (where, key, sympy.N(value, 12)))
    if need_std and not keystd:
        fails.append('key: %s: %r is not in standard form' % (where, key))
    if prec and prec[0] == 'sf' and need_std and keysf != prec[1]:
        fails.append('key: %s: %r is written to %d s.f., the question says %d' % (where, key, keysf, prec[1]))
    # s1-003 (R1): where the ask says "to 3 s.f.", a distractor in standard form is written to 3 s.f. too, or its form alone rules it out
    if prec and prec[0] == 'sf' and prec[1] >= 2 and need_std:
        for o, (v, std, sf) in zip(opts[1:], info[1:]):
            if std and sf is not None and sf != prec[1]:
                fails.append('precision: %s: the distractor %r is written to %d s.f., the question says %d (ruled out by its form alone)'
                             % (where, o, sf, prec[1]))
    right = [o for o, (v, std, _) in zip(opts, info) if fits(v, value, prec) and (std or not need_std)]
    if right != [key]:
        fails.append('options: %s: the right option(s) are %r, the key is %r' % (where, right, key))


def check_bank(fails, bank):
    for lv, items in bank.items():
        seen = set()
        for i, q in enumerate(items, 1):
            where = '%s %d (%s)' % (lv, i, q['q'][:50])
            try:
                check_item(fails, where, q)
            except Exception as e:      # an item the reader cannot read is a fail, not a skip
                fails.append('key: %s: could not be worked out here (%s: %s)' % (where, type(e).__name__, e))
            k = (q['q'], q['ask'])
            if k in seen:
                fails.append('options: %s: item repeated' % where)
            seen.add(k)


# ---- in the page ----------------------------------------------------------------------------------------------------
RENDER_JS = r"""(bank) => {
  const bad = [];
  for (const lv of Object.keys(bank)) for (const q of bank[lv]) {
    for (const t of [q.q].concat([q.correct], q.d.filter(v => v.includes('\\') || v.includes('^') || v.includes('{')))) {
      try { katex.renderToString(t, {throwOnError: true}); } catch (e) { bad.push(lv + ': ' + t + ' -> ' + e.message); }
    }
  }
  return bad;
}"""
SESSION_JS = r"""() => { const out = {};
  for (const lv of ['gcse', 'alevel']) { out[lv] = [];
    for (let k = 0; k < 3; k++) { level = lv; startGame(); out[lv].push({n: questions.length, idx: questions.map(q => QUESTIONS[lv].indexOf(q))}); } }
  return out; }"""
MARK_JS = r"""(args) => {
  const [lv, i] = args;
  level = lv; startGame();
  const item = QUESTIONS[lv][i], wanted = [item.correct].concat(item.d), out = [];
  const ann = (el) => { const a = el.querySelector('annotation'); return a ? a.textContent : el.textContent; };
  for (let k = 0; k < 4; k++) {
    questions = [item]; qIdx = 0; score = 0; streak = 0; correctCount = 0; showQ();
    const btns = [...document.querySelectorAll('#options .opt-btn')];
    const shown = btns.map(b => ({val: b.dataset.val, tex: ann(b)}));
    const qtex = ann(document.getElementById('question'));
    const target = btns.find(b => b.dataset.val === wanted[k]);
    target.click();
    out.push({k: k, shown: shown, qtex: qtex, prompt: document.getElementById('prompt').textContent,
              cls: target.className, keycls: btns.find(b => b.dataset.val === item.correct).className,
              others: btns.filter(b => b !== target && b.dataset.val !== item.correct).map(b => b.className),
              score: score, streak: streak, next: document.getElementById('nextMount').children.length});
    MaffsLock.clearTimers();
  }
  return out;
}"""


# ---- the working (contract SFB-WORKING-GCSE) -------------------------------------------------------------------------
WORKING_JS = "() => ({gcse: QUESTIONS.gcse.map(working), alevel: QUESTIONS.alevel.map(working)})"


def math_runs(line):
    """The maths of a working line: the runs outside its top-level \\text{...} groups."""
    runs, cur, i = [], '', 0
    while i < len(line):
        if line.startswith('\\text{', i):
            _inside, i = group(line, i + 5)
            runs.append(cur)
            cur = ''
            continue
        cur += line[i]
        i += 1
    runs.append(cur)
    return [r for r in runs if r.strip()]


def flat(tex):
    return re.sub(r'[{}\s]', '', tex)


def working_checks(fails, bank, work):
    """Every GCSE item has working and no A-Level item does; every "=" true; each working ends on the key."""
    for lv in ('gcse', 'alevel'):
        for i, (q, lines) in enumerate(zip(bank[lv], work[lv])):
            where = 'working: %s %d (%s)' % (lv, i + 1, q['q'][:40])
            if lv == 'alevel':
                if lines:
                    fails.append('%s: an A-Level item has working (A-Level is unchanged)' % where)
                continue
            if not lines:
                fails.append('%s: no working (its ask fits none of the six kinds)' % where)
                continue
            for k, line in enumerate(lines, 1):
                try:
                    for run in math_runs(line):
                        parts = run.split('=')
                        vals = [tex_value(x) for x in parts]
                        if len(parts) > 1 and any(sympy.simplify(v - vals[0]) != 0 for v in vals[1:]):
                            fails.append('%s line %d: %r is false (%s)' % (where, k, run.strip(), ' = '.join(map(str, vals))))
                except Exception as e:  # a line this script cannot read fails, never skips
                    fails.append('%s line %d: cannot read %r (%s)' % (where, k, line, e))
            if q['ask'].startswith('Which '):
                if lines[-1] != '\\text{So }' + q['correct']:
                    fails.append('%s: the working ends %r, not "So" and the key' % (where, lines[-1]))
                continue
            last = lines[-1].split('=')[-1]
            if flat(last) != flat(q['correct']):
                fails.append('%s: the working ends on %r, the key is %r' % (where, last.strip(), q['correct']))
            if q['ask'] == 'Write in standard form':
                m = NUM_RE.fullmatch(q['correct'])
                m1 = re.fullmatch(r'\\text\{Put the point after the first non-zero digit: \}(\S+)', lines[0])
                m2 = re.fullmatch(r'\\text\{Count the places it moves: \}(\d+)\\text\{, (left|right), so the power is '
                                  r'(positive|negative)\}', lines[1] if len(lines) > 1 else '')
                want = ('left', 'positive') if m and int(m.group(2)) >= 0 else ('right', 'negative')
                if not (m and m1 and m2) or Rational(m1.group(1)) != Rational(m.group(1)) \
                        or int(m2.group(1)) != abs(int(m.group(2))) or (m2.group(2), m2.group(3)) != want:
                    fails.append('%s: the first two lines do not name the coefficient and the places moved: %r'
                                 % (where, lines[:2]))


CARD_JS = r"""() => {
  window.setTimeout = () => 0; window.setInterval = () => 0;
  const out = [];
  for (const lv of ['gcse', 'alevel']) QUESTIONS[lv].forEach((q, i) => {
    for (const pick of [q.correct, ...q.d]) {
      level = lv; questions = [q]; qIdx = 0; totalQ = 1; score = 0; streak = 0; correctCount = 0;
      document.getElementById('progress').innerHTML = '<div class="pip current"></div>';
      showQ();
      const btn = [...document.querySelectorAll('#options .opt-btn')].find(x => x.dataset.val === pick);
      if (!btn) { out.push([lv, i, pick, 'not on screen']); continue; }
      btn.click();
      const cards = [...document.querySelectorAll('.maffs-ref')];
      const shown = cards.filter(c => getComputedStyle(c).display !== 'none');
      const want = working(q).length, box = shown[0], got = box ? box.querySelectorAll('.wl').length : 0;
      const next = document.querySelector('#nextMount .maffs-next');
      if (pick !== q.correct && lv === 'gcse') {
        if (shown.length > 1) out.push([lv, i, pick, 'answered wrong: ' + shown.length + ' cards show at once']);
        if (!box || !want || got !== want) out.push([lv, i, pick, 'answered wrong: the card shows ' + got + ' of ' + want + ' lines']);
        else if (box.querySelector('.katex-error') || [...box.querySelectorAll('.wl')].some(l => !l.textContent.trim()))
          out.push([lv, i, pick, 'answered wrong: a working line does not render']);
        else if (cards.some(c => c.querySelector(':scope > summary .maffs-ref-title').textContent !== 'How to get there'
                              || c.querySelector(':scope > summary .maffs-ref-show').textContent !== 'Working'))
          out.push([lv, i, pick, 'answered wrong: the card is not titled "How to get there" (open) and "Working" (collapsed)']);
        else if (cards.some(c => c.querySelectorAll('.wl').length !== want))
          out.push([lv, i, pick, 'answered wrong: the two copies of the card hold different lines']);
        if (!next) out.push([lv, i, pick, 'answered wrong: no Next']);
        else if (box && !(box.compareDocumentPosition(next) & Node.DOCUMENT_POSITION_FOLLOWING))
          out.push([lv, i, pick, 'answered wrong: the card comes after Next (canon 7.6.1: feedback above Next)']);
      } else if (shown.length) out.push([lv, i, pick, (pick === q.correct ? 'answered right' : 'A-Level') + ': the card is shown']);
      MaffsLock.clearTimers();
    }
  });
  return out;
}"""

# The sizes measured, (width, height): canon phones, a tall phone, the band edges of the page's media query (open at
# 320x1050, 360x980, 440x940, 760x870; collapsed at 359x1049, 439x979, 759x939, 760x869), the two laptops (ruling R2) and
# desktops.
LAYOUT_SIZES = [(320, 568), (375, 667), (390, 844), (412, 915), (320, 1050), (359, 1049), (360, 980), (439, 979),
                (440, 940), (759, 939), (760, 869), (760, 870), (1280, 720), (1366, 768), (1440, 900), (1920, 1080)]
NO_HEIGHT_TOL = 0.5
# Options sit two to a row and a row is as tall as its taller option, so every item is measured in all three pairings.
LAYOUT_JS = r"""async () => {
  const res = []; level = 'gcse'; startGame();
  for (let i = 0; i < QUESTIONS.gcse.length; i++) {
    const q = QUESTIONS.gcse[i]; questions[qIdx] = q; showQ();
    [...document.querySelectorAll('#options .opt-btn')].find(x => x.dataset.val !== q.correct).click();
    await document.fonts.ready;
    const n = document.querySelector('#nextMount .maffs-next');
    const box = document.getElementById('options'), bs = [...box.children], row = document.getElementById('workRow');
    let bottom = null, cost = 0;
    if (n && row) for (const o of [[0, 1, 2, 3], [0, 2, 1, 3], [0, 3, 1, 2]]) {
      o.forEach(k => box.appendChild(bs[k]));
      const withCard = n.getBoundingClientRect().bottom + scrollY;
      row.classList.remove('shown');
      const without = n.getBoundingClientRect().bottom + scrollY;
      row.classList.add('shown');
      bottom = Math.max(bottom === null ? -1 : bottom, withCard);
      cost = Math.max(cost, withCard - without);
    }
    const c = typeof shownCard === 'function' ? shownCard() : null;
    let lines = null;
    if (c && !c.open) {
      c.open = true;
      lines = [[...c.querySelectorAll('.wl')].filter(l => l.getBoundingClientRect().height > 0).length, working(q).length];
      c.open = false;
    }
    MaffsLock.clearTimers();
    const f = document.querySelector('.site-footer');
    const fold = innerHeight - (f && getComputedStyle(f).position === 'fixed' ? Math.round(f.getBoundingClientRect().height) : 0);
    res.push([i + 1, bottom, fold, cost, c ? (c.open ? 'open' : 'collapsed') : 'none', lines]);
  }
  return res;
}"""


def layout(fails, html, sizes=None):
    """Next within the fold with the card the media query shows, every GCSE item, normal and Aa."""
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            for mode in ('normal', 'aa'):
                for w, h in sizes or LAYOUT_SIZES:
                    ctx = browser.new_context(viewport={'width': w, 'height': h})
                    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
                    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
                    if mode == 'aa':
                        ctx.add_init_script("try { localStorage.setItem('mfg_accessible', 'true'); } catch (e) {}")
                    bc.offline(ctx, base)
                    ctx.route(lambda url: bc.is_font_cdn(url), bc.serve_real_font)
                    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
                    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                        status=200, content_type='text/html; charset=utf-8', body=html))
                    page = ctx.new_page()
                    page.goto(base + '/games/%s/?cb=layout' % SLUG, wait_until='load', timeout=20000)
                    page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof katex !== "undefined"', timeout=15000)
                    for i, bottom, fold, cost, card, lines in page.evaluate(LAYOUT_JS):
                        tag = 'layout %s %dx%d gcse %d' % (mode, w, h, i)
                        if bottom is None or card == 'none':
                            fails.append('%s: no card or no Next after a wrong answer' % tag)
                            continue
                        if lines and lines[0] != lines[1]:
                            fails.append('%s: the collapsed card, opened, shows %d of %d lines' % (tag, lines[0], lines[1]))
                        if card == 'open' and bottom > fold + 0.5:
                            fails.append('%s: with the card open, Next ends at %.0fpx, past the %dpx fold' % (tag, bottom, fold))
                        if card == 'collapsed' and cost > NO_HEIGHT_TOL:
                            fails.append('%s: the collapsed card costs %.0fpx: Next ends lower than with no card' % (tag, cost))
                    ctx.close()
            browser.close()
    finally:
        proc.terminate()
        proc.wait()


def mark_checks(fails, page, bank):
    for lv, items in bank.items():
        for i, q in enumerate(items):
            where = '%s %d (%s)' % (lv, i + 1, q['q'][:40])
            res = page.evaluate(MARK_JS, [lv, i])
            for r in res:
                right = r['k'] == 0
                if right:
                    ok = 'correct' in r['cls'].split() and 'wrong' not in r['cls'].split() and r['score'] == 100 and r['streak'] == 1
                else:
                    ok = ('wrong' in r['cls'].split() and 'correct' in r['keycls'].split() and r['score'] == 0
                          and r['streak'] == 0 and r['next'] >= 1 and all('correct' not in c.split() and 'wrong' not in c.split() for c in r['others']))
                if not ok:
                    fails.append('marking: %s, option %d (%s): classes %r / key %r, score %d, streak %d, next %d' % (
                        where, r['k'], 'the key' if right else 'a distractor', r['cls'], r['keycls'], r['score'], r['streak'], r['next']))
                    break
            r0 = res[0]
            if sorted(s['val'] for s in r0['shown']) != sorted([q['correct']] + q['d']):
                fails.append('marking: %s: the buttons are %r, not the item\'s options' % (where, [s['val'] for s in r0['shown']]))
            for s in r0['shown']:
                if any(ch in s['val'] for ch in '\\^{') and s['tex'] != s['val']:
                    fails.append('render: %s: option %r shows as %r' % (where, s['val'], s['tex']))
                    break
            if r0['qtex'] != q['q'] or r0['prompt'] != q['ask']:
                fails.append('render: %s: the question shows as %r / %r' % (where, r0['qtex'], r0['prompt']))


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    stats = {}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            ctx.route(lambda url: bc.is_font_cdn(url), bc.serve_real_font)     # KaTeX from the pinned local copy
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.clock.install()
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof katex !== "undefined"', timeout=15000)
            bank = page.evaluate('() => JSON.parse(JSON.stringify(QUESTIONS))')
            check_bank(fails, bank)
            for msg in page.evaluate(RENDER_JS, bank):
                fails.append('render: KaTeX cannot parse %s' % msg)
            for lv, deals in page.evaluate(SESSION_JS).items():
                for d in deals:
                    if d['n'] != 20 or len(set(d['idx'])) != 20 or min(d['idx']) < 0:
                        fails.append('session: %s dealt %d questions (%d different, from the bank: %s)' % (
                            lv, d['n'], len(set(d['idx'])), min(d['idx']) >= 0))
            mark_checks(fails, page, bank)
            working_checks(fails, bank, page.evaluate(WORKING_JS))
            for lv, i, pick, what in page.evaluate(CARD_JS):
                fails.append('card: %s %d (%s), option %r %s' % (lv, i + 1, bank[lv][i]['q'][:40], pick, what))
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            browser.close()
            stats = {lv: len(v) for lv, v in bank.items()}
    finally:
        proc.terminate()
        proc.wait()
    return stats


PLANTS = [
    ('a wrong standard-form key (exponent off by one)', 'key:',
     [("correct:'4.5 \\\\times 10^4',d:['45 \\\\times 10^3'", "correct:'4.5 \\\\times 10^5',d:['45 \\\\times 10^3'")]),
    ('a second right option (equal and in standard form)', 'options:',
     [("d:['45 \\\\times 10^3','4.5 \\\\times 10^3','0.45 \\\\times 10^5']", "d:['45 \\\\times 10^3','4.50 \\\\times 10^4','0.45 \\\\times 10^5']")]),
    ('a 3 s.f. key off in the last figure', 'key:',
     [("correct:'4.14 \\\\times 10^{-15}'", "correct:'4.13 \\\\times 10^{-15}'")]),
    ('a context answer off by one', 'key:',
     [("correct:'£37313'", "correct:'£37314'")]),
    ('the largest of three keyed as the smallest', 'options:',
     [("correct:'2.9 \\\\times 10^5',d:['3.1 \\\\times 10^4','8 \\\\times 10^3','All equal']", "correct:'8 \\\\times 10^3',d:['3.1 \\\\times 10^4','2.9 \\\\times 10^5','All equal']")]),
    ('SR-4/16: an option equal to the key in value, "ordinary number" asked', 'options:',
     [("correct:'37000',d:['3700','370000','370']", "correct:'37000',d:['37000.0','370000','370']")]),
    ('SR-4/16: an option equal to the key in value, plain "Calculate" asked', 'options:',
     [("correct:'1',d:['0','10^{12}','10^{-12}']", "correct:'1',d:['1.0','10^{12}','10^{-12}']")]),
    ('SR-4: two wrong options equal in value (2.5 x 10^3 and 25 x 10^2, B11-CLEAR)', 'options:',
     [("d:['2.5 \\\\times 10^{3}','2.5 \\\\times 10^{-3}','4 \\\\times 10^{-4}']", "d:['2.5 \\\\times 10^{3}','25 \\\\times 10^{2}','4 \\\\times 10^{-4}']")]),
    ('a solve-for key that does not solve the equation', 'key:',
     [("correct:'7',d:['70','0.7','14']", "correct:'70',d:['7','0.7','14']")]),
    ('the wrong claim keyed for "which two are equal"', 'options:',
     [("correct:'4.5 \\\\times 10^6 \\\\text{ and } 45 \\\\times 10^5',d:['None are equal','4.5 \\\\times 10^5 \\\\text{ and } 45 \\\\times 10^5','All three']",
       "correct:'All three',d:['None are equal','4.5 \\\\times 10^5 \\\\text{ and } 45 \\\\times 10^5','4.5 \\\\times 10^6 \\\\text{ and } 45 \\\\times 10^5']")]),
    ('marking by the first three characters only', 'marking:',
     [("const ok=btn.dataset.val===q.correct;", "const ok=btn.dataset.val.slice(0,3)===q.correct.slice(0,3);")]),
    ('SR-1: the approximate key with no precision stated (s1-001)', 'precision:',
     [("ask:'How many times heavier is Earth? (nearest whole number)'", "ask:'How many times heavier is Earth?'")]),
    ('SR-4: the two-error distractor back (s1-002)', 'options:',
     [("'4.5 \\\\times 10^{19}','2 \\\\times 10^{-3}']", "'4.5 \\\\times 10^{19}','2 \\\\times 10^3']")]),
    ('s1-003: a 1 s.f. distractor beside a 3 s.f. key', 'precision:',
     [("'5.99 \\\\times 10^{-27}','5.99 \\\\times 10^{25}']", "'5.99 \\\\times 10^{-27}','6 \\\\times 10^{25}']")]),
    ('a session one question short', 'session:',
     [("slice(0,totalQ);qIdx=0;score=0;", "slice(0,totalQ-1);qIdx=0;score=0;")]),
    ('a misspelt TeX command in a key', 'render:',
     [("correct:'3.7 \\\\times 10^4'", "correct:'3.7 \\\\tims 10^4'")]),
]
# SFB-WORKING-GCSE (19 Nov 2026): the working's rules broken, the card not shown, and the card below Next.
PLANTS += [
    ('working, rule d: the coefficients added, not multiplied', 'working:',
     [("const c=op==='times'?mul(A1,A2):div(A1,A2);",
       "const c=op==='times'?{m:A1.m*10n**BigInt(A1.e-Math.min(A1.e,A2.e))+A2.m*10n**BigInt(A2.e-Math.min(A1.e,A2.e)),"
       "e:Math.min(A1.e,A2.e)}:div(A1,A2);")]),
    ('working, rule e: the powers subtracted the wrong way round', 'working:',
     [("const e=op==='times'?b1+b2:b1-b2;", "const e=op==='times'?b1+b2:b2-b1;")]),
    ('working: the card not shown on a wrong answer', 'card:',
     [("else{showWorking(q);MaffsNext.wrong(", "else{MaffsNext.wrong(")]),
    ('working: the card moved below Next', 'card:',
     [('      <div id="nextMount"></div>\n    </div>', '    </div>'),
      ('    <div class="maffs-ref-row work-row" id="workRow">',
       '    <div id="nextMount"></div>\n    <div class="maffs-ref-row work-row" id="workRow">')]),
]
# the last plant needs the key's source, which is an ordinary number in this item; use the item that has TeX keys instead
PLANTS[[p[0] for p in PLANTS].index('a misspelt TeX command in a key')] = ('a misspelt TeX command in an option', 'render:',
              [("correct:'3.2 \\\\times 10^3',d:['32 \\\\times 10^2'", "correct:'3.2 \\\\tims 10^3',d:['32 \\\\times 10^2'")])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    st = play(fails, html)
    print('%s: %d GCSE and %d A-Level items, every key worked out exactly from its TeX; every option classified; every option pressed '
          'in Chromium' % (SLUG, st.get('gcse', 0), st.get('alevel', 0)))
    ok = True
    if not args.no_selftest and not args.against:
        for what, tag, edits in PLANTS:
            bad = [o for o, n in edits if html.count(o) != 1]
            if bad:
                print('  self-test %-58s *** CANNOT PLANT (%r) ***' % (what, bad[0][:60]))
                ok = False
                continue
            planted = html
            for o, n in edits:
                planted = planted.replace(o, n)
            rep = []
            play(rep, planted)
            found = [f for f in rep if tag in f]
            ok = ok and bool(found)
            print('  self-test %-58s %s' % (what, ('caught: ' + found[0][:100]) if found else '*** MISSED ***'))
    layout(fails, html)
    for f in fails[:40]:
        print('FAIL  ' + f[:400])
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
