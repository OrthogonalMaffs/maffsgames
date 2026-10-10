# MaffsGames to-do

**Repository history:** this repository started fresh on 2 Oct 2026. Any PR number or commit hash from before then, here or in canon and CLAUDE.md, refers to `OrthogonalMaffs/maffsgames-archive` (archived, read-only). This repository's PRs are #1–#31 so far.

Last updated: 6 Oct 2026 (home, night: Jon's rulings on audit tranches 3-6; 18 games unlisted, canon SR-16 to SR-20 and the build freeze, relist checklists §1.58-§1.75). Before that, 6 Oct 2026 (home: Simultaneous Solver PR #83, staged elimination, Foundation Stages 1-4 + A-Level verified; docs and the #82 relist checklists in this PR). Before that, 6 Oct 2026 (cloud: the four open PRs, one at a time): #75 (CI group D and the 75% time budget), #72 (search titles from data/games.json), #73 (teacher line on the results screen) and #74 (Estimation Engine rebuilt under SR-12, its own CI group E, back on /resit/ at 32) merged, each with main green; their docs in #76, #77 and this PR.
**29 Sep 2026, later still — three read-only follow-ups, no code touched.**
- **1.25 redeployed** by Jon, ~19:18Z; live rows confirm `correct`/`score` writing through. Only the
  backfill and a backup ahead of it remain, parked as Jon's own tasks — see 1.25's row and
  `docs/sheets-falsy-backfill.md` §6.
- **Snag #8 (recorded here, not in `docs/snagging-list.md`): Graph Transformer's analytics coverage
  against canon §1.3.** `question_answered` sends `game_slug, level, correct, question_index` — full
  coverage of §1.3's required set. `game_completed` sends `game_slug, level, score,
  questions_answered, accuracy` — **`questions_correct` is not sent**, the one §1.3-required
  parameter this game omits (confirmed live: rows show `correct` and `score`, not
  `questions_correct`); `questions_answered` here is always `puzzles.length` (12, the fixed session
  size), not a count of puzzles actually solved. `game_started` sends `game_slug, level` (no `mode`
  — this game isn't multi-mode, so §1.3 doesn't require one). `personal_best_set` sends `game_slug,
  level, score, previous_best` — full coverage. `game_abandoned` (automatic, via `analytics.js`)
  sends `game_slug, level, questions_answered` (the puzzle index reached, `pIdx`) in place of
  §1.3's `question_index` — same value, different key name, likely why live rows show it landing in
  the `questions_answered` column rather than `question_index`. **Skip is not a distinct event.**
  `skipPuzzle()` fires the exact same `question_answered` shape as a real wrong answer —
  `correct:false, question_index:pIdx+1` — with no flag distinguishing "skipped" from "tried and
  failed." In practice the two are indistinguishable in the data, but also inseparable from each
  other by design: `checkMatch()` only ever fires on a match (always `correct:true`), so every
  `correct:false` row for this game **is** a skip; there is no event at all for an unmatched
  attempt along the way (the whole point of continuous curve-manipulation gameplay — there's no
  discrete "submit"). No parameter added or changed to check any of this.
- **Leaderboard: Project Claude's recommendation, pending Jon's ruling — leave the old
  `graph-transformer` entries as they are.** The old marking rule only ever depressed scores (a
  rejected valid route forced extra moves or a skip; every multi-unit shift over-counted moves
  against par), never inflated them, so old entries undersell what the same play would score under
  the fixed rules rather than misstate it. New scores under the fixed rules will naturally displace
  them at the top of the board over time as students replay, without needing any write to Firebase.
  Not touched.

**Snagging list:** small, testable issues Jon finds while play-testing live games go in
`docs/snagging-list.md`, not here — check it alongside this file; an entry graduates into this
file's numbered sections only once it's bigger than a one-line fix.


## START OF NEXT SESSION

The live queues are `docs/handover/home.md` (home lane) and `docs/handover/cloud.md` (cloud lane).
This file's old START block (last updated 6 Oct 2026) is in `docs/history/todo-done.md`, word for word.

## 1. Live bugs and false claims

Done rows moved word for word to `docs/history/todo-done.md` ("Done rows from §1 and §3", 10 Oct 2026, TODO-SLIM); their numbers still resolve there: 1.3, 1.6, 1.7, 1.9, 1.10, 1.13, 1.15, 1.18, 1.19, 1.20, 1.21, 1.22, 1.28, 1.29, 1.31, 1.41, 1.42, 1.43, 1.44, 1.45, 1.46, 1.47, 1.49, 1.50, 1.55, 1.57, 3.13.

| # | Item | Owner |
|---|---|---|
| 1.4 | `matrix-crunch:171` and `formula-unlocked:295` show 3 options where there should be 4. `MaffsOptions.build()` drops the duplicate correctly but cannot invent a replacement. Each needs one genuine 4th distractor authored — a teaching call, not a code change. Until then `options.js` logs a `console.warn` on those questions, deliberately, as a visible canary. | **Jon** — two distractors |
| 1.8 | **Chart Interrogator, histogram Phase 2: H2 rejects a true answer.** The sentence always keys on the 4th class interval's share alone (>30% "most common range", >15% "typical"). In H2 that interval, 170–180, *is* the modal class at 28%, so "this is the most common range" is true and marked wrong. The other nine scenarios are not contradicted by the data. **RULED 29 Sep (modal class = highest frequency density); HELD 1 Oct 2026 by Jon, unbuilt: the ruling changes no key.** Under the ruled definition 170–180 is *not* H2's modal class: it has the highest frequency (40 of 143), but 165–170 has the highest density (6.0 against 4.0). So the rule keeps H2 on "typical", and keeps every other histogram's key too (H1 "most common", H3–H10 "typical"). Keying on highest frequency instead would call 170–180 "the most common range" beside a visibly taller 165–170 bar. The ruling also leaves the typical / relatively-few split on the 15% share. **The defect is the wording:** the same sentence opens "the class interval with the highest frequency is 170–180" and then asks if 170–180 is "the most common range", which a student reads as highest frequency. All ten tabled in `docs/audit-chart-interrogator-tolerances.md`. **RULED 1 Oct 2026 (Jon):** reword the item as a modal-class question ("170–180 contains the most people. Is it the modal class?"), keyed on highest frequency density, with an explanation that names frequency against frequency density. It applies to every histogram where class widths differ, which is all ten. **DONE 1 Oct 2026 (Jon approved the wording, with three additions).** Each histogram names one class and asks "[class] contains N [people]. Is it the modal class?", keyed on frequency density alone. Which class is named comes from a one-word `ask` field, with the data unchanged: `most` (the most populous class, the default), `modal` (H5) or `wide` (the most populous class wider than the modal one: H7, H8, H10). The keys split **5 Yes / 5 No** (H1, H3, H5, H6, H9 Yes). "Yes, because it contains the most …" is offered only when that is true of the named class, and is never keyed. Where the key is Yes it gets "Right answer, wrong reason." and the explanation (H1, H3, H6, H9). The % thresholds are gone. `scripts/verify-chart-interrogator.py` is in CI: it checks every class of every histogram, not only the named one, and its self-test has six injected faults. **Note for Jon:** H7's and H8's wide classes (fd 0.5 and 0.8 against 4.5 and 5.5) are easy Nos. H10's 10–20 (25 items against the modal 20–25's 30) is the only wide class that is a real trap. | — done; `--live` owed (home CC) |
| 1.11 | **Expectation Station's session-length buttons offer counts none of its banks can fill.** Core has 20 questions, GCSE 15, A-level 10 — all three below the 40–50 platform minimum (see 1.1's "24 questions only ever serves 20" finding). The real fix — growing each bank to the platform minimum — is content depth work, parked (§5). **FIXED 26 Sep (`b51e256`):** buttons now derive offered lengths from the level's bank size, falling back to the largest offered length when the previous selection no longer fits. Verified by a scripted play-through of all 7 offered buttons across the three levels. | — fixed, see 1.13 for the shared-helper follow-up |
| 1.12 | **`correct_override` — the three remaining uses, reviewed this session.** `formula-unlocked:295` overrides to a value that's algebraically equivalent to `correct` (its own `correct_note` says so) — Jon's distractor call, tracked at 1.4, not a data bug. `normal-navigator:222` and `:241` have **no `correct` field at all**, only `correct_override` — both are internally consistent with their options and steps, so nothing is hidden, but the field name implies an override of something that was never set. None of the three hide a wrong `correct` the way `coordinate-geometry-dash:298` did (fixed this session, `725dd4b`). | — reviewed, no action needed |
| 1.14 | **`test-the-claim`: every answer key recomputed. FIXED 30 Sep 2026.** It started as P3's impossible critical region (Po(3), two-tailed 5%: the region is X ≥ 8 only, with no lower region, but the key was "0 or 7"). The new independent verifier, `scripts/verify-test-the-claim.py` (in CI), recomputes every probability, critical value, p-value and verdict from each item's raw parameters, and found **16 of 48 items wrong**. Two decisions were backwards: **P7** (the true P(X ≤ 9) = 0.0433, so H₀ is rejected; the game marked the right answer wrong), and **Step 6's "Action" on all 24 items that reject H₀** (it keyed "reject the claim that ⟨H₁⟩"). Also: wrong displayed probabilities in B6, B8, B9, B11, P5, P6, P7 and P11; wrong boundaries in B6, B8, P3, P5, P6 and P7; wrong p-values in B6, B8, B9, P5, P7, P9 and P11; draft prose in B8, P9 and P11; five PMCC cells and C5 disagreeing with the Edexcel booklet's Table 8 (the booklet and exact computation agree in all 260 cells); no p-value and no explanation on all 24 Normal and correlation items ("undefined" on screen); the correct Step 6 conclusion shown twice on B8, B10, B12 and P8; and no way to enter "no lower critical region" (P3, B11, P9). All fixed under Jon's rulings of 30 Sep. Two-tailed items now compare the **probability in the tail with half the significance level**, labelled that way at Steps 3 and 4. **Full record, stated → corrected for every field, the 24 generated explanations for Jon's review, and the evidence: `docs/test-the-claim-verification.md`.** | **Follow-up, 30 Sep (later):** Step 6 lists shuffled, and correlation items give their p-value in the scenario (doc §"Follow-up"). | — fixed; **Jon** — review the 24 generated explanations; **the `--live` check is owed** (the sandbox cannot reach the site) |
| 1.16 | **Chart Interrogator: fixed tolerances that do not fit their scale, in box plots and stem and leaf.** This is the rest of 1.9's class; Contract B fixed cumulative frequency only. **Box plots B7** (a £2,880 axis) **and B10** (2,640 hours) mark the median and IQR to ±2, about a third of a pixel on the 500 px axis, so only an exact reading passes. The 2.5% rule would give ±72 and ±66. **Stem and leaf S3** (data 3.2–5.7 m) **and S9** (47.5–51.0 mm) mark to ±1 on decimal data: S3 accepts a median of 4.5 m anywhere from 3.5 to 5.5 m. A stem-and-leaf value is read from a table, not a graph, so the graph rule may not be the right one there. All 110 tolerances on the three types are tabled in Contract B's record. **RULED 29 Sep 2026 (Jon): different rules.** Box plots get the same 2.5%-of-axis-span rule as cumulative frequency (a drawn graph, estimated by eye). Stem and leaf gets exact/near-exact matching (a table of exact values, read not estimated). **FIXED 1 Oct 2026.** **Box plots:** 2.5% of the drawn axis (IQR 5%), read off `bpAxis`, the one axis definition the drawing also uses. B7 is now ±72 / ±144, B10 ±66 / ±132. **Stem and leaf:** marked exactly (Jon's ruling, 1 Oct), with a floating-point guard only; 35.5 and 35.50 are accepted, 35 and 36 are not. **Box-plot bands are capped** (Jon's ruling, 1 Oct; canon §7.1.2) below half the gap to the nearest named wrong answer: for a median, the other group's median and the box's own Q1 and Q3; for an IQR, the other group's IQR and either range. Before the cap, the uncapped 5% IQR band accepted the other group's IQR in 7 of 10 plots (3 under the old ±2); all 7 now reject it. The IQR is capped in 8 plots, the tightest being B9 at ±2.5, which is 4.6 px. No median is capped. **Nothing else moved:** no key changed, and the drawings are pixel-identical. All 110 tolerances are tabled in `docs/audit-chart-interrogator-tolerances.md`. **Verifier:** `scripts/verify-chart-interrogator.py`, 604 checks, not yet in CI (Jon's call). **Cumulative frequency re-checked against canon §7.1.2, 1 Oct 2026.** The bands are capped by the same `capTol()`. The named wrong answers are: for a quartile, the other two quartiles and its own position (n/4, n/2, 3n/4); for the IQR, n/2 and the axis range; for the benchmark count, n − count. No band admitted a named wrong answer. Only CF5's median was capped at half the gap (±1.5 to ±1.047, 8.6 px), because its median of 37.9 is 2.1 from n/2 = 40. All 30 of Contract B's pixel-measured readings of the drawn curve still pass, and the verifier checks every band. **`--live` checked 1 Oct 2026, from Claude Code at home:** the live page served the new build (all three PR 39/41/42 markers present); `check-site.py --live --only game:chart-interrogator` gave `tier 1: 9 PASS, 0 FAIL, 0 WARN (of 9 loads)`, network guard `escaped 0`, `OK`. Local `verify-chart-interrogator.py`: 1490 checks, 844 marking cases, 0 failures; all 8 self-test faults caught. | — fixed |
| 1.17 | **Chart Interrogator `drawCumFreq`: staircase shape and grey stroke.** Each class is a Bezier whose control points sit level with its ends, so the curve is horizontal at every plotted point. It reads as a smoothed staircase of S-bends, not the single smooth curve students are taught to draw. It is also drawn in the axis grey `#5a5e6a` at every level: canvas cannot resolve `strokeStyle='var(--accent)'`, so that assignment is ignored (measured from the canvas, 28 Sep). Contract B kept the drawing and keyed to it exactly, so neither affects marking. Changing the shape moves every key, so it goes through `cfCurve` and must be re-verified the same way. Needs its own contract. | **Jon** — the shape is a content call, then contract |
| 1.23 | **Spot the Error's KS3 (35) and Level 4 (30) tiers are below the platform's 40–50 question minimum** (GCSE's 45 is fine). Found by `docs/audit-spot-the-error.md`. Content depth work, likely parks alongside §5. | **Jon** — scope, then content work |
| 1.24 | **Options equal in value, only one marked right.** `coordinate-geometry-dash:233` ("Distance AB?") offered √50 beside the key 5√2 and never asked for simplest form, so a student who picked √50 was marked wrong. Found by the parent guides audit. **FIXED 28 Sep:** √50 became 50, the forgotten-square-root error (Jon's ruling); the step note keeps "5√2 and √50 are the same". **It is one of a class.** A scan of every bank (`docs/scan-value-equivalent-options.md`, `scripts/scan-value-equivalent-options.py`) found 229 value-equal pairs in 21 games:<br>• **32 more where the marked answer is offered twice and no form is asked**, in 10 games (probability-pioneer 8, sequence-solver 5, binomial-blaster 5 among them);<br>• 53 where the game is about form but the question doesn't say which (standard-form-blitz, surd-simplifier);<br>• 103 deliberate.<br>B2 and `MaffsOptions` compare strings, so none of it was visible. Draft contracts: `docs/next-contract-value-equivalent-options.md` (a B11 checker rule; the group B wording). **A further instance, 29 Sep 2026: Graph Transformer's match check compared the transform route (`{a,b,h,k}`), not the curve** — `y=(-x)^3` (Reflect y-axis) and `y=-x^3` (Reflect x-axis) are the same curve but different tuples, so a correct answer reached by a different valid route was rejected. Fixed in that game only (snag #7, `docs/snagging-list.md`) by comparing sampled curve values instead of parameters — not widened into this contract, since B11/the group A/B distractor work is about equal-value multiple-choice *options*, a different shape of the same underlying class. **Contract 2 DONE, PR 54 (2 Oct 2026):** standard-form-blitz and surd-simplifier asks now name the form they test (100 questions); group B 66 of 68 allowlisted; proof-builder's 2 wait on §1.30. | — Contract 2 done; proof-builder's 2 pairs wait on §1.30 |
| 1.25 | **Sheets export silently blanks `correct: false` and `question_index: 0`, and any other falsy field (`score`, `questions_correct`, ...).** `docs/apps-script-endpoint.js`'s `doPost` wrote every field as `data.field || ''`; `false`/`0` are both JS-falsy, so real wrong answers and real zero scores collapsed to a blank cell, indistinguishable from an omitted field. GA4 unaffected. **CODE FIXED 29 Sep 2026:** one helper, `cellValue()` (`docs/apps-script-endpoint.js:461`), replaces every `\|\| ''` in `doPost`; only `undefined`/`null` now blank a cell, `false` and `0` are written as-is. `SCRIPT_VERSION` bumped to `2026-09-29-c` so the redeploy is confirmable. **Full write-up: `docs/sheets-falsy-backfill.md`** — the inventory of every coercion in the pipeline (endpoint + `analytics.js`, the latter found clean), the Dashboard audit (Accuracy by Game / Hardest Questions have been right all along, "right by accident" — blank and `false` both fail the same `=== 'true'` check; only the Hardest-Questions *label* for the escape-room search sentinel was cosmetically malformed), the backfill function for `correct`/`question_index`/`score` (written, **not run**; `BACKFILL_CUTOFF` should now be set to Jon's ~19:18Z 29 Sep redeploy time), and a separate finding along the way: **`previous_score` is a dead column** — every sender sends `previous_best`, not `previous_score`, so that column has always been blank for an unrelated schema-mismatch reason, not this bug, and isn't backfillable. Also reported, not fixed: the escape-room `question_index: 0` sentinel's own cause (§5 of the doc). **REDEPLOYED — Jon, ~19:18Z 29 Sep 2026.** Live rows since then show `correct` and `score` writing through correctly. **Outstanding, parked (Jon's own tasks, not blocking):** the backfill for rows written before the redeploy (function is written, in `docs/sheets-falsy-backfill.md` §4(c), not run), and a backup of the pre-redeploy sheet before that backfill runs. | **Jon** — backup, then run the backfill per `docs/sheets-falsy-backfill.md` §4(c)/§6, whenever |
| 1.26 | **Hard-coded distribution values in four more games: the class of §1.14. `normal-navigator`, `core-maths-paper2a` and `maths-court` DONE 30 Sep 2026; `regression-rumble` STOPPED for Jon (37 of 40 scenarios fail).** Found by the class check of 30 Sep 2026 (none shares data or code with `test-the-claim`). **`normal-navigator` — DONE:** `scripts/verify-normal-navigator.py` (in CI) recomputes all 47 questions with `NormalDist` from their own prose (the game's `phi()` is never used) and renders each on the real page. It found **9 of 47 wrong**; Jon ruled to proceed (calculator values throughout). Stated → corrected: Q18 `:218` k = 60.2 → **60.3** (50 + 1.2816 × 8 = 60.2528; shade 60.24 → 60.25); Q23 `:225` P(bolt rejected) = 0.0456 → **0.0455** (2Φ(−2) = 0.045500; 0.0456 was 2 × the rounded 0.0228); Q14 `:212` step "0.8413 − 0.1587 = 0.6827" → "0.84134 − 0.15866 = 0.68268 ≈ 0.6827"; Q15 `:213` and Q36 `:247` "0.9772 − 0.0228 = 0.9545" (which is 0.9544) → "0.97725 − 0.02275 = 0.95450 ≈ 0.9545"; Q16/Q17 steps put on the same 5-d.p. convention (they were arithmetically right); Q37 `:248` "Same process. 1000 items…" (no distribution, and the pool is shuffled) → self-contained, "to the nearest whole number", key 45 → **46** (1000 × 0.04550026 = 45.50026), 45 kept as the truncation distractor with a misconception naming it, the old distractor "5" dropped to make room; Q38 `:251` added "Assume equal numbers of men and women." (without it "Cannot determine" was arguably right) and the unfinished "so equal density..." step rewritten as φ(1)/6 ≈ 0.0403 vs φ(1)/7 ≈ 0.0346; Q29 `:233` and Q39 `:252` `correct_override` folded into `correct` (both keys were right: μ = 25, σ = 5; μ = 16.55 → 17), and `correct_override` no longer appears in the bank (B10 ledger entries retired); Q35 `:244` misconception "for P(X > 100), also use 100.5" → "use 100.5". **Also fixed on Jon's ruling:** the μ/σ labels under the curve gave the answer away on Q29, 30, 31, 34, 39, 45 (`hideParams`: they read "?" until answered); two-region questions Q23, 29, 33, 37, 46 now shade both regions (`drawBell` takes a list of regions). **`regression-rumble`:** 28 scenarios with a hard-coded PMCC critical value (`cv`, 5% two-tailed), 14 of them also stating r beside its Σ sums, so r is recomputable. **`core-maths-paper2a`:** 7 of its 18 §3.5–3.6 items carry a Normal probability or a z critical value. **`maths-court`:** 1 item (`:575`, B(20, 0.5), P(X ≥ 15) = 0.0207, spot-checked correct). `docs/test-the-claim-verification.md` §"Class check" has the exclusions. **30 Sep 2026 (night), the other three:** one shared module, `scripts/stats_common.py` (exact binomial and Poisson, `NormalDist`, PMCC and least squares from sums or data, PMCC critical values from the exact null distribution, half-up rounding, a worked-step arithmetic checker; 42 unit tests against textbook values, in CI). `verify-test-the-claim.py` and `verify-normal-navigator.py` now import it; their output, normal and `--verbose`, is byte-identical before and after. **`core-maths-paper2a` — DONE, 0 of 27 statistics items wrong, no correction.** `scripts/verify-core-maths-paper2a.py` (in CI) recomputes every §3.5–3.7 value from its stem, checks every item's options, arithmetic and rendering (working hidden until answered; Q1's bars drawn at the stated 72/68/74/71), 5/5 injected faults caught. Note for Jon, not a failure: Q14 keys 2.5% by the 68-95-99.7 rule (calculator 2.28%); it is still the nearest option and the stem says "approximately". **`maths-court` — DONE, 0 wrong, no correction.** `scripts/verify-maths-court.py` (in CI) recomputes mc_core_001 (E = £1.50), 002 (68%), 006 (P(X ≤ 8) = 0.3120) and 009 (P(X ≥ 15) = 0.0207), arithmetic-checks every case's correct working and judge's summary, and renders each case (no card marked, summary hidden, before the verdict); 4/4 faults caught. WARN for Jon: mc_core_009 asks "Is the coin fair?" (two-tailed) but tests H₁: p > 0.5; the verdict is the same two-tailed (p = 0.0414). **`regression-rumble` — STOPPED (STOP IF: more than 10% fail), nothing corrected.** `scripts/verify-regression-rumble.py` (NOT in CI until the data is ruled) fails 37 of 40 scenarios, 62 findings: (1) Level 4's stated sums are impossible for 8 of 14 (|r| > 1: L4_1 1.30, L4_2 1.08, L4_6 1.08, L4_8 1.32, L4_9 1.37, L4_10 1.15, L4_11 1.34), and the stated r disagrees with the sums on 5 more (L4_3 −0.76 vs −0.55, L4_4 0.91 vs 0.81, L4_5 −0.71 vs −0.90, L4_7 −0.88 vs −0.74, L4_13 0.93 vs 0.77, L4_14 −0.87 vs −0.98; L4_12 0.74 vs 0.728 is within rounding); L4_3 is keyed significant but |r| = 0.55 < 0.6319; L4_5's prediction is 20, the line gives 21; L4_3's line prints "y = 13.17 − 0x" (b = −0.0049 to 2 d.p.). (2) Every core and A-level scatter contradicts its stated r: the points the game draws from its seed have r ≈ 0.98–1.00 whatever is stated (AL10 states 0.35, weak, not significant, and draws a near-perfect line); CM9 and AL14 draw a different line from the one stated; AL14 clips 7 of 15 points to the axis. (3) Pre-answer leak on all 14 Level 4 scenarios: the regression line and its equation are drawn before "Calculate b and a" is asked. What checks out: all six critical values (n = 10, 12, 15, 18, 20, 25), every other prediction, every sq4Type. Fixing it is new data (and a scatter generator whose r is the stated r), which is Jon's content call. | **Jon** — rule on regression-rumble's data; then **CC** fixes it and wires its verifier into CI |
| 1.27 | **New Shapes' three topic banks are 15 (parallelogram), 20 (trapezium) and 15 (prism), each below the platform's 40–50 minimum** (Jon, 1 Oct 2026). The game's one Year 6 bank totals 50, and a 30-question session draws 9 / 12 / 9. Recorded, not fixed: content work. | **Jon** — scope, then content |
| 1.30 | **`proof-builder` renders its induction stage prompts through `rkStr()`, which is KaTeX maths mode, so prose loses its spaces on every stage.** `:561` `promptDiv.innerHTML=rkStr(stage.prompt)`; `rkStr` (`:197`) passes the whole string to `katex.render`. Rendered 2 Oct 2026 exactly as `rkStr` does: "What value of n should we use for the base case?" shows as `Whatvalueofnshouldweuseforthebasecase?`. Live for every Further Maths student in induction mode. The steps and the other `rkStr` text (`:386`, `:444`, `:458`, `:524`, `:596`) are **suspected, not verified**. Same class as §1.10 (prose whole through KaTeX). Found during Contract 2, whose proof-builder step was split out for it; its 2 group B pairs (INDUCTION[0] stage 4, INDUCTION[3] stage 2) wait on this fix. **B7 ledger, 2 Oct (PR 59): 132 proof-builder entries** (INDUCTION prompts 12 and steps 13, COUNTER steps 65, SORTER lines 38 and titles 2, COUNTER `s` and `prompt` 1 each); every suspected `rkStr` site confirmed. | **Jon** — contract after the KaTeX wrapper audit (START block) |
| 1.32 | **`test-the-claim` shows `q.crExplanation` through `K(hint)` on a wrong Step 3 answer (critical-region method; `index.html:1718-1719`), so explanations that join their maths with a plain word lose their spaces.** Confirmed 2 Oct 2026 by calling the game's own `checkStep3()` with a wrong value on all 36 binomial, Poisson and Normal questions: **15 lose their spaces (8 binomial, 7 Poisson)**, e.g. `P(X ≤ 0) = 0.0352 < 0.05 and P(X ≤ 1) = 0.1671 > 0.05` shows as `P(X≤0)=0.0352<0.05andP(X≤1)=0.1671>0.05`. The other 21, and all 8 correlation explanations, were authored with `\text{}` and render correctly. (Jon's ruling filed this as "all 36 discrete explanations", from a figure the audit overstated mid-session; the count above is the corrected one.) Missed by §1.10, which fixed the prompts only (via `PQ`), and by B7, whose call-site match needs `K(x.field)` while this argument is a local variable. B7's prose test would flag only 1 of the 15 anyway ("and" and "Upper" are single words). **§1.14's verification (`verify-test-the-claim.py`) checked values, not rendering.** Found by the KaTeX wrapper audit, `docs/audit-katex-wrappers.md`. **B7 ledger, 2 Oct (PR 59): 15 entries**, all `QUESTIONS.crExplanation`, B7 now sees them through `K(hint)`. | **Jon** — in the fix contract with §1.30/§1.31 |
| 1.33 | ~~**`games/sequence-solver/index-original.html` is a stale, publicly served copy of Sequence Solver.** 531 lines, added 14 Mar 2026 (`757837d`), last touched 25 Mar 2026: the original single-mode "next term" game (a `SEQUENCES` array of term lists, a device-local `seq_lb` leaderboard), not the tiered rebuild. Checked 2 Oct 2026: **it does not serve `alevel[23]`** (it has no level banks at all; §1.29's fix is not missing from it, there is nothing for it to be missing from) but its own content has never been through any bank check; **it sends no game events** (no `mfg()`, no `analytics.js`, no `game_slug`, no Firebase), only GA4's automatic `page_view` under its own path, with the same `<title>` as the real game; **it is not in `sitemap.xml`** and is linked from nowhere in the repo, but it has no `noindex` and no canonical, so whether Google holds it is unknown (not checkable from a cloud session: Search Console, Jon). Exempt in `check-footer.py` with this row as its reason, untouched by the footer PR. **Proposed fix (Jon to confirm):** replace it with a redirect stub to `/games/sequence-solver/` (git history keeps the original).~~ **FIXED, PR 58, 2 Oct 2026:** replaced by a redirect stub to `/games/sequence-solver/` in the `/schools/` stubs' shape (meta refresh, canonical, link fallback); the original is in git history at `757837d`. Not indexed (Search Console, Jon, 2 Oct). Now a redirect-stub exemption in `check-footer.py`, and in `check-canonical-links.py`'s `REDIRECTS`, so a link to it fails CI. A search of `games/` found no other served copy of a game. Tier 1 cannot load it (§4 item 12). | — fixed |
| 1.34 | **Nine non-game pages scroll sideways on a 320px phone, from their own content.** Found 2 Oct 2026 while measuring the footer (document width at 320×568, identical on `main` and the footer branch, so not the footer): `/spec-map/` 540px, and eight parent guides, `probability-trees` 397, `indices-surds` 364, `fractions` 347 (its `.equiv-table`), `graphs-transformations` 339, `standard-form` 338, `pythagoras` 325, `statistics-data` 325, `coordinates` 324. Six games did the same (~~`estimation-golf` 797~~ fixed PR #47, 4 Oct 2026, `trig-wars` 711, `estimation-engine` 378, `equatle` 348, `better-value` 339, `differentiation-duel` 321); those are §3.9's phone-fit batches. Not traced element by element beyond `fractions`. **2 Oct 2026 (PR 62): recorded, not fixed.** Tier 1 now measures every page at 320×568 and fails on a new overflow; all of these are listed in `tier1_phone_overflow` (`scripts/checker-allowlist.json`) with their widths in the fallback font (e.g. `fractions` 347, `spec-map` 540) and the gate found more: 8 teacher pages (§1.37), 16 more games, and display maths in four of the guides (§1.38, not tables). Each fixing PR removes its entry. **Not in that list (3 Oct 2026): `moments-master` overflows at 320 on two questions only (`alevel[19]`, `alevel[40]`), which the seeded gate does not draw; recorded in §1.40.** | phone-fit batch, or its own |
| 1.35 | **Live bug class (tier 1/3): three games' KS3/GCSE scores never show on the leaderboard hub.** fraction-equivalence:208, percentage-flip:216 and prime-factorisation:212 submit non-year6 scores under level 'all', while leaderboards/index.html lists them with year6/ks3/gcse, so their KS3/GCSE scores never show on the hub. check-leaderboard-coverage.js misses it: with a variable level it assumes the roster's tiers rather than reading the variable's values. Also: extract-banks reports percentage-flip as 32 questions at every level (true: 12/12/20); check whether fraction-equivalence's 20 is misattributed the same way. Confirm the 'all' boards exist in the Firebase console before contracting. (Jon, 2 Oct 2026.) | **Jon** — confirm the 'all' boards in the Firebase console; then a contract |
| 1.36 | **Live bug class (canon §0.2, tier 1): answer tolerance not tied to the precision the question asks.** Every typed answer is `parseFloat` against a fixed or percentage band; there is no shared answer-marking helper in `schools/assets/`, every game rolls its own, and every money input is `type="number"` (a leading £ empties it). **Case 1, 2 d.p. money (Jon's rule, 2 Oct 2026):** if the correct answer is whole pounds, an integer is accepted (1250 or 1250.00); once pence are part of the answer it MUST be exactly 2 d.p. (1250.70 right; 1250.7 is the right amount in the wrong form). **Corrected 3 Oct 2026 to Jon's actual rule (canon §7.1.3):** the typed amount is compared numerically first; a right amount wrongly written (1250.7, 3050.0, 1250.700) is marked neither right nor wrong: the format message names the student's figure and they resubmit, with no penalty recorded. 1 d.p. is never accepted. Still assumed, not ruled: a leading £ is optional. **Live instance, checked 2 Oct 2026 on `4a04d7e`: `split-it`.** Single answers are marked to ±0.05 (`:543`), so on a pence answer it accepts the wrong value as well as the wrong form: £12.30 and £12.38 both pass for £12.34. That covers the £ unit-cost questions (`:380`) and the € currency questions (`:387`, keyed `toFixed(2)`). Its recipe-scaling answers, keyed to 1 d.p. (`:362`), are marked to ±0.15 (`:536`, `:538`), so 2.4 or 2.6 passes for 2.5. **Not live, checked:** `percentage-flip` (`:259`, `:282`) has no money answers (all 32 keys are whole numbers, no £); the rule applies to its rebuild (§3.11). `tax-theft` (`:1029`) keys whole pounds (`Math.round(expected)`, `:1040`); `growth-and-decay` (`:751`, `:790`) keys money to 3 s.f. Neither has a d.p. form problem; both have a tolerance question (below). **Proposed fix (shared layer):** `schools/assets/answer.js`, `MaffsAnswer.money(raw, correct)`, reading the raw typed string, never a parsed number, with three outcomes: correct / wrong / right value wrong form. Right value wrong form is NOT marked (corrected 3 Oct 2026; this line used to say "marked WRONG"): it gets the format message and a resubmission (canon §7.1.3; `moneyResult()` in tax-theft is the reference). Money inputs become `type="text" inputmode="decimal"`. `percentage-flip` adopts it as part of its rebuild; `split-it` follows as a separate pass, not a sweep, and its ±0.05 and ±0.15 bands go with it (the helper behind a band that admits wrong pence fixes nothing). Needs a checker rule too: any money answer in a bank stored or displayed at 1 d.p. **`tax-theft` and `growth-and-decay` tolerances (found 2 Oct 2026):** `tax-theft` accepted ±£1 (personal allowance, taxable) and ±£2 (tax, NI, deductions, net) of the whole-pound key (`:859`–`:961`), so a pence answer such as 1250.7 passed for £1251; its tax and NI are computed unrounded (only the allowance taper uses `Math.floor`) while the payslip shows rounded figures. `growth-and-decay` accepts 2% of the key + 0.01 on sub-question 1 (`:754`; sub-question 3 gets 0.5%, min 0.05), about ±£163 on CM4's £8,140, and ±0.15 on sub-question 4 (`:793`). **Suspected content bug, verified not fixed: `growth-and-decay` keys disagree with the precision their stems ask.** CM3 `:229` asks for 2 s.f. and keys 1808 (e^7.5 = 1808.04, so 1800); a scan of all 46 keys that carry an `sf` field found two more, AL5 `:380` (3 s.f., keyed 15530, should be 15500; money) and AL8 `:404` (3 s.f., keyed 2172, should be 2170). The `sf` field is never read. The 2% band hides it (1800, 15500 and 2170 are all accepted), but on a right answer the feedback shows the unrounded key. **RULED 2 Oct 2026 (Jon); both are requirements of the shared precision marker, not separate patches.** **`tax-theft`:** every step is keyed from the figures the student can see on screen, never from unrounded internals ("we can't mark a student against numbers they cannot see"), and marked to the penny. (This line used to say "marked as exact whole pounds": a misreading. Jon's 'whole pounds' meant whole-pound amounts need no .00, never round answers to pounds. Corrected 3 Oct 2026.) The ±£1 and ±£2 bands go. **Tax-theft DONE 3 Oct 2026 (START item 4).** **`growth-and-decay`:** correct the three keys (`:229` → 1800, `:380` → 15500, `:404` → 2170) and mark to the precision the question states, using the `sf` field the game already carries. (Jon, 2 Oct 2026.) **The three growth-and-decay keys are corrected in PR #3 (wrong-keys batch 1); marking by `sf` is still open.** **split-it DONE 3 Oct 2026 (PR #12):** every typed answer marked by the shared `MaffsAnswer` (`schools/assets/answer.js`): money (£ unit cost, € currency, £ shares) to the penny with an optional £/€, in `type="text" inputmode="decimal"` inputs; GCSE recipes and the speed questions now say "Give your answer(s) to 1 decimal place." and are marked to it (Jon's rulings; speed keys now exact, half up); everything else exact. The ±0.05 and ±0.15 bands are gone. Best Value's two unit prices now always differ by at least 1p (Jon). `verify-split-it.py` (CI) failed on the old file and passes. The shared helper is the proposed fix above, built; the other money games are START item 5. | **Code Claude** (shared precision marker; tax-theft and growth-and-decay ruled); **Jon** to rule the two assumed points |
| 1.37 | **`table.tt` overflows a 320px phone on all 8 teacher pages (500 to 617px).** Found by the phone-width gate, 2 Oct 2026. One rule, `escape-rooms/assets/engine.css:163` (`table.tt{width:100%;border-collapse:collapse;…}` with `td` padding that cannot shrink); every room's `teacher.html` builds its tables through `teacher.js`. **One shared fix** (a scroll container on the table, or a stacked layout under 480px), then remove the 8 `tier1_phone_overflow` entries. The teacher pages stay `noindex`. | CC |
| 1.38 | **KaTeX display maths overflows a phone in four parent guides** (`indices-surds` 364, `probability-trees` 397, `pythagoras` 325, `statistics-data` 325; the gate names `span.base`). Display maths with no horizontal scroll container. **Fix at the shared stylesheet, `parents/guide.css`** (`overflow-x: auto` on `.katex-display`), not per guide; check any other page that renders display maths. Then remove the 4 entries. Listed in §1.34 but a different cause from its tables. | CC |
| 1.39 | **`div.header-right` overflows a phone in 10 games** (`decimal-detective`, `equation-builder`, `four-quadrant-explorer`, `like-terms-collector`, `maths-court`, `negative-number-line`, `probability-pioneer`, `shape-shifter`, `word-problem-decoder`, `wrong-on-the-internet`, after start; 4 to 55px over). 24 games use the class name. **First establish whether it is a shared copied template** (diff the `.header-right` rules); if it is, one fix in the template's source and the 24 games that carry it; if not, §3.9's per-game batches (§3.9 already treats it per game). Nothing is changed until that is known. | CC |
| 1.40 | **Live (phone): `moments-master`'s option buttons overflow a 320px phone on some questions.** Seen in CI on 2 Oct 2026 (run 37045374170, the push run of PR 66, which touched no game): `phone-start:moments-master` 355px wide at 320×568 (+35), `button.opt-btn` to 355px. The pull-request run of the same commit passed, so it depends on the random first question; a student on a small phone gets sideways scroll on those questions. Not in `tier1_phone_overflow`, so the gate fails at random. **Jon (2 Oct): record it in `tier1_phone_overflow` with its width so CI is deterministic about it; fix it in the game's theme migration pass (§3.12).** **The entry lands with §4 item 16, not before:** an entry for a page that fits fails as stale (`check-site.py:1350`), so until the gate measures the same draws every run, an entry only flips which runs fail. Record the width §4 item 16's seeded measurement gives (its worst seed), not the 355px of one draw. **3 Oct 2026 (§4 item 16's PR): the overflowing questions are found and recorded here, not in `tier1_phone_overflow`.** A sweep of every question in both banks, each in all 24 option orders, at 320, 375 and 390px (web fonts blocked, as tier 1 does) found two, both A-Level and both at 320px only: **`alevel[19]`** (0-based bank index; the light beam, "Is it in equilibrium?") 365px locally, the key "No — net moment about midpoint \neq 0" is prose sent to KaTeX math mode, so it cannot wrap and **also loses its spaces** (a §1.10-class string, left alone: this PR may not touch questions); **`alevel[40]`** (the gate's top hinge) 361px locally, the key `\text{Cannot determine without more info}` is one unbreakable KaTeX box. Either one widens its grid column (`.options` is `1fr 1fr`, whose minimum is the widest option) and pushes the other column past the edge. Level 4: none. At 375 and 390: none. Widths are in the Windows fallback font; CI's DejaVu draw was 355px on 2 Oct. **Why no allowlist entry:** the seeded gate draws a first question that fits (320px), so an entry would fail as stale every run; the gate is now stable on this game and the overflow is recorded here instead. **Why not fixed here:** no contained fix exists. Wrapping needs either a layout change (one column on narrow phones) or rewriting the two keys (not allowed in this PR, and `alevel[19]` needs it anyway), so it stays with Jon's 2 Oct ruling: fix in the game's §3.12 theme pass, and re-sweep at 320, 375 and 390 then. | **§3.12 pass** (layout) + the `alevel[19]` string |
| 1.48 | **Cosmetic (not fixed): split-it's speed working shows the speed unrounded.** The feedback line reads e.g. "Speed = 40÷3 = 13.333333333333334 mph" (`spd = d/t` printed as a float). The key itself is now exact (PR #12). Also: the speed input shows "miles" on both sides (the unit label is drawn before the input for every unit and after it for non-money units). Found 3 Oct 2026; both left (question content and layout were out of scope). | Code Claude, with item 4 |
| 1.51 | **Resit audit (PR #35): what is left in the five games PR #36 fixed**, by the audit's fix batches. **Batch 2 (wrong keys at the card's level):** ~~`probability-pioneer` Stage 3 Q7 "If two outcomes are equally likely, each has probability 0.5" keyed True (audit F2; Jon ruled 4 Oct (decision 4): rekey False, with the explanation)~~ **DONE PR #45, with F3-F6 and F8 below; probability-pioneer now has its full verifier (`scripts/verify-probability-pioneer.py`, CI); only F7 (judgement call) remains.** **Batch 4 (MEDIUM):** ~~`probability-pioneer` F3 (lottery feedback says Impossible), F4 (rain in Britain keyed Certain only)~~ (done, PR #45); `estimation-engine` F2 (the meter's centre label is the key rounded to a whole number, outside the band on six items) and F3 (A-Level items served to everyone; rides with its SR-12 rebuild); `decimal-detective` ~~F4 (the 2 d.p. readout lets a student drag to the target without reading the scale; judgement call)~~ (done, PR #65, with F2 and F3). **Batch 5 (LOW):** `shape-shifter` F5 (15 items per mode; no 180° question is ever built, because its wrong-direction distractor equals the answer, so it is filtered out; every rotation is about (0,0)); `probability-pioneer` ~~F5/F6 (two value-equal distractor pairs, 2/3 and 4/6, 1/2 and 2/4)~~, F7, ~~F8~~ (F5, F6, F8 done, PR #45; F7 a judgement call, left); `estimation-engine` F5 (float edge on the band), F6 (an empty entry stops the timer silently), F7 (2 s auto-advance, not `MaffsNext`); `decimal-detective` ~~F6 (Round Up 9.5/9.50), F7 (= §1.49)~~ (done, PR #50, with F1), F5 (7.895: 7.90 vs 7.9, stands: the ask names the form), Line-Up's Check enabled on load; `negative-number-line` (Calculate distractors off the drawn line; wrong-answer Next not `MaffsNext`; its full verifier is in CI since PR #54). **Fixed in PR #36 beyond the contract's list:** shape-shifter F3 (duplicate options) and F4 (a distractor equal to the object), decimal-detective F3 (0.25's neighbouring tenths), negative-number-line F2 (half-way points). Each game still needs its full verifier (audit class 1); `check-resit-fixes.py` covers only the fixed faults. | Code Claude, batch by batch (F2 of probability-pioneer ruled by Jon, 4 Oct) |
| 1.52 | **Angle Ace: GCSE has 35 questions, and the roster lists a KS3 level with no bank** (resit audit F14). 35 is below the 40-50 minimum (`check-banks.py` B4 carries it in the ledger). `?level=ks3` falls back to GCSE (audit class 8, batch 5). Adding questions is content (Jon's call); every new item needs only a `fig` and passes `scripts/verify-angle-ace.py` or fails it. Found 4 Oct 2026, logged 6 Oct 2026 (Angle Ace contract, SR-9). | Jon (content) |
| 1.53 | **RELIST checklist: Trig Worms (`trig-worms`), unlisted by PR #82** pending its audit fixes (audit of 6 Oct 2026, Project doc `claude/audit-12-unverified-games-2026-10-06.md`). Done in the PR that fixes the game, every item: [ ] roster row back to listed; [ ] portal card in `index.html`; [ ] `sitemap.xml`; [ ] spec-map links; [ ] leaderboard hub row in `leaderboards/index.html` and its entry removed from `NOT_ON_HUB` in `scripts/check-leaderboard-coverage.js`; [ ] the trigonometry parent guide's "Play Trig Worms" button and its "two free games" line restored (`parents/trigonometry/index.html`). Jon, 6 Oct 2026. | done 7 Oct 2026: relisted under canon SR-21 (verifier in CI, no open CRITICAL/HIGH; open MEDIUM and LOW entries stay in the register) |
| 1.54 | **RELIST checklist: Spot the Error (`spot-the-error`), unlisted by PR #82** pending its audit fixes (same audit; see also 1.20-1.23). Done in the PR that fixes the game, every item: [ ] roster row back to listed; [ ] portal card in `index.html`; [ ] `sitemap.xml`; [ ] spec-map links; [ ] leaderboard hub row, and its entry removed from `NOT_ON_HUB`; [ ] the "Word Problems 1/3, 2/3" badges in `word-problem-decoder` and `equation-builder` checked: do they still make sense with Spot the Error unlisted, and again once it is back. Jon, 6 Oct 2026. | done 7 Oct 2026: relisted under canon SR-21 (verifier in CI, no open CRITICAL/HIGH; open MEDIUM and LOW entries stay in the register) |
| 1.56 | **RELIST checklist: Trig Identity Duel (`trig-identity-duel`), unlisted 6 Oct 2026** for the tranche 2 audit's faults (same report: wrong keys at :172 and :227-229, the value-equal pair at :243-244, keyboard re-marking). Relist when contract F's verifier for this game is merged, in that PR, every item: [ ] roster row back to the GCSE section (was #43); [ ] portal card in `index.html` (`?level=gcse`); [ ] `sitemap.xml`; [ ] spec-map: the E1–E7 link, and the G22–G23 row's plain text "Trig Identity Duel (being fixed)" back to its link (`../games/trig-identity-duel/?level=gcse`); [ ] leaderboard hub row `['trig-identity-duel','Trig Identity Duel',['gcse','alevel','level4']]`, and its entry removed from `NOT_ON_HUB`. Jon, 6 Oct 2026 19:15. | done 7 Oct 2026: relisted under canon SR-21 (verifier in CI, no open CRITICAL/HIGH; open MEDIUM and LOW entries stay in the register) |
| 1.58 | **RELIST checklist: Binomial Blaster (`binomial-blaster`), unlisted 6 Oct 2026** for the tranche 5 audit's faults (Jon's rulings of 20:30, canon SR-20 and his call beyond it: all eleven of tranche 5). Relist when this game's verifier merges and its register entries are fixed, in that PR, every item: [ ] roster row back to the A-Level section (was #81); [ ] portal card in `index.html` (`games/binomial-blaster/?level=alevel`); [ ] `sitemap.xml`; [ ] spec-map rows B4–B5: "(being fixed)" text back to links, removed links restored; [ ] leaderboard hub row `['binomial-blaster','Binomial Blaster',['alevel','alevel2']]` in `leaderboards/index.html`, and its entry removed from `NOT_ON_HUB`; [ ] weekly fact's game link in `index.html` FACTS restored ("Why 0! = 1": `g:"binomial-blaster",gl:"Work with factorials and binomials"`); [ ] every entry in `docs/audits/findings/binomial-blaster.yml` fixed, with its PR. Jon, 6 Oct 2026 20:30. | done 7 Oct 2026: relisted under canon SR-21 (verifier in CI, no open CRITICAL/HIGH; open MEDIUM and LOW entries stay in the register) |
| 1.59 | **RELIST checklist: Moments Master (`moments-master`), unlisted 6 Oct 2026** for the tranche 5 audit's faults (Jon's rulings of 20:30, canon SR-20 and his call beyond it: all eleven of tranche 5). Relist when this game's verifier merges and its register entries are fixed, in that PR, every item: [ ] roster row back to the A-Level section (was #79); [ ] portal card in `index.html` (`games/moments-master/?level=alevel`); [ ] `sitemap.xml`; [ ] spec-map rows S1–S3: "(being fixed)" text back to links, removed links restored; [ ] leaderboard hub row `['moments-master','Moments Master',['alevel','level4']]` in `leaderboards/index.html`, and its entry removed from `NOT_ON_HUB`; [ ] every entry in `docs/audits/findings/moments-master.yml` fixed, with its PR. Jon, 6 Oct 2026 20:30. | done 7 Oct 2026: relisted under canon SR-21 (verifier in CI, no open CRITICAL/HIGH; open MEDIUM and LOW entries stay in the register) |
| 1.60 | **RELIST checklist: Force Resolver (`force-resolver`), unlisted 6 Oct 2026** for the tranche 5 audit's faults (Jon's rulings of 20:30, canon SR-20 and his call beyond it: all eleven of tranche 5). Relist when this game's verifier merges and its register entries are fixed, in that PR, every item: [ ] roster row back to the A-Level section (was #78); [ ] portal card in `index.html` (`games/force-resolver/?level=alevel`); [ ] `sitemap.xml`; [ ] spec-map rows R1–R5: "(being fixed)" text back to links, removed links restored; [ ] leaderboard hub row `['force-resolver','Force Resolver',['alevel','level4']]` in `leaderboards/index.html`, and its entry removed from `NOT_ON_HUB`; [ ] every entry in `docs/audits/findings/force-resolver.yml` fixed, with its PR. Jon, 6 Oct 2026 20:30. | done 7 Oct 2026: relisted under canon SR-21 (verifier in CI, no open CRITICAL/HIGH; open MEDIUM and LOW entries stay in the register) |
| 1.61 | **RELIST checklist: Proof Builder (`proof-builder`), unlisted 6 Oct 2026** for the tranche 5 audit's faults (Jon's rulings of 20:30, canon SR-20 and his call beyond it: all eleven of tranche 5). Relist when this game's verifier merges and its register entries are fixed, in that PR, every item: [ ] roster row back to the A-Level section (was #83); [ ] portal card in `index.html` (`games/proof-builder/?level=alevel`); [ ] `sitemap.xml`; [ ] spec-map rows A1–A5, A1: "(being fixed)" text back to links, removed links restored; [ ] leaderboard hub row `['proof-builder','Proof Builder',['alevel','further']]` in `leaderboards/index.html`, and its entry removed from `NOT_ON_HUB`; [ ] weekly fact's game link in `index.html` FACTS restored ("Is Mathematics Discovered or Invented?": `g:"proof-builder",gl:"Build mathematical proofs"`); [ ] every entry in `docs/audits/findings/proof-builder.yml` fixed, with its PR. Jon, 6 Oct 2026 20:30. | done 7 Oct 2026: relisted under canon SR-21 (verifier in CI, no open CRITICAL/HIGH; open MEDIUM and LOW entries stay in the register) |
| 1.62 | **RELIST checklist: Factor Theorem (`factor-theorem`), unlisted 6 Oct 2026** for the tranche 5 audit's faults (Jon's rulings of 20:30, canon SR-20 and his call beyond it: all eleven of tranche 5). Relist when this game's verifier merges and its register entries are fixed, in that PR, every item: [x] roster row back to the A-Level section (was #88), A-Level only (Jon, 9 Oct); [x] portal cards in `index.html` (`games/factor-theorem/`, `games/factor-theorem/`); [x] `sitemap.xml`; [x] spec-map rows B6, Factor theorem, algebraic division (Coverage Status): "(being fixed)" text back to links, removed links restored; [x] leaderboard hub row `['factor-theorem','Factor Theorem',['alevel']]` in `leaderboards/index.html`, and its entry removed from `NOT_ON_HUB`; [x] relisted under SR-21 instead (no open CRITICAL or HIGH; t5-016 and t5-017, MEDIUM, open for the test bank). Jon, 6 Oct 2026 20:30. | **done 9 Oct 2026 (DOCS-9OCT)** |
| 1.63 | **RELIST checklist: Partial Fractions Duel (`partial-fractions-duel`), unlisted 6 Oct 2026** for the tranche 5 audit's faults (Jon's rulings of 20:30, canon SR-20 and his call beyond it: all eleven of tranche 5). Relist when this game's verifier merges and its register entries are fixed, in that PR, every item: [ ] roster row back to the A-Level section (was #82); [ ] portal card in `index.html` (`games/partial-fractions-duel/?level=alevel`); [ ] `sitemap.xml`; [ ] spec-map rows H1–H8: "(being fixed)" text back to links, removed links restored; [ ] leaderboard hub row `['partial-fractions-duel','Partial Fractions Duel',['alevel']]` in `leaderboards/index.html`, and its entry removed from `NOT_ON_HUB`; [ ] every entry in `docs/audits/findings/partial-fractions-duel.yml` fixed, with its PR. Jon, 6 Oct 2026 20:30. | done 7 Oct 2026: relisted under canon SR-21 (verifier in CI, no open CRITICAL/HIGH; open MEDIUM and LOW entries stay in the register) |
| 1.64 | **RELIST checklist: SUVAT Selector (`suvat`), unlisted 6 Oct 2026** for the tranche 5 audit's faults (Jon's rulings of 20:30, canon SR-20 and his call beyond it: all eleven of tranche 5). Relist when this game's verifier merges and its register entries are fixed, in that PR, every item: [ ] roster row back to the A-Level section (was #76); [ ] portal card in `index.html` (`games/suvat/?level=alevel`); [ ] `sitemap.xml`; [ ] spec-map rows Q1–Q3, Q4, Q5, LO2: "(being fixed)" text back to links, removed links restored; [ ] leaderboard hub row `['suvat','SUVAT Selector',['alevel','level4']]` in `leaderboards/index.html`, and its entry removed from `NOT_ON_HUB`; [ ] every entry in `docs/audits/findings/suvat.yml` fixed, with its PR. Jon, 6 Oct 2026 20:30. | done 7 Oct 2026: relisted under canon SR-21 (verifier in CI, no open CRITICAL/HIGH; open MEDIUM and LOW entries stay in the register) |
| 1.65 | **RELIST checklist: Curling Friction (`curling-friction`), unlisted 6 Oct 2026** for the tranche 5 audit's faults (Jon's rulings of 20:30, canon SR-20 and his call beyond it: all eleven of tranche 5). Relist when this game's verifier merges and its register entries are fixed, in that PR, every item: [ ] roster row back to the A-Level section (was #77); [ ] portal card in `index.html` (`games/curling-friction/?level=alevel`); [ ] `sitemap.xml`; [ ] spec-map rows R1–R5: "(being fixed)" text back to links, removed links restored; [ ] leaderboard hub row `['curling-friction','Curling Friction',['alevel','level4']]` in `leaderboards/index.html`, and its entry removed from `NOT_ON_HUB`; [ ] every entry in `docs/audits/findings/curling-friction.yml` fixed, with its PR. Jon, 6 Oct 2026 20:30. | done 7 Oct 2026: relisted under canon SR-21 (verifier in CI, no open CRITICAL/HIGH; open MEDIUM and LOW entries stay in the register) |
| 1.66 | **RELIST checklist: Dimension Checker (`dimension-checker`), unlisted 6 Oct 2026** for the tranche 5 audit's faults (Jon's rulings of 20:30, canon SR-20 and his call beyond it: all eleven of tranche 5). Relist when this game's verifier merges and its register entries are fixed, in that PR, every item: [ ] roster row back to the A-Level section (was #86); [ ] portal card in `index.html` (`games/dimension-checker/?level=level4`); [ ] `sitemap.xml`; [ ] spec-map rows LO2: "(being fixed)" text back to links, removed links restored; [ ] leaderboard hub row `['dimension-checker','Dimension Checker',['level4']]` in `leaderboards/index.html`, and its entry removed from `NOT_ON_HUB`; [ ] weekly fact's game link in `index.html` FACTS restored ("Dimensional Analysis Saves Lives": `g:"dimension-checker",gl:"Check dimensions in equations"`); [ ] every entry in `docs/audits/findings/dimension-checker.yml` fixed, with its PR. Jon, 6 Oct 2026 20:30. | done 7 Oct 2026: relisted under canon SR-21 (verifier in CI, no open CRITICAL/HIGH; open MEDIUM and LOW entries stay in the register) |
| 1.67 | **RELIST checklist: Differentiation Duel (`differentiation-duel`), unlisted 6 Oct 2026** for the tranche 5 audit's faults (Jon's rulings of 20:30, canon SR-20 and his call beyond it: all eleven of tranche 5). Relist when this game's verifier merges and its register entries are fixed, in that PR, every item: [ ] roster row back to the A-Level section (was #74); [ ] portal card in `index.html` (`games/differentiation-duel/?level=alevel`); [ ] `sitemap.xml`; [ ] spec-map rows G1–G4, G5–G6, Q4, LO2: "(being fixed)" text back to links, removed links restored; [ ] leaderboard hub row `['differentiation-duel','Differentiation Duel',['alevel','level4']]` in `leaderboards/index.html`, and its entry removed from `NOT_ON_HUB`; [ ] every entry in `docs/audits/findings/differentiation-duel.yml` fixed, with its PR. Jon, 6 Oct 2026 20:30. | done 7 Oct 2026: relisted under canon SR-21 (verifier in CI, no open CRITICAL/HIGH; open MEDIUM and LOW entries stay in the register) |
| 1.68 | **RELIST checklist: Integration Duel (`integration-duel`), unlisted 6 Oct 2026** for the tranche 5 audit's faults (Jon's rulings of 20:30, canon SR-20 and his call beyond it: all eleven of tranche 5). Relist when this game's verifier merges and its register entries are fixed, in that PR, every item: [ ] roster row back to the A-Level section (was #75); [ ] portal card in `index.html` (`games/integration-duel/?level=alevel`); [ ] `sitemap.xml`; [ ] spec-map rows H1–H8, LO2: "(being fixed)" text back to links, removed links restored; [ ] leaderboard hub row `['integration-duel','Integration Duel',['alevel','level4']]` in `leaderboards/index.html`, and its entry removed from `NOT_ON_HUB`; [ ] weekly fact's game link in `index.html` FACTS restored ("The Fundamental Theorem of Calculus": `g:"integration-duel",gl:"Practise integration"`); [ ] every entry in `docs/audits/findings/integration-duel.yml` fixed, with its PR. Jon, 6 Oct 2026 20:30. | done 7 Oct 2026: relisted under canon SR-21 (verifier in CI, no open CRITICAL/HIGH; open MEDIUM and LOW entries stay in the register) |
| 1.69 | **RELIST checklist: Eigenvector Engine (`eigenvector-engine`), unlisted 6 Oct 2026** for the tranche 6 audit's faults (Jon's rulings of 20:30, canon SR-20). Relist when this game's verifier merges and its register entries are fixed, in that PR, every item: [ ] roster row back to the Further Maths section (was #95); [ ] portal card in `index.html` (`games/eigenvector-engine/?level=further`); [ ] `sitemap.xml`; [ ] spec-map rows C10–C11: "(being fixed)" text back to links, removed links restored; [ ] leaderboard hub row `['eigenvector-engine','Eigenvector Engine',['further']]` in `leaderboards/index.html`, and its entry removed from `NOT_ON_HUB`; [ ] every entry in `docs/audits/findings/eigenvector-engine.yml` fixed, with its PR. Jon, 6 Oct 2026 20:30. | done 7 Oct 2026: relisted under canon SR-21 (verifier in CI, no open CRITICAL/HIGH; open MEDIUM and LOW entries stay in the register) |
| 1.70 | **RELIST checklist: The Truth Will Set You Free (`truth-will-set-you-free`), unlisted 6 Oct 2026** for the tranche 6 audit's faults (Jon's rulings of 20:30, canon SR-20). Relist when this game's verifier merges and its register entries are fixed, in that PR, every item: [ ] roster row back to the A-Level section (was #90); [ ] portal cards in `index.html` (`games/truth-will-set-you-free/?level=level4`, `games/truth-will-set-you-free/?level=level4`); [ ] `sitemap.xml`; [ ] spec-map rows LO1: "(being fixed)" text back to links, removed links restored; [ ] leaderboard hub row `['truth-will-set-you-free','The Truth Will Set You Free',['level4']]` in `leaderboards/index.html`, and its entry removed from `NOT_ON_HUB`; [ ] every entry in `docs/audits/findings/truth-will-set-you-free.yml` fixed, with its PR. Jon, 6 Oct 2026 20:30. | done 7 Oct 2026: relisted under canon SR-21 (verifier in CI, no open CRITICAL/HIGH; open MEDIUM and LOW entries stay in the register) |
| 1.71 | **RELIST checklist: Glorious Gantt Game (`glorious-gantt`), unlisted 6 Oct 2026** for the tranche 4 audit's faults (Jon's rulings of 20:30, canon SR-20). Relist when this game's verifier merges and its register entries are fixed, in that PR, every item: [ ] roster row back to the Core Maths section (was #72); [ ] portal card in `index.html` (`games/glorious-gantt/?mode=a&level=core`); [ ] `sitemap.xml`; [ ] spec-map rows LO2, §3.8: "(being fixed)" text back to links, removed links restored; [ ] leaderboard hub row `['glorious-gantt','Glorious Gantt',['core','level4']]` in `leaderboards/index.html`, and its entry removed from `NOT_ON_HUB`; [ ] canon §6.1's §3.8 row and note back to Covered; [ ] every entry in `docs/audits/findings/glorious-gantt.yml` fixed, with its PR. Jon, 6 Oct 2026 20:30. | open |
| 1.72 | **RELIST checklist: Screening Room (`screening-room`), unlisted 6 Oct 2026** for the tranche 4 audit's faults (Jon's rulings of 20:30, canon SR-20). Relist when this game's verifier merges and its register entries are fixed, in that PR, every item: [x] roster row back to the GCSE section (was #62); [x] portal cards in `index.html` (`games/screening-room/?level=gcse`, `games/screening-room/?level=gcse`, `games/screening-room/?level=core`); [x] `sitemap.xml`; [x] spec-map rows P6, P9, J1–J3, §3.9, Conditional probability, Bayes' theorem (Coverage Status): "(being fixed)" text back to links, removed links restored; [x] leaderboard hub row `['screening-room','Screening Room',['gcse','alevel','core','level4']]` in `leaderboards/index.html`, and its entry removed from `NOT_ON_HUB`; [x] weekly fact's game link in `index.html` FACTS restored ("98% Accurate Doesn't Mean What You Think": `g:"screening-room",gl:"Discover the base-rate effect"`); [x] canon §6.1's §3.9 row: "(unlisted)" removed; [x] every entry in `docs/audits/findings/screening-room.yml` fixed, with its PR (superseded by SR-21, 7 Oct: no open CRITICAL or HIGH is the bar). Jon, 6 Oct 2026 20:30. | **DONE 9 Oct 2026 (contract RELIST-SR, canon SR-21)**: t4-014 (MEDIUM) and t4-017 (LOW) stay open in the register (SR-21: MEDIUM and LOW do not hold a game back). Not on `/essentials/` before unlisting, so not added there. No /updates/ entry or badge (canon §3.4: phase 3 showing the scenario and array again fixed t4-015, hidden data, a correctness fix) |
| 1.73 | **RELIST checklist: Component Crusher (`component-crusher`), unlisted 6 Oct 2026** for the tranche 4 audit's faults (Jon's rulings of 20:30, canon SR-20). Relist when this game's verifier merges and its register entries are fixed, in that PR, every item: [ ] roster row back to the GCSE section (was #58); [ ] portal card in `index.html` (`games/component-crusher/?level=gcse`); [ ] `sitemap.xml`; [ ] spec-map rows I1–I2, Vectors in 2D and 3D (Coverage Status): "(being fixed)" text back to links, removed links restored; [ ] leaderboard hub row `['component-crusher','Component Crusher',['gcse','alevel','level4']]` in `leaderboards/index.html`, and its entry removed from `NOT_ON_HUB`; [ ] every entry in `docs/audits/findings/component-crusher.yml` fixed, with its PR. Jon, 6 Oct 2026 20:30. | done 7 Oct 2026: relisted under canon SR-21 (verifier in CI, no open CRITICAL/HIGH; open MEDIUM and LOW entries stay in the register) |
| 1.74 | **RELIST checklist: Linear Equation Solver (`linear-equation-solver`), unlisted 6 Oct 2026** for the tranche 4 audit's faults (Jon's rulings of 20:30, canon SR-20). Relist when this game's verifier merges and its register entries are fixed, in that PR, every item: [ ] roster row back to the GCSE section (was #63); [ ] portal card in `index.html` (`games/linear-equation-solver/`); [ ] `sitemap.xml`; [ ] spec-map rows A17: "(being fixed)" text back to links, removed links restored; [ ] leaderboard hub row `['linear-equation-solver','Linear Equation Solver',['gcse']]` in `leaderboards/index.html`, and its entry removed from `NOT_ON_HUB`; [ ] `/resit/` card back after `like-terms-collector` (Algebra), the slug back in `SUITE` and out of `UNLISTED` in `scripts/check-resit-page.py`; [ ] every entry in `docs/audits/findings/linear-equation-solver.yml` fixed, with its PR. Jon, 6 Oct 2026 20:30. | done 7 Oct 2026: relisted under canon SR-21 (verifier in CI, no open CRITICAL/HIGH; open MEDIUM and LOW entries stay in the register) |
| 1.75 | **RELIST checklist: Truth Buster (`truth-buster`), unlisted 6 Oct 2026** for the tranche 3 audit's faults (Jon's rulings of 20:30, canon SR-20). Relist when this game's verifier merges and its register entries are fixed, in that PR, every item: [x] roster row back to the KS3 section (was #17); [x] portal card in `index.html` (`games/truth-buster/`); [x] `sitemap.xml`; [x] leaderboard hub row `['truth-buster','Truth Buster',['all']]` in `leaderboards/index.html`, and its entry removed from `NOT_ON_HUB`; [x] its `EXCEPTIONS` entry back in `scripts/check-spec-mapping.py` (enrichment by design, Jon 3 Oct 2026); [ ] every entry in `docs/audits/findings/truth-buster.yml` fixed, with its PR (superseded by SR-21, 7 Oct: no open CRITICAL or HIGH is the bar). Jon, 6 Oct 2026 20:30. | **DONE 8 Oct 2026 (contract RELIST-3, canon SR-21)**: t3-014 (MEDIUM), t3-015 (LOW), t3-016 (MEDIUM) stay open in the register (SR-21: MEDIUM and LOW do not hold a game back; the cloud lane's) |

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
- [x] **1.5 Spec-map page false claims.** Hard-coded "87 games live" (`:363` before edit) while
  listing 69 of 94; "Every Maffs Games game mapped", "Full coverage achieved", "0 Gaps", "All
  Gaps Closed". **Interim fix (removal only, adds no new hard-coded number so it cannot drift):**
  the three stat tiles and the script that filled them deleted; the intro rewritten to state the
  page is being rebuilt; the "All Gaps Closed" heading now reads "Coverage Status"; "Full
  curriculum mapping" dropped from both meta descriptions; the back-link points at the portal
  root, labelled "Back to Games". No mapping row or figure touched. The real fix is §3.2.
