#!/usr/bin/env python3
# ci-line: Trig Wars (each side scores its own hits; the trig panel's numbers agree; hits found along the path; miss advice true by the physics) |
"""Trig Wars: scoring by side, the trig panel, hit detection and the miss advice, against the game's own physics.

Trig Wars is an artillery game (canvas, two sides of three tanks, turns). It has no question bank; what a student is
told and scored on comes from the physics, so this verifier carries its own copy of it and plays the page in Chromium
through the controls both the old and the fixed page share (the sliders, FIRE, cpuShot):

  Physics (Python, the game's own rules): ty(x) terrain, Euler per frame (x += vx; vy += 0.28; y += vy), launch from
    the side's end tank at (x + 22 dir, y - 13), V scaled by 0.28. A shot hits when the path drawn between two frames
    enters an enemy tank's hit circle (r = 22, centre 10px above the tank) before it reaches the ground.
  Scoring (trig-wars-t2-001; Jon's ruling, 8 Oct 2026): VS CPU, a hit counts only for the side that fired it; the
    score is Player 1's hits, questions_answered Player 1's shots, question_answered only for Player 1's shots, and
    submitScore once, win or lose. 2 PLAYER submits nothing (no submitScore, no device history). Three battles are
    played: Player 1 misses and the CPU wins; Player 1 wins and the CPU misses; 2 PLAYER, Player 2 wins.
  Trig panel (t2-002, t2-005): for a grid of angles and powers, Vx and Vy are V cos(theta) and V sin(theta) to 1 d.p.
    with V the power shown, so cos = Vx/V and sin = Vy/V hold for the numbers on screen; no "u/s" unit.
  Hits (t2-003): layouts where the old per-frame test (ground first, frame points only) misses a shell whose path
    goes through a tank, both kinds (the frame that enters the circle is below ground; the shell crosses the circle
    between frames): each must hit. A few true misses must stay misses.
  Miss advice (t2-004): every change the message suggests (steeper or shallower angle, more or less power) must,
    for some step of 1 to 8, land nearer the nearest enemy (or hit), by the physics; checked over angles either side
    of 45 degrees and shells stopped by the hill.
  SR-14 (t2-006): the four lines the audit named are gone.
A self-test plants three of the audit's faults back into a copy of the page (t2-001 the shared score, t2-002 the
0.28 in the panel, t2-003 the ground tested first); each must FAIL naming its entry.

    python scripts/verify-trig-wars.py [--no-selftest] [--against FILE]
"""
import argparse
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'trig-wars'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
BW, BH, G, HIT_R = 1100, 310, 0.28, 22

# ── The physics (the game's own rules) ────────────────────────────────────────


def ty(x):
    if x < 170 or x > 730:
        return BH - 65
    t = (x - 170) / 560
    return (BH - 65 - 52 * math.sin(t * math.pi) - 18 * math.sin(t * math.pi * 3)
            - 10 * math.sin(t * math.pi * 5.5 + 0.5))


def off(x, y):
    return y >= ty(x) or x < -10 or x > BW + 10


def path(tanks, p, ang, pwr, sc=0.0):
    """Frame points of a shot by side p, from its launch to the first frame the game's ground/edge test fires."""
    alive = [t for t in tanks[p] if t['alive']]
    src = alive[-1] if p == 1 else alive[0]
    d = 1 if p == 1 else -1
    rad = ang * math.pi / 180
    x, y = src['x'] + d * 22, src['y'] - 13
    vx, vy = d * pwr * math.cos(rad + sc) * 0.28, -pwr * math.sin(rad + sc) * 0.28
    pts = [(x, y)]
    for _ in range(4000):
        x += vx; vy += G; y += vy
        pts.append((x, y))
        if off(x, y):
            break
    return pts


def seg_enter(a, b, c, r):
    (ax, ay), (bx, by) = a, b
    dx, dy, fx, fy = bx - ax, by - ay, ax - c[0], ay - c[1]
    C = fx * fx + fy * fy - r * r
    if C < 0:
        return 0.0
    A, B = dx * dx + dy * dy, 2 * (fx * dx + fy * dy)
    disc = B * B - 4 * A * C
    if A == 0 or disc < 0:
        return None
    t = (-B - math.sqrt(disc)) / (2 * A)
    return t if 0 <= t <= 1 else None


