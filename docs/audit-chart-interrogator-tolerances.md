# Chart Interrogator: box-plot and stem-and-leaf tolerances, plural nouns (todo 1.16, 1.18), and 1.8 held

**Built 1 Oct 2026** in a web session (PR 39), **amended the same day by Jon's rulings 1–3 and 5**: stem
and leaf marked exactly, box-plot bands capped below named wrong answers, the rule written into canon
§7.1.2. Built, on branch `claude/optimistic-turing-2dimgc`. Only
`games/chart-interrogator/index.html` changed. Contract B's record (`docs/audit-chart-interrogator-cumfreq.md`)
set the method and is the model for this one.

The contract carried three fixes: §1.8, §1.16 and §1.18.
- **1.16 and 1.18 are built.**
- **1.8 is held, by Jon's decision of 1 Oct.** The data contradicts its premise; see the last section.

## What changed

1. **Box plots (1.16).** A reading is marked to 2.5% of the drawn axis's span and an IQR to twice that,
   which is cumulative frequency's rule. Each band is then capped below half the gap to the nearest
   named wrong answer (canon §7.1.2, `capTol()`).
   - **Named wrong answers for a median:** the other group's median, and the box's own Q1 and Q3
     (an edge read for the median line).
   - **Named wrong answers for an IQR:** the other group's IQR, and either group's range (the range
     given for the IQR).
   - **A "wrong" value equal to the key is skipped.** B7's and B10's two IQRs are equal, so there the
     other group's IQR is the right answer.
   - **The axis has one definition**, `bpAxis(s)`. `drawBoxPlot` draws on it and the band is read off
     it. The drawing is pixel-identical to `main`.
   - **A first draft took every other line drawn as a wrong answer for a median.** That capped the
     medians of B1, B3, B4, B5 and B6, mostly because the *other* box's quartile sat near this
     median, which is not a named misconception. It went beyond the ruling and lost real readings,
     so it was narrowed before commit.
2. **Stem and leaf (1.16): marked exactly** (Jon, 1 Oct). 35.5 and 35.50 are both accepted, because
   `parseFloat` reads them as the same number. 35 and 36 are rejected for 35.5. The tolerance is only a
   floating-point guard, a billionth of the table's precision, so that 2.4 matches a key computed as
   5.6 − 3.2 = 2.3999999999999995.
3. **Plural nouns (1.18), by Jon's ruling of 1 Oct, applied to every frame that names the noun.**
   - **One helper, `nounSubject(s)`, gives the noun phrase and its verb.** A plural count noun reads as
     a number: "the median number of hours is". A plural with no singular takes "are": "the median
     earnings are", since "number of earnings" is wrong.
   - **Plurals are declared once, in `PLURAL_NOUNS`.** Today those are `hours` and `earnings`. A new
     plural noun is added there, not to a scenario.
   - **The helper is defined above the URL-parameter start-up.** `?type=…&level=…` calls `beginGame()`
     while the script is still loading.
   - **The 25% sentence is reworded for all ten scenarios**, so it never needs an article.
   - **Jon ruled that the helper also covers S4, S8 and B8**, the same bug outside cumulative frequency.
     It changed their Phase 1 question text and their Phase 2 comparison sentence.

## 1.16: every tolerance, before and after (110)

**No key changed. Only the tolerances changed.** Every key on these three types is exact: a five-number
summary drawn exactly, or a value computed from the data.

**Stem and leaf (40).** The last column asks whether one group's window also holds the other group's
true value. If it does, a student who read the wrong side of the table is marked correct.

After Jon's ruling 1, all four are marked **exactly**. The PR 39 draft's ±0.5 / ±0.05 is in the
"draft" column.

| Scenario | Median A | Median B | Range A | Range B | Before (all four) | PR 39 draft | Window holds the other group's value? |
|---|---|---|---|---|---|---|---|
| S1 | 35.5 | 39 | 43 | 40 | ±1 | ±0.5 | before: no; after: no |
| S2 | 168 | 162 | 32 | 25 | ±1 | ±0.5 | before: no; after: no |
| S3 | 4.5 | 4.8 | 2.4 | 1.9 | ±1 | ±0.05 | before: median, range; after: no |
| S4 | 45 | 20 | 25 | 24 | ±1 | ±0.5 | before: range; after: no |
| S5 | 237.5 | 272.5 | 100 | 110 | ±1 | ±0.5 | before: no; after: no |
| S6 | 48 | 72 | 33 | 40 | ±1 | ±0.5 | before: no; after: no |
| S7 | 40 | 25 | 35 | 45 | ±1 | ±0.5 | before: no; after: no |
| S8 | 222.5 | 355 | 80 | 170 | ±1 | ±0.5 | before: no; after: no |
| S9 | 49.3 | 49.65 | 2.1 | 3.5 | ±1 | ±0.05 | before: median; after: no |
| S10 | 51.5 | 53 | 16 | 30 | ±1 | ±0.5 | before: no; after: no |

