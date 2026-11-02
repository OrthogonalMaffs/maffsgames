# Local rendering and browser tests

Use `python -X utf8 scripts/serve-stubbed.py` (default http://127.0.0.1:8765/) for local rendering. Never check layout against the live endpoint: it writes production rows. Background startup follows AGENTS.md.

Always cache-bust with `?cb=<random>` on page loads and live fetches. Preview a scratch copy using `--against`; never swap the repository's game file for a preview.

For end-to-end play, capture the game's own `setTimeout` callbacks and drain them synchronously, in order; this is test-only and is never committed.

The stub server replaces `window.fetch` site-wide; an in-page fetch throws `Error: stubbed`. Use `XMLHttpRequest` to read a file in a test.

Separate worktrees still share Firebase, Sheets, GA4, server ports and Actions use. Stubs protect the backends; use distinct ports, letting the server choose a free one where supported.

Reason and testing history: canon §12, “Local render testing” and “RULEBOOK”.