def outcome(tanks, p, ang, pwr, sc=0.0):
    """(hit tank index or None, landing x): the first of 'enters an enemy hit circle' and 'reaches the ground'."""
    pts = path(tanks, p, ang, pwr, sc)
    enemy = [(i, t) for i, t in enumerate(tanks[2 if p == 1 else 1]) if t['alive']]
    for a, b in zip(pts, pts[1:]):
        hit = None
        for i, t in enemy:
            u = seg_enter(a, b, (t['x'], t['y'] - 10), HIT_R)
            if u is not None and (hit is None or u < hit[0]):
                hit = (u, i)
        g = None
        if off(*b):
            lo, hi = 0.0, 1.0
            for _ in range(40):
                m = (lo + hi) / 2
                if off(a[0] + (b[0] - a[0]) * m, a[1] + (b[1] - a[1]) * m):
                    hi = m
                else:
                    lo = m
            g = hi
        if hit and (g is None or hit[0] <= g):
            return hit[1], None
        if g is not None:
            return None, a[0] + (b[0] - a[0]) * g
    return None, pts[-1][0]


def old_hit(tanks, p, ang, pwr):
    """The game before the fix: per frame, the ground first, then the hit test at the frame point."""
    pts = path(tanks, p, ang, pwr)
    enemy = [t for t in tanks[2 if p == 1 else 1] if t['alive']]
    for x, y in pts[1:]:
        if off(x, y):
            return False
        if any(math.hypot(x - t['x'], y - (t['y'] - 10)) < HIT_R for t in enemy):
            return True
    return False


_AIM = {}


def aim(tanks, p, hit=True):
    """A shot for side p that hits (robust to the game's +-0.009 scatter), or the sure miss 85 degrees, power 20."""
    if not hit:
        return 85, 20
    key = (p, tuple((t['x'], t['alive']) for side in (1, 2) for t in tanks[side]))
    if key not in _AIM:
        _AIM[key] = _aim(tanks, p)
    return _AIM[key]


def _aim(tanks, p):
    for ang in range(45, 4, -1):
        for pwr in range(20, 101):
            if all(outcome(tanks, p, ang, pwr, sc)[0] is not None for sc in (-0.009, 0.0, 0.009)):
                return ang, pwr
    raise RuntimeError('no hitting shot for side %d' % p)


def nearer(tanks, p, ang, pwr, land_x, d_ang, d_pwr):
    """Does a change of 1-8 steps (d_ang degrees, d_pwr power) land nearer the nearest enemy than land_x, or hit?"""
    enemies = [t['x'] for t in tanks[2 if p == 1 else 1] if t['alive']]
    tgt = min(enemies, key=lambda e: abs(land_x - e))
    base = abs(land_x - tgt)
    for k in range(1, 9):
        a, w = ang + d_ang * k, pwr + d_pwr * k
        if not (5 <= a <= 85 and 20 <= w <= 100):
            break
        h, lx = outcome(tanks, p, a, w)
        if h is not None or abs(lx - tgt) < base - 0.5:   # a real gain, not floating-point noise
            return True
    return False


# Phrases that advise a change, old and new wording, and the direction each claims.
ADVICE = [
    (r'steeper angle|bump the angle|angle or the power up', (1, 0)),
    (r'shallower angle|angle down', (-1, 0)),
    (r'more power|power up|V was too low|needs more to work with', (0, 1)),
    (r'less power', (0, -1)),
]
SR14 = ['shooting yourself', 'did themselves in', 'WE LOST ONE', "'💀 DOWN!'"]

