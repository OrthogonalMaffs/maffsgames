#!/usr/bin/env python3
"""Build a double-sided, guillotine-ready loop-card pack (PDF) from a game's own question bank (contract LOOP-CARDS,
12 Nov 2026).

    python -X utf8 tools/loop-cards/build_deck.py six-sevens-bruv          # -> dist-packs/six-sevens-bruv-loop-cards.pdf
    python -X utf8 tools/loop-cards/build_deck.py like-terms-collector --final   # the copy for Tes: approved wording only
    python -X utf8 tools/loop-cards/build_deck.py six-sevens-bruv --proofs # also the PNG proofs in docs/screens/loop-cards/
    python -X utf8 tools/loop-cards/build_deck.py --selftest               # planted faults; builds no PDF

A pack holds three decks, of 16, 24 and 32 cards, each its own closed loop with its own deck code. A card's front
says "I have <answer>"; its back asks "Who has <question>?", whose answer is on the NEXT card's front, and the last
card's back asks the first card's answer, so following the backs visits every card once and comes back round.

Game-agnostic. Everything about a game lives in its adapter (six_sevens.py, like_terms.py): where its questions come
from, how a printed question and answer are recomputed (independently of the bank), how they are typeset, and any
special cards. decks/<slug>/config.json holds the title, seed, pack version and Jon's approval of the teacher wording
("wording_approved"; while it is null the teacher pages carry the DRAFT badge and --final refuses the pack). Approval,
the DRAFT badge, --final, the offline browser and the page footer are tools/pack-generator/build_pack.py's own.

The build, in order; any failure stops it before a PDF exists:
  1. Each deck: its cards chosen from the bank by the adapter (seeded), put in a seeded loop order, given shuffled
     card IDs (no two loop neighbours numbered one apart) and shuffled sheet places (no two loop neighbours side by
     side or one above the other on a sheet).
  2. Render: A4 portrait sheets of 2 x 4 A7 cards edge to edge; fronts then their mirrored backs (flip on long edge);
     then fold-over pages (front | back strips); teacher pages first. Every card's text is fitted in Chromium, at no
     less than 20 pt for questions and answers.
  3. The check reads what the pages PRINT (Chromium, network shut): the card faces' text and places, the answer
     sheets and the teacher page; it recomputes every question and answer with the adapter's own parser and proves
     each deck one closed loop, every back mirrored, every text inside the 8 mm safe zone, and the rest of the
     contract's list (README). The PDF's page count must equal the pages built.

The PDF goes to dist-packs/ (gitignored) and nowhere else. It is the product: never commit it, never upload it.
"""
import argparse
import copy
import datetime
import importlib
import json
import pathlib
import random
import re
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "tools" / "pack-generator"))
sys.path.insert(0, str(HERE))

import build_pack as bp      # noqa: E402  approval, DRAFT badge, --final, offline browser, page() and its footer

BuildError = bp.BuildError
OUT_DIR = bp.OUT_DIR
PROOF_DIR = ROOT / "docs" / "screens" / "loop-cards"
ADAPTERS = ("six_sevens", "like_terms")

CARD_W, CARD_H = 105.0, 74.25       # A7, mm: A4 portrait is exactly 2 x 4 of them
COLS, ROWS = 2, 4
SAFE_MM = 8.0                       # every text element this far inside each card edge
SIZES = (16, 24, 32)                # 2, 3 and 4 sheets
MIN_MAIN_PT = 20                    # questions, answers and the shout line
MIN_SMALL_PT = 9                    # labels, deck code and card ID, the web address
SHOUT_STEP = 4                      # the shout line is this much larger than the 42 above it
WEB = "maffsgames.co.uk"

# ---- the teacher page: Project Claude's draft, verbatim (contract item 8); Jon approves it via wording_approved -----
STEPS = (
    "Pick your deck from the table. Print it.",
    "Hand out every card. Some students get two.",
    "Anyone starts: read your back aloud.",
    "Got that answer on your front? Say “I have…”, turn over, read your back.",
    "It ends when the first card’s answer comes back round.",
)
WHICH = "Which deck?"
WHICH_ROWS = (("up to 16", 16), ("17–24", 24), ("25–32", 32))
WHICH_PAIRS = ("more than 32", "work in pairs, one card per pair")
TIPS = (
    "Pairs work for any class: nobody stands alone with a wrong answer.",
    "Group race: print one deck per group. First table to close the loop wins.",
)
NEVER_REMOVE = "Use every card in the deck. Missing cards break the loop."
PRINTING = (
    "Double-sided · flip on long edge · actual size (100%).",
    "Print one sheet first; hold it to the light to check.",
    "No double-sided printer? Use the fold-over pages (p. {FOLD}).",
)
MAX_WORDS, MAX_STEP_WORDS, MAX_LINES = 120, 15, 3
NUMBER_WORDS = re.compile(r"\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|"
                          r"fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|"
                          r"eighty|ninety|hundred|sixes|sevens|eights|nines|twelves|shout\w*)\b", re.I)


# ---- config and adapters -------------------------------------------------------------------------------------------

def load_config(slug):
    p = HERE / "decks" / slug / "config.json"
    if not p.is_file():
        raise BuildError("no tools/loop-cards/decks/%s/config.json" % slug)
    cfg = json.loads(p.read_text(encoding="utf-8"))
    if cfg.get("pack") != slug:
        raise BuildError("%s names pack %r" % (p.relative_to(ROOT), cfg.get("pack")))
    if cfg.get("adapter") not in ADAPTERS:
        raise BuildError("%s: adapter %r is not one of %s" % (p.relative_to(ROOT), cfg.get("adapter"), ADAPTERS))
    if not isinstance(cfg.get("seed"), int) or not str(cfg.get("title", "")).strip():
        raise BuildError("%s needs a title and an integer seed" % p.relative_to(ROOT))
    bp.wording_approved(cfg, slug)
    return cfg


def adapter(cfg):
    ad = importlib.import_module(cfg["adapter"])
    if ad.GAME != cfg["pack"]:
        raise BuildError("adapter %s is for %s, not %s" % (cfg["adapter"], ad.GAME, cfg["pack"]))
    return ad


def check_final(cfg, slug):
    """--final: build_pack's own refusal, named for this tool's config."""
    try:
        bp.check_final(cfg, slug)
    except BuildError:
        raise BuildError("%s: --final refuses a pack whose teacher wording is not approved (\"wording_approved\" is "
                         "null in tools/loop-cards/decks/%s/config.json)" % (slug, slug))


# ---- the decks -----------------------------------------------------------------------------------------------------

