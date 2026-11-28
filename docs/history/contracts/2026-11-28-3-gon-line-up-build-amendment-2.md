3-GON-LINE-UP-BUILD AMENDMENT 2 (Project Claude, 28 Nov 2026, ruling on the audit-register self-test STOP).

Ruling: approved. Your diagnosis is confirmed on main: scripts/audit-register.py:450 takes the first findings file by name, and plants 1 and 2 (lines 455, 464-465) write into its findings[0] and findings[-1]; 34 findings files are `findings: []`, and 3-gon-line-up.yml now sorts first. This is a fault in a shared checker (any slug sorting before 52dle hits it), so the fix goes in the checker, not this game.

Changes to the contract:
1. Lane exception for scripts/audit-register.py's self-test only: choose the plant file by content, as the first file in name order whose findings list is non-empty. If no file has a finding, the self-test fails with a clear message rather than crashing. Read the rest of the self-test (every plant) for the same assumption, that a particular file or entry exists by position or name, and fix each instance the same way. Report every line you change. Nothing else in that file or in any other checker changes.
2. Prove it: with the fix, audit-register.py --check --selftest passes on your branch, every plant still reports "caught", and it still passes with 3-gon-line-up.yml removed (the old order).
3. Your rejected workarounds stay rejected: no renamed file, no invented finding.
4. Save this amendment verbatim as docs/handover/contracts/2026-11-28-3-gon-line-up-build-amendment-2.md and include it in the PR.

Then re-run the Gate and merge with merge-pr.py on green. The tier is unchanged: Medium.
