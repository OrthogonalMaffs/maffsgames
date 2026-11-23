#!/usr/bin/env python3
# ci-line: When will I use this? (the pages are build-uses.py's output exactly; every source https and public; every worked step with = recomputed, or marked noCheck with a reason; Practise it names live games only; the 15 Skills England routes; in Chromium no page scrolls sideways at 320x568 or 390x844, normal or Aa, and its KaTeX renders with no .katex-error; every scenario has a question ending ?, an Inside tag and a formula or null; planted faults) | --selftest && --check
# ci-deps: data/uses.json when-will-i-use-this/ scripts/build-uses.py data/games.json .claude/rules/game-roster.md sitemap.xml index.html parents/guide.css parents/guide.js schools/assets/opendyslexic.css scripts/katex_page_common.py
"""WHEN-WILL-I-USE-THIS (Jon, spec 10 Nov 2026, build 22 Nov 2026): the "When will I use this?" section, held to its data.

    python -X utf8 scripts/check-uses.py --check      # CI: the static rules, then the pages in Chromium
    python -X utf8 scripts/check-uses.py --static     # the static rules only (no browser)
    python -X utf8 scripts/check-uses.py --selftest   # every planted fault must be caught

data/uses.json is the one source; scripts/build-uses.py writes every page from it. This check fails if:
  (a) a page under when-will-i-use-this/, or sitemap.xml's block, differs from what build-uses.py writes, or a page there
      is one it no longer writes (a hand edit, or a data change without a rebuild);
  (b) a scenario has no source, or a source whose URL is not https, whose title is empty, or whose type is not "public"
      (the only type in v1: a contributor type needs Jon's ruling on consent and naming);
  (c) a worked step's "=" does not hold. For each "=" in a step: the left side is the text after the last ": ", ". "
      or "; " in front of it, less any leading words (or, inside a chain a = b = c, the whole middle part). If that is
      an arithmetic expression (numbers as written, "30 000" included; % after a number on the left divides by 100;
      £; + − × ÷ and brackets), it is recomputed exactly and must equal the right side within half a unit of the right
      side's last decimal place. The right side is the whole middle part of a chain when that is an expression, or else
      the number it starts with, as written (a unit or a % after it is not read). A left side with no digits ("Developer
      = 40 × 2") is a label, not a claim. A step none of whose "=" signs could be recomputed, or with any "=" whose left
      side has digits but is not an expression ("3% of 230", "30 000 m²"), cannot be read: it fails unless the data
      marks it {"text": ..., "noCheck": "<one-line reason>"}, and the "=" signs it can read are still recomputed. A
      noCheck on a step the check reads in full is stale and fails. No step is skipped silently: the run prints how
      many steps it checked and lists every step it could not read, by scenario id;
  (d) a "Practise it" link (any /games/<slug>/ link in the section) names a game that is not live (a numbered roster
      row outside the Unlisted and Withdrawn sections, listed in data/games.json), or a topic matches no live game;
  (e) a scenario's route is not one of the 15 routes, or the routes are not Skills England's 15, by exact name;
  (f) in Chromium, any page scrolls sideways at 320x568 or 390x844, with the Aa toggle off or on, or shows KaTeX
      source it did not render, or throws.
WWIUT-STAND-OUT (22 Nov 2026) adds: every scenario's headline sum recomputes as a step does and reads in full; every
route colour gives white text 4.5:1 or better, is at least delta E 15 from every other and 25 from the portal's teal;
every job card's anchor on the hub is a scenario on its topic page; the hub never links to itself; and in Chromium the
text on every tile, chip and route header measures 4.5:1 or better against the colour behind it.
WWIUT-BATCH-1-2 (22 Nov 2026) adds: every scenario has a tier, "F", "H" or "L4" (a Higher or Level 4 card's tag measures
4.5:1 in Chromium too); the home page strip's "N real jobs" (index.html, between build-uses.py's COUNT_BEGIN and
COUNT_END) is the number of scenarios; and the reader in (c) also reads "1,000", "1/16", "½", √ of a number or a
bracket, superscript powers, sin, cos and tan in degrees and their inverses (giving degrees), "°" after a number, and a
right side that is an expression ("3² + 4² = 5²", exactly). The 14 scenarios before it read exactly as they did.
WWIUT-CARD-FORMAT (23 Nov 2026) adds: every scenario has a non-empty "question" ending in "?", a non-empty "inside",
"formula" a non-empty LaTeX string or null (the run reports how many are null), and "formulaNote", where given, a
non-empty string; and in Chromium any .katex-error on any page fails, naming the page, the source and KaTeX's message
(the pages render with throwOnError:false, so a LaTeX mistake would otherwise show as red source and pass).
Also: ids unique, every topic known, exampleFigures true exactly when the wording says "(example figure)" or
"(example figures)", and every parent guide named is a page in parents/.

Not in CI: scripts/check-uses-links.py --live fetches every source URL (external sites are flaky).
"""
import argparse, copy, importlib.util, json, math, mimetypes, os, pathlib, re, shutil, sys, tempfile
from fractions import Fraction
from urllib.parse import unquote, urlsplit

BASE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "scripts"))
import plant_common as pc  # noqa: E402

_spec = importlib.util.spec_from_file_location("build_uses", BASE / "scripts" / "build-uses.py")
bu = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bu)

ROUTES = [
    "Agriculture, environmental and animal care", "Business and administration", "Care services",
    "Catering and hospitality", "Construction and the built environment", "Creative and design", "Digital",
    "Education and childcare", "Engineering and manufacturing", "Hair and beauty", "Health and science",
    "Legal, finance and accounting", "Protective services", "Sales, marketing and procurement", "Transport and logistics",
]
SIZES = [(320, 568), (390, 844)]
ORIGIN = "http://uses.test"
EXAMPLE = re.compile(r"\(example figures?\)")
GAME_LINK = re.compile(r'href="/games/([a-z0-9-]+)/')


# ---------------------------------------------------------------- (c) the arithmetic

# Numbers as written: "30 000" and "1,047.50" (thousands), "12.5", a fraction "1/16" (digits/digits, no spaces) and "½".
# WWIUT-BATCH-1-2 (22 Nov 2026) extends the reader, in this one place: commas in thousands, "a/b", "½", √ (of a number
# or a bracket), superscript powers (² ³ ⁴ ⁶ ...), sin, cos and tan (in degrees) and sin⁻¹, cos⁻¹, tan⁻¹ (giving degrees),
# "°" after a number (a unit: no effect), and a right side that is an expression ("3² + 4² = 5²").
NUM = r"\d{1,3}(?:,\d{3})+(?![\d,])(?:\.\d+)?|\d{1,3}(?: \d{3})+(?!\d)|\d+(?:\.\d+)?"
SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"
DIGITISH = "½" + SUP   # count as digits: a left side holding one is a claim, never a label
TOKEN = re.compile(r"\s*(?:(£?)(\d+/\d+(?![\d./])|" + NUM + r"|½)(%?)|(√)|(sin|cos|tan)(⁻¹)?(?![a-z])|([" + SUP
                   + r"]+)|(°)|([+−×÷()-]))")
