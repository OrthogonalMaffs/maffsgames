Model: opus · Effort: high — correctness checks on live rooms; set /model before pasting

CONTEXT FOR A FRESH SESSION: git fetch; create a new worktree from origin/main. Do not pull into the primary worktree or any existing branch. Read CLAUDE.md (Task Contract), canon §11, scripts/gen-escape-variants.py, scripts/check-escape-rooms.py, and the 11 Oct handover entry on §11.3.

TASK: Move the escape rooms' per-set correctness checks into a shared module that CI runs on every set in every live room, then rewrite canon §11.3 accurately with no hand-typed figures.

ROOT CAUSE: The per-set checks (exactly one answer, answer and misconception both settable, answer absent from the clue) exist only in gen-escape-variants.py. That script is run by hand, is not in CI, and writes to a hardcoded path in the old E:\jon\maffsgames folder. CI checks that variants.json is consistent, not that each set is correct, so an edited or new set can pass CI unverified. This breaks the standing ruling that authored content is verified in CI.

CLASS CHECK: This is a class problem. The verification logic lives in a one-off generator rather than in shared infrastructure, and it affects all 11 live rooms and every future room. The fix: extract the checks into one module imported by both the generator and CI. Do not create a second copy of the logic.

EXACT CHANGE:
1. Extract the per-set checks from gen-escape-variants.py into a new shared module (e.g. scripts/escape_set_checks.py): pure functions, no file I/O. Move the logic; do not change it.
2. gen-escape-variants.py imports the module; replace the hardcoded path with repo-relative paths. Prove that regenerating produces byte-identical variants.json for all 11 rooms.
3. check-escape-rooms.py runs the shared checks on every set in every live room's variants.json. On failure, name the room, lock, set and failed check. Print per-room and total verified-set counts.
4. Add a negative test with a test fixture (never a live file): a deliberately broken set must fail CI.
5. CLAUDE.md, Task Contract: state that a session starts by creating a new worktree from origin/main and never pulls into the primary worktree or an existing branch.
6. Canon §11.3: say that sets are generated and checked by gen-escape-variants.py, that every set is re-checked in CI by check-escape-rooms.py through the shared module, and that counts are printed in the CI log. Remove every hand-typed figure from the bullet (199, 2,384, per-room valid counts, rugby's 156).
7. Read-only sweep of canon for other hand-typed counts derived from repo content, including §11.1. List each with its section and text in the handover; change none.
8. Handover in docs/handover/home.md; remove this task's worktree per CLAUDE.md.

DO NOT TOUCH: any room's HTML, room.js or variants.json content; the logic of any check (move, never alter); the keypad check; canon sections other than §11.3; .claude/rules/game-roster.md; any room's release state.

SUCCESS CONDITION: CI passes on all 11 live rooms and fails on the broken fixture; regeneration is byte-identical; per-room and total counts appear in the CI log; §11.3 is accurate and contains no figures; the CLAUDE.md worktree rule is in; the sweep list is in the handover; merged on green, main green.

STOP IF: any live set fails a check (a correctness finding: report room, lock, set and check, and do not fix the content); regeneration is not byte-identical; the checks depend on something that exists only under the old E: path; the generator's checks differ between rooms in a way one module can't hold.
