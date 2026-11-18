#!/usr/bin/env python3
# ci-shards: I Dropped My Ice Cream (all 96 answers and every trap recomputed from "given" with exact decimals, 40-digit pi, half up to 1 d.p.; no answer within 0.005 of a 1 d.p. boundary; early rounding never the answer; every trap off its answer and its box's other traps; 48 items a level, 12 a stage, ids unique, no repeated given, none of Jon's assessment numbers, every stage-4 prompt "solid"; the bank, Jon's lines, tagline and picture against the saved contract, verbatim; every box marked by its answer only, box (b) from full accuracy and never from the student's (a), every trap showing Jon's line; the working's cut values; the formula panel by level and stage; the calculator on every stage; every diagram from its given values, the cone to its true proportion, the height's label clear of both slant edges, labels exact, no overlap and nothing cut off at 360 px; every stage at both levels played: one board submission each, on <level>-<mode>; fault-injection self-test) | | 1
# ci-deps: games/i-dropped-my-ice-cream/ docs/handover/contracts/ docs/history/contracts/
r"""Independent verification for I Dropped My Ice Cream (games/i-dropped-my-ice-cream/), contract I-DROPPED-MY-ICE-CREAM,
18 Nov 2026. SR-30: checked from its first PR.

WHAT THIS DOES NOT TRUST
-------------------------------------------------------------------------------
The page holds a fixed bank of 96 items (48 a level, 12 a stage), each with its 1 d.p. "answers" and the 1 d.p. value of each
named mistake ("traps"). This script recomputes every one from the item's "given" with Python's Decimal (pi to 40 digits,
rounded half up), never from the page's numbers:

  Bank      r = C / 2pi, A = pi r^2 (from the unrounded r); for a cone r = d / 2, V = pi r^2 h / 3, l = sqrt(r^2 + h^2) and
            A = pi r^2 + pi r l (from the unrounded l). Traps: r.diameter C / pi; A.early_rounding pi (r to 1 d.p.)^2 or pi r^2 +
            pi r (l to 1 d.p.); V.diameter pi d^2 h / 3; V.no_third pi r^2 h; l.diameter sqrt(d^2 + h^2); A.curved_only pi r l.
            Each equals the item's to 1 d.p.; no answer within 0.005 of a rounding boundary; early_rounding is not the answer;
            every trap differs from its answer and from its box's other traps. 48 items a level, 12 a stage; ids unique and
            naming their level; no "given" twice in a level; none of Jon's assessment numbers (C = 220; d = 120; d, h = 120,
            180); every stage-4 prompt says "solid" (a given is its values with their unit, Amendment 2); every prompt states its given values in its unit. Every item line
            equals, character for character, its line in the contract file (docs/handover/contracts/ or, once merged,
            docs/history/contracts/).
  Start     the title, Jon's tagline (from the contract) under it, the picture right after the header, 1600 x 873 in its
            tag and in the file, with the contract's alt text.
  Marking   in the page, for every item and every box: the answer to 1 d.p. is right; 0.1 either side is wrong; the right
            value to 2 d.p. and an unreadable answer are never marked; each trap value is wrong and shows Jon's line for
            that trap (his lines read from the contract, never from the page), and a wrong non-trap value shows no line;
            every wrong answer shows the answer. Box (b) is right after a wrong (a) and wrong when worked from the rounded
            (a): it is marked against the bank's full-accuracy answer, never the student's own (a).
  Working   every value written before "\ldots" is the exact value cut (never rounded) to 4 d.p.: r (and A) for a circle; V;
            l (and A, from the unrounded l) for a cone; r = d / 2 written exactly; the last line the answer to 1 d.p.
  Formulas  no panel in GCSE Stages 1 and 2, and no circle formula anywhere on the card before it is answered; the cone's
            formulas in GCSE Stages 3 and 4; every stage's at Level 3 (C and A; C, A; V; l and A).
  Modes     the scientific calculator mounted and shown on every stage.
  Diagrams  every item drawn as the game draws it, at 360 x 640: a circle with exactly "C = <C> <unit>" and "r = ?" (and
            "A = ?" in Stage 2); a cone with exactly "h = <h> <unit>" and "diameter = <d> <unit>" (and "l = ?" in Stage 4),
            its drawn base width over its height equal to d / h (to 0.5%); the height's label clear of both slant edges; no
            two labels overlapping; nothing outside the drawing; no sideways scroll.
  Play      every stage at both levels played to the end at 360 x 640: eight different items of that level and stage, every
            box asked, the score the boxes right, one game_completed, one leaderboard submission on '<level>-<mode>'.

Work units: "bank" (no browser), "marking", "diagrams 360x640", "play 360x640" and "plant: <what>" (one per planted fault).

    python scripts/verify-i-dropped-my-ice-cream.py              # every unit, then the self-test
    python scripts/verify-i-dropped-my-ice-cream.py --selftest   # the planted faults only
"""
import argparse
import contextlib
import glob
import json
import os
import re
import struct
import sys
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN, getcontext

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402
import plant_common as pc  # noqa: E402

