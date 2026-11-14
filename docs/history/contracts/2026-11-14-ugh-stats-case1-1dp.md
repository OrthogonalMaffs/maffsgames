UGH-STATS-CASE1-1DP (Project Claude, Sat 14 Nov 2026 21:55)
Recommended: Sonnet or Opus, effort medium. LANE: home. TIER: Medium (merge on green; Project Claude reviews after merge). START: now, after #766's close-out (carry it in this PR's first commit if not already on main). One PR from current origin/main (8f2b84f or newer). MERGE: merge-pr.py on a green Gate.

TASK: Make Case 1's per-day questions give a meaningful number for low-answer games: answers per day to one decimal place, not to the nearest whole number.

ROOT CAUSE: Case 1 Q1–Q3 (ugh-stats/half-our-games/) round answers per day to a whole number. Every A level / Further / Level 4 game gets under one answer a day since 1 September, so game 2 always shows "about 0": live now, Eigenvector Engine 21 ÷ 75 = 0.28 → 0, and Factor Theorem at 10 answers would be 10 ÷ 75 = 0.13 → 0. "About 0" contradicts the game having answers and makes Q3's comparison meaningless. Project Claude's spec set the rounding; the build followed it.

CLASS CHECK: The rounding rule lives in two places that must agree: the page's question data and check-ugh-stats.py's independent recomputation. The widget's typed-answer check is shared (ugh-stats.js) and gains 1 dp support once, for every page. No per-question workaround.

EXACT CHANGE:
1. Case 1 Q1 and Q2: the stem ends "What is its mean number of answers per day, to 1 decimal place?"; answer = N ÷ D rounded half up to 1 dp; working "{N} ÷ {D} = {to 3 dp} ≈ {answer}". Q3's stem uses the same 1 dp values ("about {a} answers a day; {game 2} about {b}").
2. Game 2 qualifies only if its 1 dp value is at least 0.1 (else the next qualifying game; none → skip Q2 and Q3, as now).
3. Widget (ugh-stats.js): a typed question may declare dp: 0 or 1 (default 0). With dp 1 the input accepts a decimal point (inputmode="decimal") and the answer is accepted only when its value equals the stated value to 1 dp: accept "90.9" and "90.90", reject "91" and "90.8". Cases 2 and 3 stay dp 0, behaviour unchanged.
4. check-ugh-stats.py: recompute Case 1 at 1 dp; plants: a whole-number answer accepted for a dp 1 question must fail; a game 2 at 0.0 must fail. home.md entry.
DO NOT TOUCH: every other question's wording and rounding; Cases 2–4; the game 2 level rule from #766's follow-up; the logging; every other page.
SUCCESS CONDITION: live Case 1 shows Six Sevens and game 2 per day to 1 dp, neither shown as 0; typed answers accept the 1 dp value; check and plants pass; Gate green; merged; main's check-site and phone-fit-full on the merge commit green and reported; home.md updated.
STOP IF: no game currently qualifies at 0.1 or more (report the figures; Q2 and Q3 skipped is acceptable, but say so); the widget change would alter any whole-number question's behaviour; anything in DO NOT TOUCH would need a change.
