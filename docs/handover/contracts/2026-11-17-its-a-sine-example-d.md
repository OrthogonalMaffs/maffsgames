Recommended: Sonnet, low effort — two data edits and a verifier re-run.

Follow-up, to start only AFTER #812 has merged and you have reported its last line, merge commit and main's run IDs. New branch and PR from the new main.

TASK: Replace worked example D's triangle with a clearly obtuse one, and remove two false keywords from its-a-sine's games.json entry.
ROOT CAUSE: Project Claude's contract chose 8, 9, 12 cm for example D without checking its largest angle (C = 89.6°), so it looks right-angled, against Jon's 10:48 instruction. games.json still tags the game "ambiguous case" and "bearings"; no question uses either since the Level 3 bank was replaced.
CLASS CHECK: Local. One example's data and one game's keyword list; no shared code involved.
EXACT CHANGE:
 1. games/its-a-sine/index.html, worked example D (letter 'D', version 'cosine-angle'): given becomes a = 7, b = 6, c = 11 (cm), still find A.
    setup: \(a = 7\text{ cm}\), \(b = 6\text{ cm}\), \(c = 11\text{ cm}\). Find \(A\).
    work: \(\cos A = \frac{6^2 + 11^2 - 7^2}{2 \times 6 \times 11} = \frac{108}{132} = 0.81818\ldots\), so \(A = 35.1^\circ\).
    answer: '35.1'; item.given { a: 7, b: 6, c: 11 }. Title, "why" line and links unchanged.
 2. data/games.json, slug its-a-sine: delete the keywords "ambiguous case" and "bearings". Nothing else in the entry changes.
 3. Update the verifier's expected values for example D so it recomputes these from first principles (A = 35.0968…°, cos A = 9/11 truncated to 0.81818).
DO NOT TOUCH: Examples A, B and C; any bank item; the drawing and unit code; the bearing-drawing code (now unused, kept on purpose); any other games.json entry; canon.
SUCCESS CONDITION: Example D's diagram is visibly obtuse at C (115.4°); the verifier passes with D's new numbers and catches a planted fault in D's answer; games.json has neither keyword for its-a-sine; Gate green and merged via scripts/merge-pr.py; handover/cloud.md records the merge commit and main's run IDs.
STOP IF: The triangle 7, 6, 11 already appears in any bank item; or games.json validation in CI expects a minimum keyword count that removing two would break.
