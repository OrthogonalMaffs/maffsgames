CONTRACT: LIBRARY-DRAFT (Project Claude for Jon, 9 Oct 2026, 19:35). Phase 1 of a NEW
escape room (the eleventh; Mrs Barb Phile's library). Draft only. Either lane may take it,
after The Rightful King and Car Trap drafts; it touches no live file. Save verbatim under
docs/handover/contracts/ when it starts.

======================================================================
TASK (LIBRARY-DRAFT): Draft every piece of prose for a new ★ Warm-up
escape room set in the school library, plus the variant parameters for
its three locks, into one review file for Jon. Change no live file.

ROOT CAUSE: Not a fault — new content for the priority audience. Only
two rooms (Comic Caper, Kiln Disaster) will carry ★ (grades 1–3) under
the difficulty scheme, and grade 1–3 students and resitters are the
site's first audience (canon §0). Jon gave the premise and character in
interview on 9 Oct 2026 (below). Canon §11.5: Jon reviews the draft
before any file is touched.

CLASS CHECK: Not a bug: content work under the existing voice-rewrite
process. docs/escape-room-voice-contract.md, docs/escape-room-voice-
rewrite.md (read first), escape-rooms/hamster-heist/room.js (reference)
and escape-rooms/kiln-disaster/room.js (the ★ GCSE-resit precedent, and
the first two-digit keypad) govern it. No shared code.

THE BRIEF (Jon, 9 Oct 2026):
- Setting: St Martha's school library, the backroom behind the returns
  trolley. The returns drop-box and its sorting belt are old and
  breaking down — "budget cuts". Nobody's fault; there is no villain.
- The machine has jammed with the whole class's returned books inside
  it, so the library system shows every one of them as LOST. At 3:30
  the system emails every parent about lost books and charges fines.
  The students have until 3:30 to get the machine working so the books
  land in the cleared bin and the record shows them returned.
- Mrs Barb Phile, the librarian ("Bibby" to the students). She likes
  books much more than she likes children, though bookworms are
  acceptable. Her books are her babies. She will NOT overturn fines or
  rescind the emails to parents — she trusts the system over any
  child's word. Her reason is not pettiness: the school budget is
  tight, lost books are unlikely to be replaced, and she wants the
  stories preserved for future year groups. Her love of literature
  means she wants to share the stories with children even though she
  is not that keen on them. The prose must carry that: stern, never a
  villain.
- She is present throughout, muttering and finding books returned to
  the wrong shelves. Jon's line, verbatim, the model for her voice:
  "Pride and Prejudice is NOT staying in the Biography section."
- How the students win (the design point): they never ask her to
  overturn anything. They make the record true, so her own system
  tells her the books are home, and the emails are never sent. She
  ends the room relieved: her babies were never lost. No humiliation.
- Wrong-entry lines: her muttering about another misshelved book,
  escalating (four lines; Jon's line among them, verbatim). Never aimed
  at the students. The theme — something in the wrong place — is what
  a wrong answer is.
- Pressure: the 3:30 email run, as a countdown (Kiln precedent); Bibby
  is the face of it.
- Rated ★ Warm-up (grades 1–3); every lock must be grade 1–3.
- Title: propose two or three in the draft; Jon chooses. Propose a
  slug. Same school, no year, no brands, British English. No book
  title may be one still in copyright if quoted beyond its title;
  titles alone are fine (Pride and Prejudice is public domain).

EXACT CHANGE:
1. Write docs/escape-room-drafts/library-draft.md (a new file, not
   served) containing, in the order room.js uses them: title options,
   hook, brief, stakes, win, fail; the wrongLines (four, escalating,
   Bibby's misshelving mutters); eight objects (name, where, and clue
   or flavour: six clues and at least two blanks), each clue written
   with {{key.token}} placeholders, never figures; for each lock: name,
   brief, instrument label and verb, the three-step hint ladder,
   missTitle, missSays and solve text; the three picture alts (scene,
   fail, win: empty of people, no lettering); the hub card line and
   the meta description.
2. Locks (Jon approved A, B and C, 19:32). Propose variant parameters
   for gen-escape-variants.py (propose only; list every set):
   - A, the sorting arm (ordering decimals, grade 2–3): the arm files
     by Dewey number. Five or six books on the trolley share a whole-
     number part and differ in decimal length (e.g. 520.15, 520.35,
     520.4, 520.5); the clue names one book; set the dial to the slot it
     goes in when the trolley is put in ascending order. Answer for the
     example: 3rd. Named misconception: "longer means bigger" (0.35 >
     0.4 because 35 > 4), giving a different slot (1st in the example).
     Constraints: answer and misconception slots differ; the answer is
     not the first or last position on the dial; the asked-for book has
     one decimal place; whole-number parts identical within a set.
     Instrument: short dial (1 to the number of books, or a little
     more).
   - B, the deflector arm (angles on a straight line, grade 1–2): the
     arm sits at x° to the belt; set the angle on the other side,
     180 − x. Named misconception: subtracting from 90, giving 90 − x.
     Constraints: x from 20 to 70, not a multiple of 5 (so 90 − x is
     never mistaken for a clean dial mark), answer ≠ any other lock's
     figures. Instrument: dial 0–180, step 1.
   - C, the fines (money and units, grade 1–2): the system has charged
     p pence a day for d days to each of n students; enter the total to
     be voided, in pounds. Answer p × d × n ÷ 100. Named misconception:
     pence read as pounds, p × d × n. Constraints: whole-pound totals
     only, answer at most 99 so the misconception (100 × answer) is
     settable on the keypad; p from 5 to 20 pence. Example: 15p × 12
     days × 30 students = £54 (miss 5400). Instrument: keypad, up to
     four digits.
   Check every set against the joint-draw rules (canon §11.3) and
   report the expected VALID count; the checker fails a room under 20.
3. Run the prose against the voice contract's checklist and the room
   rules in the working doc; list each rule with pass/fail at the end.
4. Open a PR with the draft file only; record it in the handover as
   "Library room draft for Jon's review". Merge on a green Gate (it
   changes nothing served).

DO NOT TOUCH: every existing room; the hub; the front page; the
sitemap; docs/art/ (pictures come after the build, as for The Rightful
King — write no art prompts); gen-escape-variants.py (propose
parameters only); engine.js (no new instrument — dial and keypad only).

SUCCESS CONDITION: the draft file exists, with every slot room.js
needs; no figure in the prose outside {{tokens}} (Dewey numbers
included); all three locks' parameter sets listed and checked; the
checklist all pass, or each fail explained; Jon has it to review.
Phase 2 (title, slug, build, variants, teacher page, hub, release) and
phase 3 (art) are separate contracts after Jon approves.

STOP IF: the brief contradicts the voice contract or a room rule in a
way the draft cannot resolve (quote both); any lock cannot be given
exactly one settable answer on its instrument; the joint draw gives
fewer than 20 VALID combinations; a lock would need a grade above 3.
