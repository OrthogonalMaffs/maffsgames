#!/usr/bin/env python3
# ci-line: Complex Converter (every key equal to its given number, the principal argument stated and keyed, no option a second form of the key; every option marked in Chromium; every wrong answer's Why card recomputed and its slip checked; the back link clear of every header) |
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
number, with principal angles; no context asks for another range ("positive angle"); no two options are the same
number (an angle written with π read in radians) unless checker-allowlist.json lists the pair as a form question
(SR-4; B11-CLEAR, 12 Oct 2026: 3∠30° and 3∠π/6 under "(degrees)"). In Chromium (390x844)
every item is shown through showRouletteQ() and every option clicked through rouletteAnswer(): the key marked
right, the others wrong, and a polar or exponential question's target line states the range.
Calculator hints (SWEEP-1, batch 11; complex-converter-t6-005): every CALC_HINTS entry (20 entries, 80 expression/result pairs) has its correct and
distractor expressions parsed from their own TeX and evaluated (degrees where the argument carries °, arctan in
the entry's DEG or RAD mode), and each printed result must equal the computed value to its printed decimals, with
the unit matching the mode. Six hand-typed results had been wrong (6.65 for 6.67, 1.73 for 17.32 ...).
Why (contract COMPLEX-CONVERTER-WHY, Jon 21 Nov 2026): a wrong answer in Form Roulette shows a reference card
that works the conversion with the item's own numbers and names the slip when the picked option is one slip by
computation. Every card (55 items, all 165 distractors, built by the page's WHY.card()) is checked: each value shown
recomputes from the numbers beside it (to its shown places; = only where exact, an approx sign only where the given
number was itself rounded), the working's inputs are the item's Re and Im, or r and θ, arctan is of Im over Re, its
last values are the key's, and the slip named is the one this script finds by its own computation (none when no one
slip gives the option). In Chromium, Jon's q16 (6 + 8j, picked 10e^{j0.644}) shows the card before Next, naming the
upside-down fraction, in j under Level 4 and i under Further Maths. The back link, in the page's flow since this
contract (it was fixed over each mode's title), may not touch any title or header on any screen (menu, the three
modes, end) at 320x568, 390x844 and 1366x768, and reads site-nav's label.
A self-test plants the audit's item, one item's old positive-angle key and two old hint figures back into a copy
of the page, and three Why faults (arctan of Re over Im, a slip named for an option it does not give, the back link
fixed over the title); each must FAIL naming its item.

    python scripts/verify-complex-converter.py [--no-selftest] [--against FILE] [--katex-dir DIR]
"""
import argparse
import cmath
import json
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
        deg = math.degrees(real(th)) if '\\pi' in th else real(th)    # an angle written with pi is in radians
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


def listed_pairs():
    """Option pairs equal in value that checker-allowlist.json lists as form questions for this game (the ask names
    the form: 3∠30° and 3∠π/6 under "(degrees)"), as (index, frozenset(pair)); Level 4 and Further share the bank."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'checker-allowlist.json')
    out = set()
    for e in json.load(open(path, encoding='utf-8'))['b11_form_questions']:
        m = re.fullmatch(r'complex-converter QUESTIONS\.\w+\[(\d+)\]', e['where'])
        if m:
            out.add((int(m.group(1)), frozenset(e['pair'])))
    return out


def check_bank(fails, bank):
    listed = listed_pairs()
    if len(bank) != COUNT:
        fails.append('bank: %d items, expected %d' % (len(bank), COUNT))
    for n, q in enumerate(bank):
        w = 'id %d (%s → %s, %s)' % (q['id'], q['source'], q['target'], q['givenLatex'])
        opts = [q['correctLatex']] + list(q['distractors'])
        if q['id'] in (19, 24, 27, 34, 50) and re.search(r'impedance|reactance', q.get('context', '')):   # s1-002 (R3)
            fails.append('%s: the context calls a number with a negative real part, or a reactance that is not purely imaginary, an impedance or a reactance (a passive impedance has no negative resistance): %r (complex-converter-s1-002)' % (w, q['context']))
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
            if close(v, z) and (n, frozenset((opts[0], o))) not in listed:
                fails.append('%s: the wrong option %s is the same number as the key %s' % (w, o, opts[0]))
        # SR-4 (B11-CLEAR, 12 Oct 2026): no two wrong options are the same number either (0 + 7j beside 7j).
        for x in range(1, 4):
            for y in range(x + 1, 4):
                if close(vals[x][0], vals[y][0]) and (n, frozenset((opts[x], opts[y]))) not in listed:
                    fails.append('%s: the wrong options %s and %s are the same number (SR-4)' % (w, opts[x], opts[y]))
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
CARDS = []          # the last run's Why cards, for the report


def hint_value(tex, mode):
    """Evaluate a CALC_HINTS expression's TeX (\\arctan, \\cos/\\sin/\\tan, \\dfrac, \\sqrt, \\pi, °)."""
    t = tex.replace('\\left', '').replace('\\right', '').replace('\\!', '').replace('\\pi', 'pi')
    t = t.replace('\u00b0', '*pi/180')
    for _ in range(6):
        t = re.sub(r'\\dfrac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', t)
        t = re.sub(r'\\sqrt\{([^{}]*)\}', r'sqrt(\1)', t)
    t = re.sub(r'\\(arctan|cos|sin|tan)', lambda m: {'arctan': 'atan'}.get(m.group(1), m.group(1)), t)
    t = re.sub(r'(\d|\))\s*(?=[a-z(])', r'\1*', t)
    if '\\' in t:
        raise ValueError('unparsed TeX in %r' % tex)
    env = {k: getattr(math, k) for k in ('pi', 'sqrt', 'cos', 'sin', 'tan', 'atan')}
    v = eval(t, {'__builtins__': {}}, env)
    if 'atan' in t and mode == 'DEG':
        v = math.degrees(v)
    return v


def check_hints(fails, hints):
    if len(hints) != 20:
        fails.append('CALC_HINTS has %d entries, expected 20' % len(hints))
    for qid, h in sorted(hints.items(), key=lambda kv: int(kv[0])):
        exprs = [h['correct']] + list(h['distractors'])
        results = [h['result']] + list(h['results'])
        if len(exprs) != len(results):
            fails.append('CALC_HINTS id %s: %d expressions but %d results' % (qid, len(exprs), len(results)))
            continue
        for tex, res in zip(exprs, results):
            res = res.replace('\u200b', '')
            m = re.match(r'^(-?\d+(?:\.(\d+))?)(\u00b0|\s+rad)?', res)
            if not m:
                fails.append('CALC_HINTS id %s: cannot read result %r' % (qid, res))
                continue
            shown, dec, unit = float(m.group(1)), len(m.group(2) or ''), m.group(3)
            try:
                got = hint_value(tex, h['mode'])
            except Exception as e:  # noqa: BLE001
                fails.append('CALC_HINTS id %s: cannot evaluate %r (%s)' % (qid, tex, e))
                continue
            if 'arctan' in tex and (unit or '').strip() != ('\u00b0' if h['mode'] == 'DEG' else 'rad'):
                fails.append('CALC_HINTS id %s: %r shown as %r in %s mode' % (qid, tex, res, h['mode']))
            if abs(round(got, dec) - shown) > 1e-9:
                fails.append('CALC_HINTS id %s: %s = %.*f but the hint shows %s' % (qid, tex, dec + 2, got, res))



# ---- WHY (contract COMPLEX-CONVERTER-WHY, Jon 21 Nov 2026) ----------------------------------------------------------
# After a wrong answer in Form Roulette the page shows a "Why" reference card: the conversion worked with the item's own
# numbers and, when the picked option is one slip by computation, that slip named. Here every card (55 items, every
# distractor: 165) is rebuilt by the page's WHY.card() and checked against this script's own computation: every value
# shown recomputes from the numbers beside it (to its shown places, = only where exact, \approx only where the given
# number was itself rounded), the working's inputs are the item's re, im, r and angle, its last value is the key's, and
# the slip named is the one this script finds (or none, when no one slip gives the option).

def parts(tex):
    """(form, a, b, flag): polar (r, angle as written, written in degrees?), exponential (r, angle as written, None),
    cartesian (re, im, None). An angle with \\pi is read in radians, as written."""
    t = tex.strip()
    if '\\angle' in t:
        r, th = t.split('\\angle')
        return 'polar', real(r), real(th.replace('°', '')), '°' in th
    m = re.fullmatch(r'(.*?)e\^\{(.*)\}', t)
    if m:
        ex = m.group(2).replace('\\cdot', '').replace(' ', '')
        sign = -1 if ex.startswith('-') else 1
        body = ex.lstrip('-')
        body = body[1:] if body.startswith('j') else body
        return 'exponential', real(m.group(1)), (sign * real(body)) if body else 0.0, None
    z = value(t)[0]
    return 'cartesian', z.real, z.imag, None


def near(a, b, tol=None):
    return abs(a - b) <= (tol if tol is not None else 0.002 * max(1.0, abs(b)))


def slip_of(q, pick):
    """The slip family that gives `pick` from the item's numbers, or None (no family, or two at once)."""
    re_, im, r, deg, rad = q['re'], q['im'], q['r'], q['argDeg'], q['argRad']
    form, a, b, in_deg = parts(pick)
    found = set()
    if q['target'] == 'cartesian':
        if form != 'cartesian':
            return None
        same_size = near(abs(re_), abs(im))
        if not same_size and near(a, im) and near(b, re_):
            found.add('cos_sin')                                          # r sin θ + (r cos θ) j
        if (not same_size and min(abs(re_), abs(im)) > 1e-9 and (a < 0) == (re_ < 0) and (b < 0) == (im < 0)
                and near(abs(a), abs(im)) and near(abs(b), abs(re_))):
            found.add('cos_sin')                                          # the sizes swapped, the quadrant's signs kept
        for sa, sb in ((-1, 1), (1, -1), (-1, -1)):
            if (sa < 0 and abs(re_) < 1e-9) or (sb < 0 and abs(im) < 1e-9):
                continue
            if near(a, sa * re_) and near(b, sb * im):
                found.add('signs')
    else:
        if form != q['target']:
            return None
        polar = form == 'polar'
        want = deg if polar else rad
        tol = 0.02 if polar else 0.002
        ang = (b if in_deg else float('nan')) if polar else b
        unit = (lambda x: x) if polar else math.radians
        r_ok = near(a, r)
        if q['source'] == 'cartesian' and re_ != 0 and im != 0:
            ref = math.degrees(math.atan(abs(im) / abs(re_)))
            sg = 1 if im > 0 else -1
            principal_of = (lambda x: sg * x) if re_ > 0 else (lambda x: sg * (180 - x))
            if r_ok and near(ang, unit(principal_of(90 - ref)), tol):
                found.add('upside')                                       # arctan(Re/Im), then the item's own step
            if r_ok and re_ < 0 and (near(ang, unit(ref), tol) or near(ang, unit(-ref), tol)):
                found.add('quadrant_missing')
            if r_ok and re_ > 0 and near(ang, unit(sg * (180 - ref)), tol):
                found.add('quadrant_extra')
        if q['source'] == 'cartesian' and near(ang, want, tol) and not r_ok:
            if near(a, abs(re_)) or near(a, abs(im)):
                found.add('mod_part')
            if near(a, abs(re_) + abs(im)):
                found.add('mod_sum')
            if near(a, re_ * re_ + im * im):
                found.add('mod_noroot')
        if r_ok and abs(deg) > 0.01 and abs(abs(deg) - 180) > 0.01 and near(ang, -want, tol):
            found.add('conjugate')
        if not polar and r_ok and abs(deg) > 3.5 and near(b, deg, 0.02):
            found.add('deg_in_exp')
        if polar and r_ok and abs(rad) > 0.01 and near(b, rad, 0.002):
            found.add('rad_as_deg')
        if q['source'] != 'cartesian' and near(a, parts(q['givenLatex'])[2]) and near(b, r):
            found.add('r_theta_swap')
    groups = {('mod' if f.startswith('mod_') else f) for f in found}
    if len(groups) != 1:
        return None
    if groups == {'mod'}:
        mods = sorted(found)
        return mods[0] if len(mods) == 1 else 'mod_both'
    return groups.pop()


def tex_value(seg):
    """A worked value's TeX as a number in radians where it is an angle (° is pi/180), or None for a symbolic one."""
    s = seg.strip()
    if not s or re.search(r'\\mathrm\{(Re|Im)\}|\\theta|\\tan|^r$|r\\(cos|sin)', s):
        return None
    t = s.replace('\\left', '').replace('\\right', '').replace('\\,', '').replace('\\mathrm{rad}', '')
    t = t.replace('\\times', '*').replace('\\arctan', 'atan').replace('\\cos', 'cos').replace('\\sin', 'sin')
    t = t.replace('\\pi', 'pi').replace('°', '*(pi/180)')
    for _ in range(6):
        t = re.sub(r'\\dfrac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', t)
        t = re.sub(r'\\sqrt\{([^{}]*)\}', r'sqrt(\1)', t)
    t = t.replace('^2', '**2').replace('{', '(').replace('}', ')')
    t = re.sub(r'(\d|\))\s*(?=[a-z(])', r'\1*', t)
    if '\\' in t or re.search(r'[^0-9a-z+\-*/(). ]', t):
        raise ValueError('unread TeX %r' % seg)
    return float(eval(t, {'__builtins__': {}}, {k: getattr(math, k) for k in ('pi', 'sqrt', 'cos', 'sin', 'atan')}))


def chain(math_tex):
    """Split a line's maths at its top-level = and \\approx: ([segments], [operators])."""
    segs, ops, d, cur, i = [], [], 0, '', 0
    while i < len(math_tex):
        c = math_tex[i]
        if c in '{(':
            d += 1
        elif c in '})':
            d -= 1
        if d == 0 and c == '=':
            segs.append(cur); ops.append('='); cur = ''; i += 1; continue
        if d == 0 and math_tex.startswith('\\approx', i):
            segs.append(cur); ops.append('~'); cur = ''; i += 7; continue
        cur += c
        i += 1
    segs.append(cur)
    return [s.strip() for s in segs], ops


def agrees(left, seg, op):
    """Does the shown `seg` equal the computed `left` (radians for angles): to its decimals for '=', or near it for '~'?"""
    right = tex_value(seg)
    scale = math.pi / 180 if '°' in seg else 1.0
    lv, rv = left / scale, right / scale
    m = re.fullmatch(r'-?\d+\.(\d+)°?(\\,\\mathrm\{rad\})?', seg.strip())
    p = len(m.group(1)) if m else 0
    if op == '=':
        return abs(lv - rv) <= (0.5 * 10 ** -p + 1e-9 if p else 1e-4 * max(1.0, abs(rv)))
    return abs(lv - rv) <= max(0.5 * 10 ** -p if p else 0, 0.005 * max(1.0, abs(rv)))


def angle_ok(v, q):
    return v is not None and abs(v - math.radians(q['argDeg'])) <= 6e-4


def why_faults(q, pick, card):
    w = 'id %d (%s → %s, %s, picked %s)' % (q['id'], q['source'], q['target'], q['givenLatex'], pick)
    out = []
    kind, lines = card['kind'], card['lines']
    want = slip_of(q, pick)
    if kind != want:
        out.append('%s: Why names the slip %r, by computation from the item it is %r' % (w, kind, want))
    if kind:
        head, lines = lines[0], lines[1:]
        if kind == 'signs':
            c, s = math.cos(math.radians(q['argDeg'])), math.sin(math.radians(q['argDeg']))
            word = lambda x: 'positive' if x > 1e-9 else 'negative' if x < -1e-9 else '0'
            if 'cos θ is %s and sin θ is %s' % (word(c), word(s)) not in head:
                out.append('%s: the slip line %r has the wrong signs for cos and sin' % (w, head))
    if not lines or lines[-1] != '\\text{So the answer is }' + q['correctLatex']:
        out.append('%s: Why does not end "So the answer is %s"' % (w, q['correctLatex']))
    G = parts(q['givenLatex'])
    got = set()
    for line in lines[:-1]:
        maths = re.sub(r'\\text\{[^{}]*\}', ' ', line)
        segs, ops = chain(maths)
        try:
            vals = [tex_value(s) for s in segs]
        except (ValueError, SyntaxError, ZeroDivisionError) as e:
            out.append('%s: Why line %r cannot be read: %s' % (w, line, e))
            continue
        for k, op in enumerate(ops):
            if vals[k] is not None and vals[k + 1] is not None and not agrees(vals[k], segs[k + 1], op):
                out.append('%s: Why line %r: %s %s %s is not true' % (w, line, segs[k], '=' if op == '=' else '≈', segs[k + 1]))
        last = vals[-1] if vals else None
        if line.startswith('r = \\sqrt{\\mathrm{Re}^2 + \\mathrm{Im}^2} = '):
            m = re.fullmatch(r'\\sqrt\{\(?(.+?)\)?\^2 \+ \(?(.+?)\)?\^2\}', segs[2])
            if not (m and near(tex_value(m.group(1)), q['re']) and near(tex_value(m.group(2)), q['im'])):
                out.append('%s: Why squares %r, not the item\'s Re %s and Im %s' % (w, segs[2], q['re'], q['im']))
            if last is None or not near(last, q['r']):
                out.append('%s: Why gives r = %s, the item\'s r is %s' % (w, segs[-1], q['r']))
            got.add('r')
        elif '\\arctan' in line:
            if '\\arctan\\left(\\dfrac{\\mathrm{Im}}{\\mathrm{Re}}\\right)' not in line:
                out.append('%s: Why line %r is not arctan(Im / Re)' % (w, line))
            m = re.search(r'\\arctan\\left\(\\dfrac\{([^{}]*(?:\{[^{}]*\})?[^{}]*)\}\{([^{}]*(?:\{[^{}]*\})?[^{}]*)\}\\right\)', segs[-2] if len(segs) > 1 else '')
            if not (m and near(tex_value(m.group(1)), q['im']) and near(tex_value(m.group(2)), q['re'])):
                out.append('%s: Why line %r: the arctan is not of the item\'s Im over its Re (%s / %s)' % (w, line, q['im'], q['re']))
            if line.startswith('\\theta'):
                got.add('theta') if angle_ok(last, q) else out.append('%s: Why gives θ = %s, the key\'s angle is %s°' % (w, segs[-1], q['argDeg']))
        elif re.search(r'[+-] (180°|\\pi) = ', maths):
            got.add('theta') if angle_ok(last, q) else out.append('%s: Why\'s quadrant step gives %s, the key\'s angle is %s°' % (w, segs[-1], q['argDeg']))
        elif line.startswith('\\mathrm{Re} = r\\cos\\theta = ') or line.startswith('\\mathrm{Im} = r\\sin\\theta = '):
            part, fn = ('re', 'cos') if line.startswith('\\mathrm{Re}') else ('im', 'sin')
            m = re.fullmatch(r'(.*)\\%s\((.*)\)' % fn, segs[2])
            given_rad = math.radians(G[2]) if G[3] else G[2]
            if not (m and near(tex_value(m.group(1)) if m.group(1) else 1.0, G[1]) and near(tex_value(m.group(2)), given_rad)):
                out.append('%s: Why line %r does not use the given r and θ' % (w, line))
            if last is None or not near(last, q[part]):
                out.append('%s: Why gives %s = %s, the item\'s is %s' % (w, part.title(), segs[-1], q[part]))
            got.add(part)
        elif '\\times \\dfrac{' in line:
            given_rad = math.radians(G[2]) if G[0] == 'polar' else G[2]
            if not near(tex_value(segs[1].split('\\times')[0]), given_rad, 0.001):
                out.append('%s: Why converts %s, the given angle is %s' % (w, segs[1], q['givenLatex']))
            got.add('converted')
            if angle_ok(last, q):
                got.add('theta')
        elif re.search(r' - (360°|2\\pi) = ', maths):
            got.add('theta') if angle_ok(last, q) else out.append('%s: Why\'s range step gives %s, the key\'s angle is %s°' % (w, segs[-1], q['argDeg']))
        elif line.startswith('\\text{r stays the same: }r = '):
            got.add('r') if near(last, q['r']) else out.append('%s: Why keeps r = %s, the item\'s r is %s' % (w, segs[-1], q['r']))
        elif re.match(r'\\text\{(Re|Im) is 0: the point is on the (positive|negative) (real|imaginary) axis, so \}\\theta = ', line):
            got.add('theta') if angle_ok(last, q) else out.append('%s: Why puts θ = %s on the axis, the key\'s angle is %s°' % (w, segs[-1], q['argDeg']))
        elif re.fullmatch(r'\\text\{The point is on the (positive|negative) (real|imaginary) axis\.\}', line):
            pass
        elif line.startswith('\\text{(') and 'is itself rounded' in line:
            pass
        else:
            out.append('%s: Why line %r is not one this check knows' % (w, line))
    need = {'r', 'theta'} if q['target'] != 'cartesian' else {'re', 'im'}
    if not need <= got:
        out.append('%s: Why never reaches the key\'s %s' % (w, ', '.join(sorted(need - got))))
    return out


CARDS_JS = r"""() => QUESTIONS.level4.flatMap(q => q.distractors.map(d => ({id: q.id, pick: d, card: WHY.card(q, d)})))"""


def check_why(fails, bank, cards):
    by_id = {q['id']: q for q in bank}
    if len(cards) != 3 * COUNT:
        fails.append('Why: %d cards built, expected %d' % (len(cards), 3 * COUNT))
    for c in cards:
        fails.extend(why_faults(by_id[c['id']], c['pick'], c['card']))


def why_report(bank, cards):
    """The PR report's table: distractors per slip family, and the ids left unnamed."""
    from collections import Counter
    kinds = Counter(c['card']['kind'] or 'none' for c in cards)
    unnamed = sorted({c['id'] for c in cards if not c['card']['kind']})
    return kinds, unnamed


# The live checks: a wrong answer shows Why before Next, in the level's notation; the back link clear of every header.
LIVE_JS = r"""([qid, pick]) => {
  const q = QUESTIONS.level4.find(x => x.id === qid);
  rQuestions = [q, q]; rIndex = 0; rScore = 0; rCorrect = 0; rTimes = []; rDirStats = {}; rCalcUses = 0;
  showScreen('rouletteScreen'); showRouletteQ();
  [...document.querySelectorAll('#rOptions .opt-btn')].find(b => b.dataset.val === pick).click();
  const card = [...document.querySelectorAll('#rWhyRow > .maffs-ref')].filter(d => getComputedStyle(d).display !== 'none');
  const nx = document.querySelector('#rNext .maffs-next');
  const tex = card.length ? [...card[0].querySelectorAll('annotation')].map(a => a.textContent) : [];
  return {cards: card.length, before: !!(card.length && nx && (card[0].compareDocumentPosition(nx) & Node.DOCUMENT_POSITION_FOLLOWING)),
          tex, text: card.length ? card[0].textContent : '', errors: card.length ? card[0].querySelectorAll('.katex-error').length : 0}; }"""
SCREENS_JS = r"""() => {
  const out = [];
  const box = e => { const r = e.getBoundingClientRect(); return {l: r.left, t: r.top + scrollY, r: r.right, b: r.bottom + scrollY, w: r.width, h: r.height}; };
  const hit = (a, b) => a.l < b.r - 0.5 && b.l < a.r - 0.5 && a.t < b.b - 0.5 && b.t < a.b - 0.5;
  const screens = [['menu', () => showMenu()], ['roulette', () => startMode('roulette')], ['triples', () => startMode('triples')],
                   ['sniper', () => startMode('sniper')], ['end', () => showScreen('endScreen')]];
  for (const [name, go] of screens) {
    go(); window.scrollTo(0, 0);
    const links = [...document.querySelectorAll('a.back-link')].filter(a => a.getClientRects().length);
    if (links.length !== 1) { out.push([name, links.length + ' back links shown']); continue; }
    const bl = box(links[0]);
    if (bl.w < 1 || bl.h < 1) { out.push([name, 'the back link has no box']); continue; }
    const scr = document.getElementById(name === 'menu' ? 'menuScreen' : name + 'Screen');
    const heads = [...scr.querySelectorAll('.game-header, .game-header *, .menu-title, .menu-sub, .level-pill, .end-title, .end-score')]
      .filter(e => e.getClientRects().length);
    for (const h of heads) if (hit(bl, box(h))) { out.push([name, 'the back link overlaps ' + (h.className || h.tagName) + ' "' + h.textContent.trim().slice(0, 30) + '"']); break; }
  }
  return out; }"""


def live_why(fails, browser, base, html, page_url):
    def ctx_for(w, h, referer_hub=False):
        ctx = browser.new_context(viewport={'width': w, 'height': h})
        ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
        bc.offline(ctx, base)
        if KATEX_DIR:
            ctx.route(lambda url: '/katex@' in url and '/dist/' in url, lambda route: route.fulfill(
                path=os.path.join(KATEX_DIR, route.request.url.split('/dist/', 1)[1].split('?')[0])))
        else:
            ctx.route(lambda url: bc.is_font_cdn(url), bc.serve_real_font)
        ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
            status=200, content_type='text/html; charset=utf-8', body=html))
        return ctx
    # q16 (Jon's item): 6 + 8j, picked 10e^{j0.644}, arctan(6/8).
    for level, unit in (('level4', 'j'), ('further', 'i')):
        ctx = ctx_for(390, 844)
        page = ctx.new_page()
        page.goto(base + '/games/%s/?level=%s&cb=why' % (SLUG, level), wait_until='load', timeout=20000)
        page.wait_for_function('typeof WHY !== "undefined" && typeof katex !== "undefined"', timeout=15000)
        got = page.evaluate(LIVE_JS, [16, '10e^{j0.644}'])
        where = 'Why in Chromium (%s, id 16 picked 10e^{j0.644})' % level
        if got['cards'] != 1 or not got['before']:
            fails.append('%s: %d cards shown, %s Next' % (where, got['cards'], 'before' if got['before'] else 'not before'))
        if 'The fraction is upside down' not in got['text']:
            fails.append('%s: no "The fraction is upside down" line: %r' % (where, got['text'][:120]))
        joined = ' '.join(got['tex'])
        other = 'i' if unit == 'j' else 'j'
        if ('e^{%s0.927}' % unit) not in joined or re.search(r'(?<![a-z\\])%s(?![a-z])' % other, joined.replace('\\mathrm{Im}', '')):
            fails.append('%s: the working is not in %s: %r' % (where, unit, joined[:160]))
        if got['errors']:
            fails.append('%s: %d KaTeX errors in the card' % (where, got['errors']))
        ctx.close()
    # The back link: in every screen, at every size, clear of the titles and headers; relabelled by site-nav.
    for w, h in ((320, 568), (390, 844), (1366, 768)):
        ctx = ctx_for(w, h)
        page = ctx.new_page()
        page.goto(base + '/games/%s/?level=level4&cb=back' % SLUG, wait_until='load', timeout=20000,
                  referer=base + '/essentials/')
        page.wait_for_function('typeof startMode !== "undefined"', timeout=15000)
        for screen, what in page.evaluate(SCREENS_JS):
            fails.append('back link at %dx%d, %s screen: %s' % (w, h, screen, what))
        label = page.evaluate("() => [document.querySelector('a.back-link').textContent, window.MaffsNav && MaffsNav.backLabel]")
        if label[1] and label[0] != label[1]:
            fails.append('back link at %dx%d: reads %r, site-nav says %r' % (w, h, label[0], label[1]))
        ctx.close()


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            bc.offline(ctx, base)
            if KATEX_DIR:
                ctx.route(lambda url: '/katex@' in url and '/dist/' in url, lambda route: route.fulfill(
                    path=os.path.join(KATEX_DIR, route.request.url.split('/dist/', 1)[1].split('?')[0])))
            else:
                ctx.route(lambda url: bc.is_font_cdn(url), bc.serve_real_font)     # KaTeX from the pinned local copy
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?level=level4&cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof katex !== "undefined"', timeout=15000)
            bank = page.evaluate('() => QUESTIONS.level4')
            check_hints(fails, page.evaluate('() => CALC_HINTS'))
            for qid, pick, what in page.evaluate(SWEEP_JS, RANGE_WORDS):
                fails.append('id %d in Chromium: option %s %s' % (qid, pick, what))
            cards = page.evaluate(CARDS_JS)
            check_why(fails, bank, cards)
            CARDS[:] = cards
            live_why(fails, browser, base, html, page_url)
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            return bank
    finally:
        proc.terminate()
        proc.wait()


