#!/usr/bin/env python3
"""Phase 1 of the search-titles contract: write docs/seo-titles-draft.md from data/games.json.

    python scripts/draft-seo-titles.py

Reads data/games.json and the roster's Levels column, generates every title and description by
the rules the draft states, checks the limits (title <= 60, description <= 155, no duplicate
titles, slugs equal the roster's numbered rows) and writes the review table. Exit 1, nothing
written, on any breach. Phase 2's apply-meta.py takes over these rules; this script goes then.
"""
import html, json, re, sys

ROSTER = ".claude/rules/game-roster.md"
TITLE_MAX, DESC_MAX = 60, 155

# roster label (lower case) -> teacher word; order is the order words appear in a title
LEVEL_WORDS = [
    ("year 6", "Year 6"), ("ks3", "KS3"), ("gcse", "GCSE"), ("a-level", "A-Level"),
    ("a-level year 2", "A-Level"), ("l3", "Level 3"), ("l4", "Level 4"),
    ("further", "Further Maths"), ("core", "Core Maths"),
]
ORDER = ["Year 6", "KS3", "GCSE", "A-Level", "Level 3", "Level 4", "Further Maths", "Core Maths"]

PHRASE_NEEDED = "PHRASE NEEDED"


# Where a game's phrase is NOT drawn from its spec-map row, or is otherwise my call: shown in the draft.
NOTES = {
    "truth-buster": "STOP IF: no spec-map reference (a ruled exception, check-spec-mapping.py). Suggestion: **Always, Sometimes or Never True**, the name teachers use for this task type.",
    "just-pythag-it-bruv": "STOP IF: no spec-map reference (unlisted, noindex). Suggestion: **Pythagoras' Theorem** (G20). Its only roster level is KS3 (shown as Foundation, SR-11), so the title would say KS3 on a resit game.",
    "estimation-engine": "In games.json, NOT applied until its rebuild merges (item 6).",
    "equatle": "Spec ref is N1 'number reasoning'; the phrase names the format teachers search for.",
    "52dle": "Spec ref is N1 'number reasoning'; no topic phrase fits a daily puzzle better.",
    "prisoners-dilemma": "Spec ref is Core §3.10 cost-benefit analysis; the phrase is the game's own name because it is what is searched.",
    "core-maths-paper1": "Exam-paper phrase, not a spec topic: teachers search for the paper. The topics are in the description.",
    "core-maths-paper2a": "As paper 1.",
    "core-maths-paper2b": "As paper 1.",
    "core-maths-paper2c": "As paper 1.",
    "spot-the-muppet": "AO2 game; the four AO2 games need distinct phrases.",
    "terrible-advice": "AO2 game.",
    "wrong-on-the-internet": "AO2 game.",
    "maths-court": "AO2 game.",
    "matrix-crunch": "'Matrices' keeps 'Further Maths' in the title; 'Determinants and Inverses' would drop it.",
}


def roster():
    out = []
    for line in open(ROSTER, encoding="utf-8"):
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) >= 7 and c[0].isdigit():
            m = re.match(r"^`([a-z0-9-]+)`$", c[2])
            if m:
                out.append((m.group(1), c[1], c[3]))
    return out


def level_words(levels_cell):
    table = dict(LEVEL_WORDS)
    words = []
    for part in levels_cell.split(","):
        w = table[part.strip().lower()]   # KeyError on an unknown label: never dropped
        if w not in words:
            words.append(w)
    return sorted(words, key=ORDER.index)


def title_for(phrase, words):
    lv = "/".join(words)
    if not lv.endswith("Maths"):
        lv += " Maths"
    t = "%s Game – %s | MaffsGames" % (phrase, lv)
    if len(t) <= TITLE_MAX:
        return t, True
    maths = "" if re.search(r"\bmath", phrase, re.I) else " Maths"   # never "Maths ... Maths"
    return "%s%s Game | MaffsGames" % (phrase, maths), False


def levels_sentence(words):
    if len(words) == 1:
        s = words[0]
    else:
        s = ", ".join(words[:-1]) + " and " + words[-1]
    return "For %s." % s


def description_for(practises, words):
    return "%s %s Free, no sign-up." % (practises, levels_sentence(words))


