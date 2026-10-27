#!/usr/bin/env python3
# ci-shards: The 6 P's (the topic data file is the generator's output; no mark figure, AQA, Edexcel or "in development" in the page, no launch into a game; the four past-paper sites before Start; 10,000 sessions each way: six distinct covered topics in band order, frequencies in proportion to marks; every format marked by value through the page's own judge(), schema faults left out, five picked unseen first; a full session at 1280 px with localStorage working, on fixture banks covering all nine formats: every format answered right and wrong, never-marked answers not marked, slips, working, five a topic and a topic card, results, nudge, practice links, tick-list and events; resumed mid-topic after a reload; the same session at 320 px on a touch screen, typed on the phone keypad, with localStorage blocked: no sideways scroll on any screen, resumed mid-topic from window.name; every real bank's verdict and Next on a 375 x 667 phone; a topic with no bank offers Skip only; fault-injection self-test: the planted faults, each caught) |  | 2
# ci-deps: the-6-ps/ schools/assets/exam-topics-ocr-foundation.json scripts/gen-exam-topics.py scripts/fixtures/six-ps/
"""Independent verification for The 6 P's (/the-6-ps/): built 24 Oct 2026 (contract THE-6-PS), its question player
25 Oct 2026 (contract SIX-PS-PLAYER, Jon's ruling: self-contained, no hand-off into games).

WHAT IS CHECKED, AND AGAINST WHAT
-------------------------------------------------------------------------------
  Data       schools/assets/exam-topics-ocr-foundation.json equals what scripts/gen-exam-topics.py builds from its
             table (compared as data). The page types no figure: no number next to "mark", no audit figure (13.3,
             ...) and not the source sentence; every figure it shows is read from the file.
  Claims     neither "AQA" nor "Edexcel" appears in the page; "in development" appears nowhere (SIX-PS-SOON's intent);
             no emoji outside the shared footer; the four past-paper sites are linked, each after Start (Start is the first thing
             on the screen: contract SIX-PS-PLAYER-FIXES (f), Jon, 27 Oct 2026).
  No launch  no link into a game with burst parameters, no ?done= return handling, none of v1's tool events.
  Sessions   the page's own plan(), run 10,000 times with storage blocked and 10,000 times on one device: six distinct
             COVERED topics in Jon's band order, frequencies within tolerance of 10,000 x 6 x marks / total (as v1).
  Marking    every fixture question (scripts/fixtures/six-ps/, all nine formats; not published) marked through the
             page's own judge() against a table typed here from the schema (docs/six-ps-schema.md) and canon 7.1.3:
             right forms (6.50 for 6.5, 6/8 under "equivalent", 2 : 4 : 6), wrong values, SR-3's format cases (3.33 at
             1 d.p., 6/8 under "simplest", 7/4 for a mixed answer, 4 : 6), SR-2's money case (3.5), unreadable entries
             (the Unicode minus, a thousands comma), a range's band, a slip matched by the question's own rule, a
             choice by its dataset.val. Schema faults (an unknown format, three options, a range reaching half way to
             a slip) are left out. Five are picked unseen first, then the longest seen, through the page's own store.
  Session    (at 1280 px and at 320 px) a full session through the page on the fixture banks: each question's scripted
             answers typed (at 320 px on the phone keypad), the never-marked ones (format, unreadable, no unit) showing the
             shared message with nothing marked or sent; each marked one showing right or wrong at once, the slip line
             and the working on a wrong one, the working one tap away on a right one; the header "Question n of 5 ·
             Topic m of 6"; after the fifth answer the topic card ("<topic>: r of 5", its weight) and never a sixth
             question; the results (scores, weights, "Want more practice? <game>" linking the game at its level), the
             nudge, the tick-list and its one event; question_answered (correct, and the topic id packed in
             filter_type/filter_value, Jon's ruling of 25 Oct), one game_started and one game_completed. Resumed
             mid-topic after a reload, from localStorage (1280 px) and from window.name (320 px, storage blocked).
             Diagrams: drawn, with their script, handler and external image removed.
  Phone      320 px: no sideways scroll on the start screen, any question, a topic card or the results.
  No bank    a drawn topic whose bank does not load says its questions aren't ready, with Skip only.

    python scripts/verify-the-6-ps.py                  # every unit
    python scripts/verify-the-6-ps.py --list-units     # the units: the data and routes, the static checks, the draws,
                                                       # the marking, each browser check (each real bank's 375 x 667
                                                       # feedback its own), each session, each plant
    python scripts/verify-the-6-ps.py --shard 2/3      # part 2 of 3 of the units (CI; scripts/ci-groups.py chooses 3)
"""
import argparse
import contextlib
import importlib.util
import json
import math
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

PAGE = os.path.join(ROOT, 'the-6-ps', 'index.html')
DATA = os.path.join(ROOT, 'schools', 'assets', 'exam-topics-ocr-foundation.json')
FIXTURES = os.path.join(HERE, 'fixtures', 'six-ps')
SESSION_FIXTURES = ['fx-1', 'fx-2', 'fx-3', 'fx-4', 'fx-5', 'fx-6']
K, PER_TOPIC = 6, 5
DRAWS = 10000
SITES = ['https://hannahkettlemaths.co.uk/', 'https://corbettmaths.com/', 'https://www.mathsgenie.co.uk/',
         'https://www.mathslinks.co.uk/']


