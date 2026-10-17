CONTRACT: BSB-ROOM-DRAFT (Project Claude for Jon, 16 Oct 2026, 10:30).
CLOUD LANE. Phase 1: draft only. Save verbatim under
docs/handover/contracts/ in the first commit.

TASK: Draft "Big School Begins", a four-challenge Year 6/7 escape room
set on transition day at St Martha's Secondary, as a prose draft with
every slot room.js needs, the four locks' parameter sets checked, and
the voice checklist, for Jon's review. Build nothing.

ROOT CAUSE: The hub has no room for Year 6 or new Year 7. Jon's brief
(16 Oct 2026): a transition-day scavenger hunt in which the locks are
not physical but challenges of not getting lost and of helping a
fellow new student.

CLASS CHECK: Not a bug: a content draft under the existing room
process (docs/escape-room-voice-rewrite.md, canon §11, the format of
docs/escape-room-drafts/dnd-club-draft.md). Three of Jon's rulings
depart from canon for this room only: four locks, a 20-minute timer,
and a "Year 6/7" label in place of stars. The draft records them and
changes no shared code or canon; phase 2 carries them, and the home
lane records the exceptions in canon.

JON'S RULINGS (16 Oct 2026):
1. Title "Big School Begins". Label "Year 6/7", no stars: the Year 7s
   relate to the buddy, the Year 6s to the new students.
2. Four challenges and a 20-minute timer, as named exceptions for this
   room only, not a new default. Penalty stays 45 seconds.
3. Frame: the transition-day scavenger hunt. The locks are hunt clue
   cards and "don't get lost" challenges; the engine's lock mechanics
   are reskinned in prose. No antagonist.
4. William Trembles: a nervous new Year 6 from another primary who
   keeps getting lost; the team keeps finding him. He is never the
   joke: no character mocks his name, no line plays on it, and no one
   gives him a nickname.
5. Daisy Reddington, Year 7 buddy: helpful, and remembers what being
   new was like. She voices each challenge's misconception as her own
   past mistake ("When I started, I read the grid backwards..."), so a
   wrong answer is met with reassurance and never with the answer
   (Jon, 15 Oct: wrong-answer feedback must not give the answer away).
6. Mrs Barb Phile, "Bibby", the librarian (Library Jam): the library is
   a hunt stop, and she sets challenge B. Stern and precise, never a
   villain.
7. The four challenges, in this order:
   A. The hall: find the library on the school map. Coordinates, first
      quadrant (KS2). Answer: the grid reference as a two-digit code,
      x then y. Misconception: x and y swapped (code y then x).
      Constraints: x and y from 1 to 9, x != y. Keypad, maxDigits 2.
   B. The library: Bibby's directions. Turns in degrees (KS2). You
      face one of the 8 compass points; the next stop lies at another;
      how many degrees CLOCKWISE must you turn? Misconception: the
      anticlockwise turn, 360 - answer. Constraints: answer a multiple
      of 45 from 45 to 315, and never 180 (its misconception would
      equal it). Dial, min 0, max 360, step 45.
   C. The corridor: when does William's lesson end? Time durations
      (KS2). A lesson starts at hh:mm and lasts m minutes; the answer
      is the end time as digits (11:30 -> 1130). Misconception: an hour
      treated as 100 minutes, i.e. the start written as a number plus
      m (10:35 + 55 -> 1035 + 55 = 1090). Constraints: m from 35 to
      70; mm + m crosses exactly one hour, so the answer is always
      40 more than the misconception; the start is from 10:00 to 14:30,
      so neither answer nor misconception has a leading zero. Keypad,
      maxDigits 4.
   D. The canteen: lunch on a £5 card. Money and change (KS2). Three
      items; the answer is the change in pence. Misconception: in each
      column, take the smaller digit from the larger (total 365:
      answer 135, misconception 265). Constraints: prices multiples of
      5p; total from £2.00 to £4.50; the total's units digit is 5 and
      its tens digit non-zero, so both columns need an exchange and the
      misconception never equals the answer. Keypad, maxDigits 3.

EXACT CHANGE:
1. docs/escape-room-drafts/big-school-begins-draft.md: every room.js
   slot, in prose with {{tokens}} only (no bare figures), with [X] on
   anything extrapolated and a "For Jon" section.
2. The clock and the ending are not yet ruled. Draft them as [X]
   proposals: the clock is the hunt's end (teams report back for
   lunch); the ending is everyone at one canteen table, William
   included. Jon rules on both at review.
3. "For Jon" must include:
   a. Object count: eight objects with at least two blanks leaves six
      clues for four locks. Propose the count; the canon minimum of two
      blanks stands.
   b. Theme: canon §7.5.1 makes a Year 6 room light and playful. Say
      what that needs from the shared room styling (a phase 2, home
      lane change), without changing it.
   c. How "Year 6/7" replaces the derived stars (rating.js and the hub
      chip are shared; phase 2, home lane). Propose; change nothing.
   d. Each lock's grade/level field, as the build will need it.
   e. Whether challenge B's dial should use the full 360° sweep
      (sweep: 360), where 0 and 360 coincide; neither is ever an
      answer.
4. Parameter sets for A-D in the format of the library draft. Check
   every set against the joint-draw rules (canon §11.3) and report the
   expected VALID count across the four locks.
5. The voice contract's checklist and the room rules, pass/fail each,
   at the end of the draft.
6. One PR: the draft file, the saved contract and the cloud.md handover
   entry. It changes nothing served: merge on a green Gate with main
   green, then watch main's run.

DO NOT TOUCH: every existing room; escape-rooms/assets/ (engine.js,
rating.js, teacher.js, engine.css); the hub; the front page; the
sitemap; docs/art/ (no art prompts: Project Claude writes them after
the build); gen-escape-variants.py (propose parameters only); canon;
CLAUDE.md; docs/todo.md.

SUCCESS CONDITION: The draft exists with every slot room.js needs. No
figure appears in the prose outside {{tokens}}. All four locks' sets are
listed and checked, with a VALID count. The checklist is all pass, or
each fail is explained. The For Jon items and the two [X] proposals are
present. The PR is merged, main is green, and the handover is recorded.

STOP IF:
- Main's latest full run is red.
- Any lock cannot be given exactly one settable answer on its
  instrument, or its misconception is not settable.
- The joint draw over four locks gives fewer than 20 VALID combinations.
- The brief contradicts the voice contract or a room rule in a way the
  draft cannot resolve (quote both).
- Any lock would need maths beyond KS2.
- You would schedule any task that merges, pushes or edits.

END OF CONTRACT
