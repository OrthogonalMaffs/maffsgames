# PIZZA-CARDS (cloud lane, Game tier, 7 Nov 2026)

Saved verbatim as received.

LANE: cloud (NEW session) · TIER: Game · from current main
COORDINATION: home owns possibly-maybe, who-ate-all-the-pies, as-you-can-see, distinctly-average, hc-factor, i-found-a-mark, better-value, scripts/measure-phone-fit.py, scripts/phone-fit-state.json (PHONE-FIT-RED). Codex owns tools/pack-generator/ (#689). Touch none. Do NOT edit docs/handover/home.md or cloud.md: close-out entry goes in the PR body. Save this contract in docs/handover/contracts/ per AGENTS.md. Claim free-daily-pizza on scripts/answer-lock-state.json first, in its own commit.

TASK: Make Free Daily Pizza's practice cards show their inline fraction on one line and align their titles to the top.
ROOT CAUSE: games/free-daily-pizza/index.html line 56, `.stage-btn span{display:block;...;line-height:1.9}`, is a descendant selector: it also matches every span inside KaTeX's output, so stage 3's \dfrac{3}{5} is broken into stacked blocks and "25% of 80, ⅗ of 45" spreads over the card. The grid then stretches all buttons to that height, and <button> centres content vertically, so stages 1 and 2 sit lower than stage 3.
CLASS CHECK: The bug shape (a descendant `<sel> span{display:block}` that reaches into KaTeX output) can exist in any game that copied it. Step 3 searches the whole library. If it appears in no other game, the bug is local and fixed here. If it appears in any other game, STOP: that becomes a library fix, ruled by Project Claude.
EXACT CHANGE:
1. Line 56: `.stage-btn span` → `.stage-btn > span`; line-height 1.9 → 1.35. Line 55: `.stage-btn b` → `.stage-btn > b`.
2. Line 54 .stage-btn: add `display:flex;flex-direction:column;justify-content:flex-start;align-items:stretch` so content sits at the top of every card.
3. Search every games/*/index.html (and schools/assets/*.css) for a rule whose selector ends in a descendant `span` (or `*`) and sets display:block, in a file that loads KaTeX. Paste every hit with file:line.
4. Screenshots of the menu at 1280 wide, 390x844 and 320x568 in normal and aa, before and after.
5. No /updates/ line.
DO NOT TOUCH: questions, answers, generators, the daily seed, the pizza drawing, every other rule in the file, every other game, schools/assets/**, the files under COORDINATION.
SUCCESS CONDITION: stage 3 reads "25% of 80, ⅗ of 45" with the fraction inline at every size; all five cards' titles start at the same height in each row; no other part of the page changes (before/after screenshots of the game, feedback and results screens identical); phone-fit for free-daily-pizza still passes in all modes; Gate green; contract saved; close-out entry in PR body. Stop for Project Claude's review of the screenshots and Jon's "merge".
STOP IF: step 3 finds the same shape in any other game or shared asset (report the list, fix only Pizza, stop); the fraction still wraps at 320 wide in aa (report the card's width and the fraction's width); any screenshot outside the menu changes.

## Amendment 1 (Jon, 7 Nov 2026, after the STOP), saved verbatim

Thank you — good stop. Rulings, same PR #696, same branch:

1. Log Laws: games/log-laws/index.html:480 `.mode-btn span` → `.mode-btn > span`. That one selector only; nothing else in log-laws changes. Claim log-laws on answer-lock-state.json in its own commit first; release in the PR. Screenshot its mode buttons before/after at 1280 and 320 (normal, aa): expected identical.
2. Class guard: add a check to the Gate's site-wide checks (extend the existing site-wide checker if one fits; otherwise a new scripts/check-katex-css.py, wired the same way). It fails any game that loads KaTeX and has a CSS rule whose selector's last compound is `span` or `*` reached by a descendant (space) combinator, with `display:block` in the declarations. Self-test with planted faults: (a) `.x span{display:block}` fails; (b) `.x > span{display:block}` passes; (c) `.x span{color:red}` passes; (d) `.x *{display:block}` fails. Record the rule in canon §7.1.1 in one sentence. After steps 1–2, the check passes on the whole library.
3. Report: is free-daily-pizza aa on scripts/phone-fit-state.json known-failures? Answer yes/no with the line. Do not change the file.
4. Screenshot evidence: accepted as is.
5. Not in this PR: the Aa font on stage cards (queued separately).
6. Watch the PR; report the Gate per check when it finishes.

DO NOT TOUCH (unchanged otherwise): every other game; schools/assets/**; scripts/measure-phone-fit.py and phone-fit-state.json; docs/handover/home.md and cloud.md.
STOP IF: the check finds any other game (report it; do not fix); the check flags a rule that is not this shape (report it, so the pattern can be tightened); the Log Laws screenshots differ.
