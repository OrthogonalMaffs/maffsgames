# Cloud lane handover: archive

History only, never loaded by default (contract CTX, 8 Oct 2026). `docs/handover/cloud.md` keeps the current state
and the last three entries; older entries move here, newest first, unchanged.

## 2026-10-13 (cloud): SWEEP-1 batch 12 and the end of the sweep (A-Level and Further Maths, part 3)

- **SWEEP-1 is finished:** every live game except glorious-gantt has been read (batches 1 to 12), 13 SR-20 levels fixed the same day under SR-30. The home lane can set SWEEP_DONE = True (audit-register.py was not touched). The report's closing section (`docs/audits/sweep-1-2026-10.md`) holds the list for Jon, grouped by class.
- **Ledger lesson (CI, Tier 4 layer A):** fixing a game's wording can remove a ledgered B7 entry; the lint then fails "STALE ledger entry" until `data/check-ledger.json` is cleared. Run `python scripts/check-banks.py --ci` after `extract-banks.py` before pushing a text fix (it caught `matrix-crunch` and `eigenvalue-extractor` here).
- **Fixed in batch 12:** complex-converter's six wrong calculator-hint results (SR-8, closing t6-005; every hint pair is now recomputed); matrix-crunch's true wrong options on the singular systems and its shuffled "Same circuit" items; eigenvalue-extractor's "No eigenvalues exist"; truth-will-set-you-free's "any two", symbols, XOR and unnamed output; boolean-blitz's Q38 step and four no-op steps; characteristic-quest, eigenvector-engine and factor-theorem wording. Each verifier fails on the old content and plants it.
- **Open, for Jon:** see the report's grouped list. **For the home lane:** log-laws' 34 negative typed answers and suvat ALEVEL[34] behind inputmode="decimal"; SR-32 (CMP1) into canon and a figure check in the other chart games; the timer-policy class (SR-23: circle-theorem-spotter, dimension-checker, matrix-crunch, growth-and-decay, characteristic-quest ...); eigenvector-engine's and others' hard-coded logged level.
- **Next:** nothing from this contract. The sweep's last step is Jon's rulings on the grouped list, which the cloud lane then applies in per-game PRs.

## 2026-10-13 (cloud): CMP1-READABLE-FIGURES (core-maths-paper1; SR-32)

