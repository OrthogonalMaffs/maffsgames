#!/usr/bin/env python3
"""Canon SR-14: question contexts, examples and jokes never involve death, injury, illness, self-harm,
crime, abuse or family breakdown.

    python scripts/check-content-safety.py              # CI: fails on a NEW hit, or a KNOWN entry that is stale
    python scripts/check-content-safety.py --known      # also list every KNOWN hit with its line
    python scripts/check-content-safety.py --selftest   # planted hits must fail; the tree as it is must pass
    python scripts/check-content-safety.py --root <copy of the repo>

Why (Jon, 4 Oct 2026): the resit audit found a "suicides by hanging" pair played for laughs in
correlation-or-coincidence, in front of the site's priority audience (canon §0). One game was fixed by hand
(PR #36); the class is "student-facing text nobody screened". This scan is the screen, for every game.

What it reads: every games/**/*.html and *.js file and every escape-rooms/**/*.html and *.js file, with CSS
(<style> blocks), HTML comments and JavaScript comments removed, so it reads the page text and the
question banks the scripts hold, not the code's own notes. It matches whole words (case-insensitive) from
WORDS below, one list per SR-14 theme.

It is a word list, so it is a net, not a judge. A hit is "this needs a human look", never "this is
unsafe": `neglect` is also "base rate neglect", `crash` can be a program. Every hit present when the check
was written is in KNOWN, for Jon to rule on: KNOWN hits are reported, never failed. A hit not in KNOWN
fails (a new one, or one more of a word in a file than KNOWN records). A KNOWN entry whose file now has
fewer of that word fails too ("stale: lower the count"), so the list stays true as games are fixed.

Deliberately not in WORDS: `die` and `dies` (a fair die, in every probability game); `hurt`, `attack`,
`shoot`, `fire`, `war` (game mechanics and titles: Stat Attack, Trig Wars); `blood` (blood groups are a
standard data context, not illness); `split`, `separated` (maths words); `hanging` (16 hits on 4 Oct 2026, all
masses on strings, open drawers and cables; the one unsafe use, the correlation pair, has its own check in
scripts/check-resit-fixes.py). Add a word here, never in a
game; changing WORDS changes which hits are KNOWN, so re-run with --known and update KNOWN in that PR.
"""
import argparse, collections, pathlib, re, sys

BASE = pathlib.Path(__file__).resolve().parent.parent
GLOBS = ("games/**/*.html", "games/**/*.js", "escape-rooms/**/*.html", "escape-rooms/**/*.js")

# One list per SR-14 theme. Whole words; a trailing \w* takes the word's other forms.
WORDS = {
    "death": r"died|dying|deaths?|dead|deadly|kill(?:s|ed|ing|er|ers)?|murder\w*|fatal\w*|funerals?|"
             r"coffins?|corpses?|drown\w*|mortality|graveyards?",
    "injury": r"injur\w*|wound(?:s|ed)?|bleed\w*|accidents?|crash(?:es|ed)?|fractured?",
    "illness": r"ill|illness\w*|disease\w*|cancer\w*|virus\w*|flu|sick\w*|infect\w*|hospital\w*|patients?|"
               r"symptoms?|diagnos\w*|tumou?rs?|diabet\w*|vaccin\w*|medic\w*|overdose\w*",
    "self-harm": r"suicid\w*|self-harm\w*",
    "crime": r"crim\w*|theft|thie(?:f|ves)|steal\w*|stole|stolen|robber\w*|robs?|robbed|burglar\w*|"
             r"prisons?|prisoners?|jail\w*|arrest\w*|police|fraud\w*|scam\w*|shoplift\w*|pira(?:cy|tes?)|smuggl\w*",
    "abuse": r"abus\w*|bull(?:y|ying|ied)|neglect\w*|assault\w*|violen\w*|weapons?|guns?|knife|knives",
    "family breakdown": r"divorc\w*|orphan\w*|custody|widow\w*|bereave\w*",
}
WORD_RE = re.compile(r"\b(" + "|".join("(?:%s)" % v for v in WORDS.values()) + r")\b", re.I)
THEME_RE = {t: re.compile(r"^(?:%s)$" % v, re.I) for t, v in WORDS.items()}

