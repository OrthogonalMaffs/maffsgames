LANE: cloud (Claude Code on the web), the same session. SEND: once merge-pr.py has reported #821's last line (main's check-site and phone-fit-full). Before DAILY-ANSWERS.
RECOMMENDED: Sonnet 5.5, medium effort. One picture into an existing game, with a check.

TASK: SUMS-IN-DISGUISE-ART. Put Jon's start picture under the title of Sums in Disguise (games/sums-in-disguise/), in both looks, as Ice Cream does.

ROOT CAUSE: #821 shipped without a start picture. The house pattern is a picture under the title, as in i-dropped-my-ice-cream, its-a-sine and the ESSENTIALS-ART games. Jon made the picture (18 Nov 2026, 09:12: "I LOVE IT"). Project Claude then removed one stray floor shadow, cropped and converted it.

CLASS CHECK: Local. The picture belongs to this game alone, and the .start-art pattern already exists (i-dropped-my-ice-cream/index.html lines 136-139 and 173). Copy that pattern; no shared file changes.

EXACT CHANGE:
0. First commit: the close-out of #821 SUMS-IN-DISGUISE per AGENTS.md's close-out rule: merge commit e9f236e; main's check-site and phone-fit-full run IDs and conclusions, read back from the API in this session; its contract to docs/history/contracts/. Then save this contract verbatim as docs/handover/contracts/2026-11-18-sums-in-disguise-art.md.
1. Copy the file "start (1).webp" from the root of branch art/sums-in-disguise, byte for byte, to games/sums-in-disguise/assets/start.webp.
   - Before copying, check it: SHA-256 bfdd4ecd1d99f714387c8030e6dfc500ba1d0e18cbe1ebadc26a59fef4484645, 54,110 bytes, 1600 x 873 WebP.
   - The name on the branch has a space and "(1)" (Jon's download name). The copy is named start.webp.
2. games/sums-in-disguise/index.html: under the title on the start screen, in both looks:
   <img class="start-art" src="assets/start.webp" width="1600" height="873" alt="Five disguises hanging on coat hooks in a cloakroom: a fake moustache, round glasses, a wig, a rubber duck and a top hat, above an empty bench">
   Use the same .start-art CSS as Ice Cream (lines 136-139), including the max-height:600px rule. The picture is not shown on the play screen.
3. scripts/verify-sums-in-disguise.py, as verify-its-a-sine.py does (around line 543):
   - the img has its src, width, height and alt;
   - the file is 1600 x 873;
   - its SHA-256 is the one above.
   Add one plant that must fail: a missing alt.
4. docs/handover/cloud.md entry. In todo row SUMS-IN-DISGUISE-LIST, add: "start picture in (SUMS-IN-DISGUISE-ART)".

DO NOT TOUCH:
- The branch art/sums-in-disguise (don't delete, merge or change it).
- schools/assets/, any other game, the bank, LINES, the marking and the read-aloud.
- canon (home lane).
- No listing.
- No draft PR.

SUCCESS CONDITION:
- The start screen of /games/sums-in-disguise/ and of /games/sums-in-disguise/#kids/Maple shows the picture under the title.
- verify-sums-in-disguise.py passes, with the new plant failing.
- check-site, phone-fit (dispatched on the branch), check-theme and check-start-mount all pass.
- Merged by merge-pr.py, with its last line, the merge commit and main's check-site and phone-fit-full run IDs reported.
- Handover and todo committed.

STOP IF:
- The file on art/sums-in-disguise is missing or its SHA-256 differs (report both).
- The picture pushes the stage buttons below the fold at 360 px in either look, and the Ice Cream CSS doesn't fix it.
- merge-pr.py refuses for a reason other than a transient 5xx it already retries.

DECIDED IN SESSION (Jon, 18 Nov 2026, on STOP IF "the picture pushes the stage buttons below the fold at 360 px"): "Accept as is (Recommended)". Ice Cream's CSS is used unchanged. At 360 x 640 stage 1 stays fully above the fold in both looks (bottom 571 of 600 grown, 557 kids); before the picture stages 1 to 3 showed. Ice Cream and It's a SINE show none of their stage buttons above the fold at that size.

AMENDMENT 1 (the follow-up to SUMS-IN-DISGUISE, recorded here as the contract asks; verbatim):
FOLLOW-UP to SUMS-IN-DISGUISE (Jon, 18 Nov 2026, 10:38, playing Stage 4 in the kid look: "asking the kids to find 5 factorial is a bit advanced isn't it?").

ROOT CAUSE: LINES.kids.find is "Find {little}!", so the screen reads "Find 2 + 5!", which is 2 + 5 factorial. Project Claude's placeholder. It is the only place in the repo where a "!" follows maths (games/sums-in-disguise/index.html:293).

CLASS CHECK: Local: one string in one game's LINES; no other game has a "!" straight after an expression. The check below stops this game's LINES ever doing it again.

EXACT CHANGE:
- If SUMS-IN-DISGUISE-ART has not merged, add this to its PR (record it there as Amendment 1). If it has merged, open a new PR, SUMS-IN-DISGUISE-FIND, with the close-out of SUMS-IN-DISGUISE-ART as its first commit.
- games/sums-in-disguise/index.html: LINES.kids.find "Find {little}!" → "Find {little} in disguise!". Change nothing else in LINES.
- scripts/verify-sums-in-disguise.py: no LINES string, in either look, has "{little}" or "{big}" followed by "!" or "?"; the read-aloud text for Stage 4 matches the new line. One new plant that must fail: "Find {little}!".
- In the saved contract and the handover, note the change.

DO NOT TOUCH: everything else in LINES, the bank, the marking, the read-aloud logic, schools/assets/, other games. No listing. No draft PR.

SUCCESS CONDITION: Stage 4 in the kid look reads "Find 2 + 5 in disguise!"; the verifier passes with the new plant failing; the Gate and phone-fit pass; merged by merge-pr.py with its last line and main's run IDs reported.

STOP IF: the new line breaks phone-fit at 360 px, or merge-pr.py refuses for a reason other than a transient 5xx.

AMENDMENT 2 (verbatim):
FOLLOW-UP to SUMS-IN-DISGUISE: STAGE 5 SPLIT (Jon, 18 Nov 2026, 10:45-10:46: "stage 5 doesn't really land on its own, the 10 in the hat makes sense to me but would it make sense to a 7 year old"; "yes lets split it"). Provisional: Jon is asking the class teacher how she crosses a ten, and may change the method afterwards. Do not put the teacher's name anywhere.

ROOT CAUSE: In Stage 5 the step that does the work (the 1 in 12 is a ten, and it joins the tens) happens only in the child's head. The disguise carries the tens away and back in Stages 1 and 2, but nothing on screen shows the ten from the little sum going into the hat, so "forgot the ten" (22 for 27 + 5) has nothing visual to correct it.

CLASS CHECK: Local to this game's Stage 5 flow (type cross). No shared file changes. The bank is unchanged: the split is worked out from each item's little and big.

EXACT CHANGE:
- If the PR in flight (SUMS-IN-DISGUISE-ART or SUMS-IN-DISGUISE-FIND) has not merged, add this to it (record it as the next amendment). If it has merged, open a new PR, SUMS-IN-DISGUISE-SPLIT, with the close-out of the last merged PR as its first commit.
- games/sums-in-disguise/index.html, Stage 5 only (both looks), with a new step after the little sum:
  1. Unchanged: she takes off the hat (its tag shows 10t, e.g. 20), then answers the little sum on tiles 0 to 20. A wrong tile shows the right answer and carries on, as now.
  2. NEW, the split: the little answer c is drawn as base-10 blocks, one ten-stick (ten small squares in a column) and c − 10 single cubes (none when c = 10), with "c = 10 + (c − 10)" in KaTeX under them, e.g. "12 = 10 + 2".
  3. NEW, she moves the ten: a button from LINES (kids.ten_in_hat "Put the ten in my hat!", grown.ten_in_hat "Put the ten in the hat"), with the ten-stick itself also tappable (a real button with its own click handler and an aria-label). The stick hops into the hat, and the hat's tag changes from 10t to 10t + 10 (20 → 30). With prefers-reduced-motion it moves without animation. In the kid look, the pointing hand shows on this step on the first question of a run.
  4. The hat goes back on, and she answers "27 + 5 = ?" from the four options, as now.
  - The stacked working for cross items becomes:
      7 + 5 = 12 = 10 + 2
      27 + 5 = 20 + 10 + 2 = 32
    lined up on the first "=", with the moved 10 highlighted. Every number comes from the item.
  - Read aloud, for the split step: "12 is 10 and 2. Put the 10 in the hat." Built from the item. The working in words: "7 plus 5 is 12, which is 10 and 2. So 27 plus 5 is 20 plus 10 plus 2, which is 32."
  - Add ten_in_hat to both LINES blocks, exactly as above. Change no other line.
- scripts/verify-sums-in-disguise.py, for every cross item in play, in both looks:
  - the split shows one ten-stick and exactly c − 10 cubes;
  - the label reads "c = 10 + (c − 10)";
  - the tag goes from 10t to 10t + 10 only after the ten is moved;
  - the big options don't appear until it is moved;
  - the stacked working's numbers match the item.
  New plants that must fail: a wrong cube count; the tag not changing; the options shown before the ten is moved.
- Note the change in the saved contract and the handover. Add to todo row SUMS-IN-DISGUISE-LIST: "Stage 5 split is provisional until Jon hears how the class crosses a ten."

DO NOT TOUCH: Stages 1-4, the bank, the other LINES, the marking (still dataset.val), read-aloud's local-voice rule, schools/assets/, other games. No listing. No draft PR.

SUCCESS CONDITION:
- Stage 5 shows the split for every item, including the c = 10 items (no cubes).
- The ten has to be moved before the big options appear.
- The verifier passes with the new plants failing.
- The Gate and phone-fit (dispatched on the branch) pass at 360 px in both looks.
- Merged by merge-pr.py, with its last line and main's run IDs reported.

STOP IF: the blocks and the hat cannot fit above the fold at 360 px, or merge-pr.py refuses for a reason other than a transient 5xx.

AMENDMENT 3 (Jon, 18 Nov 2026, 10:45-10:53; REPLACES Amendment 2, which was built on the branch but not committed or merged, and is kept above only as a record; verbatim):
FOLLOW-UP to SUMS-IN-DISGUISE: TENS ON SHOW (Jon, 18 Nov 2026, 10:45-10:53). This REPLACES the "STAGE 5 SPLIT" follow-up if you received it: build this instead, keeping only what fits below. The "find" line fix (LINES.kids.find) is separate and stands.

JON'S WORDS: 10:45 "stage 5 doesn't really land on its own, the 10 in the hat makes sense to me but would it make sense to a 7 year old"; 10:50 "so we're REMOVING the existing 10's to focus on the unit addition, then putting the 10's back in, that step is not clearly happening in the game"; 10:52 "it's just not made clear WHY that is happening if the student doesn't know the step". The Stage 5 method is provisional: Jon is asking the class teacher how she crosses a ten. Do not put the teacher's name anywhere.

ROOT CAUSE: The method has three steps: take the tens off, add the ones, put the tens back. The take-off flow shared by Stages 1, 2 and 5 (unmask() and onTile(), games/sums-in-disguise/index.html around lines 747-785) shows the "what" of two of them and the "why" of none:
- nothing shows that 77 is 70 + 7, so the tens vanish into the disguise like magic;
- disguiseOn(false) parks the disguise in a corner, far from the sum;
- after the little sum, disguiseOn(true) snaps it back and askBig() asks the big sum, so putting the tens back is never shown or done;
- in Stage 5 the ten made by the ones is never shown, and the reveal line "Hey! A ten in my hat!" fires at take-off, when the hat holds seven tens.

CLASS CHECK: Architectural within this game. The gap is in the take-off flow shared by Stages 1, 2 and 5, so the fix is one picture model (base-10 blocks) and one put-back step in that flow, with the Stage 5 exchange as its cross-item case. No files outside the game change. The bank is unchanged: every number and block count comes from the item.

EXACT CHANGE:
- If the PR in flight (SUMS-IN-DISGUISE-ART, -FIND or -SPLIT) has not merged, add this to it (record it as the next amendment). If it has merged, open a new PR, SUMS-IN-DISGUISE-TENS, with the close-out of the last merged PR as its first commit.
- games/sums-in-disguise/index.html, Stages 1, 2 and 5, both looks (inline SVG, no emoji; every button a real button with its own click handler, PR 811 rule):
  1. BLOCKS. Under the big sum, draw it as base-10 blocks:
     - ten-sticks (ten small squares in a column) and single cubes;
     - ones and cross items, (10t + a) + b: t sticks and a cubes, then b cubes;
     - tens items, 10a + 10b: a sticks, then b sticks.
     A "+" between the groups. Sticks in one colour, cubes in another; the stacked working's highlight matches the sticks. Blocks scale to fit; never fewer blocks than the count.
  2. TAKE OFF (button LINES.<look>.take_off, or tap the disguise). The disguise parks BESIDE the sum and STAYS VISIBLE.
     - Ones and cross items: the t sticks fly into it, and its tag reads 10t. The cubes stay; the sum becomes the little sum.
     - Tens items: no sticks leave. The disguise holds a "0", and the sum becomes a + b, counting the sticks as ones.
     The reveal line shows here for Stages 1 and 2. Stage 5 shows no line at take-off.
  3. ONES. Unchanged: she answers the little sum on tiles (0 to 10; 0 to 20 in Stage 5). A wrong tile shows the right answer and carries on. Then the blocks show c counted.
  4. STAGE 5 EXCHANGE (button LINES.<look>.ten_in_hat, or tap the cubes). Ten cubes join into one stick, which hops into the hat: the tag goes from 10t to 10t + 10, leaving c − 10 cubes (none when c = 10). "c = 10 + (c − 10)" shows in KaTeX. LINES.<look>.reveal["stage-5"] shows NOW.
  5. PUT IT BACK (button LINES.<look>.put_back, or tap the parked disguise). The disguise and its sticks slide back beside the cubes. The question shows the regrouping in KaTeX, matching the blocks:
       ones:  "64 + 3 = 60 + 7 = ?"
       tens:  "40 + 20 = 6 \text{ tens} = ?"
       cross: "27 + 5 = 30 + 2 = ?"
     The four options appear only now.
  - With prefers-reduced-motion, everything moves without animation. In the kid look, the pointing hand points at each button (take off, ten in the hat, put it back) on the first question of a run.
- LINES: add to kids: put_back "Put it back on!", ten_in_hat "Put the ten in my hat!". Add to grown: put_back "Put the disguise back on", ten_in_hat "Put the ten in the hat". Change no other line; every kids line stays 6 words or fewer.
- Stacked working after the answer, lined up on the first "=", with the tens highlighted:
    ones:   4 + 3 = 7
           60 + 7 = 67
    tens:   4 + 2 = 6
            6 tens = 60
    cross:  7 + 5 = 12 = 10 + 2
           20 + 10 + 2 = 32
- Read aloud, built from the item:
  - at take-off: "77 is 7 tens and 7 ones. The tens go in the hat.";
  - at the exchange: "10 ones make a ten. Put the ten in the hat.";
  - at put-back: "70 and 10. Put it back on.";
  - the working in words.
- Stages 3 and 4: unchanged.
- scripts/verify-sums-in-disguise.py, for every Stage 1, 2 and 5 item in play, in both looks:
  - the block counts at every step match the item (start: t sticks, a cubes, b cubes; after take-off: t sticks in the disguise; Stage 5 after the exchange: t + 1 sticks and c − 10 cubes; after put-back: the regrouped numbers);
  - the disguise stays visible and parked beside the sum;
  - the options do not exist until put-back;
  - the regrouped question and the stacked working match the item;
  - the Stage 5 reveal line appears only at the exchange.
  New plants that must fail: a wrong stick count; a wrong cube count; the disguise hidden at take-off; the options before put-back; a wrong regrouped number (50 + 7 for 64 + 3); the Stage 5 reveal at take-off; the exchange skipped.
- Note the change in the saved contract and the handover. Add to todo row SUMS-IN-DISGUISE-LIST: "Stage 5 method provisional until Jon hears how the class crosses a ten."

DO NOT TOUCH: the bank, the marking (dataset.val), Stages 3 and 4, the other LINES, read-aloud's local-voice rule, schools/assets/, other games. No listing. No draft PR.

SUCCESS CONDITION:
- In Stages 1, 2 and 5 the child sees the sum as blocks, watches the tens go into the disguise, adds the ones, (Stage 5) exchanges ten ones for a ten, puts the tens back, and only then chooses an answer, with every count matching the item.
- The verifier passes with every new plant failing.
- The Gate and phone-fit (dispatched on the branch) pass at 360 px in both looks.
- Merged by merge-pr.py, with its last line and main's run IDs reported.

STOP IF: the worst item (9 sticks, 9 cubes and 9 cubes) cannot be drawn legibly above the fold at 360 px with the parked disguise and the tiles (report the layout), or merge-pr.py refuses for a reason other than a transient 5xx.
