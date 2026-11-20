#!/usr/bin/env python3
"""MaffsCards: computes every value of the 48 cards and writes data/maffscards.json (contract MAFFSCARDS-DATA, 19 Nov 2026).

MaffsCards is a compare-and-win number card deck: each card is a number from 1 to 100 with six values, and the
higher value wins a round (the lower one on distance to the nearest square). The printed deck (build_pdf.py) and the
online game both read data/maffscards.json and never recompute or retype a value, so a card cannot differ between them.

What is fixed here, by hand: the deck list (which numbers, which deck) and each card's nickname. What is computed here,
never typed: every value. tools/maffscards/check.py recomputes every value by a second method and compares all three
(this output, the contract's table and the committed JSON).

The six categories, in card order (contract part 2):
  sof     Sum of factors: every positive divisor, 1 and n included.
  lpf     Largest prime factor; 1 has none and scores 0 (shown "none").
  roman   Roman numeral length, standard subtractive (IV, IX, XL, XC); the numeral itself is in the data.
  dist    Distance to the nearest square of 0, 1, 4, ..., 100; lowest wins.
  powers  Superpowers, one each: prime, square, cube, triangular, Fibonacci, palindrome. 1 counts as square, cube,
          triangular and Fibonacci; 1 is not prime; single digits are palindromes. The list is in that order.
  pi      Occurrences of n's digits in a row among the 1,000 decimals of pi after the point (the leading 3 not
          counted), overlaps counted.

It also writes games/maffscards/cards.json for the online game (contract MAFFSCARDS-GAME, 20 Nov 2026), because data/
is not part of the live site (_config.yml): the same content as data/maffscards.json plus, on every card, a "how" line
for each category, the working that ends on the card's value (e.g. "28: 1 + 2 + 4 + 7 + 14 + 28 = 56"). The how lines
are built from the same functions as the values; the page reads cards.json and never recomputes a value.

    python -X utf8 tools/maffscards/gen.py           # write data/maffscards.json and games/maffscards/cards.json
    python -X utf8 tools/maffscards/gen.py --check   # exit 1 if either committed file differs from what this computes
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "maffscards.json"
GAME_OUT = ROOT / "games" / "maffscards" / "cards.json"

PI_DECIMALS = 1000

# (n, nickname), in deck order. Fixed by the contract; nothing else here is typed.
MAIN = [
    (1, "Technically Everything"),
    (2, "The Only Even Prime, and Insufferable About It"),
    (7, "Lucky for Some, Prime for All"),
    (11, "Prime From Both Ends"),
    (17, "One Past Sixteen and Still Not a Square"),
    (21, "Blackjack, Triangle AND Fibonacci"),
    (26, "One Letter for Every Superpower It Doesn't Have"),
    (27, "Three Threes Walk Into a Cube"),
    (28, "Perfect, and Knows It"),
    (33, "Mirror, Mirror"),
    (36, "The Show-Off Square"),
    (37, "The Loner"),
    (43, "Prime, Miles From Any Square"),
    (46, "The Chromosome Count"),
    (48, "Factor Hoarder"),
    (49, "Seven Sevens, Very Tidy"),
    (51, "Looks Prime, Isn't"),
    (53, "Prime, Ordinary, Proud"),
    (55, "The Triple Threat"),
    (60, "Twelve Factors and a Clock"),
    (61, "One Minute Over"),
    (64, "Square AND Cube, and Won't Shut Up About It"),
    (68, "Four 17s in a Trench Coat"),
    (71, "Prime, Stuck in the Seventies"),
    (74, "Two 37s Holding Hands"),
    (77, "Sevens All the Way Down"),
    (88, 'LXXXVIII: Roman for "Ouch"'),
    (89, "Fibonacci's Lanky Prime"),
    (93, "Also Looks Prime, Also Isn't"),
    (94, "Two 47s, No Plan"),
    (96, "The Factor Factory"),
    (100, "The Big Round One"),
]
EXTRA = [
    (4, "Two Twos, Squared Away"),
    (5, "High Five: Prime, Fibonacci, Palindrome"),
    (13, "Unlucky? It's Prime AND Fibonacci"),
    (19, "One Short of a Score"),
    (34, "Fibonacci in Disguise"),
    (38, "No Powers, Just Vibes"),
    (47, "Two Short of a Square"),
    (59, "Last Prime Before Sixty"),
    (63, "One Short of a Square AND a Cube"),
    (66, "Route 66: Triangular Palindrome"),
    (73, "Prime Both Ways"),
    (75, "Three Quarters of a Hundred"),
    (80, "So Close to 81 It Hurts"),
    (87, "The Prime Impersonator"),
    (92, "Four 23s Pretending to Be One Number"),
    (95, "Five 19s and a Dream"),
]

POWER_ORDER = ["prime", "square", "cube", "triangular", "Fibonacci", "palindrome"]

# Card order. "measure" says what is compared: the value itself, or its length (the numeral's letters, the list's
# powers), so the game never has to infer it.
CATEGORIES = [
    {"key": "sof", "label": "Sum of factors", "winner": "highest", "measure": "value"},
    {"key": "lpf", "label": "Largest prime factor", "winner": "highest", "measure": "value"},
    {"key": "roman", "label": "Roman numeral length", "winner": "highest", "measure": "length"},
    {"key": "dist", "label": "Distance to nearest square", "winner": "lowest", "measure": "value"},
    {"key": "powers", "label": "Superpowers", "winner": "highest", "measure": "length"},
    {"key": "pi", "label": "Times in pi's first 1,000 digits", "winner": "highest", "measure": "value"},
]


# ------------------------------------------------------------------------------------------------ the values
def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def sum_of_factors(n):
    return sum(divisors(n))


def is_prime(n):
    """Trial division. 1 is not prime: it has one divisor, not two."""
    return n >= 2 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def largest_prime_factor(n):
    """0 for 1, which has no prime factor."""
    best, m, p = 0, n, 2
    while m > 1:
        while m % p == 0:
            best, m = p, m // p
        p += 1
    return best


ROMAN = [(100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]


def roman(n):
    """Standard subtractive numerals, greedy from the largest value (1 to 100 needs nothing past C)."""
    out = ""
    for v, s in ROMAN:
        while n >= v:
            out, n = out + s, n - v
    return out


SQUARES = [k * k for k in range(0, 11)]          # 0, 1, 4, ..., 100


def distance_to_square(n):
    return min(abs(n - s) for s in SQUARES)


def fibonacci_upto(limit):
    a, b, out = 1, 2, {1}
    while b <= limit:
        out.add(b)
        a, b = b, a + b
    return out


FIB = fibonacci_upto(100)
TRI = {k * (k + 1) // 2 for k in range(1, 15)}
CUBES = {k ** 3 for k in range(1, 5)}


def powers(n):
    has = {
        "prime": is_prime(n),
        "square": n in SQUARES,
        "cube": n in CUBES,
        "triangular": n in TRI,
        "Fibonacci": n in FIB,
        "palindrome": str(n) == str(n)[::-1],
    }
    return [p for p in POWER_ORDER if has[p]]


def pi_digits(count):
    """'3' and then `count` decimals of pi, by Gibbons' unbounded spigot (exact integer arithmetic, no rounding)."""
    q, r, t, k, m, x = 1, 0, 1, 1, 3, 3
    out = []
    while len(out) < count + 1:
        if 4 * q + r - t < m * t:
            out.append(str(m))
            q, r, m = 10 * q, 10 * (r - m * t), (10 * (3 * q + r)) // t - 10 * m
        else:
            q, r, t, k, m, x = q * k, (2 * q + r) * x, t * x, k + 1, (q * (7 * k + 2) + r * x) // (t * x), x + 2
    return "".join(out)


