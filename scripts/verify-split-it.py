#!/usr/bin/env python3
# ci-line: Split It (every generator's keys recomputed + marking at the stated precision) |
"""Independent verification of split-it's keys and its marking (todo §1.36, canon §7.1.3).

Until Oct 2026 split-it marked single and share answers to ±0.05 (so £12.30 and £12.38 both
passed for £12.34) and recipes to ±0.15 (2.4 passed for 2.5); its GCSE recipes scale by 5/3 and
were keyed to 1 d.p. without the question saying so; its speed questions could have recurring
answers with no precision stated; a typed £ or € emptied the type="number" input; and Best Value
could draw two packs at the same unit price.

Every generator is run on the page itself (seeded Math.random), at both levels, many times:
  - KEYS: each key is recomputed from the numbers in the prompt (exact fractions). If the prompt
    states a precision ("Give your answer(s) to 1 decimal place"), the key must be the exact value
    rounded half up to it; if it states none, the exact value must terminate (at most 2 d.p. for
    money, otherwise a value the student can write exactly) and the key must equal it. Best Value:
    the two unit prices, each rounded to the nearest penny, differ by at least 1p, and the key is
    the cheaper pack. Recipes (canon SR-10): every whole-item ingredient (one with no unit, e.g.
    eggs) scales to a whole number; the GCSE Pancakes recipe once asked for 3.3 eggs (todo §1.47).
  - MARKING: a sample of every question type is rendered and answered through checkAnswer(),
    one input at a time (the others correct). Money (a £ or € amount): the key at 2 d.p., a
    whole-pound key also as an integer, and with a leading £/€, are correct; 1p and 4p off are
    wrong; the right amount wrongly written is 'format'. Stated precision: the key (and with a
    trailing zero) is correct; 0.1 off is wrong; the unrounded value is 'format'. Exact answers:
    the key (and with .0) is correct; 0.01, 0.1 and 1 off are wrong. 'format' and 'unreadable'
    record nothing (no score, no penalty, no event) and show MaffsAnswer's words, with the
    student's figure and currency.

    python scripts/verify-split-it.py [--file PATH] [--per N] [--sample N] [--verbose]

--file checks another copy of the page (served in place of the real one), e.g. the file on main.
"""
import argparse
import os
import re
import sys
from collections import defaultdict
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'split-it'
PAGE = os.path.join(bc.GAMES_DIR, SLUG, 'index.html')
MODES = ['simplify', 'equivalent', 'divide', 'fractions', 'scale', 'unitary']
LEVELS = ['ks3', 'gcse']
UNREADABLE_MSG = 'Type just the number, e.g. 12.34'
DP_RE = re.compile(r'Give your answers? to (\d+) decimal places?', re.I)

SEEDED = """(seed) => {
  let a = seed >>> 0;
  Math.random = function () {           // mulberry32
    a = (a + 0x6D2B79F5) >>> 0; let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}"""

GENERATE = """([mode, level, n, seed]) => {
  (%s)(seed);
  const out = [];
  for (let i = 0; i < n; i++) {
    const q = generators[mode](level);
    out.push(Object.assign({}, q, {items: q.items || null, mode, level}));
  }
  return out;
}""" % SEEDED

# One question, many probes: render it, then for each probe fill the inputs, press Check and
# read what happened, all in one page task (the page's timers are stubbed out, see SETUP).
PROBE = """([q, probes]) => {
  const out = [];
  for (const p of probes) {
    renderQ(q); S._currentQ = q; $('fbArea').innerHTML = '';
    p.values.forEach((v, i) => { $('in' + i).value = v; });
    const before = {c: S.correct, p: S.penalties, e: window.__qa.length};
    checkAnswer();
    const fb = $('fbArea').querySelector('.feedback');
    out.push({c: S.correct - before.c, p: S.penalties - before.p, e: window.__qa.length - before.e,
              fbClass: fb ? fb.className : '', fbText: fb ? fb.textContent : '',
              typed: p.values.map((_, i) => $('in' + i).value)});
  }
  return out;
}"""