FUNCS = {"sin": math.sin, "cos": math.cos, "tan": math.tan}
INVERSE = {"sin": math.asin, "cos": math.acos, "tan": math.atan}


def _number(raw):
    if raw == "½":
        return Fraction(1, 2)
    if "/" in raw:
        a, b = raw.split("/")
        return Fraction(int(a), int(b)) if int(b) else None
    return Fraction(raw.replace(" ", "").replace(",", ""))


def scan(s, right=False):
    """([(kind, value, raw number or None)], whole) for s: the tokens read from its start, and whether they cover all of
    it. On a right side (right=True) a % after a number is a unit and is not read, as before."""
    s, pos, out = s.strip(), 0, []
    while pos < len(s):
        m = TOKEN.match(s, pos)
        if not m:
            return out, False
        if m.group(2):
            v = _number(m.group(2))
            if v is None:
                return out, False
            out.append(("n", v / 100 if m.group(3) and not right else v, m.group(2)))
        elif m.group(4):
            out.append(("sqrt", None, None))
        elif m.group(5):
            out.append(("fn", m.group(5) + ("-1" if m.group(6) else ""), None))
        elif m.group(7):
            out.append(("pow", int("".join(str(SUP.index(c)) for c in m.group(7))), None))
        elif m.group(8):
            out.append(("deg", None, None))
        else:
            out.append(("op", m.group(9).replace("-", "−"), None))
        pos = m.end()
        while pos < len(s) and s[pos] == " ":
            pos += 1
    return out, True


def tokens(s):
    """[(kind, value)] for an arithmetic expression, or None if s is not one."""
    toks, whole = scan(s)
    return [(k, v) for k, v, _ in toks] if whole and any(k == "n" for k, _, _ in toks) else None


def _sqrt(x):
    """√x, exact when x is the square of a fraction."""
    if x < 0:
        raise ValueError("square root of a negative number")
    if isinstance(x, Fraction):
        a, b = math.isqrt(x.numerator), math.isqrt(x.denominator)
        if a * a == x.numerator and b * b == x.denominator:
            return Fraction(a, b)
    return math.sqrt(x)


def _apply(fn, x):
    if fn.endswith("-1"):
        if fn != "tan-1" and not -1 <= x <= 1:
            raise ValueError("inverse sine or cosine outside -1 to 1")
        return math.degrees(INVERSE[fn[:-2]](float(x)))
    return FUNCS[fn](math.radians(float(x)))


def evaluate(toks):
    """The value of a token list (a Fraction when exact, else a float), or None if it does not parse. Grammar:
    expr = term (+ − term)*; term = unary (× ÷ unary)*; unary = − unary | power; power = primary superscript*;
    primary = number °? | ( expr ) | √ primary | sin/cos/tan[⁻¹] primary."""
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else (None, None)

    def take():
        pos[0] += 1
        return toks[pos[0] - 1]

    def primary():
        k, v = peek()
        if k == "op" and v == "(":
            take()
            x = expr()
            if peek() != ("op", ")"):
                raise ValueError("unclosed bracket")
            take()
            return x
        if k == "sqrt":
            take()
            return _sqrt(primary())
        if k == "fn":
            take()
            return _apply(v, primary())
        if k == "n":
            x = take()[1]
            if peek()[0] == "deg":
                take()
            return x
        raise ValueError("expected a number")

    def power():
        x = primary()
        while peek()[0] == "pow":
            x = x ** take()[1]
        return x

    def unary():
        if peek() == ("op", "−"):
            take()
            return -unary()
        return power()

    def term():
        x = unary()
        while peek()[0] == "op" and peek()[1] in "×÷":
            op = take()[1]
            y = unary()
            x = x * y if op == "×" else x / y
        return x

    def expr():
        x = term()
        while peek()[0] == "op" and peek()[1] in "+−":
            op = take()[1]
            y = term()
            x = x + y if op == "+" else x - y
        return x

    try:
        x = expr()
    except (ValueError, ZeroDivisionError, OverflowError):
        return None
    return x if pos[0] == len(toks) else None


def value(s):
    t = tokens(s)
    return None if t is None else evaluate(t)


def right_value(s):
    """(value, tolerance) for the last part of a chain: the longest leading expression the reader can evaluate. A lone
    number (with its sign, £, °, or a % it does not read) is judged at the precision written, within half a unit of its
    last decimal place, as before; an expression ("5²") or a fraction ("1/18") must match exactly. None when it does not
    start with a number."""
    toks, _ = scan(s, right=True)
    for n in range(len(toks), 0, -1):
        part = toks[:n]
        if not any(k == "n" for k, _, _ in part):
            continue
        x = evaluate([(k, v) for k, v, _ in part])
        if x is None:
            continue
        core = [t for t in part if t[0] != "deg" and (t[0], t[1]) != ("op", "−")]
        if len(core) == 1 and core[0][0] == "n" and "/" not in core[0][2] and core[0][2] != "½":
            raw = core[0][2]
            return x, Fraction(1, 2 * 10 ** (len(raw.split(".")[1]) if "." in raw else 0))
        return x, Fraction(0)
    return None


def left_text(s):
    """A claim's left side: the text after the last ": ", ". ", "; " or ", " in front of its "=", less any leading
    words (never sin, cos or tan, which belong to the sum)."""
    s = s.rstrip()
    cut = max(s.rfind(": "), s.rfind(". "), s.rfind("; "), s.rfind(", "))
    if cut >= 0:
        s = s[cut + 2:]
    return re.sub(r"^(?:(?!(?:sin|cos|tan)(?![a-z]))(?:(?![" + DIGITISH + r"])[^\W\d_])+\s+)+", "", s.strip()).strip()


def fmt(x):
    return ("%.6f" % float(x)).rstrip("0").rstrip(".")


def _same(a, b, tol):
    """a and b agree within tol; a float (from √ or trigonometry) gets a rounding allowance of one part in 10^9."""
    if isinstance(a, float) or isinstance(b, float):
        return abs(float(a) - float(b)) <= float(tol) + 1e-9 * max(1.0, abs(float(b)))
    return abs(a - b) <= tol


