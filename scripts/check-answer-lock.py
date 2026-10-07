#!/usr/bin/env python3
# ci-line: L1 | Answer lock in play, part 1 (canon 7.6.0: self-test, static rules; migrated games played in Chromium) | --selftest && --part 1/2
# ci-line: L2 | Answer lock in play, part 2 (canon 7.6.0: migrated games played in Chromium) | --part 2/2
# ci-deps: schools/assets/answer-lock.js schools/assets/next-control.js scripts/check-site.py
"""Does every game mark through MaffsLock (canon §7.6.0), so that no repeat marks twice or finishes twice?

Every roster game that records question_answered is either MIGRATED (its own guards replaced by
schools/assets/answer-lock.js) or on NOT_YET. NOT_YET is reported, never failed, and may only shrink:
it must be a subset of NOT_YET_AT_START (the games when contract F1 began), so a new game cannot be put on
it. A game on NOT_YET that already loads answer-lock.js (the cloud lane adopts the lock in its own PRs) is
played and judged like a migrated one: its failures fail, and when it passes the home lane moves it to
MIGRATED. The one exception: while the game is on the cloud lane's remaining list (the `cloud-remaining:`
line in docs/handover/cloud.md), its failures are reported, not failed. That state ends when the cloud lane
takes the game off its list (contract LH, 7 Oct 2026). A missing list fails the check.

How the check produces a wrong answer is the game's own declaration, never this script's (contract LH): a
`<!-- maffs-lock-hint ... -->` comment in the game's page, holding JSON (canon §7.6.0; answer-lock.js's
header). Every migrated game has one; `{}` when the generic driver plays it unaided. Its keys are HINT_KEYS
below; a JS value may be a list of strings, joined with nothing between them.

A migrated game must, statically:
  - load answer-lock.js once (in either order with next-control.js: neither reads the other at load) and
    call MaffsLock.lock(, MaffsLock.fresh( or MaffsLock.screen(, and MaffsLock.finishOnce(;
  - declare a maffs-lock-hint that parses, with known keys only;
  - keep no local answered flag: no `answered = true` (or locked, answerLocked, choiceLocked, busy,
    canAnswer, isAnswering, acceptingInput ...) assignment of a boolean;
  - make no raw setTimeout: every timer goes through MaffsLock.timer. A line that must keep one (focus,
    an animation frame that marks nothing) says why in a `// lock-ok: <reason>` comment on that line.
and, in Chromium (game timers run at TIME_SCALE so a run takes seconds; MaffsLock's 300 ms window runs on
the real clock), at its first roster level:
  1. answer wrong (up to 8 questions to find one), then click every option of that question and press
     Enter and Space on each, all inside MaffsNext's floor: the score,
     the question_answered count and its correct count, game_completed and submitScore are unchanged;
  2. double-click Next (MaffsNext, or the game's own continue control): one advance, and its second click
     marks nothing on the next question;
  3. at 390px on a touch screen, answer wrong and double-tap Next: nothing marked by the second tap;
  4. tap through to the end quickly (each answer followed at once by its continue control, then the end
     screen tapped for a while, the way formula-plug-in's reveal screen ran showResults twice): exactly one
     game_completed and at most one submitScore.
A game the driver cannot play (no option group, no input) is reported UNPLAYABLE and fails: its declaration
needs an "answer" (and whatever else it takes to reach a question).

    python scripts/check-answer-lock.py                    # every migrated game
    python scripts/check-answer-lock.py --game formula-plug-in [--against FILE]
    python scripts/check-answer-lock.py --not-yet          # play the NOT_YET games too (a report, never fails)
    python scripts/check-answer-lock.py --selftest         # a planted failing game off the cloud list is caught
    python scripts/check-answer-lock.py --part 1/2         # CI: every other migrated game (by slug); part 1 also
                                                           # runs the static rules. Add a part (and a group,
                                                           # L1-L4 in ci-groups.py) when a part passes 3 minutes.
"""
import argparse
import asyncio
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

TIME_SCALE = 0.25
WORKERS = 4

# The cloud lane's remaining list: the one `cloud-remaining: <slug> <slug> ...` line in its own handover. While a
# game is on it, a failure here is reported, not failed; the cloud lane takes a game off in the PR that finishes it.
CLOUD_HANDOVER = os.path.join(ROOT, 'docs', 'handover', 'cloud.md')
CLOUD_LIST = re.compile(r'`cloud-remaining:([^`]*)`')


def cloud_remaining(text=None):
    """The slugs on the cloud lane's remaining list; ValueError if the handover has no single such line."""
    if text is None:
        text = open(CLOUD_HANDOVER, encoding='utf-8').read()
    found = CLOUD_LIST.findall(text)
    if len(found) != 1:
        raise ValueError('docs/handover/cloud.md has %d `cloud-remaining:` lines (exactly one)' % len(found))
    return set(found[0].split())

