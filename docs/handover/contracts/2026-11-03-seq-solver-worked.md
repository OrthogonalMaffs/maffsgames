# SEQ-SOLVER-WORKED (received 3 Nov 2026, cloud lane, Claude Code)

Saved verbatim on receipt (canon §7.8.2, CONTRACTS-FOLDER). Jon, 3 Nov: "This one next, although context may become an
issue before you get to this." Starts after SEQ-SOLVER-FIXES merges; DASHBOARD-METRICS starts after this merges.

## Contract (verbatim)

CONTRACT: SEQ-SOLVER-WORKED
Tier: Shared · Lane: cloud · Implementer: Claude Code (cloud)

START
After SEQ-SOLVER-FIXES merges.

TASK
Show a short worked solution when a student answers a Sequence Solver question wrongly, for every question in all
three banks, with every worked solution checked by script.

ROOT CAUSE
A wrong answer shows only which option was right, with no working (SEQ-SOLVER-REREAD, #647). On a steep bank a
struggling student meets several in a row and leaves: since 28 Sep only 6 of 46 started games finished, most
abandoned after about 2 questions. Jon, 3 Nov 2026: "a worked solution on a wrong answer is really important".

CLASS CHECK
The missing worked solution is common across the library, but the fix here is content for one game. Use the game's
existing wrong-answer path (MaffsNext.wrong, canon §7.6) and the house pattern for worked steps that other games
use (canon's worked-explanation rules); do not build a new shared component in this contract. Report how many other
listed games lack a wrong-answer explanation, for Jon, without changing them.

EXACT CHANGE
1. Each question in QUESTIONS (ks3, gcse, alevel, as left by SEQ-SOLVER-FIXES) gains a `worked` field: 1 to 3 short
   steps at the level's language (KS3 plain words; KaTeX for expressions per canon §7.1.1), ending in the keyed
   answer. No dash before a number (canon §7.1).
2. On a wrong answer the worked solution shows under the options, after the right option is marked, before Next
   (MaffsNext.wrong unchanged). A right answer is unchanged.
3. verify-sequence-solver.py: every question has a worked solution; its last step states the keyed answer; every
   number it states that comes from the sequence is recomputed from the question's own terms where the question
   gives terms (common difference, ratio, nth term value at the stated n); plants: a missing worked field, a final
   step contradicting the key, a wrong difference; each CAUGHT.
4. Phone fit: the worked solution and Next fit at 320x568, 375x667, 390x844 per the fold rules, or the panel
   scrolls only as the rules allow.

DO NOT TOUCH
Questions, options and keys; marking; MaffsNext and other shared assets; other games; Gate files.

SUCCESS CONDITION
All questions carry a checked worked solution; shown on a wrong answer before Next; verifier and plants pass; phone
fit passes; a sample of ten worked solutions (three per level plus one) quoted in the PR for review; Gate green;
Shared review by Project Claude; stop for Jon's "merge"; Record line.

STOP IF
A question's worked solution would need a method beyond its level (list it); the fold rules cannot be met with the
worked solution shown; a fix would need a change to MaffsNext or another shared file.
