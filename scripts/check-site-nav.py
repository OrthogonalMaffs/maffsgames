#!/usr/bin/env python3
# ci-line: Site navigation (back link to the hub the student came from, kept on reload and level switch, as written otherwise; stage-exit's row and HUD agree; the class page's name carried there and back; the margin logo only where it fits; planted faults caught) | --selftest && --check
# ci-deps: schools/assets/site-nav.js schools/assets/stage-exit.js schools/assets/favicon.svg class/index.html schools/assets/kids-look.js scripts/apply-class-page.py games/sums-in-disguise/index.html games/some-thingies/index.html games/angle-ace/index.html games/free-daily-pizza/index.html games/52dle/index.html games/chart-interrogator/index.html op/index.html essentials/index.html games/scale-factor-scaling/index.html games/dimension-checker/index.html games/suvat/index.html .claude/rules/game-roster.md scripts/apply-site-nav.py scripts/check-start-mount.py
"""Site navigation (contract SITE-NAV, Jon 21 Nov 2026; canon §7.5.8): schools/assets/site-nav.js.

    python scripts/check-site-nav.py --static     # the static rule (check-site.py runs this in its site-wide part)
    python scripts/check-site-nav.py --check      # the rule, then the pages played in Chromium
    python scripts/check-site-nav.py --selftest   # planted faults caught (static and Chromium)
    python scripts/check-site-nav.py --survey     # the logo on every back-link page at 1920x1080: shown or what blocks it
    python scripts/check-site-nav.py --survey-names [--out FILE]   # every roster game at 1280x720, 1366x768 and 1920x1080,
                                                  # start screen and first question: the logo and the name label

THE STATIC RULE (static_faults(); in check-site.py's site-wide part, so it runs on every pull request with no new
always-run line, ALWAYS_BUDGET being full):
  1. every page with an a.back-link, and every games/<slug>/index.html whose slug has a numbered roster row, loads
     site-nav.js exactly once (scripts/apply-site-nav.py writes the tag);
  1a. the game's name (contract GAME-TITLE-IN-PLAY, Jon 24 Nov 2026): on every roster game page the tag carries
     data-game-name, and its decoded value equals the roster's Game column for that slug exactly (roster_names(), the one
     reader of the roster here; apply-site-nav.py imports it); a page outside games/ never carries the attribute; a
     roster Game cell with markup in it is a fault;
  2. HUBS in site-nav.js holds every page outside games/ that links to a game page (a new hub is labelled there);
  3. a page carrying <html data-site-logo="off"> is on LOGO_OPT_OUT below with its reason, and a page that shows its
     own logo (class logo, numblr-logo or header-logo) and loads site-nav.js carries it.

IN CHROMIUM (--check), served by serve-stubbed.py with the network cut:
  - Angle Ace opened from /op/: every a.back-link goes to /op/ and reads "← Back to OP for Secondary"; reloaded, and
    with ?level= changed, the same; opened with no referrer, and from another game, every link exactly as written;
  - Free Daily Pizza (stage-exit) opened from /essentials/: its row link and its HUD home link both go to /essentials/;
  - the class page (contract CLASS-PAGE, Jon 21 Nov 2026): /class/#Willow greets "Welcome, Willow Class!" (text only) and
    every card links /games/<slug>/#kids/Willow; /class/ shows the teachers' line and links #kids; an invalid name
    (#Year6) shows no greeting and links #kids. Each child-look game (scripts/apply-class-page.py's list), opened by
    clicking its card on /class/#Willow, carries #kids/Willow, and its back links and stage-exit HUD home link go to
    /class/#Willow (MaffsNav.backLabel "← Back to the class page"; stage-exit's row link its short form, "← the class
    page"), reloaded too. A site-nav.js that drops the fragment is caught;
  - the logo: shown at 1920x1080 on Angle Ace, links to "/", is named "MaffsGames home", and nothing painted comes
    within its clear space at any scroll position (hit-tested with elementsFromPoint, not site-nav.js's own measure);
    hidden at 390x844 and on a 768x1024 tablet; hidden on Chart Interrogator (its header bar runs the full width); absent on 52-dle;
  - the game's name during play (GAME-TITLE-IN-PLAY): at 1280x720 But It's Only Half the Size! shows no label on its start
    screen (its <h1> shows) and, after Start, the label reading the roster's name; Free Daily Pizza, whose title stays
    during play, shows none at any point; none at 390x844, on a 768x1024 tablet, on Chart Interrogator or on 52-dle.
    Wherever the label shows, an independent hit test (elementsFromPoint over its box, at scroll positions down the
    page) finds nothing the page paints under it, and its colour against the body's background is at least 4.5:1 (a
    light and a dark game). Plants: a label shown while the <h1> is rendered; a label overlapping the game column; a
    data-game-name that differs from the roster; a roster game page without site-nav.js;
  - every distinct label in HUBS on a small phone (SITE-NAV-GUIDE-LABEL, Jon 21 Nov 2026): at 360x640, opened with that
    hub as referrer, Angle Ace's a.back-link and Free Daily Pizza's stage-exit row link each sit on one line (no text
    of the link starts below its first line). A 60-character plant label is caught.
"""
import argparse
import html as htmllib
import importlib.util
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
ROSTER = os.path.join(ROOT, '.claude', 'rules', 'game-roster.md')
NAME_ATTR = re.compile(r'\bdata-game-name="([^"]*)"')
ROSTER_ROW = re.compile(r'^\|\s*\d+\s*\|\s*([^|]*?)\s*\|\s*`([a-z0-9-]+)`\s*\|', re.M)


