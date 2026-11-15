# ANSWER-LOCK-FLAKE (contract, verbatim)

Received by Claude Code 15 Nov 2026, from Jon's paste, in a cloud session (the contract's lane is home).

```text
ANSWER-LOCK-FLAKE (Project Claude, drafted Sat 14 Nov 2026 22:45; reissued Sun 15 Nov 08:55 with PR 1 added; Jon 14 Nov 22:38 "after please"; Jon 15 Nov 08:37 and 08:51)
Recommended: Opus, effort high: PR 2 is a diagnosis in shared test infrastructure and its fix must address the cause, not retry around it; PR 1 is small.
LANE: home. TIER: Medium (merge on green; Project Claude reviews after each merge). START: now. UGH-STATS-HOME's close-out is on main (#772, 8547a16), so there is none to carry. Two PRs, in this order, each merged before the next is opened; each branched from current origin/main.
MERGE: merge-pr.py on a green Gate.

JON'S RULINGS (verbatim in the PR bodies):
- 14 Nov 22:38: "after please" (to: this flake work follows UGH-STATS-HOME). Standing from the 14 Nov handover: a third answer-lock flake gets its own contract.
- 15 Nov 08:37: "I have all the images saved on the computer as well as on chatgpt" (to: are the original PNGs on art/answer-box-redraws kept anywhere else? The WebP versions on main are enough, so the branch can go).
- 15 Nov 08:51: "remove the badge entirely please" (to: the "Built to be safe for school networks" header badge, which, with the new "Ugh, stats" badge, pushed the header from 240 to 282 px at 1280 and 1366 px wide; with it removed, the header is 240 px at both, as before #771).

TASK: PR 1: remove the "Built to be safe for school networks" header badge and delete the leftover branch art/answer-box-redraws. PR 2: find why the answer-lock check fails on unchanged code and fix that cause.

ROOT CAUSE:
- PR 1, header: #771 added an "Ugh, stats" badge to .header-badges (index.html). At 1280 and 1366 px it wraps alone onto a second row, making the header 282 px, against 240 px before (measured by Project Claude on 15 Nov, 1366 × 768 being the usual school laptop). Removing the "Built to be safe for school networks" badge (index.html:788-791) returns it to one row, 240 px, at both widths (measured).
- PR 1, branch: art/answer-box-redraws (799748c, "Add files via upload") holds only art-incoming/prom-11-router-dial.png and art-incoming/rfi-10-plans-keypad.png. #769 (c0cec86) landed their WebP conversions under tools/pack-generator/rooms/*/art/. The PNGs are not on main, by the repo's practice (main keeps no art-incoming/ folder); Jon holds the originals.
- PR 2: not yet known; finding it is part 1 of PR 2. Recorded instances: (a) main run 43590939932 on 6f37c69 (#760): red only in Answer lock L7, trig-identity-duel, "Page.goto: Timeout 20000ms exceeded" loading the page from the runner's own server; rerun green. (b) #765 and (c) #768 (14 Nov): failed in the local parallel check-changed run, passed alone (see each PR body). Older: home archive 14 Oct, "MaffsLock undefined" at start in parts 1, 5 and 6 under load. Leads to test, not conclusions: check-answer-lock.py:686 waits for 'load' with a 20 s timeout, while its route (:675) lets /katex@ requests through to the network, so a slow CDN delays 'load'; the stub server is bank_common.start_stub_server (:130), shared by many checks; 192 scripts use wait_until='load' and 38 let katex@ through. (Not this flake: #771's first Gate failed pulling the Playwright image from mcr.microsoft.com before any test ran.)

CLASS CHECK:
- PR 1: local. One badge in one page; one leftover branch. The badge wording stays elsewhere (op/index.html:485, the privacy page's descriptions): those are sentences, not the badge row, and are unchanged.
- PR 2: probably a class. If the cause is in the page-loading or serving pattern (the stub server, the route, what 'load' waits for), it sits in shared infrastructure or a pattern repeated across checks, and the fix goes there: in bank_common / browser_check or one shared helper the affected checks call, not in check-answer-lock.py alone. If the diagnosis shows the cause is specific to the answer-lock check (its own timing, a MaffsLock start-up race in its driver), say why it is local and fix it locally.

EXACT CHANGE:
PR 1:
 1. index.html: remove the <span class="badge"> holding "Built to be safe for school networks" (:788-791). No other badge, style or order changes.
 2. Measure the header at 1280 × 800, 1366 × 768 and 1440 × 900 before and after; after, the badges are on one row and the header is no taller than before #771 (240 px at 1366, per Project Claude's measure) at all three. Report the figures in the PR body.
 3. Delete the remote branch: git push origin --delete art/answer-box-redraws. Before deleting, confirm its only commit is 799748c and it changes only the two PNGs named above; report that in the PR body.
 4. docs/todo.md row ANSWER-BOX-REDRAWS-BRANCH closed with Jon's 15 Nov 08:37 ruling. home.md entry. No /updates/ line.
PR 2:
 5. Diagnose. Reproduce: run the answer-lock check in parallel under load the way check-changed does, enough times to see the failure (state the count and the failure rate); capture for each failure the game, step, error text and what the page had or had not loaded (network log for katex@, timing of MaffsLock's definition). Pull the logs of run 43590939932's L7 job. Name the cause with that evidence. Report it in the PR body before the fix.
 6. Fix the cause at the layer the CLASS CHECK puts it. Show it: the same load test, the same count, zero failures after; and, if the fix is shared, that every check using the changed helper still passes.
 7. A planted fault in the relevant --selftest that recreates the cause (for example a delayed KaTeX response, or a delayed answer-lock.js) and shows the fixed check handles it, while a game that really fails still fails.
 8. home.md entry; todo row closed if one exists; the 14 Nov flake notes in docs/handover/cloud.md left as they are.
DO NOT TOUCH: every header badge other than the one in EXACT CHANGE 1; op/index.html and the privacy page; the "Ugh, stats" badge, linked total and Statistics card from #771; every remote branch other than art/answer-box-redraws; the games and their pages; schools/assets/ (answer-lock.js included); what the answer-lock check judges (its points, NOT_YET, GATE_EXCLUDED, answer-lock-state.json); CI timeouts and the group packing; docs/handover/cloud.md; Gate files.
SUCCESS CONDITION: PR 1: the header is on one row at 1280, 1366 and 1440 and no taller than before #771; art/answer-box-redraws is gone; todo row closed; merged on green; main's check-site and phone-fit-full green on its merge commit and reported. PR 2: cause named with evidence; fix at the layer the evidence points to; the load test fails before the fix and passes after at the same count; selftest plant caught; every check using any changed shared code passes; merged on green; main's check-site and phone-fit-full green on its merge commit and reported. home.md updated for both.
STOP IF: removing the badge does not bring the header back to one row at 1366 (report the widths; do not change other badges); the branch holds anything other than the two PNGs, or the delete is refused; the flake cannot be reproduced in a reasonable number of runs (report what was tried and the counts); the only fix found is a retry, a longer timeout or a skip, which hide the cause rather than fix it; the fix would change what the answer-lock check judges or loosen any check; the cause turns out to be in a game page or a shared site asset rather than the test infrastructure.
```
