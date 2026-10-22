# K-PUNCTUATION-SCAN (Jon, 22 Oct 2026), verbatim

TASK: Report-only scan: do any of the 36 games that render KaTeX through their own K() (not MaffsText) start a line with punctuation after inline maths, as MaffsText did before #471?
ROOT CAUSE: MATHTEXT-NOWRAP (#471) fixed the fault in the shared renderer for its 16 games. The home lane noted 36 games build their own maths HTML with K() and were not measured. The same fault may be live in some of them.
CLASS CHECK: The shape (maths and its following punctuation as separate inline content) is the same class #471 fixed. The root fix for affected games is moving them onto MaffsText, not per-game patches. This task only measures, so that fix can be scoped from data.
EXACT CHANGE: None to any game or shared file. Reuse scripts/test-mathtext.py's line-box method on each of the 36 games: walk every question and screen with inline maths followed by punctuation at 320, 375 and 390 px, recording any line that begins with closing punctuation or ends with an orphaned opening bracket. Write docs/audits/k-punctuation-scan-2026-10.md: per game, items scanned, items affected with widths and one example each, and whether its K() could be swapped for MaffsText.html directly. Commit the scan script under scripts/ (not in CI).
DO NOT TOUCH: Every game, mathtext.js, theme.css, the workflow, findings files.
SUCCESS CONDITION: All 36 games scanned or listed with why not; every count from the committed script; the report merged through merge-pr.py on a green Gate.
STOP IF: A game's maths cannot be walked without changing it (list it and carry on); more than 10 games are affected (finish the report, then stop and report: it becomes a migration contract for Jon).
FINISH: Merged; docs/handover/cloud.md records the report's location and headline counts.
