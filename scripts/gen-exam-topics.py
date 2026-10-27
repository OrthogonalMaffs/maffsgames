#!/usr/bin/env python3
"""The 6 P's: generate the topic data file from the OCR Foundation audit (contract THE-6-PS, Jon, 24 Oct 2026).

    python scripts/gen-exam-topics.py            # print the data and its totals
    python scripts/gen-exam-topics.py --write    # write schools/assets/exam-topics-ocr-foundation.json
    python scripts/gen-exam-topics.py --check    # exit 1 if the committed file is not what this script generates

The table below is the one place the audit's figures are typed: an audit of 18 OCR J560 Foundation papers (June
2025, Nov 2024, June 2024, Nov 2023, June 2023, Nov 2022), each topic's average marks per series (three papers,
300 marks) and the number of the six series it appeared in. /the-6-ps/ reads the generated file and types no figure
of its own (a figure on a page is a claim); scripts/verify-the-6-ps.py holds both to that.

  COVERED      a topic a real game already teaches, with its route: the game, the level it opens at, and the game's
               own keys to choose from, one picked per session: modes (sent as &mode=, a [data-mode] button) or stages
               (sent as &stage=, a [data-stage] button); none means the game's own menu. Jon's rulings of 25 Oct 2026:
               how-many-parts Foundation stage 3, simultaneous-solver stage 4 and free-daily-pizza stages 1-3 (by
               &stage=), shape-shifter Random Mix (random-mix), negative-number-line with no mode; venn and
               two-way-tables moved to coming soon (Given That's second question is always P(A|B), Higher content). Where the
               contract named no level, the route takes the game's declared fallback (MaffsLevel.resolve), and the
               verifier checks every level is one the game declares.
  band         Jon's grade band for the topic (24 Oct 2026; his judgement from the audit, not OCR data). Used only to
               order a session's six topics, lower bound first, then upper. Never shown as a grade.
  COVERED needs a bank (SIX-PS-BANKS (h), 25 Oct 2026): a topic below is covered only if
               schools/assets/six-ps/<topic-id>.json exists and holds at least MIN_BANK (30) questions; any other
               topic is written to coming_soon with its marks. Derived from the files, never from a manifest.
  bank-first   a covered topic whose game is not built yet (pie-charts, Jon's ruling of 26 Oct 2026): its row has game slug None, its
               route is null, and the page leaves out the "Want more practice?" link for it. When the game is built the row
               gets its slug and level.
  NOT_OFFERED  a topic the platform will not offer (Constructions, Jon, 27 Oct 2026): in neither list, never on the page; kept in
               the file under "not_offered" so a regeneration cannot bring it back as coming soon.
  COMING_SOON  a topic with no game that can run it as a burst yet ("in development"), shown on the page with its
               marks and offered in the results' tick-list. Never drawn into a session.

Game names are read from .claude/rules/game-roster.md (the one copy), never typed here.
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "schools", "assets", "exam-topics-ocr-foundation.json")
ROSTER = os.path.join(ROOT, ".claude", "rules", "game-roster.md")

SOURCE = "From 18 OCR GCSE Foundation papers, June 2025 back to November 2022."
PAPERS = 18
SERIES = 6
MARKS_PER_SERIES = 300

# id, name, avg marks per series, series appeared (of 6), band (lo, hi), game slug, level, mode keys, stage keys
COVERED = [
    ("ratio", "Ratio", 13.3, 6, (2, 5), "split-it", "ks3", ["simplify", "divide"], []),
    ("direct-proportion", "Direct proportion", 11.7, 6, (1, 4), "split-it", "ks3", ["unitary", "scale"], []),
    ("powers-roots", "Powers and roots", 9.0, 6, (2, 5), "index-laws", "gcse", [], []),
    ("compound-measures", "Compound measures", 8.2, 6, (3, 5), "squared-squirrel", "ks3", ["stage-2", "stage-3"], []),
    ("linear-equations", "Linear equations", 7.5, 6, (2, 5), "linear-equation-solver", "gcse", [], []),
    ("sequences", "Sequences", 7.3, 6, (1, 4), "sequence-solver", "ks3", [], []),
    ("angles", "Angles", 7.2, 6, (1, 4), "angle-ace", "gcse", [], []),
    ("arithmetic-negatives", "Negative numbers", 7.0, 5, (1, 3), "negative-number-line", "year6", [], []),
    ("fdp-convert", "Fractions, decimals and percentages", 6.8, 6, (1, 3), "free-daily-pizza", "ks3", [], ["1", "2"]),
    ("number-vocabulary", "Factors, multiples and primes", 6.7, 6, (1, 3), "factor-race", "ks3", [], []),
    ("fraction-operations", "Calculating with fractions", 6.5, 6, (1, 4), "how-many-parts", "ks3", ["stage3"], []),
    ("fraction-percentage-of-amount", "Fractions and percentages of amounts", 6.3, 6, (1, 4), "free-daily-pizza", "ks3", [], ["3"]),
    ("averages", "Averages and range", 6.3, 6, (1, 4), "distinctly-average", "ks3", [], []),
    ("area", "Area", 6.0, 6, (1, 5), "take-a-walk", "ks3", ["stage-1", "stage-2", "stage-3"], []),
    ("inverse-operations", "Inverse operations", 5.3, 6, (1, 3), "think-of-a-number", "year6", [], []),
    ("trigonometry", "Trigonometry", 5.0, 6, (4, 5), "trig-worms", "gcse", [], []),
    ("simultaneous", "Simultaneous equations", 4.2, 4, (4, 5), "simultaneous-solver", "gcse", [], ["stage4"]),
    ("transformations", "Transformations", 4.0, 5, (1, 4), "shape-shifter", "year6", ["random-mix"], []),
    ("simplify-expressions", "Simplifying expressions", 3.7, 5, (1, 3), "like-terms-collector", "year6", [], []),
    ("basic-probability", "Probability", 3.7, 5, (1, 3), "probability-pioneer", "year6", [], []),
    ("substitution", "Substitution", 3.5, 5, (1, 4), "formula-plug-in", "year6", [], []),
    ("perimeter", "Perimeter", 3.3, 4, (1, 4), "take-a-walk", "ks3", ["stage-1"], []),
    ("standard-form", "Standard form", 3.2, 5, (4, 5), "standard-form-blitz", "gcse", [], []),
    ("quadratics-factorise", "Factorising quadratics", 3.0, 6, (4, 5), "quadratic-factoriser", "gcse", [], []),
    ("estimation", "Estimation", 3.0, 5, (2, 4), "estimation-engine", "gcse", [], []),
    ("metric-units", "Metric units", 3.0, 4, (1, 3), "unit-converter", "gcse", [], []),
    ("vectors", "Vectors", 2.8, 5, (3, 4), "component-crusher", "gcse", [], []),
    ("form-expressions", "Forming expressions and equations", 2.7, 5, (3, 4), "equation-builder", "ks3", [], []),
    ("rounding", "Rounding", 2.3, 5, (1, 3), "decimal-detective", "year6", [], []),
    ("pythagoras", "Pythagoras' theorem", 2.3, 3, (4, 5), "just-pythag-it-bruv", "ks3", [], []),
    ("change-subject", "Changing the subject", 2.0, 5, (4, 5), "formula-unlocked", "gcse", [], []),
    ("coordinates", "Coordinates", 1.8, 5, (1, 2), "four-quadrant-explorer", "year6", [], []),
    # Bank-first (Jon, 26 Oct 2026; contract PIE-CHARTS-BANK, canon 8.2.1): the bank comes before its game, so no route yet ("Who Ate
    # All the Pies?" is the planned game). The page leaves out "Want more practice?" for a topic whose route is null.
    ("pie-charts", "Pie charts", 4.0, 4, (2, 4), None, None, [], []),
    # Bank-first (Jon, 27 Oct 2026; contract PERCENTAGES-MONEY-BANK): percentage change and reverse percentages (36 marks) and interest and
    # depreciation (44 marks) of 1,800 over 18 papers; they were two coming-soon rows (6.0 and 7.3 a series). "It's on Sale!" is the planned game.
    ("percentages-money", "Percentages, interest and depreciation", 13.3, 6, (3, 5), None, None, [], []),
]

# id, name, avg marks per series, series appeared (of 6), planned game name (or None)
COMING_SOON = [
    ("everyday-multi-step", "Everyday multi-step problems", 14.3, 6, None),
    ("scatter-graphs", "Scatter graphs", 6.2, 6, None),
    ("volume-surface-area", "Volume and surface area", 5.5, 6, None),
    ("hcf-lcm", "HCF and LCM", 5.3, 6, None),
    ("expand-factorise", "Expanding and factorising", 5.3, 6, "The HC Factor"),
    ("tree-diagrams", "Tree diagrams", 5.3, 5, None),
    ("bar-pictogram-line", "Bar charts, pictograms and line graphs", 5.2, 5, None),
    ("relative-frequency", "Relative frequency", 4.8, 6, None),
    # Moved from COVERED (Jon, 25 Oct 2026): Given That's second question is always P(A|B), Higher content, so no
    # Foundation burst serves them.
    ("venn", "Venn diagrams", 4.2, 6, None),
    ("straight-line-graphs", "Straight-line graphs", 4.7, 6, "Y So Steep?"),
    ("similarity-congruence", "Similarity and congruence", 4.7, 6, None),
    ("listing-outcomes", "Listing outcomes", 4.5, 6, None),
    ("scale-bearings", "Scale drawings and bearings", 4.5, 5, None),
    ("2d-shapes", "2D shapes", 3.8, 5, None),
    ("two-way-tables", "Two-way tables", 3.5, 3, None),   # moved from COVERED with venn (Jon, 25 Oct 2026)
    ("quadratic-graphs", "Quadratic graphs", 3.5, 5, None),
    ("real-life-graphs", "Real-life graphs", 3.2, 4, None),
    ("3d-solids", "3D solids", 3.0, 6, None),
    ("bounds", "Bounds", 2.8, 5, None),
    ("inequalities", "Inequalities", 2.5, 5, None),
    ("enlargement", "Enlargement", 1.7, 3, None),
]


# NOT_OFFERED: a topic the platform will not offer, so it is neither covered nor coming soon: the page lists it nowhere (not under
# "Coming soon", not in the "Was a topic missing?" tick-list) and no session draws it. It stays in the data file, under "not_offered",
# with its marks, so the audit's 300 marks a series still add up and a regeneration cannot bring it back as coming soon.
#   id, name, avg marks per series, series appeared (of 6), why
NOT_OFFERED = [
    ("constructions", "Constructions", 4.0, 6,
     "A drawing skill (compasses and ruler) that cannot be practised on a screen; Jon, 27 Oct 2026. It is practised on paper."),
]


MIN_BANK = 30   # a topic is covered only if schools/assets/six-ps/<id>.json holds at least this many questions
BANK_DIR = os.path.join(ROOT, "schools", "assets", "six-ps")


def bank_size(tid):
    """Questions in the topic's bank, 0 if it has none. Derived from the file: no manifest."""
    try:
        with open(os.path.join(BANK_DIR, tid + ".json"), encoding="utf-8") as f:
            return len(json.load(f).get("questions", []))
    except (OSError, ValueError):
        return 0


