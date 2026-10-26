# LOOK-REDS-2, second contract of 26 Oct 2026 (Jon, via Project Claude), verbatim

TASK: Finish LOOK-REDS-2 (Distinctly Average) under Jon's 26 Oct rulings: tighten and apply the phone-fit rule, build a shared collapsible reference component, place the median card with it, then merge.

ROOT CAUSE: Branch claude/theme-distinctly-average (checkpoint 9d7e0c5, clean tree) stopped on two STOP IFs. (1) The hardened measure-phone-fit.py flags 20 other live games whose answer options start below the fold. (2) Putting the median card back above the question pushes all 136 Foundation median items over the fold at 320 × 568 in normal mode. Also, the rule as first worded ("options start above the fold") passes items whose LAST option is hidden, so a student can be choosing from three of four options without knowing it.

CLASS CHECK: Yes, on three counts. (1) The phone-fit rule applies to every game, so it lives in canon and in the shared script, with a list of known failures that can only shrink (the check-theme.py and answer-lock pattern). (2) Reference panels pushing the options down are likely the shared cause in the 20 games, so the median-card fix is built as a shared component in theme.css, not as Distinctly Average code. (3) The fix is layout only, never wording: the 6 P's banks read this game's text.

EXACT CHANGE:
1. Finish the corrected Aa roster run (re-run it if the result is lost), with every command run from the worktree, not with "cd X && (A) & (B)".
2. measure-phone-fit.py: also measure where the LAST option ends. Report both rule versions across every live game in the handover. Then apply the tighter rule:
   - Normal mode at all three canon sizes, and Aa at 375 × 667 and 390 × 844: the last option ends above the fold.
   - Aa at 320 × 568 only (the accepted exception): the options start above the fold. Overflow beyond that is a warning.
   Games already failing go on a known-failures list, which is reported and never failed. Any game not on the list fails, and the script exits 1. Keep --selftest, adding planted cases for the last-option rule.
3. theme.css (plus a shared script if one is needed): a reference-card component. It is collapsed as "Show the rule" on the asking screen, and open inside the feedback, between the working and Next. Document it in canon §7.5 or §7.6 as the house pattern for help and reference panels.
4. Distinctly Average: the "Finding the median" card uses the component.
5. Layout only (spacing, panel order, collapsing): close the 12 items whose last option ends below the fold, and the 9 items over at 375 × 667.
6. canon.md §7.6.1: add the rule as in item 2, the Aa-at-320 exception with Distinctly Average GCSE (114 items, worst 184 px) as its first logged instance, and the known-failures pattern. Date it 26 Oct 2026, "Jon's ruling".
7. Re-measure all 657 items at all three sizes, in both modes, and update the screenshots page.
8. Open the PR, merge once CI is green, write the handover (the counts under both rule versions, the known-failures list, before and after). Then stop. Do NOT start Prime Sprint: Jon will send the next contract.

DO NOT TOUCH: Any question, explanation, misconception or help wording. gen-six-ps.py and the 6 P's banks. The 20 other games (list them, don't fix them). score-history.js. todo §3.9 (home lane's file). The CI workflow: putting the gate into CI is a later contract. The score-bar fold and data-chip changes, which stand.

SUCCESS CONDITION: Distinctly Average passes the tighter rule at every size and mode, apart from the recorded Aa-320 exception. The median card is collapsed while asking and open in the feedback, above Next. measure-phone-fit.py exits 0 on main with the known-failures list, and 1 on any game added to it later. Canon carries the rule, the exception and the component. The PR is merged, main is green, and the handover is complete.

STOP IF: The tighter rule puts more than 10 games on the known-failures list beyond the 20 already found (report the numbers; Jon decides). Distinctly Average can't pass the tighter rule by layout alone. The open median card in the feedback fails the gate. The component can't be added without changing how another live game renders.

## Jon's rulings on the two STOPs (26 Oct 2026), verbatim

Rulings, 26 Oct:

1. Median card in feedback: collapsed on phones, open where it fits, decided by a CSS media query on viewport height (no script). The card stays collapsed while asking, as now. Close the 11 GCSE frequency-table items at normal 320 and the 7 Aa-375 Next overruns by layout only, no wording changes.
2. The tighter rule and the 44-game known-failures list stand. Record, for each game, the sizes and modes it fails. Add a second list for the 14 games the driver can’t measure, also reported and only able to shrink, so they never read as passing. Write canon §7.6.1 and §7.6.2 accordingly, including that the feedback screen keeps Next above the fold (where Aa at 320 is the recorded exception).
3. Don’t force-push. Push f2d4838 (plus the changes above) to a new branch, claude/theme-distinctly-average-2. Leave the old branch untouched, and note it in the handover.
Then open the PR, merge once CI is green (CI judges the 6 P’s bank check), write the handover, and stop. I’ll send the next contract.
