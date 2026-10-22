#!/usr/bin/env python3
"""K() punctuation scan (contract K-PUNCTUATION-SCAN, Jon, 22 Oct 2026). REPORT ONLY, not wired into CI.

    python scripts/scan-k-punctuation.py                      # every game in the set, the report's numbers
    python scripts/scan-k-punctuation.py --game suvat         # one game (repeatable)
    python scripts/scan-k-punctuation.py --sessions 3 --max-q 40 --json out.json

THE QUESTION
-------------------------------------------------------------------------------
MATHTEXT-NOWRAP (#471) fixed a fault in the shared renderer, MaffsText.html(): KaTeX's span and the prose after it
were separate inline content, so a line could break between the maths and the punctuation straight after it (a line
starting with "." or ")"), or between an opening bracket and the maths after it. The games that render KaTeX
through their own code were not measured. This script measures them, by line box, in Chromium, in KaTeX's real
(pinned) fonts, never by reading the markup.

THE SET
-------------------------------------------------------------------------------
Every game page (games/<slug>/index.html, the withdrawn one excepted) that calls katex.renderToString or
katex.render itself and does not load schools/assets/mathtext.js. Computed here from the files, printed on every
run; the contract's "36" was the home lane's count on 21 Oct.

THE WALK
-------------------------------------------------------------------------------
Each game is played by check-answer-lock.py's Driver (its seeded Math.random, its scaled timers, the page's own
maffs-lock-hint), so no game is changed or given an adapter here. For each roster level and each of --sessions seeds (2) the start screen is
measured, and the shared "Worked Example" overlay where a game has one (#methodOverlay, opened as its button does), then up to --max-q questions are answered, rotating through the options (so right and wrong feedback
are both seen), and every question screen and every screen after a mark is measured. A screen is measured at
320, 375 and 390 px wide (the viewport resized, layout settled, fonts loaded).

THE MEASURE (test-mathtext.py's line-box method, widened to the games' markup)
-------------------------------------------------------------------------------
For each visible inline .katex (display maths excluded): the first text after it in document order, within the
same block, that is not whitespace-led. If it starts with closing punctuation (. , ; : ! ? ) ] and closing quotes)
and that character's line box is not on the line of the maths' last box, the line starts with punctuation. And
the last text before it: if it ends with an opening bracket or quote whose line box is not on the line of the
maths' first box, the line ends with an orphaned opening bracket. A screen "has a candidate" when any maths on it
touches such a mark; only those can be affected.

THE SOURCE (--static-only prints it alone)
-------------------------------------------------------------------------------
Every place where a KaTeX helper's output is joined straight to closing punctuation after it, or to an opening
bracket before it (`K(x) + '.'`, `'(' + K(x)`, and inside template literals). In a game that concatenates its own
maths HTML these are the only shapes the fault can take, so a game with none cannot show it, whatever the walk
reached; prose a game parses itself (how-many-parts' renderLine) is seen by the walk only.

OUTPUT: per game, static sites, sessions played, screens measured, distinct screens with a candidate, distinct screens affected,
the widths affected and one example; then the renderer's shape (read from the source) for the report.
"""
import argparse
import asyncio
import glob
import hashlib
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

WIDTHS = (320, 375, 390)

