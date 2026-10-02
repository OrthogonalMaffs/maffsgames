/* MaffsSession — session-length buttons that never promise more than the bank holds.
 *
 * WHY THIS EXISTS
 * ---------------
 * Five games shipped fixed length buttons (8/16/24, or 10/20/30) and slice to the
 * bank with `shuffle(pool).slice(0, Math.min(sessionLength, pool.length))`. The
 * slice is safe — it never throws, never serves more than the bank has — but the
 * BUTTON is a promise the slice quietly breaks: pick "24" against a 15-question
 * bank and the game serves 15 while the label still says 24.
 *
 * Expectation Station shipped this first (core 20, GCSE 15, A-level 10 against
 * fixed 8/16/24 buttons) and was hand-fixed in this session before the shape was
 * known to be a class. Once it was: better-value (gcse 20 vs 10/20/30),
 * expected-damage (ks3/core 15 vs 10/20), spot-the-muppet (core/gcse/ks3
 * 12/20/18 vs 10/20/30) and wrong-on-the-internet (core/gcse/ks3 10/20/15 vs
 * 10/20/30) all had the identical defect. Hand-patching each would have made
 * five separate implementations of one rule — this is that rule, made once.
 *
 * WHAT IT GUARANTEES
 * ------------------
 *   - every offered button serves exactly its label's number of questions
 *   - a length is only offered if the pool can fill it
 *   - a pool size that isn't a multiple of the preferred lengths gets an
 *     honest "All (n)" button instead of silently rounding down to the
 *     largest preferred length that fits
 *   - if the previously-selected length is no longer offered (a level or
 *     filter change shrank the pool), the largest offered length is selected
 *     instead — never a length the new pool can't fill
 *
 * WHAT IT DOES NOT DO
 * -------------------
 * It does not grow a bank. A bank below the preferred lengths gets an
 * honest smaller set of buttons, not more questions — that is a content
 * decision (docs/todo.md §5), not a code one. It also does not compute the
 * pool itself: the caller must know the pool size before the student can
 * pick a length, which means the pool must be determined by level/filter
 * selection, not by the Start button.
 *
 * USAGE
 * -----
 *   MaffsSession.render({
 *     mount: document.getElementById('sessionSelect'),
 *     poolSize: QUESTIONS[currentLevel].length,
 *     preferred: [10, 20, 30],           // default [8, 16, 24]
 *     selected: sessionLength,           // the caller's current choice, if any
 *     selectedClass: 'selected',         // default 'selected'; pass 'active' if
 *                                        // the game's own CSS uses that instead
 *     onChange: count => { sessionLength = count; }
 *   });
 *
 * Call it once on load and again every time the pool can change size — a level
 * switch, a topic-filter toggle. It re-derives the offered lengths from the new
 * poolSize each time, so there is nothing else to keep in sync.
 *
 * `MaffsSession.lengths(poolSize, preferred)` returns just the offered-length
 * array, for a caller that wants to compute this without touching the DOM.
 */
(function () {
  'use strict';

  var DEFAULT_PREFERRED = [8, 16, 24];

  function lengths(poolSize, preferred) {
    var pref = Array.isArray(preferred) && preferred.length ? preferred : DEFAULT_PREFERRED;
    var offered = pref.filter(function (c) { return poolSize >= c; });
    if (offered.indexOf(poolSize) === -1) offered.push(poolSize);
    return offered;
  }

  function render(opts) {
    opts = opts || {};
    var mount = opts.mount;
    var poolSize = opts.poolSize;
    var onChange = opts.onChange;
    if (!mount || typeof poolSize !== 'number' || typeof onChange !== 'function') return null;

    var preferred = Array.isArray(opts.preferred) && opts.preferred.length ? opts.preferred : DEFAULT_PREFERRED;
    var selectedClass = opts.selectedClass || 'selected';
    var offered = lengths(poolSize, preferred);
    var wanted = offered.indexOf(opts.selected) !== -1 ? opts.selected : offered[offered.length - 1];

    mount.innerHTML = '';
    offered.forEach(function (count) {
      var btn = document.createElement('button');
      btn.className = 'session-btn' + (count === wanted ? ' ' + selectedClass : '');
      btn.dataset.count = count;
      btn.textContent = preferred.indexOf(count) !== -1 ? String(count) : ('All (' + count + ')');
      btn.addEventListener('click', function () {
        var siblings = mount.querySelectorAll('.session-btn');
        for (var i = 0; i < siblings.length; i++) siblings[i].classList.remove(selectedClass);
        btn.classList.add(selectedClass);
        onChange(count);
      });
      mount.appendChild(btn);
    });

    onChange(wanted);
    return wanted;
  }

  window.MaffsSession = { lengths: lengths, render: render };
})();
