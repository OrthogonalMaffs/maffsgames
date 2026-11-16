#!/usr/bin/env python3
# ci-line: Percentage Flip (every key and every equation in the working recomputed from the question text alone; 3/3/2/2 easiest-first deals per level; MaffsAnswer marking both ways round, money format never marked; KaTeX working; the fold after a wrong answer at 320x568 and 375x667) |
"""Percentage Flip (games/percentage-flip/): three banks of 40, one per level, served easiest first (contract
PERCENTAGE-FLIP-BANKS, 16 Nov 2026; Jon's rulings of 15 Nov).

The bank is one object, QUESTIONS = {year6, ks3, gcse}, read from the page as served. Each item is
{band, q, a, u?, w}: band 1-4 (1 easiest), the question, the key, the unit ("£", "%", "g" or none), the working
(one KaTeX string per line).

WHAT THIS DOES NOT TRUST
-------------------------------------------------------------------------------
The key and the working are never used to grade themselves. From the question's own words alone, with
fractions.Fraction, this script works out the kind of question (percentage of, increase or decrease, one number as
a percentage of another, percentage change, profit or loss, simple interest, reverse percentage), its answer, the
amount the working's percentages are of, the change and the interest. Then:
  Key      equals that answer.
  Working  every equation in every line holds: each side of each "=" is evaluated (numbers, +, -, \\times, \\div,
           \\frac, \\tfrac); a leading "P\\%" is P% of the question's base (or P/100 itself when it equals a unit
           fraction); "\\text{change}" is the difference of the two amounts; "\\text{interest}" is P r y / 100;
           "N \\text{ is } P\\% \\text{ of the original}" is N = P% of the recomputed original. A line this script
           cannot read fails. The last line ends with the key.
  Form     a "£" key is a whole number of pence; every other key is exact (a terminating decimal), and no question
           asks for rounding.
  Bank     40 questions a level, 10 a band, no question repeated within a level.
In Chromium, through the page's own functions:
  KaTeX    every working line rendered by the page's renderWorking(): one .katex each, no .katex-error.
  Deals    startGame() 20 times a level: 10 different questions of that level's own bank, bands 1,1,1,2,2,2,3,3,4,4.
  Routing  ?level=year6, ks3 and gcse: gameLevel is that level, a full game submits that level to the leaderboard and
           sends it on every question_answered.
  Marking  every item: the key as the card shows it is right (+10), the key one unit (one penny for "£") out is wrong;
           the money item 27.60: "27.60" and "£27.60" right, "27.6" format (the format message, no mark, no event, the
           card stays, and "27.60" can then be resubmitted), "27.59" wrong; on a "%" item, "35%" unreadable (no mark,
           no event) and "35" right; the same through the card (flipCard): an empty card counts wrong and turns, a
           typed 27.6 does not turn it. The box: a £ box on money items only, the unit beside it for % and g.
  Fold     after a wrong answer, every question at each level: the reason and Next above the fold (the viewport less the
           40px footer) at 320x568 and 375x667, no sideways scroll, neither face of the card clipped.
Marks are read from the page's feedback and score, never from analytics; question_answered events are only counted.

Plants (each must fail): a key changed by 1; a duplicate question; a working line that does not end with the key;
a band served out of order; a pence key at 1 d.p. accepted as right; GCSE routed to the KS3 bank.

    python scripts/verify-percentage-flip.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402
import plant_common as pc  # noqa: E402

SLUG = 'percentage-flip'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
LEVELS = ('year6', 'ks3', 'gcse')
SERVED = [1, 1, 1, 2, 2, 2, 3, 3, 4, 4]
DEALS = 20
FOLD_SIZES = ((320, 568), (375, 667))
FOOTER = 40
NUM = r'(\d+(?:\.\d+)?)'
F = Fraction


# ---------------------------------------------------------------- the answer, from the question's words alone
def solve(t):
    """{'kind', 'ans', 'base', 'change'?, 'interest'?} from the question text, or raises ValueError."""
    m = re.fullmatch(r'What is ' + NUM + r'% of ' + NUM + r'\?', t)
    if m:
        p, n = F(m[1]), F(m[2])
        return {'kind': 'of', 'ans': p * n / 100, 'base': n}
    m = (re.fullmatch(r'What is ' + NUM + r' out of ' + NUM + r' as a percentage\?', t)
         or re.fullmatch(r'What is ' + NUM + r' as a percentage of ' + NUM + r'\?', t)
         or re.fullmatch(r'\w+ (?:got|scored) ' + NUM + r' out of ' + NUM + r' on a test\. What percentage (?:is that|did she score)\?', t)
         or re.fullmatch(NUM + r' of the ' + NUM + r' [a-z ]+\. What percentage (?:walk|is that)\?', t)
         or re.fullmatch(r'\w+ spends £' + NUM + r' of his £' + NUM + r' budget on food\. What percentage of his budget is that\?', t))
    if m:
        return {'kind': 'outof', 'ans': F(m[1]) / F(m[2]) * 100, 'base': None}
    m = re.fullmatch(r'(Increase|Decrease) ' + NUM + r' by ' + NUM + r'%\.', t)
    if m:
        n, p = F(m[2]), F(m[3])
        s = 1 if m[1] == 'Increase' else -1
        return {'kind': 'incdec', 'ans': n * (100 + s * p) / 100, 'base': n}
    m = re.fullmatch(r'£' + NUM + r' is saved at ' + NUM + r'% simple interest per year\. How much (interest is earned in|is in the account after) (\d+) years\?', t)
    if m:
        P, r, y = F(m[1]), F(m[2]), F(m[4])
        i = P * r / 100 * y
        return {'kind': 'interest', 'ans': i if m[3].startswith('interest') else P + i, 'base': P, 'interest': i}
    m = re.search(r'from £?' + NUM + r'(?: cm)? to £?' + NUM, t)
    want = re.search(r'percentage (increase|decrease)\?$', t)
    if m and want:
        a, b = F(m[1]), F(m[2])
        if (b > a) != (want[1] == 'increase'):
            raise ValueError('the words say %s but the amounts go the other way' % want[1])
        return {'kind': 'change', 'ans': abs(b - a) / a * 100, 'base': a, 'change': abs(b - a)}
    m = re.search(r'buys an? \w+ for £' + NUM + r' and sells it for £' + NUM + r'\. What is (?:the|his|her) percentage (loss|profit)\?$', t)
    if m:
        a, b = F(m[1]), F(m[2])
        if (b > a) != (m[3] == 'profit'):
            raise ValueError('the words say %s but the amounts go the other way' % m[3])
        return {'kind': 'change', 'ans': abs(b - a) / a * 100, 'base': a, 'change': abs(b - a)}
    # an increase or decrease in context, forwards or reversed
    pcts = re.findall(NUM + r'%', t)
    if len(pcts) != 1:
        raise ValueError('not a question shape this verifier knows')
    p = F(pcts[0])
    up = bool(re.search(r'goes up by|pay rise|VAT|increase|price rise', t))
    down = bool(re.search(r'reduced by|% off|smaller|reduction|% cut', t))
    if up == down:
        raise ValueError('cannot tell an increase from a decrease')
    s = 1 if up else -1
    amounts = [F(x) for x in re.findall(r'£' + NUM, t)] + [F(x) for x in re.findall(NUM + r' (?:g|people)\b', t)]
    if len(amounts) != 1:
        raise ValueError('expected one amount, found %d' % len(amounts))
    n = amounts[0]
    if re.search(r'\bbefore\b(?! VAT\. VAT)|original', t):
        orig = n * 100 / (100 + s * p)
        return {'kind': 'reverse', 'ans': orig, 'base': orig}
    return {'kind': 'incdec', 'ans': n * (100 + s * p) / 100, 'base': n}


def evalexpr(e):
    """An arithmetic side of an equation, exactly; None if it is not arithmetic."""
    e = re.sub(r'\\t?frac\{([\d.]+)\}\{([\d.]+)\}', r'(F("\1")/F("\2"))', e.strip())
    e = e.replace('\\times', '*').replace('\\div', '/')
    e = re.sub(r'(?<![\w"])(\d+(?:\.\d+)?)', r'F("\1")', e)
    if not e or not re.fullmatch(r'[F()"\d.\s*/+-]+', e):
        return None
    try:
        return eval(e, {'F': F, '__builtins__': {}})  # noqa: S307 - digits, operators and F() only (checked above)
    except (SyntaxError, ZeroDivisionError):
        return None


def working_faults(w, facts):
    """Every equation in the working checked against the question's own facts. [] when it all holds."""
    out, prev = [], None
    base = facts['base']
    for line in w:
        for stmt in re.split(r',\s*\\;\s*', line):
            s, label = stmt.strip(), None
            m = re.match(r'\\text\{([^}]*)\}\s*', s)
            if m:
                label, s = m[1].strip(), s[m.end():]
            m = re.fullmatch(NUM + r' \\text\{ is \} ' + NUM + r'\\% \\text\{ of the original\}', s)
            if m:
                if facts['kind'] != 'reverse' or F(m[1]) != F(m[2]) / 100 * base:
                    out.append('%r: %s is not %s%% of the original %s' % (line, m[1], m[2], base))
                continue
            segs = [x.strip() for x in s.split('=')]
            vals = []
            if label in ('change', 'interest'):
                if label not in facts:
                    out.append('%r: this question has no %s' % (line, label))
                    continue
                if segs[0] != '':
                    out.append('%r: cannot read %r' % (line, stmt))
                    continue
                segs = segs[1:]
                vals.append(('v', facts[label]))
            elif label not in (None, 'one year:'):
                out.append('%r: unknown label %r' % (line, label))
                continue
            bad = False
            for i, seg in enumerate(segs):
                if seg == '' and i == 0 and not vals:
                    if prev is None:
                        out.append('%r: continues nothing' % line)
                        bad = True
                        break
                    vals.append(('v', prev))
                    continue
                pm = re.fullmatch(NUM + r'\\%', seg)
                if pm and i == 0 and not vals:
                    vals.append(('pct', F(pm[1])))
                elif pm:
                    vals.append(('pctval', F(pm[1])))
                else:
                    v = evalexpr(seg)
                    if v is None:
                        out.append('%r: cannot read %r' % (line, seg))
                        bad = True
                        break
                    vals.append(('v', v))
            if bad or len(vals) < 2:
                if not bad and len(vals) < 2:
                    out.append('%r: no equation in %r' % (line, stmt))
                continue
            kind, ref = vals[0]
            if kind == 'pct':
                if re.fullmatch(r'\\tfrac\{\d+\}\{\d+\}', segs[1]):
                    ref = ref / 100
                elif base is None:
                    out.append('%r: a percentage of nothing in this question' % line)
                    continue
                else:
                    ref = ref / 100 * base
            for k, v in vals[1:]:
                if not (v == ref or (k == 'pctval' and v / 100 == ref)):
                    out.append('%r: %s does not equal %s' % (line, v, ref))
            prev = vals[-1][1]
    return out


