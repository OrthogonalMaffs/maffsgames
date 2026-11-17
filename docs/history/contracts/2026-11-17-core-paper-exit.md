LANE: cloud (Claude Code on the web), a NEW session. SEND: now. It WAITS (step W below) until ANSWER-BOX-TEXT, running in another session, has fully merged; it makes no branch or edit before then. Researched on main ea7bcaa (17 Nov 14:55).
RECOMMENDED: Opus 5.5, high effort. It changes a shared asset used by 11 games and must leave them byte-for-byte in behaviour.

TASK: CORE-PAPER-EXIT. Give the four Core Maths papers (core-maths-paper1, -paper2a, -paper2b, -paper2c) an in-paper "← Exit paper" control back to the paper's start screen, by widening the shared stage-exit shell so any multi-question game can use it. List every other game with the same gap.

ROOT CAUSE: During a paper the only control is the page's back link, games/core-maths-paper1/index.html:169 <a href="../../" class="back-link">MaffsGames</a> (2a :130, 2b :130, 2c :141). It goes to the homepage, never back to the paper's start, and these are the only 4 game pages whose back link reads "MaffsGames" (70 read "← Back to Games"). The shared shell that gives stage games a way out, schools/assets/stage-exit.js, cannot be used here because it is wired to one layout: it needs a #game screen with a .hud row, and leaves by clicking #menuBtn or #againBtn (stage-exit.js header comment, leave()); stage-exit.css hides its row with body:has(#game.active) and shows its button only on #example.active. The papers use #gameScreen, have no .hud, and restart with restartGame() / showScreen('startScreen').

CLASS CHECK: A class, in shared infrastructure. The missing way back to a game's own start is the same shape in all four papers (copies of one design) and possibly in other multi-question games, and the one shared mechanism for it is hard-wired to stage games. So the fix goes into stage-exit.js/.css as page-declared options, with today's behaviour as the default; the papers then opt in. A per-paper hand-made button would be the call-site patch.

JON'S DECISIONS (17 Nov 2026; verbatim in the PR body):
- Jon raised the missing exit on 17 Nov at 11:55.
- 14:55: leaving needs a SECOND TAP: the first tap turns the button into "Tap again to exit" for 3 seconds (no pop-up dialog); a second tap within 3 seconds leaves; otherwise it reverts.
- 14:55: other games with the gap are LISTED ONLY, in docs/todo.md, for Jon to decide.
- 14:55: the label is "← Exit paper".
- 14:54: sent to a new session that waits for the current run to close.

