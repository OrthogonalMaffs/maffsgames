#!/usr/bin/env python3
# ci-shards: Feedback that teaches, Possibly Maybe (every probability question has a one-line why equal to the last two worked lines, recomputed here from the worked lines; every plain n/d in a feedback or question string becomes KaTeX and nothing else is touched, against an independent converter on thousands of strings and dated, decimal and TeX probes; the fraction echo against exact fractions on a grid of typed answers; the page played at four phone sizes with a wide font and real KaTeX: no plain-text fraction anywhere on screen, a right answer shows Yes, the echo where the form differs, then the why, a named slip shows the why marked in the working, compare questions carry their values on the buttons and keep only the ask, Next above the fold; the planted faults, each caught) | | 3
# ci-deps: games/possibly-maybe/ schools/assets/probability-game.js schools/assets/probability-generator.js schools/assets/fraction-feedback.js
"""Independent verification for contract FEEDBACK-TEACHES (build lane, 28 Oct 2026), part 1: the probability bank, the game layer and the
Possibly, Maybe page. SR-30: checked from its first PR.

Feedback has to teach on every answer (Jon, 28 Oct): the reason after a right answer and after a named slip, the student's own fraction joined
to the stored one ("1/3 = 5/15"), fractions typeset in KaTeX (canon 7.1.1), and, for a compare question, the values on the buttons.

What is asserted, each from a code path of its own (no import of the game's or bank's code for the expected values):

  Bank     every question of every stage and slot over SEEDS seeds has a non-empty `why` equal to the last two lines of its `worked`, joined
           with a space (the one line when there is only one); the worked lines themselves are non-empty strings.
  Texify   MaffsProbabilityGame.texify against an independent Python converter on every stem, option, worked line, slip line and why the bank
           makes, and on probes it must leave alone (1/2/3, 0.5/2, and/or, \\frac{1}{2}) or convert (3/4, "1/3 = 4/12", (2/5)). After conversion
           no plain n/d remains outside the \\( \\) pairs.
  Echo     MaffsFractionFeedback.echo against exact fractions on a grid of typed answers and keys: nothing for the same form, for an
           unequal value, for an unreadable or zero-denominator answer; "student = stored" (as TeX and as plain text) for an equal value
           written another way.
  Page     the page at 375x667, 360x640, 320x568 and 390x844 (Verdana injected on the phones, KaTeX served from the pinned copy): every
           stage and slot is put on screen by itself (PM.ui.preview) and answered right (a fraction typed in a different form from the
           bank's where it may be) and wrong. No plain n/d outside KaTeX in the question, buttons or feedback; a right answer shows
           "Yes.", the echo where the forms differ (one KaTeX equation, data-echo), then the why, with a KaTeX fraction for each n/d in
           it; a wrong answer shows its slip or generic line and the last two worked lines marked (li.why) in the working; the compare
           question (the bank's 'order') has "Event X: value" on every button and only its ask in the text, and its right answer shows
           the decimals; Next on the screen; no sideways scroll.
  Plants   faults put into copies of the sources, each of which must be caught.
"""
import argparse
import itertools
import os
import re
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_common as bc  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

ROOT = bc.ROOT
SLUG = 'possibly-maybe'
FILES = {
    'page': 'games/possibly-maybe/index.html',
    'probability-generator.js': 'schools/assets/probability-generator.js',
    'probability-game.js': 'schools/assets/probability-game.js',
    'fraction-feedback.js': 'schools/assets/fraction-feedback.js',
    'answer.js': 'schools/assets/answer.js',
}
SEEDS = 20
SIZES = [(375, 667), (360, 640), (320, 568), (390, 844)]
PAGE_SEED = 3

# the independent converter: a plain n/d (not part of a longer run of digits, a decimal, a date-like n/n/n, a word, or TeX)
PLAIN = re.compile(r'(?<![\w./\\{}])(\d+)/(\d+)(?![\w/])')


def read(name):
    with open(os.path.join(ROOT, FILES[name]), encoding='utf-8') as f:
        return f.read()


def expect_texify(s):
    return PLAIN.sub(lambda m: '\\(\\frac{%s}{%s}\\)' % (m.group(1), m.group(2)), s)


def expect_why(worked):
    return ' '.join(worked[-2:])


