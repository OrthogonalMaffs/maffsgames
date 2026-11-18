LANE: cloud (Claude Code on the web), a FRESH session. SEND: now (#823 merged as 5e53fd4).
RECOMMENDED: Sonnet 5.5, medium effort. A small change to one game's labels and spoken text, with verifier checks.

TASK: SUMS-IN-DISGUISE-NO-LABELS. In Sums in Disguise (games/sums-in-disguise/), stop giving away the answer before the child chooses: remove the value labels under the block groups at put-back, and the values from the put-back read-aloud line.

ROOT CAUSE: #823 (ONE-EQUALS) moved the regrouping out of the question into value labels under the blocks at put-back. Jon, 18 Nov 2026, 12:21, on Stage 2 "70 + 10 = ?" with "80" written under the blocks: "are we happy making it THIS easy? the answer is right there".
- games/sums-in-disguise/index.html:943-946 draws these labels: 10c on tens items, 10(t + 1) and c − 10 on cross items, 10t and c on ones items. They give the answer, or its two parts, while the options are on screen.
- The read-aloud at put-back (lines 1134-1136) speaks the same values: "8 tens. Put it back on."; "70 and 10. Put it back on."; "60 and 7. Put it back on."
The blocks themselves are the method: the child reads eight sticks as eight tens. The labels do that step for her.

CLASS CHECK: One rule for the whole game, enforced where labels are drawn (drawBlocks) and where spoken text is built: before the big answer is marked, nothing on screen or spoken shows the answer or the regrouped values. Only the blocks show them. Not a one-stage patch: the verifier checks every Stage 1, 2 and 5 item in both looks. No files outside the game and its verifier change.

EXACT CHANGE:
0. First commit: the close-out of #823 SUMS-IN-DISGUISE-ONE-EQUALS per AGENTS.md's close-out rule: merge commit 5e53fd4; main's check-site and phone-fit-full run IDs and conclusions, read back from the API in this session; its contract to docs/history/contracts/ if one was saved. Then save this contract verbatim as docs/handover/contracts/2026-11-18-sums-in-disguise-no-labels.md.
1. games/sums-in-disguise/index.html:
   - Lines 943-946: draw the put-back blocks with NO label on any group (drop the label property). Counts unchanged: tens items c sticks; cross items t + 1 sticks and c − 10 cubes (no cube group when c = 10); ones items t sticks and c cubes. Remove the .labelled and .glabel CSS (lines 119 and 121) if nothing else uses them.
   - Read aloud at put-back (lines 1134-1136): every item speaks only "Put it back on." The question is still read as "81 plus 9 equals what?". The working is still read after the answer.
   - Unchanged: the parked disguise's tag (10t, or "0" on tens items, part of taking the tens off); the little-sum line ("7 + 1 = 8 ✓"); the one-equals rule; the stacked working shown after the answer.
2. scripts/verify-sums-in-disguise.py: for every Stage 1, 2 and 5 item in play, in both looks, from load until the big answer is marked, no rendered text outside the tag and the little-sum line, and no spoken text, contains:
   - the answer;
   - the regrouped tens value (10t, 10c on tens items, or 10(t + 1) in Stage 5) as a label;
   - c, or c − 10, as a label under blocks.
   New plants that must fail:
   - an "80" label under the sticks of "70 + 10";
   - the spoken "70 and 10. Put it back on." before marking.
3. docs/handover/cloud.md entry.

DO NOT TOUCH:
- The bank (226 items; SHA-256 19e415561cb6baecdaf01d2bde6f23f367a6aff2802d33b8d152dce6561068a8, as the verifier already checks).
- The marking (dataset.val), the block counts and the steps, the one-equals rule, LINES.
- Read-aloud's local-voice rule.
- schools/assets/, other games, canon (home lane).
- No listing.
- No draft PR.

SUCCESS CONDITION:
- In Stages 1, 2 and 5, both looks, the put-back screen shows the blocks with no value labels.
- The put-back read-aloud says only "Put it back on."
- The verifier passes, with both new plants failing.
- The Gate and phone-fit (dispatched on the branch) pass at 360 px in both looks.
- Merged by merge-pr.py, with its last line, the merge commit and main's check-site and phone-fit-full run IDs reported.
- Handover committed.

STOP IF:
- Lines 943-946 or 1134-1136 no longer match the description above (report what is there).
- merge-pr.py refuses for a reason other than a transient 5xx it already retries.
