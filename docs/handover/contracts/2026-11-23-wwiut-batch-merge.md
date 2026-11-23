# WWIUT-BATCH-MERGE (contract, 23 Nov 2026, 09:11; saved verbatim)

```text
LANE: cloud. Send now (lane free: #889 merged, main 765ae37 green).
MODEL: Sonnet, effort medium: a takeover, a main merge, a Gate and docs; no new code.

TASK: Take over the home lane's finished branch claude/wwiut-batch-1-2 ("When will I use this?": 40 jobs in 16 topics), bring it up to main, and merge it on a green Gate; carry #889's close-out and correct #887's record.

ROOT CAUSE: The home lane finished WWIUT-BATCH-1-2 at 06:49 on 23 Nov (branch head bc1fa32, main 661f822 merged in) and stopped for Project Claude's review and Jon's "merge". Jon is at work with no home lane, so the branch is stranded. Main has since gained 765ae37 (#889) and ccbcc4b. Separately, docs/handover/cloud.md's SITE-CONTRAST entry records main's 616 px failure as "a real overflow, NOT a flake", wording copied from Project Claude's PRIMARY-FIT-SWEEP contract; #889's sweep showed otherwise.

CLASS CHECK: Not a bug class: a one-off lane handover of finished, reviewed work, plus a records correction. Local. Explicit exceptions to Lane ownership (AGENTS.md:75), granted by Jon for this task only: the cloud lane may merge a branch that changes shared files (schools/assets/site-nav.js: 12 HUBS lines, Jon's ruling 23 Nov; index.html; data/games.json) and may add ONE line to the home lane's WWIUT-BATCH-1-2 entry in docs/handover/home.md.

EXACT CHANGE:
1. Check out the existing branch claude/wwiut-batch-1-2 (head bc1fa32). Do not start a new branch and do not rebase.
2. First commit on it (standing close-out rule, docs/handover/cloud.md): (a) #889's close-out: move docs/handover/contracts/2026-11-23-primary-fit-sweep.md to docs/history/contracts/; in cloud.md's PRIMARY-FIT-SWEEP entry record: merged as 765ae37 (#889), route merge-pr.py, main's runs check-site 45139129589 success attempt 1, phone-fit-full 45139129106 success attempt 1, pages build 45139128202 success attempt 1; PR head 597d29c check-site 45137452185 and phone-fit-full 45137452271 success. (b) In cloud.md's SITE-CONTRAST entry, replace "a real overflow, NOT a flake" with: "measured before schools/assets/fold.js laid the options two to a row (the old check's timing, not the game): not reproduced locally, and CI's own image passed every Sums in Disguise item and wrong option in #889's sweep". (c) Save this contract verbatim as docs/handover/contracts/2026-11-23-wwiut-batch-merge.md.
3. Merge origin/main into the branch (AGENTS.md:58). A trial merge was clean; resolve any conflict by keeping both sides' lines. Then run scripts/build-uses.py and confirm it changes nothing; if it does, commit its output.
4. Find the branch's PR with `gh api` REST (repos/OrthogonalMaffs/maffsgames/pulls?head=OrthogonalMaffs:claude/wwiut-batch-1-2&state=open). If none exists, open one, not a draft, with the batch contract, the home lane's report (its docs/handover/home.md entry) and this contract in the body. Either way the PR body lists the close-outs this PR carries (#889) and the record correction.
5. Review authority: Project Claude reviewed the branch on 23 Nov 08:55 (check-uses.py --static: 40 headlines recomputed, 32 pages; --selftest 94 of 94; all 40 worked examples recomputed by hand; the 55p mileage rate checked on GOV.UK). Jon said "merge" by sending this contract (23 Nov, 09:11). So when the Gate is green, merge with `python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600` and report its last line.
6. Add one line to the end of the home lane's WWIUT-BATCH-1-2 entry in docs/handover/home.md: "- Taken over and merged by the cloud lane (contract WWIUT-BATCH-MERGE, 23 Nov): see docs/handover/cloud.md." Write the cloud lane's own entry in docs/handover/cloud.md (done, next, discoveries). The batch's contract file stays where it is: its move to docs/history/contracts/ and the record of this merge and main's runs ride on the cloud lane's next task (standing rule).
7. Report: the PR number, merge commit, merge-pr.py's last line, and main's run IDs and results.

DO NOT TOUCH: data/uses.json and every generated page under when-will-i-use-this/ (approved wording, verbatim; no rewording, no new or restored scenarios, no headline changes: a separate contract will change the card format); scripts/check-uses.py and scripts/build-uses.py; schools/assets/ beyond what the branch already changes; any game; AGENTS.md; any other part of docs/handover/home.md than the one line in step 6; the seven dropped scenarios and the dropped Probability topic (leave them out).

SUCCESS CONDITION: The batch is on main via merge-pr.py with main green on the merge commit (no re-run); #889 closed out and #887's record corrected in the first commit; this contract saved in docs/handover/contracts/; the home entry carries the one takeover line; the cloud handover is current; the PR body lists the close-out.

STOP IF: the branch head is not bc1fa32 or has commits Project Claude has not seen; merging main conflicts anywhere other than docs/handover/ or updates/index.html; build-uses.py changes any generated page after the main merge; the Gate goes red on anything but a known infrastructure failure (if a check fails and passes on its one allowed re-run, report it as "passed on re-run", with the failing check's output, not as a flake); main's run on the merge commit is red; gh api cannot reach the PR or merge-pr.py cannot reach GitHub.
```
