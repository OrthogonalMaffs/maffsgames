/* The pie-chart question generator (contract PIE-CHARTS-BANK, Jon, 26 Oct 2026): matchday pie sales at a sports stadium.

   The first bank-first topic: the bank is generated from this file by scripts/gen-six-ps.py, and the game "Who Ate All
   the Pies?", when it is built, loads this same file (canon 8.2.1). It never copies the questions.

   Pure data, no DOM: MaffsPieCharts.question(stage, slot, rng) returns one question as plain data (the setting, the
   charts, the stem, the answer, the working, the named slips), and the draw of the pie itself is the caller's. rng is a
   function returning a number from 0 up to 1 (Math.random by default), so a seed makes a question reproducible.

   Five stages, 12 slots each (the slot fixes what the question is about, rng only chooses the stand, the pies and the
   amounts the slot leaves open, so the 12 are always 12 different questions):
     1 read it        the fraction of the whole a sector shows
     2 find the amount  angle / 360 x total, the total given
     3 draw it        from a frequency table, the angle of one named sector
     4 can you tell?  two charts, or one: "Yes, it's ..." or "You can't tell"
     5 work backwards one sector's angle and frequency given: the total
   Every angle is a whole number of degrees and the angles of a chart make 360; every amount is a whole number.
   `friendly` is true when every division the method makes is by a friendly divisor (FRIENDLY) and gives a whole number:
   those questions can be tried without a calculator.

   A question is { stage, slot, kind, setting, charts, ask, answer, stem, worked, slips, friendly } where
     charts   [{ stand, total (a number, or null when the chart does not say), sectors: [{ pie, angle, shown }] }]
     ask      what is asked, by type: fraction | amount | angle | total | compare | cantell (see each stage)
     answer   { type: 'fraction', n, d } | { type: 'number', value } | { type: 'choice', options: [...], correct: <index> }
     slips    [{ kind, answer, line }] (the named wrong answers, each recomputable from its kind)
*/
(function (root) {
  'use strict';

  var STANDS = ['home end', 'away end', 'family stand', 'main stand'];
  var PIES = ['steak', 'chicken balti', 'cheese and onion', 'mince', 'vegetable'];
  var CANT = "You can't tell";
  // A division is friendly when its divisor is a times-table fact (12 or under) or a multiple of ten that goes into 360.
  var FRIENDLY = [2, 3, 4, 5, 6, 8, 9, 10, 12, 20, 30, 40, 60, 90, 120, 180];
  var SLOTS = 12;

  function gcd(a, b) { return b ? gcd(b, a % b) : Math.abs(a); }
  function rint(rng, a, b) { return a + Math.floor(rng() * (b - a + 1)); }
  function pick(rng, arr) { return arr[Math.floor(rng() * arr.length)]; }
  function shuffled(rng, arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(rng() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  function tex(s) { return '\\(' + s + '\\)'; }
  function deg(n) { return n + '°'; }
  function degTex(n) { return tex(n + '^\\circ'); }
  function fracTex(n, d) { return tex('\\frac{' + n + '}{' + d + '}'); }
  function friendlyDiv(d) { return FRIENDLY.indexOf(d) >= 0; }
  function clean(v) { return Math.abs(v * 100 - Math.round(v * 100)) < 1e-9; }   // a value a student can type exactly

  // k parts (each a positive multiple of step, at least minU steps) that make `sum`.
  function split(rng, sum, k, step, minU) {
    var units = sum / step;
    if (units < k * minU) return null;
    for (var tries = 0; tries < 200; tries++) {
      var cuts = {}, n = 0;
      while (n < k - 1) { var c = rint(rng, 1, units - 1); if (!cuts[c]) { cuts[c] = 1; n++; } }
      var pts = [0].concat(Object.keys(cuts).map(Number).sort(function (a, b) { return a - b; }), [units]);
      var parts = [], ok = true;
      for (var i = 1; i < pts.length; i++) { var u = pts[i] - pts[i - 1]; if (u < minU) ok = false; parts.push(u * step); }
      if (ok) return parts;
    }
    return null;
  }

  // The step every angle of a chart moves in: 5 degrees, or with a total the step that makes every sector's amount a whole number.
  function stepFor(total, angle) { return total ? 360 / gcd(360, total) : ((360 - angle) % 5 === 0 ? 5 : 1); }

  // A chart in which the first sector is `angle` and the rest (k - 1 sectors) make up the other angles.
  function chartWith(rng, stand, total, firstPie, angle, k, showFirst) {
    var step = stepFor(total, angle), rest = null;
    for (var kk = k; !rest && kk >= 2; kk--) rest = split(rng, 360 - angle, kk - 1, step, Math.ceil(15 / step));   // 15 degrees at least
    k = rest.length + 1;
    var others = shuffled(rng, PIES.filter(function (p) { return p !== firstPie; })).slice(0, k - 1);
    var sectors = [{ pie: firstPie, angle: angle, shown: !!showFirst }];
    for (var i = 0; i < rest.length; i++) sectors.push({ pie: others[i], angle: rest[i], shown: false });
    return { stand: stand, total: total, sectors: sectors };
  }

  function frac(angle) { var g = gcd(angle, 360); return { n: angle / g, d: 360 / g }; }
  function pieceTex(n, d) { return d === 1 ? String(n) : '\\frac{' + n + '}{' + d + '}'; }
  function intro(stand) { return 'The pie chart shows the pies sold in the ' + stand + ' on matchday.'; }

  // ---------------------------------------------------------------- stage 1: read it
  var S1 = [[180, 'direct'], [90, 'direct'], [120, 'direct'], [60, 'direct'], [270, 'direct'], [45, 'direct'],
            [150, 'direct'], [240, 'direct'], [60, 'rest'], [150, 'rest'], [100, 'rest'], [80, 'rest']];

  function stage1(slot, rng) {
    var a = S1[slot][0], kind = S1[slot][1], stand = pick(rng, STANDS), pie = pick(rng, PIES);
    var k = kind === 'rest' ? 2 : (a >= 270 ? 2 : (a >= 240 ? 3 : rint(rng, 3, 4)));
    var chart = chartWith(rng, stand, null, pie, a, k, true);
    var ask = kind === 'rest' ? chart.sectors[1].pie : pie;      // 'rest': the unlabelled sector is asked
    var angle = kind === 'rest' ? 360 - a : a;
    var f = frac(angle), fa = frac(a);
    var stem, worked;
    if (kind === 'rest') {
      stem = intro(stand) + ' The ' + pie + ' sector is ' + degTex(a) + '. There is only one other sector, ' + ask +
        '. What fraction of the pies sold were ' + ask + '? Give your answer in its simplest form.';
      worked = ['The angles in a pie chart make ' + degTex(360) + '.',
        'The ' + ask + ' sector is ' + tex('360 - ' + a + ' = ' + angle) + ' degrees.',
        'Its fraction is ' + tex('\\frac{' + angle + '}{360}') + '.',
        'In its simplest form that is ' + tex(pieceTex(f.n, f.d)) + '.'];
    } else {
      stem = intro(stand) + ' The ' + pie + ' sector is ' + degTex(a) +
        '. What fraction of the pies sold were ' + pie + '? Give your answer in its simplest form.';
      worked = ['The whole pie chart is ' + degTex(360) + '.',
        'The ' + pie + ' sector is ' + degTex(a) + ', so its fraction is ' + tex('\\frac{' + a + '}{360}') + '.',
        'In its simplest form that is ' + tex(pieceTex(f.n, f.d)) + '.'];
    }
    var slips = [];
    if (kind === 'rest') {
      slips.push({ kind: 'not360', answer: { n: fa.n, d: fa.d },
        line: 'The ' + pie + ' sector is ' + tex(pieceTex(fa.n, fa.d)) + ', not ' + ask + '. The two sectors make ' + degTex(360) + ', so ' + ask + ' is the rest.' });
    } else {
      var pg = gcd(a, 100);
      slips.push({ kind: 'percent', answer: { n: a / pg, d: 100 / pg },
        line: 'A sector of ' + degTex(a) + ' is not ' + tex(a + '\\%') + '. The whole chart is ' + degTex(360) + ', not 100.' });
    }
    return { kind: kind, charts: [chart], ask: { type: 'fraction', pie: ask }, answer: { type: 'fraction', n: f.n, d: f.d },
      stem: stem, worked: worked, slips: slips, friendly: friendlyDiv(f.d) };
  }

  // ---------------------------------------------------------------- stage 2: find the amount
  // Jon's spec: stage 2 is "find an amount given the total". The 'cant' kind below is kept for the game that loads this file;
  // "you can't tell" belongs to stage 4, so the bank's slots are all 'direct'.
  var S2 = [[90, 'direct'], [180, 'direct'], [120, 'direct'], [60, 'direct'], [45, 'direct'], [30, 'direct'],
            [270, 'direct'], [150, 'direct'], [135, 'direct'], [210, 'direct'], [105, 'direct'], [35, 'direct']];
  var TOTALS = [60, 72, 80, 96, 100, 120, 144, 150, 160, 180, 200, 216, 240, 288, 300, 360, 400, 480, 600];

  function stage2(slot, rng) {
    var a = S2[slot][0], kind = S2[slot][1], stand = pick(rng, STANDS), pie = pick(rng, PIES), f = frac(a);
    var ok = TOTALS.filter(function (t) { return t % f.d === 0; });
    var total = pick(rng, ok), k = rint(rng, 3, 4);
    if (kind === 'cant') {
      var chart = chartWith(rng, stand, null, pie, a, k, true);
      var wrong = [a + ' pies', (360 - a) + ' pies', '100 pies'];
      var opts = [CANT].concat(wrong);
      var order = shuffled(rng, opts);
      return { kind: 'cant', charts: [chart], ask: { type: 'cantell', pie: pie },
        answer: { type: 'choice', options: order, correct: order.indexOf(CANT) },
        stem: intro(stand) + ' The ' + pie + ' sector is ' + degTex(a) + '. How many ' + pie + ' pies were sold?',
        worked: ['The angle shows the fraction of the pies, not how many there are.',
          'The chart does not say how many pies were sold in total.',
          'Without the total, the number of ' + pie + ' pies cannot be worked out.',
          "So you can't tell."],
        slips: [{ kind: 'number_no_total', answer: { type: 'choice', option: a + ' pies' },
          line: 'The ' + degTex(a) + ' is an angle, not a number of pies. The total number of pies is not given.' }],
        friendly: true };
    }
    var chart2 = chartWith(rng, stand, total, pie, a, k, true);
    var amount = total * a / 360;
    var simple = pieceTex(f.n, f.d);
    var worked = ['The ' + pie + ' sector is ' + degTex(a) + ' of ' + degTex(360) + ', which is ' + tex('\\frac{' + a + '}{360}') +
        ' = ' + tex(simple) + '.',
      'Find ' + tex(simple) + ' of ' + total + ' pies.',
      f.n === 1 ? tex(total + ' \\div ' + f.d + ' = ' + amount) : tex(total + ' \\div ' + f.d + ' = ' + (total / f.d) + ', \\quad ' + (total / f.d) + ' \\times ' + f.n + ' = ' + amount)];
    var slips = [], p100 = total * a / 100;
    if (clean(p100) && p100 !== amount) slips.push({ kind: 'percent', answer: { type: 'number', value: p100 },
      line: 'The ' + degTex(a) + ' was divided by 100, as if it were a percentage. The whole chart is ' + degTex(360) + ': divide by 360.' });
    return { kind: 'direct', charts: [chart2], ask: { type: 'amount', pie: pie },
      answer: { type: 'number', value: amount },
      stem: intro(stand) + ' ' + total + ' pies were sold in total. The ' + pie + ' sector is ' + degTex(a) + '. How many ' + pie + ' pies were sold?',
      worked: worked, slips: slips, friendly: friendlyDiv(f.d) };
  }

  // ---------------------------------------------------------------- stage 3: draw it
  var S3 = [[36, 0], [60, 0], [40, 0], [72, 0], [90, 0], [120, 0], [24, 0], [45, 0], [48, 0], [80, 0], [100, 0], [150, 0]];

  function stage3(slot, rng) {
    var T = S3[slot][0], stand = pick(rng, STANDS), k = rint(rng, 3, 5);
    var stepF = T / gcd(360, T);              // a frequency that gives a whole-degree angle
    var minU = Math.ceil(T / 24 / stepF);     // a sector of 15 degrees at least
    var parts = split(rng, T, k, stepF, minU);
    for (var tr = 0; !parts && tr < 50; tr++) { k = Math.max(3, k - 1); parts = split(rng, T, k, stepF, minU); }
    var pies = shuffled(rng, PIES).slice(0, parts.length);
    var ix = rint(rng, 0, parts.length - 1), f = parts[ix], pie = pies[ix];
    var sectors = parts.map(function (p, i) { return { pie: pies[i], angle: p * 360 / T, shown: false, freq: p }; });
    var angle = f * 360 / T;
    var list = parts.map(function (p, i) { return cap(pies[i]) + ' ' + p; }).join(', ');
    var per = 360 / T, worked;
    if (360 % T === 0) {
      worked = ['There are ' + T + ' pies in total, and the whole chart is ' + degTex(360) + '.',
        'Each pie is worth ' + tex('360 \\div ' + T + ' = ' + per) + ' degrees.',
        'The ' + pie + ' sector is ' + tex(f + ' \\times ' + per + ' = ' + angle) + ' degrees.'];
    } else {
      worked = ['There are ' + T + ' pies in total, and the whole chart is ' + degTex(360) + '.',
        'Each pie is worth ' + tex('360 \\div ' + T + ' = ' + per) + ' degrees.',
        'The ' + pie + ' sector is ' + tex(f + ' \\times ' + per + ' = ' + angle) + ' degrees.'];
    }
    var slips = [], pc = f * 100 / T, t360 = f * 360;
    if (clean(pc) && pc !== angle) slips.push({ kind: 'percent', answer: { type: 'number', value: pc },
      line: 'That is the percentage of the pies, ' + tex(f + ' \\div ' + T + ' \\times 100') + ', not the angle. The angle is out of ' + degTex(360) + '.' });
    if (t360 !== angle) slips.push({ kind: 'times360', answer: { type: 'number', value: t360 },
      line: 'The ' + f + ' was multiplied by 360 but not divided by the total of ' + T + ' pies.' });
    return { kind: 'draw', charts: [{ stand: stand, total: T, sectors: sectors }], ask: { type: 'angle', pie: pie },
      answer: { type: 'number', value: angle },
      stem: 'The table shows the pies sold in the ' + stand + ' on matchday. ' + list + '. ' + T + ' pies were sold in total. ' +
        'A pie chart is drawn from the table. What angle should the ' + pie + ' sector be?',
      worked: worked, slips: slips, friendly: 360 % T === 0 && friendlyDiv(T) };
  }

  // ---------------------------------------------------------------- stage 4: can you tell?
  // [kind, angleA, angleB, totalA, totalB]
  var S4 = [['two', 120, 90], ['two', 60, 90], ['two', 180, 45], ['two', 90, 90], ['two', 150, 100],
            ['totals', 90, 120, 400, 240], ['totals', 45, 150, 360, 120], ['totals', 90, 180, 240, 120],
            ['same', 120, 90, 180, 180], ['same', 60, 100, 180, 180],
            ['one', 150, 90], ['one', 30, 100]];

  function stage4(slot, rng) {
    var s = S4[slot], kind = s[0], aA = s[1], aB = s[2], pair = shuffled(rng, STANDS).slice(0, 2), sa = pair[0], sb = pair[1];
    var pie = pick(rng, PIES);
    if (kind === 'one') {
      var two = shuffled(rng, PIES).slice(0, 2), p1 = two[0], p2 = two[1], stand = pick(rng, STANDS);
      var rest = split(rng, 360 - aA - aB, rint(rng, 1, 2), 5, 3);
      var others = PIES.filter(function (p) { return p !== p1 && p !== p2; });
      var secs = [{ pie: p1, angle: aA, shown: true }, { pie: p2, angle: aB, shown: true }];
      rest.forEach(function (r, i) { secs.push({ pie: others[i], angle: r, shown: true }); });
      var opts = ["Yes, it's " + p1, "Yes, it's " + p2, 'They sold the same number', CANT], o = shuffled(rng, opts);
      var big = aA > aB ? p1 : p2;
      return { kind: 'one', charts: [{ stand: stand, total: null, sectors: secs }], ask: { type: 'compare', pies: [p1, p2], stand: stand },
        answer: { type: 'choice', options: o, correct: o.indexOf("Yes, it's " + big) },
        stem: 'The pie chart shows the pies sold in the ' + stand + ' on matchday. Can you tell whether more ' + p1 + ' pies or more ' + p2 + ' pies were sold?',
        worked: ['Both sectors are on the same chart, so they are parts of the same total.',
          'The ' + p1 + ' sector is ' + degTex(aA) + ' and the ' + p2 + ' sector is ' + degTex(aB) + '.',
          'The bigger angle is the bigger share of the same total.', 'More ' + big + ' pies were sold, so you can tell.'],
        slips: [], friendly: true };
    }
    function mkChart(stand, a, total) {
      var step = stepFor(total, a), rest = null;
      for (var kk = rint(rng, 1, 2); !rest && kk >= 1; kk--) rest = split(rng, 360 - a, kk, step, Math.ceil(15 / step));
      var others = shuffled(rng, PIES.filter(function (p) { return p !== pie; }));
      var secs = [{ pie: pie, angle: a, shown: true }];
      rest.forEach(function (r, i) { secs.push({ pie: others[i], angle: r, shown: true }); });
      return { stand: stand, total: total, sectors: secs };
    }
    var tA = kind === 'two' ? null : s[3], tB = kind === 'two' ? null : s[4];
    var charts = [mkChart(sa, aA, tA), mkChart(sb, aB, tB)];
    var options = ["Yes, it's the " + sa, "Yes, it's the " + sb, 'They sold the same number', CANT], o2 = shuffled(rng, options);
    var key, worked, slips = [], friendly = true, intro2;
    var head = 'The pie charts show the pies sold in the ' + sa + ' and the ' + sb + ' on matchday.';
    if (kind === 'two') {
      key = CANT;
      intro2 = head + ' The ' + pie + ' sector is ' + degTex(aA) + ' in the ' + sa + ' and ' + degTex(aB) + ' in the ' + sb + '. Can you tell which stand sold more ' + pie + ' pies?';
      worked = ['The sectors are fractions of two different totals.',
        'The chart for the ' + sa + ' and the chart for the ' + sb + ' do not say how many pies were sold.',
        'A bigger angle on one chart does not mean more pies than a smaller angle on the other.', "So you can't tell."];
      var guess = aA === aB ? 'They sold the same number' : (aA > aB ? "Yes, it's the " + sa : "Yes, it's the " + sb);
      slips.push({ kind: 'compare_totals', answer: { type: 'choice', option: guess },
        line: 'The sectors were compared as if the two charts had the same total. They are different charts, and no totals are given.' });
    } else if (kind === 'totals') {
      var nA = tA * aA / 360, nB = tB * aB / 360;
      key = nA === nB ? 'They sold the same number' : (nA > nB ? "Yes, it's the " + sa : "Yes, it's the " + sb);
      intro2 = head + ' The ' + sa + ' sold ' + tA + ' pies and the ' + sb + ' sold ' + tB + ' pies. The ' + pie + ' sector is ' + degTex(aA) + ' in the ' + sa +
        ' and ' + degTex(aB) + ' in the ' + sb + '. Can you tell which stand sold more ' + pie + ' pies?';
      worked = ['Both totals are given, so the numbers can be worked out.',
        'The ' + sa + ': ' + tex(tA + ' \\times \\frac{' + aA + '}{360} = ' + nA) + '.',
        'The ' + sb + ': ' + tex(tB + ' \\times \\frac{' + aB + '}{360} = ' + nB) + '.',
        nA === nB ? 'The two numbers are equal, so they sold the same number.' : 'The ' + (nA > nB ? sa : sb) + ' sold more, so you can tell.'];
      var bigger = aA === aB ? CANT : (aA > aB ? "Yes, it's the " + sa : "Yes, it's the " + sb);
      if (bigger !== key) slips.push({ kind: 'compare_totals', answer: { type: 'choice', option: bigger },
        line: 'The bigger sector was chosen, but the two charts have different totals. Work out the numbers of pies first.' });
      friendly = friendlyDiv(frac(aA).d) && tA % frac(aA).d === 0 && friendlyDiv(frac(aB).d) && tB % frac(aB).d === 0;
    } else {   // same total stated
      var t = tA, nA2 = t * aA / 360, nB2 = t * aB / 360;
      key = nA2 > nB2 ? "Yes, it's the " + sa : "Yes, it's the " + sb;
      intro2 = head + ' Each stand sold ' + t + ' pies. The ' + pie + ' sector is ' + degTex(aA) + ' in the ' + sa + ' and ' + degTex(aB) + ' in the ' + sb +
        '. Can you tell which stand sold more ' + pie + ' pies?';
      worked = ['Both stands sold ' + t + ' pies, so the totals are the same.',
        'With the same total, the bigger angle is the bigger share.',
        'The ' + degTex(Math.max(aA, aB)) + ' sector is bigger than the ' + degTex(Math.min(aA, aB)) + ' sector.',
        'The ' + (aA > aB ? sa : sb) + ' sold more, so you can tell.'];
      friendly = true;
    }
    return { kind: kind, charts: charts, ask: { type: 'compare', pie: pie, stands: [sa, sb] },
      answer: { type: 'choice', options: o2, correct: o2.indexOf(key) }, stem: intro2, worked: worked, slips: slips, friendly: friendly };
  }

  // ---------------------------------------------------------------- stage 5: work backwards
  // Jon's spec: stage 5 is "work backwards from one sector's angle and frequency to the total". The 'other' and 'cant' kinds
  // below are kept for the game that loads this file; the bank's slots are all 'total'.
  var S5 = [['total', 90, 20], ['total', 60, 15], ['total', 120, 45], ['total', 45, 12], ['total', 30, 7], ['total', 72, 18],
            ['total', 150, 25], ['total', 135, 27], ['total', 40, 6], ['total', 80, 16], ['total', 36, 9], ['total', 100, 20]];

  function stage5(slot, rng) {
    var s = S5[slot], kind = s[0], a = s[1], stand = pick(rng, STANDS), pie = pick(rng, PIES);
    if (kind === 'cant') {
      var aB = s[2], fB = s[3], two = shuffled(rng, STANDS).slice(0, 2), sa = two[0], sb = two[1];
      var chA = chartWith(rng, sa, null, pie, a, rint(rng, 2, 3), true), chB = chartWith(rng, sb, null, pie, aB, rint(rng, 2, 3), true);
      var naive = fB * a / aB;
      var opts = [CANT, naive + ' pies', a + ' pies', fB + ' pies'], o = shuffled(rng, opts);
      return { kind: 'cant', charts: [chA, chB], ask: { type: 'cantell', pie: pie, stands: [sa, sb], knownFreq: fB, knownAngle: aB },
        answer: { type: 'choice', options: o, correct: o.indexOf(CANT) },
        stem: 'The pie charts show the pies sold in the ' + sa + ' and the ' + sb + ' on matchday. In the ' + sb + ', the ' + pie + ' sector is ' + degTex(aB) +
          ' and ' + fB + ' ' + pie + ' pies were sold. In the ' + sa + ', the ' + pie + ' sector is ' + degTex(a) + '. How many ' + pie + ' pies were sold in the ' + sa + '?',
        worked: ['The ' + sb + ' chart gives the total for the ' + sb + ' only.',
          'The ' + sa + ' chart is a different chart and its total is not given.',
          'The two totals could be different, so the ' + sb + ' numbers cannot be used for the ' + sa + '.', "So you can't tell."],
        slips: [{ kind: 'compare_totals', answer: { type: 'choice', option: naive + ' pies' },
          line: 'The two charts were treated as having the same total. The ' + sa + ' total is not given, so the ' + sb + ' numbers cannot be used.' },
          { kind: 'number_no_total', answer: { type: 'choice', option: a + ' pies' },
          line: 'The ' + degTex(a) + ' is an angle, not a number of pies. The total number of pies in the ' + sa + ' is not given.' }],
        friendly: true };
    }
    var f = frac(a);
    if (kind === 'total') {
      var fq = s[2], total = fq * 360 / a, k = rint(rng, 3, 4);
      var chart = chartWith(rng, stand, null, pie, a, k, true);
      var worked = ['The ' + pie + ' sector is ' + degTex(a) + ' of ' + degTex(360) + ', which is ' + tex(pieceTex(f.n, f.d)) + ' of the pies.',
        fq + ' pies are ' + tex(pieceTex(f.n, f.d)) + ' of the total.',
        f.n === 1 ? 'The total is ' + tex(fq + ' \\times ' + f.d + ' = ' + total) + ' pies.'
          : 'One part is ' + tex(fq + ' \\div ' + f.n + ' = ' + (fq / f.n)) + ', so the total is ' + tex((fq / f.n) + ' \\times ' + f.d + ' = ' + total) + ' pies.'];
      if (fq % f.n !== 0) worked = [worked[0], worked[1], 'The total is ' + tex(fq + ' \\times \\frac{360}{' + a + '} = ' + total) + ' pies.'];
      var slips = [], pv = fq * 100 / a;
      if (clean(pv) && pv !== total) slips.push({ kind: 'percent', answer: { type: 'number', value: pv },
        line: 'The ' + degTex(a) + ' was used as if it were a percentage, so the total was found out of 100. The whole chart is ' + degTex(360) + '.' });
      return { kind: 'total', charts: [chart], ask: { type: 'total', pie: pie, freq: fq }, answer: { type: 'number', value: total },
        stem: intro(stand) + ' The ' + pie + ' sector is ' + degTex(a) + ' and ' + fq + ' ' + pie + ' pies were sold. How many pies were sold in total?',
        worked: worked, slips: slips, friendly: friendlyDiv(f.d) && fq % f.n === 0 };
    }
    var fq2 = s[2], b = s[3], ans = fq2 * b / a, rest = 360 - a - b;       // another sector
    var pies2 = shuffled(rng, PIES).slice(0, 3), sec = [{ pie: pies2[0], angle: a, shown: true }, { pie: pies2[1], angle: b, shown: true }];
    if (rest > 0) sec.push({ pie: pies2[2], angle: rest, shown: false });
    var g = gcd(a, b), ra = a / g, rb = b / g;
    return { kind: 'other', charts: [{ stand: stand, total: null, sectors: sec }], ask: { type: 'amount', pie: pies2[1], known: pies2[0], knownFreq: fq2 },
      answer: { type: 'number', value: ans },
      stem: intro(stand) + ' The ' + pies2[0] + ' sector is ' + degTex(a) + ' and ' + fq2 + ' ' + pies2[0] + ' pies were sold. The ' + pies2[1] + ' sector is ' + degTex(b) +
        '. How many ' + pies2[1] + ' pies were sold?',
      worked: ['The pies are shared in proportion to the angles.',
        ra === 1 ? degTex(a) + ' is ' + fq2 + ' pies.' : degTex(a) + ' is ' + fq2 + ' pies, so each ' + degTex(g) + ' is ' + tex(fq2 + ' \\div ' + ra + ' = ' + (fq2 / ra)) + ' pies.',
        'The ' + pies2[1] + ' sector is ' + degTex(b) + ', which is ' + tex(rb + ' \\times ' + g + '^\\circ') + ', so it is ' + tex(rb + ' \\times ' + (fq2 / ra) + ' = ' + ans) + ' pies.'],
      slips: [], friendly: friendlyDiv(ra) && fq2 % ra === 0 };
  }

  var STAGE_FN = { 1: stage1, 2: stage2, 3: stage3, 4: stage4, 5: stage5 };
  var BANDS = { 1: 2, 2: 3, 3: 3, 4: 4, 5: 4 };

  function question(stage, slot, rng) {
    rng = rng || Math.random;
    var q = STAGE_FN[stage](slot, rng);
    q.stage = stage; q.slot = slot; q.band = BANDS[stage];
    q.setting = 'matchday pie sales at a sports stadium';
    return q;
  }

  root.MaffsPieCharts = { STANDS: STANDS, PIES: PIES, FRIENDLY: FRIENDLY, SLOTS: SLOTS, STAGES: [1, 2, 3, 4, 5], BANDS: BANDS, CANT: CANT, question: question };
})(typeof window !== 'undefined' ? window : globalThis);
