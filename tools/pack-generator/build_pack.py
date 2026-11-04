#!/usr/bin/env python3
"""Build a printable A4 group-race pack (PDF) of an escape room from its checked data (contract PACK-GENERATOR, 4 Nov 2026).

    python -X utf8 tools/pack-generator/build_pack.py kiln-disaster              # -> dist-packs/kiln-disaster-pack.pdf
    python -X utf8 tools/pack-generator/build_pack.py kiln-disaster --sets 7 --seed 1
    python -X utf8 tools/pack-generator/build_pack.py --selftest                 # planted faults; builds no PDF

Room-agnostic. Everything about a room comes from three places, none of them typed here:
  * escape-rooms/<slug>/room.js, evaluated by Chromium exactly as the room page evaluates it (window.ROOM): the prose,
    objects, locks, hints and worked-solution templates; and teacher.html's window.TEACH (topics, minutes);
  * escape-rooms/variants.json, the verified variant libraries (room.js must equal them, as check-escape-rooms.py holds);
  * tools/pack-generator/rooms/<slug>/config.json: the art, each image's role and label box in image pixels, the font
    per card, the set count, seed and pack version, and the words printed on red-herring objects.

The build, in order; any failure stops it before a PDF exists:
  1. scripts/check-escape-rooms.py is imported (run in full, unchanged): its draw_is_valid() and clue_strings() are the
     rules the room engine serves draws by. If that check fails, nothing is built.
  2. Selection: every joint draw (one variant per lock) is judged by draw_is_valid(); from the VALID ones, N are chosen
     with every lock's answers distinct across the N sets. Deterministic for a seed (a seeded shuffle, then a search).
  3. Verification: lockcheck.py recomputes every answer, common wrong answer and worked-solution figure from each
     variant's givens, by a method independent of the generator that made them. Any mismatch stops the build.
  4. Render: one HTML page per A4 page, printed to PDF by Playwright's Chromium with the network shut (fonts from the
     repo's pinned copies). In the page, every printed label is fitted to its box at no less than 11 pt, every page is
     checked for overflow, every student page for its set letter, every red herring for digits, everything for an
     unfilled {{token}}; the PDF's page count must equal the pages built.

The PDF goes to dist-packs/ (gitignored) and nowhere else. It is the product: never commit it, never upload it.
"""
import argparse
import contextlib
import copy
import datetime
import html
import importlib.util
import io
import itertools
import json
import pathlib
import random
import re
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SCRIPTS = ROOT / "scripts"
ROOMS = ROOT / "escape-rooms"
OUT_DIR = ROOT / "dist-packs"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(HERE))

import lockcheck                # noqa: E402  the independent recomputation, keyed by lock id
import plant_common as pc       # noqa: E402

MIN_PT = 11                     # no printed label smaller than this (contract STOP IF)
MAX_PT = 20                     # a label is fitted downward from here
FONTS = {                       # the faces a config's "font" may name: tools/pack-generator/fonts/, with their licences
    "label": ("PackLabel", "Oswald-Variable.ttf", "200 700", 600),
    "hand": ("PackHand", "PermanentMarker-Regular.ttf", "400", 400),
}
LOGO = ROOT / "schools" / "assets" / "m_plus_logo.svg"   # read in place (Amendment 1), never copied
GOOGLE_FONTS = "https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap"


class BuildError(Exception):
    pass


# ---- the room's checked data ---------------------------------------------------------------------------------------

class _Sink(io.StringIO):
    def reconfigure(self, **kw):          # check-escape-rooms.py reconfigures stdout for a Windows console
        pass


def load_checker():
    """scripts/check-escape-rooms.py, imported unchanged. Importing it runs the whole room check (about 2 s): its
    output is held back, and a failing check stops the build with that output."""
    spec = importlib.util.spec_from_file_location("check_escape_rooms", SCRIPTS / "check-escape-rooms.py")
    mod = importlib.util.module_from_spec(spec)
    sink = _Sink()
    try:
        with contextlib.redirect_stdout(sink):
            spec.loader.exec_module(mod)
    except SystemExit:
        raise BuildError("scripts/check-escape-rooms.py fails, so the rooms' data is not checked. Its output:\n"
                         + sink.getvalue()[-4000:])
    for name in ("draw_is_valid", "clue_strings", "flat"):
        if not callable(getattr(mod, name, None)):
            raise BuildError("scripts/check-escape-rooms.py no longer defines %s()" % name)
    return mod


def offline_context(browser):
    """A browser context that reaches nothing on the network: Google Fonts requests are answered from the repo's
    pinned copies (bank_common.serve_real_font, the phone-fit checks' own route); every other http(s) request is
    aborted, so no analytics or CDN call can ever leave."""
    import bank_common as bc
    ctx = browser.new_context()

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


def read_room(page, slug):
    """(ROOM, TEACH, room.js text): room.js and teacher.html's TEACH block evaluated in a blank page. The page itself is
    never loaded, so neither analytics.js nor the engine runs."""
    room_dir = ROOMS / slug
    if not (room_dir / "room.js").is_file():
        raise BuildError("no escape-rooms/%s/room.js" % slug)
    js = (room_dir / "room.js").read_text(encoding="utf-8")
    page.goto("about:blank")
    page.add_script_tag(content=js)
    room = page.evaluate("() => JSON.parse(JSON.stringify(window.ROOM))")
    teach = {}
    t = room_dir / "teacher.html"
    if t.is_file():
        m = re.search(r"<script>\s*(window\.TEACH\s*=.*?)</script>", t.read_text(encoding="utf-8"), re.S)
        if m:
            page.add_script_tag(content=m.group(1))
            teach = page.evaluate("() => JSON.parse(JSON.stringify(window.TEACH || {}))")
    return room, teach, js


def load_config(slug):
    p = HERE / "rooms" / slug / "config.json"
    if not p.is_file():
        raise BuildError("no tools/pack-generator/rooms/%s/config.json" % slug)
    cfg = json.loads(p.read_text(encoding="utf-8"))
    if cfg.get("room") != slug:
        raise BuildError("%s names room %r" % (p.relative_to(ROOT), cfg.get("room")))
    for im in cfg["images"]:
        f = HERE / "rooms" / slug / im["file"]
        if not f.is_file():
            raise BuildError("config image missing: %s" % f.relative_to(ROOT))
        if im.get("font", "label") not in FONTS:
            raise BuildError("%s: font %r is not one of %s" % (im["file"], im.get("font"), sorted(FONTS)))
        x0, y0, x1, y1 = im["label_box"]
        if not (0 <= x0 < x1 and 0 <= y0 < y1):
            raise BuildError("%s: label_box %r is not a box" % (im["file"], im["label_box"]))
    return cfg