# (the item the failure must name, what is planted, today's text, main's text before LISTED-HIGH).
PLANTS = [
    ('id 34 ', 's1-002: -5 + 12j called an impedance',
     'context:"Express this complex number in exponential form."', 'context:"Express this impedance in exponential form."'),
    ('id 19 ', 's1-002: an impedance with a negative real part',
     'context:"This complex number has a negative real part. Find its polar form."', 'context:"This impedance has a negative real part. Find its polar form."'),
    ('id 21 ', 't6-001: 5∠306.87° beside the key 5∠−53.13°',
     'distractors:["5\\\\angle 53.13°","5\\\\angle 126.87°","5\\\\angle -126.87°"]',
     'distractors:["5\\\\angle 53.13°","5\\\\angle 306.87°","5\\\\angle -126.87°"]'),
    ('id 43 ', 'SR-4: two wrong options the same number (0 + 7j beside 7j)',
     'distractors:["7j","0","-7"]', 'distractors:["7j","0 + 7j","-7"]'),
    ('id 15 ', 'SR-4: 3∠π/3 (radians) beside 3∠60°, not listed',
     'distractors:["3\\\\angle 60°","3\\\\angle \\\\pi/6","6\\\\angle 30°"]',
     'distractors:["3\\\\angle 60°","3\\\\angle \\\\pi/6","3\\\\angle \\\\pi/3"]'),
    ('CALC_HINTS id 55', 't6-005: 10tan(4π/3) shown as 1.73, not 17.32',
     'results:["-8.66","5.00","17.32"]', 'results:["-8.66","5.00","1.73"]'),
    ('CALC_HINTS id 34', 't6-005: arctan(12/13) shown as 0.747 rad, not 0.745',
     'results:["0.395 rad","0.745 rad","0.367 rad"]', 'results:["0.395 rad","0.747 rad","0.368 rad"]'),
    ('id 20 ', 'the old positive-angle key 5∠233.13°',
     'correct:"5\\\\angle -126.87°",correctLatex:"5\\\\angle -126.87°"',
     'correct:"5\\\\angle 233.13°",correctLatex:"5\\\\angle 233.13°"'),
    ('id 1 ', 'Why: arctan(Re / Im) for arctan(Im / Re)',
     "\\\\dfrac{' + G.imTex + '}{' + G.reTex + '}\\\\right) = ';", "\\\\dfrac{' + G.reTex + '}{' + G.imTex + '}\\\\right) = ';"),
    ('id 3 ', 'Why: a slip named for an option it does not give',
     "    if (fams.length !== 1) return null;\n", "    if (fams.length !== 1) return fams.length ? null : 'upside';\n"),
    ('back link', 'the back link fixed over the title',
     '.back-link{display:inline-block;margin:8px 16px 4px;', '.back-link{position:fixed;top:16px;left:16px;z-index:200;margin:0;'),
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
    if CARDS:
        kinds, unnamed = why_report(bank, CARDS)
        print('  Why: %d cards, slips named %s; no slip named for %d distractors (ids %s)' % (
            len(CARDS), ', '.join('%s %d' % kv for kv in sorted(kinds.items()) if kv[0] != 'none'),
            kinds.get('none', 0), ' '.join(map(str, unnamed))))
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
