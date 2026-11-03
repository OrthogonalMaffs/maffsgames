#!/usr/bin/env python3
# ci-line: Question id (question_answered names its question: analytics.js hashes question_text to question_id and never sends the text, GA4 and the Sheet alike; Sequence Solver's ids decode with no collision; shrink-only warn list; planted faults) | --selftest && --check
# ci-deps: games/ the-6-ps/ escape-rooms/assets/engine.js schools/assets/ scripts/question-id-warn.json scripts/decode-question-ids.py
"""QUESTION-ID (contract, Jon, 3 Nov 2026; canon §1.3): question_answered carried question_index, a position in a shuffled
round, so no game's hard questions could be found from the data. A game now says which question it asked, with
question_id (its own stable id) or question_text (the prompt as shown, from its bank), and schools/assets/analytics.js
sends question_text only as its hash, question_id = "h" + 8 hex digits (FNV-1a). Nothing a student types is ever passed.

--check, in two parts:

  1. Every call site (no browser). For each page under games/ and the-6-ps/, and escape-rooms/assets/engine.js, every
     call of the form <name>('question_answered', { ... }) is read. A site is moved when each of its calls names
     question_id or question_text. It fails if:
       - it is not moved and not on the warn list (warn first, canon §7.8.4: scripts/question-id-warn.json, every site
         not yet moved, seeded 3 Nov 2026; a listed site WARNS; the list is shrink-only against the pull request's own
         base, and an entry whose site has moved is stale and fails);
       - a question_text value reads .value (what a student typed; contract STOP IF);
       - a game in decode-question-ids.py's RECIPES passes a question_text expression other than its recipe's, or its
         ids collide (two different questions, one id).
  2. In Chromium, with the real analytics.js served as https://maffsgames.co.uk (a Playwright route: nothing leaves
     the machine; the Sheet is read from the posts to the endpoint, GA4 from window.dataLayer):
       - question_id is sent as given, cut to 40 characters; question_text becomes question_id = the decoder's
         question_hash() of it, and the text reaches neither the Sheet nor GA4, on any event; with neither, the event
         is unchanged (the same keys as before);
       - analytics.js's hash equals the decoder's on every Sequence Solver question and on awkward strings (accents in
         NFC and NFD, £, √, a no-break space, an emoji, runs of whitespace);
       - Sequence Solver, one round played: every question_answered carries a question_id that decodes to the
         question on screen, and no question_text.

    python -X utf8 scripts/check-question-id.py --check
    python -X utf8 scripts/check-question-id.py --selftest   planted faults: an unmoved site, a warn-list addition, a
                                                             stale entry, a typed value, recipe drift, a collision; an
                                                             analytics.js that sends the text, and one that skips NFC
"""
import argparse
import importlib.util
import json
import mimetypes
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import plant_common as pc  # noqa: E402

WARN = 'scripts/question-id-warn.json'
ORIGIN = 'https://maffsgames.co.uk'
ANALYTICS = 'schools/assets/analytics.js'
ENDPOINT_HOST = 'script.google.com'

_spec = importlib.util.spec_from_file_location('decode_question_ids', ROOT / 'scripts' / 'decode-question-ids.py')
dq = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dq)

CALL = re.compile(r"""(?<![\w$])([A-Za-z_$][\w$.]*)\(\s*(['"])question_answered\2\s*,\s*\{""")
KEY = re.compile(r"""(?:^|[{,\s])(['"]?)question_(id|text)\1\s*:""")


# ---------------------------------------------------------------- part 1: the call sites
def sites(root=ROOT):
    out = {}
    for p in sorted((root / 'games').glob('*/index.html')) + [root / 'the-6-ps' / 'index.html',
                                                               root / 'escape-rooms' / 'assets' / 'engine.js']:
        if p.is_file():
            out[p.relative_to(root).as_posix()] = p.read_text(encoding='utf-8', errors='replace')
    return out


