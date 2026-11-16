#!/usr/bin/env python3
"""Answer audit, pilot: Claude solves every question of 21 games without seeing the game's key, and every
disagreement is reported for review (contract ANSWER-AUDIT-PILOT, Jon, 16 Nov 2026).

WHAT IT DOES
------------
Each game's own verifier was written alongside its bank and can share its author's mistake. This is a second,
independent solver. For every question of the games in FIELD_MAP it builds the question as the student reads it
(the text fields, the options if multiple choice, the level), never the key and never a field that gives the
answer away, and asks Claude to solve it, ending on one fixed line, "FINAL: <answer>".

  Pass 1  every question, claude-sonnet-5-5, one Message Batch.
  Pass 2  only pass 1's DISAGREE and UNCLEAR items, re-solved by claude-opus-5-5 in a second batch.

Final status per item: AGREE (pass 1 agreed with the key), RESOLVED (pass 1 did not, Opus agrees with the key),
DISAGREE (Opus disagrees too), UNCLEAR (a reply that cannot be compared), ERROR (the request failed or was
refused). A DISAGREE IS A LEAD FOR REVIEW, NOT A VERDICT: Claude can be wrong, a question can be ambiguous, and
Project Claude and Jon triage every one against the game before anything changes.

It never runs in CI: it declares no ci-line, and it needs Jon's own API key.

THE 21 GAMES (unique questions in data/banks/ on 16 Nov 2026; a bank served at several levels is counted once)
---------------------------------------------------------------------------------------------------------
  angle-ace 85 (every question needs its figure: none sent)    binomial-blaster 100
  coordinate-geometry-dash 45                                  core-maths-paper1 36 (4 need their chart)
  core-maths-paper2a 36 (1 needs its chart)                    core-maths-paper2b 36
  core-maths-paper2c 36                                        curling-friction 76
  fermi-lab 65                                                 force-resolver 72
  log-laws 45                                                  moments-master 69
  normal-navigator 47 (every question draws its curve: none)   partial-fractions-duel 50
  probability-paradox 38                                       proportion-blaster 100
  screening-room 70                                            standard-form-blitz 100
  surd-simplifier 100                                          trig-identity-duel 99
  truth-buster 60
  1,365 in all; 137 are excluded as "not audited: needs its figure", so 1,228 are sent.

The per-game knowledge (which fields make the question, which are the options and the key, which give the
answer away, which hold a figure) lives only in FIELD_MAP below. A game not in it is never sent. A question
that carries one of its game's figure fields is never sent and is listed in the report as "not audited: needs
its figure". Before anything is sent, every request is checked: no stripped field's text and, for a typed
answer, no form of the key may appear in it; a request that fails is refused, never sent.

HOW TO RUN (on Jon's PC; Python 3.10+, `pip install anthropic`)
---------------------------------------------------------------
  0. The banks: python -X utf8 scripts/extract-banks.py   (writes data/banks/<slug>.json; the audit says which
     game's file is missing and stops if one is).
  1. The key: create an API key in the Claude Console, put it alone in ~/.config/maffs/anthropic-audit-key, and
     `chmod 600` it. The script reads the key only from that file (--key-file to move it), refuses it unless its
     mode is 600 and it is outside the repository, and never prints, logs or writes it. It never reads
     ANTHROPIC_API_KEY: a key in the shell would make Claude Code bill the API instead of Jon's plan, and passing
     the key to the SDK explicitly stops the SDK consulting the environment for credentials.
  2. Dry run, always first:  python -X utf8 scripts/audit-answers.py --dry-run
     Builds every request, prints counts per game and the estimated cost, sends nothing.
  3. One game:  python -X utf8 scripts/audit-answers.py --game surd-simplifier
  4. All 21:    python -X utf8 scripts/audit-answers.py
  Interrupted? Each batch's id is printed and saved in data/audit/<run>/state.json; resume pass 1 with
  --batch-id <id> (and pass 2 with --pass2-batch-id <id>) and the same --game arguments.

WHAT IT COSTS
-------------
Batch prices are half the standard rate: Sonnet 5.5 $1 in / $5 out, Opus 5.5 $2 in / $10 out, per million
tokens. Output dominates and includes the model's thinking. The dry run estimates input from the request's
length (3 characters a token, on the high side) and output from an assumed average (--assume-out1, default 2,000
tokens; --assume-out2, default 4,000): about $13 for pass 1 over the 1,228 questions, and at most about $50 for
pass 2 if every question disagreed (in practice a small fraction). The real run refuses to start pass 1 if its
estimate exceeds --max-usd (default 50), and refuses pass 2 if pass 1's actual cost plus pass 2's estimate would.
The report gives the actual tokens and cost of each pass from the API's usage figures, and the average output
per question, so the next dry run can use real figures. max_tokens caps each reply (8,000 pass 1, 16,000 pass 2).

OUTPUT
------
docs/audits/answer-audit-<date>.md (not committed by this task): per game the counts (sent, excluded for a
figure, agree, resolved, disagree, unclear, error), then every DISAGREE and UNCLEAR with slug, level, index (into
the bank's array), the question as sent, the game's key, both models' answers and Opus's working; then each pass's
tokens and cost. Raw requests and results: data/audit/<run>/ (gitignored).

custom_id: the contract names "<slug>|<level>|<index>"; the Batch API allows only letters, digits, "_" and "-"
in a custom_id, so it is sent as "<slug>--<level>--<index>" (anything else made "_") and the manifest maps it back.

    python scripts/audit-answers.py [--dry-run] [--game SLUG ...] [--max-usd N] [--key-file PATH]
                                    [--batch-id ID] [--pass2-batch-id ID] [--selftest]
"""
import argparse
import datetime
import hashlib
import html
import json
import os
import re
import stat
import sys
import tempfile
import time
from types import SimpleNamespace

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BANKS = os.path.join(REPO, 'data', 'banks')
AUDIT = os.path.join(REPO, 'data', 'audit')
REPORTS = os.path.join(REPO, 'docs', 'audits')
DEFAULT_KEY_FILE = os.path.join('~', '.config', 'maffs', 'anthropic-audit-key')

PASS1_MODEL, PASS2_MODEL = 'claude-sonnet-5-5', 'claude-opus-5-5'
# Batch prices, US dollars per million tokens (half the standard rate).
BATCH_PRICE = {PASS1_MODEL: (1.0, 5.0), PASS2_MODEL: (2.0, 10.0)}
MAX_TOKENS = {1: 8000, 2: 16000}
EFFORT = {1: 'medium', 2: 'high'}
CHARS_PER_TOKEN = 3.0

