#!/usr/bin/env python3
# ci-line: Graph Transformer (BFS + par; every explanation, checkpoint and phone panel; planted faults) |
"""Verifies every Graph Transformer puzzle is solvable with its tier's buttons and
correctly parred (docs/snagging-list.md snag #7's par-verification pass, promoted
to CI so an unsolvable or misparred puzzle cannot ship again).

WHY THIS RUNS THE BFS INSIDE THE PAGE, NOT AS A PYTHON RE-IMPLEMENTATION
-------------------------------------------------------------------------------
A Python re-implementation of the button effects and the curve-match rule could
drift from the game and would then be verifying itself -- the same reasoning as
verify-log-laws.py / verify-distinctly-average.py. Instead games/graph-transformer/
index.html exports window.GT_VERIFY, whose bfsCheck(level, puzzlesOverride) runs a
breadth-first search using the tier's ACTUAL button definitions
(transformButtonDefs), the ACTUAL move-merging rule (mirroring recomputeMoveCount:
a run of consecutive clicks on the same mergeable button is one move; every other
click is its own move -- replayed by calling the real button closures against the
real `state` object), and the ACTUAL curve comparison (curvesMatch/evalState) for
the goal test. curveDupPairs(puzzles) flags two puzzles in a tier whose target
curves agree at every sample point, using the same tolerance rule curvesMatch
uses, generalised across a pair of (possibly different) base functions.

WHAT IT ASSERTS
-------------------------------------------------------------------------------
For every puzzle in every tier (gcse, alevel):
  - the target is reachable within MAX_MOVES (6 -- the largest known par is 4,
    so this leaves comfortable headroom without letting the search run away);
  - the stored par equals the BFS minimum exactly -- too low OR too high both fail.
And for every tier as a whole:
  - no two puzzles share an identical target curve, except a pair recorded in
    KNOWN_DUP_PAIRS below (tracked, not failed -- same pattern as
    scripts/checker-allowlist.json and verify-distinctly-average.py's
    SIGNATURE_ALLOWLIST: a stale entry that no longer reproduces is itself a
    failure, so the list cannot silently rot into a blanket exemption).

FAULT-INJECTION SELF-TEST
-------------------------------------------------------------------------------
Runs on every CI pass (--no-selftest skips it): clones a real A-level puzzle and
sets its amplitude to 3 (unreachable -- the only y-scale buttons are Stretch x2/
Stretch x1/2 in y, which only ever reach +/-2^n) and requires bfsCheck to report it
unreachable; clones another and mutates its stored par by +1 and requires bfsCheck
to report a par mismatch. Both go through bfsCheck's puzzlesOverride parameter, so
neither mutation ever touches the real bank or the file on disk.

USAGE
-------------------------------------------------------------------------------
    python scripts/verify-graph-transformer.py
    python scripts/verify-graph-transformer.py --no-selftest
"""
import argparse
import asyncio
import copy
import os
import re
import sys
import time
from urllib.parse import urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import bank_common as bc  # noqa: E402  (start_stub_server: checked start, free port)
SLUG = "graph-transformer"
PORT = None  # set by main() to the free port the stub server got
LEVELS = ("gcse", "alevel")

# Known, reported-not-fixed duplicate-target pairs: (level, 0-indexed i, 0-indexed j) -> reason.
# Found by this script's own curveDupPairs check, not one of the three named puzzles this
# task fixed, so left as Jon's call (per the task's STOP IF) rather than fixed here.
KNOWN_DUP_PAIRS = {
    ("gcse", 10, 11): "x^3 is odd, so reflecting in the x-axis (a=-1, giving -x^3) and reflecting in "
                      "the y-axis (b=-1, giving (-x)^3 = -x^3) are the identical curve -- the same "
                      "reflect-x/reflect-y aliasing-on-an-odd-function class as the A-level match-check "
                      "bug fixed 29 Sep 2026 (docs/snagging-list.md #7), here showing up as a duplicate "
                      "puzzle rather than a wrongly-rejected route. Reported to Jon 29 Sep 2026 (this "
                      "session's par-verification build), tracked not fixed on his ruling.",
}

_FAILURES = []


def fail(msg):
    _FAILURES.append(msg)
    print("FAIL: " + msg)


async def run_bfs_on(page, lvl, puzzles):
    return await page.evaluate("(a) => window.GT_VERIFY.bfsCheck(a.l, a.p)", {"l": lvl, "p": puzzles})


