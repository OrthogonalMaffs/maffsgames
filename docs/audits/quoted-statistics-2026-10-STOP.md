# Quoted real-world statistics audit: STOP report (5 Oct 2026)

**Status: halted, waiting for Jon's rulings.** This is not the audit report the contract asks for
(`docs/audits/quoted-statistics-2026-10.md`). Three of the contract's STOP IFs fired. Nothing in any game, question
bank, `check-content-safety.py` or canon was changed.

| STOP IF | Fired? | Detail |
|---|---|---|
| Hit count passes 150 | **Yes**, on the contract's own unit (one hit = one figure with one status, step 2) | about 250 figures in about 130 items, 17+ games (table below) |
| A CONTRADICTED figure is in a keyed answer | **Yes**: two Fermi Lab references | §1 |
| More than a handful of items need a real-vs-invented judgement | **Yes**: whole classes of items | §3 |

## 1. Keyed figures contradicted by a source (reported first, as the contract requires)

Fermi Lab marks each chain step by a factor band around a keyed `reference` (`withinFactor()`,
`games/fermi-lab/index.html:446`): **green 15 pts, amber 8, red 2.** Both items below put the reference at about
half the real figure. A student who enters the true figure gets amber instead of green: they lose 7 points for being
right. Each hint also states the wrong figure, so the student who follows the hint gets green.

