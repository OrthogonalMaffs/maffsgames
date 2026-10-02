# KaTeX wrapper audit: where prose loses its spaces

Read-only audit, 2 Oct 2026 (cloud session). Contract: the KaTeX wrapper audit in `docs/todo.md`'s
START block, feeding §1.30 (proof-builder) and §1.31 (B7 sees only `K()` / `katex.renderToString()`
call sites). Jon's rulings of 2 Oct, mid-audit: test-the-claim counts as affected (see §3); a second
count sits beside B7's; the test-the-claim defect is filed as §1.32. **Nothing in a game, an asset or
the checker was changed.** The scripts are not committed; §9 says how to rerun them.

## 1. Findings

1. **19 games render prose through KaTeX maths mode and lose its spaces, 386 distinct strings, by
   B7's own prose test.** B7 has reported 0 for every one of them, because it sees only the fields
   named in a `K(x.field)` or `katex.renderToString(x.field)` call. None of the 19 is reached that
   way. proof-builder alone is 155: every proof-mode text that goes through `rkStr()`, including
   all 12 induction stage prompts (§1.30).
2. **B7's prose test undercounts.** It needs two adjacent words, so a single word between pieces of
   maths is never counted: `0.05 and P(X ≤ 1)` renders as `0.05andP(X≤1)`, `Find \mathbf{a} + \mathbf{b}.`
   as `Finda + b.` The second count (§4) finds **522 strings in 25 games** (one of them regression-rumble's withdrawn
   file, not served). A hand-read of 20 strings
   flagged by the second count alone found **17 real defects (16 prose, 1 unit) and 3 false positives**.
3. **component-crusher is clean by B7 and not clean by the second count: 31 strings.** `PQ()` sends a
   string with no `\( \)` whole to `K()`, by design (`schools/assets/mathtext.js`: "whole-expression"
   strings keep going through `K()`). Its 31 `Find …` prompts are such strings, and the one word "Find"
   runs into the maths. §1.10's fix is intact for every string that was given `\( \)`; these never were.
