# The library room: draft for Jon’s review

**Phase 1 of a new ★ Warm-up escape room, the eleventh (contract LIBRARY-DRAFT, 9 Oct 2026, 19:35; saved as
`docs/handover/contracts/2026-10-09-library-draft.md`).** This is draft prose only. No live file is touched. Phase
2 (title, slug, build, variants, teacher page, hub, release) and phase 3 (art) are separate contracts after you
approve this.

How to read it:

- `{{key.token}}` is a figure filled from the drawn variant. The prose has no other figures, Dewey numbers
  included: every spine number is a token. Times are written in words ("half past three").
- Prose is shown with real quotation marks and apostrophes. In phase 2 they become entities in every slot except
  the object and lock `name` and `where`, which are escaped and keep real characters (canon §11.3).
- **[X]** marks a detail I extrapolated rather than took from your brief. Strike any you don’t want.
- Your line is used verbatim: “Pride and Prejudice is NOT staying in the Biography section.”

---

## For Jon: decisions in this draft

1. **Lock C’s instrument doesn’t exist yet. This is the big one.** The contract asks for a "keypad, up to four
   digits". The engine’s keypad takes **exactly** `digits` digits. Fewer gets "Not enough digits. The keypad
   wants all 4 of them." (`engine.js:610`), and typing past the limit is ignored (`engine.js:593`). So:
   - **On a four-digit keypad**, £54 has to be keyed as 0054. Worse, the four blank slots and that message both
     tell a grade 1–3 student the answer has four digits, which is exactly the misconception (5400). The keypad
     would teach the error the lock exists to catch.
   - **On a two-digit keypad**, the misconception can’t be set, so its response never fires. Worse, a student who
     types 5400 gets 54, because the extra digits are dropped: right by accident.
   - **The cause is shared, not this lock’s.** The Rightful King draft hit the same limit (its passcode examples
     60, 24, 42 against misses of 125, 64, 49), and Kiln’s note says its keypad was built round it. The fix
     belongs in the engine: an **opt-in keypad that accepts up to `digits` digits**, with the existing keypads
     unchanged. That is shared code, a home-lane change, and outside this contract (DO NOT TOUCH `engine.js`).
     **My recommendation: commission it before phase 2.**
   - **The generator needs a matching change.** Its `keep()` treats a keypad as a 0 to 9999 travel and rejects
     every answer under 400 as "at the end of the travel". The library below was built with that rule set aside
     for this lock.
   - The draft is written for the up-to-four-digit keypad. If you’d rather not change the engine, the
     alternative is a four-digit keypad with leading zeros, and I advise against it for the reason above.
2. **There is no `fail` slot in `room.js`.** The engine shows `stakes` on the start screen after "If you get it
   wrong." and on the time-out screen after "And so:" (`engine.js:244`, `:797`). The fail is written into
   `stakes` and reads after both lead-ins (the Car Trap precedent).
3. **`hook`, `brief`, `stakes` and `win` can’t carry tokens** (the engine writes them raw), so every spine number,
   fine and angle is in a clue, lock brief, hint or solve.
4. **Lock A, the trolley’s drop order.** The list is shown in the order the books were dropped in, never already
   sorted. Your example (520.15, 520.35, 520.4, 520.5) is in order and has four books. Variant 0 adds a fifth
   (520.62, which keeps your answer, 3rd, and your misconception slot, 1st) and shuffles the drop order. Proposed
   rule: a drop order already sorted either way is rejected.
5. **Lock A’s dial is 1 to 8 for every variant.** A lock has one instrument; only its variants change. Six books
   at most, so the dial is "the number of books, or a little more". The answer is never slot 1 (your rule), but
   can be the last book on the trolley (variants 3, 4, 5: still not the end of the dial). Strike that if you want
   the last book excluded too; it costs three variants.
6. **Lock C’s fines are multiples of five pence** (5p, 10p, 15p, 20p): inside your 5–20p range, and the
   arithmetic stays at grade 1–2 without a calculator, the Kiln standard. 15 × 12 × 30 still asks something of a
   grade 2 student. **For you:** calculator allowed or not; the teacher page should say.
