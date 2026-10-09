"""Is the teacher feedback line on every game's results screen, mounted for itself, in Jon's exact words?

The line (schools/assets/teacher-invite.js, `MaffsInvite.mount(el, slug)`; contract 4 Oct 2026) links to
/feedback/?type=classroom&game=<slug>. Jon, 5 Oct 2026: it belongs on the RESULTS screen, after the last control
row, because that is where a game ends in a lesson and where the teacher looks at how it went; on the start screen
only where a game has no end (canon §7.1). docs/teacher-invite-results-survey.md is the survey behind the routes.

Every roster game (each numbered row of .claude/rules/game-roster.md; a withdrawn game, numbered "—", is a holding
page and is skipped) must be in exactly one of:

  RESULTS         a results container in the page's own markup. The mount point must be inside it (by id), and no
                  control (button, link, select, input, onclick) may follow it there: the line goes after the last
                  control row, so it never sits between an answer input and its keypad.
  FUNCTION_ROUTE  results built by script or more than one end state: the game moves its one line into whichever
                  end container it shows (MaffsInvite.place). Checked by PLAYING each end state in Chromium: the
                  line must be visible inside that end container, and not visible on the start screen.
  START_SCREEN    no end of game, so the line stays on the start screen (reason recorded).
  PENDING         the line stays put until a named rebuild merges. The page's content hash is recorded; once the
                  page changes, the RESULTS rule applies to it with the container recorded here.

It also fails if a game does not load teacher-invite.js exactly once, does not make exactly one MaffsInvite.mount
call, mounts with a slug other than its directory name, or mounts onto an id not on the page exactly once; if the
escape-room engine (escape-rooms/assets/engine.js) does not mount the line on the end card it rebuilds in finish()
(and nowhere else), a live room does not load teacher-invite.js, or a room's R.slug is not 'escape-' + its directory
name; if /leaderboards/ does not mount it once with no game (null); if the link text is not exactly TEXT. In
Chromium, every live room is played to a win and to a loss: the line must be on the end card both times, naming
the room, and not on the brief. And on every roster page, in Chromium: the line reads at 4.5:1 or better against the
background behind it (canon 7.5), and its parent is not a flex row or a grid, where it would be squeezed in beside
the buttons instead of sitting under them (both slipped past the first version of this check, 5 Oct 2026: Estimation
Golf's cream line on its cream summary card, Complex Converter's line inside its button row).

    python scripts/check-teacher-invite.py               # the check (static + Chromium)
    python scripts/check-teacher-invite.py --static      # the static half only (no browser)
    python scripts/check-teacher-invite.py --selftest    # each planted fault must fail; the clean copy passes
"""
import argparse, asyncio, hashlib, json, pathlib, re, shutil, socket, subprocess, sys, tempfile, time
import urllib.request
from html.parser import HTMLParser

BASE = pathlib.Path(__file__).resolve().parent.parent
ROSTER = ".claude/rules/game-roster.md"
ASSET = "schools/assets/teacher-invite.js"
ENGINE = "escape-rooms/assets/engine.js"
TEXT = "Using this with a class? I'd love to hear how it went. — Jon"
ROW = re.compile("^\\|\\s*(\\d+)\\s*\\|[^|]*\\|\\s*`([a-z0-9-]+)`\\s*\\|")
INCLUDE = re.compile(r'<script\b[^>]*\bsrc="[^"]*schools/assets/teacher-invite\.js"', re.I)
MOUNT = re.compile(r"MaffsInvite\.mount\(\s*document\.getElementById\('([^']+)'\)\s*,\s*(null|'([^']*)')\s*\)")
ANY_MOUNT = re.compile(r"MaffsInvite\.mount\(")
PLACE = re.compile(r"MaffsInvite\.place\(")
ENGINE_MOUNT = "window.MaffsInvite.mount(el('teacherInvite'), R.slug.replace(/^escape-/, ''))"
ENGINE_POINT = "'<p id=\"teacherInvite\"></p>'"
ENGINE_END = "el('endCard').innerHTML ="
ROOM_SLUG = re.compile(r"slug:\s*'([^']+)'")

