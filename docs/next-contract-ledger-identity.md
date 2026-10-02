# Contract: ledger identity by content for B1–B10 (to-do item 7)

Status: **DONE, PR 52, 2 Oct 2026 (cloud session).** Issued by Jon, 2 Oct 2026, and held for a fresh
session. Its precondition was met: B11 merged (PR 51) and `content_id()` is in `scripts/bank_common.py`.

## Jon's rulings during the build (2 Oct 2026)

The contract below is amended where these rulings changed it. Each amendment is marked
**[Amended 2 Oct]**.

1. **regression-rumble's three B4 entries are copied across unchanged**, as PR 51 did (canon §11.5),
   because `--write-ledger` drops withdrawn games. Making `--write-ledger` carry such entries forward
   is to-do §4 item 10 and is not part of this contract.
2. **B3 is named after every copy, sorted by `content_id()`.** As drafted, EXACT CHANGE 2 rested on a
   false premise: B3 compares normalised scenario text plus the answer, not whole questions, so the
   later copy's ordinal is usually 1, not "2 or more". A name taken from the later copy alone also
   flips when the copies swap. A movement proof for swapping two copies was added.
3. **B7's KaTeX and MaffsText halves get content ids from their strings.** The ROOT CAUSE below is
   true of only one of B7's three halves. The other two were named `slug::katex[field][i]` and
   `slug::mathtext[kind][i]`, where `i` is a position in a hazard list carrying no question.
   `extract-banks.py` stays untouched, because the string's identity is its content.
4. **B8's enclosing name, in this order: the innermost named function, then the enclosing top-level
   variable, then `(top level)`. B8 and B9 hash the parser's text** (the text the AST's ranges
   index into). Two consequences are documented: renaming the enclosing function or variable changes
   a B8 id (new + stale in CI, expected), and changing either syntax rewrite in
   `bank_common._shim_for_parser` changes every B8/B9 id at once.

## Before you start (notes added by Claude Code at home, 2 Oct 2026; not part of the contract)

1. **The cloud sandbox cannot read three banks.** `cdn.jsdelivr.net` is refused there
   (`docs/sandbox-checks.md`), so `extract-banks.py` records `differentiation-duel`, `index-laws` and
   `integration-duel` as generators with empty banks. Since PR 51, `check-banks.py --ci` FAILS on that
   ("BANK NOT READ"), and `--write-ledger` on such an extraction would silently delete those games'
   entries. **Never run `--write-ledger` on an extraction where any of the three is not `live`.** Either
   serve KaTeX locally to the extractor (`docs/sandbox-checks.md` step 1 gives the files; the extractor
   does not route requests, so it needs a wrapper that adds a `context.route` for
   `https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/**` and fulfils from the local copy, without editing
   `extract-banks.py`), or check the extraction summary says "82 bank (live), 1 bank (static fallback),
   13 generator" before trusting anything.
2. **Withdrawn regression-rumble trap.** The ledger holds 3 B4 entries for `regression-rumble` (core,
   alevel, level4), which is withdrawn and off the roster, so no run produces them. That is why B4 is
   104 in the ledger but 101 in a run. `--write-ledger` rebuilds the ledger from the roster and **drops
   those 3**, which this contract's STOP IF ("any old entry maps to zero ... new entries") would catch.
   PR 51 avoided it by generating B11 entries with `--write-ledger` and merging only those into the old
   ledger. Decide before migrating (carry the 3 over unchanged, or ask Jon), and say which in the PR.
3. **`--write-ledger` also refreshes drifted `line` fields** (expected-damage, formula-unlocked,
   maths-court, matrix-crunch, probability-paradox, terrible-advice, wrong-on-the-internet differ only
   in `line` today). That is expected once ids no longer use lines, but report it.
4. Counts on `main` after PR 51 (ledger): B1 0, B2 2, B3 4, B4 104 (101 live + 3 withdrawn), B5 0,
   B6 19, B7 0, B8 0, B9 0, B10 1, B11 111.
5. Useful from PR 51: `bank_common.content_ids(slug, questions)` numbers a whole game in bank order;
   B11's id format is `content_id + "::B11::" + json.dumps(sorted pair)`; the bank order used is
   `check-banks.py`'s `dedup_groups()`.

## The contract, verbatim

TASK: Identify every check-banks.py finding (B1–B10) by content rather than by bank index or source line, so a known defect keeps its ledger match when the code around it moves.

ROOT CAUSE: diff_against_ledger() in scripts/check-banks.py matches ledger entries on id alone. B1, B2, B3, B6, B7 and B10 build that id with loc_string(), which is the bank index (e.g. binomial-blaster::QUESTIONS.alevel2[36]); B8 and B9 use the source line (slug::line527). Insert a question above a known defect, or a line above a B8/B9 hit, and the unchanged defect shows up as one "new" violation plus one "stale" one: CI fails on a defect it already tracks. That happened on 28 Sep, when the OpenDyslexic change moved test-the-claim's B8 entry from line 527 to 526. B4 and B5 (slug::level) are already content-stable.

