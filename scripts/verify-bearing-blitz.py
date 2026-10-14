#!/usr/bin/env python3
# ci-line: Bearing Blitz (every whole-degree bearing dragged on the real compass and read back; the needle drawn checked; hit, miss, points and message figures recomputed around 0/360; lives and end flows played in Chromium) |
"""Bearing Blitz: a target bearing is shown ("045°"); the student drags the needle by eye and fires; within ±5° is a hit.

Generated, not banked: `generateBearings()` gives 16 fixed bearings (0, 30, 45, 60, 90, ... 330) and 8 drawn from 0..359, shuffled;
a game is at most 20 targets. There is no option list: the key is the target bearing and the mark is the angle between the needle
and it. Coverage: all 360 whole-degree bearings are dragged and read back, and hit/miss marking is played for 38 targets (the 16
fixed, 0, 359, 1, 180 and others spread round the circle) at needle offsets of -10..+10 degrees, so every wrap across 0/360 is tried.

Checks, independent of the game's code (bearings measured clockwise from North, Python's math):
  Reading the needle: a mouse press at the canvas point at bearing B (60% of the radius out, in the drawn compass's own pixel
    frame) sets the needle to B, for every whole degree; the needle is then drawn pointing at B (its colour at 60% of the radius
    along B and not along B + 90, B + 180 or B + 270).
  Display: the target reads as three digits and a degree sign ("005°"); North is marked at the top.
  Marking (each shot through the game's own Fire button): the error is the shorter way round, min(|n - t|, 360 - |n - t|); 5 or
    under is a hit worth 150 (0-1 off), 100 (2-3) or 50 (4-5), and the message reads "💥 HIT! Target was TTT° — you were D° off. +P
    points"; over 5 is a miss that costs a life, shows the target line, and reads "... You were D° off. Target was TTT°. N lives
    left!" with the Next control.
  Sessions: startGame() dealt five times: 24 bearings, whole numbers 0..359, the 16 fixed ones all present.
  Flows: three misses read "HIT! Surface ships locked onto your position." and Next shows "Submarine Destroyed!" with the shots, hits and accuracy; twenty hits end
    with "All Ships Sunk!" and the score added up here.
No analytics or leaderboard request leaves the stub server (every other request is aborted).

    python scripts/verify-bearing-blitz.py [--no-selftest] [--against FILE]
"""
import argparse
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'bearing-blitz'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
FIXED = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]
TARGETS = sorted(set(FIXED + [359, 1, 180] + [(17 * k + 7) % 360 for k in range(21)]))
NEEDLE_RGB = (6, 182, 212)          # #06b6d4


def err(n, t):
    d = abs(n - t) % 360
    return min(d, 360 - d)


def bearing_of(cx, cy, left, top, w, h):
    """The bearing, clockwise from North, of a whole-pixel press at (cx, cy) in the compass's 320-unit frame."""
    x = (cx - left) * 320 / w - 160
    y = (cy - top) * 320 / h - 160
    return math.degrees(math.atan2(x, -y)) % 360


def press_point(b, left, top, w, h):
    """A whole-pixel point near bearing b, 0.9 of the radius out, whose own bearing is within 0.35 degrees of b."""
    fx = left + (160 + 145 * 0.9 * math.sin(math.radians(b))) * w / 320
    fy = top + (160 - 145 * 0.9 * math.cos(math.radians(b))) * h / 320
    best = None
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            cx, cy = round(fx) + dx, round(fy) + dy
            e = abs((bearing_of(cx, cy, left, top, w, h) - b + 180) % 360 - 180)
            if best is None or e < best[0]:
                best = (e, cx, cy)
    assert best[0] < 0.35, (b, best)
    return [best[1], best[2]]


def points(d):
    return 150 if d <= 1 else 100 if d <= 3 else 50


