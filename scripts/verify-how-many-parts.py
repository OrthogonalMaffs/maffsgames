#!/usr/bin/env python3
# ci-line: How Many Parts?, part 1 (every pool entry, key and named error recomputed exactly, the bar model, sessions, both levels played at 320, 390 and 1280px) | --part 1
# ci-line: How Many Parts?, part 2 (every wrong-answer screen measured at 320x568: the reason and Next above the fold) | --part 2
# ci-line: How Many Parts?, part 3 (every wrong-answer screen measured at 375x667: the reason and Next above the fold) | --part 3
# ci-line: How Many Parts?, part 4 (every wrong-answer screen measured at 390x844: the reason and Next above the fold) | --part 4
# ci-line: How Many Parts?, part 5 (fault-injection self-test: six planted faults, each caught) | --part 5
# ci-deps: games/how-many-parts/
"""Independent verification for How Many Parts? (games/how-many-parts/), built 20 Oct 2026 (contract HOW-MANY-PARTS,
verbatim in docs/handover/contracts/2026-10-20-how-many-parts.md; SR-30: checked from its first PR).

WHY THIS READS THE LIVE PAGE
-------------------------------------------------------------------------------
The game keeps every decision a student sees (the pools, every key, every option and the named error behind it,
the bar model, the worked lines) on window.HMP as plain functions, and its UI calls them through HMP. This script
loads the page under Playwright, drives THOSE functions, and recomputes everything here, in Python, with exact
fractions, from definitions written out below from the contract's words, never read back from the page.

WHAT IT ASSERTS
-------------------------------------------------------------------------------
  Pools      every stage's pool is exactly the questions this script enumerates from the stated parameters
             (denominators 2-12; stage a the same denominator, b one a multiple of the other, c neither, with a
             lowest common multiple of at most 24; proper fractions, in their simplest form in b and c; an
             answer between 0 and 1), less those where a named error equals the key in value or fewer than three
             named errors with distinct values apply (the filter, as PR 453). Each stage keeps at least 40, adding
             and taking away each at least 15.
  Questions  every pool entry, over SEEDS seeds: the key recomputed exactly and shown in its simplest form;
             three distractors, each in its simplest form, each the value of the named error it carries
             (recomputed here), none equal in value to the key or to another option; an option's name is the
             first error in the precedence order with that value; the required errors (tops and bottoms, a
             denominator changed without its numerator, the larger denominator kept, the denominators
             multiplied) fill the options before the others whenever they apply.
  Bar model  every question's model: the premise ("The denominator says how many parts. Only parts of the
             same size can be added." / "taken away."); a bar for each fraction cut into its denominator's parts
             with its numerator's parts coloured; when the denominators differ, both cut into the common number
             of parts with the right counts; the full model's last bar holds the answer (put together, or the
             taken-away parts crossed out), and its label is the unsimplified answer over the common
             denominator. Every worked solution ends on the key; every worked example starts from the value of
             the error it names.
  Sessions   SESSIONS seeds per level: Foundation 5 per built stage, Advanced 4, stages in order; no question
             twice; adding and taking away within one of half each; the bar model flagged on the first three
             of every stage and no others.
  Play       both levels, end to end, at 320x568, 390x844 and 1280x800, with the Firebase SDK blocked, read
             from what the page shows (canon 7.9): the bar model on screen exactly where flagged or after a
             wrong answer; every wrong answer shows the bar model in its feedback, the working, and a Next
             that waits; the first three named errors get the worked example (Next with no fallback), later
             ones the nudge; a right answer advances on its own; the results screen; game_started,
             question_answered (mode = the stage) and game_completed at the level played, and one score
             submitted to that level's board for the session's length. No sideways scroll on a question or
             its feedback; every option at least 44px tall; every bar's part at least 8px wide; every
             fraction drawn by KaTeX. The page is noindex (unlisted) and has no typed answer box (stages 4-6
             wait for FRACTION-FORM: no hand-rolled fraction marker).
  Self-test  six faults planted into a copy of the page (the filter cut, so a distractor can equal the key;
             the key shown unsimplified; the bar model not redrawn after a wrong answer; the feedback without
             its bar model; the fill-in errors chosen before the required ones; no worked example); each must
             FAIL.

  Phone fit  (canon 7.6.1) every pool entry, with every named error it can carry and both help forms, drawn by the
             game's own wrong-answer path at 320x568, 375x667 and 390x844: the fact, the hint and Next above the
             fold (the viewport less the 40px footer); reading order fact, hint, working, picture, Next; on a phone
             or a screen 800px tall or less the picture below Next; no sideways scroll.

    python scripts/verify-how-many-parts.py [--part 1-5] [--no-selftest] [--seeds N] [--sessions N]
    (CI runs the five parts side by side: 1 the engine and the play, 2-4 the phone fit at one size each, 5 the
    self-test; no --part runs all five)
"""
import argparse
import os
import re
import sys
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'how-many-parts'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
BUILT = ['a', 'b', 'c']
LEVELS = {'ks3': {'per': 5, 'stages': ['a', 'b', 'c', 'd']}, 'gcse': {'per': 4, 'stages': ['a', 'b', 'c', 'd', 'e', 'f']}}
MAX_PARTS = 24
ORDER = ['TB', 'DN', 'KL', 'MD', 'MULT', 'OP']
REQUIRED = {'TB', 'DN', 'KL', 'MD'}
SIZES = [(320, 568), (390, 844), (1280, 800)]


