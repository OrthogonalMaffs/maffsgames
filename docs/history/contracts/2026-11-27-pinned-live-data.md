PINNED-LIVE-DATA (Project Claude, Fri 27 Nov 2026 18:05, reissued; checked against main b8ab511)
Jon, 26 Nov 2026, 13:26: "yes please" to the DAILY-DEAL follow-ups, which include this fix (found in DAILY-FIT's review); 27 Nov, 17:49: send it now, alongside his play of d by dx? Why?.
RECOMMENDED: Claude Code, Opus 5.5, effort high. Shared test infrastructure: 171 scripts start pages through this server.
LANE: cloud. SEND: now. First commit carries D-BY-DX-SIGN-LINE's close-out (AGENTS.md:62): #934 squash-merged as f6c0809 by merge-pr.py on a green Gate at 4730844 (check-site 46007737308, phone-fit-full 46007737275); merge-pr.py's last line "main f6c0809 run 46010247971: GREEN"; main's runs on f6c0809: check-site 46010247971, phone-fit-full 46010247561, pages 46010246665, each success. Move docs/handover/contracts/2026-11-27-d-by-dx-sign-line.md to docs/history/contracts/. Save this contract verbatim as docs/handover/contracts/2026-11-27-pinned-live-data.md in the same commit.
TIER: Shared (stop at green for Project Claude's review and Jon's "merge").

TASK: Make every check that renders a page through scripts/serve-stubbed.py see fixed data in place of the files bots rewrite on main, so no check's result changes with Jon's play, the nightly counts or any other bot commit.

ROOT CAUSE (shown, file:line on b8ab511):
- Three files a page reads are rewritten on main by bots with [skip ci]: games/maffscards/daily.json (.github/workflows/maffscards-daily.yml:73, on each of Jon's plays), schools/assets/answer-counts.json and schools/assets/ugh-stats.json (answer-counts.yml:71-72, nightly).
- All three are read by XMLHttpRequest, which the stub server does not touch: games/maffscards/index.html:939-940; schools/assets/answer-count.js:210 (loaded by every game with a count mount and the homepage); schools/assets/ugh-stats.js:95 and :358 (the /ugh-stats/ pages). serve-stubbed.py replaces only analytics.js (STUB, :35-42: mfg, fetch, sendBeacon). Correction to the 26 Nov draft of this contract: answer-counts.json is not read by fetch, so it does reach checks today.
- So a check that loads these pages through the server shows whatever the bot last wrote: Jon's daily result or not; a game's answer line or not, as its count crosses 1,000 (answer-count.js GAME_MIN :36) or the file's as_of goes past 7 days (STALE_MS :38). scripts/measure-phone-fit.py (start_stub_server at :937; its route at :479-498 passes these through) is one such check.
- Owner checks already pin their own data with Playwright routes, which answer before the server: verify-maffscards.py open_page (:391-417, DAILY-FIT); check-answer-count.py (_fixture and its route, :147-165). check-ugh-stats.py's REAL unit deliberately uses the repo's own answer-counts.json and ugh-stats.json through the server (its docstring :14; routes :286-300).

CLASS CHECK: A class: missing safety in shared infrastructure called from many paths (three bot-written files, many checks). The fix goes in scripts/serve-stubbed.py, the one server every rendering check uses, plus a CI guard so the next bot-written file cannot escape the same way. Not at each check.

EXACT CHANGE:
1. scripts/serve-stubbed.py: a table BOT_WRITTEN of every repo path any workflow stages with git add. Each entry is one of:
   - pinned: the server answers that path, with or without a query string, with a fixed body, whatever the file on disk says. Each pinned body is the file's "shows nothing" state, valid for its reader:
     games/maffscards/daily.json: {"date": null, "result": null, "rounds": null, "line": null} (not played).
     schools/assets/answer-counts.json: {"as_of": <the time of serving>, "since": "2026-09-01", "total": 0, "games": {}} (never stale; no line on any page).
     schools/assets/ugh-stats.json: the smallest body ugh-stats.js accepts as valid that shows no figure, as_of set to the time of serving; if no valid body shows nothing, STOP IF below.
     For each pinned file, name in the report the owner check that covers its shown states (verify-maffscards.py for daily.json; check-answer-count.py for answer-counts.json; check-ugh-stats.py for both stats files). If any has none, STOP IF below.
   - not pinned, with the reason in a few words checked against the code, not assumed (e.g. "never read by a page"). Today's other staged paths: check-site.yml:194 (docs/audits/REGISTER.md), :217 (the two handovers and two archives), :313 (four scripts/ci-*.json).
2. An opt-out for checks that need the committed files through the server: a server argument and an environment variable (your choice of names, both in the docstring). check-ugh-stats.py's REAL unit uses it; nothing else does unless a check fails for this reason (STOP IF). bank_common.start_stub_server passes it through; its port and retry logic are unchanged.
3. A guard, run in CI (a --selftest of serve-stubbed.py, or a step in an existing static check: your choice, named in the report): every path any .github/workflows/*.yml stages with git add is in BOT_WRITTEN, and every BOT_WRITTEN path is still staged by some workflow. Plants, each must FAIL: a workflow line adding an unlisted path; daily.json removed from the table; a pin answering with the file on disk; answer-counts.json's pin with an as_of 8 days old.
4. serve-stubbed.py's docstring: what it pins and why (Jon's play and bot commits must never change a check's colour), and the opt-out. docs/handover/cloud.md entry.

DO NOT TOUCH:
- schools/assets/ (analytics.js, answer-count.js, ugh-stats.js and the rest), every game and /ugh-stats/ page, the three bot-written files, every workflow (read them; do not edit), scripts/merge-pr.py.
- The fetch stub's behaviour; start_stub_server's port and retry logic.
- verify-maffscards.py, check-answer-count.py and check-ugh-stats.py's units and plants, beyond the opt-out in step 2.
- canon, the roster, docs/todo.md.
- No force-push.

SUCCESS CONDITION:
- Through the stub server, daily.json (and daily.json?t=...) is the not-played body, and answer-counts.json and ugh-stats.json are their pinned bodies, even when the files on disk hold other data; proved by a test that serves from a temporary root or a temporary copy, never by editing a committed file.
- Every workflow-staged path is classified, each "not pinned" reason checked against the code; the guard and its four plants run in CI.
- check-ugh-stats.py's REAL unit still reads the committed files, through the opt-out.
- Every existing check passes; phone-fit-full green on the PR. Any check whose result changed because of the pin is listed in the report with its before and after.
- At green: stop and report to Project Claude for review; merge only on Jon's "merge", through python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600; if main moves while waiting, merge main into the branch and let the Gate re-run; cloud.md records it.

STOP IF:
- Any bot-written file is read by a page by a means other than fetch or XMLHttpRequest (for example a script tag or an import): report it before pinning.
- A pinned file has no owner check covering its shown states, or ugh-stats.json has no valid "shows nothing" body: report it; do not pin that file.
- An existing check fails because of the pin (other than check-ugh-stats.py's REAL unit, which takes the opt-out): report the check and why it needs the committed file; do not opt it out on your own.
- main is red when you come to merge: report it; do not use --override.
- merge-pr.py cannot reach GitHub or refuses: report its output; do not merge another way.