# slug -> id of the results container the mount point must sit inside (docs/teacher-invite-results-survey.md).
# "modal" is the overlay holding #modal-result.
RESULTS = {
    "sequence-solver": "results", "estimation-golf": "summaryCard",
    "factor-race": "gameOver", "prime-factorisation": "gameOver", "prime-or-composite": "modal",
    "percentage-flip": "gameOver", "fraction-equivalence": "gameOver", "equatle": "m-end", "52dle": "modal",
    "split-it": "resultsScreen", "word-problem-decoder": "resultsScreen", "equation-builder": "resultsScreen",
    "spot-the-error": "resultsScreen", "gradient-hunter": "resultsScreen", "truth-buster": "resultsScreen",
    "spot-the-muppet": "resultsScreen", "terrible-advice": "resultsScreen",
    "wrong-on-the-internet": "resultsScreen", "maths-court": "resultsScreen", "expected-damage": "resultsScreen",
    "negative-number-line": "resultsScreen", "think-of-a-number": "resultsScreen",
    "formula-plug-in": "resultsScreen", "decimal-detective": "resultsScreen",
    "four-quadrant-explorer": "resultsScreen", "like-terms-collector": "resultsScreen",
    "probability-pioneer": "resultsScreen", "shape-shifter": "resultsScreen", "new-shapes": "resultsScreen",
    "higher-power": "results", "seven-bridges": "resultsScreen", "distinctly-average": "gameOver",
    "index-laws": "gameOver", "quadratic-factoriser": "gameOver", "trig-worms": "gameOver",
    "modular-battle": "gameOver", "surd-simplifier": "results", "proportion-blaster": "results",
    "trig-identity-duel": "results", "standard-form-blitz": "results", "simultaneous-solver": "results",
    "circle-theorem-spotter": "results", "probability-paradox": "results", "angle-ace": "results",
    "coordinate-geometry-dash": "results", "graph-transformer": "results", "formula-unlocked": "results",
    "bearing-blitz": "results", "scale-factor-scaling": "results", "unit-converter": "results",
    "formula-forge": "results", "correlation-or-coincidence": "results", "component-crusher": "resultsScreen",
    "expectation-station": "resultsScreen", "better-value": "resultsScreen", "given-that": "resultsScreen",
    "screening-room": "endScreen", "linear-equation-solver": "results", "core-maths-paper1": "resultsScreen",
    "core-maths-paper2a": "resultsScreen", "core-maths-paper2b": "resultsScreen",
    "core-maths-paper2c": "resultsScreen", "tax-theft": "completionScreen", "stat-attack": "resultsScreen",
    "growth-and-decay": "resultsScreen", "graph-sketcher": "resultsScreen", "glorious-gantt": "resultsScreen",
    "test-the-claim": "resultsScreen", "differentiation-duel": "gameOver", "integration-duel": "gameOver",
    "suvat": "gameOver", "curling-friction": "results", "force-resolver": "results", "moments-master": "results",
    "binomial-blaster": "results", "partial-fractions-duel": "results", "proof-builder": "results",
    "normal-navigator": "results", "fermi-lab": "endScreen", "dimension-checker": "results",
    "boolean-blitz": "resultsScreen", "truth-will-set-you-free": "resultsScreen", "complex-converter": "endScreen",
    "matrix-crunch": "results", "characteristic-quest": "results", "eigenvalue-extractor": "results",
    "eigenvector-engine": "results", "six-sevens-bruv": "results", "free-daily-pizza": "results",
    "just-pythag-it-bruv": "results", "estimation-engine": "results",
}

START_SCREEN = {
    "constructions-lab": "an open task menu: the game has no end, no results screen and no game_completed",
    "trig-wars": "the game ends with 'PLAYER n WINS' written into the play screen's turn bar; it has no results "
                 "screen to mount on, and giving it one would change how the game ends",
}

PENDING = {}

# Drivers for the function route. Each end state is (CSS selector of the end container the line must be inside,
# steps). A step is ("click", selector), pressing one of the game's controls, or ("play", js_step, js_done): js_step
# is one student action through the game's own controls, repeated until js_done is true.
CI_STEP = r"""(() => {
  const q = phase1Questions[currentQIndex], inp = document.getElementById('qInput');
  if (currentPhase === 1 && inp && q) { inp.value = q.expected; document.querySelector('.q-submit').click(); return; }
  const mcs = [...document.querySelectorAll('.mc-btn:not([disabled])')];
  if (currentPhase === 1 && mcs.length && q) { (mcs.find(b => b.textContent === String(q.expected)) || mcs[0]).click(); return; }
  const sels = document.querySelectorAll('.scaffold-text select');
  if (sels.length) {
    sels.forEach(s => { s.value = s.dataset.correct; });
    document.querySelectorAll('.scaffold-text input').forEach(i => { i.value = i.dataset.expected; });
    document.querySelector('.scaffold-submit .q-submit').click();
  }
})()"""
FT_STEP = r"""((area) => {
  const vis = e => e && e.offsetParent !== null;
  const nx = document.querySelector('#' + area + ' .next-q-btn');
  if (vis(nx)) { nx.click(); return; }
  document.querySelectorAll('#' + area + ' input.answer-input:not([disabled])').forEach(i => { if (vis(i)) i.value = '0'; });
  document.querySelectorAll('#' + area + ' .opt-group').forEach(g => { const b = g.querySelector('.opt-btn:not([disabled])'); if (vis(g) && b && !g.querySelector('.opt-btn.chosen')) b.click(); });
  const ck = document.querySelector('#' + area + ' .submit-btn');
  if (vis(ck)) ck.click();
})"""
PD_STEP = r"""(() => {
  const b = document.getElementById('btnDefect');
  if (b && b.offsetParent !== null && !b.disabled) b.click();
})()"""
# The tournament unlocks at three wins: play single games, one opponent after another, always defecting.
PD_UNLOCK = r"""(() => {
  if (document.getElementById('results').classList.contains('active')) { showScreen('menu'); renderMenu(); return; }
  if (document.getElementById('menu').classList.contains('active')) {
    window.__pdNext = window.__pdNext || 0;
    const cards = document.querySelectorAll('#menuOpponents .opp-card');
    cards[window.__pdNext++ % cards.length].click();
    return;
  }
  const b = document.getElementById('btnDefect');
  if (b && b.offsetParent !== null && !b.disabled) b.click();
})()"""
LL_LAWS = r"""(() => {
  const nx = document.querySelector('#mainGame .maffs-next');
  if (nx && nx.offsetParent !== null) { nx.click(); return; }
  const c = document.querySelector('#choices .choice:not(.correct):not(.wrong)');
  const ch = document.getElementById('choices');
  if (c && !MaffsLock.isLocked(ch) && !MaffsLock.isFresh(ch)) c.click();
})()"""
LL_SOLVE = r"""(() => {
  const $ = id => document.getElementById(id);
  const nx = document.querySelector('#solveBox .maffs-next');
  if (nx && nx.offsetParent !== null) { nx.click(); return; }
  if (!$('solveAnswer').hidden) { if (!$('solveCheck').disabled) { $('solveInput').value = '1'; $('solveCheck').click(); } return; }
  if (!$('solveChoose').hidden) { const b = document.querySelector('#solveChooseGrid .choose-btn:not([disabled])'); if (b) b.click(); return; }
  const moves = [...document.querySelectorAll('#solveMoves .move-btn')];
  const m = moves.find(b => !b.classList.contains('nope') && !b.classList.contains('meh')) || moves[0];
  if (m) m.click();
})()"""

