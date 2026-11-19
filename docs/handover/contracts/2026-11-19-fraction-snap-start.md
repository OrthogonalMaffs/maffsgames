FRACTION-SNAP-START, one part.
LANE: cloud. Send now; FORMULA-FORGE-40 has merged (#834, d10f9d7). TIER: Small. MODEL: Claude Code, Sonnet 5.5, low effort.

TASK: Fraction Snap's start screen stops teaching the old "+1 on the bottom" trick and draws its fractions in KaTeX.

ROOT CAUSE: games/fraction-equivalence/index.html:157-159 (main 1f88f36) say "½ and 4/9 are not equivalent", the shape #833 removed from the game (1/2 to 4/9 is ×4 on top, ×4 + 1 on the bottom). All three lines are plain text, not KaTeX (canon 7.1.1).

CLASS CHECK: Local: this game's own teaching text. The page already renders inline TeX through the shared MaffsText.html (schools/assets/mathtext.js, used at :415), so no new mechanism is needed.

EXACT CHANGE:
1. First commit: close out #834 FORMULA-FORGE-40 (d10f9d7; read main's runs on it from the API, record them in its cloud.md entry, move its contract to docs/history/contracts/). Save this contract verbatim as docs/handover/contracts/2026-11-19-fraction-snap-start.md.
2. Lines 157-159 become these three, rendered through MaffsText.html once KaTeX is ready (line 156, "Equivalent = same value, different form", is unchanged):
   \(\dfrac{1}{2}\) and \(\dfrac{4}{8}\) are equivalent: both are 0.5
   \(\dfrac{1}{2}\) and \(\dfrac{2}{3}\) are not: adding the same number to the top and bottom changes the value
   Cross multiply to check: \(\dfrac{a}{b}\) and \(\dfrac{c}{d}\) are equivalent when \(ad = bc\)
3. scripts/verify-fraction-equivalence.py: the how-to check (:368-370) and its plant (:415-416) move to the new third line: the rule must name its fractions a/b and c/d (now as \dfrac{a}{b} and \dfrac{c}{d}) and state ad = bc. Add a check that the how-to contains no "4/9" or "4}{9}", and that every fraction in it renders as KaTeX in Chromium (no plain n/d text). New plant that must FAIL: the old "½ and 4/9 are not equivalent" line restored. Every other check and plant passes unchanged.
4. Phone-fit: the start screen must still fit at every phone size it fits at now (Aa mode at 320x568 already warns on main; it must not get worse).
5. Report only, change nothing: list other games' start screens or how-to text with a plain-text fraction (a digit, "/", a digit), in the PR body and cloud.md.
6. cloud.md entry. PR, Gate and phone-fit-full green, then merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600; report its last line. No draft PR.

DO NOT TOUCH: the game's banks, generators, marking, boards and best; schools/assets/; canon; docs/handover/home.md; any other game; docs/todo.md.

SUCCESS CONDITION: the three lines read as above, in KaTeX; the verifier passes with the new plant failing; phone fit no worse; the report-only list given (or "none"); #834 closed out; merged by merge-pr.py with a GREEN last line; cloud.md records it all.

STOP IF: lines 156-159 or the verifier's :368-370 / :415-416 don't match this contract (report what is there); the start screen fails a phone size it passes on main; merge-pr.py can't reach GitHub; anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies (report under "Decided for you").
