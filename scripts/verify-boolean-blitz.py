#!/usr/bin/env python3
# ci-line: Boolean Blitz (every key's truth table recomputed from its expression; an option right exactly when it has the key's truth table and no more literals; answer once; Chromium) |
"""Boolean Blitz: every key simplifies its expression, and an option is right exactly when it means the same and
is no longer.

42 Level 4 items, each a Boolean expression to simplify fully, with four options. The tranche 6 audit of 7 Oct
2026 found (contract LISTED-HIGH and Jon's rulings, 9 Oct 2026):
  boolean-blitz-t6-001  the options were locked by a CSS class only: Enter added +3 per press, Tab+Enter turned a
                        wrong answer right. Fixed on main by F1 batch 11 (MaffsLock); kept here.
  boolean-blitz-t6-002  key B(A + C); AB + BC, the same function, marked wrong.
  boolean-blitz-t6-003  key A(B + C); AB + AC marked wrong, though the walkthrough passes through it.
Jon's rulings: mark by truth table over all inputs, in the game; and (9 Oct, his answer on unsimplified forms) an
option is right when it has the key's truth table AND no more literals than the longer of the key and the function's
minimal sum of products: AB + BC (minimal SOP) is right for B(A + C); A·B + A stays wrong for A.

Checks: every item's key has its expression's truth table (keys recomputed); the options this rule accepts
(computed here, with this script's own parser) are exactly those the page marks right, every option clicked in
Chromium (390x844); t6-002 and t6-003 accept their second form, and no other option anywhere is accepted beside
its key (Jon, 18:56: a new one needs his ruling); t6-001: after a mark, Enter three times and Tab+Enter on another
option change neither the score nor the marks. A self-test plants the old exact-string marking, a rule accepting
any option with the key's truth table, a new equal option in Q24, and the old CSS-only lock; each must FAIL.

    python scripts/verify-boolean-blitz.py [--no-selftest] [--against FILE] [--katex-dir DIR]
"""
import argparse
import itertools
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'boolean-blitz'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNT = 42
RULED = {'B(A + C)': 'AB + BC', 'A(B + C)': 'AB + AC'}     # t6-002, t6-003: the second form each must accept