def _object_at(src, i):
    """The text of the object literal whose '{' is at src[i], strings and nesting respected."""
    depth, j, q = 0, i, None
    while j < len(src):
        c = src[j]
        if q:
            if c == '\\':
                j += 2
                continue
            if c == q:
                q = None
        elif c in '\'"`':
            q = c
        elif c in '{[(':
            depth += 1
        elif c in '}])':
            depth -= 1
            if depth == 0:
                return src[i:j + 1]
        j += 1
    return src[i:]


def _value_of(obj, key):
    """The source text of key's value in an object literal's text (to the next top-level comma or the end)."""
    m = re.search(r"""(?:^|[{,\s])(['"]?)%s\1\s*:""" % key, obj)
    if not m:
        return None
    depth, j, q, start = 0, m.end(), None, m.end()
    while j < len(obj):
        c = obj[j]
        if q:
            if c == '\\':
                j += 2
                continue
            if c == q:
                q = None
        elif c in '\'"`':
            q = c
        elif c in '{[(':
            depth += 1
        elif c in '}])':
            if depth == 0:
                break
            depth -= 1
        elif c == ',' and depth == 0:
            break
        j += 1
    return obj[start:j].strip()


def calls(src):
    """[(line, object text)] for every <name>('question_answered', {...}) not on a // comment line."""
    out = []
    for m in CALL.finditer(src):
        line_start = src.rfind('\n', 0, m.start()) + 1
        if src[line_start:m.start()].lstrip().startswith('//'):
            continue
        out.append((src.count('\n', 0, m.start()) + 1, _object_at(src, m.end() - 1)))
    return out


def analyse(pages, listed_warn, base_warn, recipes=None, decode=None):
    """pages: {path: source}. Returns (errors, warnings, moved sites)."""
    recipes = dq.RECIPES if recipes is None else recipes
    decode = dq.decode if decode is None else decode
    errors, warnings, moved = [], [], []
    warn = set(listed_warn)
    if len(warn) != len(listed_warn):
        errors.append('duplicate warn-list entries')
    for path in sorted(warn - set(base_warn)):
        errors.append('%s: adding to the warn list fails; it is shrink-only' % path)
    for path in sorted(warn - set(pages)):
        errors.append('%s: no such site; remove its stale warn-list entry' % path)
    by_page = {r['page']: slug for slug, r in recipes.items()}
    for path, src in sorted(pages.items()):
        cs = calls(src)
        if not cs:
            if path in warn:
                errors.append('%s: sends no question_answered; remove its stale warn-list entry' % path)
            continue
        named = [(ln, obj) for ln, obj in cs if KEY.search(obj)]
        for ln, obj in named:
            text = _value_of(obj, 'question_text')
            if text is not None and re.search(r'\.value\b', text):
                errors.append('%s:%d: question_text reads .value, which is what a student typed: never send it '
                              '(QUESTION-ID STOP IF): %s' % (path, ln, text))
        if len(named) == len(cs):
            moved.append(path)
            if path in warn:
                errors.append('%s: names its question now; remove its stale warn-list entry' % path)
        else:
            lines = ', '.join(str(ln) for ln, obj in cs if not KEY.search(obj))
            msg = '%s: question_answered without question_id or question_text (line %s)' % (path, lines)
            (warnings if path in warn else errors).append(msg + (' [warn-listed]' if path in warn else ''))
        if path in by_page:
            slug = by_page[path]
            want = recipes[slug]['expr']
            for ln, obj in cs:
                got = _value_of(obj, 'question_text')
                if got != want:
                    errors.append('%s:%d: question_text is %r, but decode-question-ids.py rebuilds %r; change both '
                                  'together or the ids will not decode' % (path, ln, got, want))
            try:
                _, collisions = decode(slug, html=src)
            except (OSError, ValueError) as exc:
                errors.append('%s: cannot decode its ids: %s' % (path, exc))
                continue
            errors.extend('COLLISION %s (contract STOP IF)' % c for c in collisions)
    return errors, warnings, moved


