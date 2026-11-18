#!/usr/bin/env python3
# ci-shards: Sums in Disguise (the bank's SHA-256 against the contract's; all 226 items recomputed from little and the big sum's tens, every decoy by its rule, distinct, never the answer, never negative; Stage 4's decoys different facts in range; coverage of every pair, no repeated big sum, no ones sum in two of Stages 1, 3 and 4; the 67 counts; the lines against the contract, verbatim; the fragment never sent or stored; in both looks every tile, option and Stage 4 sum marked by dataset.val alone, every decoy's aha line then the learning line, the 67 after marking on exactly the firing items; the greeting for each fragment; every stage played in both looks at 360x640 with every control above the fold, one board submission on stage-N, no payload naming the look; fault-injection self-test) | | 1
# ci-deps: games/sums-in-disguise/ docs/handover/contracts/ docs/history/contracts/
r"""Independent verification for Sums in Disguise (games/sums-in-disguise/), contract SUMS-IN-DISGUISE, 18 Nov 2026.
SR-30: checked from its first PR.

WHAT THIS DOES NOT TRUST
-------------------------------------------------------------------------------
The page holds a fixed bank of 226 items, made by the generator in the contract. This script never uses the page's
numbers to check the page's numbers:

  Bank      the page's items, written one a line as json.dumps(item, separators=(",", ":")) with a newline after
            each, have the SHA-256 the contract states. Counts 50/36/50 (25 ones, 25 tens)/40 (25 ones, 15 tens)/50,
            ids unique. Every item recomputed from little = [a, b] and t, the big sum's tens: little_answer = a + b; the
            answer is the big sum's total; ones (10t + a) + b with a + b <= 9; tens 10a + 10b with a + b <= 9; cross
            (10t + a) + b with a + b >= 10 and a total <= 99. Decoys by rule (tens p + 10q; concat the digits of p - a
            then of a + b, or on a cross item of t then of a + b; off_by_one the answer +-1, or +-10 where the fallback
            applied; forgot_disguise a + b; extra_zero 100(a + b); ones p + b; forgot_ten the answer - 10), the three
            distinct, never the answer, never negative. Stage 4: answer_sum is the little fact in its disguise; each
            decoy a different fact (not {a, b} either way round), in range, no crossing; the three options distinct.
            Coverage: Stage 1 and 2 every one of the 36 pairs, Stage 5 every one of the 45; no big sum twice in a stage;
            no ones big sum in two of Stages 1, 3 and 4. The 67 fires on 6/2/7/4/14 items.
  Source    the greeting is never written with innerHTML; location.hash is read once; no mfg() payload, storage write
            or board names the look, the fragment or the class name.
  Lines     the page's LINES equal the contract's placeholder lines, character for character, in both looks.
  Marking   in each look, every item in the page: the disguise on the big sum; for Stages 1, 2 and 5 taking it off
            shows the little sum, the tag (p - a, or "0 0" on a tens item) and the stage's reveal line, then tiles 0 to 10
            (0 to 20 in Stage 5), each marked by its dataset.val with every tile's text blanked first, right only for
            a + b, and the disguise back on with the big sum after any tile; Stage 3's Peek shows the little sum and the
            reveal line. Every option, with every option's text blanked first, is marked by its dataset.val: right only
            for the answer (Stage 4: answer_sum as "p+q"); a decoy shows its own aha line (Stage 4: the duck's), then the
            learning line built here from the item, in KaTeX; the 67 hidden before marking and shown after it exactly
            when a 6 and a 7 are among the big sum's numbers and the answer.
  Greeting  "#kids/Maple" and "#kids/Maple%20Class" -> "Welcome, Maple Class!"; "#KIDS" and "#kids" -> the kid look
            and its welcome; "#kids/<script>" -> the kid look, no class greeting, nothing injected; no hash or "#kidsx"
            -> the grown-up look; a bad ?level= rewritten by MaffsLevel keeps the fragment.
  Play      every stage in each look at 360 x 640 (the kid look from #kids/Maple): 10 different items of the stage, the
            unmask button, tiles, options and Next above the fold, no sideways scroll; one game_completed with the score,
            one board submission [slug, 'stage-N', score, 10]; Stage 3's "Done without peeking"; the end line; no mfg()
            payload, localStorage or sessionStorage value containing "kids", "Maple" or "#".

Work units: "bank" (no browser), "marking grown", "marking kids", "greeting", "play grown 360x640", "play kids 360x640",
and "plant: <what>" (one per planted fault).

    python scripts/verify-sums-in-disguise.py              # every unit, then the self-test
    python scripts/verify-sums-in-disguise.py --selftest   # the planted faults only
"""
import argparse
import contextlib
import glob
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402
import plant_common as pc  # noqa: E402

