/**
 * MaffsGames Score History
 * Device-local score history per game+level. No server call, no accounts,
 * no PII. Purely additive alongside each game's existing single-value
 * "personal best" localStorage key — does not replace or read those.
 *
 * TOP-SCORES (Jon, 25 Oct 2026): record() also keeps each game+level's best
 * five in a key of its own (mfg_top_v1::), all time, never a score of 0 or
 * less, a tie keeping the earlier score. renderTop() draws a game's "Top
 * scores" panel from it, dates in British form. The last-10 history above is
 * what the leaderboards hub reads; it is unchanged.
 */

(function() {
  'use strict';

  var PREFIX = 'mfg_hist_v1::';
  var MAX_HISTORY = 10;
  var TOP_PREFIX = 'mfg_top_v1::';
  var TOP_N = 5;

  function key(gameSlug, level) {
    return PREFIX + gameSlug + '::' + level;
  }

  function topKey(gameSlug, level) {
    return TOP_PREFIX + gameSlug + '::' + level;
  }

  // Highest first; a tie keeps the earlier score ahead, so a later equal score
  // never displaces it. Anything not above 0 is dropped.
  function best(arr, n) {
    return arr.filter(function(e) { return e && typeof e.score === 'number' && e.score > 0; })
      .sort(function(a, b) { return (b.score - a.score) || (a.timestamp - b.timestamp); })
      .slice(0, n);
  }

  function recordTop(gameSlug, level, score, timestamp) {
    if (!(typeof score === 'number' && score > 0)) return;
    var k = topKey(gameSlug, level);
    var arr = JSON.parse(localStorage.getItem(k) || '[]');
    arr.push({ score: score, timestamp: timestamp });
    localStorage.setItem(k, JSON.stringify(best(arr, TOP_N)));
  }

  function record(gameSlug, level, score) {
    if (window.MaffsBurst && window.MaffsBurst.active()) return;   // BURST: a burst keeps no history (24 Oct 2026)
    try {
      var k = key(gameSlug, level);
      var now = Date.now();
      var arr = JSON.parse(localStorage.getItem(k) || '[]');
      arr.unshift({ score: score, timestamp: now });
      if (arr.length > MAX_HISTORY) arr = arr.slice(0, MAX_HISTORY);
      localStorage.setItem(k, JSON.stringify(arr));
      recordTop(gameSlug, level, score, now);
    } catch (e) {}
  }

  function get(gameSlug, level) {
    try {
      return JSON.parse(localStorage.getItem(key(gameSlug, level)) || '[]');
    } catch (e) {
      return [];
    }
  }

  function top(gameSlug, level, n) {
    try {
      return best(JSON.parse(localStorage.getItem(topKey(gameSlug, level)) || '[]'), n || TOP_N);
    } catch (e) {
      return [];
    }
  }

  // A game's "Top scores" panel: rows of rank, date (en-GB) and score, in the
  // lb-row markup the games style; "No scores yet" when there are none.
  function renderTop(el, gameSlug, level, n) {
    if (!el) return;
    var rows = top(gameSlug, level, n);
    el.innerHTML = rows.map(function(e, i) {
      return '<div class="lb-row"><span class="lb-rank lb-pos">#' + (i + 1) + '</span>' +
        '<span class="lb-date">' + new Date(e.timestamp).toLocaleDateString('en-GB') + '</span>' +
        '<span class="lb-score">' + e.score + '</span></div>';
    }).join('') || '<div class="lb-empty" style="text-align:center;font-size:13px;padding:12px">No scores yet</div>';
  }

  window.MaffsScoreHistory = {
    record: record,
    get: get,
    top: top,
    renderTop: renderTop,
    MAX_HISTORY: MAX_HISTORY,
    TOP_N: TOP_N
  };

})();
