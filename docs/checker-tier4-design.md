# Checker tier 4 — five layers, designed by Project Claude, 26 Sep 2026

## Why tier 4 exists

Tiers 1–3 prove a page loads, doesn't hang, and can be played through. None of them
inspects the *question data itself*. The defects that made tier 4 necessary were all
sitting in plain sight in bank source, all found only because Jon played the games:

- a duplicate option (`matrix-crunch:171`, `formula-unlocked:298` via `correct_override`)
- draft prose shipped as the answer ("...actually let me recalculate",
  `scale-factor-scaling:162`)
- a self-correcting answer key inside the same object literal
- prose passed whole through KaTeX, losing every space
  (`component-crusher`'s "Whatisthereversetranslation?")
- three hand-written `QUESTIONS[n] =` patches overwriting the wrong entries
  (`normal-navigator`)
- a level's bank below the 40–50 question floor the platform commits to
- a session-length button offering more questions than the bank can fill

Every one of these is a **class**, not a one-off — the same shape can recur in any of
the 94 games, so the fix belongs at the platform layer (one extractor, one lint pass),
not as 94 separate audits.

## The five layers

Each layer needs strictly more machinery than the one before it, and each is honest
about what it *can't* see — the point of naming five rather than building one big
checker is that "no violations found" should mean something different, and something
narrower, at layer A than a human reader might assume.

### Layer A — static bank lint (BUILT, this phase)

**What it needs:** the live-extracted bank (`data/banks/*.json`) plus one static AST
pass over each game's source.

**What it catches:** structural and data defects that don't require understanding the
maths at all — missing/empty answer keys, duplicate options, duplicate questions,
banks below the content-depth minimum, session lengths exceeding the bank, draft
prose leaking into shipped content, a rendering hazard where KaTeX swallows spaces
out of prose, duplicate object keys, hand-written index patches, and `correct_override`
usage. Ten rules, B1–B10, documented in `scripts/check-banks.py`.

**What it cannot catch, structurally:** anything where the *stored* value is
syntactically fine but semantically wrong — a correct answer that is simply the wrong
number, a distractor that happens to also be mathematically valid, a generator whose
formula can produce an impossible instance. Layer A has no model of the mathematics;
it only has a model of the *data shape*.

**A concrete boundary, found while building this layer:** 16 of the 84 real banks
(word-problem-decoder, chart-interrogator, regression-rumble, fermi-lab, and others)
carry no field this layer recognises as an answer key at all, because their
correctness is *computed* at grading time (a topic-name match, a recomputed
prediction against a tolerance, a rebuilt truth table) rather than stored. For these,
B1/B2/B5 correctly find nothing to check — that is not a gap in the extractor, it is
exactly the boundary layer C exists to close.

### Layer B — cross-question consistency (NOT BUILT)

**What it would need:** the same extracted bank, but compared against itself
relationally rather than question-by-question — e.g. a distractor in one question
that is the *correct* answer to a different, adjacent question (which can leak the
answer to an attentive student); a unit or rounding convention that changes silently
partway through a bank; two scenarios in the same level sharing enough surface
structure that a student can pattern-match the answer without doing the maths.

**What it would catch that A can't:** defects that are only visible when questions are
read *together*, not one at a time.

**What it still couldn't catch:** whether any individual answer is correct.

### Layer C — computed-answer verification (NOT BUILT)

**What it would need:** a small re-implementation, per question *shape* (not per
game), of the arithmetic the game itself performs — recompute a determinant from a
stored matrix and assert it equals `correct`; recompute a z-score from `mu`/`sigma`;
recompute an expected value from stored outcomes and probabilities.

**What it would catch that A can't:** Circle Theorem Spotter's Q48 (a question with no
correct solution, where the marked answer encodes the misconception the game exists to
correct) and the historical `es_gcse_005` (an unwinnable scenario whose product,
displayed as 0.375 → "0.38", was checked against a 4dp value with a tolerance that
excluded the true answer by exactly 0.005). Both had a clean layer-A read: nothing was
missing, duplicated, or malformed. The number was just wrong.

**What it still couldn't catch:** whether the *pedagogy* is wrong — a question that is
arithmetically self-consistent but teaches the wrong idea, or is worded ambiguously.

### Layer D — generator range-proving (NOT BUILT)

**What it would need:** for every *procedural* game (the 10 layer A found nothing
static to read, plus any game layer A already reads statically but whose distractors
are computed), a symbolic or exhaustively-sampled sweep of the generator's parameter
space, checking every output stays inside whatever domain the question type requires.

**What it would catch that A/C can't:** Trig Worms' `5*Math.floor(Math.random()*17)+15`
angle range (15–95°), which includes 90° and 95° — neither of which can be the
non-right angle of a right-angled triangle, and at 95° the adjacent side goes negative.
That bug shipped for months; tier 1 never reached it because every *individual* load
was fine, and layer A has nothing to read (there is no static bank). Modular Battle's
`generateChoices` rejection-sampling freeze on a modulus below 4 is the same shape:
correct for most of the parameter space, silently broken at its edges.

**What it still couldn't catch:** a generator whose entire *domain* is wrong on
purpose (a scale drawn to look right but derived from the wrong formula throughout).

### Layer E — rendered-output fidelity (NOT BUILT)

**What it would need:** a live browser, driving the game, comparing what actually
appears on screen (a drawn curve, a dot grid, a chart) against the value the game
grades against.

**What it would catch that nothing above can:** Modular Battle's dot grid, which
capped its drawing at 40 dots and scaled counts down — so `46 mod 7` drew **3** red
dots for an answer of **4**, and 3 was one of the four options. And Chart
Interrogator's cumulative-frequency reading: the key is computed by straight-line
interpolation between class boundaries, but the chart is *drawn* as a Bezier curve, so
a student reading correctly off the curve on screen is marked wrong against a value
the curve was never drawn to produce. Both defects are invisible to every layer above
this one — the stored data and the computed answer can each be internally consistent
and the *picture* still lies.

**What it still couldn't catch:** wording and pedagogy, same as every layer above it.

## What no layer in this design can catch — by construction

Two classes of defect are explicitly out of scope for A–E, and stay Jon's call:

- **Wording** — Chart Interrogator's histogram Phase 2 rejecting a true statement
  ("this is the most common range") because the key only ever checks one class
  interval's share; Circle Theorem Spotter's Q48 needing new numbers chosen by
  someone who can judge what a GCSE student should see. A checker can flag that an
  answer is inconsistent; it cannot judge whether a sentence reads ambiguously to a
  15-year-old.
- **Pedagogy** — whether a distractor teaches the *right* misconception, whether a
  scenario is age-appropriate, whether a "spot the deliberate error" game's in-character
  wrong reasoning (terrible-advice, wrong-on-the-internet) is convincing without being
  confusing. This is design judgement, not a checkable invariant.

## The proposed new-game gate (awaiting Jon's ruling)

**Proposal:** once layer A is trusted (a few weeks of clean CI runs with no
ledger-integrity failures), block merging a *new* game until it passes layer A —
i.e. `extract-banks.py` finds a static bank (or the game is declared a generator) and
`check-banks.py` reports zero unrecorded violations. Layers B–E stay advisory until
built; this phase only proposes gating on what actually exists today.

**Why this scope and not "every game must pass layer A retroactively":** the ledger
already carries every current violation — matrix-crunch's dropped duplicate,
formula-unlocked's `correct_override` collision, factor-theorem's `display:true` steps
(not a defect, see below), component-crusher's 37 KaTeX-collapsed prompts (3 games,
79 hits total, once B7's KaTeX half was correctly redefined on 27 Sep around prose —
two or more adjacent real words surviving after LaTeX commands are stripped — rather
than the general-string half's letter-run threshold or a naive "lost a space" test,
either of which mis-sized this by an order of magnitude in opposite directions). Gating
retroactively would either force fixing all of them under this phase's DO NOT TOUCH,
or need a second, weaker "existing games are grandfathered" rule that the ledger
mechanism already provides more honestly.

