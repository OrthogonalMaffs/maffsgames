CONTRACT: COLLISION-IDENTITIES (Jon, 20 Oct 2026; name given by the cloud lane, the contract has none). CLOUD LANE. Saved verbatim.

TASK: Reclassify key-collision survey cases where the "error" is a valid identity for that question's parameters, and re-report the coincidence counts.
ROOT CAUSE: scripts/survey-key-collisions.py labels an error "coincidence" whenever it is a different calculation from the key, without testing whether it equals the key for EVERY question sharing that parameter. Structural identities (a mod 2 and a mod 5 = last digit of a mod b; b - r = r when b = 2; first decimal digit of a/9 = a mod 9; 1-d.p. ratio rounding that cannot change the nearest whole degree) are counted as coincidences. modular-battle's 231 and trig-worms' 128 are inflated, and filtering on them would remove legitimate questions.
CLASS CHECK: Yes, a bug class. The fault is in the shared classifier, which every game's count passes through. Fix the classification rule in the script, not per game and not by editing error lists to hide cases.
EXACT CHANGE: In scripts/survey-key-collisions.py, after counting collisions per (game, part, error), group the questions by the parameters the error depends on (e.g. b for modular-battle). If the error equals the key on every question in a group, reclassify those cases as "agree (identity)" and name the parameter value. Add self-test fixtures: 11 mod 2 / b - r -> agree; 13 mod 5 / last digit -> agree; 12 mod 9 / first decimal digit -> agree; 12 mod 5 / quotient -> coincidence; Just Pythag control still 0. Re-run on main and rewrite docs/audits/key-collision-survey-2026-10.md with before/after counts per game and the remaining genuine coincidences listed per game, with one example each.
DO NOT TOUCH: any game, verifier, shared module, findings file, register or workflow; CI wiring (the script stays out of CI); the methods-agree and two-way sections, apart from adding the reclassified cases.
SUCCESS CONDITION: The self-test passes; the report shows corrected coincidence counts for all 14 games, with the reclassified cases identified; the control still reports 0; handover updated with the PR and main run.
STOP IF: a reclassified group would hide a case where the identity does NOT hold for some question in it; any game's genuine coincidence count rises; the corrected total for any listed game is still above 20. If so, list them and stop for a ruling.

---

Rulings (Jon, 20 Oct), verbatim:

COLLISION-IDENTITIES:
(1) Assumption 1 accepted: count an error only where its value is a residue the game offers.
(2) Assumption 2 not accepted as stated. Classify by error type, not by grouping. “Ratio rounded before the inverse” is “agree (precision)” in every case, grouped or not, including the 9 at TOA 65°: it is a precision slip, and where it changes the degree the student is already marked wrong. Wrong-function and upside-down errors that give the key are coincidences even where they hold across a whole group at the nearest degree. That restores the 30 upside-down cases (CAH 80° and 85°).
(3) modular-battle: accept all 123. Record why: 123 across 4 errors × 408 questions is 7.5% per error per question, below the 1-in-9 floor at which a random residue hits the key, so no method beats guessing; filtering 30% of the questions would teach that b/2 is never the answer.
(4) trig-worms: filter, under TRIG-WORMS-FILTER.
Finish the report with these classes, merge it, then return to TRIG-WORMS-FILTER.
