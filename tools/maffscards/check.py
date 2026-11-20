#!/usr/bin/env python3
"""MaffsCards: every value of the 48 cards recomputed by a second method (contract MAFFSCARDS-DATA, 19 Nov 2026).

Three sources must agree on every card, every category:
  1. what tools/maffscards/gen.py computes now (its own functions, run here);
  2. this file's own recomputation, by methods that share no code with gen.py (below);
  3. the contract's table (part 2, typed into TABLE below once, as the contract gives it);
and data/maffscards.json must be gen.py's output byte for byte, so a hand edit in the JSON fails.

The second methods:
  pi      Machin's formula, pi = 16 arctan(1/5) - 4 arctan(1/239), in fixed-point integers with guard digits, AND
          gen.py's spigot; the two strings must be equal, and decimals 1-10 = 1415926535, 991-1000 = 2164201989.
          Counts by a regex lookahead (overlaps counted), not gen.py's slice loop.
  sof     from the prime factorisation: the product of (p^(k+1) - 1)/(p - 1), not a divisor loop.
  lpf     from a smallest-prime-factor sieve, not trial division.
  roman   digit by digit from place-value tables (hundreds, tens, units), not greedy; and read back to n.
  dist    from the integer square root: min(n - r^2, (r + 1)^2 - n).
  powers  prime from a sieve of Eratosthenes; square and cube from integer roots; triangular when 8n + 1 is a
          square; Fibonacci when 5n^2 + 4 or 5n^2 - 4 is a square; palindrome by reversing the digits arithmetically.

Also: 32 main and 16 extra cards, no number twice, the six categories in card order with their labels and winners
(distance lowest, the rest highest), the pi label stating the 1,000-digit limit, and the phrase the deck must never
use (a registered trade mark) absent from every MaffsCards file and the printables page.

Plants (--selftest; each must FAIL, by plant_common): one pi count off by one; 1 counted as prime; a hand edit in the
JSON.

    python -X utf8 tools/maffscards/check.py [--selftest]
"""
import json
import math
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts"))
import gen                     # noqa: E402  (source 1)
import plant_common as pc      # noqa: E402

JSON_PATH = ROOT / "data" / "maffscards.json"
PI_FIRST10 = "1415926535"
PI_991_1000 = "2164201989"
TRADE_MARK = "top" + " " + "trumps"          # split so this file never holds the phrase it scans for
SCANNED = [HERE / "gen.py", HERE / "check.py", HERE / "build_pdf.py", HERE / "README.md", JSON_PATH,
           ROOT / "printables" / "index.html"]

