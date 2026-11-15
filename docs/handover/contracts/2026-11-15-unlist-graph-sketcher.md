UNLIST-GRAPH-SKETCHER (Project Claude, Sun 15 Nov 2026; re-checked against main 984851c at 20:08; Jon 10:29, 10:31, 10:32, 19:33)
Recommended: Sonnet, effort medium: an unlisting by the repo's own SR-21 list in reverse, two backlog rows and one /updates/ line; no game code.
LANE: home. TIER: Medium (merge on green; Project Claude reviews after merge). START: now. First commit: FOOTER-NO-SUPPORT's close-out per the standing rule (home.md's "MERGED: pending" becomes #789, 8791910, check-site 43753882335 + phone-fit-full 43753882351 green; contract to history). One PR. Branch from current origin/main.
MERGE: merge-pr.py on a green Gate.

JON'S RULINGS (verbatim in the PR body):
- 15 Nov 10:29: "yes, unlist it please, it's no good as it is." (canon SR-20: "Jon may unlist beyond this").
- 15 Nov 10:31: "it goes into whats changed, with us having found low completion numbers and realised it was not up to standard, removed pending rebuild. another trust building note"
- 15 Nov 10:32: "thats fine as written" (to the /updates/ line in EXACT CHANGE 4).
- 15 Nov 19:33: "yes please" (to adding a todo row for the extra pack art, EXACT CHANGE 5).

TASK: Take Graph Sketcher off every list on the site while its page stays live at its URL, say so openly on /updates/, record what its redesign must fix, and add the backlog row for the extra pack art.

