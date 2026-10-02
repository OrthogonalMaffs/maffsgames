# Level 3 SOW coverage mapping

**Read-only analysis, 18 September 2026.** Maps Jon's EAL Level 3 Engineering Mathematics scheme of work
against the 93 live games and 8 live escape rooms, so that any new build starts from what is actually
missing rather than from what sounds missing.

**Sources read**

- the AME3-004 scheme of work `.docx` (local only; its path is in `CLAUDE.local.md`) — EAL Level 3 Engineering, AME3-004 Engineering
  Mathematics (= AMEDK3-003), Tuesday/Wednesday/Thursday classes on a Level 3 engineering course. 17 weeks, 3.5 hours a week, w/c
  14/09/26 to w/c 25/01/27. Read by unzipping the .docx and stripping the tags from `word/document.xml`.
- `.claude/rules/game-roster.md` — 93 games.
- `docs/canon.md` §11.1 — the eight live rooms.
- The game files themselves for every game named below. Where the roster and the file disagree, the file wins
  and the disagreement is stated.

**Nothing in the repo was changed.** This file is the whole output.

---

## Mismatch found, reported not fixed

The contract's STOP IF on the roster disagreeing with `games/` fired once:

> **`games/the-perfect-prank/` exists but is not on the roster.** It holds a single `index.html` describing a
> maths escape room ("Your teacher is out for 40 minutes. Pull off the perfect harmless prank"). It is
> referenced from neither `index.html` nor `sitemap.xml`, so it is unlinked rather than live. 94 folders
> against 93 roster rows; every roster row does have a folder.

No other mismatch. Not touched, per the contract.

## The scheme of work at a glance

Seventeen lessons, of which **ten teach new content** and seven are revision, assessment or flex. Only the ten
teaching lessons carry topics to map; the other seven are listed at the end for completeness.

| Lesson | LO | Topic |
| --- | --- | --- |
| 1 | LO1 | One- and two-step equations, rearranging formulae |
| 2 | LO1 | Indices, standard form, factorisation |
| 3 | LO1 | Quadratics — factorising and the quadratic formula |
| 4 | LO1 | Simultaneous equations; straight-line graphs |
| 5 | LO1 | Logarithms and exponentials; applied-algebra consolidation |
| 9 | LO2 | Ratios, right-angled triangles, trigonometric graphs, CAST |
| 10 | LO2 | Radians; inverse trig; sine and cosine rules |
| 11 | LO3 | Transposition of formulae; surface areas and volumes |
| 14 | LO4 | Differentiation and standard integrals |
| 15 | LO5 | Statistical diagrams, central tendency, dispersion |

---

## Topic by topic, in SOW order

### Lesson 1 — One- and two-step equations *(split verdict)*

**Solving one- and two-step equations: GAP.** No game on the roster solves a linear equation in algebraic
notation. The three near misses are all something else:

- `think-of-a-number` — Year 6 only, 50 questions. "I think of a number" puzzles undone step by step. This is
  the inverse-operation idea without the notation, and it is four levels below this class.
- `equation-builder` — **forms** equations, never solves them. Described from the file: 120 questions, split
  exactly 40 `ks3` / 40 `gcse` / 40 `level4`, in two mechanics — `assembly` 68 (drag tiles into slots to build
  the equation) and `gapfill` 52 (slots pre-filled except the missing pieces). Every question carries a
  `topic` label, and the spread is wide and thin: Forming Equations 10, Probability 6, and then 2–4 apiece
  across roughly sixty topics, from Ratio and Reverse Percentage up to Eigenvalues, Maclaurin Series and
  De Moivre's Theorem at `level4`. Relevant counts for this unit: Simultaneous Equations 2, Quadratics 2,
  Quadratic Formula 1, Standard Form 2, Logarithms 2, Logarithm Laws 1, Differentiation 2, Integration 2.
  **The learner never evaluates or solves** — the answer is always the assembled expression. It is the Word
  Problem suite's middle game (decode the topic → build the equation → spot the error), and it is a
  translation exercise, so it cannot carry any SOW topic on its own.
