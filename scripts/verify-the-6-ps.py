#!/usr/bin/env python3
# ci-line: The 6 P's, part 1 (the topic data file is the generator's output; no mark figure, AQA or Edexcel typed in the page; the four past-paper sites linked before Start; every route's game declares its level and every launch link carries the burst parameters; 10,000 sessions each way: six distinct covered topics in band order, frequencies in proportion to marks; a full session played back through return links with localStorage working and blocked, results, nudge and tick-list event; 320 px without sideways scroll) | --part 1
# ci-line: The 6 P's, part 2a (every COVERED route, each mode, opened in its real game from the page's link through burst.js: in a burst, at its level, at its stage as the game's own game_started reports it, five answers played, the return bar linking to /the-6-ps/?done=<id>&r=&n=5; a third of the routes) | --part 2 --shard 1/3
# ci-line: The 6 P's, part 2b (the routes' launch checks, as part 2a: the second third) | --part 2 --shard 2/3
# ci-line: The 6 P's, part 2c (the routes' launch checks, as part 2a: the last third) | --part 2 --shard 3/3
# ci-line: The 6 P's, part 3 (fault-injection self-test: the planted faults, each caught) | --part 3
# ci-line: The 6 P's, part 4 (a full session through the page and the real games: Start, each topic's link followed into its game, five answers, the return bar followed back, six times; the results show each score) | --part 4
# ci-deps: the-6-ps/ schools/assets/exam-topics-ocr-foundation.json scripts/gen-exam-topics.py
"""Independent verification for The 6 P's (/the-6-ps/), built 24 Oct 2026 (contract THE-6-PS, Jon).

WHAT IS CHECKED, AND AGAINST WHAT
-------------------------------------------------------------------------------
  Data       schools/assets/exam-topics-ocr-foundation.json equals what scripts/gen-exam-topics.py builds from its
             table (compared as data). The page types no figure: no number next to "mark", no audit figure (13.3,
             ...) and not the source sentence; every figure it shows is read from the file.
  Claims     neither "AQA" nor "Edexcel" appears in the page (the contract: never claim their weightings); the four
             past-paper sites are linked, each before the Start button.
  Routes     every COVERED route's game exists and declares its level in MaffsLevel.resolve; every launch link, for
             every mode the route offers, is /games/<slug>/?level=<level>[&mode=<mode>]&burst=5&from=six-ps&topic=<id>.
  Launches   (part 2, three shards) every route, each mode, opened in its real game from the page's own link, driven as
             scripts/check-burst.py drives it (its contexts and the answer-lock driver; KaTeX served from the pinned
             copy): burst.js active, the level taken from the link, the stage the one the game's own game_started
             reports (a pressed button alone proves nothing), five answers, and the return bar linking to
             /the-6-ps/?done=<id>&r=<right>&n=5. The games are never stubbed.
  Session    (part 4) one full session through the page and the real games and back, six topics, to the results.
  Sessions   the page's own plan(), run 10,000 times with storage blocked (systematic sampling) and 10,000 times on
             one device (the rotation): every session is six distinct COVERED topics in Jon's band order (lower bound,
             then upper), and each topic's frequency is within tolerance of 10,000 x 6 x marks / total marks. Random
             draws: within 4.5 standard deviations (binomial) plus 2; the rotation, which is deterministic, within 3.
             On the rotation, no topic waits longer than twice its expected gap after the first 200 sessions.
  Flow       played in Chromium with localStorage working and with it blocked (every access throws): Start, each
             topic's link read from the page, a return link ?done=<id>&r=&n= for each (one topic skipped), a forged
             return (wrong topic, r > n) ignored; the results list each topic with its score and "worth about X marks
             a series on OCR's Foundation papers", X the file's marks rounded; the nudge names the weakest topic
             played; the tick-list is exactly the coming-soon topics plus "Something else", and sends one
             six_ps_feedback event whose only fields are the topic ids (topics, and the same ids packed in
             filter_type/filter_value for the Sheet, Jon's ruling of 24 Oct 2026).
  Phone      the start screen, a session and the results at 320 px: no sideways scroll.

    python scripts/verify-the-6-ps.py              # every part
    python scripts/verify-the-6-ps.py --part 1     # the checks
    python scripts/verify-the-6-ps.py --part 2 [--shard k/3]   # every route launched in its real game
    python scripts/verify-the-6-ps.py --part 3     # the plants
    python scripts/verify-the-6-ps.py --part 4     # a full session through the real games
"""
import argparse
import importlib.util
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

