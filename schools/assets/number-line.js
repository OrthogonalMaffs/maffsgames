/* MaffsNumberLine — marking a placement on a number line (canon §7.1.2). One copy, for every game.
 *
 * Canon §7.1.2: every number-line placement snaps to a grid containing every target, is marked by
 * exact match through this helper, and offers step buttons on phones. On a number line the named
 * wrong answers are the neighbouring positions the student can place on, so a tolerance of even one
 * grid step would accept one of them (Negative Number Line accepted 0 and 1 for 0.5, and -2.5 for -3,
 * until 4 Oct 2026; Decimal Detective marked a freely dragged marker by a band until 5 Oct 2026).
 *
 *   MaffsNumberLine.placementCorrect({placed, target, mode: 'snapped'})
 *       True only when placed equals target (to 1e-9, a guard for floating point only). placed may
 *       be null (nothing placed yet): false.
 *
 * There is no other mode: 'continuous' (a free marker marked by a band) was removed on Jon's ruling on
 * the resit audit's Decimal Detective F4 (5 Oct 2026), and any mode but 'snapped' throws, so no game
 * can bring a tolerance band back through this helper.
 *
 * A snapped line must give the student a way to reach every grid position on a phone: the ◀ ▶ step
 * buttons and the arrow keys (Negative Number Line: a 0.5 step is 7.4px at 390px wide; Decimal
 * Detective: half a tick gap). scripts/verify-negative-number-line.py and
 * scripts/verify-decimal-detective.py run the rule through real taps, in CI.
 */
(function () {
  'use strict';
  var EPS = 1e-9;

  function finite(x) {
    return typeof x === 'number' && isFinite(x);
  }

  function placementCorrect(opts) {
    var mode = opts && opts.mode;
    if (mode !== 'snapped') {
      throw new Error('MaffsNumberLine: number-line placements must snap (canon §7.1.2); got mode ' + mode);
    }
    if (!finite(opts.target)) {
      throw new Error('MaffsNumberLine: target must be a finite number, got ' + opts.target);
    }
    if (!finite(opts.placed)) return false;
    return Math.abs(opts.placed - opts.target) < EPS;
  }

  window.MaffsNumberLine = { placementCorrect: placementCorrect };
})();
