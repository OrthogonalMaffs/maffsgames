#!/usr/bin/env python3
# ci-line: Shared answer lock (schools/assets/answer-lock.js, MaffsLock: every behaviour in Chromium, four planted faults) |
# ci-deps: schools/assets/answer-lock.js schools/assets/next-control.js
"""Browser test for the shared answer lock, schools/assets/answer-lock.js (MaffsLock, canon §7.6).

    python scripts/test-answer-lock.py              # the repo's helper, then the planted faults
    python scripts/test-answer-lock.py --no-plants  # the repo's helper only

A fixture game (four options: three buttons and a tabindex tile; a wrong answer shows MaffsNext over
the first option; a right answer advances on a MaffsLock.timer; a key handler answers on 1-4 and Enter)
is played in headless Chromium against the real next-control.js and answer-lock.js:

  once        lock() is true once per question, false after; every control gets the disabled attribute
              (where it has one) and aria-disabled
  capture     after the lock, a click on the tile and Enter/Space on it never reach its own listeners
  re-mark     clicking the answered option again, Enter, Space and the game's 1-4 keys change nothing
  fresh       a click within FRESH_MS of a new question is ignored; one after it is marked; isFresh()
              says so for the container and for no target, never for an element outside it
  dblclick    a double-click on Next advances once and its second click does not answer the next
              question (the option under it)
  double-tap  the same with two taps at 390px on a touch screen
  keys        two Enter presses on a focused option mark once
  own-next    a game's own Next marked data-maffs-lock-skip is never locked, but fresh() covers it
  timer       a right answer's advance timer does not fire after a screen change (screen()), and a
              timer set on the wrong path does not fire after MaffsNext's advance
  finish      finishOnce() runs once per session, and again after newSession()

Then each planted fault (a CSS-only lock, no fresh delay, timers never cleared, a double finish) is put
into a copy of the helper; each must FAIL a named check.
"""
import argparse
import asyncio
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOCK = os.path.join(ROOT, 'schools', 'assets', 'answer-lock.js')
NEXT = os.path.join(ROOT, 'schools', 'assets', 'next-control.js')

FIXTURE = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body { font: 16px sans-serif; margin: 16px; }
  #stage { position: relative; width: 300px; }
  #area button, #area .tile { display: block; width: 300px; height: 60px; margin: 0 0 8px; box-sizing: border-box; }
  #area .tile { border: 1px solid #888; cursor: pointer; }
  #fb { position: absolute; left: 0; top: 0; width: 300px; }
  #fb .maffs-next { width: 300px; height: 60px; margin: 0; }
</style></head>
<body><div id="stage"><div id="area"></div><div id="fb"></div></div><div id="screen2" hidden>Menu</div>
<script>%(next)s</script>
<script>%(lock)s</script>
<script>
  MaffsNext.FLOOR_MS = 0;
  var area = document.getElementById('area'), fb = document.getElementById('fb');
  window.S = { q: 0, answered: 0, score: 0, advanced: 0, drawn: 0, completed: 0, rawTile: 0, rawTileKey: 0 };
  function answer(i) {
    if (!MaffsLock.lock(area)) return;
    S.answered++;
    if (i === 0) { S.score++; MaffsLock.timer(advance, 400); }
    else {
      MaffsLock.timer(function () { S.drawn++; }, 400);      // a solution animation's next frame
      MaffsNext.wrong({ mount: fb, onAdvance: advance });
    }
  }
  function render() {
    S.q++;
    area.innerHTML = '';
    for (var i = 0; i < 3; i++) {
      var b = document.createElement('button');
      b.className = 'opt'; b.dataset.i = i; b.textContent = 'Q' + S.q + ' option ' + i;
      b.addEventListener('click', (function (k) { return function () { answer(k); }; })(i));
      area.appendChild(b);
    }
    var t = document.createElement('div');
    t.className = 'tile'; t.tabIndex = 0; t.dataset.i = 3; t.textContent = 'Q' + S.q + ' tile';
    t.addEventListener('click', function () { S.rawTile++; answer(3); });
    t.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { S.rawTileKey++; answer(3); }
    });
    area.appendChild(t);
    MaffsLock.fresh(area);
  }
  function advance() { S.advanced++; render(); }
  document.addEventListener('keydown', function (e) {
    if ('1234'.indexOf(e.key) !== -1 && e.key !== '') answer(Number(e.key) - 1);
  });
  window.endGame = MaffsLock.finishOnce(function () { S.completed++; });
  render();