getcontext().prec = 60
PI = Decimal('3.141592653589793238462643383279502884197')
SLUG = 'i-dropped-my-ice-cream'
GAME = os.path.join(ROOT, 'games', SLUG, 'index.html')
PICTURE = os.path.join(ROOT, 'games', SLUG, 'assets', 'start.webp')
LEVELS = ['gcse', 'level3']
MODES = ['stage-1', 'stage-2', 'stage-3', 'stage-4']
BOXES = {1: ['r'], 2: ['r', 'A'], 3: ['V'], 4: ['l', 'A']}
TRAPS = {1: {'r': {'diameter'}}, 2: {'r': {'diameter'}, 'A': {'early_rounding'}}, 3: {'V': {'diameter', 'no_third'}},
         4: {'l': {'diameter'}, 'A': {'early_rounding', 'curved_only'}}}
# The formulas each level and stage shows (the contract's rule).
FORMULAS = {('gcse', 'stage-1'): [], ('gcse', 'stage-2'): [], ('gcse', 'stage-3'): ['V'], ('gcse', 'stage-4'): ['l', 'Acone'],
            ('level3', 'stage-1'): ['C'], ('level3', 'stage-2'): ['C', 'Acircle'], ('level3', 'stage-3'): ['V'],
            ('level3', 'stage-4'): ['l', 'Acone']}
CONTRACT = 'i-dropped-my-ice-cream.md'
PHONE = (360, 640)
PER = 8
ONE = Decimal('0.1')


# ---------------------------------------------------------------- the contract: the bank, Jon's lines, tagline, alt text
def contract_file():
    for d in ('docs/handover/contracts', 'docs/history/contracts'):
        for f in glob.glob(os.path.join(ROOT, d, '*' + CONTRACT)):
            return f
    return None


def contract():
    f = contract_file()
    if f is None:
        return None
    text = open(f, encoding='utf-8').read()
    lines = [ln for ln in text.split('\n') if ln.startswith('{"id":')]
    lines_by_id = {json.loads(ln)['id']: ln for ln in lines}
    traps = {}
    for m in re.finditer(r'^\s+- ((?:[rAVl]\.[a-z_]+)(?:, [rAVl]\.[a-z_]+)*) → "(.*)"$', text, re.M):
        for key in m.group(1).split(', '):
            traps[key] = m.group(2)
    tag = re.search(r'^- Tagline \([^)]*\), verbatim on the start screen: "(.*)"$', text, re.M)
    alt = re.search(r'with alt "(.*?)"\.$', text, re.M)
    return {'lines': lines_by_id, 'traps': traps, 'tagline': tag and tag.group(1), 'alt': alt and alt.group(1), 'file': f}


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


def d1(x):
    return x.quantize(ONE, rounding=ROUND_HALF_UP)


def cut4(x):
    return x.quantize(Decimal('0.0001'), rounding=ROUND_DOWN)


def exact(q):
    """Every quantity of the item, exactly, from "given"."""
    g = q['given']
    if 'C' in g:
        C = Decimal(str(g['C']))
        r = C / (2 * PI)
        return {'r': r, 'A': PI * r * r}
    d, h = Decimal(str(g['d'])), Decimal(str(g['h']))
    r = d / 2
    l = (r * r + h * h).sqrt()
    return {'r': r, 'V': PI * r * r * h / 3, 'l': l, 'A': PI * r * r + PI * r * l}


