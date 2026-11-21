#!/usr/bin/env python3
# ci-line: Site navigation (back link to the hub the student came from, kept on reload and level switch, as written otherwise; stage-exit's row and HUD agree; the margin logo only where it fits; planted faults caught) | --selftest && --check
# ci-deps: schools/assets/site-nav.js schools/assets/stage-exit.js schools/assets/favicon.svg games/angle-ace/index.html games/free-daily-pizza/index.html games/52dle/index.html games/chart-interrogator/index.html op/index.html essentials/index.html
"""Site navigation (contract SITE-NAV, Jon 21 Nov 2026; canon §7.5.8): schools/assets/site-nav.js.

    python scripts/check-site-nav.py --static     # the static rule (check-site.py runs this in its site-wide part)
    python scripts/check-site-nav.py --check      # the rule, then the pages played in Chromium
    python scripts/check-site-nav.py --selftest   # planted faults caught (static and Chromium)
    python scripts/check-site-nav.py --survey     # the logo on every back-link page at 1920x1080: shown or what blocks it

THE STATIC RULE (static_faults(); in check-site.py's site-wide part, so it runs on every pull request with no new
always-run line, ALWAYS_BUDGET being full):
  1. every page with an a.back-link loads site-nav.js exactly once (scripts/apply-site-nav.py writes the tag);
  2. HUBS in site-nav.js holds every page outside games/ that links to a game page (a new hub is labelled there);
  3. a page carrying <html data-site-logo="off"> is on LOGO_OPT_OUT below with its reason, and a page that shows its
     own logo (class logo, numblr-logo or header-logo) and loads site-nav.js carries it.

IN CHROMIUM (--check), served by serve-stubbed.py with the network cut:
  - Angle Ace opened from /op/: every a.back-link goes to /op/ and reads "← Back to OP for Secondary"; reloaded, and
    with ?level= changed, the same; opened with no referrer, and from another game, every link exactly as written;
  - Free Daily Pizza (stage-exit) opened from /essentials/: its row link and its HUD home link both go to /essentials/;
  - the logo: shown at 1920x1080 on Angle Ace, links to "/", is named "MaffsGames home", and nothing painted comes
    within its clear space at any scroll position (hit-tested with elementsFromPoint, not site-nav.js's own measure);
    hidden at 390x844 and on a 768x1024 tablet; hidden on Chart Interrogator (its header bar runs the full width); absent on 52-dle.
"""
import argparse
import html as htmllib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSET = os.path.join(ROOT, 'schools', 'assets', 'site-nav.js')
TAG = '<script src="/schools/assets/site-nav.js"></script>'
LOADS = re.compile(r'<script\b[^>]*\bsrc="[^"]*schools/assets/site-nav\.js"[^>]*>\s*</script>')
BACK_LINK = re.compile(r'<a\b[^>]*\bclass="[^"]*\bback-link\b')
OWN_LOGO = re.compile(r'\bclass="[^"]*\b(?:logo|numblr-logo|header-logo)\b')
OPT_OUT_ATTR = re.compile(r'<html\b[^>]*\bdata-site-logo="off"')
SKIP_DIRS = {'docs', 'tools', 'node_modules', 'scripts', 'claude'}

# Pages that keep the margin logo off, each with its reason (contract SITE-NAV names them). Shrink or grow only with a
# reason; a page carrying the attribute and missing here fails, and so does an entry for a page without it.
LOGO_OPT_OUT = {
    'games/equatle/index.html': 'its header is the site logo already ("Maffs Games", a.logo to /)',
    'games/52dle/index.html': 'named in SITE-NAV: its header is its own title card ("52-dle"), kept free of a second mark',
    'games/as-you-can-see/index.html': 'its start screen has its own logo artwork (svg.logo, a chart under a magnifying glass)',
    'games/possibly-maybe/index.html': 'its start screen has its own logo artwork (svg.logo, a probability scale with a dice)',
    'games/wrong-on-the-internet/index.html': 'its posts carry the Numblr site logo (.numblr-logo): one logo on screen',
}

HUB_PAGE = 'op/index.html'
GAME = 'games/angle-ace/index.html'            # a centred-column game OP for Secondary links (as ?level=year6)
OTHER_GAME = 'games/factor-race/index.html'
STAGE_GAME = 'games/free-daily-pizza/index.html'   # stage-exit, with a HUD; Essentials links it
STAGE_HUB = 'essentials/index.html'
FULL_WIDTH = 'games/chart-interrogator/index.html'   # its header bar runs the full width: no margin
OWN_LOGO_GAME = 'games/52dle/index.html'


