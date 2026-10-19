#!/usr/bin/env python3
# ci-line: Four Quadrant Explorer (every plot target, point reading and fourth corner recomputed; every grid cell tapped on the real canvas in Chromium) |
"""Four Quadrant Explorer: three kinds of question on a -5..5 grid, in a cycle of plot, read, shape.

Static banks, read from the page as served: PLOT_QUESTIONS (tap the point (x, y)), READ_QUESTIONS (four options
naming a drawn point; the key is options[correct], and the game shuffles their order) and SHAPE_QUESTIONS (three
corners of an axis-aligned rectangle drawn, tap the fourth). The mark for a tap is the grid cell it snaps to.

Checks, independent of the game's code:
  Plot: every target an integer pair on the grid (-5..5), none repeated.
  Read: the key option is the drawn point written "(x,y)"; four distinct options, each an ordered pair of integers on
    the grid; exactly one equals the point (so no other option is also true); every distractor is a slip a student
    makes (a sign flipped, both signs flipped, the pair reversed, or the reversed pair with a sign flipped); no point
    repeated. The point is drawn: in Chromium the canvas pixel at the grid point is the point's colour, at exactly one
    of the 121 grid points.
  Shape: the three corners are three corners of an axis-aligned rectangle (one x and one y repeat; the right angle is
    at the corner that shares an x with one and a y with the other), all on the grid, and the key is the missing
    fourth corner (the x that appears once and the y that appears once), computed here.
  Sessions: buildQueue() at 10, 20 and 30 (three draws each) has that length and cycles plot, read, shape.
  Marking, in Chromium (390x844), through the game's own canvas handlers (a click event at each grid point's pixel, the
    page's real coordinate mapping): every plot target is tapped at all 121 grid points, and only the target reads
    "Correct!" (and scores 1), the others "The correct position was (x, y)"; a tap 0.45 of a cell off the target still
    counts and 0.55 off does not (the snap is to the nearest point); every read question has each of its four options
    pressed: the key reads "Correct!" and the others "The correct answer was (x,y)"; every shape question is tapped at
    all 121 points as a first try (the fourth corner scores 1 and reads "Correct! First attempt."; any other reads
    "Not quite - try once more"), then fourth corner after a miss ("Got it! (No point - not first
    attempt)", no score) and two misses (shows "The fourth corner was (x, y)").
  Labels (four-quadrant-explorer-r-001), in Chromium at 320, 390 and 1280 px wide (Outfit served from the pinned copy):
    every piece of text drawGrid() writes on the canvas is measured where it is drawn (measureText's bounding box at
    its alignment); the tick labels -5..5 on both axes are all there, the origin label "(0,0)" once, and no two
    boxes overlap, so "(0,0)" covers no tick label and every tick label can be read.
No analytics or leaderboard request leaves the stub server (every other request is aborted).

A self-test plants faults in a copy of the page and each must FAIL: a wrong read key (the second option made the key),
a second correct read option (a distractor equal to the point), a wrong shape key, a plot tolerance of 1.4 cells (a
wrong tap marked right), a wrong figure in the plot feedback (x and y swapped) and the origin label back below-left of
the origin, over the -1 labels (r-001).

    python scripts/verify-four-quadrant-explorer.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'four-quadrant-explorer'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
RANGE = range(-5, 6)
SESSIONS = (10, 20, 30)
DEALS = 3
POINT_RGB = (99, 102, 241)      # #6366f1, the colour the game draws the point in


def on_grid(x, y):
    return isinstance(x, int) and isinstance(y, int) and not isinstance(x, bool) and -5 <= x <= 5 and -5 <= y <= 5


def pair(s):
    m = re.fullmatch(r'\((-?\d+),(-?\d+)\)', s)
    return (int(m.group(1)), int(m.group(2))) if m else None


def slips(x, y):
    return {(-x, y), (x, -y), (-x, -y), (y, x), (-y, x), (y, -x), (-y, -x)}


def fourth_corner(verts):
    xs = [v['x'] for v in verts]
    ys = [v['y'] for v in verts]
    ox = [x for x in xs if xs.count(x) == 1]
    oy = [y for y in ys if ys.count(y) == 1]
    if len(verts) != 3 or len(ox) != 1 or len(oy) != 1 or len(set(xs)) != 2 or len(set(ys)) != 2:
        return None
    return (ox[0], oy[0])


def check_banks(fails, plots, reads, shapes):
    seen = set()
    for i, p in enumerate(plots, 1):
        if not on_grid(p['x'], p['y']):
            fails.append('plot %d: %r is off the grid' % (i, p))
        if (p['x'], p['y']) in seen:
            fails.append('plot %d: (%s, %s) is repeated' % (i, p['x'], p['y']))
        seen.add((p['x'], p['y']))
    seen = set()
    for i, q in enumerate(reads, 1):
        where = 'read %d (%s, %s)' % (i, q['x'], q['y'])
        if not on_grid(q['x'], q['y']):
            fails.append('%s: off the grid' % where)
        if (q['x'], q['y']) in seen:
            fails.append('%s: the point is repeated' % where)
        seen.add((q['x'], q['y']))
        opts = q['opts']
        prs = [pair(o) for o in opts]
        if len(opts) != 4 or len(set(opts)) != 4 or None in prs:
            fails.append('%s: options %r are not four distinct "(x,y)" strings' % (where, opts))
            continue
        if any(not on_grid(*p) for p in prs):
            fails.append('%s: an option is off the grid: %r' % (where, opts))
        right = [k for k, p in enumerate(prs) if p == (q['x'], q['y'])]
        if right != [q['correct']]:
            fails.append('%s: the options equal the point at %s, but the key is option %s (%r)' % (
                where, right, q['correct'], opts))
        for k, p in enumerate(prs):
            if k not in right and p not in slips(q['x'], q['y']):
                fails.append('%s: distractor %s is not a sign or order slip of the point' % (where, opts[k]))
    for i, q in enumerate(shapes, 1):
        where = 'shape %d %r' % (i, q['verts'])
        if not all(on_grid(v['x'], v['y']) for v in q['verts'] + [q['answer']]):
            fails.append('%s: off the grid' % where)
        want = fourth_corner(q['verts'])
        if want is None:
            fails.append('%s: not three corners of an axis-aligned rectangle' % where)
        elif (q['answer']['x'], q['answer']['y']) != want:
            fails.append('%s: keyed (%s, %s), the fourth corner is %s' % (where, q['answer']['x'], q['answer']['y'], want))


FIELD_JS = r"""(args) => {
  const [q, mode] = args;
  startGame();
  questions = [Object.assign({type: q.type}, q)]; currentQ = 0; score = 0;
  showQuestion();
  return null;
}"""
SWEEP_JS = r"""(args) => {
  const [q, type, offs] = args;
  const out = [];
  const click = (gx, gy, dx, dy) => {
    const r = canvas.getBoundingClientRect();
    const px = toCanvasX(gx) + dx * gridSpacing, py = toCanvasY(gy) + dy * gridSpacing;
    canvas.dispatchEvent(new MouseEvent('click', {clientX: r.left + px * r.width / canvasW,
                                                   clientY: r.top + py * r.height / canvasH, bubbles: true}));
  };
  const fb = () => document.getElementById('feedbackBar').textContent;
  for (let gx = -5; gx <= 5; gx++) for (let gy = -5; gy <= 5; gy++) {
    startGame(); questions = [Object.assign({type: type}, q)]; currentQ = 0; score = 0; showQuestion();
    click(gx, gy, 0, 0);
    out.push({gx: gx, gy: gy, fb: fb(), score: score, locked: MaffsLock.isLocked(gameArea)});
  }
  const edge = [];
  if (offs) for (const [gx, gy, dx, dy] of offs) {
    startGame(); questions = [Object.assign({type: type}, q)]; currentQ = 0; score = 0; showQuestion();
    click(gx, gy, dx, dy);
    edge.push({dx: dx, dy: dy, fb: fb(), score: score});
  }
  MaffsLock.clearTimers();
  return {cells: out, edge: edge};
}"""
SHAPE_SEQ_JS = r"""(args) => {
  const [q, seq] = args;
  startGame(); questions = [Object.assign({type: 'shape'}, q)]; currentQ = 0; score = 0; showQuestion();
  const out = [];
  for (const [gx, gy] of seq) {
    const r = canvas.getBoundingClientRect();
    canvas.dispatchEvent(new MouseEvent('click', {clientX: r.left + toCanvasX(gx) * r.width / canvasW,
                                                   clientY: r.top + toCanvasY(gy) * r.height / canvasH, bubbles: true}));
    out.push({fb: document.getElementById('feedbackBar').textContent, score: score, locked: MaffsLock.isLocked(gameArea)});
  }
  MaffsLock.clearTimers();
  return out;
}"""
READ_JS = r"""(q) => {
  const out = [];
  for (let i = 0; i < 4; i++) {
    startGame(); questions = [Object.assign({type: 'read'}, q)]; currentQ = 0; score = 0; showQuestion();
    const btns = [...document.querySelectorAll('#optionsRow .option-btn')];
    const b = btns.find(x => +x.dataset.idx === i);
    b.click();
    out.push({text: b.textContent, fb: document.getElementById('feedbackBar').textContent, score: score,
              texts: btns.map(x => x.textContent)});
  }
  // the drawn point: the canvas pixel at every grid point
  startGame(); questions = [Object.assign({type: 'read'}, q)]; currentQ = 0; score = 0; showQuestion();
  const dpr = window.devicePixelRatio || 1, hits = [];
  for (let gx = -5; gx <= 5; gx++) for (let gy = -5; gy <= 5; gy++) {
    const d = ctx.getImageData(Math.round(toCanvasX(gx) * dpr), Math.round(toCanvasY(gy) * dpr), 1, 1).data;
    if (Math.abs(d[0] - %d) < 6 && Math.abs(d[1] - %d) < 6 && Math.abs(d[2] - %d) < 6) hits.push([gx, gy]);
  }
  MaffsLock.clearTimers();
  return {answers: out, hits: hits};
}""" % POINT_RGB
LABEL_WIDTHS = (320, 390, 1280)
LABELS_JS = r"""async () => {
  await document.fonts.load('12px Outfit');
  startGame(); MaffsLock.clearTimers();
  initCanvas();
  const rec = [], orig = ctx.fillText;
  ctx.fillText = function (t, x, y) {
    const m = ctx.measureText(String(t));
    rec.push({t: String(t), l: x - m.actualBoundingBoxLeft, r: x + m.actualBoundingBoxRight,
              top: y - m.actualBoundingBoxAscent, bot: y + m.actualBoundingBoxDescent});
    return orig.apply(this, arguments);
  };
  drawGrid();
  delete ctx.fillText;
  return rec;
}"""
QUEUE_JS = r"""() => { const out = {};
  for (const n of %s) { out[n] = [];
    for (let k = 0; k < %d; k++) out[n].push(buildQueue(n).map(q => q.type)); }
  return out; }""" % (list(SESSIONS), DEALS)


def play_checks(fails, page, plots, reads, shapes):
    for p in plots:
        res = page.evaluate(SWEEP_JS, [p, 'plot', [[p['x'], p['y'], 0.45, 0], [p['x'], p['y'], -0.45, 0.45],
                                                   [p['x'], p['y'], 0.55, 0], [p['x'], p['y'], 0, -0.55]]])
        for c in res['cells']:
            hit = (c['gx'], c['gy']) == (p['x'], p['y'])
            want = '✓ Correct!' if hit else '✗ The correct position was (%d, %d)' % (p['x'], p['y'])
            if c['fb'] != want or c['score'] != (1 if hit else 0):
                fails.append('plot (%d, %d), tapped (%d, %d): %r score %d, expected %r' % (
                    p['x'], p['y'], c['gx'], c['gy'], c['fb'], c['score'], want))
                break
        e = res['edge']
        for k, ok in enumerate((True, True, False, False)):
            if (e[k]['score'] == 1) != ok:
                fails.append('plot (%d, %d): a tap %s cells off should %sscore' % (
                    p['x'], p['y'], (0.45, 0.45, 0.55, 0.55)[k], '' if ok else 'not '))
    for q in reads:
        res = page.evaluate(READ_JS, q)
        key = (q['x'], q['y'])
        if res['hits'] != [list(key)]:
            fails.append('read %r: the point is drawn at grid points %s, not just %s' % (key, res['hits'], key))
        for i, a in enumerate(res['answers']):
            right = pair(q['opts'][i]) == key
            want = '✓ Correct!' if right else '✗ The correct answer was %s' % ('(%d,%d)' % key)
            if a['fb'] != want or a['score'] != (1 if right else 0) or a['text'] != q['opts'][i]:
                fails.append('read %r, option %d (%s): %r score %d, expected %r' % (key, i, q['opts'][i], a['fb'], a['score'], want))
    for q in shapes:
        ans = (q['answer']['x'], q['answer']['y'])
        res = page.evaluate(SWEEP_JS, [q, 'shape', None])
        for c in res['cells']:
            hit = (c['gx'], c['gy']) == ans
            want = '✓ Correct! First attempt.' if hit else '✗ Not quite — try once more'
            if c['fb'] != want or c['score'] != (1 if hit else 0):
                fails.append('shape %r, tapped (%d, %d) first: %r score %d, expected %r' % (
                    q['verts'], c['gx'], c['gy'], c['fb'], c['score'], want))
                break
        miss = [(g[0], g[1]) for g in ((0, 0), (5, 5)) if (g[0], g[1]) != ans] + [(-5, -5)]
        miss = [m for m in miss if m != ans][:2]
        s1 = page.evaluate(SHAPE_SEQ_JS, [q, [miss[0], ans]])
        if not (s1[0]['fb'] == '✗ Not quite — try once more' and
                s1[1]['fb'] == '✓ Got it! (No point — not first attempt)' and s1[1]['score'] == 0):
            fails.append('shape %r: a miss then the fourth corner reads %r' % (q['verts'], s1))
        s2 = page.evaluate(SHAPE_SEQ_JS, [q, [miss[0], miss[1]]])
        if not (s2[1]['fb'] == '✗ The fourth corner was (%d, %d)' % ans and s2[1]['score'] == 0):
            fails.append('shape %r: two misses read %r' % (q['verts'], s2))


def check_labels(fails, width, boxes):
    texts = [b['t'] for b in boxes]
    ticks = sorted(str(i) for i in RANGE if i) * 2
    if sorted(t for t in texts if t != '(0,0)' and not t.startswith('Q')) != sorted(ticks) or texts.count('(0,0)') != 1:
        fails.append('labels at %d px: drawn %r, expected the tick labels -5..5 on both axes and "(0,0)" once' % (width, texts))
    for i, a in enumerate(boxes):
        for c in boxes[i + 1:]:
            if a['l'] < c['r'] and c['l'] < a['r'] and a['top'] < c['bot'] and c['top'] < a['bot']:
                fails.append('labels at %d px: "%s" covers "%s" (boxes %s and %s; r-001)' % (
                    width, a['t'], c['t'], [round(a[k]) for k in ('l', 'top', 'r', 'bot')],
                    [round(c[k]) for k in ('l', 'top', 'r', 'bot')]))


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    stats = {}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            for w in LABEL_WIDTHS:
                lctx = browser.new_context(viewport={'width': w, 'height': 900})
                lctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
                lctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
                lctx.route(lambda u: bc.is_font_cdn(u), bc.serve_real_font)   # Outfit from the pinned copy
                lctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                    status=200, content_type='text/html; charset=utf-8', body=html))
                lpage = lctx.new_page()
                lpage.goto(base + '/games/%s/?cb=labels%d' % (SLUG, w), wait_until='load', timeout=20000)
                lpage.wait_for_function('typeof drawGrid === "function"', timeout=15000)
                check_labels(fails, w, lpage.evaluate(LABELS_JS))
                lctx.close()
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof PLOT_QUESTIONS !== "undefined" && typeof buildQueue === "function"', timeout=15000)
            plots = page.evaluate('() => JSON.parse(JSON.stringify(PLOT_QUESTIONS))')
            reads = page.evaluate('() => JSON.parse(JSON.stringify(READ_QUESTIONS))')
            shapes = page.evaluate('() => JSON.parse(JSON.stringify(SHAPE_QUESTIONS))')
            check_banks(fails, plots, reads, shapes)
            for n, qs in page.evaluate(QUEUE_JS).items():
                for d in qs:
                    if len(d) != int(n) or d != [('plot', 'read', 'shape')[i % 3] for i in range(int(n))]:
                        fails.append('a %s-question queue is not the plot, read, shape cycle: %r' % (n, d[:6]))
            play_checks(fails, page, plots, reads, shapes)
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            browser.close()
            stats = {'plot': len(plots), 'read': len(reads), 'shape': len(shapes)}
    finally:
        proc.terminate()
        proc.wait()
    return stats


PLANTS = [
    ('a wrong read key (the second option made the key)', 'but the key is option',
     [("{x:4,y:-1, opts:['(4,-1)','(-4,1)','(4,1)','(-1,4)'], correct:0}", "{x:4,y:-1, opts:['(4,-1)','(-4,1)','(4,1)','(-1,4)'], correct:1}")]),
    ('a second correct read option (a distractor equal)', 'options',
     [("{x:-2,y:3, opts:['(-2,3)','(2,3)','(-2,-3)','(3,-2)'], correct:0}", "{x:-2,y:3, opts:['(-2,3)','(-2,3)','(-2,-3)','(3,-2)'], correct:0}")]),
    ('a wrong shape key', 'keyed',
     [("answer:{x:1,y:3}", "answer:{x:1,y:2}")]),
    ('a plot tolerance of 1.4 cells (a wrong tap marked right)', 'tapped',
     [("const tolerance = 0.4;\n  const dx = Math.abs(snapped.x - q.x);", "const tolerance = 1.4;\n  const dx = Math.abs(snapped.x - q.x);")]),
    ('a wrong figure in the plot feedback (x and y swapped)', 'tapped',
     [("showFeedback(false, 'The correct position was (' + q.x + ', ' + q.y + ')');", "showFeedback(false, 'The correct position was (' + q.y + ', ' + q.x + ')');")]),
    ('the origin label back over the -1 labels (r-001)', 'covers',
     [("  ctx.textAlign = 'left';\n  ctx.textBaseline = 'bottom';\n  ctx.fillText('(0,0)', toCanvasX(0) + 6, toCanvasY(0) - 6);",
       "  ctx.textAlign = 'right';\n  ctx.textBaseline = 'top';\n  ctx.fillText('(0,0)', toCanvasX(0) - 6, toCanvasY(0) + 6);")]),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    st = play(fails, html)
    print('%s: %d plot, %d read and %d shape questions recomputed; every grid point tapped on the canvas for each plot and '
          'shape question, every option pressed for each read question, in Chromium' % (
              SLUG, st.get('plot', 0), st.get('read', 0), st.get('shape', 0)))
    ok = True
    if not args.no_selftest and not args.against:
        for what, tag, edits in PLANTS:
            bad = [o for o, n in edits if html.count(o) != 1]
            if bad:
                print('  self-test %-54s *** CANNOT PLANT (%r) ***' % (what, bad[0][:60]))
                ok = False
                continue
            planted = html
            for o, n in edits:
                planted = planted.replace(o, n)
            rep = []
            play(rep, planted)
            hit = [f for f in rep if tag in f]
            ok = ok and bool(hit)
            print('  self-test %-54s %s' % (what, ('caught: ' + hit[0][:100]) if hit else '*** MISSED ***'))
    for f in fails[:40]:
        print('FAIL  ' + f[:400])
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
