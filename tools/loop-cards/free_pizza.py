"""Free Daily Pizza: the loop-card adapter (contract FDP-LOOP-CARDS, Amendment 1, 13 Nov 2026).

Fraction, decimal and percentage equivalence. A card's back asks for a value in another form ("Who has 3/4 as a
decimal?") and exactly one front answers it in that form ("I have 0.75").

The values and every printed form are the game's own, never copied: page_forms() runs the script of
games/free-daily-pizza/index.html that defines FDP (FDP.S1_VALUES, FDP.S2_VALUES and FDP.fmt's fracText, decText and
pctText) in a node subprocess, in node's vm module with no browser, and returns what those helpers print. So a
recurring decimal is the game's 0.3 with a dot over the 3 (the digit, then U+0307) and a third of a percent is 33⅓%.

  Every deck: all 15 FDP.S1_VALUES (the benchmarks, 1/3 and 2/3 among them), plus n - 15 of FDP.S2_VALUES drawn
  uniformly. Every value is on exactly one card, so 0.25 and 25% never both appear. The six conversions (fraction to
  decimal, fraction to percentage, and so on) are each used floor(n/6) or ceil(n/6) times. No shout card.

The build's check never trusts choose() or the page: read() parses the PRINTED text again with Python's Fraction (a
fraction a/b in lowest terms, a decimal with or without recurring dots, a percentage with or without a third), and
shares nothing with the page's code. value_q() and value_a() return (value, form), so the loop is matched on the
value AND the form: a front in the wrong form answers nothing. deck_problems() holds each deck's mix to the rule
above from the printed backs alone.

On a card a fraction is stacked. Its "/" stays in the page's text (so the text reads back as "3/4") but is not
drawn: the bar is the numerator's bottom border. On the answer sheet the same fraction is printed inline, as 3/4.
"""
import functools
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import bank_common as bc     # noqa: E402  the pinned KaTeX fonts' CDN address

CODE = "FP"
GAME = "free-daily-pizza"
SOURCE = ROOT / "games" / "free-daily-pizza" / "index.html"
SIZES = (16, 24, 32)
PAIRS = ("f>d", "f>p", "d>f", "d>p", "p>d", "p>f")       # given form > asked form
ASKED = {"f": "a fraction", "d": "a decimal", "p": "a percentage"}
FORM_OF = {words: form for form, words in ASKED.items()}
FORM_NAME = {"f": "fraction", "d": "decimal", "p": "percentage"}
TXT_CLASS = "fp-maths"
FRONT_MAX, BACK_MAX = 60, 40
FONTS = ("Outfit", "KaTeX_Main")
_K = bc.KATEX_CDN + "fonts/"
CSS = ("@font-face { font-family: 'KaTeX_Main'; src: url('%sKaTeX_Main-Bold.woff2') format('woff2'); font-weight: 700; "
       "font-style: normal; }"
       ".fp-maths { font-family: 'KaTeX_Main', serif; font-weight: 700; }"
       # the answer sheet: a fraction inline, its slash printed
       ".fp-as { font-family: 'Outfit', sans-serif; font-weight: 500; }"
       ".lc-txt .fp-as { font-weight: 800; }"
       # a card: the value on its own line, the fraction stacked, its slash in the text but not drawn
       ".lc-txt .fp-br { display: block; }"
       ".lc-txt .fp-val { font-size: 1.4em; }"
       ".lc-txt .fp-frac { display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; "
       "line-height: 1.05; margin: 0 0.06em; }"
       ".lc-txt .fp-frac .fp-n { border-bottom: 0.07em solid #000; padding: 0 0.12em 0.02em; }"
       ".lc-txt .fp-frac .fp-d { padding: 0.02em 0.12em 0; }"
       ".lc-txt .fp-frac .fp-sl { position: absolute; width: 0; height: 0; overflow: hidden; font-size: 0; }"
       # a recurring digit: the dot is drawn over it; its U+0307 stays in the text, undrawn, so no font can misplace it
       ".fp-rec { position: relative; display: inline-block; }"
       ".fp-rec .fp-dot { position: absolute; width: 0; height: 0; overflow: hidden; font-size: 0; }"
       ".fp-rec::after { content: ''; position: absolute; left: 50%%; top: 0.06em; width: 0.13em; height: 0.13em; "
       "margin-left: -0.065em; border-radius: 50%%; background: #000; }") % _K
# The contract's line is "Every card's value is different, so 0.25 and 25% never both appear." (12 words); page 1
# allows 120 words outside its table and has 114 before this line, so only its last six words fit.
TEACHER_EXTRA = ("0.25 and 25% never both appear.",)
SHOUT = None

