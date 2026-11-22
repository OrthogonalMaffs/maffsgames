#!/usr/bin/env python3
# ci-line: Aa flag (game_started carries aa from the body class the Aa toggle switches: every toggle found by analytics.js's one selector, every switch one of its three known classes; in Chromium aa false, then true after the toggle, never from storage, none on a page with no toggle; planted faults) | --selftest && --check
# ci-deps: schools/assets/analytics.js games/ escape-rooms/
"""AA-USAGE (Jon, 22 Nov 2026; the privacy page, "The data we collect"): game_started carries aa, whether the
dyslexia-friendly (Aa) font is on, so Aa-only layout fixes can be ranked by real use. schools/assets/analytics.js reads
it in mfg(), the one point every start passes: aa is true when <body> has one of AA_CLASSES, false when the page has an
element matching AA_TOGGLE and none of them, and left out on a page with no toggle (so it never counts as "off"). It is
read from the class the student sees, never from storage. Both constants are read from analytics.js here: the one
definition.

--check, in two parts:

  1. Every page git tracks that loads analytics.js (no browser), read with the local scripts it loads (an escape room's
     engine.js switches its class). It fails if:
       - a page has an Aa toggle (an element AA_TOGGLE matches) and switches none of AA_CLASSES on <body>: a fourth
         class name would report every student as "off";
       - a page that sends game_started switches one of AA_CLASSES on <body> but has no element AA_TOGGLE matches: its
         Aa use would report nothing (a toggle the selector does not know).
     Pages that never send game_started (the parents' guides, the hubs) can never carry aa and are only counted.
  2. In Chromium, with the real analytics.js served as https://maffsgames.co.uk (a Playwright route: nothing leaves the
     machine; the Sheet is read from the posts to the endpoint, GA4 from window.dataLayer), on one game per class name
     and the game with no toggle: a start with the font off carries aa = false, and stays false when storage says on;
     after a click on the page's own toggle the next start carries aa = true, and stays true when storage says off;
     the no-toggle game's start carries no aa; no other event carries aa. GA4 and the Sheet alike.

    python -X utf8 scripts/check-aa-flag.py --check
    python -X utf8 scripts/check-aa-flag.py --selftest   planted faults: a game switching a fourth class name, a toggle
                                                         the selector does not know, and an analytics.js that reads
                                                         the flag from localStorage
"""
import argparse
import json
import mimetypes
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import plant_common as pc  # noqa: E402

ANALYTICS = 'schools/assets/analytics.js'
ORIGIN = 'https://maffsgames.co.uk'
ENDPOINT_HOST = 'script.google.com'
NOT_SERVED = ('docs/', 'scripts/', 'tools/')
# The Chromium sample: one game per class name, and the one listed game with no toggle, each with the button that
# switches that class (None: the first AA_TOGGLE match). spot-the-error and word-problem-decoder show two Aa buttons:
# the shared #a11yToggle (accessible) and their older #a11yBtn (dyslexia, its own key); the second is clicked here.
SAMPLE = (('split-it', 'accessible', None), ('boolean-blitz', 'accessible-mode', None),
          ('spot-the-error', 'dyslexia', '#a11yBtn'), ('complex-converter', None, None))
STORAGE_KEY = 'mfg_accessible'   # the games' own key; set here only to make storage and the class disagree

SCRIPT_SRC = re.compile(r"""<script\b[^>]*\bsrc\s*=\s*["']([^"']+\.m?js)(?:\?[^"']*)?["']""", re.I)
BODY_SWITCH = re.compile(r"""body\.classList\.(?:toggle|add)\(\s*['"]([\w-]+)['"]""")
STARTS = re.compile(r"""['"]game_started['"]""")


def constants(src):
    """(AA_CLASSES, AA_TOGGLE) from analytics.js's text."""
    m = re.search(r"var AA_CLASSES = \[([^\]]*)\];", src)
    t = re.search(r"var AA_TOGGLE = '([^']*)';", src)
    if not m or not t:
        raise ValueError('analytics.js defines no AA_CLASSES or AA_TOGGLE')
    return [c.strip().strip("'\"") for c in m.group(1).split(',') if c.strip()], t.group(1)


def selector_parts(selector):
    """'#a, #b, .c' -> ({'a', 'b'}, {'c'}). Only plain #id and .class parts: anything else is refused."""
    ids, classes = set(), set()
    for part in (p.strip() for p in selector.split(',')):
        m = re.fullmatch(r'([#.])([\w-]+)', part)
        if not m:
            raise ValueError('AA_TOGGLE part %r is not a plain #id or .class: this check cannot read it' % part)
        (ids if m.group(1) == '#' else classes).add(m.group(2))
    return ids, classes


