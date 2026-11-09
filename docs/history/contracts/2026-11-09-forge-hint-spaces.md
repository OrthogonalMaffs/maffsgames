FORGE-HINT-SPACES (Project Claude, 9 Nov 13:05)
LANE: cloud (Claude Code web) · TIER: Small · CONTRACT: FORGE-HINT-SPACES (new todo row, closed in this PR) · branch from origin/main 3929b1a or later. No other lane is running. Stop at a green Gate for Project Claude's review and Jon's "merge"; do not merge. Not a draft. Save this contract verbatim in docs/handover/contracts/ in the first commit. Claim formula-forge in its own commit first; release it in the PR.
FIRST COMMIT ALSO (#717 leftovers): git mv docs/handover/contracts/2026-11-09-header-fit.md to docs/history/contracts/; cloud.md's HEADER-FIT entry → "merged as 3929b1a (main run 42618722393 green)".
CONTRACT EXCEPTION (explicit, as in #714–#717): this PR adds and closes its own todo row. Edit no rule file.

TASK: Make Formula Forge's Hint 2 read properly (it currently loses every space on 33 of 45 questions, e.g. "2A = bh.Nowdividebyb.").
ROOT CAUSE: index.html:465 renders hint2 through rkStr(), which sends the whole string to KaTeX in maths mode; 33 hint2 strings are English sentences, and maths mode drops the spaces between words.
CLASS CHECK: The class (prose sent to KaTeX maths mode) is already fixed at the shared layer: canon §7's rule and schools/assets/mathtext.js (MaffsText), enforced by B7. This game never adopted it. Fix at the game's call site, one convention for the whole field: every hint2 marks its maths with \( \) and renders through MaffsText.html(), so the 12 pure-maths hints (wrapped whole in \( \)) and the 33 prose hints use the same path. Not 33 \text{} patches.
EXACT CHANGE:
1. games/formula-forge/index.html: load ../../schools/assets/mathtext.js (after KaTeX, as test-the-claim does). At :465 render hint2 (and the hint1 fallback in that expression) with MaffsText.html() instead of rkStr().
2. All 45 hint2 strings: wrap each piece of maths in \( \), leave the English as plain text. Pure-maths hints are wrapped whole: '\\(d = \\dfrac{C}{\\pi}\\)'. Unicode maths becomes LaTeX inside the delimiters ("I²" → "\\(I^2\\)"). No word, number or operation changes.
3. Leave q.steps and every other rkStr() call unchanged unless B7 flags them; report any it flags, do not fix them here.
4. data/check-ledger.json: python scripts/check-banks.py --only formula-forge --write-ledger; the only change is the removal of the 33 B7 Q.hint2 entries (B7 → pass). Leave any line-number drift as it is on main (put stale line fields back by hand if the rewrite moves them, as #714 did).
5. Proof in the PR body: in Chromium, open Hint 2 on every one of the 45 questions at all three levels; 45 of 45 render with spaces between words and the maths as maths; quote three before and after (one pure-maths). scripts/verify-formula-forge.py passes; check-banks.py --ci passes.
6. docs/todo.md: add a row FORGE-HINT-SPACES (B7 ledger debt, formula-forge, 33 hint2 strings) with today's date and this PR, and move it straight to docs/history/todo-done.md under "Closed by fix PRs (Nov 2026)".
7. /updates/: one dated line in plain words for Jon to confirm, e.g. "Formula Forge: Hint 2 now reads properly, with spaces between the words."
8. Release the claim; close-out entry in docs/handover/cloud.md.
DO NOT TOUCH: hint1 text and how it is shown; questions, answers, marking, steps; schools/assets/ (load mathtext.js, do not edit it); any other game; other ledger entries; Gate files; canon; AGENTS.md and docs/rules/; other todo rows; home.md.
SUCCESS CONDITION: 45 of 45 Hint 2s read with spaces and maths rendered; B7 passes for formula-forge with exactly 33 entries removed; verifier and checks green; row added and closed; /updates/ line drafted; claim released; Gate green; stopped for review.
STOP IF: a hint needs a wording or maths change to render (report it, do not change it); --write-ledger changes anything beyond the 33 entries other than stale line fields; mathtext.js would need editing; another lane or claim holds formula-forge.