MEASURE_JS = r"""
() => {
  const CLOSE = '.,;:!?)]”’"\'', OPEN = '([“‘"\'';
  const blockOf = (n) => {
    let e = n.nodeType === 1 ? n : n.parentElement;
    while (e && e !== document.body) {
      const d = getComputedStyle(e).display;
      if (!d.startsWith('inline') && d !== 'contents') return e;
      e = e.parentElement;
    }
    return document.body;
  };
  const mid = (node, i) => {
    const r = document.createRange(); r.setStart(node, i); r.setEnd(node, i + 1);
    const rs = r.getClientRects();
    return rs.length ? (rs[0].top + rs[0].bottom) / 2 : null;
  };
  const textNodes = (root) => {
    const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT), out = [];
    while (w.nextNode()) out.push(w.currentNode);
    return out;
  };
  const all = textNodes(document.body);
  const index = new Map(all.map((t, i) => [t, i]));
  const visible = (e) => { const r = e.getClientRects(); return r.length && r[0].width > 0 && getComputedStyle(e).visibility !== 'hidden'; };
  const snippet = (blk, t, i) => {
    const s = (blk.innerText || blk.textContent || '').replace(/\s+/g, ' ').trim();
    return s.length > 140 ? s.slice(0, 140) + '...' : s;
  };
  const cands = [], bad = [];
  document.querySelectorAll('.katex').forEach(K => {
    if (K.closest('.katex-display') || !visible(K)) return;
    const rs = K.getClientRects();
    const first = rs[0], last = rs[rs.length - 1];
    const inner = textNodes(K);
    if (!inner.length) return;
    const blk = blockOf(K);
    // after: the first non-empty text node after K's last text node, in the same block
    for (let i = index.get(inner[inner.length - 1]) + 1; i < all.length; i++) {
      const t = all[i];
      if (K.contains(t) || !t.data.length) continue;
      if (blockOf(t) !== blk) break;
      if (CLOSE.indexOf(t.data[0]) >= 0) {
        cands.push('after');
        const m = mid(t, 0);
        if (m !== null && (m > last.bottom || m < last.top)) bad.push({ kind: 'line starts with ' + JSON.stringify(t.data[0]), text: snippet(blk) });
      }
      break;
    }
    // before: the last non-empty text node before K's first text node, in the same block
    for (let i = index.get(inner[0]) - 1; i >= 0; i--) {
      const t = all[i];
      if (!t.data.length) continue;
      if (blockOf(t) !== blk) break;
      if (t.parentElement && t.parentElement.closest('.katex')) break;   // the maths before it: not prose
      const c = t.data[t.data.length - 1];
      if (OPEN.indexOf(c) >= 0) {
        cands.push('before');
        const m = mid(t, t.data.length - 1);
        if (m !== null && (m > first.bottom || m < first.top)) bad.push({ kind: 'line ends with ' + JSON.stringify(c), text: snippet(blk) });
      }
      break;
    }
  });
  const sig = (document.body.innerText || '').replace(/\s+/g, ' ').trim();
  return { cands: cands.length, bad, sig };
}
"""


def game_set():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'games', '*', 'index.html'))):
        slug = os.path.basename(os.path.dirname(f))
        html = open(f, encoding='utf-8').read()
        if '_withdrawn' in html and 'noindex' in html and len(html) < 6000:
            continue
        if re.search(r'katex\.(renderToString|render)\s*\(', html) and 'assets/mathtext.js' not in html:
            out.append(slug)
    return out


CLOSE_CH, OPEN_CH = '.,;:!?)]\u201d\u2019', '([\u201c\u2018'
DEF_RE = re.compile(r'(?:function\s+([A-Za-z_$][\w$]*)\s*\(|([A-Za-z_$][\w$.]*)\s*=\s*(?:function\s*\(|\([^)]*\)\s*=>|[A-Za-z_$][\w$]*\s*=>))')


def helpers(src):
    """Names whose definition renders KaTeX within its first 400 characters, plus katex.renderToString itself."""
    out = {'katex.renderToString'}
    for m in DEF_RE.finditer(src):
        name = m.group(1) or m.group(2)
        if name and 'renderToString' in src[m.end():m.end() + 400]:
            out.add(name)
    return out


def _close(src, i):
    """Index just past the parenthesis matching src[i] == '(', skipping string literals; -1 if none."""
    depth, q = 0, None
    while i < len(src):
        c = src[i]
        if q:
            if c == '\\':
                i += 1
            elif c == q:
                q = None
        elif c in '\'"`':
            q = c
        elif c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return -1


