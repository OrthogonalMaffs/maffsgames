---
name: snagging-list
description: Running list of small issues Jon finds while testing live games — content errors, UI bugs, wrong hints. Not for architecture decisions or backlog items (those live in canon.md).
---

# MaffsGames Snagging List

Small, testable issues found during play-testing. Each entry should be small enough for Code Claude to action without further scoping — if it turns out to be bigger than that, it graduates to canon.md as a proper backlog item.

**Status key:** Open · Fixed (commit ref) · Won't fix (reason)

---

## Open

### 8. Graph Transformer — GCSE #11/#12 target the identical curve

- **Game / URL:** `graph-transformer`, `?level=gcse`
- **Found:** 29 Sep 2026, by the new `scripts/verify-graph-transformer.py`'s duplicate-curve check, while fixing the 3 par-verification mismatches in #7 above (not one of the three named there).
- **The defect:** puzzle #11 "Reflect in x-axis" (`x³`, target `a=-1`) and puzzle #12 "Reflect in y-axis" (`x³`, target `b=-1`) are the identical curve `y=-x³`, since `x³` is an odd function — `f(-x) = -f(x)` for it, so reflecting in the y-axis and reflecting in the x-axis land on the same graph. Same root-cause class as #7's match-check bug (reflect-x/reflect-y aliasing on an odd function), just showing up here as two puzzles with no distinguishable target rather than a wrongly-rejected route.
- **Status:** Open — reported to Jon rather than fixed, per the par-verification task's own stop condition (only the three named A-level puzzles were in scope). Jon's ruling 29 Sep 2026: track it, don't fail CI on it, fix later. Tracked in `KNOWN_DUP_PAIRS` in `scripts/verify-graph-transformer.py` so CI stays green on this known pair but would still fail on any new duplicate.

### 2. Spot the Error — Stage 2 "Find the misread" is badly designed; audit whole game

- **Game / URL:** `spot-the-error` (seen on the default tier; other tiers unchecked)
- **Found:** 27 Sep 2026, by Jon
- **Scheduled:** after CC finishes its current task. Jon's verdict: "it's a poor game".
- **How the game works:** Stage 1 shows a scenario with a wrong calculation and the student spots the error. Stage 2 reuses the same scenario and asks the student to "find the misread" by clicking a phrase.
- **Issues seen on live:**
  1. **Label contradicts mechanic.** "Find the misread" reads as "find the mistake", but the phrase to click is correct text (e.g. "total length of fencing needed"). A literal-minded student hunts for a false statement, finds none, and is marked wrong. Either the wording changes or the thing clicked must itself be wrong.
  2. **Stage 2 does not show the wrong working from Stage 1**, so the target phrase can't be derived from what is on screen.
  3. **Many "misreads" are really method errors.** E.g. the basketball item (6 players mean 17, 7 players mean 17.5, find the 7th = 20.5): the usual error is averaging means or not converting to totals, which is METHOD, not READING. The stage is labelled as one skill and tests another.
  4. **The scenario is rendered twice** on the Stage 2 screen (the box, then the clickable copy): double the reading load.
  5. "A coach calculates" doesn't say the calculation is wrong.
- **Maths itself looked sound** in both items seen (fencing 2(85+62)=294 m; basketball 20.5 years).
- **Step 1 — read-only extraction: DONE 28 Sep 2026.** `docs/audit-spot-the-error.md`, one row per
  question (all 110: KS3 35 / GCSE 45 / Level 4 30). Confirms issues 1, 2 and 4 above are **100%
  systemic** (every question, not occasional) from the game's own code, not authoring variance.
  Issue 3 also confirmed platform-wide: the bank's own `errorType` field never has a "reading"
  value — **110/110 questions classify as METHOD, 0 as READING**. A STOP IF fired (counts don't
  reconcile) and was resolved in the audit's own header: `data/banks/spot-the-error.json` is a
  corrupted export (all three tiers hold the same combined 110-question list, not their own 35/45/30
  split) — not read by the live game, but flagged as a live bug (`docs/todo.md` 1.20). Two further
  live bugs found and filed: `ste_gcse_016`'s Stage 2 is unwinnable (1.21), and `ste_gcse_002`'s
  "corrected" compound-interest answer is itself wrong by 20p (1.22). KS3 (35) and Level 4 (30) are
  both under the 40–50 question minimum (1.23).
- **Step 2 — Jon's decision after the audit:** relabel Stage 2 honestly (e.g. "Which phrase did the student misread?", with the working shown) vs re-author its bank as genuine misreads vs redesign the game. Likely graduates to canon.md as a backlog item at that point.
- **Related:** Google Search Console lists `/games/spot-the-error/` (and `?level=ks3`) as **Soft 404**, last crawled 19 Jul. Hold the indexing request until the content is fixed.
- **Status:** Step 1 done, awaiting Jon's decision on Step 2