def expect_echo(raw, key):
    m = re.match(r'^\s*(\d+)\s*/\s*(\d+)\s*$', str(raw))
    if not m or int(m.group(2)) == 0 or key['den'] <= 0:
        return None
    n, d = int(m.group(1)), int(m.group(2))
    if Fraction(n, d) != Fraction(key['num'], key['den']) or (n, d) == (key['num'], key['den']):
        return None
    return {'tex': '\\frac{%d}{%d} = \\frac{%d}{%d}' % (n, d, key['num'], key['den']), 'plain': '%d/%d = %d/%d' % (n, d, key['num'], key['den'])}


# ---------------------------------------------------------------- pure: bank, texify, echo
QUESTIONS_JS = """([seeds]) => {
  const B = window.MaffsProbability, out = [];
  for (let st = 1; st <= 5; st++) for (let sl = 0; sl < B.SLOTS; sl++) for (const sd of seeds) {
    const q = B.question(st, sl, B.makeRng(sd * 31 + sl * 7 + st));
    out.push({ st, sl, sd, why: q.why, worked: q.worked, stem: q.stem, slips: q.slips.map(s => s.line), options: q.answer.options || [], hasWhy: 'why' in q });
  }
  return out;
}"""
TEXIFY_JS = "(xs) => xs.map(x => MaffsProbabilityGame.texify(x))"
ECHO_JS = "(ps) => ps.map(([r, k]) => MaffsFractionFeedback.echo(r, k))"

PROBES_KEEP = ['1/2/3', 'about 0.5/2 of them', 'and/or', '\\frac{1}{2}', 'the 12/05/2026 date', 'x/y', 'a1/2', '1/', '/2', 'no fractions here', '']
PROBES_CONVERT = ['3/4', '1/3 = 4/12', '(2/5)', 'P(red) = 1/5.', '4/5, 0.75, 78%', 'Event A: 2/5; Event B: 42%', '7/5 is over 1.', '1/2 and 3/6']


def pure(base, srcs, out):
    """Bank, texify and echo checks from the sources given."""
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page()
        pg.set_content('<html><body></body></html>')
        for n in ('answer.js', 'probability-generator.js', 'probability-game.js', 'fraction-feedback.js'):
            pg.add_script_tag(content=srcs[n])
        qs = pg.evaluate(QUESTIONS_JS, [list(range(1, SEEDS + 1))])
        strings = set(PROBES_KEEP + PROBES_CONVERT)
        for q in qs:
            tag = 's%d slot %d seed %d' % (q['st'], q['sl'], q['sd'])
            if not q['hasWhy'] or not isinstance(q['why'], str) or not q['why'].strip():
                out.append('%s: no why' % tag)
            elif q['why'] != expect_why(q['worked']):
                out.append('%s: why %r is not the last two worked lines %r' % (tag, q['why'][:70], expect_why(q['worked'])[:70]))
            if not q['worked'] or not all(isinstance(w, str) and w.strip() for w in q['worked']):
                out.append('%s: an empty worked line' % tag)
            strings.update([q['stem'], q['why'] or ''] + list(q['worked']) + list(q['slips']) + list(q['options']))
        strings = sorted(strings)
        got = pg.evaluate(TEXIFY_JS, strings)
        bad = 0
        for s, g in zip(strings, got):
            e = expect_texify(s)
            if g != e and bad < 8:
                out.append('texify(%r) = %r, expected %r' % (s[:70], g[:90], e[:90])); bad += 1
            rest = re.sub(r'\\\(.*?\\\)', '', g)
            if PLAIN.search(rest) and bad < 8:
                out.append('texify(%r) leaves a plain fraction in %r' % (s[:70], rest[:70])); bad += 1
        for s in PROBES_KEEP:
            if '\\(' in pg.evaluate(TEXIFY_JS, [s])[0]:
                out.append('texify changed %r, which has no plain fraction' % s)
        for s in PROBES_CONVERT:
            if '\\(\\frac{' not in pg.evaluate(TEXIFY_JS, [s])[0]:
                out.append('texify left %r unchanged' % s)
        keys = [{'num': n, 'den': d} for n, d in [(5, 15), (1, 3), (4, 12), (1, 2), (3, 4), (7, 5), (0, 5), (6, 6)]]
        raws = ['1/3', '5/15', '2/6', '4/12', '1/2', '2/4', '3/4', '6/8', '7/5', '14/10', '0/5', '0/9', '1/0', '1/', '/3', 'abc', '', ' 1 / 3 ', '2/3', '3/5']
        probes = [[r, k] for r in raws for k in keys]
        res = pg.evaluate(ECHO_JS, probes)
        wrong = 0
        for (r, k), g in zip(probes, res):
            e = expect_echo(r, k)
            if e is None:
                ok = g['same'] is True and g['tex'] == '' and g['plain'] == ''
            else:
                ok = g['same'] is False and g['tex'] == e['tex'] and g['plain'] == e['plain']
            if not ok and wrong < 8:
                out.append('echo(%r, %d/%d) = %r, expected %r' % (r, k['num'], k['den'], g, e)); wrong += 1
        br.close()
    return len(qs), len(strings), len(probes)