def roster_names(text=None):
    """{slug: the roster's Game column} for every numbered row of .claude/rules/game-roster.md (a withdrawn game's row is
    numbered "—" and is not one). The one reader of the roster for the name label; apply-site-nav.py imports it."""
    if text is None:
        with open(ROSTER, encoding='utf-8') as f:
            text = f.read()
    out = {}
    for name, slug in ROSTER_ROW.findall(text):
        if slug in out and out[slug] != name:
            raise ValueError('the roster names %s twice: %r and %r' % (slug, out[slug], name))
        out[slug] = name
    return out


def game_slug(rel):
    """The slug of games/<slug>/index.html, else None."""
    m = re.fullmatch(r'games/([^/]+)/index\.html', rel)
    return m.group(1) if m else None


def tag_for(rel, names):
    """The site-nav.js tag a page carries: with the roster's name on a roster game page, plain everywhere else."""
    slug = game_slug(rel)
    if slug in names:
        return '<script src="/schools/assets/site-nav.js" data-game-name="%s"></script>' % htmllib.escape(names[slug], quote=True)
    return TAG


def nav_pages(texts, names):
    """Every page that must load site-nav.js: one with an a.back-link, or a roster game's page."""
    return [r for r, t in sorted(texts.items()) if BACK_LINK.search(t) or game_slug(r) in names]

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
TITLE_GOES = 'games/scale-factor-scaling/index.html'   # But It's Only Half the Size!: its <h1> is in the start screen (light)
TITLE_GOES_DARK = 'games/dimension-checker/index.html'  # the same on a dark page (the check holds its background to dark)
NO_BACK_LINK_GAME = 'games/suvat/index.html'           # a roster game with no a.back-link: it loads site-nav.js by its roster row
PHONE = (360, 640)                             # the small phone every hub label must fit on one line at
CLASS_PAGE = '/class/'                         # the class page (contract CLASS-PAGE): the documented example is #Willow
# The child-look games the class page lists, named here so scripts/ci-deps.py selects this check for each; held equal to
# scripts/apply-class-page.py's list (data/games.json's "kids": true), so a new child-look game is added here too.
CLASS_GAMES = ('games/sums-in-disguise/index.html', 'games/some-thingies/index.html')
CLASS_JS = '''() => { const h = document.getElementById('hello');
  return { hello: h.hidden ? '' : h.textContent, tags: h.children.length, teacher: !document.getElementById('teacher').hidden,
           hrefs: [...document.querySelectorAll('#cards a.card')].map(a => a.getAttribute('href')) }; }'''
CLASS_BACK_JS = '''() => ({ hash: location.hash, label: window.MaffsNav && window.MaffsNav.backLabel,
  back: [...document.querySelectorAll('a.back-link')].map(a => [a.getAttribute('href'), a.textContent.trim(), !!a.closest('.stage-exit-row')]),
  home: [...document.querySelectorAll('.stage-exit-home')].map(a => a.getAttribute('href')) })'''