**What the gate would NOT catch:** anything from layers B–E, and everything under
"what no layer can catch" above. A green layer-A gate is a floor, the same way tier 1
green is a floor — it proves the new game's data is *shaped* correctly, not that it is
*correct*.

This is a proposal, not a decision — Jon's ruling on whether to enable it, and on the
timeline, is open.

## Implementation notes (for whoever touches this next)

- **Ledger ids are content, never position (to-do item 7, PR 52, 2 Oct 2026).**
  `diff_against_ledger()` matches on id alone, so an id built from a bank index or a source
  line turns any edit above a known defect into one "new" and one "stale" entry. That happened
  on 28 Sep, when an unrelated edit moved `test-the-claim`'s B8 entry from line 527 to 526. The
  ids, by rule:

  | Rule | Id |
  |---|---|
  | B1 B2 B6 B7 B10 | `<content_id>::<rule>[.<sub-answer>]` |
  | B3 | `<slug>::B3::<every copy's content hash, sorted, joined by +>` |
  | B4 B5 | `<slug>::<level>` |
  | B7 KaTeX half | `<slug>::B7::katex[<path>]::<sha12 of the string>#1` (path: the bank field, `literal`, `page`, or `<VARIABLE>(state)`) |
  | B7 MaffsText half | `<slug>::B7::mathtext[balance or throws]::<sha12 of the string>#<ordinal>` |
  | B8 | `<slug>::B8::<enclosing name>::<duplicate keys>::<sha12 of the object's text>` |
  | B9 | `<slug>::B9::<target as written>::<sha12 of the right-hand side>` |
  | B11 | `<content_id>::B11::<the pair>` |

  `content_id()` (`bank_common`) is the SHA-1 of the whole question's canonical JSON plus an
  ordinal over exact copies, numbered over `dedup_groups()` in bank order.
  - **B3** names the whole group of copies (every question in the level with the same normalised
    signature), because a name taken from the later copy alone flips when the copies swap. A group
    of three or more copies has one name; its findings differ in detail.
  - **B7's KaTeX and MaffsText halves** carry no question. The KaTeX half is one entry per distinct
    (bank path, string) that loses a space in any render, so its ordinal is always 1; the MaffsText
    half's ordinal separates identical strings.
  - **B8's enclosing name** is the innermost named function, then the top-level variable, then
    `(top level)` (`bank_common.enclosing_name()`).
  - **B8 and B9 hash the parser's text**, `bank_common._shim_for_parser(src)`, because the AST's
    ranges index into that text, not the raw source. The rewrites change no line, so `line`
    stays true.

  Ids change, by design, when the content changes: any edit to a question's fields, a comment
  added inside a B8 object, renaming the function or variable a B8 object sits in, or changing
  either parser rewrite, which renames every B8/B9 finding at once. Each shows in CI as one new
  and one stale entry, to be re-recorded.
