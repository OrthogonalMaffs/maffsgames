HOME SESSION — two contracts in order (Project Claude, Tue 10 Nov 2026, 21:05). Jon, 20:37: high-value home work tonight, minimal time at the PC.

PREAMBLE (applies to both):
- Order: HUB-ALL-BOARDS first, merged; then FIREBASE-ESCAPING from the new main. Both edit leaderboards/index.html, so never in parallel with each other.
- May run alongside the cloud lane's CAST-AWAY-DIAGNOSE (branch claude/cast-away-diagnose) only. The only shared file is updates/index.html: whichever merges second takes main and keeps both lines. Any other open PR from another lane: STOP.
- MERGE CHANGE (Jon, 10 Nov evening): each contract's "Stop at a green Gate for Project Claude's review and Jon's merge; do not merge" is replaced by: merge with merge-pr.py --watch once its Gate is green (Small, home lane); Project Claude reviews after merge. Report main's run on each merge commit.
- Each PR that changes what a student sees adds a dated /updates/ line (AGENTS.md). HUB-ALL-BOARDS: "Leaderboards: the all-levels boards for Fraction Snap, Percentage Flip and Prime Sprint now show on the leaderboard hub." FIREBASE-ESCAPING: no line (nothing visible changes).
- Line numbers re-checked on main c89392e: leaderboards/index.html hub rows :184, :186, :187 (as written); check-leaderboard-coverage.js submittedLevels :275–282 (written as :274–281); Firebase render :394 (written as :393–395), and :382 also inserts best.score unescaped (FIREBASE-ESCAPING step 1's whole-file audit covers it); index.html esc() is at :3775 (written as :3758); firebase/database.rules.json :26 and :28 as written.
- Firebase rules: the FIREBASE-ESCAPING PR writes the rules file and the deploy doc only. Jon deploys afterwards. No deploy and no live write from this session.

=== CONTRACT 2 (after contract 1 has merged) ===
FIREBASE-ESCAPING (Project Claude, 10 Nov 06:30)
LANE: home · TIER: Small · branch from current origin/main (after HUB-ALL-BOARDS). Save this contract verbatim in docs/handover/contracts/ in the first commit.

Evidence (Firebase export of 10 Nov 06:13): the deployed rules are the repo's (docs/firebase-rules-deploy.md records Jon's deploy and live check on 30 Sep; all 572 recent_scores entries and every leaderboard entry obey them: initials 0–3 capitals, score a number). The only unescaped render of Firebase data found: the hub (see preamble line numbers). The homepage ticker escapes everything (esc(), index.html); firebase-leaderboard.js renders the player's own local score only; six-sevens-bruv's initials are local, not Firebase. Rules: recent_scores game (:26) and level (:28) accept any characters; the ticker escapes them, so no exposure today.

TASK: The leaderboard hub escapes every value it reads from Firebase, and the rules file refuses < and > in recent_scores' game and level, ready for Jon to deploy.
ROOT CAUSE: leaderboards/index.html joins e.initials and e.score (and best.score) into innerHTML without escaping; it is safe today only because the deployed rules constrain those fields. firebase/database.rules.json:26 and :28 let game and level hold any characters.
CLASS CHECK: Not a class. A search of every page and shared asset that renders Firebase data found one unescaped render site (the hub); the ticker already escapes and the other initials renders are local data. The fix is local to the hub, plus one rules-file change.
EXACT CHANGE:
1. leaderboards/index.html: one esc() helper in the page (same as index.html's); every Firebase-sourced value inserted into HTML on the page goes through it (initials, score, best.score, and any other field the page renders: audit the whole file, list each site in the PR body). The '&mdash;' fallback stays unescaped markup.
2. firebase/database.rules.json: recent_scores game and level gain `&& !newData.val().matches(/[<>]/)` (keep the existing length rules). Nothing else in the file changes.
3. docs/firebase-rules-deploy.md: a dated section "10 Nov 2026 change" listing the two rule lines before and after, the console steps to deploy, and the two refusals to test after deploying (a recent_scores write with game "<b>x</b>" refused; a normal score still accepted). Status line: "Written, NOT deployed — Jon deploys."
4. A plant in the hub's existing check, or a small script in scripts/ if none covers the hub: a board entry whose initials contain markup must render as text. Report it caught.
5. todo row FIREBASE-ESCAPING: append the result; it stays open, owner Jon, for the deploy only.
6. Close-out entry in docs/handover/home.md; release any claim.
DO NOT TOUCH: the live Firebase rules or data (no deploy, no REST write); schools/assets/; index.html (the ticker); any game; Gate files and workflows; canon; cloud.md; other todo rows.
SUCCESS CONDITION: every Firebase value the hub renders is escaped (list in PR body); the plant fails on old code and passes on new; the rules file validates (JSON parses; the regex form matches the file's existing style); deploy doc ready for Jon; Gate green; merged as the preamble says.
STOP IF: any other page or shared asset is found rendering Firebase data unescaped (report it; it becomes a class and the contract changes); the rules change would refuse any value a current game actually sends as game or level (check every submitScore() caller's game names and level labels; report any with < or >); testing the rules would need a deploy or a live write.