# The contract's table, part 2, verbatim: n|sum of factors|largest prime factor (0 = none)|Roman numeral|distance to
# nearest square|superpowers|pi count|nickname. Main deck, then extra.
TABLE_MAIN = """\
1|1|0|I|0|square,cube,triangular,Fibonacci,palindrome|116|Technically Everything
2|3|2|II|1|prime,Fibonacci,palindrome|103|The Only Even Prime, and Insufferable About It
7|8|7|VII|2|prime,palindrome|95|Lucky for Some, Prime for All
11|12|11|XI|2|prime,palindrome|16|Prime From Both Ends
17|18|17|XVII|1|prime|18|One Past Sixteen and Still Not a Square
21|32|7|XXI|4|triangular,Fibonacci|15|Blackjack, Triangle AND Fibonacci
26|42|13|XXVI|1|-|9|One Letter for Every Superpower It Doesn't Have
27|40|3|XXVII|2|cube|14|Three Threes Walk Into a Cube
28|56|7|XXVIII|3|triangular|13|Perfect, and Knows It
33|48|11|XXXIII|3|palindrome|10|Mirror, Mirror
36|91|3|XXXVI|0|square,triangular|9|The Show-Off Square
37|38|37|XXXVII|1|prime|12|The Loner
43|44|43|XLIII|6|prime|7|Prime, Miles From Any Square
46|72|23|XLVI|3|-|16|The Chromosome Count
48|124|3|XLVIII|1|-|13|Factor Hoarder
49|57|7|XLIX|0|square|11|Seven Sevens, Very Tidy
51|72|17|LI|2|-|10|Looks Prime, Isn't
53|54|53|LIII|4|prime|15|Prime, Ordinary, Proud
55|72|11|LV|6|triangular,Fibonacci,palindrome|6|The Triple Threat
60|168|5|LX|4|-|14|Twelve Factors and a Clock
61|62|61|LXI|3|prime|9|One Minute Over
64|127|2|LXIV|0|square,cube|13|Square AND Cube, and Won't Shut Up About It
68|126|17|LXVIII|4|-|6|Four 17s in a Trench Coat
71|72|71|LXXI|7|prime|13|Prime, Stuck in the Seventies
74|114|37|LXXIV|7|-|7|Two 37s Holding Hands
77|96|11|LXXVII|4|palindrome|9|Sevens All the Way Down
88|180|11|LXXXVIII|7|palindrome|9|LXXXVIII: Roman for "Ouch"
89|90|89|LXXXIX|8|prime,Fibonacci|9|Fibonacci's Lanky Prime
93|128|31|XCIII|7|-|14|Also Looks Prime, Also Isn't
94|144|47|XCIV|6|-|11|Two 47s, No Plan
96|252|3|XCVI|4|-|9|The Factor Factory
100|217|5|C|0|square|1|The Big Round One
"""
TABLE_EXTRA = """\
4|7|2|IV|0|square,palindrome|93|Two Twos, Squared Away
5|6|5|V|1|prime,Fibonacci,palindrome|97|High Five: Prime, Fibonacci, Palindrome
13|14|13|XIII|3|prime,Fibonacci|12|Unlucky? It's Prime AND Fibonacci
19|20|19|XIX|3|prime|16|One Short of a Score
34|54|17|XXXIV|2|Fibonacci|12|Fibonacci in Disguise
38|60|19|XXXVIII|2|-|12|No Powers, Just Vibes
47|48|47|XLVII|2|prime|5|Two Short of a Square
59|60|59|LIX|5|prime|16|Last Prime Before Sixty
63|104|7|LXIII|1|-|6|One Short of a Square AND a Cube
66|144|11|LXVI|2|triangular,palindrome|11|Route 66: Triangular Palindrome
73|74|73|LXXIII|8|prime|10|Prime Both Ways
75|124|5|LXXV|6|-|12|Three Quarters of a Hundred
80|186|5|LXXX|1|-|6|So Close to 81 It Hurts
87|120|29|LXXXVII|6|-|9|The Prime Impersonator
92|168|23|XCII|8|-|13|Four 23s Pretending to Be One Number
95|120|19|XCV|5|-|16|Five 19s and a Dream
"""
FIELDS = ["n", "sof", "lpf", "roman", "dist", "powers", "pi", "nickname"]
CATEGORY_SPEC = [("sof", "highest"), ("lpf", "highest"), ("roman", "highest"), ("dist", "lowest"),
                 ("powers", "highest"), ("pi", "highest")]


def table_cards():
    out = []
    for deck, text in (("main", TABLE_MAIN), ("extra", TABLE_EXTRA)):
        for line in text.strip("\n").split("\n"):
            n, sof, lpf, rom, dist, pw, pi, nick = line.split("|")
            out.append({"n": int(n), "deck": deck, "nickname": nick, "sof": int(sof), "lpf": int(lpf), "roman": rom,
                        "dist": int(dist), "powers": [] if pw == "-" else pw.split(","), "pi": int(pi)})
    return out