# SWEEP-1 (13 Oct 2026): what "Show steps" says for each target, and how a 1/x equation is written.
TEXT_JS = """(l) => {
  level=l; startGame();
  return window.GT_VERIFY.allPuzzles(l).map(p => {
    puzzles=[p];pIdx=0;loadPuzzle();state={...p.target};checkMatch();
    const read=()=>Array.from(document.querySelectorAll('#successText .explanation-step')).map(el=>({
      name:el.querySelector('strong').textContent,
      vector:el.querySelector('strong annotation')?.textContent,
      eq:el.children[1].querySelector('annotation')?.textContent,
      text:Array.from(el.children).slice(2).map(n=>n.textContent).join(' '),
      raw:Array.from(el.childNodes).map(n=>{const c=n.cloneNode(true);c.querySelectorAll?.('.katex').forEach(k=>k.remove());return c.textContent}).join(' '),
      errors:el.querySelectorAll('.katex-error').length
    }));
    const success=read();
    loadPuzzle();skipPuzzle();const skip=read();
    loadPuzzle();const shown=buildGhostSteps(p.target,p.base).map(()=>{
      stepThrough();const el=document.querySelector('#stepCaption .step-what');
      return {name:el.textContent,vector:el.querySelector('annotation')?.textContent};
    });
    const initial={a:1,b:1,h:0,k:0}, expected=[];
    let before={...initial};
    for(const key of ['b','h','a','k']){
      if(p.target[key]===initial[key])continue;
      const after={...before,[key]:p.target[key]};
      expected.push({from:buildEquation(p.base,before),to:buildEquation(p.base,after)});
      before=after;
    }
    return {label:buildGhostSteps(p.target,p.base).map(s=>s.what).join('; '),base:p.base,t:p.target,
      steps:buildGhostSteps(p.target,p.base),success,skip,shown,expected,eq:buildEquation(p.base,p.target)};
  });
}"""


def gt_fmt(n):
    if abs(n - 0.5) < 1e-9:
        return '\u00bd'
    if abs(n + 0.5) < 1e-9:
        return '-\u00bd'
    v = round(n * 1000) / 1000
    return str(int(v)) if v == int(v) else str(v)


