CONTRACT: RAW-TEX-LAST-2 (Project Claude for Jon, 18 Oct 2026, 13:45).
CLOUD LANE. Save verbatim under docs/handover/contracts/ in the first
claim commit.

TASK: Make the last two games that show raw LaTeX or ASCII maths to
students render it through KaTeX, one game per PR: sequence-solver,
then core-maths-paper2c.

ROOT CAUSE:
1. sequence-solver (findings r-002, open MEDIUM): index.html :327 writes
   q.seq with textContent, so a seq holding TeX (e.g. :232
   'T_n = 3 \\times 2^{n-1}') reaches the student as raw markup. KaTeX
   is loaded (:19-20) and the game's rk() (:315) already renders q.q
   (:330); the seq line was never routed through it.
2. core-maths-paper2c (findings t4-006, open MEDIUM): notation such as
   3^4.2 and e^(kt) is shown as plain text, with KaTeX loaded and never
   called (canon: no ASCII approximations; KaTeX for expressions,
   §7.1.1).

CLASS CHECK: A class: "maths written with textContent or as ASCII,
not KaTeX" has been found in 9 games and fixed one game at a time; these
are the last two open. Within each game, every field that can hold
notation is checked, not only the reported line. The architectural fix,
a shared check that fails on raw TeX or ASCII powers reaching the page,
is shared code (home lane) and is not part of this contract; record in
the handover that it is still missing.

EXACT CHANGE (one PR per game, claimed per the listed-game lane rule in
docs/handover/cloud.md):
1. sequence-solver: every field that can hold notation (seq, q, ask,
   options, hints, explanations, at every level) is rendered through
   KaTeX (rk() or the game's existing mixed-text renderer), never
   textContent. Plain number sequences ("2, 5, 8, 11") must render
   identically to today. List every field and item touched in the PR.
   Close r-002.
2. core-maths-paper2c: every power, exponential or other expression
   written in ASCII is written in TeX and rendered through KaTeX, in
   every field. List every item touched. Close t4-006.
3. Rendering a question must not change its answer key, option text
   meaning, or dataset.val matching (answers match by dataset.val,
   never rendered HTML). Each game's verifier still passes; update it
   only to read the new TeX source, not to change what it checks.
4. Reworded items move content ids in data/check-ledger.json: update as
   CI's Tier 4 layer A directs; never hand-edit ids.
5. Per PR: python scripts/check-changed.py before opening the PR (CI is
   the judge for checks this container cannot run: KaTeX CDN, esprima,
   WebKit, as recorded); look at every changed screen in Chromium at
   390 px and attach screenshots of three items per level; merge on a
   green Gate with main green; watch main's run.
6. Handover entry per game in docs/handover/cloud.md, including: "the
   shared raw-TeX check is still missing (home lane)".

DO NOT TOUCH: answer keys; any other finding in these games; shared
code (schools/assets/), shared scripts/, the workflow, canon,
CLAUDE.md, docs/todo.md; any other game.

SUCCESS CONDITION: No student-facing text in either game shows a
backslash, a brace, an underscore-subscript or a ^ power: every
expression renders as maths. Plain sequences look as before. Both
findings closed with their PRs; verifiers pass; screenshots attached;
both PRs merged; main green after each; handover recorded.

STOP IF:
- Main's latest full run is red.
- A game is in an open home-lane batch branch (skip it, note it).
- Rendering would change an answer key or how an answer is matched.
- KaTeX can't render an item as written (report it with the item; do
  not reword the maths).
- You would schedule any task that merges, pushes or edits.

END OF CONTRACT