def room_locks(room, slug):
    """The room's locks, each with its verified library from variants.json (which room.js must equal)."""
    verified = json.loads((ROOMS / "variants.json").read_text(encoding="utf-8"))
    locks = []
    for l in room["locks"]:
        lid, key = l["id"], l.get("key") or l["id"]
        if lid not in verified:
            raise BuildError("%s/%s: no verified library in escape-rooms/variants.json" % (slug, lid))
        if l.get("variants") != verified[lid]:
            raise BuildError("%s/%s: room.js has drifted from variants.json" % (slug, lid))
        locks.append(dict(l, key=key, variants=verified[lid]))
    return locks


def room_url(slug):
    """The room's own public URL, from the repo (Amendment 1): the host in CNAME and the room's folder. The page must
    exist and be live (no noindex: a withdrawn room's holding page is not advertised)."""
    host = (ROOT / "CNAME").read_text(encoding="utf-8").strip()
    url = "%s/escape-rooms/%s/" % (host, slug)
    problem = resolve_url(url)
    if problem:
        raise BuildError(problem)
    return url


def resolve_url(url):
    """None if `url` (host/path, as printed) is a live room page in this repo, else the reason it is not."""
    host = (ROOT / "CNAME").read_text(encoding="utf-8").strip()
    m = re.fullmatch(r"(?:https?://)?(?:www\.)?%s/(escape-rooms/[a-z0-9-]+/)" % re.escape(host), url)
    if not m:
        return "%s is not a room page on %s" % (url, host)
    page = ROOT / m.group(1) / "index.html"
    if not page.is_file():
        return "%s resolves to %s, which does not exist" % (url, page.relative_to(ROOT).as_posix())
    if "noindex" in page.read_text(encoding="utf-8"):
        return "%s resolves to a withdrawn room (noindex)" % url
    return None


URL_RE = re.compile(r"(?:https?://)?(?:www\.)?[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:co\.uk|org\.uk|com|org|net|io|uk)"
                    r"(?:/[^\s,;)]*)?", re.I)


def check_printed_text(pages_text, url):
    """Problems with what the pages print (Amendment 1): every URL printed resolves to a live room page in the repo
    and is the room's own; the cover sheets and teacher notes carry the play-online line; no Tes branding."""
    out = []
    line = "Play this room free online: " + url
    for kind, text in pages_text:
        for u in URL_RE.findall(text):
            u = u.rstrip(".")
            why = resolve_url(u)
            if why:
                out.append("%s page prints %s" % (kind, why))
            elif u != url:
                out.append("%s page prints another URL, %s" % (kind, u))
        if kind in ("cover", "teacher") and line not in " ".join(text.split()):
            out.append("a %s page does not carry %r" % (kind, line))
        if re.search(r"\bTes\b", text):
            out.append("a %s page names Tes" % kind)
    return out


def text_of(s):
    """The words a reader sees in a room string (tags dropped, entities decoded)."""
    return html.unescape(re.sub(r"<[^>]*>", " ", s or ""))


# ---- selection -----------------------------------------------------------------------------------------------------

def valid_picks(checker, room_js, locks):
    """(every VALID joint draw as a tuple of variant indices, the number of joint draws)."""
    clues = checker.clue_strings(room_js)
    valid, total = [], 0
    for pick in itertools.product(*[range(len(l["variants"])) for l in locks]):
        total += 1
        if checker.draw_is_valid([(l["key"], l["variants"][i]) for l, i in zip(locks, pick)], clues):
            valid.append(pick)
    return valid, total


def make_set(letter, pick, locks):
    return {"letter": letter, "pick": tuple(pick), "vars": [copy.deepcopy(l["variants"][i]) for l, i in zip(locks, pick)]}


def choose(checker, valid, locks, n, seed):
    """N VALID draws with every lock's answers distinct across them, or BuildError naming the most found.
    The VALID draws are shuffled by the seed, then searched in that order (depth first), so a seed gives one pack."""
    order = list(valid)
    random.Random(seed).shuffle(order)
    ans = {p: [frozenset(checker.flat(l["variants"][i]["answer"])) for l, i in zip(locks, p)] for p in order}
    chosen, best, budget = [], [], [200000]

    def fits(p):
        return all(not (ans[p][j] & ans[q][j]) for q in chosen for j in range(len(locks)))

    def search(start):
        nonlocal best
        if len(chosen) > len(best):
            best = list(chosen)
        if len(chosen) == n:
            return True
        for k in range(start, len(order)):
            budget[0] -= 1
            if budget[0] < 0:
                return False
            if fits(order[k]):
                chosen.append(order[k])
                if search(k + 1):
                    return True
                chosen.pop()
        return False

    if not search(0):
        raise BuildError("only %d joint draws can be VALID with every lock's answers distinct, fewer than the %d sets "
                         "asked for (%d VALID draws in all)" % (len(best), n, len(valid)))
    return [make_set(chr(ord("A") + i), p, locks) for i, p in enumerate(chosen)]


def check_sets(checker, room_js, locks, sets):
    """Problems with a choice of sets: a joint draw that is not VALID, or a lock whose answer repeats across sets."""
    clues = checker.clue_strings(room_js)
    out = []
    for s in sets:
        if not checker.draw_is_valid([(l["key"], v) for l, v in zip(locks, s["vars"])], clues):
            out.append("set %s: its joint draw is not VALID" % s["letter"])
    for j, l in enumerate(locks):
        for a, b in itertools.combinations(sets, 2):
            if checker.flat(a["vars"][j]["answer"]) & checker.flat(b["vars"][j]["answer"]):
                out.append("%s: sets %s and %s share an answer (%s)" % (l["id"], a["letter"], b["letter"],
                                                                        a["vars"][j]["answer"]))
    return out


def verify_sets(locks, sets):
    """(problems, number of values checked, number of answers checked): every value lockcheck recomputes, compared
    with the variant's own."""
    out, checked, answers = [], 0, 0
    for l in locks:
        if l["id"] not in lockcheck.RECOMPUTE:
            out.append("%s: no independent recomputation in tools/pack-generator/lockcheck.py" % l["id"])
    for s in sets:
        for l, v in zip(locks, s["vars"]):
            fn = lockcheck.RECOMPUTE.get(l["id"])
            if not fn:
                continue
            for k, want in fn(v).items():
                checked += 1
                answers += k == "answer"
                if v.get(k) != want:
                    out.append("set %s, %s: %s is %r, recomputed %r" % (s["letter"], l["id"], k, v.get(k), want))
    return out, checked, answers


