# ROOM-ESCAPED (received 4 Nov 2026, cloud lane, Claude Code)

Saved verbatim on receipt (canon §7.8.2, CONTRACTS-FOLDER).

## Contract (verbatim)

CONTRACT: ROOM-ESCAPED (cloud lane, Shared; Jon, 4 Nov 2026)
LANE: docs/apps-script-endpoint.js and scripts/test-apps-script-report.py only (as DASHBOARD-METRICS). Save this
contract verbatim as docs/handover/contracts/2026-11-04-room-escaped.md in the first commit, with one line in
docs/handover/cloud.md's queue, ahead of SEARCH-KEYWORDS.

TASK: The daily email and the Dashboard count a room as escaped only when the student escaped, not when the
clock ran out.

ROOT CAUSE: escape-rooms/assets/engine.js finish(win) sends game_completed for both outcomes (win and timeout,
:900-916). rptBuild() in docs/apps-script-endpoint.js counts every game_completed for an escape- slug as escaped.
Evidence, report of 3 Nov: escape-rightful-king "1 escaped, no lock opened" and escape-pe-shed-rebellion the same,
which is impossible for a real escape.

CLASS CHECK: Not a class needing a wider fix. The counting lives in one shared function, rptBuild(), which already
feeds both the email and the Dashboard, so fixing it there fixes every reader. The engine's event is correct
(a room ending is a completion, and its questions_correct says how many locks opened); only the report's reading of
it is wrong. The overview's "Games completed" and TOP GAMES "completed" mean "finished", which a timeout is, and
stay as they are.

EXACT CHANGE:
1. rptBuild(): a room row with event game_completed counts as escaped only when questions_correct equals
   questions_answered and both are numbers greater than 0 (finish(true) fires only when every lock is open). Add
   a "timed out" count per room (game_completed that is not an escape).
2. The rooms line in the email and the Dashboard's rooms table: "N started, E escaped (rate), T timed out, ...".
   Escape rate stays escaped / started.
3. SCRIPT_VERSION -> 2026-11-04-a. docs/apps-script-redeploy.md: note the version (no new permission needed).
4. scripts/test-apps-script-report.py: rows for a win (3/3), a timeout (1/3) and a timeout with 0 locks; assert
   escaped 1, timed out 2. Planted fault: counting every game_completed as escaped must fail.

DO NOT TOUCH: escape-rooms/ (the engine and every room); doPost and the Sheet's columns; analytics.js; every other
section of the report; data/games.json; canon (put a one-line note for the home lane in docs/handover/cloud.md).

SUCCESS CONDITION: The test passes with its planted fault caught; main green; the PR stops at a green Gate for
Project Claude's review and Jon's "merge"; after Jon redeploys, the next report never shows an escape with
"no lock opened"; the work is committed and docs/handover/cloud.md records the state, so the home session knows
where it stands.

STOP IF: any room's game_completed rows in the Sheet's last 7 days have blank questions_correct or
questions_answered (report how many; the test needs a different signal); a room exists whose win is not
"every lock open"; the fix needs any change to the engine or to what the Sheet stores.

## Found on receipt (4 Nov, Claude Code)

- No SEARCH-KEYWORDS item is in docs/handover/cloud.md's queue on main (921f7fb); this contract's line is put first
  among the queue's items, which is "ahead of" anything added after it.
- STOP IF 2 clear: every live room loads escape-rooms/assets/engine.js (it-vengeance is a redirect to
  rightful-king), no room.js calls finish or mfg, and finish(true) fires only at engine.js:756, when every lock is
  open.
- STOP IF 1, checked from code, not from the Sheet: the Drive connector can see "MaffsGames Events" (1.1 MB) but
  returns content inline, too large to read in a session. On origin/main the engine has sent
  questions_answered: R.locks.length and questions_correct: opened on every game_completed since at least 15 Oct
  (the history's repack root), engine.js has had no commit since 24 Oct, analytics.js forwards every param, and
  doPost's cellValue blanks only undefined and null, so a 0 is stored as 0. A blank in the 7-day window would need a
  page cached from before 15 Oct. Jon can confirm with one Sheet filter before redeploying (in the PR).
