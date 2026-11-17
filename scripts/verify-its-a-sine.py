#!/usr/bin/env python3
# ci-shards: It's a SINE!! (all 120 answers recomputed by coordinate geometry and vector addition, never the sine or cosine rule; every item's rule and version from the pattern of what it gives; the ambiguous items' two triangles and every other sine-angle item's one; no answer within 0.005 of a 1 d.p. boundary; the bank against the saved contract, verbatim; every item marked in every stage by its key only, by dataset.val and MaffsAnswer; the working's angles and numbers; the calculator and the header badge in each mode; every diagram checked against an independent construction for its shape, its exact labels, no overlap and nothing cut off at 360 px; every mode played at every level: one board submission each, on <level>-<mode>; ITS-A-SINE-POLISH: the start picture, the Level 3 bank's two types only, level4_034 in mm, every drawn length's unit from its item, the four worked examples' numbers recomputed (each \ldots a truncation) and drawn, each wrong Stage 2 or 3 step's link to its version's example; fault-injection self-test) | | 1
# ci-deps: games/its-a-sine/ docs/handover/contracts/ docs/history/contracts/
r"""Independent verification for It's a SINE!! / No it's not (games/its-a-sine/), contract SINE-NOT-SINE, 17 Nov 2026, and
contract ITS-A-SINE-POLISH, 17 Nov 2026 (the start picture, the worked examples, the Level 3 bank, level4_034 in mm).
SR-30: checked from its first PR.

WHAT THIS DOES NOT TRUST
-------------------------------------------------------------------------------
The page holds a fixed bank of 120 items (40 a level), each with its "rule", "version" and 1 d.p. "answer", and works its
feedback by the sine and cosine rules. This script never uses either rule. For every item it builds the triangle from what
the item gives, by coordinates (two rays meeting, a circle meeting a line, a point at a bearing) or by adding vectors, and
measures the answer off that construction:

  Bank      each answer, measured, rounded half up to 1 d.p., equals the item's; none lies within 0.005 of a rounding
            boundary. Each item's "rule" and "version" are the ones its given pattern calls for (two angles and a side, or two
            sides and an angle opposite one: sine; two sides and the angle between, or three sides: cosine; a side wanted:
            the side-on-top version, an angle wanted: the rearranged one), where the pattern is read from the triangle the
            context forms (a bearing journey's two legs and the turn between them, two forces drawn nose to tail, ...). An
            "ambiguous" item has two triangles and asks for the obtuse angle; every other sine-angle item has one. Forty items
            a level, ids unique and naming their level, and every item line equal, character for character, to the bank in
            the contract file (docs/handover/contracts/ or, once merged, docs/history/contracts/), an amendment's
            replacement line for an id taking the original's place.
  Marking   in the page, for every item: Stage 1 marks only the rule's button right, Stage 2 only the version's, Stage 3
            only the answer (a value 0.1 out is wrong; the right value to 2 d.p. and an unreadable answer are never marked).
            The Stage 1 key is read by dataset.val: with the two buttons' labels swapped, the key's button is still right.
  Working   the last line is the answer; the line before rounds to it; a third_angle_first item shows the missing angle
            (measured here) before the rule; a bearings item shows the angle at the turn (measured here), a force or phasor
            item 180 degrees minus the angle between, and an ambiguous item both angles whose sine is sin B.
  Modes     the calculator is shown in Stage 3 and All three only; the header badge is the mode's own.
  Diagrams  every drawing is the true shape: its points are a similarity of this script's own construction (every distance
            in proportion, north up for the bearings), and its labels are exactly the given values, the unknown's symbol and
            the names: no derived value (a third angle, the triangle's angle) is ever written. At 360 px no two labels
            overlap and none is outside the drawing.
  Polish    (ITS-A-SINE-POLISH) the start picture right after the title, 1600 x 873 in its tag and in the file. Level 3 is
            exactly 20 cosine-side and 20 sine-angle items (two sides and the angle between; two sides and an angle opposite
            one, one triangle), none with bearings, an ambiguous case or a third angle first. level4_034's prompt is in mm.
            Every drawn length's unit is the item's own unit when it is a length, else the length unit in its prompt, else
            its level's (gcse cm, level3 mm, level4 m; the worked examples cm). The bank's contract lines: SINE-NOT-SINE's,
            then ITS-A-SINE-POLISH's replacement lines by id and its "prompt only" change for level4_034.
  Examples  the four worked examples, A to D, one per version in that order, none in the bank: each measured here off its
            own construction (the side or angle; sin B; b^2 + c^2 - a^2 and a^2; cos A), every value printed before
            \ldots a truncation (never a rounding) of the measured one, the printed answer the measured one to 1 d.p., the
            setup's numbers the item's given values, each drawn (shape and labels as Diagrams) and its KaTeX without errors.
            A wrong Stage 2 or Stage 3 step (alone, or in All three) offers "See the worked example" for its version's
            example (sine-side A, sine-angle B, cosine-side C, cosine-angle D), closed until tapped and drawn when opened;
            a right step and Stage 1 offer none.
  Play      every mode at every level played to the end at 360x640: ten different items, the score the steps right, one
            game_completed and one leaderboard submission on '<level>-<mode>', no sideways scroll.

Work units: "bank" (no browser), "marking", "diagrams 360x640", "examples 360x640", "play 360x640" and "plant: <what>" (one
per planted fault).

    python scripts/verify-its-a-sine.py              # every unit, then the self-test
    python scripts/verify-its-a-sine.py --selftest   # the planted faults only
"""
import argparse
import contextlib
import glob
import json
import math
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402
import plant_common as pc  # noqa: E402

SLUG = 'its-a-sine'
GAME = os.path.join(ROOT, 'games', SLUG, 'index.html')
LEVELS = ['gcse', 'level3', 'level4']
MODES = ['stage-1', 'stage-2', 'stage-3', 'all-three']
CALC = {'stage-1': 'not allowed', 'stage-2': 'not allowed', 'stage-3': 'scientific', 'all-three': 'scientific'}
BADGE = {'not allowed': 'not-allowed', 'scientific': 'scientific'}
CONTRACT = 'sine-not-sine.md'
POLISH = 'its-a-sine-polish.md'
PHONE = (360, 640)


# ---------------------------------------------------------------- the bank, read from the page's source
def bank_of(html):
    """The page's QUESTIONS: every item line, parsed as JSON, keyed by level, with the raw line kept."""
    m = re.search(r'var QUESTIONS = \{\n(.*?)\n  \};', html, re.S)
    if not m:
        raise ValueError('no QUESTIONS block in the page')
    out, level = {}, None
    for ln in m.group(1).split('\n'):
        s = ln.strip()
        h = re.match(r'^([a-z0-9]+): \[$', s)
        if h:
            level = h.group(1)
            out[level] = []
            continue
        if s.startswith('{'):
            raw = s[:-1] if s.endswith(',') else s
            out[level].append((json.loads(raw), raw))
    return out


