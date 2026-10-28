# Handover: stale plants (STALE-PLANTS, Jon, 28 Oct 2026; home lane)

**The rule.** A verifier that plants a fault must plant it through `scripts/plant_common.py` (canon 7.9): `apply_plant(src, old, new, name=)`
and `apply_re_plant` raise `StalePlant` if the target is absent, repeated (unless `allow_multiple`) or unchanged; `apply_js(page, name, code)` turns
any error while applying an in-page patch into a `StalePlant`; `is_caught(found, err)` is true only with findings and NO error. A `StalePlant`
fails the run as `STALE PLANT: <name>: <why>`. A plant is never skipped because its target is not live: that fails too. Tested by
`scripts/test-plant-common.py`. bank_common.py was not touched (frozen); the helper imports only the standard library.

**Moved onto it (this PR).**
- `verify-correlation-or-coincidence.py`: the fault loop. Before: an exception while patching or checking printed "the page broke", counted as
  CAUGHT. Proven in a scratch copy: B25 -> ZZ25 now prints `STALE PLANT: B25's old pair back ...` and exits 1. All 17 faults are still caught
  with no error on the real page, so none was hiding behind the hole.
- `verify-just-pythag-it-bruv.py`: the UI_FAULTS loop (`apply_patch` raises `StalePlant`; "the run broke" is no longer a catch).
- `test-ga4-summary.py`: a harness crash is no longer a catch; plants go through `apply_plant`.
- `check-escape-rooms.py`: the rating plants are built from any live room (the first with no label, a graded lock and a hub card not already one
  star; today canteen-hack, not rugby-mud) and FAIL, not skip, when none is live. This also exposed a loose plant: "the hub's star key saying
  grades 4-6" replaced the first of 8 matches; it now edits the star-key line itself.

**Known limit.** A CSS-only plant (`("style", ...)`) whose selector matches nothing, and an in-page assignment to a property that does not exist
yet (`X.newName = 1`), still apply without error. Both fail red when not caught (the safe direction); a selector-matches-something guard is
future work.

**The 53 unguarded verifiers to migrate when next touched (classified by audit heuristic, not verified)** (the audit's SAFE-outcome set, `AUDIT-stale-plants.txt`, 28 Oct 2026: no explicit guard, but a stale plant ends MISSED = red, so they fail in the safe direction with a misleading message; the verdicts are heuristic and the list includes some scripts with few or no plants): `audit-register.py`, `bg.py`, `check-analytics-loader.py`, `check-answer-lock.py`, `check-calculator.py`, `check-changed.py`, `check-launch-sash.py`, `check-level-logged.py`, `check-levels.py`, `check-lock-bank.py`, `check-publish-scope.py`, `check-quoted-figures.py`, `check-resit-page.py`, `check-scroll-reveal.py`, `check-site.py`, `check-student-labels.py`, `check-text-writes.py`, `ci-groups.py`, `ci_shards.py`, `fetch-answer-counts.py`, `gen-six-ps.py`, `merge-pr.py`, `scan-k-punctuation.py`, `scan-value-equivalent-options.py`, `six_ps_rules.py`, `test-analytics-loader.py`, `test-calculator-js.py`, `test-escape-art.py`, `test-exam-vocab.py`, `test-initials-overlay.py`, `test-level.py`, `test-mathtext.py`, `test-real-fonts.py`, `test-scores-offline.py`, `timing-gate.py`, `verify-angle-ace.py`, `verify-better-value-tax.py`, `verify-core-maths-paper1-tax.py`, `verify-core-maths-paper1.py`, `verify-core-maths-paper2a.py`, `verify-estimation-engine.py`, `verify-free-daily-pizza.py`, `verify-graph-sketcher.py`, `verify-graph-transformer.py`, `verify-log-laws.py`, `verify-maths-court.py`, `verify-normal-navigator.py`, `verify-probability-pioneer.py`, `verify-regression-rumble.py`, `verify-six-sevens.py`, `verify-stat-attack.py`, `verify-tax-theft.py`, `verify-the-6-ps.py`.