def last_figure(line):
    m = re.search(NUM + r'(?:\\%)?\s*$', line)
    return F(m[1]) if m else None


def shown(it):
    """The key as the card should show it, and the right answer to type."""
    a = F(str(it['a']))
    if it.get('u') == '£':
        typed = str(a.numerator) if a.denominator == 1 else '%.2f' % float(a)
        return '£' + typed, typed
    typed = str(it['a'])
    return typed + {'%': '%', 'g': ' g'}.get(it.get('u'), ''), typed


def check_bank(fails, level, bank):
    if len(bank) != 40:
        fails.append('%s: %d questions, not 40' % (level, len(bank)))
    for b in range(1, 5):
        n = sum(1 for it in bank if it.get('band') == b)
        if n != 10:
            fails.append('%s: band %d has %d questions, not 10' % (level, b, n))
    seen = set()
    for i, it in enumerate(bank, 1):
        where = '%s item %d (%s)' % (level, i, it.get('q'))
        if it['q'] in seen:
            fails.append('%s: the question is repeated' % where)
        seen.add(it['q'])
        if it.get('u') not in (None, '£', '%', 'g'):
            fails.append('%s: unknown unit %r' % (where, it.get('u')))
        if isinstance(it['a'], bool) or not isinstance(it['a'], (int, float)):
            fails.append('%s: the key is not a number: %r' % (where, it['a']))
            continue
        try:
            facts = solve(it['q'])
        except ValueError as e:
            fails.append('%s: cannot recompute: %s' % (where, e))
            continue
        key = F(str(it['a']))
        if key != facts['ans']:
            fails.append('%s: key %s, recomputed %s' % (where, it['a'], facts['ans']))
        for f in working_faults(it['w'], facts):
            fails.append('%s: working %s' % (where, f))
        if last_figure(it['w'][-1]) != facts['ans']:
            fails.append('%s: the last working line %r does not end with the answer %s' % (where, it['w'][-1], facts['ans']))
        if it.get('u') == '£':
            if (facts['ans'] * 100).denominator != 1:
                fails.append('%s: a money answer that is not a whole number of pence' % where)
        else:
            d = facts['ans'].denominator
            while d % 2 == 0:
                d //= 2
            while d % 5 == 0:
                d //= 5
            if d != 1:
                fails.append('%s: the answer %s is not an exact decimal' % (where, facts['ans']))
        if re.search(r'decimal place|significant|nearest|round', it['q'], re.I):
            fails.append('%s: the question asks for rounding' % where)


