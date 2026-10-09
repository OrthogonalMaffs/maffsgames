#!/usr/bin/env python3
# ci-line: Scores offline (no page but firebase-leaderboard.js calls the Firebase SDK; /leaderboards/ and the portal with Firebase blocked and with a fake SDK; planted faults caught) |
# ci-deps: schools/assets/firebase-leaderboard.js leaderboards/index.html index.html schools/assets/score-history.js
"""Contract SCORES-OFFLINE (9 Oct 2026): pages read Firebase only through MaffsLeaderboard.

    python scripts/test-scores-offline.py             # the rule, both pages both ways, then the plants
    python scripts/test-scores-offline.py --no-plants

  rule      no served .html/.js file except schools/assets/firebase-leaderboard.js calls firebase.database or
            firebase.initializeApp (a direct call throws on a network that blocks the SDK and stops the page)
  blocked   gstatic.com/firebasejs refused (a college network): /leaderboards/ has no page error, renders Your
            Scores from the device (one seeded game) and shows its "can't load on this network" line; the portal
            has no page error and hides its ticker
  live      a fake SDK in its place: /leaderboards/ renders its game cards, the portal ticker shows the fake
            recent score; neither shows the offline line (everything behaves as before)

Plants: a page that calls firebase.database() itself (the rule must name it); main's /leaderboards/ from before
the contract, under "blocked" (its Your Scores must be caught never rendering).
"""
import argparse
import asyncio
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SHARED = 'schools/assets/firebase-leaderboard.js'
DIRECT = re.compile(r'firebase\.(database|initializeApp)\s*\(')
NOT_SERVED = ('scripts/', 'docs/', '.github/', '.claude/', 'firebase/', 'tests/')

FAKE_SDK = r"""
(function () {
  var now = Date.now();
  var DATA = {
    recent_scores: { a: { game: 'Fake Game', slug: 'angle-ace', level: 'GCSE', score: 42, initials: 'ZZZ', timestamp: now } },
    leaderboards: {}
  };
  function at(path) {
    var o = DATA;
    path.split('/').forEach(function (p) { o = (o || {})[p]; });
    return o || null;
  }
  function snap(v) {
    return { val: function () { return v; },
             forEach: function (f) { Object.keys(v || {}).forEach(function (k) { f({ val: function () { return v[k]; } }); }); } };
  }
  function ref(path) {
    var r = {
      once: function () { return Promise.resolve(snap(at(path))); },
      on: function (ev, cb) { setTimeout(function () { cb(snap(at(path))); }, 0); },
      orderByChild: function () { return r; }, limitToLast: function () { return r; },
      push: function () { return Promise.resolve({ key: 'k' }); }, child: function (c) { return ref(path + '/' + c); }
    };
    return r;
  }
  window.firebase = { apps: [], initializeApp: function () { window.firebase.apps.push({}); return {}; },
                      app: function () { return {}; }, database: function () { return { ref: ref }; } };
})();
"""

SEED = """localStorage.setItem('mfg_hist_v1::angle-ace::gcse', JSON.stringify([{score: 17, timestamp: Date.now()}]));"""


def served_files():
    out = subprocess.run(['git', 'ls-files', '*.html', '*.js'], cwd=ROOT, capture_output=True, text=True).stdout
    return [f for f in out.split() if not f.startswith(NOT_SERVED)]


def rule(files, read=None):
    read = read or (lambda f: open(os.path.join(ROOT, f), encoding='utf-8', errors='replace').read())
    return [f for f in files if f != SHARED and DIRECT.search(read(f))]