### 1. Truth Will Set You Free (Level 4) — false "can be simplified" hint
- **Game / URL:** `truth-will-set-you-free`, `?level=level4`
- **Found:** 31 Aug 2026, by Jon
- **Issue:** After answering correctly with `A · B`, the game shows: *"This expression can be simplified using Boolean algebra — try Boolean Blitz."* This is mathematically false — `A · B` is already in minimal form (a single AND of two uncomplemented literals; no Boolean law reduces it further).
- **Why it matters:** Platform principle is curriculum-serious, mathematically rigorous content. A false simplification claim shown as fact to students undermines that, and the cross-promo to Boolean Blitz is riding on an incorrect premise.
- **Suspected cause (needs confirming):** Hint may fire unconditionally on every question in this game rather than checking whether the matched expression is actually reducible. If so, this is a template-level bug, not a one-off wrong string — check whether other already-minimal answers (e.g. any single-literal or two-literal AND/OR with no complements) trigger the same false hint.
- **Suggested fix:** Suppress the "can be simplified" hint (and the Boolean Blitz link) when the correct expression is already in minimal SOP/POS form. Confirm scope before Code Claude touches it — this may be one conditional or a per-question flag depending on how the hint is currently wired.
- **Status:** Open

## Fixed

### 7. Graph Transformer — marking by route not value, click-counted moves, doubled brackets
- **Game / URL:** `graph-transformer`, `?level=gcse` (all three defects reproduced there; (b) and (c) also affect `?level=alevel`)
- **Found:** 29 Sep 2026, by Jon, live at `?level=gcse`
- **Three defects, one game, fixed together:**
  1. **Matching compared the route, not the curve.** `checkMatch()` compared the student's `{a,b,h,k}` transform tuple against the target's tuple directly. `y = (-x)^3` (Reflect y-axis) and `y = -x^3` (Reflect x-axis) are the identical curve on an odd function, but their tuples differ (`b=-1` vs `a=-1`), so the correct-but-differently-routed answer was rejected. Same class as `docs/todo.md` 1.24 ("marking by representation instead of value") — noted there as a further instance, not widened into that contract.
  2. **Par counted transformations; moves counted every button click.** A shift of size *n* took *n* clicks but was worth 1 transformation, so a correct solve using any multi-unit shift scored *n − 1* over par (7 moves vs par 2 on `(x+3)² + 4`; 2 vs par 1 on `sin(x) + 2`, rated "One over par. Close!" when it should have been "Par! Perfect.").
  3. **Horizontal shifts rendered with doubled brackets:** `((x + 3))² + 4`, `sin((x + 3))`. Root cause: the shift step already produced a self-contained `(x±h)` when there was no `b`-coefficient, and the base-function step then wrapped it again without checking.
- **Fixed 29 Sep 2026** (`games/graph-transformer/index.html`):
  1. `checkMatch()` now calls `curvesMatch()`, which evaluates both curves at 601 fixed, deterministic sample points across the plotted range and requires agreement to 1e-9 (relative above magnitude 1, absolute below); a point where one curve is defined and the other isn't is a mismatch, both-undefined points are ignored.
  2. A move is now a maximal run of consecutive clicks on the same *shift* button (Left/Right/Up/Down) — Left, Left, Left is 1 move. Reflections and stretches are deliberately never merged, even against themselves (Reflect x-axis twice is 2 moves), since repeating one changes the outcome each time. Tracked via a click log recomputed on every change, including undo, so "undo empties the run → moves drops by one" falls out for free.
  3. `buildEquation()` reuses the shift's own bracket instead of adding a second one when nothing else needs wrapping; a coefficient or reflection sign between two brackets (`2(x-3)`, `-(x-3)`) is legitimate nesting and was left alone, since removing it would be a different, unrequested defect.
