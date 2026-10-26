# Contract BELOW-FOLD-AUDIT (Jon, 26 Oct 2026), verbatim

TASK: Find out why the 45 games on the phone-fit known-failures list fail, and measure classroom laptop and projector sizes across the whole roster: report only, no fixes.

ROOT CAUSE: Unknown, to be established. Facts: 45 live games fail canon §7.6.1 (the last answer option ends below the fold), 39 of them in normal mode alone, and 14 games can't be measured by the generic driver. Some games fail by the same amount at every size (differentiation-duel's options start at 809 px at all three phone sizes), which suggests a panel above the question (a how-to or quick reference) rather than the screen size. Separately, Distinctly Average's Next sits 251 px below the fold at 1280 × 720 without its card; canon has no rule for laptop or projector sizes, so nothing measures them.

CLASS CHECK: Expected yes, to be confirmed. If most failures share a cause (a common panel pattern, a shared stylesheet, a layout that pushes the options down), the fix is architectural and likely uses the .maffs-ref component built in #554. The report must group the games by cause, so the fix can be scoped once, not 45 times.

EXACT CHANGE:
1. For each of the 45 games, record: the sizes and modes where it fails; how far over; what sits above the options (each element, with its height at 320 × 568); and the lowest tier it serves, from .claude/rules/game-roster.md.
2. Group the games by cause: an identical layout pattern, or shared code or CSS. Name each group, with the games in it, their total count, and one example.
3. For each group, state whether the .maffs-ref pattern (collapsed while asking, open in the feedback) would fix it. If not, state what would.
4. For the 14 unmeasurable games, record why the driver can't measure them, and what a game-specific measurement would need.
5. Run measure-phone-fit.py (or an extension of it, in report mode only) at 1280 × 720, 1280 × 800 and 1366 × 768, in normal mode, across every measurable live game. Record where the last option and Next end against the fold.
6. Write it all to docs/audits/below-fold-2026-10-26.md, ordered by priority: lowest tier served first (grade 1–3 and resit games at the top), then by the number of common sizes failed. Commit the report, merge once CI is green, and write the handover. Then stop: Jon will send the fix contract.

DO NOT TOUCH: Any game file, theme.css or the .maffs-ref component. The known-failures lists and the gate's rules. Canon. Any question wording.

SUCCESS CONDITION: The report covers all 45 games and all 14 unmeasurable ones, grouped by cause, with a stated fix for each group. Laptop and projector measurements cover every measurable live game. Games are ordered with the priority audience first. The report is merged and main is green.

STOP IF: More than a quarter of the 45 have no identifiable cause (report what you have). Measuring at laptop sizes needs a change to the gate's rules, not just a report mode. Any game measures differently on main from the known-failures list (report the difference).
