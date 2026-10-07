# Handover: cloud lane

The cloud lane's running handover (canon §7.8.2). Only cloud-lane sessions edit this file; the home lane's is
`docs/handover/home.md`. Newest first. Keep it current on the branch as you go (CLAUDE.md, checkpoint discipline).

**Cloud lane owns:** per-game fixes in games that are currently unlisted, one game per PR, each with its verifier,
closing its entries in its own `docs/audits/findings/<slug>.yml`. It never edits `schools/assets/`, the shared
modules in `scripts/`, the workflow, canon, the roster's listed section, `docs/todo.md` or
`docs/audits/REGISTER.md` (CI regenerates that on main). Relisting a fixed game is the home lane's docs PR.

**Standing rule (Jon, 7 Oct 2026):** after each game's PR merges and main's full run is green, start the
next game on the contract's list without asking. Stop only for a STOP IF or an empty list.

**Every PR:** `python scripts/check-changed.py` before the first push; merge only on a green Gate, and never while
main's last full run is red; watch main's run after merging.

## 2026-10-07 (cloud): game 18 Factor Theorem (PR #130, open, paused for a new instance); NEXT = merge #130, then eigenvector-engine

- **Where it stopped (17:45 UTC):** #130's CI was green on c015325. main then took the home lane's #131
  (check-answer-lock: a CLOUD_LANE game that loads answer-lock.js while on NOT_YET is reported, not failed; "the home
  lane moves it to MIGRATED once it passes"). Merged main into the branch (clean); both answer-lock parts pass locally
  with KaTeX served (all 10 migrated). Pushed; wait for CI on the new head, then merge on a green Gate (main green
  after #131; no home-lane merge in the last 10 minutes).
- **Lane question for Jon:** #130 itself moves suvat and factor-theorem to MIGRATED, with a driving HINT each, and
  fixes the two faults the check found (suvat loaded answer-lock.js before next-control.js; factor-theorem's resize
  debounce needed `// lock-ok:`). #131's comment says the home lane does the MIGRATED move. Both are now on the same
  lines of `scripts/check-answer-lock.py`: keep #130's entries, or drop them and leave the move to the home lane.
- **Each later game in the queue loads answer-lock.js:** under #131 it is reported, not failed, so it no longer needs a
  MIGRATED edit to pass CI. Run `check-answer-lock.py --game <slug>` (with KaTeX served) before each PR anyway and
  give the home lane what it finds.
- **SUVAT Selector (PR #128) merged** at 17:12 on a green Gate (its first run lost its Gate job in GitHub's 500s; one
  re-run); main green after #125 before it.
- **Factor Theorem:** typed answers looked up in ACCEPTED (canon 7.1 pattern, R12), written by
  `scripts/verify-factor-theorem.py --write` (E): one box per blank, matched by position; numbers via MaffsAnswer;
  algebra through canon() (case, spaces, minus sign, superscripts, Greek names, a leading "f(x) ="). Every scaffold line
  accepts every value of its blanks that makes it true (my call, listed in the PR). Project Claude's T4 (a = -19,
  b = 30; (x - 3)(x - 2)(x + 5)). Q24/Q38/Q20 asks, Q22 hint, Learn ex. 4 candidates, test prompts' raw TeX (t5-019,
  new). MaffsLock (no class-1 entries in its register). Open: t5-004/-005 (free text), -008/-009 (exam-vocab.js),
  -013 (4), -014/-015 (design), -016/-017 (5), -018 (MaffsNext advance: check-teacher-invite's FT_STEP clicks only
  `.next-q-btn`, home lane).
- **Committed locally, waiting their turn (one PR at a time), each verifier passing and failing on main:**
  - eigenvector-engine (`/home/user/ee-work`, claude/ee-prep): Project Claude's QS[16]; SR-17 (no option a multiple of
    an eigenvector or of another option); working through MaffsText (B7, 16 ledger entries cleared); MaffsLock.
  - truth-will-set-you-free (`/home/user/tw-work`): tables computed from each key (no stored outputs); correct cells
    only score; [27] simplified; [6]'s distributive-law twin distractor (new t6-006); Aa saved; MaffsLock.
  - Jon's 15:27 follow-ups: trig-identity-duel (`/home/user/tid-work`: gcse[16] 12.2, hidden count-up, MaffsLock),
    binomial-blaster (`bb-work`: alevel2[36] B = 2, MaffsLock), partial-fractions-duel (`pfd-work`: alevel[22]
    C = 1/6, MaffsLock), truth-buster (`tb-work`: Next above the fold at 390x844 on all 60, MaffsLock).
