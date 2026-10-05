# Search titles and descriptions: draft for review (Phase 1)

Draft, 5 Oct 2026 (cloud). **Nothing on any page has changed.** This table is generated from
`data/games.json` and the roster's Levels column by the rules below; on Jon's word (with his edits)
Phase 2 writes it into every game page and /resit/ (`scripts/apply-meta.py`) and holds it there in CI
(`scripts/check-meta.py`).

**97 roster games** (every numbered row, so it includes the unlisted `just-pythag-it-bruv`; the
withdrawn `regression-rumble` is not a numbered row). 54 keep their levels in the title,
41 drop them, 2 are PHRASE NEEDED.

## The rules (as built; each is a call for review)

1. **Title:** `<search_phrase> Game – <levels> Maths | MaffsGames`, at most 60 characters (Python
   `len`, so the en dash counts as 1). Levels from the roster in teacher words, joined with `/`, in
   the order Year 6, KS3, GCSE, A-Level, Level 3, Level 4, Further Maths, Core Maths; "A-Level Year
   2" folds into A-Level. **My call:** when the last level is Further Maths or Core Maths, " Maths"
   is not added again ("A-Level/Further Maths", not "… Further Maths Maths").
2. **Over 60:** the levels part goes, never the phrase. **My call:** the fallback is
   `<search_phrase> Maths Game | MaffsGames`, keeping "maths" in the title (the brief's root cause
   notes /resit/'s title lacks it); a phrase that already says "maths" or "mathematical" gets no
   second "Maths". The literal reading, `<search_phrase> Game | MaffsGames`, is a
   one-line change.
3. **Description:** `<what the student practises> For <levels>. Free, no sign-up.`, at most 155.
   **My call:** only the first part is stored in `games.json`; the levels sentence is generated from
   the roster, so the levels are held once, as the brief's CLASS CHECK asks.
4. **Phrases** are drawn from each game's spec-map row(s) and roster topic, in the words a teacher
   would type. Where a phrase is not from its spec row, the Note column says so.
5. **For Phase 2 (a question, not a change):** three pages (`higher-power`, `prisoners-dilemma`,
   `screening-room`) also carry `twitter:title` and `twitter:description`. The brief names og: tags
   only; I recommend apply-meta.py writes the twitter: pair too where present, or they go stale.

Rendered character counts are not pixel widths: Google truncates by width (about 580px), so a
60-character title of wide letters can still be cut. No title here relies on its last characters.


## /resit/

| Page | Current title | New title | Chars | New description | Chars |
|---|---|---|---|---|---|
| `/resit/` | GCSE Resit \| MaffsGames | GCSE Maths Resit Games – Free, No Sign-up \| MaffsGames | 54 | Maths games for GCSE Foundation resit classes aiming for grade 4: number, algebra, ratio, geometry, probability and statistics. Free, no sign-up. | 145 |

## Every roster game (97), in roster order

| Slug | Current title | New title | Chars | New description | Chars | Note |
|---|---|---|---|---|---|---|
| `sequence-solver` | Sequence Solver — MaffsGames | Sequences and nth Term Maths Game \| MaffsGames | 46 | Find the nth term of arithmetic and geometric sequences, then sigma notation and recurrence. For KS3, GCSE, A-Level and Level 4. Free, no sign-up. | 146 |  |
| `estimation-golf` | Estimation Golf — MaffsGames | Estimation and Rounding Maths Game \| MaffsGames | 47 | Estimate answers by rounding: the closer you get, the further the ball goes. For Year 6, KS3, GCSE, A-Level, Level 4 and Core Maths. Free, no sign-up. | 150 |  |
| `estimation-engine` | Estimation Engine — MaffsGames | Estimating by Rounding Maths Game \| MaffsGames | 46 | Estimate calculations by rounding each number first, against the clock. For KS3, GCSE and Core Maths. Free, no sign-up. | 119 | In games.json, NOT applied until its rebuild merges (item 6). |
| `factor-race` | Factor Race — MaffsGames | Finding Factors Game – Year 6/KS3/GCSE Maths \| MaffsGames | 57 | Two numbers, one tap: pick the one with more factors. Fast factor recall. For Year 6, KS3 and GCSE. Free, no sign-up. | 117 |  |
| `prime-factorisation` | Prime Sprint — MaffsGames | Prime Factorisation Maths Game \| MaffsGames | 43 | Build a number's prime factorisation by multiplying up from 1, one prime at a time. For Year 6, KS3 and GCSE. Free, no sign-up. | 127 |  |
| `prime-or-composite` | Prime or Composite — MaffsGames | Prime Numbers Game – KS3/GCSE Maths \| MaffsGames | 48 | Sort numbers as prime or composite against the clock. For KS3 and GCSE. Free, no sign-up. | 89 |  |
| `percentage-flip` | Percentage Flip — MaffsGames | Percentages of Amounts Maths Game \| MaffsGames | 46 | Find percentages of amounts, from 50% of 80 to harder percentages, in a quick card-flip game. For Year 6, KS3 and GCSE. Free, no sign-up. | 137 |  |
| `fraction-equivalence` | Fraction Snap — MaffsGames | Equivalent Fractions Maths Game \| MaffsGames | 44 | Decide whether two fractions are equivalent, at speed, by cross-multiplying or simplifying. For Year 6, KS3 and GCSE. Free, no sign-up. | 135 |  |
| `equatle` | Equatle — MaffsGames | Equation Wordle Game – KS3/GCSE Maths \| MaffsGames | 50 | Deduce a hidden equation from colour-coded clues, Wordle style. Number sense and reasoning. For KS3 and GCSE. Free, no sign-up. | 127 | Spec ref is N1 'number reasoning'; the phrase names the format teachers search for. |
| `52dle` | 52-dle — MaffsGames | Daily Number Puzzle Game – KS3/GCSE Maths \| MaffsGames | 54 | A daily number deduction puzzle: use the maths clues to find the hidden number. For KS3 and GCSE. Free, no sign-up. | 115 | Spec ref is N1 'number reasoning'; no topic phrase fits a daily puzzle better. |
| `constructions-lab` | Constructions Lab — MaffsGames | Constructions and Loci Game – KS3/GCSE Maths \| MaffsGames | 57 | Bisect angles and lines, draw perpendiculars and loci, with a virtual compass and ruler. For KS3 and GCSE. Free, no sign-up. | 124 |  |
| `split-it` | Split It — MaffsGames | Ratio Game – KS3/GCSE Maths \| MaffsGames | 40 | Simplify ratios, find equivalents, share amounts in a ratio, scale recipes and use the unitary method. For KS3 and GCSE. Free, no sign-up. | 138 |  |
| `word-problem-decoder` | Word Problem Decoder — MaffsGames | Word Problems Game – KS3/GCSE Maths \| MaffsGames | 48 | Read a word problem and identify the maths it needs: the step before any calculation. For KS3 and GCSE. Free, no sign-up. | 121 |  |
| `equation-builder` | Equation Builder — MaffsGames | Forming Equations Game – KS3/GCSE/Level 4 Maths \| MaffsGames | 60 | Turn a word problem into an equation or formula by building it from tiles. For KS3, GCSE and Level 4. Free, no sign-up. | 119 |  |
| `spot-the-error` | Spot the Error — MaffsGames | Errors in Word Problems Maths Game \| MaffsGames | 47 | Find the error in a worked word problem, then the misreading that caused it. For KS3, GCSE and Level 4. Free, no sign-up. | 121 |  |
| `gradient-hunter` | Gradient Hunter — MaffsGames | Gradient and Rate of Change Maths Game \| MaffsGames | 51 | Find the gradient of real-world graphs and say what the rate of change means. For GCSE, A-Level and Core Maths. Free, no sign-up. | 129 |  |
| `truth-buster` | Truth Buster — MaffsGames | PHRASE NEEDED | — | Is it always true? Decide whether mathematical statements always hold, then see why. For KS3, GCSE and A-Level. Free, no sign-up. | 129 | STOP IF: no spec-map reference (a ruled exception, check-spec-mapping.py). Suggestion: **Always, Sometimes or Never True**, the name teachers use for this task type. |
| `spot-the-muppet` | Spot the Muppet — MaffsGames | Maths Misconceptions Game – KS3/GCSE/Core Maths \| MaffsGames | 60 | Spot who has the maths wrong and pick the right answer: misconceptions in number, algebra and statistics. For KS3, GCSE and Core Maths. Free, no sign-up. | 153 | AO2 game; the four AO2 games need distinct phrases. |
| `terrible-advice` | Terrible Advice — MaffsGames | Financial Maths Mistakes Game \| MaffsGames | 42 | Spot the maths mistakes in bad money advice: percentages, ratios and interest. For KS3, GCSE and Core Maths. Free, no sign-up. | 126 | AO2 game. |
| `wrong-on-the-internet` | Wrong on the Internet — MaffsGames | Spot the Mistake Game – KS3/GCSE/Core Maths \| MaffsGames | 56 | Find the maths mistake in social media posts, polls and comment threads. For KS3, GCSE and Core Maths. Free, no sign-up. | 120 | AO2 game. |
| `maths-court` | Maths Court — MaffsGames | Mathematical Reasoning Game \| MaffsGames | 40 | Three arguments, one correct: rule on maths disputes by finding the argument that holds up. For KS3, GCSE and Core Maths. Free, no sign-up. | 139 | AO2 game. |
| `expected-damage` | Expected Damage — MaffsGames | Expected Value Game – KS3/GCSE/Core Maths \| MaffsGames | 54 | Use probability and expected value to choose the best option, not a guess. For KS3, GCSE and Core Maths. Free, no sign-up. | 122 |  |
| `negative-number-line` | Negative Number Line — MaffsGames | Negative Numbers Game – Year 6 Maths \| MaffsGames | 49 | Place, order and calculate with negative numbers on a number line from −10 to 10. For Year 6. Free, no sign-up. | 111 |  |
| `think-of-a-number` | Think of a Number — MaffsGames | Inverse Operations Game – Year 6 Maths \| MaffsGames | 51 | Solve 'I think of a number' puzzles by undoing each step with inverse operations. For Year 6. Free, no sign-up. | 111 |  |
| `formula-plug-in` | Formula Plug-In — MaffsGames | Substitution into Formulae Game – Year 6 Maths \| MaffsGames | 59 | Substitute values into formulae and work out the answer, from simple rules to area and speed. For Year 6. Free, no sign-up. | 123 |  |
| `decimal-detective` | Decimal Detective — MaffsGames | Ordering and Rounding Decimals Maths Game \| MaffsGames | 54 | Order decimals, round them and place them on a number line. For Year 6. Free, no sign-up. | 89 |  |
| `four-quadrant-explorer` | Four Quadrant Explorer — MaffsGames | Four Quadrant Coordinates Game – Year 6 Maths \| MaffsGames | 58 | Plot points and read coordinates in all four quadrants, and complete shapes on the grid. For Year 6. Free, no sign-up. | 118 |  |
| `like-terms-collector` | Like Terms Collector — MaffsGames | Collecting Like Terms Game – Year 6 Maths \| MaffsGames | 54 | Simplify expressions by collecting like terms, from fruit to letters to full algebra. For Year 6. Free, no sign-up. | 115 |  |
| `probability-pioneer` | Probability Pioneer — MaffsGames | Simple Probability Game – Year 6 Maths \| MaffsGames | 51 | Place events on the probability scale, calculate simple probabilities and test true-or-false claims. For Year 6. Free, no sign-up. | 130 |  |
| `shape-shifter` | Shape Shifter — MaffsGames | Transformations Game – Year 6 Maths \| MaffsGames | 48 | Translate, reflect and rotate shapes on a coordinate grid. For Year 6. Free, no sign-up. | 88 |  |
| `new-shapes` | New Shapes — MaffsGames | Area and Volume Game – Year 6 Maths \| MaffsGames | 48 | Area of parallelograms and trapezia, and volume of prisms. For Year 6. Free, no sign-up. | 88 |  |
| `higher-power` | Higher Power — Mathematical Constants Game — MaffsGames | Comparing Powers and Roots Maths Game \| MaffsGames | 50 | Compare powers, roots and famous constants: which is higher? Then match expressions to their values. For KS3, GCSE and A-Level. Free, no sign-up. | 145 |  |
| `prisoners-dilemma` | Prisoner's Dilemma — Game Theory — MaffsGames | Prisoner's Dilemma Maths Game \| MaffsGames | 42 | Play the iterated prisoner's dilemma against computer opponents and weigh up the payoffs. For KS3, GCSE, A-Level and Core Maths. Free, no sign-up. | 146 | Spec ref is Core §3.10 cost-benefit analysis; the phrase is the game's own name because it is what is searched. |
| `seven-bridges` | Seven Bridges — Graph Theory Puzzles — MaffsGames | Graph Theory: Euler Paths Maths Game \| MaffsGames | 49 | Euler's bridges puzzle: trace routes, spot impossible graphs and find the rule for Euler paths. For KS3, GCSE and A-Level. Free, no sign-up. | 140 |  |
| `distinctly-average` | Distinctly Average — MaffsGames | Mean, Median, Mode and Range Maths Game \| MaffsGames | 52 | Find the mean, median, mode and range of data sets, then frequency tables and missing values. For KS3 and GCSE. Free, no sign-up. | 129 |  |
| `index-laws` | Index Laws — MaffsGames | Laws of Indices Game – GCSE/A-Level Maths \| MaffsGames | 54 | Apply the laws of indices: multiplying, dividing, powers of powers, zero, negative and fractional indices. For GCSE and A-Level. Free, no sign-up. | 146 |  |
| `quadratic-factoriser` | Quadratic Factoriser — MaffsGames | Factorising Quadratics Maths Game \| MaffsGames | 46 | Factorise quadratics with a = 1, then a > 1 by the AC method, then solve with the quadratic formula. For GCSE and A-Level. Free, no sign-up. | 140 |  |
| `trig-wars` | Trig Wars — MaffsGames | Trigonometry and Projectiles Maths Game \| MaffsGames | 52 | Set the angle and power of a shot and watch the trigonometry resolve it into horizontal and vertical parts. For GCSE and A-Level. Free, no sign-up. | 147 |  |
| `trig-worms` | Trig Worms — MaffsGames | SOH CAH TOA Game – GCSE/A-Level Maths \| MaffsGames | 50 | Use SOH CAH TOA to find the side or angle that aims the cannon. For GCSE and A-Level. Free, no sign-up. | 103 |  |
| `modular-battle` | Modular Battle — MaffsGames | Modular Arithmetic Game – GCSE/A-Level Maths \| MaffsGames | 57 | Find remainders against the clock, with dot pictures while you need them. For GCSE and A-Level. Free, no sign-up. | 113 |  |
| `surd-simplifier` | Surd Simplifier — MaffsGames | Simplifying Surds Game – GCSE/A-Level Maths \| MaffsGames | 56 | Simplify surds and rationalise denominators. For GCSE and A-Level. Free, no sign-up. | 84 |  |
| `proportion-blaster` | Proportion Blaster — MaffsGames | Direct and Inverse Proportion Maths Game \| MaffsGames | 53 | Direct and inverse proportion problems, and sharing in a ratio. For GCSE and A-Level. Free, no sign-up. | 103 |  |
| `trig-identity-duel` | Trig Identity Duel — MaffsGames | Sine and Cosine Rules Maths Game \| MaffsGames | 45 | Exact trig values, the sine rule and the cosine rule. For GCSE, A-Level and Level 4. Free, no sign-up. | 102 |  |
| `standard-form-blitz` | Standard Form Blitz — MaffsGames | Standard Form Game – GCSE/A-Level Maths \| MaffsGames | 52 | Convert to and from standard form, then multiply and divide numbers in standard form. For GCSE and A-Level. Free, no sign-up. | 125 |  |
| `simultaneous-solver` | Simultaneous Solver — MaffsGames | Simultaneous Equations Maths Game \| MaffsGames | 46 | Solve linear simultaneous equations, then linear with non-linear pairs. For GCSE and A-Level. Free, no sign-up. | 111 |  |
| `circle-theorem-spotter` | Circle Theorem Spotter — MaffsGames | Circle Theorems Game – GCSE Maths \| MaffsGames | 46 | Spot and apply all seven circle theorems, with a diagram on every question. For GCSE. Free, no sign-up. | 103 |  |
| `probability-paradox` | Probability Paradox — MaffsGames | Probability Misconceptions Maths Game \| MaffsGames | 50 | Probability paradoxes, conditional probability and common fallacies, in three modes. For GCSE and Core Maths. Free, no sign-up. | 127 |  |
| `angle-ace` | Angle Ace — MaffsGames | Angle Facts Game – Year 6/KS3/GCSE Maths \| MaffsGames | 53 | Find missing angles, then name the angle fact that gives each one. For Year 6, KS3 and GCSE. Free, no sign-up. | 110 |  |
| `coordinate-geometry-dash` | Coordinate Geometry Dash — MaffsGames | Coordinate Geometry Game – GCSE/A-Level Maths \| MaffsGames | 58 | Midpoints, gradients, lengths and equations of lines and circles on a plotted grid. For GCSE and A-Level. Free, no sign-up. | 123 |  |
| `graph-transformer` | Graph Transformer — MaffsGames | Graph Transformations Game – GCSE/A-Level Maths \| MaffsGames | 60 | Translate, reflect and stretch a curve to match the target graph in as few moves as possible. For GCSE and A-Level. Free, no sign-up. | 133 |  |
| `formula-unlocked` | Formula Unlocked — MaffsGames | Changing the Subject Maths Game \| MaffsGames | 44 | Change the subject of a formula, step by step, with hints when you need them. For GCSE, A-Level and Level 4. Free, no sign-up. | 126 |  |
| `bearing-blitz` | Bearing Blitz — MaffsGames | Three-Figure Bearings Game – GCSE Maths \| MaffsGames | 52 | Estimate and set three-figure bearings, then fire at the target. For GCSE. Free, no sign-up. | 92 |  |
| `scale-factor-scaling` | Scale Factor Scaling — MaffsGames | Area and Volume Scale Factors Maths Game \| MaffsGames | 53 | Length, area and volume scale factors: k, k squared and k cubed. For GCSE, A-Level and Level 4. Free, no sign-up. | 113 |  |
| `unit-converter` | Unit Converter — MaffsGames | Area and Volume Unit Conversions Maths Game \| MaffsGames | 56 | Convert between units of length, area and volume, including cm² to m² and cm³ to litres. For GCSE, A-Level and Level 4. Free, no sign-up. | 137 |  |
| `formula-forge` | Formula Forge — MaffsGames | Rearranging Formulae Maths Game \| MaffsGames | 44 | Rearrange formulae through four progressive stages, with step-by-step feedback. For GCSE, A-Level and Level 4. Free, no sign-up. | 128 |  |
| `correlation-or-coincidence` | Correlation or Coincidence — MaffsGames | Correlation and Causation Maths Game \| MaffsGames | 49 | Does one variable cause the other, does something else cause both, or is it coincidence? For GCSE, A-Level and Core Maths. Free, no sign-up. | 140 |  |
| `chart-interrogator` | Chart Interrogator — MaffsGames | Interpreting Statistical Diagrams Maths Game \| MaffsGames | 57 | Read stem and leaf, box plots, cumulative frequency and histograms, then compare data sets. For GCSE, A-Level, Level 4 and Core Maths. Free, no sign-up. | 152 |  |
| `component-crusher` | Component Crusher — MaffsGames | Vectors Game – GCSE/A-Level/Level 4 Maths \| MaffsGames | 54 | Column vectors, magnitude, addition, scalar product and vector equations of lines. For GCSE, A-Level and Level 4. Free, no sign-up. | 131 |  |
| `expectation-station` | Expectation Station — MaffsGames | Expectation and E(X) Maths Game \| MaffsGames | 44 | Set up a probability table, calculate E(X), then say what it means in context. For GCSE, A-Level and Core Maths. Free, no sign-up. | 130 |  |
| `better-value` | Better Value — MaffsGames | Value for Money Game – GCSE/Core Maths \| MaffsGames | 51 | Compare phone contracts, energy tariffs and loans to decide which is better value. For GCSE and Core Maths. Free, no sign-up. | 125 |  |
| `given-that` | Given That — Conditional Probability — MaffsGames | Conditional Probability Maths Game \| MaffsGames | 47 | Conditional probability from two-way tables, Venn diagrams and frequency trees. For GCSE, A-Level, Level 4 and Core Maths. Free, no sign-up. | 140 |  |
| `screening-room` | Screening Room — False Positives and Base Rates — MaffsGames | False Positives and Base Rates Maths Game \| MaffsGames | 54 | Why a 99% accurate test can still be wrong most of the time: base rates with icon arrays. For GCSE, A-Level, Level 4 and Core Maths. Free, no sign-up. | 150 |  |
| `linear-equation-solver` | Linear Equation Solver — MaffsGames | Solving Linear Equations Game – GCSE Maths \| MaffsGames | 55 | Solve one- and two-step linear equations by choosing the inverse operation at each step. For GCSE. Free, no sign-up. | 116 |  |
| `core-maths-paper1` | Core Maths Paper 1 Practice — MaffsGames | Paper 1 Exam Practice Game – Core Maths \| MaffsGames | 52 | Exam-style questions for AQA Core Maths Paper 1: analysis of data and personal finance. For Core Maths. Free, no sign-up. | 121 | Exam-paper phrase, not a spec topic: teachers search for the paper. The topics are in the description. |
| `core-maths-paper2a` | Core Maths Paper 2A Practice — MaffsGames | Paper 2A Exam Practice Game – Core Maths \| MaffsGames | 53 | Exam-style questions for AQA Core Maths Paper 2A: critical analysis, normal distribution, estimation, correlation. For Core Maths. Free, no sign-up. | 148 | As paper 1. |
| `core-maths-paper2b` | Core Maths Paper 2B Practice — MaffsGames | Paper 2B Exam Practice Game – Core Maths \| MaffsGames | 53 | Exam-style questions for AQA Core Maths Paper 2B: critical analysis, expectation, cost-benefit and risk. For Core Maths. Free, no sign-up. | 138 | As paper 1. |
| `core-maths-paper2c` | Core Maths Paper 2C Practice — MaffsGames | Paper 2C Exam Practice Game – Core Maths \| MaffsGames | 53 | Exam-style questions for AQA Core Maths Paper 2C: graphs, rates of change and exponential models. For Core Maths. Free, no sign-up. | 131 | As paper 1. |
| `tax-theft` | Tax Theft — MaffsGames | Tax and National Insurance Game – Core Maths \| MaffsGames | 57 | Work out income tax, National Insurance and take-home pay from a payslip, step by step. For Core Maths. Free, no sign-up. | 121 |  |
| `stat-attack` | Stat Attack — MaffsGames | Grouped Frequency Tables Maths Game \| MaffsGames | 48 | Modal class, median class, estimated mean and standard deviation from grouped frequency tables. For GCSE, Level 4 and Core Maths. Free, no sign-up. | 147 |  |
| `growth-and-decay` | Growth and Decay — MaffsGames | Exponential Growth and Decay Maths Game \| MaffsGames | 52 | Exponential models: substitute, interpret the parameters, find constants and solve with logarithms. For A-Level, Level 4 and Core Maths. Free, no sign-up. | 154 |  |
| `graph-sketcher` | Graph Sketcher — MaffsGames | Sketching Graphs Maths Game \| MaffsGames | 40 | Tables of values, sketching and reading quadratic, cubic, exponential, reciprocal and trig graphs. For A-Level, Level 4 and Core Maths. Free, no sign-up. | 153 |  |
| `glorious-gantt` | Glorious Gantt Game — MaffsGames | Critical Path and Gantt Charts Maths Game \| MaffsGames | 54 | Critical path analysis: early and late times, the critical path, floats and Gantt charts. For Level 4 and Core Maths. Free, no sign-up. | 135 |  |
| `test-the-claim` | Test the Claim — MaffsGames | Hypothesis Testing Game – A-Level/Level 4 Maths \| MaffsGames | 60 | Six-step hypothesis tests for binomial, Poisson, normal and correlation. For A-Level and Level 4. Free, no sign-up. | 115 |  |
| `differentiation-duel` | Differentiation Duel — MaffsGames | Differentiation Game – A-Level/Level 4 Maths \| MaffsGames | 57 | Differentiate polynomials, trig and exponentials, with the chain, product and quotient rules. For A-Level and Level 4. Free, no sign-up. | 136 |  |
| `integration-duel` | Integration Duel — MaffsGames | Integration Game – A-Level/Level 4 Maths \| MaffsGames | 53 | Integrate polynomials, trig and exponentials, and integrate by parts. For A-Level and Level 4. Free, no sign-up. | 112 |  |
| `suvat` | SUVAT Selector — MaffsGames | SUVAT Equations Game – A-Level/Level 4 Maths \| MaffsGames | 57 | Pick the right SUVAT equation, then use it to find the answer. For A-Level and Level 4. Free, no sign-up. | 105 |  |
| `curling-friction` | Curling Friction — MaffsGames | Friction Problems Game – A-Level/Level 4 Maths \| MaffsGames | 59 | Friction, Newton's laws, SUVAT and momentum, in a curling setting. For A-Level and Level 4. Free, no sign-up. | 109 |  |
| `force-resolver` | Force Resolver — MaffsGames | Resolving Forces Game – A-Level/Level 4 Maths \| MaffsGames | 58 | Resolve forces on inclined planes, pulleys and connected particles. For A-Level and Level 4. Free, no sign-up. | 110 |  |
| `moments-master` | Moments Master — MaffsGames | Moments Game – A-Level/Level 4 Maths \| MaffsGames | 49 | Moments, beams, reactions at supports and tilting problems. For A-Level and Level 4. Free, no sign-up. | 102 |  |
| `log-laws` | Log Laws — MaffsGames | Laws of Logarithms Maths Game \| MaffsGames | 42 | Practise the laws of logarithms, then use them to solve exponential equations step by step. For A-Level, Level 3 and Level 4. Free, no sign-up. | 143 |  |
| `binomial-blaster` | Binomial Blaster — MaffsGames | Binomial Expansion Game – A-Level Maths \| MaffsGames | 52 | Binomial expansion, Pascal's triangle and nCr. For A-Level. Free, no sign-up. | 77 |  |
| `partial-fractions-duel` | Partial Fractions Duel — MaffsGames | Partial Fractions Game – A-Level/Level 4 Maths \| MaffsGames | 59 | Split into partial fractions: distinct linear, repeated and improper. For A-Level and Level 4. Free, no sign-up. | 112 |  |
| `proof-builder` | Proof Builder — MaffsGames | Mathematical Proof Game – A-Level/Further Maths \| MaffsGames | 60 | Find counterexamples, order the steps of a proof and build proofs by induction. For A-Level and Further Maths. Free, no sign-up. | 128 |  |
| `normal-navigator` | Normal Navigator — MaffsGames | Normal Distribution Maths Game \| MaffsGames | 43 | Z-scores, shaded regions and normal probabilities. For A-Level, Level 4 and Core Maths. Free, no sign-up. | 105 |  |
| `fermi-lab` | Fermi Lab — MaffsGames | Fermi Estimation Maths Game \| MaffsGames | 40 | Break a big estimation question into smaller steps and estimate each one. For KS3, GCSE, A-Level, Level 4 and Core Maths. Free, no sign-up. | 139 |  |
| `dimension-checker` | Dimension Checker — MaffsGames | Dimensional Analysis Maths Game \| MaffsGames | 44 | Check whether physics equations are dimensionally consistent using M, L and T. For A-Level and Level 4. Free, no sign-up. | 121 |  |
| `factor-theorem` | Factor Theorem — Learn + Practice — MaffsGames | Factor and Remainder Theorem Maths Game \| MaffsGames | 52 | Learn the factor theorem, the remainder theorem and algebraic division, then practise. For A-Level and Level 4. Free, no sign-up. | 129 |  |
| `boolean-blitz` | Boolean Blitz — MaffsGames | Boolean Algebra Game – Level 4 Maths \| MaffsGames | 49 | Simplify Boolean expressions with the logic laws, with full step-by-step working. For Level 4. Free, no sign-up. | 112 |  |
| `truth-will-set-you-free` | The Truth Will Set You Free — MaffsGames | Truth Tables Game – Level 4 Maths \| MaffsGames | 46 | Build truth tables from engineering scenarios and match them to Boolean expressions. For Level 4. Free, no sign-up. | 115 |  |
| `complex-converter` | Complex Converter — MaffsGames | Complex Numbers Game – Level 4/Further Maths \| MaffsGames | 57 | Convert complex numbers between Cartesian, polar and exponential form. For Level 4 and Further Maths. Free, no sign-up. | 119 |  |
| `matrix-crunch` | Matrix Crunch — MaffsGames | Matrices Game – Level 4/Further Maths \| MaffsGames | 50 | Determinants, inverse matrices and solving equations with Cramer's rule. For Level 4 and Further Maths. Free, no sign-up. | 121 | 'Matrices' keeps 'Further Maths' in the title; 'Determinants and Inverses' would drop it. |
| `characteristic-quest` | Characteristic Quest — MaffsGames | Characteristic Equations Maths Game \| MaffsGames | 48 | Find the characteristic equation of a matrix: eigenvectors, part 1. For Level 4 and Further Maths. Free, no sign-up. | 116 |  |
| `eigenvalue-extractor` | Eigenvalue Extractor — MaffsGames | Eigenvalues Game – Level 4/Further Maths \| MaffsGames | 53 | Solve the characteristic equation to find eigenvalues: eigenvectors, part 2. For Level 4 and Further Maths. Free, no sign-up. | 125 |  |
| `eigenvector-engine` | Eigenvector Engine — MaffsGames | Eigenvectors Game – Level 4/Further Maths \| MaffsGames | 54 | Find the eigenvector for each eigenvalue: eigenvectors, part 3. For Level 4 and Further Maths. Free, no sign-up. | 112 |  |
| `six-sevens-bruv` | Six Sevens, Bruv — MaffsGames | Times Tables Game – KS3/GCSE Maths \| MaffsGames | 47 | Times tables to 12 by 12, typed not chosen; each fact you know lights up your own grid. For KS3 and GCSE. Free, no sign-up. | 123 |  |
| `free-daily-pizza` | Free Daily Pizza — MaffsGames | Fractions, Decimals and Percentages Maths Game \| MaffsGames | 59 | Convert between fractions, decimals and percentages, and find fractions and percentages of amounts. For KS3 and GCSE. Free, no sign-up. | 135 |  |
| `just-pythag-it-bruv` | Just Pythag It, Bruv — MaffsGames | PHRASE NEEDED | — | Use Pythagoras' theorem with a calculator to find the hypotenuse or a shorter side, from simple triangles to ladders and ramps. For KS3. Free, no sign-up. | 154 | STOP IF: no spec-map reference (unlisted, noindex). Suggestion: **Pythagoras' Theorem** (G20). Its only roster level is KS3 (shown as Foundation, SR-11), so the title would say KS3 on a resit game. |

**Titles with the levels part dropped (over 60 with it), 41:** `sequence-solver`, `estimation-golf`, `estimation-engine`, `prime-factorisation`, `percentage-flip`, `fraction-equivalence`, `spot-the-error`, `gradient-hunter`, `terrible-advice`, `maths-court`, `decimal-detective`, `higher-power`, `prisoners-dilemma`, `seven-bridges`, `distinctly-average`, `quadratic-factoriser`, `trig-wars`, `proportion-blaster`, `trig-identity-duel`, `simultaneous-solver`, `probability-paradox`, `formula-unlocked`, `scale-factor-scaling`, `unit-converter`, `formula-forge`, `correlation-or-coincidence`, `chart-interrogator`, `expectation-station`, `given-that`, `screening-room`, `stat-attack`, `growth-and-decay`, `graph-sketcher`, `glorious-gantt`, `log-laws`, `normal-navigator`, `fermi-lab`, `dimension-checker`, `factor-theorem`, `characteristic-quest`, `free-daily-pizza`.

## For review: what I would most like a ruling on

1. **41 of 97 titles lose their levels** under the brief's rule (drop the levels part when over
   60). Many are the GCSE and KS3 games the mission puts first, so "GCSE" leaves their titles. An
   alternative that keeps the rule's spirit: when over 60, keep the **first** level only
   ("Prime Factorisation Game – Year 6 Maths"), and drop it entirely only if still over 60. I have
   not applied it; say if you want it and I will regenerate the table.
2. **The two PHRASE NEEDED rows** (`truth-buster`, `just-pythag-it-bruv`), suggestions in their Note.
3. **The four Core Maths papers** use an exam-paper phrase, not a spec topic (Note column).
4. **Rules 1-3 and 5 above**: each is my call and each is a one-line change.

Regenerate this table after editing `data/games.json`: `python scripts/draft-seo-titles.py`.