# ── The per-game knowledge, in one place ─────────────────────────────────────────────────────────────────────
# text:    the fields that make the question, in the order the student reads them (a string field, an HTML
#          field, a table dict, or a fermi chain); "label: field" puts a label before it.
# kind:    'mc_plus'   options = [key] + the distractor field, shuffled (the game shuffles them too);
#          'mc_list'   options = the options field; the key is one of its values; accept = other values the
#                      game also accepts;
#          'mc_index'  options = the options field, in its order; the key is an index; accept = more indices;
#          'truefalse' the key is a boolean;
#          'percent_dp' a typed percentage to the question's dp; the game's accepted keys are integers of 10^-dp %;
#          'fermi'     a Fermi estimate; agreement is within the game's own "Good" band (a factor of 5).
# strip:   fields that give the answer away; never sent, and the leak check proves their text is absent.
# figure:  fields that hold a figure or diagram; a question carrying one is never sent.
FIELD_MAP = {
    'angle-ace': dict(text=['prompt'], kind='mc_list', options='angleOpts', key='answer',
                      strip=['steps', 'reason', 'misconception', 'multiReason', 'recognitionOpts'], figure=['fig']),
    'binomial-blaster': dict(text=['ask', 'q'], kind='mc_plus', options='d', key='correct', strip=[], figure=[]),
    'coordinate-geometry-dash': dict(text=['ctx', 'q'], kind='mc_list', options='opts', key='correct',
                                     strip=['steps', 'misconception'], figure=[]),
    'core-maths-paper1': dict(text=['stem', 'table', 'stemAfterTable'], kind='mc_index', options='options',
                              key='correct', accept='accept', strip=['working'], figure=['svg']),
    'core-maths-paper2a': dict(text=['stem', 'table', 'stemAfterTable'], kind='mc_index', options='options',
                               key='correct', accept='accept', strip=['working'], figure=['svg']),
    'core-maths-paper2b': dict(text=['stem', 'table', 'stemAfterTable'], kind='mc_index', options='options',
                               key='correct', accept='accept', strip=['working'], figure=['svg']),
    'core-maths-paper2c': dict(text=['stem', 'table', 'stemAfterTable'], kind='mc_index', options='options',
                               key='correct', accept='accept', strip=['working'], figure=['svg']),
    'curling-friction': dict(text=['ctx', 'q', 'ask'], kind='mc_plus', options='d', key='correct', strip=[],
                             figure=[]),
    'fermi-lab': dict(text=['question', 'chain'], kind='fermi', key='acceptedAnswer',
                      strip=['answerNote', 'answerFig', 'answerFigScale', 'eval_question', 'eval_answer'], figure=[]),
    'force-resolver': dict(text=['ctx', 'q', 'ask'], kind='mc_plus', options='d', key='correct', strip=[], figure=[]),
    # The game shows the rule's name above the expression, then "<q> = ?", then the key and its first three
    # distractors (log-laws index.html, showQuestion).
    'log-laws': dict(text=['Rule: rule', 'q'], q_suffix=' = ?', kind='mc_plus', options='distractors', max_d=3,
                     key='correct', strip=['exp'], figure=[]),
    'moments-master': dict(text=['ctx', 'q', 'ask'], kind='mc_plus', options='d', key='correct', strip=[], figure=[]),
    'normal-navigator': dict(text=['ctx', 'q'], kind='mc_list', options='opts', key='correct',
                             strip=['steps', 'misconception'], figure=['shade']),
    'partial-fractions-duel': dict(text=['q', 'ask'], kind='mc_plus', options='d', key='correct', strip=[], figure=[]),
    'probability-paradox': dict(text=['scenario', 'q'], kind='mc_list', options='opts', key='correct', accept='accept',
                                strip=['steps', 'explain', 'misconception'], figure=[]),
    'proportion-blaster': dict(text=['ctx', 'q', 'ask'], kind='mc_plus', options='d', key='correct', strip=[],
                               figure=[]),
    # Phase 3, the typed answer: the game shows the context and the scenario, then "Of the <N> positive results,
    # what percentage are real?" and "Give your answer as a percentage to <dp> decimal place(s)" (index.html, the
    # calcPrompt and calcHint lines); N is on screen from phase 2.
    'screening-room': dict(text=['context', 'scenarioText'], kind='percent_dp', key='keys',
                           strip=['explanation', 'explanationText', 'answerText', 'answerTex', 'bayesTex'], figure=[]),
    'standard-form-blitz': dict(text=['ask', 'q'], kind='mc_plus', options='d', key='correct', strip=[], figure=[]),
    'surd-simplifier': dict(text=['ask', 'q'], kind='mc_plus', options='d', key='correct', strip=[], figure=[]),
    'trig-identity-duel': dict(text=['ctx', 'q', 'ask'], kind='mc_plus', options='d', key='correct', strip=[],
                               figure=[]),
    'truth-buster': dict(text=['statement'], kind='truefalse', key='answer',
                         strip=['revealTitle', 'revealText', 'counterexample'], figure=[]),
}

SYSTEM = """You are independently checking the answers in a maths revision game for UK students (KS3 to A-Level, \
Core Maths and Level 4). Solve the question yourself, carefully, as an expert. Text between $...$ or written as \
LaTeX is KaTeX source that the student sees rendered.

Show brief working (a few lines). Then end your reply with exactly one final line in this form:
FINAL: <answer>

- Multiple choice: <answer> is the letter of the correct option, e.g. "FINAL: B". If more than one option is \
correct, give every correct letter separated by commas, e.g. "FINAL: B, D". If no option is correct, write \
"FINAL: NONE".
- True or false: "FINAL: TRUE" if the statement is always true, otherwise "FINAL: FALSE".
- A number: the number only, in the form and precision the question asks for, e.g. "FINAL: 25.8".
Nothing may follow the FINAL line."""

LETTERS = 'ABCDEFGHIJ'


class AuditError(Exception):
    """A refusal: the run stops and nothing more is sent."""


# ── Building the questions ───────────────────────────────────────────────────────────────────────────────────
def plain(s):
    """HTML as the student reads it: tags dropped, entities decoded; KaTeX source kept as it is."""
    s = re.sub(r'<br\s*/?>', '\n', str(s), flags=re.I)
    s = re.sub(r'<[^>]+>', '', s)
    return html.unescape(s).strip()


def table_text(t):
    if not isinstance(t, dict) or not t.get('rows'):
        return ''
    head = [plain(h) for h in t.get('headers', [])]
    out = []
    if head:
        out += ['| ' + ' | '.join(head) + ' |', '|' + '---|' * len(head)]
    out += ['| ' + ' | '.join(plain(c) for c in row) + ' |' for row in t['rows']]
    return '\n'.join(out)


