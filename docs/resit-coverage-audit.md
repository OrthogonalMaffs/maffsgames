# Resit coverage audit — GCSE Foundation content vs the live library

**Dated 30 Sep 2026. Read-only audit of `main` at `81b341a`.** A dated report, not a maintained table: it does not replace `spec-map/`, the roster or `docs/todo.md` §3.1, and nothing in it has been wired into the site. Written for Jon to rule on; it proposes no resit suite, no grade 1-3 banding and no portal change.

**Update, 30 Sep 2026: grade 1–3 banding added as §10** (Jon's ruling: CORE / STRETCH / OUT for all 129 parts, all 129 parts tagged after his rulings on the open questions, the ranked CORE gaps and the candidate resit suite). The sentence above that this audit "proposes no grade 1-3 banding" describes §§1–9; §10 is the banding.

**Why it exists.** The priority audience is grade 1-3 students and post-16 resitters. The portal is organised by KS3/GCSE/A-Level, and the spec-map has been stale before. Without this map the resit suite and the half-term target (w/c 26 Oct) would be chosen by guesswork.

## Headline

- **129 Foundation-assessable parts** in `data/dfe-gcse-parts.json` (74 standard + 55 underlined; the 45 bold parts are Higher-only and excluded). **62 COVERED, 36 THIN, 31 GAP.** 62 + 36 + 31 = 129; the totals reconcile with the file.
- **Counted, not asserted.** Every count below is computed from the extracted question banks or from a generator called live; nothing is inferred from a title, a roster tag or `spec-map/`.
- **The verdicts do not depend on the fuzzy attributions.** 62 COVERED holds whether or not the five diagnostic games (spot-the-error, spot-the-muppet, terrible-advice, wrong-on-the-internet, maths-court) are counted (62 without them). Only 12 THIN-versus-GAP calls hinge on their single items (§1.7).
- **COVERED is a floor, not a warranty.** It means one game has 10+ Foundation-pitched items for the part as the file words it. Many COVERED parts are composite and only some of the enumerated skills are practised; §3 states each gap it found (for example HCF/LCM, unknown-on-both-sides equations, mass and time conversions, enlargement, Pythagoras).
- **Where the library is thinnest:** the geometry vocabulary and 3D strand (G1, G4, G5, G9, G12, G13, G18), charts (S2), inequalities and quadratics-by-factorising (A18, A22), fractions/decimals conversion and arithmetic (N8, N10), ratio-as-fraction (R3, R6) and systematic listing/frequency trees (N5, P1).

## Stop conditions — how each was checked

1. **File typing usable and reconciling: yes.** The file types every part `standard`, `underlined` or `bold` (§2); 97 statements match the extractor's asserted ranges (N16 A25 R16 G25 P9 S6) and 174 parts = 74 + 55 + 45.
2. **Banks extractable: yes, for 84 of 95 games from a bank; the other 11 are true generators, handled from source and live calls, not from titles** (§1.2). Not a "handful failing": no game is unreadable. One environmental problem was found and fixed on the way (§1.2).
3. **More than 20% of coverage calls ambiguous between parts: TRIGGERED on two of three measures, so it is reported here as the contract requires.** 21% of records and 33% of (game, part) calls span two or more DfE statements; 15% of items do. The pattern is (a) the file splits one skill into fragments, so one item legitimately serves several, and (b) in the five diagnostic games one topic was mapped to two statements (Fractions to N2.1 and N8.1, Area to G16.1 and G17.1, Ratio to R4.1 and R5.1). §1.7 shows the sensitivity: **no COVERED verdict changes; 12 parts would move from THIN to GAP if those five games are dropped, and 1 (N8.1) if each topic is mapped to its first statement only.** I finished the report rather than halting, because the effect is bounded and stated; if you would rather the diagnostic games did not count at all, that is a one-line change to the rule.

## 1. Method

### 1.1 Spec side

Source: `data/dfe-gcse-parts.json`, derived by `scripts/extract-dfe-tier.py` from the DfE PDF vendored in `docs/sources/` (SHA-256 asserted). Read only; tiering was **not** re-derived from the PDF. The file stores the DfE's *printed* type per part. Its own rule (the `convention` block):

> **standard** — all students develop confidence and competence with this content.
> **underlined** — all students are assessed on standard and underlined content.
> **bold** — only the more highly attaining students are assessed on this content.

So **Foundation-assessable = `standard` + `underlined`**. `bold` is Higher-only and is not audited. The file has no F/H field; `data/spec-mapping.json` (with `depth` F/H/F+H) does not exist yet (todo §3.1). "Foundation-assessable" is therefore the DfE's printed content, which is wider than what an exam board's Foundation paper actually reaches (quadratic sequences, exact trig values and area/volume scale factors are printed underlined). Pitch, below, is judged separately.

| Area | Statements | Parts | standard | underlined | bold | **Foundation-assessable** |
|---|---|---|---|---|---|---|
| Number (N) | 16 | 26 | 14 | 5 | 7 | **19** |
| Algebra (A) | 25 | 62 | 20 | 20 | 22 | **40** |
| Ratio, proportion and rates of change (R) | 16 | 22 | 13 | 6 | 3 | **19** |
| Geometry and measures (G) | 25 | 42 | 15 | 18 | 9 | **33** |
| Probability (P) | 9 | 10 | 6 | 3 | 1 | **9** |
| Statistics (S) | 6 | 12 | 6 | 3 | 3 | **9** |
| **Total** | 97 | 174 | 74 | 55 | 45 | **129** |

**Two caveats about the file itself, both for Jon's outstanding spot-check (todo §3.1).**

- **Many parts are grammatical fragments**, cut at a type boundary: `N7.3` "indices", `G20.3` "and", `A22.3` "variable(", `A12.3` "y = 1x", `R13.2` "1Y ;". A fragment has no skill of its own, so it is marked † and given the verdict of the skill it belongs to (`G20.3` inherits `G20.1`; the others already share their neighbour's evidence). This is why a game that teaches one skill can "cover" three or four parts.
- **`A4.1` is typed standard but ends "…including those involving surds".** `N8.2` and `N8.4` type surds bold. I did not count surd items as Foundation evidence for `A4.1`; that is a judgement, and the fragment is the kind the spot-check should look at.

### 1.2 Game side

- **Banks:** `python scripts/extract-banks.py` (unchanged) reads every game's bank back from the live page under Playwright. Result: **95 games; 84 read from a bank (83 live + `given-that` by static fallback); 11 true generators** (`bearing-blitz`, `distinctly-average`, `equatle`, `graph-transformer`, `modular-battle`, `prime-factorisation`, `quadratic-factoriser`, `split-it`, `tax-theft`, `trig-wars`, `trig-worms`), matching the committed `data/check-ledger.json`. **5,082 unique bank items.**
- **Environmental problem found and fixed, worth knowing.** This sandbox's proxy returns 403 for the KaTeX CDN. Four games call `katex` at load *before* their bank is declared, so a first extraction reported `index-laws`, `differentiation-duel` and `integration-duel` as "generators" and read only 14 of `boolean-blitz`'s 56 items. I re-ran the unchanged extractor through a wrapper that answers the KaTeX URLs with a stub; the result then matched the ledger exactly. No repository file was changed. A checker run in an offline environment would report the same false generators.
- **Tier is read from the bank's own path, not the `?level=` query.** The extractor evaluates the whole bank object for every level query, so every level shows every item; de-duplicated by (game, variable, path, index). Where a bank is a single shared array the items are recorded as "shared bank" and the levels are the roster's. Where a bank is level-keyed only the Year 6 / KS3 / GCSE / Core tiers were audited, plus the GCSE tiers of games that also serve A-Level.
- **The 11 generators were read from the running page or their own source, not guessed.** Pools read live: `distinctly-average` (`DA_ITEMS`: 259 KS3, 398 GCSE), `quadratic-factoriser` (`gcsePool` 174, `higherPool` 3,760, `formulaPool` 1,254), `prime-factorisation` (`NUMBERS`), `tax-theft` (`SALARIES`). Generators called live and sampled: `split-it` (`generators[mode](level)`, 60 draws per mode and level) and `trig-worms` (`generateQuestion`, 300 draws). Read from source: `bearing-blitz` (`generateBearings`). **Counts for generators are lower bounds of an unbounded space** and are marked as such.
- **Escape rooms** were read from each `room.js` with the variant-0 figures filled in (`node` evaluation of `window.ROOM`); §6.

### 1.3 What counts as "addressing" a part

An item addresses a part when answering it makes the student *exercise* the skill: compute it, construct it, interpret it, or find the error in a worked use of it. Each record carries a mode: `procedural`, `constructive`, `interpretive` or `diagnostic`. **Recognition-only items are not counted:** `word-problem-decoder` asks the student to name the topic, never to do the topic (§7). Diagnostic games (a character gives flawed advice) are counted, flagged, and stay small (1-4 items per topic).

### 1.4 Pitch — the rule

Judged on **demand, not on the roster label**: an item is *Foundation-pitched* if its technique lies inside the part's standard/underlined wording and its demand is that of a Foundation-paper question (a few steps, modest numbers, formula or scaffold given). Items that need a bold-typed technique, Higher-only content, A-level content, or heavy calculator work are not. Per record: **YES** = at least 90% of counted items Foundation-pitched; **NO** = under 10%; **MIXED** = between. (Five records carry an explicit override, each stated in its reasoning line: `stat-attack`, where half of every scenario is beyond Foundation, and `graph-sketcher` A12.1/A14.1 (MIXED); `fermi-lab`, `regression-rumble` and the not-counted quadratic nth-term record (NO).) "Below Foundation" content (primary-level items such as adding on a -10 to 10 line) is counted as Foundation-pitched when the demand matches a Foundation paper's easiest questions; it is flagged in the reasoning line, because a resit student needs Foundation depth, not primary depth. **This is a judgement per item set; the sample items in §4 are there so you can overrule it.**

### 1.5 Verdict rule (from the contract)

- **COVERED** — at least one *single game* has 10 or more Foundation-pitched items for the part (a game's records for the same part are summed).
- **THIN** — items exist, but no single game reaches 10 Foundation-pitched ones (fewer items, or only in a game pitched too hard).
- **GAP** — no item in any game.

A part covered by three games with six items each is therefore THIN; the evidence column shows every game so you can see that. Composite parts are given the verdict of the contract's literal rule and the sub-skill gaps are stated separately (§3).

### 1.6 Register — how it was measured

Loaded each game in headless Chromium and read the computed body background and font, plus the visible start-screen text and the words in the question bank. **Canon §7.5.1** puts a game on the light/playful row if it serves a Year 6 or KS3 tier, and on the dark GCSE+ row otherwise. Facts only: the expected row, the measured row, and any wording a 16-19-year-old could read as school-age. The ☕ and 🏆 in every footer and leaderboard link are chrome and are ignored.

### 1.7 Ambiguity, and how much it matters

| Attribution rule | COVERED | THIN | GAP |
|---|---|---|---|
| As reported (all records) | 62 | 36 | 31 |
| Drop the five diagnostic games entirely | 62 | 24 | 43 |
| Diagnostic games mapped to their first statement only | 62 | 35 | 32 |

The 12 parts whose verdict changes without the diagnostic games (N8.1, N16.1, A4.4, A4.6, A7.1, A9.1, A18.1, A18.3, A22.1, A22.3, A22.5, R2.1) each rest on 1-3 items in those games.

### 1.8 What was not done

- Wording, pedagogy and whether an item is *good* stay Jon's call. Only "does it exercise the part, and is it Foundation-pitched" was judged.
- No grade 1-3 banding and no recommendation. Foundation covers grades 1-5; which of these parts a grade 2 student can meet is the ruling this report is meant to feed.
- A-Level, Further and Level 4 tiers were screened by roster tag and by reading the start, middle and end of each bank, not item by item. `data/banks/` was regenerated and is gitignored, so nothing here is committed except this file and the todo pointer. The classification code was scratch work and is not committed; the counts can be reproduced from `scripts/extract-banks.py` output plus the selectors described in each record.

## 2. The 129 Foundation parts, by area

| Area | Foundation parts | COVERED | THIN | GAP | COVERED, with a sub-skill note |
|---|---|---|---|---|---|
| Number | 19 | 11 | 5 | 3 | 10 |
| Algebra | 40 | 14 | 20 | 6 | 10 |
| Ratio, proportion and rates of change | 19 | 13 | 3 | 3 | 4 |
| Geometry and measures | 33 | 16 | 4 | 13 | 7 |
| Probability | 9 | 5 | 2 | 2 | 3 |
| Statistics | 9 | 3 | 2 | 4 | 3 |
| **Total** | **129** | **62** | **36** | **31** | **37** |

Reconciliation: 62 + 36 + 31 = 129 = the file's 129 Foundation-assessable parts (129 = 74 standard + 55 underlined).

## 3. Verdict by part

Columns: **Type** s = standard, u = underlined. **Evidence** = `game items-counted/Foundation-pitched` (a generator's figure is a lower bound). † = fragment with no skill of its own. Sub-skill notes are facts checked against the banks.

### Number

| Part | Type | DfE wording (as split in the file) | Verdict | Evidence (game n/F) | Sub-skill note |
|---|---|---|---|---|---|
| N1.1 | s | order positive and negative integers, decimals and fractions; use the symbols =, ≠, <, >… | **COVERED** | `negative-number-line` 15/15; `decimal-detective` 15/15; `wrong-on-the-internet` 1/1; `maths-court` 1/1 | Orders integers and decimals. No game orders fractions or uses the symbols =, ≠, <, >. |
| N2.1 | s | apply the four operations, including formal written methods, to integers, decimals and s… | **COVERED** | `negative-number-line` 15/15; `spot-the-error` 6/6; `terrible-advice` 3/3; `spot-the-muppet` 2/2; `wrong-on-the-internet` 2/2; `maths-court` 2/2 | Only add/subtract of negatives within ±10 is practised (15 items). No fraction, decimal or mixed-number arithmetic and no formal written methods. |
| N3.1 | s | recognise and use relationships between operations, including inverse operations (e.g. c… | **COVERED** | `think-of-a-number` 50/50; `wrong-on-the-internet` 2/2; `maths-court` 2/2 | Inverse operations only. Priority of operations (BIDMAS) appears in 4 diagnostic items (wrong-on-the-internet, maths-court). |
| N4.1 | s | use the concepts and vocabulary of prime numbers, factors (divisors), multiples, common … | **COVERED** | `prime-factorisation` 38/32; `prime-or-composite` 66/24; `factor-race` 20/20; `wrong-on-the-internet` 2/2; `maths-court` 2/2 | Factors, primes and prime factorisation are practised. Multiples, common factors, HCF and LCM have no practice item in any game (3 mentions in diagnostic/constructive items); the escape rooms carry them. |
| N5.1 | s | apply systematic listing strategies | **GAP** | — |  |
| N6.1 | s | use positive integer powers and associated real roots (square, cube and higher), recogni… | **COVERED** | `estimation-engine` 19/13; `index-laws` 14/7; `wrong-on-the-internet` 1/1 | Squares, cubes and roots occur only as operands inside estimation-engine. |
| N7.1 | u | calculate with roots, and with integer | **THIN** | `index-laws` 14/7; `wrong-on-the-internet` 2/2; `spot-the-muppet` 1/1; `terrible-advice` 1/1; `maths-court` 1/1 |  |
| N7.3 | u | † indices | **THIN** | `index-laws` 14/7 |  |
| N8.1 | s | calculate exactly with fractions, | **THIN** | `spot-the-error` 4/4; `terrible-advice` 2/2; `spot-the-muppet` 1/1; `wrong-on-the-internet` 1/1; `maths-court` 1/1 |  |
| N8.3 | u | † and multiples of π | **GAP** | — |  |
| N9.1 | s | calculate with and interpret standard form A x 10n, where 1 ≤ A < 10 and n is an integer… | **COVERED** | `standard-form-blitz` 50/30; `spot-the-error` 3/3; `spot-the-muppet` 2/2; `terrible-advice` 2/2; `wrong-on-the-internet` 1/1; `maths-court` 1/1 | Convert, compare and calculate. The 20 "calculate" items in standard-form-blitz (multiply/divide) are grade 5-6. |
| N10.1 | s | work interchangeably with terminating decimals and their corresponding fractions (such a… | **GAP** | — |  |
| N11.1 | s | identify and work with fractions in ratio problems | **COVERED** | `split-it` 91/91 |  |
| N12.1 | s | interpret fractions and percentages as operators. | **COVERED** | `percentage-flip` 29/29; `spot-the-muppet` 1/1 | Percentage of an amount (29) plus one fraction-of-amount diagnostic item; no fraction-of-amount practice. |
| N13.1 | s | use standard units of mass, length, time, money and other measures (including standard c… | **COVERED** | `unit-converter` 58/47 | Length, area, volume, litres and speed. No mass or time conversions. |
| N14.1 | s | estimate answers; check calculations using approximation and estimation, including answe… | **COVERED** | `estimation-engine` 49/32; `estimation-golf` 18/17; `fermi-lab` 27/0 | Tolerance-band mental arithmetic, not the round-to-1-s.f. estimation method. |
| N15.1 | s | round numbers and measures to an appropriate degree of accuracy (e.g. to a specified num… | **COVERED** | `decimal-detective` 15/15; `estimation-golf` 2/2; `spot-the-error` 1/1; `wrong-on-the-internet` 1/1; `maths-court` 1/1 | Rounding to nearest tenth/whole, 2 d.p., 1 s.f. No truncation. |
| N15.2 | u | to specify simple error intervals due to truncation or rounding | **THIN** | `core-maths-paper1` 1/1 |  |
| N16.1 | u | apply and interpret limits of accuracy | **THIN** | `spot-the-error` 1/0; `spot-the-muppet` 1/0; `terrible-advice` 1/0; `wrong-on-the-internet` 1/0; `maths-court` 1/0 |  |

### Algebra

| Part | Type | DfE wording (as split in the file) | Verdict | Evidence (game n/F) | Sub-skill note |
|---|---|---|---|---|---|
| A1.1 | s | use and interpret algebraic notation, including:  ab in place of a × b 3y in place of … | **GAP** | — |  |
| A2.1 | s | substitute numerical values into formulae and expressions, including scientific formulae | **COVERED** | `formula-plug-in` 50/50; `maths-court` 1/1 | Whole-number substitution into simple formulae. |
| A3.1 | s | understand and use the concepts and vocabulary of expressions, equations, formulae, iden… | **GAP** | — |  |
| A4.1 | s | simplify and manipulate algebraic expressions (including those involving surds | **GAP** | — |  |
| A4.3 | s | ) by:  collecting like terms  multiplying a single term over a bracket  taking out co… | **COVERED** | `like-terms-collector` 40/40; `spot-the-error` 1/1; `wrong-on-the-internet` 1/1 | Collecting like terms only. Multiplying a single term over a bracket and taking out common factors have no dedicated items. |
| A4.4 | u | expanding products of two | **THIN** | `spot-the-error` 1/1; `spot-the-muppet` 1/1; `terrible-advice` 1/1; `wrong-on-the-internet` 1/1; `maths-court` 1/1 |  |
| A4.6 | u | † binomials  | **THIN** | `spot-the-error` 1/1; `spot-the-muppet` 1/1; `terrible-advice` 1/1; `wrong-on-the-internet` 1/1; `maths-court` 1/1 |  |
| A4.7 | u | factorising quadratic expressions of the form x2 + bx + c, including the difference of t… | **COVERED** | `quadratic-factoriser` 174/174; `spot-the-muppet` 1/1; `terrible-advice` 1/1; `wrong-on-the-internet` 1/1; `maths-court` 1/1 | a = 1 only, which is what A4.7 states. |
| A4.9 | s |  simplifying expressions involving sums, products and powers, including the laws of ind… | **COVERED** | `index-laws` 31/25; `wrong-on-the-internet` 2/2; `spot-the-muppet` 1/1; `terrible-advice` 1/1; `maths-court` 1/1 |  |
| A5.1 | s | understand and use standard mathematical formulae; rearrange formulae to change the subj… | **COVERED** | `formula-unlocked` 29/18; `formula-forge` 29/15; `spot-the-error` 1/1 | Mostly stage 1-2 items; harder items excluded from the count. |
| A6.1 | u | know the difference between an equation and an identity; argue mathematically to show al… | **GAP** | — |  |
| A7.1 | s | where appropriate, interpret simple expressions as functions with inputs and outputs | **THIN** | `spot-the-error` 2/0 |  |
| A8.1 | s | work with coordinates in all four quadrants | **COVERED** | `four-quadrant-explorer` 45/45 |  |
| A9.1 | s | plot graphs of equations that correspond to straight-line graphs in the coordinate plane… | **THIN** | `spot-the-error` 1/1; `terrible-advice` 1/1; `wrong-on-the-internet` 1/1 |  |
| A9.2 | u | use the form y = mx + c to identify parallel | **THIN** | `coordinate-geometry-dash` 1/1 |  |
| A9.4 | u | ; find the equation of the line through two given points, or through one point with a gi… | **THIN** | `coordinate-geometry-dash` 4/4 |  |
| A10.1 | s | identify and interpret gradients and intercepts of linear functions graphically and alge… | **THIN** | `gradient-hunter` 15/7; `coordinate-geometry-dash` 6/6; `spot-the-error` 1/1; `spot-the-muppet` 1/1; `terrible-advice` 1/1; `wrong-on-the-internet` 1/1; +1 more |  |
| A11.1 | u | identify and interpret roots, intercepts, turning points of quadratic functionsgraphical… | **GAP** | — |  |
| A12.1 | s | recognise, sketch and interpret graphs of linear functions, quadratic functions, | **THIN** | `graph-sketcher` 15/8 |  |
| A12.2 | u | simple cubic functions, the reciprocal function | **THIN** | `graph-sketcher` 7/7 |  |
| A12.3 | s | † y = 1x | **THIN** | `graph-sketcher` 3/3 |  |
| A12.4 | u | † with x ≠ 0 | **THIN** | `graph-sketcher` 3/3 |  |
| A14.1 | s | plot and interpret graphs | **THIN** | `graph-sketcher` 15/8; `gradient-hunter` 15/7 |  |
| A14.2 | u | (including reciprocal graphs | **THIN** | `graph-sketcher` 3/3 |  |
| A14.4 | s | )and graphs of non-standard functions in real contexts, to find approximate solutions to… | **THIN** | `gradient-hunter` 15/7; `core-maths-paper2c` 4/4 |  |
| A17.1 | s | solve linear equations in one unknown algebraically (including those with the unknown on… | **COVERED** | `linear-equation-solver` 141/141 | Unknown on one side. No unknown-on-both-sides shape, which A17.1 names. |
| A18.1 | u | solve quadratic equations ( | **THIN** | `spot-the-error` 1/1; `spot-the-muppet` 1/1; `terrible-advice` 1/1 |  |
| A18.3 | u | ) algebraically by factorising | **THIN** | `spot-the-error` 1/1; `spot-the-muppet` 1/1; `terrible-advice` 1/1 |  |
| A18.5 | u | ; find approximate solutions using a graph | **GAP** | — |  |
| A19.1 | u | solve two simultaneous equations in two variables (linear/linear | **COVERED** | `simultaneous-solver` 50/46; `spot-the-error` 3/3; `spot-the-muppet` 2/2; `terrible-advice` 2/2; `maths-court` 1/1 |  |
| A19.3 | u | ) algebraically; find approximate solutions using a graph | **THIN** | `coordinate-geometry-dash` 2/2; `core-maths-paper2c` 1/1 |  |
| A21.1 | u | translate simple situations or procedures into algebraic expressions or formulae; derive… | **COVERED** | `equation-builder` 80/60 | Builds the expression/equation. Does not ask the student to solve or interpret it. |
| A22.1 | u | solve linear inequalities in one | **THIN** | `spot-the-error` 1/1 |  |
| A22.3 | u | † variable( | **THIN** | `spot-the-error` 1/1 |  |
| A22.5 | u | ; represent the solution set on a number line | **THIN** | `spot-the-error` 1/1 |  |
| A23.1 | s | generate terms of a sequence from either a term-to-term or a position-to-term rule | **COVERED** | `sequence-solver` 46/46; `spot-the-error` 4/4; `spot-the-muppet` 2/2; `terrible-advice` 2/2; `maths-court` 1/1 | Term-to-term and position-to-term. |
| A24.1 | s | recognise and use sequences of triangular, square and cube numbers, simple | **COVERED** | `sequence-solver` 10/10 | Cube numbers in one item only. |
| A24.2 | u | arithmetic progressions, Fibonacci type sequences, quadratic sequences, and simple geome… | **COVERED** | `sequence-solver` 43/43 |  |
| A25.1 | s | deduce expressions to calculate the nth term of linear | **COVERED** | `sequence-solver` 21/21; `spot-the-error` 4/4; `spot-the-muppet` 2/2; `terrible-advice` 2/2; `maths-court` 1/1 | Linear nth term only (quadratic is the bold A25.2). |
| A25.3 | s | † sequences. | **COVERED** | `sequence-solver` 21/21 | Fragment of A25.1 (same evidence). |

### Ratio, proportion and rates of change

| Part | Type | DfE wording (as split in the file) | Verdict | Evidence (game n/F) | Sub-skill note |
|---|---|---|---|---|---|
| R1.1 | s | change freely between related standard units (e.g. time, length, area, volume/capacity, … | **COVERED** | `unit-converter` 58/47; `spot-the-error` 1/1; `wrong-on-the-internet` 1/1 | Length, area, volume, speed. No mass or time conversions. |
| R2.1 | s | use scale factors, scale diagrams and maps | **THIN** | `spot-the-error` 1/1; `spot-the-muppet` 1/1; `terrible-advice` 1/1 |  |
| R3.1 | s | express one quantity as a fraction of another, where the fraction is less than 1 or grea… | **GAP** | — |  |
| R4.1 | s | use ratio notation, including reduction to simplest form | **COVERED** | `split-it` 109/109; `spot-the-error` 3/3; `terrible-advice` 3/3; `spot-the-muppet` 2/2; `wrong-on-the-internet` 1/1; `maths-court` 1/1 |  |
| R5.1 | s | divide a given quantity into two parts in a given part:part or part:whole ratio; express… | **COVERED** | `split-it` 118/118; `proportion-blaster` 12/10; `spot-the-error` 3/3; `terrible-advice` 3/3; `spot-the-muppet` 2/2; `wrong-on-the-internet` 1/1; +1 more |  |
| R6.1 | s | express a multiplicative relationship between two quantities as a ratio or a fraction | **GAP** | — |  |
| R7.1 | s | understand and use proportion as equality of ratios | **COVERED** | `split-it` 116/116; `spot-the-error` 2/2; `spot-the-muppet` 1/1; `terrible-advice` 1/1; `maths-court` 1/1 |  |
| R8.1 | s | relate ratios to fractions and to linear functions | **COVERED** | `split-it` 91/91 |  |
| R9.1 | s | define percentage as ‘number of parts per hundred’; interpret percentages and percentage… | **COVERED** | `percentage-flip` 29/29; `tax-theft` 20/8; `spot-the-error` 7/7; `core-maths-paper1` 8/7; `spot-the-muppet` 6/6; `terrible-advice` 6/6; +4 more | Percentage of an amount is the practised skill (29 items, percentage-flip). Money-context percentages appear in the Core Maths papers (8 items in paper 1); original-value problems in 2 proportion-blaster items and several diagnostic items. "As a percentage of" wording appears in 3 items only. |
| R10.1 | s | solve problems involving direct and inverse proportion, including graphical and algebrai… | **COVERED** | `split-it` 193/193; `proportion-blaster` 34/21; `spot-the-error` 2/2; `spot-the-muppet` 1/1; `terrible-advice` 1/1; `maths-court` 1/1 | Direct and inverse proportion by formula. No graphical representation. |
| R11.1 | s | use compound units such as speed, rates of pay, unit pricing | **COVERED** | `split-it` 193/193; `better-value` 20/18; `formula-plug-in` 15/15; `spot-the-muppet` 2/2; `spot-the-error` 1/1; `terrible-advice` 1/1; +1 more |  |
| R11.2 | u | † , density and pressure | **GAP** | — |  |
| R12.1 | s | compare lengths, areas and volumes using ratio notation; make links to similarity | **COVERED** | `scale-factor-scaling` 46/28 | Area/volume scale factors. No link to trigonometric ratios. |
| R12.2 | u | (including trigonometric ratios) and scale factors | **COVERED** | `scale-factor-scaling` 46/28; `spot-the-error` 1/1 |  |
| R13.1 | u | understand that X is inversely proportional to Y is equivalent to X is proportional to | **COVERED** | `proportion-blaster` 34/21 |  |
| R13.2 | s | † 1Y ; | **COVERED** | `proportion-blaster` 34/21 |  |
| R13.4 | u | interpret equations that describe direct and inverse proportion | **COVERED** | `proportion-blaster` 34/21 |  |
| R14.1 | u | interpret the gradient of a straight line graph as a rate of change; recognise and inter… | **THIN** | `gradient-hunter` 15/7; `core-maths-paper2c` 2/2; `maths-court` 1/1 |  |
| R16.1 | u | set up, solve and interpret the answers in growth and decay problems, includingcompound … | **THIN** | `growth-and-decay` 15/9; `spot-the-muppet` 2/2; `terrible-advice` 2/2; `proportion-blaster` 2/2; `spot-the-error` 1/1; `wrong-on-the-internet` 1/1; +2 more |  |

### Geometry and measures

| Part | Type | DfE wording (as split in the file) | Verdict | Evidence (game n/F) | Sub-skill note |
|---|---|---|---|---|---|
| G1.1 | s | use conventional terms and notations: points, lines, vertices, edges, planes, parallel l… | **GAP** | — |  |
| G2.1 | u | use the standard ruler and compass constructions (perpendicular bisector of a line segme… | **COVERED** | `constructions-lab` 10/10 |  |
| G3.1 | s | apply the properties of angles at a point, angles at a point on a straight line, vertica… | **COVERED** | `angle-ace` 75/75; `spot-the-error` 4/4; `spot-the-muppet` 1/1; `terrible-advice` 1/1; `wrong-on-the-internet` 1/1; `maths-court` 1/1 | Angle facts, parallel-line angles, triangle sum, isosceles. No polygon angle-sum items (two items use the exterior angle of a triangle). |
| G4.1 | s | derive and apply the properties and definitions of: special types of quadrilaterals, inc… | **GAP** | — |  |
| G5.1 | u | use the basic congruence criteria for triangles (SSS, SAS, ASA, RHS) | **GAP** | — |  |
| G6.1 | u | apply angle facts, triangle congruence, similarity and properties of quadrilaterals to c… | **GAP** | — |  |
| G7.1 | s | identify, describe and construct congruent and similar shapes, including on coordinate a… | **COVERED** | `shape-shifter` 45/45 | Translation, reflection, rotation. No enlargement items. |
| G7.2 | u | † (including fractional | **GAP** | — |  |
| G7.4 | u | † scale factors) | **GAP** | — |  |
| G9.1 | s | identify and apply circle definitions and properties, including: centre, radius, chord, | **GAP** | — |  |
| G9.2 | u | diameter, circumference, tangent, arc, sector and segment | **GAP** | — |  |
| G11.1 | s | solve geometrical problems on coordinate axes | **THIN** | `coordinate-geometry-dash` 8/6 |  |
| G12.1 | s | identify properties of the faces, surfaces, edges and vertices of: cubes, cuboids, prism… | **GAP** | — |  |
| G13.1 | u | † construct and | **GAP** | — |  |
| G13.2 | s | interpret plans and elevations of 3D shapes. | **GAP** | — |  |
| G14.1 | s | use standard units of measure and related concepts (length, area, volume/capacity, mass,… | **COVERED** | `unit-converter` 58/47 | Same evidence as N13.1: no mass or time. |
| G15.1 | s | measure line segments and angles in geometric figures, including interpreting maps and s… | **COVERED** | `bearing-blitz` 24/24; `spot-the-error` 1/1 | Bearings set by eye on a compass. No measuring, no back-bearings, no map or scale drawing. |
| G16.1 | s | know and apply formulae to calculate: area of triangles, parallelograms, trapezia; volum… | **COVERED** | `new-shapes` 50/50; `formula-plug-in` 10/10; `spot-the-error` 3/3; `spot-the-muppet` 2/2; `maths-court` 2/2; `terrible-advice` 1/1; +1 more | Parallelogram, trapezium, prism (new-shapes), triangle area and cuboid volume (formula-plug-in, 10). No cylinder items. |
| G17.1 | s | know the formulae: circumference of a circle = 2πr = πd, area of a circle = πr2; calcula… | **THIN** | `spot-the-error` 5/5; `spot-the-muppet` 3/3; `terrible-advice` 3/3; `maths-court` 3/3; `estimation-golf` 1/1; `wrong-on-the-internet` 1/1 |  |
| G17.2 | u | ; surface area and volume of spheres, pyramids, cones and composite solids | **GAP** | — |  |
| G18.1 | u | calculate arc lengths, angles and areas of sectors of circles | **GAP** | — |  |
| G19.1 | u | apply the concepts of congruence and similarity, including the relationships between len… | **COVERED** | `scale-factor-scaling` 46/28; `spot-the-error` 1/0 |  |
| G19.3 | u | † in similar figures | **COVERED** | `scale-factor-scaling` 46/28 |  |
| G20.1 | u | know the formulae for: Pythagoras’ theorem, a2 + b2 = c2, and the trigonometric ratios, | **COVERED** | `trig-worms` 274/274; `spot-the-error` 1/1; `spot-the-muppet` 1/1; `terrible-advice` 1/1; `wrong-on-the-internet` 1/1; `maths-court` 1/1 | The trigonometric half only. Pythagoras has no dedicated practice: 5 diagnostic items are attributed here, and 4 coordinate-geometry distance/hypotenuse items sit under G11.1. |
| G20.2 | s | sinθ = oppositehypotenuse , cosθ = adjacenthypotenuse | **COVERED** | `trig-worms` 274/274 |  |
| G20.3 | u | † and | **COVERED** | follows G20.1 |  |
| G20.4 | s | tanθ = oppositeadjacent | **COVERED** | `trig-worms` 274/274 |  |
| G20.5 | u | ; apply them to find angles and lengths in right-angled triangles | **COVERED** | `trig-worms` 274/274; `spot-the-error` 3/3; `spot-the-muppet` 1/1; `terrible-advice` 1/1 | Right-angled triangles; tan is never used to find a side. |
| G20.7 | u | † in two | **COVERED** | `trig-worms` 274/274 |  |
| G20.9 | u | † dimensional figures | **COVERED** | `trig-worms` 274/274 |  |
| G21.1 | u | know the exact values of sinθ and cosθ for θ = 00, 300, 450 , 600 and 900; know the exac… | **COVERED** | `trig-identity-duel` 12/12 |  |
| G24.1 | s | describe translations as 2D vectors | **THIN** | `component-crusher` 1/1 |  |
| G25.1 | u | apply addition and subtraction of vectors, multiplication of vectors by a scalar, and di… | **THIN** | `component-crusher` 15/5; `spot-the-error` 2/0; `spot-the-muppet` 1/0; `terrible-advice` 1/0; `wrong-on-the-internet` 1/0; `maths-court` 1/0 |  |

### Probability

| Part | Type | DfE wording (as split in the file) | Verdict | Evidence (game n/F) | Sub-skill note |
|---|---|---|---|---|---|
| P1.1 | s | record describe and analyse the frequency of outcomes of probability experiments using t… | **GAP** | — |  |
| P2.1 | s | apply ideas of randomness, fairness and equally likely events to calculate expected outc… | **COVERED** | `expected-damage` 50/15; `core-maths-paper2b` 1/1 | Expected value of two "tracks" (KS3 tier). No "expected number of heads in 100 flips". |
| P3.1 | s | relate relative expected frequencies to theoretical probability, using appropriate langu… | **COVERED** | `probability-pioneer` 25/25 |  |
| P4.1 | s | apply the property that the probabilities of an exhaustive set of outcomes sum to one; a… | **THIN** | `probability-pioneer` 7/7; `probability-paradox` 2/2; `core-maths-paper2b` 1/1 |  |
| P5.1 | u | understand that empirical unbiased samples tend towards theoretical probability distribu… | **GAP** | — |  |
| P6.1 | s | enumerate sets and combinations of sets systematically, using tables, grids, Venn | **COVERED** | `given-that` 25/25 | Reads probabilities from tables/Venn/trees. Constructing the diagram is not asked. |
| P6.2 | u | diagrams and tree diagrams | **COVERED** | `given-that` 25/25; `core-maths-paper2b` 1/1 | Same as P6.1. |
| P7.1 | s | construct theoretical possibility spaces for single and combined experiments with equall… | **COVERED** | `probability-pioneer` 20/20; `wrong-on-the-internet` 4/4; `spot-the-error` 3/3; `spot-the-muppet` 3/3; `terrible-advice` 3/3; `maths-court` 1/1; +1 more |  |
| P8.1 | u | calculate the probability of independent and dependent combined events, including using … | **THIN** | `wrong-on-the-internet` 5/5; `spot-the-error` 4/4; `spot-the-muppet` 3/3; `terrible-advice` 3/3; `maths-court` 3/3; `probability-paradox` 2/2; +1 more |  |

### Statistics

| Part | Type | DfE wording (as split in the file) | Verdict | Evidence (game n/F) | Sub-skill note |
|---|---|---|---|---|---|
| S1.1 | u | infer properties of populations or distributions from a sample, whilst knowing the limit… | **THIN** | `core-maths-paper1` 2/2 |  |
| S2.1 | s | interpret and construct tables, charts and diagrams, including frequency tables, bar cha… | **GAP** | — |  |
| S2.2 | u | ungrouped discrete numerical data, tables and line graphs for time series data and | **GAP** | — |  |
| S2.3 | s | know their appropriate use | **GAP** | — |  |
| S4.1 | s | interpret, analyse and compare the distributions of data sets from univariate empirical … | **COVERED** | `chart-interrogator` 10/10 | Stem-and-leaf comparison only. |
| S4.3 | s |  appropriate measures of central tendency (median, mean, mode and modal class) and spre… | **COVERED** | `distinctly-average` 398/398; `stat-attack` 12/12; `spot-the-error` 3/3; `core-maths-paper1` 3/3; `spot-the-muppet` 3/2; `terrible-advice` 3/2; +2 more | Mean, median, mode, range, outliers, frequency tables, modal class and median class of grouped data. |
| S5.1 | s | apply statistics to describe a population | **GAP** | — |  |
| S6.1 | s | use and interpret scatter graphs of bivariate data; recognise correlation and know | **THIN** | `wrong-on-the-internet` 3/3; `core-maths-paper2a` 3/3; `spot-the-muppet` 2/2; `terrible-advice` 2/2; `maths-court` 2/2; `regression-rumble` 12/0 |  |
| S6.2 | u | that it does not indicate causation; draw estimated lines of best fit; make predictions;… | **COVERED** | `correlation-or-coincidence` 13/13; `wrong-on-the-internet` 3/3; `core-maths-paper2a` 3/3; `spot-the-muppet` 2/2; `terrible-advice` 2/2; `maths-court` 2/2; +2 more | Correlation vs causation as interpretation. No scatter graph is drawn or fitted. |

## 4. Evidence by game

One block per game. For each record: the part(s) it addresses, the tier(s) where the items live, how many items address it, how many of those are Foundation-pitched, the pitch, three quoted items, and one line of reasoning. `beyond Foundation` marks a quoted item that is *not* counted as Foundation-pitched. Parts marked (bold) are not Foundation parts; the record is kept so the count is visible.

### `angle-ace` — Angle Ace (Year 6, KS3, GCSE)

- **G3.1** · tiers: Year 6 (40), GCSE (35) · **75** items, **75** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Find angle x, then name the reason: angles on a line/at a point, vertically opposite, alternate/corresponding/co-interior, triangle sum, isosceles base angles, exterior angle. Foundation demand throughout.
  - Covers: angle facts, parallel-line angles, triangle sum. no polygon angle-sum items (two items use the exterior angle of a triangle)
  - `[year6] Find angle x -> 140 because: Angles on a straight line sum to 180°`
  - `[year6] What type of angle pair is this? -> Alternate angles (equal) because: Alternate angles are equal`
  - `[gcse] Three angles on a straight line. Find x. -> 90 because: Angles on a straight line sum to 180°`

### `bearing-blitz` — Bearing Blitz (GCSE)

- **G15.1** · tiers: GCSE label · **24** items, **24** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: generateBearings() read from source; the 16 fixed values are all multiples of 15 or 30. The task is estimating a bearing by eye on a compass, not measuring one with a protractor, not calculating a back bearing, and no map/scale drawing. Foundation-level content, thin form.
  - Covers: three-figure bearings read by eye
  - `round = 16 fixed bearings (000, 030, 045, 060, 090, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330) + 8 random 0-359`
  - `the student sets a three-figure bearing on a compass by eye and fires`
  - `score is by closeness of the setting`

### `better-value` — Better Value (GCSE, Core)

- **R11.1** · tiers: GCSE (20); Core (50) excluded · **20** items, **18** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Best-buy comparisons by cost per unit (direct 8, rate 5), hidden extra costs such as delivery and warranty (5) and two break-even equation problems. Foundation demand except the break-even items.
  - Covers: unit pricing and best value; no per-100g conversion tables
  - `Two pizza deals for a school party. Pizza Palace: £8 per pizza. Slice House: 3 pizzas for £21. The school needs 9 pizzas.`
  - `Two car parks near school. Car Park A charges £6 for 4 hours. Car Park B charges £8 for 6 hours.`
  - `[beyond Foundation] A reusable water bottle costs £15. Buying bottled water costs £1 per bottle. How many bottles of water must you drink for the reus`

### `chart-interrogator` — Chart Interrogator (GCSE, A-Level, Core, L4)

- **S4.1** · tiers: GCSE label (shared bank STEM_LEAF, 10 of 40) · **10** items, **10** Foundation-pitched · **YES** · mode: interpretive
  - Reasoning: Back-to-back stem-and-leaf diagrams of two classes (16 values each): read both, then a structured comparison. Stem-and-leaf is Foundation-assessable content under S4.1 "appropriate graphical representation"; the other 30 scenarios (box plots, histograms, cumulative frequency) are bold/Higher.
  - Covers: reading and comparing two distributions from a stem-and-leaf diagram (two-phase game)
  - `Maths test scores (out of 60): Class A [12, 15, 18, 22, 25].. vs Class B [18, 21, 24, 27, 29]..`
  - `Reaction times (ms): Under 25s [180, 195, 210, 220, 230].. vs Over 25s [220, 235, 250, 260, 265]..`
  - `Assembly times (seconds): Line A [42, 44, 46, 48, 50].. vs Line B [38, 40, 44, 46, 50]..`

### `component-crusher` — Component Crusher (GCSE, A-Level, L4)

- **G25.1** · tiers: GCSE (15); A-Level (15), L4 (15) excluded · **15** items, **5** Foundation-pitched · **MIXED** · mode: procedural
  - Reasoning: 15 GCSE vector scenarios, each with 2-4 sub-questions: column vectors, a + b, scalar multiples and path cancellation (5 scenarios) are in range; magnitude to 2 d.p., unit vectors, collinearity, parallel, position vectors and midpoints (10) are not.
  - Covers: column vectors, addition, scalar multiples
  - `Two vectors from the origin: Write down vector \mathbf{a} as a column vector. / Find \|\mathbf{a}\|.`
  - `Path cancellation: Total displacement = \mathbf{a} + \mathbf{b} + (-\mathbf{a}) / Explain why the total equals \mathbf{b}.`
  - `[beyond Foundation] Pythagorean triple: Find \|\mathbf{p}\|. / Find \frac{1}{2}\mathbf{p}.`
- **G24.1** · tiers: GCSE tier · **1** items, **1** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: "Write down the column vector of the translation shown", then the reverse translation.
  - Covers: translation as a column vector, one scenario
  - `Translation vector: Write down the column vector of the translation shown. / The arrow shows a translation. What translation takes the arrowhead ba`

### `constructions-lab` — Constructions Lab (KS3, GCSE)

- **G2.1** · tiers: KS3, GCSE labels (one shared bank TASKS, 10) · **10** items, **10** Foundation-pitched · **YES** · mode: constructive
  - Reasoning: Ten interactive ruler-and-compass tasks: perpendicular bisector, angle bisector, perpendicular from/at a point, 60 degrees, equilateral triangle and four loci. Each is a full construction, not a multiple-choice item, and all sit inside the underlined G2.1 wording.
  - Covers: standard constructions and loci. The "shortest distance from a point to a line" fact is not tested separately
  - `task: Perpendicular Bisector`
  - `task: 60° Angle`
  - `task: Locus: Fixed Distance from a Line`

### `coordinate-geometry-dash` — Coordinate Geometry Dash (GCSE, A-Level)

- **A10.1** · tiers: GCSE label (shared bank Q_GCSE 24); Q_ALEVEL 21 excluded · **6** items, **6** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Gradient from two points (positive, negative, zero, vertical) and an x-intercept. Foundation grade 4-5 demand.
  - Covers: gradient and intercept from points/equation
  - `A = (1, 2) and B = (5, 6) \| Find the gradient of AB -> 1`
  - `A = (−2, 4) and B = (4, 1) \| Gradient of AB? -> −1/2`
  - `A line has equation y = −2x + 3 \| Find the x-intercept -> (3/2, 0)`
- **A9.4** · tiers: GCSE label (Q_GCSE) · **4** items, **4** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Equation of a line from a point and gradient, or two points. Foundation-assessable (underlined); grade 5 demand.
  - Covers: equation of a straight line
  - `Line through (1, 1) with gradient 2 \| Find the equation -> y = 2x − 1`
  - `Find the equation of the line through (1, 2) and (3, 8) \| y = ? -> y = 3x − 1`
  - `Which line is shown? \| The line passes through (0, 2) and (4, 4) -> y = ½x + 2`
- **A9.2** · tiers: GCSE label (Q_GCSE) · **1** items, **1** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Parallel lines from y = mx + c.
  - Covers: parallel lines only (perpendicular is bold A9.3)
  - `Line A: y = 2x + 1. Line B: y = 2x − 3 \| What is the relationship? -> Parallel`
- **G11.1** · tiers: GCSE label (Q_GCSE) · **8** items, **6** Foundation-pitched · **MIXED** · mode: procedural
  - Reasoning: Midpoint (3), distance/hypotenuse by Pythagoras (4) and collinearity. The 5 root-2 distance and the collinearity item are beyond Foundation.
  - Covers: midpoint and distance on coordinate axes
  - `A = (2, 3) and B = (6, 7) \| Find the midpoint of AB -> (4, 5)`
  - `Right triangle with vertices (1,1), (5,1), (5,4) \| Find the length of the hypotenuse -> 5`
  - `[beyond Foundation] A = (1, 2), B = (3, 4), C = (5, 6) \| Are A, B, C collinear? -> Yes — all on y = x + 1`
- **A19.3** · tiers: GCSE label (Q_GCSE) · **2** items, **2** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Intersection of two straight lines by solving simultaneously.
  - Covers: intersection of two lines
  - `Line 1: y = x + 1. Line 2: y = −x + 5 \| Find the intersection point -> (2, 3)`
  - `Line 1: y = 2x − 1. Line 2: y = ½x + 2 \| Intersection? -> (2, 3)`

### `core-maths-paper1` — Core Maths Paper 1 Practice (Core)

- **R9.1** · tiers: Core label (shared bank QUESTIONS, 36 per paper) · **8** items, **7** Foundation-pitched · **MIXED** · mode: interpretive
  - Reasoning: Core Maths exam-style multiple choice: Level 3 wording and multi-step contexts, but the underlying skill is Foundation content. Simple interest, income tax, VAT, reverse percentage, 10% of pay, NI, student loan, comparing 2.1% with 3.4%.
  - Covers: percentage of an amount in money contexts; original-value (1 item); percentage comparison
  - `[3.2] £2,500 is invested at 3% simple interest per year. What is the total interest earned after 4 years?`
  - `[3.2] A worker's salary increases by 2.1%. RPI inflation the same year is 3.4%. Which statement best describes the effect on t`
  - `[beyond Foundation] [3.2] Student loan repayments are 9% of earnings above £27,295. A graduate earns £28,000. How much do they repay in the first `
- **R16.1** · tiers: Core label (shared bank QUESTIONS, 36 per paper) · **1** items, **1** Foundation-pitched · **YES** · mode: interpretive
  - Reasoning: Core Maths exam-style multiple choice: Level 3 wording and multi-step contexts, but the underlying skill is Foundation content. Two years of compound interest.
  - Covers: compound interest, one item
  - `[3.2] £6,000 is invested for 2 years at 4% compound interest per annum. What is the value at the end of 2 years?`
- **N15.2** · tiers: Core label (shared bank QUESTIONS, 36 per paper) · **1** items, **1** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Core Maths exam-style multiple choice: Level 3 wording and multi-step contexts, but the underlying skill is Foundation content. "A length is measured as 8.4 cm to 1 d.p. - what is the error interval?".
  - Covers: error interval from rounding, one item
  - `[3.2] A length is measured as 8.4 cm, rounded to 1 decimal place. What is the error interval for the true length l?`
- **S4.3** · tiers: Core label (shared bank QUESTIONS, 36 per paper) · **3** items, **3** Foundation-pitched · **YES** · mode: interpretive
  - Reasoning: Core Maths exam-style multiple choice: Level 3 wording and multi-step contexts, but the underlying skill is Foundation content. Estimated mean from a grouped table, mean vs median with an outlier (salaries), effect of removing an outlier.
  - Covers: averages and outliers in context
  - `[3.1] The table shows the number of hours per week 40 adults spend exercising. What is the estimated mean?`
  - `[3.1] The annual salaries of 5 employees are: £22,000, £24,000, £26,000, £28,000, £85,000. A recruitment advert states "Averag`
  - `[3.1] Reaction times (ms) for 8 people: 210, 215, 218, 222, 225, 229, 234, 614. Mean = 270.9 ms. A researcher considers removi`
- **S1.1** · tiers: Core label (shared bank QUESTIONS, 36 per paper) · **2** items, **2** Foundation-pitched · **YES** · mode: interpretive
  - Reasoning: Core Maths exam-style multiple choice: Level 3 wording and multi-step contexts, but the underlying skill is Foundation content. Spotting a biased sample (first 40 outside a cinema; students at the library).
  - Covers: limitations of sampling, 2 items
  - `[3.1] A journalist surveys the first 40 people outside a cinema on a Saturday afternoon to find out how much TV people watch. `
  - `[3.1] A school wants to survey students about a new homework policy. The head teacher proposes asking students who visit the l`
- **S6.2** · tiers: Core label (shared bank QUESTIONS, 36 per paper) · **1** items, **1** Foundation-pitched · **YES** · mode: interpretive
  - Reasoning: Core Maths exam-style multiple choice: Level 3 wording and multi-step contexts, but the underlying skill is Foundation content. Breakfast and income: correlation is not causation.
  - Covers: causation vs correlation, one item
  - `[3.1] A survey of 500 people finds that those who eat breakfast earn on average £4,200 more per year. A blogger concludes "Eat`

### `core-maths-paper2a` — Core Maths Paper 2A Practice (Core)

- **R9.1** · tiers: Core label (shared bank QUESTIONS, 36 per paper) · **3** items, **3** Foundation-pitched · **YES** · mode: interpretive
  - Reasoning: Core Maths exam-style multiple choice: Level 3 wording and multi-step contexts, but the underlying skill is Foundation content. What a 200% rise means, a x1.2 multiplier in a spreadsheet, a pass rate rising 78% to 81%.
  - Covers: percentage change interpretation
  - `[3.4] A newspaper headline states: "House prices have risen 200% in 20 years." A homeowner paid £80,000 for a house 20 years a`
  - `[3.4] A spreadsheet cell B3 contains the value 450. Cell C3 contains the formula =B3*1.2. What does C3 calculate?`
  - `[3.4] A school reports that its GCSE pass rate improved from 78% to 81% over two years, while the national average stayed at 7`
- **S6.1, S6.2** · tiers: Core label (shared bank QUESTIONS, 36 per paper) · **3** items, **3** Foundation-pitched · **YES** · mode: interpretive
  - Reasoning: Core Maths exam-style multiple choice: Level 3 wording and multi-step contexts, but the underlying skill is Foundation content. Describe r = -0.87, predict from y = 2.8x + 5.3, ice cream sales vs drownings.
  - Covers: interpreting correlation and using a regression line to predict
  - `[3.7] The PMCC for a dataset is calculated as r = −0.87. Which statement best describes this value?`
  - `[3.7] A regression line ŷ = 2.8x + 5.3 is fitted to data where x ranges from 10 to 50. Estimate the value of y when x = 25.`
  - `[3.7] A student calculates r = 0.93 between the number of ice creams sold and the number of drownings per month. Which conclus`

### `core-maths-paper2b` — Core Maths Paper 2B Practice (Core)

- **P4.1** · tiers: Core label (shared bank QUESTIONS, 36 per paper) · **1** items, **1** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Core Maths exam-style multiple choice: Level 3 wording and multi-step contexts, but the underlying skill is Foundation content. P(not red) from 4 red, 3 blue, 5 green.
  - Covers: complement of an event, one item
  - `[3.9] A bag contains 4 red, 3 blue, and 5 green balls. What is the probability of drawing a ball that is not red?`
- **P8.1** · tiers: Core label (shared bank QUESTIONS, 36 per paper) · **1** items, **1** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Core Maths exam-style multiple choice: Level 3 wording and multi-step contexts, but the underlying skill is Foundation content. P(A and B) for independent events.
  - Covers: independent events, one item
  - `[3.9] Events A and B are independent. P(A) = 0.4 and P(B) = 0.3. What is P(A ∩ B)?`
- **P7.1** · tiers: Core label (shared bank QUESTIONS, 36 per paper) · **1** items, **1** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Core Maths exam-style multiple choice: Level 3 wording and multi-step contexts, but the underlying skill is Foundation content. Two dice, total 7.
  - Covers: possibility space of two dice, one item
  - `[3.9] Two fair dice are rolled. What is the probability that the total is 7?`
- **P6.2** · tiers: Core label (shared bank QUESTIONS, 36 per paper) · **1** items, **1** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Core Maths exam-style multiple choice: Level 3 wording and multi-step contexts, but the underlying skill is Foundation content. Venn counting: French, Spanish, both.
  - Covers: Venn counting, one item
  - `[3.9] In a class of 30 students, 18 study French, 12 study Spanish, and 6 study both. How many students study neither language`
- **P2.1** · tiers: Core label (shared bank QUESTIONS, 36 per paper) · **1** items, **1** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Core Maths exam-style multiple choice: Level 3 wording and multi-step contexts, but the underlying skill is Foundation content. 2% fault rate, 200 items: expected faulty.
  - Covers: expected number = n x p, one item
  - `[3.9] A factory has a 2% fault rate. A batch of 200 items is produced. How many items are expected to be faulty?`

### `core-maths-paper2c` — Core Maths Paper 2C Practice (Core)

- **A10.1** · tiers: Core label (shared bank QUESTIONS, 36 per paper) · **1** items, **1** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Core Maths exam-style multiple choice: Level 3 wording and multi-step contexts, but the underlying skill is Foundation content. Gradient through (2,5) and (6,13).
  - Covers: gradient from two points, one item
  - `[3.12] A straight line passes through (2, 5) and (6, 13). What is its gradient?`
- **R14.1** · tiers: Core label (shared bank QUESTIONS, 36 per paper) · **2** items, **2** Foundation-pitched · **YES** · mode: interpretive
  - Reasoning: Core Maths exam-style multiple choice: Level 3 wording and multi-step contexts, but the underlying skill is Foundation content. Gradient of a distance-time line as speed; horizontal v-t line as zero acceleration.
  - Covers: gradient as rate of change
  - `[3.12] A distance–time graph is a straight line from (0, 0) to (4, 100). What does the gradient of this line represent?`
  - `[3.12] A velocity–time graph shows a horizontal line at 15 m/s from t = 0 to t = 8. What is the acceleration?`
- **A19.3** · tiers: Core label (shared bank QUESTIONS, 36 per paper) · **1** items, **1** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Core Maths exam-style multiple choice: Level 3 wording and multi-step contexts, but the underlying skill is Foundation content. Intersection of y = 3x - 2 and y = -x + 6.
  - Covers: intersection of two lines, one item
  - `[3.11] Find the x-coordinate of the intersection of y = 3x − 2 and y = −x + 6.`
- **A14.4** · tiers: Core label (shared bank QUESTIONS) · **4** items, **4** Foundation-pitched · **YES** · mode: interpretive
  - Reasoning: Core Maths exam-style: distance-time and velocity-time graphs (speed as gradient, acceleration, distance travelled). Foundation content in Level 3 wording.
  - Covers: simple kinematic graph reading
  - `[3.4] A velocity–time graph shows a straight line from (0, 0) to (5, 30). A student says: "The acceleration is 6 m/s²." Is thi`
  - `[3.12] A velocity–time graph shows a horizontal line at 15 m/s from t = 0 to t = 8. What is the acceleration?`
  - `[3.12] A velocity–time graph shows a straight line from (0, 8) to (5, 28). What is the distance travelled?`

### `correlation-or-coincidence` — Correlation or Coincidence (GCSE, A-Level, Core)

- **S6.2** · tiers: GCSE, A-Level, Core labels (shared bank QUESTIONS, 13) · **13** items, **13** Foundation-pitched · **YES** · mode: interpretive
  - Reasoning: Given two variables and a correlation coefficient, decide whether the link is real or a coincidence (cheese consumption vs bedsheet strangling, r = 0.95). Foundation uses qualitative correlation; the r value is given, never calculated. Same 13 items are served at GCSE, A-Level and Core labels.
  - Covers: correlation does not imply causation. No scatter graph is drawn, no line of best fit
  - `spurious: Nicolas Cage films released per year vs Swimming pool drownings per year, r = 0.87`
  - `real: Hours of study per week vs Exam score (%), r = 0.97`
  - `spurious: Renewable energy capacity (GW) vs Number of pirates globally (thousands), r = 0.85`

### `decimal-detective` — Decimal Detective (Year 6)

- **N1.1** · tiers: Year 6 (shared bank LINEUP_QUESTIONS) · **15** items, **15** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Order 5 decimals with 1-3 dp (0.3, 0.03, 3.0, 0.33, 0.303). Foundation grade 2-3 place-value demand.
  - Covers: ordering decimals only
  - `0.3 \| 0.03 \| 3.0 \| 0.33 \| 0.303 \| 0.03 \| 0.3 \| 0.303 \| 0.33 \| 3.0`
  - `5.2 \| 5.02 \| 5.22 \| 5.202 \| 5.022 \| 5.02 \| 5.022 \| 5.2 \| 5.202 \| 5.22`
  - `0.4 \| 0.44 \| 0.404 \| 0.044 \| 0.440 \| 0.044 \| 0.4 \| 0.404 \| 0.44 \| 0.440`
- **N15.1** · tiers: Year 6 (shared bank ROUNDUP_QUESTIONS) · **15** items, **15** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Round to nearest tenth/whole/2dp/1sf with the unrounded value shown among the options. Foundation grade 2-4 demand.
  - Covers: rounding to dp and 1 s.f.; no error intervals
  - `value=3.74 \| instruction=Round to the nearest tenth \| answer=3.7 \| 3.7 \| 3.8 \| 3.74 \| 4.0`
  - `value=9.50 \| instruction=Round to the nearest whole number \| answer=10 \| 9 \| 10 \| 9.5 \| 9.50`
  - `value=12.8 \| instruction=Round to 1 significant figure \| answer=10 \| 10 \| 13 \| 12 \| 12.8`

### `distinctly-average` — Distinctly Average (KS3, GCSE)

- **S4.3** · tiers: KS3 (259), GCSE (398, superset) · **398** items, **398** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: DA_ITEMS read live: KS3 pool 259, GCSE pool 398 (the KS3 pool plus 139 GCSE-only items). Categories: mean 73, median 58, range 53, mode (unique 33, bimodal 42); GCSE adds frequency-table mean 20 and median 20, compare means 18 and ranges 18, outliers 48, missing value 15. All whole-number data, 5 to 11 values. Foundation demand.
  - Covers: mean, median, mode, range, outliers on ungrouped data; frequency-table mean and median. Modal class and grouped data are not in this game
  - `mean: data [5, 9, 7, 7, 7] -> 7 (distractors tagged sum_not_divided, value_not_mean ...)`
  - `median: unsorted data set, KS3 whole numbers 1-20; a stepped scaffold that fades`
  - `gcse: compareRange "which set is more consistent" / outlierMean / missing-value from the mean`

### `equation-builder` — Equation Builder (KS3, GCSE, L4)

- **A21.1** · tiers: KS3 (40), GCSE (40); L4 (40) excluded · **80** items, **60** Foundation-pitched · **MIXED** · mode: constructive
  - Reasoning: Build an expression, formula or equation from a word problem by slotting tiles. All 40 KS3 items and the Foundation-content GCSE topics (reverse percentage, simultaneous, right-angled trig, speed) are in range; the GCSE items on cosine rule, circle theorems, vectors, bounds, functions and the quadratic formula are not.
  - Covers: translating a situation into an expression/equation. It does not ask the student to solve or interpret, which A21.1 also names
  - `[ks3/Forming Equations] A taxi company charges a fixed booking fee of £3 plus £2.50 for every mile of the journey. A customer wants to`
  - `[gcse/Forming Equations] A cinema: 3 adult tickets and 5 child tickets cost £45. Write the first equation using a = adult price, c = ch`
  - `[beyond Foundation] [gcse/Quadratics] A path of uniform width x metres surrounds a rectangular garden 14 m by 10 m. The total area including path is`

### `estimation-engine` — Estimation Engine (KS3, GCSE, Core)

- **N14.1** · tiers: KS3, GCSE, Core labels, one shared bank QUESTIONS · **49** items, **32** Foundation-pitched · **MIXED** · mode: procedural
  - Reasoning: First 32 are whole-number mental arithmetic answered within a tolerance; the last 17 use e, pi, phi, ln and log which are A-level/calculator content. It rewards a close answer, not the round-to-1-s.f. method Foundation papers test.
  - Covers: approximate answers within a tolerance; not rounding-to-1-s.f. estimation
  - `expr=12 × 15 \| ans=180 \| tol=5 \| time=30`
  - `expr=∛125000 \| ans=50 \| tol=2 \| time=30`
  - `[beyond Foundation] expr=e × π \| ans=8.54 \| tol=3 \| time=30`
- **N6.1** · tiers: shared bank QUESTIONS · **19** items, **13** Foundation-pitched · **MIXED** · mode: procedural
  - Reasoning: Square/cube roots and powers, but √1,764, √5041, √9801 and ∛125000 need recall or a calculator; 2¹⁰, 3¹⁰ likewise.
  - Covers: squares/cubes/roots/powers as operands in an estimate
  - `expr=√400 \| ans=20 \| tol=1 \| time=30`
  - `expr=3¹⁰ \| ans=59049 \| tol=3 \| time=30`
  - `[beyond Foundation] expr=φ² \| ans=2.618 \| tol=3 \| time=30`

### `estimation-golf` — Estimation Golf (Year 6, KS3, GCSE, A-Level, L4, Core)

- **N14.1** · tiers: KS3 (9), GCSE (9); Year 6 (20) excluded · **18** items, **17** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Two 9-hole rounds (KS3, GCSE) of short real-world estimates: seconds in a day, 15% of 200, area of a 7 x 9 rectangle, 75 mph to km/h, recipe scaling. All are Foundation-level except the 8-digit heartbeats-in-a-year item. Scored on proximity, so it rewards an approximate answer, not the round-to-1-s.f. method.
  - Covers: estimating and approximating in context. The Year 6 round (20 items) is general-knowledge recall (days in a year) and is not counted
  - `Round 3,847 to the nearest hundred. -> 3800`
  - `A factory makes 840 items per hour. Estimate output over a 7.5-hour shift. -> 6300`
  - `[beyond Foundation] Estimate the number of heartbeats in a year (assume 70 bpm). -> 36792000`
- **N15.1** · tiers: KS3 (1), GCSE (1) · **2** items, **2** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: "Round 3,847 to the nearest hundred" and "Round 0.004857 to 2 significant figures".
  - Covers: rounding to a place value and to s.f., 2 items
  - `Round 3,847 to the nearest hundred. -> 3800`
  - `Round 0.004857 to 2 significant figures. -> 0.0049`
- **G17.1** · tiers: GCSE (1) · **1** items, **1** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: One item: area of a circle of radius 7 cm with pi = 3.14.
  - Covers: area of a circle, 1 item
  - `Estimate the area of a circle with radius 7 cm. (π ≈ 3.14) -> 153.86`

### `expected-damage` — Expected Damage (KS3, GCSE, Core)

- **P2.1** · tiers: KS3 (15), GCSE (20), Core (15) · **50** items, **15** Foundation-pitched · **MIXED** · mode: procedural
  - Reasoning: Choose between two "tracks" by expected value: sum of (muppets x probability), e.g. 12 x 0.25 = 3 vs a certain 2. The KS3 tier (15) is a single multiplication; GCSE and Core tiers use several outcomes or word problems and are expected-value (Core Maths S3.9), not Foundation expected frequency.
  - Covers: expected outcome as number x probability, once; no "expected number of heads in 100 flips"
  - `[ks3] A=3 vs B outcomes=[(8, 0.5), (0, 0.5)] -> higher EV: B`
  - `[ks3] A=8 vs B outcomes=[(4, 0.9), (0, 0.1)] -> higher EV: A`
  - `[beyond Foundation] [gcse] A=4 vs B outcomes=[(12, 0.3333333333333333), (0, 0.6666666666666666)] -> higher EV: A`

### `factor-race` — Factor Race (Year 6, KS3, GCSE)

- **N4.1** · tiers: Year 6/KS3/GCSE labels, one shared bank YEAR6_BANK · **20** items, **20** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Compare the number of factors of two numbers up to 50. Below Foundation numeracy demand but the vocabulary (factor) is N4.
  - Covers: factors only
  - `which has more factors: 12 or 8?`
  - `which has more factors: 6 or 4?`
  - `which has more factors: 42 or 35?`

### `fermi-lab` — Fermi Lab (KS3, GCSE, A-Level, L4, Core)

- **N14.1** · tiers: KS3 (12), GCSE (15); Core (15) excluded · **27** items, **0** Foundation-pitched · **NO** · mode: interpretive
  - Reasoning: Fermi chains ("How many piano tuners are there in London?") estimate real-world quantities from stated assumptions. That is estimation in the everyday sense, not the DfE skill of checking a calculation by rounding, and the chains have 4-6 steps with population-scale figures. Counted as THIN evidence at most.
  - Covers: order-of-magnitude reasoning; not rounding to 1 s.f.
  - `[beyond Foundation] How many classrooms are there in UK schools?`
  - `[beyond Foundation] How many piano tuners are there in London?`
  - `[beyond Foundation] How many photos are taken in the UK each day?`

### `formula-forge` — Formula Forge (GCSE, A-Level, L4)

- **A5.1** · tiers: GCSE label (29 of 74 in the bank); A-Level and L4 tiers excluded · **29** items, **15** Foundation-pitched · **MIXED** · mode: procedural
  - Reasoning: Stage 1-2 items (v = u + at, A = bh, y = mx + c, P = 2(l + w)) are in range; stage 3-4 put the subject inside a power, root or on both sides (v^2 = u^2 + 2as, T = 2 pi sqrt(l/g), ax + b = cx + d).
  - Covers: changing the subject of a formula
  - `v = u + at, subject u -> u = v - at`
  - `s = \dfrac{d}{t}, subject t -> t = \dfrac{d}{s}`
  - `[beyond Foundation] s = ut + \dfrac{1}{2}at^2, subject a -> a = \dfrac{2(s - ut)}{t^2}`

### `formula-plug-in` — Formula Plug-In (Year 6)

- **A2.1** · tiers: Year 6 (one shared bank QUESTIONS, 50) · **50** items, **50** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Substitute whole numbers into area, perimeter, speed, distance, cost and volume formulae (A = l x w, P = 2(l + w), S = D / T). Foundation grade 2-3 demand, one formula per question.
  - Covers: substituting into simple formulae
  - `Area of a rectangle: A = l \times w, l=6, w=4 -> 24`
  - `Distance: D = S \times T, S=25, T=6 -> 150`
  - `Mean: \text{Mean} = \text{Sum} \div n, Sum=45, n=9 -> 5`
- **R11.1** · tiers: Year 6 (shared bank QUESTIONS) · **15** items, **15** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Speed, distance, time and unit-cost formulae with whole numbers (72 km in 8 h; 12 items at £5).
  - Covers: compound measures: speed and cost per item only; no density or pressure
  - `Speed: S = D \div T, D=60, T=3 -> 20`
  - `Distance: D = S \times T, S=30, T=5 -> 150`
  - `Cost: C = n \times p, n=9, p=8 -> 72`
- **G16.1** · tiers: Year 6 (shared bank QUESTIONS) · **10** items, **10** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: The 10 triangle-area and cuboid-volume items, formula shown, whole numbers. (Rectangle, square and perimeter items are lower than the part and are not counted here.)
  - Covers: area of a triangle, volume of a cuboid
  - `Area of a triangle: A = \tfrac{1}{2} \times b \times h, b=6, h=4 -> 12`
  - `Area of a triangle: A = \tfrac{1}{2} \times b \times h, b=7, h=4 -> 14`
  - `Volume of a cuboid: V = l \times w \times h, l=7, w=4, h=3 -> 84`

### `formula-unlocked` — Formula Unlocked (GCSE, A-Level, L4)

- **A5.1** · tiers: GCSE label (shared bank Q_GCSE, 29) · **29** items, **18** Foundation-pitched · **MIXED** · mode: procedural
  - Reasoning: Stages 1-2 (one and two inverse steps: u = v - at, h = 2A/b) are in range; stage 3 (pendulum, squared subjects) and stage 4 (subject on both sides) are Higher.
  - Covers: changing the subject of a formula
  - `stage 1: v = u + at, subject u -> u = v - at`
  - `stage 2: v^2 = u^2 + 2as, subject s -> s = \dfrac{v^2 - u^2}{2a}`
  - `[beyond Foundation] stage 3: v^2 = u^2 + 2as, subject v -> v = \sqrt{u^2 + 2as}`

### `four-quadrant-explorer` — Four Quadrant Explorer (Year 6)

- **A8.1** · tiers: Year 6 (shared banks PLOT 20, READ 15, SHAPE 10) · **45** items, **45** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Plot a point, read a point and complete a shape in all four quadrants, integer coordinates within +-5. Foundation grade 1-3 demand.
  - Covers: coordinates in four quadrants
  - `x=-3 \| y=4`
  - `x=-3 \| y=-4 \| (-3,-4) \| (3,4) \| (-4,-3) \| (3,-4) \| correct=0`
  - `-3 \| 1 \| 1 \| 1 \| 1 \| -3 \| -3 \| -3`

### `given-that` — Given That (GCSE, A-Level, Core, L4)

- **P6.1, P6.2** · tiers: GCSE label (25); A-Level, Core, L4 excluded · **25** items, **25** Foundation-pitched · **YES** · mode: interpretive
  - Reasoning: Phase 1 of each scenario reads a probability off a two-way table (12), a Venn diagram (8) or a tree of counts (5): "P(passed maths)" = 60/100. That is Foundation. Phase 2 of every scenario is conditional probability P(A|B), which is Higher and not counted here.
  - Covers: reading probabilities from tables, Venn diagrams and trees. Constructing the diagram is not asked
  - `[table] Students, revision class, maths pass/fail :: What is the probability a randomly chosen student passed maths? -> \tfrac{60}{100}`
  - `[tree] 200 coin flips, heads/tails, then win/lose game :: What is P(win the game)? -> \tfrac{110}{200}`
  - `[table] Students, year group, satisfaction :: What is P(rated canteen 'Poor')? -> \tfrac{95}{250}`

### `gradient-hunter` — Gradient Hunter (GCSE, Core, A-Level)

- **A10.1** · tiers: GCSE (15); Core (20), A-Level (10) excluded · **15** items, **7** Foundation-pitched · **MIXED** · mode: procedural
  - Reasoning: Seven of the 15 have a straight-line graph (speed from a distance-time graph, cost per mile); the eight with a smooth curve ask for a gradient between two points or a chord, which is Higher.
  - Covers: gradient of a straight line and its meaning as a rate
  - `[calculate/linear] A car travels along a motorway. Distance from the start is recorded every 30 minutes.`
  - `[reading/linear] A graph shows a car slowing down. The chord from (0, 30) to (6, 0) has gradient -5.`
  - `[beyond Foundation] [reading/smooth] A graph shows savings in a jar over weeks. The chord from (2, 10) to (10, 50) has gradient 5.`
- **R14.1** · tiers: GCSE (15) · **15** items, **7** Foundation-pitched · **MIXED** · mode: procedural
  - Reasoning: The straight-line items ask what the gradient means (mph, litres per minute), i.e. rate of change. The curve items ask for a chord gradient.
  - Covers: interpreting gradient as a rate of change
  - `[calculate/linear] A car travels along a motorway. Distance from the start is recorded every 30 minutes.`
  - `[reading/linear] A graph shows a car slowing down. The chord from (0, 30) to (6, 0) has gradient -5.`
  - `[beyond Foundation] [reading/smooth] A graph shows savings in a jar over weeks. The chord from (2, 10) to (10, 50) has gradient 5.`
- **A14.1, A14.4** · tiers: GCSE (15) · **15** items, **7** Foundation-pitched · **MIXED** · mode: procedural
  - Reasoning: All 15 are real-context graphs (distance-time, cost, volume drained, temperature) read for a gradient; the 7 straight-line ones are Foundation. Kinematic (distance, speed) graphs are the A14.4 examples.
  - Covers: reading and interpreting real-context graphs
  - `[calculate/linear] A car travels along a motorway. Distance from the start is recorded every 30 minutes.`
  - `[reading/linear] A graph shows a car slowing down. The chord from (0, 30) to (6, 0) has gradient -5.`
  - `[beyond Foundation] [reading/smooth] A graph shows savings in a jar over weeks. The chord from (2, 10) to (10, 50) has gradient 5.`

### `graph-sketcher` — Graph Sketcher (Core, A-Level, L4)

- **A12.1, A14.1** · tiers: Core (15); A-Level (15), L4 (15) excluded · **15** items, **8** Foundation-pitched · **MIXED** · mode: constructive
  - Reasoning: Complete a table of values, sketch the curve and read it in a real-world context. Quadratic and reciprocal contexts (h = 15t - 5t^2, t = 120/s) are Foundation-assessable; cubic, exponential and trig items are not, and the decimals (0.001s^2 + 0.04s) make several heavy.
  - Covers: tables of values and sketching quadratics/reciprocals; A12.3/A12.4 reciprocal only in 3 items
  - `Wave height h (m) vs wind speed s (mph).: h = 0.001s^2 + 0.04s`
  - `Pressure P (kPa) vs volume V (litres). Boyle's Law.: P = \frac{100}{V}`
  - `[beyond Foundation] Mass M (g) of a decaying substance, t = days.: M = 80 \times 0.85^t`
- **A12.2** · tiers: Core (15); A-Level, L4 excluded · **7** items, **7** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Cubics (profit P = x^3 - 6x^2 + 9x, open-box volume V = 4x^3 - 36x^2 + 80x) and reciprocals (C = 2000/n + 5, t = 120/s, P = 100/V) as table + sketch + interpret tasks in engineering/business contexts.
  - Covers: cubic and reciprocal graphs, real contexts (Core Maths wording)
  - `Profit P (£thousands) from selling x hundred items.: P = x^3 - 6x^2 + 9x`
  - `Journey time t (minutes) at average speed s (mph).: t = \frac{120}{s}`
  - `Pressure P (kPa) vs volume V (litres). Boyle's Law.: P = \frac{100}{V}`
- **A12.3, A12.4, A14.2** · tiers: Core (15) · **3** items, **3** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: The three reciprocal items (C = 2000/n + 5, t = 120/s, P = 100/V).
  - Covers: reciprocal graphs y = k/x with x not 0
  - `Average cost C (£) per item when producing n items.: C = \frac{2000}{n} + 5`
  - `Journey time t (minutes) at average speed s (mph).: t = \frac{120}{s}`
  - `Pressure P (kPa) vs volume V (litres). Boyle's Law.: P = \frac{100}{V}`

### `growth-and-decay` — Growth and Decay (Core, A-Level, L4)

- **R16.1** · tiers: Core (15); A-Level, L4 excluded · **15** items, **9** Foundation-pitched · **MIXED** · mode: procedural
  - Reasoning: Exponential models: multiplier form (500 x 1.08^t, 18000 x 0.82^t) is Foundation-assessable compound growth/decay; the e^(kt) models (drug concentration, cooling, real value) are A-level.
  - Covers: growth and decay from a given multiplier model; not setting the model up
  - `An online retailer's customer base grows exponentially. C = number of : C = 500 \times 1.08^t`
  - `Atmospheric pressure decreases with altitude. P = pressure (kPa), d = : P = k \times 0.96^d`
  - `[beyond Foundation] Radioactive decay — N = mass (g), t = days. Half-life is 1 day since e: N = k \times e^{-0.693t}`

### `index-laws` — Index Laws (GCSE, A-Level)

- **A4.9** · tiers: GCSE, A-Level labels; one bank QUESTIONS (45) · **31** items, **25** Foundation-pitched · **MIXED** · mode: procedural
  - Reasoning: Algebraic index-law items (x^3 x x^4, 6x^7 / 2x^2, (2x^2)^3, 7x^0, x^-3). Multiply, divide, power-of-power, zero and negative powers are Foundation-assessable; the items with a fractional exponent (x^(1/2), x^(3/2), (x^(1/2))^4) are the bold N7.2 and are not counted as Foundation-pitched.
  - Covers: laws of indices with integer powers on algebraic terms
  - `Multiply Rule: x^3 \times x^4 = x^7`
  - `Negative Power: 4x^{-1} = \dfrac{4}{x}`
  - `[beyond Foundation] Fractional Power: x^{\frac{1}{2}} = \sqrt{x}`
- **N7.1, N7.3, N6.1** · tiers: shared bank QUESTIONS · **14** items, **7** Foundation-pitched · **MIXED** · mode: procedural
  - Reasoning: Numeric-base items (3^4 x 3^2, 2^-4, 5^-2, 10^-3, (5^2)^3, 2^7/2^3). The fractional-power numerics (8^(1/3), 27^(2/3), 16^(3/4)) are bold N7.2 and are not counted.
  - Covers: integer indices on numbers; no roots as radicals
  - `Multiply Rule: 3^4 \times 3^2 = 3^6`
  - `Negative Power: 10^{-3} = \dfrac{1}{1000}`
  - `[beyond Foundation] Fractional Power: 25^{\frac{1}{2}} = 5`

### `like-terms-collector` — Like Terms Collector (Year 6)

- **A4.3** · tiers: Year 6 (shared banks STAGE2 10, STAGE3 30) · **40** items, **40** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Fruit-then-letters-then-full simplification: 3x + 2x + 4y + y, 5a + 3b - 2a + 4b, with subtraction and two or three letters. Foundation grade 2-4 demand.
  - Covers: collecting like terms only. No multiplying a single term over a bracket, no taking out common factors
  - `prompt=3x + 2x + 4y + y \| x \| y \| 5 \| 5`
  - `4m + 3n + 2m − n -> 6m + 2n`
  - `5a + 3a + 4b − 4b -> 8a`

### `linear-equation-solver` — Linear Equation Solver (GCSE)

- **A17.1** · tiers: GCSE label (bank gcse, 141) · **141** items, **141** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: 141 equations by choosing the inverse operation at each step: one- and two-step, negative, fractional, brackets, constant-first, unknown on the right. Foundation grade 2-4 demand.
  - Covers: linear equations with the unknown on ONE side (plus brackets). The bank has no unknown-on-both-sides shape, which A17.1 names explicitly
  - `[One-step · integer] x + 7 = 12 -> x = 5`
  - `[Two-step · integer] \frac{x}{4} - 9 = 1 -> x = 40`
  - `[Two-step · fractional] \frac{4}{5}x + 6 = 18 -> x = 15`

### `maths-court` — Maths Court (KS3, GCSE, Core)

- **N3.1** · tiers: ks3 (1), gcse (1) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/BIDMAS] Calculate 3 + 4 × 2`
  - `[gcse/BIDMAS] Calculate 18 ÷ (2 + 1) × 3²`
- **N2.1, N8.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Fractions] Which is larger: 3/5 or 5/8?`
- **R9.1** · tiers: ks3 (1), gcse (1) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Percentages] Find 35% of 60`
  - `[gcse/Reverse Percentage] A coat costs £68 after a 15% reduction. Find the original price.`
- **R5.1, R4.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Ratio] Share 84 in the ratio 3:4`
- **G16.1, G17.1** · tiers: ks3 (2) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Area] Find the area of a right-angled triangle with legs 6cm and 8cm`
  - `[ks3/Perimeter vs Area] A rectangle is 7cm by 4cm. Find the perimeter.`
- **A23.1, A25.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Sequences] What is the nth term of: 5, 8, 11, 14...?`
- **G3.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Angles] Find the missing angle in a triangle where two angles are 47° and 63°`
- **P7.1, P8.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Probability] A bag has 3 red and 5 blue balls. What is P(red)?`
- **S4.3** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Mean] Find the mean of: 4, 7, 3, 9, 2`
- **N2.1, N1.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Negative Numbers] Calculate −3 × −4`
- **N4.1** · tiers: ks3 (2) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/LCM] Find the LCM of 4 and 6`
  - `[ks3/Factors] List all the factors of 24`
- **A2.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Substitution] If a = 3 and b = −2, find 2a − b²`
- **N15.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Rounding] Round 3.456 to 2 decimal places`
- **A4.4, A4.6** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Algebra — Expanding] Expand and simplify (2x + 3)(x − 4)`
- **A19.1** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Simultaneous Equations] Solve: 3x + 2y = 16 and x − y = 2`
- **G20.1** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Pythagoras] A right triangle has legs 5cm and 12cm. Find the hypotenuse.`
- **P8.1** · tiers: gcse (2) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Probability — Combined] P(A) = 0.4, P(B) = 0.3, A and B are independent. Find P(A and B).`
  - `[gcse/Probability Tree] P(rain) = 0.3 on each of two independent days. Find P(rain on exactly one day).`
- **A4.9, N7.1** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Indices] Simplify (x³)⁴ ÷ x⁵`
- **G25.1** · tiers: gcse (1) · **1** items, **0** Foundation-pitched · **NO** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
- **N16.1** · tiers: gcse (1) · **1** items, **0** Foundation-pitched · **NO** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
- **A4.7** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Factorising Quadratics] Factorise x² − 5x + 6`
- **G17.1** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Arc Length] Find the arc length of a sector with radius 10cm and angle 72°.`
- **N9.1** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Standard Form Arithmetic] Calculate (3 × 10⁴) × (2 × 10³)`
- **R7.1, R10.1** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Proportion] y is directly proportional to x². When x = 3, y = 36. Find y when x = 5.`
- **R14.1** · tiers: core (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[core/Gradient Interpretation] A distance-time graph shows a straight line from (0, 0) to (4, 100). Interpret the gradient.`
- **S6.1, S6.2** · tiers: core (2) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[core/Correlation vs Causation] Ice cream sales and drowning rates both increase in summer. Does ice cream cause drowning?`
  - `[core/Regression Interpretation] A regression equation for house prices is: Price = 15,000 + 2,500 × (number of bedrooms). Interpret the 2,500.`
- **R16.1** · tiers: core (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Three courtroom arguments about a maths claim; the student judges which is right (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[core/Compound Interest Comparison] Bank A: 5% simple interest. Bank B: 4.8% compound interest. Which is better after 10 years on £1,000?`

### `negative-number-line` — Negative Number Line (Year 6)

- **N1.1** · tiers: Year 6 (shared bank ORDER_QUESTIONS) · **15** items, **15** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Order four integers in the range -10 to 10. Foundation grade 1-2 demand; nothing outside the integers.
  - Covers: ordering positive and negative integers only (no decimals/fractions, no inequality symbols)
  - `order: -3, 7, -8, 2`
  - `order: 1, -1, 0, -3`
  - `order: -6, 2, -2, 6`
- **N2.1** · tiers: Year 6 (shared bank CALC_QUESTIONS) · **15** items, **15** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Single add/subtract step on a -10..10 number line (e.g. start -3, add 5). Foundation grade 1-2 demand.
  - Covers: add/subtract with negative integers only; no multiply/divide, no decimals or fractions
  - `start -3, add 5 -> 2`
  - `start 1, subtract 6 -> -5`
  - `start 2, subtract 5 -> -3`

### `new-shapes` — New Shapes (Year 6)

- **G16.1** · tiers: Year 6 (shared banks PARALLELOGRAM 15, TRAPEZIUM 20, PRISM 15; ALL_QUESTIONS is their union) · **50** items, **50** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Area of parallelogram and trapezium and volume of a prism from given lengths, whole numbers, formula supplied. Foundation grade 3-4 demand.
  - Covers: area of parallelogram/trapezium, volume of a prism; no triangle-only, cuboid or cylinder items
  - `Area of a parallelogram: A = b \times h, b=6, h=4 -> 24`
  - `Area of a trapezium: A = \tfrac{1}{2}(a + b) \times h, a=5, b=7, h=8 -> 48`
  - `Volume of a prism: V = A \times l, A=21, l=4 -> 84`

### `percentage-flip` — Percentage Flip (Year 6, KS3, GCSE)

- **N12.1** · tiers: Year 6, KS3, GCSE labels (shared banks QUESTIONS_DEFAULT 12 + QUESTIONS_YEAR6 20) · **29** items, **29** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Percentage of an amount by the 10%/50%/25% building-block method, non-calculator. Direct Foundation demand.
  - Covers: percentage as operator on an amount only
  - `q=What is 50% of 80? \| a=40 \| w=50% = ÷2 → 80÷2 = 40`
  - `q=What is 75% of 40? \| a=30 \| w=75% = 50%+25% → 20+10 = 30`
  - `q=What is 75% of 160? \| a=120 \| w=75% = 50%+25% → 80+40 = 120`
- **R9.1** · tiers: shared banks · **29** items, **29** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Same 32 items; only "x% of an amount". No percentage change, reverse percentage or expressing one quantity as a percentage of another.
  - Covers: percentage of an amount only (1 of the 6 skills in R9.1)
  - `q=What is 50% of 80? \| a=40 \| w=50% = ÷2 → 80÷2 = 40`
  - `q=What is 75% of 40? \| a=30 \| w=75% = 50%+25% → 20+10 = 30`
  - `q=What is 75% of 160? \| a=120 \| w=75% = 50%+25% → 80+40 = 120`

### `prime-factorisation` — Prime Sprint (Year 6, KS3, GCSE)

- **N4.1** · tiers: Year 6, KS3, GCSE (fixed pools) · **38** items, **32** Foundation-pitched · **MIXED** · mode: procedural
  - Reasoning: Numbers read live from NUMBERS_DEFAULT (28) and NUMBERS_YEAR6 (20); 38 distinct (10 shared). 32 distinct are <=100; 120, 126, 132, 150, 180, 210 are beyond Foundation.
  - Covers: prime factorisation only (multiply-up build, 3 lives)
  - `default set: 12, 18, 24, 30, 36, 48, 60, 72, 84, 96 ...`
  - `Year 6 set: 12, 18, 20, 24, 28, 30, 36, 40, 42, 45 ...`
  - `default set includes 120, 132, 150, 180, 210`

### `prime-or-composite` — Prime or Composite (KS3, GCSE)

- **N4.1** · tiers: KS3, GCSE labels, one shared bank QUESTIONS · **66** items, **24** Foundation-pitched · **MIXED** · mode: procedural
  - Reasoning: n runs 2..9973: only 24 of 66 are <=100. Numbers like 157, 197, 239, 9973 cannot be judged mentally by a Foundation student.
  - Covers: prime vs composite only
  - `n=2 (Smallest prime)`
  - `n=99 (9 × 11 = ?)`
  - `[beyond Foundation] n=197 (Three digits)`

### `probability-paradox` — Probability Paradox (GCSE, Core)

- **P4.1, P8.1** · tiers: GCSE, Core labels (conditional set 14) · **2** items, **2** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Two Find-P(A U B) / P(A n B) items with mutually exclusive or independent events among the 12 conditional items. The rest of the game (Monty Hall, Simpson, Bertrand, P(A|B)) is Higher content.
  - Covers: addition rule for mutually exclusive events; independent events
  - `A and B are mutually exclusive events with P(A) = 0.3 and P(B) = 0.4. :: Find P(A ∪ B) -> 0.7`
  - `Events A and B are independent. P(A) = 0.6, P(B) = 0.3. :: Find P(A' ∩ B') -> 0.28`

### `probability-pioneer` — Probability Pioneer (Year 6)

- **P3.1** · tiers: Year 6 (shared banks STAGE1 10, STAGE3 15) · **25** items, **25** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Place events on the 0-1 scale with the words Impossible/Unlikely/Even chance/Likely/Certain (10) and judge true/false statements about probability (15: P between 0 and 1, P(A) + P(not A) = 1, gambler's fallacy, sample size). Foundation grade 1-3 demand.
  - Covers: 0-1 scale and language of probability; the "closer to theoretical with more trials" statement touches P5.1
  - `event=You will breathe today \| answer=1 \| label=Certain`
  - `statement=Rolling heads 5 times makes tails more likely next`
  - `statement=Two events with the same probability are equally likely`
- **P4.1** · tiers: Year 6 (shared bank STAGE3) · **7** items, **7** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: The statements that P(A) + P(not A) = 1, that a probability cannot exceed 1 and that P(certain) = 1.
  - Covers: probabilities summing to one (statements, not calculations)
  - `statement=P(event) is always between 0 and 1 inclusive`
  - `statement=P(certain event) = 1`
  - `statement=P(rolling 7 on a standard die) = 7/6`
- **P7.1** · tiers: Year 6 (shared bank STAGE2, 20) · **20** items, **20** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Single-event probabilities from a die, coin, bag of counters (P(6) = 1/6, P(prime) = 1/2) and one combined event (heads twice in a row).
  - Covers: theoretical probability of single events; one combined-event item, no possibility-space diagrams
  - `q=P(rolling a 6 on a fair die) \| answer=1/6 \| 1/6 \| 1/3 \| 1/2 \| 6`
  - `q=P(multiple of 3 on a die) \| answer=1/3 \| 1/3 \| 2/3 \| 1/2 \| 1/6`
  - `q=P(letter in MATHS also in GAMES) \| answer=2/5 \| 2/5 \| 3/5 \| 1/5 \| 4/5`

### `proportion-blaster` — Proportion Blaster (GCSE, A-Level)

- **R10.1, R13.1, R13.2, R13.4** · tiers: GCSE (50 of 100); A-Level tier excluded · **34** items, **21** Foundation-pitched · **MIXED** · mode: procedural
  - Reasoning: Direct proportion y = kx (12 items) and inverse y = k/x (9) are in range: find k, then find y or x. The 10 y = kx^2 and 3 y = k/x^2 items are Higher.
  - Covers: setting up and using y = kx and y = k/x. No graphs of proportional relationships and no "which of these tables is proportional"
  - `y is directly proportional to x. When x = 3, y = 12. :: Find k -> 4`
  - `P is inversely proportional to V. When V = 4, P = 25. :: Find P when V = 10 -> 10`
  - `[beyond Foundation] y ∝ x². When x = 5, y = 50. :: Find k -> 2`
- **R5.1** · tiers: GCSE tier · **12** items, **10** Foundation-pitched · **MIXED** · mode: procedural
  - Reasoning: Share an amount in a ratio (10 items, two and three parts) are in range; the two "combine a:b and b:c" items are grade 7.
  - Covers: dividing a quantity in a ratio
  - `Share £60 in the ratio 2 : 3. :: Find the larger share -> £36`
  - `A recipe uses flour and sugar in ratio 5 : 2. You have 350 g of flour. :: How much sugar? -> 140`
  - `[beyond Foundation] x : y = 5 : 8. y : z = 4 : 3. :: Find x : y : z -> 5 : 8 : 6`
- **R9.1** · tiers: GCSE tier · **2** items, **2** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Reverse percentage: original price after a 20% rise; original value after a 15% fall.
  - Covers: original-value percentage problems, 2 items
  - `After a 20% increase, the new price is £60. :: What was the original price? -> £50`
  - `After a 15% decrease, the value is £170. :: What was the original value? -> £200`
- **R16.1** · tiers: GCSE tier · **2** items, **2** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Depreciation 10% a year over 2 years; 5% growth over 3 years.
  - Covers: compound growth/decay, 2 items
  - `A car depreciates by 10% each year. It cost £20,000. :: Value after 2 years? -> £16,200`
  - `A population increases by 5% per year from 8000. :: Population after 3 years (nearest whole) -> 9261`

### `quadratic-factoriser` — Quadratic Factoriser (GCSE, A-Level)

- **A4.7** · tiers: GCSE level (of three) · **174** items, **174** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: gcsePool read live: bothPos 45, oneNeg 72, bothNeg 45, dots 12. All are x^2 + bx + c with a = 1, which is what A4.7 states. In practice grade 5-6, but the pool stays inside the underlined part.
  - Covers: factorising x^2 + bx + c incl. difference of two squares. The 3,760 a > 1 items (A4.8) and 1,254 formula items (A18.4) are bold and excluded
  - `x^2 + 2x + 1 (both positive), x^2 + 7x + 12`
  - `x^2 + 2x - 8 style (one negative): p=6, q=-8 -> x^2 - 2x - 48`
  - `difference of two squares: x^2 - k^2 (12 items)`

### `regression-rumble` — Regression Rumble (Core, A-Level, L4)

- **S6.1, S6.2** · tiers: Core (12); A-Level, L4 excluded · **12** items, **0** Foundation-pitched · **NO** · mode: procedural
  - Reasoning: Core Maths S3.7: fitted regression equations and correlation coefficients (r = 0.88, y = 32 + 4.2x) from reading to calculating. Foundation S6 is an estimated line of best fit by eye.
  - Covers: (not Foundation content)
  - `[beyond Foundation] Hours of revision vs Exam score, n=15, r=0.88`
  - `[beyond Foundation] Screen time (hours) vs Sleep (hours), n=20, r=-0.72`
  - `[beyond Foundation] Sunshine (hours per day) vs Energy bill (\u00a3), n=16, r=-0.78`

### `scale-factor-scaling` — Scale Factor Scaling (GCSE, A-Level, L4)

- **G19.1, G19.3, R12.1, R12.2** · tiers: GCSE, A-Level, L4 labels (one shared bank, T1-T4, 46) · **46** items, **28** Foundation-pitched · **MIXED** · mode: procedural
  - Reasoning: Area and volume scale factors (k^2, k^3) from a linear scale factor: 28 forward items (double the lengths, area x4) are in range; the 10 reverse items (cube-root a volume ratio) and 8 contextual ratio items are grade 6+.
  - Covers: length/area/volume scale factors of similar shapes; no similar-triangle side-length calculation and no enlargement
  - `[Area SF] Length scale factor = 2. Area scale factor = ? -> 4`
  - `[Volume SF] A model car is 1:20 scale. Real car volume = 4 m³. Model volume = ? -> 0.0005 m³`
  - `[beyond Foundation] [Reverse] Area ratio = 9:25. Volume ratio = ? -> 27:125`

### `sequence-solver` — Sequence Solver (KS3, GCSE, A-Level, L4)

- **A23.1** · tiers: KS3 (50), GCSE (50) tiers of a 154-item bank; A-Level tier excluded · **46** items, **46** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Continue a sequence (+2, -5, x2, x1/3, Fibonacci, squares), generate terms from T_n = 2n + 5, and evaluate the 40th term from a given formula. Foundation grade 2-4 demand; the x2/x3 items are geometric but still term-to-term.
  - Covers: term-to-term and position-to-term rules
  - `[ks3] 2, 4, 6, 8, __ :: Find the next term -> 10`
  - `[ks3] 2, 3, 5, 7, 11, 13, __ :: Find the next term -> 17`
  - `[gcse] 3, __, 12, __, 21 :: Fill in the gaps -> 3, 7.5, 12, 16.5, 21`
- **A24.1** · tiers: KS3 (50), GCSE (50) tiers · **10** items, **10** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: The "what type of sequence?" items (arithmetic/geometric/Fibonacci/triangular/square) plus continue-the-sequence items on square, triangular and Fibonacci numbers. Cube numbers appear in one item only (a type-naming item, 1, 8, 27, 64, 125).
  - Covers: recognising triangular, square, Fibonacci-type and (once) cube sequences
  - `[ks3] 3, 6, 9, 12, 15 :: What type of sequence? -> Arithmetic`
  - `[ks3] 1, 3, 6, 10, 15 :: What type of sequence? -> Triangular numbers`
  - `[ks3] 0, 1, 1, 2, 3, 5, 8, 13, 21, __ :: Find the next term -> 34`
- **A24.2** · tiers: KS3 (50), GCSE (50) tiers · **43** items, **43** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Continue an arithmetic or geometric sequence, common difference, common ratio (integer and fractional), second differences. Foundation-assessable per the file; the ratio and second-difference items are grade 4-6.
  - Covers: arithmetic, geometric (r integer/rational, no surds), Fibonacci-type and quadratic sequence recognition
  - `[ks3] 2, 4, 6, 8, __ :: Find the next term -> 10`
  - `[ks3] 64, 32, 16, 8, __ :: Find the next term -> 4`
  - `[gcse] 1, __, __, 64 :: If geometric, fill the gaps -> 1, 4, 16, 64`
- **A25.1, A25.3** · tiers: KS3 (50), GCSE (50) tiers · **21** items, **21** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Deduce the linear nth term (4n + 1, 13 - 3n) and find a later term of a pattern. Foundation grade 4-5 demand.
  - Covers: linear nth term. The 9 quadratic nth-term items are the bold A25.2 and are excluded
  - `[ks3] 3, 6, 9, 12, ... :: Find the 10th term -> 30`
  - `[gcse] 3, 5, 7, 9, ... :: Find the nth term -> 2n + 1`
  - `[gcse] The first term is 5, the common difference is -3. :: Find the 10th term -> -22`
- **A25.2 (bold/not Foundation)** — *not counted* · tiers: GCSE tier · **9** items, **0** Foundation-pitched · **NO** · mode: procedural
  - Reasoning: Quadratic nth term (n^2 + 3, n^2 + 2n) is bold, Higher only. Recorded for the count only; A25.2 is not a Foundation part.
  - Covers: (not a Foundation part)
  - `[beyond Foundation] [gcse] 1, 4, 9, 16, 25 :: Find the nth term -> n^2`
  - `[beyond Foundation] [gcse] 4, 7, 12, 19, 28 :: Find the nth term -> n^2 + 3`
  - `[beyond Foundation] [gcse] 3, 8, 15, 24, 35 :: Find the nth term -> n^2 + 2n`

### `shape-shifter` — Shape Shifter (Year 6)

- **G7.1** · tiers: Year 6 (shared banks TRANSLATION 15, REFLECTION 15, ROTATION 15) · **45** items, **45** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Translate, reflect (x- and y-axis) and rotate (90 degrees about the origin) a triangle or rectangle on a coordinate grid. Foundation grade 2-4 demand.
  - Covers: translation, reflection, rotation. There are NO enlargement items, which G7.1 (and G7.2/G7.4 fractional scale factors) name
  - `Translate 2 right and 1 up (triangle)`
  - `Reflect in the y-axis (rectangle)`
  - `Rotate 90° anticlockwise about (0,0) (rectangle)`

### `simultaneous-solver` — Simultaneous Solver (GCSE, A-Level)

- **A19.1** · tiers: GCSE tier (50); A-Level tier excluded · **50** items, **46** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Two linear equations, elimination-friendly coefficients (2x + y = 7, x - y = 2), find x or y. Four give fractional answers (e.g. 30/13) and are grade 6+. None involve a quadratic.
  - Covers: linear/linear simultaneous equations algebraically
  - `2x + y = 7 \| x - y = 2 :: Find x -> 3`
  - `2x - y = 0 \| x + 3y = 14 :: Find y -> 4`
  - `[beyond Foundation] 5x + 2y = 3 \| x - y = 3 :: Find x -> \tfrac{9}{7}`

### `split-it` — Split It (KS3, GCSE)

- **R4.1** · tiers: KS3, GCSE (mode simplify) · **109** items, **109** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Foundation demand. Two-part ratios (KS3 label) and three-part (GCSE label), highest common factor at most 10.
  - Covers: reduce a ratio to simplest form
  - `ks3: "Write 12 : 24 in its simplest form." -> 1:2`
  - `ks3: "Write 80 : 60 in its simplest form." -> 4:3`
  - `gcse: "Write 15 : 12 : 3 in its simplest form." -> 5:4:1`
- **R5.1** · tiers: KS3, GCSE (mode divide) · **118** items, **118** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Foundation demand, whole-number shares; three-part shares at the GCSE label.
  - Covers: divide a quantity in a given ratio (two and three parts)
  - `ks3: "Share 48 kg in the ratio 4 : 2" -> 32, 16`
  - `ks3: "Share 153 kg in the ratio 4 : 5" -> 68, 85`
  - `gcse: "Divide 143 in the ratio 5 : 5 : 1" -> 65, 65, 13`
- **R7.1** · tiers: KS3, GCSE (mode equivalent) · **116** items, **116** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Foundation demand: scale factor 2-9 between equivalent ratios.
  - Covers: equivalent ratios / proportion as equality of ratios
  - `ks3: "1 : 5 = 6 : ?" -> 30`
  - `ks3: "6 : 5 = ? : 15" -> 18`
  - `gcse: "If 4 : 3 = x : 18, find x." -> 24`
- **N11.1, R8.1** · tiers: KS3, GCSE (mode fractions) · **91** items, **91** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Foundation-friendly: the fraction is part / sum of parts, simplified.
  - Covers: fraction of the total from a ratio
  - `ks3: "In the ratio 4 : 6, what fraction of the total is the larger part?" -> 3/5`
  - `ks3: "In the ratio 5 : 2, what fraction of the total is the smaller part?" -> 2/7`
  - `gcse: "In the ratio 2 : 5 : 3, what fraction of the total is the largest part?" -> 1/2`
- **R10.1, R11.1** · tiers: KS3, GCSE (modes unitary and scale) · **193** items, **193** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Unitary method, recipe scaling and best-value comparison. Foundation demand throughout (grade 3-5).
  - Covers: direct proportion by the unitary method, unit pricing, speed. No inverse proportion
  - `ks3: "7 stickers cost £15.40. How much do 12 stickers cost?" -> £26.40`
  - `gcse: "Pack A: 5 for £2.75. Pack B: 10 for £2.00. Which is better value?" -> B`
  - `gcse: "A car travels 232 miles in 5 hours. How far in 3 hours?" -> 139.2`

### `spot-the-error` — Spot the Error (KS3, GCSE, L4)

- **R5.1, R4.1** · tiers: ks3 (3) · **3** items, **3** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Ratio] Three friends win prize money on a scratch card. They agree to share the winnings in the ratio of the number o`
  - `[ks3/Ratio] A drink is made by mixing orange juice and water in the ratio 1:4. A student calculates how much orange juice `
  - `[ks3/Ratio] A recipe uses oats and butter in the ratio 4:1 by mass. A chef wants to make a batch using 600 g of oats. She `
- **R9.1** · tiers: ks3 (4), gcse (3) · **7** items, **7** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Percentages] A sports shop is having a sale. All trainers are reduced by 20%. Jayden sees a pair of trainers with an origin`
  - `[ks3/Percentages] A football club had 4,500 fans on average last season. This season the average is 5,040. A journalist calculat`
  - `[gcse/Reverse Percentage] A house is valued at £292,500 after its value increased by 17% over 5 years. An estate agent wants to find the`
- **N2.1, N8.1** · tiers: ks3 (4) · **4** items, **4** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Fractions] A baker makes 48 muffins. She sells three-quarters of them before lunch and one-third of the remainder in the `
  - `[ks3/Fractions] Freya is training for a sponsored walk. On Monday she walks 2⅓ miles, on Wednesday 1¾ miles and on Friday 3⅙ m`
  - `[ks3/Fractions] In a school, two-fifths of students study French and one-quarter study Spanish. The rest study German. A stude`
- **R7.1, R10.1** · tiers: ks3 (2) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Proportion] A car uses petrol at a constant rate. It travels 240 miles on a full tank of 30 litres. A driver plans a journ`
  - `[ks3/Proportion] A car travels 150 km in 2 hours. A student calculates how long to travel 225 km at the same speed.`
- **A23.1, A25.1** · tiers: ks3 (3), gcse (1) · **4** items, **4** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Sequences] Square tiles are laid in a growing pattern. The first pattern uses 1 tile, the second uses 5, the third uses 9`
  - `[ks3/Sequences] A ball is dropped from 160 cm. After each bounce it reaches half the height of the previous bounce. A student `
  - `[gcse/nth Term] A sequence goes: 5, 8, 11, 14... A student finds the nth term.`
- **G16.1, G17.1** · tiers: ks3 (3) · **3** items, **3** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Area] A triangular warning sign has a base of 40 cm and a perpendicular height of 35 cm. A manufacturer calculates t`
  - `[ks3/Area & Perimeter] A farmer wants to fence a rectangular field 85 m long and 62 m wide. A student calculates the total length of `
  - `[ks3/Area] A circular pond has a diameter of 4.2 metres. An owner calculates the area of the pond to buy a cover.`
- **S4.3** · tiers: ks3 (3) · **3** items, **3** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Mean] The mean age of 6 players in a basketball team is 17 years. A seventh player joins and the new mean of all 7 p`
  - `[ks3/Mean] A teacher records 9 test scores: 14, 18, 9, 14, 20, 11, 14, 17, 15. A student finds the median to report to pa`
  - `[ks3/Median] A student records test scores: 5, 2, 8, 4, 6, 1, 9. They find the median without sorting the data first.`
- **P7.1, P8.1** · tiers: ks3 (1), gcse (2) · **3** items, **3** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Probability] A bag contains red, blue and yellow counters. Maria pulls a counter and replaces it 80 times, getting red 24 t`
  - `[gcse/Probability] A bag has 5 red, 3 blue and 2 green counters. Two are drawn from the bag without replacement. A student finds `
  - `[gcse/Probability] The probability it rains on any given day is 0.3. A student finds the probability that it rains on at least on`
- **R2.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Scale] A map uses a scale of 1:50,000. On the map, the distance between two locations is 6.4 cm. A hiker calculates t`
- **G3.1** · tiers: ks3 (4) · **4** items, **4** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Angles] Two roads meet at a junction. The angle between them on one side is 47°. A surveyor calculates the angle on th`
  - `[ks3/Triangle] A right-angled triangle has shorter sides 6 cm and 8 cm. A student finds the hypotenuse.`
  - `[ks3/Angle Sum] A quadrilateral has angles of 80°, 110° and 95°. A student finds the missing angle.`
- **N2.1** · tiers: ks3 (2) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Number] Two planets orbit a star. Planet A takes 420 days per orbit and Planet B takes 315 days. A student finds when `
  - `[ks3/Subtraction] A train journey is 142 km. After travelling 87 km the driver checks how far is left. A student calculates the `
