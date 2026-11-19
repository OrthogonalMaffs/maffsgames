#!/usr/bin/env python3
"""The Core Maths papers' deal, checked in Chromium (contract CORE-PAPERS-SHUFFLE, Jon, 19 Nov 2026).

Each of the four Core Maths paper verifiers imports this module and calls run(); it names no game itself, so a
change to one paper never selects the other three verifiers (ci-deps.py follows imports and reads literals).

Every play deals each section's questions in a new order, the sections in place and in their sizes, and each
question's options in a new order through MaffsOptions; an option's dataset.val is its index in q.options, and
marking compares that value with the key (or the item's accept list), never the button's position. Over SESSIONS
real sessions (startGame()), checked:

  - every question exactly once, inside its own section (the sections are the bank's own runs of q.section, in
    source order, and must match the page's SECTIONS/SECTION_STARTS where it has them); each section's order
    differs between sessions;
  - each question's options are a permutation of its source options (values 0..n-1, each drawn with its own
    text, lettered A, B, C, D by position), in more than one order across the sessions; the key lands in each of
    A-D somewhere on the paper;
  - every option clicked: marked right exactly when its value is the key or in the item's accept list;
  - question_answered carries question_index (the position, 1-based) and question_id, the source id
    "<prefix>-qNN" of the question shown, the same in every session;
  - "Q n of 36" counts positions, and the results screen's section scores count the dealt sections.

plants(html) returns the faults the self-test plants: options not shuffled; a question dealt into another
section; marking by position; question_id from the position. Each must FAIL.
"""
import re

import bank_common as bc

SESSIONS = 20
TAG = 'deal'

PLAY_JS = r"""([sessions, mathtext]) => {
  window.setTimeout = () => 0;            // no banner or Next timers: the sweep drives the page itself
  const sent = [];
  window.mfg = function (ev, p) { if (ev === 'question_answered') sent.push(Object.assign({}, p)); };
  const R = mathtext ? (o => MaffsText.html(o)) : (o => o);
  const norm = h => { const d = document.createElement('div'); d.innerHTML = h; return d.innerHTML; };
  const area = () => { document.getElementById('sectionBanner').style.display = 'none';
                       document.getElementById('questionArea').style.display = 'block'; };
  const out = {sessions: [], sections: null, results: null};
  if (typeof SECTIONS !== 'undefined' && typeof SECTION_STARTS !== 'undefined')
    out.sections = SECTIONS.map((s, i) => [SECTION_STARTS[i], s.count]);
  for (let s = 0; s < sessions; s++) {
    startGame(); area();
    const ses = {paper: PAPER.slice(), qs: []};
    for (let n = 0; n < PAPER.length; n++) {
      currentQ = n; answers = []; score = 0;
      showQuestion();
      const src = PAPER[n], q = QUESTIONS[src], ok = q.accept || [q.correct];
      const btns = [...document.querySelectorAll('#optionsContainer .option-btn')];
      const rec = {src: src, counter: document.getElementById('qCounter').textContent,
                   vals: btns.map(b => b.dataset.val),
                   letters: btns.map(b => b.querySelector('.option-letter').textContent),
                   textOk: btns.every(b => b.querySelector('.option-text').innerHTML === norm(R(q.options[+b.dataset.val]))),
                   marks: [], sent: null};
      for (let v = 0; v < q.options.length; v++) {
        currentQ = n; answers = []; score = 0;
        showQuestion();
        const b = [...document.querySelectorAll('#optionsContainer .option-btn')].find(x => x.dataset.val === String(v));
        if (!b) { rec.marks.push([v, 'not on screen']); continue; }
        sent.length = 0;
        b.click();
        const right = b.classList.contains('correct') && answers[0] === true;
        if (right !== ok.includes(v)) rec.marks.push([v, right ? 'marked right' : 'marked wrong']);
        if (v === q.correct) rec.sent = sent.slice();
      }
      ses.qs.push(rec);
    }
    out.sessions.push(ses);
  }
  // One full session: the key on every question of the first section, a wrong option everywhere else.
  startGame(); area();
  const firstSec = QUESTIONS[PAPER[0]].section;
  for (let n = 0; n < PAPER.length; n++) {
    currentQ = n; showQuestion();
    const q = QUESTIONS[PAPER[n]], ok = q.accept || [q.correct];
    const want = q.section === firstSec;
    const b = [...document.querySelectorAll('#optionsContainer .option-btn')]
      .find(x => ok.includes(+x.dataset.val) === want);
    b.click();
  }
  showResults();
  out.results = {final: document.getElementById('finalScore').textContent,
                 scores: [...document.querySelectorAll('[id^="s"][id$="Score"]')].filter(e => /^s\d+Score$/.test(e.id))
                   .map(e => e.textContent)};
  return out;
}"""