- **A ledger write is a merge, never a rebuild (to-do §4 item 10, PR 53, 2 Oct 2026).**
  `merge_ledger()` replaces only the games this run linted (and true generators already recorded
  as such); every other game keeps its record byte for byte, reported with a reason:
  withdrawn/off-roster, not selected by `--only`, bank missing, bank not read. Rebuilding from
  the run alone had three failure triggers sharing one shape, "not read" treated as clean or as
  gone: a withdrawn game's entries vanished (regression-rumble's, copied back by hand twice),
  `--only` wrote a one-game ledger, and a bank that did not extract was written as "pass". The
  write refuses (exit 1, nothing written) when a bank the ledger knows as read came back missing
  or as a generator. A game new to the ledger that did not read is not written, so a new true
  generator is added deliberately rather than by a run that cannot tell it from a failed read.

- **Extraction is live, not static, on purpose.** `extract-banks.py` reads each
  candidate bank variable back from the page under Playwright, after the game's own
  init code has run — this is what makes normal-navigator's now-fixed index patches
  visible as the *final* served state, matching what B9's separate AST pass on the raw
  source flags as the anti-pattern regardless of whether today's numbers are right.
- **Bank variable candidates are SCREAMING_SNAKE_CASE only.** Checked directly: every
  real bank across all 94 games is named this way (`QUESTIONS`, `BANK`, `YEAR6_BANK`,
  `QUESTION_LIBRARY`, ...); runtime session state is always lowerCamelCase (`pool`,
  `currentQ`, `roundQuestions`). Without this filter, estimation-golf's `roundQuestions`
  (a live copy of its own source bank, populated by page load) registered as a second
  "bank" and every one of its questions flagged as a B3 duplicate of itself.