def equalities(text):
    """[(kind, detail)] for each "=" in a step: kind is ok, fail, label or unparsed."""
    segs = text.split("=")
    out = []
    for k in range(1, len(segs)):
        lraw, rraw = segs[k - 1], segs[k]
        L = value(lraw) if k >= 2 else None
        if L is None:
            lt = left_text(lraw)
            if not re.search(r"[\d" + DIGITISH + r"]", lt):
                out.append(("label", lt))
                continue
            L = value(lt)
            if L is None:
                out.append(("unparsed", "left side %r is not an arithmetic expression" % lt))
                continue
        R = value(rraw) if k < len(segs) - 1 else None
        if R is not None:
            tol = Fraction(0)
        else:
            got = right_value(rraw)
            if got is None:
                out.append(("unparsed", "right side %r does not start with a number" % rraw.strip()))
                continue
            R, tol = got
        if _same(L, R, tol):
            out.append(("ok", "%s = %s" % (fmt(L), fmt(R))))
        else:
            out.append(("fail", "the left side is %s, the right side %s (allowed: %s)" % (fmt(L), fmt(R), fmt(tol))))
    return out


def arithmetic(data):
    """(errors, report lines)."""
    errors, unread, n_steps, n_eq, n_label = [], [], 0, 0, 0
    for sc in data.get("scenarios", []):
        for i, step in enumerate(sc.get("steps", []), 1):
            text = bu.step_text(step)
            nocheck = step.get("noCheck") if isinstance(step, dict) else None
            where = "%s step %d" % (sc.get("id"), i)
            if isinstance(step, dict) and ("noCheck" not in step or not isinstance(nocheck, str) or not nocheck.strip()
                                           or "\n" in nocheck):
                errors.append("%s: a step written as an object needs a one-line noCheck reason" % where)
            if "=" not in text:
                if nocheck:
                    errors.append("%s: noCheck on a step with no \"=\" (stale: remove it)" % where)
                continue
            n_steps += 1
            eqs = equalities(text)
            for kind, detail in eqs:
                if kind == "fail":
                    errors.append("%s: %r does not recompute: %s" % (where, text, detail))
            n_eq += sum(1 for k, _ in eqs if k in ("ok", "fail"))
            n_label += sum(1 for k, _ in eqs if k == "label")
            why = [d for k, d in eqs if k == "unparsed"]
            if not why and not any(k in ("ok", "fail") for k, _ in eqs):
                why = ["no \"=\" in it has an arithmetic left side"]
            if why:
                unread.append("  %s: %r: %s%s" % (where, text, "; ".join(why),
                                                  " (noCheck: %s)" % nocheck if nocheck else " (NOT marked noCheck)"))
                if not nocheck:
                    errors.append("%s: %r could not be read (%s): mark it noCheck with a one-line reason, or reword "
                                  "nothing and report it" % (where, text, "; ".join(why)))
            elif nocheck:
                errors.append("%s: noCheck on a step the check reads in full (stale: remove it)" % where)
    report = ["arithmetic: %d steps with \"=\" checked: %d \"=\" signs recomputed, %d labels, %d steps could not be read "
              "in full%s" % (n_steps, n_eq, n_label, len(unread), ":" if unread else "")] + unread
    # Each card's headline sum (WWIUT-STAND-OUT): read as a step is, and it must read in full: no noCheck for a headline.
    n_head = 0
    for sc in data.get("scenarios", []):
        h = sc.get("headline")
        where = "%s headline" % sc.get("id")
        if not isinstance(h, str) or "=" not in h:
            errors.append("%s: every scenario needs a headline sum with \"=\"" % where)
            continue
        eqs = equalities(h)
        for kind, detail in eqs:
            if kind == "fail":
                errors.append("%s: %r does not recompute: %s" % (where, h, detail))
            elif kind != "ok":
                errors.append("%s: %r cannot be read in full (%s): a headline is a sum the check recomputes"
                              % (where, h, detail or kind))
        n_head += 1
    report.append("headlines: %d sums recomputed" % n_head)
    return errors, report


# ---------------------------------------------------------------- route colours (WWIUT-STAND-OUT)

TEAL = "#0d9488"
MIN_CONTRAST = 4.5
MIN_APART = 15     # CIE76 delta E between any two route colours: distinct at a glance
MIN_FROM_TEAL = 25


def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _rgb(h):
    return [int(h[i:i + 2], 16) for i in (1, 3, 5)]


def luminance(h):
    r, g, b = [_lin(x) for x in _rgb(h)]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def _lab(h):
    r, g, b = [_lin(x) for x in _rgb(h)]
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116   # noqa: E731
    return 116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z))


def delta_e(a, b):
    return sum((p - q) ** 2 for p, q in zip(_lab(a), _lab(b))) ** 0.5


def colour_errors(data):
    errors, cols = [], {}
    for r in data.get("routes", []):
        c = r.get("colour")
        if not isinstance(c, str) or not re.match(r"^#[0-9a-f]{6}$", c):
            errors.append("route %s: colour %r is not a lower-case #rrggbb" % (r.get("slug"), c))
            continue
        cols[r["slug"]] = c
        if contrast(c, "#ffffff") < MIN_CONTRAST:
            errors.append("route %s: white on %s is %.2f:1, under %.1f:1" % (r["slug"], c, contrast(c, "#ffffff"), MIN_CONTRAST))
        if delta_e(c, TEAL) < MIN_FROM_TEAL:
            errors.append("route %s: %s is too close to the portal's teal %s (delta E %.1f, under %d)"
                          % (r["slug"], c, TEAL, delta_e(c, TEAL), MIN_FROM_TEAL))
    items = sorted(cols.items())
    for i, (a, ca) in enumerate(items):
        for b, cb in items[i + 1:]:
            if delta_e(ca, cb) < MIN_APART:
                errors.append("routes %s and %s: %s and %s are not distinct (delta E %.1f, under %d)"
                              % (a, b, ca, cb, delta_e(ca, cb), MIN_APART))
    return errors


# ---------------------------------------------------------------- (a), (b), (d), (e) and the rest

