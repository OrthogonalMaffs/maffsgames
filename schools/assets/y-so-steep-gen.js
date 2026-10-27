/* Y So Steep?: the question bank (contract Y-SO-STEEP, build lane, 27 Oct 2026; bank-first, canon 8.2.1).
 *
 * One module, no DOM. games/y-so-steep/ imports it, and the 6 P's will later (in its own contract), never a copy.
 * Every m and c is computed from the item's own numbers with exact fractions ([n, d], d > 0, lowest terms), so each
 * answer is correct by construction; scripts/verify-y-so-steep.py recomputes every one from the printed stem.
 *
 *   MaffsYSoSteep.STAGES                  six stages: Foundation 1-2, Higher 3-6 (name, mode, steps, marks)
 *   MaffsYSoSteep.bank(stage, fractions)  at least 45 distinct items, fixed seed. fractions: false (the default) gives
 *                                         whole-number gradients and intercepts only; true adds fractions (denominators
 *                                         2-5) to stages 3-6. Stage 3 (rearrange it) exists in full only with fractions.
 *   MaffsYSoSteep.session(stage, seed, fractions, count)   the items of a round, kinds taken in turn
 *   MaffsYSoSteep.mark(item, stepIndex, raws)   {kind: 'right'|'slip'|'wrong'|'unreadable', ok: [bool per box], why}
 *                                         raws are the typed strings, read by MaffsAnswer.fraction() (answer.js) and
 *                                         compared by VALUE; there is no parser in this file.
 *   MaffsYSoSteep.eqTex(m, c)             y = mx + c written in full, as TeX (m, c as [n, d])
 *   MaffsYSoSteep.fstr(f)                 a fraction as typed: 3 or 3/2
 *
 * An item: { key, stage, sub, stem, figure?, steps, worked, marks, line: {m, c}, needsFractions, neat? }
 * A step: { id, labels: ['m'] | ['c'] | ['m','c'], keys: [[n,d]...], slips: [{vals: [f|null...], why}], instr, generic }
 * Text with a pair of § marks holds TeX between them.
 */
