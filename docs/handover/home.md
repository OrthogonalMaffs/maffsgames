# Handover: home lane

**Queue (cross-lane facts; never archived)**

- PHONE-SCROLL (Small; Project Claude, 10 Nov 05:55, Amendments 1-3): merged as a594c8f (#721) under Jon's one-off ruling of 10 Nov 07:05; main run 42772678182 GREEN (89/89 jobs; phone-fit-full 42772678203 green). Entry below.

- DOCS-BUNDLE (Docs; Project Claude, 9 Nov 19:10, Amendments 1-2): merged as 10d3167.

- WHOSE-SIDE: the cloud lane owns the game until stage 5; timer-policy.md's line is `docs/todo.md` row WHOSE-SIDE-TIMER-LINE. DONE lines moved to docs/history/handover-home-archive.md, 8 Nov.

- One lane at a time: AGENTS.md, Lane ownership (rule e, BACKLOG-ONE).

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts: `docs/todo.md` row HOW-MANY-PARTS-FRACTION (§3)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

## 2026-11-28 (home): TODO-AUDIT (every item in docs/todo.md checked against main: finished and duplicated items moved out with evidence, stale ones listed for Jon)

Claude Code (home lane), worktree `~/mg-todo-audit`, branch `claude/todo-audit`. PR #944. The contract is at `docs/handover/contracts/2026-11-28-todo-audit.md` (verbatim).

- **Close-out of TODO-SEARCH-DEMAND (#942), each confirmed from GitHub Actions:** merged 28 Nov as a0c6f53 (squash) by main's merge-pr.py, which ended "main a0c6f53 run 46095376807: GREEN". PR head 59cd56a2: check-site 46093722219 and phone-fit-full 46093722236, both success. Main on a0c6f53: check-site 46095376807, phone-fit-full 46095376824 and the pages build 46095376554, each success. Its contract moved to `docs/history/contracts/2026-11-27-todo-search-demand.md`.
- **The audit:** 259 items (every table row, every §4 item, every bullet and paragraph of the prose sections), each with one verdict and its evidence in `docs/audits/todo-audit-2026-11-28.md`. Checked on main abb9b605.
- **Totals:** `docs/todo.md` 106,470 bytes before, 101,535 after (4,935 moved; 5,985 under TODO_LIMIT). DONE 5 items (3,283 bytes); PART DONE 4 (302); DUPLICATE 2 (439); OWED 213 (911 bytes of history clauses cut from 10 rows that stay); STALE? 35 (nothing moved).
- **Moved whole (DONE):** §1's index of closed rows; §3.9's "Seen while reading" (the nine games' wrong-answer timers); §4 item 2 (§7.6 Group B and the floor); §4 item 46 (ESCAPE-COUNT-SOURCE); the parked GA4 inline-gtag line. **DUPLICATE:** §5's bank growth for four games (two done, two in their LEDGER rows); §6's spec-map spot-check (row 3.1's own cell). **PART DONE:** §3.9's rulings (1) and (3); §4 item 12's DONE clause; row 3.21 and §4 item 17 are half done but nothing could be cut without rewording.
- **`docs/history/todo-done.md`:** "## Closed by TODO-AUDIT (28 Nov 2026)" holds each piece word for word with its evidence line, and each cut row as it stood. `scripts/check-todo-trim.py --base origin/main` passes: no ID or sentence lost.
- **For Jon, 35 STALE? items** (the report's own section, one line each with keep or close): the parked 27 Oct queue items, §3.9's order and Aa paragraphs, rows the code has moved past (3.20, WHEN-WILL-I-USE-THIS, FOLD-COMPONENTS), local-check items since check-changed stopped being run, and reviews whose counts no longer hold. His rulings come back as a follow-up contract.
- **Found, not recorded (STOP IF 1, nothing added):** row CGD-PHONE-LONG waits for PHONE-FIT-ALL-ITEMS, which has no row.
- **For Project Claude:** wording inside rows that stay has drifted (counts, line numbers; GRAPH-SKETCHER-REDESIGN says the shared calculator has no sin or cos, and it has had them since 9 Oct). Not changed: it would reword owed text. Listed under "Seen while auditing".
- **Why so little moved:** most of the file is genuinely owed. The 43 LEDGER rows match `data/check-ledger.json` entry for entry, and the earlier trims had already taken the finished rows.
- **/updates/:** none (internal work).
- **Run IDs and the merge:** in the next home contract's first commit, as usual (AGENTS.md, close-outs).

Record: agent Claude Code; wall 0:30; review cycles 0; amendments 0; usage n/a.

## 2026-11-28 (home): TODO-SEARCH-DEMAND (the 27 Nov search-log findings, 3-gon Line-up and the Level 3 full-release plan in the backlog; two Events-sheet tasks closed; canon's ticker line; todo.md trimmed)

Claude Code (home lane), worktree `~/mg-todo-search-demand`, branch `claude/todo-search-demand`. PR #942. The contract is at `docs/history/contracts/2026-11-27-todo-search-demand.md` (verbatim). The first commit closed out D-BY-DX-POLISH.

- **`docs/todo.md`:** rows 3-GON-LINE-UP, SEARCH-DEMAND and L3-FULL-RELEASE after PLOT-MIGRATE, copied from the contract by script; the ideas edits (Venn Diagrams AGAIN?, Not in Pen, Plans and elevations, Whack-a-mole); in §6 the Functional Skills Maths decision in place of "None open", and the two Events-sheet manual tasks gone. Every "before" line was on main as quoted.
- **`docs/history/todo-done.md`:** "## Part closed by TODO-SEARCH-DEMAND (27 Nov 2026)" holds the two manual tasks, each with its answer line, the "None open" line, and every trimmed part word for word.
- **`docs/canon.md` line 3335:** the ticker reads the latest 50 and shows the newest 20 from games with a portal card. Nothing else in canon changed.
- **The trim:** 107,496 bytes before; 109,932 with the new text; 106,470 now, 1,050 under TODO_LIMIT. Finished rows and parts verified on main 4ae47558 came to 2,281 bytes (15 moves; the PR lists each with its evidence), 1,155 short of the headroom. The rest is 1,181 bytes of notes of where a row came from ("Moved from cloud.md's Queue ...", "... live pointers", "... §6 (TODO-TIDY)"), taken out of 30 rows: history, not owed work. **For Project Claude to rule if that reading is wrong:** by finished work alone the file would have been 131 bytes over its limit and the contract's STOP IF (1) would apply.
- **Left in place, finished state unclear** (listed in the PR): §5's bank growth for four games (two now pass B4); §6's Spot the Error and New Shapes reviews; WHEN-WILL-I-USE-THIS's owner cell; CHECK-CHANGED-ONE-RUN (superseded, not finished); §4 item 14; LARGE-SCREEN-LAYER's and LOCAL-CHECKS's finished descriptions; §1's index paragraph.
- **Also seen:** the contract's SUCCESS CONDITION says four moved lines; steps 2 and 3 name three, and three moved.
- **/updates/:** none (internal work).
- **Run IDs and the merge:** in the next home contract's first commit, as usual (AGENTS.md, close-outs).

Record: agent Claude Code; wall 0:15; review cycles 0; amendments 0; usage n/a.

## 2026-11-27 (home): D-BY-DX-POLISH (d by dx? Why?: two columns from 1280 px with a larger graph and the table under it; a table that cannot scroll; room round the working's stacked fractions; a regenerated bank with bracketed arguments, numbered labels and Stage 5 in descending powers)

Claude Code (home lane), worktree `~/mg-d-by-dx-polish`, branch `claude/d-by-dx-polish`. PR #941. The contract is at `docs/history/contracts/2026-11-27-d-by-dx-polish.md` (verbatim). The first commit closed out D-BY-DX-GRAPH.

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
- **Gate on the PR head 90d2ed18** (main's #940 merged in before it): check-site 46078782995 and phone-fit-full 46078783001, both green.
- **Merged** 27 Nov as b94be44 (#941, squash) by main's merge-pr.py from the primary checkout, which ended "main b94be44 run 46080481809: GREEN". Main on b94be44: check-site 46080481809, phone-fit-full 46080481898 and the pages build 46080481488, each success.

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