# ── Chromium ──────────────────────────────────────────────────────────────────
INIT = r"""(() => {
  try { localStorage.setItem('mfg_tw_briefed', 'true'); } catch (e) {}
  // Fast clock for the game's pauses and animation frames (the physics is per frame, so nothing else changes).
  const st = window.setTimeout.bind(window);
  window.setTimeout = (f, ms, ...a) => st(f, Math.min(ms || 0, 2000) / 100, ...a);
  // Animation frames run at once (a flight is a chain of frames; the physics is per frame, so the result is the
  // same); past a depth of 2000 a frame waits for a timer instead, so no chain can overflow the stack.
  let depth = 0;
  window.requestAnimationFrame = (f) => {
    if (depth > 2000) { st(() => f(performance.now()), 0); return 0; }
    depth++; try { f(performance.now()); } finally { depth--; } return 0;
  };
  // Seeded Math.random, so a run is the same every time.
  let s = 12345;
  Math.random = () => { s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
})();"""

HOOK = r"""() => {
  window.__ev = []; window.__sub = []; window.__hist = [];
  if (window.__hooked) return;          // wrap mfg once: a second wrapper would record every event twice
  window.__hooked = true;
  const m = window.mfg;
  window.mfg = function (e, p) { window.__ev.push([e, JSON.parse(JSON.stringify(p || {}))]); return m && m.apply(this, arguments); };
  window.MaffsLeaderboard = { submitScore: (...a) => { window.__sub.push(a); return Promise.resolve(); } };
  window.MaffsScoreHistory = { record: (...a) => { window.__hist.push(a); } };
}"""

STATE = """() => ({turn, over, mode, tanks: {1: tanks[1].map(t => ({x: t.x, y: t.y, alive: t.alive})),
                                       2: tanks[2].map(t => ({x: t.x, y: t.y, alive: t.alive}))},
        p1msg: document.getElementById('p1msg').textContent, p2msg: document.getElementById('p2msg').textContent,
        p1fire: !document.getElementById('p1fire').disabled, p2fire: !document.getElementById('p2fire').disabled})"""


def js_tanks(t):
    """Tanks for page.evaluate (JSON keys are strings; JS reads t[1] as t['1'])."""
    return {str(k): v for k, v in t.items()}


def state(page):
    st = page.evaluate(STATE)
    st['tanks'] = {int(k): v for k, v in st['tanks'].items()}
    return st


def set_shot(page, p, ang, pwr):
    page.evaluate("([p, a, w]) => { document.getElementById('p' + p + 'ang').value = a; "
                  "document.getElementById('p' + p + 'pwr').value = w; }", [p, ang, pwr])


def wait(page, js, ms=20000):
    page.wait_for_function(js, timeout=ms)


def battle(page, mode, p1_hits, p2_hits):
    """Play one battle to the end. Each side fires its sure miss or a hitting shot. Returns (events, submits, hist)."""
    page.evaluate("(m) => { setMode(m); }", mode)
    page.evaluate(HOOK)
    if mode == 'cpu':
        # The CPU fires what the verifier sets in __cpu (the game's own cpuShot aims at random).
        page.evaluate("""() => { window.cpuShot = function () { if (over) return;
            document.getElementById('p2ang').value = window.__cpu[0]; document.getElementById('p2pwr').value = window.__cpu[1];
            fire(2); }; }""")
    for _ in range(40):
        st = state(page)
        if st['over']:
            break
        p = st['turn']
        if mode == 'cpu' and p == 2:
            wait(page, '() => over || turn === 1')
            continue
        ang, pwr = aim(st['tanks'], p, p1_hits if p == 1 else p2_hits)
        if mode == 'cpu':
            # the CPU's reply, for the tanks as they will be after this shot (a miss changes nothing; a hit is
            # aimed again on its next turn)
            page.evaluate("(s) => { window.__cpu = s; }", list(aim(st['tanks'], 2, p2_hits)))
        set_shot(page, p, ang, pwr)
        page.evaluate("(p) => document.getElementById('p' + p + 'fire').click()", p)
        if mode == 'cpu':       # back to Player 1 once the CPU has replied
            wait(page, "() => over || (turn === 1 && !document.getElementById('p1fire').disabled)")
        else:                   # the other side's turn
            wait(page, "(p) => over || (turn !== %d && !document.getElementById('p' + turn + 'fire').disabled)" % p)
    wait(page, '() => over')
    page.wait_for_timeout(200)
    return page.evaluate('() => [window.__ev, window.__sub, window.__hist]')