- **G17.1** · tiers: ks3 (1), gcse (1) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Circumference] A circular flower bed has radius 3.5 m. A gardener calculates the area to buy topsoil.`
  - `[gcse/Arc Length] A sector has radius 10 cm and angle 72°. A student finds the arc length.`
- **N15.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Rounding] A measurement of 3.45 m is rounded to 1 decimal place. A student gives the answer.`
- **R11.1, R1.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Conversion] A recipe requires 1.5 litres of milk. A student converts this to millilitres.`
- **R12.2** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Scale Factor] A map has scale 1:25000. A path on the map is 8 cm. A student calculates the real length.`
- **A4.3** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Brackets] A student evaluates 3(x + 4) when x = 2.`
- **R16.1** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Compound Interest] A savings account pays 3.5% compound interest per year. £2,000 is invested. A student calculates the value aft`
- **G25.1** · tiers: gcse (2) · **2** items, **0** Foundation-pitched · **NO** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
- **N9.1** · tiers: gcse (3) · **3** items, **3** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Standard Form] The speed of light is 3 × 10⁸ m/s and the distance to Proxima Centauri is 4.013 × 10¹⁶ m. A student calculates`
  - `[gcse/Standard Form] Calculate (3 × 10⁴) × (2 × 10³). A student works it out.`
  - `[gcse/Standard Form] The mass of the Earth is 5.97 × 10²⁴ kg and the Moon is 7.34 × 10²² kg. A student calculates how many times he`
- **G20.5** · tiers: gcse (3) · **3** items, **3** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Trigonometry] From the top of a cliff 80 m high, the angle of depression to a boat is 34°. A student finds the horizontal di`
  - `[gcse/Trigonometry] A ramp rises 0.9 m over a horizontal distance of 6 m. An architect checks the angle of incline.`
  - `[gcse/Trigonometry] A ship sails 15 km north then 22 km east. A student uses trigonometry to find the bearing to return to port.`
