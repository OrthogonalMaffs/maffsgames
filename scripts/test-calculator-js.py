#!/usr/bin/env python3
"""Self-tests for schools/assets/calculator.js (MaffsCalc, the shared on-screen calculator, canon §4.4).

Runs the real file in Chromium, with theme.css for its styles, and checks:
  Engine    arithmetic, order of operations (× and ÷ before + and −, left to right), x², √ (which
            opens a bracket, like a Casio), brackets (missing closing ones closed on =, extra ones an
            error), unary minus (−3² = −9), implicit multiplication (2(3), 2√(9)), and every error a
            calculator shows as "Error": divide by 0, √ of a negative, 1.2.3, a trailing operator.
  Display   10 significant figures with trailing zeros dropped: 0.1 + 0.2 shows 0.3, never
            0.30000000000000004; 1 ÷ 3 shows 0.3333333333; large and tiny values as a×10^n.
  Keys      sequences pressed on the real buttons: =, then an operator carries the answer on as
            "Ans", a digit starts afresh; DEL and C; √ deletes as one key; after an Error an
            operator starts afresh.
  Keyboard  typed keys drive it only while focus is inside the panel; typing in a page's own input
            never reaches it; Enter on a focused key presses that key, not =.
  Toggle    the panel starts closed, opens and closes, aria-expanded follows; Escape closes it.
  Privacy   nothing leaves the page: no request, no analytics call (window.mfg, gtag), no storage.
  Fit       at 320, 375 and 390px (a game card's padding around it): no key under 44x44px, the panel
            inside its card, the page never scrolls sideways.
  Dock      a game column 720px wide (a 688px card), mounted with {dock: card}: at 1280x720, 1366x768
            and 1920x1080 the open panel sits right of the card (never over it), inside the window,
            level with the card's top, keys at least 44px; opening and closing it never moves the card;
            scrolled 600px it stays in view (sticky). At 1240px and 390px it does not dock: it opens in
            the flow under its toggle. Five planted faults (no dock, not sticky, over the column, docking
            below the breakpoint, never docking) must each fail.
  Scientific (contract SCI-CALC, 9 Oct 2026) the engine's ^ (right-associative, tighter than a minus on its
            left), ln, log, e^, trig and its inverses in DEG and RAD, π and e, each exact to 10 s.f., and the
            errors (ln 0, log of a negative, sin⁻¹ 2, tan 90 in DEG); two planted engine faults (a
            left-associative ^, no tan 90 guard) must each fail. mount() without {keys} renders exactly
            the basic key set; mount(el, {keys: 'scientific'}) adds the scientific block, fits a touch phone
            at 320, 390 and 412px (48px keys, nothing sideways), and its DEG/RAD key switches the mode shown
            in the display and used by sin.
  Answer    (Jon, 4 Oct 2026) mounted with {answer: input}, on a touch phone (390x844 and 320x568), in
  target    Chromium AND WebKit: the answer box is read-only with inputmode="none"; a tap on it never
            focuses it (no system keyboard) and opens the keypad on it, marked by a heavier border and a
            "typing here" tag; the operators, brackets, x², √ and = are disabled, digits, the point, DEL
            and C type into the answer; a tap on the calculator display selects it (operators back, the
            answer untouched); the Calculator button moves into the panel as a close key; keys 48px tall,
            44px wide at least. With a mouse (1280x720, and 390px) nothing changes: the answer box is an
            ordinary input. Eight planted faults (Chromium) must each fail. WebKit cannot show a system
            keyboard either: what it confirms is the attributes and the focus behaviour, not the keyboard.

    python scripts/test-calculator-js.py
"""
import asyncio
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CALC_JS = os.path.join(ROOT, 'schools', 'assets', 'calculator.js')
KEYPAD_JS = os.path.join(ROOT, 'schools', 'assets', 'keypad.js')   # MaffsCalc's answer mode composes MaffsKeypad
THEME_CSS = os.path.join(ROOT, 'schools', 'assets', 'theme.css')
# theme.css imports calculator.css (the calculator and keypad styles, SCI-CALC); the tests drop @import
# lines (no network), so they add it themselves.
CALC_CSS = os.path.join(ROOT, 'schools', 'assets', 'calculator.css')

