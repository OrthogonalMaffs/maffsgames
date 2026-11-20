#!/usr/bin/env python3
"""MaffsCards: the printable deck, from data/maffscards.json, rendered in Chromium (contract MAFFSCARDS-DATA, 19 Nov 2026).

Reads every value from data/maffscards.json and computes none (gen.py writes it; check.py checks it). Writes
printables/maffscards.pdf, the free download on /printables/ (Jon's ruling, 18 Nov 2026: the PDF is free, so it is
committed and published, unlike the loop cards and the escape-room packs).

The PDF: A4 portrait, nine playing cards (63 x 88 mm) a page, edge to edge, with dashed cut lines.
  pages 1-4  the rules card, the "how to read your card" card, then the 32 main cards;
  pages 5-6  the 16 extra cards;
  pages 7-8  the teacher sheet: how each category works and five conversation starters, then every value.
Each card: the number large; its nickname (Outfit Bold, teal, at most two lines); the number as dots in its squarest
rectangle; the six values, "lowest wins" on distance; the superpower badges inside the card (shrunk to no less than
4.4 pt, then wrapped). Black on white wherever it matters: the teal nickname is bold text that reads in grey, and
nothing is told by colour alone. Outfit and JetBrains Mono, served from the repo's pinned copies (scripts/fonts/),
nothing else loaded.

Before writing, the build measures every card in Chromium and refuses (BUILD FAILED, no PDF) if: a font did not load;
a nickname takes a third line; a badge row needs less than 4.4 pt even wrapped; anything overflows its card or the
teacher pages; a page holds more than nine cards; or the registered trade mark the deck must never use appears.

    python -X utf8 tools/maffscards/build_pdf.py [--out PATH] [--proofs DIR]

--proofs DIR also writes a PNG of every page (2x), for looking at; never committed.
"""
import argparse
import html
import json
import math
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
DATA = ROOT / "data" / "maffscards.json"
OUT = ROOT / "printables" / "maffscards.pdf"
FONTS = ("https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800"
         "&family=JetBrains+Mono:wght@400;500;700&display=swap")      # a query the repo pins (scripts/fonts/google)
BADGE_START, BADGE_MIN = 6.5, 4.4                                         # pt
TRADE_MARK = "top" + " " + "trumps"

esc = html.escape


class BuildError(Exception):
    pass


# ------------------------------------------------------------------------------------------------ the cards
def squarest(n):
    """(rows, cols): rows x cols = n, rows <= cols, as close to a square as n allows (a prime makes one line)."""
    rows = max(d for d in range(1, math.isqrt(n) + 1) if n % d == 0)
    return rows, n // rows


def dots_svg(n, w=54.0, h=15.0):
    rows, cols = squarest(n)
    pitch = min(w / cols, h / rows, 3.2)
    r = pitch * 0.36
    gw, gh = pitch * cols, pitch * rows
    x0, y0 = (w - gw) / 2 + pitch / 2, (h - gh) / 2 + pitch / 2
    circles = "".join('<circle cx="%.3f" cy="%.3f" r="%.3f"/>' % (x0 + c * pitch, y0 + rr * pitch, r)
                      for rr in range(rows) for c in range(cols))
    label = "%d dots: %d by %d" % (n, rows, cols) if rows > 1 else "%d dots in a line" % n
    return ('<svg class="mc-dots" viewBox="0 0 %s %s" width="%smm" height="%smm" role="img" aria-label="%s">%s</svg>'
            % (w, h, w, h, label, circles))


def value_text(card, key):
    v = card[key]
    if key == "lpf":
        return "none" if v == 0 else str(v)
    if key == "roman":
        return str(len(v))
    if key == "powers":
        return str(len(v))
    return str(v)


