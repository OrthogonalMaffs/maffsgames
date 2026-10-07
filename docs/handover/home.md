# Handover: home lane

The home lane's running handover (canon §7.8.2). Only home-lane sessions edit this file; the cloud lane's is
`docs/handover/cloud.md`. Newest first. Keep it current on the branch as you go (CLAUDE.md, checkpoint discipline).

**Home lane owns:** shared code, shared assets, CI and canon (contract F's shared fixes, then contract C), and every
docs PR: `docs/todo.md`, the roster's listed section, relisting fixed games (batched).

## 2026-10-07 (home): CI split for speed + two lanes (this PR); NEXT = contract B

**State of play.**
- main `a041590` (#94) green before this PR. Build freeze in force (canon §0.2).
- Done today: the tranche 3-6 contract (#87-#90: 18 games unlisted, the freeze, the findings register) and the
  quoted-figures contract (#91-#94: Fermi Lab, Screening Room, Core Maths Paper 1 CPI, `check-quoted-figures.py`).
  The detail is in CLAUDE.md's last two "Handover" sections (7 Oct), the history this file replaces.
- **This PR (CI + two lanes):**
  - `check-site.py --shard i/n` and `--shard-selftest n`: tier 1 runs as four shards; tier 2 and the parts that
    cannot be split run in shard 1 only. The site-wide checks are their own job.
  - Tier 4 layer A and the shared-asset tests are separate jobs; group B is B1 + B2.
  - `verify-just-pythag-it-bruv.py --part 1|2|3` and `--part-selftest`: C1, C2, C3. (The contract named two parts,
    phone and desktop; measured, the heavier half would still have taken about 5.8 minutes as a job, which leaves
    no room under the 7-minute target for main, so it is three parts dealt by measured cost.)
  - REGISTER.md is no longer edited by PRs: `audit-register.py --check` validates the yml files only; the
    `register` job regenerates and commits it on main after the Gate (canon §0.4).
  - Handover by lane (this file and `cloud.md`); CLAUDE.md's opening block is a fixed pointer; canon §7.8.1-§7.8.2.
- **Before/after timings** (canon §7.8.1): full run 10m42s -> 5m45s; site-wide critical path 6m34s -> 3m03s
  (Tier 4 layer A); shards 1m40s-2m18s at --workers 4 on 4 CPUs (not the critical path, so more workers were not
  tried). Still over 4 min as single verifiers: Equation Builder (D, 4m48s) and B1 (4m51s); a PR touching those
  games waits on them. Split them next if it matters (Equation Builder needs a --part like JPIB's).
- Planted page error in `parents/fractions` (a shard-3 page) on a throwaway branch: only shard 3 failed, Gate red.

**Next.**
1. Watch this PR's merge run on main: every job green, and the `register` job either commits
   `Regenerate REGISTER.md [skip ci]` or reports "unchanged". (It should commit: the generated header's wording
   changed in this PR, and REGISTER.md was deliberately left unregenerated here.)
2. **Contract F0** (Jon pasted it 7 Oct: B11 value comparison in bank_common.py; START only after this PR is merged and main is green), then contract C (audit batch 3) when Jon pastes it.

**Gotchas learned today.**
- On the GitHub runner the "Content verifiers" jobs still pull the Playwright image even when the plan selects
  nothing for them (about 40 seconds each), so every matrix entry costs a runner briefly on every PR. A PR run is
  now 19 jobs (16 in the matrix, was 9); two PRs at once ask for up to 38 of the 20 runners a public repo gets,
  so some jobs wait for the short skipped ones to finish. Watch for it before adding more entries.
- A flake seen once on #92's run: Simultaneous Solver at 320x568, keypad 1px. Not reproduced since.