# ------------------------------------------------------------------------------------------------ source 2
def machin_pi_decimals(count):
    """The `count` decimals of pi after the point, by Machin's formula in fixed-point integers (20 guard digits)."""
    scale = 10 ** (count + 20)

    def arctan_inv(x):                       # arctan(1/x) * scale, by its Taylor series
        total, term, k, sign = 0, scale // x, 1, 1
        x2 = x * x
        while term:
            total += sign * (term // k)
            term //= x2
            k += 2
            sign = -sign
        return total
    pi = 16 * arctan_inv(5) - 4 * arctan_inv(239)
    s = str(pi // 10 ** 20)                  # "3" and `count` decimals, the guard digits dropped
    assert s[0] == "3" and len(s) == count + 1, "Machin's sum has the wrong shape"
    return s[1:]


def sieve(limit):
    """Smallest prime factor of every number up to limit (0 and 1 have none: 0)."""
    spf = [0] * (limit + 1)
    for i in range(2, limit + 1):
        if spf[i] == 0:
            for j in range(i, limit + 1, i):
                if spf[j] == 0:
                    spf[j] = i
    return spf


SPF = sieve(100)


def factorise(n):
    f = {}
    while n > 1:
        p = SPF[n]
        f[p] = f.get(p, 0) + 1
        n //= p
    return f


def sof2(n):
    out = 1
    for p, k in factorise(n).items():
        out *= (p ** (k + 1) - 1) // (p - 1)
    return out


def lpf2(n):
    return max(factorise(n), default=0)


UNITS = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
TENS = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
HUNDREDS = ["", "C"]
VALUE = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


def roman2(n):
    return HUNDREDS[n // 100] + TENS[n // 10 % 10] + UNITS[n % 10]


def roman_value(s):
    total = 0
    for i, ch in enumerate(s):
        v = VALUE[ch]
        total += -v if i + 1 < len(s) and VALUE[s[i + 1]] > v else v
    return total


def is_square(m):
    return m >= 0 and math.isqrt(m) ** 2 == m


def dist2(n):
    r = math.isqrt(n)
    return min(n - r * r, (r + 1) ** 2 - n) if r < 10 else n - 100     # past 100 there is no square in the list


def icbrt(n):
    c = 0
    while (c + 1) ** 3 <= n:
        c += 1
    return c


def reverse_digits(n):
    r = 0
    while n:
        r, n = r * 10 + n % 10, n // 10
    return r


def powers2(n):
    has = {
        "prime": SPF[n] == n and n >= 2,
        "square": is_square(n),
        "cube": icbrt(n) ** 3 == n,
        "triangular": is_square(8 * n + 1),
        "Fibonacci": is_square(5 * n * n + 4) or is_square(5 * n * n - 4),
        "palindrome": reverse_digits(n) == n,
    }
    return [p for p in ["prime", "square", "cube", "triangular", "Fibonacci", "palindrome"] if has[p]]


def pi_count2(decimals, n):
    return len(re.findall("(?=%s)" % re.escape(str(n)), decimals))


def recompute(n, decimals):
    return {"sof": sof2(n), "lpf": lpf2(n), "roman": roman2(n), "dist": dist2(n), "powers": powers2(n),
            "pi": pi_count2(decimals, n)}


# ------------------------------------------------------------------------------------------------ the check
def run(build=None, json_text=None):
    """Every finding as a string; [] means PASS. `build` is gen.py's data (a fresh gen.build() by default) and
    `json_text` the committed file's text (read from disk by default): the plants pass in their own."""
    bad = []
    data = gen.build() if build is None else build
    if json_text is None:
        json_text = JSON_PATH.read_text(encoding="utf-8")

    # pi, three ways
    machin = machin_pi_decimals(gen.PI_DECIMALS)
    spigot = gen.pi_decimals(gen.PI_DECIMALS)
    if machin != spigot:
        i = next(i for i in range(len(machin)) if machin[i] != spigot[i])
        bad.append("pi: gen.py's spigot and Machin's formula first differ at decimal %d" % (i + 1))
    if machin[:10] != PI_FIRST10 or machin[990:1000] != PI_991_1000:
        bad.append("pi: decimals 1-10 or 991-1000 are not %s / %s" % (PI_FIRST10, PI_991_1000))

    # the JSON is gen.py's output, byte for byte
    if json_text != gen.dumps(data):
        try:
            committed = json.loads(json_text)
        except ValueError as e:
            committed = None
            bad.append("data/maffscards.json does not parse: %s" % e)
        bad.append("data/maffscards.json is not gen.py's output (a hand edit, or gen.py changed and was not run)")
    else:
        committed = data

    table = table_cards()
    if len([c for c in table if c["deck"] == "main"]) != 32 or len([c for c in table if c["deck"] == "extra"]) != 16:
        bad.append("TABLE: not 32 main and 16 extra")

    sources = [("gen.py", data.get("cards", []))]
    if committed is not None and committed is not data:
        sources.append(("data/maffscards.json", committed.get("cards", [])))
    for name, cards in sources:
        if [c.get("n") for c in cards] != [c["n"] for c in table]:
            bad.append("%s: the cards are not the contract's numbers in the contract's order" % name)
            continue
        if [c.get("deck") for c in cards] != [c["deck"] for c in table]:
            bad.append("%s: a card is in the wrong deck" % name)
        for got, want in zip(cards, table):
            n = want["n"]
            if set(got) != {"n", "deck", "nickname", "sof", "lpf", "roman", "dist", "powers", "pi"}:
                bad.append("%s card %d: fields %s" % (name, n, sorted(got)))
            again = recompute(n, machin)
            for f in ("sof", "lpf", "roman", "dist", "powers", "pi"):
                if got.get(f) != want[f]:
                    bad.append("%s card %d %s: %r, the contract's table says %r" % (name, n, f, got.get(f), want[f]))
                if again[f] != want[f]:
                    bad.append("card %d %s: the second method gives %r, the contract's table %r"
                               % (n, f, again[f], want[f]))
            if got.get("nickname") != want["nickname"]:
                bad.append("%s card %d nickname: %r" % (name, n, got.get("nickname")))
        for c in cards:                          # the numeral is right as well as the right length
            if roman_value(c.get("roman", "")) != c["n"]:
                bad.append("%s card %d: %s does not read back as %d" % (name, c["n"], c.get("roman"), c["n"]))

    for name, d in [("gen.py", data)] + ([("data/maffscards.json", committed)] if committed is not None else []):
        cats = d.get("categories", [])
        if [(c.get("key"), c.get("winner")) for c in cats] != CATEGORY_SPEC:
            bad.append("%s: categories are not %s" % (name, CATEGORY_SPEC))
        pi_label = next((c.get("label", "") for c in cats if c.get("key") == "pi"), "")
        if "1,000" not in pi_label:
            bad.append("%s: the pi label does not state the 1,000-digit limit: %r" % (name, pi_label))
        if any(not c.get("label") for c in cats):
            bad.append("%s: a category has no label" % name)
    if len({c["n"] for c in table}) != 48:
        bad.append("TABLE: a number appears twice")

    for path in SCANNED:
        if path.exists() and TRADE_MARK in path.read_text(encoding="utf-8").lower():
            bad.append("%s uses the registered trade mark the deck must never name" % path.relative_to(ROOT))
    return bad


# ------------------------------------------------------------------------------------------------ plants
def selftest():
    results = []

    def plant(name, fn, must):
        """Caught only if a finding names the planted card and category (`must`), not merely any difference."""
        try:
            found, err = [f for f in fn() if must in f], None
        except pc.StalePlant as e:
            results.append((name, False, str(e)))
            return
        except Exception as e:                       # an error is never a catch
            found, err = [], e
        ok = pc.is_caught(found, err)
        results.append((name, ok, (found[0] if found else "error: %r" % err)))

    def pi_off_by_one():
        real = gen.count_overlapping
        gen.count_overlapping = lambda hay, needle: real(hay, needle) + (1 if needle == "37" else 0)
        try:
            built = gen.build()
        finally:
            gen.count_overlapping = real
        if next(c for c in built["cards"] if c["n"] == 37)["pi"] != 13:
            raise pc.StalePlant("one pi count off by one", "card 37's pi count did not change")
        return run(build=built)

    def one_is_prime():
        real = gen.is_prime
        gen.is_prime = lambda n: n == 1 or real(n)
        try:
            built = gen.build()
        finally:
            gen.is_prime = real
        if "prime" not in built["cards"][0]["powers"]:
            raise pc.StalePlant("1 counted as prime", "card 1 did not gain prime")
        return run(build=built)

    def hand_edit():
        text = JSON_PATH.read_text(encoding="utf-8")
        edited = pc.apply_plant(text, '"sof": 217,', '"sof": 218,', name="a hand edit in the JSON (card 100's sum)")
        return run(json_text=edited)

    plant("one pi count off by one", pi_off_by_one, "gen.py card 37 pi: 13, the contract's table says 12")
    plant("1 counted as prime", one_is_prime, "gen.py card 1 powers")
    plant("a hand edit in the JSON", hand_edit, "data/maffscards.json card 100 sof: 218")
    clean = run()
    print("clean run: %s" % ("PASS" if not clean else "FAIL"))
    for f in clean:
        print("  " + f)
    for name, ok, why in results:
        print("plant %-26s %s  (%s)" % (name + ":", "CAUGHT" if ok else "MISSED", why))
    good = not clean and all(ok for _, ok, _ in results)
    print("SELFTEST " + ("PASS" if good else "FAIL"))
    return 0 if good else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    bad = run()
    for f in bad:
        print("FAIL: " + f)
    if bad:
        return 1
    print("PASS: 48 cards (32 main, 16 extra), every value equal in gen.py, the second method, the contract's table "
          "and data/maffscards.json; pi's 1,000 decimals equal by Machin and the spigot")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