**Box plots (40).** The drawn axis is 1.2 × the data range. "Band" is 2.5% of it for a median and 5%
for an IQR. "After" is the band once capped. **No median is capped:** the nearest named wrong answer is
always at least twice the band away. **The IQR is capped in 8 of 10 plots.** In B7 and B10 the two IQRs
are equal, and the ranges are far away.

| Scenario | Drawn axis | Median A / B | IQR A / B | Before: median / IQR | Band: median / IQR | After: median | After: IQR (pixels) | The other group's IQR is accepted? |
|---|---|---|---|---|---|---|---|---|
| B1 | 52.8 | 46 / 52 | 16 / 18 | ±2 / ±2 | ±1.32 / ±2.64 | ±1.32 | ±1 (9.5 px) | before yes, band yes, **after no** |
| B2 | 210 | 110 / 125 | 65 / 60 | ±2 / ±2 | ±5.25 / ±10.5 | ±5.25 | ±2.5 (6.0 px) | band yes, **after no** |
| B3 | 43.2 | 28 / 33 | 12 / 14 | ±2 / ±2 | ±1.08 / ±2.16 | ±1.08 | ±1 (11.6 px) | before yes, band yes, **after no** |
| B4 | 80.4 | 32 / 40 | 18 / 22 | ±2 / ±2 | ±2.01 / ±4.02 | ±2.01 | ±2 (12.4 px) | band yes, **after no** |
| B5 | 390 | 175 / 210 | 80 / 110 | ±2 / ±2 | ±9.75 / ±19.5 | ±9.75 | ±15 (19.2 px) | no |
| B6 | 216 | 115 / 140 | 55 / 60 | ±2 / ±2 | ±5.4 / ±10.8 | ±5.4 | ±2.5 (5.8 px) | band yes, **after no** |
| B7 | 2880 | 1950 / 2150 | 700 / 700 | ±2 / ±2 | ±72 / ±144 | ±72 | ±144 (25 px), uncapped | equal IQRs: it is the key |
| B8 | 38.4 | 38 / 40 | 8 / 9 | ±2 / ±2 | ±0.96 / ±1.92 | ±0.96 | ±0.5 (6.5 px) | before yes, band yes, **after no** |
| B9 | 270 | 420 / 400 | 80 / 85 | ±2 / ±2 | ±6.75 / ±13.5 | ±6.75 | ±2.5 (4.6 px) | band yes, **after no** |
| B10 | 2640 | 1600 / 1800 | 800 / 800 | ±2 / ±2 | ±66 / ±132 | ±66 | ±132 (25 px), uncapped | equal IQRs: it is the key |

**For Jon: B9's IQR is now ±2.5, which is 4.6 px on screen,** about ±2.3 px on each box edge. The two IQRs
(80 and 85) differ by 5 on a 270-unit axis, so the cap leaves nothing wider without accepting the
other box. An accurate reader passes; a rough one may not. That trade-off is the ruling's, stated
here so it is seen.

**Histograms (30): unchanged, outside 1.16.** All ten scenarios (H1–H10) are marked as follows, before
and after:
- class frequency ±1;
- sample total ±1;
- proportion ±2 percentage points.

Contract B's step 2 showed that none of these can fail an accurate reader.

## Found while building: the box-plot IQR window (resolved by ruling 2)

**Under the uncapped band (PR 39's first commit), 7 of 10 box plots accepted the other group's IQR,**
against 3 of 10 under the old ±2. Jon's ruling 2 caps the band. Those 7 plots (B1, B2, B3, B4, B6, B8,
B9) now reject it, and the verifier proves it. Run against PR 39's first commit, the verifier fails
165 checks, among them each of the 7 plots' "named wrong answer was accepted".

