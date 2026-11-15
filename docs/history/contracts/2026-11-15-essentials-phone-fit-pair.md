ESSENTIALS-PHONE-FIT-PAIR (Project Claude, Sat 14 Nov 2026 23:05, re-checked against main 7aeefcaf at 18:12 on 15 Nov; Jon 22:46 "do them in numerical order please" (this is 2 of 3); lane exception Jon 22:54)
Recommended: Sonnet, effort medium: two games' own layout, traced and fixed, and one line in a shared script.
LANE: cloud, with one explicit exception: this contract may change schools/assets/session-length.js, a home-lane shared asset, in the one place EXACT CHANGE 1 names. TIER: Medium (merge on green; Project Claude reviews after each merge; Jon plays each game after its merge). START: now, fresh session; this task's first commit is PACK-WORDING-1511's close-out (#785 merged as b408cbe; main's check-site 43740131412 and phone-fit-full 43740131422 both success; contract to history) in cloud.md, the standing rule. Two PRs, in this order, each merged before the next is opened; each branched from current origin/main.
MERGE: on a green Gate, by merge-pr.py or, when gh auth fails, the 10 Nov 2026 GitHub-connection route; before each merge, main's latest full run green with only bot commits after it.

JON'S RULINGS (verbatim in each PR body): 14 Nov 22:46: "do them in numerical order please" (item 2 of 3: Better Value and Chart Interrogator fit a phone). 14 Nov 22:54, to "the shared fix: a lane exception for the cloud lane, or a home-lane contract?": "an explicit exception for home lane is fine for this one".

TASK: Make two Essentials games fit their screens: Better Value's start screen does not scroll sideways at 320 px and its Next is above the fold at 1366 × 768; Chart Interrogator does not scroll sideways at 320 or 375 px.

ROOT CAUSE:
- Better Value, sideways: its session-length row is drawn by schools/assets/session-length.js (render, :70-99) into the game's mount #sessionRow (games/better-value/index.html:231), styled by the game as a flex row that cannot wrap (:62 .session-row: display:flex, no flex-wrap) with 12px 28px buttons (:63). It offers four (10, 20, 30, All (50)), 339 px wide at 320 (scripts/checker-allowlist.json tier1_phone_overflow: at load, button.session-btn).
- Better Value, Next: about 180 px below the fold at 1366 × 768 (todo BETTER-VALUE-NEXT). Not yet traced: part of this task.
- Chart Interrogator: tier1_phone_overflow records 392 px at 320 at start, in div.diagram-panel and #questionPanel; todo CHART-INTERROGATOR-SCROLL records 34 px at 375. A quick measurement on its start screen at 375 × 667 found no overflow, so it is on a question screen. Not yet traced: part of this task.

CLASS CHECK:
- The session row is a class. session-length.js draws the buttons for 12 games, and each game styles the row itself. Three of them leave it unable to wrap: Better Value (.session-row), Expected Damage (.session-select) and Log Laws (.session-row). Only Better Value overflows today (the tier 1 gate measures every page at 320 px), but the other two will once their buttons outgrow the row. The script owns the buttons it puts in the mount, so it owns their wrapping: one line in render() fixes all twelve, and no game's CSS is patched.
- Better Value's Next and Chart Interrogator's overflow are each the game's own layout. The 1 Oct phone-fit investigation traced every such overflow to the game's own markup, never to a shared script (todo §3.9, "Not a shared-asset problem"). Fix each in its game; if the trace shows a shared asset is the cause, that is a STOP.

EXACT CHANGE:
PR 1, session row and Better Value:
 1. schools/assets/session-length.js, render(): set the mount's flex-wrap to wrap (mount.style.flexWrap = 'wrap') before the buttons are added. Nothing else in the script changes. Update its header comment's guarantees with one line.
 2. Better Value: trace what puts Next about 180 px below the fold at 1366 × 768, on both outcomes and every stage; fix it in the game's own layout (spacing, order, sizing of the game's own blocks), within canon §7.5's type and target minimums. State the cause and the fix in the PR body.
 3. Remove Better Value's tier1_phone_overflow entry; todo rows 1.34 (Better Value's part) and BETTER-VALUE-NEXT closed.
 4. Evidence in the PR body: screenshots of every one of the 12 session-length games' start screens at 320 × 568 and 1366 × 768, before and after; only Better Value's may differ.
PR 2, Chart Interrogator:
 5. Trace the overflowing element on every question type and phase, at 320 × 568 and 375 × 667; fix it in the game's own markup or CSS. State the element and the fix in the PR body.
 6. Remove its tier1_phone_overflow entry; todo row CHART-INTERROGATOR-SCROLL closed.
Each PR: docs/handover/cloud.md entry; no /updates/ line (layout fixes).
DO NOT TOUCH: session-length.js beyond EXACT CHANGE 1 (lengths(), the labels, onChange, the selected logic); every other game's CSS and markup, Expected Damage and Log Laws included (they get wrapping from the shared line); question content and marking in both games; the phone-fit and tier 1 checks and their thresholds; the tier3_exceptions entry for Better Value; Gate files; each game's theme and palette.
SUCCESS CONDITION: Better Value's start screen fits 320 × 568 without sideways scroll; its Next is above the fold at 1366 × 768 and at every size the phone-fit check measures; Chart Interrogator has no sideways scroll at 320 and 375 on any screen; both allowlist entries are gone and the Gate is green without them; the other 11 session-length games' start screens are unchanged in the before/after screenshots; two PRs merged in order on green; main's check-site and phone-fit-full green on each merge commit and reported; cloud.md and the todo rows updated.
STOP IF: the wrap line changes any other game's start screen where it did not overflow; Better Value's Next can fit only by removing content or going below canon §7.5's minimums; the trace shows a shared asset other than session-length.js causes either fault; Chart Interrogator's overflow cannot be reproduced at any measured size (report what was measured; do not remove its entry unless the Gate measures it clean); any check would have to be loosened or an entry added to an exception list.
