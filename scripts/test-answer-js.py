#!/usr/bin/env python3
"""Self-tests for schools/assets/answer.js (MaffsAnswer, canon §7.1.3).

Runs the real file in Chromium and checks every outcome of every function: correct, wrong,
format and unreadable for money(), decimal(), exact(), fractionOrDecimal() and fractionForm() (value and form, 20 Oct 2026), the exact
reading of a typed fraction (fraction(), 7 Oct 2026: a/b, negatives, whole numbers), the accepted £/€ prefix, parse(),
and the words message() returns. moneyInput() (MONEY-INPUT, 9 Nov 2026) on real inputs: a type="number" box becomes
type="text" inputmode="decimal" autocomplete="off"; its sign shows inside the box's left edge, in the box's font and
colour, with the typing clear of it; the aria-label gains "in pounds" / "in euros"; a second call changes nothing; a
falsy currency takes the sign off; the wrapper is hidden with the box and keeps a flex:1 or 100% box's width; a box
focused at once keeps the focus; and
"£12.50" and "12.50", typed on the keyboard, are both 'correct' through money(). Then an equivalence check: on every string a type="number"
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
    # fraction: the exact reading of a/b or a whole number, in lowest terms, den > 0
    ("JSON.stringify(fraction('3/7'))", '{"num":3,"den":7}'),
    ("JSON.stringify(fraction('6/14'))", '{"num":3,"den":7}'),
    ("JSON.stringify(fraction(' 15 / 35 '))", '{"num":3,"den":7}'),
    ("JSON.stringify(fraction('-3/7'))", '{"num":-3,"den":7}'),
    ("JSON.stringify(fraction('3/-7'))", '{"num":-3,"den":7}'),
    ("JSON.stringify(fraction('-3/-7'))", '{"num":3,"den":7}'),
    ("JSON.stringify(fraction('+3/7'))", '{"num":3,"den":7}'),
    ("JSON.stringify(fraction('5'))", '{"num":5,"den":1}'),
    ("JSON.stringify(fraction('-5'))", '{"num":-5,"den":1}'),
    ("JSON.stringify(fraction('0'))", '{"num":0,"den":1}'),
    ("JSON.stringify(fraction('-0/4'))", '{"num":0,"den":1}'),
    ("JSON.stringify(fraction('10/5'))", '{"num":2,"den":1}'),
    ("JSON.stringify(fraction('3/0'))", 'null'),
    ("JSON.stringify(fraction('0.5'))", 'null'),
    ("JSON.stringify(fraction('1.5/3'))", 'null'),
    ("JSON.stringify(fraction('3//7'))", 'null'),
    ("JSON.stringify(fraction('3/7/2'))", 'null'),
    ("JSON.stringify(fraction('--3/7'))", 'null'),
    ("JSON.stringify(fraction('3/7x'))", 'null'),
    ("JSON.stringify(fraction(''))", 'null'),
    ("JSON.stringify(fraction('/7'))", 'null'),
    ("JSON.stringify(fraction('99999999999999999/2'))", 'null'),
    # fractionOrDecimal: 3/7 at 3 d.p. (Given That's case: 3/7 and 0.429 right, 0.43 not)
    ("fractionOrDecimal('3/7', 3, 7, 3)", 'correct'),
    ("fractionOrDecimal('15/35', 3, 7, 3)", 'correct'),
    ("fractionOrDecimal('-3/-7', 3, 7, 3)", 'correct'),
    ("fractionOrDecimal('0.429', 3, 7, 3)", 'correct'),
    ("fractionOrDecimal('.429', 3, 7, 3)", 'correct'),
    ("fractionOrDecimal('0.4290', 3, 7, 3)", 'correct'),
    ("fractionOrDecimal('0.4286', 3, 7, 3)", 'format'),
    ("fractionOrDecimal('0.43', 3, 7, 3)", 'wrong'),
    ("fractionOrDecimal('0.428', 3, 7, 3)", 'wrong'),
    ("fractionOrDecimal('4/7', 3, 7, 3)", 'wrong'),
    ("fractionOrDecimal('-3/7', 3, 7, 3)", 'wrong'),
    ("fractionOrDecimal('3/0', 3, 7, 3)", 'unreadable'),
    ("fractionOrDecimal('0.4/1', 3, 7, 3)", 'unreadable'),
    ("fractionOrDecimal('3/7ths', 3, 7, 3)", 'unreadable'),
    ("fractionOrDecimal('43%', 3, 7, 3)", 'unreadable'),
    # the key is rounded half up exactly: 5/8 = 0.625 at 2 d.p. is 0.63; 1/8 = 0.125 is 0.13
    ("fractionOrDecimal('0.63', 5, 8, 2)", 'correct'),
    ("fractionOrDecimal('0.62', 5, 8, 2)", 'wrong'),
    ("fractionOrDecimal('0.13', 1, 8, 2)", 'correct'),
    ("fractionOrDecimal('0.125', 1, 8, 2)", 'format'),
    ("fractionOrDecimal('0.0518', 259, 5000, 4)", 'correct'),
    ("fractionOrDecimal('0.05', 259, 5000, 4)", 'wrong'),
    ("fractionOrDecimal('-0.429', -3, 7, 3)", 'correct'),
    ("fractionOrDecimal('-0.429', 3, -7, 3)", 'correct'),
    ("fractionOrDecimal('-3/7', 3, -7, 3)", 'correct'),
    # whole numbers
    ("fractionOrDecimal('1', 7, 7, 3)", 'correct'),
    ("fractionOrDecimal('1.00', 7, 7, 3)", 'correct'),
    ("fractionOrDecimal('7/7', 7, 7, 3)", 'correct'),
    ("fractionOrDecimal('0', 0, 9, 3)", 'correct'),
    ("fractionOrDecimal('0/9', 0, 9, 3)", 'correct'),
    ("fractionOrDecimal('2', 3, 7, 3)", 'wrong'),
    # decimal() and exact() are unchanged: a fraction is still unreadable to them
    ("decimal('3/7', 0.429, 3)", 'unreadable'),
    ("decimal('6/2', 3, 1)", 'unreadable'),
    ("exact('3/7', 0.429)", 'unreadable'),
    # fractionForm: value AND form (20 Oct 2026). simplest is the default.
    ("fractionForm('1/2', {num: 1, den: 2})", 'correct'),
    ("fractionForm('2/4', {num: 1, den: 2})", 'format'),
    ("fractionForm('3/6', {num: 1, den: 2})", 'format'),
    ("fractionForm(' 1 / 2 ', {num: 1, den: 2})", 'correct'),
    ("fractionForm('+1/2', {num: 1, den: 2})", 'correct'),
    ("fractionForm('1/3', {num: 1, den: 2})", 'wrong'),
    ("fractionForm('2/3', {num: 1, den: 2})", 'wrong'),
    ("fractionForm('1', {num: 1, den: 2})", 'wrong'),
    ("fractionForm('1/2/3', {num: 1, den: 2})", 'unreadable'),
    ("fractionForm('1/2', {num: 1, den: 2}, {form: 'simplest'})", 'correct'),
    ("fractionForm('2/4', {num: 1, den: 2}, {form: 'simplest'})", 'format'),
    ("fractionForm('0.5', {num: 1, den: 2})", 'unreadable'),
    ("fractionForm('1/0', {num: 1, den: 2})", 'unreadable'),
    ("fractionForm('', {num: 1, den: 2})", 'unreadable'),
    ("fractionForm('abc', {num: 1, den: 2})", 'unreadable'),
    ("fractionForm('1/ 2x', {num: 1, den: 2})", 'unreadable'),
    ("fractionForm('1/-2', {num: 1, den: 2})", 'unreadable'),
    ("fractionForm('-1/-2', {num: 1, den: 2})", 'unreadable'),
    ("fractionForm('1 1/ 2 3', {num: 1, den: 2})", 'unreadable'),
    ("fractionForm('1,5', {num: 1, den: 2})", 'unreadable'),
    ("fractionForm('2', {num: 2, den: 1})", 'correct'),
    ("fractionForm('6/3', {num: 2, den: 1})", 'format'),
    ("fractionForm('4/2', {num: 2, den: 1})", 'format'),
    ("fractionForm('2/1', {num: 2, den: 1})", 'format'),
    ("fractionForm('3', {num: 2, den: 1})", 'wrong'),
    ("fractionForm('1', {num: 2, den: 1})", 'wrong'),
    ("fractionForm('2 0/3', {num: 2, den: 1})", 'format'),
    ("fractionForm('2.0', {num: 2, den: 1})", 'unreadable'),
    ("fractionForm('2', {num: 2, den: 1}, {form: 'mixed'})", 'correct'),
    ("fractionForm('6/3', {num: 2, den: 1}, {form: 'mixed'})", 'format'),
    ("fractionForm('2 0/3', {num: 2, den: 1}, {form: 'mixed'})", 'format'),
    ("fractionForm('7/4', {num: 7, den: 4})", 'correct'),
    ("fractionForm('14/8', {num: 7, den: 4})", 'format'),
    ("fractionForm('1 3/4', {num: 7, den: 4})", 'format'),
    ("fractionForm('1 6/8', {num: 7, den: 4})", 'format'),
    ("fractionForm('7/5', {num: 7, den: 4})", 'wrong'),
    ("fractionForm('1 1/4', {num: 7, den: 4})", 'wrong'),
    ("fractionForm('2', {num: 7, den: 4})", 'wrong'),
    ("fractionForm('1 3/4', {num: 7, den: 4}, {form: 'mixed'})", 'correct'),
    ("fractionForm('1  3 / 4', {num: 7, den: 4}, {form: 'mixed'})", 'correct'),
    ("fractionForm(' 1 3/4 ', {num: 7, den: 4}, {form: 'mixed'})", 'correct'),
    ("fractionForm('7/4', {num: 7, den: 4}, {form: 'mixed'})", 'format'),
    ("fractionForm('1 6/8', {num: 7, den: 4}, {form: 'mixed'})", 'format'),
    ("fractionForm('1 7/4', {num: 7, den: 4}, {form: 'mixed'})", 'wrong'),
    ("fractionForm('2 3/4', {num: 7, den: 4}, {form: 'mixed'})", 'wrong'),
    ("fractionForm('1 1/4', {num: 7, den: 4}, {form: 'mixed'})", 'wrong'),
    ("fractionForm('0 7/4', {num: 7, den: 4}, {form: 'mixed'})", 'format'),
    ("fractionForm('1', {num: 7, den: 4}, {form: 'mixed'})", 'wrong'),
    ("fractionForm('14/8', {num: 7, den: 4}, {form: 'mixed'})", 'format'),
    ("fractionForm('1 3 4', {num: 7, den: 4}, {form: 'mixed'})", 'unreadable'),
    ("fractionForm('1 3/0', {num: 7, den: 4}, {form: 'mixed'})", 'unreadable'),
    ("fractionForm('1 -3/4', {num: 7, den: 4}, {form: 'mixed'})", 'unreadable'),
    ("fractionForm('1 3/4 5', {num: 7, den: 4}, {form: 'mixed'})", 'unreadable'),
    ("fractionForm('1 3/4', {whole: 1, num: 3, den: 4}, {form: 'mixed'})", 'correct'),
    ("fractionForm('7/4', {whole: 1, num: 3, den: 4}, {form: 'mixed'})", 'format'),
    ("fractionForm('1 6/8', {whole: 1, num: 3, den: 4}, {form: 'mixed'})", 'format'),
    ("fractionForm('1 7/4', {whole: 1, num: 3, den: 4}, {form: 'mixed'})", 'wrong'),
    ("fractionForm('7/4', {whole: 1, num: 3, den: 4})", 'correct'),
    ("fractionForm('1 3/4', {whole: 1, num: 3, den: 4})", 'format'),
    ("fractionForm('14/8', {whole: 1, num: 3, den: 4})", 'format'),
    ("fractionForm('1 5/4', {whole: 2, num: 1, den: 4}, {form: 'mixed'})", 'format'),
    ("fractionForm('2 1/4', {whole: 2, num: 1, den: 4}, {form: 'mixed'})", 'correct'),
    ("fractionForm('1/2', {num: 1, den: 2}, {form: 'mixed'})", 'correct'),
    ("fractionForm('2/4', {num: 1, den: 2}, {form: 'mixed'})", 'format'),
    ("fractionForm('0 1/2', {num: 1, den: 2}, {form: 'mixed'})", 'format'),
    ("fractionForm('-1/2', {num: -1, den: 2})", 'correct'),
    ("fractionForm('-2/4', {num: -1, den: 2})", 'format'),
    ("fractionForm('1/2', {num: -1, den: 2})", 'wrong'),
    ("fractionForm('-1', {num: -1, den: 2})", 'wrong'),
    ("fractionForm('- 1/2', {num: -1, den: 2})", 'unreadable'),
    ("fractionForm('-1 3/4', {whole: -1, num: 3, den: 4}, {form: 'mixed'})", 'correct'),
    ("fractionForm('-7/4', {whole: -1, num: 3, den: 4}, {form: 'mixed'})", 'format'),
    ("fractionForm('1 3/4', {whole: -1, num: 3, den: 4}, {form: 'mixed'})", 'wrong'),
    ("fractionForm('-7/4', {whole: -1, num: 3, den: 4})", 'correct'),
    ("fractionForm('-1 3/4', {whole: -1, num: 3, den: 4})", 'format'),
    ("fractionForm('-2', {num: -2, den: 1})", 'correct'),
    ("fractionForm('-4/2', {num: -2, den: 1})", 'format'),
    ("fractionForm('2', {num: -2, den: 1})", 'wrong'),
    ("fractionForm('0', {num: 0, den: 5})", 'correct'),
    ("fractionForm('0/5', {num: 0, den: 5})", 'format'),
    ("fractionForm('0/1', {num: 0, den: 5})", 'format'),
    ("fractionForm('-0', {num: 0, den: 5})", 'correct'),
    ("fractionForm('-0/5', {num: 0, den: 5})", 'format'),
    ("fractionForm('0 0/5', {num: 0, den: 5})", 'format'),
    ("fractionForm('1', {num: 0, den: 5})", 'wrong'),
    ("fractionForm('0/0', {num: 0, den: 5})", 'unreadable'),
    ("fractionForm('0', {num: 0, den: 5}, {form: 'mixed'})", 'correct'),
    ("fractionForm('0/5', {num: 0, den: 5}, {form: 'mixed'})", 'format'),
    ("fractionForm('99999999999999999/2', {num: 1, den: 2})", 'unreadable'),
    ("fractionForm('1 99999999999999999/2', {num: 1, den: 2})", 'unreadable'),
    ("message('format', '2/4', {fraction: 'simplest'})",
     'Right value, but simplify it fully. In the exam, 2/4 may lose the mark. Fix it and resubmit.'),
    ("message('format', ' 7/4 ', {fraction: 'mixed'})",
     'Right value, but write it as a mixed number in its simplest form. In the exam, 7/4 may lose the mark. Fix it and resubmit.'),
    ("message('unreadable', 'abc', {fraction: 'simplest'})", 'Type a fraction or a whole number, e.g. 3/7'),
    ("message('unreadable', 'abc', {fraction: 'mixed'})", 'Type a mixed number, e.g. 1 3/4'),
    ("message('correct', '1/2', {fraction: 'simplest'})", ''),
    ("message('wrong', '1/3', {fraction: 'mixed'})", ''),
    # the existing messages are unchanged by the new fraction values
    ("message('format', '333.33', {dp: 1, fraction: true})",
     'Right value, but the question asks for 1 decimal place. In the exam, 333.33 loses the mark. Fix it and resubmit.'),
    ("typeof fractionForm + ' ' + Object.keys(MaffsAnswer).sort().join()",
     'function decimal,exact,fraction,fractionForm,fractionOrDecimal,message,money,moneyInput,parse'),
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
    ("message('unreadable', 'abc', {fraction: true})", 'Type a fraction or a decimal, e.g. 3/7 or 0.429'),
    ("message('format', '0.4286', {dp: 3, sf: 3})",
     'Right value, but the question asks for 3 significant figures. In the exam, 0.4286 loses the mark. Fix it and resubmit.'),
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

# moneyInput() on real inputs, the shapes the six money games build: a type="number" box (tax-theft), a flex:1 box in
# a row (tax-theft), a width:100% box (estimation-engine), a fixed-width centred box (split-it), a box with no
# aria-label (its placeholder "?" is no label), and one shared by money and other questions (squared-squirrel, its-on-sale).
MONEY_PAGE = '''<!doctype html><title>t</title>
<style>body{font:16px sans-serif;color:rgb(10,20,30)}
.row{display:flex;gap:8px;width:400px}
.box{font:600 20px monospace;color:rgb(200,0,0);padding:4px 6px;border:2px solid #888;box-sizing:border-box}
#flex{flex:1}#full{width:100%}#fixed{width:120px;text-align:center}</style>
<div class="row"><span>&pound;?</span><input id="num" class="box" type="number" aria-label="Your answer"></div>
<div class="row"><input id="flex" class="box" type="text" placeholder="?"><button>Check</button></div>
<div style="width:300px;display:flex"><input id="full" class="box" type="text" aria-label="Estimate"></div>
<div><input id="fixed" class="box" type="text" aria-label="Your answer in pounds"></div>
<div><input id="eur" class="box" type="text" aria-label="Share"></div>
<div><input id="shared" class="box" type="text" inputmode="decimal" aria-label="Your answer"></div>'''

MONEY_JS = '''() => {
  const $ = id => document.getElementById(id), out = {};
  const w0 = { flex: $('flex').offsetWidth, full: $('full').offsetWidth, fixed: $('fixed').offsetWidth };
  ['num', 'flex', 'full', 'fixed'].forEach(id => MaffsAnswer.moneyInput($(id), '\u00a3'));
  MaffsAnswer.moneyInput($('eur'), '\u20ac');
  const look = id => {
    const inp = $(id), wrap = inp.parentElement, sign = wrap.querySelector('.maffs-money-sign'), cs = getComputedStyle(inp);
    const sc = sign && getComputedStyle(sign), ir = inp.getBoundingClientRect(), sr = sign && sign.getBoundingClientRect();
    return { type: inp.type, im: inp.getAttribute('inputmode'), ac: inp.getAttribute('autocomplete'),
             label: inp.getAttribute('aria-label'), wrapped: wrap.className, sign: sign && sign.textContent,
             hiddenFromReaders: sign && sign.getAttribute('aria-hidden'),
             shown: !!(sr && sr.width > 0 && sr.left >= ir.left && sr.right <= ir.left + parseFloat(cs.paddingLeft) + parseFloat(cs.borderLeftWidth)),
             font: sc && sc.fontFamily === cs.fontFamily && sc.fontSize === cs.fontSize && sc.fontWeight === cs.fontWeight,
             colour: sc && sc.color === cs.color, width: inp.offsetWidth };
  };
  ['num', 'flex', 'full', 'fixed', 'eur'].forEach(id => { out[id] = look(id); });
  out.w0 = w0;
  const before = $('num').parentElement.parentElement.innerHTML;
  MaffsAnswer.moneyInput($('num'), '\u00a3');
  out.idem = $('num').parentElement.parentElement.innerHTML === before && document.querySelectorAll('.maffs-money').length === 5
             && document.querySelectorAll('#maffs-money-css').length === 1;
  const sh = $('shared');
  MaffsAnswer.moneyInput(sh, null);
  out.offFirst = !sh.parentElement.classList.contains('maffs-money');
  MaffsAnswer.moneyInput(sh, '\u00a3');
  const on = look('shared');
  MaffsAnswer.moneyInput(sh, null);
  const sign = sh.parentElement.querySelector('.maffs-money-sign');
  out.shared = { on: on.shown && on.label === 'Your answer in pounds',
                 off: getComputedStyle(sign).display === 'none' && sh.getAttribute('aria-label') === 'Your answer'
                      && sh.style.paddingLeft === '' };
  MaffsAnswer.moneyInput(sh, '\u00a3');
  sh.hidden = true;
  return new Promise(r => setTimeout(() => {
    out.hidden = sh.parentElement.hidden && sh.parentElement.offsetWidth === 0;
    r(out);
  }, 0));
}'''



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
        fails += await money_input_fails(browser)
        await browser.close()
    for u in unread:
        fails.append(f'money({u!r}) is unreadable, but a type="number" input can pass it')
    for d in diff['out'][:20]:
        fails.append('tax-theft equivalence: ' + d)
    return fails, len(CASES), diff['n']


async def money_input_fails(browser):
    """moneyInput() on the MONEY_PAGE boxes, and typing into a money box on the keyboard."""
    fails = []
    page = await browser.new_page()
    await page.set_content(MONEY_PAGE)
    await page.add_script_tag(path=ANSWER_JS)
    got = await page.evaluate(MONEY_JS)
    words = {'num': 'Your answer in pounds', 'flex': 'Your answer in pounds', 'full': 'Estimate in pounds',
             'fixed': 'Your answer in pounds', 'eur': 'Share in euros'}
    for box, label in words.items():
        g = got[box]
        if (g['type'], g['im'], g['ac']) != ('text', 'decimal', 'off'):
            fails.append('moneyInput #%s: type %r, inputmode %r, autocomplete %r (want text, decimal, off)'
                         % (box, g['type'], g['im'], g['ac']))
        if g['wrapped'] != 'maffs-money' or g['sign'] != ('\u20ac' if box == 'eur' else '\u00a3'):
            fails.append('moneyInput #%s: wrapper %r, sign %r' % (box, g['wrapped'], g['sign']))
        if not g['shown']:
            fails.append('moneyInput #%s: the sign is not shown inside the box, clear of the typing' % box)
        if g['hiddenFromReaders'] != 'true':
            fails.append('moneyInput #%s: the sign is read out (aria-hidden %r); the label carries it'
                         % (box, g['hiddenFromReaders']))
        if not (g['font'] and g['colour']):
            fails.append("moneyInput #%s: the sign is not in the box's font and colour" % box)
        if g['label'] != label:
            fails.append('moneyInput #%s: aria-label %r, want %r' % (box, g['label'], label))
    for box in ('flex', 'full', 'fixed'):
        if abs(got[box]['width'] - got['w0'][box]) > 1:
            fails.append('moneyInput #%s: the box was %dpx wide and is %dpx in its wrapper'
                         % (box, got['w0'][box], got[box]['width']))
    if not got['idem']:
        fails.append('moneyInput: a second call with the same currency changed the page')
    if not got['offFirst']:
        fails.append('moneyInput(input, null) on a plain box wrapped it')
    if not got['shared']['on']:
        fails.append('moneyInput: a shared box switched to money shows no sign or no "in pounds"')
    if not got['shared']['off']:
        fails.append('moneyInput(input, null): the sign, the label or the padding is not put back')
    if not got['hidden']:
        fails.append('moneyInput: a hidden box leaves its wrapper (and sign) showing')
    # A game that focuses a new money box at once (estimation-engine's first box): measuring it on the next frame
    # must not take the focus away, or the student's typing goes nowhere.
    kept = await page.evaluate('''() => new Promise(r => {
        const i = document.createElement('input'); i.id = 'late'; i.className = 'box';
        document.body.appendChild(i); MaffsAnswer.moneyInput(i, '\u00a3'); i.focus();
        requestAnimationFrame(() => requestAnimationFrame(() => r(document.activeElement === i))); })''')
    if not kept:
        fails.append('moneyInput: a box focused at once lost the focus when it was measured')
    await page.keyboard.type('£5.00')
    if await page.input_value('#late') != '£5.00':
        fails.append('moneyInput: typing into a box focused at once went elsewhere (%r)' % await page.input_value('#late'))
    for box in ('num', 'fixed'):
        for typed in ('\u00a312.50', '12.50'):
            await page.fill('#' + box, '')
            await page.click('#' + box)
            await page.keyboard.type(typed)
            value = await page.input_value('#' + box)
            res = await page.evaluate('v => MaffsAnswer.money(v, 12.5)', value)
            if value != typed or res != 'correct':
                fails.append('moneyInput #%s: typed %r, the box holds %r, money() says %r (want it kept, correct)'
                             % (box, typed, value, res))
    await page.close()
    return fails


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
    print(f'PASS: {ncases} outcome cases; moneyInput() on 7 boxes (type, inputmode, sign, label, width, a second '
          f'call, sign off, hidden, focus kept, "£12.50" and "12.50" typed); money() equals the old moneyResult() on {nequiv} '
          f'(type="number" string, key) pairs')
    return 0


if __name__ == '__main__':
    sys.exit(main())
