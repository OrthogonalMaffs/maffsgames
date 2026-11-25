#!/usr/bin/env python3
# ci-shards: Sums in Disguise (the bank's SHA-256 against the contract's; all 226 items recomputed from little and the big sum's tens, every decoy by its rule, distinct, never the answer, never negative; Stage 4's decoys different facts in range; coverage of every pair, no repeated big sum, no ones sum in two of Stages 1, 3 and 4; the 67 counts; the lines against the contract, verbatim; the fragment never sent or stored; in both looks every tile, option and Stage 4 sum marked by dataset.val alone, every decoy's aha line then the learning line, the 67 after marking on exactly the firing items; the greeting for each fragment; Amendment 1: the question as maths, the stacked working, one LINES string in feedback, kid lines of 6 words or fewer, the hand, read aloud on local voices only against a mocked speechSynthesis; every item of every stage above the fold at 360x640 in both looks, speaker showing: every control at every step, then Next after every right-answer line and every decoy (fit_common's sweep, nothing sampled); every stage played in both looks at 360x640, one board submission on stage-N, no payload naming the look; fault-injection self-test) | | 1
# ci-deps: games/sums-in-disguise/ docs/handover/contracts/*sums-in-disguise.md docs/history/contracts/*sums-in-disguise.md
r"""Independent verification for Sums in Disguise (games/sums-in-disguise/), contract SUMS-IN-DISGUISE, 18 Nov 2026.
SR-30: checked from its first PR.

WHAT THIS DOES NOT TRUST
-------------------------------------------------------------------------------
The page holds a fixed bank of 226 items, made by the generator in the contract. This script never uses the page's
numbers to check the page's numbers:

  Bank      the page's items, written one a line as json.dumps(item, separators=(",", ":")) with a newline after
            each, have the SHA-256 the contract states. Counts 50/36/50 (25 ones, 25 tens)/40 (25 ones, 15 tens)/50,
            ids unique. Every item recomputed from little = [a, b] and t, the big sum's tens: little_answer = a + b; the
            answer is the big sum's total; ones (10t + a) + b with a + b <= 9; tens 10a + 10b with a + b <= 9; cross
            (10t + a) + b with a + b >= 10 and a total <= 99. Decoys by rule (tens p + 10q; concat the digits of p - a
            then of a + b, or on a cross item of t then of a + b; off_by_one the answer +-1, or +-10 where the fallback
            applied; forgot_disguise a + b; extra_zero 100(a + b); ones p + b; forgot_ten the answer - 10), the three
            distinct, never the answer, never negative. Stage 4: answer_sum is the little fact in its disguise; each
            decoy a different fact (not {a, b} either way round), in range, no crossing; the three options distinct.
            Coverage: Stage 1 and 2 every one of the 36 pairs, Stage 5 every one of the 45; no big sum twice in a stage;
            no ones big sum in two of Stages 1, 3 and 4. The 67 fires on 6/2/7/4/14 items.
  Source    the greeting is never written with innerHTML; location.hash is read once; no mfg() payload, storage write
            or board names the look, the fragment or the class name.
  Lines     the page's LINES equal the contract's placeholder lines, character for character, in both looks.
  Marking   in each look, every item in the page: the disguise on the big sum; for Stages 1, 2 and 5 taking it off
            shows the little sum, the tag (p - a, or "0 0" on a tens item) and the stage's reveal line, then tiles 0 to 10
            (0 to 20 in Stage 5), each marked by its dataset.val with every tile's text blanked first, right only for
            a + b, and the disguise back on with the big sum after any tile; Stage 3's Peek shows the little sum and the
            reveal line. Every option, with every option's text blanked first, is marked by its dataset.val: right only
            for the answer (Stage 4: answer_sum as "p+q"); a decoy shows its own aha line (Stage 4: the duck's), then the
            learning line built here from the item, in KaTeX; the 67 hidden before marking and shown after it exactly
            when a 6 and a 7 are among the big sum's numbers and the answer.
  Greeting  "#kids/Maple" and "#kids/Maple%20Class" -> "Welcome, Maple Class!"; "#KIDS" and "#kids" -> the kid look
            and its welcome; "#kids/<script>" -> the kid look, no class greeting, nothing injected; no hash or "#kidsx"
            -> the grown-up look; a bad ?level= rewritten by MaffsLevel keeps the fragment.
  Amendment 1 (Jon, 18 Nov 2026, 09:19): every question is the sum and "= ?" (Stage 4: LINES' find, with the little
            sum in KaTeX), no other words; the working stacked in KaTeX, its rows and highlighted tens recomputed here from
            the item and read from the rendered source; feedback never holds two LINES strings; every LINES.kids string 6
            words or fewer; the disguise and the button both take it off; the pointing hand on question 1 of a kid run only.
  Amendment 3 (tens on show; SUMS-IN-DISGUISE-ART, replacing its Amendment 2): for every Stage 1, 2 and 5 item in both
            looks, the blocks at every step, counted from the item: at the start t sticks and a cubes + b cubes (a sticks +
            b sticks on a tens item); after take-off (by the button and by the disguise) t sticks held by the disguise, its
            tag 10t ("0" on a tens item, no sticks leaving), the disguise in view beside the little sum; the ones on tiles;
            Stage 5 as BRIDGE replaced it (below); put-back (by the button and by the disguise): the regrouped
            blocks and question ("64 + 3 = 60 + 7 = ?", "40 + 20 = 6 tens = ?", "27 + 5 = 30 + 2 = ?"); no options before
            it; the working's rows and highlighted tens; the read-aloud for each step; the hand on each step's button on
            question 1 of a kid run.
  ONE-EQUALS (Jon, 18 Nov 2026, 11:34): every KaTeX string rendered in the play card, at every step of every item in
            both looks, has at most one "=" a line, a sum on its left and a single number or "?" on its right; the put-back
            question is the plain big sum; the working one "=" a line ("8 + ? = 10" allowed: "?" may be a term on the left).
  NO-LABELS (Jon, 18 Nov 2026, 12:21): for every Stage 1, 2 and 5 item in both looks, at every step from the start until
            the big answer is marked, the play screen's text outside the tag, the little-sum line and the answer controls
            (the 0 to 10 tiles, the options), and what the speaker would read, hold neither the answer nor the regrouped tens (10t, 10c on a tens item, 10(t + 1)
            in Stage 5) as a number; after put-back no group of blocks carries a label and nothing is written under the
            blocks; the put-back read-aloud is "Put it back on." alone.
  BRIDGE (Jon, 18 Nov 2026, the class's method): every Stage 5 item in both looks, bridge = 10 - a, rest = a + b - 10:
            after take-off the tag 10t, t sticks held, the a cubes in a ten outline (a full, bridge empty; a disabled button
            named by fill_ten) and b cubes beside it; "a + ? = 10" on tiles 0 to 10, keyed to bridge; then fill the ten,
            by the button and by the outline: t + 1 sticks held, the tag 10t + 10 only now, rest cubes, no outline, the
            reveal line, no options until put-back; the working "p + bridge = 10(t + 1)" and "10(t + 1) + rest = n" (one
            line when rest = 0); the read-aloud "a and how many make 10?", "Fill the ten.", the working in words; the hand
            on the tiles and on the fill button; every Stage 5 item above the fold at 360 px with the speaker (Fit, below).
  Read aloud against a mocked speechSynthesis: no speaker without speechSynthesis, with no voice or with only a voice
            that is not local; a speaker once a local voice arrives (voiceschanged); only that voice passed to speak();
            nothing spoken before a tap; the question, then the one feedback line and the working, in words from the
            item; never the greeting; cancel() on Next and on leaving the play screen; nothing in an mfg() payload or
            storage. (The fold with the speaker showing is Fit's.)
  Play      every stage in each look at 360 x 640 (the kid look from #kids/Maple): 10 different items of the stage, played
            to the end (the fold is Fit's, every item, not these 10); one game_completed with the score,
            one board submission [slug, 'stage-N', score, 10]; Stage 3's "Done without peeking"; the end line; no mfg()
            payload, localStorage or sessionStorage value containing "kids", "Maple" or "#".
  Fit       every item above the fold (PRIMARY-FIT-SWEEP, scripts/fit_common.py): all 226 in each look at 360 x 640
            with a local voice, so the speaker shows, the real fonts and the settled layout: each previewed by itself and
            walked step by step, every control measured at every step (take off, the tiles, fill the ten, put back, the
            options, Stage 3's peek), then Next after every feedback variant: each LINES.right line (SID.ui.answer's line
            argument), each decoy (SID.ui.pick), Stage 3 peeked and not, and the steps after a wrong tile; a 67 that shows
            is left showing. No sideways scroll. Nothing sampled: the same items and variants every run.

Work units: "bank" (no browser), "marking grown", "marking kids", "greeting", "read aloud", "play grown 360x640", "play kids 360x640",
"fit <look> stage-N" (one per look and stage) and "plant: <what>" (one per planted fault).

    python scripts/verify-sums-in-disguise.py              # every unit, then the self-test
    python scripts/verify-sums-in-disguise.py --selftest   # the planted faults only
"""
import argparse
import contextlib
import glob
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402
import plant_common as pc  # noqa: E402
import fit_common as fc  # noqa: E402

SLUG = 'sums-in-disguise'
GAME = os.path.join(ROOT, 'games', SLUG, 'index.html')
CONTRACT = 'sums-in-disguise.md'
SHA = '19e415561cb6baecdaf01d2bde6f23f367a6aff2802d33b8d152dce6561068a8'
# The start picture (contract SUMS-IN-DISGUISE-ART, 18 Nov 2026): Jon's, from branch art/sums-in-disguise, byte for byte.
PICTURE = os.path.join(ROOT, 'games', SLUG, 'assets', 'start.webp')
PICTURE_SHA = 'bfdd4ecd1d99f714387c8030e6dfc500ba1d0e18cbe1ebadc26a59fef4484645'
PICTURE_ALT = ('Five disguises hanging on coat hooks in a cloakroom: a fake moustache, round glasses, a wig, a rubber duck '
               'and a top hat, above an empty bench')
MODES = ['stage-1', 'stage-2', 'stage-3', 'stage-4', 'stage-5']
COUNTS = {1: 50, 2: 36, 3: 50, 4: 40, 5: 50}
TYPES = {3: {'ones': 25, 'tens': 25}, 4: {'ones': 25, 'tens': 15}}
FIRES = {1: 6, 2: 2, 3: 7, 4: 4, 5: 14}
PHONE = (360, 640)
PER = 10
ONES_PAIRS = [(a, b) for a in range(1, 9) for b in range(1, 10 - a)]
CROSS_PAIRS = [(a, b) for a in range(1, 10) for b in range(1, 10) if a + b >= 10]


# ---------------------------------------------------------------- the contract
def contract_file():
    for d in ('docs/handover/contracts', 'docs/history/contracts'):
        for f in glob.glob(os.path.join(ROOT, d, '*' + CONTRACT)):
            return f
    return None