def trap_values(q):
    g, e = q['given'], exact(q)
    if 'C' in g:
        C = Decimal(str(g['C']))
        return {'r': {'diameter': C / PI}, 'A': {'early_rounding': PI * d1(e['r']) ** 2}}
    d, h, r = Decimal(str(g['d'])), Decimal(str(g['h'])), e['r']
    return {'V': {'diameter': PI * d * d * h / 3, 'no_third': PI * r * r * h},
            'l': {'diameter': (d * d + h * h).sqrt()},
            'A': {'early_rounding': PI * r * r + PI * r * d1(e['l']), 'curved_only': PI * r * e['l']}}


def boundary_gap(x):
    """How far x is from the nearest 1 d.p. rounding boundary (x.x5)."""
    f = (x * 10) % 1
    return abs(f - Decimal('0.5')) / 10


def check_bank(html, out, info):
    con = contract()
    if con is None:
        out.append('no contract file *%s in docs/handover/contracts/ or docs/history/contracts/' % CONTRACT)
        return
    bank = bank_of(html)
    if sorted(bank) != LEVELS:
        out.append('the bank\'s levels are %s, not %s' % (sorted(bank), LEVELS))
    ids, n = set(), 0
    for lv in LEVELS:
        items = bank.get(lv, [])
        if len(items) != 48:
            out.append('%s: %d items, not 48' % (lv, len(items)))
        for st in (1, 2, 3, 4):
            k = sum(1 for q, _ in items if q['stage'] == st)
            if k != 12:
                out.append('%s stage %d: %d items, not 12' % (lv, st, k))
        givens = {}
        for q, raw in items:
            iid = q['id']
            n += 1
            if iid in ids:
                out.append('%s: id used twice' % iid)
            ids.add(iid)
            if not iid.startswith(lv + '_'):
                out.append('%s: in the %s bank' % (iid, lv))
            want = con['lines'].get(iid)
            if want is None:
                out.append('%s: not in the contract\'s bank' % iid)
            elif raw != want:
                out.append('%s: the page\'s line differs from the contract\'s' % iid)
            # A given is its values with their unit (Amendment 2: gcse_005's 61 cm and gcse_020's 61 m are different).
            key = json.dumps([q['given'], q['unit']], sort_keys=True)
            if key in givens:
                out.append('%s: the same given as %s' % (iid, givens[key]))
            givens[key] = iid
            g, st = q['given'], q['stage']
            if g.get('C') == 220 or g.get('d') == 120 or (g.get('d'), g.get('h')) == (120, 180):
                out.append('%s: uses Jon\'s assessment numbers %s' % (iid, g))
            if st == 4 and 'solid' not in q['prompt']:
                out.append('%s: a stage-4 prompt without "solid"' % iid)
            for k, v in g.items():
                if ('%s %s' % (v, q['unit'])) not in q['prompt']:
                    out.append('%s: the prompt does not state %s = %s %s' % (iid, k, v, q['unit']))
            if sorted(q['answers']) != sorted(BOXES[st]):
                out.append('%s: answers for %s, not %s' % (iid, sorted(q['answers']), BOXES[st]))
                continue
            if {k: set(v) for k, v in q.get('traps', {}).items()} != TRAPS[st]:
                out.append('%s: traps %s, not %s' % (iid, q.get('traps'), TRAPS[st]))
                continue
            e, tv = exact(q), trap_values(q)
            for k in BOXES[st]:
                got = Decimal(str(q['answers'][k]))
                if d1(e[k]) != got:
                    out.append('%s: %s %s, recomputed %s (%s)' % (iid, k, got, d1(e[k]), e[k]))
                if boundary_gap(e[k]) < Decimal('0.005'):
                    out.append('%s: %s = %s is within 0.005 of a 1 d.p. boundary' % (iid, k, e[k]))
                seen = {}
                for name, val in q['traps'][k].items():
                    t = Decimal(str(val))
                    if d1(tv[k][name]) != t:
                        out.append('%s: trap %s.%s %s, recomputed %s (%s)' % (iid, k, name, t, d1(tv[k][name]), tv[k][name]))
                    if t == got:
                        out.append('%s: trap %s.%s equals the answer %s' % (iid, k, name, got))
                    if t in seen:
                        out.append('%s: traps %s.%s and %s.%s are both %s' % (iid, k, name, k, seen[t], t))
                    seen[t] = name
            if st == 2 and Decimal(str(q['traps']['A']['early_rounding'])) == Decimal(str(q['answers']['A'])):
                out.append('%s: early rounding gives the answer' % iid)
            if st == 4 and Decimal(str(q['traps']['A']['early_rounding'])) == Decimal(str(q['answers']['A'])):
                out.append('%s: early rounding gives the answer' % iid)
    if len(con['lines']) != 96 or set(con['lines']) != ids:
        out.append('the contract\'s bank has %d items; the page\'s ids differ from it' % len(con['lines']))
    check_start(html, con, out)
    info['bank'] = n


