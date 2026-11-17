#!/usr/bin/env python3
# ci-line: Glorious Gantt's answer boxes (text boxes, never type="number"; every early time, late time, float and Gantt reading in the pool marked exactly as on the old number boxes for every string a number box can hold, and junk refused; NOT the game's verifier) |
# ci-deps: games/glorious-gantt/ schools/assets/answer.js
"""Glorious Gantt's typed answers after ANSWER-BOX-TEXT (contract ANSWER-BOX-TEXT, PR 2; Amendment 2, Jon 17 Nov 2026).

    python scripts/test-answer-box-gantt.py                # the check, then the planted faults
    python scripts/test-answer-box-gantt.py --no-selftest

THIS IS NOT GLORIOUS GANTT'S VERIFIER. It does not recompute a single key (no forward or backward pass, no float, no
critical path): it only proves that the change from number boxes to text boxes left the marking as it was. The game
has no verifier yet; this file does not meet canon SR-21's "verifier merged" condition for relisting it (Jon's ruling,
17 Nov 2026, Amendment 2: a narrow test, named so it is not taken for the verifier).

WHAT IT CHECKS, in Chromium:
  * the four boxes (early time, late time, float, a Gantt reading) are type="text" with inputmode="decimal", and no
    key in the pool is negative (so no minus key is needed);
  * PROOF of unchanged marking: every node's early and late time, every non-critical activity's float and every Gantt
    reading in the pool is played with the same typed strings on this page and on the OLD page (this page with the
    boxes set back to type="number" and the read back to plain parseInt, so the browser itself empties what a number
    box cannot hold). For every string a number box can hold ("7", "7.0", "2.5", "1e1", "-3", ".5"), the two give the
    same result: marked right, marked wrong or not marked. "2.5" is read as 2 on both (parseInt), as Jon ruled.
  * junk a number box cannot hold ("1,000", "12abc", "£5", "5 days") is refused by this page: not marked.
Planted faults (each must fail): a box back to type="number"; the junk check undone (parseInt on the raw string).
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'glorious-gantt'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
READ_NEW = 'function typedInt(raw){return MaffsAnswer.parse(raw)===null?NaN:parseInt(raw);}'
READ_OLD = 'function typedInt(raw){return parseInt(raw);}'
BOX_NEW = 'type="text" inputmode="decimal" class="num-input"'
BOX_OLD = 'type="number" class="num-input"'
JUNK = ['1,000', '12abc', '£5', '5 days']

PLAY_JS = r"""(junk) => {
  window.setTimeout = () => 0;
  const out = {boxes: {}, keys: [], marks: {}};
  const valid = k => [String(k), String(k + 1), String(Math.max(0, k - 1)), String(k) + '.0', String(k) + '.7', '2.5', '1e1', '0', '-3', '.5'];
  const mark = (id, check) => (typed) => {
    const b = document.getElementById(id); b.value = typed;
    const s = G.score, p = G.penalties; check();
    return G.score > s ? 'right' : G.penalties > p ? 'wrong' : 'not marked';
  };
  const seen = (id) => { const b = document.getElementById(id); out.boxes[id] = b ? [b.type, b.getAttribute('inputmode')] : ['missing', null]; };
  const all = Object.values(SCENARIOS).flat();
  all.forEach((q, qi) => {
    G.questions = [q]; G.qIdx = 0; loadScenario();
    const tag = (q.id || q.title || ('scenario ' + qi));
    q.nodes.forEach((n, ni) => {
      out.keys.push(n.early, n.late);
      const play = (render, id, check, key, what) => {
        const rows = [];
        for (const t of valid(key).concat(junk)) { render(); rows.push([t, mark(id, check)(t)]); }
        render(); seen(id);
        out.marks[tag + ' ' + what] = rows;
      };
      play(() => { G.earlyDone = {}; q.nodes.slice(0, ni).forEach(m => { G.earlyDone[m.id] = true; }); renderForwardPass(q); },
           'earlyInput', () => checkEarly(n.id), n.early, 'node ' + n.id + ' early');
      const rev = [...q.nodes].reverse(), ri = rev.indexOf(n);
      play(() => { G.lateDone = {}; rev.slice(0, ri).forEach(m => { G.lateDone[m.id] = true; }); renderBackwardPass(q); },
           'lateInput', () => checkLate(n.id), n.late, 'node ' + n.id + ' late');
    });
    const nonCrit = q.activities.filter(a => !q.criticalPath.includes(a.id));
    nonCrit.forEach((a, k) => {
      const key = q.floats[a.id]; out.keys.push(key);
      const rows = [];
      for (const t of valid(key).concat(junk)) { G.floatIdx = k; renderFloats(q); rows.push([t, mark('floatInput', () => checkFloat(a.id, key))(t)]); }
      G.floatIdx = k; renderFloats(q); seen('floatInput');
      out.marks[tag + ' float ' + a.id] = rows;
    });
    (q.ganttQs || []).forEach((gq, i) => {
      if (gq.type !== 'read') return;
      out.keys.push(gq.answer);
      const rows = [];
      for (const t of valid(gq.answer).concat(junk)) { G.gqIdx = i; renderGanttQs(q); rows.push([t, mark('gqInput', checkGQ_read)(t)]); }
      G.gqIdx = i; renderGanttQs(q); seen('gqInput');
      out.marks[tag + ' Gantt Q' + (i + 1)] = rows;
    });
  });
  return out;
}"""


def play(html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof SCENARIOS !== "undefined" && typeof checkEarly === "function"', timeout=15000)
            out = page.evaluate(PLAY_JS, JUNK)
            browser.close()
            out['errors'] = errors
            return out
    finally:
        proc.terminate()
        proc.wait()


def check(html):
    fails = []
    if html.count(READ_NEW) != 1 or html.count(BOX_NEW) != 4:
        fails.append('the old page cannot be rebuilt from this one (%d junk-check reads, %d text boxes; want 1 and 4): '
                     'the comparison below would prove nothing' % (html.count(READ_NEW), html.count(BOX_NEW)))
    new = play(html)
    old = play(html.replace(READ_NEW, READ_OLD).replace(BOX_NEW, BOX_OLD))
    fails += ['page error: %s' % e for e in new['errors']]
    for box, (typ, mode) in sorted(new['boxes'].items()):
        if typ != 'text' or mode != 'decimal':
            fails.append('%s: type="%s" inputmode="%s", not a text box with inputmode="decimal"' % (box, typ, mode))
    if set(new['boxes']) != {'earlyInput', 'lateInput', 'floatInput', 'gqInput'}:
        fails.append('boxes seen: %s, not the four' % sorted(new['boxes']))
    neg = [k for k in new['keys'] if k < 0]
    if neg:
        fails.append('%d keys are negative (%s): a minus key would be needed' % (len(neg), neg[:5]))
    n = 0
    for item, rows in new['marks'].items():
        before = dict(old['marks'].get(item, []))
        for typed, got in rows:
            n += 1
            if typed in JUNK:
                if got != 'not marked':
                    fails.append('%s: typed %r (no number) was marked %s' % (item, typed, got))
            elif got != before.get(typed):
                fails.append('%s: typed %r: now %s, on the old number box %s' % (item, typed, got, before.get(typed)))
    return fails, n, len(new['marks'])


PLANTS = [
    ('a box back to type="number"', 'type="text" inputmode="decimal" class="num-input" id="earlyInput"',
     'type="number" inputmode="decimal" class="num-input" id="earlyInput"',
     'earlyInput: type="number"'),
    ('the junk check undone (parseInt on the raw string)', READ_NEW, READ_OLD, 'no number) was marked'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    html = open(GAME, encoding='utf-8').read()
    fails, n, items = check(html)
    print('%s answer boxes: %d typed strings over %d answers (every early and late time, float and Gantt reading), each '
          'marked as on the old number box; junk refused' % (SLUG, n, items))
    ok = True
    if not args.no_selftest:
        for what, old, new, want in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-52s *** CANNOT PLANT (%d) ***' % (what, html.count(old)))
                ok = False
                continue
            got = [f for f in check(html.replace(old, new))[0] if want in f]
            ok = ok and bool(got)
            print('  self-test %-52s %s' % (what, ('caught: ' + got[0][:90]) if got else '*** MISSED ***'))
    for f in fails[:60]:
        print('FAIL  ' + f)
    if len(fails) > 60:
        print('FAIL  ... and %d more' % (len(fails) - 60))
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