def static_errors(root):
    """(errors, report lines) for a repo copy at root."""
    errors, report = [], []
    try:
        data = bu.load(root)
    except (OSError, ValueError) as e:
        return ["data/uses.json cannot be read: %s" % e], report
    # (e) the routes
    names = [r.get("name") for r in data.get("routes", [])]
    slugs = [r.get("slug") for r in data.get("routes", [])]
    if sorted(names) != sorted(ROUTES) or len(names) != len(ROUTES):
        errors.append("routes are not the 15 Skills England routes by exact name: extra %s, missing %s"
                      % (sorted(set(names) - set(ROUTES)), sorted(set(ROUTES) - set(names))))
    if len(set(slugs)) != len(slugs) or not all(isinstance(s, str) and re.match(r"^[a-z0-9-]+$", s) for s in slugs):
        errors.append("route slugs must be unique, lower case words joined by hyphens: %s" % slugs)
    topics = {t.get("slug") for t in data.get("topics", [])}
    ids = [s.get("id") for s in data.get("scenarios", [])]
    for i in sorted({i for i in ids if ids.count(i) > 1}):
        errors.append("scenario id %s is used twice" % i)
    for sc in data.get("scenarios", []):
        sid = sc.get("id")
        if sc.get("route") is not None and sc.get("route") not in slugs:
            errors.append("scenario %s: route %r is not one of the 15 routes" % (sid, sc.get("route")))
        if sc.get("topic") not in topics:
            errors.append("scenario %s: topic %r is not a topic" % (sid, sc.get("topic")))
        if sc.get("tier") not in bu.TIERS:
            errors.append("scenario %s: tier %r is not one of %s (Foundation GCSE, Higher GCSE, Level 4)"
                          % (sid, sc.get("tier"), ", ".join(bu.TIERS)))
        # the card's hook (WWIUT-CARD-FORMAT)
        q = sc.get("question")
        if not isinstance(q, str) or not q.strip():
            errors.append("scenario %s has no question (the card's text in place of the worked sum)" % sid)
        elif not q.rstrip().endswith("?"):
            errors.append("scenario %s: question %r does not end in \"?\"" % (sid, q))
        if not isinstance(sc.get("inside"), str) or not sc["inside"].strip():
            errors.append("scenario %s has no \"inside\" (the card's \"Inside:\" topic tag)" % sid)
        if "formula" not in sc or not (sc["formula"] is None or (isinstance(sc["formula"], str) and sc["formula"].strip())):
            errors.append("scenario %s: formula must be a non-empty LaTeX string or null, not %r" % (sid, sc.get("formula", "missing")))
        if "formulaNote" in sc and not (isinstance(sc["formulaNote"], str) and sc["formulaNote"].strip()):
            errors.append("scenario %s: formulaNote, where given, must be non-empty text" % sid)
        # (b) the sources
        srcs = sc.get("sources") or []
        if not srcs:
            errors.append("scenario %s has no source" % sid)
        for s in srcs:
            if not str(s.get("url", "")).startswith("https://"):
                errors.append("scenario %s: source URL %r is not https" % (sid, s.get("url")))
            if not str(s.get("title", "")).strip():
                errors.append("scenario %s: a source has no title" % sid)
            if s.get("type") != "public":
                errors.append("scenario %s: source type %r: only \"public\" is valid in v1 (a contributor type needs "
                              "Jon's ruling)" % (sid, s.get("type")))
        words = " ".join([sc.get("text", "")] + [bu.step_text(x) for x in sc.get("steps", [])])
        if bool(EXAMPLE.search(words)) != (sc.get("exampleFigures") is True):
            errors.append("scenario %s: exampleFigures is %r but the wording %s \"(example figure/s)\""
                          % (sid, sc.get("exampleFigures"), "says" if EXAMPLE.search(words) else "never says"))
    for t in data.get("topics", []):
        g = t.get("parentGuide")
        if g is not None and not (root / "parents" / str(g) / "index.html").is_file():
            errors.append("topic %s: parent guide parents/%s/ is not a page" % (t.get("slug"), g))
    nulls = [s.get("id") for s in data.get("scenarios", []) if s.get("formula", "") is None]
    report.append("formulas: %d of %d scenarios have one; %d null%s" % (len(data.get("scenarios", [])) - len(nulls),
                  len(data.get("scenarios", [])), len(nulls), " (%s)" % ", ".join(nulls) if nulls else ""))
    # (c), with the headlines
    e, r = arithmetic(data)
    errors += e
    report += r
    errors += colour_errors(data)
    if errors:
        return errors, report
    # (d) live games
    live = bu.live_games(root)
    for t in data["topics"]:
        if not bu.practise(root, t, live):
            errors.append("topic %s matches no live game (keywords %s)" % (t["slug"], t["keywords"]))
    sec = root / bu.SECTION
    for p in sorted(sec.rglob("index.html")) if sec.is_dir() else []:
        for slug in GAME_LINK.findall(p.read_text(encoding="utf-8")):
            if slug not in live:
                errors.append("%s: a Practise it link names %s, which is not a live game" % (p.relative_to(root).as_posix(), slug))
    # the home page's strip count is the number of scenarios (WWIUT-BATCH-1-2): written by the build, never typed
    portal = (root / bu.PORTAL).read_text(encoding="utf-8")
    m = re.search(re.escape(bu.COUNT_BEGIN) + r"(.*?)" + re.escape(bu.COUNT_END), portal, re.S)
    if not m:
        errors.append("%s: the strip's job count has no %s ... %s block" % (bu.PORTAL, bu.COUNT_BEGIN, bu.COUNT_END))
    elif m.group(1) != "%d real jobs" % len(data["scenarios"]):
        errors.append("%s: the strip says %r, but data/uses.json has %d scenarios: run python -X utf8 scripts/build-uses.py"
                      % (bu.PORTAL, m.group(1), len(data["scenarios"])))
    # (a) the pages are the build's output
    out, refusals = bu.build(root)
    errors += ["build-uses.py refuses: %s" % x for x in refusals]
    for path, text in out.items():
        f = root / path
        if not f.is_file():
            errors.append("%s is missing: run python -X utf8 scripts/build-uses.py" % path)
        elif f.read_text(encoding="utf-8") != text:
            errors.append("%s differs from what build-uses.py writes (never edit it by hand: edit data/uses.json, then run "
                          "the script)" % path)
    # the build's own output is whole: a page cut short by the generator would match itself and pass (a)
    hub_path = bu.SECTION + "/index.html"
    for path, text in out.items():
        if not (path.startswith(bu.SECTION + "/") and path.endswith(".html")):
            continue
        want = ["<h1>", "</main>", bu.cf.CANONICAL, "</body>\n</html>\n"]
        if path == hub_path:
            want += ['href="%s/"' % t["slug"] for t in data["topics"]]
            want += ['href="route/%s/" class="route-tile"' % r for r in {s["route"] for s in data["scenarios"] if s["route"]}]
            want += ['href="%s/#%s" class="job-card"' % (s["topic"], s["id"]) for s in data["scenarios"]]
            want += ["Pick your course", "The jobs", "By maths topic"]
            if 'href="/%s/"' % bu.SECTION in text:
                errors.append("%s: the hub links to itself" % path)
        elif "/route/" not in path:
            want += ["<h2>Practise it</h2>", "<h2>Sources</h2>", 'href="/%s/"' % bu.SECTION]
        else:
            want += ["<h2>Sources</h2>", "route-hero", 'href="/%s/"' % bu.SECTION]
        for w in want:
            if w not in text:
                errors.append("%s: build-uses.py's page has no %r (the generator is broken)" % (path, w[:40]))
    # every job card's anchor is a scenario on its topic page (read from the committed pages)
    hub = root / hub_path
    if hub.is_file():
        for topic, anchor in re.findall(r'href="([a-z0-9-]+)/#([a-z0-9-]+)" class="job-card"', hub.read_text(encoding="utf-8")):
            page = root / bu.SECTION / topic / "index.html"
            if not page.is_file() or ('id="%s"' % anchor) not in page.read_text(encoding="utf-8"):
                errors.append("%s: the job card %s/#%s points at no scenario on that topic page" % (hub_path, topic, anchor))
    for path in bu.stale(root, out) if out else []:
        errors.append("%s is not written by build-uses.py (stale: run the script, which deletes it)" % path)
    html = [p for p in out if p.startswith(bu.SECTION + "/") and p.endswith(".html")]
    report.append("pages: %d generated (%d topics, %d routes with scenarios) and the section's stylesheet, %d scenarios, "
                  "%d sources" % (len(html), len(data["topics"]), len(html) - 1 - len(data["topics"]), len(data["scenarios"]),
                                  sum(len(s["sources"]) for s in data["scenarios"])))
    report.append("practise it: " + "; ".join("%s: %s" % (t["slug"], ", ".join(s for s, _, _ in bu.practise(root, t, live)))
                                              for t in data["topics"]))
    return errors, report


