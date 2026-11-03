CONTRACT: CALC-DOCK-WIDE
Tier: Shared · Lane: home · Implementer: Codex (WSL)

START
After UPDATES-NOVEMBER merges. git -C ~/maffsgames pull --ff-only, then a worktree codex/calc-dock-wide from
origin/main. Concurrency (Jon, 3 Nov 2026): allowed with the cloud lane's SEQ-SOLVER-FIXES, SEQ-SOLVER-WORKED and
DASHBOARD-METRICS, which do not touch schools/assets/calculator.*; if any open PR touches calculator.js or
calculator.css, STOP.

TASK
Make the docked calculator always sit beside its question card on wide screens, whatever the page's structure, with
no sideways scroll.

ROOT CAUSE
Reproduced by Project Claude, 3 Nov 2026 (Sequence Solver, GCSE, calculator opened): at 1920x1080 the column is centred
(580-1340) and the card ends at 1324, but the docked panel's left edge is at 1932, past the viewport, with 352 px of
sideways scroll (1983x642 the same: panel at 1995). calculator.js dock() sets the rail to position:absolute with
left: calc(100% + gap), relying on the rail's containing block being the dock card (calculator.css: ".maffs-calc-host
makes the card the rail's containing block"). That holds only when the page mounts the calculator inside the card.
Sequence Solver mounts it in #calc, a sibling below .q-card, so the containing block is a wider ancestor and the
panel lands off screen. Nothing checks the assumption. Jon hit it on his own screen, 3 Nov 2026.

CLASS CHECK
Yes: shared infrastructure (the dock, every docked page) relying on an unchecked page structure. Fix it once in
calculator.js: compute the rail's left from the dock card's on-screen right edge relative to the rail's actual
containing block (or reparent the rail into the card), so the result is the same wherever the page mounts the
calculator. Editing Sequence Solver's markup, or special-casing it, is the wrong fix.

EXACT CHANGE
1. schools/assets/calculator.js dock(): position the docked rail from the dock host's bounding box (its right edge plus
   D.gap), independent of where the calculator element sits in the page; keep the existing room test (when it docks
   at all), width rule, sticky panel and every non-docked behaviour unchanged. Recompute on resize as now.
2. scripts/test-calculator-js.py dock cases: add a page whose calculator is mounted outside its dock card (as Sequence
   Solver does) at 1280x720, 1920x1080 and 2560x1440; assert the panel's left edge is the card's right edge plus the
   gap (within 1 px), its right edge inside the viewport, and no sideways scroll; plant: the old calc(100% + gap)
   rule, CAUGHT. Existing dock cases unchanged and passing.
3. Measure every page that mounts MaffsCalc with a dock, in play with the calculator open, at 1920x1080 and
   2560x1440, before and after: card right, panel left, gap, sideways scroll. Table in the PR. Sequence Solver
   screenshot at 1920x1080 before and after.

DO NOT TOUCH
The dock's breakpoint and room rule; the calculator's keys, maths, toggle (full and icon forms) and phone behaviour;
any game file; Gate files.

SUCCESS CONDITION
On every docked page at 1920 and 2560 the panel sits beside its card, inside the viewport, no sideways scroll; tests
and plant pass; table and screenshots in the PR; check-changed.py green; Shared review by Project Claude; stop at
Gate green for Jon's "merge"; Record line.

STOP IF
The fix changes when the calculator docks, or its layout at any width where it does not dock; any page's verifier
fails after the change for a reason other than the dock position (report it); an open PR touches calculator.js or
calculator.css.