def text_fails(lvl, items):
    """Independent coordinate and name expectations from target parameters.
    Equation formatting is compared with buildEquation as the contract requires;
    that comparison is a consistency check, not an independent maths oracle."""
    out = []
    for i, it in enumerate(items):
        t, tag = it['t'], '%s #%d (%s)' % (lvl, i + 1, it['label'])
        want = []
        if t['b'] != 1:
            m = abs(t['b'])
            want.append('Reflection in the y-axis' if m == 1 else
                        'Stretch, scale factor ' + gt_fmt(1 / m) + ', parallel to the x-axis' +
                        ('; Reflection in the y-axis' if t['b'] < 0 else ''))
        if t['h']:
            want.append('Translation by vector (' + gt_fmt(t['h']) + ', 0)')
        if t['a'] != 1:
            m = abs(t['a'])
            want.append('Reflection in the x-axis' if m == 1 else
                        'Stretch, scale factor ' + gt_fmt(m) + ', parallel to the y-axis' +
                        ('; Reflection in the x-axis' if t['a'] < 0 else ''))
        if t['k']:
            want.append('Translation by vector (0, ' + gt_fmt(t['k']) + ')')
        if [st['what'] for st in it['steps']] != want:
            out.append('%s: step names do not match independently derived names %s' % (tag, want))
        count = sum(t[k] != v for k, v in [('b', 1), ('h', 0), ('a', 1), ('k', 0)])
        for panel in ('success', 'skip'):
            blocks = it[panel]
            if len(blocks) != count:
                out.append('%s: %s has %d blocks, expected %d' % (tag, panel, len(blocks), count))
            for j, (block, step, eq) in enumerate(zip(blocks, it['steps'], it['expected'])):
                if block['errors'] or re.search(r'\\(?:begin|end|longrightarrow|dfrac|tfrac|sqrt|sin)', block['raw']):
                    out.append('%s: %s raw LaTeX or KaTeX error' % (tag, panel))
                if j >= len(it['shown']) or any(block.get(k) != it['shown'][j].get(k) for k in ('name', 'vector')):
                    out.append('%s: %s name differs from rendered Show steps' % (tag, panel))
                expected_eq = eq['from'] + ' \\longrightarrow ' + eq['to']
                if block['eq'] != expected_eq or step['from'] != eq['from'] or step['to'] != eq['to']:
                    out.append('%s: %s step %d before/after equation mismatch' % (tag, panel, j + 1))
                if 'Translation by vector' in step['what']:
                    vector = re.search(r'\(([^,]+), ([^)]+)\)', step['what'])
                    latex = '\\begin{pmatrix}' + vector[1] + '\\\\' + vector[2] + '\\end{pmatrix}'
                    # KaTeX has accessible MathML and visual text: inspect the source annotation separately below.
                    if 'Translation by vector' not in block['name']:
                        out.append('%s: %s missing translation name' % (tag, panel))
                    if block.get('vector') != latex:
                        out.append('%s: %s column vector mismatch' % (tag, panel))
                elif step['what'] != block['name']:
                    out.append('%s: %s name differs from Show steps' % (tag, panel))
                if step['title'] == 'Horizontal shift':
                    direction = 'right' if t['h'] > 0 else 'left'
                    opposite = 'left' if t['h'] > 0 else 'right'
                    # Inspect the affirmative clause, rather than accepting "right, not left" with its words flipped.
                    clause = block['text'].split(', not')[0].lower()
                    if direction not in clause or opposite in clause:
                        out.append('%s: %s horizontal shift direction wrong' % (tag, panel))
                    signed = 'x-' + gt_fmt(t['h']) if t['h'] > 0 else 'x+' + gt_fmt(-t['h'])
                    if signed not in eq['to']:
                        out.append('%s: horizontal shift equation has wrong sign' % tag)
                bad = re.search(r'factor of 1(?![\d.])|(raises|lowers) every point by -|1/½|1/-', block['text'])
                if bad:
                    out.append('%s: invalid explanation %s' % (tag, bad.group(0)))
        # Independently map the base point using x_new=x_old/b+h, y_new=a*y_old+k.
        seed = (0, 1) if it['base'] == 'eˣ' else (1, 1) if it['base'] == '1/x' else (0, 0)
        label = {'x²': 'Vertex', 'x³': 'Origin point', 'sin x': 'Zero crossing',
                 '√x': 'Endpoint'}.get(it['base'], 'Reference point')
        prev = dict(a=1, b=1, h=0, k=0)
        keys = [k for k in ('b', 'h', 'a', 'k') if t[k] != prev[k]]
        def coords(st):
            return '(' + gt_fmt(seed[0] / st['b'] + st['h']) + ', ' + gt_fmt(st['a'] * seed[1] + st['k']) + ')'
        for key, step in zip(keys, it['steps']):
            nxt = dict(prev, **{key: t[key]})
            if step['state'] != nxt or step['before'] != prev:
                out.append('%s: incorrect decomposition state' % tag)
            check = label + ': ' + coords(prev) + ' → ' + coords(nxt) + '.'
            if step['checkpoint'] != check:
                out.append('%s: checkpoint does not follow the coordinate map' % tag)
            prev = nxt
        if it['base'] == '1/x' and re.search(r'(\d|\\tfrac\{1\}\{\d+\})\\dfrac', it['eq']):
            out.append('%s: %s reads as a mixed number (s1-004)' % (tag, it['eq']))
    return out


async def check_phone_panels(page):
    """Every puzzle, both panels, all canon phone sizes and both font modes."""
    await page.add_style_tag(content='*,*::before,*::after{animation:none!important;transition:none!important}')
    worst = 0
    for aa in (False, True):
        await page.evaluate('(aa)=>document.body.classList.toggle("accessible",aa)', aa)
        for width, height in ((320, 568), (375, 667), (390, 844)):
            await page.set_viewport_size({'width': width, 'height': height})
            await page.evaluate(bc.settle_js())
            rows = await page.evaluate("""() => {
              const rows=[];
              for(const lvl of ['gcse','alevel']){
                level=lvl;startGame();
                for(const [i,p] of GT_VERIFY.allPuzzles(lvl).entries()){
                  puzzles=[p];pIdx=0;
                  for(const mode of ['success','skip']){
                    loadPuzzle();if(mode==='success'){state={...p.target};checkMatch()}else skipPuzzle();
                    const panel=document.getElementById('successMsg');
                    const button=document.querySelector(mode==='success'?'#matchNext':'#skipNext button');
                    const rect=button.getBoundingClientRect();
                    rows.push({lvl,puzzle:i+1,mode,bottom:rect.bottom,top:rect.top,height:rect.height,
                      clipped:panel.scrollHeight>panel.clientHeight,wide:panel.scrollWidth>panel.clientWidth});
                  }
                }
              }return rows;
            }""")
            for row in rows:
                worst = max(worst, row['bottom'])
                if row['height'] < 44 or row['wide'] or row['top'] < 0:
                    fail('phone %dx%d Aa=%s: %s' % (width, height, aa, row))
                elif (row['bottom'] > height - 40 or row['clipped']) and not (aa and width == 320):
                    fail('phone %dx%d Aa=%s: %s' % (width, height, aa, row))
            exceptions = sum(row['bottom'] > height - 40 or row['clipped'] for row in rows)
            print('  %dx%d Aa=%s: 100 panels, Next bottom <= %.2fpx, %d overflow%s' %
                  (width, height, aa, max(row['bottom'] for row in rows), exceptions,
                   ' (canon Aa/320 exception)' if aa and width == 320 else ''))
    print('Phone panels: 600 checked; worst Next bottom %.2fpx; 40px footer reserved' % worst)