PAGE = os.path.join(ROOT, 'the-6-ps', 'index.html')
DATA = os.path.join(ROOT, 'schools', 'assets', 'exam-topics-ocr-foundation.json')
BURST_JS = os.path.join(ROOT, 'schools', 'assets', 'burst.js')
K, BURST = 6, 5
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


def static_checks(html, data, out):
    if '<meta name="robots" content="noindex">' not in html:
        out.append('the page is not noindex (it is unlisted until Jon has played it)')
    if '<!-- UNLISTED' not in html:
        out.append('the page has no UNLISTED comment')
    if not re.search(r'<script src="/schools/assets/analytics\.js"></script>', html):
        out.append('the page does not load analytics.js')
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
    start = html.find('id="startBtn"')
    for url in SITES:
        at = html.find('href="%s"' % url)
        if at < 0:
            out.append('the page does not link %s' % url)
        elif start >= 0 and at > start:
            out.append('%s is linked after the Start button' % url)
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
    for t in data['covered']:
        r = t['route']
        levels = declared_levels(r['slug'])
        if levels is None:
            out.append('%s: no game at games/%s/' % (t['id'], r['slug']))
        elif r['level'] not in levels:
            out.append('%s: %s does not declare level %r (it declares %s)' % (t['id'], r['slug'], r['level'], levels))


def about(marks):
    """Marks as the page says them, 'about N': rounded half up (6.5 is 7; Python's round() would say 6), at least 1."""
    return max(1, int(math.floor(marks + 0.5)))


def openers(t):
    """[(mode, stage)] a route may open its game at: each mode, or each stage, or neither."""
    r = t['route']
    return [(m, '') for m in r['modes']] + [('', st) for st in r.get('stages', [])] or [('', '')]


def expected_launch(t, mode, stage=''):
    q = 'level=%s' % t['route']['level']
    if mode:
        q += '&mode=%s' % mode
    if stage:
        q += '&stage=%s' % stage
    return '/games/%s/?%s&burst=%d&from=six-ps&topic=%s' % (t['route']['slug'], q, BURST, t['id'])


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


class Browser:
    def __init__(self, pw, base, html, size=(1280, 800), blocked=False):
        self.br = pw.chromium.launch()
        touch = size[0] <= 600
        self.ctx = self.br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch)
        self.events = []
        self.errors = []
        self.ctx.expose_function('__mfgRecord', lambda n, p: self.events.append((n, json.loads(p))))
        self.ctx.add_init_script(RECORD_MFG)
        if blocked:
            self.ctx.add_init_script(BLOCK_STORAGE)
        self.base = base
        self.ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
        page_url = re.compile(r'/the-6-ps/(\?[^/]*)?$')
        self.ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
            status=200, content_type='text/html; charset=utf-8', body=html))
        # A game is never opened here: until BURST is merged a launch link is read, not followed (contract STOP IF).
        self.ctx.route(lambda url: '/games/' in url, lambda route: route.abort())
        self.page = self.ctx.new_page()
        self.page.set_default_timeout(5000)   # every step is a local click or load; a planted fault fails fast
        self.page.on('pageerror', lambda e: self.errors.append(str(e)))
        # Off-site requests (the font CDN) are aborted above, and Chromium logs each as a failed resource; any other
        # console.error is the page's own and fails.
        self.page.on('console', lambda m: m.type == 'error' and not m.text.startswith('Failed to load resource')
                     and self.errors.append('console.error: ' + m.text))

    def open(self, query=''):
        self.page.goto(self.base + '/the-6-ps/' + query, wait_until='load', timeout=20000)
        self.page.wait_for_function("""() => !!window.SixPs && (!!SixPs.data() ||
            !document.getElementById('loadError').hidden)""", timeout=10000)

    def close(self):
        self.br.close()