def has_toggle(html, ids, classes):
    for m in re.finditer(r'<[a-zA-Z][^>]*>', html):
        tag = m.group(0)
        i = re.search(r'\bid\s*=\s*["\']([^"\']+)["\']', tag)
        if i and i.group(1) in ids:
            return True
        c = re.search(r'\bclass\s*=\s*["\']([^"\']+)["\']', tag)
        if c and set(c.group(1).split()) & classes:
            return True
    return False


def pages(root=ROOT):
    """{page: (its html, its html plus the text of the local scripts it loads)} for every served page loading analytics.js."""
    out = subprocess.run(['git', 'ls-files', '*.html'], cwd=root, capture_output=True, text=True, check=True)
    res = {}
    for p in out.stdout.split():
        if p.startswith(NOT_SERVED):
            continue
        html = (root / p).read_text(encoding='utf-8')
        if 'analytics.js' not in html:
            continue
        full = [html]
        for u in SCRIPT_SRC.findall(html):
            if re.match(r'(https?:)?//', u):
                continue
            q = os.path.normpath(u.lstrip('/') if u.startswith('/') else os.path.join(os.path.dirname(p), u))
            f = root / q
            if f.is_file() and q != ANALYTICS:
                full.append(f.read_text(encoding='utf-8'))
        res[p] = (html, '\n'.join(full))
    return res


def analyse(pg, aa_classes, toggle):
    """-> (errors, counts) for {page: (html, full text)}."""
    ids, classes = selector_parts(toggle)
    errors, counts = [], {'toggle': [], 'no toggle, starts': [], 'never starts': []}
    for p, (html, full) in sorted(pg.items()):
        switched = set(BODY_SWITCH.findall(full))
        known = switched & set(aa_classes)
        starts = bool(STARTS.search(full))
        tog = has_toggle(html, ids, classes)
        if tog and not known:
            errors.append('%s: has an Aa toggle (%s) but switches none of %s on <body> (it switches %s): aa would always '
                          'be false' % (p, toggle, ', '.join(aa_classes), ', '.join(sorted(switched)) or 'nothing'))
        if starts and known and not tog:
            errors.append('%s: sends game_started and switches %s on <body>, but no element matches AA_TOGGLE (%s): its '
                          'Aa use would report nothing' % (p, ', '.join(sorted(known)), toggle))
        counts['toggle' if tog else 'no toggle, starts' if starts else 'never starts'].append(p)
    return errors, counts


# ---------------------------------------------------------------- part 2: Chromium
GA4 = """() => (window.dataLayer || []).filter(a => a && a[0] === 'event').map(a => Object.assign({ event: a[1] }, a[2] || {}))"""


def browse(served, toggle):
    """{slug: {'starts': [...]} } for each SAMPLE game, with {repo path: text} served in place of the files."""
    import bank_common as bc
    from playwright.sync_api import sync_playwright
    out = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for slug, cls, button in SAMPLE:
            posts, errs = [], []
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

            ctx.route('**/*', route)   # route() closes over this game's posts: defined in the loop body
            page = ctx.new_page()
            page.on('pageerror', lambda e, errs=errs: errs.append(str(e)))
            page.goto(ORIGIN + '/games/%s/?cb=aa' % slug, wait_until='load')
            page.wait_for_function('typeof window.mfg === "function"', timeout=15000)
            page.wait_for_timeout(300)
            body = lambda: page.evaluate('Array.from(document.body.classList)')   # noqa: E731
            start = lambda n: page.evaluate(   # noqa: E731
                "n => { window.mfg('question_answered', { game_slug: 'aa-check', level: 'gcse', question_index: 1, correct: true });"
                " window.mfg('game_completed', { game_slug: 'aa-check', level: 'gcse', score: 0 });"
                " window.mfg('game_started', { game_slug: 'aa-check', level: 'gcse', mode: n }); }", n)
            res = {'class': cls, 'errors': errs, 'steps': []}
            # off, then off with storage saying on (the games' own values '1' and 'true' alike)
            res['steps'].append(('off', body()))
            start('off')
            page.evaluate("k => localStorage.setItem(k, 'true')", STORAGE_KEY)
            res['steps'].append(('off, storage says on', body()))
            start('off, storage says on')
            if cls:
                page.locator(button or toggle).first.click()
                page.wait_for_timeout(100)
                res['steps'].append(('on (toggle clicked)', body()))
                start('on (toggle clicked)')
                page.evaluate("k => localStorage.setItem(k, 'false')", STORAGE_KEY)
                res['steps'].append(('on, storage says off', body()))
                start('on, storage says off')
            page.wait_for_timeout(400)
            res['sheet'] = list(posts)
            res['ga4'] = page.evaluate(GA4)
            out[slug] = res
            ctx.close()
        browser.close()
    return out


