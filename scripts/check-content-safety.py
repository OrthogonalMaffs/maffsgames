#!/usr/bin/env python3
"""Canon SR-14: sensitive content, in three tiers (Jon, 4 Oct 2026).

    python scripts/check-content-safety.py              # CI: fails on a NEW hit, or a KNOWN entry that is stale
    python scripts/check-content-safety.py --known      # also list every KNOWN hit with its line
    python scripts/check-content-safety.py --selftest   # planted hits must fail; the tree as it is must pass
    python scripts/check-content-safety.py --root <copy of the repo>

SR-14 (canon §0.3):
  (a) Banned everywhere: death, fatal outcomes, suicide, self-harm, abuse, drowning, violence, family breakdown.
  (b) Banned in jokes, silly theories and humour: everything in (a), plus illness and injury.
  (c) Allowed in neutral exam-style contexts: illness, medical tests, screening, patients, hospitals,
      phrased as the exam boards phrase them.
  Established technical terms are not hits ("Prisoner's Dilemma", "base rate neglect"); titles and humour
  Jon has approved are allowlisted ("Tax Theft").

What the scan does, per tier:
  (a) TIER_A words fail anywhere in a game's or escape room's student-facing text.
  (b) TIER_B words (illness, injury) fail only inside a humour field, where the scan can tell one: the
      value of an object field named in HUMOUR_KEYS (joke:, theory:, conspiracies: [...], quip:, ...).
      Elsewhere they are tier (c) and are not scanned: whether a context is phrased as an exam board would
      phrase it is a human judgement, not a word match.
  ALLOW phrases are blanked out before matching.

What it reads: every games/**/*.html and *.js and escape-rooms/**/*.html and *.js file, with CSS (<style>
blocks), HTML comments and JavaScript comments removed, so it reads the page text and the question banks,
not the code's own notes. Whole words, case-insensitive.

It is a word list, so it is a net, not a judge: a hit means "look". Every hit present when a tier was set
is in KNOWN, for Jon to rule on: reported, never failed. A hit not in KNOWN fails (a new one, or one more
of a word in a file than KNOWN records); so does a KNOWN entry whose file now has fewer ("stale: lower the
count"), so the list stays true as games are fixed. The tier-(a) KNOWN hits are todo's SR-14 fix batch.

Deliberately not words: `die` and `dies` (a fair die); `hurt`, `attack`, `shoot`, `fire`, `war` (game
mechanics and titles); `hanging` (masses on strings, open drawers; the one unsafe use, the old correlation
pair, has its own check in scripts/check-resit-fixes.py). Crime is not in SR-14 as amended (4 Oct 2026),
so crime words are not scanned. Change a list here, never in a game, and update KNOWN in the same PR.
"""
import argparse, collections, pathlib, re, sys

BASE = pathlib.Path(__file__).resolve().parent.parent
GLOBS = ("games/**/*.html", "games/**/*.js", "escape-rooms/**/*.html", "escape-rooms/**/*.js")

# Tier (a): banned everywhere. Whole words; a trailing \w* takes the word's other forms.
TIER_A = {
    "death": r"died|dying|deaths?|dead|deadly|kill(?:s|ed|ing|er|ers)?|murder\w*|fatal\w*|funerals?|"
             r"coffins?|corpses?|graveyards?|mortality",
    "drowning": r"drown\w*",
    "suicide or self-harm": r"suicid\w*|self-harm\w*|overdose\w*",
    "abuse": r"abus\w*|neglect\w*|bull(?:y|ying|ied)",
    "violence": r"violen\w*|assault\w*|weapons?|guns?|knife|knives|stab(?:s|bed|bing)?",
    "family breakdown": r"divorc\w*|orphan\w*|custody|widow\w*|bereave\w*",
}
# Tier (b): banned in humour only (tier (c) elsewhere).
TIER_B = {
    "illness": r"ill|illness\w*|disease\w*|cancer\w*|virus\w*|flu|sick\w*|infect\w*|hospital\w*|patients?|"
               r"symptoms?|diagnos\w*|tumou?rs?|diabet\w*|vaccin\w*|medic\w*",
    "injury": r"injur\w*|wound(?:s|ed)?|bleed\w*|accidents?|crash(?:es|ed)?|fractured?",
}
# Not hits: established technical terms, and titles Jon has approved.
ALLOW = [r"prisoner'?s'? dilemma", r"prisoners'? dilemma", r"base[- ]rate neglect", r"tax[- ]theft"]
# Object fields whose values are humour: joke:, theory:, conspiracies: [...] and the like.
HUMOUR_KEYS = r"jokes?|theory|theories|conspirac\w*|quips?|puns?|gags?|banter|roasts?|humou?r\w*|silly\w*|tinfoil\w*"