SETUP = """() => {
  window.setTimeout = function () { return 0; };   // no advance, no dismiss button, no endGame
  window.__qa = [];
  const o = window.mfg;
  window.mfg = function (name) { if (name === 'question_answered') window.__qa.push(arguments[1]);
                                 return o ? o.apply(this, arguments) : undefined; };
  S.mode = 'verify'; S.level = 'verify'; S.qIdx = 0; S.total = 1e9;
}"""


# --- exact arithmetic -------------------------------------------------------------------------

def half_up(x, dp):
    s = F(10) ** dp
    sign = -1 if x < 0 else 1
    return sign * F(int(abs(x) * s + F(1, 2)), s)


def terminating_dp(x):
    """Decimal places x needs, or None if its decimal never ends."""
    d = x.denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    if d != 1:
        return None
    n = 0
    while (x * 10 ** n).denominator != 1:
        n += 1
    return n


def fmt(x, dp):
    s = F(10) ** dp
    v = int(abs(x) * s)
    assert v == abs(x) * s, (x, dp)
    sign = '-' if x < 0 else ''
    return sign + (f'{v // 10 ** dp}.{v % 10 ** dp:0{dp}d}' if dp else str(v))


def text_of(prompt):
    t = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', prompt.replace('<br>', ' '))).strip()
    return re.sub(r' ([,.?])', r'\1', t)


def nums(s):
    return [int(n) for n in re.findall(r'\d+', s)]


# --- what each question asks, recomputed from its prompt ----------------------------------------

def expected(q):
    """(kind, exact answers, extra) where kind is 'money', 'exact', 'bestvalue' or 'fraction',
    or raises ValueError for a prompt this script cannot read."""
    t = text_of(q['prompt'])
    m = re.match(r'Write ([\d : ]+?) in its simplest form', t)
    if m:
        parts = nums(m.group(1))
        g = 0
        for p in parts:
            g = __import__('math').gcd(g, p)
        return 'exact', [F(p, g) for p in parts], None
    m = re.match(r'(\d+) : (\d+) = ?(\d+|\?) : ?(\d+|\?)$', t)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        if m.group(4) == '?':
            return 'exact', [F(b * int(m.group(3)), a)], None
        return 'exact', [F(a * int(m.group(4)), b)], None
    m = re.match(r'If (\d+) : (\d+) = x : (\d+), find x', t)
    if m:
        a, b, c = map(int, m.groups())
        return 'exact', [F(a * c, b)], None
    m = re.match(r'(?:Share|Divide) (£)?(\d+)(?: \w+)? in the ratio ([\d : ]+)$', t)
    if m:
        amt, parts = int(m.group(2)), nums(m.group(3))
        ans = [F(amt * p, sum(parts)) for p in parts]
        return ('money', ans, '£') if m.group(1) else ('exact', ans, None)
    m = re.match(r'In the ratio ([\d : ]+), what fraction of the total is the (smaller|larger|largest) part', t)
    if m:
        parts = nums(m.group(1))
        pick = min(parts) if m.group(2) == 'smaller' else max(parts)
        return 'fraction', [F(pick, sum(parts))], None
    m = re.search(r'recipe for (\d+) \w+ uses .* for (\d+) \w+\?', t)
    if m:
        n0, n1 = int(m.group(1)), int(m.group(2))
        return 'exact', [F(it['v']) * n1 / n0 for it in q['items']], None
    m = re.match(r'(\d+) (\w+) cost £([\d.]+)\. How much do (\d+) \w+ cost\?', t)
    if m:
        n, cost, k = int(m.group(1)), F(m.group(3)), int(m.group(4))
        return 'money', [cost / n * k], '£'
    m = re.match(r'£1 = €([\d.]+)\. Convert £(\d+) to euros\.', t)
    if m:
        return 'money', [F(m.group(1)) * int(m.group(2))], '€'
    # SR-17 (SWEEP-1, split-it-s1-001): the key assumes the same speed, so the question says so; a speed
    # question without it is unreadable here, and fails.
    m = re.match(r'A car travels (\d+) miles in (\d+) hours\. At the same speed, how far in (\d+) hours\?', t)
    if m:
        d, h, h2 = map(int, m.groups())
        return 'exact', [F(d * h2, h)], None
    m = re.match(r'Pack A: (\d+) for £([\d.]+)\. Pack B: (\d+) for £([\d.]+)\. Which is better value\?', t)
    if m:
        nA, pA, nB, pB = int(m.group(1)), F(m.group(2)), int(m.group(3)), F(m.group(4))
        return 'bestvalue', [half_up(pA / nA, 2), half_up(pB / nB, 2)], None
    raise ValueError('unreadable prompt: ' + t)


