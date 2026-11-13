# Printable escape-room packs

A group-race pack is an A4 PDF of one escape room in several sets (A, B, C, ...), each with different numbers, for a
class to race through on paper. It is the offline convenience version that canon §7.1 allows to be sold; the online
room stays free and identical. **The PDF is the product: never commit it, upload it or attach it anywhere.**
`dist-packs/` is gitignored, and the build refuses to write anywhere git would track. This folder is excluded from
the website (`_config.yml`).

## Build it (Jon, at home)

From the repo root, in the WSL venv (it needs only Playwright and its Chromium, which the repo's checks already use):

```sh
python -X utf8 tools/pack-generator/build_pack.py kiln-disaster
```

It writes `dist-packs/kiln-disaster-pack.pdf` (35 pages, about 8 MB) and prints what it checked. The same command
with the same seed gives the same sets every time; `--seed 2` gives a different choice, `--sets 5` fewer sets,
`--target 67` one final-padlock target for every set (the build fails, naming each set and why, if any cannot make it). Any
failed check prints `BUILD FAILED` with the reason, and no PDF is written.

**Approval and the DRAFT badge.** Whether Jon has approved a room's printed wording lives in its
`rooms/<slug>/config.json`, once: `"wording_approved": {"by": "Jon", "date": "YYYY-MM-DD"}`, or `null` (no key counts
as `null`). Pages 1 and 2 carry the "DRAFT: Jon's wording" badge only while it is `null`, and the build fails if an
approved room prints DRAFT anywhere. Copies for Tes are built with `--final`, which refuses an unapproved room:
`python -X utf8 tools/pack-generator/build_pack.py kiln-disaster --final`.

Print it **at 100% (actual size), A4, double-sided off**. It is designed to print in black and white.
Page 1 carries the room's win image from `docs/art/<art>-win.webp`; a room without one does not build.

## What to proofread

1. **Page 1, Run it (DRAFT badge until the room's `wording_approved` is set, above):** Project Claude's draft, verbatim, with each set's pages
   (generated: "Each set is 4 pages: A 6-9 ... G 30-33.") and Amendment 11's final-padlock line; at most 150 words
   (the build counts them; it is exactly 150 for Kiln, so the play-online line is on page 2). Send your wording to Code Claude: it goes into `run_it()` in `build_pack.py`; your approval goes into
   the room's config, and the badge follows it.
2. **Page 2, Read-outs (DRAFT badge until approved):** three boxed scripts, each for its moment: the start (hook, brief and one line to the
   students; the hook is read aloud here and printed nowhere else, WARMUP-PACKS Ruling 2, 12 Nov 2026), a team finishing (room.js `win`) and calling time (room.js `stakes`, the timeout outcome, which is read
   nowhere else and printed on the covers only as "If time runs out: ..."); then the play-online line.
3. **Page 3, Score sheet (landscape):** two blanks you fill in first ("Each wrong answer adds ___ min", "Each hint
   adds ___ min"); one row per set; for each lock and for the final padlock an Opened box and five wrong-answer boxes;
   finishing time, the counts of wrong answers and hints, penalty (min) and total time; the rule in two lines under it.
   No fixed penalty figure is printed on it or on any student page.
4. **Pages 4-5, Answer key and worked solutions:** the "About this room" box (contents, each lock's topic and time,
   the level, the final padlock's shape and target range); every answer, common wrong answer and worked line was
   recomputed by a separate method before the PDF was made, so a mismatch would have stopped the build. Spot-check
   one set against its cover and evidence pages anyway: that is what a teacher will do.
   **The final padlock (Amendments 5, 7, 11):** students are told only: each answer once, any of + - x /, no
   brackets, no calculator, make the target. Behind the scenes every set's one solution has the same shape (one x and
   one + or -), is the only expression of any shape that makes the target, works out in whole steps, and its product
   has a factor that is a multiple of 5 or 12 or less; the sets are chosen so every set has one, or the build fails.
   The shape is never printed for students (the build checks); "About this room" gives it, the target range and the
   intended route (estimation) for the teacher. Option B (one + and one -) is `"final_shape": "plus-and-minus"`.
5. **Each set (cover, evidence pages 1-2, locks page):** the set letter is in the top-right box of every page; the
   figures printed on each object (asset tag, cable label, installation sheet, calibration log, instruction card)
   read clearly; the three red herrings (helpdesk ticket, emergency stop, firing screen) carry no number; the cover
   prints the room's picture, the brief and the "If time runs out:" warning, never the hook; the cover's answer boxes show only each instrument's picture, label and unit (no digit slots, range or maximum); the locks page
   ends with the final padlock's target, its rules, a working box and the expression line.
6. **The look of the labels on the art:** each label is fitted to its box at 11 pt or larger. If one sits badly on
   its picture, its box is `label_box` in `rooms/kiln-disaster/config.json` (in the image's own pixels). Measure each
   `label_box` inside the object's printable surface, never to its edge, with a margin of at least 2% of the art's
   width on any side that meets an edge of the paper, card or screen.
7. **Hint cards and certificate (last two pages):** the locks' three hints each, then the final padlock's card.
8. **Footer:** the MaffsGames logo and name, the room, pack version, seed and build date on every page. Give a
   buyer's question the version and seed from the footer and the pack can be rebuilt exactly.

## How it works

`build_pack.py` holds no room's facts. For a room it reads:

- `escape-rooms/<slug>/room.js`, evaluated in a blank Chromium page (as the room page evaluates it), and the `TEACH`
  block of its `teacher.html` (topics, minutes). The pages themselves are never loaded, and the browser has no
  network: fonts come from the repo's pinned copies.
- `escape-rooms/assets/rating.js`, added to the same blank page: the answer key's level line is its own
  `MaffsEscapeRating.rating(ROOM)`, the room's rating from its lock grades ("Level: Warm-up (1 of 3 stars), grades
  1–3, set by the hardest lock."), never a line typed in the teacher notes. A lock with no grade stops the build.
- `escape-rooms/variants.json`, the verified variant libraries (room.js must equal them).
- `rooms/<slug>/config.json`: the art files and their roles (`clue`, `herring`, `answer`), each image's label box in
  image pixels, the font per card (`label`: Oswald; `hand`: Permanent Marker), the number of sets, the seed, the pack
  version, the certificate title, the final padlock's shape (default one x and one + or -), the words printed on
  each red herring (which must come from that object's flavour text in room.js and contain no digit) and a clue
  card's optional print-only `printed` and `caption` ("Adding a room", below).

Then, in order, any failure stopping the build:

1. `scripts/check-escape-rooms.py` is imported unchanged, which runs the whole room check; its `draw_is_valid()` and
   `clue_strings()` are the rules the room engine serves draws by.
2. **Selection:** every joint draw (one variant per lock) is judged VALID or not; from the VALID ones, a seeded
   search picks the sets so that no lock's answer repeats across them and every set has a final padlock with a
   friendly product; then `final.py` gives each set its final padlock in the pack's one shape.
3. **Verification:** `lockcheck.py` recomputes every answer, common wrong answer and worked-solution figure from each
   variant's givens, by its own method (it imports neither the variant generator nor its set checks), and re-reads
   every final expression with its own parser: its value, its shape, and that no other expression makes its target.
4. **Render and check:** the pages are built as HTML and printed by Chromium. Before the PDF is written: every label
   fits its box at 11 pt or more (one line if it can, else balanced lines); no page overflows; every student page
   shows its set letter; no red herring shows a digit; no answer box or lock line gives away a digit, range or
   maximum; no `{{token}}` is left unfilled; every footer carries the logo and name under 12 mm high; the one URL
   printed (covers and page 2) resolves to the room's own live page in this repo (host from `CNAME`); the score sheet
   has one row per set and one column group per lock and for the final padlock; no fixed penalty figure is on the
   score sheet or a student page; `stakes` is only in its read-out and, prefixed, on the covers; the hook is in the
   start read-out and on no cover, and a hook or brief with a `{{token}}` fails the build (the start read-out is
   filled once, from set A); page 1 is at most
   150 words and no rule is stated on more than one teacher page; no student page prints the final padlock's
   shape or allows a calculator. The PDF's page count must equal the pages built.

`python -X utf8 tools/pack-generator/build_pack.py --selftest` (in CI as `scripts/test-pack-generator.py`) checks
every room with a config and plants faults, each of which must be caught (the run prints how many), among them: a duplicate answer across sets,
an invalid joint draw, a wrong recomputed answer, a printed URL with no room page, a missing score-sheet row, a final
target two expressions reach and one no expression reaches, a fixed penalty figure, a pack whose sets use different
final-padlock shapes, a range and digit slots on answer boxes, `stakes` unprefixed on a cover and inside the start
read-out, page 1 over 150 words, a rule stated on two teacher pages, the final padlock's shape or a calculator allowance on
a student page, a set whose product has no factor a multiple of 5 or 12 or less, a wrong recomputed answer in each of The
Comic Caper and The Library Jam, a cover printing the hook, a start read-out without it and a hook with a token, a
clue whose caption is left with an orphan full stop, a caption override with a space before its full stop, a
`printed` key on a red-herring image and a room with an ungraded lock. It builds no PDF.

## Adding a room

1. `rooms/<slug>/config.json` with its art in `rooms/<slug>/art/` (each image at most 250 KB).
2. Each of the room's locks in `lockcheck.py`'s `RECOMPUTE`, by lock id, recomputed its own way. The build refuses a
   room with a lock missing there.
3. Build, then proofread as above.

**Captions and print-only words (contract CAPTION-GAPS, 13 Nov 2026).** A clue's `<b>` part is printed on the art
and the rest of the clue is the caption under the picture: the text before `<b>` and the text after `</b>`, joined
so that it still reads as a sentence. A right part that starts with `.` `,` `;` or `:` joins with no space ("Spine
label. A sticker ..."); after a left part ending in a colon, a right part that is only punctuation is dropped
("... dropped in:"); with no left part, the right part's first letter is capitalised ("Books posted today ...").
Every caption is then checked, and the build fails naming the room, the object and the caption if it has a space
before `.` `,` `;` `:` or a closing quote, ends with a lone punctuation mark after a space, or starts with a
lowercase letter.

When a clue cannot be tidied into a caption (its sentence runs through the `<b>` part), give its **clue** image in
`config.json` print-only words instead of changing the live room:

- `"printed"`: replaces the `<b>` part on the art;
- `"caption"`: replaces the caption (`""` for none).

Both are filled for each set with the same `{{token}}` filler as the clue, and the caption check applies to an
override too. Either key on a `herring` or `answer` image fails the build. Library Jam's reset card uses both.

## Fonts

`fonts/Oswald-Variable.ttf` (SIL Open Font License 1.1, `fonts/Oswald-OFL.txt`) and
`fonts/PermanentMarker-Regular.ttf` (Apache License 2.0, `fonts/PermanentMarker-LICENSE.txt`), both from
`github.com/google/fonts`. Outfit comes from the repo's pinned copies in `scripts/fonts/`.