def static_sites(slug):
    """Every place in the game's source where a KaTeX helper's output is joined straight to closing punctuation
    after it, or to an opening bracket before it: `K(x) + '.'`, `'(' + K(x)`, and the same inside a template
    literal (`${K(x)}.`, `(${K(x)}`). The only shapes in which the fault can arise in a game that builds its own
    maths HTML; a game with none cannot show it, whatever a walk reaches. [(line, 'after'|'before', snippet)]"""
    src = open(os.path.join(ROOT, 'games', slug, 'index.html'), encoding='utf-8').read()
    names = sorted(helpers(src), key=len, reverse=True)
    call = re.compile(r'(?<![\w$.])(' + '|'.join(re.escape(n) for n in names) + r')\s*\(')
    sites = []
    for m in call.finditer(src):
        before = src[max(0, m.start() - 40):m.start()]
        if re.search(r'(function\s+|=\s*)$', before) and src[m.end():m.end() + 1] != ')':
            pass
        end = _close(src, m.end() - 1)
        if end < 0:
            continue
        line = src.count('\n', 0, m.start()) + 1
        tail = src[end:end + 40]
        if re.match(r"\s*\+\s*['\"`]([.,;:!?)\]\u201d\u2019])", tail) or re.match(r'\}([.,;:!?)\]\u201d\u2019])', tail):
            sites.append((line, 'after', (src[m.start():end] + tail[:6]).replace('\n', ' ')[:90]))
        if re.search(r"[(\[\u201c\u2018]['\"`]\s*\+\s*$", before) or re.search(r'[(\[\u201c\u2018]\$\{$', before):
            sites.append((line, 'before', (before[-6:] + src[m.start():end]).replace('\n', ' ')[:90]))
    return sites


def renderer_shape(slug):
    """How the game turns TeX into HTML, read from its source: the facts the report's 'could K() be swapped for
    MaffsText.html directly?' column rests on."""
    html = open(os.path.join(ROOT, 'games', slug, 'index.html'), encoding='utf-8').read()
    k_def = re.search(r'(function\s+K\s*\(|(var|const|let)\s+K\s*=)', html)
    delim = bool(re.search(r'\\\\\\?\(|\\\\\(\[\\s\\S\]|\\\$\\\$|/\\\\\\\(', html)) or \
        bool(re.search(r"split\(\s*/\(\\\$|replace\(\s*/\\\$", html))
    calls = len(re.findall(r'\bK\s*\(', html)) - (1 if k_def else 0)
    rts = len(re.findall(r'katex\.renderToString\s*\(', html))
    rnd = len(re.findall(r'katex\.render\s*\(', html))
    auto = 'renderMathInElement' in html
    return {'K': bool(k_def), 'K_calls': max(calls, 0), 'renderToString': rts, 'render': rnd,
            'delimiter_parser': delim, 'auto_render': auto}


