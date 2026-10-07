#!/usr/bin/env python3
"""Equation Builder: which tile arrangements are correct? Decided here, once, by SymPy (SR-13; audit 2026-10-04 F1-F8).

The game marks a built answer correct only if its token sequence is in that question's ACCEPTED list. This
script computes every such list from the tiles, and fails if the bank's lists ever differ from it.

    python scripts/verify-equation-builder.py              # the check (CI)
    python scripts/verify-equation-builder.py --report     # accepted-list sizes, distractor builds, unclassifiable
    python scripts/verify-equation-builder.py --selftest   # planted faults must fail
    python scripts/verify-equation-builder.py --part 1/2   # CI job D1 (D2: --part 2/2)
    python scripts/verify-equation-builder.py --part-selftest

PARTS (7 Oct 2026, canon §7.8.1). One job took 5m23s on main, and one question (eb_ks3_012, 31,032 candidate
arrangements) is 60% of it, so CI splits by candidate, not by question: part i of n classifies candidate k of
every question when k mod n = i - 1 (the candidates in their own sorted order), and checks that slice against
the page's ACCEPTED list cut to the same candidates. A check that is about a question as a whole (the key is
among the candidates; no accepted arrangement; the page's stored arrangements that are not candidates at all;
a valid tile not among the tiles; eb_gcse_013's geometry; ids the bank does not have) runs in part 1 only.
So the parts together fail on exactly what the whole run failed on; --part-selftest proves they cover every
candidate of every question once, and that the workflow runs every part.

How (contract, 4 Oct 2026):
  a. every well-formed arrangement of the tiles, any length from the shortest that parses up to the slot count,
     each tile used at most once (unused tiles allowed); gap-fill: every placement of tiles into the empty slots;
  b. classified by the key's kind:
     - formula (the key has one side that is a single subject tile, e.g. "C = ..."): that tile alone on one side
       (either side), the other side equal in value to the key's for all inputs;
     - equation (any other key with "="): the same solution set as the key's equation over the reals, and not
       an identity (accepted when the two differences are a non-zero constant multiple, or, in one unknown,
       when their real solution sets are equal);
     - expression (no "="): equal in value;
  c. the per-question exceptions (sums, constants of integration) are in SPECIAL below;
  d. an accepted arrangement may not use a distractor tile.
Each tile is translated on its own into an explicit SymPy fragment (TILE_FRAGMENT / translate), so two tiles
side by side never multiply implicitly: "3" then "m" is not "3m".
"""
import argparse, itertools, json, pathlib, random, re, sys
from fractions import Fraction

import sympy as sp
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, rationalize,
                                        implicit_multiplication_application, convert_xor)

BASE = pathlib.Path(__file__).resolve().parent.parent
PAGE = BASE / "games" / "equation-builder" / "index.html"

OPS = {'+': '+', '−': '-', '×': '*', '÷': '/'}
EQ = '='
TR_TILE = standard_transformations + (implicit_multiplication_application, convert_xor, rationalize)
TR_PLAIN = standard_transformations + (rationalize,)

NAMES = ['DYDX', 'D2Y', 'DETA1', 'DETA', 'ABSZ', 'SINF', 'OM', 'OP', 'IQR', 'Q1', 'Q3', 'Days', 'coeff',
         'PNEITHER', 'HINV', 'AINV', 'ZSTAR', 'U2', 'X1', 'T4', 'P0', 'lam', 'th', 'A1']
LOCAL = {n: sp.Symbol(n) for n in NAMES}
for n in ('E', 'I', 'S', 'N', 'O', 'Q', 'C', 'beta'):
    LOCAL[n] = sp.Symbol(n)
LOCAL.update({'lcm': sp.lcm, 'gcd': sp.gcd, 'sqrt': sp.sqrt, 'ln': sp.log, 'log': sp.log, 'sin': sp.sin,
              'cos': sp.cos, 'tan': sp.tan, 'exp': sp.exp, 'pi': sp.pi, 'J': sp.I, 'factorial': sp.factorial,
              'binomial': sp.binomial})