EXACT CHANGE:
W. WAIT. Another cloud session is running ANSWER-BOX-TEXT as two PRs (#814, then a PR 2 for estimation-golf and glorious-gantt). Every 10 minutes, fetch origin and list open PRs. Proceed only when BOTH are true:
   - origin/main contains the merge of ANSWER-BOX-TEXT PR 2 (a merged PR whose title starts "ANSWER-BOX-TEXT" and covers estimation-golf/glorious-gantt);
   - no open PR's title starts "ANSWER-BOX-TEXT".
   Then branch from that main and re-check every file:line in this contract against it.
0. First commit: close-outs per AGENTS.md for ANSWER-BOX-TEXT PR 1 and PR 2 (and any earlier one not on main): merge commits, merge-pr.py's last line where the other session recorded it, and main's check-site and phone-fit-full run IDs read from GitHub Actions for each merge commit.
1. schools/assets/stage-exit.js and stage-exit.css: page-declared options on the script tag, every default equal to today's behaviour:
   - data-game: selector of the in-play screen (default "#game").
   - data-leave: name of a global function to call to leave (default: click #menuBtn or #againBtn, as now).
   - data-confirm="second-tap": the two-tap rule above (default: none, as now). The 3-second window and the revert are in the shell, not the page. Clear any pending MaffsNext first, as leave() does now.
   - With no .hud inside the in-play screen, the exit row (button + home link) stays visible while that screen is active, in the place the page's back link already occupies (no extra height). It is hidden on every other screen except the home link.
   - Leaving never fires game_completed, submits to a board or records a score (unchanged rule).
   - Update the header comment: what a page must provide, now and with options.
2. The four papers include stage-exit.js/.css with data-game="#gameScreen", data-leave naming a function that returns to the start screen (showScreen('startScreen') and nothing else that records), data-confirm="second-tap", data-label="← Exit paper". The home link reads "← Games" (the shell's default data-home-label). Starting the paper again must start a fresh run (startGame already resets).
3. scripts/verify-stage-exit.py: add the four papers to ci-deps and tests:
   - The exit shows during play and on the section banner, not on the start or results screens.
   - One tap shows "Tap again to exit" and does not leave; it reverts after 3 s; two taps within 3 s land on the start screen.
   - Leaving records nothing (no game_completed, no leaderboard submit, no score history).
   - Begin Practice after leaving starts at question 1 with a score of 0.
   - Every existing test for the 11 stage games passes unchanged.
   Plants that must fail: a single tap leaves a paper; leaving fires game_completed; the row hidden during play; a stage game's default changed (e.g. the row visible during #game).
4. Survey: list every game page whose run has more than one question and which has no control during play that returns to the game's own start (only a homepage link, or nothing). Method and evidence in the PR body. Add docs/todo.md row IN-PLAY-EXIT-GAP listing the slugs, for Jon. Do not change those games.
5. /updates/ line in the site's plain wording, e.g. "Core Maths papers now have an Exit paper button (tap twice) that takes you back to the start."
6. docs/handover/cloud.md entry.
7. Dispatch phone-fit-full on the branch (PRs do not run it). Merge with scripts/merge-pr.py when the Gate and that run are green.

DO NOT TOUCH:
- Anything at all before step W is satisfied: no branch, commit or PR.
- The papers' questions, answers, marking, scoring, leaderboard and analytics calls, and their results screens (including "Back to Portal").
- The 11 games already using stage-exit.js: no edits to their pages.
- Any game in the survey list.
- canon (home lane).
- No draft PR.

SUCCESS CONDITION:
- On a phone and a laptop, each of the four papers shows "← Exit paper" and "← Games" during play; two taps return to the paper's start, one tap does not; nothing is recorded.
- The 11 stage games behave exactly as before (verify-stage-exit.py's existing tests unchanged and passing).
- Plants fail; phone-fit-full and check-site green.
- The todo row lists the other games with the gap.
- Merged by merge-pr.py, reported with its last line, the merge commit and main's check-site and phone-fit-full run IDs. Handover committed.

STOP IF:
- Step W is not satisfied within 4 hours of starting (report what main and the open PRs show).
- ANSWER-BOX-TEXT's merges changed any file:line this contract relies on in a way that changes the plan.
- Any of the 11 stage games would change behaviour or layout to support the options.
- A paper cannot return to its start without touching its scoring or analytics code.
- The row during play pushes the first answer option below the fold at 375 × 667 where it was above before (report both measurements).
- merge-pr.py refuses for a reason other than a transient 5xx it already retries.

---

Amendment 1 (Jon, 17 Nov 2026, 15:18 UTC, in session, verbatim):

Thank you. Shared tier, as you said: Project Claude's contract omitted the tier (AGENTS.md:8), and a change to stage-exit.js/.css, loaded by 11 games, is Shared under docs/agent-workflow.md §2. So step 7 is replaced: when the Gate and phone-fit-full on the branch are green, STOP with "Ready for architect review", report the PR number, both run IDs and the fold measurements (each paper's screen top ≤ 47 px at 375 × 667; first option above the fold on at least 36/36, 35/36, 36/36, 36/36), and do NOT merge. Project Claude reviews; Jon then says "merge", and you merge with scripts/merge-pr.py.
Your MaffsLock.clearTimers() addition before showScreen('startScreen') is approved: record it in the PR body as found by you, outside the contract.
The survey stands as reported (89 pages, exclusions with reasons) in the todo row IN-PLAY-EXIT-GAP, listed only.
