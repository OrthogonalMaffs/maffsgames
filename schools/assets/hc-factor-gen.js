/* The HC Factor: the question bank (contract HC-FACTOR, build lane, 27 Oct 2026; bank-first, canon 8.2.1).
 *
 * One module, pure data, no DOM. games/hc-factor/ imports it, and the 6 P's could later. Every answer is computed from the
 * question's own numbers, so it is correct by construction; scripts/verify-hc-factor.py recomputes each one through a
 * separate code path (polynomial multiplication) and plays random answers through mark() to compare.
 *
 *   MaffsHCFactor.STAGES                six stages, easiest first (name, what it drills, marks a question)
 *   MaffsHCFactor.bank(stage)           at least 40 distinct questions per stage, fixed seed, the same every load
 *   MaffsHCFactor.session(stage, seed)  six questions of the bank, the kinds of the stage taken in turn
 *   MaffsHCFactor.mark(step, vals)      {kind: 'right' | 'format' | 'slip' | 'wrong', why}; vals are the typed numbers in
 *                                       the step's layout order (a sign box gives a signed number), or, for a sign-grid
 *                                       step, the index of the option chosen
 *
 * A polynomial is [c2, c1, c0]: c2 x^2 + c1 x + c0. A box answer is marked by VALUE: whatever the boxes multiply out to
 * is compared with the target, so the two brackets of a factorisation may come in either order. Stage 3 is the one place
 * a correct value can still be refused: an answer that multiplies out right but is not fully factorised gets the
 * 'format' message, not 'wrong'.
 *
 * A question: { key, stage, sub, stem, instr, steps: [step...], worked: { lines, grid }, marks }.
 * A step is one of
 *   { kind: 'boxes', form, layout, target, canon?, slips: [{poly, why}], generic, formatWhy? }
 *   { kind: 'signs', correct, options, whys: [text per option], named: [bool per option], rule }
 * layout is a list of tokens: { lit: 'x²' } text, or { num: true, sign: bool } a typed-number box (sign: true gives it a
 * plus/minus toggle in front, so the typed value is signed).
 * Text with a pair of § marks holds TeX between them.
 */
