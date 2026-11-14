/* "Ugh, stats": the one loader and the chart drawing shared by the four /ugh-stats/ pages
   (contract UGH-STATS-PAGES, 14 Nov 2026).

   A figure on a page is a claim, so no live figure is typed by hand and none comes from outside the site. Each comes
   from one of two committed same-origin files, both written once a day by .github/workflows/answer-counts.yml:

     counts   /schools/assets/answer-counts.json   {as_of, since, total, games:{slug: answers}}
     stats    /schools/assets/ugh-stats.json       {as_of, daily, levels, hours:{weekday, weekend}, countries}

   The questions (quiz(), below) also read /schools/assets/launch-dates.json {slug: 'YYYY-MM-DD'}, each game's and
   room's launch date (written once by scripts/build-launch-dates.py; a new game adds its own line at launch).

   THE RULE (answer-count.js's): a source that is missing, is not the shape above, or whose as_of is more than 7 days
   old is not used at all. Every mount that reads it ([data-ugh-live="counts"] or [data-ugh-live="stats"]) then shows
   "Figures unavailable right now" and nothing else: never a stale number, and never half a page of numbers (a render
   that throws part-way is wiped the same way). Anything that only makes sense with the data, such as a download
   button, carries data-ugh-needs and stays hidden.

   Small counts: the stats file publishes any count from 1 to 9 as the string "<10". It is drawn as a bar of 5 with
   the label "<10", shown as "<10" in every table and CSV, and never added to anything: tally() returns the numeric
   sum and, separately, how many entries were hidden.

   Charts are plain inline SVG drawn here (no chart library), at the mount's own width so nothing scrolls sideways on a
   phone, and each has its figures as a table under it for screen readers.

   scripts/check-ugh-stats.py holds the four pages and this file to all of the above. */
