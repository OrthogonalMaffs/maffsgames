# LOCAL-FLAKES: why some checks failed on Jon's Windows machine and passed in CI (18 Oct 2026)

Contract: `docs/handover/contracts/2026-10-18-local-flakes.md`. Branch `claude/local-flakes`.

## Cause (one, for every check below)

`scripts/serve-stubbed.py` is the local server the browser checks load their pages from. Its `ThreadingHTTPServer`
used socketserver's default `request_queue_size` of 5. Chromium opens up to six parallel connections per page, and
several checks load pages at once (`check-changed.py` runs up to six light checks beside one heavy one). On Windows a
full listen backlog is refused outright, so a page or one of its scripts got `net::ERR_CONNECTION_REFUSED`. A missing
script then shows as `X is not defined` page errors or as a tap that never lands (30 s timeout). Linux CI queues the
overflow instead of refusing it, which is why CI never saw it.

Not the cause: fixed sleeps. The answer-lock driver already waits on state, so no wait was changed.

## Proof

1. Instrumented failing runs showed `ERR_CONNECTION_REFUSED` on requests to the local server and the `X is not defined`
   page errors that follow.
2. A/B stress, 120 page loads against the server in the same pattern: stock queue 323 and 263 refusals (two runs);
   `request_queue_size = 128` 0 refusals; the fixed `serve-stubbed.py` itself 0 refusals.
3. The ten-run series below, before and after.

## Fix

`serve-stubbed.py`: `class Server(http.server.ThreadingHTTPServer)` with `request_queue_size = 128`. A queue deep
enough for every page a check can have in flight leaves nothing to refuse. No game code and nothing under
`schools/assets/` was touched, and no sleep was lengthened.

## Results, per check (runs passed / runs, sequential)

| Check | Before, idle | Before, loaded | After, idle |
|---|---|---|---|
| Estimation Engine (`verify-estimation-engine.py`) | 10/10 | 9/10 | 10/10 |
| Quadratic Factoriser self-test | 9/10 (run 1 contaminated) | 0/10 | 10/10 |
| Escape-room difficulty stars (`test-escape-rating.py`) | 10/10 | 0/9 | 10/10 |
| Level resolver part 1 (`test-level.py --games --part 1/4`) | 9/10 | not run | 10/10 |
| Answer lock part 5 | 9/10 | failed, `Page.goto` refused | 10/10 |
| Answer lock part 6 | 10/10 | failed in the full run | 10/10 |
| Answer lock part 1 (with self-test) | 10/10 | failed in the full run | 10/10 |

After the fix: 70/70 idle runs passed. "Loaded" means a full `check-changed.py` running alongside.

### Per check

- **Estimation Engine.** Loaded failure was a keypad tap timing out at 30 s, consistent with a script that never loaded.
- **Quadratic Factoriser self-test and difficulty stars.** Fail every time under load, because they start their own
  stub server and several pages hit it together. Both pass 10/10 after.
- **Level resolver part 1 (idle failure, run 10: `MaffsInvite` not defined)** and **Answer lock part 5 (idle failure,
  run 4: component-crusher)**. Not instrumented at the time. They match the refusal signature and did not recur in 10
  runs each after the fix.
- **Answer lock parts 1, 5, 6.** Loaded failures were refusals on `Page.goto`; after the fix, idle 30/30.
- **Text writes.** Failed once in a full run because my own scratch scripts were in `scripts/`; deleted, passes. Not a
  flake.

## Still open

The loaded post-fix 10x set is running as this PR goes up (the load is a full `check-changed.py --full` on this
branch). Its result will be added here in the next PR.
