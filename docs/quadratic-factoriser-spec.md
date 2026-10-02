# Quadratic Factoriser rebuild spec

Item 0 of the quadratic-factoriser rebuild contract (docs/next-contract-quadratic-factoriser.md).
This file records that contract's design before any code was written, plus the rulings made
during the build on a contradiction the contract itself contained (Section 2). Section 1 is
the contract text, unedited, exactly as dictated by Jon on 27 Sep 2026.

## 1. The contract, verbatim

Status: READY, not started. Dictated by Jon 27 Sep 2026, verbatim below. Context will be
cleared before this build starts; this file is the full brief, not a summary.

TASK: Rebuild quadratic-factoriser into three levels: factorise a=1, factorise a>1 with a
fading AC-method tutorial, and solve with the quadratic formula, as the first game whose
questions are machine-verified.

ROOT CAUSE: The live game covers a=1 only (10 questions, level hard-coded gcse at lines 711,
756, 768). GCSE needs a>1 factorising (split the middle term) and the quadratic formula, and
neither exists on the site as a game. Jon teaches the AC method: a times c is the product, b
is the sum; split bx; factorise in pairs; take out the common bracket.

CLASS CHECK: Not a bug class, a rebuild of one game. But it is built to the proposed new-game
standard so it can prove it: finite enumerated pools (no rejection sampling), shared helpers
(MaffsSession, MaffsNext, MaffsText), and its own layer C/D verification script.

EXACT CHANGE:

0. docs/quadratic-factoriser-spec.md, this contract design, verbatim, before any code.

1. Structure. Same slug, same file. Three levels selectable on the start screen and by the
   level query parameter: gcse = factorise a=1 (keeps the existing leaderboard/PB key and
   analytics history); higher = factorise a>1; formula = quadratic formula. Every mfg() event
   and submitScore() uses the real level (fixes the hard-coded gcse). Session lengths via
   MaffsSession; wrong answers via MaffsNext with the worked solution shown first (canon
   section 7.6); every string mixing prose and maths via MaffsText; all maths in KaTeX. Dark
   GCSE+ theme (canon section 7.5.1, lowest tier served is GCSE). Aa toggle kept.

2. Pools, enumerated once at load, deduplicated, shuffled, sliced. No draw-and-retry loop.
   gcse (a=1): (x+p)(x+q), p and q each range across plus or minus 1 to 9, b not equal to
     zero except in the difference-of-two-squares stage (x squared minus k squared, k from
     1 to 12). Stages, in order: both positive, then one negative, then both negative, then
     the difference-of-two-squares stage. Answer: the existing bracket picker; accept either
     bracket order.
   higher (a>1): (px+q)(rx+s), p and r each range across 1 to 6 with their product at least
     2 and at most 12, q and s each range across plus or minus 1 to 9, the greatest common
     divisor of p and q is 1 and likewise for r and s (no hidden common factor), b not equal
     to zero, the magnitude of a times c is at most 72. A later stage only: k times
     (px+q)(rx+s), k from 2 to 5, where the student must take out k first.
     Answer: coefficient pickers for the two brackets, plus an outer-factor picker in the
     take-out-the-common-factor stage. Mark by expanding the student's brackets and comparing
     a, b and c, never by string, so bracket order does not matter. Display the answer with
     positive leading coefficients.
   formula: a x squared + b x + c = 0, a from 1 to 5, b and c each plus or minus 1 to 9.
     Mostly non-square discriminants; about 15 percent negative discriminant, answered with a
     No real solutions button. Exclude any item with a root within 1e-6 of a 2 decimal place
     rounding boundary, filtered out of the pool rather than retried. Answer: two inputs, any
     order; a root is correct only if the input equals the root rounded to 2 decimal places
     (so 1.2378 accepts 1.24, not 1.23).

