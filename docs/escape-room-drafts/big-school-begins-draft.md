# Big School Begins: draft for Jon’s review

**Phase 1 of the transition-day room (contract BSB-ROOM-DRAFT, 16 Oct 2026; saved as
`docs/handover/contracts/2026-10-16-bsb-room-draft.md`).** Draft prose only. There is no `escape-rooms/`
directory for this room, and nothing served is touched. Phase 2 (the build, the variants, the shared-code
exceptions, the teacher page, the release) is a separate contract after you approve this, and the art comes
after the build (Project Claude writes the prompts).

The room is built under the house process: `docs/escape-room-voice-rewrite.md`, canon §11 and the format of
`docs/escape-room-drafts/dnd-club-draft.md`, with the parameter sets laid out as in
`docs/escape-room-drafts/library-draft.md`.

How to read it:

- `{{key.token}}` is a figure filled from the drawn variant. There are no other figures in the prose; numbers
  written as words are listed in the checklist at the end.
- Prose is shown with real quotation marks and apostrophes. In phase 2 they become entities in every slot except
  the object and lock `name` and `where`, which keep real characters (canon §11.3).
- **[X]** marks a detail I extrapolated rather than took from your brief. Strike any you don’t want.
- Four token keys: `map` (A, the hall), `dir` (B, the library), `tt` (C, the corridor), `till` (D, the canteen).

---

## For Jon: decisions in this draft

Items 1 and 2 are places where your brief meets a standing rule. The draft resolves both without breaking either,
so neither is a STOP, but both are yours to overrule. Items 3 to 5 are the [X] proposals the contract asks for.
Items 6 to 10 are the contract’s a to e. The rest I found while drafting.

1. **SR-11 (age-neutral wording) and the year groups in your brief.** SR-11 (canon §0.3): *“Start screens and
   other student-facing copy carry no year-group or key-stage wording (no ‘Year 7’, ‘primary’, ‘secondary
   school’ …).”* Your brief: *“a nervous new Year 6 from another primary”*, *“Daisy Reddington, Year 7 buddy”*,
   and the label *“Year 6/7”*.
   - **How the draft resolves it:** the label is your named exception (ruling 1), and the contract already
     records it for canon. Everything else keeps SR-11. The prose never says Year 6, Year 7, primary or secondary.
     William “has come from a school none of the rest of you went to”; Daisy “started here last September”; the
     players are visiting “the school you start at in September”. The premise still reads clearly as a transition
     day without naming a year group.
   - **Two things the exception has to cover as well, for the home lane’s canon entry:** the title (“big school”
     is the colloquial name for secondary school, and the title is on every student surface), and “Year 6/7” on
     the hub and front-page chips as well as the start screen. The meta description and hub line below carry no
     year group, so the exception does not need to reach them.
   - If you would rather the prose said “Year 7 buddy” outright, it is one phrase in the hook, but it widens the
     exception from a label to student copy.

2. **Bibby already speaks in The Library Jam.** The working doc’s rule (§4): *“Characters may recur offstage
   across rooms, but each speaks only in their own room.”* Your brief: *“she sets challenge B”*.
   - **How the draft resolves it:** she sets it in writing. She hands over a card of directions in very neat
     capitals (the Library Jam memo’s “AGAIN, in very neat capitals” is hers too), and everything else she does is
     narrated, never quoted: the Mr Strictman precedent in Roll for Initiative, recognised and never heard. She is
     stern and precise, and the one kindness she shows is the one Library Jam gave her: she makes an exception for
     a bookworm, and lets William stay in the reading corner. **[X]**
   - If you want her to speak, it is your rule to set aside for her; say so and I will give her one line.

3. **[X] The clock (contract item 2): the hunt ends at the lunch bell.** Every group reports back for lunch, so the
   clock is something every student in the room can feel. The penalty is reskinned: Daisy sends you back to look
   again, and the hall clock doesn’t wait. **One knock-on, already handled:** your range for lock C starts lessons
   from ten o’clock to half past two, but a lesson that starts after lunch cannot sit inside a hunt that ends at
   lunch. So all ten of C’s sets start between ten and half past eleven (inside your range, so no ruling is
   broken). If you rule a different clock, afternoon starts can be added back; the full range has thousands of
   candidate sets and every one passes the per-set checks.

4. **[X] The ending (contract item 2): everyone at one canteen table, William included.** Written as you gave it,
   in “Win”. Daisy’s last line is “Same table in September?” and William says yes first. **[X]**

5. **[X] The fail (the `stakes` slot, which is also the time-out screen).** There is no `fail` slot in `room.js`:
   the engine shows `stakes` after “If you get it wrong.” on the start screen and after “And so:” at time-out
   (Car Trap and Roll for Initiative did the same). The draft’s fail mirrors the ending: the hunt ends with boxes
   blank, the group is split across a full canteen, and William eats at the end of a table of strangers.
   - **I want to flag the tone.** The canon rule wants a failure that matters to the students, and this is
     the one the brief makes matter: helping a fellow new student. But the audience is about to make this move
     themselves, and some of them are anxious about exactly this picture, on the start screen as well as at
     time-out.
   - **A gentler alternative, if you prefer it:** “The lunch bell goes and the hunt is over, with boxes still blank
     on the card. Your group eats at the last table left, a seat short, and William finds you there late, walked
     over by a teacher on lunch duty.” It still costs something, and nobody is left alone.

6. **(a) Object count: eight objects, six clues and two blanks.** Four locks share six clues, which is the
   number the two-blank minimum leaves. A has one (the map); B two (the compass rose, Bibby’s card); C one
   (William’s timetable); D two (the tray, the lunch card). The blanks are the lost property box and Bibby’s
   returns trolley. **Why not more clues:** a ninth object is possible (nothing in canon caps the count at eight),
   but every object is a tap on a phone, and four locks in twenty minutes already ask more of a group than three in
   fifteen. I would keep eight.

