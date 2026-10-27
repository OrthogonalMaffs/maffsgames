/* The "I Found a Mark" question templates (contract FOUND-A-MARK, Jon, 27 Oct 2026): multi-mark exam questions broken into
   the steps a marker gives method marks for.

   The bank-first source of the topic (canon 8.2.1): the game games/i-found-a-mark/ loads this file and the 6 P's could load it
   too; the questions are never copied. Pure data, no DOM. MaffsFoundAMark.question(type, rng) returns one question; rng is a
   function giving a number from 0 up to 1 (Math.random by default; makeRng(seed) for a repeatable one). The student is never
   asked to work anything out: every step is a calculation SHOWN in terms of the question's numbers or a named earlier result,
   and the template computes its value (kept for the verifier, never shown).

   Four types, each 4 marks = 3 method marks + 1 answer mark (the answer mark is never asked for):
     enough    "Is it enough?"       items, a percentage off, a budget
     ratio     ratio with a twist    shared in a ratio, the difference between two shares given
     interest  compound / simple     compound growth, depreciation, or (1 in 4) simple interest
     garden    L-shaped garden       a drawn L, four sides labelled, turf at a price per m2

   A question is
     { type, calc, marks: 4, stem: [paragraph with TeX between § marks], diagram: null | {...}, params, numbers,
       slots: [{ id, label }],                 the 3 method marks; a slot is earned by the first of its steps found
       steps: [{ id, name, slot|null, value, forms: [{ expr, tex, deps, implies }] }],
       distractors: [{ expr, tex, value, deps, for, why }] }
   expr is space-separated tokens: numbers, + - * / ^ ( ), a postfix % after a number, and @stepId (a named earlier result).
   A form's deps are the steps that must already be found before it is offered (they include every @ref); implies lists the
   steps whose work the form shows inline, found at the same time ("60 / ( 5 - 3 )" shows 5 - 3). A literal number in an expr is
   a number of the question (numbers) or the value of one of the form's ancestors. A distractor is offered once its deps are
   found and the step it is `for` is on offer; its value never equals a step's value (the template drops any that would), and
   `why` names the slip in one line. A step with slot null is a step on the way: accepted, no mark of its own. */