## 1.18: the sentences, before and after

| Scenario | Before | After |
|---|---|---|
| CF5 | The median hours is approximately 38. … Approximately 25% of workers have a hours below Q1 (33). | The median number of hours is approximately 38. … For approximately 25% of workers, the number of hours is below Q1 (33). |
| CF8 | The median hours is approximately 38. … Approximately 25% of employees have a hours below Q1 (33). | The median number of hours is approximately 38. … For approximately 25% of employees, the number of hours is below Q1 (33). |
| CF1 (as all singular ones) | Approximately 25% of students have a score below Q1 (34). | For approximately 25% of students, the score is below Q1 (34). |
| S4 | What is the median hours for Full-time? … so the typical hours is higher for Full-time. | What is the median number of hours for Full-time? … so the typical number of hours is higher for Full-time. |
| B8 | What is the median hours for Region A? … so the typical hours is higher for Region B. | What is the median number of hours for Region A? … so the typical number of hours is higher for Region B. |
| S8 | What is the median earnings for Apprentices? … so the typical earnings is higher for Graduates. | What are the median earnings for Apprentices? … so the typical earnings are higher for Graduates. |

**Only the 25% sentence changes in the other eight cumulative-frequency scenarios.** It now reads "For
approximately 25% of {population}, the {noun} is below Q1 (v)".
- Dropdown options and keys are unchanged.
- The sentence frames of the other 37 scenarios are byte-identical to `main`.

## Verification

All checks were run in a cloud sandbox per `docs/sandbox-checks.md`, against a worktree of `origin/main`
(`527c612`) served the same way, with a seeded `Math.random`.

- **Comparison with `main`: 460 assertions, 0 failures, over all 40 scenarios.** Each scenario was driven
  through the game's own functions (`drawDiagram`, `buildPhase1Questions`, `showPhase2`, `showModelAnswer`),
  and the following were checked against `main`:
  - **Drawing:** pixel-identical (canvas data URL; stem-and-leaf table HTML).
  - **Keys:** every Phase 1 key, multiple-choice option set and Phase 2 dropdown key is identical.
  - **Tolerances:**
    - box plots equal 2.5% / 5% of the independently computed axis;
    - stem and leaf is half the table's precision;
    - cumulative frequency and histograms are identical to `main`.
  - **Text:** Phase 1 question text, Phase 2 HTML and the model answer equal `main`'s with only the frame
    rewrites above applied, and nothing else differs.
- **`scripts/verify-chart-interrogator.py`** (new, not yet in CI): 604 checks and 444 marking cases
  through `submitPhase1()`, **0 failures.**
  - It reads the scenario data off the page and recomputes every box-plot and stem-and-leaf key and
    tolerance in exact arithmetic.
  - It checks that no tolerance reaches a named wrong answer.
  - It types, through the game's own input:
    - the key (and, for stem and leaf, the key with a trailing zero), which must be accepted;
    - every named wrong answer, which must be rejected;
    - for stem and leaf, the key rounded to the table's precision, which must be rejected;
    - for box plots, the key ± 0.999 of the tolerance (must be accepted) and ± 1.001 (must be rejected).
  - It is regression-proven: against PR 39's first commit it fails 165 checks.
  - Run it with `--chromium /opt/pw-browsers/chromium` in a cloud sandbox.
- **The 493 marking cases of PR 39's first commit, replayed on the final code.**
  - **No exact key is lost, and nothing newly accepted.**
  - 128 cases accepted before are rejected now:
    - **Stem and leaf, 96, all by ruling 1 (exact marking):**
      - 80 probes at ± 0.999 of the old ±0.5 / ±0.05;
      - 12 keys rounded to the table's precision;
      - S1's median 35.5 typed as 35 and as 36;
      - S3's range 2.4 typed as 2.35 and as 2.45.
    - **Box plots, 32, all IQR probes at ± 0.999 of the 5% band,** in B1, B2, B3, B4, B5, B6, B8 and
      B9: two per IQR, four per plot.
      - Each sits 25 px from the key, the edge of the uncapped band.
      - Each is further from the key than half the gap to the other group's IQR.
      - No median case and no exact reading is lost.
- **Comparison with `main`, rerun on the final code: 300 assertions, 0 failures.** Drawings, keys,
  option sets and text are unchanged apart from the 1.18 frames. Tolerances are left to the
  verifier.