def lcm(a, b):
    return a * b // gcd(a, b)


def key_of(q):
    a, b, c, d = q['a'], q['b'], q['c'], q['d']
    return F(a, b) + F(c, d) if q['op'] == '+' else F(a, b) - F(c, d)


def named_errors(q):
    """{id: Fraction} of every named error that applies, written out from the contract's words."""
    a, b, c, d, op = q['a'], q['b'], q['c'], q['d'], q['op']
    s = 1 if op == '+' else -1
    L = lcm(b, d)
    out = {}

    def put(i, n, m):
        if n > 0 and m > 0:
            out[i] = F(n, m)
    put('TB', a + s * c, b + s * d)            # added (took away) the tops and the bottoms
    if b != d:
        put('DN', a + s * c, L)                # changed a denominator without its numerator
        put('KL', a + s * c, max(b, d))        # kept the larger denominator
    put('MD', a + s * c, b * d)                # multiplied the denominators, added the numerators
    put('MULT', a * c, b * d)                  # multiplied the fractions
    other = abs(F(a, b) - s * F(c, d))         # the other operation (larger minus smaller)
    if other > 0:
        out['OP'] = other
    return out


def distinct(errs):
    seen, out = [], []
    for i in ORDER:
        if i in errs and errs[i] not in seen:
            seen.append(errs[i])
            out.append(i)
    return out


def stage_of(b, d):
    if b == d:
        return 'a'
    if b % d == 0 or d % b == 0:
        return 'b'
    return 'c'


def expected_pools():
    pools = {'a': [], 'b': [], 'c': []}
    for b in range(2, 13):
        for d in range(2, 13):
            st = stage_of(b, d)
            if st == 'c' and lcm(b, d) > MAX_PARTS:
                continue
            for a in range(1, b):
                if st != 'a' and gcd(a, b) != 1:
                    continue
                for c in range(1, d):
                    if st != 'a' and gcd(c, d) != 1:
                        continue
                    for op in '+-':
                        q = {'a': a, 'b': b, 'op': op, 'c': c, 'd': d}
                        k = key_of(q)
                        if not (0 < k < 1):
                            continue
                        e = named_errors(q)
                        if any(v == k for v in e.values()) or len(distinct(e)) < 3:
                            continue
                        pools[st].append((a, b, op, c, d))
    return pools


def frac_of(val):
    n, _, m = val.partition('/')
    return F(int(n), int(m) if m else 1)


def simplest_text(fr):
    return str(fr.numerator) if fr.denominator == 1 else '%d/%d' % (fr.numerator, fr.denominator)


TEX_FRAC = re.compile(r'\\dfrac\{(\d+)\}\{(\d+)\}')


def tex_value(t):
    m = TEX_FRAC.fullmatch(t.strip())
    if m:
        return int(m.group(1)), int(m.group(2))
    if re.fullmatch(r'\d+', t.strip()):
        return int(t), 1
    return None


