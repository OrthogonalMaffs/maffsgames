/* Who Ate All the Pies?: the game's own layer over the pie-charts bank (contract WHO-ATE-ALL-THE-PIES, build lane, 27 Oct 2026).
 *
 * Bank-first (canon 8.2.1): every question comes from MaffsPieCharts.question() (schools/assets/pie-chart-generator.js, the
 * same file the 6 P's bank is generated from). Nothing is copied or rewritten here. This module only
 *   - picks the questions of a session (ten of a stage's twelve slots, easiest first) and the stage's worked example,
 *   - says what a typed answer is (two boxes for a fraction, one for a number, one box a sector for a table, buttons for a
 *     choice) and marks it by value through MaffsAnswer, naming the bank's slips.
 *
 * Pure data, no DOM. A game question is the bank's question with
 *   type      'fraction' (n and d boxes) | 'number' (one box) | 'angles' (a box for every sector of the table) | 'choice'
 *   key       what is right: {n, d} | number | [angle, ...] | option index
 *   slips     [{kind, line, ...}]: the bank's named wrong answers; for 'angles' the same two slips worked for each sector
 *   bank      the bank's question itself, untouched (for the verifier)
 * mark(q, raws) takes the raw strings typed (a choice: the option index as a string) and returns
 *   { kind: 'right' | 'format' | 'slip' | 'wrong' | 'unreadable', why, ok: [bool a box] }.
 */