def check_engine(b, data, out):
    """Launch links and 10,000 sessions each way, from the page's own functions."""
    p = b.page
    for t in data['covered']:
        for mode, stage in openers(t):
            got = p.evaluate('([id, mode, stage]) => SixPs.launchUrl(SixPs.data().covered.find(t => t.id === id), mode, stage)',
                             [t['id'], mode, stage])
            want = expected_launch(t, mode, stage)
            if got != want:
                out.append('%s: launch link %r, expected %r' % (t['id'], got, want))
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
    return res


def visible_text(p, sel):
    return p.evaluate('(s) => Array.from(document.querySelectorAll(s)).map(e => e.innerText.trim())', sel)


def sideways(p, where, out):
    w = p.evaluate('() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]')
    if w[0] > w[1]:
        out.append('%s: sideways scroll at 320 px (%d > %d)' % (where, w[0], w[1]))


def play(pw, base, html, data, out, blocked, narrow=False):
    tag = 'storage blocked' if blocked else 'storage working'
    b = Browser(pw, base, html, size=(320, 700) if narrow else (1280, 800), blocked=blocked)
    p = b.page
    covered = {t['id']: t for t in data['covered']}
    try:
        b.open()
        if narrow:
            sideways(p, 'start screen', out)
        coming = visible_text(p, '#comingList li .name')
        if coming != [t['name'] for t in data['coming_soon']]:
            out.append('%s: the coming-soon list is not the data file\'s (%s)' % (tag, coming))
        shown = p.inner_text('#sourceLine').strip()
        if shown != data['source']:
            out.append('%s: the source line shows %r' % (tag, shown))
        p.click('#startBtn')
        p.wait_for_selector('#session:not([hidden])', timeout=5000)
        if narrow:
            sideways(p, 'a session', out)
        plan = p.evaluate("""() => Array.from(document.querySelectorAll('#planList li .name')).map(e => e.textContent)""")
        names = {t['name']: t for t in data['covered']}
        topics = [names.get(n) for n in plan]
        if None in topics or len(topics) != K or len({t['id'] for t in topics if t}) != K:
            out.append('%s: the session is not six distinct covered topics: %s' % (tag, plan))
            return
        scores = [(4, 5), None, (2, 5), (5, 5), (3, 5), (1, 5)]   # None: skipped
        for k, t in enumerate(topics):
            href = p.get_attribute('#goBtn', 'href')
            want = [expected_launch(t, m, st) for m, st in openers(t)]
            if href not in want:
                out.append('%s: topic %d link %r, expected one of %s' % (tag, k + 1, href, want))
            if scores[k] is None:
                p.click('#skipBtn')
                continue
            # The game's six_ps_topic event fires on the click; the navigation itself is stopped (no game is opened).
            p.evaluate("""() => { const stop = e => { e.preventDefault(); document.removeEventListener('click', stop); };
                                   document.addEventListener('click', stop); }""")
            p.click('#goBtn')
            if k == 0:   # forged and stale returns change nothing
                other = topics[1]['id']
                for q in ('?done=%s&r=5&n=5' % other, '?done=%s&r=6&n=5' % t['id'], '?done=%s&r=x&n=5' % t['id']):
                    b.open(q)
                    if p.is_hidden('#session') or p.inner_text('#nextName').strip() != t['name']:
                        out.append('%s: the return %s moved the session on' % (tag, q))
                        return
            r, n = scores[k]
            b.open('?done=%s&r=%d&n=%d' % (t['id'], r, n))
            if '?' in p.url:
                out.append('%s: the return link stays in the address bar (%s)' % (tag, p.url))
        p.wait_for_selector('#results:not([hidden])', timeout=5000)
        if narrow:
            sideways(p, 'the results', out)
        rows = visible_text(p, '#resultList li')
        for k, t in enumerate(topics):
            score = 'skipped' if scores[k] is None else '%d of %d' % scores[k]
            want = '%s: %s' % (t['name'], score)
            marks = "worth about %d marks a series on OCR’s Foundation papers" % about(t['marks'])
            row = rows[k] if k < len(rows) else ''
            if want not in row or marks not in row:
                out.append('%s: results row %d is %r; expected %r and %r' % (tag, k + 1, row, want, marks))
        played = [(t, s) for t, s in zip(topics, scores) if s and s[0] < s[1]]
        low = min(s[0] / s[1] for t, s in played)
        weakest = max((t for t, s in played if s[0] / s[1] == low), key=lambda t: t['marks'])
        nudge = p.inner_text('#nudge').strip()
        if weakest['name'] not in nudge or weakest['route']['game'] not in nudge:
            out.append('%s: the nudge %r does not name the weakest topic, %s' % (tag, nudge, weakest['name']))
        ticks = p.evaluate("() => Array.from(document.querySelectorAll('#tickList input')).map(b => b.value)")
        if ticks != [t['id'] for t in data['coming_soon']] + ['other']:
            out.append('%s: the tick-list is %s, not the coming-soon topics plus "Something else"' % (tag, ticks))
            return
        if p.evaluate("() => !!document.querySelector('#feedbackForm textarea, #feedbackForm input[type=text]')"):
            out.append('%s: the tick-list has a free-text box' % tag)
        pick = [data['coming_soon'][0]['id'], 'other']
        for v in pick:
            p.check('#tickList input[value="%s"]' % v)
        p.click('#sendBtn')
        p.wait_for_selector('#thanks:not([hidden])', timeout=5000)
        names_ = [e[0] for e in b.events]
        fb = [e[1] for e in b.events if e[0] == 'six_ps_feedback']
        want_fb = {'topics': ','.join(pick), 'filter_type': 'six_ps', 'filter_value': 'v1|topics=' + ','.join(pick)}
        if fb != [want_fb]:
            out.append('%s: six_ps_feedback sent %s, expected one event %s' % (tag, fb, want_fb))
        if names_.count('six_ps_started') != 1:
            out.append('%s: six_ps_started sent %d times' % (tag, names_.count('six_ps_started')))
        topic_ev = [e[1].get('topic') for e in b.events if e[0] == 'six_ps_topic']
        want_topics = [t['id'] for t, s in zip(topics, scores) if s]
        if topic_ev != want_topics:
            out.append('%s: six_ps_topic sent for %s, expected %s' % (tag, topic_ev, want_topics))
        fin = [e[1] for e in b.events if e[0] == 'six_ps_finished']
        right = sum(s[0] for s in scores if s)
        total = sum(s[1] for s in scores if s)
        if len(fin) != 1 or fin[0].get('right') != right or fin[0].get('total') != total:
            out.append('%s: six_ps_finished sent %s, expected one with right %d, total %d' % (tag, fin, right, total))
        b.open()   # a finished session is not shown again, and nothing is sent twice
        if p.is_hidden('#intro') or b.events.count(('six_ps_finished', fin[0] if fin else None)) > 1:
            out.append('%s: reopening the page after the results did not open the start screen cleanly' % tag)
        out.extend('%s: page error: %s' % (tag, e) for e in b.errors)
    finally:
        b.close()


