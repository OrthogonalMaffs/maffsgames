#!/usr/bin/env python3
# ci-line: Canon rooms (canon §11.1's Live rows are exactly the hub's room cards, no withdrawn row is on the hub, every row has a known state; planted faults caught) | --selftest && --check
# ci-deps: docs/canon.md escape-rooms/index.html scripts/check-canon-rooms.py
"""Canon §11.1 is the only list of escape rooms; the hub shows the live ones (contract CANON-LIVE-COUNTS, Jon, 5 Nov 2026).

    python scripts/check-canon-rooms.py --check       # the repo as it is
    python scripts/check-canon-rooms.py --selftest    # planted faults are caught
    python scripts/check-canon-rooms.py --selftest --check

Canon used to type "Thirteen rooms live" beside its table while the hub showed 14 (canon §7.5.3: a site fact is never
hand-typed beside its data). The count is gone; this keeps the one list canon owns equal to the page that shows it.
It fails when:
  - a room card on the hub (`<a class="room-card" href="<slug>/">` in escape-rooms/index.html) has no Live row in §11.1;
  - a Live row in §11.1 has no card on the hub;
  - a Withdrawn row's slug has a card on the hub;
  - a row's State is neither Live nor Withdrawn, a slug appears twice, or §11.1 or its table cannot be found.
Links on the hub that are not room cards (The Perfect Prank's note, canon §4.2) are not rooms and are not read.
"""
import argparse
import pathlib
import re
import sys

BASE = pathlib.Path(__file__).resolve().parent.parent
CANON = "docs/canon.md"
HUB = "escape-rooms/index.html"

SECTION = re.compile(r"^## 11\.1 .*?$(.*?)(?=^## |\Z)", re.M | re.S)
ROW = re.compile(r"^\|[^|\n]*\|\s*`([a-z0-9-]+)`\s*\|(?:[^|\n]*\|){2}\s*([^|\n]*?)\s*\|\s*$", re.M)
CARD = re.compile(r"""<a\b[^>]*\bclass=["'][^"']*\broom-card\b[^"']*["'][^>]*\bhref=["']([a-z0-9-]+)/?["']"""
                  r"""|<a\b[^>]*\bhref=["']([a-z0-9-]+)/?["'][^>]*\bclass=["'][^"']*\broom-card\b""", re.I)


def canon_rows(text):
    """[(slug, state)] from §11.1's table, state 'live', 'withdrawn' or the raw text; None if §11.1 is missing."""
    m = SECTION.search(text)
    if not m:
        return None
    rows = []
    for slug, state in ROW.findall(m.group(1)):
        bare = state.replace("*", "").strip().lower()
        rows.append((slug, "live" if bare.startswith("live") else "withdrawn" if bare.startswith("withdrawn") else state))
    return rows


def hub_cards(html):
    return [a or b for a, b in CARD.findall(html)]


def problems(canon_text, hub_html):
    rows = canon_rows(canon_text)
    if rows is None:
        return ["%s: no '## 11.1' section" % CANON]
    if not rows:
        return ["%s §11.1: no table rows with a `slug` found" % CANON]
    out = []
    slugs = [s for s, _ in rows]
    for s in sorted({s for s in slugs if slugs.count(s) > 1}):
        out.append("%s §11.1: `%s` has more than one row" % (CANON, s))
    for s, st in rows:
        if st not in ("live", "withdrawn"):
            out.append("%s §11.1: `%s` has State %r, neither Live nor Withdrawn" % (CANON, s, st))
    live = {s for s, st in rows if st == "live"}
    withdrawn = {s for s, st in rows if st == "withdrawn"}
    cards = hub_cards(hub_html)
    for s in sorted({c for c in cards if cards.count(c) > 1}):
        out.append("%s: `%s` has more than one room card" % (HUB, s))
    cards = set(cards)
    for s in sorted(cards - live - withdrawn):
        out.append("%s: room card `%s` has no row in %s §11.1: add its row" % (HUB, s, CANON))
    for s in sorted(live - cards):
        out.append("%s §11.1: `%s` is marked Live but has no room card on %s" % (CANON, s, HUB))
    for s in sorted(withdrawn & cards):
        out.append("%s §11.1: `%s` is Withdrawn but has a room card on %s" % (CANON, s, HUB))
    return out


def read(root):
    return ((root / CANON).read_text(encoding="utf-8"), (root / HUB).read_text(encoding="utf-8"))


def selftest():
    """Plant each fault in a copy of the real files' text; every plant must be caught, and the real files must pass
    or fail exactly as --check says (the plants are judged against the real text, so a broken parser cannot pass)."""
    canon, hub = read(BASE)
    rows = canon_rows(canon) or []
    live = [s for s, st in rows if st == "live"]
    withdrawn = [s for s, st in rows if st == "withdrawn"]
    if not live or not withdrawn:
        return ["selftest: §11.1 needs at least one Live and one Withdrawn row to plant against (found %d, %d)"
                % (len(live), len(withdrawn))], 0
    victim = live[-1]
    row_of = re.compile(r"^\|[^|\n]*\|\s*`%s`\s*\|.*\n" % re.escape(victim), re.M)
    extra = "| Planted Room | `planted-room` | GCSE | — | **Live** (01/01/2026) |\n"
    first_row = row_of.search(canon)
    plants = [
        ("a Live room's row missing from §11.1", row_of.sub("", canon, count=1), hub, "has no row"),
        ("an extra Live row with no hub card", canon[:first_row.start()] + extra + canon[first_row.start():], hub,
         "`planted-room` is marked Live but has no room card"),
        ("a Withdrawn room with a hub card", canon,
         hub.replace("</body>", '<a class="room-card" href="%s/">x</a></body>' % withdrawn[0], 1),
         "is Withdrawn but has a room card"),
        ("a hub card dropped", canon, re.sub(r'<a\b[^>]*class="room-card"[^>]*href="%s/"' % re.escape(victim),
                                             '<a class="gone" href="%s/"' % victim, hub, count=1),
         "is marked Live but has no room card"),
        ("a row with an unknown State", row_of.sub(lambda m: m.group(0).replace("**Live**", "**Soon**"), canon, count=1),
         hub, "neither Live nor Withdrawn"),
        ("§11.1 missing", canon.replace("## 11.1 ", "## 11.9 ", 1), hub, "no '## 11.1' section"),
    ]
    bad = []
    for name, c, h, want in plants:
        got = problems(c, h)
        if not any(want in g for g in got):
            bad.append("selftest: plant not caught: %s (got %s)" % (name, got or "no problems"))
        else:
            print("  caught  %-40s %s" % (name, [g for g in got if want in g][0]))
    return bad, len(plants)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="check the repo (the default when --selftest is not given)")
    ap.add_argument("--selftest", action="store_true", help="plant faults and require each to be caught")
    a = ap.parse_args()
    failed = False
    if a.selftest:
        bad, n = selftest()
        for b in bad:
            print("FAIL  " + b)
        print("selftest: %s (%d plants)" % ("FAIL" if bad else "PASS", n))
        failed |= bool(bad)
    if a.check or not a.selftest:
        canon, hub = read(BASE)
        got = problems(canon, hub)
        rows = canon_rows(canon) or []
        for g in got:
            print("FAIL  " + g)
        print("check: %s (§11.1: %d Live, %d Withdrawn; hub: %d room cards)" % (
            "FAIL" if got else "PASS", sum(st == "live" for _, st in rows), sum(st == "withdrawn" for _, st in rows),
            len(set(hub_cards(hub)))))
        failed |= bool(got)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
