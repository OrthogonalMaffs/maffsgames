# ANSWER-LOCK-STATIC (Jon, 22 Oct 2026), verbatim

Jon, 22 Oct. This message supersedes my two earlier ones today. The home lane is NOT doing ANSWER-LOCK-STATIC; you are.

ORDER: (1) ANSWER-LOCK-STATIC, its own PR, below. (2) When it is merged and main is green: merge main into claude/brave-allen-reghhq, apply rulings (a)-(d) below, and open the How Many Parts? redesign PR through scripts/merge-pr.py.

LANE EXCEPTION (as DEPS-SRC-HAZARD): you may edit scripts/check-answer-lock.py and canon §7.6.0 for this contract only. Nothing in the home lane touches that file today.

TASK: Move the answer-lock self-test and static rules out of part 1 into their own CI line, so the six play parts carry equal kinds of load and no PR touching a migrated game fails the per-line limit.
ROOT CAUSE: scripts/check-answer-lock.py --part i/n plays every n-th migrated game in slug order, and part 1 alone also runs --selftest and the static rules (NOT_YET, lock hints). Part 1 is therefore always heaviest (median 299 s; parts 2-6: 224, 167, 147, 173, 188 s) and is main's only split candidate (324 s with setup, against a 315 s limit). How Many Parts? (#469) joining the migrated games tipped it over; any PR touching a migrated game now fails --check, because it selects that line for a reason of its own (LINE-LIMIT-SCOPE).
CLASS CHECK: Yes. Shared infrastructure (one verifier's slicing, run by every PR touching any migrated game), and the fault is structural: part 1 carries a fixed load the others don't. A further split of part 1, or a warning for coverage growth, would be the call-site patch.
EXACT CHANGE: scripts/check-answer-lock.py: a new ci-line "Answer lock, static rules and self-test" running --selftest and --static (static rules and the NOT_YET report, no games played); --part i/n plays games only, for every i including 1; report-not-fail rule unchanged. Keep n = 6. Selftest proves: each migrated game is played by exactly one part; the static rules run exactly once across all lines; a static fault still fails. Record the new line in canon §7.6.0 where the parts are described.
DO NOT TOUCH: The answer-lock rules, NOT_YET, scripts/answer-lock-state.json, the play harness, budgets and limit figures, ci-groups.py, ci-deps.py, every game, and the redesign branch until this merges.
SUCCESS CONDITION: --check passes on main with no answer-lock split candidate (from main's run after the merge); the selftest passes; check-changed.py finishes before the first push; merged through scripts/merge-pr.py on a green Gate; main's run green, timings job included, every answer-lock part under 70% of its budget.
STOP IF: Any play part is still over the limit after the move (report each part's time; do not raise n); the static rules depend on state built while playing; or ci-groups.py or the workflow needs changing beyond adding the line.
FINISH: Merged; docs/handover/cloud.md records the entry, PR, main run and each part's time (cloud.md is at its cap: move your oldest finished entries verbatim to docs/history/handover-cloud-archive.md to make room); one line in docs/handover/home.md telling the home lane check-answer-lock.py changed.

RULINGS FOR THE REDESIGN PR (apply after the merge above):
(a) Drop the two stage 6 collision questions (2½ ÷ 1⅔, 2⅔ ÷ 1⅓) from pool f by the build-time filter, as #453 did; the verifier checks zero.
(b) "Subtracted the smaller part from the larger" is about the fractional parts (3¼ − 1¾ → 2½), not the key's size. Report how many pool f subtractions have a first fractional part smaller than the second. If none, pool f lacks the classic borrowing case: say so in the handover for a follow-up; don't add it in this PR.
(c) Update How Many Parts?'s own entry in scripts/survey-key-collisions.py to the new per-stage lists (this game's entry only). It must report 0.
(d) Accepted: the bar drawn after Next in Aa mode on small phones; "Simplest form."; the hidden stage label on short screens; the subtitle "Fractions, one bar of chocolate at a time."