(function (root) {
  'use strict';

  var TYPES = ['enough', 'ratio', 'interest', 'garden'];

  /* ---------- helpers ---------- */
  function rint(rng, a, b) { return a + Math.floor(rng() * (b - a + 1)); }
  function pick(rng, arr) { return arr[Math.floor(rng() * arr.length)]; }
  function shuffled(rng, arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(rng() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function gcd(a, b) { return b ? gcd(b, a % b) : Math.abs(a); }
  function makeRng(seed) {                                  // mulberry32
    var s = seed >>> 0;
    return function () {
      s = (s + 0x6D2B79F5) >>> 0;
      var t = s;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function pounds(pence) { return '£' + (pence % 100 === 0 ? String(pence / 100) : (pence / 100).toFixed(2)); }
  function thousands(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function dec(n) { return String(Math.round(n * 1e6) / 1e6); }        // 1.03, 0.9, 0.25: a decimal as written

  /* ---------- expressions ---------- */
  // expr := term (+|- term)*; term := pow (*|/ pow)*; pow := atom (^ pow)?; atom := number [%] | @id | ( expr )
  function evalExpr(expr, vals) {
    var t = expr.split(' '), i = 0;
    function atom() {
      var k = t[i++];
      if (k === '(') { var v = sum(); i++; return v; }
      if (k.charAt(0) === '@') {
        if (!(k.slice(1) in vals)) throw new Error('unknown result ' + k);
        return vals[k.slice(1)];
      }
      var x = parseFloat(k);
      if (isNaN(x)) throw new Error('bad token ' + k);
      if (t[i] === '%') { i++; x = x / 100; }
      return x;
    }
    function pow() { var b = atom(); if (t[i] === '^') { i++; return Math.pow(b, pow()); } return b; }
    function prod() {
      var v = pow();
      while (t[i] === '*' || t[i] === '/') { var op = t[i++], r = pow(); v = op === '*' ? v * r : v / r; }
      return v;
    }
    function sum() {
      var v = prod();
      while (t[i] === '+' || t[i] === '-') { var op = t[i++], r = prod(); v = op === '+' ? v + r : v - r; }
      return v;
    }
    var out = sum();
    if (i !== t.length) throw new Error('trailing tokens in ' + expr);
    return Math.round(out * 1e9) / 1e9;
  }
  function refsOf(expr) {
    return expr.split(' ').filter(function (k) { return k.charAt(0) === '@'; }).map(function (k) { return k.slice(1); });
  }
  // The calculation as KaTeX. A named result is its name in words; thousands get a thin comma.
  function texOf(expr, names) {
    var t = expr.split(' '), out = '';
    for (var i = 0; i < t.length; i++) {
      var k = t[i];
      if (k === '*') out += ' \\times ';
      else if (k === '/') out += ' \\div ';
      else if (k === '^') { out += '^{' + t[++i] + '}'; }
      else if (k === '%') out += '\\%';
      else if (k.charAt(0) === '@') out += '\\text{' + names[k.slice(1)] + '}';
      else if (/^\d{4,}$/.test(k)) out += k.replace(/\B(?=(\d{3})+(?!\d))/g, '{,}');
      else out += k;
    }
    return out.replace(/^\s+|\s+$/g, '').replace(/\s{2,}/g, ' ');
  }

  /* ---------- assembling a question ---------- */
  // spec: { type, calc, stem, diagram, params, numbers, slots, steps (in dependency order), distractors }
  function build(spec) {
    var names = {}, vals = {}, known = {};
    spec.steps.forEach(function (s) { names[s.id] = s.name; });
    var steps = spec.steps.map(function (s) {
      var forms = s.forms.map(function (f) {
        var deps = (f.deps || []).slice();
        refsOf(f.expr).forEach(function (r) { if (deps.indexOf(r) < 0) deps.push(r); });
        deps.forEach(function (d) { if (!known[d]) throw new Error(s.id + ' needs ' + d + ' before it exists'); });
        return { expr: f.expr, tex: texOf(f.expr, names), deps: deps, implies: (f.implies || []).slice() };
      });
      var v = evalExpr(forms[0].expr, vals);
      vals[s.id] = v; known[s.id] = true;
      return { id: s.id, name: s.name, slot: s.slot || null, value: v, forms: forms };
    });
    // A distractor never equals a step's value (a true statement is never a wrong option: SR-16): the candidates are filtered.
    var stepVals = steps.map(function (s) { return s.value; });
    var seen = {};
    var distractors = [];
    spec.distractors.forEach(function (d) {
      var deps = (d.deps || []).slice();
      refsOf(d.expr).forEach(function (r) { if (deps.indexOf(r) < 0) deps.push(r); });
      var v = evalExpr(d.expr, vals);
      var clash = stepVals.some(function (x) { return Math.abs(x - v) < 1e-7 * Math.max(1, Math.abs(x)); });
      var dupKey = texOf(d.expr, names);
      if (clash || seen[dupKey]) return;
      seen[dupKey] = true;
      distractors.push({ expr: d.expr, tex: dupKey, value: v, deps: deps, 'for': d['for'], why: d.why });
    });
    return {
      type: spec.type, calc: !!spec.calc, marks: 4, stem: spec.stem, diagram: spec.diagram || null,
      params: spec.params, numbers: spec.numbers, slots: spec.slots, steps: steps, distractors: distractors
    };
  }

  /* ---------- type 1: is it enough? ---------- */
  var ITEMS = ['T-shirts', 'pairs of socks', 'caps', 'mugs', 'notebooks', 'scarves', 'towels', 'candles', 'cushions', 'plant pots'];
  var PEOPLE = ['Sam', 'Priya', 'Jo', 'Alex', 'Maya', 'Tom', 'Chloe', 'Imran', 'Beth', 'Ravi'];

  function qEnough(rng) {
    var n = pick(rng, [2, 3]), items = shuffled(rng, ITEMS).slice(0, n), who = pick(rng, PEOPLE), rows = [], total = 0, i;
    for (i = 0; i < n; i++) {
      var q = rint(rng, 2, 5), p = 5 * rint(rng, 20, 400);         // 5p steps, £1 to £20
      rows.push({ item: items[i], q: q, p: p }); total += q * p;
    }
    // 10% and 25% off need the total to come out in whole pence; 20% always does (the total is a multiple of 5p).
    var ds = [20]; if (total % 10 === 0) ds.push(10); if (total % 4 === 0) ds.push(25);
    var d = pick(rng, ds), disc = total * d / 100, paid = total - disc;
    // The budget: within 15% of the discounted total, either side, in whole pounds where one fits, then 50p, then 5p.
    var budget = null, unit = 100, gap = [100, 50, 20];
    for (var u = 0; u < 3 && budget === null; u++) {
      unit = [100, 50, 5][u];
      var lo = Math.ceil(paid * 0.85 / unit), hi = Math.floor(paid * 1.15 / unit), c = [];
      for (var b = lo; b <= hi; b++) if (Math.abs(b * unit - paid) >= gap[u]) c.push(b * unit);
      if (c.length) budget = pick(rng, c);
    }
    var dd = dec(d / 100), mm = dec((100 - d) / 100);
    var buy = rows.map(function (r) { return r.q + ' ' + r.item + ' at ' + pounds(r.p) + ' each'; });
    var list = buy.length === 2 ? buy[0] + ' and ' + buy[1] : buy[0] + ', ' + buy[1] + ' and ' + buy[2];
    var steps = [], dist = [], money = function (p) { return (p / 100).toFixed(2); };
    rows.forEach(function (r, k) {
      steps.push({ id: 'c' + (k + 1), name: 'the ' + r.item + ' cost', slot: 'cost', forms: [{ expr: r.q + ' * ' + money(r.p) }] });
    });
    var ids = rows.map(function (r, k) { return '@c' + (k + 1); });
    steps.push({ id: 'total', name: 'the total', slot: 'total', forms: [{ expr: ids.join(' + ') }] });
    steps.push({ id: 'discount', name: 'the discount', slot: 'off', forms: [{ expr: '@total * ' + dd }] });
    steps.push({ id: 'price', name: 'the price after the discount', slot: 'off',
      forms: [{ expr: '@total * ' + mm }, { expr: '@total - @discount' }] });
    rows.forEach(function (r, k) {
      var other = rows[(k + 1) % n], id = 'c' + (k + 1);
      dist.push({ expr: r.q + ' + ' + money(r.p), 'for': id,
        why: 'That adds the number of items to the price. Several items cost the price that many times: multiply.' });
      dist.push({ expr: money(r.p) + ' / ' + r.q, 'for': id,
        why: 'That divides the price by the number of items. More items cost more, not less: multiply.' });
      dist.push({ expr: money(r.p) + ' * ' + other.q, 'for': id,
        why: 'Right price, wrong quantity: that uses the number of ' + other.item + ', not the ' + r.item + '.' });
    });
    dist.push({ expr: ids.slice(0, 2).join(' * '), 'for': 'total', deps: ['c1', 'c2'],
      why: 'That multiplies the costs together. To find what the shopping comes to, add them.' });
    dist.push({ expr: '@total - ' + d, 'for': 'discount',
      why: 'That takes ' + d + ' pounds off, but the offer is ' + d + ' per cent of the total.' });
    dist.push({ expr: '@total * ' + d, 'for': 'discount',
      why: d + '% is not × ' + d + '. Per cent means out of 100, so ' + d + '% is ' + d + ' ÷ 100.' });
    dist.push({ expr: '@total / ' + d, 'for': 'discount',
      why: 'Dividing by ' + d + ' is not finding ' + d + '%. Write ' + d + '% as ' + d + ' ÷ 100 and multiply.' });
    dist.push({ expr: '@total + @discount', 'for': 'price', deps: ['total', 'discount'],
      why: 'A discount comes off the total. Adding it makes the price go up.' });
    var nums = [budget / 100, d, d / 100, (100 - d) / 100];
    rows.forEach(function (r) { nums.push(r.q, r.p / 100); });
    return build({
      type: 'enough', calc: false,
      stem: [who + ' has ' + pounds(budget) + '. ' + who + ' wants to buy ' + list + '.',
             'The shop takes ' + d + '% off the total. Does ' + who + ' have enough money?'],
      params: { who: who, rows: rows, d: d, budget: budget },
      numbers: nums,
      slots: [{ id: 'cost', label: 'an item cost' }, { id: 'total', label: 'the total' }, { id: 'off', label: d + '% off' }],
      steps: steps, distractors: dist
    });
  }

  /* ---------- type 2: ratio with a twist ---------- */
  var DUOS = [['Amir', 'Beth'], ['Cara', 'Dev'], ['Ella', 'Femi'], ['Gus', 'Hana'], ['Ivan', 'Jess'], ['Kofi', 'Lily']];
  var STUFF = {
    money: { share: 'share some money', more: function (D, big) { return big + ' gets £' + D + ' more than'; }, ask: 'How much money do they share?' },
    sweets: { share: 'share some sweets', more: function (D, big) { return big + ' gets ' + D + ' more sweets than'; }, ask: 'How many sweets do they share?' },
    stickers: { share: 'share some stickers', more: function (D, big) { return big + ' gets ' + D + ' more stickers than'; }, ask: 'How many stickers do they share?' },
    points: { share: 'share the points in a game', more: function (D, big) { return big + ' gets ' + D + ' more points than'; }, ask: 'How many points do they share?' }
  };
  var RATIOS = (function () {
    var out = [];
    for (var a = 1; a <= 5; a++) for (var b = a + 1; a + b <= 12; b++) if (gcd(a, b) === 1) out.push([a, b]);
    return out;
  })();

  function qRatio(rng) {
    var ab = pick(rng, RATIOS), a = ab[0], b = ab[1], part = rint(rng, 2, 20), D = part * (b - a);
    var duo = pick(rng, DUOS), kind = pick(rng, ['money', 'sweets', 'stickers', 'points']), S = STUFF[kind];
    var steps = [
      { id: 'diff', name: 'the difference in parts', slot: 'diff', forms: [{ expr: b + ' - ' + a }] },
      { id: 'part', name: 'one part', slot: 'part', forms: [
        { expr: D + ' / ( ' + b + ' - ' + a + ' )', implies: ['diff'] }, { expr: D + ' / @diff' }] },
      { id: 'total', name: 'the total', slot: 'total', forms: [{ expr: '@part * ( ' + a + ' + ' + b + ' )' }] }
    ];
    var dist = [
      { expr: b + ' + ' + a, 'for': 'diff',
        why: 'That adds the parts. How many more parts one person has is the difference: subtract.' },
      { expr: D + ' / ( ' + a + ' + ' + b + ' )', 'for': 'part',
        why: 'That shares the extra ' + D + ' over every part. The ' + D + ' is only the extra parts, the difference.' },
      { expr: D + ' / ' + a, 'for': 'part',
        why: 'That divides by ' + duo[0] + "'s parts only. The " + D + ' is the gap between the two shares.' },
      { expr: D + ' / ' + b, 'for': 'part',
        why: 'That divides by ' + duo[1] + "'s parts only. The " + D + ' is the gap between the two shares.' },
      { expr: '@part * ' + b, 'for': 'total',
        why: "That is " + duo[1] + "'s share. The question asks for everything shared, so use all the parts." },
      { expr: D + ' * ( ' + a + ' + ' + b + ' )', 'for': 'total', deps: ['part'],
        why: 'That multiplies the ' + D + ' by the parts. Find the size of one part first, then multiply that.' }
    ];
    return build({
      type: 'ratio', calc: false,
      stem: [duo[0] + ' and ' + duo[1] + ' ' + S.share + ' in the ratio §' + a + ' : ' + b + '§.',
             S.more(D, duo[1]) + ' ' + duo[0] + '. ' + S.ask],
      params: { a: a, b: b, part: part, D: D, kind: kind, duo: duo },
      numbers: [a, b, D],
      slots: [{ id: 'diff', label: 'the difference in parts' }, { id: 'part', label: 'one part' }, { id: 'total', label: 'the total' }],
      steps: steps, distractors: dist
    });
  }

  /* ---------- type 3: compound interest, depreciation, simple interest ---------- */
  var THINGS = ['a car', 'a laptop', 'a van', 'a motorbike', 'a tractor'];

  function qInterest(rng) {
    var simple = rng() < 0.25, dep = !simple && rng() < 0.35, P = 100 * rint(rng, 5, 200), n = rint(rng, 2, 5);
    var r = dep ? rint(rng, 5, 25) : rint(rng, 1, 6);
    var rr = dec(r / 100), m = dec(dep ? (100 - r) / 100 : (100 + r) / 100), pc = String(dep ? 100 - r : 100 + r);
    var steps, dist, stem, slots, nums, kind = simple ? 'simple' : (dep ? 'depreciation' : 'compound');
    if (simple) {
      stem = ['£' + thousands(P) + ' is invested at ' + r + '% simple interest per year for ' + n + ' years.',
              'Work out the total interest.'];
      steps = [
        { id: 'rate', name: 'the rate', slot: 'rate', forms: [{ expr: rr }, { expr: r + ' %' }] },
        { id: 'year', name: "one year's interest", slot: 'year', forms: [
          { expr: P + ' * ' + rr, deps: ['rate'] }, { expr: P + ' * ' + r + ' %', implies: ['rate'] }] },
        { id: 'total', name: 'the total interest', slot: 'total', forms: [
          { expr: '@year * ' + n }, { expr: P + ' * ' + rr + ' * ' + n, deps: ['rate'] }] }
      ];
      dist = [
        { expr: dec(r / 10), 'for': 'rate', why: dec(r / 10) + ' treats ' + r + '% as ' + dec(r / 10) + '. Per cent is out of 100: ' + r + '% is ' + rr + '.' },
        { expr: m, 'for': 'rate', why: m + ' is the compound multiplier. This question is simple interest: the rate is just ' + rr + '.' },
        { expr: P + ' * ' + r, 'for': 'year', why: 'That multiplies by ' + r + ', not by ' + r + '%. Per cent means out of 100.' },
        { expr: P + ' * ' + m, 'for': 'year', deps: [], why: 'That adds the interest on to the ' + P + ". One year's interest is only the " + r + '% part.' },
        { expr: P + ' * ' + m + ' ^ ' + n, 'for': 'total',
          why: 'That is compound interest. This question says simple, so the same interest is added every year.' },
        { expr: P + ' * ' + m + ' * ' + n, 'for': 'total', why: 'That multiplies the whole amount by the years. Simple interest is one year\'s interest, times the years.' },
        { expr: P + ' * ' + r + ' * ' + n, 'for': 'total', why: 'That multiplies by ' + r + ', not ' + r + '%. Write the rate as a decimal first.' }
      ];
      slots = [{ id: 'rate', label: 'the rate as a decimal' }, { id: 'year', label: "one year's interest" }, { id: 'total', label: 'the total interest' }];
      nums = [P, r, n, r / 100];
    } else {
      var ground = dep ? [pick(rng, THINGS)] : null;
      stem = dep
        ? [ground[0].charAt(0).toUpperCase() + ground[0].slice(1) + ' is worth £' + thousands(P) + ' new. Its value falls by ' + r + '% each year.',
           'Work out its value after ' + n + ' years.']
        : ['£' + thousands(P) + ' is invested at ' + r + '% compound interest per year for ' + n + ' years.',
           'Work out the value of the investment at the end.'];
      var rep = [];
      for (var k = 0; k < n; k++) rep.push(m);
      steps = [
        { id: 'mult', name: 'the multiplier', slot: 'mult', forms: [{ expr: m }, { expr: pc + ' %' }] },
        { id: 'year1', name: 'the value after 1 year', slot: 'year', forms: [{ expr: P + ' * ' + m, deps: ['mult'] }] },
        { id: 'change1', name: dep ? "the first year's fall" : "the first year's interest", slot: 'year',
          forms: [{ expr: P + ' * ' + rr }] },
        { id: 'final', name: dep ? 'the value after ' + n + ' years' : 'the value after ' + n + ' years', slot: 'final', forms: [
          { expr: P + ' * ' + m + ' ^ ' + n, deps: ['mult'] }, { expr: P + ' * ' + rep.join(' * '), deps: ['mult'] }] }
      ];
      if (dep) {
        dist = [
          { expr: dec(1 + r / 100), 'for': 'mult', why: dec(1 + r / 100) + ' is for a rise. The value falls by ' + r + '%, so ' + (100 - r) + '% is left: ' + m + '.' },
          { expr: rr, 'for': 'mult', why: rr + ' is the amount lost, not what is left. ' + (100 - r) + '% is left, so the multiplier is ' + m + '.' },
          { expr: P + ' * ' + r, 'for': 'mult', deps: [], why: 'That multiplies by ' + r + ', not by ' + r + '%. Per cent means out of 100.' },
          { expr: P + ' / ' + r, 'for': 'year', why: 'Dividing by ' + r + ' is not finding ' + r + '%. Write ' + r + '% as ' + rr + ' and multiply.' },
          { expr: P + ' * ' + rr + ' * ' + n, 'for': 'final', why: 'That takes the same amount off every year. A percentage fall is taken off the smaller value each time: use the multiplier as a power.' },
          { expr: P + ' * ' + m + ' * ' + n, 'for': 'final', deps: ['mult'], why: 'That multiplies by the years. Multiplying by ' + m + ' once a year is a power, ' + m + ' to the ' + n + '.' },
          { expr: P + ' * ' + dec(1 + r / 100) + ' ^ ' + n, 'for': 'final', why: 'That makes the value grow. It is falling, so the multiplier is below 1.' }
        ];
      } else {
        dist = [
          { expr: dec(1 + r / 10), 'for': 'mult', why: dec(1 + r / 10) + ' treats ' + r + '% as ' + dec(r / 10) + '. ' + r + '% is ' + rr + ', so the multiplier is ' + m + '.' },
          { expr: rr, 'for': 'mult', why: rr + ' is just the interest. Adding it to 1 keeps the original amount: the multiplier is ' + m + '.' },
          { expr: P + ' * ' + r, 'for': 'mult', deps: [], why: 'That multiplies by ' + r + ', not by ' + r + '%. Per cent means out of 100.' },
          { expr: P + ' * ' + r, 'for': 'year', why: 'That multiplies by ' + r + ', not by ' + r + '%. Per cent means out of 100.' },
          { expr: P + ' * ' + rr + ' * ' + n, 'for': 'final', why: "That is simple interest: the same amount every year. Compound interest is worked out on the growing total, so use the multiplier as a power." },
          { expr: P + ' * ' + m + ' * ' + n, 'for': 'final', deps: ['mult'], why: 'That multiplies by the years. Multiplying by ' + m + ' once a year is a power, ' + m + ' to the ' + n + '.' },
          { expr: P + ' * ' + dec(1 + r / 10) + ' ^ ' + n, 'for': 'final', why: dec(1 + r / 10) + ' treats ' + r + '% as ' + dec(r / 10) + '. ' + r + '% is ' + rr + '.' }
        ];
      }
      slots = [{ id: 'mult', label: 'the multiplier' }, { id: 'year', label: dep ? 'the first year' : 'the first year' }, { id: 'final', label: 'the value at the end' }];
      nums = [P, r, n, r / 100, (100 + (dep ? -r : r)) / 100, 100 + (dep ? -r : r)];
    }
    return build({
      type: 'interest', calc: true, stem: [stem[0], stem[1]],
      params: { kind: kind, P: P, r: r, n: n }, numbers: nums, slots: slots, steps: steps, distractors: dist
    });
  }

  /* ---------- type 4: the L-shaped garden ---------- */
  function qGarden(rng) {
    var W = rint(rng, 6, 15), H = rint(rng, 6, 15);
    var cw = rint(rng, 2, W - 3), chs = [], c;
    for (c = 2; c <= H - 3; c++) if (c !== cw) chs.push(c);
    var ch = pick(rng, chs), top = W - cw, lr = H - ch, price = 200 + 50 * rint(rng, 0, 20);   // £2 to £12 in 50p
    var ps = (price / 100).toFixed(2);
    var steps = [
      { id: 'gapW', name: 'the missing width', slot: 'len', forms: [{ expr: W + ' - ' + top }] },
      { id: 'gapH', name: 'the missing height', slot: 'len', forms: [{ expr: H + ' - ' + lr }] },
      { id: 'partA', name: 'the tall rectangle', slot: null, forms: [{ expr: top + ' * ' + H }] },
      { id: 'partB', name: 'the lower rectangle', slot: null, forms: [{ expr: cw + ' * ' + lr, deps: ['gapW'] }] },
      { id: 'partC', name: 'the wide rectangle', slot: null, forms: [{ expr: W + ' * ' + lr }] },
      { id: 'partD', name: 'the upper rectangle', slot: null, forms: [{ expr: top + ' * ' + ch, deps: ['gapH'] }] },
      { id: 'big', name: 'the full rectangle', slot: null, forms: [{ expr: W + ' * ' + H }] },
      { id: 'cut', name: 'the corner cut out', slot: null, forms: [{ expr: cw + ' * ' + ch, deps: ['gapW', 'gapH'] }] },
      { id: 'area', name: 'the whole area', slot: 'area', forms: [
        { expr: '@partA + @partB' },
        { expr: '( ' + top + ' * ' + H + ' ) + ( ' + cw + ' * ' + lr + ' )', deps: ['gapW'], implies: ['partA', 'partB'] },
        { expr: '@partC + @partD' },
        { expr: '( ' + W + ' * ' + lr + ' ) + ( ' + top + ' * ' + ch + ' )', deps: ['gapH'], implies: ['partC', 'partD'] },
        { expr: '@big - @cut' },
        { expr: '( ' + W + ' * ' + H + ' ) - ( ' + cw + ' * ' + ch + ' )', deps: ['gapW', 'gapH'], implies: ['big', 'cut'] }] },
      { id: 'cost', name: 'the cost', slot: 'cost', forms: [{ expr: '@area * ' + ps }] }
    ];
    var sides = W + ' + ' + H + ' + ' + top + ' + ' + lr;
    var dist = [
      { expr: W + ' + ' + top, 'for': 'gapW', why: 'That adds two sides. A missing length is the longer side take away the shorter one, so subtract.' },
      { expr: H + ' + ' + lr, 'for': 'gapH', why: 'That adds two sides. A missing length is the longer side take away the shorter one, so subtract.' },
      { expr: top + ' * ' + lr, 'for': 'partA', why: 'Those two sides belong to different parts of the garden, so they do not make a rectangle.' },
      { expr: sides, 'for': 'partA', why: 'That adds the sides. Adding gives the distance round the edge. Turf covers the inside: area, not perimeter.' },
      { expr: '@area / ' + ps, 'for': 'cost', why: 'That divides by the price. Each square metre costs the price, so more turf costs more: multiply.' },
      { expr: '( ' + sides + ' ) * ' + ps, 'for': 'cost', why: 'That adds the sides first, which is the edge, not the area. The turf covers the area.' },
      { expr: '@area + ' + ps, 'for': 'cost', why: 'That adds the price to the area. The price is for each square metre, so multiply.' }
    ];
    return build({
      type: 'garden', calc: false,
      stem: ['The diagram shows the plan of a garden, in metres. It is going to be covered in turf at ' + pounds(price) + ' per square metre.',
             'Work out the cost of the turf.'],
      diagram: { kind: 'lshape', W: W, H: H, cw: cw, ch: ch,
                 labels: { bottom: W, left: H, top: top, lowerRight: lr } },
      params: { W: W, H: H, cw: cw, ch: ch, price: price },
      numbers: [W, H, top, lr, price / 100],
      slots: [{ id: 'len', label: 'a missing length' }, { id: 'area', label: 'the whole area' }, { id: 'cost', label: 'the cost' }],
      steps: steps, distractors: dist
    });
  }

  function question(type, rng) {
    rng = rng || Math.random;
    var q = ({ enough: qEnough, ratio: qRatio, interest: qInterest, garden: qGarden })[type](rng);
    q.key = JSON.stringify(q.params);
    return q;
  }

  /* ---------- play: the state of one question ---------- */
  // found: { stepId: 'tap' | 'help' | 'implied' }; slots: { slotId: 'tap' | 'help' }; struck: { optionId: true }
  function newState() { return { found: {}, slots: {}, struck: {}, wrong: 0 }; }
  function stepOf(Q, id) { for (var i = 0; i < Q.steps.length; i++) if (Q.steps[i].id === id) return Q.steps[i]; return null; }
  function depsMet(S, deps) { return deps.every(function (d) { return !!S.found[d]; }); }
  function finished(Q, S) { return Q.slots.every(function (s) { return !!S.slots[s.id]; }); }

  // The calculations on offer: every form of an unfound step whose deps are found (at most two forms a step), then
  // distractors for the steps on offer. Option ids are 's:<step>:<form>' and 'd:<n>'.
  function options(Q, S, rng) {
    rng = rng || Math.random;
    var valid = [], onOffer = {}, extra = [];
    Q.steps.forEach(function (st) {
      if (S.found[st.id]) return;
      var shown = 0;
      st.forms.forEach(function (f, fi) {
        if (!depsMet(S, f.deps)) return;
        onOffer[st.id] = true;
        var o = { id: 's:' + st.id + ':' + fi, tex: f.tex, step: st.id };
        if (shown === 0) valid.push(o); else if (shown === 1) extra.push(o);
        shown++;
      });
    });
    valid = shuffled(rng, valid);
    // Six on offer at most (three rows of two on a phone: canon 7.6.1); a valid step left out shows once another is found.
    var cap = 6;
    var v = valid.slice(0, 4);
    shuffled(rng, extra).forEach(function (o) { if (v.length < 4) v.push(o); });
    var cands = [];
    Q.distractors.forEach(function (d, di) {
      var id = 'd:' + di;
      if (S.struck[id] || !onOffer[d['for']] || !depsMet(S, d.deps)) return;
      cands.push({ id: id, tex: d.tex, step: null });
    });
    var nd = Math.min(cands.length, Math.max(2, cap - v.length));
    return shuffled(rng, v.concat(shuffled(rng, cands).slice(0, nd)));
  }

  function award(Q, S, stepId, how) {
    var st = stepOf(Q, stepId), gained = null;
    S.found[stepId] = how;
    if (st.slot && !S.slots[st.slot]) { S.slots[st.slot] = how === 'help' ? 'help' : 'tap'; gained = st.slot; }
    return gained;
  }
  // The student taps an option. Returns { kind: 'mark' | 'step' | 'wrong' | 'ignored', why, slots: [newly earned], steps: [found] }.
  function choose(Q, S, optId) {
    var m = /^s:([^:]+):(\d+)$/.exec(optId);
    if (m) {
      var st = stepOf(Q, m[1]);
      if (!st || S.found[st.id]) return { kind: 'ignored', slots: [], steps: [] };
      var f = st.forms[+m[2]];
      if (!f || !depsMet(S, f.deps)) return { kind: 'ignored', slots: [], steps: [] };
      var slots = [], steps = [st.id], g;
      (f.implies || []).forEach(function (id) {
        if (!S.found[id]) { g = award(Q, S, id, 'implied'); steps.push(id); if (g) slots.push(g); }
      });
      g = award(Q, S, st.id, 'tap'); if (g) slots.push(g);
      return { kind: slots.length ? 'mark' : 'step', slots: slots, steps: steps };
    }
    m = /^d:(\d+)$/.exec(optId);
    if (m && Q.distractors[+m[1]] && !S.struck[optId]) {
      S.struck[optId] = true; S.wrong++;
      return { kind: 'wrong', why: Q.distractors[+m[1]].why, slots: [], steps: [] };
    }
    return { kind: 'ignored', slots: [], steps: [] };
  }
  // "Show me a step": reveals one, never scores. Prefers a step that would earn a mark.
  function hint(Q, S) {
    var best = null, any = null;
    Q.steps.forEach(function (st) {
      if (S.found[st.id]) return;
      var fi = -1;
      st.forms.forEach(function (f, i) { if (fi < 0 && depsMet(S, f.deps)) fi = i; });
      if (fi < 0) return;
      if (!any) any = { st: st, fi: fi };
      if (!best && st.slot && !S.slots[st.slot]) best = { st: st, fi: fi };
    });
    var h = best || any;
    if (!h) return null;
    var f = h.st.forms[h.fi], steps = [h.st.id];
    (f.implies || []).forEach(function (id) { if (!S.found[id]) { award(Q, S, id, 'help'); steps.push(id); } });
    var gained = award(Q, S, h.st.id, 'help');
    return { step: h.st.id, tex: f.tex, slot: gained, steps: steps };
  }
  function unaided(Q, S) { return Q.slots.filter(function (s) { return S.slots[s.id] === 'tap'; }).length; }

  root.MaffsFoundAMark = {
    TYPES: TYPES, question: question, makeRng: makeRng, evalExpr: evalExpr, texOf: texOf,
    newState: newState, options: options, choose: choose, hint: hint, finished: finished, unaided: unaided
  };
})(typeof window !== 'undefined' ? window : this);
