# Handover: cloud lane

The cloud lane's running handover (canon §7.8.2). Only cloud-lane sessions edit this file; the home lane's is
`docs/handover/home.md`. Newest first. Keep it current on the branch as you go (CLAUDE.md, checkpoint discipline).

**Cloud lane owns:** per-game fixes in games that are currently unlisted, one game per PR, each with its verifier,
closing its entries in its own `docs/audits/findings/<slug>.yml`. It never edits `schools/assets/`, the shared
modules in `scripts/`, the workflow, canon, the roster's listed section, `docs/todo.md` or
`docs/audits/REGISTER.md` (CI regenerates that on main). Relisting a fixed game is the home lane's docs PR.

**Standing rule (Jon, 7 Oct 2026):** after each game's PR merges and main's full run is green, start the
next game on the contract's list without asking. Stop only for a STOP IF or an empty list.

**Remaining list (contract LH, 7 Oct 2026; added by the home lane, kept by the cloud lane):** it lives in
`scripts/answer-lock-state.json`, not in this file (contract ANSWER-LOCK-STATE, 19 Oct 2026); `scripts/check-answer-lock.py`
reads it. Take a game off it in the PR that finishes it. While a game is on it, a failure of that game in the check
is reported, not failed; off it, a failure fails CI.

**Lane rule, listed games (Jon, 8 Oct 2026; contract "listed-game CRITICAL/HIGH"; the home lane records it in
canon §7.8 in its next docs PR):** the cloud lane now also fixes listed games. Before starting one, add it to the
remaining list (`scripts/answer-lock-state.json`) and push that commit on its own, so the home lane's F1 batches skip it; take it off
in the PR that fixes it. One game claimed at a time; never claim a game already in an open home-lane F1 batch branch
(check `docs/handover/home.md` and the open PRs first; if it is, skip to the next and note it).

**Resume rule, MaffsLock (Jon, contract LH):** adopting MaffsLock includes the game's lock-hint declaration
(`<!-- maffs-lock-hint ... -->`, canon §7.6.0), and the game passes `check-answer-lock.py`. Hints live in the
game's page, never in the shared script.
A two-option game declares an `answer` that picks the option differing from its key for `i >= 1` (canon
§7.6.0, contract DET, 8 Oct; prime-or-composite is the pattern).