def menu_fails(text):
    """graph-transformer-s1-005 (R2): the start screen says what Par is and that repeated presses of one shift button are one move."""
    out = []
    if 'Par is the fewest moves' not in text:
        out.append('start: the start screen must say Par is the fewest moves the puzzle needs')
    if 'counts as one move' not in text:
        out.append('start: the start screen must say pressing the same shift button again and again counts as one move')
    return out


# The old caption and equation code, planted back in the page (each must fail).
OLD_TEXT_PLANTS = [
    ('a reflection captioned as a stretch by a factor of 1',
     "buildGhostSteps = (function (orig) { return function (t,b) { return orig(t,b).map(s => s.what === 'Reflection in the x-axis'"
     " ? Object.assign({}, s, {what: 'Squash vertically by a factor of 1, and reflect in the x-axis'}) : s); }; })(buildGhostSteps);"),
    ('a downward shift that "raises every point by -3"',
     "buildGhostSteps = (function (orig) { return function (t,b) { return orig(t,b).map(s => s.title === 'Vertical shift' && t.k < 0"
     " ? Object.assign({}, s, {why: '+ ' + t.k + ' raises every point by ' + t.k + '.'}) : s); }; })(buildGhostSteps);"),
    ('2 written beside 1/x',
     "buildEquation = (function (orig) { return function (b, st) { return b === '1/x' && st.a === 2 ? 'y = 2\\\\dfrac{1}{x}' : orig(b, st); }; })(buildEquation);"),
    ('flipped horizontal direction word',
     "buildGhostSteps = (function(orig){return function(t,b){return orig(t,b).map(s=>s.title==='Horizontal shift'"
     " ? {...s,why:s.why.replace(/RIGHT|LEFT/g,w=>w==='RIGHT'?'LEFT':'RIGHT')} : s)}})(buildGhostSteps);"),
    ('horizontal scale factor b instead of 1/abs(b)',
     "buildGhostSteps = (function(orig){return function(t,b){return orig(t,b).map(s=>s.title==='Horizontal stretch'"
     " ? {...s,what:s.what.replace('factor '+fmt(1/Math.abs(t.b)), 'factor '+fmt(Math.abs(t.b)))} : s)}})(buildGhostSteps);"),
    ('missing result step block',
     "renderExplanation = (function(orig){return function(...args){orig(...args);document.querySelector('#successText .explanation-step')?.remove()}})(renderExplanation);"),

]


async def run_selftest(page, all_puzzles):
    """Mutate one puzzle's amplitude to 3 (unreachable) and another's par by +1
    (mismatch), via bfsCheck's puzzlesOverride. The real bank is never touched."""
    ok = True
    lines = []
    lvl, pool = "alevel", all_puzzles["alevel"]

    amp = copy.deepcopy(pool[0])
    amp["target"]["a"] = 3
    res = (await run_bfs_on(page, lvl, [amp]))[0]
    caught = not res["reachable"]
    ok = ok and caught
    lines.append("  amplitude -> 3 on %-42s %s" %
                 (amp["label"], "CAUGHT (unreachable)" if caught else "*** MISSED ***"))

    src = next((p for p in pool if p is not pool[0]), pool[0])
    par_item = copy.deepcopy(src)
    par_item["par"] = par_item["par"] + 1
    res2 = (await run_bfs_on(page, lvl, [par_item]))[0]
    caught2 = res2["reachable"] and res2["minMoves"] != par_item["par"]
    ok = ok and caught2
    lines.append("  par +1 on %-46s %s" %
                 (par_item["label"], "CAUGHT (par mismatch)" if caught2 else "*** MISSED ***"))

    await page.evaluate("() => { document.querySelector('#menu .menu-info').innerHTML = 'The blue curve is yours.'; }")
    caught = bool(menu_fails(await page.inner_text('#menu')))
    ok = ok and caught
    lines.append("  %-56s %s" % ("Par and the one-move rule not explained", "CAUGHT" if caught else "*** MISSED ***"))
    for name, js in OLD_TEXT_PLANTS:
        await page.evaluate("() => { window.__gt_saved = [buildGhostSteps, buildEquation, renderExplanation]; }")
        await page.evaluate("() => { " + js + " }")
        caught = False
        for lv in LEVELS:
            caught = caught or bool(text_fails(lv, await page.evaluate(TEXT_JS, lv)))
        await page.evaluate("() => { buildGhostSteps = window.__gt_saved[0]; buildEquation = window.__gt_saved[1]; renderExplanation = window.__gt_saved[2]; }")
        ok = ok and caught
        lines.append("  %-56s %s" % (name, "CAUGHT" if caught else "*** MISSED ***"))

    return ok, lines


