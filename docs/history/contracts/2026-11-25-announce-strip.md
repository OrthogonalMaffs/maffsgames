ANNOUNCE-STRIP (Project Claude, Wed 25 Nov 2026 18:15; checked against main d4050ed)
Jon, 25 Nov 2026, 17:58-18:00: MaffsCards' Challenge a friend needs to be on the homepage, "people won't know about it unless they see social media or go into the game"; rulings: the homepage strip for two weeks (1), wording "MaffsGames first, Challenge a friend or something similar" (2), this lane after LIKE-TERMS-PLUS, with the MaffsCards Aa results fix (3).
RECOMMENDED: Claude Code, Opus 5.5, effort medium. A small shared component made data-driven, its check updated, and one layout fix.
LANE: cloud, lane 2. SEND: now (#914 merged; lane 2 is free). First commit closes out LIKE-TERMS-PLUS (AGENTS.md:62). The home lane is on SITE-BAR-PILOT (site-nav.js, site-bar.css, stage-exit.js, calculator.css, three game pages, check-site-nav.py, verify-stage-exit.py, docs/todo.md, canon §7.5.8, updates/index.html, docs/handover/home.md): you share updates/index.html only; merge main in before merging.
TIER: Medium (merge on green). Two PRs in this order, each merged before the next: A the strip, B the MaffsCards fix.

TASK: Make the homepage announcement strip read its text, link and end date from data, announce MaffsCards' Challenge a friend for two weeks, and fit MaffsCards' normal results above the fold in Aa at 320x568.

ROOT CAUSE: Shown. (A) schools/assets/launch-sash.js hard-codes its one announcement (END, HREF, TEXT at :21-23, The 6 P's, ended 10 Nov 2026), so every announcement is a code change and a check-script change (scripts/check-launch-sash.py's END regex looks for `var END` in the JS). (B) Reported by the home lane in MAFFSCARDS-CHALLENGE's report (25 Nov, 17:42): on a normal MaffsCards game's results in Aa at 320x568, "Change the settings" ends 11 px below the fold, already so on main before #913; challenge results were tightened by #913 (games/maffscards/index.html:189-194, the .ch-res rules) and fit.

CLASS CHECK: (A) The strip is the site's one announcement component (homepage only); making it data-driven fixes the shape once: every future announcement is an entry, not code, as featured-items.json already is for featured cards. (B) Local: one game's results layout in Aa; the fix reuses that page's own compact rules.

EXACT CHANGE:
0. First commit: LIKE-TERMS-PLUS close-out (AGENTS.md:62); save this contract verbatim as docs/handover/contracts/2026-11-25-announce-strip.md.
PR A, the strip:
A1. index.html, beside the strip's two lines (:750-751): a data block
    <script type="application/json" id="announcements">{"items":[{"id":"maffscards-challenge","text":"A MaffsGames first: challenge a friend on MaffsCards →","href":"/games/maffscards/#challenge","end":"2026-12-10T00:00:00Z"}]}</script>
    (an inline block, not a fetched file: no request and no late layout jump, the pattern MaffsCards' marvinLines uses.)
A2. schools/assets/launch-sash.js: read #announcements; show the first item whose end is in the future (and whose optional start, if given, has passed); every item must have a valid ISO end, and an item without one is never shown. Text by textContent; one link; same id (launchSash), classes, position (before #scoreTicker, else .filter-bar) and look as now. No data-mfg-* labels (the existing rule). If the block is missing or invalid, or no item is live, draw nothing. Update the file's header comment to say it is data-driven.
A3. schools/assets/launch-sash.css: at max-width 380px the text may wrap to two lines (no nowrap there), so the whole sentence shows at 320 px; everything else unchanged.
A4. games/maffscards/index.html: the section the link targets is #challenge (:284). Opening /games/maffscards/#challenge shows the challenge section on screen at 1920x1080 and 390x844 (native anchor scroll; if the page's script moves focus or scroll after load and defeats it, scroll it into view once after load, nothing else). No other change to the page in PR A.
A5. scripts/check-launch-sash.py: replace the `var END` rule with: index.html's #announcements parses; every item has id, text, href (a path on this site) and a valid ISO end; the script compares end with the clock before drawing (keep the Date.now() comparison rule); homepage only (unchanged). Plants (each must FAIL): an item without end; an item with an unparseable end; the JS drawing an item whose end has passed; the sash loaded on a page other than the homepage. Update the ci-line.
A6. In Chromium: the homepage at 1920x1080, 390x844 and 320x568 shows the strip with the whole sentence (no clipping, 4.5:1), and its link opens MaffsCards with #challenge in view; with the clock past end (mfgToday-style test override, never committed) the strip is absent.
A7. /updates/: one dated line: "Homepage: a strip announcing MaffsCards' Challenge a friend, until 10 Dec." docs/handover/cloud.md entry. Merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600 on green; report its last line.
PR B, MaffsCards' Aa results:
B1. games/maffscards/index.html :189-194: apply the compact Aa results rules to every results screen (drop the .ch-res qualifier from those four rules), so normal and challenge results share one layout; update the comment above them. Nothing else.
B2. Measure: normal and challenge results at 320x568 and 375x667, normal and Aa, both buttons above the fold; report before and after. The MaffsCards verifier and phone fit pass (phone fit runs on the PR by itself; do not dispatch it).
B3. /updates/: one dated line: "MaffsCards: on a small phone with Aa on, the results buttons now fit on screen." cloud.md entry. Merge as A7; report its last line.

DO NOT TOUCH:
- The homepage beyond the data block (A1); the ticker, filters, cards, badges, featured cards, hero.
- MaffsCards' game, rules, Marvin, challenge logic, wording, analytics; its page beyond A4 and B1.
- schools/assets/ beyond launch-sash.js and launch-sash.css; every other game; site-nav.js, site-bar.css, stage-exit.js, calculator.css and the three site-bar pilot pages (the home lane's); .github/workflows/; canon; the roster.

SUCCESS CONDITION:
- The homepage strip reads "A MaffsGames first: challenge a friend on MaffsCards →" from data until 10 Dec 2026 00:00 UTC, whole at 320 px, linking to MaffsCards with the challenge section in view; an item without an end can never show; check-launch-sash.py passes with its plants caught.
- MaffsCards' normal and challenge results fit above the fold at 320x568 and 375x667 in normal and Aa.
- Two PRs merged in order through merge-pr.py, last lines reported; cloud.md records both.

STOP IF:
- The sentence cannot show whole at 320 px in two lines at the strip's 13 px: report the measurement and wait for Jon's shorter wording; do not shorten it yourself.
- The #challenge anchor needs more than a single scroll-into-view after load: report why.
- Any existing check fails and the cause is not in this change.
- merge-pr.py cannot reach GitHub, or refuses: report its output; do not merge another way.
