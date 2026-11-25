/* The homepage announcement strip. Data-driven since ANNOUNCE-STRIP (Jon, 25 Nov 2026): the announcements are the homepage's inline
 * <script type="application/json" id="announcements"> block, {"items":[{"id", "text", "href", "end", "start"?}]}, so a new
 * announcement is an entry there, not a change to this file. It first carried "Our 100th: The 6 P's" (SIX-PS-LAUNCH, Jon,
 * 27 Oct 2026, ended 10 Nov 2026). Homepage only.
 *
 * A claim with a date in it goes stale: every item carries its own end (an ISO 8601 instant) and is hidden from that instant on,
 * whatever anyone remembers to do (the same rule as the answer counts). An item with no end, or one that is not a valid instant,
 * is never shown; an optional start holds an item back until then. The first live item is drawn; with no block, an unreadable
 * block or no live item, nothing is drawn. scripts/check-launch-sash.py checks the block, the clock comparison and that no page but
 * the homepage loads this file.
 *
 * A thin gold announcement strip across the full width, in the page's flow between the hero and the scores ticker (it replaced the
 * diagonal corner ribbon on 29 Oct 2026, which covered the hero's Leaderboards link). Static: no animation.
 * No analytics labels (data-mfg-*): a time-limited element must not be one the portal's click test counts, or that test fails the day it ends.
 * It is an ordinary link: keyboard focus, a visible focus ring, text contrast above 4.5:1.
 */
(function () {
  'use strict';
  // An ISO 8601 instant with a zone: 2026-12-10T00:00:00Z or 2026-12-10T00:00:00+01:00. Anything else is not an end.
  var INSTANT = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:\d{2})$/;

  function instant(v) {
    if (typeof v !== 'string' || !INSTANT.test(v)) return NaN;
    return Date.parse(v);
  }

  // The first item that is live now, or null.
  function live() {
    var block = document.getElementById('announcements');
    if (!block) return null;
    var data;
    try { data = JSON.parse(block.textContent); } catch (e) { return null; }
    var items = data && data.items;
    if (!Array.isArray(items)) return null;
    for (var i = 0; i < items.length; i++) {
      var it = items[i];
      if (!it || typeof it.text !== 'string' || !it.text || typeof it.href !== 'string' || !it.href) continue;
      var ends = instant(it.end);
      if (!(ends > 0) || Date.now() >= ends) continue;   // no valid end, or ended: never shown
      if (it.start !== undefined) {
        var starts = instant(it.start);
        if (!(starts > 0) || Date.now() < starts) continue;
      }
      return it;
    }
    return null;
  }

  function add() {
    if (document.getElementById('launchSash')) return;
    var item = live();
    if (!item) return;
    var wrap = document.createElement('div');
    wrap.id = 'launchSash';
    wrap.className = 'launch-sash';
    var a = document.createElement('a');
    a.href = item.href;
    a.className = 'launch-sash-link';
    a.textContent = item.text;
    wrap.appendChild(a);
    // Between the hero and the scores ticker; the ticker hides itself when there is no live data, so fall back to the filter bar.
    var before = document.getElementById('scoreTicker') || document.querySelector('.filter-bar');
    if (before && before.parentNode) before.parentNode.insertBefore(wrap, before);
    else document.body.insertBefore(wrap, document.body.firstChild);
  }
  if (document.body) add(); else document.addEventListener('DOMContentLoaded', add);
})();
