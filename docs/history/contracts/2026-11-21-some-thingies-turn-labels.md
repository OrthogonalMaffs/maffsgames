# Contract SOME-THINGIES-TURN-LABELS (Project Claude; Jon, 21 Nov 2026), verbatim: the 20:09 reissue (amendment 1), which replaces the 20:08 text

SOME-THINGIES-TURN-LABELS. Home lane. REISSUED IN FULL (amendment 1, Jon, 21 Nov 2026, 20:09: "any way of making the thingies stay eyes up as it rotates?"), replacing the 20:08 text. If you've started, carry on from where you are; step 3 is the only addition.
Recommended: Claude Code, Sonnet, low effort. One game, a few lines of CSS and JS, plus verifier cases.

TASK: In Stage 3's turn: (a) hide the scaffold's labels ("R rows", "C in each row") before the array turns, so the rotating array never clips or overlaps them; (b) keep every thingy upright (eyes up) throughout the turn.

ROOT CAUSE: turnArray() (games/some-thingies/index.html:1205-1210 on 8bf4b4e) adds .arr.turning (rotate(90deg), :141) while the labels #arrSide and #arrTop (set by labelArray(), :931) are still showing beside and above the array in .arr-wrap (:133). The rotating array sweeps across them, and Jon sees the wording clipped mid-turn. The same rotate(90deg) on the whole array also turns every thingy on its side mid-turn (Jon, 20:09).

CLASS CHECK: Local. One game's turn animation, its own labels and its own thingies.

EXACT CHANGE:
1. First commit: the standing close-out for #868 SOME-THINGIES-PERSONALITY (merge commit 8bf4b4e, merge-pr.py, its main runs incl. phone-fit-full with some-thingies' result in each mode), per AGENTS.md. Jon accepted the conga fallback at 320 px (21 Nov, 19:46).
2. In turnArray(): fade both labels out (opacity to 0 over about 120 ms) and only then start the rotation, so the labels are fully gone before the array moves. With reduced motion, clear them at once (there is no rotation). After the turn, the redrawn array shows no stale label (a label must never show the pre-turn numbers on the turned array).
3. Upright thingies: while .arr.turning rotates the array 90° clockwise, counter-rotate each cell's thingy 90° anticlockwise about its own centre (transform-origin: centre; transform-box as needed for SVG), with the same duration and easing, so every thingy stays eyes-up throughout. After the turn the array is redrawn as now, with the thingies upright and no leftover rotation. Accessories (hats, hair) stay upright too, as they're part of the same thingy.
4. Use the game's existing timer (MaffsLock.timer) so nothing fires after the student has moved on; Next and the answer lock are never delayed.
5. Verifier: at the moment the turn starts, both labels are hidden (opacity 0 or empty); after the turn, no label shows the old rows or columns; mid-turn, each thingy's net rotation is 0° (array +90°, thingy -90°), sampled at least once halfway. Plants: labels left visible during the turn; a thingy not counter-rotated. Each must be caught.
6. Merge on green via scripts/merge-pr.py, then the standing close-out.

DO NOT TOUCH: The scaffold's steps and scoring, the turn's timing beyond the short fade, the array's layout and colours, the bank, anything outside games/some-thingies/ and its verifier.

SUCCESS CONDITION: Watching a Stage 3 turn, the labels vanish just before the array rotates, with no clipping, and every thingy stays eyes-up throughout, on laptop and phone. The verifier catches both plants. CI is green and the PR is merged.

STOP IF: The fade or the counter-rotation would delay Next, marking or the answer lock. The counter-rotation can't keep the thingies upright in a browser phone-fit uses (report which). Main goes red for a reason outside this change (one rerun per AGENTS.md, then stop and report).