def _rx(groups):
    return re.compile(r"\b(" + "|".join("(?:%s)" % v for v in groups.values()) + r")\b", re.I)


A_RE, B_RE = _rx(TIER_A), _rx(TIER_B)
ALLOW_RE = re.compile("|".join(ALLOW), re.I)
_STR = r"'(?:\\.|[^'\\\n])*'|\"(?:\\.|[^\"\\\n])*\"|`[^`]*`"
HUMOUR_RE = re.compile(r"(?<![\w$])(?:%s)\s*:\s*(%s|\[(?:\s|,|%s)*\])" % (HUMOUR_KEYS, _STR, _STR), re.I)


def theme(word):
    for groups in (TIER_A, TIER_B):
        for t, v in groups.items():
            if re.fullmatch(v, word, re.I):
                return t
    return "?"


def tier(word):
    return "a" if A_RE.fullmatch(word) else "b"


def _blank(m):
    return re.sub(r"[^\n]", " ", m.group(0))


def student_text(src):
    """The file with CSS, HTML comments, JS comments and allowlisted phrases blanked (offsets kept)."""
    src = re.sub(r"<style\b.*?</style>", _blank, src, flags=re.S | re.I)
    src = re.sub(r"<!--.*?-->", _blank, src, flags=re.S)
    src = re.sub(r"/\*.*?\*/", _blank, src, flags=re.S)
    src = re.sub(r"(?m)^\s*//.*$", _blank, src)
    src = re.sub(r"(?m)(?<![:'\"\\])\s//\s.*$", _blank, src)    # a trailing "  // note", never a URL
    return ALLOW_RE.sub(_blank, src)


def hits_in(text):
    """[(line, word)] for one file: tier (a) anywhere, tier (b) inside humour fields."""
    text = student_text(text)
    line = lambda pos: text.count("\n", 0, pos) + 1
    out = [(line(m.start()), m.group(1).lower()) for m in A_RE.finditer(text)]
    for h in HUMOUR_RE.finditer(text):
        out += [(line(h.start(1) + m.start()), m.group(1).lower()) for m in B_RE.finditer(h.group(1))]
    return sorted(out)


def terms(text, humour=False):
    """The SR-14 words in one string: tier (a), plus tier (b) if the string is humour."""
    text = ALLOW_RE.sub(_blank, text)
    found = [m.group(1).lower() for m in A_RE.finditer(text)]
    if humour:
        found += [m.group(1).lower() for m in B_RE.finditer(text)]
    return sorted(set(found))


def scan(root, override=None):
    """{relative path: [(line, word)]} for every file with a hit. override: {rel: text} replaces a file."""
    out, seen = {}, set()
    for g in GLOBS:
        for f in sorted(root.glob(g)):
            rel = f.relative_to(root).as_posix()
            if rel in seen:
                continue
            seen.add(rel)
            text = (override or {}).get(rel)
            if text is None:
                text = f.read_text(encoding="utf-8", errors="replace")
            h = hits_in(text)
            if h:
                out[rel] = h
    return out


# Every hit present on 4 Oct 2026 (SR-14 as amended that evening), for Jon to rule on: file -> {word: count}.
# Reported, never failed. Lower a count (or drop the entry) in the PR that removes the words.
KNOWN = {
    "escape-rooms/prom-budget/room.js": {"dead": 1},
    "games/bearing-blitz/index.html": {"dead": 1},
    "games/core-maths-paper2a/index.html": {"drowning": 2, "drownings": 2},
    "games/given-that/index.html": {"fatal": 4},
    "games/maths-court/index.html": {"drowning": 4, "drownings": 3},
    "games/probability-paradox/index.html": {"neglected": 1},
    "games/proof-builder/index.html": {"kills": 1},
    "games/the-perfect-prank/index.html": {"dead": 1},
    "games/trig-wars/index.html": {"dead": 1},
    "games/truth-buster/index.html": {"drownings": 1},
    "games/wrong-on-the-internet/index.html": {"drowning": 5},
}


