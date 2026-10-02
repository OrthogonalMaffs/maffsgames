# Contract — Free Daily Pizza (resit fluency strand, game 2)

**Jon's contract of 30 Sep 2026, recorded verbatim.** It supersedes the earlier queued draft of this
file (the one committed with Six Sevens, Bruv, with Jon's keying rulings and daily-mix addendum
folded in). Header from Jon: *Model: opus · Effort: xhigh — new build, exact arithmetic, leaderboard
keying, verifier; set /model before pasting.*

**Ruling during the build (Jon, 30 Sep 2026):** `firebase-leaderboard.js`'s `GAME_NAMES` map may take
one row, `'free-daily-pizza':'Free Daily Pizza'`, beside the levelLabel() additions in item 7, so the
ticker never shows the raw slug.

---

CONTEXT FOR A FRESH SESSION: pull origin/main first. Read, in order: CLAUDE.md (Task Contract section); docs/todo.md START OF NEXT SESSION; games/six-sevens-bruv/ (the resit strand's reference implementation — register, phone layout, analytics mode keying); canon §7.5.1 (resit-strand register rule), §7.6 (advance rule incl. the phone rule), §1.3 (events); schools/assets/firebase-leaderboard.js (levelLabel(), MaffsInitials, standing()); scripts/roster-levels.json; scripts/check-leaderboard-coverage.js (hub-registry and ticker-label checks). This contract supersedes docs/next-contract-free-daily-pizza.md — replace that file's contents with this contract in your first commit.

TASK: Build "Free Daily Pizza", the resit strand's fraction–decimal–percentage equivalence game, with a practice mode and a date-seeded daily pizza that shows today's best score as a target.

ROOT CAUSE: FDP equivalence is the top CORE gap in the resit audit (docs/resit-coverage-audit.md §10: fractions and decimals, 7 parts including N10.1, R3.1, R6.1). Converting between fractions, decimals and percentages is among the most-reported weaknesses of grade 1–3 students, and no live game covers it at a Foundation pitch.

CLASS CHECK: A new build. Four known bug classes are designed out rather than patched later:
(1) value-equivalent options (todo 1.24, rule B11) — in an equivalence game a distractor equal in value to the answer marks a correct student wrong, so every option is compared as an exact rational;
(2) floating-point marking (Expectation Station) — all values held as integer numerator/denominator pairs, never floats;
(3) non-comparable scores on one leaderboard key (higher-power, §8.2b; Six Sevens q20/q40) — practice lengths and the daily pizza are keyed separately;
(4) a device-only path depending on a third-party network (MaffsInitials lesson) — the game plays fully with Firebase blocked.
Shared helpers are reused, never hand-rolled: MaffsOptions.build, MaffsNext, MaffsSession, MaffsLeaderboard (standing, submitScore), MaffsInitials, levelLabel().

EXACT CHANGE:
1. games/free-daily-pizza/index.html, single file: standard head (canon §1.1, §2); game title and Aa toggle on every screen; prefers-reduced-motion; footer; GCSE+ row per the resit-strand register rule; phone rule per §7.6 (controls unusable during feedback are hidden, secondary panels collapse, the reason to read and Next sit above the fold at 320×568, 375×667, 390×844); no horizontal scroll at 320px.

2. Content — four stages, 40–50+ distinct items each (generation from parameters is fine):
   S1 benchmark equivalents: ½, ¼, ¾, ⅕ and fifths, ⅒ and tenths, ⅓, ⅔, ⅛, 1/100 ↔ decimal ↔ percentage;
   S2 wider set: eighths, twentieths, hundredths, simplifying (e.g. 18/24 = ¾);
   S3 fraction or percentage of an amount, non-calculator numbers (25% of 80, ⅗ of 45);
   S4 one quantity as a fraction and as a percentage of another, simplest form (15 out of 60 = ¼ = 25%).
   Recurring decimals are shown as recurring (0.3̇, 0.6̇), never as 0.33 presented as exact; percentages as 33⅓%.

3. Options via MaffsOptions.build(). Distractors are named misconceptions, each carrying a tag: digit-reading (¼ → 0.4), denominator-as-decimal (⅕ → 0.5), place value (0.5 → 5%), truncation (⅓ → 0.3), inversion (15 out of 60 → 60/15 or 4), unsimplified (only where the question asks for simplest form). NO option may equal the correct answer in value unless the question explicitly asks for a particular form — compared as exact rationals.

4. Pictures, drawn honestly (scaffold rule): pizza with equal slices for fractions; a 100-square grid or bar for decimals and percentages; shown after a wrong answer via MaffsNext.wrong() with the working, in the order working → picture → Next (the picture may drop below Next on the smallest phone; the working never does); on conversion questions the two pictures side by side. A picture must never show the answer before the student answers. Never a lossy drawing: if a value cannot be drawn clearly, show no picture for it.

5. Practice mode: MaffsSession (20 / 40), stages selectable (single stage or mixed), count-up visible timer feeding the standard formula (BASE = 100, T_K = 0.15). Leaderboard levels 'practice-q20' and 'practice-q40', ranked separately.

6. Daily pizza: 10 questions, a fixed stage mix served easiest first — 3 from S1, 3 from S2, 2 from S3, 2 from S4 — drawn by a deterministic PRNG seeded from the UK date (Europe/London), so every device gets the same pizza on the same UK day. Replays allowed. Score submitted to level 'daily-YYYY-MM-DD'. Today's best shown as the target via MaffsLeaderboard.standing(); if Firebase is unavailable, play proceeds with no target and no error.

7. Leaderboard naming and registry: add labels to levelLabel()'s forward map — 'practice-q20' → "Practice · 20", 'practice-q40' → "Practice · 40"; the existing daily pattern names 'daily-YYYY-MM-DD' ("Daily pizza 1 Oct"). Hub registry lists practice-q20 and practice-q40 only; the daily pattern is declared in the hub-registry check so it passes without appearing on the hub. scripts/roster-levels.json gains whatever entries the new keys need.

8. Analytics (§1.3): level 'all' and mode 'practice-q20' | 'practice-q40' | 'daily' on every event; question_answered with question_index (1-based) and correct; game_completed with score, questions_answered, questions_correct; personal_best_set with previous_best (personal-best key follows the board key).

9. Verifier scripts/verify-free-daily-pizza.py in CI: every item's answer recomputed with exact rationals; every distractor recomputed from its misconception tag; no distractor value-equal to the answer; recurring decimals never presented as exact; S1–S4 each ≥ 40 distinct items; daily seed gives the identical set for a fixed UK date on repeated runs and different sets across dates; the daily mix is 3/3/2/2 and ordered by stage; every picture's slice/square count matches its value; no pre-answer picture reveals the answer; every event carries level, mode and its required parameters. Fault injection — a wrong answer, a value-equal distractor, a wrong tag, a broken daily mix, a pre-answer leak — must each FAIL; evidence in the handover.

10. Release: roster row (.claude/rules/game-roster.md); portal cards in the KS3 and GCSE sections and on /op/ (identical cards, data-topics="number", data-badge="new" + today's date on every occurrence); sitemap; game counts (96 → 97) wherever canon, CLAUDE.md and the portal state them; timer-policy.md (count-up, scored); docs/todo.md item 3.6 done and the resit slate updated.

DO NOT TOUCH: any other game; shared helpers except to import them and the levelLabel() forward-map additions in item 7; RTDB rules; the leaderboard hub's logic beyond registry entries; next-control.js.

SUCCESS CONDITION:
- Verifier PASS in CI and FAIL on each injected fault.
- Played locally on serve-stubbed.py: all four stages; a wrong answer shows working then picture then Next; two loads on the same simulated UK date give the same daily pizza, easiest first; the daily target shows with Firebase available and is absent without error with the SDK blocked; practice-q20, practice-q40 and daily scores land on separate keys (stubbed network log).
- Phone: screenshots at 320×568, 375×667, 390×844 of a wrong-answer screen, Next above the fold (or the picture-below-Next fallback at 568 only).
- check-site.py tiers 1+2 green (including the level-control and ticker-label checks); --tier 3 --only free-daily-pizza reported (UNSUPPORTED acceptable, FAIL not); tier 4 layer A accounts for the game; check-leaderboard-coverage.js passes.
- Merged on green; handover written.

STOP IF:
- The RTDB rules reject the 'daily-YYYY-MM-DD' or 'practice-q20' key patterns.
- standing() cannot read a single level key without modification.
- Any stage cannot reach 40 distinct items without near-duplicates.
- A value in the bank cannot be drawn honestly and has no sensible no-picture fallback.
- Fitting a phone would put the working below Next.