- `maths-court`, `spot-the-error`, `terrible-advice` — linear equations appear inside scenarios, but the task
  is judging an argument or finding someone else's error, not solving.

This is the unit's opening lesson and the thing the SOW says "everything in LO1 rests on".

**Rearranging formulae: COVERED, and covered at the right level.** Two games, both with a Level 4 tier:

- `formula-unlocked` — three separate banks read from the file. `Q_GCSE` 29 items across four named stages
  (one step 10, two steps 8, powers and roots 7, variable appears twice 4); `Q_ALEVEL` 6 items (stages 2–4);
  **`Q_LEVEL4` 14 items** on engineering formulae — `V = IR`, `σ = F/A`, `ε = ΔL/L`, `P = I²R`, `σ = Eε`,
  `v = u + at`, `M = Fd`, `P_total = P₁ + P₂ + P₃`. Multiple choice with two staged hints and a worked
  step list.
- `formula-forge` — `gcse` and `level4` banks, four stages each (`s1`–`s4`), 45 formula items in total, with
  hint-then-hint-then-steps scaffolding and explicit "what undoes multiplication?" inverse-operation prompts.

Level tier that fits: **L4 on both.** The Level 4 bank of `formula-unlocked` is the closest thing on the site
to this cohort's own trade formulae.

### Lesson 2 — Indices, standard form, factorisation *(split verdict)*

**Indices: PARTIAL.** `games/index-laws/` described from the file:

- One flat bank of **45 multiple-choice questions**, 12 served per play, 7 seconds each, KaTeX rendered.
- Six rules, by count: Fractional Power 10, Multiply 8, Divide 8, Negative Power 8, Power of a Power 7,
  Zero Power 4.
- Questions are pure manipulation — `x³ × x⁴`, `2x² × 3x⁵`, `a⁻² × a⁵`, `x^½ × x^½`, `3⁴ × 3²` — each with
  three distractors and a one-line explanation ("Add the powers: 3+4=7").
- **There are no level tiers in the file at all.** The roster lists it as "GCSE, A-Level"; the file has one
  bank and no tier switch. This is a roster description that overstates the game, not a missing folder, so it
  is noted here rather than raised as the STOP IF mismatch.

What is missing against the SOW: the laws are drilled, not derived from first principles; nothing uses
engineering magnitudes; the seven-second timer makes it a recall drill rather than the applied work the
lesson wants.

**Standard form: COVERED.** `standard-form-blitz`, GCSE + A-Level, 50+50 questions — convert, multiply,
divide. The SOW additionally wants standard form entered and read back on the calculator, which no game does
(see the note on calculator work at the end).

**Factorisation: PARTIAL, and the partial part is the one this lesson leads with.** `quadratic-factoriser`
generates **monic quadratics only** — `genQuadratic()` picks two integer roots in ±1..8 and builds
`x² + bx + c`, answered on a two-number bracket picker, 10 per game. The SOW teaches "factorising by common
factor and by grouping, building to quadratic trinomials". **Common factor and grouping are not covered
anywhere**; only the trinomial endpoint is, and only with a leading coefficient of 1.

### Lesson 3 — Quadratics: factorising and the quadratic formula — PARTIAL

Factorising is as described above: monic only, integer roots, no `a ≠ 1`.

**The quadratic formula is not in any game.** `equation-builder` has exactly one question tagged
"Quadratic Formula", and that question asks the learner to *assemble* the formula from tiles, not to use it.
Nothing covers deciding between the two methods, and nothing covers recognising that there is no real root —
`quadratic-factoriser` cannot generate an unfactorisable case by construction.

### Lesson 4 — Simultaneous equations; straight-line graphs *(split verdict)*

**Simultaneous equations: PARTIAL.** `simultaneous-solver` from the file: `QUESTIONS` is an object keyed
`gcse` and `alevel`, 20 questions served per game, multiple choice with three distractors, 100-point base with
a time bonus. The GCSE bank is linear pairs with small positive integer solutions, each system asked twice —
once "Find x", once "Find y" (`2x + y = 7 / x − y = 2`, `3x + 2y = 12 / x + 2y = 8`, and so on), all set up for
elimination.

