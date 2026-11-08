TASK: Build As You Can See, the reading-charts game, with its question bank, unlisted.
ROOT CAUSE: Reading charts carries 68 OCR Foundation marks, mostly at grades 1–3, and no game covers it. Jon named it 27 Oct 2026. No bank exists, so the bank is written first in its own module and the game imports it (bank-first rule, canon §8.2.1), so The 6 P's can import it later.
CLASS CHECK: Local: a new game and bank, new files only. One possible shared need: tolerance marking for readings from a graph. If MaffsAnswer already supports a value-with-tolerance match, use it; if not, do NOT add it to the shared file. Implement it inside the bank as an accepted interval per question, and report it as a candidate for the shared helper (two-plus games would make it a class).
EXACT CHANGE:
1. Bank module, same pattern as the pie-charts bank: at least 12 distinct questions per stage, 60 in total, fixed seed, charts generated as data and drawn in SVG. Every answer computed from the chart data, never typed; a verifier recomputes through a separate code path, with planted faults.
2. games/as-you-can-see/. Five stages, the Who Ate All the Pies? pattern (worked example, 10 questions easiest first, "Next: Stage N+1"):
   1 Pictograms: the key; half and quarter symbols.
   2 Bar charts: scales in 2s, 5s, 10s; comparisons; composite and dual bars.
   3 Line graphs and time series: reading values; trends; "can you tell between the points?".
   4 Scatter graphs: type of correlation; estimating from a line of best fit; outliers; correlation is not cause; estimating beyond the data is unreliable.
   5 Is this chart lying?: truncated axes, uneven scales, 3D or area-scaled pictures, missing labels.
3. Answers: typed numbers for readings, accepted within half a minor gridline; multiple choice with the reason for correlation type, "you can't tell" and stage 5. "You can't tell" is a genuine option from time to time in stages 3 and 4. No calculator.
4. Named slips, matched by value: key ignored (symbols counted); half symbol counted as a whole or as 1; reading to the wrong gridline on a 2s/5s scale; composite segment read at its top instead of its length; value trusted beyond the data; correlation taken as cause; truncated axis taken at face value.
5. Chart labels at least 12 px; series told apart by label or pattern as well as colour. Plain wording; setting and jokes are Jon's.
6. Theme from the roster levels (KS3, GCSE). Phone fit with the keypad open at 320×568, 360×640, 375×667, 390×844. Next roster row, Unlisted.
DO NOT TOUCH: Shared files (MaffsAnswer, theme.css, fold files, measure-phone-fit.py), the lists (games.json, sitemap, homepage, Essentials), any other game or bank.
SUCCESS CONDITION: Merged once CI is green, unlisted, main green. build.md records the state, a "Decided for you" list, and one screenshot per stage at 375×667 in your scratchpad.
STOP IF: A chart can't be drawn legibly at 320×568 even at 12 px labels: park that stage on the known-failures list and report. A stage can't reach 12 distinct questions without repeating a chart: build the rest, show "Coming soon" there, and report. Fetch main first: merges go through the fixed gate, and --part lines now fail the plan job.