- **G19.1** · tiers: gcse (1) · **1** items, **0** Foundation-pitched · **NO** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
- **A19.1** · tiers: gcse (3) · **3** items, **3** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Simultaneous Equations] Mr Jones buys 5 tins of paint and 4 rolls of tape for £167. He returns 1 tin and 1 roll for a refund of £33.75`
  - `[gcse/Simultaneous Equations] A cinema sells adult tickets at £a and child tickets at £c. On Monday, 3 adult and 5 child tickets cost £45. O`
  - `[gcse/Simultaneous] A student solves: 2x + 3y = 13 and 4x − y = 5 by substitution.`
- **A9.1, A10.1** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Gradient] A line passes through (2, 5) and (6, 13). A student calculates the gradient.`
- **N16.1** · tiers: gcse (1) · **1** items, **0** Foundation-pitched · **NO** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
- **A7.1** · tiers: gcse (2) · **2** items, **0** Foundation-pitched · **NO** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
- **A22.1, A22.3, A22.5** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Inequalities] A student solves the inequality −3x > 12.`
- **A18.1, A18.3** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Quadratics] A rectangular field has a length that is 7 metres more than its width w metres. The area of the field is 198 m`
- **G20.1** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Pythagoras] A 6 m ladder leans against a vertical wall. Its foot is 1.8 m from the base of the wall. A student finds how f`
- **G15.1** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Bearing] A ship sails on a bearing of 250° for 30 km. A student calculates the westward displacement.`
- **P8.1** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Probability Tree] P(rain) = 0.4 over two days. A student draws a tree diagram but makes an error in the second branch.`
- **A4.4, A4.6** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Expanding Brackets] A student is asked to expand (x + 3)(x + 5).`
- **A5.1** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: Error-finding in a worked solution (which step is wrong): diagnostic reasoning about the method, not procedural practice. 1-4 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Equation Rearrangement] A student is asked to make t the subject of v = u + at.`

### `spot-the-muppet` — Spot the Muppet (KS3, GCSE, Core)

- **R9.1** · tiers: ks3 (3), gcse (2), core (1) · **6** items, **6** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Percentages] You need 30% of 80. Easy — just divide by 30. So 80 ÷ 30 = 2.67. That's your answer. I do this kind of thing a`
  - `[ks3/Combined Percentage Discounts] You've got a 20% off voucher and a 30% off voucher. Use them both together for 50% off. That's just addition, `
  - `[core/Reverse Percentage] Receipt says £120 including 20% VAT. To find the pre-VAT price, take off 20%: £120 − £24 = £96.`
