HOME LANE QUEUE, 9 Oct 2026 (Project Claude; Jon's rulings 9 Oct). Save each contract
verbatim under docs/handover/contracts/ as it starts. The standing rule applies: start
the next item when one merges with main green. Stop for a STOP IF, an unruled decision,
or an empty queue. Checkpoint after item 4.

JON'S RULINGS on the overnight questions (9 Oct 2026). Record them in item 1:
- unit-converter: on MaffsLock since #196, so move it from NOT_YET to MIGRATED.
- wrong-on-the-internet: keep the 3 s pause before Try again. Feedback on a wrong
  answer is shown, not skipped (Jon's rule of 8 Oct).
- complex-converter: keep Play Again replaying the mode just played, provided the mode
  menu is still one tap away from the end screen. If it is not, add a "Choose mode"
  button there (item 1).
- graph-sketcher: fix its phone overflow now, then put it on the lock (item 2).

======================================================================
ITEM 1

TASK (home lane, RULINGS-9OCT): Record Jon's rulings of 9 Oct on the
overnight questions, and act on the two that need a change.

ROOT CAUSE: The overnight run (#198-#200) asked Jon four questions; he
ruled as above. unit-converter loads MaffsLock (#196) but is not in
MIGRATED, so the check only judges it as a game outside the list.

CLASS CHECK: Not a bug: bookkeeping plus one small UI check. Local.

EXACT CHANGE:
1. check-answer-lock.py: move unit-converter into MIGRATED (seeds 1-3
   must pass; they did in #196).
2. complex-converter: confirm in Chromium that the end screen offers a
   way back to the mode menu in one tap. If not, add a "Choose mode"
   button beside Play Again, through MaffsLock.screen like the rest of
   the game's screen changes.
3. Record all four rulings in docs/handover/home.md and canon where
   behaviour rules live (wrong-on-the-internet's pause under §7.6;
   Play Again replaying the mode as allowed behaviour).
4. Handover updated.

DO NOT TOUCH: the pause length; any other game.

SUCCESS CONDITION: the lock check passes with unit-converter in
MIGRATED; complex-converter's end screen reaches the menu in one tap;
merged on a green Gate; main green.

STOP IF: unit-converter fails any seed (report it to the cloud lane via
the handover; leave it outside MIGRATED).

======================================================================
ITEM 2

TASK (home lane, GRAPH-SKETCHER-FIT): Fix Graph Sketcher's phone
overflow (todo §3.9), then put it on MaffsLock. It is the last listed
game on NOT_YET.

ROOT CAUSE: Graph Sketcher's page is wider than a phone, so the browser
zooms out. In the overnight run a tap on Next landed on the footer's
"Parent guides" link instead, for a student as much as for the check.
That is a broken game on phones today (priority 1), not just a check
failure.

CLASS CHECK: Probably local to this page's layout: its own fixed widths
(a canvas or table wider than the viewport). Check that first. If the
overflow comes from a shared stylesheet or component that other games
use, fix it there, and list the other games it affects. The lock
itself is the existing F1 pattern.

EXACT CHANGE:
1. Measure the overflow at 320x568, 390x844 and 412x915 (the element
   and its width). Fix it at its source, for example a canvas sized to
   its container with drawing scaled to it, or a table that wraps or
   scrolls inside its own box, never the page.
2. The curve-drawing input must still work by touch at 390x844. Check
   in Chromium with touch.
3. Then the F1 pattern: MaffsLock and MaffsNext with its lock-hint
   declaration; seeds 1-3 pass; remove it from NOT_YET; record any real
   faults found, as in the batches.
4. Close todo §3.9's graph-sketcher part; handover updated.

DO NOT TOUCH: its scenarios and marking (apart from the lock); other
games, unless CLASS CHECK finds a shared cause; the footer.

SUCCESS CONDITION: no sideways scroll and no page zoom at the three
sizes; Next is tappable at 390x844; the lock check passes; NOT_YET
holds only glorious-gantt; merged on a green Gate; main green.

STOP IF: fitting the page needs the drawing area so small that drawing
by touch stops working (screenshot, and say what size it needs); the
cause is shared and touches more than five other games (list them, and
ask Jon before changing them).

======================================================================
ITEM 3

TASK (home lane, PLAY-AGAIN-SCREEN): Stop a double-click on Play Again
from landing on the menu's next control (the leaderboards link in many
games), across every game.

ROOT CAUSE (reported by the cloud lane, 8 Oct): about 25 games' Play
Again calls showMenu(){ show('menu') } directly. The menu appears under
the pointer at once, so the second click of a double-click lands on
whatever sits there, often the /leaderboards/ link. The student leaves
the game. On main, 32 game pages call show('menu') and 38 already use
MaffsLock.screen(). The lock check only catches it where the layout
happens to line up.

CLASS CHECK: A bug class: the same shape in many games, and the absence
of safety on a screen change called from many paths. The architectural
fix exists: MaffsLock.screen(container), which opens the 300 ms fresh
window on the new screen (canon §7.6.0). Every screen change goes
through it. Patching the menu's link in each game would be the wrong
fix.

EXACT CHANGE:
1. Every listed game's screen changes (Play Again, back to menu, mode
   select, results) go through MaffsLock.screen(). Convert the 32 pages
   still calling show('menu') directly, as one batch PR or two batches
   of 16, as the CI time allows.
2. check-answer-lock.py, or a new check with a ci-line header: for every
   listed game, finish a session, double-click Play Again, and assert
   that the page is still on the game's own page, on the expected
   screen, with nothing else activated. Plant one game with a bare
   show('menu'); it must fail.
3. Canon §7.6.0: "every screen change goes through MaffsLock.screen()".
4. Handover updated.

DO NOT TOUCH: game content and marking; the leaderboard pages;
cloud-claimed games (read cloud-remaining: first, and leave any claimed
game for a later batch).

SUCCESS CONDITION: the new check passes on every listed game and fails
on the plant; no page calls show('menu') except through
MaffsLock.screen; merged on a green Gate; main green.

STOP IF: a game's screen change can't go through MaffsLock.screen
without changing its flow (describe it); the check needs more CI time
than the budget allows (report the numbers).

======================================================================
ITEM 4

TASK (home lane, SCORES-OFFLINE): Keep "Your Scores" and the portal
working on networks that block Firebase.

ROOT CAUSE: leaderboards/index.html:159 and index.html:3764 call
firebase.database() directly, outside any guard. On a network that
blocks the Firebase SDK (common on college networks), `firebase` is
undefined, and the script stops. On /leaderboards/ that kills
"Your Scores", which is device-local and needs no Firebase at all. The
shared module (schools/assets/firebase-leaderboard.js) already handles
a missing SDK (its init() rejects cleanly when !db).

CLASS CHECK: A bug class: two pages call the SDK directly instead of
through the shared module that already has the safety. Fix it by
routing both through MaffsLeaderboard (add a read function for
recent_scores and boards if it lacks one), not by adding try/catch on
each page. The class check adds a CI rule: no page outside the shared
module calls firebase.* directly.

EXACT CHANGE:
1. leaderboards/index.html and the portal ticker read through
   MaffsLeaderboard. With the SDK missing, /leaderboards/ shows
   "Your Scores" from the device and a short line that live
   leaderboards can't load on this network. The portal hides the ticker
   quietly.
2. A check (ci-line header): no served page except
   firebase-leaderboard.js references firebase.database or
   firebase.initializeApp. A test loads /leaderboards/ and the portal
   with gstatic.com/firebasejs blocked and asserts no page error, and
   that Your Scores renders.
3. Handover updated.

DO NOT TOUCH: database.rules.json; board keys; how games submit scores.

SUCCESS CONDITION: with Firebase blocked, /leaderboards/ shows Your
Scores and the portal loads with no error; with it allowed, everything
behaves as before; merged on a green Gate; main green.

STOP IF: another page also calls the SDK directly (list it and include
it, as the same class); the shared module needs a change to its submit
path (report it; this contract is read-only paths).

======================================================================
CHECKPOINT after item 4: update home.md and stop.