# ---------------------------------------------------------------------------------------------------------------
# Static checks, on the engine (no UI)

def check_pools(page, out):
    got = page.evaluate("() => { const o = {}; for (const s of ['a','b','c']) o[s] = HMP.POOLS[s].map(q => [q.a, q.b, q.op, q.c, q.d]); return o; }")
    want = expected_pools()
    for st in BUILT:
        g = [tuple(x) for x in got[st]]
        if sorted(g) != sorted(want[st]):
            extra = sorted(set(g) - set(want[st]))
            miss = sorted(set(want[st]) - set(g))
            out.append('pool %s: serves %d entries this script leaves out (%s...), leaves out %d it should serve (%s...)'
                       % (st, len(extra), extra[:3], len(miss), miss[:3]))
            for e in extra[:3]:
                q = dict(zip(('a', 'b', 'op', 'c', 'd'), e))
                hits = [i for i, v in named_errors(q).items() if v == key_of(q)]
                if hits:
                    out.append('pool %s: %d/%d %s %d/%d has named error(s) %s equal to the key %s'
                               % (st, e[0], e[1], e[2], e[3], e[4], hits, key_of(q)))
        if len(g) != len(set(g)):
            out.append('pool %s: an entry appears twice' % st)
        n_add = sum(1 for x in g if x[2] == '+')
        if len(g) < 40 or n_add < 15 or len(g) - n_add < 15:
            out.append('pool %s: %d entries (%d adding, %d taking away): the contract asks at least 40, each kind 15'
                       % (st, len(g), n_add, len(g) - n_add))
    return {st: len(got[st]) for st in BUILT}


QUESTIONS_JS = r"""(seeds) => {
  const out = [];
  for (const st of ['a', 'b', 'c']) for (const src of HMP.POOLS[st]) for (const s of seeds) {
    const q = HMP.makeQuestion(src, st, HMP.mulberry32(s * 7919 + src.a * 131 + src.b * 17 + src.c * 5 + src.d));
    out.push({ q, part: HMP.barModel(q, false), full: HMP.barModel(q, true), worked: HMP.worked(q),
               examples: q.choices.map(c => ({ id: c.err, lines: HMP.example(q, c.err) })) });
  }
  return out;
}"""


def check_question(q, out, where):
    k = key_of(q)
    if frac_of(q['keyVal']) != k or q['keyVal'] != simplest_text(k):
        out.append('%s: key %s, recomputed %s' % (where, q['keyVal'], simplest_text(k)))
    if tex_value(q['keyTex']) != (k.numerator, k.denominator):
        out.append('%s: the key is shown as %s, not in its simplest form %s' % (where, q['keyTex'], simplest_text(k)))
    errs = named_errors(q)
    ch = q['choices']
    if len(ch) != 3:
        out.append('%s: %d distractors, not 3' % (where, len(ch)))
    vals = [k]
    for c in ch:
        v = frac_of(c['val'])
        if c['val'] != simplest_text(v) or tex_value(c['tex']) != (v.numerator, v.denominator):
            out.append('%s: option %s (%s) is not shown in its simplest form' % (where, c['val'], c['tex']))
        if c['err'] not in errs:
            out.append('%s: option %s names %s, which does not apply here' % (where, c['val'], c['err']))
        elif errs[c['err']] != v:
            out.append('%s: option %s names %s, whose value is %s' % (where, c['val'], c['err'], errs[c['err']]))
        else:
            first = [i for i in ORDER if errs.get(i) == v][0]
            if first != c['err']:
                out.append('%s: option %s is named %s, but %s comes first with that value' % (where, c['val'], c['err'], first))
        if v == k:
            out.append('%s: option %s is equal in value to the key %s' % (where, c['val'], simplest_text(k)))
        elif v in vals[1:]:
            out.append('%s: option %s twice' % (where, c['val']))
        vals.append(v)
    req = [i for i in distinct(errs) if i in REQUIRED]
    picked = [c['err'] for c in ch]
    if len(req) >= 3 and any(i not in REQUIRED for i in picked):
        out.append('%s: a fill-in error %s was chosen while required ones applied (%s)' % (where, picked, req))
    if len(req) < 3 and not set(req) <= set(picked):
        out.append('%s: required error(s) %s left out (%s)' % (where, sorted(set(req) - set(picked)), picked))


