# WWIUT-CARD-FORMAT (contract, 23 Nov 2026; saved verbatim)

```text
LANE: cloud. Send now (lane free: #888 merged, main a5b3742 green; current main 5adf87a).
MODEL: Opus, effort high: the shared card builder, its checker (new fields, a KaTeX error check, planted faults) and 40 data entries in LaTeX.

TASK: Give every "When will I use this?" job a school-shaped equation, the job's question and an "Inside:" topic tag, shown on its hub card in place of the worked sum, with the worked answer kept on the job's own page.

ROOT CAUSE: Shown: every hub card shows the scenario's "headline", a finished arithmetic sum (scripts/build-uses.py:283-284 headline(), used by hub_page() and scenario_html()), e.g. "£350 × 1.2 = £420". The card gives away its answer and shows only basic arithmetic, so it gives a student no reason to click (Jon, 23 Nov 07:54). Separately, shown: the pages load KaTeX's auto-render with throwOnError:false (build-uses.py head(), about line 236), so a LaTeX error renders as red source text and nothing fails; check-uses.py has no check for .katex-error (grep: no match).

CLASS CHECK: Not a bug class; a format change in one shared place. Every card and job section is written by build-uses.py's functions (headline(), scenario_html(), hub_page()) from data/uses.json, so the change goes there and in the data, never in generated pages by hand. The KaTeX silent-failure gap is a class across the site (other pages also use throwOnError:false): here fix it in check-uses.py for this section only, and REPORT (not fix) the other pages that load KaTeX with throwOnError:false. Explicit lane-ownership exception (AGENTS.md:75), granted by Jon for this task: the cloud lane may change scripts/build-uses.py and scripts/check-uses.py.

EXACT CHANGE:
0. First commit (standing close-out rule). On your start branch from main 5adf87a or later:
   (a) #888's close-out: move docs/handover/contracts/2026-11-22-wwiut-batch-1-2.md and docs/handover/contracts/2026-11-23-wwiut-batch-merge.md to docs/history/contracts/; in docs/handover/cloud.md's WWIUT-BATCH-MERGE entry record: merged as a5b3742 (#888), route merge-pr.py (squash); main's runs check-site 45150284668, phone-fit-full 45150284616, pages build 45150283155, all success on attempt 1; PR head 3058b98 check-site 45147664700 and phone-fit-full 45147664846 success.
   (b) Correct two phrases in docs/handover/cloud.md's SITE-CONTRAST entry (line 95 on 5adf87a; find by text, not line). Replace exactly "measured before schools/assets/fold.js laid the options two to a row (the old check's timing, not the game): not reproduced locally, and CI's own image passed every Sums in Disguise item and wrong option in #889's sweep" with "not reproduced locally or in CI's image by #889's sweep; cause not shown (possibly the fold.js timing #889 found in Some Thingies)". Replace exactly "which fixes the sampled check and the overflow" with "which fixes the sampled check (no overflow was found)".
   (c) Save this contract verbatim as docs/handover/contracts/2026-11-23-wwiut-card-format.md.
1. data/uses.json: add to every scenario "formula" (a LaTeX string, or null), "question" (text ending "?"), "inside" (text), and optionally "formulaNote" (text). Values below, verbatim; LaTeX given raw, so JSON-escape the backslashes. Update the file's _comment to describe the four fields. Never change any existing field (text, steps, sources, headline, tier, route, topic).
2. scripts/build-uses.py:
   - Hub card ("The jobs", hub_page()): replace the headline sum with, in order: the formula set large (\(\displaystyle ...\) inside the existing \( \) delimiter; omit when null), the formulaNote in small muted text if present, the question, then a small "Inside: <inside>" label, then the existing "How it works →". Keep the route dot, the job name and the tier tag as now.
   - Job section (scenario_html(), topic and route pages): after the chips, show the formula (large), formulaNote, and the question; then the text and steps as now; then the headline sum after the steps, labelled "The answer:". The worked steps are unchanged.
   - CSS in USES_CSS for the new parts: the formula visibly larger than body text (it is the card's hook), navy; the note and Inside label small and muted at 4.5:1 or better. No change to colours, route bands or tier tags.
   - Update the module docstring for the new card. Idempotent as before.
3. scripts/check-uses.py:
   - Static: every scenario has a non-empty "question" ending in "?", a non-empty "inside", and "formula" either a non-empty string or null; report how many are null. The headline sum is still recomputed exactly as now.
   - Browser (--check): any element .katex-error on any page fails, naming the page and the source. The existing sideways-scroll check (320x568 and 390x844, normal and Aa) must pass with the new cards.
   - Planted faults (selftest): a scenario with no question; a question with no "?"; a formula with broken LaTeX (e.g. "\dfrac{1}{") caught by the browser check as a .katex-error.
   - Update its ci-line and docstring.
4. Run build-uses.py, then check-uses.py --selftest and --check. If a formula scrolls sideways at 320 px in either mode, reduce the formula's font size in USES_CSS (one rule for all cards); never change a formula.
5. updates/index.html: one line, in that page's existing style: the job cards on "When will I use this?" now lead with the equation each job uses and its question.
6. Report the other pages/games that load KaTeX auto-render with throwOnError:false (path and count only; change nothing).
7. docs/handover/cloud.md entry (done, next, discoveries); PR not draft; merge on a green Gate with `python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600`; report its last line and main's runs. Screenshots of the hub and one topic page at 390x844 and 1366x768 under docs/screens/wwiut-card-format/.

THE VALUES (id | formula | formulaNote | question | inside):
bricklayer | 1 : 2 : 3 | — | How much cement goes in 0.3 m³ of concrete? | Ratio
hairdresser | 1 : 2 | — | How much developer for 40 g of colour? | Ratio
hospital-nurse | \text{dose} = \dfrac{\text{want}}{\text{have}} \times \text{volume} | — | How many ml is a 125 mg dose? | Proportion
plumber | \text{total} = \text{price} \times 1.2 | — | What goes on the bill once VAT is added? | Percentage multipliers
electrician | \dfrac{\text{drop}}{230} \times 100 | — | Will this lighting circuit pass inspection? | Percentages
baker | \text{water} = 70\% \times \text{flour} | — | How much water for 500 g of flour? | Percentages
jeweller | \dfrac{9}{24} = 0.375 | — | How much real gold is in a 9 carat ring? | Fractions to decimals
painter-decorator | A = P \times h | P is the perimeter, h the height | How many litres to paint this room? | Area and perimeter
groundsperson | P = 2(l + w) | — | How much white line does a full-size pitch need? | Perimeter
farmer | A = l \times w | — | How much fertiliser does this field need? | Area and units
practice-nurse | \bar{x} = \dfrac{\sum x}{n} | — | Why isn't one blood pressure reading enough? | Averages
health-visitor | null | — | What does "the 91st centile" mean for this baby? | Percentages
ecologist | N = \bar{x} \times \text{area} | — | How many orchids are in this meadow, without counting them? | Mean, scaling up
meteorologist | \bar{x} = \dfrac{\sum x}{n} | — | How much warmer is a "normal" UK year now? | Averages
sports-scientist | \dfrac{\text{new} - \text{old}}{\text{old}} \times 100 | — | Has six weeks' training actually worked? | Percentage change
payroll-administrator | \text{tax} = 0.2(\text{pay} - \text{allowance}) | — | How much tax comes off a £2,500 month? | Percentages, brackets
bookkeeper | \text{VAT due} = 0.2S - 0.2P | S is sales, P is purchases, before VAT | How much does this business owe HMRC? | Percentages
self-employed-plasterer | 0.2(P - 12\,570) | P is the year's profit | How much should you put aside for tax? | Percentages, brackets
office-administrator | \text{pay} = 0.55m | m is the business miles | What do we pay back for 140 miles? | Substitution
cnc-machinist | 25.00 \pm 0.05 | — | Does a 25.07 mm shaft pass? | Decimals, bounds
maintenance-electrician | I = \dfrac{P}{V} | — | 3 A or 13 A fuse for a toaster? | Formulae
bike-mechanic | \text{gear ratio} = \dfrac{\text{chainring}}{\text{cog}} | — | Which gear gets you up the hill? | Ratio
tiler | \dfrac{(n-2) \times 180}{n} | n is the number of sides | Why do hexagon tiles fit, but pentagons don't? | Angles in polygons
it-support-technician | t = \dfrac{\text{size} \times 8}{\text{speed}} | — | How long will a 600 MB update take? | Speed and units
hgv-driver | t = \dfrac{d}{s} | — | Does this run need a legal break? | Speed, distance, time
care-worker | \text{balance} = \text{in} - \text{out} | — | Is this patient taking in enough fluid? | Negative numbers
shop-floor-assistant | 19 \times 24 \approx 20 \times 24 | — | Has the right delivery arrived? | Estimation
roads-policing-officer | s = \dfrac{d}{t} | — | Was this car speeding between the cameras? | Speed, distance, time
nursery-practitioner | 1 : 5 | — | How many staff does this room legally need? | Ratio, rounding up
tv-producer | \dfrac{8}{60} \times 100 | — | How much of a prime-time hour is your programme? | Percentages
firefighter | a^2 + b^2 = c^2 | — | How long a ladder reaches a window 8 m up? | Pythagoras
games-developer | \lvert \mathbf{v} \rvert = \sqrt{x^2 + y^2} | — | How fast is your character really moving? | Pythagoras, vectors
toolmaker | h = L \sin\theta | L is the sine bar's length | How do you tilt a part to exactly 10°? | Trigonometry
cnc-programmer | (x, y) = (r\cos\theta,\ r\sin\theta) | r is the circle's radius | Where exactly do the bolt holes go? | Trigonometry
hair-colourist | 1 : 2 | — | How much colour goes in a 60 ml mix? | Ratio
vehicle-body-repairer | t = \dfrac{8}{2^n} | n is the number of 3 dB steps above 85 dB | How long is safe in a 94 dB workshop? | Powers
highways-engineer | \text{gradient} = \dfrac{\text{rise}}{\text{run}} | — | How far does a 10% hill climb in a kilometre? | Gradient
architectural-technician | \text{rise} \le \dfrac{\text{length}}{12} | — | How high can a 2 m wheelchair ramp rise? | Gradient, inequalities
painter-decorator-wallpaper | \begin{pmatrix} 0 \\ -32 \end{pmatrix} | In cm: down 32 against the strip beside it | How far down does each strip of half-drop wallpaper move? | Translations
quality-practitioner | z = \dfrac{\bar{x} - \mu}{\sigma / \sqrt{n}} | — | Has the machine drifted, or is it just chance? | Hypothesis testing
("—" means no formulaNote field.)

DO NOT TOUCH: every existing field of every scenario in data/uses.json (text, steps, sources, headline, tier, route, topic, exampleFigures), including the payroll figures (a separate decision for Jon); topics and routes; schools/assets/; parents/guide.css and parents/guide.js; any game; index.html beyond what build-uses.py already writes (the job count is unchanged at 40); the KaTeX loader in other pages (report only, step 6); AGENTS.md; docs/handover/home.md.

SUCCESS CONDITION: All 40 hub cards show formula (39) or question only (health-visitor), note where given, question and Inside label, and no worked sum; every job section shows the formula, note and question first, the unchanged text and steps, then "The answer:" with the headline sum; check-uses.py --selftest catches the three new plants; --check passes with no .katex-error and no sideways scroll at 320x568 and 390x844 in normal and Aa; build-uses.py is idempotent; #888 closed out and both cloud.md phrases corrected in the first commit; one /updates/ line; screenshots saved; merged via merge-pr.py with main green on attempt 1; cloud handover current.

STOP IF: either exact phrase in step 0(b) is not found in docs/handover/cloud.md on your start branch; either contract file in step 0(a) is missing; any formula still shows .katex-error after a correct JSON escape (report the id and the KaTeX message; do not rewrite the formula); a formula scrolls sideways at 320 px even at a formula size no smaller than body text; build-uses.py would change a file outside when-will-i-use-this/, sitemap.xml or the index.html count block; the change needs anything in schools/assets/; main's run on the merge commit is red. A check that fails and passes on its one allowed re-run is reported as "passed on re-run" with the failing output, not as a flake.
```
