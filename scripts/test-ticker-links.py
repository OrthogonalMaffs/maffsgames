#!/usr/bin/env python3
# ci-line: Portal score ticker links (a score whose game has a portal card opens it, with its level only when a card lists that level and never a board key; a score with no card is not shown, the newest 20 listed of the latest 50 read; only the first set is in the Tab order and focus on a link pauses the scores; ticker_clicked carries the slug and badge; Firebase text shown as text, never markup; taps at least 24 px at 390 and 1280; planted faults caught) |
# ci-deps: index.html
"""Contract TICKER-LINKS (Jon, 7 Nov 2026; Amendments 1-2): each score in the portal's ticker is a link to its game.
Contract TICKER-LISTED (Jon, 27 Nov 2026): a score whose game has no portal card is not shown at all.

    python scripts/test-ticker-links.py              # the checks at 1280 and 390, then the planted faults
    python scripts/test-ticker-links.py --no-plants

The page is served with a fake Firebase SDK, so MaffsLeaderboard.watchRecent() and standing() run unchanged on a fixed feed (FEED below,
newest first) and fixed boards; the fake's limitToLast(n) keeps only the newest n, as Firebase does. The portal's own cards are the link source; the served page gains one extra card, a second
estimation-engine card that lists only `core`, so a slug with two cards is tested on cards whose levels differ (the live portal has
none today). Checked in Chromium:

  Links     each first-set item is an <a> exactly where FEED expects, with FEED's href: ?level=<key> only when one of the slug's cards
            lists that key (gcse; alevel; core from the second card only), the bare games/<slug>/ for a board key (q20); a slug with no
            card (not-a-real-game, a made-up slug; d-by-dx-why, an unlisted game) and an entry with no slug are not shown at all, and
            no score is a <span>.
  Window    (TICKER-LISTED) a feed of 30 unlisted scores then 5 listed ones still shows the 5, each a link; 30 unlisted then 25
            listed shows exactly 20; an all-unlisted feed shows "No recent scores yet".
  Cue       a link ends "Play ->" in .play-cue, the arrow aria-hidden; not underlined at rest, underlined on hover; the accessible name
            reads "Play <game> (<level>): high score <score> by <initials>".
  Size      every link is at least 24 px tall (WCAG 2.5.8); the heights are printed.
  Keyboard  Tab from the pause button visits the first set's links in order and no link in a repeat set; the focused link has a
            visible ring and the scores stop while it has focus. Every link in a repeat set has tabindex -1.
  Escaping  hostile Firebase text (initials <img src=x onerror=alert(1)>, a game name with <b>, a level with <i>) shows as literal
            text in the score and its accessible name; no element is made from it and no dialog opens.
  Clicks    with mfg() replaced by a recorder, a click on the high, weekly and plain links sends ticker_clicked once each, with
            exactly {game_slug, detail}.

Plants (scripts/plant_common.py, so a plant that does not apply fails the run): a board key passed as ?level=, a repeat set's links left
focusable, a slug with no card shown (TICKER-LISTED: it was "linked"), a click that sends no event, and (beyond the contract's four) no underline on hover; from
Amendment 2, the initials and the game name each rendered as markup; from TICKER-LISTED, an unlisted score shown and the read window
back at 20.
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
HOSTILE_INITIALS = '<img src=x onerror=alert(1)>'
HOSTILE_GAME = '<b>Bold</b> "Engine" & co'
HOSTILE_LEVEL = '<i>GCSE</i>'
# (slug, levelKey, level label, score, initials, expected tag (None: not shown), expected href, expected detail[, game name])
FEED = [
    ('trig-wars', 'gcse', 'GCSE', 900, 'ABC', 'A', 'games/trig-wars/?level=gcse', 'high'),
    ('six-sevens-bruv', 'q20', '20 questions', 500, 'DEF', 'A', 'games/six-sevens-bruv/', 'weekly'),
    ('estimation-engine', 'core', 'Core Maths', 30, '', 'A', 'games/estimation-engine/?level=core', 'plain'),
    ('estimation-engine', 'gcse', 'GCSE', 31, 'GHI', 'A', 'games/estimation-engine/?level=gcse', 'plain'),
    ('not-a-real-game', 'stage-1', 'Stage 1', 40, 'JKL', None, None, None),
    (None, None, 'GCSE', 41, 'MNO', None, None, None),
    ('d-by-dx-why', 'stage-1', 'Stage 1', 44, 'VWX', None, None, None),
    ('trig-wars', 'alevel', 'A-Level', 10, 'PQR', 'A', 'games/trig-wars/?level=alevel', 'plain'),
    # Hostile text (Amendment 2, ruling 5). The rules refuse such initials, but let `game` and `level` be any text; each must show as
    # literal text, with no element made from it.
    ('trig-wars', 'alevel', 'A-Level', 42, HOSTILE_INITIALS, 'A', 'games/trig-wars/?level=alevel', 'plain'),
    ('estimation-engine', 'gcse', HOSTILE_LEVEL, 43, 'STU', 'A', 'games/estimation-engine/?level=gcse', 'plain', HOSTILE_GAME),
]
# boards (Firebase keys): trig-wars gcse's best is r0's 900 (high score); six-sevens q20's week best is r1's 500 under an older 999
# (weekly best); trig-wars alevel's best is an old 50 (plain, "best: 50"); estimation-engine has no board (plain).
BOARDS = {
    'trig_wars_gcse': {'a': {'score': 900, 'ago': 1}},
    'six_sevens_bruv_q20': {'a': {'score': 999, 'ago': 9 * DAY}, 'b': {'score': 500, 'ago': 2}},
    'trig_wars_alevel': {'a': {'score': 50, 'ago': 30 * DAY}},
}
NAME0 = 'Play Trig Wars (GCSE): high score 900 by ABC'
NAME8 = 'Play %s (%s): score 43 by STU' % (HOSTILE_GAME, HOSTILE_LEVEL)
GAME = {'trig-wars': 'Trig Wars', 'six-sevens-bruv': 'Six Sevens, Bruv', 'estimation-engine': 'Estimation Engine',
        'not-a-real-game': 'not-a-real-game', 'd-by-dx-why': 'd by dx? Why?'}
SHOWN = [fe for fe in FEED if fe[5]]                    # what the ticker shows, in order
I_HOSTILE_INITIALS = next(i for i, fe in enumerate(SHOWN) if fe[4] == HOSTILE_INITIALS)
I_HOSTILE_GAME = next(i for i, fe in enumerate(SHOWN) if len(fe) > 8)


def rows(feed):
    return [list(f[:5]) + [f[8] if len(f) > 8 else GAME.get(f[0], 'Old Game')] for f in feed]


# TICKER-LISTED's window feeds, newest first: unlisted scores (an unlisted game and a made-up slug), then listed ones.
UNLISTED = [('d-by-dx-why' if i % 2 else 'not-a-real-game', 'stage-1', 'Stage 1', 100 + i, 'UNL', None, None, None) for i in range(30)]


def listed(n):
    return [('trig-wars', 'gcse', 'GCSE', 200 + i, 'LIS', 'A', 'games/trig-wars/?level=gcse', None) for i in range(n)]


WINDOW = [('30 unlisted then 5 listed', UNLISTED + listed(5), 5),
          ('30 unlisted then 25 listed', UNLISTED + listed(25), 20),
          ('only unlisted', UNLISTED, 0)]

FAKE_SDK_JS = r"""
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
  function snap(v, order, limit) { return { val: function () { return v; },
    forEach: function (f) { var ks = Object.keys(v || {}); if (order) ks.sort(function (a, b) { return v[a].timestamp - v[b].timestamp; });
      if (limit) ks = ks.slice(-limit);
      ks.forEach(function (k) { f({ val: function () { return v[k]; } }); }); } }; }
  function ref(path) {
    var limit = 0;
    var r = { once: function () { return Promise.resolve(snap(at(path))); },
      on: function (ev, cb) { setTimeout(function () { cb(snap(at(path), true, limit)); }, 0); },
      orderByChild: function () { return r; }, limitToLast: function (n) { limit = n; return r; },
      push: function () { return Promise.resolve({ key: 'k' }); }, child: function (c) { return ref(path + '/' + c); } };
    return r;
  }
  window.firebase = { apps: [], initializeApp: function () { window.firebase.apps.push({}); return {}; },
                      app: function () { return {}; }, database: function () { return { ref: ref }; } };
})();
"""


def fake_sdk(feed):
    return FAKE_SDK_JS % (json.dumps(rows(feed)), json.dumps(BOARDS))


FAKE_SDK = fake_sdk(FEED)

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
HOSTILE_JS = """() => { const t = document.getElementById('scoreTickerTrack'), inner = t.querySelector('.score-ticker-inner');
  const first = [...inner.children].filter(e => e.classList.contains('score-ticker-item'));
  return { img: t.querySelectorAll('img').length, b: t.querySelectorAll('b').length, i: t.querySelectorAll('i').length,
           spans: t.querySelectorAll('span.score-ticker-item').length,
           t7: first[%d] ? first[%d].textContent : '', t8: first[%d] ? first[%d].textContent : '',
           n8: first[%d] ? first[%d].getAttribute('aria-label') : null }; }""" % ((I_HOSTILE_INITIALS,) * 2 + (I_HOSTILE_GAME,) * 4)
RECORDER = """() => { window.__calls = []; window.mfg = function (n, p) { window.__calls.push([n, JSON.parse(JSON.stringify(p || {}))]); };
  document.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('#scoreTickerTrack a')) e.preventDefault(); }); }"""


async def moving(page, ms=350):
    await page.wait_for_timeout(120)
    a = await page.evaluate(TX)
    await page.wait_for_timeout(ms)
    b = await page.evaluate(TX)
    return a is not None and abs(b - a) > 0.5


async def context(browser, base, size, body, sdk=FAKE_SDK, ready='#scoreTickerTrack .score-ticker-inner'):
    ctx = await browser.new_context(viewport={'width': size[0], 'height': size[1]})
    await ctx.route(re.compile(r'gstatic\.com/firebasejs/.*firebase-app-compat\.js'),
                    lambda r: r.fulfill(status=200, content_type='application/javascript', body=sdk))
    await ctx.route(re.compile(r'gstatic\.com/firebasejs/.*firebase-database-compat\.js'),
                    lambda r: r.fulfill(status=200, content_type='application/javascript', body='/* in the app stub */'))
    await ctx.route(lambda u: not u.startswith(base) and 'gstatic.com/firebasejs' not in u, lambda r: r.abort())
    await ctx.route(re.compile(re.escape(base) + r'/$'), lambda r: r.fulfill(status=200, content_type='text/html; charset=utf-8', body=body))
    page = await ctx.new_page()
    errs = []
    page.on('pageerror', lambda e: errs.append(str(e)[:120]))
    page.on('dialog', lambda d: (errs.append('a dialog opened: %s' % d.message), asyncio.ensure_future(d.dismiss())))
    await page.goto(base + '/', wait_until='load', timeout=20000)
    await page.wait_for_selector(ready, timeout=8000)
    await page.wait_for_timeout(400)
    return ctx, page, errs


async def checks(browser, base, size, body, report=None):
    where = '%dx%d' % size
    f = []
    ctx, page, errs = await context(browser, base, size, body)
    try:
        f += ['%s: page error: %s' % (where, e) for e in errs]
        items = await page.evaluate(ITEMS)
        if not items or len(items) != len(SHOWN):
            return f + ['%s: %s first-set scores, expected %d (of %d in the feed, %d with no portal card)'
                        % (where, len(items or []), len(SHOWN), len(FEED), len(FEED) - len(SHOWN))]
        heights = []
        for i, (it, fe) in enumerate(zip(items, SHOWN)):
            slug, key, tag, href, detail = fe[0], fe[1], fe[5], fe[6], fe[7]
            what = '%s: score %d (%s, %s)' % (where, i, slug, key)
            if it['tag'] != tag:
                f.append('%s is a <%s>, expected <%s>' % (what, it['tag'].lower(), tag.lower()))
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
        hz = await page.evaluate(HOSTILE_JS)
        for tag, src in (('img', 'the initials'), ('b', 'the game name'), ('i', 'the level label')):
            if hz[tag]:
                f.append('%s: Firebase text became markup: %d <%s> element(s) made from %s' % (where, hz[tag], tag, src))
        if hz['spans']:
            f.append('%s: %d score(s) shown as a plain <span>, not a link' % (where, hz['spans']))
        if HOSTILE_INITIALS not in hz['t7']:
            f.append('%s: the hostile initials do not show as literal text (%r)' % (where, hz['t7'][:80]))
        if HOSTILE_GAME not in hz['t8'] or HOSTILE_LEVEL not in hz['t8']:
            f.append('%s: the hostile game name or level does not show as literal text (%r)' % (where, hz['t8'][:80]))
        if hz['n8'] != NAME8:
            f.append('%s: the hostile score is named %r, expected %r' % (where, hz['n8'], NAME8))
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
        n_links = len(SHOWN)
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
        for i, fe in enumerate(SHOWN):
            sel = '#scoreTickerTrack .score-ticker-inner > .score-ticker-item >> nth=%d' % i
            await page.evaluate("() => { window.__calls = []; }")
            await page.locator(sel).click(timeout=3000)
            await page.wait_for_timeout(30)
            calls = await page.evaluate("() => window.__calls")
            want = [['ticker_clicked', {'game_slug': fe[0], 'detail': fe[7]}]]
            if calls != want:
                f.append('%s: a click on score %d (%s) sent %s, expected %s' % (where, i, fe[7], calls, want))
    finally:
        await ctx.close()
    return f


WINDOW_JS = """() => { const t = document.getElementById('scoreTickerTrack'), inner = t.querySelector('.score-ticker-inner');
  const first = inner ? [...inner.children].filter(e => e.classList.contains('score-ticker-item')) : [];
  return { n: first.length, links: first.filter(e => e.tagName === 'A').map(e => e.getAttribute('href')),
           slugs: first.map(e => e.getAttribute('data-slug')), empty: !!t.querySelector('.score-ticker-empty') }; }"""


async def window_checks(browser, base, size, body):
    """TICKER-LISTED: unlisted scores at the head of the feed never crowd the listed ones out of the ticker."""
    where = '%dx%d' % size
    f = []
    for name, feed, want in WINDOW:
        ctx, page, errs = await context(browser, base, size, body, fake_sdk(feed),
                                        ready='#scoreTickerTrack .score-ticker-inner, #scoreTickerTrack .score-ticker-empty')
        try:
            f += ['%s: %s feed: page error: %s' % (where, name, e) for e in errs]
            w = await page.evaluate(WINDOW_JS)
            if w['n'] != want:
                f.append('%s: the %s feed shows %d scores, expected %d' % (where, name, w['n'], want))
            if len(w['links']) != w['n'] or any(h != 'games/trig-wars/?level=gcse' for h in w['links']):
                f.append('%s: the %s feed shows a score that is not a link to its listed game: %s' % (where, name, w['links'][:3]))
            if any(s != 'trig-wars' for s in w['slugs']):
                f.append('%s: the %s feed shows an unlisted score (%s)' % (where, name, sorted(set(w['slugs']) - {'trig-wars'})))
            if want == 0 and not w['empty']:
                f.append('%s: the %s feed does not show "No recent scores yet"' % (where, name))
        finally:
            await ctx.close()
    return f


PLANTS = [
    ('a board key passed as ?level=', "(levelKey && cardLevels[slug].indexOf(levelKey) >= 0 ? '?level=' + levelKey : '')",
     "(levelKey ? '?level=' + levelKey : '')", r"six-sevens-bruv, q20\) links to"),
    ('repeat-set links left focusable', """(dup ? ' tabindex="-1"' : '')""", "''", r'repeat sets are focusable|Tab reached a link in a repeat set'),
    ('a slug with no card shown', "return s && onPortal(s.slug);", "return s && !!s.slug;", r'first-set scores, expected|shows an unlisted score'),
    ('a click that sends no event', "mfg('ticker_clicked', {", "String('ticker_clicked', {", r'a click on score \d \(high\) sent \[\]'),
    ('no underline on hover', 'a.score-ticker-item:hover .play-cue,', '', r'not underlined on hover'),
    ('initials rendered as markup', "esc(s.initials) + '</span> &mdash; '", "s.initials + '</span> &mdash; '", r'<img> element'),
    ('a game name rendered as markup', "esc(s.game) + '</span>' + levelStr", "s.game + '</span>' + levelStr", r'<b> element'),
    # TICKER-LISTED
    ('an unlisted score shown', "return s && onPortal(s.slug);", "return !!s;", r'first-set scores, expected|shows an unlisted score'),
    ('the read window back at 20', "var TICKER_READ = 50,", "var TICKER_READ = 20,", r'30 unlisted then 5 listed feed shows 0 scores, expected 5'),
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
                if size == (1280, 800):
                    got += await window_checks(browser, base, size, body)
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
                        got += await window_checks(browser, base, (1280, 800), planted)
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
