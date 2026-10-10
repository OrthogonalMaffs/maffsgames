# MaffsGames — CLAUDE.md

## Project Overview
Free curriculum-aligned maths games for UK schools. 96 games and nine escape rooms live (Regression Rumble withdrawn 30 Sep 2026 pending a data rebuild). Separate from MathsWins (mathswins.co.uk).

- **Repo:** https://github.com/OrthogonalMaffs/maffsgames
- **Live site:** maffsgames.co.uk (GitHub Pages)
- **maffsgames.com:** bought 24 Sep 2026, 301-redirects to maffsgames.co.uk at the Cloudflare edge
  and serves nothing of its own. See `docs/domain-maffsgames-com.md` — including why the .co.uk stays
  canonical, and the two IONOS prompts to ignore
- **Contact:** contact@maffsgames.co.uk
- **BMC:** buymeacoffee.com/maffsgames
- **Project brief:** `.claude/rules/project-claude.md` — the mission, the audience, the division of
  labour and the platform principles. Loaded at the start of every session; read it with the note
  under **Task Contract** at the end of this file.

## Before stopping for a decision: the Standing rulings (canon §0.3)

Check canon §0.3 first. If a standing ruling (SR-1 …) covers the question, apply it and list
"SR-n applied: …" in the PR description. Stop only for what no ruling covers, or for an item on
§0.3's "Still stops for Jon" list. A contract's own STOP IF still applies as written.

## Checkpoint discipline, not a context stop (Jon, 5 Oct 2026)

No contract stops at "context passes 60%": that line is removed from every STOP IF, in current and future
contracts. A session cannot measure its own context; Jon can, and clears when needed. Instead:
- **Commit and push at every milestone** (a verifier passing, a bank written, a UI change working, docs done).
- **Keep your lane's handover (`docs/handover/home.md` or `docs/handover/cloud.md`) on the branch current as you go**,
  so a clear at any moment loses nothing: what is done, what is next, and anything learned that the next session needs.

## Before pushing: `python scripts/check-changed.py`, not the full local suite (canon §7.8, 4 Oct 2026)

