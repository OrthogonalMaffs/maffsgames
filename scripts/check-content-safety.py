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

What it reads (Jon's ruling, 4 Oct 2026: "the scan checks text a player sees; code identifiers are
excluded"): every games/**/*.html and *.js and escape-rooms/**/*.html and *.js file, reduced by
displayed() to the text a player can be shown, everything else blanked with its line numbers kept:
  HTML: text nodes and attribute values, except CODE_ATTRS (class, id, style, href, src, ...); on*="..."
        is read as JavaScript; <style>, comments and tag names are blanked.
  JS (<script> blocks, .js files): string literals and template-literal text (${...} read as JavaScript),
        each read as an HTML fragment, since a string may be innerHTML. Identifiers, keywords, numbers,
        regex literals and comments are code. So are the strings code uses as names, not words: quoted
        object keys and case labels; class names and ids (.className = / .id = ..., classList.add/remove/
        toggle/contains/replace(...)); selectors (getElementById, querySelector(All), closest, matches,
        getElementsByClassName); attribute names, and setAttribute's value for a CODE_ATTRS name.
  A string the code shows (textContent, innerHTML, a bank field, a ternary branch) is still read.
Whole words, case-insensitive.

It is a word list, so it is a net, not a judge: a hit means "look". Every hit present when a tier was set
is in KNOWN, for Jon to rule on: reported, never failed. A hit not in KNOWN fails (a new one, or one more
of a word in a file than KNOWN records); so does a KNOWN entry whose file now has fewer ("stale: lower the
count"), so the list stays true as games are fixed. The tier-(a) KNOWN hits are todo's SR-14 fix batch.

Deliberately not words: `die` and `dies` (a fair die); `hurt`, `attack`, `shoot`, `fire`, `war` (game
mechanics and titles); `hanging` (masses on strings, open drawers; the one unsafe use, the old correlation
pair, has its own check in scripts/check-resit-fixes.py). Crime is not in SR-14 as amended (4 Oct 2026),
so crime words are not scanned. Change a list here, never in a game, and update KNOWN in the same PR.
"""
import argparse, collections, functools, pathlib, re, sys

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
# Not hits: established technical terms, titles Jon has approved, and the idioms Jon ruled not SR-14
# content (4 Oct 2026, 20:06): the pot plants (the-perfect-prank, prom-budget), Proof Builder's "kills the
# claim" and Probability Paradox's base-rate question ("What has the doctor neglected?").
ALLOW = [r"prisoner'?s'? dilemma", r"prisoners'? dilemma", r"base[- ]rate neglect", r"tax[- ]theft",
         r"half dead", r"three[- ]quarters dead", r"kills the claim", r"doctor neglected"]
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


# ---------------------------------------------------------------- displayed text (Jon's ruling, 4 Oct 2026)
# Attributes whose values are code, never shown as words. Any other attribute (alt, title, placeholder,
# aria-*, value, content, data-*, ...) is read: the list is of what to skip, so an unlisted one stays scanned.
CODE_ATTRS = {"class", "id", "style", "href", "src", "srcset", "type", "name", "for", "rel", "lang", "charset",
              "http-equiv", "role", "target", "method", "action", "xmlns", "xmlns:xlink", "xlink:href",
              "viewbox", "d", "transform", "crossorigin", "integrity", "referrerpolicy", "inputmode",
              "autocomplete", "pattern", "tabindex", "form", "async", "defer", "width", "height"}
_TAG = re.compile(r"<!--.*?-->|<!(?!--)[^>]*>|<(/?)([A-Za-z][\w:.-]*)((?:\"[^\"]*\"|'[^']*'|[^'\">])*)>", re.S)
_ATTR = re.compile(r"([^\s\"'=<>/\\]+)(?:\s*=\s*(\\\"(?:(?!\\\").)*\\\"|\\'(?:(?!\\').)*\\'|\"[^\"]*\"|'[^']*'|[^\s>]+))?",
                   re.S)
_RAW = re.compile(r"<(script|style)\b[^>]*>(.*?)</\1\s*>", re.S | re.I)
# A string escape that is not a character on screen (\n, \u2014, ...): blanked so "\nDead" reads "Dead".
_ESC = re.compile(r"\\(?:u\{[0-9A-Fa-f]+\}|u[0-9A-Fa-f]{4}|x[0-9A-Fa-f]{2}|[nrtbfv0])")
# A call whose string arguments are class names, ids or selectors.
_DOM_CALL = re.compile(r"(?:classList\s*\.\s*(?:add|remove|toggle|contains|replace)|\b(?:getElementById|"
                       r"getElementsByClassName|getElementsByTagName|querySelector|querySelectorAll|closest|"
                       r"matches))\s*$")
_ATTR_CALL = re.compile(r"\b(?:set|get|has|remove|toggle)Attribute(?:NS)?\s*$")
_NAME_ASSIGN = re.compile(r"\s*\+?=(?!=)")
_NEXT = re.compile(r"\s*")
_WS = re.compile(r"[ \t\r]+")
_IDENT = re.compile(r"(?:[^\W\d]|\$)[\w$]*")
_NUM = re.compile(r"[\w.]+")
_REGEX_AFTER = set("(,=:[!&|?{};+-*%<>~^") | {"", "return", "typeof", "case", "do", "else", "in", "of", "new",
                                              "delete", "void", "throw", "instanceof", "yield", "await"}
_CONTINUES = set("+-*/%?:=(,|&[{<>!.")


def _keep(text, a, b, base, out, esc):
    """Copy text[a:b] into out at base+a (a string's escapes and template placeholders blanked)."""
    seg = text[a:b]
    if esc and "\\" in seg:
        seg = _ESC.sub(lambda m: " " * len(m.group(0)), seg)
    for k, ch in enumerate(seg):
        if ch not in "\n\0":
            out[base + a + k] = ch


def _html(text, base, out, top):
    """Keep the displayed parts of an HTML page (top) or of an HTML fragment held in a JS string."""
    pos, n = 0, len(text)
    raw = list(_RAW.finditer(text)) if top else []
    while pos < n:
        r = next((m for m in raw if m.start() >= pos), None)
        t = _TAG.search(text, pos, r.start() if r else n)
        if t is None and r is None:
            _keep(text, pos, n, base, out, not top)
            break
        m = t if t is not None else r
        _keep(text, pos, m.start(), base, out, not top)
        if m is r:                                   # <script> read as JS, <style> blanked
            if r.group(1).lower() == "script":
                _js(text, r.start(2), r.end(2), out)
        elif m.group(2):                             # a tag: only its displayed attribute values
            attrs, a0 = m.group(3), m.start(3)
            for a in _ATTR.finditer(attrs):
                name = a.group(1).lower()
                if a.group(2) is None or name in CODE_ATTRS:
                    continue
                vs, ve = a0 + a.start(2), a0 + a.end(2)
                if name.startswith("on") and top:
                    _js(text, vs + 1, ve - 1, out)
                else:
                    _keep(text, vs, ve, base, out, not top)
        pos = m.end()


def _string_end(src, pos, end):
    """Index after the quote string starting at pos (an unterminated one ends at its line)."""
    q, i = src[pos], pos + 1
    while i < end:
        c = src[i]
        if c == "\\":
            i += 2
            continue
        if c == q:
            return i + 1
        if c == "\n":
            return i
        i += 1
    return end


def _js(src, pos, end, out, brace_stop=False):
    """Keep the displayed strings of the JavaScript in src[pos:end]; returns where it stopped (at the '}'
    closing a template's ${...} when brace_stop)."""
    frames, depth, assign, prev = [], 0, None, ""
    while pos < end:
        c = src[pos]
        if c in " \t\r":
            pos = _WS.match(src, pos, end).end()
            continue
        if c == "\n":
            if assign and assign == (len(frames), depth) and prev not in _CONTINUES:
                assign = None
            pos += 1
            continue
        two = src[pos:pos + 2]
        if two == "//":
            nl = src.find("\n", pos, end)
            pos = end if nl < 0 else nl
            continue
        if two == "/*":
            close = src.find("*/", pos + 2, end)
            pos = end if close < 0 else close + 2
            continue
        if c in "'\"`":
            if c == "`":
                after, exprs, i = None, [], pos + 1
                while i < end:
                    if src[i] == "\\":
                        i += 2
                    elif src[i] == "`":
                        after = i + 1
                        break
                    elif src[i:i + 2] == "${":
                        close = _js(src, i + 2, end, out, brace_stop=True)
                        exprs.append((i, close + 1))
                        i = close + 1
                    else:
                        i += 1
                after = after or end
                body = list(src[pos + 1:after - 1])
                for s, e in exprs:
                    body[s - pos - 1:e - pos - 1] = "\0" * (e - s)
                body = "".join(body)
            else:
                after = _string_end(src, pos, end)
                body = src[pos + 1:after - 1]
            frame = frames[-1] if frames else None
            nxt = _NEXT.match(src, after, end)
            is_code = (assign is not None
                       or (frame is not None and frame["dom"])
                       or (frame is not None and frame["attr"] and (frame["args"] == 0 or frame["first"] in CODE_ATTRS))
                       or prev == "case"
                       or (prev in ("{", ",") and nxt.end() < end and src[nxt.end()] == ":" and c != "`"))
            if frame is not None and frame["attr"] and frame["args"] == 0:
                frame["first"] = body.lower()
            if not is_code:
                _html(body, pos + 1, out, top=False)
            prev, pos = "str", after
            continue
        if c == "/" and prev in _REGEX_AFTER:
            i, cls = pos + 1, False
            while i < end and src[i] != "\n":
                if src[i] == "\\":
                    i += 2
                    continue
                if src[i] == "[":
                    cls = True
                elif src[i] == "]":
                    cls = False
                elif src[i] == "/" and not cls:
                    break
                i += 1
            if i < end and src[i] == "/":
                pos = i + 1
                while pos < end and (src[pos].isalnum() or src[pos] in "_$"):
                    pos += 1
                prev = "re"
                continue
        if c.isalpha() or c in "_$":
            i = _IDENT.match(src, pos, end).end()
            word = src[pos:i]
            if (word in ("className", "id") and src[max(0, pos - 40):pos].rstrip().endswith(".")
                    and _NAME_ASSIGN.match(src, i)):
                assign = (len(frames), depth)
            prev, pos = word, i
            continue
        if c.isdigit():
            pos = _NUM.match(src, pos, end).end()
            prev = "num"
            continue
        if c == "(":
            before = src[max(0, pos - 80):pos]
            frames.append({"dom": bool(_DOM_CALL.search(before)), "attr": bool(_ATTR_CALL.search(before)),
                           "args": 0, "first": None})
        elif c == ")":
            if frames:
                frames.pop()
            if assign and len(frames) < assign[0]:
                assign = None
        elif c == "{":
            depth += 1
        elif c == "}":
            if brace_stop and depth == 0:
                return pos
            depth -= 1
            if assign and depth < assign[1]:
                assign = None
        elif c == ";":
            if assign and assign == (len(frames), depth):
                assign = None
        elif c == "," and frames:
            frames[-1]["args"] += 1
        prev = c
        pos += 1
    return pos


def displayed(src, js=False):
    """src with everything a player cannot be shown blanked (newlines kept, so offsets and lines hold)."""
    out = ["\n" if ch == "\n" else " " for ch in src]
    if js:
        _js(src, 0, len(src), out)
    else:
        _html(src, 0, out, top=True)
    return "".join(out)


@functools.lru_cache(maxsize=None)
def hits_in(text, js=False):
    """[(line, word)] for one file: tier (a) in displayed text, tier (b) in displayed text inside humour fields."""
    shown = ALLOW_RE.sub(_blank, displayed(text, js))
    code = student_text(text)                    # the humour keys are code, so they are found in the source
    line = lambda pos: shown.count("\n", 0, pos) + 1
    out = [(line(m.start()), m.group(1).lower()) for m in A_RE.finditer(shown)]
    for h in HUMOUR_RE.finditer(code):
        out += [(line(h.start(1) + m.start()), m.group(1).lower())
                for m in B_RE.finditer(shown[h.start(1):h.end(1)])]
    return tuple(sorted(out))


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
            h = hits_in(text, js=rel.endswith(".js"))
            if h:
                out[rel] = h
    return out


# Every hit present on 4 Oct 2026 (SR-14 as amended that evening), for Jon to rule on: file -> {word: count}.
# Reported, never failed. Lower a count (or drop the entry) in the PR that removes the words. 5 Oct 2026: the
# idioms and the class names Jon ruled out of SR-14 (4 Oct, 20:06) are no longer hits (ALLOW, displayed()).
KNOWN = {
    "games/truth-buster/index.html": {"drownings": 1},
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
    missed, n = [], 0
    if not compare(scan(root), KNOWN)[0]:     # else the real run reports the tree's own errors
        missed, n = _selftest_files(root)
    m2, n2 = _selftest_snippets()
    print("self-test: %d of %d planted cases right" % (n + n2 - len(missed) - len(m2), n + n2))
    return ["self-test: wrong: " + m for m in missed + m2]


def _selftest_files(root):
    """Planted hits in a real game must fail, and a stale KNOWN entry must fail."""
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
    return missed, len(faults)


def _selftest_snippets():
    """Displayed text only, and what SR-14 allows, on planted snippets (run whatever state the tree is in)."""
    missed = []
    # Displayed text only (Jon, 4 Oct 2026): (text, is a .js file). The same word must be a hit as words a
    # player sees, and must not be as code.
    loud = {
        "tier (a) in a displayed JS string": ("<script>msg.textContent = 'The worm is dead.';</script>", False),
        "tier (a) in a ternary's displayed branch": ("<script>el.textContent = lives ? 'alive' : 'dead';</script>", False),
        "tier (a) in innerHTML text": ("<script>box.innerHTML = '<span class=\"x\">Nobody drowned</span>';</script>", False),
        "tier (a) in a template literal": ("<script>t.innerHTML = `${n} of them died`;</script>", False),
        "tier (a) after a \\n escape": ("<script>var s = 'Line one\\nDead end';</script>", False),
        "tier (a) in a .js bank string": ("window.ROOM = {flavour: 'A dead plant.'};", True),
        "tier (a) in an alt attribute": ("<img alt=\"a dead tree\" src=\"x.webp\">", False),
        "tier (a) in an onclick string": ("<button onclick=\"say('it is dead')\">Go</button>", False),
    }
    quiet = {
        "comments, CSS and 'die'": ("<style>.dead{}</style><!-- murder --><script>/* drowning */\n// killed\n</script><p>Roll a fair die.</p>", False),
        "tier (b) in a neutral context (tier c)": ("<p>A test for a disease is given to 1000 patients in a hospital.</p>", False),
        "allowlisted terms": ("<h1>Prisoner's Dilemma</h1><p>Base rate neglect.</p><a href='/games/tax-theft/'>Tax Theft</a>", False),
        "allowlisted idioms": ("<p>Half dead. Three quarters dead. One kills the claim. What has the doctor neglected?</p>", False),
        "tier (a) as a JS identifier": ("<script>let dead = 0; dead++; worm.dead = true; function kill(){}</script>", False),
        "tier (a) as a CSS class name": ("<script>d.className = 'life ' + (i < n ? 'alive' : 'dead');\n"
                                         "el.classList.toggle('dead', !t.alive);</script><div class=\"dead\">ok</div>", False),
        "tier (a) as an id or selector": ("<script>document.getElementById('dead').id = 'killed';"
                                          "document.querySelector('.dead');</script>", False),
        "tier (a) as an object key": ("<script>var s = {'dead': 1, \"killed\": 2};</script>", False),
        "tier (a) as a .js identifier": ("function paintDead(dead) { return dead.killed; }", True),
    }
    for name, (text, js) in loud.items():
        if not hits_in(text, js):
            missed.append("%s must be a hit" % name)
    for name, (text, js) in quiet.items():
        if hits_in(text, js):
            missed.append("%s must not be a hit (got %s)" % (name, hits_in(text, js)))
    return missed, len(loud) + len(quiet)


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
