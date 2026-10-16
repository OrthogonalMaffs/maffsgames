CONTRACT: DND-ROOM-BUILD (Project Claude for Jon, 15 Oct 2026). Phase 2 of the D&D Club room. Either lane. Save verbatim under docs/handover/contracts/ when it starts.

TASK (DND-ROOM-BUILD): Build the "Roll for Initiative" escape room from the approved draft (docs/escape-room-drafts/dnd-club-draft.md, merged in #415) with Jon's six changes below, and leave it ready for Jon's play-test behind a holding page. Do not release it.

ROOT CAUSE: New room, first build under the lifted build freeze (Jon, 15 Oct 2026). Phase 1 draft approved by Jon with six changes (Project Claude's review, 15 Oct 2026). Idea credited to Mrs Rogers, who consented to her name being used (recorded in the handover).

CLASS CHECK: Not a bug. Content build under the existing room process (docs/escape-room-voice-rewrite.md §2 steps 6–7; canon §11). The engine, checker and variant generator are shared and are NOT changed in logic; only new lock entries and variant libraries are added in the existing formats.

JON'S RULINGS ON THE DRAFT (15 Oct 2026):
1. Title: "Roll for Initiative". Slug: roll-for-initiative.
2. Initiative moves to lock 3: lock 3's brief opens "The goblins have seen you. 'Roll for initiative,' you tell her: it's how a fight decides who goes first." Remove the "last piece of ceremony" initiative paragraph and its phase-2 note from the room brief.
3. Win: "She writes it in the species box" becomes "She writes DWARF in the species box and WIZARD in the class box."
4. Hint ladders are generic (every student sees them; the single misconception is handled by missTitle/missSays only):
   Lock 1: unchanged from the draft.
   Lock 2: (1) "Did you use the Commandant's scale?" (2) "There are 100 cm in a metre." (3) "One square on the mat is {{plan.sq}} m. How many fit along the corridor?"
   Lock 3: (1) "The fireball covers the space inside the circle." (2) "Area uses the radius squared." (3) "Square the radius, multiply by π, then round."
5. "Form G-14" becomes "Form G" everywhere (wrong-entry line 2, lock 1's open, the gate clue's guard description). "Form R-1" in lock 3's open stays.
6. Token names stay distinct: no token in lock 3 may be named sq (it means the square size in lock 2). Name the circle's bounding square sqr if it is used at all; after ruling 4 it appears in no prose.
Everything else in the draft stands as written, including every [X], Mrs Rogers' approved lines word for word, and rulings 1 and 16 already in the draft.

EXACT CHANGE:
1. escape-rooms/roll-for-initiative/room.js: every slot from the draft with the six rulings applied: title, hook, brief, stakes, win, wrongLines, the eight objects (ids as the draft's table), the three locks (keypads; ids, keys, grades 4/3/4, labels, maxDigits, verbs, missTitle, missSays, hints, solve, onOpen as drafted and ruled). Entities in every slot except object and lock name/where (canon §11.3). No missArt on any lock; record why in the room.js header. Header also carries the credit line and the date of Mrs Rogers' consent.
2. escape-rooms/roll-for-initiative/index.html and teacher.html in the existing room format. The teacher page carries the credit line "Built from a teacher's idea. Thank you, Mrs Rogers." in its footer, and every lock's answer and solve (read from room.js, as every room does).
3. Lock bank: the three locks' bank entries in a new docs/lock-bank-batch<N>.txt (next free number). escape_set_checks.LOCKS: the three solvers and clue_numbers exactly as the draft's pot sections state, including lock 3's stated π-and-3.14 agreement check.
4. scripts/gen-escape-variants.py: add the three variant libraries with the draft's sets (gate 9, plan 7, fireball 5; variant 0 first in each) and constraints, then re-run the generator so variants.json and room.js's variants: block are written by it. Never hand-edit a variants: block. The joint draw must report the draft's counts (182 of 315 VALID, variant 0 VALID); reconcile any difference in the PR.
5. Art: Jon supplies three images. Run each through scripts/strip-gen-watermark.py --width 1600 --frame 1600x873 and file them as docs/art/roll-for-initiative-scene.webp, -fail.webp, -win.webp. Write sceneAlt, failAlt and winAlt from the draft, re-checked against the filed images.
6. Holding page: the room is reachable at its URL for Jon's play-test and Mrs Rogers' preview, with noindex, and is NOT in the hub, the front page, the sitemap or any listing, as Car Trap was before release.
7. Run check-escape-rooms.py, check-content-safety.py, check-student-labels.py and the room's checks; play the room in Chromium to a win and a time-out at 390px and 1280px (the existing play checks), and attach both end screens to the PR.
8. Handover: the room is built and held, the preview URL, ★★ Core with grades 4/3/4 for the difficulty contract, the credit and consent record, and "Awaiting Jon's play-test and Mrs Rogers' preview before release".

DO NOT TOUCH: The engine (engine.js) and checker logic; every other room and its variants (re-running the generator must leave every other room's variants: block byte-identical); the hub, front page and sitemap; any game. No star field or label on the room or hub (the difficulty contract owns it).

SUCCESS CONDITION: The room plays to a win and a time-out at both sizes with all three locks solvable on every variant. Every check passes, and variants.json and all other rooms' blocks are unchanged except for the new room. The art is filed watermark-free with matching alts. The room is reachable only at its URL, noindex and unlisted. Full CI is green. Merged, with the handover entry. Release (hub card, front page, sitemap, removal of noindex) is a separate instruction from Jon after his play-test and Mrs Rogers' preview.

STOP IF: Jon's three images are not supplied (build everything else, leave the art slots falling back as the engine allows, and report). The generator can't reproduce the draft's sets or joint-draw counts. Any approved line of Mrs Rogers would need to change. Re-running the generator changes any other room's variants. Any check requires a change to shared engine or checker logic.