def contract_file(name):
    for d in ('docs/handover/contracts', 'docs/history/contracts'):
        for f in glob.glob(os.path.join(ROOT, d, '*' + name)):
            return f
    return None


def contract_lines():
    """SINE-NOT-SINE's bank, then ITS-A-SINE-POLISH's: a later line for an id replaces the earlier one, in place (its
    amendments and the new Level 3 alike), and a numbered '<id> prompt only: "..."' line replaces that item's prompt."""
    f, g = contract_file(CONTRACT), contract_file(POLISH)
    if f is None or g is None:
        return None, f or g
    order, latest = [], {}
    for path in (f, g):
        for ln in open(path, encoding='utf-8'):
            if ln.startswith('{"id":'):
                ln = ln.rstrip('\n')
                iid = json.loads(ln)['id']
                if iid not in latest:
                    order.append(iid)
                latest[iid] = ln
    for m in re.finditer(r'^\d+\. ([a-z0-9]+_\d{3}) prompt only: "(.*?)" given', open(g, encoding='utf-8').read(), re.M):
        iid, new = m.group(1), m.group(2)
        old = json.loads(latest[iid])['prompt']
        latest[iid] = latest[iid].replace('"prompt":%s' % json.dumps(old, ensure_ascii=False), '"prompt":%s' % json.dumps(new, ensure_ascii=False))
    return [latest[i] for i in order], g


# The unit of a triangle's lengths (Jon's ruling, 17 Nov 2026): the item's own unit when it is a length; else the length
# unit in its prompt; else its level's.
LEVEL_LENGTH = {'gcse': 'cm', 'level3': 'mm', 'level4': 'm', 'example': 'cm'}


def length_unit(q):
    if q['unit'] in ('mm', 'cm', 'm', 'km'):
        return q['unit']
    m = re.search(r'\d\s*(mm|cm|km|m)\b', q.get('prompt', ''))
    return m.group(1) if m else LEVEL_LENGTH[q['id'].split('_')[0]]


# ---------------------------------------------------------------- independent geometry (no sine rule, no cosine rule)
def V(x, y):
    return (x, y)


def vadd(p, q):
    return (p[0] + q[0], p[1] + q[1])


def vsub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def vmul(p, k):
    return (p[0] * k, p[1] * k)


def norm(p):
    return math.hypot(p[0], p[1])


def ray(deg, r=1.0):
    return (r * math.cos(math.radians(deg)), r * math.sin(math.radians(deg)))


def bear(b, r=1.0):
    return (r * math.sin(math.radians(b)), r * math.cos(math.radians(b)))


def angle_between(u, w):
    return abs(math.degrees(math.atan2(u[0] * w[1] - u[1] * w[0], u[0] * w[0] + u[1] * w[1])))


def meet(p, d, q, e):
    det = d[0] * (-e[1]) - d[1] * (-e[0])
    rx, ry = q[0] - p[0], q[1] - p[1]
    t = (rx * (-e[1]) - ry * (-e[0])) / det
    return vadd(p, vmul(d, t))


def tri_aas(A, B, a):
    """B at the origin, C at (a, 0); A where the ray from B at angle B meets the ray from C at 180 - C."""
    Bp, C = V(0, 0), V(a, 0)
    Ap = meet(Bp, ray(B), C, ray(180 - (180 - A - B)))
    return {'A': Ap, 'B': Bp, 'C': C}


def tri_ssa(a, b, A):
    """A at the origin, C = b at angle A; B on the x-axis (x > 0) with |BC| = a: every such triangle, B's x ascending."""
    C = ray(A, b)
    disc = a * a - C[1] ** 2
    out = []
    if disc >= 0:
        for x in sorted({C[0] - math.sqrt(disc), C[0] + math.sqrt(disc)}):
            if x > 1e-9:
                out.append({'A': V(0, 0), 'B': V(x, 0), 'C': C})
    return out


def tri_sas(b, c, A):
    return {'A': V(0, 0), 'B': V(c, 0), 'C': ray(A, b)}


def tri_sss(a, b, c):
    x = (c * c - b * b + a * a) / (2 * a)
    return {'B': V(0, 0), 'C': V(a, 0), 'A': V(x, math.sqrt(c * c - x * x))}


def ang(T, at, p, q):
    return angle_between(vsub(T[p], T[at]), vsub(T[q], T[at]))


def dist(T, p, q):
    return norm(vsub(T[p], T[q]))


def kind_of(q):
    g = q['given']
    for key, k in (('B_exterior', 'ext'), ('leg1_km', 'bear'), ('AB_km', 'light'), ('angle_between', 'force'),
                   ('phase', 'phasor'), ('crank_mm', 'crank'), ('AB_m', 'survey')):
        if key in g:
            return k
    if 'F1' in g and 'R' in g:
        return 'fdir'
    keys = ','.join(sorted(g))
    frame = q['unit'] == 'm' or (q['unit'] == '°' and 'frame' in q['prompt'])
    return {'A,B,a': 'aas', 'A,a,b': 'ssa', 'A,b,c': 'frame-sas' if frame else 'sas',
            'a,b,c': 'frame-sss' if frame else 'sss'}.get(keys)