What is missing: the learner never carries out or chooses a method — picking 3 from four numbers is not
eliminating a variable. The SOW wants elimination *and* substitution applied to the same pair, and the same
pair solved graphically and algebraically with the results compared. There is also no Level 4 tier.
`equation-builder` adds 2 forming-only questions on the topic.

**Straight-line graphs: COVERED at GCSE/A-Level, no L4 tier.**

- `gradient-hunter` — 45 questions, 27 of type `calculate` and 18 of type `reading`, on a canvas with plotted
  lines; levels `gcse`, `core`, `alevel`. This is exactly the SOW's "gradient read from a plot and calculated
  from two points".
- `coordinate-geometry-dash` — `gcse` and `alevel`, plotted points, lines and circles.
- `graph-transformer` — translations, reflections, stretches onto a target curve.

Gradient and intercept are well served; the *graphical solution of a simultaneous pair* is the piece that
falls between this topic and the one above, and nothing covers it.

### Lesson 5 — Logarithms and exponentials — COVERED

- `log-laws` — 45 questions across six named categories: Power Rule 9, Product Rule 8, Quotient Rule 8,
  Change of Base 7, Combined Laws 7, Special Values 6. Roster level A-Level, L4.
- `growth-and-decay` — 45 exponential-modelling scenarios; Core, A-Level, **L4**. This carries the SOW's
  "exponential growth and decay applied to engineering contexts".
- `core-maths-paper2c` — S3.13 exponential functions, in exam-question form.

Level tier that fits: **L4 on both of the first two.** The one thin spot is logs *as the inverse of
exponentials*, which the laws drill assumes rather than teaches.

**Update, 28 Sep 2026: Solve mode closes the gap.** The laws drill above covered this lesson for
*recognition* only; it never asked a student to *use* a law to solve an equation. `log-laws` now has a
**Solve** mode, opened at `?level=level3` (labelled "Level 3 (Engineering)"), in which the student picks
every step: take logs, the power, product and quotient laws, log 10 = 1 / ln e = 1, undo the log,
rearrange. It runs in six stages: aˣ = b; a^(kx) = b and a^(x+k) = b; base e, including capacitor
discharge V = V₀e^(−t/RC); the quotient law; the product law, with the root that makes a log argument
negative rejected; and two bases, aˣ = b^(x−k). log₁₀ and ln only, so no change of base. 501 items,
every line SymPy-verified (`scripts/verify-log-laws.py`). Contract: `docs/next-contract-log-laws-solve.md`.

**"Applied-algebra consolidation", the second half of this lesson, is UNCLEAR as a coverage question** — the
SOW's wording is "mixed consolidation set across the whole of LO1", which is a revision activity over the
topics above rather than a topic of its own. Nothing to map; recorded here and carried on, as the contract
requires.

### Lesson 9 — Trigonometry foundations *(split verdict)*

**Ratios and right-angled triangles: COVERED.** `trig-worms` (level `gcse`, cannon aiming with SOH CAH TOA),
`trig-wars` (artillery, set angle and power), `bearing-blitz` (bearings by eye). All GCSE-pitched, none
tiered to L4.

**Trigonometric graphs and CAST: GAP.** Searched every game for "unit circle", "trig graph", "sin graph" and
CAST as a taught rule — nothing. No game plots a sine or cosine curve, and nothing asks for *every* solution
in range rather than the first. Given the SOW's emphasis ("CAST used to find every solution in range, not just
the first"), this is a real hole rather than a nicety.

### Lesson 10 — Radians; inverse trig; sine and cosine rules *(split verdict)*

**Sine and cosine rules: COVERED.** `trig-identity-duel`, `QUESTIONS` keyed `gcse` and `alevel` — exact values
for 30°/45°/60° first, then sine and cosine rule application. Roster tags it GCSE, A-Level, **L4**.

