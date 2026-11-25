MAFFSCARDS-CHALLENGE (Project Claude, Wed 25 Nov 2026 17:00; checked against main 24835d0)
Jon, 25 Nov 2026: "option 1 please" (a challenge code, not live two-player). His rulings, 16:45: challenge games are off the leaderboard; a 6-character code plus a link; game_started and game_completed carry a challenge flag (true/false, never the code); plain placeholder wording, which Jon rewrites after playing.
RECOMMENDED: Claude Code, Opus 5.5, effort high. One game file and its verifier, but the fairness logic (a deal and a Marvin both students share) must be exact and proved.
LANE: home. SEND: now. Lane 2 is merging #912 (it adds an /updates/ line): merge main into your branch before you merge.
TIER: Medium (merge on green).

TASK: Add "Challenge a friend" to MaffsCards: a 6-character code (and a link) that gives two students the same settings, the same deal and the same Marvin, so they can compare rounds taken.

ROOT CAUSE: A feature, not a bug. Shown (games/maffscards/index.html): one generator, rng (line 330; MC.seed swaps it at :639), drives the shuffle (deal, :408-410), Marvin's start line (:456), every quip (:389), the end line, and Marvin's choices (marvinChoice :364, easyChoice :361). A shared seed alone would therefore NOT give a shared Marvin: after round 1 the number of rng draws depends on the student's own choices (who chooses next, which quips fire), so the two students' Marvins drift apart. A challenge needs its own generators: one for the deal, and one per Marvin decision keyed to the decision, not to the order of draws.

CLASS CHECK: Local. Only MaffsCards has a computer opponent and a dealt deck; no shared asset is involved, and the normal (non-challenge) game's behaviour, including rng and the verifier's seeded simulations, must stay exactly as it is.

EXACT CHANGE (games/maffscards/index.html, scripts/verify-maffscards.py, .claude/rules/game-roster.md row 114, updates/index.html):
0. First commit: save this contract verbatim as docs/handover/contracts/2026-11-25-maffscards-challenge.md.
1. The code. ALPHABET = '23456789ABCDEFGHJKMNPQRSTUVWXYZ' (31 characters: no 0, 1, I, L or O). A code is 5 data characters then 1 check character.
   - Data: the five characters read as a base-31 number v (first character most significant), 0 <= v < 31^5. settings = v % 8: bit 1 deck (0 main, 1 all), bit 2 length (0 ten, 1 deck), bit 4 marvin (0 easy, 1 hard). seed = floor(v / 8).
   - Check: ALPHABET[(1*d1 + 2*d2 + 3*d3 + 4*d4 + 5*d5) mod 31], where di is the index of data character i. This catches every single wrong character and every swap of two neighbouring data characters.
   - Reading a code: trim spaces, upper-case; reject (no game) if the length is not 6, any character is outside ALPHABET, or the check fails.
   - Making a code: seed from rng (so the verifier can seed it), settings from the menu's current options.
