FOLLOW-UP to SUMS-IN-DISGUISE: ONE EQUALS SIGN (Jon, 18 Nov 2026, 11:34, on Stage 5 "81 + 9 = 90 + 0 = ?": "THEY ARE 7 YEARS OLD, and we've got 2 equals signs on 1 line"). Project Claude's error: Tens on show asked for the chained question.

ROOT CAUSE: The regrouped question ("64 + 3 = 60 + 7 = ?", "27 + 5 = 30 + 2 = ?", "40 + 20 = 6 tens = ?"), the Stage 5 working line "7 + 5 = 12 = 10 + 2" and the exchange label "18 = 10 + 8" put two equals signs, or a sum after "=", on one line. Children of 7 are still learning that "=" means "the same as", not "the answer comes next"; a chain confuses exactly that. The blocks already show the regrouping.

CLASS CHECK: A game-wide presentation rule, not one screen. Apply it to every piece of maths the game renders, in both looks, and check it in the verifier, so no screen can break it again. No files outside the game change.

EXACT CHANGE:
- If #822 has not merged, add this to it (Amendment 4). If it has merged, open a new PR, SUMS-IN-DISGUISE-ONE-EQUALS, with #822's close-out as its first commit.
- THE RULE, for every KaTeX string the page renders (questions, the little sum, labels, the stacked working, Stage 4 options and prompts): at most one "=", a sum on its left, and on its right only a single number or "?".
- games/sums-in-disguise/index.html:
  - Put-back question: back to the plain big sum, "81 + 9 = ?" (tens items "40 + 20 = ?"). The regrouping shows in the blocks: under the stick group its value as a plain number (e.g. "90"), under the cube group its value (e.g. "0"), with no label under an empty group. No "=" in these labels.
  - Stage 5 exchange label: "10 + 8" (no "c =").
  - Stacked working, one "=" per line:
      ones:   4 + 3 = 7
             60 + 7 = 67
      tens:   4 + 2 = 6
             40 + 20 = 60
      cross:  7 + 5 = 12
             20 + 10 + 2 = 32
    The tens are highlighted as before. The tens working loses "6 tens = 60", which broke the rule's "sum on the left".
  - Read aloud follows the same lines ("81 plus 9 equals what?"; the working line by line).
- scripts/verify-sums-in-disguise.py: for every item in play, in both looks, collect every rendered KaTeX string and fail if any has more than one "=", or anything other than a single number or "?" after "=". New plants that must fail: "81 + 9 = 90 + 0 = ?"; "7 + 5 = 12 = 10 + 2"; "18 = 10 + 8".
- Note it in the saved contract and the handover.

DO NOT TOUCH: the bank, the marking (dataset.val), the blocks' counts and steps, LINES, read-aloud's local-voice rule, schools/assets/, other games. No listing. No draft PR.

SUCCESS CONDITION: No rendered maths anywhere in the game has two equals signs or a sum after "="; the verifier passes with the new plants failing; the Gate and phone-fit (dispatched on the branch) pass at 360 px in both looks; merged by merge-pr.py with its last line and main's run IDs reported.

STOP IF: merge-pr.py refuses for a reason other than a transient 5xx.

AMENDMENT 1 (Jon, 18 Nov 2026; verbatim):
FOLLOW-UP to SUMS-IN-DISGUISE-ONE-EQUALS (#823): "Empty group" meant ANY group with no blocks in it. When a group has no blocks (e.g. the cubes after 81 + 9, where c = 10 leaves none), show no group and no label: under 81 + 9 only "90" shows. If #823 has not merged, add it there; if it has, add it as the first change of the next PR in this lane, recorded in the handover. Verifier: no value label is drawn where its group has zero blocks; one new plant that must fail, a "0" label under an empty cubes group. Everything else in #823 stands.