- **Gotcha:** MaffsLock's 300 ms fresh window drops clicks a sweep makes right after a render: set
  `MaffsLock.FRESH_MS = 0` in sweeps and keep the real window in the lock test. A double click must be tested with
  `page.mouse` at the control (clicking a detached element twice fires its old listener).

## 2026-10-07 (cloud): game 17 SUVAT Selector (PR #128); #127 Force Resolver merged; NEXT = factor-theorem

- **Force Resolver (PR #127) merged** at 16:15 on a green Gate; main green after #126 before it.
- **SUVAT Selector:** every typed step marked by MaffsAnswer (`exact`, or `decimal` at the step's stated `dp`; the
  prompt says the precision; phase 0 to 2 d.p.); local parseFloat-and-tolerance gone (t5-006). Keys recomputed both
  ways: from the exact data, and from the values the student is shown (rounded chips, the previous step's key); a
  step's precision is the finest at which both round to the key (al[32] 1 d.p., al[18] 2 d.p., al[41]/[48] whole
  numbers, al[49] 1 d.p.; t5-007). Project Claude's sprinter (u = 8; t5-001) and ALEVEL[39] (2.02 s, 19.8 m/s;
  t5-003). v_y keyed -0.32 (t5-002); ALEVEL[22] says it lands at 3 s (t5-008); a question counts correct only if
  every typed step is (t5-009); wrong answers show the answer and wait for MaffsNext; ALEVEL[3]'s second root
  explained (t5-011). **MaffsLock (#125) adopted (Jon, 7 Oct 17:30):** lock first in every answer handler,
  fresh() on every render, MaffsLock.timer for every delay, endGame through finishOnce, newSession on Start;
  t5-004 closed. `scripts/verify-suvat.py` (E) adds the class-1 test (double click + Enter on CHECK mark once,
  two equation choices count once, one submit). Open: t5-005 (4), t5-010 (5).
- **Standing rule from Jon (7 Oct 17:30): MaffsLock is on main; every game fixed from now on adopts it and closes
  its class-1 entries in the same PR.** `check-answer-lock.py` (F1 part b) is not on main yet, so each verifier
  tests the lock itself.
- **Next: factor-theorem** (worktree `/home/user/ft-work`, branch claude/ft-prep, findings read, no edits):
  ACCEPTED-list typed answers (R12) and Project Claude's T4 (a = -19, b = 30; (x - 3)(x - 2)(x + 5) any order);
  t5-004/-005 (free text) and t5-008/-009 (exam-vocab.js, shared) stay open and get listed.

## 2026-10-07 (cloud): game 16 Force Resolver (PR #127); #126 Moments Master merged; NEXT = suvat

- **Moments Master (PR #126) merged** at 16:01 on a green Gate; main green after #124 before it.
- **Force Resolver:** `scripts/verify-force-resolver.py` (E), the Moments Master verifier's shape plus: options written
  as expressions evaluated (25 root 3 N, 10 tan 30 N) and a rounded figure counted equal to the expression it rounds
  from (43.3 N beside 25 root 3 N); figures quoted in text keys recomputed (FIGS) and their verdict required
  (VERDICT: "Yes", it slides). Project Claude's truss for level4[18] (12.8 kN) exactly. From the items' own data:
  level4[8] 1.40 m/s^2 (t5-002), alevel[47] 5 N (t5-004), alevel[32] "Yes" (t5-007), level4[7] worked with the
  stated 9.81 (1224 N; t5-011), alevel[31] "Equilibrium" (t5-012), alevel[35] g stated (t5-013); value-equal
  distractors replaced by named errors (t5-005, t5-006, f0-001, t5-014: 50 root 3, 1 N, "Undefined (tan 90)", 2.5 N,
  4.33 N, 266 N; for review); the given trig values stated where a key used them (alevel[11], level4[1]); 49.8 not
  49.7 (level4[15]). Wrong answers show the answer and working, then MaffsNext. Open: t5-008 (1), t5-009 (4),
  t5-010 (5).
- **Prepared locally, not pushed:** suvat (`/home/user/sv-work`, branch claude/sv-prep): typed steps on MaffsAnswer
  at a stated precision (the finest at which the exact data and the values shown both round to the key: al[32] 1 d.p.,
  al[18] 2 d.p., al[41]/[48] whole numbers), Project Claude's sprinter and ALEVEL[39], wrong answers wait for Next,
  a question correct only if every typed answer is; `scripts/verify-suvat.py` (E).

## 2026-10-07 (cloud): game 15 Moments Master (PR #126); #124 Linear Equation Solver merged; NEXT = Force Resolver

- **Linear Equation Solver (PR #124) merged** at 15:47 on a green Gate, after main's runs following #122 (re-run;
  the first attempt lost its Gate job in GitHub's 15:05-15:17 write errors) and #123 were green.
- **Moments Master:** `scripts/verify-moments-master.py` (E): every numeric key from the item's own data (SymPy;
  KEYS), distractors equal in value to the key (5 kW = 5000 W) or to each other, named-error REASONS for the items
  rewritten, numeric claims in keys and working lines, "Same beam" items quoting their predecessor, text keys pinned
  (REVIEWED, --print-pins); Chromium at 390 and 320: every option clicked, no raw TeX, no sideways scroll. Project
  Claude's data for :128, :134, :147, :172/:173 exactly; :141 rekeyed 75 N; :180's 5 kW replaced by 524 W
  (P = 2 pi N T / 60 with 100 taken as rpm; for review). Filed and fixed: t5-014 (premises: the trapdoor uniform,
  the level4 cable beam light with a vertical cable), t5-015 (R_B, T_A shown raw by textContent: ctx and ask now
  through MaffsText). Wrong answers show the answer and the item's working line, then MaffsNext (no stored
  explanations exist: fuller ones would be Project Claude content). Open: t5-009 (1), t5-010 (4), t5-011 (5),
  t5-012 (the gate premise: Jon).
- **Prepared locally, not pushed:** Force Resolver (`/home/user/fr-work`, branch claude/fr-prep). suvat is planned
  (typed answers onto MaffsAnswer with a stated precision per step; keys from the values the student is shown).

## 2026-10-07 (cloud): Linear Equation Solver, Jon's "optimal move" contract (PR #124); #115 Proof Builder merged; NEXT = moments-master

- **Proof Builder (PR #115) merged**; main's full run after it green (and after #117).
- **Jon's list (7 Oct, this session):** proof-builder (done), linear-equation-solver, then with Project Claude's
  replacement data moments-master, force-resolver, suvat, factor-theorem, eigenvector-engine, then
  truth-will-set-you-free; then (Jon, 15:27) follow-ups to merged games, one PR each: trig-identity-duel gcse[16]
  replaced + timer to hidden count-up; binomial-blaster alevel2[36] replaced; partial-fractions-duel alevel[22]
  replaced (each clears its B3 ledger entry); truth-buster Next visible at 390x844 on every item. The replacement
  data is in Jon's 7 Oct paste (the session's first message); if it is not to hand, ask Jon.
- **MaffsLock (`schools/assets/answer-lock.js`) is not on main yet:** class 1 stays open. Once it lands, adopt it in
  each game fixed (lock, fresh, timer, finishOnce) and close that game's class-1 entries.
- **Linear Equation Solver:** `scripts/gen-linear-moves.py` (depth-3 search, iterative deepening, under 1 s) writes
  MOVES between its own GENERATED markers: per line, every optimal move (one per distinct line), one slower move
  where one exists, named errors (one-side, carry, xonly, constnot) to fill four. Options show the move and the line
  it gives with the number side unevaluated (x = 12 - 7), so a one-side error can be shown and the answer phase
  still asks for the value. The trail follows the student's route (295 lines for 141 questions). Amber = 12.5 (half
  the 25 at stake), streak kept; amber and red wait for MaffsNext. Hints and feedback through MaffsText (t4-002).
  `gen-linear-equations.py` no longer writes the superseded per-step `opts`/`hint` (QUESTIONS otherwise identical)
  and uses a repo path. `scripts/verify-linear-equation-solver.py` (group E, ~40 s): its own TeX parser and search,
  SymPy for every value; every option clicked in Chromium; Jon's four cases tapped; page == generator. On main's
  file it fails on exactly r-001 (18 options in the 14 questions), r-002 (49) and t4-002 (11).
  - **Decision to review:** "fractions" in the tie-break means fractional constants, not coefficients (Jon's own x2
    example on x/2 + 5 = 11 needs x/2 = 6 to count as fraction-free). Under that reading every keyed move is
    optimal (STOP IF not triggered).
  - Four lines (-x = c in U1-U4) have 3 options: no fourth honest one exists.
  - Open: t4-003 (class 1).
  - **Gotcha (MOVES size):** the first version stored each option's feedback sentence (MOVES 280 KB, page 348 KB)
    and tier 4's extraction of this one game ran for minutes: the render-site evaluator calls `literal_to_json` on a
    literal every time it resolves an identifier (about 350 calls a second, no cache). Options are now compact arrays
    and the page words the feedback from their fields (MOVES 92 KB, page 159 KB, extraction 8.5 s). A large
    generated literal in any game will hit the same cost.
