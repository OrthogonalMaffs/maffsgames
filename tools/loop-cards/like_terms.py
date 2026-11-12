"""Like Terms Collector: the loop-card adapter (contract LOOP-CARDS, 12 Nov 2026).

The game's own bank, read from games/like-terms-collector/index.html (never copied): the 30 STAGE3 items and the
first 2 STAGE2 items in expression form ("3x + 2x + 4y + y" -> "5x + 5y"). The 32 deck is all of them; the 16 and 24
decks are seeded subsets of it.

The build's check never trusts the bank's answers: coeffs() parses each PRINTED expression and answer into a
coefficient for each letter, and the loop is matched on those maps, never on strings. Only the true minus (U+2212)
is accepted as a minus sign.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import bank_common as bc     # noqa: E402  the pinned KaTeX fonts' CDN address

CODE = "LT"
GAME = "like-terms-collector"
SOURCE = ROOT / "games" / "like-terms-collector" / "index.html"
STAGE2_TAKEN = 2
TXT_CLASS = "lc-maths"
FRONT_MAX, BACK_MAX = 46, 38
FONTS = ("Outfit", "KaTeX_Main", "KaTeX_Math")
_K = bc.KATEX_CDN + "fonts/"
CSS = ("@font-face { font-family: 'KaTeX_Main'; src: url('%sKaTeX_Main-Bold.woff2') format('woff2'); font-weight: 700; "
       "font-style: normal; }"
       "@font-face { font-family: 'KaTeX_Math'; src: url('%sKaTeX_Math-BoldItalic.woff2') format('woff2'); "
       "font-weight: 700; font-style: italic; }"
       ".lc-maths { font-family: 'KaTeX_Main', serif; font-weight: 700; }"
       ".lc-maths i { font-family: 'KaTeX_Math', serif; font-style: italic; font-weight: 700; }") % (_K, _K)
TEACHER_EXTRA = ()
SHOUT = None


def _block(src, name):
    m = re.search(r"const %s = \[(.*?)\n\];" % name, src, re.S)
    if not m:
        raise ValueError("no %s bank in %s" % (name, SOURCE.relative_to(ROOT)))
    return m.group(1)


def _js(s):
    return json.loads('"%s"' % s)          # the bank's − escapes


def bank():
    src = SOURCE.read_text(encoding="utf-8")
    s3 = [{"q": _js(e), "a": _js(a)} for e, a in re.findall(r"\{expr:'([^']*)', answer:'([^']*)'", _block(src, "STAGE3"))]
    if len(s3) != 30:
        raise ValueError("STAGE3 has %d items, not 30" % len(s3))
    s2 = []
    for prompt, labels, answers in re.findall(r"\{prompt:'([^']*)', labels:\[([^\]]*)\], answers:\[([^\]]*)\]\}",
                                              _block(src, "STAGE2")):
        letters = re.findall(r"'([^']*)'", labels)
        nums = [int(x) for x in answers.split(",")]
        s2.append({"q": _js(prompt), "a": " + ".join(("" if c == 1 else str(c)) + v for c, v in zip(nums, letters))})
    if len(s2) < STAGE2_TAKEN:
        raise ValueError("STAGE2 has %d items" % len(s2))
    return s3 + s2[:STAGE2_TAKEN]


def choose(n, rng):
    items = bank()
    if n > len(items):
        raise ValueError("the bank gives %d items, not %d" % (len(items), n))
    return [dict(it) for it in (items if n == len(items) else rng.sample(items, n))]


def unused(items):
    raise ValueError("Like Terms has no required card")


# ---- the independent recomputation, from the printed text --------------------------------------------------------

TERM = re.compile(r"\s*([+−]?)\s*(\d*)([a-z])\s*")


def coeffs(text, simplest=False):
    """{letter: coefficient} of a printed expression, as a frozenset of pairs with zero coefficients dropped.
    simplest=True (an answer): each letter once, no zero or written-out 1 coefficient, no leading +."""
    if "-" in text:
        raise ValueError("%r has a hyphen-minus, not a true minus (U+2212)" % text)
    s, pos, out, first = text.strip(), 0, {}, True
    if not s:
        raise ValueError("an empty expression")
    while pos < len(s):
        m = TERM.match(s, pos)
        if not m or m.end() == pos:
            raise ValueError("cannot read %r at character %d" % (text, pos))
        sign, num, var = m.groups()
        if not sign and not first:
            raise ValueError("%r: a term without + or −" % text)
        if simplest and (var in out or num in ("0", "1") or (first and sign == "+")):
            raise ValueError("%r is not in its simplest form" % text)
        c = int(num) if num else 1
        out[var] = out.get(var, 0) + (-c if sign == "−" else c)
        pos, first = m.end(), False
    return frozenset((k, v) for k, v in out.items() if v != 0)


def value_q(text):
    return coeffs(text)


def value_a(text):
    return coeffs(text, simplest=True)


def show(value):
    terms = sorted(value)
    return " + ".join("%d%s" % (c, v) for v, c in terms).replace("+ -", "− ") if terms else "0"


def html(text):
    """Letters italic (KaTeX's maths italic), numbers and operators upright, the true minus kept."""
    out = []
    for ch in text:
        out.append("<i>%s</i>" % ch if "a" <= ch <= "z" else ch.replace("&", "&amp;").replace("<", "&lt;"))
    return "".join(out)
