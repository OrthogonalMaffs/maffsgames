# MaffsGames to-do

**Repository history:** this repository started fresh on 2 Oct 2026. Any PR number or commit hash from before then, here or in canon and CLAUDE.md, refers to `OrthogonalMaffs/maffsgames-archive` (archived, read-only). This repository's PRs are #1–#31 so far.

History: `git log -p docs/todo.md`.

**Snagging list:** small, testable issues Jon finds while play-testing live games go in
`docs/snagging-list.md`, not here — check it alongside this file; an entry graduates into this
file's numbered sections only once it's bigger than a one-line fix.


## START OF NEXT SESSION

This file is the single backlog (AGENTS.md); the lane handovers hold only work in flight. Order: by priority (canon §0.2).
This file's old START block (last updated 6 Oct 2026) is in `docs/history/todo-done.md`, word for word.

## 1. Live bugs and false claims

Done rows moved word for word to `docs/history/todo-done.md` ("Done rows from §1 and §3", 10 Oct 2026, TODO-SLIM); their numbers still resolve there: 1.3, 1.6, 1.7, 1.9, 1.10, 1.13, 1.15, 1.18, 1.19, 1.20, 1.21, 1.22, 1.28, 1.29, 1.31, 1.41, 1.42, 1.43, 1.44, 1.45, 1.46, 1.47, 1.49, 1.50, 1.55, 1.57, 3.13. Closed by LIVE-BUG-RECHECK (8 Nov 2026), under that heading there: 1.8, 1.24, 1.30, 1.40. Closed by fix PRs (Nov 2026), under that heading there: 1.32, FORGE-HINT-SPACES, 1.37, 1.38, CAST-AWAY (from §3). Closed by RULES-EMULATOR-TEST (11 Nov 2026), under that heading there: FIREBASE-ESCAPING. Closed by HOME-QUEUE-1111 (11 Nov 2026), under that heading there: PACK-APPROVED, STAGE-EXIT-LABEL. Closed by PP-AA-STACK (12 Nov 2026), under that heading there: PP-AA-OVERFLOW.

