#!/usr/bin/env python3
"""Write every game page's, live escape room's, the hub's and /essentials/'s search title and description, and every card's search keywords, from data/games.json.

    python scripts/apply-meta.py            # write
    python scripts/apply-meta.py --dry-run  # report what would change

Idempotent: a second run changes nothing. The rules, the expected values and the head rewriter
all come from scripts/check-meta.py, which holds every page to them in CI. For each page this
sets <title>, <meta name="description">, og:title and og:description, and twitter:title and
twitter:description where the page has them. On the portal (index.html) and /essentials/ it sets
data-keywords on every game card from games.json's keywords (contract SEARCH-KEYWORDS, 4 Nov 2026), for
on-site search only. Nothing else in the file changes.

Games in check-meta.py's PENDING are skipped. It refuses (exit 1, nothing written) when
games.json breaks a rule (a slug, a length, a duplicate title) or a page has a head tag in a
shape it cannot read, or a card links to something with no keywords in games.json: those need a person,
not a regex (keywords are never invented).
"""
import argparse, importlib.util, pathlib, sys

BASE = pathlib.Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("check_meta", BASE / "scripts" / "check-meta.py")
cm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cm)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    exp, errors = cm.expected(BASE)
    if errors:
        print("\n".join("REFUSED: " + e for e in errors))
        return 1
    writes = {}
    for path, values in exp.items():
        if values["slug"] in cm.PENDING:
            print("skipped  %s (PENDING: %s)" % (path, cm.PENDING[values["slug"]]))
            continue
        p = BASE / path
        old = p.read_text(encoding="utf-8")
        try:
            new = cm.render(old, values)
        except ValueError as e:
            print("REFUSED: %s: %s" % (path, e))
            return 1
        if new != old:
            writes[p] = new
    kw, _ = cm.card_records(cm.load(BASE))
    for path, cls in cm.CARD_PAGES.items():
        p = BASE / path
        old = writes.get(p) or p.read_text(encoding="utf-8")
        try:
            new = cm.render_cards(old, cls, kw)
        except ValueError as e:
            print("REFUSED: %s: %s" % (path, e))
            return 1
        if new != p.read_text(encoding="utf-8"):
            writes[p] = new
    for p, new in writes.items():
        print("%s %s" % ("would write" if a.dry_run else "wrote   ", p.relative_to(BASE)))
        if not a.dry_run:
            p.write_text(new, encoding="utf-8", newline='')
    print("%d of %d pages %s" % (len(writes), len(exp), "would change" if a.dry_run else "changed"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