def _apply_class_page():
    spec = importlib.util.spec_from_file_location('apply_class_page', os.path.join(HERE, 'apply-class-page.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# Does a visible link's text wrap? Its text's line boxes (Range rects): any that starts below the first line has wrapped.
WRAP_JS = r"""(sel) => [...document.querySelectorAll(sel)].filter(a => a.getClientRects().length).map(a => {
  const rg = document.createRange(); rg.selectNodeContents(a);
  const rs = [...rg.getClientRects()].filter(r => r.width > 0 && r.height > 0);
  const first = Math.min(...rs.map(r => r.bottom));
  return {text: a.textContent.trim(), href: a.getAttribute('href'), width: Math.round(a.getBoundingClientRect().width),
          lines: rs.some(r => r.top >= first - 1) ? 2 : 1};
})"""


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


def static_faults(texts=None, js=None, opt_out=None, names=None):
    texts = texts or {r: read(r) for r in pages()}
    opt_out = LOGO_OPT_OUT if opt_out is None else opt_out
    hub = hubs(js)
    out = []
    if not hub:
        out.append('site-nav.js: no HUBS map found')
    try:
        names = roster_names() if names is None else names
    except (OSError, ValueError) as e:
        names = {}
        out.append('the roster cannot be read for the games\' names: %s' % e)
    for slug, name in sorted(names.items()):
        if not name or re.search(r'[<>`*\[\]]|&[a-z#0-9]+;', name):
            out.append('roster: the Game cell for %s holds markup or is empty (%r): the name label needs plain text' % (slug, name))
        if 'games/%s/index.html' % slug not in texts:
            out.append('roster: %s has a row but no games/%s/index.html' % (slug, slug))
    for r in nav_pages(texts, names):
        n = len(LOADS.findall(texts[r]))
        if n != 1:
            out.append('%s: %s and loads site-nav.js %d time(s) (once: python scripts/apply-site-nav.py)'
                       % (r, 'is a roster game\'s page' if game_slug(r) in names else 'has an a.back-link', n))
    for r, t in sorted(texts.items()):
        tags = LOADS.findall(t)
        got = [htmllib.unescape(m.group(1)) for tag in tags for m in [NAME_ATTR.search(tag)] if m]
        slug = game_slug(r)
        if slug in names:
            if len(tags) == 1 and got != [names[slug]]:
                out.append('%s: its site-nav.js tag carries data-game-name %s, not the roster\'s name %r (python scripts/apply-site-nav.py)'
                           % (r, repr(got[0]) if got else 'nothing', names[slug]))
        elif got:
            out.append('%s: carries data-game-name %r but is not a roster game\'s page (the label is for games only)' % (r, got[0]))
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
    print('  site nav (contract SITE-NAV): %d page(s) with an a.back-link, %d hub(s), %d roster game page(s) named; %s'
          % (len(back_link_pages()), len(hubs()), len(roster_names()), 'PASS' if not f else '%d fault(s)' % len(f)))
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


# The name label (GAME-TITLE-IN-PLAY), judged independently of site-nav.js's own measure. Re-measure first (as a click
# would), then: is the logo shown, is the label shown and what does it read, is the page's first <h1> rendered; and where
# the label shows, what the page paints under its box (elementsFromPoint on a grid over it, at scroll positions down the
# page: the label takes no pointer events, so it is never in the list itself), its line count, and its colour's contrast
# against the body's background (the html's where the body has none).
LABEL_JS = r"""async () => {
  if (window.MaffsNav && MaffsNav.place) MaffsNav.place();
  const L = document.querySelector('.maffs-site-logo'), N = document.querySelector('.maffs-site-name');
  const on = (el) => !!el && getComputedStyle(el).display !== 'none';
  const h = document.querySelector('h1');
  const hr = h ? h.getBoundingClientRect() : null;
  const out = { logo: on(L), blocked: L ? L.getAttribute('data-blocked-by') : 'no logo', label: on(N), labels: document.querySelectorAll('.maffs-site-name').length,
                why: N ? N.getAttribute('data-hidden-by') : (window.MaffsNav ? MaffsNav.nameHiddenBy : 'no site-nav.js'),
                free: N && N.getAttribute('data-room-px') !== null ? Number(N.getAttribute('data-room-px')) : null,
                text: N ? N.textContent : null, name: window.MaffsNav ? MaffsNav.gameName : null,
                h1: !!h && h.getClientRects().length > 0 && hr.width > 0 && hr.height > 0 && getComputedStyle(h).visibility !== 'hidden',
                touches: [], lines: 0, contrast: null, link: !!N && (N.tagName === 'A' || !!N.closest('a')), hidden: N ? N.getAttribute('aria-hidden') : null };
  if (!out.label) return out;
  const r = N.getBoundingClientRect(), pad = 8;
  out.lines = Math.round(r.height / (parseFloat(getComputedStyle(N).fontSize) * 1.25));
  out.box = [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)];
  const paints = (el) => {
    const cs = getComputedStyle(el);
    if (/^(IMG|SVG|CANVAS|VIDEO|INPUT|BUTTON|SELECT|TEXTAREA|IFRAME)$/i.test(el.tagName)) return true;
    if (cs.backgroundColor && !/rgba\([^)]*,\s*0\)$|transparent/.test(cs.backgroundColor)) return true;
    if (cs.backgroundImage !== 'none' || cs.boxShadow !== 'none') return true;
    if (['Top','Right','Bottom','Left'].some(s => parseFloat(cs['border'+s+'Width']) > 0 && cs['border'+s+'Style'] !== 'none')) return true;
    return [...el.childNodes].some(n => n.nodeType === 3 && /\S/.test(n.nodeValue));
  };
  const H = Math.max(document.documentElement.scrollHeight, innerHeight);
  scan: for (let y = 0; y <= H; y += Math.max(100, innerHeight / 3)) {
    scrollTo(0, y);
    await new Promise(res => requestAnimationFrame(() => requestAnimationFrame(res)));
    for (let x = r.left - pad; x <= r.right + pad; x += 6) for (let yy = r.top - pad; yy <= r.bottom + pad; yy += 6) {
      if (x < 0 || yy < 0) continue;
      for (const el of document.elementsFromPoint(x, yy)) {
        if (el === L || (L && L.contains(el)) || el === N || el === document.body || el === document.documentElement) continue;
        if (paints(el)) { out.touches.push(el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + ' at scroll ' + Math.round(y)); break scan; }
      }
    }
  }
  scrollTo(0, 0);
  const rgb = (c) => (c.match(/[\d.]+/g) || []).map(Number);
  const lum = (c) => { const [R, G, B] = c.slice(0, 3).map(v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }); return 0.2126 * R + 0.7152 * G + 0.0722 * B; };
  let bg = rgb(getComputedStyle(document.body).backgroundColor);
  if (bg.length > 3 && bg[3] === 0) bg = rgb(getComputedStyle(document.documentElement).backgroundColor);
  if (!bg.length || (bg.length > 3 && bg[3] === 0)) bg = [255, 255, 255];
  const a = lum(rgb(getComputedStyle(N).color)), b = lum(bg);
  out.contrast = Math.round((Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05) * 100) / 100;
  out.bgImage = getComputedStyle(document.body).backgroundImage !== 'none';
  out.bgLum = Math.round(b * 1000) / 1000;
  return out;
}"""

_cs = None


def _check_site():
    """check-site.py, for tier 3's page-side driver (TIER3_INIT: the game's own Start control found by behaviour)."""
    global _cs
    if _cs is None:
        spec = importlib.util.spec_from_file_location('check_site', os.path.join(HERE, 'check-site.py'))
        _cs = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_cs)
    return _cs


_mods = {}


def _module(name):
    if name not in _mods:
        spec = importlib.util.spec_from_file_location(name.replace('-', '_'), os.path.join(HERE, name + '.py'))
        _mods[name] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_mods[name])
    return _mods[name]


