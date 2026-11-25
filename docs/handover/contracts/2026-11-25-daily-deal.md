DAILY-DEAL (Project Claude, Wed 25 Nov 2026 20:10; checked against main 5dd81d6)
Jon, 25 Nov 2026, 19:16-19:57 (all rulings below are his; the line pool is his or approved by him): a MaffsCards daily deal, the same for everyone each day, with Jon's own result on it, set from a Google Sheet with no page edit and no GitHub visit; "I would really like it to be running how we plan by the morning" (19:57). Rulings 20:05: a new small Creator sheet with its own script (the counts script stays read-only and untouched); a Sheet line over 240 characters is skipped for a pool line; "Today's deal" at the top of the menu; #916 stays open overnight.
RECOMMENDED: Claude Code, Opus 5.5 (or Fable), effort high. A game feature, a new workflow that commits to main, an Apps Script and a runbook; every number in the line pool must be right.
LANE: home. SEND: now. If #916 (SITE-BAR-PILOT) is mid-Gate, let the run finish and report it in one line, leave #916 OPEN and do not merge it tonight (Jon's ruling), then start this. Lane 2 is on VERIFIER-SPLIT PR 2 (scripts/ci-deps.py) then ANNOUNCE-STRIP (index.html, schools/assets/launch-sash.*, scripts/check-launch-sash.py; its PR B edits games/maffscards/index.html :189-194, the Aa results CSS): merge main in before merging and keep lane 2's CSS.
TIER: Shared (a new workflow that pushes to main). Stop at Gate green for Project Claude's review and Jon's "merge".

TASK: Give MaffsCards a daily deal (main deck, first to 10, Marvin Hard, the same deal for everyone each UK day) with Jon's result and a line on it, read from a file a new workflow writes when Jon fills a row in his Creator sheet.

ROOT CAUSE: A feature. Shown: the challenge machinery exists (games/maffscards/index.html: chEncode/chDecode, chKey, challengeChoice, deal(ch) at :481; challenge games off the board, boardScore :642; challenge true/false on both events :490, :655). The page loads its data with XMLHttpRequest beside itself (cards.json, :741). The answer-counts workflow is the model for a bot commit to main (.github/workflows/answer-counts.yml: permissions contents: write :36-37, concurrency :39, commit and push :79-80).

CLASS CHECK: Local to MaffsCards plus one new, self-contained workflow. It reuses the challenge generators and the existing commit pattern rather than adding a second shuffle or a second way to publish data. The counts Apps Script is deliberately read-only (docs/apps-script-counts.md) and is not touched.

THE LINE POOL (verbatim; {N} is Jon's round count; Jon's typos already fixed). Jon won: shown, then "Jon took {N} rounds." unless the line contains {N}.
W1 Marvin dreamt that Jon changed his parameters and that is why he lost. Jon did not, he's just a proper maths nerd. Are you?
W2 Marvin is busy running algorithms to prove that 9 should be a prime number so he can challenge the latest loss. It's not going well so far.
W3 Jon beat Marvin in {N} rounds. Marvin says he let him win. Marvin is lying. Beat {N}.
W4 Jon took {N} rounds. Marvin has requested a recount. Can you take fewer?
W5 Marvin insists that Jon wear short sleeves in future matches. He's convinced Jon had an extra 89 card up his sleeve.
W6 Jon won. Marvin has asked if they can play Some Thingies instead, as he's having an off day.
W7 Marvin has filed a complaint that 100 appears only once in the first 1,000 digits of pi. Pi has declined to comment.
W8 Marvin says Jon only won because 96's factors add up to 252, and that's 'just showing off'. Yes, Marvin. That's how winning works.
W9 Marvin has demanded a recount in Roman numerals. LXXXVIII apologises for nothing.
W10 Marvin has asked Jon to stop playing 64. Being a square AND a cube is, apparently, 'unsporting'.
W11 Marvin tried to play 1's largest prime factor. There isn't one. Marvin is having a quiet sit-down.
Marvin won:
L1 Marvin hacked his own code and won, Jon is trying to figure out the right ones and zeroes to fix this, check if he fixed it yet.
L2 Marvin beat Jon today. Jon has asked us to describe it as 'a tactical loss'. It was not.
L3 Today's deal: Marvin 10, Jon wept. Your turn to avenge him.
L4 Jon lost to Marvin. Jon built Marvin. Make of that what you will.
L5 Marvin beat Jon today and has been insufferable ever since. Please, someone, humble him.
L6 Jon was defeated by a computer he coded himself. Can you do what the creator could not?
L7 Jon lost to Marvin. Jon is now polishing his maths degree certificate and has challenged Marvin to Eigenvector Engine. Marvin says he doesn't do matrices on a school night.
L8 Marvin won and has changed his status to 'smarter than my creator'. Jon has changed his to 'rebooting'.
L9 Marvin beat Jon and now insists on being called Marvin the Magnificent. Please beat him so we can stop.
L10 Jon lost to Marvin. In his defence, he was distracted by 89 being exactly 8 from the nearest square. Pathetic, Jon.
L11 Marvin won today and celebrated by reciting the first 1,000 digits of pi. All of them. Twice. Make it stop.
L12 Jon says Marvin got lucky. Marvin says luck is just probability Jon didn't calculate. Settle it: win today's deal.