def contract_lines():
    """The placeholder lines, parsed from the contract: {look: {key: str | [str] | {k: str}}}."""
    f = contract_file()
    if f is None:
        raise ValueError('no contract file *%s in docs/handover/contracts or docs/history/contracts' % CONTRACT)
    text = open(f, encoding='utf-8').read()
    q = r'"((?:[^"\\]|\\.)*)"'
    out = parse_lines(text.split('THE PLACEHOLDER LINES', 1)[1].split('\nShared, both looks', 1)[0], q)
    # Amendment 1: the kid set replaced, verbatim; take_off and find added to the grown set.
    if 'AMENDMENT 1' in text:
        amend = text.split('AMENDMENT 1', 1)[1]
        new = parse_lines(amend.split('THE NEW KID PLACEHOLDER SET', 1)[1].split('\nADD to the grown', 1)[0], q)
        out['kids'] = new['kids']
        add = re.search(r'^ADD to the grown: block: (.*)$', amend, re.M).group(1)
        out['grown'].update(dict(re.findall(r'([a-z_]+): ' + q, add)))
    # SUMS-IN-DISGUISE-ART's Amendment 1 (Jon, 18 Nov 2026, 10:38): LINES.kids.find, its "!" no longer after the sum.
    for d in ('docs/handover/contracts', 'docs/history/contracts'):
        for f in glob.glob(os.path.join(ROOT, d, '*sums-in-disguise-art.md')):
            for look, key, old, new in re.findall(r'LINES\.(kids|grown)\.([a-z_]+) ' + q + r' \u2192 ' + q, open(f, encoding='utf-8').read()):
                if out[look].get(key) == old:
                    out[look][key] = new
            # Amendment 2: lines it adds (kids.ten_in_hat "...", grown.ten_in_hat "...").
            amend2 = open(f, encoding='utf-8').read().split('AMENDMENT 2', 1)
            if len(amend2) == 2:
                for look, key, val in re.findall(r'(kids|grown)\.([a-z_]+) ' + q, amend2[1]):
                    out[look].setdefault(key, val)
            # Amendment 3: "add to kids: put_back "...", ten_in_hat "...". Add to grown: ..."
            amend3 = open(f, encoding='utf-8').read().split('AMENDMENT 3', 1)
            if len(amend3) == 2:
                for look, adds in re.findall(r'[Aa]dd to (kids|grown): (.*?)(?=\. Add to|\. Change no)', amend3[1]):
                    for key, val in re.findall(r'([a-z_]+) ' + q, adds):
                        out[look].setdefault(key, val)
    # SUMS-IN-DISGUISE-BRIDGE (Jon, 18 Nov 2026): fill_ten replaces ten_in_hat in both looks.
    for d in ('docs/handover/contracts', 'docs/history/contracts'):
        for f in glob.glob(os.path.join(ROOT, d, '*sums-in-disguise-bridge.md')):
            text = open(f, encoding='utf-8').read()
            for look, key, val in re.findall(r'(kids|grown)\.(fill_ten) ' + q, text):
                out[look][key] = val
            if 'Remove ten_in_hat from both LINES blocks' in text:
                for look in out:
                    out[look].pop('ten_in_hat', None)
    return out


def parse_lines(block, q):
    out, look = {}, None
    for ln in block.split('\n'):
        m = re.match(r'^(grown|kids):$', ln)
        if m:
            look = m.group(1)
            out[look] = {}
            continue
        m = re.match(r'^  ([a-z_]+): (.*)$', ln)
        if not m or look is None:
            continue
        key, rest = m.groups()
        if rest.startswith('{'):
            out[look][key] = {k: v for k, v in re.findall(r'([a-z_][a-z_0-9-]*): ' + q, rest)}
        elif rest.startswith('['):
            out[look][key] = re.findall(q, rest)
        else:
            out[look][key] = re.fullmatch(q, rest).group(1)
    return out


# ---------------------------------------------------------------- the bank, read from the page's source
def bank_of(html):
    m = re.search(r'var QUESTIONS = \[\n(.*?)\n  \];', html, re.S)
    if not m:
        raise ValueError('no QUESTIONS block in the page')
    items = []
    for ln in m.group(1).split('\n'):
        s = ln.strip()
        if s.startswith('{'):
            items.append(json.loads(s[:-1] if s.endswith(',') else s))
    return items


def big_of(q):
    return q['answer_sum'] if q['stage'] == 4 else q['big']


def has67(q):
    d = '%d%d%d' % (big_of(q)[0], big_of(q)[1], q['answer'])
    return '6' in d and '7' in d


def tag_of(q):
    return '0 0' if q['type'] == 'tens' else str(big_of(q)[0] - q['little'][0])


def hl_tens(n, typ):
    return ['0' for ch in str(n) if ch == '0'] if typ == 'tens' else [str(n)[:-1]]


def working(q):
    """The two rows of the stacked working, and its highlighted pieces, from the item alone. Stages 1, 2 and 5 (Amendment 3
    of SUMS-IN-DISGUISE-ART): the tens put back as the blocks show them; Stages 3 and 4 as Amendment 1 left them."""
    a, b = q['little']
    c, (p, r), n, typ = a + b, big_of(q), sum(big_of(q)), q['type']
    if q['stage'] in (1, 2, 5):
        t10, nt = p - a, str(n)[:-1]
        if typ == 'tens':
            return ['%d + %d = %d' % (a, b, c), '%d + %d = %d' % (p, r, n)], [str(p)[:-1], str(r)[:-1], nt]
        if typ == 'cross':
            # BRIDGE: p + bridge = 10(t + 1), then 10(t + 1) + rest = n; one line when rest = 0. Every number's tens lit.
            br, rest = 10 - a, c - 10
            nx = p + br
            if not rest:
                return ['%d + %d = %d' % (p, br, nx)], [str(p)[:-1], str(nx)[:-1]]
            return (['%d + %d = %d' % (p, br, nx), '%d + %d = %d' % (nx, rest, n)],
                    [str(p)[:-1], str(nx)[:-1], str(nx)[:-1], nt])
        return ['%d + %d = %d' % (a, b, c), '%d + %d = %d' % (t10, c, n)], [str(t10), nt]
    rows = ['%d + %d = %d' % (a, b, c), '%d + %d = %d' % (p, r, n)]
    hl = hl_tens(p, typ) + (hl_tens(r, typ) if typ == 'tens' else []) + hl_tens(n, typ)
    return rows, hl


HL = re.compile(r'\\htmlClass\{hl\}\{\\mathbf\{([^{}]*)\}\}')


def tex_rows(t):
    """The rows and highlighted pieces of the working's KaTeX source, as rendered."""
    hl = HL.findall(t or '')
    plain = HL.sub(lambda m: m.group(1), t or '')
    plain = re.sub(r'\\text\{([^{}]*)\}', lambda m: m.group(1), plain).replace('\\begin{aligned}', '').replace('\\end{aligned}', '').replace('&', '')
    return [re.sub(r'\s+', ' ', x).strip() for x in plain.split('\\\\')], hl


def spoken_working(q):
    a, b = q['little']
    c, (p, r), n = a + b, big_of(q), sum(big_of(q))
    if q['stage'] in (1, 2, 5):
        if q['type'] == 'tens':
            return '%d plus %d is %d. %d plus %d is %d.' % (a, b, c, p, r, n)
        if q['type'] == 'cross':
            nx = p + 10 - a
            return '%d plus %d is %d.' % (p, 10 - a, nx) + (' %d plus %d is %d.' % (nx, c - 10, n) if c > 10 else '')
        return '%d plus %d is %d. %d plus %d is %d.' % (a, b, c, p - a, c, n)
    return '%d plus %d is %d, so %d plus %d is %d' % (a, b, c, p, r, n)


def giveaways(q):
    """NO-LABELS: the numbers that must not be shown or spoken before the big answer is marked: the answer, and the
    regrouped tens (10t on a ones item, 10c on a tens item, 10(t + 1) on a Stage 5 crossing item)."""
    a, b = q['little']
    c, t10 = a + b, q['big'][0] - a
    tens = 10 * c if q['type'] == 'tens' else t10 + 10 if q['type'] == 'cross' else t10
    return {str(q['answer']), str(tens)}


PUT_BACK_READ = 'Put it back on.'


EQ_SUM = re.compile(r'^[0-9 ?]+(\+[0-9 ?]+)+$')   # BRIDGE: "8 + ? = 10", a "?" may stand for a term on the left


def one_equals(t):
    """The rule for a rendered KaTeX string: each line has at most one "=", a sum on its left and a single number or "?"
    on its right. Returns the offending line, or None."""
    plain = HL.sub(lambda m: m.group(1), t or '')
    plain = re.sub(r'\\text\{([^{}]*)\}', lambda m: m.group(1), plain)
    plain = plain.replace('\\begin{aligned}', '').replace('\\end{aligned}', '').replace('&', '').replace('{?}', '?')
    for line in plain.split('\\\\'):
        line = re.sub(r'\s+', ' ', line).strip()
        if line.count('=') > 1:
            return line
        if '=' in line:
            left, right = (x.strip() for x in line.split('='))
            if not EQ_SUM.match(left) or not re.fullmatch(r'\d+|\?', right):
                return line
    return None


def blocks_at(q, step):
    """The blocks, from the item: a list of (sticks, cubes) groups, and the sticks the disguise holds."""
    a, b = q['little']
    c, t = a + b, (q['big'][0] - a) // 10
    tens = q['type'] == 'tens'
    if step == 'start':
        return ([(a, 0), (b, 0)] if tens else [(t, a), (0, b)]), 0
    if step == 'little':
        if q['type'] == 'cross':
            return [(0, 0), (0, b)], t          # BRIDGE: the a cubes in the ten outline (no loose cubes), b beside it
        return ([(a, 0), (b, 0)] if tens else [(0, a), (0, b)]), (0 if tens else t)
    if step == 'filled':
        return ([(0, c - 10)] if c > 10 else []), t + 1
    if step == 'counted':
        return [(c, 0)] if tens else [(0, c)], (0 if tens else t)
    if step == 'back':
        return ([(c, 0)] if tens else [(t + 1, 0)] + ([(0, c - 10)] if c > 10 else []) if q['type'] == 'cross' else [(t, 0), (0, c)]), 0


def strings(d):
    """Every string in a LINES set, flattened."""
    if isinstance(d, str):
        return [d]
    if isinstance(d, dict):
        return [x for v in d.values() for x in strings(v)]
    return [x for v in d for x in strings(v)]


def words(t):
    return len(t.replace('{name}', '').replace('{little}', '').split())