def read(rel):
    with open(os.path.join(ROOT, rel), encoding='utf-8') as f:
        return f.read()


def pages():
    """Every served .html page, repo-relative, sorted (no dot or underscore folders, docs, tools, scripts)."""
    out = []
    for d, dirs, files in os.walk(ROOT):
        rel = os.path.relpath(d, ROOT)
        dirs[:] = [x for x in dirs if not x.startswith(('.', '_')) and (rel != '.' or x not in SKIP_DIRS)]
        for f in files:
            if f.endswith('.html') and not f.startswith('_'):
                out.append(os.path.normpath(os.path.join(rel, f)).replace(os.sep, '/'))
    return sorted(out)


def back_link_pages(texts=None):
    texts = texts or {r: read(r) for r in pages()}
    return [r for r, t in sorted(texts.items()) if BACK_LINK.search(t)]


def hubs(js=None):
    """{path: label} from site-nav.js's HUBS."""
    js = js if js is not None else open(ASSET, encoding='utf-8').read()
    m = re.search(r'var HUBS = \{(.*?)\n  \};', js, re.S)
    return dict(re.findall(r"'([^']+)':\s*'((?:[^'\\]|\\.)*)'", m.group(1))) if m else {}


def url_path(rel):
    """The URL path a page is served at: games/x/index.html -> /games/x/."""
    return '/' + re.sub(r'(^|/)index\.html$', r'\1', rel)


def links_to_game(rel, text):
    d = os.path.dirname(rel)
    for h in re.findall(r'href="([^"#?]+)', text):
        if h.startswith(('http:', 'https:', 'mailto:', '//')):
            continue
        p = h.lstrip('/') if h.startswith('/') else os.path.normpath(os.path.join(d, h)).replace(os.sep, '/')
        if p.startswith('games/') and len(p.strip('/').split('/')) >= 2:
            return True
    return False


def static_faults(texts=None, js=None, opt_out=None):
    texts = texts or {r: read(r) for r in pages()}
    opt_out = LOGO_OPT_OUT if opt_out is None else opt_out
    hub = hubs(js)
    out = []
    if not hub:
        out.append('site-nav.js: no HUBS map found')
    for r in back_link_pages(texts):
        n = len(LOADS.findall(texts[r]))
        if n != 1:
            out.append('%s: has an a.back-link and loads site-nav.js %d time(s) (once: python scripts/apply-site-nav.py)' % (r, n))
    for r, t in sorted(texts.items()):
        if r.startswith('games/') or not links_to_game(r, t):
            continue
        if url_path(r) not in hub:
            out.append('%s: links to a game but %s is not in site-nav.js HUBS (a back link from that game cannot name it)'
                       % (r, url_path(r)))
    for r, t in sorted(texts.items()):
        off = bool(OPT_OUT_ATTR.search(t))
        if off and r not in opt_out:
            out.append('%s: data-site-logo="off" without an entry and reason in LOGO_OPT_OUT' % r)
        if not off and r in opt_out:
            out.append('%s: on LOGO_OPT_OUT but its <html> does not carry data-site-logo="off"' % r)
        if not off and LOADS.search(t) and OWN_LOGO.search(t):
            out.append('%s: shows a logo of its own (class logo, numblr-logo or header-logo) but does not opt out of the '
                       'margin logo (data-site-logo="off", with a LOGO_OPT_OUT reason)' % r)
    for r in opt_out:
        if r not in texts:
            out.append('%s: on LOGO_OPT_OUT but no such page' % r)
    return out


def static_report():
    """For check-site.py: print the static rule's result, return the faults."""
    f = static_faults()
    print('  site nav (contract SITE-NAV): %d page(s) with an a.back-link, %d hub(s); %s'
          % (len(back_link_pages()), len(hubs()), 'PASS' if not f else '%d fault(s)' % len(f)))
    for x in f:
        print('    FAIL  ' + x)
    return f


# ---------- Chromium ----------
LINKS_JS = '() => [...document.querySelectorAll("a.back-link")].map(a => [a.getAttribute("href"), a.textContent.trim(), a.getAttribute("aria-label")])'

