/* "Ugh, stats": the one loader and the chart drawing shared by the four /ugh-stats/ pages
   (contract UGH-STATS-PAGES, 14 Nov 2026).

   A figure on a page is a claim, so no live figure is typed by hand and none comes from outside the site. Each comes
   from one of two committed same-origin files, both written once a day by .github/workflows/answer-counts.yml:

     counts   /schools/assets/answer-counts.json   {as_of, since, total, games:{slug: answers}}
     stats    /schools/assets/ugh-stats.json       {as_of, daily, levels, hours:{weekday, weekend}, countries}

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

  function legend(mount, entries) {
    var p = htmlEl('p', 'ugh-legend');
    entries.forEach(function (e) {
      var s = htmlEl('span', 'ugh-key'), sw = htmlEl('span', 'ugh-swatch');
      sw.style.background = e[1];
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

  window.UghStats = {
    UNAVAILABLE: UNAVAILABLE, HIDDEN: HIDDEN, NAVY: NAVY, TEAL: TEAL,
    run: run, format: format, show: show, hidden: hidden, drawn: drawn, niceMax: niceMax, tally: tally,
    dMon: dMon, asOfDate: asOfDate, weekend: weekend,
    vbars: vbars, hbars: hbars, table: table, legend: legend, hiddenNote: hiddenNote, daily: daily,
    el: htmlEl, csvText: csvText, download: download
  };
})();