def check_item(q, out):
    """Every number of one item, recomputed from little and the big sum's tens."""
    i, st, typ = q['id'], q['stage'], q['type']
    a, b = q['little']
    s = big_of(q)
    p, r = s
    want_type = {1: 'ones', 2: 'tens', 5: 'cross'}.get(st)
    if (want_type and typ != want_type) or typ not in ('ones', 'tens', 'cross'):
        out.append('%s: type %s in stage %d' % (i, typ, st))
        return
    if q['little_answer'] != a + b:
        out.append('%s: little_answer %s, recomputed %d' % (i, q['little_answer'], a + b))
    if q['answer'] != p + r:
        out.append('%s: answer %s, recomputed %d' % (i, q['answer'], p + r))
    t = (p - a) // 10
    if typ == 'tens':
        if (p, r) != (10 * a, 10 * b):
            out.append('%s: a tens item whose big sum %d + %d is not 10a + 10b' % (i, p, r))
        if a + b > 9:
            out.append('%s: a tens item crosses a hundred' % i)
    else:
        if p != 10 * t + a or r != b or t < 1 or not 1 <= a <= 9 or not 1 <= b <= 9:
            out.append('%s: big sum %d + %d is not (10t + a) + b for little %d + %d' % (i, p, r, a, b))
        if typ == 'ones' and a + b > 9:
            out.append('%s: a ones item crosses a ten' % i)
        if typ == 'cross' and a + b < 10:
            out.append('%s: a cross item does not cross a ten' % i)
        if typ == 'cross' and p + r > 99:
            out.append('%s: a cross item totals over 99' % i)
    ans = p + r
    if st == 4:
        opts = [tuple(s)] + [tuple(d['sum']) for d in q['decoys']]
        if len(q['decoys']) != 2 or len(set(opts)) != 3:
            out.append('%s: Stage 4 options are not three distinct sums' % i)
        for d in q['decoys']:
            dp, dr = d['sum']
            if typ == 'tens':
                ok = dp % 10 == 0 and dr % 10 == 0
                da, db = dp // 10, dr // 10
            else:
                ok = (dp - (dp % 10)) == 10 * t
                da, db = dp % 10, dr
            if not ok or not (1 <= da <= 9 and 1 <= db <= 9 and da + db <= 9):
                out.append('%s: Stage 4 decoy %d + %d is out of range or not the same disguise' % (i, dp, dr))
            if sorted([da, db]) == sorted([a, b]):
                out.append('%s: Stage 4 decoy %d + %d is the same fact as %d + %d' % (i, dp, dr, a, b))
        return
    d = q['decoys']
    rules = {'ones': {'tens': p + 10 * r, 'concat': int('%d%d' % (p - a, a + b)), 'off_by_one': None},
             'tens': {'forgot_disguise': a + b, 'extra_zero': 100 * (a + b), 'ones': p + b},
             'cross': {'forgot_ten': ans - 10, 'concat': int('%d%d' % (t, a + b)), 'off_by_one': None}}[typ]
    if sorted(d) != sorted(rules):
        out.append('%s: decoys %s, the rule names %s' % (i, sorted(d), sorted(rules)))
    for k, v in rules.items():
        if k not in d:
            continue
        if v is None:
            if d[k] not in (ans + 1, ans - 1, ans + 10, ans - 10):
                out.append('%s: off_by_one %s is not the answer +-1 (or +-10)' % (i, d[k]))
        elif d[k] != v:
            out.append('%s: decoy %s %s, recomputed %d' % (i, k, d[k], v))
    vals = list(d.values())
    if len(set(vals)) != len(vals):
        out.append('%s: two decoys are equal' % i)
    if ans in vals:
        out.append('%s: a decoy equals the answer' % i)
    if any(v < 0 for v in vals):
        out.append('%s: a negative decoy' % i)


def check_bank(html, out, info):
    items = bank_of(html)
    blob = ''.join(json.dumps(q, separators=(',', ':')) + '\n' for q in items).encode('utf-8')
    got = hashlib.sha256(blob).hexdigest()
    if got != SHA:
        out.append('the bank has SHA-256 %s, the contract states %s' % (got, SHA))
    ids = [q['id'] for q in items]
    if len(ids) != len(set(ids)):
        out.append('ids repeat')
    for st, n in COUNTS.items():
        s = [q for q in items if q['stage'] == st]
        if len(s) != n:
            out.append('stage %d has %d items, not %d' % (st, len(s), n))
        for typ, k in TYPES.get(st, {}).items():
            if sum(1 for q in s if q['type'] == typ) != k:
                out.append('stage %d has not %d %s items' % (st, k, typ))
        bigs = [tuple(big_of(q)) for q in s]
        if len(bigs) != len(set(bigs)):
            out.append('stage %d repeats a big sum' % st)
        fires = sum(1 for q in s if has67(q))
        if fires != FIRES[st]:
            out.append('stage %d: the 67 fires on %d items, not %d' % (st, fires, FIRES[st]))
    for st, pairs in ((1, ONES_PAIRS), (2, ONES_PAIRS), (5, CROSS_PAIRS)):
        have = {tuple(q['little']) for q in items if q['stage'] == st}
        if have != set(pairs):
            out.append('stage %d does not use every one of its %d pairs' % (st, len(pairs)))
    seen = {}
    for q in items:
        if q['type'] == 'ones' and q['stage'] in (1, 3, 4):
            seen.setdefault(tuple(big_of(q)), set()).add(q['stage'])
    for k, v in seen.items():
        if len(v) > 1:
            out.append('the ones big sum %d + %d is in stages %s' % (k[0], k[1], sorted(v)))
    for q in items:
        try:
            check_item(q, out)
        except (KeyError, TypeError, ValueError) as e:
            out.append('%s: unreadable item (%s)' % (q.get('id'), e))
    info['bank'] = len(items)


def webp_size(path):
    b = open(path, 'rb').read(64)
    if b[:4] != b'RIFF' or b[8:12] != b'WEBP':
        return None
    kind = b[12:16]
    if kind == b'VP8 ':
        return int.from_bytes(b[26:28], 'little') & 0x3fff, int.from_bytes(b[28:30], 'little') & 0x3fff
    if kind == b'VP8L':
        v = int.from_bytes(b[21:25], 'little')
        return (v & 0x3fff) + 1, ((v >> 14) & 0x3fff) + 1
    if kind == b'VP8X':
        return int.from_bytes(b[24:27], 'little') + 1, int.from_bytes(b[27:30], 'little') + 1
    return None


def check_picture(html, out):
    """The start picture: straight after the start screen's header, its src, size and alt in the tag; the file that size
    and that SHA-256 (contract SUMS-IN-DISGUISE-ART)."""
    img = re.search(r'<div id="menu" class="screen active">\s*<div class="header">.*?</div>\s*(<img class="start-art"[^>]*>)', html, re.S)
    if not img:
        out.append('start picture: no img.start-art straight after the start screen\'s header')
    else:
        tag = img.group(1)
        for attr in ('src="assets/start.webp"', 'width="1600"', 'height="873"', 'alt="%s"' % PICTURE_ALT):
            if attr not in tag:
                out.append('start picture: the tag has no %s' % attr)
    if not os.path.exists(PICTURE):
        out.append('start picture: assets/start.webp is missing')
        return
    size = webp_size(PICTURE)
    if size != (1600, 873):
        out.append('start picture: assets/start.webp is %s, not 1600 x 873' % (size,))
    got = hashlib.sha256(open(PICTURE, 'rb').read()).hexdigest()
    if got != PICTURE_SHA:
        out.append('start picture: assets/start.webp has SHA-256 %s, not %s' % (got, PICTURE_SHA))


def check_source(html, out):
    """The fragment, the look and the class name stay in the page."""
    js = '\n'.join(re.findall(r'<script>(.*?)</script>', html, re.S))
    # No line puts "!" or "?" straight after a sum: "Find {little}!" read as a factorial (Jon, 18 Nov 2026, 10:38).
    lines_src = re.search(r'var LINES = \{(.*?)\n  \};', js, re.S)
    for m in re.finditer(r'\{(little|big)\}[!?]', lines_src.group(1) if lines_src else ''):
        out.append('a LINES string puts %r straight after a sum' % m.group(0))
    if re.search(r'innerHTML\s*=[^;\n]*(greeting\(|CLASS_NAME|\bfrag\b|\bnm\b)', js):
        out.append('the greeting (the class name) is written with innerHTML')
    if js.count('location.hash') != 1:
        out.append('location.hash is read %d times, not once' % js.count('location.hash'))
    if 'sessionStorage' in js:
        out.append('the page uses sessionStorage')
    for m in re.finditer(r'\b(?:lsSet|localStorage\.setItem)\(([^;\n]*)', js):
        if re.search(r'LOOK|CLASS_NAME|\bfrag\b|\bnm\b|hash', m.group(1)):
            out.append('a storage write names the look or the fragment: %s' % m.group(0)[:80])
    for m in re.finditer(r'\bev\((\'[a-z_]+\'), \{([^}]*)\}', js):
        if re.search(r'LOOK|CLASS_NAME|\bfrag\b|\bnm\b|hash', m.group(2)):
            out.append('an mfg() payload names the look or the fragment: %s' % m.group(1))


# ---------------------------------------------------------------- the browser
def open_page(pw, base, html, size, frag='', query='?cb=verify'):
    br = pw.chromium.launch()
    touch = size[0] <= 600
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch)
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    # Record every mfg() call from the first one: analytics.js's own mfg is wrapped as it is defined.
    ctx.add_init_script("""(() => { window.__ev = []; let real = null;
      Object.defineProperty(window, 'mfg', { configurable: true,
        get() { return function (n, p) { window.__ev.push([n, JSON.parse(JSON.stringify(p || {}))]); }; },
        set(v) { real = v; } }); })();""")
    bc.offline(ctx, base)
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/%s%s' % (SLUG, query, frag), wait_until='load', timeout=30000)
    page.wait_for_function('!!window.SID && !!SID.ui', timeout=15000)
    page.emulate_media(reduced_motion='reduce')   # the split's hop is then at once: the marking checks run without waiting
    page.evaluate("""() => { window.__sub = [];
        window.MaffsLeaderboard = window.MaffsLeaderboard || {};
        MaffsLeaderboard.submitScore = (g, l, s, n) => { window.__sub.push([g, l, s, n]); return Promise.resolve(); }; }""")
    return br, page, errors