4. **test-the-claim has a live defect §1.10 did not reach, filed as §1.32.** `checkStep3()` shows
   `q.crExplanation` through `K(hint)` (`index.html:1718-1719`). Confirmed by calling the game's own
   `checkStep3()` with a wrong value on all 36 binomial, Poisson and Normal questions: **15 lose their
   spaces (8 binomial, 7 Poisson)**, e.g. `P(X ≤ 0) = 0.0352 < 0.05 and P(X ≤ 1) = 0.1671 > 0.05` →
   `P(X≤0)=0.0352<0.05andP(X≤1)=0.1671>0.05`. The other 21, and all 8 correlation explanations, were
   authored with `\text{}` and render correctly. B7's prose test flags only 1 of the 15 (`x = 9 does
   not reach CR`), since "and" and "Upper" are single words. **Correction to what was reported to Jon
   mid-audit:** "all 36 discrete explanations" was wrong on both counts. The 36 include 12 Normal
   ones, and 15 of the 36 are affected, not all.
5. **The class is concentrated in one wrapper shape:** a game-local helper (`rk`, `rkStr`, `rkI`,
   `tex`, `K` …) that hands its whole argument to `katex.render`/`renderToString`, called on a bank field
   that holds prose: options ("Cannot tell" → `Cannottell`), worked steps, hints, proof lines. 72 of the
   84 wrappers found hand their whole argument to KaTeX. Only the 6 games that route through `MaffsText.html` (component-crusher, factor-theorem, free-daily-pizza, log-laws, quadratic-factoriser, test-the-claim)
   split prose from maths, and only for strings authored with `\( \)`.

## 2. Method

**Wrappers, by behaviour.** Every game's inline scripts were parsed with the checker's own parser
(`bank_common.parse_game_source`). A function is a wrapper when one of its parameters, or a local
derived from it (assignment, string method, `forEach`/`map` callback), reaches the first argument of
`katex.render`/`katex.renderToString` or `MaffsText.html`, directly or through another wrapper, to a
fixed point. A parameter used only for a field read (`q.prompt`) does not make a wrapper. That function
is a call site, and is treated as one. Names played no part. 84 wrappers in 50 files (72 call KaTeX
directly, 8 through one other wrapper, 4 through two or three), plus 6 direct `katex.*` calls in anonymous
callbacks.

**Runtime capture.** An init script trapped the `window.katex` the CDN script sets and wrapped
`render`/`renderToString`. Each call logged the string, `displayMode`, the caller stack (inline-script
line numbers are file line numbers, so each frame maps to a wrapper and its call site), and the visual
text KaTeX produced (`.katex-html` only, as B7 reads it). The games were driven by `check-site.py`
tier 3, imported and run unchanged in the sandbox recipe of `docs/sandbox-checks.md`, 50 questions per
level run: 163 runs, 2,223 questions, 0 FAIL. Tier 3 always takes a setup menu's first entry, so the
three games with menus (complex-converter, factor-theorem, proof-builder) were run again with each
other entry. test-the-claim, which tier 3 cannot drive, was confirmed through its own `checkStep3()`
(finding 4).

**Bank fallback.** For every KaTeX call site, the strings that can reach it were rebuilt from the live
bank (`extract-banks.py` output, 82 live + 1 static + 13 generators, as expected). The rebuild follows
the site's argument back through locals and iteration callbacks, and **evaluates the argument
expression per question**, so `rkStr(currentQ.hint2||currentQ.hint1)` gives `hint2`, or `hint1` only
where there is no `hint2`. Likewise `K(hint)` with `hint = cr ? q.crExplanation : 'Expected: ' +
q.pValueExpr` gives both branches, prefix included. Each string was then **handed to the site's own
callee in the game page** (the wrapper itself, or `MaffsText.html`), so it is rendered exactly as that
function renders it. A site whose argument calls a game function (`formatQuadratic`, `ratTex`) cannot
be rebuilt from a bank and is runtime-only. Source literals at call sites were rendered the same way.
Two wrappers are unreachable by name and are pure pass-throughs: given-that's `kx`, inside an IIFE, and
log-laws' Solve helpers. given-that's was reproduced from its own call; the log-laws helpers render
generator output, which runtime covers.

**Classification.** Every distinct string KaTeX received, per game:
- **B7 test (headline):** `bank_common.katex_prose_hazard()`, unchanged.
- **Second count:** a string counts if any real word loses, in the rendered output, a space it had in
  the source. "Real word" is B7's own definition: a run of two or more letters, after B7's stripping of
  `\text{}`/`\mathrm{}`/`\operatorname{}` and bare commands. B7 has no dictionary. "Rendered output" is
  what the student sees. KaTeX draws operator and relation spacing as empty `.mspace` spans, so each
  positive-width `.mspace` reads as a space, zero-width spaces are dropped, and no-break and thin
  spaces read as spaces. Rendered with the KaTeX 0.16.9 the site loads.

"Runtime" in the tables means seen during play (or on page load). "Fallback only" means rendered from
the bank or a source literal through the game's own function, but not reached during play.

## 3. The known positive and negatives

| Check | Result |
|---|---|
| proof-builder's induction prompts (known positive, §1.30) | **Affected: all 12** `INDUCTION.stages[].prompt` strings fail B7's test via `rkStr` `:561`, 8 of them reached at runtime. "What value of n should we use for the base case?" → `Whatvalueofnshouldweuseforthebasecase?` |
| component-crusher (known negative, §1.10) | **B7: 0.** Second count: 31 (finding 3) |
| factor-theorem (known negative, §1.10) | **B7: 0. Second count: 0.** 89 strings |
| test-the-claim `checkStep3` → `K(hint)` (confirmed positive, Jon's ruling) | **Affected:** B7 1, second count 15, all 15 confirmed at runtime (finding 4) |

## 4. Summary, sorted by B7's count

Counts are distinct strings KaTeX received. "Second count" includes B7's (no string is flagged by B7
and not by the second count, except higher-power's one false positive, §6).

| Game | B7 test (headline) | of which runtime / fallback only | Second count | of which runtime / fallback only | Strings KaTeX received | runtime / fallback only |
|---|---:|---|---:|---|---:|---|
| `proof-builder` | **155** | 66 / 89 | 171 | 76 / 95 | 392 | 154 / 238 |
| `moments-master` | **43** | 1 / 42 | 47 | 1 / 46 | 219 | 134 / 85 |
| `matrix-crunch` | **32** | 7 / 25 | 37 | 8 / 29 | 283 | 68 / 215 |
| `curling-friction` | **30** | 0 / 30 | 41 | 1 / 40 | 251 | 110 / 141 |
| `formula-forge` | **30** | 0 / 30 | 34 | 1 / 33 | 328 | 285 / 43 |
| `circle-theorem-spotter` | **17** | 0 / 17 | 27 | 0 / 27 | 111 | 1 / 110 |
| `force-resolver` | **15** | 0 / 15 | 18 | 1 / 17 | 210 | 145 / 65 |
| `sequence-solver` | **13** | 0 / 13 | 22 | 0 / 22 | 393 | 41 / 352 |
| `binomial-blaster` | **13** | 0 / 13 | 13 | 0 / 13 | 346 | 111 / 235 |
| `boolean-blitz` | **11** | 0 / 11 | 13 | 0 / 13 | 276 | 246 / 30 |
| `eigenvalue-extractor` | **7** | 5 / 2 | 7 | 5 / 2 | 153 | 140 / 13 |
| `characteristic-quest` | **6** | 4 / 2 | 7 | 5 / 2 | 149 | 138 / 11 |
| `standard-form-blitz` | **5** | 0 / 5 | 5 | 0 / 5 | 434 | 203 / 231 |
| `partial-fractions-duel` | **3** | 0 / 3 | 3 | 0 / 3 | 98 | 54 / 44 |
| `trig-identity-duel` | **2** | 0 / 2 | 3 | 0 / 3 | 276 | 99 / 177 |
| `eigenvector-engine` | **1** | 1 / 0 | 16 | 15 / 1 | 94 | 87 / 7 |
| `test-the-claim` | **1** | 1 / 0 | 15 | 15 / 0 | 747 | 32 / 715 |
| `screening-room` | **1** | 0 / 1 | 2 | 1 / 1 | 158 | 64 / 94 |
| `higher-power` | **1** | 0 / 1 | 1 | 0 / 1 | 242 | 22 / 220 |
| `component-crusher` | **0** | 0 / 0 | 31 | 3 / 28 | 56 | 9 / 47 |
| `differentiation-duel` | **0** | 0 / 0 | 2 | 2 / 0 | 437 | 183 / 254 |
| `formula-unlocked` | **0** | 0 / 0 | 2 | 2 / 0 | 272 | 246 / 26 |
| `regression-rumble` | **0** | 0 / 0 | 2 | 0 / 2 | 7 | 0 / 7 |
| `stat-attack` | **0** | 0 / 0 | 2 | 0 / 2 | 44 | 6 / 38 |
| `equation-builder` | **0** | 0 / 0 | 1 | 0 / 1 | 33 | 0 / 33 |
| `better-value` | **0** | 0 / 0 | 0 | 0 / 0 | 4 | 4 / 0 |
| `complex-converter` | **0** | 0 / 0 | 0 | 0 / 0 | 288 | 235 / 53 |
| `distinctly-average` | **0** | 0 / 0 | 0 | 0 / 0 | 3 | 3 / 0 |
| `expectation-station` | **0** | 0 / 0 | 0 | 0 / 0 | 16 | 16 / 0 |
| `expected-damage` | **0** | 0 / 0 | 0 | 0 / 0 | 1 | 1 / 0 |
| `factor-theorem` | **0** | 0 / 0 | 0 | 0 / 0 | 89 | 36 / 53 |
| `formula-plug-in` | **0** | 0 / 0 | 0 | 0 / 0 | 103 | 3 / 100 |
| `free-daily-pizza` | **0** | 0 / 0 | 0 | 0 / 0 | 64 | 64 / 0 |
| `given-that` | **0** | 0 / 0 | 0 | 0 / 0 | 228 | 63 / 165 |
| `gradient-hunter` | **0** | 0 / 0 | 0 | 0 / 0 | 7 | 7 / 0 |
| `graph-sketcher` | **0** | 0 / 0 | 0 | 0 / 0 | 55 | 16 / 39 |
| `graph-transformer` | **0** | 0 / 0 | 0 | 0 / 0 | 6 | 6 / 0 |
| `growth-and-decay` | **0** | 0 / 0 | 0 | 0 / 0 | 88 | 19 / 69 |
| `index-laws` | **0** | 0 / 0 | 0 | 0 / 0 | 201 | 138 / 63 |
| `integration-duel` | **0** | 0 / 0 | 0 | 0 / 0 | 395 | 178 / 217 |
| `linear-equation-solver` | **0** | 0 / 0 | 0 | 0 / 0 | 620 | 199 / 421 |
| `log-laws` | **0** | 0 / 0 | 0 | 0 / 0 | 217 | 164 / 53 |
| `new-shapes` | **0** | 0 / 0 | 0 | 0 / 0 | 110 | 3 / 107 |
| `proportion-blaster` | **0** | 0 / 0 | 0 | 0 / 0 | 199 | 27 / 172 |
| `quadratic-factoriser` | **0** | 0 / 0 | 0 | 0 / 0 | 24 | 14 / 10 |
| `simultaneous-solver` | **0** | 0 / 0 | 0 | 0 / 0 | 160 | 113 / 47 |
| `surd-simplifier` | **0** | 0 / 0 | 0 | 0 / 0 | 370 | 212 / 158 |
| `suvat` | **0** | 0 / 0 | 0 | 0 / 0 | 5 | 5 / 0 |
| `truth-will-set-you-free` | **0** | 0 / 0 | 0 | 0 / 0 | 105 | 0 / 105 |
| `dimension-checker` | **0** | | 0 | | 0 (wrapper never called) | |
| `glorious-gantt` | **0** | | 0 | | 0 (wrapper never called) | |
| **Total, 51 files (50 live games + regression-rumble's withdrawn file)** | **386** | | **522** | | **9367** | |

## 5. Per game

Every game that calls KaTeX. "Wrappers" lists each function found by behaviour: its line, the
`displayMode` it passes (conditional = the caller decides), and whether it hands KaTeX the whole string
or splits prose from maths. Examples show the source string and what the student sees; where a
wrapper split the string first, what KaTeX received is shown too. Fields are named by their bank path
(`VARIABLE.field[]`), and grouped as prompt, option, step, hint or explanation.

**Second-count figures include its false positives (§7):** a two-letter product in maths reads as a
word to it. stat-attack's 2, regression-rumble's 2, higher-power's 1 and the `mg`, `bx`, `mc` examples
below are all this, not prose.

### `better-value`
- **Wrappers:** `K` :1392 (display mode, via `katex.renderToString`, whole string to KaTeX); `k` :1393 (inline mode, via `katex.renderToString`, whole string to KaTeX)
- **Strings KaTeX received:** 4 distinct (4 seen at runtime; 0 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**

### `binomial-blaster`
- **Wrappers:** `rk` :232 (conditional mode, via `katex.render`, whole string to KaTeX); `K` :250 (display mode, via `katex.renderToString`, whole string to KaTeX); `k` :251 (inline mode, via `katex.renderToString`, whole string to KaTeX)
- **Strings KaTeX received:** 346 distinct (111 seen at runtime; 235 from the bank fallback only; 0 of those are source literals).
- **B7 test: 13 lose prose spaces** (0 runtime, 13 bank fallback only). Fields: option. As rendered:
  - `Pascal rule` → `Pascalrule`
  - `Is undefined` → `Isundefined`
  - `Converges to 0` → `Convergesto0`
  - Bank paths: `QUESTIONS.d[]` 11, `QUESTIONS.correct` 2

### `boolean-blitz`
- **Wrappers:** `K` :327 (conditional mode, via `katex.renderToString`, whole string to KaTeX)
- **Strings KaTeX received:** 276 distinct (246 seen at runtime; 30 from the bank fallback only; 0 of those are source literals).
- **B7 test: 11 lose prose spaces** (0 runtime, 11 bank fallback only). Fields: step. As rendered:
  - `De Morgan's` → `DeMorgan′s`
  - `XOR Definition` → `XORDefinition`
  - `Double Negation` → `DoubleNegation`
  - Bank paths: `QUESTIONS.steps[][]` 11