FUNCTION_ROUTE = {
    "chart-interrogator": {
        "scenario": ("#activeQuestion", [("click", '[data-type="stemleaf"]'), ("click", '[data-level="gcse"]'),
                                         ("click", "#startBtn"),
                                         ("play", CI_STEP, "!!document.querySelector('#activeQuestion .score-bar')")]),
    },
    "factor-theorem": {
        "practice": ("#practice-results", [("click", '[data-section="practice"]'),
                                           ("play", FT_STEP + "('sec-practice')",
                                            "getComputedStyle(document.getElementById('practice-results')).display !== 'none'")]),
        "test": ("#test-results", [("click", '[data-section="test"]'),
                                   ("play", FT_STEP + "('sec-test')",
                                    "getComputedStyle(document.getElementById('test-results')).display !== 'none'")]),
    },
    "prisoners-dilemma": {
        "single game": ("#results", [("click", "#menuOpponents .opp-card"),
                                     ("play", PD_STEP, "document.getElementById('results').classList.contains('active')")]),
        "tournament": ("#tournamentResults", [
            ("play", PD_UNLOCK, "document.getElementById('tournamentBtn').style.display !== 'none' && "
                                "document.getElementById('menu').classList.contains('active')"),
            ("click", "#tournamentBtn button"),
            ("play", PD_STEP, "document.getElementById('tournamentResults').classList.contains('active')")]),
    },
    "log-laws": {
        "laws": ("#gameOver", [("click", "#startScreen .btn-primary"),
                               ("play", LL_LAWS, "document.getElementById('gameOver').classList.contains('visible')")]),
        "solve": ("#solveOver", [("click", '[data-mode="solve"]'), ("click", "#stagePick button"),
                                 ("click", "#solveLengths button"), ("click", "#startScreen .btn-primary"),
                                 ("play", LL_SOLVE, "document.getElementById('solveOver').classList.contains('visible')")]),
    },
}

WIDTHS = (390, 1280)

# Test harness only: every timer fires within 25 ms, so a 20-round match plays in seconds, and the shared Next
# control has no floor (as the content verifiers run it). The games' own logic is untouched.
FAST_INIT = """(() => {
  const st = window.setTimeout;
  window.setTimeout = function (f, ms) { const a = [].slice.call(arguments, 2); return st.call(window, f, Math.min(ms || 0, 25), ...a); };
  let api;
  Object.defineProperty(window, 'MaffsNext', { configurable: true, get() { return api; },
    set(v) { if (v && typeof v === 'object') v.FLOOR_MS = 0; api = v; } });
})()"""

LINE = """(sel) => {
  const p = document.getElementById('teacherInvite');
  if (!p) return {vis: false, inside: false};
  const r = p.getBoundingClientRect();
  let vis = r.width > 0 && r.height > 0;
  for (let e = p; e; e = e.parentElement) {
    const c = getComputedStyle(e);
    if (c.display === 'none' || c.visibility === 'hidden' || c.opacity === '0') { vis = false; break; }
  }
  const a = p.querySelector('a');
  return {vis: vis, inside: sel ? !!p.closest(sel) : true, href: a && a.getAttribute('href')};
}"""