RECT_JS = "() => { const r = canvas.getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; }"
PRESS_JS = r"""(pts) => {
  // pts: [bearing, clientX, clientY], chosen in Python on whole pixels; the compass is drawn in a 320-unit frame centred (160, 160)
  const out = [];
  const dpr = canvas.width / 320;
  const isNeedle = (x, y) => { const d = ctx.getImageData(Math.round(x * dpr), Math.round(y * dpr), 1, 1).data;
    return Math.abs(d[0] - %d) < 30 && Math.abs(d[1] - %d) < 30 && Math.abs(d[2] - %d) < 30; };
  const at = (b, f) => [160 + 145 * f * Math.sin(b * Math.PI / 180), 160 - 145 * f * Math.cos(b * Math.PI / 180)];
  for (const [b, cx, cy] of pts) {
    canvas.dispatchEvent(new MouseEvent('mousedown', {clientX: cx, clientY: cy, bubbles: true}));
    document.dispatchEvent(new MouseEvent('mouseup', {bubbles: true}));
    out.push({b: b, read: currentAngle, along: isNeedle(...at(b, 0.6)),
              off: [90, 180, 270].map(o => isNeedle(...at(b + o, 0.6)))});
  }
  return out;
}""" % NEEDLE_RGB
SHOT_JS = r"""([t, n]) => {
  startGame(); MaffsLock.clearTimers();
  bearings.length = 0; bearings.push(t); sunkCount = 0; nextTarget();
  const shown = document.getElementById('targetBearing').textContent;
  currentAngle = n; drawCompass();
  document.getElementById('fireBtn').click();
  const res = {shown: shown, msg: document.getElementById('message').textContent, score: score, lives: livesLeft, sunk: sunkCount,
               next: document.getElementById('nextMount').querySelectorAll('button').length};
  MaffsLock.clearTimers();
  return res;
}"""
SESSION_JS = r"""() => { const out = [];
  for (let k = 0; k < 5; k++) { startGame(); MaffsLock.clearTimers(); out.push(bearings.slice()); }
  return out; }"""
