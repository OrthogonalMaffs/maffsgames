#!/usr/bin/env python3
# ci-line: New and updated (dated homepage cards, ordering, cap, deduplication, expiry, unchanged filter sets and phone compact controls; three plants caught) | --selftest
# ci-deps: index.html
"""NEW-AND-UPDATED, Jon, 3 Nov 2026. Browser observations checked against
the level cards' metadata, read independently in Python. No production requests.
The only clock replacement is in the test's served copy of the page.
"""
import argparse
from datetime import date
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

import bank_common as bc
import plant_common as pc
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'index.html'
TODAY = date(2026, 11, 3)
SIZES = [(320, 568), (375, 667), (390, 844)]
NOTE = ("The newest games first, and games that have had real work done: new questions, new levels or new help. "
        "Each one is also in its level section below. Every game feeds the leaderboards and keeps a score history on your device.")


class Attrs(HTMLParser):
    def handle_starttag(self, tag, attrs):
        self.attrs = dict(attrs)


def level_cards(src):
    """Read original cards only; the generated section cannot supply expectations."""
    src = src[src.index('<!-- KS3 SECTION -->'):]
    cards = []
    for match in re.finditer(r'<a\b[^>]*class="game-card"[^>]*>(.*?)</a>', src, re.S):
        parser = Attrs()
        parser.feed(match.group(0).split('>', 1)[0] + '>')
        attrs = parser.attrs
        title = re.search(r'<div class="card-title">(.*?)</div>', match.group(1), re.S)
        cards.append(dict(attrs, slug=attrs['href'].split('?')[0],
                          title=unescape(title.group(1)).strip(),
                          text=unescape(re.sub('<[^>]+>', ' ', match.group(1))).lower()))
    assert len(cards) > 100, 'level card parser is blind'
    return cards


def expected(cards, today):
    live = {}
    for card in cards:
        if 'data-badge' not in card:
            continue
        stamp = date.fromisoformat(card['data-badge-date'])
        assert stamp.isoformat() == card['data-badge-date'], 'noncanonical badge date'
        if (today - stamp).days < 56:
            live.setdefault(card['slug'], card)
    return sorted(live.values(), key=lambda c: (-date.fromisoformat(c['data-badge-date']).toordinal(),
                  c['data-badge'] != 'new', c['title'].casefold()))


def source_check(src):
    section = src[src.index('<!-- NEW AND UPDATED SECTION -->'):src.index('<!-- KS3 SECTION -->')]
    return ['hand card left in section'] if re.search(r'class="game-card"', section) else []


def open_page(browser, base, src, today, size=(1280, 900)):
    clock = 'function mfgToday() { return new Date(); }'
    assert src.count(clock) == 1, 'clock stub target moved'
    src = src.replace(clock, "function mfgToday() { return new Date('%sT12:00:00'); }" % today.isoformat())
    ctx = browser.new_context(viewport=dict(width=size[0], height=size[1]),
                              is_mobile=size[0] <= 600, has_touch=size[0] <= 600)
    ctx.route(lambda url: not url.startswith(base), bc.serve_real_font)
    ctx.route(base + '/?cb=*', lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=src))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda err: errors.append(str(err)))
    page.goto(base + '/?cb=new-and-updated-' + today.isoformat(), wait_until='load')
    page.evaluate('document.fonts.ready')
    return ctx, page, errors


def check_page(page, cards, today):
    fails = []
    want = expected(cards, today)
    got = page.locator('#cmpNew .game-card').evaluate_all(
        "(cs) => cs.map(c => ({href:c.getAttribute('href'), slug:c.getAttribute('href').split('?')[0], "
        "kind:c.dataset.badge, date:c.dataset.badgeDate, fresh:c.dataset.fresh, "
        "ribbon:c.querySelector('.fresh-badge')?.textContent, ids:c.querySelectorAll('[id]').length + (c.id ? 1 : 0)}))")
    if [c['slug'] for c in got] != [c['slug'] for c in want[:12]]:
        fails.append('order/cap/dedup: got %s expected %s' % ([c['slug'] for c in got], [c['slug'] for c in want[:12]]))
    for actual, original in zip(got, want[:12]):
        if (actual['href'], actual['kind'], actual['date'], actual['fresh'], actual['ribbon'], actual['ids']) != (
                original['href'], original['data-badge'], original['data-badge-date'], '1',
                'New' if original['data-badge'] == 'new' else 'Updated', 0):
            fails.append('copy lost href, metadata or ribbon, or duplicated id: %s' % actual)
    if page.locator('#cmpNew').is_visible() != bool(want):
        fails.append('whole section visibility differs from live badges')
    if today == TODAY:
        for slug in ('who-ate-all-the-pies', 'i-found-a-mark'):
            if 'games/' + slug + '/' not in [c['slug'] for c in got]:
                fails.append(slug + ' missing on 3 Nov')
    if page.locator('#cmpNew h2').text_content() != 'New and updated':
        fails.append('heading changed')
    if page.locator('#cmpNew .section-note').text_content() != NOTE:
        fails.append('note changed')
    if page.locator('#cmpNew .section-note a').get_attribute('href') != 'leaderboards/':
        fails.append('leaderboards link lost')
    if page.locator('#cmpNew').get_attribute('data-mfg-section') != 'new-and-updated':
        fails.append('section label changed')
    # Independently derive each set from the level cards, including uncapped live
    # games. Compare DOM flags and the portal's de-duplicated count.
    for level, topic, search, fresh in [
            ('all', 'all', '', False), ('all', 'all', '', True),
            ('gcse', 'all', '', True), ('ks3', 'number', '', True),
            ('all', 'statistics', '', True), ('all', 'all', 'pies', True),
            ('all', 'all', 'no-such-game-xyz', True)]:
        live_slugs = {c['slug'] for c in want}
        # Whether a card matches the search is asked of the page's own MaffsSearch.match (the one search rule,
        # schools/assets/search.js; contract SEARCH-KEYWORDS, Amendment 1), never restated here. It is asked card by
        # card, the page's level cards aligned with the source cards read above, so level, topic and fresh still have
        # to hold for the same copy of a game.
        dom = page.evaluate("q => [...document.querySelectorAll('.game-card')].filter(c => !c.closest('#cmpNew'))"
                            ".map(c => [c.getAttribute('href'), !q || window.MaffsSearch.match(c, q)])", search)
        if [h for h, _ in dom] != [c['href'] for c in cards]:
            fails.append('the page\'s level cards differ from the source cards (%d on the page, %d read)' % (len(dom), len(cards)))
            continue
        selected = {c['slug'] for c, (_, hit) in zip(cards, dom)
                    if (level == 'all' or level in c.get('data-levels', ''))
                    and (topic == 'all' or topic in c.get('data-topics', ''))
                    and hit
                    and (not fresh or c['slug'] in live_slugs)}
        observed = page.evaluate("""s => {
            activeLevel=s.level; activeTopic=s.topic; freshOnly=s.fresh;
            document.getElementById('searchInput').value=s.search;
            applyFilters(); compactSecondary();
            return {slugs:[...new Set([...document.querySelectorAll('.game-card:not(.hidden)')]
                    .map(c=>c.getAttribute('href').split('?')[0]))].sort(),
                    count:document.getElementById('gameCount').textContent};
        }""", dict(level=level, topic=topic, search=search, fresh=fresh))
        if observed['slugs'] != sorted(selected) or observed['count'] != (
                str(len(selected)) + (' game' if len(selected) == 1 else ' games')):
            fails.append('filter results changed: %s: %s' % ((level, topic, search, fresh), observed))
    return fails


