# Next contract — leaderboard tidy (queued 30 Sep 2026, for a new session)

**BUILT 30 Sep 2026**: all three rulings, in the PR that carries this note. The record and the
follow-ups are in `docs/todo.md` START OF NEXT SESSION. The scan below was ported into
`scripts/check-site.py` ("Tier 1, level controls"). No game needed declaring, because the generic
reveal and menu steps reach `split-it`, `prisoners-dilemma` and `proof-builder`.

**State when queued.** PR #21 (Six Sevens, Bruv + hub-registry check) is **merged** (`562abef`). Nothing
below has been built. Jon's rulings are recorded verbatim-in-substance; the class-check scan for 2(a)
has **already been run** and its result is below, so the next session starts from the finding, not
from zero. Merge on green, handover in `docs/todo.md`.

## Jon's rulings (30 Sep 2026)

**2(a) regression-rumble.** Fix the crash so both Level 4 routes play and submit `level4` (the key the
roster and hub use). Existing leaderboard entries untouched; the hub lists Level 4 once (it already
does — `core`, `alevel`, `level4`; PR #21 corrected it). **Class check first:** the checker never
clicks level buttons (tier 1 loads `?level=` URLs, tier 3 plays from the URL), so any game whose
button sets a key its banks don't have is invisible to CI. Scan every game with a level picker: for
each button, confirm its key resolves to a bank/generator and a first question renders. Report every
failure; fix only regression-rumble here, list the rest for a separate contract. Then **add the check
to tier 1 or tier 3** (Code Claude's call) so a dead level button fails CI; prove it on
regression-rumble's pre-fix code.

**2(b)** `.claude/rules/game-roster.md`: binomial-blaster's second level is A-Level Year 2 (`alevel2`),
not L4.

**2(c) Ticker labels.** Build the separate-map design, with Jon's change: the new forward map
(key → label) covers **every submitted key, old and new**, so `levelLabel()` is the single source for
naming a level. The existing label → key lookup (`LABEL_TO_LEVEL`, built from `LEVEL_LABELS`) is
**frozen as legacy**, commented as used only for ticker entries written before `levelKey` existed
(28 Sep), and never extended. Daily keys via a pattern list (`daily-YYYY-MM-DD` → "Daily pizza DD Mon").
`submitScore()` uses `levelLabel()`. `scripts/check-leaderboard-coverage.js` loads
`firebase-leaderboard.js` (it runs without Firebase — verified with a bare `vm` context on 30 Sep) and
FAILS on any submitted level `levelLabel()` cannot name; prove it by removing one label.
*Why frozen, not extended:* `index.html:3777` resolves old ticker entries with
`levelKeyFromLabel()`; adding `l4: 'Level 4'` to the inverted map would re-key every old "Level 4"
entry to `l4`, and a pattern cannot be inverted at all (the STOP IF that paused 2(c)).

Tiers 1+2 green, merge on green, handover in todo.md.

## 2(a) class-check scan — ALREADY RUN (30 Sep 2026), result

**46 games have a level picker; 123 level controls pressed; 1 dead: `regression-rumble` L4.** Every
other control starts its game (`game_started` fires, no uncaught exception).

- **regression-rumble, L4 button:** sets `selectedLevel = 'l4'`; `beginGame()` reads `SCENARIOS['l4']`
  (only `level4` exists) and throws `Cannot read properties of undefined (reading 'slice')` —
  unplayable from the button. `?level=l4|level4` maps to `level4` and works. `pillMap['l4']` is also
  missing (line ~416), so a one-line fix at `selectLevel()` (normalise `l4` → `level4`) is the
  minimal change; check `getBestKey()` and the pill map follow.
- **Eight controls start only after further menu steps**, each confirmed by hand to fire
  `game_started` at its own level: `glorious-gantt` core/level4 (needs a mode — `data-mode` — before
  Start), `proof-builder` alevel/further (starts from a `.mode-card`), `prisoners-dilemma`
  ks3/gcse/alevel/core (opponent `.opp-card` appears after the level click).
- Games covered: angle-ace, better-value, binomial-blaster, chart-interrogator, component-crusher,
  coordinate-geometry-dash, curling-friction, distinctly-average, equation-builder, estimation-golf,
  expectation-station, force-resolver, formula-forge, formula-unlocked, given-that, glorious-gantt,
  gradient-hunter, graph-sketcher, graph-transformer, growth-and-decay, higher-power, integration-duel,
  linear-equation-solver, maths-court, matrix-crunch, moments-master, prisoners-dilemma, proof-builder,
  proportion-blaster, quadratic-factoriser, regression-rumble, scale-factor-scaling, screening-room,
  sequence-solver, seven-bridges, simultaneous-solver, spot-the-error, spot-the-muppet,
  standard-form-blitz, stat-attack, surd-simplifier, terrible-advice, trig-identity-duel,
  unit-converter, word-problem-decoder, wrong-on-the-internet.
- **Known gap to close in the CI version:** `split-it`'s level buttons (`onclick="startGame('ks3')"`)
  were not reached — they are not visible on first load (a mode is chosen first). Re-check which other
  games hide their picker behind a first screen.

### How the scan found and drove controls (port this into check-site.py)

A level control is any visible element that is (1) `[data-level]`, or (2) `[onclick]` calling a
function with a level-key literal (`ks3|gcse|alevel|alevel2|further|level3|level4|l3|l4|core|year6|
higher|formula|foundation`), or (3) a `<button>` inside a level container (`[id*=level i]`,
`[class*=level-select|level-row|levelselect|level-grid i]`, `[id*=lvl i]`) — the third rule is what
reaches pickers built in JavaScript (`quadratic-factoriser`, `distinctly-average`). Controls are indexed
in document order so a fresh page can press the same one.

Per control, in a fresh page with `TIER3_INIT` (it records `game_started` via the `mfg` accessor and
provides `__mfgClickStart`): load bare → press the control → press the first visible element of each
other picker attribute (`data-type`, `data-mode`, `data-stage`, `data-topic`, `data-count`,
`data-length`, `data-tier`) → `__mfgClickStart()` → poll ~3 s for `game_started`.
**FAIL** = an uncaught exception after the press (the dead-key signature). **PASS** = `game_started`.
Neither → FAIL unless the game is declared (with a reason, like `tier3_exceptions`) as needing menu
steps the driver does not make; declared games still FAIL on an exception. `prisoners-dilemma` and
`proof-builder` would need declaring; `glorious-gantt` passes once other pickers are always pressed.
**Do not count "options on screen" as started** — the level picker itself is an option group, which
made regression-rumble's crash read as a pass in the first draft.

Recommended home: **tier 1** (tier 3 is not in CI; the requirement is that CI fails). Cost measured
locally: ~123 fresh page loads.

## Also queued with this contract

- **Free Daily Pizza item 7 is ruled** (applied to `docs/next-contract-free-daily-pizza.md` in the PR
  that queued this file): `mode` is `'practice-q20' | 'practice-q40' | 'daily'`.

## Environment notes for the next session (this sandbox)

- The agent proxy blocks the KaTeX, Firebase, gtag and font CDNs, so local tier 1 FAILs on every
  page for network reasons; CI is the authority. For local driving, stub KaTeX with
  `window.katex={render(t,el){el&&(el.textContent=t)},renderToString:String}` via a route.
- `serve-stubbed.py` refuses a port still in TIME_WAIT; pick a free port per run.
- `pkill -f <pattern>` inside the same shell command matches the shell itself and kills it (exit 144).
- Installed Playwright must match the pre-installed Chromium build: `pip install playwright==1.56.0`.