def construct(q):
    """(the measured answer, the named points of the construction, facts for the other checks)."""
    g, k, f = q['given'], kind_of(q), {}
    if k in ('aas', 'ext'):
        B = g['B'] if k == 'aas' else 180 - g['B_exterior']
        T = tri_aas(g['A'], B, g['a'])
        f['missing'] = ang(T, 'C', 'A', 'B') if k == 'aas' else B
        if k == 'ext':
            T['E'] = vadd(T['B'], vmul(vsub(T['B'], T['C']), 0.3))
        return dist(T, 'C', 'A') if q['find'] == 'b' else dist(T, 'A', 'B'), T, f
    if k == 'ssa':
        Ts = tri_ssa(g['a'], g['b'], g['A'])
        f['triangles'] = len(Ts)
        f['Bs'] = sorted(ang(T, 'B', 'A', 'C') for T in Ts)
        T = max(Ts, key=lambda t: ang(t, 'B', 'A', 'C')) if q.get('ambiguous') else Ts[0]
        return ang(T, 'B', 'A', 'C'), T, f
    if k in ('sas', 'frame-sas'):
        T = tri_sas(g['b'], g['c'], g['A'])
        return dist(T, 'B', 'C'), T, f
    if k in ('sss', 'frame-sss'):
        T = tri_sss(g['a'], g['b'], g['c'])
        return ang(T, 'A', 'B', 'C'), T, f
    if k == 'bear':
        O = V(0, 0)
        Tp = bear(g['bearing1'], g['leg1_km'])
        E = vadd(Tp, bear(g['bearing2'], g['leg2_km']))
        T = {'O': O, 'T': Tp, 'E': E}
        f['turn'] = ang(T, 'T', 'O', 'E')
        return dist(T, 'O', 'E'), T, f
    if k == 'light':
        A = V(0, 0)
        B = bear(g['bearing_A_to_B'], g['AB_km'])
        L = meet(A, bear(g['bearing_A_to_L']), B, bear(g['bearing_B_to_L']))
        T = {'A': A, 'B': B, 'L': L}
        f['angles'] = (ang(T, 'A', 'B', 'L'), ang(T, 'B', 'A', 'L'), ang(T, 'L', 'A', 'B'))
        f['missing'] = f['angles'][2]
        return dist(T, 'B', 'L'), T, f
    if k in ('force', 'phasor'):
        m1, m2, th = (g['F1'], g['F2'], g['angle_between']) if k == 'force' else (g['V1'], g['V2'], g['phase'])
        A1, A2 = V(m1, 0), ray(th, m2)
        T = {'O': V(0, 0), 'A1': A1, 'A2': A2, 'R': vadd(A1, A2)}
        f['triangle_angle'] = ang(T, 'A1', 'O', 'R')
        return norm(T['R']), T, f
    if k == 'fdir':
        lo, hi = 0.0, 180.0       # the angle between the forces, by bisection on |F1 + F2| = R
        for _ in range(200):
            mid = (lo + hi) / 2
            if norm(vadd(V(g['F1'], 0), ray(mid, g['F2']))) > g['R']:
                lo = mid
            else:
                hi = mid
        A1 = V(g['F1'], 0)
        Q = vadd(A1, ray(lo, g['F2']))
        T = {'O': V(0, 0), 'A1': A1, 'Q': Q}
        return ang(T, 'O', 'A1', 'Q'), T, f
    if k == 'crank':
        P = ray(g['crank_angle'], g['crank_mm'])
        Q = V(P[0] + math.sqrt(g['rod_mm'] ** 2 - P[1] ** 2), 0)
        T = {'O': V(0, 0), 'P': P, 'Q': Q}
        f['acute_only'] = g['rod_mm'] > g['crank_mm']
        return ang(T, 'Q', 'O', 'P'), T, f
    if k == 'survey':
        A, B = V(0, 0), V(g['AB_m'], 0)
        Pm = meet(A, ray(g['angle_A']), B, ray(180 - g['angle_B']))
        T = {'A': A, 'B': B, 'P': Pm}
        f['missing'] = ang(T, 'P', 'A', 'B')
        return dist(T, 'A', 'P'), T, f
    raise ValueError('%s: no construction for its given %s' % (q['id'], sorted(g)))


PATTERN = {'aas': 'AAS', 'ext': 'AAS', 'light': 'AAS', 'survey': 'AAS', 'ssa': 'SSA', 'crank': 'SSA',
           'sas': 'SAS', 'frame-sas': 'SAS', 'bear': 'SAS', 'force': 'SAS', 'phasor': 'SAS',
           'sss': 'SSS', 'frame-sss': 'SSS', 'fdir': 'SSS'}
RULE = {'AAS': 'sine', 'SSA': 'sine', 'SAS': 'cosine', 'SSS': 'cosine'}


def half_up(x):
    return float(Decimal(repr(x)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))


def boundary_gap(x):
    return abs((x * 10) % 1 - 0.5) / 10


def check_bank(html, out, info):
    bank = bank_of(html)
    want, cfile = contract_lines()
    ids, lines = set(), []
    if sorted(bank) != LEVELS:
        out.append('bank levels are %s, not %s' % (sorted(bank), LEVELS))
    for lv in LEVELS:
        items = bank.get(lv, [])
        if len(items) != 40:
            out.append('%s: %d items, not 40' % (lv, len(items)))
        for q, raw in items:
            lines.append(raw)
            if q['id'] in ids:
                out.append('%s: a duplicate id' % q['id'])
            ids.add(q['id'])
            if not q['id'].startswith(lv + '_'):
                out.append('%s: in level %s' % (q['id'], lv))
            k = kind_of(q)
            if k is None:
                out.append('%s: its given pattern %s is none the game knows' % (q['id'], sorted(q['given'])))
                continue
            got, T, f = construct(q)
            if half_up(got) != q['answer']:
                out.append('%s: answer %s, but the construction measures %.4f (%s to 1 d.p.)' % (q['id'], q['answer'], got, half_up(got)))
            if boundary_gap(got) < 0.005:
                out.append('%s: the measured %.5f is within 0.005 of a 1 d.p. boundary' % (q['id'], got))
            rule = RULE[PATTERN[k]]
            if q['rule'] != rule:
                out.append('%s: rule %s, but its pattern (%s) calls for the %s rule' % (q['id'], q['rule'], PATTERN[k], rule))
            version = rule + ('-angle' if q['unit'] == '°' else '-side')
            if q['version'] != version:
                out.append('%s: version %s, but a %s rule finding %s is %s' % (q['id'], q['version'], rule, 'an angle' if q['unit'] == '°' else 'a side', version))
            if k == 'ssa':
                n = f['triangles']
                if q.get('ambiguous'):
                    if n != 2:
                        out.append('%s: marked ambiguous, but the given data make %d triangle(s)' % (q['id'], n))
                    elif 'obtuse' not in q['prompt'] or not max(f['Bs']) > 90:
                        out.append('%s: ambiguous, but the prompt does not ask for the obtuse angle' % q['id'])
                elif n != 1:
                    out.append('%s: a sine-angle item with %d triangles, not marked ambiguous' % (q['id'], n))
                elif not q['given']['b'] < q['given']['a']:
                    out.append('%s: the working says b is shorter than a, and it is not' % q['id'])
            if k == 'crank' and not f['acute_only']:
                out.append('%s: the rod is not longer than the crank, so phi could be obtuse' % q['id'])
            if q.get('ambiguous') and k != 'ssa':
                out.append('%s: marked ambiguous but not a two-sides-and-an-angle item' % q['id'])
            w = q.get('working', {})
            if k == 'bear' and abs(w.get('angle_at_turn', -1) - f['turn']) > 1e-6:
                out.append('%s: working.angle_at_turn %s, measured %.4f' % (q['id'], w.get('angle_at_turn'), f['turn']))
            if k == 'bear' and (q['given']['bearing1'] + 180) - q['given']['bearing2'] != w.get('angle_at_turn'):
                out.append('%s: the working\'s "back bearing minus the second bearing" is not the angle at the turn' % q['id'])
            if k in ('force', 'phasor') and abs(w.get('triangle_angle', -1) - f['triangle_angle']) > 1e-6:
                out.append('%s: working.triangle_angle %s, measured %.4f' % (q['id'], w.get('triangle_angle'), f['triangle_angle']))
            if k == 'light':
                a, b, l = f['angles']
                if any(abs(x - y) > 1e-6 for x, y in zip((a, b, l), (w.get('angle_A'), w.get('angle_B'), w.get('angle_L')))):
                    out.append('%s: working angles %s, measured %.3f %.3f %.3f' % (q['id'], w, a, b, l))
            tf = k in ('ext', 'light', 'survey') or (k == 'aas' and q['find'] == 'c')
            if q['third_angle_first'] != tf:
                out.append('%s: third_angle_first is %s; finding %s from what is given needs it %s' % (q['id'], q['third_angle_first'], q['find'], tf))
    check_polish(html, bank, out)
    if want is None:
        out.append('a contract file (*%s or *%s) is in neither contracts folder' % (CONTRACT, POLISH))
    elif want != lines:
        diff = [i for i in range(max(len(want), len(lines))) if i >= len(want) or i >= len(lines) or want[i] != lines[i]]
        out.append('the page bank differs from the contract (%s) at item %d of %d' % (os.path.relpath(cfile, ROOT), diff[0] + 1, len(want)))
    info['bank'] = len(lines)