def compare(found, known):
    """(errors, known_hits): a new or extra hit, or a stale KNOWN entry, is an error."""
    errors, known_hits = [], 0
    for rel in sorted(set(found) | set(known)):
        have = collections.Counter(w for _, w in found.get(rel, []))
        want = known.get(rel, {})
        for word in sorted(set(have) | set(want)):
            n, k = have.get(word, 0), want.get(word, 0)
            known_hits += min(n, k)
            if n > k:
                lines = [str(ln) for ln, w in found[rel] if w == word]
                errors.append("%s: %r (tier %s, %s) %d time(s), KNOWN allows %d; line(s) %s. SR-14: rewrite it, "
                              "or ask Jon to rule" % (rel, word, tier(word), theme(word), n, k, ", ".join(lines)))
            elif n < k:
                errors.append("%s: KNOWN records %r %d time(s), the file has %d: stale, lower the count in KNOWN"
                              % (rel, word, k, n))
    return errors, known_hits


def selftest(root):
    """Planted hits must fail, a stale KNOWN entry must fail, and what SR-14 allows must not be a hit."""
    if compare(scan(root), KNOWN)[0]:
        return []                       # the real run reports them
    target = "games/correlation-or-coincidence/index.html"
    clean = (root / target).read_text(encoding="utf-8")
    faults = {
        "tier (a) in a game's page text": ({target: clean.replace("</body>", "<p>Nobody drowned.</p></body>")}, KNOWN),
        "tier (a) in a question bank string": ({target: clean.replace("explain:'Every mile driven", "explain:'A fatal mile. Every mile driven")}, KNOWN),
        "tier (b) in a joke": ({target: clean.replace(" joke:'Butter makes", " joke:'Butter cures flu and makes")}, KNOWN),
        "tier (b) in a list of theories": ({target: clean.replace("</body>", "<script>var x={conspiracies:['a','the hospital did it']};</script></body>")}, KNOWN),
        "a stale KNOWN entry": (None, dict(KNOWN, **{target: {"murder": 1}})),
    }
    missed = [name for name, (override, known) in faults.items() if not compare(scan(root, override), known)[0]]
    quiet = {
        "comments, CSS and 'die'": "<style>.dead{}</style><!-- murder --><script>/* drowning */\n// killed\n</script><p>Roll a fair die.</p>",
        "tier (b) in a neutral context (tier c)": "<p>A test for a disease is given to 1000 patients in a hospital.</p>",
        "allowlisted terms": "<h1>Prisoner's Dilemma</h1><p>Base rate neglect.</p><a href='/games/tax-theft/'>Tax Theft</a>",
    }
    for name, text in quiet.items():
        if hits_in(text):
            missed.append("%s must not be a hit (got %s)" % (name, hits_in(text)))
    n = len(faults) + len(quiet)
    print("self-test: %d of %d planted cases right" % (n - len(missed), n))
    return ["self-test: wrong: " + m for m in missed]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(BASE))
    ap.add_argument("--known", action="store_true", help="list every KNOWN hit with its line")
    ap.add_argument("--selftest", action="store_true", help="run only the self-test")
    args = ap.parse_args()
    root = pathlib.Path(args.root)
    errors = selftest(root)
    if args.selftest:
        print("FAIL" if errors else "OK")
        return 1 if errors else 0
    found = scan(root)
    errs, known_hits = compare(found, KNOWN)
    errors += errs
    files = sorted(r for r in found if r in KNOWN)
    by_tier = collections.Counter(tier(w) for r in files for _, w in found[r])
    print("SR-14 content scan: %d files read; %d KNOWN hit(s) in %d file(s) (tier a: %d, tier b in humour: %d), "
          "for Jon to rule on (reported, not failed)" % (sum(1 for g in GLOBS for _ in root.glob(g)), known_hits,
                                                        len(files), by_tier["a"], by_tier["b"]))
    for rel in files:
        c = collections.Counter(w for _, w in found[rel])
        print("  KNOWN %-48s %s" % (rel, ", ".join("%s %d (%s)" % (w, n, tier(w)) for w, n in c.most_common())))
        if args.known:
            for ln, w in found[rel]:
                print("        line %-5d %s (tier %s, %s)" % (ln, w, tier(w), theme(w)))
    for e in errors:
        print("FAIL " + e)
    print("FAIL" if errors else "OK")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