# The logo, judged independently of site-nav.js's own measure: at scroll positions down the page, every element under a
# grid of points over the logo and its clear space (elementsFromPoint) that paints anything there is a touch.
TOUCH_JS = r"""async () => {
  const L = document.querySelector('.maffs-site-logo');
  if (!L || getComputedStyle(L).display === 'none') return {shown: false, blocked: L ? L.getAttribute('data-blocked-by') : 'no logo'};
  const r = L.getBoundingClientRect(), pad = 12, out = [];
  const paints = (el) => {
    const cs = getComputedStyle(el);
    if (/^(IMG|SVG|CANVAS|VIDEO|INPUT|BUTTON|SELECT|TEXTAREA|IFRAME)$/i.test(el.tagName)) return true;
    if (cs.backgroundColor && !/rgba\([^)]*,\s*0\)$|transparent/.test(cs.backgroundColor)) return true;
    if (cs.backgroundImage !== 'none' || cs.boxShadow !== 'none') return true;
    if (['Top','Right','Bottom','Left'].some(s => parseFloat(cs['border'+s+'Width']) > 0 && cs['border'+s+'Style'] !== 'none')) return true;
    return [...el.childNodes].some(n => n.nodeType === 3 && /\S/.test(n.nodeValue));
  };
  const H = Math.max(document.documentElement.scrollHeight, innerHeight);
  for (let y = 0; y <= H; y += Math.max(100, innerHeight / 3)) {
    scrollTo(0, y);
    await new Promise(res => requestAnimationFrame(() => requestAnimationFrame(res)));
    for (let x = r.left - pad; x <= r.right + pad; x += 8) for (let yy = r.top - pad; yy <= r.bottom + pad; yy += 8) {
      if (x < 0 || yy < 0) continue;
      for (const el of document.elementsFromPoint(x, yy)) {
        if (el === L || L.contains(el) || el === document.body || el === document.documentElement) continue;
        if (paints(el)) { out.push(el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + ' at scroll ' + Math.round(y)); break; }
      }
      if (out.length) break;
    }
    if (out.length) break;
  }
  scrollTo(0, 0);
  return {shown: true, touches: out, href: L.getAttribute('href'), name: L.getAttribute('aria-label')};
}"""


def as_written(text):
    """[[href, text, aria-label]] for each a.back-link exactly as the page's HTML writes it."""
    out = []
    for m in re.finditer(r'<a\b([^>]*\bclass="[^"]*\bback-link\b[^"]*"[^>]*)>(.*?)</a>', text, re.S):
        attrs, inner = m.groups()
        h = re.search(r'\bhref="([^"]*)"', attrs)
        a = re.search(r'\baria-label="([^"]*)"', attrs)
        out.append([htmllib.unescape(h.group(1)) if h else None, htmllib.unescape(re.sub(r'<[^>]+>', '', inner)).strip(),
                    htmllib.unescape(a.group(1)) if a else None])
    return out


