#!/usr/bin/env python3
"""Self-tests for schools/assets/keypad.js (MaffsKeypad, the phone keypad for typed answers, canon §4.4).

Runs the real file in Chromium, with theme.css for its styles, on a test page holding 1, 2 and 4
answer boxes in a row (the shape of a "round each number" step), and checks:

  Touch     at 320x568, 375x667 and 390x844 (touch, mobile): every box is read-only with
            inputmode="none" and the keys are shown, at least 44px wide and 48px tall; the first box
            is active to begin with; a tap on a box makes it the only one marked (a heavier border and
            the "typing here" tag, the tag inside the window and over no other box); each box receives
            only the keys typed while it was active; DEL and C act on the active box only; every key
            fires an "input" event on its own box; a box takes 12 characters at most; nothing editable
            is ever focused (so no system keyboard opens); the page never scrolls sideways; a tap on a
            box below the fold brings the box and the keys into the window together.
  Minus     a mount with {keys: {minus: true}}: the minus key types "-" into an empty box only; a
            mount without it has no minus key.
  Mouse     at 1280x720 and 390x844 with no touch: no keys are drawn; the boxes are ordinary text
            inputs (not read-only, inputmode="decimal") that take focus and typing.
  Privacy   nothing leaves the page: no request, no analytics call, no storage.
  Faults    six planted faults must each fail: a key leaking to the wrong box, a tap focusing a box,
            no mark on the active box, the length limit ignored, keys drawn with a mouse, phone keys
            under 48px.

    python scripts/check-keypad.py               # the checks and the planted faults
    python scripts/check-keypad.py --shots DIR   # also save screenshots (4 boxes, each width)
"""
import argparse
import asyncio
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYPAD_JS = os.path.join(ROOT, 'schools', 'assets', 'keypad.js')
THEME_CSS = os.path.join(ROOT, 'schools', 'assets', 'theme.css')
TOUCH = [(320, 568), (375, 667), (390, 844)]
MOUSE = [(1280, 720), (390, 844)]
COUNTS = [1, 2, 4]


def page_html(n, spacer=0):
    """A game card with n answer boxes in a row and a keypad under them (spacer px above, for the fold)."""
    boxes = ''.join('<label class="cell"><span>%s</span><input id="t%d" type="text" aria-label="Box %d"></label>'
                    % ('abcd'[i], i, i + 1) for i in range(n))
    return ("""<!doctype html><html data-theme="light"><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>*{box-sizing:border-box}body{margin:0}.container{max-width:720px;width:100%%;padding:.6rem}
.qcard{border:1px solid #ccc;border-radius:14px;padding:.75rem .7rem;display:flex;flex-direction:column;gap:.6rem;align-items:center}
.row{display:flex;gap:.5rem;width:100%%}.cell{flex:1 1 0;min-width:0;display:flex;flex-direction:column;gap:.2rem}
.cell input{width:100%%;font:inherit;font-size:1.1rem;padding:.5rem;border:2px solid #999;border-radius:8px}
.spacer{height:%dpx}</style></head>
<body><div class="container"><div class="qcard" id="card"><div class="spacer"></div><p>Round each number to 1 significant figure.</p>
<div class="row" id="row">%s</div><div id="keypad"></div></div></div></body></html>""" % (spacer, boxes))


STATE_JS = """() => { const ts = [...document.querySelectorAll('.row input')], vis = e => !!e && e.offsetParent !== null;
  const R = e => { const r = e.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom]; };
  const keys = [...document.querySelectorAll('.maffs-keypad-key')].filter(vis).map(k => k.getBoundingClientRect());
  const ae = document.activeElement;
  return { values: ts.map(t => t.value), ro: ts.map(t => t.readOnly), im: ts.map(t => t.getAttribute('inputmode')),
    marked: ts.map(t => t.classList.contains('maffs-keypad-selected')),
    cues: [...document.querySelectorAll('.maffs-keypad-cue-answer')].map(c => vis(c) ? R(c) : null),
    boxes: ts.map(R), active: __kp.active(), keys: keys.length, shown: vis(document.querySelector('.maffs-keypad-panel')),
    keyW: keys.length ? Math.min(...keys.map(r => r.width)) : 0, keyH: keys.length ? Math.min(...keys.map(r => r.height)) : 0,
    panel: vis(document.querySelector('.maffs-keypad-panel')) ? R(document.querySelector('.maffs-keypad-panel')) : null,
    editable: !!ae && (ae.tagName === 'INPUT' || ae.tagName === 'TEXTAREA' || ae.isContentEditable),
    inputs: window.__inp, sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth,
    vh: innerHeight, vw: innerWidth }; }"""