SUP = {'⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6',
       '⁷': '7', '⁸': '8', '⁹': '9', 'ⁿ': 'n', 'ˣ': 'x'}
SUPS = ''.join(SUP)
NAMED = [('d²y/dx²', 'D2Y'), ('dy/dx', 'DYDX'), ('det(A₁)', 'DETA1'), ('det(A)', 'DETA'),
         ('|z|', 'ABSZ'), ('S∞', 'SINF'), ('P(neither)', 'PNEITHER'), ('h⁻¹(x)', 'HINV'),
         ('A⁻¹', 'AINV'), ('z*', 'ZSTAR'), ('u₂', 'U2'), ('x₁', 'X1'), ('T₄', 'T4'),
         ('P₀', 'P0'), ('A₁A', 'A1*A'), ('λ', 'lam'), ('θ', 'th'), ('cos C', 'cos(C)'),
         ('cosC', 'cos(C)'), ('4C2', 'binomial(4,2)')]

# Tiles that are not whole expressions: the explicit fragment each one contributes.
TILE_FRAGMENT = {
    '2(2w': '2*(2*w', '(2w': '(2*w', '(6×17': '(6*17', '(T': '(T', '(x²cos(x)': '(x**2*cos(x)',
    '15)': '15)', '2(3w': '2*(3*w', '2(3x+4': '2*(3*x+4', '2)': '2)', '2xsin(x))': '2*x*sin(x))', '3)': '3)',
    '315)': '315)', '4²)': '4**2)', '60)': '60)', '6x(x': '6*x*(x', '7)': '7)', '9)': '9)',
    'HCF(420,': 'gcd(420,', 'LCM(420,': 'lcm(420,', 'a)': 'a)', 'b)': 'b)', 'jsinnθ)': 'J*sin(n*th))',
    'log(8×4': 'log(8*4', 'log(a': 'log(a', 'rⁿ(cosnθ': 'r**n*(cos(n*th)', 'w(w': 'w*(w',
    'x−1)': 'x-1)', '√(3²': 'sqrt(3**2', '√(9': 'sqrt(9', '7)': '7)',
}
# Fragments after which an operand is expected (they end inside an argument list).
EXPECT_AFTER = {'HCF(420,', 'LCM(420,'}

# Tiles that stand for an object SymPy must not evaluate: fixed symbols.
OPAQUE = {'∫x·eˣdx': 'INT_XEX', '∫eˣdx': 'INT_EX'}
for _n in OPAQUE.values():
    LOCAL[_n] = sp.Symbol(_n)

# Per-question rules the generic ones cannot decide (Jon's rulings, 4 Oct 2026 21:04). Each has a one-line reason.
#   fixed: the accepted list is exactly these variants of the key ('key', 'swap', 'r0' = sigma from r = 0)
#   kind:  override the key's kind (and subject tile for a formula)
#   pm_c:  a constant of integration may be + c or - c
SPECIAL = {
    'eb_l4_008': {'kind': ('equation', None),
                  'why': 'integration by parts: the integral tiles are fixed symbols, so the same step in any '
                         'arrangement is accepted and evaluating the second integral is not'},
    'eb_l4_021': {'fixed': ('key', 'swap'),
                  'why': 'a definite integral built from two tiles: the key and swapped sides only'},
    'eb_l4_023': {'fixed': ('key', 'r0'),
                  'why': 'sigma notation: from r = 1 or r = 0 (the r = 0 term of r squared is 0, same sum)'},
    'eb_l4_033': {'fixed': ('key',), 'why': 'a matrix gap-fill: one operator slot, only the key is right'},
    'eb_gcse_031': {'fixed': ('key',), 'why': 'a plus-or-minus gap-fill: one operator slot, only the key is right'},
    'eb_gcse_039': {'fixed': ('key',), 'why': 'two = signs in one answer: only the key tile gives the right root'},
    'eb_l4_015': {'kind': ('formula', 'log(16)'),
                  'why': 'no unknown: a formula for log(16): one side exactly that tile, the other equal in value'},
    'eb_l4_002': {'pm_c': True, 'why': 'constant of integration: + c and - c are both right'},
    'eb_l4_026': {'pm_c': True, 'why': 'constant of integration: + c and - c are both right'},
    'eb_l4_034': {'pm_c': True, 'why': 'constant of integration: + c and - c are both right'},
}