SLUG = 'sums-in-disguise'
GAME = os.path.join(ROOT, 'games', SLUG, 'index.html')
CONTRACT = 'sums-in-disguise.md'
SHA = '19e415561cb6baecdaf01d2bde6f23f367a6aff2802d33b8d152dce6561068a8'
MODES = ['stage-1', 'stage-2', 'stage-3', 'stage-4', 'stage-5']
COUNTS = {1: 50, 2: 36, 3: 50, 4: 40, 5: 50}
TYPES = {3: {'ones': 25, 'tens': 25}, 4: {'ones': 25, 'tens': 15}}
FIRES = {1: 6, 2: 2, 3: 7, 4: 4, 5: 14}
PHONE = (360, 640)
PER = 10
ONES_PAIRS = [(a, b) for a in range(1, 9) for b in range(1, 10 - a)]
CROSS_PAIRS = [(a, b) for a in range(1, 10) for b in range(1, 10) if a + b >= 10]


# ---------------------------------------------------------------- the contract
def contract_file():
    for d in ('docs/handover/contracts', 'docs/history/contracts'):
        for f in glob.glob(os.path.join(ROOT, d, '*' + CONTRACT)):
            return f
    return None


def contract_lines():
    """The placeholder lines, parsed from the contract: {look: {key: str | [str] | {k: str}}}."""
    f = contract_file()
    if f is None:
        raise ValueError('no contract file *%s in docs/handover/contracts or docs/history/contracts' % CONTRACT)
    text = open(f, encoding='utf-8').read()
    block = text.split('THE PLACEHOLDER LINES', 1)[1].split('\nShared, both looks', 1)[0]
    out, look = {}, None
    q = r'"((?:[^"\\]|\\.)*)"'
    for ln in block.split('\n'):
        m = re.match(r'^(grown|kids):$', ln)
        if m:
            look = m.group(1)
            out[look] = {}
            continue
        m = re.match(r'^  ([a-z_]+): (.*)$', ln)
        if not m or look is None:
            continue
        key, rest = m.groups()
        if rest.startswith('{'):
            out[look][key] = {k: v for k, v in re.findall(r'([a-z_][a-z_0-9-]*): ' + q, rest)}
        elif rest.startswith('['):
            out[look][key] = re.findall(q, rest)
        else:
            out[look][key] = re.fullmatch(q, rest).group(1)
    return out


# ---------------------------------------------------------------- the bank, read from the page's source
def bank_of(html):
    m = re.search(r'var QUESTIONS = \[\n(.*?)\n  \];', html, re.S)
    if not m:
        raise ValueError('no QUESTIONS block in the page')
    items = []
    for ln in m.group(1).split('\n'):
        s = ln.strip()
        if s.startswith('{'):
            items.append(json.loads(s[:-1] if s.endswith(',') else s))
    return items


def big_of(q):
    return q['answer_sum'] if q['stage'] == 4 else q['big']


def has67(q):
    d = '%d%d%d' % (big_of(q)[0], big_of(q)[1], q['answer'])
    return '6' in d and '7' in d


def tag_of(q):
    return '0 0' if q['type'] == 'tens' else str(big_of(q)[0] - q['little'][0])


def learning(q):
    a, b = q['little']
    c, (p, r), n = a + b, big_of(q), sum(big_of(q))
    if q['stage'] == 4:
        return '%d + %d = %d, so %d + %d = %d is %d + %d in disguise.' % (a, b, c, p, r, n, a, b)
    if q['type'] == 'cross':
        return '%d + %d = %d, so %d + %d = %d + %d = %d.' % (a, b, c, p, r, p - a, c, n)
    return '%d + %d = %d, so %d + %d = %d.' % (a, b, c, p, r, n)