# ---------------------------------------------------------------- in Chromium
LOAD_JS = r"""(it) => { window.__qa = []; questions = [it]; qNum = 0; score = 0; correct = 0; flipped = false;
  MaffsLock.clearTimers(); MaffsLock.newSession(); loadQuestion(); }"""
STATE_JS = r"""() => { const fb = document.getElementById('feedback'), inp = document.getElementById('answerInput'),
  unit = document.getElementById('answerUnit'), wrap = inp.closest('.maffs-money');
  return {fb: fb.textContent, cls: fb.className, score: score, locked: MaffsLock.isLocked(mainEl), flipped: flipped,
          turned: document.getElementById('card').classList.contains('flipped'),
          events: window.__qa.length, back: document.getElementById('answerText').textContent,
          money: !!wrap && !wrap.classList.contains('maffs-money-off'), unit: unit.hidden ? '' : unit.textContent,
          label: inp.getAttribute('aria-label') || '', type: inp.type, mode: inp.getAttribute('inputmode')}; }"""
SPY_JS = r"""() => { window.__qa = []; window.__sub = []; if (window.__spied) return; window.__spied = true;
  const m = window.mfg; window.mfg = function (ev, p) { if (ev === 'question_answered') window.__qa.push(p); return m && m.apply(this, arguments); };
  window.MaffsLeaderboard = window.MaffsLeaderboard || {};
  window.MaffsLeaderboard.submitScore = function () { window.__sub.push([].slice.call(arguments)); return Promise.resolve(); }; }"""
