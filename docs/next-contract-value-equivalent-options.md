Status: **Contract 1 DONE: B11 built, PR 51 (2 Oct 2026). Contract 2 DONE, PR 54 (2 Oct 2026), on standard-form-blitz, surd-simplifier and sequence-solver.** Its scope was redrafted by Project Claude on 2 Oct (afternoon). proof-builder (its step 3) was split out by Jon's ruling, because its induction prompts render through KaTeX maths mode and lose their spaces (to-do §1.30), so new wording there would be unreadable until that is fixed; its 2 group B pairs stay in the ledger. Originally **DRAFT, not issued.** Drafted by Code Claude on 28 Sep 2026 at Jon's instruction ("your
decisions for all 5 are good"), after the `coordinate-geometry-dash:233` contract's STOP IF fired.
Nothing here starts until Jon issues it. The evidence is `docs/scan-value-equivalent-options.md`.

The work is two contracts. The architectural one comes first, because it stops new cases while the
existing ones are fixed. Group A's 32 content fixes are not drafted: each needs Jon's replacement
distractor, as `:233`'s "50" did, so they go in per-game batches once he has chosen.

---

## Contract 1: a checker rule for options equal in value (B11)

**Status: DONE, PR 51 (2 Oct 2026).** Built as re-issued that day (whole-question `content_id`, the
corrected `\text{}` rule, Jon's group C rulings). The record is the "B11 built, 2 Oct 2026" section
of `docs/scan-value-equivalent-options.md`.

TASK: Make CI fail when a question bank offers two options that are different strings but equal in
value, so that the √50/5√2 shape cannot ship again.

ROOT CAUSE: Every existing guard compares options as strings. `MaffsOptions.build()` de-duplicates on
`String(value)` by design (canon §7.1), and `check-banks.py` B2 does the same. Two options with the
same value in different forms are therefore invisible to all of them. The 28 Sep scan found 229 such
pairs in 21 games; 32 offer the marked answer twice where the question asks for no particular form.

CLASS CHECK: Yes, a class. Group A alone spans 10 games, and the gap sits in shared infrastructure,
the checker every bank passes through. So the fix is a rule at the checker layer, not per-item
patches. `options.js` keeps string semantics: marking compares `dataset.val` strings, so
de-duplicating by value there would change marking, which is a different decision.

EXACT CHANGE:
1. Move `parse_value()` and `equal()` from `scripts/scan-value-equivalent-options.py` into
   `scripts/bank_common.py`, so there is one copy. The scan script imports them.
2. In `scripts/check-banks.py`, add rule B11, "options equal in value". It runs over the same answer
   units as B2, compares distinct strings only, and identifies a finding by game, question content
   and the pair, never by line number (to-do item 7).
3. Fix the three false-positive shapes the report lists, and add each as an unequal fixture: en-dash
   class intervals ("20–40"); `\text{}` units that carry meaning ("clockwise", "anticlockwise"); and
   e^{jθ} phasors.
4. Add the scan's 32 fixtures, plus step 3's, to `check-banks.py --selftest`.
5. Record the deliberate form questions (group C, 103 pairs) in `scripts/checker-allowlist.json`
   under a new key. Each entry is keyed on game plus question identity, with a written reason. B11
   skips listed entries. Review them per question, not per game.
6. Record groups A, B and D as tracked violations with `check-banks.py --write-ledger`, so CI fails
   only on a new pair.
7. Add one paragraph naming B11 to canon §7.1, and one to CLAUDE.md's "Tier 4, layer A" section.

DO NOT TOUCH: any game file; `schools/assets/options.js` and its string semantics; the behaviour of
B1–B10; `scripts/extract-banks.py`; the CI workflow (SymPy is already installed at
`.github/workflows/check-site.yml:49`).

SUCCESS CONDITION:
- `check-banks.py --selftest` passes every fixture.
- `check-banks.py --ci` is green on `main`: the ledger holds every current A, B and D pair, and the
  allowlist covers every C pair.
- Restoring `√50` at `coordinate-geometry-dash:233` fails `--ci` with B11, then passes once reverted
  (regression-proven the way B6 and B9 were).
- On a fresh extraction, B11's count matches the report's genuine pairs (229, less the 10 false
  positives), with none of the false positives reported.
- CI is green on the push.

STOP IF:
- B11 reports a pair the scan did not find, other than from content changed since 28 Sep.
- Moving `parse_value()`/`equal()` changes any B1–B10 result.
- Any group C entry turns out, on reading, not to ask for the form it tests (a teaching call).
- B11 adds more than 60 seconds to the CI job.

---

## Contract 2: say which form is wanted (group B, 53 pairs)

**Needs redraft by Project Claude: scope grew on 2 Oct (15 more group B pairs on 11 questions, incl. a key flip at surd-simplifier alevel[16] and two proof-builder induction stages; plus the sequence-solver alevel[23] group A fix).**

**DONE, PR 54, 2 Oct 2026, from Project Claude's redraft of 2 Oct (afternoon), with Jon's rulings:** the two 0.9̇ questions ask "Write in its simplest form"; the three cross-level copies matched x2 by design; proof-builder split out (see the status line). The record is the "Contract 2 applied, 2 Oct 2026" section of `docs/scan-value-equivalent-options.md`. The draft below is kept as it was.

TASK: State the required form in every question whose options include the right value in another
form, in `standard-form-blitz` and `surd-simplifier`.

ROOT CAUSE: 53 questions offer the marked answer in a second form but never say which form is
wanted, so a student who picks the right value is marked wrong.
- `standard-form-blitz` "Calculate" questions offer 30 × 10⁶ beside the key 3 × 10⁷.
- `surd-simplifier` "Convert to a fraction" questions offer 3/9 beside the key 1/3.

CLASS CHECK: Yes within two games. It is one shape: an `ask` line that omits the form the options
test. The fix is at the `ask` for every question of that shape, not at the options. The options stay
as they are: once the form is stated, they become the deliberate form-distractors of group C.

EXACT CHANGE: patch each entry in place, never by index (CLAUDE.md, "patch the entry, not an index"):
- `standard-form-blitz`: every `ask: "Calculate"` becomes "Calculate. Give your answer in standard
  form.", and "Estimate to 1 s.f." becomes "Estimate to 1 s.f., in standard form."
- `surd-simplifier`: every `ask: "Convert to a fraction"` becomes "Convert to a fraction in its
  simplest form.", and `alevel[45]`'s "Expand" (offering 9 − 5 beside 4) becomes "Expand and
  simplify."
- Jon to confirm the wording before it is applied.

DO NOT TOUCH: any option or key; any other game; the checker (Contract 1).

SUCCESS CONDITION:
- Every one of the 53 pairs in report section B sits on a question whose `ask` names the form.
- With Contract 1 built, all 53 move from the ledger to the reviewed group C list.
- Tiers 1+2 green in CI; `check-banks.py --ci` green; tier 3 on both games no worse than before, run
  from home.

STOP IF: a new `ask` would change what the question tests; or on some question, the "wrong-form"
option is arguably the better answer.