def chain_text(chain):
    """A Fermi chain's steps as the student sees them: label, unit and hint, never the reference or tolerance."""
    lines = ['Work it out in these steps:']
    for k, st in enumerate(chain or [], 1):
        unit = (' (%s)' % st['unit']) if st.get('unit') else ''
        hint = (' Hint: %s' % st['hint']) if st.get('hint') else ''
        lines.append('%d. %s%s.%s' % (k, plain(st.get('label', '')), unit, hint))
    lines.append('Give your final estimate as a single number.')
    return '\n'.join(lines)


def field_text(q, spec, entry):
    label, _, name = spec.rpartition(': ')
    v = q.get(name)
    if v in (None, '', [], {}):
        return ''
    if name == 'chain':
        s = chain_text(v)
    elif isinstance(v, dict):
        s = table_text(v)
    else:
        s = plain(v)
        if name == 'q' and entry.get('q_suffix'):
            s += entry['q_suffix']
    return (label + ': ' + s) if (label and s) else s


def shuffled(options, seed):
    """The options in an order fixed by the item, so the key is not always first (the games shuffle too)."""
    return sorted(options, key=lambda o: hashlib.sha256((seed + '\x00' + str(o)).encode('utf-8')).hexdigest())


def norm(s):
    """A normalised string: KaTeX spacing commands, spaces and case ignored."""
    s = plain(str(s)).lower()
    s = re.sub(r'\\[,;:! ]|\\quad|\\qquad', '', s)
    s = s.replace('\\dfrac', '\\frac').replace('\\tfrac', '\\frac').replace('\\left', '').replace('\\right', '')
    return re.sub(r'\s+', '', s)


def flat_strings(v):
    if isinstance(v, str):
        yield v
    elif isinstance(v, dict):
        for x in v.values():
            yield from flat_strings(x)
    elif isinstance(v, (list, tuple)):
        for x in v:
            yield from flat_strings(x)


def make_item(slug, entry, level, index, q, all_levels):
    shown = {spec.rpartition(': ')[2] for spec in entry['text']} | {entry.get('options'), entry['key']}
    if shown & set(entry['strip']):
        raise AuditError('%s: field %s is both shown and stripped' % (slug, ', '.join(sorted(shown & set(entry['strip'])))))
    seed = '%s|%s|%d' % (slug, level, index)
    parts = [field_text(q, f, entry) for f in entry['text']]
    text = '\n\n'.join(p for p in parts if p)
    kind = entry['kind']
    item = dict(slug=slug, level=level, index=index, kind=kind, key_id=seed, levels=all_levels, text=text,
                options=None, accept=None, key_display='')
    if kind == 'mc_plus':
        d = list(q.get(entry['options']) or [])[:entry.get('max_d', 99)]
        opts = shuffled([q[entry['key']]] + d, seed)
        item.update(options=opts, accept=[i for i, o in enumerate(opts) if norm(o) == norm(q[entry['key']])],
                    key_display=str(q[entry['key']]))
    elif kind == 'mc_list':
        opts = list(q[entry['options']])
        good = [q[entry['key']]] + list(q.get(entry.get('accept') or '', None) or [])
        item.update(options=opts, accept=[i for i, o in enumerate(opts) if any(norm(o) == norm(g) for g in good)],
                    key_display=str(q[entry['key']]))
    elif kind == 'mc_index':
        opts = list(q[entry['options']])
        acc = sorted(set([int(q[entry['key']])] + [int(a) for a in (q.get(entry.get('accept') or '') or [])]))
        item.update(options=opts, accept=acc, key_display='%s) %s' % (LETTERS[acc[0]], opts[acc[0]]))
    elif kind == 'truefalse':
        item.update(key=bool(q[entry['key']]), key_display='TRUE' if q[entry['key']] else 'FALSE')
    elif kind == 'percent_dp':
        dp = int(q['dp'])
        ex = [None, '12.5', '1.25', '0.125'][dp] if dp in (1, 2, 3) else '12'
        item['text'] += ('\n\nOf the %s positive results, what percentage are real? Calculate P(condition | positive).'
                         '\nGive your answer as a percentage to %d decimal place%s (e.g. %s).'
                         % ('{:,}'.format(q['testPositive']['total']), dp, '' if dp == 1 else 's', ex))
        keys = [int(k) for k in q[entry['key']]]
        item.update(dp=dp, keys=keys, key_display=' or '.join('%.*f%%' % (dp, k / 10 ** dp) for k in keys))
    elif kind == 'fermi':
        item.update(key=float(q[entry['key']]), key_display='{:,}'.format(q[entry['key']]))
    else:
        raise AuditError('%s: unknown kind %r' % (slug, kind))
    if item['options'] is not None and not item['accept']:
        raise AuditError('%s %s #%d: the key is not among its options' % (slug, level, index))
    item['stripped'] = [s for f in entry['strip'] for s in flat_strings(q.get(f))]
    # What the student sees: a stripped line that only repeats it (a working line restating the question's data,
    # or ending on an option's own words) is not a leak.
    item['visible'] = norm(item['text']) + '\x00' + '\x00'.join(norm(o) for o in (item['options'] or []))
    return item


def group_label(variable, path, levels, multi_var):
    if path:
        return '.'.join(str(p) for p in path)
    return variable if multi_var else levels[0]


def load_items(games, field_map=None, banks=BANKS):
    """Every mapped question, once each: (items to send, excluded for a figure, excluded for shape, skipped)."""
    field_map = FIELD_MAP if field_map is None else field_map
    items, figure, shape, skipped = [], [], [], []
    for slug in games:
        entry = field_map.get(slug)
        if entry is None:
            skipped.append(slug)           # an unmapped game is never sent
            continue
        path = os.path.join(banks, slug + '.json')
        if not os.path.exists(path):
            raise AuditError('%s is missing: run  python -X utf8 scripts/extract-banks.py --only %s  first'
                             % (os.path.relpath(path, REPO), slug))
        with open(path, encoding='utf-8') as f:
            bank = json.load(f)
        groups = {}
        for lv, L in bank.get('levels', {}).items():
            for g in L.get('groups', []):
                k = (g['variable'], tuple(g['path']))
                if k not in groups:
                    groups[k] = [g, []]
                groups[k][1].append(lv)
        multi_var = len({v for v, _ in groups}) > 1
        for (variable, path), (g, lvs) in groups.items():
            label = group_label(variable, path, lvs, multi_var)
            for i, q in enumerate(g['questions']):
                where = dict(slug=slug, level=label, index=i)
                if any(q.get(f) not in (None, '', False, [], {}) for f in entry['figure']):
                    figure.append(dict(where, text=plain(next((q[f] for f in entry['text'] if isinstance(q.get(f), str) and q.get(f)), ''))[:160]))
                    continue
                try:
                    # The level the student plays it at: the bank's own level where it is keyed by one,
                    # otherwise every level query that serves it.
                    items.append(make_item(slug, entry, label, i, q, [label] if path else lvs))
                except (KeyError, TypeError, ValueError, IndexError) as e:
                    shape.append(dict(where, why='%s: %s' % (type(e).__name__, e)))
    return items, figure, shape, skipped


