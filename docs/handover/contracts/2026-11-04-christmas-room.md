CONTRACT: CHRISTMAS-ROOM
Tier: Shared · Lane: home · Implementer: Codex (WSL)

START
git -C ~/maffsgames pull --ff-only, then a worktree codex/christmas-room from origin/main. Read canon §11,
docs/escape-room-voice-rewrite.md (§5c release list) and escape-rooms/kiln-disaster/room.js (the pattern) first.
Save this contract verbatim as docs/handover/contracts/2026-11-04-christmas-room.md in the first commit, with one
line in docs/handover/home.md's queue.

LANE EXCEPTION, THIS CONTRACT ONLY (Jon, 4 Nov): you may add escape-rooms/christmas-tree-fiasco/, edit
escape-rooms/index.html (one card), the front-page escape-room band in index.html (one card), sitemap.xml (one url),
escape-rooms/variants.json, scripts/gen-escape-variants.py and scripts/escape_set_checks.py (this room's three locks
only), docs/art/ (three pictures), /updates/ (one line) and the room counts named in §5c. Never docs/handover/cloud.md.

TASK
Build and release a new escape room, "The Christmas Tree Fiasco" (slug christmas-tree-fiasco), exactly as written in
the approved draft below, with its number libraries generated and checked like every other room.

ROOT CAUSE
New content (Jon, 4 Nov 2026): a seasonal, resit-level room for end-of-term lessons, to be live by the end of
November. Jon has approved the draft below (prose, locks, objects, hints, misconceptions, worked solutions, generator
rules). The draft is the source: do not rewrite its prose.

CLASS CHECK
Not a bug class: a new room on the existing engine, room.js pattern and generator, with no engine change. Every number
comes from gen-escape-variants.py through escape_set_checks.py (canon §11.3), never typed into prose.

EXACT CHANGE
1. escape-rooms/christmas-tree-fiasco/room.js on the Kiln Disaster pattern: minutes 15, penalty 45, art slug; hook,
   brief, stakes, win, wrongLines from the draft; the 8 objects with the draft's ids, names, where, clues (tokens as
   written) and blank flavours; three locks: ct (dial 0-24, step 1, grade 3), sc (keypad maxDigits 3, grade 3),
   cr (slider 0-40, step 1, grade 5), each with brief, instrument label, missTitle, missSays, three hints, solve and
   onOpen from the draft. sceneAlt, winAlt, failAlt from the draft's art section.
2. Number libraries: add the three locks to gen-escape-variants.py and escape_set_checks.py with the draft's generator
   rules, including the derived tokens (ct.rate, ct.rise; sc.tree, sc.total, sc.ccm; cr.r1, cr.r2, cr.r3, cr.parts,
   cr.each). The fixed decoys -18 (truck display) and 1.2 (hall plan) count as clue figures for the VALID rules: no
   answer or misconception may equal 18. At most 10 sets per lock; at least 20 VALID draws.
3. index.html and teacher.html for the room on the existing pattern (teacher page stays noindex); hub card and
   front-page band card with data-stars from the derived rating; sitemap url; /updates/ line in Jon's voice: "New escape
   room, just in time for the last lesson of term: The Christmas Tree Fiasco. Eric Ember, fire safety officer and
   Christmas's biggest fan, has entered the school into a competition for a brand-new tree. Negative numbers, scale
   and combined ratios, and a refrigerated truck nobody can explain."
4. Art: take christmas-tree-fiasco-{scene,win,fail}.jpg.jpg from the root of branch art/christmas-tree-fiasco; run
   scripts/strip-gen-watermark.py on each (no-op if clean); save as docs/art/christmas-tree-fiasco-{scene,win,fail}.webp
   (1600x873, q80). Check each yourself for lettering or people (house rule: none). Leave the art branch for Jon.
5. Room counts wherever §5c says.

DO NOT TOUCH
escape-rooms/assets/ (engine, teacher.js, rating.js, css); every other room and its variants; tools/pack-generator/
(the pack is a later contract); the draft's wording (report anything that does not fit a slot instead of rewording);
analytics; docs/handover/cloud.md.