ITEM_JS = r"""([q]) => {
  const $ = (id) => document.getElementById(id);
  const out = { tiles: {}, opts: {} };
  const flow = q.stage === 3 ? 'wig' : q.stage === 4 ? 'duck' : 'unmask';
  const sumOf = () => $('sum').dataset.sum;
  const ann = (el) => { const a = el.querySelector('annotation'); return a ? a.textContent : null; };
  const words = (el) => { const c = el.cloneNode(true); c.querySelectorAll('.katex').forEach(k => k.remove()); return c.textContent; };
  const on = () => !$('suspect').classList.contains('unmasked');
  // Every KaTeX string rendered in the play card right now (ONE-EQUALS), with where it was seen.
  out.maths = [];
  // NO-LABELS: the play screen's text, outside the tag, the little-sum line and the answer controls (tiles, options), each KaTeX string read once
  // from its annotation and every text node apart (so "8" and "0" in two nodes never read as 80); and what the speaker reads.
  out.shown = [];
  const shown = () => {
    const c = $('game').cloneNode(true);
    c.querySelectorAll('#tag, #clue, #tiles, #opts, [hidden]').forEach(e => e.remove());
    c.querySelectorAll('.katex').forEach(k => { const a = k.querySelector('annotation'); k.replaceWith(document.createTextNode(' ' + (a ? a.textContent : '') + ' ')); });
    const w = document.createTreeWalker(c, NodeFilter.SHOW_TEXT), t = [];
    while (w.nextNode()) t.push(w.currentNode.nodeValue);
    return t.join(' ');
  };
  const maths = (where) => { document.querySelectorAll('#qcard annotation').forEach(a => out.maths.push([where, a.textContent]));
                             out.shown.push([where, SID.ui.state(), shown(), SID.ui.toRead()]); };
  const blocks = () => ({ groups: [...$('blocks').querySelectorAll('.grp')].map(g => [g.querySelectorAll('.stk').length, g.querySelectorAll('.cubes i').length]),
                          held: $('held').querySelectorAll('.stk').length,
                          frame: (f => f ? [f.querySelectorAll('.slot.full').length, f.querySelectorAll('.slot:not(.full)').length] : null)($('tenFrame')) });
  const key = () => SID.ui.littleKey();
  const opts = () => $('opts').children.length > 0 && !$('opts').hidden;
  const beside = () => { const d = $('disguise').getBoundingClientRect(), k = ($('sum').querySelector('.katex') || $('sum')).getBoundingClientRect();
    const cs = getComputedStyle($('disguise'));
    return { shown: d.width > 0 && d.height > 0 && cs.visibility !== 'hidden' && cs.opacity !== '0' && cs.display !== 'none',
             beside: d.left >= k.right - 2 && d.top < k.bottom && d.bottom > k.top }; };
  if (flow === 'wig') { SID.ui.preview(q.id); maths('the wig on'); SID.ui.peek(); maths('the peek'); }
  if (flow === 'unmask') {
    SID.ui.preview(q.id);
    maths('the start');
    out.mask = { state: SID.ui.state(), sum: sumOf(), on: on(), pop: !$('pop67').hidden, button: $('unmaskBtn').textContent,
                 aria: $('disguise').getAttribute('aria-label'), disabled: $('disguise').disabled, blocks: blocks(), opts: opts() };
    SID.ui.unmask('disguise');
    out.viaDisguise = SID.ui.state();
    SID.ui.preview(q.id);
    SID.ui.unmask('button');
    out.little = { state: SID.ui.state(), sum: sumOf(), on: on(), tag: $('tag').textContent, ask: ann($('sum')), prompt: $('prompt').textContent, key: key(),
                   frameBtn: (f => f ? { tag: f.tagName, aria: f.getAttribute('aria-label'), disabled: f.disabled } : null)($('tenFrame')),
                   tagShown: getComputedStyle($('tag')).display !== 'none', say: $('say').textContent, blocks: blocks(), park: beside(), opts: opts() };
    maths('after take-off');
    out.tileVals = [...$('tiles').querySelectorAll('.tile')].map(b => b.dataset.val);
    for (const v of out.tileVals) {
      window.__ev = [];
      SID.ui.preview(q.id); SID.ui.unmask();
      $('tiles').querySelectorAll('.tile').forEach(b => { b.textContent = '?'; });
      SID.ui.tile(v);
      out.tiles[v] = { little: $('clue').dataset.little || null, state: SID.ui.state(), sum: sumOf(), on: on(), opts: opts(),
                       answered: (window.__ev || []).filter(e => e[0] === 'question_answered').length };
    }
    // After the ones: counted (Stage 5: the ten waiting to be filled); Stage 5's fill by the button and by the outline;
    // put-back by the button and by the disguise.
    SID.ui.preview(q.id); SID.ui.unmask(); SID.ui.tile(key());
    out.counted = { state: SID.ui.state(), blocks: blocks(), note: ann($('blocksNote')), say: $('say').textContent, opts: opts(), tag: $('tag').textContent,
                    fill: $('fillBtn').textContent, fillShown: !$('fillRow').hidden, put: $('putBtn').textContent, putShown: !$('putRow').hidden,
                    frameOn: !!$('tenFrame') && !$('tenFrame').disabled, clue: ann($('clue')) };
    maths('the ones counted');
    if (q.stage === 5) {
      for (const via of ['button', 'outline']) {
        SID.ui.preview(q.id); SID.ui.unmask(); SID.ui.tile(key());
        SID.ui.fill(via);
        out['fill_' + via] = { state: SID.ui.state(), tag: $('tag').textContent, blocks: blocks(), note: ann($('blocksNote')), say: $('say').textContent,
                               opts: opts(), park: beside(), putShown: !$('putRow').hidden, aria: $('disguise').getAttribute('aria-label') };
        maths('the ten filled');
      }
    }
    for (const via of ['button', 'disguise']) {
      SID.ui.preview(q.id); SID.ui.unmask(); SID.ui.tile(key());
      if (q.stage === 5) SID.ui.fill();
      const before = { opts: opts(), state: SID.ui.state(), aria: $('disguise').getAttribute('aria-label') };
      SID.ui.putBack(via);
      out['back_' + via] = { before: before, state: SID.ui.state(), on: on(), blocks: blocks(), ask: ann($('sum')),
                             written: ($('blocks').textContent + ' ' + $('blocksNote').textContent).replace(/[+\s]/g, ''),
                             labelled: $('blocks').querySelectorAll('.glabel, .katex, [data-label]').length,
                             say: $('say').textContent, opts: opts() };
      maths('after put-back');
    }
  }
  if (flow === 'wig') {
    SID.ui.preview(q.id);
    out.wigOn = { state: SID.ui.state(), sum: sumOf(), on: on() };
    SID.ui.peek();
    out.peek = { sum: sumOf(), on: on(), say: $('say').textContent, tag: $('tag').textContent };
  }
  const toBig = () => { SID.ui.preview(q.id); if (flow === 'unmask') { SID.ui.unmask(); SID.ui.tile(key()); if (q.stage === 5) SID.ui.fill(); SID.ui.putBack(); } };
  toBig();
  maths('the big sum');
  out.big = { state: SID.ui.state(), sum: sumOf(), on: on(), ask: ann($('sum')), prompt: words($('prompt')), promptMath: ann($('prompt')),
              line: $('prompt').dataset.line || null };
  out.optVals = [...$('opts').querySelectorAll('.opt')].map(b => b.dataset.val);
  for (const v of out.optVals) {
    toBig();
    const popBefore = !$('pop67').hidden;
    $('opts').querySelectorAll('.opt').forEach(b => { b.innerHTML = '?'; });
    window.__ev = [];
    SID.ui.pick(v);
    const fb = document.querySelector('#feedback .fb'), ln = $('learn');
    const qa = window.__ev.filter(e => e[0] === 'question_answered');
    out.opts[v] = { popBefore: popBefore, why: fb ? fb.dataset.why : null, pick: fb ? (fb.dataset.pick || null) : null,
      say: $('say').textContent, learn: ln ? ln.dataset.learn : null, katex: !!(ln && ln.querySelector('.katex')),
      tex: ln ? ann(ln) : null, hlShown: ln ? ln.querySelectorAll('.hl').length : 0,
      shown: $('say').textContent + ' || ' + words($('feedback')) + ' || ' + words($('prompt')),
      pop: $('pop67').hidden ? null : $('pop67').textContent.trim(), score: SID.ui.score(),
      next: !!document.querySelector('#feedback .maffs-next, #nextBtn'),
      qa: qa.map(e => [e[1].correct, e[1].question_id]) };
    maths('after marking ' + v);
  }
  return out;
}"""