| # | Item | Owner |
|---|---|---|
| 1.14 | **`test-the-claim`: every answer key recomputed. FIXED 30 Sep 2026.** It started as P3's impossible critical region (Po(3), two-tailed 5%: the region is X ≥ 8 only, with no lower region, but the key was "0 or 7"). The new independent verifier, `scripts/verify-test-the-claim.py` (in CI), recomputes every probability, critical value, p-value and verdict from each item's raw parameters, and found **16 of 48 items wrong**. Two decisions were backwards: **P7** (the true P(X ≤ 9) = 0.0433, so H₀ is rejected; the game marked the right answer wrong), and **Step 6's "Action" on all 24 items that reject H₀** (it keyed "reject the claim that ⟨H₁⟩"). Also: wrong displayed probabilities in B6, B8, B9, B11, P5, P6, P7 and P11; wrong boundaries in B6, B8, P3, P5, P6 and P7; wrong p-values in B6, B8, B9, P5, P7, P9 and P11; draft prose in B8, P9 and P11; five PMCC cells and C5 disagreeing with the Edexcel booklet's Table 8 (the booklet and exact computation agree in all 260 cells); no p-value and no explanation on all 24 Normal and correlation items ("undefined" on screen); the correct Step 6 conclusion shown twice on B8, B10, B12 and P8; and no way to enter "no lower critical region" (P3, B11, P9). All fixed under Jon's rulings of 30 Sep. Two-tailed items now compare the **probability in the tail with half the significance level**, labelled that way at Steps 3 and 4. **Full record, stated → corrected for every field, the 24 generated explanations for Jon's review, and the evidence: `docs/test-the-claim-verification.md`.** | **Follow-up, 30 Sep (later):** Step 6 lists shuffled, and correlation items give their p-value in the scenario (doc §"Follow-up"). Re-checked 2026-11-08 on main f8a287b4: PART — FIXED: every key recomputed by `scripts/verify-test-the-claim.py` (in the public repository since ab701b4c), green in main run 42512282061; the owed `--live` check ran today: `check-site.py --live --only games/test-the-claim/` OK, and the deployed page is byte-identical to main's (SHA-256 140404ab…). Remains: Jon's review of the 24 generated explanations (`docs/test-the-claim-verification.md`). | — fixed; **Jon** — review the 24 generated explanations; **the `--live` check is owed** (the sandbox cannot reach the site) |
| 1.26 | **Hard-coded distribution values in four more games: the class of §1.14. `normal-navigator`, `core-maths-paper2a` and `maths-court` DONE 30 Sep 2026; `regression-rumble` STOPPED for Jon (37 of 40 scenarios fail).** Found by the class check of 30 Sep 2026 (none shares data or code with `test-the-claim`). **`normal-navigator` — DONE:** `scripts/verify-normal-navigator.py` (in CI) recomputes all 47 questions with `NormalDist` from their own prose (the game's `phi()` is never used) and renders each on the real page. It found **9 of 47 wrong**; Jon ruled to proceed (calculator values throughout). Stated → corrected: Q18 `:218` k = 60.2 → **60.3** (50 + 1.2816 × 8 = 60.2528; shade 60.24 → 60.25); Q23 `:225` P(bolt rejected) = 0.0456 → **0.0455** (2Φ(−2) = 0.045500; 0.0456 was 2 × the rounded 0.0228); Q14 `:212` step "0.8413 − 0.1587 = 0.6827" → "0.84134 − 0.15866 = 0.68268 ≈ 0.6827"; Q15 `:213` and Q36 `:247` "0.9772 − 0.0228 = 0.9545" (which is 0.9544) → "0.97725 − 0.02275 = 0.95450 ≈ 0.9545"; Q16/Q17 steps put on the same 5-d.p. convention (they were arithmetically right); Q37 `:248` "Same process. 1000 items…" (no distribution, and the pool is shuffled) → self-contained, "to the nearest whole number", key 45 → **46** (1000 × 0.04550026 = 45.50026), 45 kept as the truncation distractor with a misconception naming it, the old distractor "5" dropped to make room; Q38 `:251` added "Assume equal numbers of men and women." (without it "Cannot determine" was arguably right) and the unfinished "so equal density..." step rewritten as φ(1)/6 ≈ 0.0403 vs φ(1)/7 ≈ 0.0346; Q29 `:233` and Q39 `:252` `correct_override` folded into `correct` (both keys were right: μ = 25, σ = 5; μ = 16.55 → 17), and `correct_override` no longer appears in the bank (B10 ledger entries retired); Q35 `:244` misconception "for P(X > 100), also use 100.5" → "use 100.5". **Also fixed on Jon's ruling:** the μ/σ labels under the curve gave the answer away on Q29, 30, 31, 34, 39, 45 (`hideParams`: they read "?" until answered); two-region questions Q23, 29, 33, 37, 46 now shade both regions (`drawBell` takes a list of regions). **`regression-rumble`:** 28 scenarios with a hard-coded PMCC critical value (`cv`, 5% two-tailed), 14 of them also stating r beside its Σ sums, so r is recomputable. **`core-maths-paper2a`:** 7 of its 18 §3.5–3.6 items carry a Normal probability or a z critical value. **`maths-court`:** 1 item (`:575`, B(20, 0.5), P(X ≥ 15) = 0.0207, spot-checked correct). `docs/test-the-claim-verification.md` §"Class check" has the exclusions. **30 Sep 2026 (night), the other three:** one shared module, `scripts/stats_common.py` (exact binomial and Poisson, `NormalDist`, PMCC and least squares from sums or data, PMCC critical values from the exact null distribution, half-up rounding, a worked-step arithmetic checker; 42 unit tests against textbook values, in CI). `verify-test-the-claim.py` and `verify-normal-navigator.py` now import it; their output, normal and `--verbose`, is byte-identical before and after. **`core-maths-paper2a` — DONE, 0 of 27 statistics items wrong, no correction.** `scripts/verify-core-maths-paper2a.py` (in CI) recomputes every §3.5–3.7 value from its stem, checks every item's options, arithmetic and rendering (working hidden until answered; Q1's bars drawn at the stated 72/68/74/71), 5/5 injected faults caught. Note for Jon, not a failure: Q14 keys 2.5% by the 68-95-99.7 rule (calculator 2.28%); it is still the nearest option and the stem says "approximately". **`maths-court` — DONE, 0 wrong, no correction.** `scripts/verify-maths-court.py` (in CI) recomputes mc_core_001 (E = £1.50), 002 (68%), 006 (P(X ≤ 8) = 0.3120) and 009 (P(X ≥ 15) = 0.0207), arithmetic-checks every case's correct working and judge's summary, and renders each case (no card marked, summary hidden, before the verdict); 4/4 faults caught. WARN for Jon: mc_core_009 asks "Is the coin fair?" (two-tailed) but tests H₁: p > 0.5; the verdict is the same two-tailed (p = 0.0414). **`regression-rumble` — STOPPED (STOP IF: more than 10% fail), nothing corrected.** `scripts/verify-regression-rumble.py` (NOT in CI until the data is ruled) fails 37 of 40 scenarios, 62 findings: (1) Level 4's stated sums are impossible for 8 of 14 (|r| > 1: L4_1 1.30, L4_2 1.08, L4_6 1.08, L4_8 1.32, L4_9 1.37, L4_10 1.15, L4_11 1.34), and the stated r disagrees with the sums on 5 more (L4_3 −0.76 vs −0.55, L4_4 0.91 vs 0.81, L4_5 −0.71 vs −0.90, L4_7 −0.88 vs −0.74, L4_13 0.93 vs 0.77, L4_14 −0.87 vs −0.98; L4_12 0.74 vs 0.728 is within rounding); L4_3 is keyed significant but |r| = 0.55 < 0.6319; L4_5's prediction is 20, the line gives 21; L4_3's line prints "y = 13.17 − 0x" (b = −0.0049 to 2 d.p.). (2) Every core and A-level scatter contradicts its stated r: the points the game draws from its seed have r ≈ 0.98–1.00 whatever is stated (AL10 states 0.35, weak, not significant, and draws a near-perfect line); CM9 and AL14 draw a different line from the one stated; AL14 clips 7 of 15 points to the axis. (3) Pre-answer leak on all 14 Level 4 scenarios: the regression line and its equation are drawn before "Calculate b and a" is asked. What checks out: all six critical values (n = 10, 12, 15, 18, 20, 25), every other prediction, every sq4Type. Fixing it is new data (and a scatter generator whose r is the stated r), which is Jon's content call. Re-checked 2026-11-08 on main f8a287b4: PART — FIXED: normal-navigator, core-maths-paper2a and maths-court, held by `scripts/verify-normal-navigator.py`, `verify-core-maths-paper2a.py` and `verify-maths-court.py` (in the public repository since ab701b4c), green in main run 42512282061. STILL LIVE: regression-rumble; `scripts/verify-regression-rumble.py` run today ends `FAILED: 62 FAIL(s) across 37 of 40 scenarios`, unchanged, and is still not in CI. The game is withdrawn (holding page; `.claude/rules/game-roster.md:180`), so no student meets its keys. | **Jon** — rule on regression-rumble's data; then **CC** fixes it and wires its verifier into CI |
| 1.34 | **Nine non-game pages scroll sideways on a 320px phone, from their own content.** Found 2 Oct 2026 while measuring the footer (document width at 320×568, identical on `main` and the footer branch, so not the footer): `/spec-map/` 540px, and eight parent guides, `probability-trees` 397, `indices-surds` 364, `fractions` 347 (its `.equiv-table`), `graphs-transformations` 339, `standard-form` 338, `pythagoras` 325, `statistics-data` 325, `coordinates` 324. Six games did the same (~~`estimation-golf` 797~~ fixed PR #47, 4 Oct 2026, `trig-wars` 711, `estimation-engine` 378, `equatle` 348, `better-value` 339, `differentiation-duel` 321); those are §3.9's phone-fit batches. Not traced element by element beyond `fractions`. **2 Oct 2026 (PR 62): recorded, not fixed.** Tier 1 now measures every page at 320×568 and fails on a new overflow; all of these are listed in `tier1_phone_overflow` (`scripts/checker-allowlist.json`) with their widths in the fallback font (e.g. `fractions` 347, `spec-map` 540) and the gate found more: 8 teacher pages (§1.37), 16 more games, and display maths in four of the guides (§1.38, not tables). Each fixing PR removes its entry. **Not in that list (3 Oct 2026): `moments-master` overflows at 320 on two questions only (`alevel[19]`, `alevel[40]`), which the seeded gate does not draw; recorded in §1.40.** Re-checked 2026-11-08 on main f8a287b4: PART — main run 42512282061's Tier 1 measures every page at 320×568 in the real fonts and fails a stale entry, so `tier1_phone_overflow` (`scripts/checker-allowlist.json`) is the evidence. FIXED (no entry): guides `graphs-transformations` and `coordinates`, and `differentiation-duel` (#256, FONT-FIT: they fit in the real fonts); `estimation-golf` (#47); `estimation-engine` (#74); `equatle` (#669). STILL LIVE (entry): `spec-map` 540, `fractions` 321, `standard-form` 338, `trig-wars` 711, `better-value` 339; the four display-maths guides are §1.38. **10 Nov 2026 (PHONE-SCROLL):** PART — `parents/guide.js` wraps every guide table in `div.table-scroll` (`overflow-x:auto`, `parents/guide.css`; the table's margin moved to the box, so the guides look the same at desktop width, pixel-identical at 1366×768). FIXED: `fractions` and `standard-form` (entries removed). standard-form's table fits (314px); its last overflow was prose, the Conversation starter's "5,970,000,000,000,000,000,000,000 kg", which cannot break between digits: Amendment 1 puts `<wbr>` after each comma on that line only (`parents/standard-form/index.html:120`), and "weighs" became "has a mass of" (Jon, 10 Nov). STILL LIVE (entry): `spec-map` 540, `trig-wars` 711, `better-value` 339. | phone-fit batch, or its own |
| 1.35 | **Live bug class (tier 1/3): three games' KS3/GCSE scores never show on the leaderboard hub.** fraction-equivalence:208, percentage-flip:216 and prime-factorisation:212 submit non-year6 scores under level 'all', while leaderboards/index.html lists them with year6/ks3/gcse, so their KS3/GCSE scores never show on the hub. check-leaderboard-coverage.js misses it: with a variable level it assumes the roster's tiers rather than reading the variable's values. Also: extract-banks reports percentage-flip as 32 questions at every level (true: 12/12/20); check whether fraction-equivalence's 20 is misattributed the same way. Confirm the 'all' boards exist in the Firebase console before contracting. (Jon, 2 Oct 2026.) Re-checked 2026-11-08 on main f8a287b4: STILL LIVE — `games/fraction-equivalence/index.html:239`, `percentage-flip:257` and `prime-factorisation:248` submit non-year6 scores as 'all', while `leaderboards/index.html:184-187` lists year6, ks3 and gcse, and a card loads only the levels it lists (`:406`). CAN'T TELL from the repository whether the 'all' boards exist (Jon's Firebase console). **Hub part FIXED 10 Nov 2026 (contract HUB-ALL-BOARDS, PR #727):** the 'all' boards exist (Jon's Firebase export of 10 Nov: fraction_equivalence_all 28 scores, percentage_flip_all 50, prime_factorisation_all 14); the hub lists year6 and all for the three games, and its cards read all 92 (screenshots in the PR); check-leaderboard-coverage.js now reads a level variable's assigned values, with a selftest whose planted hub (the roster's tiers) fails. **Still open: the extract-banks part only.** extract-banks still reports percentage-flip as 32 at year6, ks3 and gcse (row LEDGER-B4-PERCENTAGE-FLIP), and fraction-equivalence's 20 at every level is unchecked. | **home lane** — the extract-banks part only |
| 1.36 | **Live bug class (canon §0.2, tier 1): answer tolerance not tied to the precision the question asks.** Every typed answer is `parseFloat` against a fixed or percentage band; there is no shared answer-marking helper in `schools/assets/`, every game rolls its own, and every money input is `type="number"` (a leading £ empties it). **Case 1, 2 d.p. money (Jon's rule, 2 Oct 2026):** if the correct answer is whole pounds, an integer is accepted (1250 or 1250.00); once pence are part of the answer it MUST be exactly 2 d.p. (1250.70 right; 1250.7 is the right amount in the wrong form). **Corrected 3 Oct 2026 to Jon's actual rule (canon §7.1.3):** the typed amount is compared numerically first; a right amount wrongly written (1250.7, 3050.0, 1250.700) is marked neither right nor wrong: the format message names the student's figure and they resubmit, with no penalty recorded. 1 d.p. is never accepted. Still assumed, not ruled: a leading £ is optional. **Live instance, checked 2 Oct 2026 on `4a04d7e`: `split-it`.** Single answers are marked to ±0.05 (`:543`), so on a pence answer it accepts the wrong value as well as the wrong form: £12.30 and £12.38 both pass for £12.34. That covers the £ unit-cost questions (`:380`) and the € currency questions (`:387`, keyed `toFixed(2)`). Its recipe-scaling answers, keyed to 1 d.p. (`:362`), are marked to ±0.15 (`:536`, `:538`), so 2.4 or 2.6 passes for 2.5. **Not live, checked:** `percentage-flip` (`:259`, `:282`) has no money answers (all 32 keys are whole numbers, no £); the rule applies to its rebuild (§3.11). `tax-theft` (`:1029`) keys whole pounds (`Math.round(expected)`, `:1040`); `growth-and-decay` (`:751`, `:790`) keys money to 3 s.f. Neither has a d.p. form problem; both have a tolerance question (below). **Proposed fix (shared layer):** `schools/assets/answer.js`, `MaffsAnswer.money(raw, correct)`, reading the raw typed string, never a parsed number, with three outcomes: correct / wrong / right value wrong form. Right value wrong form is NOT marked (corrected 3 Oct 2026; this line used to say "marked WRONG"): it gets the format message and a resubmission (canon §7.1.3; `moneyResult()` in tax-theft is the reference). Money inputs become `type="text" inputmode="decimal"`. `percentage-flip` adopts it as part of its rebuild; `split-it` follows as a separate pass, not a sweep, and its ±0.05 and ±0.15 bands go with it (the helper behind a band that admits wrong pence fixes nothing). Needs a checker rule too: any money answer in a bank stored or displayed at 1 d.p. **`tax-theft` and `growth-and-decay` tolerances (found 2 Oct 2026):** `tax-theft` accepted ±£1 (personal allowance, taxable) and ±£2 (tax, NI, deductions, net) of the whole-pound key (`:859`–`:961`), so a pence answer such as 1250.7 passed for £1251; its tax and NI are computed unrounded (only the allowance taper uses `Math.floor`) while the payslip shows rounded figures. `growth-and-decay` accepts 2% of the key + 0.01 on sub-question 1 (`:754`; sub-question 3 gets 0.5%, min 0.05), about ±£163 on CM4's £8,140, and ±0.15 on sub-question 4 (`:793`). **Suspected content bug, verified not fixed: `growth-and-decay` keys disagree with the precision their stems ask.** CM3 `:229` asks for 2 s.f. and keys 1808 (e^7.5 = 1808.04, so 1800); a scan of all 46 keys that carry an `sf` field found two more, AL5 `:380` (3 s.f., keyed 15530, should be 15500; money) and AL8 `:404` (3 s.f., keyed 2172, should be 2170). The `sf` field is never read. The 2% band hides it (1800, 15500 and 2170 are all accepted), but on a right answer the feedback shows the unrounded key. **RULED 2 Oct 2026 (Jon); both are requirements of the shared precision marker, not separate patches.** **`tax-theft`:** every step is keyed from the figures the student can see on screen, never from unrounded internals ("we can't mark a student against numbers they cannot see"), and marked to the penny. (This line used to say "marked as exact whole pounds": a misreading. Jon's 'whole pounds' meant whole-pound amounts need no .00, never round answers to pounds. Corrected 3 Oct 2026.) The ±£1 and ±£2 bands go. **Tax-theft DONE 3 Oct 2026 (START item 4).** **`growth-and-decay`:** correct the three keys (`:229` → 1800, `:380` → 15500, `:404` → 2170) and mark to the precision the question states, using the `sf` field the game already carries. (Jon, 2 Oct 2026.) **The three growth-and-decay keys are corrected in PR #3 (wrong-keys batch 1); marking by `sf` is still open.** **split-it DONE 3 Oct 2026 (PR #12):** every typed answer marked by the shared `MaffsAnswer` (`schools/assets/answer.js`): money (£ unit cost, € currency, £ shares) to the penny with an optional £/€, in `type="text" inputmode="decimal"` inputs; GCSE recipes and the speed questions now say "Give your answer(s) to 1 decimal place." and are marked to it (Jon's rulings; speed keys now exact, half up); everything else exact. The ±0.05 and ±0.15 bands are gone. Best Value's two unit prices now always differ by at least 1p (Jon). `verify-split-it.py` (CI) failed on the old file and passes. The shared helper is the proposed fix above, built; the other money games are START item 5. Re-checked 2026-11-08 on main f8a287b4: PART — FIXED: split-it (#12, `scripts/verify-split-it.py`); tax-theft keyed from the figures on screen and marked to the penny (`scripts/verify-tax-theft.py`, from PR 4); growth-and-decay's three keys (`:265` 1800, `:416` 15500, `:440` 2170) and its marking at the stated precision (#352, `sqMark` `:795`, `scripts/verify-growth-and-decay.py`); all green in main run 42512282061. Remains: money inputs still `type="number"` (`tax-theft:690`, `growth-and-decay:753`), so a leading £ empties the field; no money-at-1-d.p. rule in `scripts/check-banks.py`; Jon's ruling on the assumed point (a leading £ optional). **MONEY-INPUT, 9 Nov 2026 (this row's PR):** Jon ruled the box (9 Nov): a fixed currency sign shown in it, and a typed £ accepted (canon §7.1.3), which settles the assumed point. `MaffsAnswer.moneyInput()` (`schools/assets/answer.js`) makes a game's own input a money box: `type="text" inputmode="decimal"`, the £ or € inside its left edge. Every game that marks with `MaffsAnswer.money()` calls it: `estimation-engine`, `its-on-sale`, `split-it`, `squared-squirrel`, `tax-theft` (no longer `type="number"`; a typed £ now reaches the marker instead of "Please enter a number.") and `the-6-ps`; the £ each showed beside its box went. `scripts/check-banks.py` fails a page that calls `MaffsAnswer.money(` without `MaffsAnswer.moneyInput(` (every .html page; its plant runs in `--ci`); `scripts/test-answer-js.py` covers the helper. `growth-and-decay` is not one of them: it marks every typed sub-question to the significant figures its prompt states (`MaffsAnswer.decimal`, `sqMark`), never by `money()`, so its `type="number"` inputs stay as they are; moving them to `money()` would change its marking. **Still open on this row:** a check-banks rule for money keys stored or displayed at 1 d.p. 9 Nov: the shared helper exists (answer.js MaffsAnswer.money, moneyInput #719); the 'no shared helper' wording above is historical. Remaining: a check for money keys stored or shown at 1 d.p. **MONEY-ANSWERS, 11 Nov 2026 (CLOUD-QUEUE-1111 PR 2):** settles 'money inputs still `type="number"`' for every typed answer in pounds. Money boxes and a leading £ now cover the answers marked by `decimal()`/`exact()` with `opts.currency` (`growth-and-decay`, closing GD-MONEY-INPUT; `stat-attack`; `graph-sketcher`; `squared-squirrel`'s stages 2-3; The 6 P's £ compound measures), and those read by `MaffsAnswer.parse()` (`chart-interrogator`, `graph-sketcher`'s reads); `fermi-lab`'s and `as-you-can-see`'s readers were boxed too. `check-banks.py` now sees money answers by all three routes. `tax-theft:690` is a money box since #720. Not settled here: the money-at-1-d.p. check, and `graph-sketcher` CM11's table keys stored at 1 d.p. (608.3 for £608.30, marked to 1 d.p.: unchanged by contract). Answers in £k, £100s or pence, and the escape rooms, are MONEY-THOUSANDS (§3). | **Code Claude** (shared precision marker; tax-theft and growth-and-decay ruled); **Jon** to rule the two assumed points |
| 1.48 | **FIXED 11 Oct 2026 (SPLIT-IT-KATEX): split-it speed working and unit label.** Fractions in working text now render through KaTeX (`F()`/`X()`); speed shows a whole number or a stacked fraction; the unit label is drawn once. Scale-factor working fixed too. Scans: `docs/audits/split-it-fraction-scan-2026-10-11.md`; open there: `fraction-equivalence` builds its fractions with CSS. Re-checked 2026-11-08 on main f8a287b4: PART — split-it FIXED by #281 (5d9d961f), held by `scripts/verify-split-it.py`, green in main run 42512282061. STILL LIVE: `games/fraction-equivalence/index.html:39-40` and `:168-176` still build the two fractions in CSS (`.frac-num`, `.frac-line`, `.frac-den`). | Code Claude |
| 1.51 | **Resit audit (PR #35): what is left in the five games PR #36 fixed**, by the audit's fix batches. **Batch 2 (wrong keys at the card's level):** ~~`probability-pioneer` Stage 3 Q7 "If two outcomes are equally likely, each has probability 0.5" keyed True (audit F2; Jon ruled 4 Oct (decision 4): rekey False, with the explanation)~~ **DONE PR #45, with F3-F6 and F8 below; probability-pioneer now has its full verifier (`scripts/verify-probability-pioneer.py`, CI); only F7 (judgement call) remains.** **Batch 4 (MEDIUM):** ~~`probability-pioneer` F3 (lottery feedback says Impossible), F4 (rain in Britain keyed Certain only)~~ (done, PR #45); `estimation-engine` F2 (the meter's centre label is the key rounded to a whole number, outside the band on six items) and F3 (A-Level items served to everyone; rides with its SR-12 rebuild); `decimal-detective` ~~F4 (the 2 d.p. readout lets a student drag to the target without reading the scale; judgement call)~~ (done, PR #65, with F2 and F3). **Batch 5 (LOW):** `shape-shifter` F5 (15 items per mode; no 180° question is ever built, because its wrong-direction distractor equals the answer, so it is filtered out; every rotation is about (0,0)); `probability-pioneer` ~~F5/F6 (two value-equal distractor pairs, 2/3 and 4/6, 1/2 and 2/4)~~, F7, ~~F8~~ (F5, F6, F8 done, PR #45; F7 a judgement call, left); `estimation-engine` F5 (float edge on the band), F6 (an empty entry stops the timer silently), F7 (2 s auto-advance, not `MaffsNext`); `decimal-detective` ~~F6 (Round Up 9.5/9.50), F7 (= §1.49)~~ (done, PR #50, with F1), F5 (7.895: 7.90 vs 7.9, stands: the ask names the form), Line-Up's Check enabled on load; `negative-number-line` (Calculate distractors off the drawn line; wrong-answer Next not `MaffsNext`; its full verifier is in CI since PR #54). **Fixed in PR #36 beyond the contract's list:** shape-shifter F3 (duplicate options) and F4 (a distractor equal to the object), decimal-detective F3 (0.25's neighbouring tenths), negative-number-line F2 (half-way points). Each game still needs its full verifier (audit class 1); `check-resit-fixes.py` covers only the fixed faults. Re-checked 2026-11-08 on main f8a287b4: PART — FIXED: probability-pioneer in full (F2–F6 and F8 by #45; F7's item removed by #576; `scripts/verify-probability-pioneer.py`); estimation-engine F2, F3, F5, F6 and F7 by its rebuild, #74 (old pool, meter and timer gone; MaffsNext; `scripts/verify-estimation-engine.py`); decimal-detective F4 (#65), F6 and F7 (#50); each of the four games has its full verifier in CI (`verify-shape-shifter.py`, `verify-decimal-detective.py`, `verify-negative-number-line.py`, `verify-estimation-engine.py`), all green in main run 42512282061. STILL LIVE: shape-shifter F5 (`docs/audits/findings/shape-shifter.yml` t3-002 and t3-004 open: no 180° rotation, 15 items a mode, every rotation about (0,0)); decimal-detective's Check enabled on load for Line-Up (`games/decimal-detective/index.html:457`); negative-number-line's Calculate distractors can fall off the −10..10 line (`:898` keeps −12..12), and its Next is its own button, not MaffsNext (`:290`). decimal-detective F5 stands (ruled). | Code Claude, batch by batch (F2 of probability-pioneer ruled by Jon, 4 Oct) |
| 1.52 | **Angle Ace: GCSE has 35 questions, and the roster lists a KS3 level with no bank** (resit audit F14). 35 is below the 40-50 minimum (`check-banks.py` B4 carries it in the ledger). `?level=ks3` falls back to GCSE (audit class 8, batch 5). Adding questions is content (Jon's call); every new item needs only a `fig` and passes `scripts/verify-angle-ace.py` or fails it. Found 4 Oct 2026, logged 6 Oct 2026 (Angle Ace contract, SR-9). Re-checked 2026-11-08 on main f8a287b4: PART — FIXED: KS3 is off the roster (#333; `.claude/rules/game-roster.md:72` reads "Year 6, GCSE"), and the game resolves year6 and gcse only (`games/angle-ace/index.html:662`). STILL LIVE: GCSE has 35 questions (B4 entry `angle-ace::gcse` in `data/check-ledger.json`). | Jon (content) |
| 1.71 | **RELIST checklist: Glorious Gantt Game (`glorious-gantt`), unlisted 6 Oct 2026** for the tranche 4 audit's faults (Jon's rulings of 20:30, canon SR-20). Relist when this game's verifier merges and its register entries are fixed, in that PR, every item: [ ] roster row back to the Core Maths section (was #72); [ ] portal card in `index.html` (`games/glorious-gantt/?mode=a&level=core`); [ ] `sitemap.xml`; [ ] spec-map rows LO2, §3.8: "(being fixed)" text back to links, removed links restored; [ ] leaderboard hub row `['glorious-gantt','Glorious Gantt',['core','level4']]` in `leaderboards/index.html`, and its entry removed from `NOT_ON_HUB`; [ ] canon §6.1's §3.8 row and note back to Covered; [ ] every entry in `docs/audits/findings/glorious-gantt.yml` fixed, with its PR. Jon, 6 Oct 2026 20:30. Re-checked 2026-11-08 on main f8a287b4: STILL LIVE — still unlisted: no card in `index.html`, no `sitemap.xml` entry, still on `NOT_ON_HUB` (`scripts/check-leaderboard-coverage.js:163`); no `scripts/verify-glorious-gantt.py`; all 13 findings in `docs/audits/findings/glorious-gantt.yml` open. No checklist item is done. | open |

**Done this session (26 Sep):**
- [x] **1.1 Expectation Station cannot be completed — since it shipped (`812cd6a`, 22 Mar).**
  `checkStage1()` hid its own Check Table button (`:707`, `:725`) and `renderStage1()` never
  re-showed it, unlike stages 2 and 3 (`:822`, `:953`). From question 2 onward a student filled
  the table and had no way to submit — no run had reached `game_completed` since it shipped. **Fixed**: `renderStage1()`
  now sets `checkStage1`'s `display` back to `''` alongside its existing `disabled` line, one
  line, matching the pattern stages 2 and 3 already used. Confirmed no second blocker — the
  function rebuilds the table cells and tile listeners from scratch on every call, so `display`
  was the only state it failed to restore. **Verified completing at 8, 16 and 24 questions**
  under the stub server, driving real clicks through a headless browser and asserting
  `game_completed` fires: 8 → score 10, `questions_correct` 3; 16 → score 24, `questions_correct`
  8; 24 → score 31, `questions_correct` 10 (see the next bullet for why 24 answers 20).
  - **A "24 questions" core session only ever serves 20 — found while verifying, reported, not
    fixed.** `newQuestion()`'s `questionQueue = shuffle([...bank]).slice(0,
    Math.min(sessionLength, bank.length))` caps the queue at the level's bank size. Core has 20
    questions, GCSE 15, A-level 10 — **none of the three levels has 24**, so the "24" button
    always under-delivers, silently, and correctly ends the session early with `game_completed`
    reporting the true count (`questions_answered: questionQueue.length`). Nothing is broken —
    the game behaves consistently — but the UI promises a number the content can't back on any
    level. Not this contract's fix (bank/scoring were DO NOT TOUCH); flagging for a content or UI
    decision (more questions authored, or the "24" option removed/relabelled per level).
  - **The verification itself took three false leads worth recording**, since each nearly got
    misread as a game defect: (1) the first driver script filled Stage-1 cells by watching for
    the `missing` CSS class to clear, but the game correctly keeps that class after a wrong
    attempt (only adds `incorrect-cell` alongside it) — an infinite loop in the *test*, not the
    game. (2) A "Page crashed" on the 24-question run reproduced twice with a fresh browser each
    time, independent of GPU flags, with a flat JS heap throughout (5–7MB, no leak) — looked like
    a real bug, but per-question timing logs showed the crash always landed at roughly the same
    *elapsed time* rather than the same *question count*, which pointed at something external to
    the page. (3) With full instrumentation it turned out to be the bank-size cap above: the
    driver kept "playing" past the natural end of the queue once the game had already switched to
    the results screen, hammering controls that no longer existed. Fixed by checking for the
    results screen at the top of every loop iteration, not just after finishing a question.
  - **Class check on this shape, requested and run:** a static scan for "an element's
    `style.display` set to `'none'` inside an answer/check handler and never restored anywhere in
    the file" across all 95 games. One category-A hit outside Expectation Station
    (`shape-shifter:843`, `undoBtn`), which is a false positive — `shape-shifter:509` restores it
    via a ternary (`(mode === 'rotation') ? 'none' : 'inline-block'`) that a literal-value scan
    can't read; checked by hand and it restores correctly. **No other game in the roster looks
    uncompletable by this defect shape.**
- [x] **1.2 Worked solutions showed the author's self-correction.** The original diagnosis (dead
  duplicate `c:`/`d:` keys, canon §8.2c Shape 2) was wrong about *where* the leak lived —
  `showExplain` renders only `q.s`, and the prose was in the `s:` array, never duplicated.
  Deleting the dead `c:`/`d:` pairs (also done) removed real dead code but would have left the
  leak untouched. **Fixed** by rewriting both `s:` arrays: `unit-converter:163` drops the "…wait,
  1.5 × 0.6 = 0.9…" line entirely; `scale-factor-scaling:162` also had a **wrong intermediate
  step** in the dead draft (`4 × 2.5×10⁹ cm² = 10⁹ cm²` — the correct product is `1×10¹⁰`, not
  `10⁹`) and now shows the cm²→m² conversion as its own explicit step. **Canon §8.2c's correction
  is drafted but held out of this commit** — the contract that fixed this named Canon under DO
  NOT TOUCH, so the canon.md diff sits unstaged for Jon's separate ruling rather than landing
  with the code fix. See "Held back" below.
- [x] **A draft-prose scan of every question bank**, report-only, requested alongside 1.2 because
  three games shipping this now makes it a class (proof-builder, scale-factor-scaling,
  unit-converter). First pass on a bare "actually" returned 126 hits, nearly all ordinary content
  prose ("things you actually use"); tightened to high-signal shapes (ellipsis + retraction,
  "wait,", "let me recalculate", explicit retractions, first-person authoring voice, placeholder
  markers) and found **17 candidates**: `angle-ace`, `coordinate-geometry-dash`,
  `factor-theorem` (×3), `formula-unlocked`, `probability-paradox`, `spot-the-muppet`,
  `terrible-advice` (×4) and `wrong-on-the-internet` (×3). **Not triaged as defects** —
  `terrible-advice` and `wrong-on-the-internet` are "spot the deliberate error" games where a
  character's wrong reasoning *is* the content, so most of their hits need reading in context,
  not fixing. Full list drafted for canon §8.2c, held with the item above.
- [x] **Expectation Station snag not reproducing.** Moved from a numbered finding to
  `docs/jon-playtest-2026-08.md`'s new Snagging section — the reported "can be simplified" wording
  against `A · B` doesn't match any question in the current bank (all `A · B`-shaped questions
  have `bbLink: null`, which renders the neutral "try Boolean Blitz" line, never a simplification
  claim). Jon to replay once and either close it or give the exact wording seen.
- [x] **1.13 — `MaffsSession` built and adopted in 5 games**, migrating Expectation Station off
  its 1.11 hand fix. Each game verified by a scripted play-through (stub server) driving every
  offered button, at every level, to completion, asserting `questions_answered` matches the
  label and `game_completed` fires; no game's PB key depends on session length, so nothing is
  orphaned. Tiers 1+2 green; tier 3 clean per game (details in the `e8f8a69` commit message).
  Canon §7.1 now says "Session-length controls use `MaffsSession`... the same pattern as
  `MaffsOptions`."
  - **Reported, not touched, per contract (`terrible-advice`, `fermi-lab`, `word-problem-decoder`):**
    - `terrible-advice` already hand-rolls the identical fix (`updateSessionButtons()`, bank-aware
      + an explicit "All N"), built before this session knew the shape was a class. One inherited
      quirk found while reading it: its filter is `[10,20,30].filter(n => n < available)` — strict
      less-than, not `MaffsSession`'s `>=` — so a bank that lands exactly on a preferred length
      (GCSE = 20) shows "All 20" instead of a plain "20". Cosmetic, not an over-promise; not fixed,
      per DO NOT TOUCH.
    - `fermi-lab` never over-promises: its Quick/Standard/Marathon buttons are 5/10/"all in tier",
      and every tier's bank (ks3 13, gcse 15, alevel 13, level4 10, core 15) is ≥ 10, so `Math.min`
      never has anything to truncate. PB key (`fermi_scores_` + tier) is level-only. Would adopt
      `MaffsSession` with `preferred:[5,10]` cleanly if the roster is ever standardised.
    - `word-problem-decoder` is a genuinely different shape, not just report-only caution: its
      "pool" isn't `bank.length` — a `multi` question contributes one phrase per highlighted topic
      the student has active, so the true servable count is a sum over filtered questions, not a
      length. That sum is still computable before Start (`currentLevel` + `activeTopics`, both set
      on the settings screen), so adoption isn't blocked — it would need its own poolSize helper
      (not a bare bank count) and a re-render on every topic-chip toggle, not just on level change.
      PB key (`wpd_pb_` + level) is level-only, so no orphan risk. Not attempted this session.

**Checker tier 4, layer A — built later the same day (26 Sep), separate contract.** New files:
`scripts/bank_common.py`, `scripts/extract-banks.py`, `scripts/check-banks.py`,
`data/check-ledger.json`, `docs/checker-tier4-design.md`; changed: `.github/workflows/check-site.yml`
(new CI step), `.gitignore` (`data/banks/` — regenerated, ~8MB, not committed), `CLAUDE.md`.
**Not yet committed.**

- Extraction reads every game's bank back from the live page under Playwright (post any runtime
  patch), not from the static source — this is what makes it see the *served* state, the same
  reason normal-navigator's now-fixed index patches were dangerous. Bank variable candidates are
  restricted to SCREAMING_SNAKE_CASE names, checked directly: every real bank across all 94 games
  is named that way; runtime session state (`pool`, `currentQ`, `roundQuestions`) never is. Without
  that filter, estimation-golf's `roundQuestions` (a live copy of its own bank, populated by page
  load) registered as a second bank and flagged every one of its own questions as a B3 duplicate
  of itself.
- Ten lint rules, B1–B10 (missing/duplicate answers, duplicate questions, bank size,
  session-length overpromise, draft prose, a KaTeX rendering hazard, duplicate object keys, index
  patches, `correct_override`). Full rule list and current counts: `docs/checker-tier4-design.md`
  and the "Report" in this session's transcript.
- **STOP IF triggered and resolved, not bypassed:** more than 10 games came back with no
  gradeable static bank on the first honest pass. Investigated each rather than loosening the
  threshold — resolved into 10 confirmed true generators (no static array anywhere; several
  explicitly say "Procedural generation" in the roster) and 16 real banks whose correctness is
  *computed* rather than stored (regression-rumble, chart-interrogator, word-problem-decoder,
  fermi-lab, ...) — exactly what a future layer C would check, not a gap in layer A. All 94 still
  land in the ledger, per the success condition.
- **B7's KaTeX half went through two rejected designs before the one that shipped**, both
  instructive: rendering every bank string through KaTeX regardless of whether the game ever sends
  it there flagged 3772 false hits (most banks carry hint/explanation text that's never rendered
  that way); sampling a handful of live clicks through the game was flaky (0–3 hits across
  identical runs on the same, unfixed game). Shipped version statically finds which object field
  each game's OWN source passes to `K()`/`renderToString` (`component-crusher` → `prompt`) and
  renders every value of just that field, once, deterministically — precise and reproducible,
  and it is what surfaced `factor-theorem` and `test-the-claim` as two more games with the same
  class as §1.10, previously unknown.
- **Regression-proven the same way tiers 1–3 were**, three reverts plus a fourth check with no
  revert (component-crusher's hits are un-fixed today, so proving they're already in the ledger is
  the test, not a revert): restoring scale-factor-scaling's "let me recalculate" line and
  normal-navigator's three `QUESTIONS[n]=` patches each failed `check-banks.py --ci` with the right
  rule (B6, B9), each reverted after (`git status` clean on `games/` throughout, checked). The
  scale-factor-scaling revert also incidentally re-triggered B8 on the same dead `c:`/`d:` keys
  that commit had cleaned up — an unplanned but correct confirmation.
- **One real bug in the checker itself, found by the regression pass, fixed before this was
  trusted:** `correct` and `correct_override` resolve in DECLARATION order by default; several
  games' own runtime reads `correct_override || correct`, override winning when both are present.
  The first version of B1/B2 read `correct` first and so entirely missed formula-unlocked:296's
  known duplicate (the override, not `correct`, collides with a distractor) until this was
  caught and fixed (`bank_common.resolve_correct`, precedence-ordered, not the same list as
  "does this carry an answer key at all").
- **New-game gate proposed, not decided:** block a new game's merge on layer A passing (a static
  bank found, or declared a generator, and zero unrecorded violations). Layers B–E stay advisory
  until built. `docs/checker-tier4-design.md`'s final section; **Jon's ruling**, §6.

**Not yet reproduced or resolved:**
- **regression-rumble never reports a wrong answer.** `_rrQAnswered`/`_rrCorrectCount` rise
  together and only on a correct answer (it will not advance otherwise), so `accuracy` is always
  100% and GA4/Sheets never see a wrong attempt. No leaderboard effect. Not part of this session's
  fix list; carried forward here because it has nowhere else to live.

## 2. Leaderboard integrity — one widened contract, not five patches

The held contract `docs/next-contract-leaderboard-modes.md` is the architectural fix. **Not
started.** Widen it before it runs so it covers the whole class:

- **Sort direction per game/mode:** `higher-power` Pairs, `estimation-golf` (strokes — the hub
  already sorts ascending via `LOWER_IS_BETTER`, but `firebase-leaderboard.js`'s 🏆 HIGH SCORE and
  "best:" use `score >= maxScore`, so the worst round gets the trophy), `equatle` (guess count — a
  6-guess win would outrank a 1-guess win on both the hub and the ticker). Both games are
  currently gated off at the call site behind `LEADERBOARD_MODE_READY` — the `submitScore()` call
  itself is still present and visible in both, not deleted or commented out, so
  `scripts/check-leaderboard-coverage.js` still sees it and distinguishes **held** (gated) from
  **excluded** (no score to submit), failing if a held game loses its gate or an undeclared gate
  appears. Lifting both holds is this contract's job.
- **Scores that aren't scores:**
  - `trig-wars` counts the opponent's hits, so a 0–3 loss submits 3.
  - `chart-interrogator` submits a constant 100 for every completed scenario (the time
    multiplier was removed), so its board can only ever be a tie. Its Level 4 key is `l4`, not
    `level4`.
- **Local "leaderboard" wording not backed by the shared system** (found 26 Sep, already written
  up in `docs/next-contract-leaderboard-modes.md`'s "Added scope" section):
  - `equatle:256`–`:873` has an entirely device-local second "leaderboard" — name prompt, "Submit
    Score to Leaderboard" button, "Score submitted!" toast — that never touches `MaffsLeaderboard`
    or Firebase, while the real board is held. Nothing about its own sort is broken.
  - `estimation-golf:589` shows a "🏆 Global leaderboard" link inside its end-of-round summary at
    the exact moment a round has not reached the global board.
  - **Scan all 94 roster games** for hand-rolled local leaderboards, name/initials prompts, or any
    "submitted"/"leaderboard" wording not backed by `MaffsLeaderboard`/`MaffsScoreHistory`, and
    list what's found — two turned up just from looking at two games.
- **`like-terms-collector`'s banked runs** (Stage 3 "Finish here", 25 or 35 answered) share a
  board with full 45-question runs, scored as raw correct count. Pre-existing; keep, or separate? **RULED 29 Sep 2026 (Jon): separate.** Give Stage 3's banked finishes ("Finish here" at 25/35) their own leaderboard entry/tag so they stop competing directly with full 45-question runs. Not yet built: every run submits to one board, `'year6'` (`games/like-terms-collector/index.html:608`), on 11 Nov 2026. Moved from §6 (TODO-TIDY).
- **Housekeeping in the contract itself:** remove `MIN_QUESTIONS_FOR_LEADERBOARD` from its DO NOT
  TOUCH — confirmed gone from the codebase (`grep` clean, 26 Sep).
- **Still unverified:** `node` is not installed on the Windows machine (checked again 26 Sep,
  still absent), so the updated `check-leaderboard-coverage.js` has **not been executed** — its
  logic was mirrored in Python against the real files and reports what it should (93 games with
  the call, 0 missing, both held games gated, no undeclared gates), but the JavaScript itself is
  unrun. Run it on the Linux machine before trusting it.
- **Leave out:** the roster-vs-code level mismatch (canon §8.2b, 22 games). Separate decision
  (real per-tier level, or a roster correction) that would double this contract's size.

**Do not start without Jon's say-so** — his stated order was this fix list, then checker tiers
3–4, then this.

## 3. Mission work — resit / Core / OCR

| # | Item | Blocked on |
|---|---|---|
| 3.1 | **Spec mapping contract 1** — boards, crosswalks, the 94-game mapping, checker, review doc with the two resit gap lists. Part-built: `docs/sources/dfe-gcse-maths-subject-content.pdf` vendored under OGL (logo must never appear on the site — this repo is public); `scripts/extract-dfe-tier.py` derives 97 DfE statements as 174 typed parts into `data/dfe-gcse-parts.json`, asserting the source SHA256, the published reference ranges (N16 A25 R16 G25 P9 S6) and the 24 Sep review checkpoint as regressions. Data model: `tier` stores the DfE *printed type* (`standard`/`underlined`/`bold`, never F/H); `depth` (F/H/F+H) required only on standard/underlined, each with an evidence note and `reviewed: false` — no Foundation-only content exists, so a bare F is an editorial judgement, kept separate. Still owed: A-level content the same way; the board crosswalks; the 94-game mapping; `data/spec-mapping.json`; `scripts/check-spec-mapping.py`; `docs/spec-mapping-review-2026-09.md` with its two gap lists. `spec-map/index.html` covers **69** of 94 roster games, not the ~80 assumed, 25 absent, 0 orphan slugs. | **Jon: spot-check 10 of the 34 mixed statements** in `data/dfe-gcse-parts.json` against the PDF |
| 3.2 | Spec mapping contract 2 — render `spec-map/` from the data, board selector, Foundation filter, checker in CI. This is the real fix for §1.5. | 3.1 review |
| 3.3 | Exam-topic tool, OCR first — needs the OCR crosswalk and gap list from 3.1; building it first would repeat the work. | 3.1 |
| 3.4 | **Times-tables recall game (new build) — for resitters and Jon's Level 3 maths-module student. Requested 30 Sep 2026. DONE 30 Sep 2026 as `six-sevens-bruv` (START block); design points 1-4 settled by its contract: reverse questions as missing-factor forms, never "c = ? × ?"; the grid is a mastery map that never shows an unearned product; visible count-up, no countdown; adult register. The second game below, "Don't Count the Zeroes", is still to build and should reuse `schools/assets/progress.js`.** Design points to settle before a build contract: (1) the 12×12 grid must not turn recall into lookup — preferred: reverse questions ("56 = ? × ?", click the cell) and/or the grid as a mastery map with keypad answers; (2) speed via count-up scoring, per canon §5 (no countdown under 30 s); (3) adult register for 16+ users — choose tiers with §7.5.1 in mind; (4) adaptive: weak facts served more often, device-local mastery (localStorage). **Roster check done 30 Sep: no existing times-tables or multiplication game** (roster, `games/`, todo, canon and the idea backlog searched; `factor-race` and `prime-factorisation` practise factors, not recall of products). **Same entry, second game: "Don't Count the Zeroes" — standard form (name ruled by Jon, 30 Sep).** Progression: ×/÷ by powers of 10 on a fixed place-value chart (digits slide, placeholder zeros fill, count the jumps) → large numbers to standard form → small numbers (negative powers) → converting back and ordering → calculating (top tier only). Distractors are named misconceptions: counting zeros (0.00045 → 4.5×10⁻³), A outside 1 ≤ A < 10 (45×10⁻⁵), wrong sign of the power. The counting-zeros feedback line is "Don't count the zeroes — count the jumps." **Existing coverage checked 30 Sep:** `standard-form-blitz` (roster #44, GCSE/A-Level, 50+50, convert/multiply/divide) exists. `docs/resit-coverage-audit.md` finds N9.1 COVERED by it (30 of its 50 GCSE items are Foundation-pitched conversions and comparisons; the 20 multiply/divide items are grade 5-6), and a search of its source finds no place-value chart or jump-counting scaffold. It also contradicts `timer-policy.md` today (item 12). So the new game is a scaffold-first sibling, not a duplicate; to rule: does it sit beside Blitz or replace it, and note the CLAUDE.md rule that a scaffold must fade once the student can work without it. | Jon: design points 1-4. The relationship to Standard Form Blitz is ruled, see 3.5 |
| 3.5 | **Resit strand rulings (Jon, 30 Sep 2026).** (1) **Register: every resit-strand game gets an adult register.** A game entering the strand is restyled to it regardless of what its roster levels give it under canon §7.5.1, which says the lowest tier served decides. **Canon §7.5 / §7.5.1 were rewritten on 2 Oct 2026 (one adult register for every game), which carries this rule; the note that they had not been amended is out of date (corrected 3 Oct 2026).** The audit's §5 lists what needs changing: of the 24 candidate-suite games (audit §10.5 lists **31**; use §10.5, this count is unreconciled), 12 list Year 6 first and 12 render a different row from the one §7.5.1 gives them (measured 30 Sep). (2) **`standard-form-blitz` stays** as it is; standard form is STRETCH (`N9.1`), COVERED by it. (3) **"Don't Count the Zeroes" is built as the resit-strand standard form game** — this rules the relationship question left open in 3.4: it sits beside Blitz, does not replace it, and is scaffold-first with a place-value chart. The 3.4 design points 1-4 are still owed. The item 12 conflict between Blitz and `timer-policy.md` is not touched by this ruling. Banding: audit §10. (4) **Algebra basics is one game (Jon, 30 Sep 2026): `A4.1` (simplifying, surds excluded) and `A1.1` (notation) join `A3.1` (vocabulary) and `A7.1` (function machines)**, so audit §10.4's ranks 7, 8 and 11 are one build of 4 formal parts plus the `A4.3` sub-skill (expanding one bracket). The audit's table is left as the record of the ranking on the day. (5) **Six Sevens, Bruv** follows (1): first game under the amended §7.5.1. | Jon: none on the banding (all ruled 30 Sep); canon §7.5.1 amendment (a canon contract, not started) |
| 3.6 | **Free Daily Pizza — FDP equivalence, resit fluency strand game 2. DONE 30 Sep 2026 as `free-daily-pizza` (START block has the full record and ten points for Jon).** Was: QUEUED 30 Sep 2026 for a new session, to start only after Six Sevens, Bruv is merged. Jon's full seven-field contract, with his addendum (the daily pizza is a fixed easiest-first mix: 3 from S1, 3 S2, 2 S3, 2 S4, verified for any date), is recorded verbatim in `docs/next-contract-free-daily-pizza.md`, with notes on leaderboard keying for its two STOP IFs. Top of the audit §10.4 build list (the fractions game, 7 parts incl. `R3.1`/`R6.1`). | Done; Jon: eyeball pass and the ten points in START |
| 3.7 | **Six Sevens, Bruv fits a phone — DONE 30 Sep 2026.** After a wrong answer, Next is above the fold on all 144 orientations at 320×568, 375×667 and 390×844; before, it was below the fold on every one, with its bottom edge 782–1,006px down the page. Keypad hidden during wrong-answer feedback; grid collapsed to a bar on narrow screens; order fact → hint → array → Next; the array below Next on screens 600px tall or less. The phone rule is canon §7.6.1. Open: Aa mode, and the 41px shared Next control. Full record in START OF NEXT SESSION. | Done; Aa mode for Jon |
| 3.8 | **Leaderboard tidy — BUILT 30 Sep 2026 (PR 23), follow-ups built the same day.** `regression-rumble` Level 4 plays from the button; tier 1 presses every level button (125 controls, 47 games); `binomial-blaster` roster row is A-Level Year 2; `levelLabel()` names every submitted level, on the ticker and the hub; one roster-level table (`scripts/roster-levels.json`); `extract-banks.py` fails loudly on a dead server. Full record in START OF NEXT SESSION. Open: seven other scripts start the stub server unchecked, and 14 games keep in-game level-name maps. | Done; follow-ups listed |
| 3.9 | **Phone fit, every game (Jon's contract, 1 Oct 2026). New Shapes DONE 1 Oct (START block). The rest: fix one game at a time, never by sweep.** `scripts/measure-phone-fit.py` measures each game's first question at 320×568, 375×667 and 390×844 and writes `docs/phone-fit-report.md` (report only, not a CI gate). 56 games failed on 1 Oct; **the order to fix them, in batches of three, is the subsection "3.9 — Phone fit order" directly below this table** (Jon, 1 Oct 2026). **Also worth reading in the report:** 11 games pass but show no Next after a wrong answer (they auto-advance; canon §7.6's open rollout, not a fit problem); 12 pass on the asking screen but the driver could not produce a wrong answer; 10 are UNMEASURABLE (no answer controls the generic driver recognises: the four Core Maths papers, `bearing-blitz`, `equation-builder`, `four-quadrant-explorer`, `shape-shifter`, `spot-the-error`, and `six-sevens-bruv`, measured by hand on all 144 orientations on 30 Sep, item 3.7, though its verifier does not re-measure it). **For each game:** measure every question shape in full first (as New Shapes and Six Sevens were), then apply canon §7.6.1. One sample per size means a game near the fold can flip between runs. Not measured by the script: the on-screen keyboard over a native input, Aa mode, levels other than the default. **Since 2 Oct 2026 (PR 62) tier 1 also gates width at 320×568: each game's batch removes the game's `tier1_phone_overflow` entries (`load` and `start`) in `scripts/checker-allowlist.json`, and CI fails on a stale one.** | Order set 1 Oct (below); one game at a time within each batch **graph-sketcher DONE 9 Oct 2026 (contract GRAPH-SKETCHER-FIT, #PR):** its overflow was its own: the canvas was sized to its panel less 12px (the panel has about 21px of padding and border, so each scenario widened the grid track ~9px more, 361 to 567px) with a 320px floor, and the grid tracks were plain `fr`, so the value table widened its column instead of scrolling in its box. Now `minmax(0,..)` tracks and the canvas sized to the panel's content box: no sideways scroll at 320, 390 and 412 for every one of the 45 scenarios; its `tier1_phone_overflow` entry is removed. |
| 3.10 | **Portal fits a phone — DONE 1 Oct 2026 (Jon's contract, widened by Jon to the whole top of the page).** First game card, no filter: 4,637 → 1,025px at 320×568 (8.16 → 1.80 screens), 4,284 → 998 at 375×667 (6.42 → 1.50), 4,431 → 946–1,020 at 390×844 (5.25 → 1.12–1.21). With a filter tapped, the first result is on screen at every phone size (before: 5–7.6 screens down). Sticky filter bar 276 → 109px. One `.cmp` mechanism for the fact card, escape band, parents strip and "New for 2026/27"; desktop with no filter pixel-identical. Full record in START. | Jon: 320 is 173px over 1.5 screens; the remaining cuts are features (START, Needs Jon 1) |
| 3.11 | **Priority audience (canon §0.2, tier 2). percentage-flip: KS3 and GCSE share one 12-question bank** (QUESTIONS_DEFAULT; routing at :216 sends every non-year6 level to it as 'all'); Year 6 has 20. No ?level=gcse entry point exists: the portal card, spec-map (incl. GCSE N12) and parents/fractions all link ?level=ks3. Answer format is a typed number (input type=number, parseFloat, ±0.01), so all resit percentage skills fit if each question states the form to type. Plan: separate KS3 and GCSE banks of 40+ each, GCSE aimed at grade 1–3 resit content; routing branch and a GCSE entry point. Also false copy: start screen 'Questions get harder as you go' and portal card 'Gets progressively harder. Great GCSE prep.' (shuffle() discards the bank order). The 3 questions shared with YEAR6 are harmless across levels; resolve them in the rewrite. Wrong-answer fixed timer is already batch 3 (§7.6). (Jon, 2 Oct 2026.) | **Project Claude** — content; **Code Claude** — routing |
| 3.12 | **Theme migration queue (canon §7.5; Jon's contract, 2 Oct 2026). Split It DONE as the pilot (START block). The other 96: one game at a time, never by sweep.** Each migration moves the game from NOT_YET to MIGRATED in `scripts/check-theme.py` in its own PR, with its phone fit re-measured in normal and Aa mode (`measure-phone-fit.py --only <slug>` and `--aa`, both to a scratch `--out`) and every wording change quoted for Jon. **Order. (1) The resit suite first** (`docs/resit-coverage-audit.md` §10.5), **each game's migration and its phone-fit fix done together, in §3.9's batches of three:** batch 2 `distinctly-average`, `estimation-golf`, `angle-ace` (held for this contract by Jon's ruling of 2 Oct 2026); batch 3 `think-of-a-number`, `decimal-detective`, `percentage-flip` (percentage-flip's with its rebuild, §3.11); batch 4 `correlation-or-coincidence`, `prime-or-composite`, `chart-interrogator`; batch 5 `factor-race`, `given-that`, `formula-forge`; batch 6 `prime-factorisation`, `formula-unlocked`, `linear-equation-solver`; batch 7 `estimation-engine`, `probability-pioneer`, `like-terms-collector`. **Then the 12 suite games with no phone fix outstanding**, in threes: `better-value`, `formula-plug-in`, `expected-damage` (fitted in batch 1); `new-shapes`, `sequence-solver`, `unit-converter`; `negative-number-line`, `proportion-blaster`, `bearing-blitz`; `equation-builder`, `four-quadrant-explorer`, `stat-attack`. **(2) Then the rest (66)**, in §3.9's Group 3 batch order where a game has one, then the games with none. **Light to dark (3):** `differentiation-duel`, `integration-duel`, `log-laws` (the light-slate sub-family; all three are in §3.9 batches 8–9). **Dark to light (53):** every game whose roster levels include Year 6, KS3 or GCSE and that renders dark today (measured 2 Oct 2026 by body background), including the resit strand's `six-sevens-bruv` and `free-daily-pizza`. `python scripts/check-theme.py` prints each NOT_YET game's expected palette and findings. **Rulings (Jon, 2 Oct 2026).** (a) **Level names:** a key stage or year group
becomes Foundation / GCSE / Advanced (the third only where a game needs it; **superseded 3 Oct 2026 by canon SR-11: Year 6 is "Starter", KS3 "Foundation"**, applied to the 31 resit-suite games in one PR); Split It's KS3 is already
"Foundation". (b) **Firebase level keys never change.** The label a student sees is declared once per game and
read by the leaderboard hub (today `levelLabel()` in `firebase-leaderboard.js` names every game's `ks3`
"KS3"); this is done in each game's migration pass, **Split It in the next one**, and folds into `games.json`
when that is built. (c) **Age wording** (`check-theme.py --verbose`, 27 games) is removed game by game as each
game migrates, never by sweep; each batch quotes its before and after lines for Jon. (d) **§3.12 is not next:**
see the START block's NEXT line. | **Code Claude**, batch by batch; **Jon** rules each batch's wording |
| 3.14 | **Portal labelling, for a later ruling (found 3 Oct 2026 while mapping §1.42; reported, not changed).** Year 6 games whose content is KS3 in the National Curriculum, not KS2: `probability-pioneer` (KS2 has no probability), `like-terms-collector` (collecting like terms), `new-shapes` (trapezium area, prism volume; Year 6 has parallelograms, triangles and cuboids), `shape-shifter` (rotation; Year 6 has translate and reflect), `decimal-detective` (rounding to 1 s.f.). `seven-bridges` offers KS3 and GCSE levels, but graph theory is in A-Level Further Maths only (AQA 7367 DA1–DA2). `truth-buster` is listed KS3, GCSE, A-Level but every session mixes 7 KS3/GCSE, 7 A-Level and 6 "beyond the curriculum" statements and submits as level `all`. | **Jon** |
| 3.15 | **SR-11 left the leaderboard hub and the portal ticker alone (3 Oct 2026, PR A of the resit section).** `MaffsLeaderboard.levelLabel()` (`schools/assets/firebase-leaderboard.js`) names `ks3` "KS3" and `year6` "Year 6" for every game, and `submitScore()` writes that label into each `recent_scores` entry. Changing it would change what is sent to the leaderboard, which the SR-11 contract forbids (STOP IF). A fix that keeps every stored value: map the label at render time on the hub and the ticker, per game, from the declared labels (§3.12 ruling (b), `games.json` when built), and leave the stored label alone. | **Jon** — contract |
| 3.16 | **School-year wording inside question contexts in resit-suite games (listed under SR-11, not changed: question content).** `given-that` `gcse_15` ("200 students — Year group and Lunch choice", columns are year groups), `gcse_20` ("90 Year 9 students — Subject choices"), `gcse_25` ("250 students — Year group and Canteen satisfaction"); `chart-interrogator` `S2` ("Heights of Year 10 students (cm)"). Each is a survey of school students, a context choice. | **Jon** — keep, or new contexts |
| 3.17 | **`prime-or-composite` needs a Foundation-range option to join /resit/** (Jon, 3 Oct 2026: held out of the resit suite because its numbers run to 9,973). A level or mode with Foundation-range numbers, then add it to `SUITE` in `check-resit-page.py` and a card on the page in the same PR. | **Jon** — scope; then CC |
| 3.19 | **Latent, not live: `section_clicked` sends position 0 when one element carries both `data-mfg-section` and `data-mfg-item`** (found 3 Oct 2026 building the /resit/ portal badge). `analytics.js` finds the section with `closest()`, which matches the element itself, but counts position with `sec.querySelectorAll('[data-mfg-item]')`, which does not include it. No live markup does this: the badge's section is a `display:contents` wrapper. Fix (count `sec` itself when it is an item) or document the rule in the analytics.js comment. | CC — small, when analytics.js is next touched |
| 3.20 | **Back links/headers: 40 games are not on the standard pattern** (survey 4 Oct 2026, all 99 `games/` folders). Standard, used by 59 since just-pythag-it-bruv moved to it (PR #32, 4 Oct): `<a href="../../" class="back-link">← Back to Games</a>` above the game header (its CSS varies cosmetically). Fold each game onto it in its §3.12 theme migration, never by sweep. **Entity only, looks identical (10):** chart-interrogator, complex-converter, gradient-hunter, higher-power, matrix-crunch, proportion-blaster, screening-room, tax-theft, trig-identity-duel, the-perfect-prank (off-roster prototype). **Split It's header bar, `class="back"` (15):** differentiation-duel, distinctly-average, factor-race, fraction-equivalence, index-laws, integration-duel, log-laws, modular-battle, percentage-flip, prime-factorisation (`href="/"`), quadratic-factoriser, regression-rumble (withdrawn), split-it, suvat, trig-worms. **`back-link` saying "MaffsGames" (4):** core-maths-paper1, -paper2a, -paper2b, -paper2c. **`back-link` to `/` (1):** fermi-lab. **Inline-styled link at the bottom (4):** better-value, expected-damage, formula-plug-in, new-shapes. **Inline-styled themed link (2):** estimation-golf, trig-wars. **A logo, not a back link (2):** 52dle, equatle. **`home-btn` (2):** boolean-blitz, truth-will-set-you-free. Whether the standard should become split-it's bar instead is Jon's call (§7.5 design). | Jon / per game |
| 3.21 | **Phone-fit checks do not model the system keyboard (found 4 Oct 2026, the phone keypad PR).** Every phone-fit measurement (tier 1's phone pass, `measure-phone-fit.py`, the per-game verifiers) loads the page at a full window height. On a real phone, focusing a typed-answer box opens the system keyboard, which takes roughly 40% of the screen, so a game that fits on paper can hide its question or diagram the moment the student starts typing (Just Pythag It, Bruv did; its keypad PR stopped the keyboard opening at all). **Games with a typed answer box (22, survey 4 Oct 2026, `<input>` of type text/number or built in script, leaderboard name fields excluded):** `52dle`, `chart-interrogator`, `component-crusher`, `estimation-engine`, `estimation-golf`, `factor-theorem`, `fermi-lab`, `given-that`, `glorious-gantt`, `graph-sketcher`, `growth-and-decay`, `just-pythag-it-bruv` (done: MaffsCalc's answer target, canon §4.4), `like-terms-collector`, `log-laws`, `percentage-flip`, `quadratic-factoriser`, `screening-room`, `split-it`, `stat-attack`, `suvat`, `tax-theft`, `test-the-claim`. Name or initials fields only (the keyboard opens at the end, over nothing that matters): `equatle`, `prime-or-composite`, `six-sevens-bruv`. **Options, for Jon:** (a) measure each game with the window shortened by a keyboard's height while the answer box has focus (Chromium cannot show the real keyboard; a shortened viewport is the model), and fix what that finds per game, with §3.9's phone fit; (b) give typed-answer games the shared keypad (MaffsCalc's answer target, or a keypad-only mount for games without a calculator), so the keyboard never opens. **Jon ruled (b), 4 Oct 2026:** the shared keypad, which fixes the cause once, in one place. **The shared layer is built (5 Oct 2026, PR #70):** `MaffsKeypad` (`schools/assets/keypad.js`, canon §4.4), the keypad-only form for games without a calculator and for several answer boxes; MaffsCalc's answer mode composes it, so there is one phone keypad. **Still to do: the rollout**, one game per contract, each game's phone fit measured with the keypad. **`estimation-engine` is the first game on MaffsKeypad (PR #74, 6 Oct 2026).** | Code Claude |
| SIX-PS-THREE-BANKS | **Three 6 P's banks from live games, stopped at step 1** (#561: source counts short, nothing banked). `venn-two-way`, `straight-line-graphs` and `constructions-loci` do not exist yet. Contract and stop report: `docs/handover/contracts/2026-10-26-six-ps-three-banks.md` and `...-report.md`. | home lane; Project Claude writes the questions the sources lack |
| FOLD-COMPONENTS | **FOLD-COMPONENTS PRs 3–6, on branches, each needing main merged in:** PR 3 `claude/fold-options-v2` (44a4ef8), PR 4 `claude/fold-figures-v2` (227c3d6), PR 5 `claude/fold-canon` (4a526a6), PR 6 `claude/fold-publish` (ed00d80; stops before merge for Project Claude's live 404 check). PRs 1–2 merged (#563, #564). Contract: `docs/handover/contracts/2026-10-27-fold-components.md`. Moved from cloud.md's live pointers. | cloud lane (the contract's lane exception) |
| KEYPAD-FRACTION | **The / key on the shared keypad:** branch `claude/keypad-fraction` (fbf6c36: 799dbfd9 cherry-picked, 4 plants; phone-fit on the 19 keypad games identical to main in all three modes) needs main merged in. After it merges, the build lane sets `FRACTIONS = true` in `games/y-so-steep/` (Stage 3). Moved from cloud.md's live pointers. | cloud lane |
| COMIC-CAPER-PRIME-LOCK | **Comic Caper's "count primes 1..V" lock becomes a list of 6–8 volume numbers between 20 and 40**, with divisibility hints and equal effort per variant (Jon, 7 Nov 2026). See VARIANT-EFFORT, §4. | Project Claude to contract; cloud lane |
| SIX-PS-LOOK-REDS | **Look audit, 25 Oct: factor-race and distinctly-average use pixel fonts**, which must change before The 6 P's is listed. Check first whether it is done: LOOK-REDS-2 (#554) moved Distinctly Average onto theme.css. | cloud lane (per-game) |
| BETTER-VALUE-NEXT | **Better Value's Next is about 180 px below the fold at 1366 × 768.** | cloud lane |
| HOW-MANY-PARTS-FRACTION | **How Many Parts? moves onto MaffsFractionInput** (`scripts/fraction-input-warn.json`): home.md's Queue line "how-many-parts to move next", moved here 7 Nov; part of the FRACTION-STACK follow-up in cloud.md's Queue. | cloud lane |
| CURLING-TEACH | **Curling Friction teaching, Level 4.** Low priority. | held by Project Claude since 4 Nov |
| ABOUT-PAGE | **Project Claude's About-page contract (27 Oct), never sent.** | **Jon**: keep or drop |
| LOOK-REFRESH-PALETTE | **57 of the 88 NOT_YET games render a different palette from canon §7.5's rule** (53 dark where it gives light, 4 light where it gives dark); list in the contact-sheet PR (LOOK-REFRESH-1, Amendment 1 ruling 4). Moved from cloud.md's live pointers. | Project Claude to triage |
| SPEC-MAP-SHORT-BANKS | **Spec-map rows whose banks do not teach, and possibly short banks** (SEARCH-KEYWORDS ruling 6): archive entry "SEARCH-KEYWORDS triage lists" in `docs/history/handover-cloud-archive.md`. Moved from cloud.md's live pointers. | Project Claude to triage |
| PRIME-SPRINT-LOOK-REDS | **Prime Sprint (LOOK-REDS) waits for Jon's next contract:** a live tail of the Queue DONE items moved 4 Nov (`docs/history/handover-cloud-archive.md`). Check first whether LOOK-REFRESH-1 (#660, Prime Sprint onto the shared adult theme) settled it. Moved from cloud.md's Queue 8 Nov (BRANCH-CLEANUP). | **Jon** — the contract |
| ESTIMATION-GOLF-ART | **Estimation Golf art parked: the game has no start screen; placement to be decided** (Jon, 2 Nov; branch `art/estimation-golf`, 028cf683, the PNG unchanged, no PR). Parked with the older Queue items (Jon, 3 Nov). Moved from cloud.md's Queue 8 Nov (BRANCH-CLEANUP). | **Jon** — placement |
| HIGHER-POWER-PHONE | **Higher Power's card values spill on phones** (item 4 of the cloud lane's session queue, Jon, 27 Oct). Parked (Jon, 3 Nov). Moved from cloud.md's Queue 8 Nov (BRANCH-CLEANUP). | cloud lane |
| SCREENING-ROOM-PANELS | **Screening Room panels and the hardened top-scores check** ("item E", item 5 of the 27 Oct session queue): no contract text found in the repo; ask Jon. Parked (Jon, 3 Nov). Moved from cloud.md's Queue 8 Nov (BRANCH-CLEANUP). | **Jon** — the contract; then cloud lane |
| ANSWER-CONTROL-TALL-INPUT | **The answer-control (8) and tall-input (6) games** (item 7 of the 27 Oct session queue). Parked (Jon, 3 Nov). Moved from cloud.md's Queue 8 Nov (BRANCH-CLEANUP). | cloud lane |
| TAKE-A-WALK-PHONE-LAYOUT | **Take a Walk's walk-or-cover and answer screens overflow a phone** (found by TAKE-A-WALK-SEED's sweep, 12 Nov 2026; Jon's option 1, the split). Measured with measure-phone-fit.py's own `__pfAsking` (the last answer control's bottom against the fold), 200 seeds x 4 stages, 968 question variants, every asking screen, on main 7736de6. **Stage 1's first question, walk or cover** (all phone-fit measures): 375x667 normal 0 of 200 seeds over; 375x667 Aa 7 of 200 (+50, 677/627, CI's red); 320x568 normal 31 of 200 (+36, 564/528, CI's red; seed 168); 320x568 Aa 200 of 200 (+218, the recorded Aa exception). So 36-50 px for the first question. **Every Stage 1 walk-or-cover screen**: up to +111 (320x568 normal) and +120 (375x667 Aa); 375x667 normal fits (-13). **The answer screen** (after walk or cover; every question in Stages 2-4), never measured by phone-fit: 375x667 normal Stage 2 84 of 462 over (+7), Stage 3 28/195 (+32), Stage 4 103/131 (+96, the calculator); 375x667 Aa every screen over, +206 to +394; 320x568 normal every screen but two over, +163 to +272; 320x568 Aa every screen, up to +586. At 320x568 the card starts at 145 px, the question is 74-99 px, the to-scale drawing up to 282 px, the answer row wraps to two lines (96 px, Check on the second); headless Chromium shows no keypad, which adds more on a phone. Not a spacing fix: capping the drawing shrinks its 12 px labels with it (282 to 150 px halves them). Screenshots (main, seed 168, 320x568 normal): `docs/screenshots/take-a-walk-walk-or-cover-seed168-320x568.png`, `docs/screenshots/take-a-walk-answer-seed168-320x568.png`. The Gate is not red over it: with the seed fixed it always measures the same first question (486/528, Aa 599/627, Aa 320x568 668/528 WARN). | **Jon** — a design ruling for the answer screen; then cloud lane |
| BOOLEAN-BLITZ-LENGTH | **Boolean Blitz: a start-screen choice of 10, 20 or all 42 questions, with one leaderboard per length (SR-22).** After the live-bug fixes. Jon, 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| CLAIM-WALKTHROUGH | **Test the Claim: an optional, very clearly shown "Watch one first" worked example per mode** (one idea per screen, the student's Next, unscored); step feedback naming the actual mistake; "Show me" after two wrong tries. Jon, 9 Nov 2026 (DOCS-BUNDLE). | Project Claude writes the scripts for Jon's approval before the build; then cloud lane |
| FORGE-SUBJECT-PROMPT | **Formula Forge: the subject letter in "Make … the subject" much more prominent**, and a start-screen line "Powers and Multi: have paper handy". Jon, 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| SCROLL-BOX-FOCUS | SCROLL-BOX-FOCUS — the .tt-scroll and .table-scroll boxes from #721 are not keyboard-focusable in Safari; add tabindex="0" (and an aria-label naming the table) where the wrapper is created (teacher.js, guide.js). (Project Claude's review of #721, 10 Nov 2026.) | home lane |
| CHART-INTERROGATOR-SCROLL | CHART-INTERROGATOR-SCROLL — Chart Interrogator scrolls 34 px sideways at 375 px wide (found by #725's checks, 10 Nov 2026; on main before #725). Find the element that overflows and fix it in the game. (Code Claude, #725, 10 Nov 2026.) | cloud lane |
| WHEN-WILL-I-USE-THIS | WHEN-WILL-I-USE-THIS — a 'When will I use this?' section: for each area of maths, where it appears in real life and careers, by topic and by vocational route (Skills England's 15 routes), each scenario sourced and linked to the games that practise it; as many areas of maths as possible (Jon, 10 Nov 2026). Spec: Project Claude (draft 10 Nov), then contract. | **Project Claude** (spec) |
| EVERYDAY-MAFFS | EVERYDAY-MAFFS — an 'Everyday MAFFS' section teaching the maths people need in daily life (tax, compound interest and debt, mortgages, pensions, inflation, everyday probability), migrated from MathsWins' six Everyday Maths courses and rewritten: every tax/NI/pension figure states its tax year and check date (yearly review row); nothing from or naming the MathsWins Academy's gambling courses comes across (Jon, 10 Nov 2026). Separate from WHEN-WILL-I-USE-THIS. | **Jon** (scope), then Project Claude |
| SIX-PS-SHORT-WRONG | **The 6 P's wrong state on short screens (Jon's ruling, 27 Oct 2026): 14 questions at 320 x 568 have Next 1 to 208 px below the fold** (worked lines plus figure taller than the screen: area 5, basic-probability 3, pie-charts 3, percentages-money 2, simultaneous 1). Parked in `KNOWN_FAILURES` in `scripts/sweep-six-ps-wrong.py`, which only shrinks. The working is not shortened. **Later fix:** on short screens in the wrong state, shrink or hide the figure; then delete the entries. Moved from §6, 11 Nov 2026 (TODO-TIDY). | cloud lane |
| EXPECTATION-EXACT | **Expectation Station: exact everywhere. RULED 29 Sep 2026 (Jon): go exact everywhere.** Retire `formatPNum` globally — all 42 decimal scenarios move from "0.50"-style padded output to exact ("0.5"), matching FRACTION mode. Not yet built: `formatPNum` still has 3 uses in `games/expectation-station/index.html` on 11 Nov 2026. Moved from §6 (TODO-TIDY). | cloud lane |
| KILN-FOLLOW-UPS | **The Kiln Disaster's follow-ups, RULED 29 Sep 2026 (Jon), not built on 11 Nov 2026.** (1) **Name him.** Add Mr Stephen Mudge's real name to the teacher page alongside "Smudgey", so a teacher opening it cold isn't confused (the name is only in `escape-rooms/kiln-disaster/room.js:43`'s hook, which `teacher.js` does not show). (2) **Add the explanation.** Document on the teacher page (not just canon §11.3) that a group hitting only named misconceptions skips some of Smudgey's wrong-entry lines by design. (3) **Set a floor on `a`.** Constrain the check-value lock generator so no future variant lands as lopsided as "2 + 48 ÷ 2" (`scripts/gen-escape-variants.py:638`; that variant is still in `room.js`). Moved from §6 (TODO-TIDY). | home lane (the shared variant generator) |
| MONEY-THOUSANDS | **Money answers not in whole pounds, left unboxed by MONEY-ANSWERS (CLOUD-QUEUE-1111 PR 2, 11 Nov 2026) for Jon to rule.** MONEY-ANSWERS boxed every typed answer in pounds (£, £/kg, £/m, £/litre); these answers are amounts of money in another unit, and a £ inside the box would misstate them, so each is unchanged. **£k (thousands of pounds):** `stat-attack` CM1 'Annual salaries (£k)' and CM4 'House prices (£k)' (mean, midpoints, fx, standard deviation typed; the unit shows only in the table's class label, 'Salary (£k)', 'Price (£k)'); `chart-interrogator` B4, B5 (box plots) and CF4, CF6 (cumulative frequency) (Phase 1 readings typed in thousands; the unit shows in the context title and axis, '(£k)', and Phase 2's text writes £28k); `graph-sketcher` CM2 and CM13 (table values and reads of P, axis 'P (£k)'). **£100s:** `as-you-can-see` Stage 4's 'Value (£100s)' scatter (the estimate of y and the outlier's value, axis 'Value (£100s)'). **Pence:** `estimation-golf` 'If 8 pencils cost 96p, what does 1 pencil cost in pence?' (unit 'p', shown after the box). **Escape rooms (shared `escape-rooms/assets/engine.js`, home lane; outside MONEY-ANSWERS' lane exception):** `prom-budget` 'Transfer amount — whole pounds' and `library-jam` 'TOTAL TO REVERSE, IN POUNDS' (keypads, whose typed fallback keeps digits only, so a typed £ is dropped, not an emptied box), `big-school-begins` 'LEFT ON THE CARD (PENCE)' (keypad, pence), `canteen-hack` 'Baseline prices — whole pounds' (two dials whose typed fallback is `type="number"`, so a typed £ empties it; the rooms do not load answer.js). To rule: how each unit is boxed or shown (a £ box with 'thousands' beside it, the unit written after the box, or as it is), and whether the room engine gets money boxes. Recorded 11 Nov 2026 (contract CLOUD-QUEUE-1111, PR 2). | Jon (ruling); home lane (the room engine) |
| WARMUP-PACKS-APPROVE | **The ★ Warm-up print packs: Jon proofreads The Comic Caper's and The Library Jam's PDFs and approves their wording** (contract WARMUP-PACKS, 12 Nov 2026). Each room's `tools/pack-generator/rooms/<slug>/config.json` has `wording_approved: null`, so pages 1 and 2 carry the DRAFT badge. Build each at home with `python -X utf8 tools/pack-generator/build_pack.py comic-caper` (and `library-jam`), proofread against the README's "What to proofread" 1-8, then record the approval in the config. Then the `--final` builds go to Tes, and the ★ Warm-up bundle of Kiln, Comic Caper and Library Jam can be listed. Caption gaps fixed by CAPTION-GAPS (13 Nov 2026). | Jon's proofread |
| PACKS-REAPPROVE | **The Kiln Disaster's and The Christmas Tree Fiasco's print packs: Jon proofreads each pack's answer-key page (page 4), the only page that changes, and re-approves** (contract CAPTION-GAPS, 13 Nov 2026). The key's "About this room" box now prints the level from the room's rating (`escape-rooms/assets/rating.js`): Kiln "Level: Warm-up (1 of 3 stars), grades 1–3, set by the hardest lock." in place of "Built for grade 3/4 resit students: ..."; Christmas "Level: Core (2 of 3 stars), grades 4–5, set by the hardest lock." where it had no level line. Both configs' `wording_approved` is `null` until then, so pages 1 and 2 carry the DRAFT badge and `--final` refuses. Build each at home with `python -X utf8 tools/pack-generator/build_pack.py kiln-disaster` (and `christmas-tree-fiasco`); record the approval in `tools/pack-generator/rooms/<slug>/config.json`; then the `--final` builds replace the Tes PDFs. | Jon's proofread, then home lane |

### 3.9 — Phone fit order (Jon, 1 Oct 2026)

**The rule for the order.** First, the failing games in the candidate resit suite (`docs/resit-coverage-audit.md` §10.5), worst first; then `like-terms-collector`; then the rest, worst first. "Worst" is the report's ranking: pixels past the fold at the worst size, with sideways-only failures after every fold failure. Batches of three, so each game can be play-tested after its fix. Within a batch, still one game at a time, never by sweep.

**Rulings on this list (Jon, 1 Oct 2026).** (1) New Shapes' right-answer Next: fix, in batch 1. (2) `expected-damage`, `estimation-golf` and `fermi-lab` (WAITS, unmarked) **keep waiting for Next after every answer**: each answer's rating is worth reading (§7.6). Their Next must still be above the fold. (3) **Wrong-answer timers** (the "Seen while reading" list below): fixed in each game's own batch where the game already has an explanation to show; where it has none, it is §7.6 Group C, left on its timer and listed there. (4) `like-terms-collector`: measure its feedback screen first. **The batch contract is one template for every batch** (Jon's "Phone-fit batch <N>" contract of 1 Oct): measure before, apply §7.6.1, apply §7.6 as ruled above, measure after, update the report and this list.

**Batch 1 done (1 Oct, evening; record in START).** The regenerated report also moved three untouched games, each because it samples one random first question: `negative-number-line` (resit suite) and `like-terms-collector` (batch 7) scroll sideways at 320 on some question, and `truth-buster` is 7px over at 320. `negative-number-line` and `truth-buster` are in no batch yet; placing them is Jon's call. `linear-equation-solver` and `moments-master` passed this time; both are within ~25px of the fold, so measure them in full in their batches.

**Not a shared-asset problem (checked 1 Oct, the contract's STOP IF).** The vertical failures come from each game's own content above its controls. The fold already subtracts the fixed footer, and no shared script adds anything to the asking screen: `session-length.js` draws on the start screen only, the leaderboard overlay appears at the end of a game only, and `next-control.js` draws only the Next button itself. All ten sideways scrolls were traced at 320×568 to an element in the game's own markup: game headers (`maths-court`, `probability-pioneer`, `equatle`), game layouts (`tax-theft`, `estimation-golf`, `trig-wars`), `equatle`'s keypad row, `estimation-engine`'s Submit button, and `differentiation-duel`'s Aa button (1px). `decimal-detective` and `proof-builder` did not scroll on the first question at that sample, so theirs shows on a later screen; neither game loads a shared script that draws anything. The shared footer's "☕ Support MaffsGames" link does overrun 320 and 375 phones, but it is `position: fixed`, so it is clipped rather than scrolled. It causes none of the 56 failures; it is the cosmetic defect already noted in START. **One bug shape does repeat, though not through a shared file: a header row too wide for 320px** (`maths-court`, `probability-pioneer`, `equatle`, and New Shapes before its fix). Each is per-game CSS, so it is fixed in each game's own batch.

**What happens after a correct answer**, read from each game's source (no edits). Canon §7.6 says a right answer advances briskly and only a wrong one waits for Next. The flag matters for the fit as well as for §7.6: **wherever a right answer waits, its Next has to be above the fold too, so that screen must be measured alongside the asking and wrong ones**, and canon §7.6.1's "hide the keypad on a wrong answer" becomes "hide it on both", as in New Shapes.

- **advances** — a right answer moves on by itself (delay given). §7.6 satisfied on the right-answer side.
- **WAITS** — a right answer shows Next and waits for the student. §7.6 says it should not.
- **WAITS, unmarked** — the game has no right or wrong, only a score or rating, and shows Next after every answer. §7.6's right/wrong split does not map onto it; Jon's call.
- **n/a** — no question-by-question advance at all.

Tally over the 56: **27 advances, 21 WAITS, 3 WAITS unmarked, 1 by mode, 4 n/a**, plus `like-terms-collector` (WAITS).

**Group 1 — failing games in the resit suite (20 of the suite's 31; the other 11 pass or are UNMEASURABLE).**

| Batch | Game | Fail | After a right answer |
|---|---|---|---|

| 2 | `distinctly-average` | +353 | advances, 1200ms (`:1421`) |
| 2 | `estimation-golf` | +322, sideways | **WAITS, unmarked**: strokes, not right/wrong; "Next Hole" every time (`:860`) |
| 2 | `angle-ace` | +287 | advances: phase 1 to phase 2 at 800ms, then the next question at 1000ms (`:797`, `:825`) |
| 3 | `think-of-a-number` | +234 | **WAITS**: Next on both (`:642`) |
| 3 | `decimal-detective` | +212, sideways | **WAITS**: "Next Case" on both, all three question types (`:847`) |
| 3 | `percentage-flip` | +180 | advances, 3000ms. The same timer runs on a wrong answer, which gets no Next either (`:300`) |
| 4 | `correlation-or-coincidence` | +143 | **WAITS**: solution or tinfoil card with Next, on both (`:328`) |
| 4 | `prime-or-composite` | +139 | advances, 1800ms (`:413`) |
| 4 | `chart-interrogator` | +126 | **WAITS** at the end: phase 1 sub-questions advance at 600ms; phase 2 shows the model answer and waits (`:817`, `:1042`) |
| 5 | `factor-race` | +119 | advances, 1600ms. The same on a wrong answer, with no Next (`:348`) |
| 5 | `given-that` | +119 | **WAITS** at the end: phase 1 to phase 2 at 1200ms; phase 2 shows the worked explanation and waits (`:804`, `:935`) |
| 5 | `formula-forge` | +83 | advances, 1000ms (`:453`) |
| 6 | `prime-factorisation` | +77 | advances, 1500ms once the factorisation is complete (`:346`) |
| 6 | `formula-unlocked` | +69 | advances, 1000ms (`:487`) |
| 6 | `linear-equation-solver` | +26 | advances: each phase at 700ms, a clean question at 800ms; a question with any miss shows the working and waits (`:422`, `:441`) |
| 7 | `estimation-engine` | sideways only | advances, 2000ms. The same on a wrong answer, with no Next (`:409`) |
| 7 | `probability-pioneer` | sideways only | **WAITS**: Next on both, in all three stages, behind its 5s floor (`:513`) |

**`split-it` (resit suite; passes, so in no batch): re-measured for the theme pilot, 2 Oct 2026.** Asking screen,
bottom edge / fold, normal 410/354/354 → 403/350/350 and Aa (`--aa`) 470/386/386 → 459/378/378 at 320×568,
375×667 and 390×844, all above the fold, no sideways scroll; the wrong-answer screen is still unmeasurable by the
driver ("could not get an answer marked"). No worse at any size (§3.12, START block).

**Group 2.**

| Batch | Game | Fail | After a right answer |
|---|---|---|---|
| 7 | `like-terms-collector` | **not one of the 56**: passes the asking screen at all three sizes; the driver could not get an answer marked, so its feedback screen is unmeasured | **WAITS**: Next on both (`:469`). Measure its feedback screen, right and wrong, before deciding there is anything to fix |

**Group 3 — the rest, worst first (36).**

| Batch | Game | Fail | After a right answer |
|---|---|---|---|
| 8 | `fermi-lab` | +652 | **WAITS, unmarked**: rating only, Next after every chain (`:684`) |
| 8 | `index-laws` | +588 | advances, 1800ms (`:787`) |
| 8 | `differentiation-duel` | +572, sideways | advances, 1800ms (`:981`) |
| 9 | `log-laws` | +570 | advances, 2000ms, Laws and Solve alike (`:1074`, `:1894`) |
| 9 | `integration-duel` | +562 | advances, 1800ms (`:1005`) |
| 9 | `boolean-blitz` | +521 | **WAITS**: walkthrough with Next on both (`:819`–`:856`) |
| 10 | `maths-court` | +401, sideways | **WAITS**: Next Case after 400ms (`:762`) |
| 10 | `truth-will-set-you-free` | +401 | **WAITS** at both stages (`:798`, `:865`) |
| 10 | `tax-theft` | +389, sideways | **WAITS** at the end: each step advances at 800ms; the finished payslip waits on "Next Salary" (`:1076`) |
| 11 | `wrong-on-the-internet` | +383 | **WAITS** at the end: stage 1 to stage 2 at 1200ms; stage 2 shows the explanation, then Next (`:1106`) |
| 11 | `complex-converter` | +369 | **by mode**: Roulette advances at 1200ms (and on a wrong answer too); Triples advances; Sniper is unmarked and waits on every shot (`:618`, `:849`, `:973`) |
| 11 | `terrible-advice` | +366 | **WAITS**: Next after 800ms (`:557`) |
| 12 | `seven-bridges` | +325 | **WAITS**: "Next Puzzle" (`:631`) |
| 12 | `suvat` | +325 | advances: phase timers of 1200–2400ms (`:737`, `:809`, `:923`) |
| 12 | `equatle` | +316, sideways | n/a: one puzzle; solving it opens the end modal, and Free Play's "Next Puzzle" waits (`:669`, `:781`) |
| 13 | `quadratic-factoriser` | +306 | advances, 1400ms; Higher's guided step 4 waits on Continue (`:1269`, `:1442`) |
| 13 | `word-problem-decoder` | +271 | advances, 1000ms. The same on a wrong answer, with no Next (`:786`) |
| 13 | `curling-friction` | +261 | advances, 1800ms (`:286`) |
| 14 | `matrix-crunch` | +255 | advances, 1000ms (`:343`) |
| 14 | `52dle` | +248 | n/a: one daily puzzle; a right guess ends the game (`:912`) |
| 14 | `coordinate-geometry-dash` | +247 | **WAITS**: worked solution with "Got it — next question" on both (`:357`) |
| 15 | `normal-navigator` | +246 | **WAITS**: worked solution with Next on both (`:355`) |
| 15 | `modular-battle` | +237 | advances, 1200ms (`:311`) |
| 15 | `spot-the-muppet` | +226 | **WAITS**: Next after about 1.3s (`:522`) |
| 16 | `trig-worms` | +221 | advances, about 1300ms after the shot animation (`:536`) |
| 16 | `constructions-lab` | +154 | n/a: a sandbox; nothing is marked (`:447`) |
| 16 | `circle-theorem-spotter` | +148 | advances, 1000ms. The same on a wrong answer, with no Next (`:445`) |
| 17 | `partial-fractions-duel` | +111 | advances, 1000ms. The same on a wrong answer, with no Next (`:158`) |
| 17 | `proof-builder` | +110, sideways | advances, 900–1200ms in every mode (`:432`, `:519`, `:583`) |
| 17 | `eigenvector-engine` | +109 | advances, 1000ms (`:153`) |
| 18 | `higher-power` | +87 | advances, 1800ms in Higher-or-Lower; Pairs has no per-question advance (`:591`) |
| 18 | `expectation-station` | +85 | **WAITS** at the end: stages advance at 800ms; after stage 3, Next (`:1025`) |
| 18 | `screening-room` | +57 | **WAITS**: Continue after phase 2, Next after phase 3 (`:705`, `:820`) |
| 19 | `test-the-claim` | +50 | **WAITS** at the end: steps 1–5 advance at 800ms; after step 6, Next (`:2002`) |
| 19 | `moments-master` | +10 | advances, 1000ms. The same on a wrong answer, with no Next (`:198`) |
| 19 | `trig-wars` | sideways only | n/a: artillery, no questions (`:886`) |

Line numbers are `games/<slug>/index.html` on 1 Oct 2026. Every one of the 56 appears once: 20 in group 1, 36 in group 3. Two games near the fold may not fail on a re-run (`linear-equation-solver` +26 and `moments-master` +10; the report notes such flips), which is why each game is measured in full before it is fixed.

**Seen while reading, not part of this order:** eight of the games above still run a fixed timer after a **wrong** answer with no Next (`percentage-flip`, `factor-race`, `estimation-engine`, `word-problem-decoder`, `circle-theorem-spotter`, `partial-fractions-duel`, `moments-master`, `complex-converter`'s Roulette), and `suvat`'s phase 0 and phase 2 do too. That is canon §7.6's open rollout. **Ruled 1 Oct: fixed in each game's own batch where it already has an explanation to show; otherwise §7.6 Group C, listed and left.**

**Aa mode: one fix across three games (Jon, 1 Oct 2026).** `six-sevens-bruv`, `free-daily-pizza` and `new-shapes` are each fitted to the phone rule in normal mode. Two are known to be over the fold in Aa (OpenDyslexic) mode: Six Sevens' Next at 320×568 and 375×667 (canon §7.6.1's known gap), and New Shapes' parallelogram asking screen at 320×568, 11px over (Enter at 539 against a fold of 528), because "AREA OF A PARALLELOGRAM" wraps. Free Daily Pizza has not been measured in Aa. To be fixed **once, for all three**, not game by game. All three load the shared `schools/assets/opendyslexic.css`, which makes it the candidate layer; the fix design, and measuring Free Daily Pizza in Aa, are for that contract. Canon §7.6.1's "needs its own ruling" is now ruled.

### Game ideas, not yet built (Jon, 10 Nov 2026)

Each idea is one line here and nowhere else in the repo; detail goes in its spec when it is scheduled. New builds follow SR-30 (canon §0.3). Spec references are DfE subject-content parts (`docs/resit-coverage-audit.md`). The strand's voice word is "Bruv", never "Bro". [PROPOSED] = working name not fixed.

**Resit strand games:**
- **It's Not a Diamond** [PROPOSED]: shape vocabulary and properties (G1, G4, G9.1, G12).
- **It's Just Base 60, Bruv**: time only.
- **Small, or Far Away?**: metric units, map scales, scale drawings, measuring lines and angles (N13, R2.1, G15.1). Father Ted reference in the title only: no characters, lines or look-alike art.
- **Letters? In Maffs? Y?!**: algebra basics (A1.1, A3.1, A4.1, A7.1), carrying A4.3 (expanding one bracket); each stage opens with why letters are used. Decide first whether to link to `like-terms-collector` instead of restyling it.
- **Bond. Number Bond.** [PROPOSED]: number bonds to 10/100/1000, and decimals to 1.
- **Maths Wizard** [PROPOSED]: Jon's mental strategies; each card gives the trick, why it works and where it breaks, then a drill. Undecided: whether adding by compensation (add 8 = add 10, subtract 2) goes here.
- **Don't Count the Zeroes**: standard form (STRETCH), scaffold-first with a place-value chart; `standard-form-blitz` stays the source until it is built.
- **Venn Diagrams AGAIN?**: HCF and LCM via prime-factor Venn diagrams.
- **Not in Pen**: constructing charts (drag bars, set pie angles, plot scatter points) (S2, S6).
- **Use a Ruler, PLEASE** [PROPOSED]: real-life graphs (A14.1, A14.4). Straight lines are `y-so-steep` (Jon, 27 Oct 2026).
- **It's Not 50/50** [PROPOSED]: constructing Venn diagrams and two-way tables (P6.1, P6.2). `possibly-maybe` covers the rest; `given-that` only reads them (Jon, 11 Nov 2026).

**Other games:**
- **Holey Moley** [PROPOSED]: circles (area, circumference, arcs, sectors); after the three highest-mark gap games.
- **Sine and cosine rule game**: for Jon's Level 3 class (asked 6 Nov 2026).
- **Is That a Fake Bag?**: asymptotes (Jon, 9 Nov 2026).
- **8:53**: grade 7–9 exam-prep game; deliberately outside the mission, parked as long as needed.
- **Log Laws basic level**: Log Laws is too hard for Jon's Level 3 class; research the level needed first.

**Escape rooms:**
- **IT Vengeance**: rebuild (withdrawn, awaiting its voice rewrite).
- **Food Technology** (bake-off) and **Music** (PA feedback): Gemini seeds stored.
- **Anime Society**: Mrs Rogers's idea, credited.
- **Environmental Club**: Jon's; exponential growth and decay, ratios for ppm air quality; probably 3 stars.
- **Pi Day**: idea only.

**Printables:**
- **PRINTABLES-PAGE** (Jon, 12 Nov 2026): the printables page and its "Printable games" section (Six Sevens, Bruv loop cards free; Like Terms Collector loop cards £3 on Tes) is a separate contract, waiting for the Tes links (after LOOP-CARDS-APPROVE, §6). Owner: Project Claude to write the contract; home lane.

## 4. Prevention and quality — after §1–3

1. **Checker tier 4, layer C — the answer-key tier. STILL NOT BUILT.** Trig Worms, Modular
   Battle, `es_gcse_005` and now Expectation Station all passed a green tier-1 run while shipping
   wrong maths or an uncompletable stage. A layer that recomputes each question's answer from its
   own stored parameters and asserts the stored `correct` matches would have caught all four on
   day one, including §1.7 and §1.8 above. **Layer A (static bank lint, below) shipped 26 Sep and
   is a different, narrower thing — it checks the DATA is shaped correctly, not that the MATHS is
   right.** Full five-layer design, what each catches and what none can:
   `docs/checker-tier4-design.md`.
   - **Checker tier 4, layer A — bank extraction + lint. BUILT 26 Sep.**
     `scripts/extract-banks.py` + `scripts/check-banks.py`, in CI. Every one of the 94 games is in
     `data/check-ledger.json` (83 banks read live, 1 via a static IIFE fallback, 10 confirmed
     procedural generators with no static bank at all). Ten rules, B1–B10 — see the design doc and
     the ledger for the full findings. Two real, previously-unknown defects worth a look when
     picking: `test-the-claim:538`'s `crBoundaryUpper` duplicate key, a maths content bug
     tracked at **§1.14** (B8); and §1.10 above, now three games not one (B7, redefined
     27 Sep around prose rather than space loss). CI fails only on a violation not yet in the ledger, or a
     ledger entry that no longer reproduces — everything currently in the ledger is tracked, not a
     blocker. **Not yet committed** — eight new/changed files, listed at the end of this section.
     New-game gate on layer A passing: proposed in the design doc, **Jon's ruling**, see §6.
2. **§7.6 rollout, Group B — 11 games whose explanations are already written but never shown.**
   The cheapest real quality win on the site:
   - `mc` (misconception): `characteristic-quest`, `dimension-checker`, `eigenvalue-extractor`,
     `eigenvector-engine`, `scale-factor-scaling`, `unit-converter`
   - `steps`: `angle-ace`, `matrix-crunch`, `proof-builder`
   - `hint` + `steps`: `formula-forge`, `formula-unlocked`

   Surface it on the wrong path, *then* add `MaffsNext.wrong(...)`. Do not add the button first —
   canon §7.6 forbids a pause with nothing to read.
   - **§7.6 Group C — 6 games with no explanation data at all** (`equation-builder`, `factor-race`,
     `simultaneous-solver` show a bare "WRONG!"; `estimation-engine`, `fraction-equivalence`,
     `quadratic-factoriser` construct the answer but never the why) is **Jon's call** — author
     explanations, or accept answer-only and leave these on a timer. See §6.
   - **Does §7.6 want a floor as well as a button?** `probability-pioneer` already enforces a 5s
     minimum before its next button will act. If Jon likes it, it's one change to
     `next-control.js`, applying platform-wide. `linear-equation-solver` hand-rolled the pattern
     before §7.6 existed; both left alone for now. **Jon's call** — see §6.
3. **KaTeX §7.1.1 rollout — 16 of 17 games still to do.** `suvat` is the reference
   implementation. Three sub-classes:
   - **A — loads KaTeX, never calls it:** `coordinate-geometry-dash` (worst case — it even styles
     `.katex` selectors that can never match), `normal-navigator`, `probability-paradox`,
     `unit-converter`
   - **B — no KaTeX at all:** `scale-factor-scaling`, `estimation-golf`*, `estimation-engine`*,
     `52dle`, `prime-or-composite`, `fraction-equivalence`, `trig-worms`, `trig-wars`
   - **C — KaTeX for options, raw text for the explanation:** `differentiation-duel`,
     `integration-duel`, `index-laws`, `proof-builder`

   \* re-check against §7.1.1's narrower scope first — some instances may be units.
   One game at a time, each played. Never a sweep — `96381d74`, `76514c70`, `4b3d7d3` are why.
   `suvat`'s own Group C debt (58 `working:` strings still raw Unicode) is deliberately not done
   in the same pass as its KaTeX work.
4. **The `4b3d7d3` timer audit — still open from 21 Sep.** Seven files unaudited against
   `.claude/rules/timer-policy.md`: `complex-converter`, `integration-duel`, `log-laws`, `suvat`,
   `trig-identity-duel`, `schools/index.html`, `schools/spec-map/index.html`. All pass tier 1;
   timer policy is play-time behaviour and tier 1 is structurally blind to it. Note `suvat`,
   `integration-duel` and `log-laws` were edited and played on 22 Sep, but for KaTeX/theme/advance,
   not timer policy.
5. **Tier-3 UNSUPPORTED ledger — 35 of 42 games still to read.** Groundwork for tier 4. An entry
   in `checker-allowlist.json`'s `tier3_exceptions` is a claim you've read the game, so it was not
   bulk-filled from the run; 7 read so far.
   - Related: four games use rejection sampling safe only because their banks are big enough
     (`complex-converter`, `gradient-hunter`, `maths-court`, `negative-number-line`) — no present
     bug, deliberately left alone, but a content edit could trip any of them.
   - Rule worth writing into CLAUDE.md: never mark by re-parsing a displayed value — tile identity
     belongs in `dataset.val` or a closure. Whether other games do this is unaudited.
6. **Archive CLAUDE.md's "Previous state" sections into `docs/history.md`.** Every session
   currently loads ~860 lines of CLAUDE.md, most of it history rather than current state. Cuts
   the per-session cost without losing the record.
7. **A shared calculator widget — Jon's idea, unscoped.** Students without a scientific calculator
   cannot play the trig games at all. Agreed shape: shared `schools/assets/` widget, opt-in per
   game, visible DEG/RAD indicator (radian-mode error is the most common real trig failure).
   Needs a "which games actually require one" scan first.
9. **PQ(s) routing is duplicated in `component-crusher:524`, `factor-theorem:262`,
   `test-the-claim:1159`** — move into `MaffsText.auto(s)` before a fourth game copies it.
11. **B3's reach (found 2 Oct, during item 7; not judged).** (a) The ledgered `moments-master` B3
   pair, alevel[18] and [29], is two different questions (a 6 m uniform beam and a 10 m non-uniform
   beam). Each shares the 33-character label `\text{Moments about left support}` and the answer 75 N,
   which is all B3's signature compares; the other three B3 entries may be the same. (b) B3 cannot see
   `wrong-on-the-internet`: `bank_common.question_text()` returns `None` for its questions (their text
   is under `post.text`), so a copy-pasted question there raises nothing. **Jon's call** whether to
   re-judge the four entries and widen `TEXT_KEYS`.
12. ~~**Tier 1 loads `index.html` files only (found 2 Oct, §1.33).** `check-site.py`'s
   `build_page_list()` globs `games/*/index.html`, `escape-rooms/*/{index,teacher}.html` and every
   other `index.html` via `discover_pages()`, so a served page with any other name is never loaded.
   Two exist today: `games/sequence-solver/index-original.html` (a redirect stub since PR 58, proved
   once by hand: lands on the game, no error) and `games/regression-rumble/_withdrawn.html` (the
   withdrawn game, never loaded by tier 1 since it was moved there on 30 Sep). Jon ruled 2 Oct not to
   widen discovery in the §1.33 PR. **Fix, its own contract:** discover every served `.html`, not just
   `index.html`, and decide whether `_withdrawn.html` should then load on every push.~~ **DONE 2 Oct 2026 (PR 62):** `jekyll_serves()` decides what is served, and tier 1 loads every such `.html`; `_withdrawn.html` is not served, so it is not loaded. The `--live` confirmation is still owed (see the START block).
13. **B7 cannot see generator-built strings; candidate: a runtime KaTeX hook layer** (Jon's ruling,
   2 Oct 2026, with §1.31). Sites whose strings only a generator builds as the game runs are listed
   by `check-banks.py --ci` as `runtime-only`, never checked: log-laws' Solve mode (11 sites: `MT`
   :1811 :1844, `addLine` :1813 :1828 :1891 :1901, `setMsg` :1839 :1892 :1905, `K` :1846 :1859),
   quadratic-factoriser (24), free-daily-pizza (6), graph-transformer (2). The audit's runtime hook
   (`scripts/audit-katex/kx_hook.js`, driven by tier 3) is the prototype: it saw 4,104 strings in
   play, none of them a defect in these four games, three of which route mixed text through
   `MaffsText`. Not scheduled.
14. **Self-host Outfit; then switch the phone gate to measure in Outfit** (Jon, 2 Oct 2026).
   `parents/fractions` is +1px in Outfit and is hidden by fallback measurement, and 12 of the 44
   recorded overflows fit in Outfit. The gate blocks Google's fonts so its verdict is the same every
   run; it therefore measures a font no student sees (the same known gap as the verifiers' holding step,
   `.github/workflows/check-site.yml`). The real fix is one contract: serve Outfit and KaTeX from the
   repo, measure in Outfit with a minimum margin, then re-record `tier1_phone_overflow`.
15. **Teach tier 1's start driver four games** (found 2 Oct, PR 62): `factor-theorem` (starts on the
   Practice/Test tab), `six-sevens-bruv` (needs a grid made first), `trig-worms` (button reads "FIRE!")
   and `test-the-claim` (needs mode, tail and significance chosen). Until then their post-start width
   is not gated. Do it by behaviour, not a per-game list, and in the same driver tier 3 and
   `measure-phone-fit.py` use.
16. ~~**The tier 1 phone gate measures one random draw, so any game that randomises its first question
   can flip between runs**~~ **DONE 3 Oct 2026 (§4 item 16's PR): the phone pass is seeded.** `PHONE_SEED` in
   `check-site.py` replaces `Math.random` before any page script with mulberry32 seeded by the FNV-1a
   hash of the page's `location.pathname`: one fixed seed per page (the contract's choice), not the set
   of seeds planned below, so the gate measures one stable draw, not a game's worst question; a game
   whose width depends on the draw is swept on its own and recorded (`moments-master`, §1.40). Seeding
   broke no game and revealed no new overflow. `--phone-widths FILE` dumps every measurement; repeated
   runs gave identical files. No retry logic anywhere. `measure-phone-fit.py` is not seeded (a report,
   not a gate). Original entry: (found 2 Oct 2026 via §1.40: `moments-master` failed one CI run and passed
   the next on the same commit). Under the zero-failures merge rule a flaky gate blocks every merge, so
   **Jon ordered this ahead of everything else (2 Oct 2026), the §4 "after §1–2" rule notwithstanding.**
   **Fix at the gate:** seed `Math.random` in the page during the phone measurement, over a fixed set
   of seeds, and take the widest result, so every run measures the same thing and a game is held to its
   worst question. Then re-run on `main` and record any game whose recorded width changes (and any new
   overflow, `moments-master` among them: §1.40's entry lands in this PR). Check the pass time against
   the job's timeout, and whether `measure-phone-fit.py` (same driver) should take the same seeds.

17. **Four check scripts are never run in CI** (found 3 Oct 2026): `check-escape-rooms.py`,
   `check-lock-uniqueness.py` and `check-feedback-options.py` pass locally; `check-lock-bank.py` takes a
   bank file and passes batches 4–7. Batch 3 rejects `hamster-feeder-bounds`, whose VERIFY in
   `docs/lock-bank-batch3.txt` is a syntax error: that file is a stale record (the live room was
   corrected 8 Sep, `docs/escape-puzzle-bank.md`; a header note now says so). `check-verifier-coverage.py`
   only polices `verify-*`/`test-*`, so it did not catch them. **Fix:** add the three to a CI group, run
   `check-lock-bank.py` over the batches that are still the record (or retire the batch files), and
   widen the coverage check to `check-*`. S.
18. **CI Contract B: triggers, concurrency and local/CI parity** (named "CI Contract B" to keep it apart
   from Chart Interrogator's 28 Sep "Contract B"; first recorded here 3 Oct 2026). `check-site.yml` runs on
   `push` to every branch and on `pull_request`, with no `concurrency` group, so every PR commit runs
   the whole suite twice (PR #3 and #4 each show every job twice). Parity gaps that make local runs
   disagree with CI: CRLF checkouts (`verify-test-the-claim.py`'s node driver), `node` not on PATH on
   Windows (Playwright's bundled node works), and the Windows fallback font (14 "stale: now fits" phone
   entries locally, 0 in CI). Jon adds branch protection after it (none today: API 404, 0 rulesets). M.
   **Triggers and concurrency DONE 4 Oct 2026 (selective CI, canon §7.8):** push on main only, a PR's new
   push cancels its running checks, and a `gate` job for branch protection to require. **Parity still open
   (Windows-only local failures, for a later tidy-up; `check-changed.py` avoids the first by not running
   tier 1 locally):** (a) tier 1's 13 "stale: now fits" phone entries, from the fallback font; (b)
   `verify-test-the-claim.py` fails locally with `ReferenceError: generateWrongContexts is not defined`
   under Playwright's node v24 (it passes in CI; CRLF checkouts are the suspected cause, above); (c) node
   is not on PATH on Windows (Playwright's bundled node works; `check-changed.py` does not need it unless
   Test the Claim is selected); (d) the shared calculator check (`test-calculator-js.py`, "Shared on-screen
   calculator") was reported on 12 Oct as failing locally on every run. **Not reproduced 13 Oct 2026:** it passes
   here, alone and inside `check-changed.py`. Its only environment-dependent path is the answer-box check, which
   needs Playwright's WebKit (`python -m playwright install webkit`) and says so when it is missing ("WebKit would
   not start", line 460); an earlier sandbox without WebKit failed it the same way. Nothing in the harness to fix;
   if it fails locally, install WebKit first. (e) Under `check-changed.py`'s parallel load, Chromium sometimes
   crashes in the answer-lock parts and `verify-characteristic-quest.py` ("Page crashed", "Target page, context or
   browser has been closed", 13 Oct); a re-run or CI passes.
19. **CI flake: tier 4 lint reported B4 "level bank below 40" for `proportion-blaster::gcse`** in one of
   two identical runs of PR #36 (same commit; the other passed, as did a re-run). Locally the extraction
   reads 50 GCSE items and the game never mutates its bank, so the extraction or its grouping is
   intermittently short. Not investigated further (outside that PR). S.
20. **GATE-STEP-4: repeatable gating checks** (step 4 of GATE-WARN-THEN-ENFORCE). The stub server injects a fixed default seed; verifiers keep fixed seed lists; a nightly, non-gating random sweep adds each failing seed to its list; ~~Take a Walk's `Date.now` seed is fixed~~ DONE 12 Nov 2026 (TAKE-A-WALK-SEED): no game's seed reads the clock (take-a-walk, how-many-parts, just-pythag-it-bruv, squared-squirrel), and check-site.py tier 2's clock-seed scan keeps it so (allow-list: equatle's and free-daily-pizza's daily seeds; Jon's option A); every page measurement waits on `bc.wait_settled`, `measure-phone-fit.py` included. Spec, Jon's ruling and the audit of about 45 sites: `docs/handover/contracts/2026-10-27-gate-step4-spec.md`. Moved from cloud.md's live pointers. **Still owed, added 12 Nov 2026 (Jon, option 1 of TAKE-A-WALK-SEED): phone-fit measures only the first asking screen in every game; answer and later screens are unmeasured.** A shared-infrastructure gap, not Take a Walk's (`measure-phone-fit.py` stops at the first screen with answer controls; Take a Walk's answer screen overflowed by up to 272 px unseen, row TAKE-A-WALK-PHONE-LAYOUT). Owner: cloud lane (gate files).
21. **GATE-STEP-6: the shard migration** (step 6 of GATE-WARN-THEN-ENFORCE, `docs/handover/contracts/2026-10-27-gate-warn-then-enforce.md`; steps 1, 2, 3 and 5 merged as #590, #630, #592 and #631). Step 6 supersedes PLAN-SHARED-ASSETS (`docs/history/contracts/2026-10-27-plan-shared-assets.md`). The warn list is empty; moving Factor Theorem (88 s), Growth and Decay (123 s) and Screening Room (94 s) to work units is insurance only. Moved from cloud.md's live pointers. Owner: **Jon** to say; cloud lane.
22. **PROBE-DATA-OPT** (PHONE-FIT-RED follow-up): the phone-fit checker should see `[data-opt]` delegated buttons, with `possibly-maybe`'s unmeasurable entry coming off; the sideways check should run on every game, unmeasurable ones included; diagnose "asking only" on `hc-factor`, `y-so-steep`, `i-found-a-mark` and `who-ate-all-the-pies` (`y-so-steep` and `i-found-a-mark` have no `[data-opt]`). Owner: home lane.
23. **LOCAL-CHECKS**: browser verifiers fail intermittently in WSL `maffs`, on clean main too. Leading lead, untested: WSL's clock stepping backwards, up to 2.884 s in 40 s. Local runs measure `screening-room` 717/680 while CI passes it; CI is the authority (AGENTS.md). Owner: home lane. Re-checked 2026-11-08: CI's nightly now reproduces screening-room 717/680 (see SCREENING-ROOM-FOLD), so that case is not local-only. teacher-feedback-line fails locally on prisoners-dilemma's tournament at 390 px; passes in CI. 9 Nov: verifiers of squared-squirrel, its-on-sale, estimation-engine, the-6-ps and the Burst, Chart drawings and two Feedback-that-teaches checks fail locally on clean main; pass in CI (#719).
24. **AA-AUDIT**: font-family overrides that bypass OpenDyslexic; HUD label overlap at 375; Aa `line-height` never below 1.5 (`distinctly-average` sets 1.4). Owner: home lane (shared Aa styles); per-game fixes cloud lane.
25. **VARIANT-EFFORT**: no check that a lock's variants take similar effort (COMIC-CAPER-PRIME-LOCK, §3, is the case in hand). Owner: home lane.
26. **LEVEL-CODES**: the portal's level code `l4` against the games' `level4` (one game's `l4` key is noted in §2). Owner: home lane.
27. **MERGE-PR-VERDICT**: `merge-pr.py --watch` sometimes exits without its final line; find out too why `merge-pr.py` works in some cloud sessions and not others. Owner: cloud lane (gate file).
28. **MERGE-PR-GRACE** (Low; Jon, 2 Nov, after GATE-FIX): `merge-pr.py` counts "the newest merge has no run of its own" as red even under `--wait`, so in the seconds before GitHub registers a new merge's run it refuses ("start one by hand") instead of waiting. Fix: count it as unfinished for a short grace period (about 5 minutes after the commit), with a plant. Moved from cloud.md's live pointers. Owner: cloud lane (gate file).
29. **CI-DEPS-TOOLS** (PACK-GENERATOR, Amendment 2): `tools` is not in `scripts/ci-deps.py` KNOWN_TOP, so a `tools/` change selects every verifier. Moved from cloud.md's live pointers. Owner: Project Claude to triage; cloud lane (gate file).
30. **PACK-FITTER**: a "no fit down to 1 pt" failure mode for the pack fitter. Owner: home lane (`tools/pack-generator/`).
31. **CHECK-BANKS-ESCAPE** (Jon, 2 Nov): `scripts/check-banks.py:25` has an invalid escape `\(` (`ci-deps.py`'s `ast.parse` warns on Python 3.12+). Harmless. Moved from cloud.md's live pointers. Owner: home lane.
32. **PHONE-FIT-DRIVER-RULINGS**: PHONE-FIT-DRIVER's two rulings, the 11-game exception and a start-screen rule, are Jon's (a live tail of the Queue DONE items moved 4 Nov, `docs/history/handover-cloud-archive.md`). Moved from cloud.md's Queue 8 Nov (BRANCH-CLEANUP). Owner: Jon.
33. **SIX-PS-PHONE-FIT**: The 6 P's in the phone-fit gate, a driver change (item 3 of the cloud lane's 27 Oct session queue); `/the-6-ps/` is not in the nightly phone-fit run. Parked (Jon, 3 Nov). Moved from cloud.md's Queue 8 Nov (BRANCH-CLEANUP). Owner: cloud lane.
34. **MODE-DIMENSION**: the mode dimension ("item D", item 6 of the 27 Oct session queue): no contract text found in the repo; ask Jon. Parked (Jon, 3 Nov). Moved from cloud.md's Queue 8 Nov (BRANCH-CLEANUP). Owner: Jon, then cloud lane.
35. **START-SCREEN-RULE**: the start-screen rule, only once a shared compact start screen exists, else write up what it needs and stop (item 8 of the 27 Oct session queue; Jon's ruling is in PHONE-FIT-DRIVER-RULINGS). Parked (Jon, 3 Nov). Moved from cloud.md's Queue 8 Nov (BRANCH-CLEANUP). Owner: cloud lane.
36. **REPORT-EMAIL-PROPERTY**: `docs/apps-script-endpoint.js:15` ships `REPORT_EMAIL = 'OWNER_EMAIL_HERE'`; on 4 Nov a manual `sendDailyReport` failed "Invalid email: OWNER_EMAIL_HERE" because the pasted endpoint kept the placeholder (record: branch `claude/stoic-galileo-xvzt45`, which stays). Proposal: read the address from Script Properties, so the public repo never holds it and a redeploy cannot break the report. BRANCH-CLEANUP Amendment 1, 8 Nov. Owner: home lane (endpoint file); Jon sets the property and redeploys.
37. **PHONE-FIT-CHECKER**: `scripts/measure-phone-fit.py` (a) `settle()`'s 5 s ceiling false-passes controls shown at about 5 s (screening-room); (b) it measures one seeded question per game, against canon §7.6.1's "every question shape"; (c) `--aa` never switches Aa on in games that read a non-standard saved setting (probability-pioneer, shape-shifter, like-terms-collector); (d) it gave three verdicts on the same code (717 FAIL, "no Next", PASS). Also audit every entry #707 removed as "stale". Recorded 9 Nov 2026 (DOCS-BUNDLE). Owner: home lane, its own contract.
38. **PHONE-FIT-PR-COVERAGE**: only the nightly full run measures laptop mode; a push touching one game's page skips the full measure. Recorded 9 Nov 2026 (DOCS-BUNDLE). Owner: cloud lane (gate files).
39. **LEDGER-LINE-DRIFT**: `data/check-ledger.json`'s `line` fields go stale on every game edit (on 9 Nov maths-court's two B6 entries said 444 and 516; the strings are at 461 and 533). Stop recording or comparing them. Recorded 9 Nov 2026 (DOCS-BUNDLE). Owner: home lane (`scripts/check-banks.py`).
40. **CLOUD-MERGE-TOKEN** — some cloud sessions get an invalid GH_TOKEN, so merge-pr.py (the only permitted merge route, AGENTS.md) refuses and the lane needs a ruling (#721, #722, 10 Nov 2026). Find why the token differs between sessions and fix it, or give merge-pr.py a second transport with the same checks; then retire the standing ruling of 10 Nov. Deadline: before Tue 24 Nov 2026, when that ruling lapses. If the token comes from the cloud environment's settings, the fix is Jon's: say so on this row. (Project Claude, 10 Nov 2026.) Owner: home lane.
41. **TEST-ESCAPE-RATING-UNHIDE** — scripts/test-escape-rating.py still hides the teacher tables before measuring; since #721 they scroll in their own box, so the hiding can go. (Code Claude, #722, 10 Nov 2026.) Owner: home lane.
42. **ROSTER-CELLS** — a roster Description containing '|' splits its table row (#723 wrote '|k| > 1', found at listing by #724); the look sign-off check skips Unlisted rows, so the fault hid there. Add a check that every roster row in every section, Unlisted included, has the header's cell count. (Project Claude, 10 Nov 2026.) Owner: home lane.
43. **PREVIOUS-SCORE-COLUMN** — the Sheets endpoint reads data.previous_score (docs/apps-script-endpoint.js:21, :59) but every game sends previous_best, the documented field (.claude/rules/analytics.md:22), so the Sheet's previous_score column has always been blank; GA4 is unaffected. Fix it in the endpoint (read previous_best; keep the column header as is or rename it, say which), then Jon redeploys the live Apps Script. Found while closing 1.25 (Code Claude, HOME-DOCS-1110, 10 Nov 2026). Owner: home lane (endpoint), then Jon (redeploys the live Apps Script).
44. **STALE-PLANTS-STOP** — Stop a planted browser run at its first measured finding (Jon, 28 Oct 2026; STALE-PLANTS). Done in `verify-just-pythag-it-bruv.py` (`phone_fit`: `patch and len(out) > n0` checkpoints), because a fault that breaks the page makes the steps after it time out, and a timeout must never read as a catch. Not yet applied to the other verifiers that run a planted fault through an interactive session: `verify-decimal-detective.py`, `verify-free-daily-pizza.py` (both patch a live page; check whether a caught fault is followed by a step that can time out); neither has the checkpoint on 11 Nov 2026. `plant_common.py` does not run plants, so the rule lives in each verifier's loop. Moved from §6 (TODO-TIDY). Owner: cloud lane (per-game verifiers).
45. **PLAN-MAP-ONCE** (cloud lane, after 2 Nov). `ci-deps.py` builds the dependency map once per Plan job, used by both `--selftest` and `--changed-from`; then the Plan timeout in `.github/workflows/check-site.yml` goes back to 5 in the same PR (it is 10 under Jon's freeze exception of 29 Oct 2026, a stopgap; still 10 at `:70` on 11 Nov 2026). Evidence: #614 cancelled 5x, run 40820873132. Moved from §6 (TODO-TIDY). Owner: cloud lane (gate files).
46. **ESCAPE-COUNT-SOURCE** (after 2 Nov): one source for the live escape-room count and roster; index.html and escape-rooms/index.html read from it or a CI check compares them; the check proved by a planted mismatch. Moved from §6 (TODO-TIDY). Owner: home lane.
47. **PE-SHED-VARIANT-0** — `pe-shed-rebellion` variant 0 collision (48 psi vs "48π"; 12 m vs "day 12"). **RULED 29 Sep 2026 (Jon): fix it.** Change the audited bank locks per voice-rewrite doc §5h, even though the engine never currently serves variant 0 — latent, not worth leaving. Not built: `scripts/check-escape-rooms.py` still reports `pe-shed-rebellion` "variant 0 INVALID" on 11 Nov 2026. Moved from §6 (TODO-TIDY). Owner: home lane (bank and generator).
48. **NEW-GAME-GATE** — block merging a new game until it passes tier 4 layer A. **RULED 29 Sep 2026 (Jon): adopt the gate.** Layers B–E stay advisory until built. Half there on 11 Nov 2026: layer A runs on every PR (`check-banks.py --ci`, `check-site.yml:530`) and fails any violation not in the ledger, and a merge needs a green Gate (merge-pr.py's check (a); the standing merge-route ruling). Missing: an unreadable bank passes as a generator without declaring itself one (`extract-banks.py:519` records it `generator: True`; `check-banks.py --ci` fails a lost bank only when the ledger already knows it as read, `:1268`). Add the declaration requirement: a new game extracts a static bank or is declared a generator, or CI fails. `docs/checker-tier4-design.md:139` still says "awaiting Jon's ruling" (not edited here). Moved from §6 (TODO-TIDY; Jon's ruling 2 of 11 Nov 2026). Owner: home lane (`scripts/extract-banks.py`, `scripts/check-banks.py`).
49. **GROUP-C-EXPLANATIONS** — §7.6 Group C. **RULED 29 Sep 2026 (Jon): author real explanations** for all 6 (`equation-builder`, `factor-race`, `simultaneous-solver`, `estimation-engine`, `fraction-equivalence`, `quadratic-factoriser`). Four are still answer-only (Jon, 11 Nov 2026): `simultaneous-solver` A-Level (`:1274`, "The answer is …"), `equation-builder` (`:657`, the key only), `factor-race` (`:398`, the two factor counts) and Fraction Snap (`fraction-equivalence:360`, one cross-multiplication line). `estimation-engine`, `quadratic-factoriser` and Simultaneous Solver's Foundation stages show the working. Moved from §6 (TODO-TIDY; Jon's ruling 3 of 11 Nov 2026). Owner: cloud lane (per-game).
50. **AA-KEY-MISMATCH**: probability-pioneer, shape-shifter and like-terms-collector read only mfg_dyslexia; measure-phone-fit.py --aa sets mfg_accessible, so the Gate never measures their Aa mode. Fix at the measuring layer or the games' key. Owner: cloud lane (Gate files). Recorded 12 Nov 2026 (contract PP-AA-STACK).

### Check-ledger debt (DOCS-BUNDLE, 9 Nov 2026)

One row per failing rule-and-game group in `data/check-ledger.json` (B6 is one row: one fix across games), 167 entries in 43 games on 9 Nov 2026; none is a wrong answer a student can see. What each rule checks, the counts and an example entry per group: `docs/audits/ledger-debt-2026-11.md`. A fix PR that clears a group's entries updates or closes its row.

| # | Item | Owner |
|---|---|---|
| LEDGER-B4-52DLE | **B4 ledger debt, `52dle`: 2 levels below the 40-question minimum** (ks3 20, gcse 20). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-ANGLE-ACE | **B4 ledger debt, `angle-ace`: 1 level below the 40-question minimum** (gcse 35). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-BETTER-VALUE | **B4 ledger debt, `better-value`: 1 level below the 40-question minimum** (gcse 20). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-CHARACTERISTIC-QUEST | **B4 ledger debt, `characteristic-quest`: 2 levels below the 40-question minimum** (further 26, level4 26). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-COMPONENT-CRUSHER | **B4 ledger debt, `component-crusher`: 3 levels below the 40-question minimum** (gcse 15, alevel 15, level4 15). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-CONSTRUCTIONS-LAB | **B4 ledger debt, `constructions-lab`: 2 levels below the 40-question minimum** (ks3 10, gcse 10). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-CORE-MATHS-PAPER1 | **B4 ledger debt, `core-maths-paper1`: 1 level below the 40-question minimum** (core 36). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-CORE-MATHS-PAPER2A | **B4 ledger debt, `core-maths-paper2a`: 1 level below the 40-question minimum** (core 36). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-CORE-MATHS-PAPER2B | **B4 ledger debt, `core-maths-paper2b`: 1 level below the 40-question minimum** (core 36). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-CORE-MATHS-PAPER2C | **B4 ledger debt, `core-maths-paper2c`: 1 level below the 40-question minimum** (core 36). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-CURLING-FRICTION | **B4 ledger debt, `curling-friction`: 1 level below the 40-question minimum** (level4 20). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-DIMENSION-CHECKER | **B4 ledger debt, `dimension-checker`: 1 level below the 40-question minimum** (level4 28). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-EIGENVALUE-EXTRACTOR | **B4 ledger debt, `eigenvalue-extractor`: 2 levels below the 40-question minimum** (further 25, level4 25). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-EIGENVECTOR-ENGINE | **B4 ledger debt, `eigenvector-engine`: 2 levels below the 40-question minimum** (further 25, level4 25). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-ESTIMATION-GOLF | **B4 ledger debt, `estimation-golf`: 5 levels below the 40-question minimum** (year6 20, ks3 9, gcse 9, alevel 9, level4 9). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-EXPECTED-DAMAGE | **B4 ledger debt, `expected-damage`: 3 levels below the 40-question minimum** (ks3 15, gcse 20, core 15). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-FACTOR-RACE | **B4 ledger debt, `factor-race`: 2 levels below the 40-question minimum** (year6 20, ks3 20). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-FERMI-LAB | **B4 ledger debt, `fermi-lab`: 5 levels below the 40-question minimum** (ks3 12, gcse 15, alevel 13, level4 10, core 15). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-FORCE-RESOLVER | **B4 ledger debt, `force-resolver`: 1 level below the 40-question minimum** (level4 20). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-FORMULA-FORGE | **B4 ledger debt, `formula-forge`: 3 levels below the 40-question minimum** (gcse 29, alevel 29, level4 16). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-FRACTION-EQUIVALENCE | **B4 ledger debt, `fraction-equivalence`: 3 levels below the 40-question minimum** (year6 20, ks3 20, gcse 20). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-GIVEN-THAT | **B4 ledger debt, `given-that`: 4 levels below the 40-question minimum** (gcse 25, alevel 25, core 20, level4 20). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-GLORIOUS-GANTT | **B4 ledger debt, `glorious-gantt`: 2 levels below the 40-question minimum** (core 15, level4 15). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-GRADIENT-HUNTER | **B4 ledger debt, `gradient-hunter`: 3 levels below the 40-question minimum** (gcse 15, core 20, alevel 10). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-GRAPH-SKETCHER | **B4 ledger debt, `graph-sketcher`: 3 levels below the 40-question minimum** (core 15, alevel 15, level4 15). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-GROWTH-AND-DECAY | **B4 ledger debt, `growth-and-decay`: 3 levels below the 40-question minimum** (core 15, alevel 15, level4 15). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-MATHS-COURT | **B4 ledger debt, `maths-court`: 3 levels below the 40-question minimum** (ks3 15, gcse 20, core 10). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-MATRIX-CRUNCH | **B4 ledger debt, `matrix-crunch`: 2 levels below the 40-question minimum** (further 35, level4 18). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-MOMENTS-MASTER | **B4 ledger debt, `moments-master`: 1 level below the 40-question minimum** (level4 20). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-NEGATIVE-NUMBER-LINE | **B4 ledger debt, `negative-number-line`: 1 level below the 40-question minimum** (year6 30). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-PERCENTAGE-FLIP | **B4 ledger debt, `percentage-flip`: 3 levels below the 40-question minimum** (year6 32, ks3 32, gcse 32). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-PRISONERS-DILEMMA | **B4 ledger debt, `prisoners-dilemma`: 4 levels below the 40-question minimum** (ks3 9, gcse 9, alevel 9, core 9). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-PROBABILITY-PARADOX | **B4 ledger debt, `probability-paradox`: 2 levels below the 40-question minimum** (gcse 38, core 38). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-PROOF-BUILDER | **B4 ledger debt, `proof-builder`: 2 levels below the 40-question minimum** (alevel 33, further 10). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-REGRESSION-RUMBLE | **B4 ledger debt, `regression-rumble`: 3 levels below the 40-question minimum** (core 12, alevel 14, level4 14). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-SCREENING-ROOM | **B4 ledger debt, `screening-room`: 4 levels below the 40-question minimum** (gcse 20, alevel 20, core 15, level4 15). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-SEVEN-BRIDGES | **B4 ledger debt, `seven-bridges`: 3 levels below the 40-question minimum** (ks3 25, gcse 25, alevel 25). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-STAT-ATTACK | **B4 ledger debt, `stat-attack`: 3 levels below the 40-question minimum** (gcse 12, core 12, level4 12). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-TERRIBLE-ADVICE | **B4 ledger debt, `terrible-advice`: 3 levels below the 40-question minimum** (ks3 18, gcse 20, core 12). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-TRUTH-WILL-SET-YOU-FREE | **B4 ledger debt, `truth-will-set-you-free`: 1 level below the 40-question minimum** (level4 32). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B4-WRONG-ON-THE-INTERNET | **B4 ledger debt, `wrong-on-the-internet`: 3 levels below the 40-question minimum** (ks3 15, gcse 20, core 10). Survey: `docs/audits/ledger-debt-2026-11.md` §B4. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B7-CHARACTERISTIC-QUEST | **B7 ledger debt, `characteristic-quest`: 7 rendered strings lose their spaces.** Survey: `docs/audits/ledger-debt-2026-11.md` §B7. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B7-EIGENVALUE-EXTRACTOR | **B7 ledger debt, `eigenvalue-extractor`: 6 rendered strings lose their spaces.** Survey: `docs/audits/ledger-debt-2026-11.md` §B7. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B7-EQUATION-BUILDER | **B7 ledger debt, `equation-builder`: 1 rendered string lose their spaces.** Survey: `docs/audits/ledger-debt-2026-11.md` §B7. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B7-MATRIX-CRUNCH | **B7 ledger debt, `matrix-crunch`: 30 rendered strings lose their spaces.** Survey: `docs/audits/ledger-debt-2026-11.md` §B7. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B6 | **B6 ledger debt: 18 draft-marker hits in 6 games, none a wrong answer** (`expected-damage` 2, `maths-court` 2, `probability-paradox` 5, `terrible-advice` 4, `test-the-claim` 1, `wrong-on-the-internet` 4). One fix across games: let the rule accept deliberate character voice and ordinary uses of "wait", then retire the entries. Survey: `docs/audits/ledger-debt-2026-11.md` §B6. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B3-ANGLE-ACE | **B3 ledger debt, `angle-ace`: 7 duplicate questions.** Survey: `docs/audits/ledger-debt-2026-11.md` §B3. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |
| LEDGER-B3-MOMENTS-MASTER | **B3 ledger debt, `moments-master`: 1 duplicate question.** Possibly a false match: see §4 item 11. Survey: `docs/audits/ledger-debt-2026-11.md` §B3. Recorded 9 Nov 2026 (DOCS-BUNDLE). | cloud lane |


## 5. Parked, deliberately

- `MaffsOptions.build()` retrofit (~29 games hand-rolling option assembly), for a down-time
  window only (canon §8.2c) — not a platform sweep.
- Shared calculator widget — see §4.7, parked until scoped.
- Matrix Crunch bank expansion to 50+50.
- Expectation Station bank growth to the 40–50 platform minimum (core 20, GCSE 15, A-level 10
  today) — content depth, not code. See 1.11.
- Bank growth for 1.13's four over-promising games — content depth, not code. All below the
  40–50 platform minimum, and all resit-audience games: `wrong-on-the-internet` core 10 /
  ks3 15 / gcse 20; `spot-the-muppet` core 12 / ks3 18 / gcse 20; `expected-damage` ks3 15 /
  core 15 / gcse 20; `better-value` gcse 20.
- Escape rooms: the Car Trap voice rewrite (it needs a premise/image conversation
  first), rooms A and B.
- Certificates (Phase 1b), teacher portal (Phase 2).

## 6. Jon — decisions and manual tasks

Only what needs Jon: a ruling, a content review, or a task only he can do. Build work goes in §1–§4 and §7 whoever ruled it; a ruled item moves there the day it is ruled.

**Decisions:**
- None open (11 Nov 2026: matrix-crunch's fourth distractor, §1.4, ruled by Jon on 10 Nov and closed by CLOUD-QUEUE-1111 PR 1).

**Content to review:**
- **LOOP-CARDS-APPROVE** (12 Nov 2026): approve both loop-card packs' teacher wording (proofs `docs/screens/loop-cards/*-teacher1.png`) (the PR's three layout calls were approved by Jon on 12 Nov). **Six Sevens' cards changed (SIX-SEVENS-WEIGHTING, 13 Nov 2026):** the 16 and 24 decks are only 6, 7, 8, 9 and 12-table facts with no 11s and no 2s, the 32 deck all 25 of those plus 7 from the 3, 4, 5 and 11 tables, and the build checks it; Jon proofreads the new Six Sevens PDF (`python -X utf8 tools/loop-cards/build_deck.py six-sevens-bruv`) before approving. Approval goes in `tools/loop-cards/decks/<slug>/config.json` "wording_approved"; then `--final` builds go to Tes (Like Terms Collector £3; Six Sevens, Bruv free). Owner: Jon, then home lane.
- Spot the Error banks (§1.23): KS3 35, Level 4 30.
- New Shapes banks (§1.27): 15 / 20 / 15.
- Regression Rumble (§1.26): Jon's look at the rebuilt game before the holding page is replaced.

**Manual tasks:**
- Spec-map spot-check (blocks §3.1): 10 of the 34 mixed statements in `data/dfe-gcse-parts.json` against the PDF.
- Analytics checkpoint (overdue): re-answer the open questions in the project's `analytics-notes.md`. From 10 Nov 2026 GA4 excludes Jon's home IPv4 and IPv6 /56 (filter Version 3), so figures step down from that date: compare like with like.
- Events sheet: confirm no `game_abandoned` against the homepage, 1–15 Sep.
- Events sheet (optional): `binomial-blaster` `game_completed`, score 400, about 17:16 UTC 16 Sep; if present, the deleted Firebase score was real and can be restored.

## 7. Housekeeping

- Canon §4 still says 93 games; the roster (94, exactly `games/` minus `the-perfect-prank`) is
  correct. Jon's ruling: noted, leave it, separate fix.
- **`MAFFSGAMES_PROJECT_INSTRUCTIONS.md` is not in this repo** — it exists only in Claude Project
  knowledge and reports stale from there (still names the repo `QF-Games`; its "Current Backlog"
  was shipped months ago). Recommend moving it into the repo so it has one source of truth, or
  accept it must be hand-synced. Replace its backlog section with a pointer to this file.
- The project's own copies of `canon.md` and `CLAUDE.md` lag the repo. Refresh them, or delete
  them and treat the repo as the only source — and delete the temporary `plan` doc once this
  merge lands (see the note at the top of this file).
- canon.md: `game_restarted` event not in canon's event table; factor-theorem start counts now
  reflect real runs from `883b3ca` (completion-rate jump is a measurement correction). Also `analytics.js`: `game_restarted` ignoring mode? Not investigated 29 Sep — carried forward, still open (moved from §6, 11 Nov 2026, TODO-TIDY).
- **CI maintenance:**
  - `serve-stubbed.py`'s port probe has no `SO_REUSEADDR`. For ~60s after a checker run the port
    sits in TIME_WAIT, the probe's plain `bind()` fails, the server exits, and `check-site.py`
    reports every page as a "navigation error" rather than "server did not start". Bites two
    back-to-back local runs; CI runs once per job, so unaffected there.
  - Bump the runner pin deliberately after 19 Oct 2026 (GitHub migrates `ubuntu-latest` to
    Ubuntu 26 from that date; pinned to `ubuntu-24.04` since 21 Sep): move to `ubuntu-26.04`,
    confirm one green run, then keep it pinned. Not urgent — 24.04 stays available well beyond.
  - Action versions: `actions/checkout@v4` and `actions/setup-python@v5` target Node 20 and are
    being forced onto Node 24 (a warning annotation, not a failure). Bump when GitHub names a
    removal date.
- **HANDOVER-IN-TASK-PRS:** BACKLOG-ONE's rule a: task PRs never edit `docs/handover/home.md` or `cloud.md`. A lane's close-out entry goes in the PR body under "Close-out entry (for <file>)", then into that lane's own file in a docs-only close-out PR, opened when no other live open PR edits the same file; stale PRs are reported for closing, not waited for. Parked by BACKLOG-ONE: AGENTS.md's "keep the branch handover current" (Contracts and handovers) and the takeover paragraph built on it assume a task branch edits its lane's handover. Owner: Project Claude to rule; home lane.
- **CANON-SEARCH-RULE** (SEARCH-KEYWORDS, 4 Nov): canon §7 records the one search rule, `MaffsSearch.match` (`schools/assets/search.js`: text plus `data-keywords`, every word, trailing s), called by the portal and card-filter.js; keywords in games.json via apply-meta.py, held by check-meta.py. Moved from cloud.md's live pointers. Owner: home lane.
- **CANON-ROOM-ESCAPED** (ROOM-ESCAPED, 4 Nov): canon §1.4 item 5 says rooms "escaped (`game_completed`)"; from endpoint `2026-11-04-a` an escape is a `game_completed` with `questions_correct` = `questions_answered` > 0, and any other is "timed out" (its own column). Moved from cloud.md's live pointers. Owner: home lane.
- **CANON-MONEY-ANSWERS** (MONEY-ANSWERS, 11 Nov 2026, CLOUD-QUEUE-1111 PR 2): canon §7.1.3 records the widened rule. A typed answer that is an amount of money gets a money box (`MaffsAnswer.moneyInput`) whichever marker the game uses. `MaffsAnswer.decimal()` and `exact()` take `opts.currency` ('£' or '€') and then accept one leading sign of that currency, exactly as `money()` does. A reader of its own (`parseFloat`) reads a money answer through `MaffsAnswer.parse()`. `scripts/check-banks.py` fails a page with money answers by any route (`money(`, a currency passed to `decimal(`/`exact(`, a `unit:'£'`/`'€'` question) that never calls `moneyInput(`. Owner: home lane (canon).
- **WHOSE-SIDE-TIMER-LINE:** `.claude/rules/timer-policy.md` gains Whose Side's line from the code (counts up, no lives, a faster right answer scores more); docs only; Project Claude reviews. It waited for WHOSE-SIDE-FIT, merged as #688. Moved from home.md's Queue. Owner: home lane.
- **ROOM-TIMES-READING:** read the room-time data, live from 7 Nov 16:41; exclude Jon's Comic Caper test, 16:42–16:45. Owner: Project Claude.
- **TICKER-CLICKED-REVIEW (about 21 Nov):** review the `ticker_clicked` data from TICKER-LINKS (#704). Owner: Project Claude.
- **BURST-CLEANUP:** remove `schools/assets/burst.js` and its hooks in a cleanup contract after The 6 P's launch (Jon, 25 Oct); until then do NOT remove them. The 6 P's v2 is built (SIX-PS-PLAYER, 25 Oct; `docs/history/contracts/2026-10-25-six-ps-player.md`). Moved from cloud.md's Queue 8 Nov (BRANCH-CLEANUP). Owner: home lane (shared asset).
- **CHECK-CHANGED-ONE-RUN** (Jon, 29 Oct 2026): full `check-changed` runs must not run concurrently on this machine. Two 225-check runs ran out of memory on 28 Oct and Claude Code stopped them. Run one at a time with nothing else heavy open; `--workers 2` is a safe setting (the default is half the CPUs, at most 6; heavy checks already run one at a time). A run killed this way is not a check failure. Not yet written as a rule: AGENTS.md and canon do not state it, and `docs/rules/scripts.md`'s two queues cover heavy checks inside one run, not two runs at once (11 Nov 2026). Write it into `docs/rules/scripts.md`, its reason in canon §12. Moved from §6 (TODO-TIDY). Owner: home lane.
- **PORTAL-RESET-TRIGGER** — `trigger: 'reset'`: **RULED 29 Sep 2026 (Jon): fire it on a cleared search.** Not yet built — wire `reportFilter('reset')` (or equivalent) into whatever clears the portal search box. On 11 Nov 2026 `index.html` calls `reportFilter` only with 'fresh', 'level', 'topic' and 'search' (`:3380`–`:3507`), and `.claude/rules/analytics.md` still calls `reset` reserved. Moved from §6 (TODO-TIDY). Owner: home lane (portal).
- **ESCAPE-FEEDBACK-LINK** — the escape-room feedback link, the remainder of "Footers everywhere" (**RULED 29 Sep 2026 (Jon): yes, standardise**; footer standardisation done, PR 57, 2 Oct 2026). No room page has a footer, and the footer PR left `escape-rooms/` alone: a fixed bar over the room engine needs its own layout check, so it is exempt in `check-footer.py` until that is done. Moved from §6 (TODO-TIDY). Owner: home lane.

## Parked, low priority
- `check-lock-bank.py` flags a computed `n == len([...])` VERIFY as a tautology; batch 6 works
  round it with `len([...]) - n == 0`.
- Escape-room games saved before `0907f6e` resume with their old, possibly colliding draw; clears
  itself as those games finish, no action planned.
- `serve-stubbed.py` blocks every fetch, not just analytics; consider `Cache-Control: no-store`
  for local serving.
- GA4 inline `gtag` `page_view` still fires on non-production hosts; needs a hostname condition in
  every page's snippet, or a saved hostname filter.
- **DAILY-BOARD-GROWTH:** Free Daily Pizza writes one Firebase board per day played (free_daily_pizza_daily_YYYY_MM_DD; 9 between 5 Oct and 3 Nov 2026, export of 10 Nov). Nothing removes old days. Decide later: delete days older than N, or move past days under an archive node. (Jon, 10 Nov 2026.) Owner: **Jon**.

---

## Post-freeze (after 2 Nov 2026): split the exam-guidance label from the on-screen calculator
Jon, 29 Oct 2026: the roster Calculator tag is exam guidance ("likely" a calculator or non-calculator paper), not enforcement. Today it also decides whether a game loads the calculator (`check-calculator.py`, canon 4.4). **To do:** make the calculator a separate per-game setting, on in every game except where the arithmetic is the skill (Six Sevens, Bruv, Estimation Golf, Factor Race; **Jon to confirm the list**). Badge wording ("Calculator required") is fixed by that check; "likely" on badges means changing the check and every badge together.