# ---- filling -------------------------------------------------------------------------------------------------------

def js_string(v):
    """A token's value as engine.js writes it (String(v)): a whole float without its .0."""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


def filler(locks, s):
    t = {"%s.%s" % (l["key"], k): js_string(val) for l, v in zip(locks, s["vars"]) for k, val in v.items()}

    def fill(text):
        if text is None:
            return ""
        return re.sub(r"\{\{([\w.-]+)\}\}", lambda m: t.get(m.group(1), m.group(0)), str(text))
    return fill


def split_clue(clue):
    """(what is printed on the object: the clue's <b> part; the narration around it). One <b> part per clue."""
    parts = re.findall(r"<b>(.*?)</b>", clue, re.S)
    if len(parts) != 1:
        raise BuildError("a clue needs exactly one <b>...</b> part (the words on the object): %r" % clue[:80])
    return parts[0].strip(), re.sub(r"\s*<b>.*?</b>\s*", " ", clue, flags=re.S).strip()


# ---- the pages -----------------------------------------------------------------------------------------------------

CSS = """
@page { size: A4; margin: 0; }
@page landscape { size: A4 landscape; margin: 0; }
html, body { margin: 0; padding: 0; background: #fff; }
body { font-family: 'Outfit', sans-serif; color: #000; font-size: 10.5pt; line-height: 1.35;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; box-sizing: border-box; padding: 10mm 12mm 0; position: relative;
        overflow: hidden; break-after: page; display: flex; flex-direction: column; }
.page:last-child { break-after: auto; }
.page.landscape { page: landscape; width: 297mm; height: 210mm; }
table.score { table-layout: fixed; font-size: 9.5pt; }
table.score th, table.score td { padding: 1.2mm 1.5mm; vertical-align: middle; }
table.score th { text-align: center; line-height: 1.2; }
table.score tr.row td { height: 15mm; }
table.score td.set { text-align: center; font-size: 15pt; font-weight: 800; }
.box { display: inline-block; width: 4mm; height: 4mm; border: 0.8pt solid #000; margin: 0 0.6mm; vertical-align: middle; }
.box.big { width: 6mm; height: 6mm; }
td.boxes { text-align: center; white-space: nowrap; }
.rule { font-size: 9.5pt; margin-top: 2.5mm; }
.goal { font-weight: 700; margin: 2mm 0 3mm; }
.main { flex: 1 1 auto; height: 0; overflow: hidden; margin-bottom: 15mm; }
.foot { position: absolute; left: 12mm; right: 12mm; bottom: 5mm; border-top: 0.4pt solid #000; padding-top: 1.2mm;
        display: flex; justify-content: space-between; align-items: center; font-size: 7.5pt; letter-spacing: 0.02em; }
.foot .brand { display: flex; align-items: center; gap: 2mm; }
.foot .brand b { font-size: 8.5pt; font-weight: 700; letter-spacing: 0; }
.logo { display: inline-block; width: 6.6mm; height: 5.5mm; overflow: hidden; flex: none; }
.logo img { display: block; width: 22mm; height: 16.5mm; margin: -5.5mm 0 0 -7.7mm; filter: grayscale(1) contrast(1.4); }
.online { margin-top: 3mm; font-size: 9.5pt; }
.head { display: flex; align-items: center; justify-content: space-between; gap: 6mm; border-bottom: 1.4pt solid #000;
        padding-bottom: 2.5mm; margin-bottom: 4mm; flex: none; }
.head h1 { font-size: 17pt; line-height: 1.1; margin: 0; font-weight: 800; }
.head .sub { font-size: 10pt; font-weight: 500; margin-top: 0.8mm; }
.setbox { border: 2.2pt solid #000; border-radius: 2mm; padding: 1mm 4mm; font-size: 26pt; font-weight: 800;
          line-height: 1.1; white-space: nowrap; }
.draft { border: 1.4pt dashed #000; padding: 1mm 3mm; font-weight: 800; font-size: 11pt; white-space: nowrap; }
h2 { font-size: 12.5pt; margin: 3.5mm 0 1.2mm; font-weight: 700; }
p { margin: 0 0 2mm; }
ol, ul { margin: 0 0 2mm; padding-left: 6mm; }
li { margin-bottom: 0.8mm; }
blockquote { margin: 0 0 2mm; padding: 2mm 4mm; border-left: 2pt solid #000; }
.art { position: relative; }
.art img { display: block; width: 100%; height: auto; }
.lbl { position: absolute; display: flex; align-items: center; justify-content: center; overflow: hidden; }
.lbl > div { width: 100%; min-width: 0; text-align: center; line-height: 1.08; overflow-wrap: normal; word-break: keep-all; }
.lbl.label > div { font-family: 'PackLabel'; font-weight: 600; }
.lbl.hand > div { font-family: 'PackHand'; }
.lbl.light > div { color: #fff; }
.write { position: absolute; border: 0.8pt dashed #000; box-sizing: border-box; }
.cover-art { width: 150mm; margin: 0 auto 3mm; display: block; }
.team { margin: 3mm 0 2mm; font-size: 12pt; font-weight: 600; }
.team span { display: inline-block; width: 120mm; border-bottom: 0.8pt solid #000; }
.answers { display: grid; grid-template-columns: repeat(3, 1fr); gap: 5mm; }
.answers .cap { font-size: 9pt; line-height: 1.2; min-height: 11mm; }
.answers .cap b { display: block; font-size: 10pt; }
.evidence { display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 4mm 4mm; height: 100%; }
.card { border: 0.6pt solid #000; padding: 1.2mm; display: flex; flex-direction: column; overflow: hidden; }
.card .cap { margin-top: 1.5mm; font-size: 9.5pt; line-height: 1.3; }
.card .cap .name { font-weight: 700; font-size: 11pt; }
.card .cap .where { font-style: italic; }
.lock { margin-bottom: 4mm; }
.lock h2 { margin-top: 0; }
.lock .opens { font-size: 9.5pt; }
.work { height: 58mm; border: 0.8pt solid #000; margin-top: 1.5mm;
        background-image: linear-gradient(#bbb 0.3pt, transparent 0.3pt), linear-gradient(90deg, #bbb 0.3pt, transparent 0.3pt);
        background-size: 5mm 5mm; }
table { border-collapse: collapse; width: 100%; font-size: 10pt; }
th, td { border: 0.6pt solid #000; padding: 1.4mm 2mm; text-align: left; vertical-align: top; }
th { font-weight: 700; }
td.n { font-family: 'Outfit'; font-weight: 700; font-size: 12pt; }
.wrong { font-weight: 400; font-size: 9.5pt; }
.solution { margin-bottom: 2.2mm; font-size: 9.5pt; line-height: 1.3; break-inside: avoid; }
.solution b.set { font-size: 10.5pt; }
.hints { display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: repeat(3, 1fr); height: 100%; }
.hint { border: 0.8pt dashed #000; padding: 4mm; display: flex; flex-direction: column; }
.hint .which { font-size: 9pt; font-weight: 600; }
.hint .lockname { font-weight: 700; font-size: 11pt; margin-bottom: 3mm; }
.hint .text { font-size: 12pt; line-height: 1.35; }
.cert { text-align: center; }
.cert h1 { font-size: 40pt; margin: 6mm 0 4mm; font-weight: 800; }
.cert img { width: 170mm; display: block; margin: 0 auto 6mm; }
.cert .line { font-size: 14pt; margin: 6mm 0; }
.cert .line span { display: inline-block; width: 90mm; border-bottom: 0.8pt solid #000; }
"""