- **For the home lane:** content group B4 ran 243 s on main's run after #117, over canon's 4-minute cap; this
  verifier went in E (133 s on that run) instead. `bank_common.literal_to_json` is re-run per identifier
  resolution; memoising it by node would make large literals cheap (shared code). SR-13's scoring sentence
  ("scores full marks") needs a note for Jon's 7 Oct amber rule.

## 2026-10-07 (cloud): game 13 Proof Builder (PR #115); #112 Dimension Checker merged; NEXT = Linear Equation Solver (Jon's 7 Oct contract)

- **Dimension Checker (PR #112) merged** on a green Gate; main's full run after it green.
- **Proof Builder (PR #115):** `scripts/verify-proof-builder.py` (B4, declared by its own `# ci-line:` header; no workflow edit): refutation predicates for every counter-example option, SymPy induction stages, sorter orders, rendering at 390px. One renderer `M()` and 79 strings migrated to `\( \)` (132 B7 + 2 B11 ledger entries cleared). The options' TeX test is written as `includes()` at each call site, because tier 4 cannot decide a helper (`isTeX(v)`) and crashes on a regex `.test()` (game 8's note). Open: t5-014, t5-016 (1), t5-021 (5), t5-023 (per-mode boards: Jon), t5-024 in part (4).
- **Main went red once after #109** (13:16): group E, Like Terms Collector item 1, the same failure as on #106 and #88's first run (third time today). One re-run of the failed job was green. It does not reproduce here (0 of 24 runs, 8 at a time; this sandbox has Playwright 1.56 and no gstatic, CI has 1.63 and both). Home lane: the verifier hardening proposed on #106.
- **Original contract list done.** Everything left open is a shared class (1, 4, 5, B11), a decision for Jon (TID timer, Integration Duel + c, Proof Builder per-mode boards, Truth Buster fold), or needs new content (duplicate items in TID, BB and PFD; Truth Buster video IDs to check from home). Skipped until Project Claude supplies data: moments-master, force-resolver, suvat, factor-theorem, eigenvector-engine, truth-will-set-you-free.
- **Next: Linear Equation Solver** (Jon's contract of 7 Oct, added after Proof Builder): "What is the optimal move here?", every tied optimal move full marks, a valid but slower move amber (half, streak kept), wrong options named real errors; option sets generated by `scripts/gen-linear-moves.py` (depth-3 search) between GENERATED markers; the verifier re-derives every class with SymPy; the SR-13 note in canon.

## 2026-10-07 (cloud): game 12 Dimension Checker (PR #112); #109 Curling Friction merged; NEXT = Proof Builder

- **Curling Friction (PR #109) merged** on a green Gate; main's full run after it green.
- **Dimension Checker (PR #112):** `scripts/verify-dimension-checker.py` (B4, declared by its own `# ci-line:` header; no workflow edit): dimension algebra for keys, options and every worked step; MaffsOptions, MaffsNext. Open: t5-003 (1), t5-005 (5), t5-006 (4).
- **Next:** Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 11 Curling Friction (PR #109); #107 Integration Duel merged; NEXT = Dimension Checker

- **Integration Duel (PR #107) merged** on a green Gate; main's full run after it green.
- **Curling Friction (PR #109):** `scripts/verify-curling-friction.py` (B4): exact targets per item; no negative "speed"; friction only on sliding stones; MaffsNext. t5-008 filed and fixed. Open: t5-003 (1), t5-004 (4), t5-005 (5).
- **CI lines (Jon, 7 Oct):** from when contract V merges (home lane), a cloud-lane verifier declares its CI group
  with a `# ci-line:` header in the verifier file itself, and the PR does not edit `.github/workflows/check-site.yml`
  at all. Until then: one workflow line per PR, and rebase on main before merging.
- **Next:** Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 10 Integration Duel (PR #107); #106 Differentiation Duel merged; NEXT = Curling Friction

- **Differentiation Duel (PR #106) merged** on a green Gate; main's full run after it green.
- **Integration Duel (PR #107):** `scripts/verify-integration-duel.py` (B4): antiderivatives checked by differentiating, c held as a symbol, ln x + c sampled where it is right. Missing + c named in feedback (Jon may rule it right). B11 (5) cleared. Open: t5-010 in part (class 4).
- **Like Terms Collector's verifier flaked once on #106** (group E; item 1 typed 8.9/6.5, `MARK()` null, empty feedback;
  it passed 5 of 5 locally and on the one re-run). Same item and shape as #88's first-run flake. Home lane: after
  `page.fill`, wait for the boxes to read the typed values and for the feedback panel's class before reading the mark.
- **#103 split content group B into B1-B4**; the cloud lane's verifiers go at the end of B4, where #103 put them.
  A branch prepared before a ledger change on main conflicts on `data/check-ledger.json`: take main's ledger and
  replace only that game's record (the scratch helper did this per commit).
- **Next:** Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 9 Differentiation Duel (PR #106); #105 Partial Fractions Duel merged; NEXT = Integration Duel

- **Partial Fractions Duel (PR #105) merged** on a green Gate; main's full run after it green.
- **Differentiation Duel (PR #106):** `scripts/verify-differentiation-duel.py` (B4): implicit items compared on the curve; explanations must state the answer. B11 (9, five of them added by #99) and B7 (1) ledger entries cleared; t5-013/014 filed and fixed. Open: t5-010, t5-011 (class 4).
- **Next:** Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 8 Partial Fractions Duel (PR #105); #104 Binomial Blaster merged; NEXT = Differentiation Duel

- **Binomial Blaster (PR #104) merged** on a green Gate; main's full run after it green.
- **Partial Fractions Duel (PR #105):** `scripts/verify-partial-fractions-duel.py` (B4): every Find solved from its stated form; valid equivalent forms removed. Open: t5-007 (class 1), t5-009 (class 4). New B3 ledger entry: the Find B / Find C pair for 1/(x(x+1)(x-1)) now share stem, options and key (needs a new item).
- **The tier 4 crash recorded under game 6 has a known cause (home lane: shared code).** `_SiteEval.regex()` in
  `bank_common.py` returns `(pattern, glob)`, and the `.test` branch of `_SiteEval.call()` calls `.search` on that
  tuple, so any `/re/.test(x)` the evaluator reaches raises. Taking the pattern from the tuple fixes it. Also: a
  guard written as a page helper (`isTeX(v)`) is never decided, so both branches count; until the evaluator can
  look inside, the cloud lane writes such guards as `includes()` at the call site.
- **Next:** Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 7 Binomial Blaster (PR #104); #102 Trig Identity Duel merged; NEXT = Partial Fractions Duel

- **Trig Identity Duel (PR #102) merged** on a green Gate; main's full run after it green.
- **Binomial Blaster (PR #104):** `scripts/verify-binomial-blaster.py` (B4): three-term estimates as the ask states, rounding-ambiguity check, MaffsOptions. Open: t5-017 (class 1), t5-018 (class 4), t5-022 in part (portal card: home lane). One B3 duplicate (needs a new item).
- **Next:** Partial Fractions Duel, Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 6 Trig Identity Duel (PR #102); #101 Component Crusher merged; NEXT = Binomial Blaster

- **Component Crusher (PR #101) merged** on a green Gate; main's full run after it green.
- **Trig Identity Duel (PR #102):** `scripts/verify-trig-identity-duel.py` (B2): every option read into SymPy. Compound-angle keys, 85.9°, identical options fixed; t2-011 filed and fixed. Open: t2-007 (class 1), t2-010 (timer: Jon's decision). gcse[16] duplicates gcse[12] (B3; needs a new item).
- **For the home lane (shared code, not edited here):** `bank_common.py`'s render-site analysis crashes
  (`AttributeError: 'tuple' object has no attribute 'search'`, in `call`) on a regex literal's `.test()` in some
  positions: inside a template-literal expression (Component Crusher's first CI run) and `/[\\^_{}]/.test(...)`
  (Proof Builder, found locally). Extraction then fails and every ledger entry reads as stale. The cloud lane works
  round it in each game (a named function, or string methods); the parser fix is the home lane's.
- **Local tier 4 in the cloud sandbox works:** serve KaTeX from the npm tarball (route the jsdelivr KaTeX URLs to
  `package/dist`), run `extract-banks.py`, then `check-banks.py --ci`; about 95 s with 4 workers.
- **Next:** Binomial Blaster, Partial Fractions Duel, Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 5 Component Crusher (PR #101); #100 Expectation Station merged; NEXT = Trig Identity Duel

- **Expectation Station (PR #100) merged** on a green Gate; main's full run after it green.
- **Component Crusher (PR #101):** `scripts/verify-component-crusher.py` (B2): keys from what is shown, diagrams measured from the canvas, marking through MaffsAnswer. Level 4 data shown; prompts' maths in `\( \)` (31 B7 ledger entries cleared). Open: t4-005 (class 1), t4-011 (class 5), t4-014 in part (class 4).
- **Next:** Trig Identity Duel, Binomial Blaster, Partial Fractions Duel, Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 4 Expectation Station (PR #100); #98 Trig Worms merged; NEXT = Component Crusher

- **Trig Worms (PR #98) merged** on a green Gate; main's full run after it green.
- **Expectation Station (PR #100):** `scripts/verify-expectation-station.py` (B1): all 180 Stage 3 cards reviewed with checks from the distribution ("most" = more than half); Stage 1 marked exactly. t2-001..016 fixed, t2-018/019 filed and fixed; open: t2-017 (class 1).
- **Next:** Component Crusher, Trig Identity Duel, Binomial Blaster, Partial Fractions Duel, Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 3 Trig Worms (PR #98); #97 Truth Buster merged; NEXT = Expectation Station

- **Truth Buster (PR #97) merged** on a green Gate; main's full run after it green.
- **Trig Worms (PR #98):** `scripts/verify-trig-worms.py` (group B2, ~20 s). The generator is rebuilt from a
  `POOL` of servable outcomes (1,204; no retry); every outcome is recomputed with mpmath from the values shown,
  at the stated precision ("to the nearest degree", "to 1 decimal place"); every distractor is a named error and
  the feedback names it; only the two given sides are labelled and the triangle is drawn at one scale.
  t1-001..t1-004 fixed; nothing left open.
- **Next:** Expectation Station, then component-crusher, trig-identity-duel, binomial-blaster,
  partial-fractions-duel, differentiation-duel, integration-duel, curling-friction, dimension-checker,
  proof-builder (all prepared on local worktrees /home/user/*-work, not pushed; their PR texts and register
  specs are in this session's scratchpad).

## 2026-10-07 (cloud): game 2 Truth Buster (PR #97); #96 Spot the Error merged; NEXT = Trig Worms

- **Spot the Error (PR #96) merged** on a green Gate; main's full run after it green.
- **Truth Buster (PR #97):** `scripts/verify-truth-buster.py` (group B1). Keys are reviewed judgements, with the
  words a statement must contain for its key to hold (`needs`, SR-18) and SymPy where a key can be computed;
  every reveal figure is in `FIGURES` (an unlisted `=`, `<`, `>` fails); dates and counts in `SOURCED`.
  t3-001..012 fixed. Open: t3-013 (class 1), t3-014 (class 5/4), t3-015 in part: the 21 Learn More video IDs
  (YouTube is refused from the cloud sandbox: check them from home) and Next below the fold (shorter reveal
  text, Project Claude, or a layout ruling).
- **Next:** Trig Worms, then expectation-station, component-crusher, trig-identity-duel, binomial-blaster,
  partial-fractions-duel, differentiation-duel, integration-duel, curling-friction, dimension-checker (all
  prepared on local worktrees /home/user/*-work, not pushed), then proof-builder (in progress). A lost container
  loses them: redo from the register.
- **Gotchas:** a PR that clears a fixed B7/B11 finding also clears its entry in `data/check-ledger.json` (dump
  with `indent=1, ensure_ascii=False, sort_keys=True`, as `check-banks.py` does), or CI fails it as stale. With a
  workflow edit, `check-changed.py` selects every check (about 45 minutes here): run it in the background with a
  long timeout, never the default 30 minutes (the Truth Buster run was cut off there).

## 2026-10-07 (cloud): unlisted-games contract, game 1 Spot the Error (PR #96); NEXT = Truth Buster

Jon's contract of 7 Oct (cloud lane): fix the unlisted games one per PR, each under a new verifier, in this order:
spot-the-error, truth-buster, trig-worms, expectation-station, component-crusher, trig-identity-duel,
binomial-blaster, partial-fractions-duel, differentiation-duel, integration-duel, curling-friction,
dimension-checker, proof-builder. Shared classes stay open: 1 (answer lock, F1), 4 (?level resolver, F2),
5 (bank size), B11 parser gaps (F0). Skipped until Project Claude supplies data: moments-master, force-resolver,
suvat, factor-theorem, eigenvector-engine, truth-will-set-you-free. Other owners: linear-equation-solver,
screening-room, glorious-gantt.

- **Spot the Error (PR #96):** `scripts/verify-spot-the-error.py` (group B2, ~9 s). All 19 register entries
  fixed (t1-001..014 plus the re-audit's t1-015..019); nothing left open. 16 items reworded (listed in the PR
  for Project Claude). Model: the key is the first step that departs from correct working; later steps carry it.
- **Prepared on local branches, not pushed** (worktrees under /home/user/*-work, gone with this container): the
  next games are rebuilt from their audit entries in the same order. If this container is lost, redo from the
  register; the PR descriptions list the content choices.
- **Gotchas:**
  - A reviewed verdict (a step judged an error, a statement judged true) reads no text, so each verifier that
    holds verdicts pins each item's content hash (`REVIEWED`, `--print-pins`): any edit fails until re-reviewed.
  - The self-tests count a plant as caught only by a check other than that pin.
  - Locally, the KaTeX CDN is refused: KaTeX games' verifiers take `--katex-dir` (the npm tarball's dist/).
    `check-changed.py` here always fails seven checks for environment reasons (PR #96 lists them).
  - `extract-banks.py` through the sandbox wrapper reports component-crusher's 34 B7 entries stale even on main:
    do not trust a local tier 4 run for B7; read CI's.
  - A shared TeX-to-SymPy reader would serve several of these verifiers (each carries its own small one, since
    the cloud lane does not add shared modules): a home-lane candidate.

## 2026-10-07: the lane starts (written by the home lane, which set up the lanes)

- No cloud session has run since the lanes were split. The last cloud work was 6 Oct 2026 (#85 audit tranches 1-2
  and two games unlisted; #86 Core Maths Paper 1), recorded in CLAUDE.md's history.
- The unlisted games and their open findings: `docs/audits/REGISTER.md` ("By game", Listed = unlisted) and the
  roster's Unlisted section. Each has its relist checklist in `docs/todo.md` §1.53-§1.75.
- **Next:** Jon's first cloud-lane contract names the game.
