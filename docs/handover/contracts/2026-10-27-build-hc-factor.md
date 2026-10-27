TASK: Build "The HC Factor": expanding and factorising, from single brackets to factorising x² + bx + c with Jon's sign grid, with typed answers in bracket-shaped number boxes and a talent-show theme. Unlisted.

ROOT CAUSE: New build for the priority audience (Jon, 23 and 27 Oct 2026). Expanding and factorising carry 32 of 1,800 OCR Foundation marks over 18 papers, and factorising/solving quadratics 18 more; there is no game for single brackets or double-bracket expansion. Jon drills a sign grid for factorising: same signs means c is positive, different signs means c is negative.

CLASS CHECK: Not a bug. Bank-first (canon §8.2.1): the question generator lives in its own module that the game imports (and the 6 P's could later import); every answer is computed, correct by construction, and checked by a verifier through a separate code path. The bracket-shaped answer boxes are built in the game; if they would be useful elsewhere, report that rather than changing shared files.

EXACT CHANGE:
1. Generator module (new file, e.g. schools/assets/hc-factor-gen.js), at least 30 distinct questions per stage, fixed seed.
2. Stages, each played one at a time, easiest first:
   S1 Expand: k(x + a), k 2–9, a ±1–9.
   S2 Expand with negatives and x outside: −k(x − a), x(x + a), kx(x + a).
   S3 Factorise fully into one bracket: e.g. 6x + 9 → 3(2x + 3); 4x² + 6x → 2x(2x + 3). Positive HCF only.
   S4 Expand double brackets: (x + a)(x + b), a, b in ±1–9, not both zero.
   S5 The sign grid: given x² + bx + c, choose the signs of the brackets (both +, both −, one of each) and score a mark for it on its own. Feedback states the rule: same signs when c is positive (both the sign of b); different signs when c is negative.
   S6 Factorise x² + bx + c (a = 1): the sign-grid choice first (marked), then the numbers.
   a > 1 is NOT in this game (Quadratic Factoriser covers it).
3. Answers are typed numbers in boxes laid out as the bracket: ☐(☐x + ☐), ☐x(☐x + ☐), x² + ☐x + ☐, (x ☐ ☐)(x ☐ ☐), with a sign toggle where a sign is needed. No algebra keyboard. Marked by value: both orders of the two brackets accepted; in S3, an equal but not fully factorised answer (e.g. 2(2x² + 3x)) gets the "factorise fully" format message, not "wrong".
4. Named wrong answers (slip lines matched by value): k(x + a) → kx + a (multiplied the first term only); −k(x − a) → −kx − ka (sign of the second term); x(x + a) → x² + a; partial factorising; (x + a)(x + b) → x² + ab (missing middle term) or x² + (a + b)x + (a + b); sign grid: same signs chosen when c is negative; both + chosen when b is negative; S6 pairs that multiply to c but add to −b.
5. Worked lines for every question: S4 by the grid method; S5/S6 show the sign grid, then "two numbers that multiply to c and add to b".
6. Theme (Jon: "you're through to the next round"): a generic talent show, a stage under lights, a panel of three judges whose "yes" cards light up for right answers, "You're through to the next round!" between stages. Dark theme row (lowest tier served is GCSE, canon §7.5.1). No real programme's logo, music, set design, catchphrases or judges' names (an original show, not an imitation). Copy plain and adult; Jon adds jokes later.
7. Game page games/hc-factor/ (new folder); theme.css and the shared components as they are; KaTeX for expressions; the phone-fit rules in canon §7.6 at the three phone sizes and 1366 × 768 / 1280 × 720, with the answer boxes and Next above the fold; any figure text at least 12 px; analytics with existing events only; a leaderboard per stage by existing conventions (if a board needs a shared-file change, leave it off and report). Unlisted.
8. Verifier (new file): for every generated question, recompute the expansion or factorisation independently (polynomial multiplication), check the sign-grid answer against c and b, check every slip value differs from the answer, and that S3 answers are fully factorised. Plants, each caught: an expansion with the wrong middle term; a sign-grid answer contradicting c; a partial factorisation accepted as correct in S3.
9. Merge once CI and main are green, write docs/handover/build.md, and report with screenshots at 375 × 667 and 1366 × 768 for Jon (one of each stage). Then stop, or start the next queued contract.

DO NOT TOUCH: Any shared file (see your lane rules), except the minimum a site-wide check demands for a new game folder, marked unlisted and reported. Quadratic Factoriser. The 6 P's. Other games. What analytics collects.

SUCCESS CONDITION: All six stages play end to end on a phone and a laptop with typed answers in bracket-shaped boxes; both bracket orders accepted; partial factorising gets the format message; the sign grid is marked as its own step; the verifier passes with all plants caught. Unlisted, merged, main green, screenshots reported.

STOP IF: A stage can't generate at least 30 distinct questions in its ranges. The bracket boxes can't fit a 320 × 568 phone with the question and Next visible (park, report with screenshots, start the next job). The design needs a shared-file change beyond the minimum for a new game folder.