# The line's contrast against the first opaque background behind it (translucent layers composited), and how its
# parent lays it out. Computed styles do not depend on the screen being shown, so the page is measured as loaded.
STYLE = r"""(() => {
  const p = document.getElementById('teacherInvite');
  if (!p) return null;
  const a = p.querySelector('a') || p, q = p.parentElement, pc = getComputedStyle(q);
  const rgb = s => { const v = (s.match(/rgba?\(([^)]+)\)/) || [0, ''])[1].split(/[ ,\/]+/).filter(Boolean).map(Number);
    return v.length < 3 ? null : {r: v[0], g: v[1], b: v[2], a: v.length > 3 ? v[3] : 1}; };
  const layers = [];
  for (let e = p; e; e = e.parentElement) {
    const b = rgb(getComputedStyle(e).backgroundColor);
    if (b && b.a > 0) { layers.push(b); if (b.a >= 0.99) break; }
  }
  let bg = {r: 255, g: 255, b: 255};
  for (let i = layers.length - 1; i >= 0; i--) {
    const L = layers[i];
    bg = {r: L.r * L.a + bg.r * (1 - L.a), g: L.g * L.a + bg.g * (1 - L.a), b: L.b * L.a + bg.b * (1 - L.a)};
  }
  const c = rgb(getComputedStyle(a).color);
  const fg = {r: c.r * c.a + bg.r * (1 - c.a), g: c.g * c.a + bg.g * (1 - c.a), b: c.b * c.a + bg.b * (1 - c.a)};
  const lum = x => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(x.r) + 0.7152 * f(x.g) + 0.0722 * f(x.b); };
  const l1 = lum(fg), l2 = lum(bg);
  return {ratio: (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05),
          row: (/flex/.test(pc.display) && pc.flexDirection.startsWith('row')) || /grid/.test(pc.display),
          parent: (q.id ? '#' + q.id : '') + (q.className ? '.' + String(q.className).split(' ')[0] : q.id ? '' : q.tagName.toLowerCase())};
})()"""


# Escape rooms: set each lock to its value (win), or keep setting a wrong value until the penalties run the clock
# out (loss). The value comes from the room's own data for the variant this play drew.
ROOM_STEP = r"""((win) => {
  const R = window.ROOM;
  let vars = {};
  try { vars = (JSON.parse(localStorage.getItem('mfg_escape_vars_' + R.slug)) || {}).vars || {}; } catch (e) {}
  for (let i = 0; i < R.locks.length; i++) {
    const l = R.locks[i];
    const b = document.querySelector('[data-lock="' + i + '"]');
    if (!b) return;
    b.click();
    const set = document.getElementById('setBtn');
    if (!set) continue;                                   // already open
    const v = l.variants ? (l.variants[vars[l.id] || 0] || l.variants[0]) : {};
    const ans = v.answer !== undefined ? v.answer : l.answer, ins = l.instrument;
    const put = (id, val) => { const n = document.getElementById(id); n.value = String(val); n.dispatchEvent(new Event('input', {bubbles: true})); };
    if (ins.kind === 'keypad') {
      const d = ins.digits, good = String(ans).padStart(d, '0');
      put('numK', win ? good : (good === '0'.repeat(d) ? '1'.repeat(d) : '0'.repeat(d)));
    } else if (ins.kind === 'pair') {
      put('numA', win ? ans[0] : (Number(ans[0]) === ins.a.min ? ins.a.max : ins.a.min));
      put('numB', ans[1]);
    } else {
      put('num', win ? ans : (Number(ans) === ins.min ? ins.max : ins.min));
    }
    set.click();
    return;
  }
})"""


def roster(root):
    """Slugs of the roster's numbered (listed or unlisted) game rows."""
    out = []
    for line in (root / ROSTER).read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if m:
            out.append(m.group(2))
    return out


def lf_sha256(path):
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


class _El:
    def __init__(self, tag, attrs, start, parent):
        self.tag, self.attrs, self.start, self.end, self.parent, self.children = tag, dict(attrs), start, None, parent, []

    def walk(self):
        yield self
        for c in self.children:
            yield from c.walk()

    def ancestors(self):
        p = self.parent
        while p is not None:
            yield p
            p = p.parent


class _Tree(HTMLParser):
    """Elements with their source offsets: enough to say what contains what, and what comes after what."""
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

    def __init__(self, src):
        super().__init__(convert_charrefs=True)
        self.src, self.lines = src, [0] + [i + 1 for i, ch in enumerate(src) if ch == "\n"]
        self.root = _El("#root", [], 0, None)
        self.stack = [self.root]
        self.feed(src)
        self.close()

    def _off(self):
        line, col = self.getpos()
        return self.lines[line - 1] + col

    def handle_starttag(self, tag, attrs):
        o, top = self._off(), self.stack[-1]
        if tag == "p" and top.tag == "p":
            top.end = o
            self.stack.pop()
            top = self.stack[-1]
        e = _El(tag, attrs, o, top)
        top.children.append(e)
        if tag in self.VOID:
            e.end = self.src.index(">", o) + 1
        else:
            self.stack.append(e)

    def handle_startendtag(self, tag, attrs):
        o = self._off()
        e = _El(tag, attrs, o, self.stack[-1])
        self.stack[-1].children.append(e)
        e.end = self.src.index(">", o) + 1

    def handle_endtag(self, tag):
        o = self._off()
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                for e in self.stack[i:]:
                    e.end = self.src.index(">", o) + 1 if e is self.stack[i] else o
                del self.stack[i:]
                return