FIT_JS = """
async ([minPt]) => {
  for (const img of document.images) {
    await img.decode();
    if (!img.naturalWidth) throw new Error('image did not load: ' + img.src);
  }
  await document.fonts.ready;
  const loaded = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/"/g, ''));
  const out = {labels: [], loaded: [...new Set(loaded)]};
  for (const el of document.querySelectorAll('.lbl, .write')) {
    const img = el.parentElement.querySelector('img');
    const [x0, y0, x1, y1] = JSON.parse(el.dataset.box);
    const W = img.naturalWidth, H = img.naturalHeight;
    if (x1 > W || y1 > H) throw new Error('label box outside its image: ' + img.src);
    el.style.left = (x0 / W * 100) + '%'; el.style.top = (y0 / H * 100) + '%';
    el.style.width = ((x1 - x0) / W * 100) + '%'; el.style.height = ((y1 - y0) / H * 100) + '%';
    if (!el.classList.contains('lbl')) continue;
    const inner = el.firstElementChild;
    let pt, fits = false, lines = 1;
    for (const mode of ['nowrap', 'balance']) {         // one line if it fits at the minimum; else balanced lines
      inner.style.textWrap = mode;
      for (pt = +el.dataset.max; pt >= minPt; pt -= 0.5) {
        inner.style.fontSize = pt + 'pt';
        if (inner.scrollWidth <= el.clientWidth + 0.5 && inner.offsetHeight <= el.clientHeight + 0.5) { fits = true; break; }
      }
      if (fits) break;
    }
    lines = Math.round(inner.offsetHeight / (pt * 96 / 72 * 1.08));
    if (!fits) { pt = minPt; inner.style.fontSize = pt + 'pt'; }
    out.labels.push({id: el.dataset.id, set: el.dataset.set || '', pt, fits, lines, text: inner.textContent});
  }
  return out;
}
"""

AUDIT_JS = """
() => {
  const pages = [...document.querySelectorAll('.page')];
  const out = {pages: pages.length, studentPages: 0, overflow: [], setLetters: [], herringDigits: [], tokens: [], logo: [], logoMm: 0, text: []};
  const mm = px => px * 25.4 / 96;
  pages.forEach((p, i) => {
    out.text.push([p.dataset.kind, p.innerText]);
    const logos = p.querySelectorAll('.logo');
    const lg = p.querySelector('.foot .logo img');
    if (logos.length !== 1 || !lg || !lg.naturalWidth) out.logo.push((i + 1) + ': the logo is not in the footer once');
    else {
      const h = mm(p.querySelector('.foot').getBoundingClientRect().height);
      out.logoMm = Math.max(out.logoMm, h);
      if (h >= 12) out.logo.push((i + 1) + ': the footer is ' + h.toFixed(1) + ' mm high');
    }
    if (!/MaffsGames/.test(p.querySelector('.foot').textContent)) out.logo.push((i + 1) + ': no MaffsGames in the footer');
    const m = p.querySelector('.main');
    if (m.scrollHeight > m.clientHeight + 1 || m.scrollWidth > m.clientWidth + 1)
      out.overflow.push((i + 1) + ' ' + p.dataset.kind + ' ' + (p.dataset.set || '') + ' (' + m.scrollHeight + ' > ' + m.clientHeight + ')');
    if (p.dataset.set !== undefined) {
      out.studentPages++;
      const box = p.querySelector('.head .setbox');
      if (!box || box.textContent.trim() !== 'Set ' + p.dataset.set)
        out.setLetters.push((i + 1) + ' ' + p.dataset.kind + ' ' + p.dataset.set);
    }
  });
  document.querySelectorAll('.card.herring').forEach(c => {
    if (/[0-9]/.test(c.textContent)) out.herringDigits.push(c.dataset.id + ' in set ' + c.dataset.set + ': ' + c.textContent.trim());
  });
  if (document.body.textContent.includes('{{')) out.tokens.push('an unfilled {{token}} is on a page');
  return out;
}
"""


def esc(s):
    return html.escape(str(s), quote=True)


def art_block(img_path, box, cls, text=None, ident="", set_letter="", max_pt=MAX_PT):
    """An image with its label box laid over it (positions are set in the page from the image's natural size)."""
    inner = ""
    if cls == "write":
        inner = '<div class="write" data-box="%s"></div>' % esc(json.dumps(box))
    else:
        inner = ('<div class="lbl %s" data-box="%s" data-id="%s" data-set="%s" data-max="%s"><div>%s</div></div>'
                 % (cls, esc(json.dumps(box)), esc(ident), esc(set_letter), max_pt, text or ""))
    return '<div class="art"><img src="%s" alt="">%s</div>' % (img_path.as_uri(), inner)


def page(kind, body, title, sub="", set_letter=None, badge="", landscape=False):
    attrs = 'data-kind="%s"' % kind + (' data-set="%s"' % set_letter if set_letter else "")
    right = ('<div class="setbox">Set %s</div>' % set_letter) if set_letter else badge
    return ('<section class="page%s" %s><div class="head"><div><h1>%s</h1>%s</div>%s</div>'
            '<div class="main">%s</div><div class="foot">{{FOOT}}</div></section>'
            % (" landscape" if landscape else "", attrs, title, ('<div class="sub">%s</div>' % sub) if sub else "", right, body))


