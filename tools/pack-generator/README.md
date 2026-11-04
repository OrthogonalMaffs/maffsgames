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

It writes `dist-packs/kiln-disaster-pack.pdf` (34 pages, about 8 MB) and prints what it checked. The same command
with the same seed gives the same sets every time; `--seed 2` gives a different choice, `--sets 5` fewer sets,
`--target 67` one final-padlock target for every set (the build fails, naming each set and why, if any cannot make it). Any
failed check prints `BUILD FAILED` with the reason, and no PDF is written.

Print it **at 100% (actual size), A4, double-sided off**. It is designed to print in black and white.

## What to proofread

1. **Teacher notes (page 1): marked DRAFT for your wording.** Drafted from the room and its teacher page. Send your
   wording to Code Claude: it goes into `build_pack.py`, and the DRAFT badge comes off in the same change.
2. **Score sheet (page 2, landscape):** two blanks the teacher fills in first ("Each wrong answer adds ___ min",
   "Each hint adds ___ min", Amendment 6); one row per set, letters printed; for each lock an Opened box and five
   wrong-answer boxes; the final padlock's Opened box and five wrong-answer boxes, like a lock's; finishing time, the counts of wrong answers and hints, penalty (min)
   and total time. Checking is per lock as teams go (Amendment 3): right ticks Opened, wrong checks a box and gets
   "not yet". Total time = finishing time + (wrong answers x the first) + (hints x the second). No fixed penalty
   figure is printed on the score sheet or any student page; the teacher notes suggest 1 minute each.
3. **Answer key and worked solutions (pages 3-4):** every answer, common wrong answer and worked line was recomputed
   by a separate method before the PDF was made, so a mismatch would have stopped the build. The key also gives each
   set's final-padlock target and its one expression; the worked solutions show its working. Spot-check one set
   against its cover and evidence pages anyway: that is what a teacher will do.
   **The final padlock (Amendments 5 and 7):** each set's lock answers, each once, with one x and one + or - and no
   brackets, make the set's target. Every set in a pack uses that same shape, so they are equally hard: a whole
   number of any size, made by exactly one expression of any shape (up to the order of its parts), never the plain
   sum, never one of the answers, worked in whole steps. A set with no such target fails the build. Calculator
   allowed for the final padlock only; the teacher notes say so. Option B (one + and one -, no calculator) is
   `"final_shape": "plus-and-minus"` in the room's config.
4. **Each set (cover, evidence pages 1-2, locks page):** the set letter is in the top-right box of every page; the
   figures printed on each object (asset tag, cable label, installation sheet, calibration log, instruction card)
   read clearly; the three red herrings (helpdesk ticket, emergency stop, firing screen) carry no number; the cover's
   answer boxes show only each instrument's picture, label and unit (Amendment 4: no digit slots, range or maximum);
   the locks page ends with the final padlock's target, its rules, a working box and the expression line.
5. **The look of the labels on the art:** each label is fitted to its box at 11 pt or larger. If one sits badly on
   its picture, its box is `label_box` in `rooms/kiln-disaster/config.json` (in the image's own pixels).
6. **Hint cards and certificate (last two pages).**
7. **Footer:** the MaffsGames logo and name, the room, pack version, seed and build date on every page. Give a
   buyer's question the version and seed from the footer and the pack can be rebuilt exactly.

## How it works

`build_pack.py` holds no room's facts. For a room it reads:

- `escape-rooms/<slug>/room.js`, evaluated in a blank Chromium page (as the room page evaluates it), and the `TEACH`
  block of its `teacher.html` (topics and minutes). The pages themselves are never loaded, and the browser has no
  network: fonts come from the repo's pinned copies.
- `escape-rooms/variants.json`, the verified variant libraries (room.js must equal them).
- `rooms/<slug>/config.json`: the art files and their roles (`clue`, `herring`, `answer`), each image's label box in
  image pixels, the font per card (`label`: Oswald; `hand`: Permanent Marker), the number of sets, the seed, the pack
  version, the certificate title and the words printed on each red herring (which must come from that object's
  flavour text in room.js and contain no digit).

Then, in order, any failure stopping the build:

1. `scripts/check-escape-rooms.py` is imported unchanged, which runs the whole room check; its `draw_is_valid()` and
   `clue_strings()` are the rules the room engine serves draws by.
2. **Selection:** every joint draw (one variant per lock) is judged VALID or not; from the VALID ones, a seeded
   search picks the sets so that no lock's answer repeats across them.
3. **Verification:** `lockcheck.py` recomputes every answer, common wrong answer and worked-solution figure from each
   variant's givens, by its own method (it imports neither the variant generator nor its set checks).
4. **Render and check:** the pages are built as HTML and printed by Chromium. Before the PDF is written: every label
   fits its box at 11 pt or more (one line if it can, else balanced lines), no page overflows, every student page
   shows its set letter, no red herring shows a digit, no `{{token}}` is left unfilled, every footer carries the
   logo and name under 12 mm high, and the one URL printed (on the covers and teacher notes) resolves to the room's
   own live page in this repo (host from `CNAME`), and the score sheet has exactly one row per set and one column
   group per lock, with its Final padlock column. Every final target is re-evaluated from its printed expression and
   all expressions are re-searched, by `lockcheck.py`'s own evaluator. The PDF's page count must equal the pages built.

`python -X utf8 tools/pack-generator/build_pack.py --selftest` (in CI as `scripts/test-pack-generator.py`) checks
every room with a config and plants ten faults, each of which must be caught: a duplicate answer across sets, an
invalid joint draw, a wrong recomputed answer, a printed URL with no room page, a missing score-sheet row, a final
target two expressions reach and one no expression reaches, a fixed penalty figure ("1 minute") on the score
sheet, a pack whose sets use different final-padlock shapes, and a range and digit slots on answer boxes. It builds
no PDF.

## Adding a room

1. `rooms/<slug>/config.json` with its art in `rooms/<slug>/art/` (each image at most 250 KB).
2. Each of the room's locks in `lockcheck.py`'s `RECOMPUTE`, by lock id, recomputed its own way. The build refuses a
   room with a lock missing there.
3. Build, then proofread as above.

## Fonts

`fonts/Oswald-Variable.ttf` (SIL Open Font License 1.1, `fonts/Oswald-OFL.txt`) and
`fonts/PermanentMarker-Regular.ttf` (Apache License 2.0, `fonts/PermanentMarker-LICENSE.txt`), both from
`github.com/google/fonts`. Outfit comes from the repo's pinned copies in `scripts/fonts/`.
