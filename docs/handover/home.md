# Handover: home lane

**Queue (cross-lane facts; never archived)**

- UPDATES-NOVEMBER: home/Codex, codex/updates-november, /home/maffs/mg-updates-november; contract docs/handover/contracts/2026-11-03-updates-november.md (Amendment 1). Claims updates/index.html, index.html and AGENTS.md; Small, merge on green.

- NEW-AND-UPDATED: home/Codex claims index.html on codex/new-and-updated, /home/maffs/mg-new-and-updated, PR #648; contract docs/handover/contracts/2026-11-03-new-and-updated.md. Full checks 56/56, exit 0. Shared: green Gate then Project Claude review and Jon's merge. Fresh base ffcd9a9b includes DASH-MINUS #646; verifier Amendment 1 applied.

- TODO-TRIM: home/Codex, codex/todo-trim, /home/maffs/mg-todo-trim, PR #645; contract and Jon's 3 Nov HTTP-503 retry ruling in the PR. Small, merge on green. NEW-AND-UPDATED is next; no saved contract found at this head.

- PIES-SIGNOFF-AND-PRIMARY-FF: home/Codex, codex/pies-signoff, /home/maffs/mg-pies-signoff; contract `docs/handover/contracts/2026-11-03-pies-signoff-and-primary-ff.md`. Small, merge on green; TODO-TRIM starts after completion.

- LOOK-STAGE: home/Codex, codex/look-stage, /home/maffs/mg-look-stage, PR #638; contract `docs/handover/contracts/2026-11-02-look-stage.md`. Concurrent PIES-LOOK/ESSENTIALS-ART authorised by Jon; roster, canon and registration reserved here. Pies remains warned until Jon's explicit look sign-off, irrespective of its artwork merge. Shared: stop at green Gate for Project Claude review and Jon's “merge”.
- RULEBOOK: home/Codex, codex/rulebook, /home/maffs/mg-rulebook, PR #635; Shared. Amendment 1 findings addressed on the same branch; stop at Gate green for re-review and Jon's “merge”. Two lanes are explicitly authorised for this task.
- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

## 2026-11-03 (home): UPDATES-NOVEMBER

Agent: Codex. Worktree: /home/maffs/mg-updates-november. Branch: codex/updates-november. Base: 9e17ddfc; implementation f1d26d4f. Checked locally. Next: PR, guarded merge and main watch. November uses Jon's approved wording and existing markup; The 6 P's gains its 27 Oct New badge; AGENTS.md requires dated updates in visible-change PRs, with rationale in canon §12. No checker or game changes. Initial STOP for missing dash exception mechanism resolved by Amendment 1: updates/ is outside that check's scope. Open PRs #518 and #424 touch home.md only. No SR decision needed; SR-27 does not apply. Contract and amendment saved verbatim.

Full check-changed.py: 56/56 passed in 638s (12 heavy serial, 44 light), summary "All selected checks passed. Push, and CI runs the rest." Log .claude/bg-1793721466846.log; detached launcher did not retain the exit status. Seven standard CI deferrals: four page-load shards (first also hang scan), bank extraction, ledger lint and leaderboard coverage. Dash-minus selftest 31/31; check 0 hits across 134 files, exit 0. New-and-updated passes in the full run; independent metadata assertion confirms I Found a Mark, Pies, The 6 P's first to third. November game links and UTF-8 punctuation verified; October and earlier byte-identical; git diff --check clean. No answer-bearing change.

Record: agent Codex; wall n/a; review cycles 0; amendments 1; usage n/a.

## 2026-11-03 (home): NEW-AND-UPDATED

Agent: Codex. Worktree: /home/maffs/mg-new-and-updated. Branch: codex/new-and-updated. Base ffcd9a9b includes DASH-MINUS #646; claim commit 75dcee63; implementation 6ae4421e; amendment b995f2d9; checks e205418b; previous STOP record a21f0f3c. PR #648: https://github.com/OrthogonalMaffs/maffsgames/pull/648 . Checked locally and pushed. Next: this handover head's Gate, then stop for Project Claude review and Jon's merge. Current-head Gate and review hand-off are tracked in the PR report. No merge or cleanup authorised.

Implemented: cmpNew derives its cards from applyBadges(), one per slug, newest first with New then title ties, cap 12; evergreen heading/note and new-and-updated analytics label. Badge dates/rules, level cards, filter and compact behaviour unchanged. New ci-line verifier reads level-card metadata independently and stubs the clock only in routed copies. Section-click test also fixes its test clock so generated cards remain testable after the current badges expire.

Targeted checks: new verifier passes on 3 Nov (14 live, 12 displayed), 13 Nov (13 live) and 2030 (none, whole section hidden). All three required plants CAUGHT. Phones 320x568, 375x667, 390x844 pass compact controls, live/filtered counts and overflow checks using pinned real fonts. Section clicks pass for all 20 labelled elements; copied cards still fire game_card_clicked alone. First verifier run read the CSS-uppercased heading via inner_text; corrected to text_content, then all pass. UTF-8 characters verified. No answer-bearing change; no SR decision needed; SR-27 exemption does not apply.

