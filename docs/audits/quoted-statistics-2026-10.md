# Quoted real-world statistics audit (October 2026)

**Status: phases 1 and 2 done; fixes merged 7 Oct 2026 (PRs #91 Fermi Lab, #92 Screening Room, #93 Core Maths Paper 1); `scripts/check-quoted-figures.py` (PR #94, CI) fails if any CONTRADICTED old value returns to its page.** The original report follows. No game, bank, check script or canon was changed. Phase 1 (below) is
every real-world figure a student is marked against; phase 2 (the last section) is Screening Room's real-world rates
and the real-year CPI/inflation figures, which are stated, not keyed.

**Scope (Jon's rulings, 5 Oct 2026 18:10):** (b). Phase 1 covers every real-world figure a student is marked against.
- Fermi modelling guesses are OUT; references a hint states as fact are IN.
- Constants are IN where keyed.
- Estimation Golf's general knowledge is OUT (already ruled for replacement).
- Maths-history dates are IN only if keyed.
- VERIFIED means a WebSearch result naming its source URL, recorded per figure.
- No 150 cap.

**Per-figure record:** `docs/audits/quoted-statistics-2026-10-ledger.md` (119 lines covering about 140 keyed values;
one line can cover several items that share a figure, such as UK population in four items).

| Status | Ledger lines |
|---|---|
| VERIFIED (source agrees within the item's band) | 94 |
| CONTRADICTED (key or stated figure outside the band, or materially wrong) | 11 |
| UNVERIFIABLE (no source names the figure) | 11 |
| COMPUTED (definition or arithmetic) | 3 |

Plus 7 modelling statements a hint words as fact, listed as NOT SEARCHED (no public statistic exists for them).

**How Fermi Lab scores** (`games/fermi-lab/index.html`): each chain step is green (15 points), amber (8) or red (2)
against a factor band around its `reference` (`withinFactor`). The final estimate rates Brilliant (factor up to 2,
20 points), Good (up to 5, 10), Reasonable (up to 10, 5) or Poor (0) against `acceptedAnswer`.

## Already fixed

- **STOP 2:** `eq_sleep_loss` and `eq_homework` (GCSE cohort 300,000 / 600,000) are fixed by **PR #64**. One figure
  (`FIG.gcseCohortEngland`, 600,000 per year group, DfE KS4 2024/25: 625,673) is now read by both items.
- **52-dle:** "52! … more than atoms in the observable universe" is fixed by **PR #64** (now "more than the number of
  atoms in the Earth (about 10⁵⁰)").

- **PR #91 (Fermi Lab, 7 Oct 2026)** fixes every Fermi Lab item in §1 and §2 except `m25-concrete`'s depth hint (its
  key is VERIFIED), plus the cohort strings. Each corrected figure is a `FIG` entry with its source, and the hint or
  note that states it is built from the stored value. The same PR found that **19 of 65 Fermi chains never multiplied
  to their own key** (a step changed unit), so typing every reference rated Poor or Good. All 19 are fixed by data
  (Jon, 7 Oct 2026), including `molecules-swimming-pool`, which was keyed 1,000 times too small.
  `scripts/verify-fermi-lab.py` checks every chain in Chromium and every figure against its source. Rows below
  marked **Fixed (PR #91)**.

- **PR #92 (Screening Room, 7 Oct 2026)** fixes the six phase 2 rates. Each is a `SOURCES` entry with its source, and
  every count, answer and figure is computed from the stated rates (`scripts/verify-screening-room.py`). Rows marked
  **Fixed (PR #92)**.

- **PR #93 (Core Maths Paper 1, 7 Oct 2026)** fixes the CPI pair: 9.1% (2022) and 7.3% (2023), the ONS annual averages,
  stored with the source; key £111.21. `verify-core-maths-paper1.py` checks the rates against ONS.

## 1. Contradicted keyed figures: a student with the true figure loses marks

| Item | Keyed figure (wording) | Source figure | Effect of entering the true figure |
|---|---|---|---|
| `fermi-lab` `eq_school_trip` s2 **Fixed (PR #91)** | 12.8 L per coach for 160 km. Hint: "A coach uses about 8 litres per 100 km" | Diesel coaches use 19-24 L/100 km; a Scania Touring did 18.2 in a test ([Scania](https://scania.com/group/en/home/newsroom/news/2017/scania-touring-excels-in-fuel-consumption.html), [IRU](https://www.iru.org/sites/default/files/2016-06/Factsheet_-_environment.pdf)). True: 29-38 L | Step: **amber, not green** (ratio 2.3-3.0). Final estimate with true fuel and the Sept 2026 diesel price (£174-£229) rates **Good, not Brilliant** against the key £61.44 |
| `fermi-lab` `uk-texts-per-day` answer **Fixed (PR #91)** | 120,000,000 SMS a day ("Ofcom: roughly 100-150 million SMS/day in recent years") | 6.4 billion SMS in 2023 = 17.5 million a day person-to-person ([Statista, Ofcom data](https://www.statista.com/statistics/288581/uk-mobile-network-quarterly-sms-and-mms-message-volumes)); plus about 55 million a day of business (A2P) texts ([ISPreview](https://www.ispreview.co.uk/index.php/2025/01/ofcom-uk-propose-to-cap-the-wholesale-price-of-bulk-business-texts.html)) | Person-to-person figure: **Reasonable (5 points), not Brilliant (20)**, factor 6.9. Counting business texts as well: Brilliant (1.67). The question says "text messages (SMS) sent", so which count it means needs Jon's call |
| `fermi-lab` `uk-energy-daily` s2 **Fixed (PR #91)** | 5 kW per person | UK final energy consumption 2024: 128.1 mtoe = 1,490 TWh ([DESNZ ECUK 2025](https://www.gov.uk/government/statistics/energy-consumption-in-the-uk-2025/energy-consumption-in-the-uk-ecuk-2025)) / 69.3M people / 8,760 h = **2.45 kW** | Step: **amber, not green** (ratio 2.04 against a green band of 2). The answer 8 billion kWh a day is 1.96x the source's 4.08 (still Brilliant, just) and 1.8x the item's own note ("~4.4 TWh/day") |
| `fermi-lab` `eq_packed_lunch` s1 **Fixed (PR #91)** | 500 of 1,000 bring a packed lunch ("About half") | England secondary 2023: **17%** packed lunch, 57% school meals 4+ days a week, 26% a mixture ([ParentPay report](https://www.parentpay.com/cypad/wp-content/uploads/sites/7/2023/02/ParentPay-School-Meals-Report-England-DIGITAL-FINAL.pdf)) | 17%: step **amber**, answer **Good, not Brilliant**. Counting half the mixed group (~30%): green. Contradicted either way: half is not the figure |

## 2. Wrong figures in hints and notes, key unaffected (within the band)

| Item | Stated as fact | Source | Why the score is unaffected |
|---|---|---|---|
| `football-pitches-m25` s1 hint **Fixed (PR #91)** | "a rough circle about 30-40 km across" | Circumference 195.5 km, greatest radius from central London 20 miles ([Wikipedia](https://en.wikipedia.org/wiki/M25_motorway)): about 60 km across | The key (2,500 km²) is plausible. **The hint misleads**: a 35 km circle is 962 km², which scores **amber** |
| `lego-bricks-year` note **Fixed (PR #91)** | "Lego Group reports producing approximately 60 billion bricks per year" | About 36 billion elements a year ([Wikipedia](https://en.wikipedia.org/wiki/Lego)) | 36bn rates Brilliant (factor 1.67) |
| `aircraft-rivets` note **Fixed (PR #91)** | "Boeing states a 747 contains approximately 3 million rivets" | 3 million **fasteners**, about half of them rivets ([CS Monitor](https://www.csmonitor.com/1997/1029/102997.us.us.2.html)) | 1.5M rates Brilliant (factor 2.0, on the boundary) |
| `eq_coffee_cups` s1 hint **Fixed (PR #91)** | "About 65% of 300,000 are adults" | Under-18s are about 22% of the population, so adults about 78% ([UNICEF](https://data.unicef.org/how-many/how-many-children-under-18-are-there-in-the-uk/)) | 234,000 vs 195,000 is ratio 1.2: green |
| `ball-bearings-global` s2 hint **Fixed (PR #91)** | "A car has 20-30 bearings" | 100-150 in a conventional car, at least 36 ([NTN-SNR](https://www.ntn-snr.com/pt/blog/how-many-bearings-are-there-car)) | The step's key (10 per device across all devices) is a modelling guess, out of scope |
| `london-bus-annual-km` s3 hint **Fixed (PR #91)** | "London buses run every day of the year" | No TfL buses on Christmas Day ([Time Out](https://www.timeout.com/london/travel/everything-you-need-to-know-about-public-transport-in-london-over-the-festive-period)) | 364 vs 365 |
| `m25-concrete` s3 hint | "Motorway surfacing is typically 0.3-0.5m deep" | Heavy-traffic asphalt 180-360 mm ([spec](https://www.contractsfinder.service.gov.uk/Notice/Attachment/2828a5fe-a4e9-4538-ab73-5ce435a17794)) | Key 0.3 m is right; only the 0.5 m upper end overstates |

## 3. Keys that disagree with their own note (all inside the Brilliant band)

The answer note quotes a sourced figure, and the key is the chain product instead. A student who looks up the quoted
figure still rates Brilliant, but only just in two cases:

| Item | Key | Note's figure (verified) | Factor |
|---|---|---|---|
| `uk-energy-daily` **Fixed (PR #91)** | 8.0 billion kWh/day | 4.4 TWh/day (source: 4.08) | 1.8-1.96 |
| `internet-data-daily` | 25 billion GB/day | Cisco 396 EB/month = 13.2 billion GB/day (a 2018 forecast for 2022) | 1.89 |
| `food-lifetime-kg` | 58,000 kg | "~35 tonnes" ([Scientific American](https://www.scientificamerican.com/article/the-amount-of-food-consumed-by-a-ma/)) | 1.66 |
| `london-bus-annual-km` | 90,000 km | ~55,000 km (TfL: 490M bus-km / 8,776 buses = 56,000) | 1.61 |
| `uk-bread-slices` | 73 billion slices | "~80 billion/year" (Federation of Bakers: 11M loaves/day, now 13M) | 1.1 |

## 4. Unverifiable

No source names these figures. Each is in the ledger with what was found instead.
- **`uk-trees` answer:** 3.2 billion "Forestry Commission". About 3 billion found (aerial-photo estimate); the
  attribution was not found.
- **`grass-blades-pitch` s2:** 70,000 blades/m². Only secondary estimates found (32,000-54,000), which would score
  amber.
- **`uk-milkmen-pints` answer:** Milk & More at "~500,000 households". Milk & More's own figure is 110M pints a year.
- **`ball-bearings-global` answer:** 150 billion balls. Found "18 billion bearings" a year, with balls not counted.
- **`uk-photos-daily` answer:** 165M a day. Sources disagree (47M-133M).
- **`school-water-year` note:** "Waterwise 4-8 m³". Water-company audits say 2.1-11 m³.
- **`school-water-year` s1:** 1,200 people. No per-school average found.
- **`eq_sleep_loss` s2:** 1 hour lost per night.
- **`eq_canteen` s2:** 400 g a meal (the DfE portion guide's parts sum to about this).
- **`uk-trees` s3:** 200-400 trees per hectare. Only planting densities found.
- **`eq_textbooks` s4:** 500 g textbook. Only US hardcovers found, at 0.9-2.7 kg; 1.4 kg or more would score
  amber.

## 5. Dated figures (correct now, will go stale)

- **`higher-power` `gcse_34`:** largest Mersenne exponent 136,279,841 (M52, 12 Oct 2024). Still the record as of
  Sep 2026 ([GIMPS](https://www.mersenne.org/primes/?press=M136279841)). It is keyed, so it becomes wrong when M53 is
  found. **Review-by note added to todo.**
- **`fermi-lab` `eq_school_trip` s4:** diesel at £1.60/L. RAC put it at 188.63p on 9 Sep 2026 and 199.18p on 30 Sep
  2026; ratio 1.24 is still green.
- **Fermi notes citing a year or a past forecast:** `uk-cars` ("DVLA 2024": 34.49M), `internet-data-daily` (a Cisco
  forecast for 2022), `uk-bread-slices` (FoB "11M loaves", now "over 13M").

## 6. Verified, by game

- **`fermi-lab`:** every other keyed fact step and sourced answer in the ledger (UK, London and world population;
  households; schools; pupils; area; woodland; the 747, Eiffel Tower, Forth Bridge and Astute figures; constants;
  distances; and so on).
- **`higher-power`:** all 11 keyed real-world values. The speed of light and absolute zero are exact by definition;
  the others are the Moon, the Sun, the speed of sound, Earth's radius, world population, the Mersenne exponent,
  atoms in the universe, g, and the year's length.
- **`estimation-golf`:** the speed of sound (343 m/s at 20°C), the one keyed constant outside the general knowledge
  ruled out.
- **`probability-paradox`:** the hot-hand answer ("It's debated — recent research suggests a small effect may
  exist"), a keyed research claim, matches Miller & Sanjurjo (Econometrica 2018).
- **`52dle`:** no keyed real-world figure beyond definitions (52 cards, 7 days).
- **`truth-buster`:** answers are true/false verdicts on mathematical statements. Dates appear only in reveal text,
  so none is keyed (OUT).

## 7. Out of scope under scope (b) (stated, not keyed: not audited)

These games give a real-world figure in the question and mark only the arithmetic, so a wrong figure cannot cost a
student marks:
- `standard-form-blitz`, `word-problem-decoder`, `spot-the-error` and `equation-builder`: Sun distance, proton mass,
  hair and atom widths, Earth and Moon masses, Proxima Centauri.
- `unit-converter`: conversion factors, all stated.
- `curling-friction`, `suvat` and `moments-master`: g is given.
- `better-value`: city rents.
- `chart-interrogator` CF4: "National median = £28k".
- `correlation-or-coincidence`: axis labels.

Fermi modelling guesses (slices of bread a day, the fraction of households with a piano, …) are out by ruling.

## 8. Found on the way (not real-world figures; reported, not fixed)

- **`truth-buster` `tb_t3_016`: "Every even number greater than 2 can be written as the sum of two primes" is keyed
  `false`.** Goldbach's conjecture is unproven, not false; the reveal itself says it is verified up to 4×10¹⁸. A
  student who answers "true" is marked wrong for a statement no one has refuted. It needs Jon's ruling: reword the
  statement (e.g. "…has been proved") or remove the item.
- **`fermi-lab` `uk-school-meals` note:** "~10.6 million pupils (DfE 2024)". 10.6M is the 2021/22 UK figure;
  2022/23 is 10.7M.
- **`fermi-lab` `brain-neurons` note:** "Herculano-Houzel (2009)". The first author is Azevedo (Herculano-Houzel is
  the senior author).
- **The two Fermi items that share the UK population** (67M in four items) and household size (2.4 in two) each
  state it separately. They agree today; they are the next candidates for `FIG` (PR #64's class fix).

## Method

- **Population:** every bank in `data/banks/` (regenerated by `scripts/extract-banks.py` on 5 Oct 2026, 97 games).
  Two passes:
  - A keyword net over 40 data-heavy banks, read by hand.
  - Full reads of `fermi-lab` (65 items, 189 steps), `higher-power`, `estimation-golf`, `52dle` and `truth-buster`.
- **Fermi coverage:** a script listed every one of the 189 steps not yet in the ledger, and each was classed as a
  given value, a computation, a modelling guess, or a hint-stated fact (which was then searched). The ledger records
  every step that is IN.
- **Effects** were computed from each step's own `tolerance` and the game's `getLight` / `getFinalRating` rules.
- **Network:** WebSearch for every figure (standard mode; extended once, for the Mersenne record). WebFetch was not
  needed.

## Phase 2: Screening Room's real-world rates and real-year CPI

These figures are **stated, not keyed**: Screening Room computes every answer from the rates its scenario states,
and the CPI questions do arithmetic on the rates given. A wrong figure never marks a student wrong. **It teaches a
wrong fact**, and in Screening Room the size of the rate is the whole lesson (the positive predictive value moves
with it).
- **In scope (Jon's ruling, "Screening Room's sample rates"):**
  - every base rate that reads as a real prevalence: 20 of the 70 scenarios;
  - test accuracy credited to a real, named test or programme.
- **Out:** invented contexts (security gates, spam filters, engineering NDT, fraud, an "outbreak" sample, the people
  who take a pregnancy test).

| Item | Stated | Source | Status |
|---|---|---|---|
| `screening-room` `alevel_05` **Fixed (PR #92)** | NHS FIT: "sensitivity of 74%" | At England's programme threshold (120 µg/g) FIT finds **47.8%** of colorectal cancers; 74% matches a threshold near 40 µg/g ([PMC8366184](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8366184/)) | **CONTRADICTED** |
| `screening-room` `alevel_03` **Fixed (PR #92)** | "standard ELISA test" specificity **98.5%** | 4th-generation assays 99.81-99.97% ([aidsmap](https://aidsmap.com/node/9459)) | **CONTRADICTED**, and it drives the lesson: at 0.16% prevalence the PPV is about 10% at 98.5% but about 60% at 99.9% |
| `screening-room` `core_01` **Fixed (PR #92)** | NHS Health Check: HbA1c "correctly identifies **85%** of diabetics", flags 7% | HbA1c at 48 mmol/mol in a UK population: **61%** sensitive, 99% specific ([Oxford PHC](https://www.phc.ox.ac.uk/publications/1217970)) | **CONTRADICTED** |
| `screening-room` `alevel_15` **Fixed (PR #92)** | NHS AAA: "About **1.5%** have an aneurysm" | NHS detection 1.12% (2015-16), 0.92% (2019-20), ~0.74% (2023-24) ([AAA standards report](https://www.gov.uk/government/statistics/abdominal-aortic-aneurysm-screening-standards-report-2023-to-2024/aaa-standards-report-2023-to-2024--2)) | **CONTRADICTED** (about 2x) |
| `screening-room` `gcse_03` **Fixed (PR #92)** | colour blindness **8%** of 200 students | 8% of **males**, 0.5% of females; 4.5% of the UK overall ([Colour Blind Awareness](https://www.colourblindawareness.org/?p=21)) | **CONTRADICTED** for a mixed group (true only for boys) |
| `screening-room` `gcse_05` **Fixed (PR #92)** | **10%** of Year 7 "actually need glasses" | NICER: 14.6-17.7% of 12-13-year-olds are myopic alone ([PMC4718680](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4718680/)) | **CONTRADICTED** (low) |
| `core-maths-paper1` (3.2, AO2) **Fixed (PR #93)** | "CPI inflation: **8.7% in 2022, 6.3% in 2023**" | ONS CPI: annual average 9.1% (2022), 7.3% (2023); to December 10.5%, 4.0%. 8.7% was the April/May **2023** rate; no 2023 measure was 6.3% ([ONS](https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/consumerpriceinflation/december2023), [CIPP](https://www.cipp.org.uk/resources/news/uk-inflation-falls-to-8-7.html)) | **CONTRADICTED** (real years, wrong rates) |
| `wrong-on-the-internet` `woti_core_005` | "UK inflation in 2023 was 7.3%" | ONS annual average 2023: 7.3% | VERIFIED |
| `screening-room` `alevel_13` | NHS cervical screening: "The Pap smear" (sensitivity 70%, specificity 95%) | The accuracy figures match cytology meta-analyses; but **England's programme has used HPV primary testing since 2019** | VERIFIED but DATED |

**Verified, in the ledger:**
- hearing 3%; nut allergy 2%; dyslexia 10% (the BDA figure); scoliosis 3%; head lice 15% (inside the published
  range, high for the UK); strep 25% (true for children, high for a GP's mixed list);
- mammography 0.8% with sensitivity 87% (UK 86.6%; specificity 91% is at the low end);
- UK HIV 0.16%; lateral flow 80% and 99% (the best-case laboratory figure; field sensitivity was about half);
- COVID 0.2% in a low period; diabetes 8%; CF carriers 1 in 25; radon 7% "in certain parts"; meningitis 15% of
  suspected cases.

**Not checked separately** (listed in the ledger): bowel cancer 0.3% of 60-74s, prostate cancer 4% of men over 50,
the PCR accuracy, and cervical 0.6%.

## For Jon

1. **Phase 1, §1:** four contradicted keys that cost a student marks. Each is a fix contract of its own, like
   PR #64. The SMS item first needs a ruling: does "text messages (SMS)" include business texts?
2. **Phase 2:** six Screening Room rates and the core-maths CPI pair are wrong as stated facts. They are not keyed,
   so a fix is a wording change: correct the rate, or drop the claim that it is real ("In the NHS…",
   "CPI inflation in 2022…").
3. **§2:** the M25 hint misleads (it scores amber if followed). The other hint and note errors are cosmetic.
4. **§8:** Goldbach keyed `false` in `truth-buster`.