def roster_names():
    """{slug: game name} from the roster's numbered rows (a withdrawn row, numbered with a dash, is left out)."""
    names = {}
    row = re.compile(r"^\|\s*\d+\s*\|\s*([^|]+?)\s*\|\s*`([a-z0-9-]+)`\s*\|")
    with open(ROSTER, encoding="utf-8") as f:
        for line in f:
            m = row.match(line)
            if m:
                names[m.group(2)] = m.group(1)
    return names


def build():
    names = roster_names()
    errors = []
    covered = []
    coming = [{"id": tid, "name": name, "marks": marks, "series": series, "planned": planned}
              for tid, name, marks, series, planned in COMING_SOON]
    for tid, name, marks, series, band, slug, level, modes, stages in COVERED:
        if slug is not None and slug not in names:
            errors.append("%s: game %s is not a numbered roster row" % (tid, slug))
        if bank_size(tid) < MIN_BANK:
            # Covered only by a bank (SIX-PS-BANKS (h), 25 Oct 2026): with fewer than MIN_BANK questions the topic is
            # coming soon, with its marks as now, placed where its marks put it among the others.
            entry = {"id": tid, "name": name, "marks": marks, "series": series, "planned": None}
            at = next((i for i, c in enumerate(coming) if c["marks"] < marks), len(coming))
            coming.insert(at, entry)
            continue
        covered.append({
            "id": tid, "name": name, "marks": marks, "series": series, "band": list(band),
            "route": None if slug is None else {"slug": slug, "game": names.get(slug, ""), "level": level, "modes": modes, "stages": stages},
        })
    not_offered = [{"id": tid, "name": name, "marks": marks, "series": series, "reason": why}
                   for tid, name, marks, series, why in NOT_OFFERED]
    ids = [t["id"] for t in covered] + [t["id"] for t in coming] + [t["id"] for t in not_offered]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        errors.append("duplicate topic ids: %s" % ", ".join(dup))
    for t in covered + coming + not_offered:
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", t["id"]):
            errors.append("%s: an id is lower case, digits and hyphens" % t["id"])
        if not (0 < t["marks"] <= MARKS_PER_SERIES) or round(t["marks"] * 10) != t["marks"] * 10:
            errors.append("%s: marks %r is not a positive figure to one decimal place" % (t["id"], t["marks"]))
        if not (1 <= t["series"] <= SERIES):
            errors.append("%s: series %r is not 1 to %d" % (t["id"], t["series"], SERIES))
    for t in covered:
        if t["route"] and t["route"]["modes"] and t["route"]["stages"]:
            errors.append("%s: a route opens by mode or by stage, not both" % t["id"])
        lo, hi = t["band"]
        if not (1 <= lo <= hi <= 9):
            errors.append("%s: band %r is not a grade range" % (t["id"], t["band"]))
    data = {
        "_generated": "by scripts/gen-exam-topics.py from its table; never edit by hand",
        "board": "OCR", "tier": "Foundation", "source": SOURCE,
        "papers": PAPERS, "series": SERIES, "marks_per_series": MARKS_PER_SERIES,
        "covered": covered, "coming_soon": coming, "not_offered": not_offered,
    }
    return data, errors


