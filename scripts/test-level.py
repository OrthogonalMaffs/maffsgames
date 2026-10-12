#!/usr/bin/env python3
# ci-line: Shared level reader (schools/assets/level.js, MaffsLevel in Chromium: constructor, __proto__, toString, empty, mixed-case, unknown and valid keys; the leaderboard refuses an undeclared key; a property-lookup reader planted and caught) | --selftest && --run
# ci-line: lock | Level resolver in play, part 1 (every migrated game loads at its default for constructor, __proto__ and nonsense, and at each declared level, with no page error) | --games --part 1/4
# ci-line: lock | Level resolver in play, part 2 (migrated games, as part 1) | --games --part 2/4
# ci-line: lock | Level resolver in play, part 3 (migrated games, as part 1) | --games --part 3/4
# ci-line: lock | Level resolver in play, part 4 (migrated games, as part 1) | --games --part 4/4
# ci-deps: schools/assets/level.js schools/assets/firebase-leaderboard.js scripts/check-levels.py games/
"""Browser test for MaffsLevel (contract LEVEL-RESOLVER, 12 Oct 2026; canon section 4.5).

    python scripts/test-level.py --run         # the cases below, in headless Chromium
    python scripts/test-level.py --selftest    # the same cases against a reader that looks the key up as a property:
                                               # it must FAIL (so the test bites)

Each case opens a fixture page that loads the real schools/assets/level.js and declares
`{slug: 'fixture', levels: ['gcse', 'alevel'], fallback: 'gcse', boards: ['q20']}`, with the query string given:

  ?level=constructor   ?level=__proto__   ?level=toString   ?level=hasOwnProperty   ?level=        ?level=GCSE
  ?level=nonsense      ?level=alevel      (no level)        ?level=gcse&mode=hard#top

and requires: resolve() returns the right key and never throws; the page raises no error; when a level parameter
was present and not declared, the URL ends up carrying the fallback (other parameters and the hash kept); when it
was declared or absent, the URL is untouched.

The leaderboard guard: with the real firebase-leaderboard.js and a fake Firebase SDK, submitScore() under an
undeclared key warns and never reaches the SDK; under a declared level or board it does; and a page that
declared nothing behaves as before (the SDK is reached).
"""
import argparse
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LEVEL_JS = os.path.join(ROOT, 'schools', 'assets', 'level.js')
LB_JS = os.path.join(ROOT, 'schools', 'assets', 'firebase-leaderboard.js')
HOST = 'https://fixture.test'
sys.path.insert(0, HERE)
JUNK = ['constructor', '__proto__', 'nonsense']

DECL = "{slug: 'fixture', levels: ['gcse', 'alevel'], fallback: 'gcse', boards: ['q20']}"
PAGE = ('<!doctype html><html><head><meta charset="utf-8"><title>fixture</title></head><body>'
        '<script src="/level.js"></script>'
        '<script>window.__r = {};try{window.__r.level = MaffsLevel.resolve(%s);}catch(e){window.__r.threw = String(e);}'
        'window.__r.search = location.search; window.__r.hash = location.hash; window.__r.fromUrl = MaffsLevel.declared("fixture").fromUrl;</script></body></html>')
PAGE_LB = ('<!doctype html><html><head><meta charset="utf-8"><title>fixture</title></head><body>'
           '%s<script src="/level.js"></script><script src="/lb.js"></script></body></html>')

# (query string, expected level, expected search after resolve, expected hash)
CASES = [
    ('?level=constructor', 'gcse', '?level=gcse', ''),
    ('?level=__proto__', 'gcse', '?level=gcse', ''),
    ('?level=toString', 'gcse', '?level=gcse', ''),
    ('?level=hasOwnProperty', 'gcse', '?level=gcse', ''),
    ('?level=', 'gcse', '?level=gcse', ''),
    ('?level=GCSE', 'gcse', '?level=gcse', ''),
    ('?level=nonsense', 'gcse', '?level=gcse', ''),
    ('?level=alevel', 'alevel', '?level=alevel', ''),
    ('', 'gcse', '', ''),
    ('?mode=hard&level=zzz#top', 'gcse', '?mode=hard&level=gcse', '#top'),
]