def check_item(q, out):
    """Every number of one item, recomputed from little and the big sum's tens."""
    i, st, typ = q['id'], q['stage'], q['type']
    a, b = q['little']
    s = big_of(q)
    p, r = s
    want_type = {1: 'ones', 2: 'tens', 5: 'cross'}.get(st)
    if (want_type and typ != want_type) or typ not in ('ones', 'tens', 'cross'):
        out.append('%s: type %s in stage %d' % (i, typ, st))
        return
    if q['little_answer'] != a + b:
        out.append('%s: little_answer %s, recomputed %d' % (i, q['little_answer'], a + b))
    if q['answer'] != p + r:
        out.append('%s: answer %s, recomputed %d' % (i, q['answer'], p + r))
    t = (p - a) // 10
    if typ == 'tens':
        if (p, r) != (10 * a, 10 * b):
            out.append('%s: a tens item whose big sum %d + %d is not 10a + 10b' % (i, p, r))
        if a + b > 9:
            out.append('%s: a tens item crosses a hundred' % i)
    else:
        if p != 10 * t + a or r != b or t < 1 or not 1 <= a <= 9 or not 1 <= b <= 9:
            out.append('%s: big sum %d + %d is not (10t + a) + b for little %d + %d' % (i, p, r, a, b))
        if typ == 'ones' and a + b > 9:
            out.append('%s: a ones item crosses a ten' % i)
        if typ == 'cross' and a + b < 10:
            out.append('%s: a cross item does not cross a ten' % i)
        if typ == 'cross' and p + r > 99:
            out.append('%s: a cross item totals over 99' % i)
    ans = p + r
    if st == 4:
        opts = [tuple(s)] + [tuple(d['sum']) for d in q['decoys']]
        if len(q['decoys']) != 2 or len(set(opts)) != 3:
            out.append('%s: Stage 4 options are not three distinct sums' % i)
        for d in q['decoys']:
            dp, dr = d['sum']
            if typ == 'tens':
                ok = dp % 10 == 0 and dr % 10 == 0
                da, db = dp // 10, dr // 10
            else:
                ok = (dp - (dp % 10)) == 10 * t
                da, db = dp % 10, dr
            if not ok or not (1 <= da <= 9 and 1 <= db <= 9 and da + db <= 9):
                out.append('%s: Stage 4 decoy %d + %d is out of range or not the same disguise' % (i, dp, dr))
            if sorted([da, db]) == sorted([a, b]):
                out.append('%s: Stage 4 decoy %d + %d is the same fact as %d + %d' % (i, dp, dr, a, b))
        return
    d = q['decoys']
    rules = {'ones': {'tens': p + 10 * r, 'concat': int('%d%d' % (p - a, a + b)), 'off_by_one': None},
             'tens': {'forgot_disguise': a + b, 'extra_zero': 100 * (a + b), 'ones': p + b},
             'cross': {'forgot_ten': ans - 10, 'concat': int('%d%d' % (t, a + b)), 'off_by_one': None}}[typ]
    if sorted(d) != sorted(rules):
        out.append('%s: decoys %s, the rule names %s' % (i, sorted(d), sorted(rules)))
    for k, v in rules.items():
        if k not in d:
            continue
        if v is None:
            if d[k] not in (ans + 1, ans - 1, ans + 10, ans - 10):
                out.append('%s: off_by_one %s is not the answer +-1 (or +-10)' % (i, d[k]))
        elif d[k] != v:
            out.append('%s: decoy %s %s, recomputed %d' % (i, k, d[k], v))
    vals = list(d.values())
    if len(set(vals)) != len(vals):
        out.append('%s: two decoys are equal' % i)
    if ans in vals:
        out.append('%s: a decoy equals the answer' % i)
    if any(v < 0 for v in vals):
        out.append('%s: a negative decoy' % i)


def check_bank(html, out, info):
    items = bank_of(html)
    blob = ''.join(json.dumps(q, separators=(',', ':')) + '\n' for q in items).encode('utf-8')
    got = hashlib.sha256(blob).hexdigest()
    if got != SHA:
        out.append('the bank has SHA-256 %s, the contract states %s' % (got, SHA))
    ids = [q['id'] for q in items]
    if len(ids) != len(set(ids)):
        out.append('ids repeat')
    for st, n in COUNTS.items():
        s = [q for q in items if q['stage'] == st]
        if len(s) != n:
            out.append('stage %d has %d items, not %d' % (st, len(s), n))
        for typ, k in TYPES.get(st, {}).items():
            if sum(1 for q in s if q['type'] == typ) != k:
                out.append('stage %d has not %d %s items' % (st, k, typ))
        bigs = [tuple(big_of(q)) for q in s]
        if len(bigs) != len(set(bigs)):
            out.append('stage %d repeats a big sum' % st)
        fires = sum(1 for q in s if has67(q))
        if fires != FIRES[st]:
            out.append('stage %d: the 67 fires on %d items, not %d' % (st, fires, FIRES[st]))
    for st, pairs in ((1, ONES_PAIRS), (2, ONES_PAIRS), (5, CROSS_PAIRS)):
        have = {tuple(q['little']) for q in items if q['stage'] == st}
        if have != set(pairs):
            out.append('stage %d does not use every one of its %d pairs' % (st, len(pairs)))
    seen = {}
    for q in items:
        if q['type'] == 'ones' and q['stage'] in (1, 3, 4):
            seen.setdefault(tuple(big_of(q)), set()).add(q['stage'])
    for k, v in seen.items():
        if len(v) > 1:
            out.append('the ones big sum %d + %d is in stages %s' % (k[0], k[1], sorted(v)))
    for q in items:
        try:
            check_item(q, out)
        except (KeyError, TypeError, ValueError) as e:
            out.append('%s: unreadable item (%s)' % (q.get('id'), e))
    info['bank'] = len(items)


def check_source(html, out):
    """The fragment, the look and the class name stay in the page."""
    js = '\n'.join(re.findall(r'<script>(.*?)</script>', html, re.S))
    if re.search(r'innerHTML\s*=[^;\n]*(greeting\(|CLASS_NAME|\bfrag\b|\bnm\b)', js):
        out.append('the greeting (the class name) is written with innerHTML')
    if js.count('location.hash') != 1:
        out.append('location.hash is read %d times, not once' % js.count('location.hash'))
    if 'sessionStorage' in js:
        out.append('the page uses sessionStorage')
    for m in re.finditer(r'\b(?:lsSet|localStorage\.setItem)\(([^;\n]*)', js):
        if re.search(r'LOOK|CLASS_NAME|\bfrag\b|\bnm\b|hash', m.group(1)):
            out.append('a storage write names the look or the fragment: %s' % m.group(0)[:80])
    for m in re.finditer(r'\bev\((\'[a-z_]+\'), \{([^}]*)\}', js):
        if re.search(r'LOOK|CLASS_NAME|\bfrag\b|\bnm\b|hash', m.group(2)):
            out.append('an mfg() payload names the look or the fragment: %s' % m.group(1))