| Item | Player-visible wording | Keyed reference (green band) | Source figure | Effect on a correct answer |
|---|---|---|---|---|
| `fermi-lab` `eq_sleep_loss` (core) | "GCSE students in England: Approximately 300,000 students sitting GCSEs." | 300,000 (×2: 150,000 to 600,000) | **625,673** pupils at the end of KS4 in state-funded schools in England, 2024/25 (DfE, [Key stage 4 performance 2024/25](https://explore-education-statistics.service.gov.uk/find-statistics/key-stage-4-performance/2024-25)) | 625,673 / 300,000 = 2.09: **amber**, not green |
| `fermi-lab` `eq_homework` (core) | "GCSE students in England: Approximately 600,000 students in Years 10 and 11." | 600,000 (×2: 300,000 to 1,200,000) | Years 10 and 11 are two cohorts of about 625,000 each (same DfE release), so about **1.25 million** | about 2.08: **amber**, not green |

The two items also contradict each other: one puts the cohort sitting GCSEs at 300,000, the other puts two cohorts
at 600,000.

*How verified:* WebSearch, whose result quoted the DfE figure and named the page above. The page itself could not be
fetched (WebFetch is blocked for every gov.uk, ONS and Wikipedia host, see Method). Corroboration: JCQ's 2025
press notice reports 5,212,910 GCSE entries from Year 11 students ([JCQ](https://www.jcq.org.uk/wp-content/uploads/2025/08/UK-JCQ-Press-notice-Level-1-2-2025.pdf)),
consistent with roughly 600,000 candidates sitting about 8 to 9 subjects each, not 300,000.

**Not fixed, per DO NOT TOUCH.**

## 2. Count by game (why the 150 STOP fired)

"Figure" = one real-world number stated as fact (each needs its own status under step 2). "Items" = questions or cards
containing at least one. The counts are lower bounds: the scan stopped at the STOP IF, and the games marked * were not
read in full.

| Game | Items | Figures | What they are |
|---|---|---|---|
| `fermi-lab` | 61 of 65 | ~155 (128 chain-step references or hints not given by the question, plus 27 sourced answer notes) | UK population, school counts, London population, household size, distances, Lego and Forth Bridge figures, energy use; many keyed (see §1) |
| `screening-room`* | ≥14 | ≥40 | NHS programme prevalences and test sensitivity and specificity (breast, bowel FIT, cervical, AAA, Health Check), UK HIV 0.16%, COVID 0.2%, CF carriers 1 in 25 |
| `higher-power` | ~22 | ~22 | **Keyed** card values: speed of light, distances to the Moon and Sun, speed of sound, Earth's radius, world population, largest Mersenne exponent; facts: NFL 32 teams, ASCII 128, Plato's 5,040, Euler 1735, Apéry 1978 |
| `standard-form-blitz` | 5 | ~9 | Sun distance, proton mass, hair and atom widths, Earth and Moon masses |
| `estimation-golf` | ~7 | ~7 | **Keyed** (proximity-scored): bones 206, adult teeth 32, continents 7, "typical school class" 30, door 200 cm, speed of sound 343 |
| `truth-buster` | 7 | 8 | tb_t2_012's mozzarella r = 0.959 (sourced, PR #62); Cantor 1874, Smale 1957, Four Colour 1976, Gödel 1931, Goldbach 1742 and 4×10¹⁸ |
| `word-problem-decoder`, `spot-the-error`, `equation-builder` | 6 | ~12 | Earth and Moon masses, Proxima Centauri distance, speed of light, hair diameter |
| `52dle` | 3 | 3 | "52! … more than atoms in the observable universe"; 7 "the most favourite number of humans globally"; Mersenne 521 in 1952 |
| `probability-paradox`* | ≥2 | ≥3 | Hot hand: Gilovich et al. 1985, Miller and Sanjurjo 2015 |
| `given-that`* | 2 | 2 | Lateral flow at 5% prevalence; a "Met Office forecast accuracy" tree |
| `wrong-on-the-internet` | 1 | 1 | "UK inflation in 2023 was 7.3%" |
| `core-maths-paper1` | 1 | 2 | "CPI inflation: 8.7% in 2022, 6.3% in 2023" |
| `better-value` | 1 | 2 | Average rent: Manchester £650, London £1,200 a month |
| `seven-bridges` | 1 | 1 | Euler, 1736 |
| **Total (lower bound)** | **~133** | **~265** | |

Not yet read for real-world figures: `unit-converter`, `dimension-checker`, `curling-friction`, `force-resolver`,
`correlation-or-coincidence`'s axis data, `core-maths-paper2a`/`2b`/`2c` beyond the scan, `estimation-engine`, and the
rest of `screening-room` and `probability-paradox`.

## 3. Judgement calls needed (the third STOP IF)

Telling a real-world claim from an invented context is not item-by-item here: it is several whole classes. Each needs
Jon's ruling before the audit can be scoped. I have not decided any of them.

1. **Fermi Lab's chain references.** Some are facts ("UK population 67,000,000"), some are modelling guesses offered
   as typical ("3 slices per person per day", "2% of households own a piano"), and all are keyed. Are the guesses in
   scope, or only references the hint states as fact?
2. **Physical, astronomical and biological constants** (speed of light, Earth's mass, bones in the body). They are
   real-world figures but not "statistics", and the contract's list does not name them. In or out?
3. **General-knowledge counts keyed in Estimation Golf's Year 6 bank** (teeth, continents, "typical class"). These
   are conventions as much as data: 7 continents is one model of several, and "typical class 30" is not the DfE
   average.
4. **Dates of mathematical results** (Truth Buster, Higher Power, Seven Bridges, 52-dle). The contract lists "real
   dates presented as data"; these are history, not data.
5. **Screening Room's school-sample items** (hearing 3%, colour blindness 8%, nut allergy 2%). Each figure is
   attributed to an invented sample ("A school screens 1,000 students"), but the rates read as real prevalences.
6. **Real indices with real years, no source** (`core-maths-paper1`'s CPI 8.7% and 6.3%; `wrong-on-the-internet`'s
   7.3%). Are they data claims or worked-example numbers?

## 4. Found on the way, not keyed

- `52dle` (the 52 puzzle's clue, `games/52dle/index.html`, `PUZZLES[0]`): "52! arrangements — more than atoms in the
  observable universe." **CONTRADICTED**: 52! = 8.07 × 10⁶⁷ (computed); atoms in the observable universe are usually
  estimated at about 10⁸⁰, range 10⁷⁸ to 10⁸² ([ProofWiki](https://proofwiki.org/wiki/Number_of_Atoms_in_Observable_Universe),
  via WebSearch). The keyed answer (52) is unaffected. Higher Power's googol card ("larger than atoms in the observable
  universe") is consistent with the same source.
- `higher-power` `gcse_34` "Largest Mersenne prime exponent 136,279,841": still the largest known as of September 2026
  (M52, found 12 Oct 2024; [Wikipedia: Largest known prime number](https://en.wikipedia.org/wiki/Largest_known_prime_number),
  via WebSearch). It is keyed and will go stale when GIMPS finds M53.

## Method so far (repeatable)

- **Files:** every `games/**/*.html|js` and `escape-rooms/**/*.html|js`: **134 files**. These are the same globs as
  `check-content-safety.py`. Each file is reduced to player-visible text by that script's `displayed()`, imported
  read-only, not changed.
- **Net:** the regex patterns in the appendix (correlation coefficients, study and survey words, agencies, rates on
  real populations, prevalences, records, years as data, real prices, named real places and people, measured real
  objects). The first pass matched 292 lines and the second 329. Each matched line was read by hand. Games likely to
  hold real-world facts were then read in full where the net is blind (keyed values in data fields): `fermi-lab`,
  `higher-power`, `estimation-golf`, `52dle`, `truth-buster`.
- **Network:** `curl` from the sandbox reaches only GitHub. WebFetch is blocked for en.wikipedia.org, gov.uk, ons.gov.uk,
  networkrail.co.uk and every other source host tried. WebSearch works and names its sources. Its result is a summary of
  the pages, not the page read directly, so every status in this file says "via WebSearch". If Jon wants VERIFIED to
  mean "page read", most items will be UNVERIFIABLE from the sandbox.

## What a scope ruling would let me finish

Options, for Jon to choose (or amend):
- **(a) Statistics only, as the contract's list reads:** correlations, studies and surveys, rates on real populations,
  records, prices, inflation, and Fermi references only where the hint states them as fact. Out: constants, general
  knowledge, maths history. Estimate: ~120 figures, mostly Fermi Lab and Screening Room.
- **(b) Everything keyed first:** every real-world figure a student is marked against (Fermi Lab references, Higher
  Power values, Estimation Golf answers), then the rest. This targets the "marked wrong for a correct answer" risk.
- **(c) Everything, raise the cap:** all ~265+ figures. Feasible, but most statuses would rest on WebSearch summaries
  (see Network).

## Appendix: the scan script

The script lives outside the repo (scratchpad). Its patterns and loop are reproduced here so the scan can be re-run
from the repo root with `python scan_stats.py --json hits.json`.

```python
import argparse, importlib.util, json, pathlib, re, sys
PATTERNS = {
    "r-value": r"(?<![A-Za-z])r\s*(?:=|≈|≃|~|is about|of)\s*[-−–]?\s*(?:0|1)?\.\d",
    "correlation-of": r"correlation (?:coefficient )?(?:of|was|is|=)\s*[-−–]?\s*0?\.\d",
    "study": r"\b(?:study|studies|survey(?:ed)?|poll(?:ed)?|research(?:ers)?|scientists|census|meta-analysis|trial)\b",
    "source-words": r"\b(?:according to|data from|source:|published|reported|statistics show|figures show|found that)\b",
    "agency": r"\b(?:ONS|Office for National Statistics|NHS|WHO|World Health|DfE|Ofsted|Met Office|"
              r"HMRC|gov\.uk|UNESCO|UNICEF|OECD|World Bank|CDC|NASA|FIFA|Olympic\w*|Guinness)\b",
    "pct-population": r"\d[\d.,]*\s*(?:%|per ?cent)[^.\n]{0,60}\b(?:of|in)\s+(?:the\s+)?(?:UK|British|Britons|"
                      r"England|English|Scotland|Wales|US|USA|American|adults|children|people|population|"
                      r"households|teenagers|pupils|students|men|women|drivers|smokers|world)\b",
    "population-rate": r"\b(?:UK|Britain|British|England|US|USA|America|world(?:wide)?|global(?:ly)?)\b[^.\n]{0,60}"
                       r"\d[\d.,]*\s*(?:%|per ?cent|million|billion|in \d|out of \d|per \d)",
    "prevalence": r"\b(?:prevalence|incidence|affects? (?:about|around|roughly)?\s*\d|1 in \d+ (?:people|adults|children|of))",
    "record": r"\b(?:world record|record[- ]breaking|record holder|fastest|tallest|longest|highest ever|"
              r"largest ever|biggest ever)\b",
    "year-data": r"\b(?:in|since|from|between|by|during)\s+(?:1[6-9]\d\d|20[0-3]\d)\b",
    "real-price": r"\b(?:average (?:UK |British )?(?:house|salary|wage|price|rent|income)|national minimum wage|"
                  r"national living wage|minimum wage|state pension|inflation|interest rate|Bank of England|"
                  r"FTSE|stock market)\b",
    "named-real": r"\b(?:Nicolas Cage|Usain Bolt|Everest|Eiffel|Big Ben|Titanic|Moon landing|Mount|"
                  r"London|Manchester|Birmingham|Premier League|World Cup)\b",
    "real-object": r"\b(?:Earth|Sun|Moon|Mars|Jupiter|Saturn|Venus|Mercury|Neptune|Uranus|Pluto|planet|galaxy|"
                   r"Milky Way|light[- ]years?|speed of (?:light|sound)|atom|electron|proton|neutron|nucleus|"
                   r"bacteri\w*|virus|red blood cells?|DNA|human hair|human body|heart beats?|neurons?|"
                   r"population of|people (?:live|living) in|inhabitants)\b",
    "measured-real": r"\b(?:mass of the|diameter of the|distance (?:from|to|between) the|height of the|"
                     r"is about [\d.,]+\s*(?:m|km|kg|tonnes|metres|miles) (?:tall|high|long|wide|deep))\b",
}
CASE = {"agency"}   # acronyms: WHO must not match "who"
RX = {k: re.compile(v, 0 if k in CASE else re.I) for k, v in PATTERNS.items()}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--root", default="."); ap.add_argument("--json")
    a = ap.parse_args(); root = pathlib.Path(a.root).resolve()
    spec = importlib.util.spec_from_file_location("ccs", root / "scripts" / "check-content-safety.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    files, seen, hits = 0, set(), []
    for g in m.GLOBS:
        for f in sorted(root.glob(g)):
            rel = f.relative_to(root).as_posix()
            if rel in seen: continue
            seen.add(rel); files += 1
            shown = m.displayed(f.read_text(encoding="utf-8", errors="replace"), js=rel.endswith(".js"))
            for n, line in enumerate(shown.split("\n"), 1):
                tags = [k for k, r in RX.items() if r.search(line)]
                if tags:
                    hits.append({"file": rel, "line": n, "tags": tags, "text": re.sub(r"\s+", " ", line).strip()})
    print("files scanned: %d; lines matched: %d" % (files, len(hits)), file=sys.stderr)
    out = json.dumps(hits, indent=1, ensure_ascii=False)
    pathlib.Path(a.json).write_text(out, encoding="utf-8") if a.json else print(out)

if __name__ == "__main__":
    main()
```