def check_marking(page, html, look, out, info):
    want = contract_lines()
    got = page.evaluate('SID.lines()')
    for lk in ('grown', 'kids'):
        if got.get(lk) != want.get(lk):
            keys = sorted(set(got.get(lk, {})) | set(want.get(lk, {})))
            bad = [k for k in keys if got.get(lk, {}).get(k) != want.get(lk, {}).get(k)]
            out.append('LINES.%s differs from the contract at %s' % (lk, bad))
    for k, v in got.get('kids', {}).items():
        for t in strings(v):
            if words(t) > 6:
                out.append('LINES.kids.%s has %d words (6 at most): %r' % (k, words(t), t))
    L = want[look]
    every = set(strings(L))
    tagl = look
    fired = {}
    for q in bank_of(html):
        r = page.evaluate(ITEM_JS, [q])
        i, st = q['id'], q['stage']
        a, b = q['little']
        big = '%d+%d' % tuple(big_of(q))
        little = '%d+%d' % (a, b)
        mode = 'stage-%d' % st
        if st in (1, 2, 5):
            c, t = a + b, (big_of(q)[0] - a) // 10
            tens = q['type'] == 'tens'
            m = r['mask']
            if m['state'] != 'mask' or m['sum'] != big or not m['on'] or m['pop']:
                out.append('%s %s: the big sum is not shown in its disguise first (%s)' % (tagl, i, m))
            if m['button'] != L['take_off'] or m['aria'] != L['take_off'] or m['disabled']:
                out.append('%s %s: the take-off button reads %r and the disguise %r (disabled %s)' % (tagl, i, m['button'], m['aria'], m['disabled']))
            want_b = blocks_at(q, 'start')
            if [tuple(g) for g in m['blocks']['groups']] != want_b[0] or m['blocks']['held'] != want_b[1]:
                out.append('%s %s: the blocks at the start are %s, expected %s' % (tagl, i, m['blocks'], want_b))
            if m['opts']:
                out.append('%s %s: options exist before put-back (at the start)' % (tagl, i))
            if r['viaDisguise'] != 'little':
                out.append('%s %s: tapping the disguise does not take it off' % (tagl, i))
            lt = r['little']
            bridge = st == 5
            br = 10 - a
            want_ask, want_sum, want_key = ('%d + {?} = 10' % a, '%d+?=10' % a, br) if bridge else ('%d + %d = {?}' % (a, b), little, c)
            if lt['ask'] != want_ask or lt['prompt'].strip():
                out.append('%s %s: the little sum is asked as %r with the words %r, expected %r' % (tagl, i, lt['ask'], lt['prompt'], want_ask))
            if lt['key'] != want_key:
                out.append('%s %s: the step-2 tile key is %s, expected %s' % (tagl, i, lt['key'], want_key))
            want_tag = '0' if tens else str(10 * t)
            if lt['state'] != 'little' or lt['sum'] != want_sum or lt['on'] or not lt['tagShown'] or lt['tag'] != want_tag:
                out.append('%s %s: taking the disguise off does not show %s with the tag %s (%s)' % (tagl, i, want_sum, want_tag, lt))
            want_b = blocks_at(q, 'little')
            if [tuple(g) for g in lt['blocks']['groups']] != want_b[0] or lt['blocks']['held'] != want_b[1]:
                out.append('%s %s: after take-off the blocks are %s, expected %s' % (tagl, i, lt['blocks'], want_b))
            # BRIDGE: the ten outline, a filled and 10 - a empty, a real button named by fill_ten (Stage 5 only).
            want_f = [a, br] if bridge else None
            if lt['blocks']['frame'] != want_f:
                out.append('%s %s: after take-off the ten outline is %s, expected %s' % (tagl, i, lt['blocks']['frame'], want_f))
            if bridge and (not lt['frameBtn'] or lt['frameBtn']['tag'] != 'BUTTON' or lt['frameBtn']['aria'] != L['fill_ten'] or not lt['frameBtn']['disabled']):
                out.append('%s %s: the ten outline is not a button named %r, off until step 3 (%s)' % (tagl, i, L['fill_ten'], lt['frameBtn']))
            if not lt['park']['shown'] or not lt['park']['beside']:
                out.append('%s %s: at take-off the disguise is not in view beside the sum (%s)' % (tagl, i, lt['park']))
            if lt['say'] != ('' if st == 5 else L['reveal'][mode]):
                out.append('%s %s: at take-off the line is %r' % (tagl, i, lt['say']))
            if lt['opts']:
                out.append('%s %s: options exist before put-back (after take-off)' % (tagl, i))
            n = 10
            if r['tileVals'] != [str(v) for v in range(n + 1)]:
                out.append('%s %s: tiles %s, not 0 to %d' % (tagl, i, r['tileVals'], n))
            next_state = 'fill' if bridge else 'putback'
            for v, tt in r['tiles'].items():
                ok = 'right' if int(v) == want_key else 'wrong'
                if tt['little'] != ok or tt['state'] != next_state or tt['sum'] != little or tt['on'] or tt['answered'] or tt['opts']:
                    out.append('%s %s: tile %s marked %s, expected %s, then %s (%s)' % (tagl, i, v, tt['little'], ok, next_state, tt))
            ct = r['counted']
            if bridge:
                # Step 3 waits: the a + bridge = 10 line, the blocks as at take-off, the tag still 10t, fill by button or outline.
                want_b = blocks_at(q, 'little')
                if [tuple(g) for g in ct['blocks']['groups']] != want_b[0] or ct['blocks']['frame'] != [a, br] or ct['note']:
                    out.append('%s %s: before the fill the blocks are %s (note %r), expected %s and the outline [%d, %d]' % (tagl, i, ct['blocks'], ct['note'], want_b, a, br))
                if ct['clue'] != '%d + %d = 10' % (a, br):
                    out.append('%s %s: after the tiles the line reads %r, not "%d + %d = 10"' % (tagl, i, ct['clue'], a, br))
                if ct['tag'] != str(10 * t):
                    out.append('%s %s: before the fill the tag reads %s, not %d' % (tagl, i, ct['tag'], 10 * t))
                if (ct['state'] != 'fill' or not ct['fillShown'] or ct['fill'] != L['fill_ten'] or not ct['frameOn'] or ct['putShown']
                        or ct['say'] or ct['opts']):
                    out.append('%s %s: the fill step is not offered by its button and the outline alone (%s)' % (tagl, i, ct))
                for via in ('button', 'outline'):
                    fl = r['fill_' + via]
                    want_b = blocks_at(q, 'filled')
                    if [tuple(g) for g in fl['blocks']['groups']] != want_b[0] or fl['blocks']['held'] != want_b[1] or fl['blocks']['frame'] is not None:
                        out.append('%s %s: after the fill (%s) the blocks are %s, expected %s and no outline' % (tagl, i, via, fl['blocks'], want_b))
                    if fl['tag'] != str(10 * t + 10):
                        out.append('%s %s: after the fill (%s) the tag reads %s, not %d' % (tagl, i, via, fl['tag'], 10 * t + 10))
                    if fl['note']:
                        out.append('%s %s: after the fill a value is written under the blocks (%r)' % (tagl, i, fl['note']))
                    if fl['say'] != L['reveal'][mode]:
                        out.append('%s %s: at the fill the line is %r, not the Stage 5 reveal' % (tagl, i, fl['say']))
                    if fl['state'] != 'putback' or fl['opts'] or not fl['putShown'] or not fl['park']['shown']:
                        out.append('%s %s: after the fill (%s) it does not wait for put-back with the hat in view (%s)' % (tagl, i, via, fl))
            elif [tuple(g) for g in ct['blocks']['groups']] != blocks_at(q, 'counted')[0] or ct['note'] != str(c):
                out.append('%s %s: the ones are not shown counted (%s, %r), expected %s and %d' % (tagl, i, ct['blocks'], ct['note'], blocks_at(q, 'counted')[0], c))
            if not bridge and (not ct['putShown'] or ct['put'] != L['put_back'] or ct['fillShown'] or ct['state'] != 'putback'):
                out.append('%s %s: after the ones, put-back is not offered alone (%s)' % (tagl, i, ct))
            want_b = blocks_at(q, 'back')
            for via in ('button', 'disguise'):
                bk = r['back_' + via]
                if bk['before']['opts'] or bk['before']['state'] != 'putback' or bk['before']['aria'] != L['put_back']:
                    out.append('%s %s: before put-back (%s) %s' % (tagl, i, via, bk['before']))
                if bk['state'] != 'big' or not bk['on'] or not bk['opts'] or bk['say']:
                    out.append('%s %s: putting it back (%s) does not put the disguise on and ask (%s)' % (tagl, i, via, bk))
                if [tuple(g) for g in bk['blocks']['groups']] != want_b[0] or bk['blocks']['held'] != want_b[1]:
                    out.append('%s %s: after put-back (%s) the blocks are %s, expected %s' % (tagl, i, via, bk['blocks'], want_b))
                if bk['ask'] != '%d + %d = {?}' % tuple(q['big']):
                    out.append('%s %s: after put-back the question is %r, not the plain big sum' % (tagl, i, bk['ask']))
                if bk['labelled'] or bk['written']:
                    out.append('%s %s: after put-back (%s) the blocks carry a label or a value under them (%r)' % (tagl, i, via, bk['written']))
            # NO-LABELS: from the start until the answer is marked, neither the answer nor the regrouped tens is shown or
            # spoken; the put-back read-aloud is the line alone.
            give = giveaways(q)
            for where, state, text, read in r['shown']:
                if where.startswith('after marking'):
                    continue
                hit = give & set(re.findall(r'\d+', text))
                if hit:
                    out.append('%s %s: %s gives the answer away on screen: %s in %r' % (tagl, i, where, sorted(hit), re.sub(r'\s+', ' ', text).strip()))
                hit = give & set(re.findall(r'\d+', read))
                if hit:
                    out.append('%s %s: %s gives the answer away in the read-aloud: %s in %r' % (tagl, i, where, sorted(hit), read))
                if state == 'putback' and read != PUT_BACK_READ:
                    out.append('%s %s: at put-back the read-aloud is %r, not %r' % (tagl, i, read, PUT_BACK_READ))
        if st == 3:
            if r['wigOn']['state'] != 'big' or r['wigOn']['sum'] != big or not r['wigOn']['on']:
                out.append('%s %s: the wig is not on the big sum at the question (%s)' % (tagl, i, r['wigOn']))
            pk = r['peek']
            if pk['sum'] != little or pk['on'] or pk['say'] != L['reveal'][mode] or pk['tag'] != tag_of(q):
                out.append('%s %s: Peek does not show %s with the reveal line (%s)' % (tagl, i, little, pk))
        bg = r['big']
        if bg['state'] != 'big' or (st != 4 and (bg['sum'] != big or not bg['on'])):
            out.append('%s %s: the big sum is not asked in its disguise (%s)' % (tagl, i, bg))
        if st == 4:
            key = big
            want_opts = {key} | {'%d+%d' % tuple(d['sum']) for d in q['decoys']}
            names = {'%d+%d' % tuple(d['sum']): d['kind'] for d in q['decoys']}
            if bg['line'] != 'find' or bg['promptMath'] != '%d + %d' % (a, b) or bg['prompt'] != L['find'].replace('{little}', ''):
                out.append('%s %s: the Stage 4 question reads %r with %r' % (tagl, i, bg['prompt'], bg['promptMath']))
        else:
            key = str(q['answer'])
            want_opts = {key} | {str(v) for v in q['decoys'].values()}
            if bg['ask'] != '%d + %d = {?}' % tuple(big_of(q)) or bg['prompt'].strip():
                out.append('%s %s: the big sum is asked as %r with the words %r' % (tagl, i, bg['ask'], bg['prompt']))
            names = {str(v): k for k, v in q['decoys'].items()}
        if set(r['optVals']) != want_opts or len(r['optVals']) != len(want_opts):
            out.append('%s %s: options %s, expected %s' % (tagl, i, r['optVals'], sorted(want_opts)))
        bad = [(w, t) for w, t in r['maths'] if one_equals(t)]
        if bad:
            out.append('%s %s: %d rendered maths string(s) break one "=" a line, e.g. %r at %s' % (tagl, i, len(bad), one_equals(bad[0][1]), bad[0][0]))
        rows, hl = working(q)
        for v, o in r['opts'].items():
            right = v == key
            if o['why'] != ('right' if right else 'wrong') or o['score'] != (1 if right else 0):
                out.append('%s %s: option %s marked %s, expected %s' % (tagl, i, v, o['why'], 'right' if right else 'wrong'))
            if o['qa'] != [[right, i]]:
                out.append('%s %s: option %s logged %s' % (tagl, i, v, o['qa']))
            if o['popBefore']:
                out.append('%s %s: the 67 shows before marking' % (tagl, i))
            if (o['pop'] == '67') != has67(q) or (o['pop'] not in (None, '67')):
                out.append('%s %s: after marking the 67 is %r, expected %s' % (tagl, i, o['pop'], 'shown' if has67(q) else 'hidden'))
            if o['learn'] != '|'.join(rows) or not o['katex']:
                out.append('%s %s: the working is %r (KaTeX %s), expected %r' % (tagl, i, o['learn'], o['katex'], '|'.join(rows)))
            tr, th = tex_rows(o['tex'])
            if tr != rows or th != hl or o['hlShown'] != len(hl):
                out.append('%s %s: the working shown is %s with %s highlighted, expected %s with %s' % (tagl, i, tr, th, rows, hl))
            hits = {t for t in every if t in o['shown']}
            if len(hits) > 1:
                out.append('%s %s: option %s: feedback holds %d LINES strings: %s' % (tagl, i, v, len(hits), sorted(hits)))
            if not o['next']:
                out.append('%s %s: no Next after option %s' % (tagl, i, v))
            if st == 4:
                line = L['duck_right'] if right else L['duck_wrong']
                if o['say'] != line:
                    out.append('%s %s: option %s: the duck says %r' % (tagl, i, v, o['say']))
            elif right:
                if o['say'] not in L['right']:
                    out.append('%s %s: a right answer says %r' % (tagl, i, o['say']))
            else:
                k = names.get(v)
                ak = 'concat_cross' if k == 'concat' and q['type'] == 'cross' else k
                if o['pick'] != k or o['say'] != L['aha'].get(ak):
                    out.append('%s %s: decoy %s (%s) says %r, not its aha line' % (tagl, i, v, k, o['say']))
        if any(o['pop'] == '67' for o in r['opts'].values()):
            fired[st] = fired.get(st, 0) + 1
    for st, n in FIRES.items():
        if fired.get(st, 0) != n:
            out.append('%s: the 67 showed on %d stage %d items, not %d' % (tagl, fired.get(st, 0), st, n))
    info['marked'] = info.get('marked', 0) + len(bank_of(html))


GREETINGS = [
    ('', 'grown', None),
    ('#kidsx', 'grown', None),
    ('#kids', 'kids', None),
    ('#KIDS', 'kids', None),
    ('#kids/Maple', 'kids', 'Welcome, Maple Class!'),
    ('#kids/Maple%20Class', 'kids', 'Welcome, Maple Class!'),
    ('#kids/%3Cscript%3Ealert(1)%3C%2Fscript%3E', 'kids', None),
    ('#kids/<script>', 'kids', None),
]


def check_greeting(pw, base, html, out):
    L = contract_lines()
    cases = GREETINGS + [('#kids/Maple', 'kids', 'Welcome, Maple Class!', '?level=bogus')]
    for c in cases:
        frag, look, greet = c[:3]
        query = c[3] if len(c) > 3 else '?cb=verify'
        br, page, errs = open_page(pw, base, html, PHONE, frag, query)
        try:
            got = page.evaluate("""() => ({ kids: document.body.classList.contains('look-kids'),
                welcome: document.getElementById('welcome').textContent, title: document.getElementById('titleLine').textContent,
                scripts: document.querySelectorAll('#welcome *').length, hash: location.hash, look: SID.LOOK })""")
            want = greet or L[look]['welcome']
            if got['kids'] != (look == 'kids') or got['look'] != look:
                out.append('greeting %r: the %s look, expected the %s look' % (frag, got['look'], look))
            if got['welcome'] != want or got['scripts']:
                out.append('greeting %r: the welcome reads %r, expected %r' % (frag, got['welcome'], want))
            if got['title'] != L[look]['title']:
                out.append('greeting %r: the title line reads %r' % (frag, got['title']))
            if frag and got['hash'].lower() != frag.lower() and '%' not in frag and '<' not in frag:
                out.append('greeting %r%s: the fragment became %r' % (frag, query, got['hash']))
            if errs:
                out.append('greeting %r: page error %s' % (frag, errs[0][:120]))
        finally:
            br.close()


