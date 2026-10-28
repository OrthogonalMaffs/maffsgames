/* Possibly, Maybe: the game's own layer over the probability bank (contract POSSIBLY-MAYBE, build lane, 27 Oct 2026).
 *
 * Bank-first (canon 8.2.1): every question comes from MaffsProbability.question() (schools/assets/probability-generator.js).
 * Nothing is copied or rewritten here. This module only
 *   - picks the questions of a session (ten of a stage's twelve slots, easiest first) and the stage's worked example,
 *   - says what a typed answer is (two boxes for a fraction, one box for a number, buttons for a choice) and marks it by
 *     value with MaffsAnswer, naming the bank's slips.
 *
 * Fractions are typed (Jon's amendment): numerator and denominator, matched by value, so 2/4 is 1/2. A fraction in its lowest
 * terms is required only when the question says so (answer.simplest): then 2/4 is a 'format' result, the right value in the wrong
 * form, which is NEVER MARKED (no score change, the student retypes). A number is matched by value with MaffsAnswer.exact().
 *
 * Pure data, no DOM. A game question is the bank's question with
 *   type    'fraction' (two boxes) | 'number' (one box) | 'choice' (buttons)
 *   key     what is right: {num, den} | the string | the option index
 *   slips   [{kind, num, den | key | option, line}]
 *   bank    the bank's question itself, untouched (for the verifier)
 * Feedback that teaches (contract FEEDBACK-TEACHES, 28 Oct 2026): a question also carries
 *   why     the bank's one-line working (the last two worked lines), shown after a right answer and under a named slip
 *   labels  what each choice button says. For a compare question (the bank's 'order': three events with a probability each) the
 *           values go on the buttons ("Event A: 2/5") and askText keeps only the ask ("Which event is the most likely?"); the bank's
 *           stem and options are untouched (slips are matched on the bank's option text).
 * texify(text) turns every plain n/d in text into a KaTeX fraction between the page's markers, the form the page renders with KaTeX (canon 7.1.1); the bank's
 * strings are not rewritten, the page converts as it renders.
 * mark(q, raws) takes the raw strings typed (a fraction: "n/d" as MaffsFractionInput.raw() gives it; a choice: the option index
 * as a string) and returns { kind: 'right' | 'slip' | 'wrong' | 'format' | 'unreadable', why }.
 */