# ---------------------------------------------------------------- the page
def open_page(pw, base, html, size):
    br = pw.chromium.launch()
    touch = size[0] <= 600
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch)
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    bc.offline(ctx, base)
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=30000)
    page.wait_for_function('!!window.SNS && !!SNS.ui', timeout=15000)
    page.evaluate("""() => { window.__ev = []; window.__sub = [];
        window.mfg = (n, p) => { window.__ev.push([n, p]); };
        window.MaffsLeaderboard = window.MaffsLeaderboard || {};
        MaffsLeaderboard.submitScore = (g, l, s, n) => { window.__sub.push([g, l, s, n]); return Promise.resolve(); }; }""")
    return br, page, errors


MARK_JS = r"""([mode, id, how, val, swap]) => {
  SNS.ui.preview(mode, id);
  const st = () => SNS.ui.state();
  if (how === 'click') {
    const bs = [...document.querySelectorAll('#opts .opt')];
    if (swap && bs.length === 2) { const t = bs[0].textContent; bs[0].textContent = bs[1].textContent; bs[1].textContent = t; }
    const b = bs.find(x => x.dataset.val === val);
    if (!b) return { err: 'no button with data-val ' + val, vals: bs.map(x => x.dataset.val) };
    b.click();
  } else {
    document.getElementById('ans').value = val;
    document.getElementById('checkBtn').click();
  }
  const fb = document.querySelector('#feedback .fb');
  return { state: st(), why: fb ? fb.dataset.why : null, msg: document.getElementById('msg').dataset.why || null };
}"""


