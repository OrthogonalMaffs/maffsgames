#!/usr/bin/env python3
# ci-line: Portal score ticker links (a score whose game has a portal card opens it, with its level only when a card lists that level and never a board key; no card means plain text; only the first set is in the Tab order and focus on a link pauses the scores; ticker_clicked carries the slug and badge; taps at least 24 px at 390 and 1280; planted faults caught) |
# ci-deps: index.html
"""Contract TICKER-LINKS (Jon, 7 Nov 2026; Amendment 1): each score in the portal's ticker is a link to its game.

    python scripts/test-ticker-links.py              # the checks at 1280 and 390, then the planted faults
    python scripts/test-ticker-links.py --no-plants

The page is served with a fake Firebase SDK, so MaffsLeaderboard.watchRecent() and standing() run unchanged on a fixed feed (FEED below,
newest first) and fixed boards. The portal's own cards are the link source; the served page gains one extra card, a second
estimation-engine card that lists only `core`, so a slug with two cards is tested on cards whose levels differ (the live portal has
none today). Checked in Chromium:

  Links     each first-set item is an <a> exactly where FEED expects, with FEED's href: ?level=<key> only when one of the slug's cards
            lists that key (gcse; alevel; core from the second card only), the bare games/<slug>/ for a board key (q20); a slug with no
            card (whose-side-are-you-on, unlisted) and an entry with no slug stay a <span> with no cue.
  Cue       a link ends "Play ->" in .play-cue, the arrow aria-hidden; not underlined at rest, underlined on hover; the accessible name
            reads "Play <game> (<level>): high score <score> by <initials>".
  Size      every link is at least 24 px tall (WCAG 2.5.8); the heights are printed.
  Keyboard  Tab from the pause button visits the first set's links in order and no link in a repeat set; the focused link has a
            visible ring and the scores stop while it has focus. Every link in a repeat set has tabindex -1.
  Clicks    with mfg() replaced by a recorder, a click on the high, weekly and plain links sends ticker_clicked once each, with
            exactly {game_slug, detail}; a click on a plain-text score sends nothing.

Plants (scripts/plant_common.py, so a plant that does not apply fails the run): a board key passed as ?level=, a repeat set's links left
focusable, a slug with no card linked, a click that sends no event, and (beyond the contract's four) no underline on hover.
"""
import argparse
import asyncio
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402
import plant_common as pc  # noqa: E402

DAY = 86400000
# (slug, levelKey, level label, score, initials, expected tag, expected href, expected detail)
FEED = [
    ('trig-wars', 'gcse', 'GCSE', 900, 'ABC', 'A', 'games/trig-wars/?level=gcse', 'high'),
    ('six-sevens-bruv', 'q20', '20 questions', 500, 'DEF', 'A', 'games/six-sevens-bruv/', 'weekly'),
    ('estimation-engine', 'core', 'Core Maths', 30, '', 'A', 'games/estimation-engine/?level=core', 'plain'),
    ('estimation-engine', 'gcse', 'GCSE', 31, 'GHI', 'A', 'games/estimation-engine/?level=gcse', 'plain'),
    ('whose-side-are-you-on', 'stage-1', 'Stage 1', 40, 'JKL', 'SPAN', None, None),
    (None, None, 'GCSE', 41, 'MNO', 'SPAN', None, None),
    ('trig-wars', 'alevel', 'A-Level', 10, 'PQR', 'A', 'games/trig-wars/?level=alevel', 'plain'),
]
# boards (Firebase keys): trig-wars gcse's best is r0's 900 (high score); six-sevens q20's week best is r1's 500 under an older 999
# (weekly best); trig-wars alevel's best is an old 50 (plain, "best: 50"); estimation-engine has no board (plain).
BOARDS = {
    'trig_wars_gcse': {'a': {'score': 900, 'ago': 1}},
    'six_sevens_bruv_q20': {'a': {'score': 999, 'ago': 9 * DAY}, 'b': {'score': 500, 'ago': 2}},
    'trig_wars_alevel': {'a': {'score': 50, 'ago': 30 * DAY}},
}
NAME0 = 'Play Trig Wars (GCSE): high score 900 by ABC'
GAME = {'trig-wars': 'Trig Wars', 'six-sevens-bruv': 'Six Sevens, Bruv', 'estimation-engine': 'Estimation Engine',
        'whose-side-are-you-on': 'whose-side-are-you-on'}

