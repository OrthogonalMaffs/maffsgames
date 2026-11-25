#!/usr/bin/env python3
"""Link schools/assets/site-nav.js once on every page that has an a.back-link, and on every roster game's page, where the tag
also carries the game's name from the roster (contract SITE-NAV, 21 Nov 2026; GAME-TITLE-IN-PLAY, 24 Nov 2026).

    python scripts/apply-site-nav.py            # write
    python scripts/apply-site-nav.py --dry-run  # report what would change

Idempotent: a second run changes nothing. A page that already links it keeps its tag where it is; on a roster game's page
(games/<slug>/index.html with a numbered roster row) the tag is rewritten to carry data-game-name="<the roster's Game
column>", HTML-escaped, and rewritten again whenever the roster's name changes; anywhere else a tag that carries the
attribute loses it. A new tag goes just before
stage-exit.js where a page loads that (so MaffsNav is set first; stage-exit.js also reads it lazily), else just before
</head>. Which pages, and the tag itself, come from scripts/check-site-nav.py, which holds every page to them in CI.
Nothing else in a page is touched: not its header, its back link's markup or its layout.

The site bar (contract SITE-BAR-PILOT, 25 Nov 2026): on the pages in check-site-nav.py's SITE_BAR_PAGES, and only those, it
also links schools/assets/site-bar.css and writes the bar's slot as the first child of <body> (bar() below).
"""
import argparse
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('check_site_nav', os.path.join(HERE, 'check-site-nav.py'))
csn = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(csn)

STAGE_EXIT = re.compile(r'<script\b[^>]*\bsrc="[^"]*schools/assets/stage-exit\.js"')


def fix(text, tag=None):
    """The page's text with `tag` (default: the plain tag) as its one site-nav.js tag: added if it has none, rewritten
    in place if its tag differs, unchanged otherwise."""
    tag = tag or csn.TAG
    found = csn.LOADS.search(text)
    if found:
        return text if found.group(0) == tag else text[:found.start()] + tag + text[found.end():]
    m = STAGE_EXIT.search(text)
    at = m.start() if m else text.lower().find('</head>')
    if at < 0:
        raise ValueError('no </head> and no stage-exit.js to put the tag before')
    return text[:at] + tag + '\n' + text[at:]


def bar(text):
    """The page's text with the site bar's stylesheet linked (just before its site-nav.js tag) and the slot as the first
    child of <body>; each is added only where the page has none, so a second run changes nothing. For the pages on
    check-site-nav.py's SITE_BAR_PAGES only (contract SITE-BAR-PILOT, 25 Nov 2026). It removes nothing: a page's own back
    links are taken out by hand, and check-site-nav.py fails a page on the list that still has one."""
    if not csn.BAR_CSS_LINK.search(text):
        at = csn.LOADS.search(text).start()
        text = text[:at] + csn.BAR_CSS + '\n' + text[at:]
    if not csn.BAR_ATTR.search(text):
        body = csn.BODY_OPEN.search(text)
        if not body:
            raise ValueError('no <body> to put the site bar\'s slot in')
        text = text[:body.end()] + '\n' + csn.BAR_SLOT + text[body.end():]
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    changed = 0
    names = csn.roster_names()
    texts = {r: csn.read(r) for r in csn.pages()}
    todo = csn.nav_pages(texts, names)
    for rel in todo:
        path = os.path.join(csn.ROOT, rel)
        with open(path, encoding='utf-8', newline='') as f:
            text = f.read()
        named = fix(text, csn.tag_for(rel, names))
        new = bar(named) if rel in csn.SITE_BAR_PAGES else named
        if new != text:
            changed += 1
            had = bool(csn.LOADS.search(text))
            print(('would ' if args.dry_run else '') + ('bar ' if named == text else 'name ' if had else 'link ') + rel)
            if not args.dry_run:
                with open(path, 'w', encoding='utf-8', newline='') as f:
                    f.write(new)
    print('%d page(s) %s; %d already as they should be' % (changed, 'to change' if args.dry_run else 'changed', len(todo) - changed))
    return 0


if __name__ == '__main__':
    sys.exit(main())