def check_phone(page):
    fails = []
    group = page.locator('#cmpNew')
    n = page.locator('#cmpNew .game-card').count()
    if 'cmp-on' not in group.get_attribute('class') or 'cmp-open' in group.get_attribute('class'):
        fails.append('phone is not initially compact')
    if page.locator('#cmpNew [data-cmp-count]').inner_text() != str(n):
        fails.append('phone summary count is stale')
    if page.locator('#cmpNew .game-card').first.is_visible():
        fails.append('phone cards visible before opening')
    toggle = page.locator('#cmpNew .cmp-toggle')
    toggle.click()
    if toggle.get_attribute('aria-expanded') != 'true' or not page.locator('#cmpNew .game-card').first.is_visible():
        fails.append('phone toggle does not open cards')
    if page.evaluate('document.documentElement.scrollWidth > innerWidth'):
        fails.append('phone sideways overflow')
    toggle.click()
    if toggle.get_attribute('aria-expanded') != 'false' or page.locator('#cmpNew .game-card').first.is_visible():
        fails.append('phone toggle does not close cards')
    # Use the actual control to check that the existing compact listener updates
    # its summary after filtering.
    page.locator('.filter-btn.gcse').click()
    visible = page.locator('#cmpNew .game-card:not(.hidden)').count()
    if page.locator('#cmpNew [data-cmp-count]').inner_text() != str(visible):
        fails.append('phone filtered count is stale')
    return fails


def run(selftest):
    src = PAGE.read_text(encoding='utf-8')
    cards = level_cards(src)
    assert len(expected(cards, TODAY)) > 12, 'cap test needs more than 12 live games'
    fails = source_check(src)
    server, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            # Include the oldest badge's exact expiry boundary and a date after
            # every current badge expires.
            for today in (TODAY, date(2026, 11, 13), date(2030, 1, 1)):
                ctx, page, errors = open_page(browser, base, src, today)
                found = check_page(page, cards, today) + errors
                fails.extend(found)
                print('%s: %s (%d live games)' % (today, 'FAIL' if found else 'PASS', len(expected(cards, today))))
                ctx.close()
            for size in SIZES:
                ctx, page, errors = open_page(browser, base, src, TODAY, size)
                found = check_phone(page) + errors
                fails.extend(found)
                print('phone %dx%d: %s' % (*size, 'FAIL' if found else 'PASS'))
                ctx.close()
            if selftest:
                plants = [
                    ('order reversed', 'b.dataset.badgeDate.localeCompare(a.dataset.badgeDate)',
                     'a.dataset.badgeDate.localeCompare(b.dataset.badgeDate)'),
                    ('cap removed', 'liveCards.slice(0, NEW_CAP)', 'liveCards'),
                    ('hand card left', '<div class="games-grid" data-cmp-hide></div>',
                     '<div class="games-grid" data-cmp-hide><a class="game-card" href="games/stale/">Stale</a></div>'),
                ]
                for name, old, new in plants:
                    planted = pc.apply_plant(src, old, new, name=name)
                    ctx, page, errors = open_page(browser, base, planted, TODAY)
                    found = source_check(planted) + check_page(page, cards, TODAY)
                    caught = pc.is_caught(found, errors or None)
                    print('plant %s: %s' % (name, 'CAUGHT' if caught else 'MISSED/ERROR'))
                    if not caught:
                        fails.append('plant %s: %s' % (name, errors or 'not caught'))
                    ctx.close()
            browser.close()
    finally:
        server.terminate()
        server.wait()
    for fail in fails:
        print('FAIL:', fail)
    print('New and updated: %s (%d failures)' % ('FAIL' if fails else 'PASS', len(fails)))
    return bool(fails)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--selftest', action='store_true')
    sys.exit(run(parser.parse_args().selftest))