FAKE_SDK = r"""
(function () {
  var now = Date.now(), FEED = %s, BOARDS = %s, recent = {}, lb = {};
  FEED.forEach(function (f, i) {
    var e = { game: f[5], level: f[2], score: f[3], timestamp: now - (i + 1) * 60000 };
    if (f[0]) e.slug = f[0];
    if (f[1]) e.levelKey = f[1];
    if (f[4]) e.initials = f[4];
    recent['k' + i] = e;
  });
  Object.keys(BOARDS).forEach(function (b) { lb[b] = {}; Object.keys(BOARDS[b]).forEach(function (k) {
    lb[b][k] = { score: BOARDS[b][k].score, timestamp: now - BOARDS[b][k].ago }; }); });
  var DATA = { recent_scores: recent, leaderboards: lb };
  function at(path) { var o = DATA; path.split('/').forEach(function (p) { o = (o || {})[p]; }); return o || null; }
  function snap(v, order) { return { val: function () { return v; },
    forEach: function (f) { var ks = Object.keys(v || {}); if (order) ks.sort(function (a, b) { return v[a].timestamp - v[b].timestamp; });
      ks.forEach(function (k) { f({ val: function () { return v[k]; } }); }); } }; }
  function ref(path) {
    var r = { once: function () { return Promise.resolve(snap(at(path))); },
      on: function (ev, cb) { setTimeout(function () { cb(snap(at(path), true)); }, 0); },
      orderByChild: function () { return r; }, limitToLast: function () { return r; },
      push: function () { return Promise.resolve({ key: 'k' }); }, child: function (c) { return ref(path + '/' + c); } };
    return r;
  }
  window.firebase = { apps: [], initializeApp: function () { window.firebase.apps.push({}); return {}; },
                      app: function () { return {}; }, database: function () { return { ref: ref }; } };
})();
""" % (json.dumps([list(f[:5]) + [GAME.get(f[0], 'Old Game')] for f in FEED]), json.dumps(BOARDS))

# The second estimation-engine card, placed just before the real one (inside its grid).
CARD_ANCHOR = '<a href="games/estimation-engine/" class="game-card"'
EXTRA_CARD = ('<a href="games/estimation-engine/?level=core" class="game-card" data-levels="core" data-topics="number">'
              '<div class="card-title">Estimation Engine (test card)</div></a>\n  ')

ITEMS = """() => { const inner = document.querySelector('#scoreTickerTrack .score-ticker-inner'); if (!inner) return null;
  return [...inner.children].filter(e => e.classList.contains('score-ticker-item')).map(e => {
    const cue = e.querySelector('.play-cue'), arrow = cue && cue.querySelector('[aria-hidden="true"]');
    return { tag: e.tagName, href: e.getAttribute('href'), detail: e.getAttribute('data-detail'), name: e.getAttribute('aria-label'),
             tab: e.getAttribute('tabindex'), cue: cue ? cue.textContent.replace(/\\s+/g, ' ').trim() : null,
             arrowHidden: !!(arrow && arrow.textContent.trim() === '\\u2192'),
             cueLine: cue ? getComputedStyle(cue).textDecorationLine : null, aLine: getComputedStyle(e).textDecorationLine,
             h: e.getBoundingClientRect().height }; }); }"""
DUPS = """() => { const d = [...document.querySelectorAll('#scoreTickerTrack .ticker-dup')];
  const links = d.flatMap(s => [...s.querySelectorAll('a')]);
  return { sets: d.length, links: links.length, focusable: links.filter(a => a.getAttribute('tabindex') !== '-1').length,
           spans: d.flatMap(s => [...s.querySelectorAll('span.score-ticker-item .play-cue')]).length }; }"""
ACTIVE = """() => { const a = document.activeElement, inner = document.querySelector('.score-ticker-inner');
  if (!a || !inner || !inner.contains(a)) return { where: 'outside', id: a ? a.id : null };
  if (a.closest('.ticker-dup')) return { where: 'dup' };
  const first = [...inner.children].filter(e => e.tagName === 'A');
  const cs = getComputedStyle(a);
  return { where: 'first', i: first.indexOf(a), ring: cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) >= 2,
           paused: document.getElementById('scoreTicker').classList.contains('tp-focus') }; }"""
TX = """() => { const i = document.querySelector('#scoreTickerTrack .score-ticker-inner'); if (!i) return null;
  const m = getComputedStyle(i).transform; return m === 'none' ? 0 : parseFloat(m.split(',')[4]); }"""
RECORDER = """() => { window.__calls = []; window.mfg = function (n, p) { window.__calls.push([n, JSON.parse(JSON.stringify(p || {}))]); };
  document.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('#scoreTickerTrack a')) e.preventDefault(); }); }"""


async def moving(page, ms=350):
    await page.wait_for_timeout(120)
    a = await page.evaluate(TX)
    await page.wait_for_timeout(ms)
    b = await page.evaluate(TX)
    return a is not None and abs(b - a) > 0.5