def check(html, data, out, engine=True, flows=True, narrow=True):
    from playwright.sync_api import sync_playwright
    static_checks(html, data, out)
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            if engine:
                b = Browser(pw, base, html)
                try:
                    b.open()
                    guarded(out, 'the engine checks', lambda: check_engine(b, data, out))
                    out.extend('page error: ' + e for e in b.errors)
                finally:
                    b.close()
            if flows:
                for blocked in (False, True):
                    guarded(out, 'the session flow', lambda: play(pw, base, html, data, out, blocked))
            if narrow:
                guarded(out, 'the session flow at 320 px', lambda: play(pw, base, html, data, out, False, narrow=True))
    finally:
        proc.terminate()


def guarded(out, what, f):
    try:
        f()
    except Exception as e:  # a crash in a check is a failure, never a pass
        out.append('%s stopped: %s: %s' % (what, type(e).__name__, str(e).splitlines()[0] if str(e) else ''))


# ---------------------------------------------------------------- BURST (part 2)
# The real games, driven exactly as scripts/check-burst.py drives them (its contexts, the answer-lock driver and its
# recorder), never stubbed. KaTeX's CDN is served from the pinned copy (bank_common.serve_real_font_async), so a KaTeX
# game plays the same bytes here as in CI.
LAUNCH_WORKERS = 4


