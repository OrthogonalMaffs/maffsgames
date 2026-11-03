# QUESTION-ID (received 3 Nov 2026, cloud lane, Claude Code)

Saved verbatim on receipt (canon §7.8.2, CONTRACTS-FOLDER). Jon: "this then queues behind the reread contract"
(SEQ-SOLVER-REREAD). Saved here so a fresh session has it; work starts on its own branch after SEQ-SOLVER-REREAD.

## Contract (verbatim)

CONTRACT: QUESTION-ID
Tier: Shared · Lane: cloud · Implementer: Claude Code (cloud)

TASK
Record which question was asked on every question_answered event, as an anonymous question ID, starting with Sequence
Solver, so that "hardest questions" can name real questions instead of round positions.

ROOT CAUSE
question_answered carries question_index, the position in a shuffled round, not the question. The dashboard's
"Hardest Questions" table therefore ranks round positions, and no game's difficult questions can be found from the data
(Sequence Solver, 3 Nov 2026). The privacy page already states the purpose ("which questions students find difficult");
Jon approved the field on 3 Nov 2026.

CLASS CHECK
Yes: every game sends question_answered its own way. Fix once in the shared layer (schools/assets/analytics.js and
the Apps Script endpoint), then migrate games warn-first (canon §7.8.4); Sequence Solver is the first.

EXACT CHANGE
1. schools/assets/analytics.js: question_answered accepts either question_id (the game's own stable id, at most 40
   characters) or question_text (the prompt as shown); given text, it sends question_id = "h" + an 8-hex-digit FNV-1a
   hash of the normalised text and never sends the text itself. Selftest cases for both and for neither (field absent,
   behaviour unchanged).
2. docs/apps-script-endpoint.js: append question_id as the last column (after seq), bump SCRIPT_VERSION, and add the
   step to its deploy notes. Jon deploys it and adds the column header; until then the field is simply not stored.
3. GA4: send question_id as an event parameter; note in canon §1 that Jon registers it as a custom dimension.
4. games/sequence-solver/index.html: pass question_text with each question_answered. New
   scripts/decode-question-ids.py <slug>: prints id -> question for a game with static banks (Sequence Solver first).
5. New scripts/check-question-id.py (ci-line, warn-first, shrink-only warn list of every other game).
6. Privacy page: one line under what is collected: "Which question was asked, as an anonymous code. Nothing a student
   types is ever sent." Canon §1 field table and §12 reason line.

DO NOT TOUCH
Any field a student types (answers, initials) — never sent as question_text; other games' calls; GA4 and Sheet
settings (Jon's); the existing columns' order; Gate files.

SUCCESS CONDITION
Sequence Solver's events carry question_id (verified in Chromium with the stub endpoint); decode script maps every
Sequence Solver id to its question with no collisions; analytics selftest and check-question-id selftest pass; privacy
line live; Gate green; Shared review by Project Claude; stop for Jon's "merge"; handover lists Jon's two steps
(redeploy Apps Script with the new column; register the GA4 custom dimension); Record line.

STOP IF
Any game sends student-typed text where question_text would go; the hash collides within one game's banks; the
endpoint change would alter existing columns; the privacy page wording needs more than the one line.
