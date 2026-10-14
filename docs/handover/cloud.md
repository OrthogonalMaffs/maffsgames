# Handover: cloud lane

The cloud lane's running handover (canon §7.8.2). Only cloud-lane sessions edit this file; the home lane's is
`docs/handover/home.md`. Newest first. Keep it current on the branch as you go (CLAUDE.md, checkpoint discipline).

**Cloud lane owns:** per-game fixes in games that are currently unlisted, one game per PR, each with its verifier,
closing its entries in its own `docs/audits/findings/<slug>.yml`. It never edits `schools/assets/`, the shared
modules in `scripts/`, the workflow, canon, the roster's listed section, `docs/todo.md` or
`docs/audits/REGISTER.md` (CI regenerates that on main). Relisting a fixed game is the home lane's docs PR.

**Standing rule (Jon, 7 Oct 2026):** after each game's PR merges and main's full run is green, start the
next game on the contract's list without asking. Stop only for a STOP IF or an empty list.

**Remaining list (contract LH, 7 Oct 2026; added by the home lane, kept by the cloud lane):** take a game off
this line in the PR that finishes it. `scripts/check-answer-lock.py` reads it. While a game is on it, a
failure of that game in the check is reported, not failed; off it, a failure fails CI.
`cloud-remaining: wrong-on-the-internet`

**Lane rule, listed games (Jon, 8 Oct 2026; contract "listed-game CRITICAL/HIGH"; the home lane records it in
canon §7.8 in its next docs PR):** the cloud lane now also fixes listed games. Before starting one, add it to the
remaining list above and push that handover commit on its own, so the home lane's F1 batches skip it; take it off
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