# Every hit present on 4 Oct 2026 (the check's first run), for Jon to rule on: file -> {word: count}.
# Reported, never failed. Lower a count (or drop the entry) in the PR that removes the words.
KNOWN = {
    "escape-rooms/canteen-hack/room.js": {"accident": 1},
    "escape-rooms/prom-budget/room.js": {"dead": 1},
    "escape-rooms/rugby-mud/room.js": {"thief": 1},
    "games/bearing-blitz/index.html": {"dead": 1},
    "games/better-value/index.html": {"accident": 1, "scam": 1, "theft": 1},
    "games/core-maths-paper1/index.html": {"patients": 1},
    "games/core-maths-paper2a/index.html": {"drowning": 2, "drownings": 2},
    "games/core-maths-paper2b/index.html": {"crime": 4, "illness": 1},
    "games/expectation-station/index.html": {"patient": 2, "patients": 1, "sick": 8},
    "games/given-that/index.html": {"accident": 1, "cancer": 4, "disease": 5, "fatal": 4, "flu": 12, "injured": 4, "injuries": 2, "injury": 4, "patient": 1, "patients": 2},
    "games/gradient-hunter/index.html": {"hospital": 1, "medication": 3, "patient": 2},
    "games/graph-sketcher/index.html": {"fracture": 1},
    "games/maths-court/index.html": {"drowning": 4, "drownings": 3},
    "games/prisoners-dilemma/index.html": {"crash": 1, "patient": 1, "prisoner": 8, "prisoners": 8},
    "games/probability-paradox/index.html": {"crash": 1, "crashes": 1, "disease": 15, "hospital": 5, "medical": 1, "neglect": 5, "neglected": 1, "patient": 1, "patients": 1},
    "games/probability-pioneer/index.html": {"medicine": 1},
    "games/proof-builder/index.html": {"kills": 1},
    "games/regression-rumble/_withdrawn.html": {"crime": 1},
    "games/screening-room/index.html": {"cancer": 13, "crime": 1, "diabetes": 9, "diabetics": 2, "diagnosis": 1, "disease": 3, "flu": 3, "fraud": 3, "fraudulent": 3, "medical": 1, "patient": 1, "patients": 15, "police": 2, "shoplifting": 1, "stolen": 3, "symptoms": 2, "vaccinated": 1, "vaccine": 3},
    "games/spot-the-muppet/index.html": {"patients": 1, "steals": 1},
    "games/tax-theft/index.html": {"theft": 13},
    "games/terrible-advice/index.html": {"patients": 1, "steals": 1},
    "games/test-the-claim/index.html": {"accident": 1, "accidents": 2, "hospital": 2, "patients": 3},
    "games/the-perfect-prank/index.html": {"dead": 1},
    "games/trig-wars/index.html": {"dead": 1},
    "games/truth-buster/index.html": {"drownings": 1},
    "games/word-problem-decoder/index.html": {"hospital": 2, "patients": 4},
    "games/wrong-on-the-internet/index.html": {"drowning": 5},
}


def theme(word):
    return next(t for t, rx in THEME_RE.items() if rx.match(word))


def _blank(m):
    return "\n" * m.group(0).count("\n")


def student_text(src):
    """The file with CSS, HTML comments and JS comments blanked out (line numbers kept)."""
    src = re.sub(r"<style\b.*?</style>", _blank, src, flags=re.S | re.I)
    src = re.sub(r"<!--.*?-->", _blank, src, flags=re.S)
    src = re.sub(r"/\*.*?\*/", _blank, src, flags=re.S)
    src = re.sub(r"(?m)^\s*//.*$", "", src)
    src = re.sub(r"(?m)(?<![:'\"\\])\s//\s.*$", "", src)    # a trailing "  // note", never a URL
    return src


def hits_in(text):
    """[(line, word)] for one file's student-facing text."""
    text = student_text(text)
    return [(text.count("\n", 0, m.start()) + 1, m.group(1).lower()) for m in WORD_RE.finditer(text)]


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
                errors.append("%s: %r (%s) %d time(s), KNOWN allows %d; line(s) %s. SR-14: rewrite it, "
                              "or ask Jon to rule and add it to KNOWN" % (rel, word, theme(word), n, k, ", ".join(lines)))
            elif n < k:
                errors.append("%s: KNOWN records %r %d time(s), the file has %d: stale, lower the count in KNOWN"
                              % (rel, word, k, n))
    return errors, known_hits


def selftest(root):
    """A planted hit must fail; so must a stale KNOWN entry; the tree as it is must pass."""
    base_found = scan(root)
    if compare(base_found, KNOWN)[0]:
        return []                       # the real run reports them
    target = "games/correlation-or-coincidence/index.html"
    clean = (root / target).read_text(encoding="utf-8")
    faults = {
        "a new SR-14 word in a game's text": ({target: clean.replace("</body>", "<p>The patients in the ward.</p></body>")}, KNOWN),
        "a SR-14 word inside a question bank string": ({target: clean.replace("explain:'Every mile driven", "explain:'A crash. Every mile driven")}, KNOWN),
        "a stale KNOWN entry": (None, dict(KNOWN, **{target: {"murder": 1}})),
    }
    missed = []
    for name, (override, known) in faults.items():
        if not compare(scan(root, override), known)[0]:
            missed.append(name)
    # And what must NOT be a hit: comments, CSS, and the excluded words.
    quiet = "<style>.dead{}</style><!-- injury --><script>/* police */\n// theft\n</script><p>Roll a fair die.</p>"
    if hits_in(quiet):
        missed.append("comments, CSS and 'die' must not be hits (got %s)" % hits_in(quiet))
    print("self-test: %d of %d planted faults caught" % (len(faults) + 1 - len(missed), len(faults) + 1))
    return ["self-test: not caught: " + m for m in missed]


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
    print("SR-14 content scan: %d files read; %d KNOWN hit(s) in %d file(s), for Jon to rule on (reported, not failed)"
          % (sum(1 for g in GLOBS for _ in root.glob(g)), known_hits, len(files)))
    for rel in files:
        c = collections.Counter(w for _, w in found[rel])
        print("  KNOWN %-48s %s" % (rel, ", ".join("%s %d" % (w, n) for w, n in c.most_common())))
        if args.known:
            for ln, w in found[rel]:
                print("        line %-5d %s (%s)" % (ln, w, theme(w)))
    for e in errors:
        print("FAIL " + e)
    print("FAIL" if errors else "OK")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
