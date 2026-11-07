LANE: home (Codex) · TIER: Shared · only after ROOM-ORDER-HERRINGS (codex/escape-herrings) has merged, from current main

COORDINATION: the cloud lane owns games/whose-side-are-you-on/ and its verifier (WHOSE-SIDE-FIT, then WHOSE-SIDE-BIOS). Claude Code (home) may be on PHONE-FIT-ASIDE: scripts/measure-phone-fit.py, scripts/phone-fit-state.json, docs/canon.md §7.6.1, games/equatle/, games/52dle/, games/prime-or-composite/. Touch none of those. Record in the PR body, and in docs/handover/home.md keeping every entry.

TASK: File Jon's 11 Christmas pack images and build a 6-set printable pack for The Christmas Tree Fiasco with tools/pack-generator, every answer recomputed independently.

ROOT CAUSE: New room for the generator. The room (#667) is live; Jon's 11 images are on branch art/christmas-pack (74bcc1b) as PNGs at the branch root (xmas-01-truck-display.png ... xmas-11-slider.png, 1254x1254 RGB), each checked by Project Claude at full size. The generator refuses a room without rooms/<slug>/config.json and without each lock in lockcheck.py's RECOMPUTE.

CLASS CHECK: Mostly local: a new room's config, art and recompute functions, in the slots the generator already provides (README "Adding a room"). One possible shared change: the truck display carries two readouts on two separate screens, and a config image has one label_box. If (and only if) both readouts cannot sit legibly in the top screen's box at 11 pt, add OPTIONAL generic support for "label_boxes": a list of boxes, the image's printed text split at the clue's existing " · " separator in order, the count of parts required to equal the count of boxes (build fails otherwise). Room-agnostic, covered by a selftest plant, Kiln unchanged. No Christmas-specific logic in build_pack.py.

EXACT CHANGE:
1. Art: for each of the 11 PNGs, run scripts/strip-gen-watermark.py (report what it finds; Project Claude saw no mark), then save as WebP in tools/pack-generator/rooms/christmas-tree-fiasco/art/ with the same base name, at most 250 KB each, no resize below what Kiln used (1254 square). No PNG committed outside art/christmas-pack. The art/christmas-pack branch is not merged; Jon deletes it after.
2. Config: tools/pack-generator/rooms/christmas-tree-fiasco/config.json, in Kiln's schema: room, pack_version "1", sets 6, seed 1, certificate_title "Tree delivered" (DRAFT for Jon), final shape default. Roles and fonts:
   01 truck-display clue label · 02 eric-clipboard clue hand · 03 prize-leaflet clue label · 04 hall-plan clue label · 05 packing-slip clue label · 06 sticky-note clue hand · 07 old-box herring hand, text "DO NOT USE" · 08 laptop herring label, text "The Christmaffs Store's final, counting down" · 09 dial answer christmas-cold-store · 10 keypad answer christmas-scale-clearance · 11 slider answer christmas-combined-ratios.
   Label boxes measured on each WebP in image pixels, inset inside the blank area:
   01 the top screen (or both screens, per CLASS CHECK) · 02 the sheet, below the clip · 03 the cream panel inside its border · 04 the bottom strip below the ruled line · 05 the slip between the two tapes · 06 the note · 07 the white label · 08 the screen · 09 the label plate · 10 the display glass, clear of the holly at its top-left · 11 the label plate.
   Herring texts come from each object's flavour in room.js and contain no digit.
3. lockcheck.py RECOMPUTE, each by its own method (import neither the variant generator nor the set checks):
   christmas-cold-store: the smallest whole number of hours t with start*h + g*t >= min*h, found by counting t up from 0 in integers (no division); the common wrong answer per the lock's missTitle (the gap measured from the absolute value of start), also by counting; check rate and rise.
   christmas-scale-clearance: in millimetres, integers only: ceiling c*1000, tree d*k*10, stand s*10; answer = (ceiling - tree - stand)/10; the common wrong answer per the lock's missTitle; check tree, total and ccm.
   christmas-combined-ratios: by enumeration: the unique (B, T, U) of positive integers with B + T + U = N, B*b = T*a and T*d = U*c; answer U; the common wrong answer per the lock's missTitle; check r1:r2:r3, parts and each.
4. Build: python -X utf8 tools/pack-generator/build_pack.py christmas-tree-fiasco. Every existing check must pass (labels at 11 pt or more, no herring digit, no giveaways, set letters, footer, URL, score sheet, 150-word page 1, final padlock rules). Run --selftest; it must include the new room and pass. The PDF stays in dist-packs/ (gitignored): never committed, uploaded or attached.
5. Proof for review: export PNGs of page 1, the answer key, and set A's cover, both evidence pages and locks page at 100 dpi to docs/screens/christmas-pack/ (committed, small), so Project Claude can review without the PDF.
6. Report: the VALID joint-draw count; the 6 sets' answers per lock and each final padlock target; each label's fitted point size; anything the build warned about.

DO NOT TOUCH: escape-rooms/christmas-tree-fiasco/ (room.js, teacher.html, art) and escape-rooms/variants.json; the Kiln config and art; build_pack.py except the optional label_boxes support above; final.py's rules; the image content (convert only); the files under COORDINATION.

SUCCESS CONDITION: The pack builds with 6 sets and every check green; every Christmas lock recomputed independently and matching; selftest passes including the new room (and the label_boxes plant if added); the 11 WebPs under 250 KB each; proof PNGs committed. Committed, PR open, Gate green, home.md entry; stop for Project Claude's review of the proof PNGs and Jon's "merge". Jon then builds the PDF at home and proofreads it.

STOP IF: ROOM-ORDER-HERRINGS has not merged; the generator cannot reach 6 sets with fair final padlocks under the herring rule (report the count it reaches); any recompute disagrees with a variant (report the variant; do not edit the library); a label cannot fit its box at 11 pt (report the image and the text, do not shrink below 11 pt); strip-gen-watermark.py finds a mark on an image (report which; do not edit the art beyond its standard removal); a change to room.js or variants.json seems necessary.

AMENDMENT 1 to CHRISTMAS-PACK (Project Claude, 6 Nov 18:05). Codex's stop was correct; the fix is in the room, not the generator.

ROOT CAUSE (added): every other room marks the words printed on an object with exactly one <b>...</b> per clue (76 of 87 clues across 14 rooms); The Christmas Tree Fiasco has 0 of 6. split_clue() is right to require it. A plain-text mode in build_pack.py would have to guess where narration ends, so it is not authorised.

EXACT CHANGE (added, item 0): in escape-rooms/christmas-tree-fiasco/room.js, markup only, no word changed, wrap the printed part of each clue in one <b>...</b>:
- truck-display: Two readouts. <b>CHILLER ZONE (TREE): {{ct.start}} °C · FREEZER ZONE (MINCE PIES): −18 °C</b>
- eric-clipboard: Eric&apos;s handwriting. <b>TREE COMES INSIDE AT {{ct.min}} °C OR WARMER. WARMS {{ct.g}} °C EVERY {{ct.h}} HOURS ONCE UNLOADED</b>
- prize-leaflet: The Christmaffs Store&apos;s drawing of the prize tree. <b>DRAWN TO SCALE 1 : {{sc.k}}. HEIGHT ON THIS PAGE {{sc.d}} cm. STAND ADDS {{sc.s}} cm</b>
- hall-plan: The caretaker&apos;s plan. <b>HALL CEILING {{sc.c}} m · FIRE DOOR WIDTH 1.2 m</b>
- packing-slip: The prize list. <b>BAUBLES : TINSEL = {{cr.a}} : {{cr.b}} · TINSEL : CHRISTMAS UNICORNS = {{cr.c}} : {{cr.d}}</b>
- sticky-note: <b>MAX {{cr.N}} DECORATIONS. FIRE LOAD.</b> Underneath, smaller: There is no such thing as too much tinsel.
Then run scripts/check-escape-rooms.py (VALID count must stay 98 of 900; every other check unchanged) and the escape-room play-through, and confirm the room still renders each clue (now with its printed words in bold, as in the other rooms).

DO NOT TOUCH (amended): room.js may change ONLY by adding those six <b>...</b> pairs. Still no plain-text clue support in build_pack.py; label_boxes stays the only build_pack.py change allowed. Herring flavours, variants and everything else in room.js unchanged.

STOP IF (added): any check's result changes after the markup (VALID count, TRUE-MINUS, tokens); split_clue() still fails on a Christmas clue.

AMENDMENT 2 to CHRISTMAS-PACK (Project Claude, 6 Nov 18:12). Stop correct; the fault is generic, so the fix is in build_pack.py.

ROOT CAUSE (added): render()'s `numbered` collects every page tagged with a set letter, including the per-set hint pages a room gets when its hints use the set's figures (hint_sets = sets). Those pages sit at the end, so each set's list is no longer contiguous; set_pages_line() falls back to the long form with ranges like "A 6-30", which is longer and wrong. Any room with set-specific hints hits this; Kiln does not only because its hints carry no figures.

CLASS CHECK: Yes, shared code serving every room. Fix it in build_pack.py, room-agnostic.

EXACT CHANGE (added):
a. `numbered` counts only each set's student pack pages: kinds cover, evidence and locks (never hints).
b. When per-set hint pages exist, set_pages_line() appends one short sentence: "Hint cards: pages X-Y, one page per set." (from the build). With one shared hint page, the line is unchanged, so Kiln's page 1 must stay exactly as it is now (150 words).
c. Selftest: plant a per-set hint page counted inside a set's range; it must be caught (the range check fails). Kiln's page 1 text compared before/after: identical.

DO NOT TOUCH (amended): build_pack.py may change for label_boxes and for (a)-(c) only. Page 1's draft wording (run_it()) is unchanged: no word cut to fit.

STOP IF (added): Christmas page 1 is still over 150 words after (a)-(b) (report the count and the line; do not cut Jon's draft text); Kiln's page 1 changes in any way.

AMENDMENT 3 to CHRISTMAS-PACK (Project Claude, 6 Nov 18:20). Supersedes Amendment 2 (b) and its "Kiln page 1 unchanged" condition.

1. set_pages_line(): when per-set hint pages exist, the line ends "; hint cards X-Y." inside the same sentence, e.g. "Each set is 4 pages: A 6-9 … F 26-29; hint cards 30-35." (no separate sentence). With one shared hint page, the line is unchanged.
2. run_it(), Project Claude's DRAFT wording, three trims (all rooms):
   "Tell the teams your penalties." -> "Tell teams your penalties."
   "Final padlock ticked: write down the time." -> "Final padlock ticked: note the time."
   "Hand over the card and add one to Hints." -> "Hand over the card; add one to Hints."
   Update run_it()'s docstring to cite this amendment. Nothing else in page 1 changes; the DRAFT badge stays.
3. Expected: Christmas page 1 at most 150 words; Kiln page 1 = its current text minus exactly those three trims (147 words). Report both counts and both lines.
4. Selftest: the range plant from Amendment 2 stays; all plants caught.

STOP IF: Christmas page 1 is still over 150 words (report the count); any other part of page 1 or any other page changes.

AMENDMENT 4 to CHRISTMAS-PACK (Project Claude, 6 Nov 18:25).

STANDING AUTHORITY (this contract only): a fault in build_pack.py exposed by building a second room may be fixed there, provided the fix is room-agnostic, its root cause is stated in the PR body, a selftest plant catches the fault, Kiln still builds, and any change to Kiln's output is reported with before/after page images. Wording changes, room.js changes and lowering any check's threshold are still NOT authorised: stop for those.

Under it, now:
a. Answer key misconception list (build_pack.py ~line 889): fill missTitle and missSays through the same filler as clues, with Set A's variant, and say so in the list's lead-in: "(shown with Set A's figures)". The build's existing unfilled-{{token}} check must pass. Plant: a missTitle token left unfilled, caught.
b. Locks page: the working-space boxes take the height that is left after the briefs (flex), with a minimum height per box; state the minimum in the PR body. If a set cannot meet the minimum, the existing overflow check fails the build. Report each set's box height and Kiln's before/after.

STOP IF: a locks page cannot meet the minimum without cutting brief text (report the overflow per set); filling the key needs a token the variants do not carry; any fix would need wording, room.js or a threshold change.

AMENDMENT 5 (review fixes; verbatim below):

CHRISTMAS-PACK, review fixes for PR #689 (Project Claude, 6 Nov 19:20; supersedes the 19:15 block). The previous session finished: PR #689 is open on codex/christmas-pack and the worktree is clean. Ignore the earlier recovery handover; there is nothing to recover. Continue on this branch, same PR.

LANE: home (Codex) · TIER: Shared · branch codex/christmas-pack, PR #689 · same COORDINATION and STANDING AUTHORITY as the consolidated CHRISTMAS-PACK contract (docs/handover/contracts/2026-11-06-christmas-pack.md on this branch)

TASK: Fix the printed labels in the Christmas pack so every figure reads cleanly and sits inside its blank area, and change the leaflet clue so it cannot be read as "measure the picture".

ROOT CAUSE: Project Claude's proof review found: (1) the truck's two readouts share the top screen, leaving the bottom one blank, and the text runs into the border; (2) the label wrapper breaks a number from its unit ("AT 16 / °C OR") and inside a ratio ("= 5 : / 1"); (3) the laptop's label box is wider than its screen, so text runs onto the bezel; (4) the slider's answer box sits below its white plate on the cover; (5) answer captions repeat the unit when the label already holds it ("...COME IN hours", "CHRISTMAS UNICORNS unicorns"); (6) an /updates/ line the contract did not ask for; (7) the leaflet's "HEIGHT ON THIS PAGE 10 cm": on paper the drawn tree is about 4 cm, so "this page" invites a student to measure the printed picture and get it wrong (Jon, 6 Nov: change it).

CLASS CHECK: (2) and (5) are generic build_pack.py faults (every room's labels and captions), so they are fixed there, room-agnostic, with selftest plants. (1), (3) and (4) are this room's config (label boxes measured wrong); (1) uses the already-authorised optional label_boxes. (6) and (7) are local.

EXACT CHANGE:
1. Truck (xmas-01): label_boxes with two boxes, the top and bottom screens' glass, inset; the clue's printed text split at " · " into "CHILLER ZONE (TREE): {{ct.start}} °C" and "FREEZER ZONE (MINCE PIES): −18 °C". Generic label_boxes support with its selftest plant (part count must equal box count), Kiln unchanged.
2. Line breaking (build_pack.py, all rooms): a number never separates from what follows it as a unit or symbol (°C, cm, m, %, and similar), and "a : b" never breaks around its colon. Implement by binding those pairs with non-breaking spaces before fitting. Plants: a label whose fit splits "16 °C"; one that splits "5 : 1". Kiln's labels compared before/after; report any change.
3. Minus signs: confirm every negative figure printed on the art uses U+2212 (TRUE-MINUS, #671), the truck's −8 and −18 included. If any is a hyphen, fix it in the generic printing path, with a plant.
4. Laptop (xmas-08): re-measure the label box inside the screen's glass only, inset; the text must fit at 11 pt or more.
5. Slider (xmas-11): re-measure the label box inside the white plate; check the dial's and keypad's boxes the same way on the cover.
6. Answer captions (build_pack.py, all rooms): don't append the instrument's unit when the label already contains it (case-insensitive, whole word: "hours", "unicorns", "(cm)"). Plant: a label containing its unit, which must not be printed twice.
7. Remove the updates/index.html line from this PR.
8. escape-rooms/christmas-tree-fiasco/room.js, prize-leaflet clue, ONE wording change (Jon, 6 Nov): "HEIGHT ON THIS PAGE {{sc.d}} cm" -> "HEIGHT ON THE LEAFLET {{sc.d}} cm". Nothing else in room.js changes. Then re-run check-escape-rooms.py (VALID stays 98 of 900) and the escape play-through; the online clue and the teacher page's clue table show the new wording.
9. Re-export the proof PNGs (page 1, answer key, set A cover, both evidence pages, locks page) and add a set D evidence page 1 (other figures, other line lengths). Report each label's fitted point size.

DO NOT TOUCH: room.js beyond the six <b> pairs and item 8; the maths, variants, sets and seed; page 1's wording; image content; the files under COORDINATION.

SUCCESS CONDITION: Each readout sits in its own truck screen; no figure is separated from its unit and no ratio breaks; every label sits inside its blank area at 11 pt or more; negative figures print with U+2212; no repeated units; the leaflet reads "HEIGHT ON THE LEAFLET" online and on paper; the /updates/ line gone; selftest passes with every new plant caught; Kiln still builds (changes reported with before/after images); new proof PNGs committed; Gate green. Stop for Project Claude's review and Jon's "merge".

STOP IF: a label cannot fit inside its blank area at 11 pt once the bindings are in (report the image and text); any Kiln label changes in a way that isn't the two binding rules or the unit rule; the minus fix needs a change outside the generic printing path; the wording change alters any check result other than the clue text itself.