7. **Lock B’s spread.** With the generator’s default spread (answers at least nine degrees apart), x from 20 to
   70 with no multiples of 5 gives four variants. With a five-degree spread it gives eight. I propose five.
8. **Bibby doesn’t overturn anything, and the room never asks her to.** The fines are reversed by the system
   itself once the books are in the cleared bin. The lock is the system’s own check before it cancels the
   half-past-three run. She trusts the system, so the system is what the students put right, as your brief says.
9. **How she is heard [X].** She is out in the library among the shelves, re-shelving. You hear her through the
   open hatch behind the returns trolley. She is present throughout and never addresses the students, so no
   line can be aimed at them.
10. **The difficulty rating isn’t in the repo yet.** No ★ field exists in any `room.js`, and the scheme isn’t in
    canon. The draft calls the room ★ Warm-up, grades 1–3, as the contract does. Where the stars are shown is
    phase 2’s call. `levelLabel` is proposed as "GCSE", the Kiln and Comic precedent.
11. **Her name.** Mrs Barb Phile is your name (a bibliophile pun) and "Bibby" your nickname. I can’t check
    whether it maps onto a real, identifiable member of staff.

---

## Title (three options; you choose)

**Chosen: The Library Jam (Jon, 10 Oct 2026).** Proposed slug `library-jam`, settled in phase 2.

1. **The Library Jam** *(my recommendation: says where and what in three words. Slug `library-jam`)*
2. **Bibby’s Babies** *(her books, her word for them. Slug `bibbys-babies`)*
3. **Overdue** *(short, and every student knows the word. Slug `overdue`)*

## Hook

The library at St Martha’s belongs, as far as anyone can tell, to Mrs Barb Phile. Officially she is the
librarian. To every student in the school she is Bibby. She likes books a great deal more than she likes
children, though she will make an exception for a bookworm. She calls the books her babies, and she means it.

Behind the returns trolley is a hatch, and behind the hatch is the backroom where the returns drop-box empties
onto an old sorting belt. Budget cuts. The machine is older than most of the staff, and today it has jammed with
your whole class’s returned books inside it.

## Brief

The library system can’t see inside a jammed machine. As far as it knows, every one of those books is lost. At
half past three it emails every parent in the class about a lost book, and charges a fine for each one.

Bibby will not overturn a fine, and she will not take a child’s word over the system’s. It isn’t spite. The
budget is tight, a lost book is unlikely ever to be replaced, and she wants those stories still on the shelves
for the year groups after yours.

So don’t ask her. Make the record true. Get the machine running, get the books into the cleared bin, and the
system will see them home and stop the emails itself.

She is out among the shelves, finding books in places they shouldn’t be. Every wrong setting costs you time, and
she always finds another one.

## Stakes (also the fail screen; see "For Jon" 2)

At half past three the emails go out: every parent in the class, one lost book each, one fine each. Bibby reads
the list on her screen without a flicker, because the system is never wrong, and starts the replacement forms
the budget will never pay for. Inside the drop-box, under the jam, every one of those books sits in the dark.

*(Read after "If you get it wrong." on the start screen and after "And so:" on the time-out screen; both work.)*

## Win

The arm swings, the belt runs, and the books come down the chute one at a time into the cleared bin. Each one
beeps as it lands. On the screen, LOST turns to RETURNED, name by name, and the half-past-three run cancels itself.

Bibby comes round the end of the shelves with Pride and Prejudice under her arm. She looks at the screen, then at
the bin. She lifts out the top book, checks the spine, and holds it for a moment longer than she needs to.

“They were here all along,” she says, to the book.

Then she puts it on the trolley, spine out, and goes to find a shelf for Pride and Prejudice that isn’t
Biography **[X]**.

---

## wrongLines (four, escalating; the last repeats)

Each `head` is the machine; each `body` is Bibby, out in the library, finding something in the wrong place. A
wrong answer is something in the wrong place, and so is everything she finds. None of it is aimed at the
students.

1. **head:** The machine clunks and the setting clears.
   **body:** Out in the library, a book slides off a shelf. A tut. “A cookbook. In Astronomy.” It slides back
   in somewhere else.
