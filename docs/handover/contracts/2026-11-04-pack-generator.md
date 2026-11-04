PRE-STEP (Jon, 4 Nov): in this contract's first commit (1) close out PACKS-CANON (contract file to
docs/history/contracts/, DONE in cloud.md's queue); (2) correct cloud.md: Jon redeployed ROOM-ESCAPED at 09:02 on
4 Nov and /exec reports 2026-11-04-a, so that step is done; (3) before adding anything else, move DONE prose out of
the queue section verbatim into docs/history/handover-cloud-archive.md (as on 4 Nov) so the size check passes without
its warning, now and after this contract's own close-out.

CONTRACT: PACK-GENERATOR (cloud lane, Shared; Jon, 4 Nov 2026)
Moved from the home lane to cloud (Jon, 4 Nov). PACKS-CANON is merged (c693a17). LANE EXCEPTION, THIS CONTRACT ONLY:
you may create tools/pack-generator/ and edit .gitignore. Save this contract verbatim as
docs/handover/contracts/2026-11-04-pack-generator.md in the first commit, with one line in docs/handover/cloud.md's queue.

TASK: Build a room-agnostic generator that turns an escape room's checked variants into a printable A4 group-race
pack (PDF), piloted on The Kiln Disaster with 7 sets (A-G).

ROOT CAUSE: New capability: no offline version of any room exists. Jon will sell packs on Tes (canon §7.1 as amended
by PACKS-CANON). The risk to design against is drift: every figure, answer and worked solution must come from the
room's own checked data (room.js, escape-rooms/variants.json, verified in CI), never typed. The repo is public, so
the built PDF (the product) must never be committed or published anywhere, including CI artifacts.

CLASS CHECK: Yes: the generator will serve every room, so it holds no Kiln-specific logic. Per-room facts (art files,
label boxes, fonts per card, set count) live in a per-room config. It reuses the repo's existing room parser and
scripts/check-escape-rooms.py's draw_is_valid(); it does not write second copies of either.

EXACT CHANGE:
1. tools/pack-generator/: build_pack.py <room-slug> [--sets N] [--seed S], README, and rooms/kiln-disaster/config.json
   (sets 7; for each of the 11 images: file, role, and the label box in image pixels; font per card: label font for
   printed labels, handwritten-style font for the cable label and the helpdesk sign-off).
2. Art: Jon's 11 images are at the root of branch art/kiln-pack. Save each as
   tools/pack-generator/rooms/kiln-disaster/art/kiln-NN-<id>.webp, optimised, at most 250 KB each, per this mapping
   (Project Claude, checked 4 Nov; confirm visually, stop only if one clearly contradicts it):
     01 asset-tag        <- Wall-Mounted Electrical Control Panel.png (blank white label strip = the tag)
     02 cable-label      <- Masking Tape Label on Ethernet Cable.png
     03 install-sheet    <- Worn Paper Form with Coffee Stain.png
     04 calibration-log  <- Clipboard Log with Highlighted Row.png
     05 instruction-card <- Laminated Blank Instruction Sign.png
     06 helpdesk-ticket  <- Comic-Style Folder and Job Ticket.png
     07 stop-button      <- Emergency Stop Button and Blank Sign.png
     08 firing-screen    <- Industrial Control Panel with Red Accents.png
     09 keypad           <- Retro Keypad Panel Illustration.png
     10 dial             <- Teal-Tipped Selector Control Panel.png
     11 slider           <- Teal-Accented Slider Control Panel.png
   Cover art reuses docs/art/kiln-disaster-scene.webp and the certificate docs/art/kiln-disaster-win.webp (read, not
   copied).
3. Selection: choose N joint draws (one variant per lock) that are each VALID by draw_is_valid(), with every lock's
   answers distinct across the N sets. Deterministic for a given seed; the seed and pack version print in the footer.
4. Independent verification before rendering: recompute every answer by a separate method (sensor: the largest
   multiple of k not above L by enumeration; fan: LCM by enumerating multiples; check value: a + b / c with the
   division first). Any mismatch with the variant's answer fails the build.
