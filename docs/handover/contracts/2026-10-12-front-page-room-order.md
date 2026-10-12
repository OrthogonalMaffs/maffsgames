CONTRACT FOR THE HOME LANE: FRONT-PAGE-ROOM-ORDER (Project Claude for Jon, 12 Oct 2026, 17:35). Recommended: Sonnet, low effort (one shared check widened, one block of cards reordered).
Save this verbatim as docs/handover/contracts/2026-10-12-front-page-room-order.md in the PR's first commit. Queue: after CONTAINER-PULL-TIMEOUT and RULINGS-12OCT.
======================================================================
TASK (home lane, FRONT-PAGE-ROOM-ORDER): Order the escape-room cards on the front page by difficulty, ★ rooms first, matching the hub, and make CI enforce that order on every page that lists rooms.

ROOT CAUSE: The front page's escape-room grid (index.html, `div.esc-grid`, about lines 806-904 on main 12 Oct) lists the rooms in the order they were built: ★★ ×5, ★★★ Rugby Mud, ★ Comic Caper, ★ Kiln Disaster, ★★ Car Trap, ★★★ Rightful King, ★ Library Jam. The hub (escape-rooms/index.html) is in rating order, and scripts/check-escape-rooms.py enforces that. `check_ratings()` already reads both pages (`pages = {"hub": ..., "front page": ...}`) and checks every card's chip on both. But its order rule sits under `if page == "hub":`, so the front page was never held to it.

CLASS CHECK: Yes. The same rule ("rooms are listed easiest first") applies to two components, and the shared check enforces it on only one. The fix goes in the check: the order rule applies to every page in `pages`. The front page must also match the hub's order exactly, so the tie order within a star band has one source (the hub). Reordering the front page alone would leave the next new room free to land out of order again.

EXACT CHANGE (one PR, branch claude/front-page-room-order, a new worktree from origin/main):
1. scripts/check-escape-rooms.py, `check_ratings()`: apply the rating-order rule to every page, not just the hub. The message names the page. Then add one comparison: the front page's sequence of live-room slugs must equal the hub's sequence. On failure, print both sequences.
2. The check's planted faults: add one front page with two cards swapped across a star band, and one front page that is rating-ordered but has a different tie order from the hub. Each must fail the run. The real files must pass.
3. index.html, the `esc-grid` block: reorder the cards to the hub's order, which on main is comic-caper, kiln-disaster, library-jam, hamster-heist, pe-shed-rebellion, heatwave-mutiny, prom-budget, canteen-hack, car-trap, rugby-mud, rightful-king. Move each card whole. Comic Caper and Kiln Disaster are each wrapped in a `<div style="display:flex;...">` with their `esc-note` ("Built from a site user's request..."): move each wrapper with its card and note, unchanged. Change no card's markup, text, image or data attribute; only the order.
4. Check at 320 px and desktop width with the stub server (serve-stubbed.py) that the grid still lays out with no overflow. The two wrapped cards now sit side by side at the start of the grid, so check that the third card (Library Jam) lines up with them.
5. docs/handover/home.md: a dated entry. Merge on a green Gate with main green. Watch main's run. Remove the worktree and branch per CLAUDE.md as it then stands.

DO NOT TOUCH: escape-rooms/index.html (already in order); any room's files, chips, ratings or grades; the "Open all eleven rooms" button; the rest of index.html; canon (no ruling changes); docs/handover/cloud.md.

SUCCESS CONDITION: The front page shows the three ★ rooms first, then the six ★★, then the two ★★★, in the hub's order. check-escape-rooms.py passes on main and fails on both planted faults. The grid fits at 320 px. Main's full run is green after the merge.

STOP IF: the hub's own order on main differs from the list in step 3 (follow the hub, and say so); moving the wrapped cards breaks the grid layout in a way that needs a CSS change (report it with a screenshot description; do not restyle); any other page lists room cards that the check does not read.