def dump(data):
    return json.dumps(data, indent=1, ensure_ascii=False) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="write the data file")
    ap.add_argument("--check", action="store_true", help="fail if the committed data file differs from this output")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    data, errors = build()
    for e in errors:
        print("ERROR  " + e)
    if errors:
        return 1
    if a.check:
        try:
            with open(OUT, encoding="utf-8") as f:
                committed = json.load(f)
        except (OSError, ValueError) as e:
            print("FAIL  %s cannot be read: %s" % (os.path.relpath(OUT, ROOT), e))
            return 1
        if committed != data:   # compared as data, so a checkout's line endings cannot fail it
            print("FAIL  %s is not what scripts/gen-exam-topics.py generates; run it with --write"
                  % os.path.relpath(OUT, ROOT))
            return 1
        print("PASS  %s matches the generator" % os.path.relpath(OUT, ROOT))
        return 0
    if a.write:
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            f.write(dump(data))
        print("wrote %s" % os.path.relpath(OUT, ROOT))
    else:
        sys.stdout.write(dump(data))
    cov = sum(t["marks"] for t in data["covered"])
    soon = sum(t["marks"] for t in data["coming_soon"])
    off = sum(t["marks"] for t in data["not_offered"])
    print("covered %d topics, %.1f marks a series; coming soon %d, %.1f; not offered %d, %.1f" % (
        len(data["covered"]), cov, len(data["coming_soon"]), soon, len(data["not_offered"]), off), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
