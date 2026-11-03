#!/usr/bin/env python3
"""Turn question_id values from the Sheet or GA4 back into questions (contract QUESTION-ID, Jon, 3 Nov 2026; canon §1.3).

A game that sends question_text has it hashed by schools/assets/analytics.js: question_id = "h" + the 8-hex-digit
FNV-1a (32-bit) hash of the text, normalised (Unicode NFC, each run of spaces, tabs, line breaks and no-break spaces
to one space, then trimmed), over its UTF-8 bytes. The text itself never leaves the page. question_hash() below is
the same function; scripts/check-question-id.py compares the two in Chromium, so they cannot drift apart.

This works for a game whose bank is static: the text of every question can be rebuilt here from the page's source,
with no browser. Each such game is in RECIPES, with the expression its page passes as question_text, verbatim
(check-question-id.py fails the page if its expression differs) and the same text built in Python.

    python -X utf8 scripts/decode-question-ids.py sequence-solver            id, where, question (tab-separated)
    python -X utf8 scripts/decode-question-ids.py sequence-solver --id h1234abcd   one id
    python -X utf8 scripts/decode-question-ids.py sequence-solver --json     {id: [{"where", "text"}, ...]}

Exit 1 if two different questions in the game share an id (a hash collision: contract STOP IF), or the bank cannot
be read. The same text in two places is the same question, one id: listed, not a collision.
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))

WS = re.compile('[ \t\n\r\f\v\u00a0]+')   # analytics.js: /[ \t\n\r\f\v\u00a0]+/g


def question_hash(text):
    """analytics.js questionHash(), exactly."""
    s = WS.sub(' ', unicodedata.normalize('NFC', str(text)))
    if s.startswith(' '):
        s = s[1:]
    if s.endswith(' '):
        s = s[:-1]
    h = 0x811c9dc5
    for b in s.encode('utf-8'):
        h ^= b
        h = (h * 0x01000193) & 0xffffffff
    return 'h%08x' % h


def _join(*parts):
    """JavaScript's [a, b, c].filter(Boolean).join(' | ') for string fields."""
    return ' | '.join(p for p in parts if p)


# One entry per game moved onto question_text with a static bank.
#   page   the game's page
#   bank   the top-level variable holding the bank: a list, or {level: list}
#   expr   the page's question_text expression, verbatim (check-question-id.py holds the page to it)
#   text   the same text, from one bank item, in Python
RECIPES = {
    'sequence-solver': {
        'page': 'games/sequence-solver/index.html',
        'bank': 'QUESTIONS',
        'expr': "[q.seq,q.q,q.ask].filter(Boolean).join(' | ')",
        'text': lambda q: _join(q.get('seq'), q.get('q'), q.get('ask')),
    },
}


def read_bank(slug, root=ROOT, html=None):
    """[(where, item)] for every question in the game's static bank, in source order."""
    import bank_common as bc   # needs esprima (see the cloud handover's container setup)
    r = RECIPES[slug]
    if html is None:
        html = (root / r['page']).read_text(encoding='utf-8')
    tree, _ = bc.parse_game_source(html)
    if tree is None:
        raise ValueError('%s: the page does not parse' % r['page'])
    found = [init for name, init, _ in bc.top_level_declarations(tree) if name == r['bank']]
    if len(found) != 1:
        raise ValueError('%s: %d top-level declarations of %s' % (r['page'], len(found), r['bank']))
    value = bc.static_bank_value(r['bank'], found[0], tree)
    if value is None:
        raise ValueError('%s: %s is not a static literal' % (r['page'], r['bank']))
    groups = value.items() if isinstance(value, dict) else [('', value)]
    out = []
    for level, items in groups:
        for i, q in enumerate(items):
            out.append(('%s[%d]' % (level, i) if level else '[%d]' % i, q))
    return out


def decode(slug, root=ROOT, html=None):
    """({id: [(where, text)]}, [collision messages])."""
    ids = {}
    for where, q in read_bank(slug, root, html):
        text = RECIPES[slug]['text'](q)
        ids.setdefault(question_hash(text), []).append((where, text))
    collisions = []
    for qid, uses in sorted(ids.items()):
        texts = {WS.sub(' ', unicodedata.normalize('NFC', t)).strip(' ') for _, t in uses}
        if len(texts) > 1:
            collisions.append('%s: %s share %s' % (slug, ', '.join('%s %r' % u for u in uses), qid))
    return ids, collisions


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('slug', choices=sorted(RECIPES))
    ap.add_argument('--id', help='print only this id')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    try:
        ids, collisions = decode(args.slug)
    except (OSError, ValueError) as exc:
        print('FAIL: %s' % exc)
        return 1
    if args.json:
        print(json.dumps({k: [{'where': w, 'text': t} for w, t in v] for k, v in sorted(ids.items())},
                         ensure_ascii=False, indent=1))
    else:
        for qid, uses in sorted(ids.items()):
            if args.id and qid != args.id:
                continue
            for where, text in uses:
                print('%s\t%s\t%s' % (qid, where, text))
        if args.id and args.id not in ids:
            print('%s: not a %s question' % (args.id, args.slug))
    for c in collisions:
        print('COLLISION: %s' % c, file=sys.stderr)
    n = sum(len(v) for v in ids.values())
    print('%s: %d questions, %d ids, %d collisions' % (args.slug, n, len(ids), len(collisions)), file=sys.stderr)
    return 1 if collisions or (args.id and args.id not in ids) else 0


if __name__ == '__main__':
    raise SystemExit(main())
