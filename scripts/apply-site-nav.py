#!/usr/bin/env python3
"""Link schools/assets/site-nav.js once on every page that has an a.back-link (contract SITE-NAV, 21 Nov 2026).

    python scripts/apply-site-nav.py            # write
    python scripts/apply-site-nav.py --dry-run  # report what would change

Idempotent: a page that already links it is left alone, so a second run changes nothing. The tag goes just before
stage-exit.js where a page loads that (so MaffsNav is set first; stage-exit.js also reads it lazily), else just before
</head>. Which pages, and the tag itself, come from scripts/check-site-nav.py, which holds every page to them in CI.
Nothing else in a page is touched: not its header, its back link's markup or its layout.
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


def fix(text):
    """The page's text with the tag added once, or unchanged if it already has it."""
    if csn.LOADS.search(text):
        return text
    m = STAGE_EXIT.search(text)
    at = m.start() if m else text.lower().find('</head>')
    if at < 0:
        raise ValueError('no </head> and no stage-exit.js to put the tag before')
    return text[:at] + csn.TAG + '\n' + text[at:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    changed = 0
    for rel in csn.back_link_pages():
        path = os.path.join(csn.ROOT, rel)
        with open(path, encoding='utf-8', newline='') as f:
            text = f.read()
        new = fix(text)
        if new != text:
            changed += 1
            print(('would link ' if args.dry_run else 'linked ') + rel)
            if not args.dry_run:
                with open(path, 'w', encoding='utf-8', newline='') as f:
                    f.write(new)
    print('%d page(s) %s; %d already link site-nav.js' % (changed, 'to change' if args.dry_run else 'changed',
                                                          len(csn.back_link_pages()) - changed))
    return 0


if __name__ == '__main__':
    sys.exit(main())
