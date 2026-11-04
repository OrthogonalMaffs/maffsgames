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

AMENDMENT 5 to PACK-GENERATOR (Jon, 4 Nov): a final code. Applies to every pack.
- After the room's locks, each set has a final step, "The final padlock": use each of the set's lock answers exactly
  once, with + - x and / only, NO brackets (normal order of operations applies), to make the set's target number.
- Target per set, chosen by the generator from that set's answers: a whole number from 10 to 999; reachable by
  exactly one expression (counting a+b and b+a, a*b and b*a, as the same); prefer targets whose expression uses
  x or /; never one that is just the sum of the answers. Option --target 67: use 67 for every set if every set can
  reach it under these rules, otherwise fail the build with the sets that cannot. Default: per-set targets.
- Student pages: the target and the rules on the locks page, with a working box and an answer line for the
  expression. Score sheet: a "Final" tick column before finishing time; a team finishes when the final padlock is
  ticked. Answer key: each set's target and its one expression, worked with the order of operations shown; note
  that the teacher accepts any expression that evaluates to the target under these rules.
- Independent verification: recompute each target from its expression by a separate evaluator, and re-search all
  expressions to confirm exactly one hits the target. Selftest: a planted target with two expressions, and one with
  none, are each caught.
Record this amendment verbatim in the saved contract and the PR body.

(No Amendment 4 reached the cloud session; Amendment 5 is recorded as received.)

AMENDMENT 6 to PACK-GENERATOR (Jon, 4 Nov): penalties are the teacher's choice. Overrides the fixed 1-minute
penalties in Amendments 3 and 4.
- Score sheet header: two blanks the teacher fills in before the game: "Each wrong answer adds ___ min" and
  "Each hint adds ___ min". Total time = finishing time + (wrong answers x the first) + (hints x the second).
  Column headings say "Wrong answers" and "Hints" (counts), then "Penalty (min)" and "Total time".
- Teacher notes: "We suggest 1 minute for each wrong answer and 1 minute for each hint. You know your class:
  set your own before you start, and tell the teams." (Still DRAFT for Jon's wording.)
- Cover-sheet line for students: "Bring each answer to your teacher. Wrong answers and hints add time; your
  teacher will tell you how much." (no figure printed).
- Selftest: no fixed penalty figure appears on the score sheet or any student page (a planted "1 minute" is caught).
Record this amendment verbatim in the saved contract and the PR body.

(Amendment 6 overrides Amendment 4's penalty, but Amendment 4 itself never reached the cloud session; hints are
counted on the score sheet as Amendment 6 says. Anything else Amendment 4 asked for is not in this pack.)

