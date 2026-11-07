# PIE-CHARTS-BANK: the report (27 Oct 2026)

**PIE-CHARTS-BANK (26-27 Oct, Jon's contract via Project Claude; PR and main run: see the line in `home.md` once merged).** The first bank-first topic: a `pie-charts` bank of **60 questions**, 12 in each of five stages, matchday pie sales at a sports stadium (home end, away end, family stand, main stand; steak, chicken balti, cheese and onion, mince, vegetable).

**Stages, checked against Jon's agreed spec (27 Oct; the first build had not read it):**
1. **Read it:** the fraction a sector shows, 180°, 90° and 120° first; 8 direct, 4 "only one other sector" (the rest of 360°). Answer: a fraction in its simplest form.
2. **Find the amount given the total:** 12, all with the total stated. *Changed on 27 Oct:* the first build had two "you can't tell" questions here (no total given); they are stage 4's idea, so they are now two more amounts (135° and 210°).
3. **One sector's angle from a frequency table:** 12 tables, 3 to 5 pies; answer in degrees.
4. **Can you tell?:** 12. Two charts with different totals and no totals given (the main misconception): **"you can't tell" is correct in 5**; wrong in 7 (both totals given 3, the same total stated 2, two sectors on one chart 2), so a student cannot always answer "can't tell".
5. **Work backwards from one sector's angle and frequency to the total:** 12, all the total. *Changed on 27 Oct:* the first build had four "find another sector" and two "you can't tell" here; all six are now totals (150°/25, 135°/27, 40°/6, 80°/16, 36°/9, 100°/20).
The generator keeps its `other`, `cant` and stage-2 `cant` kinds, because the game "Who Ate All the Pies?" loads the same file (canon 8.2.1); only the slot tables, which decide the bank, changed. `pie_selftest()` now takes its "can't tell" plant from stage 4.

**Calculator optional throughout:** every pie question is `calc: "optional"` (new third value, `docs/six-ps-schema.md`); **48 of 60** also carry `try_without: true` (every division by a friendly divisor and a whole number); the page shows "Calculator optional" and, for those 48, "Try without a calculator". **No "Want more practice?" link:** the topic has no game (Jon, confirmed); a bank-first topic's row has game slug `None` and `route` `null`, and the results and the nudge name no game for it.

**Generator and checks:** `schools/assets/pie-chart-generator.js` (`MaffsPieCharts.question(stage, slot, rng)`, seedable, no DOM); `gen-six-ps.py` runs it in Chromium, one fixed seed a slot (`stage*100+slot+1`). `pie_faults()` / `pie_expected()` recompute every answer, named slip, "you can't tell", the friendly flag, whole-degree angles summing to 360 and whole amounts, from the question's own data; `pie_selftest()` plants seven faults, each caught. Diagram check: 444 diagrams, **0 faulty** after the labels are moved. `gen-six-ps.py --check` passes (33 banks). `verify-the-6-ps.py` has a session test that always draws the pie topic, and plants for the two calc labels.

**Topic row (Jon to confirm):** pie-charts 4.0 marks, 4 series (the audit's figure), bands 2 to 4 (stage 1 band 2, stages 2 and 3 band 3, stages 4 and 5 band 4).

**Also owed:** the 27 Oct 05:40 UTC answer-counts run; as of 07:25 UTC that slot had not started (the newest scheduled run was 26 Oct 21:52 UTC, success, edc035ec).