# ── Requests, the leak check and cost ────────────────────────────────────────────────────────────────────────
def custom_id(item):
    cid = re.sub(r'[^A-Za-z0-9_-]', '_', '%s--%s--%d' % (item['slug'], item['level'], item['index']))
    if len(cid) > 64:
        cid = cid[:51] + '-' + hashlib.sha256(cid.encode()).hexdigest()[:12]
    return cid


def user_text(item):
    lines = ['Level: %s' % ', '.join(item['levels']), '', item['text']]
    if item['options'] is not None:
        lines += ['', 'Options:'] + ['%s) %s' % (LETTERS[i], plain(o)) for i, o in enumerate(item['options'])]
    elif item['kind'] == 'truefalse':
        lines += ['', 'Is this statement always true? Answer TRUE or FALSE.']
    return '\n'.join(lines)


def build_request(item, pass_no):
    model = PASS1_MODEL if pass_no == 1 else PASS2_MODEL
    params = dict(model=model, max_tokens=MAX_TOKENS[pass_no], system=SYSTEM,
                  output_config={'effort': EFFORT[pass_no]},
                  messages=[{'role': 'user', 'content': user_text(item)}])
    return dict(custom_id=custom_id(item), params=params)


def key_forms(item):
    """Every way a typed answer's key could be written; MC keys are among the options by design."""
    if item['kind'] == 'percent_dp':
        out = set()
        for k in item['keys']:
            v = k / 10 ** item['dp']
            out |= {'%.*f%%' % (item['dp'], v), '%.*f %%' % (item['dp'], v), '= %.*f' % (item['dp'], v),
                    '%.*f' % (item['dp'] + 2, v / 100)}
        return out
    if item['kind'] == 'fermi':
        v = item['key']
        return {'{:,}'.format(int(v)) if v >= 1000 else None, str(int(v)) if v >= 100 and v == int(v) else None} - {None}
    return set()


def leak_check(item, req):
    """Refuse a request that carries a stripped field's text or a typed answer's key."""
    body = req['params']['system'] + '\n' + req['params']['messages'][0]['content']
    flat = norm(body)
    for s in item['stripped']:
        ns = norm(s)
        if len(ns) >= 8 and ns in flat and ns not in item['visible']:
            raise AuditError('%s: a stripped field is in the request: %r' % (req['custom_id'], s[:60]))
    for k in key_forms(item):
        if k in body:
            raise AuditError('%s: the key (%s) is in the request' % (req['custom_id'], k))


def estimate(reqs, pass_no, assume_out):
    inp, out = BATCH_PRICE[PASS1_MODEL if pass_no == 1 else PASS2_MODEL]
    tin = sum((len(r['params']['system']) + len(r['params']['messages'][0]['content'])) / CHARS_PER_TOKEN for r in reqs)
    tout = assume_out * len(reqs)
    return (tin * inp + tout * out) / 1e6, int(tin), tout


def cost_of(usage, pass_no):
    inp, out = BATCH_PRICE[PASS1_MODEL if pass_no == 1 else PASS2_MODEL]
    return (usage['input_tokens'] * inp + usage['output_tokens'] * out) / 1e6


# ── Comparing a reply with the key ───────────────────────────────────────────────────────────────────────────
FINAL = re.compile(r'^\s*\**FINAL\**\s*:\s*(.+?)\s*$', re.I | re.M)


def final_answer(text):
    found = FINAL.findall(text or '')
    if not found:
        return None
    return found[-1].strip().strip('*').strip().rstrip('.')


def number(s):
    s = s.replace(',', '').replace('%', '').replace('\u2212', '-').strip()
    m = re.fullmatch(r'[-+]?(\d+(\.\d*)?|\.\d+)(e[-+]?\d+)?', s, re.I)
    return float(s) if m else None


def classify(item, text):
    """AGREE, DISAGREE or UNCLEAR, and the answer as read. Never agreement on doubt."""
    a = final_answer(text)
    if a is None:
        return 'UNCLEAR', ''
    if item['options'] is not None:
        if a.upper() == 'NONE':
            return 'DISAGREE', 'NONE'
        picks = [p.strip().upper().strip('()') for p in re.split(r'[,&]|\band\b', a)]
        n = len(item['options'])
        if not picks or any(len(p) != 1 or p not in LETTERS[:n] for p in picks):
            return 'UNCLEAR', a
        got = {LETTERS.index(p) for p in picks}
        shown = ', '.join('%s) %s' % (LETTERS[i], plain(item['options'][i])) for i in sorted(got))
        return ('AGREE' if got <= set(item['accept']) else 'DISAGREE'), shown
    if item['kind'] == 'truefalse':
        if a.upper() not in ('TRUE', 'FALSE'):
            return 'UNCLEAR', a
        return ('AGREE' if (a.upper() == 'TRUE') == item['key'] else 'DISAGREE'), a.upper()
    v = number(a)
    if v is None:
        return 'UNCLEAR', a
    if item['kind'] == 'percent_dp':
        scaled = int(v * 10 ** item['dp'] + 0.5 + 1e-9)          # half up at the question's stated precision
        return ('AGREE' if scaled in item['keys'] else 'DISAGREE'), a
    if item['kind'] == 'fermi':
        if v <= 0:
            return 'UNCLEAR', a
        factor = max(v / item['key'], item['key'] / v)
        return ('AGREE' if factor <= 5 else 'DISAGREE'), a
    return ('AGREE' if norm(a) == norm(item.get('key', '')) else 'UNCLEAR'), a


# ── The key file ─────────────────────────────────────────────────────────────────────────────────────────────
def read_key(path):
    """The API key, from the key file only. Refused unless the file is mode 600 and outside the repository."""
    p = os.path.realpath(os.path.expanduser(path))
    if not os.path.isfile(p):
        raise AuditError('no key file at %s (create it, then chmod 600)' % path)
    if p == REPO or p.startswith(REPO + os.sep):
        raise AuditError('the key file must be outside the repository')
    mode = stat.S_IMODE(os.stat(p).st_mode)
    if mode != 0o600:
        raise AuditError('the key file must be mode 600 (it is %03o): chmod 600 %s' % (mode, path))
    with open(p, encoding='utf-8') as f:
        key = f.read().strip()
    if not key:
        raise AuditError('the key file is empty')
    return key


