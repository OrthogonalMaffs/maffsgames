Status: DONE 28 Sep 2026, commit `d8b244e` on `claude/cool-hawking-f88bj7`. The step 6 report,
the step 2 report and the verification are in `docs/audit-chart-interrogator-cumfreq.md`.
Drafted by Project Claude 26 Sep 2026; ruled by Jon (C + D). Its STOP IF fired once, before any
edit, on CF7's comparator ratio; Jon's rulings on it are verbatim at the end of this file.
`--live` run 28 Sep after `d165d63` deployed: 5/5 PASS.

TASK: Make Chart Interrogator's cumulative-frequency mode mark what the student can see — key from the drawn curve, scale-aware tolerance — and replace its ill-posed spread sentence with a benchmark question and a comparator question.

ROOT CAUSE: (1) drawCumFreq (:562–:573) draws a cubic Bezier through the points; the key
uses interpolateCF (:700), straight segments. They disagree by up to ~2.4% of the axis: CF6
Q1 drawn 185.4 vs key 192.5, CF7 Q3 drawn 1546 vs key 1575 — an accurate reader is marked
wrong at the fixed ±3 tolerance. (2) Tolerance is a fixed absolute number (tolerance:1/2/3)
whatever the axis: CF7 spans £1600, CF9 spans 10 days. (3) expected is Math.round()ed (:666–
:669), so CF9 Q1 1.53 days is keyed as 2. (4) The spread sentence (:882, :934) compares the
IQR with 1.5 × itself, so it is always "relatively consistent" — and a single data set's
consistency cannot be judged without a comparator. (5) The "25% below Q1 / above Q3"
dropdown (:884–:885) offers two true options and accepts one.

CLASS CHECK: Yes, on (1)–(3). The same marking path (:772) and the same tolerance/rounding
pattern serve every scenario and all four chart types; the drawing and the key are two
separate implementations of one curve. Fix at that layer: one curve function used by both
drawing and key; one tolerance rule. (4)–(5) are local content defects in one sentence.

EXACT CHANGE:
1. One source of truth for the curve: a function giving x for a cumulative frequency on
   the SAME Bezier the drawing uses (same control points, solved numerically — bisection
   on t, fixed iteration count, no retry loop), and its inverse (cf at a given x).
   drawCumFreq keeps its drawing; every cumfreq key uses the new functions. interpolateCF
   is no longer used for cumfreq keys.
2. Tolerance for a value read off a graph = 2.5% of that axis's span (x: last hi − first
   lo; count axis: n). An IQR tolerance = 2 × the x tolerance. expected is no longer
   Math.round()ed; display precision follows the axis (e.g. 1 dp where span ≤ 20).
   Apply to cumfreq now. For stemleaf, boxplot and histogram: REPORT every tolerance and
   rounding they use and whether the rule would change them. Do not change them.
3. Replace the spread sentence with two, both keyed from the TRUE values computed in step
   1 — never from sessionAnswers:
   a) Benchmark (per scenario, new fields benchQuestion + benchSide 'above'|'below'):
      CF1 "How many students passed?" above 40 · CF2 "How many plants reached the target?"
      above 120 · CF3 "How many journeys were late?" above 45 · CF4 "How many employees
      earn below the national median?" below 28 · CF5 "How many work over the legal
      maximum?" above 48 · CF6 "How many properties are below the regional average?" below
      220 · CF7 "How many households pay above the average bill?" above 1400 · CF8 "How
      many work over contract hours?" above 37.5 · CF9 "How many deliveries missed the
      SLA?" above 3 · CF10 "How many components exceed the tolerance limit?" above 52.
      Numeric input; tolerance per step 2 on the count axis.
   b) Comparator (new fields compLabel + compIQR). Sentence: "The IQR of ___ compared with
      [compLabel] shows this group is [more consistent / less consistent]."
      CF1 last year's IQR, 32 · CF2 a second greenhouse, 12 mm · CF3 the old timetable,
      28 min · CF4 a competitor firm, £8k · CF5 last year, 20 hrs · CF6 a neighbouring
      town, £60k · CF7 last year, £300 · CF8 another department, 14 hrs · CF9 the previous
      courier, 3.5 days · CF10 Machine B, 2 mm.
      Key: true IQR < compIQR → "more consistent", else "less consistent".
4. The 25% dropdown: options "below Q1", "below the median", "below Q3" (with values);
   only "below Q1" correct.
5. showModelAnswer (:933–:938): rebuild from the same true values and the new sentences.
6. Report a table: per scenario, true Q1/median/Q3/IQR from the drawn curve, benchmark
   answer, comparator verdict, and the ratio compIQR/IQR.

DO NOT TOUCH: Histogram H2 / the histogram sentence (1.8 — awaiting Jon). Stem-and-leaf,
box-plot and histogram tolerances (report only). The leaderboard score (constant 100 — it
belongs to the leaderboard-modes contract). Scenario data (classes, frequencies, benchmarks).
Any other game.

SUCCESS CONDITION: For every CF scenario, entering the drawn-curve Q1/median/Q3 is marked
correct and a value 2 × tolerance away is marked wrong (assert in a scripted check under the
stub server). Comparator verdicts split 5 more / 5 less, and every compIQR/IQR ratio is
outside 0.7–1.4. No sentence keys from sessionAnswers. Tiers 1+2 green; tier 3 --only
chart-interrogator PASS or UNSUPPORTED. Pushed; --live PASS.

STOP IF: Any comparator verdict flips or any ratio falls inside 0.7–1.4 once computed from
the drawn curve (report; do not pick new values). The 2.5% rule would make a Phase 1
reading on another chart type fail against its current key. The Bezier inverse is not
monotonic in any class. Any checker FAIL.

---

Rulings (Jon, 28 Sep 2026), verbatim. They came after the STOP IF above fired on CF7: the drawn
curve's IQR is £425.80, so a comparator of £300 gave a ratio of 0.7046, inside 0.7–1.4.

1. CF7 comparator: change £300 to £280. Everything else in CF7 unchanged.
2. Comparator wording: accepted as proposed — "The IQR of 20.7 mm compared with a second
   greenhouse (12 mm) shows this group is [less consistent ▾]", CF1 as "compared with last
   year's IQR (32)".

As built, CF2's IQR reads "21 mm", not "20.7 mm". Step 2's display rule shows whole numbers on
CF2's 70 mm axis, and 20.7 was the unrounded figure used in the proposal. The wording is as ruled.
