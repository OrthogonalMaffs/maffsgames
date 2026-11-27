# Handover: home lane

**Queue (cross-lane facts; never archived)**

- PHONE-SCROLL (Small; Project Claude, 10 Nov 05:55, Amendments 1-3): merged as a594c8f (#721) under Jon's one-off ruling of 10 Nov 07:05; main run 42772678182 GREEN (89/89 jobs; phone-fit-full 42772678203 green). Entry below.

- DOCS-BUNDLE (Docs; Project Claude, 9 Nov 19:10, Amendments 1-2): merged as 10d3167.

- WHOSE-SIDE: the cloud lane owns the game until stage 5; timer-policy.md's line is `docs/todo.md` row WHOSE-SIDE-TIMER-LINE. DONE lines moved to docs/history/handover-home-archive.md, 8 Nov.

- One lane at a time: AGENTS.md, Lane ownership (rule e, BACKLOG-ONE).

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts: `docs/todo.md` row HOW-MANY-PARTS-FRACTION (§3)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

## 2026-11-27 (home): D-BY-DX-POLISH (d by dx? Why?: two columns from 1280 px with a larger graph and the table under it; a table that cannot scroll; room round the working's stacked fractions; a regenerated bank with bracketed arguments, numbered labels and Stage 5 in descending powers)

Claude Code (home lane), worktree `~/mg-d-by-dx-polish`, branch `claude/d-by-dx-polish`. PR #941. The contract is at `docs/handover/contracts/2026-11-27-d-by-dx-polish.md` (verbatim). The first commit closed out D-BY-DX-GRAPH.

- **The bank:** `tools/d-by-dx-why/bank.py` is the contract's, verbatim; it prints total 60 and sha256 f9ddc279...8ec927, and its two checks pass. Embedded one item a line. The page's table rows are bracketed too: sin(ax), a cos(ax), cos(ax), -a sin(ax), ln(ax); e^(ax) is written as the power it is.
- **The table's scroll, measured before changing (main 9e05404):** the body's own `overflow-x:auto` (the page's rule; `fold.css` sets none) computes overflow-y to auto, and under the large-screen zoom the body's content came out 1 px taller than its box at 115 of 990 window sizes tried in headless Chromium (1024 to 2560 px wide, five heights, normal and Aa): all in normal mode, at zooms 1.15 to 1.55, the narrowest 1504 px wide. Never at zoom 1, and not at 2560 x 1440 itself (zoom 1.6), so Jon's own two windows were not reproduced here; the cause was. The rule is gone, so no bar can be drawn at any size, and the table is as wide as its column; it fits every width without a smaller font (the narrowest: 264 px of column, Aa).
- **The graph's box at 1280 x 720 before: 324 x 230 px.** The plotter's own shape is 24 wide to 17 high (its viewBox, 480 x 340), not 4:3; the plotter is not touched, so the graph fills its column in that shape.
- **Layout from 1280 px:** the question's card on the left; on the right the graph, filling its column, with the table under it. The page stays 1240 px wide. The right column's width follows the window's height (in vh, no height breakpoint, so the large-screen zoom is not capped): between 460 and 620 px. With the table it is as wide as lets the graph and the whole table end above the fold; in Pro it is 620 px. Measured (the graph's box in the page's own px, and its area over 324 x 230): 1280 x 720, 1366 x 768 and 1920 x 1080 with the table 424 x 300 (1.71 times); 2560 x 1440 with the table 472 x 334 (2.12 times); a half-width 1280 x 1440 window 584 x 414 (3.24 times); Pro at every one of them 584 x 414 (3.24 times). The question's card is 572 px wide or more (516 px before).
- **For Jon and Project Claude, the cost of the table under the graph:** on a window 720 px tall after the zoom (a 1280 x 720 laptop, and any 1920 x 1080 screen) the table cannot end above the fold under a graph 1.6 times larger: it ends at 772 px (815 px in Aa) and the fold is at 680 px, so the e and ln rows need a scroll. Before this, all six rows were on screen there. It fits from about 870 px of height: at 2560 x 1440 it ends 44 px above the fold in Aa. The contract's layout, as written; a ruling is wanted on whether a short window should keep three columns.
- **Also decided here:** the right column is the larger of the two only where the window is tall enough (a half-width 1280 x 1440 window in Pro, 584 against 572 px); elsewhere the question's card is wider, because a wider graph pushes the table off a 2560 x 1440 screen. `body.in-run` (new, set while a question's screen shows) widens the page for Pro runs too.
- **The working:** from 1024 px a line holding a stacked fraction has .18 em of room above and below (`.w-line:has(.mfrac)`); a line of plain maths is as it was. Closest lines, KaTeX box to KaTeX box: 0.30 em before, 0.53 em now (the plain lines' own spacing); narrower than 1024 px the labels sit between the lines and it was 0.99 em already, so nothing changed there. Next stays above the fold everywhere: the least room is 38 px (1280 x 720, Aa; 31 px before), 41 px (375 x 667, Aa), 43 px (320 x 568).
- **The verifier:** the new digest; its formatter writes the brackets and its reader refuses a function without them; labels rebuilt with the item's number, and a label naming the table's letter is its own finding; every Stage 5 sum in descending powers. Fit units at 1920 x 1080 and 2560 x 1440 (26 fit units in all), and at every size: the table's body cannot scroll, no option wider than its button, the working's 0.5 em. From 1280 px: two columns, the table under the graph, the box at least 1.6 times 324 x 230. Five new plants, each caught (18 in all): the contract's four, and the fraction's room taken away.
- **Large screens:** the page's measured need is 617 px (607 before); `data/large-screen.json` and the page's tag updated; `check-large-screen.py` passes.
- **Found, not changed (shared):** `schools/assets/site-nav.js` sizes the corner title from rectangles in the screen's px and applies it in the page's px, so under the zoom the title can be given more room than there is. On main it ends 4 px short of this page's HUD at 2560 x 1440; a page 40 px wider would sit under it.
- **/updates/:** none (the game is unlisted). **`docs/todo.md`:** untouched.
- **Run IDs and the merge:** in the next home contract's first commit, as usual (AGENTS.md, close-outs).

Record: agent Claude Code; wall 0:35; review cycles 0; amendments 0; usage n/a.

## 2026-11-27 (home): D-BY-DX-GRAPH (d by dx? Why? draws f with the question and the gradient function over it once answered, through a new shared plotter; a regenerated bank; Next after a right answer; the large-screen layer)

Claude Code (home lane), worktree `~/mg-d-by-dx-graph`, branch `claude/d-by-dx-graph`. PR #938. The contract is at `docs/history/contracts/2026-11-27-d-by-dx-graph.md` (verbatim). The first commit closed out NEXT-NO-FALLBACK.

- **Jon (27 Nov 2026, 18:11):** "draw the graph as part of the question, when you get the answer draw the gradient line on the same graph in a different colour, really hammer home that we are finding the gradient function".
- **The plotter, `schools/assets/plot.js` (MaffsPlot), new:** SVG and KaTeX, no canvas, no pointer, no timer. The caller gives the window; axes through 0 or along the edge nearer 0; ticks at nice steps or multiples of pi/2; a value that is not finite breaks the line; a curve can draw in (0.6 s) and two can be drawn together by pens; it draws only while it is on screen and the tab is showing; reduced motion draws at once. Each path carries its window and box, so a check maps its points back to values. `scripts/test-plot.py` is its check (a `ci-line` of its own): 63 checks, 11 plants.
- **The bank:** `tools/d-by-dx-why/bank.py` is the contract's, verbatim; it prints total 60 and sha256 c6c0c8dc...bb7c960, and its two checks pass. Embedded one item a line, with START_SHOW's three pairs beside it.
- **The page:** the graph is a reference card: beside the question from 1024 px (question, graph, table side by side from 1280 px; the table under the graph from 1024 px), a closed "Graph" button on anything narrower, which reads "See the gradient function" once answered and closes on Next. f is the accent, the gradient function amber and the wider line. A right answer shows "Right:", draws the gradient function and waits on Next (floor 0.6 s). A wrong answer shows the line, the working (label, left side, "=" and the right side, the "=" in one column; labels above their lines below 1024 px), the table rows and Next; no "The answer is" line. `root_upside_down` is the contract's new line.
- **`schools/assets/next-control.js`:** an optional `floorMs`, a shorter floor for one control and never a longer one; no existing caller passes it, so none changes. Its case and two plants are in `scripts/test-next-control.py`.
- **The start screen:** the pens draw START_SHOW's pairs (4 s, then 3 s still, round again); the equations are written as they finish.
- **Large screens:** the page is on `check-large-screen.py`'s MIGRATED with ten starts (five stages, with the table and in Pro); its measured need is 607 px. From 1024 px the options are 1.5rem with more padding.
- **The verifier:** its own renderer and its own TeX reader; every working line equal in sympy to the function or its derivative; every curve read back from the page within 1 px (worst 0.03 px); the pens, the waits on a fast clock, the fit of the asking, right and wrong screens, the start screen at four sizes; 13 plants.
- **Decided here, for Jon and Project Claude:** (1) the stage buttons already ran past the fold on a phone, so the start picture sits under them there and beside them from 1024 px: it pushes no start control down. Above them it would be seen first, and would push Stage 3 below the fold at 375 x 667. (2) The two unused options now go during a wrong answer's feedback on every screen, not only phones: with four board lines, Next was 60 px below the fold at 1280 x 720 in Aa. (3) Below 1024 px the options stay 1.3rem (maths 1.57 times the body): larger put Next 2 px below the fold at 375 x 667 in Aa. (4) On a phone the gradient function draws in when the student opens the fold-out, since the plotter waits until it is on screen.
- **Least room under Next, measured here:** 31 px (1280 x 720, Aa, with the table), 41 px (375 x 667, Aa), 43 px (320 x 568).
- **`docs/todo.md`:** new row PLOT-MIGRATE; D-BY-DX says the graph is built and adds Jon's ruling on the start picture.
- **/updates/:** none (the game is unlisted).
- **Gate on the PR head a0752575** (main's #936 merged in before it): check-site 46068038708 and phone-fit-full 46068038653, both green.
- **Merged** 27 Nov as 9e05404 (#938, squash) by merge-pr.py from the primary checkout, which ended "main 9e05404 run 46070280000: GREEN". Main on 9e05404: check-site 46070280000, phone-fit-full 46070279934 and the pages build 46070280046, each success.

Record: agent Claude Code; wall 0:55; review cycles 0; amendments 0; usage n/a.

## 2026-11-27 (home): NEXT-NO-FALLBACK (the shared Next control no longer advances by itself; canon §7.6 says so, and that a revealing right answer waits too)

Claude Code (home lane), worktree `~/mg-next-no-fallback`, branch `claude/next-no-fallback`. PR #937. The contract is at `docs/history/contracts/2026-11-27-next-no-fallback.md` (verbatim). The first commit closed out MERGE-GUARD.

- **Jon (27 Nov 2026, 18:27):** "I'd remove the auto advance … the student needs to press continue, it gives them a chance to check where they went wrong, and write down the correct method before moving on".
- **The helper (`schools/assets/next-control.js`):** no timer unless `fallbackMs` is passed; the 20 s default and the exported `FALLBACK_MS` are gone (nothing read the constant but canon). `fallbackMs` stays for test harnesses. The floor, the in-view scroll, advance-once, clear(), the 44 px target and the MaffsLock clearing are untouched.
- **The seven pages:** the-6-ps, take-a-walk, squared-squirrel, just-pythag-it-bruv, how-many-parts, 52dle and distinctly-average no longer pass `fallbackMs` (the NO_FALLBACK constants and the day-long literal are gone). Nothing else in them changed.
- **The guard, in `scripts/test-next-control.py` (the "Shared asset tests" job, which runs on every PR):** a static scan fails on any `.html` or `.js` under games/, escape-rooms/, the-6-ps/ or any page in the site root that names `fallbackMs` (plant: a page passing `fallbackMs: 20000`, caught); with no `fallbackMs` the control does not advance in 90 s on a fast clock (the page's setTimeout at 1/100) and Enter still advances once (plant: the 20 s default restored, caught). The existing fallback cases already passed `fallbackMs` themselves.
- **One verifier changed, because it held a page's workaround:** `verify-just-pythag-it-bruv.py` required the worked example's Next to be given the day-long delay; it now requires that the page passes none.
- **One check relied on the 20 s default, and now advances for itself:** `check-teacher-invite.py` plays factor-theorem to its results screen, and its step never pressed the shared Next (its harness cut every timer to 25 ms, so the fallback moved it on). The first Gate (check-site 46053172613) failed there. The step now presses Next; what the check tests, the teacher line on the results screen, is unchanged. The same Gate also failed Text writes (the new test's two planted files were written without newline=''; fixed) and one job on a Docker pull.
- **Canon §7.6:** a wrong answer waits with no timer (Jon's reason); the new line on a right answer that reveals something new, in the contract's words; the three other mentions of the fallback in the section now say "a test's `fallbackMs`".
- **Stale words fixed:** `check-answer-lock.py`'s docstring and `docs/sandbox-checks.md` spoke of the 20 s fallback. `scripts/check-site.py:2680` still does, in a comment; that file is the cloud lane's.
- **A wrong answer advanced by a page's own timer (the contract's STOP IF list; none changed here):** trig-wars (a miss shows its tip for 2.8 s and passes the turn; exempt by Jon's ruling of 19 Nov) and higher-power (a wrong guess ends the run). correlation-or-coincidence falls back to 4 s only if next-control.js did not load. CI's pause check (WRONG-PAUSE-NEXT) holds every other judged game for 3 s; a scan of the pages for timers of 3 s or more found no other. Six games that check cannot judge are on its own list (WRONG_PAUSE_UNCHECKED).
- **/updates/:** one line, 27 Nov.
- **Gate on the PR head 1640c8e0:** check-site 46055742396 and phone-fit-full 46055742477, both green.
- **Merged** 27 Nov at 19:38 UTC as e91a25a (#937, squash) via merge-pr.py, which ended "main e91a25a run 46058091551: GREEN". Main on e91a25a: check-site 46058091551, phone-fit-full 46058091615 and the pages build 46058090668, each success.

Record: agent Claude Code; wall 0:45; review cycles 0; amendments 0; usage n/a.

## 2026-11-27 (home): MERGE-GUARD (merge-pr.py refuses a PR whose Gate or phone-fit run started before main's newest merge)

Claude Code (home lane), worktree `~/mg-merge-guard`, branch `claude/merge-guard`, PR #935. The contract is at `docs/history/contracts/2026-11-27-merge-guard.md` (verbatim). Shared tier: it stops at Gate green for Project Claude's review and Jon's "merge". The first commit closed out BASE-60-TIDY.

- **Jon (27 Nov 2026, 17:57):** "merge script please".
- **(a''), new, in `scripts/merge-pr.py`:** M is main's newest merge as (b') picks it (bot skip-marker commits passed over). If M is the PR's head or an ancestor of it (compare M...head reads "ahead" or "identical"), it passes. Otherwise the Gate's run and the phone-fit run must each have been created after M's committer date, or the merge is refused, naming M and the run. The Gate's time is its workflow run's created_at, found by check suite; the Gate check's own started_at (the end of the run) is never read.
- **Red, never waited on:** judged every poll with (a) and (a'), also while a run is still going; --wait does not wait on it and --override does not waive it.
- **The record behind the fixtures:** #930's runs were created at 17:16:26Z on 26 Nov, #927 landed on main at 17:35:08Z, the Gate check started at 17:37:25Z and #930 merged at 17:52:57Z. Ids, shas and those times in the selftest are GitHub's.
- **Selftest:** 17 new cases and 4 plants (the check removed; the Gate's started_at for its run's created_at; bot skip-marker commits counted as M; the ancestor test inverted), each caught. The 108 lines the selftest printed before are printed unchanged.
- **Decided here, for review:** (1) a run created in the same second as M is refused (not after it); (2) under --override, which waives (b'), an unreadable M is refused by (a'') itself, so the override cannot pass an unjudged PR; (3) a Gate check that cannot be tied to a run, or an unreadable compare or commit, is refused, never guessed; (4) the selftest's fake API moves a phone-fit script on once per poll, not once per read, since two checks now read those runs in a poll.
- **Not touched:** (a), (a'), (b), (b'), (c), the watch, --head, the retries, the merge PUT; every workflow; `serve-stubbed.py`, `bank_common.py`.
- **AGENTS.md:** the stale-Gate rule gains "merge-pr.py enforces this (MERGE-GUARD, 27 Nov 2026)".
- **Gate on the PR head f038472f:** check-site 46046955243 and phone-fit-full 46046955221, both green.
- **Merged** on Jon's "merge", 27 Nov at 18:30 UTC, as b6c0119 (#935, squash) via merge-pr.py, which ended "main b6c0119 run 46049988829: GREEN". Main on b6c0119: check-site 46049988829, phone-fit-full 46049988775 and the pages build 46049988366, each success.
- **Departure, as the lane reported it:** the contract said main's current script judges this merge. merge-pr.py was run from the PR's worktree, so the new version judged its own merge; the new check passed (main's newest merge, #934, was in the branch) and every existing condition was applied unchanged.

Record: agent Claude Code; wall 0:50; review cycles 0; amendments 0; usage n/a.

## 2026-11-26 (home): BASE-60-TIDY (Base 60's cuckoo rides out on a perch joined to its clock; the page's stale comment; spec-map row N13 names time)

Claude Code (home lane), worktree `~/mg-base-60-tidy`, branch `claude/base-60-tidy`, PR #932. The contract is at `docs/history/contracts/2026-11-26-base-60-tidy.md` (verbatim). The first commit closed out BASE-60-LIST.

- **Jon (26 Nov 2026, 19:51):** "the cuckoo clock looks much better alhough the cuckoo is not attached to the clock when it pays a visit".
- **The perch:** a thin level arm (`.ck-perch`, cream with a dark edge, as the bird is drawn) from inside the doorway (x 36 of the drawing) to under the bird's body (x 7). It grows out of the doorway and back with the bird, on the same times and easing, and is hidden at no length when the bird is in. The bird's own movement, timings and shape are unchanged; it bows and droops on the arm, which stays level.
- **Decided here:** the arm extends from the doorway; it does not slide as a fixed-length piece. A fixed-length arm sliding with the bird would stick out of the far side of the house while the bird is in, and past the drawing's edge. Measured every 20 ms of a right answer and through a wrong answer's transition at 1366x768, 320x568 and 1920x955: the bird is on the arm whenever it shows.
- **The drawing's box does not grow** (the arm lies inside the bird's reach), so the clock's size, the fold figures and `data/large-screen.json` are untouched.
- **Verifier:** the bird units also hold the perch showing and within 1 drawing unit of the door's box and the bird's at each sampled moment of the hold, after a wrong answer and in both reduced-motion states. Two plants: the perch removed, and the perch left behind at the door. Run locally: both bird units pass, both plants and the two older bird plants caught.
- **Page comment and spec map:** the UNLISTED comment is now "Listed 26 Nov 2026 (contract BASE-60-LIST, PR 930)." ("PR 930", not "#930": the first Gate, check-site 45887805820, failed only on the Theme check, which read "#930" in the page as a hex colour outside :root); row N13 reads "Standard units and conversions: length, area, volume, mass, time", its games unchanged.
- **Screenshot** (the bird out on its perch at 1366x768): in the report to Jon; no image is committed.
- **Gate on the PR head d5417e8f:** check-site 45892119116 and phone-fit-full 45892119126, both green. Main was merged in twice while the PR waited (9f51bb8d, then eaf158af), and the Gate re-ran each time, as the contract's step 6 asked.
- **Merged** on 26 Nov as 60fb649 (#932, squash) via merge-pr.py, which ended "main 60fb649 run 45894195608: GREEN" (the line as the lane reported it to Jon on 26 Nov; this file did not hold it). Main on 60fb649, read from GitHub Actions on 27 Nov: check-site 45894195608, phone-fit-full 45894195615 and the pages build 45894194832, all success.

Record: agent Claude Code; wall 0:40; review cycles 0; amendments 0; usage n/a.