- **Second count only (not B7): 2** (0 runtime, 2 bank fallback only). Fields: step. As rendered:
  - `Complement (×2)` → `Complement(×2)`
  - `Complement (×3)` → `Complement(×3)`

### `characteristic-quest`
- **Wrappers:** `rkI` :89 (conditional mode, via `katex.render`, whole string to KaTeX); `rk` :90 (display mode, via `katex.render`, whole string to KaTeX)
- **Strings KaTeX received:** 149 distinct (138 seen at runtime; 11 from the bank fallback only; 0 of those are source literals).
- **B7 test: 6 lose prose spaces** (4 runtime, 2 bank fallback only). Fields: step. As rendered:
  - `Repeated eigenvalue \lambda = 3 (scalar matrix)` → `Repeatedeigenvalueλ = 3(scalarmatrix)`
  - `Diagonal matrix: (5-\lambda)(2-\lambda) = \lambda^2 - 7\lambda + 10 = 0` → `Diagonalmatrix : (5 − λ)(2 − λ) = λ2 − 7λ + 10 = 0`
  - `Upper triangular: (2-\lambda)(1-\lambda) = \lambda^2 - 3\lambda + 2 = 0` → `Uppertriangular : (2 − λ)(1 − λ) = λ2 − 3λ + 2 = 0`
  - Bank paths: `QS.s[]` 6
- **Second count only (not B7): 1** (1 runtime, 0 bank fallback only). Fields: step. As rendered:
  - `Repeated \lambda = 4, but A \neq 4I` → `Repeatedλ = 4, butA ≠ 4I`

### `circle-theorem-spotter`
- **Wrappers:** `rk` :440 (conditional mode, via `katex.render`, whole string to KaTeX)
- **Strings KaTeX received:** 111 distinct (1 seen at runtime; 110 from the bank fallback only; 0 of those are source literals).
- **B7 test: 17 lose prose spaces** (0 runtime, 17 bank fallback only). Fields: option. As rendered:
  - `Cannot tell` → `Cannottell`
  - `Angle in semicircle` → `Angleinsemicircle`
  - `Cyclic quadrilateral` → `Cyclicquadrilateral`
  - Bank paths: `QUESTIONS.correct` 9, `QUESTIONS.d[]` 9
- **Second count only (not B7): 10** (0 runtime, 10 bank fallback only). Fields: option, other. As rendered:
  - `2 cm` → `2cm`
  - `3 cm` → `3cm`
  - `4 cm` → `4cm`

