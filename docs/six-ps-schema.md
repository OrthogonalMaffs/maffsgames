# The 6 P's: question bank schema (schema 1)

The shape of every question The 6 P's player asks (contract SIX-PS-PLAYER (a), Project Claude's schema of 25 Oct
2026, given in full). The home lane writes the banks to it; the player (`the-6-ps/index.html`) renders and marks any
question in it and knows nothing about topics, so adding a topic is a bank file and never a page change.

Notes marked **Recorded:** are Code Claude's: the maths renderer (the schema asked for the repo's convention to be
recorded) and SR-3 (a standing ruling the schema refers to). **Marking through `MaffsAnswer`** (below) is Jon's ruling
of 25 Oct 2026, which brought the schema into line with canon §7.1.2, §7.1.3, SR-2 and SR-3: the optional `dp`, money
at two decimal places, and `MaffsAnswer`'s reading of a typed number replace what the schema first said.

## Bank file

`schools/assets/six-ps/<topic-id>.json`:

```json
{"topic": "<topic-id>", "schema": 1, "questions": [ ... ]}
```

## Question fields

- **id**: `"<topic-id>-<source hash, 8 hex>"`. Stable: the same source item always gives the same id, so the
  device's "seen recently" list survives regeneration.
- **topic**: the topic id from `schools/assets/exam-topics-ocr-foundation.json`.
- **source**: `{"game": "<slug>", "ref": "<where in the game>"}`, where `ref` is a variable path and index (e.g.
  `QUESTIONS.ks3[12]`) or `generator:<function>:<seed>`. Provenance, not a paper reference.
- **band**: integer 1 to 5, the grade the question is pitched at. (The topic file's `"2-5"` ranges are per topic;
  each question gets one integer.)
- **calc**: `true` or `false`. Shown as "Calculator" or "Non-calculator".
- **stem**: plain text; maths inside `\( ... \)`. No HTML. "Not drawn accurately" goes in the stem where the paper
  would say it.
- **diagram**: `null`, or a self-contained inline SVG string: no external references, colours via `currentColor`
  or theme tokens, a `viewBox`, labels as text.
- **format**: one of `number`, `money`, `fraction`, `ratio`, `coordinates`, `choice`, `number_unit`.
- **answer**: shape by format (below).
- **accept**: by format (below). Absent means the format's default.
- **unit**: `number` only, optional: a label shown after the box (e.g. `"cm²"`). Not marked.
- **units**: `number_unit` only: 3 or 4 unit labels shown as buttons; the answer's unit is one of them.
- **options**: `choice` only: exactly 4 of `{"val": "a"|"b"|"c"|"d", "label": "<text, \( \) allowed>"}`. `val` is
  the `dataset.val` key; labels must be distinct.
- **worked**: array of 0 to 5 strings, one line each (`\( \)` allowed). Empty only for items on the missing-worked
  list; the player then shows the answer alone.
- **slip**: array (may be empty) of `{"answer": <same shape as answer>, "line": "<what mistake gives this>"}`.

**Recorded (the maths renderer):** the repo's convention uses the same delimiter. Every string with `\( ... \)`
(`stem`, `options[].label`, `worked[]`, `slip[].line`) is rendered by `MaffsText.html()`
(`schools/assets/mathtext.js`), not KaTeX auto-render: it HTML-escapes the prose (so "no HTML" holds even if a bank
breaks it), renders each maths segment through KaTeX inline with `throwOnError: false`, and keeps touching
punctuation on the maths segment's line. A string with no `\( \)` is plain text. **Never `$...$`:** `$` is a literal
in this platform's prose (currency).

## Answer shapes and marking

By value, never by string.