- **B7's KaTeX half, rebuilt 2 Oct 2026 (to-do §1.31).** Until then it found KaTeX inputs
  with a regex on two call shapes, `K(x.field)` and `katex.renderToString(x.field)`, and tested
  each value for two adjacent prose words. 50 games render through 84 wrappers under other
  names, so it never saw their strings; and a single word between maths (`0.05 and P(X ≤ 1)`,
  `Find \mathbf{a}`) was never prose to it (`docs/audit-katex-wrappers.md`). It now works in
  four steps, all in `bank_common` and `extract-banks.py`, with no per-game list anywhere:
  1. **Render sites, by behaviour** (`katex_wrappers`, `katex_render_sites`). A function is a
     wrapper when a parameter, or a local derived from it, reaches the first argument of
     `katex.render`/`katex.renderToString`/`MaffsText.html`, directly or through another
     wrapper, to a fixed point. Every call of one is a site; a wrapper's own call on its
     parameter is its body.
  2. **What reaches each site, per question** (`resolve_render_site`). Locals, both branches of
     a ternary, `||`/`&&`, templates, `+`, iteration callbacks, `.map` with an inline callback,
     `.push` and element writes, source tables, and functions that only select or reorder
     (`shuffle`, `makeChoices`, `MaffsOptions.build`). **Guards are evaluated per string**: in
     `if (v.includes('\\')) rk(b, v); else b.textContent = v` a plain option never reaches
     KaTeX and is never a hit (Jon's ruling, 2 Oct). A guard that cannot be decided keeps both
     ways open. A game function applied to bank data becomes a page expression: pure ones
     (`ratTex(q.pr)`, `fmt(q.sumFx2)`) are called as they stand; ones that read game state
     (`exactEX()` reads `completedTable`) are called after the page is put in the state the
     question puts the game in, each state variable set from the game's own assignment of it.
     A site fed by nothing that can carry bank data (log-laws' Solve families, the generators)
     is **runtime-only**; anything else that cannot be rebuilt is **unresolved**. Both are listed
     by `--ci`, never failures, and no site is ever silently empty.
  3. **Rendered in the page** (`extract-banks.py`, `SITE_RENDER_JS`), through the site's own
     callee: the wrapper by name, or reproduced from its one renderer call when an IIFE hides it
     (given-that's `kx`, log-laws' `MT`/`setMsg`). The visual text is `.katex-html` (the hidden
     `.katex-mathml` keeps the source's spaces and would mask the defect), each positive-width
     `.mspace` read as a space, zero-width spaces dropped. A wrapper that gates its input
     (`curling-friction`'s `rkStr`, `equation-builder`'s `renderContent`) is measured as it
     behaves.
  4. **The test** (`katex_lost_word_spaces`): a hit when a space the source has between two
     tokens is missing from what the student sees and one of the tokens is a word, 3+ letters or
     a 2-letter English function word (to of is as or an in on at by if so no be do up it we he me
     my us am). Two-letter maths products (mg, bx, mc) are not words; units ("13 cm") are out of
     scope. `\text{}`/`\mathrm{}`/`\operatorname{}` are stripped with braces nested two deep
     (higher-power's `\text{Primes under 1{,}000}` was the old regex's false positive); a word
     joined to a brace group (`ABC\overline{D}`) is measured from its free side.
  First run: **277 strings in 12 games**, every one of them flagged by the audit's second count;
  the audit's other 246 are 217 guarded (shown as plain text), 13 two-letter products and 16
  other (13 boolean-blitz law names the audit read from `steps` but the game shows as plain
  text, higher-power's `\text{}`, regression-rumble's withdrawn file). A hand-read of 30 random
  hits found 30 genuine. `RULE_MAX` is 800 for B7 alone. Fixtures: `check-banks.py --selftest`
  (each site found, resolved and tested against a recorded KaTeX 0.16.9 render) and
  `--selftest-live` (the same rendered in a real page, the recording checked). The superseded
  regex helpers (`katex_field_names`, `katex_prose_hazard`) stay in `bank_common` only because
  `scripts/audit-katex/` imports them.
- **B3's "duplicate question" needs real scenario text, not a shared instruction
  label.** Comparing on a question's prompt field alone found 699 "duplicates" that
  were two different matrices sharing the fixed label "Find the determinant". B3
  requires prose ≥30 characters (a real scenario, not a label) *and* a matching
  correct answer before it calls two questions the same.
- **`correct_override` wins over `correct` when both are present** — matches the
  games' own runtime (`currentQ.correct_override||currentQ.correct`). Resolving the
  wrong one hid formula-unlocked:296's known duplicate entirely on the first pass.
- **A step object with `display:true` is shown, not answered, by design**
  (factor-theorem's `scaffoldSteps`) — its empty `answer` is correct, not missing.
