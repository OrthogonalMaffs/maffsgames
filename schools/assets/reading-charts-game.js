/* As You Can See: the game's own layer over the reading-charts bank (contract AS-YOU-CAN-SEE, build lane, 27 Oct 2026).
 *
 * Bank-first (canon 8.2.1): every question comes from MaffsReadingCharts.question() (schools/assets/reading-charts-generator.js).
 * Nothing is copied or rewritten here. This module only
 *   - picks the questions of a session (ten of a stage's twelve slots, easiest first) and the stage's worked example,
 *   - says what a typed answer is (one box for a number, buttons for a choice) and marks it by value, naming the bank's slips.
 *
 * A number is right when it lies in the question's accepted interval, value +/- tol (half a minor gridline for a reading from a
 * graph, 0 for a count, a total or a difference). MaffsAnswer has no value-with-tolerance match, so the interval is applied here,
 * on the number MaffsAnswer.parse() reads from the raw string; the bank stores the interval (candidate for the shared helper).
 *
 * Pure data, no DOM. A game question is the bank's question with
 *   type     'number' (one box) | 'choice' (buttons)
 *   key      what is right: the value | the option index;  tol: the accepted half-width (number)
 *   slips    [{kind, value | option, line}]
 *   why      the bank's one-line working (the last two worked lines): shown after a right answer and marked in the working under a slip
 *   bank     the bank's question itself, untouched (for the verifier)
 * texify(text) turns each run of plain arithmetic in a string (4 x 5 = 20, 30 - 20 = 10, 18 / 4 = 4.5, with the school signs) into a KaTeX
 * expression between the page's markers (canon 7.1.1); the bank's strings are not rewritten, the page converts as it renders. There are
 * no fractions in this bank.
 * mark(q, raws) takes the raw strings typed (a choice: the option index as a string) and returns
 *   { kind: 'right' | 'slip' | 'wrong' | 'unreadable', why, ok: [bool a box] }.
 */
(function (root) {
  'use strict';

  var Bank = root.MaffsReadingCharts, A = root.MaffsAnswer;
  var PER_STAGE = 10, SLOTS = 12;

  var STAGES = {
    1: { n: 1, name: 'Pictograms', blurb: 'Use the key. Count whole, half and quarter symbols.',
         generic: 'Look at the key first: it says what one symbol stands for. A half symbol is half of that, and a quarter symbol is a quarter.' },
    2: { n: 2, name: 'Bar charts', blurb: 'Read scales in 2s, 5s and 10s; dual and stacked bars.',
         generic: 'Work out what each gridline is worth, then read across from the top of the bar. In a stacked bar a part is as long as its own length.' },
    3: { n: 3, name: 'Line graphs', blurb: 'Read values, spot trends, know what you cannot tell.',
         generic: 'Read the point on the line across to the scale. Only the marked points were measured: between them the graph cannot tell you.' },
    4: { n: 4, name: 'Scatter graphs', blurb: 'Correlation, the line of best fit, outliers and cause.',
         generic: 'Look at the direction of the points. Use the line of best fit only inside the data, and a correlation never proves a cause.' },
    5: { n: 5, name: 'Is this chart lying?', blurb: 'Spot the axes, scales and pictures that mislead.',
         generic: 'Check the numbers up the side (do they start at 0 and go up evenly?), how the pictures are drawn, and whether the chart is labelled.' }
  };

  var makeRng = Bank.makeRng;

  // The bank's question as a game question.
  function adapt(b) {
    var S = STAGES[b.stage], a = b.answer;
    var q = { stage: b.stage, slot: b.slot, kind: b.kind, type: a.type, stem: b.stem, worked: b.worked, why: b.why, chart: b.chart, ask: b.ask,
      generic: S.generic, bank: b, slips: [] };
    if (a.type === 'number') {
      q.key = a.value; q.tol = a.tol;
      q.slips = b.slips.map(function (s) { return { kind: s.kind, value: s.answer.value, line: s.line }; });
    } else {
      q.key = a.correct; q.options = a.options.slice();
      q.slips = b.slips.map(function (s) { return { kind: s.kind, option: s.answer.option, line: s.line }; });
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

  // A run of plain arithmetic: numbers (a minus sign allowed before one) joined by x, /, minus, plus or equals, with the school signs.
  var PLAIN_SUM = /−?\d+(?:\.\d+)?(?:\s*[×÷−+=]\s*−?\d+(?:\.\d+)?)+/g;
  function texify(text) {
    return String(text == null ? '' : text).replace(PLAIN_SUM, function (m) {
      return '\\(' + m.replace(/×/g, '\\times ').replace(/÷/g, '\\div ').replace(/−/g, '-') + '\\)';
    });
  }

  // What a right answer types, for tests and for the answer helper.
  function solution(q) { return [String(q.key)]; }

  /* ---------- marking: the number MaffsAnswer reads, against the accepted interval ---------- */
  function within(x, v, tol) { return Math.abs(x - v) <= tol + 1e-9; }
  function unreadable(raw) { return A.exact(raw, '0') === 'unreadable'; }

  function mark(q, raws) {
    raws = raws.map(function (r) { return String(r == null ? '' : r).trim(); });
    if (q.type === 'choice') {
      var i = parseInt(raws[0], 10);
      if (i === q.key) return { kind: 'right', why: '', ok: [true] };
      for (var k = 0; k < q.slips.length; k++) if (q.options[i] === q.slips[k].option) return { kind: 'slip', why: q.slips[k].line, ok: [false] };
      return { kind: 'wrong', why: q.generic, ok: [false] };
    }
    if (raws[0] === '' || unreadable(raws[0])) return { kind: 'unreadable', why: A.message('unreadable'), ok: [] };
    var x = A.parse(raws[0]);
    if (x == null || !isFinite(x)) return { kind: 'unreadable', why: A.message('unreadable'), ok: [] };
    if (within(x, q.key, q.tol)) return { kind: 'right', why: '', ok: [true] };
    for (var m = 0; m < q.slips.length; m++) if (within(x, q.slips[m].value, q.tol)) return { kind: 'slip', why: q.slips[m].line, ok: [false] };
    return { kind: 'wrong', why: q.generic, ok: [false] };
  }

  root.MaffsChartsGame = { STAGES: STAGES, PER_STAGE: PER_STAGE, SLOTS: SLOTS, session: session, example: example, adapt: adapt, mark: mark,
    solution: solution, makeRng: makeRng, texify: texify };
})(typeof window !== 'undefined' ? window : globalThis);
