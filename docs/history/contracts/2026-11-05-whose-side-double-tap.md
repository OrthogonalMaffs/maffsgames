WHOSE-SIDE-DOUBLE-TAP. Jon's second play-test, verbatim. "New PR from main": #675 was still open and its slots are not on main, so this branch starts from #675's head (963e4fd5) and depends on it.

JON'S PLAY-TEST 2 (5 Nov 21:40), thank you. Bug: a side can be tapped into both slots, so an accidental double click puts the same side top and bottom and costs the streak.
Fix: a side already in a slot cannot fill the other slot: tapping it again does nothing (it stays where it is; emptying is still by tapping the slot). Also, on every stage, a tap is ignored while an answer is being marked or its feedback is showing, so a double click can never answer twice or carry into the next question.
If not already in: Stage 2's prompt reads "[OPP] over [HYP]: tap the top side, then the bottom. Tap a box to empty it, then press Check." (coloured words as now).
Verifier: a double click on one side fills one slot only; a double click on a Stage 1 side answers once; plant the old behaviour and require it caught. New PR from main, stop at a green Gate and report.

Addition to the double-click fix (Jon, 5 Nov 21:57), thank you: on a right answer, hold for 0.8 s with the side(s) lit in colour and "✓ Right" showing, then go to the next question automatically (no Next button). The clock pauses during the hold, so the score is unaffected; taps during the hold are ignored (as in the double-click fix). Wrong answers keep their feedback and Next button as now. Verifier: a right answer shows the lit side and "✓ Right" before the next question appears, and the clock does not run during the hold.