def check_wording(q, rep):
    """R1, R3 (SWEEP-1 split-it-s1-003 to -008): the part asked for exists and is unique, no question asks for the
    amount it has just given, a recipe is scaled in units that fit it, whole items are said to be whole, no ASCII
    fraction in the working, and a rounded value is not written with an equals sign."""
    t = text_of(q['prompt'])
    where = f"{q['mode']}/{q['level']}"
    bad = []
    m = re.match(r'In the ratio ([\d : ]+), what fraction of the total is the (smaller|larger|largest) part', t)
    if m:
        parts = nums(m.group(1))
        pick = min(parts) if m.group(2) == 'smaller' else max(parts)
        if parts.count(pick) != 1:
            bad.append(f'"the {m.group(2)} part" of {m.group(1)} is not one part')
    m = re.match(r'(\d+) \w+ cost £([\d.]+)\. How much do (\d+) \w+ cost\?', t)
    if m and m.group(1) == m.group(3):
        bad.append(f'asks for the cost of the {m.group(3)} just given: {t}')
    m = re.match(r'A car travels (\d+) miles in (\d+) hours\. At the same speed, how far in (\d+) hours\?', t)
    if m:
        d, h, h2 = map(int, m.groups())
        if h == h2:
            bad.append(f'asks for the distance in the {h} hours just given: {t}')
        exact = (10 * d * h2) % h == 0
        sign = re.search(r'([=≈]) [\d.]+ miles', q['working'])
        if not sign or sign.group(1) != ('=' if exact else '≈'):
            bad.append(f'the speed working writes {sign and sign.group(1)} for a value that is {"exact" if exact else "rounded"}: {q["working"]}')
    m = re.search(r'A (.+?) recipe for (\d+) (\w+) uses', t)
    if m:
        if m.group(1) == 'Concrete mix' and m.group(3) == 'people':
            bad.append('a concrete mix is scaled "for people"')
        whole = [i['n'].lower() for i in q['items'] if i.get('whole')]
        said = re.search(r'\((.+?) (?:is|are) whole numbers?\)', t)
        if whole and 'decimal place' in t and not (said and said.group(1) == ' and '.join(whole)):
            bad.append(f'the whole-number ingredient {whole} is asked "to 1 decimal place" with no word that it is whole: {t}')
        if not whole and said:
            bad.append(f'a recipe with no whole item says one is: {t}')
        if re.search(r'Scale factor = \d+/\d+', q['working']):
            bad.append(f'the working writes the scale factor with an ASCII slash: {q["working"]}')
    for b in bad:
        rep[(where, 'wording')].append(b)


