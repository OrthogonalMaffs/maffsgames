#!/usr/bin/env python3
# ci-shards: Feedback that teaches, As You Can See (every reading-charts question has a one-line why equal to the last two worked lines, recomputed here from the worked lines; every run of plain arithmetic in a feedback or question string becomes KaTeX and nothing else is touched, against an independent converter on thousands of strings and on time, week, decimal and bare-number probes; the page played at four phone sizes with a wide font and real KaTeX: no plain arithmetic anywhere on screen, a right answer shows Yes then the why, a named slip shows the why marked in the working, Next above the fold; the planted faults, each caught) | | 3
# ci-deps: games/as-you-can-see/ schools/assets/reading-charts-game.js schools/assets/reading-charts-generator.js
"""Independent verification for contract FEEDBACK-TEACHES (build lane, 28 Oct 2026), part 2: the reading-charts bank, its game layer and the
As You Can See page. SR-30: checked from its first PR.

Feedback has to teach on every answer (Jon, 28 Oct): the reason after a right answer and after a named slip, and the maths typeset in KaTeX
(canon 7.1.1). There are no fractions in this bank; its working is arithmetic (4 x 5 = 20, 30 - 20 = 10, 18 / 4 = 4.5 with the school signs),
which the page turns into KaTeX as it renders (MaffsChartsGame.texify), the bank's strings staying as written.

What is asserted, each from a code path of its own (no import of the game's or bank's code for the expected values):

  Bank     every question of every stage and slot over SEEDS seeds has a non-empty `why` equal to the last two lines of its `worked`, joined
           with a space (the one line when there is only one); the worked lines themselves are non-empty strings.
  Texify   MaffsChartsGame.texify against an independent Python converter on every stem, option, worked line, slip line and why the bank makes,
           and on probes it must leave alone (Week 12, 6pm, 2026, mid-April, 1.5, a bare number) or convert (a product, a difference with a
           negative answer, a quotient, a sum of three). After conversion no plain arithmetic remains outside the \\( \\) pairs.
  Page     the page at 375x667, 360x640, 320x568 and 390x844 (Verdana injected on the phones, KaTeX served from the pinned copy): every stage and
           slot is put on screen by itself (ACS.ui.preview) and answered right and wrong. No plain arithmetic outside KaTeX in the question, buttons
           or feedback; a right answer shows "Yes." then the why, with a KaTeX expression for each run of arithmetic in it; a wrong answer shows its
           slip or generic line and the last two worked lines marked (li.why) in the working; Next on the screen; no sideways scroll.
  Plants   faults put into copies of the sources, each of which must be caught.
"""
import argparse
import itertools
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_common as bc  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

ROOT = bc.ROOT
SLUG = 'as-you-can-see'
FILES = {
    'page': 'games/as-you-can-see/index.html',
    'reading-charts-generator.js': 'schools/assets/reading-charts-generator.js',
    'reading-charts-game.js': 'schools/assets/reading-charts-game.js',
    'answer.js': 'schools/assets/answer.js',
}
SEEDS = 20
SIZES = [(375, 667), (360, 640), (320, 568), (390, 844)]
PAGE_SEED = 3

# the independent converter: a run of numbers (a minus sign allowed before one) joined by x, /, minus, plus or equals, school signs
MINUS, TIMES, DIVIDE = '−', '×', '÷'
RUN = re.compile(r'%s?\d+(?:\.\d+)?(?:\s*[%s%s%s+=]\s*%s?\d+(?:\.\d+)?)+' % (MINUS, TIMES, DIVIDE, MINUS, MINUS))
LEFT = re.compile(r'\d\s*[%s%s%s+=]\s*\d' % (TIMES, DIVIDE, MINUS))      # plain arithmetic that must not survive outside KaTeX


def read(name):
    with open(os.path.join(ROOT, FILES[name]), encoding='utf-8') as f:
        return f.read()


def expect_texify(s):
    def tex(m):
        return '\\(' + m.group(0).replace(TIMES, '\\times ').replace(DIVIDE, '\\div ').replace(MINUS, '-') + '\\)'
    return RUN.sub(tex, s)


def expect_why(worked):
    return ' '.join(worked[-2:])