- [x] Both merged branches deleted on `origin`: `claude/wizardly-gauss-uxv4v4`,
  `claude/cool-hawking-f88bj7` — both confirmed 0 commits ahead of `origin/main` before deletion.
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
- `proof-builder:232` — fixed earlier (`26af2fe`).
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
  board with full 45-question runs, scored as raw correct count. Pre-existing; keep, or separate?
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
| 3.18 | **DONE 4 Oct 2026 (Jon's rulings): better-value added to the R11 row; new rows P2 (expected-damage) and S6 (correlation-or-coincidence); the three /resit/ cards now show GCSE R11, P2, S6.** Original entry: **Three /resit/ games have no GCSE reference on the spec map** (found 3 Oct 2026 building the page; mapping is Jon's call, canon §0.3). `better-value` (map: Core Maths §3.10 only; audit §10.5 covers GCSE R11.1), `expected-damage` (Core §3.9 only; audit: P2.1), `correlation-or-coincidence` (A-Level M1–M3, Core §3.7; audit: S6.2). Their cards show the map's references with "(no GCSE reference on the map)"; once Jon maps them, rebuild the cards' spec lines (the check fails until the card matches the map). | — done |
| 3.19 | **Latent, not live: `section_clicked` sends position 0 when one element carries both `data-mfg-section` and `data-mfg-item`** (found 3 Oct 2026 building the /resit/ portal badge). `analytics.js` finds the section with `closest()`, which matches the element itself, but counts position with `sec.querySelectorAll('[data-mfg-item]')`, which does not include it. No live markup does this: the badge's section is a `display:contents` wrapper. Fix (count `sec` itself when it is an item) or document the rule in the analytics.js comment. | CC — small, when analytics.js is next touched |
| 3.20 | **Back links/headers: 40 games are not on the standard pattern** (survey 4 Oct 2026, all 99 `games/` folders). Standard, used by 59 since just-pythag-it-bruv moved to it (PR #32, 4 Oct): `<a href="../../" class="back-link">← Back to Games</a>` above the game header (its CSS varies cosmetically). Fold each game onto it in its §3.12 theme migration, never by sweep. **Entity only, looks identical (10):** chart-interrogator, complex-converter, gradient-hunter, higher-power, matrix-crunch, proportion-blaster, screening-room, tax-theft, trig-identity-duel, the-perfect-prank (off-roster prototype). **Split It's header bar, `class="back"` (15):** differentiation-duel, distinctly-average, factor-race, fraction-equivalence, index-laws, integration-duel, log-laws, modular-battle, percentage-flip, prime-factorisation (`href="/"`), quadratic-factoriser, regression-rumble (withdrawn), split-it, suvat, trig-worms. **`back-link` saying "MaffsGames" (4):** core-maths-paper1, -paper2a, -paper2b, -paper2c. **`back-link` to `/` (1):** fermi-lab. **Inline-styled link at the bottom (4):** better-value, expected-damage, formula-plug-in, new-shapes. **Inline-styled themed link (2):** estimation-golf, trig-wars. **A logo, not a back link (2):** 52dle, equatle. **`home-btn` (2):** boolean-blitz, truth-will-set-you-free. Whether the standard should become split-it's bar instead is Jon's call (§7.5 design). | Jon / per game |
| 3.21 | **Phone-fit checks do not model the system keyboard (found 4 Oct 2026, the phone keypad PR).** Every phone-fit measurement (tier 1's phone pass, `measure-phone-fit.py`, the per-game verifiers) loads the page at a full window height. On a real phone, focusing a typed-answer box opens the system keyboard, which takes roughly 40% of the screen, so a game that fits on paper can hide its question or diagram the moment the student starts typing (Just Pythag It, Bruv did; its keypad PR stopped the keyboard opening at all). **Games with a typed answer box (22, survey 4 Oct 2026, `<input>` of type text/number or built in script, leaderboard name fields excluded):** `52dle`, `chart-interrogator`, `component-crusher`, `estimation-engine`, `estimation-golf`, `factor-theorem`, `fermi-lab`, `given-that`, `glorious-gantt`, `graph-sketcher`, `growth-and-decay`, `just-pythag-it-bruv` (done: MaffsCalc's answer target, canon §4.4), `like-terms-collector`, `log-laws`, `percentage-flip`, `quadratic-factoriser`, `screening-room`, `split-it`, `stat-attack`, `suvat`, `tax-theft`, `test-the-claim`. Name or initials fields only (the keyboard opens at the end, over nothing that matters): `equatle`, `prime-or-composite`, `six-sevens-bruv`. **Options, for Jon:** (a) measure each game with the window shortened by a keyboard's height while the answer box has focus (Chromium cannot show the real keyboard; a shortened viewport is the model), and fix what that finds per game, with §3.9's phone fit; (b) give typed-answer games the shared keypad (MaffsCalc's answer target, or a keypad-only mount for games without a calculator), so the keyboard never opens. **Jon ruled (b), 4 Oct 2026:** the shared keypad, which fixes the cause once, in one place. **The shared layer is built (5 Oct 2026, PR #70):** `MaffsKeypad` (`schools/assets/keypad.js`, canon §4.4), the keypad-only form for games without a calculator and for several answer boxes; MaffsCalc's answer mode composes it, so there is one phone keypad. **Still to do: the rollout**, one game per contract, each game's phone fit measured with the keypad. **`estimation-engine` is the first game on MaffsKeypad (PR #74, 6 Oct 2026).** | Code Claude |

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
| 1 | `better-value` | +1097 | **WAITS**: Next on right and wrong alike (`:1278`). **DONE 1 Oct (batch 1):** right answers advance; wrong-answer Next fits 197/210/210 screens; asking may scroll (Jon) |
| 1 | `formula-plug-in` | +567 | **WAITS**: feedback panel with Next on both (`:214`). **DONE 1 Oct (batch 1):** right answers advance; asking and wrong fit 50/50 at all three sizes |
| 1 | `expected-damage` | +401 | **WAITS, unmarked**: Next after every trolley outcome (`:831`). **DONE 1 Oct (batch 1):** Next fits 50/50 normal, 19/20/20 escape; asking 35/43/50 |
| 1 | *also* `new-shapes` | passes | **WAITS**. **Ruled 1 Oct (Jon): fix**, so a right answer advances briskly. Done in this first batch, as it is not in any other. Once right answers advance, the keypad can go back to hiding on a wrong answer only (canon §7.6.1's wording); re-measure its right-answer screen **DONE 1 Oct (batch 1).** |

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

### Resit strand — game slate (Jon, 30 Sep)

Build order. The strand's voice word is **"Bruv"**, never "Bro". **[PROPOSED]** marks a working name
Jon has not yet fixed. Spec references are DfE subject-content parts (`docs/resit-coverage-audit.md`).

1. **Six Sevens, Bruv**: times tables. **Built** (PR 21, PR 25; items 3.4, 3.7).
2. **Free Daily Pizza**: FDP equivalence. **Built** 30 Sep 2026 (item 3.6, `docs/next-contract-free-daily-pizza.md`).
3. **How Many Parts?**: fraction operations, with misconception distractors.
4. **Not in Pen**: charts, reading AND constructing (drag bars, set pie angles, plot scatter points) (S2, S6).
5. **It's Not a Diamond** [PROPOSED]: shape vocabulary and properties (G1, G4, G9.1, G12).
6. **Use a Ruler, PLEASE** [PROPOSED]: straight-line and real-life graphs (A9.1, A14.1, A14.4).
7. **It's Not 50/50** [PROPOSED]: probability (P1.1, P6.1, P6.2).
8. **It's Just Base 60, Bruv**: time only.

   8b. **Small, or Far Away?**: metric units, map scales, scale drawings, measuring lines and angles (N13, R2.1, G15.1). The Father Ted reference is in the title only: no characters, lines or look-alike art.
9. **Letters? In Maffs? Y?!**: algebra basics (A1.1, A3.1, A4.1, A7.1). This is item 3.5(4)'s one algebra game, which also carries the A4.3 sub-skill (expanding one bracket). Each stage opens with why letters are used. **Decide before building** whether to link to `like-terms-collector` (live in a Google Classroom) rather than restyle it.
10. **Bond. Number Bond.** [PROPOSED]: number bonds to 10/100/1000, and decimals to 1.
11. **Maths Wizard** [PROPOSED]: Jon's mental strategies. Each card gives the trick, why it works and where it breaks, then a drill.
12. **Don't Count the Zeroes**: standard form (STRETCH). Item 3.5(3): built beside `standard-form-blitz`, scaffold-first with a place-value chart.
13. **Venn Diagrams AGAIN?**: HCF and LCM via prime-factor Venn diagrams.
14. **Just Pythag It, Bruv** (working title, Jon): Pythagoras' theorem, find the hypotenuse, find a shorter side, in
    context (G20.1's Pythagoras half; **STRETCH**, Jon 4 Oct 2026; for the June 2027 exams). **There is no dedicated
    Pythagoras game in the library:** G20's COVERED verdict rests on `trig-worms`, which never tests Pythagoras
    (audit §10.4, STRETCH build target). Design (Jon, 4 Oct 2026): (1) every question starts by identifying the
    hypotenuse; (2) the bank is weighted towards finding a shorter side (subtract); (3) the two types are mixed
    unpredictably so students can't add by habit; (4) the adding-instead-of-subtracting answer must appear as a
    distractor where options are shown; (5) Stage (a) includes scaled triples (e.g. 6-8-10, 9-12-15, 15-20-25,
    30-40-50, 10-24-26). When a question is a 3-4-5 or 5-12-13 multiple, the feedback after answering names it:
    "Spotted it? 6, 8, 10 is the 3-4-5 triangle doubled. No calculation needed." (adjusted to the triple and scale).
    The full worked method is still shown. The verifier checks every triple-family message names the correct base
    triple and scale factor. Still to specify: the stages (only stage (a) is named) and the build contract.

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
8. ~~**Readability check** — flag rendered question text with runs of >25 letters and no spaces
   (would have caught 1.10).~~ **DONE 26 Sep**, as checker tier 4 layer A's rule B7 (item 1 above)
   — and it did catch 1.10, plus (after 27 Sep's redefinition around prose, see 1.10) 2 more
   games. Two variants, both in `check-banks.py`: a syntactic check on the stored string itself,
   and a KaTeX-render check scoped to whichever field(s) each game's own source passes to
   `K()`/`renderToString` (found by reading the source, not a per-game list).
9. **PQ(s) routing is duplicated in `component-crusher:524`, `factor-theorem:262`,
   `test-the-claim:1159`** — move into `MaffsText.auto(s)` before a fourth game copies it.
10. ~~**`--write-ledger` must carry forward, unchanged, all ledger entries for games outside the
   extraction set (withdrawn or skipped), and report how many it carried.**~~ **DONE, PR 53, 2 Oct
   2026** (see the START block). Second occurrence of
   hand-copying (regression-rumble's three B4 entries, PRs 51 and 52); treat as a bug class, not a
   recurring manual step. (Jon, 2 Oct 2026.)
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
   Test the Claim is selected).
19. **CI flake: tier 4 lint reported B4 "level bank below 40" for `proportion-blaster::gcse`** in one of
   two identical runs of PR #36 (same commit; the other passed, as did a re-run). Locally the extraction
   reads 50 GCSE items and the game never mutates its bank, so the extraction or its grouping is
   intermittently short. Not investigated further (outside that PR). S.


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
- Escape rooms: IT Vengeance and Car Trap voice rewrites (each needs a premise/image conversation
  first), rooms A and B.
- Certificates (Phase 1b), teacher portal (Phase 2).

## 6. Jon — decisions and manual tasks

**Blocking something:**
- ~~**Database rules — ready to deploy (30 Sep 2026).**~~ **DONE: deployed by Jon and verified 30 Sep 2026 (night)**; see the handover. `docs/firebase-rules-deploy.md`. The live Realtime Database lets anyone delete or overwrite scores (proved 30 Sep: 11 `JLF` entries removed with no login). `firebase/database.rules.json` makes scores create-only, and it is emulator-tested (32/32). Jon: save the current rules, paste and publish, then verify that a real score submits and a REST `DELETE` is refused. The site change it depends on (no client prune) merges with the rules file, so publish any time after that.
- **Regression Rumble rebuild — needs Jon's content steer.** Withdrawn 30 Sep behind a holding page; what the rebuild needs is in §1.26.
- ~~Commit checker tier 4 layer A, or hold it back?~~ Resolved: committed 27 Sep as `175fb64` and
  running in CI.
- **Value-equivalent options (§1.24, queue item 8).** Issue or amend the two draft contracts. Choose
  the group A replacement distractors per game, starting with `probability-pioneer`. Confirm
  Contract 2's `ask` wording. **Not ruled 29 Sep** — needs its own session, per-game distractor
  authoring is too big to rule in passing.
- ~~Parent guides migration (queue item 9).~~ **Resolved, overtaken during this same session:**
  built and merged as PR #9 (`b4772cb`), 20 of 20 guides live at `/parents/`. See queue item 9 and
  this file's START block for the full record — this §6 entry was written before that merge landed
  and is stale now.
- ~~New-game gate: block merging a new game until it passes tier 4 layer A?~~ **RULED 29 Sep 2026
  (Jon): adopt the gate.** Layers B–E stay advisory until built. **Not yet implemented** — this
  rules the policy, the CI/branch-protection wiring is still to build.
- Spec-map spot-check (blocks §3.1) — still **Jon's own manual task**, not done 29 Sep.
- Circle Theorem Spotter Q48 numbers (§1.3); the two distractors (§1.4) — **not ruled 29 Sep**, need
  the actual question content read first; still open.
- ~~§7.6 Group C: author explanations, or accept answer-only?~~ **RULED 29 Sep 2026 (Jon): author
  real explanations** for all 6 (`equation-builder`, `factor-race`, `simultaneous-solver`,
  `estimation-engine`, `fraction-equivalence`, `quadratic-factoriser`). Not yet built.
- ~~§7.6 5s floor: adopt platform-wide?~~ **RULED 29 Sep 2026 (Jon): adopt platform-wide, but at
  3 seconds, not 5** — one change to `next-control.js`. Not yet built.
- Chart Interrogator §1.7/§1.8 keying rules — **1.8 (histogram H2) RULED 29 Sep 2026 (Jon): key on
  modal class**, not a raw % threshold — "most common range" is true iff the interval is the modal
  class (highest frequency density). **HELD 1 Oct 2026 (Jon):** under that definition H2's 170–180 is not modal (165–170 is), so the ruling changes no key; re-filed in §1.8 as a wording fix. **DONE 1 Oct 2026 (PR 41):** reworded as a modal-class question, keyed on frequency density; see §1.8.
- About page wording (§1.6) — **RULED and DONE 3 Oct 2026** (PR #6). Mapping the 28 unmapped games
  is §1.42.
- ~~Equations game (inverse operations, RAG rating): red move applies-and-recovers or reverts;
  portal level; name.~~ **RULED 29 Sep 2026 (Jon): drop this item — superseded.** `linear-
  equation-solver` already fills this gap; no separate equations game is needed.
- ~~Equation Builder read-only overlap report, before the equations game is built.~~ **Dropped 29
  Sep 2026** alongside the equations game item above — no longer has anything to report ahead of.

**Small, unblock whenever:**
- ~~Search-term sanitising: leave disagreeing, or strip both?~~ **RULED 29 Sep 2026 (Jon): leave
  disagreeing.** Checked the actual mechanism first: `search_query` goes to GA4 raw as its own
  field (no risk); `filter_value` packs the whole portal state into one Sheets column using `;=|`
  as its own delimiters, so `q=` strips those three characters before packing or the packing itself
  breaks. The two only disagree if a student's search text contains `;`, `=` or `|` — rare on a
  maths-game search box. Not worth losing GA4's raw text for that. No code change.
- ~~`trigger: 'reset'`?~~ **RULED 29 Sep 2026 (Jon): fire it on a cleared search.** Not yet built —
  wire `reportFilter('reset')` (or equivalent) into whatever clears the portal search box.
- ~~`like-terms-collector` banked runs: share or separate?~~ **RULED 29 Sep 2026 (Jon): separate.**
  Give Stage 3's banked finishes ("Finish here" at 25/35) their own leaderboard entry/tag so they
  stop competing directly with full 45-question runs. Not yet built; overlaps §2.
- ~~Expectation Station: exact everywhere, or keep the split?~~ **RULED 29 Sep 2026 (Jon): go exact
  everywhere.** Retire `formatPNum` globally — all 42 decimal scenarios move from "0.50"-style
  padded output to exact ("0.5"), matching FRACTION mode. Not yet built.
- Expectation Station bank mixes rounding conventions: `es_gcse_003`/`es_gcse_008` authored to
  rounded sums (1.33, 1.67), `es_gcse_005` exactly (1.5). No authoring errors — derived E(X) is
  always within 0.005 of the stated answer. Not raised for a ruling 29 Sep — not a decision, just a
  note.
- The four Kiln follow-ups — all **RULED 29 Sep 2026 (Jon)**, none built yet:
  - **Name him.** Add Mr Stephen Mudge's real name to the teacher page alongside "Smudgey", so a
    teacher opening it cold isn't confused.
  - **Add the explanation.** Document on the teacher page (not just canon §11.3) that a group
    hitting only named misconceptions skips some of Smudgey's wrong-entry lines by design.
  - **Leave the art as is.** The frayed-strap/finger ambiguity at thumbnail size is accepted, not
    rerolled.
  - **Set a floor on `a`.** Constrain the check-value lock generator so no future variant lands as
    lopsided as "2 + 48 ÷ 2".
- ~~`pe-shed-rebellion` variant 0 collision (48 psi vs "48π"; 12 m vs "day 12")?~~ **RULED 29 Sep
  2026 (Jon): fix it.** Change the audited bank locks per voice-rewrite doc §5h, even though the
  engine never currently serves variant 0 — latent, not worth leaving.
- ~~Footers everywhere?~~ **RULED 29 Sep 2026 (Jon): yes, standardise.** ~~Add the standard footer to
  `truth-will-set-you-free`~~ and a feedback link to the escape rooms.
  ~~**Also (1 Oct 2026): the site-wide "What's changed" link (`/updates/`).** It is on the portal and
  About footers only; every other footer gets it here, with the footer bug in §1.28.~~
  **Footer standardisation DONE, PR 57, 2 Oct 2026** (§1.28): every page but the exempt ones carries
  the one footer, "What's changed" included; `truth-will-set-you-free`, `boolean-blitz` (its own
  in-flow footer, Jon 2 Oct) and the `regression-rumble` holding page (Jon 2 Oct) gained it.
  **Still open: the escape-room feedback link.** No room page has a footer, and the footer PR left
  `escape-rooms/` alone: a fixed bar over the room engine needs its own layout check, so it is
  exempt in `check-footer.py` until that is done.
- **Rugby Mud, checked 29 Sep 2026 — no bug, answered.** Escape-room `dial`-type instruments (e.g.
  the fabric-cutter/tap-timer locks) *are* draggable — `escape-rooms/assets/engine.js`'s
  `wireDial()` repaints the dial on every `pointermove` while dragging (`:568`). But
  `question_answered` only fires from the lock-submit handlers (`:618`/`:628`), never from `paint()`
  itself, so dragging the needle around does **not** spam `question_answered` — it fires once per
  submitted attempt, same as every other lock type. Nothing to fix.
- **Sheets endpoint, checked 29 Sep 2026:**
  - `question_index` **is 1-based**, confirmed both by the documented convention
    (`.claude/rules/analytics.md:61`, "`question_index` is 1-based") and by
    `escape-rooms/assets/engine.js` itself (`R.locks.indexOf(l) + 1`, `activeLock + 1`). The one
    exception is the escape-room "search" event, which uses a `0` sentinel with its own `detail:
    'searched:...'` tag (`:347`) — not a real question index.
  - **Found a real bug, not yet fixed:** `docs/apps-script-endpoint.js`'s `doPost` (`:42`–`:47`)
    writes every field as `data.field || ''` — including `data.correct` and `data.question_index`.
    `false || ''` and `0 || ''` both collapse to blank, so **every genuinely wrong answer
    (`correct: false`) writes an empty `correct` cell in the Sheet**, indistinguishable from an
    event that never carried a `correct` field at all — and the escape-room's `question_index: 0`
    search event blanks the same way. This only affects the Sheets export; GA4 is unaffected (it
    receives the real values). Filed as **1.25** in §1.
- ~~`analytics.js`: `game_restarted` ignoring mode?~~ Not investigated 29 Sep — carried forward,
  still open.
- ~~Portal: "Correlation or Coincidence" two card titles?~~ **FIXED 29 Sep 2026.** The second card
  (`index.html:2618`, the Core Maths section) read "Correlation or Coincidence" without the "?";
  the canonical title, matching the game's own `<title>` and `<h1>`, has the "?"
  (`games/correlation-or-coincidence/index.html:16`/`:101`). One-word text fix, no other card
  touched.

**Manual tasks:**
- GA4: update the internal-traffic Data Filter to Jon's current home IP — Ivybridge traffic is
  still dirtying the portal analytics.
- Search Console: request indexing for `/escape-rooms/` and each live room (including
  `/escape-rooms/comic-caper/` and `/escape-rooms/kiln-disaster/`).
- **The mid-September analytics checkpoint is overdue.** Re-answer the three open questions in
  the project's `analytics-notes.md` against the 289/193/61.3% baseline.
- Events sheet: filter `game_abandoned` by `game_slug`, 1–15 Sep, to confirm no abandons are
  recorded against the homepage.
- Events sheet: check whether `FALSE` ever appears in the `correct` column for
  `question_answered` on any quiz game.
- Events sheet: optional — `binomial-blaster` `game_completed` with score 400 around 17:16 UTC
  16 Sep. If present, the deleted Firebase score was a real user and can be restored.

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
  reflect real runs from `883b3ca` (completion-rate jump is a measurement correction).
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

## Parked, low priority
- `check-lock-bank.py` flags a computed `n == len([...])` VERIFY as a tautology; batch 6 works
  round it with `len([...]) - n == 0`.
- Escape-room games saved before `0907f6e` resume with their old, possibly colliding draw; clears
  itself as those games finish, no action planned.
- `serve-stubbed.py` blocks every fetch, not just analytics; consider `Cache-Control: no-store`
  for local serving.
- GA4 inline `gtag` `page_view` still fires on non-production hosts; needs a hostname condition in
  every page's snippet, or a saved hostname filter.

---