EXACT CHANGE:
0. First commit: save this contract verbatim as docs/handover/contracts/2026-11-25-daily-deal.md (and any close-out AGENTS.md requires of this lane).
1. The day and the deal (games/maffscards/index.html). today = the date in Europe/London as YYYY-MM-DD (Intl.DateTimeFormat with timeZone 'Europe/London'; a test hook may override it, never committed as a fixed date). The day's seed: a deterministic integer from the date string through the page's own 32-bit hash (chKey / mix32), reduced into 0..CH_SEEDS-1. The day's code: chEncode(seed, {deck: 'main', length: 'ten', marvin: 'hard'}), played through deal(ch) exactly as a challenge (same deal generator and per-decision Marvin), so it is off the board and replayable. Everyone gets the same code for the same UK date; it changes at UK midnight.
2. Jon's result: games/maffscards/daily.json beside the page, loaded like cards.json (XMLHttpRequest): {"date": "YYYY-MM-DD" or null, "result": "won" | "lost" | null, "rounds": int or null, "line": string or null}. Commit it as all nulls. It counts only when date == today; otherwise it is as if Jon has not played. A missing, unreadable or invalid file is the same as not played (never an error on screen).
3. The day's line: when Jon has played today: daily.json's line if it is a non-empty string of at most 240 characters; otherwise the pool line for the result, chosen by the day (the day number since 2026-01-01, modulo the pool's length for that result), so everyone sees the same line that day. The pool sits in the page in a JSON block like marvinLines (:206), id dailyLines, verbatim from THE LINE POOL above. {N} becomes rounds. Text set by textContent, never HTML. Game names in lines stay plain text (no links in this contract).
4. "Today's deal" panel, top of the menu (above the Deck heading, :265), in the menu's existing styles: heading "Today's deal" and the date (e.g. "Wed 26 Nov"); the status: not played: "Jon hasn't played today's deal yet."; Jon won: the line, then "Jon took {N} rounds." unless the line has {N}; Jon lost: the line. A button "Play today's deal" (starts the day's code; the menu's options are set to the deal's settings, as a challenge does). Plain placeholders for the panel's fixed words; Jon rewrites after playing.
5. Results of a daily game: one line (in the challenge line's place, :329): you won: "You took X rounds." plus, when Jon played and won: "Jon took N: you beat him." / "Jon took N: you matched him." / "Jon took N: he beat you."; when Jon lost: "Jon lost to Marvin today. You did what Jon could not."; you lost: "Marvin beat you too." when Jon lost, "Marvin won this time." otherwise; Jon not played: "Jon hasn't played today's deal yet." (Fewer rounds is better; a first-to-10 game you won has X >= 10.) The leaderboard note reads as for a challenge. "Play again" after a daily game starts today's deal again.
6. Analytics: a daily game sends mode 'daily' on game_started and game_completed (the existing mode parameter), challenge true, and detail gains " · daily". Never the code, the date or anything of Jon's. No other change to events or storage.
7. The workflow: .github/workflows/maffscards-daily.yml, workflow_dispatch only, inputs date, result, rounds, line (line optional). It runs scripts/set-maffscards-daily.py, which validates: date is YYYY-MM-DD and is today or yesterday in Europe/London; result is won or lost; rounds is a whole number, 10 to 100 when won, 10 to 200 when lost; line is plain text (no "<" or ">"), stripped, at most 240 characters, else written as null; and the repo's personal-details check passes on the line (else null). Then it writes games/maffscards/daily.json and commits "Record the MaffsCards daily result [skip ci]" and pushes to main, copying answer-counts.yml's permissions, concurrency and commit-and-push pattern (:36-39, :79-80). A failure writes nothing and fails the run. The script has --selftest (each planted bad input rejected; good inputs pass) and a # ci-line so CI runs the self-test.
8. The Creator sheet's script (docs/apps-script-creator.js, nothing secret in it) and its runbook (docs/apps-script-creator.md, written for Jon, one step per numbered line, in the style of docs/apps-script-counts.md): a new Google Sheet "MaffsGames Creator", headers in row 1: Date | Result | Rounds | Line; a script bound to it with an installable on-edit trigger that, when the edited row has Date, Result and Rounds filled, POSTs to https://api.github.com/repos/OrthogonalMaffs/maffsgames/actions/workflows/maffscards-daily.yml/dispatches with {ref: 'main', inputs: {...}} using a token read from Script Properties (GITHUB_TOKEN); it writes "sent HH:MM" or the error into column E of that row. The runbook covers: making the sheet; pasting the script; creating a fine-grained GitHub token (this repository only; Actions: read and write; expiry one year; never pasted anywhere but Script Properties); storing it; installing the trigger; the permissions Google will ask for (this spreadsheet, connect to an external service) and to stop and ask if it asks for anything else; a first test row; and the fallback: GitHub → Actions → maffscards-daily → Run workflow, the same four fields, from a phone.
9. Verifier (scripts/verify-maffscards.py, new SHARD units; existing units and plants unchanged):
   - daily: the date-to-code rule matches this script's own for 400 consecutive days across both clock changes; the same date gives the same code in two page loads; different dates differ; the code decodes to main / ten / hard.
   - pool: every line in the page's dailyLines equals THE LINE POOL verbatim; every number fact checked against games/maffscards/cards.json: 100's pi count is 1; 96's sum of factors is 252; 88's Roman numeral is LXXXVIII; 64 is a square and a cube (its powers list); 1 has no largest prime factor (lpf 0); 89 is in the main deck once and its distance to the nearest square is 8 (81) and 89 - 81 < 100 - 89; 9 = 3 x 3 is not prime; Some Thingies and Eigenvector Engine are roster names of listed games.
   - status and results, in Chromium with the clock hook: not played (nulls, stale date, missing file, invalid file); won with a Sheet line, with a 241-character line (pool line shown), with no line (pool line, {N} filled, "Jon took N rounds." added only when the line lacks {N}); lost; each results branch of step 5; the same line for everyone on one day (two loads).
   - board and analytics: a daily game never submits; mode 'daily', challenge true, " · daily" in detail.
   - fit: the panel and the daily results at 320x568 and 375x667, normal and Aa.
   - plants (each must FAIL): the day's code from Math.random; a pool line changed by one word; W8's 252 changed to 250 in the facts table; a stale-date daily.json shown as today's; a 241-character line shown; a daily game submitted to the board.
10. scripts/set-maffscards-daily.py --selftest in CI; the roster row 114: one sentence: "Today's deal (DAILY-DEAL, 25 Nov 2026): the same main-deck, first-to-10, Hard deal for everyone each UK day, off the board, with Jon's result and a line read from games/maffscards/daily.json, which the maffscards-daily workflow writes from his Creator sheet." /updates/: "MaffsCards: Today's deal. A new deal every day, the same for everyone. Can you beat Jon?" docs/handover/home.md entry.
11. At Gate green: stop; report the head SHA, the Gate and phone-fit run IDs, and what Jon must do next (the runbook's first step); wait for Jon's "merge". Then merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600; report its last line. After the merge, run the workflow once yourself with a test row only if Jon asks; otherwise leave daily.json as nulls.

DO NOT TOUCH:
- Normal games and challenge codes: their generators, Marvin, rules, boards, lines (marvinLines), wording, analytics; the menu's existing sections beyond adding the panel above them.
- docs/apps-script-counts.js, docs/apps-script-endpoint.js, the counts and analytics Apps Scripts, scripts/fetch-answer-counts.py, .github/workflows/answer-counts.yml (model only), check-site.yml, phone-fit-full.yml.
- firebase/, schools/assets/ (shared assets), privacy/, every other game, #916's branch, canon beyond one line naming the new workflow where canon lists answer-counts.yml.
- No token, secret or Sheet id anywhere in the repo.

SUCCESS CONDITION:
- On the live page after merge: "Today's deal" at the top of MaffsCards' menu, the same deal for everyone that UK day, "Jon hasn't played today's deal yet." until a row arrives; a test of the workflow (by Jon, through the sheet or the Run workflow form) shows his result and the right line within minutes.
- The verifier proves the date rule, every pool line and every number in it, every status and results branch, off-board, analytics and fit; every plant caught; set-maffscards-daily.py --selftest passes.
- The runbook lets Jon set up the sheet without help beyond it; no secret in the repo.
- Gate green, Project Claude's review, merged after Jon's "merge"; last line reported; home.md records it.

STOP IF:
- A bot commit from the new workflow cannot push to main the way answer-counts.yml does (branch protection, permissions): report the error; do not weaken any protection.
- The day's deal cannot be played through deal(ch) without changing normal or challenge play: report why.
- Any pool line's fact fails against cards.json: report the line; do not change the line (Jon's words) or the cards.
- Phone fit fails at 320x568 because of the panel and the fix needs more than this page's own layout.
- Any existing check fails and the cause is not in this change.
- merge-pr.py cannot reach GitHub, or refuses: report its output; do not merge another way.
