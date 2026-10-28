/* The reading-charts question generator (contract AS-YOU-CAN-SEE, Jon, 27 Oct 2026): pictograms, bar charts, line graphs,
   scatter graphs and "is this chart lying?".

   Bank first (canon 8.2.1): the game "As You Can See" loads this same file and never copies a question; the 6 P's can
   import it later. Pure data, no DOM: MaffsReadingCharts.question(stage, slot, rng) returns one question as plain data (the
   chart, the stem, the answer, the working and the named slips), and the drawing of the chart is the caller's (the game
   draws every chart in SVG from the data). rng is a function returning a number from 0 up to 1; MaffsReadingCharts.bank()
   makes all 60 questions with a fixed seed, so the bank is the same every time.

   Five stages, 12 slots each (the slot fixes what the question is about; rng chooses the setting, the scale and the
   numbers, so the 12 are always 12 different questions):
     1 pictograms     read a row, the key, half and quarter symbols, totals, differences, a changed key
     2 bar charts     scales in 2s, 5s and 10s; comparisons; dual bars; composite (stacked) bars
     3 line graphs    reading values, change, the trend, and "can you tell between the points?"
     4 scatter graphs type of correlation, estimating from a line of best fit, outliers, correlation is not cause,
                      estimating beyond the data
     5 is it lying?   a truncated axis, an uneven scale, pictures scaled both ways, 3D bars, missing labels, or a fair chart

   A question is { stage, slot, kind, chart, stem, ask, answer, worked, slips, calc } where
     chart    the chart as data (see each stage: type is pictogram | bar | dual | composite | line | scatter | lying)
     ask      what is asked: { op: ..., ... } (the verifier recomputes the answer from the chart and this)
     answer   { type: 'number', value, tol } | { type: 'choice', options: [...], correct: <index> }
              A number is right within tol of value. tol is half a minor gridline for a reading from a graph and 0 for a
              count, a total or a difference worked out from readings. (MaffsAnswer has no value-with-tolerance match, so
              the accepted interval lives here, in the question: a candidate for the shared helper.)
     slips    [{ kind, answer: { value } | { option }, line }]: the named wrong answers, each outside the accepted interval
     calc     false: nothing here needs a calculator
*/
(function (root) {
  'use strict';

  var SLOTS = 12, FIXED_SEED = 20261027;
  var CANT = "You can't tell";

  /* ---------- small helpers ---------- */
  function makeRng(seed) {
    var s = seed >>> 0;
    return function () {
      s = (s + 0x6D2B79F5) >>> 0;
      var t = s;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function rint(rng, a, b) { return a + Math.floor(rng() * (b - a + 1)); }
  function pick(rng, arr) { return arr[Math.floor(rng() * arr.length)]; }
  function shuffled(rng, arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(rng() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function sum(a) { return a.reduce(function (x, y) { return x + y; }, 0); }
  function lower(s) { return s.charAt(0).toLowerCase() + s.slice(1); }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  function idxMax(a) { var k = 0; for (var i = 1; i < a.length; i++) if (a[i] > a[k]) k = i; return k; }
  function idxMin(a) { var k = 0; for (var i = 1; i < a.length; i++) if (a[i] < a[k]) k = i; return k; }
  // k different values from [lo, hi], each a multiple of step.
  function distinctMultiples(rng, k, lo, hi, step) {
    var pool = [], v;
    for (v = lo; v <= hi; v += step) pool.push(v);
    return shuffled(rng, pool).slice(0, k);
  }

  function num(value, tol) { return { type: 'number', value: value, tol: tol || 0 }; }
  function slipN(kind, value, line) { return { kind: kind, answer: { value: value }, line: line }; }
  function slipO(kind, option, line) { return { kind: kind, answer: { option: option }, line: line }; }

  // The finished question: slips outside the accepted interval, none repeated, none negative.
  function finish(stage, slot, kind, chart, stem, ask, answer, worked, slips) {
    var out = [], seen = {};
    (slips || []).forEach(function (s) {
      var key, bad;
      if (answer.type === 'number') {
        key = 'n' + s.answer.value;
        bad = Math.abs(s.answer.value - answer.value) <= answer.tol + 1e-9 || s.answer.value < 0;
      } else {
        key = 'o' + s.answer.option;
        bad = answer.options[answer.correct] === s.answer.option || answer.options.indexOf(s.answer.option) < 0;
      }
      if (!bad && !seen[key]) { seen[key] = 1; out.push(s); }
    });
    if (chart.minor && !/each gridline is/.test(worked.join(' ')) && !/^line-(between|estimate|trend|compare|any-above|peak|steepest)$/.test(kind)) worked = [scaleLine(chart)].concat(worked);
    return { stage: stage, slot: slot, kind: kind, chart: chart, stem: stem, ask: ask, answer: answer, worked: worked, slips: out, calc: false };
  }
  // A multiple-choice answer from the right option and the wrong ones (the right one placed by rng).
  function choice(rng, right, wrongs) {
    var opts = shuffled(rng, [right].concat(wrongs));
    return { type: 'choice', options: opts, correct: opts.indexOf(right) };
  }
  // Options in a fixed order (labels the student reads in order, like the categories of a chart).
  function choiceFixed(options, right) { return { type: 'choice', options: options.slice(), correct: options.indexOf(right) }; }

  /* =====================================================================================================
     STAGE 1: pictograms. chart = { type: 'pictogram', title, shape, per, what, rows: [{ label, q }], keyHidden }
     q is the row in quarter-symbols: 4 a whole symbol, 2 a half, 1 a quarter; a row's value is q x per / 4.
     ===================================================================================================== */
  var PIC = [
    { title: 'Books borrowed from the library', what: 'books', shape: 'circle' },
    { title: 'Cups of tea sold at the cafe', what: 'cups of tea', shape: 'square' },
    { title: 'Bikes in the cycle park', what: 'bikes', shape: 'triangle' },
    { title: 'School lunches ordered', what: 'lunches', shape: 'diamond' },
    { title: 'Visitors to the museum', what: 'visitors', shape: 'star' },
    { title: 'Tickets sold for the school play', what: 'tickets', shape: 'square' }
  ];
  var PIC_ROWS = [
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    ['Class 7A', 'Class 7B', 'Class 7C', 'Class 7D', 'Class 7E'],
    ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5']
  ];
  function picChart(rng, per, mode) {
    var c = pick(rng, PIC), labels = pick(rng, PIC_ROWS), rows = [];
    // Each row is some whole symbols and, in half and quarter mode, a part symbol on at least two rows.
    var partRows = shuffled(rng, [0, 1, 2, 3, 4]).slice(0, mode === 'whole' ? 0 : 3);
    labels.forEach(function (l, i) {
      var n = rint(rng, 1, 5), part = 0;
      if (partRows.indexOf(i) >= 0) part = mode === 'half' ? 2 : (rng() < 0.7 ? 1 : 2);
      rows.push({ label: l, q: 4 * n + part });
    });
    return { type: 'pictogram', title: c.title, shape: c.shape, per: per, what: c.what, rows: rows, keyHidden: false };
  }
  function val(ch, i) { return ch.rows[i].q * ch.per / 4; }
  function symbols(r) { return Math.ceil(r.q / 4); }          // symbols counted as the picture shows them
  function wholes(r) { return Math.floor(r.q / 4); }
  function partOf(r) { return r.q % 4; }
  function sym(n, whole) { return n + ' ' + (whole ? 'whole ' : '') + (n === 1 ? 'symbol' : 'symbols'); }   // counts agree in number: 1 symbol, 2 symbols
  function pickRowWith(rng, ch, part) {                       // a row whose part symbol is `part` quarters (0: none)
    var ok = [];
    ch.rows.forEach(function (r, i) { if (partOf(r) === part) ok.push(i); });
    return ok.length ? pick(rng, ok) : -1;
  }
  function keyLine(ch) { return 'Each symbol stands for ' + ch.per + ' ' + ch.what + '.'; }

  function stage1(slot, rng) {
    var per, mode, ch, i, j, r, v, a, b, stem, w, slips, row;
    var cleanPer = [2, 5, 10], halfPer = [4, 6, 10, 20], quarterPer = [4, 8, 20, 40];
    if (slot <= 1) {                                          // read one row: whole symbols
      per = pick(rng, slot === 0 ? cleanPer : [3, 4, 20]);
      ch = picChart(rng, per, 'whole'); i = rint(rng, 0, 4); r = ch.rows[i]; v = val(ch, i);
      stem = 'The pictogram shows the ' + lower(ch.title) + '. ' + keyLine(ch) + ' How many ' + ch.what + ' are shown for ' + r.label + '?';
      w = ['The key says each symbol stands for ' + ch.per + ' ' + ch.what + '.', r.label + ' has ' + sym(wholes(r)) + '.',
        sym(wholes(r)) + ', each ' + ch.per + ': ' + wholes(r) + ' × ' + ch.per + ' = ' + v + '.'];
      return finish(1, slot, 'pic-read', ch, stem, { op: 'read', row: r.label }, num(v), w,
        [slipN('key-ignored', symbols(r), 'You counted the symbols (' + symbols(r) + ') but not what each one stands for. Each symbol is ' + ch.per + ' ' + ch.what + ', so multiply.')]);
    }
    if (slot === 2) {                                         // a half symbol
      per = pick(rng, halfPer); ch = picChart(rng, per, 'half'); i = pickRowWith(rng, ch, 2); r = ch.rows[i]; v = val(ch, i);
      stem = 'The pictogram shows the ' + lower(ch.title) + '. ' + keyLine(ch) + ' How many ' + ch.what + ' are shown for ' + r.label + '?';
      w = ['One whole symbol stands for ' + per + ' ' + ch.what + ', so a half symbol stands for ' + (per / 2) + '.',
        r.label + ' has ' + sym(wholes(r), true) + ' and one half symbol.',
        wholes(r) + ' × ' + per + ' + ' + (per / 2) + ' = ' + v + '.'];
      return finish(1, slot, 'pic-half', ch, stem, { op: 'read', row: r.label }, num(v), w, [
        slipN('half-as-whole', symbols(r) * per, 'You counted the half symbol as a whole one. A half symbol is half of ' + per + ', which is ' + (per / 2) + '.'),
        slipN('half-as-one', wholes(r) * per + 1, 'You counted the half symbol as 1. A half symbol is half of what a whole symbol stands for: ' + (per / 2) + '.'),
        slipN('key-ignored', symbols(r), 'You counted the symbols but did not use the key. Each whole symbol is ' + per + ' ' + ch.what + '.')]);
    }
    if (slot === 3 || slot === 4) {                           // two rows: together, or how many more
      per = pick(rng, halfPer); ch = picChart(rng, per, 'half');
      i = rint(rng, 0, 4); do { j = rint(rng, 0, 4); } while (j === i);
      a = val(ch, i); b = val(ch, j);
      if (slot === 4 && a < b) { var t = i; i = j; j = t; t = a; a = b; b = t; }
      var more = slot === 4;
      stem = 'The pictogram shows the ' + lower(ch.title) + '. ' + keyLine(ch) + (more
        ? ' How many more ' + ch.what + ' are shown for ' + ch.rows[i].label + ' than for ' + ch.rows[j].label + '?'
        : ' How many ' + ch.what + ' are shown for ' + ch.rows[i].label + ' and ' + ch.rows[j].label + ' altogether?');
      var ans = more ? a - b : a + b;
      w = ['Read each row using the key (a half symbol is ' + (per / 2) + '): ' + ch.rows[i].label + ' is ' + a + ' and ' + ch.rows[j].label + ' is ' + b + '.',
        more ? a + ' − ' + b + ' = ' + ans + '.' : a + ' + ' + b + ' = ' + ans + '.'];
      var cnt = more ? symbols(ch.rows[i]) - symbols(ch.rows[j]) : symbols(ch.rows[i]) + symbols(ch.rows[j]);
      return finish(1, slot, more ? 'pic-diff' : 'pic-total2', ch, stem, more ? { op: 'diff', a: ch.rows[i].label, b: ch.rows[j].label } : { op: 'sum', rows: [ch.rows[i].label, ch.rows[j].label] },
        num(ans), w, [slipN('key-ignored', cnt, 'You counted symbols and did not use the key. Each whole symbol is ' + per + ' ' + ch.what + ', and a half is ' + (per / 2) + '.')]);
    }
    if (slot === 5) {                                         // a quarter symbol
      per = pick(rng, quarterPer); ch = picChart(rng, per, 'quarter');
      i = pickRowWith(rng, ch, 1); if (i < 0) { ch.rows[0].q = 4 * wholes(ch.rows[0]) + 1; i = 0; }
      r = ch.rows[i]; v = val(ch, i);
      stem = 'The pictogram shows the ' + lower(ch.title) + '. ' + keyLine(ch) + ' How many ' + ch.what + ' are shown for ' + r.label + '?';
      w = ['One whole symbol stands for ' + per + ' ' + ch.what + ', so a quarter symbol stands for ' + (per / 4) + '.',
        r.label + ' has ' + sym(wholes(r), true) + ' and one quarter symbol.', wholes(r) + ' × ' + per + ' + ' + (per / 4) + ' = ' + v + '.'];
      return finish(1, slot, 'pic-quarter', ch, stem, { op: 'read', row: r.label }, num(v), w, [
        slipN('quarter-as-whole', symbols(r) * per, 'You counted the quarter symbol as a whole one. A quarter symbol is a quarter of ' + per + ', which is ' + (per / 4) + '.'),
        slipN('quarter-as-half', wholes(r) * per + per / 2, 'A quarter symbol is only a quarter of ' + per + ' (' + (per / 4) + '), not a half.'),
        slipN('key-ignored', symbols(r), 'You counted the symbols but did not use the key. Each whole symbol is ' + per + ' ' + ch.what + '.')]);
    }
    if (slot === 6) {                                         // how many symbols to show a number
      per = pick(rng, [4, 10, 20]); ch = picChart(rng, per, 'whole');
      var n = rint(rng, 2, 7), half = rng() < 0.5; v = n * per + (half ? per / 2 : 0);
      stem = 'The pictogram shows the ' + lower(ch.title) + '. ' + keyLine(ch) + ' A new row has ' + v + ' ' + ch.what + '. How many symbols would show it? (A half symbol counts as 0.5.)';
      var syms = v / per;
      w = ['Each symbol stands for ' + per + ' ' + ch.what + '.', 'Divide: ' + v + ' ÷ ' + per + ' = ' + sym(syms) + '.'];
      return finish(1, slot, 'pic-draw', ch, stem, { op: 'draw', value: v }, num(syms), w, [
        slipN('key-ignored', v, 'You typed the number of ' + ch.what + ', not the number of symbols. Divide by what one symbol stands for (' + per + ').'),
        slipN('times-key', v * per, 'To find how many symbols you divide by the key, you do not multiply.')]);
    }
    if (slot === 7) {                                         // all five rows
      per = pick(rng, halfPer); ch = picChart(rng, per, 'half');
      var tot = sum(ch.rows.map(function (r2, k) { return val(ch, k); })), cnt2 = sum(ch.rows.map(symbols));
      stem = 'The pictogram shows the ' + lower(ch.title) + '. ' + keyLine(ch) + ' How many ' + ch.what + ' are shown in all five rows together?';
      w = ['Read each row using the key (a half symbol is ' + (per / 2) + '): ' + ch.rows.map(function (r2, k) { return val(ch, k); }).join(', ') + '.', 'Add them: ' + tot + '.'];
      return finish(1, slot, 'pic-total-all', ch, stem, { op: 'all' }, num(tot), w, [
        slipN('key-ignored', cnt2, 'You counted the symbols and did not use the key. Each whole symbol is ' + per + ' ' + ch.what + '.')]);
    }
    if (slot === 8) {                                         // busiest minus quietest
      per = pick(rng, [2, 4, 10, 20]); ch = picChart(rng, per, 'half');
      var vals = ch.rows.map(function (r2, k) { return val(ch, k); }), hi = idxMax(vals), lo = idxMin(vals);
      if (vals[hi] === vals[lo]) { ch.rows[hi].q += 4; vals = ch.rows.map(function (r2, k) { return val(ch, k); }); hi = idxMax(vals); }
      v = vals[hi] - vals[lo];
      stem = 'The pictogram shows the ' + lower(ch.title) + '. ' + keyLine(ch) + ' How many more ' + ch.what + ' are shown for the busiest row than for the quietest row?';
      w = ['The busiest row is ' + ch.rows[hi].label + ': ' + vals[hi] + '. The quietest is ' + ch.rows[lo].label + ': ' + vals[lo] + '.', vals[hi] + ' − ' + vals[lo] + ' = ' + v + '.'];
      return finish(1, slot, 'pic-range', ch, stem, { op: 'range' }, num(v), w, [
        slipN('key-ignored', symbols(ch.rows[hi]) - symbols(ch.rows[lo]), 'You compared the symbols and did not use the key. Each whole symbol is ' + per + ' ' + ch.what + '.')]);
    }
    if (slot === 9) {                                         // find the key from a row
      per = pick(rng, [2, 3, 4, 5, 10]); ch = picChart(rng, per, 'whole'); ch.keyHidden = true;
      i = rint(rng, 0, 4); ch.rows[i].q = 4 * rint(rng, 2, 5); r = ch.rows[i]; v = val(ch, i);
      stem = 'The pictogram shows the ' + lower(ch.title) + '. The key is missing. The row for ' + r.label + ' has ' + wholes(r) + ' symbols and shows ' + v + ' ' + ch.what + '. How many ' + ch.what + ' does one symbol stand for?';
      w = [r.label + ' has ' + sym(wholes(r)) + ' for ' + v + ' ' + ch.what + '.', 'One symbol is ' + v + ' ÷ ' + wholes(r) + ' = ' + per + '.'];
      return finish(1, slot, 'pic-find-key', ch, stem, { op: 'findkey', row: r.label, value: v }, num(per), w, [
        slipN('key-ignored', v, 'That is the number of ' + ch.what + ' on the whole row. One symbol stands for ' + v + ' ÷ ' + wholes(r) + '.'),
        slipN('times-key', v * wholes(r), 'To find one symbol you divide the total by the number of symbols.')]);
    }
    if (slot === 10) {                                        // a changed key
      per = pick(rng, [2, 5, 10]); ch = picChart(rng, per, 'whole');
      i = rint(rng, 0, 4); ch.rows[i].q = 4 * 2 * rint(rng, 1, 3); r = ch.rows[i]; v = val(ch, i);
      var per2 = per * 2;
      stem = 'The pictogram shows the ' + lower(ch.title) + '. ' + keyLine(ch) + ' The key is changed so that one symbol stands for ' + per2 + ' ' + ch.what + '. How many symbols would ' + r.label + ' need now?';
      w = [r.label + ' has ' + v + ' ' + ch.what + ' (' + sym(wholes(r)) + ' × ' + per + ').', 'With one symbol standing for ' + per2 + ': ' + v + ' ÷ ' + per2 + ' = ' + sym(v / per2) + '.'];
      return finish(1, slot, 'pic-new-key', ch, stem, { op: 'newkey', row: r.label, newPer: per2 }, num(v / per2), w, [
        slipN('key-ignored', wholes(r), 'That is how many symbols it needs with the old key. The new key is bigger, so fewer symbols are needed.'),
        slipN('times-key', v * per2, 'You divide ' + v + ' by the new key (' + per2 + '), you do not multiply.')]);
    }
    // slot 11: three rows with part symbols, added
    per = pick(rng, quarterPer); ch = picChart(rng, per, 'quarter');
    var three = shuffled(rng, [0, 1, 2, 3, 4]).slice(0, 3).sort(), t3 = sum(three.map(function (k) { return val(ch, k); })), c3 = sum(three.map(function (k) { return symbols(ch.rows[k]); }));
    stem = 'The pictogram shows the ' + lower(ch.title) + '. ' + keyLine(ch) + ' How many ' + ch.what + ' are shown for ' + three.map(function (k) { return ch.rows[k].label; }).join(', ').replace(/, ([^,]*)$/, ' and $1') + ' altogether?';
    w = ['A quarter symbol is ' + (per / 4) + ' and a half symbol is ' + (per / 2) + '.', 'The rows are ' + three.map(function (k) { return val(ch, k); }).join(', ') + '.', 'Add them: ' + t3 + '.'];
    return finish(1, slot, 'pic-total3', ch, stem, { op: 'sum', rows: three.map(function (k) { return ch.rows[k].label; }) }, num(t3), w, [
      slipN('key-ignored', c3, 'You counted the symbols and did not use the key. Each whole symbol is ' + per + ' ' + ch.what + '.')]);
  }

  /* =====================================================================================================
     Scales for bar charts and line graphs: { max, minor, major } gridlines every `minor`, a number every `major`.
     Scales in 2s, 5s and 10s.
     ===================================================================================================== */
  function scaleOf(rng, s) {
    if (s === 2) return { max: pick(rng, [20, 30]), minor: 2, major: 10 };
    if (s === 5) return { max: pick(rng, [30, 40, 50]), minor: 5, major: 10 };
    return { max: pick(rng, [60, 70]), minor: 10, major: 10 };
  }

  /* =====================================================================================================
     STAGE 2: bar charts. chart = { type: 'bar', title, yLabel, cats: [{ label, value }], max, minor, major }
       dual:      { type: 'dual', title, yLabel, series: [name, name], cats: [{ label, values: [a, b] }], max, minor, major }
       composite: { type: 'composite', title, yLabel, series: [..2 or 3], cats: [{ label, values: [..] }], max, minor, major }
     ===================================================================================================== */
  var BAR = [
    { title: 'Favourite fruit', noun: 'students', yLabel: 'Number of students', cats: ['Apple', 'Banana', 'Orange', 'Grape', 'Pear'] },
    { title: 'Pets owned by Year 7', noun: 'pets', yLabel: 'Number of pets', cats: ['Dog', 'Cat', 'Fish', 'Rabbit', 'Hamster'] },
    { title: 'How students travel to school', noun: 'students', yLabel: 'Number of students', cats: ['Walk', 'Bus', 'Car', 'Bike', 'Train'] },
    { title: 'Sports played at lunchtime', noun: 'students', yLabel: 'Number of students', cats: ['Football', 'Netball', 'Rugby', 'Tennis', 'Hockey'] },
    { title: 'Books read in a term', noun: 'books', yLabel: 'Number of books', cats: ['Class 7A', 'Class 7B', 'Class 7C', 'Class 7D', 'Class 7E'] },
    { title: 'Drinks sold at the cafe', noun: 'drinks', yLabel: 'Number sold', cats: ['Tea', 'Coffee', 'Milk', 'Juice', 'Water'] }
  ];
  var DUAL = [
    { title: 'Favourite fruit', noun: 'students', yLabel: 'Number of students', series: ['Girls', 'Boys'], cats: ['Apple', 'Banana', 'Orange', 'Grape'] },
    { title: 'Visitors to the museum', noun: 'visitors', yLabel: 'Number of visitors', series: ['This year', 'Last year'], cats: ['Monday', 'Tuesday', 'Wednesday', 'Thursday'] },
    { title: 'Cups of tea sold', noun: 'cups', yLabel: 'Number of cups', series: ['Morning', 'Afternoon'], cats: ['Monday', 'Tuesday', 'Wednesday', 'Thursday'] },
    { title: 'Books borrowed', noun: 'books', yLabel: 'Number of books', series: ['Year 7', 'Year 8'], cats: ['Week 1', 'Week 2', 'Week 3', 'Week 4'] }
  ];
  var STACK = [
    { title: 'How students get to school', noun: 'students', yLabel: 'Number of students', series: ['Walk', 'Bus', 'Car'] },
    { title: 'Books borrowed', noun: 'books', yLabel: 'Number of books', series: ['Fiction', 'Non-fiction', 'Comics'] },
    { title: 'Students in after-school clubs', noun: 'students', yLabel: 'Number of students', series: ['Sport', 'Music', 'Drama'] }
  ];
  var GROUPS = ['Year 7', 'Year 8', 'Year 9', 'Year 10'];

  function barChart(rng, ctx, s, n) {
    var sc = scaleOf(rng, s), vals = distinctMultiples(rng, n, s, sc.max - s, s);
    var cats = ctx.cats.slice(0, n).map(function (l, i) { return { label: l, value: vals[i] }; });
    return { type: 'bar', title: ctx.title, yLabel: ctx.yLabel, noun: ctx.noun, cats: cats, max: sc.max, minor: sc.minor, major: sc.major };
  }
  function dualChart(rng, s) {
    var ctx = pick(rng, DUAL), sc = scaleOf(rng, s), n = 4, cats = [];
    for (var i = 0; i < n; i++) {
      var a = rint(rng, 1, Math.floor((sc.max - s) / s)) * s, b;
      do { b = rint(rng, 1, Math.floor((sc.max - s) / s)) * s; } while (b === a);
      cats.push({ label: ctx.cats[i], values: [a, b] });
    }
    return { type: 'dual', title: ctx.title, yLabel: ctx.yLabel, noun: ctx.noun, series: ctx.series, cats: cats, max: sc.max, minor: sc.minor, major: sc.major };
  }
  function stackChart(rng, s) {
    var ctx = pick(rng, STACK), ser = ctx.series, sc = scaleOf(rng, s), n = 3, cats = [], groups = shuffled(rng, GROUPS).slice(0, n).sort();
    for (var i = 0; i < n; i++) {
      var vals = [];
      for (var k = 0; k < ser.length; k++) vals.push(rint(rng, 1, 3) * s + (s === 2 ? 2 * rint(rng, 0, 1) : 0));
      while (sum(vals) > sc.max - s) { var m = idxMax(vals); vals[m] -= s; }
      cats.push({ label: groups[i], values: vals });
    }
    return { type: 'composite', title: ctx.title, yLabel: ctx.yLabel, noun: ctx.noun, series: ser, cats: cats, max: sc.max, minor: sc.minor, major: sc.major };
  }
  function tolOf(ch) { return ch.minor / 2; }
  function readSlips(ch, v, noun) {
    var m = ch.minor, out = [];
    if (m === 2 || m === 5) {
      out.push(slipN('gridline-high', v + m, 'You read one gridline too high. On this scale each gridline is ' + m + ', so count the gridlines up from the last number.'));
      if (v - m > 0) out.push(slipN('gridline-low', v - m, 'You read one gridline too low. On this scale each gridline is ' + m + ', so count the gridlines up from the last number.'));
    }
    return out;
  }
  // The scale is NOT in the stem: working out what a gridline is worth is part of reading the chart. The working says how.
  function scaleLine(ch) {
    return ch.minor === ch.major ? 'There is a number on every gridline, so each gridline is ' + ch.minor + '.'
      : 'The numbers go up in ' + ch.major + ' with ' + (ch.major / ch.minor) + ' gaps between them, so each gridline is ' + ch.major + ' ÷ ' + (ch.major / ch.minor) + ' = ' + ch.minor + '.';
  }

  function barIntro(ch) { return 'The bar chart shows ' + lower(ch.title) + '. '; }
  function dualIntro(ch) { return 'The bar chart compares ' + lower(ch.series[0]) + ' and ' + lower(ch.series[1]) + ' for ' + lower(ch.title) + '. '; }
  function stackIntro(ch) { return 'The stacked bar chart shows ' + lower(ch.title) + ', split into ' + ch.series.join(', ').replace(/, ([^,]*)$/, ' and $1') + '. '; }

  function stage2(slot, rng) {
    var s = pick(rng, [10, 5, 2]), ch, ctx, i, j, v, w, stem, a, b;
    if (slot === 0) s = 10;
    if (slot === 1) s = 5;
    if (slot === 2) s = 2;
    if (slot <= 2) {                                          // read one bar
      ctx = pick(rng, BAR); ch = barChart(rng, ctx, s, 5); i = rint(rng, 0, 4); v = ch.cats[i].value;
      stem = barIntro(ch) + 'How many ' + ch.noun + ' are shown for ' + ch.cats[i].label + '?';
      w = ['Find the bar for ' + ch.cats[i].label + ' and follow its top across to the scale.', scaleLine(ch), 'The top of the bar is at ' + v + '.'];
      return finish(2, slot, 'bar-read', ch, stem, { op: 'read', cat: ch.cats[i].label }, num(v, tolOf(ch)), w, readSlips(ch, v));
    }
    if (slot === 3 || slot === 4) {                           // two bars: how many more / altogether
      ctx = pick(rng, BAR); ch = barChart(rng, ctx, s, 5); i = rint(rng, 0, 4); do { j = rint(rng, 0, 4); } while (j === i);
      a = ch.cats[i].value; b = ch.cats[j].value;
      if (slot === 3 && a < b) { var t = i; i = j; j = t; t = a; a = b; b = t; }
      var more = slot === 3, ans = more ? a - b : a + b;
      stem = barIntro(ch) + (more
        ? 'How many more ' + ch.noun + ' are shown for ' + ch.cats[i].label + ' than for ' + ch.cats[j].label + '?'
        : 'How many ' + ch.noun + ' are shown for ' + ch.cats[i].label + ' and ' + ch.cats[j].label + ' altogether?');
      w = ['Read both bars: ' + ch.cats[i].label + ' is ' + a + ' and ' + ch.cats[j].label + ' is ' + b + '.', more ? a + ' − ' + b + ' = ' + ans + '.' : a + ' + ' + b + ' = ' + ans + '.'];
      return finish(2, slot, more ? 'bar-diff' : 'bar-total2', ch, stem, more ? { op: 'diff', a: ch.cats[i].label, b: ch.cats[j].label } : { op: 'sum', cats: [ch.cats[i].label, ch.cats[j].label] },
        num(ans), w, more ? [slipN('added', a + b, 'You added the two bars. "How many more" means take the smaller from the larger.')]
          : (ch.minor !== 10 ? [slipN('gridline-high', ans + ch.minor, 'One of your readings was a gridline out. On this scale each gridline is ' + ch.minor + '.')] : []));
    }
    if (slot === 5) {                                         // which is the most
      ctx = pick(rng, BAR); ch = barChart(rng, ctx, s, 5); i = idxMax(ch.cats.map(function (c) { return c.value; }));
      stem = barIntro(ch) + 'Which has the highest bar?';
      var labels = ch.cats.map(function (c) { return c.label; });
      w = ['The highest bar is the tallest one.', 'It is ' + ch.cats[i].label + ' (' + ch.cats[i].value + ').'];
      var low = idxMin(ch.cats.map(function (c) { return c.value; }));
      return finish(2, slot, 'bar-highest', ch, stem, { op: 'highest' }, choiceFixed(labels, labels[i]), w,
        [slipO('lowest-read', labels[low], 'That is the lowest bar. The highest bar is the tallest.')]);
    }
    if (slot === 6 || slot === 7 || slot === 8) {             // dual bars
      ch = dualChart(rng, s); i = rint(rng, 0, 3);
      var sn = rint(rng, 0, 1), other = 1 - sn, nm = ch.series[sn], on = ch.series[other];
      if (slot === 6) {
        v = ch.cats[i].values[sn];
        stem = dualIntro(ch) + 'How many ' + ch.noun + ' does the ' + nm + ' bar show for ' + ch.cats[i].label + '?';
        w = ['Use the key to find the ' + nm + ' bars.', 'The ' + nm + ' bar for ' + ch.cats[i].label + ' reaches ' + v + '.'];
        return finish(2, slot, 'dual-read', ch, stem, { op: 'readS', cat: ch.cats[i].label, series: nm }, num(v, tolOf(ch)), w,
          readSlips(ch, v).concat([slipN('other-series', ch.cats[i].values[other], 'That is the ' + on + ' bar. Check the key for which bar is ' + nm + '.')]));
      }
      if (slot === 7) {
        var big = ch.cats[i].values[0] > ch.cats[i].values[1] ? 0 : 1, sm = 1 - big, d = ch.cats[i].values[big] - ch.cats[i].values[sm];
        stem = dualIntro(ch) + 'For ' + ch.cats[i].label + ', how many more ' + ch.noun + ' does the ' + ch.series[big] + ' bar show than the ' + ch.series[sm] + ' bar?';
        w = ['Read both bars for ' + ch.cats[i].label + ': ' + ch.series[big] + ' ' + ch.cats[i].values[big] + ', ' + ch.series[sm] + ' ' + ch.cats[i].values[sm] + '.', ch.cats[i].values[big] + ' − ' + ch.cats[i].values[sm] + ' = ' + d + '.'];
        return finish(2, slot, 'dual-diff', ch, stem, { op: 'diffS', cat: ch.cats[i].label, more: ch.series[big], less: ch.series[sm] }, num(d), w,
          [slipN('added', ch.cats[i].values[0] + ch.cats[i].values[1], 'You added the two bars. "How many more" means take the smaller from the larger.')]);
      }
      var tot = sum(ch.cats.map(function (c) { return c.values[sn]; }));
      stem = dualIntro(ch) + 'What is the total number of ' + ch.noun + ' shown by the ' + nm + ' bars?';
      w = ['Read the ' + nm + ' bars: ' + ch.cats.map(function (c) { return c.values[sn]; }).join(', ') + '.', 'Add them: ' + tot + '.'];
      return finish(2, slot, 'dual-total', ch, stem, { op: 'sumS', series: nm }, num(tot), w,
        [slipN('other-series', sum(ch.cats.map(function (c) { return c.values[other]; })), 'That is the total for the ' + on + ' bars. Check the key.')]);
    }
    // composite bars
    ch = stackChart(rng, s); i = rint(rng, 0, 2);
    if (slot === 9) {                                         // a segment's length (not the bottom one)
      var sg = rint(rng, 1, ch.series.length - 1), len = ch.cats[i].values[sg], top = sum(ch.cats[i].values.slice(0, sg + 1));
      stem = stackIntro(ch) + 'How many ' + ch.noun + ' are in the ' + ch.series[sg] + ' part of the ' + ch.cats[i].label + ' bar?';
      w = ['The ' + ch.series[sg] + ' part sits on top of the parts below it.', 'Its bottom edge is at ' + (top - len) + ' and its top edge is at ' + top + '.', 'Its length is ' + top + ' − ' + (top - len) + ' = ' + len + '.'];
      return finish(2, slot, 'stack-segment', ch, stem, { op: 'seg', cat: ch.cats[i].label, seg: ch.series[sg] }, num(len, tolOf(ch)), w,
        [slipN('segment-top', top, 'You read the top of the part. The part is only as long as the gap between its bottom edge and its top edge.')]);
    }
    if (slot === 10) {                                        // the whole bar
      var totb = sum(ch.cats[i].values);
      stem = stackIntro(ch) + 'How many ' + ch.noun + ' are there in total in the ' + ch.cats[i].label + ' bar?';
      w = ['The total is the height of the whole bar, to its top edge.', 'The ' + ch.cats[i].label + ' bar reaches ' + totb + '.'];
      return finish(2, slot, 'stack-total', ch, stem, { op: 'total', cat: ch.cats[i].label }, num(totb, tolOf(ch)), w,
        [slipN('segment-top', ch.cats[i].values[ch.series.length - 1], 'That is just the top part. The total is the height of the whole bar.')]);
    }
    // slot 11: one part in two bars, the difference (the two parts differ)
    var sg2 = rint(rng, 1, ch.series.length - 1);
    for (var tryN = 0; tryN < 50 && ch.cats[0].values[sg2] === ch.cats[1].values[sg2]; tryN++) ch = stackChart(rng, s);
    i = 0; j = 1;
    a = ch.cats[i].values[sg2]; b = ch.cats[j].values[sg2];
    if (a < b) { i = 1; j = 0; var t2 = a; a = b; b = t2; }
    var dd = a - b;
    stem = stackIntro(ch) + 'How many more ' + ch.noun + ' are in the ' + ch.series[sg2] + ' part of the ' + ch.cats[i].label + ' bar than in the ' + ch.series[sg2] + ' part of the ' + ch.cats[j].label + ' bar?';
    w = ['Find the length of each ' + ch.series[sg2] + ' part: ' + ch.cats[i].label + ' is ' + a + ' and ' + ch.cats[j].label + ' is ' + b + '.', a + ' − ' + b + ' = ' + dd + '.'];
    var topA = sum(ch.cats[i].values.slice(0, sg2 + 1)), topB = sum(ch.cats[j].values.slice(0, sg2 + 1));
    return finish(2, slot, 'stack-diff', ch, stem, { op: 'segdiff', cats: [ch.cats[i].label, ch.cats[j].label], seg: ch.series[sg2] }, num(dd), w,
      [slipN('segment-top', Math.abs(topA - topB), 'You compared the tops of the parts. Each part is only as long as its own length.')]);
  }

  /* =====================================================================================================
     STAGE 3: line graphs and time series. chart = { type: 'line', title, xLabel, yLabel, points: [{ label, value }], mids,
       max, minor, major }. mids[k] names a time between point k and point k + 1 (where nothing was measured).
     ===================================================================================================== */
  var LINE = [
    { title: 'Temperature during the day', xLabel: 'Time', yLabel: 'Temperature (°C)', unit: '°C', what: 'the temperature',
      labels: ['6am', '9am', '12pm', '3pm', '6pm', '9pm'], mids: ['7:30am', '10:30am', '1:30pm', '4:30pm', '7:30pm'], lo: 4 },
    { title: 'Money saved', xLabel: 'Month (end of month)', yLabel: 'Savings (£)', unit: '£', what: 'the savings',
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], mids: ['mid-February', 'mid-March', 'mid-April', 'mid-May', 'mid-June'], lo: 0 },
    { title: 'Visitors in the park', xLabel: 'Time', yLabel: 'Number of visitors', unit: ' visitors', what: 'the number of visitors',
      labels: ['10am', '12pm', '2pm', '4pm', '6pm', '8pm'], mids: ['11am', '1pm', '3pm', '5pm', '7pm'], lo: 0 },
    { title: 'Water in the tank', xLabel: 'Day', yLabel: 'Water (litres)', unit: ' litres', what: 'the water in the tank',
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], mids: ['Monday evening', 'Tuesday evening', 'Wednesday evening', 'Thursday evening', 'Friday evening'], lo: 0 },
    { title: 'Height of a plant', xLabel: 'Week', yLabel: 'Height (cm)', unit: ' cm', what: 'the height of the plant',
      labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6'], mids: ['half way between Week 1 and Week 2', 'half way between Week 2 and Week 3', 'half way between Week 3 and Week 4', 'half way between Week 4 and Week 5', 'half way between Week 5 and Week 6'], lo: 0 }
  ];
  function lineChart(rng, s, shape) {
    var ctx = pick(rng, LINE), sc = scaleOf(rng, s), vals = [], n = ctx.labels.length, lo = 2 * s, hi = sc.max - s, k, v;
    // shape: 'any' (a wandering line, no two neighbours equal), 'up' (rising, never level)
    var steps = Math.floor((hi - lo) / s);
    v = rint(rng, 0, Math.floor(steps / 3)) * s + lo;
    for (k = 0; k < n; k++) {
      vals.push(v);
      var d = 0;
      for (var tries = 0; tries < 20; tries++) {
        d = (shape === 'up' ? rint(rng, 1, 2) : rint(rng, -2, 2)) * s;
        if (d === 0) continue;
        if (v + d >= lo && v + d <= hi) break;
        d = 0;
      }
      if (d === 0) d = (v + s <= hi) ? s : -s;
      v += d;
    }
    return { type: 'line', title: ctx.title, xLabel: ctx.xLabel, yLabel: ctx.yLabel, unit: ctx.unit, what: ctx.what, mids: ctx.mids,
      points: ctx.labels.map(function (l, i) { return { label: l, value: vals[i] }; }), max: sc.max, minor: sc.minor, major: sc.major };
  }
  function lineUntil(rng, s, shape, ok) {
    var ch, n = 0;
    do { ch = lineChart(rng, s, shape); n++; } while (!ok(ch.points.map(function (p) { return p.value; })) && n < 400);
    return ch;
  }
  function lineStem(ch) { return 'The line graph shows ' + lower(ch.title) + '. '; }
  function withUnit(ch, v) { return ch.unit.charAt(0) === ' ' ? v + ch.unit : (ch.unit === '£' ? '£' + v : v + ch.unit); }

  function stage3(slot, rng) {
    var s = pick(rng, [10, 5, 2]), ch, i, j, k, v, w, stem, ans, pts;
    if (slot === 0) s = 10;
    if (slot === 1) s = 5;
    if (slot === 2) s = 2;
    ch = slot === 5 ? lineChart(rng, s, 'up')
      : lineUntil(rng, s, 'any', slot === 4 ? function (v) { return v.filter(function (x) { return x === Math.max.apply(null, v); }).length === 1; }
        : (slot === 8 ? function (v) { var d = []; for (var k = 0; k < 5; k++) d.push(v[k + 1] - v[k]); var m = Math.max.apply(null, d); return m > 0 && d.filter(function (x) { return x === m; }).length === 1; }
        : (slot === 3 ? function (v) { return v[0] !== v[3] || v[1] !== v[4] || v[2] !== v[5]; } : function () { return true; })));
    pts = ch.points;
    var vals = pts.map(function (p) { return p.value; });
    if (slot <= 2) {                                          // read a value at a labelled time
      i = rint(rng, 0, 5); v = vals[i];
      stem = lineStem(ch) + 'What is the reading at ' + pts[i].label + '?';
      w = ['Find ' + pts[i].label + ' on the bottom axis and go up to the line.', 'Go across to the scale: ' + scaleLine(ch), 'The reading is ' + v + '.'];
      return finish(3, slot, 'line-read', ch, stem, { op: 'read', pt: pts[i].label }, num(v, tolOf(ch)), w, readSlips(ch, v));
    }
    if (slot === 3) {                                         // change between two readings
      var cands = [];
      for (i = 0; i < 3; i++) for (j = 3; j < 6; j++) if (vals[i] !== vals[j]) cands.push([i, j]);
      var cj = pick(rng, cands); i = cj[0]; j = cj[1];
      var rise = vals[j] > vals[i], dv = Math.abs(vals[j] - vals[i]);
      stem = lineStem(ch) + 'By how much did it ' + (rise ? 'rise' : 'fall') + ' from ' + pts[i].label + ' to ' + pts[j].label + '?';
      w = ['Read both points: ' + pts[i].label + ' is ' + vals[i] + ' and ' + pts[j].label + ' is ' + vals[j] + '.', 'The change is ' + Math.max(vals[i], vals[j]) + ' − ' + Math.min(vals[i], vals[j]) + ' = ' + dv + '.'];
      return finish(3, slot, 'line-change', ch, stem, { op: 'change', from: pts[i].label, to: pts[j].label, dir: rise ? 'rise' : 'fall' }, num(dv), w,
        [slipN('end-value', vals[j], 'That is the reading at ' + pts[j].label + '. The change is the difference between the two readings.')]);
    }
    if (slot === 4) {                                         // when was it highest
      i = idxMax(vals);
      stem = lineStem(ch) + 'When was the reading highest?';
      var labs = pts.map(function (p) { return p.label; }), lo2 = idxMin(vals);
      w = ['The highest point on the line is the peak.', 'It is at ' + pts[i].label + ' (' + vals[i] + ').'];
      return finish(3, slot, 'line-peak', ch, stem, { op: 'peak' }, choiceFixed(labs, labs[i]), w,
        [slipO('lowest-read', labs[lo2], 'That is where the line is lowest. The highest reading is the peak.')]);
    }
    if (slot === 5) {                                         // trend: the line only goes up here
      stem = lineStem(ch) + 'What is the trend from ' + pts[0].label + ' to ' + pts[5].label + '?';
      var opts = ['It goes up overall', 'It goes down overall', 'It stays about the same'];
      w = ['Compare the first and last readings: ' + vals[0] + ' then ' + vals[5] + '.', 'The readings are higher at the end, so the trend is upward.'];
      return finish(3, slot, 'line-trend', ch, stem, { op: 'trend', from: pts[0].label, to: pts[5].label }, choiceFixed(opts, opts[0]), w,
        [slipO('trend-reversed', opts[1], 'Look at the first and last readings. The last is higher than the first, so the trend is upward.')]);
    }
    if (slot === 6) {                                         // can you tell between the readings?
      k = rint(rng, 0, 4); var thr = Math.round((vals[k] + vals[k + 1]) / 2 / s) * s;
      stem = lineStem(ch) + 'Readings were taken only at the times marked. Was the reading above ' + withUnit(ch, thr) + ' at ' + ch.mids[k] + '?';
      var o3 = ['Yes', 'No', CANT];
      w = ['There are readings at ' + pts[k].label + ' and ' + pts[k + 1].label + ', but none at ' + ch.mids[k] + '.', 'The line joins the points, but nothing was measured in between, so the graph cannot tell you.'];
      return finish(3, slot, 'line-between', ch, stem, { op: 'between', k: k, thr: thr }, choiceFixed(o3, CANT), w, [
        slipO('join-the-dots', vals[k] + vals[k + 1] > 2 * thr ? 'Yes' : 'No', 'The line between the points is only a join; nothing was measured at ' + ch.mids[k] + '. You cannot tell.')]);
    }
    if (slot === 7) {                                         // higher at one time than another: it can be told
      i = rint(rng, 0, 2); j = rint(rng, 3, 5);
      var yes = vals[i] > vals[j];
      stem = lineStem(ch) + 'Was the reading higher at ' + pts[i].label + ' than at ' + pts[j].label + '?';
      var o4 = ['Yes', 'No', CANT];
      w = ['Read both marked points: ' + pts[i].label + ' is ' + vals[i] + ' and ' + pts[j].label + ' is ' + vals[j] + '.', 'Both were measured, so you can tell: ' + (yes ? 'yes' : 'no') + '.'];
      return finish(3, slot, 'line-compare', ch, stem, { op: 'compare', a: pts[i].label, b: pts[j].label }, choiceFixed(o4, yes ? 'Yes' : 'No'), w,
        [slipO('cant-tell-overused', CANT, 'Both of those times are marked points on the graph, so both were measured. You can tell.')]);
    }
    if (slot === 8) {                                         // the biggest rise between neighbouring readings
      var best = 0, bi = -1;
      for (k = 0; k < 5; k++) if (vals[k + 1] - vals[k] > best) { best = vals[k + 1] - vals[k]; bi = k; }
      var ivs = []; for (k = 0; k < 5; k++) ivs.push('Between ' + pts[k].label + ' and ' + pts[k + 1].label);
      stem = lineStem(ch) + 'Between which two neighbouring readings was the biggest rise?';
      w = ['Look for the steepest part of the line going up.', 'The rises are ' + ivs.map(function (t, q) { return Math.max(vals[q + 1] - vals[q], 0); }).join(', ') + '.', 'The biggest rise is ' + lower(ivs[bi]) + '.'];
      var pk = idxMax(vals), alt = ivs[Math.max(0, Math.min(4, pk))];
      var sl = alt !== ivs[bi] ? [slipO('highest-not-steepest', alt, 'The highest point is not the same as the steepest rise. Look for the biggest jump up between neighbouring points.')] : [];
      return finish(3, slot, 'line-steepest', ch, stem, { op: 'steepest' }, choiceFixed(ivs, ivs[bi]), w, sl);
    }
    if (slot === 9) {                                         // a value at an unmeasured time: you can't tell
      k = rint(rng, 0, 4);
      stem = lineStem(ch) + 'Readings were taken only at the times marked. What was the reading at ' + ch.mids[k] + '?';
      var mid = (vals[k] + vals[k + 1]) / 2, mo = ['Exactly ' + mid, 'Exactly ' + vals[k], 'Exactly ' + vals[k + 1], CANT];
      w = ['Readings exist at ' + pts[k].label + ' (' + vals[k] + ') and ' + pts[k + 1].label + ' (' + vals[k + 1] + '), but not at ' + ch.mids[k] + '.', 'You can estimate, but you cannot tell exactly.'];
      return finish(3, slot, 'line-estimate', ch, stem, { op: 'unmeasured', k: k }, choiceFixed(mo, CANT), w,
        [slipO('join-the-dots', mo[0], 'Half way between the readings is only a guess. Nothing was measured at ' + ch.mids[k] + ', so you cannot tell exactly.')]);
    }
    if (slot === 10) {                                        // range
      i = idxMax(vals); j = idxMin(vals); ans = vals[i] - vals[j];
      stem = lineStem(ch) + 'What is the difference between the highest and the lowest reading?';
      w = ['The highest reading is ' + vals[i] + ' and the lowest is ' + vals[j] + '.', vals[i] + ' − ' + vals[j] + ' = ' + ans + '.'];
      return finish(3, slot, 'line-range', ch, stem, { op: 'range' }, num(ans), w, [slipN('highest-only', vals[i], 'That is the highest reading. The difference is the highest take away the lowest.')]);
    }
    // slot 11: still: was it ever above a value? Only the marked readings can be told
    var maxv = vals[idxMax(vals)], thr2 = Math.floor((maxv - s) / s) * s;
    var ab = vals.filter(function (x) { return x > thr2; }).length;
    stem = lineStem(ch) + 'Readings were taken only at the times marked. Was any marked reading above ' + withUnit(ch, thr2) + '?';
    var o5 = ['Yes', 'No', CANT];
    w = ['Check each marked reading: the highest is ' + maxv + '.', maxv + ' is above ' + thr2 + ', so yes.'];
    return finish(3, slot, 'line-any-above', ch, stem, { op: 'anyAbove', thr: thr2 }, choiceFixed(o5, 'Yes'), w,
      [slipO('cant-tell-overused', CANT, 'The marked readings were measured, so you can tell. Look at them.'), slipO('no-reading', 'No', 'The highest marked reading is ' + maxv + ', which is above ' + thr2 + '.')]);
  }

  /* =====================================================================================================
     STAGE 4: scatter graphs. chart = { type: 'scatter', title, xLabel, yLabel, xMax, yMax, xMajor, yMajor, xMinor, yMinor,
       points: [{ x, y, tag }], line: { c, m } | null, dataMax }. A tag is a letter on a point (outlier questions).
     ===================================================================================================== */
  var SC = [
    { sign: 1, title: 'Revision and test scores', xLabel: 'Hours of revision', yLabel: 'Test score', xMax: 10, yMax: 100, xMajor: 2, yMajor: 20, xMinor: 1, yMinor: 5 },
    { sign: 1, title: 'Temperature and ice creams', xLabel: 'Temperature (°C)', yLabel: 'Ice creams sold', xMax: 30, yMax: 60, xMajor: 10, yMajor: 10, xMinor: 2, yMinor: 2 },
    { sign: 1, title: 'Age and height of children', xLabel: 'Age (years)', yLabel: 'Height (cm)', xMax: 10, yMax: 150, xMajor: 2, yMajor: 30, xMinor: 1, yMinor: 5 },
    { sign: 1, title: 'Practice and goals', xLabel: 'Hours of practice', yLabel: 'Goals scored', xMax: 10, yMax: 20, xMajor: 2, yMajor: 5, xMinor: 1, yMinor: 1 },
    { sign: -1, title: 'Temperature and hot drinks', xLabel: 'Temperature (°C)', yLabel: 'Hot drinks sold', xMax: 30, yMax: 60, xMajor: 10, yMajor: 10, xMinor: 2, yMinor: 2 },
    { sign: -1, title: 'Age and value of a car', xLabel: 'Age (years)', yLabel: 'Value (£100s)', xMax: 10, yMax: 100, xMajor: 2, yMajor: 20, xMinor: 1, yMinor: 5 },
    { sign: -1, title: 'Price and number sold', xLabel: 'Price (£)', yLabel: 'Number sold', xMax: 10, yMax: 100, xMajor: 2, yMajor: 20, xMinor: 1, yMinor: 5 },
    { sign: -1, title: 'Distance and journey time', xLabel: 'Speed (mph)', yLabel: 'Time taken (minutes)', xMax: 60, yMax: 120, xMajor: 20, yMajor: 20, xMinor: 5, yMinor: 5 },
    { sign: 0, title: 'Shoe size and test score', xLabel: 'Shoe size', yLabel: 'Test score', xMax: 10, yMax: 100, xMajor: 2, yMajor: 20, xMinor: 1, yMinor: 5 },
    { sign: 0, title: 'Height and number of pets', xLabel: 'Height (cm)', yLabel: 'Pets owned', xMax: 20, yMax: 10, xMajor: 5, yMajor: 2, xMinor: 1, yMinor: 1 }
  ];
  function pearson(pts) {
    var n = pts.length, mx = sum(pts.map(function (p) { return p.x; })) / n, my = sum(pts.map(function (p) { return p.y; })) / n, sxy = 0, sxx = 0, syy = 0;
    pts.forEach(function (p) { sxy += (p.x - mx) * (p.y - my); sxx += (p.x - mx) * (p.x - mx); syy += (p.y - my) * (p.y - my); });
    return sxy / Math.sqrt(sxx * syy);
  }
  function ctxFor(rng, sign) { return pick(rng, SC.filter(function (c) { return c.sign === sign; })); }
  // A scatter graph for a context: 'strong' (|r| >= 0.9), 'weak' (0.5..0.75) or 'none' (|r| < 0.2). Points on whole units of x
  // and y; the line of best fit has whole-number c and m and passes through the middle of the points.
  function scatterChart(rng, ctx, strength, withLine, maxPoints) {
    var X = ctx.xMax, Y = ctx.yMax, sgn = ctx.sign || 1, pts, r, tries, m, c, n = 12;
    for (tries = 0; tries < 400; tries++) {
      var span = strength === 'none' ? 0 : (strength === 'strong' ? 0.07 : 0.2) * Y;
      // a whole-number gradient that carries the line across about two thirds of the height over the data
      var xs = [], x0 = Math.max(1, Math.round(X * 0.08)), x1 = Math.round(X * (maxPoints || 0.92));
      m = Math.max(1, Math.round(0.65 * Y / X));
      if (m * X > 0.8 * Y) m = Math.max(1, Math.floor(0.8 * Y / X));
      c = sgn > 0 ? Math.round(Y * (0.08 + 0.18 * rng()) / ctx.yMinor) * ctx.yMinor : Math.round(Y * (0.8 + 0.1 * rng()) / ctx.yMinor) * ctx.yMinor;
      if (sgn < 0) m = Math.max(1, Math.round(0.7 * c / X));
      if (m * X > 0.9 * Y && sgn > 0) m = Math.floor(0.8 * Y / X);
      for (var k = 0; k < n; k++) xs.push(Math.max(x0, Math.min(x1, Math.round(x0 + (x1 - x0) * (k + rng() * 0.8) / n))));
      pts = xs.map(function (x) {
        var y;
        if (strength === 'none') y = Math.round(Y * (0.1 + 0.8 * rng()));
        else y = Math.round(c + sgn * m * x + (rng() * 2 - 1) * span);
        return { x: x, y: Math.max(1, Math.min(Y - 1, y)) };
      });
      r = pearson(pts);
      var seenXY = {}, dup = false;
      pts.forEach(function (p) { var kk = p.x + ',' + p.y; if (seenXY[kk]) dup = true; seenXY[kk] = 1; });
      if (dup) continue;
      if (strength === 'strong' && Math.abs(r) >= 0.9 && Math.sign(r) === sgn) break;
      if (strength === 'weak' && Math.abs(r) >= 0.5 && Math.abs(r) <= 0.75 && Math.sign(r) === sgn) break;
      if (strength === 'none' && Math.abs(r) < 0.2) break;
    }
    return { type: 'scatter', title: ctx.title, xLabel: ctx.xLabel, yLabel: ctx.yLabel, xMax: X, yMax: Y, xMajor: ctx.xMajor, yMajor: ctx.yMajor,
      xMinor: ctx.xMinor, yMinor: ctx.yMinor, points: pts, line: strength === 'none' ? null : { c: c, m: sgn * m }, dataMax: x1, sign: sgn, r: r };
  }
  function lineY(ch, x) { return ch.line.c + ch.line.m * x; }
  var TYPE3 = ['Positive correlation: as one goes up, so does the other', 'Negative correlation: as one goes up, the other goes down', 'No correlation: no pattern in the points'];

  var CAUSE = [
    { sign: 1, x: 'ice cream sales', y: 'sunburn cases', other: 'hot weather', xl: 'Ice cream sales', yl: 'Sunburn cases' },
    { sign: 1, x: "children's shoe size", y: 'reading score', other: 'age', xl: 'Shoe size', yl: 'Reading score' },
    { sign: 1, x: 'firefighters at a fire', y: 'damage caused', other: 'the size of the fire', xl: 'Firefighters', yl: 'Damage (£1000s)' },
    { sign: 1, x: 'sun cream sold', y: 'sunglasses sold', other: 'sunny weather', xl: 'Sun cream sold', yl: 'Sunglasses sold' },
    { sign: 1, x: 'books at home', y: 'test score', other: 'how much the family reads', xl: 'Books at home', yl: 'Test score' },
    { sign: -1, x: 'heating bills', y: 'ice cream sales', other: 'the outside temperature', xl: 'Heating bill (£)', yl: 'Ice creams sold' },
    { sign: -1, x: 'umbrellas sold', y: 'sunglasses sold', other: 'the weather', xl: 'Umbrellas sold', yl: 'Sunglasses sold' }
  ];

  function stage4(slot, rng) {
    var ctx, ch, w, stem, v, i, x, y, sgn, strength, o, opts;
    if (slot <= 2) {                                          // type of correlation
      sgn = [1, -1, 0][slot]; ctx = ctxFor(rng, sgn); ch = scatterChart(rng, ctx, sgn === 0 ? 'none' : 'strong', false);
      var right = TYPE3[sgn === 1 ? 0 : (sgn === -1 ? 1 : 2)];
      stem = 'The scatter graph shows ' + lower(ctx.title) + '. What type of correlation does it show?';
      w = [sgn === 0 ? 'The points are scattered with no pattern.' : (sgn === 1 ? 'The points go up from left to right.' : 'The points go down from left to right.'), 'This is ' + lower(right.split(':')[0]) + '.'];
      return finish(4, slot, 'scatter-type', ch, stem, { op: 'corr' }, choiceFixed(TYPE3, right), w,
        [slipO('type-reversed', TYPE3[sgn === 1 ? 1 : 0], 'Check the direction. ' + (sgn === 1 ? 'The points rise from left to right, so as one goes up the other goes up too.' : 'The points fall from left to right, so as one goes up the other goes down.'))]);
    }
    if (slot === 3) {                                         // strength too
      sgn = pick(rng, [1, -1]); strength = pick(rng, ['strong', 'weak']); ctx = ctxFor(rng, sgn); ch = scatterChart(rng, ctx, strength, false);
      var T = ['Strong positive correlation', 'Weak positive correlation', 'Strong negative correlation', 'Weak negative correlation'];
      var rt = (strength === 'strong' ? 'Strong ' : 'Weak ') + (sgn === 1 ? 'positive' : 'negative') + ' correlation';
      stem = 'The scatter graph shows ' + lower(ctx.title) + '. Which description fits it best?';
      w = ['The points ' + (sgn === 1 ? 'rise' : 'fall') + ' from left to right: ' + (sgn === 1 ? 'positive' : 'negative') + '.', strength === 'strong' ? 'They lie close to a straight line: strong.' : 'They are spread out around a line: weak.'];
      var opp = (strength === 'strong' ? 'Weak ' : 'Strong ') + (sgn === 1 ? 'positive' : 'negative') + ' correlation';
      return finish(4, slot, 'scatter-strength', ch, stem, { op: 'corr' }, choiceFixed(T, rt), w, [slipO('strength-wrong', opp, 'Look at how close the points are to a line. Close together means strong; spread out means weak.')]);
    }
    if (slot === 4 || slot === 5 || slot === 11) {            // estimate from the line of best fit
      sgn = pick(rng, [1, -1]); ctx = ctxFor(rng, sgn); ch = scatterChart(rng, ctx, 'strong', true);
      if (slot === 5) {                                       // x from y
        var xq = rint(rng, Math.max(2, Math.round(ch.xMax * 0.2)), Math.round(ch.dataMax - 1)); xq = Math.round(xq / ch.xMinor) * ch.xMinor;
        if (xq < 1 || xq > ch.dataMax) xq = Math.round(ch.dataMax / 2);
        y = lineY(ch, xq);
        stem = 'The line of best fit is drawn on the scatter graph of ' + lower(ctx.title) + '. Use the line to estimate the ' + lower(ctx.xLabel) + ' when the ' + lower(ctx.yLabel) + ' is ' + y + '.';
        w = ['Find ' + y + ' on the up axis and go across to the line.', 'Then go down to the bottom axis.', 'The line is at ' + xq + '.'];
        return finish(4, slot, 'scatter-estimate-x', ch, stem, { op: 'estx', y: y }, num(xq, ch.xMinor / 2), w,
          [slipN('axes-swapped', y, 'That is the number you were given. You need the other axis: go from ' + y + ' across to the line, then down.')]);
      }
      if (slot === 11) {                                      // how much y changes per 1 of x
        stem = 'The line of best fit is drawn on the scatter graph of ' + lower(ctx.title) + '. The line ' + (ch.line.m > 0 ? 'rises' : 'falls') + ' by the same amount for each extra 1 of ' + lower(ctx.xLabel) + '. By about how much does the ' + lower(ctx.yLabel) + ' ' + (ch.line.m > 0 ? 'rise' : 'fall') + ' for each extra 1?';
        var m = Math.abs(ch.line.m);
        w = ['Pick two points on the line and see how far it goes up (or down) for 1 across.', 'It ' + (ch.line.m > 0 ? 'rises' : 'falls') + ' ' + m + ' for each 1 across.'];
        return finish(4, slot, 'scatter-gradient', ch, stem, { op: 'gradient' }, num(m), w,
          [slipN('wrong-sign-read', lineY(ch, 0), 'That is where the line meets the up axis. The question asks how much it changes for each extra 1 across.')]);
      }
      x = rint(rng, Math.max(2, Math.round(ch.xMax * 0.2)), Math.round(ch.dataMax - 1)); x = Math.round(x / ch.xMinor) * ch.xMinor; if (x < 1) x = ch.xMinor;
      v = lineY(ch, x);
      stem = 'The line of best fit is drawn on the scatter graph of ' + lower(ctx.title) + '. Use the line to estimate the ' + lower(ctx.yLabel) + ' when the ' + lower(ctx.xLabel) + ' is ' + x + '.';
      w = ['Find ' + x + ' on the bottom axis and go up to the line.', 'Then go across to the up axis.', 'The line is at ' + v + '.'];
      return finish(4, slot, 'scatter-estimate-y', ch, stem, { op: 'esty', x: x }, num(v, ch.yMinor / 2), w, [
        slipN('axes-swapped', x, 'That is the number you were given. You need the other axis: go from ' + x + ' up to the line, then across.')]);
    }
    if (slot === 6 || slot === 7) {                           // an outlier
      sgn = pick(rng, [1, -1]); ctx = ctxFor(rng, sgn); ch = scatterChart(rng, ctx, 'strong', true);
      // move one point well away from the line, then label four points
      var k = rint(rng, 3, 8), p = ch.points[k], off = Math.round(ch.yMax * 0.3);
      var target = lineY(ch, p.x) + (lineY(ch, p.x) + off <= ch.yMax - 5 ? off : -off);
      p.y = Math.max(2, Math.min(ch.yMax - 2, target));
      var tags = [k], sep = Math.max(2, ch.xMax * 0.16), order = shuffled(rng, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11].filter(function (z) { return z !== k; }));
      while (tags.length < 4 && sep >= 1) {
        order.forEach(function (z) {
          if (tags.length < 4 && tags.indexOf(z) < 0 && tags.every(function (y) { return Math.abs(ch.points[z].x - ch.points[y].x) >= sep; })) tags.push(z);
        });
        sep -= 1;
      }
      var letters = ['A', 'B', 'C', 'D'], ord = tags.slice().sort(function (a, b) { return ch.points[a].x - ch.points[b].x; });
      ord.forEach(function (z, q) { ch.points[z].tag = letters[q]; });
      if (slot === 6) {
        stem = 'The scatter graph shows ' + lower(ctx.title) + '. One of the labelled points is an outlier. Which one?';
        w = ['An outlier is a point that does not fit the pattern of the others.', 'Point ' + p.tag + ' is far from the line.'];
        var near = ord.filter(function (z) { return z !== k; });
        return finish(4, slot, 'scatter-outlier', ch, stem, { op: 'outlier' }, choiceFixed(letters, p.tag), w,
          [slipO('not-outlier', ch.points[near[0]].tag, 'That point is close to the line of best fit, so it fits the pattern. The outlier is the one far from the pattern.')]);
      }
      stem = 'The scatter graph shows ' + lower(ctx.title) + '. One point is an outlier. What is its ' + lower(ctx.yLabel) + ' (the up axis reading)?';
      w = ['The outlier is the point far from the others, at ' + p.x + ' across.', 'Go across to the up axis: ' + p.y + '.'];
      return finish(4, slot, 'scatter-outlier-value', ch, stem, { op: 'outlierY' }, num(p.y, ch.yMinor / 2), w,
        [slipN('axes-swapped', p.x, 'That is the reading on the bottom axis. The question asks for the up axis.')]);
    }
    if (slot === 8) {                                         // correlation is not cause
      var cs = pick(rng, CAUSE); ctx = { sign: cs.sign, title: cs.xl + ' and ' + lower(cs.yl), xLabel: cs.xl, yLabel: cs.yl, xMax: 10, yMax: 100, xMajor: 2, yMajor: 20, xMinor: 1, yMinor: 5 };
      ch = scatterChart(rng, ctx, 'strong', false);
      stem = 'The scatter graph shows a strong ' + (cs.sign === 1 ? 'positive' : 'negative') + ' correlation between ' + cs.x + ' and ' + cs.y + '. Someone says that changes in ' + cs.x + ' cause the changes in ' + cs.y + '. What is the best reply?';
      var good = 'Correlation does not show cause: ' + cs.other + ' could explain both';
      o = choice(rng, good, ['Yes, the strong correlation shows one causes the other', 'Yes, because the points are close to a line', 'No, because there is no correlation']);
      w = ['A correlation means the two go together. It does not show that one causes the other.', 'Something else, such as ' + cs.other + ', could cause both.'];
      return finish(4, slot, 'scatter-cause', ch, stem, { op: 'cause', sign: cs.sign }, o, w, [
        slipO('correlation-as-cause', 'Yes, the strong correlation shows one causes the other', 'A strong correlation shows the two go together, not that one causes the other.')]);
    }
    if (slot === 9) {                                         // estimating beyond the data
      sgn = pick(rng, [1, -1]); ctx = ctxFor(rng, sgn); ch = scatterChart(rng, ctx, 'strong', true, 0.65);
      var xb = Math.round(ch.xMax * 0.9 / ch.xMinor) * ch.xMinor; var yb = lineY(ch, xb);
      if (yb <= 0 || yb >= ch.yMax) { ch.dataMax = Math.round(ch.xMax * 0.5); xb = Math.round(ch.xMax * 0.8); yb = lineY(ch, xb); }
      stem = 'The line of best fit is drawn on the scatter graph of ' + lower(ctx.title) + '. The points only go up to ' + ch.dataMax + ' on the bottom axis. A student uses the line to estimate the ' + lower(ctx.yLabel) + ' when the ' + lower(ctx.xLabel) + ' is ' + xb + '. Is the estimate reliable?';
      var bad = 'Yes: the line gives ' + yb, ok = 'No: ' + xb + ' is outside the data, so the line may not hold';
      o = choiceFixed([bad, ok, 'Yes: the correlation is strong', CANT], ok);
      w = ['The points stop at ' + ch.dataMax + '. The line is only trusted inside the data.', xb + ' is beyond ' + ch.dataMax + ', so the estimate is not reliable.'];
      return finish(4, slot, 'scatter-beyond', ch, stem, { op: 'beyond', x: xb }, o, w,
        [slipO('beyond-the-data', bad, 'The line is only reliable between the smallest and largest values of the data. ' + xb + ' is outside it.'), slipO('strong-so-reliable', 'Yes: the correlation is strong', 'A strong correlation inside the data does not make an estimate outside the data reliable.')]);
    }
    // slot 10: the same trend for another group? you can't tell
    sgn = pick(rng, [1, -1]); ctx = ctxFor(rng, sgn); ch = scatterChart(rng, ctx, 'strong', true);
    var groups = ['adults', 'another school', 'other countries', 'last year'];
    var g = pick(rng, groups);
    stem = 'The scatter graph shows ' + lower(ctx.title) + ' for one class. Does the graph tell you the same pattern is true for ' + g + '?';
    var os = ['Yes, because the correlation is strong', 'No, the pattern is the opposite', CANT];
    w = ['The graph only shows the class that was measured.', 'It does not tell you about ' + g + '. You can’t tell.'];
    return finish(4, slot, 'scatter-generalise', ch, stem, { op: 'generalise' }, choiceFixed(os, CANT), w,
      [slipO('strong-so-always', os[0], 'The correlation is only for the class that was measured. It does not tell you about ' + g + '.')]);
  }

  /* =====================================================================================================
     STAGE 5: is this chart lying? chart = { type: 'lying', form: 'bar' | 'line' | 'pics', title (or null), yLabel (or null),
       xLabel (or null), items: [{ label, value }], yStart, ticks: [..], areaScaled, threeD, labelled, flaw }.
     flaw is what is wrong with the chart: truncated | uneven | area | threeD | nolabels | fair. The chart is drawn from
     yStart, ticks (the numbers on the up axis, from the bottom: even steps unless the flaw is "uneven") and the other flags;
     an honest chart starts at 0 with even ticks.
     ===================================================================================================== */
  var LIE_OPTS = {
    fair: 'Yes: it is a fair chart',
    truncated: 'No: the axis does not start at 0',
    uneven: 'No: the scale has uneven steps',
    area: 'No: the pictures are scaled both ways',
    threeD: 'No: the 3D bars are misleading',
    nolabels: 'No: no title, labels or units'
  };
  var LIE = [
    { unit: '£', yLabel: 'Sales (£)', title: 'Sales of the Zing phone', items: ['Last year', 'This year'], times: ['2021', '2022', '2023', '2024'], claim: 'Sales have doubled' },
    { unit: '', yLabel: 'Average score', title: 'Average test score', items: ['Class A', 'Class B'], times: null, claim: 'Class B is much better than Class A' },
    { unit: '', yLabel: 'Members', title: 'Club members', items: ['2023', '2024'], times: ['2021', '2022', '2023', '2024'], claim: 'The club has grown enormously' },
    { unit: '', yLabel: 'Votes', title: 'Votes in the school election', items: ['Sam', 'Alex'], times: null, claim: 'Alex got far more votes than Sam' },
    { unit: '', yLabel: 'Matches won', title: 'Matches won', items: ['Reds', 'Blues'], times: null, claim: 'The Blues are far better than the Reds' },
    { unit: '', yLabel: 'Rainfall (mm)', title: 'Rainfall in two towns', items: ['Town P', 'Town Q'], times: null, claim: 'Town Q gets far more rain than Town P' }
  ];
  function lyingChart(rng, flaw, form) {
    var c = pick(rng, LIE.filter(function (x) { return form !== 'line' || x.times; })), a, b, ticks = [0, 20, 40, 60, 80, 100], yStart = 0, items;
    if (flaw === 'truncated') {
      var base = pick(rng, [60, 70, 80, 90]); a = base + 2 * rint(rng, 1, 3); b = a + 2 * rint(rng, 1, 3);
      yStart = base - 10; ticks = [yStart, yStart + 5, yStart + 10, yStart + 15, yStart + 20, yStart + 25];
    } else if (flaw === 'uneven') {
      a = pick(rng, [10, 20, 30]); b = a + pick(rng, [10, 20]);
      ticks = pick(rng, [[0, 10, 20, 50, 100], [0, 5, 10, 30, 80], [0, 20, 30, 40, 100]]);
    } else {
      a = pick(rng, [20, 30, 40]); b = flaw === 'fair' ? 2 * a : a + pick(rng, [20, 40]);
    }
    if (form === 'line') {                                    // four readings that rise from a to b
      var step = (b - a) / 3;
      items = c.times.map(function (t, k) { return { label: t, value: Math.round(a + step * k) }; });
    } else items = [{ label: c.items[0], value: a }, { label: c.items[1], value: b }];
    if (flaw === 'area') { form = 'pics'; items = [{ label: c.items[0], value: a }, { label: c.items[1], value: a * 2 }]; }
    return { type: 'lying', form: form, title: flaw === 'nolabels' ? null : c.title, yLabel: flaw === 'nolabels' ? null : c.yLabel, xLabel: null,
      items: items, yStart: yStart, ticks: ticks, areaScaled: flaw === 'area', threeD: flaw === 'threeD', labelled: flaw !== 'nolabels', flaw: flaw,
      claim: c.claim };
  }
  var LIE_PLAN = [
    ['truncated', 'bar'], ['truncated', 'line'], ['uneven', 'bar'], ['area', 'pics'], ['nolabels', 'bar'], ['fair', 'bar'],
    ['truncated', 'bar'], ['uneven', 'line'], ['threeD', 'bar'], ['fair', 'line'], ['nolabels', 'line'], ['area', 'pics']
  ];
  function stage5(slot, rng) {
    var plan = LIE_PLAN[slot], flaw = plan[0], ch = lyingChart(rng, flaw, plan[1]);
    var stem = 'The chart is used to say: "' + ch.claim + '." Is the chart a fair way to show it?';
    var others = Object.keys(LIE_OPTS).filter(function (k) { return k !== flaw && k !== 'fair'; });
    var wrongs = shuffled(rng, others).slice(0, flaw === 'fair' ? 2 : 2);
    if (flaw === 'fair') { wrongs = wrongs.filter(function (k) { return k !== 'truncated'; }).slice(0, 2); wrongs.unshift('truncated'); }
    else wrongs.unshift('fair');
    var opts = [flaw].concat(wrongs).map(function (k) { return LIE_OPTS[k]; });
    var answer = choice(rng, LIE_OPTS[flaw], wrongs.map(function (k) { return LIE_OPTS[k]; }));
    var a = ch.items[0].value, b = ch.items[1].value, w, slips = [];
    if (flaw === 'truncated') {
      w = ['Look at the numbers up the side: the axis starts at ' + ch.yStart + ', not 0.', 'The values are ' + a + ' and ' + b + ', so the difference is small, but the chart makes the second look much bigger.'];
      slips = [slipO('truncated-face-value', LIE_OPTS.fair, 'The bars look very different, but the axis does not start at 0. Cutting the axis makes a small difference look big.')];
    } else if (flaw === 'uneven') {
      w = ['Look at the numbers up the side: ' + ch.ticks.join(', ') + '.', 'The steps are not all the same size, so the heights of the bars cannot be compared fairly.'];
      slips = [slipO('face-value', LIE_OPTS.fair, 'The gaps between the numbers on the scale are not equal, so the chart is not a fair picture.')];
    } else if (flaw === 'area') {
      w = ['The second picture is twice the first in value (' + a + ' and ' + b + ').', 'But it is drawn twice as tall and twice as wide, so its area is four times as big and it looks far bigger.'];
      slips = [slipO('face-value', LIE_OPTS.fair, 'Doubling both the height and the width makes the area four times as big. That exaggerates the difference.')];
    } else if (flaw === 'threeD') {
      w = ['The bars are drawn in 3D, with tops and sides.', 'It is hard to see where the top of each bar meets the scale, and the bars look bigger than they are.'];
      slips = [slipO('face-value', LIE_OPTS.fair, 'The 3D effect makes the bars hard to read against the scale and makes them look bigger.')];
    } else if (flaw === 'nolabels') {
      w = ['There is no title, no label on the axes and no units.', 'Without them you cannot tell what the chart shows, so you cannot trust the claim.'];
      slips = [slipO('face-value', LIE_OPTS.fair, 'Without a title, axis labels or units you cannot tell what the chart is about.')];
    } else {
      w = ['The axis starts at 0, the steps are even, and the chart is labelled.', 'The bars show ' + a + ' and ' + b + ' fairly.'];
      slips = [slipO('doubted-fair', LIE_OPTS.truncated, 'The axis does start at 0. Check the numbers up the side before saying a chart is misleading.')];
    }
    return finish(5, slot, 'lying-' + flaw, ch, stem, { op: 'flaw' }, answer, w, slips);
  }

  /* ---------- the bank ---------- */
  var STAGE_FN = { 1: stage1, 2: stage2, 3: stage3, 4: stage4, 5: stage5 };
  var STAGE_NAMES = { 1: 'Pictograms', 2: 'Bar charts', 3: 'Line graphs', 4: 'Scatter graphs', 5: 'Is this chart lying?' };

  function question(stage, slot, rng) {
    rng = rng || Math.random;
    return STAGE_FN[stage](slot, rng);
  }
  // All 60 questions with a fixed seed: the same bank every time.
  function bank(seed) {
    var out = [], st, sl;
    seed = seed == null ? FIXED_SEED : seed;
    for (st = 1; st <= 5; st++) for (sl = 0; sl < SLOTS; sl++) out.push(question(st, sl, makeRng(seed + st * 1000 + sl)));
    return out;
  }

  root.MaffsReadingCharts = { question: question, bank: bank, makeRng: makeRng, SLOTS: SLOTS, FIXED_SEED: FIXED_SEED, CANT: CANT,
    STAGE_NAMES: STAGE_NAMES, LIE_OPTS: LIE_OPTS, TYPE3: TYPE3 };
})(typeof window !== 'undefined' ? window : globalThis);