def runs(bank):
    """[(section, start, count)]: the bank's own runs of q.section, in source order."""
    out = []
    for i, q in enumerate(bank):
        if out and out[-1][0] == q['section']:
            out[-1][2] += 1
        else:
            out.append([q['section'], i, 1])
    return [tuple(r) for r in out]


def check(fails, bank, res, prefix):
    secs = runs(bank)
    if len({s for s, _, _ in secs}) != len(secs):
        fails.append('%s: a section is split in the bank %s' % (TAG, [(s, c) for s, _, c in secs]))
        return
    if res['sections'] is not None and [list(x) for x in res['sections']] != [[st, c] for _, st, c in secs]:
        fails.append('%s: the page\'s sections %s are not the bank\'s %s' % (TAG, res['sections'], [(st, c) for _, st, c in secs]))
    total = len(bank)
    seen_orders = {s: set() for s, _, _ in secs}
    opt_orders = {i: set() for i in range(total)}
    key_pos = set()
    for k, ses in enumerate(res['sessions'], 1):
        paper = ses['paper']
        if sorted(paper) != list(range(total)):
            fails.append('%s: session %d does not deal every question exactly once (%d dealt)' % (TAG, k, len(paper)))
            continue
        for s, st, c in secs:
            part = paper[st:st + c]
            out = [i + 1 for i in part if not st <= i < st + c]
            if out:
                fails.append('%s: session %d dealt Q%s into section %s (positions %d-%d)'
                             % (TAG, k, ','.join(map(str, out)), s, st + 1, st + c))
            seen_orders[s].add(tuple(part))
        for n, r in enumerate(ses['qs']):
            q = bank[r['src']]
            w = '%s: session %d, position %d (Q%d)' % (TAG, k, n + 1, r['src'] + 1)
            m = len(q['options'])
            if r['counter'] != 'Q%d of %d' % (n + 1, total):
                fails.append('%s: the counter reads %r' % (w, r['counter']))
            if sorted(r['vals']) != [str(i) for i in range(m)]:
                fails.append('%s: options %s are not a permutation of the source options' % (w, r['vals']))
                continue
            if not r['textOk']:
                fails.append('%s: an option is drawn with another option\'s text' % w)
            if r['letters'] != list('ABCD'[:m]):
                fails.append('%s: letters %s' % (w, r['letters']))
            opt_orders[r['src']].add(tuple(r['vals']))
            key_pos.add(r['vals'].index(str(q['correct'])))
            for v, what in r['marks']:
                fails.append('%s: option value %d %s' % (w, v, what))
            want = '%s-q%02d' % (prefix, r['src'] + 1)
            sent = r['sent'] or []
            if len(sent) != 1:
                fails.append('%s: %d question_answered events for one answer' % (w, len(sent)))
            elif sent[0].get('question_id') != want or sent[0].get('question_index') != n + 1:
                fails.append('%s: question_answered sent question_id %r, question_index %r (expected %r, %d)'
                             % (w, sent[0].get('question_id'), sent[0].get('question_index'), want, n + 1))
    if len(res['sessions']) > 1:
        for s, st, c in secs:
            if c > 1 and len(seen_orders[s]) < 2:
                fails.append('%s: section %s was dealt in the same order in all %d sessions' % (TAG, s, len(res['sessions'])))
        same = [i + 1 for i in range(total) if len(opt_orders[i]) < 2]
        if same:
            fails.append('%s: options not shuffled: Q%s drawn in one order in all %d sessions'
                         % (TAG, ','.join(map(str, same[:8])) + ('...' if len(same) > 8 else ''), len(res['sessions'])))
        if key_pos != {0, 1, 2, 3}:
            fails.append('%s: the key never landed at %s' % (TAG, ', '.join('ABCD'[i] for i in range(4) if i not in key_pos)))
    s0, _, c0 = secs[0]
    want = ['%d / %d' % (c0, c0)] + ['0 / %d' % c for _, _, c in secs[1:]]
    if res['results']['scores'] != want or res['results']['final'] != '%d / %d' % (c0, total):
        fails.append('%s: results after keying section %s only: %s %s (expected %s %s)'
                     % (TAG, s0, res['results']['final'], res['results']['scores'], '%d / %d' % (c0, total), want))