# (expression, expected display). ASCII forms: * / - ^2 sqrt( are the keys × ÷ − x² √(.
CASES = [
    ('2+3', '5'), ('7-10', '−3'), ('6*7', '42'), ('7/2', '3.5'), ('0', '0'),
    ('2+3*4', '14'), ('2*3+4', '10'), ('20-6/3', '18'), ('8/4/2', '1'), ('10-4-3', '3'),
    ('(2+3)*4', '20'), ('2*(3+4)', '14'), ('((1+2)*(3+4))', '21'),
    ('5^2', '25'), ('5^2+12^2', '169'), ('2*3^2', '18'), ('(2*3)^2', '36'), ('3^2^2', '81'),
    ('-3^2', '−9'), ('(-3)^2', '9'), ('--4', '4'), ('2*-3', '−6'), ('-2+5', '3'),
    ('sqrt(169)', '13'), ('sqrt(5^2+12^2)', '13'), ('sqrt(2)', '1.414213562'), ('sqrt(0)', '0'),
    ('sqrt(25-9', '4'), ('sqrt(7.5^2-4.5^2)', '6'), ('2sqrt(9)', '6'), ('2(3)', '6'), ('(2)(3)', '6'),
    ('(1+2', '3'), ('((4', '4'),
    ('0.1+0.2', '0.3'), ('1/3', '0.3333333333'), ('2/3', '0.6666666667'), ('0.1*3', '0.3'),
    ('1.1^2', '1.21'), ('sqrt(40)', '6.32455532'), ('1/3*3', '1'), ('.5+.5', '1'), ('5.+1', '6'),
    ('9999999999', '9999999999'), ('123456789*1000', '1.23456789×10^11'), ('99999999999*10', '1×10^12'),
    ('10^2^2^2^2', '1×10^16'), ('1/1000000000', '1×10^−9'), ('0.000001', '0.000001'), ('-10^2^2^2^2', '−1×10^16'),
    ('1-1', '0'), ('-0', '0'),
    # errors
    ('1/0', 'Error'), ('5/(3-3)', 'Error'), ('sqrt(-4)', 'Error'), ('1.2.3', 'Error'), ('3+', 'Error'),
    ('*3', 'Error'), ('(1+2))', 'Error'), (')(', 'Error'), ('', 'Error'), ('()', 'Error'), ('sqrt()', 'Error'),
    ('^2', 'Error'), ('.', 'Error'),
]

# (expression, angle mode, expected display): the scientific engine (contract SCI-CALC). ASCII: ^ is xʸ,
# asin( is sin⁻¹(, pi is π.
SCI_CASES = [
    ('1.05^10', 'deg', '1.628894627'), ('2^3^2', 'deg', '512'), ('-2^2', 'deg', '−4'), ('2^-1', 'deg', '0.5'),
    ('ln(e)', 'deg', '1'), ('log(1000)', 'deg', '3'), ('e^(ln(5))', 'deg', '5'), ('2pi', 'deg', '6.283185307'),
    ('3e^(1)', 'deg', '8.154845485'), ('sin(30)', 'deg', '0.5'), ('tan(45)', 'deg', '1'), ('asin(0.5)', 'deg', '30'),
    ('cos(180)', 'deg', '−1'), ('sin(180)', 'deg', '0'), ('acos(0)', 'deg', '90'), ('atan(1)', 'deg', '45'),
    ('sin(pi/6)', 'rad', '0.5'), ('asin(1)', 'rad', '1.570796327'), ('2^25', 'deg', '33554432'),
    ('ln(0)', 'deg', 'Error'), ('log(-1)', 'deg', 'Error'), ('asin(2)', 'deg', 'Error'), ('tan(90)', 'deg', 'Error'),
    ('tan(270)', 'deg', 'Error'), ('tan(pi/2)', 'rad', 'Error'), ('0^-1', 'deg', 'Error'), ('(-8)^(1/3)', 'deg', 'Error'),
]
# The basic panel, label for label, as it was before the scientific keys: mount() without {keys} must not change.
BASIC_LABELS = ['C', 'DEL', '(', ')', '÷', '7', '8', '9', '√', '×', '4', '5', '6', 'x²', '−',
                '1', '2', '3', '.', '+', '0', '=']
# Planted engine faults: each must make a SCI_CASES case fail.
SCI_PLANTS = [
    ('a left-associative ^', 'v = Math.pow(v, unary());',
     'v = Math.pow(v, primary()); while (peek() === POW) { i++; v = Math.pow(v, primary()); }'),
    ('no tan 90 guard', 'return k % 2 ? NaN : 0;', 'return Math.tan(x * Math.PI / 180);'),
]