**Radians: GAP.** No game converts degrees to radians or back. The only files containing the word are
`graph-sketcher` and `higher-power`, and in neither is it the thing being practised. The SOW also wants the
calculator mode changed to match, which nothing covers.

**Inverse trigonometric functions and the range of their results: GAP.** Nothing covers the range question,
which is the part learners get wrong.

### Lesson 11 — Transposition of formulae; surface areas and volumes *(split verdict)*

**Transposition: COVERED** — the same two games as Lesson 1, and the SOW itself says this lesson draws
directly on that rearrangement. Stage 3 of both `formula-unlocked` and `formula-forge` is "powers and roots",
which is the SOW's "subjects inside a root or a power". Stage 4 handles the variable appearing twice.
**L4 tiers exist on both.**

**Surface areas and volumes: GAP.** No game calculates the surface area or volume of a prism, cylinder, cone
or sphere. What exists nearby, and why none of it covers this:

- `scale-factor-scaling` (gcse/alevel/level4) — k, k², k³ scaling *between* solids, not the measure itself.
- `unit-converter` (GCSE/A-Level/L4) — converts length, area and volume units, does not compute them.
- `formula-forge` — uses volume formulae as things to rearrange, never to evaluate.
- `new-shapes` — Year 6, parallelogram/trapezium/prism, four levels below this class.

Composite solids broken into parts, which is where the LO3 marks are, are covered nowhere.

### Lesson 14 — Differentiation and standard integrals — COVERED (over-level)

- `differentiation-duel` — A-Level, L4. Rules by count: Power 24, Chain 20, Product 13, Trig 8, Quotient 8,
  Implicit 8, Parametric 7, Exponential 6, Logarithm 4.
- `integration-duel` — Power 10, Trig 8, Kinematics 8, Logarithm 7, Definite 7, By Parts 7, Exponential 6,
  Reverse Chain 5, AC Circuits 5, Substitution 5.
- `graph-sketcher` (Core/A-Level/L4) — stationary points, roots, reading a curve.
- `gradient-hunter` — gradient read from a plot, which is the SOW's stated way in.

**The caveat is that both duels sit above the SOW, not below it.** This lesson is "the whole of LO4 in one
lesson", polynomials from the standard result with a formula sheet. A learner sent to `differentiation-duel`
meets the chain, product, quotient, implicit and parametric rules, none of which is in the unit. Usable, but
only with the categories filtered — and the game has no filter.

### Lesson 15 — Statistics: diagrams, central tendency, dispersion — COVERED

- `stat-attack` — `SCENARIOS` keyed `gcse` and, per the roster, **L4**. Each scenario is a full grouped
  frequency table carrying modal class, median class, mean, variance, standard deviation, midpoints, Σfx and
  Σfx². This is the SOW's "mean, median and mode for grouped and ungrouped data" and "range and standard
  deviation" almost exactly.
- `chart-interrogator` — 40 scenarios by level: core 12, gcse 10, alevel 10, **l4 8**. Two-phase diagram
  reading then structured comparison.
- `core-maths-paper1` — histograms, box plots, stem-and-leaf in exam form.
- `regression-rumble`, `correlation-or-coincidence` — scatter diagrams and correlation.

One genuine edge: the SOW says diagrams are **drawn** as well as read, and every game here reads them. And
standard deviation "on the calculator in statistics mode" is not something any game can teach.

### The seven non-teaching lessons

Lessons 6, 12 and 16 are revision plus two full mock papers; lessons 7, 13 and 17 are the 2-hour centre-marked
004A/004B/004C knowledge assessments; lesson 8 is the banked flex week for 004A feedback, resits and
re-teach. **No topic coverage to map.** Worth recording, though, that nothing on the site is shaped like a
2-hour written paper against the EAL descriptor table — the site is drill and context, and the SOW's
assessment rehearsal is paper-based by design.

---

## Where the escape rooms land

All eight live rooms are pitched KS3, GCSE or Core, none at Level 3 or Level 4, and each is a 15-minute group
activity rather than individual practice. Read against the SOW they are prior-knowledge or context, not
coverage. The two the contract names, plus what the other six actually contain, from their `room.js` files:

| Room | Maths in its three locks | Against the SOW |
| --- | --- | --- |
| `comic-caper` | Factors, primes, HCF | Below L3 — assumed prior knowledge |
| `kiln-disaster` | Multiples, LCM, order of operations | Below L3 — assumed prior knowledge |
| `rugby-mud` | Similar-shape area scale factor; combined rates; **index laws with simultaneous equations** (2^H × 4^A = 2^(H+2A), then H + 2A = N with A = H + d) | The closest thing on the site to Lesson 2 + Lesson 4 in one applied context |
| `canteen-hack` | Reverse mean; **simultaneous equations by elimination**; fractions of an amount | Touches Lesson 4 and Lesson 15 |
| `hamster-heist` | Circumference and rate; bounds of accuracy with volume; **gradient of a straight line from two points** | Touches Lesson 4 |
| `heatwave-mutiny` | LCM; **cube surface area solved back to an edge length**; inequalities with primes | Touches Lesson 11, from the transposition side |
| `pe-shed-rebellion` | Sector area; **inverse proportion**; linear sequence | Peripheral to LO1 |
| `prom-budget` | Reverse percentages; **exponential growth solved for n**; Venn/set counting | Touches Lesson 5 |

`rugby-mud` is the one worth showing this cohort as it stands.

## A standing caveat: the calculator

The SOW builds calculator fluency deliberately — the Casio fx-991EX/fx-991CW is named in every lesson's
resources, standard form is entered and read back on it, degree/radian mode is changed on it, and standard
deviation is computed in its statistics mode. **No game on the site involves the calculator**, and none can.
This is not a gap a build can close; it is a limit on what the site can do for this unit, and it is worth
saying out loud before anything is scoped.

---

## The gaps, shortest build first

Eight, ordered by build cost, with what each one looks like.

1. **Radians, and degrees ↔ radians conversion** (Lesson 10) — *content top-up.* `unit-converter` already
   owns the "convert between two units" mechanic and already has a Level 4 tier; a radians bank drops into it.
2. **The quadratic formula, and recognising no real root** (Lesson 3) — *content top-up, possibly a new tier.*
   `quadratic-factoriser` already generates `b` and `c`; the discriminant path and an unfactorisable branch
   are additions to an existing generator rather than a new game.
3. **Level 4 tiers on the LO1 games that lack one** — *content top-up, four games.* `index-laws` (no tiers at
   all), `simultaneous-solver` (`gcse`/`alevel` only), `gradient-hunter` (`gcse`/`core`/`alevel`),
   `quadratic-factoriser` (`gcse`). Each already has the tier-switch pattern in a sibling game to copy.
4. **Factorising by common factor and by grouping** (Lesson 2) — *new tier on an existing game, with a new
   input.* It can live inside `quadratic-factoriser` as stages ahead of the current one, but the bracket
   picker only takes two integers, so the answer mechanic has to be rebuilt.
5. **Solving one- and two-step linear equations** (Lesson 1) — *new game.* Nothing covers it, and it is the
   lesson the whole of LO1 is said to rest on. The mechanic is well understood and the bank is cheap to
   write; this is the smallest genuinely new build on the list, and the highest value.
6. **Surface area and volume of prisms, cylinders, cones and spheres, including composite solids**
   (Lesson 11) — *new game.* Needs diagrams, which is the cost; it is half of LO3 and covered nowhere.
7. **Trigonometric graphs, CAST and inverse trig range** (Lesson 9 and 10) — *new game.* Canvas plotting of
   sine and cosine curves plus every-solution-in-range makes this the most expensive of the teaching gaps.
8. **Drawing statistical diagrams rather than reading them** (Lesson 15) — *new game.* A drawing UI for bar,
   pie, histogram and scatter is the heaviest build here, and it is the least of the gaps, because
   `stat-attack` and `chart-interrogator` already cover the calculation and the interpretation.

Items 1–3 are top-ups to games that exist. Items 5–7 are the three topics where an L3 apprentice would find
nothing on the site at all.