- **Contract:** `docs/handover/contracts/2026-10-13-cmp1-readable-figures.md`. Jon's play-test: Q4's histogram bars at 2.4, 3.6 and 1.2 had no gridlines and labelled ticks only at 0 to 3, so 3.6 could not be read. The fix is in the game's chart-drawing code: the gridline step is the largest of 1, 0.5, 0.2, 0.1 (times a power of ten) at which every plotted value lies on a gridline (Q4 every 0.2, Q12 every 0.1), the labels unchanged; each box-plot number sits over a tick. Q12 and Q9 had the same fault and are fixed with it.
- **Verifier:** every figure is read (each bar's density has a gridline or labelled tick within 0.5 px and the bar is drawn there; each box-plot value has a labelled tick; gridlines at least 4 px apart at 320 px, measured in Chromium: 4.3 px). Three plants; the old page fails 13 checks.
- **End of task:** #357 merged and main's run (993) green. `scripts/end-task.py claude/cmp1-readable-figures` REFUSED here (the cloud sandbox has no `gh`, so it cannot report the PR's state); nothing was deleted by hand, so the local worktree and branch are left for a session that has `gh`.
- **Slug:** the contract wrote core-maths-paper-1; the game, verifier and findings file are core-maths-paper1.
- **For the home lane:** SR-32 is not yet in canon (the contract leaves it to the home lane). Other games that draw charts have no check of this kind (chart-interrogator, graph-sketcher, stat-attack and others): a verifier rule per game, as here. The 320 px spacing needed a taller chart for a 0.1 grid (Q12's drawing is 364 units tall).
- **Next:** batch 12 (factor-theorem, complex-converter, matrix-crunch, characteristic-quest, eigenvalue-extractor, eigenvector-engine, boolean-blitz, truth-will-set-you-free), then the final "for Jon" list and the SWEEP_DONE note.

## 2026-10-13 (cloud): SWEEP-1 batch 11 (A-Level, part 2: mechanics, logs, binomials, proofs)

- **No SR-20 level.** Three HIGH items fixed: moments-master ("At the pivot" true as a wrong option), binomial-blaster ("r > n" true), proof-builder (a second valid order of the cos² + sin² proof rejected, SR-24; the verifier now holds every reviewed order).
- **Fixed in batch 11:** dimension-checker's four verdict-sharing options (SR-31); force-resolver's shuffled "Same system" item, stated beams, 18 unstated precisions and 21 unchecked working lines; curling-friction's head-on collisions, horizontal surfaces and a duplicate KE option; moments-master's eight precisions, perpendicular, opposite sides, beam weight; log-laws' undeclared log₁₀ in Laws mode; proof-builder's induction domains and wording; binomial-blaster's two true options; partial-fractions-duel's method item and hint check. Each verifier fails on the old content and plants it.
- **Open, for Jon:** proof-builder's TRUE option appearing only where it is the key (a design choice), a lemma order, key texts; log-laws' "Change of Base" label; binomial-blaster's ≈ stems and the coefficient item; dimension-checker's live timer (SR-23); curling-friction's "Worked solution" heading. **For the home lane:** log-laws' 34 negative typed answers behind inputmode="decimal".
- **Next:** (done: see the CMP1-READABLE-FIGURES entry above.)

## 2026-10-13 (cloud): correlation-or-coincidence (#347) and SWEEP-1 batch 8 (GCSE part 4)

- **SR-20 hit, ruled the same day:** correlation-or-coincidence keyed "Something else causes both" on three pairs where one drives the other (B22, B25, B27). #347: Jon's three pairs (shoe size/reading age, ice creams/sunburn, umbrellas/taxis), the verifier bars the old pairs; the new ones overlap B4, B1 and B3 (s1-002, my error, for Jon).
- **Fixed in batch 8:** component-crusher L9's direction vector takes any non-zero multiple (SR-24), and AL11/L11 state their axes; formula-forge's A = πr² misconception; better-value's three true threshold options, the meal-prep reason, the van's resale and TPFT; given-that's two explanations; chart-interrogator's unlabelled boundaries and four-option Q1; expectation-station's k-cells ("2k = ?"), exact reveal and "Exactly half". Every verifier PASS locally with its plants; answer-lock PASS.
- **Open, for Jon:** better-value-s1-002 (equal at break-even, with r-006); chart-interrogator-s1-001 (histogram bands by axis, canon §7.1.2) and s1-005; expectation-station-s1-005 ("Most"); stem changes in unit-converter, formula-forge, given-that.
- **Class (running):** verifier gaps in worked text in every batch 8 game (each has an entry); conventions stated in one item and not its neighbours (component-crusher AL14 only).

## 2026-10-13 (cloud): core-maths-paper2a (#349), stat-attack (#350) and SWEEP-1 batch 9 (GCSE part 5, Core Maths)

- **Two SR-20 levels, fixed under SR-30:** core-maths-paper2a (three true criticisms as wrong options, #349); stat-attack (#350: the mean, SD and variance marked to bands, not the 3 s.f. asked; a wrong SD marked right on all 36; the variance to 3 s.f. and the SD from the unrounded variance on Jon's ruling).
- **Jon's rulings, 13 Oct (verbatim in the rulings file), done in batch 9's PR:** paper2a Q5's CEO says "increased by 10%"; paper2b Q24, Q33, Q35, Q36 give a verdict other than the key's; **SR-31 (standing): no wrong option gives the key's verdict or choice** (a check in every Core Maths verifier and in the brief; its scan fixed five more); Screening Room's box shows a fixed % and reads a percentage.
- **Fixed in batch 9:** screening-room wording; estimation-engine's counts as £ and its money format path (SR-3); core-maths-paper1 (stem-and-leaf key, SR-16/SR-31 options); paper2b (precision, assumption); paper2c (units).
- **Next:** (done: see batch 10's entry above.)

## 2026-10-13 (cloud): growth-and-decay (#352), test-the-claim (#353), graph-sketcher (#354) and SWEEP-1 batch 10 (Core Maths and A-Level, part 1)

- **Three SR-20 levels, each fixed in its own PR under SR-30 (keys unchanged):** growth-and-decay (#352), test-the-claim (#353), graph-sketcher (#354): typed answers marked to bands that disagree with the precision their prompt states, so wrong answers were marked right and right ones wrong (todo §1.36); now marked through the shared MaffsAnswer at the stated precision, plus true or accepted-H0 wrong options (SR-16), signed boundaries and stated conventions (SR-17).
- **Jon's tax-theft ruling, done in batch 10's PR (verbatim in the rulings file):** Hard's table in taxable-income bands from uk_rates.py, the payslip annual throughout, "You Keep per Year", the factor-of-12 hint skipped on a £0 key, Jon's closing line.
- **Fixed in batch 10:** integration-duel's three working lines (every expression of the working is now checked); normal-navigator's 26 unstated precisions (SR-1), the IQR working, "exactly 95%"; suvat's double-negative deceleration.
- **Open, for Jon:** normal-navigator-s1-002 (minimum-mark rounding) and -007 (one level logged for three); suvat-s1-002 and -005; differentiation-duel-s1-001; the SR-20 games' open entries (growth-and-decay s1-003/-004/-007/-008, test-the-claim s1-006/-007, graph-sketcher s1-006/-007). **For the home lane:** suvat ALEVEL[34] (v_y = −0.32 behind inputmode="decimal").
- **Next:** batch 11 (curling-friction, force-resolver, moments-master, log-laws, binomial-blaster, partial-fractions-duel, proof-builder, dimension-checker), then batch 12 (factor-theorem, complex-converter, matrix-crunch, characteristic-quest, eigenvalue-extractor, eigenvector-engine, boolean-blitz, truth-will-set-you-free), then the final "for Jon" list and the SWEEP_DONE note. Notes: scratchpad `batch11-notes.txt`.

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

## 2026-10-13 (cloud): SWEEP-1 batch 5 (KS3 part 3, first GCSE)

- **Fixed:** index-laws, 20 conversion items name their form (SR-17; form_needed()); gradient-hunter, exact keys at 2+ places say "Give the exact value." (SR-1) and two true y-value options name their error (SR-16).
- **Open, for Jon:** fermi-lab-s1-001 HIGH (eq_bus_distance keys student-km for "distance travelled by school buses"); gradient-hunter-s1-003 (y-value readings true at an instant, about twenty options).
- **Class for Jon (running):** assumptions only in hidden hints with tight bands (fermi-lab s1-002).

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

## 2026-10-12 (cloud): B11-CLEAR game 3, index-laws (#320)

- **Replacements (kind a, keys unchanged):** [6] 3^{12} -> 3^2 (subtracted the powers; 9^6 kept); [27] 1/x^{-3} -> −1/x^3 (negative as well; x^3 kept); [38] 27/3 -> 1/3, [39] 100/2 -> 1/10, [40] 25/2 -> 1/5 (reciprocal as for a negative power; 9, 50, 12.5 kept).
- **Verifier** fails on any equal pair except the key beside another form where `ask` names it ((5^2)^3); plant puts 3^{12} back.
- **Games 4-7 are built and committed locally** (worktrees /home/user/wt/sfb, ss, bb, cc; branches claude/b11-<slug>), each verifier PASS with its plant, each ledger clean for its game only. Each needs: rebase on main, claim commit pushed alone, fix pushed, PR, findings + release commit. Recipe: KaTeX via `npm pack katex@0.16.9` in the scratchpad; extraction through `docs/sandbox-checks.md`'s `run_extract_offline.py`; verifiers take `--katex-dir`.
- **Surd Simplifier note for Jon:** six of its eight pairs (27/99 and 9/33 for 3/11, and so on) are both the KEY's value unsimplified, under "simplest form": SR-4's form exception, so they are listed in the allowlist (as alevel[6]/[7] already were), not replaced. gcse[38] and [43] are replaced. Jon can reverse this.

## 2026-10-13 (cloud): B11-CLEAR game 6, boolean-blitz (#330)

- **Replacements (kind a, keys unchanged):** Q4 NOT(AB) -> NOT(A)NOT(B); Q15 NOT(A) + A -> A NOT(B); Q17 A.BC -> 0; Q40 ABC + ABD -> ABCD (each a named slip; the other of each pair kept).
- **Listed (kind b):** Q2, Q10, Q12, Q19 (key unsimplified, wrong under "Simplify fully.") and Q24, Q41 (second forms accepted, #227), all in b11_form_questions. No stem changed; nothing for Jon.

## 2026-10-13 (cloud): B11-CLEAR game 5, surd-simplifier (#328)

- **Replacements (kind a, keys unchanged):** gcse[38] 0.(2): 1/5 -> 2/99 (used 99, as for two recurring digits; 2/10 kept). gcse[43] 0.(45): 9/20 -> 4/9 (took only the 4 as recurring; 45/100 kept).
- **Listed, not replaced:** gcse[42], [44], [49], alevel[31], [32], [39]: both options are the key's value uncancelled, and each ask is "Convert to a fraction in its simplest form" (SR-4's exception, as alevel[6]/[7]).
- **Local KaTeX:** this verifier takes `--katex-dir scripts/fonts/katex/dist`; without it, it times out here (CDN 403), as main's copy does.

## 2026-10-13 (cloud): B11-CLEAR game 4, standard-form-blitz (#324)

- **Replacement (kind a, key unchanged):** alevel[35] (5 x 10^-2)^-2, key 4 x 10^2: 25 x 10^2 -> 2.5 x 10^-3 (squared, ignoring the minus in the power); 2.5 x 10^3 kept.
- **Verifier** fails on any equal pair except, where standard form is asked, the key's value in another form; plant puts 25 x 10^2 back. Ledger: only this game changed.
- **Note:** a ledger change selects ~150 checks in check-changed.py; locally it passes the 50-minute cap. Games 5-7 (surd-simplifier, boolean-blitz, complex-converter) are built locally in
  /home/user/wt/ss, bb, cc (one commit each on an older main; cherry-pick onto a fresh claim commit, as game 4).

## 2026-10-12 (cloud): B11-CLEAR game 2, coordinate-geometry-dash (#315)

- **Replacement (kind a, key unchanged):** alevel[15] (x = 2t + 1, y = t^2 - 3, dy/dx at t = 1; key 1): 1/2 -> −2 (gave y at t = 1, not the gradient); ½ kept.
- **Verifier** fails on any equal pair (EQUAL_PAIRS empty; plant puts 1/2 back). Ledger: this game only.
- **Container (new session after a clear):** cdn.jsdelivr.net is refused by the proxy (403), so every browser check of a page loading KaTeX from the CDN fails locally (about 30, incl. answer-lock parts); the changed game's own verifier and B11 passed. CI is the measure. Playwright needs `PLAYWRIGHT_BROWSERS_PATH` pointing at a dir with `chromium-1243 -> /opt/pw-browsers/chromium-1194` (and the headless shell likewise); esprima as in game 1. A full check-changed run takes over 35 min here: give the background run the 2 h timeout. Never run two at once (they share the stub server's port: "QUESTIONS is not defined").
- **Next:** index-laws (replacements drafted: [6] 3^{12} -> 3^2, subtracted the powers; [27] 1/x^{-3} -> −1/x^3, made the answer negative as well; [38] 27/3 -> 1/3, [39] 100/2 -> 1/10, [40] 25/2 -> 1/5, each took the reciprocal as for a negative power; the kept twin of each is the student's own form). Then standard-form-blitz ([35] 25x10^2 -> 2.5x10^{-3}, squared and ignored the minus); surd-simplifier (its pairs also equal the key: 27/99 = 9/33 = 3/11; ask "simplest form"); boolean-blitz (every question shows "Simplify fully.", so the six kind-b items are allowlisted, #227 accepts AB + BC for B(A + C)); complex-converter ([14] context "Express in polar form (degrees).": allowlist; [42] 0 + 7j -> 0, took e^{j0} as 0).

## 2026-10-12 (cloud): B11-CLEAR game 1, scale-factor-scaling (#312, merge commit 031d8ed)

- **Replacements (kind a, keys unchanged):** T1[8] 4:10 -> 4:5 (squared only the first number; 2:5 kept); T1[9] 3:9 -> 1:6 (doubled the scale factor instead of squaring it; 1:3 kept).
- **Verifier** fails on any equal pair (EQUAL_PAIRS empty; plant puts 4:10 back). **Ledger:** `extract-banks.py --only` then `check-banks.py --only <slug> --write-ledger`; only this game changed.
- **Container:** extraction needs esprima, which will not build here; the CI pin (4.0.1) is pure Python: `pip download --no-binary :all: esprima==4.0.1`, untar into the scratchpad, put it on PYTHONPATH.

## 2026-10-12 (cloud): VERIFIERS-20 game 20, prisoners-dilemma (#309, merge commit 9b57ab9); the list is complete

- **Verifier:** `scripts/verify-prisoners-dilemma.py` (from the parked draft). The game marks nothing, so (as constructions-lab) it checks what the game states and does: payoffs, every opponent
  against its stated rule over 3040 histories, 28 games and a tournament per level played in Chromium with every score and figure recomputed. Six planted faults fail. t4-001 untouched.
- **Main's runs:** 38299209665 (#308, after #307) green; #309's Gate green first time.
- **VERIFIERS-20 complete:** 20 verifiers, #282-#309. Findings opened: fraction-equivalence-v20-001 (stays open until that bank's SR-26 growth, Jon 12 Oct), index-laws-v20-001 (ruled, #297),
  formula-forge-v20-001 (ruled below). Fixed on the way: characteristic-quest-t6-003 (#306), woti t2-006 (#304), the modular-battle verifier flake (#303).
- **Jon's rulings, 12 Oct:** formula-forge-v20-001: in each equal pair the sqrt(x^2) form is replaced (v = u^2 + 2as; a = sqrt(c^2 + b^2); u = sqrt(v^2 + 2as)), keys unchanged, EQUAL_PAIRS emptied, finding
  closed, in its own PR (claimed here). prisoners-dilemma is off the remaining line (#309), so the **home lane can do t4-001**.
- **Drafts branch** `claude/verifiers-17-20-drafts` is spent (all four drafts merged); it can be deleted with the merged `claude/verifier-*` branches (the proxy refuses remote deletes).

## 2026-10-12 (cloud): MAIN RED, verify-modular-battle (run 826, #301's merge); fix is this lane's

- **Were #300 and #301 merged on green? Yes, both.** #300 merged after run 820 (#298) finished green (17:22 UTC); #301 after
  run 825 (#299) finished green (17:53). #300's own run, 822, was green. **Main went red on 826, #301's own merge run:**
  Content verifiers 13, verify-modular-battle (#298's verifier), attempt 1 and the re-run both failed. No cloud merge since.
- **Cause (a flaky verifier, not the game):** after the 408 steered questions, the scaffold and 90-second session drivers
  loaded questions on live `Math.random`. Under the "key offered twice" plant a b = 2 draw can show only the key twice, so
  `find()` returned undefined and the script threw (TypeError at `b.click()`). Measured: the old driver threw 24 of 200.
  It passed #298's PR and runs 820, 822 and 825 by chance.
- **FIXED: #303 merged (9714acc)** after its Gate was green and main's run 828 (#302) was green. Watch main's run on 9714acc.
- **Fix (#303):** both drivers load fixed steered questions (`DRIVE_PAIRS`) and
  assert the steering took; a missing button is a `scaffold:`/`session:` FAIL, not an exception. New driver: 0 of 200, one
  outcome. Full verifier three times: PASS, identical output, all 7 plants caught.
- **Class check: local.** Of the 16 VERIFIERS-20 scripts, only this one drives play on live randomness; the other
  find-then-click drivers (four-quadrant-explorer, standard-form-blitz, index-laws) press fixed items, so are deterministic.
- **Then:** the woti t2-006 PR (#304) merges only once main's run after #303 is green.

## 2026-10-12 (cloud): New Shapes diagram findings, Jon's ruling

- **Jon, 12 Oct:** New Shapes' diagram findings (r-001, t3-003, t3-004, t3-005: proportions fixed whatever the numbers, the prism's l arrow on the wrong dimension) **stay open until its SR-26 bank growth, which redraws from each question's parameters.** No cloud-lane redraw before then. The `new-shapes` verifier (#292) checks the numbers on the diagram only and prints that the geometry is not asserted; when the bank is grown and the diagrams are drawn from each item's parameters, extend the verifier to assert the geometry (drawn proportions and the l arrow along the depth edge) and close those four entries in the same PR.

## 2026-10-12 (cloud): Runner cancels at "Initialize containers" (Jon's rule, 12 Oct)

Rule: a job cancelled at Initialize containers is runner infrastructure; re-run only those jobs, up to 3 times per run; a green re-run counts as main green; any other failure or cancel stops the lane. Record per cancelled job, duration against timeout (content groups: 6 min = 360 s), for the home lane:
- Main run 802 (bb79123), attempt 1: 8 jobs cancelled at Initialize containers (Site-wide checks, Content verifiers 3, 9, 12, 25, 14, 32, 24). Durations not captured; one re-run used.
- Main run 802, attempt 2: Content verifiers 33 cancelled at Initialize containers, 10:56:22 to 11:02:41 = 379 s against a 360 s timeout (the whole timeout spent before the first step ran). Second re-run used.
- Earlier, on PR heads: #291 Content verifiers 3; #292 Tiers 1+2 shard 3/4, Content verifiers 4, then 3, 21, 13. Durations not captured.
Reading: 379 s is over the timeout, so the container pull is consuming the timeout, not the checks.

## 2026-10-12 (cloud): CHECKPOINT 2 (Jon asked for one at 66% context)

- **Merged:** VERIFIERS-20 games 1-16 (#282-#287, #290-#298, #300, #301; index-laws ruling #297); main green after each (last checked: 38286441432 on #299, and the #301 merge's run was in progress).
- **IN FLIGHT: wrong-on-the-internet t2-006 (Jon's SR-14 ruling, 12 Oct), branch `claude/woti-t2-006`.** Pushed: claim commit, and the one-line change in woti_core_006's correct stage-2 option
  ("At 100°C humans can't survive, let alone buy ice cream." becomes "At 100°C water boils, so nobody is queuing for ice cream."; key, options, explanation unchanged). The verify-wrong-on-the-internet.py run passed.
  **#304 open:** check-changed run (woti passes; only the container's esprima/WebKit/KaTeX failures); t2-006 set fixed with pr 304 and the ruling; the game is off the remaining line.
  DONE: main run 830 (#303) green; #304 merged on a green Gate (73478d6).
- **Next, games 17-20:** drafts that pass are parked on branch `claude/verifiers-17-20-drafts` in `docs/handover/drafts/`, with a README giving each one's follow-ups (formula-forge-v20-001 to file for Jon;
  characteristic-quest's t6-003 SR-6 fix as a patch; a plant label to fix in eigenvalue-extractor; prisoners-dilemma left alone on t4-001). Each game gets its own claim, PR, Gate and main run.
- **Open for Jon:** formula-forge-v20-001 (three items with two wrong options equal in value; replacements suggested in the drafts README). Merged `claude/verifier-*` remote branches need deleting (the proxy refuses).
- **Interim rule:** the re-run rule for "Initialize containers" cancels can be retired once main has had two full runs with no such cancel since #299 (CONTAINER-PULL-TIMEOUT); remove it then.
- **Container setup (each new session):** Playwright 1.63 expects Chromium build 1243; the container has 1194 in another layout. In a scratch dir make `chromium_headless_shell-1243/` (with empty INSTALLATION_COMPLETE and DEPENDENCIES_VALIDATED files)
  holding a symlink `chrome-headless-shell-linux64 -> /opt/pw-browsers/chromium_headless_shell-1194/chrome-linux`, plus `chromium-1243/chrome-linux64` the same way. Add a symlink `chrome-headless-shell -> headless_shell` inside that 1194 dir.
  Set `PLAYWRIGHT_BROWSERS_PATH` to the scratch dir.
- **Recipe that works (games 1-8):** worktree from origin/main; claim commit (the previous game's entry + one `cloud-remaining` line) pushed alone; script; `ci-groups --check`,
  `audit-register --check`, `check-verifier-coverage`, `check-context-size`; PR; merge on green Gate with main's last run green (the "Record CI timings" commit appears only after a
  green main run). KaTeX games: serve it with `bc.is_font_cdn` + `bc.serve_real_font`. Never write the remaining-list token in backticks in an entry; keep this file under 20 KB (move old entries to the archive).
- **TeX readers (Jon, 12 Oct 2026):** per-verifier TeX readers are acceptable (as in verify-formula-unlocked.py, games 12 and 13); games 17-19 carry their own. HOME-LANE ITEM: give `bank_common`
  one exact TeX reader and move these verifiers onto it. Today `parse_value` reads `6x^7 \div 2x^2` as 3x^9 (against Jon's ruling on index-laws-v20-001), reads standard form as a float,
  and returns None for `v = u + at` (multi-letter juxtaposition) and for anything with `\lambda`.
- **Pre-push set for verifier-only PRs (Jon's ruling, 12 Oct 2026; the home lane records it as SR-27):** run the verifier and its self-test, `ci-groups.py --check`,
  `audit-register.py --check`, `check-verifier-coverage.py` and `check-context-size.py`; not `check-changed.py`. A PR that also touches a game page, a shared asset or another script still runs `check-changed.py`.
  Applies from game 12 (standard-form-blitz); games 10 and 11 ran the longer set.

## 2026-10-12 (cloud): VERIFIERS-20 game 19, eigenvalue-extractor (#307, merge commit 1cc99fa)

- **Verifier:** `scripts/verify-eigenvalue-extractor.py` (from the parked draft): 25 items, each equation solved in SymPy and every option read as its eigenvalues; 36 worked lines and sums checked; every option
  pressed in Chromium. Seven planted faults fail (one plant's label corrected: it plants a repeated root keyed as 3 and -3). No faults; no findings closed.
- **Main's runs:** 38298131469 (#306) green first time; #307's Gate green first time.

## 2026-10-12 (cloud): VERIFIERS-20 game 18, characteristic-quest (#306, merge commit 521c40c)

- **Verifier:** `scripts/verify-characteristic-quest.py` (from the parked draft): 26 items, each det(A - lambda I) recomputed in SymPy, every option classified, 76 worked expressions and trace/det/eigenvalue claims
  checked, every option pressed in Chromium. Eight planted faults fail, one of them the old t6-003 step put back.
- **Fixed: t6-003 (SR-6).** [[0,2],[2,0]]'s worked step read as lambda^2 + 4; now the trace-and-determinant form. One line of the game page. Full check-changed run (SR-27): the game passes; the rest failed only on this container (esprima, WebKit, KaTeX CDN).
- **Main's runs:** 835 (#305) green first time; #306's Gate green on its head (the first head's run was cancelled by the next push).

## 2026-10-12 (cloud): VERIFIERS-20 game 17, formula-forge (#305, merge commit 7695b8e)

- **Verifier:** `scripts/verify-formula-forge.py` (from the parked draft): 45 items (GCSE and Level 4; A-Level reuses GCSE); every key solved back into its formula in SymPy (its own TeX reader, Jon 12 Oct),
  every option classified, 159 worked lines and Hint 2 equations checked, every option pressed in Chromium. Seven planted faults fail.
- **Open for Jon: formula-forge-v20-001 (MEDIUM).** Three items have two wrong options equal in value (sqrt(u^2) = u); keys right. Suggested replacements are in the finding and #305's body (new content, SR-19).
- **Main's runs:** 833 (#304) green first time; #305's Gate green first time. #304 (woti t2-006) merged on run 830 green.

## 2026-10-12 (cloud): VERIFIERS-20 game 16, constructions-lab (#301, merge commit 5b1307a; STOP IF: the game marks nothing)

- **Verifier:** `scripts/verify-constructions-lab.py`: there is no key (t3-001: nothing marks a construction), so per the contract's STOP IF it verifies what the game states and draws. Each task's figure is recorded from
  its own setup (moveTo/lineTo/arc/fillText) and every letter the steps name sits within 25 units of the point it labels; all ten tasks are built by their own steps with the game's compass, Lock Radius and ruler
  (clicks on the real canvas, pinned 1:1), every snapped crossing recomputed in Python (to 1e-6), and each stated result checked: perpendicular bisectors, angle bisectors, perpendiculars from and at P, "Angle BAC = 60°",
  the equilateral triangle, the 120px circle and the two 80px lines (label and steps agreeing), "more than half AB" both ways; the tap mapping at 390 px within one CSS pixel. Eight planted faults fail. About 10 s.
- **Not verifiable, reported:** whether a student's construction is right (t3-001); snapping ignores the given lines and points (t3-002: the verifier draws a ruler line along a given line first); t3-004, t3-005.

## 2026-10-12 (cloud): VERIFIERS-20 game 15, bearing-blitz (#300, merge commit 3575276)

- **Verifier:** `scripts/verify-bearing-blitz.py`: no option list (the key is the target bearing; the mark is the needle's error). All 360 whole-degree bearings pressed on the real compass (whole-pixel points chosen
  here within 0.35 degrees) and read back clockwise from North, with the needle drawn along each; 798 shots through Fire for 38 targets at -10..+10 degrees (every 0/360 wrap): hit within 5, points 150/100/50,
  message figures, lives; sessions (24 bearings, the 16 fixed present); three misses to "Submarine Destroyed!" through the real Next; twenty hits to "All Ships Sunk!" with the score added up. Eight planted faults fail. About 95 s.
- **Main's run:** 38285029221 (the #300 merge) green first time; Gate on #300 51 passed, 2 skipped.
- **Faults fixed:** none; no findings for this game.

## 2026-10-12 (cloud): VERIFIERS-20 game 14, modular-battle (#298, merge commit b220dd4)

- **Verifier:** `scripts/verify-modular-battle.py`: generated game (a 10..60, b 2..9). All 408 questions are driven through the game's own `generateQ()`/`loadQuestion()` by steering the two `Math.random`
  draws; 20,000 free draws land only on those 408 and reach all of them. Each: key = a mod b (Python divmod), min(4, b) different options from 0..b-1 with exactly one the key (SR-4/16), the dot grid
  (floor(a/b) groups of b, then a mod b red) and its label, every option pressed (feedback figures "a÷b=q rR" / "remainder R", score, Next). Scaffold shows, withdraws after 2 right, returns after 2 wrong;
  a session ends at 90 s with the right score. Seven planted faults fail. About 65 s with the self-test.
- **Main's run:** 38282980872 (the #298 merge) green first time; Gate on #298 51 passed, 2 skipped.
- **Faults fixed:** none. **Left open, not asserted:** t4-001 (says 60 s, runs 90; the portal card is outside the folder), t4-002, t4-003 (portal, spec map), t4-004 (the scaffold shows the answer: a design call).

## 2026-10-12 (cloud): VERIFIERS-20 game 13, index-laws (#296, merge commit 7339c3f; ruling #297, 5cdff5c)

- **Verifier:** `scripts/verify-index-laws.py`: all 45 items read from their TeX into exact SymPy expressions (positive symbols), every key worked out and the only right option (SR-4/16; the (5^2)^3 item's `ask` names a form,
  so 25^3 is legitimately wrong); the rule labels (8/8/7/4/8/10) checked against each question; 48 sums and stated roots in the explanations recomputed; KaTeX parses everything; sessions of 12 dealt 5 times; every item shown by
  `nextQ()` and all four options pressed in Chromium. Twelve planted faults fail after the ruling. About 35 s with the self-test.
- **index-laws-v20-001, RULED (Jon, 12 Oct):** the convention stands: a term such as 2x^2 is one object (implied multiplication binds tighter than ÷), so `6x^7 \div 2x^2` = 3x^5; keys and stems unchanged.
  The finding is closed as `ruled`; the verifier now reads a coefficient-and-variable term after ÷ as one term (no expected failures) and fails only a divisor that is not such a term (SR-17), in the follow-up PR.
  The home lane records the convention as a standing ruling.
- **Main's runs:** 38279747529 (#296) and 38281083831 (#297) green first time; both Gates 51 passed, 2 skipped.
- **Faults fixed:** none.

## 2026-10-12 (cloud): CHECKPOINT (Jon asked for one: context very high)

- **Done and merged:** games 1-7 (#282-#287, #290); the CI-TIMINGS-MEDIAN home-lane fix (#288, #289). **In flight:** game 8 four-quadrant-explorer, PR #291
  (verifier passes locally, 5 planted faults caught; waiting on its Gate; merge on green with main's run green, then record it in the next entry).
- **Game 9 draft:** `scripts/verify-new-shapes.py` is on branch `claude/verifier-new-shapes` (passes; 50 items; diagram numbers checked; 5 planted faults caught).
  To resume: after #291 merges, make a fresh worktree from origin/main, claim `new-shapes` in a handover commit, bring the script over from that branch
  (`git checkout claude/verifier-new-shapes -- scripts/verify-new-shapes.py`), run `ci-groups --check`, open the PR. The diagram's PROPORTIONS and the prism l arrow
  are deliberately not asserted (open findings r-001, t3-003/004/005: a redraw is Jon's call); the verifier prints that.
- **SR-26 (Jon, 12 Oct): growing banks.** A bank too small or with duplicates is fixed by growing it from parameters, never by swapping single items; new
  real-world contexts stop for Jon; a bank is grown only after its verifier runs in CI. This now decides `fraction-equivalence-v20-001` (the repeated Year 6 pair) and
  t1-001 (20 items): fix = a parameter-generated Year 6 pair bank. NOT started: the contract still says not to add questions, and the size and the named
  misconceptions for the non-equivalent pairs need Jon (a contract).
- **Recipe that works (games 1-8):** worktree from origin/main; claim commit (the previous game's entry + one `cloud-remaining` line) pushed alone; script; `ci-groups --check`,
  `audit-register --check`, `check-verifier-coverage`, `check-context-size`; PR; merge on green Gate with main's last run green (the "Record CI timings" commit appears only after a
  green main run). KaTeX games: serve it with `bc.is_font_cdn` + `bc.serve_real_font`. Never write the remaining-list token in backticks in an entry; keep this file under 20 KB (move old entries to the archive).
- **TeX readers (Jon, 12 Oct 2026):** per-verifier TeX readers are acceptable (as in verify-formula-unlocked.py, games 12 and 13); games 17-19 carry their own. HOME-LANE ITEM: give `bank_common`
  one exact TeX reader and move these verifiers onto it. Today `parse_value` reads `6x^7 \div 2x^2` as 3x^9 (against Jon's ruling on index-laws-v20-001), reads standard form as a float,
  and returns None for `v = u + at` (multi-letter juxtaposition) and for anything with `\lambda`.
- **Pre-push set for verifier-only PRs (Jon's ruling, 12 Oct 2026; the home lane records it as SR-27):** run the verifier and its self-test, `ci-groups.py --check`,
  `audit-register.py --check`, `check-verifier-coverage.py` and `check-context-size.py`; not `check-changed.py`. A PR that also touches a game page, a shared asset or another script still runs `check-changed.py`.
  Applies from game 12 (standard-form-blitz); games 10 and 11 ran the longer set.
- **Container setup (each new session):** `pip install playwright==1.63.0 sympy mpmath`; Chromium 1194 via a scratch dir of symlinks named 1243 (see the container note in the game 1 entry); `PLAYWRIGHT_BROWSERS_PATH` pointing at it.
- **Remaining after 12:** index-laws, modular-battle, bearing-blitz, constructions-lab, formula-forge, characteristic-quest, eigenvalue-extractor, prisoners-dilemma (contract order).
- **Open for Jon:** delete the merged `claude/verifier-*` branches on GitHub (the proxy refuses remote deletes); `fraction-equivalence-v20-001` and SR-26 scope (above).

## 2026-10-12 (cloud): VERIFIERS-20 game 12, standard-form-blitz (#295, merge commit ad66122)

- **Verifier:** `scripts/verify-standard-form-blitz.py`: all 100 items (50 GCSE, 50 A-Level) read from their own TeX into exact SymPy values (conversions, products and quotients, powers, roots, sums, fractions),
  the nine context problems from the numbers in their text, comparisons decided from the listed values, the two solve-for items tried with each option. Each key equals the value at the stated precision
  (3 s.f., 1 s.f., nearest £, whole number), is in standard form where asked, and is the only right option (an equal but non-standard distractor is legitimately wrong). KaTeX parses every question and option
  (pinned local copy); sessions dealt 3 times per level; every item shown by `showQ()` and all four options pressed in Chromium. Twelve planted faults fail (two plant SR-4/16: an option equal to the key in value where standard form is not asked). About 45 s with the self-test.
- **Main's run:** 38277156140 (the #295 merge) green first time; Gate on #295 had 50 passed, 2 skipped. Pre-push was the short set (SR-27 note below).
- **Faults fixed:** none; no findings to close (the register has none for this game).

## 2026-10-12 (cloud): VERIFIERS-20 game 11, equatle (#294, merge commit a20cd5d)

- **Verifier:** `scripts/verify-equatle.py`: the generated bank (23,399) recomputed exactly (`Fraction`, BODMAS, leading zeros); all 55,825 valid 8-character equations enumerated here
  and every one accepted by `validate()` (no float refusal); refusal figures; `states()` against Wordle's rule over 131,000+ pairs; Hard Mode over 3,000 cases; the daily pick for 34 dates;
  played in Chromium on a stepped clock (win, six misses with every tile and key checked, refusals cost no row, Hard Mode, the 17 keys). Nine planted faults fail. About 75 s with the self-test.
- **Faults fixed:** none. **Left open, not asserted:** equatle-t2-001 (a result of 0, for Jon) and t2-002 (puzzle number off-by-one).
- **Main's run:** 38273086593 (the #294 merge) green first time; Gate on #294 had 51 passed, 2 skipped. Local `check-changed.py` fails site-wide checks only because the container lacks `esprima`, WebKit and the KaTeX CDN.

## 2026-10-12 (cloud): VERIFIERS-20 game 10, shape-shifter (#293, merge commit 8e52e94)

- **Verifier:** `scripts/verify-shape-shifter.py`: 15 translation, 15 reflection and 15 rotation items recomputed from their words (SR-25: dx/dy, axis, turn
  direction; rotation turned here, clockwise (x,y)->(y,-x)); four rotation options, one true, each other a named slip; letters inside their shapes; sessions of all four
  modes dealt 5 times; every vertex of every answer tapped at all 121 grid points and every rotation letter tapped over 8 deals on the real canvas; whole sessions played to 10/10 and 0/10.
  Seven planted faults fail (wrong dx, wrong axis, reversed turn = old r-001, second correct option, wrong feedback letter, y ignored, wrong reflection). About 2 min a run.
- **Main's run:** 38266515892 (the #293 merge) green first time; Gate on #293 had 50 passed, 2 skipped. Local `check-changed.py` fails site-wide checks only because this container lacks `esprima`, WebKit and the KaTeX CDN.
- **Faults fixed:** none. **Expected failure left open:** t3-003 (reflection item 15 is its own image; a replacement is content, SR-26). Not asserted: t3-001, t3-002, t3-004, t3-005.

## 2026-10-12 (cloud): VERIFIERS-20 game 9, new-shapes (#292, merge commit 12c5018)

- **Verifier:** `scripts/verify-new-shapes.py`: all 50 items (15 parallelogram, 20 trapezium, 15 prism) against three formulas held in the verifier; key by `Fraction` from the item's values;
  working steps checked; sessions of 10/20/30 dealt 3 times; the diagram's numbers and accessible description checked in Chromium (SR-25); every item answered on the numpad. Five planted faults fail.
- **Faults fixed:** none. **Left open:** diagram proportions and the prism l arrow (r-001, t3-003/004/005), Jon's call.
- **Main's run:** 38236088363 (the #291 merge) green on its third attempt after two "Initialize containers" cancels (container pull used the 360 s timeout; two of three re-runs used).
  Run 38260101808 (the #292 merge) green first time. Gate on #292: 51 jobs passed, 2 main-only skipped.

## 2026-10-12 (cloud): VERIFIERS-20 game 8, four-quadrant-explorer (#291, merge commit bb79123)

- **Verifier:** `scripts/verify-four-quadrant-explorer.py`: Plot (20), Read (15) and Shape (10) banks recomputed (grid points; read options four distinct, one equal, every
  distractor a sign or order slip; the point drawn at exactly one of 121 grid points; shape key = the missing fourth corner), queues cycle plot/read/shape at 10/20/30, and
  every plot and shape question tapped at all 121 grid points on the real canvas (plus 0.45/0.55-cell edge taps), every read option pressed, in Chromium. Five planted faults fail.
- **Faults fixed:** none. **Expected failures left open:** none (r-001, t3-002, t3-003 stay open).
- **Main's run:** 38233755799 (the #290 merge) green. A runner cancelled one job once ("Initialize containers"); one re-run of the failed job passed.

## 2026-10-12 (cloud): VERIFIERS-20 game 7, formula-plug-in (#290, merge commit d31a12a)

- **Verifier:** `scripts/verify-formula-plug-in.py`: all 50 items against ten formulas held in the verifier (variables, result variable, rule):
  key from the item's own values with Fraction (whole numbers); `formulaKatex` read as maths and worked with the values; every working step has the
  formula's left-hand side and is worth exactly the key; the substitution step uses the formula's numbers plus the values only; last step is
  "LHS = key"; sessions of 10/20/30 dealt 3 times; every item shown by `loadQuestion()` (formula TeX read from KaTeX's annotation, variables line,
  prompt) and answered on the numpad in Chromium (key right; key +-1 and the usual slips wrong, with "the answer is K" and the item's working). KaTeX is
  served from the pinned local copy (`bank_common.serve_real_font`), so it runs offline. Four planted faults all fail the run.
- **Faults fixed:** none. **Expected failures left open:** none (t3-002..006 stay open as before).
- **Main's run:** 38232674780 (the #287 merge) green.

## 2026-10-12 (cloud): VERIFIERS-20 game 6, think-of-a-number (#287, merge commit 25a73bc)

- **Verifier:** `scripts/verify-think-of-a-number.py`: all 50 items (10 one-step, 20 two-step, 20 three-step): each key run forwards with
  Fraction must give the result (every intermediate a whole number from 0 up, key 1-9999) and run backwards must return the key; step
  displays and every `undoSteps` line recomputed; sessions of 10, 20 and 30 (2/4/4, 4/8/8, 6/12/12, no repeats); every item shown and answered on the
  numpad in Chromium (key right; result, key +-1, steps run forwards again, steps undone in the order told: wrong with the recomputed working).
  Four planted faults all fail the run.
- **Faults fixed:** none. **Expected failures left open:** none.
- **Lessons:** (1) #287 was held up by CI-TIMINGS-MEDIAN (home lane #288: timings are now the median of 5 main runs and the timings job
  commits only a pack that passes `--check`; main unblocked, run 791 green). (2) `cloud.md` must stay under 20 KB (context-size check):
  older entries move to `docs/history/handover-cloud-archive.md`. (3) The answer-lock self-test counts the backticked remaining-list line in this
  file: exactly one, so never write that token in backticks in an entry.
- **Main's run:** 38231678130 (the #289 merge) green; game 6's own main run is checked in the game 7 entry.

(Entries for VERIFIERS-20 games 1-5 and the CI stop of 12 Oct are in `docs/history/handover-cloud-archive.md`: #282-#286, all green; the stop was resolved by #288.)

## 2026-10-12 (cloud): VERIFIERS-20 STOPPED after game 5: main's CI is red from the generated timings pack (home-lane item) - RESOLVED

- **RESOLVED 12 Oct:** the home lane's CI-TIMINGS-MEDIAN (#288, d00a818) made the timings a median of the last 5 runs; main's run 791 is green and `ci-groups.py --check` passes. This branch has main merged in; VERIFIERS-20 resumes with #287, then `formula-plug-in`.
- **STOP IF reached:** "main's full run is red after a merge and the fault is not in this lane's files". Main's run 787 (38225600227, the
  merge of #286) failed in 1 minute: the Plan job's `python scripts/ci-groups.py --check` fails with 12 group-budget FAILs
  (Content verifiers 1-4, 19-24, 34, 35 and Answer lock L1, each 81-108% of its budget). The same check fails on plain `main` at
  `ef82d88`, so every open PR is red too (#287's Plan and Gate are red for this alone).
- **Cause:** the automatic "Record CI timings and repack (run 38224711265)" commit `25f887b` (run 785) recorded inflated timings
  (e.g. Growth and Decay 55 s to 94 s, Formula Unlocked 17 s to 28 s, while PR #286's CI ran beside it) and repacked, leaving
  about a dozen groups above 80%. The check passed on main at `0f2f398` (before the repack) and failed from `25f887b`. The timings job
  only runs after a green full run, so main cannot repack itself out: it needs a home-lane commit. `scripts/ci-timings.json`
  and `scripts/ci-pack.json` are generated files outside this lane, so none was edited.
- **For the home lane:** restore the pack (for example revert `25f887b`, or re-record the timings from a quiet run and run
  `python scripts/ci-groups.py --write-pack`), and consider recording the median of several runs so one slow run cannot break the
  check. Note also that each new verifier line counts as 120 s until a main run times it.
- **State of play:** games 1-5 done and merged (#282-#286; main runs 779, 781, 783, 785 green, 787 red for the reason above). Game 6
  `think-of-a-number` is built and passing (`scripts/verify-think-of-a-number.py`, 50 items, four planted faults caught) in PR #287,
  which is merged-ready except for the red Plan/Gate. Games 7-20 not started. Game 6 is off the remaining list in this PR;
  nothing is claimed.
- **To resume:** once main's `ci-groups.py --check` passes again, merge `main` into `claude/verifier-think-of-a-number`, push, merge #287 on
  a green Gate, then continue with `formula-plug-in`.
- **Open for Jon:** delete branches `claude/verifier-prime-or-composite` and the other merged `claude/verifier-*` branches on GitHub (the
  proxy refuses remote deletes).

## 2026-10-12 (cloud): VERIFIERS-20 game 5, prime-factorisation (#286, merge commit ef82d88)

- **Verifier:** `scripts/verify-prime-factorisation.py`: both target banks (28 + 20) factorised by trial division, every prime factor
  on a button (buttons checked to be 2, 3, 5, 7, 11, 13), sessions of 8 different targets, and 4273 taps (ascending, descending,
  one too many, every button, non-dividing taps, seeded random) replayed against a model of the rule in Chromium: lives, product,
  hearts, product line, "T = p x q (+200)", "p is not a factor here!" and the out-of-lives factorisation. Four planted faults all fail.
- **Faults fixed:** none. **Expected failures left open:** none (t3-001..004 stay open as before).
- **Main's run:** 785 (game 4's merge) green.

## 2026-10-12 (cloud): VERIFIERS-20 game 4, factor-race (#285, merge commit 0f2f398)

- **Verifier:** `scripts/verify-factor-race.py`: the 20 Year 6 pairs (numbers 1-50, counts differ, no repeat, sessions of 10) and the
  KS3 table (`VALID_PAIRS`, 2694 pairs) rebuilt independently and compared as a set; 20,000 draws all inside it; every Year 6 pair and
  539 KS3 pairs answered by both cards and by time-out in Chromium (mark, card styles, "a has X factors; b has Y.", labels). Four
  planted faults all fail the run. Divisors are counted by the verifier's own loop, never the game's `getFactors()`.
- **Faults fixed:** none. **Expected failures left open:** none (t3-001..004 and f1-001 stay open as before).
- **Main's run:** 783 (game 3's merge) green.

## 2026-10-12 (cloud): VERIFIERS-20 game 3, percentage-flip (#284, merge commit c2f9d86)

- **Verifier:** `scripts/verify-percentage-flip.py`: both static banks (12 default + 20 Year 6): every key from the question's own
  P and N, every figure in every working line (seven shapes; an unknown shape fails), five deals per level, and each item
  answered right and wrong (key, key +-1, +-0.5, a tenth, ten times, the complement) through `checkAnswer()` and `flipCard()`
  in Chromium. Four planted faults all fail the run.
- **Faults fixed:** none. **Expected failures left open:** none (f1-001 phone fold stays open as before).
- **Main's run:** 781 (game 2's merge) green. Game 3's own main run is checked in the game 4 entry.

## 2026-10-12 (cloud): VERIFIERS-20 game 2, fraction-equivalence (#283, merge commit 69a2003)

- **Verifier:** `scripts/verify-fraction-equivalence.py`: the Year 6 bank (20 pairs) and the generator (20,000 draws in
  Chromium, every multiplier 2-6 and offset 1-3 reached); every key and cross-multiplication line recomputed with Fraction;
  every bank pair and 400 draws answered YES and NO through `guess()`; Year 6 sessions checked. Four planted faults all fail.
- **Faults fixed:** none. **Expected failure left open (for Jon):** `fraction-equivalence-v20-001` (LOW): Year 6 bank items
  12 and 18 are one question written both ways round, so 19 different pairs; replacing one is new content (SR-19). The
  verifier names it and fails on any other repeat. t1-001 (20 items) and f1-001 (phone fold) stay open as before.
- **Main's run:** see the next entry.
- Branch `claude/verifier-fraction-equivalence` deleted locally; GitHub branch `claude/verifier-prime-or-composite` is still
  on the remote (proxy refuses deletes): listed under Open for Jon. Squash merges mean `git branch -d` refuses, so the
  local branch was removed with `-D` after confirming the PR was merged.

## 2026-10-12 (cloud): VERIFIERS-20 game 1, prime-or-composite (#282, merge commit cdd29ff)

- **Verifier:** `scripts/verify-prime-or-composite.py`, all 66 numbers: key by trial division (SymPy cross-check), every hint
  claim, every explanation (first three divisors, ellipsis rule), each number marked both ways through the game's buttons in
  Chromium, five deals checked (whole bank once, 6 then 7 first). Five planted faults all fail the run.
- **Faults fixed:** none found. **Expected failures left open:** none (t1-002, hints give the answer away, MEDIUM, is not a
  key fault and stays open as before).
- **Main's run:** 779 (38218891574) green.
- **Container note for the next session:** the cloud container has no `esprima`, no WebKit and no KaTeX CDN, so
  `check-changed.py` shows environment failures (B11, calculator, answer-lock parts, teacher feedback) that CI does not.
  Python needs `pip install playwright==1.63.0 sympy mpmath`, and Chromium 1194 through scratch symlinks named 1243.
- **Open for Jon:** delete branch `claude/verifier-prime-or-composite` in GitHub (the proxy refused the remote delete).

## 2026-10-11 (cloud): RK-STICKY-NOTE, The Rightful King's passcode note says no key repeats anywhere (Jon's play-test)

- **Why:** "NEVER THE SAME KEY TWICE" read as "not twice in a row" gives 8 × 7 × 7 = 392, not the key 336.
- **room.js:** the sticky note now reads "ADMIN PASSCODE: {{pc.L}} KEYS, NO KEY USED MORE THAN ONCE." (the count is
  still the token; every variant has L = 3). The miss feedback quoted the old note ("the note says never the same key
  twice"), so it now quotes the new one. Answer, variants and key counts unchanged.
- **teacher.html:** the clue map's line for the note matches, and "Running it" gains the 392 misconception
  (k × (k − 1) × (k − 1)). The teacher page has no per-lock field for a second misconception, so it goes in the notes.
- **Left as history:** `docs/lock-bank-batch9.txt` line 21 and the draft still carry the old wording.
- check-escape-rooms passes; the teacher page in Chromium shows the new wording and 392, none of the old.

## 2026-10-10 (cloud): UPDATES-WEEKEND, /updates/ October entries (Jon's wording, checked against main)

- **DONE.** #272 merged 10 Oct (d96aeb2); main's run 758 is green.
- **First pass stopped** (STOP IF): four claims differed from the code. Library Jam "our first ★ Warm-up room"
  (Comic Caper and Kiln Disaster already are) and Bibby fining the class (the library system does); calculator five
  games, not six (Growth and Decay, #239); Boolean Blitz "no longer than the simplest form" (AB + BC is longer than
  B(A + C); #227); Wrong on the Internet "spinner" (a roulette wheel and two independent events; #223). Minor: Your
  Scores is a section of /leaderboards/ (#238). **Jon approved the proposed wording for all five (23:00+).**
- **Jon's rulings:** Rightful King topic "repeated percentage decrease" (each minute takes a percentage of what is
  left); rooms go before Car Trap, as #271 has them (newest first).
- **Done:** New gains stars (#253), calculator (#239, #261, #264-#267) and scores (#238) after Car Trap; Corrected
  gains Boolean Blitz (#227), 2C (#225), 2B (#226), Wrong on the Internet (#223) at the top (newest first).
- **Rooms:** #271 merged while #272 was open (main run 755 green), so the two room lines #271 added are replaced
  with Jon's approved text, in #271's placement (before Car Trap). The interim home.md note is removed (the cloud
  lane's own addition; home.md otherwise as main). Log Laws: no fix merged, item left out.

## 2026-10-10 (cloud): LIBRARY-JAM-BUILD, The Library Jam built behind its holding page (for Jon's play-test)

- **Jon can play-test it at `/escape-rooms/library-jam/play.html`** once the PR merges (noindex, unlinked, analytics
  off). `index.html` is a noindex holding page and `teacher.html` the real teacher page. No hub card until release.
- **The stop and Jon's ruling (10 Oct):**
  - `keep()`'s end-of-travel rule rejected every keypad answer under 400.
  - **Jon: exempt every keypad, in this PR.** `keypad(n)` now returns a `Keypad` range, and `keep()` skips that
    rule for it. Prom's, Heatwave's and Kiln's keypads use `keypad(n)` too.
  - **Proof:** every other room's room.js and all 34 existing libraries in variants.json are identical to main's.
  - Lock C also has `minsep=1` (answers only have to differ, the draft's rule); the default spread of 5% of 0-9999
    kept one set.
- **Locks (bank batch 10; unique: 3, 143, 54).** Each library is the draft's own sets:
  - `dewey-sort-arm`: grade 2, ordering decimals; eight shelves, spread off.
  - `deflector-straight-line`: grade 1, angles on a straight line; eight angles, five-degree spread.
  - `fines-pence-to-pounds`: grade 2, pence to pounds with no calculator; ten sets on maxDigits 4.
  - **★ Warm-up derived** (grades 1–3). No `levelLabel`: Jon agreed, the stars replace it.
- **check-escape-rooms:** library-jam VALID **572 of 640**, variant 0 VALID (the draft's figure).
- **The teacher page at 320 px:** 538 px here (`table.tt`). It is allowlisted under §1.37 like the other ten (Jon);
  if CI measures differently, CI's figure goes in.
- **Played headless (three random draws and variant 0, all PASS):**
  - The start screen shows ★ WARM-UP · GRADES 1–3.
  - 8 objects and 3 briefs on screen, every token filled.
  - The wrong lines come in order, then the last repeats, Jon's line 3 among them. Each misconception gives its
    response.
  - On variant 0, **5400 on the real keys shows "5400" with no empty slots and gives the named misconception; 54
    opens.** Then the win screen ("They were here all along").
  - A time-out ends on the stakes. No errors, no 4xx, nothing sent to analytics.
  - The teacher page shows ★ only, no "Suits a top set", and the no-calculator note.

## 2026-10-10 (cloud): RIGHTFUL-KING-BUILD, The Rightful King built behind its holding page (for Jon's play-test)

- **Jon can play-test it at `/escape-rooms/rightful-king/play.html`** (noindex, linked from nowhere, analytics off).
  `index.html` is a noindex "coming soon" holding page; `teacher.html` is the real teacher page (noindex, unlinked).
  There is no hub card, sitemap entry or count change: the release contract brings those, with the ★★★ chip.
- **Art pending:** no `art` field, so no picture is requested. Jon generates the three pictures after his play-test.
  The alts are the draft's.
- **Locks (bank batch 9, `docs/lock-bank-batch9.txt`; check-lock-bank: unique on all three):**
  - `admin-passcode-product-rule`, grade 6: the product rule with no repeats (Higher). maxDigits 3; k = 5 to 9 with
    L = 3 (60, 120, 210, 336, 504); variant 0 is k = 7.
  - `vote-log-overwrite`, grade 5: building powers of one multiplier, the method #253 graded 5 in Prom (the draft
    said 7). The library is the draft's ten sets, each through the rules, including (1 - f) x 100 not a multiple
    of r. The generator asserts that the 3 d.p. powers keep their comparison with the threshold.
  - `leak-audit-conditional`, grade 7: conditional probability from a Venn diagram (Higher). The library is the
    draft's seven sets, under its story rules.
- **Derived rating, from check-escape-rooms' own `room_rating()`: ★★★ Challenge (grades 6–9).** No grade was fitted.
- **check-escape-rooms:** rightful-king VALID **215 of 350**, variant 0 VALID (the draft measured 183 of 280; the
  fifth passcode set adds draws).
- **The old URL:** `it-vengeance/index.html` is a noindex meta-refresh to `/escape-rooms/rightful-king/` with a
  plain link (ruling 6). `it-vengeance/room.js` and `teacher.html` stay as history. The checker reads every room
  folder; a noindex index makes it not live, so it needs no card or grade.
- **Played headless (scratch script, four draws, all PASS):**
  - Start screen: the brief, ★★★ CHALLENGE · GRADES 6–9, and the stakes after "If you get it wrong."
  - All 8 objects and all 3 lock briefs on screen, every token filled.
  - Four wrong lines in order, then the last repeats. Each misconception gives its own response.
  - All three locks open; k = 5's 60 opens on the up-to-three-digit keypad. Then the win screen ("It was my
    prompt").
  - A time-out ends on the stakes after "And so:".
  - No page errors, no 4xx, nothing sent to analytics.
  - The teacher page shows ★★★, "Suits a top set" and the calculator note. The old URL lands on the holding page.
- **Generator:** run through a scratch wrapper that swaps in this checkout's paths. Before the M block went in, a run
  reproduced every existing library byte for byte.
- **Teacher page at 320 px:** 558 px wide (`table.tt`, the shared overflow, todo §1.37). It is allowlisted in the
  same form as the other nine teacher pages, per Jon's CAR-TRAP-ONE-LANE contract; §1.37 (`engine.css`, home lane)
  stays the real fix for all ten. LIBRARY-JAM-BUILD's teacher page got the same entry (#262).

## 2026-10-10 (cloud): LIBRARY-DRAFT, Library room draft for Jon's review

- **The draft:** `docs/escape-room-drafts/library-draft.md`. It has three title options; **Jon chose The Library Jam
  (10 Oct)**, slug proposed `library-jam`, every slot, three locks with libraries (8, 8 and 10 variants), the alts, hub and meta lines,
  and the checklist. Jon's line is wrong-entry line 3, verbatim. No art prompts.
- **For Jon 1, the big one: lock C needs a keypad that takes "up to four digits", and the engine's keypad takes
  exactly `digits`** (`engine.js:610`, and `:593` drops extra digits). A four-digit keypad shows four slots, which
  steers a student to 5400, the misconception. A two-digit keypad turns a typed 5400 into 54, right by accident.
  Rightful King's lock 1 hit the same limit, so the fix is shared: an opt-in variable-length keypad in `engine.js`
  (home lane), plus the generator's `keep()` edge rule for keypads. Recommended before phase 2.
- **Measured (scratch):** the checker's own `draw_is_valid()` on the draft's clues gives **572 of 640 VALID, variant
  0 VALID**. Fines are multiples of 5p, to stay non-calculator (For Jon 6).

## 2026-10-10 (cloud): RIGHTFUL-KING-DRAFT, Rightful King draft for Jon's review

- **The draft:** `docs/escape-room-drafts/rightful-king-draft.md`. It has every slot `room.js` needs, three new
  locks with proposed libraries, bank entries, the teacher-page line, and the checklist (all pass). No art prompts.
  Its "For Jon" list has 14 items. The ones that change the contract's maths:
  - **Lock 1:** the example sets 60, 24, 42 can't go on a three-digit keypad (the engine wants every digit; no
    leading zero). The only all-three-digit sets with L >= 3 are k = 6 to 9, L = 3, so the library is 4 (120, 210,
    336, 504). Variant 0 is k = 7 (210), because 120 collides with audit set 0's 120 voters.
  - **Lock 2:** where r divides (1 - f) x 100 exactly, a strict linear reader lands one minute later. For 25 with
    a half that is the right answer, so the misconception scores. Proposed: reject those sets. Whole-number r from
    5 to 40 gives 10 variants; the lock needs a calculator.
  - **Lock 3:** the set 150, 70, 50, 60 prints its own answer (60). Proposed story rules: he has 30-60% of the
    vote, P(him | saw it) is at least 20 points above P(him | didn't), and S is not 100. The library is 7.
- **Measured (scratch, nothing committed):** `check-lock-bank.py` says unique on all three bank entries. The
  checker's own `draw_is_valid()` on the draft's clue strings gives **183 of 280 VALID, variant 0 VALID**.
- **STOP IF did not fire:** prom-budget was read in full and never mentions a vote, a king or Narry.
- **Next:** LIBRARY-DRAFT. Phase 2 of The Rightful King is a separate contract after Jon approves.

## 2026-10-10 (cloud): CAR-TRAP-BUILD, the rewritten Car Trap built behind its holding page (awaiting Jon's play-test)

- **10 Oct, after ART-PENDING (#244): rebased on main; `art` dropped.** The room requests no picture.
  check-escape-rooms lists it as art pending (VALID 352 of 512). Tier 1 passes the play page, and
  `test-escape-art.py` passes.
  - **Still red, one failure:** the teacher page is 545 px wide at 320 px. This is the shared `table.tt` overflow
    (todo §1.37). **Jon (10 Oct): the home lane fixes §1.37 first; no allowlist entry.** #242 waits for that.
  - **Jon's message of 10 Oct ("the Car Trap art is now on main; set art to those pictures; rewrite winAlt for the
    win picture's high CCTV-style view") did not match main.** The only `car-trap-*.webp` on main are the OLD
    pictures: an orange sports car reversing into a VISITOR bay before a crowd of staff, an eye-level view. Main is
    unchanged in `docs/art/` since before #242, and home.md names no new files.
    - So `art` was NOT set and winAlt was NOT rewritten: pointing at those would show the wrong premise, and an alt
      cannot be written for a picture not seen.
    - When the new files are on main: add `art:` naming them, check all three alts against them, and rewrite winAlt
      for the win picture's view.

- **Built from the approved draft with Jon's changes (9 Oct, 22:53).**
  - "The dullest car in the county" appears once, in the hook (scripted count: 1).
  - The stakes and lock 3's onOpen are as ruled.
  - Wrong-entry line 1 carries the figure in words.
  - The only figures in the prose outside tokens are the draft's flagged words and locks 2 and 3's unchanged method
    constants. Mr Strictman is invented, Jon confirmed.
- **For the difficulty contract: the room is ★★ Core** (Jon's ruling 3). No star field or label was added anywhere.
- **Lock 1, `head-bay-lower-bound`, is bank batch 8** (`docs/lock-bank-batch8.txt`; check-lock-bank `unique (2.35)`).
  - Its library is in `gen-escape-variants.py`: the draft's eight widths, variant 0 = 2.4, the draft's solver, all
    eight kept.
  - The generator also writes the room's `variants:` blocks.
  - `visitor-space-bounds` leaves the room; its bank entry and library stay as history.
  - Locks 2 and 3: a scripted diff shows id, key, instrument, variants, missTitle, hints and solve unchanged. Only
    framing and missSays' last clause changed, per the draft.
  - **check-escape-rooms: car-trap VALID 352 of 512, variant 0 VALID**, as the draft measured.
- **The generator's paths are Jon's machine's** (`E:\jon\maffsgames\...`). The cloud lane runs it through a scratch
  wrapper that swaps in this checkout's paths at run time; the script's paths are unchanged.
  - Before the new library went in, a run reproduced every existing library byte for byte.
  - Only car-trap's room.js and variants.json changed.
- **Art pending.** `art: 'car-trap-v2'` has no files yet, so the engine drops the frame and none of the six old pictures
  shows (they stay in docs/art/ untouched). No lock has art or missArt (the rule is in room.js's header).
  - **Filing Jon's three pictures is a separate step:** file them as `car-trap-v2-scene`, `-fail` and `-win.webp`, or
    file over the old names and set `art` back to `car-trap`.
  - The three alts are the draft's, to be checked against the pictures before release.
- **Pages (Jon's answers, 10 Oct):**
  - `teacher.html` is the real teacher page (noindex, unlinked).
  - `play.html` is the play-test page: noindex, linked from nowhere, analytics off (no gtag, no analytics.js, so the
    engine sends no events).
  - `index.html` stays the holding page.
  - **At release, in one PR:** play.html's content becomes index.html, with prom-budget's head lines (analytics, meta,
    og:) put back; play.html is deleted; then the §5c release steps.
- **Played through in Chromium** on serve-stubbed, with no page errors and nothing sent off-origin.
  - It shows every object and all three lock briefs on screen.
  - The four wrong-entry lines arrive in order, then the last repeats.
  - Each lock's misconception gives its own response.
  - All three locks open on their answers; lock 1 is set by the slider's arrow keys.
  - Then the win screen; a second play times out to the stakes after "And so:".
  - The teacher page follows the draw. The cloud session cannot open Jon's Chrome: that is what play.html is for.

## 2026-10-09 (cloud): PD-CLOSE, LISTED-HIGH item 12 closed (Jon's ruling, 22:45, option A)

- **t4-002 closed by #232 (shared-overlay fix); covered by the OVERLAY-KEYS CI check; per-game check not added
  because the fault was in shared code.** The check is `scripts/test-initials-overlay.py` (in CI). Measured 9 Oct, with
  `--games prisoners-dilemma`: main passes, and its plant is caught. Run `--against` the pre-#232 overlay, it fails
  with 55 keys reaching the game's document keydown. That confirms the check covers this game, so the STOP IF did not fire.
- `verify-prisoners-dilemma.py` is **not** in CI. Its branch, `claude/youthful-feynman-anpxuq-pd-check`, had nothing in
  its handover that main lacks. It was deleted locally, but the remote delete was refused (the sandbox proxy, HTTP
  403), so **Jon deletes it in GitHub's branch list**.
- **prisoners-dilemma-t4-001** (the leaderboard ranks the chosen opponent) stays open for Jon's design decision.
- Jon's note is saved verbatim as `docs/history/contracts/2026-10-09-listed-high-note-2245.md`.

## 2026-10-09 (cloud): CAR-TRAP-DRAFT, Car Trap draft for Jon's review (#235 merged ba5b6b2; main run 661 green)

- **Contract:** the repo copy on main, `contracts/2026-10-09-car-trap-draft.md` (Jon's amended text of 16:45, saved
  verbatim by the home lane in dc43926 and merged in #221). It is left where it is, because the home lane's handover
  points to that path; it moves to `docs/history/contracts/` with phase 2.
- **The draft:** `docs/escape-room-drafts/car-trap-draft.md`. It has every slot `room.js` needs, the three art
  prompts, lock 1's variant proposal and bank entry, and the checklist (all pass; two figure exceptions in words,
  both flagged). Its "For Jon" list has 11 decisions, including:
  - **There is no `fail` slot.** The engine shows `stakes` after "If you get it wrong." (`engine.js:238`) and after
    "And so:" on time-out (`:791`), so the Fail is written into `stakes`.
  - **`hook`, `brief` and `stakes` are written raw**, so they can't hold tokens.
- **Lock 1 (`head-bay-lower-bound`, proposed):**
  - W 2.2 to 2.9 m to the nearest ten centimetres; slider 2.00 to 3.00 m, step 0.01; answer W - 0.05; miss the
    stated W.
  - Scratch checks, not committed: `check-lock-bank.py` "unique (2.35)", and all 8 variants pass the generator's
    `keep()` rules.
  - Joint draws by the checker's collision rules: 352 of 512 VALID with the precision in words, 184 with a numeral
    10.
- **Next (phase 2, a separate contract after Jon approves):** the generator block, a lock-bank batch entry,
  `room.js`, `teacher.html`, the art and the release. STOP IF did not fire: no brief/rule clash the draft couldn't
  resolve, and lock 1 has exactly one settable answer in every variant.

## 2026-10-09 (cloud): PD-CHECK (LISTED-HIGH item 12) STOPPED for Jon: #232 fixes t4-002; the saved check is wrong

- **#232 (OVERLAY-KEYS) is on main** (9a0830f, merged 18:46 UTC, before #229; main green, run 654). The pd-check
  branch already contained it: no rebase needed.
- **The saved check FAILS on main** (both cases): STOP IF fired. **But the cause is the check, not the game:** it builds
  its own `<div id="mfg-initials-overlay">`, which #232's listeners (bound to the overlay that `askInitials()` creates)
  never touch; and its "dd typed into a text field" case has no counterpart in this game (prisoners-dilemma has no
  input, textarea or contenteditable; the overlay's inputs are the only text fields it ever shows). Both were written
  for the discarded in-game guard.
- **Measured, real path (scratch probe, not committed; no game code changed):** a tournament in Chromium, match 1
  played to its end with C, the real overlay opened by `submitScore`, match 2 ready, "CDC" typed into the overlay.
  Main's overlay: round 0 -> 0, nothing played, the overlay holds "CDC"; C plays a move after Skip. The pre-#232 overlay
  (`6642c82~1`): round 0 -> 1, a move played, the overlay holds "DC" (the first initial went to the game).
- **Already in CI:** #232's `scripts/test-initials-overlay.py` opens the real overlay in prisoners-dilemma, types a-z
  (so C and D), and fails if any game key listener sees a key: stronger than "no move played". It names
  prisoners-dilemma among the 11 games whose shortcuts fired before the fix.
- **For Jon (recommendation A):** close t4-002 citing #232 and `test-initials-overlay.py`; retire the saved check (no
  PR, no new CI line). The bug was a shared-layer bug, fixed and tested there across 97 games; a per-game copy would test
  a weaker property of the same code. **B:** rewrite the check on the real path above (the probe, as a verifier;
  self-test serves the pre-#232 overlay and must FAIL), drop the text-field case, wire it in, close t4-002. Either way
  the text-field case goes: no such field exists in this game. **t4-001** stays open (SR-22, Jon's leaderboard).
- Branch `claude/youthful-feynman-anpxuq-pd-check` left as it was (its check unchanged, no PR).

## 2026-10-09 (cloud): LISTED-HIGH (complete; contract in `docs/history/contracts/2026-10-09-listed-high.md`)

One PR per game, in the contract's order; each next game's claim is a commit of its own at the end of the previous
game's PR (so it reaches main before that game starts). New verifiers go in **B2** (main run 595: 249 s of its 360 s
budget; E is at 491 s and takes nothing new).
- **1 surd-simplifier: #210** (claim #209). t1-001 keyed sqrt2 (sqrt2.sqrt2 kept as the value-2 distractor;
  8sqrt32/32 removed, so no B11 allowlist entry was needed), t1-002 keyed 206/495. New `verify-surd-simplifier.py`
  (B2, ~15 s): every stem read as TeX and compared with its key in SymPy, keys in simplest form, every option
  clicked; fails main's page on both. No other key differed.
- **2 52dle: #211** (claim rode #210). Guesses marked by the shared `MaffsAnswer.exact` on the raw text (answer.js
  loaded), never `parseInt`. The pi hint "100 × π rounded to 2dp" read as 314.16; it now says "100 × (π to 2 d.p.)"
  (an unambiguous key/word clash in the finding's own puzzle: fixed here, per the STOP IF). New `verify-52dle.py`
  (B2, ~4 s): every number recomputed from its clue and hints (FACTS), 7 guesses per puzzle typed in Chromium.
- **3 scale-factor-scaling: #212.** The paint item states the original surface (10 m², 1 litre); key 4 litres (its
  text "4 litres per 10 m²" contradicted the stem's rate; the value is kept). New `verify-scale-factor-scaling.py`
  (B2, ~2 s): every key from the quantities its prompt states. Seen, not touched (B11's domain, not this finding):
  T1[8] offers 2:5 and 4:10, T1[9] 1:3 and 3:9, wrong options equal to each other.
- **Main went red after #211 (run 601): group E at 9m04s of its 9m budget**, none of this lane's verifiers in it.
  Jon (9 Oct): the cloud lane adds E2 now, on a branch of its own: **#213** (`claude/youthful-feynman-anpxuq-e2`,
  merged 63ad521) moved Screening Room, Simultaneous Solver and Terrible Advice into E2; E 4m31s, E2 4m22s on its
  run; main green again (run 37950120068). E's job name still lists two moved verifiers (names kept stable): the
  home lane's call.
- **Jon's rulings of 9 Oct, 16:21** saved beside the contract (`docs/history/contracts/2026-10-09-listed-high-rulings.md`):
  item 9 t4-003 is NOT rewritten: "Yes - but only when k > 0" is accepted alongside the key (an accepted set, in
  the game), the explanation says why both are right; the rest as written.
- **4 coordinate-geometry-dash: #214.** x = 3t, y = 4/t: options xy = 12 (key), xy = 7, y = 12x, x = 3y/4. New
  `verify-coordinate-geometry-dash.py` (B2, ~4 s): all 45 keys recomputed, equations compared as curves.
- **5 complex-converter: #216** (#215 was the home lane's RULINGS-9OCT). The contract's "apply it to every item" taken literally: the target line states
  the range on every polar and exponential question; ids 20, 28, 30, 38, 53 keyed principal (same numbers; ids 20,
  28 and 53 said "positive angle", which went); a second form of the key removed from ids 20, 21, 28, 40, 48 (40
  and 48 had a negative-modulus twin); argDeg/argRad principal everywhere (Triples' cards). New
  `verify-complex-converter.py` (B2, ~5 s, KaTeX from the CDN): every option read as a complex number. Also closes
  t6-002 and t6-003 (the ids 40/48 twins, MEDIUM jc). **Lesson (CI red once on #216): a fixed B11 pair must leave
  `data/check-ledger.json` in the same PR** (tier 4 fails a stale entry); run `extract-banks.py --only <slug>` then
  `check-banks.py --ci --only <slug>` before pushing (esprima: pip build fails here; unpack its sdist on PYTHONPATH).
- **6 higher-power: #217.** Pairs matches by value (`sameValue`). New `verify-higher-power.py` (B2, ~2 s).
- **Jon, 9 Oct (answer to a question, item 11): Boolean Blitz marks an option right when it has the key's truth
  table AND no more literals than the key** (AB + BC, AB + AC accepted; the t6-004 unsimplified forms such as
  A·B + A for A stay wrong; t6-004 untouched). Boolean-blitz has B11 ledger entries for t6-002/003: clear them.
- **7 seven-bridges: #219, merged 5926c24.** al_15's E to (300,150); t4-001 fixed by F1 batch 9 (closed with
  measurements). **Jon's rulings, 9 Oct 18:03 (addendum, folded into #219):** al_10, al_18, al_21's grazing edges
  fixed (each layout mirrors its own other half; edges unchanged); `CLEAR` 28 px (current vertex r 24 + 2 px stroke
  + half a 4 px edge; grazes were 19.8-21.1 px, next edge 28.1 px), no exemptions. **complex-converter ids 20, 28, 53
  stay on the principal range (-pi < arg z <= pi), as merged in #216: no change.** Main's #217 run went over budget
  in B4 and L2 (no test failed); one re-run passed.
- **8 wrong-on-the-internet: #223, merged 4094b01** after main went green on #224 (run 37969653160). The wheel is
  stated (European, single zero; key 18/37) and A and B are said to be independent in their post.
- **9 core-maths-paper2c: #225.** Q12 stem opens "f is a quadratic."; Q35 `accept: [1, 3]` (Jon 16:21): selectAnswer
  marks against `q.accept || [q.correct]`, the lock hint picks outside it, the working says why both "Yes" are right;
  t4-001 fixed by F1 batch 10. New `verify-core-maths-paper2c.py` (~25 s).
- **10 core-maths-paper2b: #226** (stacked on #225, on its own branch so CI runs while #225 waits; Jon, 18:56: one
  PR each). Q28 option D is "Neither — both premiums cost more than the expected loss" (false: the data breach
  premium, £900, is below its expected loss, £1,000). New `verify-core-maths-paper2b.py` (~5 s).
- **11 boolean-blitz: #227** (stacked on #226). Marked in the game (boolParse, minSopLiterals, sameAnswer): right =
  the key's truth table AND literals <= max(the key's, the minimal SOP's) (Jon's two answers of 9 Oct). Only Q24's
  AB + BC and Q41's AB + AC are accepted beside a key; the verifier fails any other (Jon, 18:56). t6-001 fixed by F1
  batch 11. The B11 ledger entries stay (options unchanged; Jon agrees). Locally the bank lint cannot extract this
  bank (KaTeX CDN; main's page fails the same way): CI judges it.
- **13a characteristic-quest t6-001: #228** (stacked on #227): closed with measurements, no code change.
- **13b eigenvalue-extractor t6-001: #229** (stacked on #228): closed with measurements, no code change.
- **13c matrix-crunch t6-001, t6-002: #230** (stacked on #229): new `verify-matrix-crunch.py` (~40 s, both levels,
  the flag path check-answer-lock never presses); fails the pre-batch page with the audit's numbers.
- **13d formula-forge t4-001: #231** (stacked on #230): closed with measurements, no code change. **LISTED-HIGH is done
  but item 12** (held for OVERLAY-KEYS); the remaining list is empty.
- **CI (CI-BALANCE, #220):** groups are packed now. A new verifier's header is `# ci-line: <label> | <args>` (no
  group id); untimed lines get a group each until main's timings job records them. `ci-groups.py --check` locally.
- **Local checks used for each PR** (the sandbox cannot reach the KaTeX CDN): check-changed's plan, the answer lock for
  the changed game with KaTeX served locally, and `extract-banks.py --only <slug>` + `check-banks.py --ci --only
  <slug>` (stale B11 ledger entries must leave `data/check-ledger.json` with the fix). esprima: unpack its sdist on
  PYTHONPATH. Teacher-line fails locally on factor-theorem and log-laws only (KaTeX CDN): not a change's fault.
- **Item 12, prisoners-dilemma t4-002: waiting on the home lane's OVERLAY-KEYS (#232)** (Jon, 18:56; note in
  `docs/history/contracts/2026-10-09-listed-high-note-1900.md`). The drafted in-game keydown guard was **discarded**, in no PR: it
  was the defensive-patch shape (the shared initials overlay lets typed keys reach page shortcuts in every game with a
  document keydown handler; the overlay is the fix). **The check is saved on branch
  `claude/youthful-feynman-anpxuq-pd-check`** (`scripts/verify-prisoners-dilemma.py`, verbatim from the scratchpad;
  no PR, not in CI: it fails main until #232 is on main). It asserts, on a tournament's first match in Chromium: C
  pressed on the game screen plays a move; "CDC" typed into the initials overlay (`#mfg-initials-overlay`, an input
  focused in it) plays nothing; "dd" typed into any other text field plays nothing. **When #232 is on main:** run it
  against prisoners-dilemma with no change to the game's code; it must pass. Its self-test plants the discarded
  in-game guard, so it reports CANNOT PLANT: rewrite the plant to serve main's pre-#232 overlay module (the shared
  file's old content) and confirm it FAILs, update the `ci-line` header to the packed form (`# ci-line: <label> |`),
  then open the PR (claim prisoners-dilemma first), closing t4-002. **t4-001** (the board ranks whichever opponent is
  chosen) stays open: Jon's leaderboard design, not this lane's.
- **Stacked PRs (Jon's ruling, 9 Oct 20:20): one branch per PR, stacked, is fine.** #226-#231 were each on
  `claude/youthful-feynman-anpxuq-<game>`, opened together so CI ran in parallel, merged strictly in order, each on a
  green Gate with main green on the previous merge.

## 2026-10-09 (cloud): FT-FIX, factor-theorem (fix #207 merged cf96929; main run 593 green)

- **For the home lane, CI, before the next E verifier lands:** main's run 593 put group E at **8m39s of its 9m00s
  budget** (12 min timeout). Factor Theorem now takes 69 s there (its option, level and Next checks and 8 plants);
  Screening Room 89 s, Simultaneous Solver 73 s, Terrible Advice 57 s, Linear Equation Solver 52 s. The B1, B3 and B4 jobs
  took 5m00s to 5m23s (setup included; their budget is 6 min), so moving one verifier only moves the pressure: a new group (E2 or B5) in
  `scripts/ci-groups.py`. The cloud lane left E as it is.
- **Answer buttons (answers 1):** Q33 ("Which line proves it?") and T9(c) are four shuffled buttons each, the
  contract's lines, marked by `dataset.val` on Check or Submit (with T9's other parts); the explanation shows after
  marking. All in the game (`fillOptions`, `chosenValue`, `markOptions`, `.opt-*` CSS); the lock hint picks a button.
- **A-Level only (answers 2):** the page never reads `?level` (a comment says so); every URL logs and submits
  `alevel`. No start screen, no level4 board. **For the home lane, at relisting: remove L4 from Factor Theorem's
  roster row, the portal filter and the spec map.** With no open CRITICAL or HIGH after this PR, it is ready (SR-21).
- **Practice submits nothing** (t5-014, t5-015); its device-local score-history record went with it (nothing reads
  `MaffsScoreHistory.get`). The Test alone submits, once, to `factor_theorem_alevel`.
- **A wrong answer waits on `MaffsNext`** (t5-018's note; next-control.js loaded); a right one keeps Next Question.
  t5-018's other parts were already fixed on main: closed with the measurements.
- **`scripts/check-teacher-invite.py` (answers 3):** one line added to FT_STEP (choose a button in any unanswered
  `.opt-group`); nothing else changed. Its factor-theorem routes reach both end screens at 390 and 1280 (KaTeX served
  locally: the sandbox cannot reach the CDN). check-answer-lock seeds 1-3 PASS the same way.
- **Verifier** (group E): the option checks (Q33's working for every n; T9(c) from s, v and a), prose keys, the five
  ?level URLs, no Practice submit, MaffsNext on a wrong answer; 8 plants, all caught. About 80 s with its self-test.
- **Still open, not this lane's:** t5-008 (home lane, VOCAB-IDEMPOTENT), t5-016 and t5-017 (a Test bank of 40 from
  Project Claude, a separate contract).

## 2026-10-09 (cloud): FT-FIX stopped before building (contract STOP IF; answered 11:00, above)

- **STOP IF fired: "the game's selection pattern can't serve a 4-option item inside a multi-part test question
  without engine changes".** factor-theorem has no selection pattern at all: every Practice item and every Test part
  is a typed box (no options, no `dataset.val` anywhere). Engine changes needed, all in the game: an item or part
  with `options` renders four buttons (shuffled, `data-val` the option's text) in place of its box; choosing one
  marks it chosen; Check (Practice) or Submit Answer (Test, with the other parts) marks `dataset.val` against the
  key; one attempt, as the typed tier-5 items. Self-contained, about 40 lines. Recommended.
- **Also unexpected, for Jon:** the game has **no start screen**. It opens on Learn, with Practice and Test as
  tabs. Step 5's "an absent or unknown key shows the start screen (level choice)" needs a new one. Proposal: a
  level choice (A-Level, Level 4) shown instead of the tabs until a level is chosen; a valid `?level` skips it;
  the top bar's badge shows the chosen level. Design addition (canon §0.3 "still stops").
- **Both changes break a shared check the cloud lane may not edit:** `scripts/check-teacher-invite.py` (site-wide,
  every PR) plays factor-theorem with no `?level`, clicks the Practice tab and fills `input.answer-input` boxes
  (FUNCTION_ROUTE, FT_STEP). Additive fix: a `("click", '[data-level="alevel"]')` step first in both routes, and
  FT_STEP choosing the first option in any unanswered option group. Jon authorises it in the FT-FIX PR (as the
  foundation-s5 lines), or the home lane lands it first. check-answer-lock needs nothing shared: the game's own
  lock hint can name `"level": "alevel"`.
- **t5-018 is fixed on main already** (Chromium, 390x844, this session): T5 and every Test question 390 px wide;
  Learn at 390 and 320 px; no literal `___` and no `<span` in any attribute; `question_index` is `qIdx + 1` in
  both modes; hint button off after marking; Enter checks. Left: its "wrong-answer advance not MaffsNext" note.
- **For Jon (the rule recorded with SR-16 to SR-20):** "a level that serves another level's items is not listed as
  that level". Step 5 has Level 4 serve A-Level's content (the page has no separate Level 4 content); relisting it
  at L4 would fall under that rule. The home lane's relisting decides.
- **Did not fire:** Q33 and T9(c) match the quoted text; `question_index` needs no change; a `level4` board needs
  no hub or coverage change (factor-theorem is in NOT_ON_HUB; the module labels `level4` "Level 4").

## 2026-10-09 (cloud): UC-T4-007, unit-converter (claim #204; fix #205 merged 920c5b1)

- **The fix (Jon's answer 3c):** the 60 mph item reads "Convert 60 mph to m/s (1 mile ≈ 1609 m). Give your answer to
  3 significant figures."; key 26.8 m/s unchanged. t4-007 closed with the ruling.
- **Verifier:** the t4-007 NOTE is now a check: "=" before a stated conversion fails unless it is the exact
  definition; "≈" before a rounded one passes. A plant puts "1 mile = 1609 m" back and is caught (11 plants).
- **Main's run on 4081538 (SIM-S5) green**, run 583. #204's PR run: E 36 s, B3 1m32s (the plan ran few verifiers).
- **Moved to the archive:** the entries before SIM-S5's claim. Still live from them: **for the home lane**, a B5
  group before the next verifier lands in B (main's run on c9fbf4b had B4 at 5m17s of its 6m budget); move Unit Converter
  from "Hidden Count-Up" to "No Timer" in `.claude/rules/timer-policy.md` (answers 3b; it shows, logs and scores no
  clock since #196); move unit-converter to check-answer-lock's MIGRATED (it passes seeds 1-3).
  From SIM-S5 (#203): record the build freeze's one named exception (Jon, 9 Oct, 00:25: Simultaneous Solver Stage 5
  only) in canon §0.2 and the todo; the roster row could mention Stage 5.
- **Next: FT-FIX** (`contracts/2026-10-08-ft-fix.md` as amended). From the PP-T1-004 entry: merge main first;
  factor-theorem is in check-answer-lock's MIGRATED, so it must still pass; `wrapExamVocab` is the shared
  `schools/assets/exam-vocab.js:109` (step 3 and t5-008 go to the home lane, per the amendment); both
  `question_index` calls already send `qIdx + 1`; the contract's line numbers are stale (re-find by quoted text).

## 2026-10-09 (cloud): SIM-S5 built (claim #202; fix #203 takes the game off the remaining list)

- **Stage 5** in simultaneous-solver: its own screen and flow (`startForm`, beside the A-Level one); Stages 1-4
  untouched (four existing lines widened: a trailing comma, a third `MaffsNext.clear`, two test hooks). `WORDS`
  bank between markers, worded as the contract (the verifier compares it); 8 a session, 3 W and 3 E at least;
  a mark per line (16); board `foundation-s5` with its label, coverage entry and hub row (Jon's authorisation).
- **EqTiles**, the builder: self-contained (build, read, parse, mark, markAll, tokens, text; `.eqt-*` CSS), exact
  fractions; tiles are whole terms (letters, the keys' numbers, + − =, distractors); Delete and Clear line.
- **Distractors (no invention):** a spare number in the text (not 1) or a pounds amount in pence (SR-4, the
  partly-scaled error). 35 of 40 have fewer than two: for Project Claude to supply if wanted (list in the PR).
- **Feedback notes** (one line each, where the key needs a fact the words leave out): W07, W11, W12, W13, W15,
  E05, E09, E11; listed in the PR for Jon.
- **Verifier** (group E): solutions held only there; every key's forms marked by the page's own EqTiles; tiles
  build every key; 60 draws; sessions tapped at 390x844 and 1280x900; MaffsLock; 3 plants. Stage 5 adds ~30 s.
  check-answer-lock seeds 1-3 PASS. **For the home lane:** the roster row could mention Stage 5 (yours).
- **For the home lane (SIM-S5 item 9): the build freeze has one named exception, Jon, 9 Oct 2026 (00:25): Simultaneous
  Solver Stage 5 only. Record it in canon §0.2 and the todo ("Stage 5 is parked under it" no longer holds).**

## 2026-10-09 (cloud): SIM-S5 claimed (Jon's answers, 08:10)

- **Option A, approved:** a Stage 5 tile builder in simultaneous-solver, marked as a non-zero multiple of a key; the
  builder is a self-contained object (build, read, mark; no reach into Stages 1-4) so it can become a shared module.
- **Jon (9 Oct, in session): the `foundation-s5` board's three shared lines land in the SIM-S5 PR** (as the roster's
  Calculator field did in UC-FIX): its label in `schools/assets/firebase-leaderboard.js`, its entry in
  `scripts/check-leaderboard-coverage.js`'s simultaneous-solver list, its hub row in `leaderboards/index.html`.
  Additive, nothing else in those files.
- **For the home lane (answers 3b):** `.claude/rules/timer-policy.md`: move Unit Converter from "Hidden Count-Up" to
  "No Timer" (since #196 it shows, logs and scores no clock). A shared rules file, so the cloud lane does not edit it.
- **For the home lane:** unit-converter passes check-answer-lock on seeds 1-3: move it to MIGRATED (your question).

## 2026-10-09 (cloud): SIM-S5 stopped before its claim (step 3 STOP IF; answered 08:10, above)

- **simultaneous-solver has no tile UI:** Stages 1-4 are typed boxes on MaffsKeypad (`readInt` whole numbers only;
  keys 0-9, point, minus). Equation Builder's tiles are its own code (fixed slots, arrangement matching), not shared.
  Options put to Jon: **A (recommended)** a Stage 5 free-build tile builder in this game (whole-term tiles incl.
  decimals, Delete/Clear, marked as a non-zero multiple of a key); B a shared tile module first (home lane);
  C typed coefficient boxes (fixes the form; no rearranged answers). Waiting on his choice.
- **The other STOP IFs do not fire:** all 40 bank systems solve uniquely to the stated positive solution (SymPy,
  exact rationals) and each "Let..." line names both letters; a `stage5` STAGES entry, a new step in `askStep()` and
  a problem-text branch in `nextQ()` are additive, so Stages 1-4 and A-Level stay untouched.
- **For the home lane (CI):** main's run on c9fbf4b: B4 5m17s of its 6m budget (Unit Converter 78 s), B3 4m00s; the
  PR runs had B1 4m14s, B2 3m40s. The B tier is close to full: a B5 group (ci-groups.py GROUPS) before the next
  verifier lands in B.

## 2026-10-09 (cloud): UC-FIX, unit-converter (claim #195; fix #196 merged c9fbf4b, main green)

- **The fix:** MaffsLock + MaffsNext ("Got it — next", in the worked solution) with its lock hint; ?level only from
  the game's own LEVELS (hasOwnProperty); 3 s.f. stated on the cylinder, 60 mph and shaft, working as the contract
  quotes (5000π, no 3.14); "1 inch = 2.54 cm"; one `fmt()` for every displayed number (options keep their stored
  `dataset.val`), the start screen's static "1000 cm³" now "1,000"; the calculator (theme.css before the page style,
  which is neutral here; `--surface-alt` and `--hint` added to :root; "Use a calculator." on every question; badge;
  roster field `required`). t4-005: 100 per correct answer, the HUD Time item and its clock removed (nothing logged it).
- **unit-converter has migrated: the home lane can move it from NOT_YET to MIGRATED** (check-answer-lock seeds 1-3 pass).
- **For Jon, the boards (amendment's STOP IF; never delete or move scores):** `unit_converter_gcse`,
  `unit_converter_alevel`, `unit_converter_level4`; the new maximum is **2,000** (20 questions × 100). The old
  speed-weighted score also topped out at 2,000 (100 a question only at 0 s), so honest old scores sit at or below
  what is now possible; scores inflated by the t4-001 re-mark (the audit made 4,399) sit above it. t4-003 may also
  have made junk boards (`unit_converter_nonsense`, `unit_converter___proto__`, `unit_converter_l4`, ...). The
  sandbox cannot reach Firebase: Jon checks in the console.
- **Dock:** docks at 1366 and 1920, not at 1280: this game's column is 760 px (canon's reference is 720), and by
  canon's formula it docks from 1292 px. The column width is design, so left as it is.
- **For Jon and the home lane, the timer list:** `.claude/rules/timer-policy.md` lists Unit Converter under Hidden
  Count-Up ("time shown on results screen only"); the amendment takes time off the results screen too, so it now has
  no timer at all (the No Timer list). Either the list moves it (home lane's file) or Jon wants the time on results.
- **Filed, open, for Jon:** t4-007 (LOW): "1 mile = 1609 m" is not exact (1609.344); the key is 26.8 either way.
  The verifier reports it as a NOTE. The bank is **58** items (I said 59 to Jon in the session; corrected).
- **Verifier** `scripts/verify-unit-converter.py`, group B4 (79 s in CI with its self-test; B3 reached 5m51s of its 6m
  budget with it, so it moved to B4, which ran 3m25s). Reads
  marks from page classes, events through the defineProperty hook (canon §7.9), speed by a skewed Date.now (not
  Playwright's clock: it replays every animation frame, so main's rAF clock took minutes).
- **Sandbox gotchas (this container):** pip's newest Playwright wants a browser build not in /opt/pw-browsers: pin
  `playwright==1.56.0` (matches chromium-1194). `esprima` will not build here: download its sdist and put the source
  on PYTHONPATH for extract-banks/check-banks.
- **Claimed** in its own commit, with three contracts saved verbatim: UC-FIX (21:05), its amendment (23:45: t4-005 joins,
  score on correct answers only, timer hidden; Screening Room t4-017 ruled "one row per answer is correct") and the
  FT-FIX amendment (21:30, Part A). Nothing open held unit-converter (only #193, the home lane's VOCAB-IDEMPOTENT).
- **STOP IF fired, step 5 (separators), and Jon ruled (9 Oct, this session):** marking compares `dataset.val`, which is
  the displayed string itself ('1570 cm³'). Ruling: "One formatter function for all displayed numbers. Verifier proves
  marking unchanged on all 59 items and that every displayed number of 1,000 or more has a comma." Stored strings stay.
- **Keys recomputed: none wrong.** Rounded with nothing stated: cylinder, 60 mph, shaft only. Circle and pipe are exact
  under their stated "π ≈ 3.14".

## 2026-10-08 (cloud, night): probability-paradox t1-004 (contract PP-T1-004)

- **Claim #187** (with both contracts saved, first in this section, then in `docs/handover/contracts/` after Jon's
  20:00 correction). Nothing loads that folder at session start: `check-context-size.py` measures only its three
  files, and CLAUDE.md names `home.md` and `cloud.md`. The home lane was told that the heading reads "read
  `docs/handover/`".
- **The item (#189):** Jon's text exactly, in the same place (fallacy bank, after the horoscope item), with no id.
  Analytics logs only `question_index`, and the B6 ledger keys only the bus item (`ca42ff7e8e2f`), so neither
  STOP IF fired. Tier 4 `--ci` matches the ledger exactly.
- **Verifier:** `PINNED_RTM` (the one item keyed "Regression to the mean": the scenario says "the lowest scores" and "of
  the same difficulty", the four options exactly, the key). `phone()` shows the item at 390x844, asking and after
  its longest wrong option, and measures scrollWidth 390 both times. The old item is planted back whole (nine plants,
  all caught). Main's page fails naming t1-004 (and FALLACY, which no longer reviews it).
- **Next: FT-FIX.** Merge main first. factor-theorem is in check-answer-lock's MIGRATED, so it must still pass.
  **Waiting on Jon before step 3:** `wrapExamVocab` is not the game's helper. It is defined in the shared
  `schools/assets/exam-vocab.js:109` (register t5-008 says so too), which the contract's DO NOT TOUCH and the lane
  rule both exclude. Step 4 to check: on main, both `question_index` calls already send `qIdx + 1` (:1072, :1248).
  The contract's line numbers (177, 625, 780, 1046) are stale (now :817, 958, 1143, 1145); Q33 (:702) and T9 (:766)
  match the quoted text.

## 2026-10-08 (cloud, evening): Jon's rulings on the open items (spot-the-muppet, terrible-advice, word-problem-decoder)

- **Jon's rulings (8 Oct), before probability-paradox:** one PR per game, each claimed first. The loan
  (stm_core_012, ta_core_012): "6% APR"; key about £364.20 a month (total £13,111.19), APR as the effective annual rate,
  interest on what is still owed; the old keys become named distractors (£397 compound, £393.33 simple, both "on the
  whole £12,000 for 3 years, as if none of it were repaid"), "£333.33, Lenny is correct" kept. The "patients" joke becomes
  "I'm telling everyone I know to buy a bigger telly." spot-the-muppet-t2-007 ruled (not in this game). Word Problem
  Decoder: gcse_017 £136, gcse_021 £44 and £48, gcse_059 "about 61 tins", gcse_022 rewritten (3 laps then 4, 33 minutes).
- **spot-the-muppet (claim #166; fix #168):** the key in words ("the twelfth root of 1.06, minus 1", not
  1.06^(1/12): canon 7.1, no ASCII notation; the page shows options as plain text). Each distractor keeps the game's
  "Lenny is wrong — " opening; Jon's em dash after the figure became a colon. Verifier: LOAN check (APR said; the key
  states the rate, the payment and the total to the penny; one distractor per named figure with its method word), the
  joke check, two plants (8 in all). Main's page fails t2-006 and t2-008 by name. Fits 320px (no sideways scroll).
- **spot-the-muppet #168 merged** 14:16 UTC; main's full run on 7252c9d green.
- **terrible-advice (claim #170; fix #171):** "6% per year" -> "6% APR"; the same key working (opening "the 6%
  is interest, not an arrangement fee", which this item's muppet claims) and the same three distractors; the joke as
  spot-the-muppet's. Verifier: `stm.check_loan` (the one copy, in verify-spot-the-muppet.py) on ta_core_012, the joke
  check, three plants (9 in all). Main's page fails t2-005 and t2-007 by name.
- **terrible-advice #171 merged** 14:54 UTC; main's full run on 6386a07 green.
- **word-problem-decoder (claim #173; fix #174):** Jon's numbers and wording, each highlight phrase matching
  its text. gcse_059 keeps "in the box" (Jon's quote left it out; only the number changed). Verifier `check_numbers`:
  gcse_017 and 021 solved from their text (whole and positive), gcse_022 read as 3x + 4y = 33 with y = 2x, gcse_059's
  estimate = round(box / tin volume) and more than the 48 that fit; two plants (5 in all). t1-011, t1-012 (LOW) open.
- **Jon's queue after probability-paradox (8 Oct, two contracts):** screening-room (t4-005 HIGH, 006, 008, 013, 016;
  leave t4-014, 015), then factor-theorem (t5-004, 005 HIGH, 008, 018; leave t5-009, 013-017). Both verbatim in the
  session; each claimed first; relisting is the home lane's.
- **word-problem-decoder #174 merged** 15:29 UTC; main's full run on 7eaff03 green. Jon's three ruling games done.
- **probability-paradox (claim #175; fix #177; listed-games contract 6 of 23).** SR-18 applied: the
  envelope keyed "Cannot determine — it depends on how the amounts were chosen" (t1-001); the bus states random
  (Poisson) arrivals, no timetable (t1-002); Sleeping Beauty accepts 1/3 and 1/2 through an `accept` list and
  `accepted(q)` (t1-003); Two-Child and Tuesday are asked questions with equally likely outcomes (t1-006); Monty's host
  rule and the 95% test's two rates stated (t1-009, re-audit). Simulations (t1-005): Beauty counts wakings (a trial may
  return several outcomes); the bus waits for the next bus of a Poisson stream. Fisher two-sided p 0.58 (t1-007).
  MaffsLock, MaffsNext on a wrong answer, hint (starts Paradox Predictor); t1-010 CRITICAL (score again on the revealed
  key) and t1-011 (mode on every event) filed and fixed. **t1-004 (HIGH, jc: "the test was easier") left open for
  Jon.** Verifier `scripts/verify-probability-paradox.py` (group E, ~1 min; ~8 min with the self-test, 8 plants).
- **Gotcha (again):** editing an item's text changes its content id, so a ledger entry on it (here B6's "wait"
  false positive on the bus item) goes stale and Tier 4 fails; `check-changed.py` does not run Tier 4. After any bank
  edit: `extract-banks.py --only <slug>` then `check-banks.py --only <slug> --write-ledger`.
- **probability-paradox #177 merged** 16:30 UTC; main's full run on dc0f22c green.
- **screening-room (claim #181; fix #183; unlisted, Jon's SR-21 contract + t4-015 ruling + Project
  Claude's note, 8 Oct).** MaffsLock and MaffsNext, hint (plays all three phases). **Gotcha: `fresh(gameScreen)` does
  not undo a lock held by a container inside it** (the gut options, the answer row, Next): fresh each locked container
  when it renders, or the second question's gut check is ignored. t4-006 own levels only (`hasOwnProperty`). t4-008
  (PC's rule): over 10,000, k = gcd(N, condition, TP, FP) if N / k fits 10,000, else the least whole k that fits with
  a group's remainder as one part-icon (`data-part`, CSS gradient); a note gives k in the item's `unit` and every exact
  count. t4-013 phases stack (column). t4-015 phase 3 keeps phase 2 on screen (Continue hidden). t4-016: fixed on main
  by #92 (bf3aa90); pinned with plants; its analytics part filed as t4-017 (LOW, open: own code, one row per answer,
  two answers a question; one row a question is a data change for Jon). t4-014 open (pools).
  **screening-room has migrated: the home lane can take it off NOT_YET** (passes check-answer-lock seeds 1-3; the
  cloud lane does not edit that script). Verifier gains open_page/extra_checks; run it WITHOUT the KaTeX shim (its
  async route handler hangs this verifier's sync page loads). **Without KaTeX the sandbox missed a real phone fault**
  (CI caught it: the A-Level Bayes formula, rendered, is up to 519 px wide); measure phone fit with KaTeX routed by a
  sync handler (`page.route(... lambda r: r.fulfill(path=...))`). Fixed: KaTeX lines scroll inside their box.
- **Main went red at 16:46 (home #180: verify-like-terms-collector, "item 1: typed 8.9/6.5, marked correct=None";
  Check marked nothing within 5 s, so the click itself, not the read); the failed job's re-run passed (17:40). Not
  reproduced with a 200 ms gap after every Playwright action (3 runs). The home lane holds contract MAIN-RED for it.
- **Factor Theorem (Project Claude, 18:35):** go ahead. **The alevel board: checked by Jon, 8 Oct 18:52:
  leaderboards/factor_theorem_alevel is null (nothing ever submitted): record "checked: empty" in the PR; that STOP IF
  cannot trigger.** (The sandbox cannot reach Firebase.) level4: no hub change
  while unlisted (NOT_ON_HUB skips the level check); the home lane's relist adds both levels.
- **#183 merged 18:13; main's run on 8ead626 red on group E's time budget** (10m03s of 12m, budget 9m; every
  verifier passed: today's joiners Probability Paradox 105 s, Screening Room 84 s, Spot the Muppet 69 s, Terrible
  Advice 56 s). Fixed by each verifier's own header: Probability Paradox to B1, Spot the Muppet to B2 (both ran about
  2m50 of 6m). **A new cloud verifier: pick a B group with room, not E.**
- **CHECKPOINT (Jon, 8 Oct ~19:00, context over 60%): STOP once main is green after the group fix.** Nothing claimed
  after it. The next session starts with probability-paradox t1-004.
- **Both contracts are now saved in the repo** (Project Claude, 19:55; queue above): PP-T1-004, then FT-FIX, which
  replaces the two lost Factor Theorem contracts. #180 closed t5-009, so merge main first. The alevel board is
  empty and level4 needs no hub change (both above).

## 2026-10-08 (cloud, afternoon): CHECKPOINT STOP (Jon's queue done): listed-games contract at 5 of 23; nothing claimed

- **Jon's queue for this session is done:** spot-the-muppet (#155), word-problem-decoder (#157), terrible-advice
  (#160), then the Correlation or Coincidence contract (#163, 84 items). All merged on a green Gate, main green after
  each. The remaining list above is empty: **no game is claimed.**
- **Next game: probability-paradox.** Claim it first, in a PR of its own on main (canon 7.8.2). Check the open PRs and
  `docs/handover/home.md` first, and claim one game at a time.
- **The rest of the order:** core-maths-paper2c, core-maths-paper2b, wrong-on-the-internet, higher-power,
  prisoners-dilemma, coordinate-geometry-dash, surd-simplifier, scale-factor-scaling, unit-converter, formula-forge;
  then boolean-blitz, matrix-crunch, complex-converter, eigenvalue-extractor, characteristic-quest. **Skip 52dle and
  seven-bridges:** the home lane's F1 batch 5 (#161) holds them.
- **Per game, as for the first five:** claim PR; read its open register entries and the game; a verifier that fails on
  main naming the entries; MaffsLock with its lock hint; a scoring change beyond the named fault, or new data, goes to
  Jon; `check-changed.py`; PR; fill the register's PR number; merge on green, 10 min clear of a home merge; watch main.
- **Waiting on Jon:** the two loan keys (spot-the-muppet-t2-006, terrible-advice-t2-005: the convention to state);
  spot-the-muppet-t2-007 (the slip is terrible-advice's only; the register has no "not in this game" status); the
  two "patients" jokes (t2-008 / t2-007); word-problem-decoder t1-006..008 (new numbers or wording).
- **This checkpoint trimmed this file** (contract CTX: current state and the last three entries; check-context-size.py
  holds it to 20 KB). The older entries are in `docs/history/handover-cloud-archive.md`. Its DEFERRED entry for this
  file is removed in the same PR, as the entry itself said to do at this checkpoint.
- **Gotchas this session:** `pkill -f` / `pgrep -f` on a pattern that is in your own command line kills your own shell
  (exit 144). Kill a background run by its task id, or match a pattern your command does not contain. In this
  sandbox, `check-changed.py` fails the teacher line (and, when `cloud.md` changes, the answer lock parts) only on
  KaTeX games, because the KaTeX CDN is refused. CI has KaTeX.

## 2026-10-08 (cloud, afternoon): correlation-or-coincidence, 84 items (Jon's contract, 8 Oct)

- **#160 (terrible-advice) merged** 12:46 UTC, after main's red run on #158 (five KaTeX games in answer lock L1; #158's
  own PR run had passed) went green on the home lane's re-run. Claim #162.
- **The 42 items** (A15-A28, B15-B28, C15-C28; Project Claude's and Jon's, the jokes Jon's) appended exactly as
  pasted, each block with its own header comment after A14, B14 and C14; every pasted line is in the page byte for
  byte. 84 items, 28 of each kind. `MIN_BANK = 84` in the verifier, nothing else changed there (a copy with C28
  removed fails "bank has 83 items, the minimum is 84").
- **Every new graph's r inside its band** at its n and whole-number settings (the PR lists all 42). Closest to an
  edge: C27 (strong, n = 8, x whole 0-4) r = 0.928 of [0.80, 0.94]. No STOP IF fired: phone fit at 320/375/390 for
  every item (asking screen and wrong-answer feedback); SR-14 clean; a session of 10 played at 390x844 by real taps,
  the real MaffsNext floor (no sideways scroll, Next above the footer every time, one game_completed).
- **Register:** no bank-size entry exists for this game; nothing to close.
- **For the home lane:** Jon may want an /updates/ line ("Correlation or Coincidence now has 84 questions"): his
  call, not this PR. The home lane's F1 batch 5 (#161) holds 52dle and seven-bridges, both on the listed-games list:
  the cloud lane skips them.

## 2026-10-08 (cloud, afternoon): terrible-advice (listed-games contract, 5 of 23)

- **#157 (word-problem-decoder) merged** 12:18 UTC; main's full run on 2c846ac green. Claim #159 merged 12:26.
- **The same format as spot-the-muppet, its own engine** (a point for a right first pick only; kept). MaffsLock as
  spot-the-muppet: a first wrong pick marks and logs nothing; the question is marked and logged once; finishOnce;
  Play Again a screen change; the same two-wrong-picks hint (seeds 1, 2, 7 pass).
- **Fixed:** t2-001 gcse_006's "Prudence is correct — upper bound is 2.45m" (true, keyed wrong) -> "Prudence is wrong
  — upper bound is 2.49m"; t2-002 core_002 as spot-the-muppet's; t2-003 core_007 (the weighted mean is 70% too): the
  key says she got the right answer this time but her method is wrong, the distractor is "Wendy is correct in both
  method and answer" (the pattern of gcse_008 and gcse_012); t2-006 the key's "£500 × 1.1249 = £562.43" -> "× 1.124864";
  t2-008 the key's "Square roots always have a positive and negative solution" -> "because (−5)² = 25 as well"; filed
  and fixed t2-009 (core_004's working: 1.05 × 20 = 21.05) and t2-010 (HIGH: core_004's simple-interest option true as
  written, as spot-the-muppet-t2-001).
- **Verifier** `scripts/verify-terrible-advice.py` (group E, ~70 s with the self-test) imports spot-the-muppet's
  arithmetic (`# ci-deps: scripts/verify-spot-the-muppet.py`), which this PR extends: every vulgar fraction (⅖ was read
  as a whole number at 0 d.p. and matched ⅚); pounds against pence ("£4.80 ÷ 400 = 1.2p/g"); a rounded intermediate
  ("1,000 × 1.05²⁰ = 1,000 × 2.653") passes only between two expressions and only for a decimal not in the advice, so
  a slip on a given (t2-009) or at the last step (t2-006) still fails. Main's page fails t2-001..004, 006, 008, 009, 010
  by name; six plants.
- **Left open (for Jon):** t2-005 the loan key (simple interest on the whole £12,000 for 3 years, about £393/month; a
  repayment loan is about £364.20/month), with spot-the-muppet-t2-006: both need a stated convention (APR effective
  monthly, or a flat-rate loan). t2-007 the "patients" joke (SR-14 tier (c) vs a joke).
- **spot-the-muppet-t2-007** (562.45 vs 562.43, filed against both games) is terrible-advice's slip only; spot-the-
  muppet's key was always right. The register has no status for "not in this game": Jon's call (ruled, or removed).
- **For the home lane:** terrible-advice passes the lock check: add it to MIGRATED. The two games share one engine
  shape in two copies; a shared module would be the architectural fix (not this lane's).

## 2026-10-08 (cloud, afternoon): word-problem-decoder (listed-games contract, 4 of 23)

- **#155 (spot-the-muppet) merged** 11:51 UTC; main's full run on 6232248 green. Claim #156 merged 12:00.
- **The category scheme (SR-18: one scheme, both accepted where both fit):** `PARENT_TOPIC` in the game: Reverse
  Percentage is a kind of Percentages, Standard Form a kind of Number & Place Value (the KS3 bank, which offers
  neither kind, keys ks3_013, ks3_015 and ks3_023 under the parent), so a phrase keyed the kind is right under the
  parent too (t1-003, t1-004). A phrase's own `also` lists any other topic that genuinely fits: ks3_006 phrase 2
  (t1-001) and gcse_017 (t1-002), plus six found on the re-audit (t1-010: ks3_022, ks3_046, gcse_013, gcse_022,
  gcse_039, gcse_060 phrase 2). `acceptedTopics(hl)` marks; after a pick, every topic that fits and is on the buttons is
  revealed. **The judgement on each `also` is listed in the PR for Project Claude** (it is content).
- **t1-005, MaffsLock:** `lock(optionsGrid)` first in handleAnswer; `fresh(optionsGrid)` per phrase; the advance
  timers through MaffsLock.timer (the ~1 s auto-advance after a wrong answer is kept: the audit's class 7, "not counted
  as a fault"); finishOnce; Play Again a screen change. Hint `{}`: the generic driver plays it (seeds 1, 2, 7).
- **t1-009 (the 3 uncounted MEDIUMs) closed by the re-audit:** every phrase read against the 23 topics; filed t1-010
  (HIGH, fixed), t1-011 (LOW, open: three items refer to a figure the game never shows) and t1-012 (LOW, open: two Aa
  buttons).
- **Verifier** `scripts/verify-word-problem-decoder.py` (group E, ~5 s; ~15 s with the self-test): bank shape; every
  phrase played in Chromium with each topic it accepts and three it does not on the buttons (getDistractors replaced
  for the test), so the marking is tested whatever the page's code; `ACCEPT` holds every second topic with its reason;
  answer once; the session ends once. Main's page fails t1-001..005 and every t1-010 phrase by name; three plants.
  **Gotcha:** the sweep renders each phrase itself, so it drops the game's own setTimeout advances (they would fire
  mid-sweep and move it on).
- **Left open (MEDIUM, wording or numbers: for Jon / Project Claude):** t1-006 gcse_017 and gcse_021 have no
  whole-number answers (c = 71/19; a = 170/19); t1-007 gcse_059 says 48 tins is "too high" but 48 fit exactly
  (6 × 4 × 2), and 72000 ÷ (π × 25 × 15) is 61.1, not 48; t1-008 gcse_022's lap count is ambiguous.
- **For the home lane:** word-problem-decoder passes the lock check: add it to MIGRATED.

## 2026-10-08 (cloud, afternoon): spot-the-muppet (listed-games contract, 3 of 23); session queue

- **Jon's queue for this session (8 Oct):** spot-the-muppet, word-problem-decoder, terrible-advice; then the
  Correlation or Coincidence contract (42 new items, 42 -> 84, MIN_BANK = 84; Jon's text and items arrived 8 Oct, the
  items verbatim in `docs/handover/cloud-coc-items-2026-10-08.js` until that PR appends them and deletes the file);
  then CHECKPOINT: next game probability-paradox, not claimed.
- **Claim #154** (merged 11:3x UTC, main green).
- **spot-the-muppet (this PR):** t2-001 core_004's advice says "compound interest" and the simple-interest option
  claims to be the answer (£1,000 + 20 × £50 = £2,000, false for compound); t2-002 core_008's "£120 − £20 = £100" ->
  "£120 × 1.20 = £144"; t2-003 ks3_005's "(2+10) ÷ 2 = 6" -> "(3+7+8+2+10) ÷ 4 = 7.5"; t2-004 core_002's advice no
  longer makes the valid marginal argument (it compares the extra £1.30 with the whole £3.50, which proves nothing);
  t2-009 (filed here) core_004's working said 1,000 × 1.05 × 20 = 21,050 (it is 21,000).
- **t2-005, MaffsLock:** the two-pick retry is kept (score unchanged: a right second pick still scores 1). A first
  wrong pick marks and logs nothing (the card is disabled, a fresh window opens); the question is marked and logged
  once, when right or at the second wrong pick (spot-the-error's pattern). So question_answered is now one row per
  question (before: a first wrong pick logged its own row). Every timer through MaffsLock.timer; finishOnce; Play
  Again is a screen change. Lock hint: two different wrong picks. `check-answer-lock.py --game spot-the-muppet`
  passes at seeds 1, 2, 7.
- **Verifier** `scripts/verify-spot-the-muppet.py` (group E, ~70 s with the self-test): every equation chain in the
  advice and the keys evaluated (a muppet's deliberate wrong sum is in MUPPET_SUMS); every key recomputed (KEYS) or
  reviewed (CONCEPT), so a new item cannot skip review; no distractor ends on the key's value as the key writes it
  (SR-16); every item played three ways; Next's second click, a real double click, a double click on a first wrong
  pick, the end once. Main's page fails t2-001..005 and t2-009 by name; six plants caught. **Gotchas:** a whole
  number under 10 in a key never stands for a non-whole value ("not 1" is not 0.665); the first piece of an
  equation chain after "of" / "year" or glued to a word ("cos⁻¹(") is a fragment, not a value.
- **Left open (MEDIUM; for Jon):** t2-006 core_012 (the loan key's £14,292.19 total and ≈ £397/month are compound
  growth, not a repayment loan: about £364.20/month at 6% APR; the verifier reports it as KNOWN_OPEN and fails once
  it is fixed and not removed), t2-008 (the "patients" joke, SR-14 tier (c) vs a joke: Jon's call).
- **Seen, not filed (for Project Claude):** gcse_006 Prudence's method "add 5 to the last digit" is keyed correct by
  the key's own reasoning "adding half the degree of accuracy"; the words don't say the same thing.
- **For the home lane:** spot-the-muppet passes the lock check: add it to MIGRATED.
- **check-changed.py:** all green but the teacher line, which fails only on factor-theorem and log-laws (KaTeX CDN
  refused in this sandbox, the known gotcha), not on this game.

## 2026-10-08 (cloud): CHECKPOINT STOP (Jon): listed-games contract at 2 of 23; nothing claimed

- **Where the contract stands (Jon's listed-games contract, 8 Oct):** both listed CRITICALs are closed.
  trig-wars (#148, merged, main green) and gradient-hunter (#152; its entry below). The remaining list above is
  empty: **no game is claimed.** The session stopped at Jon's checkpoint without claiming the next game.
- **Next game: spot-the-muppet.** Start with a claim PR on main (canon 7.8.2, #145): check the open PRs and the home
  handover first, claim one game at a time, the fix PR takes it off the line.
- **The rest of the order, after spot-the-muppet:** word-problem-decoder, terrible-advice, probability-paradox,
  core-maths-paper2c, core-maths-paper2b, wrong-on-the-internet, 52dle, higher-power, prisoners-dilemma,
  seven-bridges, coordinate-geometry-dash, surd-simplifier, scale-factor-scaling, unit-converter, formula-forge;
  then boolean-blitz, matrix-crunch, complex-converter, eigenvalue-extractor, characteristic-quest.
- **Per game, as done for the first two:** claim PR; read its open register entries and the game; a verifier
  that fails on main naming the entries (group E has room: trig-wars ~45 s, gradient-hunter ~15 s); MaffsLock with
  its lock hint; a scoring change beyond the named fault, or new data, goes to Jon (gradient-hunter t2-003 did);
  `check-changed.py`; PR; fill the register's PR number; merge on green, 10 min clear of a home merge; watch main.
- **Earlier today (all merged, main green):** truth-buster #143; expectation-station #146 (Stage 1 one completion,
  40/40/40; ready to relist under SR-21).

## 2026-10-08 (cloud): gradient-hunter (listed-games contract, 2 of 23; the second CRITICAL); #148 merged

- **#148 (trig-wars) merged** 09:50 UTC; main's full run on b8691f8 green. Claim through main: #149 (merged 09:58).
- **t2-001 (CRITICAL):** MaffsLock locks the options at the first pick (the revealed correct option re-scored without
  limit). A wrong answer now waits for MaffsNext (canon 7.6; it moved on at once before); a right answer keeps its
  own Next, locked at the press; every question opens a fresh window on the game screen (the canvas included);
  `finishOnce`; Play Again opens the menu with `MaffsLock.screen` (the menu has the leaderboard link, as
  partial-fractions-duel's did). The KaTeX wait for the method reference is `// lock-ok:`.
- **t2-002:** the three stated tangents are the DRAWN curve's: a cardinal spline's slope at a plotted point is its
  neighbours' gradient, whatever the tension: 4.5 (was 5), 110 (was "a steeper gradient of 150"; the audit's 98.0 is
  the ideal exponential, not what is drawn, and 110 is LESS steep than the 116.7 chord) and 3.25 (was 4).
- **t2-003, filed and fixed (Jon's ruling, 8 Oct, option A):** a Calculate item scored a point for the gradient
  whatever the student did (the game showed it once the two points were clicked). Now the student types it after
  the two points: `MaffsAnswer.fractionOrDecimal` against the chord through the points clicked (`chordGradient`:
  exact rise/run; "to 2 decimal places" only when it recurs, so -9/80 is asked as -0.1125); that earns the point,
  clicking scores nothing, the working (rise / run) follows, the interpretation is unchanged. One question_answered
  per item, as before (the interpretation's). A text keyboard on phones (`inputmode="text"`: iOS's decimal pad has
  no minus): the shared MaffsKeypad is styled by theme.css, which this game has not migrated to, so it joins the
  todo 3.21 list (home lane: the keypad comes with its theme migration).
- **Verifier** `scripts/verify-gradient-hunter.py` (group E, ~9 s): chords from their points, stated tangents from the
  spline, one true interpretation (an "instantaneous/marginal ... is V" option is keyed right exactly when V is the
  tangent; a plain "is V" claims V to the hundredth, "about V" at V's places), every item played, the typed gradient
  on all 27 Calculate items, answer once and Next once (~15 s). Main's page fails t2-001 on six items, t2-002 on four
  claims and t2-003 on all 27; three plants caught.
  **Gotchas:** read numbers with thousands separators; a fall's interpretation gives its size; MaffsNext takes focus,
  so an Enter after a wrong pick advances (test the option with clicks, not the keyboard). **Never write a shared
  asset's file name (theme.css, keypad.js ...) in a game page, even in a comment:** `ci-deps.py --selftest` (b) reads
  a page that mentions it as one that loads it, and the PR's Plan job fails (#152's first run).
- **For the home lane:** gradient-hunter passes the lock check: add it to MIGRATED.
- **Next:** spot-the-muppet (the first of the audience order): claim PR first (not claimed: checkpoint stop).

## 2026-10-08 (cloud): trig-wars (listed-games contract, 1 of 23; first CRITICAL); #146 merged

- **#146 (expectation-station) merged** 08:56 UTC; main's full run green. **The claim went through main** (#147,
  merged 09:03): under #145 the home lane reads the line on main, so a listed game's claim is its own small PR.
- **Jon's ruling (8 Oct):** 2 PLAYER submits nothing (two people on one device; SR-22). VS CPU scores Player 1 only.
- **Fixed, all six entries (t2-001 CRITICAL, t2-002 HIGH, t2-003..006 MEDIUM):**
  - t2-001: hits and shots per side; VS CPU logs and scores Player 1's shots only, submitted win or lose;
    2 PLAYER logs both sides and submits nothing. Events carry `mode` (analytics rule for multi-mode games).
  - t2-002/005: the panel's Vx, Vy are V cos/sin in V's own units (no "u/s"; 0.28 stays internal).
  - t2-003: one physics (`newShell`/`stepShell`/`simulateShot`) for the flight, the advice and the check's aim; a hit
    is tested along each frame's segment before the ground. The old test missed 3.4% of true hits, half
    ground-first, half a fast shell crossing the circle between frames.
  - t2-004: the quip says only how it missed; `missAdvice()` suggests a change only if the physics says it lands
    at least 1px nearer (a 45-degree rule was wrong on 38% of misses: the hill; a 0-px gain was floating-point
    noise at the field's edge).
  - t2-006: four lines replaced (new wording in the PR for Project Claude).
- **MaffsLock:** FIRE locks per side (the slider rows are `data-maffs-lock-skip`, so a player can aim during the
  other turn); every timer through `MaffsLock.timer`; `finishOnce`; `shotId` stops a flight still animating after a
  reset. Lock hint: i = 0 fires `aimAtEnemy()` (a sure hit), i >= 1 fires 85 deg / 20 (a sure miss).
  `check-answer-lock.py --game trig-wars` passes (judged in full). Its note "no Next after a wrong answer" stands:
  after a miss the turn passes to the opponent (not in the register).
- **Verifier** `scripts/verify-trig-wars.py` (group E, ~45 s with the self-test): its own copy of the physics in
  Python; plays three battles, 252 panel settings, both kinds of missed hit, and near misses either side of 45 deg.
  Main's page fails on all six entries; three plants caught. **Harness gotchas:** run animation frames
  synchronously (a flight is ~150 chained frames; `setTimeout(0)` clamps to 4 ms); read the miss message by
  wrapping the page's `msg()` (the game clears it before a poll sees it); wrap `mfg` once per page.
- **Not changed:** the phone width (711px at load in CI's font, allowlisted, todo §3.9 batch 19).
- **For the home lane:** trig-wars passes the lock check: add it to MIGRATED.
- **Next:** gradient-hunter (the second CRITICAL): claim PR first.

## 2026-10-08 (cloud): expectation-station, Stage 1 one completion and 40/40/40 (Jon's bundle contract); #143 merged

- **#143 (truth-buster) merged** 08:10 UTC on a green Gate, after merging main (#144, contract DET, landed 07:58 while
  #143's CI ran: truth-buster's hint passes DET's lock check, seed 1, twice). #141 closed as superseded.
- **Claimed** in its own commit (58e19a0), off the line in this PR.
- **The bundle** (Project Claude, 7 Oct; Jon's ruling B), applied by script, verbatim: the 33 items get their sentence
  appended to the context and prepended to the explanation; 75 new items (core 021-040, gcse 016-040, alevel 011-040).
  Each level serves min(session length, bank), so 40 each.
- **Verifier:** `COUNTS` 40/40/40; the bundle's CARDS and FIGURES; `FIGURES_ADDED` (the 33 items' new opening claims);
  `CLUES` for all 120; **Stage 1 uniqueness**: every placement of the tiles into the missing cells is tried, and exactly
  one may sum to 1 and satisfy the CLUES entry, the keyed one. A CLUES ratio, difference or E(X) must also be in the
  context's own words (so a CLUES entry cannot claim what the student is not told). Fourth plant: es_core_001 without
  its sentence, CLUES ('none',): caught. Main's page fails 38 items on Stage 1, plus the counts. Runs in about 10 s.
- **Found by the uniqueness check, not in the bundle:** es_gcse_006, es_gcse_014, es_alevel_003, es_alevel_008 and
  es_alevel_010 have equal keyed values, so the bundle gave them ('none',), but a second pair of tiles also summed to
  the gap. **Jon's ruling (8 Oct, approved by Project Claude):** one stray tile changed on each (1/6 -> 1/8,
  0.35 -> 0.40, 0.3 -> 0.4, 0.30 -> 0.35, 0.25 -> 0.30). No new wording.
- **Added here, not in the bundle:** ten definition-only FIGURES entries ("Let P(X = a) = p and P(X = b) = q",
  es_alevel_021-030), like the existing "k + 2k + ... = 1" entries.
- **es_alevel_006** (approved by Project Claude, 8 Oct): its context said only "a batch of 4", so x = 1 and x = 4
  could swap (0.2916 and 0.0001 both fit the sum). It now ends "Each item is defective independently with probability
  0.1."; CONTEXT requires those words and the table to be exactly B(4, 0.1). Cards and explanation unchanged.
- **Phone:** the context is `.context-text` (textContent, no clamp); every one of the 120 measured unclipped at 390x844.
- **Register:** pc-001 fixed; no other entry open. **Ready to relist (SR-21, home lane): no CRITICAL or HIGH open.**
- **Ledger:** 40/40/40 made the three B4 (bank size) entries stale, which failed Tier 4 on the first CI run.
  `extract-banks.py --only <slug>` then `check-banks.py --only <slug> --write-ledger` cleared them (no other rule
  fired on the 75 new items). **Any bank change: run both before the first push** (`check-changed.py` does not run Tier 4).
- **Next:** Jon's listed-games contract (8 Oct): trig-wars first, then gradient-hunter.

## 2026-10-08 (cloud): truth-buster (queue 6 of 6, the last); the remaining list is empty

- **State found:** the previous session's closing note (partial-fractions-duel next) predated #139; #139 and the relist
  (#142) had merged and main's full run on a99efa5 was green. Only truth-buster was left.
  **Missed at the start: #141** (the previous session's truth-buster PR, the same cherry-pick) was already open. #143
  duplicated it; #143 was merged (its lock hint has no fixed wait, the cause contract DET names) with #141's fuller
  t3-016 (375x667 too), and #141 closed as superseded. **Check the open PRs, not only main and this file, at the start.**
- **truth-buster:** the old session's commit (fcc5e4c, `claude/keen-cray-ypsime-truth-buster`) cherry-picked onto main
  cleanly: MaffsLock in full (no `S.answered`; Next locks at its first press; the tier transition and the Next delay
  through MaffsLock.timer; finishOnce), and on a phone the answer buttons fold away during the reveal and the page moves
  Next above the footer. Added here: its maffs-lock-hint. **Two options: it presses the button that differs from the
  key, so every attempt is wrong.** Without it the generic driver came out all right on 8 draws in 1 run of 3 here
  (UNPLAYABLE), the fault contract DET names. Off the remaining list.
- **Proofs:** `verify-truth-buster.py` passes; against main's page it fails 62 times (the double Enter at the tier
  boundary, t3-013; Next under the fold at 390x844 on all 60 items). `check-answer-lock.py --game truth-buster` passes
  four times with the list empty (judged in full; 20 answered, 0 right, the same every run); `--selftest` passes.
- **Register:** t3-013 fixed. t3-015 stays open (the 21 Learn More video IDs: YouTube is refused here); its fold part is
  fixed at 390x844, and 320x568 is filed as **t3-016** (MEDIUM, open: 32 of 60 fit; the reveal is taller than the
  screen, so it needs shorter reveal text or a layout ruling; 375x667: 58 of 60). t3-014 (levels, class 4/5) stays open.
- **For the home lane:** truth-buster passes the lock check: add it to MIGRATED.
- **Next:** Jon's contract of 8 Oct (listed games' CRITICAL/HIGH, trig-wars first) runs after the **Expectation Station
  bundle contract**, whose text this session has not received.

## 2026-10-07 (cloud): partial-fractions-duel (queue 5 of 6); #138 binomial-blaster merged; NEXT = truth-buster

- **#138 merged** at 20:53 on a green Gate; main's full run on b10d3db green.
- **partial-fractions-duel:** the old session's commit (9a19235) cherry-picked onto main (Jon's alevel[22]:
  1/(x(x+1)(x-2)), find C, keyed 1/6; distractors -1/2 = A, 1/3 = B, -1/6 the sign slip; MaffsLock; the B3 duplicate
  cleared), plus its maffs-lock-hint (`{}`) and off the remaining list.
- **The two lock-check reports were one fault, in the game:** Play Again calls `showMenu()`, and at 1280x900 the menu's
  "Global leaderboard" link sits under the button, so the second click of a double click opened /leaderboards/.
  That page then threw "firebase is not defined" (the check blocks the Firebase CDN). `showMenu()` now calls
  `MaffsLock.screen()` on the menu (the shared API's own screen-change call; nothing shared edited). The verifier tests
  a real double click and Play Again then the link and Start; a fourth plant (the old showMenu) is caught.
  `check-answer-lock.py --game partial-fractions-duel` passes, twice. Filed as t5-011 (class 1), fixed.
- **For the home lane, two findings outside this lane:**
  - **The same Play Again shape is in 25 games** (`function showMenu(){show('menu')}` with a `/leaderboards/` link on
    the menu): angle-ace, bearing-blitz, binomial-blaster, characteristic-quest, circle-theorem-spotter,
    coordinate-geometry-dash, curling-friction, dimension-checker, eigenvalue-extractor, eigenvector-engine,
    force-resolver, formula-forge, formula-unlocked, graph-transformer, matrix-crunch, moments-master,
    normal-navigator, probability-paradox, proportion-blaster, scale-factor-scaling, sequence-solver,
    standard-form-blitz, surd-simplifier, trig-identity-duel, unit-converter. The check's Play Again test is a
    double click at one point, so it catches the fault only where a control happens to sit under the button
    (binomial-blaster and trig-identity-duel pass it with the same code). A layout-independent test (Play Again,
    then a click on every menu control within the window) would find all of them.
  - **/leaderboards/ throws when the Firebase SDK does not load** (a school network that blocks gstatic.com):
    `leaderboards/index.html:159` calls `firebase.database()` unguarded, so the whole script stops, including the
    device-local "Your Scores" section. firebase-leaderboard.js guards the same case (`typeof firebase`).

## 2026-10-07 (cloud): binomial-blaster (queue 4 of 6); #137 trig-identity-duel merged; NEXT = partial-fractions-duel

- **#137 merged** at 20:21 on a green Gate. Its first L1 run failed on fraction-equivalence, the second home-lane
  two-option game to do so (prime-or-composite on #134): the shared check's wrong-answer search is not deterministic
  for a two-option game. Passed on the one re-run; commented on #137 with the architectural fix (pick the wrong option
  from the game's data, or seed Math.random as tier 1's PHONE_SEED does). **For the home lane: it will keep failing
  PRs at random until fixed.**
- **binomial-blaster:** the old session's commit (67bf685) cherry-picked onto main, plus its maffs-lock-hint (`{}`), the
  method reference's KaTeX wait (:253) marked `// lock-ok:`, and off the remaining list. Jon's alevel2[36]:
  3/((1+x)(1-2x)) = A/(1+x) + B/(1-2x), find B, keyed 2 (distractors 1, -2, 3); the old item (1/((1+x)(1-x)), B = 1/2)
  was right but duplicated another (B3 ledger entry cleared, no register entry). MaffsLock in full.
- **Register:** t5-017 (class 1) fixed. t5-018 (class 4, shared level resolver) and t5-022 (wording) stay open.

## 2026-10-07 (cloud): trig-identity-duel (queue 3 of 6); #135 truth-will-set-you-free merged; NEXT = binomial-blaster

- **#135 merged** at 19:47 on a green Gate (main green on 571bb60; last home merge 18:44).
- **trig-identity-duel:** the old session's commit (03c34eb) cherry-picked onto main, plus its maffs-lock-hint (`{}`)
  and off the remaining list. Jon's gcse[16]: A = 45°, a = 10 cm, B = 60°, b = 12.2 (the old item, B = 30° keyed 7.1,
  was right but duplicated another question: the B3 ledger entry is cleared, no register entry). Hidden count-up
  (timer-policy, SR-23): no HUD timer, a right answer scores BASE whatever the time, time on the results only.
  MaffsLock in full.
- **Register:** t2-007 (class 1) and t2-010 fixed. Every other entry was already fixed by #102.
- **Not in its register, not fixed here:** a wrong answer still moves on by itself after 1 s (MaffsLock.timer), with
  no Next (canon 7.6). The lock check notes it ("no Next after a wrong answer"); it does not fail.

## 2026-10-07 (cloud): truth-will-set-you-free (queue 2 of 6); #134 eigenvector-engine merged; NEXT = trig-identity-duel

- **#134 merged** at 19:16 on a green Gate. Its first L1 run failed on prime-or-composite, a home-lane game the PR
  did not touch: `answer_wrong()` taps option (k+1) % 2 on 8 unseeded draws, and after a right answer `to_next()`
  waits a fixed 350 ms ('auto'), so a tap can land in the next question's 300 ms fresh window and be dropped. It
  passed 5 of 5 locally and on the one re-run. Commented on #134; the fix is the home lane's (shared check, or an
  `answer` in prime-or-composite's declaration). **For the home lane.**
- **Old branches:** this session's git proxy refuses any push but its own branch, deletes included, so the
  `claude/keen-cray-ypsime-<game>` branches cannot be deleted from here. Jon (or the old session) deletes them.
- **truth-will-set-you-free:** the old session's commit (7b07e09) cherry-picked onto main, plus:
  - [27], approved by Project Claude (7 Oct): "This expression can be written (A ⊕ B)·C·D·Ē, where A ⊕ B = A·B̄ + Ā·B
    (XOR: one or the other, but not both). Play Boolean Blitz →", in KaTeX. XOR is introduced nowhere else in the
    game, so a form using it carries `identity` and `gloss`; the verifier checks the identity is true, the gloss, and
    the rendered line (a third plant, XOR with no definition, is caught).
  - Contract LH: its maffs-lock-hint (a wrong table, every cell the opposite of its key, then Submit; on the
    expression step the first option) and off the remaining list. `check-answer-lock.py --game` passes in full, twice.
    Its Next is replaced on each render (btnRow), so the hidden-button double advance eigenvector-engine had is absent.
- **Register:** t6-001, -002, -003, -005 fixed; t6-006 filed and fixed ([6]'s distractors A + B·C and (A + B)·(A + C)
  are equal by the distributive law; class 2, LOW); t6-004 (class 5, bank size) stays open.
- **Queue state (each prepared in a worktree, verifier passing on its branch and failing on main):**
  trig-identity-duel (`/home/user/tid-wt`, hint `{}` committed), binomial-blaster (`bb-wt`, hint `{}` and :253's KaTeX
  wait `// lock-ok:` committed), partial-fractions-duel (`pfd-wt`: needs a hint; the lock check here also reported
  "dblclick on Play again: its second click answered the first question" and "firebase is not defined", neither of
  which reproduces in a direct Chromium probe without the KaTeX shim: settle on CI, where it is judged in full),
  truth-buster (`tb-wt`: needs a hint with an `answer`; the generic driver finds no wrong answer; plus the MEDIUM
  320x568 entry, canon 7.6.1).

## 2026-10-07 (cloud): eigenvector-engine (queue 1 of 6); #130 Factor Theorem merged; NEXT = truth-will-set-you-free

- **#130 merged** at 18:22 on a green Gate (main green on b7e634b; last home merge 17:43). Main's run on d337b0b watched.
- **eigenvector-engine:** the old session's commit (3394734, from `claude/keen-cray-ypsime-eigenvector-engine`)
  cherry-picked onto main. It already adopts MaffsLock in full (newSession, lock, fresh, timer, finishOnce; no local
  flags), so the class-1 entry t6-002 closes. One addition here: `check-answer-lock.py` (on main since #129, after the
  commit was written) found a raw `setTimeout(buildExample, 300)` on load; it draws the start screen's worked example
  and marks nothing, so it carries `// lock-ok:`. Static rules pass.
- **Found here, fixed (class 1, part of t6-002):** `check-answer-lock.py --game eigenvector-engine --not-yet` (KaTeX
  served) reported "question_index jumped" on the old page every run. Instrumented: the worked solution's "Got it —
  next" was a plain onclick, only hidden after use, so a second Enter in the same frame (about 10 ms apart in the
  tap-through) ran closeSol() twice and skipped a question unseen. Now MaffsNext.wrong (canon 7.6; next-control.js
  loads before answer-lock.js), label kept. The verifier checks a real double click and two activations in one task
  (two Enters in one frame); a third plant (the old onclick) is caught. Python's separate key presses never land in
  one frame, so a keyboard test of this needs the in-page double activation.
- Verifier passes on the branch, fails on main's page (QS[22], [23], [24]); all three plants caught. The tap-through
  passes on the fixed page.
- **Register:** t6-001, -002, -004, -005, f0-001..007 fixed; t6-003 (class 5) stays open.
- **TWSYF is ready in `/home/user/tw-wt` (branch tw-local):** [27] uses Project Claude's approved wording (7 Oct):
  "This expression can be written (A ⊕ B)·C·D·Ē, where A ⊕ B = A·B̄ + Ā·B (XOR: one or the other, but not both). Play
  Boolean Blitz →", in KaTeX. XOR is introduced nowhere else in the game; the verifier checks the identity, the gloss
  and the rendered line, and a third plant (XOR with no definition) is caught.
- **Contract LH (#133, home lane, merged 18:44) landed while this was being prepared:** eigenvector-engine declares
  its maffs-lock-hint (`{}`: the generic driver plays it) and comes off the remaining list above, so CI now judges it
  in full. Each later game does the same in its own PR.
- **Delete each `claude/keen-cray-ypsime-<game>` branch once its game has merged (Jon).**

## 2026-10-07 (cloud): game 18 Factor Theorem (PR #130, merged); NEXT = merge #130, then the six queued games

- **New instance, fresh container (18:00 UTC).** The old worktrees and `/home/user/queue-patches/` were gone. Jon
  approved the old session pushing the six queued games to their own branches; this lane picks each up from its
  branch, one PR per game, under the usual merge rules. Do not rebuild them.
- **Jon's rulings (7 Oct, 18:00):**
  - **The lane question:** #130 does not edit `scripts/check-answer-lock.py`; the home lane moves cloud-lane games to
    MIGRATED. #130's MIGRATED and HINTS edits were dropped when main (#132) was merged in (the file is main's,
    byte for byte). The two in-game fixes stay: suvat loads answer-lock.js after next-control.js, and factor-theorem's
    resize debounce carries `// lock-ok:`. **The home lane will move per-game hints into each game's own file under a
    coming contract: build nothing around the central HINTS.** The two driving hints the old session wrote and
    passed with, as data for the home lane (suvat: Level 4, the equation is picked, then a wrong typed answer;
    factor-theorem: the Practice tab, a wrong answer in every box, Check pressed until the scaffold's three attempts
    are used):

```python
    # suvat (Level 4: pick the equation, then type the answer; question_answered fires on the typed answer).
    # The answer waits out MaffsLock's 300 ms window on the real clock before it presses CHECK.
    'suvat': {
        'level': 'level4',
        'ready': "document.getElementById('mainGame').classList.contains('visible')",
        'answer': ("return (async () => {"
                   "  const vis = id => { const e = document.getElementById(id); return e && e.offsetParent !== null; };"
                   "  const real = ms => new Promise(r => { const t = performance.now(); (function f() {"
                   "    if (performance.now() - t >= ms) r(); else requestAnimationFrame(f); })(); });"
                   "  for (let k = 0; k < 60; k++) {"
                   "    if (vis('phase2') && !document.getElementById('calcInput').disabled) {"
                   "      await real(350); document.getElementById('calcInput').value = '9999';"
                   "      document.querySelector('#phase2 .calc-btn').click(); return; }"
                   "    const b = [...document.querySelectorAll('#eqChoices .eq-btn')].find(e => !e.disabled && e.dataset.val === currentQ.equation);"
                   "    if (vis('phase1') && b) { await real(350); b.click(); }"
                   "    await real(60);"
                   "  }"
                   "})();"),
        'surface': '#phase2',
    },
    # factor-theorem: the Practice tab; a wrong answer in every box, Check pressed until the question is marked
    # (a scaffold has three attempts).
    'factor-theorem': {
        'start': "document.querySelector('[data-section=\"practice\"]').click()",
        'ready': "document.getElementById('sec-practice').classList.contains('active') && !!document.getElementById('checkBtn')",
        'answer': ("return (async () => {"
                   "  const real = ms => new Promise(r => { const t = performance.now(); (function f() {"
                   "    if (performance.now() - t >= ms) r(); else requestAnimationFrame(f); })(); });"
                   "  await real(350);"
                   "  for (let k = 0; k < 3; k++) {"
                   "    const c = document.getElementById('checkBtn');"
                   "    if (!c || c.style.display === 'none') return;"
                   "    document.querySelectorAll('#practice-area input.answer-input:not([disabled])').forEach(e => { e.value = 'zz'; });"
                   "    c.click();"
                   "  }"
                   "})();"),
        'surface': '#practice-area .q-card',
    },
```

  - **Factor Theorem scaffold:** keep "every value of the blanks that makes the line true" (Q6 also takes -2, -3).
  - **Truth Buster:** Next below the fold at 320x568 is filed as an open MEDIUM register entry citing canon 7.6.1;
    it does not block the fix PR.
  - **TWSYF [27]:** keep XOR only if the game introduces it before [27]; otherwise rewrite with AND/OR/NOT and list
    the wording in the PR for Project Claude.
- **The queue after #130, in order (one PR each; register entries to close):**
  1. eigenvector-engine: t6-001, -002, -004, -005, f0-001..007 fixed; t6-003 stays open.
  2. truth-will-set-you-free: t6-001, -002, -003, -005 fixed; file and fix t6-006 ([6]'s duplicate distractor);
     t6-004 stays open.
  3. trig-identity-duel: t2-007, t2-010.
  4. binomial-blaster: t5-017.
  5. partial-fractions-duel: t5-007.
  6. truth-buster: t3-013; file the 320x568 Next entry (above).
- **Each later game loads answer-lock.js:** under #131 it is reported, not failed. Run `check-answer-lock.py --game
  <slug>` (with KaTeX served) before each PR and give the home lane what it finds, in the PR and here.
- **Factor Theorem (unchanged from the PR):** typed answers looked up in ACCEPTED (canon 7.1 pattern, R12), written by
  `scripts/verify-factor-theorem.py --write` (E): one box per blank, matched by position; numbers via MaffsAnswer;
  algebra through canon(). Project Claude's T4 (a = -19, b = 30; (x - 3)(x - 2)(x + 5)). Q24/Q38/Q20 asks, Q22 hint,
  Learn ex. 4 candidates, test prompts' raw TeX (t5-019, new). MaffsLock. Open: t5-004/-005 (free text), -008/-009
  (exam-vocab.js), -013 (4), -014/-015 (design), -016/-017 (5), -018 (MaffsNext advance: check-teacher-invite's
  FT_STEP clicks only `.next-q-btn`, home lane).
- **Gotchas:** MaffsLock's 300 ms fresh window drops clicks a sweep makes right after a render: set
  `MaffsLock.FRESH_MS = 0` in sweeps and keep the real window in the lock test. A double click must be tested with
  `page.mouse` at the control (clicking a detached element twice fires its old listener). A fresh container has no
  KaTeX: fetch `registry.npmjs.org/katex/-/katex-0.16.9.tgz` (its `package/dist`). A `sitecustomize.py` on
  PYTHONPATH that adds a KaTeX route to every new context lets the teacher-line and answer-lock checks pass, but it
  makes every verifier that routes for itself (sync API: suvat, factor-theorem, check-resit-page) time out on `load`.
  Run those bare, with `--katex-dir` where the verifier has it.

## 2026-10-07 (cloud): game 17 SUVAT Selector (PR #128); #127 Force Resolver merged; NEXT = factor-theorem

- **Force Resolver (PR #127) merged** at 16:15 on a green Gate; main green after #126 before it.
- **SUVAT Selector:** every typed step marked by MaffsAnswer (`exact`, or `decimal` at the step's stated `dp`; the
  prompt says the precision; phase 0 to 2 d.p.); local parseFloat-and-tolerance gone (t5-006). Keys recomputed both
  ways: from the exact data, and from the values the student is shown (rounded chips, the previous step's key); a
  step's precision is the finest at which both round to the key (al[32] 1 d.p., al[18] 2 d.p., al[41]/[48] whole
  numbers, al[49] 1 d.p.; t5-007). Project Claude's sprinter (u = 8; t5-001) and ALEVEL[39] (2.02 s, 19.8 m/s;
  t5-003). v_y keyed -0.32 (t5-002); ALEVEL[22] says it lands at 3 s (t5-008); a question counts correct only if
  every typed step is (t5-009); wrong answers show the answer and wait for MaffsNext; ALEVEL[3]'s second root
  explained (t5-011). **MaffsLock (#125) adopted (Jon, 7 Oct 17:30):** lock first in every answer handler,
  fresh() on every render, MaffsLock.timer for every delay, endGame through finishOnce, newSession on Start;
  t5-004 closed. `scripts/verify-suvat.py` (E) adds the class-1 test (double click + Enter on CHECK mark once,
  two equation choices count once, one submit). Open: t5-005 (4), t5-010 (5).
- **Standing rule from Jon (7 Oct 17:30): MaffsLock is on main; every game fixed from now on adopts it and closes
  its class-1 entries in the same PR.** `check-answer-lock.py` (F1 part b) is not on main yet, so each verifier
  tests the lock itself.
- **Next: factor-theorem** (worktree `/home/user/ft-work`, branch claude/ft-prep, findings read, no edits):
  ACCEPTED-list typed answers (R12) and Project Claude's T4 (a = -19, b = 30; (x - 3)(x - 2)(x + 5) any order);
  t5-004/-005 (free text) and t5-008/-009 (exam-vocab.js, shared) stay open and get listed.

## 2026-10-07 (cloud): game 16 Force Resolver (PR #127); #126 Moments Master merged; NEXT = suvat

- **Moments Master (PR #126) merged** at 16:01 on a green Gate; main green after #124 before it.
- **Force Resolver:** `scripts/verify-force-resolver.py` (E), the Moments Master verifier's shape plus: options written
  as expressions evaluated (25 root 3 N, 10 tan 30 N) and a rounded figure counted equal to the expression it rounds
  from (43.3 N beside 25 root 3 N); figures quoted in text keys recomputed (FIGS) and their verdict required
  (VERDICT: "Yes", it slides). Project Claude's truss for level4[18] (12.8 kN) exactly. From the items' own data:
  level4[8] 1.40 m/s^2 (t5-002), alevel[47] 5 N (t5-004), alevel[32] "Yes" (t5-007), level4[7] worked with the
  stated 9.81 (1224 N; t5-011), alevel[31] "Equilibrium" (t5-012), alevel[35] g stated (t5-013); value-equal
  distractors replaced by named errors (t5-005, t5-006, f0-001, t5-014: 50 root 3, 1 N, "Undefined (tan 90)", 2.5 N,
  4.33 N, 266 N; for review); the given trig values stated where a key used them (alevel[11], level4[1]); 49.8 not
  49.7 (level4[15]). Wrong answers show the answer and working, then MaffsNext. Open: t5-008 (1), t5-009 (4),
  t5-010 (5).
- **Prepared locally, not pushed:** suvat (`/home/user/sv-work`, branch claude/sv-prep): typed steps on MaffsAnswer
  at a stated precision (the finest at which the exact data and the values shown both round to the key: al[32] 1 d.p.,
  al[18] 2 d.p., al[41]/[48] whole numbers), Project Claude's sprinter and ALEVEL[39], wrong answers wait for Next,
  a question correct only if every typed answer is; `scripts/verify-suvat.py` (E).

## 2026-10-07 (cloud): game 15 Moments Master (PR #126); #124 Linear Equation Solver merged; NEXT = Force Resolver

- **Linear Equation Solver (PR #124) merged** at 15:47 on a green Gate, after main's runs following #122 (re-run;
  the first attempt lost its Gate job in GitHub's 15:05-15:17 write errors) and #123 were green.
- **Moments Master:** `scripts/verify-moments-master.py` (E): every numeric key from the item's own data (SymPy;
  KEYS), distractors equal in value to the key (5 kW = 5000 W) or to each other, named-error REASONS for the items
  rewritten, numeric claims in keys and working lines, "Same beam" items quoting their predecessor, text keys pinned
  (REVIEWED, --print-pins); Chromium at 390 and 320: every option clicked, no raw TeX, no sideways scroll. Project
  Claude's data for :128, :134, :147, :172/:173 exactly; :141 rekeyed 75 N; :180's 5 kW replaced by 524 W
  (P = 2 pi N T / 60 with 100 taken as rpm; for review). Filed and fixed: t5-014 (premises: the trapdoor uniform,
  the level4 cable beam light with a vertical cable), t5-015 (R_B, T_A shown raw by textContent: ctx and ask now
  through MaffsText). Wrong answers show the answer and the item's working line, then MaffsNext (no stored
  explanations exist: fuller ones would be Project Claude content). Open: t5-009 (1), t5-010 (4), t5-011 (5),
  t5-012 (the gate premise: Jon).
- **Prepared locally, not pushed:** Force Resolver (`/home/user/fr-work`, branch claude/fr-prep). suvat is planned
  (typed answers onto MaffsAnswer with a stated precision per step; keys from the values the student is shown).

## 2026-10-07 (cloud): Linear Equation Solver, Jon's "optimal move" contract (PR #124); #115 Proof Builder merged; NEXT = moments-master

- **Proof Builder (PR #115) merged**; main's full run after it green (and after #117).
- **Jon's list (7 Oct, this session):** proof-builder (done), linear-equation-solver, then with Project Claude's
  replacement data moments-master, force-resolver, suvat, factor-theorem, eigenvector-engine, then
  truth-will-set-you-free; then (Jon, 15:27) follow-ups to merged games, one PR each: trig-identity-duel gcse[16]
  replaced + timer to hidden count-up; binomial-blaster alevel2[36] replaced; partial-fractions-duel alevel[22]
  replaced (each clears its B3 ledger entry); truth-buster Next visible at 390x844 on every item. The replacement
  data is in Jon's 7 Oct paste (the session's first message); if it is not to hand, ask Jon.
- **MaffsLock (`schools/assets/answer-lock.js`) is not on main yet:** class 1 stays open. Once it lands, adopt it in
  each game fixed (lock, fresh, timer, finishOnce) and close that game's class-1 entries.
- **Linear Equation Solver:** `scripts/gen-linear-moves.py` (depth-3 search, iterative deepening, under 1 s) writes
  MOVES between its own GENERATED markers: per line, every optimal move (one per distinct line), one slower move
  where one exists, named errors (one-side, carry, xonly, constnot) to fill four. Options show the move and the line
  it gives with the number side unevaluated (x = 12 - 7), so a one-side error can be shown and the answer phase
  still asks for the value. The trail follows the student's route (295 lines for 141 questions). Amber = 12.5 (half
  the 25 at stake), streak kept; amber and red wait for MaffsNext. Hints and feedback through MaffsText (t4-002).
  `gen-linear-equations.py` no longer writes the superseded per-step `opts`/`hint` (QUESTIONS otherwise identical)
  and uses a repo path. `scripts/verify-linear-equation-solver.py` (group E, ~40 s): its own TeX parser and search,
  SymPy for every value; every option clicked in Chromium; Jon's four cases tapped; page == generator. On main's
  file it fails on exactly r-001 (18 options in the 14 questions), r-002 (49) and t4-002 (11).
  - **Decision to review:** "fractions" in the tie-break means fractional constants, not coefficients (Jon's own x2
    example on x/2 + 5 = 11 needs x/2 = 6 to count as fraction-free). Under that reading every keyed move is
    optimal (STOP IF not triggered).
  - Four lines (-x = c in U1-U4) have 3 options: no fourth honest one exists.
  - Open: t4-003 (class 1).
  - **Gotcha (MOVES size):** the first version stored each option's feedback sentence (MOVES 280 KB, page 348 KB)
    and tier 4's extraction of this one game ran for minutes: the render-site evaluator calls `literal_to_json` on a
    literal every time it resolves an identifier (about 350 calls a second, no cache). Options are now compact arrays
    and the page words the feedback from their fields (MOVES 92 KB, page 159 KB, extraction 8.5 s). A large
    generated literal in any game will hit the same cost.
- **For the home lane:** content group B4 ran 243 s on main's run after #117, over canon's 4-minute cap; this
  verifier went in E (133 s on that run) instead. `bank_common.literal_to_json` is re-run per identifier
  resolution; memoising it by node would make large literals cheap (shared code). SR-13's scoring sentence
  ("scores full marks") needs a note for Jon's 7 Oct amber rule.

## 2026-10-07 (cloud): game 13 Proof Builder (PR #115); #112 Dimension Checker merged; NEXT = Linear Equation Solver (Jon's 7 Oct contract)

- **Dimension Checker (PR #112) merged** on a green Gate; main's full run after it green.
- **Proof Builder (PR #115):** `scripts/verify-proof-builder.py` (B4, declared by its own `# ci-line:` header; no workflow edit): refutation predicates for every counter-example option, SymPy induction stages, sorter orders, rendering at 390px. One renderer `M()` and 79 strings migrated to `\( \)` (132 B7 + 2 B11 ledger entries cleared). The options' TeX test is written as `includes()` at each call site, because tier 4 cannot decide a helper (`isTeX(v)`) and crashes on a regex `.test()` (game 8's note). Open: t5-014, t5-016 (1), t5-021 (5), t5-023 (per-mode boards: Jon), t5-024 in part (4).
- **Main went red once after #109** (13:16): group E, Like Terms Collector item 1, the same failure as on #106 and #88's first run (third time today). One re-run of the failed job was green. It does not reproduce here (0 of 24 runs, 8 at a time; this sandbox has Playwright 1.56 and no gstatic, CI has 1.63 and both). Home lane: the verifier hardening proposed on #106.
- **Original contract list done.** Everything left open is a shared class (1, 4, 5, B11), a decision for Jon (TID timer, Integration Duel + c, Proof Builder per-mode boards, Truth Buster fold), or needs new content (duplicate items in TID, BB and PFD; Truth Buster video IDs to check from home). Skipped until Project Claude supplies data: moments-master, force-resolver, suvat, factor-theorem, eigenvector-engine, truth-will-set-you-free.
- **Next: Linear Equation Solver** (Jon's contract of 7 Oct, added after Proof Builder): "What is the optimal move here?", every tied optimal move full marks, a valid but slower move amber (half, streak kept), wrong options named real errors; option sets generated by `scripts/gen-linear-moves.py` (depth-3 search) between GENERATED markers; the verifier re-derives every class with SymPy; the SR-13 note in canon.

## 2026-10-07 (cloud): game 12 Dimension Checker (PR #112); #109 Curling Friction merged; NEXT = Proof Builder

- **Curling Friction (PR #109) merged** on a green Gate; main's full run after it green.
- **Dimension Checker (PR #112):** `scripts/verify-dimension-checker.py` (B4, declared by its own `# ci-line:` header; no workflow edit): dimension algebra for keys, options and every worked step; MaffsOptions, MaffsNext. Open: t5-003 (1), t5-005 (5), t5-006 (4).
- **Next:** Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 11 Curling Friction (PR #109); #107 Integration Duel merged; NEXT = Dimension Checker

- **Integration Duel (PR #107) merged** on a green Gate; main's full run after it green.
- **Curling Friction (PR #109):** `scripts/verify-curling-friction.py` (B4): exact targets per item; no negative "speed"; friction only on sliding stones; MaffsNext. t5-008 filed and fixed. Open: t5-003 (1), t5-004 (4), t5-005 (5).
- **CI lines (Jon, 7 Oct):** from when contract V merges (home lane), a cloud-lane verifier declares its CI group
  with a `# ci-line:` header in the verifier file itself, and the PR does not edit `.github/workflows/check-site.yml`
  at all. Until then: one workflow line per PR, and rebase on main before merging.
- **Next:** Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 10 Integration Duel (PR #107); #106 Differentiation Duel merged; NEXT = Curling Friction

- **Differentiation Duel (PR #106) merged** on a green Gate; main's full run after it green.
- **Integration Duel (PR #107):** `scripts/verify-integration-duel.py` (B4): antiderivatives checked by differentiating, c held as a symbol, ln x + c sampled where it is right. Missing + c named in feedback (Jon may rule it right). B11 (5) cleared. Open: t5-010 in part (class 4).
- **Like Terms Collector's verifier flaked once on #106** (group E; item 1 typed 8.9/6.5, `MARK()` null, empty feedback;
  it passed 5 of 5 locally and on the one re-run). Same item and shape as #88's first-run flake. Home lane: after
  `page.fill`, wait for the boxes to read the typed values and for the feedback panel's class before reading the mark.
- **#103 split content group B into B1-B4**; the cloud lane's verifiers go at the end of B4, where #103 put them.
  A branch prepared before a ledger change on main conflicts on `data/check-ledger.json`: take main's ledger and
  replace only that game's record (the scratch helper did this per commit).
- **Next:** Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 9 Differentiation Duel (PR #106); #105 Partial Fractions Duel merged; NEXT = Integration Duel

- **Partial Fractions Duel (PR #105) merged** on a green Gate; main's full run after it green.
- **Differentiation Duel (PR #106):** `scripts/verify-differentiation-duel.py` (B4): implicit items compared on the curve; explanations must state the answer. B11 (9, five of them added by #99) and B7 (1) ledger entries cleared; t5-013/014 filed and fixed. Open: t5-010, t5-011 (class 4).
- **Next:** Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 8 Partial Fractions Duel (PR #105); #104 Binomial Blaster merged; NEXT = Differentiation Duel

- **Binomial Blaster (PR #104) merged** on a green Gate; main's full run after it green.
- **Partial Fractions Duel (PR #105):** `scripts/verify-partial-fractions-duel.py` (B4): every Find solved from its stated form; valid equivalent forms removed. Open: t5-007 (class 1), t5-009 (class 4). New B3 ledger entry: the Find B / Find C pair for 1/(x(x+1)(x-1)) now share stem, options and key (needs a new item).
- **The tier 4 crash recorded under game 6 has a known cause (home lane: shared code).** `_SiteEval.regex()` in
  `bank_common.py` returns `(pattern, glob)`, and the `.test` branch of `_SiteEval.call()` calls `.search` on that
  tuple, so any `/re/.test(x)` the evaluator reaches raises. Taking the pattern from the tuple fixes it. Also: a
  guard written as a page helper (`isTeX(v)`) is never decided, so both branches count; until the evaluator can
  look inside, the cloud lane writes such guards as `includes()` at the call site.
- **Next:** Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 7 Binomial Blaster (PR #104); #102 Trig Identity Duel merged; NEXT = Partial Fractions Duel

- **Trig Identity Duel (PR #102) merged** on a green Gate; main's full run after it green.
- **Binomial Blaster (PR #104):** `scripts/verify-binomial-blaster.py` (B4): three-term estimates as the ask states, rounding-ambiguity check, MaffsOptions. Open: t5-017 (class 1), t5-018 (class 4), t5-022 in part (portal card: home lane). One B3 duplicate (needs a new item).
- **Next:** Partial Fractions Duel, Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 6 Trig Identity Duel (PR #102); #101 Component Crusher merged; NEXT = Binomial Blaster

- **Component Crusher (PR #101) merged** on a green Gate; main's full run after it green.
- **Trig Identity Duel (PR #102):** `scripts/verify-trig-identity-duel.py` (B2): every option read into SymPy. Compound-angle keys, 85.9°, identical options fixed; t2-011 filed and fixed. Open: t2-007 (class 1), t2-010 (timer: Jon's decision). gcse[16] duplicates gcse[12] (B3; needs a new item).
- **For the home lane (shared code, not edited here):** `bank_common.py`'s render-site analysis crashes
  (`AttributeError: 'tuple' object has no attribute 'search'`, in `call`) on a regex literal's `.test()` in some
  positions: inside a template-literal expression (Component Crusher's first CI run) and `/[\\^_{}]/.test(...)`
  (Proof Builder, found locally). Extraction then fails and every ledger entry reads as stale. The cloud lane works
  round it in each game (a named function, or string methods); the parser fix is the home lane's.
- **Local tier 4 in the cloud sandbox works:** serve KaTeX from the npm tarball (route the jsdelivr KaTeX URLs to
  `package/dist`), run `extract-banks.py`, then `check-banks.py --ci`; about 95 s with 4 workers.
- **Next:** Binomial Blaster, Partial Fractions Duel, Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 5 Component Crusher (PR #101); #100 Expectation Station merged; NEXT = Trig Identity Duel

- **Expectation Station (PR #100) merged** on a green Gate; main's full run after it green.
- **Component Crusher (PR #101):** `scripts/verify-component-crusher.py` (B2): keys from what is shown, diagrams measured from the canvas, marking through MaffsAnswer. Level 4 data shown; prompts' maths in `\( \)` (31 B7 ledger entries cleared). Open: t4-005 (class 1), t4-011 (class 5), t4-014 in part (class 4).
- **Next:** Trig Identity Duel, Binomial Blaster, Partial Fractions Duel, Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 4 Expectation Station (PR #100); #98 Trig Worms merged; NEXT = Component Crusher

- **Trig Worms (PR #98) merged** on a green Gate; main's full run after it green.
- **Expectation Station (PR #100):** `scripts/verify-expectation-station.py` (B1): all 180 Stage 3 cards reviewed with checks from the distribution ("most" = more than half); Stage 1 marked exactly. t2-001..016 fixed, t2-018/019 filed and fixed; open: t2-017 (class 1).
- **Next:** Component Crusher, Trig Identity Duel, Binomial Blaster, Partial Fractions Duel, Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 3 Trig Worms (PR #98); #97 Truth Buster merged; NEXT = Expectation Station

- **Truth Buster (PR #97) merged** on a green Gate; main's full run after it green.
- **Trig Worms (PR #98):** `scripts/verify-trig-worms.py` (group B2, ~20 s). The generator is rebuilt from a
  `POOL` of servable outcomes (1,204; no retry); every outcome is recomputed with mpmath from the values shown,
  at the stated precision ("to the nearest degree", "to 1 decimal place"); every distractor is a named error and
  the feedback names it; only the two given sides are labelled and the triangle is drawn at one scale.
  t1-001..t1-004 fixed; nothing left open.
- **Next:** Expectation Station, then component-crusher, trig-identity-duel, binomial-blaster,
  partial-fractions-duel, differentiation-duel, integration-duel, curling-friction, dimension-checker,
  proof-builder (all prepared on local worktrees /home/user/*-work, not pushed; their PR texts and register
  specs are in this session's scratchpad).

## 2026-10-07 (cloud): game 2 Truth Buster (PR #97); #96 Spot the Error merged; NEXT = Trig Worms

- **Spot the Error (PR #96) merged** on a green Gate; main's full run after it green.
- **Truth Buster (PR #97):** `scripts/verify-truth-buster.py` (group B1). Keys are reviewed judgements, with the
  words a statement must contain for its key to hold (`needs`, SR-18) and SymPy where a key can be computed;
  every reveal figure is in `FIGURES` (an unlisted `=`, `<`, `>` fails); dates and counts in `SOURCED`.
  t3-001..012 fixed. Open: t3-013 (class 1), t3-014 (class 5/4), t3-015 in part: the 21 Learn More video IDs
  (YouTube is refused from the cloud sandbox: check them from home) and Next below the fold (shorter reveal
  text, Project Claude, or a layout ruling).
- **Next:** Trig Worms, then expectation-station, component-crusher, trig-identity-duel, binomial-blaster,
  partial-fractions-duel, differentiation-duel, integration-duel, curling-friction, dimension-checker (all
  prepared on local worktrees /home/user/*-work, not pushed), then proof-builder (in progress). A lost container
  loses them: redo from the register.
- **Gotchas:** a PR that clears a fixed B7/B11 finding also clears its entry in `data/check-ledger.json` (dump
  with `indent=1, ensure_ascii=False, sort_keys=True`, as `check-banks.py` does), or CI fails it as stale. With a
  workflow edit, `check-changed.py` selects every check (about 45 minutes here): run it in the background with a
  long timeout, never the default 30 minutes (the Truth Buster run was cut off there).

## 2026-10-07 (cloud): unlisted-games contract, game 1 Spot the Error (PR #96); NEXT = Truth Buster

Jon's contract of 7 Oct (cloud lane): fix the unlisted games one per PR, each under a new verifier, in this order:
spot-the-error, truth-buster, trig-worms, expectation-station, component-crusher, trig-identity-duel,
binomial-blaster, partial-fractions-duel, differentiation-duel, integration-duel, curling-friction,
dimension-checker, proof-builder. Shared classes stay open: 1 (answer lock, F1), 4 (?level resolver, F2),
5 (bank size), B11 parser gaps (F0). Skipped until Project Claude supplies data: moments-master, force-resolver,
suvat, factor-theorem, eigenvector-engine, truth-will-set-you-free. Other owners: linear-equation-solver,
screening-room, glorious-gantt.

- **Spot the Error (PR #96):** `scripts/verify-spot-the-error.py` (group B2, ~9 s). All 19 register entries
  fixed (t1-001..014 plus the re-audit's t1-015..019); nothing left open. 16 items reworded (listed in the PR
  for Project Claude). Model: the key is the first step that departs from correct working; later steps carry it.
- **Prepared on local branches, not pushed** (worktrees under /home/user/*-work, gone with this container): the
  next games are rebuilt from their audit entries in the same order. If this container is lost, redo from the
  register; the PR descriptions list the content choices.
- **Gotchas:**
  - A reviewed verdict (a step judged an error, a statement judged true) reads no text, so each verifier that
    holds verdicts pins each item's content hash (`REVIEWED`, `--print-pins`): any edit fails until re-reviewed.
  - The self-tests count a plant as caught only by a check other than that pin.
  - Locally, the KaTeX CDN is refused: KaTeX games' verifiers take `--katex-dir` (the npm tarball's dist/).
    `check-changed.py` here always fails seven checks for environment reasons (PR #96 lists them).
  - `extract-banks.py` through the sandbox wrapper reports component-crusher's 34 B7 entries stale even on main:
    do not trust a local tier 4 run for B7; read CI's.
  - A shared TeX-to-SymPy reader would serve several of these verifiers (each carries its own small one, since
    the cloud lane does not add shared modules): a home-lane candidate.

## 2026-10-07: the lane starts (written by the home lane, which set up the lanes)

- No cloud session has run since the lanes were split. The last cloud work was 6 Oct 2026 (#85 audit tranches 1-2
  and two games unlisted; #86 Core Maths Paper 1), recorded in CLAUDE.md's history.
- The unlisted games and their open findings: `docs/audits/REGISTER.md` ("By game", Listed = unlisted) and the
  roster's Unlisted section. Each has its relist checklist in `docs/todo.md` §1.53-§1.75.
- **Next:** Jon's first cloud-lane contract names the game.