# Sequences of button labels, and what the screen shows after them: [expression line, result line].
SEQS = [
    (['1', '2', '+', '5', '='], ['12+5 =', '17']),
    (['5', 'x²', '+', '1', '2', 'x²', '='], ['5²+12² =', '169']),
    (['√', '1', '6', '9', '='], ['√(169 =', '13']),
    (['√', '1', '6', '9', ')', '='], ['√(169) =', '13']),
    (['1', '÷', '3', '=', '×', '3', '='], ['Ans×3 =', '1']),          # Ans keeps full precision
    (['2', '+', '2', '=', '7'], ['7', '']),                              # a digit after = starts afresh
    (['2', '+', '2', '=', 'x²', '='], ['Ans² =', '16']),
    (['1', '2', '3', 'DEL', '='], ['12 =', '12']),
    (['√', 'DEL', '4', '='], ['4 =', '4']),                              # √( deletes as one key
    (['9', '9', 'C'], [' ', '0']),
    (['1', '÷', '0', '='], ['1÷0 =', 'Error']),
    (['1', '÷', '0', '=', '+', '2', '='], ['+2 =', '2']),                # after an Error, no Ans
    (['0', '.', '1', '+', '0', '.', '2', '='], ['0.1+0.2 =', '0.3']),
    (['(', '2', '+', '3', ')', '×', '4', '='], ['(2+3)×4 =', '20']),
    (['−', '3', 'x²', '='], ['−3² =', '−9']),
    (['3', '+', '4', '=', 'DEL', '='], ['3+4 =', '7']),
]

PAGE = """<!doctype html><html data-theme="light"><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{margin:0}.container{max-width:720px;width:100%;padding:.6rem;box-sizing:border-box}
.qcard{border:1px solid #ccc;border-radius:14px;padding:.75rem .7rem;box-sizing:border-box}*{box-sizing:border-box}</style></head>
<body><div class="container"><div class="qcard" id="card"><input id="answer" type="text"><div id="calc"></div></div></div></body></html>"""


# A game column like Just Pythag It, Bruv's: 720px wide with 1rem padding, so a 688px card.
DOCK_PAGE = """<!doctype html><html data-theme="light"><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>*{box-sizing:border-box}body{margin:0;display:flex;flex-direction:column;align-items:center}
.container{max-width:720px;width:100%;padding:1rem}.qcard{border:1px solid #ccc;border-radius:14px;padding:1rem;
display:flex;flex-direction:column;gap:.6rem;min-height:1600px}</style></head>
<body><div class="container"><div class="qcard" id="card"><input id="answer" type="text"><div id="calc"></div></div></div></body></html>"""

DOCK_SIZES = [(1280, 720, True), (1366, 768, True), (1920, 1080, True), (1240, 800, False), (390, 844, False)]

DOCK_FAULTS = [
    ("no dock (the panel stays in the flow)", "style", ".maffs-calc.docked .maffs-calc-rail{position:static!important}"),
    ("not sticky", "style", ".maffs-calc.docked .maffs-calc-panel{position:static!important}"),
    ("docked over the game column", "style", ".maffs-calc.docked .maffs-calc-rail{left:40%!important}"),
    ("docks below the breakpoint", "script", "MaffsCalc.DOCK.min = 100;"),
    ("never docks", "script", "MaffsCalc.DOCK.min = 5000;"),
]

DOCK_JS = """() => { const R = e => { const r = e.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom]; };
  const card = document.getElementById('card'), keys = [...document.querySelectorAll('.maffs-calc-key')].map(k => k.getBoundingClientRect());
  return { card: R(card), panel: R(document.querySelector('.maffs-calc-panel')), toggle: R(document.querySelector('.maffs-calc-toggle')),
    docked: __calc.isDocked(), open: __calc.isOpen(), cw: document.documentElement.clientWidth,
    sw: document.documentElement.scrollWidth, vh: innerHeight,
    key: [Math.min(...keys.map(k => k.width)), Math.min(...keys.map(k => k.height))] }; }"""


