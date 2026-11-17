LANE: cloud (Claude Code on the web), one-off LANE EXCEPTION (listing is normally home-lane work; Jon, 17 Nov 2026, chose "Cloud, before ice cream"). SEND: now (CORE-PAPER-EXIT #816 merged and reported 19:53); before I DROPPED MY ICE CREAM. Line numbers re-checked on main 7d8ff64 (17 Nov 19:50): all as below.
TIER: Medium (a listing that edits several site surfaces and CI-check note lists; no shared asset). Merge on green, Project Claude reviews after.
RECOMMENDED: Opus 5.5, medium effort. A listing by existing conventions; nothing to design.
MERGE TIMING: one merge heading for main at a time. CANTEEN-PACK (#817, home lane) is queued to merge now; if it is in its Gate or merge when yours is green, wait for it, rebase, then merge.

APPROVAL (verbatim in the PR body and cloud.md):
- Jon, 17 Nov 2026, 14:58: "also the students have tried the it's a sign game, it's ready to get listed now please"
- Jon, 17 Nov 2026, ~15:03, answers to Project Claude:
  - levels "All three" (GCSE, Level 3, Level 4);
  - placement "GCSE section" (roster GCSE Games, a portal GCSE card, NO /essentials/ card);
  - lane "Cloud, before ice cream".

TASK: ITS-A-SINE-LIST. List "It's a SINE!! / No it's not" (games/its-a-sine/) on the live site at all three levels: roster GCSE Games, a portal GCSE card, sitemap, spec map, leaderboard hub, /updates/.

ROOT CAUSE: It merged unlisted (contract SINE-NOT-SINE, #810, 17 Nov) for Jon to play and use by URL. His class has played it and he has approved listing. Every listing surface still leaves it out:
- scripts/check-leaderboard-coverage.js:178 lists it in NOT_ON_HUB: "new, unlisted until Jon has played and approved it; hub row added at listing".
- scripts/audit-register.py:87 and scripts/check-theme.py:76 carry "unlisted until Jon approves" notes.
- .claude/rules/game-roster.md row #111 (line 178) is under "## Unlisted (8)" (line 147), with the note at line 153.

CLASS CHECK: Not a bug class. This is a planned listing of one game by existing conventions. Patterns to copy:
- whose-side-are-you-on: GCSE section, staged game, portal card at index.html:2353, hub row at leaderboards/index.html:220, sitemap.xml:123.
- cast-away: stage boards, hub row at leaderboards/index.html:275, coverage entry at check-leaderboard-coverage.js:203.

EXACT CHANGE:
0. First commit: CORE-PAPER-EXIT's close-out per AGENTS.md: #816 squash-merged as 7d8ff64 at 19:39:03 UTC via merge-pr.py, exit 0, last line "main 7d8ff64 run 44160860707: GREEN"; main on 7d8ff64: check-site 44160860707 success, phone-fit-full 44160860832 success, pages build 44160860492 success; PR's final checks on head 4dfe3ff: Gate 44158222817 and phone-fit-full 44158207479 green. Record: agent Claude Code; wall about 4:41 (contract 14:58, merged 19:39, mostly the step-W wait for #815 and runner queues); review cycles 1 (first Gate red on Answer lock: the exit row was open to a double-click's second click after Play again; fixed in stage-exit.js); amendments 1; usage n/a. Move its contract to docs/history/contracts/. Also any other merged PR not yet closed out on main.
1. games/its-a-sine/index.html: if it carries any noindex meta or UNLISTED comment, remove it (none was found on fee6ad3). Nothing else in the game.
2. index.html: one card for games/its-a-sine/ in the GCSE section, built as whose-side-are-you-on's card, placed by the section's existing order.
   - data-levels from the portal's own vocabulary: GCSE plus Level 4 ("l4"). The portal has no Level 3 tag (no card uses one). Say what you chose and why.
   - data-topics from the roster's Geometry.
   - data-keywords from data/games.json's its-a-sine keywords.
   - data-badge="new" and data-badge-date="<go-live date>".
   Report which ordering rule you followed.
3. sitemap.xml: one <url> for https://maffsgames.co.uk/games/its-a-sine/, in its neighbours' form.
4. spec-map/index.html:
   - Add it to the GCSE row "G22–G23 Sine rule, cosine rule, area = ½ab sin C (Higher)" (line 146), in that row's link form, with ?level=gcse.
   - Add it to the Level 4 row "LO2 Trigonometry: SOH CAH TOA, sine/cosine rules, radians" (line 283), with ?level=level4.
   - Report any Level 3 row about the sine/cosine rules; do not add one.
5. leaderboards/index.html: a hub row for its-a-sine with exactly the board keys the game submits to (read them from its MaffsLeaderboard.submitScore calls), placed by the hub's grouping.
   scripts/check-leaderboard-coverage.js: remove 'its-a-sine' from NOT_ON_HUB (line 178), and add its stage-board entry in cast-away's form (line 203) if the check needs one.
6. The "unlisted" notes: update scripts/audit-register.py:87 and scripts/check-theme.py:76 to say it was listed <go-live date> (Jon approved 17 Nov 2026). Change no logic.
7. .claude/rules/game-roster.md:
   - Move row #111 from "## Unlisted (8)" to "## GCSE Games (30)", keeping its number and columns.
   - Append to its Description: "Look signed off by Jon, 2026-11-17."
   - The counts become GCSE Games (31) and Unlisted (7).
   - Replace the "New 17 Nov 2026 (contract SINE-NOT-SINE, cloud lane)" note (line 153) with: "**Listed <go-live date>:** `its-a-sine` (merged unlisted 17 Nov for Jon to play, contract SINE-NOT-SINE; his Level 3 class played it; Jon approved listing at all three levels, 17 Nov 2026, 14:58; GCSE section, no /essentials/ card; listed by the cloud lane under his one-off lane exception), now GCSE Games #111."
8. updates/index.html, under November 2026, "New", in the list's form: "It's a SINE!! / No it's not: sine rule or cosine rule? Pick the rule, pick the version, then solve the triangle. Worked examples for each. For GCSE Higher, Level 3 and Level 4." Plain words; no word that labels students.
9. docs/todo.md: close ITS-A-SINE-LIST (line 235 on 7d8ff64; re-find it after any rebase) to docs/history/todo-done.md with this PR. docs/todo.md is within ~120 bytes of its 153,600-byte cap: add no new row. Add a cloud.md entry with the approval and the lane exception verbatim.
10. Merge with scripts/merge-pr.py <n> --watch --wait 3600 when the Gate is green (per MERGE TIMING).

DO NOT TOUCH:
- Anything in the game beyond step 1.
- data/games.json.
- Every other roster row and section.
- schools/assets/; canon; AGENTS.md; Gate files and workflows; robots.txt; docs/handover/home.md.
- /essentials/ (no card, by Jon's ruling).
- Any other game's listing state.
- tools/pack-generator/ (CANTEEN-PACK).
- No draft PR.

Run only the checks this contract names and the Gate (listing checks: check-look-signoff, leaderboard coverage, sitemap/SEO, check-levels, phone-fit on the portal). No optional all-game local runs.

SUCCESS CONDITION:
- The portal's GCSE section shows the card with a New badge, and the portal search finds it by "sine rule" and "cosine rule".
- The sitemap, the two spec-map rows, the hub (its boards) and /updates/ include it.
- The roster lists it under GCSE Games with "Look signed off by Jon, 2026-11-17.".
- check-look-signoff, leaderboard coverage, sitemap/SEO, check-levels and phone-fit are green.
- cloud.md is under 18 KiB.
- Merged by merge-pr.py, with its last line, the merge commit and main's check-site and phone-fit-full run IDs reported.
- Screenshots of the portal card at 1366×768 and 375×667 in the report.

STOP IF:
- A listing check fails for a reason outside these files.
- A check requires the game to appear somewhere this contract does not name (report where before adding it).
- The hub cannot show its boards without editing shared code.
- check-leaderboard-coverage.js needs more than the NOT_ON_HUB removal and a stage-board entry.
- The change would touch a file outside: the game page (step 1 only), index.html, sitemap.xml, spec-map/index.html, leaderboards/index.html, scripts/check-leaderboard-coverage.js, scripts/audit-register.py, scripts/check-theme.py, the roster, updates/index.html, docs/todo.md, docs/history/todo-done.md, docs/handover/cloud.md and its archive, and the contract files.
- merge-pr.py refuses for a reason other than a transient 5xx it already retries.
