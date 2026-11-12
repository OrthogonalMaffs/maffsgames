"""Six Sevens, Bruv: the loop-card adapter (contract LOOP-CARDS, 12 Nov 2026).

Facts a x b with 2 <= a <= b <= 12, no x10 (the contract's rule for this pack), every product in a deck distinct,
chosen deterministically from the deck's seeded generator and weighted to the 6, 7, 8, 9 and 12 tables. Every deck
holds 6 x 7, whose card pair is SHOUTED (Jon, 12 Nov 2026, 15:05 and 15:07).

The build's check never trusts choose(): value_q() and value_a() read the PRINTED text again and work the
products out themselves, including the shouted question in words.
"""
import re

CODE = "SS"
GAME = "six-sevens-bruv"
FACTORS = [a for a in range(2, 13) if a != 10]
WEIGHTED = {6, 7, 8, 9, 12}
WEIGHT = 3                   # a fact on a weighted table is three times as likely to be chosen
REQUIRED = 42                # 6 x 7, in every deck
TXT_CLASS = "lc-num"
FRONT_MAX, BACK_MAX = 60, 46
FONTS = ("Outfit",)
CSS = ".lc-num { font-family: 'Outfit', sans-serif; font-weight: 800; }"
TEACHER_EXTRA = ("Two cards are SHOUTED. Let them.",)
SHOUT = {
    "answer": "42",                                   # the answering card's front, as printed
    "answer_line": "SHOUT: I’VE GOT SIX SEVENS, BRUV!",
    "ask_label": "SHOUT IT",
    "ask": "WHO HAS SIX SEVENS?",                     # in words: no "6 x 7" on the asking card
    "line_max": 34, "ask_max": 40,
}


def _facts():
    by_product = {}
    for a in FACTORS:
        for b in FACTORS:
            if a <= b:
                by_product.setdefault(a * b, []).append((a, b))
    return by_product


def _weight(fact):
    return WEIGHT if (fact[0] in WEIGHTED or fact[1] in WEIGHTED) else 1


def choose(n, rng):
    """n facts with distinct products, 6 x 7 always among them. A weighted sample without replacement
    (Efraimidis-Spirakis keys), so the same seed always gives the same deck."""
    by_product = _facts()
    if len(by_product) < n:
        raise ValueError("only %d distinct products, not %d" % (len(by_product), n))
    pool = sorted(p for p in by_product if p != REQUIRED)
    key = {p: rng.random() ** (1.0 / max(_weight(f) for f in by_product[p])) for p in pool}
    chosen = [REQUIRED] + sorted(pool, key=lambda p: -key[p])[:n - 1]
    items = []
    for p in chosen:
        facts = by_product[p]
        fk = {f: rng.random() ** (1.0 / _weight(f)) for f in facts}
        a, b = max(facts, key=lambda f: fk[f])
        if rng.random() < 0.5:
            a, b = b, a
        items.append({"q": "%d × %d" % (a, b), "a": str(p)})
    return items


def unused(items):
    """A fact (as an item) whose product is in none of these items: the selftest's replacement for 6 x 7."""
    have = {value_a(it["a"]) for it in items}
    for p, facts in sorted(_facts().items()):
        if p not in have and p != REQUIRED:
            a, b = facts[0]
            return {"q": "%d × %d" % (a, b), "a": str(p)}
    raise ValueError("no unused product")


# ---- the independent recomputation, from the printed text --------------------------------------------------------

WORDS = {"TWO": 2, "THREE": 3, "FOUR": 4, "FIVE": 5, "SIX": 6, "SEVEN": 7, "EIGHT": 8, "NINE": 9,
         "ELEVEN": 11, "TWELVE": 12}
FACT_RE = re.compile(r"(\d{1,2}) × (\d{1,2})")
WORDS_RE = re.compile(r"WHO HAS ([A-Z]+) ([A-Z]+?)S")


def _factor(x):
    if not (2 <= x <= 12) or x == 10:
        raise ValueError("factor %d is outside 2 to 12 without 10" % x)
    return x


def value_q(text):
    """A printed back without its "?": "a × b" (U+00D7), or the shout in words, "WHO HAS SIX SEVENS"
    (six lots of seven). Returns the product."""
    m = FACT_RE.fullmatch(text)
    if m:
        return _factor(int(m.group(1))) * _factor(int(m.group(2)))
    m = WORDS_RE.fullmatch(text)
    if m and m.group(1) in WORDS and m.group(2) in WORDS:
        return _factor(WORDS[m.group(1)]) * _factor(WORDS[m.group(2)])
    raise ValueError("cannot read the question %r (expected 'a × b' with U+00D7)" % text)


def value_a(text):
    if not re.fullmatch(r"[1-9]\d*", text):
        raise ValueError("cannot read the answer %r" % text)
    return int(text)


def show(value):
    return str(value)


def html(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