- **Verified:** scripted Playwright pass against `serve-stubbed.py`, driving the shipped page directly — both reflection routes accepted for `y=-x^3`; a genuinely different curve and a curve agreeing on only part of the range both correctly rejected; a domain/asymptote mismatch correctly rejected; Left×3-then-Up×4 on `(x+3)²+4` shows 2 moves and rates "Par! Perfect."; Up×2 on `sin(x)+2` shows 1 move and rates "Par! Perfect."; Left,Right = 2 moves; Reflect x-axis twice = 2 moves; undo behaves as specified; a sweep of every puzzle's target in both tiers plus every reachable intermediate state (all 6 bases × h,k ∈ [-4,4] × a,b ∈ {1,-1,2,0.5,3}) found no doubled brackets or malformed signs. `check-site.py --tier all`: 348 PASS/0 FAIL/0 WARN, network guard clean. `--tier 3 --only graph-transformer`: UNSUPPORTED (not a pick-one/typed-answer shape — recorded in `scripts/checker-allowlist.json`), 0 FAIL.
- **Par verification (BFS, bounded depth 4, moves not clicks, same `curvesMatch()` the game ships) found 3 mismatches out of 50 puzzles — reported, none touched, per DO NOT TOUCH:**
  - **A-level puzzle "Stretch ×3 y, left 1, up 2" (par 3) and "Amp 3, freq 2, down 1" (par 3) are both unreachable.** Both target `a=3`, but the only amplitude buttons are Stretch ×2/×½, which only ever reach powers of 2 (and their negatives via reflect) — 3 is never reachable from 1. These two puzzles cannot be solved as authored.
  - **A-level puzzle "Stretch ×2 y, reflect, right 1, up 3" (par 3): true minimum is 4 moves, not 3.** Reaching `a=-2` from `a=1` needs Reflect x-axis *and* Stretch ×2 y — two separate buttons, no single click does both — so the `a`-dimension alone costs 2 moves, plus 1 for the shift and 1 for the merged up-run = 4. Par understates the true difficulty.
  - No GCSE-tier mismatches found.
- **All 3 mismatches above fixed 29 Sep 2026, later still, and the par-verification pass turned into a permanent CI check.** On Jon's ruling: both amplitude-×3 targets retargeted to ×2 (the puzzle formerly "Stretch ×3 y, left 1, up 2" is now `y=2(x+1)²+2`, par 3 unchanged; the puzzle formerly "Amp 3, freq 2, down 1" is now `y=2sin(2x)-1`, par 3 unchanged; both puzzles' `desc` text updated to match); the reflect+stretch puzzle's par corrected 3→4, target unchanged. New `scripts/verify-graph-transformer.py` reads `window.GT_VERIFY` (added to the game file: `transformButtonDefs()` factored out of `buildTransformButtons()` with identical behaviour, plus a `gtBfsCheck`/`gtCurveKeyPairs` hook — no button, match-check or move-counting logic touched) and runs the same BFS, now wired into `.github/workflows/check-site.yml`, so a future unreachable target or wrong par fails CI instead of shipping. Confirmed locally: the two retargeted puzzles solve in 3 moves at par, the reflect+stretch one in 4 at par; all 50 puzzles across both tiers reachable and correctly parred except the tracked exception in #8 below. Fault-injection self-test (built into the script, runs every CI pass): clones a puzzle and forces its amplitude back to 3 — caught as unreachable; clones another and mutates its par by +1 — caught as a par mismatch. Also hand-verified once outside the self-test: edited the live file to reintroduce amplitude 3 on the fixed puzzle, ran the verifier, got `FAIL: ... target {'a': 3, ...} is UNREACHABLE`; reverted; edited the file to set the reflect+stretch puzzle's par back to 3, ran the verifier, got `FAIL: ... stored par 3 != true minimum 4 moves`; reverted; re-ran, got `PASS`. `check-site.py --tier all`: 348/0/0; `--tier 3 --only graph-transformer`: UNSUPPORTED, 0 FAIL, unchanged; `check-banks.py --ci`: matches the ledger exactly (95/95), unaffected.
- **Leaderboard (read-only, not touched):** `firebase-leaderboard.js`'s `submitScore()` stores only `{score, timestamp, initials?}` per entry under `leaderboards/graph_transformer_{level}` — no per-puzzle move or route data anywhere, client-side or in the Sheets/GA4 analytics events (`question_answered` for this game only ever carries `correct`/`question_index`, never moves). **Existing entries cannot be re-derived** against the fixed rules — there is nothing to recompute from. Both bugs only ever depressed scores (a rejected valid route forced extra moves or a skip; every multi-unit shift over-counted moves against par), never inflated them, so historical entries are a systematic underestimate of what the same play would score today, not corrupted. Whether to leave them, wipe them, or annotate them is Jon's call, not made here.
- **Suggestion, not built, Jon's call for later (ruled 29 Sep 2026):** a "choose the size of a shift in one move" option (e.g. "Left ×3" as a single button/input) so the student reads the transformation off the target equation before seeing it move, rather than discovering the shift size by repeated 1-unit clicks. Project Claude's note: this could combine with the merged-click scoring already shipped here as a fading scaffold — offered at higher tiers, or unlocked after N on-par solves — rather than replacing 1-unit clicks outright. Unscoped; no button-set or puzzle-content change made in this session (out of scope per DO NOT TOUCH).
- **Status:** Fixed
