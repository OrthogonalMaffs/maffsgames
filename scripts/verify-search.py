#!/usr/bin/env python3
# ci-line: Search (schools/assets/search.js, the one matcher on the portal and /essentials/, played in Chromium: topic queries find the game whatever it is called, every word on the card text plus its data-keywords, the trailing-s rule, a nonsense query empty with its message, both pages call MaffsSearch.match; planted faults caught) |
# ci-deps: schools/assets/search.js schools/assets/card-filter.js index.html essentials/index.html data/games.json
"""Does a teacher who types a topic into a MaffsGames search box find the games that teach it? Contract SEARCH-KEYWORDS
(Jon, 4 Nov 2026).

Both pages that search cards, the portal (index.html applyFilters) and /essentials/ (MaffsCardFilter, card-filter.js),
decide a match with ONE function, MaffsSearch.match (schools/assets/search.js): the card's text plus its data-keywords
(written from data/games.json by scripts/apply-meta.py, held by scripts/check-meta.py), every query word found, a word
longer than 3 letters ending in "s" also found without it, an empty query matching all.

This loads the real pages from the stub server in Chromium (analytics stubbed) and checks:
  - the matcher on its own, on hand-made cards (the expected answers are written here, not computed by search.js);
  - each page's filter calls MaffsSearch.match: replaced by one that never matches, the page shows nothing;
  - every query in QUERIES shows its game on the portal and, where the game has a card there, on /essentials/;
    the contract's nine, then ten of this check's own, one per topic area;
  - which of those the card's visible text alone would not find (keywords are doing the work), and that "nth term"
    is one of them, so the dropped-keywords plant tests something;
  - "zzqx": no card, the count "0 games" and the no-results message, on both pages.
Planted faults, each must fail a check: the matcher ignoring data-keywords; the matcher back to the portal's old rule
(the whole query as one substring); sequence-solver's cards without data-keywords on both pages.

    python scripts/verify-search.py
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_common as bc  # noqa: E402
import plant_common as pc  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEARCH_JS = os.path.join(ROOT, 'schools', 'assets', 'search.js')
PORTAL = os.path.join(ROOT, 'index.html')
ESSENTIALS = os.path.join(ROOT, 'essentials', 'index.html')
STUB_ANALYTICS = "window.__ev = []; window.mfg = function (n, p) { window.__ev.push([n, p]); };"

# (query, the game it must find). The contract's nine, then ten of this check's own, one per topic area.
QUERIES = [
    ('circle', 'take-a-walk'), ('circles', 'take-a-walk'), ('area circle', 'take-a-walk'),
    ('nth term', 'sequence-solver'), ('times tables', 'six-sevens-bruv'), ('ratio', 'split-it'),
    ('income tax', 'tax-theft'), ('prime', 'prime-or-composite'), ('circle theorems', 'circle-theorem-spotter'),
] + [
    ('bodmas', 'equatle'),                                  # number
    ('simultaneous equations', 'simultaneous-solver'),      # algebra
    ('density', 'squared-squirrel'),                        # ratio, proportion and rates of change
    ('loci', 'constructions-lab'),                          # geometry
    ('tree diagram', 'probability-paradox'),                # probability
    ('box plot', 'chart-interrogator'),                     # statistics
    ('best buy', 'better-value'),                           # financial maths
    ('coefficient of friction', 'curling-friction'),        # mechanics
    ('chain rule', 'differentiation-duel'),                 # calculus
    ('argand diagram', 'complex-converter'),                # further maths
]
NONSENSE = 'zzqx'
MUST_NEED_KEYWORDS = 'nth term'

PAGES = {
    'portal': {'url': '/', 'input': '#searchInput', 'cards': 'a.game-card', 'count': '#gameCount',
               'empty': "(() => { const e = document.getElementById('noResults'); return e.classList.contains('visible') && e.getClientRects().length > 0; })()"},
    'essentials': {'url': '/essentials/', 'input': '.cf-search', 'cards': 'a.card', 'count': '.cf-count',
                   'empty': "(() => { const e = document.querySelector('.cf-empty'); return !e.hidden && e.getClientRects().length > 0; })()"},
}

SLUG_OF = r"""(c) => { const h = c.getAttribute('href') || ''; const m = h.match(/games\/([a-z0-9-]+)/) || h.match(/^\/?([a-z0-9-]+)\//); return m ? m[1] : h; }"""

STATE = """([sel, countSel, emptyExpr]) => {
  const slugOf = %s;
  const vis = [...document.querySelectorAll(sel)].filter(c => c.getClientRects().length > 0).map(slugOf);
  return { shown: [...new Set(vis)], count: (document.querySelector(countSel) || {}).textContent || '', empty: eval(emptyExpr) };
}""" % SLUG_OF

# Hand-made cards and what MaffsSearch.match must say. [text, data-keywords or null, query, expected]
UNIT = [
    ['Take a Walk Perimeter and area', 'area | circle', 'area circle', True],      # every word, across text and keywords
    ['Take a Walk', 'perimeter | circle', 'circles', True],                       # longer than 3 letters, trailing s
    ['Prime or Composite', None, 'primes', True],
    ['ga', None, 'gas', False],                                                     # 3 letters: the s stays
    ['abc', 'circle', 'circle zzqx', False],                                        # every word, not any
    ['abc', None, '', True], ['abc', None, '   ', True],                            # empty query: everything
    ['Nth  Term', None, '  NTH   term ', True],                                     # case and whitespace
    ['Sequence Solver', 'nth term | sequences', 'nth term', True],                  # keywords alone
    ['Sequence Solver', None, 'nth term', False],
    ['circle', None, 'circel', False],                                              # no fuzzy matching
    ['Six Sevens, Bruv', 'times tables | multiplication', 'times table', True],
]
UNIT_JS = """(cases) => cases.map(([text, kw, q, want]) => {
  const a = document.createElement('a'); a.textContent = text; if (kw !== null) a.setAttribute('data-keywords', kw);
  return [text, kw, q, want, window.MaffsSearch.match(a, q)];
})"""

# For each query: does the target card match on its visible text alone, with data-keywords removed?
NEEDS_JS = """([sel, q, slug]) => {
  const slugOf = %s;
  const c = [...document.querySelectorAll(sel)].find(x => slugOf(x) === slug);
  if (!c) return null;
  const bare = c.cloneNode(true); bare.removeAttribute('data-keywords');
  return { withKw: window.MaffsSearch.match(c, q), bare: window.MaffsSearch.match(bare, q) };
}""" % SLUG_OF


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def open_page(br, base, which, sources):
    ctx = br.new_context(viewport={'width': 1280, 'height': 900})
    ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
    ctx.route(lambda url: url.split('?')[0].endswith('/schools/assets/analytics.js'), lambda route: route.fulfill(
        status=200, content_type='application/javascript', body=STUB_ANALYTICS))

    def serve(match, ctype, body):
        ctx.route(match, lambda route: route.fulfill(status=200, content_type=ctype + '; charset=utf-8', body=body))
    if 'search.js' in sources:
        serve(lambda url: url.split('?')[0].endswith('/schools/assets/search.js'), 'application/javascript', sources['search.js'])
    if which in sources:
        path = PAGES[which]['url']
        serve(lambda url: url.split('?')[0] in (base + path, base + path + 'index.html'), 'text/html', sources[which])
    page = ctx.new_page()
    page.goto(base + PAGES[which]['url'], wait_until='load', timeout=30000)
    page.wait_for_selector(PAGES[which]['input'], timeout=10000)
    return ctx, page


def search(page, which, q):
    cfg = PAGES[which]
    page.fill(cfg['input'], q)
    return page.evaluate(STATE, [cfg['cards'], cfg['count'], cfg['empty']])


def check_page(br, base, which, sources, out, report=None):
    """Every check on one page; failures appended to out, prefixed with the page."""
    cfg = PAGES[which]
    ctx, page = open_page(br, base, which, sources)
    try:
        if not page.evaluate("typeof window.MaffsSearch === 'object' && typeof window.MaffsSearch.match === 'function'"):
            out.append('%s: window.MaffsSearch.match is not loaded' % which)
            return
        on_page = set(page.evaluate("([sel]) => [...document.querySelectorAll(sel)].map(%s)" % SLUG_OF, [cfg['cards']]))
        if which == 'portal':
            for text, kw, q, want, got in page.evaluate(UNIT_JS, UNIT):
                if got != want:
                    out.append('matcher: %r on a card %r (keywords %r) gave %s, should be %s' % (q, text, kw, got, want))
        needs = []
        for q, slug in QUERIES:
            if slug not in on_page:
                if which == 'portal':
                    out.append('portal: no card for %s (query %r)' % (slug, q))
                continue
            st = search(page, which, q)
            if slug not in st['shown']:
                out.append('%s: %r does not show %s (shows %d games: %s)' % (which, q, slug, len(st['shown']), ', '.join(st['shown'][:8])))
            n = page.evaluate(NEEDS_JS, [cfg['cards'], q, slug])
            if n and n['withKw'] and not n['bare']:
                needs.append(q)
        if which == 'portal' and MUST_NEED_KEYWORDS not in needs:
            out.append('portal: %r is found without keywords, so the dropped-keywords plant tests nothing' % MUST_NEED_KEYWORDS)
        st = search(page, which, NONSENSE)
        if st['shown'] or not st['count'].startswith('0 ') or not st['empty']:
            out.append('%s: %r shows %d cards, count %r, no-results message %s' % (which, NONSENSE, len(st['shown']), st['count'], st['empty']))
        # The page's filter must call the shared matcher: replace it, filter again, nothing may show.
        search(page, which, '')
        page.evaluate("window.MaffsSearch.match = function () { return false; }")
        st = search(page, which, 'ratio')
        if st['shown']:
            out.append("%s: with MaffsSearch.match never matching, 'ratio' still shows %d cards: the page matches on its own" % (which, len(st['shown'])))
        if report is not None:
            report[which] = (len([q for q, s in QUERIES if s in on_page]), needs)
    finally:
        ctx.close()


def plants():
    js, portal, ess = read(SEARCH_JS), read(PORTAL), read(ESSENTIALS)
    drop = lambda src: pc.apply_re_plant(src, r'(<a\b[^>]*games/sequence-solver/[^>]*?)\s+data-keywords="[^"]*"', r'\1',
                                         'sequence-solver card without data-keywords', count=0)
    return [
        ('the matcher ignores data-keywords', lambda: {'search.js': pc.apply_plant(
            js, "var kw = (card.getAttribute && card.getAttribute('data-keywords')) || '';", "var kw = '';",
            'matcher ignores data-keywords')}),
        ("the matcher back to the portal's old rule (the whole query as one substring)", lambda: {'search.js': pc.apply_plant(
            js, "return words.every(function (w) { return found(hay, w); });", "return hay.indexOf(words.join(' ')) !== -1;",
            'whole-query substring')}),
        ("sequence-solver's cards without data-keywords", lambda: {'portal': drop(portal), 'essentials': drop(ess)}),
    ]


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    out, report, missed = [], {}, []
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch()
            for which in PAGES:
                check_page(br, base, which, {}, out, report)
            for which, (n, needs) in report.items():
                print('search: %s: %d queries, %d found only through keywords (%s)' % (which, n, len(needs), ', '.join(needs)))
            for name, make in plants():
                try:
                    sources = make()
                except pc.StalePlant as e:
                    out.append('plant %s: %s' % (name, e))
                    continue
                got = []
                for which in PAGES:
                    check_page(br, base, which, sources, got)
                caught = pc.is_caught(got)
                print('  plant %-75s %s' % (name, ('CAUGHT: ' + got[0][:90]) if caught else 'MISSED'))
                if not caught:
                    missed.append(name)
            br.close()
    finally:
        proc.terminate()
    for f in out[:60]:
        print('FAIL  ' + f)
    for m in missed:
        print('FAIL  planted fault not caught: ' + m)
    if out or missed:
        print('search: FAILED')
        return 1
    print('search: OK (%d queries on the portal, the matcher, the nonsense query, both pages through MaffsSearch.match, %d plants caught)'
          % (len(QUERIES), len(plants())))
    return 0


if __name__ == '__main__':
    sys.exit(main())