7. **(b) Theme. The contract says canon §7.5.1 makes a Year 6 room light and playful. That is not what canon now
   says, and I think you should know that before deciding.**
   - **What canon says.** §7.5 (your ruling of 2 Oct 2026) *replaced* the “light/playful Nunito + Press Start 2P
     for KS3” row with one adult register for every game: *“A Year 7 loses nothing by being spoken to as an adult
     … The fun comes from the mechanic, not the font.”* Its palette rule makes a **game** light if its levels
     include Year 6, KS3 or GCSE. “Playful” is no longer in canon anywhere. §7.5.1 is how `check-theme.py` checks
     roster games, and escape rooms are not on the roster.
   - **What the rooms do today.** `escape-rooms/assets/engine.css` has one dark palette and no `data-theme`. Every
     room is dark, including the KS3 and GCSE rooms the game rule would make light (Hamster Heist, Canteen Hack,
     Library Jam among them). The fonts are already the register (Outfit, JetBrains Mono).
   - **What “light” would need (phase 2, home lane; nothing changed here):** a light token set in `engine.css`
     under `:root[data-theme="light"]`, the shape `schools/assets/theme.css` already uses. The room’s
     `index.html` and `teacher.html` would carry the attribute. Then the hard-coded colours need moving onto
     tokens: `engine.css` has nine literals outside `:root` (`#11131a` four times: the accent button’s text, the
     active Aa toggle’s text and the two slider thumbs’ borders; `#fff` on the penalty flash; one `rgba` overlay;
     and `#fff`, `#000` and `#999` in the print styles, which can stay), and `engine.js` draws the dial wedge in a
     literal `rgba(245,165,36,0.18)`. Then contrast checks on the start, play and end screens, and on the teacher
     page.
   - **My recommendation:** do not make this one room “playful”. That reverses your 2 Oct ruling for the very
     audience whose reasons you gave in it. Light or dark is a set-wide question: either apply the palette rule
     to rooms as it applies to games (derived, never chosen, so the KS3/GCSE rooms go light too), or keep this
     room dark like the other eleven. A single light room makes the palette a per-room choice, which §7.5 exists
     to prevent. Either way it is a design change, which is on canon’s “Still stops for Jon” list.

8. **(c) How “Year 6/7” replaces the stars (proposal; rating.js, the hub chip and `check-escape-rooms.py` are
   shared, so this is phase 2, home lane).**
   - **The lock grades stay** (item 9), so the derived rating still exists, and still decides the hub’s
     “easiest to hardest” order and the teacher page. A new optional room-level field, say
     `label: 'Year 6/7'`, replaces the stars on the **student** surfaces only.
   - **`rating.js`:** `html(r, room)` renders the label where the room has one:
     `<span class="rating" data-label="year6-7"><span aria-hidden="true">Year 6/7</span><span class="sr-only">For
     Years 6 and 7</span></span>`. `rating(room)` is unchanged, so the start screen keeps its one call.
   - **Hub and front-page cards:** the chip carries `data-label="year6-7"` and the label text in place of
     `data-stars`. `check-escape-rooms.py`’s `check_ratings` accepts a card whose label matches the room’s, fails
     one that shows stars when the room has a label (or the reverse), and still orders by the derived rating (★
     Warm-up, so the room sits among the first cards). Its planted faults gain one: a label on the wrong card.
   - **Teacher page:** shows both (“Year 6/7 · ★ Warm-up, grades 1–3”). It is a teacher surface, so SR-11 does
     not reach it, and a teacher filtering by difficulty still gets the scale every other room uses.
   - `test-escape-rating.py` gains the label case. Canon §11.3 records it as this room’s exception, not a second
     scheme.

9. **(d) Grades and level, as the build needs them.** Every lock is **grade 1**: first-quadrant coordinates;
   turns in eighths of a whole turn; durations across the hour on the 24-hour clock; change from five pounds with
   exchanges across zeros. All four are KS2 skills, and grade 1 is the floor of the scale (there is no grade 0),
   so the derived rating is **★ Warm-up, grades 1–3**, and the label shows instead of it (item 8). The room’s
   `level` (analytics only; the engine sends it with every event) I propose as **`'year6'`** **[X]**: an
   existing key the dashboard already knows, and the youngest of the two audiences. A new key such as `'year6-7'`
   is allowed (keys are added, never changed, SR-11), but I don’t know what the dashboard does with a key it has
   never seen, so I would not risk it. `minutes: 20` and `penalty: 45` are data the engine already reads
   (`engine.js` lines 38 and 39); four locks need no engine change, since it counts `R.locks.length` throughout.

10. **(e) Lock B’s dial: yes to `sweep: 360`, and I recommend `wedge: true` with it [X].**
    - Without `sweep: 360`, a dial spreads its range over 270° (`dialAngle()`, `engine.js` line 543), so a setting
      of 90 puts the needle about 68° *anticlockwise* of the top. On a lock whose skill is “a quarter turn
      clockwise”, the instrument would draw the misconception. With `sweep: 360` the needle points where the turn
      goes, and the dial teaches the turn instead of contradicting it.
    - 0 and 360 both sit at the top, and neither is ever an answer or a misconception, so a student who lands on
      either gets an ordinary wrong entry. **Max must stay 360:** with max 315, a 315 answer would sit at the end
      of the travel and `check_set` rejects it.
    - `wedge: true` shades the sector from the top to the needle, clockwise (`paintDial()`, as P.E. Store’s arc
      uses). It is a picture of the turn, not of the answer. Strike it if you think it helps too much.
    - **One cosmetic gap (shared code, not proposed here):** the dial’s ticks are every 10°, with a major one
      every 30° (`dialSVG()`), so the 45°, 135°, 225° and 315° settings fall between ticks. It works, but a tick
      at each compass point would read better. That is an `engine.js` change for the home lane if you want it.

11. **The engine shows all four cards at once, in any order.** There is no gating (`renderLockBtns()`), so a
    group can do the canteen first. Every brief and onOpen is written to stand on its own: William is found at
    each stop in a way that doesn’t assume the stop before (he “drifted off” to the map, “slipped away” to the
    library, is collected from his lesson and is beside you at the till). One seam is left: lunch is the card’s
    last stop and William’s lesson ends before it, so a group that does the canteen first meets the two out of
    order. Nothing on screen contradicts itself, and gating would be an engine change, so I have left it. The
    lock names are places, not “card one” to “card four”, so nothing on screen implies an order the engine
    doesn’t keep.

