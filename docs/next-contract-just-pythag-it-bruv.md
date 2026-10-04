# Next contract: Just Pythag It, Bruv (HELD for a fresh session)

**Status (4 Oct 2026):** Jon issued this contract on 4 Oct, then held it: "please hold this contract until
after we clear, update docs and we will make pythag in a fresh session, along with the addendum for scaled
triples". Nothing is built. The contract and the addendum are recorded below word for word. The build target,
its band (STRETCH) and the design are also in `docs/resit-coverage-audit.md` §10.4 and `docs/todo.md`
(build order, item 14).

---

## The contract (Jon, 4 Oct 2026), verbatim

TASK: Build "Just Pythag It, Bruv", a resit-strand Pythagoras game, and merge it UNLISTED overnight for Jon to play in the morning; introduce a reusable "calculator" tag with this game as its first user.

ROOT CAUSE: Pythagoras (G20, banded STRETCH by Jon on 4 Oct) has no dedicated game; the audit's G20 cover rests on trig-worms. The commonest error is adding when the hypotenuse is given. Separately, games carry no calculator guidance, which matters for paper-specific revision.

CLASS CHECK: Partly. The game is a new build, following the resit strand's reference implementation (six-sevens-bruv) and shared components (MaffsAnswer, MaffsNext, MaffsSession, theme.css, analytics, leaderboard). The calculator tag is a class: make it one reusable field and one shared badge style, not a one-off in this game.

EXACT CHANGE:
1. games/just-pythag-it-bruv/index.html, single file, on the shared theme (MIGRATED in check-theme.py), Outfit/JetBrains Mono, own accent, no emoji, KaTeX for a² + b² = c². Age-neutral copy (SR-11). Fits 320px.
2. One level, key and label "Foundation". Sessions of 20 (MaffsSession) with a leaderboard for that length; all four canon §1.3 analytics events with required parameters; personal best.
3. Each session runs three stages in order: (a) whole-number triangles (Pythagorean triples and multiples: 3-4-5, 5-12-13, 8-15-17, 7-24-25…); (b) decimal answers; (c) worded adult contexts in metric units (ladder against a wall, TV screen diagonal, wheelchair ramp, shortcut across a field, a sloping roof). Every number plausible in context.
4. Every question: a drawn right-angled triangle with the right angle marked, in varied orientations and rotations, so the hypotenuse is never in a fixed position. Over a session, at least 60% of questions are find-a-shorter-side; the two types are mixed so no more than two of the same type appear in a row.
5. Answers typed. Exact integers marked with MaffsAnswer.exact(); others to 1 d.p. with "Give your answer to 1 decimal place." and MaffsAnswer.decimal(raw, key, 1). Keys computed exactly, rounded half up (SR-1).
6. Targeted help (Jon, 4 Oct): on a find-a-shorter-side question, if the answer matches the add-instead-of-subtract value (rounded the same way), show a worked example using that question's own numbers (identify the hypotenuse; it is given, so subtract), behind MaffsNext with no timer, for the first three occurrences per session; after that, the one-line nudge "Is the side you're finding the longest one?". Other wrong answers get normal feedback with the worked solution.
7. Calculator tag (reusable): add a "Calculator" field to the roster for every game, set to "required" for this game and "untagged" for all others. Add one shared badge style (in theme.css) and show "Calculator required" on this game's start screen. Record the field and its values (required / not allowed / optional / untagged) in canon. No other game's display changes.
8. scripts/verify-just-pythag-it-bruv.py (CI): over many seeds, check every triangle is valid (hypotenuse longest and opposite the right angle); every key is exact or correct to 1 d.p. per SR-1; stage order; ≥60% shorter-side and no run of three; the add-instead-of-subtract detection fires exactly when it should; contexts use plausible numbers. Self-test with planted faults.
9. UNLISTED: noindex; not on the portal, /resit/, the sitemap, the spec map or /updates/. Add it to the roster as unlisted. If any CI check requires listing to pass, use the narrowest documented exemption and say so.
10. todo START: "Jon to play /games/just-pythag-it-bruv/; on approval: list it on the portal, /resit/ (Geometry and measures, Choose: Foundation, Calculator required), spec map G20, sitemap, and queue an /updates/ entry." CLAUDE.md handover.
11. Full local suite (allow for the known Windows-only failures), push, PR, merge on zero failing checks, confirm the live URL loads and plays and is noindex. Post progress lines during long waits.