def ascii_math(t):
    s = t
    for a, b in NAMED:
        s = s.replace(a, b)
    s = (s.replace('−', '-').replace('×', '*').replace('÷', '/').replace('·', '*')
          .replace('π', '(pi)').replace('½', '(1/2)').replace('¾', '(3/4)')
          .replace('¼', '(1/4)').replace('⅓', '(1/3)'))
    s = re.sub('e([%s]+)' % SUPS, lambda m: 'exp(' + ''.join(SUP[c] for c in m.group(1)) + ')', s)
    s = re.sub('([%s]+)' % SUPS, lambda m: '**' + ''.join(SUP[c] for c in m.group(1)), s)
    s = re.sub(r'(sin|cos|tan)(\d+)°', r'\1(\2*pi/180)', s)
    s = re.sub(r'(sin|cos|tan)(\d+)(?![\d(])', r'\1(\2)', s)
    s = re.sub(r'(sin|cos|tan)n\*?th', r'\1(n*th)', s)
    s = re.sub(r'√\(', 'sqrt(', s)
    s = re.sub(r'√(\d+)', r'sqrt(\1)', s)
    s = re.sub(r'(\d+)!', r'factorial(\1)', s)
    s = re.sub(r'(?<=[\w)])(sin|cos|tan|exp|sqrt|log|ln)\(', r'*\1(', s)
    return s


_cache = {}


def translate(tile):
    """('op', '+') | ('eq',) | ('operand', frag) | ('open', frag, expects_operand) | ('close', frag) |
    ('lead', frag)  [a tile that starts with a binary operator, e.g. '÷6'] | ('special', tile)."""
    if tile in _cache:
        return _cache[tile]
    if tile in OPAQUE:
        r = ('operand', '(Symbol(%r))' % OPAQUE[tile])
    elif tile in OPS:
        r = ('op', OPS[tile])
    elif tile == EQ:
        r = ('eq',)
    elif tile in TILE_FRAGMENT:
        f = TILE_FRAGMENT[tile]
        depth = f.count('(') - f.count(')')
        r = ('open', f, tile in EXPECT_AFTER) if depth > 0 else ('close', f)
    elif tile[:1] in '+÷×' and len(tile) > 1:
        e = parse_expr(ascii_math(tile[1:]), local_dict=LOCAL, transformations=TR_TILE)
        r = ('lead', OPS.get(tile[0], '+') + '(' + str(e) + ')')
    else:
        try:
            e = parse_expr(ascii_math(tile), local_dict=LOCAL, transformations=TR_TILE)
            r = ('operand', '(' + sp.srepr(e) + ')')
        except Exception:
            r = ('special', tile)
    _cache[tile] = r
    return r


# ------------------------------------------------------------------ bank
def load_bank(page=PAGE):
    s = page.read_text(encoding='utf-8')
    a = s.index('const QUESTIONS=['); b = s.index('];', a)
    body = s[a + len('const QUESTIONS='):b + 1]
    body = re.sub(r'//[^\n]*', '', body)
    out, i = [], 0
    while i < len(body):                       # single-quoted JS strings -> JSON strings
        c = body[i]
        if c == "'":
            j = i + 1; buf = ''
            while body[j] != "'":
                if body[j] == '\\':
                    buf += "'" if body[j + 1] == "'" else body[j:j + 2]; j += 2
                else:
                    buf += '\\"' if body[j] == '"' else body[j]; j += 1
            out.append('"' + buf + '"'); i = j + 1
        else:
            out.append(c); i += 1
    js = ''.join(out)
    js = re.sub(r'([{,])\s*([A-Za-z_]\w*)\s*:', r'\1"\2":', js)
    js = re.sub(r',\s*([\]}])', r'\1', js)
    return json.loads(js)


