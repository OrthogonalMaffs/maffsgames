FORGE-SUBJECT-PROMPT, one part.
LANE: cloud. Send now. TIER: Small. MODEL: Claude Code, Sonnet 5.5, low effort.

TASK: Formula Forge: make the subject letter in "Make … the subject" far more prominent, and add the start-screen line "Powers and Multi: have paper handy." (todo FORGE-SUBJECT-PROMPT, Jon 9 Nov 2026).

ROOT CAUSE: On main c46eb14 (re-checked):
- games/formula-forge/index.html:478-480 render the prompt as three spans; the subject is KaTeX at 1.1em (:65) in the same colour and weight as the rest of the line (:64, var(--accent), .95rem). A student scanning the card sees the formula, not which letter to isolate.
- :475 sets tEl.innerHTML to a <strong> version that :477 immediately clears: dead code.
- The start screen (:141-148) does not warn that stages 3 (pill "Powers") and 4 (pill "Multi") need working on paper.

CLASS CHECK: Local. One game's prompt markup and one start-screen line; no shared asset renders this prompt.

EXACT CHANGE:
1. First commit: close out 52DLE-TIDY (#852, merge de5c830: main's runs on its merge commit from the API into its cloud.md entry; contract to docs/history/contracts/). Save this contract verbatim as docs/handover/contracts/2026-11-20-forge-subject-prompt.md.
2. games/formula-forge/index.html, the prompt: delete :475-476 (the dead innerHTML line and its comment). The subject span (:479) gets class "subject-chip". New CSS beside :64-65: .q-card .target .subject-chip{display:inline-block;color:var(--primary);background:rgba(249,115,22,.14);border:1.5px solid var(--primary);border-radius:8px;padding:0 .35em;margin:0 .15em;line-height:1.25;vertical-align:middle} and .q-card .target .subject-chip .katex{font-size:1.6em!important}. "Make" and "the subject" stay as they are.
3. Start screen: a new <div class="menu-info"> directly after the stage-preview block (:146), reading exactly: Powers and Multi: have paper handy.
4. scripts/verify-formula-forge.py: on a served page at each level, the first question's #target holds exactly one .subject-chip whose KaTeX text is that question's subject; the start screen shows the exact line from step 3. Plants that must FAIL: the class removed from the subject span; the start line removed.
5. Check by eye at 320x568 and 390x844, normal and Aa: a stage 1 and a stage 4 question (the longest formulas), screenshots in the PR. The chip must not wrap away from "Make" on its own line at 320 unless the whole line wraps.
6. cloud.md entry. No /updates/ line.
7. PR, Gate and phone-fit-full green, merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600; report its last line. No draft PR.

DO NOT TOUCH: the bank (Q.gcse, Q.level4), options, hints, scoring, timer, stages, leaderboard; the theme and other colours; other games; schools/assets/; canon; docs/handover/home.md.

SUCCESS CONDITION: the subject letter is in an orange chip at 1.6em on every question at every level; the dead line is gone; the start line shows; the verifier's new checks pass and both plants fail; phone-fit-full green with no new entry; 52DLE-TIDY closed out; merged GREEN; cloud.md records it.

STOP IF: phone-fit-full reports a new overflow or Next below the fold on Formula Forge at any size or mode (report the numbers; do not shrink anything else to fit); the chip makes the target line wrap mid-phrase at 320 in Aa; merge-pr.py can't reach GitHub; anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies (report under "Decided for you").
END OF CONTRACT