**Queue:** VERIFIERS-20 (12 Oct, contract now `docs/history/contracts/2026-10-12-verifiers-20.md`): 20 verifiers, one game per PR; 1 prime-or-composite DONE (#282); 2 fraction-equivalence DONE (#283); 3 percentage-flip DONE (#284); 4 factor-race DONE (#285); 5 prime-factorisation DONE (#286); 6 think-of-a-number DONE (#287); 7 formula-plug-in DONE (#290); 8 four-quadrant-explorer DONE (#291); 9 new-shapes DONE (#292); 10 shape-shifter DONE (#293); 11 equatle DONE (#294); 12 standard-form-blitz DONE (#295); 13 index-laws DONE (#296, ruling #297); 14 modular-battle DONE (#298); 15 bearing-blitz DONE (#300); 16 constructions-lab DONE (#301); between games: wrong-on-the-internet t2-006 (Jon's SR-14 ruling) DONE (#304, 73478d6), closes t2-006; modular-battle verifier flake fixed (#303); 17 formula-forge DONE (#305); 18 characteristic-quest DONE (#306); 19 eigenvalue-extractor DONE (#307); 20 prisoners-dilemma DONE (#309). **VERIFIERS-20 COMPLETE.** Then: formula-forge-v20-001 (Jon's ruling, 12 Oct) DONE (#310, 8d36ca2).
B11-CLEAR (12 Oct, contract now `docs/history/contracts/2026-10-12-b11-clear.md`): clear B11 from the ledger, one game per PR: 1 scale-factor-scaling DONE (#312, 031d8ed); 2 coordinate-geometry-dash DONE (#315); 3 index-laws DONE (#320, 588a903); 4 standard-form-blitz DONE (#324, cb0751b); 5 surd-simplifier DONE (#328, 6d40d5a); 6 boolean-blitz DONE (#330, c5ef4b0); 7 complex-converter DONE (#331). **B11-CLEAR COMPLETE: the ledger holds no B11 entry.**
**SWEEP-1** (12 Oct, contract `docs/handover/contracts/2026-10-12-sweep-1.md`): one reading sweep of 96 live games (glorious-gantt skipped), 12 batches of 8 in lowest-level order; findings in each game's file, report `docs/audits/sweep-1-2026-10.md`. **Jon's rulings, 13 Oct** (verbatim: `docs/handover/contracts/2026-10-13-sweep-1-rulings.md`): word-problem-decoder and equation-builder fixed, not unlisted; **equation-builder must merge today, or say so and the home lane unlists it.** quadratic-factoriser DONE (#342, 3ab8cd5; Jon, 13 Oct: fixed, not unlisted). **From now on (Jon, 13 Oct):** a verifier that does not check worked steps or hints is a finding; report every typed answer that can be negative behind inputmode="decimal" (so far: log-laws, suvat; listed in the report's batch 6). Batches 1-5 DONE (#332, #336, #339, #340, #341); equation-builder DONE (#338). Batch 6 DONE (#343). **SR-30 (Jon, 13 Oct; the home lane records it in canon): a CRITICAL level whose fix a standing ruling decides is fixed the same day in its own PR, no unlist, reported to Jon after; stop and ask only for a new stem, context or convention, or if it cannot merge the same day.** circle-theorem-spotter DONE (#344, 091b4f0; batch 7's SR-20 hit, fixed under SR-30). Batch 7 DONE (#345). growth-and-decay DONE (#346, 3b2eb76). **Jon, 13 Oct, from now:** an 'Estimate' stem states a method (SR-12) or says 'use the model to estimate' (brief checks g, h). correlation-or-coincidence DONE (#347, f283457; batch 8's SR-20 hit, B22, B25, B27 replaced on Jon's ruling). Batch 8 DONE (#348, 186aa27). **Batch 9 (all eight reviewed) found two SR-20 levels, each fixed first under SR-30: core-maths-paper2a DONE (#349, 3989aed); stat-attack DONE (#350, 856aa7c). Batch 9 DONE (#351, 6c7c53e; Jon's rulings of 13 Oct and SR-31).** **Batch 10 (all eight reviewed; scratchpad `batch10-notes.txt`) found three SR-20 levels: growth-and-decay (PR open), test-the-claim (wt-tc), graph-sketcher; each its own PR under SR-30, then batch 10 (tax-theft on Jon's ruling).** Then batch 11 (curling-friction, force-resolver, moments-master, log-laws, binomial-blaster, partial-fractions-duel, proof-builder, dimension-checker). Reviewer brief: `docs/handover/contracts/2026-10-12-sweep-1-reviewer-brief.md`.
SWEEP-1-RULINGS (13 Oct, contract and Jon's two documents verbatim in `docs/handover/contracts/2026-10-13-sweep-1-rulings-2.md`): Jon approved the triage in full (20:35): standing rules R1-R9 (SR-33, below), 18 Part 2 rulings, Part 3 deferrals; R10 is the home lane's (contract LEVEL-LOGGED). Order: step 0 record, step 1 split bundled entries, step 2 R4 money check, step 3 per-game fixes (Year 6, KS3, Essentials at GCSE, other GCSE, Core, A-Level, L4), step 4 proportion-blaster-003 class count.
**Standing authorisation (Jon, 10 Oct):** the cloud lane merges any PR of its own once its Gate is green and main's last full run is green, without asking each time; it still watches main's run after each merge. The 10 Oct queue (RIGHTFUL-KING, LIBRARY-JAM, FONT-FIT) is DONE and moved to `docs/history/handover-cloud-archive.md`, with Jon's rulings for the two room builds and FONT-FIT's known problems.

**Every PR:** `python scripts/check-changed.py` before the first push; merge only on a green Gate, and never while
main's last full run is red; watch main's run after merging.

## 2026-10-14 (cloud): MAIN-GREEN-AND-OPTION-PARITY (contract `docs/handover/contracts/2026-10-14-main-green-and-option-parity.md`)

- **Part 1, verify-probability-paradox.py, measured here (one local machine, serial):** before #371 (56e4ece^) 178 s; main (e057694) 231 s; fixed 74 s. Cause: #371 added four plants to the self-test, each re-running the whole `run()`, and `next_once` (real MaffsLock timers) costs 10 s of its 13.6 s. It raises only `t1-010` failures, so it now runs for the real page and the t1-010 plant, not the other 15. Not the simulation (0.2 s). All 16 plants still caught; no check dropped; no budget, workflow or ci-groups change.

## 2026-10-13 (cloud): SWEEP-1-RULINGS (finished 14 Oct; full entry in `docs/history/handover-cloud-archive.md`)

- Steps 0 to 3 merged, #361 to #371; 392 of 517 sweep entries closed, 125 open. SR-33 (rules R1 to R9) is for the home lane to carry into canon.
- Left for Jon (did not fit a rule): maths-court-s1-008, graph-sketcher-s1-006 and the rest of the list in the archived entry. bearing-blitz uses "Fire first." (the content document's wording), not Part A's "Fire before they do".

## 2026-10-13 (cloud): NEGATIVE-INPUT (log-laws, suvat; Jon's input-design ruling)

- **Ruling (Jon, 13 Oct):** mount `schools/assets/keypad.js` with `keys: {minus: true}` in every game where a negative typed answer is possible, as the 11 games that already use it do; the changed touch layout is accepted; keypad.js untouched; games with no possible negative keep their input; whether all typed-numeric games should move is a separate, later question. **Pattern copied: quadratic-factoriser's Formula level** (roots can be negative; calculator.css linked, the surface/font tokens declared on `:root`, a holder div inside the locked container, `MaffsKeypad.mount` with `keys: {minus: true}`).
- **Changed (for the home lane's check):**
  - `log-laws`: Solve mode's `#solveInput` (34 negative typed answers, log-laws-s1-005). Mounted once at page load; the keys sit inside `#solveBox`, so `MaffsLock.lock` and `fresh` switch them with the box (no keys code of its own).
  - `suvat`: Phase 2's `#calcInput` (ALEVEL[34] step 0, v_y = -0.32, suvat-s1-001) and Phase 0's `#p0ux`/`#p0uy`. No Phase 0 key in the bank is negative; it is mounted too so one game does not mix two input styles (Jon can reverse that).
  - Tested on a 390 px touch profile: real taps on minus, 3, point, 5 type `-3.5` into each; with a mouse the boxes are ordinary inputs, no keypad.
- **Judged to have no negative answer (input unchanged):**
  - `split-it`: every generator draws positive integers and builds positive answers (ratios in lowest terms, shares `a*k`, scaled recipe amounts, unit prices, money); nothing subtracts. Money boxes are `type="text" inputmode="decimal"`, the rest `type="number"`.
  - `screening-room`: the answer is `tp / (tp + fp)` from non-negative counts, a percentage from 0 to 100 (`buildItem`); no bank answer is negative (280 items).
  - `fermi-lab`: all 325 items' chain references, `acceptedAnswer`s and the figures table (`value:`) are positive estimates (smallest 2e-10); no negative anywhere in the data.
  - `just-pythag-it-bruv`: side lengths; it already loads keypad.js through MaffsCalc.
  - Already had a minus key: `simultaneous-solver`.
- **Not settled by the code, for Jon:** none of the six candidates. **Not built:** the contract's `scripts/check-negative-input.py`. The ruling calls it the home lane's check, and the extracted banks cannot be its evidence: split-it and just-pythag-it-bruv are generators, log-laws' Solve answers are generated at run time, and suvat's negative sits in `steps[].answer`, not a top-level answer field (a check must walk nested fields and carry a declared list for generators).
- **Merged:** #360 (cf976e7), CI green on re-run (three page-load timeouts in other games on the first attempt: screening-room, proof-builder, quadratic-factoriser); log-laws-s1-005 and suvat-s1-001 closed. Main's run for the merge: see the next entry.
