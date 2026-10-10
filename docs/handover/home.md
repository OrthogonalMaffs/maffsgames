# Handover: home lane

**PREPUSH-SCOPE: STOPPED on its STOP IF (10 Oct; branch `claude/prepush-scope`, not merged, no PR).**
Cause **(b)**: `check-changed.py` already selects through `ci-deps.select` (CI's own function); a shared-asset
change rightly selects every game, and the checks ran one at a time. There is no installed pre-push hook: the
"pre-push check" is `check-changed.py`, run by hand. **Before** (old runner, serial, on b40a475's tree):
docs-only 22 checks 353 s; one-game (`games/angle-ace`) 29 checks 1565 s; shared asset (#232's files) 119
checks 4198 s (70 min). **After** (branch: 6 workers, longest first from ci-timings.json, `--files`, a
printed "checks deferred to CI: ..." line; the shared-asset tests now always run, as CI runs them):
docs-only 26 checks **133 s wall** (355 s of check time), all passed; one-game 33 checks 308 s wall (1592 s
of check time) **but all six "Answer lock in play" parts FAILED** (games UNPLAYABLE after Start, one driver
error): they play games concurrently inside themselves, and six at once overloads the machine. That is the
STOP IF ("parallel runs make any check flaky"). The shared-asset after-run was then stopped by Claude Code
for low system memory (not restarted, per its rule). **Needs Jon:** e.g. run the answer-lock parts (and other
browser-heavy lines) one at a time beside the light ones, or fewer workers; then re-measure. Local-only
failures seen in the serial before-runs, unrelated: Negative Number Line 320x568 fold (fails on main too),
core-maths-paper1 UNPLAYABLE under load, Test the Claim ReferenceError under the local node.

**ESCAPE-DIFFICULTY (10 Oct, Jon's contract 13:05, after CAR-TRAP-RELEASE; contract
`docs/handover/contracts/2026-10-10-escape-difficulty.md`).** Every live lock has `grade: N`; a room's
rating is its hardest lock's band (★ Warm-up 1–3, ★★ Core 4–5, ★★★ Challenge 6–9), drawn by the new
`escape-rooms/assets/rating.js` on the start screen and the teacher page (the teacher page adds "Suits a top
set" at ★★★ only), and written as a `data-stars` chip on every hub and front-page card (the old level chips
replaced). The derived ratings reproduce Jon's list exactly (no STOP): ★ Comic Caper, Kiln Disaster; ★★
Canteen, Heatwave, P.E., Prom, Hamster, Car Trap; ★★★ Rugby Mud. Every lock's grade and reason is in the PR.
Two locks the bank tags "GCSE Higher" are graded 5 (Car Trap's monic quadratic by factorising, Prom's
compound growth by building powers): the method is Foundation's. `levelLabel` removed from the live rooms
(display only); `level` kept (analytics send it). The hub's cards are now in rating order (it says "Ordered
easiest to hardest"); the front page's order is unchanged. **check-escape-rooms.py was never in CI** (it ran
only by hand): it now has a ci-line and fails a missing grade or any disagreeing card, with two plants caught
on every run. New `scripts/test-escape-rating.py` (start screen and teacher page match the hub card in
Chromium; no 320 px overflow apart from the teacher pages' allowlisted tables, §1.37). **For the cloud lane:**
The Rightful King must derive ★★★ and The Library Jam ★: add `grade` to every lock, a `data-stars` chip on
both cards, and load `../assets/rating.js` before engine.js and teacher.js.

**CAR-TRAP-RELEASE (10 Oct, Jon's contract 13:00; `docs/handover/contracts/2026-10-10-car-trap-release.md`).**
Jon's wording in room.js: wrong lines 1 and 2 are now Mr Strictman's memos (gates at oh-seven-hundred; staffroom
biscuits discontinued), lines 3-4 unchanged; the "two point six centimetres" line moved into the brief ("You hear him
before you see him: ..."), in words, real quote marks. Released: `escape-rooms/car-trap/index.html` is the room
(play.html's body; prom-budget's head: analytics on, indexable, canonical, the draft's 158-character description
for description and og:, og:image the v2 scene), play.html deleted; card on the hub (premise line + Bounds · Arc
length · Quadratics, chip GCSE / Core, placed last) and on the front-page band; `<url>` in sitemap.xml; "eight" →
"nine" on the hub (description, og:description, lede) and the front page (band lede, "Open all nine rooms"),
CLAUDE.md, canon §11.1 (Car Trap Live 10/10, Mr Strictman, **★★**; "Nine rooms live, one withdrawn"). **The
front page's meta descriptions carry no count** (they say "15-minute escape rooms"), so the contract's "two hits"
had nothing to change. teacher.html stays noindex; it is linked from inside the room, as every room's is. /updates/:
one line under October's New. **For Jon:** the hub says "Ordered easiest to hardest"; Car Trap sits last until
ESCAPE-DIFFICULTY orders the cards by stars. Checked: check-escape-rooms passes; test-escape-art plays all nine
rooms to a win and a loss; on the real URL a wrong barrier setting shows the memo line.

**KEYPAD-VARIABLE (10 Oct, Jon's contract 10:20, ahead of PREPUSH-SCOPE: the cloud lane's Rightful King and
Library Jam builds wait on it; contract `docs/handover/contracts/2026-10-10-keypad-variable.md`).** A keypad may
now take `maxDigits: N` instead of `digits: N`: **"up to N digits, Set to submit"**. The display shows only what
has been typed (no empty slots), the room's existing Set button submits 1 to N digits (nothing typed: nothing
happens, no time lost), a leading zero is never kept (0,5,4 reads 54), and the typed fallback shares the rule
(`upTo()` in engine.js). A keypad with `digits` is key for key as before. teacher.js describes the instrument as
"keypad, up to N digits" (answers were never padded there). check-escape-rooms.py fails a maxDigits lock whose
answer or misconception is not a whole number of 1 to N digits; gen-escape-variants.py has `keypad(n)` (the range
both modes can set, so `keep()` applies the rule). check-teacher-invite's room driver handles both modes. New
`scripts/test-escape-keypad.py` (fixture: kiln-disaster's keypad rewritten in the page to maxDigits 4, answer 54,
misconception 5400; no room file edited): 5,4,Set opens; 5,4,0,0,Set raises the named misconception; Set on
nothing does nothing; no empty slot ever shows; the fixed two-digit keypad is unchanged; the old fixed-length rule
planted is caught. All 8 live rooms to a win and a loss (test-escape-art) pass; check-escape-rooms passes. STOP IFs
clear: keypad entry is not saved state (no SAVE_V change), no live room's keypad changed, one rule for keys and
typed fallback. Canon §11.3 and §11.4. **For the cloud lane: The Rightful King's passcode and the Library Jam's
fines lock can use `maxDigits` in phase 2** (the misconception must fit: 9900 needs `maxDigits: 4`).

**CAR-TRAP-BUILD, taken over (10 Oct, Jon 09:30, one lane: `docs/handover/contracts/2026-10-10-car-trap-one-lane.md`).**
The home lane owns Car Trap end to end; the cloud lane has stopped and will not touch #242 or any car-trap file. On
#242: `art: 'car-trap-v2'` (pictures merged in #246); sceneAlt corrected (the measuring wheel is at the pillar by the
yellow bollard), failAlt rewritten (the scene's own view, not from the ramp), winAlt rewritten for the high CCTV-style
view (the barrier arm is down, not up); car-trap's teacher page allowlisted at 320 px (570, table.tt) like the other
eight, todo §1.37 still the real fix for all nine. Played in Chromium: v2 scene, win and fail pictures load, no 404.
The room stays behind its holding page (`index.html` unchanged). **Jon can play-test it at
https://maffsgames.co.uk/escape-rooms/car-trap/play.html** (unlinked, noindex, analytics off). Release is a separate
step on Jon's word: play.html's content becomes index.html and play.html is deleted in that PR.

**CAR-TRAP-V2-ART (10 Oct, Jon; image work only, #242 and car-trap/room.js are the cloud lane's).** Filed for
#242's `art: 'car-trap-v2'`: **`docs/art/car-trap-v2-scene.webp`, `docs/art/car-trap-v2-fail.webp`,
`docs/art/car-trap-v2-win.webp`** (1600x873, through `strip-gen-watermark.py --width 1600 --frame 1600x873`; no
watermark found, corners checked by eye). The old `car-trap-scene/-fail/-win.webp` are left as they are (main's
room still names `car-trap`). Badges blanked: the pale blue hatchback's front (scene, fail) and rear (win), the grey
car's bonnet oval (fail) and grille oval (win). Every plate checked blank: hatchback front (white) and rear (yellow),
grey car, beige car. **For the cloud lane (#242):** rebase on main and the v2 pictures resolve, so `art` can stay. The
win is a high CCTV-style view of the bays (camera top right), so #242's `winAlt` ("The same row of bays...") needs
rewriting to match: Jon asked for it, and it is the cloud lane's file.

**ART-PENDING (10 Oct, Jon's contract 08:50, ahead of the queue for cloud PR #242; contract
`docs/handover/contracts/2026-10-10-art-pending.md`).** Rule: **no `art` field, no request.** engine.js
(`HAS_ART = !!R.art`) emits no scene, fail-thumbnail or end-card picture for a room with no top-level `art:`;
a room with art is unchanged, data-fallback included. teacher.js mentions the mid-game failure picture only when
the room has art. check-escape-rooms.py lists a room with no `art` as "art pending" (it crashed on one before);
a named picture that is missing is listed as before, and check-site's tier 1 fails its 404. New
`scripts/test-escape-art.py` (15 s): all 8 live rooms to a win and a loss, their pictures load as before; the
fixture (canteen-hack with `art` removed, by routing) makes no /docs/art/ request through the brief, its
misconception, the win and the loss; the old always-request engine is planted and caught. STOP IFs clear: every
live room has all three files, so none uses the 404 path for its data-fallback; no saved field changes (SAVE_V 1).
Recorded in CLAUDE.md and voice-rewrite §6. **For the cloud lane (#242):** drop `art` from car-trap's room.js
(and leave the hub card's `<img>` out of `escape-rooms/index.html` until the art lands), then re-run.

**DASHBOARD-CHARTS (10 Oct, Jon's contract 08:35; `docs/handover/contracts/2026-10-10-dashboard-charts.md`).**
`docs/apps-script-endpoint.js` only, SCRIPT_VERSION `2026-10-10-a`: the three percentage columns are written as
fractions with the cell format `0%` (they show as before), the Accuracy chart's axis runs 0 to 1 as percent;
`rowBelowChart()` moves the row counter below each chart (a 21 px default row), so no chart overlaps the next
section; one filter, `isMarked()`, keeps rows with a blank `correct` out of Accuracy by Game and Hardest Questions.
STOP IFs clear: prisoners-dilemma sends `correct: null` (written blank by `cellValue`), and every other
`question_answered` call in games/ sends a boolean. The daily email is untouched (its own hardest-questions list still
counts prisoners-dilemma: the contract left the email alone). **Jon must redeploy; the repo copy does not deploy
itself** (runbook `docs/apps-script-redeploy.md`): paste the file into the Apps Script editor and set `REPORT_EMAIL`
to your address before saving; Deploy, Manage deployments, edit (pencil) the existing deployment, Version: New
version, Deploy; select `testDashboard` in the function menu and Run (it rebuilds the dashboard from the sheet;
`rebuildDashboard` itself needs arguments), or wait for the 07:00 run; open the `/exec` URL and check `version` reads
`2026-10-10-a`.

**MAIN GREEN (for the cloud lane: #223 may merge):** main's full run on 5cea89b (#224) passed every job, run
37969653160, and its timings job recorded and repacked (760ef9a). Main had been red since #220 (CI-BALANCE) on its
main-only "CI timings and pack" job alone: the job-log API refused the workflow's token; #224 reads the timings from
artifacts instead. Every content group is now at most 69% of its budget. Main green again after #218 (18f5da8, run 37970610295).

**DOCS-9OCT (10 Oct, branch `claude/docs-9oct-b`, after the checkpoint).** #239 SCI-CALC and #240 (checkpoint
handover) merged on 9 Oct late, main green after each (9f51dc7, 302d4d2). DOCS-9OCT applied: Factor Theorem relisted
under SR-21, **A-Level only** (roster #88, portal, sitemap, hub, spec map, canon count 96, todo 1.62); canon §0.2 the
freeze's one exception (Simultaneous Solver Stage 5, #203); §7.6 four rulings (Skip shows the answer and waits on
Next; one log row per answer; display-only number formatting; "≈" for rounded factors); §7.8.2 closed-not-idle cloud
sessions and the E2 one-off; timer-policy: Unit Converter to No Timer. **Escape on the initials overlay (Jon, 9 Oct
19:42): left as is, Skip stays the way out; Escape-to-close is deferred to a future accessibility pass, because an
accidental Escape would discard a leaderboard entry** (the OVERLAY-KEYS contract's "Escape closes the overlay as now"
was Project Claude's error; recorded on #232 too). **Next: KEYPAD-VARIABLE (entry at the top), then PREPUSH-SCOPE** (contract
`docs/handover/contracts/2026-10-09-prepush-scope.md`). LIBRARY-DRAFT moved to the cloud lane (Jon, 10 Oct 09:30);
Car Trap moved the other way: the home lane owns it end to end (#242, entry above). **Scientific tagging, Jon's ruling (10 Oct):** tag force-resolver,
moments-master, complex-converter, formula-forge, formula-unlocked, core-maths-paper2c (one PR each, after
PREPUSH-SCOPE); not estimation-golf or equation-builder; log-laws and higher-power reported back (SCI-CALC's
entry is archived in `docs/history/handover-home-archive.md`). Finished home-lane contracts (home-queue, its addendum, hook-fix, overlay-keys) moved to `docs/history/contracts/` in
this PR; the cloud lane's (listed-high, car-trap) and the IT room brief stay.

The home lane's running handover (canon §7.8.2). Only home-lane sessions edit this file; the cloud lane's is
`docs/handover/cloud.md`. Newest first. Keep it current on the branch as you go (CLAUDE.md, checkpoint discipline).

**STANDING RULE (Jon, 7 Oct 2026):** when a contract finishes and the next queued contract's start condition is
met, start it without asking. Stop only for a STOP IF, a decision no standing ruling covers, or an empty queue.

**Home lane owns:** shared code, shared assets, CI and canon (contract F's shared fixes, then contract C), and every
docs PR: `docs/todo.md`, the roster's listed section, relisting fixed games (batched).

**OVERNIGHT RUN (Project Claude for Jon, 8 Oct 2026, 23:45): DONE.** Contract verbatim in
`docs/history/contracts/2026-10-08-overnight.md`. Every item merged (see the summary above and the entries below).
main's run on #200 (2782d17) went red on a runner network flake (the DejaVu font fetch: curl 503s and 60 s
timeouts pushed B4 and L4 past their budgets; tier 1 timed out loading spot-the-muppet, untouched); one rerun of the
failed jobs passed (run 37875059753, attempt 2).

**Contracts (canon §7.8.2, contract CONTRACTS-FOLDER):** each is saved verbatim as
`docs/handover/contracts/<yyyy-mm-dd>-<name>.md`; the queue below holds a one-line pointer; the file moves to
`docs/history/contracts/` when the work merges. Read a contract when its item starts, never at session start.

**QUEUE (home lane, Jon 9 Oct 16:10):** 1 RULINGS-9OCT (#215, merged), 2 GRAPH-SKETCHER-FIT, 3 CI-BALANCE, 4 PLAY-AGAIN-SCREEN,
5 SCORES-OFFLINE, 6 SCI-CALC, 7 DOCS-9OCT, then CHECKPOINT. (E2 merged as #213; main green.)
CAR-TRAP-DRAFT: the cloud lane's (Jon, 20:17); contract at
`docs/handover/contracts/2026-10-09-car-trap-draft.md` on main (HOOK-FIX let it through the hook). Jon also sent the
IT room rewrite brief (Narry, secret ballot; 3 open rulings): a brief, not yet a contract, saved as
contracts/2026-10-09-it-room-brief.md. SCI-CALC (item 6) is saved as docs/history/contracts/2026-10-09-sci-calc.md.
- **Answer-lock L1 flake:** act only if it recurs (the follow-up below stands).
- **Standing F1 item: done for every listed game but graph-sketcher** (NOT_YET: glorious-gantt, unlisted and the cloud
  lane's; graph-sketcher, blocked by its phone overflow, batch 10 entry). unit-converter loads the lock (cloud lane,
  #196) and is judged in full, but is not in MIGRATED: Jon's call (the overnight contract left it to the cloud lane). **Before building each batch** (contract CLAIM, canon §7.8.2): read `cloud-remaining:` in
  `docs/handover/cloud.md` on main and drop every game on it from the batch. Never claim or edit a game on that
  line. For a listed game the claim is a process lock only: check-answer-lock.py still judges it as unclaimed.
- **Follow-up (home lane, CI): Answer lock L1 failed on main once (b66ccde, run 37776985917)** with five games at
  once (binomial-blaster, curling-friction, differentiation-duel by touch at 390px; force-resolver, moments-master
  UNPLAYABLE after Start). The same slice passed 20/20 locally on that commit, the parallel run (3878582) was green, and
  a rerun of the failed job passed. Canon 7.6.0 says a verdict never depends on timing: if it recurs, find what the
  driver waits on that a slow runner breaks (start(), the touch path), and fix it there, not with retries.

**Jon's rulings, 9 Oct (on the overnight questions; RULINGS-9OCT):** unit-converter moves to MIGRATED (done,
seeds 1-3 pass). wrong-on-the-internet keeps its 3 s pause before Try again: feedback on a wrong answer is shown, not
skipped (Jon, 8 Oct). complex-converter's Play Again keeps replaying the mode, as its Menu is one tap from the end
screen. graph-sketcher: fix its phone overflow now, then put it on the lock (item 2). The first two are in canon §7.6.

**Jon's rulings, 7 Oct:** eigenvector-engine-f0-005 is not a judgement call (SR-17: a scalar multiple of an
eigenvector is never a wrong option, whatever the prompt says about "simplest"): `jc: false` (in #108). The
verifier-lines-in-the-workflow question is answered by contract V: neither lane edits the workflow for a verifier.