# ---------------------------------------------------------------- the browser
def open_page(pw, base, html, size, frag='', query='?cb=verify'):
    br = pw.chromium.launch()
    touch = size[0] <= 600
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch)
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    # Record every mfg() call from the first one: analytics.js's own mfg is wrapped as it is defined.
    ctx.add_init_script("""(() => { window.__ev = []; let real = null;
      Object.defineProperty(window, 'mfg', { configurable: true,
        get() { return function (n, p) { window.__ev.push([n, JSON.parse(JSON.stringify(p || {}))]); }; },
        set(v) { real = v; } }); })();""")
    bc.offline(ctx, base)
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/%s%s' % (SLUG, query, frag), wait_until='load', timeout=30000)
    page.wait_for_function('!!window.SID && !!SID.ui', timeout=15000)
    page.evaluate("""() => { window.__sub = [];
        window.MaffsLeaderboard = window.MaffsLeaderboard || {};
        MaffsLeaderboard.submitScore = (g, l, s, n) => { window.__sub.push([g, l, s, n]); return Promise.resolve(); }; }""")
    return br, page, errors


ITEM_JS = r"""([q]) => {
  const $ = (id) => document.getElementById(id);
  const out = { tiles: {}, opts: {} };
  const flow = q.stage === 3 ? 'wig' : q.stage === 4 ? 'duck' : 'unmask';
  const sumOf = () => $('sum').dataset.sum;
  const on = () => !$('suspect').classList.contains('unmasked');
  if (flow === 'unmask') {
    SID.ui.preview(q.id);
    out.mask = { state: SID.ui.state(), sum: sumOf(), on: on(), pop: !$('pop67').hidden };
    SID.ui.unmask();
    out.little = { state: SID.ui.state(), sum: sumOf(), on: on(), tag: $('tag').textContent,
                   tagShown: getComputedStyle($('tag')).display !== 'none', say: $('say').textContent };
    out.tileVals = [...$('tiles').querySelectorAll('.tile')].map(b => b.dataset.val);
    for (const v of out.tileVals) {
      window.__ev = [];
      SID.ui.preview(q.id); SID.ui.unmask();
      $('tiles').querySelectorAll('.tile').forEach(b => { b.textContent = '?'; });
      SID.ui.tile(v);
      out.tiles[v] = { little: $('clue').dataset.little || null, state: SID.ui.state(), sum: sumOf(), on: on(),
                       answered: (window.__ev || []).filter(e => e[0] === 'question_answered').length };
    }
  }
  if (flow === 'wig') {
    SID.ui.preview(q.id);
    out.wigOn = { state: SID.ui.state(), sum: sumOf(), on: on() };
    SID.ui.peek();
    out.peek = { sum: sumOf(), on: on(), say: $('say').textContent, tag: $('tag').textContent };
  }
  const toBig = () => { SID.ui.preview(q.id); if (flow === 'unmask') { SID.ui.unmask(); SID.ui.tile(q.little_answer); } };
  toBig();
  out.big = { state: SID.ui.state(), sum: sumOf(), on: on(), prompt: $('prompt').textContent };
  out.optVals = [...$('opts').querySelectorAll('.opt')].map(b => b.dataset.val);
  for (const v of out.optVals) {
    toBig();
    const popBefore = !$('pop67').hidden;
    $('opts').querySelectorAll('.opt').forEach(b => { b.innerHTML = '?'; });
    window.__ev = [];
    SID.ui.pick(v);
    const fb = document.querySelector('#feedback .fb'), ln = $('learn');
    const qa = window.__ev.filter(e => e[0] === 'question_answered');
    out.opts[v] = { popBefore: popBefore, why: fb ? fb.dataset.why : null, pick: fb ? (fb.dataset.pick || null) : null,
      say: $('say').textContent, learn: ln ? ln.dataset.learn : null, katex: !!(ln && ln.querySelector('.katex')),
      pop: $('pop67').hidden ? null : $('pop67').textContent.trim(), score: SID.ui.score(),
      next: !!document.querySelector('#feedback .maffs-next, #nextBtn'),
      qa: qa.map(e => [e[1].correct, e[1].question_id]) };
  }
  return out;
}"""