async def run_all(no_selftest):
    from playwright.async_api import async_playwright

    base = "http://127.0.0.1:%d" % PORT
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        await page.goto(base + "/games/" + SLUG + "/?cb=verify%d" % int(time.time()),
                        wait_until="load", timeout=20000)
        await page.wait_for_function("!!window.GT_VERIFY", timeout=8000)
        await page.evaluate(bc.settle_js())
        for f in menu_fails(await page.inner_text('#menu')):
            fail(f)

        results, all_puzzles, dup_pairs = {}, {}, {}
        for lvl in LEVELS:
            results[lvl] = await page.evaluate("(l) => window.GT_VERIFY.bfsCheck(l)", lvl)
            all_puzzles[lvl] = await page.evaluate("(l) => window.GT_VERIFY.allPuzzles(l).map(p => ({...p,label:buildGhostSteps(p.target,p.base).map(s=>s.what).join('; ')}))", lvl)
            dup_pairs[lvl] = await page.evaluate(
                "(l) => window.GT_VERIFY.curveDupPairs(window.GT_VERIFY.allPuzzles(l))", lvl)
            for f in text_fails(lvl, await page.evaluate(TEXT_JS, lvl)):
                fail(f)

        selftest_ok, selftest_lines = True, []
        await check_phone_panels(page)
        if not no_selftest:
            selftest_ok, selftest_lines = await run_selftest(page, all_puzzles)

        await browser.close()
        return results, all_puzzles, dup_pairs, errors, selftest_ok, selftest_lines


def check_results(lvl, results):
    for i, r in enumerate(results):
        tag = "%s #%d (%s, %s)" % (lvl, i + 1, r["base"], r["label"])
        if not r["reachable"]:
            fail("%s: target %r is UNREACHABLE with this tier's buttons (BFS bounded at %d moves)"
                 % (tag, r["target"], r["boundedAt"]))
            continue
        if r["minMoves"] != r["par"]:
            fail("%s: stored par %d != true minimum %d moves" % (tag, r["par"], r["minMoves"]))


def check_dups(lvl, puzzles, pairs):
    seen = set()
    for i, j in pairs:
        key = (lvl, i, j)
        seen.add(key)
        if key in KNOWN_DUP_PAIRS:
            print("  tracked, not failed: %s #%d/#%d share a target curve (%s...)"
                 % (lvl, i + 1, j + 1, KNOWN_DUP_PAIRS[key][:60]))
            continue
        fail("%s: puzzle #%d (%s) and #%d (%s) share an identical target curve"
             % (lvl, i + 1, puzzles[i]["label"], j + 1, puzzles[j]["label"]))
    for key in KNOWN_DUP_PAIRS:
        if key[0] == lvl and key not in seen:
            fail("KNOWN_DUP_PAIRS lists %s #%d/#%d but it no longer occurs -- remove the stale entry"
                 % key)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-selftest", action="store_true", help="skip the fault-injection self-test")
    args = ap.parse_args()

    global PORT
    # A free port chosen per run; raises bc.StubServerError, naming the cause, if the
    # stub server cannot start.
    server, base = bc.start_stub_server()
    PORT = urlsplit(base).port
    try:
        results, all_puzzles, dup_pairs, errors, selftest_ok, selftest_lines = asyncio.run(
            run_all(args.no_selftest))
    finally:
        server.terminate()

    for e in errors:
        fail("page error: " + e)

    for lvl in LEVELS:
        print("Verifying %s: %d puzzles" % (lvl, len(results[lvl])))
        check_results(lvl, results[lvl])
        check_dups(lvl, all_puzzles[lvl], dup_pairs[lvl])

    if not args.no_selftest:
        print()
        print("Fault-injection self-test (mutations must be caught; the real bank is never touched):")
        for ln in selftest_lines:
            print(ln)
        if not selftest_ok:
            fail("fault-injection self-test: at least one mutation was not caught")

    print()
    if _FAILURES:
        print("%d FAILURE(S)" % len(_FAILURES))
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