WRONG_BOXES = 5           # wrong-answer boxes per lock on the score sheet (Amendment 3)
SCORE_ROWS = 8            # rows a score-sheet page holds; more sets flow onto another page


def score_sheet(locks, sets):
    """The score sheet's tables (Amendment 3), one per page: a row per set, its letter printed; a column group per lock
    (Opened: one tick box; Wrong answers: WRONG_BOXES boxes); then finishing time, penalty and total time."""
    groups = "".join("<th colspan='2' data-lock='%s'>Lock %d<br><span class='wrong'>%s</span></th>" % (l["id"], i + 1, l["name"])
                     for i, l in enumerate(locks))
    subs = "".join("<th>Opened</th><th>Wrong answers</th>" for _ in locks)
    cols = ("<colgroup><col style='width:auto'><col style='width:12mm'>%s<col style='width:22mm'><col style='width:20mm'>"
            "<col style='width:20mm'></colgroup>" % "".join("<col style='width:15mm'><col style='width:%dmm'>"
                                                            % (WRONG_BOXES * 5.4 + 3) for _ in locks))
    head = ("<tr><th rowspan='2'>Team name</th><th rowspan='2'>Set</th>%s<th rowspan='2'>Finishing time</th>"
            "<th rowspan='2'>Penalty (minutes)</th><th rowspan='2'>Total time</th></tr><tr>%s</tr>" % (groups, subs))
    tables = []
    for k in range(0, len(sets), SCORE_ROWS):
        rows = "".join("<tr class='row' data-set='%s'><td></td><td class='set'>%s</td>%s<td></td><td></td><td></td></tr>"
                       % (s["letter"], s["letter"], "".join(
                           "<td class='boxes'><span class='box big' data-lock='%s' data-box='opened'></span></td>"
                           "<td class='boxes'>%s</td>" % (l["id"], "".join(
                               "<span class='box' data-lock='%s' data-box='wrong'></span>" % l["id"]
                               for _ in range(WRONG_BOXES))) for l in locks))
                       for s in sets[k:k + SCORE_ROWS])
        tables.append("<table class='score'>%s%s%s</table>" % (cols, head, rows))
    return tables


def check_score_sheet(tables, locks, sets):
    """Problems with the score sheet: every set has exactly one row, no row is for a set that is not in the pack, each
    lock has one column group, and every row holds one Opened box and WRONG_BOXES wrong-answer boxes per lock."""
    out, seen = [], []
    for t in tables:
        for lid in [l["id"] for l in locks]:
            if t.count("<th colspan='2' data-lock='%s'>" % lid) != 1:
                out.append("lock %s does not have one column group" % lid)
        for letter, row in re.findall(r"<tr class='row' data-set='([A-Z])'>(.*?)</tr>", t, re.S):
            seen.append(letter)
            for l in locks:
                o = row.count("data-lock='%s' data-box='opened'" % l["id"])
                w = row.count("data-lock='%s' data-box='wrong'" % l["id"])
                if (o, w) != (1, WRONG_BOXES):
                    out.append("set %s, %s: %d Opened and %d wrong-answer boxes" % (letter, l["id"], o, w))
    want = [s["letter"] for s in sets]
    for letter in want:
        if seen.count(letter) != 1:
            out.append("the score sheet has %d rows for set %s" % (seen.count(letter), letter))
    for letter in sorted(set(seen) - set(want)):
        out.append("the score sheet has a row for set %s, which is not in the pack" % letter)
    return out


