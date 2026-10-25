# Contract SIX-PS-PLAYER (Jon, 25 Oct 2026), verbatim

TASK: Replace The 6 P's launches into games with an in-page question player that asks each topic's five questions from its bank and ends the topic after the fifth.

ROOT CAUSE: The page hands each topic to one of 29 games through burst.js. A burst has no clear end at five (the game carries on to its own session length), the way back is easy to miss, and the games differ in style. Jon's ruling, 25 Oct 2026: self-contained, one stylesheet, no hand-off.

CLASS CHECK: Yes. Every burst fault traces to the hand-off design, so the fix replaces the design rather than patching burst.js. The player is topic-blind: it renders any question in the shared schema, so adding a topic is a bank file and never a page change.

EXACT CHANGE:
(a) First, its own small PR: docs/six-ps-schema.md, the question schema exactly as the spec gives it (id, topic, source, band, calc, stem, diagram, format, answer, accept, unit, options, worked, slip) and the seven formats (number, money, fraction, ratio, coordinates, choice, number + unit). The home lane starts once this merges; say so in the handover.
(b) the-6-ps/index.html: remove the launch links and the ?done= return handling. Add the player: load schools/assets/six-ps/<topic-id>.json for each drawn topic; pick five, easiest band first, avoiding ids seen recently on this device (localStorage, wrapped in try/catch); render stem with KaTeX and any SVG diagram; one input per format; mark by value with the accept rule (choice by dataset.val), never by string; show right or wrong at once, the matching slip line then the worked solution on a wrong answer, worked solution one tap away on a right one; after the fifth answer a topic card ("Ratio: 4 of 5", its exam weight, Next topic) with no sixth question; header "Question n of 5 · Topic m of 6". Keep session drawing, results, nudge, tick-list and resume as they are. Results add "Want more practice? <game>" as a plain link from each topic's route slug.
(c) Look: theme.css, light palette, portal tokens (white, navy #1a2744, teal #0d9488, Outfit); no emoji, no age words. Coming soon: the three highest-mark topics, the rest in a closed <details> "See all n more topics", no "in development" anywhere (SIX-PS-SOON's intent).
(d) Analytics: existing events only, game_slug "the-6-ps": game_started (session), question_answered (correct, detail = topic id), game_completed (session); the tick-list event unchanged.
(e) scripts/verify-the-6-ps.py rewritten for the player, using fixture banks under scripts/fixtures/ that cover all seven formats (not published): a full session in Chromium at 1280 and 320 px with every format answered right and wrong; the topic ends at five; results correct; resume with storage working and blocked; no sideways scroll at 320 px. Plants, each caught: a sixth question shown; an answer marked by string; a wrong answer marked right; a coming-soon topic drawn; "in development" restored.

DO NOT TOUCH: schools/assets/exam-topics-ocr-foundation.json and gen-exam-topics.py. schools/assets/six-ps/ (the home lane writes the banks). Any game. burst.js and its hooks (cleanup after launch). analytics.js. The page stays unlisted.

SUCCESS CONDITION: Schema doc merged first. With fixture banks, a full session plays end to end at 1280 and 320 px, every format marks right and wrong correctly, every topic stops at five, results and resume work, all plants caught. CI line time from the PR's own run under 60% of its group budget. Main green after merge. Work committed and handover written, naming what the home lane needs.

STOP IF: The schema needs a field the spec does not give. A format cannot be marked by value. Anything needs new data collection. KaTeX cannot render a stem form the formats need. Removing the burst handling would break anything outside the-6-ps/.

# Project Claude, 25 Oct 2026, verbatim (answer to the session's STOP: the spec was not in the session)

From Project Claude, 25 Oct 2026. Thank you for stopping: the spec lives only in the project, so here is the schema in full. It replaces "exactly as the spec gives it" in (a).

SIX-PS-PLAYER (a): THE SCHEMA, IN FULL. Commit this as docs/six-ps-schema.md.

BANK FILE: schools/assets/six-ps/<topic-id>.json = {"topic": "<topic-id>", "schema": 1, "questions": [ ... ]}

QUESTION FIELDS
- id: "<topic-id>-<source hash, 8 hex>". Stable: the same source item always gives the same id, so the device's "seen recently" list survives regeneration.
- topic: the topic id from exam-topics-ocr-foundation.json.
- source: {"game": "<slug>", "ref": "<where in the game: variable path and index, e.g. QUESTIONS.ks3[12]; or generator:<function>:<seed>>"}. Provenance, not a paper reference.
- band: integer 1 to 5, the grade the question is pitched at. (The topic file's "2-5" ranges are per topic; each question gets one integer.)
- calc: true or false. Shown as "Calculator" or "Non-calculator".
- stem: plain text; maths inside \( ... \), rendered by KaTeX auto-render. No HTML. If the repo's existing KaTeX/MaffsText convention uses other delimiters, use the repo's and record it here.
- diagram: null, or a self-contained inline SVG string (no external references, colours via currentColor or theme tokens, a viewBox, labels as text). "Not drawn accurately" goes in the stem where the paper would say it.
- format: one of number, money, fraction, ratio, coordinates, choice, number_unit.
- answer: shape by format (below).
- accept: by format (below). Absent means the format's default.
- unit: number only, optional: a label shown after the box (e.g. "cm²"). Not marked.
- units: number_unit only: 3 or 4 unit labels shown as buttons; the answer's unit is one of them.
- options: choice only: exactly 4 of {"val": "a"|"b"|"c"|"d", "label": "<text, \( \) allowed>"}. val is the dataset.val key; labels must be distinct.
- worked: array of 0 to 5 strings, one line each (\( \) allowed). Empty only for items on the missing-worked list; the player then shows the answer alone.
- slip: array (may be empty) of {"answer": <same shape as answer>, "line": "<what mistake gives this>"}.

ANSWER SHAPES AND MARKING (by value, never by string)
- number: {"value": 12.5}. accept: {"rule": "exact"} (default: numerically equal) or {"rule": "range", "lo": 12, "hi": 13} (inclusive). Rounding instructions are stated in the stem and the stored value is already rounded; a student's 2.5 equals a stored 2.50.
- money: {"pence": 350}. Input in pounds; "£" optional; 3.5 and 3.50 both equal 350p. accept: exact only.
- fraction: {"n": 3, "d": 4}, or with a whole part {"w": 1, "n": 1, "d": 4}; sign on n (or w). accept: {"rule": "equivalent"} (default: any equal value, either form) or {"rule": "simplest"} (equal value AND lowest terms, in the form asked: mixed if the answer has w). Equal but not in the form asked: marked wrong with SR-3's format message, not the "wrong answer" feedback.
- ratio: {"parts": [2, 3]} (2 or 3 parts, order matters). accept: "equivalent" (default: same proportions) or "simplest" (same proportions AND no common factor), with SR-3's format message for equal-but-not-simplest.
- coordinates: {"x": -2, "y": 5}. exact.
- choice: {"val": "b"}. Marked by dataset.val.
- number_unit: {"value": 40, "unit": "km/h"}. Both must match (value by the number rule above).

INPUT PARSING: trim spaces; strip thousands commas (1,200); accept the Unicode minus "−" as "-"; reject anything else that is not a number with the "That isn't a number" message, not as a wrong answer.

SLIPS: after a wrong answer, compare it with each slip's answer by the same rule that marks the question; on a match show that slip's line, then the worked solution.

ANALYTICS (Jon's ruling, 25 Oct 2026), replacing (d)'s "detail = topic id": question_answered carries filter_type='six_ps' and filter_value='v1|topic=<id>', as your recommendation and the 24 Oct ruling 2 pattern. game_started and game_completed unchanged.

# Jon via Project Claude, 25 Oct 2026, verbatim (answers to the session's two questions)

1. Topics with no bank: option 1. Draw as now; a topic whose bank does not load shows "This topic's questions aren't ready yet" with Skip only. This is interim: the home lane will make the topic file count a topic as covered only when its bank exists, so no student will see that card once the page is listed.
2. SR-3: confirmed as you wrote it. A right value in the wrong form gets the format message and is not marked (no score, no penalty, no event). Keep the doc's note; my "marked wrong" line was the error.

# Jon, 25 Oct 2026, verbatim (answer to the session's second STOP: the schema against MaffsAnswer)

"happy with your rulings there sir."

(Approving the session's three recommendations: (1) an optional `dp` on `number` and `number_unit` answers whose stem states a rounding, marked by `MaffsAnswer.decimal`, else `MaffsAnswer.exact`; (2) money by SR-2, so 3.5 gets the format message; (3) thousands commas and "−" stay unreadable, as `MaffsAnswer` reads them.)
