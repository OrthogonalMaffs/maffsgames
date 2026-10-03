#!/usr/bin/env python3
"""Does every game that uses UK tax or NI state the teaching year, and is every such game known?

    python scripts/check-tax-year.py               # CI
    python scripts/check-tax-year.py --root <copy of the repo>   # testing

Until 3 Oct 2026 tax and NI rates were typed into each game separately, with no shared record and
no check, so core-maths-paper1 kept the pre-2024 12% NI rate unnoticed (todo §1.41). The rates now
have one canon table (§7.1.4) and one copy in code (scripts/uk_rates.py, TEACHING_YEAR). This
check is the game-side half:

  - Every page under games/ and escape-rooms/ is scanned for UK tax or NI wording (SIGNALS). A
    page that has it must be registered in TAX_GAMES below, with what it does, so a new tax game
    cannot ship unseen. A registered game whose page no longer has the wording fails as stale.
  - In every registered game, a tax year printed near tax wording ("Income Tax 2025/26",
    taxYear: "2025/26", "<dt>Tax Year</dt><dd>2025/26</dd>") must be TEACHING_YEAR. Any other
    year fails. A game with "states_year": True must state it at least once.

What each game's rates are worth is its verifier's job (verify-tax-theft.py,
verify-core-maths-paper1-tax.py, both on uk_rates.py); this check reads years and registration.
Stdlib only; about a second. A self-test runs first on every run.
"""
import argparse, pathlib, re, sys

BASE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "scripts"))
import uk_rates as ur  # noqa: E402

SCANNED = ["games", "escape-rooms"]

# The inventory of 3 Oct 2026 (todo §1.41/§1.43). Register a new tax game here in the PR that adds it.
TAX_GAMES = {
    "tax-theft": {
        "states_year": True,
        "what": "payslip game; every rate from TAX_RULES, verified against uk_rates.py by verify-tax-theft.py",
    },
    "core-maths-paper1": {
        "states_year": False,
        "what": "three §3.2 items print their own rates (income tax, NI, take-home budget); "
                "verify-core-maths-paper1-tax.py checks them against uk_rates.py",
    },
    "better-value": {
        "states_year": False,
        "what": "a job comparison gives 'Tax and NI approximately 25% of gross'; an approximation, "
                "not table rates (todo §1.43: 15-18% at those salaries in 2025/26)",
    },
}

# UK income tax / NI wording. "NI" is matched in capitals only (not "ni" inside words or code).
SIGNALS = [
    re.compile(r"\bincome tax\b", re.I),
    re.compile(r"\bnational insurance\b", re.I),
    re.compile(r"\bpersonal allowance\b", re.I),
    re.compile(r"\bPAYE\b"),
    re.compile(r"\btax code\b", re.I),
    re.compile(r"(?<![\w-])NI(?![\w-])"),
]
# A UK tax year printed near tax wording, within 80 characters either side.
YEAR = re.compile(r"\b(20\d\d)\s*[/–-]\s*(\d\d)\b")
NEAR = re.compile(r"tax|\bNI\b|national insurance|HMRC|payslip|allowance", re.I)
YEAR_WINDOW = 80
NOISE = [re.compile(r"\\u([0-9a-fA-F]{4})")]


def decode(text):
    """Unescape \\uXXXX so a JS-escaped page reads like the page itself."""
    return NOISE[0].sub(lambda m: chr(int(m.group(1), 16)), text)


def signals(text):
    return sorted({rx.pattern for rx in SIGNALS if rx.search(text)})


def stated_years(text):
    out = []
    for m in YEAR.finditer(text):
        lo, hi = max(0, m.start() - YEAR_WINDOW), m.end() + YEAR_WINDOW
        if NEAR.search(text[lo:m.start()]) or NEAR.search(text[m.end():hi]):
            out.append("%s/%s" % (m.group(1), m.group(2)))
    return out


def pages(root):
    for d in SCANNED:
        base = root / d
        if not base.is_dir():
            continue
        for p in sorted(base.glob("*/index.html")):
            yield p.parent.name, p