def check_bars(q, part, full, out, where):
    a, b, c, d, op = q['a'], q['b'], q['c'], q['d'], q['op']
    L = lcm(b, d)
    A, C = a * L // b, c * L // d
    premise = 'The denominator says how many parts. Only parts of the same size can be %s' % ('added.' if op == '+' else 'taken away.')
    for name, items in (('scaffold', part), ('feedback', full)):
        notes = [i['text'] for i in items if i['kind'] == 'note']
        if notes != [premise]:
            out.append('%s: the %s bar model does not say the premise (%s)' % (where, name, notes))
        rows = [(i['n'], i['a'], i['b'], i['gone'], tex_value(i['tex'])) for i in items if i['kind'] == 'row']
        want = [(b, a, 0, 0, (a, b)), (d, 0, c, 0, (c, d))]
        if b != d:
            want += [(L, A, 0, 0, (A, L)), (L, 0, C, 0, (C, L))]
        if name == 'feedback':
            want.append((L, A, C, 0, (A + C, L)) if op == '+' else (L, A, 0, C, (A - C, L)))
        if rows != want:
            out.append('%s: the %s bar model draws %s, expected %s' % (where, name, rows, want))


def check_worked(item, out, where):
    q = item['q']
    k = key_of(q)
    last = [l for l in item['worked'] if l['kind'] == 'tex'][-1]['tex']
    end = last.split('=')[-1].strip()
    if tex_value(end) != (k.numerator, k.denominator):
        out.append('%s: the working ends on %s, not the key %s' % (where, end, simplest_text(k)))
    errs = named_errors(q)
    for ex in item['examples']:
        first = ex['lines'][0]
        if first['kind'] != 'tex':
            out.append('%s: the worked example for %s does not start with what the student did' % (where, ex['id']))
            continue
        got = [F(int(n), int(m)) for n, m in TEX_FRAC.findall(first['tex'].split('\\to')[-1])]
        if not got or got[0] != errs.get(ex['id']):
            out.append('%s: the worked example for %s starts from %s, the error gives %s' % (where, ex['id'], got, errs.get(ex['id'])))


def check_engine(page, out, seeds):
    sizes = check_pools(page, out)
    items = page.evaluate(QUESTIONS_JS, list(range(1, seeds + 1)))
    for it in items:
        q = it['q']
        where = '%s %d/%d %s %d/%d' % (q['stage'], q['a'], q['b'], q['op'], q['c'], q['d'])
        n0 = len(out)
        check_question(q, out, where)
        check_bars(q, it['part'], it['full'], out, where)
        check_worked(it, out, where)
        if len(out) - n0 and len(out) > 200:
            break
    return sizes, len(items)


SESSIONS_JS = r"""(n) => {
  const out = [];
  for (const lv of ['ks3', 'gcse']) for (let s = 1; s <= n; s++) out.push(HMP.buildSession(s * 104729 + 3, lv));
  return out;
}"""


