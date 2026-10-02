Status: READY, not started. Dictated by Jon 27 Sep 2026, verbatim below. Context will be
cleared before this build starts — this file is the full brief, not a summary.

TASK: Rebuild quadratic-factoriser into three levels — factorise a=1, factorise a>1 with a
fading AC-method tutorial, and solve with the quadratic formula — as the first game whose
questions are machine-verified.

ROOT CAUSE: The live game covers a=1 only (10 questions, level hard-coded 'gcse' at :711,
:756, :768). GCSE needs a>1 factorising (split the middle term) and the quadratic formula,
and neither exists on the site as a game. Jon teaches the AC method: a×c is the product, b is
the sum; split bx; factorise in pairs; take out the common bracket.

CLASS CHECK: Not a bug class — a rebuild of one game. But it is built to the proposed new-game
standard so it can prove it: finite enumerated pools (no rejection sampling), shared helpers
(MaffsSession, MaffsNext, MaffsText), and its own layer C/D verification script.

EXACT CHANGE:

0. docs/quadratic-factoriser-spec.md — this contract's design, verbatim, before any code.

1. Structure. Same slug, same file. Three levels selectable on the start screen and by
   ?level=: 'gcse' = factorise a=1 (keeps the existing leaderboard/PB key and analytics
   history); 'higher' = factorise a>1; 'formula' = quadratic formula. Every mfg() event and
   submitScore() uses the real level (fixes the hard-coded 'gcse'). Session lengths via
   MaffsSession; wrong answers via MaffsNext with the worked solution shown first (§7.6);
   every string mixing prose and maths via MaffsText; all maths in KaTeX. Dark GCSE+ theme
   (§7.5.1 — lowest tier served is GCSE). Aa toggle kept.

2. Pools — enumerated once at load, deduplicated, shuffled, sliced. NO draw-and-retry loop.
   'gcse' (a=1): (x+p)(x+q), p,q ∈ ±1..±9, b ≠ 0 except in the difference-of-two-squares
     stage (x²−k², k 1..12). Stages: both positive → one negative → both negative → DOTS.
     Answer: the existing bracket picker; accept either bracket order.
   'higher' (a>1): (px+q)(rx+s), p,r ∈ 1..6 with pr ≥ 2 and pr ≤ 12, q,s ∈ ±1..±9,
     gcd(p,q)=gcd(r,s)=1 (no hidden common factor), b ≠ 0, |ac| ≤ 72. Later stage only:
     k(px+q)(rx+s), k ∈ 2..5 — student must take out k first.
     Answer: coefficient pickers for (□x ± □)(□x ± □), plus an outer-factor picker in the
     HCF stage. Mark by EXPANDING the student's brackets and comparing a, b, c — never by
     string — so bracket order does not matter. Display the answer with positive leading
     coefficients.
   'formula': ax²+bx+c=0, a ∈ 1..5, b,c ∈ ±1..±9. Mostly non-square discriminants; ~15%
     negative discriminant, answered with a "No real solutions" button. Exclude any item
     with a root within 1e-6 of a 2 d.p. rounding boundary (filtered from the pool, not
     retried). Answer: two inputs, any order; a root is correct iff the input equals the
     root rounded to 2 d.p. (so 1.2378 accepts 1.24, not 1.23).

3. The 'higher' tutorial — Tutorial → Guided → Independent, fading per CLAUDE.md
   "Scaffolds fade". Tutorial walks one worked example with the student doing each step:
     1 identify a, b, c;  2 work out a×c;
     3 pick the pair from a factor-pair table of |ac| with signs — multiplies to ac, adds
       to b. Named misconception if the pair multiplies to c instead of ac;
     4 split: rewrite as ax² + mx + nx + c (either order accepted, and say so);
     5 factorise each pair. Named misconception when the second pair's brackets do not
       match the first because a negative factor was not taken out ("the two brackets must
       be identical — check the sign of the number you took out");
     6 take out the common bracket.
   Guided: same six steps, with prompts but no worked example. Independent: answer only,
   steps available behind a "Show me the method" control that does not count as a fail.
   Move from Guided to Independent after 2 correct in a row; back after 2 wrong in a row.

4. 'formula' feedback: on a wrong root, if it equals one of these, name it before the
   working — used +b instead of −b; divided only the square root by 2a; divided by a not
   2a; took b² as negative when b < 0. Otherwise show the full substitution.

5. scripts/verify-quadratic-factoriser.py (layers C + D, run in CI):
   enumerate every pool exactly as the game does (same parameters, exported from the game
   as a JSON-able config, not duplicated by hand) and assert with SymPy: every factorised
   form expands to its quadratic; no 'higher' non-HCF item has a common factor; every
   'higher' item has exactly one unordered {m,n} pair with mn=ac, m+n=b; every 'formula'
   root matches SymPy's roots to 1e-9; negative-discriminant items are flagged as such;
   no item sits on a rounding boundary; every pool ≥ 40 items per stage. Fail CI on any
   violation.

6. Roster, portal card and meta description: levels become GCSE (a=1), GCSE Higher
   (a>1), Quadratic formula; description rewritten to match. data/check-ledger.json
   updated by check-banks.

Commit after each phase and run the full checks before each commit:
   Phase 1: items 0, 1 and 'gcse'.  Phase 2: 'higher' with the tutorial.
   Phase 3: 'formula'. Item 5 grows with each phase; item 6 in phase 3.

DO NOT TOUCH: Any other game. The shared helpers (use them; if one is missing a
capability, STOP — do not fork it). firebase-leaderboard.js. The existing 'gcse' leaderboard
key. Other portal cards.

SUCCESS CONDITION: Per phase — verify-quadratic-factoriser.py passes; every level plays to
game_completed at every offered length (scripted, stub server); the 'higher' tutorial
steps through a full example, and each named misconception fires on its trigger (scripted);
tiers 1+2 green; tier 3 --only quadratic-factoriser PASS or UNSUPPORTED; check-banks --ci
green; pushed; --live PASS. Report screenshots of: each level's first question, every
tutorial step, one misconception message, and one formula worked solution.

STOP IF: A shared helper lacks something the game needs. Any pool falls below 40 at any
stage under these constraints (report the count; do not loosen the constraint). The
existing 'gcse' PB/leaderboard key would change. Any checker FAIL.