(function (root) {
  'use strict';

  var Bank = root.MaffsProbability, A = root.MaffsAnswer;
  var PER_STAGE = 10, SLOTS = 12;

  var STAGES = {
    1: { n: 1, name: 'The scale', blurb: 'Words to numbers: 0, evens, 1. Fractions, decimals and percentages.',
         generic: 'A probability is a number from 0 (impossible) to 1 (certain). Favourable outcomes over ALL the outcomes, and never more than 1.' },
    2: { n: 2, name: 'Not, and the missing one', blurb: 'P(not A) = 1 - P(A). Tables that add up to 1.',
         generic: 'All the probabilities of a set of outcomes add up to 1. For "not", take the probability away from 1.' },
    3: { n: 3, name: 'Listing outcomes', blurb: 'Sample spaces, dice and spinners, and counting combinations.',
         generic: 'List every outcome, counting 2 then 3 and 3 then 2 separately. Then favourable outcomes over all the outcomes. Combinations multiply.' },
    4: { n: 4, name: 'Expected and relative frequency', blurb: 'Expected number, estimates from results, is it fair.',
         generic: 'Expected number = probability x number of trials. Relative frequency = times it happened / number of trials. More trials, better estimate.' },
    5: { n: 5, name: 'Tree diagrams', blurb: 'Multiply along the branches, add between them.',
         generic: 'Multiply along the branches for "and". Add the different ways for "or". For "at least one", take P(none) away from 1.' }
  };

  var makeRng = Bank.makeRng;

  // The bank's question as a game question.
  function adapt(b) {
    var S = STAGES[b.stage], a = b.answer;
    var q = { stage: b.stage, slot: b.slot, kind: b.kind, type: a.type, stem: b.stem, worked: b.worked, why: b.why, chart: b.chart, ask: b.ask,
      generic: S.generic, bank: b, slips: [] };
    if (a.type === 'fraction') {
      q.key = { num: a.num, den: a.den }; q.simplest = !!a.simplest;
      q.slips = b.slips.map(function (s) { return { kind: s.kind, num: s.answer.num, den: s.answer.den, line: s.line }; });
    } else if (a.type === 'number') {
      q.key = a.key; q.unit = a.unit || '';
      q.slips = b.slips.map(function (s) { return { kind: s.kind, key: s.answer.key, line: s.line }; });
    } else {
      q.key = a.correct; q.options = a.options.slice();
      q.labels = a.options.slice(); q.askText = b.stem;
      var cmp = b.ask && b.ask.op === 'order' && b.ask.values && b.ask.values.length === a.options.length ? /(Which [^?]*\?)\s*$/.exec(b.stem) : null;
      if (cmp) { q.labels = a.options.map(function (o, i) { return o + ': ' + b.ask.values[i]; }); q.askText = cmp[1]; q.compare = true; }
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

  // Every plain n/d in a feedback or question string as KaTeX between the page markers: "P = 5/15" becomes P = then a KaTeX 5 over 15. Not a date-like
  // 1/2/3, a decimal such as 0.5/2, a name such as and/or (no digits), or text that is already TeX.
  var PLAIN_FRAC = /(^|[^\w.\/\\{}])(\d+)\/(\d+)(?![\w\/])/g;
  function texify(text) {
    return String(text == null ? '' : text).replace(PLAIN_FRAC, function (m, pre, n, d) { return pre + '\\(\\frac{' + n + '}{' + d + '}\\)'; });
  }

  // What a right answer types, for tests and for the answer helper.
  function solution(q) {
    if (q.type === 'fraction') return [q.key.num + '/' + q.key.den];
    return [String(q.key)];
  }

  /* ---------- marking ---------- */
  var FRACRAW = /^\d+\/\d+$/;
  function sameFrac(a, b) { return a.num === b.num && a.den === b.den; }
  function reduce(n, d) { var x = n, y = d; while (y) { var t = x % y; x = y; y = t; } return { num: n / x, den: d / x }; }

  function mark(q, raws) {
    raws = raws.map(function (r) { return String(r == null ? '' : r).trim(); });
    var raw = raws[0], k;
    if (q.type === 'choice') {
      var i = parseInt(raw, 10);
      if (i === q.key) return { kind: 'right', why: '' };
      for (k = 0; k < q.slips.length; k++) if (q.options[i] === q.slips[k].option) return { kind: 'slip', why: q.slips[k].line };
      return { kind: 'wrong', why: q.generic };
    }
    if (q.type === 'number') {
      var r = A.exact(raw, q.key);
      if (raw === '' || r === 'unreadable') return { kind: 'unreadable', why: A.message('unreadable') };
      if (r === 'correct') return { kind: 'right', why: '' };
      for (k = 0; k < q.slips.length; k++) if (A.exact(raw, q.slips[k].key) === 'correct') return { kind: 'slip', why: q.slips[k].line };
      return { kind: 'wrong', why: q.generic };
    }
    // a fraction: both boxes, whole numbers, a denominator that is not 0
    if (!FRACRAW.test(raw)) return { kind: 'unreadable', why: 'Fill in both boxes: the top and the bottom of the fraction.' };
    var f = A.fraction(raw);
    if (!f) return { kind: 'unreadable', why: 'The bottom of a fraction cannot be 0.' };
    var key = reduce(q.key.num, q.key.den);
    if (sameFrac(f, key)) {
      if (q.simplest) {
        var ff = A.fractionForm(raw, q.key, { form: 'simplest' });
        if (ff === 'format') return { kind: 'format', why: A.message('format', raw, { fraction: 'simplest' }) };
      }
      return { kind: 'right', why: '' };
    }
    for (k = 0; k < q.slips.length; k++) if (sameFrac(f, reduce(q.slips[k].num, q.slips[k].den))) return { kind: 'slip', why: q.slips[k].line };
    return { kind: 'wrong', why: q.generic };
  }

  root.MaffsProbabilityGame = { STAGES: STAGES, PER_STAGE: PER_STAGE, SLOTS: SLOTS, session: session, example: example, adapt: adapt,
    mark: mark, solution: solution, makeRng: makeRng, texify: texify };
})(typeof window !== 'undefined' ? window : globalThis);
