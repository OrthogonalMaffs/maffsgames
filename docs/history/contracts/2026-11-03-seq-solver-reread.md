# SEQ-SOLVER-REREAD (received 3 Nov 2026, cloud lane, Claude Code)

Saved verbatim on receipt (canon §7.8.2, CONTRACTS-FOLDER).

## Contract (verbatim)

CONTRACT: SEQ-SOLVER-REREAD
Tier: Shared · Lane: cloud · Implementer: Claude Code (cloud)

TASK
Re-read every question in Sequence Solver's three banks and confirm each one can be answered correctly by a student
at its level; fix what cannot, and report the rest for Jon.

ROOT CAUSE
Sequence Solver is consistently the hardest game on the Sheet in both logging eras (GCSE 46–51%, KS3 60–65%, A-level
52–61%, site 78%); since 28 Sep only 6 of 46 started games finished, most abandoned after about 2 questions. Questions
are shuffled and the Sheet records only the round position, so the data cannot say which questions cause it. Its 4
Oct resit audit found and fixed a HIGH (0.999... = 1, #117). Low accuracy may be honest difficulty or questions that
cannot be answered as keyed: the re-read decides which (Jon, 3 Nov 2026).

CLASS CHECK
Not yet known. Per question it is local; if one shape recurs (for example "next term" with more than one valid rule,
or notation beyond the level), report it as a class and stop for Jon before fixing it game-wide.

EXACT CHANGE
1. Read every question in games/sequence-solver/index.html QUESTIONS (ks3, gcse, alevel) as a student at that level
   would see it, rendered. For each, check: the keyed answer is correct; it is the only correct option (no
   value-equal or equally valid distractor, including a different valid rule for the same terms); the question gives
   enough information to reach it; the notation and vocabulary are within the level (canon's level rules); the
   options render and read cleanly at 375x667.
2. Record every finding in docs/audits/findings/sequence-solver.yml in the register's schema, with level and the
   question text. Anything SR-30 covers (CRITICAL with a standing ruling deciding the fix) is fixed in this PR, text
   only, with verify-sequence-solver.py passing and extended to catch it.
3. Report in the PR, per level: questions read, findings by severity, and a short judgement: is the level hard but
   fair, or is something making it unanswerable?

DO NOT TOUCH
Questions with no finding; the game's layout, timer, scoring and marking code; other games; Gate files.

SUCCESS CONDITION
All three banks read (counts in the PR); findings in the register; SR-30 fixes made with a verifier case each; Gate
green; Shared review by Project Claude; stop for Jon's "merge"; Record line.

STOP IF
A finding needs a new convention or a change to what a question asks (list it for Jon); a class of problem recurs
across many questions; a fix would change the game's marking code.