12. **The hub and the front page will say something false when this room ships.** The hub’s lede and meta say
    “three locks each, fifteen minutes a room”; the front page says “Three locks a room”, “15 minutes a room” and
    “under 15 minutes each”, and its meta says “15-minute escape rooms”. Canon §11 says the same. That copy is a
    public claim (canon’s “Still stops for Jon” list, and “start screens and cards state what the code does”),
    so the release contract needs your wording, for example “most rooms fifteen minutes”. It is not touched here
    (DO NOT TOUCH).

13. **Wrong-answer feedback on a reversal (A and B).** Your rule of 15 Oct is that feedback never gives the
    answer. Locks A and B are built round a reversal (y then x; anticlockwise), and for a reversal, naming the
    mistake *is* one step from the answer: “you swapped them” hands over the code. So Daisy’s A and B lines tell
    her own story and the rule of thumb (“along the corridor, then up the stairs”; “the way a clock’s hands go”)
    without saying “you swapped them” or printing a reversed code. The student still has to go back to the map or
    the rose and apply the rule. C and D are not reversals, so their lines can be plainer about the mistake
    without risk. If you think the A and B lines still give too much away, the fallback is the general sentence
    with no rule of thumb, which is weaker teaching.

14. **The map clue gives “up” before “along” on purpose [X].** If it said “along, then up”, a student who
    doesn’t know the convention would read the code off in order and be right by luck. Up first is how the
    misconception actually happens, so the lock tests the convention, which is the skill.

15. **Lock D is “left on the card”, not “change”.** A lunch card gives no change: the till keeps what is left on
    the card. The maths is the same subtraction from five hundred pence. The card’s value is written “five
    pounds” in words, the Library Jam “half past three” precedent. A numeral there would be a clue figure, and
    measured, it costs 650 of the 5,710 VALID draws (it collides with C’s “11:05”-type start times). If you want
    “£5”, the pot still has 5,060.

16. **One extra check for lock D (for phase 2’s `LOCKS` entry).** `check_set` compares the answer with the
    figures a clue *prints*, and a price under the £ sign prints as a decimal (£1.25 prints 1.25). One of my
    first sets had orange juice at £1.25 with an answer of 125p, and `check_set` passed it; a student would have
    seen the answer on the tray. I replaced the set (the table below has the fix). Phase 2’s `clue_numbers` for
    this lock should return each price in pence as well as in its printed form, so the check catches it next time.

17. **William’s name.** No line plays on it. The words tremble, trembling, shake, shaking, shiver, quiver, quake
    and wobble appear nowhere in the room, about him or anyone (Daisy never “shakes her head”). He is named in
    full once, in the hook, and is “William” after that. He is never laughed at; the one joke near him is
    Daisy’s, about herself, and he gets the room’s last word.

18. **Calculator: not needed, and the teacher page should say so.** Every lock is mental or written KS2
    arithmetic, the Kiln and Library standard.

19. **Lock A marks a point, not a square.** The brief says “grid reference” and “coordinates”. In KS2 maths,
    coordinates name a point where two grid lines cross; numbered squares are a geography grid reference. The
    across-first rule is the same in both, but a struggling student should meet the maths version, so the map
    numbers its grid lines and draws the library where two of them cross. My first wording numbered squares; I
    changed it before sending this.

---

## Title

**Ruled by Jon, 16 Oct 2026: Big School Begins.** Slug proposed `big-school-begins` (phase 2).

## Room fields (phase 2 writes them; listed so nothing is missed)

- `slug: 'escape-big-school-begins'`, `title: 'Big School Begins'`, `level: 'year6'` **[X]** (item 9)
- `minutes: 20`, `penalty: 45` (ruling 2: named exceptions for this room only)
- `label: 'Year 6/7'` (ruling 1; a new field, item 8; phase 2 only once the home lane has built it)
- **No `art` field** until the three pictures are filed (contract ART-PENDING, CLAUDE.md): the engine then
  requests no scene, fail or win picture. `sceneAlt`, `failAlt` and `winAlt` are below as **provisional** text,
  to be rewritten against the pictures.

## Hook

It’s transition day at St Martha’s: the day you come and see the school you start at in September, and find out
it is much, much bigger than the one you are leaving. You arrived this morning as a crowd of strangers in new
shoes. By now you have been put in a group, handed a clipboard each and given a buddy: Daisy Reddington, who
started here last September and still remembers exactly what it felt like.

There is one more of you. William Trembles has come from a school none of the rest of you went to. He knows
nobody, says almost nothing and holds his clipboard with both hands. The building is a lot bigger than he is used
to, and it keeps swallowing him.

“Everyone gets lost,” Daisy says. “I got lost in the canteen. The canteen is one room.” **[X]**

## Brief

Daisy explains the hunt. There are four stops, a clue card for each, and the whole school to find them in. Every
card has a box for the answer. Daisy has the answer sheet, and when she ticks a box, that stop is done. She says it
isn’t a test, and then admits she got every card wrong when she did it.

There is one rule she is strict about: a group finishes together, or it doesn’t finish. **[X]**

The hunt ends when the lunch bell goes. **[X]** Every wrong answer costs you time: Daisy sends you back to look
again, and the clock in the hall doesn’t wait.

## Stakes (also the time-out screen; see “For Jon” 5) [X]

The lunch bell goes and the hunt is over, with boxes still blank on the card. By the time you find the canteen the
tables have filled up, and your group ends up split across the room. William is at the end of a table of people he
doesn’t know, eating his lunch without looking up. Daisy says everyone gets lost on their first day. She’s right.
It doesn’t make it feel any better.

*(Read after “If you get it wrong.” on the start screen and after “And so:” at time-out; both work. No tokens:
the engine writes this slot raw.)*

## Win [X: the shape is the contract’s proposal; the details are mine]

The lunch bell goes, and every box on the card has a tick in it. Daisy finds a table by the window big enough for
all of you, and you all sit down at it: William too, between two people he hadn’t met this morning, eating and,
for the first time today, talking.

Daisy hands in the card and sits down at the end.

“Same table in September?” she says.

William says yes first.

