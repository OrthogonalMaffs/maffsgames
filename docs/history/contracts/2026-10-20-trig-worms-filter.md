# TRIG-WORMS-FILTER (Jon, 20 Oct 2026), verbatim, with Jon's amendments of the same day

TASK: Remove from Trig Worms every question where a wrong-function or upside-down-ratio error, rounded to the nearest degree as the game marks, gives the key.
ROOT CAUSE: Find-the-angle questions at some ratio and angle pairs (e.g. CAH 75°, SOH and TOA 15°) let tan⁻¹ for sin⁻¹ or cos⁻¹, the other inverse, or the ratio upside down land on the key's whole degree. questionFrom drops a named distractor that equals the key, so the student using that method picks the key and is marked right. Count from the survey after Jon's rulings of 20 Oct (about 52; take the figure from the rewritten report).
CLASS CHECK: Same shape as PYTHAG-KEY-COLLIDE (#453), but no shared generator exists (KEY-COLLISION-SURVEY), so the fix is in this game's own pool construction. The survey has shown the class across all 14 generated games; this is the only listed game with wrong-method collisions still ruled for filtering.
EXACT CHANGE: Claim trig-worms in scripts/answer-lock-state.json in its own commit. games/trig-worms: one pass after the find-the-angle pools are built keeps only the (ratio, angle, sides) entries where no wrong-function or upside-down error, rounded to the nearest degree, equals the key. Filter once, as #453 did; no redraw loop (canon §12, SR-5). Rounding-before-inverse is not filtered (Jon's ruling). Verifier: enumerate every find-the-angle question, recompute key and errors exactly (mpmath), assert zero wrong-method collisions; plant the unfiltered pools and show the verifier catches the old count; report how many entries each (ratio, angle) loses. Take the claim off in the PR.
DO NOT TOUCH: Rounding-before-inverse cases; find-a-side questions; distractor choice beyond what the filter removes; scoring, levels, cannon mechanics; shared modules; modular-battle and every other game in the survey.
SUCCESS CONDITION: The verifier passes and fails on the plant; every angle and ratio a level offered before still appears; check-changed.py green; merged on a green Gate; main green after.
STOP IF: The filter removes every question for any (ratio, angle) a level offers, or more than 10% of any level's find-the-angle pool; the count differs from the rewritten report's; or the fix needs a shared module.
FINISH: Committed and merged; claim released; docs/handover/cloud.md updated with the entry, per-angle losses, PR and main run.

---

Amendment (Jon, 20 Oct), verbatim:

TRIG-WORMS-FILTER: filter all 52 and drop CAH at 80° and 85°: no triangle there can separate the right method from the slip. Amended SUCCESS CONDITION: every (ratio, angle) pair offered before still appears except CAH 80° and CAH 85°. Amended STOP IF: the filter empties any pair other than those two, or removes more than 10% of the find-the-angle pool. Take the count from the merged report; if it differs from 52, stop.