def read_warn(text):
    data = json.loads(text)
    if not isinstance(data, dict) or not isinstance(data.get('pages'), dict) or any(not isinstance(k, str) for k in data['pages']):
        raise ValueError('%s must be {"pages": {"<path>": "<reason>", ...}}' % WARN)
    return list(data['pages'])


def base_warn(listed, root=ROOT, env=None):
    """The warn list on the pull request's own base (fail closed); outside a pull request, on the merge base with main.
    Before the list existed on the base: the list as it stands (the seed, in the pull request that adds it)."""
    env = os.environ if env is None else env
    if env.get('GITHUB_EVENT_NAME') == 'pull_request':
        event = json.loads(Path(env['GITHUB_EVENT_PATH']).read_text(encoding='utf-8'))
        base = event['pull_request']['base']['sha']
    else:
        base = subprocess.run(['git', 'merge-base', 'origin/main', 'HEAD'], cwd=root,
                              capture_output=True, text=True, check=True).stdout.strip()
    if subprocess.run(['git', 'cat-file', '-e', '%s^{commit}' % base], cwd=root, capture_output=True).returncode:
        subprocess.run(['git', 'fetch', '--no-tags', '--depth=1', 'origin', base], cwd=root,
                       capture_output=True, text=True, check=True)
    if not subprocess.run(['git', 'ls-tree', '--name-only', base, '--', WARN], cwd=root,
                          capture_output=True, text=True, check=True).stdout.strip():
        return list(listed)
    return read_warn(subprocess.run(['git', 'show', '%s:%s' % (base, WARN)], cwd=root, capture_output=True, text=True,
                                    encoding='utf-8', check=True).stdout)


# ---------------------------------------------------------------- part 2: in Chromium
ODD = ['Find the next term', '  Find\tthe\n next\u00a0term ZQXTEXT  ', 'Caf\u00e9', 'Cafe\u0301', '\u00a374.50',
       '\u221a2 \u00d7 \u03c0', 'emoji \U0001F355 pizza', '\\(T_n = 3 \\times 2^{n-1}\\)', '', 'a | b | c']
LONG_ID = 'L' * 50
HARNESS = '<!doctype html><meta charset="utf-8"><script src="/%s"></script><p>question-id harness</p>' % ANALYTICS
GA4 = "() => (window.dataLayer || []).filter(a => a && a[0] === 'event').map(a => [a[1], a[2] || {}])"
CASES = """() => {
  mfg('game_started', {game_slug: 'qid-test', level: 'gcse', question_text: 'ZQXSTART never sent'});
  mfg('question_answered', {game_slug: 'qid-test', level: 'gcse', question_index: 1, correct: true, question_id: 'q-17'});
  mfg('question_answered', {game_slug: 'qid-test', level: 'gcse', question_index: 2, correct: false, question_id: '%s'});
  mfg('question_answered', {game_slug: 'qid-test', level: 'gcse', question_index: 3, correct: true, question_text: %s});
  mfg('question_answered', {game_slug: 'qid-test', level: 'gcse', question_index: 4, correct: false});
}""" % (LONG_ID, json.dumps(ODD[1]))
NEITHER_SHEET = {'event', 'client_ts', 'seq', 'game_slug', 'level', 'question_index', 'correct'}
NEITHER_GA4 = {'game_slug', 'level', 'question_index', 'correct'}