---

## wrongLines (four, escalating; the last repeats)

There is no antagonist (ruling 3), so the wrong-entry voice is an ally’s, the Kiln precedent (Mr Mudge). Each
`head` is the hunt going on around you; each `body` is Daisy remembering her own first weeks. None is about the
maths (her maths mistakes are the misconception lines, on each lock), and none is about William or the students.

1. **head:** Daisy checks her sheet and pulls a face. Not that one.
   **body:** “Don’t worry. On my first day I walked into the staff room looking for the toilets. Twice.”
2. **head:** A bell goes somewhere. The corridors fill up, then empty again.
   **body:** “In my first week I followed a really tall student for ages, because I thought he knew where he was
   going. He was lost too.”
3. **head:** The clock in the hall is further on than you’d like.
   **body:** “Honestly, everybody gets these wrong at the start. Everybody. Ask anyone at lunch.”
4. **head:** Daisy crosses something out, and smiles anyway.
   **body:** “Deep breath. Read it again.”

*(Line 4 repeating is the kindest version of the house joke: she says it every time, and means it every time.
Remember that a misconception hit uses up a line without printing it, so a group that makes only the named
mistakes skips some of these.)*

---

## Objects (eight: six clues, two blanks)

Clue objects get the ids below; `teacher.html` maps clues to locks by `id`, and phase 2 writes that map from this
table. The two blanks are `lost-property` and `trolley`. No numeral is typed into any clue; the only clue figures
are tokens (the Kiln rule, working doc §5i).

| # | id | name | where | clue or flavour |
|---|---|---|---|---|
| 1 | `map` | The school map | on an easel by the stage in the hall | A big map of the whole school, every building drawn on a grid. The grid lines are numbered along the bottom and up the side, counting from the bottom-left corner. The library is the little open book, drawn where two grid lines cross: **{{map.y}} up** and **{{map.x}} along**. *(“For Jon” 14: up before along, on purpose; 19: a point, not a square.)* |
| 2 | `rose` | The compass rose | set into the library carpet | Set into the carpet in front of the desk: north at the top and then, going round clockwise, north-east, east, south-east, south, south-west, west and north-west. **[X]** |
| 3 | `bibby-card` | Bibby’s directions | on a card she slides across the library desk | In very neat capitals: **FACE {{dir.fromU}}. YOUR NEXT STOP IS {{dir.toU}}. TURN CLOCKWISE.** Signed B. PHILE, and underlined once, exactly. |
| 4 | `timetable` | William’s timetable | clipped to his clipboard | TASTER LESSON: SCIENCE **[X]**. Starts at **{{tt.start}}**. Lasts **{{tt.m}} minutes**. Underneath, in a teacher’s writing: *please collect from the lab door when the lesson ends*. |
| 5 | `tray` | William’s tray | in the canteen queue | On the tray: {{till.i1}}, **{{till.p1}}**; {{till.i2}}, **{{till.p2}}**; and {{till.i3}}, **{{till.p3}}**. Every price is on a sticker. |
| 6 | `lunch-card` | William’s lunch card | in his hand, held out to the till | LUNCH CARD. Topped up this morning with **five pounds**. The till takes off what lunch costs and keeps the rest on the card. *(“For Jon” 15.)* |
| 7 | `lost-property` | Lost property | a box by the hall doors | *(blank)* Odd socks, one football boot, a recorder, and a coat that has been here so long it looks like part of the furniture. Nobody ever comes back for anything. **[X]** |
| 8 | `trolley` | The returns trolley | beside the library desk | *(blank)* Every book on it spine out, in order, and level with the edge of the shelf. Nobody would dare put one back wrong. **[X]** *(A nod to The Library Jam; Bibby doesn’t speak.)* |

---

## Locks

Three keypads and a dial; no instrument art (set-wide) and no `missArt` on any lock (the fail is the lunch bell,
true only at time-out: the Kiln and Comic rule). **Every lock grade 1** (“For Jon” 9). Each `missSays` is Daisy’s
own past mistake, opening “When I started”, your pattern (ruling 5); none prints the answer or the code reversed
(“For Jon” 13). Hint ladders are general (every group sees them, so none assumes a particular mistake), and none
prints a worked figure. The worked `solve` appears only on a solved lock’s panel, on the end screen and on the
teacher page.

### Lock A: the hall map (coordinates, first quadrant)

- **id:** `school-map-coordinates` (proposed) · **key:** `map` · **grade:** 1
- **name:** The hall map
- **brief:** Daisy’s clue card for the hall says: FIND THE LIBRARY ON THE MAP. WRITE ITS COORDINATES AS A
  CODE: NO BRACKETS, NO COMMA. The map is on an easel by the stage, and every group in the hall is crowded round
  it. **[X]**
- **instrument:** keypad · **label:** LIBRARY: COORDINATES AS A CODE · `maxDigits: 2` · **verb:** Write it in
- **missTitle:** Daisy has seen this one before.
- **missSays:** “When I started, I read the grid backwards. What fixed it for me was: along the corridor, then up
  the stairs.” *(The first sentence is your example line, ruling 5.)*
- **hints:**
  1. Find the little open book on the map, and the two grid lines that cross where it is drawn.
  2. Coordinates always go across first, then up.
  3. The code is the two coordinates written next to each other, with no brackets and no comma.
- **solve:** The library is where grid line {{map.x}} along crosses grid line {{map.y}} up, so its coordinates
  are ({{map.x}}, {{map.y}}): across first, then up. The code is **{{map.answer}}**.
- **onOpen:** Daisy ticks the box: the library, found. At the edge of the crowd, standing much too close to the
  map, is William. He drifted off to look for it on his own and got as far as the map. When you call him, he
  comes.

**Pot for lock A (proposals only; `gen-escape-variants.py` and `escape_set_checks.py` are not touched).** Your
constraints: x and y from 1 to 9, x ≠ y; answer 10x + y, misconception 10y + x. **Added [X]:** no 5 in x or y,
and no x of 1. Those two rules mean no A answer or misconception ends in 0 or 5, and no A answer falls in C’s hours
(10 to 14). Every other lock’s answers, misconceptions and clue figures either end in 0 or 5, have four digits,
or are C’s hours, and A’s own clue figures are single digits other than 5, so **lock A collides with nothing in any
draw** (the scratch run confirms it for this pot: A is in none of the INVALID draws). No two sets are each
other’s reversal (37 and 73 are never both in the pot).

