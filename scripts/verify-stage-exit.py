#!/usr/bin/env python3
# ci-shards: Stage exit (the shared stage button and the standard back link on every stage game, played in Chromium: shown on the worked example and on a question of all seven games, one tap to the stage picker and one to the portal, no game_completed, no board submission, no score recorded, a pending Next control cleared so it cannot advance a stage that was left; fits at 320x568, 360x640, 375x667, 390x844 and 1280x720; planted faults, each caught) | | 4
# ci-deps: schools/assets/stage-exit.js schools/assets/stage-exit.css games/its-on-sale/ games/as-you-can-see/ games/possibly-maybe/ games/hc-factor/ games/y-so-steep/ games/i-found-a-mark/ games/free-daily-pizza/
"""Verification for the shared stage-exit shell (contract STAGE-EXIT, Jon, 28 Oct 2026).

The stage games hid "Back to Games" while a question was on screen and had no way back to the stage picker,
so the only ways out were ten questions or the browser's Back button. schools/assets/stage-exit.{js,css} give every
one of them a "Stages" button next to the standard back link while a stage or worked example is on screen.

For each of the seven games (Who Ate All the Pies? is exempt, see EXEMPT) this opens the page, starts a stage and, on the worked example (where the game has one)
and on a question, asserts:
  - the stage button and the Back to Games link are both on screen, inside the viewport, text at least 12 px;
  - one tap on the button reaches the stage picker (#menu active, body not playing), and no game_completed event,
    no leaderboard submission and no score-history record happened;
  - one tap on the back link goes to the portal (/);
  - a "Next" control pending when the student leaves is gone, and its fallback never advances the stage.
And at five sizes: both controls inside the viewport, no sideways scroll.

Planted faults (each must be caught): button never shown, back link hidden in play, leave fires game_completed,
leave submits to a board, leave leaves the Next control running, leave does nothing, a page that lost the script tag.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_common as bc  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Who Ate All the Pies? is exempt BY NAME (Jon, 28 Oct 2026): its HUD holds the calculator toggle, so the shared HUD
# controls do not fit at 320 and 360 px without breaking the phone-fit rules, and no fold rule is loosened. It keeps its
# hide rule and carries no stage-exit stylesheet or script. Revisit after the 2 Nov shared-infra freeze (docs/todo.md).
EXEMPT = ['who-ate-all-the-pies']
GAMES = ['its-on-sale', 'as-you-can-see', 'possibly-maybe',
         'hc-factor', 'y-so-steep', 'i-found-a-mark', 'free-daily-pizza']
SIZES = [(320, 568), (360, 640), (375, 667), (390, 844), (1280, 720)]
ASSETS = {'stage-exit.js': os.path.join(ROOT, 'schools', 'assets', 'stage-exit.js'),
          'stage-exit.css': os.path.join(ROOT, 'schools', 'assets', 'stage-exit.css')}
LABEL = {'hc-factor': '← Rounds', 'i-found-a-mark': '← Menu', 'free-daily-pizza': '← Menu'}
ACTIVE = "() => { const a = document.querySelector('.screen.active'); return a ? a.id : null; }"

MEASURE = """() => {
  const vis = (e) => { const cs = getComputedStyle(e), r = e.getBoundingClientRect();
    return cs.display !== 'none' && cs.visibility !== 'hidden' && r.width > 0 && r.height > 0; };
  const pick = (sel) => { const all = [...document.querySelectorAll(sel)]; return all.find(vis) || all[0] || null; };
  const b = pick('.stage-exit-stages'), a = pick('a.back-link, a.stage-exit-home');
  const box = (e) => { if (!e) return null; const cs = getComputedStyle(e), r = e.getBoundingClientRect();
    return { shown: vis(e), x: r.left, y: r.top, r: r.right, b: r.bottom, fs: parseFloat(cs.fontSize), h: r.height,
             txt: (e.textContent || '').trim() }; };
  const doc = document.documentElement;
  return { btn: box(b), link: box(a), vw: window.innerWidth, vh: window.innerHeight, sx: doc.scrollWidth - doc.clientWidth };
}"""


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def open_page(pw, base, slug, size, sources=None):
    sources = sources or {}
    br = pw.chromium.launch()
    touch = size[0] <= 600
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch)
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % re.escape(slug))
    if 'page' in sources:
        ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
            status=200, content_type='text/html; charset=utf-8', body=sources['page']))
    def serve(name, ctype):
        body = sources[name]
        ctx.route(lambda url: url.split('?')[0].endswith('/' + name), lambda route: route.fulfill(
            status=200, content_type=ctype + '; charset=utf-8', body=body))
    for name, ctype in (('stage-exit.js', 'application/javascript'), ('stage-exit.css', 'text/css')):
        if name in sources:
            serve(name, ctype)
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % slug, wait_until='load', timeout=20000)
    page.evaluate("""() => { window.__ev = []; window.__sub = []; window.__hist = [];
        window.mfg = (n, p) => { window.__ev.push(n); };
        window.MaffsLeaderboard = window.MaffsLeaderboard || {};
        MaffsLeaderboard.submitScore = () => { window.__sub.push(1); return Promise.resolve(); };
        if (window.MaffsScoreHistory) MaffsScoreHistory.record = () => { window.__hist.push(1); }; }""")
    return br, page, errors


def start_stage(page, out, where):
    """Start a stage the way a student does; return the active screen id."""
    for sel in ('#stageList [data-stage="1"]', '#stageListF [data-stage="1"]'):
        loc = page.locator(sel)
        if loc.count() and loc.first.is_visible() and loc.first.is_enabled():
            loc.first.click()
            break
    if page.evaluate(ACTIVE) == 'menu' and page.locator('#startBtn').count() and page.locator('#startBtn').is_visible():
        page.locator('#startBtn').click()
    page.wait_for_timeout(250)
    scr = page.evaluate(ACTIVE)
    if scr == 'menu':
        out.append('%s: could not start a stage' % where)
    return scr


def through_example(page, scr):
    for _ in range(24):
        if scr != 'example':
            break
        page.locator('#example button.btn.solid').first.click()
        page.wait_for_timeout(120)
        scr = page.evaluate(ACTIVE)
    return scr


def check_controls(page, slug, where, out, min_h=30):
    m = page.evaluate(MEASURE)
    want = LABEL.get(slug, '← Stages')
    if not m['btn'] or not m['btn']['shown']:
        out.append('%s: no "%s" button on screen' % (where, want))
        return False
    if m['btn']['txt'] != want:
        out.append('%s: button reads %r, not %r' % (where, m['btn']['txt'], want))
    if not m['link'] or not m['link']['shown']:
        out.append('%s: the Back to Games link is not on screen' % where)
        return False
    for name in ('btn', 'link'):
        e = m[name]
        if e['x'] < -0.5 or e['r'] > m['vw'] + 0.5 or e['y'] < -8 or e['b'] > m['vh'] + 0.5:
            out.append('%s: the %s is outside the viewport (%d..%d x %d..%d of %dx%d)' % (
                where, name, e['x'], e['r'], e['y'], e['b'], m['vw'], m['vh']))
        if e['fs'] < 12:
            out.append('%s: the %s text is %.1f px' % (where, name, e['fs']))
        if e['h'] < min_h:
            out.append('%s: the %s is only %d px tall' % (where, name, e['h']))
    if m['sx'] > 1:
        out.append('%s: the page scrolls sideways by %d px' % (where, m['sx']))
    return True


def leave_and_check(page, where, out):
    page.locator('.stage-exit-stages:visible').first.click()
    page.wait_for_timeout(300)
    if page.evaluate(ACTIVE) != 'menu':
        out.append('%s: one tap on the stage button did not reach the picker (still on %s)' % (where, page.evaluate(ACTIVE)))
    if page.evaluate("document.body.classList.contains('playing')"):
        out.append('%s: still playing after leaving' % where)
    if 'game_completed' in page.evaluate('window.__ev'):
        out.append('%s: leaving fired game_completed' % where)
    if page.evaluate('window.__sub.length'):
        out.append('%s: leaving submitted to a leaderboard' % where)
    if page.evaluate('window.__hist.length'):
        out.append('%s: leaving recorded a score' % where)


def exit_game(base, slug, size, out, sources=None):
    where = '%s %dx%d' % (slug, size[0], size[1])
    with sync_playwright() as pw:
        br, page, errors = open_page(pw, base, slug, size, sources)
        try:
            shown = page.evaluate("[...document.querySelectorAll('.stage-exit-stages')].some(b => b.getBoundingClientRect().width > 0)")
            if shown:
                out.append('%s: the stage button shows on the picker' % where)
            scr = start_stage(page, out, where)
            if scr == 'example':
                if check_controls(page, slug, where + ' worked example', out):
                    leave_and_check(page, where + ' worked example', out)
                scr = start_stage(page, out, where)
            scr = through_example(page, scr)
            if scr != 'game':
                out.append('%s: could not reach a question (on %s)' % (where, scr))
                return
            if not check_controls(page, slug, where + ' question', out):
                return
            # a Next control pending when the student leaves must not advance the stage later
            page.evaluate("""() => { const host = document.querySelector('#game .qcard') || document.getElementById('game');
                const mount = document.createElement('div'); host.appendChild(mount); window.__adv = 0;
                if (window.MaffsNext) MaffsNext.wrong({ mount: mount, onAdvance: () => { window.__adv++; }, fallbackMs: 1200 }); }""")
            leave_and_check(page, where + ' question', out)
            if page.evaluate("document.querySelectorAll('.maffs-next-wrap').length"):
                out.append('%s: a Next control was left running after leaving' % where)
            page.wait_for_timeout(2200)
            if page.evaluate('window.__adv'):
                out.append('%s: a Next control advanced the stage after the student left' % where)
            if page.evaluate(ACTIVE) != 'menu':
                out.append('%s: the page left the picker by itself (now %s)' % (where, page.evaluate(ACTIVE)))
            if 'game_completed' in page.evaluate('window.__ev'):
                out.append('%s: game_completed fired after leaving' % where)
            # the standard link takes a student to the portal in one tap, from a question too
            scr = through_example(page, start_stage(page, out, where))
            page.locator('a.back-link:visible, a.stage-exit-home:visible').first.click()
            page.wait_for_load_state('load')
            path = re.sub(r'^https?://[^/]+', '', page.url).split('?')[0]
            if path != '/':
                out.append('%s: the back link went to %s, not the portal' % (where, path))
            for e in errors:
                out.append('%s: page error %s' % (where, e[:120]))
        finally:
            br.close()


def fit_size(base, size, out):
    for slug in GAMES:
        where = '%s %dx%d' % (slug, size[0], size[1])
        with sync_playwright() as pw:
            br, page, errors = open_page(pw, base, slug, size)
            try:
                scr = start_stage(page, out, where)
                check_controls(page, slug, where + ' ' + str(scr), out)
                scr = through_example(page, scr)
                if scr == 'game':
                    check_controls(page, slug, where + ' question', out)
            finally:
                br.close()


def mutate(js=(), css=()):
    src = {'stage-exit.js': read(ASSETS['stage-exit.js']), 'stage-exit.css': read(ASSETS['stage-exit.css'])}
    for old, new in js:
        assert src['stage-exit.js'].count(old) == 1, old
        src['stage-exit.js'] = src['stage-exit.js'].replace(old, new)
    for old, new in css:
        assert src['stage-exit.css'].count(old) == 1, old
        src['stage-exit.css'] = src['stage-exit.css'].replace(old, new)
    return src


GO = "    var go = document.getElementById('menuBtn')"
PLANTS = [
    ('the stage button is never shown (example)', 'possibly-maybe',
     dict(css=[('body:has(#example.active) .stage-exit-row .stage-exit-stages{display:inline-flex}', 'body:has(#example.active) .stage-exit-row .stage-exit-stages{display:none}')]),
     r'no ".*" button on screen'),
    ('the stage button is never shown (HUD)', 'free-daily-pizza',
     dict(css=[('.hud .stage-exit-stages,.hud .stage-exit-home{display:inline-flex;', '.hud .stage-exit-stages,.hud .stage-exit-home{display:none;')]),
     r'no ".*" button on screen'),
    ('the back link is missing from the HUD', 'its-on-sale',
     dict(js=[('hud.appendChild(home);', 'void home;')]),
     r'Back to Games link is not on screen'),
    ('leaving fires game_completed', 'as-you-can-see',
     dict(js=[(GO, "    if (window.mfg) mfg('game_completed', {});\n" + GO)]),
     r'fired game_completed'),
    ('leaving submits to a board', 'possibly-maybe',
     dict(js=[(GO, "    if (window.MaffsLeaderboard) MaffsLeaderboard.submitScore('x', 'y', 1, 1);\n" + GO)]),
     r'submitted to a leaderboard'),
    ('leaving leaves a Next control running', 'hc-factor',
     dict(js=[('MaffsNext.clear(wraps[i].parentNode);', 'void 0;')]),
     r'Next control (was left running|advanced)'),
    ('leaving does nothing', 'y-so-steep',
     dict(js=[('if (go) go.click();', 'void go;')]),
     r'did not reach the picker'),
    ('a page that lost the script tag', 'i-found-a-mark', 'NOSCRIPT', r'no ".*" button on screen'),
]


def run_plant(p):
    what, slug, edit, want = p
    out = []
    if edit == 'NOSCRIPT':
        page_src = read(os.path.join(ROOT, 'games', slug, 'index.html'))
        tag = re.search(r'\n?<script src="\.\./\.\./schools/assets/stage-exit\.js"[^>]*></script>', page_src)
        assert tag, slug
        srcs = {'page': page_src.replace(tag.group(0), '')}
    else:
        srcs = mutate(edit.get('js', ()), edit.get('css', ()))
    proc, base = bc.start_stub_server()
    try:
        exit_game(base, slug, (375, 667), out, sources=srcs)
    finally:
        proc.terminate()
    hit = [g for g in out if re.search(want, g)]
    print('  self-test %-44s %s' % (what, ('caught: ' + hit[0][:80]) if hit else '*** MISSED ***' + (' (other: %s)' % out[0][:80] if out else '')))
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
    units = ['exempt'] + ['exit ' + g for g in GAMES] + ['fit %dx%d' % s for s in SIZES] + ['plant: ' + p[0] for p in PLANTS]
    if args.list_units:
        print('\n'.join(units))
        return 0
    mine = shard.pick(units)
    out = []
    ok = True
    proc, base = bc.start_stub_server()
    if 'exempt' in mine:
        with shard.unit('exempt'):
            for g in EXEMPT:
                src = read(os.path.join(ROOT, 'games', g, 'index.html'))
                if 'stage-exit' in src:
                    out.append('%s: is exempt by name but carries the stage-exit shell; take it out of EXEMPT' % g)
    try:
        for g in GAMES:
            if 'exit ' + g in mine:
                with shard.unit('exit ' + g):
                    exit_game(base, g, (375, 667), out)
                print('stage-exit: %s left from the worked example and a question, to the picker and the portal' % g)
        for s in SIZES:
            if 'fit %dx%d' % s in mine:
                with shard.unit('fit %dx%d' % s):
                    fit_size(base, s, out)
                print('stage-exit: both controls in view on all seven games at %dx%d' % s)
    finally:
        proc.terminate()
    for p in PLANTS:
        if 'plant: ' + p[0] in mine:
            with shard.unit('plant: ' + p[0]):
                ok = run_plant(p) and ok
    for f in out[:60]:
        print('FAIL  ' + f)
    if len(out) > 60:
        print('... and %d more' % (len(out) - 60))
    if out or not ok:
        print('stage-exit: FAILED')
        return 1
    print('stage-exit: OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