def card_html(card, cats):
    rows = []
    for c in cats:
        key = c["key"]
        label = esc(c["label"])
        if key == "roman":
            label += ' <span class="mc-roman">%s</span>' % esc(card["roman"])
        if c["winner"] == "lowest":
            label += ' <span class="mc-low">lowest wins</span>'
        rows.append('<div class="mc-row" data-key="%s"><span class="mc-lab">%s</span><span class="mc-val">%s</span></div>'
                    % (key, label, esc(value_text(card, key))))
        if key == "powers":
            badges = "".join('<span class="mc-badge">%s</span>' % esc(p) for p in card["powers"])
            rows.append('<div class="mc-badges">%s</div>' % (badges or '<span class="mc-nobadge">no superpowers</span>'))
    return ("""<article class="mc-card" data-n="{n}" data-deck="{deck}"><div class="mc-frame">
<div class="mc-top"><span class="mc-num">{n}</span><span class="mc-deck">{decklabel}</span></div>
<div class="mc-nick">{nick}</div>
<div class="mc-dotbox">{dots}</div>
<div class="mc-stats">{rows}</div>
<div class="mc-foot"><span>MaffsCards</span><span>maffsgames.co.uk</span></div>
</div></article>""".format(n=card["n"], deck=card["deck"], decklabel="Main deck" if card["deck"] == "main" else "Extra deck",
                           nick=esc(card["nickname"]), dots=dots_svg(card["n"]), rows="".join(rows)))


RULES = """<article class="mc-card mc-info" data-info="rules"><div class="mc-frame">
<div class="mc-ihead">How to play</div>
<ol class="mc-steps">
<li>2 to 6 players. Shuffle and deal all the cards face down. Hold your pile face down.</li>
<li>Everyone turns over their top card and looks at it, nobody else's.</li>
<li>The player left of the dealer picks one of the six categories and reads out their value.</li>
<li>Everyone reads theirs. The highest value wins, except Distance to nearest square: the lowest wins.</li>
<li>The winner takes every card played and puts them at the bottom of their pile, then picks the next category.</li>
<li>A tie: the cards stay in the middle and the winner of the next round takes them too.</li>
<li>Run out of cards and you are out. The last player holding cards wins.</li>
</ol>
<p class="mc-itip">Short on time? Play for 10 minutes; most cards wins.</p>
<div class="mc-foot"><span>MaffsCards</span><span>maffsgames.co.uk</span></div>
</div></article>"""

READ = """<article class="mc-card mc-info" data-info="read"><div class="mc-frame">
<div class="mc-ihead">How to read your card</div>
<dl class="mc-read">
<dt>The dots</dt><dd>the number as a rectangle, as square as it can be. A prime can only make one line.</dd>
<dt>Sum of factors</dt><dd>add every number that divides it, 1 and itself included.</dd>
<dt>Largest prime factor</dt><dd>the biggest prime that divides it. 1 has none.</dd>
<dt>Roman numeral length</dt><dd>how many letters its Roman numeral has.</dd>
<dt>Distance to nearest square</dt><dd>how far to the closest of 0, 1, 4, 9, &hellip;, 100. Lowest wins.</dd>
<dt>Superpowers</dt><dd>one each for prime, square, cube, triangular, Fibonacci and palindrome.</dd>
<dt>Pi&rsquo;s first 1,000 digits</dt><dd>how many times its digits appear in a row after the point.</dd>
</dl>
<div class="mc-foot"><span>MaffsCards</span><span>maffsgames.co.uk</span></div>
</div></article>"""