SUCCESS CONDITION
check-escape-rooms.py passes with the new room (its VALID count printed); test-escape-dial.py, test-escape-keypad.py,
test-escape-setcodes.py and test-escape-rating.py pass; the room plays end to end at 390x844 and desktop with no
sideways scroll; rating ★★ Core everywhere; check-changed.py green; Gate green; stop for Shared review by Project
Claude and Jon's play-test and "merge"; committed, and home.md records the state with a Record line.

STOP IF
The art branch is missing or an image contains lettering or people; fewer than 20 VALID draws under the draft's rules
(report the count and which rule binds); any draft text needs a slot the engine lacks; a negative temperature cannot
be shown in a clue as written; a generator rule yields a set whose misconception equals its answer; main moves and the
branch conflicts (report; do not merge main in).

==================== THE APPROVED DRAFT (v3, Jon, 4 Nov 2026) ====================
Numbers shown are one example set (Set A); the generator makes the rest.

OPENING
Hook: Eric Ember is the fire safety officer, and Eric LOVES Christmas. So it nearly broke his heart to tape the
school's decorations into a box marked DO NOT USE: the tinsel is older than the Year 11s and the lights are held
together with tape. Nothing goes up in this school that could hurt a student. Not even at Christmas. Especially not
at Christmas.
Brief: So Eric entered the school into the Christmaffs Store's competition: a huge tree and every decoration, all
fire-safe. St Martha's has made the final, and goes first. The Christmaffs truck is already in the car park: the
prize goes home with the winner today. The final round is three puzzles about the prize itself. Fifteen minutes. Then
it's St Donald's turn, the private school up the road, and they already have a tree.
Stakes (timeout): The Christmaffs screen goes blank, then cheerful. "Thank you, St Martha's! Next up: St Donald's."
Outside, the Christmaffs truck pulls out of the car park. Eric closes the laptop very gently, and takes off his
Santa hat.
Win: The last puzzle clears and the Christmaffs screen fills with confetti. The tree is yours. Eric punches the air,
then gets his tape measure out. "Right. It needs to fit without blocking a single emergency exit. Nobody touch
anything till I've checked." He is humming a carol.

OBJECTS (8)
1 truck-display | Truck display | On the back of the Christmaffs truck | Two readouts. CHILLER ZONE {{ct.start}} °C ·
  FREEZER ZONE −18 °C | lock ct
2 eric-clipboard | Eric's clipboard | On the trolley by the door | Eric's handwriting. TREE COMES INSIDE AT
  {{ct.min}} °C OR WARMER. WARMS {{ct.g}} °C EVERY {{ct.h}} HOURS ONCE UNLOADED | lock ct
3 prize-leaflet | Prize leaflet | Pinned to the noticeboard | The Christmaffs Store's drawing of the prize tree.
  DRAWN TO SCALE 1 : {{sc.k}}. HEIGHT ON THIS PAGE {{sc.d}} cm. STAND ADDS {{sc.s}} cm | lock sc
4 hall-plan | Hall plan | Taped to the hall door | The caretaker's plan. HALL CEILING {{sc.c}} m · FIRE DOOR WIDTH
  1.2 m | lock sc
5 packing-slip | Packing slip | Stuck to the prize box | The prize list. BAUBLES : TINSEL = {{cr.a}} : {{cr.b}} ·
  TINSEL : CHRISTMAS UNICORNS = {{cr.c}} : {{cr.d}} | lock cr
6 sticky-note | Eric's sticky note | On the laptop lid | MAX {{cr.N}} DECORATIONS. FIRE LOAD. Underneath, smaller:
  There is no such thing as too much tinsel. | lock cr
7 old-box | Old decorations | In the corner, taped shut | (blank) A box marked DO NOT USE in Eric's capitals. Through
  the gap: tinsel gone grey, and a fairy with one wing.
8 laptop | Competition laptop | On the trolley | (blank) The Christmaffs Store's final, counting down. Below it, a
  little waiting icon: St Donald's.

