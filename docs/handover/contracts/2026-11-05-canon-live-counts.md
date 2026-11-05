# CANON-LIVE-COUNTS (Jon, 5 Nov 2026), verbatim

TASK: Remove hand-typed live counts of games and rooms from docs/canon.md, add The Christmas Tree Fiasco to §11.1, record that pr-assets/* branches are kept, and add a check that keeps §11.1's live rooms equal to the hub.

ROOT CAUSE: Canon types counts beside the data they summarise, and they have drifted: "Thirteen rooms live" (§11.1, line ~2411, and Project Overview, line ~3193) while 14 rooms are on the hub; §11.1's table has no Christmas row; the games count says "101 games live ... and a hundredth listed item" (line 22) while §11 and Coverage say "99 live games" (lines ~2260, ~2407). Canon's own rule (§7.5.3, line ~1487: "A site fact is never hand-typed beside its data") already bans this on the homepage but not in canon itself.

CLASS CHECK: Yes, a class: a hand-typed figure beside its source goes stale, here three times in one file. Updating the numbers would only reset the clock. The fix removes the counts, points to the source, and puts a check on the one list canon does own.

EXACT CHANGE:
1. docs/canon.md: replace each present-tense live count of games or rooms with a pointer to its source: rooms → "§11.1 is the only list; the hub escape-rooms/index.html shows the live ones"; games → .claude/rules/game-roster.md (and data/games.json "pages" for The 6 P's). Lines at least: 22, ~2260, ~2407, ~2411, ~3193. Dated historical statements ("found raw Unicode in 17 games, 22 Sep") stay: they are history, not a live count.
2. §11.1: add The Christmas Tree Fiasco row in the table's existing format (Level, Antagonist, State) from room.js and teacher.html; State "Live (05/11/2026)". Where the room names no antagonist, follow Big School Begins' pattern.
3. §7.5.3's rule: extend it to say canon, CLAUDE.md and AGENTS.md follow it too.
3a. Add to canon's git/branch policy (wherever close-out cleanup is described): pr-assets/* branches hold the screenshots a PR's description links to; they are kept permanently and never deleted at close-out (Jon, 5 Nov 2026). Remove the "due to go after review" note for pr-assets/christmas-room from docs/handover/cloud.md.
4. A check (new scripts/check-canon-rooms.py with a ci-line header, or a section in check-escape-rooms.py): the slugs in §11.1 marked Live equal the room links on escape-rooms/index.html; withdrawn rows are not on the hub. Self-test with a missing row and an extra row planted.

BEFORE MERGE: #668 (CHRISTMAS-ROOM close-out) is green and waits for the home lane to merge it. Once it lands, rebase on main; if docs/handover/cloud.md or CLAUDE.md conflict, keep every entry intact and STOP rather than drop one.

DO NOT TOUCH: the roster, data/games.json, the hub page, the homepage, any game, any figure in a dated history line, §11.1's existing rows.

SUCCESS CONDITION: grep finds no present-tense live game or room count in canon; §11.1 lists 14 Live rooms and 1 Withdrawn; the pr-assets rule is in canon; the new check passes on main and catches both planted faults. Committed, PR open, entry in docs/handover/cloud.md.

STOP IF: any script, test or page reads one of these counts from canon; the hub and §11.1 disagree about a room other than Christmas; a count you would remove is the only place a fact is recorded.

## Amendment 1 (Jon, 5 Nov 2026, answering the cloud lane's two questions)

Q1, branch (the session's branch `claude/kind-carson-hlusgj` carries open PR #669): "New branch (Recommended)": `claude/canon-live-counts` from origin/main, its own PR; #669 untouched.

Q2, lane and tier (none stated; canon is the home lane's): "Cloud, Shared (Recommended)": a lane exception for this contract only: the cloud lane edits canon §1, §7.5.3, §7.8 (branches), §9's Coverage heading, §11 and §12's Project Overview, and adds the check. Shared tier: stop at Gate green for Project Claude's review and Jon's "merge".

Decided by the lane, not asked (AGENTS.md forbids force push): "rebase on main" is done as a merge of main into the branch, with the same STOP on a cloud.md or CLAUDE.md conflict.
