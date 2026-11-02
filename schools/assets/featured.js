/* MaffsFeatured: the pinned, featured card (launch contract SIX-PS-LAUNCH, Jon, 27 Oct 2026).
 *
 * One component, driven by data. A page puts an empty <div data-featured="<page>"> where the cards go, with a plain link
 * inside it as the no-script fallback, and loads this file and featured.css. The items are schools/assets/featured-items.json;
 * an item is drawn on every page named in its "pages". A second featured item is a new entry in that file, not new markup.
 *
 *   { id, pages: ["essentials"], flag, title, lede, facts: [..], href, cta }
 *
 * The text is set with textContent, so a title with an apostrophe or an ampersand is safe. If the file cannot be read the
 * fallback link stays. Nothing is stored and nothing is sent.
 */
(function () {
  'use strict';
  var URL_ITEMS = '/schools/assets/featured-items.json';

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    return e;
  }

  function card(item) {
    var a = el('a', 'featured-card');
    a.href = item.href;
    a.setAttribute('data-mfg-item', item.id);
    a.appendChild(el('span', 'featured-flag', item.flag));
    a.appendChild(el('span', 'featured-title', item.title));
    a.appendChild(el('span', 'featured-lede', item.lede));
    if (item.facts && item.facts.length) {
      var ul = el('span', 'featured-facts');
      item.facts.forEach(function (f) { ul.appendChild(el('span', 'featured-fact', f)); });
      a.appendChild(ul);
    }
    a.appendChild(el('span', 'featured-cta', item.cta + ' \u2192'));
    return a;
  }

  function draw(host, items) {
    var mine = items.filter(function (it) { return it.pages && it.pages.indexOf(host.getAttribute('data-featured')) >= 0; });
    if (!mine.length) return;
    host.textContent = '';
    mine.forEach(function (it) { host.appendChild(card(it)); });
    host.classList.add('featured-on');
  }

  function run() {
    var hosts = [].slice.call(document.querySelectorAll('[data-featured]'));
    if (!hosts.length || !window.fetch) return;
    fetch(URL_ITEMS).then(function (r) { return r.ok ? r.json() : null; }).then(function (d) {
      if (d && d.items) hosts.forEach(function (h) { draw(h, d.items); });
    }).catch(function () { /* the fallback link stays */ });
  }

  window.MaffsFeatured = { draw: draw, card: card };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();