def to_first_question(page, slug=None):
    """Press through the game's own start screen to its first question, on a page opened with tier 3's init script. In
    turn, until the game is playing: the controls check-start-mount.py records for a game the shared driver cannot start
    (START_STEPS); the shared driver, as measure-phone-fit.py uses it (the first level or option, then Start); the game's
    own declared start (its maffs-lock-hint, canon 7.6.0). True once the game has reported game_started, or its recorded
    steps were pressed, or its declared 'ready' holds."""
    def started():
        return page.evaluate('window.__mfgStats ? window.__mfgStats().started : 0') > 0
    steps = _module('check-start-mount').START_STEPS.get(slug) if slug else None
    if steps:
        try:
            for step in steps:
                if isinstance(step, tuple):
                    page.fill(step[0], step[1], timeout=3000)
                else:
                    page.locator(step).first.click(timeout=3000)
                page.wait_for_timeout(400)
            page.wait_for_timeout(400)
            return True
        except Exception:
            pass
    picked = False
    for _ in range(5):
        if started():
            break
        if not picked and page.evaluate('window.__mfgProbe().n') >= 2:
            page.evaluate('window.__mfgClickOpt(0)')
            picked = True
        elif page.evaluate('window.__mfgHasStart()'):
            page.evaluate('window.__mfgClickStart()')
        elif page.evaluate('window.__mfgProbe().n') >= 2:
            page.evaluate('window.__mfgClickOpt(0)')
        else:
            break
        page.wait_for_timeout(600)
    if not started():
        try:
            page.evaluate("typeof window.startGame === 'function' && window.startGame()")
        except Exception:
            pass
        page.wait_for_timeout(600)
    if not started() and slug:
        try:
            with open(os.path.join(ROOT, 'games', slug, 'index.html'), encoding='utf-8') as f:
                hint, bad = _module('check-answer-lock').read_hint(f.read())
            if not bad and hint.get('start'):
                page.evaluate(hint['start'])
                page.wait_for_timeout(900)
                if hint.get('ready') and page.evaluate(hint['ready']):
                    return True
        except Exception:
            pass
    return started()


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
            if want('class'):
                apply = _apply_class_page()
                games = [s for s, _ in apply.kids_games()]
                if ['games/%s/index.html' % s for s in games] != list(CLASS_GAMES):
                    faults.append('class page: CLASS_GAMES %s differs from the child-look games in data/games.json, %s' % (list(CLASS_GAMES), games))
                for frag, greet, teacher, suffix in (('#Willow', 'Welcome, Willow Class!', False, '#kids/Willow'),
                                                     ('', '', True, '#kids'), ('#Year6', '', False, '#kids')):
                    ctx = context(viewport={'width': 1280, 'height': 800})
                    page = ctx.new_page()
                    page.goto(base + CLASS_PAGE + frag, wait_until='load')
                    page.wait_for_timeout(150)
                    got = page.evaluate(CLASS_JS)
                    want_hrefs = ['/games/%s/%s' % (s, suffix) for s in games]
                    where = 'class page %s' % (CLASS_PAGE + frag)
                    if got['hello'] != greet or got['tags']:
                        faults.append('%s: the greeting reads %r (%d tags), expected %r' % (where, got['hello'], got['tags'], greet))
                    if got['teacher'] != teacher:
                        faults.append('%s: the teachers\' line is %s' % (where, 'shown' if got['teacher'] else 'hidden'))
                    if got['hrefs'] != want_hrefs:
                        faults.append('%s: the cards link %s, expected %s' % (where, got['hrefs'], want_hrefs))
                    ctx.close()
                for slug in games:
                    ctx = context(viewport={'width': 1280, 'height': 800})
                    page = ctx.new_page()
                    page.goto(base + CLASS_PAGE + '#Willow', wait_until='load')
                    page.wait_for_timeout(150)
                    with page.expect_navigation(wait_until='load'):
                        page.click('a.card[data-game="/games/%s/"]' % slug)
                    page.wait_for_timeout(150)
                    for when in ('opened', 'reloaded'):
                        got = page.evaluate(CLASS_BACK_JS)
                        where = '%s opened from /class/#Willow, %s' % (slug, when)
                        if got['hash'] != '#kids/Willow':
                            faults.append('%s: its address carries %r, not #kids/Willow' % (where, got['hash']))
                        # A header link reads "← Back to the class page"; stage-exit's row keeps its short form (STAGE-EXIT-LABEL).
                        if got['label'] != '← Back to the class page':
                            faults.append('%s: MaffsNav.backLabel is %r, not "← Back to the class page"' % (where, got['label']))
                        if not got['back'] or any(h != '/class/#Willow' or x != ('← the class page' if row else '← Back to the class page')
                                                  for h, x, row in got['back']):
                            faults.append('%s: back links %s, not /class/#Willow reading "← Back to the class page" (the stage-exit '
                                          'row: "← the class page")' % (where, got['back']))
                        if any(h != '/class/#Willow' for h in got['home']):
                            faults.append('%s: stage-exit HUD home links %s, not /class/#Willow' % (where, got['home']))
                        if when == 'opened':
                            page.reload(wait_until='load')
                            page.wait_for_timeout(150)
                    ctx.close()
            if want('phone'):
                js_now = js_swap.get('/schools/assets/site-nav.js') or open(ASSET, encoding='utf-8').read()
                first_hub = {}
                for path, label in hubs(js_now).items():
                    first_hub.setdefault(label, path)
                for label, path in sorted(first_hub.items(), key=lambda x: x[1]):
                    for rel, sel, want_text in ((GAME, 'a.back-link', '← Back to ' + label),
                                                (STAGE_GAME, '.stage-exit-row a.back-link', '← ' + label)):
                        ctx = context(viewport={'width': PHONE[0], 'height': PHONE[1]}, has_touch=True, is_mobile=True)
                        page = ctx.new_page()
                        page.goto(base + url_path(rel), referer=base + path, wait_until='load')
                        page.wait_for_timeout(300)
                        got = page.evaluate(WRAP_JS, sel)
                        where = '%s at %dx%d from %s' % (rel, PHONE[0], PHONE[1], path)
                        if not got or any(g['href'] != path or g['text'] != want_text for g in got):
                            faults.append('phone: %s: links %s, not %s and "%s"' % (where, [(g['href'], g['text']) for g in got],
                                                                                     path, want_text))
                        for g in got:
                            if g['lines'] > 1:
                                faults.append('phone: %s: "%s" wraps onto a second line (%d px wide)' % (where, g['text'], g['width']))
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
            if want('name'):
                names = roster_names()
                cs = _check_site()

                def game(rel, vp, touch=False):
                    ctx = context(viewport={'width': vp[0], 'height': vp[1]}, has_touch=touch, is_mobile=touch)
                    ctx.add_init_script(cs.TIER3_INIT)
                    page = ctx.new_page()
                    page.goto(base + url_path(rel), wait_until='load')
                    page.wait_for_timeout(700)
                    return ctx, page

                def judge(where, res, expect, name=None):
                    if res['labels'] > 1:
                        faults.append('name: %s has %d labels' % (where, res['labels']))
                    if res['label'] and res['h1']:
                        faults.append('name: %s shows the label while the page\'s own <h1> is rendered' % where)
                    if res['label'] and not res['logo']:
                        faults.append('name: %s shows the label without the logo' % where)
                    if expect == 'hidden' and res['label']:
                        faults.append('name: %s shows the label %r, where it must be hidden' % (where, res['text']))
                    if expect == 'shown':
                        if not res['label']:
                            faults.append('name: %s shows no label (%s; logo %s), where the title is gone and the margin fits it'
                                          % (where, res['why'], 'shown' if res['logo'] else 'blocked by %s' % res['blocked']))
                        elif res['text'] != name or res['name'] != name:
                            faults.append('name: %s reads %r (MaffsNav.gameName %r), not the roster\'s %r' % (where, res['text'], res['name'], name))
                    if res['label']:
                        if res['touches']:
                            faults.append('name: on %s the label\'s box (%s) overlaps %s' % (where, res.get('box'), ', '.join(res['touches'])))
                        if res['lines'] > 3:
                            faults.append('name: on %s the label runs to %d lines' % (where, res['lines']))
                        if res['contrast'] is None or res['contrast'] < 4.5:
                            faults.append('name: on %s the label\'s contrast against the body background is %s:1 (4.5:1 at least)' % (where, res['contrast']))
                        if res['link'] or res['hidden'] != 'true':
                            faults.append('name: on %s the label is a link or is not aria-hidden' % where)

                for rel in (TITLE_GOES, TITLE_GOES_DARK):
                    slug = game_slug(rel)
                    ctx, page = game(rel, (1280, 720))
                    judge('%s at 1280x720, start screen' % rel, page.evaluate(LABEL_JS), 'hidden')
                    if not to_first_question(page, slug):
                        faults.append('name: %s could not be started, so its label during play is unchecked' % rel)
                    else:
                        page.wait_for_timeout(700)
                        res = page.evaluate(LABEL_JS)
                        judge('%s at 1280x720, in play' % rel, res, 'shown', names.get(slug))
                        dark = res.get('bgLum') is not None and res['bgLum'] < 0.2
                        if res['label'] and dark != (rel == TITLE_GOES_DARK):
                            faults.append('name: %s is no longer a %s page (background luminance %s): pick another game for this check'
                                          % (rel, 'dark' if rel == TITLE_GOES_DARK else 'light', res['bgLum']))
                    ctx.close()
                ctx, page = game(STAGE_GAME, (1280, 720))
                judge('%s at 1280x720, start screen' % STAGE_GAME, page.evaluate(LABEL_JS), 'hidden')
                if not to_first_question(page, game_slug(STAGE_GAME)):
                    faults.append('name: %s could not be started' % STAGE_GAME)
                page.wait_for_timeout(700)
                res = page.evaluate(LABEL_JS)
                if not res['h1']:
                    faults.append('name: %s no longer keeps its own title during play: pick another game for this check' % STAGE_GAME)
                judge('%s at 1280x720, in play (its own title stays)' % STAGE_GAME, res, 'hidden')
                ctx.close()
                for rel, vp, touch in ((TITLE_GOES, (390, 844), True), (TITLE_GOES, (768, 1024), True), (FULL_WIDTH, (1920, 1080), False),
                                       (OWN_LOGO_GAME, (1920, 1080), False)):
                    ctx, page = game(rel, vp, touch)
                    where = '%s at %dx%d%s' % (rel, vp[0], vp[1], ' (touch)' if touch else '')
                    judge(where + ', start screen', page.evaluate(LABEL_JS), 'hidden')
                    if to_first_question(page, game_slug(rel)):
                        page.wait_for_timeout(700)
                        judge(where + ', in play', page.evaluate(LABEL_JS), 'hidden')
                    elif rel == TITLE_GOES:
                        faults.append('name: %s could not be started' % where)
                    ctx.close()
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return faults


