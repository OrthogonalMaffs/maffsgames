"""Six Sevens, Bruv: the loop-card adapter (contract LOOP-CARDS, 12 Nov 2026).

Facts a x b with 3 <= a <= b <= 12, no x10, every product in a deck distinct, chosen deterministically from the deck's
seeded generator. The decks drill the 6, 7, 8, 9 and 12 tables by RULE, not by probability (contract
SIX-SEVENS-WEIGHTING, Jon's rulings of 13 Nov 2026, 01:50 and 01:55):

  CORE  = the distinct products a x b (a, b from 3 to 12, not 10 or 11) with a or b in {6, 7, 8, 9, 12}: 25 products.
  OTHER = every other distinct product a x b (a, b from 3 to 12, not 10): 15 products, from the 3, 4, 5 and 11 tables.

  SS-16 and SS-24: 42 and the rest drawn uniformly from CORE, each printed as a fact on the 6, 7, 8, 9 or 12 table
  with no 11. SS-32: all 25 CORE products, plus 7 drawn uniformly from OTHER.

Every deck holds 6 x 7, whose card pair is SHOUTED (Jon, 12 Nov 2026, 15:05 and 15:07).

The build's check never trusts choose(): value_q() and value_a() read the PRINTED text again and work the
products out themselves, including the shouted question in words; deck_problems() reads the printed backs' factors
again and holds every deck to the rule above.
"""
import re

CODE = "SS"
GAME = "six-sevens-bruv"
FACTORS = [a for a in range(3, 13) if a != 10]
TABLES = {6, 7, 8, 9, 12}    # the tables the decks drill
NOT_CORE = 11                # an 11-table fact is never core, whatever it is paired with
REQUIRED = 42                # 6 x 7, in every deck
CORE_DECKS = (16, 24)        # every card core
ALL_CORE_DECK, OTHERS = 32, 7    # all of CORE, plus this many from OTHER
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


def is_core(fact):
    """A fact on the 6, 7, 8, 9 or 12 table with no 11 in it."""
    return NOT_CORE not in fact and bool(TABLES & set(fact))


def _sets():
    """(CORE, OTHER): each a dict of product -> the facts it may be printed as, in a fixed order."""
    core, other = {}, {}
    for p, facts in sorted(_facts().items()):
        good = [f for f in facts if is_core(f)]
        if good:
            core[p] = good
        else:
            other[p] = facts
    return core, other


def choose(n, rng):
    """n facts with distinct products, 6 x 7 always among them, by the rule in the module's docstring. Every draw
    comes from rng, over sorted lists, so the same seed always gives the same deck."""
    core, other = _sets()
    if n in CORE_DECKS:
        pool = sorted(p for p in core if p != REQUIRED)
        if len(pool) < n - 1:
            raise ValueError("only %d core products besides 42, not %d" % (len(pool), n - 1))
        chosen = [(REQUIRED, core[REQUIRED])] + [(p, core[p]) for p in rng.sample(pool, n - 1)]
    elif n == ALL_CORE_DECK:
        if len(core) + OTHERS != n or len(other) < OTHERS:
            raise ValueError("%d core and %d other products cannot make %d + %d cards"
                             % (len(core), len(other), len(core), OTHERS))
        chosen = [(p, core[p]) for p in sorted(core)] + [(p, other[p]) for p in rng.sample(sorted(other), OTHERS)]
    else:
        raise ValueError("no Six Sevens deck of %d cards (16, 24 or 32)" % n)
    items = []
    for p, facts in chosen:
        a, b = rng.choice(facts)
        if rng.random() < 0.5:
            a, b = b, a
        items.append({"q": "%d × %d" % (a, b), "a": str(p)})
    return items


def unused(items):
    """A fact (as an item) whose product is in none of these items: the selftest's replacement for 6 x 7."""
    have = {value_a(it["a"]) for it in items}
    core, other = _sets()
    for p, facts in sorted(list(core.items()) + list(other.items())):
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
    if not (3 <= x <= 12) or x == 10:
        raise ValueError("factor %d is outside 3 to 12 without 10" % x)
    return x


def _parse(text):
    """The two numbers a printed back names: "a × b" (U+00D7), or the shout in words, "WHO HAS SIX SEVENS"
    (six lots of seven). Neither range-checked nor multiplied: value_q() and factors_q() share this reading."""
    m = FACT_RE.fullmatch(text)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = WORDS_RE.fullmatch(text)
    if m and m.group(1) in WORDS and m.group(2) in WORDS:
        return WORDS[m.group(1)], WORDS[m.group(2)]
    raise ValueError("cannot read the question %r (expected 'a × b' with U+00D7)" % text)


def value_q(text):
    """A printed back without its "?". Returns the product."""
    a, b = _parse(text)
    return _factor(a) * _factor(b)


def factors_q(text):
    """A printed back without its "?". Returns its two factors (a, b) as printed."""
    return _parse(text)


def deck_problems(code, n, backs):
    """The table rule, read from the deck's PRINTED backs (each without its "?") through factors_q() alone, never
    from choose(). SS-16 and SS-24: every card core (a factor in 6, 7, 8, 9, 12; no 11). SS-32: at least 25 core
    cards and at most 7 others. Every deck: no factor below 3. One message per fault, naming the deck and the back."""
    problems, core, others = [], [], []
    for text in backs:
        try:
            fact = factors_q(text)
        except ValueError as e:
            problems.append("%s: the back %r: %s" % (code, text, e))
            continue
        if min(fact) < 3:
            problems.append("%s: the back %r has a factor below 3" % (code, text))
        (core if is_core(fact) else others).append(text)
    if n in CORE_DECKS:
        for text in others:
            problems.append("%s: the back %r is not on the 6, 7, 8, 9 or 12 table without an 11 (every %s card must be)"
                            % (code, text, code))
    elif n == ALL_CORE_DECK:
        need = len(_sets()[0])
        if len(core) < need or len(others) > OTHERS:
            problems.append("%s: %d cards on the 6, 7, 8, 9 and 12 tables without an 11 and %d others (%s); it needs at "
                            "least %d and at most %d" % (code, len(core), len(others), ", ".join(map(repr, others)),
                                                         need, OTHERS))
    else:
        problems.append("%s: no table rule for a deck of %d cards" % (code, n))
    return problems


def value_a(text):
    if not re.fullmatch(r"[1-9]\d*", text):
        raise ValueError("cannot read the answer %r" % text)
    return int(text)


def show(value):
    return str(value)


def html(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