DOT = "̇"                                # the game's recurring dot: a combining dot above, after its digit
THIRDS = {"⅓": Fraction(1, 3), "⅔": Fraction(2, 3)}

# ---- the game's own values and printed forms, from the page, in node ---------------------------------------------

NODE_DRIVER = r"""
const fs = require('fs'), vm = require('vm');
const src = fs.readFileSync(process.argv[1], 'utf8');
const scripts = [...src.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).filter(s => s.includes('FDP.S1_VALUES ='));
if (scripts.length !== 1) { console.error('found ' + scripts.length + ' scripts defining FDP.S1_VALUES, not 1'); process.exit(2); }
const win = {};
vm.runInContext(scripts[0], vm.createContext({ window: win }), { timeout: 30000 });
const FDP = win.FDP;
if (!FDP || !FDP.fmt || !Array.isArray(FDP.S1_VALUES) || !Array.isArray(FDP.S2_VALUES)) { console.error('the page defines no FDP values or FDP.fmt'); process.exit(2); }
const form = v => ({ v: v, f: FDP.fmt.fracText(v), d: FDP.fmt.decText(v), p: FDP.fmt.pctText(v) });
process.stdout.write(JSON.stringify({ s1: FDP.S1_VALUES.map(form), s2: FDP.S2_VALUES.map(form) }));
"""


def find_node():
    """node on PATH, else the node the Playwright package ships (scripts/test-ga4-country.py's find_node(); CI puts
    that one on PATH for verify-test-the-claim.py)."""
    node = shutil.which("node")
    if node:
        return node
    try:
        import playwright
        cand = os.path.join(os.path.dirname(playwright.__file__), "driver", "node")
        if os.path.exists(cand) or os.path.exists(cand + ".exe"):
            return cand
    except ImportError:
        pass
    raise ValueError("no node on PATH and no Playwright driver node, so the game page's FDP code cannot run")