def check_key(q, rep):
    check_wording(q, rep)
    t = text_of(q['prompt'])
    where = f"{q['mode']}/{q['level']}"
    try:
        kind, exact, cur = expected(q)
    except ValueError as e:
        rep[(where, 'prompt')].append(str(e))
        return None
    if kind == 'bestvalue':
        ua, ub = exact
        if abs(ua - ub) < F(1, 100):
            rep[(where, 'best value: unit prices less than 1p apart')].append(t)
        elif q['answers'] != ['A' if ua < ub else 'B']:
            rep[(where, 'best value: key is not the cheaper pack')].append(t)
        return None
    if kind == 'fraction':
        x = exact[0]
        if q['answers'] != [x.numerator, x.denominator]:
            rep[(where, 'fraction key')].append(f'{t} keyed {q["answers"]}, expected {x}')
        return None
    # SR-10 (Jon, 3 Oct 2026): a whole-item ingredient (one with no unit: eggs) is only scaled
    # by a whole number, so its scaled amount is a whole number. Read from the unit, not from the
    # page's own `whole` flag, so a recipe that forgets the flag is still caught.
    for i, it in enumerate(q.get('items') or []):
        if it.get('u', '') == '' and exact[i].denominator != 1:
            rep[(where, 'whole-item ingredient scaled to a fraction (SR-10)')].append(
                f'{t} -> {it["n"]} {float(exact[i]):g}')
    m = DP_RE.search(t)
    dp = int(m.group(1)) if m else None
    keys = []
    for i, x in enumerate(exact):
        if dp is not None:
            want = half_up(x, dp)
        else:
            need = terminating_dp(x)
            if need is None or (kind == 'money' and need > 2):
                rep[(where, 'precision not stated, and the answer does not terminate' if need is None
                     else 'money answer below a penny')].append(f'{t} -> {float(x)}')
                return None
            want = x
        got = q['answers'][i]
        if abs(F(got) - want) > F(1, 10 ** 9):
            what = ('key rounded, but the prompt states no precision' if dp is None and abs(F(got) - half_up(x, 1)) < F(1, 10 ** 9)
                    else 'key differs from the recomputed answer')
            rep[(where, what)].append(f'{t} [{i}] keyed {got}, expected {want}')
            return None
        keys.append(want)
    return kind, keys, cur, dp, exact


# --- marking probes ------------------------------------------------------------------------------

def probes_for(kind, key, cur, dp, exact):
    """[(label, raw, expected outcome)] for one input."""
    out = []
    if kind == 'money':
        p2 = fmt(key, 2)
        out += [('2 d.p.', p2, 'correct'), (cur + ' prefix', cur + p2, 'correct'),
                ('1p over', fmt(key + F(1, 100), 2), 'wrong'), ('1p under', fmt(key - F(1, 100), 2), 'wrong'),
                ('4p over', fmt(key + F(4, 100), 2), 'wrong')]
        if key.denominator == 1:
            out += [('whole pounds', fmt(key, 0), 'correct'), ('1 d.p. form', fmt(key, 1), 'format')]
        else:
            out += [('3 d.p. form', fmt(key, 3), 'format')]
            if (key * 10).denominator == 1:
                out += [('1 d.p. form', fmt(key, 1), 'format')]
        out += [('unreadable', p2 + 'p', 'unreadable')]
    elif dp is not None:
        k = fmt(key, dp)
        out += [('stated d.p.', k, 'correct'), ('trailing zero', fmt(key, dp + 1), 'correct'),
                ('0.1 over', fmt(key + F(1, 10 ** dp), dp), 'wrong'),
                ('0.1 under', fmt(key - F(1, 10 ** dp), dp), 'wrong')]
        if exact != key:
            unrounded = half_up(exact, dp + 2)
            out += [('unrounded', fmt(unrounded, dp + 2), 'format')]
        else:
            out += [('unrounded', fmt(key + F(4, 10 ** (dp + 2)), dp + 2), 'format')]
    else:
        need = terminating_dp(key)
        out += [('exact', fmt(key, need), 'correct'), ('exact + .0', fmt(key, need + 1), 'correct'),
                ('0.01 over', fmt(key + F(1, 100), max(need, 2)), 'wrong'),
                ('0.1 over', fmt(key + F(1, 10), max(need, 1)), 'wrong'),
                ('1 over', fmt(key + 1, need), 'wrong')]
    return out