def check_marking(page, html, look, out, info):
    want = contract_lines()
    got = page.evaluate('SID.lines()')
    for lk in ('grown', 'kids'):
        if got.get(lk) != want.get(lk):
            keys = sorted(set(got.get(lk, {})) | set(want.get(lk, {})))
            bad = [k for k in keys if got.get(lk, {}).get(k) != want.get(lk, {}).get(k)]
            out.append('LINES.%s differs from the contract at %s' % (lk, bad))
    L = want[look]
    tagl = look
    fired = {}
    for q in bank_of(html):
        r = page.evaluate(ITEM_JS, [q])
        i, st = q['id'], q['stage']
        a, b = q['little']
        big = '%d+%d' % tuple(big_of(q))
        little = '%d+%d' % (a, b)
        mode = 'stage-%d' % st
        if st in (1, 2, 5):
            m = r['mask']
            if m['state'] != 'mask' or m['sum'] != big or not m['on'] or m['pop']:
                out.append('%s %s: the big sum is not shown in its disguise first (%s)' % (tagl, i, m))
            lt = r['little']
            if lt['state'] != 'little' or lt['sum'] != little or lt['on'] or not lt['tagShown'] or lt['tag'] != tag_of(q):
                out.append('%s %s: taking the disguise off does not show %s with the tag %s (%s)' % (tagl, i, little, tag_of(q), lt))
            if lt['say'] != L['reveal'][mode]:
                out.append('%s %s: the reveal line is %r' % (tagl, i, lt['say']))
            n = 20 if st == 5 else 10
            if r['tileVals'] != [str(v) for v in range(n + 1)]:
                out.append('%s %s: tiles %s, not 0 to %d' % (tagl, i, r['tileVals'], n))
            for v, t in r['tiles'].items():
                ok = 'right' if int(v) == a + b else 'wrong'
                if t['little'] != ok or t['state'] != 'big' or t['sum'] != big or not t['on'] or t['answered']:
                    out.append('%s %s: tile %s marked %s, expected %s, then the disguise back on the big sum (%s)' % (tagl, i, v, t['little'], ok, t))
        if st == 3:
            if r['wigOn']['state'] != 'big' or r['wigOn']['sum'] != big or not r['wigOn']['on']:
                out.append('%s %s: the wig is not on the big sum at the question (%s)' % (tagl, i, r['wigOn']))
            pk = r['peek']
            if pk['sum'] != little or pk['on'] or pk['say'] != L['reveal'][mode] or pk['tag'] != tag_of(q):
                out.append('%s %s: Peek does not show %s with the reveal line (%s)' % (tagl, i, little, pk))
        bg = r['big']
        if bg['state'] != 'big' or (st != 4 and (bg['sum'] != big or not bg['on'])):
            out.append('%s %s: the big sum is not asked in its disguise (%s)' % (tagl, i, bg))
        if st == 4:
            key = big
            want_opts = {key} | {'%d+%d' % tuple(d['sum']) for d in q['decoys']}
            names = {'%d+%d' % tuple(d['sum']): d['kind'] for d in q['decoys']}
            if bg['prompt'].replace(' ', '').find('Whichoneis') != 0:
                out.append('%s %s: the Stage 4 question reads %r' % (tagl, i, bg['prompt']))
        else:
            key = str(q['answer'])
            want_opts = {key} | {str(v) for v in q['decoys'].values()}
            names = {str(v): k for k, v in q['decoys'].items()}
        if set(r['optVals']) != want_opts or len(r['optVals']) != len(want_opts):
            out.append('%s %s: options %s, expected %s' % (tagl, i, r['optVals'], sorted(want_opts)))
        lr = learning(q)
        for v, o in r['opts'].items():
            right = v == key
            if o['why'] != ('right' if right else 'wrong') or o['score'] != (1 if right else 0):
                out.append('%s %s: option %s marked %s, expected %s' % (tagl, i, v, o['why'], 'right' if right else 'wrong'))
            if o['qa'] != [[right, i]]:
                out.append('%s %s: option %s logged %s' % (tagl, i, v, o['qa']))
            if o['popBefore']:
                out.append('%s %s: the 67 shows before marking' % (tagl, i))
            if (o['pop'] == '67') != has67(q) or (o['pop'] not in (None, '67')):
                out.append('%s %s: after marking the 67 is %r, expected %s' % (tagl, i, o['pop'], 'shown' if has67(q) else 'hidden'))
            if o['learn'] != lr or not o['katex']:
                out.append('%s %s: the learning line is %r (KaTeX %s), expected %r' % (tagl, i, o['learn'], o['katex'], lr))
            if not o['next']:
                out.append('%s %s: no Next after option %s' % (tagl, i, v))
            if st == 4:
                line = (L['duck_right'] if right else L['duck_wrong']) + ' ' + L['reveal'][mode]
                if o['say'] != line:
                    out.append('%s %s: option %s: the duck says %r' % (tagl, i, v, o['say']))
            elif right:
                if o['say'] not in L['right']:
                    out.append('%s %s: a right answer says %r' % (tagl, i, o['say']))
            else:
                k = names.get(v)
                ak = 'concat_cross' if k == 'concat' and q['type'] == 'cross' else k
                if o['pick'] != k or o['say'] != L['aha'].get(ak):
                    out.append('%s %s: decoy %s (%s) says %r, not its aha line' % (tagl, i, v, k, o['say']))
        if any(o['pop'] == '67' for o in r['opts'].values()):
            fired[st] = fired.get(st, 0) + 1
    for st, n in FIRES.items():
        if fired.get(st, 0) != n:
            out.append('%s: the 67 showed on %d stage %d items, not %d' % (tagl, fired.get(st, 0), st, n))
    info['marked'] = info.get('marked', 0) + len(bank_of(html))