ROOT CAUSE: Jon played it on 15 Nov after its completion figure (13 starts, 0 completions; every recent abandon in the Sheets backend on question 0). Found on main 984851c (games/graph-sketcher/index.html):
- Table cells are type="number" with onchange="checkCell(this)" (:698): one click of the box's arrows submits the value; a wrong value adds a penalty (G.qPenalties++, :753) and the box is wiped after 0.8 s (:754).
- No calculator, though its scenarios need powers (100 x 1.05^t), e and sin/cos (degrees and radians); the site calculator (schools/assets/calculator.js) has none of x^y, e, sin, cos.
- L4_15 (:608-614): yRange [0, 1.1e7] for values up to 1e6, so the curve fills the bottom tenth, and its "read" question asks a value off that curve.
- The table header is text-transform:uppercase (:79), so stress σ shows as Σ (summation).
- Values and axes in JavaScript e-notation (toExponential, :715, :873: "1.0e+7", "1.00e+6"), against canon's KaTeX standard form.
- "Give each value to 0 decimal places" for whole numbers; the y-axis title overlaps its numbers; the table scrolls sideways with its last column cut off at 1250-1266 px wide.
- scripts/verify-graph-sketcher.py (in CI) recomputes keys from each printed equation but checks no axis range, notation or label, which is why L4_15 and the σ/Σ fault passed.
Separately (EXACT CHANGE 5): PACK-WORDING-1511 (#785) closed rows CAR-TRAP-PACK-APPROVE and ROLL-PROM-PACKS-APPROVE, and its close note in docs/history/todo-done.md says the new art they listed is "no longer tracked by a todo row". Nothing in docs/todo.md now tracks it.

CLASS CHECK: Local, as an unlisting: one game, by the repo's existing procedure (SR-20 to unlist, SR-21 to relist, whose list of what relisting puts back is exactly what this removes). The faults themselves are not fixed here. The type="number" fault is a class across 12 games (contract ANSWER-BOX-TEXT); the calculator is shared (a later contract); the game's own faults go into its redesign row. The pack-art row is local: one backlog row restoring tracking that a close-out dropped; no code.

EXACT CHANGE:
1. Unlist by SR-21's list, in reverse: the roster row moves to the Unlisted section of .claude/rules/game-roster.md (section counts updated, the row's note "unlisted 15 Nov 2026 by Jon, redesign: todo GRAPH-SKETCHER-REDESIGN"); its portal cards (data/games.json and anything built from it, index.html) and weekly-fact links; sitemap.xml; spec-map/index.html; the leaderboard hub row (leaderboards/index.html, into NOT_ON_HUB); /resit/ and parent-guide links if any. Find every listing with a grep for graph-sketcher outside docs/ and games/graph-sketcher/ (on 984851c it also appears in scripts/*, schools/assets/launch-dates.json, schools/assets/firebase-leaderboard.js, data/check-ledger.json and updates/index.html: change those only where SR-21 names them or a check requires it); state each place changed in the PR body.
2. The page stays live at /games/graph-sketcher/, unchanged, with noindex added as the other unlisted games have it (games/regression-rumble/index.html:6 has <meta name="robots" content="noindex, nofollow">; follow that pattern).
3. docs/todo.md: a new row GRAPH-SKETCHER-REDESIGN (owner: Project Claude to spec; Jon approves) carrying every fault in ROOT CAUSE above with its file:line, plus: scripts/verify-graph-sketcher.py must be extended to check every scenario's axis range against its function's values, its notation and its labels; the calculator dependency; the answer-box class (ANSWER-BOX-TEXT). Relisting follows SR-21 after the redesign.
4. /updates/: today's entry gains this line, verbatim, in the page's own markup for an entry line (bold game name as the page's other lines have it):
   Graph Sketcher is off the game lists while we rebuild it. Our own numbers showed that almost nobody was finishing it, so we played it ourselves and found out why: answer boxes that wiped themselves, no calculator for questions that needed one, and graphs drawn at the wrong scale. It will be back once it's up to standard. Until then, its page still works for anyone who has it bookmarked.
   If no 15 Nov entry exists, add one in the page's existing date format. docs/handover/home.md entry.
5. docs/todo.md: a new row PACK-ART-EXTRAS (owner: Project Claude writes the art prompts, Jon makes and uploads the art, then a lane swaps it in; low priority, after the remaining Core rooms' generator work), placed in the same section as the other print-pack rows, carrying, with the figures from the closed rows CAR-TRAP-PACK-APPROVE and ROLL-PROM-PACKS-APPROVE in docs/history/todo-done.md:
   (a) Prom Budget: the card for The bronze bust shows a cash box (prom-08-cash-box; the art prompt barred statues): a bust, or a different object, is wanted.
   (b) Car Trap: the charger's sticker (342 px wide; the longest formula needs 448 px at 11 pt) prints LOAD LIMITER with the formula in the caption; new art with a sticker at least 520 px wide would let the formula print on the picture. The hatchback's sign (250 x 134 px) is blank; a sign of about 900 x 500 px would let its words print.
   (c) Prom Budget's Christmas card (187 px wide: "It is not December." does not fit at 11 pt) and Roll for Initiative's notice-board card (126 px: "NOTICES." does not fit) print nothing; art with a wider blank area would let them.
   (d) After any swap: rebuild the pack with --final, re-run lockcheck and the answer-box check, and Jon re-uploads the PDF to Tes.
   The row also points to the close note in docs/history/todo-done.md ("Closed 15 Nov 2026 (PACK-WORDING-1511)"), and that close note gains one sentence at its end: "Re-tracked 15 Nov 2026 as row PACK-ART-EXTRAS (UNLIST-GRAPH-SKETCHER)."
DO NOT TOUCH: games/graph-sketcher/index.html beyond the noindex line; scripts/verify-graph-sketcher.py (stays in CI unchanged: the live page is still served); its leaderboard scores and Firebase data; its analytics; every other game; canon (SR-20 already allows this); the wording of the /updates/ line; every pack config, art file and pack PDF (row PACK-ART-EXTRAS records the work, it does not do it).
SUCCESS CONDITION: FOOTER-NO-SUPPORT's close-out is in the first commit; Graph Sketcher appears in no portal list, filter, search, sitemap, spec map or leaderboard hub; its URL still loads and plays; the roster shows it under Unlisted with the reason; the /updates/ line is live, verbatim; the GRAPH-SKETCHER-REDESIGN row exists with every fault; the PACK-ART-EXTRAS row exists with (a)-(d) and the todo-done close note carries the re-tracked sentence; check-site and the roster checks pass; Gate green; merged; main's check-site and phone-fit-full green on the merge commit and reported; home.md updated.
STOP IF: any check would need loosening to accept the unlisting (report it); unlisting needs a change to shared code beyond data and listing files; a listing place is found that SR-21 does not name and removing it would change another game; the /updates/ line would need rewording to pass a check (report the check and its message; do not reword); a docs/todo.md or docs/history/todo-done.md rule (entry size, row format, archive rule) would refuse either new row or the added sentence as written (report the rule; do not shorten the fault list).


---

UNLIST-GRAPH-SKETCHER: follow-up from Project Claude, 15 Nov 2026 20:35 (Jon's rulings 20:33: "agreed" to points 1-3 and to the banner wording below). This replaces EXACT CHANGE 2 and widens DO NOT TOUCH for the game page as set out here; everything else in the contract stands.

Cause: the contract was wrong, not your work. An existing game unlisted for faults follows Glorious Gantt's precedent: page left indexed (.claude/rules/game-roster.md:162, "Their pages are unchanged (no noindex), so existing links, Google Classroom links and search results still work.") and carrying the correction notice (scripts/audit-register.py:206-214). Regression Rumble's noindex is the withdrawn-game holding page (roster :178), a different category. Canon SR-20 says when to unlist but not this, which is why the contract missed it.

Do, in the same worktree and PR (#791):
1. games/graph-sketcher/index.html: remove the noindex line you added. Revert the /updates/ October "Wrong answer keys" mention to the link it was on main (check-canonical-links should accept it once noindex is gone); say so in the PR body.
2. games/graph-sketcher/index.html: add the correction notice on the start screen in Glorious Gantt's pattern (games/glorious-gantt/index.html:143-144 for the marker and div; :40 for the .correction-notice rule, adapted to Graph Sketcher's own theme variables), with this text verbatim:
   We're rebuilding this game. Some answer boxes clear themselves, there's no calculator for the questions that need one, and some graphs are drawn at the wrong scale, so it's harder to play than it should be until this notice is removed.
   No other change to the page. Check it at 320 px and at 1280 px: the notice must not push the start button below the fold on a phone where it was above it on main; if it does, STOP and report the measurement.
3. docs/canon.md SR-20 (:82): append this sentence to the rule's text, before the "Exception: SR-32." sentence: "An existing game unlisted for faults keeps its page live and indexed (no noindex, so existing and Google Classroom links and search results still work) and carries the correction notice (<!-- maffs-correction-notice -->, scripts/audit-register.py), which goes when it is relisted." No other canon change.
4. Do not add graph-sketcher to UNLISTED_NOT_BY_AUDIT; do not change audit-register.py.
Then: re-run the Gate, merge on green as the contract says, report main's check-site and phone-fit-full on the merge commit, and update home.md (the stop entry closed with this follow-up).
STOP IF: the Findings register step or any other check still fails after 1-3 (report the message; do not loosen anything); the notice changes the page's phone fit as above.


---

UNLIST-GRAPH-SKETCHER: second follow-up from Project Claude, 15 Nov 2026 20:50. Jon's ruling: option 1. Move the correction notice (marker and div together) to just after the Start button on the start screen; no change to its text, style or the rest of 449905c6. Start's bottom edge must be unchanged from main at 320x568, 375x667, 390x844 and 1280x720 (526, 469, 469, 434); report the notice's top and bottom edges at each. Then push, Gate, merge as the contract says, report main's check-site and phone-fit-full on the merge commit, and close the stop in home.md.
STOP IF: the Findings register check requires the marker in a particular place on the page (report its rule); Start moves at any measured width.
