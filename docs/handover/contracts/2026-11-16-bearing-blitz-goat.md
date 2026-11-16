Recommended: Sonnet, medium effort. One game's start screen, counter, points and message, plus its verifier; small and local.

TASK: Bearing Blitz: tell the player the run's length on the start screen and in the counter, and reward a dead-on shot (0° off) with its own message and a bonus.

ROOT CAUSE: games/bearing-blitz/index.html ends a run at MAX_TARGETS = 20 (line 129), but the start screen (lines 95-99) never says how many ships there are and the HUD counter (line 108) shows only "Ships sunk 18", so a player cannot tell the game ends (Jon, 16 Nov, after sinking 18 in a row). A shot 0° off scores 150 and gets the same message as one 1° off (lines 270-276), so a perfect shot is not recognised.

CLASS CHECK: Local. Both gaps are this game's own text and scoring in its own page: MAX_TARGETS, its menu copy, its HUD and its hit branch exist only here; no shared asset (schools/assets/) is involved, and no other game shares this code. So the fix is in games/bearing-blitz/index.html and its own verifier, scripts/verify-bearing-blitz.py.

EXACT CHANGE:
First commit: HAMSTER-PACK-FINAL's close-out (AGENTS.md cloud close-out rule). Merged #799 as bf6cd95 via merge-pr.py on the first attempt, last line "main bf6cd95 run 43930644204: GREEN", exit 0. Main's runs on bf6cd95: check-site 43930644204 success 18:49:16 UTC, phone-fit-full 43930644108 success 18:49:07 UTC, both push-triggered. Move docs/handover/contracts/2026-11-16-hamster-pack-final.md to docs/history/contracts/. In the same commit, close docs/todo.md row LEDGER-B4-ANGLE-ACE (it still says gcse 35; ANGLE-ACE-GCSE-45, #795, 833f6e1, made the GCSE bank 45), moving it to docs/history/todo-done.md as the repo does. Save this contract verbatim at docs/handover/contracts/2026-11-16-bearing-blitz-goat.md.

1. Start screen (menu-info, lines 95-99): add as its first line, in bold, Jon's wording verbatim:
   "20 enemy ships. Only 22 torpedoes. Can you become a legend?"
   Build the two numbers from MAX_TARGETS (20) and MAX_TARGETS + 2 (22: 19 hits and 3 misses, or 20 hits and 2 misses, is the most any game can fire) in script, not typed, so they cannot drift from the rule. Keep every existing line (drag the needle, ±5° tolerance, "Three lives." ..., the North reminder) unchanged.
2. HUD counter (line 108 and every place that sets #sunk: lines 233, 274): show "n / 20" (e.g. "18 / 20"), the 20 from MAX_TARGETS. The label "Ships sunk" stays.
3. Scoring (lines 270-271): 0° off scores 200; 1° 150; 2-3° 100; 4-5° 50 (unchanged above 0°).
4. Hit message (line 276): when diff is 0 the message is exactly
   💥 HIT! 0° off. The radar operator whispers: “this one is the GOAT.” +200 points
   (curly quotes as shown). Every other hit keeps today's message unchanged.
5. scripts/verify-bearing-blitz.py: update its independent model and docstring to the new rules: points 200/150/100/50; the 0° message above verbatim; the counter "n / 20"; the start-screen line with 20 and 22. Add planted faults that must be caught: 0° scoring 150; the 0° message shown at 1° off; the counter missing "/ 20"; the start screen saying 21 torpedoes. All existing plants still caught; the twenty-hit flow's score recomputed under the new points.
6. /updates/: one dated plain-words line (student-visible): Bearing Blitz now shows how many ships are left and rewards a perfect shot.

Lane note: this is a per-game fix, cloud lane's own. The todo.md row closure and contract move are the standing close-out rule.

DO NOT TOUCH: the tolerance (±5°), lives, MAX_TARGETS, the bearings list or generateBearings(); the miss messages; the end screen; the leaderboard call, slug or level ('all'); analytics events; schools/assets/; any other game; firebase/; Gate files (workflow, scripts/ci-*, merge-pr.py); the home-lane handover.

SUCCESS CONDITION:
- On the live page after merge: the start screen's first line reads "20 enemy ships. Only 22 torpedoes. Can you become a legend?"; the counter reads "0 / 20" at the start and "n / 20" after each hit; a 0° hit shows the GOAT message and adds 200; 1° adds 150 with the old message.
- scripts/verify-bearing-blitz.py passes on main with its self-test, every old and new plant caught.
- Run only the checks this contract names and the Gate; no optional all-game local runs.
- PR merged on green via `python -X utf8 scripts/merge-pr.py <n>`; report its last line and exit status, and main's check-site and phone-fit-full run IDs and results on the merge commit. Cloud handover documented; contract saved as in the first commit.

STOP IF:
- Any other check (theme, start-mount, answer-lock, phone-fit) fails because of the new start-screen line or counter text: report the message; do not edit the check.
- The verifier cannot set a needle exactly 0° off a target through the real compass (it already reads every whole degree back; if that is no longer true, stop).
- merge-pr.py reports it cannot reach GitHub (a 5xx during the Gate wait may be retried once with the same script).
