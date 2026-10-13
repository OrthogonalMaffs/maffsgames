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

## 2026-10-13 (cloud): SWEEP-1-RULINGS (started; step 0)

- **SR-33 (Jon, 13 Oct 2026; for the home lane to carry into canon): the standing rules R1 to R9, as written in Part 1 of `docs/handover/contracts/2026-10-13-sweep-1-rulings-2.md`.** R1 wording, plurals, British usage and notation are fixed without asking when no key, context or convention changes. R2 a convention a key rests on is stated in the stem or start screen (SR-17 library-wide), key unchanged. R3 on-screen text that is false or contradicts the game is corrected to the nearest true wording; never a key (that comes to Jon). R4 money is shown to the penny from unrounded values (`toFixed(2)`), with a check over the extracted banks. R5 a true distractor is replaced by a named error (SR-4). R6 SR-14 content is removed. R7 a Hidden Count-Up game hides its running Time from the HUD (characteristic-quest joins that list). R8 rendering bugs (raw TeX, prose-mode maths, drawings off the canvas) are fixed without asking. R9 marking follows canon (§7.1.2 bands, SR-24 every valid order, the "actually TRUE" option on every counter-example item). R10 (logged level = resolved level) is the home lane's.
- **Where the two documents differ:** Part A's R6 says bearing-blitz "Fire or die" becomes "Fire before they do"; Part B (the drafted wording) says "Fire first." The contract says the content document's exact wording is used, so "Fire first." is applied. Reported here, not rewritten.
- **Step 1 done (docs-only PR):** 50 of the 179 open judgement entries held faults of different kinds and are now 169 entries (119 new, ids continue each game's s1 numbering; the first part keeps the parent's id, so every id the triage cites still means its main defect). **My definition of "defect"** (the contract does not give one): one fault of one kind, its instances together ("ten stems write an approximately-equals sign" stays one entry); different kinds, or the same item with two different faults, are separate entries, each with its own severity. Reading every instance as its own entry would have made about 450. Reported so Jon can overrule; the reviewer brief now says one defect per entry. Wrong maths no longer hides at LOW: fermi-lab-s1-003 is now HIGH (wrong key, 140 against a chain of 82) with its wording fault split off; maths-court's gcse_015 arithmetic, higher-power's al_30 and al_36 statements and the core_003 conclusion are MEDIUM. Also: new-shapes-s1-001 raised to HIGH and prime-factorisation-s1-001 to MEDIUM (Part 2 #1, #2); core-maths-paper1-s1-006's stale half (the histogram ticks, fixed in #357) is closed, its Q19 half stays open (process point 3); graph-sketcher-s1-006 is four entries (Part 2 #14). **stat-attack-s1-006 closed, citing #350 (856aa7c), on Jon's ruling:** the by-value bound comparison is on main; the sign-ignoring residual stays described in its summary, with no open entry of its own.
- **Step 1 merged:** #361. Lesson: stage by explicit path, never `git add -A docs` after a script run (a regenerated REGISTER.md slipped in). Not done: process point 2, the class-label tidy (unlisted in the contract).
- **Progress (each PR's description has the detail; every verifier pins its fixes, with plants):** fermi-lab #363 (s1-001 to -004, incl. the wrong key 140 -> 82 under SR-30); maths-court #364 (s1-004 to -007, -009 to -012); spot-the-error #365 (s1-001 to -007); new-shapes and graph-sketcher #366 (new-shapes-s1-001; graph-sketcher-s1-009 to -011); R4 #367 (`scripts/check-money.py` in CI; split-it-s1-002, stat-attack-s1-004); Year 6 #368 (formula-plug-in-s1-001; probability-pioneer-s1-001 to -004; shape-shifter-s1-001, -002; angle-ace-s1-001, -002); KS3 batch 1 #369 (sequence-solver-s1-002 to -004; estimation-golf-s1-001 to -006; prime-factorisation-s1-001; fraction-equivalence-s1-001; sequence-solver's verifier loads the pinned local KaTeX); KS3 batch 2 #370 (constructions-lab-s1-001, -002; equatle-s1-001 to -007; 52dle-s1-001 to -007; split-it-s1-003 to -008; word-problem-decoder-s1-004, -005, -007, -008, -010 and -003 ruled; equation-builder-s1-004, -005). The closed count is taken from the register at the end.
- **List for Jon (did not fit its rule, left open):** maths-court-s1-008 (core_003: "Paid off in year 14" against "About 13 years" are both true of 13.16 years, so R3 does not apply; no ruling gives wording). graph-sketcher-s1-006 (L4_5: Jon's drafted "the turning point" is ambiguous, since y = x^3 - 6x^2 + 9x has two turning points on [0, 4], (1, 4) and (3, 0); not applied per STOP IF; proposed "the local maximum"), graph-sketcher-s1-007, -012, -013 (implausible contexts; CM9's "speed cannot be zero" is true; L4_11 "maximum strain" and the `1.00e+6` display need a content or marking convention: no rule gives wording). estimation-golf-s1-007 (the speed-of-sound stem gives its key; deleting the bracket makes the item pure recall). word-problem-decoder-s1-006 (the extra "fell on the floor 4 times" sentence: a context change) and -009 (gcse_059 has no volume topic to be keyed under). 52dle-s1-008 (help-audit.md lists a How to Play modal the page lacks: a home-lane docs line). spot-the-error-s1-008 (gcse_007: "similar in shape" is keyed and the missed cue, the capacity, is not offered; no distractor is defensible, so R5 does not apply, and offering the capacity would change the design or the key).
- **Next:** step 3 in the contract's audience order (KS3, Essentials at GCSE, other GCSE, Core, A-Level, L4), then step 4 (proportion-blaster-003's class count). L4_5 stays with Jon.

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
