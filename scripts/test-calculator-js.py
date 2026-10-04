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

    python scripts/test-calculator-js.py
"""
import asyncio
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CALC_JS = os.path.join(ROOT, 'schools', 'assets', 'calculator.js')
THEME_CSS = os.path.join(ROOT, 'schools', 'assets', 'theme.css')

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
            css = ''.join(l for l in open(THEME_CSS, encoding='utf-8').read().splitlines(True) if not l.startswith('@import'))
            await page.add_style_tag(content=css)
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
          '%d key sequences; keyboard, toggle, privacy; keys >= 44px at 320/375/390px' % (len(CASES), len(SEQS)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
