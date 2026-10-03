#!/usr/bin/env python3
"""Self-tests for schools/assets/answer.js (MaffsAnswer, canon §7.1.3).

Runs the real file in Chromium and checks every outcome of every function: correct, wrong,
format and unreadable for money(), decimal() and exact(), the accepted £/€ prefix, parse(),
and the words message() returns. Then an equivalence check: on every string a type="number"
input can hand a game (signs, leading dots, trailing dots, exponents, 0-4 decimal places) and
a spread of keys, money() returns exactly what tax-theft's old moneyResult() returned. That is
the proof that moving tax-theft onto the helper changes nothing it marks.

    python scripts/test-answer-js.py
"""
import asyncio
import itertools
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANSWER_JS = os.path.join(ROOT, 'schools', 'assets', 'answer.js')

# (call, expected)
CASES = [
    # money: pence key
    ("money('1250.70', 1250.7)", 'correct'),
    ("money('£1250.70', 1250.7)", 'correct'),
    ("money('€12.34', 12.34)", 'correct'),
    ("money(' £ 12.34 ', 12.34)", 'correct'),
    ("money('1250.7', 1250.7)", 'format'),
    ("money('1250.700', 1250.7)", 'format'),
    ("money('£1250.7', 1250.7)", 'format'),
    ("money('1250.71', 1250.7)", 'wrong'),
    ("money('12.30', 12.34)", 'wrong'),
    ("money('12.38', 12.34)", 'wrong'),
    ("money('12.33', 12.34)", 'wrong'),
    # money: whole-pound key
    ("money('3050', 3050)", 'correct'),
    ("money('3050.00', 3050)", 'correct'),
    ("money('£3050', 3050)", 'correct'),
    ("money('3050.0', 3050)", 'format'),
    ("money('3050.000', 3050)", 'format'),
    ("money('3051', 3050)", 'wrong'),
    ("money('3049.99', 3050)", 'wrong'),
    # money: unreadable
    ("money('', 5)", 'unreadable'),
    ("money('   ', 5)", 'unreadable'),
    ("money('£', 5)", 'unreadable'),
    ("money('12abc', 12)", 'unreadable'),
    ("money('1,250.70', 1250.7)", 'unreadable'),
    ("money('$12.34', 12.34)", 'unreadable'),
    ("money('££12.34', 12.34)", 'unreadable'),
    # decimal, 1 d.p.
    ("decimal('333.3', 333.3, 1)", 'correct'),
    ("decimal('333.30', 333.3, 1)", 'correct'),
    ("decimal('2.5', 2.5, 1)", 'correct'),
    ("decimal('2.50', 2.5, 1)", 'correct'),
    ("decimal('500', 500, 1)", 'correct'),
    ("decimal('500.0', 500, 1)", 'correct'),
    ("decimal('333.33', 333.3, 1)", 'format'),
    ("decimal('333.333333', 333.3, 1)", 'format'),
    ("decimal('16.66', 16.7, 1)", 'format'),
    ("decimal('16.65', 16.7, 1)", 'format'),
    ("decimal('16.649', 16.7, 1)", 'wrong'),
    ("decimal('333.4', 333.3, 1)", 'wrong'),
    ("decimal('333.2', 333.3, 1)", 'wrong'),
    ("decimal('333', 333.3, 1)", 'wrong'),
    ("decimal('2.4', 2.5, 1)", 'wrong'),
    ("decimal('0.05', 0.1, 1)", 'format'),
    ("decimal('0.04', 0.1, 1)", 'wrong'),
    ("decimal('-2.55', -2.6, 1)", 'format'),
    ("decimal('£2.5', 2.5, 1)", 'unreadable'),
    ("decimal('2.5kg', 2.5, 1)", 'unreadable'),
    ("decimal('', 2.5, 1)", 'unreadable'),
    # decimal with a float-noisy key: the key is taken at its stated precision
    ("decimal('19.8', 6.6 * 3, 1)", 'correct'),
    # exact
    ("exact('24', 24)", 'correct'),
    ("exact('24.0', 24)", 'correct'),
    ("exact('24.00', 24)", 'correct'),
    ("exact('2.5', 2.5)", 'correct'),
    ("exact('24.3', 24)", 'wrong'),
    ("exact('23.99', 24)", 'wrong'),
    ("exact('25', 24)", 'wrong'),
    ("exact('2', 2.5)", 'wrong'),
    ("exact('x', 24)", 'unreadable'),
    ("exact('', 24)", 'unreadable'),
    # parse
    ("String(parse('£12.34'))", '12.34'),
    ("String(parse('2.5'))", '2.5'),
    ("String(parse('1e3'))", '1000'),
    ("String(parse('12abc'))", 'null'),
    ("String(parse(''))", 'null'),
    # message
    ("message('format', '1250.7', {currency: '£'})",
     'Right amount, but money always has two decimal places. In the exam, £1250.7 loses the mark. Fix it and resubmit.'),
    ("message('format', '€12.3', {currency: '€'})",
     'Right amount, but money always has two decimal places. In the exam, €12.3 loses the mark. Fix it and resubmit.'),
    ("message('format', '333.33', {dp: 1})",
     'Right value, but the question asks for 1 decimal place. In the exam, 333.33 loses the mark. Fix it and resubmit.'),
    ("message('format', '1.234', {dp: 2})",
     'Right value, but the question asks for 2 decimal places. In the exam, 1.234 loses the mark. Fix it and resubmit.'),
    ("message('unreadable', 'abc')", 'Type just the number, e.g. 12.34'),
    ("message('correct', '5')", ''),
]