| # | x (along) | y (up) | answer, x then y | miss, y then x |
|---|---|---|---|---|
| 0 | 3 | 7 | **37** | 73 |
| 1 | 6 | 2 | **62** | 26 |
| 2 | 8 | 4 | **84** | 48 |
| 3 | 2 | 9 | **29** | 92 |
| 4 | 4 | 6 | **46** | 64 |
| 5 | 9 | 3 | **93** | 39 |
| 6 | 7 | 1 | **71** | 17 |
| 7 | 6 | 8 | **68** | 86 |
| 8 | 2 | 4 | **24** | 42 |
| 9 | 4 | 9 | **49** | 94 |

Generator rules: keypad, up to two digits; tokens `x`, `y`, `answer`, `miss`. Solver
`lambda x, v: x == 10 * v["x"] + v["y"]`; `clue_numbers` `[x, y]`. The full space under your two constraints is 72
sets, all of which pass `check_set`; with my two added rules, 49 remain. Variant 0 is my choice **[X]** (your brief
gave no example for A).

### Lock B: Bibby’s directions (turns in degrees)

- **id:** `library-compass-turn` (proposed) · **key:** `dir` · **grade:** 1
- **name:** Bibby’s directions
- **brief:** The library is silent, and Mrs Barb Phile, the librarian, whom every student calls Bibby, intends to
  keep it that way. She does not give directions out loud. She writes them on a card, slides it across the desk
  and goes back to her shelves. You find William in the reading corner with a book: he slipped away from the
  group looking for somewhere quiet, and Bibby, who will make an exception for a bookworm, has let him stay.
  **[X]** Stand on the compass rose and set the dial to the turn on her card.
- **instrument:** dial · **label:** TURN CLOCKWISE · **unit:** ° · min 0, max 360, step 45, 0 decimals, starts at
  0, `sweep: 360`, `wedge: true` **[X]** · **verb:** Turn (“For Jon” 10)
- **missTitle:** Daisy looks at the dial, then at the compass rose.
- **missSays:** “When I started, I turned the wrong way round, every single time. Bibby’s card says clockwise.
  That’s the way a clock’s hands go. Stand on the rose and try it.”
- **hints:**
  1. Stand facing the way the card says, then turn the way a clock’s hands go until you face your next stop.
  2. A whole turn is {{dir.whole}}°. There are eight compass points round the rose, so each step from one point
     to the next is {{dir.eighth}}°.
  3. Count the steps clockwise from where you face to your next stop, then multiply by {{dir.eighth}}.
- **solve:** From {{dir.from}} to {{dir.to}} is {{dir.steps}} steps clockwise round the rose. Each step is
  {{dir.eighth}}°, so the turn is {{dir.steps}} × {{dir.eighth}} = **{{dir.answer}}°**.
- **onOpen:** You turn, and there is the door to the science corridor, exactly where the card said. Bibby does not
  look up, but she lets William take the book with him. He marks his page and comes with you.

**Pot for lock B.** Your constraints: from and to two of the eight points; answer the clockwise turn, a multiple
of 45 from 45 to 315, never 180; misconception 360 − answer. There are only **six distinct answers** (45, 90, 135,
225, 270, 315) across 48 possible sets, so the pot repeats answers from **different starting directions**. Each of
the eight points is the start once. That is the Library Jam lock-A precedent, the spread rule set aside for this
lock. Every answer appears at least once.

| # | face (`from`) | next stop (`to`) | steps clockwise | answer | miss, anticlockwise |
|---|---|---|---|---|---|
| 0 | south | west | 2 | **90°** | 270° |
| 1 | north | north-west | 7 | **315°** | 45° |
| 2 | north-east | north-west | 6 | **270°** | 90° |
| 3 | east | south-west | 3 | **135°** | 225° |
| 4 | south-east | north | 5 | **225°** | 135° |
| 5 | south-west | west | 1 | **45°** | 315° |
| 6 | west | north | 2 | **90°** | 270° |
| 7 | north-west | south-west | 6 | **270°** | 90° |

Generator rules: dial (0, 360, 45), `sweep: 360`; tokens `from`, `to` (lower case, for the solve), `fromU`, `toU`
(capitals, for her card), `steps`, `answer`, `miss`, and the constants `whole` (360) and `eighth` (45), carried
as tokens as Library Jam carries `half`. Solver: `x == ((POINTS.index(to) − POINTS.index(from)) mod 8) × 45`, one
setting on the grid by construction; `clue_numbers` `[]` (the card prints words only). Every answer is between
45 and 315, clear of the end-of-travel margin (4% of the range, 14.4°) at each end of a 0 to 360 dial. Variant 0 is my choice **[X]**, and was picked
so that variant 0 is a VALID draw (an earlier pick, 135°, shared its answer with D’s variant 0).

### Lock C: William’s lesson (durations across the hour)

- **id:** `taster-lesson-end-time` (proposed) · **key:** `tt` · **grade:** 1
- **name:** William’s lesson
- **brief:** William’s card has something the rest of yours don’t: a taster lesson, on his own, in a lab he has
  never seen. **[X]** He has gone in. Your clue card says to be at the lab door the moment the lesson ends, so
  nobody walks off without him. Write down when that is. The keypad has no colon, so type the four digits of the
  time on the twenty-four-hour clock.
- **instrument:** keypad · **label:** LESSON ENDS (NO COLON) · `maxDigits: 4` · **verb:** Write the time
  *(No numeral in the label: “24-hour” would be a figure on screen, so the brief says it in words.)*
- **missTitle:** That time isn’t on any clock.
  *(Always true: every misconception has more than fifty-nine in its minutes, since the lesson always crosses
  the hour.)*
- **missSays:** “When I started, I added minutes like ordinary numbers, and kept getting times that don’t exist.
  An hour runs out at {{tt.hourmins}} minutes, so you go past the hour and start counting again.”
