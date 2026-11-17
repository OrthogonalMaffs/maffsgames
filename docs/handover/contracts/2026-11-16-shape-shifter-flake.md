TOOL: Claude Code (cloud lane). SIZE: small (one verifier's one check, plus a one-word room text fix). Recommended: Sonnet, medium effort.
MERGE TIMING: send first; this unblocks main. HEATWAVE-PACK (home lane) waits for this merge before it merges.

TASK: Make scripts/verify-shape-shifter.py's rotation "moving on" check deterministic so main goes green again, and capitalise the P.E. Store's time-called read-out.

ROOT CAUSE:
1. Main's check-site run 43961875130 on 6e1f4e0 failed only in the Shape Shifter verifier: "moving on: rotation: the wrong answer reads 'Correct! (B)'". The check records where the rotation options are, then reloads the question; games/shape-shifter/index.html reshuffles questions and options with Math.random (shuffle(), line 576), so after the reload the "wrong" tap can land on the right answer. The same code passed on #803's own Gate: it is a random fault, not a game bug.
2. escape-rooms/pe-shed-rebellion/room.js: the time-called read-out text begins lowercase ("the whistle goes…"); the pack prints it after "If time runs out:" (PE-SHED-FINAL, #803, reported it).

CLASS CHECK: 1 is local to this verifier's own check (the game's shuffle is correct behaviour). Do grep the other scripts/verify-*.py for the same shape (positions or option order read, then a reload or new question, then a tap using the old positions) and list any you find in the PR and as a todo row; do not fix them here. 2 is local to one room's string.

EXACT CHANGE:
First commit: ANSWER-AUDIT-PILOT's close-out (AGENTS.md rule): #802 merged as bbbab73 via merge-pr.py, last line "main bbbab73 run 43950743520: GREEN", exit 0; check-site 43950743520 success, phone-fit-full 43950743561 success. Move its contract to docs/history/contracts/. Save this contract verbatim at docs/handover/contracts/2026-11-16-shape-shifter-flake.md.
1. scripts/verify-shape-shifter.py: in the rotation moving-on check, choose the wrong option from the option positions and values read AFTER the reload (or seed/stub Math.random for that check only, if the verifier already has a pattern for it), so the tap is always on a wrong option. Add a planted fault to the self-test that the old behaviour would let through (e.g. tapping a stale position), and confirm it is caught. Run the check enough times locally (e.g. 50 loops of that check) to show it never picks the right answer.
2. escape-rooms/pe-shed-rebellion/room.js: capitalise the first letter of the time-called read-out ("The whistle goes…"); nothing else in the string.
3. docs/todo.md: a row for any other verifier with the same stale-position shape (if found). Cloud handover.

Run only the checks this contract names and the Gate: verify-shape-shifter.py with self-test (and the 50-loop run), check-escape-rooms.py. No optional all-game local runs.

DO NOT TOUCH: games/shape-shifter/index.html (its shuffle is correct); any other verifier (list, don't fix); the pack generator and pack configs; Gate files; the home handover.

SUCCESS CONDITION:
- verify-shape-shifter.py passes 50 consecutive runs of the rotation moving-on check and its self-test catches the new plant.
- The P.E. Store read-out starts with a capital.
- PR merged on green via `python -X utf8 scripts/merge-pr.py <n>`; main's check-site and phone-fit-full on the merge commit both green (look them up yourself if merge-pr.py prints NO RUN FOUND because it looked too early); report run IDs. Cloud handover documented.

STOP IF:
- The failure reproduces with options read after the reload (then it is a game bug: report, do not change the game).
- Another job on main is also failing for a reason this does not fix (report it).
- merge-pr.py reports it cannot reach GitHub (a 5xx during the Gate wait may be retried once with the same script).
