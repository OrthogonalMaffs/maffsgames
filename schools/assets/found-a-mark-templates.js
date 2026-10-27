/* The "I Found a Mark" question templates (contract FOUND-A-MARK, Jon, 27 Oct 2026): multi-mark exam questions broken into
   the steps a marker gives method marks for.

   The bank-first source of the topic (canon 8.2.1): the game games/i-found-a-mark/ loads this file and the 6 P's could load it
   too; the questions are never copied. Pure data, no DOM. MaffsFoundAMark.question(type, rng) returns one question; rng is a
   function giving a number from 0 up to 1 (Math.random by default; makeRng(seed) for a repeatable one). The student is never
   asked to work anything out: every step is a calculation SHOWN in terms of the question's numbers or a named earlier result,
   and the template computes its value (kept for the verifier, never shown).

   Nine types. Each has method marks (its slots) and answer marks (never asked for; marks = slots + answers):
     enough    "Is it enough?"       items, a percentage off, a budget                                   3 + 1
     ratio     ratio with a twist    shared in a ratio, the difference between two shares given           3 + 1
     interest  compound / simple     compound growth, depreciation, or (1 in 4) simple interest           3 + 1
     garden    L-shaped garden       a drawn L, four sides labelled, turf at a price per m2               3 + 1
   Batch 2 (contract FOUND-A-MARK-2, Jon, 27 Oct 2026):
     angles    parallel lines        two given angles, the third by a straight line or the triangle       3 + 1
     mean      frequency table       x times f for each row, their total, the total divided by the sum of f 3 + 1
     ladder    Pythagoras            the squares, then the square root (height, or length of the ladder)   2 + 1
     coffee    simultaneous          two equations, a matched equation, the equation with one letter       4 + 2
     twoway    conditional prob.     a two-way table that fills in, then a probability                    4 + 1

   A question is
     { type, calc, marks, answers, stem: [paragraph with TeX between § marks], diagram: null | {...}, params, numbers,
       slots: [{ id, label }],                 the 3 method marks; a slot is earned by the first of its steps found
       steps: [{ id, name, slot|null, value, forms: [{ expr, tex, deps, implies }] }],
       distractors: [{ expr, tex, value, deps, for, why }] }
   expr is space-separated tokens: numbers, + - * / ^ ( ), a postfix % after a number, and @stepId (a named earlier result).
   A form's deps are the steps that must already be found before it is offered (they include every @ref); implies lists the
   steps whose work the form shows inline, found at the same time ("60 / ( 5 - 3 )" shows 5 - 3). A literal number in an expr is
   a number of the question (numbers) or the value of one of the form's ancestors. A distractor is offered once its deps are
   found and the step it is `for` is on offer; its value never equals a step's value (the template drops any that would), and
   `why` names the slip in one line. A step with slot null is a step on the way: accepted, no mark of its own.

   Batch 2 extends this engine once, for every type (nothing per type): (1) a question has `answers` answer marks (default 1) and
   marks = slots + answers; (2) a form or distractor may carry its own `tex` and no `expr`, for a statement that is not a number
   (an equation, "x times f for each row"); a step or distractor may carry a `fact`, a string naming WHAT is claimed and its value
   ("EFG=52"), and a distractor then clashes only with a step of the same fact (angle EGF = 31 is not angle EFG = 31); (3) `sqrt`
   in an expression: "sqrt @A" or "sqrt ( ... )". A step valid at once and also by a later route is two forms of one step with
   different deps; two routes whose second part differs (a different matched equation, so a different eliminated one) are two
   steps in one slot. */