</script></body></html>"""

PLANTS = [
    ('a CSS-only lock', 're-mark',
     'function lock(container) {',
     "function lock(container) { if (container) container.classList.add('answered'); return true;"),
    ('no fresh delay', 'fresh', 'var FRESH_MS = 300;', 'var FRESH_MS = 0;'),
    ('timers never cleared', 'timer', 'function clearTimers() {', 'function clearTimers() { return;'),
    ('a double finish', 'finish', 'if (ran === session) return undefined;', ''),
]


async def suite(browser, lock_js, next_js):
    """[(check, ok, detail)] for one copy of the helper."""
    html = FIXTURE % {'lock': lock_js, 'next': next_js}
    out = []

    def check(name, ok, detail=''):
        out.append((name, bool(ok), detail))

    async def fresh_page(**ctx_kw):
        ctx = await browser.new_context(**ctx_kw)
        page = await ctx.new_page()
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        await page.set_content(html)
        await page.wait_for_timeout(350)        # past the first question's fresh window
        return ctx, page, errors

    async def S(page):
        return await page.evaluate('() => Object.assign({}, S)')

    # once
    ctx, page, errors = await fresh_page()
    r = await page.evaluate("""() => {
        const before = MaffsLock.isLocked(area);
        const a = MaffsLock.lock(area), b = MaffsLock.lock(area), during = MaffsLock.isLocked(area);
        const btns = [...area.querySelectorAll('button')], all = [...area.children];
        const disabled = btns.every(e => e.disabled), aria = all.every(e => e.getAttribute('aria-disabled') === 'true');
        render();
        const after = MaffsLock.isLocked(area);
        return { a, b, before, during, after, disabled, aria };
    }""")
    check('once', r['a'] is True and r['b'] is False and r['disabled'] and r['aria']
          and [r['before'], r['during'], r['after']] == [False, True, False],
          'lock() %s then %s; buttons disabled %s; aria-disabled on all %s; isLocked %s/%s/%s (before/after lock/next question)'
          % (r['a'], r['b'], r['disabled'], r['aria'], r['before'], r['during'], r['after']))
    await ctx.close()

    # capture: a locked tile's own listeners never see a click or a key
    ctx, page, errors = await fresh_page()
    await page.focus('#area .tile')
    await page.evaluate('() => MaffsLock.lock(area)')
    await page.evaluate("() => document.querySelector('#area .tile').click()")
    await page.keyboard.press('Enter')
    await page.keyboard.press(' ')
    s = await S(page)
    check('capture', s['rawTile'] == 0 and s['rawTileKey'] == 0,
          'tile listeners after the lock: %d click(s), %d key(s)' % (s['rawTile'], s['rawTileKey']))
    await ctx.close()

    # re-mark: the answered option, Enter, Space and the game's own keys change nothing
    ctx, page, errors = await fresh_page()
    await page.evaluate('() => { MaffsNext.FLOOR_MS = 3000; }')   # the real floor: no key may advance
    await page.focus('#area .tile')
    await page.keyboard.press('Enter')              # answers via the tile (wrong: index 3)
    before = await S(page)
    await page.keyboard.press('Enter')
    await page.keyboard.press(' ')
    await page.keyboard.press('1')
    await page.keyboard.press('2')
    await page.evaluate("() => document.querySelector('#area .tile').click()")
    await page.evaluate("() => document.querySelector('#area .opt').click()")
    after = await S(page)
    check('re-mark', before['answered'] == 1 and after['answered'] == 1 and after['score'] == 0,
          'answered %d then %d after Enter, Space, 1, 2 and two clicks; score %d'
          % (before['answered'], after['answered'], after['score']))
    await ctx.close()

    # fresh: a click straight after a new question renders is ignored; one after FRESH_MS is marked
    ctx, page, errors = await fresh_page()
    r = await page.evaluate("""async () => {
        render();
        const seen = () => [MaffsLock.isFresh(area), MaffsLock.isFresh(), MaffsLock.isFresh(fb)];
        const during = seen();
        document.querySelector('#area .opt').click();
        const early = S.answered;
        await new Promise(res => setTimeout(res, 350));
        const after = seen();
        document.querySelector('#area .opt').click();
        return { early, late: S.answered, during, after };
    }""")
    check('fresh', r['early'] == 0 and r['late'] == 1
          and r['during'] == [True, True, False] and r['after'] == [False, False, False],
          'answered %d straight after render, %d after 350 ms; isFresh(area, none, outside) %s then %s'
          % (r['early'], r['late'], r['during'], r['after']))
    await ctx.close()

    # dblclick on Next: one advance, and the second click does not answer the option under it
    ctx, page, errors = await fresh_page()
    await page.click('#area button[data-i="1"]')     # wrong: Next appears over the first option
    await page.wait_for_selector('#fb .maffs-next:not([disabled])')
    before = await S(page)
    await page.dblclick('#fb .maffs-next')
    await page.wait_for_timeout(450)
    after = await S(page)
    check('dblclick', after['advanced'] == before['advanced'] + 1 and after['answered'] == before['answered'],
          'advanced %+d, answered %+d' % (after['advanced'] - before['advanced'], after['answered'] - before['answered']))
    await ctx.close()

    # double-tap on Next at 390px
    ctx, page, errors = await fresh_page(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True)
    await page.tap('#area button[data-i="2"]')
    await page.wait_for_selector('#fb .maffs-next:not([disabled])')
    box = await page.locator('#fb .maffs-next').bounding_box()
    before = await S(page)
    x, y = box['x'] + box['width'] / 2, box['y'] + box['height'] / 2
    await page.touchscreen.tap(x, y)
    await page.wait_for_timeout(60)
    await page.touchscreen.tap(x, y)
    await page.wait_for_timeout(450)
    after = await S(page)
    check('double-tap', after['advanced'] == before['advanced'] + 1 and after['answered'] == before['answered'],
          'at 390px: advanced %+d, answered %+d' % (after['advanced'] - before['advanced'], after['answered'] - before['answered']))
    await ctx.close()

    # keys: two quick Enters on a focused option mark once
    ctx, page, errors = await fresh_page()
    await page.evaluate('() => { MaffsNext.FLOOR_MS = 3000; }')
    await page.focus('#area .tile')
    await page.keyboard.press('Enter')
    await page.keyboard.press('Enter')
    s = await S(page)
    check('keys', s['answered'] == 1, 'two Enters on a focused option: answered %d' % s['answered'])
    await ctx.close()

    # own-next: a game's own Next inside the container, marked data-maffs-lock-skip, is never locked, but the
    # fresh window covers it (a second Enter on it must not load the question after the one it just loaded)
    ctx, page, errors = await fresh_page()
    r = await page.evaluate("""async () => {
        let n = 0;
        const own = document.createElement('button');
        own.setAttribute('data-maffs-lock-skip', ''); own.textContent = 'Next';
        own.addEventListener('click', () => { n++; });
        render(); area.appendChild(own);
        own.click();
        const early = n;
        await new Promise(res => setTimeout(res, 350));
        MaffsLock.lock(area); own.click();
        return { early, late: n, disabled: own.disabled };
    }""")
    check('own-next', r['early'] == 0 and r['late'] == 1 and not r['disabled'],
          'skip-marked Next: %d click(s) in the fresh window, %d after the lock; disabled %s'
          % (r['early'], r['late'], r['disabled']))
    await ctx.close()

    # timer: a right answer's advance does not fire after a screen change; a wrong path's timer does not
    # fire after MaffsNext's advance
    ctx, page, errors = await fresh_page()
    r = await page.evaluate("""async () => {
        document.querySelector('#area .opt[data-i="0"]').click();       // right: advance in 400 ms
        MaffsLock.screen(document.getElementById('screen2'));          // the student leaves for the menu
        await new Promise(res => setTimeout(res, 600));
        const afterScreen = S.advanced;
        render();
        await new Promise(res => setTimeout(res, 350));
        document.querySelector('#area .opt[data-i="1"]').click();       // wrong: a 400 ms timer + Next
        await new Promise(res => setTimeout(res, 20));
        document.querySelector('#fb .maffs-next').click();
        await new Promise(res => setTimeout(res, 600));
        return { afterScreen, drawn: S.drawn };
    }""")
    check('timer', r['afterScreen'] == 0 and r['drawn'] == 0,
          'advance fired %d time(s) after screen(); wrong-path timer fired %d time(s) after Next'
          % (r['afterScreen'], r['drawn']))
    await ctx.close()

    # finish: once per session
    ctx, page, errors = await fresh_page()
    r = await page.evaluate("""() => {
        endGame(); endGame();
        const one = S.completed;
        MaffsLock.newSession(); endGame(); endGame();
        return { one, two: S.completed };
    }""")
    check('finish', r['one'] == 1 and r['two'] == 2,
          'end handler ran %d time(s) in one session, %d after newSession()' % (r['one'], r['two']))
    if errors:
        check('page errors', False, '; '.join(errors[:3]))
    await ctx.close()
    return out


async def run(plants):
    from playwright.async_api import async_playwright
    lock_js = open(LOCK, encoding='utf-8').read()
    next_js = open(NEXT, encoding='utf-8').read()
    ok = True
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        print('MaffsLock (schools/assets/answer-lock.js):')
        for name, good, detail in await suite(browser, lock_js, next_js):
            print('  %s  %-11s %s' % ('PASS' if good else 'FAIL', name, detail))
            ok = ok and good
        if plants:
            print('\nPlanted faults (each must fail its check):')
            for what, want, old, new in PLANTS:
                if lock_js.count(old) != 1:
                    print('  FAIL  %-22s cannot plant: %r found %d times' % (what, old, lock_js.count(old)))
                    ok = False
                    continue
                res = await suite(browser, lock_js.replace(old, new), next_js)
                failed = [n for n, good, _ in res if not good]
                caught = want in failed
                print('  %s  %-22s %s' % ('PASS' if caught else 'FAIL', what,
                                          ('caught by %s' % ', '.join(failed)) if caught
                                          else 'MISSED (failed: %s)' % (', '.join(failed) or 'nothing')))
                ok = ok and caught
        await browser.close()
    print('\n' + ('PASS' if ok else 'FAILED'))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-plants', action='store_true')
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    return asyncio.run(run(not args.no_plants))


if __name__ == '__main__':
    sys.exit(main())