GREETINGS = [
    ('', 'grown', None),
    ('#kidsx', 'grown', None),
    ('#kids', 'kids', None),
    ('#KIDS', 'kids', None),
    ('#kids/Maple', 'kids', 'Welcome, Maple Class!'),
    ('#kids/Maple%20Class', 'kids', 'Welcome, Maple Class!'),
    ('#kids/%3Cscript%3Ealert(1)%3C%2Fscript%3E', 'kids', None),
    ('#kids/<script>', 'kids', None),
]


def check_greeting(pw, base, html, out):
    L = contract_lines()
    cases = GREETINGS + [('#kids/Maple', 'kids', 'Welcome, Maple Class!', '?level=bogus')]
    for c in cases:
        frag, look, greet = c[:3]
        query = c[3] if len(c) > 3 else '?cb=verify'
        br, page, errs = open_page(pw, base, html, PHONE, frag, query)
        try:
            got = page.evaluate("""() => ({ kids: document.body.classList.contains('look-kids'),
                welcome: document.getElementById('welcome').textContent, title: document.getElementById('titleLine').textContent,
                scripts: document.querySelectorAll('#welcome *').length, hash: location.hash, look: SID.LOOK })""")
            want = greet or L[look]['welcome']
            if got['kids'] != (look == 'kids') or got['look'] != look:
                out.append('greeting %r: the %s look, expected the %s look' % (frag, got['look'], look))
            if got['welcome'] != want or got['scripts']:
                out.append('greeting %r: the welcome reads %r, expected %r' % (frag, got['welcome'], want))
            if got['title'] != L[look]['title']:
                out.append('greeting %r: the title line reads %r' % (frag, got['title']))
            if frag and got['hash'].lower() != frag.lower() and '%' not in frag and '<' not in frag:
                out.append('greeting %r%s: the fragment became %r' % (frag, query, got['hash']))
            if errs:
                out.append('greeting %r: page error %s' % (frag, errs[0][:120]))
        finally:
            br.close()


FIT_JS = r"""(sel) => {
  const f = document.querySelector('.site-footer');
  const fixed = f && getComputedStyle(f).position === 'fixed';
  const fold = window.innerHeight - (fixed ? f.getBoundingClientRect().height : 0);
  const els = [...document.querySelectorAll(sel)].filter(e => e.getBoundingClientRect().height > 0);
  const bottom = els.length ? Math.max(...els.map(e => e.getBoundingClientRect().bottom + window.scrollY)) : null;
  return { n: els.length, bottom: bottom, fold: fold, sw: document.documentElement.scrollWidth, vw: window.innerWidth };
}"""


def fit(page, sel, what, out):
    page.evaluate('window.scrollTo(0, 0)')
    f = page.evaluate(FIT_JS, sel)
    if not f['n']:
        out.append('%s: nothing on screen for %s' % (what, sel))
    elif f['bottom'] > f['fold'] + 0.5:
        out.append('%s: %s ends at %.0f px, below the fold at %.0f px' % (what, sel, f['bottom'], f['fold']))
    if f['sw'] > f['vw']:
        out.append('%s: the page scrolls sideways (%d > %d)' % (what, f['sw'], f['vw']))