def build_html(slug, room, teach, locks, sets, cfg, seed, built, url):
    rdir = HERE / "rooms" / slug
    images = cfg["images"]
    by_obj = {im["object"]: im for im in images if im["role"] in ("clue", "herring")}
    by_lock = {im["lock"]: im for im in images if im["role"] == "answer"}
    for o in room["objects"]:
        if o["id"] not in by_obj:
            raise BuildError("config has no image for object %r" % o["id"])
        role = by_obj[o["id"]]["role"]
        if (role == "clue") != bool(o.get("clue")):
            raise BuildError("config calls %r a %s, but room.js %s a clue" % (o["id"], role,
                                                                            "gives it" if o.get("clue") else "gives it no"))
    for l in locks:
        if l["id"] not in by_lock:
            raise BuildError("config has no answer image for lock %r" % l["id"])
    for im in images:
        if im["role"] == "herring":
            words = im.get("text", "")
            if re.search(r"\d", words):
                raise BuildError("the words printed on red herring %r contain a digit: %r" % (im["object"], words))
            flavour = text_of(next(o for o in room["objects"] if o["id"] == im["object"]).get("flavour"))
            if words and re.sub(r"[^\w ]", "", words).lower() not in re.sub(r"[^\w ]", "", flavour).lower():
                raise BuildError("the words printed on %r (%r) are not in its flavour text in room.js" % (im["object"], words))

    art = room.get("art")
    scene = ROOT / "docs" / "art" / ("%s-scene.webp" % art) if art else None
    win = ROOT / "docs" / "art" / ("%s-win.webp" % art) if art else None
    title = room["title"]
    letters = [s["letter"] for s in sets]
    fill_a = filler(locks, sets[0])
    meta = teach.get("lockMeta") or [{}] * len(locks)
    pages = []

    # a. teacher notes (DRAFT)
    first_note = re.search(r"<p[^>]*>(.*?)</p>", teach.get("notes", ""), re.S)
    bank_minutes = sum(m.get("minutes", 0) for m in meta)
    topics = "".join("<li><b>Lock %d, %s:</b> %s%s</li>" % (
        i + 1, l["name"], esc(m.get("topic", "")), (" (about %d min)" % m["minutes"]) if m.get("minutes") else "")
        for i, (l, m) in enumerate(zip(locks, meta)))
    has_tokens = any("{{" in (room.get(k) or "") for k in ("hook", "brief", "stakes"))
    script = ("<blockquote><p>%s</p><p>%s</p><p>%s</p><p>Every team has a different set, so your numbers are not "
              "your neighbours&rsquo;. Bring each answer to me as soon as you have it. Every wrong answer adds a "
              "minute to your time. Lowest total time wins.</p></blockquote>" % (fill_a(room["hook"]),
                                                                                fill_a(room["brief"]),
                                                                                fill_a(room["stakes"])))
    if has_tokens:
        script = "<p>Read the hook and brief from any team&rsquo;s cover sheet, then:</p>" + script
    body = (
        "<h2>What is in the pack</h2>"
        "<p>%d sets, %s to %s: the same room with different numbers, so neighbouring teams cannot share answers. Each "
        "set is a cover sheet, two evidence pages and a locks page. Also here: the score sheet, the answer key, hint "
        "cards and a certificate.</p><ul>%s</ul>%s"
        "<h2>Set-up (under two minutes)</h2><ol>"
        "<li>Print one set per team, each team a different letter.</li>"
        "<li>Hand each team its set face down, cover sheet on top.</li>"
        "<li>Keep the score sheet and the answer key with you, and a timer that counts up.</li>"
        "<li>Optional: cut out the hint cards and keep them at the front.</li></ol>"
        "<h2>Read this out</h2>%s"
        "<h2>How checking works</h2>"
        "<p>Use one timer for the whole class, counting up, and start it when every team has its set. A team brings "
        "each lock&rsquo;s answer to you as they go; check it against their set&rsquo;s row in the answer key. "
        "<b>Right:</b> tick that lock&rsquo;s Opened box on the score sheet. <b>Wrong:</b> check one of that "
        "lock&rsquo;s wrong-answer boxes and say &ldquo;not yet&rdquo;, with no explanation.</p>"
        "<p>When a team&rsquo;s last lock is ticked, write the time on the timer as its finishing time. "
        "<b>Total time = finishing time + 1 minute per wrong answer. Lowest total time wins</b> (the certificate is "
        "at the back). The key also gives each lock&rsquo;s common wrong answer and the misconception behind it, for "
        "the debrief.</p>"
        "<h2>Timing</h2><p>How long to run it is your choice. The online room gives %d minutes%s.</p>"
        "<p class='online'><b>Play this room free online: %s</b></p>"
        % (len(sets), letters[0], letters[-1], topics, ("<p>%s</p>" % first_note.group(1)) if first_note else "",
           script, room.get("minutes", 15),
           ("; the locks&rsquo; own times add up to about %d minutes" % bank_minutes) if bank_minutes else "",
           esc(url)))
    pages.append(page("teacher", body, "%s: teacher notes" % title, "Group race pack, %d sets" % len(sets),
                      badge='<div class="draft">DRAFT: Jon&rsquo;s wording</div>'))

    # a2. score sheet (Amendment 3): landscape, one row per set, a column group per lock
    tables = score_sheet(locks, sets)
    for k, t in enumerate(tables):
        rule = ("<p class='rule'>Right: tick Opened. Wrong: check one box and say &ldquo;not yet&rdquo;. Finishing time: "
                "the timer when the last lock is ticked. Penalty: 1 minute per checked box. "
                "<b>Total time = finishing time + penalty. Lowest total time wins.</b></p>")
        pages.append(page("score", t + rule, "%s: score sheet" % title,
                          "One timer for the whole class, counting up" + (", page %d of %d" % (k + 1, len(tables))
                                                                         if len(tables) > 1 else ""), landscape=True))

    # b. answer key: the table, then the worked solutions
    head = "".join("<th>%s<br><span class='wrong'>%s</span></th>" % (l["name"], esc(m.get("topic", "")))
                   for l, m in zip(locks, meta))
    rows = "".join("<tr><th>Set %s</th>%s</tr>" % (s["letter"], "".join(
        "<td class='n'>%s <span class='wrong'>(common wrong answer %s)</span></td>"
        % (js_string(v["answer"]), js_string(v["miss"]) if v.get("miss") is not None else "none")
        for v in s["vars"])) for s in sets)
    legend = "".join("<li><b>%s:</b> %s %s</li>" % (l["name"], l.get("missTitle", ""), l.get("missSays", ""))
                     for l in locks)
    pages.append(page("key", "<table><tr><th></th>%s</tr>%s</table><h2>The common wrong answers</h2><ul>%s</ul>"
                      % (head, rows, legend), "%s: answer key" % title, "Check each answer against its set's row"))
    sols = ""
    for s in sets:
        f = filler(locks, s)
        sols += "<div class='solution'><b class='set'>Set %s</b><br>%s</div>" % (
            s["letter"], "<br>".join("<b>%s:</b> %s" % (l["name"], f(l["solve"])) for l in locks))
    pages.append(page("solutions", sols, "%s: worked solutions" % title, "One line per lock, for each set"))

    # c. per set: cover, evidence (two pages of four), locks
    for s in sets:
        f = filler(locks, s)
        L = s["letter"]
        answers = ""
        for l in locks:
            im = by_lock[l["id"]]
            answers += ("<div><div class='cap'><b>%s</b>%s</div>%s</div>"
                        % (l["name"], esc(text_of((l.get("instrument") or {}).get("label", ""))),
                           art_block(rdir / im["file"], im["label_box"], "write")))
        cover = ("%s<p>%s</p><p>%s</p><p><b>%s</b></p>"
                 "<div class='team'>Team name: <span></span></div>"
                 "<h2>Your codes: write each in its box</h2>"
                 "<p class='goal'>Bring each answer to your teacher. Every wrong answer adds a minute to your time.</p>"
                 "<div class='answers'>%s</div><p class='online'>Play this room free online: %s</p>"
                 % (('<img class="cover-art" src="%s" alt="">' % scene.as_uri()) if scene and scene.is_file() else "",
                    f(room["hook"]), f(room["brief"]), f(room["stakes"]), answers, esc(url)))
        pages.append(page("cover", cover, title, "Group race: cover sheet", set_letter=L))
        cards = []
        for o in room["objects"]:
            im = by_obj[o["id"]]
            font = im.get("font", "label") + (" light" if im.get("ink") == "light" else "")
            if o.get("clue"):
                printed, narration = split_clue(f(o["clue"]))
                cls, extra = "card", narration
            else:
                printed, cls, extra = esc(im.get("text", "")), "card herring", f(o.get("flavour"))
            cards.append("<div class='%s' data-id='%s' data-set='%s'>%s<div class='cap'><span class='name'>%s</span>"
                         " &middot; <span class='where'>%s</span><br>%s</div></div>"
                         % (cls, o["id"], L, art_block(rdir / im["file"], im["label_box"], font, printed, o["id"], L,
                                                       im.get("max_pt", MAX_PT)),
                            o["name"], o.get("where", ""), extra))
        per = 4
        npages = (len(cards) + per - 1) // per
        for k in range(npages):
            pages.append(page("evidence", "<div class='evidence'>%s</div>" % "".join(cards[k * per:(k + 1) * per]),
                              title, "Evidence, page %d of %d" % (k + 1, npages), set_letter=L))
        lk = "".join("<div class='lock'><h2>Lock %d: %s</h2><p>%s</p><div class='opens'>Opens at: <b>%s</b></div>"
                     "<div class='work'></div></div>"
                     % (i + 1, l["name"], f(l["brief"]), esc(text_of((l.get("instrument") or {}).get("label", ""))))
                     for i, l in enumerate(locks))
        pages.append(page("locks", lk, title, "The locks: working space", set_letter=L))

    # d. hint cards (one page for all sets unless a hint uses a set's figures) and the certificate
    hint_sets = sets if any("{{" in h for l in locks for h in l.get("hints", [])) else [None]
    for s in hint_sets:
        f = filler(locks, s) if s else filler(locks, sets[0])
        cards = "".join("<div class='hint'><div class='which'>Hint %d of %d</div><div class='lockname'>%s</div>"
                        "<div class='text'>%s</div></div>" % (k + 1, len(l["hints"]), l["name"], f(h))
                        for k in range(max(len(l.get("hints", [])) for l in locks))
                        for l in locks for h in [l["hints"][k] if k < len(l.get("hints", [])) else ""])
        sub = "Cut out; hand one over when a team asks" + ("" if s else ". The same for every set")
        pages.append(page("hints", "<div class='hints'>%s</div>" % cards, "%s: hint cards" % title, sub,
                          set_letter=s["letter"] if s else None))
    cert = ("<div class='cert'><h1>%s</h1>%s<p class='line'>%s</p><p class='line'>Team <span></span></p>"
            "<p class='line'>Set ______ &nbsp; Date <span style='width:50mm'></span></p></div>"
            % (esc(cfg.get("certificate_title", "Room escaped")),
               ('<img src="%s" alt="">' % win.as_uri()) if win and win.is_file() else "", fill_a(room.get("win", ""))))
    pages.append(page("certificate", cert, title, "Certificate"))

    fonts = "".join("@font-face { font-family: '%s'; src: url('%s'); font-weight: %s; }"
                    % (fam, (HERE / "fonts" / fn).as_uri(), w) for fam, fn, w, _ in FONTS.values())
    foot = ('<span class="brand"><span class="logo"><img src="%s" alt=""></span><b>MaffsGames</b>'
            '<span>%s &middot; pack v%s &middot; seed %s &middot; built %s</span></span>'
            % (LOGO.as_uri(), slug, esc(cfg.get("pack_version", "?")), seed, built))
    doc = "".join(p.replace("{{FOOT}}", "%s<span>page %d of %d</span>" % (foot, i + 1, len(pages)))
                  for i, p in enumerate(pages))
    return ("<!doctype html><html lang='en'><head><meta charset='utf-8'><title>%s pack</title>"
            "<link rel='stylesheet' href='%s'><style>%s%s</style></head><body>%s</body></html>"
            % (esc(title), GOOGLE_FONTS, fonts, CSS, doc)), len(pages)


