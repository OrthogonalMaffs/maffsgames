# Handover: home lane

**Queue (cross-lane facts; never archived)**

- PHONE-SCROLL (Small; Project Claude, 10 Nov 05:55, Amendments 1-3): merged as a594c8f (#721) under Jon's one-off ruling of 10 Nov 07:05; main run 42772678182 GREEN (89/89 jobs; phone-fit-full 42772678203 green). Entry below.

- DOCS-BUNDLE (Docs; Project Claude, 9 Nov 19:10, Amendments 1-2): merged as 10d3167.

- WHOSE-SIDE: the cloud lane owns the game until stage 5; timer-policy.md's line is `docs/todo.md` row WHOSE-SIDE-TIMER-LINE. DONE lines moved to docs/history/handover-home-archive.md, 8 Nov.

- One lane at a time: AGENTS.md, Lane ownership (rule e, BACKLOG-ONE).

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts: `docs/todo.md` row HOW-MANY-PARTS-FRACTION (§3)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

## 2026-11-24 (home): THREE-GAMES-LIST (MaffsCards, Sums in Disguise and Some Thingies are listed)

Claude Code (home lane), worktree `~/mg-three-games-list`, branch `claude/three-games-list`. The contract is at `docs/history/contracts/2026-11-24-three-games-list.md` (verbatim, with Amendment 1). The first commit closed out TIER3-LOCK-FIX.

- **Approval (verbatim):**
  - Jon, 24 Nov 2026, 21:32: "lets release maffscards and the 2 primary games please."
  - Jon, 24 Nov 2026, ~21:35, answering Project Claude: "No Essentials cards" (portal KS3 section only; the two primary games stay on /class/ as now).
- **Portal:** three cards at the end of the KS3 section, New badges dated 2026-11-24. MaffsCards is `ks3`; the other two are `year6 ks3` and link `?level=year6`.
- **Also listed on:** the sitemap, the leaderboard hub (4, 5 and 8 boards), /updates/, and for MaffsCards the spec map (GCSE N4). MaffsCards' noindex is gone.
- **Roster:** #113, #114 and #115 are in KS3 Games (38), look signed off by Jon, 2026-11-24. Unlisted is 9.
- **Amendment 1 (Jon, in session):** check-spec-mapping.py failed the two primary games, which the contract keeps off the spec map. Jon chose "EXCEPTIONS entry (Recommended)"; both are in that script's EXCEPTIONS.
- **Coverage check:** it needed LEVEL_OVERRIDES entries for the two primary games' stage boards, as the contract allowed.
- **Todo:** MAFFSCARDS-LIST moved whole; the other two rows keep Jon's LINES rewrites and Miss O'Brien's questions.
- **Screenshots:** the three cards at 1366 x 768 and 375 x 667, sent to Jon in session.
- **Merged** on 24 Nov as ee09c84 (#905) via merge-pr.py, which ended "main ee09c84 run 45497440759: GREEN".
- **PR head b8569cd:** check-site 45494570251 and phone-fit-full 45494570226, both success.
- **Main on ee09c84:** check-site 45497440759 success, phone-fit-full 45497440773 success, pages build 45497440296 success.
- **Cleanup:** end-task cleaned up. The contract moved to `docs/history/contracts/`, closed out by MAFFSCARDS-CHALLENGE's first commit.

Record: agent Claude Code; wall 0:40; review cycles 0; amendments 1; usage n/a.

## 2026-11-24 (home): TIER3-LOCK-FIX (tier 3 plays the games the 300 ms answer lock made it skip)

Claude Code (home lane), worktree `~/mg-tier3-lock-fix`, branch `claude/tier3-lock-fix`. The contract is at `docs/history/contracts/2026-11-24-tier3-lock-fix.md` (verbatim). The first commit closed out TIER3-COVERAGE-REPORT.

- **Fix:** tier3()'s contexts add `bc.NO_LOCK_FRESH_INIT`. quadratic-factoriser left tier3_exceptions.
- **Local, four shards as CI runs them, main 855fce7 then the branch:**
  - runs passing 49 to 188 of 355, questions 556 to 1799, 0 FAIL both times, KaTeX check clean;
  - games passing every run 10 to 52: the report's 39, plus estimation-golf, screening-room and spot-the-muppet;
  - expectation-station is no longer UNSUPPORTED but WARNs once (a repeated tile, which the driver expects there);
  - 64 games still have an UNSUPPORTED run.
- **Wall time:** shards took 8:06 to 9:19 locally (3:22 to 6:35 before). The CI step timeout is 12 minutes: cloud to watch.
- **Self-test:** new `--tier3-lock-selftest`: tier3() plays a planted lock page fully; with the init script emptied it is UNSUPPORTED after 1 question. CI does not run it until cloud adds it to the workflow.
- **Decided for you:** the planted page shows its next question 460 ms after a mark, not at once as the contract says. Shown at once, it is tapped 500 ms later, outside the window, and the plant is not caught (tested).
- **For Project Claude:** the tier3_exceptions entries for spot-the-muppet and expectation-station are now stale; not touched.
- **Merged** on 24 Nov as 590efd7 (#904) via merge-pr.py, which ended "main 590efd7 run 45489207767: GREEN".
- **PR head 87ccba6:** check-site 45486151268 and phone-fit-full 45486151312, both success.
- **Main on 590efd7:** check-site 45489207767 success, phone-fit-full 45489207373 success, pages build 45489206130 success. CI's tier 3 counts match the local ones on all four shards (486 to 557 s a shard).
- **Cleanup:** end-task cleaned up. The contract moved to `docs/history/contracts/`, closed out by THREE-GAMES-LIST's first commit.

Record: agent Claude Code; wall 1:05; review cycles 0; amendments 0; usage n/a.

## 2026-11-24 (home): TIER3-COVERAGE-REPORT (which games CI's tier 3 really plays, and whether the 300 ms answer lock is why it skips the rest)

Claude Code (home lane), worktree `~/mg-t3`, branch `claude/tier3-coverage-report`. The contract is at `docs/history/contracts/2026-11-24-tier3-coverage-report.md` (verbatim). The first commit closed out HALF-THE-SIZE.

- **Report:** `docs/audits/tier3-coverage-2026-11.md`, with one row per game, every run's reason in full, and the result when waited out.
- **Stock tier 3, local = CI exactly** (main 77b6a78, run 45255198196, all four shards' numbers and the same 106 UNSUPPORTED games):
  - 116 games, 352 runs;
  - 10 games PLAYED in every run, 4 more at some levels;
  - 49 runs PASS, 303 UNSUPPORTED, 0 FAIL, 556 questions;
  - 9 UNSUPPORTED games are recorded in tier3_exceptions and 97 are not.
- **Waited out** (each tap waits until `MaffsLock.isFresh()` is false, as check-answer-lock.py does; throwaway wrapper, never committed): of the 97 unrecorded games,
  - 39 now play fully, 4 at some levels;
  - 54 are still UNSUPPORTED: 25 never offer an option group, 29 are still unmarked after a waited tap;
  - runs passing site-wide 49 to 167, questions 556 to 1597.
- **Control:** FRESH_MS set to 0 and no wait gives the same 39 + 4, so the 300 ms window is the cause for those 43.
- **Cloud lane's report confirmed:** formula-unlocked and scale-factor-scaling are UNSUPPORTED on every run stock and PASS on every run (10 questions) waited out.
- **Also found:** quadratic-factoriser's tier3_exceptions entry is stale (it PASSES).
- **Decided for you:** tier 3 was run through a throwaway wrapper that calls check-site.py's own `tier3()` with CI's arguments, rather than the bare command, because CI's output truncates reasons to 90 characters and never lists the games it played. Its numbers match the bare command's (CI's) on all four shards.
- **Merged** on 24 Nov as fa3f7be (#895) via merge-pr.py, which ended "main fa3f7be run 45356433810: GREEN".
- **PR head de3cfbe:** check-site 45354282188 and phone-fit-full 45354282154, both success.
- **Main on fa3f7be:** check-site 45356433810 success, phone-fit-full 45356433623 success, pages build 45356433627 success.
- **Cleanup:** end-task cleaned up. The contract moved to `docs/history/contracts/2026-11-24-tier3-coverage-report.md`, closed out by TIER3-LOCK-FIX's first commit.

## 2026-11-23 (home): HALF-THE-SIZE (Scale Factor Scaling becomes "But It's Only Half the Size!": funny prompts, 8 new questions, KaTeX notation, calculator required)

Claude Code (home lane), worktree `~/mg-hs`, branch `claude/half-the-size`. The contract is at `docs/handover/contracts/2026-11-23-half-the-size.md` (verbatim). The first commit closed out FORMULA-UNLOCKED-BANK.

- **Banks:** APPENDIX A, verbatim: 54 items in five tiers. GCSE serves 46, A-Level and Level 4 serve 54.
- **KaTeX:** steps and notes go through MaffsText, and fraction options show as \dfrac. The start screen renders once KaTeX has loaded, and startGame waits for it.
- **Calculator:** required, docked to the question card.
- **Name:** changed everywhere step 5 lists except `<title>`/og:title, which stay as before by Jon's ruling, because check-meta ties them to data/games.json, which this contract cannot touch.
- **Verifier:** APPENDIX B and T5, plus a KaTeX check on all 54 items. PASS, with all 7 plants caught.
- **First fix:**
  - scroll.js loads with keypad.js;
  - the KaTeX wait's setTimeout carries a `// lock-ok:` reason;
  - verify-formula-unlocked.py, which grew in #893 and was over the per-line budget at 213s, is split into 3 ci-shards parts (base run plus 9 plants), as Project Claude authorised.
- **Merged** on 23 Nov as 77b6a78 (#894) via merge-pr.py, which ended "main 77b6a78 run 45255198196: GREEN".
- **PR head d4393cfe:** check-site 45252185356 and phone-fit-full 45252185350, both success.
- **Main on 77b6a78:** check-site 45255198196 success, phone-fit-full 45255197837 success, pages build 45255197006 success.
- **Cleanup:** end-task cleaned up. The contract moved to `docs/history/contracts/2026-11-23-half-the-size.md`, closed out by TIER3-COVERAGE-REPORT's first commit.

## 2026-11-23 (home): FORMULA-UNLOCKED-BANK (Formula Unlocked's A-Level mode stops repeating questions; 57 new questions take every level to 40 or more)

Claude Code (home lane), worktree `~/mg-fu`, branch `claude/formula-unlocked-bank`. The contract is at `docs/history/contracts/2026-11-23-formula-unlocked-bank.md` (verbatim). The first commit closed out WWIUT-RESTORE-7.

- **Banks:** the 57 appendix questions, verbatim. Q_GCSE is now 40, Q_ALEVEL 26 and Q_LEVEL4 40, with the contract's stage counts.
- **A-Level draw:** now 6+7+7 from the stage lists, which hold each question once.
- **verify-formula-unlocked.py:** BANKS, GREEK and the \ln\left( fix. A new session check runs startGame() 1000 times at each level: no repeats, and no session shorter than its draw. It passes at all three levels: 106 questions, and all 9 self-test plants caught, including the old A-Level line.
- **Decided for Jon:** Level 4's session minimum is 18, not 20, because its draw (unchanged by contract) takes 4+5+5+4. Also, the session check runs only for its own plant during the self-test.
- **First fix:** the Gate's 6 P's bank line failed, because change-subject.json is generated from this game. I regenerated it (schools/assets/six-ps/, allowed by Jon on 23 Nov). The time budget was not the failure.
- **Merged** on 23 Nov as 28be68a (#893) via merge-pr.py, which ended "main 28be68a run 45236117062: GREEN".
- **PR head 6d1fc0eb:** check-site 45233939506 and phone-fit-full 45233939165, both success.
- **Main on the merge commit:** check-site 45236117062, phone-fit-full 45236117010 and pages 45236116620, all success.
- **Cleanup:** end-task cleaned up. The contract moved to `docs/history/contracts/2026-11-23-formula-unlocked-bank.md`, closed out by HALF-THE-SIZE's first commit.

## 2026-11-23 (home): WWIUT-RESTORE-7 ("When will I use this?" gets back the 7 jobs #888 left out, and a Probability page: 47 jobs in 17 topics)

Claude Code (home lane), worktree `~/mg-r7`, branch `claude/wwiut-restore-7`. The contract is at `docs/history/contracts/2026-11-23-wwiut-restore-7.md` (verbatim). It was closed out by FORMULA-UNLOCKED-BANK's first commit.

- **Data:** the 7 scenarios verbatim, Probability after trigonometry, and the payroll sentence; a script asserted no other change. Also the Probability page entry, its one HUBS line, and a line on /updates/.
- **check-uses.py:** self-test 98 of 98, 47 headlines, 33 pages, 62 sources, OK. Every figure is the contract's.
- **Live link check:** 55 of 60 answered 200, so the STOP IF fired. Five failed: Wonkee Donkee 522, Plus 403, The Analyst 403, uhsussex ?p=5862 404, FSA hot-holding PDF 404. BNMS redirects to its home page. Reported in #891 and held.
- **Merged:** 23 Nov as 38895242 (#891), on Jon's "merge" after the held report, via merge-pr.py. Its last line read "main 3889524 run 45223623100: GREEN".
- **Gate:** the first Gate failed because check-site's PR-budget job ran past its 5-minute limit and was cancelled. An empty commit re-ran it, and it passed: check-site 45220394899 and phone-fit-full 45220395448, both success.
- **Main on the merge commit:** check-site 45223623100, phone-fit-full 45223623121 and pages 45223622181, all success.
- **Cleaned up** by end-task.
- Ruling (Project Claude, 23 Nov): keep all five sources and all seven jobs. Each page was fetched by Project Claude on 23 Nov and answers with the content the job cites: the 403s and the 522 are the sites refusing automated clients; the two 404s (uhsussex ?p=5862, the FSA hot-holding PDF) answer for a browser fetch. The BNMS redirect is noted; that job keeps its other source. No change to data/uses.json.
- #888: the end-task refusal is expected. 3058b98 is the cloud lane's WWIUT-BATCH-MERGE commit (it took #888 over by contract); #888 merged as a5b3742 and was closed out in the cloud entry. Nothing to do on that branch.

## 2026-11-23 (home): WWIUT-BATCH-1-2 ("When will I use this?" grows to 40 jobs in 16 topics, with a tier on every job and the home strip's count written by the build)

Claude Code (home lane), worktree `~/mg-batch`, branch `claude/wwiut-batch-1-2`; contract `docs/handover/contracts/2026-11-22-wwiut-batch-1-2.md` (verbatim). The first commit carries WWIUT-STAND-OUT's close-out (#885, 66a29e7).

- Data: 26 of the 33 approved scenarios and 12 of the 13 topics, verbatim; every scenario has a tier (the 14 existing "F"). Step 5 took out 7 scenarios whose sources do not answer 200 (re-fetched as a browser too: 404, 410, 403, 522): football-analyst, bricklayer-corner, crime-scene-investigator, mammographer, football-recruitment-analyst, nuclear-medicine-technologist, chef. That passed the STOP IF of 4; by the standing rule the rest was finished and the list reported. Probability, left with no scenario, is left out too (decided for Jon). Each is listed in the PR with its source.
- check-uses.py's reader, in one place, also reads "1,000", "1/16", ½, √, superscript powers, sin, cos, tan and their inverses (degrees), "°", and an expression on the right; the 14 existing scenarios read exactly as before (all 48 results compared). 40 headlines and 83 "=" signs recomputed; 5 new noCheck steps, each with a reason (hours and minutes, minutes and seconds, "% of", "1 in 5"). Self-test 94 of 94.
- build-uses.py: a Higher or Level 4 tag on cards (measured 4.5:1 in Chromium); KaTeX for the new signs; index.html's "N real jobs" written between uses-count markers and checked. A topic heading ("Transformations:") scrolled 46 px at 320 in Aa: headings now wrap long words.
- index.html: #usesFlag and #parFlag lose data-cmp-hide, so both show on phones while current; expiry unchanged. 12 HUBS lines in site-nav.js under Jon's ruling (23 Nov), as #883's 4. 21 new data/games.json "pages" entries; 7 descriptions updated.
- Next: Gate green, then wait for Project Claude's review and Jon's "merge".
- Taken over and merged by the cloud lane (contract WWIUT-BATCH-MERGE, 23 Nov): see docs/handover/cloud.md.

## 2026-11-22 (home): WWIUT-STAND-OUT ("When will I use this?" gets its own navy strip on the home page; the section leads with coloured course tiles and a sum on every job card)

Claude Code (home lane), worktree `~/mg-wwiut`, branch `claude/wwiut-stand-out`; contract `docs/handover/contracts/2026-11-22-wwiut-stand-out.md` (verbatim). The first commit carries WHEN-WILL-I-USE-THIS's close-out (#883, 2710eed).

- Portal: a navy strip (`#usesStrip`, `.par-strip uses-strip cmp`) above the parents strip, with a New flag dated 2026-11-22 and the button "See the jobs" (`data-mfg-item="open-wwiut"`, section `when-will-i-use-this`). The parents strip has its one button again. `applyParFlag()` became `applyStripFlags()`: every `.par-flag[data-badge-date]` expires on BADGE_DAYS; game cards are untouched.
- `verify-new-and-updated.py` checks each strip flag on its last shown day and its first hidden day, read from the markup. A new plant (the expiry ignores the new flag) is caught: 4 of 4.
- Data: 15 route colours, white at 4.92:1 or better, the closest pair delta E 16.4, the nearest to teal delta E 33.5. The 14 headlines are as the contract gives them, and all recompute.
- Pages: the hub runs "Pick your course" tiles, then 14 job cards (each with its headline in KaTeX, linked to `<topic>/#<id>`), then "By maths topic", in a 1040 px container. Scenario cards get a route-colour top band, a route chip and the headline. Route headers are filled with their colour. The hub's foot line drops its self-link. The look is in `when-will-i-use-this/uses.css`, written by build-uses.py.
- check-uses.py: headlines, colours, anchors, no hub self-link, and Chromium contrast on tiles, chips and headers. Self-test 50 of 50. A route header scrolled 9 px at 320 in Aa ("environmental"); fixed with overflow-wrap and less phone padding.
- MERGED 22 Nov as 66a29e7 (#885) via merge-pr.py, exit 0, last line "main 66a29e7 run 45075943570: GREEN", on Jon's "merge", after a merge of main for #886's conflict on updates/index.html (both lines kept; head 662f42a, Gate check-site 45074183522 and phone-fit-full 45074183455, both success). Main on the merge commit: check-site 45075943570 success, phone-fit-full 45075943580 success, pages build 45075943027 success. Cleaned up by end-task. Contract moved to `docs/history/contracts/2026-11-22-wwiut-stand-out.md` (closed out by WWIUT-BATCH-1-2's first commit).

