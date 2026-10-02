# Game integrity — 21 September 2026

Four games repaired in five commits, all live. This file exists because the **prevention layer is
still unbuilt**: `scripts/check-game-console.py` does not exist, and the next contract for it should
start here, because none of the four defects below would have been caught by loading a page and
reading the console.

| Commit | Game | Broken since | What it was |
|---|---|---|---|
| `2ec80e0` | chart-interrogator | 22 Mar 2026 (`96381d74`) | HTML swept into a JS string; whole script failed to parse |
| `b685e44` | modular-battle | never playable | parse error (`76514c70`) masking an infinite loop (`1a407fe`) |
| `4917203` | expectation-station | — | distractor loop that could not terminate on its own resources |
| `9b1c4e2` | expectation-station | 2 Mar 2026 | `es_gcse_005` unwinnable; game moved onto exact rationals |
| `9e6d9e1` | expectation-station | always | loss scenarios had no negative distractors |

---

## 1. The sweep-damage class — closed

Two site-wide sweeps inserted markup by matching page text without regard to whether the match sat
in HTML or inside a `<script>`:

- **`96381d74`** "Add leaderboard teaser to all game results screens" (80 files)
- **`76514c70`** "Add 'Back to Games' link to all 81 game results screens" (48 files)

Note `02f41a5f` (26 Aug) only swapped the teaser text for a real `/leaderboards/` link — it
inherited the break in chart-interrogator rather than causing it. Blame on the visible line is
misleading here; the damage is older.

**All 95 `games/*/index.html` were scanned for both shapes and are now clean.** Two detectors were
used, and each was blind to the other's defect:

- unterminated `'`/`"` string inside a `<script>` — caught chart-interrogator
- HTML in *code* position, i.e. `<` starting a tag while not inside any string — caught
  modular-battle, whose damage left every string balanced

`regression-rumble` matched on text but is correctly formed inside JS strings — a false positive.
Four games (`decimal-detective`, `maths-court`, `split-it`, `the-perfect-prank`) tripped the second
detector on nested template literals; all four were cleared by loading them.

**Lesson for the checker:** a text search for the swept strings finds the wrong set in both
directions. Only a parse-level check is reliable, and the repo has no Node, so the checker must
either drive a browser or carry its own JS-aware scan.

---

## 2. Hang-capable loops — scan of all 95 games + escape-rooms

Rejection sampling into a fixed-size collection hangs whenever the candidate pool is smaller than
the target. Six loops match the shape. **Two were real; four survive on bank size, not structure,
and a content edit could trip any of them.**

| File | Line | Pool | Verdict |
|---|---|---|---|
| `modular-battle` | 171 | residues `0..b-1`, `b = randInt(2,9)` | **Was live** — froze on 25% of questions. Fixed `b685e44` |
| `expectation-station` | 1162 | `\|p ± 0.15\|` per correct product | **Latent** — 2 of 45 scenarios had pool 1 vs target 2; only the earlier phase covering the shortfall kept it alive (~1e-30 hang). Fixed `4917203` |
| `complex-converter` | 718 | full bank, 48 distinct keys, N=5 | Safe *because* 48 ≫ 5 |
| `gradient-hunter` | 690 | `QUESTIONS[level]`, 20 and 15 | Safe *because* both banks non-empty |
| `maths-court` | 638 | bank, guarded on `length` | Structurally safe — appends duplicates |
| `negative-number-line` | 839 | integers −10..10, N=4 | Safe *because* 21 ≥ 4 |

The four "safe" ones were deliberately **not** changed — no present bug. They want a CLAUDE.md rule
(build distractors by construction, never by retry) plus the checker, not edits.

**Lesson for the checker:** a hang shows nothing on page load. Catching this class means driving a
number of questions per game with a watchdog, and because the failure is a wedged renderer the
checker must time out rather than wait.

---

## 3. The answer-key tier — the `es_gcse_005` class