async def context(browser, base, size, body):
    ctx = await browser.new_context(viewport={'width': size[0], 'height': size[1]})
    await ctx.route(re.compile(r'gstatic\.com/firebasejs/.*firebase-app-compat\.js'),
                    lambda r: r.fulfill(status=200, content_type='application/javascript', body=FAKE_SDK))
    await ctx.route(re.compile(r'gstatic\.com/firebasejs/.*firebase-database-compat\.js'),
                    lambda r: r.fulfill(status=200, content_type='application/javascript', body='/* in the app stub */'))
    await ctx.route(lambda u: not u.startswith(base) and 'gstatic.com/firebasejs' not in u, lambda r: r.abort())
    await ctx.route(re.compile(re.escape(base) + r'/$'), lambda r: r.fulfill(status=200, content_type='text/html; charset=utf-8', body=body))
    page = await ctx.new_page()
    errs = []
    page.on('pageerror', lambda e: errs.append(str(e)[:120]))
    await page.goto(base + '/', wait_until='load', timeout=20000)
    await page.wait_for_selector('#scoreTickerTrack .score-ticker-inner', timeout=8000)
    await page.wait_for_timeout(400)
    return ctx, page, errs


async def checks(browser, base, size, body, report=None):
    where = '%dx%d' % size
    f = []
    ctx, page, errs = await context(browser, base, size, body)
    try:
        f += ['%s: page error: %s' % (where, e) for e in errs]
        items = await page.evaluate(ITEMS)
        if not items or len(items) != len(FEED):
            return f + ['%s: %s first-set scores, expected %d' % (where, len(items or []), len(FEED))]
        heights = []
        for i, (it, fe) in enumerate(zip(items, FEED)):
            slug, key, tag, href, detail = fe[0], fe[1], fe[5], fe[6], fe[7]
            what = '%s: score %d (%s, %s)' % (where, i, slug, key)
            if it['tag'] != tag:
                f.append('%s is a <%s>, expected <%s>' % (what, it['tag'].lower(), tag.lower()))
                continue
            if tag == 'SPAN':
                if it['cue'] is not None:
                    f.append('%s has no card but shows a cue' % what)
                continue
            if it['href'] != href:
                f.append('%s links to %r, expected %r' % (what, it['href'], href))
            if it['detail'] != detail:
                f.append('%s carries detail %r, expected %r' % (what, it['detail'], detail))
            if it['cue'] != 'Play →' or not it['arrowHidden']:
                f.append('%s cue reads %r (arrow aria-hidden: %s), expected "Play →" with the arrow hidden' % (what, it['cue'], it['arrowHidden']))
            if it['cueLine'] != 'none' or it['aLine'] != 'none':
                f.append('%s is underlined at rest' % what)
            if it['tab'] is not None:
                f.append('%s is in the first set but has tabindex %r' % (what, it['tab']))
            heights.append(it['h'])
            if it['h'] < 24:
                f.append('%s is %.1f px tall, under 24' % (what, it['h']))
        if items[0]['name'] != NAME0:
            f.append('%s: score 0 is named %r, expected %r' % (where, items[0]['name'], NAME0))
        if report is not None and heights:
            report.append('%s: links %.1f-%.1f px tall' % (where, min(heights), max(heights)))

        d = await page.evaluate(DUPS)
        if d['sets'] < 1 or d['links'] < 1:
            f.append('%s: no repeat set with links (sets %d, links %d)' % (where, d['sets'], d['links']))
        if d['focusable']:
            f.append('%s: %d links in the repeat sets are focusable (no tabindex -1)' % (where, d['focusable']))
        if d['spans']:
            f.append('%s: a plain score in a repeat set shows a cue' % where)

        # hover underlines the cue
        await page.evaluate("() => document.getElementById('scoreTicker').scrollIntoView({block: 'center'})")
        # the first cue, brought into the track's view (at 390 the first score is wider than the screen)
        r = await page.evaluate("() => { const c = document.querySelector('.score-ticker-inner > a.score-ticker-item .play-cue');"
                                " c.scrollIntoView({block: 'nearest', inline: 'center'}); const t = document.getElementById('scoreTickerTrack').getBoundingClientRect(),"
                                " b = c.getBoundingClientRect(), x = b.left + b.width / 2;"
                                " return x > t.left + 4 && x < t.right - 4 ? [b.left, b.top, b.width, b.height] : null; }")
        if r is None:
            f.append('%s: the test could not hover a cue (none of the first set\'s cues is on screen)' % where)
        else:
            await page.mouse.move(r[0] + r[2] / 2, r[1] + r[3] / 2)
            await page.wait_for_timeout(80)
            line = await page.evaluate("() => { const h = document.querySelector('.score-ticker-inner > a.score-ticker-item:hover .play-cue'); return h ? getComputedStyle(h).textDecorationLine : null; }")
            if line != 'underline':
                f.append('%s: the cue is not underlined on hover (%r)' % (where, line))
        await page.mouse.move(2, 2)
        await page.evaluate("() => { document.getElementById('scoreTickerTrack').scrollLeft = 0; }")

        # keyboard: Tab from the pause button through the scores
        n_links = sum(1 for fe in FEED if fe[5] == 'A')
        await page.focus('#tickerToggle')
        seen = []
        for k in range(n_links + 2):
            await page.keyboard.press('Tab')
            a = await page.evaluate(ACTIVE)
            seen.append(a)
            if k == 0 and a['where'] == 'first':
                if not a['ring']:
                    f.append('%s: a keyboard-focused score link shows no focus ring' % where)
                if not a['paused'] or await moving(page):
                    f.append('%s: the scores keep moving while a score link has keyboard focus' % where)
            if a['where'] == 'outside':
                break
        firsts = [a['i'] for a in seen if a['where'] == 'first']
        if any(a['where'] == 'dup' for a in seen):
            f.append('%s: Tab reached a link in a repeat set' % where)
        if firsts != list(range(n_links)):
            f.append('%s: Tab visited first-set links %s, expected %s' % (where, firsts, list(range(n_links))))

        # clicks
        await page.evaluate(RECORDER)
        await page.click('#tickerToggle')          # stop the scores so a click lands where it aims
        await page.wait_for_timeout(80)
        for i, fe in enumerate(FEED):
            sel = '#scoreTickerTrack .score-ticker-inner > .score-ticker-item >> nth=%d' % i
            await page.evaluate("() => { window.__calls = []; }")
            await page.locator(sel).click(timeout=3000)
            await page.wait_for_timeout(30)
            calls = await page.evaluate("() => window.__calls")
            if fe[5] == 'A':
                want = [['ticker_clicked', {'game_slug': fe[0], 'detail': fe[7]}]]
                if calls != want:
                    f.append('%s: a click on score %d (%s) sent %s, expected %s' % (where, i, fe[7], calls, want))
            elif calls:
                f.append('%s: a click on plain score %d sent %s' % (where, i, calls))
    finally:
        await ctx.close()
    return f