def browse(served, game_rounds=True):
    """Run part 2 with {repo path: replacement text} served in place of the files. -> {name: result}."""
    import bank_common as bc
    from playwright.sync_api import sync_playwright
    out = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch()

        def context():
            posts = []
            ctx = browser.new_context(viewport={'width': 375, 'height': 667})

            def route(r):
                url = r.request.url
                if url.startswith(bc.KATEX_CDN):
                    resp = bc.real_font_response(url)
                    return r.fulfill(**resp) if resp else r.abort()
                if url.startswith(ORIGIN):
                    path = unquote(urlsplit(url).path).lstrip('/')
                    if path.endswith('/') or path == '':
                        path += 'index.html'
                    if path == 'qid-test/index.html':
                        return r.fulfill(status=200, body=HARNESS, content_type='text/html; charset=utf-8')
                    if path in served:
                        return r.fulfill(status=200, body=served[path].encode('utf-8'),
                                         content_type=mimetypes.guess_type(path)[0] or 'text/plain')
                    f = ROOT / path
                    if f.is_file():
                        return r.fulfill(status=200, body=f.read_bytes(),
                                         content_type=mimetypes.guess_type(str(f))[0] or 'application/octet-stream')
                    return r.fulfill(status=404, body=b'')
                if urlsplit(url).netloc == ENDPOINT_HOST:
                    if r.request.method == 'POST':
                        try:
                            posts.append(json.loads(r.request.post_data or '{}'))
                        except ValueError:
                            pass
                    return r.fulfill(status=200, body=b'{"ok":true}', content_type='application/json')
                return r.abort()

            ctx.route('**/*', route)
            return ctx, posts

        # the analytics cases and the hash parity
        ctx, posts = context()
        page = ctx.new_page()
        page.goto(ORIGIN + '/qid-test/?cb=qid', wait_until='load')
        page.evaluate(CASES)
        page.wait_for_timeout(300)
        texts = [dq.RECIPES['sequence-solver']['text'](q) for _, q in dq.read_bank('sequence-solver')] + ODD
        out['cases'] = {'sheet': list(posts), 'ga4': page.evaluate(GA4),
                        'hashes': page.evaluate('ts => ts.map(t => window.mfgQuestionHash ? window.mfgQuestionHash(t) : null)', texts),
                        'texts': texts}
        ctx.close()

        # Sequence Solver: one round, every answer's id against the question on screen
        if game_rounds:
            ctx, posts = context()
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
            page = ctx.new_page()
            errs = []
            page.on('pageerror', lambda e: errs.append(str(e)))
            page.goto(ORIGIN + '/games/sequence-solver/?level=gcse&cb=qid', wait_until='load')
            page.wait_for_function('typeof katex !== "undefined" && typeof startGame === "function"', timeout=15000)
            page.evaluate('startGame()')
            shown = []
            for _ in range(20):
                page.wait_for_selector('#options .opt-btn', timeout=10000)
                shown.append(page.evaluate("[questions[qIdx].seq, questions[qIdx].q, questions[qIdx].ask].filter(Boolean).join(' | ')"))
                n = page.evaluate('qIdx')
                page.click('#options .opt-btn >> nth=0')
                page.wait_for_timeout(150)
                nxt = page.query_selector('#nextMount button')
                if nxt:
                    nxt.click()
                page.wait_for_function('n => qIdx > n', arg=n, timeout=5000)
            page.wait_for_timeout(300)
            out['game'] = {'sheet': list(posts), 'ga4': page.evaluate(GA4), 'shown': shown, 'errors': errs}
            ctx.close()
        browser.close()
    return out


