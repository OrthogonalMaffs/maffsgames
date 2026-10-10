CONTRACT FOR THE CLOUD LANE: LISTED-HIGH (Project Claude for Jon, 9 Oct 2026, 14:00). Save verbatim as docs/handover/contracts/2026-10-09-listed-high.md before starting. Standing rules apply: one game per PR, each game claimed on cloud-remaining: in its own commit first, merge on a green Gate with main green, watch main, then the next game without asking. Stop only for a STOP IF, or after the last game.
====================================================================== TASK (cloud lane, LISTED-HIGH): Close every open CRITICAL and HIGH finding on listed games, game by game, wrong answer keys first, so no live game marks a right answer wrong or a wrong answer right.
ROOT CAUSE: 25 CRITICAL/HIGH findings are open on listed games (docs/audits/findings/*.yml, main 8def243; glorious-gantt is unlisted and excluded). They fall into three kinds: (a) wrong maths or wrong marking on live games; (b) six judgement calls, now ruled by Jon (below); (c) answer-lock findings already fixed on main by the home lane's F1 batches 7-11 (MaffsLock) but never closed.
CLASS CHECK: Each item is local to its game's content or marking, and is fixed in that game with its verifier, per canon. Two are instances of a class the site already has a rule for:

* equivalent answers marked wrong (boolean-blitz, coordinate-geometry- dash, complex-converter, higher-power): the rule is SR-13/SR-17, and every equivalent correct answer is accepted. Fix each by marking on value or equivalence in that game, never by deleting the equivalent form.
* unstated conventions (scale-factor-scaling, core-maths-paper2c, wrong-on-the-internet, complex-converter's angle range): state the convention in the question. If any fix would need a shared asset, stop and report it (home lane's).

ORDER AND EXACT CHANGE (one PR per game, in this order):

1. surd-simplifier
   * t1-001: 8/√32, "Rationalise and simplify": the key is √2 (8/√32 = 8/(4√2) = 2/√2 = √2). The current key "√2·√2" equals 2: make √2 the key, and keep "√2·√2" only if it stands as a distractor whose value is 2.
   * t1-002: 0.41616… = 0.4161616… = 412/990 = 206/495. Key 206/495. Make sure exactly one option equals it. Verifier: recompute every key exactly (fractions, surds by SymPy).
2. 52dle (t2-001): compare the typed value exactly; no parseInt truncation. 23.9 must not match 23. Verifier plants it.
3. scale-factor-scaling (t1-001): state the original quantity the question needs, chosen so the existing key is right (doubling dimensions multiplies area by 4). Apply the same check to every item in the bank: no item may depend on a quantity it doesn't state.
4. coordinate-geometry-dash (t1-001): x = 3t, y = 4/t: xy = 12, y = 12/x and x = 12/y are all correct. Rewrite the options so exactly one is correct (keep one correct form; replace the others with genuine errors such as xy = 7, y = 12x, x = 3y/4), or mark any equivalent correct option right. Exactly one option may be keyed correct, and no unkeyed option may be correct.
5. complex-converter (t6-001): state the convention in the question: "give θ with −180° < θ ≤ 180°" (principal argument). Apply it to every item, and check that no item's options contain two forms of the same number.
6. higher-power (t2-001): Pairs mode matches by value, not pairId: 2⁸ with any card worth 256 is a match.
7. seven-bridges (t4-001, t4-002): cancel the solution animation when a puzzle changes (it traces onto the next one); redraw the graph so no edge passes through a vertex it doesn't join (E must not sit on AC or BD). The graph's degrees and the answer are unchanged.
8. wrong-on-the-internet, Jon's rulings:
   * t2-001: the post states a European single-zero wheel; the key becomes 18/37. Keep "Depends on the wheel" only if, once the wheel is stated, it is plainly wrong.
   * t2-002: the post states that A and B are independent, so 0.12 stands and "Need more information" is wrong.
9. core-maths-paper2c, Jon's rulings:
   * t4-002: add "f is a quadratic" to the question, so the minimum at x = 4 by symmetry holds.
   * t4-003: rewrite option D ("Yes - but only when k > 0") so it is a false statement, keeping it as a plausible error.
   * t4-001 (double-tap on Next): check it on main (MaffsLock, F1 batch 7). If fixed, close it with the evidence.
10. core-maths-paper2b (t2-001, Jon's ruling): rewrite option D so it does not pick the same policy as the key.
11. boolean-blitz (Jon's ruling, t6-002, t6-003): accept any expression with the same truth table as the key (AB + BC for B(A + C); AB + AC for A(B + C)). Mark by truth table over all inputs, in the game. t6-001: check it on main (F1 batch 11), and close it with the evidence if fixed.
12. prisoners-dilemma (t4-002 only): typing initials in the leaderboard overlay must not play moves. Keyboard play is ignored while the overlay is open. Leave t4-001 (the board ranks whichever opponent is chosen) open: it's a design decision for Jon.
13. Stale lock findings: characteristic-quest t6-001, eigenvalue-extractor t6-001, matrix-crunch t6-001 and t6-002, formula-forge t4-001. For each game, check on main that the fault is gone (the lock check passes, and the finding's own reproduction no longer reproduces). Close it in a small PR per game with that evidence. If one still reproduces, fix it as in the batches. For every game: its verifier gains a check that fails main's page for each fixed finding (plant the old content in the self-test); close the findings citing this contract or Jon's ruling; take the game off cloud-remaining: in its PR; handover updated.

DO NOT TOUCH: any item not named in its finding; shared assets and scripts (calculator, answer lock, analytics, leaderboard module); canon, the roster and todo (the home lane's); glorious-gantt; prisoners-dilemma-t4-001; leaderboard data.
SUCCESS CONDITION: no open CRITICAL or HIGH on any listed game, except prisoners-dilemma-t4-001; each game's verifier passes and fails on main's old page for its fixes; every PR merged on a green Gate with main green after it; handover current, listing each PR.
STOP IF: a recomputed key in any game differs from its stored key in a way no finding covers (a new wrong answer: list it, and fix it in that game's PR if it is unambiguous, otherwise stop for Jon); a fix needs a shared asset; a ruled rewrite cannot be made without changing the key (quote it); CI group E has no room for a verifier you need to add (it's at 8m39s of 9m; report it, and add the check to the game's existing verifier where possible rather than a new one).
