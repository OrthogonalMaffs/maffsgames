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
**SWEEP-1** (12 Oct, contract `docs/handover/contracts/2026-10-12-sweep-1.md`): one reading sweep of 96 live games (glorious-gantt skipped), 12 batches of 8 in lowest-level order; findings in each game's file, report `docs/audits/sweep-1-2026-10.md`. **Jon's rulings, 13 Oct** (verbatim: `docs/handover/contracts/2026-10-13-sweep-1-rulings.md`): word-problem-decoder and equation-builder fixed, not unlisted; **equation-builder must merge today, or say so and the home lane unlists it.** Batches 1-3 DONE (#332, #336, #339); equation-builder DONE (#338). Batch 4 (truth-buster, spot-the-muppet, terrible-advice, wrong-on-the-internet, maths-court, expected-damage, higher-power, prisoners-dilemma): PR open. Batch 5 (seven-bridges, distinctly-average, just-pythag-it-bruv, fermi-lab, six-sevens-bruv, free-daily-pizza, gradient-hunter, index-laws): being read.
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

## 2026-10-13 (cloud): SWEEP-1 batch 4 (KS3 part 2)

- **Fixed (rulings):** terrible-advice gcse_008/core_002 true "X is correct" options, ks3_017/gcse_019 true equations, gcse_018 "add for OR" (SR-16); wrong-on-the-internet ks3_007 "a fair coin", core_004 "5% compound interest" (Jon's ruling, RULED); maths-court ks3_002's summary names Numerica (SR-16, a check on every case), gcse_010 3 s.f. (SR-1), core_007's 1.048¹⁰ (SPECS); higher-power ks3_35's fact (check_perfect). Each verifier PASS locally with its new plants.
- **Open, for Jon:** maths-court-s1-004 HIGH (gcse_001 keys Brenda's false rule correct); SR-14: expected-damage s1-003 (core_004 "stand and welcome it"; the trolley premise), spot-the-muppet s1-002 and terrible-advice core_004 ("No Relation to the Clown").
- **Class for Jon (running):** fair coin unstated in three games (spot-the-muppet ks3_014, terrible-advice ks3_014; woti fixed); "add 5 to the last digit" praised as a method (spot-the-muppet, terrible-advice gcse_006, woti gcse_020); the court never says if it judges the reasoning or the answer (maths-court).

## 2026-10-13 (cloud): SWEEP-1 batch 3 (KS3 part 1; SR-20 stop and Jon's rulings)

- **Stop:** word-problem-decoder GCSE (3 SR-18 overlaps) and equation-builder (31 "expression" items) reached SR-20's count; Jon ruled the same day (fix, no unlist). equation-builder: #338 merged.
- **Fixed here:** word-problem-decoder gcse_029, 056, 024 and ks3_030 accept their second topic (SR-18; ACCEPT rows; plant on gcse_029); split-it's speed question says "At the same speed" (SR-17; the verifier's pattern needs it, so the old wording fails).
- **Open, for Jon:** spot-the-error-s1-001 HIGH (ks3_010: the explanation blames the 80 trials, "replaces it 80 times" marked wrong; moving the Stage 2 key needs a ruling); s1-003 (Stage 2 slip items, a class); equatle s1-001 (left to right); 52dle s1-001/s1-002 (false or empty clue facts); and the LOWs.
- **Class for Jon (running):** Stage 2 "misread phrase" on slip items (spot-the-error); "form an equation" phrases and Forming Expressions (word-problem-decoder, Jon to rule once); rates under Ratio & Proportion (word-problem-decoder s1-003).

## 2026-10-13 (cloud): equation-builder, Jon's ruling (SWEEP-1 batch 3's stop)

- **Stems:** 27 "Write an expression for X" items now ask for "a formula for X" (keys unchanged). **Keys:** ks3_014 `LCM(420, 315)` (Days, = tiles removed), ks3_033 `2 × r³`, l4_015 `log(16)`, l4_021 `∫₁⁴ 2x dx`. Full list in the PR.
- **Rearrangements:** gcse_008, 012, 014, 018, 019 now equations (as gcse_007); valid gains gcse_008 ×, gcse_012 −, gcse_018 ×, gcse_019 +.
- **Tiles:** shuffled per question by `orderTiles()`, never starting with the key's tiles in order.
- **Verifier:** kind from the question's words (last "write" sentence), SR-25 form check, tile order checked in Chromium (part 1); five new plants. Locally: check PASS, --selftest PASS, --part-selftest PASS (through `run_offline_sync.py`).
- **Findings:** equation-builder-s1-001 HIGH, s1-002 HIGH, s1-003 MEDIUM fixed; s1-004, s1-005 LOW open (l4_010 form only; l4_021 "Evaluate").

## 2026-10-13 (cloud): SWEEP-1 batch 2 (Year 6 part 2, sequence-solver)

- **Fixed (SR-17):** sequence-solver gcse[48] "Fill in the gaps" -> "If arithmetic, fill the gaps" (key unchanged); the verifier's FILL() now fails an ask naming no type (plant: the old ask).
- **Open:** probability-pioneer s1-001 MEDIUM, s1-002; shape-shifter s1-001..002; new-shapes s1-001 MEDIUM (waits on the SR-26 redraw, Jon 12 Oct); angle-ace s1-001..002; sequence-solver s1-002 MEDIUM, s1-003..004. No new findings: decimal-detective, four-quadrant-explorer, like-terms-collector.
- **Class for Jon (running):** assumptions unstated (fair, six-sided, at random): probability-pioneer (s1-001). Raw TeX on screen: sequence-solver (s1-002; r-002 already).
- **Container:** verifiers that load KaTeX from the CDN run here through `run_offline_sync.py` (scratchpad): it patches the sync API's launch (executable /opt/pw-browsers/chromium) and new_context (routes the KaTeX CDN to `scripts/fonts/katex/dist`); the verifier is unchanged. The async wrapper from sandbox-checks.md does not reach sync-API verifiers (goto times out).

## 2026-10-13 (cloud): SWEEP-1 batch 1 (Year 6 games, part 1)

- **Read:** estimation-golf, factor-race, prime-factorisation, percentage-flip, fraction-equivalence, negative-number-line, think-of-a-number, formula-plug-in. Report section in `docs/audits/sweep-1-2026-10.md`.
- **Recorded (open, none fixed):** estimation-golf-s1-001 MEDIUM, s1-002..005 LOW; prime-factorisation-s1-001, fraction-equivalence-s1-001, formula-plug-in-s1-001 LOW. No HIGH, no CRITICAL.
- **Method:** one read-only reviewer per game (brief: session scratchpad `sweep-brief.md`; inputs: the page, `data/banks/<slug>.json` from an offline extract, the verifier, the findings file), then every candidate checked against the page by me before recording. Out-of-scope notes go in the report, not the register. Fixes only where a ruling decides the wording; new copy is Jon's.
- **Class for Jon (running):** SR-12, "Estimate" with no stated method and an exact key: estimation-golf (s1-001).
- **Container:** esprima from the sdist on PYTHONPATH, `pip install playwright==1.63.0 sympy mpmath` (pyyaml is Debian's), KaTeX from `scripts/fonts/katex/dist` through the sandbox-checks wrapper: 82 live, 1 static, 14 generators.

## 2026-10-13 (cloud): B11-CLEAR game 7, complex-converter (#331); B11-CLEAR complete

- **Replacement (kind a, key unchanged):** id 43 (7e^{j0} to rectangular, key 7): 0 + 7j -> 0 (took e^{j0} as 0, not 1); 7j kept.
- **Listed (kind b):** id 15 (3e^{j pi/6} to polar, key 3 angle 30 deg) beside 3 angle pi/6: its context, shown on screen, reads "Express in polar form (degrees)." The verifier now reads pi angles in radians.
- **FOR THE HOME LANE: data/check-ledger.json holds no B11 entry for any game** (summed over every game after #331). Exit-bar point 3's "B11 parser" item can be set to True in
  audit-register.py (the cloud lane does not edit that file). All 8 kind-(b) pairs are allowlisted with their ask quoted; none needed Jon's ruling. Every replacement is listed in
  the game entries above and in each PR (#312, #315, #320, #324, #328, #330, #331); each of the seven verifiers fails on a planted equal-value pair.
- **Container note:** boolean-blitz's extraction needs KaTeX; locally (CDN 403) it falls back to the LAWS bank and check-banks --ci misreads it. CI reads it correctly.
