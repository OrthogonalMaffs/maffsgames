#!/usr/bin/env python3
# ci-line: Scroll reveal (feedback and Next scroll through MaffsScroll.reveal, never a direct scrollIntoView / scrollBy; every page that calls it or loads keypad.js loads scroll.js; faults planted and caught) | --selftest && --check
# ci-deps: games/ the-6-ps/index.html schools/assets/ escape-rooms/assets/engine.js
"""Feedback and Next are brought into view by one shared helper, schools/assets/scroll.js (SCROLL-REVEAL, 27 Oct 2026).

The fault (#566): a page scrolled its feedback into view once, before the maths font arrived; the working grew and
Next ended under the fold. The class search found it in keypad.js and nine games. MaffsScroll.reveal() scrolls now,
on the next frame and when the fonts are ready, so no page keeps a one-off scroll of its own. This check holds that:

  1. In games/, the-6-ps/, schools/ and escape-rooms/, no file other than scroll.js calls scrollIntoView or scrollBy,
     or scrollTo to anywhere but the top, unless the line is on ALLOWED (a scroll for another reason, named below).
     scrollTo(0, 0) and scrollTo({top: 0}) (resets) and focus({ preventScroll: true }) are not this class.
  2. A page that calls MaffsScroll, or loads keypad.js (which does), also loads scroll.js.

    python scripts/check-scroll-reveal.py --check      the repo
    python scripts/check-scroll-reveal.py --selftest   planted direct scrolls and a page missing scroll.js, all caught
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HELPER = 'schools/assets/scroll.js'
SCAN = ['games', 'the-6-ps', 'schools', 'escape-rooms']

# (file, text on the line): scrolls that are not feedback or Next (class search, 27 Oct 2026).
ALLOWED = [
    ('games/factor-theorem/index.html', 'cards[0].scrollIntoView'),
    ('games/the-perfect-prank/index.html', 'f.scrollIntoView'),
    ('games/truth-will-set-you-free/index.html', "getElementById('expressionSection').scrollIntoView"),
    ('escape-rooms/assets/engine.js', 'window.scrollTo(0, Math.max(0, node.getBoundingClientRect()'),
]

CALL = re.compile(r'\bscrollIntoView\s*\(|\bscrollBy\s*\(|\bscrollTo\s*\(([^)]*)\)')
TOP = re.compile(r'^\s*(0\s*,\s*0|\{\s*top\s*:\s*0\s*(,[^}]*)?\})\s*$')


def comment_free(line):
    return re.sub(r'//.*$', '', line) if not re.search(r'["\'`][^"\'`]*//', line) else line


def problems(rel, text):
    """The offending lines of one file: [(line number, text)]."""
    out = []
    if rel == HELPER:
        return out
    for n, line in enumerate(text.splitlines(), 1):
        code = comment_free(line)
        for m in CALL.finditer(code):
            if m.group(1) is not None and TOP.match(m.group(1)):
                continue                                   # scrollTo to the top: a reset
            if any(rel == f and s in line for f, s in ALLOWED):
                continue
            out.append((n, line.strip()[:120]))
            break
    return out


def missing_helper(rel, text):
    """A page that needs scroll.js and does not load it."""
    if not rel.endswith('.html'):
        return False
    needs = 'MaffsScroll' in text or re.search(r'<script[^>]+keypad\.js', text)
    return bool(needs) and not re.search(r'<script[^>]+scroll\.js', text)


def files():
    for top in SCAN:
        for d, _, names in os.walk(os.path.join(ROOT, top)):
            for name in names:
                if name.endswith(('.html', '.js')):
                    p = os.path.join(d, name)
                    yield os.path.relpath(p, ROOT).replace(os.sep, '/'), p


def check():
    bad = []
    for rel, p in files():
        text = open(p, encoding='utf-8', errors='replace').read()
        for n, line in problems(rel, text):
            bad.append('%s:%d calls a scroll directly instead of MaffsScroll.reveal: %s' % (rel, n, line))
        if missing_helper(rel, text):
            bad.append('%s uses MaffsScroll or keypad.js but does not load %s' % (rel, HELPER))
    return bad


def selftest():
    ok = True

    def expect(name, got, want):
        nonlocal ok
        good = bool(got) == want
        ok &= good
        print('%s  %s' % ('ok  ' if good else 'FAIL', name))

    g = 'games/x/index.html'
    expect('direct window.scrollBy on Next is caught', problems(g, "if (over > 0) window.scrollBy(0, over);"), True)
    expect('scrollBy with an options object is caught', problems(g, "window.scrollBy({ top: by, behavior: 'instant' });"), True)
    expect('scrollIntoView on the feedback is caught', problems(g, "fb.scrollIntoView({ block: 'nearest' });"), True)
    expect('scrollTo down the page is caught', problems(g, "window.scrollTo({ top: window.scrollY + dy });"), True)
    expect('a scrollIntoView in schools/assets/keypad.js is caught', problems('schools/assets/keypad.js', 'el.scrollIntoView();'), True)
    expect('scrollTo(0, 0) is a reset, not caught', problems(g, 'window.scrollTo(0, 0);'), False)
    expect('scrollTo({top: 0, behavior: "smooth"}) is a reset, not caught', problems(g, "window.scrollTo({top: 0, behavior: 'smooth'});"), False)
    expect('a commented-out call is not caught', problems(g, '// window.scrollBy(0, 5)'), False)
    expect('MaffsScroll.reveal is not caught', problems(g, 'MaffsScroll.reveal(nx, { inset: 40 });'), False)
    expect('the helper itself is exempt', problems(HELPER, 'window.scrollBy(0, dy);'), False)
    expect('an allowed line is not caught', problems(ALLOWED[0][0], 'if (cards.length) cards[0].scrollIntoView({ behavior: "smooth" });'), False)
    expect('the same line in another file is caught', problems(g, 'if (cards.length) cards[0].scrollIntoView({ behavior: "smooth" });'), True)
    page = '<script src="../../schools/assets/%s"></script>'
    expect('a keypad page without scroll.js is caught', missing_helper(g, page % 'keypad.js'), True)
    expect('a MaffsScroll page without scroll.js is caught', missing_helper(g, '<script>MaffsScroll.reveal(a)</script>'), True)
    expect('a keypad page with scroll.js passes', missing_helper(g, (page % 'scroll.js') + (page % 'keypad.js')), False)
    expect('a page that uses neither passes', missing_helper(g, page % 'answer-lock.js'), False)
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if not (a.check or a.selftest):
        ap.error('--check or --selftest')
    ok = True
    if a.selftest:
        ok = selftest()
    if a.check:
        bad = check()
        for b in bad:
            print('FAIL  ' + b)
        if not bad:
            print('ok    no direct feedback scroll, every page that needs scroll.js loads it')
        ok = ok and not bad
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
