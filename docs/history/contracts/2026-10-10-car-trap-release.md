CONTRACT: CAR-TRAP-RELEASE (Project Claude for Jon, 10 Oct 2026, 13:00). HOME LANE (owns Car
Trap). Save verbatim under docs/handover/contracts/.

======================================================================
TASK (CAR-TRAP-RELEASE): Fix Car Trap's first two wrong-entry lines and
its brief to Jon's wording, then release the room: live on its own URL,
on the hub and the front page, in the sitemap, with play.html retired.

ROOT CAUSE: Jon play-tested play.html (10 Oct, 4:40, all locks open,
win correct). One fault: wrong lines 1 and 2 are measurement verdicts
("Those two bays differ by two point six centimetres", "Paint
wandering… Noted."). The engine shows a room's wrong lines after any
wrong setting, on any lock, so in a red box straight after a wrong
barrier angle they read as a judgement on the student's answer. Every
other room's lines are overheard talk about something else.

CLASS CHECK: Local. All eight live rooms checked (10 Oct): their wrong
lines are unrelated background talk, as the engine's room-wide design
intends. Only Car Trap's are verdicts on precision. Fix the content of
this room; the engine is correct.

JON'S WORDING (approved 12:56), entities as usual in room.js:
- wrongLines[0]: head "The setting clears with a beep that carries."
  body: From the far end of the row, a parade-ground voice dictating
  into a phone: "Memo. When this is MY school, the gates open at
  oh-seven-hundred. So does the staff room."
- wrongLines[1]: head "Something in a control box resets with a clunk."
  body: Closer. "Item four. Staffroom biscuits: discontinued. Morale is
  not a biscuit."
- wrongLines[2] and [3]: unchanged.
- brief: in the paragraph "He is at the far end of the row, measuring
  one bay at a time and marching towards you. That is your fifteen
  minutes." insert between the two sentences: You hear him before you
  see him: "Those two bays differ by two point six centimetres. This is
  not how it is done in MY school."
  (brief is written raw, not through fill(): use real characters as the
  other raw slots do, and no figures — the number stays in words.)

EXACT CHANGE:
1. escape-rooms/car-trap/room.js: the wording above. Nothing else in
   the room changes.
2. Release, per docs/escape-room-voice-rewrite.md §5c's steps:
   a. escape-rooms/car-trap/index.html becomes the real room page
      (play.html's content, analytics ON, indexable, meta/og/Twitter
      from the draft's meta description). Delete play.html.
   b. Card back on escape-rooms/index.html and the front-page band in
      index.html (the draft's hub card line; topics Bounds · Arc length
      · Quadratics). Label it as the other cards are labelled today (the
      star scheme is the difficulty contract's; record ★★ in the
      handover only).
   c. <url> back in sitemap.xml.
   d. Room count: grep for the current count word (eight live rooms →
      nine) everywhere §5c lists, including BOTH front-page meta
      descriptions (same string, two hits). Do not add any replay
      figure to the hub (Jon, 17 Sep: the hub quotes no figure).
   e. teacher.html stays noindex; it may now be linked as the other
      rooms' teacher pages are.
3. check-escape-rooms.py, check-site.py and the escape-room browser
   tests pass; play the room once on the real URL (a wrong setting on
   the barrier must now show the memo line, not a verdict).
4. /updates/ entry, one line in the house style: Car Trap is back,
   rewritten, with a new antagonist. Jon may edit the wording.
5. PR; merge on green. Handover and canon §11.1 table: car-trap Live
   (date), antagonist Mr Strictman, ★★.

DO NOT TOUCH: every other room; engine.js, teacher.js, the checkers'
rules; the variants and locks; the art; the it-vengeance holding page
(The Rightful King's build handles that URL).

SUCCESS CONDITION: maffsgames.co.uk/escape-rooms/car-trap/ serves the
room; a wrong setting shows the memo line; the hub and front page show
nine rooms with Car Trap's card; sitemap includes it; play.html gone;
all checks green; main green after merge.

STOP IF: the count word is not "eight" (report what the live count is
before changing anything); any check needs a rule changed to pass.
