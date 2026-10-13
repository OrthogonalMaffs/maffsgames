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
**SWEEP-1** (12 Oct, contract `docs/handover/contracts/2026-10-12-sweep-1.md`): one reading sweep of 96 live games (glorious-gantt skipped), 12 batches of 8 in lowest-level order; findings in each game's file, report `docs/audits/sweep-1-2026-10.md`. **Jon's rulings, 13 Oct** (verbatim: `docs/handover/contracts/2026-10-13-sweep-1-rulings.md`): word-problem-decoder and equation-builder fixed, not unlisted; **equation-builder must merge today, or say so and the home lane unlists it.** quadratic-factoriser DONE (#342, 3ab8cd5; Jon, 13 Oct: fixed, not unlisted). **From now on (Jon, 13 Oct):** a verifier that does not check worked steps or hints is a finding; report every typed answer that can be negative behind inputmode="decimal" (so far: log-laws, suvat; listed in the report's batch 6). Batches 1-5 DONE (#332, #336, #339, #340, #341); equation-builder DONE (#338). Batch 6 DONE (#343). **SR-30 (Jon, 13 Oct; the home lane records it in canon): a CRITICAL level whose fix a standing ruling decides is fixed the same day in its own PR, no unlist, reported to Jon after; stop and ask only for a new stem, context or convention, or if it cannot merge the same day.** circle-theorem-spotter DONE (#344, 091b4f0; batch 7's SR-20 hit, fixed under SR-30). Batch 7 DONE (#345). growth-and-decay DONE (#346, 3b2eb76). **Jon, 13 Oct, from now:** an 'Estimate' stem states a method (SR-12) or says 'use the model to estimate' (brief checks g, h). correlation-or-coincidence DONE (#347, f283457; batch 8's SR-20 hit, B22, B25, B27 replaced on Jon's ruling). **Batch 8: PR open on `claude/charming-dirac-z5eerm`.** Next: batch 9 (screening-room, estimation-engine, linear-equation-solver, stat-attack, core-maths-paper1, -paper2a, -paper2b, -paper2c). Reviewer brief: `docs/handover/contracts/2026-10-12-sweep-1-reviewer-brief.md`.
UC-FIX: DONE, #196 merged 9 Oct (c9fbf4b), main green.
SIM-S5: DONE, #203 merged 9 Oct (4081538). UC-T4-007: DONE, #205 merged 9 Oct (920c5b1; the answers' item 3c, in
`docs/history/contracts/2026-10-09-sim-s5-answers.md`; claim #204). FT-FIX: DONE, #207 merged 9 Oct (cf96929; contract, amendment and Jon's answers
of 9 Oct, 11:00, in `docs/history/contracts/2026-10-0[89]-ft-fix*.md`).
LISTED-HIGH: COMPLETE (contract, rulings and notes now in `docs/history/contracts/2026-10-09-listed-high*.md`):
#210-#212, #214, #216, #217, #219, #223, #225-#231 merged; main green (run 654, 37978742832). Item 12 closed on
Jon's ruling of 22:45 (option A): see the PD-CLOSE entry below. CAR-TRAP-DRAFT (moved from the home lane, Jon 20:17; contract on main,
`contracts/2026-10-09-car-trap-draft.md`): **Car Trap draft for Jon's review**, #235 merged (ba5b6b2); main green
(run 661). **CAR TRAP HAS MOVED ENTIRELY TO THE HOME LANE (Jon, 10 Oct), including #242 (CAR-TRAP-BUILD): the cloud
lane does not push to #242 or touch any car-trap file.** #242's state at hand-over is in its branch's
`docs/handover/cloud.md` (the CAR-TRAP-BUILD entry). It is red only on the teacher page at 320 px (§1.37). The new
art was not on main when Jon said it was: the only `car-trap-*.webp` there are the old pictures.
**QUEUE (Jon, 10 Oct), in order. Keep the handover current after each:**
Done 10 Oct: RIGHTFUL-KING-DRAFT (#247, aa660f7) and LIBRARY-DRAFT (#248, 8302ba8). Jon approved both drafts in
full ("spot on"); the Library room's title is The Library Jam.
1. **RIGHTFUL-KING-BUILD: DONE.** #257 merged 10 Oct (79165de); main's run 723 is green. The contract is now in
   `docs/history/contracts/`. Jon can play-test the room at `/escape-rooms/rightful-king/play.html`.
2. **LIBRARY-JAM-BUILD: DONE.** #262 merged 10 Oct (5f4f656); main's run 736 is green. The contract is now in
   `docs/history/contracts/`. Jon can play-test the room at `/escape-rooms/library-jam/play.html`. CI passed its
   teacher page under the §1.37 entry (recorded at 538 px, measured in the cloud container).
**Jon's ruling for both builds (10 Oct, after 13:45):**
- **The hub is left alone.** A built room sits behind its noindex holding page, and the checker counts a room as
  live only without `noindex`, so no card is needed. The star chip comes with the release contract.
- **Every lock gets a `grade` in room.js**, with a one-line reason in the PR, as #253 did.
- **The derived rating must be ★★★ (Rightful King) and ★ (Library Jam).** If honest grading gives anything else,
  STOP and report; never adjust a grade to fit.
- **Calibration from #253:** building powers to find the years (Prom's compound growth) is 5; a Venn overlap from
  totals is 4.
**Standing authorisation (Jon, 10 Oct):** the cloud lane merges any PR of its own once its Gate is green and main's
last full run is green, without asking each time. It still watches main's run after each merge.
**FONT-FIT: DONE.** #256 merged 10 Oct (a2dbdeb); main's run 720 is green. The contract is now
`docs/history/contracts/2026-10-10-font-fit.md`; the findings are in `docs/audits/font-fit-2026-10-10.md`.
- Free Daily Pizza and Negative Number Line both fit at 320x568 with **14 px** to spare (Next and Confirm at 514
  against 528), by layout only. Their verifiers assert `MARGIN = 8`.
- **Known problems, for Jon to order** (in the findings file; not fixed, not allowlisted):
  - Over the fold: standard-form-blitz +10, surd-simplifier +9, coordinate-geometry-dash +7, sequence-solver +4 and
    modular-battle +2 (320x568); estimation-golf +12 (390x844).
  - Too wide: distinctly-average, +14 px (its Aa toggle).
  - Within 5 px of the fold: proportion-blaster, prime-or-composite, higher-power, matrix-crunch, trig-worms and
    wrong-on-the-internet.
- **Lesson:** the cloud container's Chromium (1194) lays out 1 px differently from CI's (1243). parents/fractions
  measured 320 here and 321 in CI, so the allowlist keeps it at 321. **CI is the measure for a 1 px verdict.**
  Locally, Playwright 1.63 runs through scratch symlinks to build 1194 (`/opt/pw-browsers/*-1243`), with
  `FONTCONFIG_FILE` pinning DejaVu.
- **For the home lane:** CI's DejaVu pin step can now be retired for the phone checks (not removed: the workflow is
  home-lane).