PLANTS = [
    ('a board key passed as ?level=', "(levelKey && cardLevels[slug].indexOf(levelKey) >= 0 ? '?level=' + levelKey : '')",
     "(levelKey ? '?level=' + levelKey : '')", r"six-sevens-bruv, q20\) links to"),
    ('repeat-set links left focusable', """(dup ? ' tabindex="-1"' : '')""", "''", r'repeat sets are focusable|Tab reached a link in a repeat set'),
    ('a slug with no card linked', "if (!slug || !own.call(cardLevels, slug)) return '';",
     "if (!slug) return '';\n    if (!own.call(cardLevels, slug)) return 'games/' + slug + '/';", r'whose-side-are-you-on, stage-1\) is a <a>'),
    ('a click that sends no event', "mfg('ticker_clicked', {", "String('ticker_clicked', {", r'a click on score \d \(high\) sent \[\]'),
    ('no underline on hover', 'a.score-ticker-item:hover .play-cue,', '', r'not underlined on hover'),
]


async def run(plants):
    from playwright.async_api import async_playwright
    proc, base = bc.start_stub_server()
    html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    fails = []
    try:
        body = pc.apply_plant(html, CARD_ANCHOR, EXTRA_CARD + CARD_ANCHOR, name='the second estimation-engine card')
    except pc.StalePlant as exc:
        print('  FAIL  %s' % exc)
        return [str(exc)]
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            for size in ((1280, 800), (390, 844)):
                rep = []
                got = await checks(browser, base, size, body, rep)
                print('  %s  %dx%d%s' % ('FAIL' if got else 'ok  ', size[0], size[1], (': ' + '; '.join(got[:3])) if got else ''))
                for line in rep:
                    print('        ' + line)
                fails += got
            if plants:
                for name, old, new, want in PLANTS:
                    try:
                        planted = pc.apply_plant(body, old, new, name=name)
                    except pc.StalePlant as exc:
                        print('  FAIL  %s' % exc)
                        fails.append(str(exc))
                        continue
                    try:
                        got = await checks(browser, base, (1280, 800), planted)
                        err = None
                    except Exception as exc:     # an error while checking is never a catch
                        got, err = [], str(exc).splitlines()[0][:100]
                    if pc.is_caught([g for g in got if re.search(want, g)], err):
                        print('  ok    plant caught: %s' % name)
                    else:
                        print('  FAIL  plant NOT caught: %s (%s)' % (name, err or got[:2]))
                        fails.append('plant not caught: ' + name)
            await browser.close()
    finally:
        proc.terminate()
    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-plants', action='store_true')
    a = ap.parse_args()
    fails = asyncio.run(run(not a.no_plants))
    print('PASS' if not fails else 'FAIL: %d' % len(fails))
    return 0 if not fails else 1


if __name__ == '__main__':
    sys.exit(main())