# ---------------------------------------------------------------- every item above the fold (PRIMARY-FIT-SWEEP)
# The sweep's stepper (scripts/fit_common.py sweep()): every item, previewed by itself, walked step by step with the real
# buttons' handlers, every control measured at every step, then Next after every feedback variant: each LINES.right line
# (SID.ui.answer's line argument), each decoy (SID.ui.pick), Stage 3 with and without the peek, and the steps after a
# wrong tile. The speaker shows throughout (fit_common's local voice); a 67 pop that shows is left showing.
SPEAK = '#speakBtn'
NEXT = '#feedback .maffs-next, #nextBtn'
FIT_STEPPER = r"""{
  key(q) { return q.stage === 4 ? q.answer_sum[0] + '+' + q.answer_sum[1] : String(q.answer); },
  decoys(q) { return q.stage === 4 ? q.decoys.map(d => d.sum[0] + '+' + d.sum[1]) : Object.values(q.decoys).map(String); },
  variants(id) {
    const q = SID.bank().find(x => x.id === id), lines = SID.lines()[SID.LOOK].right.length, vs = [];
    const pre = q.stage === 3 ? ['', 'peek '] : [''];
    for (const p of pre) {
      if (q.stage === 4) vs.push(p + 'right');
      else for (let i = 0; i < lines; i++) vs.push(p + 'right ' + i);
      for (const d of this.decoys(q)) vs.push(p + 'wrong ' + d);
    }
    if (q.stage === 1 || q.stage === 2 || q.stage === 5) vs.push('wrong tile, then right 0');
    return vs;
  },
  run(id, v, m) {
    const ui = SID.ui, st = () => ui.state();
    const speak = () => { if (document.getElementById('speakBtn').hidden) throw new Error('the speaker is hidden'); };
    ui.preview(id);
    const q = ui.question();
    if (!q || q.id !== id) throw new Error('preview did not show ' + id);
    speak();
    if (st() === 'mask') {
      m('%(s)s, #unmaskBtn, #blocks, #disguise, #tag', 'the blocks and take off');
      ui.unmask();
      if (st() !== 'little') throw new Error('take off left the state ' + st());
      m('%(s)s, #tiles .tile, #blocks, #disguise, #tag, #tenFrame', 'the tiles');
      const k = ui.littleKey();
      ui.tile(v.startsWith('wrong tile') ? (k + 1) %% 11 : k);
      if (st() === 'fill') { m('%(s)s, #fillBtn, #blocks, #tenFrame, #tag', 'fill the ten'); ui.fill(); }
      if (st() !== 'putback') throw new Error('the tiles left the state ' + st());
      m('%(s)s, #putBtn, #blocks', 'put it back');
      ui.putBack();
    }
    if (st() !== 'big') throw new Error('no options: the state is ' + st());
    m('%(s)s, #opts .opt, #peekBtn', 'the options');
    if (v.startsWith('peek ')) { ui.peek(); m('%(s)s, #opts .opt', 'the options, peeking'); }
    const w = v.replace(/^peek /, '').replace(/^wrong tile, then /, '');
    if (w === 'right') ui.answer(true);
    else if (w.startsWith('right ')) ui.answer(true, +w.slice(6));
    else ui.pick(w.slice(6));
    if (st() !== (w.startsWith('right') ? 'done' : 'wrong')) throw new Error('marking left the state ' + st());
    if (w.startsWith('right ') && document.getElementById('say').dataset.say !== 'right.' + w.slice(6))
      throw new Error('the right line is ' + document.getElementById('say').dataset.say + ', not right.' + w.slice(6));
    m('%(s)s, %(n)s', 'Next');
  }
}""" % {'s': SPEAK, 'n': NEXT}


def check_fit(pw, base, html, look, st, out, info):
    """Every stage-st item in one look at 360 x 640, the speaker showing: every control at every step and Next after every
    feedback variant above the fold (fit_common.sweep)."""
    frag = '#kids/Maple' if look == 'kids' else ''
    br, page, errs = fc.open_phone(pw, base, html, SLUG, '!!window.SID && !!SID.ui', frag, PHONE)
    try:
        if page.evaluate("document.body.classList.contains('look-kids')") != (look == 'kids'):
            out.append('fit %s stage %d: the page is not in the %s look' % (look, st, look))
        ids = [q['id'] for q in page.evaluate('SID.bank()') if q['stage'] == st]
        got = fc.sweep(page, ids, FIT_STEPPER, out, 'fit %s %dx%d' % (look, PHONE[0], PHONE[1]))
        if got['items'] != COUNTS[st]:
            out.append('fit %s stage %d: %d items measured, expected %d' % (look, st, got['items'], COUNTS[st]))
        for k in ('items', 'variants', 'measures'):
            info.setdefault('fit', {}).setdefault(k, 0)
            info['fit'][k] += got[k]
    finally:
        out.extend('page error (fit %s stage %d): %s' % (look, st, e) for e in errs if 'production host' not in e)
        br.close()


def play(page, look, m, out):
    L = contract_lines()[look]
    page.evaluate("() => { window.__ev = []; window.__sub = []; }")
    page.evaluate('(m) => SID.ui.start(m)', m)
    st = int(m[-1])
    tag = '%s %s' % (look, m)
    seen, right, k, unpeeked = [], 0, 0, 0
    for _ in range(300):
        s = page.evaluate('SID.ui.state()')
        if s == 'over':
            break
        # Stages 1, 2 and 5, step by step with the real buttons (the hops and flights run at full motion here).
        if s == 'mask':
            q = page.evaluate('SID.ui.question()')
            seen.append(q['id'])
            hand(page, look, len(seen), 'unmaskBtn', tag, out)
            page.evaluate("document.getElementById('unmaskBtn').click()")
            page.wait_for_function("SID.ui.state() === 'little'", timeout=5000)
            continue
        if s == 'little':
            q = page.evaluate('SID.ui.question()')
            if st == 5:
                hand(page, look, len(seen), 'tiles', tag, out)
            key = page.evaluate('SID.ui.littleKey()')
            page.evaluate('(v) => SID.ui.tile(v)', key if k % 2 == 0 else (key + 1) % 11)
            continue
        if s == 'fill':
            q = page.evaluate('SID.ui.question()')
            hand(page, look, len(seen), 'fillBtn', tag, out)
            page.evaluate("document.getElementById('%s').click()" % ('fillBtn' if k % 2 == 0 else 'tenFrame'))
            page.wait_for_function("SID.ui.state() === 'putback'", timeout=5000)
            continue
        if s == 'putback':
            q = page.evaluate('SID.ui.question()')
            hand(page, look, len(seen), 'putBtn', tag, out)
            page.evaluate("document.getElementById('putBtn').click()")
            page.wait_for_function("SID.ui.state() === 'big'", timeout=5000)
            continue
        if s in ('taking', 'filling'):
            page.wait_for_timeout(100)
            continue
        if s == 'big':
            q = page.evaluate('SID.ui.question()')
            if not seen or seen[-1] != q['id']:
                seen.append(q['id'])
                hand(page, look, len(seen), 'opts', tag, out)
            elif page.evaluate("!document.getElementById('hand').hidden"):
                out.append('%s: the hand is still showing after the disguise came off' % tag)
            ok = k % 3 != 1
            peeked = st == 3 and k % 4 == 0
            if peeked:
                page.evaluate('SID.ui.peek()')
            page.evaluate('(r) => SID.ui.answer(r)', ok)
            right += 1 if ok else 0
            unpeeked += 1 if ok and not peeked else 0
            k += 1
            continue
        page.evaluate('SID.ui.next()')
    if page.evaluate('SID.ui.state()') != 'over':
        out.append('%s: the run did not finish' % tag)
        return
    if len(seen) != PER or len(set(seen)) != PER or any(not x.startswith('s%d_' % st) for x in seen):
        out.append('%s: the run served %s, not %d different stage %d items' % (tag, seen, PER, st))
    ev = page.evaluate('window.__ev')
    sub = page.evaluate('window.__sub')
    done = [p for n, p in ev if n == 'game_completed']
    if len(done) != 1 or done[0].get('score') != right or done[0].get('level') != 'year6' or done[0].get('mode') != m:
        out.append('%s: game_completed %s, expected one with score %d' % (tag, done, right))
    if sub != [[SLUG, m, right, PER]]:
        out.append('%s: the leaderboard got %s, expected one submission on %s with %d' % (tag, sub, m, right))
    qa = [p for n, p in ev if n == 'question_answered']
    if len(qa) != PER or [p.get('question_id') for p in qa] != seen or any(p.get('mode') != m or p.get('level') != 'year6' for p in qa):
        out.append('%s: question_answered %s, expected one per item with its id' % (tag, [p.get('question_id') for p in qa]))
    names = sorted({n for n, _ in ev})
    if not set(names) <= {'game_started', 'question_answered', 'game_completed', 'personal_best_set'}:
        out.append('%s: events %s' % (tag, names))
    blob = json.dumps(ev)
    for bad in ('kids', 'Maple', '#'):
        if bad in blob:
            out.append('%s: an mfg() payload contains %r' % (tag, bad))
    if bad_in_storage(page):
        out.append('%s: browser storage holds %s' % (tag, bad_in_storage(page)))
    end = page.evaluate("document.getElementById('endLine').textContent")
    if end != L['end']:
        out.append('%s: the end line reads %r' % (tag, end))
    score = page.evaluate("document.getElementById('resScore').textContent")
    if score != str(right):
        out.append('%s: the end screen shows %s, not %d' % (tag, score, right))
    if st == 3:
        np = page.evaluate("(document.getElementById('noPeek') || {}).textContent || ''")
        if np != 'Done without peeking: %d of %d' % (unpeeked, PER):
            out.append('%s: the end screen reads %r, expected "Done without peeking: %d of %d"' % (tag, np, unpeeked, PER))
    page.evaluate("document.getElementById('menuBtn').click()")


def hand(page, look, n, at, tag, out):
    h = page.evaluate("(() => { const h = document.getElementById('hand'); return { shown: !h.hidden, at: h.dataset.at || null }; })()")
    want = look == 'kids' and n == 1
    if h['shown'] != want or (want and h['at'] != at):
        out.append('%s question %d: the hand is %s%s, expected %s' % (tag, n, 'shown' if h['shown'] else 'hidden',
                   ' on ' + str(h['at']) if h['shown'] else '', ('shown on ' + at) if want else 'hidden'))


# ---------------------------------------------------------------- read aloud, against a mocked speechSynthesis
SPEECH_MOCK = """(() => { const cfg = %s; window.__spoken = []; window.__cancels = 0;
  if (cfg === 'none') { try { delete window.speechSynthesis; } catch (e) {} Object.defineProperty(window, 'speechSynthesis', { value: undefined, configurable: true }); return; }
  const voices = cfg.slice(), listeners = [];
  const synth = { getVoices() { return voices.slice(); },
    speak(u) { window.__spoken.push({ text: u.text, local: !!(u.voice && u.voice.localService === true), name: u.voice ? u.voice.name : null }); },
    cancel() { window.__cancels++; }, addEventListener(t, f) { if (t === 'voiceschanged') listeners.push(f); }, removeEventListener() {} };
  window.__setVoices = (vs) => { voices.length = 0; vs.forEach(v => voices.push(v)); listeners.forEach(f => f()); };
  Object.defineProperty(window, 'speechSynthesis', { value: synth, configurable: true });
  window.SpeechSynthesisUtterance = function (t) { this.text = t; this.voice = null; this.lang = ''; };
})();"""
REMOTE = {'name': 'Cloud UK', 'lang': 'en-GB', 'localService': False}
LOCAL = {'name': 'Device US', 'lang': 'en-US', 'localService': True}


def speech_page(pw, base, html, cfg, frag=''):
    br = pw.chromium.launch()
    ctx = br.new_context(viewport={'width': PHONE[0], 'height': PHONE[1]})
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    ctx.add_init_script(SPEECH_MOCK % json.dumps(cfg))
    ctx.add_init_script("""(() => { window.__ev = []; Object.defineProperty(window, 'mfg', { configurable: true,
        get() { return function (n, p) { window.__ev.push([n, JSON.parse(JSON.stringify(p || {}))]); }; }, set(v) {} }); })();""")
    bc.offline(ctx, base)
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    page = ctx.new_page()
    page.goto(base + '/games/%s/?cb=verify%s' % (SLUG, frag), wait_until='load', timeout=30000)
    page.wait_for_function('!!window.SID && !!SID.ui', timeout=15000)
    page.evaluate("() => { window.MaffsLeaderboard = window.MaffsLeaderboard || {}; MaffsLeaderboard.submitScore = () => Promise.resolve(); }")
    return br, page