Done: PP-T1-004 (#189; its contract is now in `docs/history/contracts/`).

**Every PR:** `python scripts/check-changed.py` before the first push; merge only on a green Gate, and never while
main's last full run is red; watch main's run after merging.

## 2026-10-13 (cloud): correlation-or-coincidence (#347) and SWEEP-1 batch 8 (GCSE part 4)

- **SR-20 hit, ruled the same day:** correlation-or-coincidence keyed "Something else causes both" on three pairs where one drives the other (B22, B25, B27). #347: Jon's three pairs (shoe size/reading age, ice creams/sunburn, umbrellas/taxis), the verifier bars the old pairs; the new ones overlap B4, B1 and B3 (s1-002, my error, for Jon).
- **Fixed in batch 8:** component-crusher L9's direction vector takes any non-zero multiple (SR-24), and AL11/L11 state their axes; formula-forge's A = πr² misconception; better-value's three true threshold options, the meal-prep reason, the van's resale and TPFT; given-that's two explanations; chart-interrogator's unlabelled boundaries and four-option Q1; expectation-station's k-cells ("2k = ?"), exact reveal and "Exactly half". Every verifier PASS locally with its plants; answer-lock PASS.
- **Open, for Jon:** better-value-s1-002 (equal at break-even, with r-006); chart-interrogator-s1-001 (histogram bands by axis, canon §7.1.2) and s1-005; expectation-station-s1-005 ("Most"); stem changes in unit-converter, formula-forge, given-that.
- **Class (running):** verifier gaps in worked text in every batch 8 game (each has an entry); conventions stated in one item and not its neighbours (component-crusher AL14 only).

## 2026-10-13 (cloud): circle-theorem-spotter (#344) and SWEEP-1 batch 7 (GCSE part 3)

- **SR-20 hit, fixed under SR-30 (Jon, 13 Oct):** circle-theorem-spotter's tangent figures marked the angle on the wrong side (6 of 55 HIGH). #344: T across AB from C, on B's side of OA; the verifier measures every tangent figure's SVG in Chromium; both old rules planted.
- **Fixed in batch 7:** probability-paradox SR-18 assumptions (Monty's random choice; "at random"/"fair" in five) and two true options (SR-16); coordinate-geometry-dash "∞"; graph-transformer's Show-steps captions and 1/x equations (every caption worked out from its target); formula-unlocked's raw-TeX target line and two misconception texts; scale-factor-scaling "Length scale factor", "Corresponding sides", "Similar solids". Every verifier PASS locally with its plants.
- **Open, for Jon:** SR-14: probability-paradox-s1-005 (plane crash, needs a new context) and bearing-blitz-s1-001 ("Fire or die."); the SR-23 timer class (surd-simplifier, circle-theorem-spotter, scale-factor-scaling, trig-identity-duel-t2-010); circle-theorem-spotter-s1-004 (Q50's numbers).
- **Class (running):** verifier gaps in worked feedback in every batch 7 game (each has an entry); raw TeX through textContent/innerHTML (formula-unlocked, proportion-blaster).

## 2026-10-13 (cloud): quadratic-factoriser (#342) and SWEEP-1 batch 6 (GCSE part 2)

- **SR-20 stop, ruled the same day:** quadratic-factoriser Higher keyed the wrong guided split on 3008 of 3760 items. #342: kps and kqr, step 5 kpx and ±kq; the verifier plays all six steps of every Higher item (3762 item-modes, about 60 s) and a self-test line plants the old split (about 80 s); the Formula roots are on MaffsKeypad with its minus key.
- **Fixed in batch 6:** proportion-blaster x > 0 (SR-17); standard-form-blitz ≈ 82's precision (SR-1, any approximate key) and the light-time inverse (SR-4); surd-simplifier's start screen; trig-wars SR-14 (Jon) and the briefing's 45° rule; trig-worms TOA error names when O > A. Every verifier PASS locally with its plants.
- **Open, for Jon:** modular-battle-s1-002 (SR-4 for a remainder drill); surd-simplifier-s1-003 (SR-23 timer); standard-form-blitz-s1-004 (calculator tag); trig-worms-s1-001 (θ arc); quadratic-factoriser-s1-003 (verifier gap).
- **Class for Jon (running):** no working after a wrong answer (proportion-blaster, standard-form-blitz, surd-simplifier, trig-identity-duel); negative typed answers behind inputmode="decimal" (log-laws, suvat), for a home-lane contract.