def play(page, look, m, out):
    L = contract_lines()[look]
    page.evaluate("() => { window.__ev = []; window.__sub = []; }")
    page.evaluate('(m) => SID.ui.start(m)', m)
    st = int(m[-1])
    tag = '%s %s' % (look, m)
    seen, right, k, unpeeked = [], 0, 0, 0
    for _ in range(300):
        s = page.evaluate('SID.ui.state()')
        if s == 'over':
            break
        if s == 'mask':
            q = page.evaluate('SID.ui.question()')
            seen.append(q['id'])
            if k < 2:
                fit(page, '#unmaskBtn', '%s %s (the disguise)' % (tag, q['id']), out)
            page.evaluate('SID.ui.unmask()')
            if k < 2:
                fit(page, '#tiles .tile', '%s %s (the tiles)' % (tag, q['id']), out)
            page.evaluate('(v) => SID.ui.tile(v)', q['little_answer'] if k % 2 == 0 else q['little_answer'] + 1)
            continue
        if s == 'big':
            q = page.evaluate('SID.ui.question()')
            if not seen or seen[-1] != q['id']:
                seen.append(q['id'])
            if k < 2:
                fit(page, '#opts .opt', '%s %s (the options)' % (tag, q['id']), out)
            ok = k % 3 != 1
            peeked = st == 3 and k % 4 == 0
            if peeked:
                page.evaluate('SID.ui.peek()')
            page.evaluate('(r) => SID.ui.answer(r)', ok)
            if k < 2:
                fit(page, '#feedback .maffs-next, #nextBtn', '%s %s (Next)' % (tag, q['id']), out)
            right += 1 if ok else 0
            unpeeked += 1 if ok and not peeked else 0
            k += 1
            continue
        page.evaluate('SID.ui.next()')
    if page.evaluate('SID.ui.state()') != 'over':
        out.append('%s: the run did not finish' % tag)
        return
    if len(seen) != PER or len(set(seen)) != PER or any(not x.startswith('s%d_' % st) for x in seen):
        out.append('%s: the run served %s, not %d different stage %d items' % (tag, seen, PER, st))
    ev = page.evaluate('window.__ev')
    sub = page.evaluate('window.__sub')
    done = [p for n, p in ev if n == 'game_completed']
    if len(done) != 1 or done[0].get('score') != right or done[0].get('level') != 'year6' or done[0].get('mode') != m:
        out.append('%s: game_completed %s, expected one with score %d' % (tag, done, right))
    if sub != [[SLUG, m, right, PER]]:
        out.append('%s: the leaderboard got %s, expected one submission on %s with %d' % (tag, sub, m, right))
    qa = [p for n, p in ev if n == 'question_answered']
    if len(qa) != PER or [p.get('question_id') for p in qa] != seen or any(p.get('mode') != m or p.get('level') != 'year6' for p in qa):
        out.append('%s: question_answered %s, expected one per item with its id' % (tag, [p.get('question_id') for p in qa]))
    names = sorted({n for n, _ in ev})
    if not set(names) <= {'game_started', 'question_answered', 'game_completed', 'personal_best_set'}:
        out.append('%s: events %s' % (tag, names))
    blob = json.dumps(ev)
    for bad in ('kids', 'Maple', '#'):
        if bad in blob:
            out.append('%s: an mfg() payload contains %r' % (tag, bad))
    if bad_in_storage(page):
        out.append('%s: browser storage holds %s' % (tag, bad_in_storage(page)))
    end = page.evaluate("document.getElementById('endLine').textContent")
    if end != L['end']:
        out.append('%s: the end line reads %r' % (tag, end))
    score = page.evaluate("document.getElementById('resScore').textContent")
    if score != str(right):
        out.append('%s: the end screen shows %s, not %d' % (tag, score, right))
    if st == 3:
        np = page.evaluate("(document.getElementById('noPeek') || {}).textContent || ''")
        if np != 'Done without peeking: %d of %d' % (unpeeked, PER):
            out.append('%s: the end screen reads %r, expected "Done without peeking: %d of %d"' % (tag, np, unpeeked, PER))
    page.evaluate("document.getElementById('menuBtn').click()")


def bad_in_storage(page):
    dump = page.evaluate("""() => { const o = {};
      for (const s of [localStorage, sessionStorage]) for (let i = 0; i < s.length; i++) o[s.key(i)] = s.getItem(s.key(i));
      return JSON.stringify(o); }""")
    return [b for b in ('kids', 'Maple', '#') if b in dump]


def check(html, out, units, shard=None):
    unit = shard.unit if shard is not None else (lambda uid: contextlib.nullcontext())
    info = {}
    if 'bank' in units:
        with unit('bank'):
            try:
                check_bank(html, out, info)
                check_source(html, out)
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
                    if uid == 'greeting':
                        try:
                            check_greeting(pw, base, html, out)
                            info['greeting'] = len(GREETINGS) + 1
                        except Exception as e:  # noqa: BLE001
                            out.append('greeting threw: %s' % str(e).splitlines()[0][:220])
                        continue
                    look = 'kids' if ' kids' in uid else 'grown'
                    frag = '#kids/Maple' if look == 'kids' else ''
                    size = PHONE if uid.startswith('play') else (1280, 800)
                    br, page, errs = open_page(pw, base, html, size, frag)
                    try:
                        if not page.evaluate("document.body.classList.contains('look-kids')") == (look == 'kids'):
                            out.append('%s: the page is not in the %s look' % (uid, look))
                        if uid.startswith('marking'):
                            check_marking(page, html, look, out, info)
                        else:
                            for m in MODES:
                                play(page, look, m, out)
                            info['played'] = info.get('played', 0) + len(MODES)
                    except Exception as e:  # noqa: BLE001
                        out.append('%s threw: %s' % (uid, str(e).splitlines()[0][:220]))
                    out.extend('page error (%s): %s' % (uid, e) for e in errs if 'production host' not in e)
                    br.close()
    finally:
        proc.terminate()
    return info


# Each plant: (what, edit(html) -> html, the unit it needs, the pattern its finding must match). The nine the contract names.
def edit(old, new):
    return lambda html, what: pc.apply_plant(html, old, new, name=what)


