#!/usr/bin/env python3
"""Write the class page's game cards (/class/, contract CLASS-PAGE, Jon 21 Nov 2026) from data/games.json.

    python scripts/apply-class-page.py           # write the cards into class/index.html
    python scripts/apply-class-page.py --check   # exit 1 if class/index.html's cards differ from what this writes

The class page lists every game with a child look. The list has one source: the games whose entry in data/games.json
carries "kids": true. data/ is never published (_config.yml; canon §7.7), so the page cannot fetch it: this script
writes the cards in at build time, between the two class-cards comments, and scripts/test-kids-look.py runs --check's
test in CI, so the page cannot drift from the data.

Each card: the game's name (its page's <h1>), its one line (games.json's search_phrase), and a drawing from the game
(ART below: Sums in Disguise's own start picture, and three of Some Thingies' thingies drawn from its thingy() SVG).
A game marked "kids" with no ART entry, or no <h1>, fails: a new child-look game brings its own drawing.
The link is /games/<slug>/#kids as written; the page's script adds the class name (MaffsKids.gameLink). Stdlib only.
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'games.json')
PAGE = os.path.join(ROOT, 'class', 'index.html')
START = '<!-- class-cards: written by scripts/apply-class-page.py from data/games.json ("kids": true); never edit by hand -->'
END = '<!-- /class-cards -->'


def _thingy(k, acc):
    """One thingy, happy, as games/some-thingies/index.html's thingy() draws it (the body, eyes, pupils, the happy mouth)."""
    return ('<svg class="th k%d" viewBox="0 0 24 24" aria-hidden="true"><ellipse class="b" cx="12" cy="14.6" rx="9.2" ry="8"/>'
            '<circle class="e" cx="8.8" cy="12.8" r="2.5"/><circle class="e" cx="15.2" cy="12.8" r="2.5"/>'
            '<circle class="p" cx="9.3" cy="13.3" r="1.15"/><circle class="p" cx="15.7" cy="13.3" r="1.15"/>'
            '<path class="m" d="M9.6 18.6 Q12 21.6 14.4 18.6"/>%s</svg>' % (k, acc))


# The drawing on each card, taken from the game. Some Thingies' three are Jon's three (21 Nov 2026): the oranges' spiky
# hair, the blues' glasses, the purples' top hat, copied from its ACCESSORY map (k2, k6, k8).
ART = {
    'sums-in-disguise': '<img src="/games/sums-in-disguise/assets/start.webp" width="1600" height="873" alt="">',
    'some-thingies': '<span class="crowd">' + ''.join((
        _thingy(2, '<path class="a-hair" d="M4.6 10 L5.6 3.2 L8.2 7.2 L10 1.4 L12 6.4 L14 1.4 L15.8 7.2 L18.4 3.2 L19.4 10 Q12 6.6 4.6 10 Z"/>'),
        _thingy(6, '<circle class="a-lens" cx="8.8" cy="12.8" r="3.3"/><circle class="a-lens" cx="15.2" cy="12.8" r="3.3"/>'
                   '<path class="a-line" d="M12.1 12.4 L11.9 12.4 M5.5 12 L3.6 10.8 M18.5 12 L20.4 10.8"/>'),
        _thingy(8, '<rect class="a-ink" x="7.6" y="0.4" width="8.8" height="6.6" rx="0.8"/><rect class="a-hatband" x="7.6" y="4.6" '
                   'width="8.8" height="1.4"/><rect class="a-ink" x="4.4" y="6.4" width="15.2" height="2" rx="1"/>'),
    )) + '</span>',
}


def kids_games(data=None):
    """[(slug, search_phrase)] for every games.json game marked "kids": true, in the file's order."""
    if data is None:
        with open(DATA, encoding='utf-8') as f:
            data = json.load(f)
    return [(g['slug'], g['search_phrase']) for g in data['games'] if g.get('kids') is True]


def game_name(slug):
    with open(os.path.join(ROOT, 'games', slug, 'index.html'), encoding='utf-8') as f:
        m = re.search(r'<h1>([^<]+)</h1>', f.read())
    if not m:
        raise SystemExit('apply-class-page: games/%s/index.html has no plain <h1> to name its card' % slug)
    return html.unescape(m.group(1)).strip()


def cards(data=None):
    """The block between START and END, as this script writes it."""
    out = [START]
    games = kids_games(data)
    if not games:
        raise SystemExit('apply-class-page: no game in data/games.json carries "kids": true')
    for slug, line in games:
        if slug not in ART:
            raise SystemExit('apply-class-page: %s is marked "kids" but has no drawing in ART' % slug)
        out.append('<a class="card" href="/games/%s/#kids" data-game="/games/%s/">' % (slug, slug))
        out.append('  <span class="art">%s</span>' % ART[slug])
        out.append('  <span class="name">%s</span>' % html.escape(game_name(slug)))
        out.append('  <span class="line">%s</span>' % html.escape(line))
        out.append('</a>')
    out.append(END)
    return '\n'.join(out)


def current(text):
    i, j = text.find(START), text.find(END)
    if i < 0 or j < i:
        return None
    return text[i:j + len(END)]


def faults(text=None, data=None):
    """[fault] when the page's cards are not what this script writes (for --check and scripts/test-kids-look.py)."""
    if text is None:
        with open(PAGE, encoding='utf-8') as f:
            text = f.read()
    now = current(text)
    if now is None:
        return ['class/index.html: the class-cards comments are missing']
    if now != cards(data):
        return ['class/index.html: its cards differ from data/games.json ("kids": true); run python scripts/apply-class-page.py']
    return []


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    with open(PAGE, encoding='utf-8') as f:
        text = f.read()
    if '--check' in sys.argv[1:]:
        f = faults(text)
        for x in f:
            print('FAIL  ' + x)
        print('FAILED' if f else 'PASS: class/index.html lists %d child-look game(s)' % len(kids_games()))
        return 1 if f else 0
    now = current(text)
    if now is None:
        raise SystemExit('apply-class-page: class/index.html has no class-cards comments to write between')
    new = text.replace(now, cards(), 1)
    if new != text:
        with open(PAGE, 'w', encoding='utf-8', newline='') as f:
            f.write(new)
        print('class/index.html: cards written (%d game(s))' % len(kids_games()))
    else:
        print('class/index.html: cards already current')
    return 0


if __name__ == '__main__':
    sys.exit(main())