def check_sessions(page, out, n):
    for sess in page.evaluate(SESSIONS_JS, n):
        lv = sess['level']
        L = LEVELS[lv]
        stages = [s for s in L['stages'] if s in BUILT]
        qs = sess['questions']
        tag = '%s seed %d' % (lv, sess['seed'])
        if sess['stages'] != stages or len(qs) != L['per'] * len(stages):
            out.append('%s: stages %s, %d questions; expected %s, %d' % (tag, sess['stages'], len(qs), stages, L['per'] * len(stages)))
            continue
        for i, st in enumerate(stages):
            block = qs[i * L['per']:(i + 1) * L['per']]
            if any(q['stage'] != st for q in block):
                out.append('%s: stage %s out of order' % (tag, st))
            subs = sum(1 for q in block if q['op'] == '-')
            if subs not in (L['per'] // 2, (L['per'] + 1) // 2):
                out.append('%s: stage %s takes away on %d of %d' % (tag, st, subs, L['per']))
            keys = [(q['a'], q['b'], q['op'], q['c'], q['d']) for q in block]
            if len(set(keys)) != len(keys):
                out.append('%s: stage %s repeats a question' % (tag, st))
            flags = [q['bar'] for q in block]
            if flags != [j < 3 for j in range(L['per'])]:
                out.append('%s: stage %s flags the bar model on %s (the first 3 only)' % (tag, st, flags))
        if [q['index'] for q in qs] != list(range(1, len(qs) + 1)):
            out.append('%s: question numbers %s' % (tag, [q['index'] for q in qs]))


# ---------------------------------------------------------------------------------------------------------------
# Play, in Chromium

INIT = r"""
window.__ev = [];
window.__sub = [];
Object.defineProperty(window, 'mfg', { configurable: true, get() { return (n, p) => window.__ev.push([n, p]); }, set(v) {} });
const __st = window.setTimeout;
// Game timers at a quarter of their length (the right-answer pause, Next's fallback); the worked example's
// "no fallback" stays as long as it is.
window.setTimeout = function (f, ms, ...a) { return __st(f, ms >= 2147483647 ? ms : (ms || 0) / 4, ...a); };
"""

STATE_JS = r"""() => {
  const fb = document.querySelector('#feedback');
  const help = fb.querySelector('[data-help]');
  const r = el => el ? el.getBoundingClientRect() : null;
  const bars = [...document.querySelectorAll('#qbars .bar')].map(b => ({ w: b.getBoundingClientRect().width, n: b.children.length }));
  const fbars = [...fb.querySelectorAll('[data-bars="feedback"] .bar')].map(b => ({ w: b.getBoundingClientRect().width, n: b.children.length }));
  return {
    state: HMP.ui.state(), index: HMP.ui.index(), q: HMP.ui.question(),
    screen: ['menu', 'game', 'results'].find(s => document.getElementById(s).classList.contains('active')),
    qbarsVisible: !!document.querySelector('#qbars .bar') && getComputedStyle(document.getElementById('qbars')).display !== 'none',
    bars, fbars,
    right: !!fb.querySelector('.fb-quick'), wrong: !!fb.querySelector('.fb.wrong'),
    help: help ? help.getAttribute('data-help') : null, helpErr: help ? help.getAttribute('data-err') : null,
    work: !!fb.querySelector('.fb-work .line'), next: !!fb.querySelector('button'),
    optH: [...document.querySelectorAll('#options .opt')].map(b => b.getBoundingClientRect().height),
    optKatex: [...document.querySelectorAll('#options .opt')].every(b => !!b.querySelector('.katex')),
    promptKatex: !!document.querySelector('#prompt .katex'),
    overflow: document.documentElement.scrollWidth - window.innerWidth,
    inputs: document.querySelectorAll('#qcard input').length
  };
}"""


def wait_for(page, js, ms=8000):
    page.wait_for_function(js, timeout=ms)


def play(page, level, size, out, wrong_at=(1, 2, 4, 7, 8)):
    """One full session at `level`: wrong (a named error) on the questions numbered in wrong_at, right on the rest.
    Returns the number of questions played."""
    tag = '%s %dx%d' % (level, size[0], size[1])
    page.evaluate("() => { window.__ev.length = 0; window.__sub.length = 0; }")
    page.click('.level-btn[data-level="%s"]' % level)
    page.click('#startBtn')
    wait_for(page, "() => HMP.ui.state() === 'asking'")
    wrongs, seen_after_wrong = 0, False
    n = page.evaluate("() => HMP.ui.session().questions.length")
    for i in range(1, n + 1):
        wait_for(page, "() => HMP.ui.state() === 'asking' && HMP.ui.index() === %d" % i)
        s = page.evaluate(STATE_JS)
        q = s['q']
        where = '%s Q%d (%s %d/%d %s %d/%d)' % (tag, i, q['stage'], q['a'], q['b'], q['op'], q['c'], q['d'])
        want_bar = q['bar'] or seen_after_wrong
        if s['qbarsVisible'] != want_bar:
            out.append('%s: the bar model is %s on the question; expected %s (first 3 of a stage: %s; after a wrong answer: %s)'
                       % (where, 'shown' if s['qbarsVisible'] else 'missing', 'shown' if want_bar else 'none', q['bar'], seen_after_wrong))
        for bar in s['bars']:
            if bar['n'] and bar['w'] / bar['n'] < 8:
                out.append('%s: a bar part is %.1fpx wide (at least 8)' % (where, bar['w'] / bar['n']))
        if s['overflow'] > 0:
            out.append('%s: the page scrolls sideways by %dpx' % (where, s['overflow']))
        if len(s['optH']) != 4 or min(s['optH']) < 44:
            out.append('%s: options %s (four, each at least 44px tall)' % (where, s['optH']))
        if not s['optKatex'] or not s['promptKatex']:
            out.append('%s: a fraction is not drawn by KaTeX' % where)
        if s['inputs']:
            out.append('%s: a typed answer box is on the page (stages 4-6 wait for FRACTION-FORM)' % where)
        go_wrong = i in wrong_at
        page.evaluate("""(w) => { const key = HMP.ui.question().keyVal;
            [...document.querySelectorAll('#options .opt')].find(b => w ? b.dataset.val !== key : b.dataset.val === key).click(); }""", go_wrong)
        wait_for(page, "() => !!document.querySelector('#feedback .fb-quick, #feedback .fb.wrong')")
        f = page.evaluate(STATE_JS)
        if go_wrong:
            wrongs += 1
            if not f['wrong'] or f['right']:
                out.append('%s: a wrong option was not marked wrong' % where)
            if not f['fbars']:
                out.append('%s: the feedback has no bar model' % where)
            for bar in f['fbars']:
                if bar['n'] and bar['w'] / bar['n'] < 8:
                    out.append('%s: a feedback bar part is %.1fpx wide (at least 8)' % (where, bar['w'] / bar['n']))
            if not f['work']:
                out.append('%s: the feedback has no working' % where)
            want_help = 'example' if wrongs <= 3 else 'nudge'
            if f['help'] != want_help:
                out.append('%s: named error %d got %s, expected the %s' % (where, wrongs, f['help'], want_help))
            if f['overflow'] > 0:
                out.append('%s: the feedback scrolls sideways by %dpx' % (where, f['overflow']))
            if not f['next']:
                out.append('%s: no Next after a wrong answer' % where)
            else:
                page.wait_for_timeout(150)
                if page.evaluate("() => HMP.ui.index()") != i or page.evaluate("() => HMP.ui.state()") != 'wrong':
                    out.append('%s: a wrong answer moved on without Next' % where)
                page.click('#feedback button')
            seen_after_wrong = True
        else:
            if not f['right'] or f['wrong']:
                out.append('%s: the key was not marked right' % where)
            seen_after_wrong = False
    wait_for(page, "() => document.getElementById('results').classList.contains('active')")
    ev = page.evaluate("() => window.__ev")
    sub = page.evaluate("() => window.__sub")
    names = [e[0] for e in ev]
    if names.count('game_started') != 1 or names.count('game_completed') != 1 or names.count('question_answered') != n:
        out.append('%s: events %s' % (tag, {x: names.count(x) for x in set(names)}))
    for name, p in ev:
        if p.get('game_slug') != SLUG or p.get('level') != level or 'mode' not in p:
            out.append('%s: %s sent %s' % (tag, name, p))
    modes = [p['mode'] for nm, p in ev if nm == 'question_answered']
    stages = [s for s in LEVELS[level]['stages'] if s in BUILT]
    if modes != [s for s in stages for _ in range(LEVELS[level]['per'])]:
        out.append('%s: question_answered modes %s' % (tag, modes))
    if sub != [[SLUG, level, sub[0][2] if sub else None, n]]:
        out.append('%s: submitScore calls %s (one, to %s, for %d questions)' % (tag, sub, level, n))
    page.click('#againBtn')
    return n


PHONES = [(320, 568), (375, 667), (390, 844)]
FOOTER = 40   # the fixed site footer (canon 7.6.1: measure against the viewport less it)

# Every pool entry, with every named error it can carry and both help forms, drawn by the game's own wrong-answer
# path (HMP.ui.preview), then measured: the fact, the hint and Next above the fold; reading order fact, hint,
# working, picture, Next; on a phone (600px wide or less) or a screen 800px tall or less the picture below Next; no
# sideways scroll.
PHONE_JS = r"""(fold) => {
  const bad = [], r = el => el.getBoundingClientRect();
  let n = 0;
  for (const st of ['a', 'b', 'c']) for (const src of HMP.POOLS[st]) {
    const q0 = HMP.makeQuestion(src, st, HMP.mulberry32(1));
    for (const e of HMP.distinctErrors(q0)) for (const help of ['example', 'nudge']) {
      HMP.ui.preview(src, st, e.id, help);
      window.scrollTo(0, 0);
      n++;
      const fb = document.querySelector('#feedback .fb'), v = fb.querySelector('.fb-verdict'),
        h = fb.querySelector('[data-help]'), w = fb.querySelector('.fb-work'), b = fb.querySelector('[data-bars]'),
        nx = fb.querySelector('.fb-next button');
      const where = st + ' ' + src.a + '/' + src.b + ' ' + src.op + ' ' + src.c + '/' + src.d + ' ' + e.id + ' ' + help;
      if (!nx) { bad.push(where + ': no Next'); continue; }
      const kids = [...fb.children];
      const ix = el => kids.indexOf(el.closest('#feedback .fb > *'));
      if (!(ix(v) < ix(h) && ix(h) < ix(w) && ix(w) < ix(b) && ix(b) < ix(nx))) bad.push(where + ': reading order is not fact, hint, working, picture, Next');
      if (r(h).bottom > fold + 0.5) bad.push(where + ': the hint ends at ' + Math.round(r(h).bottom) + 'px, below the fold at ' + fold + 'px');
      if (r(nx).bottom > fold + 0.5) bad.push(where + ': Next ends at ' + Math.round(r(nx).bottom) + 'px, below the fold at ' + fold + 'px');
      if (r(nx).height < 44) bad.push(where + ': Next is ' + r(nx).height + 'px tall');
      if (r(v).top < 0) bad.push(where + ': the fact starts above the screen');
      const below = r(b).top >= r(nx).bottom - 0.5;
      if ((window.innerHeight <= 800 || window.innerWidth <= 600) && !below) bad.push(where + ': the picture is above Next at ' + window.innerWidth + 'x' + window.innerHeight);
      if (document.documentElement.scrollWidth > window.innerWidth) bad.push(where + ': scrolls sideways by ' + (document.documentElement.scrollWidth - window.innerWidth) + 'px');
      if (bad.length > 4000) return { n, bad };
    }
  }
  return { n, bad };
}"""


def check_phone(page, size, out):
    page.click('#startBtn')
    wait_for(page, "() => HMP.ui.state() === 'asking'")
    res = page.evaluate(PHONE_JS, size[1] - FOOTER)
    for b in res['bad']:
        out.append('phone %dx%d: %s' % (size[0], size[1], b))
    return res['n']


def open_page(pw, base, html, size):
    br = pw.chromium.launch()
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]})
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    ctx.add_init_script(INIT)
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
    ctx.route(lambda url: bc.is_font_cdn(url), bc.serve_real_font)
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
    page.wait_for_function('!!window.HMP && !!HMP.ui && typeof katex !== "undefined"', timeout=10000)
    # The leaderboard is blocked here; record what the game would submit.
    page.evaluate("""() => { window.MaffsLeaderboard = window.MaffsLeaderboard || {};
        MaffsLeaderboard.submitScore = (g, l, s, n) => { window.__sub.push([g, l, s, n]); return Promise.resolve(); }; }""")
    return br, page, errors