async def dock_check(browser, css, w, h, want, fault=None):
    """Failures for one window size (with a fault patched in, if given)."""
    out, at = [], '%dx%d' % (w, h)
    ctx = await browser.new_context(viewport={'width': w, 'height': h})
    await ctx.route('**/*', lambda r: r.abort())
    page = await ctx.new_page()
    await page.set_content(DOCK_PAGE)
    await page.add_style_tag(content=css)
    await page.add_script_tag(path=KEYPAD_JS)
    await page.add_script_tag(path=CALC_JS)
    if fault and fault[1] == 'style':
        await page.add_style_tag(content=fault[2])
    if fault and fault[1] == 'script':
        await page.evaluate(fault[2])
    await page.evaluate("window.__calc = MaffsCalc.mount(document.getElementById('calc'), {dock: document.getElementById('card')})")
    before = await page.evaluate(DOCK_JS)
    await page.evaluate("document.querySelector('.maffs-calc-toggle').click()")   # a click that does not scroll
    m = await page.evaluate(DOCK_JS)
    if m['docked'] != want:
        out.append('%s: docked=%s, expected %s' % (at, m['docked'], want))
    if any(abs(a - b) > 0.5 for a, b in zip(before['card'], m['card'])):
        out.append('%s: opening the calculator moved or resized the card: %r -> %r' % (at, before['card'], m['card']))
    if m['sw'] > m['cw']:
        out.append('%s: the page is %dpx wide in a %dpx window' % (at, m['sw'], m['cw']))
    if m['key'][0] < 44 or m['key'][1] < 44:
        out.append('%s: a key is %.1f x %.1f px, under 44' % (at, m['key'][0], m['key'][1]))
    if want:
        P, C = m['panel'], m['card']
        if P[0] < C[2] + 4:
            out.append('%s: the docked panel starts at x=%.0f, over or touching the card (right edge %.0f)' % (at, P[0], C[2]))
        if P[2] > m['cw']:
            out.append('%s: the docked panel ends at x=%.0f, past the window (%d)' % (at, P[2], m['cw']))
        if abs(P[1] - C[1]) > 2:
            out.append('%s: the docked panel top %.0f is not level with the card top %.0f' % (at, P[1], C[1]))
        await page.evaluate("window.scrollTo(0, 600)")
        s2 = await page.evaluate(DOCK_JS)
        if not (0 <= s2['panel'][1] <= 40 and s2['panel'][3] <= s2['vh']):
            out.append('%s: scrolled 600px, the panel is at y=%.0f..%.0f, not held in view' % (at, s2['panel'][1], s2['panel'][3]))
        await page.evaluate("window.scrollTo(0, 0)")
    else:
        if m['panel'][1] < m['toggle'][3] - 0.5 or m['panel'][0] < m['card'][0] or m['panel'][2] > m['card'][2]:
            out.append('%s: undocked, the panel is not in the flow under its toggle, inside the card' % at)
    await page.evaluate("document.querySelector('.maffs-calc-toggle').click()")
    m3 = await page.evaluate(DOCK_JS)
    if m3['open'] or any(abs(a - b) > 0.5 for a, b in zip(before['card'], m3['card'])):
        out.append('%s: closing did not close the panel, or moved the card' % at)
    await ctx.close()
    return out


OPS = ['(', ')', '÷', '√', '×', 'x²', '−', '+', '=']
ANSWER_JS = """() => { const a = document.getElementById('answer'), c = __calc, vis = e => !!e && e.offsetParent !== null;
  const keys = [...document.querySelectorAll('.maffs-calc-key')].map(k => k.getBoundingClientRect());
  return { mode: c.answerMode(), ro: a.readOnly, im: a.getAttribute('inputmode'), focused: document.activeElement === a,
    open: c.isOpen(), target: c.target(), selected: a.classList.contains('maffs-calc-selected'),
    cue: vis(document.querySelector('.maffs-calc-cue-answer')), screenSel: document.querySelector('.maffs-calc-screen').classList.contains('maffs-calc-selected'),
    screenCue: vis(document.querySelector('.maffs-calc-screen .maffs-calc-cue')),
    disabled: [...document.querySelectorAll('.maffs-calc-key:disabled')].map(k => k.textContent),
    toggle: vis(document.querySelector('.maffs-calc-toggle')), close: vis(document.querySelector('.maffs-calc-close')),
    keyH: Math.min(...keys.map(r => r.height)), keyW: Math.min(...keys.map(r => r.width)),
    value: a.value, result: c.display().result }; }"""

ANSWER_FAULTS = [
    ("answer box writable", "MaffsCalc.ANSWER.readOnly = false;"),
    ("no inputmode none", "MaffsCalc.ANSWER.inputmode = false;"),
    ("a tap focuses the answer box", "MaffsCalc.ANSWER.blur = false;"),
    ("operators live while typing the answer", "MaffsCalc.ANSWER.disableOps = false;"),
    ("keys go to the calculator", "MaffsCalc.ANSWER.route = false;"),
    ("no 'typing here' cue", "MaffsCalc.ANSWER.cue = false;"),
    ("answer target with a mouse", "MaffsCalc.ANSWER.query = 'all';"),
    ("phone keys under 48px", "STYLE:.maffs-calc.compact .maffs-calc-key{min-height:40px!important}"),
]


async def answer_check(browser, css, w, h, touch, fault=None):
    """Failures for the answer target at one size, touch or mouse (with a fault patched in, if given)."""
    at = '%s %dx%d %s' % (browser.browser_type.name, w, h, 'touch' if touch else 'mouse')
    try:
        return await _answer_check(browser, css, w, h, touch, fault, at)
    except Exception as exc:              # a step that cannot happen (a key never shown) is a failure too
        return ['%s: broke: %s' % (at, str(exc).splitlines()[0])]


