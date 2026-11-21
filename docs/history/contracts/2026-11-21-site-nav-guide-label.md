SITE-NAV-GUIDE-LABEL. Cloud lane. From Project Claude; Jon ruled, 21 Nov 2026, 14:55 ("back to guide is fine").
Recommended: Claude Code, Sonnet, low effort. One label map plus a one-line guard in an existing check.

TASK: The 20 parents' guide hubs label the back link "← Back to the guide" (not the guide's full name), and check-site-nav.py proves every hub's label fits on one line on a small phone, so a long label can't come back.

ROOT CAUSE: schools/assets/site-nav.js HUBS (from :19) labels each parents' guide by its full name, e.g. "Fractions, Decimals & Percentages guide", so the back link reads "← Back to Fractions, Decimals & Percentages guide" (:72), long enough to wrap on a phone. Nothing catches it: the phone-fit gate opens pages directly, with no referrer, so it never sees a hub label; check-site-nav.py tests labels only at 1280x800 (:235-264).

CLASS CHECK: Architectural for the guard: the label text comes from one shared map, and no check measures it in the hub state, so any future long label would wrap unseen. The guard goes in check-site-nav.py, not in a per-label rule. The label change itself is data in that one map.

EXACT CHANGE:
1. First commit: the standing close-out for #862 (merge commit df2c0f8, merge-pr.py, main runs 44911626645 check-site GREEN, pages build, and phone-fit-full 44911626690: record its result; if red, STOP and report), per AGENTS.md.
2. site-nav.js HUBS: every /parents/<topic>/ entry's label becomes "the guide". backLabel is then "← Back to the guide" and shortLabel "← the guide"; the aria-label follows (:87). The other 9 hub labels stay as they are: Games, OP for Secondary, Essentials, Specification map, What's changed, 6 or 7, Printable packs, Escape rooms, Leaderboards.
3. check-site-nav.py: for each distinct label in HUBS, open one standard a.back-link game (e.g. games/angle-ace/) at 360x640 with that hub as referrer, and assert the back link's text sits on one line (its height equals its line height). Do the same for one stage-exit game's row link. Add a plant: a hub label of 60 characters must be caught.
4. Merge on green via scripts/merge-pr.py, then the standing close-out; cloud.md entry kept short.

DO NOT TOUCH: Any game page or its header. The hub detection, sessionStorage and logo logic in site-nav.js. stage-exit.js. The 9 non-guide labels. CI budgets.

SUCCESS CONDITION: Opened from any parents' guide, a game's back link reads "← Back to the guide" and goes to that guide. Every hub label fits one line at 360 px on a standard game and a stage-exit game, proven by the check, and the 60-character plant is caught. #862's close-out is on main. CI is green and the PR is merged.

STOP IF: A label among the 9 kept ones fails the one-line test at 360 px (report it with its width; don't shorten it: Jon rules). phone-fit-full 44911626690 is red. Main goes red for a reason outside this change (one rerun per AGENTS.md, then stop and report).