- **R5.1, R4.1** · tiers: ks3 (2) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Ratio] Share 60 sweets in the ratio 2:3. Straightforward — one person gets 60 ÷ 2 = 30 and the other gets 60 ÷ 3 = 20`
  - `[ks3/Ratio — Cocktails] Cocktail uses juice and lemonade in ratio 2:5. Need 350ml total. Juice = 350 ÷ 2 = 175ml, lemonade = 350 ÷ 5 =`
- **N2.1, N8.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Fractions] To add ½ and ⅓, just add the tops and add the bottoms. 1+1=2, 2+3=5. So ½ + ⅓ = 2/5. It's literally that simpl`
- **S4.3** · tiers: ks3 (2), core (1) · **3** items, **2** Foundation-pitched · **MIXED** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Mean vs Median] To find the mean of 3, 7, 8, 2 and 10 — find the middle number when sorted: 2, 3, 7, 8, 10. Middle value is 7.`
  - `[ks3/Mode] The mode of 3, 3, 5, 7, 7, 9 is 5 — right in the middle. Mode means the middlemost value.`
- **R7.1, R10.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Proportion] A recipe for 4 serves uses 300g of flour. For 7 people, add 3 extra portions: 300 + 3 = 303g. Cooking is basic`
- **G16.1, G17.1** · tiers: ks3 (2) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Area of Triangle] Your garden is a triangle with base 8m and height 5m. Area = base × height = 8 × 5 = 40 m². Get ordering that `
  - `[ks3/Perimeter vs Area] Rectangular lawn 9m by 4m. You need edging strip for the perimeter. Perimeter = length × width = 9 × 4 = 36m. `
- **A23.1, A25.1** · tiers: ks3 (1), gcse (1) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Sequences] The sequence 2, 4, 8, 16 is obviously going up by 4 each time. Next term = 16 + 4 = 20. Patterns are my passio`
  - `[gcse/nth Term] Sequence: 5, 8, 11, 14. The nth term is 3n + 5. Check: when n=1, 3(1)+5 = 8. Close enough to 5.`