def check_scoring(fails, page):
    tag = 'trig-wars-t2-001'
    # 1. VS CPU: Player 1 never hits; the CPU wins.
    ev, sub, hist = battle(page, 'cpu', False, True)
    qa = [p for e, p in ev if e == 'question_answered']
    gc = [p for e, p in ev if e == 'game_completed']
    shots = len(qa)
    if any(p.get('correct') for p in qa):
        fails.append('%s: VS CPU, Player 1 never hit, yet a question_answered says correct (the CPU\'s hits counted)' % tag)
    if len(gc) != 1 or gc[0].get('score') != 0:
        fails.append('%s: VS CPU, Player 1 never hit and lost 3-0: game_completed %s (score must be 0)' % (tag, gc))
    if len(sub) != 1 or sub[0][2] != 0:
        fails.append('%s: VS CPU, Player 1 never hit: submitScore %s (once, score 0)' % (tag, sub))
    elif sub[0][3] != shots or (gc and gc[0].get('questions_answered') != shots):
        fails.append('%s: VS CPU: questions_answered %s / submitScore %s, Player 1 fired %d (the CPU\'s shots counted)'
                     % (tag, gc and gc[0].get('questions_answered'), sub[0][3], shots))
    if shots != 3:
        fails.append('%s: VS CPU: %d question_answered for a battle of 3 Player 1 shots (only Player 1\'s shots)' % (tag, shots))
    # 2. VS CPU: Player 1 wins; the CPU always misses.
    ev, sub, hist = battle(page, 'cpu', True, False)
    qa = [p for e, p in ev if e == 'question_answered']
    if len(sub) != 1 or sub[0][2:4] != [3, 3] or [p.get('correct') for p in qa] != [True] * 3:
        fails.append('%s: VS CPU, Player 1 hit with all 3 shots: submitScore %s, marks %s (3, 3; three right)'
                     % (tag, sub, [p.get('correct') for p in qa]))
    # 3. 2 PLAYER: Player 2 wins. Nothing reaches the leaderboard or the device history (Jon, 8 Oct 2026).
    ev, sub, hist = battle(page, 'human', False, True)
    gc = [p for e, p in ev if e == 'game_completed']
    if sub or hist:
        fails.append('%s: 2 PLAYER submitted %s / recorded %s (two people on one device: nothing is submitted)' % (tag, sub, hist))
    if len(gc) != 1:
        fails.append('%s: 2 PLAYER: game_completed %d time(s) (once)' % (tag, len(gc)))


def check_panel(fails, page):
    page.evaluate("() => { setMode('cpu'); }")
    bad = 0
    for ang in range(5, 86, 4):
        for pwr in range(20, 101, 7):
            set_shot(page, 1, ang, pwr)
            rows = page.evaluate("() => { refreshTrig(); return [...document.querySelectorAll('#trigTable tr')].map(r => r.textContent); }")
            txt = ' | '.join(rows)
            nums = {}
            for r in rows:
                m = re.search(r'(sin|cos|tan)\(\d+°\).*?(-?[\d.]+|∞)\s*$', r)
                if m:
                    nums[m.group(1)] = m.group(2)
                m = re.search(r'V([xy]) \((horizontal|vertical)\)\s*(-?[\d.]+)', r)
                if m:
                    nums['V' + m.group(1)] = float(m.group(3))
            rad = math.radians(ang)
            ok = True
            if 'u/s' in txt and not any(f.startswith('trig-wars-t2-005') for f in fails):
                fails.append('trig-wars-t2-005: the panel labels Vx and Vy "u/s"; they are in V\'s own units')
            for key, f in (('Vx', math.cos), ('Vy', math.sin)):
                v = nums.get(key)
                if v is None or abs(v - pwr * f(rad)) > 0.051:
                    ok = False
                    why = '%s shown %s, V = %d so V %s(%d) = %.2f' % (key, v, pwr, 'cos' if key == 'Vx' else 'sin', ang, pwr * f(rad))
                    break
            if not ok:
                bad += 1
                if bad <= 3:
                    fails.append('trig-wars-t2-002 panel at %d deg, V %d: %s' % (ang, pwr, why))
    if bad > 3:
        fails.append('trig-wars-t2-002: %d more panel settings disagree' % (bad - 3))


