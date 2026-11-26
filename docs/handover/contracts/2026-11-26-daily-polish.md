DAILY-POLISH (Project Claude, Thu 26 Nov 2026 13:45; checked against main f060351)
Jon, 26 Nov 2026, 13:26: "yes please" to the DAILY-DEAL follow-ups; accepts a scroll for the Play button on very small screens and large text (DAILY-FIT's open item: closed, no change).
RECOMMENDED: Claude Code, Opus 5.5, effort medium. Two small fixes to a live feature Jon uses daily.
LANE: cloud, lane 2. SEND: now (DAILY-FIT merged as 78131de, main green). First commit carries DAILY-FIT's close-out. SEND ORDER: this first; PINNED-LIVE-DATA follows after this merges.
TIER: Medium (merge on green).

TASK: Make a reload of MaffsCards always show Jon's latest daily result, and let the daily workflow's form accept a date typed as 26/11/2026.

ROOT CAUSE: Shown on 26 Nov. (1) games/maffscards/index.html:936 requests 'daily.json' with no query string; GitHub Pages serves it cacheable for 10 minutes, so Jon's result committed at 07:42 showed only after a hard refresh. (2) scripts/set-maffscards-daily.py validate() (:87-98) accepts only YYYY-MM-DD; maffscards-daily run #1 (26 Nov 07:37) failed on a date typed 26/11/2026 in the Run workflow form. (The Creator sheet's script already converts typed UK dates itself: docs/apps-script-creator.js dateText_.)

CLASS CHECK: Local, both. (1) daily.json is the only file on the site that a bot rewrites during the day and a page reads by XMLHttpRequest; cards.json (:952) changes only with a deploy, and Pages' own deploys are covered by the same 10-minute window everywhere, which is not this fault. (2) set-maffscards-daily.py is the one validator for this one input; the Sheet path already handles the format.

EXACT CHANGE:
0. First commit: DAILY-FIT's close-out (AGENTS.md:62): #923 merged as 78131de; main's runs check-site 45822511682, phone-fit-full 45822511577, pages 45822510009, each success. Save this contract verbatim as docs/handover/contracts/2026-11-26-daily-polish.md. Record in cloud.md, closed by Jon 26 Nov 13:26: the Play button below the fold at 320x568 and in phone Aa is accepted (a scroll), no change.
1. games/maffscards/index.html:936: request daily.json with a per-load query string, x.open('GET', 'daily.json?t=' + Date.now()). Nothing else in the load or the panel changes. Update the comment above it (:932) to say why.
2. scripts/verify-maffscards.py: in the daily or dailyui unit, the request the page makes for daily.json carries a query string that differs between two loads. Plant (must FAIL): the query string removed. Every existing unit stays green (open_page's daily.json route already matches a query string: :412).
3. scripts/set-maffscards-daily.py validate(): accept the date as YYYY-MM-DD or as D/M/YYYY or DD/MM/YYYY with slashes (day first, UK); convert to YYYY-MM-DD before every existing check. The file is always written as YYYY-MM-DD; check_file() unchanged. Self-test: add good inputs '26/11/2026' and '25/11/2026' (written as 2026-11-26 and 2026-11-25), '6/1/2027' at a suitable now; add refused inputs '2026/26/11', '11/26/2026' (no month 26), '31/11/2026', '26/11/26' (two-digit year). The existing refused '26-11-2026' (dashes) stays refused.
4. .github/workflows/maffscards-daily.yml:22: the date input's description becomes "The day of the deal: 26/11/2026 or 2026-11-26 (today or yesterday in the UK)". Nothing else in the workflow changes.
5. docs/apps-script-creator.md: section 9 (phone fallback): say the form takes 26/11/2026 or 2026-11-26.
6. docs/handover/cloud.md entry.

DO NOT TOUCH:
- The daily deal's logic, dayCode, the line pool, the panel's layout and art (DAILY-FIT's work), daily.json's contents, docs/apps-script-creator.js.
- cards.json's load, every other screen, challenge codes, Marvin, boards, analytics.
- schools/assets/, scripts/serve-stubbed.py, scripts/bank_common.py, scripts/merge-pr.py, every other game, canon, the roster, every other workflow.

SUCCESS CONDITION:
- The page requests daily.json?t=<number>, different on each load; the verifier proves it and its plant fails.
- set-maffscards-daily.py --selftest passes with the new good and refused dates; a run with --date 26/11/2026 writes "date": "2026-11-26".
- The workflow form's date label names both formats.
- Merged on green through merge-pr.py; main green after; last line and main's runs reported; cloud.md records it.

STOP IF:
- Any existing verifier unit fails after (1) and the cause is the query string.
- Accepting the slash form would let any currently refused input through other than the new slash dates.
- main is red when you come to merge: report it; do not use --override.
- merge-pr.py cannot reach GitHub or refuses: report its output; do not merge another way.