- **N12.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Fractions of Amounts] To find ¾ of 48 — divide by 4 and you get 12. Simple. No need to multiply by 3, that would just make it bigger`
- **R2.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Map Scale] Scale 1:25,000. Distance of 3cm on map. Real distance = 3 × 25,000 = 75,000cm. Obviously too far — maps can't `
- **G3.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Angles in a Triangle] 360° in a triangle — well known fact. Two angles are 80° and 60°, so the third is 360 − 80 − 60 = 220°. Bit of`
- **N2.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Mental Multiplication] 24 × 15: multiply by 10 and add 5. That's 240 + 5 = 245. Always break it down.`
- **P7.1, P8.1** · tiers: ks3 (1), gcse (2) · **3** items, **3** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Gambler's Fallacy] You've flipped heads 5 times in a row. The next flip is definitely tails — the coin is 'due' one. That's just `
  - `[gcse/Probability] P(rolling a 6) = 1/6. I roll 6 dice so I'm guaranteed exactly one 6. That's just how averages work.`
  - `[gcse/Combined Probability] P(heads) = 0.5 and P(rolling a 6) = 1/6. P(heads AND a 6) = 0.5 + 1/6 = 2/3. You just add them together.`
- **N9.1** · tiers: ks3 (1), gcse (1) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Standard Form] 3,400,000 in standard form is 34 × 10⁵. I keep the first number as a whole number — much cleaner.`
  - `[gcse/Standard Form Operations] (3 × 10⁴) × (2 × 10³) = 6 × 10¹². When you multiply, you multiply the powers too: 4 × 3 = 12.`
- **R16.1** · tiers: gcse (1), core (1) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Compound Interest] £500 at 4% compound interest for 3 years: £500 × 0.04 × 3 = £60 interest. Total: £560. Compounding is just a f`
  - `[core/Compound Interest] £1,000 at 5% for 20 years: £1,000 × 1.05 × 20 = £21,050. Retirement sorted.`
- **A19.1** · tiers: gcse (2) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Simultaneous Equations — Gotcha] 2x + y = 10 and x + y = 7. Subtract: x = 3. Sub back: 3 + y = 7, y = 4. Check: 2(3)+4=10 ✓ and 3+4=7 ✓. Correc`
  - `[gcse/Simultaneous Equations — Sign Error] 3x + 2y = 16 and x + 2y = 8. Subtract the second from the first: 3x − x + 2y − 2y = 16 − 8, so 2x = 8, x = 4. `
- **N16.1** · tiers: gcse (1) · **1** items, **0** Foundation-pitched · **NO** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
- **A18.1, A18.3** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Quadratics — Square Roots] To solve x² = 25, take the square root: x = 5. One answer. Clean. Elegant.`
- **R11.1** · tiers: gcse (1), core (1) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Best Value — Gotcha] 400g coffee £4.80, 650g £7.15. The big one is better value — always the big one. I've built my entire life phi`
  - `[core/Best Value] 500ml shampoo £3.50, 750ml £4.80. Difference: £1.30 for 250ml extra. That's better than paying £3.50 for 500ml`
- **A4.9, N7.1** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Index Laws] x³ × x⁴ = x¹². You multiply the powers when you multiply. 3 × 4 = 12.`
- **G25.1** · tiers: gcse (1) · **1** items, **0** Foundation-pitched · **NO** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
- **G17.1** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Circle Area] Circle with diameter 10cm. Area = π × 10² = 314.16cm². I always use the diameter — it's the bigger number.`
- **A10.1** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Gradient — Gotcha] Gradient through (2,3) and (6,7) = rise over run = (6−2) ÷ (7−3) = 4 ÷ 4 = 1. Nice round number.`
- **A4.7** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Factorising] Factorise x² + 5x + 6: find two numbers that add to 6 and multiply to 5. That's 1 and 5. Answer: (x+1)(x+5).`
- **G20.5** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Trigonometry] Right triangle: opposite = 6cm, hypotenuse = 10cm. cos θ = opp ÷ hyp = 6 ÷ 10 = 0.6. θ = cos⁻¹(0.6) = 53.1°.`
- **A4.4, A4.6** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Expanding Brackets] (x+3)² = x² + 9. Square both parts separately. Quick, clean, no mess.`
- **G20.1** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Pythagoras] Right triangle with sides 5cm and 12cm. Hypotenuse = 5² + 12² = 25 + 144 = 169cm. Done.`
- **S6.1, S6.2** · tiers: core (2) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A comedy character gives flawed advice; the student spots the flaw (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[core/Correlation] Countries with more TVs have longer life expectancy. Therefore TVs increase lifespan. I'm prescribing televisi`
  - `[core/Line of Best Fit] I always draw my line of best fit through the origin (0,0). Every relationship starts from zero. It's common s`

### `standard-form-blitz` — Standard Form Blitz (GCSE, A-Level)

- **N9.1** · tiers: GCSE (bank tier gcse; the alevel tier is separate) · **50** items, **30** Foundation-pitched · **MIXED** · mode: procedural
  - Reasoning: 30 items convert to/from standard form or compare sizes (Foundation). The 20 "Calculate" items multiply/divide two standard-form numbers with negative powers, which is grade 5-6.
  - Covers: convert, compare and calculate with standard form
  - `Write in standard form: 45000 -> 4.5 \times 10^4`
  - `Write in correct standard form: 0.25 \times 10^{-1} -> 2.5 \times 10^{-2}`
  - `[beyond Foundation] Calculate: (8 \times 10^6) \div (2 \times 10^3) -> 4 \times 10^3`

### `stat-attack` — Stat Attack (GCSE, Core, L4)

- **S4.3** · tiers: GCSE (12); Core (12), L4 (12) excluded · **12** items, **12** Foundation-pitched · **MIXED** · mode: procedural
  - Reasoning: Grouped frequency tables (35-40 values): modal class, median class, estimated mean are Foundation; each scenario then walks variance and standard deviation (A-level), so half of every scenario is beyond Foundation. Counted as scenarios; the Foundation-pitched steps are roughly half of each.
  - Covers: modal class, median class, estimated mean of grouped data (and SD, which is not Foundation)
  - `Maths exam scores: 35 students sat a maths exam. The grouped frequency table shows their scores. classes 20 ≤ x < 30..60 ≤ x < 70, modal class 40 ≤ x < 50, mean 46.4, SD 11.6`
  - `Distance thrown in PE (metres): 35 students measured how far they could throw a ball in PE. classes 5 ≤ x < 10..25 ≤ x < 30, modal class 15 ≤ x < 20, mean 17.6, SD 5.55`
  - `Time to complete a puzzle (seconds): 40 students timed how long it took them to complete a logic puzzle. classes 30 ≤ x < 60..150 ≤ x < 180, modal class 90 ≤ x < 120, mean 108.75, SD 34.3`

### `tax-theft` — Tax Theft (Core)

- **R9.1** · tiers: Core label (3 difficulty bands) · **20** items, **8** Foundation-pitched · **MIXED** · mode: procedural
  - Reasoning: Parametric payslip calculator, 8 easy + 8 medium + 4 hard salaries. Only the 8 easy items (subtract the allowance, take 20%, then NI at 8%) are percentage-of-amount at Foundation level; the higher-rate and taper bands are Core Maths.
  - Covers: percentage of an amount in a payslip context
  - `easy band: gross £14,000 ... £35,750 -> taxable income, then 20% basic-rate tax`
  - `medium band: £52,000 ... £92,500 -> basic and higher (40%) rate`
  - `hard band: £106,000 ... £130,000 -> personal allowance taper then three rates`

### `terrible-advice` — Terrible Advice (KS3, GCSE, Core)

- **R9.1** · tiers: ks3 (3), gcse (2), core (1) · **6** items, **6** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Percentages] You need to find 30% of 80. Easy — just divide by 30. So 80 ÷ 30 = 2.67. That's your answer. I do this kind of`
  - `[ks3/Percentages] You've got a 20% off voucher and a 30% off voucher for the same shop. Use them both together for 50% off. That`
  - `[core/Reverse Percentage] A TV costs £360 including 20% VAT. To find the pre-VAT price, just subtract 20%: £360 − £72 = £288. That's £72`
- **R5.1, R4.1** · tiers: ks3 (2), gcse (1) · **3** items, **3** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Ratio] Share 60 sweets in the ratio 2:3. Straightforward — 2 + 3 = 5, so each person gets 60 ÷ 2 = 30 and 60 ÷ 3 = 20`
  - `[ks3/Ratio] This cocktail uses juice and lemonade in the ratio 2:5. I need 350ml total. Juice = 350 ÷ 2 = 175ml, lemonade `
  - `[gcse/Ratio Best Value] 400g of coffee costs £4.80 or 650g costs £7.15. The big one is better value — it's always the big one. I've bu`
- **N2.1, N8.1** · tiers: ks3 (2) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Fractions] To add ½ and ⅓, you just add the tops and add the bottoms. 1+1=2, 2+3=5. So ½ + ⅓ = ⅖. It's literally that sim`
  - `[ks3/Fractions] To find ¾ of 48 — divide by 4 and you get 12. Simple. No need to multiply by 3, that would just make it bigger`
- **S4.3** · tiers: ks3 (2), core (1) · **3** items, **2** Foundation-pitched · **MIXED** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Mean] To find the mean of 3, 7, 8, 2 and 10 — just find the middle number when they're in order. 2, 3, 7, 8, 10 — th`
  - `[ks3/Averages] The mode of 3, 3, 5, 7, 7, 9 is 5 — right in the middle. Mode means the middlemost value, everyone knows that.`
- **R7.1, R10.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Proportion] A recipe for 4 serves uses 300g of flour. To make it for 7 people, add 3 extra portions: 300 + 3 = 303g. Cooki`
- **G16.1, G17.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Area] Your garden is a triangle with base 8m and height 5m. Area = base × height = 8 × 5 = 40 m². That's how much tu`
- **A23.1, A25.1** · tiers: ks3 (1), gcse (1) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Sequences] The sequence 2, 4, 8, 16... is obviously going up by 4 each time. So the next term is 16 + 4 = 20. Patterns ar`
  - `[gcse/nth Term] The sequence 5, 8, 11, 14... has a common difference of 3. So the nth term is 3n. When n = 1: 3(1) = 3. Hmm, t`
- **R2.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Scale] The map scale is 1:25,000. A distance of 3cm on the map is 3 × 25,000 = 75,000cm in real life. But that's obvi`
- **G3.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Angles] There are 360° in a triangle. Well known fact. So if two angles are 80° and 60°, the third is 360 − 80 − 60 = `
- **N2.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Number] To multiply 24 by 15, just multiply 24 by 10 and add 5. That's 240 + 5 = 245. Always break it down, that's my `
- **P7.1, P8.1** · tiers: ks3 (1), gcse (2) · **3** items, **3** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Probability] You've flipped heads 5 times in a row. The next flip is definitely tails — the coin is 'due' a tails. That's j`
  - `[gcse/Probability] The probability of rolling a 6 on a fair die is ⅙. I roll it 6 times — so I'm guaranteed to get exactly one 6.`
  - `[gcse/Probability] The probability of flipping heads is 0.5 and rolling a 6 is 1/6. The probability of getting both (heads AND a `
- **G17.1** · tiers: ks3 (1), gcse (1) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Perimeter] Your rectangular lawn is 9m by 4m. You need edging strip for the perimeter. Perimeter = length × width = 9 × 4`
  - `[gcse/Circle Area] A circle has diameter 10cm. Area = π × 10² = 314.16cm². I always use the diameter — it's the bigger number so `
- **N9.1** · tiers: ks3 (1), gcse (1) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Standard Form] The number 3,400,000 in standard form is 34 × 10⁵. I like to keep the first number as a whole number — much cl`
  - `[gcse/Standard Form] Convert 0.00057 to standard form. Move the decimal until you get 5.7. I moved it 3 places, so it's 5.7 × 10⁻³.`
- **R16.1** · tiers: gcse (1), core (1) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Compound Interest] You invest £500 at 4% compound interest for 3 years. That's £500 × 0.04 × 3 = £60 interest. Total: £560. Compo`
  - `[core/Compound Interest] Invest £1,000 at 5% for 20 years. Using compound interest: £1,000 × 1.05 × 20 = £1,000 × 21.05 = £21,050. Reti`
- **A19.1** · tiers: gcse (2) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Simultaneous Equations] 2x + y = 10 and x + y = 7. To solve, subtract the second from the first: x = 3. Then substitute: 3 + y = 7, so`
  - `[gcse/Simultaneous Equations] Solve 3x + 2y = 16 and x + 2y = 10. Subtract: 3x + 2y − x + 2y = 16 − 10. That gives 2x + 4y = 6. Hmm, still t`
- **N16.1** · tiers: gcse (1) · **1** items, **0** Foundation-pitched · **NO** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
- **A18.1, A18.3** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Quadratics] To solve x² = 25, take the square root: x = 5. One answer. Clean. Elegant. Done.`
- **A4.9, N7.1** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Indices] x³ × x⁴ = x¹². Everyone knows you multiply the powers when you multiply the same base. Multiplication all the `
- **G25.1** · tiers: gcse (1) · **1** items, **0** Foundation-pitched · **NO** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
- **A9.1, A10.1** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Straight Line Graphs] The gradient of a line through (2,3) and (6,7) is rise over run = (6−2)÷(7−3) = 4÷4 = 1. Nice round number — y`
- **A4.7** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Factorising] To factorise x² + 5x + 6, find two numbers that add to 6 and multiply to 5. That's 1 and 5 — so the answer is `
- **G20.5** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Trigonometry] In a right-angled triangle, the opposite side is 6cm and the hypotenuse is 10cm. To find the angle, use cos θ `
- **A4.4, A4.6** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Expanding Brackets] (x+3)² = x² + 9. You just square both parts separately. Quick, clean, no mess.`
- **G20.1** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Pythagoras] A right-angled triangle has sides 6cm and 8cm. The hypotenuse = 6² + 8² = 36 + 64 = 100cm. Nice round number. `
- **R11.1** · tiers: core (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[core/Best Value] 500ml of shampoo costs £3.50 and 750ml costs £4.80. The difference in price is £1.30 for 250ml extra. That's b`
- **S6.1, S6.2** · tiers: core (2) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A "terrible advisor" gives flawed advice; the student picks the correct method (diagnostic). 1-3 items per topic.
  - Covers: one topic among many; see mode
  - `[core/Correlation] I found that countries with more TVs per household have longer life expectancy. Therefore, buying a TV increas`
  - `[core/Scatter Graphs] I've plotted height against shoe size for 30 adults. The line of best fit should always pass through the origi`

