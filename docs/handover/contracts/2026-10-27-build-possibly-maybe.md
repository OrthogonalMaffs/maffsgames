CONTRACT 5 (build lane), 27 Oct 2026, from Jon. Saved verbatim, with Jon's amendment below it.

TASK: Build Possibly, Maybe, the Foundation probability game, with its question bank, unlisted.
ROOT CAUSE: Probability carries 88 OCR Foundation marks (grades 1–5), and no game covers it as a whole. Jon named it 27 Oct 2026. Bank-first: the bank is written first as its own module, and the game imports it.
CLASS CHECK: Local: a new game and bank, new files only (infrastructure freeze until Mon 2 Nov). Two possible duplications to check first: (1) if a probability bank already exists as an importable module (e.g. behind The 6 P's basic-probability topic), extend it with these stages instead of writing a second one; if The 6 P's questions live only in its own data, write the new bank and note the overlap in the lanes' notes file for next week. (2) Fraction entry is a shared need: do NOT build a game-local fraction keypad. Fraction answers are multiple choice until the shared keypad's fraction key lands (deferred). [SUPERSEDED by the amendment below.]
EXACT CHANGE:
1. Bank module, pie-charts bank pattern: at least 12 distinct questions per stage, 60 in total, fixed seed; every answer computed, never typed; a verifier recomputes through a separate path, with planted faults.
2. games/possibly-maybe/. Five stages, Who Ate All the Pies? pattern (worked example, 10 questions easiest first, "Next: Stage N+1"):
   1 The scale: words to numbers (impossible 0, unlikely, evens ½, likely, certain 1); placing events; fraction, decimal or percentage; nothing outside 0 to 1.
   2 Not, and the missing one: P(not A) = 1 − P(A); a table of outcomes summing to 1, find the missing one; at grade 4, "x and 2x" in the table.
   3 Listing outcomes: sample spaces (two spinners, two dice, coin and dice); favourable over total; the product rule for combinations (menu choices).
   4 Expected and relative frequency: probability × trials; relative frequency from results; the more reliable estimate (more trials); "is the dice fair?".
   5 Tree diagrams: independent events; multiply along, add between; "at least one" as 1 − P(none). No without-replacement this time.
3. Answers: fractions by multiple choice with named distractors (dataset.val, matched by value, equivalent fractions equal); decimals and whole numbers typed. No calculator. [Fractions: SUPERSEDED by the amendment below.]
4. Named slips: adding along branches; P(not A) as 1 − the numerator, or as a whole number; 2+3 and 3+2 counted as one; all dice sums equally likely; expected frequency by dividing; a probability above 1; gambler's fallacy ("five heads, so tails is due"); few trials trusted over many.
5. Diagrams (spinners, sample-space grids, trees) in SVG; labels at least 12 px. Plain wording; setting and jokes are Jon's. Out of scope: Venn diagrams, two-way tables, conditional probability.
6. Theme from the roster levels (KS3, GCSE). Phone fit at 320×568, 360×640, 375×667, 390×844. Next roster row, Unlisted. New verifier lines use the shard work units (#578).
DO NOT TOUCH: Shared files (keypad, MaffsAnswer, theme.css, fold files, bank_common.py, measure-phone-fit.py), the lists, any other game or bank.
SUCCESS CONDITION: Merged once CI is green, unlisted, main green. build.md records the state, a "Decided for you" list, and one screenshot per stage at 375×667 in your scratchpad.
STOP IF: A tree diagram can't fit at 320×568 at 12 px labels: park stage 5 on the known-failures list and report. A stage can't reach 12 distinct questions: build the rest, show "Coming soon" there, report. Plan or CI blocks on something outside your files: re-run once if it's a flake (log it in the notes file), otherwise park the PR with the numbers. No override, no hand-splits.

AMENDMENT (Jon, 27 Oct 2026): Amendment to Possibly, Maybe: fraction answers are typed, not multiple choice, using The 6 P's numerator/denominator input. If that input is already a shared module, use it. If it lives inside The 6 P's page, extract it into a NEW shared file (no edits to existing shared files, and don't change The 6 P's this week), use it here, and add "switch The 6 P's to the shared fraction input" to the lanes' notes file for next week. Matched by value; equivalent fractions are equal; unsimplified fractions accepted unless the question asks for simplest form. Phone fit applies with the two boxes.
