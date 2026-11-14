# UGH-STATS-HOME (contract, verbatim)

Received by the home lane (Claude Code) 14 Nov 2026, from Jon's paste.

```text
UGH-STATS-HOME (Project Claude, Sat 14 Nov 2026 17:15; reissued 22:45 with the branch deletion, Jon 22:38 "yes please"; Jon's ruling 14 Nov 17:06)
Recommended: Sonnet or Opus, effort medium: three small additions to the homepage, the site's busiest page, and one branch deletion.
LANE: home. TIER: Medium (merge on green; Project Claude reviews after merge). START: now. If UGH-STATS-CASE1-1DP's (#768, 51bc881) close-out is not yet on main, carry it in this PR's first commit, per the standing rule; if it is, do not repeat it. One PR. Branch from current origin/main.
MERGE: merge-pr.py on a green Gate.

JON'S RULINGS (verbatim in the PR body): 14 Nov 17:06: "1, 2 AND 3 please" (to: 1 a header badge; 2 the answers-given total as a link; 3 a card in the game list when the Statistics topic is chosen). 14 Nov 22:38: "yes please" (to: the home lane deletes the leftover branch art/answer-box-redraws, which the cloud session that merged #769 could not delete: HTTP 403, it can push only to its own branch).

TASK: Give "Ugh, stats" three ways in from the homepage, so it is not only in the footer; and delete the leftover branch art/answer-box-redraws.

ROOT CAUSE: /ugh-stats/ is linked from the homepage only in the footer (index.html:3316); nothing a visitor sees at the top of the page, or while browsing statistics games, leads to it. Separately, art/answer-box-redraws (799748c) was squash-merged as #769 (c0cec86) and left on the remote because a cloud session cannot delete branches it did not create.

CLASS CHECK: Local. All three are homepage markup and the homepage's own filter script; no shared asset changes. The answers-given total is filled by schools/assets/answer-count.js ([data-maffs-answer-total], index.html:748): the link is made by wrapping that element in index.html, not by changing answer-count.js, which other pages use. The branch is a one-off leftover; cloud sessions' push limits are a known platform constraint, not a repo bug.

EXACT CHANGE:
1. Header badge. In .header-badges (index.html:750-782), after the Leaderboards badge, add a plain badge in the style of the white trust badges (same class "badge", text colour rgba(255,255,255,0.9), no tinted background, no tick icon): <a href="/ugh-stats/" class="badge" data-mfg-item="open-ugh-stats" ...>Ugh, stats &rarr;</a>. It must not use Essentials' teal styling: Essentials stays the one that stands out.
2. The total as a link. Wrap the existing <div class="answer-total" data-maffs-answer-total hidden></div> (index.html:748) in <a href="/ugh-stats/" class="answer-total-link" data-mfg-item="answer-total-ugh-stats" title="How we use these numbers">. The link inherits the total's look (no underline at rest; underline on hover and focus; a visible focus ring); while the total is hidden, the link takes no space and is not focusable (tabindex handling or display:none on the wrapper while the div is hidden; your method, stated).
3. Statistics card. When the Statistics topic is active (setTopic('statistics'), index.html:3408; applyFilters at :3416), show one card at the top of the game grid; hide it for every other topic and for "All". Text: heading "Ugh, stats."; body "Real numbers from this site, the decisions we made with them, and questions for your class."; link "Read the cases &rarr;" to /ugh-stats/, data-mfg-item="topic-ugh-stats". It is not a .game-card: it is not counted in the game count, not matched by search, never marked New, and the level filter does not hide it while the Statistics topic is active. Styled like the existing info cards on the page (the fact card), light theme, no emoji.
4. Delete the remote branch art/answer-box-redraws. First confirm it holds nothing that is not on main: for every file it changed against its merge base, the file's content at 799748c equals its content at c0cec86 (git diff 799748c c0cec86 -- <those files> is empty). Then git push origin --delete art/answer-box-redraws. State the check and its result in the PR body and home.md.
5. /updates/: no line (a link, not a feature). home.md entry, which also notes the branch deleted so the next cloud close-out does not carry it.
DO NOT TOUCH: schools/assets/answer-count.js and every other shared asset; the existing badges' order and styles; games.json and the game cards; every page other than index.html; ugh-stats/; docs/handover/cloud.md (the cloud lane's own close-out records #769); every remote branch other than art/answer-box-redraws.
SUCCESS CONDITION: on the live homepage the badge, the linked total and the Statistics card all reach /ugh-stats/; the card shows only with the Statistics topic; the game count and search results are unchanged with and without it; the homepage passes its phone-fit sizes and theme check with the badge row wrapping cleanly at 320 px; keyboard focus reaches all three; art/answer-box-redraws is gone from the remote after the content check passed; Gate green; merged; main's check-site and phone-fit-full on the merge commit green and reported; home.md updated.
STOP IF: the badge row overflows or pushes the header past its phone-fit limits at any checked size; making the total a link would need a change to answer-count.js; the card cannot be kept out of the game count or search without changing shared code; any existing homepage check would have to be loosened; any file on art/answer-box-redraws differs from main at c0cec86 (do not delete; report the files); the branch delete is refused.
```
