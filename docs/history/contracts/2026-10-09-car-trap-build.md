CONTRACT: CAR-TRAP-BUILD (Project Claude for Jon, 9 Oct 2026, 23:00). Phase 2 of the Car Trap rewrite. Either lane. Save verbatim under docs/handover/contracts/ when it starts.
====================================================================== TASK (CAR-TRAP-BUILD): Build the rewritten Headteacher's Car Trap room from the approved draft (docs/escape-room-drafts/car-trap-draft.md, merged in #235), with Jon's three changes below, and leave it ready for Jon to play-test behind its holding page. Do not release it.
ROOT CAUSE: car-trap was withdrawn on 8 Sep 2026 for its voice rewrite. The phase 1 draft is approved (Jon, 22:53): all eleven "For Jon" decisions stand, with the changes listed here.
CLASS CHECK: Not a bug: content build under the existing room process (docs/escape-room-voice-rewrite.md §2 steps 6–7; canon §11). The engine and checker are shared and are NOT changed.
JON'S RULINGS ON THE DRAFT (9 Oct, 22:53):

1. "The dullest car in the county" appears ONCE, in the hook only.
   * Stakes: "The Head comes down the ramp in the dullest car in the county and stops at the barrier" becomes "The Head comes down the ramp in his plug-in hybrid and stops at the barrier".
   * Lock 3 onOpen: "When the Head plugs in, the dullest car in the county will charge in the dullest possible way." becomes "When the Head plugs in, his car will charge without anyone noticing, which is how it does everything."
   * Leave "the dullest car imaginable" in the fail art prompt (not prose the student reads).
2. "Strictman" is invented and maps to no real person (Jon confirmed).
3. The room is ★★ Core. Record that in the handover for the difficulty contract; do NOT add a star field or label to the room or hub (the difficulty contract owns the scheme).
4. Wrong-entry line 1 keeps Jon's line with the figure in words: "Those two bays differ by two point six centimetres." (Project Claude's recommendation; Jon may still ask for the no-number version.) Everything else in the draft stands as written, including every [X].

EXACT CHANGE:

1. escape-rooms/car-trap/room.js: rewrite every slot from the draft with the changes above — title, hook, brief, stakes, win, wrongLines, the eight objects (keep the six clue ids; new blank ids `hatchback` and `sign`), the three locks. Entities in every slot except object and lock `name`/`where` (canon §11.3). No `missArt` on any lock; record why in the room.js header.
2. Lock 1 head-bay-lower-bound: add the draft's bank entry to a new docs/lock-bank-batch8.txt; add its variant library to scripts/gen-escape-variants.py with the draft's eight widths (variant 0 = 2.4, the bank entry) and the draft's solver; re-run the generator so variants.json and room.js's variants: block are written by it. Never hand-edit a variants: block. Remove visitor-space-bounds from this room (keep its bank entry; do not delete history).
3. Locks 2 and 3: framing fields only, per the draft. Every maths field unchanged.
4. escape-rooms/car-trap/teacher.html: update for the new lock 1 and the new blanks (clue → lock map by id).
5. Art: remove the room's references to its six old pictures (they show the wrong scene). The room runs with art pending — the engine's fallback, as rooms I and J did on 2026-08-31. Leave the old files in docs/art/ untouched. The three new prompts in the draft are for Jon to run; when he supplies images, filing them is a separate step. Write the draft's three alts into room.js as sceneAlt/failAlt/winAlt.
6. Run python scripts/check-escape-rooms.py and check-lock-bank.py; both must pass, with car-trap's VALID count reported (draft measured 352 of 512).
7. Keep the holding page. Start serve-stubbed.py in the background and open the room in Jon's Chrome (Jon cannot run it himself); play it through once yourself first, opening all three locks and reading all three lock briefs on screen (working doc §8: the P.E. lesson).
8. Open a PR; merge on a green Gate (nothing public changes while the holding page stays). Record in the handover: built, awaiting Jon's play-test; release is a separate step on Jon's word.

DO NOT TOUCH: engine.js, teacher.js, engine.css; check-escape-rooms.py and the collision rules; every other room; the hub, front page and sitemap; the holding page's noindex; docs/art/ files; prom-budget (the Head speaks only there).
SUCCESS CONDITION: both checkers pass; the room plays end to end in Jon's Chrome with all three locks opening on their answers and each named misconception giving its own response; "the dullest car in the county" appears exactly once in the room's prose; no figure in prose outside tokens except the draft's flagged words; the room is still behind its holding page; handover updated.
STOP IF: the VALID count falls below 20; any lock has more or less than one settable answer; the generator cannot reproduce the draft's lock 1 library; anything requires an engine change; a slot in the draft does not fit room.js as the draft assumed (quote it).

---
Jon's answers, 10 Oct 2026 (to two questions from the cloud session, which cannot reach his machine):
- teacher.html (a holding page on main, like index.html): "Write it now (Recommended)" — the real teacher page now, noindex and unlinked.
- Play-test: "Unlinked preview page, as you describe, but with analytics switched off on play.html, so no play-test events are logged as car-trap. At release, play.html's content becomes index.html and play.html is deleted in the same PR."
