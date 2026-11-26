MARVIN-LOG (Project Claude, Wed 25 Nov 2026 09:35; checked against main c7805e6 at 11:50)
Jon, 25 Nov 2026, 09:22: "are we logging the scores on each game so we can tweak it?"; 09:24, to Project Claude's proposal (the result into columns the Sheet already keeps): "yes please." That is his approval for this field (no new collection without it, canon §0).
RECOMMENDED: Sonnet 5.5, effort medium. One analytics call in one game, with its verifier.
LANE: cloud (lane 1). SEND: now (TIER3-GUARD #909 merged as 419c531). Lane 2 may still be on BANKS-40 (Jon's request): the only shared file is docs/handover/cloud.md; before your merge, merge main in and keep both lanes' entries. One PR. Branch from current origin/main. No draft PR.

TASK: Make MaffsCards' game_completed record who won and the final tally in columns the Sheet already keeps, so Marvin's difficulty can be tuned from real games.

ROOT CAUSE: Shown: games/maffscards/index.html line 570 sends game_completed with level (deck-marvin), mode, score (rounds played) and won. The Sheet's doPost (docs/apps-script-endpoint.js, about lines 62-72) writes a fixed list of columns and has no 'won', so the result is dropped; GA4 receives won but cannot report it until it is registered (canon §8.3). So the Sheet holds rounds played but not who won or the score. Shown in the Sheet on 24 Nov: two MaffsCards games, neither with a result.

CLASS CHECK: Local: one game's completion event. No change to the Sheet's script (the columns used already exist and are written: correct, questions_answered, questions_correct, detail), to analytics.js or to any other game.

EXACT CHANGE:
0. First commit (after any claim commit): close-out for TIER3-GUARD #909 per AGENTS.md line 62 (merge commit 419c531, route merge-pr.py, last line "main 419c531 run 45597594977: GREEN"; check-site 45597594977, phone-fit-full 45597595086 with its final conclusion, and the pages run, each read back from the API); move its contract to docs/history/contracts/. Save this contract verbatim as docs/handover/contracts/2026-11-25-marvin-log.md.
1. games/maffscards/index.html, the game_completed call (line 570): keep every current parameter (game_slug, level, mode, score, won) and add:
   - correct: true when the player won, false when Marvin won or it was a draw (the 100-round cap);
   - questions_answered: rounds played (G.round);
   - questions_correct: rounds the player won (G.wins.you);
   - detail: exactly "you <G.wins.you> · Marvin <G.wins.marvin> · ties <rounds tied> · <win|loss|draw> · <why>", where why is G.result.why as the page already sets it (e.g. "ten", or the reason a deck game ended).
   Count ties from the rounds that went to the middle pile, not by subtraction if the page already counts them; say which.
   Nothing else in the game changes: no new event, no per-round event, no new storage.
2. scripts/verify-maffscards.py: where it already reads the events (about line 529), assert for a won first-to-10 game, a lost one, and an entire-deck game: correct, questions_answered, questions_correct and detail as above, consistent with the game's own tally (rounds won + rounds lost + ties = rounds played). Plants that must fail: correct true on a loss; questions_correct counting Marvin's wins; a detail whose numbers do not add up. Update the docstring's "analytics sends game_started and game_completed only" line to say what game_completed now carries.
3. Privacy: the privacy page's "Session completion and score data" already covers a game's result and score. Do not change it unless it does not; then STOP.
4. canon §1.3 or the analytics section, wherever MaffsCards' events are described (if nowhere, the analytics rules' per-game notes are not to be created): one line recording that MaffsCards' game_completed carries won in correct, the tally in questions_answered/questions_correct, and the score line in detail (MARVIN-LOG, Jon 25 Nov 2026). If canon has no MaffsCards analytics text at all, add nothing to canon and say so.
5. docs/handover/cloud.md entry. Merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600 on green; report its last line. No /updates/ line (nothing a student sees changes).

DO NOT TOUCH:
- docs/apps-script-endpoint.js and the live Sheet (no redeploy); schools/assets/analytics.js; every other game.
- Marvin's choices (MARVIN_BEST), the rules, the boards, the leaderboard submission, the look.
- GA4 settings (registering a dimension is Jon's, not a lane's).

SUCCESS CONDITION:
- A finished MaffsCards game writes a Sheet row whose correct, questions_answered, questions_correct and detail give the winner and the tally; verify-maffscards.py proves it for a win, a loss and a deck game, with all three plants caught.
- #909's close-out recorded; merged through merge-pr.py; its last line reported; cloud.md records this task.

STOP IF:
- Any of main's runs on 419c531 concluded anything but success (phone-fit-full 45597595086 included).
- Any of the four columns is not written by the live endpoint as the code in docs/apps-script-endpoint.js shows (it would need a redeploy, which is Jon's).
- The privacy page does not already cover game results and scores.
- merge-pr.py cannot reach GitHub, or refuses: report its output, do not merge another way.