| format | answer | accept |
|---|---|---|
| `number` | `{"value": 12.5}`, or `{"value": 12.5, "dp": 1}` when the stem states a rounding | `{"rule": "exact"}` (default: numerically equal) or `{"rule": "range", "lo": 12, "hi": 13}` (inclusive). Rounding instructions are stated in the stem and the stored value is already rounded; a student's 2.5 equals a stored 2.50. **`dp`** (integer, 0 or more; Jon, 25 Oct 2026) is the decimal places the stem asks for: with it the answer is marked by `MaffsAnswer.decimal(raw, value, dp)`, so a value that rounds to the key without equalling it (2.47 for 2.5 at 1 d.p.) gets SR-3's format message; without it, by `MaffsAnswer.exact(raw, value)`. `dp` is never given with `range`. |
| `money` | `{"pence": 350}` | Exact only, by `MaffsAnswer.money(raw, pence / 100)` (canon §7.1.3, SR-2). Input in pounds, "£" optional. Pence are written to exactly 2 d.p.: 3.50 is correct, **3.5 gets the format message** (Jon, 25 Oct 2026: SR-2, replacing the schema's "3.5 and 3.50 both equal 350p"). A whole number of pounds needs no .00 (3 and 3.00 for 300p). |
| `fraction` | `{"n": 3, "d": 4}`, or with a whole part `{"w": 1, "n": 1, "d": 4}`; sign on `n` (or `w`) | `{"rule": "equivalent"}` (default: any equal value, either form) or `{"rule": "simplest"}` (equal value AND lowest terms, in the form asked: mixed if the answer has `w`). Typed in a box for the top and one for the bottom, with a box for the whole number only when the answer has `w` (How Many Parts?'s pattern: the phone keypad has no "/"), joined into one string ("3/4", "1 1/4", "-3/4") and marked by `MaffsAnswer.fractionForm` (form `mixed` if the answer has `w`, else `simplest`): under `equivalent` its `format` (equal value, other form) counts as correct. |
| `ratio` | `{"parts": [2, 3]}` (2 or 3 parts, order matters) | `"equivalent"` (default: same proportions) or `"simplest"` (same proportions AND no common factor). One box a part, each read by `MaffsAnswer.parse`. |
| `coordinates` | `{"x": -2, "y": 5}` | Exact: each box by `MaffsAnswer.exact`. |
| `choice` | `{"val": "b"}` | Marked by `dataset.val`. |
| `number_unit` | `{"value": 40, "unit": "km/h"}`, `dp` as for `number` | Both must match (value by the `number` rule above). No unit picked: a prompt to pick one, not a mark. |

**Equal but not in the form asked** (a `fraction` or `ratio` under `"simplest"` that has the right value but is not
in lowest terms, or not in the form asked) gets SR-3's format message, not the "wrong answer" feedback.

**A `range` is a reading band** (canon §7.1.2): it never reaches a named wrong answer. Its half-width, the larger
of `value - lo` and `hi - value`, is less than half the gap from `value` to every numeric `slip` answer; the player
drops a question that breaks this, and `value` lies in the range.

**Recorded (SR-3, canon §0.3):** the schema as given says such an answer is "marked wrong with SR-3's format
message". SR-3 says a right value in the wrong form "is never marked right or wrong: no score, no penalty, no
event". The player follows SR-3: the format message shows, nothing is marked or logged, and the student answers
again. Jon's ruling overrides this if he means otherwise.

## Input parsing

Every typed box is read by `MaffsAnswer` (`schools/assets/answer.js`; canon §7.1.3: no game marks a typed number with
its own code). Spaces round the answer are trimmed; a leading "£" is optional on money. **Thousands commas
(`1,200`) and the Unicode minus `−` are unreadable**, as `MaffsAnswer` reads them everywhere on the site (Jon, 25 Oct
2026, replacing the schema's "strip thousands commas; accept −"; the phone keypad types neither). An unreadable
answer gets `MaffsAnswer.message('unreadable', ...)` ("Type just the number, e.g. 12.34", or its fraction wording)
and is not marked.

## Slips

After a wrong answer, compare it with each slip's `answer` by the same rule that marks the question; on a match show
that slip's `line`, then the worked solution.
