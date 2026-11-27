LEADERBOARD-PAGE (Project Claude, Fri 27 Nov 2026 20:55; checked against main 314e9ed)
Jon, 27 Nov 2026, 19:21: "only 91 scoring games?"; 19:22: after the d by dx graph build (sent 20:10); 19:23: "also bundle in, there is no back button to get out of the leaderboards page"; 20:46: send to a new cloud session.
RECOMMENDED: Claude Code, Opus 5.5, effort high. One hub page, a shared top bar for every site page (the footer's pattern), two checks, privacy wording.
LANE: cloud (a new session). SEND: now. First commit carries PINNED-LIVE-DATA's close-out (AGENTS.md:62): #936 squash-merged as 447b22b by merge-pr.py (route merge-pr.py, after main was merged in twice, for #935 and #937, both clean, and one allowed rerun of a Plan timeout on ca88d71); its last line "main 447b22b run 46063470902: GREEN"; main's runs on 447b22b: check-site 46063470902 success, pages 46063470524 success, phone-fit-full 46063470889 (read its result from GitHub Actions and record it). Move docs/handover/contracts/2026-11-27-pinned-live-data.md and 2026-11-27-pinned-live-data-amendment-1.md to docs/history/contracts/. Save this contract verbatim as docs/handover/contracts/2026-11-27-leaderboard-page.md in the same commit.
TIER: Medium (merge on green).

TASK: Make the leaderboard hub's game list and count always match the games that really have leaderboards; give every site page the same top bar with a way home; and make the hub's and the privacy page's wording true.

ROOT CAUSE (shown, file:line on 314e9ed):
- leaderboards/index.html:113 hand-types "91 scoring games"; its own GAMES list (:180-287) holds 106 games; 116 game pages load schools/assets/firebase-leaderboard.js.
- Listed games with leaderboards missing from the hub: given-that (roster row 61), constructions-lab (roster row 11). Unlisted games with leaderboards, also absent: as-you-can-see, d-by-dx-why, glorious-gantt, graph-sketcher, hc-factor, i-dropped-my-ice-cream, its-on-sale, possibly-maybe, y-so-steep. On the hub but withdrawn (roster "Withdrawn"; not in data/games.json): regression-rumble.
- The hub keeps its own copy of the game list, which has drifted past every listing since it was typed; scripts/check-levels.py reads its rows (HUB_ROW, :247) only for SR-29 audience listings, never for membership.
- No way out at the top: the hub's only back link is at the foot of the page (leaderboards/index.html:138), under a grid of over 100 games; privacy/index.html has one only at :209. Other site pages carry a hand-copied top bar (nav.nav with "MaffsGames" and "← Back to Games": about/index.html:104, feedback/index.html:87, parents/index.html:27, and essentials, printables, the-6-ps, ugh-stats, updates), so the site's pages differ: the same hand-copying canon retired for the footer (docs/canon.md:1526-1531, "Never hand-copy the footer").
- leaderboards/index.html:115 "Your scores never leave this device" is untrue: top scores, with optional initials, go to the public Firebase boards (privacy/index.html:177 says so). Only the local score history (mfg_hist_v1::, schools/assets/score-history.js:41-54) stays on the device.
- privacy/index.html:181-186 says local storage is used "for two purposes" (accessibility, initials) and :201 that the only data stored on the device is "two local storage preferences"; the score history (score-history.js) and games' own personal-best keys are stored there too.
- leaderboards/index.html:110 and :392 "&#127942;" (a trophy emoji): the portal takes no decorative emoji (canon §7.5).
- scripts/check-site.py:2678-2681: a comment still describes "a 20s fallback that is a safety net"; NEXT-NO-FALLBACK (#937) removed it.

CLASS CHECK: Two classes. (1) A second, hand-kept copy of the game list (the roster is the only copy; data/games.json the single metadata source), the shape of every hand-typed count canon §7.5.3 retired: fixed by CI checking the hub against the single source and a computed count, not a corrected number. (2) A hand-copied top bar on some site pages and none on others, the shape canon fixed for the footer: fixed by one shared top bar, written by a script and held by a check, as the footer is (check-footer.py / apply-footer.py / site-footer.css), not by adding a link to the leaderboard page alone. The check-site.py comment is local (one stale comment).

EXACT CHANGE:
1. leaderboards/index.html:
   - The hub lists exactly the games in the roster's listed sections whose page loads firebase-leaderboard.js, each with the boards it submits under (scripts/check-levels.py already derives these: declared levels and boards, SUBMIT). Unlisted and withdrawn games are not on the hub; regression-rumble comes off; given-that and constructions-lab go on, with their names as the roster has them.
   - The count badge is computed from the list at run time ("N scoring games"), never typed.
   - The badge "Your scores never leave this device" becomes "Your score history stays on this device" (Jon, 27 Nov 2026).
   - Both trophy emoji go (:110, :392); the "All-time high" label keeps its words.
2. scripts/check-levels.py (or a check of its own, named in the report): the hub's games equal the listed games that load firebase-leaderboard.js, and each hub row's boards equal what that page submits under. Plants, each must FAIL: a listed game with a leaderboard removed from the hub; a withdrawn game added; a typed count in the badge; a hub row whose boards differ from the page's.
3. A shared site top bar, on the footer's pattern:
   - One canonical bar (the MaffsGames name linking to "/", and "← Back to Games" as an a.back-link so schools/assets/site-nav.js still turns it into "← Back to <hub>" when the page was opened from a hub), its markup held in one place in a check script and its CSS in one shared stylesheet under schools/assets/; an apply script writes it into every non-game site page: about, leaderboards, privacy, spec-map, feedback, parents (hub and every guide), printables, updates, ugh-stats (hub and pages), essentials, the-6-ps, when-will-i-use-this, op, class, and any other root page the footer's check covers that is not a game or an escape room. Each page's hand-copied nav.nav and its CSS go; the foot-of-page back links on leaderboards and privacy go (the bar replaces them).
   - A page with a designed header of its own that already gives a way home may opt out, each listed in the check with its reason (as check-footer.py lists exemptions); report every opt-out.
   - The check fails CI on a site page without the bar, a bar that differs from the canonical one, or bar CSS outside the shared stylesheet. Plants, each must FAIL: a page with the bar removed; a hand-edited bar; a bar CSS rule in a page.
   - No page's fold or layout gets worse: measure each changed page at 375 x 667 and 1280 x 720 before and after, and list any page whose first content moved more than the bar's height.
   - Games are not in scope (their bar is the separate SITE-BAR pilot, PR #916).
4. privacy/index.html :181-186 and :201: say what is stored on the device: the accessibility preference, the leaderboard initials, and your own score history and personal bests for each game; none of it personal data, none of it sent anywhere except initials you choose to add to a leaderboard score (as :177 says). Keep the gameplay-log sentence and the PECR sentence.
5. scripts/check-site.py:2678-2681: the comment says a wrong answer's Next waits with no timer (NEXT-NO-FALLBACK, #937); code unchanged.
6. docs/canon.md: a short paragraph after the footer's (:1526-1531), "Never hand-copy the top bar", naming the check and apply scripts. /updates/: one line (every site page now has the same bar home, and the leaderboard hub lists every scoring game). docs/handover/cloud.md entry.

DO NOT TOUCH:
- schools/assets/firebase-leaderboard.js, score-history.js, site-nav.js, the Firebase rules, every game page and escape room, the roster, data/games.json.
- The footer, its check and its stylesheet.
- The hub's board rendering, its Firebase reads and esc() (FIREBASE-ESCAPING); the SR-29 audience-listing check (AUDIENCE_LISTINGS).
- PR #916 (SITE-BAR pilot) and anything it changes; scripts/merge-pr.py; every workflow (the Plan timeout is backlog row PLAN-MAP-ONCE, not this task).
- No force-push.

SUCCESS CONDITION:
- The hub lists every listed scoring game and no other; its count is computed; its check and four plants run in CI.
- Every non-game site page has the canonical top bar (or a listed opt-out); its check and three plants run in CI; the before-and-after measurements reported.
- The badge, both emoji, the privacy wording and the check-site.py comment as above; canon paragraph; /updates/ line.
- Every existing check passes in CI; merged on green through python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600, run from main's checkout (merge main in and re-run if main moves first: the freshness guard refuses otherwise); last line and main's run IDs in cloud.md.

STOP IF:
- A listed game loads firebase-leaderboard.js but never submits a score (or submits under a key it does not declare): list it; do not add it to the hub.
- A game page stores something else in localStorage that is or might be personal data: report it before rewording the privacy page.
- The shared bar would push any page's fold check red, or clash with site-nav.js's logo on a wide screen: report it with a screenshot; do not change site-nav.js.
- main is red when you come to merge: report it; do not use --override.
- merge-pr.py cannot reach GitHub or refuses for a reason other than freshness: report its output; do not merge another way.