def is_control(e):
    if e.tag in ("button", "a", "select", "textarea"):
        return True
    if e.tag == "input" and e.attrs.get("type", "text") != "hidden":
        return True
    return "onclick" in e.attrs


def check_location(rel, src, el_id, container):
    """The mount point is inside #container, after every control there."""
    point = [e for e in _Tree(src).root.walk() if e.attrs.get("id") == el_id]
    if len(point) != 1:
        return []  # reported by check_page
    point = point[0]
    box = next((a for a in point.ancestors() if a.attrs.get("id") == container), None)
    if box is None:
        where = ["#" + a.attrs["id"] for a in point.ancestors() if a.attrs.get("id")]
        return ["%s: the teacher line's mount point is not on the results screen: want it inside #%s (it is inside %s)"
                % (rel, container, ", ".join(where) or "no element with an id")]
    after = [c for c in box.walk() if is_control(c) and c.start > point.start and point not in c.ancestors()]
    if after:
        c = after[0]
        label = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", src[c.start:c.end]))[:40].strip()
        return ["%s: the teacher line sits before a control in #%s (<%s> %r); it goes after the last control row"
                % (rel, container, c.tag, label)]
    return []


def check_page(rel, src, want_slug):
    """Problems with one page's include and mount, and the mount point's id. want_slug None means mount with null."""
    fails = []
    n = len(INCLUDE.findall(src))
    if n != 1:
        fails.append("%s: loads %s %d times (want once)" % (rel, ASSET, n))
    mounts = MOUNT.findall(src)
    if len(ANY_MOUNT.findall(src)) != 1 or len(mounts) != 1:
        fails.append("%s: %d MaffsInvite.mount calls in the expected form (want exactly one)" % (rel, len(ANY_MOUNT.findall(src))))
        return fails, None
    el_id, raw, slug = mounts[0]
    if want_slug is None and raw != "null":
        fails.append("%s: mounts with %s; this page names no game (want null)" % (rel, raw))
    if want_slug is not None and slug != want_slug:
        fails.append("%s: mounts with slug %r, but its directory is %r" % (rel, slug or raw, want_slug))
    ids = len(re.findall(r'\bid="%s"' % re.escape(el_id), src))
    if ids != 1:
        fails.append("%s: the mount point id=%r is on the page %d times (want once)" % (rel, el_id, ids))
    return fails, el_id


def live_rooms(root):
    """Rooms that load the engine (a withdrawn room's holding page does not)."""
    out = []
    for room in sorted((root / "escape-rooms").iterdir()):
        page = room / "index.html"
        if page.exists() and (room / "room.js").exists() and "assets/engine.js" in page.read_text(encoding="utf-8"):
            out.append(room.name)
    return out


def check_static(root):
    fails, notes = [], []
    js = (root / ASSET).read_text(encoding="utf-8")
    m = re.search(r'var TEXT = ("(?:[^"\\]|\\.)*");', js)
    text = json.loads(m.group(1)) if m else None
    if text != TEXT:
        fails.append("%s: link text is %r; it must be exactly %r" % (ASSET, text, TEXT))
    if "a.textContent = TEXT" not in js:
        fails.append("%s: the link no longer shows TEXT" % ASSET)

    slugs = roster(root)
    if not slugs:
        return fails + ["no game rows found in %s: the table changed shape, so this check is blind" % ROSTER], notes
    kinds = {"RESULTS": RESULTS, "FUNCTION_ROUTE": FUNCTION_ROUTE, "START_SCREEN": START_SCREEN, "PENDING": PENDING}
    for slug in slugs:
        where = [k for k, d in kinds.items() if slug in d]
        if len(where) != 1:
            fails.append("games/%s/: listed in %s in this check (want exactly one of RESULTS, FUNCTION_ROUTE, "
                         "START_SCREEN, PENDING)" % (slug, " and ".join(where) or "none"))
    for k, d in kinds.items():
        for slug in d:
            if slug not in slugs:
                fails.append("%s lists %r, which is not a numbered roster game: remove it" % (k, slug))

    for slug in slugs:
        page = root / "games" / slug / "index.html"
        rel = "games/%s/index.html" % slug
        if not page.exists():
            fails.append("games/%s/: in the roster but has no index.html" % slug)
            continue
        src = page.read_text(encoding="utf-8")
        f, el_id = check_page(rel, src, slug)
        fails += f
        if el_id is None:
            continue
        if slug in RESULTS:
            fails += check_location(rel, src, el_id, RESULTS[slug])
        elif slug in FUNCTION_ROUTE:
            if not PLACE.search(src):
                fails.append("%s: a function-route game must move its line into the end container it shows "
                             "(MaffsInvite.place); it never calls it" % rel)
        elif slug in PENDING:
            p = PENDING[slug]
            if lf_sha256(page) == p["sha256"]:
                notes.append("%s: %s" % (slug, p["why"]))
            else:
                fails += ["%s [the page has changed since it was listed as pending rebuild, so the line must now be on "
                          "its results screen; if the rebuild placed it in another container, move the game from "
                          "PENDING to RESULTS with that container]" % x
                          for x in check_location(rel, src, el_id, p["container"])]

    engine = (root / ENGINE).read_text(encoding="utf-8").replace("\r\n", "\n")
    fin = re.search(r"function finish\(win\) \{(.*?)\n  \}\n", engine, re.S)
    body = fin.group(1) if fin else ""
    if engine.count(ENGINE_MOUNT) != 1:
        fails.append("%s: want exactly one %s" % (ENGINE, ENGINE_MOUNT))
    elif ENGINE_MOUNT not in body or ENGINE_END not in body or body.index(ENGINE_END) > body.index(ENGINE_MOUNT):
        fails.append("%s: the line must be mounted in finish(), after %s rebuilds the end card" % (ENGINE, ENGINE_END))
    if engine.count(ENGINE_POINT) != 1 or ENGINE_POINT not in body:
        fails.append("%s: the mount point %s must be on the end card finish() builds, and nowhere else (not on "
                     "the brief)" % (ENGINE, ENGINE_POINT))
    for name in live_rooms(root):
        src = (root / "escape-rooms" / name / "index.html").read_text(encoding="utf-8")
        rel = "escape-rooms/%s/index.html" % name
        n = len(INCLUDE.findall(src))
        if n != 1:
            fails.append("%s: loads %s %d times (want once)" % (rel, ASSET, n))
        sm = ROOM_SLUG.search((root / "escape-rooms" / name / "room.js").read_text(encoding="utf-8"))
        if not sm or sm.group(1) != "escape-" + name:
            fails.append("escape-rooms/%s/room.js: slug %r is not 'escape-%s', so the line would name the wrong room"
                         % (name, sm and sm.group(1), name))

    fails += check_page("leaderboards/index.html", (root / "leaderboards/index.html").read_text(encoding="utf-8"), None)[0]
    return fails, notes


