#!/usr/bin/env python3
# ci-shards: Feedback that teaches, It's on Sale! and Who Ate All the Pies? (every percentages-money and pie-chart question has a one-line why equal to the last two worked lines, recomputed here from the worked lines; the money bank's plain working (£400 − £40 = £360, 500 × 1.08^2 = 583.2) becomes KaTeX and nothing else is touched, against an independent converter on thousands of strings and on price, percent and word probes; the pie bank's strings carry no plain arithmetic or fraction outside their TeX; both pages played at four phone sizes with a wide font and real KaTeX: no plain arithmetic or fraction on screen, a right answer shows Yes then the why, a named slip shows the why marked in the working, Next above the fold; the planted faults, each caught) | | 4
# ci-deps: games/its-on-sale/ games/who-ate-all-the-pies/ schools/assets/percentages-money-generator.js schools/assets/percentages-money-tex.js schools/assets/pie-chart-generator.js schools/assets/pie-game.js
"""Independent verification for contract FEEDBACK-TEACHES (build lane, 28 Oct 2026), part 3: the percentages-money and pie-chart banks, the pie
game layer, the new percentages-money-tex.js, and the pages of It's on Sale! and Who Ate All the Pies?. SR-30: checked from its first PR.

Feedback has to teach on every answer (Jon, 28 Oct): the reason after a right answer and after a named slip, and the maths typeset in KaTeX
(canon 7.1.1). The pie bank already writes its TeX between \\( and \\); the money bank writes plain text (£400 − £40 = £360), which the page
turns into KaTeX as it renders (MaffsPercentagesMoneyTex.texify), the bank's strings staying as written because The 6 P's copies them.

What is asserted, each from a code path of its own (no import of the game's or bank's code for the expected values):

  Bank     every question of both banks, over SEEDS seeds of every stage and slot, has a non-empty `why` equal to the last two lines of its
           `worked`, joined with a space (the one line when there is only one); the worked lines are non-empty strings.
  Texify   MaffsPercentagesMoneyTex.texify against an independent Python converter on every stem, worked line, slip line and why of the money
           bank, and on probes it must leave alone (a lone price, 10% of £240, a sign with nothing either side, a year) or convert (a
           difference, a product, a power, a sum). After conversion no plain arithmetic remains outside the \\( \\) pairs.
  Pie      no pie-bank string has plain arithmetic or a plain n/d outside its \\( \\) pairs.
  Page     both pages at 375x667, 360x640, 320x568 and 390x844 (Verdana injected on the phones, KaTeX served from the pinned copy): every stage and
           slot is put on screen by itself (preview) and answered right and wrong. No plain arithmetic or fraction outside KaTeX in the
           question, buttons or feedback; a right answer shows "Yes." then the why, with a KaTeX expression for each run in it; a wrong
           answer shows its slip or generic line and the last two worked lines of the bank marked (li.why); Next on the screen; no sideways scroll.
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
FILES = {
    'sale-page': 'games/its-on-sale/index.html',
    'pies-page': 'games/who-ate-all-the-pies/index.html',
    'percentages-money-generator.js': 'schools/assets/percentages-money-generator.js',
    'percentages-money-tex.js': 'schools/assets/percentages-money-tex.js',
    'pie-chart-generator.js': 'schools/assets/pie-chart-generator.js',
    'pie-game.js': 'schools/assets/pie-game.js',
    'answer.js': 'schools/assets/answer.js',
}
GAMES = {
    'sale': {'slug': 'its-on-sale', 'hook': 'IOS', 'page': 'sale-page', 'bank': 'MaffsPercentagesMoney', 'bankfile': 'percentages-money-generator.js',
             'served': ('percentages-money-generator.js', 'percentages-money-tex.js')},
    'pies': {'slug': 'who-ate-all-the-pies', 'hook': 'PIE', 'page': 'pies-page', 'bank': 'MaffsPieCharts', 'bankfile': 'pie-chart-generator.js',
             'served': ('pie-chart-generator.js', 'pie-game.js')},
}
SEEDS = 20
SIZES = [(375, 667), (360, 640), (320, 568), (390, 844)]
PAGE_SEED = 3

# the money converter, independently: a term is a number (pound sign before, percent sign after, whole-number power), joined by x / - + =
POUND, MINUS, TIMES, DIVIDE = '£', '−', '×', '÷'
TERM = r'%s?\d+(?:\.\d+)?%%?(?:\^\d+)?' % POUND
RUN = re.compile(r'%s(?:\s*[%s%s%s+=]\s*%s)+' % (TERM, TIMES, DIVIDE, MINUS, TERM))
LEFT = re.compile(r'\d\s*[%s%s%s+=]\s*[%s\d]' % (TIMES, DIVIDE, MINUS, POUND))     # plain arithmetic that must not survive outside KaTeX
PLAINFRAC = re.compile(r'(?<![\w./\\{}])\d+/\d+(?![\w/])')
TEXSEG = re.compile(r'\\\(.*?\\\)')


def read(name):
    with open(os.path.join(ROOT, FILES[name]), encoding='utf-8') as f:
        return f.read()


def expect_money(s):
    def tex(m):
        return '\\(' + (m.group(0).replace(POUND, '\\pounds ').replace('%', '\\%').replace(TIMES, '\\times ')
                        .replace(DIVIDE, '\\div ').replace(MINUS, '-')) + '\\)'
    return RUN.sub(tex, s)


def expect_why(worked):
    return ' '.join(worked[-2:])


QUESTIONS_JS = """([bank, seeds]) => {
  const B = window[bank], out = [];
  const mk = s => { let a = s >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ t >>> 15, t | 1); t ^= t + Math.imul(t ^ t >>> 7, t | 61); return ((t ^ t >>> 14) >>> 0) / 4294967296; }; };
  for (let st = 1; st <= 5; st++) for (let sl = 0; sl < B.SLOTS; sl++) for (const sd of seeds) {
    const q = B.question(st, sl, mk(sd * 31 + sl * 7 + st));
    out.push({ st, sl, sd, kind: q.kind, why: q.why, worked: q.worked, stem: q.stem, slips: (q.slips || []).map(s => s.line),
      options: (q.answer && q.answer.options) || [], hasWhy: 'why' in q });
  }
  return out;
}"""
TEXIFY_JS = "(xs) => xs.map(x => MaffsPercentagesMoneyTex.texify(x))"
PROBES_KEEP = ['£24', '10% of £240 is £24 (÷ 10).', '(÷ 10)', 'Year 2', 'the year 2026', '5% a year', '× 3', '= £4', '3 years', 'about 1.08', 'a 12% rise', '']
PROBES_CONVERT = ['New price = £400 − £40 = £360.', '2 × £2 = £4', '500 × 1.08^2 = 583.2', '£60 ÷ 2 = £30 (50% is a half).', '12% + 3% = 15%', '15% is £4 + £2 = £6.']


def strings_of(q):
    return [q['stem'], q['why'] or ''] + list(q['worked']) + list(q['slips']) + list(q['options'])


def pure(base, srcs, out):
    """Bank, texify and pie-string checks from the sources given."""
    counts = [0, 0]
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        for key in ('sale', 'pies'):
            g = GAMES[key]
            pg = br.new_page()
            pg.set_content('<html><body></body></html>')
            for n in ('answer.js',) + g['served']:
                pg.add_script_tag(content=srcs[n])
            qs = pg.evaluate(QUESTIONS_JS, [g['bank'], list(range(1, SEEDS + 1))])
            strings = set(PROBES_KEEP + PROBES_CONVERT) if key == 'sale' else set()
            for q in qs:
                tag = '%s s%d slot %d seed %d' % (key, q['st'], q['sl'], q['sd'])
                if not q['hasWhy'] or not isinstance(q['why'], str) or not q['why'].strip():
                    out.append('%s: no why' % tag)
                elif q['why'] != expect_why(q['worked']):
                    out.append('%s: why %r is not the last two worked lines %r' % (tag, q['why'][:70], expect_why(q['worked'])[:70]))
                if not q['worked'] or not all(isinstance(w, str) and w.strip() for w in q['worked']):
                    out.append('%s: an empty worked line' % tag)
                strings.update(strings_of(q))
            strings = sorted(strings)
            counts[0] += len(qs)
            counts[1] += len(strings)
            if key == 'sale':
                got = pg.evaluate(TEXIFY_JS, strings)
                bad = 0
                for s, gs in zip(strings, got):
                    e = expect_money(s)
                    if gs != e and bad < 8:
                        out.append('texify(%r) = %r, expected %r' % (s[:70], gs[:90], e[:90])); bad += 1
                    rest = TEXSEG.sub('', gs)
                    if LEFT.search(rest) and bad < 8:
                        out.append('texify(%r) leaves plain arithmetic in %r' % (s[:70], rest[:70])); bad += 1
                for s in PROBES_KEEP:
                    if '\\(' in pg.evaluate(TEXIFY_JS, [s])[0]:
                        out.append('texify changed %r, which has no run of arithmetic' % s)
                for s in PROBES_CONVERT:
                    if '\\(' not in pg.evaluate(TEXIFY_JS, [s])[0]:
                        out.append('texify left %r unchanged' % s)
            else:
                bad = 0
                for s in strings:
                    rest = TEXSEG.sub('', s)
                    if (LEFT.search(rest) or PLAINFRAC.search(rest) or '\\frac' in rest) and bad < 8:
                        out.append('pie string has maths outside its TeX: %r' % rest[:90]); bad += 1
            pg.close()
        br.close()
    return counts[0], counts[1]


SCAN_JS = """() => {
  const re = /\\d\\s*[\\u00d7\\u00f7\\u2212+=]\\s*[\\u00a3\\d]/, fr = /(^|[^\\w.\\/\\\\{}])\\d+\\/\\d+(?![\\w\\/])/;
  const out = [];
  for (const sel of ['#qtext', '#answer', '#feedback', '#exStem']) {
    const root = document.querySelector(sel); if (!root) continue;
    const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT); let n;
    while ((n = w.nextNode())) { if (n.parentElement.closest('.katex')) continue; if (re.test(n.nodeValue) || fr.test(n.nodeValue)) out.push(sel + ': ' + n.nodeValue.trim().slice(0, 80)); }
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


def why_runs(key, why):
    """(how many KaTeX expressions the why should draw, the words between them)."""
    if key == 'sale':
        n = len(RUN.findall(why))
        parts = RUN.split(why)
    else:
        n = len(TEXSEG.findall(why))
        parts = TEXSEG.split(why)
    return n, [p.strip(' .;=,') for p in parts if p.strip(' .;=,')]


def open_page(pw, base, size, srcs, key, wide=True):
    g = GAMES[key]
    br = pw.chromium.launch()
    touch = size[0] <= 600
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch)
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
    ctx.route(bc.is_font_cdn, bc.serve_real_font)                  # the pinned KaTeX, so the maths really typesets
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % g['slug'])
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=srcs[g['page']]))

    def serve(name):
        ctx.route(lambda url: url.split('?')[0].endswith('/' + name), lambda route: route.fulfill(
            status=200, content_type='application/javascript; charset=utf-8', body=srcs[name]))
    for name in g['served']:
        serve(name)
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % g['slug'], wait_until='load', timeout=20000)
    page.wait_for_function('!!window.%s && !!%s.ui && !!%s.ui.preview' % (g['hook'], g['hook'], g['hook']), timeout=10000)
    page.evaluate("""() => { window.MaffsLeaderboard = window.MaffsLeaderboard || {}; MaffsLeaderboard.submitScore = () => Promise.resolve(); window.mfg = () => {}; }""")
    if wide and touch:
        page.add_style_tag(content='body,button,input{font-family:Verdana,"DejaVu Sans",sans-serif!important}')
    return br, page, errors


