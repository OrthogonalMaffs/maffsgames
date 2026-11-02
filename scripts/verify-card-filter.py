#!/usr/bin/env python3
# ci-shards: Essentials filter (the shared card filter on /essentials/, played in Chromium: every card's data-topic is its section (including Exam technique) and its data-calc is the roster's Calculator field read separately with the named CALC_ACROSS_PAPERS exception, each topic chip shows its section alone, the likely-calculator chips, search across sections, the empty message, the URL read on load and written on change, filter_applied and game_card_clicked events in the portal's v1 format with page=essentials, the sticky bar at 320x568, 360x640, 375x667, 390x844 and 1280x720; planted faults, each caught) | | 3
# ci-deps: schools/assets/card-filter.js schools/assets/card-filter.css essentials/index.html
"""Verification for the shared card filter (contract ESSENTIALS-FILTER, Jon, 29 Oct 2026; topic chips and search, then the calculator chips).

/essentials/ carries topic chips, a search box and URL state from schools/assets/card-filter.js. This checks, without
trusting the module:
  - static: every card sits in a section, carries data-topic equal to that section's id, and carries data-calc equal to
    what the roster's Calculator field says (not allowed = non-calc; required or scientific = calc; optional = both; by stage =
    both unless every stage has one value), computed here from the roster and the game's stage map, not read from the page;
    CALC_ACROSS_PAPERS names the untagged exam-technique game that applies on every paper (both); an exception with a real tag fails;
    every other untagged roster game or a card without data-calc fails (a guide to the likely paper, not enforcement);
  - the calculator chips ("Likely non-calculator" shows non-calc and both, "Likely calculator" shows calc and both) agree
    with that mapping alone and combined with a topic;
  - each topic chip, including Exam technique, shows its section's cards alone, hides the other sections, and the count is the cards counted here;
  - search narrows across sections, a word nothing matches shows the empty message and Clear filters brings every card back;
  - the URL: ?topic=&q= opens the page filtered, a change rewrites the URL without adding a history entry, an unknown
    topic or calc value is ignored;
  - events (analytics.js stubbed): filter_applied once per chip tap and once after typing stops, filter_value
    "v1|page=essentials;topic=..;su=..;sl=..;q=..;n=..", page=essentials; game_card_clicked carries the same state;
    nothing fires on load;
  - phone: chips and search 44 px tall, chip rows scroll sideways inside themselves, no sideways page scroll, the sticky bar
    at most 27% of the screen, and after a chip tap from a scrolled page the first card's whole box is on screen below the bar
    with its centre hit-testing to the card (the bar never covers a Play target).
Planted faults, each caught: a card with no data-topic, the wrong data-topic, no data-calc, the wrong data-calc, data-calc="maybe",
a module that never rewrites the URL, one that leaves empty sections showing, one that never shows the empty message,
one that fires no filter event, one that fires on load.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_common as bc  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'essentials', 'index.html')
JS = os.path.join(ROOT, 'schools', 'assets', 'card-filter.js')
CSS = os.path.join(ROOT, 'schools', 'assets', 'card-filter.css')
TOPICS = ['number', 'algebra', 'ratio', 'geometry', 'probability', 'statistics', 'technique']
CALC_VALUES = {'non-calc', 'calc', 'both'}
ROSTER = os.path.join(ROOT, '.claude', 'rules', 'game-roster.md')
ROW = re.compile(r'^\|\s*(?:\d+|\u2014)\s*\|[^|]*\|\s*`([a-z0-9-]+)`\s*\|.*\|\s*([^|]*?)\s*\|\s*$')
STAGES = re.compile(r'<script type="application/json" id="maffs-calc-stages">(.*?)</script>', re.S)


CALC_ACROSS_PAPERS = {'i-found-a-mark': "exam technique (AO3): applies on every paper; roster Calculator field stays untagged (Jon, 30 Oct 2026)"}


def expected_calc(slug, field=None, exceptions=CALC_ACROSS_PAPERS):
    """What the card's data-calc must be, from the roster's Calculator field (own reader, not the page)."""
    if field is None:
        for line in read(ROSTER).splitlines():
            m = ROW.match(line)
            if m and m.group(1) == slug:
                field = m.group(2)
    if slug in exceptions:
        if field != 'untagged':
            raise ValueError('%s: in CALC_ACROSS_PAPERS but the roster tags it %s: remove the exception' % (slug, field))
        return 'both'
    if field == 'not allowed':
        return 'non-calc'
    if field in ('required', 'scientific'):
        return 'calc'
    if field == 'optional':
        return 'both'
    if field == 'by stage':
        vals = set(json.loads(STAGES.search(read(os.path.join(ROOT, 'games', slug, 'index.html'))).group(1)).values())
        if vals == {'not allowed'}:
            return 'non-calc'
        return 'calc' if vals <= {'required', 'scientific'} else 'both'
    return None            # untagged, or not in the roster


# A calculator chip's accepted data-calc values: both counts as either.
CHIP_ACCEPTS = {'non-calculator': {'non-calc', 'both'}, 'calculator': {'calc', 'both'}}
SIZES = [(320, 568), (360, 640), (375, 667), (390, 844), (1280, 720)]
STUB_ANALYTICS = "window.__ev = []; window.mfg = function (n, p) { window.__ev.push([n, p]); };"


def _cards():
    src = read(PAGE)
    out = []
    for sid, body in re.findall(r'<section class="topic" id="([a-z]+)">(.*?)</section>', src, re.S):
        out += [(m, sid) for m in re.findall(r'<a class="card"[^>]*\bdata-slug="([a-z0-9-]+)"', body)]
    return out


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


CARDS = _cards()
ALL_SLUGS = [s for s, _ in CARDS]
TOPIC_OF = dict(CARDS)


def static_check(src, exceptions=CALC_ACROSS_PAPERS):
    """Failure strings for the page source."""
    out = []
    secs = re.findall(r'<section class="topic" id="([a-z]+)">(.*?)</section>', src, re.S)
    if [s[0] for s in secs] != TOPICS:
        out.append('sections are %s, expected %s' % ([s[0] for s in secs], TOPICS))
    total = 0
    for sid, body in secs:
        for m in re.finditer(r'<a class="card"([^>]*)>', body):
            total += 1
            attrs = m.group(0)
            name = re.search(r'data-slug="([^"]+)"', attrs)
            name = name.group(1) if name else attrs[:60]
            t = re.search(r'\bdata-topic="([^"]*)"', attrs)
            if not t:
                out.append('%s: card has no data-topic (section %s)' % (name, sid))
            elif t.group(1) != sid:
                out.append('%s: data-topic %r does not match its section %r' % (name, t.group(1), sid))
            c = re.search(r'\bdata-calc="([^"]*)"', attrs)
            try:
                want = expected_calc(name, exceptions=exceptions)
            except ValueError as e:
                out.append(str(e))
                want = None
            if want is None:
                out.append('%s: the roster Calculator field is untagged (or the game is not in the roster)' % name)
            if not c:
                out.append('%s: card has no data-calc' % name)
            elif c.group(1) not in CALC_VALUES:
                out.append('%s: data-calc %r is not one of %s' % (name, c.group(1), sorted(CALC_VALUES)))
            elif want and c.group(1) != want:
                out.append('%s: data-calc %r, but the roster says %r' % (name, c.group(1), want))
    if total != len(re.findall(r'<a class="card"', src)):
        out.append('a card sits outside the topic sections')
    if total < 30:
        out.append('only %d cards found; the page changed shape and this check is blind' % total)
    return out


def open_page(pw, base, size, query='', sources=None):
    sources = sources or {}
    br = pw.chromium.launch()
    touch = size[0] <= 600
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch)
    ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
    ctx.route(lambda url: url.split('?')[0].endswith('/schools/assets/analytics.js'), lambda route: route.fulfill(
        status=200, content_type='application/javascript', body=STUB_ANALYTICS))
    def serve(match, ctype, body):
        # Playwright hands a handler (route, request): bind the body in a factory, not in default arguments.
        ctx.route(match, lambda route: route.fulfill(status=200, content_type=ctype + '; charset=utf-8', body=body))
    if 'page' in sources:
        serve(lambda url: re.search(r'/essentials/(\?[^/]*)?$', url) is not None, 'text/html', sources['page'])
    for name, ctype in (('card-filter.js', 'application/javascript'), ('card-filter.css', 'text/css')):
        if name in sources:
            serve((lambda n: lambda url: url.split('?')[0].endswith('/' + n))(name), ctype, sources[name])
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/essentials/' + query, wait_until='load', timeout=20000)
    # CI has real fonts, which wrap more than the stub's: a wide face makes the cards and the chip rows as tall as they get.
    page.add_style_tag(content='body, button, input { font-family: Verdana, "DejaVu Sans", sans-serif !important; }')
    page.wait_for_selector('.cf-bar', timeout=5000)
    return br, page, errors


COUNTS = """() => {
  const all = [...document.querySelectorAll('a.card')];
  const vis = all.filter(c => c.getClientRects().length > 0);
  const secs = [...document.querySelectorAll('section.topic')].filter(s => s.getClientRects().length > 0).map(s => s.id);
  return { total: all.length, shown: vis.length, secs, cards: vis.map(c => [c.dataset.slug, c.dataset.calc || '']), topics: [...new Set(vis.map(c => c.dataset.topic))],
           count: document.querySelector('.cf-count').textContent,
           empty: !document.querySelector('.cf-empty').hidden && document.querySelector('.cf-empty').getClientRects().length > 0,
           url: location.search, hist: history.length, q: document.querySelector('.cf-search').value };
}"""


def chip(page, key, group='topic'):
    page.locator('.cf-chip[data-cf-group="%s"][data-cf-key="%s"]' % (group, key)).click()
    page.wait_for_timeout(60)


def check_behaviour(base, out, sources=None, only=None):
    """topics / search / empty / url / events at 1280x720. `only` limits to named parts (for the planted faults)."""
    want = lambda n: only is None or n in only
    with sync_playwright() as pw:
        br, page, errors = open_page(pw, base, (1280, 720), sources=sources)
        try:
            c0 = page.evaluate(COUNTS)
            if want('load'):
                if c0['shown'] != c0['total'] or c0['total'] < 30:
                    out.append('load: %d of %d cards shown with no filter' % (c0['shown'], c0['total']))
                if page.evaluate('window.__ev.length'):
                    out.append('load: an event fired on load: %s' % page.evaluate('window.__ev'))
                expected = 1 + len(TOPICS) + 1 + 2
                if page.locator('.cf-chip').count() != expected:
                    out.append('load: %d chips, expected All plus %d topics and All plus two calculator chips (%d)' % (page.locator('.cf-chip').count(), len(TOPICS), expected))
                labels = page.locator('.cf-chip[data-cf-group="calc"]').all_inner_texts()
                if labels != ['All', 'Likely non-calculator', 'Likely calculator']:
                    out.append('load: the calculator chips read %s (guidance, so "Likely ...")' % labels)
            if want('topics'):
                for t in TOPICS:
                    n = page.locator('.cf-chip[data-cf-group="topic"][data-cf-key="%s"]' % t).count()
                    if n != 1:
                        out.append('topic %s: %d chips with data-cf-key=%r (expected exactly 1)' % (t, n, t))
                        continue
                    chip(page, t)
                    c = page.evaluate(COUNTS)
                    expect = page.evaluate("t => document.querySelectorAll('section#' + t + ' a.card').length", t)
                    if c['topics'] != [t] or c['shown'] != expect or c['secs'] != [t]:
                        out.append('topic %s: shows topics %s, sections %s, %d cards (expected only %s, %d)' % (
                            t, c['topics'], c['secs'], c['shown'], t, expect))
                    if c['count'] != '%d %s' % (expect, 'game' if expect == 1 else 'games'):
                        out.append('topic %s: count says %r' % (t, c['count']))
                chip(page, 'all')
                c = page.evaluate(COUNTS)
                if c['shown'] != c['total'] or len(c['secs']) != len(TOPICS):
                    out.append('All: %d of %d cards, %d sections' % (c['shown'], c['total'], len(c['secs'])))
            if want('calc'):
                for key in ('non-calculator', 'calculator'):
                    chip(page, key, 'calc')
                    c = page.evaluate(COUNTS)
                    exp = sorted(s for s in ALL_SLUGS if expected_calc(s) in CHIP_ACCEPTS[key])
                    if sorted(s for s, _ in c['cards']) != exp:
                        out.append('calc %s: shows %d cards, the roster says %d (%s)' % (
                            key, c['shown'], len(exp), sorted(set(exp) ^ set(s for s, _ in c['cards']))[:4]))
                    chip(page, 'statistics')
                    c = page.evaluate(COUNTS)
                    exp2 = sorted(s for s in exp if s in TOPIC_OF and TOPIC_OF[s] == 'statistics')
                    if sorted(s for s, _ in c['cards']) != exp2 or c['topics'] not in (['statistics'], []):
                        out.append('calc %s + statistics: shows %s, expected %s' % (key, [s for s, _ in c['cards']], exp2))
                    chip(page, 'all')
                    chip(page, 'all', 'calc')
                c = page.evaluate(COUNTS)
                if c['shown'] != c['total']:
                    out.append('calc All: %d of %d cards' % (c['shown'], c['total']))
            if want('search'):
                page.locator('.cf-search').fill('angle')
                page.wait_for_timeout(100)
                c = page.evaluate(COUNTS)
                names = page.evaluate("[...document.querySelectorAll('a.card')].filter(c => c.getClientRects().length).map(c => c.textContent.toLowerCase())")
                if not (0 < c['shown'] < c['total']) or any('angle' not in n for n in names):
                    out.append('search "angle": %d cards, %s' % (c['shown'], c['topics']))
                page.locator('.cf-search').fill('percent')
                page.wait_for_timeout(100)
                c = page.evaluate(COUNTS)
                if len(c['topics']) < 2:
                    out.append('search "percent" should reach more than one section, got %s' % c['topics'])
            if want('empty'):
                page.locator('.cf-search').fill('zzzqqq')
                page.wait_for_timeout(100)
                c = page.evaluate(COUNTS)
                if c['shown'] != 0 or not c['empty'] or c['secs']:
                    out.append('empty: %d cards, message shown=%s, sections %s' % (c['shown'], c['empty'], c['secs']))
                if c['empty']:
                    page.locator('.cf-clear').click()
                else:
                    page.locator('.cf-search').fill('')
                page.wait_for_timeout(100)
                c = page.evaluate(COUNTS)
                if c['shown'] != c['total'] or c['empty'] or c['q'] or c['url']:
                    out.append('clear: %d of %d cards, empty=%s, q=%r, url=%r' % (c['shown'], c['total'], c['empty'], c['q'], c['url']))
            if want('url-write'):
                h0 = page.evaluate('history.length')
                chip(page, 'geometry')
                page.locator('.cf-search').fill('shape')
                page.wait_for_timeout(100)
                c = page.evaluate(COUNTS)
                if c['url'] != '?topic=geometry&q=shape':
                    out.append('url: after Geometry + "shape" the URL is %r' % c['url'])
                if c['hist'] != h0:
                    out.append('url: history grew from %d to %d (replaceState only)' % (h0, c['hist']))
                chip(page, 'all')
                page.locator('.cf-search').fill('')
                page.wait_for_timeout(100)
                if page.evaluate('location.search') != '':
                    out.append('url: not cleared by All and an empty search: %r' % page.evaluate('location.search'))
            if want('events'):
                page.evaluate('window.__ev = []')
                chip(page, 'algebra')
                ev = page.evaluate('window.__ev')
                if len(ev) != 1 or ev[0][0] != 'filter_applied':
                    out.append('events: one chip tap fired %s' % [e[0] for e in ev])
                else:
                    p = ev[0][1]
                    n = page.evaluate("document.querySelectorAll('section#algebra a.card').length")
                    if p.get('filter_value') != 'v1|page=essentials;topic=algebra;calc=all;su=0;sl=0;q=;n=%d' % n or \
                            p.get('page') != 'essentials' or p.get('filter_type') != 'topic':
                        out.append('events: filter_applied is %s' % json.dumps(p))
                page.evaluate('window.__ev = []')
                chip(page, 'calculator', 'calc')
                ev = page.evaluate('window.__ev')
                if len(ev) != 1 or ev[0][1].get('filter_type') != 'calc' or \
                        not ev[0][1].get('filter_value', '').startswith('v1|page=essentials;topic=algebra;calc=calculator;') or \
                        ev[0][1].get('calc') != 'calculator':
                    out.append('events: the calculator chip fired %s' % json.dumps(ev))
                chip(page, 'all', 'calc')
                page.evaluate('window.__ev = []')
                page.locator('.cf-search').fill('')
                page.locator('.cf-search').type('equ;a=l')
                page.wait_for_timeout(1400)
                ev = page.evaluate('window.__ev')
                if len(ev) != 1 or ev[0][1].get('trigger') != 'search' or \
                        not re.match(r'^v1\|page=essentials;topic=algebra;calc=all;su=1;sl=7;q=equal;n=\d+$', ev[0][1].get('filter_value', '')):
                    out.append('events: typing "equ;a=l" fired %s' % json.dumps(ev))
                page.locator('.cf-search').fill('')
                page.evaluate('window.__ev = []')
                page.evaluate("document.querySelectorAll('a.card').forEach(c => c.addEventListener('click', e => e.preventDefault()))")
                page.locator('a.card:visible').first.click()
                ev = page.evaluate('window.__ev')
                gc = [e for e in ev if e[0] == 'game_card_clicked']
                if len(gc) != 1 or gc[0][1].get('page') != 'essentials' or gc[0][1].get('topic') != 'algebra' or \
                        not gc[0][1].get('filter_value', '').startswith('v1|page=essentials;topic=algebra;calc=all;su=0;') or \
                        not gc[0][1].get('game_slug'):
                    out.append('events: card click fired %s' % json.dumps(ev))
            if errors:
                out.append('page errors: %s' % errors[:2])
        finally:
            br.close()
    if want('url-read'):
        with sync_playwright() as pw:
            for q, want_topics, want_q in (('?topic=geometry', ['geometry'], ''), ('?topic=nonsense', TOPICS, ''),
                                          ('?calc=nonsense', TOPICS, ''), ('?q=angle', None, 'angle'),
                                          ('?topic=ratio&q=percent', ['ratio'], 'percent')):
                br, page, errors = open_page(pw, base, (1280, 720), query=q, sources=sources)
                try:
                    c = page.evaluate(COUNTS)
                    if want_topics is not None and sorted(c['topics']) != sorted(want_topics):
                        out.append('url %s: shows topics %s' % (q, c['topics']))
                    if c['q'] != want_q:
                        out.append('url %s: search box holds %r' % (q, c['q']))
                    if want_q and not 0 < c['shown'] < c['total']:
                        out.append('url %s: %d cards' % (q, c['shown']))
                    if page.evaluate('window.__ev.length'):
                        out.append('url %s: an event fired on load' % q)
                    if q == '?calc=nonsense' and c['shown'] != c['total']:
                        out.append('url %s: filtered by a calc value that is not a chip' % q)
                finally:
                    br.close()
            for q, key in (('?calc=non-calculator', 'non-calculator'), ('?calc=calculator&topic=statistics', 'calculator')):
                br, page, errors = open_page(pw, base, (1280, 720), query=q, sources=sources)
                try:
                    c = page.evaluate(COUNTS)
                    exp = sorted(s for s in ALL_SLUGS if expected_calc(s) in CHIP_ACCEPTS[key] and
                                 ('statistics' not in q or TOPIC_OF.get(s) == 'statistics'))
                    if sorted(s for s, _ in c['cards']) != exp:
                        out.append('url %s: shows %d cards, the roster says %d' % (q, c['shown'], len(exp)))
                    if q == '?calc=non-calculator' and any(v == 'calc' for _, v in c['cards']):
                        out.append('url %s: shows a calculator game' % q)
                    pressed = page.locator('.cf-chip[data-cf-group="calc"][aria-pressed="true"]').get_attribute('data-cf-key')
                    if pressed != key:
                        out.append('url %s: the %s chip is not the pressed one (%s)' % (q, key, pressed))
                finally:
                    br.close()


def check_fit(base, size, out, sources=None):
    w, h = size
    with sync_playwright() as pw:
        br, page, errors = open_page(pw, base, size, sources=sources)
        try:
            m = page.evaluate("""() => {
              const r = e => e.getBoundingClientRect(), d = document.documentElement;
              const bar = document.querySelector('.cf-bar');
              const first = document.querySelector('a.card');
              return { sx: d.scrollWidth - d.clientWidth, bar: r(bar).height,
                       chips: [...document.querySelectorAll('.cf-chip')].map(c => r(c).height),
                       search: r(document.querySelector('.cf-search')).height,
                       clear: 0,
                       rowScrolls: (() => { const row = document.querySelector('.cf-chips'); return { sw: row.scrollWidth, cw: row.clientWidth }; })(),
                       firstTop: r(first).top + window.scrollY };
            }""")
            if m['sx'] > 0:
                out.append('%dx%d: sideways page scroll of %d px' % (w, h, m['sx']))
            if min(m['chips']) < 43.5 or m['search'] < 43.5:
                out.append('%dx%d: a control is under 44 px tall (chips %.1f, search %.1f)' % (w, h, min(m['chips']), m['search']))
            if m['bar'] > 0.27 * h:
                out.append('%dx%d: the sticky bar is %d px, over 27%% of the screen' % (w, h, m['bar']))
            if w <= 390 and not m['rowScrolls']['sw'] > m['rowScrolls']['cw']:
                out.append('%dx%d: the chip row does not scroll sideways (%d in %d)' % (w, h, m['rowScrolls']['sw'], m['rowScrolls']['cw']))
            # From a scrolled page, each chip tap leaves the first card whole, below the bar, with its centre on the card.
            for t, grp in (('probability', 'topic'), ('geometry', 'topic'), ('calculator', 'calc'), ('statistics', 'topic'), ('all', 'topic'), ('all', 'calc')):
                page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                page.wait_for_timeout(80)
                chip(page, t, grp)
                page.wait_for_timeout(120)
                r = page.evaluate("""() => {
                  const bar = document.querySelector('.cf-bar').getBoundingClientRect();
                  const c = [...document.querySelectorAll('a.card')].find(c => c.getClientRects().length);
                  const b = c.getBoundingClientRect();
                  const top = document.elementFromPoint(b.left + b.width / 2, Math.min(b.top + b.height / 2, innerHeight - 1));
                  return { top: b.top, bottom: b.bottom, barBottom: bar.bottom, barTop: bar.top, atEnd: window.scrollY + innerHeight >= document.documentElement.scrollHeight - 2, vh: innerHeight, hit: !!(top && top.closest('a.card') === c),
                           name: c.dataset.slug, sx: document.documentElement.scrollWidth - document.documentElement.clientWidth };
                }""")
                if t == 'all':
                    continue
                if abs(r['barTop']) > 1 and not r['atEnd']:
                    out.append('%dx%d: after %s the bar is at %d, not stuck to the top of the screen' % (w, h, t, r['barTop']))
                elif r['top'] < r['barBottom'] - 1 or r['bottom'] > r['vh'] + 1:
                    out.append('%dx%d: after %s the first card (%s) is at %d-%d, the bar ends at %d, the screen at %d' % (
                        w, h, t, r['name'], r['top'], r['bottom'], r['barBottom'], r['vh']))
                elif not r['hit']:
                    out.append('%dx%d: after %s the first card (%s) is covered at its centre' % (w, h, t, r['name']))
            # Keyboard focus of a card far down the page lands below the bar.
            chip(page, 'all')
            page.evaluate("document.querySelectorAll('a.card')[25].focus()")
            page.wait_for_timeout(120)
            r = page.evaluate("""() => { const b = document.activeElement.getBoundingClientRect(), bar = document.querySelector('.cf-bar').getBoundingClientRect();
                                         return { top: b.top, barBottom: bar.bottom }; }""")
            if r['top'] < r['barBottom'] - 1:
                out.append('%dx%d: a focused card is behind the bar (%d < %d)' % (w, h, r['top'], r['barBottom']))
        finally:
            br.close()


def mutate_js(old, new):
    src = read(JS)
    assert src.count(old) == 1, 'stale plant: %r not found exactly once in card-filter.js' % old
    return {'card-filter.js': src.replace(old, new)}


def mutate_css(old, new):
    src = read(CSS)
    assert src.count(old) == 1, 'stale plant: %r not found exactly once in card-filter.css' % old
    return {'card-filter.css': src.replace(old, new)}


def mutate_page(old, new, count=1):
    src = read(PAGE)
    assert src.count(old) >= 1, 'stale plant: %r not found in the page' % old
    return src.replace(old, new, count)


PLANTS = [
    ('a card with no data-topic', 'static', lambda: mutate_page(' data-topic="algebra"', ''), r'no data-topic'),
    ('a card with the wrong data-topic', 'static', lambda: mutate_page('data-topic="ratio"', 'data-topic="number"'), r'does not match its section'),
    ('a card with no data-calc', 'static', lambda: mutate_page(' data-calc="non-calc"', '', 1), r'card has no data-calc'),
    ('a card with the wrong data-calc', 'static', lambda: mutate_page(' data-calc="non-calc"', ' data-calc="calc"', 1), r'but the roster says'),
    ('a card with data-calc="maybe"', 'static', lambda: mutate_page(' data-topic="geometry"', ' data-calc="maybe" data-topic="geometry"'), r'data-calc .maybe. is not one of'),
    ('both is not counted as either chip', ('calc',), lambda: mutate_js("var accepts = (opt && opt.values) || [state[g.param]];", "var accepts = [state[g.param]];"), r'calc (non-calculator|calculator)'),
    ('a calculator chip says Non-calculator', ('load',), lambda: {'page': mutate_page('label: \'Likely non-calculator\'', 'label: \'Non-calculator\'')}, r'the calculator chips read'),
    ('the module never rewrites the URL', ('url-write',), lambda: mutate_js("try { history.replaceState(null, '', location.pathname + (s ? '?' + s : '') + location.hash); }", "try { void s; }"), r'url:'),
    ('empty sections stay showing', ('topics',), lambda: mutate_js("s.classList.toggle('cf-hidden', !s.querySelector(cfg.cards + ':not(.cf-hidden)'));", "void s;"), r'topic .*sections'),
    ('the empty message never shows', ('empty',), lambda: mutate_js('els.empty.hidden = n !== 0;', 'els.empty.hidden = true;'), r'empty:'),
    ('a chip tap fires no event', ('events',), lambda: mutate_js("window.mfg('filter_applied', p);", 'void p;'), r'events: one chip tap'),
    ('the bar is not sticky', ('fit',), lambda: mutate_css('position: sticky;', 'position: static;'), r'not stuck to the top'),
    ('the bar wrapper clips the sticky bar', ('fit',), lambda: mutate_css('[data-card-filter] { display: contents; }', '[data-card-filter] { display: block; }'), r'not stuck to the top'),
    ('an event fires on load', ('load',), lambda: mutate_js('    ready = true;', "    ready = true; report('load');"), r'load: an event fired'),
    ('the exception removed', 'static', lambda: (read(PAGE), {}), r'i-found-a-mark: the roster Calculator field is untagged'),
    ('the exception given the wrong value', 'static', lambda: mutate_page('data-topic="technique" data-calc="both"', 'data-topic="technique" data-calc="calc"'), r'i-found-a-mark: data-calc .calc., but'),
    ('the exception overriding a real tag', 'static', lambda: (read(PAGE), dict(CALC_ACROSS_PAPERS, **{'distinctly-average': 'planted'})), r'distinctly-average: in CALC_ACROSS_PAPERS but the roster tags it'),
    ('the technique card in the wrong section', 'static', lambda: mutate_page('data-topic="technique"', 'data-topic="number"'), r'does not match its section'),
    ('the technique chip missing', ('topics',), lambda: {'page': mutate_page("{ key: 'technique', label: 'Exam technique' }", '')}, r"topic technique: 0 chips with data-cf-key='technique'"),
]


def run_plant(base, p):
    what, kind, make, want = p
    out = []
    if kind == 'static':
        made = make()
        out = static_check(*made) if isinstance(made, tuple) else static_check(made)
    elif kind == ('fit',):
        check_fit(base, (375, 667), out, sources=make())
    else:
        check_behaviour(base, out, sources=make(), only=set(kind))
    hit = [g for g in out if re.search(want, g)]
    print('  self-test %-40s %s' % (what, ('caught: ' + hit[0][:80]) if hit else '*** MISSED ***' + (' (other: %s)' % out[0][:80] if out else '')))
    return bool(hit)


def main():
    ap = argparse.ArgumentParser()
    bc.shard_args(ap)
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    shard = bc.Shard(__file__, args)
    behaviour = ['load', 'topics', 'calc', 'search', 'empty', 'url-write', 'url-read', 'events']
    units = ['static'] + ['behaviour: ' + b for b in behaviour] + ['fit %dx%d' % s for s in SIZES] + ['plant: ' + p[0] for p in PLANTS]
    if args.list_units:
        print('\n'.join(units))
        return 0
    mine = shard.pick(units)
    out = []
    ok = True
    if 'static' in mine:
        with shard.unit('static'):
            out += static_check(read(PAGE))
            for f in (JS, CSS):
                if not os.path.exists(f):
                    out.append('missing %s' % f)
            print('card-filter: every card carries its section as data-topic and the roster-derived data-calc')
    proc, base = bc.start_stub_server()
    try:
        for b in behaviour:
            if 'behaviour: ' + b in mine:
                with shard.unit('behaviour: ' + b):
                    check_behaviour(base, out, only={b})
                print('card-filter: %s ok' % b)
        for s in SIZES:
            if 'fit %dx%d' % s in mine:
                with shard.unit('fit %dx%d' % s):
                    check_fit(base, s, out)
                print('card-filter: the bar fits at %dx%d' % s)
        for p in PLANTS:
            if 'plant: ' + p[0] in mine:
                with shard.unit('plant: ' + p[0]):
                    ok = run_plant(base, p) and ok
    finally:
        proc.terminate()
    for f in out[:60]:
        print('FAIL  ' + f)
    if len(out) > 60:
        print('... and %d more' % (len(out) - 60))
    if out or not ok:
        print('card-filter: FAILED')
        return 1
    print('card-filter: OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