QUESTIONS_JS = """([seeds]) => {
  const B = window.MaffsReadingCharts, out = [];
  for (let st = 1; st <= 5; st++) for (let sl = 0; sl < B.SLOTS; sl++) for (const sd of seeds) {
    const q = B.question(st, sl, B.makeRng(sd * 31 + sl * 7 + st));
    out.push({ st, sl, sd, kind: q.kind, why: q.why, worked: q.worked, stem: q.stem, slips: q.slips.map(s => s.line), options: q.answer.options || [], hasWhy: 'why' in q });
  }
  return out;
}"""
TEXIFY_JS = "(xs) => xs.map(x => MaffsChartsGame.texify(x))"

PROBES_KEEP = ['Week 12', 'at 6pm', 'the year 2026', 'mid-April', 'a reading of 1.5', '20', 'Class 7E has 4 symbols.', '12 symbols and 3 halves', 'x + y', '= 20', '4 ×', '']
PROBES_CONVERT = ['4 × 5 = 20.', '10 − 20 = −10', '18 ÷ 4 = 4.5 symbols', '1 × 4 + 2 = 6.', '20 + 14 + 22 = 56', '30 − 20 = 10 and 5 + 5 = 10']


def pure(base, srcs, out):
    """Bank and texify checks from the sources given."""
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page()
        pg.set_content('<html><body></body></html>')
        for n in ('answer.js', 'reading-charts-generator.js', 'reading-charts-game.js'):
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
            if LEFT.search(rest) and bad < 8:
                out.append('texify(%r) leaves plain arithmetic in %r' % (s[:70], rest[:70])); bad += 1
        for s in PROBES_KEEP:
            if '\\(' in pg.evaluate(TEXIFY_JS, [s])[0]:
                out.append('texify changed %r, which has no run of arithmetic' % s)
        for s in PROBES_CONVERT:
            if '\\(' not in pg.evaluate(TEXIFY_JS, [s])[0]:
                out.append('texify left %r unchanged' % s)
        br.close()
    return len(qs), len(strings)


SCAN_JS = """() => {
  const re = /\\d\\s*[\\u00d7\\u00f7\\u2212+=]\\s*\\d/;
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
    done: !!fb.querySelector('.fb.done'), wrong: !!fb.querySelector('.fb.wrong'),
    why: [...fb.querySelectorAll('.worked li.why')].map(li => ({ text: strip(li), katex: li.querySelectorAll('.katex').length })),
    nextOk: !!(r && r.width > 0 && r.top >= 0 && r.bottom <= innerHeight + 0.5), nextRect: r ? [Math.round(r.top), Math.round(r.bottom)] : null,
    wide: document.documentElement.scrollWidth - innerWidth, kx: !!window.katex };
}"""
Q_JS = "() => { const q = ACS.ui.question(); return { type: q.type, kind: q.kind, stem: q.stem, why: q.why, worked: q.worked, stage: q.stage, slot: q.slot }; }"


def why_fragments(why):
    """The words of a why between its runs of arithmetic, trimmed of punctuation: each must be on screen."""
    return [p.strip(' .;=,') for p in RUN.split(why) if p.strip(' .;=,')]


def open_page(pw, base, size, srcs, wide=True):
    br = pw.chromium.launch()
    touch = size[0] <= 600
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch)
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
    ctx.route(bc.is_font_cdn, bc.serve_real_font)                  # the pinned KaTeX, so the arithmetic really typesets
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=srcs['page']))

    def serve(name):
        ctx.route(lambda url: url.split('?')[0].endswith('/' + name), lambda route: route.fulfill(
            status=200, content_type='application/javascript; charset=utf-8', body=srcs[name]))
    for name in ('reading-charts-generator.js', 'reading-charts-game.js'):
        serve(name)
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
    page.wait_for_function('!!window.ACS && !!ACS.ui', timeout=10000)
    page.evaluate("""() => { window.MaffsLeaderboard = window.MaffsLeaderboard || {}; MaffsLeaderboard.submitScore = () => Promise.resolve(); window.mfg = () => {}; }""")
    if wide and touch:
        page.add_style_tag(content='body,button,input{font-family:Verdana,"DejaVu Sans",sans-serif!important}')
    return br, page, errors


