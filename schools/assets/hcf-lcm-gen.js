/* HCF and LCM: the question bank (contract SIX-PS-BANKS batch 9, Jon, 21 Nov 2026; bank-first, canon 8.2.1).

   Pure data, no DOM. The 6 P's bank is generated from this file by scripts/gen-six-ps.py (topic hcf-lcm), and a future
   game loads this same file: the bank is its output, never a copy. The module computes every HCF and LCM itself;
   gen-six-ps.py recomputes each answer from the numbers in the stem with Python's math.gcd and math.lcm, and each named
   slip by its own rule (scripts/six_ps_rules.py, hcf_slips), separate code paths from this one.

     MaffsHcfLcm.STAGES          five stages, easiest first: { n, name, ask, band, size }
     MaffsHcfLcm.makeRng(seed)   mulberry32, as hc-factor-gen.js
     MaffsHcfLcm.bank(stage)     the stage's 12 questions, fixed seed, the same every load
                                 (bank(stage, seed) for another seed)

   Every candidate is enumerated first, then the seeded generator shuffles and picks: no draw is repeated until it fits.
     1 HCF of two numbers      a, b from 6 to 60, a ≠ b, HCF at least 2; at most 4 items where one divides the other
     2 LCM of two numbers      a, b from 2 to 15, a ≠ b, LCM at most 120; at least half with HCF above 1
     3 From prime factors      a and b over 2, 3, 5, 7 in index form (powers 0 to 3, each at most 500, at least two primes),
                               sharing a prime at different powers and each with a prime the other lacks; 6 HCF then 6 LCM
     4 HCF in context          packs of counters, rows of plants, boxes of pens: x, y from 12 to 90, HCF at least 3
     5 LCM in context          buses, flashing lights, bells: a, b from 4 to 30, LCM at most 120

   A question: { stage, index, key, ask: 'hcf' | 'lcm', nums: [a, b] (stage 3: the exponents too, as pf), stem, unit,
                 answer: { value }, slips: [{ kind, answer: { value }, line }], worked: [lines], band }.
   Maths is between \( and \); words never are.
*/
(function (root) {
  'use strict';

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
  function shuffle(rng, a) {
    a = a.slice();
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(rng() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function gcd(a, b) { while (b) { var t = a % b; a = b; b = t; } return a; }
  function lcm(a, b) { return a / gcd(a, b) * b; }
  function factors(n) { var out = []; for (var i = 1; i <= n; i++) if (n % i === 0) out.push(i); return out; }
  function multiplesTo(n, upTo) { var out = []; for (var m = n; m <= upTo; m += n) out.push(m); return out; }
  function tex(s) { return '\\(' + s + '\\)'; }
  function list(a) { return tex(a.join(', ')); }
  function divides(a, b) { return b % a === 0 || a % b === 0; }

  var STAGES = [
    { n: 1, name: 'HCF of two numbers', ask: 'hcf', band: 2, size: 12 },
    { n: 2, name: 'LCM of two numbers', ask: 'lcm', band: 2, size: 12 },
    { n: 3, name: 'From prime factors', ask: 'both', band: 4, size: 12 },
    { n: 4, name: 'HCF in context', ask: 'hcf', band: 3, size: 12 },
    { n: 5, name: 'LCM in context', ask: 'lcm', band: 3, size: 12 }
  ];
  var SEED = 20261121;

  /* ---------- the working ---------- */
  function hcfWorking(a, b, h) {
    return ['Factors of ' + a + ': ' + list(factors(a)) + '.',
            'Factors of ' + b + ': ' + list(factors(b)) + '.',
            'The highest number in both lists is ' + tex(String(h)) + '.'];
  }
  function lcmWorking(a, b, l) {
    var big = Math.max(a, b), small = Math.min(a, b);
    return ['Count up in ' + big + 's: ' + list(multiplesTo(big, l)) + '.',
            tex(l + ' \\div ' + small + ' = ' + (l / small)) + ', so ' + small + ' goes into ' + l + ': it is the first number in both times tables.',
            'The lowest common multiple is ' + tex(String(l)) + '.'];
  }

  /* ---------- the slips, each kept only if it differs from the answer and the slips before it ---------- */
  function keep(answer, slips) {
    var seen = [answer], out = [];
    slips.forEach(function (s) {
      if (s && seen.indexOf(s.answer.value) === -1) { seen.push(s.answer.value); out.push(s); }
    });
    return out;
  }
  function slip(kind, value, line) { return { kind: kind, answer: { value: value }, line: line }; }

  /* ---------- stage 1 ---------- */
  function stage1(rng) {
    var cands = [];
    for (var a = 6; a <= 60; a++) for (var b = a + 1; b <= 60; b++) if (gcd(a, b) >= 2) cands.push([a, b]);
    var out = [], div = 0;
    shuffle(rng, cands).forEach(function (p) {
      if (out.length >= 12) return;
      var d = divides(p[0], p[1]);
      if (d && div >= 4) return;
      if (d) div++;
      out.push(rng() < 0.5 ? p : [p[1], p[0]]);
    });
    return out.map(function (p) {
      var a = p[0], b = p[1], h = gcd(a, b), l = lcm(a, b);
      var smaller = factors(h).filter(function (f) { return f > 1 && f < h; }).pop();
      return {
        ask: 'hcf', nums: [a, b], key: 'hcf:' + Math.min(a, b) + ',' + Math.max(a, b),
        stem: 'Find the highest common factor (HCF) of ' + a + ' and ' + b + '.',
        answer: h,
        slips: [
          slip('lcm', l, "That's the lowest common multiple. The HCF is the biggest number that goes into both."),
          smaller ? slip('smaller_factor', smaller, "That goes into both, but it isn't the highest.") : null,
          slip('product', a * b, "That's the two numbers multiplied together. The HCF goes into both, so it can't be bigger than either.")
        ],
        worked: hcfWorking(a, b, h)
      };
    });
  }

  /* ---------- stage 2 ---------- */
  function stage2(rng) {
    var shared = [], coprime = [];
    for (var a = 2; a <= 15; a++) for (var b = a + 1; b <= 15; b++) {
      if (lcm(a, b) > 120) continue;
      (gcd(a, b) > 1 ? shared : coprime).push([a, b]);
    }
    var first = shuffle(rng, shared).slice(0, 6);
    var rest = shuffle(rng, shared.slice().filter(function (p) { return first.indexOf(p) === -1; }).concat(coprime)).slice(0, 6);
    return shuffle(rng, first.concat(rest)).map(function (p) {
      var x = rng() < 0.5 ? p : [p[1], p[0]], a = x[0], b = x[1], h = gcd(a, b), l = lcm(a, b);
      var big = Math.max(a, b), small = Math.min(a, b);
      return {
        ask: 'lcm', nums: [a, b], key: 'lcm:' + small + ',' + big,
        stem: 'Find the lowest common multiple (LCM) of ' + a + ' and ' + b + '.',
        answer: l,
        slips: [
          h > 1 ? slip('product', a * b, tex(a + ' \\times ' + b + ' = ' + (a * b)) + ' is a common multiple, but not the lowest.') : null,
          slip('hcf', h, "That's the highest common factor. The LCM is the smallest number that both go into."),
          divides(a, b) ? null : slip('one_number', big, "That's a multiple of " + big + ', but ' + small + " doesn't go into it.")
        ],
        worked: lcmWorking(a, b, l)
      };
    });
  }

  /* ---------- stage 3 ---------- */
  var PRIMES = [2, 3, 5, 7];
  function value(pf) { var v = 1; for (var i = 0; i < 4; i++) v *= Math.pow(PRIMES[i], pf[i]); return v; }
  function pfTex(pf) {
    var parts = [];
    for (var i = 0; i < 4; i++) if (pf[i]) parts.push(PRIMES[i] + (pf[i] > 1 ? '^' + pf[i] : ''));
    return parts.join(' \\times ');
  }
  function powTex(p, e) { return p + (e > 1 ? '^' + e : ''); }
  function stage3(rng) {
    var nums = [];
    for (var i = 0; i < 256; i++) {
      var pf = [i & 3, (i >> 2) & 3, (i >> 4) & 3, (i >> 6) & 3];
      if (pf.filter(Boolean).length >= 2 && value(pf) <= 500) nums.push(pf);
    }
    var pairs = [];
    for (var x = 0; x < nums.length; x++) for (var y = x + 1; y < nums.length; y++) {
      var A = nums[x], B = nums[y], sharedDiff = false, onlyOne = false;
      for (var k = 0; k < 4; k++) {
        if (A[k] && B[k] && A[k] !== B[k]) sharedDiff = true;
        if (!A[k] !== !B[k]) onlyOne = true;
      }
      if (sharedDiff && onlyOne && lcm(value(A), value(B)) <= 2000) pairs.push([A, B]);
    }
    return shuffle(rng, pairs).slice(0, 12).map(function (p, idx) {
      var A = rng() < 0.5 ? p[0] : p[1], B = A === p[0] ? p[1] : p[0];
      var a = value(A), b = value(B), h = gcd(a, b), l = lcm(a, b), ask = idx < 6 ? 'hcf' : 'lcm';
      var low = [], high = [], highShared = 1;
      for (var k = 0; k < 4; k++) {
        if (A[k] && B[k]) { low.push(powTex(PRIMES[k], Math.min(A[k], B[k]))); highShared *= Math.pow(PRIMES[k], Math.max(A[k], B[k])); }
        if (A[k] || B[k]) high.push(powTex(PRIMES[k], Math.max(A[k], B[k])));
      }
      var stem = tex('A = ' + pfTex(A)) + ' and ' + tex('B = ' + pfTex(B)) + '. Find the ' +
        (ask === 'hcf' ? 'highest common factor (HCF)' : 'lowest common multiple (LCM)') + ' of ' + tex('A') + ' and ' + tex('B') + '.';
      var worked = ask === 'hcf'
        ? ['The HCF takes each prime that is in both, at the lower of its two powers.',
           'The primes in both: ' + tex(low.join(', ')) + '. A prime in only one number is left out.',
           tex(low.join(' \\times ') + ' = ' + h) + '.']
        : ['The LCM takes every prime in either number, at the higher of its two powers.',
           'Every prime at its higher power: ' + tex(high.join(', ')) + '.',
           tex(high.join(' \\times ') + ' = ' + l) + '.'];
      return {
        ask: ask, nums: [a, b], pf: [A, B], key: ask + ':' + Math.min(a, b) + ',' + Math.max(a, b),
        stem: stem,
        answer: ask === 'hcf' ? h : l,
        slips: ask === 'hcf'
          ? [slip('lcm', l, "That's the LCM. The HCF takes the lower power of each prime the two numbers share."),
             slip('highest_powers', highShared, 'You took the higher power of each shared prime. The HCF takes the lower one.')]
          : [slip('hcf', h, "That's the HCF. The LCM takes the higher power of every prime in either number."),
             slip('product', a * b, 'That multiplies everything in both numbers together. The LCM takes each prime once, at its higher power.')],
        worked: worked
      };
    });
  }

  /* ---------- stage 4 ---------- */
  var HCF_CONTEXTS = [
    { things: ['red counters', 'blue counters'], group: 'packs', verb: 'put into identical packs', total: 'counters' },
    { things: ['tomato plants', 'pepper plants'], group: 'rows', verb: 'planted in identical rows', total: 'plants' },
    { things: ['black pens', 'blue pens'], group: 'boxes', verb: 'packed into identical boxes', total: 'pens' }
  ];
  function stage4(rng) {
    var cands = [];
    for (var x = 12; x <= 90; x++) for (var y = x + 1; y <= 90; y++) {
      if (gcd(x, y) >= 3 && x + y !== lcm(x, y)) cands.push([x, y]);
    }
    var picked = shuffle(rng, cands).slice(0, 12);
    return picked.map(function (p, idx) {
      var c = HCF_CONTEXTS[idx % 3], q = rng() < 0.5 ? p : [p[1], p[0]], x = q[0], y = q[1];
      var h = gcd(x, y), l = lcm(x, y);
      return {
        ask: 'hcf', nums: [x, y], key: 'hcf:' + Math.min(x, y) + ',' + Math.max(x, y), unit: c.group,
        stem: x + ' ' + c.things[0] + ' and ' + y + ' ' + c.things[1] + ' are ' + c.verb + ', with none left over. What is the greatest number of ' + c.group + '?',
        answer: h,
        slips: [
          slip('lcm', l, "That's the lowest common multiple. The number of " + c.group + ' has to go into both numbers exactly, so it is a common factor.'),
          slip('sum', x + y, "That's the total number of " + c.total + ', not the number of ' + c.group + '.')
        ],
        worked: ['The number of ' + c.group + ' must go into both ' + x + ' and ' + y + ' exactly: the greatest is the HCF.']
          .concat(hcfWorking(x, y, h).slice(0, 2), ['The greatest number of ' + c.group + ' is ' + tex(String(h)) + '.'])
      };
    });
  }

  /* ---------- stage 5 ---------- */
  var LCM_CONTEXTS = [
    { unit: 'minutes', stem: function (a, b) { return 'Two buses leave the station together. One leaves every ' + a + ' minutes, the other every ' + b + ' minutes. How many minutes until they next leave together?'; }, together: 'leave together' },
    { unit: 'seconds', stem: function (a, b) { return 'Two lights flash together. One flashes every ' + a + ' seconds, the other every ' + b + ' seconds. How many seconds until they next flash together?'; }, together: 'flash together' },
    { unit: 'minutes', stem: function (a, b) { return 'Two bells ring together. One rings every ' + a + ' minutes, the other every ' + b + ' minutes. How many minutes until they next ring together?'; }, together: 'ring together' }
  ];
  function stage5(rng) {
    var cands = [];
    for (var a = 4; a <= 30; a++) for (var b = a + 1; b <= 30; b++) if (lcm(a, b) <= 120) cands.push([a, b]);
    return shuffle(rng, cands).slice(0, 12).map(function (p, idx) {
      var c = LCM_CONTEXTS[idx % 3], q = rng() < 0.5 ? p : [p[1], p[0]], a = q[0], b = q[1];
      var h = gcd(a, b), l = lcm(a, b);
      return {
        ask: 'lcm', nums: [a, b], key: 'lcm:' + Math.min(a, b) + ',' + Math.max(a, b), unit: c.unit,
        stem: c.stem(a, b),
        answer: l,
        slips: [
          h > 1 ? slip('product', a * b, tex(a + ' \\times ' + b + ' = ' + (a * b)) + ' is a time they ' + c.together + ', but not the first.') : null,
          slip('hcf', h, "That's the highest common factor. They next " + c.together + ' after a time both numbers go into: a common multiple.'),
          slip('sum', a + b, 'Adding the two times does not give a time both numbers go into.')
        ],
        worked: ['They next ' + c.together + ' after the first time in both times tables: the LCM.']
          .concat(lcmWorking(a, b, l).slice(0, 2), ['They next ' + c.together + ' after ' + tex(String(l)) + ' ' + c.unit + '.'])
      };
    });
  }

  /* ---------- the banks ---------- */
  var BUILD = { 1: stage1, 2: stage2, 3: stage3, 4: stage4, 5: stage5 }, cache = {};
  function bank(stage, seed) {
    var useSeed = seed === undefined ? SEED + stage * 7919 : seed, ck = stage + ':' + useSeed;
    if (cache[ck]) return cache[ck];
    var st = STAGES[stage - 1];
    var out = BUILD[stage](makeRng(useSeed)).map(function (q, i) {
      return { stage: stage, index: i, key: q.key, ask: q.ask, nums: q.nums, pf: q.pf || null, stem: q.stem, unit: q.unit || null,
               answer: { value: q.answer }, slips: keep(q.answer, q.slips), worked: q.worked, band: st.band };
    });
    cache[ck] = out;
    return out;
  }

  root.MaffsHcfLcm = { STAGES: STAGES, makeRng: makeRng, bank: bank, gcd: gcd, lcm: lcm };
})(typeof window !== 'undefined' ? window : globalThis);
