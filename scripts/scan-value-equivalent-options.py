"""Read-only scan: option pairs that are different strings but equal in value.

  python scripts/scan-value-equivalent-options.py              # JSON report to stdout
  python scripts/scan-value-equivalent-options.py --selftest   # the shared value fixtures

Reads data/banks/*.json (regenerate with scripts/extract-banks.py) and walks each
question's options with the same bank_common helpers check-banks.py's B2 uses, so
the options examined are exactly B2's. B2 already catches identical strings; this
compares only DISTINCT strings, by value, with SymPy (surds, powers, fractions,
percentages, coordinates, ratios by HCF, equations up to a constant multiple).
Options it cannot parse (prose, units in words, inequalities) are counted, never
guessed.

Not a CI step and not a lint rule: it is the evidence behind
docs/scan-value-equivalent-options.md, and the starting point for the rule proposed
in docs/next-contract-value-equivalent-options.md. Found 28 Sep 2026 from
coordinate-geometry-dash:233 (5√2 keyed, √50 marked wrong).
"""
import glob, json, os, platform, sys, itertools, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import bank_common as bc  # noqa: E402
import sympy as sp  # noqa: E402

# The parser lives in bank_common (moved 2 Oct 2026), shared with check-banks.py B11.
parse_value, equal = bc.parse_value, bc.equal

PINNED_SYMPY = "1.14.0"     # scripts/scan-requirements.txt; CI installs this today


def dedup_groups(bank):
    seen = {}
    for lv, info in bank.get("levels", {}).items():
        for g in info.get("groups", []):
            key = (g["variable"], tuple(g["path"]))
            if key not in seen:
                seen[key] = {"variable": g["variable"], "path": g["path"], "questions": g["questions"]}
    return list(seen.values())


def main():
    hits = []
    stats = collections.Counter()
    unread = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "banks", "*.json"))):
        bank = json.load(open(f, encoding="utf-8"))
        slug = bank["slug"]
        if not bank.get("generator") and bank.get("read_method") not in ("live", "static_fallback"):
            unread.append("%s (%s)" % (slug, bank.get("read_method")))
        for g in dedup_groups(bank):
            for idx, q in enumerate(g["questions"]):
                if not isinstance(q, dict):
                    continue
                units = []
                for label, unit in bc.sub_answer_units(q):
                    if "_valid_letters" in unit:
                        continue
                    pool = bc.option_pool(unit)
                    if pool:
                        units.append((label, pool, bc.resolve_correct(unit)))
                fl = bc.flagged_option_texts_and_correct_count(q)
                if fl:
                    units.append(("flagged", fl[0], None))
                for label, pool, correct in units:
                    distinct = list(dict.fromkeys(p for p in pool if isinstance(p, str)))
                    parsed = {}
                    for p in distinct:
                        stats["options"] += 1
                        v = parse_value(p)
                        if v is None:
                            stats["unparsed"] += 1
                        else:
                            stats["parsed"] += 1
                            parsed[p] = v
                    for a, b in itertools.combinations(parsed, 2):
                        if a.strip() == b.strip():
                            continue
                        if equal(parsed[a], parsed[b]):
                            ck = str(correct) if correct is not None else None
                            hits.append({"slug": slug, "where": "%s%s[%d]%s" % (
                                g["variable"], ("." + ".".join(g["path"])) if g["path"] else "", idx,
                                ("." + label) if label else ""),
                                "pair": [a, b], "kind": parsed[a][0] + "/" + parsed[b][0],
                                "involves_key": ck in (a, b), "key": ck, "pool": pool,
                                "q": bc.question_text(q)})
    env = {"python": platform.python_version(), "sympy": sp.__version__}
    print(json.dumps({"env": env, "stats": stats, "hits": hits}, ensure_ascii=False, indent=1, default=str))
    # A bank the extractor could not read scans as no options at all, so a smaller pair
    # list looks clean. That is how the 28 Sep run missed differentiation-duel, index-laws
    # and integration-duel: the cloud sandbox blocks the KaTeX CDN, and those pages do not
    # load without it. Refuse rather than report a partial list.
    if unread:
        sys.stderr.write("REFUSED: %d non-generator bank(s) not read live, so the pair list "
                         "would be partial: %s. Re-extract where the KaTeX CDN is reachable "
                         "(see docs/sandbox-checks.md).\n" % (len(unread), ", ".join(unread)))
        return 2
    if sp.__version__ != PINNED_SYMPY:
        sys.stderr.write("NOTE: SymPy %s, pinned %s (scripts/scan-requirements.txt).\n"
                         % (sp.__version__, PINNED_SYMPY))
    return 0


# The fixtures live in bank_common (one copy), shared with check-banks.py --selftest.
FIXTURES_EQUAL = bc.VALUE_FIXTURES_EQUAL
FIXTURES_UNEQUAL = bc.VALUE_FIXTURES_UNEQUAL


def selftest():
    bad = 0
    for a, b in FIXTURES_EQUAL:
        pa, pb = parse_value(a), parse_value(b)
        if not (pa and pb and equal(pa, pb)):
            bad += 1
            print("MISSED equal: %r %r" % (a, b))
    for a, b in FIXTURES_UNEQUAL:
        pa, pb = parse_value(a), parse_value(b)
        if pa and pb and equal(pa, pb):
            bad += 1
            print("FALSE hit: %r %r" % (a, b))
    total = len(FIXTURES_EQUAL) + len(FIXTURES_UNEQUAL)
    print("%d fixtures (%d equal, %d unequal): %s" % (
        total, len(FIXTURES_EQUAL), len(FIXTURES_UNEQUAL), "FAILED %d" % bad if bad else "OK"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv[1:] else main())
