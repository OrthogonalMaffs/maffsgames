CORE-PAPERS-NO-LETTERS, one part.
LANE: cloud. Send now. TIER: Small. MODEL: Claude Code, Sonnet 5.5, medium effort.

TASK: The four Core Maths papers stop labelling their option buttons A-D, so a letter on a button can never be mistaken for a letter inside an option.

ROOT CAUSE: Checked on main eb89b6f. Each paper's option builder prints a position letter in .option-letter (paper1 :760-767, 2a :585-592, 2b :539-546, 2c :558-565). Five items name things with letters inside their options or stems: "Option A/B" (2B Q33-34), "Graph A/B" (2C Q4), "School C" (2A Q1), "Batch A" and "Account A" (Paper 1). Since #840 (merged) shuffles the options, "A: EV = £2,200" can sit beside button C. And since the shuffle, a button's position carries no meaning, so the letters can only mislead (Jon, 19 Nov 2026).

CLASS CHECK: A class: the same option builder in four pages, and any item added later (todo CORE-PAPER-BANKS) could clash the same way. The fix goes in each page's builder, written the same way in all four, rather than renaming the five items. This matches #840, which kept the deal per page because schools/assets/ is the home lane's.

EXACT CHANGE:
1. First commit: close out WORKING-CARD (#841, merge dc7885b, run 44616595773: read main's runs on its merge commit from the API, record them in its cloud.md entry, move its contract to docs/history/contracts/). Save this contract verbatim as docs/handover/contracts/2026-11-19-core-papers-no-letters.md.
2. In each paper's option builder: the .option-letter badge stays, same size and place, but holds no text (aria-hidden="true") until marking, when it shows ✓ or ✗ as now. Remove the letters array. Each button's accessible name is its option text alone.
3. scripts/core_paper_deal.py: replace the check that the letters read A-D (:54, :136-137) with a check that no badge holds text before marking, and that after marking the pressed button and the key's button show ✗/✓ as now. A new plant that must FAIL: the letters put back.
4. cloud.md entry. No /updates/ line.
5. PR, Gate and phone-fit-full green, then merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600; report its last line. No draft PR.

DO NOT TOUCH: every question's stem, options, key and working (the five lettered items keep their wording); the shuffle and deal; marking; analytics; schools/assets/; canon; docs/handover/home.md; any other game.

SUCCESS CONDITION: no button in the four papers shows a letter before marking; ✓/✗ marking unchanged; the deal check's new test passes and the plant fails; all five Core Maths verifiers pass otherwise unchanged; WORKING-CARD closed out; merged by merge-pr.py with a GREEN last line; cloud.md records it all.

STOP IF: anything reads the letters (a keyboard shortcut, analytics, the answer-lock hint, any text that says "press A"): report it and change nothing; the empty badge changes any phone-fit measurement; merge-pr.py can't reach GitHub; anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies (report under "Decided for you").
END OF CONTRACT

AMENDMENT 1 (Jon, 19 Nov 2026), ruling on #843's stop, verbatim:
Ruling on #843's stop (Jon):
1. Remove the seven stale known-failures entries from scripts/phone-fit-state.json (lists may shrink).
2. Do not list Paper 1's Aa 320x568, and do not nudge 2 px for one deal. Since #840 any question can be shown first, so measure every question, not the seeded one: add to scripts/core_paper_deal.py a phone-fit pass over every question of all four papers on the asking screen, against the fold less the footer, in page coordinates: normal mode at 320x568, 375x667, 390x844 and Aa at 375x667, 390x844 — the last option ends above the fold; Aa at 320x568 — the options start above the fold (canon 7.6.1's gate and its Aa exception).
3. Fix what fails in the pages, the same way in all four (spacing above the options, not the stems or options' text), until every question passes. If more than 10 questions across the four papers fail after reasonable spacing changes, or a fix would change any question's text, stop and report the figures.
4. One todo row PHONE-FIT-PR (§4, home lane): a PR that changes a game page is never phone-fit measured before merge (phone-fit-full runs on main only, and only when a shared path changed: .github/workflows/phone-fit-full.yml:42-79), so #840 turned main red unseen. Measure the PR's changed games in the Gate. Keep todo.md under its cap.
5. Then the manual phone-fit-full run on the branch green, Gate green, merge with merge-pr.py. Record this stop and ruling in cloud.md.