2. The challenge game. In deal() (:408), when a challenge is being played: settings come from the code (and the menu's option buttons are set to match, so the student sees them); the shuffle uses its own seeded(f(seed)) generator, not rng; G.challenge holds the code. Marvin's choice in a challenge uses a fresh seeded generator per decision, made from a 32-bit integer derived from (seed, Marvin's card number, k), where k is how many times Marvin has already chosen with that card in this game (0 the first time); its first draw decides best-or-random against MARVIN_BEST, its second draws the random category. Distinct (seed, n, k) must give independent streams (use a proper integer hash, not a sum). Nothing in a challenge game draws from rng except the lines (start, quips, end), which do not affect play. A normal game is unchanged: same rng, same draws, same order.
3. Menu (below the start row, :264): a "Challenge a friend" section with plain placeholder text (Jon rewrites):
   - heading "Challenge a friend"; line "Same deal, same Marvin. Make a code, send it to a friend, and see who takes fewer rounds."
   - button "Make a challenge code": shows the code large, a read-only box with the link (location.origin + '/games/maffscards/?c=' + CODE), a "Copy link" button (navigator.clipboard.writeText inside try; on failure, select the box's text), and a "Play it" button.
   - "Got a code?" input (labelled) and a "Play the challenge" button; a bad code shows "That code doesn't work. Check each letter and number." and starts nothing.
   - Opening the page with ?c=CODE fills the input and sets the options to the code's settings; it never starts a game by itself. The page's level handling (MaffsLevel reads only 'level') is unchanged.
4. Results for a challenge: one extra line, "Challenge CODE: N rounds. Your friend plays the same deal with the same code." boardScore() (:561) returns null for a challenge, so nothing is submitted (:576); lbNote (:586) reads "Challenge games don't go on the leaderboard." "Play again" after a challenge starts a normal game with the same settings (the code stays in the menu to replay).
5. Analytics: game_started (:415) and game_completed (:573) gain challenge: true or false (never the code). game_completed's detail gains " · challenge" at the end when true, so the Sheet shows it in its existing column. No other event, parameter or storage.
6. Verifier (scripts/verify-maffscards.py), new checks, all existing checks and plants unchanged and passing:
   - encode/decode round trip for all 8 settings over at least 1,000 seeds, including seed 0 and the largest seed; every code is 6 characters from ALPHABET.
   - every single-character change to the data characters and every neighbouring swap of distinct data characters, on 200 codes, is rejected.
   - fairness, in Chromium, for each of the 8 settings: two scripted players with different strategies (e.g. always the first category; always the best on the card) play the same code: identical starting piles; and for every (Marvin card, k) both games reach, the same category.
   - a challenge game never calls submitScore and its events carry challenge true; a normal game's carry challenge false.
   - a normal game seeded with MC.seed(n) produces the same deal and the same Marvin choices as before this change (compare against main's page for 3 seeds).
   - plants (each must FAIL): the check character ignored; Marvin's challenge choice drawn from rng; a challenge game submitted to the leaderboard.
7. The menu's new section and the results line fit 320x568 in normal and Aa mode (phone fit runs on the PR by itself; do not dispatch it).
8. Roster row 114 (.claude/rules/game-roster.md): add one sentence: "Challenge a friend (MAFFSCARDS-CHALLENGE, 25 Nov 2026): a 6-character code or ?c= link gives two students the same settings, deal and Marvin; challenge games are not on the leaderboard and carry challenge: true." Update the verifier's ci-line to name the new checks.
9. /updates/: one dated line, plain words: "MaffsCards: challenge a friend. Make a code, send it, and play the same deal against the same Marvin." docs/handover/home.md entry with the PR, run IDs and what changed. Merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600 on green; report its last line.

DO NOT TOUCH:
- The normal game: rng, its draw order, shuffle for normal games, MARVIN_BEST, hardChoice, judge, the rules, the cap, boards, leaderboard behaviour for normal games, Marvin's lines (Jon's, verbatim).
- cards.json, tools/maffscards/, the look of the card, the reveal and the results (beyond the one results line and the new menu section in the page's existing styles).
- firebase/, schools/assets/ (all shared assets), privacy/, the Apps Script / Sheet, canon, every other game, .github/workflows/.
- No live two-player, no database writes, no localStorage for challenges, no new event.

SUCCESS CONDITION:
- A code made on one device, typed or linked on another, gives the same settings, the same starting piles and the same Marvin choice for every (card, k) both games reach; proved by the verifier in Chromium for all 8 settings.
- Bad codes rejected with the message; ?c= fills but never starts.
- Challenge games never on the leaderboard; events carry challenge true/false; normal games unchanged (proved against main for 3 seeds).
- verify-maffscards.py passes with the new checks and plants; Gate and phone fit green; merged through merge-pr.py, last line reported; home.md records it.

STOP IF:
- Making the normal game unchanged is impossible without touching rng's draw order: report why; do not change normal play.
- The privacy page lists per-event parameters such that the challenge flag would make it untrue: report the line; do not edit privacy/.
- Phone fit fails at 320x568 because of the new section and the fix needs anything beyond this page's own layout: report the measurement.
- Any existing check or plant fails and the cause is not in this change.
- merge-pr.py cannot reach GitHub, or refuses: report its output; do not merge another way.