- **Start-up from URL:** all 16 `?type=…&level=…` combinations start a scenario with no page error. For
  example, `stemleaf&core` opens on S8's "What are the median earnings for Apprentices?".
- **`check-site.py --only game:chart-interrogator`:** tier 1 PASS (9 of 9 loads), tier 2 PASS, network
  guard 0 escaped.
- **Tier 3 (`--tier 3 --only game:chart-interrogator`):** 0 PASS, 0 FAIL, 0 WARN, 5 UNSUPPORTED, identical
  on `main`. The game opens on its menu, so tier 3 finds no option group.
- **Tier 4 layer A:** `extract-banks.py --only chart-interrogator`, then `check-banks.py --ci --only
  chart-interrogator`: OK, matches the ledger exactly.
- **`check-leaderboard-coverage.js`:** OK.
- **`--live` checked 1 Oct 2026, from Claude Code at home:** the live page served the new build (all three PR 39/41/42 markers present); `check-site.py --live --only game:chart-interrogator` gave `tier 1: 9 PASS, 0 FAIL, 0 WARN (of 9 loads)`, network guard `escaped 0`, `OK`. Local `verify-chart-interrogator.py`: 1490 checks, 844 marking cases, 0 failures; all 8 self-test faults caught. Recorded in todo §1.16.

## 1.8: held, and why

**The ruling (29 Sep):** "most common range" is true iff the interval is the modal class (highest
frequency density).

**Applied to all ten histograms, that rule changes no key.** The interval Phase 2 asks about is always
the fourth class.

| Scenario | Asked interval (share) | Modal class, highest fd | Highest frequency | Key now | Key under the ruling |
|---|---|---|---|---|---|
| H1 | 50–60 (30.9%) | 50–60 | 50–60 | most common | most common |
| H2 | 170–180 (28.0%) | **165–170** (fd 6.0; 170–180 is 4.0) | **170–180** (40) | typical | not "most common" |
| H3 | 25–30 (21.9%) | 20–25 | 20–25 | typical | not "most common" |
| H4 | 35–40 (17.0%) | 30–35 | 20–30 | typical | not "most common" |
| H5 | 40–50 (21.6%) | 35–40 | 25–35 | typical | not "most common" |
| H6 | 300–350 (21.3%) | 250–300 | 250–300 | typical | not "most common" |
| H7 | 80–100 (19.4%) | 60–80 | 60–80 | typical | not "most common" |
| H8 | 40–45 (15.9%) | 30–40 | 30–40 | typical | not "most common" |
| H9 | 500–600 (26.7%) | 400–500 | 400–500 | typical | not "most common" |
| H10 | 25–30 (19.8%) | 20–25 | 20–25 | typical | not "most common" |

**1.8's premise was that 170–180 is H2's modal class. It is not, by the ruled definition:** it has the
highest *frequency* (40 of 143), but 165–170 has the highest *density*. So the ruling keeps H2 on
"typical", which is exactly the complaint 1.8 was filed for.

**Neither reading can be built as contracted:**
- **Highest frequency** would flip H2 to "most common range" while 165–170 is visibly the tallest bar.
  That contradicts the picture and the GCSE definition of modal class (a STOP IF).
- **The ruling also does not decide** how "typical for the population" and "relatively few observations"
  split. Today that split is a share above 15%.

**What is actually wrong is the wording.** The same Phase 2 sentence opens "The class interval with the
highest frequency is 170–180", then asks whether 170–180 is "the most common range". To a student,
"most common" reads as highest frequency. Re-filed in todo §1.8 for a content contract.

