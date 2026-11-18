TOOL: Claude Code (home lane). SIZE: small (one sentence of room text, one config, a final build). Recommended: Sonnet, medium effort.
MERGE TIMING: one merge heading for main at a time. I-DROPPED-MY-ICE-CREAM (cloud) is building; if it is in its Gate or merge when yours is green, wait for it, rebase (or merge main in; never force-push), then merge.

TASK: Approve The Canteen Hack's print pack: add Jon's sentence to the room's opening so the £8.40 cookie reads as the Healthy Week price, record his approval, and build the final pack as v2.

ROOT CAUSE: The start read-out (from escape-rooms/canteen-hack/room.js hook, lines 76-79 on bb46787) says the last cookie is "under a glass dome at £8.40", the same in every set, while the price-tags lock asks for last term's baseline, which differs by set (£1-£7). Reading it cold, Jon (18 Nov 03:42) asked "why is the cookie at £8.40 in the intro if it's a different price for each group?" The £8.40 is deliberate (room.js:46: "THE COOKIE'S HEALTHY WEEK PRICE IS £8.40 AND THAT FIGURE IS LOAD-BEARING"), but nothing in the text says it is the inflated price. Jon approved the rest of the draft pack (canteen-hack-pack-v1.pdf, built on bb46787).

JON'S RULINGS (verbatim in the PR body): 18 Nov 2026 03:43: "yes that chance would be good, other than that I'm happy" (to: add "Last term it cost a fraction of that." after the £8.40 sentence, in the live room and so in the pack; and approval of the pack's other wording).

CLASS CHECK: Local: one room's opening text and one room's pack config. The pack reads the room's hook, so one edit fixes both the live room and the pack; no generator change.

EXACT CHANGE:
First commit: CANTEEN-PACK's close-out (AGENTS.md rule): #817 merged as 236e9ae via merge-pr.py, exit 0, last line "main 236e9ae run 44165899116: GREEN"; check-site 44165899116 success, phone-fit-full 44165898866 success. Fill in its home handover "MERGED: pending" line and move its contract to docs/history/contracts/. Save this contract verbatim at docs/handover/contracts/2026-11-18-canteen-approve.md.
1. escape-rooms/canteen-hack/room.js, hook: after "…under a glass dome at &pound;8.40." insert, verbatim, " Last term it cost a fraction of that." (same sentence, before "Ms Cinnamon is in her room…"). Nothing else in the hook, brief, locks or variants.
2. tools/pack-generator/rooms/canteen-hack/config.json: "wording_approved": {"by": "Jon", "date": "2026-11-18"}; "pack_version": 2 (the draft v1 reached Jon; the final differs, so it takes a new number).
3. Build `python -X utf8 tools/pack-generator/build_pack.py canteen-hack --final`: file canteen-hack-pack-v2.pdf, no DRAFT anywhere, the start read-out contains the new sentence and still fits; sets, answers and final padlocks unchanged from v1 (A 1928, B 2340, C 2960, D 2000, E 1510, F 3508).
4. /updates/: one line, in the site's plain wording, that The Canteen Hack's opening now says the cookie's price has rocketed since last term. docs/todo.md: close CANTEEN-PACK-APPROVE; leave CORE-BUNDLES-2 open. Home handover entry.

Run only the checks this contract names and the Gate: the --final build, check-escape-rooms.py, test-pack-generator.py with self-test. No optional all-game local runs.

DO NOT TOUCH: every other room; the rest of Canteen's text, locks and variants; the pack generator; every other pack's config; games/i-dropped-my-ice-cream/ and anything I-DROPPED-MY-ICE-CREAM touches; Gate files; the cloud handover.

SUCCESS CONDITION:
- The live room's opening contains "Last term it cost a fraction of that." right after the £8.40 sentence.
- canteen-hack-pack-v2.pdf builds --final with no DRAFT and the new sentence in the start read-out; targets unchanged.
- check-escape-rooms.py and test-pack-generator.py pass; the other ten packs unchanged.
- PR merged on green via `python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600`; report its last line and exit status and main's check-site and phone-fit-full run IDs and results on the merge commit. Home handover documented.

STOP IF:
- The new sentence fails any wording or content check (report the check and its message; do not reword Jon's text).
- The start read-out no longer fits at the generator's type floor.
- Any set, answer or padlock target changes.
- merge-pr.py refuses for a reason other than a transient 5xx it already retries.
