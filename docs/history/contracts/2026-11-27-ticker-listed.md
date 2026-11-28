TICKER-LISTED (Project Claude, Fri 27 Nov 2026 22:20; checked against main 083faa3)
Jon, 27 Nov 2026, 21:55: "a small clean up job please after this, I don't want unlisted games showing on the leaderboard ticker. when I'm testing it showing unlisted games which cannot be clicked. it's a small thing but it bothers me".
RECOMMENDED: Claude Code, Sonnet 5.5, effort medium. One function in the portal page and its existing check.
LANE: cloud. SEND: now. First commit carries LEADERBOARD-PAGE's close-out (AGENTS.md:62): #939 squash-merged as 083faa3 by merge-pr.py, its last line "main 083faa3 run 46072970885: GREEN" (exit 0); main's runs on 083faa3: check-site 46072970885, phone-fit-full 46072970949, pages 46072970255, each success. Move docs/handover/contracts/2026-11-27-leaderboard-page.md to docs/history/contracts/. Save this contract verbatim as docs/handover/contracts/2026-11-27-ticker-listed.md in the same commit.
TIER: Medium (merge on green).

TASK: Show on the front page's score ticker only scores from games that are on the portal, so an unlisted game never appears there.

ROOT CAUSE (file:line on 083faa3):
- The ticker shows the latest 20 entries of recent_scores, whatever game wrote them (index.html:3943, MaffsLeaderboard.watchRecent(20, ...); schools/assets/firebase-leaderboard.js:688-691). Unlisted games submit scores too (as does any game Jon is testing), so they appear.
- tickerHref (index.html:3811-3824) already knows which games are on the portal (its game cards, contract TICKER-LINKS) and gives a score with no card no link; buildTickerItem (:3831-3854) still shows it, as a plain span that cannot be clicked.

CLASS CHECK: Local. The ticker is the only place that shows the live score feed; its rule for "on the portal" already exists (tickerHref's card map), and the fix applies that rule to what is shown as well as to what links. The hub's list is held separately by check-leaderboard-coverage.js (#939).

EXACT CHANGE:
1. index.html: a score whose slug has no portal game card is not shown on the ticker at all (the same test tickerHref uses, from the same card map, built once). Read a wider window so the ticker still has scores to show while Jon tests unlisted games: watchRecent(50, ...), keep the newest 20 that pass. If none pass, the ticker shows its existing "No recent scores yet" line. buildTickerItem's no-link branch (a plain span) goes, since every item shown now has a link.
2. scripts/test-ticker-links.py: a case seeding the fake feed with scores from a listed game and an unlisted one: only the listed one appears, as a link; a feed of 30 unlisted then 5 listed scores still shows the 5. Plants, each must FAIL: an unlisted score shown; the window back at 20 with the 30-then-5 feed.
3. docs/canon.md: the ticker_clicked row (:263) says every score the ticker shows has a portal card and links to it (TICKER-LISTED, Jon, 27 Nov 2026); the recent_scores note (:2343) says the ticker reads the latest 50 and shows the newest 20 from listed games. docs/handover/cloud.md entry. /updates/: none.

DO NOT TOUCH:
- schools/assets/firebase-leaderboard.js (watchRecent, submitScore, recent_scores writes), the Firebase rules, the leaderboards hub, every game page.
- The ticker's badges (standing(), deriveBadge), its escaping (esc), its pause button, its animation, ticker_clicked.
- canon beyond the two lines; scripts/merge-pr.py; every workflow.
- No force-push.

SUCCESS CONDITION:
- The ticker shows only scores from games with a portal card, newest 20 of the latest 50; every item is a link; the new cases and two plants run in CI; every existing check passes.
- Merged on green through python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600, run from main's checkout (merge main in and re-run if main moves first); last line and main's run IDs in cloud.md.

STOP IF:
- Any listed game writes recent_scores under a slug that does not match its portal card's folder: list it; do not hide it.
- main is red when you come to merge: report it; do not use --override.
- merge-pr.py cannot reach GitHub or refuses for a reason other than freshness: report its output; do not merge another way.