def numbers(s):
    return [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', s)]


def check_marking(page, html, out, info):
    bank = bank_of(html)
    n = 0
    for lv in LEVELS:
        for q, _ in bank[lv]:
            iid = q['id']
            for val in ('sine', 'cosine'):
                r = page.evaluate(MARK_JS, ['stage-1', iid, 'click', val, False])
                want = 'right' if val == q['rule'] else 'wrong'
                if r.get('why') != want:
                    out.append('%s stage 1: %s marked %s, should be %s' % (iid, val, r.get('why') or r, want))
            r = page.evaluate(MARK_JS, ['stage-1', iid, 'click', q['rule'], True])
            if r.get('why') != 'right':
                out.append('%s stage 1: with the labels swapped, the key\'s button (data-val %s) is marked %s: not read by dataset.val' % (iid, q['rule'], r.get('why')))
            for val in ('sine-side', 'sine-angle', 'cosine-side', 'cosine-angle'):
                r = page.evaluate(MARK_JS, ['stage-2', iid, 'click', val, False])
                want = 'right' if val == q['version'] else 'wrong'
                if r.get('why') != want:
                    out.append('%s stage 2: %s marked %s, should be %s' % (iid, val, r.get('why') or r, want))
            a = q['answer']
            for val, want in (('%.1f' % a, 'right'), ('%.1f' % (a + 0.1), 'wrong'), ('%.1f' % (a - 0.1), 'wrong')):
                r = page.evaluate(MARK_JS, ['stage-3', iid, 'type', val, False])
                if r.get('why') != want:
                    out.append('%s stage 3: %s marked %s, should be %s' % (iid, val, r.get('why') or r, want))
            for val, want in (('%.2f' % (a + 0.04), 'format'), ('twelve', 'unreadable')):
                r = page.evaluate(MARK_JS, ['stage-3', iid, 'type', val, False])
                if r.get('state') != 'asking' or r.get('msg') != want:
                    out.append('%s stage 3: %r should not be marked (%s message); got state %s, message %s' % (iid, val, want, r.get('state'), r.get('msg')))
            check_working(q, page.evaluate('(id) => SNS.working(id)', iid), out)
            n += 1
    info['marked'] = n
    for m in MODES:
        page.evaluate('(m) => { SNS.ui.setLevel("gcse"); SNS.ui.start(m); }', m)
        shown = page.evaluate('SNS.ui.calcShown()')
        if shown != (CALC[m] == 'scientific'):
            out.append('%s: the calculator is %s' % (m, 'shown' if shown else 'not shown'))
        badge = page.evaluate("[document.getElementById('calcBadge').getAttribute('data-calc'), document.getElementById('calcBadge').textContent]")
        if badge[0] != BADGE[CALC[m]]:
            out.append('%s: the header badge is %s, not %s' % (m, badge, BADGE[CALC[m]]))
        page.evaluate("document.getElementById('menuBtn').click()")


def check_working(q, W, out):
    iid, k, g = q['id'], kind_of(q), q['given']
    _, T, f = construct(q)
    if not W or '1 d.p.' not in W[-1] or ('%.1f' % q['answer']) not in W[-1]:
        out.append('%s working: the last line does not give %.1f' % (iid, q['answer']))
        return
    pre = numbers(W[-2].rsplit('\\ldots', 1)[0]) if '\\ldots' in W[-2] else []
    if not pre or half_up(pre[-1]) != q['answer']:
        out.append('%s working: the value before the last line (%s) does not round to %.1f' % (iid, pre[-1:] or W[-2][:60], q['answer']))
    if q['third_angle_first']:
        m = round(f['missing'], 6)
        first = [i for i, w in enumerate(W) if '180^\\circ -' in w and (' = %g^\\circ' % m) in w]
        rule_line = [i for i, w in enumerate(W) if '\\sin' in w]
        if not first or not rule_line or first[0] > rule_line[0]:
            out.append('%s working: the missing angle (%g) is not shown before the sine rule' % (iid, m))
    if k == 'bear' and not any(('= %g^\\circ' % round(f['turn'], 6)) in w for w in W[:1]):
        out.append('%s working: the first line does not give the angle at the turn (%g)' % (iid, f['turn']))
    if k in ('force', 'phasor'):
        th = g['angle_between'] if k == 'force' else g['phase']
        if ('180^\\circ - %d^\\circ = %g^\\circ' % (th, round(f['triangle_angle'], 6))) not in W[0]:
            out.append('%s working: the first line does not give the triangle\'s angle as 180 - %d = %g' % (iid, th, f['triangle_angle']))
    if q.get('ambiguous'):
        acute, obtuse = f['Bs'][0], f['Bs'][1]
        txt = ' '.join(W)
        if ('%.3f' % acute) not in txt or ('%.3f' % obtuse) not in txt or 'obtuse' not in txt:
            out.append('%s working: does not show both angles (%.3f and %.3f) and the obtuse choice' % (iid, acute, obtuse))


# ---------------------------------------------------------------- diagrams
DRAW_JS = r"""(id) => {
  let host = document.getElementById('__vfig');
  if (!host) { host = document.createElement('div'); host.id = '__vfig'; host.className = 'fig'; host.style.width = '336px';
    document.getElementById('menu').prepend(host); }
  const d = SNS.drawInto(host, id), svg = host.querySelector('svg'), vb = svg.viewBox.baseVal;
  const texts = [...svg.querySelectorAll('text')].map(t => { const b = t.getBBox(); return { s: t.textContent, x: b.x, y: b.y, w: b.width, h: b.height }; });
  return { pts: d.pts, vb: [vb.x, vb.y, vb.width, vb.height], texts, width: host.getBoundingClientRect().width,
           svgw: svg.getBoundingClientRect().width };
}"""

POINTS = {'aas': 'ABC', 'ext': 'ABC', 'ssa': 'ABC', 'sas': 'ABC', 'sss': 'ABC', 'frame-sas': 'ABC', 'frame-sss': 'ABC',
          'bear': ['O', 'T', 'E'], 'light': 'ABL', 'force': ['O', 'A1', 'A2', 'R'], 'phasor': ['O', 'A1', 'A2', 'R'],
          'fdir': ['O', 'A1', 'Q'], 'crank': 'OPQ', 'survey': 'ABP'}


def webp_size(path):
    """(width, height) from a WebP file's own header (VP8, VP8L or VP8X), without an image library."""
    b = open(path, 'rb').read(64)
    if b[:4] != b'RIFF' or b[8:12] != b'WEBP':
        return None
    kind = b[12:16]
    if kind == b'VP8 ':
        return int.from_bytes(b[26:28], 'little') & 0x3FFF, int.from_bytes(b[28:30], 'little') & 0x3FFF
    if kind == b'VP8L':
        v = int.from_bytes(b[21:25], 'little')
        return (v & 0x3FFF) + 1, ((v >> 14) & 0x3FFF) + 1
    if kind == b'VP8X':
        return int.from_bytes(b[24:27], 'little') + 1, int.from_bytes(b[27:30], 'little') + 1
    return None


def check_polish(html, bank, out):
    # The start picture: right after the title's header in #menu, its size in the tag, the file that size.
    img = re.search(r'<div id="menu" class="screen active">\s*<div class="header">.*?</div>\s*(<img class="start-art"[^>]*>)', html, re.S)
    if not img:
        out.append('start picture: no img.start-art straight after the start screen\'s header')
    else:
        tag = img.group(1)
        for attr in ('src="assets/start.webp"', 'width="1600"', 'height="873"', 'alt="'):
            if attr not in tag:
                out.append('start picture: the tag has no %s' % attr)
    f = os.path.join(ROOT, 'games', SLUG, 'assets', 'start.webp')
    size = webp_size(f) if os.path.exists(f) else None
    if size != (1600, 873):
        out.append('start picture: assets/start.webp is %s, not 1600 x 873' % (size,))
    # Level 3: the assessment's two types only.
    l3 = [q for q, _ in bank.get('level3', [])]
    versions = [q['version'] for q in l3]
    if versions.count('cosine-side') != 20 or versions.count('sine-angle') != 20:
        out.append('level3: %d cosine-side and %d sine-angle items, not 20 and 20' % (versions.count('cosine-side'), versions.count('sine-angle')))
    for q in l3:
        k = kind_of(q)
        if k not in ('sas', 'ssa') or q.get('ambiguous') or q['third_angle_first'] or any('bearing' in x for x in q['given']):
            out.append('%s: not one of Level 3\'s two types (kind %s, ambiguous %s, third_angle_first %s)' % (q['id'], k, bool(q.get('ambiguous')), q['third_angle_first']))
        elif k == 'ssa' and construct(q)[2]['triangles'] != 1:
            out.append('%s: a sine-angle item with more than one triangle' % q['id'])
        if length_unit(q) != 'mm':
            out.append('%s: its lengths are in %s, not mm' % (q['id'], length_unit(q)))
    q34 = [q for q, _ in bank.get('level4', []) if q['id'] == 'level4_034']
    if not q34 or not re.search(r'380 mm and 520 mm .* 450 mm', q34[0]['prompt']) or length_unit(q34[0]) != 'mm':
        out.append('level4_034: its prompt and drawing are not in mm (%s)' % (q34[0]['prompt'] if q34 else 'missing'))


def b3(b):
    return '%03d°' % b


def expected_labels(q):
    g, k, lu = q['given'], kind_of(q), length_unit(q)
    if k in ('aas', 'ext', 'ssa', 'sas', 'sss'):
        L = ['A', 'B', 'C']
        for s in 'abc':
            L.append('%s = %s %s' % (s, g[s], lu) if s in g else ('%s = x' % s if q['find'] == s else s))
        for a in 'ABC':
            if a in g:
                L.append('%s°' % g[a])
            elif q['find'] == a:
                L.append('θ')
        if k == 'ext':
            L.append('%s°' % g['B_exterior'])
        return L
    if k in ('frame-sas', 'frame-sss'):
        L = ['A']
        for s in 'abc':
            if s in g:
                L.append('%s %s' % (g[s], lu))
            elif q['find'] == s:
                L.append('x')
        L.append('%s°' % g['A'] if 'A' in g else 'θ')
        return L
    if k == 'bear':
        return ['N', 'N', 'N', 'Start', '%s km' % g['leg1_km'], '%s km' % g['leg2_km'], 'x', b3(g['bearing1']), b3(g['bearing2'])]
    if k == 'light':
        return ['N', 'N', 'A', 'B', 'L', '%s km' % g['AB_km'], 'x', b3(g['bearing_A_to_L']), b3(g['bearing_A_to_B']), b3(g['bearing_B_to_L'])]
    if k in ('force', 'phasor'):
        m1, m2, th, un = (g['F1'], g['F2'], g['angle_between'], 'N') if k == 'force' else (g['V1'], g['V2'], g['phase'], 'V')
        return ['%s %s' % (m1, un), '%s %s' % (m2, un), '%s°' % th, '?']
    if k == 'fdir':
        return ['%s N' % g['F1'], '%s N' % g['F2'], 'R = %s N' % g['R'], 'α']
    if k == 'crank':
        return ['%s mm' % g['crank_mm'], '%s mm' % g['rod_mm'], '%s°' % g['crank_angle'], 'φ', 'line of stroke']
    if k == 'survey':
        return ['A', 'B', 'P (mast)', '%s m' % g['AB_m'], '%s°' % g['angle_A'], '%s°' % g['angle_B'], 'x']
    return []


def check_diagrams(page, html, out, info):
    bank = bank_of(html)
    n = 0
    bank['example'] = [(x['item'], None) for x in page.evaluate('SNS.examples()')]
    for lv in LEVELS + ['example']:
        for q, _ in bank[lv]:
            iid, k = q['id'], kind_of(q)
            d = page.evaluate(DRAW_JS, iid)
            _, T, _ = construct(q)
            names = list(POINTS[k])
            # The drawn points are a similarity of the construction: every distance in the same proportion.
            pairs = [(a, b) for i, a in enumerate(names) for b in names[i + 1:]]
            ratios = []
            for a, b in pairs:
                w = dist(T, a, b)
                s = math.hypot(d['pts'][a][0] - d['pts'][b][0], d['pts'][a][1] - d['pts'][b][1])
                ratios.append(s / w)
            if max(ratios) / min(ratios) > 1.002:
                out.append('%s diagram: not to shape (distance ratios %.4f to %.4f)' % (iid, min(ratios), max(ratios)))
            if k in ('bear', 'light'):     # north up: each leg's drawn bearing is its given bearing
                legs = [('O', 'T', q['given']['bearing1']), ('T', 'E', q['given']['bearing2'])] if k == 'bear' else \
                    [('A', 'B', q['given']['bearing_A_to_B']), ('A', 'L', q['given']['bearing_A_to_L']), ('B', 'L', q['given']['bearing_B_to_L'])]
                for a, b, want in legs:
                    dx, dy = d['pts'][b][0] - d['pts'][a][0], d['pts'][b][1] - d['pts'][a][1]
                    got = math.degrees(math.atan2(dx, -dy)) % 360
                    if abs((got - want + 180) % 360 - 180) > 0.05:
                        out.append('%s diagram: %s to %s drawn on a bearing of %.2f, not %s' % (iid, a, b, got, want))
            labels = sorted(t['s'] for t in d['texts'])
            want = sorted(expected_labels(q))
            if labels != want:
                out.append('%s diagram: labels %s, should be exactly %s' % (iid, labels, want))
            vx, vy, vw, vh = d['vb']
            ts = d['texts']
            for t in ts:
                if t['x'] < vx - 0.5 or t['y'] < vy - 0.5 or t['x'] + t['w'] > vx + vw + 0.5 or t['y'] + t['h'] > vy + vh + 0.5:
                    out.append('%s diagram: the label %r is outside the drawing' % (iid, t['s']))
            for i in range(len(ts)):
                for j in range(i + 1, len(ts)):
                    a, b = ts[i], ts[j]
                    ox = min(a['x'] + a['w'], b['x'] + b['w']) - max(a['x'], b['x'])
                    oy = min(a['y'] + a['h'], b['y'] + b['h']) - max(a['y'], b['y'])
                    if ox > 0.5 and oy > 0.5:
                        out.append('%s diagram: labels %r and %r overlap' % (iid, a['s'], b['s']))
            if d['svgw'] > d['width'] + 0.5:
                out.append('%s diagram: %.0f px wide in a %.0f px box' % (iid, d['svgw'], d['width']))
            n += 1
    info['diagrams'] = n


# ---------------------------------------------------------------- the worked examples (ITS-A-SINE-POLISH)
EXAMPLE_ORDER = [('A', 'sine-side'), ('B', 'sine-angle'), ('C', 'cosine-side'), ('D', 'cosine-angle')]


def trunc(x, dp):
    return math.floor(x * 10 ** dp + 1e-9) / 10 ** dp


def example_truths(x):
    """The values the example's working writes before \\ldots, in order, each measured off this script's construction."""
    q, g = x['item'], x['item']['given']
    got, T, _ = construct(q)
    if x['letter'] == 'A':
        return got, [dist(T, 'C', 'A')]
    if x['letter'] == 'B':
        return got, [math.sin(math.radians(ang(T, 'B', 'A', 'C')))]
    if x['letter'] == 'C':
        a2 = dist(T, 'B', 'C') ** 2
        return got, [g['b'] ** 2 + g['c'] ** 2 - a2, a2]
    return got, [math.cos(math.radians(ang(T, 'A', 'B', 'C')))]


LINK_JS = r"""async ([mode, id, wrongAt]) => {
  const tick = () => new Promise(r => setTimeout(r, 30));   // the panel draws on its toggle event, a task later
  SNS.ui.preview(mode, id);
  const seen = [];
  for (let k = 0; k < 6 && SNS.ui.state() === 'asking'; k++) {
    const s = SNS.ui.step();
    SNS.ui.answer(s !== wrongAt);
    const d = document.querySelector('#feedback .fb details.we');
    seen.push({ step: s, right: s !== wrongAt, link: d ? d.dataset.example : null, open: d ? d.open : null,
                text: d ? d.querySelector('summary').textContent : null });
    if (d) {
      d.querySelector('summary').click();
      await tick();
      seen[seen.length - 1].opened = d.open;
      seen[seen.length - 1].drawn = !!d.querySelector('.we-fig svg');
      seen[seen.length - 1].work = d.querySelector('.we-work').textContent;
    }
    SNS.ui.next();
  }
  return seen;
}"""


def check_examples(page, html, out, info):
    bank = bank_of(html)
    xs = page.evaluate('SNS.examples()')
    if [(x['letter'], x['version']) for x in xs] != EXAMPLE_ORDER:
        out.append('examples: %s, not A to D one per version in order' % [(x['letter'], x['version']) for x in xs])
    givens = [q['given'] for lv in LEVELS for q, _ in bank[lv]]
    for x in xs:
        q, L = x['item'], x['letter']
        k = kind_of(q)
        if k is None or RULE[PATTERN[k]] + ('-angle' if q['unit'] == '°' else '-side') != x['version']:
            out.append('example %s: its triangle (%s) is not a %s item' % (L, k, x['version']))
            continue
        if q['given'] in givens:
            out.append('example %s: its triangle is in the bank' % L)
        if sorted(numbers(x['setup'])) != sorted(float(v) for v in q['given'].values()):
            out.append('example %s: the setup %r does not give %s' % (L, x['setup'], q['given']))
        got, truths = example_truths(x)
        if '%.1f' % half_up(got) != x['answer']:
            out.append('example %s: answer %s, but the construction measures %.4f (%.1f)' % (L, x['answer'], got, half_up(got)))
        nums = re.findall(r'(-?\d+\.\d+)\\ldots', x['work'])
        if len(nums) != len(truths):
            out.append('example %s: %d values before \\ldots, expected %d' % (L, len(nums), len(truths)))
        for txt, t in zip(nums, truths):
            dp = len(txt.split('.')[1])
            if float(txt) != trunc(t, dp):
                out.append('example %s: %s\\ldots is not %.8f cut to %d d.p. (%s)' % (L, txt, t, dp, ('%.' + str(dp) + 'f') % trunc(t, dp)))
        last = numbers(x['work'])[-1:]
        if not last or '%.1f' % last[0] != x['answer']:
            out.append('example %s: the working ends on %s, not the answer %s' % (L, last, x['answer']))
        g = q['given']
        if L == 'C' and ('= %d - ' % (g['b'] ** 2 + g['c'] ** 2)) not in x['work']:
            out.append('example C: b^2 + c^2 is not written as %d' % (g['b'] ** 2 + g['c'] ** 2))
        if L == 'D' and ('\\frac{%d}{%d}' % (g['b'] ** 2 + g['c'] ** 2 - g['a'] ** 2, 2 * g['b'] * g['c'])) not in x['work']:
            out.append('example D: the fraction is not %d/%d' % (g['b'] ** 2 + g['c'] ** 2 - g['a'] ** 2, 2 * g['b'] * g['c']))
    # On the start screen: four closed panels, A to D; each drawn when opened, its labels exact, its KaTeX clean.
    page.evaluate("document.getElementById('menuBtn').click()")
    menu = page.evaluate("""async () => { const out = [];
        for (const d of document.querySelectorAll('#examples details.we')) {
          const was = d.open; d.querySelector('summary').click();
          await new Promise(r => setTimeout(r, 30));   // drawn on the toggle event, a task later
          out.push({ l: d.dataset.example, closed: !was, open: d.open, labels: [...d.querySelectorAll('.we-fig svg text')].map(t => t.textContent),
                     kerr: d.querySelectorAll('.katex-error').length, katex: d.querySelectorAll('.katex').length }); }
        return out; }""")
    if [m['l'] for m in menu] != [l for l, _ in EXAMPLE_ORDER]:
        out.append('examples on the start screen: %s, not A to D' % [m['l'] for m in menu])
    kx = page.evaluate('!!window.katex')
    for m, x in zip(menu, xs):
        if not m['closed'] or not m['open']:
            out.append('example %s on the start screen: not closed until tapped, then open' % m['l'])
        if sorted(m['labels']) != sorted(expected_labels(x['item'])):
            out.append('example %s on the start screen: labels %s, should be %s' % (m['l'], m['labels'], expected_labels(x['item'])))
        if m['kerr'] or (kx and m['katex'] < 3):
            out.append('example %s: KaTeX errors %d, KaTeX pieces %d' % (m['l'], m['kerr'], m['katex']))
    # The links: a wrong Stage 2 or 3 step offers its version's example; a right step and Stage 1 offer none.
    by_letter = {x['letter']: x for x in xs}
    for version, letter in [(v, l) for l, v in EXAMPLE_ORDER]:
        q = next(q for q, _ in bank['gcse'] if q['version'] == version)
        for mode, wrong_at in (('stage-1', 1), ('stage-2', 2), ('stage-3', 3), ('all-three', 2), ('all-three', 3), ('stage-2', 0), ('stage-3', 0)):
            for r in page.evaluate(LINK_JS, [mode, q['id'], wrong_at]):
                tag = '%s %s step %d (%s)' % (q['id'], mode, r['step'], 'right' if r['right'] else 'wrong')
                if r['right'] or r['step'] == 1:
                    if r['link']:
                        out.append('%s: offers worked example %s, should offer none' % (tag, r['link']))
                    continue
                if r['link'] != letter:
                    out.append('link: %s, a %s item, opens example %s, not %s' % (tag, version, r['link'], letter))
                    continue
                if r['open'] or not r['opened'] or not r['drawn'] or r['text'] != 'See the worked example':
                    out.append('%s: the link is %r, open before tapping %s, open after %s, drawn %s' % (tag, r['text'], r['open'], r.get('opened'), r.get('drawn')))
                ref = page.evaluate("(L) => { const d = document.querySelector('#examples details.we[data-example=\"' + L + '\"]'); return d ? d.querySelector('.we-work').textContent : null; }", letter)
                if r.get('work') != ref:
                    out.append('%s: the panel\'s working is not example %s\'s' % (tag, letter))
        page.evaluate("document.getElementById('menuBtn').click()")
    info['examples'] = len(xs)


# ---------------------------------------------------------------- play
def play(page, lv, m, out):
    page.evaluate('() => { window.__ev = []; window.__sub = []; }')
    page.evaluate('([l, m]) => { SNS.ui.setLevel(l); SNS.ui.start(m); }', [lv, m])
    seen, right, k = [], 0, 0
    for _ in range(200):
        st = page.evaluate('SNS.ui.state()')
        if st == 'over':
            break
        if st == 'asking':
            q = page.evaluate('SNS.ui.question().id')
            if not seen or seen[-1] != q:
                seen.append(q)
            ok = k % 3 != 1
            page.evaluate('(r) => SNS.ui.answer(r)', ok)
            right += 1 if ok else 0
            k += 1
        else:
            page.evaluate('SNS.ui.next()')
    tag = '%s %s' % (lv, m)
    if page.evaluate('SNS.ui.state()') != 'over':
        out.append('%s: the run did not finish' % tag)
        return
    steps = 3 if m == 'all-three' else 1
    if len(seen) != 10 or len(set(seen)) != 10 or any(not s.startswith(lv + '_') for s in seen):
        out.append('%s: the run served %s, not ten different %s items' % (tag, seen, lv))
    if k != 10 * steps:
        out.append('%s: %d steps asked, not %d' % (tag, k, 10 * steps))
    ev = page.evaluate('window.__ev')
    sub = page.evaluate('window.__sub')
    done = [p for n, p in ev if n == 'game_completed']
    if len(done) != 1 or done[0].get('score') != right or done[0].get('level') != lv or done[0].get('mode') != m:
        out.append('%s: game_completed %s, expected one with score %d' % (tag, done, right))
    if sub != [[SLUG, '%s-%s' % (lv, m), right, 10]]:
        out.append('%s: the leaderboard got %s, expected one submission on %s-%s with %d' % (tag, sub, lv, m, right))
    if page.evaluate('document.documentElement.scrollWidth') > PHONE[0]:
        out.append('%s: the page scrolls sideways at %d px' % (tag, PHONE[0]))
    qa = [p for n, p in ev if n == 'question_answered']
    if len(qa) != 10 or any(not p.get('question_id') for p in qa):
        out.append('%s: %d question_answered events, each needs a question_id' % (tag, len(qa)))
    page.evaluate("document.getElementById('menuBtn').click()")


def check(html, out, units, shard=None):
    unit = shard.unit if shard is not None else (lambda uid: contextlib.nullcontext())
    info = {}
    if 'bank' in units:
        with unit('bank'):
            try:
                check_bank(html, out, info)
            except Exception as e:  # noqa: BLE001
                out.append('the bank checks threw: %s' % str(e).splitlines()[0][:200])
    browser = [u for u in units if u != 'bank']
    if not browser:
        return info
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            for uid in browser:
                with unit(uid):
                    size = PHONE if ' ' in uid else (1280, 800)
                    br, page, errs = open_page(pw, base, html, size)
                    try:
                        if uid == 'marking':
                            check_marking(page, html, out, info)
                        elif uid.startswith('diagrams'):
                            check_diagrams(page, html, out, info)
                        elif uid.startswith('examples'):
                            check_examples(page, html, out, info)
                        else:
                            for lv in LEVELS:
                                for m in MODES:
                                    play(page, lv, m, out)
                            info['played'] = len(LEVELS) * len(MODES)
                    except Exception as e:  # noqa: BLE001
                        out.append('%s threw: %s' % (uid, str(e).splitlines()[0][:220]))
                    out.extend('page error (%s): %s' % (uid, e) for e in errs if 'production host' not in e)
                    br.close()
    finally:
        proc.terminate()
    return info


# Each plant: (what, [(old, new)], the unit it needs, the pattern its finding must match). The five the contract names.
PLANTS = [
    ('an answer 0.1 out', [('"find":"b","answer":11.3,"unit":"cm"', '"find":"b","answer":11.4,"unit":"cm"')], 'bank', r'gcse_001: answer 11.4'),
    ('a rule swapped', [('{"id":"gcse_025","rule":"cosine"', '{"id":"gcse_025","rule":"sine"')], 'bank', r'gcse_025: rule sine'),
    ('a version swapped', [('{"id":"gcse_033","rule":"cosine","version":"cosine-angle"', '{"id":"gcse_033","rule":"cosine","version":"cosine-side"')], 'bank', r'gcse_033: version'),
    ('an ambiguous item with only one solution', [('"find":"B","answer":42.4,"unit":"°","prompt":"Find angle B, to 1 d.p."}',
                                                  '"find":"B","answer":42.4,"unit":"°","prompt":"Angle B is obtuse. Find angle B, to 1 d.p.","ambiguous":true}')],
     'bank', r'gcse_017: marked ambiguous, but the given data make 1 triangle'),
    ('a stage-1 key read from the rendered HTML, not dataset.val',
     [("settle(b.dataset.val === keyOf(step()), b.dataset.val);",
       "settle((/SINE/.test(b.textContent) ? 'sine' : /not/.test(b.textContent) ? 'cosine' : b.dataset.val) === keyOf(step()), b.dataset.val);")],
     'marking', r'labels swapped'),
    # ITS-A-SINE-POLISH
    ('a worked example\'s answer 0.1 out', [("= 12.3\\\\text{ cm}\\\\).',", "= 12.4\\\\text{ cm}\\\\).',"), ("answer: '12.3',", "answer: '12.4',")],
     'examples 360x640', r'example A: answer 12.4'),
    ('a worked example\'s value rounded, not cut', [("= 12.266\\\\ldots", "= 12.267\\\\ldots")], 'examples 360x640', r'example A: 12.267'),
    ('a feedback link opening the wrong example', [("'sine-angle': 'B', 'cosine-side'", "'sine-angle': 'A', 'cosine-side'")],
     'examples 360x640', r'link: gcse_\d+ stage-2 step 2 \(wrong\), a sine-angle item, opens example A'),
    ('the start picture without its height', [(' width="1600" height="873" alt="A building site with roof', ' width="1600" alt="A building site with roof')],
     'bank', r'start picture: the tag has no height'),
    ('level4_034 back in metres', [('members of 380 mm and 520 mm meeting at joint A, and a member of 450 mm', 'members of 380 m and 520 m meeting at joint A, and a member of 450 m')],
     'bank', r'level4_034: its prompt and drawing are not in mm'),
    ('a drawn length in a fixed unit', [("    var u = lengthUnit(q);", "    var u = 'cm';")], 'diagrams 360x640', r'level3_001 diagram: labels'),
]


def selftest(html, plants=None, shard=None):
    ok = True
    for what, edits, unit_id, want in (PLANTS if plants is None else plants):
        with (shard.unit('plant: ' + what) if shard is not None else contextlib.nullcontext()):
            try:
                src = html
                for old, new in edits:
                    src = pc.apply_plant(src, old, new, name=what)
            except pc.StalePlant as e:
                print('  self-test %-62s *** %s ***' % (what, e))
                ok = False
                continue
            got, err = [], None
            try:
                check(src, got, [unit_id])
            except Exception as e:  # noqa: BLE001
                err = e
            hit = [g for g in got if re.search(want, g)]
            caught = pc.is_caught(hit, err)
            print('  self-test %-62s %s' % (what, ('caught: ' + hit[0][:90]) if caught else '*** MISSED ***' + (' (other: %s)' % got[0][:90] if got else '') + (' (error: %s)' % err if err else '')))
            ok = caught and ok
    return ok


def main():
    ap = argparse.ArgumentParser()
    bc.shard_args(ap)
    ap.add_argument('--selftest', action='store_true', help='the planted faults only')
    args = ap.parse_args()
    shard = bc.Shard(__file__, args)
    units = ['bank', 'marking', 'diagrams %dx%d' % PHONE, 'examples %dx%d' % PHONE, 'play %dx%d' % PHONE]
    if args.selftest:
        units = []
    mine = shard.pick(units + ['plant: ' + p[0] for p in PLANTS])
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    html = open(GAME, encoding='utf-8').read()
    out = []
    run = [u for u in units if u in mine]
    info = check(html, out, run, shard) if run else {}
    if 'bank' in info:
        print('%s: %d items, every answer measured off its own construction, rule, version and ambiguity from the given pattern' % (SLUG, info['bank']))
    if 'marked' in info:
        print('%s: %d items marked in every stage (stage 1 two choices and a label swap, stage 2 four, stage 3 five answers); working checked' % (SLUG, info['marked']))
    if 'diagrams' in info:
        print('%s: %d diagrams to shape, labelled exactly, no overlap at %dx%d' % (SLUG, info['diagrams'], PHONE[0], PHONE[1]))
    if 'examples' in info:
        print('%s: %d worked examples recomputed (each \\ldots a truncation), drawn, and linked from every wrong Stage 2 and 3 step' % (SLUG, info['examples']))
    if 'played' in info:
        print('%s: %d runs played (every mode at every level)' % (SLUG, info['played']))
    ok = selftest(html, [p for p in PLANTS if 'plant: ' + p[0] in mine], shard)
    for f in out[:80]:
        print('FAIL  ' + f)
    if len(out) > 80:
        print('FAIL  ... and %d more' % (len(out) - 80))
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if out or not ok else 'PASS')
    return 1 if out or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
