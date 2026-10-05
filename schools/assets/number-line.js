/* MaffsNumberLine — marking a placement on a number line (canon §7.1.2). One copy, for every game.
 *
 * Canon §7.1.2: a tolerance is never wide enough to accept a named wrong answer. On a number line
 * the named wrong answers are the neighbouring positions the student can place on, so the rule
 * depends on how the marker moves:
 *
 *   MaffsNumberLine.placementCorrect({placed, target, mode: 'snapped'})
 *       The marker snaps to a grid and shows its value, so the student sees exactly what they
 *       placed. Marked by exact match: true only when placed equals target (to 1e-9, a guard for
 *       floating point only). A tolerance of even one grid step would accept a neighbour while the
 *       marker's own label shows the wrong value (Negative Number Line accepted 0 and 1 for 0.5,
 *       and -2.5 for -3, until 4 Oct 2026). placed may be null (nothing placed yet): false.
 *
 *   MaffsNumberLine.placementCorrect({placed, target, mode: 'continuous'})
 *       A freely dragged marker (Decimal Detective's Place It). Not built: it waits for Jon's
 *       ruling on the resit audit's Decimal Detective F4 (the live 2 d.p. readout), so it throws
 *       rather than guess a band.
 *
 * A snapped line must give the student a way to reach every grid position on a phone; Negative
 * Number Line's ◀ ▶ step buttons are the pattern (a 0.5 step is 7.4px at 390px wide).
 * scripts/verify-negative-number-line.py runs the snapped rule through real taps, in CI.
 */
(function () {
  'use strict';
  var EPS = 1e-9;

  function finite(x) {
    return typeof x === 'number' && isFinite(x);
  }

  function placementCorrect(opts) {
    var mode = opts && opts.mode;
    if (mode === 'continuous') {
      throw new Error('MaffsNumberLine: continuous placement is awaiting ruling (audit DD F4)');
    }
    if (mode !== 'snapped') {
      throw new Error('MaffsNumberLine: unknown mode ' + mode);
    }
    if (!finite(opts.target)) {
      throw new Error('MaffsNumberLine: target must be a finite number, got ' + opts.target);
    }
    if (!finite(opts.placed)) return false;
    return Math.abs(opts.placed - opts.target) < EPS;
  }

  window.MaffsNumberLine = { placementCorrect: placementCorrect };
})();