### `think-of-a-number` — Think of a Number (Year 6)

- **N3.1** · tiers: Year 6 (shared bank QUESTIONS by step count) · **50** items, **50** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: One-, two- and three-step undo-the-working puzzles with whole numbers. Foundation grade 1-3 demand.
  - Covers: inverse operations; no brackets/powers/roots/reciprocals
  - `result 14 -> answer 8; undo: 14 − 6 = 8`
  - `result 6 -> answer 21; undo: 6 × 4 = 24 ; 24 − 3 = 21`
  - `result 40 -> answer 6; undo: 40 ÷ 2 = 20 ; 20 − 2 = 18 ; 18 ÷ 3 = 6`

### `trig-identity-duel` — Trig Identity Duel (GCSE, A-Level, L4)

- **G21.1** · tiers: GCSE label (50); A-Level (49) excluded · **12** items, **12** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: Recall exact values of sin, cos, tan at 30/45/60 degrees with the other exact values as distractors. Inside G21.1. The other 38 GCSE items (sine rule, cosine rule, area = 1/2 ab sin C) are bold Higher content.
  - Covers: exact trig values
  - `\sin 30° -> \dfrac{1}{2}`
  - `\sin 60° -> \dfrac{\sqrt{3}}{2}`
  - `\sin 90° -> 1`

### `trig-worms` — Trig Worms (GCSE, A-Level)

- **G20.2, G20.4, G20.5, G20.7, G20.9, G20.1** · tiers: GCSE, A-Level labels · **274** items, **274** Foundation-pitched · **YES** · mode: procedural
  - Reasoning: generateQuestion(difficulty) read live: 274 distinct prompts in 300 draws, a lower bound of an unbounded space. Right-angled triangles, angles 15-85 in steps of 5, sides to 1 dp, calculator required. Foundation demand.
  - Covers: sin, cos, tan on right-angled triangles: find an angle (SOH/CAH/TOA), an opposite/adjacent from the hypotenuse, or a hypotenuse. tan is never used to find a side. Pythagoras (the other half of G20.1) is not tested
  - `"The opposite = 8, hypotenuse = 19. Find angle theta." -> 25 degrees (SOH)`
  - `"Angle theta = 30 degrees, hypotenuse = 12. Find the opposite side." -> sin 30 x 12`
  - `"Angle theta = 20 degrees, opposite = 7.5. Find the hypotenuse." -> 22`

### `unit-converter` — Unit Converter (GCSE, A-Level, L4)

- **N13.1, R1.1, G14.1** · tiers: GCSE, A-Level, L4 labels; one shared bank in five sections (L, A, V, T, E) · **58** items, **47** Foundation-pitched · **MIXED** · mode: procedural
  - Reasoning: 47 of 58 are Foundation-pitched: metric length (10), area cm2/m2/mm2 (15), volume/litres (15), five mixed-unit area/volume items and km/h and mph to m/s. The 8 engineering items (kPa, GPa, N/mm2) and 3 that need pi are not.
  - Covers: length, area, volume/capacity and speed conversions. No mass or time conversions in the bank
  - `[Length] Convert 2500 mm to m -> 2.5 m`
  - `[Engineering] Convert 72 km/h to m/s -> 20 m/s`
  - `[beyond Foundation] [Engineering] Convert 3500 N to kN -> 3.5 kN`

### `wrong-on-the-internet` — Wrong on the Internet (KS3, GCSE, Core)