async def page_state(browser, base, path, mode, body=None):
    ctx = await browser.new_context(viewport={'width': 1280, 'height': 900})
    try:
        await ctx.add_init_script(SEED)
        if mode == 'blocked':
            await ctx.route(re.compile(r'gstatic\.com/firebasejs'), lambda r: r.abort())
        else:
            await ctx.route(re.compile(r'gstatic\.com/firebasejs/.*firebase-app-compat\.js'), lambda r: r.fulfill(
                status=200, content_type='application/javascript', body=FAKE_SDK))
            await ctx.route(re.compile(r'gstatic\.com/firebasejs/.*firebase-database-compat\.js'), lambda r: r.fulfill(
                status=200, content_type='application/javascript', body='/* in the app stub */'))
        await ctx.route(lambda u: not u.startswith(base) and 'gstatic.com/firebasejs' not in u, lambda r: r.abort())
        if body is not None:
            await ctx.route(re.compile(re.escape(base + path) + r'$'), lambda r: r.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=body))
        page = await ctx.new_page()
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)[:120]))
        await page.goto(base + path, wait_until='load', timeout=20000)
        await page.wait_for_timeout(800)
        st = await page.evaluate('''() => {
            const vis = id => { const e = document.getElementById(id); return !!e && !e.hidden && getComputedStyle(e).display !== 'none'; };
            const ys = document.getElementById('yourScoresBody');
            const t = document.getElementById('scoreTicker');
            return { yours: ys ? ys.innerText : null, offline: vis('lbOffline'), cards: document.querySelectorAll('#gameGrid > *').length,
                     ticker: t ? (vis('scoreTicker') ? t.innerText : 'HIDDEN') : null };
        }''')
        st['errs'] = errs
        return st
    finally:
        await ctx.close()


def judge(path, mode, st):
    f = ['%s (%s): page error: %s' % (path, mode, e) for e in st['errs']]
    if path == '/leaderboards/':
        if not st['yours'] or 'Loading your local history' in st['yours'] or '17' not in st['yours']:
            f.append('%s (%s): Your Scores did not render the device history (%r)' % (path, mode, (st['yours'] or '')[:60]))
        if mode == 'blocked' and not st['offline']:
            f.append('%s (blocked): no "can\'t load on this network" line' % path)
        if mode == 'live' and (st['offline'] or not st['cards']):
            f.append('%s (live): offline line %s, %d game cards' % (path, st['offline'], st['cards']))
    else:
        if mode == 'blocked' and st['ticker'] != 'HIDDEN':
            f.append('/ (blocked): the ticker is not hidden (%r)' % (st['ticker'] or '')[:60])
        if mode == 'live' and (st['ticker'] in (None, 'HIDDEN') or 'Fake Game' not in st['ticker']):
            f.append('/ (live): the ticker does not show the recent score (%r)' % (st['ticker'] or '')[:60])
    return f


async def run(cases):
    from playwright.async_api import async_playwright
    proc, base = bc.start_stub_server()
    out = []
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            for path, mode, body in cases:
                out.append((path, mode, judge(path, mode, await page_state(browser, base, path, mode, body))))
            await browser.close()
    finally:
        proc.terminate()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-plants', action='store_true')
    a = ap.parse_args()
    fails = []
    files = served_files()
    bad = rule(files)
    print('rule: %d served .html/.js files; direct SDK calls outside %s: %s' % (len(files), SHARED, ', '.join(bad) or 'none'))
    fails += ['rule: %s calls the Firebase SDK directly (read through MaffsLeaderboard)' % f for f in bad]
    for path, mode, f in asyncio.run(run([(p, m, None) for p in ('/leaderboards/', '/') for m in ('blocked', 'live')])):
        print('  %s  %s (%s)%s' % ('FAIL' if f else 'ok  ', path, mode, (': ' + '; '.join(f)) if f else ''))
        fails += f
    if not a.no_plants:
        planted = rule(['x/plant.html'], lambda f: '<script>var db = firebase.database();</script>')
        print('  plant: a page calling firebase.database() itself: %s' % ('CAUGHT' if planted else 'MISSED'))
        if not planted:
            fails.append('plant: the rule missed a direct firebase.database() call')
        old = subprocess.run(['git', 'show', 'a2b745f:leaderboards/index.html'], cwd=ROOT, capture_output=True,
                             text=True, encoding='utf-8').stdout
        if not old:
            fails.append('plant: could not read the pre-contract /leaderboards/ (a2b745f)')
        else:
            (_, _, f), = asyncio.run(run([('/leaderboards/', 'blocked', old)]))
            caught = any('Your Scores did not render' in x or 'page error' in x for x in f)
            print('  plant: /leaderboards/ before the contract, Firebase blocked: %s' % ('CAUGHT (%s)' % f[0][:90] if caught else 'MISSED'))
            if not caught:
                fails.append('plant: the pre-contract /leaderboards/ passed with Firebase blocked')
    print('PASS' if not fails else 'FAIL: %d' % len(fails))
    return 0 if not fails else 1


if __name__ == '__main__':
    sys.exit(main())