# ---------------------------------------------------------------- page
SCAN_JS = """() => {
  const re = /(^|[^\\w.\\/\\\\{}])\\d+\\/\\d+(?![\\w\\/])/;
  const out = [];
  for (const sel of ['#qtext', '#answer', '#feedback']) {
    const root = document.querySelector(sel); if (!root) continue;
    const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT); let n;
    while ((n = w.nextNode())) { if (n.parentElement.closest('.katex')) continue; if (re.test(n.nodeValue)) out.push(sel + ': ' + n.nodeValue.trim().slice(0, 80)); }
  }
  return out;
}"""
FB_JS = """() => {
  const fb = document.querySelector('#feedback'), line = fb.querySelector('.fb-line');
  const strip = el => { const c = el.cloneNode(true); c.querySelectorAll('.katex').forEach(k => k.remove()); return c.textContent.replace(/\\s+/g, ' ').trim(); };
  const nx = document.querySelector('.maffs-next, #nextBtn');
  const r = nx ? nx.getBoundingClientRect() : null;
  return { has: !!line, text: line ? strip(line) : '', katex: line ? line.querySelectorAll('.katex').length : 0,
    echo: line ? line.querySelectorAll('[data-echo] .katex').length : 0, hasEcho: !!(line && line.querySelector('[data-echo]')),
    done: !!fb.querySelector('.fb.done'), wrong: !!fb.querySelector('.fb.wrong'),
    why: [...fb.querySelectorAll('.worked li.why')].map(li => ({ text: strip(li), katex: li.querySelectorAll('.katex').length })),
    steps: fb.querySelectorAll('.worked li').length,
    nextOk: !!(r && r.width > 0 && r.top >= 0 && r.bottom <= innerHeight + 0.5), nextRect: r ? [Math.round(r.top), Math.round(r.bottom)] : null,
    wide: document.documentElement.scrollWidth - innerWidth, kx: !!window.katex };
}"""
Q_JS = """() => { const q = PM.ui.question(); return { type: q.type, kind: q.kind, stem: q.stem, askText: q.askText, compare: !!q.compare, labels: q.labels,
  options: q.options, key: q.key, simplest: !!q.simplest, why: q.why, worked: q.worked, stage: q.stage, slot: q.slot,
  buttons: [...document.querySelectorAll('#answer [data-opt]')].map(b => b.textContent.replace(/\\s+/g, ' ').trim()),
  qtext: document.querySelector('#qtext').textContent.replace(/\\s+/g, ' ').trim() }; }"""


def why_fragments(why):
    parts = re.split(r'(?<![\w./\\{}])\d+/\d+(?![\w/])', why)
    return [p.strip(' .;=,') for p in parts if p.strip(' .;=,')]


def open_page(pw, base, size, srcs, wide=True):
    br = pw.chromium.launch()
    touch = size[0] <= 600
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch)
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
    ctx.route(bc.is_font_cdn, bc.serve_real_font)                  # the pinned KaTeX, so fractions really typeset
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=srcs['page']))
    def serve(name):
        ctx.route(lambda url: url.split('?')[0].endswith('/' + name), lambda route: route.fulfill(
            status=200, content_type='application/javascript; charset=utf-8', body=srcs[name]))
    for name in ('probability-generator.js', 'probability-game.js', 'fraction-feedback.js'):
        serve(name)
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
    page.wait_for_function('!!window.PM && !!PM.ui', timeout=10000)
    page.evaluate("""() => { window.MaffsLeaderboard = window.MaffsLeaderboard || {}; MaffsLeaderboard.submitScore = () => Promise.resolve(); window.mfg = () => {}; }""")
    if wide and touch:
        page.add_style_tag(content='body,button,input{font-family:Verdana,"DejaVu Sans",sans-serif!important}')
    return br, page, errors


def alt_form(key):
    n, d = key['num'], key['den']
    g = Fraction(n, d)
    if (g.numerator, g.denominator) != (n, d):
        return '%d/%d' % (g.numerator, g.denominator)
    return '%d/%d' % (2 * n, 2 * d)