RENDER_JS = r"""(it) => { renderWorking(it); const box = document.getElementById('workingsText');
  return {lines: box.querySelectorAll('.working-line').length, katex: box.querySelectorAll('.working-line > .katex').length,
          errors: box.querySelectorAll('.katex-error').length}; }"""
DEAL_JS = r"""(n) => { const out = []; for (let k = 0; k < n; k++) { startGame(); out.push(questions.map(q => [q.q, q.band]));
  MaffsLock.clearTimers(); } return out; }"""
FACE_JS = r"""() => Array.from(document.querySelectorAll('.card-face')).some(face => { const cs = getComputedStyle(face);
  let h = parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom);
  Array.from(face.children).forEach(el => { const ec = getComputedStyle(el);
    h += el.offsetHeight + parseFloat(ec.marginTop) + parseFloat(ec.marginBottom); });
  return h > face.clientHeight + 1 || face.scrollWidth > face.clientWidth + 1; })"""
FOLD_JS = r"""() => { const st = document.scrollingElement.scrollTop;
  const B = s => { const e = document.querySelector(s); return e ? Math.round(e.getBoundingClientRect().bottom + st) : null; };
  return {reason: B('#feedback'), next: B('#nextMount button'), sw: document.documentElement.scrollWidth}; }"""


def new_page(pw_browser, base, html, w=390, h=844, fonts=False):
    ctx = pw_browser.new_context(viewport={'width': w, 'height': h})
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    bc.offline(ctx, base)
    if fonts:
        ctx.route(lambda u: u.startswith((bc.GOOGLE_CSS, bc.GOOGLE_STATIC)), bc.serve_real_font)
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    page = ctx.new_page()
    page.__errors = []
    page.on('pageerror', lambda e: page.__errors.append(str(e)))
    return ctx, page


