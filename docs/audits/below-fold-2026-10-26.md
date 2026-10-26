# Below the fold: why 45 games fail the phone gate, and laptop and projector sizes (26 Oct 2026)

Jon's contract of 26 Oct 2026 (report only; no game, `theme.css`, `.maffs-ref`, canon, list or gate rule touched). The gate is canon §7.6.1
as merged in #554: the **last** answer option ends above the fold (normal mode at 320 × 568, 375 × 667 and 390 × 844; Aa at 375 and 390),
with Aa at 320 × 568 the recorded exception (the options **start** above the fold). `scripts/phone-fit-state.json` lists 45 games that fail it
(39 in normal mode, 44 in Aa) and 14 the driver cannot measure.

## Summary

- **Every one of the 45 has an identified cause** (none unexplained; the STOP IF threshold was a quarter, 11). They fall into six groups:

| Group | Cause | Games | Does `.maffs-ref` fix it? |
|---|---|---|---|
| A | A reference or help panel sits open above the question | 8 | **Yes**, with a compact header and options two to a row: 7 of 8 fit by estimate |
| B | The driver measured the **start screen**: intro text above the level picker | 9 | **Yes for the start screen** (collapse "How it works"); 3 of the 4 that reach a question also fail there |
| C | The question itself is taller than the screen (scenario, story, persona card) | 11 | **No**: the panel is the question. Compact chrome and two-up options close 1; the rest is a ruling |
| D | A figure or diagram above the options | 9 | **No**: scale the figure on a phone, compact chrome, two-up: 4 of 9 fit by estimate |
| E | The answer input itself is tall (keypad, keyboard, picker, drag list) | 6 | **No**: the input needs redesigning for a phone (sticky input, compact keypad) |
| F | Four full-width options, nothing else | 2 | **No**: options two to a row fit both |

- **A shared component under several groups: the header bar and score bar.** Ten of the 45 use todo §3.20's "Split It header bar"
  (`class="back"`) with a score bar under it: together 139 to 154 px at 320 × 568, against Distinctly Average's 53 + 45 after its migration.
  Theme migration (canon §7.5.1) compacts both; it is one of the three levers in every estimate below.
- **The priority audience is hit first.** 11 of the 45 are in the resit suite (`docs/resit-coverage-audit.md` §10.5), six of them listing Year 6:
  `think-of-a-number`, `percentage-flip`, `decimal-detective`, `estimation-golf`, `prime-factorisation`, `negative-number-line`.
- **The unmeasurable list hides four real failures.** The Core Maths papers are "unmeasurable" only because the driver looks before their
  two-second section banner ends; waited out, all four fail the gate (paper 2A by 470 px at 320 × 568). Of the other ten, only two have a
  verifier that measures the fold (How Many Parts?, Just Pythag It, Bruv), and How Many Parts?'s covers Next, not the asking screen's options.
- **Laptops and projectors (1280 × 720, 1280 × 800, 1366 × 768), all 86 measurable games:** 21 games end their last option below the fold
  at one size or more, and 21 put Next below it after a wrong answer. Canon has no rule for these sizes; several fail only there
  (the Year 6 games `new-shapes` and `formula-plug-in` among them), because their phone layout compacts and their desktop layout does not.

## Method