# ---------------------------------------------------------------- (f) Chromium

MEASURE = """() => {
  const de = document.documentElement, over = de.scrollWidth - de.clientWidth;
  let widest = '';
  if (over > 0) {
    let w = 0;
    for (const el of document.body.querySelectorAll('*')) {
      const r = el.getBoundingClientRect();
      if (r.right > w) { w = r.right; widest = el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : ''); }
    }
  }
  // Text on the route colours (tiles, chips, a route page's header): its colour against the first painted background
  // behind it, measured as the browser draws it.
  const rgb = s => (s.match(/[\\d.]+/g) || []).map(Number);
  const lum = c => { const [r, g, b] = c.slice(0, 3).map(v => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
  const bg = el => { for (let e = el; e; e = e.parentElement) { const c = rgb(getComputedStyle(e).backgroundColor); if (c.length === 3) return c; } return [255, 255, 255]; };
  const low = [];
  let coloured = 0;
  for (const el of document.querySelectorAll('.route-tile h3, .route-tile p, .route-tile .tile-go, .route-chip, .route-hero h1, .route-hero .subtitle, .route-hero .badge, .tier-tag')) {
    coloured++;
    const a = lum(rgb(getComputedStyle(el).color)), b = lum(bg(el)), r = (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
    if (r < 4.5) low.push((el.className || el.tagName.toLowerCase()) + ' "' + el.textContent.trim().slice(0, 30) + '" ' + r.toFixed(2) + ':1');
  }
  // The KaTeX half (unrendered source, .katex-error) is katex_page_common's, read after this (contract KATEX-ERRORS)
  return {over, widest, low, coloured, aa: document.body.classList.contains('accessible')};
}"""


def browse(root, pages):
    """[faults] for each page (repo path) of the copy at root, at every size, normal and Aa."""
    import bank_common as bc
    import katex_page_common as kp
    from playwright.sync_api import sync_playwright
    faults = []

    def route(r):
        u = r.request.url
        got = bc.real_font_response(u)
        if got:
            return r.fulfill(**got)
        if u.startswith(ORIGIN):
            path = unquote(urlsplit(u).path).lstrip("/")
            if path == "" or path.endswith("/"):
                path += "index.html"
            f = root / path
            if f.is_file():
                return r.fulfill(status=200, body=f.read_bytes(),
                                 content_type=mimetypes.guess_type(str(f))[0] or "application/octet-stream")
            return r.fulfill(status=404, body=b"")
        return r.abort()

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        try:
            for path in pages:
                maths = kp.has_maths((root / path).read_text(encoding="utf-8"))
                for w, h in SIZES:
                    for mode in ("normal", "aa"):
                        ctx = browser.new_context(viewport={"width": w, "height": h})
                        ctx.add_init_script("try { localStorage.clear(); } catch (e) {}")
                        ctx.route("**/*", route)
                        page = ctx.new_page()
                        errs = []
                        page.on("pageerror", lambda e, errs=errs: errs.append(str(e)))
                        where = "%s at %dx%d %s" % (path, w, h, mode)
                        try:
                            page.goto(ORIGIN + "/" + path[:-len("index.html")] + "?cb=uses", wait_until="load")
                            kp.wait_rendered(page, maths)   # KaTeX renders on its script's load; kp.faults reports it left
                            if mode == "aa":
                                page.click("#a11yBtn")
                            page.evaluate("() => document.fonts.ready")
                            page.wait_for_timeout(250)
                            m = page.evaluate(MEASURE)
                            k = kp.state(page)
                        except Exception as e:   # a page that cannot be measured is a fault, never a pass
                            faults.append("%s: could not be measured: %s" % (where, str(e).splitlines()[0]))
                            ctx.close()
                            continue
                        if m["over"] > 0:
                            faults.append("%s: scrolls sideways by %d px (widest: %s)" % (where, m["over"], m["widest"]))
                        if mode == "aa" and not m["aa"]:
                            faults.append("%s: the Aa toggle did not switch the page to Aa" % where)
                        for x in m["low"]:
                            faults.append("%s: text on a route colour or tag under 4.5:1: %s" % (where, x))
                        faults += kp.faults(where, k, maths)
                        for e in errs:
                            faults.append("%s: page error: %s" % (where, e))
                        ctx.close()
        finally:
            browser.close()
    return faults


def generated_pages(root):
    out, _ = bu.build(root)
    return [p for p in out if p.startswith(bu.SECTION + "/") and p.endswith(".html")]


# ---------------------------------------------------------------- self-test