def burst_harness():
    spec = importlib.util.spec_from_file_location('check_burst', os.path.join(HERE, 'check-burst.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.AL.CHECK_SITE = mod.AL.load_check_site()   # as check-burst.py's main() does
    return mod


def burst_init(CB):
    """check-burst's page script, with each event's mode recorded too (a stage is honoured only when the game's own
    game_started says it started there; a pressed button alone proves nothing)."""
    src = CB.init_script()
    assert 'lv: p && p.level,' in src, 'verify-the-6-ps: check-burst.py\'s recorder changed; update burst_init'
    return src.replace('lv: p && p.level,', 'lv: p && p.level, m: p && p.mode,') % {
        'scale': CB.AL.TIME_SCALE, 'seed': CB.AL.SEED}


async def burst_ctx(CB, browser, base):
    ctx = await CB.new_ctx(browser, base, [], init=False, viewport={'width': 1280, 'height': 900})
    await ctx.add_init_script(burst_init(CB))
    await ctx.route(lambda u: bc.is_font_cdn(u), bc.serve_real_font_async)
    return ctx


async def play_five(CB, page, slug, mode=None, stage=None):
    """Five answers through the answer-lock driver: (findings, right answers the page reported, the bar or None).
    A game's lock hint may start play by pressing a stage of its own (squared-squirrel's presses stage-2, the stage
    check-answer-lock.py plays); in a burst that names a mode, the hint presses the route's mode instead, as the
    student would find it already selected."""
    hint = dict(CB.AL.read_hint(open(os.path.join(ROOT, 'games', slug, 'index.html'), encoding='utf-8').read())[0])
    if mode and isinstance(hint.get('start'), str):
        hint['start'] = re.sub(r'data-mode="[^"]*"', 'data-mode="%s"' % mode, hint['start'])
    if stage and isinstance(hint.get('start'), str):
        hint['start'] = re.sub(r'data-stage="[^"]*"', 'data-stage="%s"' % stage, hint['start'])
    d = CB.AL.Driver(page, slug, hint)
    if not await d.start():
        return ['UNPLAYABLE (no question reached)'], None, None
    s = None
    for k in range(BURST):
        s = None
        for attempt in range(14):
            s = await d.answer(k * 14 + attempt, ms=1500)
            if s is not None:
                break
            c = await d.ev('() => __lockContinue()')
            if c and c['ready']:
                await d.tap(c['rect'], False)
        if s is None:
            return ['answer %d was not recorded (driver)' % (k + 1)], None, None
        bar = await page.evaluate(CB.BAR)
        if k < BURST - 1:
            if bar:
                return ['the return bar is up after answer %d of %d' % (k + 1, BURST)], None, None
            await d.to_next(s['lastFresh'])
    return [], s['correct'], await page.evaluate(CB.BAR)


# How each game's own game_started names the mode or stage it started at, read from the games' code: a [data-mode]
# card's onclick may call the game's own key (Shape Shifter's random-mix card calls startGame('mix')); Free Daily
# Pizza reports a stage as FDP.modeFor's 'stage-s<stage>-q<length>'; Simultaneous Solver's mode() is its stage key.
STAGE_REPORTS = {'free-daily-pizza': lambda st, m: bool(m) and m.startswith('stage-s%s-' % st),
                 'simultaneous-solver': lambda st, m: m == st}


def game_mode_name(slug, mode):
    with open(os.path.join(ROOT, 'games', slug, 'index.html'), encoding='utf-8') as f:
        src = f.read()
    m = re.search(r'<[^>]*\bdata-mode="%s"[^>]*>' % re.escape(mode), src)
    oc = m and re.search(r"onclick=\"startGame\('([^']+)'\)\"", m.group(0))
    return oc.group(1) if oc else mode


def opened_at(slug, mode, stage, started):
    if mode:
        return game_mode_name(slug, mode) in started
    report = STAGE_REPORTS.get(slug, lambda st, m: m == st)
    return any(report(stage, m) for m in started)


async def launch_route(CB, browser, base, t, mode, stage=''):
    """Open one route's game at the page's launch link, play the burst and read the return link."""
    slug, level = t['route']['slug'], t['route']['level']
    where = '%s (%s%s%s)' % (t['id'], slug, ', mode ' + mode if mode else '', ', stage ' + stage if stage else '')
    f, reported = [], None
    ctx = await burst_ctx(CB, browser, base)
    try:
        page = await ctx.new_page()
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)[:120]))
        await page.goto(base + expected_launch(t, mode, stage), wait_until='load', timeout=20000)
        await page.wait_for_timeout(1200 if mode or stage else 300)
        if not await page.evaluate('() => !!(window.MaffsBurst && MaffsBurst.active())'):
            return ['%s: the game is not in a burst (does it load burst.js?)' % where], None
        got, right, bar = await play_five(CB, page, slug, mode, stage)
        f += ['%s: %s' % (where, g) for g in got]
        started = await page.evaluate("() => (window.__lockEvents || []).filter(e => e.e === 'game_started').map(e => e.m)")
        if (mode or stage) and not opened_at(slug, mode, stage, started):
            f.append('%s: STAGE the game did not open at %s %r (its own game_started reported %r)'
                     % (where, 'mode' if mode else 'stage', mode or stage, started))
        reported = started[0] if started else None
        dec = await page.evaluate('(s) => (window.MaffsLevel && MaffsLevel.declared) ? MaffsLevel.declared(s) : null', slug)
        if not dec or dec.get('fromUrl') is not True:
            f.append('%s: the game did not take ?level=%s from the link (%r)' % (where, level, dec))
        if right is not None:
            want = '/the-6-ps/?done=%s&r=%d&n=%d' % (t['id'], right, BURST)
            if not bar:
                f.append('%s: no return bar after answer %d' % (where, BURST))
            elif bar['href'] != want:
                f.append('%s: the return bar links to %r, want %r' % (where, bar['href'], want))
        f += ['%s: page error: %s' % (where, e) for e in errs]
    finally:
        await ctx.close()
    return f, reported


