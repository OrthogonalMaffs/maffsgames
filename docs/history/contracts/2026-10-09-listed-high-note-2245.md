CLOUD LANE — NOTE (9 Oct 2026, 22:45). Jon's ruling on item 12: option A.

1. Close prisoners-dilemma t4-002 on #232's own overlay test, which runs in CI, covers every game using the shared overlay (prisoners-dilemma included), and fails on the pre-#232 overlay. Record in the findings and docs/handover/cloud.md: "t4-002 closed by #232 (shared-overlay fix); covered by the OVERLAY-KEYS CI check; per-game check not added because the fault was in shared code."
2. Do not wire verify-prisoners-dilemma.py into CI. Delete the branch claude/youthful-feynman-anpxuq-pd-check after copying anything from its docs/handover/cloud.md that is not already on main.
3. t4-001 (leaderboard ranks the chosen opponent) stays open for Jon's design decision.
4. One small PR for the findings/handover change; merge on a green Gate. Then the cloud queue is empty until Jon's planning tomorrow.

STOP IF: the OVERLAY-KEYS CI check does not in fact include prisoners-dilemma (then report; option B is needed).
