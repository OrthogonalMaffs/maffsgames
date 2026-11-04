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

Print it **at 100% (actual size), A4, double-sided off**. It is designed to print in black and white.

## What to proofread

1. **Page 1, Run it (DRAFT until you say "wording final"):** Project Claude's draft, verbatim, with each set's pages
   (generated: "Each set is 4 pages: A 6-9 ... G 30-33.") and Amendment 11's final-padlock line; at most 150 words
   (the build counts them; it is exactly 150 for Kiln, so the play-online line is on page 2). Send your wording to Code Claude: it goes into `run_it()` in `build_pack.py`, and the DRAFT badge comes off
   in the same change.
2. **Page 2, Read-outs (DRAFT):** three boxed scripts, each for its moment: the start (hook, brief and one line to the
   students), a team finishing (room.js `win`) and calling time (room.js `stakes`, the timeout outcome, which is read
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
   read clearly; the three red herrings (helpdesk ticket, emergency stop, firing screen) carry no number; the cover's
   answer boxes show only each instrument's picture, label and unit (no digit slots, range or maximum); the locks page
   ends with the final padlock's target, its rules, a working box and the expression line.
6. **The look of the labels on the art:** each label is fitted to its box at 11 pt or larger. If one sits badly on
   its picture, its box is `label_box` in `rooms/kiln-disaster/config.json` (in the image's own pixels).
7. **Hint cards and certificate (last two pages):** the locks' three hints each, then the final padlock's card.
8. **Footer:** the MaffsGames logo and name, the room, pack version, seed and build date on every page. Give a
   buyer's question the version and seed from the footer and the pack can be rebuilt exactly.

## How it works

`build_pack.py` holds no room's facts. For a room it reads:

- `escape-rooms/<slug>/room.js`, evaluated in a blank Chromium page (as the room page evaluates it), and the `TEACH`
  block of its `teacher.html` (topics, minutes, level). The pages themselves are never loaded, and the browser has no
  network: fonts come from the repo's pinned copies.
- `escape-rooms/variants.json`, the verified variant libraries (room.js must equal them).
- `rooms/<slug>/config.json`: the art files and their roles (`clue`, `herring`, `answer`), each image's label box in
  image pixels, the font per card (`label`: Oswald; `hand`: Permanent Marker), the number of sets, the seed, the pack
  version, the certificate title, the final padlock's shape (default one x and one + or -) and the words printed on
  each red herring (which must come from that object's flavour text in room.js and contain no digit).

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
   score sheet or a student page; `stakes` is only in its read-out and, prefixed, on the covers; page 1 is at most
   150 words and no rule is stated on more than one teacher page; no student page prints the final padlock's
   shape or allows a calculator. The PDF's page count must equal the pages built.

`python -X utf8 tools/pack-generator/build_pack.py --selftest` (in CI as `scripts/test-pack-generator.py`) checks
every room with a config and plants seventeen faults, each of which must be caught: a duplicate answer across sets,
an invalid joint draw, a wrong recomputed answer, a printed URL with no room page, a missing score-sheet row, a final
target two expressions reach and one no expression reaches, a fixed penalty figure, a pack whose sets use different
final-padlock shapes, a range and digit slots on answer boxes, `stakes` unprefixed on a cover and inside the start
read-out, page 1 over 150 words, a rule stated on two teacher pages, the final padlock's shape or a calculator allowance on
a student page, and a set whose product has no factor a multiple of 5 or 12 or less. It builds no PDF.

## Adding a room

1. `rooms/<slug>/config.json` with its art in `rooms/<slug>/art/` (each image at most 250 KB).
2. Each of the room's locks in `lockcheck.py`'s `RECOMPUTE`, by lock id, recomputed its own way. The build refuses a
   room with a lock missing there.
3. Build, then proofread as above.

## Fonts

`fonts/Oswald-Variable.ttf` (SIL Open Font License 1.1, `fonts/Oswald-OFL.txt`) and
`fonts/PermanentMarker-Regular.ttf` (Apache License 2.0, `fonts/PermanentMarker-LICENSE.txt`), both from
`github.com/google/fonts`. Outfit comes from the repo's pinned copies in `scripts/fonts/`.
