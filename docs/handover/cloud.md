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
- **In flight (22 Oct):** FDP-KEY-COLLIDE (entry below; its PR releases the free-daily-pizza claim; merged near midnight UK); FDP-SPREAD DONE (#481, main run 39783533845, green); K-PUNCTUATION-SCAN DONE (#483, main run 39787326200, green). HMP-CHOCOLATE DONE (#479, 0cf4494; main run 39771541559, green, 60 jobs; still unlisted). ANSWER-LOCK-STATIC DONE (#478, 66ae9f1; main run 39758707435, green). HOW-MANY-PARTS DONE (#469, merged unlisted; main run 39556536598, green); it waits on Jon's play-test (his list in its archived entry). TRIG-WORMS-FILTER DONE (#462, main run 39474891224, green); COLLISION-IDENTITIES DONE (#461). MONTY-CARD-2 DONE (#459, 223d498; main run 39411995366, green, 54 jobs). KEY-COLLISION-SURVEY DONE (#458, a3d431a; **STOPPED for Jon**: wrong methods marked right in seven listed games, see its entry). No game claimed (`scripts/answer-lock-state.json` is empty).
- **Main:** green after every merge on 19 Oct (53 jobs from #451, 59 from #469) (#445 39233921992, #446 39245413455, #447 39259197128, #448 39273656313, #449 39287568708, #450 39299844863, #451 39309543642, #452 39315432381, #453 39390699573, #454 39393567338, #455 39398807202, #457 39405865621, #458 39409216606 (attempt 1 red: three tier-1 page loads timed out in shard 4/4 on a docs-only merge; the one rerun green), #459 39411995366, #460 39414714196, #461 39472244834, #462 39474891224, #463 39478497493, #469 39556536598, #474 39625941008, #478 39758707435, #479 39771541559, #481 39783533845, #483 39787326200). **#456's run 39401811389 is red on the timings job alone** ("CI timings and pack (main only)"; 52 of 53 green): the median-of-5 pack failed `ci-groups.py --check` (content groups 1 and 2 at 80% and 82% of 270 s) because this run's setup was 87 s (recorded setups 20, 19, 53, 27, 59: median 27 would become 53); nothing was written (both lines since split by PER-LINE-LIMIT, #465). **#472's run 39559284220 is red on the timings job alone:** four unchanged lines over PER-LINE-LIMIT's line limit on a setup median of 57 s; LINE-LIMIT-SCOPE (below) is the fix. #473's run 39562229614 green, pack committed.
- **With the home lane (Jon, 20 Oct; the cloud lane takes no action):** the roster's "15 triples" for Just Pythag It, Bruv (code: 14), contract ROSTER-PYTHAG-14. **Home lane: `scripts/ci-groups.py` changed in LINE-LIMIT-SCOPE (below); rebase knowingly.**
- **Waiting on Jon (no contract yet):** (1) the front page's compact mode hides every fact card's summary on phones (600 px and below, no toggle), so the new MONTY-CARD setup is unseen there: a layout contract; (2) card 2 "The Monty Hall Problem" has the same unstated setup as the 100 Doors card had (full list of cards with unstated setup in the MONTY-CARD entry); (3) PYTHAG-REPORT's findings, for his "Formula only" ruling (the 15-triples roster line is now the home lane's, above); (4) the phone stacking of the two headers was this lane's layout choice (one line overflowed 320 px), to confirm. **Ruled, Jon, 20 Oct:** PYTHAG-KEY-COLLIDE's filter-each-pool-once is correct under §12 and SR-5 (his "reject and redraw" was wrong); the roster's "15 triples" for Just Pythag It, Bruv (the code has 14) is left for the home lane.
- **Container setup (every fresh session):** `pip install playwright==1.56.0 sympy mpmath pyyaml`; `pip download --no-deps esprima==4.0.1`, untar into the scratchpad, `PYTHONPATH=<that>/esprima-4.0.1 python scripts/check-changed.py`. A run takes about 70 minutes and reports the same 25 KaTeX-CDN/WebKit failures every time (by name: the set in #441's PR); run one at a time, in the background; verifiers in scratch worktrees can run beside it (free ports). Remote branches are deleted on merge: after a squash merge, `git checkout -B claude/brave-allen-reghhq origin/main` and push without `--force-with-lease`.

**Standing authorisation (Jon, 10 Oct):** the cloud lane merges any PR of its own once its Gate is green and main's last full run is green, without asking each time; it still watches main's run after each merge. The 10 Oct queue (RIGHTFUL-KING, LIBRARY-JAM, FONT-FIT) is DONE and moved to `docs/history/handover-cloud-archive.md`, with Jon's rulings for the two room builds and FONT-FIT's known problems.
**Holds and self-scheduled tasks (Jon, 16 Oct 2026):** a hold the cloud lane states on a PR is released only by Jon. Stating a hold cancels, or rewrites to report-only, any pending task this lane scheduled for that PR. A task this lane schedules for itself carries no authority beyond the standing rules at the time it fires, and its report names it as the lane's own follow-up, not a request. Self-scheduled tasks may read CI status and report; they never merge, push or edit while a hold stands. (Contract GS-L4-5-ENDPOINT; canon §7.8 records it via the home lane.)

**Every PR:** `python scripts/check-changed.py` before the first push; merge only via `python scripts/merge-pr.py <n>`
(needs a green Gate and main, §7.8.3); watch main's run after.

## 2026-10-22 (cloud): FDP-KEY-COLLIDE (contract verbatim: `docs/history/contracts/2026-10-22-fdp-key-collide.md`; Jon's rulings that put FDP-SPREAD first: `docs/history/contracts/2026-10-22-fdp-spread.md`). **This PR; merged near midnight UK.**

- **Done:** one pass after the bank is built (`FDP.keyIsSlip`, as #453) removes every question where subtracting the percentage, or the percentage number put on the bottom, gives the key: stage 1 loses 1 of 90 (10% as a fraction, `S1:conv:p>f:1/10`), stage 3 1 of 138 (60% of 150, `S3:pct:60:150`), stages 2 and 4 none. No redraw (canon §12, SR-5).
- **Verifier (part 1):** the removed set recomputed from the parameters; every served item checked for both slips; the unfiltered bank planted and caught. Survey: free-daily-pizza coincidence 2 -> **0** (its 80 "methods agree" rows are the survey's accepted identity class; its entry needed no change).
- **The daily pizza changes on every date** from the deploy: the draw takes from one shuffled list per stage, so two fewer items move every later pick (30 of the next 30 dates differ). Merged near midnight UK on Jon's ruling; the first changed date is recorded below once main's run is in.
- **Claim released** (`scripts/answer-lock-state.json` empty).

## 2026-10-22 (cloud): K-PUNCTUATION-SCAN (report only; contract verbatim: `docs/history/contracts/2026-10-22-k-punctuation-scan.md`). **DONE (#483, 1d34ac0; main run 39787326200 green, 54 jobs).**

- **Report:** `docs/audits/k-punctuation-scan-2026-10.md`; script `scripts/scan-k-punctuation.py` (not in CI; `--selftest` plants the fault and its glued control; `--static-only` lists the source joins).
- **Headline:** 38 games render their own KaTeX (the home lane counted 36 on 21 Oct). **3 affected**, each in one place, none in a stem or an option: expectation-station (Worked Example "Prize (", 320 px), growth-and-decay (Worked Example ". " after t = 0, 390 px), how-many-parts (wrong-answer line brackets, 320 px). 34 clean; glorious-gantt not walkable (calls no KaTeX). Under 10, so no STOP.
- **Swap:** no game's K() swaps for MaffsText.html directly (bare TeX in, prose built round it); how-many-parts' renderLine is the nearest (its `§` format). The class is the Worked Example block (`renderMethodRef`, copied into eight games): its root fix is one renderer for that block, Jon's design call.
- **Not reached:** simultaneous-solver at A-level and glorious-gantt (driver cannot play them); truth-will-set-you-free's two joins (:871, :874).

## 2026-10-22 (cloud): COMIC-CAPER-BRIEFS (contract from Jon, 22 Oct, after the report): lock 1 and lock 3 briefs reworded to Jon's exact wording in `escape-rooms/comic-caper/room.js`; nothing else in the room changed. New `scripts/verify-comic-caper.py` (own ci-line; selected by room.js) pins both as rendered at 320/390/1280 px, inside the panel, no sideways scroll; each old brief and a one-line overflow planted and caught. The report's lock script rerun on the new room: 184/184 draws won, 118/118 forced entries open, 6/6 saved states. **In flight: #482** (main run to record after merge). Excluded, home lane's (the report's shared findings): teacher page set 1, dial ticks, lock-1 dial below the fold on phones, the room check reading stored data.

## 2026-10-22 (cloud): FDP-SPREAD (#481; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-22 (cloud): COMIC-CAPER-LOCKS (report only): **all locks open** on the answer worked from the rendered clues, every set of all three locks (4/9/10), typed, slider and dial, desktop and phone, all 184 fresh draws won; no stale save splits clues from answer. Report and observations for Jon: `docs/audits/comic-caper-locks-2026-10-22.md`; **DONE (#480, 254c946; main run 39781113679, green).**

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