async def full_session(CB, browser, base, data, out):
    """One session through the page and the real games: Start, each topic's link followed into its game, five
    answers, the return bar followed back; then the results."""
    covered = {t['name']: t for t in data['covered']}
    ctx = await burst_ctx(CB, browser, base)
    try:
        page = await ctx.new_page()
        await page.goto(base + '/the-6-ps/?cb=verify', wait_until='load', timeout=20000)
        await page.wait_for_function('() => !!window.SixPs && !!SixPs.data()', timeout=10000)
        await page.click('#startBtn')
        played = []
        for k in range(K):
            await page.wait_for_selector('#session:not([hidden])', timeout=10000)
            name = (await page.inner_text('#nextName')).strip()
            t = covered.get(name)
            if not t:
                out.append('full session: topic %d is %r, not a covered topic' % (k + 1, name))
                return
            href = await page.get_attribute('#goBtn', 'href')
            await page.click('#goBtn')
            await page.wait_for_url('**/games/%s/**' % t['route']['slug'], timeout=20000)
            await page.wait_for_load_state('load')
            await page.wait_for_timeout(1200)
            m = re.search(r'[?&]mode=([^&]+)', href or '')
            st = re.search(r'[?&]stage=([^&]+)', href or '')
            got, right, bar = await play_five(CB, page, t['route']['slug'], m.group(1) if m else None, st.group(1) if st else None)
            if got or not bar:
                out.append('full session: %s (%s): %s' % (t['id'], href, got or 'no return bar'))
                return
            await page.click('#mfg-burst-bar a')
            await page.wait_for_url('**/the-6-ps/**', timeout=20000)
            await page.wait_for_function('() => !!window.SixPs && !!SixPs.data()', timeout=10000)
            played.append((t, right))
        await page.wait_for_selector('#results:not([hidden])', timeout=10000)
        rows = await page.evaluate("() => Array.from(document.querySelectorAll('#resultList li')).map(e => e.innerText)")
        for (t, right), row in zip(played, rows):
            if '%s: %d of %d' % (t['name'], right, BURST) not in row:
                out.append('full session: the results row %r does not show %s: %d of %d' % (row, t['name'], right, BURST))
        if len(rows) != K:
            out.append('full session: %d results rows, not %d' % (len(rows), K))
        print('the-6-ps: a full session played through the real games and back: %s'
              % ', '.join('%s %d/%d' % (t['id'], r, BURST) for t, r in played))
    finally:
        await ctx.close()