def webp_size(path):
    b = open(path, 'rb').read(64)
    if b[:4] != b'RIFF' or b[8:12] != b'WEBP':
        return None
    kind = b[12:16]
    if kind == b'VP8 ':
        w, h = struct.unpack('<HH', b[26:30])
        return w & 0x3fff, h & 0x3fff
    if kind == b'VP8L':
        v = struct.unpack('<I', b[21:25])[0]
        return (v & 0x3fff) + 1, ((v >> 14) & 0x3fff) + 1
    if kind == b'VP8X':
        return int.from_bytes(b[24:27], 'little') + 1, int.from_bytes(b[27:30], 'little') + 1
    return None


def check_start(html, con, out):
    menu = html[html.find('<div id="menu"'):html.find('<div id="game"')]
    if '<h1>I Dropped My Ice Cream</h1>' not in menu:
        out.append('start: the title is not "I Dropped My Ice Cream"')
    if not con['tagline'] or ('<div class="sub" id="tagline">%s</div>' % con['tagline']) not in menu:
        out.append('start: the tagline is not Jon\'s, verbatim')
    m = re.search(r'</div>\s*<img class="start-art" src="assets/start\.webp"([^>]*)>', menu)
    if not m:
        out.append('start picture: not right after the header')
        return
    tag = m.group(1)
    if ' width="1600"' not in tag:
        out.append('start picture: the tag has no width 1600')
    if ' height="873"' not in tag:
        out.append('start picture: the tag has no height 873')
    if not con['alt'] or (' alt="%s"' % con['alt']) not in tag:
        out.append('start picture: the alt text is not the contract\'s')
    if not os.path.exists(PICTURE) or webp_size(PICTURE) != (1600, 873):
        out.append('start picture: the file is %s, not 1600 x 873' % (webp_size(PICTURE) if os.path.exists(PICTURE) else 'missing'))


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
    page.wait_for_function('!!window.ICE && !!ICE.ui', timeout=15000)
    page.evaluate("""() => { window.__ev = []; window.__sub = [];
        window.mfg = (n, p) => { window.__ev.push([n, p]); };
        window.MaffsLeaderboard = window.MaffsLeaderboard || {};
        MaffsLeaderboard.submitScore = (g, l, s, n) => { window.__sub.push([g, l, s, n]); return Promise.resolve(); }; }""")
    return br, page, errors


# Preview an item in its stage; answer box (a) with `pre` first when the box asked about is (b); then type `val`.
MARK_JS = r"""([mode, id, bi, pre, val]) => {
  ICE.ui.preview(mode, id);
  const type = (v) => { document.getElementById('ans').value = v; document.getElementById('checkBtn').click(); };
  const card = document.getElementById('qcard').innerHTML;
  if (bi === 1) { type(pre); ICE.ui.next(); }
  const before = ICE.ui.box();
  type(val);
  const fb = document.querySelector('#feedback .fb');
  const trap = fb ? fb.querySelector('.fb-trap') : null;
  return { state: ICE.ui.state(), box: before, why: fb ? fb.dataset.why : null, msg: document.getElementById('msg').dataset.why || null,
           trap: trap ? trap.dataset.trap : null, trapText: trap ? trap.textContent : null,
           text: fb ? fb.textContent : '', card: card,
           formulas: [...document.querySelectorAll('#formulas [data-formula]')].map(x => x.dataset.formula),
           calc: ICE.ui.calcMounted() && ICE.ui.calcShown() };
}"""


