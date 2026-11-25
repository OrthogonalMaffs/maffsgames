LIKE-TERMS-PLUS (Project Claude, Wed 25 Nov 2026 17:05; checked against main c788f40)
Jon, 25 Nov 2026, 16:49, playing Stage 2 ("6a + 3a + 2b + 5b", answer boxes shown as "9 a 7 b"): "shouldn't this have a + in the middle?" Ruled 16:55: yes, in Stage 1 (fruit) and Stage 2 (letters).
RECOMMENDED: Claude Code, Opus 5.5, effort medium. One game page and one check; the answer notation must be right.
LANE: cloud, lane 2. SEND: now (#912 merged; lane 2 is free). Its first commit closes out BANKS-40 per AGENTS.md:62. If another lane is running, the only shared file is docs/handover/cloud.md: merge main in before merging and keep every entry.
TIER: Small (merge on green).

TASK: Show the typed answer in Like Terms Collector's Stages 1 and 2 as a sum, "[ ] a + [ ] b", and give the wrong-answer feedback the same notation.

ROOT CAUSE: Shown: loadInputQuestion (games/like-terms-collector/index.html:399-419) builds one input-group per term (input then label, :407-413) and puts nothing between the groups, so the row reads "9 a 7 b"; in algebra, terms written side by side mean a product (9a x 7b). The feedback (:466) says "The answer is 9 a and 7 b.", which is not the notation the stage teaches.

CLASS CHECK: Local. The only other page with an input-label class, test-the-claim, labels hypothesis steps, not the terms of an expression (test-the-claim/index.html:1542-1612). No shared asset builds this row.

EXACT CHANGE (games/like-terms-collector/index.html, scripts/verify-like-terms-collector.py, updates/index.html):
0. First commit: BANKS-40's close-out (AGENTS.md:62), then save this contract verbatim as docs/handover/contracts/2026-11-25-like-terms-plus.md.
1. loadInputQuestion (:407-413): every term after the first starts its own input-group with a "+" span (class input-op, the same size, weight and colour as .input-label), so the "+" wraps with its term and never sits alone at a line end. Order inside the second group: "+", input, label. Applies to Stages 1 and 2 (both call this function, :394-395). Ids, aria-labels, focus and Enter handling unchanged.
2. Feedback (:466): the answer part reads "The answer is 9a + 7b." in Stage 2 (number and letter with no space) and "The answer is 8 apples + 6 tangerines." in Stage 1 (number, space, fruit word). The decimals sentence before it is unchanged.
3. Verifier: a new check, in Chromium, for every Stage 1 and Stage 2 item: the row's text reads "<box> <label1> + <box> <label2>" (exactly one "+", between the two groups, inside the second); a wrong answer's feedback ends with the notation in step 2 and the item's own answers. A plant (must FAIL): the "+" span removed. Update the ci-line. All existing checks and the parseInt plant still pass.
4. /updates/: one dated line, plain words: "Like Terms Collector: the answer boxes now read as a sum, 9a + 7b, not 9a 7b." docs/handover/cloud.md entry. Merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600 on green; report its last line.

DO NOT TOUCH:
- The questions, answers, marking (MaffsAnswer), scoring, stages, Stage 3, leaderboard, analytics, the Aa key (todo 50), the look beyond the "+" span.
- schools/assets/, every other game, scripts/measure-phone-fit.py and the Gate files, canon, the roster.

SUCCESS CONDITION:
- Stage 1 and Stage 2 rows read "[ ] label + [ ] label"; feedback reads "9a + 7b" (Stage 2) and "8 apples + 6 tangerines" (Stage 1); the verifier proves it for every item and catches the plant.
- Phone fit green (it runs on the PR by itself; do not dispatch it); merged through merge-pr.py, last line reported; cloud.md records it.

STOP IF:
- At 320x568 the row cannot hold the "+" with its term without changing anything beyond this page's .input-row/.input-group styles: report the measurement.
- Any existing check or plant fails and the cause is not in this change.
- merge-pr.py cannot reach GitHub, or refuses: report its output; do not merge another way.
