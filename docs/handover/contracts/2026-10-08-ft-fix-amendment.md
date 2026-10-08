# Contract FT-FIX: amendment, and the order of work (verbatim)

From Project Claude, pasted by Jon, 8 Oct 2026, 21:30 (Part A, cloud lane, of that paste; Part B is the home lane's and
is not copied here). Amends `2026-10-08-ft-fix.md`; read the two together when FT-FIX starts. Moves to `docs/history/`
with that contract when FT-FIX merges.

```text
ANSWER to your FT-FIX step 3 question, and the order of work:

1. You are right. wrapExamVocab is in schools/assets/exam-vocab.js (line 109), not in the game, so it is shared code and off limits to you. My contract wrongly called it "the game's own helper". The fix belongs at the shared layer, so it goes to the home lane (Part B, VOCAB-IDEMPOTENT). Amend FT-FIX as follows, and save this amendment beside the contract in docs/handover/contracts/:
   * Drop EXACT CHANGE step 3 (t5-008).
   * Drop the verifier check "wrapExamVocab(wrapExamVocab(x)) == wrapExamVocab(x)" from step 7.
   * Leave t5-008 open (home lane's).
   * Remove t5-008 from step 8's list of findings to close. Everything else in FT-FIX stands.
2. ORDER: UC-FIX next (Jon attaches cloud-contract-uc-fix-2026-10-08.md; Unit Converter is listed and live, priority 1), then FT-FIX as amended.
3. Unit Converter t4-005 (score depends on answer speed): UC-FIX leaves it open. Jon's ruling will come as its own note. Do not change the timer or the scoring in UC-FIX.
```
