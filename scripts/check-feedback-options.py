"""Check that the feedback page can still build its game menu.

feedback/index.html builds its "Which game or escape room?" menu at page load
from the live portal and escape-rooms hub, so the list itself cannot drift. What
can break is the markup it reads. Run after any change to index.html,
escape-rooms/index.html or the feedback page. It fails if:

  * the portal has no a.game-card with an href and a .card-title inside it,
    or any game card has lost its .card-title (that game would vanish from the
    menu without anyone noticing)
  * the escape-rooms hub has no a.room-card with an href and an <h3> inside it,
    or any room card has lost its <h3>
  * the feedback page's script no longer references those selectors

Paths can be overridden for testing against a temporary copy:
    python scripts/check-feedback-options.py --portal tmp/index.html
"""
import argparse, pathlib, sys
from html.parser import HTMLParser

BASE = pathlib.Path(__file__).resolve().parent.parent


class Cards(HTMLParser):
    """Collect <a> elements carrying card_class, noting whether each contains
    an element matching the title test."""

    def __init__(self, card_class, is_title):
        super().__init__()
        self.card_class, self.is_title = card_class, is_title
        self.cards, self.current = [], None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and self.card_class in (a.get("class") or "").split():
            self.current = {"href": a.get("href"), "title": False}
            self.cards.append(self.current)
        elif self.current is not None and self.is_title(tag, a):
            self.current["title"] = True

    def handle_endtag(self, tag):
        if tag == "a":
            self.current = None


def cards(path, card_class, is_title):
    p = Cards(card_class, is_title)
    p.feed(path.read_text(encoding="utf-8"))
    return p.cards


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--portal", default=BASE / "index.html", type=pathlib.Path)
    ap.add_argument("--hub", default=BASE / "escape-rooms" / "index.html", type=pathlib.Path)
    ap.add_argument("--feedback", default=BASE / "feedback" / "index.html", type=pathlib.Path)
    args = ap.parse_args()

    problems = []

    games = cards(args.portal, "game-card",
                  lambda t, a: "card-title" in (a.get("class") or "").split())
    good_games = [c for c in games if c["href"] and c["title"]]
    if not good_games:
        problems.append(f"{args.portal}: no a.game-card with an href and a .card-title")
    for c in games:
        if c not in good_games:
            problems.append(f"{args.portal}: game card {c['href']!r} has no href or no .card-title")
    slugs = {c["href"].split("?")[0] for c in good_games}

    rooms = cards(args.hub, "room-card", lambda t, a: t == "h3")
    good_rooms = [c for c in rooms if c["href"] and c["title"]]
    if not good_rooms:
        problems.append(f"{args.hub}: no a.room-card with an href and an <h3>")
    for c in rooms:
        if c not in good_rooms:
            problems.append(f"{args.hub}: room card {c['href']!r} has no href or no <h3>")

    page = args.feedback.read_text(encoding="utf-8")
    for needle in ["'.game-card'", "'.card-title'", "'.room-card'", "'h3'"]:
        if needle not in page:
            problems.append(f"{args.feedback}: script no longer references {needle}")

    print(f"portal: {len(games)} game cards, {len(slugs)} unique games; "
          f"hub: {len(good_rooms)} escape rooms")
    if problems:
        print("\nFAIL")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("feedback menu selectors OK")


if __name__ == "__main__":
    main()