CLASS CHECK: Yes, a class. Eight rules share one weakness, and it lives in shared infrastructure: the id scheme and the one function that matches ledger entries. The fix is to change the id scheme once, at the layer that builds ids, reusing content_id() from bank_common.py (added by B11). Hand-editing ledger entries whenever a line moves is the defensive patch this replaces.

EXACT CHANGE:
1. B1, B2, B6, B7, B10 (per-question rules): id = content_id(slug, q, ordinal) + "::" + rule, plus "." + sub-answer label where the rule reports per sub-answer (as loc_string's sub does now). The bank path and index move into the detail field. **[Amended 2 Oct]** B7's two halves that carry no question are named by their string: the KaTeX half `slug::B7::katex[<fields>]::<first 12 hex of the SHA-1 of the original string>#<ordinal>`, and the MaffsText half `slug::B7::mathtext[<kind>]::<first 12 hex of the SHA-1 of the original string>#<ordinal>`, where `<kind>` is `balance` or `throws`. The ordinal counts identical strings within the same half and field or kind.
2. **[Amended 2 Oct]** B3 (duplicates): id = slug + "::B3::" + the content hashes (content_id without its slug) of every copy in the level's group (the questions sharing one normalised signature), sorted and joined by "+". A group of three or more copies has one name: its findings (one per copy after the first, as before) share that id and differ in detail. The detail leads with the finding's own bank path and names the first copy by bank path, for a human reader.
3. B8 (duplicate object keys): id = slug + "::B8::" + the enclosing function or variable name (the same convention checker-allowlist.json uses) + "::" + the sorted duplicate key names + "::" + the first 12 hex of the SHA-1 of the object literal's source text. Line goes in "line" only.
4. B9 (index patches): id = slug + "::B9::" + the patched name and its index expression as written (e.g. QUESTIONS[12]) + "::" + the first 12 hex of the SHA-1 of the right-hand side's source text.
5. B4, B5, B11: unchanged.
6. Migrate data/check-ledger.json by re-running --write-ledger on unchanged main. No entry may be added or dropped by the migration.
7. Docs: CLAUDE.md "Tier 4, layer A" gains one paragraph stating that findings are identified by content and why (the 28 Sep B8 incident); docs/checker-tier4-design.md updated to match; to-do item 7 struck through with the PR number.

DO NOT TOUCH:
- What any rule detects: B1–B11 must find exactly the same defects before and after.
- diff_against_ledger()'s logic (it already matches on id; only the ids change).
- B4, B5, B11 ids.
- Any game file; schools/assets/options.js; scripts/extract-banks.py; the CI workflow; checker-allowlist.json.

SUCCESS CONDITION:
1. The migration is one-to-one: every old ledger entry maps to exactly one new entry with the same rule and the same defect, and the per-rule counts are unchanged (as of B11's merge; at the time of drafting, B2 2, B3 4, B4 104, B6 19, B10 1, B1/B5/B7/B8/B9 0, plus B11 95). Put the old-id → new-id mapping table in the PR description.
2. check-banks.py --selftest passes; --ci green on main.
3. Movement proof, each run locally on main and reverted afterwards: (a) insert a new valid question at the top of a level array holding a ledgered B6 entry: --ci reports the new question's own findings only, never "new + stale" for the known B6; (b) insert a blank line at the top of a game file holding a ledgered entry: --ci unchanged; (c) for B8/B9, which hold no ledger entries today, re-create the 28 Sep case in a scratch copy (a duplicated key, then a line inserted above it) and show its id does not change; **[Amended 2 Oct]** (d) swap two B3 copies in a scratch copy: the name must not change; (e) for each B7 half, add a hazard and then one that sorts before it: the first hazard's id must not change.
4. Detection proof: reintroduce one real defect per rule family (one per-question rule, B3, B8, B9; **[Amended 2 Oct]** and one per B7 half, KaTeX and MaffsText) and confirm --ci fails on it as a new violation, then revert.
5. CI green on the PR; merge on green.
6. Handover: docs/todo.md START block rewritten (previous handover moved word for word to "Done — full history"), with NEXT: Contract 2 (group B wording, awaiting Jon), then phone-fit batch 2. Everything committed.

STOP IF:
- The migration changes any per-rule count, or any old entry maps to zero or to two new entries.
- Two non-identical questions, or two distinct B8/B9 sites, produce the same id.
- Any rule finds a different set of defects from before.
- B11 has not merged, or content_id() is not in bank_common.py when the work starts.

(Note on success condition 1: "plus B11 95" was drafted before Jon's 2 Oct group C rulings. B11 is
111 in the ledger after PR 51: A 1 + B 68 + D 42.)