def judge(res):
    """Failures from part 2's results."""
    fails = []
    c = res['cases']
    for dest, evs in (('Sheet', [(p.get('event'), p) for p in c['sheet']]), ('GA4', c['ga4'])):
        blob = json.dumps(evs, ensure_ascii=False)
        if 'question_text' in blob or 'ZQXTEXT' in blob or 'ZQXSTART' in blob:
            fails.append('%s: the question text reached it (it must only ever get the hash)' % dest)
        qa = [p for name, p in evs if name == 'question_answered']
        if len(qa) != 4:
            fails.append('%s: %d question_answered events, expected 4' % (dest, len(qa)))
            continue
        if qa[0].get('question_id') != 'q-17':
            fails.append('%s: a given question_id was not sent as given (got %r)' % (dest, qa[0].get('question_id')))
        if qa[1].get('question_id') != LONG_ID[:40]:
            fails.append('%s: a 50-character question_id was not cut to 40 (got %r)' % (dest, qa[1].get('question_id')))
        want = dq.question_hash(ODD[1])
        if qa[2].get('question_id') != want:
            fails.append('%s: question_text did not become question_id %s (got %r)' % (dest, want, qa[2].get('question_id')))
        keys = set(qa[3])
        expect = NEITHER_SHEET if dest == 'Sheet' else NEITHER_GA4
        if keys != expect:
            fails.append('%s: with neither field the event changed: keys %s, expected %s' % (dest, sorted(keys), sorted(expect)))
    bad = [(t, h, dq.question_hash(t)) for t, h in zip(c['texts'], c['hashes']) if h != dq.question_hash(t)]
    if bad:
        fails.append('analytics.js and decode-question-ids.py hash %d of %d texts differently, e.g. %r: %r against %r'
                     % (len(bad), len(c['texts']), bad[0][0], bad[0][1], bad[0][2]))
    g = res.get('game')
    if g is not None:
        ids, _ = dq.decode('sequence-solver')
        for dest, evs in (('Sheet', [(p.get('event'), p) for p in g['sheet']]), ('GA4', g['ga4'])):
            qa = [p for name, p in evs if name == 'question_answered']
            if len(qa) != len(g['shown']):
                fails.append('Sequence Solver, %s: %d question_answered for %d questions' % (dest, len(qa), len(g['shown'])))
                continue
            if 'question_text' in json.dumps(evs):
                fails.append('Sequence Solver, %s: question_text was sent' % dest)
            for k, (p, text) in enumerate(zip(qa, g['shown']), 1):
                got = [t for _, t in ids.get(p.get('question_id'), [])]
                if text not in got:
                    fails.append('Sequence Solver, %s, question %d: question_id %r decodes to %r, but the screen showed %r'
                                 % (dest, k, p.get('question_id'), got, text))
                    break
        if g['errors']:
            fails.append('Sequence Solver: page errors: %s' % '; '.join(g['errors'][:2]))
    return fails


# ---------------------------------------------------------------- self-test
MOVED = "function handle(q, ok){ mfg('question_answered', {game_slug:'t', level:L, correct:ok, question_index:i, question_text:[q.seq,q.ask].join(' | ')}); }\n"
BARE = "function handle(q, ok){ mfg('question_answered', {game_slug:'t', level:L, correct:ok, question_index:i}); }\n"
TYPED = "function handle(q, ok){ ev('question_answered', { game_slug: 't', question_text: document.getElementById('ans').value }); }\n"
FAKE_RECIPE = {'t': {'page': 'games/t/index.html', 'bank': 'QUESTIONS', 'expr': "[q.seq,q.ask].join(' | ')",
                     'text': lambda q: ' | '.join([q['seq'], q['ask']])}}


def _fake_decode(texts):
    def decode(slug, html=None):
        ids = {}
        for k, t in enumerate(texts):
            ids.setdefault(dq.question_hash(t), []).append(('[%d]' % k, t))
        cols = ['%s: %s share %s' % (slug, ', '.join(w for w, _ in u), h) for h, u in ids.items() if len({t for _, t in u}) > 1]
        return ids, cols
    return decode


