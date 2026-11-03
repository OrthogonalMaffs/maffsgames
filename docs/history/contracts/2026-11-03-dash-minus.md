# DASH-MINUS (received 3 Nov 2026, cloud lane, Claude Code)

Saved verbatim on receipt (canon §7.8.2, CONTRACTS-FOLDER).

## Contract (verbatim)

CONTRACT: DASH-MINUS
Tier: Shared · Lane: cloud · Implementer: Claude Code (cloud)

TASK
Stop dashes in student-facing text being read as minus signs: add the rule to canon, a CI check, and fix every
occurrence.

ROOT CAUSE
Answer options such as "Victor is wrong — x = 625" (Terrible Advice) read as "−x = 625": an em dash, or a spaced en
dash, directly before a number, a variable or a minus sign looks like a minus. A sweep on 1 Nov found 84 such
occurrences in 24 games (most: terrible-advice 16, spot-the-muppet 13, better-value 11, wrong-on-the-internet 10).
Nothing checks for it. Jon's rule (3 Nov 2026): never put a dash directly before a number, a variable or a minus sign
in text students read; use a colon or rephrase.

CLASS CHECK
Yes: the same shape in 24 games. Fix with one rule, one check over every student-facing file, and the sweep.

EXACT CHANGE
1. canon §7.1 (or the student-text section): Jon's rule, verbatim; reason in §12.
2. New scripts/check-dash-minus.py (ci-line; not a Gate file): in student-facing text (games/*/index.html,
   the-6-ps/, escape-rooms/**/room.js, banks and generators under schools/assets/ that produce question or option
   text), fail an em dash (—) or a spaced en dash (" – ") followed by optional space and then a digit, "£", a minus
   sign (− or -), an opening bracket, or a single-letter variable. An unspaced en dash between two numbers (a range,
   "1–3") is allowed. Code comments are not student-facing. --selftest plants for each pattern and for the range
   exception.
3. Fix every hit: a colon ("Victor is wrong: x = 625") or a rephrase that keeps the meaning. Where a game is listed,
   the fix is text only. Each changed game's verifier passes.

DO NOT TOUCH
Meaning of any question, option or answer; marking; layout; Gate files. TeX inside KaTeX strings is not prose.

SUCCESS CONDITION
Check fails on none (no warn list needed once the sweep lands); plants caught; a table in the PR of every change
(file, before, after); Gate green (cloud ruling: no local check-changed.py; run each touched game's verifier); Shared
review; stop for Jon's "merge"; Record line.

STOP IF
A hit cannot be fixed without changing what a question says (list it for Jon); more than 150 hits (report the count by
file before fixing).

## Amendment 1 (Jon, 3 Nov 2026, chat, verbatim)

Rulings (Jon, 3 Nov), recorded in the contract file as Amendment 1:
1. Scope: all 206 in this one PR. "£" was meant: "better value — £74" is a dash before a number. Text only, a colon
   or a rephrase each, every touched game's verifier run, the before/after table in the PR grouped by file.
2. Both judgement calls approved: article "a"/"A"/"I" and "A-Level" count as words as you set them; runtime values
   (${...}) count, and 52dle's "— ${puzzle.cat}" is judged when fixing.
3. Claims: one claim commit naming every listed game the sweep touches, released in the PR. It locks them against
   home-lane batches; the home lane's queue today (roster sign-off, todo, index.html, next-control.js, the-6-ps)
   touches none of them.
4. games/the-perfect-prank/: fix it. It is live and linked from the escape-rooms hub (an earlier 40-minute room),
   and is kept out of the roster on purpose (docs/todo.md), so students read it.
5. glorious-gantt: fix it with the rest.
Then carry on to the contract's end: Gate green, Shared review, stop for Jon's "merge".
