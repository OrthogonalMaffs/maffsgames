#!/usr/bin/env python3
# ci-line: Portal score ticker pause (the ticker stops on hover, on keyboard focus in its scores and with its own pause/play button, which keeps its state through hover and focus; nothing moves under prefers-reduced-motion; its height is 36 px at 360, 768 and 1440; planted faults caught) |
# ci-deps: index.html
"""Contract TICKER-PAUSE (Jon, 29 Oct 2026; WCAG 2.2.2 Pause, Stop, Hide): the portal's scrolling score ticker.

    python scripts/check-ticker-pause.py              # the checks at 1440, 768 and 360, then the planted faults
    python scripts/check-ticker-pause.py --no-plants

The page is served with a fake Firebase SDK (twelve recent scores, so the ticker has something to run) and measured in Chromium:

  Running   the scores move on their own (the strip's transform changes over 350 ms).
  Hover     with the pointer over the scores they stop at once; off them they run again.
  Focus     with keyboard focus on an element inside the scores (a link added by the test: the scores have none of their own today) they
            stop; with focus back on the button they run again.
  Button    a real <button> inside the ticker, at its left edge, named "Pause scores" with aria-pressed false; pressing it stops the scores
            at once, names it "Play scores", aria-pressed true; the stopped state survives the pointer going over the scores and off,
            and keyboard focus going into the scores and out; pressing again runs them (with the pointer still over the button: hovering
            the button itself holds nothing still). Enter and Space both press it; it takes keyboard focus.
  Reduced   under prefers-reduced-motion: reduce, nothing moves, only one set of the scores is shown (every score still there), the
            button is hidden (there is nothing to pause), and the track scrolls sideways by hand.
  Size      the ticker is 36 px tall, and the page does not scroll sideways, at 360, 768 and 1440 px.

Plants (through scripts/plant_common.py, so a plant that does not apply fails the run): no hover pause, a button that sets no state, a button
that never changes its name, no focus pause, no reduced-motion rule.
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
import plant_common as pc  # noqa: E402

FAKE_SDK = r"""
(function () {
  var now = Date.now(), recent = {};
  for (var i = 0; i < 12; i++) recent['k' + i] = { game: 'Fake Game ' + i, slug: 'angle-ace', level: 'GCSE', score: 40 + i, initials: 'AB' + (i % 10), timestamp: now - i * 60000 };
  var DATA = { recent_scores: recent, leaderboards: {} };
  function at(path) { var o = DATA; path.split('/').forEach(function (p) { o = (o || {})[p]; }); return o || null; }
  function snap(v) { return { val: function () { return v; },
    forEach: function (f) { Object.keys(v || {}).forEach(function (k) { f({ val: function () { return v[k]; } }); }); } }; }
  function ref(path) {
    var r = { once: function () { return Promise.resolve(snap(at(path))); },
      on: function (ev, cb) { setTimeout(function () { cb(snap(at(path))); }, 0); },
      orderByChild: function () { return r; }, limitToLast: function () { return r; },
      push: function () { return Promise.resolve({ key: 'k' }); }, child: function (c) { return ref(path + '/' + c); } };
    return r;
  }
  window.firebase = { apps: [], initializeApp: function () { window.firebase.apps.push({}); return {}; },
                      app: function () { return {}; }, database: function () { return { ref: ref }; } };
})();
"""

TX = """() => { const i = document.querySelector('#scoreTickerTrack .score-ticker-inner'); if (!i) return null;
  const m = getComputedStyle(i).transform; return m === 'none' ? 0 : parseFloat(m.split(',')[4]); }"""
STATE = """() => { const b = document.getElementById('tickerToggle'), t = document.getElementById('scoreTicker'), i = document.querySelector('.score-ticker-inner');
  return { label: b.getAttribute('aria-label'), pressed: b.getAttribute('aria-pressed'), tag: b.tagName, inTicker: t.contains(b),
           play: i ? getComputedStyle(i).animationPlayState : null, name: i ? getComputedStyle(i).animationName : null,
           h: Math.round(t.getBoundingClientRect().height), sideways: document.documentElement.scrollWidth > innerWidth,
           btnShown: getComputedStyle(b).display !== 'none', btnLeft: Math.round(b.getBoundingClientRect().left) - Math.round(t.getBoundingClientRect().left) }; }"""


async def moving(page, ms=350):
    await page.wait_for_timeout(120)      # let a pause that has just been asked for take hold
    a = await page.evaluate(TX)
    await page.wait_for_timeout(ms)
    b = await page.evaluate(TX)
    return a is not None and abs(b - a) > 0.5


async def context(browser, base, size, body, reduced=False):
    ctx = await browser.new_context(viewport={'width': size[0], 'height': size[1]}, reduced_motion='reduce' if reduced else 'no-preference')
    await ctx.route(re.compile(r'gstatic\.com/firebasejs/.*firebase-app-compat\.js'),
                    lambda r: r.fulfill(status=200, content_type='application/javascript', body=FAKE_SDK))
    await ctx.route(re.compile(r'gstatic\.com/firebasejs/.*firebase-database-compat\.js'),
                    lambda r: r.fulfill(status=200, content_type='application/javascript', body='/* in the app stub */'))
    await ctx.route(lambda u: not u.startswith(base) and 'gstatic.com/firebasejs' not in u, lambda r: r.abort())
    if body is not None:
        await ctx.route(re.compile(re.escape(base) + r'/$'), lambda r: r.fulfill(status=200, content_type='text/html; charset=utf-8', body=body))
    page = await ctx.new_page()
    errs = []
    page.on('pageerror', lambda e: errs.append(str(e)[:120]))
    await page.goto(base + '/', wait_until='load', timeout=20000)
    await page.wait_for_selector('#scoreTickerTrack .score-ticker-inner', timeout=8000)
    await page.wait_for_timeout(500)
    return ctx, page, errs


async def checks(browser, base, size, body=None):
    where = '%dx%d' % size
    f = []
    ctx, page, errs = await context(browser, base, size, body)
    try:
        f += ['%s: page error: %s' % (where, e) for e in errs]
        st = await page.evaluate(STATE)
        if st['h'] != 36:
            f.append('%s: the ticker is %d px tall, not 36' % (where, st['h']))
        if st['sideways']:
            f.append('%s: the page scrolls sideways' % where)
        if st['tag'] != 'BUTTON' or not st['inTicker']:
            f.append('%s: the pause control is not a <button> inside the ticker' % where)
        if st['btnLeft'] > 2:
            f.append('%s: the pause button is %d px from the ticker\'s left edge' % (where, st['btnLeft']))
        if st['label'] != 'Pause scores' or st['pressed'] != 'false':
            f.append('%s: the button starts as %r / aria-pressed %r, not "Pause scores" / false' % (where, st['label'], st['pressed']))
        if not await moving(page):
            f.append('%s: the scores do not move on their own' % where)
        box = await page.evaluate("() => { const r = document.getElementById('scoreTickerTrack').getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; }")
        bb = await page.evaluate("() => { const r = document.getElementById('tickerToggle').getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; }")
        track_pt = (box[0] + box[2] / 2, box[1] + box[3] / 2)
        btn_pt = (bb[0] + bb[2] / 2, bb[1] + bb[3] / 2)
        await page.evaluate("() => document.getElementById('scoreTicker').scrollIntoView({block: 'center'})")
        box = await page.evaluate("() => { const r = document.getElementById('scoreTickerTrack').getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; }")
        bb = await page.evaluate("() => { const r = document.getElementById('tickerToggle').getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; }")
        track_pt = (box[0] + box[2] / 2, box[1] + box[3] / 2)
        btn_pt = (bb[0] + bb[2] / 2, bb[1] + bb[3] / 2)
        away = (box[0] + box[2] / 2, max(2, box[1] - 60))

        # hover
        await page.mouse.move(*track_pt)
        if await moving(page):
            f.append('%s: the scores keep moving with the pointer over them' % where)
        await page.mouse.move(*away)
        if not await moving(page):
            f.append('%s: the scores do not run again when the pointer leaves' % where)

        # keyboard focus inside the scores (the test adds a link: the scores have none of their own)
        await page.evaluate("() => { const a = document.createElement('a'); a.href = '#t'; a.id = 'tpLink'; a.textContent = 'x'; "
                            "document.querySelector('.score-ticker-inner').appendChild(a); }")
        await page.focus('#tickerToggle')
        await page.keyboard.press('Tab')
        if not await page.evaluate("() => document.activeElement && document.activeElement.id === 'tpLink'"):
            f.append('%s: the test could not move keyboard focus into the scores' % where)
        elif await moving(page):
            f.append('%s: the scores keep moving while a keyboard-focused element in them has focus' % where)
        await page.keyboard.press('Shift+Tab')
        if not await moving(page):
            f.append('%s: the scores do not run again when focus leaves them for the button' % where)

        # the button
        await page.mouse.click(*btn_pt)
        await page.wait_for_timeout(60)
        st = await page.evaluate(STATE)
        if st['pressed'] != 'true' or st['label'] != 'Play scores':
            f.append('%s: after a press the button is %r / aria-pressed %r, not "Play scores" / true' % (where, st['label'], st['pressed']))
        if await moving(page):
            f.append('%s: the scores keep moving after Pause is pressed' % where)
        await page.mouse.move(*track_pt)
        await page.mouse.move(*away)
        if await moving(page):
            f.append('%s: a pause set by the button was undone by the pointer going over the scores and off' % where)
        await page.focus('#tickerToggle')
        await page.keyboard.press('Tab')
        await page.keyboard.press('Shift+Tab')
        if await moving(page):
            f.append('%s: a pause set by the button was undone by keyboard focus going into the scores and out' % where)
        await page.mouse.click(*btn_pt)
        await page.wait_for_timeout(60)
        st = await page.evaluate(STATE)
        if st['pressed'] != 'false' or st['label'] != 'Pause scores':
            f.append('%s: after a second press the button is %r / %r, not "Pause scores" / false' % (where, st['label'], st['pressed']))
        if not await moving(page):
            f.append('%s: the scores do not run again after Play is pressed (pointer still over the button)' % where)

        # keyboard alone
        await page.focus('#tickerToggle')
        for key in ('Enter', 'Space'):
            await page.keyboard.press(key)
            await page.wait_for_timeout(60)
            if await moving(page):
                f.append('%s: %s on the button did not pause the scores' % (where, key))
            await page.keyboard.press(key)
            await page.wait_for_timeout(60)
            if not await moving(page):
                f.append('%s: %s on the button did not play the scores' % (where, key))
    finally:
        await ctx.close()

    # reduced motion
    ctx, page, errs = await context(browser, base, size, body, reduced=True)
    try:
        st = await page.evaluate(STATE)
        if await moving(page, 500) or st['name'] != 'none':
            f.append('%s: under prefers-reduced-motion the scores still move (animation %r)' % (where, st['name']))
        shown = await page.evaluate("() => [...document.querySelectorAll('.score-ticker-item')].filter(e => e.offsetParent !== null).length")
        if shown != 12:
            f.append('%s: under prefers-reduced-motion %d scores are shown, expected the 12 once each' % (where, shown))
        if st['btnShown']:
            f.append('%s: the pause button is still shown under prefers-reduced-motion (nothing moves)' % where)
        if st['h'] != 36:
            f.append('%s: under prefers-reduced-motion the ticker is %d px tall, not 36' % (where, st['h']))
        scroll = await page.evaluate("() => { const t = document.getElementById('scoreTickerTrack'); return [getComputedStyle(t).overflowX, t.scrollWidth > t.clientWidth]; }")
        if scroll[0] != 'auto':
            f.append('%s: under prefers-reduced-motion the track does not scroll by hand (overflow-x %s)' % (where, scroll[0]))
    finally:
        await ctx.close()
    return f


# (name, old text, new text, what the check must say)
PLANTS = [
    ('no hover pause', '  .score-ticker-track:hover .score-ticker-inner,\n', '', r'keep moving with the pointer over them'),
    ('a button that sets no state', "      box.classList.toggle('tp-user', paused);\n", '', r'keep moving after Pause is pressed'),
    ('a button that never changes its name',
     "      btn.setAttribute('aria-label', paused ? 'Play scores' : 'Pause scores');\n", '', r'after a press the button is'),
    ('no keyboard-focus pause', "box.classList.add('tp-focus')", "void 0", r'keyboard-focused element in them has focus'),
    ('no reduced-motion rule', '    .score-ticker-inner{animation:none !important;transform:none !important;}\n', '', r'under prefers-reduced-motion the scores still move'),
]


async def run(plants):
    from playwright.async_api import async_playwright
    proc, base = bc.start_stub_server()
    html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    fails = []
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            for size in ((1440, 900), (768, 1024), (360, 640)):
                got = await checks(browser, base, size)
                print('  %s  %dx%d%s' % ('FAIL' if got else 'ok  ', size[0], size[1], (': ' + '; '.join(got[:3])) if got else ''))
                fails += got
            if plants:
                for name, old, new, want in PLANTS:
                    try:
                        body = pc.apply_plant(html, old, new, name=name)
                    except pc.StalePlant as exc:
                        print('  FAIL  %s' % exc)
                        fails.append(str(exc))
                        continue
                    try:
                        got = await checks(browser, base, (1440, 900), body)
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