def teacher_html(data):
    cards = data["cards"]
    trs = []
    for c in cards:
        trs.append("<tr><td class=\"t-n\">%d</td><td>%s</td><td>%d</td><td>%s</td><td>%s (%d)</td><td>%d</td>"
                   "<td>%s</td><td>%d</td></tr>"
                   % (c["n"], "Main" if c["deck"] == "main" else "Extra", c["sof"], value_text(c, "lpf"),
                      esc(c["roman"]), len(c["roman"]), c["dist"],
                      ("%d: %s" % (len(c["powers"]), ", ".join(c["powers"]))) if c["powers"] else "0",
                      c["pi"]))
    page1 = """<section class="mc-sheet" data-sheet="1">
<h1>MaffsCards: teacher sheet</h1>
<p class="t-lead">A compare-and-win card game for the numbers 1 to 100. Print pages 1 to 4 for the main deck of 32
(with a rules card and a "how to read your card" card); pages 5 and 6 add 16 extra cards. Cut along the dashed lines.
Every value was computed by a program and checked by a second, independent one.</p>
<h2>How each category works</h2>
<dl class="t-cats">
<dt>Sum of factors (highest wins)</dt>
<dd>Add every whole number that divides it exactly, 1 and the number itself included. 28: 1 + 2 + 4 + 7 + 14 + 28 = 56.</dd>
<dt>Largest prime factor (highest wins)</dt>
<dd>Write the number as a product of primes and take the biggest. 60 = 2 &times; 2 &times; 3 &times; 5, so 5. A prime is its
own largest prime factor. 1 has no prime factors, so it scores 0 (shown "none").</dd>
<dt>Roman numeral length (highest wins)</dt>
<dd>The letters in its standard Roman numeral, using IV, IX, XL and XC. 88 = LXXXVIII, 8 letters, the longest in the deck; 100 = C, just 1.</dd>
<dt>Distance to nearest square (lowest wins)</dt>
<dd>How far it is from the closest square number of 0, 1, 4, 9, &hellip;, 100. 17 is 1 from 16; 89 is 8 from 81. A square scores 0, the best possible.</dd>
<dt>Superpowers (highest wins)</dt>
<dd>One point each for being prime, square, cube, triangular, Fibonacci or a palindrome. 1 counts as square, cube,
triangular and Fibonacci (and a palindrome, as every single digit is), but not prime.</dd>
<dt>Times in pi&rsquo;s first 1,000 digits (highest wins)</dt>
<dd>How many times the number&rsquo;s digits appear in a row among the first 1,000 decimals of pi after the point (the
3 before the point is not counted). Overlaps count: in 333, 33 appears twice.</dd>
</dl>
<h2>Five conversation starters</h2>
<ol class="t-talk">
<li><b>Why does a single digit beat every two-digit number on pi?</b> Each digit appears about one time in 10, so about
100 times in 1,000 digits (here 93 to 116). A particular pair of digits is about one in 100, so about 10 times (here 5
to 18), and 100 appears just once.</li>
<li><b>Why only the first 1,000 digits?</b> Pi&rsquo;s digits never end, so we need a fixed stretch to count in. It is
widely believed that pi is <i>normal</i>, every string of digits turning up as often as every other in the long run,
but nobody has proved it. We do not even know for certain that every digit keeps appearing forever.</li>
<li><b>Why is 1 not prime?</b> A prime has exactly two factors, 1 and itself; 1 has only one. If 1 were prime, numbers
would stop having one prime factorisation: 6 = 2 &times; 3 = 1 &times; 2 &times; 3 = 1 &times; 1 &times; 2 &times; 3 &hellip;</li>
<li><b>28 is perfect.</b> Its factors other than itself, 1 + 2 + 4 + 7 + 14, add up to 28 exactly, so its sum of
factors is 56, double the number. The only other perfect number below 100 is 6. Can students find why 6 works?</li>
<li><b>Why do primes lose on sum of factors?</b> A prime p has only two factors, 1 and p, so its sum is p + 1, the
least any number above 1 can have. 89 scores 90; 60, with twelve factors, scores 168.</li>
</ol>
<p class="t-foot">MaffsCards by MaffsGames, maffsgames.co.uk. Free to print and use in class (CC BY-ND).</p>
</section>"""
    page2 = """<section class="mc-sheet" data-sheet="2">
<h2>Every card&rsquo;s values</h2>
<table class="t-vals"><thead><tr><th>Number</th><th>Deck</th><th>Sum of factors</th><th>Largest prime factor</th>
<th>Roman numeral (length)</th><th>Distance to nearest square</th><th>Superpowers</th><th>Pi, first 1,000 digits</th></tr></thead>
<tbody>%s</tbody></table>
<p class="t-foot">Highest wins in every category except distance to nearest square, where lowest wins.</p>
</section>""" % "".join(trs)
    return page1 + page2


CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: #fff; color: #000; font-family: 'Outfit', sans-serif; }
.mc-page { width: 210mm; height: 297mm; position: relative; page-break-after: always; overflow: hidden; }
.mc-cut { position: absolute; top: 9mm; left: 0; right: 0; text-align: center; font-size: 8pt; color: #333; }
.mc-grid { position: absolute; top: 16.5mm; left: 10.5mm; width: 189mm; height: 264mm;
  display: grid; grid-template-columns: repeat(3, 63mm); grid-template-rows: repeat(3, 88mm); }
.mc-card { width: 63mm; height: 88mm; outline: 0.25mm dashed #000; outline-offset: -0.125mm; padding: 2mm; overflow: hidden; }
.mc-frame { width: 59mm; height: 84mm; border: 0.35mm solid #000; border-radius: 3mm; padding: 2.2mm 2.4mm 1.8mm;
  display: flex; flex-direction: column; overflow: hidden; }
.mc-top { display: flex; justify-content: space-between; align-items: flex-start; flex: none; }
.mc-num { font-weight: 800; font-size: 34pt; line-height: 0.95; letter-spacing: -0.02em; }
.mc-deck { font-family: 'JetBrains Mono', monospace; font-size: 6pt; font-weight: 500; border: 0.25mm solid #000;
  border-radius: 1mm; padding: 0.3mm 1mm; margin-top: 0.6mm; }
.mc-nick { flex: none; font-weight: 700; color: #0d9488; font-size: 9.5pt; line-height: 1.15; height: 2.3em;
  margin-top: 1.2mm; overflow-wrap: normal; }
.mc-dotbox { flex: none; height: 15mm; margin: 1.2mm 0 1mm; display: flex; justify-content: center; align-items: center; }
.mc-dots { display: block; fill: #000; }
.mc-stats { flex: 1 1 auto; display: flex; flex-direction: column; justify-content: flex-start; }
.mc-row { display: flex; justify-content: space-between; align-items: baseline; gap: 1.5mm;
  border-top: 0.2mm solid #000; padding: 0.55mm 0 0.45mm; }
.mc-lab { font-size: 7pt; font-weight: 500; line-height: 1.15; }
.mc-roman { font-family: 'JetBrains Mono', monospace; font-size: 6pt; }
.mc-low { font-weight: 700; font-size: 6pt; border: 0.2mm solid #000; border-radius: 0.8mm; padding: 0 0.6mm;
  white-space: nowrap; }
.mc-val { font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 9pt; line-height: 1.1; white-space: nowrap; }
.mc-badges { display: flex; flex-wrap: nowrap; gap: 0.8mm; padding: 0 0 0.7mm; font-size: 6.5pt; }
.mc-badges.mc-wrap { flex-wrap: wrap; row-gap: 0.5mm; }
.mc-badge { border: 0.25mm solid #000; border-radius: 99px; padding: 0.1mm 1.1mm; font-weight: 600; line-height: 1.2;
  white-space: nowrap; }
.mc-nobadge { font-size: 6pt; font-style: italic; line-height: 1.2; }
.mc-foot { flex: none; margin-top: auto; display: flex; justify-content: space-between; font-size: 5.5pt;
  font-family: 'JetBrains Mono', monospace; color: #333; padding-top: 0.6mm; border-top: 0.2mm solid #000; }
.mc-ihead { font-weight: 800; font-size: 13pt; line-height: 1.1; color: #0d9488; margin-bottom: 1.5mm; }
.mc-steps { padding-left: 4mm; font-size: 7.2pt; line-height: 1.25; }
.mc-steps li { margin-bottom: 0.9mm; }
.mc-itip { font-size: 7pt; font-weight: 600; margin-top: 0.6mm; }
.mc-read { font-size: 6.6pt; line-height: 1.2; }
.mc-read dt { font-weight: 700; margin-top: 0.8mm; }
.mc-read dd { margin-left: 0; }
.mc-sheet { width: 210mm; height: 297mm; padding: 14mm 15mm 12mm; page-break-after: always; overflow: hidden; position: relative; }
.mc-sheet h1 { font-size: 20pt; font-weight: 800; margin-bottom: 2mm; }
.mc-sheet h2 { font-size: 13pt; font-weight: 700; margin: 4mm 0 1.5mm; padding-bottom: 0.8mm; border-bottom: 0.5mm solid #000; }
.t-lead { font-size: 10pt; line-height: 1.35; }
.t-cats { font-size: 9.6pt; line-height: 1.32; }
.t-cats dt { font-weight: 700; margin-top: 1.6mm; }
.t-cats dd { margin-left: 0; }
.t-talk { font-size: 9.6pt; line-height: 1.32; padding-left: 5mm; }
.t-talk li { margin-bottom: 1.5mm; }
.t-foot { font-size: 8.5pt; margin-top: 3mm; color: #333; }
.t-vals { width: 100%; border-collapse: collapse; font-size: 8pt; }
.t-vals th { font-weight: 700; text-align: left; vertical-align: bottom; border-bottom: 0.4mm solid #000; padding: 0.6mm 1mm; line-height: 1.15; }
.t-vals td { font-family: 'JetBrains Mono', monospace; padding: 0.35mm 1mm; border-bottom: 0.15mm solid #888; line-height: 1.2; }
.t-vals td.t-n { font-weight: 700; }
"""

FIT_JS = """async ([start, min]) => {
  await document.fonts.ready;
  const pt = px => px * 72 / 96;
  const out = {badges: [], nick: [], overflow: [], loaded: [...document.fonts].filter(f => f.status === 'loaded')
               .map(f => f.family.replace(/["']/g, ''))};
  for (const box of document.querySelectorAll('.mc-badges')) {
    const n = box.closest('.mc-card').dataset.n;
    let s = start, wrapped = false;
    box.style.fontSize = s + 'pt';
    while (box.scrollWidth > box.clientWidth + 0.5 && s - 0.1 >= min - 1e-9) {
      s = Math.round((s - 0.1) * 10) / 10;
      box.style.fontSize = s + 'pt';
    }
    if (box.scrollWidth > box.clientWidth + 0.5) { box.classList.add('mc-wrap'); wrapped = true; }
    const fits = box.scrollWidth <= box.clientWidth + 0.5;
    out.badges.push({n, size: s, wrapped, fits});
  }
  for (const el of document.querySelectorAll('.mc-nick')) {
    const lh = parseFloat(getComputedStyle(el).lineHeight);
    el.style.height = 'auto';
    const lines = Math.round(el.getBoundingClientRect().height / lh);
    el.style.height = '';
    out.nick.push({n: el.closest('.mc-card').dataset.n, lines});
  }
  for (const el of document.querySelectorAll('.mc-frame, .mc-sheet')) {
    if (el.scrollHeight > el.clientHeight + 0.5 || el.scrollWidth > el.clientWidth + 0.5) {
      const c = el.closest('[data-n],[data-info],[data-sheet]');
      out.overflow.push((c.dataset.n || c.dataset.info || ('teacher sheet ' + c.dataset.sheet)) + ': ' +
                        (el.scrollHeight - el.clientHeight) + 'px tall, ' + (el.scrollWidth - el.clientWidth) + 'px wide');
    }
  }
  out.pages = [...document.querySelectorAll('.mc-grid')].map(g => g.children.length);
  return out;
}"""


def page_of(cells):
    return ('<div class="mc-page"><div class="mc-cut">Cut along the dashed lines.</div><div class="mc-grid">%s</div></div>'
            % "".join(cells))


def document(data):
    cats = data["categories"]
    main = [card_html(c, cats) for c in data["cards"] if c["deck"] == "main"]
    extra = [card_html(c, cats) for c in data["cards"] if c["deck"] == "extra"]
    if len(main) != 32 or len(extra) != 16:
        raise BuildError("data/maffscards.json does not hold 32 main and 16 extra cards")
    first = [RULES, READ] + main
    pages = [page_of(first[i:i + 9]) for i in range(0, len(first), 9)]
    pages += [page_of(extra[i:i + 9]) for i in range(0, len(extra), 9)]
    return ("<!DOCTYPE html><html lang=\"en-GB\"><head><meta charset=\"utf-8\"><title>MaffsCards</title>"
            "<link rel=\"stylesheet\" href=\"%s\"><style>%s</style></head><body>%s%s</body></html>"
            % (esc(FONTS), CSS, "".join(pages), teacher_html(data)))


def offline_context(browser, **opts):
    """Nothing reaches the network: Google Fonts from the repo's pinned copies (scripts/fonts/), all else aborted."""
    import bank_common as bc
    ctx = browser.new_context(**opts)

    def route(r):
        url = r.request.url
        if bc.is_font_cdn(url):
            bc.serve_real_font(r)
        elif url.startswith(("http:", "https:")):
            r.abort()
        else:
            r.continue_()
    ctx.route("**/*", route)
    return ctx


def build(out, proofs=None):
    data = json.loads(DATA.read_text(encoding="utf-8"))
    doc = document(data)
    if TRADE_MARK in doc.lower():
        raise BuildError("the deck uses the registered trade mark it must never name")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            ctx = offline_context(browser)
            page = ctx.new_page()
            page.set_content(doc, wait_until="load")
            fit = page.evaluate(FIT_JS, [BADGE_START, BADGE_MIN])
            problems = []
            for fam in ("Outfit", "JetBrains Mono"):
                if fam not in fit["loaded"]:
                    problems.append("font %s did not load (loaded: %s)" % (fam, sorted(set(fit["loaded"]))))
            for b in fit["badges"]:
                if not b["fits"] or b["size"] < BADGE_MIN:
                    problems.append("card %s: the badge row does not fit at %.1f pt even wrapped" % (b["n"], BADGE_MIN))
            for nk in fit["nick"]:
                if nk["lines"] > 2:
                    problems.append("card %s: the nickname takes %d lines" % (nk["n"], nk["lines"]))
            problems += ["overflow, %s" % o for o in fit["overflow"]]
            if any(k > 9 for k in fit["pages"]) or sum(fit["pages"]) != 50:
                problems.append("cards per page %s (34 + 16 cells, at most nine a page)" % fit["pages"])
            if problems:
                raise BuildError("; ".join(problems))
            out.parent.mkdir(parents=True, exist_ok=True)
            page.pdf(path=str(out), format="A4", print_background=True, prefer_css_page_size=True)
            if proofs:
                proofs = pathlib.Path(proofs)
                proofs.mkdir(parents=True, exist_ok=True)
                shot = offline_context(browser, viewport={"width": 794, "height": 1123},
                                       device_scale_factor=2).new_page()
                shot.set_content(doc, wait_until="load")
                shot.evaluate(FIT_JS, [BADGE_START, BADGE_MIN])
                for i, el in enumerate(shot.query_selector_all(".mc-page, .mc-sheet"), 1):
                    el.screenshot(path=str(proofs / ("page-%02d.png" % i)))
        finally:
            browser.close()
    return fit


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--proofs")
    a = ap.parse_args(argv)
    try:
        fit = build(pathlib.Path(a.out), a.proofs)
    except BuildError as e:
        print("BUILD FAILED: %s" % e)
        return 1
    sizes = sorted({b["size"] for b in fit["badges"]})
    wrapped = [b["n"] for b in fit["badges"] if b["wrapped"]]
    print("wrote %s: 8 pages; badges at %s pt%s; nicknames at most %d lines"
          % (a.out, ", ".join("%.1f" % s for s in sizes), (", wrapped on " + ", ".join(wrapped)) if wrapped else "",
             max(n["lines"] for n in fit["nick"])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