FAKE_SDK = """
window.__sdk = { init: 0 };
window.firebase = { apps: [], initializeApp: function () { window.__sdk.init++; return {}; }, app: function () { return {}; },
  database: Object.assign(function () { return { ref: function () { var r = { push: function () { return Promise.resolve({key: 'k'}); },
    once: function () { return Promise.resolve({val: function () { return null; }}); }, set: function () { return Promise.resolve(); },
    child: function () { return r; } }; return r; } }; }, { ServerValue: { TIMESTAMP: 0 } }) };
window.__warns = []; var w = console.warn; console.warn = function () { window.__warns.push([].join.call(arguments, ' ')); return w.apply(console, arguments); };
"""


def serve(route, level_src, lb_src, page):
    url = route.request.url
    if url.endswith('/level.js'):
        return route.fulfill(status=200, content_type='application/javascript', body=level_src)
    if url.endswith('/lb.js'):
        return route.fulfill(status=200, content_type='application/javascript', body=lb_src)
    return route.fulfill(status=200, content_type='text/html', body=page)


def run(level_src):
    from playwright.sync_api import sync_playwright
    lb_src = open(LB_JS, encoding='utf-8').read()
    fails = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for q, want_level, want_search, want_hash in CASES:
            page = browser.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.route('**/*', lambda r: serve(r, level_src, lb_src, PAGE % DECL))
            page.goto(HOST + '/p.html' + q + ('' if '#' in q else ''))
            r = page.evaluate('window.__r')
            now = page.evaluate('[location.search, location.hash]')
            label = q or '(no level)'
            problems = []
            if r.get('threw'):
                problems.append('threw ' + r['threw'])
            if r.get('level') != want_level:
                problems.append('returned %r, wanted %r' % (r.get('level'), want_level))
            if now[0] != want_search or now[1] != want_hash:
                problems.append('URL is %s%s, wanted %s%s' % (now[0], now[1], want_search, want_hash))
            if r.get('fromUrl') != (q in ('?level=alevel',)):
                problems.append('fromUrl is %r' % r.get('fromUrl'))
            if errors:
                problems.append('page error ' + errors[0])
            print('  %-36s %s' % (label, 'ok' if not problems else 'FAIL: ' + '; '.join(problems)))
            fails += ['%s: %s' % (label, x) for x in problems]
            page.close()

        # The leaderboard guard.
        def lb_case(name, decl, level, want_reached):
            pg = browser.new_page()
            pg.add_init_script(FAKE_SDK)
            body = '<script>' + ('' if decl is None else 'MaffsLevel_decl = 1;') + '</script>'
            pg.route('**/*', lambda r: serve(r, level_src, lb_src, PAGE_LB % body))
            pg.goto(HOST + '/p.html')
            if decl is not None:
                pg.evaluate('MaffsLevel.resolve(%s)' % decl)
            pg.evaluate("(function () { MaffsLeaderboard.submitScore('fixture', %r, 5, 10); })()" % level)   # not awaited: a real submit waits on the initials overlay
            pg.wait_for_timeout(150)
            init, warns = pg.evaluate('[window.__sdk.init, window.__warns]')
            reached = init > 0
            refused = any('not one the game declared' in w for w in warns)
            problems = []
            if reached != want_reached:
                problems.append('SDK reached=%s, wanted %s' % (reached, want_reached))
            if refused == want_reached:
                problems.append('refusal warned=%s' % refused)
            print('  %-36s %s' % (name, 'ok' if not problems else 'FAIL: ' + '; '.join(problems)))
            fails.extend('%s: %s' % (name, x) for x in problems)
            pg.close()

        lb_case('submit under an undeclared key', DECL, 'constructor', False)
        lb_case('submit under a typed-in key', DECL, 'zzz', False)
        lb_case('submit under a declared level', DECL, 'alevel', True)
        lb_case('submit under a declared board', DECL, 'q20', True)
        lb_case('submit with no declaration (unmigrated)', None, 'anything', True)
        browser.close()
    return fails


