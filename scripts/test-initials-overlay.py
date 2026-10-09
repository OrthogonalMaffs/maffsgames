#!/usr/bin/env python3
# ci-line: Shared initials overlay (schools/assets/firebase-leaderboard.js: no key typed into it reaches a game, in every game that loads it; the old overlay planted and caught) |
# ci-deps: schools/assets/firebase-leaderboard.js
"""Browser test for the shared initials overlay's key containment (contract OVERLAY-KEYS, 9 Oct 2026).

    python scripts/test-initials-overlay.py                 # every game, then the planted fault
    python scripts/test-initials-overlay.py --no-plants     # every game only
    python scripts/test-initials-overlay.py --against FILE  # run the games against another copy of the overlay
                                                            # (e.g. main's, to list the games it fails)

Every game page that loads firebase-leaderboard.js is opened in headless Chromium with a fake Firebase that
records writes. Every key listener the page registers before the overlay opens (its shortcuts, on document,
window or any element) is counted, and the test adds its own document and window keydown probes, so the
check bites in a game with no shortcuts too. Then MaffsLeaderboard.submitScore() opens the overlay and:

  typed     every key any game binds (a-z, 0-9, space, arrows, Escape and punctuation) is typed into the
            focused initials input, then Enter
  backdrop  before Enter, a tap on the overlay's backdrop moves focus out of the inputs and more keys are
            pressed: they must not reach the page either
  submitted the overlay is gone, submitScore resolved, and the submit path saved the initials typed (ABC);
            off the production host it writes nothing after that, by design, so the fake Firebase stays empty
  untouched no game key listener and no probe saw a key from the first key typed to Enter's keyup, and the
            page did not navigate (listeners added by shared assets, /schools/assets/, are counted apart)
  released  a key pressed after the overlay closed reaches the page again

The plant removes the containment from a copy of the overlay; games with shortcuts must then FAIL.
"""
import argparse
import asyncio
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

