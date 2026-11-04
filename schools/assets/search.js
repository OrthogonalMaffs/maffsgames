/* MaffsSearch: the one rule that decides whether a game card matches a search (contract SEARCH-KEYWORDS, Jon, 4 Nov 2026).
   Every page that searches cards calls it: the portal's applyFilters() and MaffsCardFilter (card-filter.js, /essentials/).

   MaffsSearch.match(card, query) -> boolean
     - the haystack is the card's text plus its data-keywords (written from data/games.json by scripts/apply-meta.py and
       held there by scripts/check-meta.py), whitespace collapsed, lower case;
     - the query is split into words, and the card matches when every word is in the haystack;
     - a word longer than 3 letters ending in "s" also matches without it ("circles" finds "circle");
     - an empty query matches every card. No ranking, no fuzzy matching.
   Plain script, no dependencies: load it before the code that filters. */
(function () {
  'use strict';

  function haystack(card) {
    var kw = (card.getAttribute && card.getAttribute('data-keywords')) || '';
    return ((card.textContent || '') + ' ' + kw).replace(/\s+/g, ' ').toLowerCase();
  }

  function found(hay, word) {
    if (hay.indexOf(word) !== -1) return true;
    return word.length > 3 && word.charAt(word.length - 1) === 's' && hay.indexOf(word.slice(0, -1)) !== -1;
  }

  function match(card, query) {
    var words = String(query || '').toLowerCase().trim().split(/\s+/).filter(Boolean);
    if (!words.length) return true;
    var hay = haystack(card);
    return words.every(function (w) { return found(hay, w); });
  }

  window.MaffsSearch = { match: match };
})();