DO NOT TOUCH: Any other game's behaviour or display. The portal, /resit/, spec map, sitemap, /updates/ (all at listing time, not now). Shared components' behaviour (use them; don't change them, except adding the badge style to theme.css).

SUCCESS CONDITION: The game is live at its URL, unlisted and noindex; it meets every design point above, verified by its CI verifier (which fails on planted faults); the calculator field and badge exist and are documented; the PR merged on green; the morning handover tells Jon exactly where to play it and what listing will involve.

STOP IF (leave the PR open with a report; do not merge): A shared component would need changing to support a design point. Any CI check can't pass without listing the game. Triangle drawing at 320px can't keep labels legible. Anything in the design above turns out to conflict with canon or the standing rulings.

---

## Design points recorded with the build target (Jon, 4 Oct 2026), verbatim

Working title "Just Pythag It, Bruv" (Jon). Design (Jon, 4 Oct): every question starts by identifying the hypotenuse; the bank is weighted towards finding a shorter side (subtract); the two types are mixed unpredictably so students can't add by habit; the adding-instead-of-subtracting answer must appear as a distractor where options are shown.

## Addendum: scaled triples (Jon, 4 Oct 2026), verbatim

Addition (Jon, 4 Oct): Stage (a) includes scaled triples (e.g. 6-8-10, 9-12-15, 15-20-25, 30-40-50, 10-24-26). When a question is a 3-4-5 or 5-12-13 multiple, the feedback after answering names it: "Spotted it? 6, 8, 10 is the 3-4-5 triangle doubled. No calculation needed." (adjusted to the triple and scale). The full worked method is still shown. The verifier checks every triple-family message names the correct base triple and scale factor.

---

## Pre-flight notes for the build session (Code Claude, 4 Oct 2026; not rulings)

Checked while recording the contract, so the build session can settle them first. Each one touches a STOP IF.

1. **The level key "Foundation".** Point 2 says "key and label 'Foundation'". `MaffsLeaderboard.levelLabel()`
   (`schools/assets/firebase-leaderboard.js`) has no `foundation` key, and `scripts/check-leaderboard-coverage.js`
   fails any submitted level that `levelLabel()` cannot name. A new key would need a change to a shared component
   (STOP IF 1). Canon SR-11 already maps the existing key `ks3` to the label "Foundation", so key `ks3` with label
   "Foundation" would meet the design with no shared change. Jon to confirm before building.
2. **"A leaderboard for that length".** The resit strand's reference (`six-sevens-bruv`) keys its boards by
   length (`q20`, `q40`) and sends `level: 'all'` plus `mode` to analytics. Decide whether this game follows that
   pattern or keys its board by the level, and check that `levelLabel()` names whichever key is used.
3. **Adding a "Calculator" column to the roster.** `.claude/rules/game-roster.md` is parsed by regex in
   `scripts/check-theme.py` (`ROW`: slug, then the Levels column), `scripts/bank_common.py` (`roster_levels()`)
   and `scripts/check-leaderboard-coverage.js`. A new column added after the existing ones should leave those
   parsers reading the same cells. Check each, and run the full suite, before relying on that.
4. **"Unlisted" in CI.** `check-spec-mapping.py` takes live games from the portal's links, so an unlisted game
   should not be required on the spec map. `check-theme.py` fails a `games/` folder that is neither a roster game
   nor in `NOT_ROSTER`. Tier 1 discovers pages by walking the tree, so it will load the game, which is wanted.
   Check `check-leaderboard-coverage.js` ("every live game submits, or is declared") and `check-verifier-coverage.py`
   for how they define "live".
5. **Stages vs "≥60% shorter-side, no run of three".** Both hold across a whole session, but the stage order
   (a, b, c) still has to be met within them. Make sure the generator satisfies all three by construction (no
   redraw loop; CLAUDE.md tier 2 forbids rejection sampling).
6. **The addendum's "6, 8, 10" feedback** should name both the base triple and the scale factor (doubled,
   tripled, ×10 …). 10-24-26 is 5-12-13 doubled. 8-15-17 and 7-24-25 are not multiples of 3-4-5 or 5-12-13, so
   they get no "Spotted it?" line.