def load_lock():
    spec = importlib.util.spec_from_file_location('check_answer_lock', os.path.join(HERE, 'check-answer-lock.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.CHECK_SITE = mod.load_check_site()
    return mod


async def settle(page):
    await page.evaluate("document.fonts.ready")
    await page.evaluate("new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))")


async def measure(page, height):
    """{width: result} at the three widths, the viewport restored to 390 after."""
    res = {}
    for w in WIDTHS:
        await page.set_viewport_size({'width': w, 'height': height})
        await settle(page)
        res[w] = await page.evaluate(MEASURE_JS)
    await page.set_viewport_size({'width': 390, 'height': height})
    await settle(page)
    return res


async def scan_game(lock, browser, base, slug, sessions, max_q):
    html = open(os.path.join(ROOT, 'games', slug, 'index.html'), encoding='utf-8').read()
    hint = lock.read_hint(html)[0]
    levels, _ = bc.roster_levels()
    lv = [hint['level']] if hint.get('level') else (levels.get(slug) or [None])
    rec = {'slug': slug, 'levels': lv, 'sessions': 0, 'screens': 0, 'cand_screens': {}, 'bad_screens': {}, 'notes': []}
    height = 844

    for level, seed in [(l, s) for l in lv for s in range(1, sessions + 1)]:
        url = base + '/games/%s/%s' % (slug, ('?level=%s' % level) if level else '')
        ctx = await browser.new_context(viewport={'width': 390, 'height': height})
        await ctx.add_init_script(lock.CHECK_SITE.TIER3_INIT)
        await ctx.add_init_script(lock.INIT % {'scale': lock.TIME_SCALE, 'seed': seed})

        async def route(r):
            u = r.request.url
            if u.startswith(base):
                await r.continue_()
            elif bc.is_font_cdn(u):
                await bc.serve_real_font_async(r)
            else:
                await r.abort()
        await ctx.route('**/*', route)
        page = await ctx.new_page()
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)[:120]))
        try:
            await page.goto(url, wait_until='load', timeout=20000)
            await page.wait_for_timeout(300)
            if not await page.evaluate("typeof katex !== 'undefined'"):
                rec['notes'].append('%s seed %d: KaTeX did not load' % (level, seed))

            def take(res, where):
                rec['screens'] += 1
                for w, r in res.items():
                    key = hashlib.sha1(r['sig'].encode()).hexdigest()[:12]
                    if r['cands']:
                        rec['cand_screens'][key] = where
                    for b in r['bad']:
                        s = rec['bad_screens'].setdefault(key, {'where': where, 'widths': set(), 'example': b})
                        s['widths'].add(w)
            take(await measure(page, height), 'start screen')
            # The shared "Worked Example" overlay (renderMethodRef, eight games): opened as its button does, measured,
            # closed. The walk never reaches it otherwise, and its prose is built round the maths.
            if await page.evaluate("() => { const o = document.getElementById('methodOverlay'); if (!o) return false; o.classList.add('show'); return true; }"):
                take(await measure(page, height), 'worked example')
                await page.evaluate("() => document.getElementById('methodOverlay').classList.remove('show')")
            d = lock.Driver(page, slug, hint)
            if not await d.start():
                rec['notes'].append('%s seed %d: not playable by the driver (no option group or input after Start)' % (level, seed))
                await ctx.close()
                continue
            rec['sessions'] += 1
            for q in range(max_q):
                take(await measure(page, height), 'question')
                s = await d.answer(q)
                if s is None:
                    take(await measure(page, height), 'end or unanswerable')
                    break
                take(await measure(page, height), 'after a mark')
                if await d.to_next(s['lastFresh']) is None:
                    take(await measure(page, height), 'end of session')
                    break
        except Exception as e:      # a crash is reported, never a pass
            rec['notes'].append('%s seed %d: driver error: %s' % (level, seed, str(e).splitlines()[0][:140]))
        if errs:
            rec['notes'].append('%s seed %d: page errors: %s' % (level, seed, '; '.join(sorted(set(errs))[:2])))
        await ctx.close()
    for s in rec['bad_screens'].values():
        s['widths'] = sorted(s['widths'])
    rec['shape'] = renderer_shape(slug)
    rec['static'] = static_sites(slug)
    return rec


PLANT_JS = r"""
(glued) => {
  // The fault planted: maths, then a full stop as separate inline content (the old renderer's shape), in a column
  // narrowed a pixel at a time; glued: the same with the mark and the maths in one nowrap span (#471's fix).
  const box = document.createElement('div');
  box.style.cssText = 'position:absolute;left:0;top:0;font:16px/1.5 sans-serif;background:#fff;z-index:99999';
  const m = katex.renderToString('x^2 + 3x = 28', { throwOnError: false });
  box.innerHTML = 'Work out the value of ' + (glued ? '<span style="white-space:nowrap">' + m + '.</span>' : m + '.') +
    ' Then state how many solutions there are, and (' + (glued ? '<span style="white-space:nowrap">(' + m + '</span>' : m) +
    ') again.';
  document.body.appendChild(box);
  return box;
}
"""