def browser_faults(swap=None, only=None, js_swap=None):
    """[fault] from the pages played in Chromium. swap {served path: html} and js_swap {served path: javascript} serve
    planted copies instead of the repo's files."""
    from playwright.sync_api import sync_playwright
    sys.path.insert(0, HERE)
    import bank_common as bc
    swap = swap or {}
    js_swap = js_swap or {}
    proc, base = bc.start_stub_server()
    faults = []

    def want(name):
        return only is None or name in only

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()

            def context(**kw):
                ctx = browser.new_context(**kw)
                bc.offline(ctx, base)
                def serve(text, kind):          # one argument: Playwright passes (route, request) to a two-argument handler
                    def handle(route):
                        route.fulfill(status=200, content_type=kind + '; charset=utf-8', body=text.encode('utf-8'))
                    return handle
                for path, text in swap.items():
                    ctx.route(base + path + '*', serve(text, 'text/html'))
                for path, text in js_swap.items():
                    ctx.route(base + path, serve(text, 'application/javascript'))
                return ctx

            def open_from(page, hub_rel, target):
                page.goto(base + url_path(hub_rel), wait_until='load')
                page.evaluate('(u) => { location.href = u; }', target)
                page.wait_for_load_state('load')
                page.wait_for_timeout(150)

            game_url = url_path(GAME) + '?level=year6'
            if want('hub'):
                ctx = context(viewport={'width': 1280, 'height': 800})
                page = ctx.new_page()
                open_from(page, HUB_PAGE, game_url)
                got = page.evaluate(LINKS_JS)
                if not got or any(h != '/op/' or t != '← Back to OP for Secondary' for h, t, _ in got):
                    faults.append('from /op/: %s back links are %s, not /op/ and "← Back to OP for Secondary"' % (GAME, got))
                page.reload(wait_until='load')
                page.wait_for_timeout(150)
                if page.evaluate(LINKS_JS) != got:
                    faults.append('from /op/, reloaded: %s back links are %s' % (GAME, page.evaluate(LINKS_JS)))
                page.goto(base + url_path(GAME) + '?level=ks3', wait_until='load')
                page.wait_for_timeout(150)
                if page.evaluate(LINKS_JS) != got:
                    faults.append('from /op/, then ?level=ks3: %s back links are %s' % (GAME, page.evaluate(LINKS_JS)))
                ctx.close()
            if want('direct'):
                written = as_written(swap.get(url_path(GAME), read(GAME)))
                ctx = context(viewport={'width': 1280, 'height': 800})
                page = ctx.new_page()
                page.goto(base + game_url, wait_until='load')
                page.wait_for_timeout(150)
                if page.evaluate(LINKS_JS) != written:
                    faults.append('no referrer: %s back links are %s, written %s' % (GAME, page.evaluate(LINKS_JS), written))
                page2 = ctx.new_page()
                open_from(page2, OTHER_GAME, game_url)
                if page2.evaluate(LINKS_JS) != written:
                    faults.append('from another game: %s back links are %s, written %s' % (GAME, page2.evaluate(LINKS_JS), written))
                ctx.close()
            if want('stage'):
                ctx = context(viewport={'width': 1280, 'height': 800})
                page = ctx.new_page()
                open_from(page, STAGE_HUB, url_path(STAGE_GAME))
                got = page.evaluate('() => [[...document.querySelectorAll(".stage-exit-row a.back-link")].map(a => a.getAttribute("href")),'
                                    ' [...document.querySelectorAll(".stage-exit-home")].map(a => a.getAttribute("href"))]')
                if not got[0] or not got[1] or set(got[0] + got[1]) != {'/essentials/'}:
                    faults.append('from /essentials/: %s stage-exit row links %s and HUD home links %s, not all /essentials/'
                                  % (STAGE_GAME, got[0], got[1]))
                ctx.close()
            if want('logo'):
                for rel, vp, touch, expect in ((GAME, (1920, 1080), False, 'shown'), (GAME, (390, 844), True, 'hidden'),
                                               (GAME, (768, 1024), True, 'hidden'), (FULL_WIDTH, (1920, 1080), False, 'hidden'),
                                               (OWN_LOGO_GAME, (1920, 1080), False, 'absent')):
                    ctx = context(viewport={'width': vp[0], 'height': vp[1]}, has_touch=touch, is_mobile=touch)
                    page = ctx.new_page()
                    page.goto(base + url_path(rel), wait_until='load')
                    page.wait_for_timeout(700)
                    n = page.evaluate('() => document.querySelectorAll(".maffs-site-logo").length')
                    res = page.evaluate(TOUCH_JS)
                    where = '%s at %dx%d%s' % (rel, vp[0], vp[1], ' (touch)' if touch else '')
                    if expect == 'absent' and n:
                        faults.append('logo: %s has the margin logo (it opts out)' % where)
                    elif expect == 'hidden' and res.get('shown'):
                        faults.append('logo: shown on %s, where it must be hidden (it touches %s)' % (where, ', '.join(res['touches']) or 'nothing'))
                    elif expect == 'shown':
                        if not res.get('shown'):
                            faults.append('logo: hidden on %s (blocked by %s), where the margin fits it' % (where, res.get('blocked')))
                        elif res['touches'] or res['href'] != '/' or res['name'] != 'MaffsGames home':
                            faults.append('logo: on %s it touches %s, links to %s, is named %r' % (where, res['touches'] or 'nothing',
                                                                                                 res['href'], res['name']))
                    ctx.close()
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return faults


