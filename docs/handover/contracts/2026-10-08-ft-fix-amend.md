# Amendment to FT-FIX, and the order of work (verbatim)

From Project Claude, pasted by Jon, 8 Oct 2026, 21:30: the paste's header and Part A (the cloud lane's). Part B is the home lane's
(VOCAB-IDEMPOTENT, CONTRACTS-FOLDER) and is not copied here. Saved verbatim under Jon's standing rule
(corrected 20:00): read this file when the item starts, not at session start; it moves to `docs/history/` when the work
merges.

```text
PASTES, Project Claude, 8 Oct 2026, 21:30. Part A is for the cloud lane; Part B is for
the home lane. Each lane saves its contracts verbatim under
docs/handover/contracts/ (not in its handover file).

######################################################################
PART A: CLOUD LANE
######################################################################

ANSWER to your FT-FIX step 3 question, and the order of work:

1. You are right. wrapExamVocab is in schools/assets/exam-vocab.js
   (line 109), not in the game, so it is shared code and off limits to
   you. My contract wrongly called it "the game's own helper". The fix
   belongs at the shared layer, so it goes to the home lane (Part B,
   VOCAB-IDEMPOTENT). Amend FT-FIX as follows, and save this amendment
   beside the contract in docs/handover/contracts/:
   - Drop EXACT CHANGE step 3 (t5-008).
   - Drop the verifier check "wrapExamVocab(wrapExamVocab(x)) ==
     wrapExamVocab(x)" from step 7.
   - Leave t5-008 open (home lane's).
   - Remove t5-008 from step 8's list of findings to close.
   Everything else in FT-FIX stands.

2. ORDER: UC-FIX next (Jon attaches cloud-contract-uc-fix-2026-10-08.md;
   Unit Converter is listed and live, priority 1), then FT-FIX as
   amended.

3. Unit Converter t4-005 (score depends on answer speed): UC-FIX leaves
   it open. Jon's ruling will come as its own note. Do not change the
   timer or the scoring in UC-FIX.
```
