# Handover: home lane

The home lane's running handover (canon §7.8.2). Only home-lane sessions edit this file; the cloud lane's is
`docs/handover/cloud.md`. Newest first. Keep it current on the branch as you go (CLAUDE.md, checkpoint discipline).

**STANDING RULE (Jon, 7 Oct 2026):** when a contract finishes and the next queued contract's start condition is
met, start it without asking. Stop only for a STOP IF, a decision no standing ruling covers, or an empty queue.

**Home lane owns:** shared code, shared assets, CI and canon (contract F's shared fixes, then contract C), and every
docs PR: `docs/todo.md`, the roster's listed section, relisting fixed games (batched).

**QUEUE (home lane, Jon 7 Oct):**
1. **V: each verifier declares its own CI group** (#108, this entry).
2. **C (revised 7 Oct): audit batch 3**, one game per PR in this order: proportion-blaster, better-value,
   given-that, formula-unlocked, sequence-solver, estimation-golf. The contract text is in Jon's 7 Oct paste;
   its rules are summarised in the next entry when it starts. Each verifier declares its own ci-line (no
   workflow edit).
3. F1, when Jon pastes it.

**Jon's rulings, 7 Oct:** eigenvector-engine-f0-005 is not a judgement call (SR-17: a scalar multiple of an
eigenvector is never a wrong option, whatever the prompt says about "simplest"): `jc: false` (in #108). The
verifier-lines-in-the-workflow question is answered by contract V: neither lane edits the workflow for a verifier.

## 2026-10-07 (home): contract C game 5, Sequence Solver

- **#116 (Formula Unlocked) merged** on a green Gate, main green after #114.
- **This PR:** alevel[49]'s "0.999..." replaced by 10 (r-001); gcse[6]'s B11 pair replaced by 3n + 7.
  `verify-sequence-solver.py` (B3) recomputes all 154 keys; on main it failed on exactly r-001 and the B11 pair: no
  other wrong key. r-002 and r-003 stay open.
- **Next:** game 6, Estimation Golf (committed locally on claude/c-estimation-golf in worktree ../mg-eg): :680
  keyed 565.49 (choice recorded: the true value, not "use pi = 3.14"), :663 states the forward difference and
  3 d.p. and keys 27.009.

## 2026-10-07 (home): contract C game 4, Formula Unlocked (#116)

- **#114 (Given That) merged** on a green Gate, main green after #113.
- **#116:** Q_ALEVEL[0]'s value-equal option replaced by named slips, override and duplicate dropped (r-001);
  value-equal wrong options replaced in Q_LEVEL4[10] (f0-001, closed), Q_GCSE[22] and Q_GCSE[23] (audit F3, F4:
  not register entries; F3 was a B11 ledger entry). `verify-formula-unlocked.py` (B3, SymPy). On main it failed on
  exactly those four items: every key satisfies its formula, no other wrong key.
- **Next:** game 5, Sequence Solver (r-001: "0.999..." beside 1; the replacement is 10, the sum taken with first
  term 9). Its B11 ledger pair (gcse[6] -3n + 10 = 10 - 3n) is fixed in the same PR. r-002 (raw TeX on screen) and
  r-003 (jc) stay open.

## 2026-10-07 (home): contract C game 3, Given That (#114)

- **#113 (Better Value) merged** on a green Gate, after main's run on the cloud lane's #112 (Dimension Checker,
  which declared its verifier by ci-line header: no workflow edit) was green.
- **#114:** alevel_18's Venn regions from its stored totals (r-001); free entry on `MaffsAnswer.decimal` with the
  precision stated on every free-entry question (r-002, r-003); F4/F5's value-equal options replaced, two B11
  ledger entries cleared. `verify-given-that.py` (B3) has a reviewed SPEC for all 180 keys. On main it failed on
  exactly r-001, r-002, r-003 and F4/F5: no other wrong key.
- **Decision taken (for Jon to see):** one precision for all free entry would not do. At 3 d.p. two small keys
  (core_06 0.0518, alevel_25 0.0297) round the same as another ratio on their own diagram, and a 4 d.p. stored
  value rounded again gives the wrong 3 d.p. key for 6/11 and 136/228 (the verifier caught both in my first
  version). So N keeps three significant figures: 3 d.p. from 0.1 up, 4 from 0.01, 5 below, stated per
  question; the two stored values carry more places. Fractions and percentages are no longer accepted (MaffsAnswer
  reads plain decimals): the placeholder says "e.g. 0.429".
- Not in scope, still open: audit F6 (no phase 1 explanation at the typed levels); Given That's typed answers are
  not yet on MaffsKeypad (canon 4.4 rollout).

## 2026-10-07 (home): contract C game 2, Better Value (#113)

- **#111 (Proportion Blaster) merged** on a green Gate (B3 ran its verifier by its header alone).
- **#113:** five Core conclusions corrected from the recomputed figures (r-001..r-005) and core_033's working put
  in pence (r-009, closed too: the verifier proves its equation solved to 425). core_009 needed its repayment
  stated (GBP 90.20/month, 8% APR effective over 24 months) to be answerable; the old key is now a wrong card,
  explained. `verify-better-value.py` (B3): every figure in a keyed card or explanation must be a given or a
  recomputed value at its printed precision. On main it failed on exactly r-001..r-005 and r-009: no other wrong
  figure in the 70 items. Open (jc: true): r-006, r-007, r-008.
- **Next:** game 3, Given That. Spec reviewed for all 180 keys (num/den by named quantity, Yes/No tables'
  headers pinned); plan: alevel_18's Venn regions from its stored totals (onlyB 15, neither 55), free entry on
  `MaffsAnswer.decimal` at 3 d.p. stated on every free-entry question, gcse_14/gcse_23 value-equal options
  replaced (audit F4/F5).

## 2026-10-07 (home): contract C game 1, Proportion Blaster (#111)

- **V (#108) merged** on a green Gate (51/51 content lines ran); main's full run after it: see the next entry.
- **Contract C (Jon, 7 Oct, revised):** audit batch 3, one game per PR, in order: proportion-blaster, better-value,
  given-that, formula-unlocked, sequence-solver, estimation-golf. Each: a verifier that recomputes every key
  (SR-4/SR-16 option checks, explanation figures), declaring its own ci-line; the game's register entries
  set fixed with the PR; other open entries the verifier proves are one-line data fixes may be closed too;
  shared-class entries (classes 1, 4, 5) stay open. STOP IF a verifier finds more wrong keys than the register
  lists (file them, stop) or a fix would change wording beyond the named item. Do not touch engines, scoring,
  levels, leaderboard keys, other games, estimation-golf's proximity scoring, or the workflow.
- **#111:** alevel[47] keyed 900/11 (r-001 fixed); F2-F5's value-equal wrong options replaced by named errors,
  five B11 ledger entries cleared; `verify-proportion-blaster.py` in B3. On main it failed on exactly r-001
  and F2-F5: no other wrong key. Not fixed (beyond the named items): gcse[16] and gcse[21] ask "Find x" from x^2
  without "positive" (SR-17); -5 is not offered, so nothing is mis-marked. Audit F6 (raw TeX in the context
  line) and F7 (no explanation, auto-advance) are not register entries and were left.
- **Next:** game 2, Better Value (r-001..r-005; r-009 too, since the verifier proves its explanation's equation
  solves to 425). Verifier drafted: every keyed and explanation figure must be a given or a recomputed value at
  its printed precision; on main it flags exactly r-001..r-005 and r-009.

## 2026-10-07 (home): contract V, verifiers declare their own CI group (#108)

- **Why:** each new verifier edited `.github/workflows/check-site.yml` (the cloud lane's #96, #97, #100-#102), two
  conflicted with home-lane PRs, and canon §7.8.2 and the cloud contract disagreed about it.
- **Headers:** every content script carries `# ci-line: <group> | <label> | <args>` (51 lines in 47 scripts,
  including `stats_common.py`, `uk_rates.py` and `check-resit-fixes.py`); `&&` in `<args>` runs the script again,
  so the C and D parts (`--part-selftest && --part 1`) and Fermi Lab / Screening Room (` && --selftest`) are
  expressed exactly. `verify-regression-rumble.py` carries `# ci-held:` (the HELD dict is gone). Optional
  `# ci-deps: <paths>` adds dependencies (none uses it yet: ci-deps.py had no per-verifier central rule to move).
- **`scripts/ci-groups.py`:** reads the headers; `GROUPS` holds the 12 groups' job names and timeouts (unchanged);
  the plan job writes the matrix (`groups` output) and the new `content` job runs `fromJSON` of it with the same
  container and steps as `check-site` (YAML anchors `check-container`, `check-steps`). Job names unchanged; the
  Gate needs `content` too, so nothing is hidden from it. Site-wide jobs stay static in the workflow.
- **Proof (item 5):** `ci-groups.py --compare <workflow>` ran in the plan job on the commit that still had the
  static lists. Its first run caught the cloud lane's Integration Duel line, merged to main minutes earlier (51 static
  lines, 50 from headers: DIFFERENT); after merging main and adding that header, 51 = 51, EQUAL. Then the lists
  were deleted.
- **Readers of the workflow moved to the headers:** `ci-deps.py` (checks + `# ci-deps:`), `check-changed.py` (via
  ci-deps), `audit-register.py` (which games have a verifier: without this, REGISTER.md would have said 97 of 97
  games have none), and the `--part-selftest`s of Just Pythag It, Bruv and Equation Builder ("CI runs every part").
- **`check-verifier-coverage.py`:** a verify-*.py with no ci-line and no ci-held fails; an unknown group fails; a
  verifier listed in the workflow, or declared AND listed, fails. Reports each group's check seconds from
  `scripts/ci-timings.json` (recorded from main's run 37625188261 after #107 by `ci-groups.py --record-timings`;
  B4 164s is the largest, setup excluded) and flags any over 240s.
- **Success proof:** throwaway PR #110 (based on this branch) added only `scripts/verify-zz-v-probe.py` with a
  `B3` ci-line: the plan selected just it, and B3 ran it (1 line run, 5 skipped; run 37626296241); closed and
  deleted. #108's own full run (CI changed, so everything): 51 of 51 content lines ran, Gate green, 4m39s.
- **The cloud lane merged twice while this was open** (#107 Integration Duel, #109 Curling Friction), each adding a
  workflow line; each time main was merged in, the verifier given its header, and `--compare` against main's
  workflow re-run: 52 = 52, EQUAL, before the merge.
- **For the cloud lane:** add the verifier's `# ci-line:` header in its own file; never edit the workflow for it.
  Canon §7.8.2 says so (the cloud handover is the cloud lane's to update).

## 2026-10-07 (home): queue item 2, every content job under 4 minutes

- Main's full run after #99 (before): D 5m23s, B2 4m33s (the cloud lane had added three verifiers to it),
  C3 4m04s, C2 3m57s, A 3m34s, B1 3m32s.
- **D:** `verify-equation-builder.py --part i/n` splits by candidate arrangement, not by question: eb_ks3_012 alone
  has 31,032 candidates and is 60% of the time. Whole-question checks run in part 1; the planted-fault self-test now
  also runs each fault through both parts and requires them to fail exactly where the whole run does;
  `--part-selftest` proves every candidate is in one part. Locally: 121 s and 124 s against 185 s whole.
- **C:** four parts (C4 added); **B:** four groups, cut by the slowest time each line has taken on main (runners vary up to 1.8x: Log Laws 30-55 s, Growth and Decay 58-93 s). Timeouts 6-8 min (budget 75%). 19 matrix entries now (was 16): more runner pressure when both lanes run.
- Canon §7.8.1: no content job past 4 minutes; a new verifier goes where that holds.
- **After (#103's full run):** every job 3m38s or less (A 3m38s, B2 3m29s, C4 3m10s, C1-C3 2m50s-3m06s, B1/B3/B4 2m47s-2m50s,
  D1 1m56s, D2 2m03s); the whole run 4m47s (main after #99: 6m19s).
- **For Jon:** the cloud lane's #96, #97, #100 and #101 each edited `.github/workflows/check-site.yml` (adding their
  verifier to a B group). Canon §7.8.2 reserves the workflow for the home lane. It did no harm (the lines were
  needed and CI passed), but either the rule should allow "add my verifier's line to a content group" or the cloud
  lane should hand those lines to the home lane. Your call.

## 2026-10-07 (home): contract F0, B11 sees the value-equal shapes it skipped

- **Fixtures first:** `scripts/test-bank-common.py` (CI, Tier 4 layer A job), 13 equal pairs from the tranche 5-6 items
  (differentiation-duel :820/:848, binomial-blaster :134, force-resolver :118/:138, moments-master :180,
  eigenvector-engine :117/:128, complex-converter ids 21/40, boolean-blitz :584/:744, plus a Boolean distributive law)
  and 14 look-alikes that must stay unequal. All 13 failed on main's parser (commit 630ff40), all pass now.
- **`bank_common.py`:** `parse_value(raw, ctx)` / `value_equal_pairs(pool, ctx)` with `item_context(slug, q)`;
  juxtaposition, `\binom`, trig of constants in degrees, ≈ chains, SI prefixes, `vector`, `polar`, `bool` kinds
  (canon §7.1, the B11 paragraph). Exact throughout. `VECTOR_DIRECTION_GAMES` and `BOOLEAN_GAMES` tag the two games
  whose ask is in code, not in the item.
- **First run: 42 new pairs in 9 games** (eigenvector-engine 11, boolean-blitz 10, complex-converter 8,
  differentiation-duel 5, force-resolver 4, formula-unlocked, log-laws, moments-master, binomial-blaster 1 each).
  28 were already in the register: each ledger entry carries `"register": "<id>"`. 14 are new findings
  `<slug>-f0-NNN` (eigenvector-engine 7, boolean-blitz 4, force-resolver, formula-unlocked, log-laws 1 each;
  log-laws had no register file, so F0 opened one, its `audited` entry saying it is a B11 run, not an audit).
  Two misreads found on the way and fixed with fixtures: "vs" read as v·s; "1! = 1" read as a value.
- `check-banks.py --write-ledger` now carries each entry's `register` link over (`keep_register_links`).
- Planted `12\cos 90° N` beside the key `0 N` in a scratch copy of force-resolver's bank: `--ci` fails on it as NEW.

## 2026-10-07 (home): CI split for speed + two lanes (#95, merged); NEXT = contract F0

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