# ------------------------------------------------------------------------------------------------ Chromium half
def _serve(root):
    """serve-stubbed.py from `root` (analytics stubbed, so nothing is sent); returns (proc, base)."""
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    proc = subprocess.Popen([sys.executable, str(root / "scripts" / "serve-stubbed.py"), str(port)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=str(root))
    base = "http://127.0.0.1:%d" % port
    for _ in range(150):
        try:
            urllib.request.urlopen(base + "/schools/assets/analytics.js", timeout=2).read()
            return proc, base
        except OSError:
            time.sleep(0.1)
    proc.terminate()
    raise RuntimeError("serve-stubbed.py did not answer on port %d" % port)


# A new best score opens the leaderboard's initials prompt over the screen; a student presses Skip.
SKIP_INITIALS = """(() => {
  const b = document.querySelector('#mfg-initials-overlay .mfg-ini-skip');
  if (b && b.offsetParent !== null) b.click();
})()"""


async def _play(page, steps, limit=1500):
    for step in steps:
        await page.evaluate(SKIP_INITIALS)
        if step[0] == "click":
            await page.wait_for_selector(step[1], state="visible", timeout=15000)
            # A screen change opens a MaffsLock fresh window (canon 7.6.0) that drops any click for 300 ms: a
            # student's click lands after it, so the driver's does too (contract PLAY-AGAIN-SCREEN).
            await page.wait_for_function("!(window.MaffsLock && MaffsLock.isFresh())", timeout=15000)
            await page.click(step[1])
            await page.wait_for_timeout(150)
            continue
        _, js_step, js_done = step
        for _ in range(limit):
            if await page.evaluate(js_done):
                break
            await page.evaluate(SKIP_INITIALS)
            await page.evaluate(js_step)
            await page.wait_for_timeout(60)
        else:
            return "never reached its end in %d moves" % limit
    return None


def _viewport(width):
    return {"width": width, "height": 844 if width < 600 else 900}


async def _game_end_state(browser, base, slug, state, container, steps, width):
    ctx = await browser.new_context(viewport=_viewport(width))
    await ctx.add_init_script(FAST_INIT)
    page = await ctx.new_page()
    where = "games/%s/ (%s, %dpx)" % (slug, state, width)
    try:
        await page.goto(base + "/games/%s/" % slug, wait_until="domcontentloaded")
        await page.wait_for_timeout(500)
        if (await page.evaluate(LINE, None))["vis"]:
            return ["%s: the teacher line shows on the start screen; it belongs on the results screen" % where]
        why = await _play(page, steps)
        if why:
            return ["%s: played in Chromium, the game %s" % (where, why)]
        await page.wait_for_timeout(400)
        await page.evaluate(SKIP_INITIALS)
        got = await page.evaluate(LINE, container)
        if not (got["vis"] and got["inside"]):
            return ["%s: played to the end, the teacher line is %s" % (
                where, "not inside %s" % container if got["vis"] else "not visible on the end screen")]
        if got["href"] != "/feedback/?type=classroom&game=" + slug:
            return ["%s: the line links to %r" % (where, got["href"])]
        return []
    except Exception as exc:
        return ["%s: %s" % (where, str(exc).splitlines()[0][:160])]
    finally:
        await ctx.close()


async def _page_style(browser, base, slug):
    ctx = await browser.new_context(viewport=_viewport(390))
    page = await ctx.new_page()
    where = "games/%s/" % slug
    try:
        await page.goto(base + "/games/%s/" % slug, wait_until="domcontentloaded")
        await page.wait_for_timeout(300)
        got = await page.evaluate(STYLE)
        if got is None:
            return []  # reported by the static half
        fails = []
        if got["ratio"] < 4.5:
            fails.append("%s: the teacher line's contrast is %.2f:1 against the background behind it (want 4.5:1; "
                         "set an existing colour on the mount point)" % (where, got["ratio"]))
        if got["row"]:
            fails.append("%s: the teacher line sits inside %s, a flex row or grid, so it is squeezed in beside the "
                         "controls; put it after that row" % (where, got["parent"]))
        return fails
    except Exception as exc:
        return ["%s: %s" % (where, str(exc).splitlines()[0][:160])]
    finally:
        await ctx.close()


async def _room_end(browser, base, name, win, width):
    ctx = await browser.new_context(viewport=_viewport(width))
    page = await ctx.new_page()
    where = "escape-rooms/%s/ (%s, %dpx)" % (name, "win" if win else "loss", width)
    try:
        await page.goto(base + "/escape-rooms/%s/" % name, wait_until="domcontentloaded")
        await page.wait_for_selector("#startBtn", state="visible", timeout=15000)
        if (await page.evaluate(LINE, None))["vis"]:
            return ["%s: the teacher line shows on the brief; it belongs on the end card" % where]
        await page.click("#startBtn")
        for _ in range(400):
            if await page.evaluate("document.getElementById('scrEnd').classList.contains('active')"):
                break
            await page.evaluate(ROOM_STEP + "(%s)" % ("true" if win else "false"))
            await page.wait_for_timeout(40)
        else:
            return ["%s: played in Chromium, the room never reached its end card" % where]
        await page.wait_for_timeout(300)
        got = await page.evaluate(LINE, "#endCard")
        if not (got["vis"] and got["inside"]):
            return ["%s: the teacher line is not on the end card" % where]
        if got["href"] != "/feedback/?type=classroom&game=" + name:
            return ["%s: the line links to %r (want game=%s)" % (where, got["href"], name)]
        return []
    except Exception as exc:
        return ["%s: %s" % (where, str(exc).splitlines()[0][:160])]
    finally:
        await ctx.close()


def check_browser(root, games=None, rooms=None, styled=None, widths=WIDTHS):
    """Play every function-route end state, and every live room to a win and a loss, in Chromium; measure every
    roster page's line (contrast, and not in a row)."""
    from playwright.async_api import async_playwright
    games = list(FUNCTION_ROUTE) if games is None else games
    rooms = live_rooms(root) if rooms is None else rooms
    styled = roster(root) if styled is None else styled
    proc, base = _serve(root)

    async def run():
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            sem = asyncio.Semaphore(4)

            async def lim(coro):
                async with sem:
                    return await coro
            jobs = [lim(_game_end_state(browser, base, g, s, c, st, w))
                    for w in widths for g in games for s, (c, st) in FUNCTION_ROUTE[g].items()]
            jobs += [lim(_room_end(browser, base, r, win, w)) for w in widths for r in rooms for win in (True, False)]
            plays = len(jobs)
            jobs += [lim(_page_style(browser, base, g)) for g in styled]
            out = await asyncio.gather(*jobs)
            await browser.close()
            return [f for fs in out for f in fs], plays
    try:
        return asyncio.run(run())
    finally:
        proc.terminate()


# ------------------------------------------------------------------------------------------------ self-test
def selftest():
    slugs = roster(BASE)
    rooms = live_rooms(BASE)
    g = "truth-buster"
    point = '<p id="teacherInvite"></p>'

    def scratch(serve):
        d = pathlib.Path(tempfile.mkdtemp(prefix="invite-check-"))
        rels = [ROSTER, ASSET, ENGINE, "leaderboards/index.html"] + ["games/%s/index.html" % s for s in slugs] + \
               ["escape-rooms/%s/%s" % (r, f) for r in rooms for f in ("index.html", "room.js")]
        for rel in rels:
            (d / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(BASE / rel, d / rel)
        if serve:  # what a game needs to run: the shared assets and the stubbed server
            shutil.copytree(BASE / "schools", d / "schools", dirs_exist_ok=True)
            (d / "scripts").mkdir(exist_ok=True)
            shutil.copy(BASE / "scripts" / "serve-stubbed.py", d / "scripts" / "serve-stubbed.py")
        return d

    def edit(path, fn):
        s = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        t = fn(s)
        assert t != s, "planted fault changed nothing in %s" % path
        path.write_text(t, encoding="utf-8")

    page = lambda d, s=g: d / "games" / s / "index.html"

    def to_start(s):
        s = s.replace("\n  " + point, "", 1)
        return s.replace('onclick="startGame()">Start</button>', 'onclick="startGame()">Start</button>\n' + point, 1)

    def static(d):
        return check_static(d)[0]

    def log_laws(d):
        return check_browser(d, games=["log-laws"], rooms=[], styled=[], widths=(390,))[0]

    def styled(*slugs):
        return lambda d: check_browser(d, games=[], rooms=[], styled=list(slugs))[0]

    def unplace_solve(d):
        edit(page(d, "log-laws"), lambda s: s.replace("if (window.MaffsInvite) MaffsInvite.place($('solveOver'));", "", 1))

    def brief(s):
        s = s.replace("      '</div>' +\n      '<p id=\"teacherInvite\"></p>';", "      '</div>';", 1)
        return s.replace("'</div>' +\n        '</div>' +\n      '</section>';",
                         "'</div>' +\n          '<p id=\"teacherInvite\"></p>' +\n        '</div>' +\n      '</section>';", 1)

    cases = [
        ("clean copy passes", None, static, False),
        ("start-screen mount (static game)", lambda d: edit(page(d), to_start), static, True),
        ("missing end-state mount (log-laws solve)", unplace_solve, log_laws, True),
        ("wrong slug", lambda d: edit(page(d), lambda s: s.replace("'%s')" % g, "'%s-x')" % g)), static, True),
        ("clean copy passes in Chromium", None, log_laws, False),
        ("line the same colour as its card (Golf)", lambda d: edit(page(d, "estimation-golf"), lambda s: s.replace(
            'id="teacherInvite" style="color:var(--ink)"', 'id="teacherInvite" style="color:var(--cream)"')),
         styled("estimation-golf"), True),
        ("line inside a button row", lambda d: edit(page(d, "complex-converter"), lambda s: s.replace(
            'Menu</button>\n    </div>\n    ' + point, 'Menu</button>\n    ' + point + '\n    </div>')),
         styled("complex-converter"), True),
        ("clean pages pass the style check", None, styled("estimation-golf", "complex-converter", g), False),
        ("control after the line", lambda d: edit(page(d), lambda s: s.replace(
            point, point + '\n  <button onclick="startGame()">x</button>', 1)), static, True),
        ("function-route game never places", lambda d: edit(page(d, "factor-theorem"), lambda s: s.replace(
            "if (window.MaffsInvite) MaffsInvite.place(resultsEl);", "")), static, True),
        ("roster game in no list", lambda d: edit(d / ROSTER, lambda s: s + "\n| 999 | X | `truth-buster-2` | x |\n"),
         static, True),
        ("mount call removed", lambda d: edit(page(d), lambda s: MOUNT.sub("", s)), static, True),
        ("link text altered", lambda d: edit(d / ASSET, lambda s: s.replace("love to hear", "like to hear")), static, True),
        ("script include removed", lambda d: edit(page(d), lambda s: INCLUDE.sub("<script data-x", s)), static, True),
        ("escape-room line back on the brief", lambda d: edit(d / ENGINE, brief), static, True),
        ("live room without the include", lambda d: edit(d / "escape-rooms" / rooms[0] / "index.html",
                                                          lambda s: INCLUDE.sub("<script data-x", s)), static, True),
        ("leaderboards names a game", lambda d: edit(d / "leaderboards/index.html", lambda s: s.replace(
            "'teacherInvite'), null)", "'teacherInvite'), 'x')")), static, True),
    ]
    # A pending game whose page changes must have its line on its results screen. Planted on the first PENDING
    # game, so it runs only while one is pending (none since estimation-engine's rebuild, 6 Oct 2026).
    pend = next(iter(PENDING), None)
    if pend:
        cases.append(("pending page changed, line not moved", lambda d: edit(page(d, pend),
                                                                     lambda s: s + "\n<!-- rebuilt -->\n"), static, True))
    bad = []
    for name, plant, run, should_fail in cases:
        d = scratch(serve=run is not static)
        try:
            if plant:
                plant(d)
            got = run(d)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        ok = bool(got) == should_fail
        print("  %s  %-42s %s" % ("PASS" if ok else "FAIL", name, got[0] if got else "(no failures)"))
        if not ok:
            bad.append(name)
    print("selftest: %s (%d cases)" % ("FAILED: " + ", ".join(bad) if bad else "PASS", len(cases)))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--static", action="store_true", help="skip the Chromium half")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    fails, notes = check_static(BASE)
    played = 0
    if not a.static:
        bf, played = check_browser(BASE)
        fails += bf
    for n in notes:
        print("NOTE", n)
    for slug, why in sorted(START_SCREEN.items()):
        print("NOTE %s keeps its start-screen line: %s" % (slug, why))
    for f in fails:
        print("FAIL", f)
    print("teacher line: %s (%d roster games: %d static results screen, %d function route, %d start screen, %d pending; "
          "the escape-room engine; /leaderboards/; %s)"
          % ("FAIL" if fails else "PASS", len(roster(BASE)), len(RESULTS), len(FUNCTION_ROUTE), len(START_SCREEN),
             len(PENDING), "%d end states played in Chromium" % played if played else "Chromium half skipped"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
