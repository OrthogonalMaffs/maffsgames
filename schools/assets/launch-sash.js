/* The "100 games" sash (launch contract SIX-PS-LAUNCH, Jon, 27 Oct 2026). Homepage only, for two weeks.
 *
 * A figure on a page is a claim, and a claim with a date in it goes stale: this one carries its own end date and removes itself
 * from that day, whatever anyone remembers to do (the same rule as the answer counts). scripts/check-launch-sash.py fails if this
 * file ships without END, or if any page but the homepage loads it.
 *
 * A thin gold announcement strip across the full width, in the page's flow between the hero and the scores ticker (it replaced the
 * diagonal corner ribbon on 29 Oct 2026, which covered the hero's Leaderboards link). Static: no animation.
 * No analytics labels (data-mfg-*): a time-limited element must not be one the portal's click test counts, or that test fails the day it ends.
 * It is an ordinary link: keyboard focus, a visible focus ring, text contrast above 4.5:1.
 */
(function () {
  'use strict';
  var END = '2026-11-10T00:00:00Z';   // hidden from this instant on
  var HREF = '/the-6-ps/';
  var TEXT = '100 games \u00b7 Meet The 6 P\u2019s \u2192';

  var ends = Date.parse(END);
  if (!(ends > 0) || Date.now() >= ends) return;
  if (document.getElementById('launchSash')) return;

  function add() {
    if (document.getElementById('launchSash')) return;
    var wrap = document.createElement('div');
    wrap.id = 'launchSash';
    wrap.className = 'launch-sash';
    var a = document.createElement('a');
    a.href = HREF;
    a.className = 'launch-sash-link';
    a.textContent = TEXT;
    wrap.appendChild(a);
    // Between the hero and the scores ticker; the ticker hides itself when there is no live data, so fall back to the filter bar.
    var before = document.getElementById('scoreTicker') || document.querySelector('.filter-bar');
    if (before && before.parentNode) before.parentNode.insertBefore(wrap, before);
    else document.body.insertBefore(wrap, document.body.firstChild);
  }
  if (document.body) add(); else document.addEventListener('DOMContentLoaded', add);
})();
