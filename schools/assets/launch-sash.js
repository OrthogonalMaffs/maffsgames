/* The "100 games" sash (launch contract SIX-PS-LAUNCH, Jon, 27 Oct 2026). Homepage only, for two weeks.
 *
 * A figure on a page is a claim, and a claim with a date in it goes stale: this one carries its own end date and removes itself
 * from that day, whatever anyone remembers to do (the same rule as the answer counts). scripts/check-launch-sash.py fails if this
 * file ships without END, or if any page but the homepage loads it.
 *
 * Wide screens: a diagonal corner sash. Phones: a slim strip across the top (a corner sash would cover the header).
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
    wrap.setAttribute('data-mfg-section', 'launch-sash');
    var a = document.createElement('a');
    a.href = HREF;
    a.className = 'launch-sash-link';
    a.setAttribute('data-mfg-item', 'meet-the-6-ps');
    a.textContent = TEXT;
    wrap.appendChild(a);
    document.body.insertBefore(wrap, document.body.firstChild);
  }
  if (document.body) add(); else document.addEventListener('DOMContentLoaded', add);
})();
