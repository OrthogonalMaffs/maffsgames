"""Shared helpers for checker tier 4, layer A: bank extraction and static lint.

Used by both `extract-banks.py` (reads live bank globals from the page) and
`check-banks.py` (lints the extracted JSON, plus a source-level AST pass for
the two checks — B8, B9 — that a live-read snapshot cannot see, because a
duplicate object key is silently resolved by the time JS has evaluated it, and
an index patch's damage is already baked into the value you would read back).

Node classification is deliberately generic across all 94 games, per the
CLASS CHECK in the tier 4 contract: one extractor, one lint pass, no per-game
special-casing. What varies per game is answered by walking the live JSON
shape (an object is "keyed by level/topic" or "a flat list" — either way the
walk finds every array of question-like dicts wherever it sits), not by a
lookup table of game names.
"""
import functools
import hashlib
import json
import math
import os
import re
import socket
import subprocess
import sys
import time
import urllib.request

# esprima is imported inside parse_game_source(), not here: the roster and
# stub-server helpers below are also used by check-site.py, which has never
# needed a JavaScript parser, and an import here would make every checker
# depend on one.

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAMES_DIR = os.path.join(ROOT, "games")
BANKS_DIR = os.path.join(ROOT, "data", "banks")
ROSTER_PATH = os.path.join(ROOT, ".claude", "rules", "game-roster.md")
ROSTER_LEVELS_PATH = os.path.join(ROOT, "scripts", "roster-levels.json")


# ---------------------------------------------------------------------------
# The roster's level vocabulary -- ONE table, ONE parser
# ---------------------------------------------------------------------------
# .claude/rules/game-roster.md names each game's levels with display labels
# ("L4", "A-Level Year 2"). The keys the games use ("level4", "alevel2") cannot
# be derived from those labels, so the mapping is stated once, in
# scripts/roster-levels.json, which the JavaScript coverage check reads too.
# check-site.py, extract-banks.py and check-leaderboard-coverage.js each used to
# keep their own copy; extract-banks.py's had no 'l3', so log-laws' Level 3 bank
# was never extracted as a level of its own.

def roster_level_keys():
    """{lower-cased roster label: level key}, from scripts/roster-levels.json."""
    with open(ROSTER_LEVELS_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)["labels"]


def roster_levels():
    """({slug: [level key, ...]}, [slug, ...] in roster order), from game-roster.md.

    A label the table does not list raises ValueError. It is never dropped: a
    dropped label is a level that no checker loads.
    """
    table = roster_level_keys()
    out, order = {}, []
    with open(ROSTER_PATH, "r", encoding="utf-8") as fh:
        for line in fh:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 4 or not cells[0].isdigit():
                continue
            m = re.match(r"^`([a-z0-9-]+)`$", cells[2])
            if not m:
                continue
            slug = m.group(1)
            levels = []
            for part in cells[3].split(","):
                label = part.strip().lower()
                if label not in table:
                    raise ValueError(
                        "%s: roster level %r is not in scripts/roster-levels.json"
                        % (slug, part.strip()))
                if table[label] not in levels:
                    levels.append(table[label])
            out[slug] = levels
            order.append(slug)
    return out, order


# ---------------------------------------------------------------------------
# Starting the stub server -- and knowing whether it started
# ---------------------------------------------------------------------------
# Scripts that render a page used to start scripts/serve-stubbed.py with Popen,
# a fixed port and a fixed sleep. When the port is unusable that server exits at
# once with a message nobody reads, and the script carries on against a dead port.
# extract-banks.py then reported all 96 games as "true generators", which is a
# classification, not an error, and on 30 Sep 2026 two CI steps clashed on 8799.
# Every caller now starts it here, on a free port chosen per run (port=0), so
# a server that cannot start is an error and no two steps can share a port.

class StubServerError(RuntimeError):
    """The stub server could not be started, or never answered."""


def free_port():
    """A port the OS says is free right now (bind to 0, read it back, release it)."""
    s = socket.socket()
    try:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]
    finally:
        s.close()


def start_stub_server(port=0, timeout=15.0, attempts=3):
    """Start serve-stubbed.py; return (Popen, base_url) once it answers.

    port=0 (the default, and what every CI caller uses) picks a free port for this
    run. The port is released between choosing it and the server binding it, so
    another process could take it in that gap; a start that fails that way is
    retried on a fresh port, up to `attempts` times, before the error is raised.
    A nonzero port is tried once, exactly as given.
    """
    if port:
        return _start_stub_server_on(port, timeout)
    last = None
    for _ in range(attempts):
        try:
            return _start_stub_server_on(free_port(), timeout)
        except StubServerError as exc:
            last = exc
    raise last


def _start_stub_server_on(port, timeout):
    """Start serve-stubbed.py on `port`; return (Popen, base_url) once it answers.

    Raises StubServerError, naming the cause, if the port is not free, if the
    server exits before answering, or if it does not answer within `timeout`.
    The port is probed the way serve-stubbed.py itself probes it (a plain bind,
    so a port still in TIME_WAIT counts as busy) before anything is launched, so
    a listener already on that port can never be mistaken for ours.
    """
    probe = socket.socket()
    try:
        probe.bind(("127.0.0.1", port))
    except OSError as exc:
        raise StubServerError(
            "port %d on 127.0.0.1 is not free (%s). Another server is on it, or it is "
            "still in TIME_WAIT from a run that just ended; wait a minute or pass a "
            "different port." % (port, exc))
    finally:
        probe.close()

    proc = subprocess.Popen(
        [sys.executable, os.path.join(ROOT, "scripts", "serve-stubbed.py"), str(port)],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=ROOT)
    base = "http://127.0.0.1:%d" % port
    deadline = time.time() + timeout
    while time.time() < deadline:
        if proc.poll() is not None:
            said = (proc.stdout.read() or "").strip()
            raise StubServerError(
                "serve-stubbed.py exited with code %s before it answered on port %d%s"
                % (proc.returncode, port, (": " + said) if said else ""))
        try:
            urllib.request.urlopen(base + "/schools/assets/analytics.js", timeout=2).read()
        except OSError:
            time.sleep(0.1)
            continue
        if proc.poll() is None:
            return proc, base
    proc.terminate()
    raise StubServerError("serve-stubbed.py did not answer on port %d within %gs"
                          % (port, timeout))


# The shared Next control (schools/assets/next-control.js) holds every wrong answer for a
# 3s floor before Next can be pressed. A content verifier checks what is on screen, not the
# floor, so waiting it out on every wrong answer only costs CI time (123 waits, ~6 minutes,
# in the Free Daily Pizza verifier alone). This init script sets MaffsNext.FLOOR_MS to 0 as
# the helper defines MaffsNext, before any game script runs. Content verifiers only:
# check-site.py (tier 3) and test-next-control.py keep the real floor on purpose.
NO_NEXT_FLOOR_INIT = """(() => {
  let api;
  Object.defineProperty(window, 'MaffsNext', {
    configurable: true,
    get() { return api; },
    set(v) { if (v && typeof v === 'object') v.FLOOR_MS = 0; api = v; },
  });
})();"""


async def no_next_floor(context):
    """Opt a Playwright browser context out of the Next control's 3s floor (see above)."""
    await context.add_init_script(NO_NEXT_FLOOR_INIT)

# A dict is "question-like" if it carries an answer key at its own top level.
# correct_override appears without `correct` in normal-navigator:222/:241
# (canon, todo 1.12), so either key alone must qualify. `answer` and `ans`
# are separate authoring vocabularies used by whole other games (given-that's
# phase1/phase2, estimation-engine, linear-equation-solver's per-step `ops[]`
# and final `ans`) -- found by reading real banks while building this checker,
# not assumed in advance. This is a vocabulary list, not a per-game lookup:
# any game using one of these four spellings is covered, whichever game it is.
ANSWER_KEYS = ("correct", "correct_override", "answer", "ans", "c")

# Where a question's student-facing prose usually lives. Order is only used
# for picking ONE representative string for duplicate-question comparisons
# (B3); every string value in the dict is still scanned for B6/B7.
TEXT_KEYS = ("q", "ask", "ctx", "prompt", "text", "phrase", "question",
             "scenario", "desc", "context", "p")

# Fields whose value is the option pool a student actually sees, distinct
# from the correct answer itself. `opts`/`options` is a pre-built full list
# (correct already included, e.g. normal-navigator, given-that's phaseN);
# the rest are distractor-only lists that get combined with `correct` the
# way MaffsOptions.build() does.
FULL_OPTION_KEYS = ("opts", "options")
DISTRACTOR_KEYS = ("d", "distractors", "wrong")

# Minimum size for the loose, no-recognised-answer-field fallback (see
# is_question_dict's `id_like_ok`) -- word-problem-decoder and its two
# siblings mark correctness by matching a `topic` string against a fixed
# button set elsewhere in the file, not by any per-question answer key. A
# small unrelated array of config objects (a handful of theme rows, a hole
# list) can accidentally look "id + prose"-shaped; requiring real bulk before
# trusting that alone is what keeps this from over-triggering.
LOOSE_BANK_MIN_SIZE = 8


def _own_answer_signal(d):
    return isinstance(d, dict) and any(k in d for k in ANSWER_KEYS)


# Precedence order, NOT membership order: formula-unlocked's own runtime
# reads `currentQ.correct_override || currentQ.correct` (index.html:447,
# :474) -- when both are present the override is what a student is actually
# marked against, and it is exactly where the known duplicate lives
# (formula-unlocked:298's correct_override repeats its own third distractor
# verbatim). ANSWER_KEYS itself stays declaration-order-free (it's only ever
# used for "does this carry an answer key", where order is irrelevant); this
# is the one place "which value actually wins" matters.
_CORRECT_PRECEDENCE = ("correct_override", "correct", "answer", "ans", "c")


def resolve_correct(unit):
    for ak in _CORRECT_PRECEDENCE:
        if ak in unit:
            return unit[ak]
    return None


def _own_options_carry_correct(d):
    """spot-the-muppet/terrible-advice/wrong-on-the-internet shape: the
    question itself has no answer field; each entry in its options list
    carries its own boolean `correct`.
    """
    if not isinstance(d, dict):
        return False
    for k in FULL_OPTION_KEYS:
        v = d.get(k)
        if (isinstance(v, list) and v and all(isinstance(o, dict) for o in v)
                and any("correct" in o for o in v)):
            return True
    return False


_OPTION_LETTER_RE = re.compile(r"^option([A-Za-z])$")


def _lettered_option_pointer(d):
    """expected-damage's shape: 2+ sibling `optionA`/`optionB`/... dicts, plus
    some other field whose string value names which one is correct (e.g.
    `higherEVOption: 'B'`). Returns (letters, pointer_key) or None.
    """
    if not isinstance(d, dict):
        return None
    letters = {}
    for k, v in d.items():
        m = _OPTION_LETTER_RE.match(k)
        if m and isinstance(v, dict):
            letters[m.group(1)] = k
    if len(letters) < 2:
        return None
    for k, v in d.items():
        if isinstance(v, str) and v in letters:
            return letters, k
    return None


def is_question_dict(v, _depth=1):
    """A dict is question-like if IT, or a direct child dict/array-of-dicts
    one level down, carries a recognised answer signal.

    The one level of nesting is what given-that's phase1/phase2 and
    linear-equation-solver's per-step `ops[]` + final `ans` need -- the outer
    dict (id, context, data...) has no answer field of its own, but the
    sub-object that actually gets marked does. Not recursing further keeps
    this from wandering into unrelated nested config.
    """
    if not isinstance(v, dict):
        return False
    if _own_answer_signal(v) or _own_options_carry_correct(v) or _lettered_option_pointer(v):
        return True
    if _depth <= 0:
        return False
    for val in v.values():
        if isinstance(val, dict) and is_question_dict(val, _depth - 1):
            return True
        if (isinstance(val, list) and val and all(isinstance(x, dict) for x in val)
                and any(is_question_dict(x, _depth - 1) for x in val)):
            return True
    return False


def _id_like_bulk_content(d):
    """The loose fallback: no recognised answer field anywhere, but this
    still looks like one entry in a real content bank (an id plus prose),
    not incidental config. Callers only trust this in bulk (see
    LOOSE_BANK_MIN_SIZE) -- one dict alone proves nothing.
    """
    if not isinstance(d, dict) or len(d) < 3:
        return False
    has_id = isinstance(d.get("id"), (str, int))
    has_text = any(k in d and isinstance(d[k], str) and d[k].strip() for k in TEXT_KEYS)
    return has_id and has_text


def find_question_groups(value, path=()):
    """Walk a live (JSON-decoded) value; return [(path_tuple, [question, ...],
    marking) ...] for every array whose elements are majority question-like
    (recognised answer signal), or -- failing that, and only in bulk -- majority
    id+prose "content bank" dicts with no answer field this checker knows how
    to read (word-problem-decoder's family: correctness is a string match
    against a `topic`, not a stored answer key).

    Recurses through dicts (level/topic keying) and lists (a list of lists is
    not a shape any bank uses, so a plain list is only ever a leaf here).
    """
    groups = []
    if isinstance(value, list):
        if not value:
            return groups
        qlike = sum(1 for x in value if is_question_dict(x))
        if qlike >= max(3, 0.5 * len(value)):
            groups.append((path, value, "recognised"))
            return groups
        if len(value) >= LOOSE_BANK_MIN_SIZE:
            idlike = sum(1 for x in value if _id_like_bulk_content(x))
            if idlike >= 0.8 * len(value):
                groups.append((path, value, "unrecognised"))
                return groups
            # Neither a recognised answer key nor an id+prose shape, but still
            # a substantial, consistently-shaped array of dicts -- a real
            # content bank (factor-race's number pairs, prime-or-composite's
            # {n, hint}) whose correctness is computed at runtime, not stored.
            # B1/B2/B5 need an answer key and will correctly find nothing to
            # check here; B3/B4/B6/B7/B8/B9/B10 do not, and still should.
            if all(isinstance(x, dict) for x in value):
                groups.append((path, value, "ungraded"))
        return groups
    if isinstance(value, dict):
        for k, v in value.items():
            groups.extend(find_question_groups(v, path + (str(k),)))
    return groups


def question_text(q):
    """Best-effort single string identifying a question, for B3's compare."""
    for k in TEXT_KEYS:
        if k in q and isinstance(q[k], str) and q[k].strip():
            return q[k]
    return None


def sub_answer_units(q):
    """Every gradeable "unit" inside one question dict, as (label, dict)
    pairs -- the dict itself if it carries an answer signal at its own top
    level, plus one entry per direct child (dict, or each element of a
    direct child array) that does. Mirrors is_question_dict's one level of
    nesting, so B1/B2 check exactly what is_question_dict decided counts.

    A flat schema-A question yields exactly [("", q)]. given-that yields
    [("phase1", q["phase1"]), ("phase2", q["phase2"])] and nothing for the
    outer dict itself (it has no answer signal of its own).
    """
    units = []
    if _own_answer_signal(q) and not q.get("display"):
        units.append(("", q))
    lettered = _lettered_option_pointer(q)
    if lettered:
        letters, pointer_key = lettered
        units.append(("lettered:" + pointer_key,
                       {"correct": q.get(pointer_key), "_valid_letters": sorted(letters)}))
    for k, val in q.items():
        if isinstance(val, dict) and _own_answer_signal(val) and not val.get("display"):
            units.append((k, val))
        elif isinstance(val, list) and val and all(isinstance(x, dict) for x in val):
            for i, x in enumerate(val):
                # factor-theorem's scaffoldSteps: a step marked `display:true`
                # is shown-not-answered by design (e.g. restating f(2) = ...
                # before the next blank), so its empty `answer` is correct,
                # not a missing one -- checked directly against the source
                # before adding this guard, not assumed.
                if _own_answer_signal(x) and not x.get("display"):
                    units.append(("%s[%d]" % (k, i), x))
    return units


def option_pool(unit):
    """[str(value), ...] the way MaffsOptions/dataset.val would compare them,
    for one answer unit (see sub_answer_units). Returns None if the unit
    carries no recognisable option field at all (so B2 has nothing to check,
    rather than a false empty-pool flag).
    """
    for k in FULL_OPTION_KEYS:
        if k in unit and isinstance(unit[k], list):
            return [str(v) for v in unit[k]]
    for k in DISTRACTOR_KEYS:
        if k in unit and isinstance(unit[k], list):
            correct = resolve_correct(unit)
            pool = [] if correct is None else [str(correct)]
            pool += [str(v) for v in unit[k]]
            return pool
    return None


