# MONOTONIC-CLOCK (contract, verbatim)

Saved word for word from Jon's paste of 15 Nov 2026.

```text
MONOTONIC-CLOCK (Project Claude, Sun 15 Nov 2026 11:10, re-checked against main 595b3af at 12:50; Jon 11:07 "yes please, ... small fixes should be done asap where we can.")
Recommended: Sonnet, effort medium: a few lines in three shared assets, chosen by what each clock reading is for, with tests.
LANE: home (shared assets). TIER: Medium (merge on green; Project Claude reviews after merge). START: now. ANSWER-LOCK-FLAKE's close-out is on main (#779, b4437c8), so there is none to carry. One PR. Branch from current origin/main.
MERGE: merge-pr.py on a green Gate.

JON'S RULING (verbatim in the PR body): 15 Nov 11:07: "yes please, stuff that goes onto the todo list can wait weeks before we get to it, small fixes should be done asap where we can." (to: replace the wall clock with a monotonic clock in the answer lock's timing windows). This is option 1 of todo row ANSWER-LOCK-WALL-CLOCK; option 2 (a monotonic Date.now() in test pages only) is not taken: it hides the dependency instead of removing it.

TASK: Time every short input window in the shared assets with a clock that never jumps (performance.now()), not the wall clock (Date.now()).

ROOT CAUSE: schools/assets/answer-lock.js times its double-tap and fresh-question windows with the wall clock (function now() { return Date.now(); }, :86). WSL's wall clock runs fast and is pulled back about 2.5 s every 30 s, so a step can hold the 300 ms window open for up to 2.9 s and clicks are ignored: 18 of 120 load runs failed, only in rounds containing a clock step (#777's body; todo row ANSWER-LOCK-WALL-CLOCK). A student's device can have its clock corrected mid-game in the same way.

CLASS CHECK: A class: the same wall-clock timing of short input windows appears in three shared assets: answer-lock.js (:86), keypad.js (the 600 ms ghost-click window, :163 and :167) and scroll.js (touch timing, :32 and :59). Fix all three. Not the class, and not changed: Date.now() used as a timestamp or a date (answer-count.js :142 and :241, launch-sash.js :19, firebase-leaderboard.js :468 and :590, progress.js :124, score-history.js :50, ugh-stats.js :109), where wall-clock time is the point.

EXACT CHANGE:
1. answer-lock.js: now() returns performance.now(), falling back to Date.now() only where performance.now is missing. keypad.js and scroll.js: their interval readings likewise; every value compared with one of these readings must come from the same clock (no mixing).
2. Tests: test-answer-lock.py gains a case where Date.now() steps back by 10 s and forward by 10 s mid-window and the lock behaves exactly as without the step; the same for keypad's ghost-click window (scripts/check-keypad.py or its test). A plant that restores Date.now() in answer-lock.js fails the new case.
3. Four scripts stub Date.now(): verify-sequence-solver.py ("Date.now = () => T"), verify-trig-identity-duel.py ("() => realNow() + 60000"), verify-unit-converter.py ("() => dn() + window.__skew") and test-top-scores.py ("() => real() + off"). For each, decide whether it drives one of these windows (then drive performance.now() instead) or a game timer or timestamp (leave it); state the decision and reason for each in the PR body.
4. todo row ANSWER-LOCK-WALL-CLOCK closed with this PR; LOCAL-CHECKS row updated. home.md entry; no /updates/ line (no visible change).
DO NOT TOUCH: every timestamp use listed in CLASS CHECK; the windows' lengths (300 ms, 600 ms and the rest); MaffsLock's API; the games; Gate files; todo row CHECKS-OFFLINE-REST (separate work).
SUCCESS CONDITION: no short input window in a shared asset reads Date.now(); the step tests pass and the plant fails; test-answer-lock.py passes under the parallel load that failed 18 of 120 runs, at the same count (120 runs, 0 failures); every check using these assets passes; Gate green; merged; main's check-site and phone-fit-full green on the merge commit and reported; home.md updated.
STOP IF: a window's behaviour changes when the clock does not step (the windows must behave exactly as now); a reading turns out to be a timestamp that is stored or sent (leave it, report it); a test needs loosening.
```

## Amendment 1 (Jon, 15 Nov 2026, after #781's first Gate failed on "Ugh, stats pages"; verbatim)

```text
Do not change check-ugh-stats.py. The cloud lane's PR #780 (head a65e129) already makes fmt() round halves up, with a self-test plant. Wait for #780 to merge to main. Then bring #781 up to date with main, let the Gate run again, and merge #781 on green as the contract says. Report main's check-site and phone-fit-full on the merge commit, and fill in the merge line in home.md. If #781's Gate is still red on anything other than "Ugh, stats pages" after the update, stop and report.
```