def pdf_page_count(path):
    return len(re.findall(rb"/Type\s*/Page[^s]", path.read_bytes()))


def ignored_by_git(path):
    r = subprocess.run(["git", "-C", str(ROOT), "check-ignore", "-q", str(path)], capture_output=True)
    return r.returncode == 0


# ---- the build -----------------------------------------------------------------------------------------------------

def prepare(slug, n, seed, page):
    checker = load_checker()
    cfg = load_config(slug)
    room, teach, room_js = read_room(page, slug)
    locks = room_locks(room, slug)
    n = n or cfg.get("sets", 7)
    seed = cfg.get("seed", 1) if seed is None else seed
    valid, total = valid_picks(checker, room_js, locks)
    sets = choose(checker, valid, locks, n, seed)
    return checker, cfg, room, teach, room_js, locks, sets, valid, total, n, seed


def build(slug, n, seed):
    from playwright.sync_api import sync_playwright
    out = OUT_DIR / ("%s-pack.pdf" % slug)
    if not ignored_by_git(out):
        raise BuildError("%s is not ignored by git: refusing to write the product where it could be committed"
                         % out.relative_to(ROOT))
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            ctx = offline_context(browser)
            pg = ctx.new_page()
            checker, cfg, room, teach, room_js, locks, sets, valid, total, n, seed = prepare(slug, n, seed, pg)
            print("%s: %d of %d joint draws VALID; %d sets chosen (seed %s):" % (slug, len(valid), total, n, seed))
            for s in sets:
                print("  Set %s  variants %s  answers %s" % (s["letter"], list(s["pick"]),
                                                          [js_string(v["answer"]) for v in s["vars"]]))
            problems = check_sets(checker, room_js, locks, sets)
            vp, checked, answers = verify_sets(locks, sets)
            if problems or vp:
                raise BuildError("the chosen sets fail:\n  " + "\n  ".join(problems + vp))
            print("every joint draw VALID; every lock's answers distinct across the %d sets" % n)
            print("verification: %d values recomputed independently (%d answers), all agree" % (checked, answers))
            built = datetime.date.today().isoformat()
            url = room_url(slug)
            if not LOGO.is_file():
                raise BuildError("the logo %s is missing" % LOGO.relative_to(ROOT).as_posix())
            doc, npages = build_html(slug, room, teach, locks, sets, cfg, seed, built, url)
            sheet = check_score_sheet(score_sheet(locks, sets), locks, sets)
            if sheet:
                raise BuildError("the score sheet fails:\n  " + "\n  ".join(sheet))
            print("score sheet: one row per set (%d), one column group per lock (%d)" % (len(sets), len(locks)))
            with tempfile.TemporaryDirectory() as tmp:
                src = pathlib.Path(tmp) / ("%s-pack.html" % slug)
                src.write_text(doc, encoding="utf-8")
                pg.goto(src.as_uri())
                fit = pg.evaluate(FIT_JS, [MIN_PT])
                for fam in ["Outfit"] + [f[0] for f in FONTS.values()]:
                    if fam not in fit["loaded"]:
                        raise BuildError("font %s did not load (loaded: %s)" % (fam, fit["loaded"]))
                small = [l for l in fit["labels"] if not l["fits"]]
                if small:
                    raise BuildError("label text does not fit its box at %d pt:\n  " % MIN_PT + "\n  ".join(
                        "%s (set %s): %s" % (l["id"], l["set"], l["text"]) for l in small))
                audit = pg.evaluate(AUDIT_JS)
                printed = check_printed_text([(k, t) for k, t in audit["text"]], url)
                if printed:
                    raise BuildError("what the pages print fails Amendment 1:\n  " + "\n  ".join(printed))
                bad = audit["overflow"] + audit["setLetters"] + audit["herringDigits"] + audit["tokens"] + audit["logo"]
                if bad or audit["pages"] != npages:
                    raise BuildError("the pages fail their checks:\n  overflow: %s\n  set letter: %s\n  digits on a red "
                                     "herring: %s\n  logo: %s\n  %s" % (audit["overflow"], audit["setLetters"],
                                                                        audit["herringDigits"], audit["logo"], audit["tokens"]))
                print("printed URL %s resolves to a live room page; on every cover and the teacher notes; "
                      "logo and name in every footer (at most %.1f mm high)" % (url, audit["logoMm"]))
                by_id = {}
                for l in fit["labels"]:
                    by_id.setdefault(l["id"], []).append((l["pt"], l["lines"]))
                print("labels fitted (smallest size across sets, at least %d pt):" % MIN_PT)
                for k, v in by_id.items():
                    print("  %-18s %4.1f pt  %s" % (k, min(x[0] for x in v),
                                                   "one line" if all(x[1] == 1 for x in v) else "up to %d lines" % max(x[1] for x in v)))
                print("set letter on all %d student pages; no digit on any red herring; no unfilled token"
                      % audit["studentPages"])
                OUT_DIR.mkdir(exist_ok=True)
                pg.pdf(path=str(out), format="A4", print_background=True, prefer_css_page_size=True)
            got = pdf_page_count(out)
            if got != npages:
                out.unlink()
                raise BuildError("the PDF has %d pages, but %d were built: a page overflowed" % (got, npages))
            print("wrote %s: %d pages, %d KB" % (out.relative_to(ROOT), got, out.stat().st_size // 1024))
        finally:
            browser.close()


# ---- the selftest --------------------------------------------------------------------------------------------------

def selftest():
    """Every room with a config: its chosen sets must pass; then three faults are planted in the first room's sets,
    through the same checks the build uses, and each must be caught. Builds no PDF."""
    from playwright.sync_api import sync_playwright
    rooms = sorted(p.parent.name for p in (HERE / "rooms").glob("*/config.json"))
    failures, caught = [], 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            pg = offline_context(browser).new_page()
            first = None
            for slug in rooms:
                checker, cfg, room, teach, room_js, locks, sets, valid, total, n, seed = prepare(slug, None, None, pg)
                probs = (check_sets(checker, room_js, locks, sets) + verify_sets(locks, sets)[0]
                         + check_score_sheet(score_sheet(locks, sets), locks, sets))
                print("%s: %d sets chosen from %d VALID draws; %s" % (slug, n, len(valid), "OK" if not probs else probs))
                failures += probs
                first = first or (checker, room_js, locks, sets, valid)
        finally:
            browser.close()
    checker, room_js, locks, sets, valid = first

    def plant_duplicate():
        s = copy.deepcopy(sets)
        if s[1]["vars"][0] == s[0]["vars"][0]:
            raise pc.StalePlant("duplicate answer", "sets A and B already share lock 1's variant")
        s[1]["vars"][0] = copy.deepcopy(s[0]["vars"][0])
        return [x for x in check_sets(checker, room_js, locks, s) if "share an answer" in x]

    def plant_invalid():
        clues = checker.clue_strings(room_js)
        bad = next((pick for pick in itertools.product(*[range(len(l["variants"])) for l in locks])
                    if not checker.draw_is_valid([(l["key"], l["variants"][i]) for l, i in zip(locks, pick)], clues)), None)
        if bad is None:
            raise pc.StalePlant("invalid joint draw", "every joint draw of this room is VALID")
        s = copy.deepcopy(sets)
        s[0] = make_set("A", bad, locks)
        return [x for x in check_sets(checker, room_js, locks, s) if "not VALID" in x]

    def plant_wrong_answer():
        s = copy.deepcopy(sets)
        s[2]["vars"][1]["answer"] = s[2]["vars"][1]["answer"] + 1
        return [x for x in verify_sets(locks, s)[0] if ": answer is " in x]

    def plant_bad_url():
        url = room_url(rooms[0])
        bad = pc.apply_plant(url, "/escape-rooms/%s/" % rooms[0], "/escape-rooms/no-such-room/", name="a dead room URL")
        text = "Play this room free online: " + bad
        return [x for x in check_printed_text([("cover", text)], url) if "does not exist" in x]

    def plant_missing_row():
        tables = score_sheet(locks, sets)
        row = re.search(r"<tr class='row' data-set='C'>.*?</tr>", tables[0], re.S)
        if not row:
            raise pc.StalePlant("a missing score-sheet row", "the score sheet has no row for set C")
        tables[0] = pc.apply_plant(tables[0], row.group(0), "", name="a missing score-sheet row")
        return [x for x in check_score_sheet(tables, locks, sets) if "0 rows for set C" in x]

    plants = (("a duplicate answer across sets", plant_duplicate),
              ("an invalid joint draw", plant_invalid),
              ("a wrong recomputed answer", plant_wrong_answer),
              ("a printed URL with no room page", plant_bad_url),
              ("a missing score-sheet row", plant_missing_row))
    for name, fn in plants:
        found, err = [], None
        try:
            found = fn()
        except pc.StalePlant as e:
            err = e
            failures.append(str(e))
        except Exception as e:          # an error is never a catch
            err = e
            failures.append("plant %s raised %r" % (name, e))
        if pc.is_caught(found, err):
            caught += 1
            print("CAUGHT %s: %s" % (name, found[0]))
        elif err is None:
            failures.append("MISSED %s" % name)
            print("MISSED %s" % name)
    print("selftest: %d/%d plants caught; %d room(s) checked; no PDF built" % (caught, len(plants), len(rooms)))
    if failures or caught != len(plants):
        print("FAIL:\n  " + "\n  ".join(failures))
        return 1
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("room", nargs="?", help="the room's slug, e.g. kiln-disaster")
    ap.add_argument("--sets", type=int, help="how many sets (default: the room's config)")
    ap.add_argument("--seed", type=int, help="the selection seed (default: the room's config)")
    ap.add_argument("--selftest", action="store_true", help="planted faults; builds no PDF")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        if a.selftest:
            return selftest()
        if not a.room:
            ap.error("name a room, e.g. kiln-disaster")
        if a.sets is not None and not 1 <= a.sets <= 26:
            ap.error("--sets is 1 to 26 (one letter a set)")
        build(a.room, a.sets, a.seed)
        return 0
    except BuildError as e:
        print("BUILD FAILED: %s" % e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