def layouts():
    """Tank layouts with shots the old test misses, both kinds, and true misses near a tank."""
    gf, tun, miss = [], [], []
    for p1 in (30, 60, 90):
        for p2 in (760, 800, 840):
            tanks = {1: [{'x': p1 + 46 * k, 'y': ty(p1 + 46 * k), 'alive': True} for k in range(3)],
                     2: [{'x': p2 + 46 * k, 'y': ty(p2 + 46 * k), 'alive': True} for k in range(3)]}
            for ang in range(15, 76, 3):
                for pwr in range(55, 101, 1):
                    h, lx = outcome(tanks, 1, ang, pwr)
                    if h is not None and not old_hit(tanks, 1, ang, pwr):
                        pts = path(tanks, 1, ang, pwr)
                        framed = any(math.hypot(x - t['x'], y - (t['y'] - 10)) < HIT_R
                                     for x, y in pts[1:] for t in tanks[2])
                        (gf if framed else tun).append((tanks, ang, pwr))
                    elif h is None and lx is not None and len(miss) < 40 and min(abs(lx - t['x']) for t in tanks[2]) < 40:
                        miss.append((tanks, ang, pwr))
    return gf[::max(1, len(gf) // 4)][:4], tun[::max(1, len(tun) // 4)][:4], miss[::10][:3]


def fire_at(page, tanks, ang, pwr):
    """Set the layout, fire Player 1's shot with no scatter, return True if an enemy tank was hit."""
    page.evaluate("""(t) => { setMode('cpu'); window.cpuShot = function () {};
        for (const p of [1, 2]) t[p].forEach((v, i) => { tanks[p][i].x = v.x; tanks[p][i].y = v.y; tanks[p][i].alive = true; });
        draw(); }""", js_tanks(tanks))
    set_shot(page, 1, ang, pwr)
    page.evaluate("() => { const r = Math.random; Math.random = () => 0.5; document.getElementById('p1fire').click(); Math.random = r; }")
    wait(page, "() => turn === 2 || over")
    return page.evaluate("() => tanks[2].some(t => !t.alive)")


def check_hits(fails, page):
    gf, tun, miss = layouts()
    for kind, cases in (('the frame that enters the hit circle is below the ground', gf),
                        ('the shell crosses the hit circle between frames', tun)):
        for tanks, ang, pwr in cases:
            if not fire_at(page, tanks, ang, pwr):
                fails.append('trig-wars-t2-003: P1 at %d deg, V %d (tanks at %s): the path goes through a tank (%s) but '
                             'it scored a miss' % (ang, pwr, [round(t['x']) for t in tanks[2]], kind))
    for tanks, ang, pwr in miss:
        if fire_at(page, tanks, ang, pwr):
            fails.append('trig-wars: P1 at %d deg, V %d: a hit on a path that never reaches a tank\'s hit circle' % (ang, pwr))
    if not gf or not tun:
        fails.append('trig-wars-t2-003: the layout search found %d ground-first and %d between-frame cases (need both)'
                     % (len(gf), len(tun)))


def near_misses(tanks):
    """Shots that land 30-200px long or short of the nearest enemy, two each side of 45 degrees: where advice is given."""
    enemies = [t['x'] for t in tanks[2]]
    out = []
    for ang in (20, 32, 58, 70):
        got = {True: 0, False: 0}
        for pwr in range(30, 101, 3):
            h, lx = outcome(tanks, 1, ang, pwr)
            if h is not None or lx is None:
                continue
            tgt = min(enemies, key=lambda e: abs(lx - e))
            if 30 < abs(lx - tgt) < 200 and got[lx > tgt] < 1:
                got[lx > tgt] += 1
                out.append((ang, pwr, lx))
    return out


def check_advice(fails, page):
    bad = seen = 0
    for p1, p2 in ((30, 760), (90, 840), (60, 800)):
        tanks = {1: [{'x': p1 + 46 * k, 'y': ty(p1 + 46 * k), 'alive': True} for k in range(3)],
                 2: [{'x': p2 + 46 * k, 'y': ty(p2 + 46 * k), 'alive': True} for k in range(3)]}
        for ang, pwr, lx in near_misses(tanks):
                page.evaluate("(t) => { setMode('cpu'); window.cpuShot = function () {};"
                              "for (const p of [1, 2]) t[p].forEach((v, i) => { tanks[p][i].x = v.x; tanks[p][i].y = v.y; tanks[p][i].alive = true; }); }",
                              js_tanks(tanks))
                for _ in range(4):          # the old page picks its line at random: read four
                    page.evaluate("() => { turn = 1; over = false; setButtons(true); window.__msgs = []; "
                                  "if (window.MaffsLock) MaffsLock.fresh(document.querySelector('.p1-panel')); }")
                    set_shot(page, 1, ang, pwr)
                    # no scatter (the first draw); the game's later draws, such as the line it picks, stay random
                    page.evaluate("() => { const r = Math.random; let first = true; "
                                  "Math.random = () => first ? (first = false, 0.5) : r(); "
                                  "document.getElementById('p1fire').click(); Math.random = r; }")
                    wait(page, "() => turn === 2 || over")
                    # the miss message, as the game set it (it clears it again before the next turn)
                    text = page.evaluate("() => (window.__msgs.find(m => m[0] === 1 && m[1]) || [1, ''])[1]")
                    if not text:
                        fails.append('trig-wars-t2-004: %d deg, V %d: no message after a miss' % (ang, pwr))
                        continue
                    seen += 1
                    for rx, (da, dp) in ADVICE:
                        if re.search(rx, text) and not nearer(tanks, 1, ang, pwr, lx, da, dp):
                            bad += 1
                            if bad <= 4:
                                fails.append('trig-wars-t2-004: %d deg, V %d lands at x = %d (enemies %s): "%s" -- %s does not '
                                             'bring it nearer' % (ang, pwr, lx, [t['x'] for t in tanks[2]], text,
                                                                  'the advised angle change' if da else 'the advised power change'))
    if bad > 4:
        fails.append('trig-wars-t2-004: %d more false pieces of advice in %d misses read' % (bad - 4, seen))


def run(html):
    """[fail] for one copy of the page."""
    from playwright.sync_api import sync_playwright
    fails = []
    for s in SR14:
        if s in html:
            fails.append('trig-wars-t2-006 (SR-14): the page still says %r' % s)
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
            ctx.add_init_script(INIT)
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
            pat = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda u: not u.startswith(base), lambda r: r.abort())
            ctx.route(lambda u: bool(pat.search(u)), lambda r: r.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function("typeof fire === 'function' && typeof refreshTrig === 'function'", timeout=8000)
            page.evaluate("() => { window.__msgs = []; const m0 = msg; "
                          "msg = function (p, t) { window.__msgs.push([p, t]); return m0(p, t); }; }")
            for check in (check_scoring, check_panel, check_hits, check_advice):
                try:
                    check(fails, page)
                except Exception as e:      # a page that never reaches the state a check waits for fails it
                    fails.append('%s: %s' % (check.__name__, str(e).splitlines()[0][:160]))
            errs = [e for e in errors if 'firebase' not in e.lower()]
            if errs:
                fails.append('page errors: %s' % '; '.join(errs[:3]))
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return fails


PLANTS = [
    ('trig-wars-t2-001', 't2-001: every hit counts for Player 1',
     'const sc=_twHits[1], n=_twShots[1];', 'const sc=_twHits[1]+_twHits[2], n=_twShots[1]+_twShots[2];'),
    ('trig-wars-t2-002', 't2-002: Vx scaled by 0.28 beside V',
     'const vxV=(pwr*cosV).toFixed(1);', 'const vxV=(pwr*cosV*0.28).toFixed(1);'),
    ('trig-wars-t2-003', 't2-003: the ground tested before the hit',
     'if(hit && tHit<=tGround) return', 'if(hit && tGround>1) return'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = run(html)
    print('%s: scoring by side in 3 battles, the trig panel at %d settings, hits along the path, the miss advice by the physics'
          % (SLUG, len(range(5, 86, 4)) * len(range(20, 101, 7))))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-46s *** CANNOT PLANT ***' % what)
                ok = False
                continue
            hit = [f for f in run(html.replace(old, new)) if f.startswith(tag)]
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
