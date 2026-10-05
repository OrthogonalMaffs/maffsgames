# Quoted statistics audit: working notes (phase 1 in progress)

Scratch record of each search, so a context clear loses nothing. The report is
`docs/audits/quoted-statistics-2026-10.md`; this file is folded into it (or deleted) when phase 1 is reported.

Rulings (Jon, 5 Oct 2026 18:10): scope (b). Phase 1 = every real-world figure a student is marked against.
VERIFIED = a WebSearch result naming its source URL. Fermi modelling guesses OUT; references a hint states
as fact IN; constants IN where keyed; Estimation Golf general knowledge OUT; maths-history dates IN only if keyed.

Status key: VERIFIED (source agrees within the item's green band), CONTRADICTED (source outside the green
band, or the stated figure is materially wrong), UNVERIFIABLE (no source found naming the figure),
COMPUTED (definition or arithmetic, no search needed).

## Fermi Lab (format: item.step | keyed ref | source figure | URL | status)

- uk-bread-slices.s1, uk-tea-daily.s1, uk-cars.s1, uk-energy-daily.s1 | UK population 67,000,000 | 69,281,400 mid-2024 | https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/bulletins/annualmidyearpopulationestimates/mid2024 | VERIFIED (ratio 1.03)
- uk-classrooms.s1 | UK schools 32,000 | 32,095 (2018/19, UKETS); England 24,479 Jan 2025 | https://dera.ioe.ac.uk/34616/1/UKETS_2019_Main_text.pdf ; https://explore-education-statistics.service.gov.uk/find-statistics/school-pupils-and-their-characteristics/2024-25 | VERIFIED
- uk-school-meals.s1 | UK pupils 10,000,000 (note: 10.6M "DfE 2024") | 10.7M 2022/23 (10.6M 2021/22) | https://explore-education-statistics.service.gov.uk/find-statistics/education-and-training-statistics-for-the-uk/2023 | VERIFIED (note's year label is off: 10.6M is 2021/22)
- piano-tuners-london.s1 | London 9,000,000 | 8.945M mid-2023 | https://data.london.gov.uk/dataset/londons-population-e6y30 | VERIFIED
- piano-tuners-london.s2, uk-cars.s2 | household size 2.4 | 2.36 (2022) | https://www.statista.com/statistics/295548/ (ONS series) | VERIFIED
- uk-milkmen-pints.s1 | households 28,000,000 | 28.6M (2024) | https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families/bulletins/familiesandhouseholds/2024 | VERIFIED
- uk-cars.ANS | 33,000,000 cars ("DVLA 2024") | 34.49M cars licensed end Dec 2024 (RAC Foundation from DfT VEH) | https://www.racfoundation.org/?p=205 ; https://www.gov.uk/government/statistics/vehicle-licensing-statistics-2024/vehicle-licensing-statistics-united-kingdom-2024 | VERIFIED (ratio 1.05)
- uk-trees.s2 | woodland fraction 0.13 | 13.5% (31 Mar 2024) | https://www.forestresearch.gov.uk/tools-and-resources/statistics/forestry-statistics/forestry-statistics-2024/2024-1-woodland-area-and-planting | VERIFIED
- uk-trees.ANS | 3.2 billion trees ("Forestry Commission") | search 1 found no source naming the figure | - | pending
- uk-trees.ANS | 3.2 billion trees ("Forestry Commission") | ~3 billion (aerial-photo estimate, Plant for the Planet method); others 3.5bn; no Forestry Commission source for 3.2bn found | https://www.woodlands.co.uk/?p=42307 | VERIFIED as an order of magnitude (ratio 1.07); the attribution is UNVERIFIABLE
- uk-trees.s1 | UK area 243,000 km² | 243,610 km² | https://www.cia.gov/the-world-factbook/about/archives/2023/countries/united-kingdom | VERIFIED
- uk-bread-slices.ANS note | Federation of Bakers "~11 million loaves per day" | "around 11 million" (older FoB); now "over 13 million loaves and bakery packs" | https://fob.uk.com/ | VERIFIED (dated; FoB now says 13M). Key 73bn is the chain product; note says ~80bn
- uk-tea-daily.ANS | 100,000,000 cups/day (UKTIA) | "over 100 million cups of tea each day" (UKTIA) | https://tea.co.uk/news/article/tea-loved-by-brits-and-5-billion-cups-of-tea-are-drunk-globally-each-day | VERIFIED
- lifetime-heartbeats.s3, food-lifetime-kg.s3, blood-pumped-lifetime.s4 | life expectancy 80 | 78.8 M / 82.8 F (2021-23) | https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/lifeexpectancies/bulletins/nationallifetablesunitedkingdom/2021to2023additionaldata | VERIFIED
- lifetime-heartbeats.s1, blood-pumped-lifetime.s2 | 72 bpm ("typically 60-80") | normal adult resting 60-100 bpm | https://healthdirect.gov.au/resting-heart-rate | VERIFIED (72 inside the range; the hint's 60-80 is narrower than the clinical 60-100)
- lego-bricks-year.ANS | 60,000,000,000 ("Lego Group reports approximately 60 billion") | ~36 billion elements a year (31bn in 2010) | https://en.wikipedia.org/wiki/Lego | CONTRADICTED (key 1.67x the source; a student giving 36bn still rates Brilliant, factor <= 2)
- hp-words.s1 / s2 / ANS | 7 books; 155,000 avg; 1,084,170 total | 1,084,170 total (per-book counts listed) | https://wordcounter.net/blog/?p=922 | VERIFIED (155,000 = 1,084,170 / 7, COMPUTED)
- tennis-balls-classroom.s2 | 157 cm³ (6.7 cm ball) | ITF diameter 6.54-6.86 cm | https://www.itftennis.com/media/4420/2023-technical-booklet.pdf | VERIFIED (sphere of 6.7 cm = 157.5 cm³, COMPUTED)
- tennis-balls-classroom.s3 | packing 0.64 | random close packing 0.6366 | https://arxiv.org/abs/1305.1032v2 | VERIFIED
