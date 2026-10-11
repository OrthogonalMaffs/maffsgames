Model: sonnet · Effort: medium

CONTEXT FOR A FRESH SESSION: git fetch; create a new worktree from origin/main (CLAUDE.md "Start of task"). Read the 11 Oct handover entry for ESCAPE-SET-CHECKS, section "For you to decide", and canon §11.3–11.5.

TASK: Bring canon §11.3–11.5 and the escape-room check's CI label up to date with the 11 live rooms and the shared checks from PR #278.

ROOT CAUSE: §11.3–11.5 and the CI label were written for eight rooms and the old checks. The two releases and #278 made them stale: ratings missing the two new rooms, "all use digits" now false, §11.4's script entries outdated, and §11.5's "All eight rooms". The label text is held in ci-pack.json and ci-timings.json.

CLASS CHECK: Two parts. Canon: an instance of the hand-typed-facts class. Any statement derived from repo content becomes a pointer, as §11.3 now does, and descriptive statements are corrected. CI label: if the same text lives in two files, that is a duplicated source. Make one file the source if the CI tooling supports it; if not, update both identically and report why.

EXACT CHANGE:
1. Correct every stale §11.3–11.5 item listed in the handover's "For you to decide". No figures derived from repo content; describe, and point to the CI log or the source file.
2. Locate the escape-room check's label text; make it single-source if possible (see CLASS CHECK), and make it describe the shared per-set checks.
3. Handover in docs/handover/home.md; remove the worktree per CLAUDE.md.

DO NOT TOUCH: scripts/escape_set_checks.py and all check logic; any room file; canon outside §11.3–11.5; the count-sweep items outside §11 (awaiting Jon's ruling); .claude/rules/game-roster.md.

SUCCESS CONDITION: every listed §11 item is corrected; §11.3–11.5 contain no derived figures; the CI label is accurate (and single-source, or the reason it isn't is recorded); CI green; merged on green, main green.

STOP IF: either new room has no rating recorded in the repo (ratings are Jon's judgement: ask, don't assign one); making the label single-source needs a change to the CI workflow beyond those two JSON files; any correction needs a figure or judgement only Jon can supply.