(function (root) {
  'use strict';

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
  function int(rng, lo, hi) { return lo + Math.floor(rng() * (hi - lo + 1)); }
  function nonzero(rng, max) { var v = int(rng, 1, max); return rng() < 0.5 ? -v : v; }
  function shuffle(rng, a) {
    a = a.slice();
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(rng() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a; }
  function same(p, q) { return p[0] === q[0] && p[1] === q[1] && p[2] === q[2]; }

  /* ---------- text ---------- */
  function sg(n) { return n < 0 ? '-' : '+'; }
  function bk(n) { return '(x ' + sg(n) + ' ' + Math.abs(n) + ')'; }            // (x + 3)
  function inner(m, n) { return (m === 1 ? '' : String(m)) + 'x ' + sg(n) + ' ' + Math.abs(n); }   // 2x + 3
  function polyTex(c) {
    var out = '', pw = [2, 1, 0];
    for (var i = 0; i < 3; i++) {
      var k = c[i];
      if (!k) continue;
      var mag = Math.abs(k), p = pw[i];
      var body = p === 0 ? String(mag) : (mag === 1 ? '' : String(mag)) + 'x' + (p === 2 ? '^2' : '');
      out += out === '' ? (k < 0 ? '-' : '') + body : (k < 0 ? ' - ' : ' + ') + body;
    }
    return out || '0';
  }
  function T(tex) { return '§' + tex + '§'; }
  function lin(c) { return polyTex([0, c, 0]); }                                   // the x term alone: 3x, -x, 0
  function add(parts) {                                                            // 'x^2', '-3x', '5' -> x^2 - 3x + 5
    return parts.map(function (t, i) { return i === 0 ? t : (t.charAt(0) === '-' ? ' - ' + t.slice(1) : ' + ' + t); }).join('');
  }
  function par(n) { return n < 0 ? '(' + n + ')' : String(n); }                    // a number in a product

  /* ---------- the layouts: what the boxes look like, and what they multiply out to ---------- */
  var LIT = function (t) { return { lit: t }; };
  var NUM = function (sign) { return { num: true, sign: !!sign }; };
  var LAYOUTS = {
    lin2: [NUM(false), LIT('x'), NUM(true)],                                       // ☐x + ☐
    lin2neg: [NUM(true), LIT('x'), NUM(true)],                                     // ±☐x ± ☐
    quad3: [NUM(false), LIT('x²'), NUM(true), LIT('x'), NUM(true)],                // ☐x² + ☐x + ☐
    quad3lead1: [LIT('x²'), NUM(true), LIT('x'), NUM(true)],                       // x² + ☐x + ☐
    hcfnum: [NUM(false), LIT('('), NUM(false), LIT('x'), NUM(true), LIT(')')],     // ☐(☐x + ☐)
    hcfx: [NUM(false), LIT('x('), NUM(false), LIT('x'), NUM(true), LIT(')')],      // ☐x(☐x + ☐)
    brackets: [LIT('(x'), NUM(true), LIT(')(x'), NUM(true), LIT(')')]              // (x ☐ ☐)(x ☐ ☐)
  };
  // What a set of typed numbers multiplies out to.
  function evalForm(form, v) {
    switch (form) {
      case 'lin2': case 'lin2neg': return [0, v[0], v[1]];
      case 'quad3': return [v[0], v[1], v[2]];
      case 'quad3lead1': return [1, v[0], v[1]];
      case 'hcfnum': return [0, v[0] * v[1], v[0] * v[2]];
      case 'hcfx': return [v[0] * v[1], v[0] * v[2], 0];
      case 'brackets': return [1, v[0] + v[1], v[0] * v[1]];
    }
    return [NaN, NaN, NaN];
  }

  /* ---------- marking ---------- */
  var FORMAT_WHY = "That multiplies out correctly, but it isn't fully factorised yet. Take out the biggest factor you can, so nothing is left to share inside the bracket.";
  function mark(step, vals) {
    if (step.kind === 'signs') {
      var c = vals;
      if (c === step.correct) return { kind: 'right', why: step.rule };
      return { kind: step.named[c] ? 'slip' : 'wrong', why: step.whys[c] };
    }
    var p = evalForm(step.form, vals);
    if (same(p, step.target)) {
      if (step.canon && vals.join() !== step.canon.join()) {
        return { kind: 'format', why: (vals[0] < 0 ? 'Take out a positive factor. ' : '') + FORMAT_WHY };
      }
      return { kind: 'right', why: '' };
    }
    for (var i = 0; i < step.slips.length; i++) {
      if (same(p, step.slips[i].poly)) return { kind: 'slip', why: step.slips[i].why };
    }
    return { kind: 'wrong', why: step.generic };
  }

  /* ---------- building steps ---------- */
  function boxes(form, target, slips, generic, canon, sol) {
    var seen = [target.join()], keep = [];
    slips.forEach(function (s) {            // a slip that is the right answer, or a repeat, is not a slip
      if (seen.indexOf(s.poly.join()) === -1) { seen.push(s.poly.join()); keep.push(s); }
    });
    var st = { kind: 'boxes', form: form, layout: LAYOUTS[form], target: target, slips: keep, generic: generic };
    if (canon) st.canon = canon;
    st.sol = sol || canon;
    return st;
  }

  var SIGN_RULE = 'Same signs when c is positive (both the sign of b). Different signs when c is negative.';
  var SIGN_OPTIONS = ['Both +', 'Both −', 'One of each'];
  // The sign grid: b and c decide the signs of the two brackets.
  function signsStep(b, c) {
    var correct = c < 0 ? 2 : (b > 0 ? 0 : 1);
    var cs = T(String(c)), bs = T(String(b));
    var whys = [], named = [false, false, false];
    var reason = c < 0
      ? 'c is ' + cs + ', negative, so the signs are different.'
      : 'c is ' + cs + ', positive, so the signs are the same, and b is ' + bs + ', ' + (b > 0 ? 'positive, so both +.' : 'negative, so both −.');
    for (var o = 0; o < 3; o++) {
      if (o === correct) { whys.push(reason); continue; }
      if (c < 0) {
        named[o] = true;     // same signs chosen when c is negative
        whys.push('Two numbers with the same sign multiply to a positive. c is ' + cs + ', negative, so the signs must be different.');
      } else if (o === 2) {
        whys.push('Different signs multiply to a negative. c is ' + cs + ', positive, so the signs are the same.');
      } else if (o === 0) {
        named[o] = true;     // both + chosen when b is negative
        whys.push('Two + signs would make b positive. b is ' + bs + ', negative, so both signs are −.');
      } else {
        whys.push('Two − signs would make b negative. b is ' + bs + ', positive, so both signs are +.');
      }
    }
    return { kind: 'signs', correct: correct, options: SIGN_OPTIONS, whys: whys, named: named, rule: reason + ' ' + SIGN_RULE };
  }

  /* ---------- the stages ---------- */
  var STAGES = {
    1: { n: 1, name: 'Expand', blurb: 'One bracket: multiply everything inside by the number outside.', subs: ['one'], marks: 1 },
    2: { n: 2, name: 'Minus signs and x outside', blurb: 'A minus outside the bracket, and an x outside the bracket.', subs: ['neg', 'xout', 'kxout'], marks: 1 },
    3: { n: 3, name: 'Factorise fully', blurb: 'Take the highest common factor out of the front.', subs: ['num', 'x'], marks: 1 },
    4: { n: 4, name: 'Double brackets', blurb: 'Expand (x + a)(x + b) with the grid.', subs: ['dbl'], marks: 1 },
    5: { n: 5, name: 'The sign grid', blurb: 'Choose the signs of the two brackets from b and c.', subs: ['signs'], marks: 1 },
    6: { n: 6, name: 'Factorise x² + bx + c', blurb: 'The signs first, then the two numbers.', subs: ['fac'], marks: 2 }
  };

  function gen(stage, sub, rng) {
    var q = { stage: stage, sub: sub, steps: [], worked: { lines: [], grid: null }, marks: STAGES[stage].marks };
    var k, a, b, m, n, p, r, tgt;
    if (stage === 1) {
      k = int(rng, 2, 9); a = nonzero(rng, 9);
      q.key = 'one:' + k + ',' + a;
      q.stem = 'Expand ' + T(k + '(' + inner(1, a) + ')') + '.';
      tgt = [0, k, k * a];
      q.steps.push(boxes('lin2', tgt, [{ poly: [0, k, a], why: 'You multiplied the x by ' + k + ' but not the ' + a + '. Everything inside the bracket gets multiplied: ' + T(k + ' \\times ' + par(a) + ' = ' + (k * a)) + '.' }],
        'Multiply both terms inside the bracket by ' + k + '.', null, [k, k * a]));
      q.worked.lines = ['Multiply every term in the bracket by ' + T(String(k)) + '.',
        T(k + ' \\times x = ' + k + 'x') + ' and ' + T(k + ' \\times ' + par(a) + ' = ' + (k * a)) + '.',
        'So ' + T(polyTex(tgt)) + '.'];
    } else if (stage === 2) {
      a = nonzero(rng, 9);
      if (sub === 'neg') {
        k = int(rng, 2, 9);
        q.key = 'neg:' + k + ',' + a;
        q.stem = 'Expand ' + T('-' + k + '(' + inner(1, a) + ')') + '.';
        tgt = [0, -k, -k * a];
        q.steps.push(boxes('lin2neg', tgt, [{ poly: [0, -k, k * a], why: 'The minus sign belongs to the ' + k + ', so it multiplies the second term too: ' + T('-' + k + ' \\times ' + par(a) + ' = ' + (-k * a)) + '.' }],
          'The number outside is -' + k + ', so multiply both terms by -' + k + '.', null, [-k, -k * a]));
        q.worked.lines = ['The number outside is ' + T('-' + k) + ', minus sign included. Multiply every term by it.',
          T('-' + k + ' \\times x = -' + k + 'x') + ' and ' + T('-' + k + ' \\times ' + par(a) + ' = ' + (-k * a)) + '.',
          'So ' + T(polyTex(tgt)) + '.'];
      } else if (sub === 'xout') {
        q.key = 'xout:' + a;
        q.stem = 'Expand ' + T('x(' + inner(1, a) + ')') + '.';
        tgt = [1, a, 0];
        q.steps.push(boxes('quad3', tgt, [{ poly: [1, 0, a], why: 'The x outside multiplies the ' + a + ' too: ' + T('x \\times ' + par(a) + ' = ' + (a === 1 ? '' : a === -1 ? '-' : a) + 'x') + ', not just ' + a + '.' }],
          'The x outside multiplies both terms: x times x is x², and x times ' + a + ' is ' + a + 'x.', null, [1, a, 0]));
        q.worked.lines = ['The x outside multiplies every term inside.',
          T('x \\times x = x^2') + ' and ' + T('x \\times ' + par(a) + ' = ' + polyTex([0, a, 0])) + '.',
          'So ' + T(polyTex(tgt)) + ', with no number term.'];
      } else {
        k = int(rng, 2, 9);
        q.key = 'kxout:' + k + ',' + a;
        q.stem = 'Expand ' + T(k + 'x(' + inner(1, a) + ')') + '.';
        tgt = [k, k * a, 0];
        q.steps.push(boxes('quad3', tgt, [{ poly: [k, a, 0], why: 'The ' + k + 'x outside multiplies the ' + a + ' as well: ' + T(k + 'x \\times ' + par(a) + ' = ' + polyTex([0, k * a, 0])) + '.' }],
          'The ' + k + 'x outside multiplies both terms.', null, [k, k * a, 0]));
        q.worked.lines = ['The ' + T(k + 'x') + ' outside multiplies every term inside.',
          T(k + 'x \\times x = ' + k + 'x^2') + ' and ' + T(k + 'x \\times ' + par(a) + ' = ' + polyTex([0, k * a, 0])) + '.',
          'So ' + T(polyTex(tgt)) + ', with no number term.'];
      }
    } else if (stage === 3) {
      do { k = sub === 'x' ? int(rng, 1, 9) : int(rng, 2, 9); m = int(rng, 1, 6); n = nonzero(rng, 9); } while (gcd(m, n) !== 1);
      if (sub === 'num') {
        q.key = 'num:' + k + ',' + m + ',' + n;
        tgt = [0, k * m, k * n];
        q.stem = 'Factorise fully ' + T(polyTex(tgt)) + '.';
        q.steps.push(boxes('hcfnum', tgt, [{ poly: [0, k * m, k * k * n], why: 'You divided the x term by ' + k + ' but left the number term as it was. Divide both terms by ' + k + '.' }],
          'Take out the highest common factor of ' + Math.abs(k * m) + ' and ' + Math.abs(k * n) + '. Multiply it back out to check.', [k, m, n]));
        q.worked.lines = ['The biggest number that goes into both ' + T(k * m + 'x') + ' and ' + T(String(Math.abs(k * n))) + ' is ' + T(String(k)) + '.',
          'Divide each term by ' + T(String(k)) + ': ' + T(k * m + 'x \\div ' + k + ' = ' + polyTex([0, m, 0])) + ' and ' + T((k * n) + ' \\div ' + k + ' = ' + n) + '.',
          'So ' + T(k + '(' + inner(m, n) + ')') + '. Expand it to check.'];
      } else {
        q.key = 'x:' + k + ',' + m + ',' + n;
        tgt = [k * m, k * n, 0];
        q.stem = 'Factorise fully ' + T(polyTex(tgt)) + '.';
        q.steps.push(boxes('hcfx', tgt, [{ poly: [k * m, k * k * n, 0], why: 'You divided the x² term but left the x term as it was. Divide both terms by ' + (k === 1 ? 'x' : k + 'x') + '.' }],
          'Take out the highest common factor, number and x. Multiply it back out to check.', [k, m, n]));
        q.worked.lines = [k === 1 ? 'Both terms have an ' + T('x') + ' and nothing else in common, so the highest common factor is ' + T('x') + '.'
            : 'The biggest number that goes into ' + T(String(Math.abs(k * m))) + ' and ' + T(String(Math.abs(k * n))) + ' is ' + T(String(k)) + '. Both terms have an x as well, so the highest common factor is ' + T(k + 'x') + '.',
          'Divide each term by ' + T(k === 1 ? 'x' : k + 'x') + ': ' + T(polyTex([k * m, 0, 0]) + ' \\div ' + (k === 1 ? 'x' : k + 'x') + ' = ' + polyTex([0, m, 0])) + ' and ' + T(polyTex([0, k * n, 0]) + ' \\div ' + (k === 1 ? 'x' : k + 'x') + ' = ' + n) + '.',
          'So ' + T((k === 1 ? '' : k) + 'x(' + inner(m, n) + ')') + '. Expand it to check.'];
      }
    } else if (stage === 4) {
      a = nonzero(rng, 9); b = nonzero(rng, 9);
      q.key = 'dbl:' + Math.min(a, b) + ',' + Math.max(a, b);
      q.stem = 'Expand and simplify ' + T(bk(a) + bk(b)) + '.';
      tgt = [1, a + b, a * b];
      q.steps.push(boxes('quad3lead1', tgt, [
        { poly: [1, 0, a * b], why: 'That is missing the middle term. Multiplying two brackets gives four pieces, and the two x pieces join to make the middle term: ' + T(add([lin(b), lin(a)]) + ' = ' + lin(a + b)) + '.' },
        { poly: [1, a + b, a + b], why: 'The number term is the two numbers multiplied, not added: ' + T(par(a) + ' \\times ' + par(b) + ' = ' + (a * b)) + '.' }],
        'Use the grid: four pieces, then collect the two x terms.', null, [a + b, a * b]));
      q.worked.grid = { cols: ['x', String(b)], rows: ['x', String(a)],
        cells: [['x^2', polyTex([0, b, 0])], [polyTex([0, a, 0]), String(a * b)]] };
      q.worked.lines = ['Fill the grid: ' + T('x') + ' and ' + T(String(b)) + ' across the top, ' + T('x') + ' and ' + T(String(a)) + ' down the side. Multiply each pair.',
        'The four pieces: ' + T(add(['x^2', lin(b), lin(a), String(a * b)])) + '.',
        'Collect the x terms: ' + T(add([lin(a), lin(b)]) + ' = ' + lin(a + b)) + '. So ' + T(polyTex(tgt)) + '.'];
    } else {
      do { p = nonzero(rng, 9); r = nonzero(rng, 9); } while (p + r === 0);
      var lo = Math.min(p, r), hi = Math.max(p, r), B = p + r, C = p * r;
      q.key = 'fac:' + lo + ',' + hi;
      var quad = T(polyTex([1, B, C]));
      q.steps.push(signsStep(B, C));
      if (stage === 5) {
        q.stem = 'The brackets will be ' + T('(x \\; ?)(x \\; ?)') + '. Which signs go in them for ' + quad + '?';
      } else {
        q.stem = 'Factorise ' + quad + '. Choose the signs first, then type the numbers.';
        tgt = [1, B, C];
        q.steps.push(boxes('brackets', tgt, [
          { poly: [1, -B, C], why: 'Those numbers multiply to ' + C + ' but add to ' + (-B) + '. They need to add to ' + B + ', the b: swap both signs.' },
          { poly: [1, B, -C], why: 'Those numbers add to ' + B + ' but multiply to ' + (-C) + '. They need to multiply to ' + C + ', the c: check the signs.' }],
          'Two numbers that multiply to c (' + C + ') and add to b (' + B + ').', null, [lo, hi]));
      }
      q.worked.lines = [signsStep(B, C).rule,
        'Factor pairs of ' + T(String(Math.abs(C))) + ': ' + pairs(Math.abs(C)) + '.',
        'Two numbers that multiply to ' + T(String(C)) + ' and add to ' + T(String(B)) + ': ' + T(String(lo)) + ' and ' + T(String(hi)) + '.' + (C < 0 ? ' The bigger one takes the sign of b.' : ''),
        'So ' + T(bk(lo) + bk(hi)) + '.'];
    }
    q.instr = q.steps[0].kind === 'signs' ? 'Choose the signs' : 'Type your answer';
    return q;
  }
  function pairs(n) {
    var out = [];
    for (var i = 1; i * i <= n; i++) if (n % i === 0) out.push(T(i + ' \\times ' + (n / i)));
    return out.join(', ');
  }

  /* ---------- the banks ---------- */
  var BANK_SIZE = 40, cache = {};
  function bank(stage) {
    if (cache[stage]) return cache[stage];
    var rng = makeRng(20261027 + stage * 7919), subs = STAGES[stage].subs, out = [], seen = {}, tries = 0;
    while (out.length < BANK_SIZE && tries++ < 20000) {
      var q = gen(stage, subs[out.length % subs.length], rng);
      if (seen[q.key]) continue;
      seen[q.key] = true;
      out.push(q);
    }
    cache[stage] = out;
    return out;
  }
  // Six questions: the kinds of the stage taken in turn, each kind's questions in a seeded random order.
  function session(stage, seed, count) {
    count = count || 6;
    var rng = makeRng(seed), subs = STAGES[stage].subs, by = {}, out = [];
    subs.forEach(function (s) { by[s] = shuffle(rng, bank(stage).filter(function (q) { return q.sub === s; })); });
    var order = shuffle(rng, subs);
    for (var i = 0; out.length < count && i < 200; i++) {
      var s = order[i % order.length];
      if (by[s].length) out.push(by[s].shift());
    }
    return out;
  }

  root.MaffsHCFactor = { STAGES: STAGES, bank: bank, session: session, mark: mark, makeRng: makeRng, SIGN_RULE: SIGN_RULE, FORMAT_WHY: FORMAT_WHY };
})(typeof window !== 'undefined' ? window : globalThis);