def page_check(pw, base, size, srcs, out, slots=range(1, 12), stages=(1, 2, 3, 4, 5)):
    br, page, errors = open_page(pw, base, size, srcs)
    tag0 = '%dx%d' % size
    n = 0
    try:
        for st, sl in itertools.product(stages, slots):
            tag = '%s s%d slot %d' % (tag0, st, sl)
            for right in (True, False):
                page.evaluate('([a,b,c]) => PM.ui.preview(a,b,c)', [st, sl, PAGE_SEED])
                q = page.evaluate(Q_JS)
                plain = page.evaluate(SCAN_JS)
                if plain:
                    out.append('%s: plain fraction on screen before answering: %s' % (tag, plain[0]))
                if q['type'] == 'choice':
                    if q['compare']:
                        vals = None
                        m = re.findall(r'(Event [A-Z]): ([^;]+?)(?=;|\. Which)', q['stem'])
                        vals = [(a, b.strip()) for a, b in m]
                        want = ['%s: %s' % (a, b) for a, b in vals]
                        got = [re.sub(r'\s+', ' ', b).replace('​', '') for b in q['buttons']]
                        # a KaTeX fraction reads as "5 8 8 5" in text: compare the lead (the event and a value that is not a fraction)
                        for w, g in zip(want, got):
                            lead = w.split(': ')[0]
                            if not g.startswith(lead + ': ') or ('/' not in w and w not in g):
                                out.append('%s: compare button %r does not carry %r' % (tag, g, w))
                        if len(got) != len(want) or not want:
                            out.append('%s: compare buttons %r do not match the stem values %r' % (tag, got, want))
                        if 'Event' in q['qtext'] or not q['qtext'].startswith('Which'):
                            out.append('%s: a compare question text %r should keep only the ask' % (tag, q['qtext']))
                    elif q['buttons'] and any(re.search(r'Event [A-Z]: ', b) for b in q['buttons']):
                        out.append('%s: values on the buttons of a question that is not a compare' % tag)
                typed = None
                if right and q['type'] == 'fraction' and not q['simplest']:
                    typed = alt_form(q['key'])
                    page.evaluate('(r) => PM.ui.type(r)', typed)
                elif right:
                    page.evaluate('() => PM.ui.answer(true)')
                else:
                    page.evaluate('() => PM.ui.answer(false)')
                fb = page.evaluate(FB_JS)
                plain = page.evaluate(SCAN_JS)
                if plain:
                    out.append('%s %s: plain fraction on screen: %s' % (tag, 'right' if right else 'wrong', plain[0]))
                if not fb['kx']:
                    out.append('%s: KaTeX is not loaded, so the check cannot see typeset fractions' % tag)
                if not fb['has']:
                    out.append('%s %s: no feedback line' % (tag, 'right' if right else 'wrong'))
                    continue
                n += 1
                if not fb['nextOk']:
                    out.append('%s %s: Next is not on the screen %s of %d px' % (tag, 'right' if right else 'wrong', fb['nextRect'], size[1]))
                if fb['wide'] > 1:
                    out.append('%s: sideways scroll %d px' % (tag, fb['wide']))
                nfrac = len(PLAIN.findall(q['why']))
                if right:
                    if not fb['done'] or not fb['text'].startswith('Yes.'):
                        out.append('%s: a right answer does not say Yes: %r' % (tag, fb['text'][:60])); continue
                    want_echo = typed is not None and typed != '%d/%d' % (q['key']['num'], q['key']['den'])
                    if want_echo != fb['hasEcho']:
                        out.append('%s: typed %s for key %s: echo %s, expected %s' % (tag, typed, q['key'], fb['hasEcho'], want_echo))
                    if want_echo and fb['echo'] != 1:
                        out.append('%s: the echo is %d KaTeX expressions, expected 1 (both fractions in one)' % (tag, fb['echo']))
                    if fb['katex'] != nfrac + (1 if want_echo else 0):
                        out.append('%s: %d KaTeX fractions in the feedback, expected %d (why %r)' % (tag, fb['katex'], nfrac + (1 if want_echo else 0), q['why'][:60]))
                    for frag in why_fragments(q['why']):
                        if frag not in fb['text']:
                            out.append('%s: the why %r is not in the right-answer feedback %r' % (tag, frag[:50], fb['text'][:90])); break
                    if q['kind'] == 'order':
                        for v in re.findall(r'= ([0-9.]+)', q['why']):
                            if v not in fb['text']:
                                out.append('%s: the decimal %s is not in the right-answer feedback' % (tag, v))
                else:
                    want = min(2, len(q['worked']))
                    if not fb['wrong'] or len(fb['why']) != want:
                        out.append('%s: a wrong answer marks %d working lines as the why, expected %d' % (tag, len(fb['why']), want)); continue
                    marked = ' '.join(w['text'] for w in fb['why'])
                    for frag in why_fragments(q['why']):
                        if frag not in marked:
                            out.append('%s: the why %r is not in the marked working %r' % (tag, frag[:50], marked[:90])); break
                    if sum(w['katex'] for w in fb['why']) != nfrac:
                        out.append('%s: %d KaTeX fractions in the marked working, expected %d' % (tag, sum(w['katex'] for w in fb['why']), nfrac))
                    if not fb['text'].strip():
                        out.append('%s: a wrong answer has no slip or generic line' % tag)
        if errors:
            out.append('%s: page errors: %s' % (tag0, errors[0][:120]))
    finally:
        br.close()
    return n