def open_level(page, base, level):
    page.goto(base + '/games/%s/?level=%s&cb=verify' % (SLUG, level), wait_until='load', timeout=20000)
    page.wait_for_function('typeof QUESTIONS !== "undefined" && window.katex && typeof checkAnswer === "function"', timeout=15000)
    page.evaluate(SPY_JS)


def answer(page, it, typed, via='check'):
    page.evaluate(LOAD_JS, it)
    page.evaluate('(v) => { document.getElementById("answerInput").value = v; }', typed)
    page.evaluate('() => checkAnswer()' if via == 'check' else '() => flipCard()')
    st = page.evaluate(STATE_JS)
    page.evaluate('() => MaffsLock.clearTimers()')
    return st


def check_marking(fails, page, banks):
    for level, bank in banks.items():
        for it in bank:
            face, typed = shown(it)
            a = F(str(it['a']))
            off = (a + F(1, 100)) if it.get('u') == '£' else (a + 1)
            off_typed = ('%.2f' % float(off)) if it.get('u') == '£' else (str(off.numerator) if off.denominator == 1 else str(float(off)))
            where = '%s %r' % (level, it['q'])
            st = answer(page, it, typed)
            if not (st['fb'].startswith('Correct! +10') and st['score'] == 10 and st['events'] == 1):
                fails.append('%s: the key %r was not marked right (%r)' % (where, typed, st))
            if st['back'] != face:
                fails.append('%s: the card shows %r, not %r' % (where, st['back'], face))
            if st['money'] != (it.get('u') == '£') or st['unit'] != {'%': '%', 'g': 'g'}.get(it.get('u'), ''):
                fails.append('%s: the answer box is wrong for unit %r (money %r, unit %r)' % (where, it.get('u'), st['money'], st['unit']))
            if st['type'] != 'text' or st['mode'] != 'decimal':
                fails.append('%s: the box is type %r inputmode %r' % (where, st['type'], st['mode']))
            want_label = {'%': 'percentage', 'g': 'grams', '£': 'pounds'}.get(it.get('u'))
            if want_label and want_label not in st['label']:
                fails.append('%s: the box label %r does not name %s' % (where, st['label'], want_label))
            st = answer(page, it, off_typed)
            if not (st['fb'].startswith('Not quite') and st['score'] == 0 and st['events'] == 1):
                fails.append('%s: %r (one %s out) was not marked wrong (%r)' % (
                    where, off_typed, 'penny' if it.get('u') == '£' else 'unit', st))

    money = next(it for it in banks['gcse'] if it['a'] == 27.6)
    pct = next(it for b in banks.values() for it in b if it.get('u') == '%' and it['a'] == 35)
    cases = [(money, '27.60', 'right'), (money, '£27.60', 'right'), (money, '27.6', 'format'), (money, '27.59', 'wrong'),
             (pct, '35%', 'unreadable'), (pct, '35', 'right')]
    for it, typed, want in cases:
        for via in ('check', 'flip'):
            st = answer(page, it, typed, via)
            where = '%r typed %r (%s)' % (it['q'][:40], typed, via)
            if want == 'right':
                ok = st['fb'].startswith('Correct! +10') and st['score'] == 10 and st['events'] == 1
            elif want == 'wrong':
                ok = st['fb'].startswith('Not quite') and st['score'] == 0 and st['events'] == 1
            else:
                msg = 'two decimal places' if want == 'format' else 'Type just the number'
                ok = msg in st['fb'] and st['score'] == 0 and st['events'] == 0 and not st['locked'] and not st['turned']
            if not ok:
                fails.append('%s: expected %s (%s): %r' % (where, want, 'format' if want == 'format' else want, st))
            if via == 'flip' and want in ('right', 'wrong') and not st['turned']:
                fails.append('%s: the card did not turn' % where)
    # a format answer, then the right form resubmitted: one mark, one event
    answer(page, money, '27.6')
    page.evaluate('() => { document.getElementById("answerInput").value = "27.60"; checkAnswer(); }')
    st = page.evaluate(STATE_JS)
    page.evaluate('() => MaffsLock.clearTimers()')
    if not (st['score'] == 10 and st['events'] == 1):
        fails.append('a format answer then 27.60 resubmitted: not one mark and one event (%r)' % st)
    # an empty card: wrong, turned, one event
    st = answer(page, money, '', 'flip')
    if not (st['turned'] and st['events'] == 1 and st['score'] == 0 and st['fb'].startswith('Answer was')):
        fails.append('an empty card tapped: not revealed and counted wrong once (%r)' % st)