LOCK ct — The cold store (dial, hours, 0-24 step 1) · grade 3
Brief: The Christmaffs driver opens the truck to show off the prize. Eric stares at it. "Who freezes a Christmas tree?
It's just wrong. We need to warm it before we take it inside." First puzzle: how many hours before the tree would be
warm enough for Eric to let it in?
Label: HOURS UNTIL THE TREE CAN COME IN
Set A: start −4 °C, minimum 16 °C, warms 8 °C every 2 hours (4 °C an hour): 16 − (−4) = 20; 20 ÷ 4 = 5 hours.
missTitle: That's the gap from 4 °C, not from −4 °C.
missSays: It starts below freezing. Count up to zero first, then keep going.  (miss: (16 − 4) ÷ 4 = 3)
Hints: 1. The tree has to warm from its starting temperature up to Eric's minimum. 2. From −4 °C to 16 °C is further
than 12 degrees: count through zero. 3. Find the warming per hour first, then divide the total rise by it.
Solve: {{ct.g}} °C every {{ct.h}} hours is {{ct.rate}} °C an hour. {{ct.min}} − ({{ct.start}}) = {{ct.rise}}.
{{ct.rise}} ÷ {{ct.rate}} = <b>{{ct.answer}}</b> hours.
onOpen: The dial clicks round. Eric ticks a box on his clipboard, and draws a tiny star next to it.
Rules: start −2 to −9; minimum 8 to 20 and bigger than the size of the start; rate 2, 3 or 4 °C an hour, given as g
every h hours (h = 2 or 3); answer whole, 3 to 12; miss = (min − |start|) ÷ rate, whole, positive, not the answer;
the −18 decoy must not give a whole-number result equal to the answer or the miss.

LOCK sc — Will it fit? (keypad, cm, maxDigits 3) · grade 3
Brief: Second puzzle: Eric needs to know how much room there would be between the top of the tree, on its stand, and
the hall ceiling. In centimetres.
Label: GAP UNDER THE CEILING (cm)
Set A: 9 × 50 = 450 cm; + 30 cm stand = 480 cm; ceiling 7 m = 700 cm; 700 − 480 = 220 cm.
missTitle: That's the tree without its stand.
missSays: The tree doesn't float. Read the leaflet again.  (miss: 700 − 450 = 250)
Hints: 1. Scale 1 : {{sc.k}} means every centimetre on the page is {{sc.k}} cm in real life. 2. The stand goes under
the tree, so it adds to the height. 3. The ceiling is in metres: change it to centimetres before you subtract.
Solve: {{sc.d}} × {{sc.k}} = {{sc.tree}} cm. {{sc.tree}} + {{sc.s}} = {{sc.total}} cm. {{sc.c}} m = {{sc.ccm}} cm.
{{sc.ccm}} − {{sc.total}} = <b>{{sc.answer}}</b> cm.
onOpen: Eric writes the number down twice, then underlines it. "Room for the star. Lovely."
Rules: scale 1 : 20, 25 or 50; drawing 6 to 12 cm; stand 20 to 40 cm (multiple of 5); ceiling 5 to 9 m (whole or .5);
answer 50 to 400 cm; miss = gap without the stand.