def selftest(browser=True):
    G, W = 'games/t/index.html', 'games/listed/index.html'
    drift = pc.apply_plant(MOVED, "[q.seq,q.ask].join(' | ')", "[q.seq,q.q,q.ask].join(' | ')", name='recipe drift')
    ok_decode, clash = _fake_decode(['Q one', 'Q two']), _fake_decode(['Q fycwgeex', 'Q kjqwhlqj'])
    cases = [  # (name, pages, warn, base warn, decode, expected error text or None, want a warning)
        ('a moved site passes', {G: MOVED}, [], [], ok_decode, None, False),
        ('PLANT: a site that does not name its question fails', {W: BARE}, [], [], ok_decode, 'without question_id', False),
        ('a warn-listed site warns', {W: BARE}, [W], [W], ok_decode, None, True),
        ('PLANT: adding to the warn list fails', {W: BARE}, [W], [], ok_decode, 'shrink-only', True),
        ('PLANT: a stale warn entry (the site moved) fails', {G: MOVED}, [G], [G], ok_decode, 'stale', False),
        ('a warn entry for a site that does not exist fails', {G: MOVED}, [W], [W], ok_decode, 'no such site', False),
        ('PLANT: question_text from a typed .value fails', {W: TYPED}, [], [], ok_decode, 'student typed', False),
        ("PLANT: the page's question_text drifts from its recipe", {G: drift}, [], [], ok_decode, 'will not decode', False),
        ('PLANT: two questions sharing an id (a real FNV-1a collision) fail', {G: MOVED}, [], [], clash, 'COLLISION', False),
        ('a // comment that names the event is not a call', {G: MOVED + "// mfg('question_answered', {})\n"}, [], [],
         ok_decode, None, False),
    ]
    failed = 0
    for name, pg, warn, base, decode, expected, want_warning in cases:
        recipes = FAKE_RECIPE if G in pg else {}
        errors, warnings, _ = analyse(pg, warn, base, recipes=recipes, decode=decode)
        ok = pc.is_caught([e for e in errors if expected in e]) if expected else not errors
        ok = ok and bool(warnings) == want_warning
        print('%s: %s%s' % ('PASS' if ok else 'FAIL', name, '' if ok else ' (errors %s, warnings %s)' % (errors, warnings)))
        failed += not ok
    total = len(cases)
    if browser:
        src = (ROOT / ANALYTICS).read_text(encoding='utf-8')
        sends_text = pc.apply_plant(src, '    if (params.question_id != null || params.question_text != null) params = withQuestionId(params);\n',
                                    '', name='analytics.js sends the text')
        no_nfc = pc.apply_plant(src, "    if (s.normalize) s = s.normalize('NFC');\n", '', name='analytics.js skips NFC')
        for name, served, expected in (('PLANT: an analytics.js that sends question_text is caught', sends_text, 'reached it'),
                                       ('PLANT: an analytics.js that skips NFC is caught', no_nfc, 'hash')):
            fails = judge(browse({ANALYTICS: served}, game_rounds=False))
            ok = pc.is_caught([f for f in fails if expected in f])
            print('%s: %s%s' % ('PASS' if ok else 'FAIL', name, '' if ok else ' (%s)' % fails))
            failed += not ok
            total += 1
    print('Question id selftest: %d/%d passed' % (total - failed, total))
    return bool(failed)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--selftest', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    if args.selftest:
        return selftest()
    try:
        warn = read_warn((ROOT / WARN).read_text(encoding='utf-8'))
        pg = sites()
        errors, warnings, moved = analyse(pg, warn, base_warn(warn))
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print('FAIL: cannot check the question ids: %s' % exc)
        return 1
    res = browse({})
    errors += judge(res)
    for w in warnings:
        print('WARN: %s' % w)
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            print('::warning title=Question id::%s' % w)
    for e in errors:
        print('FAIL: %s' % e)
    g = res.get('game', {})
    print('Question id: %d sites read, %d name their question (%s), %d warn-listed; analytics cases and %d hashes checked; '
          'Sequence Solver: %d answers, each id decoded to the question shown; %d failures'
          % (len(pg), len(moved), ', '.join(moved) or 'none', len(warnings), len(res['cases']['texts']),
             len(g.get('shown', [])), len(errors)))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