Every number here was measured on branch `claude/theme-distinctly-average-2` (game files identical to `main` after #554), Chromium, the pinned
real fonts, seeded as the gate is, on the **first question at the default level** (one sample, as the gate). "What sits above" lists every
visible block above the top answer control, outermost first, with its height at 320 × 568 (in Aa for a game that fails only in Aa). The
estimates apply three layout levers to that screen, each measured, none assumed: **(1)** a panel above the question collapsed to a 54 px
`.maffs-ref` pill; **(2)** header, score bar, HUD and progress bar together brought to 100 px (Distinctly Average's are 98); **(3)** four to six
short options laid two to a row (half the options block; not applied to options that are paragraphs of text). They are first-order: a
fix must be measured on every item, as #554 did. Where the driver reached a start screen, a second pass picked the first level and pressed
Start. Laptop sizes were measured by `measure-phone-fit.py`'s own `measure_one()` at those sizes from a report-only wrapper: no gate rule
or list was changed or needed changing (STOP IF 2 did not fire).

## Every game, priority order

Resit suite first, then by the lowest tier the game serves (Year 6, KS3, GCSE, Core, A-Level, Further, L4), then by the number of
size-and-mode cells it fails. **Worst over** is px past the fold at its worst failing cell (Aa 320: how far the options start below it).

| # | Game | Lowest tier | Resit suite | Group | Fails at (gate) | Worst over | What sits above the first answer control at 320 × 568 (px, outermost first) |
|---|---|---|---|---|---|---|---|
| 1 | `think-of-a-number` | Year 6 | yes | E | normal 320×568; normal 375×667; aa 320×568; aa 375×667; aa 390×844 | 243 | header 111 ("← Back to Games Think of a Number …"); focus 64; puzzle-card 255 ("PP Professor Puzzler "I think of a…"); numpad-btn ×9 (55 each) |
| 2 | `percentage-flip` | Year 6 | yes | D | normal 320×568; normal 375×667; aa 320×568; aa 375×667 | 192 | header 68; scorebar 69; tap-hint 36; card-scene 280 ("TAP TO REVEAL What is 75% of 80? 6…") |
| 3 | `decimal-detective` | Year 6 | yes | E | normal 320×568; aa 320×568; aa 375×667 | 148 | header 112 ("← Back to Games Decimal Detective …"); div#gameArea 267 ("Smallest → Largest 3.044 3.44 3.04…"); question-prompt 132 ("The Line-Up Drag the suspects into…") |
| 4 | `estimation-golf` | Year 6 | yes | B | normal 320×568; normal 375×667; aa 375×667 | 111 | header 206 ("Estimation Golf 9 HOLES · PAR YOUR…"); div 34 |
| 5 | `prime-factorisation` | Year 6 | yes | D | normal 320×568; aa 375×667 | 77 | header 68; scorebar 76; factor-tree 115 ("YOUR FACTORISATION: Tap a prime be…"); target-box 136 ("Build this number: 100 Your produc…") |
| 6 | `negative-number-line` | Year 6 | yes | E | aa 320×568 | 41 | (Aa) header 144 ("← Back to Games Negative Number Li…"); step-row 48; number-line-wrap 128 ("-10 -9 -8 -7 -6 -5 -4 -3 -2 -1 0 1…"); place-readout 30; place-instruction 62; place-prompt 59 |
| 7 | `better-value` | GCSE | yes | C | normal 320×568; normal 375×667; normal 390×844; aa 320×568; aa 375×667; aa 390×844 | 880 | header 57; options-row 303 ("ANYTIME RETURNS Price £48 per retu…"); scenario-card 368 ("A student is choosing between two …") |
| 8 | `given-that` | GCSE | yes | B | normal 320×568; aa 320×568; aa 375×667; aa 390×844 | 462 | start-label 21; how-section 277 ("How it works Phase 1: A dataset is…"); start-sub 102 ("Conditional probability trainer. S…"); start-title 51 |
| 9 | `chart-interrogator` | GCSE | yes | B | normal 320×568; aa 375×667 | 146 | header 107 ("Chart Interrogator ← Back to Games…"); sel-label 19; p 72; h2 42 |
| 10 | `stat-attack` | GCSE | yes | B | aa 320×568 | 71 | (Aa) back-link 24; menu-info 268 ("Grouped frequency tables — modal c…"); header 243 ("Stat Attack Can you calculate the …") |
| 11 | `correlation-or-coincidence` | GCSE | yes | D | aa 375×667 | 51 | (Aa) back-link 44; hud 58; invented 44; fig 195 ("↑ Wellington boots sold in a week …"); prompt 60 |
| 12 | `52dle` | KS3 |  | E | normal 320×568; normal 375×667; normal 390×844; aa 320×568; aa 375×667; aa 390×844 | 655 | nav 52; guess-history 308; clue-box 119 ("TODAY'S CLUE PRIME I am the 9th pr…"); status-bar 53; game-header 230 ("DAILY · MATHEMATICAL DEDUCTION 52-…") |
| 13 | `seven-bridges` | KS3 |  | B | normal 320×568; normal 375×667; normal 390×844; aa 320×568; aa 375×667; aa 390×844 | 649 | how-to 294 ("How to Play Click any vertex (circ…"); start-sub 77; start-title 51 |
| 14 | `fermi-lab` | KS3 |  | C | normal 320×568; normal 375×667; normal 390×844; aa 375×667; aa 390×844 | 586 | header 65; question-card 122 ("How many kilograms of food does a …"); scorebar 66; step-header 22 |
| 15 | `word-problem-decoder` | KS3 |  | C | normal 320×568; normal 375×667; aa 320×568; aa 375×667; aa 390×844 | 511 | visible 50; header 112 ("← Back to Games Word Problem Decod…"); fade-in 434 ("The speed of light is approximatel…") |
| 16 | `maths-court` | KS3 |  | C | normal 320×568; normal 375×667; normal 390×844; aa 375×667; aa 390×844 | 423 | header 108 ("← Back to Games Maths Court Aa KS3…"); problem-card 140 ("THE DISPUTE If a = 3 and b = −2, f…") |
| 17 | `wrong-on-the-internet` | KS3 |  | C | normal 320×568; normal 375×667; aa 320×568; aa 375×667; aa 390×844 | 363 | header 112 ("← Back to Games Wrong on the Inter…"); stage-indicator 42; div#numblrPost 436 ("N Numblr @ProbMaster A and B are i…") |
| 18 | `constructions-lab` | KS3 |  | A | normal 320×568; normal 375×667; aa 320×568; aa 375×667; aa 390×844 | 331 | back-link 16; canvas-area 247; instructions 301 ("Perpendicular Bisector 1. Set comp…") |
| 19 | `equatle` | KS3 |  | E | normal 320×568; normal 375×667; normal 390×844; aa 375×667; aa 390×844 | 330 | nav 52; grid 215; msg 20; sbar 48; div 71 |
| 20 | `spot-the-muppet` | KS3 |  | C | normal 320×568; normal 375×667; aa 320×568; aa 375×667; aa 390×844 | 269 | header 73; character-card 249 ("SB Sharon Bulk Bulk Buying Strateg…") |
| 21 | `terrible-advice` | KS3 |  | C | normal 320×568; normal 375×667; aa 320×568; aa 375×667; aa 390×844 | 264 | header 87; character-card 333 ("HW Hypatia Wrongley Pythagorean Th…"); progress-wrap 27 |
| 22 | `higher-power` | KS3 |  | D | normal 320×568; aa 320×568; aa 375×667 | 97 | back-link 18; hol-area 413 ("KNOWN Days in a year Days in a yea…"); hud 68 |
| 23 | `index-laws` | GCSE |  | A | normal 320×568; normal 375×667; normal 390×844; aa 320×568; aa 375×667; aa 390×844 | 471 | header 66; scorebar 73; law-ref 363 ("QUICK REFERENCE 𝑎 𝑚 × 𝑎 𝑛 = 𝑎 𝑚 + …"); q-sub 15; q-text 48; q-rule-label 22 |
| 24 | `screening-room` | GCSE |  | C | normal 320×568; normal 375×667; aa 320×568; aa 375×667; aa 390×844 | 368 | header 65; scorebar 66; question-card 253 ("SHOP SECURITY GATE Over a month, a…") |
| 25 | `quadratic-factoriser` | GCSE |  | E | normal 320×568; normal 375×667; aa 320×568; aa 375×667; aa 390×844 | 308 | header 67; scorebar 74; question-box 299 ("FACTORISE 𝑥 2 − 4 x 2 −4 x + ? × x…"); picker-editing 20 |
| 26 | `trig-worms` | GCSE |  | A | normal 320×568; normal 375×667; aa 320×568; aa 375×667 | 168 | header 69; scorebar 66; trig-ref 74; canvas-wrap 127; level-bar 16; q-hint 15; q-text 72; q-type 14 |
| 27 | `circle-theorem-spotter` | GCSE |  | D | normal 320×568; normal 375×667; aa 320×568; aa 375×667 | 121 | back-link 18; q-card 336 ("A B P O Two tangents PA and PB are…"); hud 68 |
| 28 | `expectation-station` | GCSE |  | C | normal 320×568; aa 320×568; aa 375×667 | 135 | header 109 ("← Back to Games Expectation Statio…"); context-card 135 ("A supermarket records the number o…"); prob-table-wrap 128 ("Items in basket (x) 1 2 3 4 P(X = …") |
| 29 | `probability-paradox` | GCSE |  | C | aa 320×568; aa 375×667 | 208 | (Aa) back-link 25; q-card 529 ("The Two-Child Problem. A family ha…"); hud 105 ("QUESTION 1 SCORE 0 CORRECT 0 TIME …") |
| 30 | `modular-battle` | GCSE |  | D | normal 320×568; aa 320×568 | 60 | header 69; scorebar 76; dot-grid 140; dot-label 30; q-sub 16; q-text 23 |
| 31 | `coordinate-geometry-dash` | GCSE |  | D | normal 320×568; aa 375×667 | 7 | back-link 16; q-card 106 ("Which line is shown? The line pass…"); graph-wrap 193; hud 53 |
| 32 | `gradient-hunter` | GCSE |  | B | aa 320×568 | 39 | (Aa) back-link 24; div 21; menu-info 223 ("Click two points on a real-world g…"); header 232 ("Gradient Hunter Click points, find…") |
| 33 | `tax-theft` | Core |  | A | normal 320×568; normal 375×667; normal 390×844; aa 320×568; aa 375×667; aa 390×844 | 543 | header 116 ("Tax Theft Core Maths ← Back to Gam…"); threshold-tables 410 ("INCOME TAX 2025/26 BAND ANNUAL INC…"); salary-display 142 ("GROSS ANNUAL SALARY £18,500 Diffic…"); step-instruction 24; step-header 27 |
| 34 | `growth-and-decay` | Core |  | B | normal 320×568; aa 320×568; aa 375×667 | 174 | back-link 16; menu-info 179 ("Exponential modelling — substitute…"); header 171 ("Growth and Decay What does the mod…") |
| 35 | `glorious-gantt` | Core |  | B | aa 320×568; aa 375×667 | 176 | (Aa) back-link 24; menu-info 134 ("Critical path analysis — calculate…"); header 232 ("Glorious Gantt Game What's on the …"); correction-notice 240 ("We're correcting this game. Some a…") |
| 36 | `differentiation-duel` | A-Level |  | A | normal 320×568; normal 375×667; normal 390×844; aa 320×568; aa 375×667; aa 390×844 | 551 | header 66; scorebar 73; rules-ref 467 ("QUICK REFERENCE 𝑑 𝑑 𝑥 ( 𝑥 𝑛 ) = 𝑛 …"); q-text 48; q-label 15; div 33 |
| 37 | `log-laws` | A-Level |  | A | normal 320×568; normal 375×667; normal 390×844; aa 320×568; aa 375×667; aa 390×844 | 453 | header 66; scorebar 73; law-ref 347 ("QUICK REFERENCE · LOG MEANS LOG₁₀ …"); timer-text 15; q-text 48; q-rule-label 22 |
| 38 | `integration-duel` | A-Level |  | A | normal 320×568; normal 375×667; normal 390×844; aa 320×568; aa 375×667; aa 390×844 | 445 | header 66; scorebar 73; rules-ref 363 ("QUICK REFERENCE ∫ 𝑥 𝑛 𝑑 𝑥 = 𝑥 𝑛 + …"); q-text 48; div 33 |
| 39 | `suvat` | A-Level |  | A | normal 320×568; normal 375×667; aa 320×568; aa 375×667; aa 390×844 | 538 | header 69; scorebar 73; vars-box 288 ("— PHASE 1: PICK THE EQUATION — An …"); suvat-ref 202 ("— THE 5 SUVAT EQUATIONS — 𝑣 = 𝑢 + …"); phase-label 28 |
| 40 | `test-the-claim` | A-Level |  | B | normal 320×568; aa 320×568; aa 375×667 | 185 | back-link 16; setup-label 15; menu-info 112 ("Guided six-step hypothesis testing…"); header 135 ("Test the Claim State your hypothes…") |
| 41 | `partial-fractions-duel` | A-Level |  | F | normal 320×568; normal 375×667; aa 375×667 | 113 | back-link 18; q-card 126 ("𝑥 2 ( 𝑥 + 1 ) ( 𝑥 − 1 ) ( 𝑥 + 2 ) …"); timer-text 15; hud 68 |
| 42 | `curling-friction` | A-Level |  | D | normal 320×568; aa 320×568; aa 375×667 | 49 | back-link 18; q-card 138 ("Stone A (20 kg, 4 m/s) hits Stone …"); rink 100 ("SWEEP!…"); hud 68 |
| 43 | `complex-converter` | Further/L3 |  | D | normal 320×568; normal 375×667; normal 390×844; aa 320×568; aa 375×667; aa 390×844 | 329 | timer-bar-wrap 28; game-header 48; argand-col 272 ("Real Imaginary -12 -12 -10 -10 -8 …"); target-label 42; given-display 72; conversion-label 20 |
| 44 | `truth-will-set-you-free` | L4 |  | C | normal 320×568; normal 375×667; normal 390×844; aa 320×568; aa 375×667; aa 390×844 | 786 | header 89; div#truthTableSection 281 ("A B C Output 0 0 0 0 0 1 0 1 0 0 1…"); div#scenarioSection 518 ("TIER 1 — FOUNDATION A warning buzz…"); progress-bar 20 |
| 45 | `boolean-blitz` | L4 |  | F | normal 320×568 | 96 | header 100 ("Boolean Blitz Aa ← Games…"); question-card 168 ("SIMPLIFY FULLY. 𝐴 ⋅ 𝐵 + 𝐴 ⋅ 𝐵 ‾ A⋅…"); progress-bar 20 |

## The groups

### A. A reference or help panel sits open above the question (8): `constructions-lab`, `index-laws`, `trig-worms`, `tax-theft`, `differentiation-duel`, `log-laws`, `integration-duel`, `suvat`

**Example:** `differentiation-duel` at 320 × 568: header 66, score bar 73, then a QUICK REFERENCE panel **467 px** tall, then the question;
the options start at 809, below a 528 fold, and end at 1,079. The panel is the same at every size, which is why the game fails by the same
amount at all three. `index-laws`, `integration-duel` and `log-laws` share the pattern (347 to 363 px panels); `suvat` (the five equations,
202, under a 288 px variables box), `tax-theft` (the tax tables, 410), `constructions-lab` (the step list, 301) and `trig-worms` (SOH CAH TOA, 74)
are the same shape. **Fix:** the panel becomes a `.maffs-ref` card (collapsed while asking, open in the feedback); with a compact header
(lever 2) and two-up options (lever 3) seven of the eight fit at 320 × 568 by estimate (`differentiation-duel` by 36 px, `index-laws` by 12,
`log-laws` by 29, `integration-duel` by 38, `tax-theft` by 10, `suvat`, `constructions-lab`); `trig-worms` stays 20 px over (its canvas, 127 px,
needs scaling too). The four quick-reference games are the strongest single case for the component: one pattern, four games.

### B. The driver measured the start screen (9): `estimation-golf`, `given-that`, `chart-interrogator`, `stat-attack`, `seven-bridges`, `gradient-hunter`, `growth-and-decay`, `glorious-gantt`, `test-the-claim`

The "answer controls" the gate measured are the start screen's level, mode or diagram buttons, under the game's intro: `given-that`'s
"How it works" (277 px), `seven-bridges`' "How to Play" (294), `stat-attack`'s and `gradient-hunter`'s menu text (268, 223, Aa),
`growth-and-decay`'s (179), `glorious-gantt`'s menu text and correction notice (134 + 240, Aa), and the hero headers of `estimation-golf`
(206) and `chart-interrogator` (107 + 114 of intro). **This is a real phone fault, but of the start screen**: a student scrolls to find the
level buttons. **Fix:** the intro becomes a `.maffs-ref` card ("How it works", collapsed), which fits five of the nine start screens by
estimate (`given-that`, `stat-attack`, `gradient-hunter`, `growth-and-decay`, `test-the-claim`); `estimation-golf`, `chart-interrogator`,
`seven-bridges` and `glorious-gantt` need their hero header or title block compacted too. **And the question screen still needs measuring:**
a second pass that picked a level and pressed Start reached a question in four: `seven-bridges` fits (its graph ends at 339 of 528);
`given-that` fails (the data container 233 px under a 120 px header: last option 743 of 528), `growth-and-decay` fails (a 359 px scenario
panel: input 573 to 611), `stat-attack` fails in Aa (options start 654 of 528). `chart-interrogator`, `estimation-golf`, `test-the-claim`
and `glorious-gantt` stayed on their start screen after Start was pressed, and in `gradient-hunter` (Aa) the second pass found no controls:
each needs a game-specific step to reach play.

### C. The question is taller than the screen (11): `better-value`, `fermi-lab`, `word-problem-decoder`, `maths-court`, `wrong-on-the-internet`, `spot-the-muppet`, `terrible-advice`, `screening-room`, `expectation-station`, `probability-paradox`, `truth-will-set-you-free`

The tall block is the question itself: `better-value`'s two deals and scenario (368 + 303 px, then four conclusion cards 353 px tall),
`word-problem-decoder`'s word problem (434), `wrong-on-the-internet`'s post (436), `truth-will-set-you-free`'s scenario and truth table
(518 + 281), `probability-paradox`'s Two-Child Problem (529, Aa), `fermi-lab`'s chain of five steps, `maths-court`'s dispute and three argument
cards (631 px of options), `screening-room`'s scenario (253), `expectation-station`'s context and table. In `spot-the-muppet` and
`terrible-advice` most of the 249 and 333 px is the character's name, title and biography, before the advice. **`.maffs-ref` does not apply:**
collapsing the question hides what must be read to answer. **Fix, in order:** compact chrome and two-up options where the options are short
(closes `expectation-station`; `screening-room` to 44 px over); collapse a persona's biography (not its advice) in the two character games;
for the rest canon §7.6.1's 1 Oct paragraph already allows the asking screen to scroll "when the question itself is taller than the screen
at a legible size", and the gate does not know it: **Jon to rule** whether these games take that exception (logged per game) or are redesigned.

### D. A figure above the options (9): `percentage-flip`, `prime-factorisation`, `correlation-or-coincidence`, `higher-power`, `circle-theorem-spotter`, `modular-battle`, `coordinate-geometry-dash`, `curling-friction`, `complex-converter`

`circle-theorem-spotter`'s diagram card (336), `complex-converter`'s Argand diagram (272), `coordinate-geometry-dash`'s graph (193),
`curling-friction`'s rink (100), `higher-power`'s two cards (413), `percentage-flip`'s card (280), `modular-battle`'s dot grid (140),
`prime-factorisation`'s factor tree and target (115 + 136), `correlation-or-coincidence`'s scatter (195, Aa). **`.maffs-ref` does not apply:**
the figure is the question. **Fix:** scale the figure to the phone's height (canon §7.6.1: "shrink a picture without changing what it says"),
plus compact chrome and two-up options: by estimate `modular-battle` (2 px over today), `coordinate-geometry-dash` (7), `curling-friction` (49)
and `prime-factorisation` fit without touching the figure; the other five need it scaled.

### E. The answer input itself is tall (6): `think-of-a-number`, `decimal-detective`, `negative-number-line`, `52dle`, `equatle`, `quadratic-factoriser`

`think-of-a-number`: a 255 px puzzle card and a 64 px display above a four-row number pad, Enter at 707 to 762 (the driver counts only Enter,
so the digits are not judged; the pad starts higher). `quadratic-factoriser`: a 24-button number picker under a 299 px question box.
`decimal-detective`: the drag-to-order list (267) and its Check button (609 to 657). `52dle` and `equatle`: Wordle-shaped, with a guess history
or grid (308, 215) and a keyboard (369) under an intro (230 in `52dle`). `negative-number-line` (Aa): a 144 px header, the number line (128)
and its arrows, Confirm at 569. **`.maffs-ref` does not apply**, except to `52dle`'s intro. **Fix:** per input: the shared phone keypad
(`MaffsKeypad`, canon) in place of a game's own pad; the input or keyboard pinned to the bottom of the screen for the two daily puzzles;
fewer number choices on screen at once in `quadratic-factoriser`.

### F. Four full-width options, nothing else (2): `partial-fractions-duel`, `boolean-blitz`

`boolean-blitz` (four options 288 px under a 168 px question and a 100 px header) and `partial-fractions-duel` (292 under 126). **Fix:**
options two to a row on a phone (as Distinctly Average's `.options-grid`): both fit by estimate (68 and 44 px to spare).

## The 14 games the driver cannot measure

| Game | What the driver sees | What a game-specific measurement needs |
|---|---|---|
| `core-maths-paper1`, `-2a`, `-2b`, `-2c` | A two-second "Section A" banner (`showSectionBanner`); the driver looks after about one | Wait for `.option-btn`. **Measured that way here, all four fail the gate**: 320 × 568 normal, last option 539, 998, 684, 668 against 528; paper 2A also at 375 and 390 (975, 932) and in Aa at every size (its stem alone is 459 px) |
| `how-many-parts` | The stage's worked example: one "Show the next step" button | Step through the example, then measure the asking screen. Its verifier (parts 3 to 5) measures Next and the worked example at all three sizes in both modes, **not** the asking screen's options |
| `squared-squirrel`, `take-a-walk` | The stage's worked example: one "Show the next step" button | Step through the example, then measure. Their verifiers check sideways scroll at 320 and 1280 px, **not the fold** |
| `just-pythag-it-bruv` | Round 1's tap-the-hypotenuse step: the triangle's sides are the only controls | Tap the hypotenuse, then measure. **Already done** by its verifier (fit at 320, 375, 390 and 412 px) |
| `six-sevens-bruv` | Its start is not recognised ("New grid"); play never begins | Press its start, then measure. Measured by hand on 30 Sep 2026 (canon §7.6.1, 144 orientations); its verifier does not measure the fold |
| `bearing-blitz` | A canvas and a Fire button; no option group | Set a bearing, fire, measure the canvas and Fire against the fold |
| `four-quadrant-explorer` | A canvas grid: the answer is a click on it | Measure the canvas and its confirm control |
| `shape-shifter` | A canvas grid with Undo: the answer is built by clicking | Measure the grid and its Check control |
| `equation-builder`, `spot-the-error` | Started by the driver, the question cards render empty (run normally they show level and session pickers and Start); the cause is not found in this audit | Pick a level and a session length, press Start, wait for the card's text, then measure |

## Laptop and projector sizes (normal mode, all 86 measurable live games)

Each cell is px past the fold (the viewport less the 40 px footer): **bold and positive** is below it. "Next" is after the first wrong answer the
driver produced; "–" means it produced none. 21 games end their last option below the fold at one size or more, 11 at all three; 21 put Next
below it after a wrong answer. Canon §7.6.1 governs the narrow screen only, so none of this fails anything today.

- **Games on the phone list are mostly the same games here** (18 of the 21 last-option failures), so the phone fixes above would carry.
- **Not on the phone list, failing on a laptop:** `new-shapes` (last option 331 px over at 1280 × 720, Next 597), `formula-plug-in` (155, 421)
  and `normal-navigator` (10, 256); Next only: `angle-ace`, `expected-damage`, `matrix-crunch`. Their phone layout compacts and their desktop
  layout does not.
- **`distinctly-average`**: on a laptop its median card is open, as ruled ("open where it fits"), and Next ends 353 px below a 680 px fold at
  1280 × 720; without the card it is already 251 px below (both recorded in canon §7.6.2).

| Game | Last option 1280×720 | 1280×800 | 1366×768 | Next 1280×720 | 1280×800 | 1366×768 |
|---|---|---|---|---|---|---|
| `new-shapes` | **+331** | **+251** | **+283** | **+597** | **+517** | **+549** |
| `formula-plug-in` | **+155** | **+75** | **+107** | **+421** | **+341** | **+373** |
| `distinctly-average` | -146 | -226 | -194 | **+353** | **+273** | **+305** |
| `coordinate-geometry-dash` | **+129** | **+49** | **+81** | **+331** | **+251** | **+283** |
| `equatle` | **+264** | **+184** | **+216** | – | – | – |
| `normal-navigator` | **+10** | -70 | -38 | **+256** | **+176** | **+208** |
| `better-value` | **+21** | -59 | -27 | **+255** | **+175** | **+207** |
| `wrong-on-the-internet` | **+108** | **+28** | **+60** | **+253** | **+173** | **+205** |
| `constructions-lab` | **+241** | **+161** | **+193** | – | – | – |
| `trig-worms` | **+110** | **+30** | **+62** | **+215** | **+135** | **+167** |
| `angle-ace` | -47 | -127 | -95 | **+211** | **+131** | **+163** |
| `tax-theft` | **+206** | **+126** | **+158** | no Next | no Next | no Next |
| `differentiation-duel` | **+63** | -17 | **+15** | **+180** | **+100** | **+132** |
| `52dle` | **+178** | **+98** | **+130** | no Next | no Next | no Next |
| `fermi-lab` | **+177** | **+97** | **+129** | **+164** | **+84** | **+116** |
| `truth-will-set-you-free` | **+176** | **+96** | **+128** | – | – | – |
| `log-laws` | **+22** | -58 | -26 | **+139** | **+59** | **+91** |
| `circle-theorem-spotter` | **+28** | -52 | -20 | **+127** | **+47** | **+79** |
| `expected-damage` | -197 | -277 | -245 | **+120** | **+40** | **+72** |
| `integration-duel` | **+3** | -77 | -45 | **+120** | **+40** | **+72** |
| `percentage-flip` | **+22** | -58 | -26 | **+117** | **+37** | **+69** |
| `index-laws` | -23 | -103 | -71 | **+94** | **+14** | **+46** |
| `curling-friction` | -111 | -191 | -159 | **+85** | **+5** | **+37** |
| `estimation-golf` | -154 | -234 | -202 | **+75** | -5 | **+27** |
| `suvat` | **+46** | -34 | -2 | – | – | – |
| `think-of-a-number` | **+44** | -36 | -4 | – | – | – |
| `quadratic-factoriser` | **+42** | -38 | -6 | – | – | – |
| `boolean-blitz` | -236 | -316 | -284 | **+40** | -40 | -8 |
| `matrix-crunch` | -196 | -276 | -244 | **+31** | -49 | -17 |
| `seven-bridges` | -14 | -94 | -62 | – | – | – |
| `eigenvector-engine` | -254 | -334 | -302 | -22 | -102 | -70 |
| `graph-transformer` | -29 | -109 | -77 | – | – | – |
| `formula-forge` | -234 | -314 | -282 | -30 | -110 | -78 |
| `free-daily-pizza` | -288 | -368 | -336 | -46 | -126 | -94 |
| `proof-builder` | -325 | -405 | -373 | -71 | -151 | -119 |
| `formula-unlocked` | -247 | -327 | -295 | -74 | -154 | -122 |
| `prime-or-composite` | -181 | -261 | -229 | -76 | -156 | -124 |
| `fraction-equivalence` | -208 | -288 | -256 | -93 | -173 | -141 |
| `moments-master` | -227 | -307 | -275 | -94 | -174 | -142 |
| `prime-factorisation` | -125 | -205 | -173 | – | – | – |
| `screening-room` | -127 | -207 | -175 | no Next | no Next | no Next |
| `force-resolver` | -199 | -279 | -247 | -131 | -211 | -179 |
| `terrible-advice` | -137 | -217 | -185 | -175 | -255 | -223 |
| `decimal-detective` | -199 | -279 | -247 | -138 | -218 | -186 |
| `modular-battle` | -229 | -309 | -277 | -142 | -222 | -190 |
| `surd-simplifier` | -245 | -325 | -293 | -145 | -225 | -193 |
| `standard-form-blitz` | -216 | -296 | -264 | -145 | -225 | -193 |
| `correlation-or-coincidence` | -146 | -226 | -194 | -270 | -350 | -318 |
| `spot-the-muppet` | -152 | -232 | -200 | no Next | no Next | no Next |
| `proportion-blaster` | -223 | -303 | -271 | -152 | -232 | -200 |
| `factor-race` | -255 | -335 | -303 | -158 | -238 | -206 |
| `characteristic-quest` | -304 | -384 | -352 | -163 | -243 | -211 |
| `sequence-solver` | -235 | -315 | -283 | -164 | -244 | -212 |
| `maths-court` | -173 | -253 | -221 | no Next | no Next | no Next |
| `eigenvalue-extractor` | -326 | -406 | -374 | -186 | -266 | -234 |
| `higher-power` | -188 | -268 | -236 | no Next | no Next | no Next |
| `partial-fractions-duel` | -190 | -270 | -238 | no Next | no Next | no Next |
| `negative-number-line` | -191 | -271 | -239 | – | – | – |
| `word-problem-decoder` | -197 | -277 | -245 | no Next | no Next | no Next |
| `dimension-checker` | -397 | -477 | -445 | -199 | -279 | -247 |
| `prisoners-dilemma` | -200 | -280 | -248 | – | – | – |
| `test-the-claim` | -201 | -281 | -249 | – | – | – |
| `trig-identity-duel` | -208 | -288 | -256 | no Next | no Next | no Next |
| `complex-converter` | -284 | -364 | -332 | -213 | -293 | -261 |
| `binomial-blaster` | -216 | -296 | -264 | no Next | no Next | no Next |
| `expectation-station` | -222 | -302 | -270 | no Next | no Next | no Next |
| `unit-converter` | -362 | -442 | -410 | -223 | -303 | -271 |
| `given-that` | -239 | -319 | -287 | – | – | – |
| `chart-interrogator` | -242 | -322 | -290 | – | – | – |
| `scale-factor-scaling` | -382 | -462 | -430 | -243 | -323 | -291 |
| `growth-and-decay` | -251 | -331 | -299 | – | – | – |
| `linear-equation-solver` | -268 | -348 | -316 | – | – | – |
| `probability-paradox` | -292 | -372 | -340 | no Next | no Next | no Next |
| `like-terms-collector` | -296 | -376 | -344 | – | – | – |
| `glorious-gantt` | -325 | -405 | -373 | – | – | – |
| `estimation-engine` | -326 | -406 | -374 | – | – | – |
| `stat-attack` | -331 | -411 | -379 | – | – | – |
| `truth-buster` | -333 | -413 | -381 | no Next | no Next | no Next |
| `simultaneous-solver` | -338 | -418 | -386 | – | – | – |
| `gradient-hunter` | -340 | -420 | -388 | – | – | – |
| `split-it` | -358 | -438 | -406 | – | – | – |
| `component-crusher` | -387 | -467 | -435 | – | – | – |
| `graph-sketcher` | -387 | -467 | -435 | – | – | – |
| `probability-pioneer` | -388 | -468 | -436 | – | – | – |
| `trig-wars` | -491 | -571 | -539 | – | – | – |
| `factor-theorem` | -529 | -609 | -577 | – | – | – |

## Checks

- **STOP IF "a game measures differently on main from the known-failures list": did not fire.** `measure-phone-fit.py` on `main` at 27f56a0
  (#554 merged), both modes: exit 0; normal 39 known failures, Aa 44, 14 unmeasurable listed in each, nothing stale, nothing unlisted.
- STOP IF "more than a quarter of the 45 with no identifiable cause": did not fire (0). STOP IF "laptop sizes need a gate change": did not
  fire (a report-only wrapper around `measure_one()`; no script, list or rule changed).
- Nothing in `games/`, `schools/assets/`, canon or `scripts/` is changed by this report.