AMENDMENTS 2 AND 4, AS RECEIVED LATE (Jon, 4 Nov: "Amendments 2 and 4 were sent earlier but never reached you; here
they are, then Amendment 7.")

AMENDMENT 2 (Project Claude's rulings on #659, for Jon):
1. scripts/test-pack-generator.py and the _config.yml "- tools" exclusion: both accepted (the exclusion is essential).
2. Evidence on two pages: accepted.
3. Oswald and Permanent Marker with their licences: accepted (OFL and Apache 2.0 allow embedding in a sold PDF).
4. tools/ missing from ci-deps.py: not in this PR; one line under "For Project Claude to triage" in cloud.md.

AMENDMENT 4 (only the part not overridden by Amendment 6): answer boxes give nothing away. No digit slots, no dial
or slider range, no maximum on student pages; each box shows the instrument's picture, its label and the unit only.
The answer key keeps everything. Selftest: a planted range or digit-slot hint on a student page is caught.

AMENDMENT 7 (Jon, 4 Nov): the final padlock must be equally hard for every set, because sets race each other.
- Every set in a pack uses the same expression shape: one x and one + or - (in either order, no brackets, order of
  operations applies). No / and no +/- only targets. Target = a whole number, any size, never one of the set's own
  answers, reachable in exactly one way under your existing sameness rule. If any set cannot get such a target, fail
  the build naming it (do not fall back to an easier shape).
- The final padlock is "calculator allowed"; say so on the locks page and in the teacher notes. The rest of the room
  stays as it was. Fix the teacher notes so "no calculator needed" applies to the locks only.
- Score sheet: the Final column gets the same wrong-answer boxes as the other locks; a wrong final expression costs
  the teacher's penalty like any other wrong answer.
- Keep your two added rules (target never one of the set's answers; key worked in whole, non-negative steps).
- Selftest: a pack whose sets use different shapes is caught.
(Option B instead: replace the first bullet's shape with "only + and -, exactly one of each" and drop the
calculator bullet.)
Record Amendments 2, 4 and 7 verbatim in the saved contract and the PR body.

AMENDMENT 8 to PACK-GENERATOR (Jon, 4 Nov): the room's ending is the teacher's to call. Applies to every room.
- In room.js, `stakes` is the timeout outcome (the online room shows it only on the fail screen) and `win` the escape
  outcome. The pack printed `stakes` as part of the opening, in "Read this out" and on every cover. Fix in the
  generator, not in any room.
- Teacher notes: three read-outs, each labelled with its moment: "Read this at the start" (hook and brief),
  "Read this when a team finishes" (win), "Read this when you call time" (stakes).
- Cover sheets: hook and brief as now; `stakes` only as a warning, prefixed "If time runs out: ".
- Selftest: a planted `stakes` text appearing unprefixed on a cover, or inside the start read-out, is caught.
Record this amendment verbatim in the saved contract and the PR body.

AMENDMENT 9 to PACK-GENERATOR (Jon, 4 Nov): the teacher notes overload the teacher. Applies to every room.
- Page 1 becomes "Run it": numbered steps under "Before the lesson" and "In the lesson", AT MOST 150 words, using
  Project Claude's draft below verbatim (still marked DRAFT for Jon's wording).
- Page 2 becomes "Read-outs": the three boxed scripts from Amendment 8 (start, a team finishes, you call time). The
  start script ends with one line to the students: "Bring each answer to me. Wrong answers and hints add time.
  Lowest total time wins."
- Everything else from the old notes moves, shortened, to an "About this room" box at the top of the answer key: the
  pack contents in one line, each lock's topic and rough time, the grade, the final padlock's shape and target range,
  and that the key's common wrong answers are for the debrief. No repeated rules.
- Score sheet footer: the checking rule in two short lines ("Right: tick Opened. Wrong: check a box, say 'not yet'.
  Total time = finishing time + penalties. Lowest wins.").
- Selftest: page 1 over 150 words, or the same rule stated on more than one teacher page, is caught.
DRAFT for page 1:
Before the lesson
1. Print one set per team (A-G). Cut out the hint cards.
2. Choose your penalties. We suggest 1 minute per wrong answer and 1 per hint.
In the lesson
1. Hand out the sets face down. Tell the teams your penalties.
2. Read the start script (page 2). Start a timer, counting up.
3. Teams bring each answer to you. Check it against their set in the key.
   Right: tick it. Wrong: check a box and say "not yet".
4. A team wants a hint? Hand over the card and add one to Hints.
5. Final padlock ticked: write down the time.
6. Call time when you choose. Read the ending that fits. Lowest total time wins.
Final padlock: calculators allowed. Any calculation that makes the target counts.
Record this amendment verbatim in the saved contract and the PR body.

AMENDMENTS 10 and 11 to PACK-GENERATOR (Jon, 4 Nov). Please apply both, then record them verbatim in the saved
contract and the PR body. Thank you.

AMENDMENT 10:
1. (Superseded by Amendment 11's page 1 line; no change needed for the old wording.)
2. Prefix: keep "If time runs out:" on paper. Online the warning reads "If you get it wrong." because a wrong setting
   can trigger the fail picture there; on paper only time can. No change to the engine.
3. Page 1, under "Before the lesson" step 1: one line giving each set's pages, generated from the build, e.g.
   "Each set is 4 pages: A 5-8, B 9-12, ...". Counted in the 150-word limit.
4. Keep the DRAFT badges on Run it and Read-outs until Jon says "wording final".

AMENDMENT 11: the final padlock was made trivial by Amendment 7 (shape given away, calculator allowed: six tries).
Replaces Amendment 7's student-facing rules and its calculator line.
- Students are told only: use each of your three answers exactly once, any of + - x /, no brackets (order of
  operations applies), NO calculator, make the target. The shape is not printed anywhere a student sees.
- Fairness stays behind the scenes: every set's one solution has the same shape (one x and one + or -), and is the
  only expression of any shape that makes the target (your existing re-search over all expressions).
- Every set's product must be mental- or quick-written-method friendly: one factor a multiple of 5, or 12 or less.
  Add this to set selection: choose the N joint draws so every set has such a target (still VALID, still distinct
  answers per lock, deterministic for the seed). If N such sets do not exist, fail the build naming the count.
- A hint card for the final padlock, after the locks' hints: "Is the target close to a round number? Which two of
  your answers multiply to about that?" Counted as a hint like any other.
- Page 1 final-padlock line: "No calculator. Any calculation that uses each answer once, with + - x / and no
  brackets, and makes the target counts (only one does)." "About this room": the shape, the target range, and that
  estimation is the intended route, for the teacher only.
- Selftest: the shape printed on a student page, a calculator allowance on a student page, or a set whose product
  has neither factor a multiple of 5 nor 12 or less, are each caught.