SURV_JS = r"""(lives) => {
  startGame(); MaffsLock.clearTimers(); livesLeft = lives;
  for (let k = 0; k < 20; k++) {
    currentAngle = targetBearing; drawCompass();
    document.getElementById('fireBtn').click();
    MaffsLock.clearTimers();
    nextTarget();
  }
  return {stats: document.getElementById('statsLine').textContent};
}"""
WIN_JS = r"""(offs) => {
  startGame(); MaffsLock.clearTimers();
  const ts = [];
  for (let k = 0; k < 20; k++) {
    ts.push(targetBearing);
    currentAngle = (targetBearing + offs[k] + 360) % 360; drawCompass();
    document.getElementById('fireBtn').click();
    MaffsLock.clearTimers();
    nextTarget();
  }
  return {ts: ts, title: document.getElementById('resultTitle').textContent, score: document.getElementById('finalScore').textContent,
          stats: document.getElementById('statsLine').textContent};
}"""


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
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.clock.install()
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof generateBearings === "function" && typeof fire === "function"', timeout=15000)
            page.evaluate('() => { startGame(); MaffsLock.clearTimers(); }')
            # reading and drawing the needle, every whole degree
            left, top, w, h = page.evaluate(RECT_JS)
            pts = []
            for b in range(360):
                pts.append([b] + press_point(b, left, top, w, h))
            for r in page.evaluate(PRESS_JS, pts):
                if r['read'] != r['b']:
                    fails.append('needle: a press at bearing %d reads %r (bearings run clockwise from North)' % (r['b'], r['read']))
                    break
                if not r['along'] or any(r['off']):
                    fails.append('needle: at bearing %d the needle is not drawn along it (along %s, at +90/180/270 %s)' % (r['b'], r['along'], r['off']))
                    break
            north = page.evaluate('() => { const d = ctx.getImageData(Math.round(160 * canvas.width / 320), Math.round((160 - 145 - 3) * canvas.width / 320), 1, 1).data; return [d[0], d[1], d[2]]; }')
            if not (north[0] > 180 and north[1] < 120):
                fails.append('needle: no North marker drawn at the top of the compass (pixel %r)' % north)
            # marking, around the circle
            n_shots = 0
            for t in TARGETS:
                for off in range(-10, 11):
                    n = (t + off) % 360
                    r = page.evaluate(SHOT_JS, [t, n])
                    n_shots += 1
                    d = err(n, t)
                    if r['shown'] != '%03d°' % t:
                        fails.append('display: target %d shows %r' % (t, r['shown']))
                    if d <= 5:
                        p = points(d)
                        want = '💥 HIT! Target was %03d° — you were %d° off. +%d points' % (t, d, p)
                        ok = r['msg'] == want and r['score'] == p and r['sunk'] == 1 and r['lives'] == 3
                    else:
                        want = "💣 Depth charge dropped nearby! You were %d° off. Target was %03d°. 2 lives left!" % (d, t)
                        ok = r['msg'] == want and r['score'] == 0 and r['sunk'] == 0 and r['lives'] == 2 and r['next'] >= 1
                    if not ok:
                        fails.append('marking: target %03d, needle %03d (%d° off): %r, score %d, lives %d, expected %r' % (
                            t, n, d, r['msg'], r['score'], r['lives'], want))
                        break
            for bs in page.evaluate(SESSION_JS):
                if len(bs) != 24 or any(not isinstance(b, int) or not 0 <= b <= 359 for b in bs) or any(f not in bs for f in FIXED):
                    fails.append('session: bearings %r: expected 24 whole numbers 0..359 including the 16 fixed' % bs)
                    break
            page.evaluate('() => { startGame(); MaffsLock.clearTimers(); }')
            msgs = []
            for _ in range(3):
                page.evaluate('() => { currentAngle = (targetBearing + 180) % 360; drawCompass(); document.getElementById("fireBtn").click(); }')
                msgs.append(page.evaluate('() => document.getElementById("message").textContent'))
                page.clock.run_for(1000)
                page.locator('#nextMount button').first.click()
            lose = page.evaluate('() => ({title: document.getElementById("resultTitle").textContent, stats: document.getElementById("statsLine").textContent, active: document.getElementById("results").classList.contains("active")})')
            lose['msgs'] = msgs
            want_last = 'HIT! Surface ships locked onto your position.'
            if (len(lose['msgs']) != 3 or 'Depth charge dropped nearby!' not in lose['msgs'][0] or "They're getting closer!" not in lose['msgs'][1]
                    or want_last not in lose['msgs'][2] or lose['title'] != 'Submarine Destroyed!' or not lose['active']
                    or '0 ships sunk from 3 torpedoes' not in lose['stats'] or 'Accuracy: 0%' not in lose['stats']):
                fails.append('flow: three misses read %r, then %r / %r' % (lose['msgs'], lose['title'], lose['stats']))
            offs = [(k % 11) - 5 for k in range(20)]
            win = page.evaluate(WIN_JS, offs)
            total = sum(points(abs(o)) for o in offs)
            if win['title'] != 'All Ships Sunk!' or win['score'] != str(total) or '20 ships sunk from 20 torpedoes' not in win['stats'] \
                    or 'Accuracy: 100%' not in win['stats']:
                fails.append('flow: twenty hits end %r, score %r (expected %d), %r' % (win['title'], win['score'], total, win['stats']))
            # SWEEP-1 (bearing-blitz-s1-002, R1): "Survived with 1 life", "... 2 lives"
            for lives, want in ((1, 'Survived with 1 life'), (2, 'Survived with 2 lives')):
                surv = page.evaluate(SURV_JS, lives)
                if want not in surv['stats'] or 'Survived with 1 lives' in surv['stats']:
                    fails.append('flow: twenty hits with %d life left read %r, expected %r' % (lives, surv['stats'], want))
            # SWEEP-1 (bearing-blitz-s1-001, -003, R6, R2): no death imagery, and the start screen says a miss repeats the target
            page.evaluate('() => { show("menu"); }')
            menu = page.inner_text('#menu')
            if 'Fire first.' not in menu or 'Fire or die' in menu:
                fails.append('start: the subtitle must read "Fire first." (SR-14: no "Fire or die", bearing-blitz-s1-001)')
            if 'same target again' not in menu:
                fails.append('start: the start screen must say that after a miss you get the same target again (bearing-blitz-s1-003)')
            for bad in ('💀', 'DESTROYED!'):
                if bad in html:
                    fails.append('start: the page still carries %r (SR-14 death imagery, bearing-blitz-s1-005)' % bad)
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            browser.close()
            stats = {'shots': n_shots}
    finally:
        proc.terminate()
        proc.wait()
    return stats