`es_gcse_005` could not be completed by a correct student. Its product 0.375 was displayed as the
tile `"0.38"`, and `checkStage2` re-parsed that tile and accepted only `|student − correct| < 0.005`
against the 4dp product. The difference is exactly 0.005 — in floating point a shade more — so the
right answer was marked wrong, twice in that scenario.

This is the general rule the site should hold to: **never compare a re-parsed display value.** A
tile's identity belongs in `dataset.val` or a closure; marking compares that, not what was drawn.
Expectation Station now marks on canonical `"n/d"` rational keys.

**Lesson for the checker:** a page with zero console errors can still be unwinnable. Catching this
tier means a checker that plays the correct answer and asserts it is *accepted* — the most valuable
and most expensive tier, and it needs a per-game answer key.

---

## 4. Expectation Station — how it is built now

Worth knowing before editing the bank or the game.

- Probabilities, x-values, products and E(X) are **reduced rationals** built from the bank's own
  strings by digit count, never from floats. Helpers: `ratFromString`, `ratMul`, `ratAdd`, `ratKey`.
- **Tiles carry `dataset.val = "n/d"`**; `checkStage2` compares keys. Nothing read off the screen
  takes part in marking.
- **E(X) is the rational sum of the products**, so the tiles always add up to the total shown. The
  bank's `answer` field is no longer used for display. Exact decimal when it terminates, otherwise
  the fraction plus a 2dp reading (`4/3 ≈ 1.33`), taken from the rational.
- **Display form is per scenario, not per value.** If any product needs a fraction the scenario is
  `FRACTION` mode and every non-integer it shows — tiles, distractors, the `P(X = x)` column — is a
  fraction over the common denominator `L`. Three scenarios are FRACTION (`es_gcse_003`,
  `es_gcse_008`, `es_alevel_005`); the other 42 are DECIMAL and render exactly as they always did.
- **Distractors are enumerated, deduped, shuffled and sliced** — never retried. Offsets are taken in
  the scenario's own form (`1/L`, `2/L` in FRACTION; `1/20`, `1/10` in DECIMAL), topping up outward.
- **Negatives are a per-scenario property.** `es_alevel_008` and `es_alevel_010` model losses; they
  drop the `≥ 0` floor and reserve one negative distractor per draw, so sign alone never identifies
  a tile. The other 43 keep the floor.

### Bank observations — reported, not edited

- `es_gcse_003` and `es_gcse_008` are authored to **rounded** sums (1.33, 1.67) while `es_gcse_005`
  is authored **exactly** (1.5). The bank mixes conventions. Derived E(X) never differs from the
  authored `answer` by more than 0.005, so there are no authoring errors — only this inconsistency.
- Stage 3 option texts state decimals (`£1.33`, `1.67`), which is why non-terminating E(X) is shown
  as `4/3 ≈ 1.33` rather than as a bare fraction. **If those texts change, check the display still
  agrees.** `es_gcse_008`'s wrong answer depends on the words "1.67 rounds to 2".

### Open question for Jon

The `P(X = x)` column still goes through `formatPNum` in DECIMAL mode, because retiring it globally
would change all 42 decimal scenarios (`formatPNum` emits `"0.50"` where exact rendering gives
`"0.5"`). It is retired in FRACTION mode only. Say if it should go entirely.

---

## 5. Testing notes

- **Live verification must cache-bust.** A live check during this session reported a clean pass that
  was actually Chrome replaying the previous build from eight minutes earlier. It can produce a
  false green as easily as a false red. Append `?cb=<random>` to every live fetch and page load.
- **The automation tab reports `document.hidden`**, so timers throttle to ~1.5/sec and any
  poll-based driver stalls. The reliable harness is to capture the game's own `setTimeout`
  callbacks and drain them synchronously — every callback still runs, in order, without the waits.
  Test-only; never commit it.
- `scripts/serve-stubbed.py` stubs `window.fetch` site-wide, so in-page `fetch` fails with
  `Error: stubbed`. Use `XMLHttpRequest` when a test needs to read a file.
