Status: READY, not started. Drafted by Project Claude 27 Sep 2026; decisions by Jon (extend Log
Laws; log₁₀ and ln; 3 s.f.; build after quadratic-factoriser). Real class need: Jon's Level 3
group, Lesson 5 (see docs/level3-sow-mapping.md), within two weeks.
**Step 5 was corrected by Jon on 28 Sep 2026 and amended by him again the same day**, adding a
`level3` key after all. Both are verbatim at the end of this file. They override step 5, and the
later one wins where they differ. Jon also confirmed the class date, **w/c 12 Oct 2026: this must be
live before then.** Queued after Chart Interrogator Contract B, by Jon's decision of 28 Sep.

TASK: Add a "Use the laws to solve" mode to Log Laws, in which students apply the product, quotient, power and special-value laws step by step to solve equations — the power law above all.

ROOT CAUSE: Log Laws drills recognising the laws (45 questions: power 9, product 8, quotient 8,
change of base 7, combined 7, special values 6) but never asks a student to use one to solve an
equation. Jon's Level 3 class (SOW Lesson 5) must apply each law — especially bringing the power
down to solve aˣ = b — and does not study change of base. docs/level3-sow-mapping.md marked
Lesson 5 "covered"; it is covered for recognition only.

CLASS CHECK: Not a bug class — a content gap in one game. Built to the new-game standard:
enumerated pools, shared helpers, its own layer C/D verification.

EXACT CHANGE:
0. Keep the existing drill as the "Laws" mode, unchanged, plus one start-screen option:
   "Skip change of base" (on by default in the new mode, which never uses it).
1. New "Solve" mode. Each question is a chain of steps. At every step the student picks the
   move from: Take log₁₀ of both sides · Take ln of both sides · Power law · Product law ·
   Quotient law · log_a a = 1 / ln e = 1 · log 1 = 0 · Undo the log (10^ or e^) · Rearrange.
   The game shows the resulting line (KaTeX, via MaffsText for mixed lines). A wrong move
   gets a named reason ("the power law moves an index to the front — there is no index here")
   and stays on the same step. The final answer is typed to 3 s.f. and is correct iff it
   equals the true root rounded to 3 s.f.
2. Families, each an enumerated pool of ≥ 40 items (no draw-and-retry), in this order:
   F1 aˣ = b (a 2..9, b not a power of a), log₁₀: take logs → power law → divide.
   F2 a^{kx} = b and a^{x+k} = b: power law then rearrange.
   F3 e^{kx} = b and engineering forms V = V₀e^{−t/RC} (solve for t): take ln → ln e = 1 →
      rearrange. Realistic component values; units stated.
   F4 quotient law: log(x + a) − log x = log b → (x + a)/x = b → x.
   F5 product law: log x + log(x + k) = 1 (log₁₀) or = log m → quadratic with integer roots →
      a "Which solution is valid?" step rejecting the root that makes a log argument ≤ 0,
      with the reason shown.
   F6 two bases: aˣ = b^{x−k} → power law on both sides → collect x → factorise → divide.
   Stages run F1→F6; the session mixes earlier families once later ones unlock.
3. Pools exclude any item whose root is within 1e-6 of a 3 s.f. rounding boundary (filtered,
   not retried). ln and log₁₀ only; no other base appears anywhere in Solve mode.
4. Wrong final answer: show the full worked chain first, then MaffsNext (§7.6). Named
   misconceptions checked before the working: divided the logs' arguments (log 20/log 3 taken
   as log(20/3)); forgot the coefficient k from the power law; kept the invalid root in F5.
5. Session lengths via MaffsSession. Levels: the existing A-Level and L4 keys both offer
   both modes; analytics and submitScore carry mode ('laws' | 'solve') and the real level.
   Leaderboard: Solve mode submits under mode 'solve' only once the leaderboard-modes contract
   lands; until then Solve mode is held off the board (LEADERBOARD_MODE_READY pattern) and
   coverage-check HELD records why.
6. scripts/verify-log-laws.py (layers C + D, in CI): enumerate every Solve pool from the game's
   exported config; with SymPy assert each step's line is equivalent to the previous on the
   valid domain under the named law; the final root matches SymPy's solution to 1e-9; F5's
   rejected root really makes an argument ≤ 0 and the kept one does not; no rounding-boundary
   items; every pool ≥ 40. Fail CI on any violation.
7. Roster and portal card: add "Solve mode — apply the laws" to the description; meta
   description updated. docs/level3-sow-mapping.md Lesson 5: note Solve mode closes the gap.

DO NOT TOUCH: The existing Laws-mode bank and its marking. Any other game. Shared helpers
(STOP if one lacks something). firebase-leaderboard.js.