def migrated_games():
    """{slug: declaration} for every game in check-levels.py's MIGRATED, read from the page."""
    spec = importlib.util.spec_from_file_location('check_levels', os.path.join(HERE, 'check-levels.py'))
    cl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cl)
    out = {}
    for slug in sorted(cl.MIGRATED):
        text = open(os.path.join(ROOT, 'games', slug, 'index.html'), encoding='utf-8').read()
        out[slug] = cl.parse_decl(text)
    return out


def games(part):
    """Each migrated game, loaded with each junk key and each declared level (CI shards by slug, as the answer lock does)."""
    import bank_common as bc
    from playwright.sync_api import sync_playwright
    decls = migrated_games()
    i, n = (int(x) for x in part.split('/')) if part else (1, 1)
    slugs = [s for k, s in enumerate(sorted(decls)) if k % n == i - 1]
    fails = []
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for slug in slugs:
                d = decls[slug]
                problems = []
                for key in JUNK + d['levels']:
                    ctx = browser.new_context()
                    ctx.route(lambda u: not u.startswith(base) and '/katex@' not in u, lambda r: r.abort())
                    pg = ctx.new_page()
                    errs = []
                    pg.on('pageerror', lambda e: errs.append(str(e)[:140]))
                    pg.goto(base + '/games/%s/?level=%s' % (slug, key), wait_until='load', timeout=30000)
                    pg.wait_for_timeout(200)
                    got = pg.evaluate("(function(){var d=window.MaffsLevel&&MaffsLevel.declared(%r);"
                                      "return [d?d.fallback:null,new URLSearchParams(location.search).get('level')];})()" % slug)
                    want = d['fallback'] if key in JUNK else key
                    if errs:
                        problems.append('?level=%s: page error %s' % (key, errs[0]))
                    if got[0] is None:
                        problems.append('?level=%s: MaffsLevel has no declaration for it' % key)
                    if got[1] != want:
                        problems.append('?level=%s: the URL ends with level=%s, wanted %s' % (key, got[1], want))
                    ctx.close()
                print('  %-28s %s' % (slug, 'ok' if not problems else 'FAIL'))
                for pr in problems:
                    print('      ' + pr)
                fails += ['%s %s' % (slug, x) for x in problems]
            browser.close()
    finally:
        proc.terminate()
    return fails


def lookup_reader(src):
    """The fault the module exists to remove: the key is looked up as a property of an object built from the levels."""
    bad = re.sub(r"if \(levels\.indexOf\(asked\) !== -1\) \{",
                 "var o = {}; levels.forEach(function (l) { o[l] = 1; }); if (o[asked]) {", src)
    if bad == src:
        raise SystemExit('selftest: the membership test was not found in level.js')
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--games', action='store_true')
    ap.add_argument('--part', default='')
    a = ap.parse_args()
    ok = True
    src = open(LEVEL_JS, encoding='utf-8').read()
    if a.games:
        print('Migrated games (part %s):' % (a.part or '1/1'))
        fails = games(a.part)
        print('OK' if not fails else 'FAILED')
        return 0 if not fails else 1
    if a.run or not a.selftest:
        print('MaffsLevel:')
        fails = run(src)
        ok = ok and not fails
    if a.selftest:
        print('planted: a reader that looks the key up as a property (must FAIL):')
        fails = run(lookup_reader(src))
        caught = any('constructor' in f or '__proto__' in f or 'toString' in f for f in fails)
        print('  self-test %-40s %s' % ('property-lookup reader', 'caught' if caught else '*** MISSED ***'))
        ok = ok and caught
        if not a.run:
            pass
    print('OK' if ok else 'FAILED')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
