#!/usr/bin/env python3
"""Checker tier 4, layer A, step 2: lint every extracted bank in data/banks/.

Reads what scripts/extract-banks.py wrote (the live, post-patch value of
every game's question bank) plus a fresh static AST pass per game (for B8
and B9, which need to see the source AS WRITTEN, not the value it evaluates
to -- a duplicate object key resolves silently by the time JS has read it,
and an index patch's damage is already baked into the value you'd read
back). Eleven rules, each with an ID:

  B1  correct answer missing or empty
  B2  duplicate options, including the correct one (compared the way
      dataset.val / MaffsOptions.build() compares: String(value))
  B3  duplicate questions within a level (exact, and separately
      whitespace/case-normalised)
  B4  a level's bank has fewer than 40 questions
  B5  an offered session length exceeds the level's bank
  B6  a draft marker in student-facing prose ("let me", "wait", ...)
  B7  two halves: a student-facing string with a run of 26+ letters and no
      space (general text of unknown source); and, rebuilt 2 Oct 2026 (to-do
      §1.31), KaTeX: every render site found by behaviour, the strings that
      reach it rebuilt per question and rendered in the page through the
      site's own callee, a hit when a space the source has beside a word is
      gone from what the student sees (bank_common.katex_lost_word_spaces).
      Plus MaffsText strings whose \( \) do not balance or do not render.
  B8  duplicate keys in one object literal (AST)
  B9  a hand-written `IDENT[literal] = ...` patch after the bank's literal
  B10 correct_override present
  B11 two options that are different strings but equal in value (5√2 and
      √50), compared with bank_common.parse_value()/equal(). Identified by
      content (bank_common.content_id), not by bank index or line. Deliberate
      form questions are listed in checker-allowlist.json, b11_form_questions.

Every finding is identified by content, never by bank index or source line
(todo item 7, 2 Oct 2026), so a known defect keeps its ledger match when the
code around it moves. On 28 Sep a one-line edit above test-the-claim's B8
entry moved it from line 527 to 526 and CI failed on a defect it already
tracked. The ids, by rule:

  B1 B2 B6 B7 B10  <content_id>::<rule>[.<sub-answer>] -- the question's content
  B3               <slug>::B3::<every copy's content hash, sorted, joined by +>
  B4 B5            <slug>::<level>
  B7 (KaTeX)       <slug>::B7::katex[<path>]::<sha12 of the string>#1 -- path is the bank
                   field (QUESTIONS.d[]), "literal" (source), "page" (the page's own DOM)
                   or "<VARIABLE>(state)" (computed in the state a question sets)
  B7 (MaffsText)   <slug>::B7::mathtext[<kind>]::<sha12 of the string>#<ordinal>
  B8               <slug>::B8::<enclosing name>::<dup keys>::<sha12 of the object>
  B9               <slug>::B9::<target as written>::<sha12 of the right-hand side>
  B11              <content_id>::B11::<the pair>

Where a finding sits (bank path and index) goes in its detail, and its source
line in "line"; neither is part of the id. Editing any field of a question
gives it a new id, as does renaming the function or variable a B8 object sits
in: CI then reports one new and one stale entry, which is expected.

B1, B2, B5 need a recognised answer key to check anything; a bank whose
correctness is computed rather than stored (regression-rumble, chart
scenarios, ...) correctly reports zero hits for those three and still runs
the rest. That is not a gap in this pass -- see docs/checker-tier4-design.md
for what layer A cannot see and why.

USAGE
-----
    python scripts/check-banks.py                       # lint, print report
    python scripts/check-banks.py --write-ledger         # (re)write the ledger
    python scripts/check-banks.py --ci                   # CI mode (see below)
    python scripts/check-banks.py --only matrix-crunch
    python scripts/check-banks.py --selftest             # B7 + B11 value-equality + content_id fixtures
    python scripts/check-banks.py --selftest-live        # B7 rendered in a real page + MaffsText throw check

CI MODE
-------
Compares this run's findings against data/check-ledger.json. FAILS only on:
  - a violation NOT already in the ledger (a new defect), or
  - a ledger entry that no longer reproduces (fixed, but the ledger was not
    cleared -- keeps the ledger honest rather than a stale wishlist).
A known, still-present violation is not a failure; it is tracked.
"""
import argparse
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_common as bc  # noqa: E402

ROOT = bc.ROOT
BANKS_DIR = bc.BANKS_DIR
LEDGER_PATH = os.path.join(ROOT, "data", "check-ledger.json")
ROSTER_PATH = os.path.join(ROOT, ".claude", "rules", "game-roster.md")
ALLOWLIST_PATH = os.path.join(ROOT, "scripts", "checker-allowlist.json")

RULE_NAMES = {
    "B1": "correct answer missing or empty",
    "B2": "duplicate options including correct",
    "B3": "duplicate question within a level",
    "B4": "level bank below 40",
    "B5": "offered session length exceeds the bank",
    "B6": "draft marker in student-facing prose",
    "B7": "rendering hazard: no-space run / KaTeX prose",
    "B8": "duplicate key in one object literal",
    "B9": "hand-written index patch after the bank literal",
    "B10": "correct_override present",
    "B11": "options equal in value",
}

DRAFT_MARKERS = ["wait", "let me", "recalculate", "actually let", "hmm", "oops",
                 "todo", "fixme"]
_WORD_MARKERS = {"wait", "hmm", "oops", "todo", "fixme"}
DRAFT_PATTERNS = [
    (m, re.compile(r"\b" + re.escape(m) + r"\b", re.IGNORECASE) if m in _WORD_MARKERS
     else re.compile(re.escape(m), re.IGNORECASE))
    for m in DRAFT_MARKERS
]

# STOP IF a rule produces more than RULE_MAX hits -- report before recording,
# it may be mis-specified rather than a real defect count. Raised 200 -> 500
# on 27 Sep 2026 when B7's KaTeX half first dropped its 26-letter threshold
# and space-loss alone looked like the test, which flagged 398 "hazards"
# across 9 games -- mostly ordinary maths ('-1 + j') whose spacing is
# cosmetic. Restored to 200 the same day once B7 was correctly redefined
# around prose, not space loss: verified false positives on real games gone
# (boolean-blitz, complex-converter, graph-sketcher, growth-and-decay,
# log-laws, truth-will-set-you-free all back to 0), true count 79 across the
# 3 games that actually have the defect.
RULE_MAX = 200
# B7 alone: the rebuilt KaTeX half (2 Oct 2026, to-do §1.31) sees every render
# site, not two call shapes, and its first run records the whole class at once.
# The KaTeX wrapper audit's second count measured it at 522 strings
# (docs/audit-katex-wrappers.md); 800 leaves room for the per-path split
# without letting a mis-specified test record thousands.
RULE_MAX_BY_RULE = {"B7": 800}


def roster_slugs():
    out = []
    with open(ROSTER_PATH, "r", encoding="utf-8") as fh:
        for line in fh:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 4 or not cells[0].isdigit():
                continue
            m = re.match(r"^`([a-z0-9-]+)`$", cells[2])
            if m:
                out.append(m.group(1))
    return out