def check(html, out, seeds=3, sessions=100, sizes=SIZES, engine=True, plays=True, quick=False, phones=PHONES):
    from playwright.sync_api import sync_playwright
    if 'name="robots" content="noindex"' not in html:
        out.append('the page is not noindex (the game is unlisted)')
    if re.search(r'MaffsAnswer\.|function\s+\w*[Ff]rac\w*Mark', html):
        out.append('the page marks typed fractions itself (FRACTION-FORM is the shared marker)')
    proc, base = bc.start_stub_server()
    info = {}
    try:
        with sync_playwright() as pw:
            for n, size in enumerate(sizes):
                br, page, errors = open_page(pw, base, html, size)
                try:
                    if engine and n == 0:
                        info['pools'], info['questions'] = check_engine(page, out, seeds)
                        check_sessions(page, out, sessions)
                    if plays:
                        for lv in ('ks3', 'gcse'):
                            pattern = (1, 2, 4, 7, 8) if not quick else (4,)
                            info.setdefault('played', []).append('%s %dx%d: %d' % (lv, size[0], size[1], play(page, lv, size, out, pattern)))
                    if errors:
                        out.append('page errors at %dx%d: %s' % (size[0], size[1], '; '.join(errors[:3])))
                finally:
                    br.close()
            for size in phones:
                br, page, errors = open_page(pw, base, html, size)
                try:
                    info.setdefault('phone', []).append('%dx%d: %d' % (size[0], size[1], check_phone(page, size, out)))
                    if errors:
                        out.append('page errors at %dx%d: %s' % (size[0], size[1], '; '.join(errors[:3])))
                finally:
                    br.close()
    finally:
        proc.terminate()
        proc.wait()
    return info