Full check-changed.py selected 56 checks (12 serial heavy, 44 light), seven standard CI deferrals. At STOP: 44 passed, one failed, 11 unfinished. The failing Circle Theorem Spotter verifier's check_copies() at line 513 hard-codes portal card count 2; the removed hand card leaves its canonical GCSE card alone. Game and level card are unchanged. This is understood but its fix is outside EXACT CHANGE; no verifier/game/Gate file changed. Registered runner PID 320924 stopped through end-task.py's stop_registered(), so the overall check has no final exit status. Log .claude/bg-1793715256421.log retained; new verifier and section clicks both passed within this run too. Branch remains local; no push, PR, merge or cleanup.

Resumed under Jon's 3 Nov verifier Amendment 1 (saved verbatim beside the earlier wait ruling): only check_copies()'s condition changes to require at least one portal card. Reason: the second card was the removed hand copy; load-built cards have no stable static count. Every card must still match CARD and none may say seven. Direct verifier PASS: 55 questions, 44 calculation questions independently solved, 10 tangent figures, all 15 plants caught. Ad hoc probes: zero cards rejected; one and three exact copies accepted; wrong second copy and seven rejected. One-line-only diff confirmed.

Complete check-changed.py after amendment: 56/56 passed in 631s, exit 0, 12 heavy serial and 44 light; seven standard CI deferrals listed above. Summary: "All selected checks passed. Push, and CI runs the rest." Log .claude/bg-1793716436188.log, including CHECK_CHANGED_EXIT_STATUS=0. No Gate files changed; original badge/filter/compact implementation and level cards byte-identical to base outside the scoped builder.

Record: agent Codex; wall n/a (initial contract-receipt timestamp unavailable); review cycles 0; amendments 2 (wait ruling and verifier Amendment 1); usage n/a.

## 2026-11-03 (home): TODO-TRIM

Agent: Codex. Worktree: /home/maffs/mg-todo-trim. Branch: codex/todo-trim. Last implementation commit: 359cb347. PR #645: https://github.com/OrthogonalMaffs/maffsgames/pull/645 . Checked locally; Gate and measured-budget check passed on 359cb347. Next: this handover head's Gate, then retry the guarded merge with --watch --wait 3600. Final merge/main/cleanup results are tracked in the PR report.

Moved 40 clearly finished blocks (32,248 bytes) verbatim into docs/history/todo-archive.md under 2026-11-03; todo.md is 118,818 bytes. Verification proves every removed block archived and all retained lines, including START and open items, byte-identical. Mixed-status entries stay intact; judgement calls and reproducible proof are in the PR. Current item formats need consistent boundaries and terminal status before safe automatic archiving. No automation changed. Full check-changed.py: 41/41 in 251s, exit 0; seven standard CI deferrals. Context-size and UTF-8 checks passed. No answer-bearing change; no SR decision needed.

503/retry: first merge helper refused on GitHub HTTP 503, exit 1; Jon's 3 Nov ruling authorises retry after the full Gate, then only if another 503 a five-minute wait and one final attempt. This handover update is explicitly authorised by that ruling; retry outcome goes in the PR report.

Record: agent Codex; wall n/a (contract-receipt timestamp unavailable; no estimate); review cycles 0; amendments 1; usage n/a.

## 2026-11-03 (home): PIES-SIGNOFF-AND-PRIMARY-FF

Agent: Codex. Worktree: /home/maffs/mg-pies-signoff. Branch: codex/pies-signoff. Base: 560b6b17. Implementation: 494f7055; check report: c104cd86. PR #644: https://github.com/OrthogonalMaffs/maffsgames/pull/644 . Checked locally; next: green Gate, guarded merge and main watch; Small, no review hold. Final merge/main/cleanup results are in the PR report.

Recorded Jon's 3 Nov look approval for Pies and emptied the warning list. Primary fast-forward is the first startup command; AGENTS.md's short rule points to canon §12 for the stale-rulebook history. Other roster rows, game files and CLOUD-LEAN rules unchanged.

Slip: relative roster patch landed in primary; stopped, then Jon's 3 Nov recovery moved only that sign-off to this worktree, passed the checker and restored a clean primary.

Look sign-off check: 101 listed games, 0 warnings, 0 failures. Context-size check passed. Full check-changed.py: 149/149 in 478s, exit 0 (5 heavy serial, 144 light); 71 indirect heavy roster checks and seven standard checks deferred to CI. Log: .claude/bg-1793708922180.log. No answer-bearing change. No SR decision needed; SR-27 exception does not apply. Contract STOP IF conditions not hit.

Record: agent Codex; wall n/a (contract-receipt timestamp unavailable; no estimate); review cycles 0; amendments 1; usage n/a.

## 2026-11-02 (home): LOOK-STAGE

