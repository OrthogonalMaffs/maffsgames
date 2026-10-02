/* MaffsGames — Parent Guides: the one shared script for the whole /parents/ section.
 *
 * WHY THIS IS A FILE AND NOT AN INLINE COPY
 * -----------------------------------------
 * The Aa (dyslexia-friendly) toggle is currently an inline script copied into each of the
 * 90-odd game pages. docs/audit-parent-guides.md's closing note is explicit that the parents
 * section "should load one shared script, not add another copy", so this is it: 21 pages,
 * one implementation.
 *
 * It reuses the EXISTING localStorage key `mfg_accessible` rather than adding a new one.
 * privacy/index.html states that local storage is used for exactly two purposes
 * (accessibility and leaderboard initials); a second accessibility key would make that
 * sentence stale. The trade-off, recorded in the audit, is that on a shared family device a
 * child's setting also applies to the parent and vice versa.
 *
 * The font itself is self-hosted and declared once in schools/assets/opendyslexic.css,
 * which every page in this section links.
 *
 * THE GCSE TIER BADGE IS ALSO HERE, AND ONLY HERE
 * -----------------------------------------------
 * Four GCSE guides teach content the DfE subject content marks bold -- assessed on the
 * Higher tier only (data/dfe-gcse-parts.json). A parent of a Foundation-tier child
 * cannot tell that from the maths, so each of the four carries
 *     <p class="tier-badge" data-tier-badge="<slug>"></p>
 * directly under its title, and its card on the hub carries the same element. This
 * script writes the wording into both. The wording and the table below are the whole
 * component: no page writes its own variant, so a guide and its card cannot drift.
 *
 * TIERS is strict JSON between the two markers. scripts/verify-parent-guides.py reads
 * it back and checks that every DfE part listed is bold in the data file, that a
 * "higher" guide's statements are bold in every part, and that each section named for
 * a partly-Higher guide has a "Higher" marker in that guide's body (and that no marker
 * names a section not listed here). Change the table, and that script says whether the
 * pages still agree with it.
 */
(function () {
  'use strict';

  var TIERS = /* TIERS-JSON-BEGIN */{
    "circle-theorems":        {"kind": "higher",  "dfe": ["G10.1"]},
    "graphs-transformations": {"kind": "higher",  "dfe": ["A13.1"]},
    "indices-surds":          {"kind": "partial", "dfe": ["N7.2", "N8.2", "N8.4"],
                               "sections": ["fractional indices", "surds"]},
    "statistics-data":        {"kind": "partial", "dfe": ["S3.1", "S4.2", "S4.4"],
                               "sections": ["histograms", "cumulative frequency", "box plots",
                                            "the interquartile range"]}
  }/* TIERS-JSON-END */;

  function listOf(items) {
    return items.length < 2 ? items.join('')
      : items.slice(0, -1).join(', ') + ' and ' + items[items.length - 1];
  }

  function tierText(slug) {
    var t = TIERS[slug];
    if (!t) return null;
    if (t.kind === 'higher') {
      return 'Higher tier only. Foundation-tier students are not examined on this topic.';
    }
    return 'Includes Higher tier content: ' + listOf(t.sections) + '.';
  }

  function renderTierBadges() {
    var els = document.querySelectorAll('[data-tier-badge]');
    for (var i = 0; i < els.length; i++) {
      var words = tierText(els[i].getAttribute('data-tier-badge'));
      if (words) {
        els[i].textContent = words;
      } else {
        /* An unknown slug renders nothing rather than a guess. warn, not error:
           console.error is a tier-1 failure, and this is a content slip, not a crash. */
        console.warn('tier badge: no TIERS entry for', els[i].getAttribute('data-tier-badge'));
      }
    }
  }

  var KEY = 'mfg_accessible';

  function readStored() {
    try {
      return localStorage.getItem(KEY) === 'true';
    } catch (e) {
      return false;
    }
  }

  function writeStored(on) {
    try {
      localStorage.setItem(KEY, String(on));
    } catch (e) {
      /* private mode, blocked site data: the toggle still works for this page view */
    }
  }

  function init() {
    renderTierBadges();

    var btn = document.getElementById('a11yBtn');
    if (btn) {
      var apply = function (on) {
        document.body.classList.toggle('accessible', on);
        btn.classList.toggle('active', on);
        btn.setAttribute('aria-pressed', String(on));
      };
      apply(readStored());
      btn.addEventListener('click', function () {
        var on = !document.body.classList.contains('accessible');
        writeStored(on);
        apply(on);
      });
    }

    /* Hub page FAQ. Keyboard-operable, unlike the MathsWins original's onclick div. */
    var qs = document.querySelectorAll('.faq-q');
    for (var i = 0; i < qs.length; i++) {
      (function (q) {
        var toggle = function () {
          var item = q.parentElement;
          var open = item.classList.toggle('open');
          q.setAttribute('aria-expanded', String(open));
        };
        q.setAttribute('role', 'button');
        q.setAttribute('tabindex', '0');
        q.setAttribute('aria-expanded', 'false');
        q.addEventListener('click', toggle);
        q.addEventListener('keydown', function (e) {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            toggle();
          }
        });
      })(qs[i]);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