(function (root) {
  'use strict';

  var TYPES = ['enough', 'ratio', 'interest', 'garden', 'angles', 'mean', 'ladder', 'coffee', 'twoway'];
  // Method marks (slots) a type carries: a session of five is dealt so that these always add to 15.
  var METHOD = { enough: 3, ratio: 3, interest: 3, garden: 3, angles: 3, mean: 3, ladder: 2, coffee: 4, twoway: 4 };

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
      if (k === 'sqrt') return Math.sqrt(atom());
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
  function texOf(expr, names) { return texTokens(expr.split(' '), names).replace(/^\s+|\s+$/g, '').replace(/\s{2,}/g, ' '); }
  function texTokens(t, names) {
    var out = '';
    for (var i = 0; i < t.length; i++) {
      var k = t[i];
      if (k === '*') out += ' \\times ';
      else if (k === '/') out += ' \\div ';
      else if (k === '^') { out += '^{' + t[++i] + '}'; }
      else if (k === '%') out += '\\%';
      else if (k === 'sqrt') {
        var j = i + 1, inner;
        if (t[j] === '(') {
          var depth = 0, e = j;
          for (; e < t.length; e++) { if (t[e] === '(') depth++; else if (t[e] === ')') { depth--; if (!depth) break; } }
          inner = t.slice(j + 1, e); i = e;
        } else { inner = [t[j]]; i = j; }
        out += '\\sqrt{' + texTokens(inner, names) + '}';
      }
      else if (k.charAt(0) === '@') out += '\\text{' + names[k.slice(1)] + '}';
      else if (/^\d{4,}$/.test(k)) out += k.replace(/\B(?=(\d{3})+(?!\d))/g, '{,}');
      else out += k;
    }
    return out;
  }

  /* ---------- assembling a question ---------- */
  // spec: { type, calc, stem, diagram, params, numbers, slots, steps (in dependency order), distractors }
  function build(spec) {
    var names = {}, vals = {}, known = {};
    spec.steps.forEach(function (s) { names[s.id] = s.name; });
    var steps = spec.steps.map(function (s) {
      var forms = s.forms.map(function (f) {
        var deps = (f.deps || []).slice();
        if (f.expr) refsOf(f.expr).forEach(function (r) { if (deps.indexOf(r) < 0) deps.push(r); });
        deps.forEach(function (d) { if (!known[d]) throw new Error(s.id + ' needs ' + d + ' before it exists'); });
        return { expr: f.expr || null, tex: f.tex || texOf(f.expr, names), deps: deps, implies: (f.implies || []).slice() };
      });
      var v = forms[0].expr ? evalExpr(forms[0].expr, vals) : null;
      vals[s.id] = v; known[s.id] = true;
      var st = { id: s.id, name: s.name, slot: s.slot || null, value: v, forms: forms };
      if (s.fact !== undefined) st.fact = s.fact;
      return st;
    });
    // A distractor never equals a step's value (a true statement is never a wrong option, SR-16): the candidates are filtered.
    // One that names what it claims (a fact, "EFG=31") clashes only with a step making the same claim.
    var stepVals = steps.map(function (s) { return s.value; }).filter(function (x) { return x !== null; });
    var seen = {};
    var distractors = [];
    spec.distractors.forEach(function (d) {
      var deps = (d.deps || []).slice();
      if (d.expr) refsOf(d.expr).forEach(function (r) { if (deps.indexOf(r) < 0) deps.push(r); });
      var v = d.expr ? evalExpr(d.expr, vals) : null;
      var clash = d.fact !== undefined
        ? steps.some(function (s) { return s.fact === d.fact; })
        : (v !== null && stepVals.some(function (x) { return Math.abs(x - v) < 1e-7 * Math.max(1, Math.abs(x)); }));
      var dupKey = d.tex || texOf(d.expr, names);
      if (clash || seen[dupKey]) return;
      seen[dupKey] = true;
      var o = { expr: d.expr || null, tex: dupKey, value: v, deps: deps, 'for': d['for'], why: d.why };
      if (d.fact !== undefined) o.fact = d.fact;
      distractors.push(o);
    });
    var answers = spec.answers || 1;
    return {
      type: spec.type, calc: !!spec.calc, marks: spec.slots.length + answers, answers: answers, fit: !!spec.fit, stem: spec.stem, diagram: spec.diagram || null,
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
          { expr: P + ' / ' + r, 'for': 'change1', why: 'Dividing by ' + r + ' is not finding ' + r + '%. Write ' + r + '% as ' + rr + ' and multiply.' },
          { expr: P + ' * ' + rr + ' * ' + n, 'for': 'final', why: 'That takes the same amount off every year. A percentage fall is taken off the smaller value each time: use the multiplier as a power.' },
          { expr: P + ' * ' + m + ' * ' + n, 'for': 'final', deps: ['mult'], why: 'That multiplies by the years. Multiplying by ' + m + ' once a year is a power, ' + m + ' to the ' + n + '.' },
          { expr: P + ' * ' + dec(1 + r / 100) + ' ^ ' + n, 'for': 'final', why: 'That makes the value grow. It is falling, so the multiplier is below 1.' }
        ];
      } else {
        dist = [
          { expr: dec(1 + r / 10), 'for': 'mult', why: dec(1 + r / 10) + ' treats ' + r + '% as ' + dec(r / 10) + '. ' + r + '% is ' + rr + ', so the multiplier is ' + m + '.' },
          { expr: rr, 'for': 'mult', why: rr + ' is just the interest. Adding it to 1 keeps the original amount: the multiplier is ' + m + '.' },
          { expr: P + ' * ' + r, 'for': 'mult', deps: [], why: 'That multiplies by ' + r + ', not by ' + r + '%. Per cent means out of 100.' },
          { expr: P + ' * ' + r, 'for': 'change1', why: 'That multiplies by ' + r + ', not by ' + r + '%. Per cent means out of 100.' },
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

  /* ====================================================================================================================
     BATCH 2 (contract FOUND-A-MARK-2, Jon, 27 Oct 2026): five more types, built on the same steps / slots / distractors.
     ==================================================================================================================== */
  function deg(n) { return n + '^\\circ'; }
  function plain(n) { return String(Math.round(n * 1e6) / 1e6); }

  /* ---------- type 5: angles in parallel lines (value only) ---------- */
  function qAngles(rng) {
    var a, b;
    do { a = rint(rng, 30, 80); b = rint(rng, 30, 80); } while (a === b || a + b < 100 || a + b > 150);   // a = b would make "= b" a true claim twice over
    var x = 180 - a - b;
    function eq(l, rhs) { return '\\angle ' + l + ' = ' + rhs; }
    var steps = [
      { id: 'A', name: 'angle EFG', slot: 'efg', fact: 'EFG=' + a, forms: [{ expr: String(a), tex: eq('EFG', deg(a)) }] },
      { id: 'B', name: 'angle EGF', slot: 'egf', fact: 'EGF=' + b, forms: [{ expr: String(b), tex: eq('EGF', deg(b)) }] },
      { id: 'C', name: 'angle FEG', slot: 'feg', fact: 'FEG=' + x, forms: [
        { expr: '180 - ' + a + ' - ' + b, tex: eq('FEG', '180^\\circ - ' + deg(a) + ' - ' + deg(b)) },          // the straight line AEB: valid at once
        { expr: '180 - @A - @B', tex: eq('FEG', '180^\\circ - \\angle EFG - \\angle EGF'), deps: ['A', 'B'] }] }    // or the triangle, once both are found
    ];
    var dist = [
      { expr: '180 - ' + a, tex: eq('EFG', '180^\\circ - ' + deg(a)), fact: 'EFG=' + (180 - a), 'for': 'A',
        why: 'That is the co-interior angle, 180° less ' + a + '°. Angle EFG and angle AEF are alternate angles, so equal: ' + a + '°.' },
      { expr: String(b), tex: eq('EFG', deg(b)), fact: 'EFG=' + b, 'for': 'A',
        why: b + '° is angle BEG, a different angle. Angle EFG is alternate to angle AEF, so it is ' + a + '°.' },
      { expr: '180 - ' + b, tex: eq('EGF', '180^\\circ - ' + deg(b)), fact: 'EGF=' + (180 - b), 'for': 'B',
        why: 'That is the co-interior angle, 180° less ' + b + '°. Angle EGF and angle BEG are alternate angles, so equal: ' + b + '°.' },
      { expr: String(a), tex: eq('EGF', deg(a)), fact: 'EGF=' + a, 'for': 'B',
        why: a + '° is angle AEF, a different angle. Angle EGF is alternate to angle BEG, so it is ' + b + '°.' },
      { expr: '360 - ' + a + ' - ' + b, tex: eq('FEG', '360^\\circ - ' + deg(a) + ' - ' + deg(b)), fact: 'FEG=' + (360 - a - b), 'for': 'C',
        why: 'Angles on a straight line, and angles in a triangle, add to 180°, not 360°.' },
      { expr: a + ' + ' + b, tex: eq('FEG', deg(a) + ' + ' + deg(b)), fact: 'FEG=' + (a + b), 'for': 'C',
        why: 'That adds the two angles you are given. Angle FEG is what is left of the straight line: take them away from 180°.' },
      { expr: '90 - ' + a, tex: eq('FEG', '90^\\circ - ' + deg(a)), fact: 'FEG=' + (90 - a), 'for': 'C',
        why: 'There is no right angle here. Angles on the straight line AEB add to 180°.' }
    ];
    return build({
      type: 'angles', calc: false, fit: true,
      stem: ['AB is parallel to CD.', 'Work out the size of angle FEG.'],
      diagram: { kind: 'angles', a: a, b: b, x: x },
      params: { a: a, b: b }, numbers: [a, b, 180],
      slots: [{ id: 'efg', label: 'angle EFG' }, { id: 'egf', label: 'angle EGF' }, { id: 'feg', label: 'angle FEG' }],
      steps: steps, distractors: dist
    });
  }

  /* ---------- type 6: the mean from a frequency table ---------- */
  var MEAN_CTX = [
    { key: 'goals', head: 'Goals', say: function (n) { return 'The table shows the goals a team scored in ' + n + ' matches.'; }, ask: 'Work out the mean number of goals in a match.' },
    { key: 'siblings', head: 'Siblings', say: function (n) { return 'The table shows the brothers and sisters of ' + n + ' students.'; }, ask: 'Work out the mean number of brothers and sisters.' },
    { key: 'pets', head: 'Pets', say: function (n) { return 'The table shows the pets owned by ' + n + ' students.'; }, ask: 'Work out the mean number of pets.' },
    { key: 'books', head: 'Books', say: function (n) { return 'The table shows the books ' + n + ' students read last month.'; }, ask: 'Work out the mean number of books.' },
    { key: 'phones', head: 'Phones', say: function (n) { return 'The table shows the phones in each of ' + n + ' homes.'; }, ask: 'Work out the mean number of phones in a home.' }
  ];

  function qMean(rng) {
    var ctx = pick(rng, MEAN_CTX), lo = pick(rng, [0, 1]), rows = pick(rng, [5, 6]), xs = [], fs, total, tries = 0, i;
    for (i = 0; i < rows; i++) xs.push(lo + i);
    do {
      fs = xs.map(function () { return rint(rng, 1, 12); });
      total = fs.reduce(function (s, f) { return s + f; }, 0);
      tries++;
    } while ((total < 15 || total > 40 || fs.every(function (f) { return f === fs[0]; })) && tries < 1000);
    var prods = xs.map(function (x, k) { return x * fs[k]; }), sum = prods.reduce(function (s, p) { return s + p; }, 0);
    var sx = xs.reduce(function (s, x) { return s + x; }, 0);
    var exact = (sum * 10) % total === 0;                         // a mean that is already 1 decimal place or fewer needs no rounding
    var join = function (arr) { return arr.join(' + '); };
    var steps = [
      { id: 'A', name: 'each x times f', slot: 'xf', fact: 'XF=' + prods.join(','), forms: [{ tex: 'x \\times f \\text{ for each row}' }] },
      { id: 'B', name: 'the total of x times f', slot: 'sum', forms: [{ expr: xs.map(function (x, k) { return x + ' * ' + fs[k]; }).join(' + '), deps: ['A'] }] },
      { id: 'C', name: 'the mean', slot: 'mean', forms: [{ expr: '@B / ' + total }] }
    ];
    var dist = [
      { tex: 'x + f \\text{ for each row}', fact: 'XF=' + xs.map(function (x, k) { return x + fs[k]; }).join(','), 'for': 'A',
        why: 'That adds x and f. A row says x happened f times, so multiply x by f.' },
      { tex: 'x \\div f \\text{ for each row}', fact: 'XF=' + xs.map(function (x, k) { return plain(x / fs[k]); }).join(','), 'for': 'A',
        why: 'That divides x by f. A row says x happened f times, so multiply.' },
      { expr: join(fs), 'for': 'B', deps: ['A'],
        why: 'That adds up the frequencies, which only counts how many values there are. We need the total of x times f.' },
      { expr: join(xs), 'for': 'B', deps: ['A'],
        why: 'That adds up the values of x and ignores how many times each one happens.' },
      { expr: '@B / ' + rows, 'for': 'C',
        why: 'That divides by the number of rows. Divide by how many values there are altogether: the total of the frequencies.' },
      { expr: total + ' / ' + rows, 'for': 'C', deps: ['B'],
        why: 'That divides the total frequency by the number of rows. The mean is the total of x times f, shared out.' },
      { expr: '@B / ' + sx, 'for': 'C',
        why: 'That divides by the total of the x values. Divide by the total of the frequencies.' }
    ];
    var nums = xs.concat(fs, [total]);
    return build({
      type: 'mean', calc: true, fit: true,
      stem: [ctx.say(total), ctx.ask + (exact ? '' : ' Give your answer to 1 decimal place.')],
      diagram: { kind: 'freq', head: [ctx.head, 'Frequency', 'x × f'], xs: xs, fs: fs, products: prods },
      params: { ctx: ctx.key, xs: xs, fs: fs, total: total, sum: sum, exact: exact },
      numbers: nums,
      slots: [{ id: 'xf', label: 'x times f for each row' }, { id: 'sum', label: 'the total of x times f' }, { id: 'mean', label: 'the mean' }],
      steps: steps, distractors: dist
    });
  }

  /* ---------- type 7: the ladder (Pythagoras) ---------- */
  var TRIPLES = [[3, 4, 5], [5, 12, 13], [7, 24, 25], [8, 15, 17]];
  // Scaled by j tenths: the foot 0.6 to 3 m and the ladder 3 to 12 m. (The contract's "foot under a third of the ladder" leaves
  // only 7-24-25, so it is not applied: the foot is the shorter leg, which is the realistic way round for every triple.)
  var LADDERS = (function () {
    var out = [];
    TRIPLES.forEach(function (t) {
      for (var j = 1; j <= 80; j++) if (t[0] * j >= 6 && t[0] * j <= 30 && t[2] * j >= 30 && t[2] * j <= 120) out.push({ t: t, j: j });
    });
    return out;
  })();

  function qLadder(rng) {
    var c = pick(rng, LADDERS), t = c.t, j = c.j, variant = pick(rng, ['height', 'length']);
    var d = dec(t[0] * j / 10), h = dec(t[1] * j / 10), L = dec(t[2] * j / 10), steps, dist, stem, nums;
    if (variant === 'height') {
      stem = ['A ladder is ' + L + ' m long. It leans against a vertical wall. The foot of the ladder is ' + d + ' m from the wall.',
              'Work out how high up the wall the ladder reaches.'];
      steps = [
        { id: 'A', name: 'the difference of the squares', slot: 'sq', forms: [{ expr: L + ' ^ 2 - ' + d + ' ^ 2' }] },
        { id: 'B', name: 'the height up the wall', slot: 'root', forms: [{ expr: 'sqrt @A' }] }
      ];
      dist = [
        { expr: L + ' ^ 2 + ' + d + ' ^ 2', 'for': 'A',
          why: 'That adds the squares. The ladder is the longest side, so its square is the biggest: to find a shorter side, subtract.' },
        { expr: L + ' - ' + d, 'for': 'A', why: 'That takes the lengths away without squaring them. Pythagoras works with the squares.' },
        { expr: L + ' ^ 2 - ' + d, 'for': 'A', why: 'Only the ladder is squared here. Square both lengths before you subtract.' }
      ];
      nums = [L, d];
    } else {
      stem = ['A ladder leans against a vertical wall. Its foot is ' + d + ' m from the wall and it reaches ' + h + ' m up the wall.',
              'Work out the length of the ladder.'];
      steps = [
        { id: 'A', name: 'the sum of the squares', slot: 'sq', forms: [{ expr: d + ' ^ 2 + ' + h + ' ^ 2' }] },
        { id: 'B', name: 'the length of the ladder', slot: 'root', forms: [{ expr: 'sqrt @A' }] }
      ];
      dist = [
        { expr: h + ' ^ 2 - ' + d + ' ^ 2', 'for': 'A',
          why: 'That subtracts. The ladder is the longest side, so add the squares of the other two.' },
        { expr: d + ' + ' + h, 'for': 'A', why: 'That adds the lengths without squaring them. Pythagoras works with the squares.' },
        { expr: d + ' ^ 2 + ' + h, 'for': 'A', why: 'Only the foot is squared here. Square both lengths before you add.' }
      ];
      nums = [d, h];
    }
    dist.push({ expr: '@A / 2', 'for': 'B', why: 'That halves it. To undo a square, take the square root.' });
    dist.push({ expr: '@A ^ 2', 'for': 'B', why: 'That squares it again. To undo a square, take the square root.' });
    return build({
      type: 'ladder', calc: true, fit: true, stem: stem,
      diagram: { kind: 'ladder', variant: variant, d: t[0] * j / 10, h: t[1] * j / 10, L: t[2] * j / 10 },
      params: { variant: variant, t: t, j: j, d: t[0] * j / 10, h: t[1] * j / 10, L: t[2] * j / 10 }, numbers: nums,
      slots: [{ id: 'sq', label: variant === 'height' ? 'the squares, subtracted' : 'the squares, added' }, { id: 'root', label: 'the square root' }],
      steps: steps, distractors: dist
    });
  }

  /* ---------- type 8: coffee and tea (simultaneous equations) ---------- */
  var BUYS = [
    { a: ['coffee', 'coffees'], b: ['tea', 'teas'], la: 'c', lb: 't' },
    { a: ['burger', 'burgers'], b: ['portion of fries', 'portions of fries'], la: 'b', lb: 'f' },
    { a: ['adult ticket', 'adult tickets'], b: ['child ticket', 'child tickets'], la: 'a', lb: 'c' },
    { a: ['pen', 'pens'], b: ['pencil', 'pencils'], la: 'p', lb: 'q' }
  ];
  function term(c, l) { return c === 1 ? l : c + l; }
  function eqTex(ca, cb, R, la, lb) {                                     // coefficients of the two letters (0 = absent) and the right-hand side in pence
    var left = [];
    if (ca) left.push(term(ca, la));
    if (cb) left.push(term(cb, lb));
    return left.join(' + ') + ' = ' + (R / 100).toFixed(2);
  }
  function qCoffee(rng) {
    var by = pick(rng, BUYS), la = by.la, lb = by.lb, p1, q1, p2, q2, cp, tp, routes, guard = 0;
    do {
      p1 = rint(rng, 1, 5); q1 = rint(rng, 1, 5); p2 = rint(rng, 1, 5); q2 = rint(rng, 1, 5);
      routes = [];
      [1, 0].forEach(function (idx) {                                      // match the coefficient of letter idx with one whole-number multiplier
        var e1 = idx ? q1 : p1, e2 = idx ? q2 : p2;
        if (e2 % e1 === 0 && e2 / e1 >= 2) routes.push({ idx: idx, scale: 0, m: e2 / e1 });
        else if (e1 % e2 === 0 && e1 / e2 >= 2) routes.push({ idx: idx, scale: 1, m: e1 / e2 });
      });
      guard++;
    } while ((p1 === p2 || q1 === q2 || p1 * q2 === p2 * q1 || !routes.length) && guard < 1000);
    do { cp = 10 * rint(rng, 8, 35); tp = 10 * rint(rng, 8, 35); } while (cp === tp);
    var E = [[p1, q1, p1 * cp + q1 * tp], [p2, q2, p2 * cp + q2 * tp]];
    var words = function (n, nm) { return n + ' ' + (n === 1 ? nm[0] : nm[1]); };
    var money = function (R) { return '£' + (R / 100).toFixed(2); };
    var tx = function (e) { return eqTex(e[0], e[1], e[2], la, lb); };
    var fct = function (e) { return 'eq:' + e.join(','); };
    var steps = [
      { id: 'A', name: 'the first equation', slot: 'e1', fact: fct(E[0]), forms: [{ tex: tx(E[0]) }] },
      { id: 'B', name: 'the second equation', slot: 'e2', fact: fct(E[1]), forms: [{ tex: tx(E[1]) }] }
    ];
    var dist = [
      { tex: (p1 + q1) + la + lb + ' = ' + (E[0][2] / 100).toFixed(2), fact: 'junk:A1', 'for': 'A',
        why: 'The ' + by.a[1] + ' and the ' + by.b[1] + ' have different prices, so they cannot be added into one lump. Give each its own letter.' },
      { tex: term(p1, la) + ' \\times ' + term(q1, lb) + ' = ' + (E[0][2] / 100).toFixed(2), fact: 'junk:A2', 'for': 'A',
        why: 'Multiplying the two amounts is not right. The total is the cost of one kind plus the cost of the other: add.' },
      { tex: tx([q1, p1, E[0][2]]), fact: fct([q1, p1, E[0][2]]), 'for': 'A',
        why: 'The numbers are the wrong way round: ' + p1 + ' goes with ' + la + ' and ' + q1 + ' goes with ' + lb + '.' },
      { tex: tx([1, 1, E[1][2]]), fact: fct([1, 1, E[1][2]]), 'for': 'B',
        why: 'That leaves out how many of each were bought. Put each number in front of its letter.' },
      { tex: tx([q2, p2, E[1][2]]), fact: fct([q2, p2, E[1][2]]), 'for': 'B',
        why: 'The numbers are the wrong way round: ' + p2 + ' goes with ' + la + ' and ' + q2 + ' goes with ' + lb + '.' }
    ];
    routes.forEach(function (r) {
      var orig = E[r.scale], other = E[1 - r.scale], m = r.m, letter = r.idx ? lb : la;
      var S = [orig[0] * m, orig[1] * m, orig[2] * m], o = 1 - r.idx, diff = S[o] - other[o];
      var big = diff > 0 ? S : other, small = diff > 0 ? other : S, res = [0, 0, big[2] - small[2]];
      res[o] = Math.abs(diff);
      var cid = 'C' + r.idx, did = 'D' + r.idx, added = [S[0] + other[0], S[1] + other[1], S[2] + other[2]], bad = [0, 0, S[2] + other[2]];
      bad[o] = Math.abs(diff);
      steps.push({ id: cid, name: 'an equation with matching ' + letter + ' terms', slot: 'match', fact: fct(S), forms: [{ tex: tx(S), deps: ['A', 'B'] }] });
      steps.push({ id: did, name: 'the equation with one letter', slot: 'elim', fact: fct(res), forms: [{ tex: tx(res), deps: [cid] }] });
      dist.push({ tex: tx([S[0], orig[1], S[2]]), fact: fct([S[0], orig[1], S[2]]), 'for': cid,
        why: 'Everything in the equation must be multiplied by ' + m + ', not just one term.' });
      dist.push({ tex: tx([S[0], S[1], orig[2]]), fact: fct([S[0], S[1], orig[2]]), 'for': cid,
        why: 'The right-hand side must be multiplied by ' + m + ' too, or the equation is no longer true.' });
      dist.push({ tex: tx(added), fact: fct(added), 'for': did,
        why: 'The ' + letter + ' terms have the same sign, so adding makes them bigger, not zero. Subtract the equations to remove the letter.' });
      dist.push({ tex: tx(bad), fact: fct(bad), 'for': did,
        why: 'The left-hand sides were subtracted but the right-hand sides were added. Do the same to both sides: subtract both.' });
    });
    return build({
      type: 'coffee', calc: true, fit: true, answers: 2,
      stem: [words(p1, by.a) + ' and ' + words(q1, by.b) + ' cost ' + money(E[0][2]) + '. ' + words(p2, by.a) + ' and ' + words(q2, by.b) + ' cost ' + money(E[1][2]) + '.',
             'Let ' + la + ' be the cost of one ' + by.a[0] + ' and ' + lb + ' the cost of one ' + by.b[0] + ', in pounds. Work out both costs.'],
      params: { by: by.a[0], p1: p1, q1: q1, p2: p2, q2: q2, cp: cp, tp: tp, la: la, lb: lb },
      numbers: [], slots: [{ id: 'e1', label: 'the first equation' }, { id: 'e2', label: 'the second equation' },
                           { id: 'match', label: 'matching one letter' }, { id: 'elim', label: 'removing a letter' }],
      steps: steps, distractors: dist
    });
  }

  /* ---------- type 9: conditional probability from a two-way table ---------- */
  var TWOWAY = [
    { rows: ['Boys', 'Girls'], cols: ['Walk', 'Bus', 'Car'], corner: 'Travel',
      ask: 'A student who comes by car is chosen at random. Work out the probability that this student is a girl.',
      cells: { A: 'boys by car', B: 'girls by bus', C: 'girls by car' } },
    { rows: ['Year 10', 'Year 11'], cols: ['Packed', 'Dinner', 'Home'], corner: 'Lunch',
      ask: 'A student who goes home for lunch is chosen at random. Work out the probability that this student is in Year 11.',
      cells: { A: 'Year 10 going home', B: 'Year 11 with dinner', C: 'Year 11 going home' } },
    { rows: ['Art', 'Music'], cols: ['Football', 'Tennis', 'Gym'], corner: 'Sport',
      ask: 'A student who chose gym is picked at random. Work out the probability that this student is on the Music course.',
      cells: { A: 'Art students in gym', B: 'Music students in tennis', C: 'Music students in gym' } }
  ];
  function qTwoWay(rng) {
    var ctx = pick(rng, TWOWAY), a = [], b = [], N, tries = 0, k;
    do {
      a = []; b = [];
      for (k = 0; k < 3; k++) { a.push(rint(rng, 3, 25)); b.push(rint(rng, 3, 25)); }
      N = a[0] + a[1] + a[2] + b[0] + b[1] + b[2];
      tries++;
    } while ((N < 50 || N > 120) && tries < 1000);
    var B = a[0] + a[1] + a[2], G = b[0] + b[1] + b[2], S = a[1] + b[1];       // the row totals and the bus total are given
    var lead = function (cell, e) { return '\\text{' + ctx.cells[cell] + '} = ' + e; };
    var steps = [
      { id: 'A', name: ctx.cells.A, slot: 'c1', forms: [{ expr: B + ' - ' + a[0] + ' - ' + a[1], tex: lead('A', B + ' - ' + a[0] + ' - ' + a[1]) }] },
      { id: 'B', name: ctx.cells.B, slot: 'c2', forms: [{ expr: S + ' - ' + a[1], tex: lead('B', S + ' - ' + a[1]) }] },
      { id: 'C', name: ctx.cells.C, slot: 'c3', forms: [{ expr: G + ' - ' + b[0] + ' - @B', tex: lead('C', G + ' - ' + b[0] + ' - \\text{' + ctx.cells.B + '}') }] },
      { id: 'D', name: 'the probability', slot: 'prob', forms: [{ expr: '@C / ( @A + @C )' }] }
    ];
    var dist = [
      { expr: B + ' - ' + a[0], tex: lead('A', B + ' - ' + a[0]), 'for': 'A', why: 'That only takes off the first column. The middle column is not in the last one either.' },
      { expr: N + ' - ' + a[0] + ' - ' + a[1], tex: lead('A', N + ' - ' + a[0] + ' - ' + a[1]), 'for': 'A', why: 'That starts from everyone. This cell is in one row, so start from that row total, ' + B + '.' },
      { expr: S + ' + ' + a[1], tex: lead('B', S + ' + ' + a[1]), 'for': 'B', why: 'The ' + a[1] + ' is part of the ' + S + ', so take it away. Adding it makes more than the column total.' },
      { expr: G + ' - ' + a[1], tex: lead('B', G + ' - ' + a[1]), 'for': 'B', why: 'The ' + a[1] + ' is in the other row. Use the column total, ' + S + ', then take away what the first row has.' },
      { expr: G + ' - ' + b[0], tex: lead('C', G + ' - ' + b[0]), 'for': 'C', deps: ['B'], why: 'That leaves out the middle cell of this row. Take that away too, to leave the last cell.' },
      { expr: N + ' - ' + b[0] + ' - ' + a[1], tex: lead('C', N + ' - ' + b[0] + ' - ' + a[1]), 'for': 'C', deps: ['B'], why: 'That starts from everyone. This cell is in one row, so start from that row total, ' + G + '.' },
      { expr: '@C / ' + N, 'for': 'D', why: 'That divides by everyone. We are told which column the student is in, so divide by that column only.' },
      { expr: '@C / ' + G, 'for': 'D', why: 'That divides by one row. The condition is the column, not a row.' },
      { expr: '@A / ( @A + @C )', 'for': 'D', why: 'That finds the probability for the other row. Put the cell you want on the top.' }
    ];
    return build({
      type: 'twoway', calc: false, fit: true,
      stem: [ctx.ask],
      diagram: { kind: 'twoway', corner: ctx.corner, head: ctx.cols.concat(['Total']), rows: [
        { label: ctx.rows[0], cells: [a[0], a[1], { fill: 'A', v: B - a[0] - a[1] }, B] },
        { label: ctx.rows[1], cells: [b[0], { fill: 'B', v: S - a[1] }, { fill: 'C', v: G - b[0] - (S - a[1]) }, G] },
        { label: 'Total', cells: ['', S, '', N] }] },
      params: { ctx: ctx.rows[0] + '/' + ctx.cols[0], a: a, b: b, N: N, B: B, G: G, S: S },
      numbers: [N, B, G, S, a[0], a[1], b[0]],
      slots: [{ id: 'c1', label: ctx.cells.A }, { id: 'c2', label: ctx.cells.B }, { id: 'c3', label: ctx.cells.C }, { id: 'prob', label: 'the probability' }],
      steps: steps, distractors: dist
    });
  }

  function question(type, rng) {
    rng = rng || Math.random;
    var q = ({ enough: qEnough, ratio: qRatio, interest: qInterest, garden: qGarden, angles: qAngles, mean: qMean, ladder: qLadder, coffee: qCoffee, twoway: qTwoWay })[type](rng);
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
  function options(Q, S, rng, cap) {
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
    // The page lowers the cap (never below 4) on a screen too short for six.
    cap = Math.max(4, Math.min(6, cap || 6));
    var vmax = Math.min(4, cap - 2);
    var v = valid.slice(0, vmax);
    shuffled(rng, extra).forEach(function (o) { if (v.length < vmax) v.push(o); });
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
    TYPES: TYPES, METHOD: METHOD, question: question, makeRng: makeRng, evalExpr: evalExpr, texOf: texOf,
    newState: newState, options: options, choose: choose, hint: hint, finished: finished, unaided: unaided
  };
})(typeof window !== 'undefined' ? window : this);