- **hints:**
  1. Count on from the start time in two jumps: first to the next o’clock, then the minutes that are left.
  2. There are {{tt.hourmins}} minutes in an hour.
  3. Write the end time on the twenty-four-hour clock and type its four digits, without the colon.
- **solve:** {{tt.start}} to {{tt.next}} is {{tt.tohour}} minutes. That leaves {{tt.m}} − {{tt.tohour}} =
  {{tt.rest}} minutes, so the lesson ends at {{tt.end}}: type **{{tt.answer}}**.
- **onOpen:** The lab door opens on the dot. William is first out, goggle marks round his eyes, looking for you,
  and you are there. This time he is smiling.

**Pot for lock C.** Your constraints: m from 35 to 70; mm + m crosses exactly one hour (so the answer is always
40 more than the misconception); start from 10:00 to 14:30 (so neither has a leading zero). **Added [X]:** starts
between 10:00 and 11:30, inside your range (“For Jon” 3); start minutes and lengths in fives, as school timetables
run; no length of exactly 60 (an hour-long lesson is just “add one to the hour”, which tests nothing).

| # | start | m (minutes) | ends | **answer** | miss, start as a number + m |
|---|---|---|---|---|---|
| 0 | 10:35 | 55 | 11:30 | **1130** | 1090 |
| 1 | 10:15 | 50 | 11:05 | **1105** | 1065 |
| 2 | 10:40 | 35 | 11:15 | **1115** | 1075 |
| 3 | 10:45 | 65 | 11:50 | **1150** | 1110 |
| 4 | 11:20 | 45 | 12:05 | **1205** | 1165 |
| 5 | 11:30 | 50 | 12:20 | **1220** | 1180 |
| 6 | 11:05 | 55 | 12:00 | **1200** | 1160 |
| 7 | 10:25 | 70 | 11:35 | **1135** | 1095 |
| 8 | 11:15 | 70 | 12:25 | **1225** | 1185 |
| 9 | 11:10 | 65 | 12:15 | **1215** | 1175 |

Generator rules: keypad, up to four digits; tokens `hh`, `mm`, `m`, `start` (as printed, “10:35”), `end`
(“11:30”), `next` (the next o’clock, “11:00”), `tohour` (60 − mm), `rest` (mm + m − 60), the constant `hourmins`
(60), `answer`, `miss`. Solver: x = 100 × ⌊(60·hh + mm + m) ÷ 60⌋ + (60·hh + mm + m) mod 60; `clue_numbers`
`[hh, mm, m]`. Variant 0 is your example. All ten answers are distinct, and answer − miss = 40 in every set.

### Lock D: lunch on William’s card (money, change with exchanges)

- **id:** `lunch-card-change` (proposed) · **key:** `till` · **grade:** 1
- **name:** The lunch card
- **brief:** The last stop on the card is lunch, and the canteen is loud. William has a lunch card and a tray with
  three things on it, and he’s too nervous to ask how much he will have left. The card says the till keeps the
  rest. Work it out for him before he gets to the front: how much will be left on his card, in pence?
- **instrument:** keypad · **label:** LEFT ON THE CARD (PENCE) · `maxDigits: 3` · **verb:** Write it in
- **missTitle:** Daisy has done exactly that.
- **missSays:** “When I started, I did my change by taking the smaller number from the bigger one in every
  column, and it was wrong every time. The top number is {{till.card}}, with nothing in its tens or its units. You
  can’t take something from nothing, so you exchange.”
- **hints:**
  1. Add up the three prices first, all in pence.
  2. Then take that total away from the card’s {{till.card}}p.
  3. Line the numbers up in columns. Where the top digit is smaller, exchange from the column to its left.
- **solve:** {{till.p1}} + {{till.p2}} + {{till.p3}} = {{till.totalP}}, which is {{till.total}}p.
  {{till.card}}p − {{till.total}}p = **{{till.answer}}p** left on the card.
- **onOpen:** The till beeps and shows exactly what you said. William looks at the screen, then at you, and says
  the most he has said all morning: “Thanks.”

**Pot for lock D.** Your constraints: three items, prices in multiples of 5p; total from £2.00 to £4.50 with a
units digit of 5 and a non-zero tens digit, so both columns need an exchange and the misconception (5 − hundreds,
tens digit, 5) never equals the answer. That leaves 22 possible totals, from 215 to 445. **Added [X]:** prices of
£1 or more are printed in pounds (£1.85) and under £1 in pence (60p), as canteens print them and as KS2 teaches
both; no price, in pence, equals its own set’s answer (“For Jon” 16); the items are an everyday canteen list,
names as tokens, and no item has two prices across the pot (a student who replays would notice).

| # | tray (`i1 p1`; `i2 p2`; `i3 p3`) | total | **answer** (500 − total) | miss, smaller from larger |
|---|---|---|---|---|
| 0 | a pasta pot £1.85; a fruit cup 60p; a carton of milk £1.20 | £3.65 | **135** | 265 |
| 1 | a sandwich £1.75; an apple 40p; a bottle of water 30p | £2.45 | **255** | 345 |
| 2 | a slice of pizza £2.10; a smoothie £1.35; a cookie 70p | £4.15 | **85** | 115 |
| 3 | a jacket potato £1.90; a yoghurt 85p; a carton of apple juice 50p | £3.25 | **175** | 225 |
| 4 | a bowl of soup £1.55; a bread roll 40p; a rice pudding 90p | £2.85 | **215** | 385 |
| 5 | a hot dinner £2.45; a flapjack 80p; a milkshake £1.10 | £4.35 | **65** | 135 |
| 6 | a wrap £2.05; a bag of crisps 55p; a carton of orange juice £1.15 | £3.75 | **125** | 275 |
| 7 | a cheese toastie £1.50; a carton of squash 70p; a biscuit 45p | £2.65 | **235** | 365 |
| 8 | a plate of curry and rice £2.25; a piece of garlic bread 60p; a carton of fruit juice £1.10 | £3.95 | **105** | 295 |
| 9 | a pasta bake £1.40; a salad pot 50p; a banana 35p | £2.25 | **275** | 325 |