def check_level_page(fails, page, base, level, banks):
    open_level(page, base, level)
    got = page.evaluate('() => [gameLevel, JSON.parse(JSON.stringify(POOL))]')
    if got[0] != level:
        fails.append('?level=%s: gameLevel is %r' % (level, got[0]))
    own = {it['q'] for it in banks[level]}
    pool = {it['q'] for it in got[1]}
    if pool != own:
        fails.append('?level=%s: the game draws from another bank (own bank: %d of %d)' % (level, len(pool & own), len(pool)))
    for d in page.evaluate(DEAL_JS, DEALS):
        qs = [q for q, _ in d]
        bands = [b for _, b in d]
        if len(qs) != 10 or len(set(qs)) != 10 or not set(qs) <= own:
            fails.append('?level=%s: a game is not 10 different questions from its own bank: %r' % (level, qs))
            break
        if bands != SERVED:
            fails.append('?level=%s: served bands %r, not %r (easiest first)' % (level, bands, SERVED))
            break
    # a full game, answered right through Check: the level reaches every event and the leaderboard
    page.evaluate(SPY_JS)
    page.evaluate('() => startGame()')
    for _ in range(10):
        it = page.evaluate('() => questions[qNum]')
        page.evaluate('(v) => { document.getElementById("answerInput").value = v; checkAnswer(); MaffsLock.clearTimers(); nextCard(); }',
                      shown(it)[1])
    st = page.evaluate('() => ({qa: window.__qa.map(p => p.level), sub: window.__sub, score: score})')
    if st['score'] != 100 or len(st['qa']) != 10 or set(st['qa']) != {level}:
        fails.append('?level=%s: a full game logged %r and scored %r' % (level, st['qa'], st['score']))
    if len(st['sub']) != 1 or st['sub'][0][:2] != [SLUG, level]:
        fails.append('?level=%s: the leaderboard got %r' % (level, st['sub']))


def check_fold(fails, browser, base, html, banks):
    for w, h in FOLD_SIZES:
        for level in LEVELS:
            ctx, page = new_page(browser, base, html, w, h, fonts=True)
            open_level(page, base, level)
            page.evaluate('() => startGame()')
            worst = 0
            for it in banks[level]:
                page.evaluate(LOAD_JS, it)
                bc.wait_settled(page, 30)
                if page.evaluate(FACE_JS):
                    fails.append('%dx%d %s %r: the question card is clipped' % (w, h, level, it['q']))
                page.fill('#answerInput', '0')
                page.click('.answer-row .btn-primary')
                page.evaluate('() => { MaffsLock.clearTimers(); showBack(true); }')
                page.wait_for_selector('#nextMount button', timeout=5000)
                bc.wait_settled(page, 30)
                r = page.evaluate(FOLD_JS)
                worst = max(worst, r['next'] or 10 ** 6)
                if r['next'] is None or r['next'] > h - FOOTER or r['reason'] > h - FOOTER:
                    fails.append('%dx%d %s %r: after a wrong answer the reason ends at %s and Next at %s, fold %d' % (
                        w, h, level, it['q'], r['reason'], r['next'], h - FOOTER))
                if r['sw'] > w:
                    fails.append('%dx%d %s %r: sideways scroll (%d)' % (w, h, level, it['q'], r['sw']))
                if page.evaluate(FACE_JS):
                    fails.append('%dx%d %s %r: the answer card is clipped' % (w, h, level, it['q']))
            print('  fold %dx%d %-5s: Next ends by %d px, fold %d' % (w, h, level, worst, h - FOOTER))
            if page.__errors:
                fails.append('%dx%d %s page errors: %s' % (w, h, level, '; '.join(page.__errors[:3])))
            ctx.close()