@functools.lru_cache(maxsize=None)
def page_forms():
    """(S1, S2): each a tuple of {"v": [n, d], "f": ..., "d": ..., "p": ...}, the page's values in the page's order
    with the text its own helpers print for each form."""
    r = subprocess.run([find_node(), "-e", NODE_DRIVER, str(SOURCE)], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise ValueError("node could not run %s's FDP code: %s" % (SOURCE.relative_to(ROOT), r.stderr.strip()[-300:]))
    data = json.loads(r.stdout)
    for name in ("s1", "s2"):
        for e in data[name]:
            if not all(isinstance(e.get(k), str) and e[k] for k in "fdp"):
                raise ValueError("the page prints no fraction, decimal or percentage for %s" % e.get("v"))
    return tuple(data["s1"]), tuple(data["s2"])


def choose(n, rng):
    """n items: every S1 value and n - 15 S2 values, each asked once, the six conversions spread evenly. Every draw
    comes from rng, over the page's own order, so the same seed always gives the same deck."""
    if n not in SIZES:
        raise ValueError("no Free Daily Pizza deck of %d cards (16, 24 or 32)" % n)
    s1, s2 = page_forms()
    extra = n - len(s1)
    if extra < 0 or extra > len(s2):
        raise ValueError("%d S1 and %d S2 values cannot make %d cards" % (len(s1), len(s2), n))
    values = list(s1) + rng.sample(list(s2), extra)
    pairs = list(PAIRS) * (n // len(PAIRS)) + rng.sample(list(PAIRS), n % len(PAIRS))
    rng.shuffle(pairs)
    return [{"q": "%s as %s" % (e[pair[0]], ASKED[pair[2]]), "a": e[pair[2]]} for e, pair in zip(values, pairs)]


def unused(items):
    raise ValueError("Free Daily Pizza has no required card")


# ---- the independent recomputation, from the printed text --------------------------------------------------------

FRACTION_RE = re.compile(r"(\d+)/(\d+)")
DECIMAL_RE = re.compile(r"(\d+)\.((?:\d%s?)+)" % DOT)
PERCENT_RE = re.compile(r"(\d+(?:\.\d+)?)?([%s])?%%" % "".join(THIRDS))
QUESTION_RE = re.compile(r"(.+) as (a fraction|a decimal|a percentage)")


def _decimal(whole, tail):
    """whole.tail, where a digit followed by U+0307 carries a recurring dot: one dotted digit recurs alone; two mark
    the first and last digit of the recurring block."""
    digits, dots = "", []
    for ch in tail:
        if ch == DOT:
            dots.append(len(digits) - 1)
        else:
            digits += ch
    if not dots:
        return Fraction(int(whole + digits), 10 ** len(digits))
    if len(dots) > 2 or dots[-1] != len(digits) - 1:
        raise ValueError("the recurring dots are not on the last digit, or there are more than two")
    pre, rep = digits[:dots[0]], digits[dots[0]:]
    return (Fraction(int(whole + pre) if whole + pre else 0, 10 ** len(pre))
            + Fraction(int(rep), (10 ** len(rep) - 1) * 10 ** len(pre)))


def read(text):
    """(exact value, form) of one printed value: "f" a fraction a/b in lowest terms, "d" a decimal, "p" a
    percentage."""
    if "̇" in text and not DECIMAL_RE.fullmatch(text):
        raise ValueError("cannot read %r: a recurring dot outside a decimal" % text)
    m = FRACTION_RE.fullmatch(text)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        if b == 0:
            raise ValueError("%r divides by zero" % text)
        v = Fraction(a, b)
        if (v.numerator, v.denominator) != (a, b):
            raise ValueError("the fraction %r is not in its lowest terms" % text)
        return v, "f"
    m = DECIMAL_RE.fullmatch(text)
    if m:
        try:
            return _decimal(m.group(1), m.group(2)), "d"
        except ValueError as e:
            raise ValueError("cannot read the decimal %r: %s" % (text, e))
    m = PERCENT_RE.fullmatch(text)
    if m and (m.group(1) or m.group(2)):
        whole, third = m.group(1), m.group(2)
        if third and whole and "." in whole:
            raise ValueError("cannot read the percentage %r" % text)
        return (Fraction(whole or "0") + (THIRDS[third] if third else 0)) / 100, "p"
    raise ValueError("cannot read %r as a fraction a/b, a decimal or a percentage" % text)


def _question(text):
    """(given value, given form, asked form) of a printed back without its "?"."""
    m = QUESTION_RE.fullmatch(text)
    if not m:
        raise ValueError("cannot read the question %r (expected '<value> as a fraction', 'as a decimal' or "
                         "'as a percentage')" % text)
    value, given = read(m.group(1))
    return value, given, FORM_OF[m.group(2)]


def value_q(text):
    """A printed back without its "?": (the value it gives, the form it asks for)."""
    value, _, asked = _question(text)
    return value, asked


def value_a(text):
    """A printed front: (its value, the form it is printed in)."""
    return read(text)


def show(value):
    v, form = value
    return "%s as a %s" % (v, FORM_NAME[form])


def deck_problems(code, n, backs):
    """The deck's mix, read from its PRINTED backs alone (each without its "?"): every given value distinct; no back
    asking for the form it gives; every S1 value of the game page among them; the six conversions used within one of
    each other. One message per fault, naming the deck."""
    problems, seen, counts = [], {}, dict.fromkeys(PAIRS, 0)
    for text in backs:
        try:
            value, given, asked = _question(text)
        except ValueError as e:
            problems.append("%s: the back %r: %s" % (code, text, e))
            continue
        seen.setdefault(value, []).append(text)
        if given == asked:
            problems.append("%s: the back %r asks for the form it gives (a %s)" % (code, text, FORM_NAME[given]))
        else:
            counts["%s>%s" % (given, asked)] += 1
    for value, texts in sorted(seen.items()):
        if len(texts) > 1:
            problems.append("%s: the value %s is on %d backs (%s): every card's value must be different"
                            % (code, value, len(texts), ", ".join(map(repr, texts))))
    s1 = [Fraction(*e["v"]) for e in page_forms()[0]]
    missing = [str(v) for v in s1 if v not in seen]
    if missing:
        problems.append("%s: %d of the game's %d S1 values are on no back (%s): every deck holds them all"
                        % (code, len(missing), len(s1), ", ".join(missing)))
    if max(counts.values()) - min(counts.values()) > 1:
        problems.append("%s: the six conversions are not spread evenly (%s): their counts must be within one of each "
                        "other" % (code, ", ".join("%s %d" % (p, counts[p]) for p in PAIRS)))
    return problems


# ---- typesetting ---------------------------------------------------------------------------------------------------

def _value_html(text):
    out = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    out = re.sub(r"(\d)%s" % DOT, r'<span class="fp-rec">\1<span class="fp-dot">%s</span></span>' % DOT, out)
    return FRACTION_RE.sub(r'<span class="fp-frac"><span class="fp-n">\1</span><span class="fp-sl">/</span>'
                           r'<span class="fp-d">\2</span></span>', out)


def html(text):
    """A value, or "<value> as a decimal". The page's text stays what was given (a fraction's "/" and a recurring
    digit's U+0307 are in it, undrawn); on a card the fraction is stacked, and a question's value is larger than the "as a ...?" on the line below it."""
    m = QUESTION_RE.fullmatch(text)
    if not m:
        return _value_html(text)
    return ('<span class="fp-val">%s</span><span class="fp-br"></span> <span class="fp-as">as %s</span>'
            % (_value_html(m.group(1)), m.group(2)))
