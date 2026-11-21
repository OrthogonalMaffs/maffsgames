#!/usr/bin/env python3
"""Draw the class page's card pictures from the games themselves (contract CLASS-PAGE, 21 Nov 2026).

    python scripts/draw-class-cards.py            # write games/<slug>/class-card.svg for each child-look game
    python scripts/draw-class-cards.py --check    # exit 1 if a written file differs from what would be drawn

/class/ shows one card per game with a child look (data/games.json "kids": true), each with a drawing taken from the
game, so the card looks like the game a child is about to open. The drawings are the games' own inline SVG, read from
each page in its kid look in Chromium, with every computed fill and stroke written onto the shapes (the games colour
them from CSS tokens, which an <img> cannot see). Nothing is redrawn by hand:

  sums-in-disguise  the Stage 2 glasses over the Stage 1 moustache (its DISGUISE strings), a disguise kit;
  some-thingies     three thingies from its start-screen crowd (thingy(k) for k = 2, 6, 8: hair, glasses, top hat).

Run it after a game's drawing changes; scripts/apply-meta.py writes the cards that show them.
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT = 'games/%s/class-card.svg'
PROPS = ('fill', 'stroke', 'stroke-width', 'stroke-linecap', 'stroke-linejoin', 'opacity')

# In the page: each shape of `svg` with its computed paint written as attributes, classes and hidden shapes removed.
INLINE_JS = r"""(svg) => {
  const PROPS = %s;
  const walk = (src, dst) => {
    const kids = [...src.children], dkids = [...dst.children];
    kids.forEach((el, i) => {
      const d = dkids[i], cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') { d.setAttribute('data-drop', '1'); return; }
      if (el.tagName !== 'g') for (const p of PROPS) {
        let v = cs.getPropertyValue(p);
        if (p === 'opacity' && v === '1') continue;
        if (p === 'stroke' && v === 'none') continue;
        if (p.startsWith('stroke-') && cs.getPropertyValue('stroke') === 'none') continue;
        d.setAttribute(p, v);
      }
      walk(el, d);
    });
  };
  const copy = svg.cloneNode(true);
  walk(svg, copy);
  copy.querySelectorAll('[data-drop]').forEach(n => n.remove());
  copy.querySelectorAll('*').forEach(n => { n.removeAttribute('class'); n.removeAttribute('style'); });
  return copy.innerHTML;
}""" % (list(PROPS),)


def rgb_hex(text):
    """rgb(r, g, b) -> #rrggbb, so the files read as the games' tokens do."""
    return re.sub(r'rgb\((\d+), (\d+), (\d+)\)', lambda m: '#%02x%02x%02x' % tuple(int(x) for x in m.groups()), text)


def wrap(view, body, label, note):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" aria-label="%s">\n'
            '<!-- %s Written by scripts/draw-class-cards.py (contract CLASS-PAGE); do not edit by hand. -->\n%s\n</svg>\n'
            % (view, label, note, rgb_hex(body)))


def draw():
    """{repo path: svg text}."""
    import bank_common as bc
    from playwright.sync_api import sync_playwright
    sums = open(os.path.join(ROOT, 'games/sums-in-disguise/index.html'), encoding='utf-8').read()
    kit = {k: re.search(r"\b%s: '(<svg[^']*</svg>)'" % k, sums).group(1) for k in ('moustache', 'glasses')}
    out = {}
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch()
            ctx = br.new_context(viewport={'width': 1280, 'height': 800}, reduced_motion='reduce')
            bc.offline(ctx, base)
            page = ctx.new_page()
            page.goto(base + '/games/sums-in-disguise/#kids', wait_until='load')
            parts = []
            for k in ('glasses', 'moustache'):
                page.evaluate('(s) => { const d = document.createElement("div"); d.id = "drawKit"; d.innerHTML = s;'
                              ' document.body.appendChild(d); }', kit[k])
                parts.append(page.evaluate('() => (' + INLINE_JS + ')(document.querySelector("#drawKit svg"))'))
                page.evaluate('() => document.getElementById("drawKit").remove()')
            body = ('<g transform="translate(0 4)">%s</g>\n<g transform="translate(0 58)">%s</g>' % tuple(parts))
            out[OUT % 'sums-in-disguise'] = wrap('0 0 120 104', body, 'Glasses and a moustache',
                                                 'The disguise kit: Sums in Disguise\'s glasses over its moustache.')
            page.goto(base + '/games/some-thingies/#kids', wait_until='load')
            page.wait_for_selector('#crowdStart svg')
            got = page.evaluate('() => [2, 6, 8].map(k => { const s = document.querySelector("#crowdStart svg.k" + k);'
                                ' return s ? (' + INLINE_JS + ')(s) : null; })')
            if None in got:
                raise SystemExit('some-thingies: the start crowd lacks thingy 2, 6 or 8')
            body = '\n'.join('<g transform="translate(%d 0)">%s</g>' % (24 * i, g) for i, g in enumerate(got))
            out[OUT % 'some-thingies'] = wrap('0 0 72 24', body, 'Three thingies',
                                              'Three thingies from Some Thingies\' start screen: spiky hair, glasses, top hat.')
            br.close()
    finally:
        proc.terminate()
        proc.wait()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    bad = 0
    for rel, text in draw().items():
        path = os.path.join(ROOT, rel)
        old = open(path, encoding='utf-8').read() if os.path.exists(path) else None
        if args.check:
            if old != text:
                print('DIFFERS  %s (python scripts/draw-class-cards.py)' % rel)
                bad = 1
            else:
                print('ok       %s' % rel)
        elif old != text:
            with open(path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(text)
            print('wrote    %s' % rel)
        else:
            print('same     %s' % rel)
    return bad


if __name__ == '__main__':
    sys.exit(main())