class Parser:
    """TeX Boolean expression -> a function of an assignment {letter: bool}. Precedence: NOT, AND, XOR, OR."""

    def __init__(self, tex):
        self.s = re.sub(r'\s+', '', tex.replace('\\,', ''))
        self.i = 0

    def at(self, w):
        return self.s.startswith(w, self.i)

    def parse(self):
        f = self.disj()
        if self.i != len(self.s):
            raise ValueError('trailing %r' % self.s[self.i:])
        return f

    def disj(self):
        parts = [self.xor()]
        while self.at('+'):
            self.i += 1
            parts.append(self.xor())
        return lambda e: any(p(e) for p in parts)

    def xor(self):
        parts = [self.conj()]
        while self.at('\\oplus'):
            self.i += 6
            parts.append(self.conj())
        return lambda e: sum(p(e) for p in parts) % 2 == 1

    def conj(self):
        parts = [self.unit()]
        while True:
            if self.at('\\cdot'):
                self.i += 5
            elif not (self.i < len(self.s) and (self.s[self.i] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ01(' or self.at('\\overline{'))):
                break
            parts.append(self.unit())
        return lambda e: all(p(e) for p in parts)

    def unit(self):
        if self.at('\\overline{'):
            self.i += 10
            inner = self.disj()
            if not self.at('}'):
                raise ValueError('no }')
            self.i += 1
            return lambda e: not inner(e)
        if self.at('('):
            self.i += 1
            inner = self.disj()
            if not self.at(')'):
                raise ValueError('no )')
            self.i += 1
            return inner
        c = self.s[self.i:self.i + 1]
        self.i += 1
        if c == '0':
            return lambda e: False
        if c == '1':
            return lambda e: True
        if c.isalpha() and c.isupper():
            return lambda e: e[c]
        raise ValueError('cannot read %r' % c)


def table(tex, letters):
    f = Parser(tex).parse()
    return tuple(f(dict(zip(letters, bits))) for bits in itertools.product((False, True), repeat=len(letters)))


def literals(tex):
    return len(re.findall(r'[A-Z]', tex))


def min_sop_literals(tex, letters):
    """Literals in the minimal sum of products of tex (SymPy's SOPform: Quine-McCluskey), 0 for a constant."""
    from sympy import symbols
    from sympy.logic import SOPform
    syms = symbols(letters)
    ones = [list(bits) for bits in itertools.product((0, 1), repeat=len(letters))
            if Parser(tex).parse()(dict(zip(letters, map(bool, bits))))]
    if not ones or len(ones) == 2 ** len(letters):
        return 0
    return sum(1 for a in __import__('sympy').preorder_traversal(SOPform(syms, ones)) if a.is_Symbol)


def accepted(q):
    """The options the ruling accepts: the key, and any with its truth table and no more literals than the
    longer of the key and the function's minimal sum of products."""
    out = []
    for o in [q['answer']] + list(q['distractors']):
        if o == q['answer']:
            out.append(o)
            continue
        letters = sorted(set(re.findall(r'[A-Z]', o + q['answer'] + q['expr'])))
        try:
            same = table(o, letters) == table(q['answer'], letters)
        except ValueError:
            same = False
        if same and literals(o) <= max(literals(q['answer']), min_sop_literals(q['answer'], letters)):
            out.append(o)
    return out


def check_bank(fails, bank):
    if len(bank) != COUNT:
        fails.append('bank: %d items, expected %d' % (len(bank), COUNT))
    for n, q in enumerate(bank):
        w = 'Q%d (%s)' % (n, q['expr'])
        letters = sorted(set(re.findall(r'[A-Z]', q['expr'] + q['answer'])))
        try:
            if table(q['answer'], letters) != table(q['expr'], letters):
                fails.append('%s: keyed %s, which does not have the expression\'s truth table' % (w, q['answer']))
        except ValueError as e:
            fails.append('%s: %s' % (w, e))
        if q['answer'] in RULED and RULED[q['answer']] in q['distractors'] and RULED[q['answer']] not in accepted(q):
            fails.append('%s: %s must be accepted beside %s (Jon\'s ruling)' % (w, RULED[q['answer']], q['answer']))
        for o in accepted(q):
            if o != q['answer'] and RULED.get(q['answer']) != o:
                fails.append('%s: %s accepted beside the key %s; Jon accepted only AB + BC (for B(A + C)) and '
                             'AB + AC (for A(B + C)): a new accepted option needs his ruling' % (w, o, q['answer']))


SWEEP_JS = r"""(acc) => {
  window.setTimeout = () => 0;
  const out = [];
  QUESTIONS.forEach((q, n) => {
    for (const pick of [q.answer, ...q.distractors]) {
      order = [n]; qIndex = 0; score = 0; points = 0;
      loadQuestion();
      const btn = [...document.querySelectorAll('#optionsGrid .opt-btn')].find(b => b.dataset.val === pick);
      if (!btn) { out.push([n, pick, 'not on screen']); continue; }
      btn.click();
      const right = btn.classList.contains('correct');
      if (right !== acc[n].includes(pick)) out.push([n, pick, right ? 'marked right' : 'marked wrong']);
    }
  });
  return out;
}"""
KATEX_DIR = None


def page_for(pw, base, html, fresh_off):
    browser = pw.chromium.launch()
    ctx = browser.new_context(viewport={'width': 390, 'height': 844})
    if fresh_off:
        ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: not url.startswith(base) and '/katex@' not in url, lambda route: route.abort())
    if KATEX_DIR:
        ctx.route(lambda url: '/katex@' in url and '/dist/' in url, lambda route: route.fulfill(
            path=os.path.join(KATEX_DIR, route.request.url.split('/dist/', 1)[1].split('?')[0])))
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
    page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof katex !== "undefined"', timeout=15000)
    return browser, page, errors


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser, page, errors = page_for(pw, base, html, True)
            bank = page.evaluate('() => QUESTIONS')
            acc = [accepted(q) for q in bank]
            page.evaluate("() => startGame()")
            for n, pick, what in page.evaluate(SWEEP_JS, acc):
                fails.append('Q%d in Chromium: option %s %s (accepted: %s)' % (n, pick, what, ', '.join(acc[n])))
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            # t6-001: a real question, the real lock: one mark, then Enter x3 and Tab+Enter on another option.
            browser, page, errors = page_for(pw, base, html, False)
            page.evaluate("() => { startGame(); order = [24]; qIndex = 0; score = 0; points = 0; loadQuestion(); }")
            time.sleep(0.5)
            key = bank[24]['answer']
            btns = page.locator('#optionsGrid .opt-btn')
            vals = [btns.nth(k).get_attribute('data-val') for k in range(btns.count())]
            btns.nth(vals.index(key)).click()
            for _ in range(3):
                page.keyboard.press('Enter')
            wrong = next(k for k, v in enumerate(vals) if v not in acc[24])
            btns.nth(wrong).focus()
            page.keyboard.press('Enter')
            time.sleep(0.3)
            pts, marks = page.evaluate("() => [points, document.querySelectorAll('#optionsGrid .opt-btn.incorrect').length]")
            if pts != 3 or marks:
                fails.append('t6-001: after one right answer, Enter x3 and Tab+Enter on a wrong option: %s points and '
                             '%d option(s) marked wrong (expected 3 and 0)' % (pts, marks))
            browser.close()
            return bank
    finally:
        proc.terminate()
        proc.wait()


PLANTS = [
    ('Q', 't6-002/003: marking by exact string',
     [('  const correct = sameAnswer(selected, q.answer);', '  const correct = selected === q.answer;'),
      ('    if (sameAnswer(b.dataset.val, q.answer)) {', '    if (b.dataset.val === q.answer) {')]),
    ('Q', 'any option with the key\'s truth table accepted',
     [('  return boolLiterals(opt) <= Math.max(boolLiterals(key), minSopLiterals(g, vars));', '  return true;')]),
    ('Q24', 'a new equal option, B(C + A), in Q24',
     [("    distractors: [`AB + BC`, `BC`, `ABC`],", "    distractors: [`AB + BC`, `B(C + A)`, `ABC`],")]),
    ('t6-001', 't6-001: a CSS-only lock (before F1 batch 11)',
     [("  if (!MaffsLock.lock(document.getElementById('optionsGrid'))) return;", "  // (no guard: the CSS class alone)")]),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    ap.add_argument('--katex-dir', help='serve KaTeX from this local dist/ folder')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    global KATEX_DIR
    KATEX_DIR = args.katex_dir
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    bank = play(fails, html)
    if bank is not None:
        check_bank(fails, bank)
        extra = ['Q%d %s: %s' % (n, q['answer'], ', '.join(a for a in accepted(q) if a != q['answer']))
                 for n, q in enumerate(bank) if len(accepted(q)) > 1]
        print('%s: %d items, every key recomputed, every option marked in Chromium; accepted beside the key: %s'
              % (SLUG, len(bank), '; '.join(extra) or 'none'))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, swaps in PLANTS:
            planted = html
            for new, old in swaps:
                if planted.count(new) != 1:
                    planted = None
                    break
                planted = planted.replace(new, old)
            if planted is None:
                print('  self-test %-46s *** CANNOT PLANT ***' % what)
                ok = False
                continue
            rep = []
            pb = play(rep, planted)
            if pb is not None:
                check_bank(rep, pb)
            hit = [f for f in rep if f.startswith(tag)]
            ok = ok and bool(hit)
            print('  self-test %-46s %s' % (what, ('caught: ' + hit[0][:110]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
