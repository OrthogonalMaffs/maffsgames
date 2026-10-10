/* ============================================================
   MaffsGames escape-room engine
   ------------------------------------------------------------
   One engine, many rooms. A room page defines window.ROOM and
   includes this file; everything below builds the whole game.

   The design rules this implements (docs/escape-rooms-concept.md):
     §3  the maths is the action — every lock is an instrument you
         set, never a question box
     §5c the cost of failing lives in the fiction, and the named
         misconception gets its own response
     §6  progress survives a refresh, hints are a three-step ladder
         and free, and every instrument has a typed fallback
   ============================================================ */
(function () {
  'use strict';

  var R = window.ROOM;
  var SAVE_KEY = 'mfg_escape_' + R.slug;
  var SAVE_V = 1;
  var ART = '../../docs/art/';

  // A room can be built, or win art added, before the picture exists. An image
  // that 404s either falls back to the one named in data-fallback or takes its
  // frame with it — never a broken-image box in the middle of a room.
  window.mfgArtFallback = function (img) {
    var next = img.getAttribute('data-fallback');
    if (next) { img.removeAttribute('data-fallback'); img.src = next; }
    else if (img.parentNode) { img.parentNode.remove(); }
  };

  // A room with no `art` field has no pictures yet (art comes after the room is
  // settled), so it requests none: no scene, fail or win frame, exactly as a lock
  // with no `art` has no instrument picture (canon §11.3). The 404 fallback above
  // is only for a room that names its art but is missing a file.
  var HAS_ART = !!R.art;

  var TOTAL = (R.minutes || 15) * 60;
  var PENALTY = R.penalty || 45;

  var st = null;      // game state, see freshState()
  var activeLock = null;
  var timerId = null;
  var pending = {};   // lockId -> current instrument value(s), not saved

  function freshState() {
    return { v: SAVE_V, found: {}, open: {}, hints: {}, wrongs: 0, left: TOTAL, done: null, vars: pickVariants() };
  }

  // ---------- variants ----------
  // Every lock carries a library of number sets. One is drawn per play, so the
  // scenario, the maths and the misconception stay put while the figures
  // change — a room can be replayed without being the same room.
  // The choice is saved, so a refresh mid-game does not reshuffle it, and it
  // is mirrored to VARS_KEY so the teacher page (a separate tab, same origin)
  // can show the numbers actually in play.
  var VARS_KEY = 'mfg_escape_vars_' + R.slug;

  // Drawing at random on its own lets a lock hand back the numbers it gave
  // last time, which is the one repeat a student actually notices. So every
  // lock draws from its library *minus* the set it just used: play again and
  // every figure in the room is one you have not just worked out. Only a
  // one-set lock can repeat, and then there is nothing else to give.
  //
  // The room is drawn as a whole, not lock by lock, because independent draws
  // collide: a figure printed in two locks' clues, one lock's answer printed in
  // another's clue, or one lock's misconception equal to another's answer. A
  // draw is VALID when, across its locks:
  //   a. no clue figure is printed in the clues of more than one lock
  //   b. no lock's answer is printed in another lock's clues
  //   c. no lock's answer equals another lock's misconception
  //   d. no two locks share an answer
  // A clue figure is any number the student reads in a clue, token or numeral,
  // and a clue belongs to the lock whose tokens it uses. Rules (a) and (b)
  // ignore figures of 2 or less; (c) and (d) apply at every size.
  // scripts/check-escape-rooms.py applies the same rules and fails a room with
  // fewer than 20 VALID draws — change the two together.
  //
  // Every VALID draw that repeats no lock's last set is equally likely. If none
  // exists, the no-repeat rule is relaxed for the fewest locks that allows one.
  // An invalid draw is never served.
  var CLUE_EXEMPT = 2;

  function numbersIn(x) {
    if (x === null || x === undefined) return [];
    if (Array.isArray(x)) return x.reduce(function (a, v) { return a.concat(numbersIn(v)); }, []);
    return (String(x).match(/\d+(?:\.\d+)?/g) || []).map(Number);
  }
  function shares(a, b) {
    for (var i = 0; i < a.length; i++) if (b.indexOf(a[i]) >= 0) return true;
    return false;
  }

  function pickVariants() {
    var prev = {};
    try {
      var saved = JSON.parse(localStorage.getItem(VARS_KEY) || 'null');
      if (saved && saved.vars) prev = saved.vars;
    } catch (e) { /* private mode, or nothing stored yet */ }

    // Per lock, per variant: the clue figures, the answer and the misconception.
    var locks = R.locks.map(function (l) {
      var key = l.key || l.id;
      var lib = l.variants && l.variants.length ? l.variants : [{}];
      var clues = R.objects.filter(function (o) {
        if (!o.clue) return false;
        var owners = {};
        String(o.clue).replace(/\{\{([\w-]+)\./g, function (m, k) { owners[k] = 1; return m; });
        var ks = Object.keys(owners);
        return ks.length === 1 && ks[0] === key;
      }).map(function (o) { return String(o.clue); });
      var last = prev[l.id];
      return {
        id: l.id,
        n: lib.length,
        last: (typeof last === 'number' && last >= 0 && last < lib.length) ? last : -1,
        figs: lib.map(function (v) {
          var out = [];
          clues.forEach(function (c) {
            var seen = c.replace(/\{\{([\w-]+)\.([\w-]+)\}\}/g, function (m, k, t) {
                         return k === key && v[t] !== undefined ? String(v[t]) : m;
                       })
                        .replace(/<[^>]*>|&[#\w]+;/g, ' ');
            numbersIn(seen).forEach(function (f) { if (f > CLUE_EXEMPT) out.push(f); });
          });
          return out;
        }),
        ans: lib.map(function (v) { return numbersIn(v.answer !== undefined ? v.answer : l.answer); }),
        miss: lib.map(function (v) { return numbersIn(v.miss !== undefined ? v.miss : l.miss); })
      };
    });

    function valid(pick) {
      for (var i = 0; i < locks.length; i++) {
        for (var j = 0; j < locks.length; j++) {
          if (i === j) continue;
          var a = locks[i], b = locks[j], p = pick[i], q = pick[j];
          if (i < j && (shares(a.figs[p], b.figs[q]) || shares(a.ans[p], b.ans[q]))) return false;
          if (shares(a.ans[p], b.figs[q]) || shares(a.ans[p], b.miss[q])) return false;
        }
      }
      return true;
    }

    // Walk every combination, keeping the VALID ones that repeat the fewest locks.
    var best = null, fewest = Infinity, pick = [];
    (function walk(i, repeats) {
      if (repeats > fewest) return;
      if (i === locks.length) {
        if (!valid(pick)) return;
        if (repeats < fewest) { fewest = repeats; best = []; }
        best.push(pick.slice());
        return;
      }
      for (var k = 0; k < locks[i].n; k++) {
        pick[i] = k;
        walk(i + 1, repeats + (locks[i].n > 1 && k === locks[i].last ? 1 : 0));
      }
    })(0, 0);

    var chosen = best ? best[Math.floor(Math.random() * best.length)] : null;
    if (!chosen) {
      // Unreachable while check-escape-rooms.py passes: it fails any room with
      // fewer than 20 VALID draws.
      if (window.console) console.error('[escape] no VALID variant draw for ' + R.slug);
      chosen = locks.map(function () { return 0; });
    }
    var v = {};
    locks.forEach(function (l, i) { v[l.id] = chosen[i]; });
    return v;
  }
  function variantOf(l) {
    if (!l.variants) return {};
    var i = (st && st.vars && st.vars[l.id]) || 0;
    return l.variants[i] || l.variants[0];
  }
  function answerOf(l) { var v = variantOf(l); return v.answer !== undefined ? v.answer : l.answer; }
  function missOf(l) { var v = variantOf(l); return v.miss !== undefined ? v.miss : l.miss; }

  // {{lock.key}} in any authored string is replaced by that lock's drawn value.
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
  function publishVars() {
    try {
      localStorage.setItem(VARS_KEY, JSON.stringify({ vars: st.vars, at: Date.now(), done: st.done }));
    } catch (e) {}
  }

  // ---------- helpers ----------
  function el(id) { return document.getElementById(id); }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function mmss(s) {
    if (s < 0) s = 0;
    var m = Math.floor(s / 60), r = s % 60;
    return m + ':' + (r < 10 ? '0' : '') + r;
  }
  function dp(v, d) { return d ? Number(v).toFixed(d) : String(Math.round(v)); }
  function track(name, extra) {
    var p = { game_slug: R.slug, level: R.level };
    for (var k in extra) p[k] = extra[k];
    if (window.mfg) window.mfg(name, p);
  }

  // A lock's answer is one number, or a pair. Compare at the
  // instrument's own precision so 3.0 and 3 are the same setting.
  function sameValue(a, b, d) {
    if (a === null || a === undefined || a === '') return false;
    return Math.abs(Number(a) - Number(b)) < (d ? 0.5 / Math.pow(10, d) : 0.5) * 0.999;
  }
  function lockById(id) {
    for (var i = 0; i < R.locks.length; i++) if (R.locks[i].id === id) return R.locks[i];
    return null;
  }

  // ---------- page shell ----------
  function build() {
    el('app').innerHTML =
      screenBrief() + screenPlay() + screenEnd() +
      '<div class="penalty-flash" id="penaltyFlash" role="status"></div>';
    bindStatic();
  }

  function screenBrief() {
    return '' +
      '<section class="screen active" id="scrBrief">' +
        '<div class="card">' +
          '<h1><span class="sub">' + esc(R.levelLabel) + ' &middot; escape room &middot; ' + R.minutes + ' minutes</span>' + esc(R.title) + '</h1>' +
          (HAS_ART ? '<div class="artframe"><img onerror="mfgArtFallback(this)" src="' + ART + R.art + '-scene.webp" alt="' + esc(R.sceneAlt) + '" loading="eager"></div>' : '') +
          '<div class="story">' + R.hook + '</div>' +
          '<p class="lede">' + R.brief + '</p>' +
          '<div class="stakes"><b>If you get it wrong.</b> ' + R.stakes + '</div>' +
          '<h2>How it works</h2>' +
          '<p class="lede">Search the room first. The notes you find do not say which lock they belong to &mdash; ' +
            'working that out is most of the puzzle. Then set each instrument to the value the room tells you. ' +
            'A wrong setting costs you <b>' + PENALTY + ' seconds</b>, so be sure before you commit. ' +
            'Hints are free and there are three levels of them.</p>' +
          '<div class="btn-row">' +
            '<button class="btn" id="startBtn">Start &mdash; ' + R.minutes + ':00 on the clock</button>' +
            '<button class="btn ghost" id="resumeBtn" style="display:none">Resume</button>' +
            '<a class="btn ghost" href="teacher.html" target="_blank" rel="noopener">Teacher page</a>' +
          '</div>' +
        '</div>' +
      '</section>';
  }

  function screenPlay() {
    return '' +
      '<section class="screen" id="scrPlay">' +
        '<div class="hud">' +
          '<div class="clock-box" id="clock" role="timer" aria-live="off">' + R.minutes + ':00</div>' +
          '<div class="hud-meta" id="hudTitle">' + esc(R.title) + '</div>' +
          '<div class="pips" id="pips"></div>' +
        '</div>' +
        '<div class="cols">' +
          '<div class="panel">' +
            '<div class="panel-head"><h2>The room</h2><span class="count" id="searchCount"></span></div>' +
            '<div class="objects" id="objects"></div>' +
            '<div class="search-out" id="searchOut" role="status"></div>' +
            '<div class="panel-head" style="margin-top:18px"><h2>What you have found</h2></div>' +
            '<div class="notebook" id="notebook"></div>' +
          '</div>' +
          '<div class="panel">' +
            '<div class="panel-head"><h2>The locks</h2><span class="count" id="lockCount"></span></div>' +
            '<div class="locks" id="lockBtns"></div>' +
            '<div id="lockPanel"></div>' +
          '</div>' +
        '</div>' +
      '</section>';
  }

  function screenEnd() {
    return '' +
      '<section class="screen" id="scrEnd">' +
        '<div class="card" id="endCard"></div>' +
      '</section>';
  }

  function bindStatic() {
    el('startBtn').onclick = function () { begin(freshState()); };
    el('resumeBtn').onclick = function () {
      var s = load();
      if (s) begin(s, true); else begin(freshState());
    };
  }

  function show(id) {
    ['scrBrief', 'scrPlay', 'scrEnd'].forEach(function (s) {
      el(s).classList.toggle('active', s === id);
    });
  }

  // ---------- save / load ----------
  function save() {
    if (st && !st.done) {
      try { localStorage.setItem(SAVE_KEY, JSON.stringify(st)); } catch (e) {}
    }
  }
  function load() {
    try {
      var raw = localStorage.getItem(SAVE_KEY);
      if (!raw) return null;
      var s = JSON.parse(raw);
      if (!s || s.v !== SAVE_V || s.done) return null;
      return s;
    } catch (e) { return null; }
  }
  function clearSave() { try { localStorage.removeItem(SAVE_KEY); } catch (e) {} }

  // ---------- the room ----------
  function renderRoom() {
    var searched = R.objects.filter(function (o) { return st.found[o.id]; }).length;
    el('searchCount').textContent = searched + ' of ' + R.objects.length + ' searched';
    el('objects').innerHTML = R.objects.map(function (o) {
      var done = st.found[o.id];
      var cls = 'obj' + (done ? ' done' : '') + (done && !o.clue ? ' empty' : '');
      return '<button class="' + cls + '" data-obj="' + o.id + '">' +
        '<span class="obj-n">' + esc(o.name) + '</span>' +
        '<span class="obj-w">' + esc(done ? (o.clue ? 'found something' : 'nothing here') : o.where) + '</span>' +
        '</button>';
    }).join('');
    Array.prototype.forEach.call(el('objects').querySelectorAll('[data-obj]'), function (b) {
      b.onclick = function () { searchObj(b.getAttribute('data-obj')); };
    });
    renderNotebook();
  }

  function searchObj(id) {
    var o = R.objects.filter(function (x) { return x.id === id; })[0];
    if (!o) return;
    var first = !st.found[o.id];
    st.found[o.id] = true;
    var out = el('searchOut');
    if (o.clue) {
      out.className = 'search-out show got';
      out.innerHTML = '<b>' + esc(o.name) + '</b>' + fill(o.clue);
    } else {
      out.className = 'search-out show nowt';
      out.innerHTML = '<b>' + esc(o.name) + '</b>' + fill(o.flavour || 'Nothing useful here.');
    }
    if (first) track('question_answered', { correct: true, question_index: 0, detail: 'searched:' + o.id });
    renderRoom();
    save();
  }

  function renderNotebook() {
    var clues = R.objects.filter(function (o) { return st.found[o.id] && o.clue; });
    el('notebook').innerHTML = clues.length
      ? clues.map(function (o) {
          return '<div class="clue"><span class="clue-src">' + esc(o.name) + '</span>' + fill(o.clue) + '</div>';
        }).join('')
      : '<p class="empty-note">Nothing yet. Search the room &mdash; the notes do not say which lock they are for.</p>';
  }

  // ---------- locks ----------
  function renderLockBtns() {
    var opened = R.locks.filter(function (l) { return st.open[l.id]; }).length;
    el('lockCount').textContent = opened + ' of ' + R.locks.length + ' open';
    el('lockBtns').innerHTML = R.locks.map(function (l, i) {
      var cls = 'lockbtn' + (st.open[l.id] ? ' open' : '') + (activeLock === i ? ' sel' : '');
      return '<button class="' + cls + '" data-lock="' + i + '">' + (st.open[l.id] ? '&#10003; ' : '') + esc(l.name) + '</button>';
    }).join('');
    Array.prototype.forEach.call(el('lockBtns').querySelectorAll('[data-lock]'), function (b) {
      b.onclick = function () { pickLock(Number(b.getAttribute('data-lock'))); };
    });
    el('pips').innerHTML = R.locks.map(function (l) {
      return '<div class="pip' + (st.open[l.id] ? ' done' : '') + '">' + (st.open[l.id] ? '&#10003;' : '&#183;') + '</div>';
    }).join('');
  }

  function pickLock(i) {
    activeLock = i;
    renderLockBtns();
    renderLockPanel();
  }

  function renderLockPanel() {
    var host = el('lockPanel');
    if (activeLock === null) {
      host.innerHTML = '<p class="pick-prompt">Pick a lock to look at it.</p>';
      return;
    }
    var l = R.locks[activeLock];
    var open = !!st.open[l.id];
    host.innerHTML =
      (l.art ? '<div class="artframe"><img onerror="mfgArtFallback(this)" src="' + ART + l.art +
               '.webp" alt="' + esc(l.artAlt) + '" loading="lazy"></div>' : '') +
      '<div class="lock-brief">' + fill(l.brief) + '</div>' +
      '<div class="feedback" id="fb" role="status"></div>' +
      (open ? openedBody(l) : instrumentBody(l)) +
      (open ? '' : hintsBody(l));
    if (!open) wireInstrument(l);
  }

  function openedBody(l) {
    return '<div class="feedback good show"><b>Open.</b>' + fill(l.onOpen) + '</div>' +
      '<div class="lock-brief"><b>How it went:</b> ' + fill(l.solve) + '</div>';
  }

  // ---------- instruments ----------
  function instrumentBody(l) {
    var ins = l.instrument;
    var body;
    if (ins.kind === 'keypad') body = keypadHTML(l, ins);
    else if (ins.kind === 'pair') body = pairHTML(l, ins);
    else body = singleHTML(l, ins, '');
    return '<div class="instrument">' +
      '<div class="instrument-label">' + esc(ins.label) + '</div>' + body +
      '</div>' +
      '<div class="btn-row"><button class="btn" id="setBtn">' + esc(ins.verb || 'Set it') + '</button></div>';
  }

  function singleHTML(l, ins, suffix) {
    var id = 'ctl' + suffix;
    var start = ins.start !== undefined ? ins.start : ins.min;
    pending[l.id + suffix] = start;
    var dial = ins.kind === 'dial'
      ? '<div class="dial-wrap">' + dialSVG(id) + '</div><p class="dial-hint">Drag the needle, or use the slider &mdash; both set the same value.</p>'
      : '';
    return dial +
      '<div class="readout" id="ro' + suffix + '" aria-hidden="true">' + dp(start, ins.decimals) +
        (ins.unit ? '<span class="unit">' + esc(ins.unit) + '</span>' : '') + '</div>' +
      '<input type="range" id="' + id + '" min="' + ins.min + '" max="' + ins.max + '" step="' + ins.step +
        '" value="' + start + '" aria-label="' + esc(ins.label) + (ins.unit ? ' in ' + esc(ins.unit) : '') + '">' +
      '<div class="range-row"><span>' + dp(ins.min, ins.decimals) + '</span><span>' + dp(ins.max, ins.decimals) + '</span></div>' +
      '<div class="fallback">' +
        '<label for="num' + suffix + '">Or type the setting</label>' +
        '<div class="fallback-row">' +
          '<input class="numin" type="number" id="num' + suffix + '" min="' + ins.min + '" max="' + ins.max +
            '" step="' + ins.step + '" value="' + dp(start, ins.decimals) + '">' +
          '<span class="count">' + esc(ins.unit || '') + '</span>' +
        '</div>' +
      '</div>';
  }

  function pairHTML(l, ins) {
    return '<div class="pair-grid">' +
      '<div><div class="instrument-label">' + esc(ins.a.label) + '</div>' + singleHTML(l, ins.a, 'A') + '</div>' +
      '<div><div class="instrument-label">' + esc(ins.b.label) + '</div>' + singleHTML(l, ins.b, 'B') + '</div>' +
      '</div>';
  }

  // A keypad is fixed-length (`digits: N`: exactly N digits, empty slots shown, 060 for 60) or, with
  // `maxDigits: N` instead (contract KEYPAD-VARIABLE, 10 Oct 2026), "up to N digits, Set to submit": the
  // display shows only what has been typed, Set submits 1 to N digits (nothing typed does nothing), and a
  // leading zero is never kept. A keypad with `digits` behaves exactly as it did before maxDigits existed.
  function keyLen(ins) { return ins.maxDigits || ins.digits; }

  // The one rule the keys and the typed fallback share in maxDigits mode: digits only, no leading zero, at most N.
  function upTo(ins, c) {
    return c.replace(/[^0-9]/g, '').replace(/^0+(?=\d)/, '').slice(0, ins.maxDigits);
  }

  function keypadHTML(l, ins) {
    pending[l.id] = '';
    var keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'clr', '0', 'del'];
    return '<div class="code-display" id="codeDisp" aria-live="polite"></div>' +
      '<div class="keypad">' + keys.map(function (k) {
        if (k === 'clr') return '<button class="wide" data-key="clr" aria-label="Clear">CLR</button>';
        if (k === 'del') return '<button class="wide" data-key="del" aria-label="Delete last digit">DEL</button>';
        return '<button data-key="' + k + '">' + k + '</button>';
      }).join('') + '</div>' +
      '<div class="fallback">' +
        '<label for="numK">Or type the code</label>' +
        '<div class="fallback-row">' +
          '<input class="numin" type="text" inputmode="numeric" id="numK" maxlength="' + keyLen(ins) + '" value="">' +
          '<span class="count">' + (ins.maxDigits ? 'up to ' + ins.maxDigits : ins.digits) + ' digits</span>' +
        '</div>' +
      '</div>';
  }

  function dialSVG(id) {
    var ticks = '';
    for (var i = 0; i <= 36; i++) {
      var a = (i / 36) * 360 - 90;
      var rad = a * Math.PI / 180;
      var major = i % 3 === 0;
      var r1 = major ? 66 : 71, r2 = 78;
      ticks += '<line class="tick' + (major ? ' major' : '') + '" x1="' + (90 + r1 * Math.cos(rad)).toFixed(1) +
        '" y1="' + (90 + r1 * Math.sin(rad)).toFixed(1) + '" x2="' + (90 + r2 * Math.cos(rad)).toFixed(1) +
        '" y2="' + (90 + r2 * Math.sin(rad)).toFixed(1) + '"/>';
    }
    return '<svg class="dial" id="dial_' + id + '" viewBox="0 0 180 180" aria-hidden="true">' +
      '<circle class="face" cx="90" cy="90" r="84"/>' + ticks +
      '<path id="wedge_' + id + '" fill="rgba(245,165,36,0.18)" stroke="none"></path>' +
      '<line class="needle" id="needle_' + id + '" x1="90" y1="90" x2="90" y2="22"/>' +
      '<circle class="boss" cx="90" cy="90" r="7"/>' +
      '</svg>';
  }

  function wireInstrument(l) {
    var ins = l.instrument;
    if (ins.kind === 'keypad') { wireKeypad(l, ins); }
    else if (ins.kind === 'pair') { wireSingle(l, ins.a, 'A'); wireSingle(l, ins.b, 'B'); }
    else { wireSingle(l, ins, ''); }
    el('setBtn').onclick = function () { attempt(l); };
  }

  function wireSingle(l, ins, suffix) {
    var range = el('ctl' + suffix), num = el('num' + suffix), ro = el('ro' + suffix);

    function paint(v, fromNum) {
      pending[l.id + suffix] = v;
      ro.innerHTML = dp(v, ins.decimals) + (ins.unit ? '<span class="unit">' + esc(ins.unit) + '</span>' : '');
      if (range.value != v) range.value = v;
      if (!fromNum && num.value !== dp(v, ins.decimals)) num.value = dp(v, ins.decimals);
      if (ins.kind === 'dial') paintDial(ins, suffix, v);
    }

    range.oninput = function () { paint(Number(range.value), false); };
    num.oninput = function () {
      var v = Number(num.value);
      if (num.value === '' || isNaN(v)) { pending[l.id + suffix] = null; return; }
      v = Math.min(ins.max, Math.max(ins.min, v));
      paint(v, true);
    };
    if (ins.kind === 'dial') wireDial(l, ins, suffix, paint);
    paint(ins.start !== undefined ? ins.start : ins.min, false);
  }

  function dialAngle(ins, v) {
    // Full-circle instruments read their own angle; everything else
    // sweeps 270 degrees so the ends of the range are distinguishable.
    if (ins.sweep === 360) return (v - ins.min) / (ins.max - ins.min) * 360;
    return -135 + (v - ins.min) / (ins.max - ins.min) * 270;
  }

  function paintDial(ins, suffix, v) {
    var deg = dialAngle(ins, v), rad = (deg - 90) * Math.PI / 180;
    var n = el('needle_ctl' + suffix);
    if (!n) return;
    n.setAttribute('x2', (90 + 68 * Math.cos(rad)).toFixed(2));
    n.setAttribute('y2', (90 + 68 * Math.sin(rad)).toFixed(2));
    var w = el('wedge_ctl' + suffix);
    if (w) {
      if (!ins.wedge) { w.setAttribute('d', ''); return; }
      var end = (deg - 90) * Math.PI / 180, r = 68;
      var large = deg > 180 ? 1 : 0;
      w.setAttribute('d', deg <= 0 ? '' :
        'M 90 90 L 90 ' + (90 - r) + ' A ' + r + ' ' + r + ' 0 ' + large + ' 1 ' +
        (90 + r * Math.cos(end)).toFixed(2) + ' ' + (90 + r * Math.sin(end)).toFixed(2) + ' Z');
    }
  }

  function wireDial(l, ins, suffix, paint) {
    var svg = el('dial_ctl' + suffix);
    if (!svg) return;
    var dragging = false;

    function fromPoint(e) {
      var b = svg.getBoundingClientRect();
      var x = e.clientX - (b.left + b.width / 2);
      var y = e.clientY - (b.top + b.height / 2);
      var deg = Math.atan2(y, x) * 180 / Math.PI + 90;   // 0 at the top, clockwise
      if (deg < 0) deg += 360;
      var frac;
      if (ins.sweep === 360) {
        frac = deg / 360;
      } else {
        if (deg > 225) deg -= 360;                        // -135 .. 135
        frac = (Math.min(135, Math.max(-135, deg)) + 135) / 270;
      }
      var raw = ins.min + frac * (ins.max - ins.min);
      var snapped = Math.round((raw - ins.min) / ins.step) * ins.step + ins.min;
      snapped = Math.min(ins.max, Math.max(ins.min, snapped));
      return Number(snapped.toFixed(ins.decimals || 0));
    }

    svg.style.cursor = 'grab';
    svg.addEventListener('pointerdown', function (e) {
      dragging = true; svg.setPointerCapture(e.pointerId); paint(fromPoint(e), false); e.preventDefault();
    });
    svg.addEventListener('pointermove', function (e) { if (dragging) paint(fromPoint(e), false); });
    svg.addEventListener('pointerup', function (e) { dragging = false; try { svg.releasePointerCapture(e.pointerId); } catch (x) {} });
    svg.addEventListener('pointercancel', function () { dragging = false; });
  }

  function wireKeypad(l, ins) {
    var disp = el('codeDisp'), num = el('numK');
    function paint() {
      var c = pending[l.id] || '';
      var out = '';
      if (ins.maxDigits) out = c;
      else for (var i = 0; i < ins.digits; i++) out += i < c.length ? c[i] : '<span class="blank">&ndash;</span>';
      disp.innerHTML = out;
      if (num.value !== c) num.value = c;
    }
    Array.prototype.forEach.call(document.querySelectorAll('.keypad [data-key]'), function (b) {
      b.onclick = function () {
        var k = b.getAttribute('data-key'), c = pending[l.id] || '';
        if (k === 'clr') c = '';
        else if (k === 'del') c = c.slice(0, -1);
        else if (ins.maxDigits) c = upTo(ins, c + k);
        else if (c.length < ins.digits) c += k;
        pending[l.id] = c;
        paint();
      };
    });
    num.oninput = function () {
      pending[l.id] = ins.maxDigits ? upTo(ins, num.value) : num.value.replace(/[^0-9]/g, '').slice(0, ins.digits);
      paint();
    };
    paint();
  }

  // ---------- attempts ----------
  function attempt(l) {
    var ins = l.instrument, ok, value;
    if (ins.kind === 'keypad') {
      value = pending[l.id] || '';
      if (ins.maxDigits && !value) return;
      if (!ins.maxDigits && value.length < ins.digits) { feedback('bad', 'Not enough digits.', 'The keypad wants all ' + ins.digits + ' of them.'); return; }
      ok = Number(value) === Number(answerOf(l));
    } else if (ins.kind === 'pair') {
      var a = pending[l.id + 'A'], b = pending[l.id + 'B'];
      value = a + ' / ' + b;
      var ans = answerOf(l);
      ok = sameValue(a, ans[0], ins.a.decimals) && sameValue(b, ans[1], ins.b.decimals);
    } else {
      value = pending[l.id + ''];
      ok = sameValue(value, answerOf(l), ins.decimals);
    }

    if (ok) {
      st.open[l.id] = true;
      track('question_answered', { correct: true, question_index: R.locks.indexOf(l) + 1, detail: l.id });
      renderLockBtns();
      renderLockPanel();
      save();
      if (R.locks.every(function (x) { return st.open[x.id]; })) setTimeout(function () { finish(true); }, 900);
      return;
    }

    st.wrongs++;
    st.left -= PENALTY;
    track('question_answered', { correct: false, question_index: R.locks.indexOf(l) + 1, detail: l.id });
    flashPenalty();
    paintClock();
    save();

    if (isMisconception(l, value)) {
      feedback('near', fill(l.missTitle || 'That is the mistake the room is waiting for.'), fill(l.missSays), !!l.missArt);
    } else {
      var wl = wrongLine();
      feedback('bad', fill(wl.head), fill(wl.body));
    }
    if (st.left <= 0) finish(false);
  }

  // The wrong-entry line escalates with the number of wrong settings made in
  // this play, not with which lock was attempted -- locks are solved in any
  // order, so the escalation belongs to the room. st.wrongs has already been
  // incremented by the time this runs, so index 0 is the first mistake. Past
  // the end of the array the last line repeats for the rest of the game: both
  // written rooms depend on that, the terminal line repeating being the joke.
  //
  // A room with no wrongLines gets the original fixed string unchanged, which
  // is what the six unconverted rooms run on.
  //
  // DECIDED 2026-09-08, so it reads as a decision rather than an oversight: a
  // misconception hit consumes an index without printing a line. The escalation
  // is the cost of getting things wrong, and a misconception is getting
  // something wrong -- the player was handed a better and more specific
  // response instead. The lines are texture, not plot; a skipped beat is one
  // nobody can perceive, because the player has no idea what they did not hear.
  // Keeping a separate count would mean new state and a SAVE_V bump, which
  // invalidates every in-progress save to buy an improvement no player can see.
  function wrongLine() {
    var lines = R.wrongLines;
    if (!lines || !lines.length) {
      return { head: 'Nothing moves.',
               body: 'That is not the setting. ' + PENALTY + ' seconds gone.' };
    }
    var e = lines[Math.max(0, Math.min(st.wrongs - 1, lines.length - 1))];
    return typeof e === 'string' ? { head: 'Nothing moves.', body: e } : e;
  }

  function isMisconception(l, value) {
    var m = missOf(l);
    if (m === undefined || m === null) return false;
    if (l.instrument.kind === 'keypad') return String(Number(value)) === String(Number(m));
    if (l.instrument.kind === 'pair') {
      return sameValue(pending[l.id + 'A'], m[0], l.instrument.a.decimals) &&
             sameValue(pending[l.id + 'B'], m[1], l.instrument.b.decimals);
    }
    return sameValue(value, m, l.instrument.decimals);
  }

  // `head` and `body` are both authored prose and may carry markup — a lock's
  // missTitle earns its emphasis (&pound;1728, "1.2 is <i>when</i>").
  function feedback(kind, head, body, withArt) {
    var f = el('fb');
    if (!f) return;
    f.className = 'feedback show ' + kind;
    f.innerHTML = '<b>' + head + '</b>' + body +
      (withArt && HAS_ART ? '<div class="failthumb"><img onerror="mfgArtFallback(this)" src="' + ART + R.art + '-fail.webp" alt="' + esc(R.failAlt) + '" loading="lazy"></div>' : '');
  }

  function flashPenalty() {
    var p = el('penaltyFlash');
    p.textContent = '−' + PENALTY + ' seconds';
    p.classList.add('show');
    setTimeout(function () { p.classList.remove('show'); }, 1100);
  }

  // ---------- hints ----------
  function hintsBody(l) {
    var used = st.hints[l.id] || 0;
    var names = ['Nudge', 'Method', 'Answer'];
    var out = '<div class="hints">';
    for (var i = 0; i < used && i < l.hints.length; i++) {
      out += '<div class="hint"><span class="hint-k">' + names[i] + '</span>' + fill(l.hints[i]) + '</div>';
    }
    if (used < l.hints.length) {
      out += '<button class="btn ghost small" id="hintBtn">' +
        (used === 0 ? 'Stuck? Take a nudge' : 'Still stuck &mdash; ' + names[used].toLowerCase()) +
        '</button> <span class="count">free, but the teacher page lists them</span>';
    } else {
      out += '<p class="empty-note">That is every hint for this lock.</p>';
    }
    return out + '</div>';
  }

  function takeHint() {
    var l = R.locks[activeLock];
    st.hints[l.id] = (st.hints[l.id] || 0) + 1;
    track('hint_used', { question_index: activeLock + 1, detail: l.id + ':' + st.hints[l.id] });
    save();
    renderLockPanel();
  }

  // Hint button is rebuilt on every render, so bind by delegation.
  document.addEventListener('click', function (e) {
    if (e.target && e.target.id === 'hintBtn') takeHint();
  });

  // ---------- clock ----------
  function paintClock() {
    var c = el('clock');
    c.textContent = mmss(st.left);
    c.classList.toggle('low', st.left <= 120);
  }
  function tick() {
    st.left--;
    paintClock();
    if (st.left % 10 === 0) save();
    if (st.left <= 0) finish(false);
  }

  // ---------- start / finish ----------
  function begin(state, resumed) {
    st = state;
    activeLock = null;
    show('scrPlay');
    renderRoom();
    renderLockBtns();
    renderLockPanel();
    paintClock();
    if (timerId) clearInterval(timerId);
    timerId = setInterval(tick, 1000);
    publishVars();
    track('game_started', { detail: resumed ? 'resumed' : 'fresh' });
    window._mfgAbandoned = true;
    if (!window._escUnload) {
      window._escUnload = true;
      window.addEventListener('beforeunload', function () {
        if (window._mfgAbandoned && window.mfg) {
          window.mfg('game_abandoned', { game_slug: R.slug, level: R.level });
        }
      });
    }
  }

  function finish(win) {
    if (st.done) return;
    st.done = win ? 'win' : 'fail';
    if (timerId) clearInterval(timerId);
    window._mfgAbandoned = false;
    clearSave();
    publishVars();

    var used = TOTAL - Math.max(0, st.left);
    var hintCount = 0;
    for (var k in st.hints) hintCount += st.hints[k];
    var opened = R.locks.filter(function (l) { return st.open[l.id]; }).length;

    track('game_completed', {
      score: opened, questions_answered: R.locks.length, questions_correct: opened,
      detail: (win ? 'escaped' : 'timeout') + ' wrongs:' + st.wrongs + ' hints:' + hintCount
    });

    el('endCard').innerHTML =
      '<h1><span class="sub">' + (win ? 'Out, with time to spare' : 'The clock beat you') + '</span>' + esc(R.title) + '</h1>' +
      (HAS_ART ? '<div class="artframe"><img onerror="mfgArtFallback(this)"' +
        (win && R.winAlt ? ' data-fallback="' + ART + R.art + '-scene.webp"' : '') +
        ' src="' + ART + R.art + (win ? (R.winAlt ? '-win' : '-scene') : '-fail') + '.webp" alt="' +
        esc(win ? (R.winAlt || R.sceneAlt) : R.failAlt) + '"></div>' : '') +
      (win ? '<div class="story">' + R.win + '</div>'
           : '<div class="stakes"><b>And so:</b> ' + R.stakes + '</div>') +
      '<div class="end-grid">' +
        '<div class="end-card"><div class="label">Locks opened</div><div class="value">' + opened + ' / ' + R.locks.length + '</div></div>' +
        '<div class="end-card"><div class="label">Time taken</div><div class="value">' + mmss(used) + '</div></div>' +
        '<div class="end-card"><div class="label">Wrong settings</div><div class="value">' + st.wrongs + '</div></div>' +
        '<div class="end-card"><div class="label">Hints taken</div><div class="value">' + hintCount + '</div></div>' +
      '</div>' +
      '<h2>What each lock wanted</h2>' +
      R.locks.map(function (l) {
        return '<div class="lock-brief"><b>' + esc(l.name) + '</b> &mdash; ' + fill(l.solve) + '</div>';
      }).join('') +
      '<div class="btn-row">' +
        '<button class="btn" id="againBtn">Play again</button>' +
        '<a class="btn ghost" href="../">Other rooms</a>' +
        '<a class="btn ghost" href="teacher.html" target="_blank" rel="noopener">Teacher page</a>' +
      '</div>' +
      '<p id="teacherInvite"></p>';
    // The teacher feedback line (schools/assets/teacher-invite.js) on the end card, after its buttons, for
    // both outcomes; mounted here because the card is rebuilt each time. Its game value is the room's
    // directory name: R.slug is 'escape-' + that name.
    if (window.MaffsInvite) window.MaffsInvite.mount(el('teacherInvite'), R.slug.replace(/^escape-/, ''));
    el('againBtn').onclick = function () { begin(freshState()); };
    show('scrEnd');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // ---------- accessibility toggle ----------
  window.toggleAa = function () {
    document.body.classList.toggle('accessible');
    document.querySelector('.a11y-toggle').classList.toggle('active');
  };

  // ---------- go ----------
  document.title = R.title + ' — MaffsGames';
  build();
  if (load()) el('resumeBtn').style.display = '';
})();