2. **head:** The belt shudders and stops again.
   **body:** “Atlases are not for leaning on.” The sound of a large book being carried, with great care, back
   to where it lives.
3. **head:** The setting slides back. The clock over the desk doesn’t.
   **body:** Her voice comes through the hatch, quite clearly: “Pride and Prejudice is NOT staying in the
   Biography section.”
4. **head:** Another one. The clock keeps going.
   **body:** From somewhere in the stacks: “Wrong place.” A pause. A book moving. “Better.”

*(Line 3 is yours, verbatim. Line 4 repeating is the joke: she finds one every time.)*

---

## Objects (eight: six clues, two blanks)

All ids are new (a new room). No numeral is typed into any clue; the spine numbers, angle, fine, days and count
are all tokens (the kiln rule, working doc §5i).

| # | id | name | where | clue or flavour |
|---|---|---|---|---|
| 1 | `trolley` | The returns trolley | behind the hatch, still loaded from this morning | Every spine has a white label, and every label starts the same. In the order they were dropped in: **{{dw.list}}**. |
| 2 | `jammed-book` | Book in the sorting arm | held fast in the arm over the belt | A book about {{dw.subject}}, gripped by its corner. Spine label **{{dw.book}}**. A sticker on the arm: FILES SMALLEST FIRST ALONG THE SHELF. |
| 3 | `belt-plate` | Maintenance plate | riveted to the side of the belt | Stamped into the metal: **DEFLECTOR ARM: {{df.x}}° TO THE BELT.** |
| 4 | `reset-card` | Reset card | taped inside the machine’s cover | “RESET: set the dial to the angle between the arm and the belt **on the other side of the arm**. The belt is straight.” |
| 5 | `fines-screen` | The library system | on the screen on Bibby’s desk | LOST BOOKS. Fine: **{{fn.p}}p a day** for each book. Days overdue: **{{fn.d}}**. |
| 6 | `drop-counter` | Drop-box counter | a little mechanical counter on the drop-box | **{{fn.n}}** books posted today, one from everyone in your class. The counter, at least, saw them go in. |
| 7 | `memo` | Memo | pinned over the drop-box | *(blank)* From the business office. The drop-box repair has been moved to next year’s budget. Somebody has written “AGAIN” under it, in very neat capitals. **[X]** |
| 8 | `biography` | The Biography shelf | through the hatch, nearest the door | *(blank)* Lives of explorers, scientists and queens, all in order. And one book that isn’t the life of anybody at all. |

Clue 4 carries no token and no figure, so the collision rules don’t count it.

---

## Locks (★ Warm-up, grades 1–3)

All three are new. Proposed ids, keys and instruments; the parameter sets are proposals for
`gen-escape-variants.py`, which this phase does not touch. Phase 2 also needs a bank batch entry for each lock.

### Lock A: the sorting arm (ordering decimals, grade 2–3)

- **id:** `dewey-sort-arm` · **key:** `dw`
- **name:** The sorting arm
- **brief:** The arm files books by the number on the spine, smallest first along the shelf. It has stopped with
  one book in its grip, and it won’t let go until it is told which slot that book goes in.
- **instrument:** dial · **label:** SLOT ON THE SHELF · 1 to 8, step 1, 0 decimals, starts at 1 · **verb:** Set
  slot
- **hints:**
  1. Every book on the trolley starts with the same whole number, so only the part after the decimal point
     matters.
  2. Compare the tenths first. Only if two books have the same tenths do you look at the hundredths. More digits
     after the point doesn’t make a number bigger.
  3. Smallest first: {{dw.sorted}}. Count along to {{dw.book}}.
- **missTitle:** That reads the digits after the point as a whole number.
- **missSays:** Slot {{dw.miss}} is where {{dw.book}} would go if a longer number after the point meant a bigger
  number. It doesn’t. Line them up by the tenths first, then the hundredths.
- **solve:** Smallest first: {{dw.sorted}}. {{dw.book}} is number **{{dw.answer}}**.
- **onOpen:** The arm swings the book into its slot with a satisfied clunk, and lets go.

