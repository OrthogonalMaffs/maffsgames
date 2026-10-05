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
- lego-bricks-year.s1 | 2,000,000,000 children under 15 ("8 billion, a quarter under 15") | 25.77% aged 0-14 in 2024, about 2.07 billion | https://gitnux.org/global-population-statistics/ | VERIFIED
- hairs-on-head.s1 | scalp 650 cm² ("600-700") | 520-705 cm² clinical range; 774 cm² (120 sq in) also cited | https://library.scconline.org/v028n05/17 ; https://www.hairlosscure2020.com/how-many-hairs-are-there-on-a-human-head/ | VERIFIED (inside the clinical range)
- hairs-on-head.s2 | 150 hairs/cm² | mean terminal density 223/cm², range 175-300; other studies 124-200 | https://bionumbers.hms.harvard.edu/bionumber.aspx?id=116431 | VERIFIED as within published study ranges (low end; 223/150 = 1.49)
- hairs-on-head.ANS | 100,000 hairs | "on average 100,000" | https://healthline.com/health/how-many-hairs-on-a-human-head | VERIFIED
- pencils-london-edinburgh.s1 | 650 km by road | 414 miles / 662 km (some 400 mi / 647 km) | https://must-see-scotland.com/how-far-is-edinburgh | VERIFIED
- pencils-london-edinburgh.s2 | 56 km of line per pencil | "35 miles (56 km)" (a widely repeated trivia figure; no primary measurement found) | https://math.answers.com/math-and-arithmetic/How_many_miles_can_the_average_pencil_draw_a_line_for | VERIFIED (secondary sources only)
- walking-year.s1 | 5 km/h | average adult walking speed about 5 km/h | https://next-cms.climatetrace.org/how-fast-does-the-average-person-walk | VERIFIED (secondary summary of studies)
- footballs-on-pitch.s1, football-pitches-m25.s2, grass-blades-pitch.s1 | pitch 7,000 m² (100 x 70) | FIFA recommended 105 x 68 m = 7,140 m² | https://publications.fifa.com/fr/football-stadiums-guidelines/technical-guideline/stadium-guidelines/pitch-dimensions-and-surrounding-areas | VERIFIED
- footballs-on-pitch.s2 | size 5 ball 0.22 m | IFAB Law 2 circumference 68-70 cm = diameter 21.7-22.3 cm | https://downloads.theifab.com/downloads/laws-of-the-game-2000-01?l=en | VERIFIED
- school-water-year.s3, lessons-yr7-yr11.s2, eq_packed_lunch.s3, eq_bus_distance.s4 | 190 school days | maintained schools open at least 380 sessions (190 days) | https://dera.ioe.ac.uk/id/eprint/40093/1/SN07148.pdf | VERIFIED
- school-water-year.ANS note | "Waterwise estimates UK schools use 4-8 m³ per pupil per year" | no Waterwise source found; water-company audits: average secondary pupil 11 m³/yr, 3.5 m³ "reasonable", 2.1 best practice | https://www.niwater.com/media/sapbw2je/water-school-audit.pdf ; https://www.anglianwater.co.uk/SysSiteAssets/household/in-the-community/water-audit.pdf | UNVERIFIABLE as attributed (the figures found bracket it: 2.1-11). Key 5.7M L = chain product (4.75 m³ per person)
- uk-school-meals.s2 | 0.5 take a school meal ("40-60%") | Scotland 53.6% all meals 2024-25; NI 66.8% on census day; no England-wide figure found | https://www.gov.scot/news/school-meal-uptake-statistics-for-2024-25-published/ ; https://datavis.nisra.gov.uk/DEstatistics/school-meals-statistical-bulletin-202425.html | VERIFIED (within the band; no England figure)
- school-water-year.s1 | 1,200 people (hint: "a typical secondary has 1000-1500 students") | 3,669,933 pupils in state-funded secondaries, Jan 2024; no per-school average found | https://explore-education-statistics.service.gov.uk/find-statistics/school-pupils-and-their-characteristics/2023-24 | pending (needs the secondary school count)