def page_check(pw, base, size, srcs, key, out, slots=range(1, 12), stages=(1, 2, 3, 4, 5)):
    g = GAMES[key]
    hook = g['hook']
    br, page, errors = open_page(pw, base, size, srcs, key)
    tag0 = '%s %dx%d' % (key, size[0], size[1])
    n = 0
    try:
        for st, sl in itertools.product(stages, slots):
            tag = '%s s%d slot %d' % (tag0, st, sl)
            for right in (True, False):
                what = 'right' if right else 'wrong'
                page.evaluate('([a,b,c]) => %s.ui.preview(a,b,c)' % hook, [st, sl, PAGE_SEED])
                q = page.evaluate('() => { const q = %s.ui.question(); return { why: q.why, worked: q.worked, type: q.type || (q.answer && q.answer.type) }; }' % hook)
                plain = page.evaluate(SCAN_JS)
                if plain:
                    out.append('%s: plain maths on screen before answering: %s' % (tag, plain[0]))
                page.evaluate('(r) => %s.ui.answer(r)' % hook, right)
                fb = page.evaluate(FB_JS)
                plain = page.evaluate(SCAN_JS)
                if plain:
                    out.append('%s %s: plain maths on screen: %s' % (tag, what, plain[0]))
                if not fb['kx']:
                    out.append('%s: KaTeX is not loaded, so the check cannot see typeset maths' % tag)
                if not fb['has']:
                    out.append('%s %s: no feedback line' % (tag, what))
                    continue
                n += 1
                if not fb['nextOk']:
                    out.append('%s %s: Next is not on the screen %s of %d px' % (tag, what, fb['nextRect'], size[1]))
                if fb['wide'] > 1:
                    out.append('%s: sideways scroll %d px' % (tag, fb['wide']))
                runs, frags = why_runs(key, q['why'])
                if right:
                    if not fb['done'] or not fb['text'].startswith('Yes.'):
                        out.append('%s: a right answer does not say Yes: %r' % (tag, fb['text'][:60])); continue
                    if fb['katex'] != runs:
                        out.append('%s: %d KaTeX expressions in the feedback, expected %d (why %r)' % (tag, fb['katex'], runs, q['why'][:60]))
                    for frag in frags:
                        if frag not in fb['text']:
                            out.append('%s: the why %r is not in the right-answer feedback %r' % (tag, frag[:50], fb['text'][:90])); break
                else:
                    want = min(2, len(q['worked']))
                    if not fb['wrong'] or len(fb['why']) != want:
                        out.append('%s: a wrong answer marks %d working lines as the why, expected %d' % (tag, len(fb['why']), want)); continue
                    marked = ' '.join(w['text'] for w in fb['why'])
                    for frag in frags:
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
    ('money bank: why missing', 'percentages-money-generator.js', 'q.why = whyOf(q.worked);', '', 'pure'),
    ('pie bank: why is only the last worked line', 'pie-chart-generator.js', 'worked.slice(-2).join', 'worked.slice(-1).join', 'pure'),
    ('money texify: leaves plain arithmetic', 'percentages-money-tex.js', ".replace(RUN, function (m) {", ".replace(/(?!)/g, function (m) {", 'pure'),
    ('money texify: turns a lone price into TeX', 'percentages-money-tex.js', "')+', 'g');", "')*', 'g');", 'pure'),
    ('money texify: leaves the pound sign as a plain character', 'percentages-money-tex.js', ".replace(/£/g,", ".replace(/£_never/g,", 'pure'),
    ('pie bank: working written without its TeX', 'pie-chart-generator.js', "function tex(s) { return '\\\\(' + s + '\\\\)'; }", 'function tex(s) { return s; }', 'pure'),
    ('sale page: right answer shows only the last worked line', 'sale-page', "renderLine(Q.why) + '</div>'", "renderLine(Q.worked[Q.worked.length - 1]) + '</div>'", 'sale'),
    ('sale page: wrong answer does not mark the why', 'sale-page', ' class="why"', '', 'sale'),
    ('sale page: working drawn as plain text', 'sale-page', 'MaffsPercentagesMoneyTex.texify(line).split', 'String(line).split', 'sale'),
    ('pies page: right answer shows only the last worked line', 'pies-page', "renderLine(Q.why + (Q.type === 'angles' ? ' ' + allAngles(Q) : ''))", 'renderLine(Q.worked[Q.worked.length - 1])', 'pies'),
    ('pies page: wrong answer does not mark the why', 'pies-page', ' class="why"', '', 'pies'),
]


def planted(base, srcs, plant):
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
            page_check(pw, base, (375, 667), s, kind, found, slots=(1, 2, 5), stages=(1, 2))
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
    units = ['pure'] + ['page %s %dx%d' % (k, s[0], s[1]) for k in ('sale', 'pies') for s in SIZES] + ['plant: ' + p[0] for p in PLANTS]
    mine = shard.pick(units)
    srcs = {n: read(n) for n in FILES}
    out, ok = [], True
    proc, base = bc.start_stub_server()
    try:
        if 'pure' in mine:
            with shard.unit('pure'):
                nq, ns = pure(base, srcs, out)
            print('feedback-teaches: %d questions, %d strings checked' % (nq, ns))
        for k in ('sale', 'pies'):
            for s in SIZES:
                uid = 'page %s %dx%d' % (k, s[0], s[1])
                if uid in mine:
                    with shard.unit(uid), sync_playwright() as pw:
                        n = page_check(pw, base, s, srcs, k, out)
                    print('feedback-teaches: %s answered %d times' % (uid, n))
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