def play(html, slug, mathtext=False, sessions=SESSIONS):
    """Serve html as the game's page and run PLAY_JS; returns (bank, result, page errors)."""
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % re.escape(slug))
            ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=deal' % slug, wait_until='load', timeout=20000)
            page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof dealPaper === "function"', timeout=15000)
            bank = page.evaluate('() => JSON.parse(JSON.stringify(QUESTIONS))')
            res = page.evaluate(PLAY_JS, [sessions, mathtext])
            browser.close()
            return bank, res, errors
    finally:
        proc.terminate()
        proc.wait()


def checked(html, slug, prefix, mathtext=False):
    fails = []
    bank, res, errors = play(html, slug, mathtext)
    if errors:
        fails.append('%s: page errors: %s' % (TAG, '; '.join(errors[:3])))
    check(fails, bank, res, prefix)
    return fails


# (name, regex on the page, replacement): each must make check() FAIL.
PLANTS = [
    ('options not shuffled',
     r'return MaffsOptions\.build\(q\.correct, others, \{ max: q\.options\.length \}\);',
     'return q.options.map(function (_, i) { return i; });'),
    ('a question dealt into another section',
     r'(PAPER = PAPER\.concat\(MaffsOptions\.shuffle\(ids\)\);\n  \}\);\n)',
     r'\1  PAPER.push(PAPER.shift());\n'),
    ('marking by position',
     r'selectAnswer\(parseInt\(this\.dataset\.val, ?10\)\)',
     'selectAnswer(pos)'),
    ('question_id from the position',
     r'question_id: ?questionId\(PAPER\[currentQ\]\)',
     'question_id: questionId(currentQ)'),
]


def run(html, slug, prefix, mathtext=False, selftest=True):
    """Print the deal check and its self-test; return True when it passes and every plant fails."""
    fails = checked(html, slug, prefix, mathtext)
    print('%s: the deal, %d sessions in Chromium: %s' % (slug, SESSIONS, 'PASS' if not fails else '%d FAIL(s)' % len(fails)))
    for f in fails[:40]:
        print('FAIL  ' + f)
    ok = not fails
    if selftest:
        for name, rx, rep in PLANTS:
            planted, n = re.subn(rx, rep, html)
            if n != 1:
                print('  self-test (deal) %-38s *** CANNOT PLANT (%d) ***' % (name, n))
                ok = False
                continue
            hit = checked(planted, slug, prefix, mathtext)
            ok = ok and bool(hit)
            print('  self-test (deal) %-38s %s' % (name, ('caught: ' + hit[0][:110]) if hit else '*** MISSED ***'))
    return ok
