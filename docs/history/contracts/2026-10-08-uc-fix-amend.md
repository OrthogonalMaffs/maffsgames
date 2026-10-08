# Amendment to UC-FIX, and the Screening Room t4-017 ruling (verbatim)

From Project Claude, pasted by Jon, 8 Oct 2026, 23:45 (Jon ruled "both yes" at 23:39). Saved verbatim under Jon's standing rule
(corrected 20:00): read this file when the item starts, not at session start; it moves to `docs/history/` when the work
merges.

```text
AMENDMENT TO UC-FIX, plus a ruling on Screening Room t4-017 (Project Claude, 8 Oct
2026, 23:45; Jon ruled "both yes" at 23:39). Save this verbatim beside the UC-FIX
contract in docs/handover/contracts/ before starting UC-FIX.

1. Screening Room t4-017 (Jon's ruling): one question_answered row per answer is
   correct. Each item asks for two answers, the gut check and the worked figure, and
   logging both shows where a student goes wrong. Keep the current behaviour. Record the
   ruling on t4-017 in the next screening-room findings edit you make, or in the UC-FIX
   PR if no screening-room PR comes first; one line in the resolution, no code change.

2. UC-FIX gains t4-005 (Jon's ruling): the score depends on correct answers only, and
   the timer is hidden, as canon's timer policy says (a hidden count-up). Changes to
   UC-FIX:
   - EXACT CHANGE, new step 5a: hide the HUD timer. The CSS currently hides .timer, not
     #timer; hide the element actually shown. Any count-up may continue invisibly if
     the game logs it. Change the score so it depends only on correctness: one fixed
     amount per correct answer, with no time factor and no speed bonus. If the game has
     streak or bonus rules that do not use time, keep them. Remove time from the score,
     the end screen and the leaderboard submission.
   - Step 7, verifier: add checks that no element showing the elapsed time is visible
     during play, and that two sessions with the same answers at different speeds score
     the same. Plant a time-weighted score in the self-test; it must fail.
   - Step 8: close t4-005 as well, citing Jon's ruling.
   - DO NOT TOUCH: remove the line excluding the timer and the score's use of time.
     Leaderboard DATA stays untouched.
   - STOP IF, added: the new scores are on a different scale from the boards'
     existing entries, so old speed-weighted scores would sit above anything now
     possible. Do not stop the work for this: finish the PR, then report in the PR and
     the handover each board key (unit_converter_<level>) and the new maximum score, so
     Jon can check the boards and decide whether to clear them. Clearing is Jon's call,
     in the Firebase console. Never delete or move scores.
   Everything else in UC-FIX stands.
```