# ------------------------------------------------------------------ enumeration
def arrangements(tiles, max_len):
    """Every distinct well-formed-looking token sequence (grammar prune; the parse decides)."""
    n = len(tiles)
    seen, out = set(), []
    tr = [translate(t) for t in tiles]

    def dfs(used, seq, state, depth, eq):
        # state: 'expect' (an operand is due) or 'after' (an operand just ended)
        if state == 'after' and depth == 0 and seq:
            key = tuple(tiles[i] for i in seq)
            if key not in seen:
                seen.add(key); out.append(key)
        if len(seq) == max_len:
            return
        for i in range(n):
            if used >> i & 1:
                continue
            k = tr[i]
            if i > 0 and tiles[i] == tiles[i - 1] and not (used >> (i - 1) & 1):
                continue                      # identical tiles: take them in order only
            kind = k[0]
            if state == 'expect':
                if kind == 'operand':
                    ns, nd = 'after', depth
                elif kind == 'open':
                    ns, nd = ('expect' if k[2] else 'after'), depth + 1
                elif kind == 'close':
                    if depth == 0: continue
                    ns, nd = 'after', depth - 1
                elif kind == 'op' and k[1] == '-' and (not seq or tr[seq[-1]][0] != 'op'):
                    ns, nd = 'expect', depth
                else:
                    continue
                neq = eq
            else:
                if kind == 'op':
                    ns, nd, neq = 'expect', depth, eq
                elif kind == 'eq':
                    if eq or depth: continue
                    ns, nd, neq = 'expect', depth, True
                elif kind == 'lead':
                    ns, nd, neq = 'after', depth, eq
                elif kind == 'close' and depth > 0 and k[1][:1] in ')':
                    ns, nd, neq = 'after', depth - 1, eq
                else:
                    continue
            dfs(used | 1 << i, seq + [i], ns, nd, neq)

    order = sorted(range(n), key=lambda i: tiles[i])
    tiles = [tiles[i] for i in order]
    tr = [translate(t) for t in tiles]
    dfs(0, [], 'expect', 0, False)
    return out


def to_sympy(tokens):
    """Token sequence -> (lhs, rhs) or (expr, None); None if it does not parse."""
    parts, cur = [], []
    for t in tokens:
        if t == EQ:
            parts.append(cur); cur = []
        else:
            cur.append(t)
    parts.append(cur)
    res = []
    for p in parts:
        frag = ''
        for t in p:
            k = translate(t)
            frag += ' %s ' % k[1] if k[0] == 'op' else k[1]
        try:
            e = parse_expr(frag, local_dict=LOCAL, transformations=TR_PLAIN)
        except Exception:
            return None
        if not isinstance(e, sp.Expr):
            return None
        res.append(e)
    return (res[0], res[1]) if len(res) == 2 else (res[0], None)


# ------------------------------------------------------------------ classification
RNG_SEED = 20261004


def points(free, k=4, seed=0):
    rng = random.Random(RNG_SEED + seed)
    # Between 1 and 10, positive, never a whole number: no pole such as x = 2, no complex principal values,
    # and no exponential so large that two different equations look like constant multiples.
    def one():
        while True:
            n = rng.randint(1010, 9990)
            if n % 1009:
                return sp.Rational(n, 1009)
    return [{s: one() for s in free} for _ in range(k)]


def num(e, pt):
    try:
        return complex(sp.N(e.subs(pt), 30))
    except Exception:
        return None


def close(a, b):
    return a is not None and b is not None and abs(a - b) <= 1e-9 * max(1, abs(a), abs(b))


def equal_value(e1, e2):
    free = sorted(e1.free_symbols | e2.free_symbols, key=str)
    return all(close(num(e1, pt), num(e2, pt)) for pt in points(free))


def split_eq(tokens):
    if EQ not in tokens:
        return list(tokens), None
    i = list(tokens).index(EQ)
    return list(tokens[:i]), list(tokens[i + 1:])


def kind_of(q):
    if 'kind' in SPECIAL.get(q['id'], {}):
        return SPECIAL[q['id']]['kind']
    key = q['slots']
    if EQ not in key:
        return ('expression', None)
    l, r = split_eq(key)
    for side, other in ((l, r), (r, l)):
        if len(side) == 1 and translate(side[0])[0] == 'operand':
            e = to_sympy(side)[0]
            if isinstance(e, sp.Symbol) and e not in to_sympy(other)[0].free_symbols:
                return ('formula', side[0])
    return ('equation', None)