(function (root) {
  'use strict';

  /* ---------- fractions: [n, d] ---------- */
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a || 1; }
  function F(n, d) { d = d === undefined ? 1 : d; if (d < 0) { n = -n; d = -d; } var g = gcd(n, d); return [n / g, d / g]; }
  function add(a, b) { return F(a[0] * b[1] + b[0] * a[1], a[1] * b[1]); }
  function sub(a, b) { return F(a[0] * b[1] - b[0] * a[1], a[1] * b[1]); }
  function mul(a, b) { return F(a[0] * b[0], a[1] * b[1]); }
  function div(a, b) { return F(a[0] * b[1], a[1] * b[0]); }
  function neg(a) { return [-a[0], a[1]]; }
  function eq(a, b) { return a[0] === b[0] && a[1] === b[1]; }
  function isInt(a) { return a[1] === 1; }
  function fstr(f) { return f[1] === 1 ? String(f[0]) : f[0] + '/' + f[1]; }
  function ftex(f) { return f[1] === 1 ? String(f[0]) : (f[0] < 0 ? '-' : '') + '\\frac{' + Math.abs(f[0]) + '}{' + f[1] + '}'; }
  function atex(f) { return ftex([Math.abs(f[0]), f[1]]); }
  function par(f) { return f[0] < 0 ? '(' + ftex(f) + ')' : ftex(f); }
  var Z = [0, 1];

  // y = mx + c in full
  function eqTex(m, c) {
    var mt = '';
    if (m[0] !== 0) mt = (eq(m, F(1)) ? '' : eq(m, F(-1)) ? '-' : ftex(m)) + 'x';
    var out = 'y = ';
    if (mt) {
      out += mt;
      if (c[0] !== 0) out += (c[0] < 0 ? ' - ' : ' + ') + atex(c);
    } else out += ftex(c);
    return out;
  }
  function T(tex) { return '§' + tex + '§'; }
  function pt(x, y) { return '(' + x + ', ' + y + ')'; }

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
  function shuffle(rng, a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(rng() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  // a gradient: whole (|n| in 1..maxN) or, with fractions on, a fraction p/q (q in 2..5, lowest terms); negative when asked
  function gradient(rng, negative, fractions, maxN, fracShare) {
    var m;
    if (fractions && rng() < fracShare) {
      var q, p;
      do { q = int(rng, 2, 5); p = int(rng, 1, 7); } while (gcd(p, q) !== 1);
      m = [p, q];
    } else m = [int(rng, 1, maxN), 1];
    return negative ? neg(m) : m;
  }

  /* ---------- marking ---------- */
  function mark(item, si, raws) {
    var step = item.steps[si], A = root.MaffsAnswer, vals = [];
    for (var i = 0; i < raws.length; i++) {
      var f = A && A.fraction ? A.fraction(raws[i]) : null;
      if (!f) return { kind: 'unreadable', ok: [], why: '' };
      vals.push(F(f.num, f.den));
    }
    var ok = step.keys.map(function (k, j) { return eq(vals[j], k); });
    if (ok.every(Boolean)) return { kind: 'right', ok: ok, why: '' };
    for (var s = 0; s < step.slips.length; s++) {
      var sl = step.slips[s], hit = true;
      for (var j = 0; j < sl.vals.length; j++) if (sl.vals[j] && !eq(sl.vals[j], vals[j])) hit = false;
      if (hit) return { kind: 'slip', ok: ok, why: sl.why };
    }
    return { kind: 'wrong', ok: ok, why: step.generic };
  }
  // slips with a value equal to the right answer (or a repeat) are dropped: a right answer is never named a slip
  function slips(keys, list) {
    var seen = [keys.map(fstr).join('|')], out = [];
    list.forEach(function (s) {
      if (!s) return;
      var id = s.vals.map(function (v, i) { return v ? fstr(v) : fstr(keys[i]); }).join('|');
      if (seen.indexOf(id) === -1) { seen.push(id); out.push(s); }
    });
    return out;
  }

  var WHY = {
    sign: function (m) { return 'The sign belongs to the gradient: ' + (m[0] < 0 ? 'a falling line goes down as x goes up, so m is negative.' : 'a rising line has a positive gradient.'); },
    run: 'You divided run by rise. The gradient is rise over run: how far up for each step across.',
    xint: 'That is where the line crosses the x-axis. c is where it crosses the y-axis, the line at x = 0.',
    sub: 'Check the substitution: put the point into y = mx + c, then c = y - mx. Take away mx, do not add it.',
    swap: 'm is the number multiplying x, and c is the number on its own: they are the other way round.',
    csign: 'The sign in front of the number belongs to c.',
    notneg: 'Flipped, but not negated. A perpendicular gradient is the negative reciprocal: flip it and change its sign.',
    notrec: 'Negated, but not flipped. A perpendicular gradient is the negative reciprocal: flip it and change its sign.',
    same: 'That is the gradient of the line you were given, so it is parallel to it. A perpendicular line has the negative reciprocal.'
  };

  /* ---------- the stages ---------- */
  var STAGES = {
    1: { n: 1, name: 'Read it', mode: 'foundation', blurb: 'Read m and c straight off y = mx + c.', marks: 1, needsFractions: false },
    2: { n: 2, name: 'Spot it', mode: 'foundation', blurb: 'Read m and c from a line on a grid.', marks: 1, needsFractions: false },
    3: { n: 3, name: 'Rearrange it', mode: 'higher', blurb: 'Rearrange to y = mx + c, then read m and c.', marks: 1, needsFractions: true },
    4: { n: 4, name: 'Two points', mode: 'higher', blurb: 'The gradient, then c, then the equation.', marks: 3, needsFractions: false },
    5: { n: 5, name: 'Point and gradient', mode: 'higher', blurb: 'Use the point to find c, then write the equation.', marks: 2, needsFractions: false },
    6: { n: 6, name: 'Parallel and perpendicular', mode: 'higher', blurb: 'Find the gradient from the line you are given, then c.', marks: 3, needsFractions: false }
  };
  var SUBS = { 1: ['std', 'rev', 'unit', 'zeroc', 'std', 'rev', 'zerom'], 2: ['grid'], 3: ['divide', 'move', 'both'], 4: ['pts'], 5: ['pg'], 6: ['par', 'perp'] };

  function mcStep(m, c, extra, instr, generic) {
    var keys = [m, c];
    return { id: 'eq', labels: ['m', 'c'], keys: keys, slips: slips(keys, extra), instr: instr || 'Type m and c', generic: generic || 'Write the line as y = mx + c. m multiplies x, and c is where it crosses the y-axis.' };
  }
  function oneStep(id, label, key, extra, instr, generic) {
    return { id: id, labels: [label], keys: [key], slips: slips([key], extra), instr: instr, generic: generic };
  }

  // the slips of an equation step, from the line and the point(s) it came through
  function eqSlips(m, c, points) {
    var l = [];
    if (m[0] !== 0) l.push({ vals: [neg(m), null], why: WHY.sign(m) });
    if (m[0] !== 0) l.push({ vals: [div(F(1), m), null], why: WHY.run });
    points.forEach(function (p) { l.push({ vals: [null, add(F(p[1]), mul(m, F(p[0])))], why: WHY.sub }); });
    return l;
  }
  function neatPoint(points) {
    var best = points[0];
    points.forEach(function (p) { if (Math.abs(p[0]) < Math.abs(best[0])) best = p; });
    return best;
  }
  function subLine(m, p, c) {      // y = mx + c with the point put in, c found
    var mx = mul(m, F(p[0]));
    return 'Put ' + T(pt(p[0], p[1])) + ' into ' + T('y = mx + c') + ': ' + T(p[1] + ' = ' + par(m) + ' \\times ' + par(F(p[0])) + ' + c') + ', so ' + T('c = ' + p[1] + (mx[0] < 0 ? ' + ' : ' - ') + par(F(Math.abs(mx[0]), mx[1])) + ' = ' + ftex(c)) + '.';
  }

  /* ---------- the items ---------- */
  function gen(stage, sub, rng, negative, fractions, idx) {
    var it = { stage: stage, sub: sub, worked: [], marks: STAGES[stage].marks, needsFractions: false, steps: [] };
    var m, c, q, p, x1, y1, x2, y2, dx, i;
    if (stage === 1) {
      c = F(int(rng, -9, 9));
      m = sub === 'zerom' ? Z : sub === 'unit' ? F(negative ? -1 : 1) : gradient(rng, negative, false, 9, 0);
      if (sub === 'zeroc') c = Z;
      if (sub === 'zerom' && c[0] === 0) c = F(int(rng, 1, 9));
      if (sub === 'std' || sub === 'rev') { if (c[0] === 0) c = F(int(rng, 1, 9)); }
      var eqs;
      if (sub === 'rev' && m[0] !== 0) eqs = 'y = ' + c[0] + (m[0] < 0 ? ' - ' : ' + ') + (Math.abs(m[0]) === 1 ? '' : Math.abs(m[0])) + 'x';
      else eqs = eqTex(m, c);
      it.key = 's1:' + eqs;
      it.stem = 'Here is a line: ' + T(eqs) + '. What are m and c?';
      it.line = { m: m, c: c };
      var ex = [];
      if (m[0] !== 0) ex.push({ vals: [neg(m), null], why: WHY.sign(m) });
      if (c[0] !== 0) ex.push({ vals: [null, neg(c)], why: WHY.csign });
      if (!eq(m, c)) ex.push({ vals: [c, m], why: WHY.swap });
      it.steps.push(mcStep(m, c, ex));
      it.worked = ['A line is ' + T('y = mx + c') + ': m is the number multiplying x, and c is the number on its own.',
        sub === 'zerom' ? 'There is no x term, so ' + T('m = 0') + ': the line is flat.' : sub === 'zeroc' ? 'There is no number on its own, so ' + T('c = 0') + ': the line goes through the origin.' : 'Here ' + T('m = ' + ftex(m)) + ' and ' + T('c = ' + ftex(c)) + '.',
        'So ' + T(eqTex(m, c)) + '.'];
    } else if (stage === 2) {
      var mm, cc, lat;
      do {
        mm = int(rng, 1, 4) * (negative ? -1 : 1); cc = int(rng, -5, 5);
        lat = [];
        for (i = -6; i <= 6; i++) { var yy = mm * i + cc; if (yy >= -6 && yy <= 6) lat.push([i, yy]); }
      } while (lat.length < 2);
      m = F(mm); c = F(cc);
      var a = lat[0], b = lat[1];                 // the closest pair of lattice points in view
      for (i = 0; i + 1 < lat.length; i++) if (lat[i + 1][0] - lat[i][0] === 1) { a = lat[i]; b = lat[i + 1]; break; }
      it.key = 's2:' + mm + ',' + cc;
      it.stem = 'Find the equation of the line on the grid. What are m and c?';
      it.line = { m: m, c: c };
      it.figure = { range: 6, m: mm, c: cc, pts: [a, b] };
      var xi = mm !== 0 && (-cc) % mm === 0 ? F(-cc / mm) : null;
      it.steps.push(mcStep(m, c, [
        { vals: [neg(m), null], why: WHY.sign(m) },
        xi ? { vals: [null, xi], why: WHY.xint } : null,
        { vals: [div(F(1), m), null], why: WHY.run }]));
      var run = b[0] - a[0], rise = b[1] - a[1];
      it.worked = ['The line crosses the y-axis at ' + T(pt(0, cc)) + ', so ' + T('c = ' + cc) + '.',
        'From ' + T(pt(a[0], a[1])) + ' to ' + T(pt(b[0], b[1])) + ': run ' + T(String(run)) + ', rise ' + T(String(rise)) + '. Gradient = rise over run = ' + T('m = ' + ftex(F(rise, run))) + '.',
        'So ' + T(eqTex(m, c)) + '.'];
    } else if (stage === 3) {
      // rearrange: build from y = mx + c, print in a form that needs rearranging
      var k;
      if (sub === 'divide') {            // q y = p x + r
        q = int(rng, 2, 5); p = int(rng, 1, 9) * (negative ? -1 : 1);
        if (!fractions) { p = q * int(rng, 1, 4) * (negative ? -1 : 1); }
        c = F(int(rng, -6, 6)); if (c[0] === 0) c = F(int(rng, 1, 6));
        var rr = c[0] * q;
        m = F(p, q);
        it.stem = 'Rearrange ' + T(q + 'y = ' + (p === 1 ? '' : p === -1 ? '-' : p) + 'x ' + (rr < 0 ? '- ' : '+ ') + Math.abs(rr)) + ' into the form ' + T('y = mx + c') + '. What are m and c?';
        it.worked = ['Divide every term by ' + T(String(q)) + ': ' + T('y = ' + eqTex(m, c).slice(4)) + '.'];
      } else if (sub === 'move') {       // a x + y = k
        k = int(rng, -9, 9); var aa = int(rng, 1, 7) * (negative ? 1 : -1);   // m = -a, so a > 0 gives a falling line
        m = F(-aa); c = F(k);
        it.stem = 'Rearrange ' + T((aa === 1 ? '' : aa === -1 ? '-' : aa) + 'x + y = ' + k) + ' into the form ' + T('y = mx + c') + '. What are m and c?';
        it.worked = ['Take ' + T((aa === 1 ? '' : aa === -1 ? '-' : aa) + 'x') + ' from both sides: ' + T(eqTex(m, c)) + '.'];
      } else {                           // a x + b y = k, with m = -a/b
        var bq = int(rng, 2, 5), an;
        do { an = int(rng, 1, 7); } while (gcd(an, bq) !== 1 && fractions);
        if (!fractions) an = bq * int(rng, 1, 3);
        if (!negative) an = -an;
        var kk = int(rng, -4, 4) * bq; if (kk === 0) kk = bq;
        m = F(-an, bq); c = F(kk, bq);
        it.stem = 'Rearrange ' + T((an === 1 ? '' : an === -1 ? '-' : an) + 'x + ' + bq + 'y = ' + kk) + ' into the form ' + T('y = mx + c') + '. What are m and c?';
        it.worked = ['Take ' + T((an === 1 ? '' : an === -1 ? '-' : an) + 'x') + ' from both sides: ' + T(bq + 'y = ' + polyLin(-an, kk)) + '.', 'Divide every term by ' + T(String(bq)) + ': ' + T(eqTex(m, c)) + '.'];
      }
      it.key = 's3:' + it.stem;
      it.needsFractions = !isInt(m) || !isInt(c);
      it.line = { m: m, c: c };
      var ex3 = [];
      if (m[0] !== 0) ex3.push({ vals: [neg(m), null], why: WHY.sign(m) });
      if (c[0] !== 0) ex3.push({ vals: [null, neg(c)], why: WHY.csign });
      it.steps.push(mcStep(m, c, ex3));
      it.worked.push('Now ' + T('m = ' + ftex(m)) + ' and ' + T('c = ' + ftex(c)) + '.');
      it.worked.push('So ' + T(eqTex(m, c)) + '.');
    } else if (stage === 4) {
      m = gradient(rng, negative, fractions, 5, 0.45);
      q = m[1];
      c = F(int(rng, -9, 9));
      do { x1 = int(rng, -4, 4) * q; dx = int(rng, 1, 3) * q; y1 = mul(m, F(x1)); y1 = add(y1, c); y2 = add(mul(m, F(x1 + dx)), c); } while (Math.abs(y1[0]) > 15 || Math.abs(y2[0]) > 15 || x1 + dx > 12);
      y1 = y1[0]; y2 = y2[0]; x2 = x1 + dx;
      var P = [[x1, y1], [x2, y2]];
      it.key = 's4:' + x1 + ',' + y1 + ',' + x2 + ',' + y2;
      it.stem = 'A line passes through ' + T(pt(x1, y1)) + ' and ' + T(pt(x2, y2)) + '. Find its equation.';
      it.line = { m: m, c: c };
      it.needsFractions = !isInt(m);
      var np = neatPoint(P);
      it.steps.push(oneStep('m', 'm', m, [{ vals: [neg(m)], why: WHY.sign(m) }, { vals: [div(F(1), m)], why: WHY.run }], 'Step 1: the gradient m', 'The gradient is rise over run: the change in y divided by the change in x.'));
      it.steps.push(oneStep('c', 'c', c, P.map(function (p) { return { vals: [add(F(p[1]), mul(m, F(p[0])))], why: WHY.sub }; }), 'Step 2: the intercept c', 'Put one of the points into y = mx + c and solve for c. Either point gives the same c.'));
      it.steps.push(mcStep(m, c, eqSlips(m, c, P), 'Step 3: the equation, y = mx + c'));
      it.worked = ['Gradient = rise over run = ' + T('\\frac{' + (y2 - y1) + '}{' + dx + '} = ' + ftex(m)) + '.', subLine(m, np, c) + ' (Either point gives the same c.)', 'So ' + T(eqTex(m, c)) + '.'];
    } else if (stage === 5) {
      m = gradient(rng, negative, fractions, 6, 0.45);
      q = m[1];
      c = F(int(rng, -9, 9));
      var atY = idx % 10 === 9;             // a few given points are the y-intercept itself (at most 1 in 10)
      do { x1 = atY ? 0 : int(rng, 1, 5) * q * (rng() < 0.5 ? -1 : 1); y1 = add(mul(m, F(x1)), c); } while (Math.abs(y1[0]) > 15);
      y1 = y1[0];
      it.key = 's5:' + m.join('/') + ',' + x1 + ',' + y1;
      it.stem = 'A line has gradient ' + T(ftex(m)) + ' and passes through ' + T(pt(x1, y1)) + '. Find its equation.';
      it.line = { m: m, c: c };
      it.needsFractions = !isInt(m);
      it.steps.push(oneStep('c', 'c', c, [{ vals: [add(F(y1), mul(m, F(x1)))], why: WHY.sub }], 'Step 1: the intercept c', 'Put the point into y = mx + c, with the gradient you were given, and solve for c.'));
      it.steps.push(mcStep(m, c, eqSlips(m, c, [[x1, y1]]), 'Step 2: the equation, y = mx + c'));
      it.worked = ['The gradient is given: ' + T('m = ' + ftex(m)) + '.', subLine(m, [x1, y1], c), 'So ' + T(eqTex(m, c)) + '.'];
    } else {
      var perp = sub === 'perp', mo, mAns;
      if (perp) {
        // the answer's gradient is negative (or not) as asked; the given line has the negative reciprocal
        mAns = fractions ? gradient(rng, negative, true, 4, 0.7) : F(negative ? -1 : 1);
        mo = neg(div(F(1), mAns));
      } else { mo = gradient(rng, negative, fractions, 6, 0.4); mAns = mo; }
      q = mAns[1];
      var co = F(int(rng, -8, 8));
      c = F(int(rng, -9, 9));
      do { x1 = int(rng, -4, 4) * q; y1 = add(mul(mAns, F(x1)), c); } while (Math.abs(y1[0]) > 15);
      y1 = y1[0];
      m = mAns;
      it.key = 's6:' + sub + ':' + mo.join('/') + ',' + co.join('/') + ',' + x1 + ',' + y1;
      it.stem = 'The line ' + T(eqTex(mo, co)) + ' is given. Find the equation of the line ' + (perp ? 'perpendicular' : 'parallel') + ' to it that passes through ' + T(pt(x1, y1)) + '.';
      it.line = { m: m, c: c };
      it.needsFractions = !isInt(m) || !isInt(mo);
      var g6 = [{ vals: [neg(m)], why: WHY.sign(m) }];
      if (perp) {
        g6.push({ vals: [div(F(1), mo)], why: WHY.notneg });
        g6.push({ vals: [neg(mo)], why: WHY.notrec });
        g6.push({ vals: [mo], why: WHY.same });
      }
      it.steps.push(oneStep('m', 'm', m, g6, 'Step 1: the gradient m', perp ? 'Perpendicular lines have gradients that multiply to -1: the negative reciprocal.' : 'Parallel lines have the same gradient.'));
      it.steps.push(oneStep('c', 'c', c, [{ vals: [add(F(y1), mul(m, F(x1)))], why: WHY.sub }], 'Step 2: the intercept c', 'Put the point into y = mx + c, with your new gradient, and solve for c.'));
      it.steps.push(mcStep(m, c, eqSlips(m, c, [[x1, y1]]), 'Step 3: the equation, y = mx + c'));
      it.worked = [perp ? 'The given gradient is ' + T(ftex(mo)) + '. Perpendicular: flip it and change the sign, ' + T('m = ' + ftex(m)) + '.' : 'Parallel lines have the same gradient: ' + T('m = ' + ftex(m)) + '.',
        subLine(m, [x1, y1], c), 'So ' + T(eqTex(m, c)) + '.'];
    }
    it.negative = it.line.m[0] < 0;
    return it;
  }
  function polyLin(a, k) { return (a === 1 ? '' : a === -1 ? '-' : a) + 'x ' + (k < 0 ? '- ' : '+ ') + Math.abs(k); }

  /* ---------- the banks ---------- */
  var SIZE = 48, cache = {};
  function bank(stage, fractions) {
    fractions = !!fractions;
    var ck = stage + (fractions ? 'f' : 'i');
    if (cache[ck]) return cache[ck];
    var rng = makeRng(20261027 + stage * 6151 + (fractions ? 977 : 0)), subs = SUBS[stage], out = [], seen = {}, tries = 0;
    while (out.length < SIZE && tries++ < 40000) {
      var i = out.length, negative = (i % 5) < 3;
      var s = subs[i % subs.length];
      if (stage === 1 && s === 'zerom') negative = false;
      var q = gen(stage, s, rng, negative, fractions, i);
      if (!q || seen[q.key]) continue;
      seen[q.key] = true;
      out.push(q);
    }
    cache[ck] = out;
    return out;
  }
  function session(stage, seed, fractions, count) {
    count = count || 6;
    var rng = makeRng(seed), subs = SUBS[stage].filter(function (x, k, a) { return a.indexOf(x) === k; }), by = {}, out = [];
    var all = bank(stage, fractions);
    subs.forEach(function (s) { by[s] = shuffle(rng, all.filter(function (q) { return q.sub === s; })); });
    var order = shuffle(rng, subs);
    for (var i = 0; out.length < count && i < 400; i++) {
      var s = order[i % order.length];
      if (by[s].length) out.push(by[s].shift());
    }
    return out;
  }

  root.MaffsYSoSteep = { STAGES: STAGES, bank: bank, session: session, mark: mark, eqTex: eqTex, fstr: fstr, makeRng: makeRng };
})(typeof window !== 'undefined' ? window : globalThis);