(function (root) {
  'use strict';

  var Bank = root.MaffsPieCharts, A = root.MaffsAnswer;
  var PER_STAGE = 10, SLOTS = 12;

  var STAGES = {
    1: { n: 1, name: 'Read it', blurb: 'What fraction of the pies is one slice?', type: 'fraction',
         generic: 'The whole chart is 360°. Put the slice\'s angle over 360, then simplify the fraction.' },
    2: { n: 2, name: 'Find the amount', blurb: 'Use the angle and the total to find how many pies.', type: 'number',
         generic: 'The angle over 360 is the fraction of the pies. Take that fraction of the total.' },
    3: { n: 3, name: 'Draw it', blurb: 'Work out every angle from the table and watch the chart build.', type: 'angles',
         generic: 'Each pie is worth 360 ÷ (the total) degrees. Multiply each frequency by that.' },
    4: { n: 4, name: 'Can you tell?', blurb: 'Is there enough information, or can you not tell?', type: 'choice',
         generic: 'Check what the charts give you. A bigger angle only means more pies when the totals are the same or known.' },
    5: { n: 5, name: 'Work backwards', blurb: 'One slice is known: find the total.', type: 'number',
         generic: 'The angle over 360 is the fraction of the total, and the frequency is that fraction of it. Scale up to the whole.' }
  };

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
  function tex(s) { return '\\(' + s + '\\)'; }
  function clean(v) { return Math.abs(v * 100 - Math.round(v * 100)) < 1e-9; }

  // The bank's question as a game question.
  function adapt(b) {
    var S = STAGES[b.stage], q = { stage: b.stage, slot: b.slot, kind: b.kind, type: S.type, stem: b.stem, worked: b.worked, why: b.why,
      charts: b.charts, ask: b.ask, friendly: b.friendly, setting: b.setting, bank: b, generic: S.generic, slips: [] };
    if (S.type === 'fraction') {
      q.key = { n: b.answer.n, d: b.answer.d };
      q.slips = b.slips.map(function (s) { return { kind: s.kind, n: s.answer.n, d: s.answer.d, line: s.line }; });
    } else if (S.type === 'number') {
      q.key = b.answer.value;
      q.slips = b.slips.map(function (s) { return { kind: s.kind, value: s.answer.value, line: s.line }; });
    } else if (S.type === 'choice') {
      q.key = b.answer.correct;
      q.options = b.answer.options.slice();
      q.slips = b.slips.map(function (s) { return { kind: s.kind, option: s.answer.option, line: s.line }; });
    } else {                                   // angles: the table's every sector, the asked one being the bank's own answer
      var ch = b.charts[0], T = ch.total;
      q.key = ch.sectors.map(function (s) { return s.angle; });
      q.sectors = ch.sectors.map(function (s) {
        var pc = s.freq * 100 / T, t360 = s.freq * 360, sl = [];
        if (clean(pc) && pc !== s.angle) sl.push({ kind: 'percent', value: pc,
          line: 'The ' + s.pie + ' angle is out of ' + tex('360^\\circ') + ', not a percentage: ' + tex(s.freq + ' \\div ' + T + ' \\times 100') + ' is the percentage.' });
        if (t360 !== s.angle) sl.push({ kind: 'times360', value: t360,
          line: 'The ' + s.pie + ' frequency ' + s.freq + ' was multiplied by 360 but not divided by the total of ' + T + ' pies.' });
        return { pie: s.pie, freq: s.freq, angle: s.angle, slips: sl };
      });
      q.total = T;
      q.askedIndex = ch.sectors.map(function (s) { return s.pie; }).indexOf(b.ask.pie);
    }
    return q;
  }

  // Ten questions of a stage, easiest first: the twelve slots in the bank's order, slot 0 kept for the worked example and one more
  // slot (random) left out.
  function session(stage, seed, count) {
    count = count || PER_STAGE;
    var rng = makeRng(seed), slots = [], i;
    for (i = 1; i < SLOTS; i++) slots.push(i);
    while (slots.length > count) slots.splice(Math.floor(rng() * slots.length), 1);
    return slots.map(function (slot) { return adapt(Bank.question(stage, slot, makeRng(seed * 31 + slot * 7 + stage))); });
  }
  function example(stage) { return adapt(Bank.question(stage, 0, makeRng(1000 + stage))); }

  // What a right answer types, for tests and for the answer helper.
  function solution(q) {
    if (q.type === 'fraction') return [String(q.key.n), String(q.key.d)];
    if (q.type === 'number') return [String(q.key)];
    if (q.type === 'angles') return q.key.map(String);
    return [String(q.key)];
  }

  /* ---------- marking, by value, through MaffsAnswer ---------- */
  function same(raw, v) { return A.exact(raw, String(v)) === 'correct'; }
  function unreadable(raws) { return raws.some(function (r) { return A.exact(r, '0') === 'unreadable'; }); }

  function mark(q, raws) {
    raws = raws.map(function (r) { return String(r == null ? '' : r).trim(); });
    if (q.type === 'choice') {
      var i = parseInt(raws[0], 10);
      if (i === q.key) return { kind: 'right', why: '', ok: [true] };
      for (var k = 0; k < q.slips.length; k++) if (q.options[i] === q.slips[k].option) return { kind: 'slip', why: q.slips[k].line, ok: [false] };
      return { kind: 'wrong', why: q.generic, ok: [false] };
    }
    if (raws.some(function (r) { return r === ''; }) || unreadable(raws)) return { kind: 'unreadable', why: A.message('unreadable'), ok: [] };
    if (q.type === 'fraction') {
      var n = raws[0], d = raws[1], dn = A.parse(d), nn = A.parse(n);
      if (!dn) return { kind: 'unreadable', why: 'The bottom number cannot be 0.', ok: [] };
      if (same(n, q.key.n) && same(d, q.key.d)) return { kind: 'right', why: '', ok: [true, true] };
      if (nn * q.key.d === q.key.n * dn) return { kind: 'format', why: 'Right value, but simplify it fully: divide the top and the bottom by the same number until you cannot.', ok: [false, false] };
      for (var j = 0; j < q.slips.length; j++) if (nn * q.slips[j].d === q.slips[j].n * dn) return { kind: 'slip', why: q.slips[j].line, ok: [false, false] };
      return { kind: 'wrong', why: q.generic, ok: [false, false] };
    }
    if (q.type === 'number') {
      if (same(raws[0], q.key)) return { kind: 'right', why: '', ok: [true] };
      for (var m = 0; m < q.slips.length; m++) if (same(raws[0], q.slips[m].value)) return { kind: 'slip', why: q.slips[m].line, ok: [false] };
      return { kind: 'wrong', why: q.generic, ok: [false] };
    }
    // angles
    var ok = q.sectors.map(function (s, x) { return same(raws[x], s.angle); });
    if (ok.every(Boolean)) return { kind: 'right', why: '', ok: ok };
    var sum = raws.reduce(function (a, r) { return a + A.parse(r); }, 0), why = null;
    for (var x2 = 0; x2 < q.sectors.length && !why; x2++) {
      if (ok[x2]) continue;
      for (var y = 0; y < q.sectors[x2].slips.length; y++) if (same(raws[x2], q.sectors[x2].slips[y].value)) { why = q.sectors[x2].slips[y].line; break; }
    }
    var closes = sum + ' degrees' + (sum === 360 ? '' : ' (a pie chart makes 360)');
    return why ? { kind: 'slip', why: why, ok: ok, sum: sum }
      : { kind: 'wrong', why: q.generic + ' Your angles add to ' + closes + '.', ok: ok, sum: sum };
  }

  root.MaffsPieGame = { STAGES: STAGES, PER_STAGE: PER_STAGE, SLOTS: SLOTS, session: session, example: example, adapt: adapt, mark: mark,
    solution: solution, makeRng: makeRng };
})(typeof window !== 'undefined' ? window : globalThis);