This replaces "full local suite before every push", including in contracts that still say it. It runs
the content verifiers `scripts/ci-deps.py` selects for the branch's changes, plus the fast site-wide
checks; then push and let CI run the rest. **Why:** the repo is public, so CI minutes are free, and the
full local run was a slower second copy of CI with known Windows-only false failures (todo §4 item 18).
**Safety net:** every PR runs every site-wide check; every merge to main, a weekly schedule and a manual
run execute EVERYTHING. Merge when the `Gate (every job passed)` check is green. `--full` still runs the
whole suite locally if ever wanted.
**Two queues (PREPUSH-SCOPE, 10 Oct 2026):** heavy checks (CI time >= 60 s, or a browser check that runs its
own work concurrently, e.g. the answer-lock parts) one at a time; light checks six at once beside them. Six
answer-lock parts side by side all failed (UNPLAYABLE), so never run heavy ones together. Measured (serial ->
two queues): docs-only 353 -> 167 s; one game 1565 -> 1375 s; shared asset (#232's files) 4198 -> 2907 s.
The last line printed is the PR line "checks deferred to CI: ..." (tiers 1-2, tier 4 banks, leaderboard
coverage). `--files a b` plans for given paths; `--workers 1` runs the light queue serially too.

## After merging: watch main's full run (Jon, 5 Oct 2026)

The session that merges a PR waits for the full `check-site` run that the merge starts on `main`, and
reports its result (green, red or cancelled, naming the job and the check). **A red or cancelled main run
is fixed before any new work starts.** **Why:** a PR runs only the verifiers its changes select, so a
group that has outgrown its timeout passes on every PR and fails only on main. Group B was cancelled at
its 12-minute limit on every main run from #68 to #71, and it was seen only when a PR touched every game.
Each verifier group now also fails at 75% of its timeout ("time budget: … split it", in
`.github/workflows/check-site.yml`), so a group is split before it is cut off; each job's summary lists
every verifier's duration.

## Handover: read `docs/handover/home.md` and `docs/handover/cloud.md` (fixed pointer; fix PRs do not edit this section)

Each lane keeps its own handover, and a session edits only its own (7 Oct 2026, canon §7.8.2):
- **`docs/handover/home.md`**: the home lane (shared code and assets, CI, canon, docs PRs).
- **`docs/handover/cloud.md`**: the cloud lane (per-game fixes in unlisted games).

Read both at the start of a session: yours for what to do next, the other for what is in flight.
`docs/handover/contracts/` is read only when starting the item it names, never at session start (canon §7.8.2). CLAUDE.md's
old "Handover" sections, the history up to 7 Oct 2026, are in `docs/history/claude-md-archive.md`; nobody adds to them.

## Two lanes: who edits what (Jon, 7 Oct 2026; canon §7.8.2)

Two sessions may run side by side. They stay out of each other's files:
- **Home lane:** shared code, shared assets, CI and canon (contract F's shared fixes, then contract C), and
  every docs PR (`docs/todo.md`, the roster's listed section, relisting fixed games, batched).
- **Cloud lane:** per-game fixes in games that are currently unlisted, one game per PR, each with its verifier,
  closing its entries in its own `docs/audits/findings/<slug>.yml`. It never edits `schools/assets/`, the
  shared modules in `scripts/`, the workflow, canon, the roster's listed section or `docs/todo.md`.
- **No PR edits `docs/audits/REGISTER.md`:** CI regenerates and commits it on main after every merge (canon §0.4).
  **A per-game fix PR does not edit `docs/todo.md`:** the register records the fix.
- **Neither lane merges while main's last full run is red.**
- **Before the first push of every PR: `python scripts/check-changed.py`** (one PR on 7 Oct 2026 cost three runs).
- **Relisting a fixed game** is a home-lane docs PR, batched.
- **The cloud lane may fix listed games it has claimed on the `cloud-remaining:` line in
  `docs/handover/cloud.md`** (Jon, 8 Oct 2026, contract CLAIM). It claims one game at a time, before starting
  it, in a handover commit of its own, and removes the game in the PR that fixes it. The home lane never claims
  or edits a game on that line: before building each batch it reads the line on main and drops any claimed
  game. **For a listed game the claim is a process lock only** (Jon's ruling, 8 Oct): `check-answer-lock.py`
  judges it exactly as if unclaimed (a migrated game must pass; a NOT_YET game is reported). The
  reported-not-failed exemption holds only for games in the roster's Unlisted section, so no time bound is needed.

## Reference Files
- Full game roster (96 games, plus 1 withdrawn): see `.claude/rules/game-roster.md`
- Help/instructions audit: see `.claude/rules/help-audit.md`
- Timer policy (countdown/hidden/none): see `.claude/rules/timer-policy.md`
- Analytics events & dual logging: see `.claude/rules/analytics.md`
- Running to-do list: docs/todo.md

### Improvement ideas — two lists, deliberately separate
- `docs/idea-backlog-2026-08.md` — **Gemini's suggestions**, logged unagreed, each with a
  cross-ref against the roster and the Dashboard. Nothing in it is scheduled.
- `docs/jon-playtest-2026-08.md` — **Jon's own play-testing.** First-hand and much stronger
  evidence than the above. He samples games through the day; new findings go here, not in the
  Gemini file. Where they touch the same game, the entry says which supersedes which.

## Local render testing — ALWAYS use the stub server
```
python scripts/serve-stubbed.py        # http://127.0.0.1:8765/
```
Every page loads `schools/assets/analytics.js`, which posts to the live Apps Script endpoint and
into the production Events sheet. **Never open a real page against the live endpoint to check a
layout** — it writes junk rows into the data Jon makes decisions from (happened once, 2026-08-26).
The script swaps analytics.js for a no-op and leaves every other byte untouched. Node is not
installed on the Windows machine; Python is the way to serve this repo there.

Three things that cost time on 21/09, local or live:

- **Always cache-bust** — `?cb=<random>` on every page load and live fetch. Chrome will happily
  replay the previous build and hand you a clean pass that means nothing. It can fake a green as
  easily as a red, locally and on Pages.
- **The automation tab reports `document.hidden`**, so timers throttle to ~1.5/sec and any
  poll-based test driver stalls. To play a game end to end, capture the game's own `setTimeout`
  callbacks and drain them synchronously — every callback still runs, in order, without the waits.
  Test-only; never commit it.
- **`serve-stubbed.py` stubs `window.fetch` site-wide**, so an in-page `fetch` fails with
  `Error: stubbed`. Use `XMLHttpRequest` when a test needs to read a file.

## Tech Stack
- Single-file HTML games — no build step, no framework
- KaTeX via CDN for math rendering
- GitHub Pages hosting
- Firebase Realtime Database for leaderboard
- GA4 + Google Sheets dual analytics via `mfg()` wrapper

## Session practice (Jon, 8 Oct 2026, contract CTX)

- **Preview from a scratch copy:** never swap the repo's game file to preview; serve a scratch copy (`--against`).
- **Never run a verifier through `| tail` under a timeout** (the output is lost): run a long one in the background
  to a log file.
- **Verifiers read a mark from the page's feedback, never from a wrapped `mfg`** (canon §7.9).

## Escape rooms: no art field, no request (Jon, 10 Oct 2026, contract ART-PENDING)

A room built before its pictures has no top-level `art:` in its `room.js`, so the engine requests no scene, fail
or win picture (no 404 for check-site's tier 1). Add `art` with the pictures, never before. Never relax the 404
rule or allowlist a missing picture. Detail: `docs/escape-room-voice-rewrite.md` §6.

## Contracts arrive whole (Jon, 8 Oct 2026, contract CTX)

Jon never amends contracts: PC sends complete pastes.

## Where things live (read on demand, not every session)

- **Canon** `docs/canon.md`: the rules. §0.3 standing rulings, §0.4 findings register, §7 technical reference
  (§7.6 Next and MaffsLock, §7.8 CI and the two lanes), §11 escape rooms, **§12 engineering reference** (moved
  from this file: `check-site.py` tiers 1-4, no rejection sampling, `MaffsOptions.build()`, generator ranges,
  scaffolds, accessibility, tiered banks, level colours, the Firebase leaderboard).
- **Handovers** `docs/handover/home.md`, `docs/handover/cloud.md`: current state and the last three entries.
- **Register** `docs/audits/findings/<slug>.yml` (one per game); `docs/audits/REGISTER.md` is generated.
- **Roster** `.claude/rules/game-roster.md`. **To-do** `docs/todo.md`.
- **Archives** (history only, never loaded by default): `docs/history/claude-md-archive.md` (this file's dated
  handovers and state sections to 7 Oct 2026, and the reference sections canon already holds),
  `docs/history/handover-home-archive.md`, `docs/history/handover-cloud-archive.md`.
- **Size limit:** `scripts/check-context-size.py` fails CI if this file or either handover passes 20 KB.

## Task Contract

**Whose brief is which.** `.claude/rules/project-claude.md` loads alongside this file at the start of
every session. It is written to Project Claude, the planning role in Claude chat, so its **Your Role**
section — plan and advise, do not build unless asked — describes Project Claude, not you. In a Claude
Code session you are **Code Claude**, the implementation row of its Division of Labour table, and the
contract below is how work reaches you. Its mission, audience, platform principles and design rules
bind you exactly as they bind Project Claude.

All tasks arriving from Jon (relayed from Claude chat) will be structured as follows.
Do not begin work unless all seven fields are present:

TASK: [one sentence description]
ROOT CAUSE: [what is actually wrong]
CLASS CHECK: [is this finding an instance of a bug class (tests below)? If yes, EXACT CHANGE addresses the architectural layer. If no, state why the bug is local]
EXACT CHANGE: [file, function, what changes to what]
DO NOT TOUCH: [explicit exclusions]
SUCCESS CONDITION: [how to know the task is complete]
STOP IF: [conditions that require you to halt and report back to Jon]

**CLASS CHECK is answered before EXACT CHANGE, because its answer decides what EXACT CHANGE is.** A
finding is an instance of a bug class when any of these hold: the same bug shape appears in two or more
components; the bug is in shared infrastructure called by multiple components; or the bug is the absence
of safety in a function called from multiple paths. If it is, the fix addresses the architectural layer,
not the call site — the defensive-patch shape, a flag in one caller working round a bug in shared code,
is always the wrong answer. If it is not, say why the bug is local and fix it locally.

### Behaviour rules

- Before touching any file, state your understanding of the ROOT CAUSE in one sentence.
- If you hit something unexpected, do not improvise. Invoke STOP IF and report back.
- Do not refactor, rename, reformat, or tidy anything outside EXACT CHANGE.
- One pass. If it isn't right, stop and report — do not attempt iterative self-correction.
- If a task arrives without this structure, ask Jon for the missing fields before proceeding.
