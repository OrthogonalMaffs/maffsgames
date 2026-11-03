CONTRACT: FRACTION-STACK
Tier: Shared · Lane: cloud · Implementer: Claude Code (cloud)

TASK
Make every typed fraction answer use the shared stacked input, starting with Who Ate All the Pies?, and add a CI check
so no game builds its own fraction boxes again.

ROOT CAUSE
Canon §7.6.1 (Jon's ruling): every fraction on screen is stacked, never 1/3. A shared stacked input,
schools/assets/fraction-input.js (MaffsFractionInput), exists since 27 Oct, but nothing requires games to use it: Who
Ate All the Pies? hand-builds side-by-side boxes with a "/" between them (games/who-ate-all-the-pies/index.html, the
Q.type === 'fraction' branch), and The 6 P's keeps its own copy (case 'fraction', with mixed numbers).

CLASS CHECK
Yes: the same shape (hand-built fraction boxes) in more than one component, and the missing safety is a shared rule
with no check. Fix at the shared layer: games use MaffsFractionInput, and a CI check enforces it, warning first per
canon §7.8.4 for pages not yet moved. A one-off CSS fix to stack Pies' own boxes would be the wrong fix.

EXACT CHANGE
1. games/who-ate-all-the-pies/index.html: replace the hand-built fraction boxes with MaffsFractionInput.mount (load
   ../../schools/assets/fraction-input.js), label "Your answer as a fraction". Hand f.inputs to MaffsKeypad as its
   targets, as possibly-maybe does. Marking reads what the shared input returns (f.raw() for MaffsAnswer.fractionForm
   when lowest terms are asked; f.value() otherwise); the marking rules themselves do not change. Remove the game's
   own .slash markup and CSS. Update scripts/verify-who-ate-all-the-pies.py's selectors to the shared input, and add a
   plant: the side-by-side boxes restored is CAUGHT.
2. New scripts/check-fraction-input.py (with a ci-line header; not a Gate file): every page under games/ and the-6-ps/
   that offers a typed fraction answer (two numeric inputs for a numerator and denominator, found by their labels or
   a separator between them) loads fraction-input.js and builds no fraction boxes of its own. Warn first (canon
   §7.8.4): a shrink-only warn list, scripts/fraction-input-warn.json, seeded with every page that fails today except
   who-ate-all-the-pies (expected: the-6-ps, because it needs a whole-number part the shared input lacks; list any
   others you find). --selftest with plants: a page with its own side-by-side boxes fails; a warn-listed one warns;
   adding to the warn list fails.
3. canon §7.6.1: one line after Jon's ruling: "Typed fractions use MaffsFractionInput
   (schools/assets/fraction-input.js); check-fraction-input.py enforces it." Reason in §12 (this contract, 3 Nov).
4. Cloud handover Queue: one line for the follow-up: give MaffsFractionInput an optional whole-number box for mixed
   numbers, then move the-6-ps (and any other warn-listed page) onto it.

DO NOT TOUCH
- schools/assets/fraction-input.js (its whole-number box is the follow-up), the-6-ps/, possibly-maybe.
- Pies' questions, bank, marking rules, look (PIES-LOOK just merged) and charts.
- Gate files (workflow, scripts/ci-*, ci_shards.py, merge-pr.py, check-context-size.py, check-changed.py) beyond the
  new check's own ci-line header.
- AGENTS.md, CLAUDE.md, docs/rules/.

SUCCESS CONDITION
Pies shows its fraction answer stacked (numerator over a bar over denominator) through MaffsFractionInput; its verifier
passes with the new plant CAUGHT; Pies' phone rule still holds with the keypad open at 320×568, 375×667 and 390×844
(Check above the fold; measurements in the PR); the new check is in CI, warning first, selftest proving all three plants;
canon line added; Gate green (standing ruling: no local check-changed.py); handover current, ending with its Record line;
stop at Gate green for Project Claude review and Jon's "merge".

STOP IF
- A Pies question needs a numerator or denominator longer than the shared input's three digits.
- The stacked input cannot keep Check above the fold at 320×568 with the keypad open.
- Moving Pies onto the shared input needs a change to fraction-input.js.
- The check cannot tell a typed-fraction page from other pages without false alarms (report the cases).