async def selftest():
    """The measure must find the planted fault at some width from 120 to 420 px, and nothing once it is glued."""
    from playwright.async_api import async_playwright
    lock = load_lock()
    proc, base = bc.start_stub_server()
    ok = True
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            for glued in (False, True):
                ctx = await browser.new_context(viewport={'width': 1000, 'height': 800})

                async def route(r):
                    u = r.request.url
                    await (r.continue_() if u.startswith(base) else
                           bc.serve_real_font_async(r) if bc.is_font_cdn(u) else r.abort())
                await ctx.route('**/*', route)
                page = await ctx.new_page()
                await page.goto(base + '/games/suvat/', wait_until='load')
                await page.evaluate("() => { document.body.innerHTML = ''; }")
                await page.evaluate(PLANT_JS, glued)
                hits = 0
                for w in range(120, 421):
                    await page.evaluate("(w) => { document.body.lastChild.style.width = w + 'px'; }", w)
                    await settle(page)
                    hits += bool((await page.evaluate(MEASURE_JS))['bad'])
                good = (hits > 0) != glued
                ok = ok and good
                print('  self-test %-48s %s (%d of 301 widths flagged)' % (
                    'glued (one nowrap span): nothing flagged' if glued else 'planted (maths, then a separate mark)',
                    'PASS' if good else '*** FAIL ***', hits))
                await ctx.close()
            await browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return ok


async def run(games, sessions, max_q, workers):
    from playwright.async_api import async_playwright
    lock = load_lock()
    proc, base = bc.start_stub_server()
    out = {}
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            sem = asyncio.Semaphore(workers)

            async def one(slug):
                async with sem:
                    try:
                        out[slug] = await asyncio.wait_for(scan_game(lock, browser, base, slug, sessions, max_q), 900)
                    except Exception as e:
                        out[slug] = {'slug': slug, 'sessions': 0, 'screens': 0, 'cand_screens': {}, 'bad_screens': {},
                                     'notes': ['scan error: %s' % str(e).splitlines()[0][:140]], 'shape': renderer_shape(slug),
                                     'static': static_sites(slug)}
                    r = out[slug]
                    print('%-28s static sites %3d  sessions %d  screens %4d  with a candidate %3d  affected %3d%s' % (
                        slug, len(r['static']), r['sessions'], r['screens'], len(r['cand_screens']), len(r['bad_screens']),
                        ('  NOTE ' + r['notes'][0]) if r['notes'] else ''), flush=True)
            await asyncio.gather(*(one(s) for s in games))
            await browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--game', action='append')
    ap.add_argument('--sessions', type=int, default=2, help='seeds per level')
    ap.add_argument('--max-q', type=int, default=40)
    ap.add_argument('--workers', type=int, default=3)
    ap.add_argument('--json')
    ap.add_argument('--selftest', action='store_true', help='only the planted fault and its glued control')
    ap.add_argument('--static-only', action='store_true', help='only the source scan for joined punctuation')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    if args.selftest:
        sys.exit(0 if asyncio.run(selftest()) else 1)
    if args.static_only:
        for g in [g for g in game_set() if not args.game or g in args.game]:
            st = static_sites(g)
            print('%-28s %3d %s' % (g, len(st), '; '.join(':%d %s %s' % x for x in st[:3])))
        return
    games = game_set()
    print('The set (%d): %s' % (len(games), ' '.join(games)))
    if args.game:
        games = [g for g in games if g in args.game]
    res = asyncio.run(run(games, args.sessions, args.max_q, args.workers))
    print()
    affected = sorted(s for s, r in res.items() if r['bad_screens'])
    print('Affected games: %d of %d: %s' % (len(affected), len(res), ' '.join(affected) or 'none'))
    for s in affected:
        for b in list(res[s]['bad_screens'].values())[:1]:
            print('  %s (%s at %s px): %s -- %s' % (s, b['where'], '/'.join(map(str, b['widths'])),
                                                  b['example']['kind'], b['example']['text']))
    unwalked = sorted(s for s, r in res.items() if not r['sessions'])
    print('Not walked: %d: %s' % (len(unwalked), '; '.join('%s (%s)' % (s, res[s]['notes'][0] if res[s]['notes'] else '?')
                                                         for s in unwalked) or 'none'))
    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(res, f, indent=1, default=list)


if __name__ == '__main__':
    main()
