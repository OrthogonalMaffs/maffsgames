#!/usr/bin/env python3
# ci-line: Wrong on the Internet (every convention a key needs stated in its post; Jon's rulings on the wheel and independence; every option marked in Chromium) |
"""Wrong on the Internet: no key depends on something its post does not say.

Each item shows a social-media post with a maths error; stage 1 asks for the right answer, stage 2 for what the
poster got wrong (45 items: ks3, gcse, core). The tranche 2 audit of 6 Oct 2026 found two keys resting on a
convention the post never stated, so a "depends" option was the right one (contract LISTED-HIGH, Jon's
rulings, 9 Oct 2026):
  wrong-on-the-internet-t2-001  gcse_004, roulette keyed 18/38 (an American wheel); a European wheel gives
                                18/37. Ruling: the post states a European single-zero wheel; the key is 18/37,
                                and "Depends on wheel" stays only if plainly wrong once the wheel is stated (it
                                is replaced by "P(black) = 1/2 every spin", the zero ignored).
  wrong-on-the-internet-t2-002  gcse_011, keyed "0.12 (if independent)" with independence never stated, and a
                                stage-2 key saying addition gives P(A OR B) (true only for mutually exclusive
                                events). Ruling: the post states that A and B are independent; 0.12 stands and
                                "Need more information" is wrong.

Checks, every item: no stage-1 key carries a condition of its own, "(if ...)" (a convention the post must state
instead); a post about roulette states its wheel, and its keys use that wheel's P(black) (18/37 with one zero,
18/38 with two); no item says addition gives P(A OR B) or "OR = add"; RULED pins the two rulings' words. In
Chromium (390x844) every stage-1 and stage-2 option of every item is clicked through the game's own handlers,
the mark read from the button: exactly the key right. A self-test plants both items as they were on main;
each must FAIL naming its item.

    python scripts/verify-wrong-on-the-internet.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'wrong-on-the-internet'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
# Jon's rulings (LISTED-HIGH): (words the post must carry, the stage-1 key, options that must not be offered).
RULED = {
    'woti_gcse_004': ('European roulette wheel (one green zero)', 'P(black) = 18/37 every spin', ['Depends on wheel']),
    'woti_gcse_011': ('A and B are independent.', '0.12', []),
}
WHEELS = {'one green zero': '18/37', 'single-zero': '18/37', 'two green zeros': '18/38', 'double-zero': '18/38',
          'American': '18/38', 'European': '18/37'}


def texts(q):
    post = q['post']
    return [post.get('text', ''), post.get('pollCaption', '')] + [r['text'] for r in post.get('replies', [])] \
        + list(q['stage1Options']) + [o['text'] for o in q['stage2Options']] + [q.get('explanation', '')]


def check_bank(fails, bank):
    for lv, items in bank.items():
        for q in items:
            w = q['id']
            allt = ' '.join(texts(q))
            key = q['stage1CorrectAnswer']
            if key not in q['stage1Options'] or len(set(q['stage1Options'])) != len(q['stage1Options']):
                fails.append('%s: stage 1 options %s do not hold the key %r once' % (w, q['stage1Options'], key))
            if sum(1 for o in q['stage2Options'] if o['correct']) != 1:
                fails.append('%s: stage 2 has %d correct options' % (w, sum(1 for o in q['stage2Options'] if o['correct'])))
            if re.search(r'\(\s*if\b', key, re.I):
                fails.append('%s: the key %r carries its own condition: state it in the post instead' % (w, key))
            if re.search(r'roulette', allt, re.I):
                stated = [f for k, f in WHEELS.items() if k.lower() in q['post']['text'].lower()]
                used = set(re.findall(r'18/3[78]', allt))
                if not stated:
                    fails.append('%s: a roulette post that does not state its wheel' % w)
                elif used != {stated[0]}:
                    fails.append('%s: the post states a wheel with P(black) = %s, the item uses %s'
                                 % (w, stated[0], ', '.join(sorted(used)) or 'neither'))
            if re.search(r'Addition gives P\(A OR B\)|OR = add', allt):
                fails.append('%s: says addition gives P(A OR B), true only for mutually exclusive events' % w)
            if w in RULED:
                words, rkey, banned = RULED[w]
                if words not in q['post']['text']:
                    fails.append('%s: the post must say "%s" (Jon\'s ruling)' % (w, words))
                if key != rkey:
                    fails.append('%s: keyed %r, Jon\'s ruling keys %r' % (w, key, rkey))
                for b in banned:
                    if b in q['stage1Options']:
                        fails.append('%s: still offers %r, which the stated convention leaves no room for' % (w, b))
    missing = set(RULED) - {q['id'] for items in bank.values() for q in items}
    if missing:
        fails.append('items not found: %s' % ', '.join(sorted(missing)))


SWEEP_JS = r"""() => {
  window.setTimeout = () => 0;
  const out = [];
  const grid = () => document.getElementById('optionsGrid');
  for (const [lv, items] of Object.entries(QUESTIONS)) items.forEach(q => {
    S.level = lv; S.session = [q]; S.qIdx = 0; S.questionNum = 0;
    for (const pick of q.stage1Options) {
      showQuestion();
      const btn = [...grid().querySelectorAll('.option-btn')].find(b => b.textContent === pick);
      if (!btn) { out.push([q.id, 1, pick, 'not on screen']); continue; }
      btn.click();
      const right = btn.classList.contains('correct');
      if (right !== (pick === q.stage1CorrectAnswer)) out.push([q.id, 1, pick, right ? 'marked right' : 'marked wrong']);
    }
    for (const opt of q.stage2Options) {
      showQuestion(); renderStage2();
      const btn = [...grid().querySelectorAll('.option-btn')].find(b => b.textContent === opt.text);
      if (!btn) { out.push([q.id, 2, opt.text, 'not on screen']); continue; }
      btn.click();
      const right = btn.classList.contains('correct');
      if (right !== !!opt.correct) out.push([q.id, 2, opt.text, right ? 'marked right' : 'marked wrong']);
    }
  });
  return out;
}"""


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof QUESTIONS !== "undefined"', timeout=15000)
            bank = page.evaluate('() => QUESTIONS')
            for qid, stage, pick, what in page.evaluate(SWEEP_JS):
                fails.append('%s in Chromium: stage %d option %r %s' % (qid, stage, pick, what))
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            return bank
    finally:
        proc.terminate()
        proc.wait()


def esc(x):
    """The page writes non-ASCII characters as JS escapes (a backslash, u, four hex digits)."""
    return ''.join(c if ord(c) < 128 else chr(92) + 'u%04x' % ord(c) for c in x)


# (the item the failure must name, what is planted, today's text, main's text before LISTED-HIGH).
PLANTS = [
    ('woti_gcse_004', 't2-001: roulette, wheel unstated, keyed 18/38',
     "text:'12 reds in a row on a European roulette wheel (one green zero). I\\'m putting",
     "text:'12 reds in a row at roulette. I\\'m putting"),
    ('woti_gcse_011', 't2-002: keyed "0.12 (if independent)"',
     "stage1CorrectAnswer:'0.12',stage1Options:['0.12',",
     "stage1CorrectAnswer:'0.12 (if independent)',stage1Options:['0.12 (if independent)',"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    bank = play(fails, html)
    if bank is not None:
        check_bank(fails, bank)
    print('%s: %d items, every key checked against what its post states, every option clicked in Chromium'
          % (SLUG, sum(len(v) for v in (bank or {}).values())))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, new, old in PLANTS:
            new, old = esc(new), esc(old)
            if html.count(new) != 1:
                print('  self-test %-46s *** CANNOT PLANT (%d) ***' % (what, html.count(new)))
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(new, old))
            if planted is not None:
                check_bank(rep, planted)
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