# Every roster game that recorded question_answered when contract F1 began (7 Oct 2026). Frozen: never add
# to it. NOT_YET must stay a subset, so a new game is migrated from the start.
NOT_YET_AT_START = frozenset('''
52dle angle-ace bearing-blitz better-value binomial-blaster boolean-blitz chart-interrogator
characteristic-quest circle-theorem-spotter complex-converter component-crusher coordinate-geometry-dash
core-maths-paper1 core-maths-paper2a core-maths-paper2b core-maths-paper2c correlation-or-coincidence
curling-friction decimal-detective differentiation-duel dimension-checker distinctly-average
eigenvalue-extractor eigenvector-engine equatle equation-builder estimation-engine estimation-golf
expectation-station expected-damage factor-race factor-theorem fermi-lab force-resolver formula-forge
formula-plug-in formula-unlocked four-quadrant-explorer fraction-equivalence free-daily-pizza given-that
glorious-gantt gradient-hunter graph-sketcher graph-transformer growth-and-decay higher-power index-laws
integration-duel just-pythag-it-bruv like-terms-collector linear-equation-solver log-laws maths-court
matrix-crunch modular-battle moments-master negative-number-line new-shapes normal-navigator
partial-fractions-duel percentage-flip prime-factorisation prime-or-composite prisoners-dilemma
probability-paradox probability-pioneer proof-builder proportion-blaster quadratic-factoriser
scale-factor-scaling screening-room sequence-solver seven-bridges shape-shifter simultaneous-solver six-sevens-bruv
split-it spot-the-error spot-the-muppet standard-form-blitz stat-attack surd-simplifier suvat tax-theft
terrible-advice test-the-claim think-of-a-number trig-identity-duel trig-wars trig-worms truth-buster
truth-will-set-you-free unit-converter word-problem-decoder wrong-on-the-internet
'''.split())

# Migrated games. The home lane adds each: in the PR that migrates it, or, for a game the cloud lane migrated,
# once it passes here. NOT_YET is the rest: reported, never failed, and it may only shrink.
MIGRATED = set('''
formula-plug-in new-shapes four-quadrant-explorer like-terms-collector shape-shifter negative-number-line
think-of-a-number decimal-detective
prime-or-composite probability-pioneer factor-race prime-factorisation
percentage-flip fraction-equivalence equatle estimation-golf
suvat factor-theorem
dimension-checker curling-friction trig-worms component-crusher
differentiation-duel integration-duel spot-the-error expectation-station
eigenvector-engine proof-builder linear-equation-solver moments-master force-resolver
truth-will-set-you-free trig-identity-duel binomial-blaster partial-fractions-duel
'''.split())
NOT_YET = set(NOT_YET_AT_START) - MIGRATED

# A game's declaration (its maffs-lock-hint), keys: 'level' (the level key to load), 'start' (JS that reaches the
# first question), 'ready' (JS: true when a question is on screen), 'answer' (JS that submits an answer; gets `i`,
# the attempt; it may return a promise), 'surface' (a selector for an answer surface that is not an option group,
# such as a canvas: the repeat phase really clicks its centre and corners too), 'start_sel' (the control that
# starts a run, when it is not a Start button: double-clicked for real), 'keys' (the game's own answer keys:
# pressed on the page in the repeat phase, inside MaffsNext's floor), 'each' (JS run before each step of the
# tap-through: a wait the game measures on the real clock, which TIME_SCALE cannot shorten), 'mark_any' (the game
# logs only right answers, as a built answer does: the repeat phase follows any mark), 'repeat' (JS that presses
# every answer control of the marked question, where they are not an option group).
HINT_KEYS = {'level': str, 'start': str, 'ready': str, 'answer': str, 'surface': str, 'start_sel': str,
             'keys': list, 'each': str, 'mark_any': bool, 'repeat': str}
HINT_RE = re.compile(r'<!--\s*maffs-lock-hint\b[^\n]*\n(.*?)-->', re.S)


def read_hint(html):
    """(the game's declaration as a dict, [fault]). A JS value given as a list of strings is joined."""
    import json
    found = HINT_RE.findall(html)
    if len(found) != 1:
        return {}, ['declares maffs-lock-hint %d times (once; {} when the generic driver plays it)' % len(found)]
    try:
        raw = json.loads(found[0])
    except ValueError as e:
        return {}, ['its maffs-lock-hint is not JSON: %s' % e]
    if not isinstance(raw, dict):
        return {}, ['its maffs-lock-hint is not a JSON object']
    hint, faults = {}, []
    for k, v in raw.items():
        want = HINT_KEYS.get(k)
        if want is str and isinstance(v, list) and all(isinstance(x, str) for x in v):
            v = ''.join(v)
        if want is None:
            faults.append('its maffs-lock-hint has an unknown key %r (known: %s)' % (k, ', '.join(sorted(HINT_KEYS))))
        elif not isinstance(v, want):
            faults.append('its maffs-lock-hint %r is not a %s' % (k, want.__name__))
        else:
            hint[k] = v
    return hint, faults

INCLUDE = re.compile(r'<script\b[^>]*\bsrc="[^"]*schools/assets/answer-lock\.js"', re.I)
FLAG = re.compile(r'\b(answered|isAnswered|hasAnswered|answerLocked|choiceLocked|inputLocked|optionsLocked|'
                  r'locked|isLocked|busy|isBusy|canAnswer|canClick|acceptingInput|accepting|isAnswering|'
                  r'answering|processing|waitingForNext|awaitingNext)\s*=\s*(true|false)\b')
RAW_TIMER = re.compile(r'(?<![\w.])(?:window\.)?setTimeout\s*\(')


