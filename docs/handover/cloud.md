# Handover: cloud lane

The cloud lane's running handover (canon §7.8.2). Only cloud-lane sessions edit this file; the home lane's is
`docs/handover/home.md`. Newest first. Keep it current on the branch as you go (CLAUDE.md, checkpoint discipline).

**Cloud lane owns:** per-game fixes in games that are currently unlisted, one game per PR, each with its verifier,
closing its entries in its own `docs/audits/findings/<slug>.yml`. It never edits `schools/assets/`, the shared
modules in `scripts/`, the workflow, canon, the roster's listed section, `docs/todo.md` or
`docs/audits/REGISTER.md` (CI regenerates that on main). Relisting a fixed game is the home lane's docs PR.

**Every PR:** `python scripts/check-changed.py` before the first push; merge only on a green Gate, and never while
main's last full run is red; watch main's run after merging.

## 2026-10-07: the lane starts (written by the home lane, which set up the lanes)

- No cloud session has run since the lanes were split. The last cloud work was 6 Oct 2026 (#85 audit tranches 1-2
  and two games unlisted; #86 Core Maths Paper 1), recorded in CLAUDE.md's history.
- The unlisted games and their open findings: `docs/audits/REGISTER.md` ("By game", Listed = unlisted) and the
  roster's Unlisted section. Each has its relist checklist in `docs/todo.md` §1.53-§1.75.
- **Next:** Jon's first cloud-lane contract names the game.
