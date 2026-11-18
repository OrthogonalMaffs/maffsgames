LANE: cloud (Claude Code on the web), a FRESH session. SEND: now. Needed for a class playing the game TOMORROW (Thu 19 Nov 2026); this goes ahead of everything else queued.
RECOMMENDED: Opus 5.5, high effort. Stage 5's teaching step changes to match how the class is taught.

TASK: SUMS-IN-DISGUISE-BRIDGE. Change Sums in Disguise's Stage 5 (crossing a ten, games/sums-in-disguise/) from "add the ones, then split the teen number" to the class teacher's method, BRIDGING TO THE NEXT TEN: 38 + 6 = 38 + 2 + 4 (38 + 2 = 40, 40 + 4 = 44).

ROOT CAUSE: Stage 5 (main ddc11e6) asks the child to add the ones first (8 + 6 = 14, tiles 0-20), then exchanges ten of the 14 cubes for a stick (exchange(), :907-941; working(), :648; spoken text :681 and :1128). The class teacher, asked how her class crosses a ten (via Jon, 18 Nov 2026, 16:54): "We teach going across a tens boundary by bridging to the next ten then adding or subtracting the extra (38+6 - 38 +2 +4)". Jon decided at 10:46 to follow her method once known. The current Stage 5 teaches a different method from the class's, the day before they play it.

CLASS CHECK: Local to Stage 5's flow (type cross) in this one game: the take-off, the blocks, the hat, put-back and marking are shared with Stages 1 and 2 and stay as they are. The bank is unchanged: everything new is worked out from each item's big [p, q] and little [a, b] (bridge = 10 − a, rest = b − bridge = a + b − 10). No files outside the game and its verifier change.

JON'S DECISIONS (verbatim in the PR body): 18 Nov 2026, 10:46: "yes lets split it, and I will ask her how she bridges 10 so I can do it the way she teaches"; the teacher's reply above, relayed by Jon at 16:54. Do not put the teacher's name anywhere.

EXACT CHANGE:
0. First commit: the close-out of #824 SUMS-IN-DISGUISE-NO-LABELS per AGENTS.md's close-out rule: merge commit ddc11e6; main's check-site and phone-fit-full run IDs and conclusions, read back from the API in this session; its contract to docs/history/contracts/. Then save this contract verbatim as docs/handover/contracts/2026-11-18-sums-in-disguise-bridge.md.
1. games/sums-in-disguise/index.html, Stage 5 only, both looks. For an item (10t + a) + b with a + b ≥ 10, write bridge = 10 − a and rest = a + b − 10. The flow:
   1. TAKE OFF: unchanged. The t sticks go into the hat (tag 10t). The a cubes now sit inside a TEN OUTLINE: a column of ten slots, the shape of a stick, with a slots filled and bridge slots empty. The b cubes sit beside it.
   2. MAKE TEN: the question is "a + ? = 10" in KaTeX (e.g. "8 + ? = 10"), answered on tiles 0 to 10, marked by dataset.val against bridge. This replaces the "a + b" little-sum step in Stage 5. A wrong tile shows the right one and carries on, no score either way, as now.
   3. FILL THE TEN: a button from LINES (kids.fill_ten "Fill the ten!", grown.fill_ten "Fill the ten"); the outline is also tappable, as a real button with its own click handler and an aria-label.
      - bridge cubes slide from the b group into the empty slots;
      - the full outline becomes a stick and hops into the hat; the tag goes from 10t to 10t + 10;
      - rest cubes stay (none when a + b = 10).
      LINES.<look>.reveal["stage-5"] shows now.
   4. PUT IT BACK: unchanged. The hat comes back, the question is "38 + 6 = ?", and the four options appear only now.
   - Remove ten_in_hat from both LINES blocks (fill_ten replaces it). Change no other LINES string.
   - Every new kid line is 6 words or fewer. Every rendered maths string keeps the one-equals rule: one "=", with a number or "?" on its right. "8 + ? = 10" meets it.
   - Nothing on screen or spoken before the big answer is marked shows the answer or 10t + 10 as a label (the NO-LABELS rule). The tag is excepted, as now.
   - The pointing hand (kid look, first question of a run) points at the tiles at step 2 and at the fill button at step 3.
2. The working for cross items, one "=" per line, the tens highlighted as now, numbers from the item:
       p + bridge = 10(t + 1)              e.g. 38 + 2 = 40
       10(t + 1) + rest = answer           e.g. 40 + 4 = 44
   When rest = 0, only the first line shows (its right-hand side is the answer).
3. Read aloud (cross items, built from the item):
   - step 2: "8 and how many make 10?";
   - step 3: "Fill the ten.";
   - put-back: "Put it back on.";
   - working: "38 plus 2 is 40. 40 plus 4 is 44." (rest 0: "38 plus 2 is 40.")
   Remove the old exchange line ("10 ones make a ten. Put the ten in the hat.") and the old cross working text.
4. The aha lines are unchanged and keyed by decoy as now (forgot_ten is still the likeliest slip).
5. The page's about text for Stage 5 (:351) describes bridging: "Crossing a ten: fill the next ten first. 38 + 6 is 38 + 2 + 4."
6. scripts/verify-sums-in-disguise.py, for every Stage 5 item in play, in both looks:
   - the ten outline shows a filled and bridge empty slots;
   - the step-2 tile key is bridge (10 − a);
   - after fill, t + 1 sticks and rest cubes, and the tag reads 10t + 10 only after fill;
   - the options do not exist until put-back;
   - the working lines match the item, with one line when rest = 0;
   - the spoken text matches.
   Replace the old exchange checks and plants with new plants that must fail:
   - the step-2 key set to a + b (the old method);
   - the old working line "8 + 6 = 14" shown;
   - fill skipped;
   - a wrong rest count;
   - "40 + 4" with the wrong number.
   All existing Stage 1-4 checks pass unchanged.
7. In docs/todo.md row SUMS-IN-DISGUISE-LIST, replace "Stage 5 method provisional until Jon hears how the class crosses a ten" with "Stage 5 bridges to the next ten, as the class is taught (SUMS-IN-DISGUISE-BRIDGE)". docs/handover/cloud.md entry.

DO NOT TOUCH:
- The bank (226 items; SHA-256 19e415561cb6baecdaf01d2bde6f23f367a6aff2802d33b8d152dce6561068a8).
- Stages 1 to 4, the marking of the big answer (dataset.val), the decoys.
- The other LINES strings, the one-equals and no-labels rules, read-aloud's local-voice rule.
- The start picture, schools/assets/, other games, canon (home lane).
- No listing. No draft PR.

SUCCESS CONDITION:
- Stage 5 in both looks: hat off, "a + ? = 10" on tiles, fill the ten (the stick goes into the hat), put back, choose; the working reads "38 + 2 = 40" / "40 + 4 = 44".
- The verifier passes with the new plants failing.
- The Gate and phone-fit (dispatched on the branch) pass at 360 px in both looks.
- Merged by merge-pr.py, with its last line, the merge commit and main's check-site and phone-fit-full run IDs reported, TONIGHT if the checks allow.
- Handover committed.

STOP IF:
- The ten outline, the b cubes, the tiles and the tag cannot fit above the fold at 360 px for the worst item (a = 1 or b = 9; report the layout).
- Any Stage 1-4 check fails after the change.
- merge-pr.py refuses for a reason other than a transient 5xx it already retries.
