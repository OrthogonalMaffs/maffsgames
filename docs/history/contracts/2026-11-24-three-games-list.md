THREE-GAMES-LIST (Project Claude, Tue 24 Nov 2026 21:45; checked against main a62ebe4)
APPROVAL (verbatim in the PR body and home.md):
- Jon, 24 Nov 2026, 21:32: "lets release maffscards and the 2 primary games please."
- Jon, 24 Nov 2026, ~21:35, answering Project Claude: "No Essentials cards" (portal KS3 section only; the two primary games stay on /class/ as now).
RECOMMENDED: Opus 5.5, effort medium. A listing of three games by existing conventions; nothing to design.
LANE: home. SEND: now (Jon is at his PC; TIER3-LOCK-FIX #904 has merged). TIER: Medium, merge on green.
MERGE TIMING: the cloud lane is on BASE-60-PLAY (games/its-just-base-60-bruv/, its verifier, docs/todo.md row BASE60-LIST, cloud.md). One merge heading for main at a time: if its merge is in progress when yours is green, wait, merge main into your branch, re-run the Gate, then merge.

TASK: List MaffsCards (games/maffscards/), Sums in Disguise (games/sums-in-disguise/) and Some Thingies (games/some-thingies/) on the live site: roster KS3 Games, portal KS3 cards, sitemap, spec map where a row fits, leaderboard hub, /updates/.

ROOT CAUSE: All three merged unlisted for Jon to play (MAFFSCARDS-GAME 20 Nov, SUMS-IN-DISGUISE 18 Nov, SOME-THINGIES 21 Nov 2026); he has now approved listing. Every listing surface still leaves them out:
- scripts/check-leaderboard-coverage.js NOT_ON_HUB: sums-in-disguise (line 180), some-thingies (182), maffscards (186).
- scripts/audit-register.py lines 89, 90, 92 and scripts/check-theme.py lines 78-80 carry "unlisted until Jon approves" notes.
- games/maffscards/index.html line 6: <meta name="robots" content="noindex">.
- .claude/rules/game-roster.md rows #113 (line 185), #114 (186), #115 (187) under "## Unlisted (12)" (line 148), with their notes at lines 160, 162 and 163.

CLASS CHECK: Not a bug class: a planned listing of three games by existing conventions. Patterns to copy:
- Year 6 portal cards: negative-number-line's (index.html:1348, data-levels="year6 ks3", href with ?level=year6), in the KS3 section (index.html:981).
- Hub rows: negative-number-line's (leaderboards/index.html:202, single board) and whose-side-are-you-on's (line 221, stage boards). check-leaderboard-coverage.js already has maffscards' board entry (line 213).
- The ITS-A-SINE-LIST listing (17 Nov 2026) for the full set of surfaces.

EXACT CHANGE:
0. First commit: save this contract verbatim as docs/handover/contracts/2026-11-24-three-games-list.md; close out TIER3-LOCK-FIX #904 per AGENTS.md (merge commit 590efd7, merge-pr.py's last line, main's check-site, phone-fit-full and pages run IDs and conclusions, read back from the API) and move its contract to docs/history/contracts/.
1. games/maffscards/index.html: remove the noindex meta (line 6). Remove any noindex or UNLISTED marker from the other two pages if present (none found on a62ebe4). Nothing else in any game.
2. index.html, KS3 section: one card each, built as negative-number-line's, placed by the section's existing order (report the rule you followed):
   - sums-in-disguise and some-thingies: data-levels="year6 ks3" as the other Year 6 games have (report if the roster's Year 6-only level should map differently), href ?level=year6, data-topics number.
   - maffscards: data-levels="ks3", data-topics number.
   - data-keywords from each game's data/games.json keywords; data-badge="new" and data-badge-date="<go-live date>".
   - The card links to the standard look, never to #kids.
3. sitemap.xml: one <url> each, in negative-number-line's form (line 87).
4. spec-map/index.html: add maffscards to the KS3 Number row(s) about factors, primes and powers, in that row's link form; report which. The spec map has no Year 6 or KS2 rows: do not add the two primary games, and report it.
5. leaderboards/index.html: a hub row for each, with exactly the board keys each game submits to (read them from its MaffsLeaderboard.submitScore calls: sums-in-disguise stage-1..stage-5; some-thingies stage-1..stage-4 and pro-stage-1..pro-stage-4; maffscards main-easy, main-hard, all48-easy, all48-hard), placed by the hub's grouping. scripts/check-leaderboard-coverage.js: remove the three NOT_ON_HUB entries, and add stage-board entries in the existing form if the check needs them.
6. The notes in scripts/audit-register.py (89, 90, 92) and scripts/check-theme.py (78-80): say each was listed <go-live date> (Jon approved 24 Nov 2026). Change no logic.
7. .claude/rules/game-roster.md:
   - Move rows #113, #114 and #115 from "## Unlisted (12)" to "## KS3 Games (35)", keeping their numbers and columns. Counts become KS3 Games (38) and Unlisted (9).
   - Append to each Description: "Look signed off by Jon, 2026-11-24."
   - Replace each "New ..." note (lines 160, 162, 163) with a "**Listed <go-live date>:**" note in the its-a-sine form: what it was merged as, "Jon approved listing, 24 Nov 2026, 21:32; KS3 section, no /essentials/ card; listed by the home lane", now KS3 Games #<n>.
8. updates/index.html, under November 2026, "New" (line 121), in the list's form, plain words, no word that labels students:
   - "MaffsCards: a number card game against Marvin, the computer. Pick the value you think beats his card: sum of factors, largest prime factor, superpowers and more."
   - "Sums in Disguise: adding within 100 with a fact you already know. Take off the disguise, find the little sum, then put it back on. For primary classes."
   - "Some Thingies: multiplication as equal groups, adding, arrays and times-table facts, the 2, 5 and 10 times tables, then the 3, 4 and 8. For primary classes."
9. docs/todo.md: rows MAFFSCARDS-LIST, SUMS-IN-DISGUISE-LIST and SOME-THINGIES-LIST: by the TODO-TRIM rule, move the listing part word for word to docs/history/todo-done.md and rewrite each row to what is still owed (e.g. SOME-THINGIES-LIST keeps the class teacher's questions and Jon's LINES rewrites); a row with nothing owed moves whole. Add no new row. home.md entry with the approval verbatim.
10. Merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600 when the Gate is green (per MERGE TIMING); report its last line.

DO NOT TOUCH:
- Anything in the three games beyond step 1.
- data/games.json; /essentials/ (Jon's ruling: no cards); /class/ (the two primary games are already there).
- Every other roster row and section.
- schools/assets/; canon; AGENTS.md; Gate files (workflow, scripts/ci-*, ci_shards.py, merge-pr.py, check-context-size.py, check-changed.py); robots.txt; docs/handover/cloud.md.
- games/its-just-base-60-bruv/ and its verifier, and todo row BASE60-LIST (the cloud lane's BASE-60-PLAY).
- No draft PR.

SUCCESS CONDITION:
- The portal's KS3 section shows the three cards with New badges; the portal search finds MaffsCards by "card game", Sums in Disguise by "addition" and Some Thingies by "times tables" (all in their data/games.json keywords).
- The sitemap, the hub (each game's boards), the spec map (MaffsCards) and /updates/ include them; MaffsCards no longer carries noindex.
- The roster lists them under KS3 Games with "Look signed off by Jon, 2026-11-24."; check-look-signoff, leaderboard coverage, sitemap/SEO, check-levels, check-theme and phone-fit on the portal are green.
- Merged by merge-pr.py, with its last line, the merge commit and main's check-site and phone-fit-full run IDs reported; screenshots of the three portal cards at 1366 x 768 and 375 x 667 in the report.

STOP IF:
- A listing check fails for a reason outside these files.
- A check requires a game to appear somewhere this contract does not name (report where before adding it).
- The hub cannot show a game's boards without editing shared code, or check-leaderboard-coverage.js needs more than the NOT_ON_HUB removals and board entries.
- The change would touch a file outside: games/maffscards/index.html (step 1), the other two game pages (step 1 only, if a marker exists), index.html, sitemap.xml, spec-map/index.html, leaderboards/index.html, scripts/check-leaderboard-coverage.js, scripts/audit-register.py, scripts/check-theme.py, the roster, updates/index.html, docs/todo.md, docs/history/todo-done.md, docs/handover/home.md and its archive, and the contract files.
- merge-pr.py cannot reach GitHub, or refuses for a reason other than a transient 5xx it already retries: report its output, do not merge another way.

Amendment 1 (Jon, 24 Nov 2026, about 21:45, in session, answering the home lane's STOP): scripts/check-spec-mapping.py fails a game with a portal card that is not on the spec map, and it failed sums-in-disguise and some-thingies. Offered an EXCEPTIONS entry, the UNMAPPED list, a GCSE N2 mapping or a hold, Jon chose "EXCEPTIONS entry (Recommended)": both games are added to EXCEPTIONS in scripts/check-spec-mapping.py, with the reason that they are primary content and the spec map has no Year 6 or KS2 rows. That file joins the contract's file list. No logic changes.
