OVERNIGHT QUEUE, HOME LANE (Project Claude, 8 Oct 2026, 23:45). Jon is asleep until
morning. Save this file verbatim as docs/handover/contracts/2026-10-08-overnight.md in
the first commit you make. Not in home.md: home.md gets a one-line pointer.

RULES FOR TONIGHT (Jon, 8 Oct 2026; these override the "checkpoint every 2 batches"
rule for this run only):
- Work through the items in order. When one finishes (merged, main green), start the
  next without asking.
- Merge your own PRs only on a green Gate, and only while main's last full run is green.
  Watch main's run after every merge, to the end, before starting the next item.
- If main goes red after your merge: fix it if the cause is your PR. If the cause is not
  yours (a flake, or the cloud lane's merge), re-run the failed job once. If it fails
  again, STOP the whole run: write the handover and leave it for Jon.
- A STOP IF in any item ends the whole run. Commit the work to its branch, open a draft
  PR, and write the handover. Stopping is a correct result, not a failure.
- Never decide anything a standing ruling doesn't cover. Record the question in the
  handover and stop.
- Update docs/handover/home.md after every merged item, so a stop at any point leaves
  the state clear.
- If your context runs low, finish the current item, write the handover, and stop at
  that boundary. Never start an item you can't finish.
- Nothing Google-side, nothing in Firebase, nothing needing Jon's approval.
- The cloud lane may run at the same time: read cloud-remaining: in
  docs/handover/cloud.md before every batch, and never touch a claimed game.

======================================================================
ITEM 1: VOCAB-IDEMPOTENT. The full contract is in Part B of
claude/lane-pastes-2026-10-08-2130.md. Jon has not sent that file, so here it is, word
for word:

TASK (home lane, VOCAB-IDEMPOTENT): Make wrapExamVocab in the shared
exam-vocab.js idempotent, so the vocabulary tooltips never wrap their
own output (factor-theorem-t5-008).

ROOT CAUSE: schools/assets/exam-vocab.js:109 wrapExamVocab(html) wraps
exam terms in tooltip spans, and :144 applies it to an element's
existing HTML. Run again on already-wrapped HTML, it matches terms
inside its own output: the tooltip text and the attributes. That
injects <span> into aria-labels and shows garbage on Factor Theorem
Q10, Q13 and others (audit tranche 5, t5-008). Only factor-theorem
loads the file today.

CLASS CHECK: Shared infrastructure: the fault is in a shared asset, and
every page that loads it inherits it. Fix it once, in exam-vocab.js.
Do not guard the calls in the game. The cloud lane's FT-FIX was amended
(8 Oct, 21:30) to leave t5-008 to the home lane.

EXACT CHANGE:
1. exam-vocab.js: wrapExamVocab skips text already inside a tooltip
   span, and never matches inside a tag or an attribute (work on text
   nodes, not on an HTML string, if that is the cleanest way). Applying
   it twice gives the same result as applying it once. Nothing visible
   changes on a first application.
2. A test, in scripts/ with a ci-line header (or added to an existing
   shared-asset test): on every factor-theorem prompt,
   wrap(wrap(x)) == wrap(x), and no tooltip markup appears inside any
   attribute. Plant the old function in the self-test; it must fail.
3. Close factor-theorem-t5-008 in docs/audits/findings/factor-theorem.yml
   in this PR, unless factor-theorem is on cloud-remaining: or has an
   open PR. In that case leave the findings file to that PR and say so
   in the handover.
4. Handover updated.

DO NOT TOUCH: the tooltip wording (VOCAB-SHOWTHAT is done); any game
page; the cloud lane's open Factor Theorem work.

SUCCESS CONDITION: the test passes and fails on main's exam-vocab.js;
in Chromium, Factor Theorem Q10 and Q13 show clean text and their
aria-labels hold no markup; merged on a green Gate; main green;
handover current.

STOP IF: making it idempotent changes what a first application shows
on any factor-theorem prompt (quote the before and after); another
page loads exam-vocab.js by the time you start (list it, then
proceed).

======================================================================
ITEM 2

TASK (home lane, CONTRACTS-FOLDER): Make docs/handover/contracts/ the
place both lanes keep contracts verbatim, and make sure no session
loads it at start.

ROOT CAUSE: On 8 Oct a /clear wiped the cloud lane's only copy of three
contracts. The repo held summaries only, so Jon had to re-send them.
The cloud lane now saves each contract verbatim under
docs/handover/contracts/ and moves it to docs/history/contracts/ when
the work merges (Project Claude's correction, 20:00). The home lane
keeps live contracts inside home.md, which loads at every session
start. CLAUDE.md's heading says "read docs/handover/", and a session
could take that as the whole folder (the cloud lane flagged this in
#187).

CLASS CHECK: Process, shared by both lanes: one convention, written
once in canon §7.8.2 and CLAUDE.md, applied to both handovers.

EXACT CHANGE:
1. CLAUDE.md: name the two handover files explicitly (home.md,
   cloud.md), and add "docs/handover/contracts/ is read only when
   starting the item it names, never at session start."
2. Canon §7.8.2: record the convention. On receipt, each contract is
   saved verbatim as docs/handover/contracts/<yyyy-mm-dd>-<name>.md;
   the handover queue holds a one-line pointer; the file moves to
   docs/history/contracts/ when the work merges.
3. home.md: move any verbatim contract text for live items into
   contracts/ files with pointers (this overnight file is the first).
   Archived ones stay where they are.
4. check-context-size.py: confirm it does not count contracts/. If
   anything at start-up would load that folder, fix it here.

DO NOT TOUCH: cloud.md's content (the cloud lane's); docs/history/
beyond adding the contracts/ folder.

SUCCESS CONDITION: CLAUDE.md and canon state the convention; home.md
holds pointers, not contract text; the size check passes; merged on a
green Gate; handover current.

STOP IF: the start-up load would grow (report the before and after
figures).

======================================================================
ITEM 3

TASK (home lane, RELIST-SR): Relist Screening Room under canon SR-21,
and take it off NOT_YET.

ROOT CAUSE: screening-room was unlisted on 6 Oct (SR-20, tranche 4).
The cloud lane's fixes have merged: MaffsLock adopted, t4-005 (HIGH)
and the MEDIUMs closed, t4-017 fixed. Its open findings are t4-014
(MEDIUM, a bank job) and possibly LOW. If no CRITICAL or HIGH is open,
it meets SR-21. It passed the answer-lock check in F1 batch 8, but it
is still on NOT_YET, which only the home lane edits.

CLASS CHECK: Not a bug: the existing SR-21 relist process and the
NOT_YET shrink rule. No shared code changes.

EXACT CHANGE:
1. Confirm on main: verify-screening-room.py in CI with a ci-line
   header; no open CRITICAL or HIGH in
   docs/audits/findings/screening-room.yml; check-answer-lock.py
   passes for it.
2. Remove screening-room from NOT_YET in check-answer-lock.py.
3. Relist it on every surface SR-21 and its todo relist row (§1.72)
   name: the roster row back to its listed section at #62, the portal,
   the sitemap, the spec map, and the leaderboard hub (remove it from
   NOT_ON_HUB). Add it to /essentials/ only if it was there before
   unlisting.
4. /updates/: no entry and no badge. Its changes are correctness, lock
   and layout fixes, which canon §3.4 excludes, apart from phase 3 now
   showing the scenario and the icon array. Judge that one under §3.4:
   it changes what a student sees while answering, so if you judge it
   qualifies, add "Screening Room: the scenario and picture now stay on
   screen while you answer." with the Updated badge, and say why in
   the PR.
5. Close the todo relist row; handover updated.

DO NOT TOUCH: the game's page and bank; the findings file; the other
unlisted games (factor-theorem, glorious-gantt).

SUCCESS CONDITION: screening-room on the portal and the sitemap, off
NOT_YET; roster, coverage, theme, meta, label and lock checks pass;
merged on a green Gate; main green; handover current.

STOP IF: any condition in step 1 fails (report which); a relist surface
the checklist names no longer exists.

======================================================================
ITEM 4 onwards: F1 BATCHES 9, 10 AND 11 (as many as finish cleanly)

The remaining listed games on NOT_YET (22 at the checkpoint), Year 6/KS3/GCSE/Core
first, 8 per batch, exactly as F1 has run (queue item 5's rules in home.md; contract F1
in docs/history). Before building each batch, read cloud-remaining: on main and drop
every claimed game. unit-converter and factor-theorem are the cloud lane's next two:
drop them even if they are not yet on the line. Draft PR first, as before. One batch at
a time: merged, main green, handover written, then the next. Stop when NOT_YET has only
cloud-claimed games left, or at the run's end conditions above.

======================================================================
WHEN THE RUN ENDS (for any reason): the top of docs/handover/home.md says, in five
lines or fewer, what merged (with PR numbers), what is open, why the run stopped, and
any question for Jon. That is the first thing Jon reads in the morning.