- **N3.1** · tiers: ks3 (1), gcse (1) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/BIDMAS] {'username': '@QuickMathsKing', 'text': "2 + 3 × 4 = 20. Add first then multiply. That's how you read left to `
  - `[gcse/BIDMAS] {'username': '@MathsWhiz2009', 'text': '6÷2(1+2) = 1. OBVIOUSLY. Brackets first: 6÷2(3) = 6÷6 = 1. Anyone sayi`
- **N2.1, N8.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Fractions] {'username': '@DailyMathsPoll', 'text': 'Which fraction is bigger: 3/4 or 4/5?', 'likes': '2.1k', 'reshares': `
- **R9.1** · tiers: ks3 (1), gcse (1) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Percentages] {'username': '@HomeworkHelp', 'text': 'Quick — 15% of 60?', 'likes': '1.4k', 'reshares': '320', 'comments': '8`
  - `[gcse/Percentage Reductions] {'username': '@SalesMaths', 'text': '20% off then 20% off again. Total reduction?', 'likes': '3.5k', 'reshares`
- **N2.1, N1.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Negative Numbers] {'username': '@NegativesAreFun', 'text': '−3 + −5 = 2. Minus and minus makes plus!! Two negatives = positive. `
- **G16.1, G17.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Area vs Perimeter] {'username': '@ShapesMatter', 'text': 'The AREA of a 5cm × 3cm rectangle?', 'likes': '1.7k', 'reshares': '540'`
- **R5.1, R4.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Ratio] {'username': '@RatioKing', 'text': "Split £120 in ratio 2:3. Give one person £2 and the other £3. That's a rat`
- **P7.1, P8.1** · tiers: ks3 (2), gcse (2) · **4** items, **4** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Gambler's Fallacy] {'username': '@ProbabilityPete', 'text': "I've flipped heads 7 times in a row. The next flip MUST be tails. Th`
  - `[gcse/Gambler's Fallacy] {'username': '@NotAGambler', 'text': "12 reds in a row at roulette. I'm putting everything on black. MATHEMATI`
  - `[gcse/Probability AND] {'username': '@ProbMaster', 'text': 'P(A)=0.4, P(B)=0.3. P(A and B) = 0.4+0.3 = 0.7. Add them together — AND m`
- **N6.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Square Numbers] {'username': '@PatternSpotter', 'text': "1, 4, 9, 16... next term is 25! Add 3, then 5, then 7, then 9. So add`
- **S4.3** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Mean vs Median] {'username': '@AveragePoll', 'text': 'What does the MEAN tell you?', 'likes': '1.9k', 'reshares': '430', 'comm`
- **N4.1** · tiers: ks3 (1), gcse (1) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/HCF vs LCM] {'username': '@NumberFacts', 'text': 'HCF of 12 and 18 is 36. Just multiply them! HCF stands for Highest so yo`
  - `[gcse/Is 1 Prime?] {'username': '@PrimeNumbers', 'text': 'Is 1 a prime number?', 'likes': '4.5k', 'reshares': '1.8k', 'comments':`
- **G3.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Angles] {'username': '@AnglePoll', 'text': 'How many degrees in a triangle?', 'likes': '2.4k', 'reshares': '560', 'com`
- **A4.3** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Expanding Brackets] {'username': '@AlgebraForum', 'text': 'Simplify 3(x + 4)', 'likes': '1.1k', 'reshares': '230', 'comments': '67`
- **N15.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Rounding] {'username': '@RoundingMaster', 'text': 'Round 3.456 to 2 decimal places = 3.45. Just chop off the last digit.`
- **R11.1, R1.1** · tiers: ks3 (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[ks3/Speed] {'username': '@PhysicsFacts', 'text': 'Speed formula: Speed = Distance × Time', 'likes': '3.8k', 'reshares': '`
- **A4.4, A4.6** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Expanding Brackets] {'username': '@AlgebraHelp', 'text': 'Expand (x+3)²', 'likes': '2.4k', 'reshares': '670', 'comments': '1,345',`
- **A4.9, N7.1** · tiers: gcse (2) · **2** items, **2** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Index Laws] {'username': '@IndicesAreEasy', 'text': "x³×x⁴=x¹². Multiply powers when multiplying. 3×4=12. It's literally o`
  - `[gcse/Negative Indices] {'username': '@IndexPoll', 'text': 'What is 2⁻³?', 'likes': '3.4k', 'reshares': '890', 'comments': '2,345', 'p`
- **G20.1** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Pythagoras] {'username': '@RightTriangles', 'text': '5²+12²=hypotenuse. 25+144=169. Hypotenuse=169.', 'likes': '2.9k', 're`
- **S6.1, S6.2** · tiers: gcse (1), core (2) · **3** items, **3** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Correlation Causation] {'username': '@DataScience4All', 'text': 'Ice cream strongly correlates with drowning. THEREFORE ice cream CAU`
  - `[core/Correlation] {'username': '@StatsFacts', 'text': "r=0.95 between revision hours and exam scores PROVES revision causes good`
  - `[core/Regression Extrapolation] {'username': '@DataDrivenDecisions', 'text': "My regression line for ice cream sales vs temperature (10°C-30°C`
- **N9.1** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Standard Form Addition] {'username': '@BigNumbers', 'text': '2.5×10³ + 3.5×10³ = ?', 'likes': '2.1k', 'reshares': '560', 'comments': '`
- **A4.7** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Factorising] {'username': '@AlgebraGuru', 'text': 'Factorise x²+5x+6', 'likes': '1.8k', 'reshares': '340', 'comments': '987`
- **A9.1, A10.1** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Gradient] {'username': '@CoordinateGeom', 'text': "y=3x+7. What's the gradient?", 'likes': '1.5k', 'reshares': '290', 'c`
- **P8.1** · tiers: gcse (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[gcse/Probability Tree] {'username': '@TreeDiagram', 'text': 'P(A)=0.6, P(B\|A)=0.4. P(A and B) = 0.6+0.4 = 1.0. Certain! Probability t`
- **G25.1** · tiers: gcse (1) · **1** items, **0** Foundation-pitched · **NO** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
- **N16.1** · tiers: gcse (1) · **1** items, **0** Foundation-pitched · **NO** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
- **R16.1** · tiers: core (1) · **1** items, **1** Foundation-pitched · **YES** · mode: diagnostic
  - Reasoning: A social-media post contains a maths error; the student finds it then explains it (diagnostic). 1-2 items per topic.
  - Covers: one topic among many; see mode
  - `[core/Compound Interest] {'username': '@SavingsGuru', 'text': 'Invest £1000 at 5% for 20 years: £1000×1.05×20=£21,050. Retirement sorte`

## 5. Register, per covering game

A covering game is any game with at least one Foundation-pitched item recorded above. "Expected row" is canon §7.5.1 from the roster levels; "measured" is what the page renders (body background luminance, 0 = black, 1 = white; first font). A mismatch is reported as a fact, not a defect. "Start-screen tokens" are Year/KS/pupil/kid words in the visible start screen; "bank words" are school-age context words in the question bank (counts, excluding A-Level/L4 tiers). Emoji excludes the footer chrome.

| Game | Roster levels | Expected row | Measured | Font | Start-screen tokens | Emoji on start screen | School-age words in bank | Start-screen tagline |
|---|---|---|---|---|---|---|---|---|
| `angle-ace` | Year 6, KS3, GCSE | light | dark (0.04) ≠ | Outfit | Year 6×2, Year 7×1, KS3×1 | ⚡ | — | Angle Ace Find the angle. Name the reason. Both required — just like the exam. Every GCSE angle question requi |
| `bearing-blitz` | GCSE | dark | dark (0.02) | Outfit | — | ⚓ | — | ⚓ Bearing Blitz You are a submarine. Enemy ships are closing in. Set your bearing by eye — no numbers, no labe |
| `better-value` | GCSE, Core | dark | dark (0.07) | Outfit | — | — | school×8, lunch×7, canteen×5, year 5×1 | Better Value Phone contracts, energy tariffs, loan deals — compare the numbers and identify which option gives |
| `chart-interrogator` | GCSE, A-Level, Core, L4 | dark | dark (0.05) | Outfit | — | — | — | Chart Interrogator ← Back to Games Chart Interrogator Read statistical diagrams and build structured compariso |
| `component-crusher` | GCSE, A-Level, L4 | dark | dark (0.04) | Outfit | — | — | — | Component Crusher Break it into components — then put it back together. Vectors from column notation to 3D sca |
| `constructions-lab` | KS3, GCSE | light | light (0.98) | Outfit | — | 📐 | — | Constructions Lab Virtual compass and ruler. Learn by constructing. LEARNING TOOL — NOT A GAME 📐 How to use th |
| `coordinate-geometry-dash` | GCSE, A-Level | dark | dark (0.04) | Outfit | — | — | — | Coordinate Geometry Dash Midpoints. Gradients. Circles. Parametrics. See the geometry. GCSE A-Level GCSE: Midp |
| `core-maths-paper1` | Core | dark | dark (0.09) | Outfit | — | 📋 | homework×2, school×1, teacher×1 | MaffsGames Core Maths Paper 1 Practice AQA Level 3 Mathematical Studies — §3.1 & §3.2 📋 36 exam-style question |
| `core-maths-paper2a` | Core | dark | dark (0.09) | Outfit | — | 📊 | school×13 | MaffsGames Core Maths Paper 2A Practice AQA Level 3 Mathematical Studies — Statistical Techniques 📊 36 exam-st |
| `core-maths-paper2b` | Core | dark | dark (0.09) | Outfit | — | 🎲 | — | MaffsGames Core Maths Paper 2B Practice AQA Level 3 Mathematical Studies — Risk and Expectation 🎲 36 exam-styl |
| `core-maths-paper2c` | Core | dark | dark (0.09) | Outfit | — | 📈 | — | MaffsGames Core Maths Paper 2C Practice AQA Level 3 Mathematical Studies — Graphical Techniques 📈 36 exam-styl |
| `correlation-or-coincidence` | GCSE, A-Level, Core | dark | dark (0.04) | Outfit | — | 🧐 🪄 | — | Correlation or Coincidence? Two datasets. One question. Is it real — or just a coincidence? You'll see two lin |
| `decimal-detective` | Year 6 | light | dark (0.07) ≠ | Outfit | — | — | — | Decimal Detective Three types of decimal challenge. Can you crack every case? The Line-Up Five decimal suspect |
| `distinctly-average` | KS3, GCSE | light | light (0.95) | Nunito | KS3×2 | — | — | ← Back Distinctly Average KS3 SCORE 0 Q 0/0 BEST 0 x̄ Distinctly Average Whole-number data sets, 5 to 11 value |
| `equation-builder` | KS3, GCSE, L4 | light | dark (0.07) ≠ | Outfit | KS3×1, Year 7×1 | — | mum×1, school×1, canteen×1, lunch×1 | Equation Builder Aa Equation Builder Read the word problem. Build the equation from tiles. Translate language  |
| `estimation-engine` | KS3, GCSE, Core | light | dark (0.09) ≠ | Outfit | — | — | — | ESTIMATION ENGINE — QUESTION 0 SCORE 0 WITHIN TOL. — BEST ERROR READY TO BEGIN Within 5% Press Start Submit St |
| `estimation-golf` | Year 6, KS3, GCSE, A-Level, L4, Core | light | dark (0.3) ≠ | Courier Prime | YEAR 6×1, KS3×1 | ⛳ 💡 | pupils×1, school×1 | ← Back Estimation Golf 9 HOLES · PAR YOUR ESTIMATE · LOWEST SCORE WINS YEAR 6 KS3 GCSE A-LEVEL LEVEL 4 MaffsGa |
| `expected-damage` | KS3, GCSE, Core | light | dark (0.07) ≠ | Outfit | KS3×1, Year 7×1 | — | — | Expected Damage A calculator trolley is rolling down the track. Muppets — oblivious phone-zombies — are in the |
| `factor-race` | Year 6, KS3, GCSE | light | light (0.96) | Nunito | — | ⚡ | — | ← Back ⚡ FACTOR RACE SCORE 0 STREAK 0 BEST 0 ⚡ FACTOR RACE Two numbers appear. Tap the one with more factors.  |
| `formula-forge` | GCSE, A-Level, L4 | dark | dark (0.04) | Outfit | — | — | — | Formula Forge Rearrange. Isolate. Master the subject change. GCSE A-Level Level 4 Stage 1: One Step Single inv |
| `formula-plug-in` | Year 6 | light | dark (0.07) ≠ | Outfit | — | — | — | Formula Plug-In You're given a formula and the values. Plug them in, calculate the answer. This is substitutio |
| `formula-unlocked` | GCSE, A-Level, L4 | dark | dark (0.04) | Outfit | — | — | — | Formula Unlocked Make the subject. Show the steps. Use hints if you need them. GCSE A-Level Level 4 Stage 1: O |
| `four-quadrant-explorer` | Year 6 | light | dark (0.07) ≠ | Outfit | Year 7×1 | — | — | Four Quadrant Explorer Plot points, read coordinates and complete shapes across all four quadrants. In primary |
| `given-that` | GCSE, A-Level, Core, L4 | dark | dark (0.07) | Outfit | — | — | homework×5, lunch×5, sweet×4, year 9×4, canteen×2, school×1 | Given That Conditional probability trainer. See the full picture, then zoom in on a condition and find the new |
| `gradient-hunter` | GCSE, Core, A-Level | dark | dark (0.07) | Outfit | — | — | school×3 | Gradient Hunter Click points, find gradients, interpret rates of change Click two points on a real-world graph |
| `graph-sketcher` | Core, A-Level, L4 | dark | dark (0.04) | Outfit | — | — | — | Graph Sketcher Can you complete the table — and draw what it means? Complete tables of values, sketch curves,  |
| `growth-and-decay` | Core, A-Level, L4 | dark | dark (0.04) | Outfit | — | — | — | Growth and Decay What does the model tell you — and what can you find from it? Exponential modelling — substit |
| `index-laws` | GCSE, A-Level | dark | light (0.98) ≠ | Outfit | — | — | — | ← Back Index Laws GCSE / A-LEVEL SCORE 0 STREAK 0 BEST 0 x^n Index Laws Six rules. All tested. Can you apply t |
| `like-terms-collector` | Year 6 | light | light (0.98) | Outfit | Year 7×1 | — | — | Like Terms Collector Collecting like terms is the first thing Year 7 students learn in algebra. By the end of  |
| `linear-equation-solver` | GCSE | dark | dark (0.04) | Outfit | — | — | — | Linear Equation Solver Pick the move. Undo it step by step. Say what x is. GCSE One-step Two-step Negatives Fr |
| `maths-court` | KS3, GCSE, Core | light | dark (0.07) ≠ | Outfit | KS3×1, Year 7×1 | — | school×1 | Maths Court Three arguments. One correct answer. You're the judge. Read the working, find the truth, deliver t |
| `negative-number-line` | Year 6 | light | dark (0.07) ≠ | Outfit | — | — | — | Negative Number Line Three question types test your understanding of negative numbers: place them, order them, |
| `new-shapes` | Year 6 | light | dark (0.07) ≠ | Outfit | Year 7×1 | — | — | New Shapes In primary school you learned area of rectangles and triangles. Year 7 introduces two new shapes —  |
| `percentage-flip` | Year 6, KS3, GCSE | light | light (0.96) | Nunito | — | — | — | ← Back 🃏 PERCENTAGE FLIP SCORE 0 Q 0/10 BEST 0 🃏 PERCENTAGE FLIP Type your answer, then flip the card to see i |
| `prime-factorisation` | Year 6, KS3, GCSE | light | light (0.99) | Nunito | — | ✓ ❤ 🌳 | — | ← Back 🌳 PRIME SPRINT SCORE 0 Q 0/8 LIVES ❤️ ❤️ ❤️ TIME 🌳 PRIME SPRINT Build each number from its prime factor |
| `prime-or-composite` | KS3, GCSE | light | dark (0.09) ≠ | Outfit | — | — | — | PRIME OR COMPOSITE — QUESTION 0 SCORE 0 STREAK — ACCURACY ACADEMIC YEAR 2026/27 6 7 Yes. That 6 7. But here's  |
| `probability-paradox` | GCSE, Core | dark | dark (0.05) | Outfit | — | — | teacher×1, school×1 | Probability Paradox Your intuition is wrong. Let the simulation prove it. PARADOXES Paradox Predictor A famous |
| `probability-pioneer` | Year 6 | light | dark (0.07) ≠ | Outfit | — | — | — | Probability Pioneer Probability is one of the most useful topics in secondary school — and in real life. It's  |
| `proportion-blaster` | GCSE, A-Level | dark | dark (0.07) | Outfit | — | — | sweets×1 | Proportion Blaster Direct. Inverse. Algebraic. Can you find the constant? GCSE A-Level GCSE: y ∝ x, y ∝ x², y  |
| `quadratic-factoriser` | GCSE, A-Level | dark | dark (0.07) | Outfit | — | — | — | ← Back Quadratic Factoriser GCSE SCORE 0 Q 0/0 BEST 0 x² Quadratic Factoriser Factorise the quadratic by findi |
| `scale-factor-scaling` | GCSE, A-Level, L4 | dark | dark (0.04) | Outfit | — | — | — | Scale Factor Scaling Length scales by k. Area scales by k². Volume scales by k³. GCSE A-Level Level 4 If a len |
| `sequence-solver` | KS3, GCSE, A-Level, L4 | light | dark (0.04) ≠ | Outfit | KS3×2 | — | — | Sequence Solver Spot the pattern. Find the rule. What comes next? KS3 GCSE A-Level KS3: Arithmetic sequences,  |
| `shape-shifter` | Year 6 | light | dark (0.07) ≠ | Outfit | Year 7×1 | — | — | Shape Shifter Transformations — moving, flipping and rotating shapes — is one of the most visual topics in Yea |
| `simultaneous-solver` | GCSE, A-Level | dark | dark (0.05) | Outfit | — | — | — | Simultaneous Solver Solve the system. Find the unknowns. GCSE A-Level GCSE: Linear simultaneous equations A-Le |
| `split-it` | KS3, GCSE | light | light (0.95) | Nunito | — | ⚖ ✂ 🍕 💰 📏 🥧 | — | ← BACK SPLIT IT SPLIT IT Six ratio skills. Pick your mode and level. ✂️ Simplify Write the ratio in its simple |
| `spot-the-error` | KS3, GCSE, L4 | light | dark (0.07) ≠ | Outfit | KS3×1, Year 7×1 | — | school×4, teacher×3, lunch×1, year 9×1 | Spot the Error Aa Spot the Error Read the word problem. Find the mistake in the working. Then find the misread |
| `spot-the-muppet` | KS3, GCSE, Core | light | light (0.98) | Outfit | KS3×1 | — | sweets×2 | MUPPET SPOTTED! Spot the Muppet A confident character gives spectacularly wrong maths advice. Your job: identi |
| `standard-form-blitz` | GCSE, A-Level | dark | dark (0.05) | Outfit | — | — | — | Standard Form Blitz Powers of ten. Big numbers. Tiny numbers. Fast. GCSE A-Level GCSE: Convert, order, multipl |
| `stat-attack` | GCSE, Core, L4 | dark | dark (0.04) | Outfit | — | — | pocket money×3, homework×3, school×2 | Stat Attack Can you calculate the standard deviation from a frequency table? Grouped frequency tables — modal  |
| `tax-theft` | Core | dark | dark (0.07) | Outfit | — | — | — | Tax Theft Core Maths ← Back to Games Choose Your Salary Band Work out income tax, National Insurance, and mont |
| `terrible-advice` | KS3, GCSE, Core | light | light (0.98) | Outfit | KS3×1 | — | sweets×3 | Terrible Advice The world's worst financial advisors, life coaches and self-proclaimed maths experts are givin |
| `think-of-a-number` | Year 6 | light | dark (0.07) ≠ | Outfit | — | — | — | Think of a Number Professor Puzzler thinks of a number and gives you clues. Can you work backwards to find it? |
| `trig-identity-duel` | GCSE, A-Level, L4 | dark | dark (0.04) | Outfit | — | — | — | Trig Identity Duel Sine rule. Cosine rule. Identities. Prove yourself. GCSE A-Level GCSE: Sine rule, cosine ru |
| `trig-worms` | GCSE, A-Level | dark | dark (0.07) | Outfit | — | 🐛 💥 | — | ← Back Trig Worms SCORE 0 LEVEL 1 BEST 0 🐛💥 TRIG WORMS Your worm has a cannon. Use SOH CAH TOA to aim it corre |
| `unit-converter` | GCSE, A-Level, L4 | dark | dark (0.04) | Outfit | — | — | — | Unit Converter Length. Area. Volume. Get the conversion factor right. GCSE A-Level Level 4 1 m = 100 cm. So 1  |
| `wrong-on-the-internet` | KS3, GCSE, Core | light | dark (0.07) ≠ | Outfit | KS3×1 | — | school×1, year 6×1 | Wrong on the Internet Someone is confidently wrong on the internet. Read their post, find the correct answer,  |

**Facts.** Of 56 covering games, 19 render a different row from the one §7.5.1 gives them (marked ≠). Only 10 render light: `constructions-lab`, `distinctly-average`, `factor-race`, `index-laws`, `like-terms-collector`, `percentage-flip`, `prime-factorisation`, `split-it`, `spot-the-muppet`, `terrible-advice`. Of the nine Year 6-only games, eight render dark; only `like-terms-collector` renders light. `index-laws` (GCSE, A-Level) renders light. Five games use Nunito with the Press Start 2P pixel font in their source: `distinctly-average`, `factor-race`, `percentage-flip`, `prime-factorisation`, `split-it`; `split-it` also puts emoji on every mode card.

**Year-group wording on start screens** (quoted): `equation-builder` level cards read "KS3 Year 7-9 · GCSE Year 10-11 · Level 4 HNC/HND"; `expected-damage` reads "KS3 — Year 7-9"; `angle-ace` reads "Year 6 → Year 7. This is real KS3 maths"; `four-quadrant-explorer` says "exactly what Year 7 students learn in their first few weeks"; `like-terms-collector` says "the first thing Year 7 students learn in algebra"; `estimation-golf` lists YEAR 6 · KS3 as level buttons. `estimation-golf` also renders a mid-grey body (luminance 0.30) in a Courier Prime face.

**School-age context words in question banks** (three or more hits): `better-value` (21), `given-that` (21), `core-maths-paper2a` (13), `spot-the-error` (9), `stat-attack` (8), `core-maths-paper1` (4), `equation-builder` (4), `gradient-hunter` (3), `terrible-advice` (3). The words counted are Year 5-9, pupil(s), homework, sweets, pocket money, mum, dad, teacher, playground, school, classroom, lunch, canteen and kid(s); a Year 12 resit student may or may not read a school canteen as childish, so the counts are a fact list, not a verdict. Generator games (`split-it`, `tax-theft`, `bearing-blitz`) were sampled: `split-it` uses stickers, pencils, rubbers, smoothies and pancakes; `tax-theft` and `bearing-blitz` use adult contexts (payslips; a submarine).

## 6. Escape rooms — listed, no verdict

Each row is a lock, read from `room.js` with the variant-0 figures filled in. "Foundation part(s)" is the file's wording the lock exercises; a note says where a lock is beyond Foundation. Eight rooms are live; `it-vengeance` and `car-trap` are withdrawn behind `noindex` holding pages. Each room is about 15 minutes with three locks; each lock draws one of 2-10 verified number sets per play.

| Room | Status / label | Lock | Instrument | Foundation part(s) addressed | Variant-0 worked line |
|---|---|---|---|---|---|
| `hamster-heist` | live, KS3 label | `hamster-wheel-rpm` | slider | G17.1 (circumference = πd), R11.1 (turns per second to per minute) | Circumference = 20π cm. 120π ÷ 20π = 6 turns a second, ×60 = 360 RPM. |
| `hamster-heist` | live, KS3 label | `hamster-feeder-bounds` | slider | N16.1 (lower bound of a rounded measurement); bounds are underlined in the file but Higher in practice | Lower bound of depth = 14.5 cm. Volume = 40 × 14.5 = 580 cm³. |
| `hamster-heist` | live, KS3 label | `heat-lamp-gradient` | slider | A10.1, R14.1 (gradient as a rate from two readings) | Gradient = (39−21) ÷ (16−4) = 18 ÷ 12 = 1.5 °C/min. |
| `pe-shed-rebellion` | live, KS3 label | `sprinkler-sector-area` | dial | G18.1 (sector angle from area), G17.1; sector calculations are underlined in the file | Whole circle = π × 12² = 144π. 48π ÷ 144π = 1/3, and 1/3 of 360° is 120°. |
| `pe-shed-rebellion` | live, KS3 label | `dodgeball-pressure-boyle` | dial | R13.1/R10.1 (inverse proportion, P × V constant) | Inverse proportion: P×V is constant. k = 20×60 = 1200, so P = 1200÷25 = 48 psi. |
| `pe-shed-rebellion` | live, KS3 label | `locker-nth-term` | dial | A25.1, A23.1 (linear sequence extended from three known terms) | Step = (68−23) ÷ (12−3) = 5 a day. Day 15 = 68 + 3×5 = 83. |
| `prom-budget` | live, GCSE label | `finance-reverse-percentage` | keypad | R9.1 (original value after a percentage increase) | £2160 is 120% of the quote. 2160 ÷ 120 × 100 = £1800. |
| `prom-budget` | live, GCSE label | `dj-deposit-compound` | slider | R16.1 (compound interest, find the number of years) | 1000 × 1.1^n = 1610.51, which gives n = 5 years. |
| `prom-budget` | live, GCSE label | `wifi-venn-router` | dial | P6.2, P6.1 (two-set Venn, find the overlap) | 80 − 12 = 68 want something. 48 + 37 − both = 68, so both = 17. |
| `canteen-hack` | live, KS3 label | `canteen-mean-calories` | slider | S4.3 (mean of five, find the missing value) | 450 × 5 = 2250 kcal for the day. The four logged come to 2150, so the fifth is 2250 − 2150 = 100 kcal. |
| `canteen-hack` | live, KS3 label | `cookie-price-simultaneous` | pair | A19.1 (linear simultaneous equations by elimination) | Second line × 3: 3C + 12P = 42. Subtract the first line (3C + 2P = 12): 10P = 30, so P = £3 and C = £2. |
| `canteen-hack` | live, KS3 label | `kale-fraction-drain` | dial | N12.1 (fraction of an amount, then subtract) | ^2/_9 of 180 = 40 portions stay on the shelf, so 140 portions go down the chute. |
| `heatwave-mutiny` | live, KS3 label | `patrol-lcm-timer` | slider | N4.1 (LCM of three numbers via prime factorisation) | LCM of 12, 15 and 18: 12 = 2^2 × 3, 15 = 3 × 5, 18 = 2 × 3^2, so the LCM is 2^2 × 3^2 × 5 = 180 minutes. |
| `heatwave-mutiny` | live, KS3 label | `cube-surface-volume` | keypad | G16.1, N6.1 (surface area to edge to volume, square and cube roots) | One face = 1350 ÷ 6 = 225 cm². Edge = √225 = 15 cm. Volume = 15³ = 3375 cm³. |
| `heatwave-mutiny` | live, KS3 label | `canteen-freezer-inequality` | dial | A22.1 (double inequality), N4.1 (identify the prime) | 25 < 3f < 37, so 8.33 < f < 12.33, leaving 9, 10, 11, 12. Only 11 is prime. |
| `rugby-mud` | live, GCSE label | `elbow-patch-scale` | dial | G19.1, R12.1 (area scale factor from a linear one) | Length s.f. = 5/15, so area s.f. is that squared. 90 ÷ 9 = 10 cm². |
| `rugby-mud` | live, GCSE label | `sprinkler-flow-rates` | dial | combined rates (1/20 + 1/30): beyond Foundation, not a Foundation part | Rates add: 1/20 + 1/30 = 1/12 of a soaking an hour, so one full soaking takes 12 hours. |
| `rugby-mud` | live, GCSE label | `rugby-scoreboard-bases` | pair | A4.9/N7.1 (index laws with bases 2 and 4) plus two unknowns: grade 6+ in demand | 2^H × 4^A = 2^H+2A = 2^17, so H + 2A = 17, with A = H + 4. That gives Home 3, Away 7. |
| `comic-caper` | live (GCSE resit), GCSE label | `chokey-factor-count` | dial | N4.1 (factors of a number) | 1, 2, 3, 4, 6, 8, 12, 24 → 8 factors. |
| `comic-caper` | live (GCSE resit), GCSE label | `chokey-prime-volumes` | dial | N4.1 (primes up to 30) | 2, 3, 5, 7, 11, 13, 17, 19, 23, 29 → 10. |
| `comic-caper` | live (GCSE resit), GCSE label | `chokey-hcf-bundles` | slider | N4.1 (HCF of two numbers in context) | Factors of 18: 1, 2, 3, 6, 9, 18. Factors of 45: 1, 3, 5, 9, 15, 45. Highest common factor 9. |
| `kiln-disaster` | live (GCSE resit), GCSE label | `kiln-sensor-limit` | keypad | N4.1 (multiples, highest below a limit) | Multiples of 9: 72, 81, 90. The highest under 85 is 81. |
| `kiln-disaster` | live (GCSE resit), GCSE label | `kiln-fan-restart` | dial | N4.1 (LCM of two numbers in context) | Multiples of 6: 6, 12, 18, 24, 30, 36, 42. Multiples of 14: 14, 28, 42. Lowest common multiple 42. |
| `kiln-disaster` | live (GCSE resit), GCSE label | `kiln-cancel-check` | slider | N3.1 (order of operations) | 45 ÷ 3 = 15. 21 + 15 = 36. |
| `it-vengeance` | withdrawn, GCSE label | `mechanical-keyboard-perms` | dial | N5.2 permutations with repeats: bold, not Foundation | 4! ÷ 2 = 24 ÷ 2 = 12 distinct passcodes. |
| `it-vengeance` | withdrawn, GCSE label | `vault-trajectory-vertex` | slider | A11.1 turning point of a quadratic by -b/2a: beyond Foundation | t at the peak = −b/2a = 1.2 s, and substituting back gives h = 3.0 m. |
| `it-vengeance` | withdrawn, GCSE label | `mat-tiling-hcf` | slider | N4.1 (HCF with decimals converted to tenths) | In tenths, HCF(48, 72) gives the largest square mat: 2.4 m (2 by 3 of them). |
| `car-trap` | withdrawn, GCSE label | `visitor-space-bounds` | dial | N16.1 (lower bounds of length and width, then area) | Lower bounds of 5.5 m and 2.5 m multiply to 13.75 m², so the dial goes to 13.75 litres. |
| `car-trap` | withdrawn, GCSE label | `boom-gate-sector` | dial | G18.1 (arc to angle), G17.1 (circumference) | Full circumference = 2π × 3 = 6π m. The arc is 0.75π m, which is ^1/_8 of the circle, so the angle is 45°. |
| `car-trap` | withdrawn, GCSE label | `ev-charger-quadratic` | dial | A18.3 (solve a quadratic by factorising, reject one root) | x² − 12x + 35 = (x − 5)(x − 7), so x = 5 or 7. The alarm limit of 6 A rules out 7, leaving 5 A. |

**Room facts.** `comic-caper` and `kiln-disaster` are wholly Number strand N3/N4 (factors, primes, HCF, multiples, LCM, order of operations): six locks, all inside Foundation-assessable parts, none needing a formula. The other eight rooms place Foundation content next to Higher: bounds and sector/arc work are underlined in the file but graded Higher in practice, and `rugby-mud` and `it-vengeance` each carry a lock that is not Foundation content. The rooms are the only Foundation evidence anywhere in the library for **N8.3 multiples of π** (`hamster-wheel-rpm`, `sprinkler-sector-area`, `boom-gate-sector`) and **G18.1 arc and sector** (`sprinkler-sector-area`, `boom-gate-sector`); both are GAP in the games. `canteen-freezer-inequality` adds a second source for **A22.1 inequalities**, which has one diagnostic game item.

## 7. Considered and not counted

| Game | Why it is not evidence for a Foundation part |
|---|---|
| `word-problem-decoder` | Recognition only: the student names the topic (110 items across 24 topics, Ratio, Percentages, Fractions, Reverse Percentage and others). It never asks for the working. Not counted; a resit student could still use it as a "which method" warm-up. |
| `fraction-equivalence` | Are two fractions equivalent (20 yes/no items, denominators up to 10). Underpins fraction work but no DfE Foundation part is worded as equivalence; closest N8.1/N10.1, neither attributed. |
| `equatle` | A Wordle for 8-character arithmetic equations. The student finds a valid equation; it does not practise a stated skill. Read from `getBank()` source. |
| `modular-battle` | Remainders (a mod b, a 10-60, b 2-9). Modular arithmetic is not in the GCSE specification; division with remainders is only implicit in N2. |
| `circle-theorem-spotter` | 55 items, all circle theorems (angle at centre, cyclic quadrilateral, alternate segment, tangent-radius). Circle theorems are G10, which is not a Foundation part; G9.1 (naming centre, radius, chord, tangent) is not tested as vocabulary. Not attributed to G9. |
| `surd-simplifier` | Surds are bold in N8.2/N8.4. (`A4.1`'s "surds" fragment is typed standard; see §1.1.) |
| `expectation-station` | E(X) from a probability table (Core Maths S3.9), not the Foundation expected-outcomes skill in P2.1. |
| `screening-room` | False positives and base rates from a population (Core Maths). |
| `trig-wars` | Projectile artillery: set an angle and a power. Not a question bank; the maths is A-level mechanics. |
| `graph-transformer` | Transformations of y = f(x) (601 match samples): Higher / A-level graph transformations. |
| higher-power, 52dle, seven-bridges, prisoners-dilemma, truth-buster, glorious-gantt, boolean-blitz, truth-will-set-you-free | Constants, puzzles, game theory, critical-path analysis and Boolean algebra. No Foundation part addressed. |
| A-Level, Further and L4 games | binomial-blaster, characteristic-quest, complex-converter, curling-friction, differentiation-duel, dimension-checker, eigenvalue-extractor, eigenvector-engine, factor-theorem, force-resolver, integration-duel, log-laws, matrix-crunch, moments-master, normal-navigator, partial-fractions-duel, proof-builder, suvat, test-the-claim, and the A-Level tier of games that also serve GCSE. Screened by roster tag and by reading start, middle and end of each bank, not item by item. |

## 8. Observations made in passing

Facts noticed while reading banks; none is acted on here.

- **`split-it`'s unitary mode can emit a degenerate item.** Sampled live: "A car travels 120 miles in 2 hours. How far in 2 hours?" (answer 120).
- **`prime-or-composite` runs to 9,973** (`n` = 2 to 9,973; 42 of 66 items exceed 100), which a Foundation student cannot judge without a calculator.
- **Roster counts and extracted counts differ** for some banks that build part of their content at run time (`negative-number-line` roster 45, extracted 30; `equation-builder`, `spot-the-error` and `word-problem-decoder` carry three tiers in one 110-120 item array). This audit uses extracted counts.
- **`percentage-flip` repeats questions across its two banks** (32 items, 29 distinct).
- **`proportion-blaster` GCSE mixes tiers of difficulty**: y = kx and y = k/x (Foundation-assessable) sit beside y = kx² and y = k/x² (Higher) in one 50-item tier, with ratio and percentage items after them.
- **Mixed difficulty inside one GCSE tier.** `unit-converter`: 11 of 58 items are not Foundation-pitched (8 engineering-unit items and 3 that need π). `sequence-solver` GCSE tier: 9 quadratic nth-term items (bold A25.2) sit among linear ones.

## 9. Source data and reproduction

- Spec: `data/dfe-gcse-parts.json` (`129` Foundation parts of 174). Game side: `python scripts/extract-banks.py` output in `data/banks/` (gitignored), generators as §1.2, rooms from `escape-rooms/*/room.js`.
- Repository state audited: `main` at `81b341a`, 30 Sep 2026. Nothing under `games/`, `escape-rooms/`, `data/`, `scripts/`, the portal, `spec-map/` or the roster was changed.

## 10. Grade 1–3 banding (Jon's ruling, 30 Sep)

**Added 30 Sep 2026, on `main` after this audit merged (PR 18). Sections 1–9 are unchanged.** Jon's ruling: every one of the 129 Foundation parts is tagged **CORE**, **STRETCH** or **OUT** for a grade 1–3 student. **All 129 are now tagged.** The first version left 30 parts, in 11 questions, for Jon to rule rather than guessing; he ruled Q1 (graphs) and Q3 (shape vocabulary) first (§10.1a) and the rest the same day (§10.3). Every part-level ruling is his; the author placed only the parts the band lists decide. The banding changes no verdict above; it only sorts them. No game, room or page was touched.

### 10.1 The bands, and how they were applied

**CORE** — place value and ordering incl. negatives; four operations with integers, decimals, fractions; order of operations; factors, multiples, primes, HCF/LCM; squares, cubes, roots; FDP conversion; fractions and percentages of amounts; rounding and estimation; standard units and conversions incl. time; ratio notation and sharing; simple direct proportion and best buys; speed; algebraic notation, substitution, collecting like terms, expanding one bracket; one- and two-step linear equations; sequences and nth term; coordinates; angle facts; perimeter and area of rectangles, triangles, circles; reading scales; charts and averages; basic probability.

**STRETCH** — unknowns on both sides, inequalities, standard form, compound measures, simple interest and percentage change, volume of prisms, frequency trees, Venn diagrams.

**OUT** — everything else (e.g. Pythagoras, trigonometry, quadratics, simultaneous equations, vectors, enlargement, arc/sector).

**Amendment, 30 Sep 2026 (Jon).** The first version of the bands omitted graphs and shape properties; Jon confirmed that was an oversight and ruled: **CORE** — plotting straight-line graphs from a table of values; reading and interpreting real-life graphs (conversion, distance–time); shape vocabulary and properties (`G1.1`, `G4.1`, `G12.1`). **STRETCH** — gradient and intercept, y = mx + c; recognising non-linear graph shapes. The five graph parts were checked one by one against that intent (§10.1a).

**Second amendment, 30 Sep 2026 (Jon).** The remaining questions were ruled part by part; §10.3 records each ruling. Where a part-level ruling and the band lists above disagree, **the ruling wins**: for example `G16.1` is CORE although volume of prisms is STRETCH, and `P6.1`/`P6.2` are CORE although Venn diagrams are STRETCH.

Rules used to place a part, so the tags can be re-run if a band moves:

1. **The band lists are read as exhaustive.** A skill named in neither CORE nor STRETCH is OUT, unless a named phrase could plausibly cover it *and* the answer matters; those went to Jon (§10.3).
2. **A fragment takes the band of the skill it belongs to** (the same rule §1.1 uses for verdicts). `A22.3` "variable(" is STRETCH because `A22.1` is; `G20.3` "and" is OUT because `G20.1` is.
3. **A composite part is tagged by its principal (main-clause) skill.** A named sub-skill in a different band is recorded in §10.6, not tagged separately, because the audit's verdict is one per part. Where no principal skill could be picked, the part went to Jon (§10.3).
4. **THIN that depends only on the spot-the-error family is treated as GAP, and marked GAP†.** "The spot-the-error family" is read as the five diagnostic games §1.7 names: `spot-the-error`, `spot-the-muppet`, `terrible-advice`, `wrong-on-the-internet`, `maths-court`. A THIN whose only evidence is one to five diagnostic items is a GAP in practice: a student cannot practise a skill by finding it wrong once. Jon confirmed this set (30 Sep). The audit's own verdict column is unchanged; GAP† appears only in this section.

#### 10.1a How the Q1 and Q3 rulings were applied

| Part | Text of the part | Placed | Why |
|---|---|---|---|
| `A9.1` | plot graphs of equations that correspond to straight-line graphs in the coordinate plane | **CORE** | Plotting straight-line graphs. The "from a table of values" method is not in the wording; the part is CORE on the skill it names. |
| `A10.1` | identify and interpret gradients and intercepts of linear functions graphically and algebraically | **STRETCH** | Gradient and intercept: exactly the STRETCH clause. |
| `A14.1` | plot and interpret graphs | **CORE** | Generic head clause of A14; the reciprocal and exponential graphs sit in fragments `A14.2` and bold `A14.3`, tagged apart. Fits "plot… interpret", read as straight-line and real-life graphs. |
| `A14.4` | …graphs of non-standard functions in real contexts, to find approximate solutions to problems such as simple kinematic problems involving distance, speed and acceleration | **CORE** | Real-life graphs incl. distance–time. "Acceleration" (velocity–time) goes beyond the two examples Jon gave; tagged CORE on the real-context clause, noted in §10.6. |
| `A12.1` | recognise, sketch and interpret graphs of linear functions, quadratic functions, | **STRETCH** (Q1R) | Did not fit cleanly: linear recognition is CORE-side, but the part also names quadratic graphs. Left for Jon as Q1R and **ruled STRETCH** (§10.3). |
| `G1.1`, `G4.1`, `G12.1` | shape terms and notation; quadrilaterals and other plane figures; faces, edges and vertices of solids | **CORE** | Ruled by Jon: shape vocabulary and properties. Note `G1.1`'s wording also includes constructions/notation for symmetry; tagged on the vocabulary. |

**Knock-on, ruled (Q1R):** "recognising non-linear graph shapes" could have read onto `A12.2`, `A12.3`, `A12.4` (cubic and reciprocal graphs) and `A14.2` (reciprocal graphs). Jon ruled they **stay OUT**.

### 10.2 Totals

| Band | Parts | COVERED | THIN | GAP† | GAP |
|---|---|---|---|---|---|
| CORE | 65 | 41 | 6 | 4 | 14 |
| STRETCH | 11 | 2 | 3 | 3 | 3 |
| OUT | 53 | 19 | 15 | 5 | 14 |
| **Total** | **129** | **62** | **24** | **12** | **31** |

Reconciliation to §2: COVERED 62 = 62; THIN 24 + GAP† 12 = 36 = the audit's 36 THIN; GAP 31 = the audit's 31 GAP. 65 CORE + 11 STRETCH + 53 OUT = 129; none awaits a ruling.

### 10.3 The questions Jon ruled (30 Sep)

The first version of this section left 30 parts untagged and uncounted, in 11 questions, because none could be placed without a judgement call; `A12.1` was held back as Q1R when Q1 was applied, and four OUT parts were queried alongside it. Jon ruled all of them on 30 Sep. The table records each question, the audit verdict and the ruling. **A GAP or THIN part ruled CORE is now in the §10.4 build list; a COVERED part ruled CORE is now in the §10.5 suite.**

| Q | Question | Part | Verdict | Ruled | Note |
|---|---|---|---|---|---|
| Q1 | Graphs (ruled with the band amendment, §10.1a) | `A9.1` | GAP† | **CORE** |  |
|  |  | `A10.1` | THIN | **STRETCH** | Gradient and intercept. |
|  |  | `A14.1` | THIN | **CORE** |  |
|  |  | `A14.4` | THIN | **CORE** |  |
| Q1R | Graphs residual: A12.1, and whether non-linear shapes move A12.2–A12.4, A14.2 | `A12.1` | THIN | **STRETCH** | Linear and quadratic graphs in one part. |
|  |  | `A12.2` | THIN | **OUT** | Stays OUT (Jon). |
|  |  | `A12.3` | THIN | **OUT** | Stays OUT (Jon). |
|  |  | `A12.4` | THIN | **OUT** | Stays OUT (Jon). |
|  |  | `A14.2` | THIN | **OUT** | Stays OUT (Jon). |
| Q2 | Scatter graphs and lines of best fit | `S6.1` | THIN | **CORE** |  |
|  |  | `S6.2` | COVERED | **CORE** |  |
| Q3 | Shape vocabulary and properties (ruled with the band amendment) | `G1.1` | GAP | **CORE** |  |
|  |  | `G4.1` | GAP | **CORE** |  |
|  |  | `G12.1` | GAP | **CORE** |  |
| Q4 | Circle vocabulary, and answers left in terms of π | `G9.1` | GAP | **CORE** |  |
|  |  | `G9.2` | GAP | **OUT** | Tangent, arc, sector, segment. |
|  |  | `N8.3` | GAP | **STRETCH** | Answers in terms of π. |
| Q5 | Expressing one quantity as a fraction or ratio of another | `R3.1` | GAP | **CORE** |  |
|  |  | `R6.1` | GAP | **CORE** |  |
| Q6 | Scale drawings, maps, measuring lines and angles | `R2.1` | GAP† | **CORE** |  |
|  |  | `G15.1` | COVERED | **CORE** | **Bearings remain OUT as a topic** (Jon): the part is CORE for measuring lines and angles, maps and scale drawings. |
| Q7 | Algebra edges | `A3.1` | GAP | **CORE** |  |
|  |  | `A4.1` | GAP | **CORE** | **CORE excluding its surd clause** (Jon). Surd items are not evidence for this part. |
|  |  | `A4.9` | COVERED | **STRETCH** | Index laws. |
|  |  | `A5.1` | COVERED | **CORE** |  |
|  |  | `A7.1` | GAP† | **CORE** |  |
|  |  | `A21.1` | COVERED | **CORE** | **CORE, linear only** (Jon). "Two simultaneous equations" stays OUT. |
| Q8 | G16.1, a part straddling three bands | `G16.1` | COVERED | **CORE** | Whole part CORE, incl. prism volume (Jon). |
| Q9 | Probability edges | `P1.1` | GAP | **CORE** |  |
|  |  | `P5.1` | GAP | **STRETCH** | Sample size and relative frequency. |
|  |  | `P6.1` | COVERED | **CORE** | Venn and tree diagrams CORE here by ruling. |
|  |  | `P6.2` | COVERED | **CORE** | Fragment of P6.1. |
| Q10 | Error intervals | `N15.2` | THIN | **STRETCH** | Error intervals. |
| Q11 | Describing a population | `S5.1` | GAP | **OUT** | Too general to place; OUT (Jon). |

### 10.4 CORE gaps and thins, ranked by parts closed

Of the 65 CORE parts, **24 are not COVERED**: 14 GAP (`N10.1`, `A1.1`, `A3.1`, `A4.1`, `R3.1`, `R6.1`, `G1.1`, `G4.1`, `G9.1`, `G12.1`, `P1.1`, `S2.1`, `S2.2`, `S2.3`), 4 GAP† (`N8.1`, `A7.1`, `A9.1`, `R2.1`; each rests only on diagnostic-game items) and 6 THIN (`A14.1`, `A14.4`, `G11.1`, `G17.1`, `P4.1`, `S6.1`). Jon's rulings (§10.1a, §10.3) added fifteen of them to the nine the band lists gave. "Closes" means the build would give one game 10 or more Foundation-pitched items for the part. `G17.1` stays THIN by rule 4 only because one `estimation-golf` item sits beside its diagnostic ones; **for build purposes it is treated as GAP (Jon, 30 Sep)**.

The verdict rule is per part, so it hides CORE sub-skills the audit's own notes say no game practises (§3 sub-skill notes). Those are counted separately in the last column: they would not change a verdict, but a resit suite that skips them has a hole the table above does not show. Ranked by total parts; ties broken by formal parts first, then by fewest Foundation items already in the library.

| Rank | Build target | Formal CORE GAP / THIN it closes | Parts with a missing CORE sub-skill it also fills | Total |
|---|---|---|---|---|
| 1 | Fractions and decimals: arithmetic, ordering, conversion, of an amount, one quantity as a fraction of another (the planned fractions game) | 4 (`N8.1`, `N10.1`, `R3.1`, `R6.1`) | 3 (`N2.1`, `N1.1`, `N12.1`) | **7** |
| 2 | Shape vocabulary and properties: terms, quadrilaterals, solids, circle parts (the shape-vocabulary game) | 4 (`G1.1`, `G4.1`, `G12.1`, `G9.1`) | 0 | **4** |
| 3 | Charts: read and construct tables, bar charts, pie charts, pictograms, line graphs | 3 (`S2.1`, `S2.2`, `S2.3`) | 1 (`S4.1`) | **4** |
| 4 | Straight-line graphs and real-life graphs: plot, read, interpret | 3 (`A9.1`, `A14.1`, `A14.4`) | 0 | **3** |
| 5 | Probability experiments and diagrams: frequency tables and trees; constructing Venn and tree diagrams | 1 (`P1.1`) | 2 (`P6.1`, `P6.2`) | **3** |
| 6 | Mass and time conversions | 0 | 3 (`N13.1`, `R1.1`, `G14.1`) | **3** |
| 7 | Algebra basics: vocabulary (expression, equation, formula, identity, term, factor) and function machines (Jon's candidate) | 2 (`A3.1`, `A7.1`) | 0 | **2** |
| 8 | Simplifying expressions: collect like terms, expand one bracket, take out a common factor (surds excluded) | 1 (`A4.1`) | 1 (`A4.3`) | **2** |
| 9 | Scale drawings, maps, measuring lines and angles | 1 (`R2.1`) | 1 (`G15.1`) | **2** |
| 10 | Scatter graphs: plot, describe correlation, draw a line of best fit | 1 (`S6.1`) | 1 (`S6.2`) | **2** |
| 11 | Algebraic notation (`ab`, `3y`, `a²`, `a/b`) | 1 (`A1.1`) | 0 | **1** |
| 12 | Circle circumference and area | 1 (`G17.1`) | 0 | **1** |
| 13 | Coordinate problems | 1 (`G11.1`) | 0 | **1** |
| 14 | Probabilities summing to one | 1 (`P4.1`) | 0 | **1** |
| 15 | Form and solve: word problem to linear equation to answer | 0 | 1 (`A21.1`) | **1** |
| 16 | Order of operations | 0 | 1 (`N3.1`) | **1** |
| 17 | Multiples, common factors, HCF, LCM | 0 | 1 (`N4.1`) | **1** |
| 18 | Squares, cubes and roots as the skill | 0 | 1 (`N6.1`) | **1** |
| 19 | Rounding to 1 significant figure to estimate | 0 | 1 (`N14.1`) | **1** |

Notes on each target:

1. **Fractions and decimals: arithmetic, ordering, conversion, of an amount, one quantity as a fraction of another (the planned fractions game).** `N8.1` is GAP†; `N10.1` GAP. **`R3.1` and `R6.1` (both GAP, ruled CORE) fold into this game (Jon, 30 Sep).** `N2.1` only add/subtract of negatives to ±10 is practised, no fraction, decimal or mixed-number arithmetic; `N1.1` no game orders fractions or uses the symbols; `N12.1` percentage of an amount is covered, fraction of an amount is not.
2. **Shape vocabulary and properties: terms, quadrilaterals, solids, circle parts (the shape-vocabulary game).** All four GAP, no item in any game. **`G9.1` (centre, radius, chord; ruled CORE) folds into this game (Jon, 30 Sep).** `circle-theorem-spotter` and `constructions-lab` are not attributed here (§7).
3. **Charts: read and construct tables, bar charts, pie charts, pictograms, line graphs.** All three GAP. `S4.1` is covered by `chart-interrogator` on stem-and-leaf comparison only.
4. **Straight-line graphs and real-life graphs: plot, read, interpret.** `A9.1` is GAP† (diagnostic items only). `A14.1` THIN: `graph-sketcher` 15/8, `gradient-hunter` 15/7. `A14.4` THIN: `gradient-hunter` 15/7, `core-maths-paper2c` 4/4. About half of each game's items are not Foundation-pitched (§1.4), so 15 items exist but fewer than 10 are pitched right. Gradient and y = mx + c is STRETCH (`A10.1`) and is not in this target.
5. **Probability experiments and diagrams: frequency tables and trees; constructing Venn and tree diagrams.** `P1.1` GAP. `P6.1`/`P6.2` are COVERED by `given-that`, which reads probabilities off a finished table, Venn or tree; no game asks the student to construct one.
6. **Mass and time conversions.** No game converts mass or time; time is named CORE. Same gap under three parts.
7. **Algebra basics: vocabulary (expression, equation, formula, identity, term, factor) and function machines (Jon's candidate).** **Named as an "algebra basics" candidate by Jon (30 Sep).** `A3.1` GAP; `A7.1` GAP† (2 `spot-the-error` items, neither Foundation-pitched). `A4.1` (rank 8) and `A1.1` (rank 11) sit next to it; whether they join is not ruled.
8. **Simplifying expressions: collect like terms, expand one bracket, take out a common factor (surds excluded).** `A4.1` GAP, CORE excluding its surd clause (Jon). `A4.3` is COVERED by `like-terms-collector` on collecting only; no game expands a single bracket or takes out a common factor.
9. **Scale drawings, maps, measuring lines and angles.** `R2.1` GAP† (3 diagnostic items). `G15.1` is COVERED only by `bearing-blitz`, and bearings remain OUT as a topic (Jon): the CORE content of the part (measuring, maps, scale drawings) has no item.
10. **Scatter graphs: plot, describe correlation, draw a line of best fit.** `S6.1` THIN (`core-maths-paper2a` 3/3 plus diagnostics; `regression-rumble` 12 items, none Foundation-pitched). `S6.2` is COVERED by `correlation-or-coincidence` as interpretation only: no scatter graph is drawn or fitted. Sits next to the charts target (rank 3).
11. **Algebraic notation (`ab`, `3y`, `a²`, `a/b`).** GAP, no item in any game. Adjacent to the algebra-basics candidate (rank 7).
12. **Circle circumference and area.** THIN by rule 4 (one `estimation-golf` item plus diagnostics); **treated as GAP for build purposes (Jon)**.
13. **Coordinate problems.** THIN: `coordinate-geometry-dash` 8/6, and that game is dark, A-level-facing.
14. **Probabilities summing to one.** THIN: `probability-pioneer` 7, nothing above 10.
15. **Form and solve: word problem to linear equation to answer.** `A21.1` (CORE, linear only) is COVERED by `equation-builder`, which builds the equation and never asks the student to solve or interpret it.
16. **Order of operations.** BIDMAS appears in 4 diagnostic items only; the `kiln-disaster` room carries one lock.
17. **Multiples, common factors, HCF, LCM.** No practice item in any game; the rooms carry it: `comic-caper` (HCF), `kiln-disaster` (multiples, LCM) and `heatwave-mutiny` (LCM).
18. **Squares, cubes and roots as the skill.** Occur only as operands inside `estimation-engine`.
19. **Rounding to 1 significant figure to estimate.** `estimation-engine` is tolerance-band mental arithmetic, not the 1 s.f. method.

All 24 formal parts appear exactly once, and 17 further parts are sub-skill holes; the two sets do not overlap (checked by script).

**Where Jon has named a game:** the fractions game (rank 1) takes `R3.1` and `R6.1`; the shape-vocabulary game (rank 2) takes `G9.1`; `A3.1` and `A7.1` form the algebra-basics candidate (rank 7). Every other grouping is the author's, by shared skill, and is a proposal only.

### 10.5 CORE COVERED — the candidate resit suite

**41 CORE parts are COVERED** by the audit's rule (one game with 10+ Foundation-pitched items). The games below are the candidate suite. The part list under each game is the CORE parts for which that game carries the 10+ items; a game that only adds diagnostic items to a part is not listed. Register columns are §5's measurements, facts not verdicts: the row §7.5.1 gives the game, the row it renders, and whether its start screen or bank carries school-age wording. **Per Jon's ruling (§10.7) every game entering the resit strand gets an adult register whatever it shows today.**

| Game | Roster levels | CORE COVERED parts | Rendered row, and the row §7.5.1 expects (≠ = mismatch) | Start-screen year wording |
|---|---|---|---|---|
| `split-it` | KS3, GCSE | 7: `N11.1`, `R4.1`, `R5.1`, `R7.1`, `R8.1`, `R10.1`, `R11.1` | light (0.95), expected light | — |
| `sequence-solver` | KS3, GCSE, A-Level, L4 | 5: `A23.1`, `A24.1`, `A24.2`, `A25.1`, `A25.3` | dark (0.04), expected light ≠ | KS3×2 |
| `formula-plug-in` | Year 6 | 3: `A2.1`, `R11.1`, `G16.1` | dark (0.07), expected light ≠ | — |
| `unit-converter` | GCSE, A-Level, L4 | 3: `N13.1`, `R1.1`, `G14.1` | dark (0.04), expected dark | — |
| `decimal-detective` | Year 6 | 2: `N1.1`, `N15.1` | dark (0.07), expected light ≠ | — |
| `estimation-engine` | KS3, GCSE, Core | 2: `N6.1`, `N14.1` | dark (0.09), expected light ≠ | — |
| `given-that` | GCSE, A-Level, Core, L4 | 2: `P6.1`, `P6.2` | dark (0.07), expected dark | — |
| `negative-number-line` | Year 6 | 2: `N1.1`, `N2.1` | dark (0.07), expected light ≠ | — |
| `percentage-flip` | Year 6, KS3, GCSE | 2: `N12.1`, `R9.1` | light (0.96), expected light | — |
| `probability-pioneer` | Year 6 | 2: `P3.1`, `P7.1` | dark (0.07), expected light ≠ | — |
| `proportion-blaster` | GCSE, A-Level | 2: `R5.1`, `R10.1` | dark (0.07), expected dark | — |
| `angle-ace` | Year 6, KS3, GCSE | 1: `G3.1` | dark (0.04), expected light ≠ | Year 6×2, Year 7×1, KS3×1 |
| `bearing-blitz` | GCSE | 1: `G15.1` | dark (0.02), expected dark | — |
| `better-value` | GCSE, Core | 1: `R11.1` | dark (0.07), expected dark | — |
| `chart-interrogator` | GCSE, A-Level, Core, L4 | 1: `S4.1` | dark (0.05), expected dark | — |
| `correlation-or-coincidence` | GCSE, A-Level, Core | 1: `S6.2` | dark (0.04), expected dark | — |
| `distinctly-average` | KS3, GCSE | 1: `S4.3` | light (0.95), expected light | KS3×2 |
| `equation-builder` | KS3, GCSE, L4 | 1: `A21.1` | dark (0.07), expected light ≠ | KS3×1, Year 7×1 |
| `estimation-golf` | Year 6, KS3, GCSE, A-Level, L4, Core | 1: `N14.1` | dark (0.3), expected light ≠ | YEAR 6×1, KS3×1 |
| `expected-damage` | KS3, GCSE, Core | 1: `P2.1` | dark (0.07), expected light ≠ | KS3×1, Year 7×1 |
| `factor-race` | Year 6, KS3, GCSE | 1: `N4.1` | light (0.96), expected light | — |
| `formula-forge` | GCSE, A-Level, L4 | 1: `A5.1` | dark (0.04), expected dark | — |
| `formula-unlocked` | GCSE, A-Level, L4 | 1: `A5.1` | dark (0.04), expected dark | — |
| `four-quadrant-explorer` | Year 6 | 1: `A8.1` | dark (0.07), expected light ≠ | Year 7×1 |
| `like-terms-collector` | Year 6 | 1: `A4.3` | light (0.98), expected light | Year 7×1 |
| `linear-equation-solver` | GCSE | 1: `A17.1` | dark (0.04), expected dark | — |
| `new-shapes` | Year 6 | 1: `G16.1` | dark (0.07), expected light ≠ | Year 7×1 |
| `prime-factorisation` | Year 6, KS3, GCSE | 1: `N4.1` | light (0.99), expected light | — |
| `prime-or-composite` | KS3, GCSE | 1: `N4.1` | dark (0.09), expected light ≠ | — |
| `stat-attack` | GCSE, Core, L4 | 1: `S4.3` | dark (0.04), expected dark | — |
| `think-of-a-number` | Year 6 | 1: `N3.1` | dark (0.07), expected light ≠ | — |

**31 games** cover the 41 parts. Every CORE COVERED part is covered by at least one game above (checked by script when this section was written).

Things the list does not say, so nobody reads it as a warranty:

- **Covered is a floor** (headline). 17 parts in this table carry a missing CORE sub-skill (the right-hand column of §10.4): `N1.1`, `N2.1`, `N3.1`, `N4.1`, `N6.1`, `N12.1`, `N13.1`, `N14.1`, `A4.3`, `A21.1`, `R1.1`, `G14.1`, `G15.1`, `P6.1`, `P6.2`, `S4.1`, `S6.2`.
- **Pitch differs by game.** 13 games in the table list Year 6 first (`formula-plug-in`, `decimal-detective`, `negative-number-line`, `percentage-flip`, `probability-pioneer`, `angle-ace`, `estimation-golf`, `factor-race`, `four-quadrant-explorer`, `like-terms-collector`, `new-shapes`, `prime-factorisation`, `think-of-a-number`). §1.4 counts easy Foundation-level questions in them as Foundation-pitched, but a resit student needs Foundation depth, not primary depth. Their register is the largest job under the ruling in §10.7.
- **`bearing-blitz` is listed only because it is the sole 10+ cover for `G15.1`, and every one of its items is a bearing, which stays OUT as a topic (Jon, 30 Sep).** On that evidence it is not a resit-suite game; the part's CORE content is rank 9 in §10.4.
- **`unit-converter` is the only cover for three parts, and 11 of its 58 items (19%) are not Foundation-pitched** (§8), and `prime-or-composite` runs to 9,973.

### 10.6 Every Foundation part, tagged

Type: s standard, u underlined. Verdict is the audit's; **GAP†** is THIN that rests only on the diagnostic games (rule 4). Ruling column: the question (§10.1a, §10.3) under which Jon placed the part; blank means the band lists placed it.

| Part | Type | Band | Audit verdict | Effective | Ruling | Note |
|---|---|---|---|---|---|---|
| `N1.1` | s | **CORE** | COVERED | COVERED |  |  |
| `N2.1` | s | **CORE** | COVERED | COVERED |  |  |
| `N3.1` | s | **CORE** | COVERED | COVERED |  |  |
| `N4.1` | s | **CORE** | COVERED | COVERED |  | Prime factorisation, product notation and the unique factorisation theorem are inside the same part. |
| `N5.1` | s | OUT | GAP | GAP |  | Systematic listing not named, so OUT. |
| `N6.1` | s | **CORE** | COVERED | COVERED |  |  |
| `N7.1` | u | OUT | THIN | THIN |  | Beyond N6: roots and fractional indices. OUT. |
| `N7.3` | u | OUT | THIN | THIN |  | Fragment of N7.1. |
| `N8.1` | s | **CORE** | THIN | GAP† |  | Fractions CORE. Fragment continues "surds and multiples of π" in N8.3. |
| `N8.3` | u | STRETCH | GAP | GAP | Q4 | Answers in terms of π. |
| `N9.1` | s | STRETCH | COVERED | COVERED |  |  |
| `N10.1` | s | **CORE** | GAP | GAP |  |  |
| `N11.1` | s | **CORE** | COVERED | COVERED |  |  |
| `N12.1` | s | **CORE** | COVERED | COVERED |  |  |
| `N13.1` | s | **CORE** | COVERED | COVERED |  | Standard units incl. time CORE; "standard compound measures" STRETCH. |
| `N14.1` | s | **CORE** | COVERED | COVERED |  |  |
| `N15.1` | s | **CORE** | COVERED | COVERED |  | Includes "use inequality notation". |
| `N15.2` | u | STRETCH | THIN | THIN | Q10 | Error intervals. |
| `N16.1` | u | OUT | THIN | GAP† |  | Limits of accuracy. |
| `A1.1` | s | **CORE** | GAP | GAP |  |  |
| `A2.1` | s | **CORE** | COVERED | COVERED |  |  |
| `A3.1` | s | **CORE** | GAP | GAP | Q7 |  |
| `A4.1` | s | **CORE** | GAP | GAP | Q7 | **CORE excluding its surd clause** (Jon). Surd items are not evidence for this part. |
| `A4.3` | s | **CORE** | COVERED | COVERED |  | Common factors (not named CORE) and single bracket (CORE); principal skill collecting/expanding. |
| `A4.4` | u | OUT | THIN | GAP† |  | Two brackets. Only one bracket is CORE. |
| `A4.6` | u | OUT | THIN | GAP† |  | Fragment of A4.4. |
| `A4.7` | u | OUT | COVERED | COVERED |  | Quadratics. |
| `A4.9` | s | STRETCH | COVERED | COVERED | Q7 | Index laws. |
| `A5.1` | s | **CORE** | COVERED | COVERED | Q7 |  |
| `A6.1` | u | OUT | GAP | GAP |  |  |
| `A7.1` | s | **CORE** | THIN | GAP† | Q7 |  |
| `A8.1` | s | **CORE** | COVERED | COVERED |  |  |
| `A9.1` | s | **CORE** | THIN | GAP† | Q1 | Ruling Q1: CORE (plotting straight-line graphs). |
| `A9.2` | u | OUT | THIN | THIN |  | Parallel and perpendicular lines via y = mx + c: beyond the straight-line skill. |
| `A9.4` | u | OUT | THIN | THIN |  | Equation of a line through two points: same. |
| `A10.1` | s | STRETCH | THIN | THIN | Q1 | Gradient and intercept. |
| `A11.1` | u | OUT | GAP | GAP |  |  |
| `A12.1` | s | STRETCH | THIN | THIN | Q1R | Linear and quadratic graphs in one part. |
| `A12.2` | u | OUT | THIN | THIN | Q1R | Stays OUT (Jon). |
| `A12.3` | s | OUT | THIN | THIN | Q1R | Stays OUT (Jon). |
| `A12.4` | u | OUT | THIN | THIN | Q1R | Stays OUT (Jon). |
| `A14.1` | s | **CORE** | THIN | THIN | Q1 | Ruling Q1: CORE (plot and interpret; reciprocal/exponential sit in `A14.2`/`A14.3`). |
| `A14.2` | u | OUT | THIN | THIN | Q1R | Stays OUT (Jon). |
| `A14.4` | s | **CORE** | THIN | THIN | Q1 | Ruling Q1: CORE (real-life graphs, distance–time). Acceleration goes beyond Jon's examples. |
| `A17.1` | s | **CORE** | COVERED | COVERED |  | Unknown on both sides is STRETCH; graph solutions OUT. Tagged by the one-unknown linear equation. |
| `A18.1` | u | OUT | THIN | GAP† |  |  |
| `A18.3` | u | OUT | THIN | GAP† |  |  |
| `A18.5` | u | OUT | GAP | GAP |  |  |
| `A19.1` | u | OUT | COVERED | COVERED |  |  |
| `A19.3` | u | OUT | THIN | THIN |  |  |
| `A21.1` | u | **CORE** | COVERED | COVERED | Q7 | **CORE, linear only** (Jon). "Two simultaneous equations" stays OUT. |
| `A22.1` | u | STRETCH | THIN | GAP† |  |  |
| `A22.3` | u | STRETCH | THIN | GAP† |  |  |
| `A22.5` | u | STRETCH | THIN | GAP† |  |  |
| `A23.1` | s | **CORE** | COVERED | COVERED |  |  |
| `A24.1` | s | **CORE** | COVERED | COVERED |  |  |
| `A24.2` | u | **CORE** | COVERED | COVERED |  | Arithmetic progressions CORE; quadratic sequences OUT; geometric progressions OUT. |
| `A25.1` | s | **CORE** | COVERED | COVERED |  |  |
| `A25.3` | s | **CORE** | COVERED | COVERED |  |  |
| `R1.1` | s | **CORE** | COVERED | COVERED |  | Standard units CORE; compound units STRETCH. |
| `R2.1` | s | **CORE** | THIN | GAP† | Q6 |  |
| `R3.1` | s | **CORE** | GAP | GAP | Q5 |  |
| `R4.1` | s | **CORE** | COVERED | COVERED |  |  |
| `R5.1` | s | **CORE** | COVERED | COVERED |  |  |
| `R6.1` | s | **CORE** | GAP | GAP | Q5 |  |
| `R7.1` | s | **CORE** | COVERED | COVERED |  |  |
| `R8.1` | s | **CORE** | COVERED | COVERED |  | Ratio to fractions CORE; "linear functions" OUT. |
| `R9.1` | s | **CORE** | COVERED | COVERED |  | Percentage of an amount CORE; percentage change and simple interest STRETCH; original-value problems and >100% not named. |
| `R10.1` | s | **CORE** | COVERED | COVERED |  | Direct proportion CORE; inverse and graphical OUT. |
| `R11.1` | s | **CORE** | COVERED | COVERED |  | Speed and unit pricing CORE. |
| `R11.2` | u | STRETCH | GAP | GAP |  |  |
| `R12.1` | s | OUT | COVERED | COVERED |  |  |
| `R12.2` | u | OUT | COVERED | COVERED |  |  |
| `R13.1` | u | OUT | COVERED | COVERED |  |  |
| `R13.2` | s | OUT | COVERED | COVERED |  |  |
| `R13.4` | u | OUT | COVERED | COVERED |  |  |
| `R14.1` | u | OUT | THIN | THIN |  | Gradient as rate of change; direct/inverse graphs. |
| `R16.1` | u | OUT | THIN | THIN |  | Compound interest is not "simple interest". |
| `G1.1` | s | **CORE** | GAP | GAP | Q3 | Ruling Q3: CORE. |
| `G2.1` | u | OUT | COVERED | COVERED |  | Constructions not named. |
| `G3.1` | s | **CORE** | COVERED | COVERED |  | Includes the angle sum in any polygon. |
| `G4.1` | s | **CORE** | GAP | GAP | Q3 | Ruling Q3: CORE. |
| `G5.1` | u | OUT | GAP | GAP |  |  |
| `G6.1` | u | OUT | GAP | GAP |  |  |
| `G7.1` | s | OUT | COVERED | COVERED |  | Transformations and enlargement; enlargement named OUT. |
| `G7.2` | u | OUT | GAP | GAP |  |  |
| `G7.4` | u | OUT | GAP | GAP |  |  |
| `G9.1` | s | **CORE** | GAP | GAP | Q4 |  |
| `G9.2` | u | OUT | GAP | GAP | Q4 | Tangent, arc, sector, segment. |
| `G11.1` | s | **CORE** | THIN | THIN |  | Coordinate problems; tagged under coordinates. |
| `G12.1` | s | **CORE** | GAP | GAP | Q3 | Ruling Q3: CORE. |
| `G13.1` | u | OUT | GAP | GAP |  | Plans and elevations. |
| `G13.2` | s | OUT | GAP | GAP |  | Plans and elevations. |
| `G14.1` | s | **CORE** | COVERED | COVERED |  |  |
| `G15.1` | s | **CORE** | COVERED | COVERED | Q6 | **Bearings remain OUT as a topic** (Jon): the part is CORE for measuring lines and angles, maps and scale drawings. |
| `G16.1` | s | **CORE** | COVERED | COVERED | Q8 | Whole part CORE, incl. prism volume (Jon). |
| `G17.1` | s | **CORE** | THIN | THIN |  |  |
| `G17.2` | u | OUT | GAP | GAP |  | Solids. |
| `G18.1` | u | OUT | GAP | GAP |  |  |
| `G19.1` | u | OUT | COVERED | COVERED |  |  |
| `G19.3` | u | OUT | COVERED | COVERED |  |  |
| `G20.1` | u | OUT | COVERED | COVERED |  |  |
| `G20.2` | s | OUT | COVERED | COVERED |  |  |
| `G20.3` | u | OUT | COVERED | COVERED |  |  |
| `G20.4` | s | OUT | COVERED | COVERED |  |  |
| `G20.5` | u | OUT | COVERED | COVERED |  |  |
| `G20.7` | u | OUT | COVERED | COVERED |  |  |
| `G20.9` | u | OUT | COVERED | COVERED |  |  |
| `G21.1` | u | OUT | COVERED | COVERED |  |  |
| `G24.1` | s | OUT | THIN | THIN |  |  |
| `G25.1` | u | OUT | THIN | THIN |  |  |
| `P1.1` | s | **CORE** | GAP | GAP | Q9 |  |
| `P2.1` | s | **CORE** | COVERED | COVERED |  | Expected outcomes read as basic probability. |
| `P3.1` | s | **CORE** | COVERED | COVERED |  |  |
| `P4.1` | s | **CORE** | THIN | THIN |  |  |
| `P5.1` | u | STRETCH | GAP | GAP | Q9 | Sample size and relative frequency. |
| `P6.1` | s | **CORE** | COVERED | COVERED | Q9 | Venn and tree diagrams CORE here by ruling. |
| `P6.2` | u | **CORE** | COVERED | COVERED | Q9 | Fragment of P6.1. |
| `P7.1` | s | **CORE** | COVERED | COVERED |  |  |
| `P8.1` | u | OUT | THIN | THIN |  | Combined events and tree diagrams; not named. |
| `S1.1` | u | OUT | THIN | THIN |  | Sampling. |
| `S2.1` | s | **CORE** | GAP | GAP |  |  |
| `S2.2` | u | **CORE** | GAP | GAP |  |  |
| `S2.3` | s | **CORE** | GAP | GAP |  |  |
| `S4.1` | s | **CORE** | COVERED | COVERED |  |  |
| `S4.3` | s | **CORE** | COVERED | COVERED |  |  |
| `S5.1` | s | OUT | GAP | GAP | Q11 | Too general to place; OUT (Jon). |
| `S6.1` | s | **CORE** | THIN | THIN | Q2 |  |
| `S6.2` | u | **CORE** | COVERED | COVERED | Q2 |  |

### 10.7 Rulings recorded

Recorded in `docs/todo.md` under §3.1 (resit strand). In brief: **(1)** every resit-strand game gets an adult register, and canon §7.5.1 is to be amended (not amended here); **(2)** `standard-form-blitz` stays as it is; **(3)** "Don't Count the Zeroes" is built as the resit-strand standard form game (todo 3.4). Part-level rulings: §10.1a and §10.3. Standard form is STRETCH (`N9.1`, COVERED by `standard-form-blitz`); the new game is the resit-strand version, not a replacement.