# ---------------------------------------------------------------- planted faults
PLANTS = [
    ('bank: why missing', 'probability-generator.js', 'why: whyOf(worked), ', '', 'pure'),
    ('bank: why is only the last worked line', 'probability-generator.js', 'worked.slice(-2).join', 'worked.slice(-1).join', 'pure'),
    ('texify: leaves plain fractions', 'probability-game.js', 'var PLAIN_FRAC = /(^|[^\\w.\\/\\\\{}])(\\d+)\\/(\\d+)(?![\\w\\/])/g;', 'var PLAIN_FRAC = /(?!)/g;', 'pure'),
    ('texify: converts a date-like 1/2/3', 'probability-game.js', '(?![\\w\\/])/g;', '/g;', 'pure'),
    ('echo: stored form first', 'fraction-feedback.js', "tex: frac(f.num, f.den) + ' = ' + frac(key.num, key.den)", "tex: frac(key.num, key.den) + ' = ' + frac(f.num, f.den)", 'pure'),
    ('echo: unequal values get an equation', 'fraction-feedback.js', 'if (f.num * key.den !== key.num * f.den) return none;', '', 'pure'),
    ('page: no echo of the typed fraction', 'page', 'MaffsFractionFeedback.echo(rawsIn[0], Q.key)', '{ tex: \'\' }', 'page'),
    ('page: compare values not on the buttons', 'probability-game.js', "return o + ': ' + b.ask.values[i];", 'return o;', 'page'),
    ('page: wrong answer does not mark the why', 'page', ' class="why"', '', 'page'),
    ('page: right answer shows only the last worked line', 'page', "renderLine(Q.why) + '</div>' +", "renderLine(Q.worked[Q.worked.length - 1]) + '</div>' +", 'page'),
    ('page: fractions drawn as plain text', 'page', 'G.texify(line).split', 'String(line).split', 'page'),
]


def planted(base, srcs, plant, out_unused=None):
    name, which, old, new, kind = plant
    s = dict(srcs)
    if old not in s[which]:
        raise RuntimeError('plant %r: the text to change is not in %s (the plant is stale)' % (name, which))
    s[which] = s[which].replace(old, new, 1)
    found = []
    if kind == 'pure':
        pure(base, s, found)
    else:
        with sync_playwright() as pw:
            page_check(pw, base, (375, 667), s, found, slots=(1, 8, 10), stages=(1, 2, 3, 4))
    return found


def main():
    ap = argparse.ArgumentParser()
    bc.shard_args(ap)
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    shard = bc.Shard(__file__, args)
    units = ['pure'] + ['page %dx%d' % s for s in SIZES] + ['plant: ' + p[0] for p in PLANTS]
    mine = shard.pick(units)
    srcs = {n: read(n) for n in FILES}
    out, ok = [], True
    proc, base = bc.start_stub_server()
    try:
        if 'pure' in mine:
            with shard.unit('pure'):
                nq, ns, npr = pure(base, srcs, out)
            print('%s: %d questions, %d strings through texify, %d echo probes' % (SLUG, nq, ns, npr))
        for s in SIZES:
            uid = 'page %dx%d' % s
            if uid in mine:
                with shard.unit(uid), sync_playwright() as pw:
                    n = page_check(pw, base, s, srcs, out)
                print('%s: %s answered %d times' % (SLUG, uid, n))
        for p in PLANTS:
            uid = 'plant: ' + p[0]
            if uid in mine:
                with shard.unit(uid):
                    got = planted(base, srcs, p)
                print('  self-test %-62s %s' % (p[0], ('caught: ' + got[0][:80]) if got else '*** MISSED ***'))
                if not got:
                    ok = False
    finally:
        proc.terminate()
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