(function () {
  'use strict';

  var UNAVAILABLE = 'Figures unavailable right now';
  var STALE_MS = 7 * 24 * 3600 * 1000;
  var HIDDEN = '<10';
  var HIDDEN_DRAWN = 5;
  var FILES = { counts: '/schools/assets/answer-counts.json', stats: '/schools/assets/ugh-stats.json' };
  var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  var NAVY = '#1a2744', TEAL = '#0d9488', NAVY_LIGHT = '#7c89a8', GRID = '#e2e8f0', MUTED = '#64748b';
  var SVG_NS = 'http://www.w3.org/2000/svg';
  var MONO = "'JetBrains Mono', ui-monospace, monospace";
  var SANS = "'Outfit', system-ui, sans-serif";

  // ---------------------------------------------------------------------------------------------- counts
  function whole(v) { return typeof v === 'number' && isFinite(v) && v >= 0 && Math.floor(v) === v; }
  function hidden(v) { return v === HIDDEN; }
  function isCount(v) { return hidden(v) || whole(v); }
  function drawn(v) { return hidden(v) ? HIDDEN_DRAWN : v; }
  function format(n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function show(v) { return hidden(v) ? HIDDEN : format(v); }
  // The sum of the counts that are numbers, and how many were hidden. A "<10" is never part of the sum.
  function tally(list) {
    var sum = 0, hid = 0;
    list.forEach(function (v) { if (hidden(v)) hid += 1; else sum += v; });
    return { sum: sum, hidden: hid };
  }

  // ---------------------------------------------------------------------------------------------- dates
  function isDate(s) { return typeof s === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(s); }
  function dMon(date) { return Number(date.slice(8, 10)) + ' ' + MONTHS[Number(date.slice(5, 7)) - 1]; }
  function weekend(date) { var d = new Date(date + 'T00:00:00Z').getUTCDay(); return d === 0 || d === 6; }
  // as_of (an ISO time) as its UK date, "14 Nov 2026".
  function asOfDate(asOf) {
    var parts = {};
    new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/London', day: 'numeric', month: 'numeric', year: 'numeric' })
      .formatToParts(new Date(asOf)).forEach(function (p) { parts[p.type] = p.value; });
    return Number(parts.day) + ' ' + MONTHS[Number(parts.month) - 1] + ' ' + parts.year;
  }

  // ---------------------------------------------------------------------------------------------- the loader
  function fresh(src, now) {
    if (!src || typeof src !== 'object' || typeof src.as_of !== 'string') return false;
    var t = Date.parse(src.as_of);
    return isFinite(t) && now - t <= STALE_MS;
  }
  function rows(list, nameKey, countKey) {
    return Array.isArray(list) && list.every(function (r) {
      return r && typeof r === 'object' && typeof r[nameKey] === 'string' && r[nameKey] && isCount(r[countKey]);
    });
  }
  var SHAPE = {
    counts: function (o) {
      return whole(o.total) && typeof o.since === 'string' && o.games && typeof o.games === 'object' &&
        Object.keys(o.games).every(function (k) { return whole(o.games[k]); });
    },
    stats: function (o) {
      var h = o.hours;
      return rows(o.daily, 'date', 'starts') && o.daily.length > 0 && o.daily.every(function (r) { return isDate(r.date); }) &&
        rows(o.levels, 'level', 'starts') && rows(o.countries, 'country', 'sessions') &&
        h && typeof h === 'object' && ['weekday', 'weekend'].every(function (k) {
          return Array.isArray(h[k]) && h[k].length === 24 && h[k].every(isCount);
        });
    }
  };
  // XMLHttpRequest, as answer-count.js uses: the local test server replaces window.fetch with a stub that refuses.
  function get(url) {
    return new Promise(function (resolve, reject) {
      var x = new XMLHttpRequest();
      x.open('GET', url);
      x.timeout = 8000;
      x.onload = function () {
        if (x.status !== 200) { reject(new Error('status ' + x.status)); return; }
        try { resolve(JSON.parse(x.responseText)); } catch (e) { reject(e); }
      };
      x.onerror = x.ontimeout = function () { reject(new Error('network')); };
      x.send();
    });
  }
  // The source, or null when it must not be used.
  function load(name) {
    return get(FILES[name])
      .then(function (o) { return fresh(o, Date.now()) && SHAPE[name](o) ? o : null; })
      .catch(function () { return null; });
  }

  var redraws = [];
  function unavailable(mount) {
    mount.textContent = UNAVAILABLE;
    mount.classList.add('ugh-unavailable');
    mount.setAttribute('data-ugh-state', 'unavailable');
  }
  // run({counts: fn(data), stats: fn(data)}): load each source the page names and hand it to the page's renderer,
  // or mark every mount of that source unavailable. Sets data-ugh-ready on <html> when both are settled.
  function run(renderers) {
    var doc = document;
    var jobs = Object.keys(renderers).map(function (name) {
      var mounts = [].slice.call(doc.querySelectorAll('[data-ugh-live="' + name + '"]'));
      var needs = [].slice.call(doc.querySelectorAll('[data-ugh-needs="' + name + '"]'));
      return load(name).then(function (data) {
        var ok = false, before = redraws.length;
        if (data) {
          try { renderers[name](data); ok = true; } catch (e) { ok = false; }
        }
        if (ok) {
          mounts.forEach(function (m) { m.setAttribute('data-ugh-state', 'live'); });
          needs.forEach(function (n) { n.hidden = false; });
        } else {
          redraws.length = before;                    // a wiped chart must not come back on a resize
          mounts.forEach(unavailable);
          needs.forEach(function (n) { n.hidden = true; });
        }
      });
    });
    return Promise.all(jobs).then(function () { doc.documentElement.setAttribute('data-ugh-ready', '1'); });
  }

  var resizeTimer = 0;
  window.addEventListener('resize', function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () { redraws.forEach(function (f) { f(); }); }, 120);
  });

  // ---------------------------------------------------------------------------------------------- drawing
  function svgEl(name, attrs, text) {
    var e = document.createElementNS(SVG_NS, name);
    Object.keys(attrs || {}).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (text !== undefined) e.textContent = text;
    return e;
  }
  function htmlEl(name, cls, text) {
    var e = document.createElement(name);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    return e;
  }
  function niceMax(v) {
    if (!(v > 10)) return 10;
    var pow = Math.pow(10, Math.floor(Math.log(v) / Math.LN10)), steps = [1, 2, 4, 5, 10];
    for (var i = 0; i < steps.length; i++) if (steps[i] * pow >= v) return steps[i] * pow;
    return 10 * pow;
  }
  function chartBox(mount, title) {
    var box = htmlEl('div', 'ugh-chart');
    box.setAttribute('role', 'img');
    box.setAttribute('aria-label', title + '. The figures are in the table that follows.');
    mount.appendChild(box);
    return box;
  }
  function width(box) { return Math.max(240, Math.min(box.clientWidth || 320, 720)); }
  function later(draw) { redraws.push(draw); draw(); }

  // Upright bars, one per item {name, tick, value, fill}: name is the bar's full label (its tooltip), tick the
  // label under it ('' for none), value a count (a number or "<10"). o: {title, max, height, unit}.
  function vbars(mount, items, o) {
    var box = chartBox(mount, o.title);
    later(function () {
      var W = width(box), H = o.height || 210, m = { l: 40, r: 4, t: 26, b: 24 };
      var pw = W - m.l - m.r, ph = H - m.t - m.b;
      var max = o.max || niceMax(Math.max.apply(null, items.map(function (it) { return drawn(it.value); })));
      var svg = svgEl('svg', { viewBox: '0 0 ' + W + ' ' + H, width: W, height: H, 'aria-hidden': 'true', focusable: 'false' });
      [0, max / 2, max].forEach(function (t) {
        var y = m.t + ph - ph * t / max;
        svg.appendChild(svgEl('line', { x1: m.l, x2: W - m.r, y1: y, y2: y, stroke: t ? GRID : MUTED, 'stroke-width': 1 }));
        svg.appendChild(svgEl('text', { x: m.l - 6, y: y + 3.5, 'text-anchor': 'end', 'font-size': 10, 'font-family': MONO, fill: MUTED },
          format(t) + (o.unit || '')));
      });
      var band = pw / items.length, bw = Math.max(2, band * 0.72);
      items.forEach(function (it, i) {
        var v = drawn(it.value), h = ph * v / max, x = m.l + band * i + (band - bw) / 2, y = m.t + ph - h;
        var rect = svgEl('rect', { x: x.toFixed(1), y: y.toFixed(1), width: bw.toFixed(1), height: Math.max(h, v ? 1 : 0).toFixed(1),
          fill: it.fill || NAVY, 'data-value': String(it.value) });
        rect.appendChild(svgEl('title', {}, it.name + ': ' + show(it.value) + (o.unit || '')));
        svg.appendChild(rect);
        var cx = x + bw / 2;
        if (hidden(it.value)) {
          svg.appendChild(svgEl('text', { x: cx, y: y - 3, 'font-size': 9, 'font-family': MONO, fill: MUTED,
            transform: 'rotate(-90 ' + cx.toFixed(1) + ' ' + (y - 3).toFixed(1) + ')', 'dominant-baseline': 'central', 'data-hidden-label': '1' }, HIDDEN));
        }
        if (it.tick) {
          svg.appendChild(svgEl('text', { x: cx, y: H - 7, 'text-anchor': 'middle', 'font-size': 10, 'font-family': SANS, fill: MUTED }, it.tick));
        }
      });
      box.textContent = '';
      box.appendChild(svg);
    });
  }

  // Bars lying down, one per item {name, value, text, fill}: the name sits above its bar, the figure after it.
  // value is a number or "<10"; text, when given, is the figure as the page words it (e.g. "59.9%").
  function hbars(mount, items, o) {
    var box = chartBox(mount, o.title);
    later(function () {
      var W = width(box), row = 40, gutter = 70, H = items.length * row + 4;
      var max = o.max || Math.max.apply(null, items.map(function (it) { return drawn(it.value); })) || 1;
      var svg = svgEl('svg', { viewBox: '0 0 ' + W + ' ' + H, width: W, height: H, 'aria-hidden': 'true', focusable: 'false' });
      items.forEach(function (it, i) {
        var y = i * row, v = drawn(it.value), w = Math.max((W - gutter) * v / max, v ? 2 : 0);
        var label = it.text || show(it.value);
        svg.appendChild(svgEl('text', { x: 0, y: y + 13, 'font-size': 13, 'font-family': SANS, fill: NAVY }, it.name));
        var rect = svgEl('rect', { x: 0, y: y + 19, width: w.toFixed(1), height: 14, rx: 2, fill: it.fill || TEAL, 'data-value': String(it.value) });
        rect.appendChild(svgEl('title', {}, it.name + ': ' + label));
        svg.appendChild(rect);
        svg.appendChild(svgEl('text', { x: (w + 6).toFixed(1), y: y + 30.5, 'font-size': 12, 'font-family': MONO, fill: NAVY, 'font-weight': 700 }, label));
      });
      box.textContent = '';
      box.appendChild(svg);
    });
  }

  // The figures behind a chart, as a table under it.
  function table(mount, caption, heads, body) {
    var d = htmlEl('details', 'ugh-table'), t = htmlEl('table'), hr = htmlEl('tr');
    d.appendChild(htmlEl('summary', '', 'Show the figures as a table'));
    t.appendChild(htmlEl('caption', '', caption));
    heads.forEach(function (h) { var th = htmlEl('th', '', h); th.scope = 'col'; hr.appendChild(th); });
    var thead = htmlEl('thead'), tb = htmlEl('tbody');
    thead.appendChild(hr); t.appendChild(thead);
    body.forEach(function (r) {
      var tr = htmlEl('tr');
      r.forEach(function (c, i) { var cell = htmlEl(i ? 'td' : 'th', '', String(c)); if (!i) cell.scope = 'row'; tr.appendChild(cell); });
      tb.appendChild(tr);
    });
    t.appendChild(tb); d.appendChild(t); mount.appendChild(d);
  }

  // entries: [label, colour] or [label, colour, 'ring'] (a hollow point's key).
  function legend(mount, entries) {
    var p = htmlEl('p', 'ugh-legend');
    entries.forEach(function (e) {
      var s = htmlEl('span', 'ugh-key'), sw = htmlEl('span', 'ugh-swatch' + (e[2] === 'ring' ? ' ring' : ''));
      if (e[2] === 'ring') sw.style.borderColor = e[1]; else sw.style.background = e[1];
      s.appendChild(sw); s.appendChild(document.createTextNode(e[0]));
      p.appendChild(s);
    });
    mount.appendChild(p);
  }
  function hiddenNote(mount, values) {
    if (values.some(hidden)) {
      mount.appendChild(htmlEl('p', 'ugh-note', 'A bar marked "<10" is a count from 1 to 9. We hide the exact figure and draw it as 5.'));
    }
  }

  // "Games started each day, last 30 days": the charts page and Case 2 share it.
  function daily(mount, stats) {
    var title = 'Games started each day, last 30 days';
    mount.textContent = '';
    legend(mount, [['Weekday', NAVY], ['Saturday or Sunday', NAVY_LIGHT]]);
    vbars(mount, stats.daily.map(function (r) {
      var mon = new Date(r.date + 'T00:00:00Z').getUTCDay() === 1;
      return { name: dMon(r.date), tick: mon ? dMon(r.date) : '', value: r.starts, fill: weekend(r.date) ? NAVY_LIGHT : NAVY };
    }), { title: title });
    mount.appendChild(htmlEl('p', 'ugh-axis', 'Each bar is one day. The dates marked are Mondays.'));
    hiddenNote(mount, stats.daily.map(function (r) { return r.starts; }));
    table(mount, title, ['Day', 'Games started'], stats.daily.map(function (r) {
      return [dMon(r.date) + (weekend(r.date) ? ' (weekend)' : ''), show(r.starts)];
    }));
  }

  // A CSV built in the browser and handed to the viewer; nothing leaves the page.
  function csvText(heads, body) {
    var cell = function (c) { c = String(c); return /[",\n]/.test(c) ? '"' + c.replace(/"/g, '""') + '"' : c; };
    return [heads].concat(body).map(function (r) { return r.map(cell).join(','); }).join('\r\n') + '\r\n';
  }
  function download(filename, heads, body) {
    var a = document.createElement('a');
    var url = URL.createObjectURL(new Blob([csvText(heads, body)], { type: 'text/csv;charset=utf-8' }));
    a.href = url; a.download = filename;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  }

  // Points lying in a plane, one per item {name, x, y, hollow}. o: {title, xLabel, yLabel, xMin, xMax, xStep, yMax}.
  // A hollow point is drawn as a ring; the page's key says what hollow means. (Contract UGH-STATS-QUESTIONS.)
  function scatter(mount, points, o) {
    var box = chartBox(mount, o.title);
    later(function () {
      var W = width(box), H = o.height || 270, m = { l: 60, r: 12, t: 12, b: 42 };
      var pw = W - m.l - m.r, ph = H - m.t - m.b;
      var yMax = o.yMax || niceMax(Math.max.apply(null, points.map(function (p) { return p.y; })));
      var X = function (x) { return m.l + pw * (x - o.xMin) / (o.xMax - o.xMin); };
      var Y = function (y) { return m.t + ph - ph * y / yMax; };
      var svg = svgEl('svg', { viewBox: '0 0 ' + W + ' ' + H, width: W, height: H, 'aria-hidden': 'true', focusable: 'false' });
      [0, yMax / 2, yMax].forEach(function (t) {
        svg.appendChild(svgEl('line', { x1: m.l, x2: W - m.r, y1: Y(t), y2: Y(t), stroke: t ? GRID : MUTED, 'stroke-width': 1 }));
        svg.appendChild(svgEl('text', { x: m.l - 6, y: Y(t) + 3.5, 'text-anchor': 'end', 'font-size': 10, 'font-family': MONO, fill: MUTED }, format(t)));
      });
      for (var t = o.xMin; t <= o.xMax + 1e-9; t += o.xStep) {
        svg.appendChild(svgEl('line', { x1: X(t), x2: X(t), y1: m.t, y2: m.t + ph, stroke: GRID, 'stroke-width': 1 }));
        svg.appendChild(svgEl('text', { x: X(t), y: m.t + ph + 14, 'text-anchor': 'middle', 'font-size': 10, 'font-family': MONO, fill: MUTED }, String(t)));
      }
      svg.appendChild(svgEl('text', { x: m.l + pw / 2, y: H - 6, 'text-anchor': 'middle', 'font-size': 11, 'font-family': SANS, fill: NAVY }, o.xLabel));
      var yl = 14, ym = m.t + ph / 2;
      svg.appendChild(svgEl('text', { x: yl, y: ym, 'text-anchor': 'middle', 'font-size': 11, 'font-family': SANS, fill: NAVY,
        transform: 'rotate(-90 ' + yl + ' ' + ym + ')' }, o.yLabel));
      points.forEach(function (p) {
        var c = svgEl('circle', { cx: X(p.x).toFixed(1), cy: Y(p.y).toFixed(1), r: 5.5, fill: p.hollow ? '#ffffff' : NAVY, stroke: NAVY,
          'stroke-width': 2, 'data-x': String(p.x), 'data-y': String(p.y), 'data-hollow': p.hollow ? '1' : '0' });
        c.appendChild(svgEl('title', {}, p.name));
        svg.appendChild(c);
      });
      box.textContent = '';
      box.appendChild(svg);
    });
  }

  // ---------------------------------------------------------------------------------------------- questions
  /* The question widget, one copy for every case (contract UGH-STATS-QUESTIONS, 14 Nov 2026). A page hands quiz() its
     questions as data, in order; each is an object, or a function that builds one from the page's live figures and
     returns null (or throws) when it cannot. A question that cannot be built is skipped and keeps its number, so
     question_index is always the question's place in the case's list.

       typed   {type: 'typed', stem, answer, working}: a whole number, to the nearest whole number. Only the exact
               answer is accepted; three tries, then the working. Commas and spaces in what is typed are ignored.
               With dp: 1 (UGH-STATS-CASE1-1DP) the answer is to 1 decimal place, the keypad offers a decimal point,
               and only that value is accepted ("90.9" or "90.90"; never "91" or "90.8"). dp 0 is the default.
       choice  {type: 'choice', stem, options: [{text, why, right}] x 4, exactly one right}: shuffled once per page
               load, one try, then the chosen option's explanation and, if it was wrong, the right one with its own.

     Every answer sends one event under its own name (never the event that counts game answers, so nothing that counts
     those has to filter these out):
     {game_slug: 'ugh-stats', level: 'case1'..'case4', question_index, correct (right first time), attempts}.
     No score is kept. */
  var EVENT = 'stats_question_answered';
  var TRIES = 3;
  var SINCE = '2026-09-01';
  var FULL_MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
    'November', 'December'];

  function getText(url) {
    return new Promise(function (resolve, reject) {
      var x = new XMLHttpRequest();
      x.open('GET', url);
      x.timeout = 8000;
      x.onload = function () { if (x.status === 200) resolve(x.responseText); else reject(new Error('status ' + x.status)); };
      x.onerror = x.ontimeout = function () { reject(new Error('network')); };
      x.send();
    });
  }
  // launch-dates.json {slug: 'YYYY-MM-DD'}, or null when it is missing or not that shape.
  function launchDates() {
    return get('/schools/assets/launch-dates.json').then(function (o) {
      var ok = o && typeof o === 'object' && !Array.isArray(o) && Object.keys(o).length > 0 &&
        Object.keys(o).every(function (k) { return isDate(o[k]); });
      return ok ? o : null;
    }).catch(function () { return null; });
  }
  // A game's own name, from the <h1> of its page; null when it has none.
  function gameName(slug) {
    return getText('/games/' + encodeURIComponent(slug) + '/').then(function (html) {
      var h1 = new DOMParser().parseFromString(html, 'text/html').querySelector('h1');
      var name = h1 ? h1.textContent.replace(/\s+/g, ' ').trim() : '';
      return name || null;
    }).catch(function () { return null; });
  }
  // Each game's levels, as the portal lists them: the union of the data-levels of every card on the home page that
  // links to it ({slug: ['alevel', 'level4', ...]}; Level 4's two spellings are one key). null when the page cannot be read.
  // (games.json holds no levels; the cards' data-levels are the roster's, held to it by scripts/check-levels.py.)
  function homeLevels() {
    return getText('/').then(function (html) {
      var out = {};
      new DOMParser().parseFromString(html, 'text/html').querySelectorAll('a.game-card[data-levels]').forEach(function (a) {
        var m = /^\/?games\/([^\/?#]+)\//.exec(a.getAttribute('href') || '');
        if (!m) return;
        var set = out[m[1]] || (out[m[1]] = []);
        a.getAttribute('data-levels').split(/\s+/).forEach(function (l) {
          if (l === 'l4') l = 'level4';
          if (l && set.indexOf(l) < 0) set.push(l);
        });
      });
      return out;
    }).catch(function () { return null; });
  }
  var LEVEL_WORDS = { alevel: 'A level', further: 'Further Maths', level4: 'Level 4' };
  // ['further', 'level4'] -> 'Further Maths and Level 4' (in the order A level, Further Maths, Level 4).
  function levelWords(levels) {
    var w = ['alevel', 'further', 'level4'].filter(function (l) { return levels.indexOf(l) >= 0; })
      .map(function (l) { return LEVEL_WORDS[l]; });
    return w.length > 1 ? w.slice(0, -1).join(', ') + ' and ' + w[w.length - 1] : w[0];
  }

  function ukDate(asOf) {
    var parts = {};
    new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/London', day: '2-digit', month: '2-digit', year: 'numeric' })
      .formatToParts(new Date(asOf)).forEach(function (p) { parts[p.type] = p.value; });
    return parts.year + '-' + parts.month + '-' + parts.day;
  }
  // The number of calendar dates from a to b, both counted.
  function days(a, b) { return Math.round((Date.parse(b + 'T00:00:00Z') - Date.parse(a + 'T00:00:00Z')) / 864e5) + 1; }
  function longDate(date) { return Number(date.slice(8, 10)) + ' ' + FULL_MONTHS[Number(date.slice(5, 7)) - 1] + ' ' + date.slice(0, 4); }

  // n ÷ d for whole numbers (d at least 1), worked in whole numbers so the working cannot disagree with the answer:
  // the answer to the nearest whole number (a half goes up), and the working "n ÷ d = q ≈ answer." with q to 1 decimal
  // place, or to more places when 1 place would read as a half that rounds the other way.
  // dp 1 (contract UGH-STATS-CASE1-1DP): the answer to 1 decimal place, the working to 3 places (or more, by the same
  // rule). answer is a number (90.9), text the answer as written ("90.9").
  function divide(n, d, dp) {
    var one = dp === 1 ? 10 : 1;
    var answer = Math.floor((2 * one * n + d) / (2 * d));          // in units of 1/one, a half going up
    var k = dp === 1 ? 3 : 1, p = Math.pow(10, k), scaled = 0;
    for (; k <= 7; k++, p *= 10) {
      scaled = Math.floor((2 * p * n + d) / (2 * d));
      var r = p / one;
      if (Math.floor((2 * scaled + r) / (2 * r)) === answer) break;
    }
    var shown = fixed(scaled, k), text = fixed(answer, dp === 1 ? 1 : 0);
    return { answer: answer / one, text: text, shown: shown, working: format(n) + ' ÷ ' + format(d) + ' = ' + shown + ' ≈ ' + text + '.' };
  }
  // A whole number of 10^-k units, written with k decimal places and thousands commas.
  function fixed(scaled, k) {
    if (!k) return format(scaled);
    var s = String(scaled);
    while (s.length <= k) s = '0' + s;
    return format(Number(s.slice(0, s.length - k))) + '.' + s.slice(s.length - k);
  }
  // What was typed, in tenths, for a 1 dp question: "90.9" and "90.90" are 909; "90.95" is not a 1 dp value (NaN).
  function tenths(raw) {
    var m = /^(\d*)(?:\.(\d*))?$/.exec(raw);
    if (!m || !(m[1] + (m[2] || ''))) return NaN;
    var frac = m[2] || '';
    if (/[^0]/.test(frac.slice(1))) return NaN;
    return Number(m[1] || '0') * 10 + Number(frac.charAt(0) || '0');
  }

  function validQuestion(q) {
    if (!q || typeof q !== 'object' || typeof q.stem !== 'string' || !q.stem) return false;
    if (q.type === 'typed') {
      var dp = q.dp === undefined ? 0 : q.dp;
      var ok = dp === 0 ? whole(q.answer)
        : dp === 1 && typeof q.answer === 'number' && q.answer >= 0 && Math.abs(q.answer * 10 - Math.round(q.answer * 10)) < 1e-9;
      return ok && typeof q.working === 'string' && !!q.working;
    }
    if (q.type !== 'choice' || !Array.isArray(q.options) || q.options.length !== 4) return false;
    return q.options.every(function (o) { return o && typeof o.text === 'string' && typeof o.why === 'string'; }) &&
      q.options.filter(function (o) { return o.right === true; }).length === 1;
  }
  function shuffle(list) {
    for (var i = list.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)), t = list[i];
      list[i] = list[j]; list[j] = t;
    }
    return list;
  }
  function send(level, q, correct, attempts) {
    if (typeof window.mfg !== 'function') return;
    try {
      window.mfg(EVENT, { game_slug: 'ugh-stats', level: level, question_index: q.index, correct: correct, attempts: attempts });
    } catch (e) { /* analytics never breaks the page */ }
  }

  function quiz(mount, level, list) {
    var qs = [];
    list.forEach(function (item, i) {
      var q = null;
      try { q = typeof item === 'function' ? item() : item; } catch (e) { q = null; }
      if (!validQuestion(q)) return;
      q = Object.assign({}, q, { index: i + 1 });
      if (q.type === 'choice') q.options = shuffle(q.options.slice());
      qs.push(q);
    });
    mount.textContent = '';
    var box = htmlEl('div', 'ugh-quiz');
    mount.appendChild(box);

    function render(pos) {
      var q = qs[pos];
      box.textContent = '';
      box.removeAttribute('data-q-state');
      box.setAttribute('data-q-index', String(q.index));
      box.setAttribute('data-q-type', q.type);
      var head = htmlEl('p', 'ugh-q-count', 'Question ' + (pos + 1) + ' of ' + qs.length);
      head.tabIndex = -1;
      box.appendChild(head);
      box.appendChild(htmlEl('p', 'ugh-q-stem', q.stem));
      var fb = htmlEl('div', 'ugh-q-feedback');
      fb.setAttribute('aria-live', 'polite');
      var next = htmlEl('button', 'btn ugh-q-next', 'Next');
      next.type = 'button';
      next.hidden = true;
      next.addEventListener('click', function () { render(pos + 1); box.querySelector('.ugh-q-count').focus(); });
      var line = function (cls, text) { fb.appendChild(htmlEl('p', cls, text)); };
      var done = function () {
        if (pos < qs.length - 1) next.hidden = false;
        else line('ugh-q-end', 'That was the last question.');
        box.setAttribute('data-q-state', 'answered');
      };

      if (q.type === 'typed') {
        var form = htmlEl('form', 'ugh-q-form'), id = 'ugh-q-' + level + '-' + q.index;
        var label = htmlEl('label', 'ugh-q-label', 'Your answer');
        label.htmlFor = id;
        var input = htmlEl('input', 'ugh-q-input');
        var dp = q.dp === 1 ? 1 : 0;
        input.id = id; input.type = 'text'; input.inputMode = dp ? 'decimal' : 'numeric'; input.autocomplete = 'off';
        input.setAttribute('enterkeyhint', 'done');
        var check = htmlEl('button', 'btn ugh-q-check', 'Check');
        check.type = 'submit';
        form.appendChild(label); form.appendChild(input); form.appendChild(check);
        box.appendChild(form);
        var tries = 0;
        form.addEventListener('submit', function (e) {
          e.preventDefault();
          if (input.disabled) return;
          var raw = input.value.replace(/[\s,]/g, '');
          fb.textContent = '';
          if (dp === 0 && !/^\d+$/.test(raw)) { line('ugh-q-try', 'Type a whole number.'); return; }
          if (dp === 1 && !/^\d*\.?\d+$|^\d+\.$/.test(raw)) { line('ugh-q-try', 'Type a number.'); return; }
          tries += 1;
          var right = dp === 1 ? tenths(raw) === Math.round(q.answer * 10) : Number(raw) === q.answer;
          if (!right && tries < TRIES) {
            var left = TRIES - tries;
            line('ugh-q-try', 'Not quite. Try again: ' + left + (left === 1 ? ' try' : ' tries') + ' left.');
            input.select();
            return;
          }
          input.disabled = true; check.disabled = true;
          line('ugh-q-verdict', right ? 'Right.' : 'Not this time. The answer is ' + (dp === 1 ? fixed(Math.round(q.answer * 10), 1) : format(q.answer)) + '.');
          line('ugh-q-working', 'Working: ' + q.working);
          send(level, q, right && tries === 1, tries);
          done();
        });
      } else {
        var group = htmlEl('div', 'ugh-q-options');
        group.setAttribute('role', 'group');
        group.setAttribute('aria-label', 'Choose one answer');
        var buttons = q.options.map(function (o) {
          var b = htmlEl('button', 'ugh-q-option', o.text);
          b.type = 'button';
          b.addEventListener('click', function () {
            if (b.disabled) return;
            buttons.forEach(function (x) { x.disabled = true; });
            b.classList.add('chosen');
            var rightOne = q.options.filter(function (x) { return x.right; })[0];
            buttons[q.options.indexOf(rightOne)].classList.add('right');
            line('ugh-q-verdict', o.right ? 'Right.' : 'Not quite.');
            line('ugh-q-why', o.why);
            if (!o.right) {
              line('ugh-q-answer', 'The answer: ' + rightOne.text);
              line('ugh-q-why', rightOne.why);
            }
            send(level, q, o.right === true, 1);
            done();
          });
          group.appendChild(b);
          return b;
        });
        box.appendChild(group);
      }
      box.appendChild(fb);
      box.appendChild(next);
    }

    if (qs.length) render(0);
    else box.appendChild(htmlEl('p', 'ugh-note', UNAVAILABLE));
    mount.setAttribute('data-ugh-quiz', 'ready');
  }

  window.UghStats = {
    UNAVAILABLE: UNAVAILABLE, HIDDEN: HIDDEN, NAVY: NAVY, TEAL: TEAL, SINCE: SINCE,
    run: run, format: format, show: show, hidden: hidden, drawn: drawn, whole: whole, niceMax: niceMax, tally: tally,
    dMon: dMon, asOfDate: asOfDate, weekend: weekend, ukDate: ukDate, days: days, longDate: longDate,
    vbars: vbars, hbars: hbars, scatter: scatter, table: table, legend: legend, hiddenNote: hiddenNote, daily: daily,
    el: htmlEl, csvText: csvText, download: download,
    launchDates: launchDates, gameName: gameName, homeLevels: homeLevels, levelWords: levelWords, divide: divide, quiz: quiz
  };
})();