Generator rules: keypad, up to three digits; tokens `i1`–`i3` (item names with their article), `p1`–`p3` (prices
as printed), `total` (pence), `totalP` (pounds, as printed), the constant `card` (500), `answer`, `miss`.
Solver `lambda x, v: x == v["card"] - v["total"]`; `clue_numbers`: each price as printed **and** in pence (“For
Jon” 16). Variant 0 has your total (365 → 135, misconception 265); the three items are mine **[X]**. Two answers,
85 and 65, have two digits, and the keypad is “up to three”, so they are entered as typed (KEYPAD-VARIABLE, canon
§11.3).

### The joint draw (canon §11.3): checked in a scratch run against today’s tools (nothing committed)

I ran every set above through `escape_set_checks.check_set` with the proposed solvers and clue figures. Then I ran
the four pots through `check-escape-rooms.py`’s own `figures()` and `draw_is_valid()`, lifted out of the file with
`ast` so the rules were the live ones, not a copy, against the six clue strings exactly as written in the objects
table.

- **All 38 sets pass `check_set`:** 10 map, 8 turn, 10 lesson, 10 lunch. Each has exactly one solving setting on
  its instrument, the answer and the misconception settable and different, no clue figure equal to the answer,
  and the dial’s answers off the end of its travel.
- **The joint pot: 10 × 8 × 10 × 10 = 8,000 draws, of which 5,710 are VALID; variant 0 is a VALID draw.** The
  floor is 20. Every set takes part in at least 420 VALID draws, so none is dead weight.
- **Where the 2,290 INVALID draws come from** (counted, by pair and rule): C and D (1,410 draws: mostly a price
  in pence, 35p to 70p, equal to a lesson’s start minutes or length, rule a; and the 65p answer against a
  65-minute lesson), B and D (600: a 90° or 45° turn against a 90p or 45p price, and 135° or 225° against a lunch
  answer or misconception), B and C (170: a 45° turn against a 45-minute figure), and draws with more than one of
  those (110). **Lock A is in none**, by design.
- **Joint-draw facts that depend on wording:** the compass rose and the lunch card carry no token, so they carry
  no clue figures. “Five pounds” in words keeps the card out of the count (item 15). Times print as “10:35”,
  which the checker reads as two figures, 10 and 35.
- The four new locks need `escape_set_checks.LOCKS` entries and bank entries (a new batch file, batch 12) in phase
  2; that is where the solvers above go. No script was changed here.

---

## Picture alts (provisional: written before any picture exists, to be rewritten against the filed art)

- **sceneAlt [X]:** A school hall on a summer morning, sun through tall windows. A big gridded map of the school
  stands on an easel by the stage, and clipboards lie on a row of chairs. Through the open doors a corridor leads
  away past a doorway lined with bookshelves, and a canteen counter is just visible at the far end. A box of lost
  property sits by the doors.
- **failAlt [X]:** A crowded school canteen at lunchtime, every table full, trays everywhere, and one chair at the
  end of a long table pulled slightly apart from the rest. *(Follows whichever fail you choose, item 5.)*
- **winAlt [X]:** A school canteen by a sunny window, one long table with every seat taken by trays and clipboards,
  a hunt card lying in the middle with every box ticked.

*(Empty of people and with no lettering, canon §11.6, so the pictures show the places and what is left on the
tables, never the students or William.)*

## Hub card line and meta description (phase 2, for the release; student surfaces, so no year group)

- **Hub card:** It’s transition day, the school is enormous, and your group has four stops to find before lunch,
  without losing anyone on the way.
  Topics line: Coordinates · Turns · Time · Money
- **Meta description** (155 characters, counted; the same string for `description` and `og:description`): A
  20-minute maths escape room. It’s transition day at St Martha’s: read the map, follow the librarian, collect
  William. Coordinates, turns, time and money.

## Teacher page (phase 2)

- `clueMap`, with no figures (teacher.js does not fill tokens): `map` → “The hall map: where the library is, up
  and along”; `rose` → “Bibby’s directions: the eight compass points, in order”; `bibby-card` → “Bibby’s
  directions: which way to face, where the next stop is”; `timetable` → “William’s lesson: when it starts and how
  long it lasts”; `tray` → “The lunch card: the three prices”; `lunch-card` → “The lunch card: what is on it”.
- Notes to carry: no calculator; the four cards can be done in any order; each lock is built round one named
  mistake (y before x; the anticlockwise turn; an hour as a hundred minutes; smaller from larger in each column),
  and Daisy’s response to each is her own memory of making it, never the answer. The label is “Year 6/7” and the
  rating ★ Warm-up, grades 1–3 (item 8). Per-lock minutes are set after a play-through, not guessed here.

---

## Notes for phase 2

- **Shared-code dependencies first (home lane):** the `label` field (item 8), and the theme only if you rule
  light (item 7). Neither touches this room’s data; the room can be built and played unlisted before either lands.
- **Token names are distinct across locks:** `map.*`, `dir.*`, `tt.*`, `till.*`; no token name is shared, and
  `dir.from`/`dir.fromU` differ only by case on purpose (one prints in the solve, one on her card).
- **Constant tokens, supplied in every set:** `dir.whole` (360), `dir.eighth` (45), `tt.hourmins` (60),
  `till.card` (500).
- **Bank batch 12:** four entries, variant 0 of each table as the audited lock.
- **ART-PENDING:** no `art:` field and no hub-card `<img>` until the three pictures are filed.
- **Release copy:** the hub and front page’s fifteen-minute, three-lock claims (item 12) wait on your wording.

---

## Checklist: the voice contract, SR-14, SR-11, §7.5.3 and the room rules

**Voice contract** (`docs/escape-room-voice-contract.md`, fixed constraints) and its STOP IF:

| Rule | Result |
|---|---|
| Students are always the heroes; the antagonist is the obstacle | **Pass, with a note.** No antagonist (ruling 3). The students find their way and look after William; the lunch bell is the pressure (the Kiln and Library precedent, working doc §3, §5i) |
| Wrong-entry lines never mock the student or their answer, only the lock | **Pass.** Every line is Daisy laughing at her own first weeks; none addresses a student’s answer or mentions William |
| The antagonist loses graciously; no humiliation | **Pass (not applicable).** No antagonist; nobody is beaten, and nobody is laughed at |
| Voice through the room setup, not a narrator layer | **Pass, with a note.** Hook and brief are narration, as in the reference room; Daisy carries the wrong-entry and misconception slots |
| “Idiot” and “stupid” never appear | **Pass** |
| British English | **Pass.** Canteen, lost property, jacket potato, flapjack, “taster lesson” |
| Name: real-sounding, no equipment puns, no innuendo, no real person | **Pass.** Your names. Daisy Reddington, William Trembles and Mrs Barb Phile (yours, from Library Jam). I can’t check whether either new name maps onto a real, identifiable student or member of staff |
| STOP IF: inventing the character rather than drawing it out | **Did not fire.** Premise, characters, traits, locks and the misconception pattern are yours; every extrapolation is **[X]** |
| STOP IF: a change to puzzle logic or lock behaviour | **Did not fire.** The maths and instruments are yours. The added constraints (A’s digits, C’s morning starts, D’s price format and in-pence check) narrow your ranges and change no lock |

**Your rulings of 16 Oct:**

| Ruling | Result |
|---|---|
| 1. Title, and “Year 6/7” in place of stars | **Pass.** Title used; the label proposed as a field (item 8); the prose keeps SR-11 (item 1) |
| 2. Four challenges, twenty minutes, forty-five-second penalty | **Pass.** `minutes: 20`, `penalty: 45`, four locks; all engine data, no engine change (item 9) |
| 3. Hunt frame; locks reskinned; no antagonist | **Pass.** Each lock is a clue card Daisy ticks; the lock names are places |
| 4. William never the joke; no line on his name; no nickname | **Pass.** Item 17: no word plays on his name, he is named in full once, no nickname, the only joke near him is Daisy’s about herself |
| 5. Daisy voices each misconception as her own past mistake, never the answer | **Pass, with item 13.** All four `missSays` open “When I started”; none prints the answer or the reversed code; for the two reversals I say why naming the mistake is avoided |
| 6. Bibby sets challenge B; stern and precise, never a villain | **Pass, with item 2.** She sets it in writing and is never quoted |
| 7. The four challenges, in order, with your constraints | **Pass.** Every set meets your constraints; the added constraints only narrow them; listed in the engine’s order |

**SR-14 (sensitive content)** and the scan (`scripts/check-content-safety.py`):

| Check | Result |
|---|---|
| Tier (a) words (death, kill, dead, violence, abuse, family breakdown…) | **Pass.** None |
| Tier (b) in humour (illness, injury…) | **Pass.** None. Daisy’s jokes are about getting lost |
| Loneliness in the fail screen | **Not an SR-14 word, but a tone call:** item 5 |

**SR-11 (age-neutral labels)** and **§7.5.3 (name the maths, never the student):**

| Check | Result |
|---|---|
| No year group or key stage, no “primary” or “secondary school” on a student surface | **Pass in the prose; exception for the label and title** (ruling 1, item 1). Never Year 6, Year 7, primary or secondary in any slot, the meta or the hub line |
| No “resit”, “retake” or “post-16” | **Pass** |
| Meta and card name the maths and level only | **Pass.** “A 20-minute maths escape room … Coordinates, turns, time and money” |

**Room rules** (working doc §3, §4, §8; canon §11.3):

| Rule | Result |
|---|---|
| One enforceable failure, able to reach the students during play | **Pass.** The lunch bell (a clock), with the penalty taking time off it; fail as in item 5 |
| A character who is not present cannot be the threat | **Pass.** No threat but the clock |
| Each character speaks only in their own room | **Pass, with item 2.** Bibby is narrated and writes a card; she says nothing. Daisy and William are new |
| No third never-knew ending | **Pass (not applicable).** No antagonist to find out |
| Students win by putting something right | **Pass.** They keep a lost new student with the group, from the map to the lunch table |
| If the students use the antagonist’s own method, the brief says why it is different | **Pass (not applicable)** |
| No figure in the prose outside `{{tokens}}` | **Pass.** No numeral in any slot. Numbers in words, all fixed and none a clue figure: “four stops”, “twice”, “eight compass points”, “four digits”, “twenty-four-hour clock”, “five pounds” (item 15), “fifty-nine” (a draft note, not prose). Maths constants in hints, misconceptions and solves are tokens (`whole`, `eighth`, `hourmins`, `card`). The label text and the meta’s “20-minute” are release copy, not prose |
| No tokens in `hook`, `brief`, `stakes`, `win` (written raw by the engine) | **Pass.** None |
| Never “Ofsted”; no brand names; no year | **Pass.** “September” is a month, not a year |
| No real child named | **Pass.** William and Daisy are invented (your brief) |
| UK school timings; St Martha’s | **Pass.** A morning hunt ending at lunch, lessons between ten and half past twelve; St Martha’s named in the hook |
| Eight objects, at least two blanks | **Pass.** Six clues, two blanks (item 6) |
| Each lock’s `brief` carries the premise | **Pass.** All four, each written to stand in any order (item 11) |
| Every lock has exactly one settable answer, and its misconception is settable (STOP IF) | **Pass.** 38 of 38 sets through `check_set`; three keypads and a 0–360 dial |
| Joint draw at least 20 VALID (STOP IF) | **Pass.** 5,710 of 8,000; variant 0 VALID |
| No lock beyond KS2 (STOP IF) | **Pass.** First-quadrant coordinates; eighths of a turn on an eight-point compass; durations on the 24-hour clock; column subtraction across zeros with money |
| Variant pot: 8–10 verified sets per lock | **Pass.** 10, 8, 10, 10; lock B’s eight repeat answers from different starting points (only six answers exist) |
| No `missArt` | **Pass.** The fail is the lunch bell, true only at time-out |
| No `art` field before the pictures (ART-PENDING) | **Pass.** Listed under “Room fields”; alts provisional |
| Meta description 150–160 characters | **Pass.** 155, counted (my first version was 170 and was cut) |
| Hint ladders general; no hint prints a worked figure | **Pass.** Constants only, as tokens |
| Wrong-answer feedback never gives the answer | **Pass, with item 13** |
