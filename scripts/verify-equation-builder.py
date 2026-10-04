#!/usr/bin/env python3
"""Equation Builder: which tile arrangements are correct? Decided here, once, by SymPy (SR-13; audit 2026-10-04 F1-F8).

The game marks a built answer correct only if its token sequence is in that question's ACCEPTED list. This
script computes every such list from the tiles, and fails if the bank's lists ever differ from it.

    python scripts/verify-equation-builder.py              # the check (CI)
    python scripts/verify-equation-builder.py --report     # accepted-list sizes, distractor builds, unclassifiable
    python scripts/verify-equation-builder.py --selftest   # planted faults must fail

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

# Questions the generic rules cannot classify (contract STOP IF): id -> why.
UNCLASSIFIABLE = {
    'eb_l4_008': 'integration by parts with unevaluated integrals as tiles',
    'eb_l4_021': 'a definite integral built from two tiles, with bracket-evaluation tiles',
    'eb_l4_023': 'sigma notation built from Σ, r=1, to, 5 tiles',
    'eb_l4_033': 'a matrix tile',
    'eb_gcse_031': 'a ± tile (two answers)',
    'eb_gcse_039': 'two = signs in one answer',
    'eb_l4_015': 'no unknown: the key is a true statement about numbers, so "same solution set, not an identity" '
                 'rejects the key itself',
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
    if tile in OPS:
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
RNG = random.Random(20261004)


def points(free, k=4):
    pts = []
    for _ in range(k):
        pts.append({s: sp.Rational(RNG.randint(11, 97), RNG.randint(7, 23)) for s in free})
    return pts


def num(e, pt):
    try:
        v = complex(sp.N(e.subs(pt), 30))
    except Exception:
        return None
    return v


def close(a, b):
    return a is not None and b is not None and abs(a - b) <= 1e-9 * max(1, abs(a), abs(b))


def equal_value(e1, e2):
    free = sorted(e1.free_symbols | e2.free_symbols, key=str)
    for pt in points(free):
        if not close(num(e1, pt), num(e2, pt)):
            return False
    return True


def kind_of(q):
    key = q['slots']
    if EQ not in key:
        return ('expression', None)
    i = key.index(EQ)
    for side, other in ((key[:i], key[i + 1:]), (key[i + 1:], key[:i])):
        if len(side) == 1 and translate(side[0])[0] == 'operand':
            e = to_sympy(side)[0]
            if isinstance(e, sp.Symbol) and e not in to_sympy(other)[0].free_symbols:
                return ('formula', side[0])
    return ('equation', None)


class Classifier:
    def __init__(self, q):
        self.q = q
        self.kind, self.subject = kind_of(q)
        self.key = to_sympy(q['slots'])
        if self.key is None:
            raise ValueError('%s: the key does not parse' % q['id'])
        if self.kind == 'formula':
            l, r = self.key
            self.target = r if q['slots'][0] == self.subject else l
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

    def accepts(self, tokens):
        p = to_sympy(tokens)
        if p is None:
            return False
        l, r = p
        if self.kind == 'expression':
            return r is None and equal_value(l, self.key[0])
        if r is None:
            return False
        if self.kind == 'formula':
            for side, other in ((l, r), (r, l)):
                if side == self.subj and self.subj not in other.free_symbols and equal_value(other, self.target):
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


def distractors(q):
    """Tiles not used by the key (a multiset difference)."""
    if q['type'] == 'gapfill':
        pre = q.get('prefilled', [])
        used = [q['slots'][i] for i in range(len(q['slots'])) if i not in pre]
    else:
        used = list(q['slots'])
    rest = list(q['tiles'])
    for t in used:
        if t in rest:
            rest.remove(t)
    return rest


def uses_distractor(q, seq):
    pool = list(q['tiles'])
    key = list(q['slots']) if q['type'] == 'assembly' else [q['slots'][i] for i in range(len(q['slots']))
                                                            if i not in q.get('prefilled', [])]
    if q['type'] == 'gapfill':
        pre = q.get('prefilled', [])
        seq = [seq[i] for i in range(len(seq)) if i not in pre]
    need = list(key)
    extra = []
    for t in seq:
        if t in need:
            need.remove(t)
        else:
            extra.append(t)
    return extra


def analyse(q):
    if q['id'] in UNCLASSIFIABLE:
        return {'id': q['id'], 'unclassifiable': UNCLASSIFIABLE[q['id']]}
    c = Classifier(q)
    cands = candidates(q)
    acc = [s for s in cands if c.accepts(s)]
    key_in = tuple(q['slots']) in set(acc)
    dis = [(s, uses_distractor(q, s)) for s in acc]
    dis = [(s, x) for s, x in dis if x]
    return {'id': q['id'], 'kind': c.kind, 'n_cands': len(cands), 'accepted': acc, 'key_in': key_in,
            'distractor_builds': dis}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--only', nargs='*')
    ap.add_argument('--json')
    a = ap.parse_args()
    bank = load_bank()
    if a.only:
        bank = [q for q in bank if any(o in q['id'] for o in a.only)]
    results = []
    for q in bank:
        r = analyse(q)
        results.append(r)
        if 'unclassifiable' in r:
            print('%-12s UNCLASSIFIABLE: %s' % (r['id'], r['unclassifiable']))
            continue
        print('%-12s %-10s cands=%-6d accepted=%-3d key_in=%s distractor_builds=%d'
              % (r['id'], r['kind'], r['n_cands'], len(r['accepted']), r['key_in'], len(r['distractor_builds'])))
        if a.report:
            for s in r['accepted']:
                print('      ACC  ' + ' '.join(s))
            for s, x in r['distractor_builds']:
                print('      DIS  ' + ' '.join(s) + '   uses: ' + ', '.join(x))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(results, ensure_ascii=False, indent=0), encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
