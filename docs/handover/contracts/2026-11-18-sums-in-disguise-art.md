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
