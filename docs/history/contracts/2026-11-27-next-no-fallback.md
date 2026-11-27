NEXT-NO-FALLBACK (Project Claude, Fri 27 Nov 2026 18:55; checked against main 46abd05)
Jon, 27 Nov 2026, 18:27: "I'd remove the auto advance … the student needs to press continue, it gives them a chance to check where they went wrong, and write down the correct method before moving on"; 18:32: "auto advance agreed. I agree the amendment to canon is a good idea" (a right answer that reveals something new waits for Next).
RECOMMENDED: Claude Code, Opus 5.5, effort medium. One shared helper used by 89 games, seven pages' workarounds removed, one canon section.
LANE: home. SEND: now. First commit carries MERGE-GUARD's close-out (AGENTS.md:62): #935 squash-merged as b6c0119 at 18:30 UTC, 27 Nov, on a green Gate at f038472f (check-site 46046955243, phone-fit-full 46046955221); merge-pr.py's last line "main b6c0119 run 46049988829: GREEN"; main's runs on b6c0119: check-site 46049988829, phone-fit-full 46049988775, pages 46049988366, each success. Record the lane's reported departure as it gave it (merge-pr.py was run from the PR's worktree, so the new version judged its own merge; the new check passed and every existing condition was applied unchanged). Move docs/handover/contracts/2026-11-27-merge-guard.md to docs/history/contracts/. Save this contract verbatim as docs/handover/contracts/2026-11-27-next-no-fallback.md in the same commit.
TIER: Medium (merge on green).

TASK: Remove the shared Next control's automatic advance, so a wrong answer always waits for the student; and record in canon that a right answer which reveals something new on screen also waits for Next.

ROOT CAUSE (shown, file:line on 46abd05):
- schools/assets/next-control.js:61 FALLBACK_MS = 20000; :210-212 start a timer that calls go(true) after it, ignoring the floor. So 20 s after a wrong answer the game moves on whether or not the student has finished reading or writing the method down. The docstring (:11-12, :46-48) and canon §7.6 (docs/canon.md:1129-1140) call it a safety net "so a walked-away tab still finishes".
- Seven pages already defeat it with the longest delay setTimeout takes or a day: the-6-ps/index.html:347 and :1173; games/take-a-walk/index.html:942 and :1371; games/squared-squirrel/index.html:810 and :1044; games/just-pythag-it-bruv/index.html:977 and :1183 (its worked example only); games/how-many-parts/index.html:1253 and :1621; games/52dle/index.html:1566; games/distinctly-average/index.html:1487-1488. A game left waiting costs nothing; a student cut off mid-method loses the lesson.

CLASS CHECK: A class: the same workaround in seven pages against one default in a shared helper used by 89 games (the defensive-patch shape). The fix is the helper's default, once; the seven workarounds then go, so no page carries its own.

EXACT CHANGE:
1. schools/assets/next-control.js:
   - No automatic advance by default: with no fallbackMs given, no fallback timer is set; the control waits for a click, Enter or Space, or the game's own advance(), after the floor.
   - fallbackMs stays as an option for test harnesses only (scripts/test-next-control.py, scripts/check-answer-lock.py:1298, scripts/verify-stage-exit.py:201, scripts/verify-just-pythag-it-bruv.py:889 use it). Remove FALLBACK_MS from the exported api (:230) only if nothing reads it; otherwise export null and say why.
   - Docstring (:1-48): rewrite the fallback sentences to say a wrong answer waits for the student, with no timer, and why (Jon, 27 Nov 2026), and that fallbackMs is for tests.
2. The seven pages above: remove each NO_FALLBACK constant (or the day-long literal) and the fallbackMs it passes. Nothing else in those pages changes.
3. A guard, in CI (scripts/test-next-control.py or an existing static check: name it in the report): no page under games/, escape-rooms/, the-6-ps/ or the site root passes fallbackMs to MaffsNext. Plant: a page passing fallbackMs: 20000 must FAIL. test-next-control.py gains a case: with no fallbackMs, no advance after 60 s (on a fast clock if it has one); plant: a default fallback restored must FAIL. Its existing fallback cases keep passing by passing fallbackMs explicitly.
4. docs/canon.md §7.6 (:1129-1140):
   - Replace the fallback sentence: a wrong answer waits for the student with no timer (Jon, 27 Nov 2026: time to check where they went wrong and write the correct method down).
   - Add: "A right answer that reveals something new on screen (a drawn result, a graph, a worked line the question did not show) waits for Next as a wrong answer does; a right answer that only confirms keeps its brisk delay." (Jon, 27 Nov 2026, for d by dx? Why?'s gradient function.)
5. /updates/: one line in plain words (every game now waits for Next after a wrong answer, however long the student takes). docs/handover/home.md entry.

DO NOT TOUCH:
- The floor (FLOOR_MS, 3 s), the in-view scroll (NEXT-IN-VIEW), advance-once, clear(), the 44 px target, MaffsLock.
- Right-answer delays in every game (d by dx's Next on a right answer is part of its graph build, not this contract).
- Every game's other code; the harnesses' own uses of fallbackMs; every workflow; scripts/merge-pr.py; scripts/serve-stubbed.py and scripts/ci-deps.py (the cloud lane's PINNED-LIVE-DATA is working there); docs/handover/cloud.md.
- No force-push.

SUCCESS CONDITION:
- On every page, a wrong answer's Next waits indefinitely after the floor; no page passes fallbackMs; the guard and both plants run in CI.
- Every existing check passes in CI (any verifier that waited on the 20 s default to finish a run is listed in the report with how it now advances).
- Canon §7.6 as in step 4; /updates/ line; merged on green through python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600, run from main's checkout, not the PR's (merge main in and re-run if main moves first; the new freshness check will refuse otherwise); last line and main's run IDs in home.md.

STOP IF:
- A verifier or check relied on the 20 s default to advance and cannot be given fallbackMs or its own advance without changing what it tests: report it.
- Any game's page advances a wrong answer by a timer of its own, outside MaffsNext: list it in the report; do not change it here.
- main is red when you come to merge: report it; do not use --override.
- merge-pr.py cannot reach GitHub or refuses: report its output; do not merge another way.