class Classifier:
    def __init__(self, q):
        self.q = q
        self.kind, self.subject = kind_of(q)
        self.pm_c = SPECIAL.get(q['id'], {}).get('pm_c', False)
        self.key = to_sympy(q['slots'])
        if self.key is None:
            raise ValueError('%s: the key does not parse' % q['id'])
        if self.kind == 'formula':
            kl, kr = split_eq(q['slots'])
            self.target = to_sympy(kr if kl == [self.subject] else kl)[0]
            self.subj = to_sympy([self.subject])[0]
        elif self.kind == 'equation':
            l, r = self.key
            self.fk = l - r
            free = self.fk.free_symbols
            self.var = next(iter(free)) if len(free) == 1 else None
            self.roots = None
            if self.var is not None:
                try:
                    self.roots = sp.solveset(self.fk, self.var, sp.S.Reals)
                except Exception:
                    self.roots = None

    def same(self, e, target):
        if equal_value(e, target):
            return True
        c = sp.Symbol('c')
        return self.pm_c and equal_value(e, target.subs(c, -c))

    def accepts(self, tokens):
        p = to_sympy(tokens)
        if p is None:
            return False
        l, r = p
        if self.kind == 'expression':
            return r is None and self.same(l, self.key[0])
        if r is None:
            return False
        if self.kind == 'formula':
            tl, tr = split_eq(tokens)
            for side, other, oe in ((tl, tr, r), (tr, tl, l)):
                if side == [self.subject] and self.subject not in other and \
                        self.subj not in oe.free_symbols and self.same(oe, self.target):
                    return True
            return False
        f = l - r
        free = sorted(f.free_symbols | self.fk.free_symbols, key=str)
        pts = points(free)
        fv = [num(f, pt) for pt in pts]
        if all(v is not None and abs(v) < 1e-12 for v in fv):
            return False                         # an identity
        kv = [num(self.fk, pt) for pt in pts]
        if all(v is not None for v in fv + kv) and all(abs(v) > 1e-15 for v in kv):
            ratios = [a / b for a, b in zip(fv, kv)]
            if all(close(x, ratios[0]) for x in ratios) and abs(ratios[0]) > 1e-12:
                return True
        if self.var is not None and self.roots is not None and f.free_symbols == {self.var}:
            try:
                return sp.solveset(f, self.var, sp.S.Reals) == self.roots
            except Exception:
                return False
        return False


def candidates(q):
    if q['type'] == 'gapfill':
        pre = q.get('prefilled', [])
        empty = [i for i in range(len(q['slots'])) if i not in pre]
        out = set()
        for perm in itertools.permutations(range(len(q['tiles'])), len(empty)):
            seq = list(q['slots'])
            for slot, ti in zip(empty, perm):
                seq[slot] = q['tiles'][ti]
            out.add(tuple(seq))
        return sorted(out)
    return arrangements(list(q['tiles']), len(q['slots']))


def fixed_variants(q, which):
    key = tuple(q['slots'])
    out = []
    for w in which:
        if w == 'key':
            out.append(key)
        elif w == 'swap':
            l, r = split_eq(key)
            out.append(tuple(r + [EQ] + l))
        elif w == 'r0':
            out.append(tuple('r=0' if t == 'r=1' else t for t in key))
    return out


def extra_tiles(q, seq):
    """Tiles an arrangement uses beyond the key's (a multiset difference)."""
    pre = q.get('prefilled', []) if q['type'] == 'gapfill' else []
    need = [q['slots'][i] for i in range(len(q['slots'])) if i not in pre]
    used = [seq[i] for i in range(len(seq)) if i not in pre]
    extra = []
    for t in used:
        if t in need:
            need.remove(t)
        else:
            extra.append(t)
    return extra


