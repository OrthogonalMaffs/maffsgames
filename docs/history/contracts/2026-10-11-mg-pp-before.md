Model: sonnet · Effort: low

CONTEXT FOR A FRESH SESSION: git fetch. Read the mg-pp-before entry in docs/handover/home.md.

TASK: Report whether the uncommitted edits in mg-pp-before are already in main, so Jon can rule keep or discard.

ROOT CAUSE: mg-pp-before is detached at a commit already in main but has uncommitted edits to scripts/check-changed.py and scripts/test-escape-keypad.py. Nobody knows whether those edits are superseded.

CLASS CHECK: Local. One worktree, two files, a one-off leftover. The workflow gap that let it build up was closed in #277.

EXACT CHANGE:
1. Diff each file's uncommitted state against the same file in origin/main.
2. For each file, report in plain English: already in main (identical or superseded), partly in main (what's missing), or not in main (what it does and whether anything in main now relies on its absence).
3. Recommend keep (as a new task) or discard, with the reason. Add it to the handover.

DO NOT TOUCH: the worktree, its files or its state. This task is read-only, so no commit, no stash, no discard.

SUCCESS CONDITION: a per-file finding and a recommendation are in the handover.

STOP IF: the edits touch anything beyond those two files; the worktree has changed since the 11 Oct handover.