ASSET = os.path.join(ROOT, 'schools', 'assets', 'firebase-leaderboard.js')
KEYS = (list('abcdefghijklmnopqrstuvwxyz') + list('0123456789') +
        ['Space', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Escape', '-', '=', '/', '.', ',', '?'])
BACKDROP_KEYS = ['r', 'n', 'Space', 'Escape', '1', 'ArrowRight']
PARALLEL = 3                       # as check-answer-lock's WORKERS: the stub server refuses past that on Windows

INIT = r"""
(function () {
  window.__ovl = { writes: [], game: [], probe: 0, shared: 0, armed: false };
  // A fake Firebase: the overlay opens only when the database initialised; writes are recorded, never sent.
  var store = {};
  function ref(path) {
    return {
      push: function (v) { __ovl.writes.push({ path: path, v: v }); (store[path] = store[path] || {})['k' + __ovl.writes.length] = v;
                           return Promise.resolve({ key: 'k' }); },
      once: function () { return Promise.resolve({ val: function () { return store[path] || null; } }); },
      set: function (v) { __ovl.writes.push({ path: path, v: v }); return Promise.resolve(); },
      child: function (c) { return ref(path + '/' + c); }
    };
  }
  var db = { ref: ref };
  window.firebase = { apps: [], initializeApp: function () { return {}; }, app: function () { return {}; },
                      database: Object.assign(function () { return db; }, { ServerValue: { TIMESTAMP: 0 } }) };
  Object.defineProperty(window, 'firebase', { value: window.firebase, writable: false, configurable: false });
  // Count every key listener the page registers while no overlay is open, when a key reaches it. One added by
  // a shared asset (/schools/assets/, e.g. the answer lock's capture guard) is counted apart: it is not a
  // game shortcut. A wrapped listener stays removable by the function the page passed.
  var add = EventTarget.prototype.addEventListener, remove = EventTarget.prototype.removeEventListener;
  var wraps = new WeakMap();
  EventTarget.prototype.addEventListener = function (type, fn, opts) {
    if (/^key(down|up|press)$/.test(type) && typeof fn === 'function' && !document.getElementById('mfg-initials-overlay')) {
      var caller = (new Error().stack || '').split('\n').slice(2, 3).join('');
      var shared = caller.indexOf('/schools/assets/') >= 0;
      var owner = this === window ? 'window' : this === document ? 'document' : (this.id ? '#' + this.id : (this.tagName || '?').toLowerCase());
      var wrapped = wraps.get(fn) || function (e) {
        if (__ovl.armed) { if (shared) __ovl.shared++; else __ovl.game.push(owner + ' ' + type + ' ' + e.key); }
        return fn.apply(this, arguments);
      };
      wraps.set(fn, wrapped);
      return add.call(this, type, wrapped, opts);
    }
    return add.call(this, type, fn, opts);
  };
  EventTarget.prototype.removeEventListener = function (type, fn, opts) {
    remove.call(this, type, (fn && wraps.get(fn)) || fn, opts);
    return remove.call(this, type, fn, opts);
  };
  window.__ovlProbe = function () {
    add.call(document, 'keydown', function () { if (__ovl.armed) __ovl.probe++; });
    add.call(window, 'keydown', function () { if (__ovl.armed) __ovl.probe++; });
  };
})();
"""


def games():
    out = []
    for slug in sorted(os.listdir(os.path.join(ROOT, 'games'))):
        p = os.path.join(ROOT, 'games', slug, 'index.html')
        if os.path.exists(p) and 'firebase-leaderboard.js' in open(p, encoding='utf-8').read():
            out.append(slug)
    return out


def plant(src):
    """The overlay before OVERLAY-KEYS: the containment listeners are never added."""
    out = src.replace("overlay.addEventListener(t, contain);", "").replace("window.addEventListener(t, guard, true);", "")
    assert out != src, 'plant: containment lines not found'
    return out


async def one(browser, base, slug, level, asset_body):
    ctx = await browser.new_context(viewport={'width': 1280, 'height': 900})
    try:
        await ctx.add_init_script(INIT)
        await ctx.route(lambda u: not u.startswith(base), lambda r: r.abort())
        if asset_body is not None:
            await ctx.route(re.compile(r'/schools/assets/firebase-leaderboard\.js(\?.*)?$'), lambda r: r.fulfill(
                status=200, content_type='application/javascript; charset=utf-8', body=asset_body))
        page = await ctx.new_page()
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)[:100]))
        url = base + '/games/%s/%s' % (slug, ('?level=%s' % level) if level else '')
        await page.goto(url, wait_until='load', timeout=20000)
        await page.wait_for_timeout(300)
        if not await page.evaluate('() => !!(window.MaffsLeaderboard && window.MaffsLeaderboard.submitScore)'):
            return ['no MaffsLeaderboard.submitScore on the page']
        href = page.url
        await page.evaluate('''(lv) => { __ovlProbe(); localStorage.removeItem('mfg_initials'); window.__ovlRes = null;
                                MaffsLeaderboard.submitScore(%r, lv || 'test', 7, 5).then(
                                  () => { __ovlRes = 'resolved'; }, (e) => { __ovlRes = 'rejected: ' + e; }); }''' % slug, level)
        try:
            await page.wait_for_function('() => document.activeElement && document.activeElement.classList.contains("mfg-ini-char")',
                                         timeout=3000)
        except Exception:
            return ['the overlay did not open with its first input focused']
        await page.evaluate('() => { __ovl.armed = true; }')
        for k in KEYS:
            await page.keyboard.press(k)
        await page.mouse.click(4, 4)                       # the backdrop: focus leaves the inputs
        for k in BACKDROP_KEYS:
            await page.keyboard.press(k)
        await page.locator('#mfg-initials-overlay .mfg-ini-char').nth(2).focus()
        await page.keyboard.press('Enter')
        await page.wait_for_timeout(250)
        st = await page.evaluate('''() => { __ovl.armed = false;
            return { open: !!document.getElementById('mfg-initials-overlay'), game: __ovl.game.slice(0, 6),
                     n: __ovl.game.length, probe: __ovl.probe, shared: __ovl.shared, res: __ovlRes,
                     saved: localStorage.getItem('mfg_initials') }; }''')
        # After the overlay: keys reach the page again (the guard released itself with Enter's keyup).
        await page.evaluate('() => { __ovl.probe = 0; __ovl.armed = true; }')
        await page.keyboard.press('x')
        after = await page.evaluate('() => { __ovl.armed = false; return __ovl.probe; }')
        faults = []
        if after != 2:
            faults.append('released: a key after the overlay closed reached %d of the 2 probes' % after)
        if st['open']:
            faults.append('submitted: the overlay is still open after Enter')
        # Off the production host submitScore writes nothing after the overlay (by design), so "submitted" is
        # read at the overlay's edge: its promise resolved and the submit path saved the initials typed.
        if st['res'] != 'resolved' or st['saved'] != 'ABC':
            faults.append('submitted: submitScore %s, initials saved %r (expected ABC)' % (st['res'] or 'pending', st['saved']))
        if st['n'] or st['probe']:
            faults.append('untouched: %d key(s) reached the game%s, %d the probes' % (
                st['n'], (' (' + ', '.join(st['game']) + ')') if st['game'] else '', st['probe']))
        if page.url != href:
            faults.append('untouched: the page navigated to %s' % page.url)
        # A page error (KaTeX blocked offline, say) is not this check's verdict: the overlay checks above are.
        return faults
    finally:
        await ctx.close()