def f1(x):
    return '%.1f' % x


def check_marking(page, html, out, info):
    con = contract() or {'traps': {}}
    bank = bank_of(html)
    n = 0
    for lv in LEVELS:
        for q, _ in bank[lv]:
            iid, st = q['id'], q['stage']
            mode = 'stage-%d' % st
            boxes = BOXES[st]
            e = exact(q)
            for bi, k in enumerate(boxes):
                a = q['answers'][k]
                pre = f1(q['answers'][boxes[0]]) if bi else ''
                tag = '%s %s box %s' % (iid, mode, k)
                for val, want in ((f1(a), 'right'), (f1(a + 0.1), 'wrong'), (f1(a - 0.1), 'wrong')):
                    r = page.evaluate(MARK_JS, [mode, iid, bi, pre, val])
                    if r['box'] != k:
                        out.append('%s: the box on screen is %s' % (tag, r['box']))
                    if r['why'] != want:
                        out.append('%s: %s marked %s, should be %s' % (tag, val, r['why'] or r['msg'], want))
                    elif want == 'wrong':
                        # 0.1 off the answer can be a trap's value (gcse_043's A + 0.1 is its early rounding): then its line.
                        is_trap = ['%s.%s' % (k, nm) for nm, tv in q['traps'][k].items() if f1(tv) == val]
                        if r['trap'] != (is_trap[0] if is_trap else None):
                            out.append('%s: %s shows the line for %s, should be %s' % (tag, val, r['trap'], is_trap[0] if is_trap else 'none'))
                        if ('= %s' % f1(a)) not in r['text'] and f1(a) not in r['text']:
                            out.append('%s: a wrong answer does not show the answer %s' % (tag, f1(a)))
                    if bi == 0 and k == boxes[0] and val == f1(a):
                        want_f = FORMULAS[(lv, mode)]
                        if r['formulas'] != want_f:
                            out.append('%s %s: formulas shown %s, should be %s' % (lv, mode, r['formulas'], want_f))
                        if lv == 'gcse' and mode in ('stage-1', 'stage-2') and re.search(r'2\\pi r|\\pi r\^2|2πr|πr²', r['card']):
                            out.append('%s %s: a circle formula is on the card before it is answered (%s)' % (lv, mode, iid))
                        if not r['calc']:
                            out.append('%s %s: the calculator is not mounted and shown' % (lv, mode))
                for val, want in (('%.2f' % (a + 0.04), 'format'), ('twelve', 'unreadable')):
                    r = page.evaluate(MARK_JS, [mode, iid, bi, pre, val])
                    if r['state'] != 'asking' or r['msg'] != want:
                        out.append('%s: %r should not be marked (%s message); got state %s, message %s' % (tag, val, want, r['state'], r['msg']))
                for name, tv in q['traps'][k].items():
                    key = '%s.%s' % (k, name)
                    r = page.evaluate(MARK_JS, [mode, iid, bi, pre, f1(tv)])
                    if r['why'] != 'wrong':
                        out.append('%s: trap %s (%s) marked %s' % (tag, key, f1(tv), r['why'] or r['msg']))
                    if r['trap'] != key or r['trapText'] != con['traps'].get(key):
                        out.append('%s: trap %s (%s) shows %r, not Jon\'s line %r' % (tag, key, f1(tv), r['trapText'], con['traps'].get(key)))
                if bi == 1:
                    # (b) after a wrong (a): still right. (b) worked from the rounded (a): wrong (it is the early-rounding trap).
                    wrong_a = f1(q['traps'][boxes[0]]['diameter'])
                    r = page.evaluate(MARK_JS, [mode, iid, 1, wrong_a, f1(a)])
                    if r['why'] != 'right':
                        out.append('%s: after a wrong (a), the full-accuracy answer %s is marked %s' % (tag, f1(a), r['why']))
                    r = page.evaluate(MARK_JS, [mode, iid, 1, pre, f1(trap_values(q)['A']['early_rounding'])])
                    if r['why'] != 'wrong':
                        out.append('%s: the answer worked from the rounded (a) is marked %s' % (tag, r['why']))
                check_working(q, k, e, page.evaluate('([id, k]) => ICE.working(id, k)', [iid, k]), out)
            n += 1
    info['marked'] = n