def outcome(r):
    if r['c'] == 1 and r['e'] == 1 and r['p'] == 0:
        return 'correct'
    if r['p'] == 1 and r['e'] == 1 and r['c'] == 0:
        return 'wrong'
    if r['c'] == 0 and r['p'] == 0 and r['e'] == 0:
        if 'format' in r['fbClass']:
            return 'format'
        if r['fbText'] == UNREADABLE_MSG:
            return 'unreadable'
        return 'nothing shown' if not r['fbText'] else 'unmarked: ' + r['fbText'][:60]
    return f"inconsistent (correct {r['c']}, penalties {r['p']}, events {r['e']})"


MARKED = defaultdict(int)
# Every rule must actually be exercised, or a PASS says nothing about it.
MUST_MARK = {
    ('divide/ks3', 'money £'), ('unitary/ks3', 'money £'), ('unitary/gcse', 'money €'),
    ('unitary/gcse', '1 d.p.'), ('scale/gcse', '1 d.p.'), ('scale/ks3', 'exact'),
    ('divide/ks3', 'exact'), ('divide/gcse', 'exact'), ('simplify/ks3', 'exact'),
    ('simplify/gcse', 'exact'), ('equivalent/ks3', 'exact'), ('equivalent/gcse', 'exact'),
}


def rule_of(q, keyinfo):
    kind, _keys, cur, dp, _exact = keyinfo
    return (f"{q['mode']}/{q['level']}",
            f'money {cur}' if kind == 'money' else f'{dp} d.p.' if dp is not None else 'exact')


def check_marking(page, q, keyinfo, rep):
    kind, keys, cur, dp, exact = keyinfo
    where = f"{q['mode']}/{q['level']}"
    MARKED[rule_of(q, keyinfo)] += 1
    base = [fmt(k, 2) if kind == 'money' else fmt(k, dp) if dp is not None else fmt(k, terminating_dp(k))
            for k in keys]
    jobs = []
    for i, k in enumerate(keys):
        for label, raw, want in probes_for(kind, k, cur, dp, exact[i]):
            vals = list(base)
            vals[i] = raw
            jobs.append((label, raw, want, vals))
    res = page.evaluate(PROBE, [q, [{'values': v} for _, _, _, v in jobs]])
    for (label, raw, want, _), r in zip(jobs, res):
        got = outcome(r)
        if got != want:
            rep[(where, f'marking: {label} should be {want}')].append(
                f'{text_of(q["prompt"])[:70]} | typed {raw!r} (input holds {r["typed"]}) -> {got}')
        elif got == 'format':
            fig = raw[1:] if raw[:1] in '£€' else raw
            if kind == 'money':
                need = f'{cur}{fig} loses the mark'
            else:
                need = f'asks for {dp} decimal place'
            if need not in r['fbText'] or fig not in r['fbText']:
                rep[(where, 'format message')].append(f'typed {raw!r}: {r["fbText"][:110]}')


def run(args):
    from playwright.sync_api import sync_playwright
    rep = defaultdict(list)
    counts = defaultdict(int)
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            if args.file:
                body = open(args.file, encoding='utf-8').read()
                page.route(f'**/games/{SLUG}/', lambda route: route.fulfill(
                    status=200, content_type='text/html; charset=utf-8', body=body))
            page.goto(f'{base.rstrip("/")}/games/{SLUG}/')
            page.evaluate(SETUP)
            for mode in MODES:
                for level in LEVELS:
                    qs = page.evaluate(GENERATE, [mode, level, args.per, 1000 + 17 * MODES.index(mode) + LEVELS.index(level)])
                    seen = set()
                    for q in qs:
                        counts[f'{mode}/{level}'] += 1
                        info = check_key(q, rep)
                        sig = text_of(q['prompt'])
                        if info is None or sig in seen:
                            continue
                        seen.add(sig)
                        # up to --sample distinct questions per marking rule, so a rare sub-type
                        # (a £ share, a speed question) is probed as often as a common one
                        if MARKED[rule_of(q, info)] < args.sample:
                            check_marking(page, q, info, rep)
            browser.close()
            for e in errors:
                rep[('page', 'script error')].append(e)
    finally:
        proc.terminate()
        proc.wait()
    return rep, counts