def survey():
    from playwright.sync_api import sync_playwright
    sys.path.insert(0, HERE)
    import bank_common as bc
    proc, base = bc.start_stub_server()
    shown, hidden = [], []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 1920, 'height': 1080})
            bc.offline(ctx, base)
            for rel in back_link_pages():
                page = ctx.new_page()
                try:
                    page.goto(base + url_path(rel), wait_until='load', timeout=20000)
                    page.wait_for_timeout(400)
                    res = page.evaluate(TOUCH_JS)
                    (shown if res.get('shown') else hidden).append((rel, res.get('touches') or res.get('blocked')))
                except Exception as e:
                    hidden.append((rel, 'load error %s' % str(e)[:60]))
                page.close()
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    print('logo at 1920x1080: shown on %d, hidden on %d' % (len(shown), len(hidden)))
    for rel, why in shown:
        print('  shown   %s%s' % (rel, ('  TOUCHES %s' % why) if why else ''))
    for rel, why in hidden:
        print('  hidden  %s  (%s)' % (rel, why))
    return 1 if any(why for _, why in shown) else 0


def selftest():
    fails = []
    texts = {r: read(r) for r in pages()}
    js = open(ASSET, encoding='utf-8').read()
    if static_faults(texts, js):
        fails.append('the repo fails the static rule, so the plants prove nothing: %s' % static_faults(texts, js)[:2])
    planted = dict(texts)
    planted[GAME] = LOADS.sub('', planted[GAME], 1)
    hit = [f for f in static_faults(planted, js) if f.startswith(GAME) and 'loads site-nav.js 0' in f]
    print('  self-test a page without site-nav.js           %s' % ('caught: ' + hit[0][:100] if hit else '*** MISSED ***'))
    fails += [] if hit else ['a page without site-nav.js passed']
    planted_js = js.replace("    '/op/': 'OP for Secondary',\n", '', 1)
    hit = [f for f in static_faults(texts, planted_js) if f.startswith(HUB_PAGE) and 'not in site-nav.js HUBS' in f]
    print('  self-test a hub missing from HUBS              %s' % ('caught: ' + hit[0][:100] if hit else '*** MISSED ***'))
    fails += [] if hit else ['a hub missing from HUBS passed']
    planted = dict(texts)
    planted[OWN_LOGO_GAME] = planted[OWN_LOGO_GAME].replace(' data-site-logo="off"', '', 1)
    hit = [f for f in static_faults(planted, js) if f.startswith(OWN_LOGO_GAME) and 'does not carry' in f]
    print('  self-test an opt-out lost from its page        %s' % ('caught: ' + hit[0][:100] if hit else '*** MISSED ***'))
    fails += [] if hit else ['an opt-out lost from its page passed']
    # In Chromium: the logo planted over content (site-nav.js measuring nothing, on the full-width game) is caught by the
    # independent hit test; a site-nav.js that does not relink is caught from /op/.
    blind = js.replace('function conflict() {', 'function conflict() { return null;', 1)
    swap_js = {'/schools/assets/site-nav.js': blind}
    got = browser_faults(only={'logo'}, js_swap=swap_js)
    hit = [f for f in got if f.startswith('logo: shown on %s' % FULL_WIDTH) and '(it touches nothing)' not in f]
    print('  self-test a logo overlapping content           %s' % ('caught: ' + hit[0][:100] if hit else '*** MISSED *** %s' % got[:1]))
    fails += [] if hit else ['a logo overlapping content passed']
    lazy = js.replace('    if (!nav.backHref) return;\n    var links', '    return;\n    var links', 1)
    got = browser_faults(only={'hub'}, js_swap={'/schools/assets/site-nav.js': lazy})
    hit = [f for f in got if f.startswith('from /op/')]
    print('  self-test back links not relinked from a hub   %s' % ('caught: ' + hit[0][:100] if hit else '*** MISSED ***'))
    fails += [] if hit else ['back links not relinked passed']
    for f in fails:
        print('FAIL  self-test: ' + f)
    print('self-test: %s' % ('FAILED' if fails else 'PASS'))
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--static', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--survey', action='store_true')
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    if args.selftest:
        return selftest()
    if args.survey:
        return survey()
    f = static_report()
    if args.check and not f:
        b = browser_faults()
        for x in b:
            print('FAIL  ' + x)
        f += b
        print('site nav in Chromium: %s' % ('PASS' if not b else 'FAILED'))
    print('FAILED' if f else 'PASS')
    return 1 if f else 0


if __name__ == '__main__':
    sys.exit(main())