| # | shelf | trolley (`list`, in drop order) | book | answer | miss |
|---|---|---|---|---|---|
| 0 | 520 (stars and planets) | 520.35, 520.5, 520.15, 520.62, 520.4 | 520.4 | 3rd | 1st |
| 1 | 567 (dinosaurs) | 567.6, 567.4, 567.07, 567.13, 567.86, 567.65 | 567.6 | 4th | 2nd |
| 2 | 641 (cooking) | 641.3, 641.7, 641.8, 641.18, 641.97 | 641.7 | 3rd | 2nd |
| 3 | 551 (volcanoes and weather) | 551.9, 551.3, 551.06, 551.77, 551.76 | 551.9 | 5th | 3rd |
| 4 | 942 (British history) | 942.4, 942.1, 942.8, 942.9, 942.63, 942.77 | 942.9 | 6th | 4th |
| 5 | 796 (sport) | 796.8, 796.2, 796.37, 796.61, 796.39 | 796.8 | 5th | 2nd |
| 6 | 598 (birds) | 598.1, 598.6, 598.8, 598.63, 598.58, 598.59 | 598.6 | 4th | 2nd |
| 7 | 821 (poetry) | 821.5, 821.7, 821.2, 821.8, 821.16, 821.53 | 821.5 | 3rd | 2nd |

Generator rules:
- **The trolley:** five or six books on one shelf, one whole-number part per variant (a real Dewey class, its
  subject as a word token). Each book has one or two decimal places, at least two of each, and none ends in a
  zero.
- **No ties under the misconception:** the decimal parts read as whole numbers are all different, so .4 and .04
  can’t both appear.
- **The asked-for book** has one decimal place.
- **The slots:** answer = its slot in ascending order; miss = its slot when the decimal parts are ranked as whole
  numbers. Answer ≠ miss, answer ≠ 1. The drop order is never already sorted ("For Jon" 4).
- **Solver:** the book’s index in the list sorted by value; one solution by construction.
- **The dial:** 1 to 8; spread off for this lock (one variant per shelf instead).

The ordinal in the table is for reading. The dial value is the number.

### Lock B: the deflector arm (angles on a straight line, grade 1–2)

- **id:** `deflector-straight-line` · **key:** `df`
- **name:** The deflector arm
- **brief:** The deflector knocks each book off the belt and down the chute to the cleared bin. It has slipped. To
  reset it, the dial wants the angle between the arm and the belt on the other side of the arm.
- **instrument:** dial · **label:** ANGLE ON THE OTHER SIDE · **unit:** ° · 0 to 180, step 1, 0 decimals, starts at
  0 · **verb:** Set angle
- **hints:**
  1. The belt is a straight line, and the arm meets it at one point. There is an angle on each side of the arm.
  2. Angles on a straight line add up to {{df.half}}°.
  3. {{df.half}} − {{df.x}}.
- **missTitle:** That makes a right angle, not a straight line.
- **missSays:** {{df.miss}}° is {{df.quarter}} − {{df.x}}, the angles that make a right angle. The belt is a
  straight line, so the two angles make {{df.half}}°.
- **solve:** {{df.half}} − {{df.x}} = **{{df.answer}}°**.
- **onOpen:** The arm clicks into place, and the first book drops down the chute.

| # | x | answer, 180 − x | miss, 90 − x |
|---|---|---|---|
| 0 | 37° | 143° | 53° |
| 1 | 46° | 134° | 44° |
| 2 | 63° | 117° | 27° |
| 3 | 68° | 112° | 22° |
| 4 | 24° | 156° | 66° |
| 5 | 56° | 124° | 34° |
| 6 | 32° | 148° | 58° |
| 7 | 51° | 129° | 39° |

Generator rules: dial (0, 180, 1); x from 20 to 70, not a multiple of 5; answer 180 − x; miss 90 − x; spread five
degrees ("For Jon" 7). Tokens `half` (180) and `quarter` (90) are constants carried as tokens, as Car Trap carries
its `half`. Your rule "answer ≠ any other lock’s figures" is the joint-draw rules below, which the engine enforces
per draw.

