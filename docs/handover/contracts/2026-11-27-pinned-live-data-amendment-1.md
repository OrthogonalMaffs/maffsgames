PINNED-LIVE-DATA, AMENDMENT 1 (Project Claude, Fri 27 Nov 2026 18:35; replaces the contract of 18:05 in full; checked against main b8ab511)
Jon, 27 Nov 2026, 18:24: passed on the lane's stop report (the ci-deps finding; ugh-stats.json has no valid "shows nothing" body). This amendment rules on both. Continue on the same branch (claude/admiring-faraday-c7alrl); its first commit (D-BY-DX-SIGN-LINE's close-out and the contract) stands. Save this amendment verbatim beside the contract as docs/handover/contracts/2026-11-27-pinned-live-data-amendment-1.md.
RECOMMENDED: Claude Code, Opus 5.5, effort high. Shared test infrastructure and a Gate file.
LANE: cloud (the same session). SEND: now.
TIER: Shared (stop at green for Project Claude's review and Jon's "merge").

TASK: Make every check that renders a page through scripts/serve-stubbed.py see fixed data in place of the files bots rewrite on main, so no check's result changes with Jon's play, the nightly counts or any other bot commit; and keep ci-deps.py from mistaking the server's table of those files for things a verifier reads.

ROOT CAUSE (shown, file:line on b8ab511 unless said):
- Three files a page reads are rewritten on main by bots with [skip ci]: games/maffscards/daily.json (.github/workflows/maffscards-daily.yml:73, on each of Jon's plays), schools/assets/answer-counts.json and schools/assets/ugh-stats.json (answer-counts.yml:71-72, nightly).
- All three are read by XMLHttpRequest, which the stub server does not touch: games/maffscards/index.html:939-940; schools/assets/answer-count.js:210; schools/assets/ugh-stats.js:95 and :358. serve-stubbed.py replaces only analytics.js (STUB, :35-42).
- So a check that loads these pages through the server shows whatever the bot last wrote. scripts/measure-phone-fit.py (start_stub_server at :937; its route at :479-498 passes these through) is one such check.
- Owner checks already pin their own data with Playwright routes: verify-maffscards.py open_page (:391-417); check-answer-count.py (:147-165). check-ugh-stats.py's REAL unit deliberately reads the repo's own files through the server.
- New (the lane's stop report, shown on its branch): ci-deps.py follows a verifier's local modules and counts their string literals as the verifier's dependencies (script_deps, scripts/ci-deps.py:162-190, LIB origin; site-wide checks are already followed as files only, :18-24 and :185). measure-phone-fit.py loads bank_common.py, which names serve-stubbed.py, so the literals of the new BOT_WRITTEN table make ten files "shared" for phone-fit, both handovers among them: nearly every PR would run the full phone-fit (about 17 minutes against 1.5). Those paths are not inputs to any verdict: the server pins them or never serves them to a page.
- New: no valid ugh-stats.json shows nothing. ugh-stats.js accepts only a body with at least one day and 24 hours each side; the smallest valid body (one day, every count 0) still draws /ugh-stats/charts/ with axes and an "Updated" date (the lane, in Chromium).

CLASS CHECK: Two classes, both in shared infrastructure. (1) Missing safety in the one server every rendering check uses: fixed at serve-stubbed.py, with a CI guard, not at each check. (2) ci-deps.py reads a shared module's literals as inputs of every verifier that loads it, when that module's literals describe what it handles, not what the verifier tests; the same shape as CI's own modules and site-wide checks, which ci-deps already follows as files only. Fixed in ci-deps.py by a declaration any such module can make, not by a name written into ci-deps, and not by spelling the paths in serve-stubbed.py so ci-deps cannot see them (that hides the problem; the lane was right not to).

EXACT CHANGE:
1. scripts/serve-stubbed.py: a table BOT_WRITTEN of every repo path any workflow stages with git add. Each entry is pinned (the server answers that path, with or without a query string, with a fixed body, whatever the file on disk says) or not pinned, with the reason in a few words checked against the code. The pins, each a fixed state that is the same on every run:
   - games/maffscards/daily.json: {"date": null, "result": null, "rounds": null, "line": null} (not played). Owner check: verify-maffscards.py.
   - schools/assets/answer-counts.json: {"as_of": <the time of serving>, "since": "2026-09-01", "total": 0, "games": {}}. No count line on games or the homepage; /ugh-stats/ shows its zero line, accepted. Owner checks: check-answer-count.py, check-ugh-stats.py.
   - schools/assets/ugh-stats.json (ruling, Project Claude, 27 Nov): pinned to the smallest valid body the lane tested (one day, every count 0, 24 hours each side, valid countries and levels as ugh-stats.js requires), with as_of the time of serving. An all-zero chart is accepted: the aim is a state that never changes, not an empty page. Owner check: check-ugh-stats.py.
   - Not pinned, as on the branch: REGISTER.md, both handovers and both archives, the four scripts/ci-*.json ("never read by a page").
2. The opt-out, as on the branch: --committed or MAFFS_STUB_COMMITTED=1, via bank_common.start_stub_server(committed=True); check-ugh-stats.py uses it (its QUIZ unit sharing that server is accepted).
3. The guard, as on the branch: serve-stubbed.py --selftest through its # ci-line header, serving from a temporary folder of fake bot data. Plants, each must FAIL: a workflow line adding an unlisted path; daily.json removed from the table; a pin answering with the file on disk; answer-counts.json's pin with an as_of 8 days old; ugh-stats.json's pin answering with the file on disk.
4. scripts/ci-deps.py: a local module may declare, in a header line of its own, "# ci-deps-literals: none". script_deps then gives that module's file (and the files of the modules it loads, as for a site-wide check) but never its literals, whatever the caller. serve-stubbed.py carries the line, with a one-line reason. The docstring's dependency list (:16-35) gains a sentence for it. The token is not a "# ci-deps:" header and must never be read as one.
   --selftest: is_shared on each of the ten paths (both handovers, both archives, REGISTER.md, daily.json, ugh-stats.json, and the three others the branch made shared) is what it is on main; serve-stubbed.py itself stays a dependency of phone-fit. Plants, each must FAIL: the declaration ignored; the declaration honoured on a module that does not carry it. The four history tests that fail in a shallow checkout are not yours: run them where history is full (CI) and report.
   Report the dependency sets of every verifier that loads serve-stubbed.py (directly or through bank_common.py), before and after, as counts plus any path that left or joined.
5. serve-stubbed.py's docstring: what it pins and why (Jon's play and bot commits must never change a check's colour), the opt-out, and the ci-deps declaration. docs/handover/cloud.md entry. cloud.md past 20 KiB only warns (AGENTS.md:71: an archivable handover; main archives it after merge), so it does not block; keep the entry short.

DO NOT TOUCH:
- schools/assets/ (analytics.js, answer-count.js, ugh-stats.js and the rest), every game and /ugh-stats/ page, the three bot-written files, every workflow (read them; do not edit), scripts/merge-pr.py (the home lane's MERGE-GUARD is changing it).
- scripts/ci-deps.py beyond step 4; every other scripts/ci-*.py.
- The fetch stub's behaviour; start_stub_server's port and retry logic.
- verify-maffscards.py, check-answer-count.py and check-ugh-stats.py's units and plants, beyond the opt-out.
- canon, the roster, docs/todo.md.
- No force-push.

SUCCESS CONDITION:
- Through the stub server, daily.json (and ?t=...), answer-counts.json and ugh-stats.json are their pinned bodies even when the files on disk hold other data; proved from a temporary root, never by editing a committed file.
- Every workflow-staged path classified; the guard and its five plants run in CI.
- ci-deps.py: none of the ten paths is shared because of serve-stubbed.py; its new selftest cases and two plants run in CI; the dependency-set report as in step 4.
- check-ugh-stats.py's REAL unit still reads the committed files through the opt-out.
- Every existing check passes in CI; phone-fit-full green on the PR. Any check whose result changed because of the pins is listed with before and after.
- At green: stop and report to Project Claude for review; merge only on Jon's "merge", through python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600; if main moves while waiting (MERGE-GUARD may land first, and will then refuse a stale Gate), merge main into the branch and let the checks re-run; cloud.md records it.

STOP IF:
- Any bot-written file is read by a page by a means other than fetch or XMLHttpRequest: report it before pinning.
- The ci-deps declaration changes the dependency set of any verifier other than through serve-stubbed.py's own literals: report it.
- An existing check fails in CI because of a pin (other than check-ugh-stats.py's units, which take the opt-out): report the check and why it needs the committed file; do not opt it out on your own.
- main is red when you come to merge: report it; do not use --override.
- merge-pr.py cannot reach GitHub or refuses: report its output; do not merge another way.