def flagged_option_texts_and_correct_count(q):
    """For the spot-the-muppet/terrible-advice shape: ([text, ...], n_correct)
    -- the rendered label of every option, and how many carry `correct: true`
    -- or None if `q` isn't that shape.
    """
    opts = options_with_own_correct(q)
    if opts is None:
        return None
    texts = []
    for o in opts:
        t = None
        for k in TEXT_KEYS:
            if k in o and isinstance(o[k], str):
                t = o[k]
                break
        texts.append(t if t is not None else str(o))
    n_correct = sum(1 for o in opts if o.get("correct") is True)
    return texts, n_correct


def options_with_own_correct(q):
    """For the spot-the-muppet/terrible-advice shape: the options list whose
    entries each carry their own boolean `correct`, or None if this question
    isn't that shape.
    """
    for k in FULL_OPTION_KEYS:
        v = q.get(k)
        if (isinstance(v, list) and v and all(isinstance(o, dict) for o in v)
                and any("correct" in o for o in v)):
            return v
    return None


def all_strings(value):
    """Yield every string leaf in a (possibly nested) live value."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for v in value:
            yield from all_strings(v)
    elif isinstance(value, dict):
        for v in value.values():
            yield from all_strings(v)


# ---------------------------------------------------------------------------
# Content identity -- a finding names the question by what it says, not where it
# sits, so inserting or reordering questions cannot turn one known defect into
# "one new + one stale" (todo item 7). B11 uses it from the start; item 7 moves
# B1-B10 onto it.
#
# The hash covers the WHOLE question as extracted (Jon's ruling, 2 Oct 2026). A
# narrower hash of stem + ask + sorted options gave one id to 74 groups of
# different questions in 21 games: simultaneous-solver's "Find x" questions share
# their ask and options and differ only in `sys`, the equations, and many games
# keep their real parameters in fields like that, under no common name. The cost
# of hashing everything: editing any field (an explanation included) changes the
# id, so the ledger shows that question as one new + one stale entry. That is
# right, since the content did change.
# ---------------------------------------------------------------------------

def content_hash(q):
    """First 12 hex of the SHA-1 of q's canonical JSON. Key order does not matter."""
    canon = json.dumps(q, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha1(canon.encode("utf-8")).hexdigest()[:12]


def content_id(slug, q, ordinal):
    """slug::<hash>#<ordinal>. ordinal is 1 for the first question in the game with
    this exact content, 2 for the next byte-identical copy, and so on (B3 shows exact
    copies exist). Copies are interchangeable, so which gets which number does not
    matter. Use content_ids() to number a whole game."""
    return "%s::%s#%d" % (slug, content_hash(q), ordinal)


def content_ids(slug, questions):
    """content_id for each question in bank order, ordinals assigned along the way."""
    seen = {}
    out = []
    for q in questions:
        h = content_hash(q)
        seen[h] = seen.get(h, 0) + 1
        out.append(content_id(slug, q, seen[h]))
    return out


# ---------------------------------------------------------------------------
# Source-level AST access (esprima) -- for B8/B9 and for finding candidate
# top-level identifier names to read from the live page.
# ---------------------------------------------------------------------------

def extract_inline_scripts(html):
    """Every inline <script> body, concatenated in document order, padded
    with spaces (newlines kept) everywhere else so byte offsets - and line
    numbers - still match the original file. Mirrors check-site.py's own
    helper of the same name; kept local so this module has no import-by-path
    dependency on a hyphenated filename.
    """
    padded = [" " if ch != "\n" else "\n" for ch in html]
    for m in re.finditer(r"<script\b([^>]*)>(.*?)</script\s*>", html,
                         re.IGNORECASE | re.DOTALL):
        attrs = m.group(1)
        if re.search(r'\bsrc\s*=', attrs, re.IGNORECASE):
            continue
        t = re.search(r'\btype\s*=\s*["\']?([^"\'\s>]+)', attrs, re.IGNORECASE)
        if t and t.group(1).lower() not in ("text/javascript", "module",
                                            "application/javascript"):
            continue
        body = m.group(2)
        start = m.start(2)
        for k, ch in enumerate(body):
            padded[start + k] = ch
    return "".join(padded)


def _shim_for_parser(src):
    """Rewrite two ES2019+/ES2020 shapes esprima's ES2017 subset rejects,
    IN THE STRING HANDED TO THE PARSER ONLY -- never touches a real file.

    Structural analysis (top-level declarations, object-literal shape,
    index-patch assignments) doesn't care about either rewrite's semantics:

      - `catch {` (optional catch binding) -> `catch (e) {`. 7 games use it.
      - `a?.b` (optional chaining) -> `a.b`. 13 games use it. The lookahead
        excludes `?.5`-shaped ternaries (`cond ? .5 : x`) written with no
        space -- per the real grammar, `?.` followed by a digit can never be
        optional chaining, since `.5` alone can't start a property name.

    Changing either rewrite changes every B8 and B9 ledger id at once:
    check-banks.py hashes this rewritten text (the text the AST's ranges index
    into) to name those findings. Re-record the ledger in the same change.
    """
    src = re.sub(r"\bcatch\s*\{", "catch (e) {", src)
    src = re.sub(r"\?\.(?!\d)", ".", src)
    return src


def parse_game_source(html):
    """(tree, src) for a game's inline scripts, or (None, src) on a parse
    error. `src` is the UNSHIMMED text (so reported line numbers stay true
    to the real file); only the parser sees the shimmed copy.
    """
    src = extract_inline_scripts(html)
    import esprima  # lazy, see the note at the top of this module
    try:
        tree = esprima.parseScript(_shim_for_parser(src), options={"loc": True, "range": True})
        return tree, src
    except Exception:
        return None, src


def line_of(src, offset):
    return src.count("\n", 0, offset) + 1


def top_level_declarations(tree):
    """[(name, init_node, kind)] for every var/let/const at Program level.

    Deliberately does NOT recurse into function bodies or IIFEs: a name only
    counts as a candidate bank if it is the kind of binding page.evaluate can
    actually reach by identifier. A bank hidden inside a module-pattern IIFE
    with nothing exposed to the outer scope is exactly the shape the tier 4
    contract's STOP IF clause exists to catch, not to paper over.
    """
    out = []
    for node in tree.body:
        if node.type == "VariableDeclaration":
            for d in node.declarations:
                if d.id.type == "Identifier" and d.init is not None:
                    out.append((d.id.name, d.init, node.kind))
    return out


def literal_key(key_node):
    """Best-effort string for a Property's key node, or None if computed in
    a way that is not a plain literal (e.g. `[1+1]:`) -- those can't collide
    with a named key statically, so B8 has nothing useful to say about them.
    """
    if key_node.type == "Identifier":
        return key_node.name
    if key_node.type == "Literal":
        return str(key_node.value)
    return None


def walk(node, visit):
    """Minimal manual AST walk -- esprima's Python port ships no built-in
    traversal helper. Visits every node reachable from `node`.
    """
    if node is None:
        return
    visit(node)
    if isinstance(node, list):
        for item in node:
            walk(item, visit)
        return
    if not hasattr(node, "__dict__"):
        return
    for key, val in vars(node).items():
        if key in ("range", "loc", "type"):
            continue
        if isinstance(val, list):
            for item in val:
                if hasattr(item, "type"):
                    walk(item, visit)
        elif hasattr(val, "type"):
            walk(val, visit)


def enclosing_name(tree, node):
    """The name B8 files a finding under: the innermost named function whose
    body contains `node`, else the top-level variable whose declaration
    contains it, else '(top level)'. checker-allowlist.json's tier-2 entries
    use the same "innermost named function, or (top level)" convention; the
    variable step is for a bank literal (`const QUESTIONS = [...]`), which sits
    in no function. A function is named by its declaration, by the variable or
    property it is assigned to, or as a method. Renaming that function or
    variable renames the finding."""
    fn_types = ("FunctionExpression", "ArrowFunctionExpression")
    scopes = []

    def visit(n):
        t = getattr(n, "type", None)
        if t == "FunctionDeclaration" and n.id is not None:
            scopes.append((n.range, n.id.name))
        elif t == "VariableDeclarator" and getattr(n.init, "type", None) in fn_types \
                and n.id.type == "Identifier":
            scopes.append((n.init.range, n.id.name))
        elif t == "Property" and getattr(n.value, "type", None) in fn_types:
            k = literal_key(n.key)
            if k is not None:
                scopes.append((n.value.range, k))

    walk(tree, visit)
    lo, hi = node.range
    inside = [(r, name) for r, name in scopes if r[0] <= lo and hi <= r[1]]
    if inside:
        return min(inside, key=lambda s: s[0][1] - s[0][0])[1]
    for stmt in tree.body:
        if stmt.type == "VariableDeclaration":
            for d in stmt.declarations:
                if d.id.type == "Identifier" and d.range[0] <= lo and hi <= d.range[1]:
                    return d.id.name
    return "(top level)"


def find_duplicate_keys(tree):
    """[(object_node, [dup_key, ...])] for every ObjectExpression with a
    literal key repeated within that SAME object (B8). AST-based per the
    contract, not regex, because a regex over source text cannot tell a
    duplicate key inside one object literal from two different objects each
    using the same key once -- which is most of the vocabulary (every
    `correct:` in the file, for instance).
    """
    hits = []

    def visit(node):
        if getattr(node, "type", None) == "ObjectExpression":
            seen = {}
            for prop in node.properties:
                if getattr(prop, "type", None) != "Property":
                    continue
                k = literal_key(prop.key)
                if k is None:
                    continue
                seen.setdefault(k, 0)
                seen[k] += 1
            dups = [k for k, c in seen.items() if c > 1]
            if dups:
                hits.append((node, dups))

    walk(tree, visit)
    return hits


def find_index_patches(tree):
    """[(ident_name, assignment_node)] for every `IDENT[literal] = ...` (or
    `IDENT[literal][literal] = ...`) assignment anywhere in the source (B9).

    Deliberately does not require the assignment to come "after" any
    particular declaration by position -- normal-navigator's patches sit
    inside the same script, textually after the QUESTIONS literal, but the
    shape being flagged (a hand-written numeric index patching a bank some
    other name owns) is the same wherever it appears, and the fix -- name the
    question, don't count to it -- is the same either way. Callers wanting
    only patches after a given identifier's declaration can filter on the
    node's `.range` against the declaration's `.range`.
    """
    hits = []

    def base_identifier(member_expr):
        node = member_expr
        while getattr(node, "type", None) == "MemberExpression":
            if getattr(node, "computed", False) and \
               getattr(node.property, "type", None) != "Literal":
                return None  # a[i] with a variable index isn't a hand patch
            node = node.object
        if getattr(node, "type", None) == "Identifier":
            return node.name
        return None

    def visit(node):
        if getattr(node, "type", None) != "AssignmentExpression":
            return
        if getattr(node.left, "type", None) != "MemberExpression":
            return
        if not getattr(node.left, "computed", False):
            return
        name = base_identifier(node.left)
        if name:
            hits.append((name, node))

    walk(tree, visit)
    return hits


# B7's syntactic half: a run this long with no space is never a real English
# word (checked directly: no dictionary word gets near this), and it is
# exactly the shape KaTeX produces when it swallows the spaces out of a
# whole sentence passed to it as one "expression" (component-crusher's
# "Whatisthereversetranslation?"). 26 is ">25 letters" per the contract.
NO_SPACE_RUN = re.compile(r"[A-Za-z]{26,}")


# SUPERSEDED 2 Oct 2026 (to-do §1.31): B7 no longer uses katex_prose_hazard,
# katex_field_names or collect_field_strings below. Its KaTeX half is the
# "render sites found by behaviour" section further down, tested with
# katex_lost_word_spaces. These three stay because scripts/audit-katex/, the
# KaTeX wrapper audit kept as the reference prototype, still imports them.
#
# B7's KaTeX half, redefined 27 Sep: math mode dropping the space out of
# '-1 + j', '(A + B) \cdot (C + D)' or '25^{1/2} = 5' is CORRECT rendering --
# LaTeX spacing is insignificant by design, and single-letter/short tokens
# either side of an operator are exactly what real maths looks like. The
# actual hazard is prose smuggled through the same call: two or more whole
# words running together with no space between them, the "Findthemagnitude"
# shape. \text{...}/\mathrm{...}/\operatorname{...} already switch to a mode
# that keeps spacing (that's what they're for), so their contents are not
# part of the maths being checked; every other backslash command (\cdot,
# \Rightarrow, \binom, \sqrt, ...) is a control token, not a word, and is
# stripped the same way. What's left is tested for a run of 2+ real words --
# a single stray letter (a variable name) never counts on its own.
_KATEX_TEXT_MODE_WRAP = re.compile(r"\\(?:text|mathrm|operatorname)\{[^{}]*\}")
_KATEX_COMMAND = re.compile(r"\\[A-Za-z]+")
_PROSE_RUN = re.compile(r"[A-Za-z]{2,}(?:\s+[A-Za-z]{2,})+")


def katex_prose_hazard(s):
    """True if `s`, once every text-mode wrap and bare LaTeX command name is
    stripped out, still contains two or more adjacent whole words -- prose
    that a whole-string K()/renderToString() call in math mode will run
    together with no space, not maths whose spacing is cosmetic anyway."""
    stripped = _KATEX_TEXT_MODE_WRAP.sub("", s)
    stripped = _KATEX_COMMAND.sub("", stripped)
    return bool(_PROSE_RUN.search(stripped))


# MaffsText's own convention (schools/assets/mathtext.js): mixed prose+maths
# strings wrap only the maths in \( ... \), never nested, never using $...$
# (money games use a literal $ in prose). `\(` never occurs by accident in
# ordinary bank text, so scanning every string in a bank for it -- not just
# fields a game's source happens to pass to K() -- is precise, the same way
# rendering only a known-scoped field was precise for the K()-call check
# above; here the marker itself is the scope.
def mathtext_has_delimiters(s):
    return isinstance(s, str) and "\\(" in s


def mathtext_delimiters_balanced(s):
    """False for a stray \\( with no matching \\), a stray \\) with nothing
    open, or (equivalently, since counts can't differ if this holds) nesting
    -- MaffsText.html's split-on-\\( \\) has no concept of a nested segment,
    so a nested pair would silently truncate at the first \\) instead of the
    author's intended one."""
    depth = 0
    i = 0
    while i < len(s):
        if s[i:i + 2] == "\\(":
            depth += 1
            i += 2
        elif s[i:i + 2] == "\\)":
            depth -= 1
            if depth < 0:
                return False
            i += 2
        else:
            i += 1
    return depth == 0


_MATHTEXT_SEGMENT = re.compile(r"\\\((.*?)\\\)", re.DOTALL)


def mathtext_segments(s):
    """Every \\( ... \\) segment's inner LaTeX, in order -- what actually
    gets handed to katex.renderToString() by MaffsText.html. Only meaningful
    when mathtext_delimiters_balanced(s) is true; call that first."""
    return _MATHTEXT_SEGMENT.findall(s)


# Shared between extract-banks.py (live extraction) and check-banks.py's
# --selftest-live (fixture proof that this JS actually distinguishes a valid
# segment from a broken one) -- one definition, not two copies to keep in
# sync. throwOnError:true here is deliberately stricter than MaffsText.html's
# own throwOnError:false, which exists so a bad segment degrades to KaTeX's
# red error styling in production rather than breaking the page; this check
# is what catches the authoring mistake before it ships.
MATHTEXT_THROW_JS = """(strings) => {
    if (typeof katex === 'undefined') return null;
    return strings.map(s => {
        try { katex.renderToString(s, {throwOnError: true}); return null; }
        catch (e) { return String(e && e.message || e); }
    });
}"""


_K_CALL_RE = re.compile(
    r"\bK\(\s*[A-Za-z_$][\w$]*\.([A-Za-z_$][\w$]*)\s*[,)]"
    r"|katex\.renderToString\(\s*[A-Za-z_$][\w$]*\.([A-Za-z_$][\w$]*)\s*[,)]")


def katex_field_names(src):
    """Field names this game's OWN code passes to KaTeX -- `K(sq.prompt)`
    yields {"prompt"}. Found once by grepping every game for a dotted K()/
    katex.renderToString() call: 12 real call sites across 8 games, almost
    all of them a genuinely mathematical field (`q.exp`, `q.expr`,
    `q.zFormula`, `q.givenLatex`, ...) except component-crusher's `prompt`
    and growth-and-decay's `hint` -- both names that read as prose, and
    component-crusher's is the confirmed defect (todo.md 1.10).

    This is what makes the render check precise instead of either a flood
    (rendering every string in the bank blindly hit 3772 "hits", mostly
    hint/explanation text the game never sends to KaTeX at all) or flaky
    (sampling live play only catches whichever question a few random clicks
    happen to land on). Testing exactly the field the game's own source
    names, across every question, is deterministic and complete for that
    field, and needs no per-game list -- the regex reads it off the source.
    """
    names = set()
    for m in _K_CALL_RE.finditer(src):
        names.add(m.group(1) or m.group(2))
    return names


def collect_field_strings(questions, field_names, _depth=3):
    """Every string value found under any of `field_names`, anywhere in
    `questions` (nested up to `_depth` levels -- component-crusher's
    `sq.prompt` sits inside `q.sqs[]`, one level below the question dict).
    """
    out = set()

    def walk(v, depth):
        if isinstance(v, dict):
            for k, val in v.items():
                if k in field_names and isinstance(val, str):
                    out.add(val)
            if depth > 0:
                for val in v.values():
                    walk(val, depth - 1)
        elif isinstance(v, list) and depth > 0:
            for item in v:
                walk(item, depth - 1)

    for q in questions:
        walk(q, _depth)
    return out


def normalise_for_dup_check(s):
    return re.sub(r"\s+", " ", s.strip().lower())


# ---------------------------------------------------------------------------
# Module-pattern IIFE fallback
# ---------------------------------------------------------------------------
#
# One roster game (given-that) wraps its entire script in
# `(function(){ 'use strict'; const QUESTIONS = {...}; ... })();` -- a bank
# declared this way is never on the page's global lexical scope, so
# page.evaluate('QUESTIONS') throws ReferenceError no matter how the game
# runs. That absence is real, not a bug in the reader: the fix is to read
# the same declaration statically, from the AST already in hand, rather than
# from the live page.

def _is_top_level_iife_call(node):
    if getattr(node, "type", None) != "ExpressionStatement":
        return None
    expr = node.expression
    if getattr(expr, "type", None) != "CallExpression" or expr.arguments:
        return None
    callee = expr.callee
    if getattr(callee, "type", None) not in ("FunctionExpression", "ArrowFunctionExpression"):
        return None
    if callee.params:
        return None
    return callee


def iife_scoped_declarations(tree):
    """[(name, init_node, kind)] one level inside every top-level, no-arg,
    no-param self-invoking function -- the only extra scope worth trusting a
    name from, because it runs synchronously at load, same as a real
    top-level statement would.
    """
    out = []
    for node in tree.body:
        fn = _is_top_level_iife_call(node)
        if fn is None:
            continue
        body = getattr(fn.body, "body", None)
        if body is None:
            continue
        for inner in body:
            if inner.type == "VariableDeclaration":
                for d in inner.declarations:
                    if d.id.type == "Identifier" and d.init is not None:
                        out.append((d.id.name, d.init, inner.kind))
    return out


class _NotLiteral(Exception):
    pass


def literal_to_json(node):
    """Best-effort static evaluation of an AST node into a plain Python
    value, for the IIFE fallback -- covers everything real banks are
    actually written with (array/object literals, strings, numbers,
    booleans, null, unary minus on a numeric literal, and template literals
    with no interpolation). Raises _NotLiteral on anything else (a computed
    value, a reference to another identifier, a function) rather than
    guessing.
    """
    t = node.type
    if t == "Literal":
        return node.value
    if t == "ArrayExpression":
        out = []
        for el in node.elements:
            if el is None:
                out.append(None)
            else:
                out.append(literal_to_json(el))
        return out
    if t == "ObjectExpression":
        out = {}
        for prop in node.properties:
            if prop.type != "Property":
                raise _NotLiteral("spread/method in object literal")
            k = literal_key(prop.key)
            if k is None:
                raise _NotLiteral("computed key")
            out[k] = literal_to_json(prop.value)
        return out
    if t == "UnaryExpression" and node.operator in ("-", "+") and node.argument.type == "Literal":
        v = node.argument.value
        return -v if node.operator == "-" else v
    if t == "TemplateLiteral" and not node.expressions:
        return "".join(q.value.cooked or "" for q in node.quasis)
    if t == "Identifier" and node.name in ("undefined",):
        return None
    raise _NotLiteral("unsupported node type: %s" % t)


def static_bank_value(name, init_node, tree):
    """The IIFE fallback's full answer for one candidate: the literal value,
    with any `NAME[literal] = ...` index patches (find_index_patches) that
    appear textually after the declaration applied in source order -- so a
    static read reflects the same final state a live read would have shown,
    the whole point being that B9 flags the patch shape as a smell while
    extraction still reports the bank a student actually gets. Returns None
    if the literal (or any patch's RHS) uses anything literal_to_json can't
    statically evaluate.
    """
    try:
        value = literal_to_json(init_node)
    except _NotLiteral:
        return None
    decl_end = init_node.range[1]
    for ident, assign in find_index_patches(tree):
        if ident != name or assign.range[0] < decl_end:
            continue
        try:
            _apply_patch(value, assign.left, literal_to_json(assign.right))
        except _NotLiteral:
            return None
    return value


def locate_array_node(tree, name, path):
    """The ArrayExpression AST node for `name` (top-level, or one level
    inside a top-level IIFE) followed by `path`'s object keys, or None.

    Used only to recover source LINE NUMBERS for a live-read question
    (check-banks.py) -- this project references every defect by file:line
    (CLAUDE.md, todo.md: "formula-unlocked:295"), and a live JSON snapshot
    has no such thing. Positional: element i of the live array is assumed to
    be element i of this node's `.elements` -- true unless a QUESTIONS[n]=
    patch inserted or removed an element outright, which no known game does
    (it overwrites in place; see find_index_patches).
    """
    candidates = [init for n, init, k in top_level_declarations(tree) if n == name]
    candidates += [init for n, init in
                   [(n, i) for n, i, k in iife_scoped_declarations(tree)] if n == name]
    for init in candidates:
        node = init
        ok = True
        for seg in path:
            if getattr(node, "type", None) != "ObjectExpression":
                ok = False
                break
            match = None
            for prop in node.properties:
                if getattr(prop, "type", None) == "Property" and literal_key(prop.key) == seg:
                    match = prop.value
                    break
            if match is None:
                ok = False
                break
            node = match
        if ok and getattr(node, "type", None) == "ArrayExpression":
            return node
    return None


def line_numbers_for_group(tree, name, path, count):
    """[line_or_None, ...] of length `count`, one per element of the group's
    live array, via locate_array_node. All None if the array can't be found
    or its length doesn't match (patch inserted/removed rather than
    overwrote -- see locate_array_node's docstring).
    """
    node = locate_array_node(tree, name, path)
    if node is None or len(node.elements) != count:
        return [None] * count
    return [el.loc.start.line if el is not None else None for el in node.elements]


def _apply_patch(value, member_expr, rhs):
    """Apply `value[...][idx] = rhs` in place, following the same chain of
    computed MemberExpressions find_index_patches already validated.
    """
    chain = []
    node = member_expr
    while getattr(node, "type", None) == "MemberExpression":
        chain.append(node.property.value)
        node = node.object
    chain.reverse()
    target = value
    for key in chain[:-1]:
        target = target[key]
    target[chain[-1]] = rhs


# ---------------------------------------------------------------------------
# Value equality of option strings -- B11 (check-banks.py) and the one-off
# scan (scan-value-equivalent-options.py) share this one copy. Moved here from
# the scan on 2 Oct 2026. SymPy is imported on first use, not at module load:
# check-site.py and extract-banks.py also import this module and never need it.

_SYMPY = {}


def _sympy_env():
    if not _SYMPY:
        import sympy as sp
        from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                                implicit_multiplication_application,
                                                convert_xor)
        syms = {c: sp.Symbol(c) for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"}
        syms.update({"pi": sp.pi, "e": sp.E, "sqrt": sp.sqrt, "sin": sp.sin, "cos": sp.cos,
                     "tan": sp.tan, "ln": sp.log, "log": sp.log, "exp": sp.exp, "i": sp.I})
        _SYMPY.update(sp=sp, parse_expr=parse_expr, syms=syms,
                      trans=standard_transformations + (implicit_multiplication_application,
                                                        convert_xor))
    return _SYMPY


VULGAR = {"½": "(1/2)", "⅓": "(1/3)", "⅔": "(2/3)", "¼": "(1/4)", "¾": "(3/4)", "⅕": "(1/5)",
          "⅖": "(2/5)", "⅗": "(3/5)", "⅘": "(4/5)", "⅙": "(1/6)", "⅚": "(5/6)", "⅛": "(1/8)",
          "⅜": "(3/8)", "⅝": "(5/8)", "⅞": "(7/8)"}
_SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺⁽⁾ⁿˣʸ", "0123456789-+()nxy")
_SUPCHARS = "⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺⁽⁾ⁿˣʸ"
_ALLOWED_WORDS = {"sqrt", "pi", "sin", "cos", "tan", "ln", "log", "exp"}


def strip_latex(s):
    s = s.replace("$", "")
    s = re.sub(r"\\[()\[\]]", "", s)
    s = re.sub(r"\\(left|right|displaystyle|,|;|!|quad|qquad)", " ", s)
    # A mixed number: an integer written straight before \frac{p}{q} or \dfrac{p}{q}
    # (p, q integers) is n + p/q, so x^{4\frac{1}{2}} is x^4.5, not x^2 (index-laws [21],
    # B11, 2 Oct 2026). Done before the general \frac rewrite, and so before the
    # implicit-multiplication rewrite, which would read it as n * p/q. A letter before
    # the fraction (2x\frac{1}{2}) is a genuine product and is left alone.
    s = re.sub(r"(?<![\d.])(\d+)\\d?frac\{(\d+)\}\{(\d+)\}", r"(\1+(\2)/(\3))", s)
    for _ in range(3):
        s = re.sub(r"\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", s)
        s = re.sub(r"\\sqrt\[([^\]]*)\]\{([^{}]*)\}", r"((\2)**(1/(\1)))", s)
        s = re.sub(r"\\sqrt\{([^{}]*)\}", r"sqrt(\1)", s)
        s = re.sub(r"\^\{([^{}]*)\}", r"**(\1)", s)
    s = s.replace("\\times", "*").replace("\\cdot", "*").replace("\\div", "/").replace("\\pi", "pi")
    s = s.replace("\\circ", "").replace("^\\circ", "")
    s = re.sub(r"\\text\{[^{}]*\}", "", s)
    return s


def to_expr_text(raw):
    s = strip_latex(raw.strip())
    s = s.replace("−", "-").replace("–", "-").replace("×", "*").replace("÷", "/").replace("·", "*")
    s = s.replace("⁄", "/").replace("π", "pi").replace("°", "")
    for k, v in VULGAR.items():
        s = s.replace(k, v)
    s = re.sub("([%s]+)" % _SUPCHARS, lambda m: "**(" + m.group(1).translate(_SUP) + ")", s)
    s = re.sub(r"√\s*\(", "sqrt(", s)
    s = re.sub(r"√\s*([0-9.]+|[A-Za-z])", r"sqrt(\1)", s)
    s = re.sub(r"(\d+(?:\.\d+)?)\s*%", r"(\1/100)", s)
    s = re.sub(r"(?<=\d),(?=\d{3}\b)", "", s)          # thousands separators
    s = s.replace("^", "**")
    # Implicit multiplication after a number, made explicit here rather than left to
    # Python's tokenizer, which changed in 3.12: there "0x" reads as a broken hex
    # literal, so "1 + 0x + 0x^2" parsed on 3.11 and not on 3.12+ (re-run, 1 Oct 2026).
    # Scientific notation (2e5, 1.5E-3) is left alone.
    s = re.sub(r"(\d)\s*(?=[A-Za-z(])(?![eE][+-]?\d)", r"\1*", s)
    s = re.sub(r"(?<![A-Za-z])e\*\*\(([^()]*)\)", _phasor_exponent, s)
    return s.strip()


_LONE_J = r"(?<![A-Za-z])j(?![A-Za-z])"


def _phasor_exponent(m):
    """In the exponent of e, j is the imaginary unit (an engineering phasor), so
    5e^{j0.927} and 5e^{j0.644} differ in angle (complex-converter, B11, 2 Oct 2026).
    Before this, "j0.927" read as one name and both phasors came out as 5."""
    x = m.group(1)
    if not re.search(_LONE_J, x):
        return m.group(0)
    x = re.sub(_LONE_J + r"\s*(?=[\d.(]|pi)", "i*", x)
    return "e**(" + re.sub(_LONE_J, "i", x) + ")"


# An en-dash between two numbers is a class interval ("20–40"), not a subtraction:
# read as one, every interval of width 20 was "equal" to every other (core-maths-paper1
# [11], B11, 2 Oct 2026). Intervals compare by their endpoints.
_INTERVAL = re.compile(r"\s*(-?\d+(?:\.\d+)?)\s*–\s*(-?\d+(?:\.\d+)?)\s*")
# \text{...} carries meaning ("Nm clockwise" against "Nm anticlockwise", moments-master
# alevel[10]); stripping it made those two "equal". So an option is split into its
# \text{} parts and the rest: two options are equal only if their \text{} parts, in
# order, are the same strings (trimmed) AND the rest is equal in value. "\sqrt{50}\text{ cm}"
# still equals "5\sqrt{2}\text{ cm}"; a unit on one side only is unequal. (2 Oct 2026: a
# first version left every \text{} option unparsed, which hid 585 options from B11.)
_TEXT_PART = re.compile(r"\\text\{([^{}]*)\}")


def tokenizer_safe(t):
    """False if t holds a character Python cannot read as a name, an operator or a
    digit (e.g. '£'). Such text is unparsed on every Python: on 3.11 the tokenizer
    raised on it, on 3.12+ SymPy read '£0.33' as 0, which made every pair of money
    options "equal" (re-run, 1 Oct 2026)."""
    return all(ord(c) < 128 or c.isidentifier() for c in t)


def parse_value(raw):
    """-> (kind, value) or None. kinds: num, expr, tuple, ratio, eq, interval, and
    text: ((the \\text{} parts, trimmed), the parsed rest)."""
    if not isinstance(raw, str) or not raw.strip():
        return None
    parts = _TEXT_PART.findall(raw)
    if parts:
        rest = parse_value(_TEXT_PART.sub(" ", raw))
        if rest is None:
            return None
        return ("text", (tuple(p.strip() for p in parts), rest))
    m = _INTERVAL.fullmatch(raw)
    if m:
        from fractions import Fraction
        return ("interval", (Fraction(m.group(1)), Fraction(m.group(2))))
    t = to_expr_text(raw)
    if re.fullmatch(r"\d+(\s*:\s*\d+)+", t):
        parts = [int(x) for x in re.split(r"\s*:\s*", t)]
        g = functools.reduce(math.gcd, parts) or 1
        return ("ratio", tuple(p // g for p in parts))
    words = set(re.findall(r"[A-Za-z]{2,}", t)) - _ALLOWED_WORDS
    if words or not tokenizer_safe(t):
        return None
    env = _sympy_env()
    sp, parse_expr, syms, trans = env["sp"], env["parse_expr"], env["syms"], env["trans"]
    try:
        if t.count("=") == 1:
            l, r = t.split("=")
            e = (parse_expr(l, local_dict=syms, transformations=trans)
                 - parse_expr(r, local_dict=syms, transformations=trans))
            return ("eq", sp.expand(e))
        if "=" in t or "<" in t or ">" in t:
            return None
        v = parse_expr(t, local_dict=syms, transformations=trans)
        if isinstance(v, sp.Tuple) or isinstance(v, tuple):
            return ("tuple", tuple(sp.nsimplify(x) if x.is_number else x for x in v))
        if not isinstance(v, sp.Basic):
            return None
        return ("num" if v.is_number else "expr", v)
    except Exception:
        return None


VALUE_FIXTURES_EQUAL = [
    ("5√2", "√50"), ("\\(5\\sqrt{2}\\)", "\\sqrt{50}"), ("1/2", "0.5"), ("50%", "0.5"),
    ("12.5%", "1/8"), ("½", "0.5"), ("2:3", "4:6"), ("(x+2)(x+3)", "x²+5x+6"),
    ("y = ½x + 2", "2y = x + 4"), ("(3, 4)", "(3.0, 4)"), ("3×10^4", "30,000"), ("−3", "-3"),
    ("2^{-3}", "1/8"), ("\\frac{3}{6}", "\\frac{1}{2}"), ("10⁴", "10000"),
    ("4.14 \\times 10^{-15}", "41.4 \\times 10^{-16}"), ("0", "0.0"),
    # Re-run, 1 Oct 2026: a zero coefficient must not depend on the tokenizer.
    ("1 + 0x + 0x^2", "1"), ("2(x+1)", "2x+2"), ("2pi", "2\\pi"),
    # B11, 2 Oct 2026: a letter before \frac is a product, not a mixed number;
    # a mixed number is n + p/q.
    ("2x\\frac{1}{2}", "x"), ("4\\frac{1}{2}", "4.5"),
    # \text{} rule, 2 Oct 2026: the same unit, equal values (whitespace inside trimmed).
    ("\\sqrt{50}\\text{ cm}", "5\\sqrt{2}\\text{ cm}"), ("5\\text{cm}", "5\\text{ cm }"),
]
# Look-alikes that must NOT match. The percent and tiny-number cases are the two
# scanner bugs these fixtures caught on 28 Sep ("50%" had parsed as 0; an absolute
# tolerance made every number below 1e-12 equal).
VALUE_FIXTURES_UNEQUAL = [
    ("1.41", "√2"), ("√7", "7"), ("5 cm", "5 m"), ("2:3", "3:2"), ("(3, 4)", "(4, 3)"),
    ("x+2", "x+3"), ("y = 2x", "y = 3x"), ("0.33", "1/3"), ("25", "5"), ("5√2", "10"),
    ("10%", "20%"), ("50%", "5%"), ("4.14 \\times 10^{-15}", "4.14 \\times 10^{-53}"),
    ("4.14 \\times 10^{-15}", "4.14 \\times 10^{-14}"), ("0", "10^{-12}"),
    # Re-run, 1 Oct 2026: on Python 3.12+ every amount in pounds had parsed as 0.
    ("£0.33", "£0.67"), ("−£0.33", "£0.33"), ("£6,480.00", "£6,504.00"),
    # B11, 2 Oct 2026: the four scanner false-positive shapes (scan doc, section E).
    ("20–40", "40–60"), ("1 \\text{ Nm anticlockwise}", "1 \\text{ Nm clockwise}"),
    ("5e^{j0.927}", "5e^{j0.644}"), ("x^{4\\frac{1}{2}}", "x^2"),
    # \text{} rule, 2 Oct 2026: same unit, unequal values; a unit on one side only.
    # (Different words, equal values: the moments-master pair above.)
    ("5\\text{ cm}", "6\\text{ cm}"), ("5\\text{ cm}", "5"),
]


def option_units(q):
    """[(label, [option string, ...], correct-or-None)] for every answer unit of q
    that offers options: B2's units (sub_answer_units + option_pool), plus the
    flagged-option shape. B11 and the scan compare options within each unit."""
    units = []
    for label, unit in sub_answer_units(q):
        if "_valid_letters" in unit:
            continue
        pool = option_pool(unit)
        if pool:
            units.append((label, pool, resolve_correct(unit)))
    fl = flagged_option_texts_and_correct_count(q)
    if fl:
        units.append(("flagged", fl[0], None))
    return units


def value_equal_pairs(pool):
    """Sorted pairs of DISTINCT option strings in pool that are equal in value,
    each pair once. Identical strings are B2's business, not this."""
    import itertools
    distinct = list(dict.fromkeys(p for p in pool if isinstance(p, str)))
    parsed = {}
    for p in distinct:
        v = parse_value(p)
        if v is not None:
            parsed[p] = v
    out = []
    for a, b in itertools.combinations(parsed, 2):
        if a.strip() != b.strip() and equal(parsed[a], parsed[b]):
            out.append(tuple(sorted((a, b))))
    return out


def equal(a, b):
    """True if two parse_value() results are the same value."""
    sp = _sympy_env()["sp"]
    ka, va = a
    kb, vb = b
    if {ka, kb} <= {"num", "expr"}:
        try:
            d = sp.simplify(va - vb)
            if d == 0:
                return True
            if d.is_number:
                x, y = complex(sp.N(va, 30)), complex(sp.N(vb, 30))
                if x == 0 or y == 0:
                    return x == y
                return abs(x - y) <= 1e-12 * max(abs(x), abs(y))
        except Exception:
            return False
        return False
    if ka != kb:
        return False
    if ka in ("ratio", "interval"):
        return va == vb
    if ka == "text":
        return va[0] == vb[0] and equal(va[1], vb[1])
    if ka == "tuple":
        return len(va) == len(vb) and all(sp.simplify(x - y) == 0 for x, y in zip(va, vb))
    if ka == "eq":
        try:
            if va == 0 or vb == 0:
                return False
            q = sp.simplify(va / vb)
            return q.is_number and q != 0
        except Exception:
            return False
    return False


# ---------------------------------------------------------------------------
# B7's KaTeX half: render sites found by behaviour (to-do §1.31, 2 Oct 2026)
# ---------------------------------------------------------------------------
# Until 2 Oct, B7 found KaTeX inputs with a regex on two call shapes, K(x.field)
# and katex.renderToString(x.field) (katex_field_names above). 50 games render
# through 84 wrappers under other names (rk, rkStr, rkI, tex, kx, renderKaTeX,
# FDP.mathHtml ...), with locals, ternaries and iteration callbacks, so B7 never
# saw their strings: the KaTeX wrapper audit (docs/audit-katex-wrappers.md)
# found 386 strings in 19 games by B7's own test where B7 reported 0. A list of
# wrapper names would go stale with the next wrapper written, so this section
# finds them the way the audit did, from the same esprima tree as B8/B9:
#
#   katex_wrappers()       a function is a wrapper when a parameter, or a local
#                          derived from it, reaches the first argument of
#                          katex.render / katex.renderToString / MaffsText.html,
#                          directly or through another wrapper, to a fixed point.
#                          Names play no part.
#   katex_render_sites()   every call of one of those (a wrapper's own call on
#                          its parameter is its body, not a site).
#   resolve_render_site()  the exact strings that reach a site, per bank
#                          question: locals, ternaries (both branches), ||, &&,
#                          template literals, +, iteration callbacks, source
#                          literals. A site that calls a game function, or that
#                          cannot be rebuilt from the bank, comes back unresolved
#                          with its reason, never silently empty.
#
# extract-banks.py then renders every resolved string through the site's own
# callee in the page, and check-banks.py tests the result with
# katex_lost_word_spaces(). Ported from scripts/audit-katex/ (find_wrappers.py,
# site_fields.py, site_eval.py), which stays as the reference prototype.

_FN_TYPES = ("FunctionDeclaration", "FunctionExpression", "ArrowFunctionExpression")
KATEX_SINKS = ("katex.render", "katex.renderToString",
               "window.katex.render", "window.katex.renderToString")
MAFFSTEXT_SINK = "MaffsText.html"
_ITERATORS = ("forEach", "map", "filter", "some", "every", "find", "flatMap")


def _ast_children(n):
    out = []
    for k, v in vars(n).items():
        if k in ("range", "loc", "type"):
            continue
        if isinstance(v, list):
            out += [c for c in v if hasattr(c, "type")]
        elif hasattr(v, "type"):
            out.append(v)
    return out


def _walk_p(n, visit, parent=None):
    """walk() with the parent passed to `visit`, iteratively (some game
    scripts nest deeply enough to trouble recursion)."""
    stack = [(n, parent)]
    while stack:
        x, p = stack.pop()
        visit(x, p)
        for c in reversed(_ast_children(x)):
            stack.append((c, x))


def _parents(tree):
    par = {}
    _walk_p(tree, lambda x, p: par.__setitem__(id(x), p))
    return par


def _ids_in(n):
    """Identifier names an expression reads (not property names)."""
    out = set()

    def v(x, p):
        if x.type != "Identifier":
            return
        if p is not None and p.type == "MemberExpression" and p.property is x and not p.computed:
            return
        if p is not None and p.type == "Property" and p.key is x and not p.computed and not p.shorthand:
            return
        out.add(x.name)
    _walk_p(n, v)
    return out


def _value_ids_in(n):
    """Like _ids_in, but an identifier used only as the object of a plain
    field read (`q.prompt`) does not count: that passes a field, not the value
    itself. A method call on it (`s.replace(...)`) still counts."""
    field_objs, called = set(), set()

    def pre(x, p):
        if x.type == "MemberExpression" and not x.computed and x.object.type == "Identifier":
            field_objs.add(id(x.object))
        if x.type == "CallExpression" and x.callee.type == "MemberExpression" \
                and x.callee.object.type == "Identifier":
            called.add(id(x.callee.object))
    _walk_p(n, pre)
    out = set()

    def v(x, p):
        if x.type != "Identifier":
            return
        if p is not None and p.type == "MemberExpression" and p.property is x and not p.computed:
            return
        if p is not None and p.type == "Property" and p.key is x and not p.computed and not p.shorthand:
            return
        if id(x) in field_objs and id(x) not in called:
            return
        out.add(x.name)
    _walk_p(n, v)
    return out


def callee_name(call):
    """'K', 'katex.render', 'FDP.mathHtml', 'window.katex.render' -- or None."""
    c = call.callee
    if c.type == "Identifier":
        return c.name
    if c.type == "MemberExpression" and not c.computed:
        o = c.object
        if o.type == "Identifier":
            return o.name + "." + c.property.name
        if o.type == "MemberExpression" and not o.computed and o.object.type == "Identifier":
            return o.object.name + "." + o.property.name + "." + c.property.name
        return "?." + c.property.name
    return None


def _fn_name(node, parent):
    if node.type == "FunctionDeclaration" and node.id:
        return node.id.name
    if parent is not None:
        if parent.type == "VariableDeclarator" and parent.id.type == "Identifier":
            return parent.id.name
        if parent.type == "Property":
            return literal_key(parent.key)
        if parent.type == "AssignmentExpression":
            left = parent.left
            if left.type == "Identifier":
                return left.name
            if left.type == "MemberExpression" and not left.computed:
                return (left.object.name + "." if left.object.type == "Identifier" else "") \
                    + left.property.name
    if node.type == "FunctionExpression" and node.id:
        return node.id.name
    return None


def _param_names(fn):
    out = []
    for p in fn.params:
        if p.type == "Identifier":
            out.append(p.name)
        elif p.type == "AssignmentPattern" and p.left.type == "Identifier":
            out.append(p.left.name)
        else:
            out.append(None)
    return out


def _tainted_locals(fn, seeds):
    """Names inside `fn` whose value derives from `seeds`: assigned from an
    expression reading a tainted name, a for..of over one, or the parameter of
    a forEach/map/replace callback on one. Iterated to a fixed point."""
    t = set(seeds)
    changed = True
    while changed:
        changed = False

        def v(x, p):
            nonlocal changed
            if x.type == "VariableDeclarator" and x.id.type == "Identifier" and x.init is not None:
                if x.id.name not in t and _value_ids_in(x.init) & t:
                    t.add(x.id.name)
                    changed = True
            elif x.type == "AssignmentExpression" and x.left.type == "Identifier":
                if x.left.name not in t and _value_ids_in(x.right) & t:
                    t.add(x.left.name)
                    changed = True
            elif x.type in ("ForOfStatement", "ForInStatement"):
                left = x.left
                nm = None
                if left.type == "VariableDeclaration" and left.declarations[0].id.type == "Identifier":
                    nm = left.declarations[0].id.name
                elif left.type == "Identifier":
                    nm = left.name
                if nm and nm not in t and _ids_in(x.right) & t:
                    t.add(nm)
                    changed = True
            elif x.type == "CallExpression" and x.callee.type == "MemberExpression" \
                    and not x.callee.computed and x.callee.property.name in ("forEach", "map", "replace"):
                if _value_ids_in(x.callee.object) & t:
                    for a in x.arguments:
                        if a.type in _FN_TYPES:
                            for pn in _param_names(a):
                                if pn and pn not in t:
                                    t.add(pn)
                                    changed = True
        _walk_p(fn.body, v)
    return t


def _functions(tree):
    fns = []
    _walk_p(tree, lambda x, p: fns.append((x, _fn_name(x, p))) if x.type in _FN_TYPES else None)
    return fns


def katex_wrappers(tree, src):
    """{name: info} for every KaTeX wrapper in a game's inline scripts, found
    by data flow (see the section comment). info: name, param (the index of
    the parameter that reaches KaTeX), param_name, params, line, via (what it
    calls), depth (1 = calls KaTeX itself), splits (routes through
    MaffsText.html, so prose and \\( \\) maths are separated), calls (each
    sink call in its body, with its argument and options text)."""
    shim = _shim_for_parser(src)
    fns = _functions(tree)
    known = {MAFFSTEXT_SINK: {"param": 0, "depth": 1, "splits": True}}
    wrappers = {}
    changed, rounds = True, 0
    while changed and rounds < 10:
        changed, rounds = False, rounds + 1
        for f, nm in fns:
            if not nm or nm in wrappers:
                continue
            pn = _param_names(f)
            for i, p in enumerate(pn):
                if not p:
                    continue
                t = _tainted_locals(f, {p})
                hits = []

                def cv(x, par):
                    if x.type != "CallExpression":
                        return
                    cn = callee_name(x)
                    if cn in KATEX_SINKS and x.arguments and _value_ids_in(x.arguments[0]) & t:
                        hits.append((cn, x))
                    elif cn in known and len(x.arguments) > known[cn]["param"] \
                            and _value_ids_in(x.arguments[known[cn]["param"]]) & t:
                        hits.append((cn, x))
                _walk_p(f.body, cv)
                if not hits:
                    continue
                info = {"name": nm, "param": i, "param_name": p, "params": pn,
                        "line": line_of(src, f.range[0]),
                        "via": sorted({cn for cn, _ in hits}),
                        "depth": max(1 if cn in KATEX_SINKS else 1 + known[cn]["depth"]
                                     for cn, _ in hits),
                        "splits": any(cn in known and known[cn].get("splits") for cn, _ in hits),
                        "calls": []}
                for cn, c in hits:
                    oi = 2 if cn.endswith(".render") else 1
                    info["calls"].append({
                        "callee": cn, "line": line_of(src, c.range[0]),
                        "arg": shim[c.arguments[0].range[0]:c.arguments[0].range[1]],
                        "options": (shim[c.arguments[oi].range[0]:c.arguments[oi].range[1]]
                                    if len(c.arguments) > oi else "")})
                wrappers[nm] = info
                known[nm] = {"param": i, "depth": info["depth"], "splits": info["splits"]}
                changed = True
                break
    return wrappers


def _enclosing_fns(node, par):
    """Enclosing function nodes of `node`, innermost first."""
    out = []
    n = par.get(id(node))
    while n is not None:
        if n.type in _FN_TYPES:
            out.append(n)
        n = par.get(id(n))
    return out


def _literal_string(n):
    if n.type == "Literal" and isinstance(n.value, str):
        return n.value
    if n.type == "TemplateLiteral" and not n.expressions:
        return n.quasis[0].value.cooked
    if n.type == "BinaryExpression" and n.operator == "+":
        a, b = _literal_string(n.left), _literal_string(n.right)
        if a is not None and b is not None:
            return a + b
    return None


def katex_render_sites(html):
    """(wrappers, sites) for one game page. Each site is a dict: callee
    (katex.*, MaffsText.html or a wrapper name), param (the argument index
    that reaches KaTeX), line, enclosing (innermost named function or
    '(top level)'), arg (its source text), and in-memory AST handles
    (_arg, _par, _tree) that resolve_render_site() uses. Not JSON-safe until
    those three are dropped."""
    tree, src = parse_game_source(html)
    if tree is None:
        return None, None
    shim = _shim_for_parser(src)
    wrappers = katex_wrappers(tree, src)
    par = _parents(tree)
    fn_names = {id(f): nm for f, nm in _functions(tree)}
    taint_cache = {}

    def tainted(fn, w):
        k = id(fn)
        if k not in taint_cache:
            taint_cache[k] = _tainted_locals(fn, {p for p in _param_names(fn) if p})
        return taint_cache[k]

    selectors = _selection_functions(tree)
    page_fns = _page_functions(tree)
    sinks = {s: 0 for s in KATEX_SINKS}
    sinks[MAFFSTEXT_SINK] = 0
    sinks.update({n: w["param"] for n, w in wrappers.items()})
    sites = []

    def v(x, p):
        if x.type != "CallExpression":
            return
        cn = callee_name(x)
        if cn not in sinks or len(x.arguments) <= sinks[cn]:
            return
        a = x.arguments[sinks[cn]]
        encl = _enclosing_fns(x, par)
        # A wrapper's own call on (something derived from) its parameter is
        # the wrapper's body, not a site: its call sites are the sites.
        for f in encl:
            nm = fn_names.get(id(f))
            if nm in wrappers and _value_ids_in(a) & tainted(f, wrappers[nm]):
                return
        enc_name = next((fn_names.get(id(f)) for f in encl if fn_names.get(id(f))), None)
        args = []
        for k, arg in enumerate(x.arguments):
            text = shim[arg.range[0]:arg.range[1]]
            lit = None
            if arg.type == "Literal" and not getattr(arg, "regex", None):
                lit = arg.value
            elif arg.type == "UnaryExpression" and arg.operator == "!" and arg.argument.type == "Literal":
                lit = not arg.argument.value
            args.append({"text": text[:200], "literal": lit})
        sites.append({"callee": cn, "param": sinks[cn], "line": line_of(src, x.range[0]),
                      "enclosing": enc_name or "(top level)",
                      "arg": shim[a.range[0]:a.range[1]][:300], "args": args,
                      "_arg": a, "_call": x, "_par": par, "_tree": tree, "_selectors": selectors,
                      "_page_fns": page_fns, "_shim": shim})
    _walk_p(tree, v)
    return wrappers, sites


class _Unresolved(Exception):
    pass


class _BankRoot(Exception):
    """A chain's root traced back to a bank variable or to the question being
    shown: read it off the current bank object instead."""


class _Elems(list):
    """An array value whose elements keep their own bank paths:
    [(value, path), ...]."""


class _PushedArgs:
    """list.push(a, b): stands for the array [a, b] when the list's elements
    are resolved."""
    type = "PushedArgs"

    def __init__(self, call, args=None):
        self.call = call
        self.args = call.arguments if args is None else args
        self.range = call.range


class _LazyObj(dict):
    """An object literal with computed values ({content: card.display}):
    a property is evaluated only when it is read, in the context the literal
    was built in."""

    def __init__(self, node, d, dpath, env):
        super().__init__()
        self.node, self.d, self.dpath, self.env = node, d, dpath, dict(env)
        for prop in node.properties:
            if prop.type == "Property":
                k = literal_key(prop.key)
                if k is not None:
                    self[k] = prop.value


class _JS:
    """A value only the page can compute: a JavaScript expression, evaluated
    at the page's global scope in extract-banks.py, built from the game's own
    functions applied to bank values (ratTex(q.pr), fmt(q.sumFx2)) or from the
    page's own DOM (document.querySelectorAll(...)). `many` means it
    evaluates to an array, each element one value."""

    def __init__(self, src, many=False, seed=()):
        # seed: statements run first, putting the page in the state this value
        # was computed in (currentQ = {...}; completedTable = ...;)
        self.src, self.many, self.seed = src, many, tuple(seed)

    def each(self, fn, seed=()):
        """Apply a JS expression template ({0} = the value) to the value, or to
        every element when `many`."""
        sd = _merge_seeds(self.seed, seed)
        if self.many:
            return _JS("Array.from(%s).map(__e => %s)" % (self.src, fn.replace("{0}", "__e", 1)),
                       True, sd)
        return _JS(fn.replace("{0}", "(%s)" % self.src, 1), False, sd)


def _merge_seeds(*seeds):
    out = []
    for sd in seeds:
        for st in sd:
            if st not in out:
                out.append(st)
    return tuple(out)


def _seed_of(*vals):
    seeds = []
    for v in vals:
        if isinstance(v, _JS):
            seeds.append(v.seed)
        elif isinstance(v, _Elems):
            seeds.append(_seed_of(*[x for x, _p in v]))
    return _merge_seeds(*seeds)


def _to_js(v):
    """JavaScript source for a value the resolver holds."""
    if isinstance(v, _JS):
        if v.many:
            raise _Unresolved("a list computed in the page passed on as one value")
        return v.src
    if isinstance(v, _LazyObj):
        raise _Unresolved("an object with computed fields passed to a game function")
    if isinstance(v, _Elems):
        return "[" + ",".join(_to_js(x) for x, _p in v) + "]"
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return json.dumps(v, ensure_ascii=False)


def _chain(n):
    """member chain -> (root identifier, [prop | '*' | int])"""
    props = []
    while n.type == "MemberExpression":
        if n.computed:
            props.append(n.property.value if n.property.type == "Literal"
                         and isinstance(n.property.value, (int, str)) else "*")
        else:
            props.append(n.property.name)
        n = n.object
    if n.type != "Identifier":
        raise _Unresolved("member chain on a %s" % n.type)
    return n.name, list(reversed(props))


class _Undef(str):
    """A string built from a value the question does not have ('n = ' + q.n
    on a question with no n): what JavaScript would show as "undefined".
    Dropped, unlike a real string that contains the word ('Is undefined')."""


def _js_str(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return str(int(v)) if v.is_integer() else repr(v)
    if v is None:
        return "undefined"
    if isinstance(v, _Elems):
        return ",".join(_js_str(x) for x, _p in v)
    if isinstance(v, list):
        return ",".join(_js_str(x) for x in v)
    if isinstance(v, dict):
        raise _Unresolved("an object turned into a string")
    return str(v)


def _join_paths(*ps):
    ps = [p for p in ps if p]
    return "+".join(dict.fromkeys(ps)) if ps else None


def _seg(path, prop):
    if path is None:
        return None
    if prop == "*" or isinstance(prop, int):
        return path + "[]"
    return path + "." + prop


def _elements(v, p):
    """(value, path) pairs of an array-ish value."""
    if isinstance(v, _JS):
        return [(_JS(("Array.from(%s).flatMap(__e => Array.from(__e))" if v.many
                      else "Array.from(%s)") % v.src, True, v.seed), p)]
    if isinstance(v, _Elems):
        return list(v)
    if isinstance(v, list):
        return [(e, _seg(p, "*")) for e in v]
    if isinstance(v, dict) and not isinstance(v, _LazyObj):
        return [(e, _seg(p, "*")) for e in v.values()]
    return []


# Array methods that only select, copy or reorder elements -- never change one.
_SELECTING_METHODS = {"slice", "filter", "concat", "sort", "reverse", "splice", "flat"}


def _selection_functions(tree):
    """Names of game functions that only select or reorder elements of their
    arguments (shuffle, makeChoices ...), found by behaviour: a body with no
    string or template literal, no string-building, and no call other than to
    Math, an array method that selects, or another such function. A call to
    one returns an array whose elements are its array arguments' elements
    (and any scalar arguments themselves). Iterated to a fixed point."""
    fns = {nm: f for f, nm in _functions(tree) if nm and f.type in _FN_TYPES}
    allowed_methods = _SELECTING_METHODS | {"random", "floor", "ceil", "min", "max", "abs", "round",
                                            "push", "pop", "shift", "unshift", "indexOf",
                                            "includes", "some", "every", "find", "findIndex",
                                            "forEach", "from", "isArray"}
    sel = set()
    changed = True
    while changed:
        changed = False
        for nm, f in fns.items():
            if nm in sel or not any(_param_names(f)):
                continue
            ok = [True]

            def v(x, p):
                if not ok[0]:
                    return
                if x.type == "TemplateLiteral" or (x.type == "Literal" and isinstance(x.value, str)):
                    ok[0] = False
                elif x.type == "CallExpression":
                    c = x.callee
                    if c.type == "Identifier":
                        if c.name not in sel:
                            ok[0] = False
                    elif c.type == "MemberExpression" and not c.computed:
                        if c.property.name not in allowed_methods:
                            ok[0] = False
                    else:
                        ok[0] = False
                elif x.type == "ReturnStatement" and (x.argument is None
                                                      or x.argument.type == "ObjectExpression"):
                    ok[0] = False
            _walk_p(f.body, v)
            has_return = [False]
            _walk_p(f.body, lambda x, p: has_return.__setitem__(0, True)
                    if x.type == "ReturnStatement" else None)
            if f.body.type != "BlockStatement":
                has_return[0] = True
            if ok[0] and has_return[0]:
                sel.add(nm)
                changed = True
    return sel


_MATH_FNS = {"Math.abs": abs, "Math.min": min, "Math.max": max, "Math.sqrt": math.sqrt,
             "Math.floor": math.floor, "Math.ceil": math.ceil,
             "Math.round": lambda x: math.floor(x + 0.5)}


# What a game function may read and still be computed in the page from its
# arguments alone: these, its own parameters and locals, other such functions,
# and top-level constants nothing ever changes.
_PAGE_GLOBALS = {"Math", "JSON", "Number", "String", "Boolean", "Array", "Object",
                 "parseInt", "parseFloat", "isNaN", "isFinite", "Infinity", "NaN",
                 "undefined", "katex", "MaffsText", "Set", "Map", "Error", "RegExp"}
_MUTATING_METHODS = {"push", "pop", "shift", "unshift", "splice", "sort", "reverse", "fill"}


def _page_functions(tree):
    """{name: game state it reads} for every top-level game function the page
    can be asked to compute, found by behaviour (to-do §1.31, Jon's ruling of
    2 Oct): it writes nothing outside itself and touches no DOM, and reads
    only its parameters and locals, other such functions, top-level constants
    nothing changes, and game state -- a top-level variable the game assigns
    or mutates. The set is that state, transitively through what it calls.

    An empty set: the result depends on the arguments alone, so a call on bank
    values is computed in the page as it stands (ratTex(q.pr), fmt(q.sumFx2)).
    A non-empty set (exactEX() reads completedTable): the page is first put in
    the state the question puts the game in, each of those variables set from
    the game's own assignment of it (_SiteEval.seed_for)."""
    fns, top, mutated = {}, set(), set()
    for node in tree.body:
        if node.type == "FunctionDeclaration" and node.id:
            fns[node.id.name] = node
        elif node.type == "VariableDeclaration":
            for dcl in node.declarations:
                if dcl.id.type != "Identifier":
                    continue
                if dcl.init is not None and dcl.init.type in ("ArrowFunctionExpression",
                                                              "FunctionExpression"):
                    fns[dcl.id.name] = dcl.init
                else:
                    top.add(dcl.id.name)

    def mv(x, p):
        t = x.left if x.type == "AssignmentExpression" else \
            x.argument if x.type == "UpdateExpression" else None
        while t is not None and t.type == "MemberExpression":
            t = t.object
        if t is not None and t.type == "Identifier":
            mutated.add(t.name)
        if x.type == "CallExpression" and x.callee.type == "MemberExpression" \
                and not x.callee.computed and x.callee.property.name in _MUTATING_METHODS \
                and x.callee.object.type == "Identifier":
            mutated.add(x.callee.object.name)
    _walk_p(tree, mv)
    state = top & mutated
    stable = top - mutated

    reads = {}
    for nm, f in fns.items():
        own = _own_names(f)
        free, writes_out = set(), [False]

        def rv(x, p):
            if x.type == "Identifier":
                if p is not None and p.type == "MemberExpression" and p.property is x and not p.computed:
                    return
                if p is not None and p.type == "Property" and p.key is x and not p.computed \
                        and not p.shorthand:
                    return
                if x.name not in own:
                    free.add(x.name)
            t = x.left if x.type == "AssignmentExpression" else \
                x.argument if x.type == "UpdateExpression" else None
            while t is not None and t.type == "MemberExpression":
                t = t.object
            if t is not None and t.type == "Identifier" and t.name not in own:
                writes_out[0] = True
        _walk_p(f.body, rv)
        reads[nm] = (free, writes_out[0])
    ok = {nm for nm, (free, w) in reads.items()
          if not w and free <= (_PAGE_GLOBALS | stable | state | set(fns))}
    changed = True
    while changed:
        changed = False
        for nm in list(ok):
            if (reads[nm][0] & set(fns)) - ok:
                ok.discard(nm)
                changed = True
    out = {nm: set(reads[nm][0] & state) for nm in ok}
    changed = True
    while changed:
        changed = False
        for nm in ok:
            for g in reads[nm][0] & ok:
                if not out[g] <= out[nm]:
                    out[nm] |= out[g]
                    changed = True
    return {nm: frozenset(v) for nm, v in out.items()}


def _own_names(f):
    """Every name declared inside a function, its parameters included."""
    names = {p for p in _param_names(f) if p}

    def dv(x, p):
        if x.type == "VariableDeclarator" and x.id.type == "Identifier":
            names.add(x.id.name)
        elif x.type in _FN_TYPES:
            names.update(n for n in _param_names(x) if n)
            if x.type == "FunctionDeclaration" and x.id:
                names.add(x.id.name)
        elif x.type == "CatchClause" and x.param is not None and x.param.type == "Identifier":
            names.add(x.param.name)
    _walk_p(f.body if f.type in _FN_TYPES else f, dv)
    return names


_DOM_READS = {"document.querySelectorAll", "document.querySelector", "document.getElementById"}


# Shared platform helpers with a documented contract (schools/assets/): the
# elements of what they return are the elements of what they were given.
_SHARED_SELECTORS = {"MaffsOptions.build"}


def _tree_index(tree, par):
    """One walk of a game's tree, kept on the tree: every binding of every
    name (declarations, assignments, pushes, element writes, for..of), the
    member writes (state.mode = ...), the top-level declarations and which of
    them the game changes. Looking a name up is then a filter, not a walk."""
    idx = getattr(tree, "_mfg_index", None)
    if idx is not None:
        return idx
    binds, assigned, mutated = {}, set(), set()
    owner_cache = {}

    def owner(node):
        k = id(node)
        if k not in owner_cache:
            n = par.get(k)
            while n is not None and n.type not in _FN_TYPES:
                n = par.get(id(n))
            owner_cache[k] = n
        return owner_cache[k]

    def v(x, p):
        t = x.type
        if t == "VariableDeclarator" and x.id.type == "Identifier" and x.init is not None:
            binds.setdefault(x.id.name, []).append(("decl", x.init, owner(x), x))
        elif t == "AssignmentExpression":
            left = x.left
            if left.type == "Identifier":
                binds.setdefault(left.name, []).append(
                    ("assign", x.right, None, x) if x.operator == "=" else ("compound", x, None, x))
            elif left.type == "MemberExpression":
                if left.computed and x.operator == "=" and left.object.type == "Identifier":
                    # slotValues[i] = s: an element of the array
                    binds.setdefault(left.object.name, []).append(
                        ("element", _PushedArgs(x, [x.right]), None, x))
                if not left.computed and left.object.type == "Identifier":
                    assigned.add((left.object.name, left.property.name))
            r = left
            while r.type == "MemberExpression":
                r = r.object
            if r.type == "Identifier":
                mutated.add(r.name)
        elif t == "UpdateExpression":
            a = x.argument
            if a.type == "Identifier":
                binds.setdefault(a.name, []).append(("compound", x, None, x))
            elif a.type == "MemberExpression" and not a.computed and a.object.type == "Identifier":
                assigned.add((a.object.name, a.property.name))
            r = a
            while r.type == "MemberExpression":
                r = r.object
            if r.type == "Identifier":
                mutated.add(r.name)
        elif t == "CallExpression" and x.callee.type == "MemberExpression" \
                and not x.callee.computed and x.callee.property.name in ("push", "unshift") \
                and x.callee.object.type == "Identifier":
            binds.setdefault(x.callee.object.name, []).append(("expr", _PushedArgs(x), None, x))
        elif t in ("ForOfStatement", "ForInStatement"):
            left = x.left
            nm = (left.declarations[0].id.name if left.type == "VariableDeclaration"
                  and left.declarations[0].id.type == "Identifier"
                  else left.name if left.type == "Identifier" else None)
            if nm:
                binds.setdefault(nm, []).append(
                    ("elements_of" if t == "ForOfStatement" else "keys_of", x.right, owner(x), x))
    _walk_p(tree, v)
    top = {}
    for node in tree.body:
        if node.type == "VariableDeclaration":
            for dcl in node.declarations:
                if dcl.id.type == "Identifier" and dcl.init is not None:
                    top.setdefault(dcl.id.name, dcl.init)
    idx = {"binds": binds, "assigned": assigned, "top": top,
           "state_vars": {n for n in top if n in mutated}}
    tree._mfg_index = idx
    return idx


class _SiteEval:
    """Evaluates a site's argument against one bank object at a time. A value
    is a list of (value, path) pairs; path names the bank field a string came
    from (`QUESTIONS.d[]`), or None for a source literal."""

    def __init__(self, tree, par, bank_vars, selectors, group_heads=None, page_fns=None,
                 src=""):
        self.page_fns = page_fns or {}
        self.src = src
        self._seeding = set()
        self.group_heads = group_heads or {}
        self._static = {}
        self.tree = tree
        self.par = par
        self.bank_vars = bank_vars
        self.selectors = selectors
        self.env = {}
        self.depth = 0
        self._bind_cache = {}
        self._bind_guards = {}
        self._callers = {}
        self._owner_cache = {}
        self._resolving = set()
        self.missed = False
        self.index = _tree_index(tree, par)
        self.assigned = self.index["assigned"]
        self.top = self.index["top"]
        self.state_vars = self.index["state_vars"]

    def static(self, name):
        """A top-level declaration's literal value, as authored, or None."""
        if name not in self._static:
            try:
                self._static[name] = literal_to_json(self.top[name]) if name in self.top else None
            except _NotLiteral:
                self._static[name] = None
        return self._static[name]

    def _owner(self, node):
        k = id(node)
        if k not in self._owner_cache:
            n = self.par.get(k)
            while n is not None and n.type not in _FN_TYPES:
                n = self.par.get(id(n))
            self._owner_cache[k] = n
        return self._owner_cache[k]

    def bindings(self, name, at):
        """Where a name read at node `at` gets its value, innermost scope
        first: [('expr', node)], [('elements', node)], [('param', fn)] or
        [('compound', node)]. Cached per (name, innermost scope)."""
        inner = self._owner(at)
        key = (name, id(inner))
        if key not in self._bind_cache:
            self._bind_cache[key] = self._bindings(name, at)
        return self._bind_cache[key]

    def _bindings(self, name, at):
        for scope in _enclosing_fns(at, self.par) + [None]:
            if scope is not None and name in _param_names(scope):
                i = _param_names(scope).index(name)
                call = self.par.get(id(scope))
                if call is not None and call.type == "CallExpression" \
                        and call.callee.type == "MemberExpression" and not call.callee.computed:
                    m = call.callee.property.name
                    if (m in _ITERATORS and i == 0) or (m == "reduce" and i == 1):
                        return [("elements", call.callee.object)]
                    if m == "call" and call.callee.object.type == "MemberExpression" \
                            and not call.callee.object.computed \
                            and call.callee.object.property.name in _ITERATORS \
                            and i == 0 and call.arguments:
                        # Array.prototype.forEach.call(list, fn)
                        return [("elements", call.arguments[0])]
                return [("param", scope)]
            found = []
            lo, hi = (scope.body.range if scope is not None else (None, None))
            for kind, payload, owner, node in self.index["binds"].get(name, ()):
                if kind in ("decl", "elements_of", "keys_of"):
                    if owner is not scope:
                        continue
                elif scope is not None and not (lo <= node.range[0] < hi):
                    continue
                if kind == "decl":
                    found.append(("expr", payload))
                elif kind == "elements_of":
                    found.append(("elements", payload))
                elif kind == "keys_of":
                    found.append(("compound", payload))
                elif kind == "assign":
                    found.append(("expr", payload))
                    # if (q.im === 0) cLatex = ...; else ...: each assignment
                    # holds only where its own conditions do
                    if id(payload) not in self._bind_guards:
                        self._bind_guards[id(payload)] = _guards(node, self.par)
                else:
                    found.append((kind, payload))
            if found:
                return found
        return []

    def ev(self, n, d, dpath):
        self.depth += 1
        try:
            if self.depth > 60:
                raise _Unresolved("binding chain too deep")
            return self._ev(n, d, dpath)
        finally:
            self.depth -= 1

    def _ev(self, n, d, dpath):
        t = n.type
        if t == "Literal":
            if getattr(n, "regex", None):
                raise _Unresolved("regex literal as a value")
            return [(n.value, None)]
        if t == "TemplateLiteral":
            outs = [("", None)]
            for i, q in enumerate(n.quasis):
                outs = [(self.binop("+", o, q.value.cooked or ""), p) for o, p in outs]
                if i < len(n.expressions):
                    vs = self.ev(n.expressions[i], d, dpath)
                    outs = [(self.binop("+", o, v), _join_paths(p, vp))
                            for o, p in outs for v, vp in vs]
            return outs
        if t == "BinaryExpression":
            L, R = self.ev(n.left, d, dpath), self.ev(n.right, d, dpath)
            out = []
            for a, pa in L:
                for b, pb in R:
                    out.append((self.binop(n.operator, a, b), _join_paths(pa, pb)
                                if n.operator == "+" else None))
            return out
        if t == "LogicalExpression":
            out = []
            for a, pa in self.ev(n.left, d, dpath):
                if isinstance(a, _JS):
                    out += [(_JS("(%s) %s (%s)" % (_to_js(a), n.operator, _to_js(b)), False,
                                 _seed_of(a, b)),
                             _join_paths(pa, pb)) for b, pb in self.ev(n.right, d, dpath)]
                    continue
                take_left = (bool(a) if n.operator == "||" else a is not None
                             if n.operator == "??" else not a)
                out += [(a, pa)] if take_left else self.ev(n.right, d, dpath)
            return out
        if t == "UnaryExpression":
            vals = self.ev(n.argument, d, dpath)
            if any(isinstance(v, _JS) for v, _p in vals):
                raise _Unresolved("a value computed in the page used in %s" % n.operator)
            if n.operator == "!":
                return [(not v, None) for v, _p in vals]
            if n.operator == "-":
                return [(-v if isinstance(v, (int, float)) else None, None) for v, _p in vals]
            if n.operator == "typeof":
                return [({str: "string", bool: "boolean", int: "number", float: "number"}
                         .get(type(v), "object" if v is not None else "undefined"), None)
                        for v, _p in vals]
            raise _Unresolved("unsupported operator %s" % n.operator)
        if t == "ConditionalExpression":
            # Both branches, unless the test decides it: which one a student
            # sees depends on play.
            truth = self.truth(n.test, d, dpath)
            if truth is True:
                return self.ev(n.consequent, d, dpath)
            if truth is False:
                return self.ev(n.alternate, d, dpath)
            return self.ev(n.consequent, d, dpath) + self.ev(n.alternate, d, dpath)
        if t == "ArrayExpression":
            items = _Elems()
            for el in n.elements:
                if el is None:
                    continue
                if el.type == "SpreadElement":
                    for v, p in self.ev(el.argument, d, dpath):
                        items += _elements(v, p)
                else:
                    items += self.ev(el, d, dpath)
            return [(items, None)]
        if t == "ObjectExpression":
            try:
                return [(literal_to_json(n), None)]
            except _NotLiteral:
                return [(_LazyObj(n, d, dpath, self.env), None)]
        if t == "MemberExpression":
            root, props = _chain(n)
            return self.member(root, props, n, d, dpath)
        if t == "Identifier":
            if n.name == "undefined":
                return [(None, None)]
            return self.identifier(n.name, n, d, dpath)
        if t == "CallExpression":
            return self.call(n, d, dpath)
        if t == "SequenceExpression":
            return self.ev(n.expressions[-1], d, dpath)
        if t == "PushedArgs":
            items = _Elems()
            for a in n.args:
                items += self.ev(a, d, dpath)
            return [(items, None)]
        raise _Unresolved("unsupported expression (%s)" % t)

    @staticmethod
    def binop(op, a, b):
        if isinstance(a, _JS) or isinstance(b, _JS):
            if op != "+":
                raise _Unresolved("a value computed in the page used in %s" % op)
            if isinstance(a, _JS) and isinstance(b, _JS) and a.many and b.many:
                raise _Unresolved("two lists computed in the page joined")
            sd = _seed_of(a, b)
            if isinstance(a, _JS) and a.many:
                return a.each("String({0}) + String(%s)" % _to_js(b), sd)
            if isinstance(b, _JS) and b.many:
                return b.each("String(%s) + String({0})" % _to_js(a), sd)
            return _JS("String(%s) + String(%s)" % (_to_js(a), _to_js(b)), False, sd)
        if op == "+":
            if isinstance(a, (str, list, dict)) or isinstance(b, (str, list, dict)) \
                    or a is None or b is None:
                joined = _js_str(a) + _js_str(b)
                if a is None or b is None or isinstance(a, _Undef) or isinstance(b, _Undef):
                    return _Undef(joined)
                return joined
            return a + b
        if op in ("===", "=="):
            return a == b
        if op in ("!==", "!="):
            return a != b
        if op in ("<", ">", "<=", ">=", "-", "*", "/", "%"):
            if not all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in (a, b)):
                raise _Unresolved("arithmetic on a non-number")
            return {"<": a < b, ">": a > b, "<=": a <= b, ">=": a >= b, "-": a - b,
                    "*": a * b, "/": a / b if b else None, "%": a % b if b else None}[op]
        raise _Unresolved("unsupported operator %s" % op)

    def truth(self, test, d, dpath, missing_is_false=False):
        """True / False when the test decides the same way for every value it
        can take here, else None (unknown: both ways stay possible). A test
        that reads a field the bank object does not have through a root that
        is not known to be the question (state.mode) is unknown, unless
        missing_is_false."""
        self.missed = False
        try:
            raw = self.ev(test, d, dpath)
        except (_Unresolved, _BankRoot):
            return None
        if any(isinstance(v, _JS) for v, _p in raw):
            return None
        vals = [bool(v) if not isinstance(v, (list, dict)) else True for v, _p in raw]
        if self.missed and not missing_is_false:
            return None
        if vals and all(vals):
            return True
        if vals and not any(vals):
            return False
        return None

    def identifier(self, name, at, d, dpath):
        if name in self.env:
            return [self.env[name]]
        if name in self.bank_vars and name in self.top:
            raise _BankRoot(name)
        b = self.bindings(name, at)
        if not b:
            raise _Unresolved("unbound name %s" % name)
        key = (name, id(self._owner(at)))
        if key in self._resolving:
            # pairsCards = shuffle(pairsCards) adds no new value; but a test on
            # reveal = !reveal cannot be decided from the source
            self.missed = True
            return []
        self._resolving.add(key)
        try:
            return self._identifier(name, b, d, dpath)
        finally:
            self._resolving.discard(key)

    def _identifier(self, name, b, d, dpath):
        out = []
        for kind, x in b:
            if kind == "expr":
                if any(self.truth(t, d, dpath) is (not want)
                       for t, want in self._bind_guards.get(id(x), ())):
                    continue
                out += self.ev(x, d, dpath)
            elif kind == "elements":
                for v, p in self.ev(x, d, dpath):
                    out += _elements(v, p) if not isinstance(v, str) else [(c, p) for c in v]
            elif kind == "element":
                # slotValues[selectedSlot] = tile, the tile a student picked:
                # what cannot be traced adds nothing; the rest still counts
                try:
                    out += self.ev(x, d, dpath)
                except _Unresolved:
                    pass
            elif kind == "param":
                raise _Unresolved("parameter %s of %s" % (
                    name, _fn_name(x, self.par.get(id(x))) or "an anonymous function"))
            else:
                raise _Unresolved("compound assignment to %s" % name)
        return out

    def member(self, root, props, n, d, dpath):
        """A member chain. Its root is resolved through its bindings when they
        lead to a source constant (a top-level table that is not a bank). When
        they lead to a bank variable, to a parameter or to game state, the root
        is "the question being shown" whatever the game calls it (q, currentQ,
        stage), and the chain is read off the current bank object."""
        if props and isinstance(props[0], str) and (root, props[0]) in self.assigned:
            # state.mode, q._zCalcDone: written by the game as it runs, so its
            # value here is not knowable from the source or the bank.
            raise _Unresolved("game state %s.%s" % (root, props[0]))
        roots, bank_root, root_exc = None, root in self.bank_vars, None
        if bank_root and props and isinstance(props[0], str) and props[0] != "*" \
                and props[0] not in self.group_heads.get(root, {props[0]}):
            # CONTENT.learn.examples: a table inside a bank variable, outside
            # every extracted question group -- read as authored.
            static = self.static(root)
            if static is not None:
                roots, bank_root = [(static, root)], False
        if roots is not None:
            pass
        elif root in self.env:
            roots = [self.env[root]]
        else:
            try:
                roots = self.identifier(root, n, d, dpath)
            except _BankRoot:
                bank_root = True     # questions = shuffle([...QUESTIONS[level]])
            except _Unresolved as e:
                # A parameter or an unbound global is the question being shown;
                # anything else (a call, game state) is kept, and raised if the
                # question does not have the field after all.
                if not str(e).startswith(("parameter ", "unbound name ")):
                    root_exc = e
            if roots is not None and not any(isinstance(v, (dict, list, _JS)) for v, _p in roots):
                roots = None
            if roots is not None:
                # let currentQ = null: a placeholder until the game assigns it
                roots = [(v, p) for v, p in roots if v is not None]
        if roots is None and props and isinstance(props[0], str) and props[0] not in d \
                and root not in self.env:
            # pDisplayHTML(r) reads r.pr, which no question has: r is whatever
            # the game's own calls of pDisplayHTML pass it
            roots = self.call_site_values(root, n, d, dpath)
        fallback = roots is None
        if roots is None and not d and props:
            raise _Unresolved("%s needs a question" % root)
        if roots is None:
            roots = [(d, dpath)]
            # pool[qIdx], questions[i]: indexing whatever holds the question
            # being shown gives that question.
            while props and (props[0] == "*" or isinstance(props[0], int)):
                props = props[1:]
            if bank_root:
                literal_var = root in self.bank_vars
                while props and (props[0] == "*" or isinstance(props[0], int)
                                 or (literal_var and isinstance(props[0], str)
                                     and props[0] not in d)):
                    props = props[1:]
                if not props:
                    # QUESTIONS[level]: a whole bank, or part of one -- only the
                    # question it is indexed down to is a bank object.
                    raise _BankRoot(root)
        vals = roots
        for prop in props:
            nxt = []
            for v, p in vals:
                if isinstance(v, _JS):
                    nxt.append((_elements(v, p)[0][0] if prop == "*" else
                                v.each("{0}[%s]" % json.dumps(prop)), _seg(p, prop) if p else None))
                elif prop == "*":
                    nxt += _elements(v, p)
                elif prop == "length" and isinstance(v, (list, str)):
                    nxt.append((len(v), None))
                elif isinstance(v, _LazyObj) and prop in v:
                    saved, self.env = self.env, v.env
                    try:
                        nxt += self.ev(v[prop], v.d, v.dpath)
                    finally:
                        self.env = saved
                elif isinstance(v, dict) and prop in v:
                    nxt.append((v[prop], _seg(p, prop)))
                elif fallback and isinstance(v, dict):
                    if root_exc is not None:
                        raise root_exc
                    # state.mode read off a question: not evidence of anything;
                    # currentQ.kValue on a question without one is undefined
                    if not bank_root:
                        self.missed = True
                    nxt.append((None, None))
                elif isinstance(v, list) and isinstance(prop, int):
                    els = _elements(v, p)
                    nxt.append(els[prop] if prop < len(els) else (None, None))
                else:
                    nxt.append((None, None))
            vals = nxt
        return vals

    def call(self, n, d, dpath):
        c = n.callee
        name = callee_name(n)
        if (c.type == "Identifier" and c.name in self.selectors) or name in _SHARED_SELECTORS:
            items = _Elems()
            for a in n.arguments:
                arg = a.argument if a.type == "SpreadElement" else a
                for v, p in self.ev(arg, d, dpath):
                    items += _elements(v, p) if isinstance(v, list) or a.type == "SpreadElement" \
                        else [(v, p)]
            return [(items, None)]
        if name in _MATH_FNS:
            argvals = [self.ev(a, d, dpath) for a in n.arguments]
            out = []
            for combo in __import__("itertools").product(*argvals):
                xs = [v for v, _p in combo]
                if not all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in xs):
                    raise _Unresolved("Math on a non-number")
                out.append((_MATH_FNS[name](*xs), None))
            return out
        if c.type == "Identifier" and c.name in ("parseFloat", "Number", "parseInt") \
                and len(n.arguments) >= 1:
            out = []
            for v, p in self.ev(n.arguments[0], d, dpath):
                if isinstance(v, _JS):
                    out.append((v.each(c.name + "({0})"), p))
                    continue
                try:
                    f = float(v) if c.name != "parseInt" else float(int(float(v)))
                except (TypeError, ValueError):
                    raise _Unresolved("%s() of %r" % (c.name, v))
                out.append((int(f) if f.is_integer() else f, p))
            return out
        if c.type == "Identifier" and c.name == "String" and len(n.arguments) == 1:
            return [(v.each("String({0})") if isinstance(v, _JS) else _js_str(v), p)
                    for v, p in self.ev(n.arguments[0], d, dpath)]
        if (c.type == "Identifier" and c.name in self.page_fns) or name in _DOM_READS:
            return self.page_call(name, n.arguments, d, dpath)
        if c.type == "MemberExpression" and not c.computed:
            m = c.property.name
            args = n.arguments
            if m == "test" and c.object.type == "Literal" and getattr(c.object, "regex", None) \
                    and len(args) == 1:
                rx = self.regex(c.object)
                return [(bool(rx.search(_js_str(v))), None) for v, _p in self.ev(args[0], d, dpath)]
            if m in ("map", "flatMap") and len(args) == 1 and args[0].type in _FN_TYPES \
                    and _param_names(args[0]) and _param_names(args[0])[0]:
                return [(self.map_values(c.object, args[0], d, dpath), None)]
            obj = self.ev(c.object, d, dpath)
            if any(isinstance(v, _JS) for v, _p in obj):
                argjs, argseed = self.js_args(m, args, d, dpath)
                out = []
                for v, p in obj:
                    if not isinstance(v, _JS):
                        v = _JS(_to_js(v))
                    out.append((v.each("{0}.%s(%s)" % (m, ", ".join(argjs)), argseed), p))
                return out
            if m in _SELECTING_METHODS:
                extra = _Elems()
                if m == "concat":
                    for a in args:
                        for v, p in self.ev(a, d, dpath):
                            extra += _elements(v, p) if isinstance(v, list) else [(v, p)]
                return [(_Elems(_elements(v, p) + list(extra)), None) for v, p in obj]
            if any(a.type in _FN_TYPES or (a.type == "Identifier" and a.name in self.page_fns)
                   for a in args):
                # q.freqs.reduce((a, b) => a + b, 0), bank.find(b => b.re === q.re):
                # the page runs the game's own callback, its free locals captured
                parts, seed = self.js_args(m, args, d, dpath)
                out = []
                for v, p in obj:
                    if v is None:
                        continue
                    recv = v if isinstance(v, _JS) else _JS(_to_js(v))
                    out.append((recv.each("{0}.%s(%s)" % (m, ", ".join(parts)), seed), p))
                return out
            lits = []
            for a in args:
                if a.type == "Literal" and getattr(a, "regex", None):
                    lits.append(self.regex(a))
                elif a.type == "Literal":
                    lits.append(a.value)
                else:
                    raise _Unresolved("%s() with a computed argument" % m)
            out = []
            for v, p in obj:
                res = self.method(m, v, lits)
                if isinstance(v, _Undef) and isinstance(res, str):
                    res = _Undef(res)
                out.append((res, p if m in (
                    "replace", "trim", "toString", "toUpperCase", "toLowerCase", "join",
                    "toFixed") else None))
            return out
        raise _Unresolved("calls %s()" % (name or "a computed function"))

    def page_call(self, name, args, d, dpath):
        """f(args) for a game function computed in the page (see
        _page_functions), or a read of the page's own DOM: one page
        expression per combination of argument values."""
        import itertools
        alts = []
        for a in args:
            if a.type == "SpreadElement":
                raise _Unresolved("spread arguments to %s()" % name)
            vals = self.ev(a, d, dpath)
            try:
                for v, _p in vals:
                    if not isinstance(v, _JS):
                        _to_js(v)
            except _Unresolved:
                # generateProductDistractors(products, completedTable): a value
                # only the page holds whole -- its own source, run in the page
                js, sd = self.page_source(a, d, dpath)
                vals = [(_JS(js, False, sd), None)]
            alts.append(vals)
        state = self.page_fns.get(name, frozenset())
        seeds = self.seed_for(state, d, dpath) if state else [()]
        out = []
        for combo in itertools.product(*alts):
            many = [i for i, (v, _p) in enumerate(combo) if isinstance(v, _JS) and v.many]
            if len(many) > 1:
                raise _Unresolved("%s() on two lists computed in the page" % name)
            parts = ["__e" if i in many else _to_js(v) for i, (v, _p) in enumerate(combo)]
            call = "%s(%s)" % (name, ", ".join(parts))
            path = _join_paths(*[p for _v, p in combo])
            for sd in seeds:
                sd = _merge_seeds(_seed_of(*[v for v, _p in combo]), sd)
                if many:
                    out.append((_JS("Array.from(%s).map(__e => %s)" % (combo[many[0]][0].src, call),
                                    True, sd), path))
                else:
                    out.append((_JS(call, False, sd), path))
        return out

    def call_site_values(self, name, at, d, dpath):
        """Values a parameter takes at its function's call sites, or None."""
        b = self.bindings(name, at)
        if len(b) != 1 or b[0][0] != "param":
            return None
        fn = b[0][1]
        fname = _fn_name(fn, self.par.get(id(fn)))
        if not fname or "." in fname:
            return None
        i = _param_names(fn).index(name)
        key = ("callsite", id(fn), i)
        if key in self._resolving:
            return None
        if fname not in self._callers:
            self._callers[fname] = []
            _walk_p(self.tree, lambda x, p: self._callers[fname].append(x)
                    if x.type == "CallExpression" and x.callee.type == "Identifier"
                    and x.callee.name == fname else None)
        out = []
        self._resolving.add(key)
        try:
            for call in self._callers[fname]:
                if len(call.arguments) > i:
                    try:
                        out += self.ev(call.arguments[i], d, dpath)
                    except (_Unresolved, _BankRoot):
                        continue
        finally:
            self._resolving.discard(key)
        out = [(v, p) for v, p in out if isinstance(v, (dict, list, _JS))]
        return out or None

    def js_args(self, m, args, d, dpath):
        """(JS sources, seed) for a method call's arguments run in the page."""
        parts, seed = [], ()
        for a in args:
            if a.type in _FN_TYPES:
                js, sd = self.page_source(a, d, dpath)
            elif a.type == "Identifier" and a.name in self.page_fns:
                if self.page_fns[a.name]:
                    raise _Unresolved("%s() reads game state as a callback" % a.name)
                js, sd = a.name, ()                  # products.map(ratKey)
            elif a.type == "Literal" and getattr(a, "regex", None):
                js, sd = "/%s/%s" % (a.regex.pattern, a.regex.flags), ()
            else:
                vals = self.ev(a, d, dpath)
                if len(vals) != 1:
                    raise _Unresolved("%s() with several possible arguments" % m)
                js, sd = _to_js(vals[0][0]), _seed_of(vals[0][0])
            parts.append(js)
            seed = _merge_seeds(seed, sd)
        return parts, seed

    def seed_for(self, names, d, dpath):
        """The page statements that put the game in the state question `d`
        puts it in, for the game-state variables `names`: each set from the
        game's own assignment of it (the trivial resets -- [], {}, null --
        left out where there is a real one), evaluated here where it can be
        and in the page where it cannot. Alternatives (an assignment per
        mode) multiply; more than 8 is unresolved."""
        alts = [()]
        for g in sorted(names):
            vals = self.global_values(g, d, dpath)
            alts = [_merge_seeds(base, sd, ("%s = %s;" % (g, src),))
                    for base in alts for src, sd in vals]
            if len(alts) > 8:
                raise _Unresolved("game state %s takes too many forms" % g)
        return alts

    def global_values(self, g, d, dpath):
        """[(js source, seed)] for game-state variable g, question d."""
        if not d or not dpath or "[]" in dpath or "." in dpath:
            # only a whole question puts the game in a state; a table row does not
            raise _Unresolved("game state %s needs a question" % g)
        key = (g, id(d))
        if key in self._seeding:
            raise _Unresolved("game state %s depends on itself" % g)
        self._seeding.add(key)
        try:
            binds = [(k, x) for k, x in self.bindings(g, self.tree)]
            exprs = [x for k, x in binds if k == "expr" and hasattr(x, "type")
                     and x.type != "PushedArgs"]
            real = [x for x in exprs if not (
                (x.type == "ArrayExpression" and not x.elements)
                or (x.type == "ObjectExpression" and not x.properties)
                or (x.type == "Literal" and x.value is None))]
            out = []
            for x in (real or exprs):
                if any(self.truth(t, d, dpath) is (not want)
                       for t, want in self._bind_guards.get(id(x), ())):
                    continue
                try:
                    for v, _p in self.ev(x, d, dpath):
                        out.append((_to_js(v), _seed_of(v)))
                except _BankRoot:
                    if not d:
                        raise _Unresolved("game state %s needs a question" % g)
                    out.append((_to_js(d), ()))      # currentQ = questionQueue[i]
                except _Unresolved:
                    out.append(self.page_source(x, d, dpath))
            if not out:
                raise _Unresolved("game state %s is never set" % g)
            return list(dict.fromkeys(out))
        finally:
            self._seeding.discard(key)

    def page_source(self, node, d, dpath):
        """(js source, seed) for an expression the page computes from its own
        source text: its free locals captured from here, the game state it
        reads seeded first."""
        own = _own_names(node) if node.type in _FN_TYPES else set()
        if node.type not in _FN_TYPES:
            _walk_p(node, lambda x, p: own.update(_own_names(x)) if x.type in _FN_TYPES else None)
        names = sorted(n for n in _ids_in(node) if n not in own and n not in _PAGE_GLOBALS
                       and n not in self.page_fns and n != "undefined")
        caps, seed = [], ()
        for nm in names:
            if nm in self.state_vars:
                for src, sd in self.global_values(nm, d, dpath)[:1]:
                    seed = _merge_seeds(seed, sd, ("%s = %s;" % (nm, src),))
                continue
            if nm in self.top and nm not in self.state_vars:
                continue                     # a constant table: the page has it
            try:
                vals = self.identifier(nm, node, d, dpath)
            except _BankRoot:
                if not d:
                    raise _Unresolved("%s needs a question" % nm)
                vals = [(d, dpath)]
            if len(vals) != 1:
                raise _Unresolved("%s has %d possible values here" % (nm, len(vals)))
            caps.append((nm, _to_js(vals[0][0])))
            seed = _merge_seeds(seed, _seed_of(vals[0][0]))
        text = self.src[node.range[0]:node.range[1]]
        if caps:
            text = "((%s) => (%s))(%s)" % (", ".join(c for c, _j in caps), text,
                                           ", ".join(j for _c, j in caps))
        else:
            text = "(%s)" % text
        return text, seed

    def map_values(self, receiver, fn, d, dpath):
        """arr.map(x => expr): expr evaluated with x bound to each element."""
        rets = [fn.body] if fn.body.type != "BlockStatement" else []
        if not rets:
            _walk_p(fn.body, lambda x, p: rets.append(x.argument)
                    if x.type == "ReturnStatement" and x.argument is not None
                    and self._owner(x) is fn else None)
        if not rets:
            raise _Unresolved("map() callback returns nothing")
        name = _param_names(fn)[0]
        items = _Elems()
        saved = dict(self.env)
        try:
            try:
                recv = self.ev(receiver, d, dpath)
                elems = [e for v, p in recv for e in (_elements(v, p) if not isinstance(v, str) else [])]
            except _BankRoot:
                elems = [(d, dpath)]     # unique.map(q => ...) over bank questions
            for e in elems:
                self.env = dict(saved)
                self.env[name] = e
                for r in rets:
                    items += self.ev(r, d, dpath)
        finally:
            self.env = saved
        return items

    @staticmethod
    def regex(node):
        flags = node.regex.flags
        return re.compile(node.regex.pattern, re.I if "i" in flags else 0), "g" in flags

    @staticmethod
    def method(m, v, args):
        if isinstance(v, str):
            if m == "replace" and len(args) == 2 and isinstance(args[1], str):
                rep = args[1]
                if isinstance(args[0], tuple):
                    (rx, glob) = args[0]
                    pyrep = re.sub(r"\$(\d)", r"\\\1", rep.replace("\\", "\\\\"))
                    return rx.sub(pyrep, v, count=0 if glob else 1)
                return v.replace(args[0], rep, 1)
            if m in ("includes", "startsWith", "endsWith") and len(args) == 1 \
                    and isinstance(args[0], str):
                return {"includes": args[0] in v, "startsWith": v.startswith(args[0]),
                        "endsWith": v.endswith(args[0])}[m]
            if m == "indexOf" and len(args) == 1 and isinstance(args[0], str):
                return v.find(args[0])
            if m == "trim" and not args:
                return v.strip()
            if m == "toUpperCase" and not args:
                return v.upper()
            if m == "toLowerCase" and not args:
                return v.lower()
            if m == "toString" and not args:
                return v
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            if m == "toFixed" and len(args) <= 1:
                k = int(args[0]) if args else 0
                from decimal import Decimal, ROUND_HALF_UP
                return str(Decimal(repr(v)).quantize(Decimal(1).scaleb(-k), rounding=ROUND_HALF_UP))
            if m == "toString" and not args:
                return _js_str(v)
        if isinstance(v, list) and m == "join" and len(args) <= 1:
            sep = args[0] if args else ","
            return sep.join(_js_str(x) for x, _p in _elements(v, None))
        if isinstance(v, list) and m == "includes" and len(args) == 1:
            return any(x == args[0] for x, _p in _elements(v, None))
        if v is None:
            return None
        raise _Unresolved("%s() on a %s" % (m, type(v).__name__))


def _bank_taint(tree, par, bank_vars):
    """Symbols -- (name, id of its declaring function, or None at the top) --
    whose value can carry bank data: the bank variables, anything assigned
    from them, a function that reads one, a parameter some call passes one to,
    a callback over one. Iterated to a fixed point. A render site whose
    argument reads none of them is fed only by what the game generates as it
    runs (log-laws' Solve families): runtime-only, not unresolved."""
    owner_cache = {}

    def owner(node):
        k = id(node)
        if k not in owner_cache:
            n = par.get(k)
            while n is not None and n.type not in _FN_TYPES:
                n = par.get(id(n))
            owner_cache[k] = n
        return owner_cache[k]

    decls = {}
    fn_nodes = {}

    def dv(x, p):
        if x.type == "VariableDeclarator" and x.id.type == "Identifier":
            decls.setdefault(id(owner(x)), set()).add(x.id.name)
            if x.init is not None and x.init.type in _FN_TYPES:
                fn_nodes[(x.id.name, id(owner(x)))] = x.init
        elif x.type in _FN_TYPES:
            decls.setdefault(id(x), set()).update(n for n in _param_names(x) if n)
            if x.type == "FunctionDeclaration" and x.id:
                decls.setdefault(id(owner(x)), set()).add(x.id.name)
                fn_nodes[(x.id.name, id(owner(x)))] = x
    _walk_p(tree, dv)

    def sym(name, at):
        for f in _enclosing_fns(at, par):
            if name in decls.get(id(f), ()):
                return (name, id(f))
        return (name, id(None))

    def reads(expr):
        out = set()

        def v(x, p):
            if x.type != "Identifier":
                return
            if p is not None and p.type == "MemberExpression" and p.property is x and not p.computed:
                return
            if p is not None and p.type == "Property" and p.key is x and not p.computed \
                    and not p.shorthand:
                return
            out.add(sym(x.name, x))
        _walk_p(expr, v)
        return out

    edges = []        # (target symbol, set of symbols it reads)

    def ev_(x, p):
        if x.type == "VariableDeclarator" and x.id.type == "Identifier" and x.init is not None:
            edges.append((sym(x.id.name, x.id), reads(x.init)))
        elif x.type == "AssignmentExpression" and x.left.type == "Identifier":
            edges.append((sym(x.left.name, x.left), reads(x.right)))
        elif x.type == "AssignmentExpression" and x.left.type == "MemberExpression":
            root = x.left               # G.questions = pool.slice(0, 6)
            while root.type == "MemberExpression":
                root = root.object
            if root.type == "Identifier":
                edges.append((sym(root.name, root), reads(x.right)))
        elif x.type in ("ForOfStatement", "ForInStatement"):
            left = x.left
            nm = (left.declarations[0].id if left.type == "VariableDeclaration" else left)
            if nm.type == "Identifier":
                edges.append((sym(nm.name, nm), reads(x.right)))
        elif x.type == "CallExpression":
            c = x.callee
            if c.type == "MemberExpression" and not c.computed:
                m = c.property.name
                if m in ("push", "unshift") and c.object.type == "Identifier":
                    edges.append((sym(c.object.name, c.object),
                                  set().union(*[reads(a) for a in x.arguments]) if x.arguments else set()))
                recv = c.object
                if m == "call" and c.object.type == "MemberExpression" and x.arguments:
                    recv = x.arguments[0]
                for a in x.arguments:
                    cb = a if a.type in _FN_TYPES else \
                        fn_nodes.get(sym(a.name, a)) if a.type == "Identifier" else None
                    if cb is not None:        # built.map(finish) as well as map(x => ...)
                        for pn in _param_names(cb)[:2]:
                            if pn:
                                edges.append(((pn, id(cb)), reads(recv)))
            elif c.type == "Identifier":
                f = fn_nodes.get(sym(c.name, c))
                if f is not None:
                    for pn, arg in zip(_param_names(f), x.arguments):
                        if pn:
                            edges.append(((pn, id(f)), reads(arg)))
    _walk_p(tree, ev_)
    for (name, oid), f in fn_nodes.items():
        # what a function returns carries bank data when its body reads some
        # from outside itself; its own parameters get theirs from call sites
        inner = {id(f)}
        _walk_p(f.body, lambda x, p: inner.add(id(x)) if x.type in _FN_TYPES else None)
        edges.append(((name, oid), {sy for sy in reads(f.body) if sy[1] not in inner}))

    tainted = set()
    # A parameter of a function nothing in the script calls by name (a click
    # handler, a method looked up at runtime) may be passed anything: assume
    # bank data, so a site there is never written off as runtime-only.
    called = set()

    def cv(x, p):
        if x.type == "CallExpression" and x.callee.type == "Identifier":
            called.add(sym(x.callee.name, x.callee))
        if x.type == "CallExpression":
            for a in x.arguments:
                if a.type == "Identifier" and sym(a.name, a) in fn_nodes \
                        and x.callee.type == "MemberExpression":
                    called.add(sym(a.name, a))
    _walk_p(tree, cv)
    for key, f in fn_nodes.items():
        if key not in called:
            tainted.update((pn, id(f)) for pn in _param_names(f) if pn)

    def bv(x, p):
        if x.type == "VariableDeclarator" and x.id.type == "Identifier" and x.id.name in bank_vars:
            tainted.add(sym(x.id.name, x.id))
    _walk_p(tree, bv)
    changed = True
    while changed:
        changed = False
        for target, srcs in edges:
            if target not in tainted and srcs & tainted:
                tainted.add(target)
                changed = True
    return lambda expr: bool(reads(expr) & tainted)


def _guards(call, par):
    """[(test node, wanted truth)] for every if / ?: / && / || between a site's
    call and its innermost enclosing function: the conditions under which
    this call runs at all."""
    out = []
    child, n = call, par.get(id(call))
    while n is not None:
        if n.type in _FN_TYPES:
            # an inline callback (q.steps.forEach(st => ...)) runs under the
            # conditions of the call that passes it; a named function does not
            if par.get(id(n)) is None or par.get(id(n)).type != "CallExpression":
                break

        if n.type == "IfStatement":
            if n.consequent is child:
                out.append((n.test, True))
            elif n.alternate is child:
                out.append((n.test, False))
        elif n.type == "ConditionalExpression":
            if n.consequent is child:
                out.append((n.test, True))
            elif n.alternate is child:
                out.append((n.test, False))
        elif n.type == "LogicalExpression" and n.right is child:
            out.append((n.left, n.operator != "||"))
        child, n = n, par.get(id(n))
    return out


def bank_objects(bank):
    """[(dict, path)] for every object in a bank: each question, under its
    variable's name, and every object nested in one (`INDUCTION.stages[]`),
    each once."""
    out, seen = [], set()
    for lv in (bank.get("levels") or {}).values():
        for g in lv.get("groups", []):
            gk = (g["variable"], tuple(g.get("path", [])))
            if gk in seen:
                continue
            seen.add(gk)

            def walk(v, path):
                if isinstance(v, dict):
                    out.append((v, path))
                    for k, x in v.items():
                        walk(x, path + "." + k)
                elif isinstance(v, list):
                    for x in v:
                        walk(x, path + "[]")
            for q in g["questions"]:
                walk(q, g["variable"])
    return out


def resolve_render_site(site, bank):
    """What reaches one render site, per bank question:
    {"items": {key: item}, "unresolved": reason or None, "runtime_only": bool}.
    An item is {"path", "source"} for a string rebuilt here, or {"path", "js",
    "many"} for one the page must compute (a game function applied to bank
    values, or the page's DOM); path is the bank field it came from
    (`QUESTIONS.d[]`) or 'literal'. "unresolved" says why the site cannot be
    rebuilt (check-banks --ci lists it); "runtime_only" marks a site whose
    strings only a generator builds at runtime, with no bank behind them.

    "Reaches" is literal: a guard between the call and its function (`if
    (v.includes('\\')) rk(b, v); else b.textContent = v`) is evaluated per
    value, so a string the game shows as plain text is not counted as rendered
    by KaTeX. A guard that cannot be decided statically keeps both ways open."""
    a, par, tree = site["_arg"], site["_par"], site["_tree"]
    lit = _literal_string(a)
    guards = _guards(site["_call"], par)
    has_bank = bool(bank) and not bank.get("generator")
    groups = [g for lv in (bank or {}).get("levels", {}).values() for g in lv.get("groups", [])]
    bank_vars = {g["variable"] for g in groups}
    heads = {}
    for g in groups:
        heads.setdefault(g["variable"], set()).add(g["path"][0] if g.get("path") else "*")
    heads = {v: h for v, h in heads.items() if "*" not in h}
    ev = _SiteEval(tree, par, bank_vars, site["_selectors"], heads, site["_page_fns"],
                   site["_shim"])
    bare = a.name if a.type == "Identifier" else None
    out = {}

    def result(unresolved=None, runtime_only=False):
        return {"items": out, "unresolved": unresolved, "runtime_only": runtime_only}

    def admitted(v, p, d, dpath):
        if not guards:
            return True
        ev.env = {bare: (v, p)} if bare else {}
        try:
            for test, want in guards:
                if ev.truth(test, d, dpath) is (not want):
                    return False
            return True
        finally:
            ev.env = {}

    # The callee itself may read game state (renderValue reads displayMode):
    # it renders each question's strings in the state that question sets.
    callee_state = site["_page_fns"].get(site["callee"], frozenset())
    callee_seeds = {}

    def seeds_for(d, dpath):
        if not callee_state or not d:
            return [()]
        if id(d) not in callee_seeds:
            try:
                callee_seeds[id(d)] = ev.seed_for(callee_state, d, dpath)
            except _Unresolved:
                callee_seeds[id(d)] = [()]
        return callee_seeds[id(d)]

    def add(v, vp, d, dpath):
        if isinstance(v, _JS):
            if admitted(v, vp, d, dpath):
                # a value computed in the state a question sets is that question's
                path = vp or ((dpath or "page") + "(state)" if v.seed else "page")
                for cs in seeds_for(d, dpath):
                    sd = _merge_seeds(v.seed, cs)
                    out.setdefault("js:" + "".join(sd) + v.src,
                                   {"path": path, "js": v.src, "many": v.many, "seed": list(sd)})
        elif isinstance(v, str) and v and not isinstance(v, _Undef) and admitted(v, vp, d, dpath):
            for cs in seeds_for(d, dpath):
                out.setdefault("".join(cs) + v, {"path": vp or "literal", "source": v,
                                                 "seed": list(cs)})

    if lit is not None:
        if lit:
            add(lit, None, {}, None)
        return result()
    if a.type == "Literal":
        return result()          # setMsg(''), submitFormulaAnswer(null): nothing to render
    cache = tree.__dict__.setdefault("_mfg_taint", {})
    key = frozenset(bank_vars)
    if key not in cache:
        cache[key] = _bank_taint(tree, par, bank_vars)
    from_bank = cache[key]

    def unresolved(reason):
        # Fed by nothing that can carry bank data: built by the game at runtime.
        if not from_bank(a):
            return result(reason, True)
        return result(reason)
    # Which bank fields can the expression read, through its local bindings?
    firsts, seen, probe = set(), set(), [a]
    while probe:
        x = probe.pop()
        if id(x) in seen:
            continue
        seen.add(id(x))

        def fv(y, p):
            if y.type == "MemberExpression":
                try:
                    _r, props = _chain(y)
                except _Unresolved:
                    return
                if props and isinstance(props[0], str) and props[0] != "*":
                    firsts.add(props[0])
        _walk_p(x, fv)
        for nm in _ids_in(x):
            for b in ev.bindings(nm, x):
                if b[0] in ("expr", "elements", "element") and hasattr(b[1], "type"):
                    probe.append(b[1] if b[1].type != "PushedArgs" else b[1].call)

    def collect(d, dpath):
        for v, vp in ev.ev(a, d, dpath):
            add(v, vp, d, dpath)

    try:
        first_err = None
        try:
            collect({}, None)        # literals, source tables, the page's DOM
        except (_Unresolved, _BankRoot) as e:
            first_err = e
        if not firsts and not (first_err is not None and "needs a question" in str(first_err)
                               and has_bank):
            if first_err is not None and not out:
                raise first_err
            if not out:
                return unresolved("no bank string reaches it (game state)")
            return result()
        if not firsts:
            # exactEX(): no field in sight, but computed in each question's state
            firsts = {k for d, p in bank_objects(bank) if "[]" not in p and "." not in p for k in d}
        if not has_bank:
            # Nothing on this page is a bank: whatever is not a literal or a
            # source table is built by the game as it runs.
            return result(None if out else "no bank: built at runtime", not out)
        dead = False
        objs = [(d, p) for d, p in bank_objects(bank) if firsts & set(d)]
        if not objs:
            if out:
                return result()
            # pDisplayHTML(r) reads r.pr, a field no question has but the game
            # computes from each one: evaluate per question all the same
            for d, p in bank_objects(bank):
                if "[]" in p or "." in p:
                    continue
                try:
                    collect(d, p)
                except (_Unresolved, _BankRoot):
                    pass
            if out:
                return result()
            # if (q.steps) { ...rk(step)... } on a bank with no `steps` anywhere:
            # the guard is false on every question, so nothing reaches the site.
            if guards and all(any(ev.truth(t, d, p, True) is (not want) for t, want in guards)
                              for d, p in bank_objects(bank)):
                return result()
            return unresolved("reads %s, which no bank object has" % ", ".join(sorted(firsts)))
        errors = []
        for d, p in objs:
            try:
                collect(d, p)
            except (_Unresolved, _BankRoot) as e:
                errors.append(str(e))
        if errors and (len(errors) == len(objs) or not out):
            return unresolved(errors[0])
        if not out and not dead:
            # Never silently empty: a site no bank string reaches is either
            # game state (a student's placed tiles) or generated at runtime.
            return unresolved("no bank string reaches it (game state)")
    except _Unresolved as e:
        return unresolved(str(e))
    except RecursionError:
        return unresolved("binding chain too deep")
    return result()


# B7's KaTeX-half test (2 Oct 2026; replaces katex_prose_hazard for this half).
# A string is a hit when a space it has in the source, between two tokens, is
# absent in what the student sees, and at least one of those tokens is a word.
# A word is a run of 3+ letters, or one of the 2-letter English function words
# below. Two-letter runs outside the list are maths: products such as mg (F =
# \mu mg), bx (e^{a + bx}) and mc (Q = mc\Delta T), which the audit's second
# count misread as words (its 3 false positives in 20). Units are OUT of scope
# for this rule: '13 cm' rendering as 13cm loses a space next to a unit, not a
# word, and is not flagged here.
KATEX_FUNCTION_WORDS = frozenset(
    "to of is as or an in on at by if so no be do up it we he me my us am".split())

# \text{}, \mathrm{} and \operatorname{} switch KaTeX to a mode that keeps
# spacing, so their contents are not tested; nested braces are allowed two
# deep, which the old single-level _KATEX_TEXT_MODE_WRAP could not match
# (higher-power's \text{Primes under 1{,}000} was B7's false positive).
_KATEX_TEXT_WRAP_NESTED = re.compile(
    r"\\(?:text|mathrm|operatorname)\s*\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}")
_LETTER_RUN = re.compile(r"(?<![A-Za-z])[A-Za-z]+(?![A-Za-z])")


def katex_source_for_test(s):
    """The source as B7 compares it: text-mode wraps and bare LaTeX commands
    removed (a command is a control token, not a word)."""
    return _KATEX_COMMAND.sub("", _KATEX_TEXT_WRAP_NESTED.sub("", s))


def is_katex_word(tok):
    return len(tok) >= 3 or tok.lower() in KATEX_FUNCTION_WORDS


def katex_lost_word_spaces(source, rendered):
    """Words (as defined above) that lose, in `rendered` (the visual text a
    student sees), a space they have beside them in `source`. Counted per
    word: the number of its occurrences with a space before (after) it in the
    source, against the same count in the rendered text; any shortfall is a
    loss. Returns the sorted list of words that lost a space ([] = no hit)."""
    src = katex_source_for_test(source)
    vis = re.sub(r"\s+", " ", rendered or "")
    lost = []
    for w in sorted({m.group(0) for m in _LETTER_RUN.finditer(src) if is_katex_word(m.group(0))}):
        whole = re.compile(r"(?<![A-Za-z])%s(?![A-Za-z])" % re.escape(w))
        sb = sa = 0
        joined_right = joined_left = False
        for m in whole.finditer(src):
            if m.start() > 0 and src[m.start() - 1].isspace() and src[:m.start()].strip():
                sb += 1
                # ABC\overline{D}: the group renders joined on, as ABCD
                joined_right = joined_right or src[m.end():m.end() + 1] in ("{", "}")
            if m.end() < len(src) and src[m.end()].isspace() and src[m.end():].strip():
                sa += 1
                joined_left = joined_left or src[m.start() - 1:m.start()] in ("{", "}")
        # A word joined to a brace group is measured from its free side only.
        before = re.compile(r"(?<![A-Za-z])%s%s" % (re.escape(w), "" if joined_right else "(?![A-Za-z])"))
        after = re.compile(r"%s%s(?![A-Za-z])" % ("" if joined_left else "(?<![A-Za-z])", re.escape(w)))
        vb = sum(1 for m in before.finditer(vis) if m.start() > 0 and vis[m.start() - 1] == " ")
        va = sum(1 for m in after.finditer(vis) if m.end() < len(vis) and vis[m.end()] == " ")
        if vb < sb or va < sa:
            lost.append(w)
    return lost
