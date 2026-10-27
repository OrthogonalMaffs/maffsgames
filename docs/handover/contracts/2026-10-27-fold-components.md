# Contract FOLD-COMPONENTS (Jon, 26-27 Oct 2026), verbatim, with the lane exception

TASK: Fix the below-fold failures in the reference-panel, four-full-width-options and figure groups through shared layout components in theme.css, starting with the resit-suite games, and bring the phone-fit gate up to Jon's 26 Oct rulings: a laptop and projector rule, two options to a row, horizontal overflow, canvas games, and the canon wording.

ROOT CAUSE: docs/audits/below-fold-2026-10-26.md (as corrected by #560) groups the 46 normal-mode known failures by cause. Three groups share causes a shared component can fix: a reference panel open above the question, four full-width options stacked, and a figure above the options at full size. Separately: (a) 21 games put the last option or Next below the fold at classroom laptop and projector sizes, with no rule to catch it; (b) the gate doesn't detect horizontal page scroll, so ShapeShifter scrolls sideways at 320 px and still passes; (c) four canvas games (bearing-blitz, four-quadrant-explorer, gradient-hunter, shape-shifter) are unmeasurable, though the canvas element's own box can be measured; (d) canon §7.6.1 says a game is "never added" to the lists, and its counts are out of date; (e) raw run JSON nearly went live, so other internal folders under docs/ may be publicly served.

CLASS CHECK: Yes, throughout. Each group's cause is a layout pattern repeated across games, so each fix is one shared component in theme.css, applied to every game in the group, never a per-game patch. The gate changes are in the shared driver and apply to every game. The publishing check covers every internal folder, not only the one already excluded.

EXACT CHANGE:
Rulings (Jon, 26 Oct 2026):
- R1: The 1 Oct exception stays literal: it covers only a question itself taller than the screen (better-value, truth-will-set-you-free, wrong-on-the-internet). The other 8 games in that table are layout failures and stay on the list for a later contract.
- R2: Laptop and projector rule: at 1366 × 768 and 1280 × 720, the last option and Next end above the fold.
- R3: Two options to a row, only when every option fits on one line without wrapping at that width, with tap targets at least 44 px; otherwise one to a row.
- R4: No start-screen rule yet. The start screen stays report-only.

1. Report, for every game in the three groups: whether it uses theme.css, and its lowest tier served (from the roster). Work order: resit-suite games first, then by lowest tier.
2. theme.css: shared components, each documented in canon §7.5 or §7.6:
   - two-to-a-row options under R3, decided by measuring the rendered options, not by character count;
   - a compact game header on phones (less height, same content);
   - figure scaling on phones: a figure shrinks to fit (keeping its labels legible, as checked by the diagram check where it applies) so the options stay above the fold.
   Reference panels use the existing .maffs-ref component (collapsed while asking, open in the feedback where it fits).
3. Apply them group by group, ONE PR per group: reference-panel group, then four-full-width-options, then figure group. A game not on theme.css adopts only the shared components it needs (stylesheet link plus classes), not a full restyle. After each PR, re-measure that group's games at every size and mode, take fixed games off the known-failures list, and record before and after.
4. measure-phone-fit.py:
   - Laptop rule (R2): judged at 1366 × 768 and 1280 × 720, with its own known-failures list that can only shrink, seeded from the laptop run in docs/audits/phone-fit-runs-2026-10-26/.
   - Horizontal overflow: fail any game whose page scrolls sideways at any measured size, with its own known-failures list.
   - Canvas games: measure the canvas element's box. If the canvas, or the answer controls next to it, end below the fold, it fails. Take games off the unmeasurable list when this measures them, with no per-game code.
   - Selftest plants for all three.
5. canon §7.6.1: record R1–R4 with the date; replace "never added" with "a list may grow only when the measurement itself improves, with Jon's ruling, never because of a new fault"; update the counts.
6. Publishing: list every folder and file type under docs/ and scripts/ that GitHub Pages currently serves on maffsgames.co.uk. Exclude internal material (handovers, contracts, audits, run data) in _config.yml. Confirm with a live fetch after merge that each excluded path returns 404.
7. Merge each PR once CI is green, updating the handover after each one. When all three groups and items 4–6 are merged, stop: Jon will send the next contract.

DO NOT TOUCH: Any question, explanation or help wording. The 8 answer-control games and the 6 tall-input games (later contract). The start-screen rule (R4). Each game's theme row, colours and fonts. gen-six-ps.py and the 6 P's banks (home lane). The Aa-at-320 exception.

SUCCESS CONDITION: Every game in the three groups passes at every size and mode, or remains on the list with the measured reason. The known-failures list is shorter by at least the number fixed. The laptop, horizontal-overflow and canvas checks run in the gate, with lists and selftest plants. Canon carries R1–R4 and the corrected wording. Internal folders return 404 on the live site. Main is green after every merge.

STOP IF: A shared component would change how a passing game looks or behaves, beyond freeing space. Adopting theme.css in a game would change its theme row or look. Any fix needs a wording change. Excluding a folder would remove a page linked from the live site. The canvas measurement needs per-game code. More than 3 games in a group can't be fixed by its shared component (report them; Jon decides).

## Lane exception (Jon, 27 Oct 2026), verbatim

Asked which lane runs it, Jon chose "This session, lane exception": the cloud lane runs it, under a lane exception for this contract only, covering theme.css, canon §7.5/§7.6.1, _config.yml, the shared scripts, and per-game edits to listed games in the three groups; each game claimed on the cloud-remaining list first; recorded in the handover.

Jon's message:

> Lane exception granted for this contract only, as you described: theme.css, canon §7.5/§7.6.1, _config.yml, the shared scripts, and per-game edits to listed games in the three groups. Claim each game before editing it, and record the exception in the handover. The home lane will run the pie-charts bank meanwhile, which edits gen-six-ps.py and adds the bank-first rule to canon outside §7.5 and §7.6. If you need canon outside those sections, stop and ask.

## Rulings (Jon, 27 Oct 2026), verbatim

> * The lane exception now also covers canon §7.6.2. In PR 5, correct where it says the reference card lives.
> * The three group-A remainders stay on the lists with their reasons: constructions-lab (its panel is the task), trig-worms on laptops (its canvas), and suvat at 320 and in Aa (its question box).

With them (same message): get #564 green and merged, then delete claude/jpib-split; find why the "Record CI timings and repack" job did not balance
Just Pythag It, Bruv, part 2 before it outgrew its limit, and fix it where the parts are allotted, reporting before changing the repack; then PR 3 to PR 6,
each merged on green with the handover updated; stop after PR 6 for Project Claude's live 404 check.