def burst_part(out, data, shard=None, shards=1, launches=True, session=True):
    """Every COVERED route (each mode it offers) opened and played as a burst (part 2, in shards for CI); and one
    full session through the page and the real games (part 4)."""
    if not os.path.isfile(BURST_JS):
        out.append('schools/assets/burst.js is missing: BURST is not on this branch')
        return {}
    import asyncio
    from playwright.async_api import async_playwright
    CB = burst_harness()
    jobs = [(t, m, st) for t in data['covered'] for m, st in openers(t)] if launches else []
    if shard is not None:
        jobs = jobs[shard - 1::shards]
    stages = {}

    async def main():
        proc, base = bc.start_stub_server()
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                sem = asyncio.Semaphore(LAUNCH_WORKERS)

                async def one(t, m, st):
                    async with sem:
                        try:
                            f, rep = await asyncio.wait_for(launch_route(CB, browser, base, t, m, st), 180)
                        except Exception as e:  # a crash is a failure, never a pass
                            f, rep = ['%s: the launch check stopped: %s: %s' % (t['id'], type(e).__name__, str(e).splitlines()[0] if str(e) else '')], None
                        out.extend(f)
                        if m:
                            stages['%s/%s' % (t['id'], m or st)] = rep
                await asyncio.gather(*(one(t, m, st) for t, m, st in jobs))
                if session:
                    try:
                        await asyncio.wait_for(full_session(CB, browser, base, data, out), 600)
                    except Exception as e:
                        out.append('full session stopped: %s: %s' % (type(e).__name__, str(e).splitlines()[0] if str(e) else ''))
                await browser.close()
        finally:
            proc.terminate()

    asyncio.run(main())
    if launches:
        print('the-6-ps: %d launches (%s)' % (len(jobs), 'shard %d of %d' % (shard, shards) if shard else 'all routes'))
    return stages