def make_client(key_file):
    import anthropic                       # only for a real run: --selftest and --dry-run need no SDK
    # An explicit api_key: the SDK then consults no environment variable for credentials.
    return anthropic.Anthropic(api_key=read_key(key_file))


# ── Batches ──────────────────────────────────────────────────────────────────────────────────────────────────
def norm_result(r):
    res = r.result
    out = dict(custom_id=r.custom_id, type=res.type, text='', stop_reason=None, input_tokens=0, output_tokens=0,
               error=None)
    if res.type == 'succeeded':
        msg = res.message
        out['text'] = '\n'.join(b.text for b in msg.content if getattr(b, 'type', '') == 'text')
        out['stop_reason'] = msg.stop_reason
        out['input_tokens'] = msg.usage.input_tokens or 0
        out['output_tokens'] = msg.usage.output_tokens or 0
    elif res.type == 'errored':
        err = getattr(res, 'error', None)
        out['error'] = str(getattr(getattr(err, 'error', err), 'message', err))
    return out


def run_batch(client, reqs, pass_no, run_dir, state, resume_id, poll):
    key = 'pass%d_batch' % pass_no
    if resume_id:
        bid = resume_id
        print('pass %d: resuming batch %s' % (pass_no, bid))
    else:
        batch = client.messages.batches.create(requests=reqs)
        bid = batch.id
        print('pass %d: batch %s created (%d requests)' % (pass_no, bid, len(reqs)))
    state[key] = bid
    save_json(os.path.join(run_dir, 'state.json'), state)
    while True:
        b = client.messages.batches.retrieve(bid)
        if b.processing_status == 'ended':
            break
        rc = b.request_counts
        print('  %s: processing %s, succeeded %s, errored %s' % (b.processing_status, rc.processing, rc.succeeded,
                                                                 rc.errored))
        time.sleep(poll)
    results = {}
    with open(os.path.join(run_dir, 'pass%d-results.jsonl' % pass_no), 'w', encoding='utf-8') as f:
        for r in client.messages.batches.results(bid):
            n = norm_result(r)
            results[n['custom_id']] = n
            f.write(json.dumps(n, ensure_ascii=False) + '\n')
    return results


def outcome(item, res):
    """(status, answer) for one result; a failed or refused request is ERROR."""
    if res is None:
        return 'ERROR', 'no result'
    if res['type'] != 'succeeded':
        return 'ERROR', res['type'] + (': ' + res['error'] if res.get('error') else '')
    if res['stop_reason'] == 'refusal':
        return 'ERROR', 'refused'
    if res['stop_reason'] == 'max_tokens':
        return 'UNCLEAR', 'cut off at max_tokens'
    return classify(item, res['text'])


def save_json(path, obj):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


# ── The run ──────────────────────────────────────────────────────────────────────────────────────────────────
def build_all(items, pass_no):
    reqs = []
    seen = set()
    for it in items:
        r = build_request(it, pass_no)
        leak_check(it, r)
        if r['custom_id'] in seen:
            raise AuditError('two questions share custom_id %s' % r['custom_id'])
        seen.add(r['custom_id'])
        reqs.append(r)
    return reqs


def audit(args, client_factory=make_client, out=print, banks=BANKS, field_map=None, audit_dir=AUDIT,
          reports=REPORTS, poll=60):
    field_map = FIELD_MAP if field_map is None else field_map
    games = args.game or sorted(field_map)
    items, figure, shape, skipped = load_items(games, field_map, banks)
    for s in skipped:
        out('%s: not in FIELD_MAP, never sent' % s)
    reqs = build_all(items, 1)
    by_id = {r['custom_id']: it for r, it in zip(reqs, items)}
    est1, tin1, tout1 = estimate(reqs, 1, args.assume_out1)
    est2, _, _ = estimate(build_all(items, 2), 2, args.assume_out2)
    out('%-26s %6s %8s %6s' % ('game', 'sent', 'figure', 'shape'))
    for slug in games:
        if slug in field_map:
            out('%-26s %6d %8d %6d' % (slug, sum(1 for i in items if i['slug'] == slug),
                                       sum(1 for f in figure if f['slug'] == slug),
                                       sum(1 for f in shape if f['slug'] == slug)))
    out('total: %d to send, %d not audited (need their figure), %d not audited (shape)'
        % (len(items), len(figure), len(shape)))
    for s in shape:
        out('  shape: %s %s #%d: %s' % (s['slug'], s['level'], s['index'], s['why']))
    cap1 = len(reqs) * MAX_TOKENS[1] * BATCH_PRICE[PASS1_MODEL][1] / 1e6
    out('pass 1 (%s): ~%d input + ~%d output tokens (assumed %d a reply): estimated $%.2f (hard ceiling at max_tokens $%.2f)'
        % (PASS1_MODEL, tin1, tout1, args.assume_out1, est1, cap1))
    out('pass 2 (%s), worst case, every question re-solved: estimated $%.2f; at 15%% of questions: $%.2f'
        % (PASS2_MODEL, est2, est2 * 0.15))
    out('--max-usd %.2f: pass 1 starts only under it; pass 2 only if pass 1 actual + pass 2 estimate is under it'
        % args.max_usd)
    if args.dry_run:
        out('dry run: nothing sent')
        return dict(items=items, figure=figure, shape=shape, est1=est1, est2=est2, sent=False)
    if est1 > args.max_usd:
        raise AuditError('pass 1 estimate $%.2f exceeds --max-usd %.2f: refused, nothing sent' % (est1, args.max_usd))
    client = client_factory(args.key_file)
    run = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
    run_dir = os.path.join(audit_dir, run)
    os.makedirs(run_dir, exist_ok=True)
    save_json(os.path.join(run_dir, 'manifest.json'),
              [dict(custom_id=r['custom_id'], key='%s|%s|%d' % (it['slug'], it['level'], it['index']),
                    request=r) for r, it in zip(reqs, items)])
    state = {}
    res1 = run_batch(client, reqs, 1, run_dir, state, args.batch_id, poll)
    usage1 = dict(input_tokens=sum(r['input_tokens'] for r in res1.values()),
                  output_tokens=sum(r['output_tokens'] for r in res1.values()))
    spent = cost_of(usage1, 1)
    rows = {}
    for cid, it in by_id.items():
        st, ans = outcome(it, res1.get(cid))
        rows[cid] = dict(item=it, p1=st, a1=ans, t1=(res1.get(cid) or {}).get('text', ''), p2=None, a2='', t2='')
    again = [rows[c]['item'] for c in rows if rows[c]['p1'] in ('DISAGREE', 'UNCLEAR')]
    usage2 = dict(input_tokens=0, output_tokens=0)
    if again:
        reqs2 = build_all(again, 2)
        est2a, _, _ = estimate(reqs2, 2, args.assume_out2)
        out('pass 1: $%.2f actual; %d to re-solve in pass 2, estimated $%.2f' % (spent, len(again), est2a))
        if spent + est2a > args.max_usd:
            raise AuditError('pass 1 actual $%.2f + pass 2 estimate $%.2f exceeds --max-usd %.2f: pass 2 refused '
                             '(pass 1 results are in %s)' % (spent, est2a, args.max_usd, run_dir))
        res2 = run_batch(client, reqs2, 2, run_dir, state, args.pass2_batch_id, poll)
        usage2 = dict(input_tokens=sum(r['input_tokens'] for r in res2.values()),
                      output_tokens=sum(r['output_tokens'] for r in res2.values()))
        for r in reqs2:
            row = rows[r['custom_id']]
            st, ans = outcome(row['item'], res2.get(r['custom_id']))
            row.update(p2=st, a2=ans, t2=(res2.get(r['custom_id']) or {}).get('text', ''))
    for row in rows.values():
        row['final'] = final_status(row)
    save_json(os.path.join(run_dir, 'statuses.json'),
              {c: dict(final=r['final'], p1=r['p1'], a1=r['a1'], p2=r['p2'], a2=r['a2']) for c, r in rows.items()})
    path = write_report(rows, figure, shape, games, field_map, usage1, usage2, reports, run_dir)
    out('report: %s' % os.path.relpath(path, REPO))
    return dict(rows=rows, sent=True, report=path)