def generator():
    spec = importlib.util.spec_from_file_location('gen_exam_topics', os.path.join(HERE, 'gen-exam-topics.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_data():
    with open(DATA, encoding='utf-8') as f:
        return json.load(f)


def fixture(name):
    with open(os.path.join(FIXTURES, name + '.json'), encoding='utf-8') as f:
        return json.load(f)


def by_ref():
    """Every fixture question by its source ref ('fx-1[0]', ...)."""
    out = {}
    for fn in sorted(os.listdir(FIXTURES)):
        if fn.endswith('.json'):
            for q in fixture(fn[:-5])['questions']:
                out[q['source']['ref']] = q
    return out


# ---------------------------------------------------------------- the scripts: what is typed, and what must happen
# Each fixture question's answers in order; every step but the last is never marked. A value is what the boxes hold:
# a string (one box), a dict (fraction: whole/num/den; coordinates: x/y), a list (ratio parts), a (value, unit) pair,
# or an option's val (choice). 'wide' steps are typed only at 1280 px (the keypad types neither "£" nor "−").
SCRIPT = {
    'fx-1[0]': [('6.50', 'right')],
    'fx-1[1]': [('3.33', 'format'), ('3.3', 'right')],
    'fx-1[2]': [('6', 'wrong+slip')],
    'fx-1[3]': [('3.5', 'format'), ('£3.50', 'right', '3.50')],
    'fx-1[4]': [('−5', 'unreadable', None), ('-5', 'right')],
    'fx-2[0]': [({'num': '6', 'den': '8'}, 'right')],
    'fx-2[1]': [({'num': '6', 'den': '8'}, 'format'), ({'num': '3', 'den': '4'}, 'right')],
    'fx-2[2]': [({'num': '7', 'den': '4'}, 'format'), ({'whole': '1', 'num': '3', 'den': '4'}, 'right')],
    'fx-2[3]': [({'num': '5', 'den': '7'}, 'wrong+slip')],
    'fx-2[4]': [({'num': '-1', 'den': '2'}, 'right')],
    'fx-3[0]': [(['4', '6'], 'format'), (['2', '3'], 'right')],
    'fx-3[1]': [(['2', '4', '6'], 'right')],
    'fx-3[2]': [(['5', '2'], 'wrong+slip')],
    'fx-3[3]': [({'x': '5', 'y': '-2'}, 'wrong+slip')],
    'fx-3[4]': [({'x': '3', 'y': '0'}, 'right')],
    'fx-4[0]': [('a', 'wrong+slip')],
    'fx-4[1]': [('d', 'right')],
    'fx-4[2]': [('a', 'wrong')],
    'fx-4[3]': [({'x': '3', 'y': '-2'}, 'right')],
    'fx-4[4]': [({'m': '45', 'e': '3'}, 'format'), ({'m': '4.5', 'e': '4'}, 'right')],
    'fx-5[0]': [(('40', None), 'nounit'), (('40', 'km'), 'wrong+slip')],
    'fx-5[1]': [(('2.55', 'g/cm³'), 'format'), (('2.6', 'g/cm³'), 'right')],
    'fx-5[2]': [(('30', 'km'), 'right')],
    'fx-5[3]': [(('5', 'h'), 'wrong')],
    'fx-5[4]': [(('5', 'm/s'), 'right')],
    'fx-6[0]': [('56', 'right')],
    'fx-6[1]': [('9', 'right')],
    'fx-6[2]': [('3.57', 'wrong')],
    'fx-6[3]': [('8', 'wrong')],
    'fx-6[4]': [(['4', '10'], 'format'), (['2', '5'], 'right')],
}
SCRIPT.update({'fx-seen[%d]' % i: [(str(2 * i + 1), 'right')] for i in range(10)})

# Marking cases beyond the session's, through judge() only: (ref, typed, result).
MARKING = [
    ('fx-1[0]', '6.5', 'correct'), ('fx-1[0]', ' 6.5 ', 'correct'), ('fx-1[0]', '6.51', 'wrong'),
    ('fx-1[0]', '6,5', 'unreadable'), ('fx-1[0]', '', 'unreadable'), ('fx-1[0]', '6.5cm', 'unreadable'),
    ('fx-1[1]', '3.30', 'correct'), ('fx-1[1]', '3.4', 'wrong'), ('fx-1[1]', '3', 'wrong'),
    ('fx-1[2]', '4.8', 'correct'), ('fx-1[2]', '5.2', 'correct'), ('fx-1[2]', '5.3', 'wrong'), ('fx-1[2]', '4.79', 'wrong'),
    ('fx-1[3]', '3.50', 'correct'), ('fx-1[3]', '£3.50', 'correct'), ('fx-1[3]', '3.500', 'format'), ('fx-1[3]', '3.49', 'wrong'),
    ('fx-6[2]', '3.75', 'correct'), ('fx-6[2]', '£3.75', 'correct'), ('fx-6[2]', '375', 'wrong'),
    ('fx-6[0]', '1,056', 'unreadable'),
    ('fx-2[0]', {'num': '3', 'den': '4'}, 'correct'), ('fx-2[0]', {'num': '9', 'den': '12'}, 'correct'),
    ('fx-2[0]', {'num': '4', 'den': '3'}, 'wrong'), ('fx-2[0]', {'num': '3', 'den': '0'}, 'unreadable'),
    ('fx-2[0]', {'num': '0.75', 'den': '1'}, 'unreadable'),
    ('fx-2[2]', {'whole': '1', 'num': '6', 'den': '8'}, 'format'), ('fx-2[2]', {'whole': '1', 'num': '1', 'den': '4'}, 'wrong'),
    ('fx-2[4]', {'num': '-2', 'den': '4'}, 'correct'), ('fx-2[4]', {'num': '1', 'den': '2'}, 'wrong'),
    ('fx-3[0]', ['2', '3'], 'correct'), ('fx-3[0]', ['3', '2'], 'wrong'), ('fx-3[0]', ['1', '1.5'], 'format'),
    ('fx-3[1]', ['1', '2', '3'], 'correct'), ('fx-3[1]', ['0.5', '1', '1.5'], 'correct'), ('fx-3[1]', ['1', '2', '4'], 'wrong'),
    ('fx-3[1]', ['0', '0', '0'], 'wrong'), ('fx-3[1]', ['-1', '-2', '-3'], 'wrong'), ('fx-3[1]', ['1', '', '3'], 'unreadable'),
    ('fx-3[3]', {'x': '-2', 'y': '5'}, 'correct'), ('fx-3[3]', {'x': '-2', 'y': '5.0'}, 'correct'),
    ('fx-3[3]', {'x': '2', 'y': '5'}, 'wrong'), ('fx-3[3]', {'x': '', 'y': '5'}, 'unreadable'),
    ('fx-4[0]', 'b', 'correct'), ('fx-4[0]', 'c', 'wrong'), ('fx-4[0]', '\\(8\\)', 'wrong'), ('fx-4[0]', '8', 'wrong'),
    ('fx-4[3]', {'x': '3', 'y': '-2'}, 'correct'), ('fx-4[3]', {'x': '3.0', 'y': '-2.0'}, 'correct'),
    ('fx-4[3]', {'x': '-2', 'y': '3'}, 'wrong'), ('fx-4[3]', {'x': '3', 'y': '2'}, 'wrong'), ('fx-4[3]', {'x': '', 'y': '3'}, 'unreadable'),
    ('fx-4[4]', {'m': '4.5', 'e': '4'}, 'correct'), ('fx-4[4]', {'m': '45', 'e': '3'}, 'format'), ('fx-4[4]', {'m': '0.45', 'e': '5'}, 'format'),
    ('fx-4[4]', {'m': '450', 'e': '2'}, 'format'), ('fx-4[4]', {'m': '4.5', 'e': '3'}, 'wrong'), ('fx-4[4]', {'m': '5.4', 'e': '4'}, 'wrong'),
    ('fx-4[4]', {'m': '4.5', 'e': '5'}, 'wrong'), ('fx-4[4]', {'m': '', 'e': '4'}, 'unreadable'), ('fx-4[4]', {'m': '4.5', 'e': 'x'}, 'unreadable'),
    ('fx-4[4]', {'m': '4.5', 'e': '4.5'}, 'unreadable'),
    ('fx-5[0]', ('40', 'km/h'), 'correct'), ('fx-5[0]', ('40', 'm/s'), 'wrong'), ('fx-5[0]', ('41', 'km/h'), 'wrong'),
    ('fx-5[0]', ('', 'km/h'), 'unreadable'),
    ('fx-5[1]', ('2.60', 'g/cm³'), 'correct'), ('fx-5[1]', ('2.55', 'g'), 'wrong'),
]
# (ref, typed, the slip whose line is shown, by index into its slip list, or None)
SLIPS = [
    ('fx-1[2]', '6.1', 0), ('fx-1[2]', '6.3', None), ('fx-2[0]', {'num': '1', 'den': '3'}, 0),
    ('fx-5[0]', ('40', 'km'), 0), ('fx-5[0]', ('40', 'h'), None), ('fx-4[0]', 'a', 0), ('fx-4[0]', 'd', None),
]
LEFT_OUT = ['LEFT OUT: an unknown format.', 'LEFT OUT: a range reaching half way to a slip.', 'LEFT OUT: three options.']


def as_input(q, v):
    """A scripted value as the page's readInput() returns it."""
    f = q['format']
    if f == 'fraction':
        return {'whole': v.get('whole', ''), 'num': v.get('num', ''), 'den': v.get('den', '')}
    if f == 'ratio':
        return {'parts': v}
    if f in ('coordinates', 'pair', 'standard_form'):
        return v
    if f == 'choice':
        return {'val': v}
    if f == 'number_unit':
        return {'value': v[0], 'unit': v[1]}
    return {'value': v}


def js_num(v):
    return str(int(v)) if float(v) == int(v) else repr(float(v))


def shown_answer(q):
    """The answer line's plain text, worked out here (None where it is drawn by KaTeX)."""
    a, f = q['answer'], q['format']
    sgn = lambda x: js_num(x).replace('-', '−')
    if f in ('number', 'number_unit'):
        v = ('%.*f' % (a['dp'], a['value'])).replace('-', '−') if 'dp' in a else sgn(a['value'])
        unit = a.get('unit') if f == 'number_unit' else q.get('unit')
        return v + (' ' + unit if unit else '')
    if f == 'money':
        return '£' + format(a['pence'] / 100, ',.2f')
    if f == 'ratio':
        return ' : '.join(js_num(p) for p in a['parts'])
    if f == 'coordinates':
        return '(%s, %s)' % (sgn(a['x']), sgn(a['y']))
    if f == 'pair':
        return 'x = %s, y = %s' % (sgn(a['x']), sgn(a['y']))
    if f == 'standard_form':
        return '%s × 10%s' % (js_num(a['m']), sgn(a['e']))
    return None


def squash(s):
    """Text with every space (and no-break space) taken out: KaTeX sets its own spacing, so the answer line is compared without it."""
    return re.sub(r'[\s\u00a0]+', '', s)


ANSWER_LINE_JS = ("() => { const c = document.getElementById('qAnswerLine').cloneNode(true); "
                  "c.querySelectorAll('.katex-mathml').forEach(e => e.remove()); return c.textContent; }")


# ---------------------------------------------------------------- data and static
def check_data(data, out):
    built, errors = generator().build()
    out.extend('generator: ' + e for e in errors)
    if data != built:
        out.append('the data file is not what scripts/gen-exam-topics.py generates (edited by hand, or not regenerated)')
    ids = [t['id'] for t in data['covered']]
    if len(set(ids)) != len(ids):
        out.append('covered topic ids repeat')


def mark_literals(data):
    """Every audit figure as it would be typed with its decimal (13.3, 9.0, ...)."""
    return sorted({'%.1f' % t['marks'] for t in data['covered'] + data['coming_soon']}, key=float)


def without_style_and_comments(html):
    """The page less its <style> blocks, HTML comments and script comments: CSS sizes (1.8rem) and a comment's
    canon reference (7.5) are not figures a reader sees, while text and script strings are."""
    s = re.sub(r'<style\b.*?</style>', ' ', html, flags=re.S | re.I)
    s = re.sub(r'<!--.*?-->', ' ', s, flags=re.S)
    s = re.sub(r'/\*.*?\*/', ' ', s, flags=re.S)
    return re.sub(r'(^|[\s;{}(,])//[^\n]*', r'\1', s)


EMOJI = re.compile('[\U0001F000-\U0001FAFF☀-➿⭐⭕️]|&#(9[0-9]{3}|1[0-9]{4,});')


def static_checks(html, data, out):
    if '<meta name="robots" content="noindex">' not in html:
        out.append('the page is not noindex (it is unlisted until Jon has played it)')
    if '<!-- UNLISTED' not in html:
        out.append('the page has no UNLISTED comment')
    if not re.search(r'<script src="/schools/assets/analytics\.js"></script>', html):
        out.append('the page does not load analytics.js')
    if '<html lang="en-GB" data-theme="light">' not in html or 'href="/schools/assets/theme.css"' not in html:
        out.append('the page is not on theme.css, light row (contract (c))')
    for m in re.finditer(r'\d+(?:\.\d+)?\s*(?:&nbsp;|\s)?marks?\b', html, re.I):
        out.append('a hand-typed mark figure in the page: %r' % html[max(0, m.start() - 30):m.end() + 10])
    shown = without_style_and_comments(html)
    for lit in mark_literals(data):
        for m in re.finditer(r'(?<![\d.])%s(?![\d])' % re.escape(lit), shown):
            out.append('the audit figure %s is typed in the page: %r' % (lit, shown[max(0, m.start() - 30):m.end() + 10]))
    if data['source'] in html or re.search(r'\b%d OCR\b' % data['papers'], html):
        out.append('the source line is typed in the page, not read from the data file')
    for word in ('AQA', 'Edexcel'):
        for m in re.finditer(r'\b%s\b' % word, html, re.I):
            out.append('"%s" appears in the page (no claim about its weightings): %r'
                       % (word, html[max(0, m.start() - 40):m.end() + 40]))
    for m in re.finditer(r'in\s+development', html, re.I):
        out.append('"in development" appears in the page (SIX-PS-SOON): %r' % html[max(0, m.start() - 40):m.end() + 20])
    body = re.sub(r'<footer class="site-footer">.*?</footer>', ' ', html, flags=re.S)
    for m in EMOJI.finditer(body):
        out.append('an emoji outside the shared footer: %r' % body[max(0, m.start() - 30):m.end() + 10])
    for pat, what in ((r'burst=', 'a launch link with burst parameters'), (r"\.get\('done'\)|\?done=", 'the ?done= return handling'),
                      (r"six_ps_(started|topic|finished)", "one of v1's tool events")):
        if re.search(pat, shown):
            out.append('the page still has %s' % what)
    start = html.find('id="startBtn"')
    for url in SITES:
        at = html.find('href="%s"' % url)
        if at < 0:
            out.append('the page does not link %s' % url)
        elif start >= 0 and at < start:
            out.append('%s is linked before the Start button (Start comes first)' % url)
    if start < 0:
        out.append('the page has no Start button (id="startBtn")')
    if "'/schools/assets/exam-topics-ocr-foundation.json'" not in html:
        out.append('the page does not read its topics from /schools/assets/exam-topics-ocr-foundation.json')


def declared_levels(slug):
    p = os.path.join(ROOT, 'games', slug, 'index.html')
    if not os.path.isfile(p):
        return None
    with open(p, encoding='utf-8') as f:
        src = f.read()
    m = re.search(r"MaffsLevel\.resolve\(\{\s*slug:\s*'%s',\s*levels:\s*\[([^\]]*)\]" % re.escape(slug), src)
    return re.findall(r"'([^']+)'", m.group(1)) if m else []


def check_routes(data, out):
    """Each topic's "Want more practice?" game exists and declares the level its link opens."""
    for t in data['covered']:
        r = t['route']
        if r is None:       # a bank-first topic: no game yet (canon 8.2.1), so no link to check
            continue
        levels = declared_levels(r['slug'])
        if levels is None:
            out.append('%s: no game at games/%s/' % (t['id'], r['slug']))
        elif r['level'] not in levels:
            out.append('%s: %s does not declare level %r (it declares %s)' % (t['id'], r['slug'], r['level'], levels))


def about(marks):
    """Marks as the page says them, 'about N': rounded half up (6.5 is 7), at least 1."""
    return max(1, int(math.floor(marks + 0.5)))


def marks_text(t):
    return "worth about %d marks across the three Foundation papers" % about(t['marks'])


# ---------------------------------------------------------------- browser
BLOCK_STORAGE = """(() => {
  const no = () => { throw new DOMException('blocked', 'SecurityError'); };
  Object.defineProperty(window, 'localStorage', { get: no, configurable: false });
  Object.defineProperty(window, 'sessionStorage', { get: no, configurable: false });
})();"""

# Every mfg() call is recorded through a binding that survives navigation; the page's own mfg cannot replace it.
RECORD_MFG = """(() => {
  const rec = (n, p) => { try { window.__mfgRecord(n, JSON.stringify(p === undefined ? null : p)); } catch (e) {} };
  Object.defineProperty(window, 'mfg', { get: () => rec, set: () => {}, configurable: false });
})();"""

# Test speed only: the wrong-answer floor (3 s) and the fresh-question guard (300 ms) set to 0 once they load.
NO_WAITS = """(() => {
  const set = () => { if (window.MaffsNext) MaffsNext.FLOOR_MS = 0; if (window.MaffsLock) MaffsLock.FRESH_MS = 0; };
  document.addEventListener('DOMContentLoaded', set);
})();"""


class Browser:
    """The page served from the given html (so a plant is an edit), with KaTeX from the pinned copy, games and every
    other site aborted, and the topic banks served from the fixtures: the first topic asked for gets queue[0], and so
    on; None is a 404. A topic keeps its fixture across reloads."""

    def __init__(self, pw, base, html, size=(1280, 800), blocked=False, queue=None, served=None):
        self.br = pw.chromium.launch()
        touch = size[0] <= 600
        self.ctx = self.br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch)
        self.touch = touch
        self.events = []
        self.errors = []
        self.warnings = []
        self.queue = list(SESSION_FIXTURES if queue is None else queue)
        self.assigned = {}
        self.real = {}           # topic id -> a real bank served in place of a fixture
        self.served = served     # the topic data file served in place of the real one (a test of a topic the real file lacks)
        self.unmarked = 0        # never-marked answers typed (format, unreadable, no unit)
        self.formats = set()     # (format, right or wrong) marked
        self.ctx.expose_function('__mfgRecord', lambda n, p: self.events.append((n, json.loads(p))))
        self.ctx.add_init_script(RECORD_MFG)
        self.ctx.add_init_script(NO_WAITS)
        if blocked:
            self.ctx.add_init_script(BLOCK_STORAGE)
        self.base = base
        page_url = re.compile(r'/the-6-ps/(\?[^/]*)?$')
        bank_url = re.compile(r'/schools/assets/six-ps/([a-z0-9-]+)\.json$')

        def handle(route):
            url = route.request.url
            if bc.is_font_cdn(url):
                return bc.serve_real_font(route)
            if not url.startswith(base) or '/games/' in url:
                return route.abort()
            if page_url.search(url):
                return route.fulfill(status=200, content_type='text/html; charset=utf-8', body=html)
            if self.served is not None and url.endswith('/exam-topics-ocr-foundation.json'):
                return route.fulfill(status=200, content_type='application/json', body=json.dumps(self.served))
            m = bank_url.search(url)
            if m:
                return self.serve_bank(route, m.group(1))
            return route.continue_()
        self.ctx.route('**/*', handle)
        self.page = self.ctx.new_page()
        self.page.set_default_timeout(5000)   # every step is a local click or load; a planted fault fails fast
        self.page.on('pageerror', lambda e: self.errors.append(str(e)))
        self.page.on('console', self.on_console)

    def on_console(self, m):
        if m.type == 'warning':
            self.warnings.append(m.text)
        elif m.type == 'error' and not m.text.startswith('Failed to load resource'):
            self.errors.append('console.error: ' + m.text)

    def serve_bank(self, route, topic):
        if topic in self.real:
            return route.fulfill(status=200, content_type='application/json', body=json.dumps(self.real[topic]))
        if topic not in self.assigned:
            self.assigned[topic] = self.queue.pop(0) if self.queue else None
        name = self.assigned[topic]
        if name is None:
            return route.fulfill(status=404, body='not found')
        bank = fixture(name)
        bank['topic'] = topic
        for q in bank['questions']:
            q['topic'] = topic
            q['id'] = q['id'].replace('fixture-', topic + '-', 1)
        route.fulfill(status=200, content_type='application/json', body=json.dumps(bank))

    def open(self, query=''):
        self.page.goto(self.base + '/the-6-ps/' + query, wait_until='load', timeout=20000)
        self.page.wait_for_function("""() => !!window.SixPs && (!!SixPs.data() ||
            !document.getElementById('loadError').hidden)""", timeout=10000)

    def close(self):
        self.br.close()


def check_engine(b, data, out):
    """10,000 sessions each way, from the page's own functions."""
    p = b.page
    res = p.evaluate("""(n) => {
        const d = SixPs.data(), blocked = { getCredit: () => undefined, setCredit: () => {} };
        let credit = {};
        const device = { getCredit: () => credit, setCredit: (c) => { credit = c; } };
        const run = (store) => { const s = []; for (let i = 0; i < n; i++) s.push(SixPs.plan(d, store, Math.random).plan.map(x => x.id)); return s; };
        return { random: run(blocked), rotating: run(device) };
    }""", DRAWS)
    covered = {t['id']: t for t in data['covered']}
    soon = {t['id'] for t in data['coming_soon']}
    W = sum(round(t['marks'] * 10) for t in data['covered'])
    for kind, sessions in res.items():
        counts = {i: 0 for i in covered}
        last, worst = {}, {}
        bad = set()
        for n, s in enumerate(sessions):
            if len(s) != K:
                bad.add('a %s session has %d topics, not %d' % (kind, len(s), K))
            if len(set(s)) != len(s):
                bad.add('a %s session repeats a topic: %s' % (kind, s))
            for i in s:
                if i in soon:
                    bad.add('a %s session drew the coming-soon topic %s' % (kind, i))
                elif i not in covered:
                    bad.add('a %s session drew the unknown topic %s' % (kind, i))
                else:
                    counts[i] += 1
                    if n >= 200 and i in last:
                        worst[i] = max(worst.get(i, 0), n - last[i])
                    last[i] = n
            keys = [(covered[i]['band'][0], covered[i]['band'][1]) for i in s if i in covered]
            if keys != sorted(keys):
                bad.add('a %s session is not in band order: %s' % (kind, s))
        out.extend(sorted(bad)[:10])
        for i, t in covered.items():
            pi = K * round(t['marks'] * 10) / W
            exp = DRAWS * pi
            tol = 3 if kind == 'rotating' else 4.5 * math.sqrt(exp * (1 - pi)) + 2
            if abs(counts[i] - exp) > tol:
                out.append('%s draws: %s came up %d times in %d sessions, expected %.0f (tolerance %.0f)'
                           % (kind, i, counts[i], DRAWS, exp, tol))
            if kind == 'rotating' and worst.get(i, 0) > 2 / pi + 1:
                out.append('rotation: %s waited %d sessions, more than twice its expected gap of %.1f' % (i, worst[i], 1 / pi))


def check_marking(b, out):
    """The page's own judge(), problem() and pickFive() against the tables above."""
    p = b.page
    refs = by_ref()
    cases = []
    for ref, steps in SCRIPT.items():
        q = refs[ref]
        for st in steps:
            want = {'right': 'correct', 'wrong': 'wrong', 'wrong+slip': 'wrong'}.get(st[1], st[1])
            cases.append((ref, st[0], want))
    cases += MARKING
    got = p.evaluate("""(cases) => cases.map(([q, inp]) => SixPs.judge(q, q.answer, inp))""",
                     [[refs[r], as_input(refs[r], v)] for r, v, _ in cases])
    for (ref, v, want), g in zip(cases, got):
        if g['result'] != want:
            out.append('marking: %s typed %r gave %r, expected %r' % (ref, v, g['result'], want))
        if want in ('format', 'unreadable', 'nounit') and not g['msg']:
            out.append('marking: %s typed %r is %s but has no message' % (ref, v, want))
    sl = p.evaluate("""(cases) => cases.map(([q, inp]) => { const s = SixPs.slipFor(q, inp); return s ? q.slip.indexOf(s) : null; })""",
                    [[refs[r], as_input(refs[r], v)] for r, v, _ in SLIPS])
    for (ref, v, want), g in zip(SLIPS, sl):
        if g != want:
            out.append('slips: %s typed %r matched slip %r, expected %r' % (ref, v, g, want))
    bank6 = fixture('fx-6')['questions']
    probs = p.evaluate("(qs) => qs.map(q => SixPs.problem(q, 'fixture'))", bank6)
    for q, why in zip(bank6, probs):
        if (q['stem'] in LEFT_OUT) != bool(why):
            out.append('schema: %r %s' % (q['stem'], 'was kept' if not why else 'was left out (%s)' % why))
    for ref, q in refs.items():
        if not ref.startswith('fx-6') and p.evaluate("(q) => SixPs.problem(q, 'fixture')", q):
            out.append('schema: the fixture %s was left out' % ref)
    seen = p.evaluate("""(qs) => {
        const st = SixPs.makeStore(), t = 'seen-test', ids = (l) => l.slice().sort().join();
        const a = SixPs.pickFive(qs, st.getSeen(t), Math.random); st.addSeen(t, a);
        const b = SixPs.pickFive(qs, st.getSeen(t), Math.random); st.addSeen(t, b);
        const c = SixPs.pickFive(qs, st.getSeen(t), Math.random);
        const bands = (l) => l.map(id => qs.find(q => q.id === id).band);
        return { a: a, b: b, c: c, ab: a.filter(x => b.indexOf(x) >= 0).length, ca: ids(c) === ids(a), bands: bands(a) };
    }""", fixture('fx-seen')['questions'])
    if seen['ab']:
        out.append('pickFive: the second five repeat %d of the first, with five unseen left' % seen['ab'])
    if not seen['ca']:
        out.append('pickFive: once all ten are seen, the third five are not the five seen longest ago')
    if seen['bands'] != sorted(seen['bands']) or len(seen['a']) != PER_TOPIC:
        out.append('pickFive: not five in band order (%s)' % seen['bands'])


def visible_text(p, sel):
    return p.evaluate('(s) => Array.from(document.querySelectorAll(s)).filter(e => e.offsetParent !== null).map(e => e.innerText.trim())', sel)


def sideways(p, where, out):
    w = p.evaluate('() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]')
    if w[0] > w[1]:
        out.append('%s: sideways scroll at 320 px (%d > %d)' % (where, w[0], w[1]))


def fill(b, part, text):
    """Type into one box: fill() with a mouse; on a touch screen, the phone keypad's own keys."""
    p, sel = b.page, '#in-' + part
    if not b.touch:
        p.fill(sel, text)
        return
    p.tap(sel)
    p.tap('#qKeys [data-act="clear"]')
    for ch in text:
        p.tap('#qKeys [data-act="minus"]' if ch == '-' else '#qKeys [data-act="in"][data-val="%s"]' % ch)
    if p.input_value(sel) != text:
        raise AssertionError('the keypad typed %r into %s, not %r' % (p.input_value(sel), sel, text))


def answer(b, q, v):
    """Enter scripted value v for question q, and submit it."""
    p, f = b.page, q['format']
    tap = p.tap if b.touch else p.click
    if f == 'choice':
        return tap('#qOpts button[data-val="%s"]' % v)
    if f == 'fraction':
        for part in ('whole', 'num', 'den'):
            if p.query_selector('#in-' + part):
                fill(b, part, v.get(part, ''))
    elif f == 'ratio':
        for i, x in enumerate(v):
            fill(b, 'p%d' % i, x)
    elif f in ('coordinates', 'pair'):
        fill(b, 'x', v['x'])
        fill(b, 'y', v['y'])
    elif f == 'standard_form':
        fill(b, 'm', v['m'])
        fill(b, 'e', v['e'])
    elif f == 'number_unit':
        fill(b, 'value', v[0])
        if v[1]:
            tap('#qUnits button[data-unit="%s"]' % v[1])
    else:
        fill(b, 'value', v)
    tap('#checkBtn')


def play_topic(b, m, topic, out, tag, narrow=False, stop_after=None, offset=0, right0=0):
    """Answer one topic's questions by their scripts. Returns the topic's right count, or None if stopped early.
    stop_after=n: stop once n questions are answered (the feedback still showing), for a resume check; offset and
    right0: a resumed topic, offset questions (right0 of them right) answered before the reload."""
    p, refs = b.page, by_ref()
    tap = p.tap if b.touch else p.click
    right, asked = right0, []
    while True:
        p.wait_for_selector('#play:not([hidden]), #between:not([hidden])', timeout=5000)
        if p.is_visible('#between'):
            break
        q = p.evaluate('() => SixPs.question()')
        ref = q['source']['ref']
        n = offset + len(asked) + 1
        asked.append(q['id'])
        head = p.inner_text('#qHead').strip()
        want_head = 'Question %d of %d' % (n, PER_TOPIC)      # the slim title line carries the topic count (Jon, 27 Oct 2026)
        if head != want_head:
            out.append('%s: header %r, expected %r' % (tag, head, want_head))
            if n > PER_TOPIC:
                return None
        if q['stem'] in LEFT_OUT:
            out.append('%s: a question the schema leaves out was asked: %r' % (tag, q['stem']))
        if '\\(' in q['stem'] and not p.query_selector('#qStem .katex'):
            out.append('%s: %s: the stem\'s maths was not rendered by KaTeX' % (tag, ref))
        if q.get('diagram'):
            d = p.evaluate("""() => { const d = document.getElementById('qDiagram'); return { shown: !d.hidden && !!d.querySelector('svg'),
                bad: !!d.querySelector('script, foreignObject, [onload]') || Array.from(d.querySelectorAll('*')).some(e =>
                  ['href', 'xlink:href'].some(a => e.hasAttribute(a) && !e.getAttribute(a).trim().startsWith('#'))),
                ran: !!window.__svgRan }; }""")
            if not d['shown'] or d['bad'] or d['ran']:
                out.append('%s: %s: the diagram %s' % (tag, ref, d))
        calc = p.inner_text('#qCalc').strip()
        want_calc = 'Calculator optional' if q['calc'] == 'optional' else 'Calculator' if q['calc'] else 'Non-calculator'
        if calc != want_calc:
            out.append('%s: %s: calculator tag %r' % (tag, ref, calc))
        try_shown = p.is_visible('#qTry')
        want_try = q['calc'] == 'optional' and q.get('try_without') is True
        if try_shown != want_try or (try_shown and p.inner_text('#qTry').strip() != 'Try without a calculator'):
            out.append('%s: %s: the "Try without a calculator" prompt is %s, expected %s' % (tag, ref, 'shown' if try_shown else 'not shown', want_try))
        if narrow:
            sideways(p, '%s (%s)' % (ref, q['format']), out)
            if q['format'] != 'choice' and not p.query_selector('#qKeys .maffs-keypad-key'):
                out.append('%s: %s: no phone keypad at 320 px' % (tag, ref))
        steps = [st for st in SCRIPT[ref] if not (narrow and len(st) > 2 and st[2] is None)]
        for st in steps:
            v = st[2] if narrow and len(st) > 2 else st[0]
            before = len(b.events)
            answer(b, q, v)
            kind = st[1]
            if kind in ('format', 'unreadable', 'nounit'):
                msg = p.inner_text('#qMsg').strip()
                phrase = {'format': r'^Right (value|amount)', 'unreadable': r'^Type ', 'nounit': r'Pick a unit'}[kind]
                if not re.search(phrase, msg):
                    out.append('%s: %s typed %r: expected the %s message, saw %r' % (tag, ref, v, kind, msg))
                if p.is_visible('#qFb') or len(b.events) != before:
                    out.append('%s: %s typed %r (%s) was marked' % (tag, ref, v, kind))
                    return None
                b.unmarked += 1
                continue
            p.wait_for_selector('#qFb:not([hidden])', timeout=3000)
            verdict = p.get_attribute('#qFb', 'data-verdict')
            want_right = kind == 'right'
            b.formats.add('%s %s' % (q['format'], 'right' if want_right else 'wrong'))
            if verdict != ('right' if want_right else 'wrong'):
                out.append('%s: %s typed %r was marked %s, expected %s' % (tag, ref, v, verdict, 'right' if want_right else 'wrong'))
            ev = [e for e in b.events[before:] if e[0] == 'question_answered']
            want_ev = {'game_slug': 'the-6-ps', 'level': 'all', 'correct': want_right,
                       'filter_type': 'six_ps', 'filter_value': 'v1|topic=' + topic['id']}
            if len(ev) != 1 or any(ev[0][1].get(k) != w for k, w in want_ev.items()):
                out.append('%s: %s: question_answered %s, expected one with %s' % (tag, ref, ev, want_ev))
            worked = q.get('worked') or []
            slip = p.is_visible('#qSlip')
            if want_right:
                right += 1
                if p.is_visible('#qAnswerLine') or slip or p.is_visible('#qWorked'):
                    out.append('%s: %s: a right answer shows the answer, a slip or the working straight away' % (tag, ref))
                if p.is_visible('#showWorkBtn') != bool(worked):
                    out.append('%s: %s: "Show the working" %s' % (tag, ref, 'missing' if worked else 'shown with no working'))
                if worked:
                    tap('#showWorkBtn')
                    if not p.is_visible('#qWorked') or p.eval_on_selector_all('#qWorked li', 'l => l.length') != len(worked):
                        out.append('%s: %s: one tap did not show the %d lines of working' % (tag, ref, len(worked)))
            else:
                want_slip = kind == 'wrong+slip'
                if slip != want_slip:
                    out.append('%s: %s typed %r: slip line %s' % (tag, ref, v, 'missing' if want_slip else 'shown'))
                elif want_slip and p.inner_text('#qSlip').strip() != q['slip'][0]['line']:
                    out.append('%s: %s: the slip line is %r' % (tag, ref, p.inner_text('#qSlip')))
                if p.is_visible('#qWorked') != bool(worked) or (worked and p.eval_on_selector_all('#qWorked li', 'l => l.length') != len(worked)):
                    out.append('%s: %s: a wrong answer does not show its %d lines of working' % (tag, ref, len(worked)))
                if slip and worked and p.evaluate("() => !(document.getElementById('qSlip').compareDocumentPosition(document.getElementById('qWorked')) & 4)"):
                    out.append('%s: %s: the slip line is not before the working' % (tag, ref))
                line = p.evaluate(ANSWER_LINE_JS) if p.is_visible('#qAnswerLine') else ''
                want_line = shown_answer(q)
                if not line.startswith('The answer: ') or (want_line and squash(line) != squash('The answer: ' + want_line)) or \
                        (q['format'] != 'choice' and not p.query_selector('#qAnswerLine .katex')):
                    out.append('%s: %s: answer line %r, expected %r drawn by KaTeX' % (tag, ref, line, want_line or '(KaTeX)'))
                if q['format'] == 'choice' and not p.query_selector('#qOpts button.key[data-val="%s"]' % q['answer']['val']):
                    out.append('%s: %s: the right option is not marked after a wrong answer' % (tag, ref))
            if narrow:
                sideways(p, '%s feedback' % ref, out)
        if stop_after is not None and len(asked) == stop_after:
            return None
        p.wait_for_selector('#qNext button:not([disabled])', timeout=3000)
        tap('#qNext button')
    if offset + len(asked) != PER_TOPIC or len(set(asked)) != len(asked):
        out.append('%s: topic %d asked %d questions (%d distinct), not five' % (tag, m, offset + len(asked), len(set(asked))))
    title = p.inner_text('#betweenName').strip()
    want = '%s: %d of %d' % (topic['name'], right, PER_TOPIC)
    if title != want or marks_text(topic) not in p.inner_text('#betweenWhat'):
        out.append('%s: topic card %r / %r, expected %r and its weight' % (tag, title, p.inner_text('#betweenWhat'), want))
    if not p.is_visible('#nextTopicBtn') or p.is_visible('#skipNotReadyBtn') or p.is_visible('#play'):
        out.append('%s: the topic card does not offer Next topic alone' % tag)
    if narrow:
        sideways(p, 'topic card %d' % m, out)
    return right


def bank_first_data(data):
    """The topic data cut to one bank-first topic (route null) and K more, all of equal weight, so that a session of K draws it six
    times in seven (the page draws in proportion to marks, and needs more topics than a session holds); None if the real file has
    no such topic."""
    if not any(t['route'] is None for t in data['covered']):
        return None
    forged = json.loads(json.dumps(data))
    keep = [t for t in forged['covered'] if t['route'] is None][:1]
    keep += [t for t in forged['covered'] if t['route'] is not None][:K]
    for t in keep:
        t['marks'] = 4.0
    forged['covered'] = keep
    return forged


def play_bank_first(pw, base, html, data, out):
    """A full session that has the bank-first topic in it (a fresh page until the draw includes it), checked as any other."""
    forged = bank_first_data(data)
    if forged is None:
        return
    need = forged['covered'][0]['id']
    for _ in range(25):
        got = []
        if play(pw, base, html, forged, got, blocked=False, served=forged, need=need) is not False:
            out.extend(got)
            return
    out.append('a session never drew the bank-first topic %s in 25 tries' % need)


def session_topics(p, data):
    names = {t['id']: t for t in data['covered']}
    return [names.get(x['id']) for x in p.evaluate('() => SixPs.session().plan')]


def play(pw, base, html, data, out, blocked, narrow=False, served=None, need=None):
    """A full session on the six fixture banks, to the results, resumed once mid-topic after a reload."""
    tag = '%s, %s' % ('320 px keypad' if narrow else '1280 px', 'storage blocked' if blocked else 'storage working')
    b = Browser(pw, base, html, size=(320, 700) if narrow else (1280, 800), blocked=blocked, served=served)
    p = b.page
    tap = p.tap if b.touch else p.click
    try:
        b.open()
        if narrow:
            sideways(p, 'start screen', out)
        soon = sorted(data['coming_soon'], key=lambda t: (-t['marks'], t['id']))
        top = visible_text(p, '#comingList li .name')
        if top != [t['name'] for t in soon[:3]]:
            out.append('%s: coming soon shows %s, not the three highest-mark topics' % (tag, top))
        label = p.inner_text('#comingMoreLabel').strip()
        if p.evaluate("() => document.getElementById('comingMore').open") or label != 'See all %d more topics' % (len(soon) - 3):
            out.append('%s: the rest of coming soon is not in a closed "See all %d more topics" (%r)' % (tag, len(soon) - 3, label))
        rest = p.evaluate("() => Array.from(document.querySelectorAll('#comingRest li .name')).map(e => e.textContent)")
        if rest != [t['name'] for t in soon[3:]]:
            out.append('%s: the closed list is %s' % (tag, rest))
        if p.inner_text('#sourceLine').strip() != data['source']:
            out.append('%s: the source line shows %r' % (tag, p.inner_text('#sourceLine')))
        tap('#startBtn')
        topics = session_topics(p, data)
        if need and need not in [t['id'] for t in topics if t]:
            return False                 # the draw left the topic out: the caller starts again
        if None in topics or len({t['id'] for t in topics}) != K:
            out.append('%s: the session is not six distinct covered topics: %s' % (tag, topics))
            return
        scores = []
        for m, t in enumerate(topics, 1):
            if m == 2:   # resumed mid-topic: two answered, the second's feedback still showing
                play_topic(b, m, t, out, tag, narrow, stop_after=2)
                cur = p.evaluate('() => SixPs.session().cur')
                b.open()
                if not p.is_visible('#intro') or not p.is_visible('#resumeBtn'):
                    out.append('%s: after a reload mid-topic the start screen offers no "Carry on"' % tag)
                    return
                tap('#resumeBtn')
                p.wait_for_selector('#play:not([hidden])', timeout=5000)
                now = p.evaluate('() => [SixPs.question().id, SixPs.session().cur]')
                if now[0] != cur['qids'][2] or now[1]['qids'] != cur['qids'] or now[1]['k'] != 2:
                    out.append('%s: resumed at %s (k %s), not question 3 of the same five' % (tag, now[0], now[1].get('k')))
                    return
                done = p.evaluate('() => SixPs.session().cur.right')
                scores.append(play_topic(b, m, t, out, tag, narrow, offset=2, right0=done))
            else:
                scores.append(play_topic(b, m, t, out, tag, narrow))
            if scores[-1] is None:
                return
            n_plan = p.eval_on_selector_all('#planList li', 'e => e.length')
            n_state = p.evaluate('() => SixPs.session().plan.length')
            if n_plan != K or n_state != K:
                out.append('%s: after topic %d "Your six" shows %d topics and the session holds %d, not %d' % (tag, m, n_plan, n_state, K))
            tap('#nextTopicBtn')
        p.wait_for_selector('#results:not([hidden])', timeout=5000)
        if narrow:
            sideways(p, 'the results', out)
        rows = visible_text(p, '#resultList li')
        if len(rows) != K:
            out.append('%s: the results list %d topics, not %d' % (tag, len(rows), K))
        links = p.evaluate("() => Array.from(document.querySelectorAll('#resultList li .more a')).map(a => [a.getAttribute('href'), a.textContent])")
        k_link = 0
        for k, t in enumerate(topics):
            row = rows[k] if k < len(rows) else ''
            want = '%s: %d of %d' % (t['name'], scores[k], PER_TOPIC)
            if t['route'] is None:      # a bank-first topic: its row has no practice link
                if want not in row or marks_text(t) not in row or 'Want more practice?' in row:
                    out.append('%s: results row %d (no game yet) is %r' % (tag, k + 1, row))
                continue
            if want not in row or marks_text(t) not in row or 'Want more practice? ' + t['route']['game'] not in row:
                out.append('%s: results row %d is %r' % (tag, k + 1, row))
            href = '/games/%s/?level=%s' % (t['route']['slug'], t['route']['level'])
            if k_link >= len(links) or links[k_link] != [href, t['route']['game']]:
                out.append('%s: row %d practice link %s, expected %s' % (tag, k + 1, links[k_link] if k_link < len(links) else None, href))
            k_link += 1
        played = [(t, s) for t, s in zip(topics, scores) if s < PER_TOPIC]
        if played:
            low = min(s for t, s in played)
            weakest = max((t for t, s in played if s == low), key=lambda t: t['marks'])
            nudge = p.inner_text('#nudge').strip()
            if weakest['name'] not in nudge or (weakest['route'] and weakest['route']['game'] not in nudge)                     or (weakest['route'] is None and 'Practise it' in nudge):
                out.append('%s: the nudge %r does not name the weakest topic, %s' % (tag, nudge, weakest['name']))
        ticks = p.evaluate("() => Array.from(document.querySelectorAll('#tickList input')).map(b => b.value)")
        if ticks != [t['id'] for t in data['coming_soon']] + ['other']:
            out.append('%s: the tick-list is %s, not the coming-soon topics plus "Something else"' % (tag, ticks))
            return
        pick = [data['coming_soon'][0]['id'], 'other']
        for v in pick:
            p.check('#tickList input[value="%s"]' % v)
        tap('#sendBtn')
        p.wait_for_selector('#thanks:not([hidden])', timeout=5000)
        names_ = [e[0] for e in b.events]
        fb = [e[1] for e in b.events if e[0] == 'six_ps_feedback']
        want_fb = {'topics': ','.join(pick), 'filter_type': 'six_ps', 'filter_value': 'v1|topics=' + ','.join(pick)}
        if fb != [want_fb]:
            out.append('%s: six_ps_feedback sent %s, expected one event %s' % (tag, fb, want_fb))
        st = [e[1] for e in b.events if e[0] == 'game_started']
        if st != [{'game_slug': 'the-6-ps', 'level': 'all'}]:
            out.append('%s: game_started sent %s, expected one for the session' % (tag, st))
        qa = [e[1] for e in b.events if e[0] == 'question_answered']
        if [e.get('question_index') for e in qa] != list(range(1, K * PER_TOPIC + 1)):
            out.append('%s: question_index ran %s, not 1 to 30' % (tag, [e.get('question_index') for e in qa]))
        fin = [e[1] for e in b.events if e[0] == 'game_completed']
        right = sum(scores)
        want_fin = {'game_slug': 'the-6-ps', 'level': 'all', 'score': right, 'questions_answered': K * PER_TOPIC,
                    'questions_correct': right}
        if fin != [want_fin]:
            out.append('%s: game_completed sent %s, expected %s' % (tag, fin, want_fin))
        other = sorted(set(names_) - {'game_started', 'question_answered', 'game_completed', 'six_ps_feedback'})
        if other:
            out.append('%s: events other than the four: %s' % (tag, other))
        if not blocked:
            seen = p.evaluate("() => JSON.parse(localStorage.getItem('six-ps-seen-v1') || '{}')")
            for t in topics:
                if len(seen.get(t['id'], [])) != PER_TOPIC:
                    out.append('%s: %s has %d ids in the seen list, not the five asked' % (tag, t['id'], len(seen.get(t['id'], []))))
        print('%s: played %s (%s), %d marked answers, %d never marked; formats %s' % (
            tag, scores, ', '.join(t['id'] for t in topics), len(qa), b.unmarked, ', '.join(sorted(b.formats))))
        b.open()   # a finished session is not shown again, and nothing is sent twice
        if not p.is_visible('#intro') or [e[0] for e in b.events].count('game_completed') != 1:
            out.append('%s: reopening the page after the results did not open the start screen cleanly' % tag)
        if len([w for w in b.warnings if 'left out' in w]) != 3:
            out.append('%s: %d schema warnings, expected the 3 for fx-6\'s left-out questions' % (tag, len([w for w in b.warnings if 'left out' in w])))
        out.extend('%s: page error: %s' % (tag, e) for e in b.errors)
    finally:
        b.close()


def no_bank(pw, base, html, data, out):
    """A drawn topic whose bank does not load: the card says so and offers Skip only; Skip moves on to the next."""
    tag = 'no bank'
    b = Browser(pw, base, html, size=(320, 700), queue=[None, 'fx-6'])
    p = b.page
    try:
        b.open()
        p.tap('#startBtn')
        p.wait_for_selector('#between:not([hidden])', timeout=5000)
        what = p.inner_text('#betweenWhat').strip()
        if what != 'This topic’s questions aren’t ready yet.':
            out.append('%s: the card says %r' % (tag, what))
        if not p.is_visible('#skipNotReadyBtn') or p.is_visible('#nextTopicBtn'):
            out.append('%s: the card does not offer Skip alone' % tag)
        sideways(p, 'the not-ready card', out)
        p.tap('#skipNotReadyBtn')
        p.wait_for_selector('#play:not([hidden])', timeout=5000)
        if p.inner_text('#qHead').strip() != 'Question 1 of 5':
            out.append('%s: after Skip the header is %r' % (tag, p.inner_text('#qHead')))
        if p.evaluate('() => SixPs.session().results[SixPs.session().plan[0].id]') != {'skipped': True}:
            out.append('%s: the topic was not recorded as skipped' % tag)
        out.extend('%s: page error: %s' % (tag, e) for e in b.errors)
    finally:
        b.close()


def check_start_screen(pw, base, html, out):
    """Start is on the screen at 320 x 568 without a scroll; the explainer is open on a first visit and closed on a return."""
    b = Browser(pw, base, html, size=(320, 568))
    try:
        b.open()
        pos = b.page.evaluate("() => { const s = document.getElementById('startBtn').getBoundingClientRect(); "
                              "return { bottom: Math.round(s.bottom), vh: innerHeight, open: document.getElementById('aboutBox').open }; }")
        if pos['bottom'] > pos['vh']:
            out.append('the start screen at 320 x 568: Start ends at %d px, below the %d px fold' % (pos['bottom'], pos['vh']))
        if not pos['open']:
            out.append('the start screen: the explainer is closed on a first visit')
        b.page.reload()
        b.page.wait_for_function("() => !!window.SixPs && !!SixPs.data()", timeout=10000)
        if b.page.evaluate("() => document.getElementById('aboutBox').open"):
            out.append('the start screen: the explainer is open on a return visit (it should be under "About The 6 P\u2019s", closed)')
        out.extend('start screen: page error: %s' % e for e in b.errors)
    finally:
        b.close()


def check_expiry(pw, base, html, data, out):
    """A saved session is offered for four hours and then not: one ten minutes old is, one five hours old is not."""
    for age_h, offered in ((0.2, True), (5, False)):
        b = Browser(pw, base, html)
        try:
            ids = [t['id'] for t in data['covered']][:K]
            sess = {'v': 2, 'plan': [{'id': x} for x in ids], 'i': 0, 'results': {}, 'cur': None, 'qn': 0, 'finishedSent': False,
                    'feedbackSent': False, 'at': 0}
            b.ctx.add_init_script("try { var s = %s; s.at = Date.now() - %d; localStorage.setItem('six-ps-session-v2', JSON.stringify(s)); } catch (e) {}"
                                  % (json.dumps(sess), int(age_h * 3600 * 1000)))
            b.open()
            if b.page.is_visible('#resumeBtn') != offered:
                out.append('a saved session %s hours old is %s: stale session offered' % (age_h, 'not offered' if offered else 'offered'))
        finally:
            b.close()


def check_chosen(pw, base, html, out):
    """A unit picked but not yet checked is navy, never the green or red that means right or wrong."""
    b = Browser(pw, base, html, queue=['fx-5'] * K)
    try:
        b.open()
        b.page.click('#startBtn')
        b.page.wait_for_selector('#qUnits button', timeout=5000)
        b.page.click('#qUnits button')
        col = b.page.evaluate("() => getComputedStyle(document.querySelector('#qUnits button[aria-pressed=true]')).borderTopColor")
        if col != 'rgb(26, 39, 68)':
            out.append('a unit chosen but not checked has the border %s, not navy: it reads as right or wrong' % col)
    finally:
        b.close()


def check_resume_finish(pw, base, html, data, out):
    """Jon's phone, 27 Oct: a refresh and Carry on in the middle of a session, then a topic of choice questions to its fifth answer. Each answer,
    the fifth included, must show its verdict and Next, with no page error; the topic card then lists six and Next topic moves on by one."""
    topic = 'powers-roots'               # a real bank of nothing but multiple choice
    b = Browser(pw, base, html, size=(375, 667))
    b.real[topic] = json.load(open(os.path.join(ROOT, 'schools', 'assets', 'six-ps', topic + '.json'), encoding='utf-8'))
    try:
        b.open()
        others = [x['id'] for x in data['covered'] if x['id'] != topic][:5]
        sess = {'v': 2, 'plan': [{'id': x} for x in [others[0], topic] + others[1:5]], 'i': 1, 'results': {others[0]: {'r': 4, 'n': 5}},
                'cur': None, 'qn': 5, 'finishedSent': False, 'feedbackSent': False}
        b.page.evaluate("s => localStorage.setItem('six-ps-session-v2', s)", json.dumps(dict(sess, at=int(time.time() * 1000))))
        b.page.reload()
        b.page.wait_for_function("() => !!window.SixPs && !!SixPs.data()", timeout=10000)
        b.page.tap('#resumeBtn')
        for n in range(PER_TOPIC):
            b.page.wait_for_selector('#play:not([hidden])', timeout=8000)
            q = b.page.evaluate('() => SixPs.question()')
            answer(b, q, real_value(q, wrong=False))
            try:
                b.page.wait_for_selector('#qFb:not([hidden])', timeout=4000)
            except Exception:
                out.append('after a resume, question %d of 5 (%s) showed no feedback' % (n + 1, q['format']))
                return
            if not b.page.query_selector('#qNext button'):
                out.append('after a resume, question %d of 5 showed no Next' % (n + 1))
                return
            b.page.tap('#qNext button')
        b.page.wait_for_selector('#between:not([hidden])', timeout=5000)
        rows = b.page.eval_on_selector_all('#planList li', 'e => e.length')
        if rows != K:
            out.append('after a resume and a finished topic "Your six" shows %d topics, not %d' % (rows, K))
        b.page.tap('#nextTopicBtn')
        if b.page.evaluate('() => SixPs.session().i') != 2:
            out.append('Next topic after a resume did not move on by exactly one topic')
        out.extend('resume and finish a topic: page error: %s' % e for e in b.errors)
    finally:
        b.close()


def check_results_once(pw, base, html, data, out):
    """Jon's phone, 27 Oct: the results screen showed the tick list from Quadratic graphs on, and Send, twice. Everything on the screen is
    drawn once: one list of topics, one form, one legend, one tick list with every topic once, one Send, one Another six, and the page
    text holds each topic's row and tick once. Looked at after the finish, after the page is restored from the back-forward cache, after
    the page script runs a second time, and after Send."""
    topic = 'powers-roots'
    b = Browser(pw, base, html, size=(375, 667))
    b.real[topic] = json.load(open(os.path.join(ROOT, 'schools', 'assets', 'six-ps', topic + '.json'), encoding='utf-8'))
    COUNT = """() => {
      const vis = e => !!(e.offsetParent || e.getClientRects().length);
      const text = sel => [...document.querySelectorAll(sel)].filter(vis).map(e => e.textContent.trim());
      const dup = a => a.filter((x, i) => a.indexOf(x) !== i);
      return {
        lists: [...document.querySelectorAll('#results ul')].filter(vis).length,
        forms: [...document.querySelectorAll('#results form')].filter(vis).length,
        legends: text('#results legend').length,
        send: text('#results button').filter(t => t === 'Send').length,
        again: text('#results button').filter(t => t === 'Another six').length,
        ticks: text('#tickList label'), rows: text('#resultList > li'),
        heads: text('#results h2').length, ids: ['resultList', 'tickList', 'feedbackForm', 'sendBtn', 'againBtn', 'nudge', 'thanks']
          .filter(i => document.querySelectorAll('[id=' + i + ']').length > 1)
      };
    }"""
    def look(tag, sent=False):
        c = b.page.evaluate(COUNT)
        for k, want in (('lists', 1), ('forms', 1), ('legends', 1), ('send', 0 if sent else 1), ('again', 1), ('heads', 1)):
            if c[k] != want:
                out.append('results screen %s: %s appears %d times, not %d' % (tag, k, c[k], want))
        if len(c['ticks']) != len(set(c['ticks'])):
            out.append('results screen %s: the tick list repeats %s' % (tag, sorted({t for t in c['ticks'] if c['ticks'].count(t) > 1})[:3]))
        if len(c['rows']) != len(set(c['rows'])) or len(c['rows']) != K:
            out.append('results screen %s: %d topic rows, %d different (want %d)' % (tag, len(c['rows']), len(set(c['rows'])), K))
        if c['ids']:
            out.append('results screen %s: ids used twice: %s' % (tag, c['ids']))
    try:
        b.open()
        others = [x['id'] for x in data['covered'] if x['id'] != topic][:5]
        sess = {'v': 2, 'plan': [{'id': x} for x in others + [topic]], 'i': 5, 'results': {x: {'r': 4, 'n': 5} for x in others},
                'cur': None, 'qn': 25, 'finishedSent': False, 'feedbackSent': False}
        b.page.evaluate("s => localStorage.setItem('six-ps-session-v2', s)", json.dumps(dict(sess, at=int(time.time() * 1000))))
        b.page.reload()
        b.page.wait_for_function("() => !!window.SixPs && !!SixPs.data()", timeout=10000)
        b.page.tap('#resumeBtn')
        for n in range(PER_TOPIC):
            b.page.wait_for_selector('#play:not([hidden])', timeout=8000)
            q = b.page.evaluate('() => SixPs.question()')
            answer(b, q, real_value(q, wrong=False))
            b.page.wait_for_selector('#qFb:not([hidden])', timeout=4000)
            b.page.tap('#qNext button')
        b.page.wait_for_selector('#between:not([hidden])', timeout=5000)
        b.page.tap('#nextTopicBtn')
        b.page.wait_for_selector('#results:not([hidden])', timeout=5000)
        look('after the finish')
        script = re.search(r'<script>\s*(/\* The 6 P.s \(contract.*?)</script>', html, re.S).group(1)
        b.page.evaluate("src => { const s = document.createElement('script'); s.textContent = src; document.body.appendChild(s); }", script)
        b.page.wait_for_timeout(300)
        look('after the page script ran a second time')
        b.page.tap('#tickList input')
        b.page.tap('#sendBtn')
        b.page.wait_for_timeout(300)
        look('after Send', sent=True)
        # the page restored from the back-forward cache starts again from the saved session: the results come back drawn once
        b.page.evaluate("() => window.dispatchEvent(new PageTransitionEvent('pageshow', {persisted: true}))")
        b.page.wait_for_timeout(300)
        b.page.reload()
        b.page.wait_for_function("() => !!window.SixPs && !!SixPs.data()", timeout=10000)
        if b.page.evaluate("() => document.querySelectorAll('#results form').length") > 1:
            out.append('results screen after a reload: the page holds %d feedback forms'
                       % b.page.evaluate("() => document.querySelectorAll('#results form').length"))
        out.extend('results screen: page error: %s' % e for e in b.errors)
    finally:
        b.close()


def check_second_copy(pw, base, html, data, out):
    """A page whose script runs twice (a browser that re-runs scripts on resume) still behaves as one: Next topic moves on by one, and
    one answer sends one event."""
    b = Browser(pw, base, html)
    try:
        b.open()
        script = re.search(r'<script>\s*(/\* The 6 P.s \(contract.*?)</script>', html, re.S).group(1)
        b.page.evaluate("src => { const s = document.createElement('script'); s.textContent = src; document.body.appendChild(s); }", script)
        b.page.click('#startBtn')
        starts = len([e for e in b.events if e[0] == 'game_started'])
        if starts != 1:
            out.append('with the page script run twice, one Start sent %d game_started events (each copy started its own session)' % starts)
        t = session_topics(b.page, data)[0]
        play_topic(b, 1, t, out, 'second copy')
        b.page.click('#nextTopicBtn')
        i = b.page.evaluate('() => SixPs.session().i')
        if i != 1:
            out.append('with the page script run twice, Next topic moved on %d topics, not 1' % i)
        n = len([e for e in b.events if e[0] == 'question_answered'])
        if n != PER_TOPIC:
            out.append('with the page script run twice, %d answers sent %d events' % (PER_TOPIC, n))
    finally:
        b.close()


def real_value(q, wrong=False):
    """A typed value for a real question: its own answer, or one that is wrong."""
    a, f = q['answer'], q['format']
    if f == 'choice':
        return next(o['val'] for o in q['options'] if (o['val'] != a['val']) == wrong and (wrong or o['val'] == a['val']))
    if f == 'number':
        return '7' if wrong else (('%.*f' % (a['dp'], a['value'])) if 'dp' in a else js_num(a['value']))
    if f == 'money':
        return '1.23' if wrong else '%.2f' % (a['pence'] / 100)
    if f == 'fraction':
        return {'whole': '', 'num': '9', 'den': '13'} if wrong else \
            {'whole': str(a['w']) if 'w' in a else '', 'num': str(a['n']), 'den': str(a['d'])}
    if f == 'ratio':
        return ['7', '9'] if wrong else [js_num(p) for p in a['parts']]
    if f in ('coordinates', 'pair'):
        return {'x': '8', 'y': '9'} if wrong else {'x': js_num(a['x']), 'y': js_num(a['y'])}
    if f == 'standard_form':
        return {'m': '9', 'e': '9'} if wrong else {'m': js_num(a['m']), 'e': js_num(a['e'])}
    if f == 'number_unit':
        return ('7', a['unit']) if wrong else (js_num(a['value']), a['unit'])
    raise AssertionError(f)


def phone_feedback_topic(pw, base, html, data, topic, out, only=None):
    """One real bank on a 375 x 667 touch screen: one answer right and one wrong, each measured after Check.
    `only` serves five copies of that one question and answers it wrong at once, so what is measured is always the same."""
    bank = json.load(open(os.path.join(ROOT, 'schools', 'assets', 'six-ps', topic['id'] + '.json'), encoding='utf-8'))
    if only is not None:
        one = [x for x in bank['questions'] if x['id'] == only]
        if len(one) != 1:
            raise AssertionError('%s: the question %s is not in the bank' % (topic['id'], only))
        bank['questions'] = [dict(one[0], id='%s-c%d' % (only, i)) for i in range(5)]
    b = Browser(pw, base, html, size=(375, 667))
    b.page.set_default_timeout(20000)      # a loaded machine runs many of these at once
    b.real[topic['id']] = bank
    others = [x['id'] for x in data['covered'] if x['id'] != topic['id']][:K - 1]
    sess = {'v': 2, 'plan': [{'id': x} for x in [topic['id']] + others], 'i': 0, 'results': {}, 'cur': None, 'qn': 0,
            'finishedSent': False, 'feedbackSent': False}
    b.ctx.add_init_script("try { var s = %s; s.at = Date.now(); localStorage.setItem('six-ps-session-v2', JSON.stringify(s)); } catch (e) {}" % json.dumps(sess))
    try:
        b.open()
        b.page.tap('#resumeBtn')
        for n, wrong in enumerate((True,) if only is not None else (False, True)):   # `only`: the wrong answer first, before the maths font is loaded
            b.page.wait_for_selector('#play:not([hidden])', timeout=8000)
            q = b.page.evaluate('() => SixPs.question()')
            answer(b, q, real_value(q, wrong))
            b.page.wait_for_selector('#qFb:not([hidden])', timeout=8000)
            m = b.page.evaluate("""() => { const r = id => { const e = document.getElementById(id); return e && !e.hidden ? e.getBoundingClientRect() : null; };
                const nb = document.querySelector('#qNext button'), nr = nb ? nb.getBoundingClientRect() : null, vr = r('qVerdict');
                return { verdict: vr ? [Math.round(vr.top), Math.round(vr.bottom)] : null, next: nr ? [Math.round(nr.top), Math.round(nr.bottom)] : null,
                         vh: innerHeight, sx: document.documentElement.scrollWidth - innerWidth, keys: !document.getElementById('qKeys').hidden }; }""")
            what = '%s %s (%s, %s)' % (topic['id'], q['id'], q['format'], 'wrong' if wrong else 'right')
            if m['keys']:
                out.append('375 x 667: %s: the keypad is still showing after Check' % what)
            if not m['verdict'] or m['verdict'][0] < 0 or m['verdict'][1] > m['vh']:
                out.append('375 x 667: %s: the verdict is not on the screen (%s of %d px)' % (what, m['verdict'], m['vh']))
            if not m['next'] or m['next'][1] > m['vh']:
                out.append('375 x 667: %s: Next is not on the screen (%s of %d px)' % (what, m['next'], m['vh']))
            if m['sx'] > 0:
                out.append('375 x 667: %s: the page scrolls sideways by %d px' % (what, m['sx']))
            if n == 0:
                b.page.tap('#qNext button')
        out.extend('375 x 667: %s: page error: %s' % (topic['id'], e) for e in b.errors)
    finally:
        b.close()


# On a 375 x 667 phone, on every real bank (each its own unit, PHONE + topic id): after Check the keypad is gone and the verdict and
# Next are on the screen with no scroll, one answer right and one wrong, and nothing scrolls sideways. One topic's trouble is reported
# against it and the rest are still measured.
PHONE = 'phone feedback: '


# Working with three fractions is the tallest feedback a bank has: on 375 x 667 it ends 15 px below the screen unless the page scrolls
# again once the maths font has arrived (main run 40479208314). Nine questions of this topic did; this one is measured every time.
TALL = ('fraction-percentage-of-amount', 'fraction-percentage-of-amount-2c420fec')


def check_tall(pw, base, html, data, out):
    topic = [t for t in data['covered'] if t['id'] == TALL[0]]
    if not topic:
        raise AssertionError('%s is not a covered topic' % TALL[0])
    phone_feedback_topic(pw, base, html, data, topic[0], out, only=TALL[1])


def one_topic(pw, base, html, data, out, name):
    """One topic on fixture `name`, to its card (the plants' short flow)."""
    b = Browser(pw, base, html, queue=[name] * K)
    try:
        b.open()
        b.page.click('#startBtn')
        t = session_topics(b.page, data)[0]
        play_topic(b, 1, t, out, 'one topic (%s)' % name)
        out.extend('one topic: page error: %s' % e for e in b.errors)
    finally:
        b.close()


def page_units(data):
    """The page's units (contract SHARD), in the order of the full run; check() runs those it is given, in this order."""
    return (['static', 'engine', 'marking', 'start', 'expiry', 'chosen', 'resume', 'results', 'second']
            + [PHONE + t['id'] for t in data['covered']] + ['tall', 'play 1280', 'play bank-first', 'play 320', 'no bank'])


def run_unit(pw, base, html, data, out, unit):
    """One browser unit of page_units(), or 'topic:<fixture>' (one topic to its card, the plants' short flow)."""
    if unit in ('engine', 'marking'):
        b = Browser(pw, base, html)
        try:
            b.open()
            if unit == 'engine':
                guarded(out, 'the draws', lambda: check_engine(b, data, out))
            else:
                guarded(out, 'the marking checks', lambda: check_marking(b, out))
            out.extend('page error: ' + e for e in b.errors)
        finally:
            b.close()
    elif unit == 'start':
        guarded(out, 'the start screen at 320 x 568', lambda: check_start_screen(pw, base, html, out))
    elif unit == 'expiry':
        guarded(out, 'the saved-session expiry', lambda: check_expiry(pw, base, html, data, out))
    elif unit == 'chosen':
        guarded(out, 'the chosen-unit colour', lambda: check_chosen(pw, base, html, out))
    elif unit == 'resume':
        guarded(out, 'a refresh and Carry on, then a finished topic of choice questions',
                lambda: check_resume_finish(pw, base, html, data, out))
    elif unit == 'results':
        guarded(out, 'the results screen drawn once', lambda: check_results_once(pw, base, html, data, out))
    elif unit == 'second':
        guarded(out, 'the page script run twice', lambda: check_second_copy(pw, base, html, data, out))
    elif unit.startswith(PHONE):
        topic = [t for t in data['covered'] if t['id'] == unit[len(PHONE):]][0]
        guarded(out, '375 x 667: %s' % topic['id'], lambda: phone_feedback_topic(pw, base, html, data, topic, out))
    elif unit == 'tall':
        guarded(out, 'the tallest feedback on a 375 x 667 phone', lambda: check_tall(pw, base, html, data, out))
    elif unit == 'play 1280':
        guarded(out, 'the session at 1280 px', lambda: play(pw, base, html, data, out, blocked=False))
    elif unit == 'play bank-first':
        guarded(out, 'the session with a bank-first topic (no game yet)', lambda: play_bank_first(pw, base, html, data, out))
    elif unit == 'play 320':
        guarded(out, 'the session at 320 px', lambda: play(pw, base, html, data, out, blocked=True, narrow=True))
    elif unit == 'no bank':
        guarded(out, 'the topic with no bank', lambda: no_bank(pw, base, html, data, out))
    elif unit.startswith('topic:'):
        guarded(out, 'one topic', lambda: one_topic(pw, base, html, data, out, unit[6:]))
    else:
        raise ValueError('no unit %r' % unit)


def check(html, data, out, parts, shard=None):
    """The units named in `parts` (page_units() order, then any 'topic:<fixture>'), each timed as its unit by `shard`."""
    from playwright.sync_api import sync_playwright
    units = [u for u in page_units(data) if u in parts] + [u for u in parts if u.startswith('topic:')]

    def timed(u):
        return shard.unit(u) if shard else contextlib.nullcontext()
    if 'static' in units:
        with timed('static'):
            static_checks(html, data, out)
    units = [u for u in units if u != 'static']
    if not units:
        return
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            for u in units:
                with timed(u):
                    run_unit(pw, base, html, data, out, u)
    finally:
        proc.terminate()


def guarded(out, what, f):
    try:
        f()
    except Exception as e:  # a crash in a check is a failure, never a pass
        out.append('%s stopped: %s: %s' % (what, type(e).__name__, str(e).splitlines()[0] if str(e) else ''))


# ---------------------------------------------------------------- plants
# (what, [(old, new)], what it needs, a pattern its finding must match). Every old text occurs exactly once in the page.
PLANTS = [
    ('a results screen that draws its form twice (Jon, 27 Oct)',
     [("$('resultsBody').replaceChildren(list, nudge, form, againRow);", "$('resultsBody').replaceChildren(list, nudge, form, againRow, form.cloneNode(true));")],
     ['results'], r'results screen after the finish: (forms|send|legends) appears 2 times'),
    ('a results screen whose tick list repeats a topic',
     [("    fill(ticks, data.coming_soon.map(function (t) { return [t.id, t.name]; })", "    fill(ticks, data.coming_soon.concat(data.coming_soon.slice(-2)).map(function (t) { return [t.id, t.name]; })")],
     ['results'], r'results screen after the finish: the tick list repeats'),
    ('a sixth question shown (a topic of six)',
     [('var PER_TOPIC = 5;', 'var PER_TOPIC = 6;')],
     ['topic:fx-seen'], r'Question 6 of 6|asked 6 questions'),
    ('an answer marked by string (a number compared as text: 6.50 is not "6.5")',
     [("r = numberResult(inp.value, ans, rangeFor(q, acc, ans));\n        return { result: r, msg: MaffsAnswer.message(r, inp.value, { dp: ans.dp }) };",
       "r = String(inp.value).trim() === String(ans.value) ? 'correct' : 'wrong';\n        return { result: r, msg: '' };")],
     ['marking'], r"typed '6\.50' gave 'wrong'"),
    ('a choice marked by its label, not its dataset.val',
     [("return { result: inp.val === ans.val ? 'correct' : 'wrong', msg: '' };",
       "return { result: inp.val === (q.options.filter(function (o) { return o.val === ans.val; })[0] || {}).label ? 'correct' : 'wrong', msg: '' };")],
     ['marking'], r"fx-4\[\d\] typed '[a-d]' gave 'wrong', expected 'correct'"),
    ('a wrong answer marked right (a ratio out of proportion)',
     [("if (!prop) return { result: 'wrong', msg: '' };", "if (!prop) return { result: 'correct', msg: '' };")],
     ['marking'], r"fx-3\[2\] typed \['5', '2'\] gave 'correct'"),
    ('a coming-soon topic drawn into a session (given a band and a route, so it reaches one)',
     [('var topics = data.covered, picked', 'var topics = data.covered.concat(data.coming_soon.map(function (t) { '
       'return Object.assign({ band: [1, 1], route: { slug: "x", game: "x", level: "x", modes: [] } }, t); })), picked')],
     ['engine'], r'coming-soon topic'),
    ('"in development" restored',
     [("These topics carry marks too, and they're next on the list.", "These topics carry marks too, and their games are in development.")],
     ['static'], r'"in development" appears'),
    ('a list drawn twice appends to itself ("Your six" doubled after a resume)',
     [("    el.textContent = '';\n    el.appendChild(frag);", "    el.appendChild(frag);")],
     ['start', 'expiry', 'chosen', 'play 1280', 'play bank-first'], r'"Your six" shows'),
    ('a unit chosen but not checked drawn green',
     [("border-color: var(--navy); background: #e8ecf5; box-shadow: inset 0 0 0 1px var(--navy); }   /* chosen, not checked: navy */",
       "border-color: var(--correct); background: #e8ecf5; box-shadow: inset 0 0 0 1px var(--correct); }")],
     ['chosen'], r'not navy'),
    ('a standard-form answer of 45 x 10^3 marked correct',
     [("if (!(Math.abs(m) >= 1 && Math.abs(m) < 10)) {", "if (false) {")],
     ['marking'], r"fx-4\[4\] typed .* gave 'correct', expected 'format'"),
    ('a session left five hours still offered',
     [("(now === undefined ? Date.now() : now) - s.at > SESSION_MAX_MS", "false")],
     ['expiry'], r'stale session offered'),
    ('a feedback that throws on the fifth answer and no plain feedback to stand in',
     [("    fb.dataset.verdict = right ? 'right' : 'wrong';\n    $('qVerdict').textContent = right ? '\\u2713 Correct' : '\\u2717 Not quite';\n    $('qKeys').hidden = true;                // the keypad has done its job",
       "    if (last) throw new Error('planted');\n    fb.dataset.verdict = right ? 'right' : 'wrong';\n    $('qVerdict').textContent = right ? '\\u2713 Correct' : '\\u2717 Not quite';\n    $('qKeys').hidden = true;                // the keypad has done its job"),
      ("      plainFeedback(right, last);\n    }\n  }", "    }\n  }")],
     ['resume'], r'showed no feedback'),
    ('the page script run twice with no guard against it',
     [("  if (window.SixPs) {   // the page script ran twice in one window", "  if (false) {   // the page script ran twice in one window")],
     ['second'], r'page script run twice'),
    ('the feedback not scrolled into view again once the maths font has arrived',
     [("        inView();\n        if (document.fonts && document.fonts.ready) document.fonts.ready.then(inView);\n", ""),
      ("      if (window.ResizeObserver) {\n        var watch = new ResizeObserver(inView);", "      if (false) {\n        var watch = new ResizeObserver(inView);")],
     ['tall'], r'Next is not on the screen'),
    ('a calculator-optional question labelled "Calculator"',
     [("$('qCalc').textContent = q.calc === 'optional' ? 'Calculator optional' : q.calc ? 'Calculator' : 'Non-calculator';",
       "$('qCalc').textContent = q.calc ? 'Calculator' : 'Non-calculator';")],
     ['topic:fx-6'], r"calculator tag 'Calculator'"),
    ('the "Try without a calculator" prompt shown on every question',
     [("$('qTry').hidden = !(q.calc === 'optional' && q.try_without === true);", "$('qTry').hidden = false;")],
     ['topic:fx-6'], r'prompt is shown, expected False'),
    ('a right value in the wrong form marked wrong (SR-3)',
     [("if (res.result !== 'correct' && res.result !== 'wrong') {", "if (res.result === 'unreadable' || res.result === 'nounit') {")],
     ['topic:fx-2'], r"\(format\) was marked"),
    ('money at 1 d.p. accepted (SR-2)',
     [("r = MaffsAnswer.money(inp.value, ans.pence / 100);", "r = MaffsAnswer.exact(String(inp.value).replace(/^£/, ''), ans.pence / 100);")],
     ['marking'], r"fx-1\[3\] typed '3\.5' gave 'correct', expected 'format'"),
]


def plant_id(what):
    return 'plant: ' + what


DATA_PLANT = plant_id('a figure in the data file edited by hand')


def selftest(html, data, names, shard=None):
    """The plants named in `names` (plant_id), each its own unit."""
    def timed(u):
        return shard.unit(u) if shard else contextlib.nullcontext()
    ok = True
    for what, edits, needs, want in PLANTS:
        if plant_id(what) not in names:
            continue
        with timed(plant_id(what)):
            planted = html
            for old, new in edits:
                if planted.count(old) != 1:
                    print('FAIL  plant %r: its text occurs %d times in the page' % (what, planted.count(old)))
                    ok = False
                    break
                planted = planted.replace(old, new)
            else:
                got = []
                if needs == ['static']:
                    static_checks(planted, data, got)
                else:
                    check(planted, data, got, needs)
                if any(re.search(want, g) for g in got):
                    print('ok    plant caught: %s' % what)
                else:
                    print('FAIL  plant NOT caught: %s (findings: %s)' % (what, got[:3]))
                    ok = False
    if DATA_PLANT in names:
        with timed(DATA_PLANT):
            forged = json.loads(json.dumps(data))
            forged['covered'][0]['marks'] += 1
            got = []
            check_data(forged, got)
            if any('not what scripts/gen-exam-topics.py generates' in g for g in got):
                print('ok    plant caught: a figure in the data file edited by hand')
            else:
                print('FAIL  plant NOT caught: a figure in the data file edited by hand')
                ok = False
    return ok


def main():
    ap = argparse.ArgumentParser()
    bc.shard_args(ap)
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    with open(PAGE, encoding='utf-8') as f:
        html = f.read()
    data = load_data()
    # Every unit, in the order of the full run: the data and routes, the page's units, then the plants.
    plants = [plant_id(p[0]) for p in PLANTS] + [DATA_PLANT]
    shard = bc.Shard(__file__, args)
    mine = shard.pick(['data and routes'] + page_units(data) + plants)
    out = []
    ok = True
    if 'data and routes' in mine:
        with shard.unit('data and routes'):
            check_data(data, out)
            check_routes(data, out)
        W = sum(t['marks'] for t in data['covered'])
        print('the-6-ps: %d covered topics (%.1f marks a series), %d coming soon; %d sessions drawn each way; '
              '%d fixture questions' % (len(data['covered']), W, len(data['coming_soon']), DRAWS, len(by_ref())))
    run = [u for u in mine if u in page_units(data)]
    if run:
        check(html, data, out, run, shard)
    if any(u in plants for u in mine):
        ok = selftest(html, data, mine, shard) and ok
    for f in out[:60]:
        print('FAIL  ' + f)
    if len(out) > 60:
        print('FAIL  ... and %d more' % (len(out) - 60))
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if out or not ok else 'PASS')
    return 1 if out or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