COPY = [bu.DATA, bu.GAMES, bu.ROSTER, bu.SITEMAP, bu.PORTAL, "parents/guide.css", "parents/guide.js", "schools/assets/opendyslexic.css",
        "schools/assets/site-footer.css", "schools/assets/favicon.svg", "schools/assets/analytics.js"]


def make_copy():
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="check-uses-"))
    rels = list(COPY) + [p.relative_to(BASE).as_posix() for p in (BASE / bu.SECTION).rglob("*") if p.is_file()]
    rels += [p.relative_to(BASE).as_posix() for p in (BASE / "parents").glob("*/index.html")]
    rels += [p.relative_to(BASE).as_posix() for p in (BASE / "schools" / "assets" / "fonts").rglob("*") if p.is_file()] \
        if (BASE / "schools" / "assets" / "fonts").is_dir() else []
    for rel in rels:
        (tmp / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(BASE / rel, tmp / rel)
    return tmp, {rel: (tmp / rel).read_bytes() for rel in rels}


def selftest():
    tmp, pristine = make_copy()
    failures, caught = [], 0
    try:
        def reset():
            for d in [tmp / bu.SECTION]:
                shutil.rmtree(d, ignore_errors=True)
            for rel, b in pristine.items():
                (tmp / rel).parent.mkdir(parents=True, exist_ok=True)
                (tmp / rel).write_bytes(b)

        def data(fn, rebuild=True):
            """Change data/uses.json; rebuild the pages so only the planted rule can fire."""
            d = json.loads(pristine[bu.DATA].decode("utf-8"))
            before = json.dumps(d, sort_keys=True)
            fn(d)
            if json.dumps(d, sort_keys=True) == before:
                raise pc.StalePlant("data plant", "the data did not change")
            (tmp / bu.DATA).write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8", newline="")
            if rebuild:
                out, refusals = bu.build(tmp)
                for path, text in out.items():
                    (tmp / path).write_text(text, encoding="utf-8", newline="")

        def edit(rel, old, new):
            p = tmp / rel
            p.write_text(pc.apply_plant(p.read_text(encoding="utf-8"), old, new, name=rel), encoding="utf-8", newline="")

        def sc(d, sid):
            return next(s for s in d["scenarios"] if s["id"] == sid)

        def set_step(sid, i, new):
            return lambda d: sc(d, sid)["steps"].__setitem__(i, new)

        ratio = bu.SECTION + "/ratio/index.html"
        n_jobs = len(json.loads(pristine[bu.DATA].decode("utf-8"))["scenarios"])
        static_plants = [
            # (a)
            ("a hand-edited page", lambda: edit(ratio, "Total parts: ", "Total parts so far: "), "ratio/index.html differs"),
            ("a stale page", lambda: ((tmp / bu.SECTION / "old").mkdir(), (tmp / bu.SECTION / "old" / "index.html").write_text("x", encoding="utf-8", newline="")),
             "old/index.html is not written by build-uses.py"),
            ("the sitemap block edited", lambda: edit(bu.SITEMAP, "when-will-i-use-this/ratio/</loc>", "when-will-i-use-this/ratios/</loc>"),
             "sitemap.xml differs"),
            ("a data change without a rebuild", lambda: data(lambda d: sc(d, "plumber").update(job="Plumber and heating engineer"), rebuild=False),
             "percentages/index.html differs"),
            # (b)
            ("a scenario with no source", lambda: data(lambda d: sc(d, "baker").update(sources=[])), "scenario baker has no source"),
            ("an http source", lambda: data(lambda d: sc(d, "baker")["sources"][0].update(url="http://www.kingarthurbaking.com/pro/bakers-percentage")),
             "is not https"),
            ("a contributor source", lambda: data(lambda d: sc(d, "baker")["sources"][0].update(type="contributor")),
             "only \"public\" is valid"),
            # (c)
            ("a wrong total", lambda: data(set_step("bricklayer", 0, "Total parts: 1 + 2 + 3 = 7.")), "bricklayer step 1"),
            ("a rounding outside half a unit", lambda: data(set_step("electrician", 1, "A lighting circuit drops 5.4 V. As a percentage: 5.4 ÷ 230 × 100 = 2.4%.")),
             "electrician step 2"),
            ("a wrong figure inside a noCheck step", lambda: data(lambda d: sc(d, "electrician")["steps"][0].update(text="Most allowed on lighting: 3% of 230 = 0.03 × 230 = 6.8 V.")),
             "electrician step 1"),
            ("a wrong thousands figure", lambda: data(lambda d: sc(d, "farmer")["steps"][0].update(text="Area: 250 × 120 = 3 000 m² = 3 ha.")),
             "farmer step 1"),
            ("a wrong bracket sum", lambda: data(set_step("groundsperson", 0, "Lines round the edge (perimeter): 2 × (100 + 64) = 228 m of white line.")),
             "groundsperson step 1"),
            ("a wrong money sum", lambda: data(set_step("plumber", 0, "£350 × 1.2 = £410.")), "plumber step 1"),
            ("an unreadable step without noCheck", lambda: data(set_step("hairdresser", 0, "Colour : developer = 1 : 2.")),
             "hairdresser step 1: 'Colour : developer = 1 : 2.' could not be read"),
            ("a noCheck with no reason", lambda: data(lambda d: sc(d, "baker")["steps"][0].update(noCheck=" ")),
             "needs a one-line noCheck reason"),
            ("a stale noCheck", lambda: data(set_step("bricklayer", 0, {"text": "Total parts: 1 + 2 + 3 = 6.", "noCheck": "x"})),
             "bricklayer step 1: noCheck on a step the check reads in full"),
            # (d)
            ("a topic matching only an unlisted game", lambda: data(lambda d: d["topics"][1].update(keywords=["percentage increase"])),
             "topic percentages matches no live game"),
            ("a Practise it link to an unlisted game", lambda: edit(bu.SECTION + "/percentages/index.html", '<li><a href="/games/percentage-flip/">',
                                                                     '<li><a href="/games/its-on-sale/">'),
             "names its-on-sale, which is not a live game"),
            # (e)
            ("a route that is not one of the 15", lambda: data(lambda d: sc(d, "plumber").update(route="plumbing"), rebuild=False),
             "route 'plumbing' is not one of the 15"),
            ("a route renamed", lambda: data(lambda d: d["routes"][6].update(name="Digital and IT")), "not the 15 Skills England routes"),
            # the rest
            ("exampleFigures false on a scenario with an example figure", lambda: data(lambda d: sc(d, "painter-decorator").update(exampleFigures=False)),
             "scenario painter-decorator: exampleFigures"),
            ("a parent guide that does not exist", lambda: data(lambda d: d["topics"][0].update(parentGuide="ratio"), rebuild=False),
             "parent guide parents/ratio/ is not a page"),
            ("an id used twice", lambda: data(lambda d: sc(d, "farmer").update(id="baker")), "scenario id baker is used twice"),
            ("a generator that cuts the hub short", lambda: setattr(bu, "tail", lambda *a, **k: ""), "index.html: build-uses.py's page has no '</main>'"),
            # WWIUT-STAND-OUT
            ("a wrong headline (2.5 ml as 25 ml)", lambda: data(lambda d: sc(d, "hospital-nurse").update(headline="125 ÷ 250 × 5 = 25 ml")),
             "hospital-nurse headline: '125 ÷ 250 × 5 = 25 ml' does not recompute"),
            ("a headline the check cannot read", lambda: data(lambda d: sc(d, "baker").update(headline="70% of 500 = 350 g of water")),
             "baker headline: '70% of 500 = 350 g of water' cannot be read in full"),
            ("a scenario with no headline", lambda: data(lambda d: sc(d, "farmer").pop("headline"), rebuild=False),
             "farmer headline: every scenario needs a headline"),
            ("a route colour failing 4.5:1", lambda: data(lambda d: d["routes"][4].update(colour="#f97316")),
             "route construction: white on #f97316 is"),
            ("a route colour the same as the teal", lambda: data(lambda d: d["routes"][1].update(colour="#0d9488")),
             "route business: #0d9488 is too close to the portal's teal"),
            ("two route colours alike", lambda: data(lambda d: d["routes"][3].update(colour="#c2410d")),
             "routes catering and construction: #c2410d and #c2410c are not distinct"),
            ("a broken job-card anchor", lambda: edit(bu.SECTION + "/index.html", 'href="ratio/#bricklayer" class="job-card"',
                                                      'href="ratio/#bricklayers" class="job-card"'),
             "the job card ratio/#bricklayers points at no scenario"),
            ("the hub linking to itself again", lambda: setattr(bu, "tail", lambda *a, **k: real_tail(True)),
             "index.html: the hub links to itself"),
            # WWIUT-BATCH-1-2
            ("a scenario with no tier", lambda: data(lambda d: sc(d, "farmer").pop("tier"), rebuild=False),
             "scenario farmer: tier None is not one of"),
            ("an unknown tier", lambda: data(lambda d: sc(d, "baker").update(tier="A"), rebuild=False),
             "scenario baker: tier 'A' is not one of"),
            ("the strip's count typed by hand", lambda: edit(bu.PORTAL, bu.COUNT_BEGIN + "%d real jobs" % n_jobs,
                                                             bu.COUNT_BEGIN + "%d real jobs" % (n_jobs + 1)),
             "index.html: the strip says '%d real jobs', but data/uses.json has %d" % (n_jobs + 1, n_jobs)),
            ("a scenario taken out without a rebuild (the count goes stale)",
             lambda: data(lambda d: d["scenarios"].pop(), rebuild=False),
             "index.html: the strip says '%d real jobs', but data/uses.json has %d" % (n_jobs, n_jobs - 1)),
            ("the strip's count markers removed", lambda: edit(bu.PORTAL, bu.COUNT_END, ""),
             "index.html: the strip's job count has no"),
            ("a wrong Pythagoras headline", lambda: data(lambda d: sc(d, "firefighter").update(headline="√(8² + 2²) = 8.52 m of ladder")),
             "firefighter headline: '√(8² + 2²) = 8.52 m of ladder' does not recompute"),
            ("a wrong sine-bar step", lambda: data(set_step("toolmaker", 0, "A 100 mm sine bar at 10°: 100 × sin 10° = 17.465 mm of blocks.")),
             "toolmaker step 1"),
            ("a wrong power in a headline", lambda: data(lambda d: sc(d, "vehicle-body-repairer").update(headline="8 ÷ 2³ = 2 hours at 94 dB")),
             "vehicle-body-repairer headline: '8 ÷ 2³ = 2 hours at 94 dB' does not recompute"),
            # WWIUT-CARD-FORMAT
            ("a scenario with no question", lambda: data(lambda d: sc(d, "farmer").pop("question"), rebuild=False),
             "scenario farmer has no question"),
            ("a question with no \"?\"", lambda: data(lambda d: sc(d, "baker").update(question="How much water for 500 g of flour")),
             "scenario baker: question 'How much water for 500 g of flour' does not end in"),
        ]
        real_tail = bu.tail
        for name, plant, needle in static_plants:
            reset()
            try:
                plant()
                errs, _ = static_errors(tmp)
            except pc.StalePlant as e:
                failures.append(str(e))
                continue
            except Exception as e:   # an error is never a catch
                failures.append("planted fault %s: the check raised %r" % (name, e))
                continue
            finally:
                bu.tail = real_tail
            if any(needle in e for e in errs):
                caught += 1
            else:
                failures.append("planted fault not caught: %s (got %s)" % (name, errs[:3]))
        # the baseline is clean, and the build is idempotent
        reset()
        errs, _ = static_errors(tmp)
        if errs:
            failures.append("baseline copy is not clean: %s" % errs[:3])
        # (f) in Chromium: one plant per shape, each on its own page
        reset()
        # a formula with broken LaTeX, planted in the data and built first (the build rewrites every page). Brace-balanced
        # ("\\dfrac{1}", a missing argument), so auto-render hands it to KaTeX, which shows it as a .katex-error.
        # An unbalanced one ("\\dfrac{1}{") never reaches KaTeX: auto-render matches braces looking for the closing
        # delimiter, so it stays as raw source, caught by the unrendered-source rule (planted on one topic page below).
        data(lambda d: sc(d, "cnc-machinist").update(formula="\\dfrac{1}"))
        hub, avg, con = bu.SECTION + "/index.html", bu.SECTION + "/averages/index.html", bu.SECTION + "/route/construction/index.html"
        edit(hub, "</main>", '<div style="width:360px;height:4px;background:#000"></div>\n</main>')
        edit(avg, "</head>", "<style>body.accessible .hero h1{width:420px}</style>\n</head>")
        edit(con, "renderMathInElement(document.body,", "void(document.body,")
        clean = bu.SECTION + "/ratio/index.html"
        agri = bu.SECTION + "/route/agriculture/index.html"
        edit(agri, 'class="hero route-hero" style="--c:#4d7c0f"', 'class="hero route-hero" style="--c:#86efac"')
        pyth = bu.SECTION + "/pythagoras/index.html"
        edit(pyth, "</head>", "<style>.tier-tag{color:#cbd5e1}</style>\n</head>")
        dec = bu.SECTION + "/decimals-measurement/index.html"
        ang = bu.SECTION + "/angles/index.html"
        edit(ang, r"\(\displaystyle \dfrac{(n-2) \times 180}{n}\)", r"\(\displaystyle \dfrac{1}{\)")
        found = browse(tmp, [hub, avg, con, clean, agri, pyth, dec, ang])
        browser_plants = [
            ("a 360 px element on the hub, caught at 320 normal", hub + " at 320x568 normal: scrolls sideways"),
            ("the same, missed at 390 (it fits)", None),
            ("an Aa-only overflow, caught at 390 Aa", avg + " at 390x844 aa: scrolls sideways"),
            ("the Aa-only overflow is not reported in normal mode", None),
            ("KaTeX left unrendered", con + " at 320x568 normal: shows KaTeX source it did not render"),
            ("an untouched page passes", None),
            ("a route header too light for white text", agri + " at 320x568 normal: text on a route colour or tag under 4.5:1"),
            ("a Higher tag too light to read", pyth + " at 320x568 normal: text on a route colour or tag under 4.5:1: tier-tag"),
            ("a formula with broken LaTeX (\\dfrac{1}) shown as a .katex-error",
             dec + " at 320x568 normal: KaTeX error on \"\\displaystyle \\dfrac{1}\""),
            ("a formula with an unclosed brace (\\dfrac{1}{) left as raw source",
             ang + " at 320x568 normal: shows KaTeX source it did not render"),
        ]
        checks = [
            any(f.startswith(browser_plants[0][1]) for f in found),
            not any(f.startswith(hub + " at 390x844 normal: scrolls") for f in found),
            any(f.startswith(browser_plants[2][1]) for f in found),
            not any(f.startswith(avg + " at 390x844 normal: scrolls") for f in found),
            any(f.startswith(browser_plants[4][1]) for f in found),
            not any(f.startswith(clean) for f in found),
            any(f.startswith(browser_plants[6][1]) for f in found),
            any(f.startswith(browser_plants[7][1]) for f in found),
            any(f.startswith(browser_plants[8][1]) for f in found),
            any(f.startswith(browser_plants[9][1]) for f in found),
        ]
        for (name, _), ok in zip(browser_plants, checks):
            if ok:
                caught += 1
            else:
                failures.append("Chromium plant failed: %s (got %s)" % (name, found[:4]))
        # the arithmetic reader on its own
        unit = [("Total parts: 1 + 2 + 3 = 6.", ["ok"]), ("Developer = 40 × 2 = 80 g.", ["label", "ok"]),
                ("Most allowed on lighting: 3% of 230 = 0.03 × 230 = 6.9 V.", ["unparsed", "ok"]),
                ("Area: 250 × 120 = 30 000 m² = 3 ha.", ["ok", "unparsed"]),
                ("x: 5.4 ÷ 230 × 100 = 2.3%.", ["ok"]), ("x: 5.4 ÷ 230 × 100 = 2.4%.", ["fail"]),
                ("mean 99.0 ÷ 5 = 19.8 °C.", ["ok"]), ("x: 50% + 10% = 0.6", ["ok"]), ("x: 8 ÷ 0 = 1", ["unparsed"]),
                ("x: (2 + 3 = 5", ["unparsed"]), ("x: 2 − 3 = −1", ["ok"]),
                # WWIUT-BATCH-1-2: each new sign, a right value passing and a wrong one caught
                ("x: √16 = 4", ["ok"]), ("x: √16 = 5", ["fail"]),
                ("x: √(3² + 4²) = 5", ["ok"]), ("x: √(3² + 4²) = 6", ["fail"]),
                ("x: √68 = 8.25", ["ok"]), ("x: √68 = 8.24", ["fail"]),
                ("x: 2³ = 8", ["ok"]), ("x: 2³ = 9", ["fail"]),
                ("x: 2⁴ = 16", ["ok"]), ("x: 2⁴ = 15", ["fail"]),
                ("x: 2⁶ = 64", ["ok"]), ("x: 2⁶ = 62", ["fail"]),
                ("Left: (½)² = 0.25", ["ok"]), ("Left: (½)² = 0.5", ["fail"]),
                ("x: 100 × sin 30° = 50", ["ok"]), ("x: 100 × sin 30° = 5", ["fail"]),
                ("x: 100 × cos 60° = 50", ["ok"]), ("x: 100 × cos 60° = 86.6", ["fail"]),
                ("x: tan 45° = 1", ["ok"]), ("x: tan 45° = 1.5", ["fail"]),
                ("x: sin⁻¹(0.5) = 30°", ["ok"]), ("x: sin⁻¹(0.5) = 60°", ["fail"]),
                ("x: cos⁻¹(0.5) = 60°", ["ok"]), ("x: cos⁻¹(0.5) = 30°", ["fail"]),
                ("x: tan⁻¹(1) = 45°", ["ok"]), ("x: tan⁻¹(1) = 40°", ["fail"]),
                ("x: sin⁻¹(2) = 30°", ["unparsed"]),
                ("Blocks: sin 10° × 100 = 17.365 mm", ["ok"]),
                ("3² + 4² = 5²", ["ok"]), ("3² + 4² = 6²", ["fail"]),
                ("x: 12570 ÷ 12 = £1,047.50.", ["ok"]), ("x: 12570 ÷ 12 = £1,074.50.", ["fail"]),
                ("x: 1 ÷ 16 = 1/16", ["ok"]), ("x: 1 ÷ 16 = 1/18", ["fail"]),
                ("Octagon: 135°, and 135 + 135 + 90 = 360°.", ["ok"])]
        for text, want in unit:
            got = [k for k, _ in equalities(text)]
            if got == want:
                caught += 1
            else:
                failures.append("arithmetic reader: %r read as %s, not %s" % (text, got, want))
        total = len(static_plants) + len(browser_plants) + len(unit)
        print("self-test: %d of %d planted faults and reader cases caught" % (caught, total))
        return failures
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--static", action="store_true")
    g.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        failures = selftest()
        for f in failures:
            print("SELF-TEST FAIL: " + f)
        return 1 if failures else 0
    errors, report = static_errors(BASE)
    print("\n".join(report))
    if not errors and a.check:
        pages = generated_pages(BASE)
        errors += browse(BASE, pages)
        print("chromium: %d pages x %d sizes x normal and Aa: %s" % (len(pages), len(SIZES), "FAIL" if errors else "no sideways scroll, KaTeX rendered"))
    for e in errors:
        print("FAIL: " + e)
    print("FAILED: %d" % len(errors) if errors else "OK")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
