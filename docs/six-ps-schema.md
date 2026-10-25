# The 6 P's: question bank schema (schema 1)

The shape of every question The 6 P's player asks (contract SIX-PS-PLAYER (a), Project Claude's schema of 25 Oct
2026, given in full). The home lane writes the banks to it; the player (`the-6-ps/index.html`) renders and marks any
question in it and knows nothing about topics, so adding a topic is a bank file and never a page change.

Two notes are Code Claude's, both marked **Recorded:** the maths renderer (the schema asked for the repo's
convention to be recorded) and SR-3 (a standing ruling the schema refers to).

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
| `number` | `{"value": 12.5}` | `{"rule": "exact"}` (default: numerically equal) or `{"rule": "range", "lo": 12, "hi": 13}` (inclusive). Rounding instructions are stated in the stem and the stored value is already rounded; a student's 2.5 equals a stored 2.50. |
| `money` | `{"pence": 350}` | Exact only. Input in pounds, "£" optional; 3.5 and 3.50 both equal 350p. |
| `fraction` | `{"n": 3, "d": 4}`, or with a whole part `{"w": 1, "n": 1, "d": 4}`; sign on `n` (or `w`) | `{"rule": "equivalent"}` (default: any equal value, either form) or `{"rule": "simplest"}` (equal value AND lowest terms, in the form asked: mixed if the answer has `w`). |
| `ratio` | `{"parts": [2, 3]}` (2 or 3 parts, order matters) | `"equivalent"` (default: same proportions) or `"simplest"` (same proportions AND no common factor). |
| `coordinates` | `{"x": -2, "y": 5}` | Exact. |
| `choice` | `{"val": "b"}` | Marked by `dataset.val`. |
| `number_unit` | `{"value": 40, "unit": "km/h"}` | Both must match (value by the `number` rule above). |

**Equal but not in the form asked** (a `fraction` or `ratio` under `"simplest"` that has the right value but is not
in lowest terms, or not in the form asked) gets SR-3's format message, not the "wrong answer" feedback.

**Recorded (SR-3, canon §0.3):** the schema as given says such an answer is "marked wrong with SR-3's format
message". SR-3 says a right value in the wrong form "is never marked right or wrong: no score, no penalty, no
event". The player follows SR-3: the format message shows, nothing is marked or logged, and the student answers
again. Jon's ruling overrides this if he means otherwise.

## Input parsing

Trim spaces; strip thousands commas (`1,200`); accept the Unicode minus `−` as `-`. Anything else that is not a
number is rejected with the "That isn't a number" message, not marked as a wrong answer.

## Slips

After a wrong answer, compare it with each slip's `answer` by the same rule that marks the question; on a match show
that slip's `line`, then the worked solution.