# (what is planted, today's text in the page, the fault). Each must make the check FAIL.
PLANTS = [
    ('equal parts in a Foundation fraction', 'let b=rInt(1,6);if(b>=a)b++;', 'let b=rInt(1,7);'),
    ('a tied largest part at GCSE', 'const L=rInt(2,5),u=rInt(1,L-1),w=rInt(1,L-1);', 'const L=rInt(2,5),u=rInt(1,L),w=rInt(1,L);'),
    ('a unitary question for the amount just given', 'let m=rInt(2,11);if(m>=n)m++;', 'let m=rInt(2,12);'),
    ('a speed question for the hours just given', 'let t2=rInt(2,7);if(t2>=t)t2++;', 'let t2=rInt(2,8);'),
    ('a concrete mix scaled for people', "{name:'Concrete mix',who:'wheelbarrows',items:", "{name:'Concrete mix',items:"),
    ('an ASCII slash in the scale working', 'Scale factor = ${F(target,orig)} = ${sf}', 'Scale factor = ${target}/${orig} = ${sf}'),
    ('a rounded speed written with =', "${(10*d*t2)%t===0?'=':'≈'}", '='),
    ('eggs asked to 1 d.p. with no word that they are whole',
     "${r.items.some(i=>i.whole)?` (${r.items.filter(i=>i.whole).map(i=>i.n.toLowerCase()).join(' and ')} are whole numbers)`:''}", ''),
]


def selftest(args):
    import tempfile
    html = open(PAGE, encoding='utf-8').read()
    ok = True
    for what, today, fault in PLANTS:
        if html.count(today) != 1:
            print(f'  self-test {what}: *** CANNOT PLANT ({html.count(today)}) ***')
            ok = False
            continue
        with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8', newline='') as f:
            f.write(html.replace(today, fault))
        try:
            rep, _ = run(argparse.Namespace(file=f.name, per=300, sample=1, verbose=False))
        finally:
            os.unlink(f.name)
        hit = bool(rep)
        ok = ok and hit
        print(f'  self-test {what}: ' + ('caught' if hit else '*** MISSED ***'))
    return ok


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--file', help='check this copy of the page instead of the repo file')
    ap.add_argument('--per', type=int, default=1500, help='questions generated per mode and level')
    ap.add_argument('--sample', type=int, default=25, help='distinct questions marked per mode and level')
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--no-selftest', action='store_true')
    args = ap.parse_args()
    rep, counts = run(args)
    total = sum(counts.values())
    for need in sorted(MUST_MARK - set(MARKED)):
        rep[(need[0], f'marking never exercised for {need[1]} answers')].append('raise --per or --sample')
    if args.verbose:
        for k, n in sorted(counts.items()):
            print(f'ok      {k}: {n} generated')
        for (w, r), n in sorted(MARKED.items()):
            print(f'marked  {w} {r}: {n} questions')
    if rep:
        for (where, what), ex in sorted(rep.items()):
            print(f'FAIL    {where}: {what} ({len(ex)}), e.g. {ex[0]}')
        print(f'\nFAILED: {len(rep)} finding(s) over {total} generated questions')
        return 1
    print(f'PASS: {total} generated questions (6 modes x 2 levels), every key recomputed; '
          f'marking probed on a sample of every type')
    if not args.file and not args.no_selftest:
        print('\nFault-injection self-test (planted in copies of the page; the file is never touched):')
        if not selftest(args):
            print('FAIL    self-test: a planted fault was not caught')
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