def judge(res, aa_classes):
    fails = []
    for slug, r in res.items():
        if r['errors']:
            fails.append('%s: page errors: %s' % (slug, '; '.join(r['errors'][:3])))
        for where in ('sheet', 'ga4'):
            evs = r[where]
            for e in evs:
                if e.get('event') != 'game_started' and 'aa' in e:
                    fails.append('%s (%s): %s carries aa' % (slug, where, e.get('event')))
            starts = {e.get('mode'): e for e in evs if e.get('event') == 'game_started' and e.get('game_slug') == 'aa-check'}
            for step, classes in r['steps']:
                e = starts.get(step)
                on = bool(set(classes) & set(aa_classes))
                want = None if r['class'] is None else on
                if e is None:
                    fails.append('%s (%s): no game_started for step %r' % (slug, where, step))
                elif want is None and 'aa' in e:
                    fails.append('%s (%s): no Aa toggle, but game_started carries aa = %r' % (slug, where, e['aa']))
                elif want is not None and e.get('aa') is not want:
                    fails.append('%s (%s), %s: game_started carries aa = %r, the body says %s (classes %s)'
                                 % (slug, where, step, e.get('aa', '(none)'), want, ' '.join(classes) or 'none'))
            if r['class'] and not any(r['class'] in c for s, c in r['steps'] if s.startswith('on')):
                fails.append('%s: the toggle click did not switch %s on <body>' % (slug, r['class']))
    return fails


def summary(res):
    lines = []
    for slug, r in res.items():
        got = {e.get('mode'): e.get('aa', '(none)') for e in r['sheet'] if e.get('event') == 'game_started'}
        lines.append('  %s (%s): %s' % (slug, r['class'] or 'no toggle',
                                        '; '.join('%s -> aa %s' % (s, got.get(s, '?')) for s, _ in r['steps'])))
    return lines


# ---------------------------------------------------------------- self-test
def selftest():
    src = (ROOT / ANALYTICS).read_text(encoding='utf-8')
    aa_classes, toggle = constants(src)
    pg = pages()
    failed, total = 0, 0

    def report(name, ok, detail=''):
        nonlocal failed, total
        total += 1
        failed += not ok
        print('%s: %s%s' % ('PASS' if ok else 'FAIL', name, '' if ok else ' (%s)' % detail))

    errors, _ = analyse(pg, aa_classes, toggle)
    report('the real pages pass', not errors, '; '.join(errors[:3]))
    g = 'games/split-it/index.html'
    html, full = pg[g]
    fourth = pc.apply_plant(full, "document.body.classList.toggle('accessible',on)",
                            "document.body.classList.toggle('aa-mode',on)", name='a fourth class name')
    errs, _ = analyse({g: (html, fourth)}, aa_classes, toggle)
    report('PLANT: a game switching a fourth class name is caught', pc.is_caught([e for e in errs if 'none of' in e]), errs)
    unknown = pc.apply_plant(html, 'class="a11y-toggle" id="a11yToggle"', 'class="aa-switch" id="aaSwitch"',
                             name='a toggle the selector does not know')
    errs, _ = analyse({g: (unknown, full.replace(html, unknown))}, aa_classes, toggle)
    report('PLANT: a toggle the selector does not know is caught', pc.is_caught([e for e in errs if 'no element' in e]), errs)
    storage = pc.apply_plant(src, """    for (var i = 0; i < AA_CLASSES.length; i++) {
      if (b.classList.contains(AA_CLASSES[i])) return true;
    }
    return false;""", """    var v = null;
    try { v = localStorage.getItem('mfg_accessible'); } catch (e) {}
    return v === 'true' || v === '1';""", name='the flag read from localStorage')
    fails = judge(browse({ANALYTICS: storage}, toggle), aa_classes)
    report('PLANT: an analytics.js that reads the flag from localStorage is caught (storage and the class disagree)',
           pc.is_caught([f for f in fails if 'the body says' in f]), fails[:3])
    print('Aa flag selftest: %d/%d passed' % (total - failed, total))
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
        aa_classes, toggle = constants((ROOT / ANALYTICS).read_text(encoding='utf-8'))
        errors, counts = analyse(pages(), aa_classes, toggle)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print('FAIL: cannot check the Aa flag: %s' % exc)
        return 1
    res = browse({}, toggle)
    errors += judge(res, aa_classes)
    for line in summary(res):
        print(line)
    for e in errors:
        print('FAIL: %s' % e)
    print('Aa flag: %d pages load analytics.js; %d have an Aa toggle (%s), %d send game_started with none (%s), %d never '
          'send game_started; Chromium on %s; %d failures'
          % (sum(len(v) for v in counts.values()), len(counts['toggle']), toggle, len(counts['no toggle, starts']),
             ', '.join(counts['no toggle, starts']) or 'none', len(counts['never starts']),
             ', '.join(s for s, _, _ in SAMPLE), len(errors)))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