async def run(slugs, asset_body):
    from playwright.async_api import async_playwright
    levels, _ = bc.roster_levels()
    proc, base = bc.start_stub_server()
    results = {}
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            sem = asyncio.Semaphore(PARALLEL)

            async def go(slug):
                async with sem:
                    try:
                        results[slug] = await one(browser, base, slug, (levels.get(slug) or [None])[0], asset_body)
                    except Exception as e:  # a page that cannot be driven is a failure, never a pass
                        results[slug] = ['could not drive the page: %s' % str(e).splitlines()[0][:120]]
            await asyncio.gather(*(go(s) for s in slugs))
            await browser.close()
    finally:
        proc.terminate()
    return results


def shortcut_games(slugs):
    pat = re.compile(r"(document|window)\.addEventListener\(\s*['\"]key(down|press|up)['\"]")
    return [s for s in slugs if pat.search(open(os.path.join(ROOT, 'games', s, 'index.html'), encoding='utf-8').read())]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-plants', action='store_true')
    ap.add_argument('--against', help='another copy of firebase-leaderboard.js to run the games against')
    ap.add_argument('--games', nargs='*')
    a = ap.parse_args()
    slugs = a.games or games()
    body = open(a.against, encoding='utf-8').read() if a.against else None
    res = asyncio.run(run(slugs, body))
    bad = {s: f for s, f in res.items() if f}
    print('Initials overlay (OVERLAY-KEYS): %d game(s) load it; %d typed %d keys + %d on the backdrop, then Enter'
          % (len(slugs), len(slugs), len(KEYS), len(BACKDROP_KEYS)))
    for s in sorted(res):
        print('  %s  %s%s' % ('FAIL' if res[s] else 'ok  ', s, (': ' + '; '.join(res[s])) if res[s] else ''))
    ok = not bad
    if not a.no_plants and not a.against:
        sc = shortcut_games(slugs)
        pres = asyncio.run(run(sc, plant(open(ASSET, encoding='utf-8').read())))
        missed = [s for s in sc if not any('reached the game' in f for f in pres[s])]
        print('plant (containment removed), %d game(s) with document/window key shortcuts: %s'
              % (len(sc), 'CAUGHT in every one' if not missed else 'MISSED in ' + ', '.join(missed)))
        ok = ok and not missed
    print('PASS' if ok else 'FAIL: %d game(s)' % len(bad))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