def check_speech(pw, base, html, out, info):
    L = contract_lines()
    shown = "!document.getElementById('speakBtn').hidden && getComputedStyle(document.getElementById('speakBtn')).display !== 'none'"
    for cfg, what in (('none', 'no speechSynthesis'), ([], 'no voices'), ([REMOTE], 'only a voice that is not local')):
        br, page = speech_page(pw, base, html, cfg)
        try:
            page.evaluate("SID.ui.start('stage-1')")
            if page.evaluate(shown):
                out.append('read aloud: the speaker shows with %s' % what)
        finally:
            br.close()
    bank = bank_of(html)
    for frag, look in (('', 'grown'), ('#kids/Maple', 'kids')):
        br, page = speech_page(pw, base, html, [], frag)
        try:
            spoken = lambda: page.evaluate('window.__spoken')
            if page.evaluate(shown):
                out.append('read aloud (%s): the speaker shows before any voice has arrived' % look)
            page.evaluate('(v) => window.__setVoices(v)', [REMOTE, LOCAL])
            page.evaluate("SID.ui.start('stage-1')")
            if not page.evaluate(shown):
                out.append('read aloud (%s): no speaker after a local voice arrived' % look)
                continue
            if spoken():
                out.append('read aloud (%s): spoke %r before any tap' % (look, spoken()[0]['text']))
            # Above the fold with the speaker showing: every item, every step, in check_fit() (fit_common's sweep).
            page.evaluate("() => { window.__spoken = []; }")
            tap = lambda: page.evaluate("document.getElementById('speakBtn').click()")
            for st in (1, 2, 3, 4, 5):
                for q in [x for x in bank if x['stage'] == st][:4]:
                    a, b = q['little']
                    p, r = big_of(q)
                    page.evaluate('(id) => SID.ui.preview(id)', q['id'])
                    if spoken():
                        out.append('read aloud (%s) %s: spoke without a tap' % (look, q['id']))
                    noun = {1: 'moustache', 2: 'glasses', 5: 'hat'}.get(st)
                    t = (p - a) // 10
                    if st == 4:
                        want = [L[look]['find'].replace('{little}', '%d plus %d' % (a, b))]
                    elif st == 3:
                        want = ['%d plus %d equals what?' % (p, r)]
                    elif q['type'] == 'tens':
                        want = ['%d is %d tens and %d is %d tens.' % (p, a, r, b)]
                    else:
                        want = ['%d is %d tens and %d ones. The tens go in the %s.' % (p, t, a, noun)]
                    tap()
                    if st in (1, 2, 5):
                        page.evaluate('SID.ui.unmask()')
                        tap()
                        if st == 5:
                            want.append('%d and how many make 10?' % a)
                            page.evaluate('(v) => SID.ui.tile(v)', 10 - a)
                            tap()
                            want.append('Fill the ten.')
                            page.evaluate('SID.ui.fill()')
                        else:
                            want.append('%d plus %d equals what?' % (a, b))
                            page.evaluate('(v) => SID.ui.tile(v)', a + b)
                        tap()
                        want.append(PUT_BACK_READ)
                        page.evaluate('SID.ui.putBack()')
                    page.evaluate('SID.ui.answer(false)')
                    line = page.evaluate("document.getElementById('say').textContent")
                    tap()
                    want.append(line + ' ' + spoken_working(q))
                    got = spoken()
                    if [x['text'] for x in got] != want:
                        out.append('read aloud (%s) %s: spoke %s, expected %s' % (look, q['id'], [x['text'] for x in got], want))
                    if any(not x['local'] for x in got):
                        out.append('read aloud (%s) %s: a voice that is not local was passed to speak()' % (look, q['id']))
                    if any('Maple' in x['text'] or 'Welcome' in x['text'] for x in got):
                        out.append('read aloud (%s): it read the greeting' % look)
                    before = page.evaluate('window.__cancels')
                    page.evaluate('SID.ui.next()')
                    if page.evaluate('window.__cancels') <= before:
                        out.append('read aloud (%s) %s: no speechSynthesis.cancel() on Next' % (look, q['id']))
                    page.evaluate('() => { window.__spoken = []; }')
            before = page.evaluate('window.__cancels')
            page.evaluate("document.getElementById('menuBtn').click()")
            if page.evaluate('window.__cancels') <= before:
                out.append('read aloud (%s): no speechSynthesis.cancel() on leaving the play screen' % look)
            blob = json.dumps(page.evaluate('window.__ev'))
            if re.search(r'speak|speech|voice|read', blob, re.I):
                out.append('read aloud (%s): an mfg() payload mentions it' % look)
            dump = page.evaluate("""() => JSON.stringify(Object.assign({}, ...[localStorage, sessionStorage].map(s => Object.fromEntries(Object.keys(s).map(k => [k, s.getItem(k)])))))""")
            if re.search(r'speak|speech|voice|read', dump, re.I):
                out.append('read aloud (%s): browser storage mentions it' % look)
        finally:
            br.close()
    info['speech'] = 2


def bad_in_storage(page):
    dump = page.evaluate("""() => { const o = {};
      for (const s of [localStorage, sessionStorage]) for (let i = 0; i < s.length; i++) o[s.key(i)] = s.getItem(s.key(i));
      return JSON.stringify(o); }""")
    return [b for b in ('kids', 'Maple', '#') if b in dump]


def check(html, out, units, shard=None):
    unit = shard.unit if shard is not None else (lambda uid: contextlib.nullcontext())
    info = {}
    if 'bank' in units:
        with unit('bank'):
            try:
                check_bank(html, out, info)
                check_source(html, out)
                check_picture(html, out)
            except Exception as e:  # noqa: BLE001
                out.append('the bank checks threw: %s' % str(e).splitlines()[0][:200])
    browser = [u for u in units if u != 'bank']
    if not browser:
        return info
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            for uid in browser:
                with unit(uid):
                    if uid == 'read aloud':
                        try:
                            check_speech(pw, base, html, out, info)
                        except Exception as e:  # noqa: BLE001
                            out.append('read aloud threw: %s' % str(e).splitlines()[0][:220])
                        continue
                    if uid.startswith('fit '):
                        _, look, m = uid.split(' ')
                        try:
                            check_fit(pw, base, html, look, int(m[-1]), out, info)
                        except Exception as e:  # noqa: BLE001
                            out.append('%s threw: %s' % (uid, str(e).splitlines()[0][:220]))
                        continue
                    if uid == 'greeting':
                        try:
                            check_greeting(pw, base, html, out)
                            info['greeting'] = len(GREETINGS) + 1
                        except Exception as e:  # noqa: BLE001
                            out.append('greeting threw: %s' % str(e).splitlines()[0][:220])
                        continue
                    look = 'kids' if ' kids' in uid else 'grown'
                    frag = '#kids/Maple' if look == 'kids' else ''
                    size = PHONE if uid.startswith('play') else (1280, 800)
                    br, page, errs = open_page(pw, base, html, size, frag)
                    try:
                        if not page.evaluate("document.body.classList.contains('look-kids')") == (look == 'kids'):
                            out.append('%s: the page is not in the %s look' % (uid, look))
                        if uid.startswith('marking'):
                            check_marking(page, html, look, out, info)
                        else:
                            for m in MODES:
                                play(page, look, m, out)
                            info['played'] = info.get('played', 0) + len(MODES)
                    except Exception as e:  # noqa: BLE001
                        out.append('%s threw: %s' % (uid, str(e).splitlines()[0][:220]))
                    out.extend('page error (%s): %s' % (uid, e) for e in errs if 'production host' not in e)
                    br.close()
    finally:
        proc.terminate()
    return info


# Each plant: (what, edit(html) -> html, the unit it needs, the pattern its finding must match). The nine the contract names.
def edit(old, new):
    return lambda html, what: pc.apply_plant(html, old, new, name=what)