LOCK cr — The final puzzle (slider, unicorns, 0-40 step 1) · grade 5
Brief: The final puzzle. The prize comes with baubles, tinsel and Christmas unicorns in fixed ratios, and Eric's fire
limit is the total. How many Christmas unicorns?
Label: CHRISTMAS UNICORNS
Set A: 3 : 2 and 4 : 1 → 6 : 4 : 1, 11 parts; 66 ÷ 11 = 6 a part; unicorns 6.
missTitle: The tinsel doesn't match up.
missSays: Tinsel is {{cr.b}} in one ratio and {{cr.c}} in the other. Make them the same before you join them.
(miss: unjoined 3 : 2 : 1, 66 ÷ 6 = 11)
Hints: 1. Both ratios mention tinsel. 2. Scale one ratio so the tinsel number is the same in both. 3. Join them into
one three-part ratio, add the parts, and share Eric's total.
Solve: {{cr.a}} : {{cr.b}} and {{cr.c}} : {{cr.d}} give {{cr.r1}} : {{cr.r2}} : {{cr.r3}}, {{cr.parts}} parts.
{{cr.N}} ÷ {{cr.parts}} = {{cr.each}}. Unicorns: {{cr.r3}} × {{cr.each}} = <b>{{cr.answer}}</b>.
onOpen: The Christmaffs screen fills with confetti.
Rules: the tinsel numbers differ; combined total 8 to 15 parts; N = parts × 2 to 8; answer 2 to 36; miss = N shared
in the unjoined ratio, whole and not the answer (drop sets where it isn't whole).

WRONG-ENTRY LINES (escalating; the last repeats)
1. head: Eric is humming "Jingle Bells". He stops. body: "Not yet. Check it again. Carefully. Careful is how Christmas
   happens."
2. head: He glances at the laptop. body: "St Donald's have a twelve-foot tree already. I've seen the photos." He sighs.
   "Fire-checked, I hope."
3. head: He pats the DO NOT USE box. body: "I had to ban that fairy. I loved that fairy. But I love you lot not being
   on fire more."
4. head: The countdown is in red now. body: "There is no such thing as too much tinsel. There is such a thing as too
   little time."

ART ALT TEXT
sceneAlt: A bare school hall in December. An empty Christmas tree stand in the middle of the floor, a box taped shut
with hazard tape in the corner, and a laptop on a trolley with a Santa hat beside it. Through the glass doors, a white
refrigerated truck is parked with its doors shut.
winAlt: The same hall with a huge decorated Christmas tree on the stand, hung with baubles, tinsel, lights and small
unicorn ornaments. A yellow tape measure is unrolled across the floor in front of it.
failAlt: The hall still bare in the evening, the empty stand and the taped box. The laptop is closed with a Santa hat
on it. Outside in the falling snow, the white truck is driving away, its tail lights glowing.

AMENDMENT 1 to CHRISTMAS-ROOM (Jon, 4 Nov): lock ct's text must follow the drawn set (canon §11.3).
- Add two derived tokens to lock ct: ct.abs = the size of the start temperature (4 for -4), and ct.short =
  ct.min - ct.abs (the wrong-sign gap; 12 in Set A).
- missTitle becomes: "That's the gap from {{ct.abs}} °C, not from {{ct.start}} °C."
- Hint 2 becomes: "From {{ct.start}} °C to {{ct.min}} °C is further than {{ct.short}} degrees: count through zero."
- No other wording changes. Record this amendment verbatim in the saved contract and the PR body. Thank you.

AMENDMENT 2 to CHRISTMAS-ROOM (Jon, 4 Nov): two more files in scope.
- docs/lock-bank-batch13.txt: add the three lock-bank entries for ct, sc and cr, in the file's existing format, taken
  from the approved draft and Amendment 1 (no new wording or rules).
- docs/audits/findings/christmas-tree-fiasco.yml: create it in the format SR-30 requires for a new room. Record only
  facts from this build; any field that needs a judgement (a verdict or severity) is marked for Project Claude's
  review rather than decided here.
Record this amendment verbatim in the saved contract and the PR body. Thank you.

AMENDMENT 3 to CHRISTMAS-ROOM (Jon, 5 Nov): scripts/checker-allowlist.json, tier1_phone_overflow: add one entry, in
the file's existing format: path escape-rooms/christmas-tree-fiasco/teacher.html, at load, width 541, todo §1.37,
where "table.tt; table.tt". No other change.

AMENDMENT 4 to CHRISTMAS-ROOM (Jon, 5 Nov): lock cr's two given ratios must each be in simplest form (gcd of a and b
is 1, gcd of c and d is 1); no clue may print a ratio like 2 : 2 or 4 : 2. Add this to the generator rule and
escape_set_checks.py, regenerate cr's library, and re-run check-escape-rooms.py, the play-through and your
independent recomputation. All other rules unchanged. STOP IF VALID falls below 20 (report the count).