def check_working(q, k, e, W, out):
    tag = '%s working for %s' % (q['id'], k)
    if not W:
        out.append('%s: none' % tag)
        return
    text = '\n'.join(W)
    cuts = [Decimal(x) for x in re.findall(r'(\d+\.\d+)\\ldots', text)]
    want = {'r': ['r'], 'V': ['V'], 'l': ['l']}.get(k) or (['r', 'A'] if 'C' in q['given'] else ['l', 'A'])
    want_cut = [cut4(e[w]) for w in want if cut4(e[w]) != e[w]]
    for c in cuts:
        if c not in want_cut:
            out.append('%s: %s\\ldots is not a 4 d.p. cut of %s' % (tag, c, ', '.join('%s = %s' % (w, e[w]) for w in want)))
    for w, c in zip(want, [cut4(e[w]) for w in want]):
        if c != e[w] and c not in cuts:
            out.append('%s: %s is not written cut to 4 d.p. (%s\\ldots)' % (tag, w, c))
    if 'd' in q['given']:
        r = e['r']
        rs = str(r.normalize()) if r != r.to_integral() else str(int(r))
        if ('\\div 2 = %s' % rs) not in text:
            out.append('%s: r = d / 2 = %s is not written exactly' % (tag, rs))
    last = W[-1]
    if ('%s = %s' % (k, f1(q['answers'][k]))) not in last:
        out.append('%s: the last line %r is not %s = %s' % (tag, last, k, f1(q['answers'][k])))


# ---------------------------------------------------------------- the diagrams
DRAW_JS = r"""([mode, id]) => {
  ICE.ui.preview(mode, id);
  const svg = document.querySelector('#fig svg');
  if (!svg) return null;
  const vb = svg.viewBox.baseVal;
  const labels = [...svg.querySelectorAll('text')].map(t => { const b = t.getBBox(); return { lab: t.dataset.lab || null, text: t.textContent, x: b.x, y: b.y, w: b.width, h: b.height }; });
  const slants = [...svg.querySelectorAll('line.c-slant')].map(l => [l.x1.baseVal.value, l.y1.baseVal.value, l.x2.baseVal.value, l.y2.baseVal.value]);
  const circle = svg.querySelector('circle.c-line');
  return { vb: [vb.x, vb.y, vb.width, vb.height], labels, slants, circle: !!circle,
           width: svg.getBoundingClientRect().width, scroll: document.documentElement.scrollWidth };
}"""


def seg_hits_box(s, b, pad=1.0):
    """Does segment s = (x1, y1, x2, y2) meet the box (x, y, w, h) grown by pad? Liang-Barsky clipping."""
    x1, y1, x2, y2 = s
    xmin, ymin, xmax, ymax = b['x'] - pad, b['y'] - pad, b['x'] + b['w'] + pad, b['y'] + b['h'] + pad
    dx, dy = x2 - x1, y2 - y1
    t0, t1 = 0.0, 1.0
    for p, qq in ((-dx, x1 - xmin), (dx, xmax - x1), (-dy, y1 - ymin), (dy, ymax - y1)):
        if p == 0:
            if qq < 0:
                return False
        else:
            t = qq / p
            if p < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                return False
    return True


def boxes_meet(a, b):
    return min(a['x'] + a['w'], b['x'] + b['w']) - max(a['x'], b['x']) > 0.5 and min(a['y'] + a['h'], b['y'] + b['h']) - max(a['y'], b['y']) > 0.5