# ---------------------------------------------------------------- plants
# (what, [(old, new)], what it needs: static | engine | flow, a pattern its finding must match). Every old text occurs
# exactly once in the page.
PLANTS = [
    ('a hand-typed mark figure in the page',
     [('<p class="muted" id="sourceLine"></p>', '<p class="muted" id="sourceLine"></p>\n  <p>Ratio is worth about 13 marks a series.</p>')],
     'static', r'hand-typed mark figure'),
    ('a coming-soon topic drawn into a session (given a band and a route, so it reaches one)',
     [('var topics = data.covered, picked', 'var topics = data.covered.concat(data.coming_soon.map(function (t) { '
       'return Object.assign({ band: [1, 1], route: { slug: "x", game: "x", level: "x", modes: [] } }, t); })), picked')],
     'engine', r'coming-soon topic'),
    ('a session with a repeated topic',
     [('if (point < cum) { out.push(order[i]); point += W; }',
       'if (point < cum) { out.push(order[i]); out.push(order[i]); point += W; }')],
     'engine', r'repeats a topic'),
    ('a route missing the burst parameters',
     [("q += '&burst=' + BURST + '&from=six-ps&topic=' + encodeURIComponent(t.id);",
       "q += '&topic=' + encodeURIComponent(t.id);")],
     'engine', r'launch link'),
    ('a weighting claim naming a board',
     [("so it's useful whichever board you sit.", "so it's useful whichever board you sit, and matches AQA's weightings too.")],
     'static', r'"AQA" appears'),
    ('a past-paper site left out',
     [('    <li><a href="https://www.mathsgenie.co.uk/" target="_blank" rel="noopener">Maths Genie</a></li>\n', '')],
     'static', r'does not link https://www\.mathsgenie'),
    ('draws one at a time by weight without replacement, which saturates heavy topics (not in proportion to marks)',
     [('  function drawRandom(topics, k, rnd) {\n',
       '  function drawRandom(topics, k, rnd) {\n'
       '    var pool = topics.slice(), res = [];\n'
       '    while (res.length < k) {\n'
       '      var S = 0; pool.forEach(function (t) { S += tenths(t); });\n'
       '      var x = Math.floor(rnd() * S), j = 0;\n'
       '      while (x >= tenths(pool[j])) { x -= tenths(pool[j]); j++; }\n'
       '      res.push(pool.splice(j, 1)[0]);\n'
       '    }\n'
       '    return res;\n')],
     'engine', r'came up \d+ times'),
    ('the tick-list missing a coming-soon topic',
     [("data.coming_soon.map(function (t) { return [t.id, t.name]; })",
       "data.coming_soon.slice(1).map(function (t) { return [t.id, t.name]; })")],
     'flow', r'tick-list is'),
    ('no session when localStorage is blocked (the window.name fallback removed)',
     [("try { window.name = NAME_PREFIX + json; } catch (e) { /* in memory only */ }", "")],
     'flow', r'storage blocked'),
    ('a return link recorded for any topic',
     [("if (session.plan[session.i].id !== done) return false;", "")],
     'flow', r'moved the session on'),
]


def selftest(html, data):
    ok = True
    for what, edits, kind, want in PLANTS:
        planted = html
        for old, new in edits:
            if planted.count(old) != 1:
                print('FAIL  plant %r: its text occurs %d times in the page' % (what, planted.count(old)))
                ok = False
                break
            planted = planted.replace(old, new)
        else:
            got = []
            if kind == 'static':
                static_checks(planted, data, got)
            else:
                check(planted, data, got, engine=kind == 'engine', flows=kind == 'flow', narrow=False)
            if any(re.search(want, g) for g in got):
                print('ok    plant caught: %s' % what)
            else:
                print('FAIL  plant NOT caught: %s (findings: %s)' % (what, got[:3]))
                ok = False
    # The data file edited by hand: one figure changed in a copy is not the generator's output.
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
    ap.add_argument('--part', choices=['1', '2', '3', '4'],
                    help='1 the checks, 2 every route launched in its game, 3 the plants, 4 a full session through the real games')
    ap.add_argument('--shard', help='part 2 only: k/n, every nth route from the kth')
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    with open(PAGE, encoding='utf-8') as f:
        html = f.read()
    data = load_data()
    out = []
    ok = True
    if args.part in (None, '1'):
        check_data(data, out)
        check_routes(data, out)
        check(html, data, out)
        W = sum(t['marks'] for t in data['covered'])
        print('the-6-ps: %d covered topics (%.1f marks a series), %d coming soon; %d sessions drawn each way'
              % (len(data['covered']), W, len(data['coming_soon']), DRAWS))
    if args.part in (None, '2', '4'):
        k, n = (int(x) for x in args.shard.split('/')) if args.shard else (None, 1)
        burst_part(out, data, shard=k, shards=n, launches=args.part != '4', session=args.part != '2')
    if args.part in (None, '3'):
        ok = selftest(html, data) and ok
    for f in out[:60]:
        print('FAIL  ' + f)
    if len(out) > 60:
        print('FAIL  ... and %d more' % (len(out) - 60))
    if not ok and args.part != '2':
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if out or not ok else 'PASS')
    return 1 if out or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
