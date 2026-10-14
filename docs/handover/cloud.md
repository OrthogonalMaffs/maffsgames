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
`cloud-remaining: `

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
TRUE-DISTRACTORS (14 Oct, contract now `docs/history/contracts/2026-10-14-true-distractors.md`): bv_core_019 DONE (#392); graph-sketcher CM8 DONE (this PR); classes (a) and (b) reported below for Jon.
**Standing authorisation (Jon, 10 Oct):** the cloud lane merges any PR of its own once its Gate is green and main's last full run is green, without asking each time; it still watches main's run after each merge. The 10 Oct queue (RIGHTFUL-KING, LIBRARY-JAM, FONT-FIT) is DONE and moved to `docs/history/handover-cloud-archive.md`, with Jon's rulings for the two room builds and FONT-FIT's known problems.

**Every PR:** `python scripts/check-changed.py` before the first push; merge only on a green Gate, and never while
main's last full run is red; watch main's run after merging.

## 2026-10-14 (cloud): TRUE-DISTRACTORS (contract now `docs/history/contracts/2026-10-14-true-distractors.md`)

- **better-value bv_core_019 DONE (#392, a3c1e75).** Every option names the day rate: the key "Contract A has the better day rate — £320/day vs £300/day"; distractors "£18,000 ÷ 12 = £1,500/day" (weeks taken for days) and "£18,000 ÷ 36 = £500/day" (A's days); "They pay the same daily rate" kept. The total-pay point (£18,000 vs £11,520, 60 days against 36) is in the explanation. Verifier REVIEW: the new verdict words, and £11,520 (12 × 3 × £320) allowed. Parity 20% / 0% -> 21% / 0%.
- **Class (a), better-value, for Jon** (every conclusion containing "better", 70 items; none fixed):
  - **True or defensible distractors, core_019's shape:** core_007 "Lease B is better if the business makes fewer than 1,000 copies" is true: B is £85 + 2p a copy, under £105 a month below 1,000 copies, against A's £120 (break-even 1,750); the scenario fixes 2,000, but the card is a true conditional. core_037 "Standard flyers are better value overall — they cost £80 less to print": on ROI (344% vs 331%) standard is the better value, and the key says "standard has the higher ROI"; the explanation's "The cheaper option is not the better value here" means net profit without saying so.
  - **Keys that are a judgement, not a computed measure:** core_047 (B "better value overall" at £135 vs £130, on "the homeowner values the longer-lasting clean"; its distractor "Cleaner A … saves £50 a year" is false only by its figure, £5); core_048 (A on cover; B's "£140 cheaper per year" is true); core_044 ("good, unless that money has a better use").
  - **"X is better because <true premise>"** (false only as "better" means least cost, and each key names a total or unit cost, so markable; for the distractor-falsity audit): gcse_002, 004, 014, 015, 017, 018; core_001, 002, 004, 010, 011, 017, 035.
  - No other distractor states a true fact with no verdict: the ten verdict-free ones (core_013, 015, 022 ×2, 023, 038 ×2, 046; gcse_010, 016) are each false as written.

- **graph-sketcher CM8 DONE.** The roots distractor "Times of maximum speed" was true (speed |15 − 10t| is greatest, 15 m/s, at t = 0 and t = 3, the roots); now "The time taken to reach maximum height" (1.5 s). Nothing else in CM8 changed; the verifier pins no option text there. Parity 6% / 2% -> 6% / 2% (CM8's key, 43 characters, sits between 21 and 54 before and after).
- **Class (b), every game, for Jon** (maximum/greatest/top speed or velocity wording, every roots question, every projectile item; none fixed):
  - **No other ground-to-ground projectile item offers the wording; no STOP IF hit.** graph-sketcher L4_7 (h = 30t − 4.9t², ground to ground) has no multiple-choice question (a turning point and a typed time of flight).
  - **Close wording, not a projectile:** graph-sketcher CM12 (fuel efficiency F against speed v), roots question, distractor "The speeds at which the car has maximum acceleration": false (the model says nothing of acceleration), but the same "maximum <rate>" shape.
  - **The phrase elsewhere, not a roots distractor:** core-maths-paper2c, the concave-up v–t question, "The car has reached its maximum speed": false (the gradient is still rising).
  - **Other projectile items checked, no such wording:** gradient-hunter gh_gcse_015 and gh_alevel_003 (chord interpretations, each distractor false), word-problem-decoder wpd_gcse_025 (topic identification), suvat (typed answers), trig-wars (no options).

## 2026-10-14 (cloud): MAIN-GREEN-AND-OPTION-PARITY (finished 14 Oct; full entry, with every game's rates and examples, in `docs/history/handover-cloud-archive.md`)

- All ten listed games pass both SR-34 limits (KNOWN starts empty), #377 to #386; the twelve option-parity worktrees and claude/pr374-merge stay (end-task.py cannot read PR state here).

## 2026-10-13 (cloud): SWEEP-1-RULINGS (finished 14 Oct; full entry in `docs/history/handover-cloud-archive.md`)

- Steps 0 to 3 merged, #361 to #371; 392 of 517 sweep entries closed, 125 open. SR-33 (rules R1 to R9) is for the home lane to carry into canon.
- Left for Jon (did not fit a rule): maths-court-s1-008, graph-sketcher-s1-006 and the rest of the list in the archived entry. bearing-blitz uses "Fire first." (the content document's wording), not Part A's "Fire before they do".