def check_diagrams(page, html, out, info):
    bank = bank_of(html)
    n = 0
    for lv in LEVELS:
        for q, _ in bank[lv]:
            iid, st, g, u = q['id'], q['stage'], q['given'], q['unit']
            mode = 'stage-%d' % st
            tag = '%s diagram (%s)' % (iid, mode)
            r = page.evaluate(DRAW_JS, [mode, iid])
            if r is None:
                out.append('%s: none drawn' % tag)
                continue
            got = {l['lab']: l['text'] for l in r['labels']}
            if 'C' in g:
                want = {'C': 'C = %s %s' % (g['C'], u), 'r': 'r = ?'}
                if st == 2:
                    want['A'] = 'A = ?'
                if not r['circle']:
                    out.append('%s: no circle' % tag)
            else:
                want = {'h': 'h = %s %s' % (g['h'], u), 'd': 'diameter = %s %s' % (g['d'], u)}
                if st == 4:
                    want['l'] = 'l = ?'
                if len(r['slants']) != 2:
                    out.append('%s: %d slant edges' % (tag, len(r['slants'])))
                else:
                    a, b = sorted(r['slants'], key=lambda s: s[2])
                    width, height = b[2] - a[2], ((a[3] + b[3]) / 2) - a[1]
                    ratio, true = width / height, g['d'] / g['h']
                    if abs(ratio / true - 1) > 0.005:
                        out.append('%s: drawn diameter : height %.4f, not %.4f' % (tag, ratio, true))
                    for l in r['labels']:
                        if l['lab'] == 'h' and any(seg_hits_box(s, l) for s in r['slants']):
                            out.append('%s: the height label crosses the slant edge' % tag)
            if got != want or len(r['labels']) != len(want):
                out.append('%s: labels %s, should be exactly %s' % (tag, [(l['lab'], l['text']) for l in r['labels']], want))
            L = r['labels']
            for i in range(len(L)):
                for j in range(i + 1, len(L)):
                    if boxes_meet(L[i], L[j]):
                        out.append('%s: labels %r and %r overlap' % (tag, L[i]['text'], L[j]['text']))
            vx, vy, vw, vh = r['vb']
            for l in L:
                if l['x'] < vx - 0.5 or l['y'] < vy - 0.5 or l['x'] + l['w'] > vx + vw + 0.5 or l['y'] + l['h'] > vy + vh + 0.5:
                    out.append('%s: %r is cut off' % (tag, l['text']))
            if r['width'] > PHONE[0] or r['scroll'] > PHONE[0]:
                out.append('%s: wider than %d px (%s, page %s)' % (tag, PHONE[0], r['width'], r['scroll']))
            n += 1
    info['diagrams'] = n


# ---------------------------------------------------------------- play
def play(page, lv, m, out):
    page.evaluate('() => { window.__ev = []; window.__sub = []; }')
    page.evaluate('([l, m]) => { ICE.ui.setLevel(l); ICE.ui.start(m); }', [lv, m])
    st = int(m[-1])
    seen, right, k = [], 0, 0
    for _ in range(200):
        s = page.evaluate('ICE.ui.state()')
        if s == 'over':
            break
        if s == 'asking':
            q = page.evaluate('ICE.ui.question()')
            if not seen or seen[-1] != q['id']:
                seen.append(q['id'])
                if q['stage'] != st:
                    out.append('%s %s: served %s, a stage %d item' % (lv, m, q['id'], q['stage']))
            ok = k % 3 != 1
            page.evaluate('(r) => ICE.ui.answer(r)', ok)
            right += 1 if ok else 0
            k += 1
        else:
            page.evaluate('ICE.ui.next()')
    tag = '%s %s' % (lv, m)
    if page.evaluate('ICE.ui.state()') != 'over':
        out.append('%s: the run did not finish' % tag)
        return
    boxes = len(BOXES[st])
    if len(seen) != PER or len(set(seen)) != PER or any(not s.startswith(lv + '_') for s in seen):
        out.append('%s: the run served %s, not %d different %s items' % (tag, seen, PER, lv))
    if k != PER * boxes:
        out.append('%s: %d boxes asked, not %d' % (tag, k, PER * boxes))
    ev = page.evaluate('window.__ev')
    sub = page.evaluate('window.__sub')
    done = [p for n, p in ev if n == 'game_completed']
    if len(done) != 1 or done[0].get('score') != right or done[0].get('level') != lv or done[0].get('mode') != m:
        out.append('%s: game_completed %s, expected one with score %d' % (tag, done, right))
    if sub != [[SLUG, '%s-%s' % (lv, m), right, PER]]:
        out.append('%s: the leaderboard got %s, expected one submission on %s-%s with %d' % (tag, sub, lv, m, right))
    if page.evaluate('document.documentElement.scrollWidth') > PHONE[0]:
        out.append('%s: the page scrolls sideways at %d px' % (tag, PHONE[0]))
    qa = [p for n, p in ev if n == 'question_answered']
    if len(qa) != PER or any(not p.get('question_id') for p in qa):
        out.append('%s: %d question_answered events, each needs a question_id' % (tag, len(qa)))
    if not page.evaluate('ICE.ui.calcMounted() && ICE.ui.calcShown()'):
        out.append('%s: the calculator is not mounted' % tag)
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