Agent: Codex. Worktree: /home/maffs/mg-look-stage. Branch: codex/look-stage. Last commit before this report: 8e2cf3ff; implementation: 5e5a9e44; base: b5c9eaa6. PR #638: https://github.com/OrthogonalMaffs/maffsgames/pull/638 . Current-head Gate and review state are tracked in the PR report. Next: stop at green Gate for Project Claude Shared review and Jon's explicit “merge”. No merge authorised.

Shared listing gap fixed in the roster Description and a new CI-header-registered checker; no existing columns or listing states changed. All 100 eligible listed games record Jon's retrospective approval; Pies alone warns. Shrink-only JSON list rejects additions, restoration after removal and stale entries. Canon §7.8 records the listing/art rule; §12 explains the pipeline failure. No game files, Gate files or answer-lock state changed. SR-21 applied (listing state retained); SR-27 does not exempt this shared check from check-changed.py.

Initial local run exposed a sign-off word-boundary bug and an incorrect expected warning in one selftest; one within-scope fix corrected both. Re-run: 7/7 selftests pass; 101 listed games, 1 warning, 0 failures. CI packing check passes; new line uses the standard untimed warning. Full check-changed: 152/152 passed in 515s (5 heavy serial, 147 light); standard seven checks and indirect heavy roster dependencies deferred to CI. Completion summary retained in `.claude/bg-1793654249945.log`; detached launcher's child exit status was not retained. UTF-8 characters and exact row preservation after removing the 100 new approval suffixes checked. An ad hoc import probe initially omitted scripts/ from sys.path; corrected probe passes, no repository change.

CI run 41528624872: the new check's seven plants passed, but content job 37 failed because its shallow checkout lacked the event's base commit. Within-scope fix fetches that exact base only when absent. Added a real shallow-clone selftest with a local file remote; the missing base is fetched and its older warning list read correctly. Direct selftest 8/8 and roster check (101 listed, one warning, zero failures) pass. Correction-file check-changed run: 41/42 pass in 251s, exit 1; Text writes alone caught three new fixture writes without newline=''. First fix for that check adds newline='' to all three; Text writes selftest/check and look selftest/check pass. Subsequent local run and CI are recorded in the PR report. No check has failed after two fixes for that check. No Gate file changes needed.

After newline correction, check-changed.py --files scripts/check-look-signoff.py docs/handover/home.md passes 42/42 in 251s, captured exit 0 (log `.claude/bg-1793655775463.log`); seven standard CI deferrals. Original complete run remains 152/152. No game files or Gate files changed during corrections.

First review hand-off: PR opened 2 Nov at 21:27 UTC; wall measured from contract/startup at 21:15 UTC.

Record: agent Codex; wall 0:12; review cycles 0; amendments 0; usage n/a.

## 2026-11-02 (home): RULEBOOK (Shared; Codex)

Agent: Codex. Worktree: /home/maffs/mg-rulebook. Branch: codex/rulebook. Last commit before this report update: dd370c69bd528bf71e91c58d8925dedd18bea9a8. PR #635: https://github.com/OrthogonalMaffs/maffsgames/pull/635 . Next: verify the amendment head's Gate, then stop for Project Claude re-review and Jon's explicit “merge”.

AGENTS.md is the common WSL rulebook; CLAUDE.md imports it with the documented @AGENTS.md form. Local testing, scripts/CI, game claims and room-art rules have explicit topic triggers. Seven previous home entries now use dated level-two headings; text outside those opening lines is unchanged. Windows procedures are historical material in canon §12. Amendment 1 moves cross-lane facts into this handover's Queue preamble and deletes the temporary machine-local notes file; platform-principle bullets are copied verbatim from the unchanged planner brief into AGENTS.md. Task-specific concurrency text is removed from that rulebook.

Rulings: understood failures caused by this change get at most two within-scope fixes; all other unexpected events stop. Answer-lock exempt() requires both a claim and roster-Unlisted status. Cloud handover's missing Unlisted qualification is flagged for cloud; that file remains untouched. Lane notes were waived for startup and replaced in WSL. No merge or cleanup authorised yet.

Validation after Amendment 1: duplicate sentences 0; platform-principle bullets verbatim; Queue in the unarchived preamble; temporary notes file absent; seven old entries (eight with RULEBOOK), with every byte outside converted opening lines unchanged. Context-size check/selftest pass. AGENTS.md 10,100 bytes, CLAUDE.md 628; combined 10,728. Initial complete check-changed: 41/41 in 253s, seven standard CI deferrals. Repeated fresh codex exec at /home/maffs/mg-rulebook-load-test-r1 (dd370c69) quoted takeover exactly with zero tools. First load-test worktree also retained. Initial full-record size assertion required two within-scope shortening fixes; all ad hoc checks now pass. Previous Gate: 84/84 on 8e4fcf21, run 41516051138; it does not verify this amendment. First review hand-off 2026-11-02 20:16:23 UTC; contract received 19:36:38. Record wall measures that first hand-off; review cycles now 1, amendments/rulings 4. Current Gate is tracked in the PR report; no merge or cleanup run.

Record: agent Codex; wall 0:39; review cycles 1; amendments 4; usage n/a.