def accepted_for(q, part=None):
    """(sorted accepted arrangements, candidate count). With part (i, n): only the candidates in that
    part's slice are classified, and the accepted ones among them come back."""
    sp_rule = SPECIAL.get(q['id'], {})
    if 'fixed' in sp_rule:
        fixed = sorted(fixed_variants(q, sp_rule['fixed']))
        return (fixed if part is None or part[0] == 1 else []), None
    c = Classifier(q)
    cands = in_part(candidates(q), part)
    return sorted(s for s in cands if c.accepts(s)), len(cands)


def in_part(cands, part):
    """The candidates part (i, n) classifies: every n-th, from the (i-1)-th. part None: all of them."""
    if part is None:
        return list(cands)
    i, n = part
    return [c for k, c in enumerate(cands) if k % n == i - 1]


def parse_part(text):
    m = re.match(r'^(\d+)/(\d+)$', text or '')
    if not m or not 1 <= int(m.group(1)) <= int(m.group(2)):
        raise ValueError('--part wants i/n with 1 <= i <= n, got %r' % text)
    return int(m.group(1)), int(m.group(2))


def tile_kind(t):
    k = translate(t)[0]
    if k == 'open':
        return 'openx' if translate(t)[2] else 'open'
    return 'operand' if k == 'special' else k


# ------------------------------------------------------------------ the page's generated block
BEGIN = '/* ACCEPTED-BEGIN: generated by scripts/verify-equation-builder.py --write. Do not edit by hand. */'
END = '/* ACCEPTED-END */'


def render_block(bank, accepted):
    acc = {qid: [list(s) for s in lists] for qid, lists in accepted.items()}
    kinds = {t: tile_kind(t) for q in bank for t in q['tiles'] + q['slots']}
    full = sorted(q['id'] for q in bank if q['type'] == 'gapfill' or 'fixed' in SPECIAL.get(q['id'], {}))
    return '\n'.join([BEGIN,
                      'const ACCEPTED=' + json.dumps(acc, ensure_ascii=False, separators=(',', ':')) + ';',
                      'const TILE_KINDS=' + json.dumps(kinds, ensure_ascii=False, separators=(',', ':')) + ';',
                      'const FULL_SLOTS=' + json.dumps(full, separators=(',', ':')) + ';',
                      END])


def page_block(src):
    a, b = src.find(BEGIN), src.find(END)
    return None if a < 0 or b < 0 else src[a:b + len(END)]


def page_accepted(src):
    blk = page_block(src)
    if blk is None:
        return None
    m = re.search(r'const ACCEPTED=(\{.*?\});\n', blk, re.S)
    return {k: sorted(tuple(x) for x in v) for k, v in json.loads(m.group(1)).items()}


# ------------------------------------------------------------------ the check
def gcse_013_geometry(q):
    """Jon's rewording: M is the midpoint of AB. With O at the origin, A = a, B = a + c, so OM = a + c/2."""
    a, c = sp.symbols('a c')
    om = (a + (a + c)) / 2
    return 'midpoint of AB' in q['text'] and sp.simplify(to_sympy(q['slots'][2:])[0].subs(
        {sp.Symbol('a'): a, sp.Symbol('c'): c}) - om) == 0