def check(found, registry, year):
    """found: {slug: (signals, years)} for every page with tax wording or registered."""
    errors, report = [], []
    for slug, (sig, years) in sorted(found.items()):
        if sig and slug not in registry:
            errors.append("%s: uses UK tax/NI wording (%s) but is not registered in TAX_GAMES: "
                          "register it, and check its rates against scripts/uk_rates.py (canon §7.1.4)"
                          % (slug, ", ".join(sig)))
            continue
        if slug not in registry:
            continue
        if not sig:
            errors.append("%s: registered in TAX_GAMES but its page has no tax/NI wording: remove it" % slug)
            continue
        bad = sorted(set(y for y in years if y != year))
        if bad:
            errors.append("%s: states tax year %s; the teaching year is %s (canon §7.1.4)"
                          % (slug, ", ".join(bad), year))
        if registry[slug]["states_year"] and year not in years:
            errors.append("%s: registered as stating its tax year, but no %s found near tax wording"
                          % (slug, year))
        report.append((slug, years, registry[slug]["what"]))
    for slug in sorted(set(registry) - set(found)):
        errors.append("%s: registered in TAX_GAMES but no such page under %s: remove it"
                      % (slug, " or ".join(SCANNED)))
    return errors, report


def selftest():
    assert decode(r"Income Tax 2025\/26 £12,570") == r"Income Tax 2025\/26 £12,570"
    assert stated_years("<h4>Income Tax 2025/26</h4>") == ["2025/26"]
    assert stated_years('taxYear: "2024/25",') == ["2024/25"]
    assert stated_years("<dt>Tax Year</dt><dd>2025–26</dd>") == ["2025/26"]
    assert stated_years("Academic year 2026/27 opener") == []          # no tax wording near it
    assert stated_years("~32,000 schools (DfE 2024/25)") == []
    assert signals("Tax and NI are approximately 25%") and not signals("drawAngle(34,35)")
    assert not signals("const NIX = 1; mini; uni-code") and signals("employer NI and pension")
    reg = {"a": {"states_year": True, "what": ""}, "b": {"states_year": False, "what": ""}}
    ok = {"a": (["x"], ["2025/26"]), "b": (["x"], [])}
    assert check(ok, reg, "2025/26")[0] == []
    assert len(check({**ok, "a": (["x"], ["2025/26", "2024/25"])}, reg, "2025/26")[0]) == 1  # wrong year
    assert len(check({**ok, "a": (["x"], [])}, reg, "2025/26")[0]) == 1                      # year missing
    assert len(check({**ok, "c": (["x"], [])}, reg, "2025/26")[0]) == 1                      # unregistered
    assert len(check({**ok, "b": ([], [])}, reg, "2025/26")[0]) == 1                         # stale
    assert len(check({"a": ok["a"]}, reg, "2025/26")[0]) == 1                                # gone


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(BASE))
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # a Windows console is cp1252
    selftest()
    root = pathlib.Path(args.root).resolve()
    found, n = {}, 0
    for slug, p in pages(root):
        n += 1
        text = decode(p.read_text(encoding="utf-8", errors="replace"))
        sig = signals(text)
        if sig or slug in TAX_GAMES:
            found[slug] = (sig, stated_years(text))
    errors, report = check(found, TAX_GAMES, ur.TEACHING_YEAR)

    print("Teaching year (scripts/uk_rates.py): %s. Pages scanned: %d. Registered tax games: %d."
          % (ur.TEACHING_YEAR, n, len(TAX_GAMES)))
    for slug, years, what in report:
        print("  %-20s years stated: %-22s %s" % (slug, ", ".join(sorted(set(years))) or "(none)", what))
    for e in errors:
        print("FAIL  %s" % e)
    if errors:
        print("\n%d problem(s)." % len(errors))
        return 1
    print("\nOK  every tax game is registered and states only %s." % ur.TEACHING_YEAR)
    return 0


if __name__ == "__main__":
    sys.exit(main())