SUCCESS CONDITION: verify-log-laws.py passes; each family plays to game_completed at every
offered length (scripted, stub server); every named wrong-move reason and misconception
fires on its trigger (scripted); Laws mode is byte-identical in behaviour (its existing
tier-3 result unchanged); tiers 1+2 green; tier 3 --only log-laws PASS or UNSUPPORTED;
check-banks --ci green; pushed; --live PASS. Screenshots: one full F1 chain, the F5
invalid-root step, one F3 engineering item, one misconception message.

STOP IF: Any family cannot reach 40 items under these constraints (report; do not loosen).
The step-choice UI cannot be built without changing Laws mode's code paths. Any checker FAIL.

---

Correction (Jon, 28 Sep 2026), verbatim:

3. Log Laws step 5: the contract was wrong — log-laws has no level keys. Add ?level= reading
   with keys 'alevel' (default when absent) and 'level4'. Both keys offer both modes and the
   same pools. Replace every hard-coded 'alevel' in mfg() and submitScore() with the real
   level. Do not add a 'level3' key. Record this correction in the contract file.

What step 5 had wrong, found 28 Sep:
- It said "the existing A-Level and L4 keys both offer both modes". log-laws has no `?level=`
  handling at all.
- It hard-codes `'alevel'` in every `mfg()` call and in `submitScore()`: six calls, at
  `games/log-laws/index.html:825`–`927` as of `e07b4ab`. So `?level=level4` served the same 45
  questions and reported itself as A-Level.
- canon lists the same shape in 22 games under "game-roster.md level lists vs. code reality". This
  correction fixes log-laws alone, by Jon's ruling.

A note for whoever builds it. The correction deliberately changes what Laws mode reports at
`?level=level4` (`'level4'`, no longer `'alevel'`). The success condition's "Laws mode is
byte-identical in behaviour" is therefore measured by its own parenthesis, "its existing tier-3
result unchanged", which a changed analytics level does not affect. If Jon meant more than that,
this is the line to raise before building.

---

Confirmations and one amendment (Jon, 28 Sep 2026), verbatim:

1. Yes: every mode, including the existing Laws drill, reports the real level it was opened with. With no ?level= in the URL, the default stays 'alevel', so existing links and the existing log_laws_alevel leaderboard are unaffected. The Laws drill's tier 3 result must stay the same; that is what "byte-identical" means here.
2. Confirmed: the class is w/c 12 Oct 2026. The build must be live before then, so Jon can check it.
3. Amendment to step 5, superseding the PR #4 wording "no level3 key": Jon has decided the portal will get an "Apprentices" filter with Level 3 and Level 4 beneath it. Level 3 means EAL Level 3 Engineering, AME3-004 Engineering Mathematics (= AMEDK3-003), the class this build is for. Read ?level= with keys 'alevel' (default), 'level3' and 'level4'. All three keys offer both modes and the same pools. LEVEL_LABELS entry for 'level3': "Level 3 (Engineering)". Do not change any other game, the portal filters or the level colours; the Apprentices filter is a separate contract.

**Where the `level3` label goes.** `LEVEL_LABELS` has two shared copies:
- `schools/assets/firebase-leaderboard.js:73`, which sets the label stored with each score and shown
  by the portal ticker;
- `leaderboards/index.html:168`, which names the boards on the hub.

The entry goes in both, so the two agree. That one line is the only change to
`firebase-leaderboard.js`; the DO NOT TOUCH on it otherwise stands. (`differentiation-duel` keeps a
private copy of its own, which is another game and untouched.)

---

Confirmations on the three items build notes flagged for Jon (Jon, 28 Sep 2026), verbatim:

1. The move label "log 10 = 1 / ln e = 1" (not the contract's "log_a a = 1") is confirmed, since
   no other base ever appears in Solve mode.
2. Free choice of stage 1–6 on the start screen, no progression locks, is confirmed.
3. The scoring formula (max(4, 10 − 2×wrong moves) + streak×3, 0 on a wrong final answer) and
   holding Solve off the leaderboard and score history (separate `ll_best_solve` PB key) are
   confirmed as built.

Merged to `main` 28 Sep 2026 (fast-forward from `claude/dreamy-galileo-e9qkk5`, `448b604`), after
an independent correctness re-verification: `verify-log-laws.py` re-run clean, a deliberately
injected wrong-law-step fault caught cleanly (564 failures, reverted), `check-banks --ci` and tiers
1+2+3 all reconfirmed green, F5's and F3's algebra hand-checked independently of SymPy, every
`K()`/KaTeX call site read for the prose-in-math-mode hazard (none found), leaderboard gating
confirmed in code. Portal card badged `updated`, 2026-09-28 (a level was added, the bank grew).
