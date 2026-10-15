# Build freeze (6 Oct 2026 to 15 Oct 2026), archived

Moved verbatim from canon §0.2 when Jon lifted the freeze on 15 Oct 2026. History only: nothing here is in force.

**BUILD FREEZE (Jon, 6 Oct 2026).** No new builds (games, modes, stages) until the exit bar is met:
1. every live game has a verifier in CI;
2. every CRITICAL and HIGH in the findings register fixed;
3. shared checks green site-wide (answer lock, level resolver, SR-14 fields, B11 parser);
4. ~~every level serves 40+~~ (no longer a gate condition; see below);
5. every unlisted game relisted or archived;
6. one sweep of the already-verified games for true wrong options and unstated conventions.

Bank depth (40+ per level, and served bank size) is tracked in the register and worked on in parallel under SR-26; it does not block new builds (Jon, 12 Oct 2026: "increasing the question banks should not stop new builds, we can have that running alongside the builds.").

**One named exception (Jon, 9 Oct 2026, 00:25): Simultaneous Solver Stage 5 only** (word problems, the two
equations built from tiles; merged #203). No other build is excepted: a further exception needs Jon's own named
ruling, never a contract's inference. **Glorious Gantt Game (`glorious-gantt`) is excluded from points 1, 2, 3 and 5 while it is in the roster's Unlisted section (Jon, 12 Oct 2026 for 1, 2 and 5; 13 Oct 2026 for 3). It stays live at its URL, as Jon accepted.** The register's exit-bar dashboard
(`docs/audits/REGISTER.md`) shows how far the site is from each point.
