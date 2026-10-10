CONTRACT: CAR-TRAP-DRAFT (Project Claude for Jon, 9 Oct 2026, 16:45). Phase 1 of the Car
Trap rewrite: draft only. Either lane may take it (cloud lane after LISTED-HIGH, or home
lane after its checkpoint), because it touches no live file. Save verbatim under
docs/handover/contracts/ when it starts.

======================================================================
TASK (CAR-TRAP-DRAFT): Draft every piece of prose for the rewritten
Car Trap escape room from Jon's brief, plus its art prompts, into one
review file for Jon. Change no live file.

ROOT CAUSE: car-trap was withdrawn on 8 Sep 2026, with the other rooms
awaiting their voice rewrite (canon §11.5). Its threat (the Head
arriving at 8:10) was not present in the room, which breaks canon's
rule ("a character who is not present can be the standard, never the
threat"), and its scene art clashes with its setting (canon §7 notes).
Jon has now given the premise and the antagonist in interview
(claude/car-trap-brief-2026-10-09.md, quoted in full below). Canon
§11.5: Jon reviews the draft before any file is touched.

CLASS CHECK: Not a bug: content work under the existing voice-rewrite
process. The voice contract (docs/escape-room-voice-contract.md), the
working doc (docs/escape-room-voice-rewrite.md, read first) and the
reference room (escape-rooms/hamster-heist/room.js) govern it. No
shared code.

THE BRIEF (Jon, 9 Oct 2026):
- It is the morning of a governors' visit. Never "Ofsted", in any form.
- The Head is the same vain Head as in Prom Budget (the statue): not
  reformed, not decent. The students back him as the lesser evil,
  because Strictman would be worse (Jon, 9 Oct 2026), and the prose may
  enjoy that. He drives an old plug-in hybrid, "the dullest car in the
  county" (optional, for Jon's review: he calls it "a statement of
  environmental leadership"). No brand names anywhere. He never knows
  what happened. Keep him consistent with prom-budget's portrayal; read
  that room first.
- Mr Strictman, the deputy head, is ex-military. He wants the school
  run like a training camp, marches everywhere, and wears impeccably
  starched "civvies". He is after the Head's job, and already speaks
  as if the school is his by right.
- He is in the car park with a measuring wheel doing an "efficiency
  survey" of the bays. It is cover: he has repainted the Head's bay
  narrower, set the barrier to come down early, and set the charger to
  trip, so the Head's arrival in front of the governors becomes a
  farce and his report can say the school "lacks discipline at the
  top".
- His own car is in the garage, so he has come in on his daughter's
  first car: small, with stick-on eyelashes on the headlights.
- The students' stake: if Strictman gets the top job, it's drill in
  the yard every morning and uniform inspections at the gate.
- Present and beatable: Strictman marches the far end of the row,
  working towards the students. That is the clock.
- Voice (Jon's line, the model for the wrong-entry lines): "Those two
  bays differ by 2.6 cm. This is not how it is done in MY school."
  Escalating, never mocking the students, only the bays and the
  standards.
- Win: the Head glides into his bay. With the lines restored to
  specification, the one car across two bays is the eyelash hatchback.
  The governors gather round it; Strictman explains, at length, that it
  is his daughter's. He loses graciously; no humiliation.
- Fail: the Head's car stops at the barrier in front of the governors.
  Strictman steps forward with his clipboard and the word
  "disappointing".

EXACT CHANGE:
1. Write docs/escape-room-drafts/car-trap-draft.md (a new file, not
   served) containing, in the order room.js uses them: title, hook,
   brief, stakes, win, fail; the wrongLines (four, escalating, in
   Strictman's voice); eight objects (name, where, and clue or flavour:
   six clues and at least two blanks), each clue written with
   {{key.token}} placeholders, never figures; for each lock: name,
   brief, instrument label and verb, hints, missSays and solve text;
   the three picture alts (scene, fail, win); the hub card line and the
   meta description.
2. Locks, all ★★ Core (grades 4–5):
   - Lock 1 (new; replaces visitor-space-bounds, which is ★★★): the
     Head's bay. The spec gives the width to the nearest 10 cm; the
     line painter must be set to the smallest width the spec allows (a
     lower bound from an error interval, not a calculation with
     bounds). Propose its variant parameters (widths, units, the
     expected misconception: the upper bound, or the stated value) for
     gen-escape-variants.py, and list them in the draft. Every variant
     must have exactly one settable answer (check-lock-bank.py rule).
   - Lock 2: keep boom-gate-sector (arc length to angle). Rewrite only
     its framing: Strictman set the barrier to come down early.
   - Lock 3: keep ev-charger-quadratic (factorise, reject the root
     above the limit). Rewrite only its framing: the Head's plug-in
     hybrid, with the charger set by Strictman to trip.
3. Art prompts for all three pictures, in the house style (canon
   §11.6: empty scenes, no people, no lettering), in the format of
   docs/escape-room-image-prompts.md. Underground staff car park;
   the measuring wheel left on a bonnet or a bollard; the scene has the
   Head's bay narrowed (fresh paint) and the barrier; the win shows the
   eyelash hatchback straddling two bays; the fail shows the dull
   hybrid stopped at the lowered barrier. Jon generates the images.
4. Run the prose against the voice contract's checklist and the room
   rules in the working doc, and list each rule with pass/fail at the
   end of the draft.
5. Open a PR with the draft file only, and record it in the handover:
   "Car Trap draft for Jon's review". Merge it on a green Gate (it
   changes nothing served).

DO NOT TOUCH: escape-rooms/car-trap/ (room.js, index.html,
teacher.html); the hub; the front page; the sitemap; the art files;
gen-escape-variants.py (propose parameters only); every other room.

SUCCESS CONDITION: the draft file exists, with every slot room.js
needs; no figure appears in the prose outside {{tokens}}; the
checklist is all pass, or each fail is explained; Jon has it to
review. Phase 2 (build, variants, art, release) is a separate contract
after Jon approves the draft.

STOP IF: the brief contradicts the voice contract or a room rule in a
way the draft cannot resolve (quote both); lock 1 cannot be given
exactly one settable answer in the instrument's range.
