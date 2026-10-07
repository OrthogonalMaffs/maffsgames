F1 roll-out, batch 3: eight of the cloud lane's finished games now mark through MaffsLock (canon §7.6.0). Each declares its `maffs-lock-hint` (contract LH).

**Games:** dimension-checker, curling-friction, trig-worms, component-crusher, differentiation-duel, integration-duel, spot-the-error, expectation-station. Each one now does the following:
- calls `MaffsLock.lock` first in every marking handler;
- calls `fresh` on every render;
- sends its per-question timers through `MaffsLock.timer`;
- runs its end screen through `finishOnce`;
- calls `newSession` on Start.

No local `answered` flag is left. The truth-buster, trig-identity-duel, binomial-blaster and partial-fractions-duel games are skipped, because they are still on the cloud lane's `cloud-remaining:` list.

**Faults fixed beyond swapping in the lock**
- **spot-the-error:** a double-click on a wrong step spent both attempts. A first wrong pick now opens a fresh window, in stage 1 and stage 2.
- **expectation-station:**
  - Each Check is now one attempt; a double-click had spent the retry (t2-017).
  - The game's own Next sat outside every container, so a second Enter skipped a question unseen. That was found by the check. The fix is `fresh(gameScreen)` when a question loads.
- **Register:** closed component-crusher-t4-005, curling-friction-t5-003 and dimension-checker-t5-003 (all HIGH, class 1), and expectation-station-t2-017.

**Declarations.** Four games declare more than `{}`:
- trig-worms: its Start button is "FIRE!".
- component-crusher: a typed key + 1000 at the stated precision, or the first wrong option.
- spot-the-error: a level, then the same wrong step twice.
- expectation-station: wrong tiles, wrong products, then a wrong card still open.

**Verifiers.**
- Each sweep that answers at once gets `bc.NO_LOCK_FRESH_INIT`.
- Two sweeps stub `window.setTimeout`. That silently dropped `MaffsLock.timer` callbacks, because the asset records a timer's id only after `setTimeout` returns. Both sweeps now stub `MaffsLock.timer` too.
- expectation-station's sweep re-renders stage 3 by hand, so it also calls `MaffsLock.fresh` there.

All eight verifiers pass. `check-answer-lock.py` passes for all 26 migrated games. NOT_YET is now 70.

Checkpoint stop after this PR (Jon). The handover is updated.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