# Each plant: (what, old, new, which checks catch it).
PLANTS = [
    ('the filter cut: a distractor can equal the key',
     'H.servable = function (q) { return !H.errorIsKey(q) && H.distinctErrors(q).length >= 3; };',
     'H.servable = function (q) { return H.distinctErrors(q).length >= 3; };', 'engine'),
    ('the key shown unsimplified (and marked right)',
     '    q.keyTex = H.tex(k);\n', '    q.keyTex = H.tex([k[0] * 2, k[1] * 2]);\n', 'engine'),
    ('the bar model not redrawn after a wrong answer', '    barNext = true;\n', '\n', 'play'),
    ('the feedback without its bar model',
     """    h += '<div class="bars" data-bars="feedback">' + renderBars(H.barModel(q, true)) + '</div>';\n""", '\n', 'play'),
    ('the fill-in errors chosen before the required ones', 'return req.concat(fill).slice(0, 3);',
     'return fill.concat(req).slice(0, 3);', 'engine'),
    ('no worked example for a named error', 'H.HELP_EXAMPLES = 3;', 'H.HELP_EXAMPLES = 0;', 'play'),
]


def selftest(html):
    ok = True
    for what, old, new, kind in PLANTS:
        if html.count(old) != 1:
            print('  self-test %-55s *** CANNOT PLANT ***' % what)
            ok = False
            continue
        got = []
        check(html.replace(old, new), got, seeds=1, sessions=5, sizes=[(390, 844)],
              engine=kind == 'engine', plays=kind == 'play', quick=False, phones=[])
        got = [g for g in got if not g.startswith('the page')]
        ok = ok and bool(got)
        print('  self-test %-55s %s' % (what, ('caught: ' + got[0][:110]) if got else '*** MISSED ***'))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--seeds', type=int, default=3, help='seeds per pool entry (default 3)')
    ap.add_argument('--sessions', type=int, default=100, help='sessions per level (default 100)')
    ap.add_argument('--part', choices=['1', '2', '3', '4', '5'], help='one of the five parts CI runs side by side (default: all)')
    args = ap.parse_args()
    html = open(GAME, encoding='utf-8').read()
    out = []
    one = args.part in (None, '1')
    phones = [PHONES[int(args.part) - 2]] if args.part in ('2', '3', '4') else PHONES if args.part is None else []
    three = args.part in (None, '5') and not args.no_selftest
    info = check(html, out, seeds=args.seeds, sessions=args.sessions, sizes=SIZES if one else [],
                 engine=one, plays=one, phones=phones) if (one or phones) else {}
    print('%s: pools %s (after the filter); %d questions checked (every pool entry x %d seeds); %d sessions per level; played %s; '
          'wrong-answer screens measured %s'
          % (SLUG, info.get('pools'), info.get('questions', 0), args.seeds, args.sessions, ', '.join(info.get('played', [])),
             ', '.join(info.get('phone', []))))
    ok = True
    if three:
        ok = selftest(html)
    for f in out[:60]:
        print('FAIL  ' + f)
    if len(out) > 60:
        print('FAIL  ... and %d more' % (len(out) - 60))
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if out or not ok else 'PASS')
    return 1 if out or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