**Contracts (Jon, 8 Oct 2026, corrected 20:00):** each contract is saved verbatim as
`docs/handover/contracts/<yyyy-mm-dd>-<name>.md` in its claim commit (or the PR's first commit), with one line
in the queue below pointing to it. Read it when the item starts, not at session start (the folder stays out of the
start-up load). When the work merges, move the file to `docs/history/`.

**Queue** (finished contracts moved to `docs/history/handover-cloud-archive.md`, 19 Oct 2026): **SWEEP-1** (12 Oct, contract `docs/handover/contracts/2026-10-12-sweep-1.md`): one reading sweep of 96 live games (glorious-gantt skipped), 12 batches of 8 in lowest-level order; findings in each game's file, report `docs/audits/sweep-1-2026-10.md`. **Jon's rulings, 13 Oct** (verbatim: `docs/handover/contracts/2026-10-13-sweep-1-rulings.md`): word-problem-decoder and equation-builder fixed, not unlisted; **equation-builder must merge today, or say so and the home lane unlists it.** quadratic-factoriser DONE (#342, 3ab8cd5; Jon, 13 Oct: fixed, not unlisted). **From now on (Jon, 13 Oct):** a verifier that does not check worked steps or hints is a finding; report every typed answer that can be negative behind inputmode="decimal" (so far: log-laws, suvat; listed in the report's batch 6). Batches 1-5 DONE (#332, #336, #339, #340, #341); equation-builder DONE (#338). Batch 6 DONE (#343). **SR-30 (Jon, 13 Oct; the home lane records it in canon): a CRITICAL level whose fix a standing ruling decides is fixed the same day in its own PR, no unlist, reported to Jon after; stop and ask only for a new stem, context or convention, or if it cannot merge the same day.** circle-theorem-spotter DONE (#344, 091b4f0; batch 7's SR-20 hit, fixed under SR-30). Batch 7 DONE (#345). growth-and-decay DONE (#346, 3b2eb76). **Jon, 13 Oct, from now:** an 'Estimate' stem states a method (SR-12) or says 'use the model to estimate' (brief checks g, h). correlation-or-coincidence DONE (#347, f283457; batch 8's SR-20 hit, B22, B25, B27 replaced on Jon's ruling). Batch 8 DONE (#348, 186aa27). **Batch 9 (all eight reviewed) found two SR-20 levels, each fixed first under SR-30: core-maths-paper2a DONE (#349, 3989aed); stat-attack DONE (#350, 856aa7c). Batch 9 DONE (#351, 6c7c53e; Jon's rulings of 13 Oct and SR-31).** **Batch 10 (all eight reviewed; scratchpad `batch10-notes.txt`) found three SR-20 levels: growth-and-decay (PR open), test-the-claim (wt-tc), graph-sketcher; each its own PR under SR-30, then batch 10 (tax-theft on Jon's ruling).** Then batch 11 (curling-friction, force-resolver, moments-master, log-laws, binomial-blaster, partial-fractions-duel, proof-builder, dimension-checker). Reviewer brief: `docs/handover/contracts/2026-10-12-sweep-1-reviewer-brief.md`.
SWEEP-1-RULINGS (13 Oct, contract and Jon's two documents verbatim in `docs/handover/contracts/2026-10-13-sweep-1-rulings-2.md`): Jon approved the triage in full (20:35): standing rules R1-R9 (SR-33, below), 18 Part 2 rulings, Part 3 deferrals; R10 is the home lane's (contract LEVEL-LOGGED). Order: step 0 record, step 1 split bundled entries, step 2 R4 money check, step 3 per-game fixes (Year 6, KS3, Essentials at GCSE, other GCSE, Core, A-Level, L4), step 4 proportion-blaster-003 class count.
ESSENTIALS-SCREEN-TRUTH-2 (18 Oct, contract `docs/history/contracts/2026-10-18-essentials-screen-truth-2.md`): four listed Essentials games whose screens show something untrue or unreadable, one game per PR, each claimed on the remaining list first: 1 formula-plug-in DONE (#441); 2 new-shapes DONE (#442); 3 four-quadrant-explorer DONE (#443); 4 shape-shifter DONE (#445; Jon's ruling (a), 19 Oct); then (Jon, 19 Oct) 5 formula-plug-in and 6 new-shapes: header "Q{n} of {N} · {right} right". Rulings verbatim at the end of the contract file.
ROOM-CREDIT v2 (19 Oct, contract and v1 verbatim `docs/history/contracts/2026-10-19-room-credit.md`; Jon's lane exception plus his rating.js ruling): one optional room.js `credit`, drawn on the room and teacher pages, checked on the hub and front-page cards; four rooms credited. **DONE (#446, 9a94e78, merged 12:33 BST).**
PYTHAG-REPORT (19 Oct, contract `docs/history/contracts/2026-10-19-pythag-report.md`, research only): **DONE (#447)**; report `docs/handover/pythag-report.md`, for Jon's ruling on a "Formula only" mode. Then ruling (2) of 19 Oct: formula-plug-in DONE (#449, 531c988); new-shapes DONE (#450, e0377e9).
MONTY-CARD (19 Oct, contract `docs/history/contracts/2026-10-19-monty-card.md`; Jon's ruling on the phone gap at its end): the "100 Doors" card states its setup and condition; step 3 list in the entry below. **DONE (#448, b973e23).**
**START HERE (next session; written 19 Oct, 18:10 BST).**
- **Done since:** the new-shapes header DONE (#450, e0377e9; main run 39299844863, green); DEPS-SRC-HAZARD DONE (#451, 0dd1b68; main run 39309543642, green, 53 jobs); ANSWER-LOCK-STATE DONE (#452, b23fceb; main run 39315432381, green, 53 jobs); PYTHAG-KEY-COLLIDE DONE (#453, 54e0fe9; main run 39390699573, green, 53 jobs); MONTY-100-RETITLE DONE (#455, ed61533; main run 39398807202, green, 53 jobs).
- **In flight (23 Oct):** FOOTBALL-PITCHES (entry below). TAKE-A-WALK-LIST DONE (#504, ee7b1eb; listed, Resit Fluency Strand #100). TAKE-A-WALK-FRAME DONE (#499, e1004c0). TAKE-A-WALK-RANGES DONE (#497, 80eca0a). TAKE-A-WALK DONE (#495, ce1810e; merged unlisted, for Jon to play). CALC-BY-STAGE DONE (#494, 6c59e7a). HMP-LIST DONE (#493). HMP-FOUNDATION-STAGES DONE (#491, 9ac77ba; main run 39858937128 green, 62 jobs; still unlisted, for Jon to play). FDP-KEY-COLLIDE DONE (#485, merged and deployed 18:34 UK; first fully changed daily 23 Oct; claim released); FDP-SPREAD DONE (#481, main run 39783533845, green); K-PUNCTUATION-SCAN DONE (#483, main run 39787326200, green). HMP-CHOCOLATE DONE (#479, 0cf4494; main run 39771541559, green, 60 jobs; still unlisted). ANSWER-LOCK-STATIC DONE (#478, 66ae9f1; main run 39758707435, green). HOW-MANY-PARTS DONE (#469, merged unlisted; main run 39556536598, green); it waits on Jon's play-test (his list in its archived entry). TRIG-WORMS-FILTER DONE (#462, main run 39474891224, green); COLLISION-IDENTITIES DONE (#461). MONTY-CARD-2 DONE (#459, 223d498; main run 39411995366, green, 54 jobs). KEY-COLLISION-SURVEY DONE (#458, a3d431a; **STOPPED for Jon**: wrong methods marked right in seven listed games, see its entry). No game claimed (`scripts/answer-lock-state.json` is empty).
- **Main:** green after every merge on 19 Oct (53 jobs from #451, 59 from #469) (#445 39233921992, #446 39245413455, #447 39259197128, #448 39273656313, #449 39287568708, #450 39299844863, #451 39309543642, #452 39315432381, #453 39390699573, #454 39393567338, #455 39398807202, #457 39405865621, #458 39409216606 (attempt 1 red: three tier-1 page loads timed out in shard 4/4 on a docs-only merge; the one rerun green), #459 39411995366, #460 39414714196, #461 39472244834, #462 39474891224, #463 39478497493, #469 39556536598, #474 39625941008, #478 39758707435, #479 39771541559, #481 39783533845, #483 39787326200, #485 39823720730). **#456's run 39401811389 is red on the timings job alone** ("CI timings and pack (main only)"; 52 of 53 green): the median-of-5 pack failed `ci-groups.py --check` (content groups 1 and 2 at 80% and 82% of 270 s) because this run's setup was 87 s (recorded setups 20, 19, 53, 27, 59: median 27 would become 53); nothing was written (both lines since split by PER-LINE-LIMIT, #465). **#472's run 39559284220 is red on the timings job alone:** four unchanged lines over PER-LINE-LIMIT's line limit on a setup median of 57 s; LINE-LIMIT-SCOPE (below) is the fix. #473's run 39562229614 green, pack committed.
- **With the home lane (Jon, 20 Oct; the cloud lane takes no action):** the roster's "15 triples" for Just Pythag It, Bruv (code: 14), contract ROSTER-PYTHAG-14. **Home lane: `scripts/ci-groups.py` changed in LINE-LIMIT-SCOPE (below); rebase knowingly.**
- **Waiting on Jon (no contract yet):** (1) the front page's compact mode hides every fact card's summary on phones (600 px and below, no toggle), so the new MONTY-CARD setup is unseen there: a layout contract; (2) card 2 "The Monty Hall Problem" has the same unstated setup as the 100 Doors card had (full list of cards with unstated setup in the MONTY-CARD entry); (3) PYTHAG-REPORT's findings, for his "Formula only" ruling (the 15-triples roster line is now the home lane's, above); (4) the phone stacking of the two headers was this lane's layout choice (one line overflowed 320 px), to confirm. **Ruled, Jon, 20 Oct:** PYTHAG-KEY-COLLIDE's filter-each-pool-once is correct under §12 and SR-5 (his "reject and redraw" was wrong); the roster's "15 triples" for Just Pythag It, Bruv (the code has 14) is left for the home lane.
- **Container setup (every fresh session):** `pip install playwright==1.56.0 sympy mpmath pyyaml`; `pip download --no-deps esprima==4.0.1`, untar into the scratchpad, `PYTHONPATH=<that>/esprima-4.0.1 python scripts/check-changed.py`. A run takes about 70 minutes and reports the same 25 KaTeX-CDN/WebKit failures every time (by name: the set in #441's PR); run one at a time, in the background; verifiers in scratch worktrees can run beside it (free ports). Remote branches are deleted on merge: after a squash merge, `git checkout -B claude/brave-allen-reghhq origin/main` and push without `--force-with-lease`.

**Standing authorisation (Jon, 10 Oct):** the cloud lane merges any PR of its own once its Gate is green and main's last full run is green, without asking each time; it still watches main's run after each merge. The 10 Oct queue (RIGHTFUL-KING, LIBRARY-JAM, FONT-FIT) is DONE and moved to `docs/history/handover-cloud-archive.md`, with Jon's rulings for the two room builds and FONT-FIT's known problems.
**Holds and self-scheduled tasks (Jon, 16 Oct 2026):** a hold the cloud lane states on a PR is released only by Jon. Stating a hold cancels, or rewrites to report-only, any pending task this lane scheduled for that PR. A task this lane schedules for itself carries no authority beyond the standing rules at the time it fires, and its report names it as the lane's own follow-up, not a request. Self-scheduled tasks may read CI status and report; they never merge, push or edit while a hold stands. (Contract GS-L4-5-ENDPOINT; canon §7.8 records it via the home lane.)

**Every PR:** `python scripts/check-changed.py` before the first push; merge only via `python scripts/merge-pr.py <n>`
(needs a green Gate and main, §7.8.3); watch main's run after.

## 2026-10-23 (cloud): FOOTBALL-PITCHES (contract verbatim: `docs/history/contracts/2026-10-23-football-pitches.md`). **IN FLIGHT** (branch `claude/exciting-darwin-r08162`).

- **Lane exception (Jon, 23 Oct 2026, 23:05):** the cloud lane builds the game and edits what a new unlisted game needs, for this PR only: the roster's Unlisted row 101 (`by stage`), `data/games.json`, the `NOT_ON_HUB` entry, the game lists in check-levels, check-answer-lock, check-theme, check-teacher-invite, check-start-mount and audit-register, and one label `stage-5` -> "Stage 5" in `firebase-leaderboard.js` (nothing else there).
- **The game** `games/squared-squirrel/` (noindex, UNLISTED): Football Pitches per Squared Squirrel. Five stages, boards `stage-1`..`stage-5`; calculator `not allowed` in 1-3, `scientific` in 4-5. **Pools:** Stage 1 the fixed ramp of 10 (exempt from 40, Jon's ruling); Stage 2 169; Stage 3 338; Stage 4 202; Stage 5 148. One nonsense-unit question in every session of 10.
- **Answers:** typed, the unit from buttons (the units in play, shuffled); the unit picker is the game's own (Take a Walk's pattern), MaffsAnswer marks the number, so the "no unit" state needed no shared change. Stage 1 questions 1-3: a wrong first try logs `correct:false` once and is tried again; the right retry scores. The lock check plays Stage 2 (its hint says why).
- **Verifier** `scripts/verify-squared-squirrel.py`, three parts (local 1: ~5 s, 2: ~85 s, 3: ~90 s): keys by units and dimensions from each question's data, slips, friendly numbers, the ramp, the measure, no formula-triangle wording or drawing, play at 1280 and 320. Seven plants, each caught.
- **Main run before this (#505's merge, 6c04fd3):** run 40029693478 was cancelled at its 16-minute limit: Index Laws stalled for 7.5 min (median 57 s) on unchanged code on a runner slow at every step (container start 181 s, normally 24 s). One re-run of the failed jobs: green, 57 of 57.

## 2026-10-23 (cloud): TAKE-A-WALK-LIST (contract in Jon's message of 23 Oct, 20:00). **DONE (#504, ee7b1eb; main run 40026650364 green, 57 of 57 jobs).** Live pages not checked from here (the network policy denies maffsgames.co.uk); Project Claude checks them.

- **Lane exceptions (Jon, 23 Oct 2026):** 20:00, the home-lane files the contract names, for this PR; 20:33, the four board labels `stage-1`..`stage-4` -> "Stage 1".."Stage 4" in `schools/assets/firebase-leaderboard.js` (LEVEL_NAMES) and nothing else there. The first try STOPPED on the coverage check ("levelLabel() cannot name"); unlisted games skip it, so #495 never met it.
- **Listed:** noindex removed; portal cards in KS3 and GCSE after How Many Parts? (135 -> 137 cards, 97 -> 98 games, recounted); Essentials, Geometry and measures, `data-kind="one"` (a stage picker, no level control; SUITE updated); sitemap; spec map G16 only; hub row `stage-1`..`-4`; `NOT_ON_HUB` entry replaced by a `LEVEL_OVERRIDES` entry; roster row 100 to the Resit Fluency Strand with the verifier's pools (181, 550, 152, 150); 98 in CLAUDE.md and canon; /updates/ line. `verify-take-a-walk.py`'s static check now fails if the page IS noindex (HMP-LIST's flip).
- **ANSWER-COUNTS (home lane, #503) merged first:** #504 merged main in; only `docs/handover/home.md` conflicted (both entries kept).

## 2026-10-23 (cloud): TAKE-A-WALK-FRAME (#499; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-23 (cloud): TAKE-A-WALK-RANGES (#497; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-23 (cloud): TAKE-A-WALK (#495; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-23 (cloud): CALC-BY-STAGE (#494; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-23 (cloud): HMP-LIST (#493; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-22 (cloud): HMP-FOUNDATION-STAGES (#491; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-22 (cloud): FDP-KEY-COLLIDE (#485; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-22 (cloud): K-PUNCTUATION-SCAN (#483; full entry in `docs/history/handover-cloud-archive.md`; report `docs/audits/k-punctuation-scan-2026-10.md`)

## 2026-10-22 (cloud): COMIC-CAPER-BRIEFS (#482; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-22 (cloud): FDP-SPREAD (#481; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-22 (cloud): COMIC-CAPER-LOCKS (#480; full entry in `docs/history/handover-cloud-archive.md`; report `docs/audits/comic-caper-locks-2026-10-22.md`)

## 2026-10-21 (cloud): HMP-CHOCOLATE (#479; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-22 (cloud): ANSWER-LOCK-STATIC (#478; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-21 (cloud): LINE-LIMIT-SCOPE (#474; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-20 (cloud): HOW-MANY-PARTS (#469; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-20 (cloud): TRIG-WORMS-FILTER (#462; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-20 (cloud): COLLISION-IDENTITIES (#461; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-20 (cloud): MONTY-CARD-2 (#459; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-20 (cloud): KEY-COLLISION-SURVEY (#458; full entry in `docs/history/handover-cloud-archive.md`; report `docs/audits/key-collision-survey-2026-10.md`)

## 2026-10-20 (cloud): MONTY-100-RETITLE (#455; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-20 (cloud): PYTHAG-KEY-COLLIDE (#453; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-19 (cloud): ANSWER-LOCK-STATE (#452; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-19 (cloud): DEPS-SRC-HAZARD (#451; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-19 (cloud): HEADER "Q{n} of {N} · {right} right" (#449, #450; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-19 (cloud): MONTY-CARD (#448; full entry, with the cards that rely on unstated setup, in `docs/history/handover-cloud-archive.md`)

## 2026-10-19 (cloud): PYTHAG-REPORT (#447; full entry in `docs/history/handover-cloud-archive.md`; report `docs/handover/pythag-report.md`)

## 2026-10-19 (cloud): ROOM-CREDIT v2 (#446; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-18 (cloud): ESSENTIALS-SCREEN-TRUTH-2 (#441-#445; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-18 (cloud): ESSENTIALS-FALSE-TEXT 3/4 new-shapes (#437; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-18 (cloud): RAW-TEX-LAST-2 (#435, #436; full entry in `docs/history/handover-cloud-archive.md`)

Older entries (17 Oct and before): `docs/history/handover-cloud-archive.md`.