FAULTS = [
    ("a key leaks to the wrong box", 'src', 'typeInto(targets[active], act, val, max)', 'typeInto(targets[0], act, val, max)'),
    ("a tap focuses a box", 'js', 'MaffsKeypad.CONFIG.blur = false;'),
    ("the active box is not marked", 'js', 'MaffsKeypad.CONFIG.cue = false;'),
    ("the length limit ignored", 'src', 'v.length < max', 'true'),
    ("keys drawn with a mouse", 'js', "MaffsKeypad.CONFIG.query = 'all';"),
    ("phone keys under 48px", 'css', '.maffs-keypad-key{min-height:40px!important}'),
]


def theme_css():
    # theme.css less its Google Fonts @import (no network here; the fallback fonts are wider, the harder case)
    return ''.join(l for l in open(THEME_CSS, encoding='utf-8').read().splitlines(True) if not l.startswith('@import'))


def keypad_src(fault):
    src = open(KEYPAD_JS, encoding='utf-8').read()
    if fault and fault[1] == 'src':
        if fault[2] not in src:
            raise SystemExit('check-keypad: the planted fault %r no longer matches keypad.js; update FAULTS' % fault[0])
        src = src.replace(fault[2], fault[3])
    return src


async def open_page(browser, w, h, touch, n, fault=None, minus=False, spacer=0, keep=False):
    ctx = await browser.new_context(viewport={'width': w, 'height': h}, has_touch=touch, is_mobile=touch)
    reqs = []

    async def route(r):
        reqs.append(r.request.url)
        await r.abort()
    await ctx.route('**/*', route)
    page = await ctx.new_page()
    page.set_default_timeout(5000)
    await page.set_content(page_html(n, spacer))
    await page.add_style_tag(content=theme_css())
    if fault and fault[1] == 'css':
        await page.add_style_tag(content=fault[2])
    await page.add_script_tag(content=keypad_src(fault))
    if fault and fault[1] == 'js':
        await page.evaluate(fault[2])
    await page.evaluate("""([minus, keep]) => { window.__mfg = []; window.mfg = function () { window.__mfg.push([...arguments]); };
      window.gtag = function () { window.__mfg.push(['gtag', ...arguments]); };
      window.__store = 0; Storage.prototype.setItem = function () { window.__store++; };
      const ts = [...document.querySelectorAll('.row input')];
      window.__inp = ts.map(() => 0);
      ts.forEach((t, i) => t.addEventListener('input', () => window.__inp[i]++));
      window.__kp = MaffsKeypad.mount(document.getElementById('keypad'), { targets: ts,
        keys: minus ? { minus: true } : undefined, keepInView: keep ? document.getElementById('row') : undefined }); }""",
                        [minus, keep])
    reqs.clear()
    return ctx, page, reqs


def key_sel(k):
    if k == 'DEL':
        return '.maffs-keypad-key[data-act="del"]'
    if k == 'C':
        return '.maffs-keypad-key[data-act="clear"]'
    if k == '-':
        return '.maffs-keypad-key[data-act="minus"]'
    return '.maffs-keypad-key[data-val="%s"]' % k