# Each plant: (what, [(old, new)], the unit it needs, the pattern its finding must match). The six the contract names.
PLANTS = [
    ('an answer 0.1 out', [('"answers":{"r":14.8},"traps":{"r":{"diameter":29.6}}', '"answers":{"r":14.9},"traps":{"r":{"diameter":29.6}}')],
     'bank', r'gcse_001: r 14\.9, recomputed 14\.8'),
    ('box (b) marked against the rounded r',
     [("var k = box(), raw = $('ans').value, r = MaffsAnswer.decimal(raw, Q.answers[k], 1);",
       "var k = box(), raw = $('ans').value, r = MaffsAnswer.decimal(raw, k === 'A' && Q.given.C !== undefined ? Math.round(PI * Q.answers.r * Q.answers.r * 10) / 10 : Q.answers[k], 1);")],
     'marking', r'gcse_013 stage-2 box A: 45\.8 marked wrong'),
    ('a trap line swapped',
     [("'V.no_third': 'just because we don\\'t like fractions, that doesn\\'t mean we can ignore them dude',",
       "'V.no_third': 'just cos you can\\'t see the bottom, doesn\\'t mean it aint there my man.',")],
     'marking', r'trap V\.no_third .* not Jon\'s line'),
    ('a GCSE stage 1 showing C = 2 pi r',
     [("function formulasShown(lv, m) { return lv === 'level3' || m === 'stage-3' || m === 'stage-4'; }",
       "function formulasShown(lv, m) { return lv === 'level3' || m === 'stage-1' || m === 'stage-3' || m === 'stage-4'; }")],
     'marking', r'gcse stage-1: formulas shown \[\'C\'\]'),
    ('the height label crossing the slant edge',
     [("if (cx + 6 + w + 4 <= cx + halfAt(yTop)) {", "if (true) {")],
     'diagrams %dx%d' % PHONE, r'the height label crosses the slant edge'),
    ('a stage-4 prompt without "solid"',
     [('"prompt":"A cone-shaped candle is a solid cone with base diameter 6 cm', '"prompt":"A cone-shaped candle is a cone with base diameter 6 cm')],
     'bank', r'gcse_038: a stage-4 prompt without "solid"'),
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
    units = ['bank', 'marking', 'diagrams %dx%d' % PHONE, 'play %dx%d' % PHONE]
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
        print('%s: %d items, every answer and trap recomputed from "given" (exact decimals), the bank and start screen against the contract' % (SLUG, info['bank']))
    if 'marked' in info:
        print('%s: %d items marked box by box (answer, 0.1 either side, 2 d.p., unreadable, every trap and Jon\'s line, box (b) from full accuracy); working, formulas and calculator checked' % (SLUG, info['marked']))
    if 'diagrams' in info:
        print('%s: %d diagrams from their given values, cones to true proportion, the height label clear of the slant edges, labels exact, no overlap at %dx%d' % (SLUG, info['diagrams'], PHONE[0], PHONE[1]))
    if 'played' in info:
        print('%s: %d runs played (every stage at both levels)' % (SLUG, info['played']))
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
