DOCS-BUNDLE (Project Claude, 9 Nov 19:10)
LANE: home (Claude Code) · TIER: Docs · CONTRACT: DOCS-BUNDLE · new worktree from origin/main b328883b or later (branch claude/docs-bundle). No other lane is running. Stop at a green Gate for Project Claude's review and Jon's "merge"; do not merge. Not a draft. Save this contract verbatim in docs/handover/contracts/ in the first commit; in the same commit git mv docs/handover/contracts/2026-11-09-money-input.md to docs/history/contracts/ (#719 merged as b328883b).

TASK: Put today's findings and Jon's requests into the backlog, reconcile one rule file with AGENTS.md, survey the check ledger's known failures, and count Jon's own leaderboard entries (read only).
ROOT CAUSE: Findings and rulings from 9 Nov exist only in chat and the project handover; the check ledger holds 167 known failures that the backlog does not name (it is a second backlog); docs/rules/games.md still forbids what AGENTS.md now requires.
CLASS CHECK: Shared process documents and one shared data file, fixed once. The ledger survey closes the "second backlog" class: every ledgered failure gets a pointer from docs/todo.md, so none is invisible again.
EXACT CHANGE:
1. docs/rules/games.md: amend line 3 ("Per-game fixes do not edit docs/todo.md") and the one-game-per-PR / one-claim-at-a-time line so they agree with AGENTS.md (a PR that fixes a todo row updates it in the same PR; one lane at a time, so a cloud PR may fix more than one small game when its contract says so). Quote both old and new lines in the PR body. No other rule line changes; if another line conflicts, report it, do not edit it.
2. Ledger survey (read only on data/check-ledger.json): docs/audits/ledger-debt-2026-11.md — every rule with status fail, per game: rule, game, count, what the rule checks (one line), one example entry. Then one docs/todo.md row per game-and-rule group (or per rule where it is one fix across games), owner cloud, with the count and a pointer to the survey file. Totals in the PR body (expected about 167 entries in 43 games: B4 96, B7 44, B6 18, B3 8, B2 1; report the real numbers).
3. New docs/todo.md rows (append-only rule; owner and date on each):
   - BOOLEAN-BLITZ-LENGTH (Jon 9 Nov): start-screen choice of 10 / 20 / all 42; one leaderboard per length (SR-22); cloud; after the live-bug fixes.
   - CLAIM-WALKTHROUGH (Jon 9 Nov): test-the-claim — optional, very clearly shown "Watch one first" worked example per mode (one idea per screen, student's Next, unscored); step feedback naming the actual mistake; "Show me" after two wrong tries; Project Claude writes the scripts for Jon's approval before the build.
   - FORGE-SUBJECT-PROMPT (Jon 9 Nov): formula-forge — the subject letter in "Make … the subject" much more prominent; start-screen line "Powers and Multi: have paper handy".
   - PP-AA-OVERFLOW: probability-pioneer scrolls sideways in Aa mode (its probability-scale labels).
   - GD-MONEY-INPUT: growth-and-decay's answers in pounds are type="number" (a typed £ empties the box); it marks to s.f., so the fix includes its own marker accepting a leading £; moneyInput() for the box.
   - PHONE-FIT-CHECKER: measure-phone-fit.py (a) settle() 5 s ceiling false-passes controls shown at ~5 s (screening-room); (b) one seeded question per game, against canon §7.6.1's "every question shape"; (c) --aa never switches Aa on in games reading a non-standard saved setting (probability-pioneer, shape-shifter, like-terms-collector); (d) three verdicts on the same code (717 FAIL, "no Next", PASS); audit every entry #707 removed as "stale". Home lane, own contract.
   - PHONE-FIT-PR-COVERAGE: only the nightly full run measures laptop mode; a push touching one game's page skips the full measure.
   - LEDGER-LINE-DRIFT: ledger `line` fields go stale on every game edit; stop recording or comparing them.
   - FAKE-BAG (idea, Jon 9 Nov): "Is That a Fake Bag?" ("a sim tote…" = asymptote) reserved for a future graph-sketching / asymptotes game.
4. Appended notes (never reword a row): LOCAL-CHECKS — "9 Nov: verifiers of squared-squirrel, its-on-sale, estimation-engine, the-6-ps and the Burst, Chart drawings and two Feedback-that-teaches checks fail locally on clean main; pass in CI (#719)." Row 1.36 — "9 Nov: the shared helper exists (answer.js MaffsAnswer.money, moneyInput #719); the 'no shared helper' wording above is historical. Remaining: a check for money keys stored or shown at 1 d.p.; GD-MONEY-INPUT."
5. Jon's leaderboard entries, READ ONLY: a one-off script (scripts/list-initials.mjs, node, no dependencies, public REST reads of the Firebase Realtime Database at the databaseURL in schools/assets/firebase-leaderboard.js; no key, writes nothing) that reads recent_scores whole and every leaderboards/<board> whose name it can derive from the games' declared levels, and lists every entry with initials JLF or SSF: board or feed, game, level, score, date, push id. Put the counts and the table in the PR body (not in the repo: it names Jon's initials, which are his, but the table is a working list). The script may be committed (it prints, never writes); if reading any board fails, list which.
6. docs/handover/home.md close-out entry.
DO NOT TOUCH: any game, shared asset, workflow, Gate file or verifier; canon; AGENTS.md; data/check-ledger.json (read only); the existing text of any todo row; Firebase (no writes, no deletes, no key); branches; cloud.md.
SUCCESS CONDITION: games.md agrees with AGENTS.md (old and new lines quoted); the ledger survey file exists with real totals and every failing rule-and-game group has a todo row; the nine new rows and two appended notes are in; the JLF/SSF table is in the PR body; Gate green; stopped for review.
STOP IF: another rule line conflicts with AGENTS.md (report it); the survey finds a ledgered failure that is a wrong answer or wrong maths a student can see today (put it at the top of the PR body as LIVE WRONG ANSWERS and stop for review before adding rows); any Firebase read needs a key or a rules change; a file-size check fails (report file and size).

---

DOCS-BUNDLE — Amendment 1 (Project Claude, 9 Nov 19:14). LANE: home. Jon confirmed both rulings at 19:12.
1. canon §0.3 Standing rulings: add SR-31 and SR-32, in the table's existing format, then remove the contract exclusion "canon" from DO NOT TOUCH for this section only:
   SR-31 Standing rules for STOP IFs (Jon, 27 Oct 2026): copy the ruling word for word from docs/handover/contracts/2026-10-27-standing-stop-rules.md; then git mv that file to docs/history/contracts/ and close the STANDING-STOP-RULES todo row.
   SR-32 Same-day fix of a CRITICAL level (Jon, 13 Oct 2026; confirmed 9 Nov): "A CRITICAL level whose fix a standing ruling already decides is fixed the same day in its own PR, without unlisting, and reported to Jon after; stop and ask only for a new stem, context or convention, or if it cannot merge the same day. An exception to SR-20." Add to SR-20's row: "Exception: SR-32."
2. cloud.md: the SWEEP-1 block's "SR-30" label → "SR-32 (recorded in canon §0.3, 9 Nov)"; change nothing else there. Close the SR-NUMBERING todo row.
3. Check-context-size must still pass (canon and AGENTS.md sizes); if a size check fails, STOP and report.
Nothing else changes.

---

DOCS-BUNDLE — Amendment 2 (Project Claude, 9 Nov 19:23). LANE: home. Same branch claude/docs-bundle.
1. docs/rules/games.md line 13: keep the first sentence (Gemini's unagreed suggestions in docs/idea-backlog-2026-08.md; nothing scheduled) unchanged. Replace the second sentence with: "Jon's first-hand findings become docs/todo.md rows (owner and date); docs/jon-playtest-2026-08.md is a historical log, not a backlog (Jon, 7 Nov 2026: one backlog)." Quote old and new in the PR body.
2. docs/jon-playtest-2026-08.md: list every item in it that is still open (asks for action, a replay, a ruling or a fix, and is not marked done/closed/fixed). For each, add a docs/todo.md row (owner, date, a pointer to its heading in that file) unless an open row already covers it (then append a pointer to that row). Do not edit the playtest file except one line at its top: "Historical log from 9 Nov 2026; open items are docs/todo.md rows (DOCS-BUNDLE)." Report the list in the PR body.
3. If an open item is a wrong answer a student can see today, the existing STOP IF applies (top of the PR body as LIVE WRONG ANSWERS, stop for review).
Line 5 (one claim at a time) is in scope as you planned. Nothing else changes; Amendment 1 still applies.