def page_check(pw, base, size, srcs, out, slots=range(1, 12), stages=(1, 2, 3, 4, 5)):
    br, page, errors = open_page(pw, base, size, srcs)
    tag0 = '%dx%d' % size
    n = 0
    try:
        for st, sl in itertools.product(stages, slots):
            tag = '%s s%d slot %d' % (tag0, st, sl)
            for right in (True, False):
                page.evaluate('([a,b,c]) => ACS.ui.preview(a,b,c)', [st, sl, PAGE_SEED])
                q = page.evaluate(Q_JS)
                plain = page.evaluate(SCAN_JS)
                if plain:
                    out.append('%s: plain arithmetic on screen before answering: %s' % (tag, plain[0]))
                page.evaluate('(r) => ACS.ui.answer(r)', right)
                fb = page.evaluate(FB_JS)
                plain = page.evaluate(SCAN_JS)
                what = 'right' if right else 'wrong'
                if plain:
                    out.append('%s %s: plain arithmetic on screen: %s' % (tag, what, plain[0]))
                if not fb['kx']:
                    out.append('%s: KaTeX is not loaded, so the check cannot see typeset arithmetic' % tag)
                if not fb['has']:
                    out.append('%s %s: no feedback line' % (tag, what))
                    continue
                n += 1
                if not fb['nextOk']:
                    out.append('%s %s: Next is not on the screen %s of %d px' % (tag, what, fb['nextRect'], size[1]))
                if fb['wide'] > 1:
                    out.append('%s: sideways scroll %d px' % (tag, fb['wide']))
                runs = len(RUN.findall(q['why']))
                if right:
                    if not fb['done'] or not fb['text'].startswith('Yes.'):
                        out.append('%s: a right answer does not say Yes: %r' % (tag, fb['text'][:60])); continue
                    if fb['katex'] != runs:
                        out.append('%s: %d KaTeX expressions in the feedback, expected %d (why %r)' % (tag, fb['katex'], runs, q['why'][:60]))
                    for frag in why_fragments(q['why']):
                        if frag not in fb['text']:
                            out.append('%s: the why %r is not in the right-answer feedback %r' % (tag, frag[:50], fb['text'][:90])); break
                else:
                    want = min(2, len(q['worked']))
                    if not fb['wrong'] or len(fb['why']) != want:
                        out.append('%s: a wrong answer marks %d working lines as the why, expected %d' % (tag, len(fb['why']), want)); continue
                    marked = ' '.join(w['text'] for w in fb['why'])
                    for frag in why_fragments(q['why']):
                        if frag not in marked:
                            out.append('%s: the why %r is not in the marked working %r' % (tag, frag[:50], marked[:90])); break
                    if sum(w['katex'] for w in fb['why']) != runs:
                        out.append('%s: %d KaTeX expressions in the marked working, expected %d' % (tag, sum(w['katex'] for w in fb['why']), runs))
                    if not fb['text'].strip():
                        out.append('%s: a wrong answer has no slip or generic line' % tag)
        if errors:
            out.append('%s: page errors: %s' % (tag0, errors[0][:120]))
    finally:
        br.close()
    return n


# ---------------------------------------------------------------- planted faults
PLANTS = [
    ('bank: why missing', 'reading-charts-generator.js', 'why: whyOf(worked), ', '', 'pure'),
    ('bank: why is only the last worked line', 'reading-charts-generator.js', 'worked.slice(-2).join', 'worked.slice(-1).join', 'pure'),
    ('texify: leaves plain arithmetic', 'reading-charts-game.js', '.replace(PLAIN_SUM, function', '.replace(/(?!)/g, function', 'pure'),
    ('texify: turns a bare number into TeX', 'reading-charts-game.js', '\\.\\d+)?)+/g;', '\\.\\d+)?)*/g;', 'pure'),
    ('page: right answer shows only the last worked line', 'page', "renderLine(Q.why) + '</div>' +", "renderLine(Q.worked[Q.worked.length - 1]) + '</div>' +", 'page'),
    ('page: wrong answer does not mark the why', 'page', ' class="why"', '', 'page'),
    ('page: arithmetic drawn as plain text', 'page', 'G.texify(line).split', 'String(line).split', 'page'),
]


def planted(base, srcs, plant):
    name, which, old, new, kind = plant
    s = dict(srcs)
    if old not in s[which]:
        return ['plant %r: the text to change is not in %s (the plant is stale)' % (name, which)]
    s[which] = s[which].replace(old, new, 1)
    found = []
    if kind == 'pure':
        pure(base, s, found)
    else:
        with sync_playwright() as pw:
            page_check(pw, base, (375, 667), s, found, slots=(1, 2, 3, 5), stages=(1, 2, 3))
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
                nq, ns = pure(base, srcs, out)
            print('%s: %d questions, %d strings through texify' % (SLUG, nq, ns))
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