def load_bank(slug):
    path = os.path.join(BANKS_DIR, slug + ".json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def dedup_groups(bank):
    """One entry per distinct (variable, path), unioned across levels, with
    the set of level keys it's the counted pool for. Avoids double-counting
    a level-invariant bank (matrix-crunch's QUESTIONS visible whole at every
    query) once per level it happens to be loaded under.
    """
    seen = {}
    for lv, info in bank.get("levels", {}).items():
        for g in info.get("groups", []):
            key = (g["variable"], tuple(g["path"]))
            if key not in seen:
                seen[key] = {"variable": g["variable"], "path": g["path"],
                              "questions": g["questions"], "count": g["count"],
                              "marking": g["marking"], "levels": set()}
            if g.get("in_pool", True):
                seen[key]["levels"].add(lv)
    return list(seen.values())


def sha12(text):
    """First 12 hex of the SHA-1 of a string: the content part of a B7, B8 or
    B9 id."""
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def question_ids(slug, groups):
    """{(variable, path, index): content_id} for every question in the game.
    Numbered over dedup_groups() in bank order, the order B11 numbers in, so
    exact copies get the same ordinals for every rule."""
    keys, qs = [], []
    for g in groups:
        for idx, q in enumerate(g["questions"]):
            if isinstance(q, dict):
                keys.append((g["variable"], tuple(g["path"]), idx))
                qs.append(q)
    return dict(zip(keys, bc.content_ids(slug, qs)))


def where(slug, group, idx, sub=None):
    """The finding's location for its detail, e.g. QUESTIONS.gcse[12]."""
    return loc_string(slug, group, idx, sub).split("::", 1)[1]


def loc_string(slug, group, idx, sub=None):
    path = ".".join(group["path"]) if group["path"] else ""
    where = "%s%s[%d]" % (group["variable"], ("." + path) if path else "", idx)
    if sub:
        where += "." + sub
    return "%s::%s" % (slug, where)


class Findings:
    def __init__(self):
        self.by_rule = {r: [] for r in RULE_NAMES}
        self._seen = set()

    def add(self, rule, entry_id, detail, line=None):
        # A level-invariant bank (matrix-crunch's QUESTIONS visible whole at
        # every level query) can put the same underlying question pair
        # through a level-scoped rule's (B3, B4) comparison more than once,
        # once per level it happens to be counted under. The finding itself
        # -- same rule, same location, same detail -- is one fact, not one
        # per level it was seen from.
        key = (rule, entry_id, detail)
        if key in self._seen:
            return
        self._seen.add(key)
        self.by_rule[rule].append({"id": entry_id, "detail": detail, "line": line})


def unit_correct_value(unit):
    return bc.resolve_correct(unit)


def is_empty_answer(val):
    if val is None:
        return True
    if isinstance(val, str) and val.strip() == "":
        return True
    return False


def lint_question_level_rules(slug, group, findings, tree, qids):
    """B1, B2, B6, B7, B10 -- properties of one question, independent of
    which level it's served under. Ids are the question's content_id (qids,
    from question_ids()); the bank path and index lead the detail.
    """
    lines = (bc.line_numbers_for_group(tree, group["variable"], group["path"],
                                        len(group["questions"]))
             if tree is not None else [None] * len(group["questions"]))
    for idx, q in enumerate(group["questions"]):
        if not isinstance(q, dict):
            continue
        line = lines[idx]
        cid = qids[(group["variable"], tuple(group["path"]), idx)]
        at = where(slug, group, idx)

        if "correct_override" in q:
            findings.add("B10", cid + "::B10",
                         "%s: correct_override=%r" % (at, q["correct_override"]), line)

        for label, unit in bc.sub_answer_units(q):
            val = unit.get("correct") if "_valid_letters" in unit else unit_correct_value(unit)
            sub = label or None
            sub_id = ("." + sub) if sub else ""
            sub_at = where(slug, group, idx, sub)
            if "_valid_letters" in unit:
                bad = is_empty_answer(val) or val not in unit["_valid_letters"]
            else:
                bad = is_empty_answer(val)
            if bad:
                findings.add("B1", cid + "::B1" + sub_id,
                             "%s: correct=%r" % (sub_at, val), line)
            pool = None if "_valid_letters" in unit else bc.option_pool(unit)
            if pool:
                seen = {}
                for v in pool:
                    seen[v] = seen.get(v, 0) + 1
                dupes = [v for v, c in seen.items() if c > 1]
                if dupes:
                    findings.add("B2", cid + "::B2" + sub_id,
                                 "%s: duplicate option(s): %s in %r" % (sub_at, dupes, pool), line)

        flagged = bc.flagged_option_texts_and_correct_count(q)
        if flagged:
            texts, n_correct = flagged
            if n_correct != 1:
                findings.add("B1", cid + "::B1",
                             "%s: %d option(s) marked correct (want exactly 1) in %r"
                             % (at, n_correct, texts), line)
            seen = {}
            for t in texts:
                seen[t] = seen.get(t, 0) + 1
            dupes = [t for t, c in seen.items() if c > 1]
            if dupes:
                findings.add("B2", cid + "::B2", "%s: duplicate option text: %s" % (at, dupes), line)

        for s in bc.all_strings(q):
            if not isinstance(s, str):
                continue
            for marker, pat in DRAFT_PATTERNS:
                if pat.search(s):
                    findings.add("B6", cid + "::B6", "%s: %r in %r" % (at, marker, s[:120]), line)
            m = bc.NO_SPACE_RUN.search(s)
            if m:
                findings.add("B7", cid + "::B7",
                             "%s: no-space run %r in %r" % (at, m.group(0), s[:120]), line)


def b11_allowlist():
    """{finding id: reason} for the deliberate form questions (group C): the
    question asks for one form, so a value-equal option in another form is the
    point of it."""
    with open(ALLOWLIST_PATH, "r", encoding="utf-8") as fh:
        entries = json.load(fh).get("b11_form_questions", [])
    return {e["id"]: e["reason"] for e in entries}


def lint_value_equal(slug, groups, findings, allowed, allowed_seen):
    """B11 -- two DISTINCT option strings in one answer unit that are equal in
    value (√50 beside 5√2: coordinate-geometry-dash:233, 28 Sep 2026). B2 sees
    only identical strings, and MaffsOptions.build() de-duplicates on
    String(value), so this shape was invisible to both. The parser is
    bank_common.parse_value()/equal(); an option it cannot read is never
    guessed at. The id is the question's content_id plus the sorted pair, so
    moving a question never changes its finding (todo item 7); where it sits
    goes in the detail."""
    qs = [(g, idx, q) for g in groups for idx, q in enumerate(g["questions"])
          if isinstance(q, dict)]
    cids = bc.content_ids(slug, [q for _g, _i, q in qs])
    for (g, idx, q), cid in zip(qs, cids):
        where = loc_string(slug, g, idx).split("::", 1)[1]
        for label, pool, correct in bc.option_units(q):
            for a, b in bc.value_equal_pairs(pool):
                eid = "%s::B11::%s" % (cid, json.dumps([a, b], ensure_ascii=False))
                if eid in allowed:
                    allowed_seen.add(eid)
                    continue
                key = "" if correct is None else str(correct)
                findings.add("B11", eid, "%s%s: %r = %r%s" % (
                    where, ("." + label) if label else "", a, b,
                    " (the marked answer is one of them)" if key in (a, b)
                    else " (both wrong options)" if correct is not None else ""))


# Below this length, a question's text field is a generic instruction label
# ("Find the determinant", "Find angle x", "y = kx"), not a scenario -- and
# most of this platform's games repeat their label across every question on
# purpose, distinguishing them by numbers stored elsewhere (a matrix, an
# angle, a coefficient) that vary per game and have no common field name.
# Comparing on the label alone found 699 "duplicates" that were really just
# two different matrices sharing an instruction; comparing label+correct+
# options instead found a second flood of coincidental matches (many
# questions legitimately share a small numeric answer or a generic 4-option
# set). The one signal this checker can trust across all 84 banks without
# per-game knowledge of where the real parameters live is prose long enough
# to be an actual scenario, not a label -- so that's what this checks.
MIN_SCENARIO_LEN = 30


def question_signature(q):
    """The text that makes two questions read as "the same" to a student --
    or None if this question's text field is too short to be a real scenario
    rather than a shared instruction label (see MIN_SCENARIO_LEN above).

    Long scenario text alone still isn't quite enough: shape-shifter reuses
    "Rotate 90 degrees clockwise about (0,0)" (32 chars, over the length
    gate) across many questions that differ only in which points get
    rotated -- not stored under any text field, so two DIFFERENT questions
    read as identical text. Requiring the correct answer to also match
    closes that gap without needing to know where each game keeps its
    numbers: two rotations of different shapes almost never land on the
    same answer coordinates by coincidence, but a genuine copy-paste
    duplicate matches on both.
    """
    text = bc.question_text(q)
    if not text or len(text.strip()) < MIN_SCENARIO_LEN:
        return None
    parts = [text]
    for _label, unit in bc.sub_answer_units(q):
        if "_valid_letters" not in unit:
            val = unit_correct_value(unit)
            parts.append(str(val))
    flagged = bc.flagged_option_texts_and_correct_count(q)
    if flagged:
        texts, _n = flagged
        parts.append("|".join(sorted(texts)))
    return " :: ".join(parts)


def lint_level_rules(slug, bank, findings, qids):
    """B3, B4 -- properties of a level's pool as a whole.

    A B3 finding is named after every copy in its group: the content hashes of
    all the level's questions with the same normalised signature, sorted. So
    moving, inserting above or swapping the copies leaves the name alone, and a
    group of three or more copies names the whole group: its findings (one per
    copy after the first, as before) share that one id and differ in detail.
    """
    for lv, info in bank.get("levels", {}).items():
        pool_qs = []
        for g in info["groups"]:
            if g.get("in_pool", True):
                for idx, q in enumerate(g["questions"]):
                    pool_qs.append((g, idx, q))

        if info["count"] < 40:
            findings.add("B4", "%s::%s" % (slug, lv),
                         "level %r has %d question(s), below the 40 minimum"
                         % (lv, info["count"]))

        sigs = []
        copies = {}
        for g, idx, q in pool_qs:
            if not isinstance(q, dict):
                continue
            sig = question_signature(q)
            if sig is None:
                continue
            norm = bc.normalise_for_dup_check(sig)
            cid = qids[(g["variable"], tuple(g["path"]), idx)]
            copies.setdefault(norm, []).append(cid.split("::", 1)[1])
            sigs.append((g, idx, sig, norm))

        def group_id(norm):
            return "%s::B3::%s" % (slug, "+".join(sorted(copies[norm])))

        seen_exact, seen_norm = {}, {}
        for g, idx, sig, norm in sigs:
            loc = loc_string(slug, g, idx)
            at = where(slug, g, idx)
            if sig in seen_exact:
                findings.add("B3", group_id(norm), "%s: exact duplicate of %s: %r"
                             % (at, seen_exact[sig], sig[:160]))
            else:
                seen_exact[sig] = loc
            if norm in seen_norm and seen_norm[norm] != seen_exact.get(sig):
                findings.add("B3", group_id(norm), "%s: normalised duplicate of %s: %r"
                             % (at, seen_norm[norm], sig[:160]))
            elif norm not in seen_norm:
                seen_norm[norm] = loc


SESSION_MIN_RE = re.compile(
    r"Math\.min\(\s*([A-Za-z_$][\w$]*)\s*,\s*[\w.$\[\]'\"]+\.length\s*\)")
BUTTON_ARRAY_RE = re.compile(r"\[\s*(\d{1,3}(?:\s*,\s*\d{1,3}){1,5})\s*\]")


def lint_session_length(slug, bank, src, findings):
    """B5 -- a static, best-effort check. Games on MaffsSession derive their
    offered lengths from the bank at runtime, so they cannot over-promise by
    construction; every known instance of this class (todo.md 1.11/1.13) was
    fixed onto that helper before this checker was built. This exists as a
    regression guard for a hand-rolled `Math.min(N, bank.length)` truncation
    reappearing, not as the primary way this run found violations.
    """
    if "MaffsSession" in src or "session-length.js" in src:
        return
    for m in SESSION_MIN_RE.finditer(src):
        window = src[max(0, m.start() - 400):m.start()]
        arr = None
        for am in BUTTON_ARRAY_RE.finditer(window):
            arr = am
        if not arr:
            continue
        offered = [int(x) for x in re.split(r"\s*,\s*", arr.group(1))]
        max_offered = max(offered)
        for lv, info in bank.get("levels", {}).items():
            if info["count"] and max_offered > info["count"]:
                findings.add("B5", "%s::%s" % (slug, lv),
                             "offers %d, level %r bank has %d"
                             % (max_offered, lv, info["count"]))


def lint_ast_rules(slug, tree, src, findings, known_names):
    """B8, B9. Named by what the code says, not where it sits. The text
    hashed is the parser's text (bank_common._shim_for_parser), because that
    is what the AST's ranges index into; its two rewrites change no line, so
    "line" stays true to the real file."""
    text = bc._shim_for_parser(src)
    for obj_node, dups in bc.find_duplicate_keys(tree):
        line = obj_node.loc.start.line
        lo, hi = obj_node.range
        findings.add("B8", "%s::B8::%s::%s::%s"
                     % (slug, bc.enclosing_name(tree, obj_node), ",".join(sorted(dups)),
                        sha12(text[lo:hi])),
                     "duplicate key(s) %s in object literal" % (dups,), line)
    for name, assign in bc.find_index_patches(tree):
        if name not in known_names:
            continue
        line = assign.loc.start.line
        target = text[assign.left.range[0]:assign.left.range[1]]
        rhs = text[assign.right.range[0]:assign.right.range[1]]
        findings.add("B9", "%s::B9::%s::%s" % (slug, target, sha12(rhs)),
                     "%s[...] = ... patches the bank literal after declaration" % name, line)


def lint_game(slug, findings, b11_allowed=None, b11_allowed_seen=None):
    bank = load_bank(slug)
    if bank is None:
        return "missing"
    if bank.get("generator"):
        return "generator"

    html_path = os.path.join(ROOT, "games", slug, "index.html")
    with open(html_path, "r", encoding="utf-8") as fh:
        html = fh.read()
    tree, src = bc.parse_game_source(html)

    groups = dedup_groups(bank)
    qids = question_ids(slug, groups)
    for g in groups:
        lint_question_level_rules(slug, g, findings, tree, qids)
    lint_value_equal(slug, groups, findings, b11_allowed or {},
                     b11_allowed_seen if b11_allowed_seen is not None else set())
    lint_level_rules(slug, bank, findings, qids)
    lint_katex_render(slug, bank.get("katex_renders") or [], findings)
    lint_mathtext(slug, bank.get("mathtext_hazards") or [], findings)
    if tree is not None:
        lint_session_length(slug, bank, src, findings)
        lint_ast_rules(slug, tree, src, findings, set(bank.get("variables", [])))
    return "linted"


# Fixture tests for bank_common.mathtext_delimiters_balanced -- B7's MaffsText
# balance check. True means "balanced, no finding"; False means "unbalanced,
# should be flagged".
MATHTEXT_BALANCE_FIXTURES = [
    (r"Find the angle between \(\mathbf{a}\) and \(\mathbf{b}\).", True,
     "two separate, correctly closed segments"),
    (r"Find \(\mathbf{a} + \mathbf{b}.", False,
     "opened, never closed"),
    (r"Find \mathbf{a} + \mathbf{b}\).", False,
     "closed with nothing open"),
    (r"Find \(f(x)\) at \(x = 2\).", True,
     "an ordinary '(' inside the segment is not a delimiter, only \\( and \\) are"),
]


# B7's KaTeX half, end to end (to-do §1.31): a game-shaped script and a bank;
# the site is found by behaviour and resolved per question; each resolved
# string is tested against the text KaTeX 0.16.9 renders for it through that
# callee. `expect` maps every string that must reach the site to True (a hit)
# or False; a string not in `expect` must NOT reach it. `rendered` is what the
# student sees, recorded from the real page by --selftest-live, which renders
# them again and fails if the recording has drifted.
_RK = ("function rk(el,tex){katex.render(tex,el,{throwOnError:false,displayMode:false})}\n"
       "function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));"
       "[a[i],a[j]]=[a[j],a[i]]}return a}\n")
_K = "function K(l,d){try{return katex.renderToString(l,{throwOnError:false,displayMode:!!d})}catch(e){return l}}\n"
B7_KATEX_FIXTURES = [
    {"why": "proof-builder's induction prompt, whole through rkStr (known positive, §1.30)",
     "script": "function rkStr(tex){const s=document.createElement('span');katex.render(tex,s,"
               "{throwOnError:false});return s.innerHTML}\n"
               "function renderInduction(stage){const p=document.createElement('div');"
               "p.innerHTML=rkStr(stage.prompt);}\n",
     "variable": "INDUCTION",
     "questions": [{"stages": [{"prompt": "What value of n should we use for the base case?"}],
                    "correct": "1"}],
     "expect": {"What value of n should we use for the base case?": True},
     "rendered": {"What value of n should we use for the base case?": "Whatvalueofnshouldweuseforthebasecase?"}},
    {"why": "test-the-claim's crExplanation through K(hint), hint a ternary (§1.32): one word, 'and', "
            "between maths; the other branch's prefix keeps its gap beside a colon",
     "script": _K + "const state={method:'cr'};function setMethod(m){state.method=m}\n"
               "function checkStep3(q){let hint=state.method==='cr'?q.crExplanation:('Expected: '+q.pValueExpr);"
               "return `<div>Incorrect. ${K(hint)}</div>`}\n",
     "variable": "QUESTIONS",
     "questions": [{"crExplanation": "P(X \\leq 0) = 0.0352 < 0.05 and P(X \\leq 1) = 0.1671 > 0.05",
                    "pValueExpr": "P(X \\leq 1) = 0.1671", "correct": "x"}],
     "expect": {"P(X \\leq 0) = 0.0352 < 0.05 and P(X \\leq 1) = 0.1671 > 0.05": True,
                "Expected: P(X \\leq 1) = 0.1671": False},
     "rendered": {"P(X \\leq 0) = 0.0352 < 0.05 and P(X \\leq 1) = 0.1671 > 0.05": "P(X \u2264 0) = 0.0352 < 0.05andP(X \u2264 1) = 0.1671 > 0.05", "Expected: P(X \\leq 1) = 0.1671": "Expected : P(X \u2264 1) = 0.1671"}},
    {"why": "component-crusher's PQ: a prompt with a LaTeX command and no \\( \\) goes whole to K() "
            "and 'Find' runs into the maths; one with \\( \\) goes through MaffsText and keeps its spaces",
     "script": _K + "function PQ(s){return(/\\\\[A-Za-z]/.test(s)&&!MaffsText.hasMaths(s))?K(s):MaffsText.html(s)}\n"
               "function showPart(sq){document.body.innerHTML=PQ(sq.prompt)}\n",
     "variable": "SCENARIOS",
     "questions": [{"sqs": [{"prompt": "Find \\mathbf{a} + \\mathbf{b}.", "correct": "x"},
                            {"prompt": "Find the angle between \\(\\mathbf{a}\\) and \\(\\mathbf{b}\\).",
                             "correct": "y"}], "correct": "z"}],
     "expect": {"Find \\mathbf{a} + \\mathbf{b}.": True,
                "Find the angle between \\(\\mathbf{a}\\) and \\(\\mathbf{b}\\).": False},
     "rendered": {"Find \\mathbf{a} + \\mathbf{b}.": "Finda + b.", "Find the angle between \\(\\mathbf{a}\\) and \\(\\mathbf{b}\\).": "Find the angle between a and b."}},
    {"why": "an option through rk() with no guard: 'Cannot tell' reaches KaTeX and loses its space; "
            "two-letter products in maths (mg, bx) are not words",
     "script": _RK + "function showQ(q){shuffle([q.correct,...q.d]).forEach(v=>{const b=document."
                     "createElement('button');rk(b,v)})}\n",
     "variable": "QUESTIONS",
     "questions": [{"correct": "F = \\mu mg", "d": ["Cannot tell", "y = e^{a + bx}"]}],
     "expect": {"Cannot tell": True, "F = \\mu mg": False, "y = e^{a + bx}": False},
     "rendered": {"F = \\mu mg": "F = \u03bcmg", "Cannot tell": "Cannottell", "y = e^{a + bx}": "y = ea+bx"}},
    {"why": "a guarded option (Jon's ruling 2): the plain one is shown as text, never rendered; "
            "the one with a backslash is rendered and loses its prose spaces",
     "script": _RK + "function showQ(q){shuffle([q.correct,...q.d]).forEach(v=>{const b=document."
                     "createElement('button');if(v.includes('\\\\')){rk(b,v)}else{b.textContent=v}})}\n",
     "variable": "QUESTIONS",
     "questions": [{"correct": "Only if r \\neq 0", "d": ["Cannot tell", "x \\neq 0"]}],
     "expect": {"Only if r \\neq 0": True, "x \\neq 0": False},
     "rendered": {"Only if r \\neq 0": "Onlyifr \ue020= 0", "x \\neq 0": "x \ue020= 0"}},
    {"why": "higher-power's \\text{} with braces inside it is text mode, not prose run together "
            "(the old regex's false positive)",
     "script": "function katexStr(s,d){return katex.renderToString(s,{throwOnError:false,displayMode:!!d})}\n"
               "function card(c){return '<div>'+katexStr(c.display)+'</div>'}\n",
     "variable": "ALL_BANKS",
     "questions": [{"display": "\\text{Primes under 1{,}000}", "correct": "168"}],
     "expect": {"\\text{Primes under 1{,}000}": False},
     "rendered": {"\\text{Primes under 1{,}000}": "Primes under 1,000"}},
    {"why": "a ternary with a prose prefix in one branch only: a hit on that branch, not the other",
     "script": _K + "let reveal=false;function toggle(){reveal=!reveal}\n"
               "function line(q){return K(reveal?q.expr:'Answer is '+q.expr)}\n",
     "variable": "QUESTIONS",
     "questions": [{"expr": "x + 1", "correct": "2"}],
     "expect": {"x + 1": False, "Answer is x + 1": True},
     "rendered": {"x + 1": "x + 1", "Answer is x + 1": "Answerisx + 1"}},
]


# The word-space test alone (bank_common.katex_lost_word_spaces), on renders
# recorded from KaTeX 0.16.9: (source, rendered, expected hit?, why).
B7_WORD_TEST_FIXTURES = [
    ("ABCD + ABC\\overline{D}", "ABCD + ABCD", False,
     "boolean-blitz: a word joined to a brace group renders joined; the space before it survives"),
    ("13 cm", "13cm", False, "a unit is out of scope for this rule"),
    ("Row 1: x = y", "Row1 : x = y", True, "eigenvector-engine: 'Row' runs into its number"),
]


def _fixture_bank(fx):
    return {"generator": False, "levels": {"default": {"groups": [
        {"variable": fx["variable"], "path": [], "questions": fx["questions"], "in_pool": True}]}}}


def b7_fixture_resolve(fx):
    """(wrappers, [(site, resolution)], {source: True}) for one fixture."""
    html = "<script>\n" + fx["script"] + "</script>"
    wrappers, sites = bc.katex_render_sites(html)
    resolved = [(st, bc.resolve_render_site(st, _fixture_bank(fx))) for st in sites]
    reached = {it["source"] for _st, r in resolved for it in r["items"].values() if "source" in it}
    return wrappers, resolved, reached


def b7_fixture_results(fx, rendered):
    """[(passed, message)] for one fixture, given what each source renders as."""
    _w, resolved, reached = b7_fixture_resolve(fx)
    out = []
    unres = [r["unresolved"] for _st, r in resolved if r["unresolved"]]
    out.append((not unres, "every site resolved%s" % (" (%s)" % unres[0] if unres else "")))
    out.append((reached == set(fx["expect"]),
                "reaches exactly %s%s" % (sorted(fx["expect"]),
                                          "" if reached == set(fx["expect"]) else ", got %s" % sorted(reached))))
    for src, want in fx["expect"].items():
        vis = rendered.get(src)
        got = bool(vis is not None and bc.katex_lost_word_spaces(src, vis))
        out.append((vis is not None and got == want,
                    "%s %r -> %r" % ("hit" if want else "not a hit", src, vis)))
    return out


def run_selftest():
    ok = True
    total_b7 = [0]
    for s, expected, why in MATHTEXT_BALANCE_FIXTURES:
        got = bc.mathtext_delimiters_balanced(s)
        print("%-4s expect=%-5s got=%-5s %-55r %s"
              % ("OK" if got == expected else "FAIL", expected, got, s, why))
        ok = ok and (got == expected)
    # B11: the value-equality parser (bank_common's shared fixtures, the scan's 38
    # plus the four false-positive shapes and the mixed-number product case).
    for a, b in bc.VALUE_FIXTURES_EQUAL:
        pa, pb = bc.parse_value(a), bc.parse_value(b)
        got = bool(pa and pb and bc.equal(pa, pb))
        print("%-4s expect=equal   %r = %r" % ("OK" if got else "FAIL", a, b))
        ok = ok and got
    for a, b in bc.VALUE_FIXTURES_UNEQUAL:
        pa, pb = bc.parse_value(a), bc.parse_value(b)
        got = not (pa and pb and bc.equal(pa, pb))
        print("%-4s expect=unequal %r, %r" % ("OK" if got else "FAIL", a, b))
        ok = ok and got
    for src, vis, want, why in B7_WORD_TEST_FIXTURES:
        got = bool(bc.katex_lost_word_spaces(src, vis))
        print("%-4s B7 word test: %r -> %r %s -- %s"
              % ("OK" if got == want else "FAIL", src, vis, "hit" if want else "not a hit", why))
        ok = ok and got == want
        total_b7[0] += 1
    for fx in B7_KATEX_FIXTURES:
        for got, msg in b7_fixture_results(fx, fx.get("rendered", {})):
            print("%-4s B7 KaTeX: %s -- %s" % ("OK" if got else "FAIL", msg, fx["why"][:60]))
            ok = ok and got
            total_b7[0] += 1
    for why, got in content_id_fixtures():
        print("%-4s content_id: %s" % ("OK" if got else "FAIL", why))
        ok = ok and got
    ledger_results = ledger_write_fixtures()
    for why, got in ledger_results:
        print("%-4s --write-ledger: %s" % ("OK" if got else "FAIL", why))
        ok = ok and got
    total = (total_b7[0] + len(MATHTEXT_BALANCE_FIXTURES)
             + len(bc.VALUE_FIXTURES_EQUAL) + len(bc.VALUE_FIXTURES_UNEQUAL)
             + len(content_id_fixtures()) + len(ledger_results))
    print("\n%s: %d fixture(s)" % ("ALL PASS" if ok else "FAILED", total))
    return ok


def content_id_fixtures():
    """[(why, passed)] for bank_common.content_id / content_ids."""
    q = {"sys": ["2x + y = 7", "x - y = 2"], "ask": "Find x", "correct": "3",
         "distractors": ["2", "4", "5"], "explanation": "Add the equations."}
    copy = json.loads(json.dumps(q))
    other_sys = dict(q, sys=["3x + 4y = 18", "x + 4y = 10"])
    other_exp = dict(q, explanation="Subtract the equations.")
    other_opt = dict(q, distractors=["2", "4", "6"])
    reordered = {k: q[k] for k in reversed(list(q))}
    ids = bc.content_ids("g", [q, other_sys, copy])
    h = bc.content_hash
    return [
        ("two byte-identical questions get #1 and #2",
         ids[0].endswith("#1") and ids[2].endswith("#2") and ids[0][:-2] == ids[2][:-2]),
        ("a question differing only in its sys field gets a different hash "
         "(simultaneous-solver's 'Find x' shape)", h(q) != h(other_sys) and ids[1].endswith("#1")),
        ("a question differing only in its explanation gets a different hash", h(q) != h(other_exp)),
        ("a question differing in one option gets a different hash", h(q) != h(other_opt)),
        ("key order in the object does not change the hash",
         list(reordered) != list(q) and h(q) == h(reordered)),
        ("the id is slug::<12 hex>#<ordinal>",
         re.fullmatch(r"g::[0-9a-f]{12}#1", bc.content_id("g", q, 1)) is not None),
    ]


def ledger_write_fixtures():
    """[(why, passed)] for --write-ledger's merge (to-do §4 item 10), on a
    temporary ledger and a temporary banks dir, never the real ones. Two real
    game slugs give lint_game a real source file; their banks are synthetic."""
    import contextlib
    import io
    import shutil
    import tempfile
    global BANKS_DIR
    a, b = "matrix-crunch", "index-laws"

    def bank(slug, generator=False):
        q = {"q": "Fixture question for " + slug, "correct": "1", "d": ["2", "3", "4"]}
        return {"slug": slug, "generator": generator, "read_method": "live", "variables": [],
                "levels": {} if generator else {"all": {"count": 1, "groups": [
                    {"variable": "FIXTURE", "path": [], "questions": [q], "count": 1,
                     "marking": None, "in_pool": True}]}},
                "katex_hazards": [], "mathtext_hazards": []}

    def record(generator, entries):
        rules = {r: {"status": "pass", "entries": []} for r in RULE_NAMES}
        rules["B4"] = {"status": "fail" if entries else "pass", "entries": entries}
        return {"layers": {"A": "violations" if entries else "verified", "B": "none",
                           "C": "none", "D": "none", "E": "none"},
                "generator": generator, "rules": rules}

    withdrawn = record(False, [{"id": "gone::core", "detail": "fixture", "line": None}] * 3)
    known_b = record(False, [{"id": b + "::all", "detail": "fixture", "line": 7}])
    true_gen = record(True, [])
    tmp = tempfile.mkdtemp()
    saved = BANKS_DIR
    results = []

    def run(old, banks, roster, only=None):
        """Write `old`, lay out `banks`, lint `roster` (or `only`), write the
        ledger; return (exit code, old text, new text, ledger)."""
        for f in os.listdir(tmp):
            os.remove(os.path.join(tmp, f))
        for slug, bk in banks.items():
            with open(os.path.join(tmp, slug + ".json"), "w", encoding="utf-8") as fh:
                json.dump(bk, fh)
        path = os.path.join(tmp, "ledger.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(old, fh, indent=1, ensure_ascii=False, sort_keys=True)
        with open(path, encoding="utf-8") as fh:
            before = fh.read()
        fbg = {}
        for slug in [s for s in roster if not only or only in s]:
            f = Findings()
            fbg[slug] = (lint_game(slug, f, {}, set()), f)
        with contextlib.redirect_stdout(io.StringIO()):
            code = write_ledger(path, fbg, roster, only)
        with open(path, encoding="utf-8") as fh:
            after = fh.read()
        return code, before, after, json.loads(after)

    try:
        BANKS_DIR = tmp
        code, _b, _a, led = run({"gone": withdrawn, a: record(False, [])}, {a: bank(a)}, [a])
        results.append(("a withdrawn game's 3 entries survive a full write, byte for byte",
                        code == 0 and led.get("gone") == withdrawn and a in led))
        code, _b, _a, led = run({a: record(False, []), b: known_b},
                                {a: bank(a), b: bank(b)}, [a, b], only=a)
        results.append(("--only=%s leaves %s's record unchanged" % (a, b),
                        code == 0 and led.get(b) == known_b))
        code, _b, _a, led = run({a: record(False, []), b: true_gen}, {a: bank(a)}, [a, b])
        results.append(("a missing bank (a true generator) is carried, not dropped",
                        code == 0 and led.get(b) == true_gen))
        code, before, after, _l = run({a: record(False, []), b: known_b}, {a: bank(a)}, [a, b])
        results.append(("a missing bank the ledger knows as read: exit 1, nothing written",
                        code == 1 and before == after))
        code, before, after, _l = run({a: record(False, []), b: known_b},
                                      {a: bank(a), b: bank(b, generator=True)}, [a, b])
        results.append(("a lost KaTeX bank (extracts as a generator): exit 1, nothing written",
                        code == 1 and before == after))
    finally:
        BANKS_DIR = saved
        shutil.rmtree(tmp, ignore_errors=True)
    return results


# Fixture tests for B7's MaffsText throw check (bank_common.MATHTEXT_THROW_JS)
# -- needs a real KaTeX engine, so unlike the two fixture sets above this
# only runs under --selftest-live, which spins up the same local stub server
# and headless Chromium extract-banks.py itself uses.
MATHTEXT_THROW_FIXTURES = [
    (r"x^2 + 1", False, "valid LaTeX, must not throw"),
    (r"\frac{1}{2}", False, "valid LaTeX, must not throw"),
    (r"\notarealcommand{x}", True, "unknown control sequence, must throw"),
    (r"\mathbf{a", True, "unbalanced brace inside the segment, must throw"),
]


def _extract_banks_module():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "extract_banks", os.path.join(os.path.dirname(os.path.abspath(__file__)), "extract-banks.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


async def _b7_fixtures_live(context, base):
    """Render every B7 KaTeX fixture through its own callee in a real page
    (KaTeX from the CDN the games load, MaffsText from schools/assets) and
    check the hits, and that the recorded `rendered` text has not drifted."""
    eb = _extract_banks_module()
    ok, n = True, 0
    for i, fx in enumerate(B7_KATEX_FIXTURES):
        url = base + "/__b7_fixture_%d.html" % i
        html = ("<!doctype html><html><head><meta charset='utf-8'>"
                "<script src='https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js'></script>"
                "<script src='/schools/assets/mathtext.js'></script></head><body><script>\n"
                + fx["script"] + "</script></body></html>")

        async def serve(route, request=None, html=html):
            await route.fulfill(status=200, content_type="text/html", body=html)
        await context.route(url, serve)
        wrappers, resolved, _reached = b7_fixture_resolve(fx)
        renders, failures = await eb.render_sites(context, url, wrappers, resolved, 20000)
        live = {r["source"]: r["rendered"] for r in renders if not r.get("error")}
        for got, msg in b7_fixture_results(fx, live):
            print("%-4s B7 KaTeX (live): %s" % ("OK" if got else "FAIL", msg))
            ok, n = ok and got, n + 1
        for src, vis in sorted(live.items()):
            same = fx.get("rendered", {}).get(src) == vis
            print("%-4s B7 KaTeX (live): recorded render of %r matches" % ("OK" if same else "FAIL", src))
            ok, n = ok and same, n + 1
        if failures:
            print("FAIL B7 KaTeX (live): %s" % failures)
            ok = False
    return ok, n


async def _run_selftest_live_async():
    from playwright.async_api import async_playwright

    server, base = bc.start_stub_server()
    ok = True
    try:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            context = await browser.new_context()
            b7_ok, b7_n = await _b7_fixtures_live(context, base)
            ok = ok and b7_ok
            page = await context.new_page()
            # component-crusher loads KaTeX and nothing about this check is
            # game-specific -- any page that loads the same CDN katex.min.js
            # would do.
            await page.goto(base + "/games/component-crusher/",
                             wait_until="load", timeout=20000)
            await page.wait_for_timeout(200)
            segs = [s for s, _, _ in MATHTEXT_THROW_FIXTURES]
            results = await page.evaluate(bc.MATHTEXT_THROW_JS, segs)
            for (s, expect_throw, why), r in zip(MATHTEXT_THROW_FIXTURES, results):
                got_throw = r is not None
                print("%-4s expect_throw=%-5s got_throw=%-5s %-30r %s"
                      % ("OK" if got_throw == expect_throw else "FAIL",
                         expect_throw, got_throw, s, why))
                ok = ok and (got_throw == expect_throw)
            await browser.close()
    finally:
        server.terminate()
    print("\n%s: %d live fixture(s)" % ("ALL PASS" if ok else "FAILED", len(MATHTEXT_THROW_FIXTURES) + b7_n))
    return ok


def run_selftest_live():
    import asyncio
    return asyncio.run(_run_selftest_live_async())


def lint_katex_render(slug, renders, findings):
    """B7's KaTeX half, rebuilt 2 Oct 2026 (to-do §1.31). extract-banks.py found
    every KaTeX render site by behaviour, rebuilt per question the strings that
    reach each one, and rendered them in the page through the site's own callee
    (bank_common, "B7's KaTeX half: render sites found by behaviour"). A string
    is a hit when a space it has in the source, between two tokens, is missing
    from what the student sees and one of those tokens is a word
    (bank_common.katex_lost_word_spaces: 3+ letters, or a 2-letter English
    function word; units are out of scope). One finding per distinct (bank
    path, string), however many sites or question states render it; any one
    losing a space is a hit. The id is the bank path and the string's SHA-1;
    the ordinal is 1 by construction and keeps the shape the MaffsText half
    uses."""
    hits = {}
    for r in renders:
        if r.get("error") or r.get("rendered") is None or not r.get("source"):
            continue
        lost = bc.katex_lost_word_spaces(r["source"], r["rendered"])
        if not lost:
            continue
        h = hits.setdefault((r["path"], r["source"]), {"r": r, "sites": set(), "lost": set()})
        h["sites"].add("%s:%d" % (r["callee"], r["line"]))
        h["lost"].update(lost)
    for (path, source), h in sorted(hits.items()):
        r = h["r"]
        findings.add("B7", "%s::B7::katex[%s]::%s#1" % (slug, path, sha12(source)),
                     "%s at %s: %r renders as %r (lost a space beside: %s)"
                     % (path, ", ".join(sorted(h["sites"])), source[:120],
                        (r["rendered"] or "")[:120], ", ".join(sorted(h["lost"]))[:80]),
                     r["line"])


def lint_mathtext(slug, mathtext_hazards, findings):
    """B7's MaffsText half (28 Sep, mathtext contract): a bank string
    authored with \\( \\) (schools/assets/mathtext.js's convention) that
    MaffsText.html() will mis-render -- either the delimiters don't balance
    (bank_common.mathtext_delimiters_balanced), so the split lands on the
    wrong boundary, or a \\( \\) segment is LaTeX KaTeX can't parse at all,
    caught by rendering it live with throwOnError:true (extract-banks.py's
    render_mathtext_throw_check) even though the runtime's own
    throwOnError:false would hide it behind a red error span rather than
    breaking the page. Both are authoring mistakes in the maths itself, not
    in whether the game passes the field to K() -- \\( never occurs by
    accident, so every hit here is scanned platform-wide, not field-scoped.
    Named, like the KaTeX half, by the string's SHA-1 plus an ordinal over
    identical strings of the same kind.
    """
    seen = {}
    for hz in mathtext_hazards:
        kind = "balance" if hz["kind"] == "unbalanced" else "throws"
        key = "mathtext[%s]::%s" % (kind, sha12(hz["original"]))
        seen[key] = seen.get(key, 0) + 1
        eid = "%s::B7::%s#%d" % (slug, key, seen[key])
        if hz["kind"] == "unbalanced":
            findings.add("B7", eid,
                         "%r has unbalanced \\( \\) delimiters" % (hz["original"][:120],))
        else:
            findings.add("B7", eid,
                         "segment %r (from %r) fails to render: %s"
                         % (hz["segment"][:80], hz["original"][:80], hz["error"][:120]))


def print_render_sites(slugs):
    """B7's KaTeX half, informational (never a failure): render sites whose
    strings cannot be rebuilt from the bank and rendered, and sites fed only by
    what a generator builds as the game runs (Jon's ruling, 2 Oct 2026; the
    candidate for those is a runtime KaTeX hook layer, to-do §4)."""
    unresolved, runtime_only = [], []
    for slug in slugs:
        bank = load_bank(slug)
        if not bank:
            continue
        for u in bank.get("katex_unresolved") or []:
            unresolved.append("unresolved: %s %s :%s %s" % (slug, u["callee"], u["line"], u["reason"]))
        for u in bank.get("katex_runtime_only") or []:
            runtime_only.append("runtime-only: %s %s :%s" % (slug, u["callee"], u["line"]))
    print("\nB7 KaTeX render sites, informational: %d unresolved, %d runtime-only"
          % (len(unresolved), len(runtime_only)))
    for line in unresolved + runtime_only:
        print("  " + line)


def build_ledger(findings_by_game):
    ledger = {}
    for slug, (status, findings) in findings_by_game.items():
        rules = {}
        any_violation = False
        for rule in RULE_NAMES:
            entries = findings.by_rule[rule] if findings else []
            rules[rule] = {"status": "fail" if entries else "pass", "entries": entries}
            if entries:
                any_violation = True
        ledger[slug] = {
            "layers": {
                "A": "violations" if any_violation else "verified",
                "B": "none", "C": "none", "D": "none", "E": "none",
            },
            "generator": status == "generator",
            "rules": rules,
        }
    return ledger


def count_entries(record):
    return sum(len(r.get("entries", [])) for r in record.get("rules", {}).values())


def merge_ledger(old_ledger, findings_by_game, roster, only=None):
    """What --write-ledger writes: the old ledger, with only the games this run
    actually read replaced (to-do §4 item 10, 2 Oct 2026). Rebuilding from this
    run alone treated "not read" as clean or as gone: a withdrawn game's entries
    vanished (regression-rumble's three B4, copied back by hand in PRs 51 and 52),
    --only wrote a ledger of one game, and a bank that did not extract was written
    as "pass", its tracked defects cleared as if fixed.

    Returns (merged, carried, refused, not_written):
      merged       the ledger to write (ignore it when `refused` is non-empty)
      carried      [(slug, reason, entry count)], each kept byte for byte
      refused      [(slug, reason)]: a bank the old ledger knows as read
                   (generator: false) that this run did not read; nothing may be
                   written, because a partial extraction is never the basis of a
                   full ledger write
      not_written  [(slug, reason)]: a game new to the ledger that did not read
    """
    fresh = build_ledger(findings_by_game)
    roster = set(roster)
    merged, carried, refused, not_written = {}, [], [], []
    for slug, (status, _f) in findings_by_game.items():
        old = old_ledger.get(slug)
        if status == "linted" or (status == "generator" and old is not None
                                   and old.get("generator") is True):
            merged[slug] = fresh[slug]
            continue
        reason = "bank missing" if status == "missing" else "bank not read"
        if old is None:
            not_written.append((slug, reason))
            continue
        if old.get("generator") is False:
            refused.append((slug, reason))
        merged[slug] = old
        carried.append((slug, reason, count_entries(old)))
    for slug, old in old_ledger.items():
        if slug in findings_by_game:
            continue
        reason = "not selected by --only" if (only and slug in roster) else "withdrawn/off-roster"
        merged[slug] = old
        carried.append((slug, reason, count_entries(old)))
    return merged, carried, refused, not_written


def write_ledger(path, findings_by_game, roster, only=None):
    """Merge over the ledger at `path` and write it, unless refused. Prints what
    was carried. Returns 0 on a write, 1 on a refusal."""
    old_ledger = {}
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as fh:
            old_ledger = json.load(fh)
    merged, carried, refused, not_written = merge_ledger(old_ledger, findings_by_game,
                                                         roster, only)
    for slug, reason in not_written:
        print("NOT WRITTEN (new to the ledger, %s): %s" % (reason, slug))
    if refused:
        print("\nREFUSED to write %s: the ledger knows these as read banks, and this run "
              "did not read them (see docs/sandbox-checks.md):" % path)
        for slug, reason in refused:
            print("  %s (%s)" % (slug, reason))
        return 1
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(merged, fh, indent=1, ensure_ascii=False, sort_keys=True)
    print("\nWrote %s (%d games)" % (path, len(merged)))
    for slug, reason, n in sorted(carried):
        print("  carried %s (%s), %d entr%s" % (slug, reason, n, "y" if n == 1 else "ies"))
    print("carried %d game(s), %d entries unchanged"
          % (len(carried), sum(n for _s, _r, n in carried)))
    return 0


def diff_against_ledger(ledger, old_ledger):
    """(new_violations, resolved_but_not_cleared) -- CI's two failure modes."""
    new_v, stale = [], []
    for slug, game in ledger.items():
        old_game = old_ledger.get(slug, {})
        old_rules = old_game.get("rules", {})
        for rule, info in game["rules"].items():
            old_ids = {e["id"] for e in old_rules.get(rule, {}).get("entries", [])}
            new_ids = {e["id"] for e in info["entries"]}
            for eid in new_ids - old_ids:
                new_v.append((slug, rule, eid))
            for eid in old_ids - new_ids:
                stale.append((slug, rule, eid))
    # A slug the ledger tracked that no longer appears in this run at all
    # (deleted game, or a bug in this run) is handled by the caller via the
    # SUCCESS CONDITION check, not here.
    return new_v, stale


def main():
    ap = argparse.ArgumentParser(description="Lint every extracted bank (checker tier 4, layer A).")
    ap.add_argument("--only", help="substring filter on slug")
    ap.add_argument("--write-ledger", action="store_true", help="write data/check-ledger.json")
    ap.add_argument("--ci", action="store_true",
                    help="fail only on a NEW violation, or a ledger entry that no longer reproduces")
    ap.add_argument("--selftest", action="store_true",
                    help="run the B7 KaTeX-prose/mathtext-balance fixture tests and exit (no bank data, no browser)")
    ap.add_argument("--selftest-live", action="store_true",
                    help="run the B7 MaffsText throw-check fixture tests and exit (spins up a browser)")
    args = ap.parse_args()

    if args.selftest:
        return 0 if run_selftest() else 1
    if args.selftest_live:
        return 0 if run_selftest_live() else 1

    slugs = [s for s in roster_slugs() if not args.only or args.only in s]
    findings_by_game = {}
    totals = {r: 0 for r in RULE_NAMES}
    b11_allowed = b11_allowlist()
    b11_allowed_seen = set()

    for slug in slugs:
        f = Findings()
        status = lint_game(slug, f, b11_allowed, b11_allowed_seen)
        findings_by_game[slug] = (status, f)
        for r in RULE_NAMES:
            totals[r] += len(f.by_rule[r])

    print("%d games checked (%d generator, %d linted, %d missing extraction)"
          % (len(slugs),
             sum(1 for s, _ in findings_by_game.values() if s == "generator"),
             sum(1 for s, _ in findings_by_game.values() if s == "linted"),
             sum(1 for s, _ in findings_by_game.values() if s == "missing")))
    print()
    print("%-4s %-42s %5s" % ("ID", "rule", "hits"))
    over_cap = []
    for r in RULE_NAMES:
        print("%-4s %-42s %5d" % (r, RULE_NAMES[r], totals[r]))
        if totals[r] > RULE_MAX_BY_RULE.get(r, RULE_MAX):
            over_cap.append(r)

    if over_cap:
        print("\nSTOP: %s produced more hits than its cap (%s) -- report before recording, "
              "it may be mis-specified rather than a real defect count."
              % (over_cap, ", ".join("%s %d" % (r, RULE_MAX_BY_RULE.get(r, RULE_MAX))
                                     for r in over_cap)))
        return 2

    print_render_sites(slugs)

    ledger = build_ledger(findings_by_game)

    missing_slugs = [s for s, (status, _) in findings_by_game.items() if status == "missing"]
    if missing_slugs:
        print("\nMISSING from data/banks/ (extract-banks.py has not been run for these):")
        for s in missing_slugs:
            print("  " + s)

    if args.write_ledger:
        if write_ledger(LEDGER_PATH, findings_by_game, roster_slugs(), args.only) != 0:
            return 1

    if args.ci:
        if not os.path.exists(LEDGER_PATH):
            print("\nFAIL: no ledger at %s to compare against -- run with --write-ledger first."
                  % LEDGER_PATH)
            return 1
        with open(LEDGER_PATH, "r", encoding="utf-8") as fh:
            old_ledger = json.load(fh)
        new_v, stale = diff_against_ledger(ledger, old_ledger)
        print("\n%d game(s) in this run, %d in the ledger" % (len(ledger), len(old_ledger)))
        not_run = sorted(s for s in old_ledger if s not in ledger)
        if not_run:
            print("In the ledger, not in this run (kept, not checked): %s" % ", ".join(not_run))
        if new_v:
            print("NEW violation(s) not in the ledger:")
            for slug, rule, eid in new_v:
                print("  %-4s %s" % (rule, eid))
        if stale:
            print("STALE ledger entry/entries (fixed, but not cleared from the ledger):")
            for slug, rule, eid in stale:
                print("  %-4s %s" % (rule, eid))
        # A bank the ledger knows as linted that extracted as a generator this run
        # was not read (the KaTeX CDN unreachable, say): every rule would see an
        # empty bank and could pass quietly. Fail and name it.
        lost = [s for s, (status, _f) in findings_by_game.items()
                if status == "generator" and old_ledger.get(s, {}).get("generator") is False]
        if lost:
            print("BANK NOT READ this run, though the ledger knows it as a linted bank "
                  "(was the page's CDN reachable? see docs/sandbox-checks.md):")
            for s in lost:
                print("  " + s)
        # A form-question entry that no longer matches anything: the question
        # changed, so its reason may no longer hold. Re-read it and re-record it.
        unused = sorted(e for e in b11_allowed
                        if e.split("::", 1)[0] in findings_by_game and e not in b11_allowed_seen)
        if unused:
            print("UNUSED b11_form_questions entr(y/ies) in checker-allowlist.json "
                  "(the question changed; re-read it):")
            for e in unused:
                print("  " + e)
        if new_v or stale or lost or unused:
            extra = "".join([", %d bank(s) not read" % len(lost) if lost else "",
                             ", %d unused allowlist" % len(unused) if unused else ""])
            print("\nFAILED - %d new, %d stale%s" % (len(new_v), len(stale), extra))
            return 1
        print("\nOK - matches the ledger exactly")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