PLANTS = [
    ('an answer 1 out',
     edit('{"id":"s1_001","stage":1,"type":"ones","big":[56,3],"little":[6,3],"little_answer":9,"answer":59,',
          '{"id":"s1_001","stage":1,"type":"ones","big":[56,3],"little":[6,3],"little_answer":9,"answer":60,'),
     'bank', r's1_001: answer 60, recomputed 59'),
    ('a decoy equal to the answer',
     edit('{"id":"s2_001","stage":2,"type":"tens","big":[40,50],"little":[4,5],"little_answer":9,"answer":90,"decoys":{"forgot_disguise":9,"extra_zero":900,"ones":45}}',
          '{"id":"s2_001","stage":2,"type":"tens","big":[40,50],"little":[4,5],"little_answer":9,"answer":90,"decoys":{"forgot_disguise":9,"extra_zero":900,"ones":90}}'),
     'bank', r's2_001: a decoy equals the answer'),
    ('a Stage 1 item that crosses a ten',
     edit('{"id":"s1_001","stage":1,"type":"ones","big":[56,3],"little":[6,3],"little_answer":9,"answer":59,"decoys":{"tens":86,"concat":509,"off_by_one":60}}',
          '{"id":"s1_001","stage":1,"type":"ones","big":[58,3],"little":[8,3],"little_answer":11,"answer":61,"decoys":{"tens":88,"concat":5011,"off_by_one":62}}'),
     'bank', r's1_001: a ones item crosses a ten'),
    ("a Stage 5 item that doesn't cross a ten",
     edit('{"id":"s5_011","stage":5,"type":"cross","big":[19,3],"little":[9,3],"little_answer":12,"answer":22,"decoys":{"forgot_ten":12,"concat":112,"off_by_one":23}}',
          '{"id":"s5_011","stage":5,"type":"cross","big":[15,3],"little":[5,3],"little_answer":8,"answer":18,"decoys":{"forgot_ten":8,"concat":18,"off_by_one":19}}'),
     'bank', r's5_011: a cross item does not cross a ten'),
    ('a Stage 4 decoy that is the same fact swapped',
     edit('"answer_sum":[83,1],"answer":84,"decoys":[{"kind":"changed_first","sum":[84,1]}',
          '"answer_sum":[83,1],"answer":84,"decoys":[{"kind":"changed_first","sum":[81,3]}'),
     'bank', r's4_005: Stage 4 decoy 81 \+ 3 is the same fact as 3 \+ 1'),
    ('an option marked by its rendered text',
     edit('var b = e.currentTarget, val = b.dataset.val;', 'var b = e.currentTarget, val = b.textContent;'),
     'marking grown', r'option \S+ marked wrong, expected right'),
    ('the 67 shown before marking',
     edit("    box.hidden = false;\n    MaffsLock.fresh(box);\n    if (S.flow === 'wig') {",
          "    box.hidden = false;\n    MaffsLock.fresh(box);\n    if (has67(Q)) showPop();\n    if (S.flow === 'wig') {"),
     'marking grown', r'the 67 shows before marking'),
    ('the class name written with innerHTML',
     edit("$('welcome').textContent = greeting();", "$('welcome').innerHTML = greeting();"),
     'bank', r'the greeting \(the class name\) is written with innerHTML'),
    ('"Maple" in an mfg() payload',
     edit("ev('game_started', { game_slug: SLUG, level: level, mode: mode });",
          "ev('game_started', { game_slug: SLUG, level: level, mode: mode, cls: CLASS_NAME || '' });"),
     'play kids %dx%d' % PHONE, r"an mfg\(\) payload contains 'Maple'"),
]


def selftest(html, plants=None, shard=None):
    ok = True
    for what, plant, unit_id, want in (PLANTS if plants is None else plants):
        with (shard.unit('plant: ' + what) if shard is not None else contextlib.nullcontext()):
            try:
                src = plant(html, what)
            except pc.StalePlant as e:
                print('  self-test %-58s *** %s ***' % (what, e))
                ok = False
                continue
            got, err = [], None
            try:
                check(src, got, [unit_id])
            except Exception as e:  # noqa: BLE001
                err = e
            hit = [g for g in got if re.search(want, g)]
            caught = pc.is_caught(hit, err)
            print('  self-test %-58s %s' % (what, ('caught: ' + hit[0][:90]) if caught else '*** MISSED ***' + (' (other: %s)' % got[0][:90] if got else '') + (' (error: %s)' % err if err else '')))
            ok = caught and ok
    return ok


def main():
    ap = argparse.ArgumentParser()
    bc.shard_args(ap)
    ap.add_argument('--selftest', action='store_true', help='the planted faults only')
    args = ap.parse_args()
    shard = bc.Shard(__file__, args)
    units = ['bank', 'marking grown', 'marking kids', 'greeting', 'play grown %dx%d' % PHONE, 'play kids %dx%d' % PHONE]
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
        print('%s: %d items, SHA-256 as the contract states, every number and decoy recomputed from little and the tens; coverage and the 67 counts' % (SLUG, info['bank']))
    if 'marked' in info:
        print('%s: %d item plays marked (every tile and option by dataset.val, the aha and learning lines, the 67 after marking)' % (SLUG, info['marked']))
    if 'greeting' in info:
        print('%s: %d fragments read for the look and the greeting' % (SLUG, info['greeting']))
    if 'played' in info:
        print('%s: %d runs played at %dx%d (every stage, the looks in this shard)' % (SLUG, info['played'], PHONE[0], PHONE[1]))
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