PLANTS = [
    ('s1-001: "Fire or die" back', 'start:', [("Fire first.</div>", "Fire or die.</div>")]),
    ('s1-005: the skull and DESTROYED back', 'start:', [("msg.textContent='HIT! Surface", "msg.textContent='💀 DESTROYED! Surface")]),
    ('s1-002: "Survived with 1 lives" back', 'flow:', [("(livesLeft===1?' life':' lives')", "' lives'")]),
    ('s1-003: a repeated target not mentioned', 'start:', [(" After a miss you get the same target again.", "")]),
    ('a tolerance of 8 degrees', 'marking:', [("const TOLERANCE=5,MAX_TARGETS=20;", "const TOLERANCE=8,MAX_TARGETS=20;")]),
    ('no wrap at 0/360 (359 is 359 off 0)', 'marking:', [("if(diff>180)diff=360-diff;", "")]),
    ('the 100-point band at 2 degrees', 'marking:', [("else if(diff<=3)pts=100;", "else if(diff<=2)pts=100;")]),
    ('a wrong figure in the hit message', 'marking:', [("'° — you were '+diff+'° off.", "'° — you were '+(diff+1)+'° off.")]),
    ('bearings read anticlockwise from East', 'needle:', [("let angle=Math.atan2(x,-y)*180/Math.PI;", "let angle=Math.atan2(-y,x)*180/Math.PI;")]),
    ('the needle drawn a quarter turn out', 'needle:', [("const needleRad=(currentAngle-90)*Math.PI/180;", "const needleRad=(currentAngle)*Math.PI/180;")]),
    ('the target shown as the back bearing', 'display:',
     [("document.getElementById('targetBearing').textContent=pad3(targetBearing)+'°';",
       "document.getElementById('targetBearing').textContent=pad3((targetBearing+180)%360)+'°';")]),
    ('a fixed bearing dropped from the session', 'session:', [("const fixed=[0,30,45,60,", "const fixed=[0,30,60,")]),
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
    print('%s: all 360 bearings pressed on the compass and read back with the needle drawn; %d shots marked over %d targets at -10..+10 '
          'degrees; sessions and both end flows played in Chromium' % (SLUG, st.get('shots', 0), len(TARGETS)))
    ok = True
    if not args.no_selftest and not args.against:
        for what, tag, edits in PLANTS:
            bad = [o for o, n in edits if html.count(o) != 1]
            if bad:
                print('  self-test %-58s *** CANNOT PLANT (%r) ***' % (what, bad[0][:60]))
                ok = False
                continue
            planted = html
            for o, n in edits:
                planted = planted.replace(o, n)
            rep = []
            play(rep, planted)
            found = [f for f in rep if f.startswith(tag)]
            ok = ok and bool(found)
            print('  self-test %-58s %s' % (what, ('caught: ' + found[0][:100]) if found else '*** MISSED ***'))
    for f in fails[:40]:
        print('FAIL  ' + f[:400])
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
