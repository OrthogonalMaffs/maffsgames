/* MaffsOptions — assemble a question's answer options, safely.
 *
 * WHY THIS EXISTS
 * ---------------
 * 32 games hand-roll the same line:
 *
 *     const opts = shuffle([q.correct, ...q.d]);
 *
 * and not one of them checks whether a distractor happens to equal the correct
 * answer, or another distractor. When that happens the question renders the same
 * option twice, which is not merely untidy — two identical buttons out of four is
 * a strong hint, so the question gives itself away to a student who has not done
 * the maths.
 *
 * It has happened three times that we know of, in three different shapes:
 *
 *   - Trig Worms COMPUTED its distractors and deduped them against the correct
 *     answer only, so when asin and atan of the same near-zero ratio both returned
 *     -5.1 it shipped -5.1 twice. Fixed 2026-09-22 (42aa9f2).
 *   - matrix-crunch:171 AUTHORED the collision: det([[6,2],[3,1]]) is 0, and '0'
 *     was also listed in its own distractor array, so the question rendered
 *     0, 0, 12, 6 with two buttons both marking correct.
 *   - formula-unlocked:295 DRIFTED into it: a late `correct_override` was set to a
 *     string identical to the question's third distractor, so the override and that
 *     distractor became twins and the bank's real `correct` form never reached the
 *     screen at all.
 *
 * The lesson from Trig Worms was written into CLAUDE.md as a rule for authors.
 * A rule cannot be applied platform-wide, because there was nowhere to apply it:
 * every game assembled its own options. This is that nowhere, made somewhere.
 *
 * WHAT IT GUARANTEES
 * ------------------
 *   - the correct answer is always present, exactly once
 *   - no two options share a key, so a duplicate can never render
 *   - order is shuffled, and the shuffle is bounded (Fisher-Yates, i-- every pass)
 *   - it never retries a random draw, per CLAUDE.md's "No rejection sampling":
 *     build the pool, dedupe, shuffle, slice. A loop that exits only when the dice
 *     cooperate is a hang waiting for the right question.
 *
 * WHAT IT DOES NOT DO
 * -------------------
 * It cannot invent a replacement for a distractor it had to drop. A bank that
 * authored a collision has one fewer real option than its author intended, and
 * this returns three options rather than four — honestly short, like
 * modular-battle showing 2 buttons when a modulus of 2 has only 2 residues.
 * Fixing the bank is a teaching call and stays a teaching call; this only
 * guarantees the collision never reaches a student.
 *
 * THE KEY
 * -------
 * Options are compared on `String(value)` by default, because that is exactly
 * what `dataset.val = v` stores and what the marking code compares — canon §7.1,
 * "Answer matching via dataset.val always, never compare rendered HTML strings".
 * Deduping on any other representation would let through a pair that the answer
 * check cannot tell apart, which is the whole failure being prevented. Pass your
 * own `key` only if your game marks on something else.
 *
 * USAGE
 * -----
 *   const opts = MaffsOptions.build(q.correct, q.d);          // drop-in
 *   const opts = MaffsOptions.build(correctVal, q.d, {max: 4});
 *   const opts = MaffsOptions.build(c, d, {key: o => o.id});  // objects
 */
(function () {
  'use strict';

  function shuffle(arr) {
    // Fisher-Yates. i-- runs on every pass whatever Math.random returns, so this
    // is bounded -- the property that separates it from rejection sampling.
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = arr[i];
      arr[i] = arr[j];
      arr[j] = t;
    }
    return arr;
  }

  function build(correct, distractors, options) {
    var opts = options || {};
    var max = typeof opts.max === 'number' ? opts.max : 4;
    var key = typeof opts.key === 'function' ? opts.key : String;
    var list = Array.isArray(distractors) ? distractors : [];

    var seen = new Set([key(correct)]);
    var pool = [];
    var dropped = [];

    for (var i = 0; i < list.length; i++) {
      var k = key(list[i]);
      if (seen.has(k)) {
        // Equal to the correct answer, or to a distractor already kept. Either
        // way it cannot be rendered as a separate choice.
        dropped.push(k);
        continue;
      }
      seen.add(k);
      pool.push(list[i]);
    }

    if (dropped.length && typeof console !== 'undefined' && console.warn) {
      // warn, not error: a console.error fails check-site.py tier 1, and this is
      // a bank defect to be seen and fixed, not a reason to call the page broken.
      console.warn('[MaffsOptions] dropped ' + dropped.length +
                   ' duplicate option(s): ' + dropped.join(' | ') +
                   ' — this question is now short an option. Fix the bank.');
    }

    shuffle(pool);
    if (max > 0) pool = pool.slice(0, max - 1);

    build.lastDropped = dropped;
    return shuffle([correct].concat(pool));
  }

  build.lastDropped = [];

  window.MaffsOptions = { build: build, shuffle: shuffle };
})();