def make_deck(ad, cfg, n, items=None):
    """One deck of n cards in loop order: card k's front is items[k]'s answer, its back asks items[k+1]'s question."""
    code = "%s-%d" % (ad.CODE, n)
    rng = random.Random("%s|%s" % (cfg["seed"], code))
    if items is None:
        try:
            items = ad.choose(n, rng)
        except ValueError as e:
            raise BuildError("%s: the bank cannot give %d cards: %s" % (code, n, e))
        rng.shuffle(items)
    cards = [{"code": code, "front_label": "I have", "front": items[k]["a"], "front_shout": None,
              "back_label": "Who has", "back": items[(k + 1) % n]["q"] + "?", "back_wrap": False}
             for k in range(n)]
    sh = ad.SHOUT
    if sh:
        for k, it in enumerate(items):
            if it["a"] == sh["answer"]:
                cards[k]["front_shout"] = sh["answer_line"]
                cards[k - 1].update(back_label=sh["ask_label"], back=sh["ask"], back_wrap=True)
    for _ in range(20000):
        ids = list(range(1, n + 1))
        rng.shuffle(ids)
        if all(abs(ids[k] - ids[(k + 1) % n]) != 1 for k in range(n)):
            break
    else:
        raise BuildError("%s: no card numbering keeps loop neighbours apart" % code)
    slots = [(s, r, c) for s in range(n // (COLS * ROWS)) for r in range(ROWS) for c in range(COLS)]
    for _ in range(200000):
        rng.shuffle(slots)
        at = {slots[k]: k for k in range(n)}
        if not any((at.get((s, r + dr, c + dc), k) - k) % n in (1, n - 1)
                   for (s, r, c), k in at.items() for dr, dc in ((0, 1), (1, 0))):
            break
    else:
        raise BuildError("%s: no sheet layout keeps loop neighbours apart" % code)
    for k, card in enumerate(cards):
        card["id"], card["slot"] = ids[k], slots[k]
    return {"code": code, "n": n, "items": items, "cards": cards}


def make_pack(slug, cfg, ad):
    return {"slug": slug, "cfg": cfg, "decks": [make_deck(ad, cfg, n) for n in SIZES], "steps": STEPS}


# ---- rendering -----------------------------------------------------------------------------------------------------

def esc(s):
    return bp.esc(s)


def typeset(ad, text):
    return '<span class="%s">%s</span>' % (ad.TXT_CLASS, ad.html(text))


def back_html(ad, card):
    if card["back_wrap"] or not card["back"].endswith("?"):
        return esc(card["back"])
    return typeset(ad, card["back"][:-1]) + "?"


def face(ad, card, side, left, top, where):
    """One card face. side: "front" or "back"; where: "duplex" or "fold" (the plants use it)."""
    shout_line, special = "", ""
    if side == "front":
        label, text, mx = card["front_label"], typeset(ad, card["front"]), ad.FRONT_MAX
        if card["front_shout"]:
            line_max = ad.SHOUT["line_max"] if ad.SHOUT else 30
            shout_line = '<div class="lc-shout" data-max="%s">%s</div>' % (line_max, esc(card["front_shout"]))
            special = "|shout"
    else:
        label, text, mx = card["back_label"], back_html(ad, card), ad.BACK_MAX
        if card["back_wrap"]:
            mx = ad.SHOUT["ask_max"] if ad.SHOUT else mx
            special = "|ask"
    plant = card.get("plant_css")
    tag_style = ' style="%s"' % plant[1] if plant and plant[0] == side else ""
    web = "" if card.get("no_web") == (where, side) else '<span class="lc-web">%s</span>' % WEB
    kind = ' data-shout="%s"' % special[1:] if special else ""
    return ('<div class="lc-face"%s style="left:%smm;top:%smm"><div class="lc-safe">'
            '<div class="lc-tag"%s>%s</div>'
            '<div class="lc-mbox"><span class="lc-txt%s" data-max="%s" data-group="%s|%s%s">%s</span></div>%s'
            '<div class="lc-crow"><span class="lc-code">%s · %d</span>%s</div></div></div>'
            % (kind, left, top, tag_style, esc(label), " lc-wrap" if side == "back" and card["back_wrap"] else "",
               mx, card["code"], side, special, text, shout_line, esc(card["code"]), card["id"], web))


def sheet(kind, code, s, body):
    return '<section class="lc-sheet" data-kind="%s" data-deck="%s" data-sheet="%d">%s</section>' % (kind, code, s + 1, body)


CUTS = ('<div class="lc-cut lc-v" style="left:%smm"></div>' % CARD_W
        + "".join('<div class="lc-cut lc-h" style="top:%smm"></div>' % (CARD_H * r) for r in range(1, ROWS)))
FOLD_CUTS = ("".join('<div class="lc-cut lc-h" style="top:%smm"></div>' % (CARD_H * r) for r in range(1, ROWS))
             + '<div class="lc-fold" style="left:%smm"></div>' % CARD_W)


def duplex_sheets(ad, deck):
    pages = []
    for s in range(deck["n"] // (COLS * ROWS)):
        on = [c for c in deck["cards"] if c["slot"][0] == s]
        fr = "".join(face(ad, c, "front", c["slot"][2] * CARD_W, c["slot"][1] * CARD_H, "duplex") for c in on)
        bk = []
        for c in on:
            _, r, col = c.get("back_slot", (s, c["slot"][1], 1 - c["slot"][2]))    # mirrored for flip on long edge
            bk.append(face(ad, c, "back", col * CARD_W, r * CARD_H, "duplex"))
        pages.append(sheet("front", deck["code"], s, CUTS + fr))
        pages.append(sheet("back", deck["code"], s, "".join(bk)))
    return pages


def fold_sheets(ad, deck):
    pages = []
    cards = sorted(deck["cards"], key=lambda c: c["id"])
    for s in range(0, len(cards), ROWS):
        body = "".join(face(ad, c, "front", 0, i * CARD_H, "fold") + face(ad, c, "back", CARD_W, i * CARD_H, "fold")
                       for i, c in enumerate(cards[s:s + ROWS]))
        pages.append(sheet("fold", deck["code"], s // ROWS, FOLD_CUTS + body))
    return pages


def pages_text(a, b):
    return "%d" % a if a == b else "%d–%d" % (a, b)


def run_page(ad, pack, ranges, fold_range, badge):
    rows = "".join("<tr><td>%s</td><td>%d deck</td><td>p. %s</td><td>p. %s</td></tr>"
                   % (who, n, pages_text(*ranges["%s-%d" % (ad.CODE, n)][0]), pages_text(*ranges["%s-%d" % (ad.CODE, n)][1]))
                   for who, n in WHICH_ROWS)
    rows += '<tr><td>%s</td><td colspan="3">%s</td></tr>' % WHICH_PAIRS
    body = ('<ol class="lc-steps">%s</ol>' % "".join("<li>%s</li>" % esc(s) for s in pack["steps"])
            + '<h2>%s</h2>' % esc(WHICH)
            + '<table class="lc-which"><thead><tr><th>Students</th><th>Deck</th><th>Double-sided</th><th>Fold-over</th>'
              '</tr></thead><tbody>%s</tbody></table>' % rows
            + "".join('<p class="lc-tip">%s</p>' % esc(t) for t in TIPS)
            + '<p class="lc-rule">%s</p>' % esc(NEVER_REMOVE)
            + "".join('<p class="lc-rule">%s</p>' % esc(t) for t in ad.TEACHER_EXTRA)
            + '<div class="lc-printing"><h2>Printing</h2>%s</div>'
              % "".join('<div class="lc-line">%s</div>' % esc(t.replace("{FOLD}", pages_text(*fold_range)))
                        for t in PRINTING))
    return bp.page("run", body, "%s loop cards: how to run it" % esc(pack["cfg"]["title"]), badge=badge)


def key_page(ad, deck, badge):
    sh = ad.SHOUT
    rows = []
    for c in deck["cards"]:
        mark_f = " (shout)" if c["front_shout"] else ""
        mark_b = " (shout)" if sh and c["back_label"] == sh["ask_label"] else ""
        rows.append("<tr><td>%d</td><td>%s%s</td><td>%s%s</td></tr>"
                    % (c["id"], typeset(ad, c["front"]), mark_f, back_html(ad, c), mark_b))
    body = ('<table class="lc-key" data-deck="%s"><thead><tr><th>Card ID</th><th>I have</th><th>Who has</th></tr></thead>'
            '<tbody>%s</tbody></table>' % (deck["code"], "".join(rows)))
    return bp.page("key", body, "Answer sheets: %s" % deck["code"], badge=badge)


CSS = """
.lc-sheet { width: 210mm; height: 297mm; position: relative; overflow: hidden; break-after: page; }
body > section:last-child { break-after: auto; }
.lc-face { position: absolute; width: %(w)smm; height: %(h)smm; box-sizing: border-box; overflow: hidden; }
.lc-safe { position: absolute; left: %(s)smm; top: %(s)smm; width: %(sw)smm; height: %(sh)smm; display: flex;
           flex-direction: column; }
.lc-tag { flex: none; font-size: 11pt; font-weight: 600; line-height: 1.35; }
.lc-face[data-shout=ask] .lc-tag { font-weight: 800; letter-spacing: 0.06em; }
.lc-mbox { flex: 1 1 auto; min-height: 0; display: flex; align-items: center; justify-content: center; }
.lc-txt { display: inline-block; white-space: nowrap; line-height: 1.3; font-weight: 800; text-align: center; }
.lc-txt.lc-wrap { white-space: normal; word-break: keep-all; overflow-wrap: normal; font-family: 'Outfit', sans-serif; }
.lc-shout { flex: none; margin-top: 1.5mm; background: #000; color: #fff; font-weight: 800; text-align: center;
            line-height: 1.15; padding: 1.4mm 2mm; border-radius: 1.5mm; }
.lc-crow { flex: none; display: flex; justify-content: space-between; align-items: flex-end; font-size: 9pt;
           line-height: 1.35; margin-top: 1mm; }
.lc-code { font-weight: 600; color: #000; }
.lc-web { color: #666; font-weight: 500; }
.lc-cut { position: absolute; }
.lc-cut.lc-v { top: 0; bottom: 0; width: 0; border-left: 0.6pt dashed #777; }
.lc-cut.lc-h { left: 0; right: 0; height: 0; border-top: 0.6pt dashed #777; }
.lc-fold { position: absolute; top: 0; bottom: 0; width: 0; border-left: 0.8pt dotted #444; }
.lc-steps { font-size: 13pt; line-height: 1.3; padding-left: 8mm; margin: 1mm 0 3mm; }
.lc-steps li { margin-bottom: 2mm; }
table.lc-which { font-size: 12pt; margin-bottom: 4mm; }
table.lc-which td, table.lc-which th { padding: 1.6mm 2.5mm; }
.lc-tip, .lc-rule { font-size: 12pt; margin: 0 0 2.5mm; }
.lc-rule { font-weight: 700; }
.lc-printing { border: 1.4pt solid #000; padding: 2.5mm 4mm; margin-top: 4mm; font-size: 12pt; }
.lc-printing h2 { margin: 0 0 1.5mm; }
table.lc-key td, table.lc-key th { font-size: 10.5pt; line-height: 1.2; padding: 0.8mm 2.5mm; }
table.lc-key td:first-child { width: 22mm; font-weight: 700; }
""" % {"w": CARD_W, "h": CARD_H, "s": SAFE_MM, "sw": CARD_W - 2 * SAFE_MM, "sh": CARD_H - 2 * SAFE_MM}


def render(ad, pack, built):
    """(html, page plan). Teacher pages first (run it, then one answer sheet per deck), then every deck's duplex
    sheets, then every deck's fold-over pages, so every duplex block starts on an odd page."""
    cfg, slug = pack["cfg"], pack["slug"]
    badge = bp.draft_badge(cfg, slug)
    duplex = [(d, duplex_sheets(ad, d)) for d in pack["decks"]]
    fold = [(d, fold_sheets(ad, d)) for d in pack["decks"]]
    p = 1 + 1 + len(pack["decks"])
    ranges = {}
    for d, sh in duplex:
        ranges[d["code"]] = [(p, p + len(sh) - 1)]
        p += len(sh)
    fold_start = p
    for d, sh in fold:
        ranges.setdefault(d["code"], [(0, 0)]).append((p, p + len(sh) - 1))
        p += len(sh)
    total = p - 1
    teacher = [run_page(ad, pack, ranges, (fold_start, total), badge)] + [key_page(ad, d, badge) for d in pack["decks"]]
    pages = teacher + [x for _, sh in duplex for x in sh] + [x for _, sh in fold for x in sh]
    if len(pages) != total:
        raise BuildError("page plan: %d pages built, %d numbered" % (len(pages), total))
    foot = ('<span class="brand"><span class="logo"><img src="%s" alt=""></span><b>MaffsGames</b>'
            '<span>%s loop cards &middot; pack v%s &middot; seed %s &middot; built %s</span></span>'
            % (bp.LOGO.as_uri(), slug, esc(cfg.get("pack_version", "?")), cfg["seed"], built))
    doc = "".join(pg.replace("{{FOOT}}", "%s<span>page %d of %d</span>" % (foot, i + 1, total))
                  for i, pg in enumerate(pages))
    html_doc = ("<!doctype html><html lang='en'><head><meta charset='utf-8'><title>%s loop cards</title>"
                "<link rel='stylesheet' href='%s'><style>%s%s%s</style></head><body>%s</body></html>"
                % (esc(cfg["title"]), bp.GOOGLE_FONTS, bp.CSS, CSS, ad.CSS, doc))
    return html_doc, {"total": total, "ranges": ranges, "fold": (fold_start, total), "teacher": len(teacher)}


# ---- measuring in Chromium -----------------------------------------------------------------------------------------

FIT_JS = """
async ([minPt, shoutStep]) => {
  await document.fonts.ready;
  const fits = (box, t) => t.scrollWidth <= box.clientWidth + 0.5 && t.offsetWidth <= box.clientWidth + 0.5
                           && t.offsetHeight <= box.clientHeight + 0.5
                           && box.scrollWidth <= box.clientWidth + 0.5 && box.scrollHeight <= box.clientHeight + 0.5;
  const best = {}, fail = [];
  const mm = px => (px * 25.4 / 96).toFixed(1);
  const faces = [...document.querySelectorAll('.lc-face')];
  for (const f of faces) {
    const box = f.querySelector('.lc-mbox'), t = f.querySelector('.lc-txt'), sh = f.querySelector('.lc-shout');
    let got = null;
    if (sh) {
      // the shout line is SHOUT_STEP pt larger than the answer: the largest such pair that fits
      for (let a = +t.dataset.max; a >= minPt && got === null; a -= 0.5) {
        const s = Math.min(a + shoutStep, +sh.dataset.max);
        if (s <= a) continue;
        sh.style.fontSize = s + 'pt';
        t.style.fontSize = a + 'pt';
        if (fits(box, t)) got = [a, s];
      }
    } else {
      for (let a = +t.dataset.max; a >= minPt; a -= 0.5) {
        t.style.fontSize = a + 'pt';
        if (fits(box, t)) { got = [a, 0]; break; }
      }
    }
    const g = t.dataset.group;
    if (got === null) {
      fail.push({group: g, text: t.textContent, shout: sh ? sh.textContent : null, needMm: mm(t.scrollWidth),
                 boxMm: mm(box.clientWidth), hMm: mm(t.offsetHeight), boxHMm: mm(box.clientHeight)});
      got = [minPt, sh ? minPt + shoutStep : 0];
    }
    best[g] = best[g] ? [Math.min(best[g][0], got[0]), Math.min(best[g][1], got[1])] : got;
  }
  for (const f of faces) {
    const t = f.querySelector('.lc-txt'), sh = f.querySelector('.lc-shout'), b = best[t.dataset.group];
    t.style.fontSize = b[0] + 'pt';
    if (sh) sh.style.fontSize = b[1] + 'pt';
  }
  await document.fonts.ready;
  return {fail, best, loaded: [...document.fonts].filter(x => x.status === 'loaded').map(x => x.family.replace(/["']/g, ''))};
}
"""

AUDIT_JS = """
([safeMm, cardW, cardH, minMain, minSmall]) => {
  const px = 96 / 25.4, mm = v => v / px, tol = 0.15 * px;
  const out = {pages: 0, kinds: [], faces: [], safe: [], sizes: [], overlap: [], overflow: [], cuts: [], draft: [],
               teacher: [], tables: [], tokens: []};
  const secs = [...document.querySelectorAll('body > section')];
  out.pages = secs.length;
  const txt = e => e ? e.textContent.replace(/\\s+/g, ' ').trim() : null;
  const pt = e => parseFloat(getComputedStyle(e).fontSize) * 72 / 96;
  const words = s => (s.match(/\\S+/g) || []).filter(w => /[A-Za-z0-9]/.test(w)).length;
  const lines = e => {
    const r = document.createRange(); r.selectNodeContents(e);
    const ls = [];
    for (const q of r.getClientRects()) {
      if (q.width < 0.5 || q.height < 0.5) continue;
      const mid = (q.top + q.bottom) / 2;
      if (!ls.some(l => mid > l[0] && mid < l[1])) ls.push([q.top, q.bottom]);
    }
    return ls.length;
  };
  const hit = (a, b) => a.left < b.right - 0.5 && b.left < a.right - 0.5 && a.top < b.bottom - 0.5 && b.top < a.bottom - 0.5;
  secs.forEach((s, i) => {
    const kind = s.dataset.kind;
    out.kinds.push(kind);
    if (/\\bDRAFT\\b/.test(s.innerText)) out.draft.push([i + 1, kind]);
    if (s.innerHTML.includes('{{') || s.innerText.includes('{FOLD}')) out.tokens.push('page ' + (i + 1) + ' has an unfilled token');
    const sr = s.getBoundingClientRect();
    if (s.classList.contains('lc-sheet')) {
      // a line counts only if it is drawn the full height or width of the sheet
      const full = (sel, vert) => [...s.querySelectorAll(sel)].filter(e => {
        const b = e.getBoundingClientRect();
        return vert ? b.height >= sr.height - px && b.width > 0 : b.width >= sr.width - px && b.height > 0; }).length;
      out.cuts.push([i + 1, kind, full('.lc-cut.lc-v', true), full('.lc-cut.lc-h', false), full('.lc-fold', true)]);
      for (const f of s.querySelectorAll('.lc-face')) {
        const fr = f.getBoundingClientRect();
        const q = sel => txt(f.querySelector(sel));
        const face = {page: i + 1, kind, deck: s.dataset.deck, sheet: +s.dataset.sheet,
                      r: Math.round((fr.top - sr.top) / (cardH * px)), c: Math.round((fr.left - sr.left) / (cardW * px)),
                      wMm: mm(fr.width), hMm: mm(fr.height), label: q('.lc-tag'), main: q('.lc-txt'),
                      shout: q('.lc-shout'), code: q('.lc-code'), web: q('.lc-web'), mainPt: 0, shoutPt: 0};
        face.all = [face.label, face.main, face.shout, face.code, face.web].filter(x => x).join(' | ');
        out.faces.push(face);
        const where = 'p' + (i + 1) + ' ' + kind + ' sheet ' + s.dataset.sheet + ' row ' + (face.r + 1) + ' col ' + (face.c + 1)
                      + ' (' + face.code + ')';
        const inner = {l: fr.left + safeMm * px - tol, t: fr.top + safeMm * px - tol,
                       r: fr.right - safeMm * px + tol, b: fr.bottom - safeMm * px + tol};
        const rects = [];
        for (const e of f.querySelectorAll('.lc-tag, .lc-txt, .lc-shout, .lc-code, .lc-web')) {
          const b = e.getBoundingClientRect();
          rects.push([e, b]);
          const rr = document.createRange(); rr.selectNodeContents(e);
          for (const qq of [b, ...rr.getClientRects()]) {
            if (qq.width > 0 && (qq.left < inner.l || qq.top < inner.t || qq.right > inner.r || qq.bottom > inner.b)) {
              out.safe.push(where + ': ' + e.className + ' "' + txt(e) + '" is past the ' + safeMm + ' mm safe zone');
              break;
            }
          }
          const p = pt(e), big = e.matches('.lc-txt, .lc-shout');
          if (p < (big ? minMain : minSmall) - 0.01) out.sizes.push(where + ': ' + e.className + ' at ' + p.toFixed(1) + ' pt');
          if (e.matches('.lc-web') && Math.abs(p - minSmall) > 0.01) out.sizes.push(where + ': the web address is ' + p + ' pt, not 9');
          if (e.matches('.lc-txt')) face.mainPt = p;
          if (e.matches('.lc-shout')) face.shoutPt = p;
          if (e.matches('.lc-shout') && e.scrollWidth > e.clientWidth + 1) out.overflow.push(where + ': the shout line overflows');
        }
        for (const [e, b] of rects) if (e.matches('.lc-code, .lc-web'))
          for (const [e2, b2] of rects) if (e2 !== e && hit(b, b2))
            out.overlap.push(where + ': ' + e.className + ' overlaps ' + e2.className);
        const box = f.querySelector('.lc-mbox');
        if (box && (box.scrollWidth > box.clientWidth + 1 || box.scrollHeight > box.clientHeight + 1))
          out.overflow.push(where + ': "' + face.main + '" overflows its box');
      }
    } else {
      const m = s.querySelector('.main');
      if (m.scrollHeight > m.clientHeight + 1 || m.scrollWidth > m.clientWidth + 1)
        out.overflow.push('page ' + (i + 1) + ' (' + kind + ') overflows');
      const tp = {page: i + 1, kind, words: 0, titleWords: words(s.querySelector('.head').innerText), steps: [],
                  long: [], printingLines: 0};
      for (const ch of m.children) if (ch.tagName !== 'TABLE') tp.words += words(ch.innerText);
      for (const li of m.querySelectorAll('ol.lc-steps > li')) tp.steps.push([words(li.innerText), li.innerText]);
      for (const e of m.querySelectorAll('li, p, h2, .lc-line, td, th')) {
        const n = lines(e);
        if (n > 3) tp.long.push([n, e.innerText]);
      }
      for (const e of m.querySelectorAll('.lc-printing .lc-line')) tp.printingLines += lines(e);
      out.teacher.push(tp);
      for (const tb of m.querySelectorAll('table.lc-key'))
        out.tables.push({page: i + 1, deck: tb.dataset.deck,
                         rows: [...tb.querySelectorAll('tbody tr')].map(tr => [...tr.cells].map(td => txt(td)))});
    }
  });
  return out;
}
"""


def measure(pg, doc):
    with tempfile.TemporaryDirectory() as tmp:
        src = pathlib.Path(tmp) / "loop-cards.html"
        src.write_text(doc, encoding="utf-8")
        pg.goto(src.as_uri())
        fit = pg.evaluate(FIT_JS, [MIN_MAIN_PT, SHOUT_STEP])
        audit = pg.evaluate(AUDIT_JS, [SAFE_MM, CARD_W, CARD_H, MIN_MAIN_PT, MIN_SMALL_PT])
    return fit, audit


# ---- the check: what the pages PRINT, recomputed ------------------------------------------------------------------

CODE_RE = re.compile(r"([A-Z]+-\d+) · (\d+)")
SHOUT_MARK = " (shout)"


def check(ad, pack, plan, fit, audit):
    """Every problem with the printed pack, as sentences; an empty list means it passes."""
    P = []
    add = P.append
    sh = ad.SHOUT
    for f in fit["fail"]:
        add("%s: %r does not fit at %d pt (needs %s x %s mm; the box is %s x %s mm)%s"
            % (f["group"], f["text"], MIN_MAIN_PT, f["needMm"], f["hMm"], f["boxMm"], f["boxHMm"],
               "; shout line %r" % f["shout"] if f["shout"] else ""))
    for fam in ad.FONTS:
        if fam not in fit["loaded"]:
            add("font %s did not load (loaded: %s)" % (fam, sorted(set(fit["loaded"]))))
    for k in ("safe", "sizes", "overlap", "overflow", "tokens"):
        P.extend(audit[k])
    if audit["pages"] != plan["total"]:
        add("%d pages rendered, %d planned" % (audit["pages"], plan["total"]))
    kinds = audit["kinds"]
    teacher_pages = {i for i, k in enumerate(kinds, 1) if k in ("run", "key")}
    drafts = {p for p, _ in audit["draft"]}
    if bp.wording_approved(pack["cfg"], pack["slug"]):
        if drafts:
            add("the wording is approved, but pages %s print DRAFT" % sorted(drafts))
    else:
        if teacher_pages - drafts:
            add("the wording is not approved, but teacher pages %s carry no DRAFT badge" % sorted(teacher_pages - drafts))
        if drafts - teacher_pages:
            add("DRAFT is printed on card pages %s" % sorted(drafts - teacher_pages))
    for page, kind, v, h, fold in audit["cuts"]:
        want = {"front": (1, ROWS - 1, 0), "back": (0, 0, 0), "fold": (0, ROWS - 1, 1)}[kind]
        if (v, h, fold) != want:
            add("page %d (%s): %d vertical and %d horizontal cut lines, %d fold lines; expected %s" % (page, kind, v, h, fold, want))
    for i, k in enumerate(kinds, 1):
        if k == "front" and i % 2 == 0:
            add("page %d is a duplex front on an even page: fronts and backs would pair wrongly" % i)
        if k == "front" and (i >= len(kinds) or kinds[i] != "back"):
            add("page %d is a front not followed by its back" % i)

    # the teacher page's limits (contract item 8)
    for tp in audit["teacher"]:
        for n, text in tp["long"]:
            add("page %d: a text block runs to %d lines (at most %d): %r" % (tp["page"], n, MAX_LINES, text))
        if tp["kind"] == "run":
            if tp["words"] > MAX_WORDS:
                add("page 1 has %d words outside its table (at most %d)" % (tp["words"], MAX_WORDS))
            for n, text in tp["steps"]:
                if n > MAX_STEP_WORDS:
                    add("page 1: a step is %d words (at most %d): %r" % (n, MAX_STEP_WORDS, text))
            if tp["printingLines"] > MAX_LINES:
                add("page 1: the Printing box is %d lines (at most %d)" % (tp["printingLines"], MAX_LINES))

    faces = audit["faces"]
    for f in faces:
        if f["web"] != WEB:
            add("p%d %s %s row %d col %d: no %s on this face" % (f["page"], f["kind"], f["deck"], f["r"] + 1, f["c"] + 1, WEB))
        if abs(f["wMm"] - CARD_W) > 0.1 or abs(f["hMm"] - CARD_H) > 0.1:
            add("p%d: a card is %.2f x %.2f mm, not A7" % (f["page"], f["wMm"], f["hMm"]))
    deck_codes = {d["code"] for d in pack["decks"]}
    for f in faces:
        if f["deck"] not in deck_codes:
            add("p%d: a sheet of unknown deck %s" % (f["page"], f["deck"]))
    summary = {}
    for d in pack["decks"]:
        summary[d["code"]] = check_deck(ad, d["code"], [f for f in faces if f["deck"] == d["code"]],
                                        [t for t in audit["tables"] if t["deck"] == d["code"]], add)
    if len([t for t in audit["tables"]]) != len(pack["decks"]):
        add("%d answer sheets for %d decks" % (len(audit["tables"]), len(pack["decks"])))
    if not sh:
        for f in faces:
            if NUMBER_WORDS.search(f["all"] or ""):
                add("p%d %s (%s): a shout or a number in words in a pack without shouts: %r"
                    % (f["page"], f["kind"], f["code"], f["all"]))
    return P, summary


def check_deck(ad, code, faces, tables, add):
    sh = ad.SHOUT
    m = re.fullmatch(r"([A-Z]+)-(\d+)", code)
    n = int(m.group(2)) if m else 0
    if not m or m.group(1) != ad.CODE or n not in SIZES:
        add("%s is not a deck code of %s-16, -24 or -32" % (code, ad.CODE))
        return {}
    printed = {}
    for f in faces:
        cm = CODE_RE.fullmatch(f["code"] or "")
        if not cm:
            add("p%d %s (%s): cannot read the deck code and card ID %r" % (f["page"], f["kind"], code, f["code"]))
            f["id"] = None
            continue
        if cm.group(1) != code:
            add("p%d %s: a card carrying deck code %s is on a %s sheet" % (f["page"], f["kind"], cm.group(1), code))
        f["id"] = int(cm.group(2))
    fr = [f for f in faces if f["kind"] == "front"]
    bk = [f for f in faces if f["kind"] == "back"]
    fo = [f for f in faces if f["kind"] == "fold"]
    for name, group in (("fronts", fr), ("backs", bk)):
        ids = [f["id"] for f in group]
        if len(group) != n or sorted(ids) != list(range(1, n + 1)):
            add("%s: %d %s with card IDs %s; expected IDs 1 to %d once each" % (code, len(group), name, sorted(map(str, ids)), n))
    # mirrored backs: front (row r, column c) has its back at (row r, column 1 - c), on the very next page
    for f in fr:
        b = [x for x in bk if x["page"] == f["page"] + 1 and x["r"] == f["r"] and x["c"] == 1 - f["c"]]
        if len(b) != 1 or b[0]["id"] != f["id"]:
            add("%s sheet %d: the back of card %s (front row %d col %d) is not at its mirrored position (row %d col %d "
                "holds %s)" % (code, f["sheet"], f["id"], f["r"] + 1, f["c"] + 1, f["r"] + 1, 2 - f["c"],
                               [x["id"] for x in b] or "nothing"))
    front = {f["id"]: f for f in fr}
    back = {b["id"]: b for b in bk}
    for f in fr:
        if f["label"] != "I have":
            add("%s card %s: the front's label is %r, not 'I have'" % (code, f["id"], f["label"]))
    A, Q = {}, {}
    for i, f in front.items():
        try:
            A[i] = ad.value_a(f["main"])
        except ValueError as e:
            add("%s card %s front: %s" % (code, i, e))
    for i, b in back.items():
        if sh and b["label"] == sh["ask_label"]:
            pass
        elif b["label"] != "Who has":
            add("%s card %s: the back's label is %r, not 'Who has'" % (code, i, b["label"]))
        if not (b["main"] or "").endswith("?"):
            add("%s card %s: the back %r does not end with '?'" % (code, i, b["main"]))
            continue
        try:
            Q[i] = ad.value_q(b["main"][:-1].strip())
        except ValueError as e:
            add("%s card %s back: %s" % (code, i, e))
    owners = {}
    for i, v in A.items():
        owners.setdefault(v, []).append(i)
    for v, ids in owners.items():
        if len(ids) > 1:
            add("%s: the answer %s is on %d cards (%s): answers must be distinct" % (code, ad.show(v), len(ids), sorted(ids)))
    nxt = {}
    for i, v in Q.items():
        hits = owners.get(v, [])
        if not hits:
            add("%s card %s: its back %r (= %s) matches no front in the deck" % (code, i, back[i]["main"], ad.show(v)))
        elif len(hits) > 1:
            add("%s card %s: its back %r matches %d fronts" % (code, i, back[i]["main"], len(hits)))
        elif hits[0] == i:
            add("%s card %s: its back %r asks its own answer" % (code, i, back[i]["main"]))
        else:
            nxt[i] = hits[0]
    asked = {}
    for i, j in nxt.items():
        asked.setdefault(j, []).append(i)
    for j, by in asked.items():
        if len(by) > 1:
            add("%s card %s: its answer is asked by %d backs (%s)" % (code, j, len(by), sorted(by)))
    cycles = []
    seen = set()
    for start in sorted(nxt):
        if start in seen:
            continue
        cur, length = start, 0
        path = set()
        while cur in nxt and cur not in path:
            path.add(cur)
            cur = nxt[cur]
            length += 1
        seen |= path
        cycles.append(length if cur == start else -length)
    if cycles != [n]:
        add("%s: following the backs gives %s, not one closed loop of all %d cards"
            % (code, ", ".join(("a loop of %d" % c) if c > 0 else ("a broken chain of %d" % -c) for c in cycles) or "nothing", n))
    for i, j in nxt.items():
        if abs(i - j) == 1:
            add("%s: loop neighbours %d and %d have consecutive card IDs" % (code, i, j))
    for f in fr:
        for g in fr:
            if f["page"] == g["page"] and (g["r"], g["c"]) in ((f["r"], f["c"] + 1), (f["r"] + 1, f["c"])) \
                    and (nxt.get(f["id"]) == g["id"] or nxt.get(g["id"]) == f["id"]):
                add("%s sheet %d: loop neighbours %s and %s sit next to each other" % (code, f["sheet"], f["id"], g["id"]))
    # fold-over pages: each strip is one card, front half then back half, the same text as the duplex card
    strips = {}
    for f in fo:
        strips.setdefault((f["page"], f["r"]), {})[f["c"]] = f
    fold_ids = []
    for (page, r), halves in sorted(strips.items()):
        L, R = halves.get(0), halves.get(1)
        if not L or not R or L["id"] != R["id"]:
            add("%s fold-over p%d strip %d: its halves are not one card's front and back" % (code, page, r + 1))
            continue
        fold_ids.append(L["id"])
        for half, dup in ((L, front.get(L["id"])), (R, back.get(L["id"]))):
            if dup and (half["label"], half["main"], half["shout"]) != (dup["label"], dup["main"], dup["shout"]):
                add("%s fold-over card %s: %r differs from its duplex face %r" % (code, L["id"], half["all"], dup["all"]))
    if sorted(fold_ids) != list(range(1, n + 1)):
        add("%s: the fold-over pages hold cards %s, not 1 to %d once each" % (code, sorted(fold_ids), n))
    # the shout pair (Six Sevens): exactly one, on 6 x 7 = 42 recomputed from the words
    ask_id = ans_id = None
    if sh:
        target = ad.value_q(sh["ask"][:-1])
        ans = owners.get(target, [])
        if len(ans) != 1:
            add("%s: no card answers %s (6 × 7): every Six Sevens deck holds it" % (code, ad.show(target)))
        shouted = [i for i, f in front.items() if f["shout"]]
        if shouted != ans or len(shouted) != 1:
            add("%s: the answering shout is on card(s) %s, whose answers are %s, not %s"
                % (code, shouted, [front[i]["main"] for i in shouted], ad.show(target)))
        elif front[shouted[0]]["shout"] != sh["answer_line"]:
            add("%s card %s: the shout line reads %r, not %r" % (code, shouted[0], front[shouted[0]]["shout"], sh["answer_line"]))
        else:
            ans_id = shouted[0]
            if not front[ans_id]["shoutPt"] > front[ans_id]["mainPt"]:
                add("%s card %s: the shout line (%.1f pt) is not larger than the answer (%.1f pt)"
                    % (code, ans_id, front[ans_id]["shoutPt"], front[ans_id]["mainPt"]))
        asks = [i for i, b in back.items() if b["label"] == sh["ask_label"]]
        if len(asks) != 1:
            add("%s: %d backs are labelled %r, not one" % (code, len(asks), sh["ask_label"]))
        for i in asks:
            if back[i]["main"] != sh["ask"] or Q.get(i) != target:
                add("%s card %s: the %s back asks %r (= %s), not %r for %s" % (code, i, sh["ask_label"], back[i]["main"],
                                                                         ad.show(Q[i]) if i in Q else "?", sh["ask"], ad.show(target)))
            elif ans_id is not None and nxt.get(i) != ans_id:
                add("%s card %s: the shouted question is not answered by the shouting card" % (code, i))
            else:
                ask_id = i
        for i, b in back.items():
            if b["main"] == sh["ask"] and i not in asks:
                add("%s card %s: the back asks %r without the %r label" % (code, i, sh["ask"], sh["ask_label"]))
        allowed = {("front", ans_id), ("back", ask_id)}
        for f in faces:
            side = f["kind"] if f["kind"] != "fold" else ("front" if f["c"] == 0 else "back")
            if NUMBER_WORDS.search(f["all"] or "") and (side, f.get("id")) not in allowed:
                add("%s card %s (%s, p%d): a shout or a number in words off the shout pair: %r"
                    % (code, f.get("id"), side, f["page"], f["all"]))
    # the answer sheet: loop order, the cards' own text, shout rows marked
    if len(tables) != 1:
        add("%s: %d answer sheets, not one" % (code, len(tables)))
    for t in tables:
        rows = t["rows"]
        if len(rows) != n:
            add("%s answer sheet: %d rows, not %d" % (code, len(rows), n))
        ids = []
        for row in rows:
            if len(row) != 3 or not re.fullmatch(r"\d+", row[0] or ""):
                add("%s answer sheet: cannot read the row %r" % (code, row))
                continue
            i = int(row[0])
            ids.append(i)
            have, mf = (row[1][:-len(SHOUT_MARK)], True) if row[1].endswith(SHOUT_MARK) else (row[1], False)
            who, mb = (row[2][:-len(SHOUT_MARK)], True) if row[2].endswith(SHOUT_MARK) else (row[2], False)
            if i not in front or have != front[i]["main"] or i not in back or who != back[i]["main"]:
                add("%s answer sheet: the row for card %d (%r, %r) is not that card" % (code, i, have, who))
            if mf != (i == ans_id) or mb != (i == ask_id):
                add("%s answer sheet: card %d's (shout) marks are wrong" % (code, i))
        for a, b in zip(ids, ids[1:] + ids[:1]):
            if nxt.get(a) != b:
                add("%s answer sheet: card %d is followed by %d, but card %d's back is answered by %s"
                    % (code, a, b, a, nxt.get(a)))
                break
    return {"n": n, "loop": cycles, "front_pt": min([f["mainPt"] for f in fr if not f["shout"]] or [0]),
            "back_pt": min([b["mainPt"] for b in bk if not (sh and b["label"] == sh["ask_label"])] or [0]),
            "shout": (front[ans_id]["mainPt"], front[ans_id]["shoutPt"], back[ask_id]["mainPt"])
            if ans_id and ask_id else None,
            "answers": [front[i]["main"] for i in sorted(front)]}


# ---- the build -----------------------------------------------------------------------------------------------------

def built_today():
    return datetime.date.today().isoformat()


def proofs(pg, ad, pack, doc):
    """PNGs at 100% (96 px per inch): each deck's first front, first back and first fold-over page; both shout cards
    on their own; page 1."""
    slug = pack["slug"]
    PROOF_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    with tempfile.TemporaryDirectory() as tmp:
        src = pathlib.Path(tmp) / "loop-cards.html"
        src.write_text(doc, encoding="utf-8")
        pg.goto(src.as_uri())
        pg.evaluate(FIT_JS, [MIN_MAIN_PT, SHOUT_STEP])
        secs = pg.locator("body > section")

        def shot(loc, name):
            path = PROOF_DIR / name
            loc.screenshot(path=str(path))
            written.append(path)
        shot(secs.nth(0), "%s-teacher1.png" % slug)
        for d in pack["decks"]:
            n = d["n"]
            for kind, tag in (("front", "front1"), ("back", "back1"), ("fold", "fallback1")):
                shot(pg.locator('section.lc-sheet[data-kind="%s"][data-deck="%s"]' % (kind, d["code"])).first,
                     "%s-%d-%s.png" % (slug, n, tag))
        if ad.SHOUT:
            shot(pg.locator('section.lc-sheet[data-kind="back"] .lc-face[data-shout="ask"]').first, "%s-shout-ask.png" % slug)
            shot(pg.locator('section.lc-sheet[data-kind="front"] .lc-face[data-shout="shout"]').first,
                 "%s-shout-answer.png" % slug)
    return written


def build(slug, final=False, want_proofs=False):
    from playwright.sync_api import sync_playwright
    cfg = load_config(slug)
    if final:
        check_final(cfg, slug)
    ad = adapter(cfg)
    out = OUT_DIR / ("%s-loop-cards.pdf" % slug)
    if not bp.ignored_by_git(out):
        raise BuildError("%s is not ignored by git: refusing to write the product where it could be committed"
                         % out.relative_to(ROOT))
    pack = make_pack(slug, cfg, ad)
    built = built_today()
    doc, plan = render(ad, pack, built)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            pg = bp.offline_context(browser).new_page()
            fit, audit = measure(pg, doc)
            problems, summary = check(ad, pack, plan, fit, audit)
            if problems:
                raise BuildError("the pack fails its checks:\n  " + "\n  ".join(problems))
            report(ad, pack, plan, fit, audit, summary, final)
            with tempfile.TemporaryDirectory() as tmp:
                src = pathlib.Path(tmp) / "loop-cards.html"
                src.write_text(doc, encoding="utf-8")
                pg.goto(src.as_uri())
                pg.evaluate(FIT_JS, [MIN_MAIN_PT, SHOUT_STEP])
                OUT_DIR.mkdir(exist_ok=True)
                pg.pdf(path=str(out), format="A4", print_background=True, prefer_css_page_size=True)
            got = bp.pdf_page_count(out)
            if got != plan["total"]:
                out.unlink()
                raise BuildError("the PDF has %d pages, but %d were built: a page overflowed" % (got, plan["total"]))
            print("wrote %s: %d pages, %d KB" % (out.relative_to(ROOT), got, out.stat().st_size // 1024))
            if want_proofs:
                for path in proofs(pg, ad, pack, doc):
                    print("proof %s" % path.relative_to(ROOT))
        finally:
            browser.close()


def report(ad, pack, plan, fit, audit, summary, final):
    cfg, slug = pack["cfg"], pack["slug"]
    for d in pack["decks"]:
        s = summary[d["code"]]
        print("%s: %d cards, one closed loop of %d (every back recomputed and matched to exactly one other card's front); "
              "fronts %.1f pt, backs %.1f pt" % (d["code"], s["n"], s["loop"][0], s["front_pt"], s["back_pt"]))
        print("  answers: %s" % ", ".join(s["answers"]))
        if s["shout"]:
            print("  shout pair: 42 at %.1f pt under the shout line at %.1f pt; the asking card at %.1f pt" % s["shout"])
    run = next(t for t in audit["teacher"] if t["kind"] == "run")
    print("every back mirrored for flip on long edge; every text inside the %g mm safe zone; questions and answers at "
          "least %d pt, labels and the web address at least %d pt; %s on all %d card faces"
          % (SAFE_MM, MIN_MAIN_PT, MIN_SMALL_PT, WEB, len(audit["faces"])))
    print("page 1: %d words outside its table (at most %d; the title adds %d), longest step %d words (at most %d), "
          "Printing box %d lines, no text block past %d lines"
          % (run["words"], MAX_WORDS, run["titleWords"], max(n for n, _ in run["steps"]), MAX_STEP_WORDS,
             run["printingLines"], MAX_LINES))
    appr = bp.wording_approved(cfg, slug)
    print("wording approved by %s on %s: no page says DRAFT%s" % (appr["by"], appr["date"], " (--final)" if final else "")
          if appr else "wording NOT approved: the DRAFT badge is on every teacher page (--final would refuse)")
    for d in pack["decks"]:
        dup, fold = plan["ranges"][d["code"]]
        print("  %s: double-sided pages %s, fold-over pages %s" % (d["code"], pages_text(*dup), pages_text(*fold)))


# ---- the selftest --------------------------------------------------------------------------------------------------

def _deck(pack, code):
    return next(d for d in pack["decks"] if d["code"] == code)


def _swap_coefficients(text):
    m = re.fullmatch(r"(\d*)([a-z]) \+ (\d*)([a-z])", text)
    if not m or (m.group(1) or "1") == (m.group(3) or "1"):
        return None
    return "%s%s + %s%s" % (m.group(3), m.group(2), m.group(1), m.group(4))


def plant_dup(ad, cfg, pack):
    d = _deck(pack, "LT-32")
    d["cards"][3]["front"] = d["cards"][7]["front"]


def plant_no_front(ad, cfg, pack):
    _deck(pack, "LT-32")["cards"][5]["back"] = "9z + z?"


def plant_two_loops(ad, cfg, pack):
    d = _deck(pack, "LT-32")
    d["cards"][15]["back"] = d["items"][0]["q"] + "?"
    d["cards"][31]["back"] = d["items"][16]["q"] + "?"


def plant_own(ad, cfg, pack):
    d = _deck(pack, "LT-32")
    d["cards"][4]["back"] = d["items"][4]["q"] + "?"


def plant_mirror(ad, cfg, pack):
    d = _deck(pack, "SS-16")
    a, b = [c for c in d["cards"] if c["slot"][0] == 0][:2]
    a["back_slot"] = (0, b["slot"][1], 1 - b["slot"][2])
    b["back_slot"] = (0, a["slot"][1], 1 - a["slot"][2])


def plant_safe(ad, cfg, pack):
    _deck(pack, "SS-24")["cards"][0]["plant_css"] = ("front", "margin-left: -3mm")


def plant_similar(ad, cfg, pack):
    d = _deck(pack, "LT-32")
    for c in d["cards"]:
        s = _swap_coefficients(c["front"])
        if s:
            c["front"] = s
            return
    raise AssertionError("no answer to swap")


def plant_foreign(ad, cfg, pack):
    d32, d24 = _deck(pack, "LT-32"), _deck(pack, "LT-24")
    stranger = copy.deepcopy(d24["cards"][0])
    stranger["slot"] = d32["cards"][2]["slot"]
    d32["cards"][2] = stranger


def plant_step(ad, cfg, pack):
    pack["steps"] = pack["steps"][:3] + ("Got that answer on your front? Then say I have, turn your card over and "
                                         "read your back.",) + pack["steps"][4:]


def plant_no_67(ad, cfg, pack):
    d = _deck(pack, "SS-16")
    items = [it if it["a"] != ad.SHOUT["answer"] else ad.unused(d["items"]) for it in d["items"]]
    pack["decks"][0] = make_deck(ad, cfg, 16, items)


def plant_shout_wrong_answer(ad, cfg, pack):
    d = _deck(pack, "SS-24")
    k = next(i for i, c in enumerate(d["cards"]) if c["front_shout"])
    d["cards"][(k + 5) % 24]["front_shout"] = d["cards"][k]["front_shout"]
    d["cards"][k]["front_shout"] = None


def plant_ask_wrong(ad, cfg, pack):
    d = _deck(pack, "SS-32")
    k = next(i for i, c in enumerate(d["cards"]) if c["back_wrap"])
    d["cards"][(k + 9) % 32]["back_label"] = ad.SHOUT["ask_label"]


def plant_lt_shout(ad, cfg, pack):
    _deck(pack, "LT-16")["cards"][0]["front_shout"] = "SHOUT: I’VE GOT SIX SEVENS, BRUV!"


def plant_no_web(ad, cfg, pack):
    _deck(pack, "SS-16")["cards"][1]["no_web"] = ("fold", "back")


PLANTS = (
    ("a duplicated answer", "like-terms-collector", plant_dup, r"is on 2 cards"),
    ("a back with no matching front", "like-terms-collector", plant_no_front, r"matches no front"),
    ("two loops of 16 inside the 32 deck", "like-terms-collector", plant_two_loops, r"a loop of 16, a loop of 16"),
    ("a card asking its own answer", "like-terms-collector", plant_own, r"asks its own answer"),
    ("a back not mirrored", "six-sevens-bruv", plant_mirror, r"not at its mirrored position"),
    ("text past the safe zone", "six-sevens-bruv", plant_safe, r"past the 8 mm safe zone"),
    ("a like-terms answer string-similar but different in value", "like-terms-collector", plant_similar,
     r"matches no front"),
    ("a card from deck 24 placed in deck 32", "like-terms-collector", plant_foreign,
     r"deck code LT-24 is on a LT-32 sheet"),
    ("a teacher step over 15 words", "six-sevens-bruv", plant_step, r"a step is 1[6-9] words"),
    ("a Six Sevens deck without 6 × 7", "six-sevens-bruv", plant_no_67, r"SS-16: no card answers 42"),
    ("the answering shout on a card that is not 42", "six-sevens-bruv", plant_shout_wrong_answer,
     r"answering shout is on card"),
    ("the asking shout on a back that does not ask for 42", "six-sevens-bruv", plant_ask_wrong,
     r"the SHOUT IT back asks"),
    ("a shout in the Like Terms pack", "like-terms-collector", plant_lt_shout, r"in a pack without shouts"),
    ("a card face without the web address", "six-sevens-bruv", plant_no_web, r"no maffsgames\.co\.uk on this face"),
)


def selftest():
    from playwright.sync_api import sync_playwright
    failures = []
    slugs = sorted(p.parent.name for p in (HERE / "decks").glob("*/config.json"))
    packs = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            pg = bp.offline_context(browser).new_page()
            for slug in slugs:
                cfg = load_config(slug)
                ad = adapter(cfg)
                pack = make_pack(slug, cfg, ad)
                packs[slug] = (cfg, ad, pack)
                doc, plan = render(ad, pack, built_today())
                problems, _ = check(ad, pack, plan, *measure(pg, doc))
                if problems:
                    failures.append("%s as built fails:\n    %s" % (slug, "\n    ".join(problems)))
                else:
                    print("ok    %s as built passes every check" % slug)
                for flip in (True, False):     # the DRAFT badge follows the approval both ways
                    c2 = dict(cfg, wording_approved={"by": "Jon", "date": "2026-11-12"} if flip else None)
                    p2 = dict(pack, cfg=c2)
                    doc2, plan2 = render(ad, p2, built_today())
                    pr2, _ = check(ad, p2, plan2, *measure(pg, doc2))
                    if pr2:
                        failures.append("%s with wording_approved %s fails:\n    %s"
                                        % (slug, c2["wording_approved"], "\n    ".join(pr2)))
            for name, slug, fn, expect in PLANTS:
                cfg, ad, pack = packs[slug]
                planted = copy.deepcopy(pack)
                fn(ad, cfg, planted)
                doc, plan = render(ad, planted, built_today())
                problems, _ = check(ad, planted, plan, *measure(pg, doc))
                caught = [x for x in problems if re.search(expect, x)]
                if caught:
                    print("ok    planted %s: caught (%s)" % (name, caught[0]))
                else:
                    failures.append("planted %s: NOT caught as /%s/; the check said: %s" % (name, expect, problems or "nothing"))
        finally:
            browser.close()
    cfg = dict(packs["six-sevens-bruv"][0], wording_approved=None)
    try:
        check_final(cfg, "six-sevens-bruv")
        failures.append("planted an unapproved --final build: NOT refused")
    except BuildError as e:
        print("ok    planted an unapproved --final build: refused (%s)" % e)
    out = OUT_DIR / "six-sevens-bruv-loop-cards.pdf"
    if not bp.ignored_by_git(out) or bp.ignored_by_git(HERE / "build_deck.py"):
        failures.append("the gitignore check does not tell dist-packs/ from tracked files")
    if failures:
        print("SELFTEST FAILED:\n  " + "\n  ".join(failures))
        return 1
    print("selftest: both packs pass; all %d planted faults caught" % (len(PLANTS) + 1))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("pack", nargs="?", help="the pack's slug: six-sevens-bruv or like-terms-collector")
    ap.add_argument("--final", action="store_true",
                    help="the copy for Tes: refuse a pack whose teacher wording is not approved (its config's wording_approved)")
    ap.add_argument("--proofs", action="store_true", help="also write the PNG proofs to docs/screens/loop-cards/")
    ap.add_argument("--selftest", action="store_true", help="planted faults; builds no PDF")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        if a.selftest:
            return selftest()
        if not a.pack:
            ap.error("name a pack, e.g. six-sevens-bruv")
        build(a.pack, a.final, a.proofs)
        return 0
    except BuildError as e:
        print("BUILD FAILED: %s" % e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