def pi_decimals(count=PI_DECIMALS):
    """The `count` decimals after the point; the leading 3 is not one of them."""
    return pi_digits(count)[1:]


def count_overlapping(hay, needle):
    return sum(1 for i in range(len(hay) - len(needle) + 1) if hay.startswith(needle, i))


# ------------------------------------------------------------------------------------------------ the deck
def card(n, deck, nickname, decimals):
    return {
        "n": n,
        "deck": deck,
        "nickname": nickname,
        "sof": sum_of_factors(n),
        "lpf": largest_prime_factor(n),
        "roman": roman(n),
        "dist": distance_to_square(n),
        "powers": powers(n),
        "pi": count_overlapping(decimals, str(n)),
    }


def build():
    decimals = pi_decimals()
    cards = [card(n, "main", nick, decimals) for n, nick in MAIN]
    cards += [card(n, "extra", nick, decimals) for n, nick in EXTRA]
    return {
        "about": "MaffsCards, generated by tools/maffscards/gen.py and checked by tools/maffscards/check.py. "
                 "Do not edit by hand: change gen.py and run it.",
        "pi_decimals": PI_DECIMALS,
        "categories": CATEGORIES,
        "cards": cards,
    }


# ------------------------------------------------------------------------------------------------ the how lines
# One line per card and category, the working that ends on the value (contract MAFFSCARDS-GAME, item 2). Built from
# the functions above, never typed; check.py checks every line ends on the card's value.
MINUS = "\u2212"
SUPERSCRIPT_2 = "\u00b2"


