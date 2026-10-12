# VERIFIERS-20 drafts, games 17-20 (cloud lane, 12 Oct 2026 checkpoint)

Not live: these files are parked here, outside scripts/, so CI does not pick them up. Each one passed its run and its
self-test in this container against main at 5b1307a. To use one: copy it to scripts/ in that game's own claim branch,
re-run it with its self-test, then follow the recipe in docs/handover/cloud.md.

- verify-formula-forge.py (game 17): carries its own TeX reader (Jon, 12 Oct). Three items have two wrong options equal
  in value to each other. They are listed in EQUAL_PAIRS as formula-forge-v20-001. ADD that finding (open, MEDIUM) to
  docs/audits/findings/formula-forge.yml in that PR, and suggest these replacements for Jon:
  - `v = u^2 + 2as` (forgot the square root)
  - `a = \sqrt{c^2 + b^2}` (added instead of subtracted)
  - `u = \sqrt{v^2 + 2as}` (sign slip)
- verify-characteristic-quest.py (game 18): apply cq-t6-003.patch to the game page in that PR (SR-6 fix of t6-003: the step
  "\lambda^2 - (0) - (0 - 4)" becomes "\lambda^2 - (0)\lambda + (0 - 4)"), close t6-003 (fixed, pr), and add a plant that
  re-introduces the old step. The PR touches a game page, so it runs the full check-changed.py (SR-27).
- verify-eigenvalue-extractor.py (game 19): one plant's label says "a repeated root keyed once only"; it actually plants
  "3, -3". Rename it to "a repeated root keyed as 3 and -3".
- verify-prisoners-dilemma.py (game 20): it drains the game's own MaffsLock.timer callbacks in the page, which takes a run
  from 68 s to 7 s. Do not touch t4-001 (the leaderboard ranking), which waits on Jon.
