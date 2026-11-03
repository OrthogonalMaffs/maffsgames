# DASHBOARD-METRICS (received 3 Nov 2026, 16:05, cloud lane, Claude Code)

Saved verbatim on receipt (canon §7.8.2, CONTRACTS-FOLDER), with SEQ-SOLVER-FIXES and SEQ-SOLVER-WORKED in Jon's
hand-off of 3 Nov 2026, 16:05 (the hand-off note is in `2026-11-03-seq-solver-fixes.md`). Starts after
SEQ-SOLVER-WORKED merges.

**Earlier wording (superseded):** #650 (main b18b064, 3 Nov) stored an earlier text of this contract from the archived
session. The text below is Jon's 16:05 hand-off, which replaces it; the earlier text stays in git history at b18b064.

Before starting, three facts found on receipt (3 Nov; recorded with the earlier wording, kept here verbatim):
- Every room's slug starts "escape-" (all 14 room.js files) and the engine logs that slug, so the prefix holds.
- docs/apps-script-endpoint.js does not use UrlFetchApp yet: adding it makes Google ask Jon to grant "connect to an
  external service" on the redeploy. Put that in Jon's redeploy step.
- Jon redeployed the endpoint after QUESTION-ID (#649) and said "we have a newer version which will help us". If the
  live script differs from docs/apps-script-endpoint.js, get the live code from Jon BEFORE editing the file, or this
  contract's redeploy would overwrite his changes. Asked on 3 Nov; answered by Amendment 1 below (the live code matches the file).

## Contract (verbatim)

CONTRACT: DASHBOARD-METRICS
Tier: Shared · Lane: cloud · Implementer: Claude Code (cloud)

START
After SEQ-SOLVER-WORKED merges.

TASK
Make the daily email and Dashboard report each kind of game by a measure that means something for it: accuracy and
hardest questions for question games, escapes and attempts per lock for escape rooms, and question games' hardest
questions named by question_id rather than round position.

ROOT CAUSE
The dashboard ranks every game by accuracy (min 5 answers) and its hardest questions by round position. For escape
rooms "correct" is logged once per lock opened while every wrong try is logged, so a room that is escaped scores
about 25-35%; for Trig Wars "correct" means a shot hit. Both fill the bottom of the table without anything being
wrong (Project Claude, checked 3 Nov 2026: Rugby Mud's and The Rightful King's answers all correct and settable).
Round position names no question because games shuffle; question_id now does (QUESTION-ID, #649). A minimum of 5
answers lets one student top the table. Wrong answers before 29 Sep 2026 ~20:00 UTC are stored blank, so any figure
that ignores blanks reads 100% for that era.

CLASS CHECK
Yes: the dashboard's measure is chosen per row, not per kind of game. Fix it once by giving each game a kind in its
single metadata record (data/games.json, for games; slug prefix "escape-" already identifies rooms, by convention),
and have the Apps Script read it; never a hand-kept list of slugs inside the script.

EXACT CHANGE
1. data/games.json: an optional "answer_kind" per game: "question" (the default when absent) or "shot" (correct means
   an attempt hit, not an answer). Survey every game's question_answered call and set "shot" where that is what it
   logs; list each one set, with the line, in the PR. Rooms need no entry.
2. docs/apps-script-endpoint.js: at report time fetch https://maffsgames.co.uk/data/games.json (UrlFetchApp, cached
   for the run); if the fetch fails, carry on treating every game as "question" and say so in one line of the email
   and dashboard. Then, in both the email and the Dashboard tab:
   a. Question games: accuracy by game, minimum 30 marked answers; overall accuracy from question games only.
   b. Hardest questions: question games only, keyed game + level + question_id, minimum 10 attempts; rows without a
      question_id are left out, and the heading says how many games send it yet. Show the id so it can be decoded with
      scripts/decode-question-ids.py.
   c. Escape rooms (slug "escape-"): per room, games started, rooms escaped (game_completed), escape rate, and attempts
      per lock opened (marked answers / correct answers); sorted by escape rate.
   d. Shot games: hits per round, or a single line naming them as left out of accuracy; one, not both.
   e. Any accuracy over a window that reaches before 2026-09-29T20:00Z counts a blank correct as wrong for those rows.
   Bump SCRIPT_VERSION; deploy notes in docs/apps-script-redeploy.md (new version of the existing deployment).
3. Tests in the style of scripts/test-apps-script-counts.py: run the report logic on fixture rows covering a question
   game, a room, a shot game, rows with and without question_id, a failed games.json fetch and pre-29-Sep blanks;
   plants: a room counted in accuracy, a row with no question_id in hardest questions, a minimum below 30, a blank
   pre-29-Sep row ignored instead of counted wrong; each CAUGHT.
4. Canon §1: the dashboard's measures and the answer_kind field, with the reason in §12.

DO NOT TOUCH
doPost and the Sheet's columns; the counts script (docs/apps-script-counts.js); game files; GA4 settings; Gate files.

SUCCESS CONDITION
Fixture tests and plants pass; answer_kind set and listed for every shot game; a sample email and dashboard layout
from fixtures in the PR; Gate green; Shared review by Project Claude; stop for Jon's "merge"; handover lists Jon's
redeploy step (new version of the existing deployment; /exec reports the new version); Record line.

STOP IF
A game's question_answered is neither an answer nor a shot (list it for Jon); the live games.json cannot be fetched
from Apps Script at all; the change would alter doPost or the Sheet's columns.

## Amendment 1 (Jon, 3 Nov 2026, verbatim)

Ruling (Jon, 3 Nov): the live endpoint matches docs/apps-script-endpoint.js. On 3 Nov at 15:45 Jon replaced Code.gs
with the repo file in full for QUESTION-ID's redeploy, and /exec reports 2026-11-03-a. The earlier question about a
newer deployed version is superseded. DASHBOARD-METRICS may edit the repo file as its contract says; Jon will grant the
"connect to an external service" permission at redeploy. The older queue items in the cloud handover stay parked:
do not start any of them.