def prime_factors(n):
    """n's prime factors with repeats, smallest first (68 -> [2, 2, 17])."""
    out, m, p = [], n, 2
    while m > 1:
        while m % p == 0:
            out, m = out + [p], m // p
        p += 1
    return out


def how_lines(c):
    n = c["n"]
    divs = divisors(n)
    lines = {"sof": "%d: %s = %d" % (n, " + ".join(str(d) for d in divs), c["sof"])}
    if n == 1:
        lines["lpf"] = "1 has no prime factors: 0"
    elif is_prime(n):
        lines["lpf"] = "%d is prime: largest prime %d" % (n, c["lpf"])
    else:
        lines["lpf"] = "%d = %s: largest prime %d" % (n, " \u00d7 ".join(str(p) for p in prime_factors(n)), c["lpf"])
    k = len(c["roman"])
    lines["roman"] = "%d = %s: %d letter%s" % (n, c["roman"], k, "" if k == 1 else "s")
    if c["dist"] == 0:
        lines["dist"] = "%d = %d%s: 0" % (n, round(n ** 0.5), SUPERSCRIPT_2)
    else:
        sq = next(s for s in SQUARES if abs(n - s) == c["dist"])
        big, small = max(n, sq), min(n, sq)
        lines["dist"] = "%d: nearest square %d, %d %s %d = %d" % (n, sq, big, MINUS, small, c["dist"])
    if c["powers"]:
        lines["powers"] = "%d: %s: %d" % (n, ", ".join(c["powers"]), len(c["powers"]))
    else:
        lines["powers"] = "%d: no superpowers: 0" % n
    lines["pi"] = "%d appears %d time%s in pi's first 1,000 digits" % (n, c["pi"], "" if c["pi"] == 1 else "s")
    return {cat["key"]: lines[cat["key"]] for cat in CATEGORIES}


def build_game(data, how=how_lines):
    """cards.json: data/maffscards.json's content, each card with its how lines. `how` is replaceable for check.py's
    plant (a how line ending on the wrong value)."""
    out = json.loads(json.dumps(data))
    for c in out["cards"]:
        c["how"] = how(c)
    return out


def dumps(data):
    return json.dumps(data, ensure_ascii=False, indent=1) + "\n"


def main(argv):
    data = build()
    outputs = [(OUT, dumps(data)), (GAME_OUT, dumps(build_game(data)))]
    if "--check" in argv:
        bad = 0
        for path, text in outputs:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                print("FAIL: %s is not gen.py's output; run python -X utf8 tools/maffscards/gen.py" % path.relative_to(ROOT))
                bad = 1
            else:
                print("PASS: %s is gen.py's output" % path.relative_to(ROOT))
        return bad
    for path, text in outputs:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        print("wrote %s (%d cards)" % (path.relative_to(ROOT), len(MAIN) + len(EXTRA)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