### Lock C: the fines (money and units, grade 1–2)

- **id:** `fines-pence-to-pounds` · **key:** `fn`
- **name:** The reconciliation screen
- **brief:** Once the books are in the cleared bin, the system can reverse the fines itself. It won’t cancel the
  half-past-three run until it is given the total it charged, in pounds.
- **instrument:** keypad, **up to four digits** ("For Jon" 1) · **label:** TOTAL TO REVERSE, IN POUNDS · **verb:**
  Enter total
- **hints:**
  1. Start with one student: so many pence a day, for so many days.
  2. Then the whole class: one fine for every book posted.
  3. That total is in pence. There are {{fn.hundred}} pence in a pound.
- **missTitle:** That is the total in pence.
- **missSays:** {{fn.miss}} is how many pence the system charged. The screen wants pounds, and there are
  {{fn.hundred}} pence in a pound.
- **solve:** {{fn.p}}p × {{fn.d}} days = {{fn.each}}p each. {{fn.each}}p × {{fn.n}} = {{fn.miss}}p = **£{{fn.answer}}**.
- **onOpen:** The screen thinks about it, then cancels the half-past-three run. No emails. No fines.

| # | p | d (days) | n (students) | each, p × d | answer (£) | miss (pence read as pounds) |
|---|---|---|---|---|---|---|
| 0 | 15p | 12 | 30 | 180p | 54 | 5400 |
| 1 | 20p | 15 | 26 | 300p | 78 | 7800 |
| 2 | 20p | 15 | 32 | 300p | 96 | 9600 |
| 3 | 20p | 10 | 24 | 200p | 48 | 4800 |
| 4 | 10p | 20 | 28 | 200p | 56 | 5600 |
| 5 | 5p | 8 | 30 | 40p | 12 | 1200 |
| 6 | 10p | 14 | 20 | 140p | 28 | 2800 |
| 7 | 15p | 14 | 20 | 210p | 42 | 4200 |
| 8 | 10p | 20 | 31 | 200p | 62 | 6200 |
| 9 | 5p | 15 | 32 | 75p | 24 | 2400 |

Generator rules:
- **Inputs:** p in {5, 10, 15, 20} ("For Jon" 6); d from 5 to 20; n from 20 to 32 (a class); p, d and n all
  different.
- **Answers:** p × d × n a whole number of pounds, from 10 to 99 (two digits), so the miss (p × d × n, four
  digits) is settable. The answer is not printed in its own clue. Answers distinct.
- **Keypad:** up to four digits ("For Jon" 1).
- **Solver:** x × 100 = p × d × n over 0 to 9999; one solution.
- Variant 0 is your example.

### Joint draw (canon §11.3)

Measured with `check-escape-rooms.py`’s own `clue_strings()` and `draw_is_valid()` on the six clue strings above
as they would appear in `room.js`: **572 of 640 joint draws VALID; variant 0 VALID.** The floor is 20. Every
Dewey number is a clue figure for lock A, which makes no difference here: none can match another lock’s whole-
number figures. Scratch only; nothing was committed to the generator.

---

## Picture alts (empty of people, no lettering; to be checked against the pictures in phase 3)

- **sceneAlt:** The backroom of a school library, seen past a loaded returns trolley. An old metal drop-box is
  built into the wall, and a sorting belt runs out of it towards a chute and a wire bin. A mechanical arm has
  stopped over the belt with one book in its grip, and a flat deflector arm sits at a slant across the belt. Shelves
  of books line the walls, a few sticking out at odd angles, and a small screen glows on a desk beside a date stamp
  and a cup of tea.
- **failAlt:** The same backroom at the end of the day. The belt is still, the arm frozen with its book, and the
  wire bin is empty. The screen on the desk glows red. The returns trolley stands where it was.
- **winAlt:** The same backroom. The wire bin is full of books, neatly stacked, and the arms are at rest. Every book
  on the shelves is pushed in level. The screen on the desk glows green.

*(No art prompts, per DO NOT TOUCH.)*

## Hub card line and meta description

- **Hub card:** The returns machine has jammed with the whole class’s books inside, and at half past three the
  library system emails every parent.
  Topics line: Ordering decimals · Angles on a line · Money