### `complex-converter`
- **Wrappers:** `K` :306 (conditional mode, via `katex.renderToString`, whole string to KaTeX)
- **Strings KaTeX received:** 288 distinct (235 seen at runtime; 53 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**

### `component-crusher`
- **Wrappers:** `K` :515 (conditional mode, via `katex.renderToString`, whole string to KaTeX); `PQ` :525 (inline mode, splits on `\( \)` via MaffsText)
- **Strings KaTeX received:** 56 distinct (9 seen at runtime; 47 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**
- **Second count only (not B7): 31** (3 runtime, 28 bank fallback only). Fields: prompt. As rendered:
  - `Find \|\mathbf{v}\|.` → `Find∣v∣.`
  - `Find \mathbf{a} + \mathbf{b}.` → `Finda + b.`
  - `Find \mathbf{a} \cdot \mathbf{b}.` → `Finda ⋅ b.`

### `curling-friction`
- **Wrappers:** `rk` :235 (conditional mode, via `katex.render`, whole string to KaTeX); `rkStr` :236 (conditional mode, via `katex.render`, whole string to KaTeX)
- **Strings KaTeX received:** 251 distinct (110 seen at runtime; 141 from the bank fallback only; 0 of those are source literals).
- **B7 test: 30 lose prose spaces** (0 runtime, 30 bank fallback only). Fields: option. As rendered:
  - `Both stop` → `Bothstop`
  - `Cannot tell` → `Cannottell`
  - `Applied force` → `Appliedforce`
  - Bank paths: `QUESTIONS.d[]` 23, `QUESTIONS.correct` 11
- **Second count only (not B7): 11** (1 runtime, 10 bank fallback only). Fields: option, prompt. As rendered:
  - `F = \mu mg` → `F = μmg`
  - `\mu mg` → `μmg`
  - `0.1 to 0.2` → `0.1to0.2`

### `differentiation-duel`
- **Wrappers:** `tex` :608 (conditional mode, via `katex.renderToString`, whole string to KaTeX)
- **Strings KaTeX received:** 437 distinct (183 seen at runtime; 254 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**
- **Second count only (not B7): 2** (2 runtime, 0 bank fallback only). Fields: prompt. As rendered:
  - `Find \dfrac{dy}{dx}` → `Finddxdy`
  - `\left(\frac{u}{v}\right)' = \frac{u'v - uv'}{v^2}` → `(vu)′ = v2u′v−uv′`

### `dimension-checker`
- **Wrappers:** `rkI` :101 (inline mode, via `katex.render`, whole string to KaTeX)
- **Strings rendered:** none. `rkI` is defined and never called.

### `distinctly-average`
- **Wrappers:** `tex` :291 (conditional mode, via `katex.renderToString`, whole string to KaTeX)
- **Strings KaTeX received:** 3 distinct (3 seen at runtime; 0 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**

### `eigenvalue-extractor`
- **Wrappers:** `rkI` :89 (conditional mode, via `katex.render`, whole string to KaTeX); `rk` :90 (display mode, via `katex.render`, whole string to KaTeX)
- **Strings KaTeX received:** 153 distinct (140 seen at runtime; 13 from the bank fallback only; 0 of those are source literals).
- **B7 test: 7 lose prose spaces** (5 runtime, 2 bank fallback only). Fields: option, step. As rendered:
  - `No eigenvalues exist` → `Noeigenvaluesexist`
  - `Both eigenvalues are negative` → `Botheigenvaluesarenegative`
  - `Repeated eigenvalue: \lambda = 3` → `Repeatedeigenvalue : λ = 3`
  - Bank paths: `QS.s[]` 6, `QS.d[]` 1

### `eigenvector-engine`
- **Wrappers:** `rkI` :90 (conditional mode, via `katex.render`, whole string to KaTeX); `rk` :91 (display mode, via `katex.render`, whole string to KaTeX)
- **Strings KaTeX received:** 94 distinct (87 seen at runtime; 7 from the bank fallback only; 0 of those are source literals).
- **B7 test: 1 loses prose spaces** (1 runtime, 0 bank fallback only). Fields: step. As rendered:
  - `Row 2: x + y = 0... but row 1: 4x + 2y = 0 \Rightarrow 2x + y = 0` → `Row2 : x + y = 0...butrow1 : 4x + 2y = 0 ⇒ 2x + y = 0`
  - Bank paths: `QS.s[]` 1
- **Second count only (not B7): 15** (14 runtime, 1 bank fallback only). Fields: step. As rendered:
  - `Row 1: x = y` → `Row1 : x = y`
  - `Row 1: y = 0` → `Row1 : y = 0`
  - `Row 1: x = 2y` → `Row1 : x = 2y`

### `equation-builder`
- **Wrappers:** `renderContent` :354 (conditional mode, via `katex.renderToString`, whole string to KaTeX)
- **Strings KaTeX received:** 33 distinct (0 seen at runtime; 33 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**
- **Second count only (not B7): 1** (0 runtime, 1 bank fallback only). Fields: other. As rendered:
  - `cos C` → `cosC`

### `expectation-station`
- **Wrappers:** `renderValue` :1187 (inline mode, via `katex.render`, whole string to KaTeX); `renderRat` :1204 (inline mode, via `katex.render`, whole string to KaTeX); `K` :1384 (display mode, via `katex.renderToString`, whole string to KaTeX); `k` :1385 (inline mode, via `katex.renderToString`, whole string to KaTeX); direct `katex.renderToString` :1247 in `pDisplayHTML`
- **Strings KaTeX received:** 16 distinct (16 seen at runtime; 0 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**

### `expected-damage`
- **Wrappers:** direct `katex.renderToString` :962 in `endSession`
- **Strings KaTeX received:** 1 distinct (1 seen at runtime; 0 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**

### `factor-theorem`
- **Wrappers:** `K` :251 (conditional mode, via `katex.renderToString`, whole string to KaTeX); `PQ` :261 (inline mode, splits on `\( \)` via MaffsText)
- **Strings KaTeX received:** 89 distinct (36 seen at runtime; 53 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**

### `force-resolver`
- **Wrappers:** `rk` :196 (conditional mode, via `katex.render`, whole string to KaTeX)
- **Strings KaTeX received:** 210 distinct (145 seen at runtime; 65 from the bank fallback only; 0 of those are source literals).
- **B7 test: 15 lose prose spaces** (0 runtime, 15 bank fallback only). Fields: option. As rendered:
  - `Free fall` → `Freefall`
  - `Cannot tell` → `Cannottell`
  - `Only if pushed` → `Onlyifpushed`
  - Bank paths: `QUESTIONS.d[]` 11, `QUESTIONS.correct` 4
- **Second count only (not B7): 3** (1 runtime, 2 bank fallback only). Fields: option, prompt. As rendered:
  - `F_{net} = F - \mu mg` → `Fnet = F − μmg`
  - `Yes — 49.7 N > 37.3 N` → `Yes—49.7N > 37.3N`
  - `F_{net} = mg\sin\theta - \mu mg\cos\theta` → `Fnet = mg sin θ − μmg cos θ`

### `formula-forge`
- **Wrappers:** `rk` :164 (display mode, via `katex.render`, whole string to KaTeX); `rkInline` :165 (conditional mode, via `katex.render`, whole string to KaTeX); `rkStr` :166 (conditional mode, via `katex.render`, whole string to KaTeX); direct `katex.render` :407 in `(anonymous callback)`
- **Strings KaTeX received:** 328 distinct (285 seen at runtime; 43 from the bank fallback only; 0 of those are source literals).
- **B7 test: 30 lose prose spaces** (0 runtime, 30 bank fallback only). Fields: hint. As rendered:
  - `st = d. Divide by s.` → `st = d.Dividebys.`
  - `Divide both sides by 4` → `Dividebothsidesby4`
  - `Divide both sides by b` → `Dividebothsidesbyb`
  - Bank paths: `Q.hint2` 30
- **Second count only (not B7): 4** (1 runtime, 3 bank fallback only). Fields: hint, prompt, step. As rendered:
  - `Q = mc\Delta T` → `Q = mcΔT`
  - `\dfrac{9C}{5} = F - 32. Add 32.` → `59C = F − 32.Add32.`
  - `\dfrac{P}{2} = l + w. Subtract l.` → `2P = l + w.Subtractl.`

### `formula-plug-in`
- **Wrappers:** `renderKatex` :383 (conditional mode, via `katex.renderToString`, whole string to KaTeX); direct `katex.renderToString` :556 in `(anonymous callback)`
- **Strings KaTeX received:** 103 distinct (3 seen at runtime; 100 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**

### `formula-unlocked`
- **Wrappers:** `rk` :164 (display mode, via `katex.render`, whole string to KaTeX); `rkInline` :165 (conditional mode, via `katex.render`, whole string to KaTeX)
- **Strings KaTeX received:** 272 distinct (246 seen at runtime; 26 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**
- **Second count only (not B7): 2** (2 runtime, 0 bank fallback only). Fields: option, prompt, step. As rendered:
  - `Q = mc\Delta T` → `Q = mcΔT`
  - `y = e^{a + bx}` → `y = ea+bx`

### `free-daily-pizza`
- **Wrappers:** `FDP.mathHtml` :814 (inline mode, splits on `\( \)` via MaffsText); direct `katex.renderToString` :820 in `FDP.optionHtml`; direct `katex.renderToString` :1124 in `(anonymous callback)`
- **Strings KaTeX received:** 64 distinct (64 seen at runtime; 0 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**

### `glorious-gantt`
- **Wrappers:** `k` :1243, local to `renderMethodRef` (inline mode, via `katex.renderToString`, whole string to KaTeX)
- **Strings rendered:** none. `k` is defined and never called; the method reference is plain HTML.

### `given-that`
- **Wrappers:** `kx` :435 (conditional mode, via `katex.renderToString`, whole string to KaTeX)
- **Strings KaTeX received:** 228 distinct (63 seen at runtime; 165 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**

### `gradient-hunter`
- **Wrappers:** `K` :1145 (display mode, via `katex.renderToString`, whole string to KaTeX); `k` :1146 (inline mode, via `katex.renderToString`, whole string to KaTeX)
- **Strings KaTeX received:** 7 distinct (7 seen at runtime; 0 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**

### `graph-sketcher`
- **Wrappers:** `K` :587 (conditional mode, via `katex.renderToString`, whole string to KaTeX); `k` :1137 (inline mode, via `katex.renderToString`, whole string to KaTeX)
- **Strings KaTeX received:** 55 distinct (16 seen at runtime; 39 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**

### `graph-transformer`
- **Wrappers:** `renderEq` :455 (conditional mode, via `katex.render`, whole string to KaTeX)
- **Strings KaTeX received:** 6 distinct (6 seen at runtime; 0 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**

### `growth-and-decay`
- **Wrappers:** `K` :598 (conditional mode, via `katex.renderToString`, whole string to KaTeX); `k` :869 (inline mode, via `katex.renderToString`, whole string to KaTeX)
- **Strings KaTeX received:** 88 distinct (19 seen at runtime; 69 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**

### `higher-power`
- **Wrappers:** `renderKatex` :374 (conditional mode, via `katex.render`, whole string to KaTeX); `katexStr` :375 (conditional mode, via `katex.renderToString`, whole string to KaTeX)
- **Strings KaTeX received:** 242 distinct (22 seen at runtime; 220 from the bank fallback only; 0 of those are source literals).
- **B7 test: 1, a false positive (§7):** the string renders correctly. As rendered:
  - `\text{Primes under 1{,}000}` → `Primes under 1,000`
  - Bank paths: `ALEVEL_CARDS.display` 1, `ALL_BANKS.display` 1
- **Second count only (not B7): 1** (0 runtime, 1 bank fallback only). Fields: prompt. As rendered:
  - `\int_0^{\infty} e^{-x^2} dx` → `∫0∞ e−x2dx`

### `index-laws`
- **Wrappers:** `tex` :580 (conditional mode, via `katex.renderToString`, whole string to KaTeX)
- **Strings KaTeX received:** 201 distinct (138 seen at runtime; 63 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**

### `integration-duel`
- **Wrappers:** `tex` :653 (conditional mode, via `katex.renderToString`, whole string to KaTeX)
- **Strings KaTeX received:** 395 distinct (178 seen at runtime; 217 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**

### `linear-equation-solver`
- **Wrappers:** `rk` :314 (inline mode, via `katex.renderToString`, whole string to KaTeX)
- **Strings KaTeX received:** 620 distinct (199 seen at runtime; 421 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**

### `log-laws`
- **Wrappers:** `K` :951 (conditional mode, via `katex.renderToString`, whole string to KaTeX); `MT` :1677 (inline mode, splits on `\( \)` via MaffsText); `addLine` :1778 (inline mode, passes its argument on to `K`); `setMsg` :1772 (inline mode, passes its argument on to `MT`)
- **Strings KaTeX received:** 217 distinct (164 seen at runtime; 53 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**

### `matrix-crunch`
- **Wrappers:** `rk` :239 (conditional mode, via `katex.render`, whole string to KaTeX); `rkStr` :240 (conditional mode, via `katex.render`, whole string to KaTeX)
- **Strings KaTeX received:** 283 distinct (68 seen at runtime; 215 from the bank fallback only; 0 of those are source literals).
- **B7 test: 32 lose prose spaces** (7 runtime, 25 bank fallback only). Fields: option, step. As rendered:
  - `This is the identity matrix I` → `ThisistheidentitymatrixI`
  - `The area is scaled by a factor of 10` → `Theareaisscaledbyafactorof10`
  - `All rotation matrices have determinant 1` → `Allrotationmatriceshavedeterminant1`
  - Bank paths: `QUESTIONS.steps[]` 26, `QUESTIONS.correct` 4, `QUESTIONS.d[]` 2
- **Second count only (not B7): 5** (1 runtime, 4 bank fallback only). Fields: step. As rendered:
  - `\det(I) = 1 always` → `det(I) = 1always`
  - `Row 2 = 2 × Row 1` → `Row2 = 2 × Row1`
  - `Singular — row 1 = 2 × row 2` → `Singular—row1 = 2 × row2`

### `moments-master`
- **Wrappers:** `rk` :191 (conditional mode, via `katex.render`, whole string to KaTeX)
- **Strings KaTeX received:** 219 distinct (134 seen at runtime; 85 from the bank fallback only; 0 of those are source literals).
- **B7 test: 43 lose prose spaces** (1 runtime, 42 bank fallback only). Fields: option. As rendered:
  - `No — net moment about midpoint \neq 0` → `No—netmomentaboutmidpoint ≠ 0`
  - `No effect` → `Noeffect`
  - `Cannot tell` → `Cannottell`
  - Bank paths: `QUESTIONS.d[]` 32, `QUESTIONS.correct` 11
- **Second count only (not B7): 4** (0 runtime, 4 bank fallback only). Fields: option. As rendered:
  - `Joule (J)` → `Joule(J)`
  - `Newton (N)` → `Newton(N)`
  - `Pascal (Pa)` → `Pascal(Pa)`

### `new-shapes`
- **Wrappers:** `renderKatex` :446 (conditional mode, via `katex.renderToString`, whole string to KaTeX); direct `katex.renderToString` :872 in `(anonymous callback)`
- **Strings KaTeX received:** 110 distinct (3 seen at runtime; 107 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**

### `partial-fractions-duel`
- **Wrappers:** `rk` :153 (conditional mode, via `katex.render`, whole string to KaTeX)
- **Strings KaTeX received:** 98 distinct (54 seen at runtime; 44 from the bank fallback only; 0 of those are source literals).
- **B7 test: 3 lose prose spaces** (0 runtime, 3 bank fallback only). Fields: option. As rendered:
  - `Cannot tell` → `Cannottell`
  - `Long division` → `Longdivision`
  - `Substitution or comparing coefficients` → `Substitutionorcomparingcoefficients`
  - Bank paths: `QUESTIONS.d[]` 2, `QUESTIONS.correct` 1

### `proof-builder`
- **Wrappers:** `rk` :195 (conditional mode, via `katex.render`, whole string to KaTeX); `rkd` :196 (display mode, via `katex.render`, whole string to KaTeX); `rkStr` :197 (inline mode, via `katex.render`, whole string to KaTeX); direct `katex.render` :407 in `(anonymous callback)`; direct `katex.render` :537 in `renderInduction`; direct `katex.render` :568 in `(anonymous callback)`
- **Strings KaTeX received:** 392 distinct (154 seen at runtime; 238 from the bank fallback only; 0 of those are source literals).
- **B7 test: 155 lose prose spaces** (66 runtime, 89 bank fallback only). Fields: option, prompt, step. As rendered:
  - `But 2 is even` → `But2iseven`
  - `These are not equal` → `Thesearenotequal`
  - `7 is divisible by 7 ✓` → `7isdivisibleby7✓`
  - Bank paths: `COUNTER.steps[]` 57, `SORTER.lines[]` 35, `COUNTER.s` with its quotes stripped at `:386` 25, `INDUCTION.stages[].prompt` 12, `INDUCTION.stages[].steps[]` 12, `SORTER.title` 8, `COUNTER.correct` 3, `COUNTER.d[]` 2, `COUNTER.prompt` 1
- **Second count only (not B7): 16** (10 runtime, 6 bank fallback only). Fields: option, step. As rendered:
  - `LHS = RHS ✓` → `LHS = RHS✓`
  - `But 25 = 5 \times 5` → `But25 = 5 × 5`
  - `x² + 1 = 0 gives x² = -1` → `x2 + 1 = 0givesx2 = −1`

### `proportion-blaster`
- **Wrappers:** `rk` :251 (conditional mode, via `katex.render`, whole string to KaTeX)
- **Strings KaTeX received:** 199 distinct (27 seen at runtime; 172 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**

### `quadratic-factoriser`
- **Wrappers:** `tex` :781 (conditional mode, via `katex.renderToString`, whole string to KaTeX); `mx` :787 (inline mode, splits on `\( \)` via MaffsText); `hfShowMisconception` :1344 (inline mode, passes its argument on to `mx`); `submitFormulaAnswer` :1695 (inline mode, passes its argument on to `mx`); `hfStep5Pick` :1499 (inline mode, passes its argument on to `hfShowMisconception`)
- **Strings KaTeX received:** 24 distinct (14 seen at runtime; 10 from the bank fallback only; 10 of those are source literals).
- **B7 test: 0.**

### `regression-rumble` (withdrawn)
- The live `index.html` is a `noindex` holding page with no KaTeX. The game, kept as `_withdrawn.html`, is not served to students and was not played; its figures are source literals only (its bank is not extracted while it is off the roster).
- **Wrappers (`_withdrawn.html`):** `kx` :315 (conditional mode, via `katex.renderToString`, whole string to KaTeX); `kxBlock` :316 (display mode, via `katex.renderToString`, whole string to KaTeX)
- **Strings KaTeX received:** 7 distinct (0 seen at runtime; 7 from the bank fallback only; 7 of those are source literals).
- **B7 test: 0.**
- **Second count only (not B7): 2** (0 runtime, 2 bank fallback only). Fields: source literal. As rendered:
  - `b = \frac{n\Sigma xy - \Sigma x \Sigma y}{n\Sigma x^2 - (\Sigma x)^2}` → `b = nΣx2 − (Σx)2nΣxy − ΣxΣy`
  - `r = \frac{n\Sigma xy - \Sigma x \Sigma y}{\sqrt{\left(n\Sigma x^2 - (\Sigma x)^2\right)\left(n\Sigma y^2 - (\S` → `r = (nΣx2 − (Σx)2) (nΣy2 − (Σy)2)nΣxy − ΣxΣy`

### `screening-room`
- **Wrappers:** `kRender` :465 (conditional mode, via `katex.renderToString`, whole string to KaTeX); `kRenderBlock` :469 (display mode, via `katex.renderToString`, whole string to KaTeX)
- **Strings KaTeX received:** 158 distinct (64 seen at runtime; 94 from the bank fallback only; 0 of those are source literals).
- **B7 test: 1 loses prose spaces** (0 runtime, 1 bank fallback only). Fields: explanation. As rendered:
  - `After Test 1: ~1043 positives (48 true, 995 false). Test 2: 48×0.98≈47 true + 995×0.03≈30 false = 77. P ≈ 47/7` → `AfterTest1 : 1043positives(48true, 995false).Test2 : 48 × 0.98 ≈ 47true + 995 × 0.03 ≈ 30false = 77.P ≈ 47/77 `
  - Bank paths: `QUESTIONS.bayesWorking` 1
- **Second count only (not B7): 1** (1 runtime, 0 bank fallback only). Fields: explanation. As rendered:
  - `After A+: P_1 = \dfrac{0.9 \times 0.02}{0.9 \times 0.02 + 0.15 \times 0.98} = 0.109. After B+: P_2 = \dfrac{0.` → `AfterA+ : P1 = 0.9 × 0.02 + 0.15 × 0.980.9 × 0.02 = 0.109.AfterB+ : P2 = 0.95 × 0.109 + 0.10 × 0.8910.95 × 0.1`

### `sequence-solver`
- **Wrappers:** `rk` :302 (conditional mode, via `katex.render`, whole string to KaTeX)
- **Strings KaTeX received:** 393 distinct (41 seen at runtime; 352 from the bank fallback only; 0 of those are source literals).
- **B7 test: 13 lose prose spaces** (0 runtime, 13 bank fallback only). Fields: option. As rendered:
  - `Powers of 2` → `Powersof2`
  - `Cube numbers` → `Cubenumbers`
  - `Only if r > 0` → `Onlyifr > 0`
  - Bank paths: `QUESTIONS.d[]` 11, `QUESTIONS.correct` 3
- **Second count only (not B7): 9** (0 runtime, 9 bank fallback only). Fields: option. As rendered:
  - `Yes (n = 6)` → `Yes(n = 6)`
  - `Yes (n = 7)` → `Yes(n = 7)`
  - `Yes (n = 8)` → `Yes(n = 8)`

### `simultaneous-solver`
- **Wrappers:** `renderKaTeX` :268 (conditional mode, via `katex.render`, whole string to KaTeX)
- **Strings KaTeX received:** 160 distinct (113 seen at runtime; 47 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**

### `standard-form-blitz`
- **Wrappers:** `rk` :226 (conditional mode, via `katex.render`, whole string to KaTeX)
- **Strings KaTeX received:** 434 distinct (203 seen at runtime; 231 from the bank fallback only; 0 of those are source literals).
- **B7 test: 5 lose prose spaces** (0 runtime, 5 bank fallback only). Fields: option. As rendered:
  - `All equal` → `Allequal`
  - `All three` → `Allthree`
  - `Cannot tell` → `Cannottell`
  - Bank paths: `QUESTIONS.d[]` 5

### `stat-attack`
- **Wrappers:** `K` :761 (conditional mode, via `katex.renderToString`, whole string to KaTeX); `k` :1345 (inline mode, via `katex.renderToString`, whole string to KaTeX)
- **Strings KaTeX received:** 44 distinct (6 seen at runtime; 38 from the bank fallback only; 2 of those are source literals).
- **B7 test: 0.**
- **Second count only (not B7): 2** (0 runtime, 2 bank fallback only). Fields: source literal. As rendered:
  - `\text{Mean} = \frac{\Sigma fx}{\Sigma f}` → `Mean = ΣfΣfx`
  - `\sigma^2 = \frac{\Sigma fx^2}{\Sigma f} - \left(\frac{\Sigma fx}{\Sigma f}\right)^2` → `σ2 = ΣfΣfx2 − (ΣfΣfx)2`

### `surd-simplifier`
- **Wrappers:** `rk` :255 (conditional mode, via `katex.render`, whole string to KaTeX)
- **Strings KaTeX received:** 370 distinct (212 seen at runtime; 158 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**

### `suvat`
- **Wrappers:** `eqHTML` :552 (conditional mode, via `katex.renderToString`, whole string to KaTeX); `setEq` :561 (inline mode, passes its argument on to `eqHTML`)
- **Strings KaTeX received:** 5 distinct (5 seen at runtime; 0 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**

### `test-the-claim`
- **Wrappers:** `K` :1196 (conditional mode, via `katex.renderToString`, whole string to KaTeX); `PQ` :1206 (inline mode, splits on `\( \)` via MaffsText)
- **Strings KaTeX received:** 747 distinct (32 seen at runtime; 715 from the bank fallback only; 2 of those are source literals).
- **B7 test: 1 loses prose spaces** (1 runtime, 0 bank fallback only). Fields: explanation. As rendered:
  - `Upper: P(X \geq 11) = 0.0028 < 0.005. x = 9 does not reach CR.` → `Upper : P(X ≥ 11) = 0.0028 < 0.005.x = 9doesnotreachCR.`
  - Bank paths: `QUESTIONS.crExplanation` 1
- **Second count only (not B7): 14** (14 runtime, 0 bank fallback only). Fields: explanation. As rendered:
  - `P(X \geq 5) = 0.0527 < 0.10 and P(X \geq 4) = 0.1429 > 0.10` → `P(X ≥ 5) = 0.0527 < 0.10andP(X ≥ 4) = 0.1429 > 0.10`
  - `P(X \geq 7) = 0.0335 < 0.05 and P(X \geq 6) = 0.0839 > 0.05` → `P(X ≥ 7) = 0.0335 < 0.05andP(X ≥ 6) = 0.0839 > 0.05`
  - `P(X \geq 9) = 0.0409 < 0.10 and P(X \geq 8) = 0.1018 > 0.10` → `P(X ≥ 9) = 0.0409 < 0.10andP(X ≥ 8) = 0.1018 > 0.10`

### `trig-identity-duel`
- **Wrappers:** `rk` :250 (conditional mode, via `katex.render`, whole string to KaTeX)
- **Strings KaTeX received:** 276 distinct (99 seen at runtime; 177 from the bank fallback only; 0 of those are source literals).
- **B7 test: 2 lose prose spaces** (0 runtime, 2 bank fallback only). Fields: option. As rendered:
  - `Cannot tell` → `Cannottell`
  - `Only if C = 90°` → `OnlyifC = 90°`
  - Bank paths: `QUESTIONS.d[]` 2
- **Second count only (not B7): 1** (0 runtime, 1 bank fallback only). Fields: option. As rendered:
  - `Exactly 90°` → `Exactly90°`

### `truth-will-set-you-free`
- **Wrappers:** `K` :267 (conditional mode, via `katex.renderToString`, whole string to KaTeX)
- **Strings KaTeX received:** 105 distinct (0 seen at runtime; 105 from the bank fallback only; 0 of those are source literals).
- **B7 test: 0.**


### Games with no KaTeX call: 47 on the roster

- **Load KaTeX and never call it (14):** `coordinate-geometry-dash`, `core-maths-paper1`, `core-maths-paper2a`, `core-maths-paper2b`, `core-maths-paper2c`, `normal-navigator`, `probability-paradox`, `spot-the-error`, `spot-the-muppet`, `terrible-advice`, `truth-buster`, `unit-converter`, `word-problem-decoder`, `wrong-on-the-internet`. Their text never reaches KaTeX, so nothing in them
  can lose spaces this way. (canon §7.1.1's audit counted the same class as "loads KaTeX but never
  calls it".)
- **No KaTeX at all (33):** `52dle`, `angle-ace`, `bearing-blitz`, `chart-interrogator`, `constructions-lab`, `correlation-or-coincidence`, `decimal-detective`, `equatle`, `estimation-engine`, `estimation-golf`, `factor-race`, `fermi-lab`, `four-quadrant-explorer`, `fraction-equivalence`, `like-terms-collector`, `maths-court`, `modular-battle`, `negative-number-line`, `percentage-flip`, `prime-factorisation`, `prime-or-composite`, `prisoners-dilemma`, `probability-pioneer`, `regression-rumble`, `scale-factor-scaling`, `seven-bridges`, `shape-shifter`, `six-sevens-bruv`, `split-it`, `tax-theft`, `think-of-a-number`, `trig-wars`, `trig-worms`. (`regression-rumble` is here for its live holding page; its
  withdrawn file is covered above.)
- `the-perfect-prank` (unlisted prototype, not on the roster) and the escape rooms load no KaTeX.

Roster: 97 games = 50 that call KaTeX + 14 that load it only + 33 without it.

## 6. B7 today, and what it would take to see the rest

**What B7's KaTeX half sees today.** `bank_common.katex_field_names()` reads field names off the
regex `K(x.field)` / `katex.renderToString(x.field)` and renders every bank value of those fields. It
finds fields in 9 games:

| Game | Fields B7 renders |
|---|---|
| `boolean-blitz` | `expr` |
| `complex-converter` | `cartLatex`, `expLatex`, `givenLatex`, `latex`, `polarLatex` |
| `factor-theorem` | `working` |
| `free-daily-pizza` | `tex` |
| `graph-sketcher` | `eqLatex` |
| `growth-and-decay` | `hint`, `modelLatex` |
| `log-laws` | `eg`, `exp`, `tex` |
| `test-the-claim` | `zFormula` |
| `truth-will-set-you-free` | `simplified` |

None of the 386 strings in §4 is in one of these fields. B7 sees no field at all in the other 41
games that call KaTeX, including all 19 affected ones. component-crusher's `K()` branch inside `PQ`
is invisible to both halves: the KaTeX half because the call is `K(s)`, the MaffsText half because
those strings carry no `\( \)`.

**What B7 would need, in order of what it buys (no code was changed):**
1. **Find render sites by behaviour, not by name.** The data-flow rule in §2 found every wrapper
   this audit used, with no per-game list, from the same esprima tree `extract-banks.py` already
   parses. Names would have missed `rkStr`, `kx`, `renderKaTeX`, `FDP.mathHtml` and any wrapper
   written tomorrow.
2. **Resolve each call site to the bank values that reach it, as the site builds them.** A field
   name is not enough. `rkStr(st)` inside `q.steps.forEach(st => …)` needs the iteration followed;
   `currentQ.hint2||currentQ.hint1` and `K(hint)` (a local holding a ternary with a prose prefix) need
   the expression evaluated per question. Rendering a field blind over-counts (this audit's first
   pass counted formula-forge's `hint1`, which is plain HTML unless `hint2` is missing: 69 became 30).
3. **Render through the game's own wrapper in the page,** not through `katex.renderToString` with
   default options, so that a wrapper which splits, gates (`equation-builder`'s `renderContent` only
   calls KaTeX when the text looks like LaTeX) or wraps its input is measured as it behaves.
4. **Decide the prose test (§7).** As written it cannot see a single word between maths, which is
   most of test-the-claim's and all of component-crusher's defects.
5. A runtime KaTeX hook, as used here, is the cross-check rather than the gate. Tier 3 reached
   4,104 of 9,367 strings: it never presses a hint button, cannot drive 50 of 163 runs, and takes
   only menu entry 0. Static resolution reaches the whole bank deterministically, as B7 already does
   for the fields it knows.

The fix for the defects themselves is the §1.10 one, at the shared layer: prose and maths separated
by `\( \)` and rendered through `MaffsText`. This audit sizes that work. §5 lists every string.

## 7. B7's prose test on these strings (reported, not changed)

- **It undercounts: one word between maths is never prose to it.** 137 strings are flagged by the
  second count and not by B7. A random sample of 20 (seed 20261002), read by hand:

| # | Game | Source | As rendered | Verdict |
|---:|---|---|---|---|
| 1 | `component-crusher` | `Find \|\overrightarrow{AB}\| to 2 d.p.` | `Find∣AB∣to2d.p.` | genuine |
| 2 | `component-crusher` | `Find \|\mathbf{b}\|.` | `Find∣b∣.` | genuine |
| 3 | `proof-builder` | `A square` | `Asquare` | genuine |
| 4 | `proof-builder` | `Then 2 = \frac{a^2}{b^2}, so a^2 = 2b^2` | `Then2 = b2a2, soa2 = 2b2` | genuine |
| 5 | `moments-master` | `Newton-metre (Nm)` | `Newton − metre(Nm)` | genuine; the hyphen also renders as a minus |
| 6 | `component-crusher` | `Find \mathbf{m} + \mathbf{n}.` | `Findm + n.` | genuine |
| 7 | `test-the-claim` | `P(X \geq 7) = 0.0335 < 0.05 and P(X \geq 6) = 0.0839 > 0.05` | `P(X ≥ 7) = 0.0335 < 0.05andP(X ≥ 6) = 0.0839 > 0.05` | genuine |
| 8 | `formula-unlocked` | `y = e^{a + bx}` | `y = ea+bx` | false positive: `bx` is a product in maths |
| 9 | `eigenvector-engine` | `Row 1: x = y` | `Row1 : x = y` | genuine |
| 10 | `test-the-claim` | `Lower: P(X \leq 10) = 0.0139 < 0.025. Upper: P(X \geq 19) = 0.0243 < 0` | `Lower : P(X ≤ 10) = 0.0139 < 0.025.Upper : P(X ≥ 19) = 0.0243 < 0.025` | genuine |
| 11 | `eigenvector-engine` | `Row 1: x = 2y` | `Row1 : x = 2y` | genuine |
| 12 | `circle-theorem-spotter` | `13 cm` | `13cm` | genuine, a unit not prose (`13cm`, italic) |
| 13 | `sequence-solver` | `Yes (n = 21)` | `Yes(n = 21)` | genuine |
| 14 | `curling-friction` | `F = \mu mg` | `F = μmg` | false positive: `mg` is a product in maths |
| 15 | `force-resolver` | `F_{net} = F - \mu mg` | `Fnet = F − μmg` | false positive: `mg` is a product in maths |
| 16 | `proof-builder` | `But \pi/4 \times \pi/4 = \pi^2/16 \neq \pi/2` | `Butπ/4 × π/4 = π2/16 ≠ π/2` | genuine |
| 17 | `test-the-claim` | `P(X \leq 2) = 0.0355 < 0.05 and P(X \leq 3) = 0.1071 > 0.05` | `P(X ≤ 2) = 0.0355 < 0.05andP(X ≤ 3) = 0.1071 > 0.05` | genuine |
| 18 | `component-crusher` | `Find \mathbf{a} - 2\mathbf{b}.` | `Finda − 2b.` | genuine |
| 19 | `test-the-claim` | `P(X \leq 1) = 0.0404 < 0.10 and P(X \leq 2) = 0.1247 > 0.10` | `P(X ≤ 1) = 0.0404 < 0.10andP(X ≤ 2) = 0.1247 > 0.10` | genuine |
| 20 | `component-crusher` | `Find \overrightarrow{AC}.` | `FindAC.` | genuine |

  **17 of 20 are real defects (16 prose, 1 unit), 3 are false positives.** All three are two-letter
  products in maths (`bx`, `mg`) that B7's word definition counts as words. So the second count is a
  better size for the fix than B7's, at roughly 15% noise on the strings only it flags. What it still
  misses, by its definition: a space lost next to punctuation rather than a word (test-the-claim's
  `Expected: …` keeps a gap only because KaTeX spaces the colon as a relation).
- **One false positive: higher-power `\text{Primes under 1{,}000}`.** It renders correctly
  ("Primes under 1,000"), but `_KATEX_TEXT_MODE_WRAP` (`\\(?:text|mathrm|operatorname)\{[^{}]*\}`) cannot match a `\text{}`
  with braces inside it, so the words are not stripped and B7's test flags the string. It is the only
  string B7 flags and the second count does not.

## 8. Coverage and limits

- **Every figure says where it came from** (§4, §5): runtime, or bank fallback only. 9,367 distinct
  strings, 4,104 seen at runtime. For 12 of the 19 B7-affected games, every affected string came from
  the fallback, mostly hints, worked steps and options a tier 3 run did not reach (§6 item 5).
- **Generators are runtime-only.** log-laws' Solve mode, quadratic-factoriser, distinctly-average,
  expectation-station and the parts of free-daily-pizza built at the call site cannot be rebuilt
  from a bank. Their figures are what play reached, and none showed a defect. Three of them (log-laws,
  quadratic-factoriser, free-daily-pizza) render their mixed text through `MaffsText`.
- **No game was left unclassified.** Two wrappers are dead code (dimension-checker, glorious-gantt).
- **Display mode** was taken from the call (display flag passed or not); it does not change either
  count.

## 9. Rerunning it

**The scripts now live in `scripts/audit-katex/`** (committed 2 Oct 2026, with a README giving run order and the sandbox recipe; not in CI).

Scripts lived in the session scratchpad, not the repo, by the contract's terms. In order:
`find_wrappers.py` (wrappers by data flow; output `wrappers.json`), `site_fields.py` (call site →
bank fields or literal), `kx_hook.js` (the init-script KaTeX hook), `run_t3_capture.py` (imports
`check-site.py` and runs tier 3 unchanged, with the hook, the sandbox network recipe and an optional
menu entry), `fallback.py` with `site_eval.py` (per-question rebuild of each site's argument, rendered
through the game's own wrapper), `analyse.py` (stack → wrapper, B7's test), `spacecount.py` +
`rerender.js` (the second count), `gen_tables.py`. If B7 is rebuilt along §6's lines, these are the
prototype; ask for them to be committed under `scripts/` as part of that contract.