async def _answer_check(browser, css, w, h, touch, fault, at):
    out = []
    ctx = await browser.new_context(viewport={'width': w, 'height': h}, has_touch=touch, is_mobile=touch)
    await ctx.route('**/*', lambda r: r.abort())
    page = await ctx.new_page()
    page.set_default_timeout(5000)
    await page.set_content(PAGE)
    await page.add_style_tag(content=css)
    await page.add_script_tag(path=KEYPAD_JS)
    await page.add_script_tag(path=CALC_JS)
    if fault and fault[1].startswith('STYLE:'):
        await page.add_style_tag(content=fault[1][6:])
    elif fault:
        await page.evaluate(fault[1])
    await page.evaluate("window.__calc = MaffsCalc.mount(document.getElementById('calc'), {answer: document.getElementById('answer')})")
    a = await page.evaluate(ANSWER_JS)
    if not touch:
        if a['mode'] or a['ro'] or a['im'] is not None:
            out.append('%s: with a mouse the answer box changed (keypad mode %s, readOnly %s, inputmode %r)' % (at, a['mode'], a['ro'], a['im']))
        await page.click('#answer')
        await page.keyboard.type('12.5')
        b = await page.evaluate(ANSWER_JS)
        if not b['focused'] or b['value'] != '12.5' or b['open']:
            out.append('%s: with a mouse the answer box is not an ordinary input (focused %s, value %r, keypad opened %s)'
                       % (at, b['focused'], b['value'], b['open']))
        await ctx.close()
        return out
    if not (a['mode'] and a['ro'] and a['im'] == 'none'):
        out.append('%s: the answer box could open the system keyboard (keypad mode %s, readOnly %s, inputmode %r)' % (at, a['mode'], a['ro'], a['im']))
    await page.tap('#answer')
    a = await page.evaluate(ANSWER_JS)
    if a['focused']:
        out.append('%s: a tap focused the answer box' % at)
    if not a['open'] or a['target'] != 'answer':
        out.append('%s: a tap on the answer box did not open the keypad on it (open %s, target %r)' % (at, a['open'], a['target']))
    if not (a['selected'] and a['cue']) or a['screenSel'] or a['screenCue']:
        out.append('%s: the answer box is not the one marked (border %s, tag %s; display marked %s/%s)'
                   % (at, a['selected'], a['cue'], a['screenSel'], a['screenCue']))
    if a['disabled'] != OPS:
        out.append('%s: typing the answer, the disabled keys are %r, expected %r' % (at, a['disabled'], OPS))
    if a['toggle'] or not a['close']:
        out.append('%s: the Calculator button is not inside the panel (button %s, close key %s)' % (at, a['toggle'], a['close']))
    if a['keyH'] < 47.5 or a['keyW'] < 44:
        out.append('%s: the smallest key is %.1f x %.1f px (want 48 tall, 44 wide)' % (at, a['keyW'], a['keyH']))
    for k in ['1', '2', '.', '5', 'DEL', '7']:
        await page.tap('.maffs-calc-key[data-act="del"]' if k == 'DEL' else '.maffs-calc-key[data-val="%s"]' % k)
    a = await page.evaluate(ANSWER_JS)
    if a['value'] != '12.7' or a['result'] != '0':
        out.append('%s: 1 2 . 5 DEL 7 gave answer %r, calculator %r (expected 12.7, 0)' % (at, a['value'], a['result']))
    await page.tap('.maffs-calc-key[data-act="clear"]')
    if (await page.evaluate(ANSWER_JS))['value'] != '':
        out.append('%s: C did not clear the answer' % at)
    await page.tap('.maffs-calc-lines')
    a = await page.evaluate(ANSWER_JS)
    if a['target'] != 'calc' or a['disabled'] or not (a['screenSel'] and a['screenCue']) or a['selected'] or a['cue']:
        out.append('%s: a tap on the display did not select it (target %r, disabled %r)' % (at, a['target'], a['disabled']))
    for k in ['3', '+', '4']:
        await page.tap('.maffs-calc-key[data-val="%s"]' % k)
    await page.tap('.maffs-calc-key[data-act="eq"]')
    a = await page.evaluate(ANSWER_JS)
    if a['result'] != '7' or a['value'] != '':
        out.append('%s: with the display selected 3 + 4 = gave calculator %r, answer %r' % (at, a['result'], a['value']))
    await page.tap('#answer')
    if (await page.evaluate(ANSWER_JS))['target'] != 'answer':
        out.append('%s: a second tap on the answer box did not select it' % at)
    await page.tap('.maffs-calc-close')
    a = await page.evaluate(ANSWER_JS)
    if a['open'] or not a['toggle']:
        out.append('%s: the close key did not close the panel and bring the Calculator button back' % at)
    await ctx.close()
    return out