def check(page=PAGE, only=None, verbose=False, part=None):
    """part (i, n): see PARTS in the docstring. part None is the whole check, as before."""
    fails, report = [], []
    whole = part is None or part[0] == 1          # the question-as-a-whole checks run here
    src = page.read_text(encoding='utf-8')
    bank = load_bank(page)
    stored = page_accepted(src)
    if stored is None:
        return ['%s: no generated ACCEPTED block' % page.name], report, {}
    computed = {}
    for q in bank:
        if only and q['id'] not in only:
            continue
        acc, n = accepted_for(q, part)
        computed[q['id']] = acc
        valid = q.get('valid', [])
        dis = [(s, [t for t in extra_tiles(q, s) if t not in valid]) for s in acc]
        dis = [(s, x) for s, x in dis if x]
        report.append((q['id'], n, len(acc), SPECIAL.get(q['id'], {}).get('why')))
        mine = set(stored.get(q['id'], []))
        key = tuple(q['slots'])
        if part is not None and 'fixed' not in SPECIAL.get(q['id'], {}):
            cands = candidates(q)
            slice_ = set(in_part(cands, part))
            mine &= slice_
            if whole:
                every = set(cands)
                stray = set(stored.get(q['id'], [])) - every
                if not stored.get(q['id']):
                    fails.append('%s: no accepted arrangement' % q['id'])
                if key not in every:
                    fails.append('%s: the key %r cannot be built from its tiles or is not accepted' % (q['id'], ' '.join(key)))
                if stray:
                    fails.append('%s: the page\'s ACCEPTED list differs from the computed one (missing 0, extra %d): %s'
                                 % (q['id'], len(stray), ' | '.join(' '.join(x) for x in list(stray)[:3])))
            if key in slice_ and key not in set(acc):
                fails.append('%s: the key %r cannot be built from its tiles or is not accepted' % (q['id'], ' '.join(key)))
        elif whole:
            if not acc:
                fails.append('%s: no accepted arrangement' % q['id'])
            if key not in set(acc):
                fails.append('%s: the key %r cannot be built from its tiles or is not accepted' % (q['id'], ' '.join(key)))
        for s, x in dis:
            fails.append('%s: accepted %r uses distractor tile(s) %s' % (q['id'], ' '.join(s), x))
        if whole:
            for t in valid:
                if t not in q['tiles']:
                    fails.append('%s: valid tile %r is not one of its tiles' % (q['id'], t))
        differs = (stored.get(q['id']) != acc) if part is None else (mine != set(acc))
        if (part is None or 'fixed' not in SPECIAL.get(q['id'], {}) or whole) and differs:
            miss = set(acc) - mine
            more = mine - set(acc)
            fails.append('%s: the page\'s ACCEPTED list differs from the computed one (missing %d, extra %d)%s'
                         % (q['id'], len(miss), len(more), (': ' + ' | '.join(' '.join(x) for x in list(miss | more)[:3]))))
        if whole and q['id'] == 'eb_gcse_013' and not gcse_013_geometry(q):
            fails.append('eb_gcse_013: the key is not the midpoint the question names')
        if verbose:
            for s in acc:
                print('      ACC  ' + ' '.join(s))
    if not only and whole:
        extra_ids = set(stored) - set(computed)
        if extra_ids:
            fails.append('ACCEPTED block has ids not in the bank: %s' % sorted(extra_ids))
    return fails, report, computed


def write(page=PAGE):
    bank = load_bank(page)
    accepted = {q['id']: accepted_for(q)[0] for q in bank}
    src = page.read_text(encoding='utf-8')
    blk = render_block(bank, accepted)
    old = page_block(src)
    if old is None:
        anchor = '/* ===== QUESTION BANK v2 ===== */'
        src = src.replace(anchor, blk + '\n' + anchor, 1)
    else:
        src = src.replace(old, blk)
    page.write_text(src, encoding='utf-8', newline='')
    return accepted


# ------------------------------------------------------------------ self-test
def selftest():
    import shutil, tempfile
    cases = [
        ('clean copy passes', None, ['eb_ks3_001', 'eb_gcse_010'], False),
        ('a wrong key (ks3_001 keyed C = 2.50m + 3m)',
         lambda s: s.replace("slots:['C','=','2.50m','+','3']", "slots:['C','=','2.50m','+','3m']", 1), ['eb_ks3_001'], True),
        ('a missing accepted arrangement (ks3_001 loses C = 3 + 2.50m)',
         lambda s: s.replace('["C","=","3","+","2.50m"],', '', 1) if '["C","=","3","+","2.50m"],' in s
                    else s.replace(',["C","=","3","+","2.50m"]', '', 1), ['eb_ks3_001'], True),
        ('a distractor that builds an equal value (gcse_010 gets 5/9 and 4/10 back)',
         lambda s: s.replace("'5/10','\\u00f7','3/9'", "'5/9','\\u00f7','4/10'", 1)
                    .replace("'\\u2212','5/10'", "'\\u2212','5/9'"), ['eb_gcse_010'], True),
    ]
    bad = []
    for name, plant, only, should_fail in cases:
        d = pathlib.Path(tempfile.mkdtemp(prefix='eb-'))
        try:
            page = d / 'index.html'
            src = PAGE.read_text(encoding='utf-8')
            if plant:
                new = plant(src)
                if new == src:
                    bad.append(name + ' (the plant changed nothing)'); continue
                src = new
            page.write_text(src, encoding='utf-8')
            fails, _, _ = check(page, only=set(only))
            # the two CI parts together must fail exactly when the whole run does
            parted = [f for i in (1, 2) for f in check(page, only=set(only), part=(i, 2))[0]]
        finally:
            shutil.rmtree(d, ignore_errors=True)
        ok = bool(fails) == should_fail and bool(parted) == should_fail
        print('  %s  %-66s %s%s' % ('PASS' if ok else 'FAIL', name, fails[0][:110] if fails else '(no failures)',
                                   '' if bool(parted) == bool(fails) else '  [the parts disagree]'))
        if not ok:
            bad.append(name)
    print('selftest: %s' % ('FAILED: ' + ', '.join(bad) if bad else 'PASS'))
    return 1 if bad else 0