def load_check_site():
    spec = importlib.util.spec_from_file_location('check_site', os.path.join(HERE, 'check-site.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def roster_games():
    """[(slug, first level key)] for every roster game that records question_answered."""
    levels, order = bc.roster_levels()
    out = []
    for slug in order:
        p = os.path.join(ROOT, 'games', slug, 'index.html')
        if os.path.exists(p) and 'question_answered' in open(p, encoding='utf-8').read():
            out.append((slug, (levels.get(slug) or [None])[0]))
    return out


def scripts_of(html):
    """The page's inline game script text, with line numbers of the page."""
    out = []
    for m in re.finditer(r'<script\b(?![^>]*\bsrc=)[^>]*>(.*?)</script>', html, re.S | re.I):
        start = html.count('\n', 0, m.start(1)) + 1
        out.append((start, m.group(1)))
    return out


def static_faults(slug, html):
    faults = []
    inc = INCLUDE.findall(html)
    if len(inc) != 1:
        faults.append('loads answer-lock.js %d times (once)' % len(inc))
    faults += read_hint(html)[1]
    for call in ('MaffsLock.lock(', 'MaffsLock.finishOnce('):
        if call not in html:
            faults.append('never calls %s' % call[:-1])
    if 'MaffsLock.fresh(' not in html and 'MaffsLock.screen(' not in html:
        faults.append('never calls MaffsLock.fresh or MaffsLock.screen')
    for start, text in scripts_of(html):
        for k, line in enumerate(text.split('\n')):
            code = line.split('//')[0] if 'lock-ok:' not in line else ''
            m = FLAG.search(code)
            if m:
                faults.append(':%d keeps a local flag (%s = %s): ask MaffsLock.isLocked'
                              % (start + k, m.group(1), m.group(2)))
            if RAW_TIMER.search(code):
                faults.append(':%d raw setTimeout: use MaffsLock.timer, or say why on the line (// lock-ok: ...)'
                              % (start + k))
    return faults


INIT = r"""
(() => {
  // Game timers at TIME_SCALE; Date.now (and so MaffsLock's 300 ms window) on the real clock.
  const S = %(scale)s, st = window.setTimeout, si = window.setInterval;
  window.setTimeout = function (fn, ms, ...a) { return st.call(window, fn, (Number(ms) || 0) * S, ...a); };
  window.setInterval = function (fn, ms, ...a) { return si.call(window, fn, Math.max(1, (Number(ms) || 0) * S), ...a); };

  // Every analytics event, in full.
  window.__lockEvents = [];
  let real = null;
  Object.defineProperty(window, 'mfg', { configurable: true,
    get() { return function (e, p) {
      try { window.__lockEvents.push({ e: e, correct: p && p.correct, i: p && p.question_index }); } catch (x) {}
      if (typeof real === 'function') { try { return real.apply(this, arguments); } catch (x) {} }
    }; },
    set(v) { real = v; } });

  // submitScore is counted and never sent (and never opens the initials overlay).
  window.__lockSubmits = 0;
  let lb;
  Object.defineProperty(window, 'MaffsLeaderboard', { configurable: true,
    get() { return lb; },
    set(v) {
      if (v && typeof v === 'object' && typeof v.submitScore === 'function') {
        v.submitScore = function () { window.__lockSubmits++; return Promise.resolve(null); };
      }
      lb = v;
    } });

  window.__lockSnap = function () {
    const ev = window.__lockEvents;
    const scores = [...document.querySelectorAll('[id*="score" i], [class*="score" i]')]
      .filter(e => e.offsetParent !== null && e.children.length === 0).map(e => e.textContent.trim()).join('|');
    return {
      answered: ev.filter(r => r.e === 'question_answered').length,
      correct: ev.filter(r => r.e === 'question_answered' && r.correct === true).length,
      lastCorrect: (ev.filter(r => r.e === 'question_answered').slice(-1)[0] || {}).correct,
      completed: ev.filter(r => r.e === 'game_completed').length,
      submits: window.__lockSubmits,
      scores: scores
    };
  };

  function visible(el) {
    const r = el.getBoundingClientRect();
    if (r.width < 4 || r.height < 4) return false;
    const cs = getComputedStyle(el);
    return cs.display !== 'none' && cs.visibility !== 'hidden';
  }
  window.__lockRect = function (el) {
    if (!el) return null;
    el.scrollIntoView({ block: 'center', inline: 'center' });
    const r = el.getBoundingClientRect();
    return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
  };
  // The option group the probe found, as rectangles (for real clicks).
  window.__lockGroupRects = function () {
    return (window.__mfgGroup || []).map(e => window.__lockRect(e));
  };
  const CONTINUE_RE = /^(got it|next|continue|carry on|onward|ok|okay|keep going|see (your )?(results|scorecard)|show results|finish)\b/;
  window.__lockContinue = function () {
    const mn = document.querySelector('.maffs-next');
    window.__lockContEl = mn;
    if (mn && visible(mn)) return { rect: window.__lockRect(mn), ready: !mn.disabled, kind: 'maffs-next' };
    const grp = window.__mfgGroup || [];
    const els = [...document.querySelectorAll('button, [role="button"], a')].filter(e =>
      // A group of interstitial controls ("Keep going" / "Finish here") is not an answer group.
      visible(e) && !e.disabled && (grp.indexOf(e) === -1 ||
        /^(continue|keep going)\b/.test((e.textContent || '').trim().toLowerCase())));
    const hit = els.find(e => { const t = (e.textContent || '').trim().toLowerCase();
      return CONTINUE_RE.test(t) || t.indexOf('next question') !== -1; });
    window.__lockContEl = hit;
    return hit ? { rect: window.__lockRect(hit), ready: true, kind: (hit.textContent || '').trim().slice(0, 30) } : null;
  };
  // A keypad: its submit key is one of the group (formula-plug-in's numpad Enter). Its index, or -1.
  const SUBMIT_RE = /^(check|submit|answer|enter|go|calculate|confirm|done|finish)\b/;
  window.__lockGroupSubmit = function () {
    return (window.__mfgGroup || []).findIndex(e => SUBMIT_RE.test((e.textContent || '').trim().toLowerCase()));
  };
  // A point on the page that is not a control: where a student taps to get past a reveal or end screen
  // without pressing Play again.
  const CONTROL = 'button, a, input, select, textarea, [role="button"], footer, header';
  window.__lockBlankPoint = function () {
    // A "tap anywhere" screen first: the largest visible element with a pointer cursor that is not a control
    // (formula-plug-in's reveal screen); a point inside it that is not a control.
    let best = null, area = 0;
    document.querySelectorAll('body *').forEach(function (el) {
      if (el.closest(CONTROL) || !visible(el) || getComputedStyle(el).cursor !== 'pointer') return;
      const r = el.getBoundingClientRect(), a = r.width * r.height;
      if (a > area && a > 10000) { best = el; area = a; }
    });
    const cands = [];
    if (best) {
      best.scrollIntoView({ block: 'center' });
      const r = best.getBoundingClientRect();
      [[0.5, 0.5], [0.5, 0.2], [0.5, 0.8], [0.1, 0.5], [0.9, 0.5]].forEach(f =>
        cands.push([r.left + r.width * f[0], r.top + r.height * f[1], best]));
    }
    const W = innerWidth, H = innerHeight;
    [[0.5, 0.5], [0.5, 0.3], [0.5, 0.7], [0.1, 0.5], [0.9, 0.5]].forEach(f => cands.push([W * f[0], H * f[1], null]));
    for (const [x, y, within] of cands) {
      const el = document.elementFromPoint(x, y);
      if (el && !el.closest(CONTROL + ', [onclick]') && (!within || within.contains(el))) return { x, y };
    }
    return null;
  };
  // The start control (check-site's startEls rule) and the play-again control, for a real double-click.
  window.__lockStartRect = function () {
    const words = ['start', 'start game', 'play', 'begin', "let's go", 'go'];
    const el = [...document.querySelectorAll('button, a, [role="button"]')].find(function (e) {
      if (!visible(e)) return false;
      const t = (e.textContent || '').trim().toLowerCase().replace(/\s+/g, ' ');
      if (/^(play again|restart|try again|again|new game|start again|back to start)/.test(t)) return false;
      const marker = (e.id + ' ' + String(e.className || '')).toLowerCase();
      return /\bstart|start-?btn|btn-?start/.test(marker) || words.indexOf(t) !== -1 || /^start\b/.test(t) || /^play\b/.test(t);
    });
    return el ? window.__lockRect(el) : null;
  };
  window.__lockAgainRect = function () {
    const el = [...document.querySelectorAll('button, a, [role="button"]')].find(e => visible(e) &&
      /^(play again|restart|try again|new game|start again)/.test((e.textContent || '').trim().toLowerCase()));
    return el ? window.__lockRect(el) : null;
  };
  // Something to do: an enabled option of the probed group, a ready continue control, or the end.
  window.__lockActionable = function () {
    const p = window.__mfgProbe();
    const free = (window.__mfgGroup || []).some(e => !e.disabled && e.getAttribute('aria-disabled') !== 'true');
    const c = window.__lockContinue();
    return free || !!(c && c.ready) || p.atEnd || p.n < 2;
  };
  // Synthetic Enter and Space on every option of the answered question (listeners on the option itself).
  window.__lockKeyOptions = function () {
    (window.__mfgGroup || []).forEach(function (el) {
      ['Enter', ' '].forEach(function (k) {
        ['keydown', 'keyup'].forEach(function (t) {
          el.dispatchEvent(new KeyboardEvent(t, { key: k, code: k === ' ' ? 'Space' : 'Enter', bubbles: true, cancelable: true }));
        });
      });
      try { el.focus(); } catch (x) {}
    });
  };
})();
"""


def same(a, b):
    return all(a[k] == b[k] for k in ('answered', 'correct', 'completed', 'submits', 'scores'))


class Driver:
    def __init__(self, page, slug, hint):
        self.page, self.slug, self.hint = page, slug, hint

    async def ev(self, js, arg=None):
        return await self.page.evaluate(js, arg) if arg is not None else await self.page.evaluate(js)

    async def snap(self):
        return await self.ev('() => __lockSnap()')

    async def probe(self):
        return await self.ev('() => __mfgProbe()')

    async def start(self, dbl=False):
        """Reach the first question; with dbl, the start control is double-clicked for real."""
        if (dbl or self.hint.get('start_sel')) and not self.hint.get('start'):
            if self.hint.get('start_sel'):
                r = await self.ev('(sel) => __lockRect(document.querySelector(sel))', self.hint['start_sel'])
            else:
                r = await self.ev('() => __lockStartRect()')
            if r and dbl:
                await self.page.mouse.dblclick(r['x'], r['y'])
            elif r:
                await self.page.mouse.click(r['x'], r['y'])
            await self.page.wait_for_timeout(500)
        if self.hint.get('start'):
            await self.ev(self.hint['start'])
            await self.page.wait_for_timeout(500)
        # A visible start control is pressed before anything is read as an option group: a start screen's
        # level or session-length buttons are not answers (check-site.py's tier 3 learnt this on angle-ace).
        for _ in range(8):
            if await self.ev('() => __mfgHasStart()'):
                await self.ev('() => __mfgClickStart()')
                await self.page.wait_for_timeout(400)
                continue
            if self.hint.get('ready') and await self.ev('() => !!(%s)' % self.hint['ready']):
                return True
            p = await self.probe()
            if p['n'] >= 2 or await self.ev('() => __mfgHasInput()'):
                return True
            await self.page.wait_for_timeout(400)
        return False

    async def wait_answered(self, before, ms=1500):
        for _ in range(ms // 50):
            s = await self.snap()
            if s['answered'] > before:
                return s
            await self.page.wait_for_timeout(50)
        return None

    async def answer(self, i, touch=False):
        """Submit one answer (option i, or a typed wrong value); the snapshot after it, or None."""
        before = (await self.snap())['answered']
        if self.hint.get('answer'):
            await self.ev('(i) => { %s }' % self.hint['answer'], i)
            return await self.wait_answered(before)
        p = await self.probe()
        if await self.ev('() => __mfgHasInput()') and p['n'] < 2:
            await self.ev("() => __mfgTypeAnswer('987654')")
            return await self.wait_answered(before)
        if p['n'] < 2:
            return None
        rects = await self.ev('() => __lockGroupRects()')
        sub_i = await self.ev('() => __lockGroupSubmit()')
        keys = [k for k in range(len(rects)) if k != sub_i]
        await self.tap(rects[keys[i % len(keys)]], touch)
        s = await self.wait_answered(before, 600)
        if s:
            return s
        if sub_i >= 0:
            await self.tap((await self.ev('() => __lockGroupRects()'))[sub_i], touch)
        else:
            await self.ev('() => __mfgClickSubmit()')
        return await self.wait_answered(before)

    async def tap(self, r, touch):
        if touch:
            await self.page.touchscreen.tap(r['x'], r['y'])
        else:
            await self.page.mouse.click(r['x'], r['y'])

    async def to_next(self, touch=False):
        """Press the continue control once (or wait for the game to move on by itself)."""
        for _ in range(60):
            c = await self.ev('() => __lockContinue()')
            if c and c['ready']:
                r = c['rect']
                if touch:
                    await self.page.touchscreen.tap(r['x'], r['y'])
                else:
                    await self.page.mouse.click(r['x'], r['y'])
                await self.page.wait_for_timeout(400)
                return c['kind']
            if not c and (await self.probe())['n'] >= 2:
                await self.page.wait_for_timeout(350)
                return 'auto'
            await self.page.wait_for_timeout(50)
        return None

    async def answer_wrong(self, touch=False):
        for k in range(8):
            s = await self.answer(k + 1, touch)
            if s is None:
                return None
            if s['lastCorrect'] is False or self.hint.get('mark_any'):
                return s
            await self.to_next(touch)
            await self.page.wait_for_timeout(350)
        return None


async def play(browser, base, slug, level, page_html):
    """[fault] for one game, played in Chromium."""
    faults = []
    hint = read_hint(page_html if page_html is not None else
                     open(os.path.join(ROOT, 'games', slug, 'index.html'), encoding='utf-8').read())[0]
    level = hint.get('level', level)
    url = base + '/games/%s/%s' % (slug, ('?level=%s' % level) if level else '')

    async def new_page(**kw):
        ctx = await browser.new_context(**kw)
        await ctx.add_init_script(CHECK_SITE.TIER3_INIT)
        await ctx.add_init_script(INIT % {'scale': TIME_SCALE})   # after: its mfg recorder wins
        await ctx.route(lambda u: not u.startswith(base) and '/katex@' not in u, lambda r: r.abort())
        if page_html is not None:
            pat = re.compile(r'/games/%s/(\?[^/]*)?$' % re.escape(slug))
            await ctx.route(lambda u: bool(pat.search(u)), lambda r: r.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=page_html))
        page = await ctx.new_page()
        errs = []
        # Reading el.onclick (the tier 3 probe) compiles an inline handler; a malformed one throws here and is the
        # page's markup fault, not a marking fault (equatle :337 had one until F1 batch 2 restored it).
        page.on('pageerror', lambda e: errs.append(str(e)[:120])
                if "Failed to read the 'onclick' property" not in str(e) else None)
        await page.goto(url, wait_until='load', timeout=20000)
        await page.wait_for_timeout(300)
        return ctx, page, errs

    # 1 and 2: desktop
    ctx, page, errs = await new_page(viewport={'width': 1280, 'height': 900})
    d = Driver(page, slug, hint)
    if not await d.start(dbl=True):
        await ctx.close()
        return ['UNPLAYABLE: no option group or input after Start (declare it in the page: maffs-lock-hint, canon 7.6.0)']
    s = await d.snap()
    if s['answered']:
        faults.append('dblclick on Start: its second click answered the first question')
    s0 = await d.answer_wrong()
    if s0 is None:
        await ctx.close()
        return faults + ['UNPLAYABLE: no wrong answer marked in 8 questions (declare it in the page: maffs-lock-hint, canon 7.6.0)']
    rects = await d.ev('() => __lockGroupRects()')
    if hint.get('surface'):
        rects += await d.ev('''(sel) => { const e = document.querySelector(sel); if (!e) return [];
            e.scrollIntoView({block: 'center'}); const r = e.getBoundingClientRect();
            return [[0.5, 0.5], [0.1, 0.1], [0.9, 0.9], [0.1, 0.9]].map(f => ({x: r.left + r.width * f[0], y: r.top + r.height * f[1]})); }''',
                            hint['surface'])
    for r in rects:
        if r:
            await page.mouse.click(r['x'], r['y'])
    for k in hint.get('keys', []):
        await page.keyboard.press(k)
    if hint.get('repeat'):
        await d.ev('() => { %s }' % hint['repeat'])
    await d.ev('() => __lockKeyOptions()')   # Enter and Space on the options themselves (a page-level Enter
                                             # may be the game's own Next: it is pressed in the tap-through)
    await page.wait_for_timeout(250)
    s1 = await d.snap()
    if not same(s0, s1):
        faults.append('re-mark: clicking, Enter and Space on the answered question changed %s' % diff(s0, s1))
    # Next, double-clicked
    c = None
    for _ in range(80):
        c = await d.ev('() => __lockContinue()')
        if c and c['ready']:
            break
        await page.wait_for_timeout(50)
    if c and c['ready']:
        before = await d.snap()
        await page.mouse.dblclick(c['rect']['x'], c['rect']['y'])
        await page.wait_for_timeout(500)
        after = await d.snap()
        if after['answered'] != before['answered'] or after['completed'] != before['completed']:
            faults.append('dblclick on %s: its second click marked %s' % (c['kind'], diff(before, after)))
    elif await d.ev('() => __lockActionable()') and (await d.snap())['answered'] == s0['answered']:
        if s0['lastCorrect'] is False:        # (a mark_any game's right answer moves on by itself, as it should)
            AUTO_ADVANCE.add(slug)            # moved on by itself after a wrong answer: no Next to double-click
    else:
        faults.append('no continue control after a wrong answer, and the game did not move on')
    # 4: tap through to the end; each continue pressed with two Enters and no gap (shape-shifter-t3-005)
    mark = len(await d.ev('() => __lockEvents'))
    t_end = asyncio.get_event_loop().time() + 180
    while asyncio.get_event_loop().time() < t_end:
        for _ in range(40):                  # wait until the game offers something (a right answer moves on itself)
            if await d.ev('() => __lockActionable()'):
                break
            await page.wait_for_timeout(50)
        await page.wait_for_timeout(320)     # past MaffsLock's 300 ms window on what just rendered
        if hint.get('each'):
            await d.ev('() => { %s }' % hint['each'])
        s = await d.snap()
        if s['completed'] or (await d.probe())['atEnd']:
            break
        if await d.answer(0) is None and not (await d.snap())['completed']:
            pt = await d.ev('() => __lockBlankPoint()')      # a reveal or interstitial screen: tap it
            if pt:
                await page.mouse.click(pt['x'], pt['y'])
            await page.wait_for_timeout(int(1000 * TIME_SCALE))
        c = await d.ev('() => __lockContinue()')
        if c and c['ready']:
            await d.ev('() => { try { __lockContEl.focus(); } catch (x) {} }')
            await page.keyboard.press('Enter')
            await page.keyboard.press('Enter')
            if (await d.ev('() => !!(__lockContEl && __lockContEl.isConnected && __lockContEl.offsetParent && !__lockContEl.disabled)')):
                await page.mouse.dblclick(c['rect']['x'], c['rect']['y'])     # Enter did not reach it: click
        await page.wait_for_timeout(60)
    for _ in range(12):                      # tap the end screen, as a student does
        pt = await d.ev('() => __lockBlankPoint()')
        if pt:
            await page.mouse.click(pt['x'], pt['y'])
        await page.wait_for_timeout(int(1000 * TIME_SCALE))
    await page.wait_for_timeout(int(9000 * TIME_SCALE) + 500)
    end = await d.snap()
    idx = [r['i'] for r in (await d.ev('() => __lockEvents'))[mark:]
           if r['e'] == 'question_answered' and isinstance(r.get('i'), int)]
    gaps = [(a, b) for a, b in zip(idx, idx[1:]) if b - a > 1]
    if gaps:
        faults.append('skip: question_index jumped %s during the tap-through (a question skipped unseen)'
                      % ', '.join('%d -> %d' % g for g in gaps[:3]))
    if VERBOSE:
        print('    [%s] end of run: %s; probe %s' % (slug, end, await d.probe()))
    if end['completed'] != 1:
        faults.append('finish: game_completed %d time(s) (once)' % end['completed'])
    if end['submits'] > 1:
        faults.append('finish: submitScore %d times (at most once)' % end['submits'])
    r = await d.ev('() => __lockAgainRect()')
    if r:
        await page.mouse.dblclick(r['x'], r['y'])
        await page.wait_for_timeout(600)
        again = await d.snap()
        if again['answered'] != end['answered']:
            faults.append('dblclick on Play again: its second click answered the first question')
    faults += ['page error: %s' % e for e in errs[:2]]
    await ctx.close()

    # 3: double-tap at 390px
    ctx, page, errs = await new_page(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True)
    d = Driver(page, slug, hint)
    if await d.start() and await d.answer_wrong(touch=True):
        c = None
        for _ in range(80):
            c = await d.ev('() => __lockContinue()')
            if c and c['ready']:
                break
            await page.wait_for_timeout(50)
        if c and c['ready']:
            before = await d.snap()
            await page.touchscreen.tap(c['rect']['x'], c['rect']['y'])
            await page.wait_for_timeout(60)
            await page.touchscreen.tap(c['rect']['x'], c['rect']['y'])
            await page.wait_for_timeout(500)
            after = await d.snap()
            if after['answered'] != before['answered']:
                faults.append('double-tap on %s at 390px: the second tap marked %s' % (c['kind'], diff(before, after)))
    else:
        faults.append('390px: could not reach a wrong answer by touch')
    await ctx.close()
    return faults


def diff(a, b):
    return ', '.join('%s %s -> %s' % (k, a[k], b[k]) for k in ('answered', 'correct', 'completed', 'submits', 'scores')
                     if a[k] != b[k]) or 'nothing'


async def play_all(games, against):
    from playwright.async_api import async_playwright
    proc, base = bc.start_stub_server()
    results = {}
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            sem = asyncio.Semaphore(WORKERS)

            async def one(slug, level):
                async with sem:
                    html = open(against, encoding='utf-8').read() if against else None
                    try:
                        results[slug] = await asyncio.wait_for(play(browser, base, slug, level, html), 300)
                    except Exception as e:      # a crash is a failure, never a pass
                        results[slug] = ['driver error: %s' % str(e)[:160]]
            await asyncio.gather(*(one(s, l) for s, l in games))
            await browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return results


CHECK_SITE = None
VERBOSE = False
AUTO_ADVANCE = set()   # games that moved on by themselves after a wrong answer (no Next): reported


def counts(slug, remaining):
    """Does a failure of this game fail the check? Yes, unless the game is not yet MIGRATED and is still on the
    cloud lane's remaining list (then it is reported). Contract LH: that state ends when the list drops it."""
    return slug in MIGRATED or slug not in remaining


# A page with no lock at all: lock() never refuses, nothing is ever locked, no fresh window.
PLANT = ('<script>MaffsLock.lock = function () { return true; }; MaffsLock.isLocked = function () { return false; };'
         ' MaffsLock.fresh = function () {}; MaffsLock.screen = function () { MaffsLock.clearTimers(); };</script>\n')


PLANT_GAME = 'decimal-detective'   # the self-test's planted game (#133's): it needs MaffsLock to pass


def selftest(games):
    """The reported state is bounded: a planted failing game off the cloud lane's list is caught, on it reported."""
    import tempfile
    errs = []
    if cloud_remaining('x `cloud-remaining: a b` y') != {'a', 'b'}:
        errs.append('cloud_remaining() misreads a list')
    for bad in ('no list here', '`cloud-remaining: a` and `cloud-remaining: b`'):
        try:
            cloud_remaining(bad)
            errs.append('cloud_remaining() accepted %r (a missing or doubled list must fail)' % bad)
        except ValueError:
            pass
    try:
        cloud_remaining()
    except ValueError as e:
        errs.append(str(e))
    for page, why in (('<!-- maffs-lock-hint\n{"answer": \n-->', 'not JSON'),
                      ('<!-- maffs-lock-hint\n{"anwser": "x"}\n-->', 'an unknown key'),
                      ('<p>no declaration</p>', 'no declaration')):
        if not read_hint(page)[1]:
            errs.append('a maffs-lock-hint with %s passed' % why)
    if read_hint('<!-- maffs-lock-hint x\n{"answer": ["a;", " b"], "keys": ["p"]}\n-->') != ({'answer': 'a; b', 'keys': ['p']}, []):
        errs.append('read_hint() misreads a declaration')
    # The plant: one named migrated game, its MaffsLock.lock never refusing, played as a game the cloud lane
    # adopted and has taken off its list. Named, not "the first in MIGRATED": a game that also guards itself
    # (binomial-blaster, first once the cloud lane's games joined) plays clean without the lock, and a plant
    # that cannot fail proves nothing.
    slug, level = next(g for g in games if g[0] == PLANT_GAME)
    html = open(os.path.join(ROOT, 'games', slug, 'index.html'), encoding='utf-8').read()
    m = INCLUDE.search(html)
    end = html.index('\n', m.end()) + 1
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(html[:end] + PLANT + html[end:])
    try:
        res = asyncio.run(play_all([(slug, level)], f.name)).get(slug, [])
    finally:
        os.unlink(f.name)
    saved = set(MIGRATED)
    MIGRATED.discard(slug)
    try:
        if not res:
            errs.append('planted %s (no lock: MaffsLock.lock never refuses, no fresh window) played clean: the check cannot see a missing lock' % slug)
        elif not counts(slug, set()):
            errs.append('planted %s fails, off the cloud list, but its failure is not counted' % slug)
        elif counts(slug, {slug}):
            errs.append('planted %s on the cloud list is failed, not reported' % slug)
        else:
            print('  self-test: planted %s (no lock: MaffsLock.lock never refuses, no fresh window), off the cloud list: CAUGHT (%d, e.g. %s);'
                  ' on the list: reported' % (slug, len(res), res[0][:90]))
    finally:
        MIGRATED.clear()
        MIGRATED.update(saved)
    for e in errs:
        print('FAIL  self-test: ' + e)
    return errs


def main():
    global CHECK_SITE, VERBOSE
    ap = argparse.ArgumentParser()
    ap.add_argument('--game', action='append', help='only this game (repeatable)')
    ap.add_argument('--against', help='play this file as the (single) --game page')
    ap.add_argument('--not-yet', action='store_true', help='play the NOT_YET games too (reported only)')
    ap.add_argument('--static', action='store_true', help='static rules only, no browser')
    ap.add_argument('--part', help='i/n: play only the i-th of n slices of the migrated games (CI)')
    ap.add_argument('--selftest', action='store_true', help='a planted failing game off the cloud list is caught')
    ap.add_argument('-v', '--verbose', action='store_true')
    args = ap.parse_args()
    VERBOSE = args.verbose
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    CHECK_SITE = load_check_site()
    games = roster_games()
    if args.selftest:
        errs = selftest(games)
        print('FAILED' if errs else 'PASS')
        return 1 if errs else 0
    slugs = {s for s, _ in games}
    fails = []
    try:
        remaining = cloud_remaining()
    except ValueError as e:
        fails.append(str(e))
        remaining = set()
    for s in sorted(NOT_YET - NOT_YET_AT_START):
        fails.append('%s: on NOT_YET but not in NOT_YET_AT_START (a new game is migrated from the start)' % s)
    for s in sorted(NOT_YET - slugs):
        fails.append('%s: on NOT_YET but not a roster game that records question_answered' % s)
    page = {s: open(os.path.join(ROOT, 'games', s, 'index.html'), encoding='utf-8').read() for s, _ in games}
    # Adopted: on NOT_YET, but the page loads the lock (the cloud lane migrates its own games). Judged in full.
    adopted = {s for s in NOT_YET & slugs if INCLUDE.search(page[s])}
    judged = [(s, l) for s, l in games if s not in NOT_YET or s in adopted]
    reported = []      # [(slug, fault)]: an adopted game still on the cloud lane's list
    for s, _ in judged:
        if args.game and s not in args.game:
            continue
        for f in static_faults(s, open(args.against, encoding='utf-8').read() if args.against else page[s]):
            (fails if counts(s, remaining) or args.against else reported).append('%s: %s' % (s, f))
    to_play = [(s, l) for s, l in judged if not args.game or s in args.game]
    if args.part:
        i, n = (int(x) for x in args.part.split('/'))
        to_play = [g for k, g in enumerate(sorted(to_play)) if k % n == i - 1]
        if i != 1:
            fails, reported = [], []    # the static rules and NOT_YET are part 1's (one report, not n)
    if args.not_yet:
        to_play += [(s, l) for s, l in games if s in NOT_YET - adopted and (not args.game or s in args.game)]
    if args.game and args.against and len(args.game) == 1:
        to_play = [(s, l) for s, l in games if s in args.game]
    print('Answer lock (canon 7.6.0): %d roster games record question_answered; %d migrated, %d adopted by the '
          'cloud lane, %d on NOT_YET; the cloud lane\'s remaining list: %s'
          % (len(games), len(slugs - NOT_YET), len(adopted), len(NOT_YET & slugs - adopted),
             ' '.join(sorted(remaining)) or '(empty)'))
    if not args.static and to_play:
        results = asyncio.run(play_all(to_play, args.against))
        for s, _ in to_play:
            res = results.get(s, ['not played'])
            hard = args.against or (s not in NOT_YET or s in adopted) and counts(s, remaining)
            tag = 'PASS' if not res else ('FAIL' if hard else ('REPORTED' if s in adopted else 'NOT_YET'))
            print('  %-8s %s%s' % (tag, s, ('' if not res else ': ' + '; '.join(res))))
            if res and hard:
                fails += ['%s: %s' % (s, r) for r in res]
            elif res and s in adopted:
                reported += ['%s: %s' % (s, r) for r in res]
    for s in sorted(adopted):
        print('  note: %s loads answer-lock.js and is on NOT_YET: %s' % (s, (
            'on the cloud lane\'s list, so its failures are reported, not failed' if s in remaining else
            'off the cloud lane\'s list, so it is judged in full; the home lane adds it to MIGRATED once it passes')))
    for r in reported:
        print('  REPORTED (on the cloud lane\'s list) ' + r)
    if AUTO_ADVANCE:
        print('  note: no Next after a wrong answer (the game moves on by itself; canon 7.6 asks for Next): %s'
              % ', '.join(sorted(AUTO_ADVANCE)))
    if NOT_YET & slugs - adopted:
        print('  NOT_YET (%d): %s' % (len(NOT_YET & slugs - adopted), ', '.join(sorted(NOT_YET & slugs - adopted))))
    for f in fails:
        print('FAIL  ' + f)
    print('FAILED' if fails else 'PASS')
    return 1 if fails else 0

if __name__ == '__main__':
    sys.exit(main())
