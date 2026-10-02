/**
 * MaffsGames Score History
 * Device-local score history per game+level. No server call, no accounts,
 * no PII. Purely additive alongside each game's existing single-value
 * "personal best" localStorage key — does not replace or read those.
 */

(function() {
  'use strict';

  var PREFIX = 'mfg_hist_v1::';
  var MAX_HISTORY = 10;

  function key(gameSlug, level) {
    return PREFIX + gameSlug + '::' + level;
  }

  function record(gameSlug, level, score) {
    try {
      var k = key(gameSlug, level);
      var arr = JSON.parse(localStorage.getItem(k) || '[]');
      arr.unshift({ score: score, timestamp: Date.now() });
      if (arr.length > MAX_HISTORY) arr = arr.slice(0, MAX_HISTORY);
      localStorage.setItem(k, JSON.stringify(arr));
    } catch (e) {}
  }

  function get(gameSlug, level) {
    try {
      return JSON.parse(localStorage.getItem(key(gameSlug, level)) || '[]');
    } catch (e) {
      return [];
    }
  }

  window.MaffsScoreHistory = {
    record: record,
    get: get,
    MAX_HISTORY: MAX_HISTORY
  };

})();