def survey_names(out_path=None, only=None):
    """Every roster game page, at 1280x720, 1366x768 and 1920x1080, on its start screen and on its first question after
    Start: the logo (shown, or what blocks it) and the name label (shown; hidden because the title shows; hidden for no
    room, with the free width). A markdown table and the totals; a report, never a gate."""
    from playwright.sync_api import sync_playwright
    sys.path.insert(0, HERE)
    import bank_common as bc
    cs = _check_site()
    names = roster_names()
    sizes = [(1280, 720), (1366, 768), (1920, 1080)]
    proc, base = bc.start_stub_server()
    rows = []          # (slug, size, phase, result or None, note)

    def cell(res):
        if res is None:
            return 'not reached'
        logo = 'logo' if res['logo'] else ('no logo: %s' % (res['blocked'] or '?')[:40])
        if res['label']:
            lab = 'NAME shown (%d line%s, %s px free)%s' % (res['lines'], '' if res['lines'] == 1 else 's', res['free'],
                                                             ' OVERLAPS ' + res['touches'][0] if res['touches'] else '')
        elif res['h1'] or 'name is on the page' in (res['why'] or ''):
            lab = 'title shows'
        else:
            lab = 'hidden: %s' % (res['why'] or '?')
        return '%s; %s' % (logo, lab)

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            for slug in sorted(names):
                if only and slug not in only:
                    continue
                rel = 'games/%s/index.html' % slug
                ctx = browser.new_context(viewport={'width': sizes[0][0], 'height': sizes[0][1]})
                bc.offline(ctx, base)
                ctx.add_init_script(cs.TIER3_INIT)
                page = ctx.new_page()
                try:
                    page.goto(base + url_path(rel), wait_until='load', timeout=20000)
                    page.wait_for_timeout(600)
                    for phase in ('start', 'play'):
                        reached = True
                        if phase == 'play':
                            page.set_viewport_size({'width': sizes[0][0], 'height': sizes[0][1]})
                            reached = to_first_question(page, slug)
                            page.wait_for_timeout(600)
                        for w, h in sizes:
                            if not reached:
                                rows.append((slug, (w, h), phase, None))
                                continue
                            page.set_viewport_size({'width': w, 'height': h})
                            page.wait_for_timeout(250)
                            rows.append((slug, (w, h), phase, page.evaluate(LABEL_JS)))
                except Exception as e:
                    rows.append((slug, sizes[0], 'error', None))
                    print('  %s: %s' % (slug, str(e).splitlines()[0][:100]))
                ctx.close()
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    by = {}
    for slug, size, phase, res in rows:
        by.setdefault(slug, {})[(size, phase)] = res
    lines = ['| Game | ' + ' | '.join('%dx%d %s' % (w, h, ph) for ph in ('start', 'play') for w, h in sizes) + ' |',
             '|---|' + '---|' * (2 * len(sizes))]
    for slug in sorted(by):
        lines.append('| %s | ' % slug + ' | '.join(cell(by[slug].get(((w, h), ph))) for ph in ('start', 'play') for w, h in sizes) + ' |')
    totals = ['', 'Totals (%d roster game pages):' % len(by), '']
    for w, h in sizes:
        play = [by[s].get(((w, h), 'play')) for s in sorted(by)]
        got = [r for r in play if r is not None]
        logo = sum(1 for r in got if r['logo'])
        loses = [r for r in got if not (r['h1'] or 'name is on the page' in (r['why'] or ''))]
        shown = sum(1 for r in loses if r['label'])
        optout = sum(1 for r in loses if not r['label'] and (r['blocked'] == 'no logo' or 'no logo on this page' in (r['why'] or '')))
        nologo = sum(1 for r in loses if not r['label'] and not r['logo']) - optout
        noroom = sum(1 for r in loses if not r['label'] and r['logo'])
        overlaps = sum(1 for r in got if r['label'] and r['touches'])
        totals.append('- %dx%d, in play: reached %d of %d; logo shown on %d; title still showing on %d; title gone on %d, of which the '
                      'name shows on %d, hidden for no room on %d, hidden because the logo is blocked on %d, hidden because the page '
                      'opts out of the logo on %d; label overlapping anything: %d.'
                      % (w, h, len(got), len(play), logo, len(got) - len(loses), len(loses), shown, noroom, nologo, optout, overlaps))
    text = '\n'.join(lines + totals) + '\n'
    if out_path:
        with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
        print('\n'.join(totals))
        print('wrote %s' % out_path)
    else:
        print(text)
    return 0


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
    dropped = js.replace('      nav.backHref = hub + classFragment(hub);\n', '      nav.backHref = hub;\n', 1)
    got = browser_faults(only={'class'}, js_swap={'/schools/assets/site-nav.js': dropped}) if dropped != js else []
    hit = [f for f in got if 'opened from /class/#Willow' in f and 'not /class/#Willow' in f]
    print('  self-test the class name dropped on the way back %s' % ('caught: ' + hit[0][:100] if hit else '*** MISSED *** %s' % got[:1]))
    fails += [] if hit else ['the class name dropped on the way back passed']
    long_label = 'A' * 60
    planted_js = js.replace("'/op/': 'OP for Secondary',", "'/op/': '%s'," % long_label, 1)
    got = browser_faults(only={'phone'}, js_swap={'/schools/assets/site-nav.js': planted_js})
    hit = [f for f in got if f.startswith('phone:') and long_label in f and 'wraps' in f]
    print('  self-test a 60-character hub label             %s' % ('caught: ' + hit[0][:100] if hit else '*** MISSED *** %s' % got[:1]))
    fails += [] if hit else ['a 60-character hub label passed']
    # The game's name (GAME-TITLE-IN-PLAY). Static: a name that differs from the roster; a roster game's page without the tag.
    names = roster_names()
    slug = game_slug(TITLE_GOES)
    planted = dict(texts)
    planted[TITLE_GOES] = planted[TITLE_GOES].replace(tag_for(TITLE_GOES, names), tag_for(TITLE_GOES, {slug: names[slug] + ' 2'}), 1)
    hit = [f for f in static_faults(planted, js) if f.startswith(TITLE_GOES) and 'not the roster\'s name' in f] if planted[TITLE_GOES] != texts[TITLE_GOES] else []
    print('  self-test a data-game-name unlike the roster   %s' % ('caught: ' + hit[0][:100] if hit else '*** MISSED ***'))
    fails += [] if hit else ['a data-game-name that differs from the roster passed']
    planted = dict(texts)
    planted[NO_BACK_LINK_GAME] = LOADS.sub('', planted[NO_BACK_LINK_GAME], 1)
    hit = [f for f in static_faults(planted, js) if f.startswith(NO_BACK_LINK_GAME) and 'roster game' in f and 'loads site-nav.js 0' in f]
    if BACK_LINK.search(texts[NO_BACK_LINK_GAME]):
        hit = []                                   # stale: the plant needs a roster game with no a.back-link
    print('  self-test a roster game page without site-nav.js %s' % ('caught: ' + hit[0][:100] if hit else '*** MISSED ***'))
    fails += [] if hit else ['a roster game page without site-nav.js passed']
    # In Chromium: a label shown whatever the page's own title does; a label placed over the game column.
    always = js.replace("  function titleShowing() {\n", "  function titleShowing() {\n    return '';\n", 1)
    got = browser_faults(only={'name'}, js_swap={'/schools/assets/site-nav.js': always}) if always != js else []
    hit = [f for f in got if f.startswith('name:') and 'while the page\'s own <h1> is rendered' in f]
    print('  self-test a label shown while the h1 shows     %s' % ('caught: ' + hit[0][:100] if hit else '*** MISSED *** %s' % got[:1]))
    fails += [] if hit else ['a label shown while the <h1> is rendered passed']
    over = js.replace("        label.style.maxWidth = free + 'px';\n", "        label.style.maxWidth = free + 'px';\n        label.style.left = '50%'; label.style.top = '25%';\n", 1)
    got = browser_faults(only={'name'}, js_swap={'/schools/assets/site-nav.js': over}) if over != js else []
    hit = [f for f in got if f.startswith('name:') and 'overlaps' in f]
    print('  self-test a label over the game column         %s' % ('caught: ' + hit[0][:100] if hit else '*** MISSED *** %s' % got[:1]))
    fails += [] if hit else ['a label overlapping the game column passed']
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
    ap.add_argument('--survey-names', action='store_true')
    ap.add_argument('--out', help='with --survey-names: write the table here')
    ap.add_argument('--only', help='with --survey-names: these slugs only (comma separated)')
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    if args.selftest:
        return selftest()
    if args.survey:
        return survey()
    if args.survey_names:
        return survey_names(args.out, set(args.only.split(',')) if args.only else None)
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
