# D-BY-DX-SIGN-LINE (Jon, 27 Nov 2026), verbatim

```text
D-BY-DX-SIGN-LINE (Project Claude, Fri 27 Nov 2026 13:10; checked against main 99a8e30)
Jon, 27 Nov 2026, 12:59: "yes please" to one small cloud contract with the s2-06 fix and D-BY-DX-BUILD's close-out.
RECOMMENDED: Claude Code, Sonnet 5.5, effort low. One placeholder string in one page, plus the close-out records.
LANE: cloud. SEND: now. First commit carries D-BY-DX-BUILD's close-out (AGENTS.md:62): #933 squash-merged as 024e9ae by merge-pr.py on a green Gate at 41029c4 (check-site 45909502642, phone-fit-full 45909502704); main's runs on 024e9ae: check-site 45911763308, phone-fit-full 45911763285, pages 45911762690, each success. merge-pr.py's last line was not captured by that session (its first watch hit a 10-minute limit and the script refuses to re-watch a merged PR); record it as "not captured; main's result read from GitHub Actions". Move docs/handover/contracts/2026-11-26-d-by-dx-build.md to docs/history/contracts/. Save this contract verbatim as docs/handover/contracts/2026-11-27-d-by-dx-sign-line.md in the same commit.
TIER: Medium (merge on green).

TASK: Reword d by dx? Why?'s placeholder sign_lost line so it is true on every item that uses it, s2-06 included.

ROOT CAUSE:
- games/d-by-dx-why/index.html:353, LINES.sign_lost: "The power was negative, so bringing it down gives a minus." It assumes the number in front is positive.
- Six stage 2 items use sign_lost (s2-01 to s2-06, :296-301). On s2-01 to s2-05 the number in front is positive and the answer is negative, so the line holds. On s2-06 (f(t) = -2/t^3, answer 6t^-4, decoy -6t^-4) the number in front is negative, so bringing the power's minus down makes the answer positive. The line tells the student the opposite.
- The decoy and key are right: the verifier models sign_lost as "the power brought down without its minus" (scripts/verify-d-by-dx-why.py:332), which is exactly how -6t^-4 arises on s2-06. Only the line's wording is wrong.

CLASS CHECK: Local. The error key, the bank's decoy model (tools/d-by-dx-why/bank.py:166) and the verifier are correct for all six items. One line of text is worded for positive coefficients only. Every other LINES line was checked against the items that use it, and none makes a claim an item contradicts. No new key, no bank change: the bank's SHA-256 stays a8ecdc05...428a14e.

EXACT CHANGE:
1. games/d-by-dx-why/index.html:353: the sign_lost value becomes exactly
   "The power is negative, so its minus comes down with it: 3 × -2 = -6, but -2 × -3 = +6."
   (× is U+00D7; the minuses are ASCII hyphens, as in the power_wrong_way line.) Keep the line's format: two-space-indented key, colon, space, a JSON string, a trailing comma (the verifier's lines_of() regex, scripts/verify-d-by-dx-why.py:105). The comment above LINES (placeholders by Project Claude; Jon writes the real lines) stays.
2. docs/handover/cloud.md: an entry for this task, including the close-out above, and a line for Jon: every sign_lost line he writes must hold for a negative number in front too (s2-06).
3. /updates/: none (the game is unlisted).
4. Merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600 when the Gate is green; if main moves while it waits, merge main into the branch and let the Gate re-run before merging. Report its last line, or, if the watch is cut off, main's run IDs on the merge commit read from GitHub Actions.

DO NOT TOUCH:
- The bank (tools/d-by-dx-why/bank.py and the embedded items), ERR_STAGES, every other LINES line, the table, Pro, the layout and the verifier.
- Every other game; schools/assets/; canon; the roster; docs/todo.md; every workflow; docs/handover/home.md; scripts/merge-pr.py.
- No force-push.

SUCCESS CONDITION:
- On s2-06, choosing -6t^-4 shows the new line; on s2-01, choosing 6x^-3 shows the same new line. The verifier's play units show the line for the chosen option's key, unchanged, and pass.
- The bank's SHA-256 is unchanged.
- D-BY-DX-BUILD's contract is in docs/history/contracts/ with its merge record in cloud.md.
- Merged on green through merge-pr.py; main green after; last line (or main's run IDs) reported in cloud.md.

STOP IF:
- The verifier fails on the new line for a reason other than a typo of yours (for example, it holds the line's text somewhere): report it; do not change the verifier.
- main is red when you come to merge: report it; do not use --override.
- merge-pr.py cannot reach GitHub or refuses: report its output; do not merge another way.
```