def overlaps(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


async def touch_check(browser, w, h, n, fault=None, shots=None):
    at = 'touch %dx%d, %d box%s' % (w, h, n, '' if n == 1 else 'es')
    try:
        return await _touch_check(browser, w, h, n, fault, shots, at)
    except Exception as exc:              # a step that cannot happen (a key never shown) is a failure too
        return ['%s: broke: %s' % (at, str(exc).splitlines()[0])]


async def _touch_check(browser, w, h, n, fault, shots, at):
    out = []
    ctx, page, reqs = await open_page(browser, w, h, True, n, fault)
    focused = []

    async def state():
        s = await page.evaluate(STATE_JS)
        if s['editable']:
            focused.append(1)
        return s

    def marked_only(s, i, when):
        if s['active'] != i:
            out.append('%s: %s, the active box is %d, expected %d' % (at, when, s['active'], i))
        want = [k == i for k in range(n)]
        cues = [c is not None for c in s['cues']]
        if s['marked'] != want or cues != want:
            out.append('%s: %s, marked boxes %r and tags %r, expected only box %d' % (at, when, s['marked'], cues, i))
            return
        c = s['cues'][i]
        if c[0] < 0 or c[1] < 0 or c[2] > s['vw'] or c[3] > s['vh']:
            out.append('%s: %s, the "typing here" tag is outside the window: %r' % (at, when, c))
        for k, b in enumerate(s['boxes']):
            if k != i and overlaps(c, b):
                out.append('%s: %s, the tag on box %d lies over box %d' % (at, when, i, k))

    s = await state()
    if not all(s['ro']) or any(im != 'none' for im in s['im']):
        out.append('%s: a box could open the system keyboard (readOnly %r, inputmode %r)' % (at, s['ro'], s['im']))
    if not s['shown'] or s['keys'] != 13:
        out.append('%s: the keypad is not shown with its 13 keys (shown %s, %d keys)' % (at, s['shown'], s['keys']))
    if s['keyW'] < 44 or s['keyH'] < 47.5:
        out.append('%s: the smallest key is %.1f x %.1f px (want 44 wide, 48 tall)' % (at, s['keyW'], s['keyH']))
    marked_only(s, 0, 'on load')
    # Each box gets its own keys: box i takes (i+1)(i+1).5
    for i in range(n):
        await page.tap('#t%d' % i)
        s = await state()
        marked_only(s, i, 'after a tap on box %d' % i)
        for k in [str(i + 1), str(i + 1), '.', '5']:
            await page.tap(key_sel(k))
    s = await state()
    want = ['%d%d.5' % (i + 1, i + 1) for i in range(n)]
    if s['values'] != want:
        out.append('%s: after typing into each box in turn the boxes hold %r, expected %r' % (at, s['values'], want))
    if s['inputs'] != [4] * n:
        out.append('%s: input events per box %r, expected 4 each' % (at, s['inputs']))
    if shots and fault is None and n == 4:
        await page.tap('#t1')
        await page.screenshot(path=os.path.join(shots, 'keypad-%dx%d-4-boxes.png' % (w, h)))
    # DEL and C on the active box only
    last = n - 1
    await page.tap('#t%d' % last)
    await page.tap(key_sel('DEL'))
    s = await state()
    want[last] = want[last][:-1]
    if s['values'] != want:
        out.append('%s: DEL on box %d left %r, expected %r' % (at, last, s['values'], want))
    await page.tap('#t0')
    await page.tap(key_sel('C'))
    s = await state()
    want[0] = ''
    if s['values'] != want:
        out.append('%s: C on box 0 left %r, expected %r' % (at, s['values'], want))
    # The length limit
    for _ in range(15):
        await page.tap(key_sel('9'))
    s = await state()
    if len(s['values'][0]) != 12:
        out.append('%s: 15 key presses put %d characters in a box (limit 12)' % (at, len(s['values'][0])))
    if s['sw'] > s['cw']:
        out.append('%s: the page is %dpx wide in a %dpx window' % (at, s['sw'], s['cw']))
    if '-' in ''.join(s['values']) or await page.locator(key_sel('-')).count():
        out.append('%s: a mount without {keys: {minus: true}} has a minus key' % at)
    if focused:
        out.append('%s: an editable element took focus during %d of the taps (the system keyboard would open)' % (at, len(focused)))
    if reqs or await page.evaluate("window.__mfg.length + window.__store"):
        out.append('%s: the keypad sent a request, called analytics or wrote to storage' % at)
    await ctx.close()
    return out


async def fold_check(browser, w, h):
    """A box well below the fold: a tap brings the row and the keys into the window together."""
    at = 'touch %dx%d, below the fold' % (w, h)
    ctx, page, _ = await open_page(browser, w, h, True, 2, spacer=h, keep=True)
    out = []
    await page.evaluate("document.getElementById('t1').scrollIntoView({block: 'start'})")
    await page.tap('#t1')
    m = await page.evaluate("""() => { const r = document.getElementById('row').getBoundingClientRect(),
        p = document.querySelector('.maffs-keypad-panel').getBoundingClientRect(); return [r.top, p.bottom, innerHeight]; }""")
    if m[0] < 0 or m[1] > m[2]:
        out.append('%s: after the tap the row starts at y=%.0f and the keys end at y=%.0f in a %d-tall window' % (at, m[0], m[1], m[2]))
    await ctx.close()
    return out


async def minus_check(browser):
    ctx, page, _ = await open_page(browser, 390, 844, True, 2, minus=True)
    out = []
    await page.tap('#t0')
    await page.tap(key_sel('-'))
    await page.tap(key_sel('5'))
    await page.tap(key_sel('-'))
    await page.tap('#t1')
    await page.tap(key_sel('5'))
    await page.tap(key_sel('-'))
    v = await page.evaluate("[...document.querySelectorAll('.row input')].map(t => t.value)")
    if v != ['-5', '5']:
        out.append('minus key: boxes hold %r, expected ["-5", "5"] (minus types only into an empty box)' % v)
    n = await page.evaluate("document.querySelectorAll('.maffs-keypad-key').length")
    if n != 14:
        out.append('minus key: %d keys drawn, expected 14' % n)
    await ctx.close()
    return out


async def mouse_check(browser, w, h, fault=None):
    at = 'mouse %dx%d' % (w, h)
    out = []
    ctx, page, _ = await open_page(browser, w, h, False, 2, fault)
    s = await page.evaluate(STATE_JS)
    if s['shown'] or s['keys']:
        out.append('%s: keys are drawn with a mouse' % at)
    if any(s['ro']) or s['im'] != ['decimal', 'decimal'] or any(s['marked']):
        out.append('%s: the boxes are not ordinary inputs (readOnly %r, inputmode %r, marked %r)' % (at, s['ro'], s['im'], s['marked']))
    await page.click('#t1')
    await page.keyboard.type('4.5')
    v = await page.evaluate("[document.activeElement.id, [...document.querySelectorAll('.row input')].map(t => t.value)]")
    if v != ['t1', ['', '4.5']]:
        out.append('%s: a click and typing did not reach the box as an ordinary input: %r' % (at, v))
    await ctx.close()
    return out


async def run(shots):
    from playwright.async_api import async_playwright
    fails = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for w, h in TOUCH:
            for n in COUNTS:
                fails.extend(await touch_check(browser, w, h, n, shots=shots))
            fails.extend(await fold_check(browser, w, h))
        fails.extend(await minus_check(browser))
        for w, h in MOUSE:
            fails.extend(await mouse_check(browser, w, h))
        for fault in FAULTS:
            caught = []
            for n in (1, 2):
                caught.extend(await touch_check(browser, 320, 568, n, fault))
            caught.extend(await mouse_check(browser, 1280, 720, fault))
            print('  fault %-34s %s' % (fault[0], ('caught (%s)' % caught[0][:80]) if caught else '*** MISSED ***'))
            if not caught:
                fails.append('planted fault not caught: ' + fault[0])
        await browser.close()
    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--shots', help='save screenshots of the 4-box page at each phone width here')
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    if args.shots:
        os.makedirs(args.shots, exist_ok=True)
    fails = asyncio.run(run(args.shots))
    for f in fails:
        print('FAIL    ' + f)
    if fails:
        print('\nFAILED: %d problem(s)' % len(fails))
        return 1
    print('PASS: MaffsKeypad on touch phones at %s with %s boxes (read-only, inputmode none, never focused, '
          'one box marked, keys to the active box only, DEL and C on it alone, 12-character limit, keys 48px, '
          'no sideways scroll, box and keys in view together); the minus key; ordinary inputs with a mouse; '
          'nothing sent; %d planted faults caught'
          % ('/'.join(str(w) for w, _ in TOUCH), '/'.join(str(n) for n in COUNTS), len(FAULTS)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
