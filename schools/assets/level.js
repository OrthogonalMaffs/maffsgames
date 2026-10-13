/* MaffsLevel: the one shared way a game reads ?level= (contract LEVEL-RESOLVER, 12 Oct 2026; canon section 4.5).
 *
 * Why. 55 of 99 game pages read ?level= with their own code, in at least eight shapes. The common one,
 * `if (QUESTIONS[p.get('level')]) level = p.get('level')`, treats `constructor` and `__proto__` as levels
 * (they are inherited properties of every object) and the game crashes; others pass the raw key to
 * MaffsLeaderboard.submitScore, which creates a stray public board under whatever was typed.
 *
 * Use:
 *     var level = MaffsLevel.resolve({ slug: 'index-laws', levels: ['gcse'], fallback: 'gcse' });
 *
 *   slug      the game's folder name.
 *   levels    every level key the game serves, equal to the roster's levels for it (scripts/check-levels.py).
 *             A game with no levels declares levels: ['all'], fallback: 'all'.
 *   fallback  the game's default level; it must be one of levels.
 *   boards    optional: extra keys the game submits to the leaderboard that are boards, not levels
 *             (session lengths such as 'q20', tournament boards such as 'gcse-tournament').
 *
 * resolve() returns the ?level= value if, and only if, it is a member of the declared array (a plain
 * indexOf over the array: never a property lookup, so 'constructor', '__proto__' and 'toString' are
 * unknown keys like any other). Otherwise it returns fallback. Keys are matched exactly: 'GCSE' is not
 * 'gcse'. When a level parameter was present but is not a declared key (including an empty one) the URL's
 * level parameter is replaced with the fallback through history.replaceState, so the page, analytics and
 * any link the student shares carry a real key; the other parameters and the hash are kept. Nothing is shown
 * to the student. A page with no level parameter is left alone.
 *
 * The declaration is recorded: MaffsLevel.declared(slug) returns {levels, fallback, boards} (copies) or
 * null; its asked is true when the URL had a level parameter at all, and its fromUrl when that parameter was a declared
 * level (for a game that acts only when it was asked).
 * firebase-leaderboard.js's submitScore refuses a level that a declared game has not declared
 * (levels or boards), with a console.warn, so a stray board cannot be created whatever a game does. A page
 * with no declaration behaves as before.
 *
 * Stdlib JS only, no dependencies. It never throws: a bad declaration warns and the fallback (or 'all')
 * is returned.
 */
(function (global) {
  'use strict';

  var decls = {};

  function strings(a) {
    var out = [];
    if (!a || typeof a.length !== 'number') return out;
    for (var i = 0; i < a.length; i++) if (typeof a[i] === 'string') out.push(a[i]);
    return out;
  }

  function readParam() {
    try { return new URLSearchParams(global.location.search).get('level'); } catch (e) { return null; }
  }

  function resolve(cfg) {
    cfg = cfg || {};
    var slug = String(cfg.slug || '');
    var levels = strings(cfg.levels);
    var fallback = typeof cfg.fallback === 'string' ? cfg.fallback : (levels.length ? levels[0] : 'all');
    if (!levels.length) levels = [fallback];
    if (levels.indexOf(fallback) === -1) {
      try { console.warn('MaffsLevel: ' + slug + ' fallback "' + fallback + '" is not one of its levels'); } catch (e) {}
      fallback = levels[0];
    }
    decls[slug] = { levels: levels.slice(), fallback: fallback, boards: strings(cfg.boards), fromUrl: false, asked: false };

    var asked = readParam();
    if (asked === null) return fallback;
    decls[slug].asked = true;
    if (levels.indexOf(asked) !== -1) { decls[slug].fromUrl = true; return asked; }
    try {
      var u = new URL(global.location.href);
      u.searchParams.set('level', fallback);
      global.history.replaceState(global.history.state, '', u.pathname + u.search + u.hash);
    } catch (e) { /* a sandboxed frame may refuse; the returned key is still right */ }
    return fallback;
  }

  function declared(slug) {
    var d = Object.prototype.hasOwnProperty.call(decls, slug) ? decls[slug] : null;
    return d ? { levels: d.levels.slice(), fallback: d.fallback, boards: d.boards.slice(), fromUrl: d.fromUrl, asked: d.asked } : null;
  }

  // True when the game has declared no levels at all (not migrated) or declared this key as a level or a board.
  function allows(slug, key) {
    var d = Object.prototype.hasOwnProperty.call(decls, slug) ? decls[slug] : null;
    if (!d) return true;
    return d.levels.indexOf(key) !== -1 || d.boards.indexOf(key) !== -1;
  }

  global.MaffsLevel = { resolve: resolve, declared: declared, allows: allows };
})(typeof window !== 'undefined' ? window : this);
