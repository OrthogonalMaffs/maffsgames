# Games, claims, findings and listings

Cloud fixes one game per PR, with its verifier and its own `docs/audits/findings/<slug>.yml`; one lane runs at a time, so a cloud PR may fix more than one small game when its contract says so. A PR that fixes all or part of a `docs/todo.md` row updates that row in the same PR (AGENTS.md); no PR edits generated `docs/audits/REGISTER.md`. Main regenerates the register. Home batches relisting under canon SR-21.

Before cloud starts a listed game, it claims it in a separate commit adding it to `scripts/answer-lock-state.json`'s `cloud-remaining` list; a PR whose contract names more than one game claims them all in that commit. Do not claim a game in an open home listing batch; check the handover and PRs first. Remove the claim in its fix PR.

Before a home batch, read the claims on main and drop claimed games; home never claims or edits a game on that list.

`scripts/check-answer-lock.py`'s `exempt()` reports rather than fails only games BOTH claimed and in the roster's Unlisted section. A claimed listed game is judged as if unclaimed: the claim is a process lock only (Jon, 8 Oct; confirmed 2 Nov 2026).

Read the roster for game coverage; the help, timer and analytics files are selected by AGENTS.md's trigger table. Canon §7.6 covers MaffsLock, including each game's own lock-hint declaration.

Improvement sources stay separate: `docs/idea-backlog-2026-08.md` holds Gemini's unagreed suggestions, cross-referenced against roster and Dashboard; nothing is scheduled. Jon's first-hand findings become docs/todo.md rows (owner and date); docs/jon-playtest-2026-08.md is a historical log, not a backlog (Jon, 7 Nov 2026: one backlog).