def final_status(row):
    if row['p1'] == 'AGREE':
        return 'AGREE'
    if row['p1'] == 'ERROR':
        return 'ERROR'
    return {'AGREE': 'RESOLVED', 'DISAGREE': 'DISAGREE'}.get(row['p2'], 'UNCLEAR' if row['p2'] != 'ERROR' else 'ERROR')


def cell(s, n=600):
    s = str(s).replace('\r', '').replace('|', '\\|').replace('\n', '<br>')
    return s if len(s) <= n else s[:n] + '…'


def write_report(rows, figure, shape, games, field_map, usage1, usage2, reports, run_dir):
    os.makedirs(reports, exist_ok=True)
    path = os.path.join(reports, 'answer-audit-%s.md' % datetime.date.today().isoformat())
    S = ('AGREE', 'RESOLVED', 'DISAGREE', 'UNCLEAR', 'ERROR')
    L = ['# Answer audit, pilot (%s)' % datetime.date.today().isoformat(), '',
         'Made by `scripts/audit-answers.py` (contract ANSWER-AUDIT-PILOT). Pass 1 %s, pass 2 %s on pass 1\'s '
         'DISAGREE and UNCLEAR. **A DISAGREE is a lead for review, not a verdict.** Raw results: `%s`.'
         % (PASS1_MODEL, PASS2_MODEL, os.path.relpath(run_dir, REPO)), '',
         '| Game | Sent | Excluded (figure) | ' + ' | '.join(s.title() for s in S) + ' |',
         '|---|---|---|' + '---|' * len(S)]
    for slug in games:
        if slug not in field_map:
            continue
        mine = [r for r in rows.values() if r['item']['slug'] == slug]
        L.append('| %s | %d | %d | %s |' % (slug, len(mine), sum(1 for f in figure if f['slug'] == slug),
                                            ' | '.join(str(sum(1 for r in mine if r['final'] == s)) for s in S)))
    L += ['', '## Disagreements and unclear replies', '',
          '| Status | Slug | Level | Index | Question as sent | Game key | Sonnet | Opus | Opus working |',
          '|---|---|---|---|---|---|---|---|---|']
    for r in sorted(rows.values(), key=lambda r: (r['final'], r['item']['slug'], r['item']['level'], r['item']['index'])):
        if r['final'] not in ('DISAGREE', 'UNCLEAR'):
            continue
        it = r['item']
        L.append('| %s | %s | %s | %d | %s | %s | %s | %s | %s |' % (
            r['final'], it['slug'], it['level'], it['index'], cell(user_text(it), 900), cell(it['key_display']),
            cell(r['a1']), cell(r['a2'] or '—'), cell(r['t2'] or r['t1'], 1200)))
    errs = [r for r in rows.values() if r['final'] == 'ERROR']
    if errs:
        L += ['', '## Errors', ''] + ['- %s %s #%d: pass 1 %s; pass 2 %s' % (
            r['item']['slug'], r['item']['level'], r['item']['index'], r['a1'], r['a2'] or '—') for r in errs]
    L += ['', '## Not audited: needs its figure', ''] + ['- %s %s #%d: %s' % (
        f['slug'], f['level'], f['index'], f['text']) for f in figure]
    if shape:
        L += ['', '## Not audited: unexpected shape', ''] + ['- %s %s #%d: %s' % (
            s['slug'], s['level'], s['index'], s['why']) for s in shape]
    n1 = max(1, len(rows))
    n2 = max(1, sum(1 for r in rows.values() if r['p2'] is not None))
    L += ['', '## Tokens and cost (from the API\'s usage figures, batch prices)', '',
          '| Pass | Model | Requests | Input tokens | Output tokens | Output a request | Cost |', '|---|---|---|---|---|---|---|',
          '| 1 | %s | %d | %d | %d | %d | $%.2f |' % (PASS1_MODEL, len(rows), usage1['input_tokens'],
                                                    usage1['output_tokens'], usage1['output_tokens'] // n1,
                                                    cost_of(usage1, 1)),
          '| 2 | %s | %d | %d | %d | %d | $%.2f |' % (PASS2_MODEL, sum(1 for r in rows.values() if r['p2'] is not None),
                                                    usage2['input_tokens'], usage2['output_tokens'],
                                                    usage2['output_tokens'] // n2, cost_of(usage2, 2)),
          '', 'Total: $%.2f.' % (cost_of(usage1, 1) + cost_of(usage2, 2))]
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
    return path


# ── Self-test: no network ────────────────────────────────────────────────────────────────────────────────────
class FakeClient:
    """Stands in for the SDK: answers from a table of replies, and records every call."""

    def __init__(self, replies):
        self.replies, self.calls, self.batches = replies, [], {}
        self.messages = SimpleNamespace(batches=self)

    def create(self, requests):
        self.calls.append(('create', len(requests)))
        bid = 'fake_%d' % len(self.batches)
        self.batches[bid] = requests
        return SimpleNamespace(id=bid)

    def retrieve(self, bid):
        self.calls.append(('retrieve', bid))
        return SimpleNamespace(processing_status='ended', request_counts=None)

    def results(self, bid):
        self.calls.append(('results', bid))
        for r in self.batches[bid]:
            model = r['params']['model']
            text = self.replies.get((r['custom_id'], model), self.replies.get(r['custom_id'], ''))
            msg = SimpleNamespace(content=[SimpleNamespace(type='text', text=text)], stop_reason='end_turn',
                                  usage=SimpleNamespace(input_tokens=100, output_tokens=200))
            yield SimpleNamespace(custom_id=r['custom_id'], result=SimpleNamespace(type='succeeded', message=msg))


def selftest():
    fails = []

    def check(what, ok):
        print('  %-66s %s' % (what, 'ok' if ok else '*** FAILED ***'))
        if not ok:
            fails.append(what)

    tmp = tempfile.mkdtemp(prefix='audit-selftest-')
    banks = os.path.join(tmp, 'banks')
    os.makedirs(banks)

    def bank(slug, groups):
        with open(os.path.join(banks, slug + '.json'), 'w', encoding='utf-8') as f:
            json.dump({'slug': slug, 'levels': {'gcse': {'groups': [
                {'variable': 'QUESTIONS', 'path': [p], 'count': len(qs), 'questions': qs} for p, qs in groups]}}}, f)

    bank('fake-mc', [('gcse', [
        {'q': '\\sqrt{12}', 'ask': 'Simplify', 'correct': '2\\sqrt{3}', 'd': ['3\\sqrt{2}', '4\\sqrt{3}', '\\sqrt{12}']},
        {'q': '\\sqrt{18}', 'ask': 'Simplify', 'correct': '9\\sqrt{2}', 'd': ['3\\sqrt{2}', '2\\sqrt{3}', '6']},     # wrong key
        {'q': '\\sqrt{8}', 'ask': 'Simplify', 'correct': '2\\sqrt{2}', 'd': ['4\\sqrt{2}', '\\sqrt{2}', '8'],
         'steps': ['8 = 4 x 2, so the square root is 2 root 2'], 'fig': {'t': 'square'}},                           # figure
        {'q': '\\sqrt{50}', 'ask': 'Simplify', 'correct': '5\\sqrt{2}', 'd': ['2\\sqrt{5}', '25\\sqrt{2}', '10']},   # unparseable
    ])])
    bank('fake-pct', [('gcse', [
        {'context': 'Test A', 'scenarioText': 'Of 1000 people, 10 are ill ...', 'testPositive': {'total': 59},
         'dp': 1, 'keys': [169], 'answerText': '16.9%', 'explanationText': 'Only 10 of the 59 positives are real here.'},
        {'context': 'Test B', 'scenarioText': 'Of 2000 people, 40 are ill ...', 'testPositive': {'total': 236},
         'dp': 1, 'keys': [153], 'answerText': '15.3%', 'explanationText': 'Only 36 of the 236 positives are real here.'},
    ])])
    bank('fake-unmapped', [('gcse', [{'q': 'x', 'correct': 'y', 'd': ['z']}])])
    fmap = {
        'fake-mc': dict(text=['ask', 'q'], kind='mc_plus', options='d', key='correct', strip=['steps'], figure=['fig']),
        'fake-pct': dict(text=['context', 'scenarioText'], kind='percent_dp', key='keys',
                         strip=['explanationText', 'answerText'], figure=[]),
    }
    items, figure, shape, skipped = load_items(['fake-mc', 'fake-pct', 'fake-unmapped'], fmap, banks)
    by = {(i['slug'], i['index']): i for i in items}
    check('a figure question is excluded, never built into a request', [(f['slug'], f['index']) for f in figure] ==
          [('fake-mc', 2)] and ('fake-mc', 2) not in by)
    check('an unmapped game is never sent', skipped == ['fake-unmapped'] and not any(i['slug'] == 'fake-unmapped' for i in items))
    reqs = build_all(items, 1)
    check('every built request passes the leak check', len(reqs) == len(items) == 5)

    def letter_of(it, value):
        return LETTERS[[norm(o) for o in it['options']].index(norm(value))]

    it0, it1, it3 = by[('fake-mc', 0)], by[('fake-mc', 1)], by[('fake-mc', 3)]
    p0, p1 = by[('fake-pct', 0)], by[('fake-pct', 1)]
    check('a correct item: AGREE', classify(it0, 'sqrt 12 = sqrt 4 sqrt 3\nFINAL: %s' % letter_of(it0, '2\\sqrt{3}'))[0] == 'AGREE')
    check('a wrong key: DISAGREE', classify(it1, 'sqrt 18 = 3 sqrt 2\nFINAL: %s' % letter_of(it1, '3\\sqrt{2}'))[0] == 'DISAGREE')
    check('no option correct: DISAGREE', classify(it1, 'FINAL: NONE')[0] == 'DISAGREE')
    check('two letters, one not the key: DISAGREE',
          classify(it0, 'FINAL: %s, %s' % (letter_of(it0, '2\\sqrt{3}'), letter_of(it0, '\\sqrt{12}')))[0] == 'DISAGREE')
    check('a numeric answer equal within the stated precision: AGREE', classify(p0, '10/59 = 16.949...\nFINAL: 16.9')[0] == 'AGREE'
          and classify(p0, 'FINAL: 16.949%')[0] == 'AGREE')
    check('a precision mismatch: DISAGREE', classify(p1, 'FINAL: 15.4')[0] == 'DISAGREE' and classify(p1, 'FINAL: 15')[0] == 'DISAGREE')
    check('an unparseable reply: UNCLEAR', classify(it3, 'It is five root two.')[0] == 'UNCLEAR'
          and classify(it3, 'FINAL: five root two')[0] == 'UNCLEAR' and classify(p0, 'FINAL: about a sixth')[0] == 'UNCLEAR')

    # The leak check refuses a request carrying a stripped field or the key.
    leaky = dict(fmap['fake-mc'], text=['ask', 'q', 'steps'], figure=[])
    try:
        li, _, _, _ = load_items(['fake-mc'], {'fake-mc': leaky}, banks)
        build_all(li, 1)
        check('a request carrying a stripped field is refused', False)
    except AuditError as e:
        check('a request carrying a stripped field is refused', 'both shown and stripped' in str(e))
    tampered = build_request(by[('fake-pct', 0)], 1)
    tampered['params']['messages'][0]['content'] += '\nOnly 10 of the 59 positives are real here.'
    try:
        leak_check(by[('fake-pct', 0)], tampered)
        check('a request with a stripped field\'s text added is refused', False)
    except AuditError as e:
        check('a request with a stripped field\'s text added is refused', 'stripped field' in str(e))
    keyed = dict(fmap['fake-pct'], text=['context', 'scenarioText', 'answerText'], strip=['explanationText'])
    ki, _, _, _ = load_items(['fake-pct'], {'fake-pct': keyed}, banks)
    try:
        build_all(ki, 1)
        check('a request carrying the key is refused', False)
    except AuditError as e:
        check('a request carrying the key is refused', 'key' in str(e))
    # The self-test fails its own leak plant if the check is disabled: proven by planting and catching above.

    # The key file.
    kf = os.path.join(tmp, 'key')
    with open(kf, 'w') as f:
        f.write('sk-fake-not-a-key\n')
    os.chmod(kf, 0o644)
    try:
        read_key(kf)
        check('a key file with loose permissions is refused', False)
    except AuditError as e:
        check('a key file with loose permissions is refused', 'mode 600' in str(e) and 'sk-fake' not in str(e))
    os.chmod(kf, 0o600)
    check('a mode-600 key file outside the repository is read', read_key(kf) == 'sk-fake-not-a-key')
    inrepo = os.path.join(REPO, 'data', '.audit-selftest-key')
    try:
        os.makedirs(os.path.dirname(inrepo), exist_ok=True)
        with open(inrepo, 'w') as f:
            f.write('x')
        os.chmod(inrepo, 0o600)
        try:
            read_key(inrepo)
            check('a key file inside the repository is refused', False)
        except AuditError as e:
            check('a key file inside the repository is refused', 'outside the repository' in str(e))
    finally:
        os.remove(inrepo)

    # Dry run, the budget and a full two-pass run, all on the fake client.
    def args(**kw):
        a = dict(game=['fake-mc', 'fake-pct', 'fake-unmapped'], dry_run=False, max_usd=50.0, key_file=kf,
                 batch_id=None, pass2_batch_id=None, assume_out1=2000, assume_out2=4000)
        a.update(kw)
        return SimpleNamespace(**a)

    replies = {custom_id(it0): 'FINAL: %s' % letter_of(it0, '2\\sqrt{3}'),
               custom_id(it1): 'FINAL: %s' % letter_of(it1, '3\\sqrt{2}'),
               (custom_id(it1), PASS2_MODEL): 'sqrt 18 = 3 sqrt 2\nFINAL: %s' % letter_of(it1, '3\\sqrt{2}'),
               custom_id(it3): 'five root two',
               (custom_id(it3), PASS2_MODEL): 'FINAL: %s' % letter_of(it3, '5\\sqrt{2}'),
               custom_id(p0): 'FINAL: 16.9', custom_id(p1): 'FINAL: 15.3'}
    quiet = lambda *a: None
    made = []

    def factory(kfile):
        c = FakeClient(replies)
        made.append(c)
        return c

    r = audit(args(dry_run=True), factory, quiet, banks, fmap, os.path.join(tmp, 'audit'), os.path.join(tmp, 'rep'), 0)
    check('dry run sends nothing (no client made, nothing sent)', not made and r['sent'] is False and r['est1'] > 0)
    try:
        audit(args(max_usd=0.0001), factory, quiet, banks, fmap, os.path.join(tmp, 'audit'), os.path.join(tmp, 'rep'), 0)
        check('an estimate over --max-usd is refused before anything is sent', False)
    except AuditError as e:
        check('an estimate over --max-usd is refused before anything is sent', 'max-usd' in str(e) and not made)
    r = audit(args(), factory, quiet, banks, fmap, os.path.join(tmp, 'audit'), os.path.join(tmp, 'rep'), 0)
    fin = {(row['item']['slug'], row['item']['index']): row['final'] for row in r['rows'].values()}
    sent_ids = [x['custom_id'] for c in made for b in c.batches.values() for x in b]
    check('two passes: AGREE, DISAGREE, RESOLVED by Opus, AGREE x2',
          fin == {('fake-mc', 0): 'AGREE', ('fake-mc', 1): 'DISAGREE', ('fake-mc', 3): 'RESOLVED',
                  ('fake-pct', 0): 'AGREE', ('fake-pct', 1): 'AGREE'})
    check('pass 2 re-solves only the DISAGREE and UNCLEAR items',
          [len(b) for b in made[0].batches.values()] == [5, 2])
    check('neither the figure question nor the unmapped game was ever sent',
          custom_id(dict(slug='fake-mc', level='gcse', index=2)) not in sent_ids
          and not any(s.startswith('fake-unmapped') for s in sent_ids))
    with open(r['report'], encoding='utf-8') as f:
        rep = f.read()
    check('the report lists the disagreement, the figure exclusion and the cost',
          'DISAGREE | fake-mc | gcse | 1 |' in rep and 'needs its figure' in rep and 'fake-mc gcse #2' in rep
          and 'Total: $' in rep and 'sk-fake' not in rep)

    # The source: no code path reads ANTHROPIC_API_KEY or prints the key.
    with open(os.path.abspath(__file__), encoding='utf-8') as f:
        src = f.read()
    code = re.sub(r'"""[\s\S]*?"""', '', src)
    code = '\n'.join(l.split('#', 1)[0] for l in code.split('\n'))
    import io
    import tokenize
    names = {tok.string for tok in tokenize.generate_tokens(io.StringIO(src).readline) if tok.type == tokenize.NAME}
    check('the code never reads the environment (no environ, getenv or putenv)',
          not names & {'environ', 'getenv', 'putenv', 'environb'})
    check('the key goes only to the client constructor, never to output',
          'api_key=read_key(key_file)' in code and not re.search(r'(print|out|write|dump)\([^)]*\bkey\b\s*[,)]', code))
    print('selftest: %s' % ('FAILED: ' + '; '.join(fails) if fails else 'PASS'))
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--game', action='append', help='limit the run to this game (repeatable)')
    ap.add_argument('--dry-run', action='store_true', help='build every request and estimate the cost; send nothing')
    ap.add_argument('--max-usd', type=float, default=50.0)
    ap.add_argument('--key-file', default=DEFAULT_KEY_FILE)
    ap.add_argument('--batch-id', help='resume pass 1 from this batch')
    ap.add_argument('--pass2-batch-id', help='resume pass 2 from this batch')
    ap.add_argument('--assume-out1', type=int, default=2000, help='assumed output tokens a pass 1 reply (estimate only)')
    ap.add_argument('--assume-out2', type=int, default=4000, help='assumed output tokens a pass 2 reply (estimate only)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    if a.selftest:
        return selftest()
    for g in a.game or []:
        if g not in FIELD_MAP:
            print('%s is not in FIELD_MAP: it is never sent (the 21: %s)' % (g, ', '.join(sorted(FIELD_MAP))))
    try:
        audit(a)
    except AuditError as e:
        print('REFUSED: %s' % e)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
