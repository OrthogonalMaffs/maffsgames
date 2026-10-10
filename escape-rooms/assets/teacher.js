/* ============================================================
   MaffsGames escape rooms — teacher page renderer
   ------------------------------------------------------------
   Reads the same room.js the game reads, so the answers and the
   hint ladder here can never drift from the ones on screen.

   Each lock draws one set of numbers per play, so this page has
   to show the set actually in play — not a fixed example. The
   game mirrors its draw into localStorage under
   mfg_escape_vars_<slug>; this page reads that, and listens for
   the storage event so that when the class hits "play again" in
   the other tab, these answers change with them.

   The page adds what the game has no use for: topic labels,
   per-lock timings, curriculum lines, which clue feeds which
   lock, and the whole library so a teacher can see the range.
   ============================================================ */
(function () {
  'use strict';
  var R = window.ROOM, T = window.TEACH || {};
  var meta = T.lockMeta || [];
  var VARS_KEY = 'mfg_escape_vars_' + R.slug;
  var live = null;      // {vars, at, done} from the game tab, or null

  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

  function readLive() {
    try {
      var raw = localStorage.getItem(VARS_KEY);
      live = raw ? JSON.parse(raw) : null;
    } catch (e) { live = null; }
  }

  function indexOf(l) {
    if (live && live.vars && live.vars[l.id] !== undefined) return live.vars[l.id];
    return 0;
  }
  function variantOf(l) { return (l.variants || [{}])[indexOf(l)] || {}; }

  function tokens() {
    var t = {};
    R.locks.forEach(function (l) {
      var v = variantOf(l);
      for (var k in v) t[(l.key || l.id) + '.' + k] = v[k];
    });
    return t;
  }
  function fill(s) {
    if (s === null || s === undefined) return s;
    var t = tokens();
    return String(s).replace(/\{\{([\w.-]+)\}\}/g, function (m, key) {
      return t[key] !== undefined ? t[key] : m;
    });
  }

  function ansOf(l, v) {
    v = v || variantOf(l);
    var a = v.answer !== undefined ? v.answer : l.answer;
    if (Array.isArray(a)) return a.join(' and ');
    return a + (l.instrument.unit ? ' ' + l.instrument.unit : '');
  }
  function missOf(l, v) {
    v = v || variantOf(l);
    var m = v.miss !== undefined ? v.miss : l.miss;
    if (m === undefined || m === null) return '&mdash;';
    return Array.isArray(m) ? m.join(' and ') : String(m);
  }

  function whenText() {
    if (!live) return null;
    var mins = Math.round((Date.now() - live.at) / 60000);
    if (live.done) return 'that game has finished';
    if (mins < 1) return 'started just now';
    return 'started ' + mins + ' minute' + (mins === 1 ? '' : 's') + ' ago';
  }

  function render() {
    var totalTime = meta.reduce(function (a, m) { return a + (m.minutes || 0); }, 0);
    var when = whenText();
    // The engine shows the failure picture beside a misconception only for a
    // lock that sets missArt, so the page only says so when one does.
    // A room with no `art` yet shows no failure picture at all (engine.js, HAS_ART).
    var midGameArt = !!R.art && R.locks.some(function (l) { return l.missArt; });

    var banner = live
      ? '<div class="unlisted" id="liveBox"><b>These are the numbers in play right now</b> &mdash; ' + when +
        ' on this device. Every answer, hint and worked solution below is the set the students are looking at. ' +
        'If they start again, this page updates itself.</div>'
      : '<div class="unlisted" id="liveBox"><b>No game running on this device.</b> Each lock draws its numbers ' +
        'fresh when a room is started, so the figures below are the <i>first</i> set in each library, shown as an ' +
        'example. Open the room in another tab and this page will switch to the numbers the students actually get.</div>';

    var html = '' +
      '<div class="card">' +
        '<h1><span class="sub">Teacher page &middot; ' + esc(R.levelLabel) + '</span>' + esc(R.title) + '</h1>' +
        '<p class="lede">' + fill(R.brief) + '</p>' +
        banner +
        '<div class="unlisted"><b>At a glance.</b> ' + R.locks.length + ' locks, ' +
          (totalTime ? totalTime + ' minutes of puzzle for a group of three or four, ' : '') +
          'on a ' + R.minutes + '-minute clock. A wrong setting costs ' + (R.penalty || 45) + ' seconds. ' +
          'Hints are free and unlimited, three levels per lock, and every one taken is counted on the results ' +
          'screen. Each lock has a library of ' +
          R.locks.map(function (l) { return (l.variants || []).length; }).join('/') +
          ' number sets, so the room can be replayed without repeating itself.</div>' +

        '<h2>The locks</h2>' +
        '<table class="tt"><thead><tr><th>Lock</th><th>Topic</th><th>Instrument</th><th>Answer</th>' +
        '<th>Wrong answer to expect</th><th>Time</th></tr></thead><tbody>' +
        R.locks.map(function (l, i) {
          var m = meta[i] || {}, ins = l.instrument;
          var insDesc = ins.kind === 'keypad' ? ins.digits + '-digit keypad'
            : ins.kind === 'pair' ? 'two dials'
            : ins.kind + ', ' + ins.min + '&ndash;' + ins.max + (ins.step !== 1 ? ' in ' + ins.step + 's' : '');
          return '<tr><td><b>' + esc(l.name) + '</b><br><code>' + esc(l.id) + '</code></td>' +
            '<td>' + esc(m.topic || '') + '</td>' +
            '<td>' + insDesc + '</td>' +
            '<td class="ans">' + ansOf(l) + '</td>' +
            '<td class="wrongans">' + missOf(l) + '</td>' +
            '<td>' + (m.minutes ? m.minutes + ' min' : '&mdash;') + '</td></tr>';
        }).join('') +
        '</tbody></table>' +

        '<h2>Where the clues are, and what they say this time</h2>' +
        '<p class="lede">The room deliberately does not tell students which note belongs to which lock &mdash; that ' +
          'is the first real piece of thinking, and it is where the difficulty lives. This table is for you.</p>' +
        '<table class="tt"><thead><tr><th>Object</th><th>Where</th><th>Feeds</th><th>What it says</th></tr></thead><tbody>' +
        R.objects.map(function (o) {
          var feeds = (T.clueMap && T.clueMap[o.id]) || (o.clue ? '' : 'nothing &mdash; a blank');
          return '<tr><td><b>' + esc(o.name) + '</b></td><td>' + esc(o.where) + '</td><td>' + feeds + '</td>' +
                 '<td>' + (o.clue ? fill(o.clue) : '<i>' + fill(o.flavour || '') + '</i>') + '</td></tr>';
        }).join('') +
        '</tbody></table>' +

        '<h2>Answers, method and the hint ladder</h2>' +
        R.locks.map(function (l, i) {
          var m = meta[i] || {};
          return '<div class="panel" style="margin-bottom:14px">' +
            '<h3>' + esc(l.name) + ' &mdash; answer <span class="ans">' + ansOf(l) + '</span></h3>' +
            '<p style="margin-bottom:8px">' + fill(l.solve) + '</p>' +
            (m.curriculum ? '<p class="print-note">Curriculum: ' + m.curriculum + '</p>' : '') +
            '<p style="margin-top:10px"><b>The misconception it is built around</b> &mdash; ' +
              '<span class="wrongans">' + missOf(l) + '</span>. ' + fill(l.missSays || '') + '</p>' +
            '<p style="margin-top:10px"><b>Hint ladder</b> (students see these one at a time):</p>' +
            '<ol class="ladder">' + l.hints.map(function (h, k) {
              return '<li><b>' + ['Nudge', 'Method', 'Answer'][k] + ':</b> ' + fill(h) + '</li>';
            }).join('') + '</ol>' +
            (l.variants && l.variants.length > 1 ? libraryTable(l) : '') +
          '</div>';
        }).join('') +

        '<h2>If they run out of time</h2>' +
        '<div class="stakes">' + fill(R.stakes) + '</div>' +
        (midGameArt ? '<p class="lede">The failure picture is also shown mid-game, but only when a group enters the one specific ' +
          'wrong answer the room is built around. It is meant to be the funniest thing in the room, not a ' +
          'telling-off.</p>' : '') +

        (T.notes ? '<h2>Running it</h2>' + T.notes : '') +

        '<div class="btn-row">' +
          '<a class="btn" href="./">Play the room</a>' +
          '<a class="btn ghost" href="../">All escape rooms</a>' +
          '<button class="btn ghost" onclick="window.print()">Print</button>' +
        '</div>' +
      '</div>';

    document.getElementById('app').innerHTML = html;
  }

  // The whole library for one lock, with the set in play marked.
  function libraryTable(l) {
    var here = indexOf(l);
    return '<p style="margin-top:12px"><b>The rest of this lock’s library</b> — what else can come up:</p>' +
      '<table class="tt"><thead><tr><th>Set</th><th>Answer</th><th>Wrong answer</th></tr></thead><tbody>' +
      l.variants.map(function (v, i) {
        return '<tr' + (i === here ? ' style="outline:2px solid var(--accent)"' : '') + '>' +
          '<td>' + (i + 1) + (i === here ? ' <b>&larr; in play</b>' : '') + '</td>' +
          '<td class="ans">' + ansOf(l, v) + '</td>' +
          '<td class="wrongans">' + missOf(l, v) + '</td></tr>';
      }).join('') +
      '</tbody></table>';
  }

  // ---- go, and keep up with the other tab ----
  readLive();
  render();
  document.title = R.title + ' — teacher page — MaffsGames';

  window.addEventListener('storage', function (e) {
    if (e.key === VARS_KEY) { readLive(); render(); }
  });

  window.toggleAa = function () {
    document.body.classList.toggle('accessible');
    document.querySelector('.a11y-toggle').classList.toggle('active');
  };
})();
