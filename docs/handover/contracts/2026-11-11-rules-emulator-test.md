RULES-EMULATOR-TEST (Project Claude, 11 Nov 2026; unnamed in the paste, named by the home lane). Recommended: Opus, effort medium — small change, but its test result decides whether Jon deploys.

TASK: Prove the 10 Nov recent_scores rule change with the repo's own emulator test before Jon deploys it, and replace the deploy doc's Playground test, which cannot tell a working rule from a broken one.

ROOT CAUSE: #728 changed firebase/database.rules.json (game and level refuse < and >) but added no case to firebase/rules.test.mjs, the emulator suite that already holds REFUSE/ALLOW cases for these fields (e.g. "REFUSE ticker game name of 200 characters"). Its only test is manual: docs/firebase-rules-deploy.md "10 Nov 2026 change" has Jon simulate a set at /recent_scores/test1 with "timestamp": <now in ms>. The rules require timestamp within now ± 60000 ms (database.rules.json:31), so: test 2 ("Factor Race" → allowed) fails unless Jon types the current millisecond count within a minute, and test 1 ("<b>x</b>" → denied) is denied by the timestamp rule whether or not the new < > rule works. Also unproven: that RTDB's matches() finds an unanchored /[<>]/ inside a longer string; the file's other uses are all anchored (^...$).

CLASS CHECK: Yes, a class: a rules change verified by hand in a simulator, outside the suite that exists for exactly this. The fix is at that layer: rules.test.mjs gains the cases, and the deploy doc's tests for every change point to the suite rather than a hand-built Playground payload. Not a fix to one timestamp value in the doc.

EXACT CHANGE:
1. firebase/rules.test.mjs: add, using goodRecent() (which already builds a valid timestamp):
   - REFUSE ticker game containing "<b>x</b>"
   - REFUSE ticker game "a<b" (single < mid-string: proves unanchored matching)
   - REFUSE ticker level containing ">"
   - ALLOW ticker game "Factor Race" and level "GCSE" (control)
2. Run it: npx firebase emulators:exec --only database --project demo-maffsgames "node rules.test.mjs" (the command in the file's header). Every case must pass. Report the output in the PR body.
3. docs/firebase-rules-deploy.md, "10 Nov 2026 change": replace the "Test straight after publishing" Playground block with: the emulator command and its result from this PR, then the existing real-game ticker check. Add one line to the file's general deploy section: every rules change adds its cases to rules.test.mjs and runs it before Jon deploys; the Playground is optional, never the proof.
4. AGENTS.md: one short entry (300-byte rule) carrying the same line. Close-out per the standing rule.

DO NOT TOUCH: firebase/database.rules.json (unless the test shows the rule does not work: then STOP); the live database or console (no deploy, no live write); leaderboards/index.html and every other page.

SUCCESS CONDITION: rules.test.mjs holds the four new cases and the whole suite passes against main's rules file, output quoted in the PR body; the deploy doc's 10 Nov section no longer asks Jon to type a timestamp; the general rule is in the deploy doc and AGENTS.md; Gate green; merged on green; committed, handover documented; Jon told the deploy is ready.

STOP IF: any new REFUSE case is allowed (the rule does not work as written: report, do not rewrite the rule); any existing case fails; the emulator cannot run on this machine (report why: Java, firebase-tools); another open PR edits docs/firebase-rules-deploy.md or firebase/.