WORKFLOW = BASE / ".github" / "workflows" / "check-site.yml"


def part_selftest(n=2):
    """Every candidate of every question is in exactly one of the n parts; the workflow runs every part."""
    bad = []
    for q in load_bank():
        if 'fixed' in SPECIAL.get(q['id'], {}):
            continue
        cands = candidates(q)
        parts = [in_part(cands, (i, n)) for i in range(1, n + 1)]
        flat = [c for p_ in parts for c in p_]
        if sorted(flat) != sorted(cands):
            bad.append('%s: the parts are not its candidate list' % q['id'])
    # planted: drop one candidate, double one; each must be noticed by the comparison above
    cands = candidates(load_bank()[0])
    if sorted(cands[1:]) == sorted(cands) or sorted(cands + cands[:1]) == sorted(cands):
        bad.append('self-test: a dropped or doubled candidate was not noticed')
    runs = re.findall(r'python scripts/verify-equation-builder\.py\b([^\n|&]*)', WORKFLOW.read_text(encoding='utf-8'))
    got = sorted(m.group(1) for m in (re.search(r'--part (\d+/\d+)', r) for r in runs) if m)
    want = sorted('%d/%d' % (i, n) for i in range(1, n + 1))
    if got != want:
        bad.append('the workflow runs parts %s, not %s' % (got, want))
    if [r for r in runs if '--part' not in r and '--selftest' not in r]:
        bad.append('the workflow also runs the unsplit check')
    for b in bad:
        print('FAIL', b)
    print('part self-test (%d parts, workflow %s): %s' % (n, ', '.join(got) or 'none', 'FAILED' if bad else 'PASS'))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--write', action='store_true', help='compute every ACCEPTED list and write the page block')
    ap.add_argument('--report', action='store_true', help='print every accepted arrangement')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--only', nargs='*')
    ap.add_argument('--part', help='i/n: classify only part i of n of every question\'s candidates (CI runs 1/2 and 2/2)')
    ap.add_argument('--part-selftest', action='store_true', help='prove the parts cover every candidate once')
    a = ap.parse_args()
    if a.part_selftest:
        return part_selftest()
    if a.selftest:
        return selftest()
    try:
        part = parse_part(a.part) if a.part else None
    except ValueError as exc:
        ap.error(str(exc))
    if a.write:
        acc = write()
        print('wrote ACCEPTED for %d questions (%d arrangements)' % (len(acc), sum(len(v) for v in acc.values())))
    only = None
    if a.only:
        only = {q['id'] for q in load_bank() if any(o in q['id'] for o in a.only)}
    fails, report, _ = check(only=only, verbose=a.report, part=part)
    for qid, n, k, why in report:
        print('%-12s accepted=%-3d of %s arrangements%s' % (qid, k, n if n is not None else 'fixed',
                                                           ('  [special: %s]' % why) if why else ''))
    for f in fails:
        print('FAIL', f)
    print('equation-builder accepted lists%s: %s (%d questions)' % (' (part %d/%d)' % part if part else '',
                                                                 'FAIL' if fails else 'PASS', len(report)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
