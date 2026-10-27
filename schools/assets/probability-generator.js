/* The probability question generator (contract POSSIBLY-MAYBE, Jon, 27 Oct 2026): the scale, "not" and the missing one, listing
   outcomes, expected and relative frequency, and tree diagrams. Foundation level (OCR grades 1 to 5).

   Bank first (canon 8.2.1): the game "Possibly, Maybe" loads this same file and never copies a question; The 6 P's can import it
   later. Pure data, no DOM: MaffsProbability.question(stage, slot, rng) returns one question as plain data (the picture, the
   stem, the answer, the working and the named slips), and the drawing is the caller's. rng is a function returning a number from
   0 up to 1; MaffsProbability.bank() makes all 60 questions with a fixed seed, so the bank is the same every time.

   Five stages, 12 slots each (the slot fixes what the question is about; rng chooses the setting and the numbers, so the 12 are
   always 12 different questions):
     1 the scale        words and numbers, fraction / decimal / percentage, nothing outside 0 to 1
     2 not, and the missing one   P(not A) = 1 - P(A); a table that sums to 1; "x and 2x"
     3 listing outcomes sample spaces (spinners, dice, coin and dice); favourable over total; the product rule for menus
     4 expected and relative frequency   probability x trials; relative frequency; the more reliable estimate; is the dice fair
     5 tree diagrams    independent events: multiply along, add between; "at least one" as 1 - P(none)

   A question is { stage, slot, kind, chart, stem, ask, answer, worked, slips, calc } where
     chart    null, or the picture as data: { type: 'spinner' | 'bag' | 'numberline' | 'grid' | 'table' | 'tree', ... }
     ask      what is asked, as parameters ({ op, ... }): the verifier recomputes the answer from these and the chart
     answer   { type: 'fraction', num, den, simplest }   a typed numerator and denominator, equal in value is right
                                                          (not in lowest terms only when simplest is true: then it is a format
                                                          slip, never marked)
              { type: 'number', key: '0.35', unit }       a typed number, equal in value to key (a string, exact); unit is
                                                          '%' when the box says %
              { type: 'choice', options: [...], correct: <index> }
     slips    [{ kind, answer: { num, den } | { key } | { option }, line }]: the named wrong answers, each different from the
              right answer; no two the same
     calc     false: nothing here needs a calculator
*/
(function (root) {
  'use strict';

  var SLOTS = 12, FIXED_SEED = 20261028;

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
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a; }
  function lowest(n, d) { var g = gcd(n, d) || 1; return { n: n / g, d: d / g }; }
  function fs(n, d) { return n + '/' + d; }
  // A decimal from hundredths: 35 -> "0.35", 40 -> "0.4", 5 -> "0.05", 100 -> "1".
  function dec(h) {
    if (h % 100 === 0) return String(h / 100);
    var s = (h / 100).toFixed(2);
    return s.replace(/0$/, '');
  }
  function sum(a) { return a.reduce(function (x, y) { return x + y; }, 0); }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

  function frac(n, d, simplest) { return { type: 'fraction', num: n, den: d, simplest: !!simplest }; }
  function numA(key, unit) { return { type: 'number', key: String(key), unit: unit || '' }; }
  function slipF(kind, n, d, line) { return { kind: kind, answer: { num: n, den: d }, line: line }; }
  function slipN(kind, key, line) { return { kind: kind, answer: { key: String(key) }, line: line }; }
  function slipO(kind, option, line) { return { kind: kind, answer: { option: option }, line: line }; }
  function choice(rng, right, wrongs) {
    var opts = shuffled(rng, [right].concat(wrongs));
    return { type: 'choice', options: opts, correct: opts.indexOf(right) };
  }
  function choiceFixed(options, right) { return { type: 'choice', options: options.slice(), correct: options.indexOf(right) }; }

  // The finished question: slips different from the right answer, none repeated.
  function same(a, b) {
    if (a.num !== undefined) return a.num * b.den === b.num * a.den;
    if (a.key !== undefined) return Math.abs(parseFloat(a.key) - parseFloat(b.key)) < 1e-9;
    return a.option === b.option;
  }
  function finish(stage, slot, kind, chart, stem, ask, answer, worked, slips) {
    var out = [];
    var right = answer.type === 'fraction' ? { num: answer.num, den: answer.den } :
      (answer.type === 'number' ? { key: answer.key } : { option: answer.options[answer.correct] });
    (slips || []).forEach(function (s) {
      if (s.answer.den === 0 || same(s.answer, right)) return;
      if (s.answer.num !== undefined && s.answer.num < 0) return;
      if (answer.type === 'choice' && answer.options.indexOf(s.answer.option) < 0) return;
      for (var i = 0; i < out.length; i++) if (same(out[i].answer, s.answer)) return;
      out.push(s);
    });
    return { stage: stage, slot: slot, kind: kind, chart: chart || null, stem: stem, ask: ask, answer: answer, worked: worked, slips: out, calc: false };
  }

  var COLOURS = ['red', 'blue', 'green', 'yellow', 'white'];
  var LETTER = { red: 'R', blue: 'B', green: 'G', yellow: 'Y', white: 'W' };

  // A spinner with equal sectors: counts[i] sectors of colour names[i], shuffled round the circle.
  function spinner(rng, names, counts) {
    var list = [];
    names.forEach(function (nm, i) { for (var k = 0; k < counts[i]; k++) list.push(nm); });
    return { type: 'spinner', sectors: shuffled(rng, list).map(function (nm) { return { name: nm, letter: LETTER[nm] }; }) };
  }
  function bag(names, counts) {
    return { type: 'bag', items: names.map(function (nm, i) { return { name: nm, letter: LETTER[nm], count: counts[i] }; }) };
  }

  /* =====================================================================================================
     STAGE 1: the scale
     ===================================================================================================== */
  var WORDS = ['impossible', 'unlikely', 'evens', 'likely', 'certain'];
  var WORD_NUM = { impossible: '0', evens: '1/2', certain: '1' };

  function s1_sectors(rng, slot) {                // P(colour) on a spinner of equal sectors
    var n = pick(rng, [4, 5, 6, 8, 10]), names = shuffled(rng, COLOURS).slice(0, 3);
    var k = rint(rng, 1, Math.max(1, Math.floor((n - 2) / 2) + 1)), m = rint(rng, 1, n - k - 1);
    var counts = [k, m, n - k - m];
    var ch = spinner(rng, names, counts);
    var stem = 'The spinner has ' + n + ' equal sectors. It is spun once. What is the probability that it lands on ' + names[0] + '?';
    return finish(1, slot, 'sectors', ch, stem, { op: 'share', of: names[0] }, frac(k, n),
      ['Count the ' + names[0] + ' sectors: ' + k + '.', 'Count all the sectors: ' + n + '.', 'P(' + names[0] + ') = ' + k + '/' + n + '.'],
      [slipF('part-to-part', k, n - k, 'That compares the ' + names[0] + ' sectors with the others. The bottom must be ALL the sectors, ' + n + '.'),
       slipF('top-only', 1, n, 'That would be one sector. There are ' + k + ' ' + names[0] + ' sectors out of ' + n + '.')]);
  }
  function s1_wordvalue(rng, slot) {
    var w = pick(rng, ['impossible', 'evens', 'certain']);
    var opts = ['0', '1/2', '1'];
    var line = { '0': 'Zero means it cannot happen: impossible.', '1/2': '1/2 means an even chance: evens.', '1': 'One means it must happen: certain.' };
    var sl = opts.filter(function (o) { return o !== WORD_NUM[w]; }).map(function (o) { return slipO('wrong-end', o, line[o]); });
    return finish(1, slot, 'word-value', null, 'On the probability scale, which number goes with the word "' + w + '"?',
      { op: 'word-value', word: w }, choiceFixed(opts, WORD_NUM[w]),
      ['Impossible is 0, evens is 1/2 and certain is 1.', '"' + cap(w) + '" goes with ' + WORD_NUM[w] + '.'], sl);
  }
  var EVENTS = [
    ['The sun rises tomorrow', 'certain'], ['You roll a 7 on an ordinary dice', 'impossible'], ['A fair coin lands on heads', 'evens'],
    ['You roll a 6 on a fair dice', 'unlikely'], ['You roll a number less than 6 on a fair dice', 'likely'],
    ['The next baby born is a girl or a boy', 'certain'], ['A person picked at random has three heads', 'impossible'],
    ['You pick a red card from a pack with one red card and 19 blue cards', 'unlikely'],
    ['You pick a blue card from a pack with one red card and 19 blue cards', 'likely']
  ];
  function s1_wordevent(rng, slot) {
    var e = pick(rng, EVENTS);
    var sl = WORDS.filter(function (w) { return w !== e[1]; }).map(function (w) { return slipO('wrong-word', w, 'Think about how often it would happen: "' + w + '" is not the best word.'); });
    return finish(1, slot, 'word-event', null, 'Choose the best word for this event: ' + e[0].charAt(0).toLowerCase() + e[0].slice(1) + '.',
      { op: 'word-event', event: e[0] }, choiceFixed(WORDS, e[1]),
      ['Ask how often it would happen if you tried many times.', 'The best word is "' + e[1] + '".'], sl);
  }
  function s1_place(rng, slot) {
    var cases = [[0.05, 'unlikely'], [0.15, 'unlikely'], [0.5, 'evens'], [0.85, 'likely'], [0.95, 'likely']];
    var c = pick(rng, cases);
    var sl = WORDS.filter(function (w) { return w !== c[1]; }).map(function (w) { return slipO('wrong-word', w, 'Look where the arrow is on the line from 0 to 1: "' + w + '" does not fit.'); });
    return finish(1, slot, 'place-word', { type: 'numberline', at: c[0] }, 'The arrow shows the probability of an event on the scale from 0 to 1. Choose the best word for it.',
      { op: 'place', at: c[0] }, choiceFixed(WORDS, c[1]),
      ['Near 0 is unlikely, in the middle is evens, near 1 is likely.', 'The arrow is at ' + c[0] + ': "' + c[1] + '".'], sl);
  }
  function s1_bag(rng, slot) {
    var names = shuffled(rng, COLOURS).slice(0, 3), counts = [rint(rng, 2, 5), rint(rng, 2, 6), rint(rng, 1, 5)], t = sum(counts);
    var stem = 'A bag has ' + counts[0] + ' ' + names[0] + ' counters, ' + counts[1] + ' ' + names[1] + ' counters and ' + counts[2] + ' ' + names[2] + ' counters. One counter is taken out without looking. What is the probability that it is ' + names[0] + '?';
    return finish(1, slot, 'bag', bag(names, counts), stem, { op: 'share', of: names[0] }, frac(counts[0], t),
      ['Counters of the colour: ' + counts[0] + '.', 'All the counters: ' + counts[0] + ' + ' + counts[1] + ' + ' + counts[2] + ' = ' + t + '.', 'P(' + names[0] + ') = ' + counts[0] + '/' + t + '.'],
      [slipF('part-to-part', counts[0], t - counts[0], 'That compares ' + names[0] + ' with the others (' + (counts[0] > t - counts[0] ? 'and gives more than 1, which a probability never is' : 'ratio style') + '). The bottom is ALL the counters, ' + t + '.')]);
  }
  function s1_fracdec(rng, slot) {
    var d = pick(rng, [4, 5, 10, 20, 25, 50]), n = rint(rng, 1, d - 1);
    var h = n * 100 / d; if (h !== Math.floor(h)) return s1_fracdec(rng, slot);
    return finish(1, slot, 'frac-to-dec', null, 'The probability of an event is ' + fs(n, d) + '. Write this probability as a decimal.',
      { op: 'frac-to-dec', n: n, d: d }, numA(dec(h)),
      [fs(n, d) + ' means ' + n + ' divided by ' + d + '.', 'Make the bottom 100: ' + fs(h, 100) + '.', 'As a decimal that is ' + dec(h) + '.'],
      [slipN('point-moved', String(h / 1000), 'The decimal point is in the wrong place. Hundredths have two digits after the point.'),
       slipN('above-one', String(h), 'A probability cannot be more than 1. ' + h + ' is the number of hundredths; as a decimal it is ' + dec(h) + '.')]);
  }
  function s1_fracpct(rng, slot) {
    var d = pick(rng, [4, 5, 10, 20, 25, 50]), n = rint(rng, 1, d - 1), p = n * 100 / d;
    if (p !== Math.floor(p)) return s1_fracpct(rng, slot);
    return finish(1, slot, 'frac-to-pct', null, 'The probability of an event is ' + fs(n, d) + '. Write this probability as a percentage.',
      { op: 'frac-to-pct', n: n, d: d }, numA(p, '%'),
      ['Make the bottom 100: ' + fs(p, 100) + '.', '"Out of 100" is a percentage: ' + p + '%.'],
      [slipN('decimal-not-percent', dec(p), 'That is the decimal. A percentage is out of 100, so ' + dec(p) + ' becomes ' + p + '%.'),
       slipN('top-only', String(n), 'That is just the top number. Scale ' + fs(n, d) + ' up to a fraction out of 100.')]);
  }
  function s1_decfrac(rng, slot) {
    var h = pick(rng, [5, 15, 35, 45, 55, 65, 75, 85, 95, 20, 40, 60, 80, 12, 24, 36, 48]), l = lowest(h, 100);
    return finish(1, slot, 'dec-to-frac', null, 'The probability of an event is ' + dec(h) + '. Write this as a fraction in its simplest form.',
      { op: 'dec-to-frac', h: h }, frac(l.n, l.d, true),
      [dec(h) + ' is ' + fs(h, 100) + '.', 'Divide the top and bottom by ' + gcd(h, 100) + ': ' + fs(l.n, l.d) + '.'],
      [slipF('over-ten', h, 10, 'The bottom should be 100, as there are two digits after the point: ' + fs(h, 100) + '. Then simplify.')]);
  }
  function s1_cards(rng, slot) {
    var N = pick(rng, [10, 12, 15, 20]), kinds = ['even', 'a multiple of 3', 'greater than ' + rint(rng, 3, N - 3), 'a prime number'];
    var which = pick(rng, kinds), fav = 0, i;
    var isPrime = function (x) { if (x < 2) return false; for (var k = 2; k * k <= x; k++) if (x % k === 0) return false; return true; };
    for (i = 1; i <= N; i++) {
      if (which === 'even' ? i % 2 === 0 : (which === 'a multiple of 3' ? i % 3 === 0 : (which === 'a prime number' ? isPrime(i) : i > parseInt(which.split(' ')[2], 10)))) fav++;
    }
    var stem = 'Cards numbered 1 to ' + N + ' are shuffled and one is taken at random. What is the probability that the number is ' + which + '?';
    return finish(1, slot, 'cards', null, stem, { op: 'cards', N: N, test: which }, frac(fav, N),
      ['List the cards that are ' + which + ' and count them: ' + fav + '.', 'There are ' + N + ' cards.', 'P = ' + fs(fav, N) + '.'],
      [slipF('part-to-part', fav, N - fav, 'That compares the cards that fit with the cards that do not. The bottom is ALL the cards, ' + N + '.'),
       slipF('off-by-one', fav + 1, N, 'Check your list again: ' + fav + ' cards fit, not ' + (fav + 1) + '.')]);
  }
  function s1_cannot(rng, slot) {
    var bad = pick(rng, ['1.2', '-0.1', '3/2', '110%', '7/5', '-5%', '2']);
    var good = shuffled(rng, ['0.4', '3/4', '5%', '1', '0', '0.99', '2/3', '50%']).slice(0, 3);
    var o = choice(rng, bad, good);
    var sl = good.map(function (g) { return slipO('inside-scale', g, g + ' is between 0 and 1 (or 0% and 100%), so it can be a probability.'); });
    return finish(1, slot, 'cannot-be', null, 'Which of these can NOT be a probability?', { op: 'cannot-be', bad: bad, good: good }, o,
      ['A probability is never less than 0 or more than 1 (0% to 100%).', bad + ' is outside that.'], sl);
  }
  function value(s) {                              // a probability written as a fraction, decimal or percentage, as hundredths
    if (/%$/.test(s)) return parseFloat(s) / 100;
    if (/\//.test(s)) { var p = s.split('/'); return parseInt(p[0], 10) / parseInt(p[1], 10); }
    return parseFloat(s);
  }
  function s1_order(rng, slot) {
    var sets = [['3/5', '0.55', '58%'], ['7/10', '0.65', '68%'], ['1/4', '0.3', '27%'], ['4/5', '0.75', '78%'], ['2/5', '0.45', '42%'], ['5/8', '0.6', '63%'], ['9/20', '0.4', '43%']];
    var s = shuffled(rng, pick(rng, sets)), evs = ['A', 'B', 'C'].map(function (L, i) { return 'Event ' + L + ': ' + s[i]; });
    var vals = s.map(value), top = vals.indexOf(Math.max.apply(null, vals));
    var opts = ['A', 'B', 'C'].map(function (L) { return 'Event ' + L; });
    var biggestFace = s.map(function (t) { return parseFloat(t.replace('%', '').replace('/', '.')); });
    var faceTop = biggestFace.indexOf(Math.max.apply(null, biggestFace));
    var sl = [];
    if (faceTop !== top) sl.push(slipO('biggest-number', opts[faceTop], 'You picked the biggest-looking number. Write them in the same form first before comparing.'));
    return finish(1, slot, 'order', null, 'The probabilities of three events are ' + evs.join('; ') + '. Which event is the most likely?',
      { op: 'order', values: s }, choiceFixed(opts, opts[top]),
      ['Write them all as decimals.', s.map(function (t, i) { return t + ' = ' + (Math.round(vals[i] * 100) / 100); }).join('; ') + '.', 'The biggest is ' + s[top] + '.'], sl);
  }
  function s1_least(rng, slot) {
    var names = shuffled(rng, COLOURS).slice(0, 4), counts = shuffled(rng, [1, 2, 3, 4]), k = counts.indexOf(1);
    var ch = spinner(rng, names, counts);
    var most = counts.indexOf(4);
    return finish(1, slot, 'least-likely', ch, 'The spinner has 10 equal sectors. Which colour is the least likely to come up?',
      { op: 'least' }, choiceFixed(names, names[k]),
      ['Count the sectors of each colour.', 'The colour with the fewest sectors is the least likely: ' + names[k] + '.'],
      [slipO('most-not-least', names[most], 'That is the MOST likely colour: it has the most sectors.')]);
  }
  var S1 = [s1_sectors, s1_wordvalue, s1_wordevent, s1_place, s1_bag, s1_fracdec, s1_fracpct, s1_decfrac, s1_cards, s1_cannot, s1_order, s1_least];

  /* =====================================================================================================
     STAGE 2: not, and the missing one
     ===================================================================================================== */
  function s2_notfrac(rng, slot) {
    var d = rint(rng, 5, 12), n = rint(rng, 2, d - 2);
    return finish(2, slot, 'not-frac', null, 'The probability that a train is late is ' + fs(n, d) + '. What is the probability that it is NOT late?',
      { op: 'not-frac', n: n, d: d }, frac(d - n, d),
      ['The two probabilities add up to 1.', '1 = ' + fs(d, d) + '.', fs(d, d) + ' - ' + fs(n, d) + ' = ' + fs(d - n, d) + '.'],
      [slipF('one-from-the-top', n - 1, d, 'You took 1 off the top number only. Take the whole probability away from 1: ' + fs(d, d) + ' - ' + fs(n, d) + '.'),
       slipF('whole-number', d - n, 1, 'That is the number of "not late" parts, not a probability. A probability is a part of the whole: ' + fs(d - n, d) + '.')]);
  }
  function s2_notdec(rng, slot) {
    var h = pick(rng, [5, 10, 15, 20, 25, 30, 35, 40, 45, 55, 60, 65, 70, 85]);
    return finish(2, slot, 'not-dec', null, 'The probability that it rains on a school trip day is ' + dec(h) + '. What is the probability that it does NOT rain?',
      { op: 'not-dec', h: h }, numA(dec(100 - h)),
      ['P(not rain) = 1 - P(rain).', '1 - ' + dec(h) + ' = ' + dec(100 - h) + '.'],
      [slipN('whole-number', String(100 - h), 'A probability is between 0 and 1. ' + (100 - h) + ' is hundredths: write it as ' + dec(100 - h) + '.'),
       slipN('take-from-ten', dec(1000 - h), 'Take it away from 1, not from 10.')]);
  }
  function s2_notpct(rng, slot) {
    var p = pick(rng, [5, 10, 15, 20, 25, 30, 35, 40, 45, 55, 60, 65, 70, 85]);
    return finish(2, slot, 'not-pct', null, 'There is a ' + p + '% chance that a bus is full. What is the percentage chance that it is NOT full?',
      { op: 'not-pct', p: p }, numA(100 - p, '%'),
      ['The chances add up to 100%.', '100 - ' + p + ' = ' + (100 - p) + '.'],
      [slipN('same-number', String(p), 'That is the chance that it IS full. Take it away from 100%.'),
       slipN('decimal', dec(100 - p), 'That is a decimal. The box wants a percentage, ' + (100 - p) + '.')]);
  }
  function s2_notbag(rng, slot) {
    var names = shuffled(rng, COLOURS).slice(0, 3), counts = [rint(rng, 2, 6), rint(rng, 2, 6), rint(rng, 1, 5)], t = sum(counts);
    var stem = 'A bag has ' + counts[0] + ' ' + names[0] + ', ' + counts[1] + ' ' + names[1] + ' and ' + counts[2] + ' ' + names[2] + ' counters. One is taken at random. What is the probability that it is NOT ' + names[0] + '?';
    return finish(2, slot, 'not-bag', bag(names, counts), stem, { op: 'not-bag', counts: counts }, frac(t - counts[0], t),
      ['Counters that are not ' + names[0] + ': ' + counts[1] + ' + ' + counts[2] + ' = ' + (t - counts[0]) + '.', 'All the counters: ' + t + '.', 'P = ' + fs(t - counts[0], t) + '.'],
      [slipF('the-colour-itself', counts[0], t, 'That is P(' + names[0] + '), the colour you were told to leave out.'),
       slipF('one-from-the-top', counts[0] - 1, t, 'Take the probability of ' + names[0] + ' away from 1, not 1 from the top number.')]);
  }
  var TABLE_OUT = [['Red', 'Blue', 'Green', 'Yellow'], ['Walk', 'Bus', 'Car', 'Bike'], ['Pizza', 'Pasta', 'Salad', 'Soup'], ['Win', 'Draw', 'Lose', 'Abandoned']];
  function s2_tabledec(rng, slot) {
    var labs = pick(rng, TABLE_OUT), v = [rint(rng, 1, 4) * 5 + 5, rint(rng, 1, 4) * 5 + 5, rint(rng, 1, 4) * 5 + 5];
    var miss = 100 - sum(v), k = rint(rng, 0, 3);
    var hs = v.slice(); hs.splice(k, 0, miss);
    if (miss < 5) return s2_tabledec(rng, slot);
    var row = hs.map(function (h, i) { return i === k ? '?' : dec(h); });
    return finish(2, slot, 'table-dec', { type: 'table', head: labs, rows: [row] }, 'The table shows the probabilities of the four possible results. The probabilities add up to 1. Find the missing probability.',
      { op: 'table-missing-dec', hs: hs, k: k }, numA(dec(miss)),
      ['All the probabilities add up to 1.', 'Add the three given: ' + dec(sum(v)) + '.', '1 - ' + dec(sum(v)) + ' = ' + dec(miss) + '.'],
      [slipN('sum-not-taken-from-1', dec(sum(v)), 'That is the total of the three you were given. Take it away from 1.'),
       slipN('whole-number', String(miss), 'Write it as a decimal: ' + dec(miss) + '.')]);
  }
  function s2_tablefrac(rng, slot) {
    var labs = pick(rng, TABLE_OUT), d = pick(rng, [8, 10, 12, 20]);
    var a = rint(rng, 1, Math.floor(d / 4)), b = rint(rng, 1, Math.floor(d / 4)), c = rint(rng, 1, Math.floor(d / 4)), m = d - a - b - c;
    if (m < 1) return s2_tablefrac(rng, slot);
    var ns = [a, b, c], k = rint(rng, 0, 3); ns.splice(k, 0, m);
    var row = ns.map(function (x, i) { return i === k ? '?' : fs(x, d); });
    return finish(2, slot, 'table-frac', { type: 'table', head: labs, rows: [row] }, 'The table shows the probabilities of the four possible results. They add up to 1. Find the missing probability, as a fraction.',
      { op: 'table-missing-frac', ns: ns, d: d, k: k }, frac(m, d),
      ['All the probabilities add up to 1, which is ' + fs(d, d) + '.', 'The three given add to ' + fs(d - m, d) + '.', fs(d, d) + ' - ' + fs(d - m, d) + ' = ' + fs(m, d) + '.'],
      [slipF('sum-not-taken-from-1', d - m, d, 'That is the total of the three given. Take it away from 1.'),
       slipF('top-only', m, 1, 'Keep the denominator ' + d + ': the answer is ' + fs(m, d) + '.')]);
  }
  function s2_x2x_find(rng, slot) {                // A = x, B = 2x, C = c: find P(B)
    var x = pick(rng, [5, 10, 15, 20, 25]), c = 100 - 3 * x;
    var labs = pick(rng, TABLE_OUT).slice(0, 3);
    return finish(2, slot, 'x-2x-b', { type: 'table', head: labs, rows: [['x', '2x', dec(c)]] }, 'A game can end in three ways. The probabilities are x, 2x and ' + dec(c) + '. They add up to 1. Find the probability shown as 2x.',
      { op: 'x2x', c: c, find: 'B' }, numA(dec(2 * x)),
      ['x + 2x + ' + dec(c) + ' = 1, so 3x = ' + dec(100 - c) + '.', 'x = ' + dec(100 - c) + ' / 3 = ' + dec(x) + '.', '2x = ' + dec(2 * x) + '.'],
      [slipN('x-not-doubled', dec(x), 'That is x. The question asks for 2x, which is double.'),
       slipN('not-divided', dec(100 - c), 'That is 3x. Divide it by 3 to get x, then double.'),
       slipN('sum-not-taken-from-1', dec(c), 'That is the probability you were given. Use 1 - ' + dec(c) + ' to find 3x first.')]);
  }
  function s2_x2x_four(rng, slot) {                // A = x, B = 2x, C and D fractions over 20: find x as a fraction
    var a = rint(rng, 1, 4), d = 20, x3 = 3 * a, rest = d - x3;
    var c = rint(rng, 1, rest - 1), e = rest - c;
    var labs = pick(rng, TABLE_OUT);
    return finish(2, slot, 'x-2x-four', { type: 'table', head: labs, rows: [['x', '2x', fs(c, d), fs(e, d)]] }, 'Four results have probabilities x, 2x, ' + fs(c, d) + ' and ' + fs(e, d) + '. They add up to 1. Find x, as a fraction.',
      { op: 'x2x-four', c: c, e: e, d: d }, frac(a, d),
      ['The known two add to ' + fs(rest, d) + '.', '3x = ' + fs(d, d) + ' - ' + fs(rest, d) + ' = ' + fs(x3, d) + '.', 'x = ' + fs(x3, d) + ' / 3 = ' + fs(a, d) + '.'],
      [slipF('not-divided', x3, d, 'That is 3x. Divide by 3 to get x.'),
       slipF('x-2x-mixed', 2 * a, d, 'That is 2x. The question asks for x.')]);
  }
  function s2_tablepct(rng, slot) {
    var v = [rint(rng, 2, 6) * 5, rint(rng, 2, 6) * 5, rint(rng, 2, 6) * 5], m = 100 - sum(v), labs = pick(rng, TABLE_OUT), k = rint(rng, 0, 3);
    var ps = v.slice(); ps.splice(k, 0, m);
    return finish(2, slot, 'table-pct', { type: 'table', head: labs, rows: [ps.map(function (p, i) { return i === k ? '?' : p + '%'; })] },
      'The table shows the chances of the four possible results, as percentages. They add up to 100%. Find the missing percentage.',
      { op: 'table-missing-pct', ps: ps, k: k }, numA(m, '%'),
      ['The percentages add up to 100.', 'The three given add to ' + sum(v) + '.', '100 - ' + sum(v) + ' = ' + m + '.'],
      [slipN('sum-not-taken-from-1', String(sum(v)), 'That is the total of the three given. Take it away from 100.'),
       slipN('decimal', dec(m), 'Write it as a percentage, ' + m + ', not as a decimal.')]);
  }
  function s2_either(rng, slot) {
    var a = pick(rng, [10, 15, 20, 25, 30]), b = pick(rng, [10, 15, 20, 25, 35]);
    return finish(2, slot, 'either-or', null, 'The probability that a bus is early is ' + dec(a) + '. The probability that it is on time is ' + dec(b) + '. It cannot be both. What is the probability that it is early or on time?',
      { op: 'either', a: a, b: b }, numA(dec(a + b)),
      ['It cannot be both, so add the probabilities.', dec(a) + ' + ' + dec(b) + ' = ' + dec(a + b) + '.'],
      [slipN('multiplied', String(a * b / 10000), 'You multiplied. For "or" with events that cannot both happen, add.'),
       slipN('one-minus-sum', dec(100 - a - b), 'That is the probability it is neither early nor on time.')]);
  }
  function s2_neither(rng, slot) {
    var a = pick(rng, [10, 15, 20, 25, 30]), b = pick(rng, [10, 15, 20, 25, 35]);
    return finish(2, slot, 'neither', null, 'The probability that a bus is early is ' + dec(a) + '. The probability that it is on time is ' + dec(b) + '. It cannot be both. Otherwise it is late. What is the probability that it is late?',
      { op: 'neither', a: a, b: b }, numA(dec(100 - a - b)),
      ['Early or on time: ' + dec(a) + ' + ' + dec(b) + ' = ' + dec(a + b) + '.', 'Late is everything else: 1 - ' + dec(a + b) + ' = ' + dec(100 - a - b) + '.'],
      [slipN('sum-not-taken-from-1', dec(a + b), 'That is the probability it is early or on time. Late is the rest: take it away from 1.')]);
  }
  function s2_counts(rng, slot) {
    var t = pick(rng, [30, 40, 50, 60]), a = rint(rng, 6, Math.floor(t / 3)), b = rint(rng, 6, Math.floor(t / 3)), m = t - a - b;
    var labs = ['Walk', 'Cycle', 'Bus', 'Total'], k = 2;
    return finish(2, slot, 'counts-missing', { type: 'table', head: labs, rows: [[String(a), String(b), '?', String(t)]] },
      'A student is chosen at random from ' + t + ' students. The table shows how many walk and how many cycle to school. Everyone else comes by bus. What is the probability that the student comes by bus?',
      { op: 'counts-missing', a: a, b: b, t: t }, frac(m, t),
      ['Bus = ' + t + ' - ' + a + ' - ' + b + ' = ' + m + '.', 'P(bus) = ' + fs(m, t) + '.'],
      [slipF('sum-not-taken', a + b, t, 'That is P(walk or cycle). The bus students are the rest.'),
       slipF('count-only', m, 1, 'That is the number of students. A probability is the number out of ' + t + '.')]);
  }
  var S2 = [s2_notfrac, s2_notdec, s2_notpct, s2_notbag, s2_tabledec, s2_tablefrac, s2_x2x_find, s2_x2x_four, s2_tablepct, s2_either, s2_neither, s2_counts];

  /* =====================================================================================================
     STAGE 3: listing outcomes
     ===================================================================================================== */
  function diceGrid() {
    var rows = [], i, j;
    for (i = 1; i <= 6; i++) { var r = []; for (j = 1; j <= 6; j++) r.push(String(i + j)); rows.push(r); }
    return { type: 'grid', corner: '+', rowHead: [1, 2, 3, 4, 5, 6].map(String), colHead: [1, 2, 3, 4, 5, 6].map(String), cells: rows };
  }
  function nGrid(n, m, f, corner) {
    var rows = [], i, j;
    for (i = 1; i <= n; i++) { var r = []; for (j = 1; j <= m; j++) r.push(String(f(i, j))); rows.push(r); }
    return { type: 'grid', corner: corner || '+', rowHead: rows.map(function (_, k) { return String(k + 1); }), colHead: rows[0].map(function (_, k) { return String(k + 1); }), cells: rows };
  }
  function s3_twospin(rng, slot) {
    var a = rint(rng, 2, 5), b = rint(rng, 2, 5); if (a === b) b = a === 5 ? 3 : a + 1;
    var nums = function (n) { var l = []; for (var i = 1; i <= n; i++) l.push(i); return l.join(', '); };
    return finish(3, slot, 'two-spinners', null, 'Spinner A shows ' + nums(a) + '. Spinner B shows ' + nums(b) + '. Both are spun. How many different outcomes are there?',
      { op: 'product', factors: [a, b] }, numA(a * b),
      ['Each of the ' + a + ' results on A can go with each of the ' + b + ' results on B.', a + ' x ' + b + ' = ' + (a * b) + '.'],
      [slipN('added', a + b, 'You added. Each result on A pairs with EVERY result on B, so multiply.')]);
  }
  function s3_coindice(rng, slot) {
    var k = pick(rng, [2, 3]);
    var what = k === 2 ? ['a coin', 'two sides', 'heads and tails'] : ['a three-sided spinner (1, 2, 3)', 'three results', '1, 2 and 3'];
    return finish(3, slot, 'coin-dice', null, 'A fair dice is rolled and ' + what[0] + ' is used too. How many different outcomes are there altogether?',
      { op: 'product', factors: [6, k] }, numA(6 * k),
      ['The dice has 6 results.', 'The other has ' + k + '.', '6 x ' + k + ' = ' + (6 * k) + '.'],
      [slipN('added', 6 + k, 'You added. Multiply the numbers of results.')]);
  }
  function s3_menu(rng, slot) {
    var s = rint(rng, 2, 4), m = rint(rng, 2, 5), d = rint(rng, 2, 3);
    return finish(3, slot, 'menu', null, 'A set meal has a choice of ' + s + ' starters, ' + m + ' main courses and ' + d + ' puddings. You choose one of each. How many different meals are possible?',
      { op: 'product', factors: [s, m, d] }, numA(s * m * d),
      ['Multiply the choices: ' + s + ' x ' + m + ' x ' + d + '.', 'That is ' + (s * m * d) + ' meals.'],
      [slipN('added', s + m + d, 'You added the choices. Each starter can go with every main and every pudding: multiply.'),
       slipN('two-only', s * m, 'You left out the puddings. Multiply all three choices.')]);
  }
  function s3_sum(rng, slot) {
    var t = pick(rng, [3, 4, 5, 6, 8, 9, 10, 11]), fav = 6 - Math.abs(7 - t), unord = Math.ceil(fav / 2);
    var l = lowest(fav, 36);
    return finish(3, slot, 'dice-sum', diceGrid(), 'Two fair dice are rolled and the scores are added. The table shows all 36 equally likely totals. What is the probability that the total is ' + t + '?',
      { op: 'dice-sum', t: t }, frac(fav, 36),
      ['Count the ' + t + 's in the table: ' + fav + '.', 'There are 36 equally likely outcomes.', 'P = ' + fs(fav, 36) + (l.n !== fav ? ' = ' + fs(l.n, l.d) : '') + '.'],
      [slipF('totals-equally-likely', 1, 11, 'The totals are NOT equally likely. Use the 36 equally likely outcomes in the table.'),
       slipF('2+3-and-3+2-as-one', unord, 21, '2 + 3 and 3 + 2 are different outcomes. Count both: there are 36 outcomes in all, not 21.')]);
  }
  function s3_double(rng, slot) {
    return finish(3, slot, 'dice-double', diceGrid(), 'Two fair dice are rolled. What is the probability that both show the same number?',
      { op: 'dice-double' }, frac(6, 36),
      ['The same number on both: 1-1, 2-2, 3-3, 4-4, 5-5, 6-6. That is 6 outcomes.', 'There are 36 outcomes in all.', 'P = 6/36 = 1/6.'],
      [slipF('2+3-and-3+2-as-one', 6, 21, 'There are 36 equally likely outcomes, because 2-3 and 3-2 are different outcomes.'),
       slipF('part-to-part', 6, 30, 'That compares doubles with non-doubles. The bottom is ALL the outcomes, 36.')]);
  }
  function s3_over(rng, slot) {
    var k = pick(rng, [8, 9, 10]), more = pick(rng, [true, false]), fav = 0, i, j, ties = 0;
    for (i = 1; i <= 6; i++) for (j = 1; j <= 6; j++) { if (more ? i + j > k : i + j < k - 5) fav++; if (i + j === (more ? k : k - 5)) ties++; }
    var th = more ? k : k - 5, word = more ? 'more than ' + k : 'less than ' + th;
    return finish(3, slot, 'dice-over', diceGrid(), 'Two fair dice are rolled and the scores are added. What is the probability that the total is ' + word + '?',
      { op: 'dice-over', th: th, more: more }, frac(fav, 36),
      ['Count the totals ' + word + ' in the table: ' + fav + '.', 'P = ' + fs(fav, 36) + '.'],
      [slipF('boundary-included', fav + ties, 36, 'The total ' + th + ' itself is not ' + word + '. Leave it out.')]);
  }
  function s3_spin34(rng, slot) {
    var A = 3, B = pick(rng, [3, 4]), t = pick(rng, [3, 4, 5]), fav = 0, i, j, tots = {};
    for (i = 1; i <= A; i++) for (j = 1; j <= B; j++) { if (i + j === t) fav++; tots[i + j] = 1; }
    var distinct = Object.keys(tots).length;
    return finish(3, slot, 'spinner-grid', nGrid(A, B, function (i2, j2) { return i2 + j2; }),
      'Spinner A shows 1, 2, 3. Spinner B shows 1' + (B === 3 ? ', 2, 3' : ', 2, 3, 4') + '. Both are spun and the scores added. The table shows all the outcomes. What is the probability that the total is ' + t + '?',
      { op: 'spinner-grid', A: A, B: B, t: t }, frac(fav, A * B),
      ['Count the ' + t + 's in the table: ' + fav + '.', 'There are ' + (A * B) + ' equally likely outcomes.', 'P = ' + fs(fav, A * B) + '.'],
      [slipF('totals-equally-likely', 1, distinct, 'The totals are not equally likely. Use all ' + (A * B) + ' outcomes in the table.')]);
  }
  function s3_coindie(rng, slot) {
    var cells = [];
    ['H', 'T'].forEach(function (c) { var r = []; for (var i = 1; i <= 6; i++) r.push(c + i); cells.push(r); });
    return finish(3, slot, 'coin-dice-grid', { type: 'grid', corner: '', rowHead: ['Coin H', 'Coin T'], colHead: ['1', '2', '3', '4', '5', '6'], cells: cells, flat: true },
      'A fair coin is flipped and a fair dice is rolled. The table lists every outcome. What is the probability of getting heads AND an even number?',
      { op: 'coin-dice-even' }, frac(3, 12),
      ['Heads with an even number: H2, H4, H6. That is 3 outcomes.', 'There are 12 outcomes in all.', 'P = 3/12 = 1/4.'],
      [slipF('added', 12, 12, 'You added the chances. For "AND" you need the outcomes that satisfy both: H2, H4, H6.'),
       slipF('heads-only', 6, 12, 'That is every outcome with heads. It must be an even number too.')]);
  }
  function s3_twocoins(rng, slot) {
    return finish(3, slot, 'two-coins', null, 'Two fair coins are flipped. What is the probability of getting at least one head?',
      { op: 'two-coins' }, frac(3, 4),
      ['List all the outcomes: HH, HT, TH, TT. That is 4.', 'At least one head: HH, HT, TH. That is 3.', 'P = 3/4.'],
      [slipF('2+3-and-3+2-as-one', 2, 3, 'HT and TH are different outcomes. Count both: there are 4 outcomes in all.'),
       slipF('half', 1, 2, 'Listing the outcomes gives 3 out of 4.')]);
  }
  function s3_always(rng, slot) {
    var t = pick(rng, [7, 2, 12, 6, 3]);
    var right = 'No: the totals are not equally likely', opts = [right, 'Yes: there are 11 totals', 'No: it is 1/12'];
    return finish(3, slot, 'eleven-totals', null, 'Dan says: "Two dice can give 11 different totals, from 2 to 12. So the probability of a total of ' + t + ' is 1/11." Is he right?',
      { op: 'eleven-totals', t: t }, choiceFixed(opts, right),
      ['Some totals can be made in more ways than others.', 'A total of 7 can be made 6 ways but 2 only 1 way.', 'So the totals are not equally likely, and 1/11 is wrong.'],
      [slipO('totals-equally-likely', opts[1], 'The 11 totals are not equally likely, so you cannot share 1 equally between them.'),
       slipO('twelve', opts[2], 'Nothing makes it 1/12. Count the ways each total can happen out of the 36 outcomes.')]);
  }
  function s3_menuprob(rng, slot) {
    var s = rint(rng, 2, 4), m = rint(rng, 2, 4);
    return finish(3, slot, 'menu-chance', null, 'A cafe set meal has ' + s + ' starters and ' + m + ' main courses. A customer picks one of each at random. What is the probability that they pick the soup and the pie (one particular starter and one particular main)?',
      { op: 'menu-chance', s: s, m: m }, frac(1, s * m),
      ['All the meals: ' + s + ' x ' + m + ' = ' + (s * m) + '.', 'One particular meal: 1 out of ' + (s * m) + '.'],
      [slipF('added', 1, s + m, 'You added the choices. Multiply them to count the meals.')]);
  }
  var S3 = [s3_twospin, s3_coindice, s3_menu, s3_sum, s3_double, s3_over, s3_spin34, s3_coindie, s3_twocoins, s3_always, s3_menuprob,
    function (rng, slot) {                          // two spinners the same: P(total t) with unordered slip
      var n = 4, t = pick(rng, [3, 4, 5, 6]), fav = 0, i, j;
      for (i = 1; i <= n; i++) for (j = 1; j <= n; j++) if (i + j === t) fav++;
      var un = 0; for (i = 1; i <= n; i++) for (j = i; j <= n; j++) if (i + j === t) un++;
      return finish(3, slot, 'same-spinners', nGrid(n, n, function (a, b) { return a + b; }),
        'A spinner shows 1, 2, 3, 4 and is spun twice. The scores are added. The table shows all 16 outcomes. What is the probability that the total is ' + t + '?',
        { op: 'same-spinners', n: n, t: t }, frac(fav, 16),
        ['Count the ' + t + 's in the table: ' + fav + '.', 'There are 16 outcomes in all.', 'P = ' + fs(fav, 16) + '.'],
        [slipF('2+3-and-3+2-as-one', un, 10, '1 then 3 and 3 then 1 are different outcomes. There are 16 outcomes, not 10.')]);
    }];

  /* =====================================================================================================
     STAGE 4: expected and relative frequency
     ===================================================================================================== */
  function s4_expected(rng, slot) {
    var d = pick(rng, [5, 10, 4]), n = rint(rng, 1, d - 1), g = pick(rng, [2, 3, 4, 5]), trials = d * g, p = dec(n * 100 / d);
    var key = trials * n / d;
    return finish(4, slot, 'expected-dec', null, 'The probability that a seed grows is ' + p + '. Ruth plants ' + trials + ' seeds. How many would you expect to grow?',
      { op: 'expected', n: n, d: d, trials: trials }, numA(key),
      ['Expected number = probability x number of trials.', p + ' x ' + trials + ' = ' + key + '.'],
      [slipN('divided', (trials * d) % n === 0 ? trials * d / n : -1, 'You divided. Multiply the probability by the number of trials.'),
       slipN('trials-minus', trials - key, 'That is the number you would expect NOT to grow.')].filter(function (x) { return x.answer.key !== '-1'; }));
  }
  function s4_expectedfrac(rng, slot) {
    var d = pick(rng, [6, 8, 5, 10]), n = rint(rng, 1, d - 1), k = rint(rng, 2, 8), trials = d * k;
    return finish(4, slot, 'expected-frac', null, 'The probability that a bus is late is ' + fs(n, d) + '. In a term there are ' + trials + ' bus journeys. How many would you expect to be late?',
      { op: 'expected', n: n, d: d, trials: trials }, numA(trials * n / d),
      ['Expected number = probability x number of trials.', fs(n, d) + ' of ' + trials + ' = ' + (trials / d) + ' x ' + n + ' = ' + (trials * n / d) + '.'],
      [slipN('divided', (trials * d) % n === 0 ? trials * d / n : -1, 'You divided by the probability. Multiply instead.'),
       slipN('one-part', trials / d, 'That is one part (' + fs(1, d) + '). You need ' + n + ' parts.')].filter(function (x) { return x.answer.key !== '-1'; }));
  }
  function s4_expectedpct(rng, slot) {
    var p = pick(rng, [10, 20, 25, 30, 40, 5, 15]), trials = pick(rng, [200, 300, 400, 500, 600]);
    return finish(4, slot, 'expected-pct', null, 'A machine fails ' + p + '% of the time. It is used ' + trials + ' times. How many failures would you expect?',
      { op: 'expected-pct', p: p, trials: trials }, numA(trials * p / 100),
      [p + '% = ' + dec(p) + '.', dec(p) + ' x ' + trials + ' = ' + (trials * p / 100) + '.'],
      [slipN('percent-as-number', trials * p, 'You multiplied by ' + p + ' not ' + p + '%. ' + p + '% of ' + trials + ' is ' + (trials * p / 100) + '.'),
       slipN('trials-minus', trials - trials * p / 100, 'That is the number you would expect NOT to fail.')]);
  }
  function s4_relfrac(rng, slot) {
    var t = pick(rng, [20, 25, 40, 50, 80, 100]), k = rint(rng, 3, t - 4);
    return finish(4, slot, 'rel-freq-frac', null, 'Mina spins a spinner ' + t + ' times and it lands on green ' + k + ' times. What is the relative frequency of green? Give it as a fraction.',
      { op: 'rel-freq', k: k, t: t }, frac(k, t),
      ['Relative frequency = number of times / number of trials.', fs(k, t) + '.'],
      [slipF('upside-down', t, k, 'You turned it upside down: the number of trials goes at the bottom.'),
       slipF('part-to-part', k, t - k, 'That compares green with not green. The bottom is all ' + t + ' spins.')]);
  }
  function s4_reldec(rng, slot) {
    var t = pick(rng, [20, 25, 40, 50, 100]), k = rint(rng, 2, t - 3), h = k * 100 / t;
    if (h !== Math.floor(h)) return s4_reldec(rng, slot);
    return finish(4, slot, 'rel-freq-dec', null, 'Sam rolls a dice ' + t + ' times. It shows a six ' + k + ' times. What is the relative frequency of a six? Give it as a decimal.',
      { op: 'rel-freq-dec', k: k, t: t }, numA(dec(h)),
      ['Relative frequency = ' + fs(k, t) + '.', 'As a decimal: ' + dec(h) + '.'],
      [slipN('not-the-event', dec(100 - h), 'That is the relative frequency of NOT getting a six. You need the sixes: ' + k + ' out of ' + t + '.'),
       slipN('percent', String(h), 'That is a percentage. The box wants a decimal, ' + dec(h) + '.')]);
  }
  function s4_resulttable(rng, slot) {
    var names = shuffled(rng, COLOURS).slice(0, 3), c = [rint(rng, 3, 9), rint(rng, 3, 9), rint(rng, 3, 9)], t = sum(c);
    var k = rint(rng, 0, 2);
    return finish(4, slot, 'result-table', { type: 'table', head: names.concat(['Total']), rows: [c.map(String).concat([String(t)])] },
      'Zoe spins a spinner and records where it lands. Use her results to estimate the probability that it lands on ' + names[k] + '. Give it as a fraction.',
      { op: 'rel-freq', k: c[k], t: t }, frac(c[k], t),
      ['Relative frequency of ' + names[k] + ' = ' + c[k] + ' / ' + t + '.', 'That is ' + fs(c[k], t) + '.'],
      [slipF('part-to-part', c[k], t - c[k], 'That compares ' + names[k] + ' with the other colours. The bottom is the total, ' + t + '.'),
       slipF('one-colour-of-three', 1, 3, 'The results are not equal, so it is not 1 out of 3. Use her results.')]);
  }
  function s4_reliable(rng, slot) {
    var A = rint(rng, 8, 20), B = rint(rng, 8, 10) * 25;
    var opts = ['Cara (' + B + ' spins)', 'Ben (' + A + ' spins)', 'They are equally reliable'];
    return finish(4, slot, 'more-reliable', null, 'Ben spins a spinner ' + A + ' times and estimates the probability of red. Cara spins the same spinner ' + B + ' times and estimates it too. Whose estimate is likely to be more reliable?',
      { op: 'more-reliable', a: A, b: B }, choiceFixed(opts, opts[0]),
      ['The more trials, the closer the relative frequency usually is to the true probability.', 'Cara spun more times (' + B + ' against ' + A + ').'],
      [slipO('few-trials', opts[1], 'Ben did far fewer spins. A small number of trials can give an unusual result.'),
       slipO('equal', opts[2], 'More trials give a better estimate, so they are not equally reliable.')]);
  }
  function s4_fair(rng, slot) {
    var few = rng() < 0.3, counts, t, right, opts = ['Probably fair', 'Probably not fair', "You can't tell"];
    if (few) {
      t = 12; counts = [2, 3, 1, 2, 1, 3]; counts = shuffled(rng, counts); right = opts[2];
    } else if (rng() < 0.5) {
      t = 60; var e = [rint(rng, -3, 3), rint(rng, -3, 3), rint(rng, -3, 3), rint(rng, -3, 3), rint(rng, -3, 3)]; counts = e.map(function (x) { return 10 + x; }); counts.push(60 - sum(counts));
      if (Math.max.apply(null, counts) > 14 || Math.min.apply(null, counts) < 6) return s4_fair(rng, slot);
      counts = shuffled(rng, counts); right = opts[0];
    } else {
      t = 60; var hi = rint(rng, 18, 22), lo = rint(rng, 2, 5); var rest = 60 - hi - lo, r4 = [0, 0, 0, 0];
      for (var i = 0; i < rest; i++) r4[i % 4]++;
      counts = shuffled(rng, [hi, lo].concat(r4)); right = opts[1];
    }
    var worked = few ? ['Only 12 throws. Each face is expected about 2 times.', 'That is too few throws to judge: you cannot tell.'] :
      ['Fair dice: each face is expected about ' + (t / 6) + ' times in ' + t + ' throws.', right === opts[0] ? 'These are all close to ' + (t / 6) + '.' : 'One face is far from ' + (t / 6) + ' (' + Math.max.apply(null, counts) + ' and ' + Math.min.apply(null, counts) + ').'];
    return finish(4, slot, 'is-it-fair', { type: 'table', head: ['1', '2', '3', '4', '5', '6'], rows: [counts.map(String)], caption: 'Score on the dice' },
      'A dice is thrown ' + t + ' times. The table shows how many times each score came up. Is the dice fair?',
      { op: 'fair', counts: counts }, choiceFixed(opts, right), worked,
      opts.filter(function (o) { return o !== right; }).map(function (o) {
        return slipO('wrong-verdict', o, o === opts[2] ? 'With ' + t + ' throws there is enough to decide.' : (o === opts[0] ? 'Look at the face that is far away from the others.' : 'These are close to what a fair dice would give.'));
      }));
  }
  function s4_gambler(rng, slot) {
    var k = pick(rng, [4, 5, 6]), c = pick(rng, ['heads', 'tails']);
    var opts = ['1/2', 'More than 1/2: the other side is due', 'Less than 1/2'];
    var other = c === 'heads' ? 'tails' : 'heads';
    opts[1] = 'More than 1/2: ' + other + ' is due';
    return finish(4, slot, 'gambler', null, 'A fair coin lands on ' + c + ' ' + k + ' times in a row. What is the probability that it lands on ' + other + ' next time?',
      { op: 'gambler' }, choiceFixed(opts, opts[0]),
      ['Each flip is independent: the coin does not remember.', 'The probability is still 1/2.'],
      [slipO('gamblers-fallacy', opts[1], 'The coin has no memory. Each flip is a fresh 1/2.'),
       slipO('streak-continues', opts[2], 'The coin does not remember the streak. Each flip is still 1/2.')]);
  }
  function s4_notexpected(rng, slot) {
    var p = pick(rng, [10, 20, 30, 40]), days = pick(rng, [50, 100, 150, 200]);
    return finish(4, slot, 'expected-not', null, 'The probability of rain on any day is ' + dec(p) + '. Over ' + days + ' days, how many days would you expect to be dry?',
      { op: 'expected-not', p: p, days: days }, numA(days * (100 - p) / 100),
      ['P(dry) = 1 - ' + dec(p) + ' = ' + dec(100 - p) + '.', dec(100 - p) + ' x ' + days + ' = ' + (days * (100 - p) / 100) + '.'],
      [slipN('wrong-event', days * p / 100, 'That is the number of RAINY days. The question asks for dry days.')]);
  }
  function s4_expectedfromrel(rng, slot) {
    var t = pick(rng, [20, 40, 50]), k = pick(rng, [3, 4, 5, 6, 8, 9]), days = pick(rng, [200, 400, 500, 600, 1000]);
    if ((days * k) % t !== 0) return s4_expectedfromrel(rng, slot);
    return finish(4, slot, 'expected-from-rel', null, 'In a test, a spinner landed on blue ' + k + ' times in ' + t + ' spins. Use this to estimate how many times it would land on blue in ' + days + ' spins.',
      { op: 'expected-from-rel', k: k, t: t, trials: days }, numA(days * k / t),
      ['Relative frequency of blue = ' + fs(k, t) + '.', fs(k, t) + ' x ' + days + ' = ' + (days * k / t) + '.'],
      [slipN('not-blue', days - days * k / t, 'That is the number of spins you would expect NOT to land on blue.'),
       slipN('divided', days * t / k, 'You divided by the relative frequency. Multiply.')]);
  }
  var S4 = [s4_expected, s4_expectedfrac, s4_expectedpct, s4_relfrac, s4_reldec, s4_resulttable, s4_reliable, s4_fair, s4_gambler, s4_notexpected, s4_expectedfromrel,
    function (rng, slot) {                          // two samples of different sizes: pick the closer-to-true
      var fairP = '1/6', a = rint(rng, 8, 15), b = rint(rng, 4, 8) * 50, ka = Math.max(1, Math.round(a / 3)), kb = Math.round(b / 6);
      var opts = ['Amy (' + b + ' throws)', 'Raj (' + a + ' throws)'];
      return finish(4, slot, 'trust-many', null, 'Raj throws a dice ' + a + ' times and gets ' + ka + ' sixes. Amy throws the same dice ' + b + ' times and gets ' + kb + ' sixes. Whose result should you trust more to estimate the probability of a six?',
        { op: 'more-reliable', a: a, b: b }, choiceFixed(opts, opts[0]),
        ['More throws give a better estimate.', 'Amy threw ' + b + ' times, Raj only ' + a + '.'],
        [slipO('few-trials', opts[1], 'Raj threw far fewer times. A small number of trials can be unusual.')]);
    }];

  /* =====================================================================================================
     STAGE 5: tree diagrams (independent events, no replacement)
     ===================================================================================================== */
  var TREE_CTX = [
    { a: 'It is windy', b: 'The match is cancelled', n: 'It is not windy', m: 'The match is not cancelled' },
    { a: 'Dev scores', b: 'Eve scores', n: 'Dev misses', m: 'Eve misses' },
    { a: 'The first bus is late', b: 'The second bus is late', n: 'The first bus is on time', m: 'The second bus is on time' },
    { a: 'The first seed grows', b: 'The second seed grows', n: 'The first seed fails', m: 'The second seed fails' }
  ];
  function tree(p, q, ctx, hide) {                 // two independent events: P(first) = p, P(second) = q, as fractions [n,d]
    var P = [p, [p[1] - p[0], p[1]]], Q = [q, [q[1] - q[0], q[1]]];
    return { type: 'tree', first: [{ label: 'Yes', p: fs(P[0][0], P[0][1]) }, { label: 'No', p: fs(P[1][0], P[1][1]) }],
      second: [[{ label: 'Yes', p: hide === 'q1' ? '?' : fs(Q[0][0], Q[0][1]) }, { label: 'No', p: fs(Q[1][0], Q[1][1]) }], [{ label: 'Yes', p: fs(Q[0][0], Q[0][1]) }, { label: 'No', p: fs(Q[1][0], Q[1][1]) }]],
      names: ['First', 'Second'] };
  }
  function pq(rng) {
    var d1 = pick(rng, [3, 4, 5, 6, 10]), d2 = pick(rng, [3, 4, 5, 6, 10]);
    return [[rint(rng, 1, d1 - 1), d1], [rint(rng, 1, d2 - 1), d2]];
  }
  function mulF(a, b) { return lowest(a[0] * b[0], a[1] * b[1]); }
  function s5_both(rng, slot) {
    var x = pq(rng), ctx = pick(rng, TREE_CTX), P = x[0], Q = x[1];
    var n = P[0] * Q[0], d = P[1] * Q[1];
    return finish(5, slot, 'tree-both', tree(P, Q, ctx), 'The tree diagram shows two independent events. First: P(Yes) = ' + fs(P[0], P[1]) + '. Second: P(Yes) = ' + fs(Q[0], Q[1]) + '. What is the probability that BOTH are Yes?',
      { op: 'tree-both', p: P, q: Q }, frac(n, d),
      ['Multiply along the branches: Yes then Yes.', fs(P[0], P[1]) + ' x ' + fs(Q[0], Q[1]) + ' = ' + fs(n, d) + '.'],
      [slipF('added-along', P[0] * Q[1] + Q[0] * P[1], P[1] * Q[1], 'You added the probabilities. Along the branches you multiply.'),
       slipF('product-tops', P[0] * Q[0], P[1] + Q[1], 'Multiply the tops AND multiply the bottoms.')]);
  }
  function s5_neither(rng, slot) {
    var x = pq(rng), P = x[0], Q = x[1], pn = P[1] - P[0], qn = Q[1] - Q[0];
    return finish(5, slot, 'tree-neither', tree(P, Q, TREE_CTX[0]), 'The tree diagram shows two independent events. First: P(Yes) = ' + fs(P[0], P[1]) + '. Second: P(Yes) = ' + fs(Q[0], Q[1]) + '. What is the probability that NEITHER is Yes (No then No)?',
      { op: 'tree-neither', p: P, q: Q }, frac(pn * qn, P[1] * Q[1]),
      ['P(No) first = ' + fs(pn, P[1]) + ', second = ' + fs(qn, Q[1]) + '.', 'Multiply along: ' + fs(pn * qn, P[1] * Q[1]) + '.'],
      [slipF('both-yes', P[0] * Q[0], P[1] * Q[1], 'That is P(Yes, Yes). You need No then No.'),
       slipF('added-along', pn * Q[1] + qn * P[1], P[1] * Q[1], 'You added. Multiply along the branches.')]);
  }
  function s5_mixed(rng, slot) {
    var x = pq(rng), P = x[0], Q = x[1], qn = Q[1] - Q[0];
    return finish(5, slot, 'tree-yes-no', tree(P, Q, TREE_CTX[1]), 'The tree diagram shows two independent events. First: P(Yes) = ' + fs(P[0], P[1]) + '. Second: P(Yes) = ' + fs(Q[0], Q[1]) + '. What is the probability that the first is Yes and the second is No?',
      { op: 'tree-yes-no', p: P, q: Q }, frac(P[0] * qn, P[1] * Q[1]),
      ['First Yes: ' + fs(P[0], P[1]) + '. Second No: ' + fs(qn, Q[1]) + '.', 'Multiply: ' + fs(P[0] * qn, P[1] * Q[1]) + '.'],
      [slipF('both-yes', P[0] * Q[0], P[1] * Q[1], 'That is Yes then Yes. The second must be No.'),
       slipF('added-along', P[0] * Q[1] + qn * P[1], P[1] * Q[1], 'You added along the branches. Multiply.')]);
  }
  function s5_exactly(rng, slot) {
    var x = pq(rng), P = x[0], Q = x[1], pn = P[1] - P[0], qn = Q[1] - Q[0], D = P[1] * Q[1];
    var key = P[0] * qn + pn * Q[0];
    return finish(5, slot, 'tree-exactly-one', tree(P, Q, TREE_CTX[2]), 'The tree diagram shows two independent events. First: P(Yes) = ' + fs(P[0], P[1]) + '. Second: P(Yes) = ' + fs(Q[0], Q[1]) + '. What is the probability that EXACTLY ONE of them is Yes?',
      { op: 'tree-exactly-one', p: P, q: Q }, frac(key, D),
      ['Two ways: Yes then No, or No then Yes.', 'Yes, No: ' + fs(P[0] * qn, D) + '. No, Yes: ' + fs(pn * Q[0], D) + '.', 'Add the two: ' + fs(key, D) + '.'],
      [slipF('only-one-way', P[0] * qn, D, 'There are TWO ways: Yes then No, and No then Yes. Add them.'),
       slipF('multiplied-between', P[0] * qn * pn * Q[0], D * D, 'Multiply along each branch, but ADD between the different ways.')]);
  }
  function s5_atleast(rng, slot) {
    var x = pq(rng), P = x[0], Q = x[1], pn = P[1] - P[0], qn = Q[1] - Q[0], D = P[1] * Q[1];
    return finish(5, slot, 'tree-at-least', tree(P, Q, TREE_CTX[3]), 'The tree diagram shows two independent events. First: P(Yes) = ' + fs(P[0], P[1]) + '. Second: P(Yes) = ' + fs(Q[0], Q[1]) + '. What is the probability that AT LEAST ONE is Yes?',
      { op: 'tree-at-least', p: P, q: Q }, frac(D - pn * qn, D),
      ['"At least one Yes" is everything except "no Yes at all".', 'P(none) = ' + fs(pn * qn, D) + '.', '1 - ' + fs(pn * qn, D) + ' = ' + fs(D - pn * qn, D) + '.'],
      [slipF('forgot-one-minus', pn * qn, D, 'That is P(none). "At least one" is 1 minus that.'),
       slipF('both-only', P[0] * Q[0], D, 'That is P(both). "At least one" also includes exactly one.')]);
  }
  function s5_missing(rng, slot) {
    var x = pq(rng), P = x[0], Q = x[1];
    return finish(5, slot, 'tree-missing', tree(P, Q, TREE_CTX[0], 'q1'), 'On the tree diagram, the probability marked ? is the chance of Yes on the second event, after the first is Yes. The events are independent, and the No branch shows ' + fs(Q[1] - Q[0], Q[1]) + '. Find the missing probability.',
      { op: 'tree-missing', q: Q }, frac(Q[0], Q[1]),
      ['The two branches from one point add up to 1.', fs(Q[1], Q[1]) + ' - ' + fs(Q[1] - Q[0], Q[1]) + ' = ' + fs(Q[0], Q[1]) + '.'],
      [slipF('the-other-branch', Q[1] - Q[0], Q[1], 'That is the No branch, which you were given. Take it away from 1.')]);
  }
  function s5_three(rng, slot) {
    var d = pick(rng, [2, 3, 4, 5]), n = 1;
    return finish(5, slot, 'three-events', null, 'The probability that a bus is on time is ' + fs(d - 1, d) + ' on any day, independently. What is the probability that it is on time on all three days of a trip?',
      { op: 'three-events', n: d - 1, d: d }, frac(Math.pow(d - 1, 3), Math.pow(d, 3)),
      ['Multiply the three probabilities: ' + fs(d - 1, d) + ' x ' + fs(d - 1, d) + ' x ' + fs(d - 1, d) + '.', '= ' + fs(Math.pow(d - 1, 3), Math.pow(d, 3)) + '.'],
      [slipF('added-along', 3 * (d - 1), d, 'Adding gives more than the probability of one day. Multiply the three.'),
       slipF('one-day-only', d - 1, d, 'That is the chance for ONE day. All three days: multiply it by itself three times.')]);
  }
  function s5_decboth(rng, slot) {
    var a = pick(rng, [2, 3, 4, 5, 6, 7, 8]), b = pick(rng, [2, 3, 4, 5, 6, 8]);
    return finish(5, slot, 'tree-dec', null, 'The probability that Kai scores a penalty is ' + dec(a * 10) + '. The probability that Lea scores hers is ' + dec(b * 10) + '. They are independent. What is the probability that BOTH score?',
      { op: 'dec-product', a: a * 10, b: b * 10 }, numA(dec(a * b)),
      ['Multiply: ' + dec(a * 10) + ' x ' + dec(b * 10) + '.', a + ' x ' + b + ' = ' + (a * b) + ', with two decimal places: ' + dec(a * b) + '.'],
      [slipN('added-along', dec(a * 10 + b * 10), 'You added. Both score: multiply.'),
       slipN('point-moved', String(a * b / 10), 'Multiplying two tenths gives hundredths: ' + dec(a * b) + '.')]);
  }
  function s5_atleastdec(rng, slot) {
    var a = pick(rng, [2, 3, 4, 5, 6]), b = pick(rng, [2, 3, 4, 5]);
    var none = (10 - a) * (10 - b), key = 100 - none;
    return finish(5, slot, 'tree-at-least-dec', null, 'A goalkeeper faces two penalties, independently. The probability of saving the first is ' + dec(a * 10) + ' and of saving the second is ' + dec(b * 10) + '. What is the probability that the keeper saves AT LEAST ONE?',
      { op: 'at-least-dec', a: a * 10, b: b * 10 }, numA(dec(key)),
      ['P(saves none) = ' + dec((10 - a) * 10) + ' x ' + dec((10 - b) * 10) + ' = ' + dec(none) + '.', 'P(at least one) = 1 - ' + dec(none) + ' = ' + dec(key) + '.'],
      [slipN('forgot-one-minus', dec(none), 'That is the chance of saving NONE. Take it away from 1.'),
       slipN('added-along', a * 10 + b * 10 <= 100 ? dec(a * 10 + b * 10) : '0', 'You added. Use 1 minus P(none).')]);
  }
  function s5_which(rng, slot) {
    var P = pick(rng, ['0.3', '0.4', '0.6', '0.7']), Q = pick(rng, ['0.2', '0.3', '0.7', '0.8']);
    var pc = (1 - parseFloat(P)).toFixed(1), qc = (1 - parseFloat(Q)).toFixed(1);
    var right = P + ' x ' + qc + ' + ' + pc + ' x ' + Q;
    var wrong1 = P + ' x ' + Q, wrong2 = P + ' + ' + Q, wrong3 = P + ' x ' + qc;
    var opts = [right, wrong1, wrong2, wrong3];
    return finish(5, slot, 'which-sum', null, 'Two independent events have probabilities ' + P + ' and ' + Q + '. Which calculation gives the probability that EXACTLY ONE of them happens?',
      { op: 'which-sum', p: P, q: Q }, choiceFixed(shuffled(rng, opts), right),
      ['Exactly one: the first happens and the second does not, OR the first does not and the second does.', 'Multiply along each branch, then add: ' + right + '.'],
      [slipO('only-one-way', wrong3, 'That is only one of the two ways. There is another: the first does not happen and the second does.'),
       slipO('both', wrong1, 'That is the probability that BOTH happen.'),
       slipO('added-along', wrong2, 'Adding the two probabilities does not give "exactly one".')]);
  }
  function s5_notatall(rng, slot) {
    var x = pq(rng), P = x[0], Q = x[1], pn = P[1] - P[0], qn = Q[1] - Q[0], D = P[1] * Q[1];
    return finish(5, slot, 'tree-first-only', tree(P, Q, TREE_CTX[1]), 'The tree diagram shows two independent events. First: P(Yes) = ' + fs(P[0], P[1]) + '. Second: P(Yes) = ' + fs(Q[0], Q[1]) + '. What is the probability that the first is No and the second is Yes?',
      { op: 'tree-no-yes', p: P, q: Q }, frac(pn * Q[0], D),
      ['First No: ' + fs(pn, P[1]) + '. Second Yes: ' + fs(Q[0], Q[1]) + '.', 'Multiply: ' + fs(pn * Q[0], D) + '.'],
      [slipF('both-yes', P[0] * Q[0], D, 'That is Yes then Yes. The first must be No.'),
       slipF('yes-no', P[0] * qn, D, 'That is Yes then No. You need No then Yes.')]);
  }
  var S5 = [s5_both, s5_neither, s5_mixed, s5_exactly, s5_atleast, s5_missing, s5_three, s5_decboth, s5_atleastdec, s5_which, s5_notatall,
    function (rng, slot) {                          // the same, but the answer is typed as a decimal for "neither"
      var a = pick(rng, [3, 4, 6, 7]), b = pick(rng, [2, 3, 5, 7]);
      return finish(5, slot, 'tree-neither-dec', null, 'The probability of rain on Saturday is ' + dec(a * 10) + '. The probability of rain on Sunday is ' + dec(b * 10) + '. The days are independent. What is the probability that it rains on NEITHER day?',
        { op: 'neither-dec', a: a * 10, b: b * 10 }, numA(dec((10 - a) * (10 - b))),
        ['P(no rain) Saturday = ' + dec((10 - a) * 10) + ', Sunday = ' + dec((10 - b) * 10) + '.', 'Multiply: ' + dec((10 - a) * (10 - b)) + '.'],
        [slipN('rain-both', dec(a * b), 'That is the chance of rain on BOTH days.'),
         slipN('added-along', (10 - a) * 10 + (10 - b) * 10 <= 100 ? dec((10 - a) * 10 + (10 - b) * 10) : '0', 'You added. Multiply the two "no rain" probabilities.')]);
    }];

  /* ---------- the bank ---------- */
  var STAGE_FN = { 1: S1, 2: S2, 3: S3, 4: S4, 5: S5 };
  function question(stage, slot, rng) {
    var q = STAGE_FN[stage][slot](rng, slot);
    q.stage = stage; q.slot = slot;
    return q;
  }
  function bank(seed) {
    var out = [];
    for (var st = 1; st <= 5; st++) for (var sl = 0; sl < SLOTS; sl++) out.push(question(st, sl, makeRng((seed || FIXED_SEED) * 131 + st * 17 + sl)));
    return out;
  }

  root.MaffsProbability = { SLOTS: SLOTS, FIXED_SEED: FIXED_SEED, makeRng: makeRng, question: question, bank: bank };
})(typeof window !== 'undefined' ? window : globalThis);