3. The higher tutorial: Tutorial, then Guided, then Independent, fading per CLAUDE.md
   "Scaffolds fade". Tutorial walks one worked example with the student doing each step:
     1 identify a, b and c;  2 work out a times c;
     3 pick the pair from a factor-pair table of the magnitude of a times c, with signs,
       that multiplies to a times c and adds to b. A named misconception fires if the pair
       multiplies to c instead of a times c;
     4 split the middle term: rewrite as a x squared + m x + n x + c (either order of m and
       n accepted, and the game says so);
     5 factorise each pair. A named misconception fires when the second pair's bracket does
       not match the first because a negative factor was not taken out ("the two brackets
       must be identical, check the sign of the number you took out");
     6 take out the common bracket.
   Guided repeats the same six steps, with prompts but no worked example. Independent gives
   answer-only entry, with the steps available behind a Show me the method control that does
   not count as a fail. The game moves from Guided to Independent after two correct answers
   in a row, and back after two wrong answers in a row.

4. formula feedback: on a wrong root, if it equals one of these named shapes, name it before
   showing the working: used plus b instead of minus b; divided only the square root by 2a;
   divided by a instead of 2a; took b squared as negative when b is negative. Otherwise show
   the full substitution.

5. scripts/verify-quadratic-factoriser.py (layers C and D, run in CI): enumerate every pool
   exactly as the game does, using the same parameters, exported from the game as a
   JSON-able config rather than duplicated by hand, and assert with SymPy: every factorised
   form expands to its quadratic; no higher non-HCF item has a common factor; every higher
   item has exactly one unordered pair m, n with the product equal to a times c and the sum
   equal to b; every formula root matches SymPy's own root to 1e-9; negative-discriminant
   items are flagged as such; no item sits on a rounding boundary; every pool has at least 40
   items per stage. Fail CI on any violation.

6. Roster, portal card and meta description: the levels become GCSE (a=1), GCSE Higher
   (a>1), and Quadratic formula; the description is rewritten to match. The check ledger
   (data/check-ledger.json) is refreshed by check-banks.

Commit after each phase and run the full checks before each commit. Phase 1 is items 0, 1 and
gcse. Phase 2 is higher with the tutorial. Phase 3 is formula. Item 5 grows with each phase;
item 6 lands in phase 3.

Things this build must never touch: any other game; the shared helpers (use them as they are;
if one is missing a capability the build should halt rather than fork it); the Firebase
leaderboard script; the existing gcse leaderboard key; other portal cards.

What counts as done, per phase: verify-quadratic-factoriser.py passes; every level plays
through to completion at every offered session length, scripted against the stub server; the
higher tutorial steps through a full worked example and each named misconception fires on its
trigger, scripted; site checker tiers 1 and 2 are green; tier 3 run with only this game comes
back PASS or UNSUPPORTED; check-banks run in CI mode is green; the phase is pushed; a live
check against the deployed site passes. The report for each phase should include screenshots
of: each level's first question, every tutorial step, one misconception message, and one
formula worked solution.

Conditions that halt the build rather than being worked around: a shared helper missing a
capability the game needs; any pool falling below 40 items at any stage under these
constraints, in which case the count is reported and the constraint is not loosened; the
existing gcse PB or leaderboard key changing; any checker failure.

## 2. Rulings made during the build

### 2.1 First blocker raised, and its ruling (superseded by 2.2)

Before any code was written, the four gcse stage pools were enumerated exactly as item 2
specifies, and counted:

| Stage | Enumeration | Count |
|---|---|---|
| both positive | p, q each 1 to 9, unordered | 45 |
| one negative | one of p, q from 1 to 9, the other from minus 1 to minus 9, b not zero | 72 |
| both negative | p, q each minus 1 to minus 9, unordered | 45 |
| difference of two squares | x squared minus k squared, k from 1 to 12; this is its entire population, there is no other free parameter | 12 |

Item 5 calls for at least 40 items per stage, and the difference-of-two-squares count of 12
is that stage's full, exhaustive population under the contract's own fixed parameter (k from
1 to 12); it cannot be enlarged without changing that parameter. This was raised as the
contract's own halt condition (a pool below 40 at some stage; report the count, do not loosen
the constraint) before any file was written.

Jon's first ruling on this, since superseded and kept here only for the record: drop the
40-item floor for the difference-of-two-squares stage alone, keep k from 1 to 12 exactly as
written, and treat that stage as a deliberate small special case. Every other stage keeps the
40-item floor.

### 2.2 Corrected ruling, the one actually built to

On reflection this was a drafting error in the contract rather than a deliberate per-stage
rule; the platform's real floor (canon: 40 to 50 questions per game per tier) is per level,
not per stage. The corrected rule, and the one this build implements, is:

- Per level (gcse, higher, formula): the level's total pool, summed across all its stages,
  must be at least 40. This is easily satisfied everywhere: gcse totals 45 + 72 + 45 + 12,
  which is 174.
- Per stage: no 40-item assertion at all. Instead, the property the 40-item idea was actually
  protecting, that a single session never has to repeat a question, is asserted directly. How
  this game samples its questions decides what that check means. Every level's pool is built
  as one combined array, all of its stages concatenated and deduplicated by the question's
  own a, b and c, the same platform pattern the better-value game already uses (shuffle the
  pool, then slice to the requested length), rather than a fixed quota drawn from each stage.
  Under that design a session cannot repeat a question, of any stage, at any offered length up
  to the size of the whole pool, because a deduplicated set sliced without replacement can
  never yield the same item twice, whatever a single stage's own size happens to be. The
  verification script therefore asserts the thing that actually guarantees no repeats, that
  the level's combined pool contains no duplicate a, b, c triple, rather than a per-stage
  floor that would be either redundant for the three large gcse stages or impossible to
  satisfy by construction for the difference-of-two-squares stage, which only has 12 possible
  values to begin with.
- The difference-of-two-squares stage stays at exactly 12 items (k from 1 to 12) by design,
  its full and exhaustive population. No exemption language is needed for it any longer,
  because it is no longer being measured against a per-stage floor: the no-repeat guarantee
  above holds for it exactly as it holds for every other stage, regardless of its size. A
  session can draw at most 12 such questions ever, because only 12 exist, not because of any
  special-cased limit.

Stage sizes were also computed ahead of the higher build, for forward reference in Phase 2:
the base stage (p, r each 1 to 6 with product between 2 and 12, q, s each plus or minus 1 to
9, coprime within each bracket, b not zero, magnitude of a times c at most 72, deduplicated on
swapping the two brackets) comes to 752 distinct quadratics; the take-out-the-common-factor
stage (k from 2 to 5 multiplied across the base pairs) comes to 3008. Both clear every floor
comfortably under either reading of the rule, so the higher level was never at risk from this
issue.
