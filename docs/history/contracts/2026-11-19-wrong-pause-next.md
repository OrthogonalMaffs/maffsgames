WRONG-PAUSE-NEXT, one part.
LANE: home. Send now. TIER: Medium. MODEL: Claude Code, Opus 5.5, high effort (four games plus a CI guard used by every game).

TASK: The four games whose wrong answer moves on by itself pause on Next and show the answer, and CI fails any game that stops pausing on a wrong answer.

ROOT CAUSE: Found by #838's corrected survey (docs/handover/cloud.md), confirmed in the code on main 233ce57. On a wrong answer these advance with nothing to read and no Next (canon 7.6): binomial-blaster handle() :247 and partial-fractions-duel handle() :167 call MaffsLock.timer(adv,1000) for right and wrong alike; trig-identity-duel :290 the same; word-problem-decoder :806-812 fades out after 800 ms and shows the next phrase. None loads schools/assets/next-control.js. Nothing in CI checks that a wrong answer pauses.

CLASS CHECK: A class with no guard. Fix the four with the shared control (MaffsNext.wrong), and add the guard where every game is already played: scripts/check-answer-lock.py's in-play run.

EXACT CHANGE:
1. First commit: close out #837 NEXT-IN-VIEW (merge 9da4073, run 44591763818) and #839 DD-VERIFIER-SHARD (merge f2e6d2a, run 44580613966) in docs/handover/home.md: read main's runs on each merge commit from the API, record them, and move both contracts from docs/handover/contracts/ to docs/history/contracts/. Save this contract verbatim as docs/handover/contracts/2026-11-19-wrong-pause-next.md.
2. binomial-blaster, partial-fractions-duel, trig-identity-duel: load next-control.js as the other MaffsNext games do; a right answer advances as now (1000 ms); a wrong answer shows "The answer:" and the key (KaTeX, as the option is drawn) in the game's feedback area above Next, then MaffsNext.wrong({mount, onAdvance: adv, keep: that feedback}); MaffsNext.clear at the top of showQ.
3. word-problem-decoder: a right answer as now. A wrong answer shows the right topic and highlights the item's own "highlights" phrases in the question text (data already on every item), then MaffsNext.wrong; the fade runs when Next advances. Read-aloud/Aa behaviour unchanged.
4. scripts/check-answer-lock.py, in-play: for every game it plays, answer one question wrong and assert that within 2 s a Next control appears (MaffsNext's, or a game's own Next listed in a new OWN_NEXT dict with a one-line reason) and the question does not change for 2 s while Next is not pressed (the auto-advance timers found are 800-1000 ms). Games that cannot be judged (expectation-station, maths-court, tax-theft: staged flows the survey could not trace; and any game the run cannot drive to a wrong answer) go in a new WRONG_PAUSE_UNCHECKED list, reported never failed, which may only shrink. Plants that must FAIL: a game's wrong path back to MaffsLock.timer(adv,1000); a Next that advances by itself in under 2 s. The extra time stays inside each game's existing work unit, so ci-groups.py re-picks the number of parts from the new times.
5. todo: one row WRONG-PAUSE-UNCHECKED pointing at the list. Close nothing else. One /updates/ line: "Four games now wait for you after a wrong answer, so you can see what the answer was." home.md entry.
6. PR, Gate and phone-fit-full green, merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600; report its last line.

DO NOT TOUCH: the four games' questions, keys, options, marking and scoring; schools/assets/ (use next-control.js as it is); other games' code; docs/handover/cloud.md; the cloud lane's open PR and its files (the core papers, surd-simplifier, circle-theorem-spotter, standard-form-blitz).

SUCCESS CONDITION: the four pause on Next after a wrong answer and show the answer (word-problem-decoder also its clue words); the new check passes on every judged game and both plants fail; WRONG_PAUSE_UNCHECKED and OWN_NEXT are explicit and documented; #837 and #839 closed out; merged GREEN; home.md records it all.

STOP IF: check-answer-lock.py's in-play run cannot answer wrong without a per-game driver for more than a handful of games (report how many, and propose where the guard should live instead); a game other than the four fails the new check (list them; don't fix them here); after repacking, any lock part is over its per-line budget; a phone-fit size the four fit now is lost; merge-pr.py can't reach GitHub; anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies (report under "Decided for you").
END OF CONTRACT