5. Render HTML to PDF with the pre-installed Playwright Chromium, A4, black-and-white printable. Pages:
   a. Teacher notes (1 page): set-up in under two minutes, a short script to read out, how checking works (teams bring
      the completed cover sheet; first fully correct sheet wins; a wrong sheet goes back with "not yet"), timing is the
      teacher's choice. Drafted from room.js and teacher.html; marked DRAFT for Jon's wording.
   b. Answer key: one table, set x lock, giving the answer and the common wrong answer (variant miss) with its
      misconception (lock missTitle); then worked solutions per set from each lock's solve string, filled.
   c. Per set: cover sheet (scene art, hook, brief and stakes from room.js, team name line, set letter large, three
      answer boxes using images 09-11 with each lock's instrument label); evidence page (the 8 objects as cards, clue
      text filled from the set's figures and printed into each image's label box, object name and "where" as caption;
      red herrings carry their flavour text, never a number); locks page (each lock's brief and working space). Every
      student page carries "Set C" (etc.) prominently.
   d. Optional, at the end: hint cards (each lock's three hints, cut-out) and a "Kiln opened" certificate (win art).
   e. Footer on every page: room slug, pack version, seed, build date.
6. Output to dist-packs/ (add it to .gitignore). Never commit a built PDF; never upload one as a CI artifact or
   anywhere else. Build it in the session only to run the checks.
7. --selftest (ci-line, no PDF in CI): plants a duplicate answer across sets, an invalid joint draw, and a wrong
   recomputed answer; each CAUGHT.
8. README: the one command Jon runs at home to build the PDF, and what to proofread.

DO NOT TOUCH: room.js, escape-rooms/variants.json, scripts/gen-escape-variants.py, scripts/check-escape-rooms.py (import
only); any live page, the escape-rooms hub, sitemap, analytics; no link to packs anywhere on the site; canon; other
rooms; docs/handover/home.md; branch art/kiln-pack (read only; leave it for Jon to delete).

SUCCESS CONDITION: build_pack.py kiln-disaster builds dist-packs/kiln-disaster-pack.pdf in the session; verification
passes for all 21 answers; answers distinct per lock across A-G; every joint draw VALID; set letter on every student
page; no number on any red herring; selftest plants caught in CI; no built file in git status, any Pages-served path or
any CI artifact; the handover size check passes without its warning; Gate green; the PR body describes each page type
and gives the image mapping for Project Claude's review; stop for Jon's "merge"; the work is committed and
docs/handover/cloud.md records the state, including that Jon builds and proofreads the PDF at home with the README's
command.

STOP IF: branch art/kiln-pack is missing, has other than 11 images, or an image clearly contradicts the mapping;
fewer than 7 joint draws meet the rules (report the count); the longest clue cannot fit its label box at 11 pt or
larger (report which); the existing parser or draw_is_valid() cannot be imported without changing them; the PDF build
needs any dependency in the live site; any built file would land in a Pages-served path or a CI artifact.

AMENDMENT 1 to PACK-GENERATOR (Jon, 4 Nov): branding.
- Every page carries the MaffsGames logo (schools/assets/m_plus_logo.svg, read, not copied) and the name
  "MaffsGames" in the footer, small and black-and-white printable, beside the existing slug/version/seed/date.
- The cover sheet and teacher notes carry: "Play this room free online: maffsgames.co.uk/escape-rooms/kiln-disaster/"
  (the room's own URL, taken from the repo, not typed). No other URL, no homepage advert, no QR code, nothing about
  prices or other products, and no Tes branding anywhere.
- Add a check to the build: the URL printed resolves to an existing room page in the repo.
- The logo must not crowd the student pages: footer only on those, under 12 mm high.

AMENDMENT 3 to PACK-GENERATOR (Jon, 4 Nov; replaces any earlier Amendment 3 text): per-lock checking and a
teacher score sheet.
- Checking changes from "bring the completed cover sheet at the end" to per lock: a team brings each lock's answer
  to the teacher as they go. Right: the teacher ticks that lock. Wrong: the teacher checks one box in that lock's
  wrong-answer boxes and says "not yet", no explanation.
- Finishing time: read from the room timer (one timer for the whole class, started together) when the team's last
  lock is ticked. Total time = finishing time + 1 minute per wrong answer. Lowest total time wins.
- New page after the teacher notes: "Score sheet", one A4 table, landscape if needed: one row per set (A-G, letter
  pre-printed), columns: Team name | Set | for each lock: Opened (one tick box) and Wrong answers (a row of 5 small
  check boxes) | Finishing time | Penalty (minutes) | Total time. Room-agnostic: lock columns come from the room's
  locks, rows from --sets.
- Teacher notes: rewrite "how checking works" to match, including "use one timer for the whole class, counting up"
  (still marked DRAFT for Jon's wording).
- Cover sheet: one line for students, "Bring each answer to your teacher. Every wrong answer adds a minute to your time."
- Selftest: the score sheet has one row per set and one column group per lock (a planted missing row is caught).
Record this amendment verbatim in the saved contract and the PR body.

(No Amendment 2 reached the cloud session; Amendment 3 is recorded as received.)