PLANTS = [
    ('an answer 1 out',
     edit('{"id":"s1_001","stage":1,"type":"ones","big":[56,3],"little":[6,3],"little_answer":9,"answer":59,',
          '{"id":"s1_001","stage":1,"type":"ones","big":[56,3],"little":[6,3],"little_answer":9,"answer":60,'),
     'bank', r's1_001: answer 60, recomputed 59'),
    ('a decoy equal to the answer',
     edit('{"id":"s2_001","stage":2,"type":"tens","big":[40,50],"little":[4,5],"little_answer":9,"answer":90,"decoys":{"forgot_disguise":9,"extra_zero":900,"ones":45}}',
          '{"id":"s2_001","stage":2,"type":"tens","big":[40,50],"little":[4,5],"little_answer":9,"answer":90,"decoys":{"forgot_disguise":9,"extra_zero":900,"ones":90}}'),
     'bank', r's2_001: a decoy equals the answer'),
    ('a Stage 1 item that crosses a ten',
     edit('{"id":"s1_001","stage":1,"type":"ones","big":[56,3],"little":[6,3],"little_answer":9,"answer":59,"decoys":{"tens":86,"concat":509,"off_by_one":60}}',
          '{"id":"s1_001","stage":1,"type":"ones","big":[58,3],"little":[8,3],"little_answer":11,"answer":61,"decoys":{"tens":88,"concat":5011,"off_by_one":62}}'),
     'bank', r's1_001: a ones item crosses a ten'),
    ("a Stage 5 item that doesn't cross a ten",
     edit('{"id":"s5_011","stage":5,"type":"cross","big":[19,3],"little":[9,3],"little_answer":12,"answer":22,"decoys":{"forgot_ten":12,"concat":112,"off_by_one":23}}',
          '{"id":"s5_011","stage":5,"type":"cross","big":[15,3],"little":[5,3],"little_answer":8,"answer":18,"decoys":{"forgot_ten":8,"concat":18,"off_by_one":19}}'),
     'bank', r's5_011: a cross item does not cross a ten'),
    ('a Stage 4 decoy that is the same fact swapped',
     edit('"answer_sum":[83,1],"answer":84,"decoys":[{"kind":"changed_first","sum":[84,1]}',
          '"answer_sum":[83,1],"answer":84,"decoys":[{"kind":"changed_first","sum":[81,3]}'),
     'bank', r's4_005: Stage 4 decoy 81 \+ 3 is the same fact as 3 \+ 1'),
    ('an option marked by its rendered text',
     edit('var b = e.currentTarget, val = b.dataset.val;', 'var b = e.currentTarget, val = b.textContent;'),
     'marking grown', r'option \S+ marked wrong, expected right'),
    ('the 67 shown before marking',
     edit("    box.hidden = false;\n    MaffsLock.fresh(box);\n    if (S.flow === 'wig') {",
          "    box.hidden = false;\n    MaffsLock.fresh(box);\n    if (has67(Q)) showPop();\n    if (S.flow === 'wig') {"),
     'marking grown', r'the 67 shows before marking'),
    ('the class name written with innerHTML',
     edit("$('welcome').textContent = greeting();", "$('welcome').innerHTML = greeting();"),
     'bank', r'the greeting \(the class name\) is written with innerHTML'),
    ('"Maple" in an mfg() payload',
     edit("ev('game_started', { game_slug: SLUG, level: level, mode: mode });",
          "ev('game_started', { game_slug: SLUG, level: level, mode: mode, cls: CLASS_NAME || '' });"),
     'play kids %dx%d' % PHONE, r"an mfg\(\) payload contains 'Maple'"),
    # Amendment 1's five.
    ('feedback showing two LINES strings',
     edit("      sayText = L[sayKey];\n", "      sayText = L[sayKey] + ' ' + L.reveal[mode];\n"),
     'marking grown', r'feedback holds 2 LINES strings'),
    ('a kid line of 7 words',
     edit('end: "All sums unmasked!"', 'end: "All of the sums are now unmasked!"'),
     'marking grown', r'LINES\.kids\.end has 7 words'),
    ('a non-local voice used',
     lambda html, what: pc.apply_plant(pc.apply_plant(html,
         "if (all[i] && all[i].localService === true) local.push(all[i]);", "if (all[i]) local.push(all[i]);", name=what),
         "if (!canSpeak || !voice || voice.localService !== true || !text) return;", "if (!canSpeak || !voice || !text) return;", name=what),
     'read aloud', r'a voice that is not local was passed to speak\(\)|the speaker shows with only a voice that is not local'),
    ('speech on load without a tap',
     edit("    $('speakBtn').hidden = !voice;\n", "    $('speakBtn').hidden = !voice;\n    if (voice) speak(L.title);\n"),
     'read aloud', r'spoke .* before any tap'),
    ('a working number typed rather than taken from the item',
     edit("var row1 = [[a + ' + ' + b, false], [' = ', false], [String(c), false]];",
          "var row1 = [[a + ' + ' + b, false], [' = ', false], [String(9), false]];"),
     'marking grown', r'the working (is|shown is)'),
    # SUMS-IN-DISGUISE-ART and its Amendment 1.
    ('the start picture with no alt',
     edit('width="1600" height="873" alt="%s">' % PICTURE_ALT, 'width="1600" height="873">'),
     'bank', r'start picture: the tag has no alt='),
    # Amendment 3: tens on show (Stages 1, 2 and 5).
    ('a wrong stick count',
     edit("else drawBlocks([{ sticks: tensOf(Q), cubes: Q.little[0] }, { cubes: Q.little[1] }]);",
          "else drawBlocks([{ sticks: tensOf(Q) + 1, cubes: Q.little[0] }, { cubes: Q.little[1] }]);"),
     'marking grown', r'the blocks at the start are'),
    ('a wrong cube count',
     edit("else drawBlocks([{ sticks: tensOf(Q), cubes: Q.little[0] }, { cubes: Q.little[1] }]);",
          "else drawBlocks([{ sticks: tensOf(Q), cubes: Q.little[0] }, { cubes: Q.little[1] + 1 }]);"),
     'marking grown', r'the blocks at the start are'),
    ('the disguise hidden at take-off',
     edit("      state = 'little';\n      disguiseOn(false);\n", "      state = 'little';\n      disguiseOn(false);\n      $('disguise').style.visibility = 'hidden';\n"),
     'marking grown', r'at take-off the disguise is not in view beside the sum'),
    ('the options before put-back',
     edit("    $('blocksNote').innerHTML = tex(String(c));\n    showPutBack();",
          "    $('blocksNote').innerHTML = tex(String(c));\n    askBig();\n    showPutBack();"),
     'marking grown', r'options exist before put-back|before put-back \('),
    # ONE-EQUALS.
    ('an empty cubes group drawn at put-back',
     edit("drawBlocks([{ sticks: t + 1 }].concat(c - 10 ? [{ cubes: c - 10 }] : []));",
          "drawBlocks([{ sticks: t + 1 }, { cubes: c - 10 }]);"),
     'marking grown', r's5_\d+: after put-back \(button\) the blocks are'),
    ('"81 + 9 = 90 + 0 = ?"',
     edit("      // After put-back: the plain big sum (ONE-EQUALS); the blocks under it show the regrouping.\n      askSum(Q.big);",
          "      askSum(Q.big);\n      $('sum').innerHTML = tex(Q.big[0] + ' + ' + Q.big[1] + ' = ' + (Q.big[0] - Q.little[0] + (Q.type === 'cross' ? 10 : 0)) + ' + ' + (Q.type === 'cross' ? Q.little_answer - 10 : Q.little_answer) + ' = {?}');"),
     'marking grown', r'break one "=" a line'),
    ('the Stage 5 reveal at take-off',
     edit("      if (!S.bridge) setSay(L.reveal[mode], 'reveal.' + mode); else setSay('');",
          "      setSay(L.reveal[mode], 'reveal.' + mode);"),
     'marking grown', r's5_\d+: at take-off the line is'),
    ('"Find {little}!"',
     edit('find: "Find {little} in disguise!",', 'find: "Find {little}!",'),
     'bank', r"a LINES string puts '\{little\}!' straight after a sum"),
    # NO-LABELS.
    ('an "80" label under the sticks of "70 + 10"',
     edit("    if (Q.type === 'tens') drawBlocks([{ sticks: c }]);\n",
          "    if (Q.type === 'tens') drawBlocks([{ sticks: c }]);\n    if (Q.big[0] === 70 && Q.big[1] === 10) $('blocks').querySelector('.grp').insertAdjacentHTML('beforeend', '<span class=\"glabel\">' + tex(String(10 * c)) + '</span>');\n"),
     'marking grown', r's2_011: after put-back \(button\) the blocks carry a label|s2_011: after put-back gives the answer away on screen: \[.80.\]'),
    ('the spoken "70 and 10. Put it back on." before marking',
     edit("    if (state === 'putback') return 'Put it back on.';",
          "    if (state === 'putback') return Q.type === 'cross' ? 10 * tensOf(Q) + ' and 10. Put it back on.' : 'Put it back on.';"),
     'marking grown', r"s5_\d+: at put-back the read-aloud is '70 and 10\. Put it back on\.'"),
    # BRIDGE: Stage 5 fills the next ten first.
    ('the step-2 key set to a + b (the old method)',
     edit("  function littleKey(q) { return S.bridge ? 10 - q.little[0] : q.little_answer; }",
          "  function littleKey(q) { return q.little_answer; }"),
     'marking grown', r's5_\d+: the step-2 tile key is \d+, expected \d+'),
    ('the old working line "8 + 6 = 14" shown',
     edit("        return rest ? [r1, hlTens(nx, typ)",
          "        r1 = [[a + ' + ' + b, false], [' = ', false], [String(c), false]];\n        return rest ? [r1, hlTens(nx, typ)"),
     'marking grown', r's5_\d+: the working is \'\d \+ \d = 1\d\|'),
    ('fill skipped',
     edit("      state = 'fill';\n      showSum(Q.little);\n      $('tenFrame').disabled = false;\n      showRow('fillRow', L.fill_ten, null);\n      return;",
          "      state = 'fill';\n      fillTen(true);\n      return;"),
     'marking grown', r's5_\d+: tile \d+ marked \w+, expected \w+, then fill'),
    ('a wrong rest count',
     edit("        drawBlocks(rest ? [{ cubes: rest }] : []);\n        setSay(L.reveal[mode], 'reveal.' + mode);",
          "        drawBlocks([{ cubes: rest + 1 }]);\n        setSay(L.reveal[mode], 'reveal.' + mode);"),
     'marking grown', r's5_\d+: after the fill \(button\) the blocks are'),
    ('"40 + 4" with the wrong number',
     edit("        return rest ? [r1, hlTens(nx, typ).concat([[' + ' + rest, false]",
          "        return rest ? [r1, hlTens(nx, typ).concat([[' + ' + (rest + 1), false]"),
     'marking grown', r's5_\d+: the working is'),
    # PRIMARY-FIT-SWEEP: the fold, on one item and one feedback variant only (a sample would miss it most runs).
    ('Next below the fold after one decoy of one item (s5_005, 617)',
     edit("    if (right) {\n      MaffsLock.fresh(fb);",
          "    if (Q.id === 's5_005' && val === '617') fb.insertAdjacentHTML('afterbegin', '<div style=\"height:160px\"></div>');\n    if (right) {\n      MaffsLock.fresh(fb);"),
     'fit kids stage-5', r'^fit kids 360x640 s5_005 \[wrong 617\] \(Next\): .* below the fold'),
    ('Next below the fold after one right-answer line only (right.3, s1_001)',
     edit("    if (right) {\n      MaffsLock.fresh(fb);",
          "    if (Q.id === 's1_001' && sayKey === 'right.3') fb.insertAdjacentHTML('afterbegin', '<div style=\"height:160px\"></div>');\n    if (right) {\n      MaffsLock.fresh(fb);"),
     'fit grown stage-1', r'^fit grown 360x640 s1_001 \[right 3\] \(Next\): .* below the fold'),
]


def selftest(html, plants=None, shard=None):
    ok = True
    for what, plant, unit_id, want in (PLANTS if plants is None else plants):
        with (shard.unit('plant: ' + what) if shard is not None else contextlib.nullcontext()):
            try:
                src = plant(html, what)
            except pc.StalePlant as e:
                print('  self-test %-58s *** %s ***' % (what, e))
                ok = False
                continue
            got, err = [], None
            try:
                check(src, got, [unit_id])
            except Exception as e:  # noqa: BLE001
                err = e
            hit = [g for g in got if re.search(want, g)]
            caught = pc.is_caught(hit, err)
            print('  self-test %-58s %s' % (what, ('caught: ' + hit[0][:90]) if caught else '*** MISSED ***' + (' (other: %s)' % got[0][:90] if got else '') + (' (error: %s)' % err if err else '')))
            ok = caught and ok
    return ok


def main():
    ap = argparse.ArgumentParser()
    bc.shard_args(ap)
    ap.add_argument('--selftest', action='store_true', help='the planted faults only')
    args = ap.parse_args()
    shard = bc.Shard(__file__, args)
    units = ['bank', 'marking grown', 'marking kids', 'greeting', 'read aloud', 'play grown %dx%d' % PHONE, 'play kids %dx%d' % PHONE]
    units += ['fit %s %s' % (look, m) for look in ('grown', 'kids') for m in MODES]
    if args.selftest:
        units = []
    mine = shard.pick(units + ['plant: ' + p[0] for p in PLANTS])
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    html = open(GAME, encoding='utf-8').read()
    out = []
    run = [u for u in units if u in mine]
    info = check(html, out, run, shard) if run else {}
    if 'bank' in info:
        print('%s: %d items, SHA-256 as the contract states, every number and decoy recomputed from little and the tens; coverage and the 67 counts' % (SLUG, info['bank']))
    if 'marked' in info:
        print('%s: %d item plays marked (every tile and option by dataset.val, the aha and learning lines, the 67 after marking)' % (SLUG, info['marked']))
    if 'greeting' in info:
        print('%s: %d fragments read for the look and the greeting' % (SLUG, info['greeting']))
    if 'speech' in info:
        print('%s: read aloud against a mocked speechSynthesis: hidden without a local voice, local voices only, nothing before a tap, words from the item, cancel on Next and on leaving, nothing sent or stored' % SLUG)
    if 'fit' in info:
        print('%s: every item above the fold at %dx%d, speaker showing: %d item views, %d feedback variants, %d controls measured (the looks and stages in this shard)'
              % (SLUG, PHONE[0], PHONE[1], info['fit']['items'], info['fit']['variants'], info['fit']['measures']))
    if 'played' in info:
        print('%s: %d runs played at %dx%d (every stage, the looks in this shard)' % (SLUG, info['played'], PHONE[0], PHONE[1]))
    ok = selftest(html, [p for p in PLANTS if 'plant: ' + p[0] in mine], shard)
    for f in out[:80]:
        print('FAIL  ' + f)
    if len(out) > 80:
        print('FAIL  ... and %d more' % (len(out) - 80))
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if out or not ok else 'PASS')
    return 1 if out or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