- **Meta description** (150 characters; the same string for `description` and `og:description`): A 15-minute maths
  escape room for grades 1 to 3. The library’s returns machine has jammed: fix it before the fines go out.
  Decimals, angles and money.

---

## Checklist: the voice contract and the room rules

Voice contract (`docs/escape-room-voice-contract.md`, fixed constraints) and its STOP IF:

| Rule | Result |
|---|---|
| Students are the heroes; the antagonist is the obstacle | **Pass, with a note.** There is no villain (your brief). The students fix the machine; the countdown is the obstacle and Bibby is its face (the Kiln precedent, working doc §3, §5i) |
| Wrong-entry lines never mock the student or their answer, only the lock | **Pass.** Every line is Bibby and a misshelved book; none reaches the students |
| The antagonist loses graciously; no humiliation | **Pass.** She isn’t beaten; she ends relieved (“They were here all along”) |
| Voice through the room setup, not a narrator layer | **Pass, with a note.** The hook and brief are narration, as in the reference room; Bibby’s voice is the wrong-entry slot and her line in the win |
| "Idiot" and "stupid" never appear | **Pass** |
| British English | **Pass.** Returns trolley, business office, pence |
| Name: real-sounding, no equipment puns, no innuendo | **Pass.** Your name, a bibliophile pun ("For Jon" 11) |
| STOP IF: inventing the character rather than drawing it out | **Did not fire.** Your brief gives her character, motive, voice, model line and arc. Every extrapolation is marked **[X]** |

Room rules (working doc §3, §4, §8; canon §11.3) and this contract:

| Rule | Result |
|---|---|
| One enforceable failure, able to reach the students during play | **Pass.** The half-past-three email run, with Bibby in earshot |
| A character who is not present cannot be the threat | **Pass.** Bibby is present; the threat is the run, not her |
| Stern, never a villain | **Pass.** Her refusal is given its reasons in the brief: budget, replacement and future year groups |
| The students never ask her to overturn anything | **Pass.** The system reverses its own record ("For Jon" 8) |
| Each character speaks only in their own room | **Pass.** Bibby is new and speaks only here |
| No third never-knew ending | **Pass.** She sees the screen and the bin |
| Students win by putting something right | **Pass.** They repair the machine and the record |
| Wrong-entry theme: something in the wrong place | **Pass.** All four lines; yours is line 3, verbatim |
| No figure in the prose outside `{{tokens}}`, Dewey numbers included | **Pass.** No numeral anywhere in the prose. Constants in hints are tokens (`half`, `quarter`, `hundred`) |
| No tokens in `hook`, `brief`, `stakes`, `win` | **Pass** |
| Book titles: none in copyright quoted beyond its title | **Pass.** One title, Pride and Prejudice (public domain), never quoted. Every other book is a subject |
| No brand names; no year; never "Ofsted" | **Pass** |
| St Martha’s; UK school timings | **Pass.** St Martha’s named in the hook; the run is at half past three |
| Eight objects, at least two blanks | **Pass.** Six clues, two blanks |
| Every lock grade 1–3 (STOP IF) | **Pass.** Ordering decimals (2–3), angles on a line (1–2), pence to pounds (1–2) |
| Every lock has exactly one settable answer on its instrument (STOP IF) | **Pass for A and B. C: pass on the instrument the contract names, which the engine doesn’t have yet ("For Jon" 1).** On today’s four-digit keypad the answer is settable only as 0054, which is exactly one answer but steers the student to the misconception. Resolved in the draft by recommending the engine option, not by bending the lock |
| Joint draw at least 20 VALID (STOP IF) | **Pass.** 572 of 640, variant 0 VALID |
| Dial and keypad only; no new instrument (DO NOT TOUCH `engine.js`) | **Pass, with "For Jon" 1.** A and B are dials and C is a keypad. Its "up to" option is a change to the existing keypad, for you to commission as shared code |
| No `missArt` | **Pass.** The fail picture shows the end of the day, true only at time-out |
| Meta description 150–160 characters | **Pass.** 150 |