**Ruled 1 Oct 2026 (Jon):** reword the item as a modal-class question ("170–180 contains the most
people. Is it the modal class?"), keyed on highest frequency density, with an explanation that names
frequency against frequency density, in every histogram where class widths differ (all ten). It is
drafted in a follow-up PR and is not merged until Jon approves the wording. **Jon approved it the same day, with three additions, and it merged as PR 41** (below).

**Built and merged 1 Oct 2026 (PR 41), with Jon's three additions:**
- **The question is general.** "[class] contains N [people]. Is it the modal class?" is keyed on frequency density.
- **Which class is named** comes from the scenario's `ask` (`most`, `modal` or `wide`), so the keys split 5 Yes / 5 No without changing data.

| Scenario | Named class (how chosen) | Count | Its fd | Modal class | Key |
|---|---|---|---|---|---|
| H1 | 50–60 (most) | 50 | 5.0 | 50–60 | Yes |
| H2 | 170–180 (most) | 40 | 4.0 | 165–170 | No |
| H3 | 20–25 (most) | 30 | 6.0 | 20–25 | Yes |
| H4 | 20–30 (most) | 40 | 4.0 | 30–35 | No |
| H5 | 35–40 (modal) | 30 | 6.0 | 35–40 | Yes |
| H6 | 250–300 (most) | 120 | 2.4 | 250–300 | Yes |
| H7 | 100–200 (wide) | 50 | 0.5 | 60–80 | No |
| H8 | 0–20 (wide) | 16 | 0.8 | 30–40 | No |
| H9 | 400–500 (most) | 400 | 4.0 | 400–500 | Yes |
| H10 | 10–20 (wide) | 25 | 2.5 | 20–25 | No |

- **The most-observations option** is offered only when true of the named class, and is never keyed.
- **On H1, H3, H6 and H9** that option is the right answer for the wrong reason. Choosing it gives "Right answer, wrong reason." and the explanation.
- **`scripts/verify-chart-interrogator.py` checks the item for every class of every histogram, and is in CI.** A choice of named class can therefore never key two options, or key anything but frequency density.

## 1 Oct 2026, later: H4 data (todo 1.15) and cumulative frequency against canon §7.1.2

**H4.** The 35–40 class was frequency density 4.5 × width 5 = 22.5 employees, total 132.5. It is now
**4.6**: 23 employees, total 133.
- **Why 4.6, not 4.4:** the contract's first choice, 4.4 (22, total 132), would have changed the "sample
  altogether" key from 133 to 132, so by the contract's rule 4.6 was used.
- **Every H4 key is unchanged,** read from the game before and after: highest-frequency class 20–30,
  frequency 30, total 133, proportion 17%, and Phase 2 "No" (the modal class is 30–35).

**Cumulative frequency.** Each band is capped by `capTol()`. The named wrong answers are:
- for a quartile, the other two quartiles and its own position (n/4, n/2, 3n/4);
- for the IQR, the position difference n/2 and the axis range;
- for the benchmark count, its complement, n − count.

| Scenario | Q1 / median / Q3 band | IQR band | Count band | Capped (before → after) |
|---|---|---|---|---|
| CF1 | ±2 | ±4 | ±2 | none |
| CF2 | ±1.75 | ±3.5 | ±1.5 | none |
| CF3 | ±2 | ±4 | ±2.5 | none |
| CF4 | ±1.5 | ±3 | ±3 | none |
| CF5 | ±1.5 | ±3 | ±2 | **median ±1.5 → ±1.047** (8.6 px): median 37.905, n/2 = 40 is 2.095 away |
| CF6 | ±7.5 | ±15 | ±2.5 | none |
| CF7 | ±40 | ±80 | ±2.25 | none |
| CF8 | ±1 | ±2 | ±2.75 | none |
| CF9 | ±0.25 | ±0.5 | ±2 | none |
| CF10 | ±0.3 | ±0.6 | ±2.5 | none (median 50.773 is 0.773 from n/2 = 50; half that, 0.386, is above ±0.3) |

**Results:**
- **No band admitted a named wrong answer** before the change.
- **No correct reading is lost:** all 30 of Contract B's pixel-measured readings of the drawn curve still
  pass. CF5's is 37.904, against a key of 37.905.
- **The verifier** recomputes every key from the Bezier curve the game draws, then marks each key,
  every named wrong answer and the band edges: through `submitPhase1()` for the readings, and through
  `submitPhase2()` for the count.

**Verifier totals:** 1,490 checks and 844 marking cases, 0 failures. Eight injected faults, all caught,
including CF5's median left uncapped and H4 put back to 22.5.

**`--live` checked 1 Oct 2026, from Claude Code at home:** the live page served the new build (all three PR 39/41/42 markers present); `check-site.py --live --only game:chart-interrogator` gave `tier 1: 9 PASS, 0 FAIL, 0 WARN (of 9 loads)`, network guard `escaped 0`, `OK`. Local `verify-chart-interrogator.py`: 1490 checks, 844 marking cases, 0 failures; all 8 self-test faults caught.