# tax-theft's moneyResult() as it stood on main before this change, word for word.
OLD_MONEY_RESULT = r"""function oldMoneyResult(raw, keyPence) {
  var v = parseFloat(raw);
  if (Math.abs(v * 100 - keyPence) > 1e-6) return 'wrong';
  var written = keyPence % 100 === 0 ? /^\d+(\.\d\d)?$/ : /^\d+\.\d\d$/;
  return written.test(raw) ? 'correct' : 'format';
}"""

KEYS_PENCE = [0, 1, 5, 10, 50, 99, 100, 101, 125070, 305000, 1250, 1234, 3086, 123456]


def number_input_strings():
    """Strings a type="number" input can pass to a game (its value is sanitised to a valid
    floating-point number or ''), built around the keys above."""
    out = set()
    for kp in KEYS_PENCE:
        pounds, pence = divmod(kp, 100)
        for p in {pounds, pounds + 1, max(pounds - 1, 0)}:
            ps = str(p)
            out |= {ps, ps + '.', '-' + ps, ps + 'e0', ps + 'e1', ps + 'E-1'}
            for frac in ['0', '00', '000', '0000', str(pence // 10), '%02d' % pence,
                         '%02d0' % pence, '%02d1' % pence, '%02d00' % pence, '5', '99']:
                out |= {ps + '.' + frac, '-' + ps + '.' + frac}
                if p == 0:
                    out.add('.' + frac)
    return sorted(out)


async def run():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content('<!doctype html><title>t</title>')
        await page.add_script_tag(path=ANSWER_JS)
        await page.add_script_tag(content=OLD_MONEY_RESULT)
        fails = []
        for call, want in CASES:
            got = await page.evaluate(f'(() => {{ with (MaffsAnswer) {{ return {call}; }} }})()')
            if got != want:
                fails.append(f'{call}: got {got!r}, expected {want!r}')
        raws = [s for s in number_input_strings()]
        diff = await page.evaluate("""([raws, keys]) => {
            const out = []; let n = 0;
            for (const k of keys) for (const r of raws) {
                const old = oldMoneyResult(r, k);
                let neu = MaffsAnswer.money(r, k / 100);
                if (neu === 'unreadable') neu = 'wrong';   // never reachable: see below
                n++;
                if (old !== neu) out.push(r + ' @ ' + k + 'p: old ' + old + ', new ' + neu);
            }
            return {n, out};
        }""", [raws, KEYS_PENCE])
        # 'unreadable' cannot occur for these strings (each is a valid number); check that too.
        unread = await page.evaluate(
            "raws => raws.filter(r => MaffsAnswer.money(r, 1) === 'unreadable')", raws)
        await browser.close()
    for u in unread:
        fails.append(f'money({u!r}) is unreadable, but a type="number" input can pass it')
    for d in diff['out'][:20]:
        fails.append('tax-theft equivalence: ' + d)
    return fails, len(CASES), diff['n']


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    fails, ncases, nequiv = asyncio.run(run())
    for f in fails:
        print('FAIL    ' + f)
    if fails:
        print(f'\nFAILED: {len(fails)} problem(s)')
        return 1
    print(f'PASS: {ncases} outcome cases; money() equals the old moneyResult() on {nequiv} '
          f'(type="number" string, key) pairs')
    return 0


if __name__ == '__main__':
    sys.exit(main())