def run(fails, html, parts=('bank', 'marking', 'levels', 'fold')):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    banks = {}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx, page = new_page(browser, base, html)
            open_level(page, base, 'gcse')
            banks = page.evaluate('() => JSON.parse(JSON.stringify(QUESTIONS))')
            if sorted(banks) != sorted(LEVELS):
                fails.append('QUESTIONS has levels %r' % sorted(banks))
                return banks
            if 'bank' in parts:
                for level in LEVELS:
                    check_bank(fails, level, banks[level])
                    for it in banks[level]:
                        r = page.evaluate(RENDER_JS, it)
                        if r['lines'] != len(it['w']) or r['katex'] != len(it['w']) or r['errors']:
                            fails.append('%s %r: KaTeX drew %r for %d working lines' % (level, it['q'], r, len(it['w'])))
            if 'marking' in parts:
                check_marking(fails, page, banks)
            if page.__errors:
                fails.append('page errors: %s' % '; '.join(page.__errors[:3]))
            ctx.close()
            if 'levels' in parts:
                for level in LEVELS:
                    ctx, page = new_page(browser, base, html)
                    check_level_page(fails, page, base, level, banks)
                    if page.__errors:
                        fails.append('?level=%s page errors: %s' % (level, '; '.join(page.__errors[:3])))
                    ctx.close()
            if 'fold' in parts:
                check_fold(fails, browser, base, html, banks)
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return banks


B = '\\\\'   # one backslash as the page's JavaScript source writes it
PLANTS = [
    ('a key changed by 1 (92 for 35% of 260)', 'key 92', ['bank'],
     '{"band": 1, "q": "What is 35% of 260?", "a": 91,', '{"band": 1, "q": "What is 35% of 260?", "a": 92,'),
    ('a duplicate question (KS3 "30% of 70" becomes "20% of 45")', 'repeated', ['bank'],
     '{"band": 1, "q": "What is 30% of 70?", "a": 21, "w": ["10' + B + '% = 7", "30' + B + '% = 7 ' + B + 'times 3 = 21"]}',
     '{"band": 1, "q": "What is 20% of 45?", "a": 9, "w": ["10' + B + '% = 4.5", "20' + B + '% = 4.5 ' + B + 'times 2 = 9"]}'),
    ('a working line that does not end with the key', 'does not end with', ['bank'],
     '"w": ["' + B + 'frac{18}{40} ' + B + 'times 100 = 45' + B + '%"]', '"w": ["45 = ' + B + 'frac{18}{40} ' + B + 'times 100"]'),
    ('a band served out of order', 'served bands', ['levels'],
     'const SERVE = [[1, 3], [2, 3], [3, 2], [4, 2]];', 'const SERVE = [[2, 3], [1, 3], [3, 2], [4, 2]];'),
    ('a pence key at 1 d.p. accepted as right', "'27.6'", ['marking'],
     "return q.u === '£' ? MaffsAnswer.money(raw, q.a) : MaffsAnswer.exact(raw, q.a);",
     "return MaffsAnswer.exact(raw, q.a, q.u === '£' ? {currency:'£'} : undefined);"),
    ('GCSE routed to the KS3 bank', 'another bank', ['levels'],
     'const POOL = QUESTIONS[gameLevel];', "const POOL = QUESTIONS[gameLevel === 'gcse' ? 'ks3' : gameLevel];"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    banks = run(fails, html)
    print('%s: %s questions; keys and working recomputed from the question text; KaTeX drawn; every item marked right and '
          'wrong; %d deals a level; routing and leaderboard by level; the fold at %s' % (
              SLUG, ' + '.join('%d %s' % (len(banks.get(k, [])), k) for k in LEVELS), DEALS,
              ', '.join('%dx%d' % s for s in FOLD_SIZES)))
    ok = True
    if not args.no_selftest and not args.against:
        for what, tag, parts, old, new in PLANTS:
            try:
                planted = pc.apply_plant(html, old, new, name=what)
            except pc.StalePlant as e:
                print('  self-test %-58s *** %s ***' % (what, e))
                ok = False
                continue
            rep = []
            err = None
            try:
                run(rep, planted, parts)
            except Exception as e:  # an error is never a catch (plant_common)
                err = e
            hit = [f for f in rep if tag in f]
            caught = pc.is_caught(hit, err)
            ok = ok and caught
            print('  self-test %-58s %s' % (what, ('caught: ' + hit[0][:110]) if caught else
                                            '*** MISSED ***' + (' (error: %s)' % err if err else '')))
    for f in fails[:40]:
        print('FAIL  ' + f[:400])
    if len(fails) > 40:
        print('FAIL  ... and %d more' % (len(fails) - 40))
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