async def run():
    from playwright.async_api import async_playwright
    fails = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        async def fresh(width=390, height=844):
            ctx = await browser.new_context(viewport={'width': width, 'height': height})
            reqs = []

            async def route(r):
                reqs.append(r.request.url)
                await r.abort()
            await ctx.route('**/*', route)
            page = await ctx.new_page()
            await page.set_content(PAGE)
            # theme.css less its Google Fonts @import (no network here; the fallback fonts are wider, the harder case)
            css = ''.join(l for l in open(THEME_CSS, encoding='utf-8').read().splitlines(True) if not l.startswith('@import')) + open(CALC_CSS, encoding='utf-8').read()
            await page.add_style_tag(content=css)
            await page.add_script_tag(path=KEYPAD_JS)
            await page.add_script_tag(path=CALC_JS)
            await page.evaluate("""() => { window.__mfg = []; window.mfg = function () { window.__mfg.push([...arguments]); };
              window.gtag = function () { window.__mfg.push(['gtag', ...arguments]); };
              window.__store = 0; Storage.prototype.setItem = function () { window.__store++; };
              window.__calc = MaffsCalc.mount(document.getElementById('calc')); }""")
            reqs.clear()                      # the theme's font @import is not the calculator's doing
            return ctx, page, reqs

        ctx, page, reqs = await fresh()
        # Engine and display
        got = await page.evaluate("cs => cs.map(c => MaffsCalc.calc(c[0]))", CASES)
        for (expr, want), g in zip(CASES, got):
            if g != want:
                fails.append('calc(%r): shows %r, expected %r' % (expr, g, want))
        if await page.evaluate("MaffsCalc.format(0.1 + 0.2)") != '0.3':
            fails.append('format(0.1 + 0.2) is not 0.3')
        if await page.evaluate("MaffsCalc.evaluate('2+3*4')") != 14:
            fails.append('evaluate() does not return a number')
        # Scientific engine
        got = await page.evaluate("cs => cs.map(c => MaffsCalc.calc(c[0], null, c[1]))", SCI_CASES)
        for (expr, mode, want), g in zip(SCI_CASES, got):
            if g != want:
                fails.append('calc(%r, %s): shows %r, expected %r' % (expr, mode, g, want))
        labels = await page.evaluate("[...document.querySelectorAll('#calc .maffs-calc-key')].map(k => k.textContent)")
        if labels != BASIC_LABELS:
            fails.append('mount() without {keys}: the basic panel changed: %r' % labels)
        # Planted engine faults, each in its own copy of calculator.js
        src = open(CALC_JS, encoding='utf-8').read()
        for name, old, new in SCI_PLANTS:
            if src.count(old) != 1:
                fails.append('scientific plant %r: its line is no longer in calculator.js' % name)
                continue
            pg = await ctx.new_page()
            await pg.set_content('<html><body></body></html>')
            await pg.add_script_tag(content=src.replace(old, new))
            pgot = await pg.evaluate("cs => cs.map(c => MaffsCalc.calc(c[0], null, c[1]))", SCI_CASES)
            bad = [c[0] for c, g in zip(SCI_CASES, pgot) if g != c[2]]
            print('  scientific fault %-28s %s' % (name, ('caught (%s)' % ', '.join(bad[:3])) if bad else 'NOT CAUGHT'))
            if not bad:
                fails.append('scientific plant not caught: ' + name)
            await pg.close()
        # Toggle
        st = await page.evaluate("""() => { const t = document.querySelector('.maffs-calc-toggle'),
            p = document.querySelector('.maffs-calc-panel'); const a = [p.hidden, t.getAttribute('aria-expanded')];
            t.click(); a.push(p.hidden, t.getAttribute('aria-expanded'), document.activeElement === p);
            t.click(); a.push(p.hidden, t.getAttribute('aria-expanded')); return a; }""")
        if st != [True, 'false', False, 'true', True, True, 'false']:
            fails.append('toggle: [hidden, aria-expanded, ...] went %r' % st)
        # Key sequences on the real buttons
        await page.click('.maffs-calc-toggle')
        for keys, want in SEQS:
            await page.click('.maffs-calc-key[data-act="clear"]')
            for k in keys:
                await page.click('.maffs-calc-key >> text="%s"' % k if k not in ('(', ')', '.') else
                                 '.maffs-calc-key[data-val="%s"]' % k)
            d = await page.evaluate("(() => { const d = __calc.display(); return [d.expr, d.result]; })()")
            if d != want:
                fails.append('keys %s: screen shows %r, expected %r' % (' '.join(keys), d, want))
        # Physical keyboard: only with focus inside the panel
        await page.click('.maffs-calc-key[data-act="clear"]')
        await page.focus('.maffs-calc-panel')
        await page.keyboard.type('3*(4+5)')
        await page.keyboard.press('Enter')
        d = await page.evaluate("__calc.display().result")
        if d != '27':
            fails.append('typed 3*(4+5) Enter: shows %r, expected 27' % d)
        await page.keyboard.type('^')
        await page.keyboard.press('Enter')
        if await page.evaluate("__calc.display().result") != '729':
            fails.append('typed ^ Enter after 27: expected 729 (Ans²)')
        await page.keyboard.press('Delete')
        await page.keyboard.type('12')
        await page.keyboard.press('Backspace')
        await page.keyboard.type('r16')
        await page.keyboard.press('Enter')
        d = await page.evaluate("(() => { const d = __calc.display(); return [d.expr, d.result]; })()")
        if d != ['1√(16 =', '4']:
            fails.append('typed Delete 12 Backspace r16 Enter: shows %r' % d)
        await page.focus('.maffs-calc-key[data-val="7"]')
        await page.keyboard.press('Delete')
        await page.keyboard.press('Enter')
        d = await page.evaluate("__calc.display()")
        if d['expr'] != '7' or d['result'] != '':
            fails.append('Enter on the focused 7 key gave %r, expected the key pressed (7), not =' % d)
        await page.keyboard.press('Delete')
        await page.focus('#answer')
        await page.keyboard.type('12.5')
        await page.keyboard.press('Enter')
        d = await page.evaluate("[__calc.display().expr, document.getElementById('answer').value]")
        if d != [' ', '12.5']:
            fails.append('typing in the page\'s own input reached the calculator, or was taken: %r' % d)
        await page.focus('.maffs-calc-panel')
        await page.keyboard.press('Escape')
        if await page.evaluate("[__calc.isOpen(), document.activeElement.className]") != [False, 'maffs-calc-toggle']:
            fails.append('Escape does not close the panel and return focus to the toggle')
        # Privacy
        if reqs:
            fails.append('the calculator made requests: %r' % reqs[:3])
        if await page.evaluate("window.__mfg.length"):
            fails.append('the calculator called analytics: %r' % await page.evaluate("window.__mfg"))
        if await page.evaluate("window.__store"):
            fails.append('the calculator wrote to storage')
        await ctx.close()

        # Fit at phone widths
        for w in (320, 375, 390):
            ctx, page, _ = await fresh(w, 640)
            await page.click('.maffs-calc-toggle')
            m = await page.evaluate("""() => { const keys = [...document.querySelectorAll('.maffs-calc-key')].map(k => k.getBoundingClientRect());
                const p = document.querySelector('.maffs-calc-panel').getBoundingClientRect(),
                      c = document.getElementById('card').getBoundingClientRect();
                return { minW: Math.min(...keys.map(r => r.width)), minH: Math.min(...keys.map(r => r.height)),
                  inside: p.left >= c.left - 0.5 && p.right <= c.right + 0.5,
                  scroll: document.documentElement.scrollWidth, inner: innerWidth,
                  overflow: [...document.querySelectorAll('.maffs-calc-key')].filter(k => k.scrollWidth > k.clientWidth).length }; }""")
            if m['minW'] < 44 or m['minH'] < 44:
                fails.append('%dpx: smallest key %.1f x %.1f px, under 44' % (w, m['minW'], m['minH']))
            if not m['inside']:
                fails.append('%dpx: the panel spills out of its card' % w)
            if m['scroll'] > m['inner']:
                fails.append('%dpx: the page is %dpx wide' % (w, m['scroll']))
            if m['overflow']:
                fails.append('%dpx: %d key labels overflow their key' % (w, m['overflow']))
            await ctx.close()
        # The wide-screen dock, and each planted fault must fail somewhere
        css = ''.join(l for l in open(THEME_CSS, encoding='utf-8').read().splitlines(True) if not l.startswith('@import')) + open(CALC_CSS, encoding='utf-8').read()
        for w, h, want in DOCK_SIZES:
            fails.extend(await dock_check(browser, css, w, h, want))
        # The answer target: Chromium and WebKit, touch phones and mouse
        from playwright.async_api import async_playwright as _ap   # noqa: F401 (same session)
        engines = [browser]
        try:
            engines.append(await p.webkit.launch())
        except Exception as exc:
            fails.append('WebKit would not start (answer-box checks need it): %s' % str(exc).splitlines()[0])
        for eng in engines:
            for w, h, touch in [(390, 844, True), (320, 568, True), (1280, 720, False), (390, 844, False)]:
                fails.extend(await answer_check(eng, css, w, h, touch))
        for fault in ANSWER_FAULTS:
            caught = []
            for w, h, touch in [(390, 844, True), (1280, 720, False)]:
                caught.extend(await answer_check(browser, css, w, h, touch, fault))
            print('  fault %-40s %s' % (fault[0], ('caught (%s)' % caught[0][:70]) if caught else '*** MISSED ***'))
            if not caught:
                fails.append('planted fault not caught: ' + fault[0])
        for eng in engines[1:]:
            await eng.close()
        for fault in DOCK_FAULTS:
            caught = []
            for w, h, want in DOCK_SIZES:
                caught.extend(await dock_check(browser, css, w, h, want, fault))
            print('  fault %-40s %s' % (fault[0], ('caught (%s)' % caught[0][:70]) if caught else '*** MISSED ***'))
            if not caught:
                fails.append('planted fault not caught: ' + fault[0])
        # The scientific panel: a touch phone at 320, 390 and 412px; at 390 the keys themselves
        css = ''.join(l for l in open(THEME_CSS, encoding='utf-8').read().splitlines(True) if not l.startswith('@import')) + open(CALC_CSS, encoding='utf-8').read()
        for w in (320, 390, 412):
            sctx = await browser.new_context(viewport={'width': w, 'height': 844}, has_touch=True, is_mobile=True)
            await sctx.route('**/*', lambda r: r.abort())
            sp = await sctx.new_page()
            await sp.set_content(PAGE)
            await sp.add_style_tag(content=css)
            await sp.add_script_tag(path=KEYPAD_JS)
            await sp.add_script_tag(path=CALC_JS)
            st = await sp.evaluate('''() => { window.__s = MaffsCalc.mount(document.getElementById('calc'), {keys: 'scientific'});
                __s.open(); const ks = [...document.querySelectorAll('.maffs-calc-key')].map(k => k.getBoundingClientRect());
                const p = document.querySelector('.maffs-calc-panel').getBoundingClientRect();
                return { n: ks.length, sci: document.querySelectorAll('.maffs-calc-sci .maffs-calc-key').length,
                  w: Math.min(...ks.map(k => k.width)), h: Math.min(...ks.map(k => k.height)), right: p.right,
                  sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth,
                  compact: __s.isCompact(), mode: document.querySelector('.maffs-calc-mode').textContent }; }''')
            if st['sci'] != 13 or st['n'] != 35:
                fails.append('scientific panel at %dpx: %d keys, %d scientific (expected 35, 13)' % (w, st['n'], st['sci']))
            if st['w'] < 44 or st['h'] < 48 or not st['compact']:
                fails.append('scientific panel at %dpx: smallest key %.0fx%.0f (want 44x48, compact %s)'
                             % (w, st['w'], st['h'], st['compact']))
            if st['sw'] > st['cw'] or st['right'] > st['cw']:
                fails.append('scientific panel at %dpx: the page scrolls sideways (%d > %d) or the panel overflows'
                             % (w, st['sw'], st['cw']))
            if st['mode'] != 'DEG':
                fails.append('scientific panel: starts in %r, expected DEG' % st['mode'])
            if w == 390:
                seq = await sp.evaluate('''() => { const r = [], P = k => __s.press(k);
                    ['sin', '3', '0', '='].forEach(P); r.push(__s.display().result);
                    P('DEG'); r.push(__s.mode(), document.querySelector('.maffs-calc-mode').textContent);
                    ['C', 'sin', 'π', '÷', '6', '='].forEach(P); r.push(__s.display().result, __s.display().expr);
                    ['C', '1', '.', '0', '5', 'xʸ', '1', '0', '='].forEach(P); r.push(__s.display().result);
                    ['C', 'ln', 'DEL'].forEach(P); r.push(__s.display().expr); return r; }''')
                want = ['0.5', 'rad', 'RAD', '0.5', 'sin(π÷6 =', '1.628894627', '\xa0']
                if seq != want:
                    fails.append('scientific keys (sin 30, RAD, sin(π÷6), 1.05ʸ10, ln DEL) went %r, expected %r' % (seq, want))
            await sctx.close()
        await browser.close()
    return fails


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    fails = asyncio.run(run())
    for f in fails:
        print('FAIL    ' + f)
    if fails:
        print('\nFAILED: %d problem(s)' % len(fails))
        return 1
    print('PASS: %d expressions (arithmetic, precedence, x², √, brackets, errors, 10 s.f. display); '
          '%d scientific expressions (^, ln, log, e^, trig DEG/RAD, π, e, errors), %d scientific plants caught, '
          'basic panel unchanged, scientific panel fits 320/390/412px; '
          '%d key sequences; keyboard, toggle, privacy; keys >= 44px at 320/375/390px; docked beside a 720px '
          'column at 1280/1366/1920 (sticky, never over it), in the flow at 1240 and 390; %d planted dock faults caught; '
          'answer target on touch phones in Chromium and WebKit (read-only, inputmode none, never focused, '
          'operators disabled, display switching, 48px keys), unchanged with a mouse; %d planted answer faults caught'
          % (len(CASES), len(SCI_CASES), len(SCI_PLANTS), len(SEQS), len(DOCK_FAULTS), len(ANSWER_FAULTS)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
