CORE-PAPERS-SHUFFLE, one part.
LANE: cloud. Send now. TIER: Medium. MODEL: Claude Code, Opus 5.5, medium effort (four pages, four verifiers).

TASK: Every play of the four Core Maths papers deals its questions in a new order within each section, and each question's options in a new order, so a resitting student can't score from memory.

ROOT CAUSE: Checked on main 346ac4d, re-checked on 8b5d7f1 (no change). None of games/core-maths-paper1, -paper2a, -paper2b, -paper2c has a shuffle: questions run in QUESTIONS order (paper1:705 QUESTIONS[currentQ]; 2a:544, 2b:499, 2c:514), and options are drawn in array order with dataset.val = their index (paper1:738-741; 2a:564, 2b:518, 2c:537). The key's position is lopsided: paper2b has 26 of 36 at B; paper1 never uses D. Always pressing B scores 72% on 2B.

CLASS CHECK: A class: the same shell, with the same missing shuffle, in four pages. Fix all four in this one PR. Options go through the shared MaffsOptions (schools/assets/options.js), not a hand-rolled shuffle. The section-preserving deal is a few lines per page, written the same way in all four; a shared module would go in schools/assets/, which is the home lane's, so it stays per page here.

EXACT CHANGE:
1. First commit: close out SURD-WORKING (#838, merge commit 13f4df3: read main's runs from the API, record them in its cloud.md entry, move its contract to docs/history/contracts/). Save this contract verbatim as docs/handover/contracts/2026-11-19-core-papers-shuffle.md.
2. In each paper, startGame() builds the session's paper: each section's questions shuffled among themselves, sections in their current order and sizes (paper1 §3.1 x18 then §3.2 x18; 2a §3.4-3.7 x9 each; 2b §3.4 x6, §3.9 x18, §3.10 x12; 2c §3.4 x6, §3.11 x9, §3.12 x9, §3.13 x12, in whatever order each page uses now). Section banners, "Q n of 36", the progress bar and section scores work from the dealt order.
3. Options: shuffled through MaffsOptions at show time. Marking compares the pressed option's value with the key, never its position or rendered HTML. 2c's accept lists are matched by value too. Letters A-D stay as labels for the positions shown.
4. Analytics: question_answered gains question_id, the question's stable source id (e.g. "p1-q07" for paper1's 7th item as written; "p2a-", "p2b-", "p2c-"). Existing field (schools/assets/analytics.js:52), so no new data. question_index stays the position in this session.
5. The answer-lock hint block at the top of each page (paper1:36, 2c:42 and equivalents) reads the dealt question, not QUESTIONS[currentQ].
6. The verifiers (scripts/verify-core-maths-paper1.py, -paper1-tax.py if it marks through the page, -paper2a.py, -paper2b.py, -paper2c.py) move to the dealt order. Add, per paper, over 20 sessions in Chromium: every question exactly once, in its own section; order differs between sessions; options a permutation of the source options; the key lands in each of A-D somewhere; the key marks right and any other option wrong (accept lists included); question_id sent and stable. New plants that must FAIL: options not shuffled; a question dealt into the wrong section; marking by position. Every existing maths check passes unchanged.
7. Docs: one /updates/ line, "Core Maths papers: questions and answers shuffle on every attempt, so a second go is a real second go." A todo row CORE-PAPER-BANKS (§3): bigger pools per section for repeat attempts, behind the priority-audience banks (Jon, 19 Nov 2026). todo.md stays under its cap. cloud.md entry.
8. PR, Gate and phone-fit-full green, then merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600; report its last line. No draft PR.

DO NOT TOUCH: any question's stem, options, key, working, table or SVG; schools/assets/; canon; docs/handover/home.md; any other game.

SUCCESS CONDITION: all four papers deal a fresh order within sections and shuffled options every play; marking by value; question_id sent; verifiers pass with the new checks and every new plant failing; /updates/ and todo done; SURD-WORKING closed out; merged by merge-pr.py with a GREEN last line; cloud.md records it all.

STOP IF: a paper's shell differs from paper1's enough that one approach doesn't fit all four (report how); any option text or working refers to a letter position (an "A" meaning "option A"): report each, change none; a verifier's maths check fails after the change; merge-pr.py can't reach GitHub; anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies (report under "Decided for you").
END OF CONTRACT