def main():
    rows = roster()
    slugs = [s for s, _, _ in rows]
    data = json.load(open("data/games.json", encoding="utf-8"))
    G = {g["slug"]: (g["search_phrase"], g["description"]) for g in data["games"]}
    if len(G) != len(data["games"]) or set(slugs) != set(G):
        print("games.json slugs differ from the roster: %s" % sorted(set(slugs) ^ set(G)))
        sys.exit(1)
    RESIT = dict(data["pages"]["resit/index.html"], path="resit/index.html")
    problems, table, dropped, titles = [], [], [], {}
    for slug, name, levels_cell in rows:
        phrase, practises = G[slug]
        words = level_words(levels_cell)
        cur = re.search(r"<title>(.*?)</title>", open("games/%s/index.html" % slug, encoding="utf-8").read(), re.S)
        cur = html.unescape(cur.group(1).strip())
        if phrase == PHRASE_NEEDED:
            title, kept = "PHRASE NEEDED", None
        else:
            title, kept = title_for(phrase, words)
            if not kept:
                dropped.append(slug)
            titles.setdefault(title, []).append(slug)
        desc = description_for(practises, words)
        if len(title) > TITLE_MAX:
            problems.append("%s title %d" % (slug, len(title)))
        if len(desc) > DESC_MAX:
            problems.append("%s description %d" % (slug, len(desc)))
        table.append((slug, cur, title, len(title), desc, len(desc), NOTES.get(slug, "")))
    for t, ss in titles.items():
        if len(ss) > 1:
            problems.append("duplicate title %r: %s" % (t, ss))
    rt, rd = RESIT["title"], RESIT["description"]
    if len(rt) > TITLE_MAX or len(rd) > DESC_MAX:
        problems.append("resit %d/%d" % (len(rt), len(rd)))
    if problems:
        print("\n".join(problems))
        sys.exit(1)

    def cell(s):
        return s.replace("|", "\\|")
    cur_resit = html.unescape(re.search(r"<title>(.*?)</title>", open(RESIT["path"], encoding="utf-8").read()).group(1))
    md = [DOC_HEAD.format(n=len(rows), dropped=len(dropped), kept=len(rows) - len(dropped) - 2), "",
          "## /resit/", "",
          "| Page | Current title | New title | Chars | New description | Chars |",
          "|---|---|---|---|---|---|",
          "| `/resit/` | %s | %s | %d | %s | %d |" % (cell(cur_resit), cell(rt), len(rt), cell(rd), len(rd)), "",
          "## Every roster game (%d), in roster order" % len(rows), "",
          "| Slug | Current title | New title | Chars | New description | Chars | Note |",
          "|---|---|---|---|---|---|---|"]
    for slug, cur, title, tl, desc, dl, note in table:
        md.append("| `%s` | %s | %s | %s | %s | %d | %s |" % (
            slug, cell(cur), cell(title), "—" if title == PHRASE_NEEDED else str(tl), cell(desc), dl, cell(note)))
    md.append("")
    md.append("**Titles with the levels part dropped (over 60 with it), %d:** %s." % (
        len(dropped), ", ".join("`%s`" % s for s in dropped)))
    md.append("")
    md.append(DOC_TAIL)
    with open("docs/seo-titles-draft.md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))
    print("ok: %d games, %d dropped levels, longest title %d, longest description %d" % (
        len(rows), len(dropped), max(t[3] for t in table if t[2] != PHRASE_NEEDED), max(t[5] for t in table)))


DOC_HEAD = """# Search titles and descriptions: draft for review (Phase 1)

Draft, 5 Oct 2026 (cloud). **Nothing on any page has changed.** This table is generated from
`data/games.json` and the roster's Levels column by the rules below; on Jon's word (with his edits)
Phase 2 writes it into every game page and /resit/ (`scripts/apply-meta.py`) and holds it there in CI
(`scripts/check-meta.py`).

**{n} roster games** (every numbered row, so it includes the unlisted `just-pythag-it-bruv`; the
withdrawn `regression-rumble` is not a numbered row). {kept} keep their levels in the title,
{dropped} drop them, 2 are PHRASE NEEDED.

## The rules (as built; each is a call for review)

1. **Title:** `<search_phrase> Game – <levels> Maths | MaffsGames`, at most 60 characters (Python
   `len`, so the en dash counts as 1). Levels from the roster in teacher words, joined with `/`, in
   the order Year 6, KS3, GCSE, A-Level, Level 3, Level 4, Further Maths, Core Maths; "A-Level Year
   2" folds into A-Level. **My call:** when the last level is Further Maths or Core Maths, " Maths"
   is not added again ("A-Level/Further Maths", not "… Further Maths Maths").
2. **Over 60:** the levels part goes, never the phrase. **My call:** the fallback is
   `<search_phrase> Maths Game | MaffsGames`, keeping "maths" in the title (the brief's root cause
   notes /resit/'s title lacks it); a phrase that already says "maths" or "mathematical" gets no
   second "Maths". The literal reading, `<search_phrase> Game | MaffsGames`, is a
   one-line change.
3. **Description:** `<what the student practises> For <levels>. Free, no sign-up.`, at most 155.
   **My call:** only the first part is stored in `games.json`; the levels sentence is generated from
   the roster, so the levels are held once, as the brief's CLASS CHECK asks.
4. **Phrases** are drawn from each game's spec-map row(s) and roster topic, in the words a teacher
   would type. Where a phrase is not from its spec row, the Note column says so.
5. **For Phase 2 (a question, not a change):** three pages (`higher-power`, `prisoners-dilemma`,
   `screening-room`) also carry `twitter:title` and `twitter:description`. The brief names og: tags
   only; I recommend apply-meta.py writes the twitter: pair too where present, or they go stale.

Rendered character counts are not pixel widths: Google truncates by width (about 580px), so a
60-character title of wide letters can still be cut. No title here relies on its last characters.
"""

DOC_TAIL = """## For review: what I would most like a ruling on

1. **41 of 97 titles lose their levels** under the brief's rule (drop the levels part when over
   60). Many are the GCSE and KS3 games the mission puts first, so "GCSE" leaves their titles. An
   alternative that keeps the rule's spirit: when over 60, keep the **first** level only
   ("Prime Factorisation Game – Year 6 Maths"), and drop it entirely only if still over 60. I have
   not applied it; say if you want it and I will regenerate the table.
2. **The two PHRASE NEEDED rows** (`truth-buster`, `just-pythag-it-bruv`), suggestions in their Note.
3. **The four Core Maths papers** use an exam-paper phrase, not a spec topic (Note column).
4. **Rules 1-3 and 5 above**: each is my call and each is a one-line change.

Regenerate this table after editing `data/games.json`: `python scripts/draft-seo-titles.py`.
"""

if __name__ == "__main__":
    main()
