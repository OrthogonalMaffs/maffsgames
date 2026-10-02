# Audit: the MathsWins parent guides

Read-only audit, 28 Sep 2026, against the contract in `docs/next-contract-parent-guides-audit.md`
(issued by Jon 28 Sep). **Nothing is fixed here.** This file is the only change the contract permits.
Jon added two instructions mid-audit: check the game links against the **live portfolio**, and take
the guides **directly from the MathsWins repo**. Both are followed below.

**Audience (Jon, 28 Sep):** parents who want to help with homework but lack the skills or the
confidence to do so. It is not the site's resit audience. Findings are weighed for that reader.

**What happened to these findings:** `docs/migrate-parent-guides.md`, the record of the migration
that followed (28 Sep 2026). 19 guides published at `/parents/`, `averages` HELD, every WRONG and
every (h) contradiction fixed, every CHECK carried across for Jon. A second pass on 29 Sep applied
Jon's approved wording, published `averages` against Distinctly Average, and badged the four
Higher-tier guides; see that record's "Second pass" section.

---

## Source

- **Guides:** the MathsWins repo `OrthogonalMaffs/MathsWins`, cloned read-only on 28 Sep 2026.
  - It has one branch, `main`, at `a0557fc` (5 May 2026). Its `CNAME` is `mathswins.co.uk`, so
    `main` is what GitHub Pages serves.
  - `parents/` was last changed by `562a2ee` on 23 Mar 2026. Its full history is five commits:
    `080228f` (all 21 pages added), `cfe8413` (cookie banner on 10 guides), `3d8dbcd` and `530615e`
    (trigonometry cards and diagrams), and `562a2ee` (index hrefs).
- **The live pages were not read.** This environment is refused `mathswins.co.uk` and
  `maffsgames.co.uk` (proxy 403, "CONNECT tunnel failed"), as `docs/todo.md` records. The repo is
  the deploy source, so the only gap is a deploy that failed or lags. Nothing suggests one.
- **MaffsGames side:** this repo at `origin/main` `47a84f6`. "Live portfolio" means the game
  cards in the portal's `index.html` at that commit, which is what GitHub Pages serves. It is **not**
  an HTTP check against the live site, which cannot be reached from here.

### STOP IF conditions

| Condition | Result |
|---|---|
| Guide count is not 20 | Clear. 20 guides (10 KS3, 10 GCSE) plus the index page |
| Generated from a data file or template engine | Clear. 21 hand-authored static HTML files, added in one commit (`080228f`, 21 HTML files + `sitemap.xml`). No generator or data file anywhere in the repo references them |
| Neither source reachable | Clear. The repo clones |
| A guide links to an external site other than `maffsgames.co.uk` | Clear. The only other outbound link is `mailto:contact@mathswins.co.uk` (11 pages). Other links stay on MathsWins: `/`, `/parents/`, `/terms/`, and one `/everyday/` on the index |
| A guide carries content that is not a parent maths guide | Clear |

---

## Header

| | Count |
|---|---|
| Guides | **20**: KS3 10, GCSE 10. Plus the index page `/parents/` |
| Template families | **4**, not the one the contract's CLASS CHECK assumed. See below |
| MaffsGames links | **29**: 24 to games (24 distinct slugs, one link each) and 5 to `maffsgames.co.uk/schools`. The index page links to no game |
| Links that resolve | **29 of 29.** All 24 slugs exist under `games/`, are in the roster and have a card on the live portal. The 5 `/schools` links reach `schools/index.html`, a JavaScript redirect to `/`, not a 301 |
| Broken links | **0** |
| Links that open the guide's own level | **16 of 24** (KS3 4 of 12, GCSE 12 of 12). 7 are PARTLY and 1 is NO; see "Game links against the live portfolio" |
| Worked examples recomputed | **All of them.** 65 scripted assertions covering every worked example, every "try another" answer and every numeric claim. **0 arithmetic MISMATCH.** One answer is right but misleading (coordinates, a 3 × 3 square answered "a rectangle") |
| Claims, per-guide sections (d), (e) and (g) | **OK 82 · WRONG 15 · CHECK 86** (183 claims; CHECK includes every "how schools teach it" claim, as the contract requires) |
| Claims, TEMPLATE section and index page | **OK 16 · WRONG 10 · CHECK 12** (38 claims) |

**Four template families, five guides each.** They share the five section headings, but most of
the text around those headings differs by family. There is no single template layer. The migration
builds one new template anyway, so this changes where the TEMPLATE findings land (once, in the new
template), not how many fixes there are.

| Family | Guides | Distinguishing marks |
|---|---|---|
| A | `negative-numbers`, `algebra-basics`, `fractions`, `ratio-proportion`, `sequences` (KS3) | "KS3" badge; "The Problem" panel; "No sign-up, no data collected, completely safe for children."; footer "© 2026 MathsWins · Terms of Use · Contact" |
| B | `area-perimeter`, `angles`, `probability`, `averages`, `coordinates` (KS3) | UPPER-CASE headings; "KS3 Parent Guide"; "Worked Example"; "It's free, … and there's no sign-up needed."; footer "All rights reserved." |
| C | `expanding-factorising`, `simultaneous-equations`, `trigonometry`, `circle-theorems`, `standard-form` (GCSE) | "Section 1–5" labels; "Parent tip", "Classic mistake", "Watch out", "Conversation starter"; footer "Schools? Visit maffsgames.co.uk/schools" |
| D | `indices-surds`, `graphs-transformations`, `pythagoras`, `probability-trees`, `statistics-data` (GCSE) | Numbered headings "1. What Your Child…"; two back links in the nav bar; "Free game on MaffsGames — no sign-up, no data collected, safe for children:" |

**The GCSE badge makes no Foundation/Higher distinction.** By the vendored DfE subject content
(`data/dfe-gcse-parts.json`, bold = Higher only), some GCSE guides are wholly or partly Higher-only:

- **Wholly Higher:** `circle-theorems` (G10) and `graphs-transformations` (A13).
- **Partly Higher:**
  - `indices-surds`: surds are N8, fractional indices N7.
  - `statistics-data`: histograms and cumulative frequency are S3, box plots S4.

The other GCSE guides stay within content both tiers are assessed on. A parent who lacks the
confidence to judge the maths also cannot judge its tier. A parent of a Foundation-tier child who
opens the circle theorems or graph transformations guide is not told that their child will not be
examined on it.

---

## The findings that matter most

In order of what a parent or student would be misled by:

1. **The data claim is false on 10 guides and the index FAQ.** They say MaffsGames has "no data
   collected". `privacy/index.html` says MaffsGames collects no **personal** data, but logs
   anonymous gameplay events and runs cookieless GA4. All 21 pages also carry MathsWins' cookie
   banner ("We use cookies for analytics"), which is untrue of MaffsGames. The privacy page says
   MaffsGames needs no banner. (T1b, T2a.)
2. **Four guides misstate what GCSE assesses:**
   - Circle theorems says the child "does not need to prove these theorems". DfE G10 is "apply and
     **prove**", and the guide's own index card says "the proofs behind them".
   - Graph transformations teaches stretches as GCSE content. DfE A13 has translations and
     reflections only, and MaffsGames' own Graph Transformer says "GCSE: Translations and reflections
     only. A-Level: Adds … stretches."
   - Coordinates says four-quadrant grids arrive at KS3. The National Curriculum puts the full
     coordinate grid in Year 6, and MaffsGames' own Four Quadrant Explorer is a Year 6 game.
   - Expanding and factorising calls "find two numbers that multiply to … and add to …" "genuinely
     the entire method". That is false once a ≠ 1 (DfE A4, Higher).
3. **Mathematical statements that are wrong** (the arithmetic itself is right everywhere):
   - Negative numbers: "Adding always means moving right". The guide contradicts it two paragraphs
     later. It also says "two negatives make a positive" applies "only when the signs are directly
     next to each other", which excludes (−2) × (−3) = 6.
   - Fractions:
     - The 0.3 against 0.25 misconception is written backwards ("because 3 is bigger than 25"),
       and its follow-up is false (0.3 **is** bigger than 0.125).
     - "Divide by the percentage only works for finding 1%" is false. It works only for **10%**,
       since a ÷ p = p% of a exactly when p² = 100.
   - Probability gives P = favourable ÷ total without "equally likely". That breaks the guide's own
     lottery example: win or lose would give ½.
   - Area says doubling a triangle makes a rectangle. That is true only for a right-angled triangle;
     otherwise it makes a parallelogram.
   - Averages says two values appearing "the same number of times" gives two modes. It is only so
     when they tie for **most** often.
   - Statistics says "exactly half … by definition of quartiles". It is approximately half.
   - Indices says the six laws "cover every situation", but (ab)ⁿ = aⁿbⁿ is missing. It also says
     "anything to the power 0 is 1", with no x ≠ 0.
4. **Links that don't fit the guide.** Eight of the 24 game links don't open the guide's level:
   - Six KS3 guides send parents to Year 6 transition banks.
   - `angle-ace` opens on GCSE for a KS3 guide.
   - `stat-attack` has no KS3 level and doesn't cover what the averages guide teaches, though the
     guide says it does.

   Three links are poor topic fits:
   - `new-shapes` for area and perimeter;
   - `coordinate-geometry-dash` for Pythagoras (3 of its 45 questions);
   - `stat-attack` for averages.

   **No game is built around** KS3 area and perimeter, ungrouped averages or Pythagoras; each
   appears only as scattered items. Formula Plug-In's Year 6 bank comes nearest for area and
   perimeter.
5. **Three linked games carry open defects.**
   - `circle-theorem-spotter`: to-do §1.3.
   - `chart-interrogator`: §1.8 and §1.15–1.18.
   - `coordinate-geometry-dash:233`: found in this audit, and not yet in the to-do. It is the one
     game the Pythagoras guide links to. Details at the end.

---

## Game links against the live portfolio

Added at Jon's request. "On live portal" means the slug has a card in `index.html` at `47a84f6`.
"Opens on" is what a bare link, the only form the guides use, loads, read from each game's own
level-routing code. "Level fit" answers the contract's question 5(b): does the game serve the level
the guide is for?

- **YES:** it serves that level on the link as written.
- **PARTLY:** it serves a neighbouring level. This is a teaching call.
- **NO:** it does not serve that level.

| Guide (level) | Anchor text | Slug | `games/` | Roster | Live portal (levels on card) | Opens on | Level fit | Topic fit |
|---|---|---|---|---|---|---|---|---|
| negative-numbers (KS3) | Play Negative Number Line on MaffsGames → | `negative-number-line` | yes | yes (Year 6) | yes (`ks3 year6`) | Year 6 bank (`const LEVEL = 'year6'`, no level param) | PARTLY | Good: place, order, calculate on −10 to 10 |
| algebra-basics (KS3) | Play Like Terms Collector → | `like-terms-collector` | yes | yes (Year 6) | yes (`ks3 year6`) | Year 6 bank (hard-coded `'year6'`) | PARTLY | Good |
| algebra-basics (KS3) | Play Think of a Number → | `think-of-a-number` | yes | yes (Year 6) | yes (`ks3 year6`) | Year 6 bank (hard-coded `'year6'`) | PARTLY | Good: the guide's own worked example is this puzzle |
| fractions (KS3) | Play Fraction Equivalence → | `fraction-equivalence` | yes | yes (Year 6, KS3, GCSE; name "Fraction Snap") | yes (`gcse ks3`) | Default "all" pool, "KS3 and GCSE fraction fluency"; Year 6 only via `?level=year6` | YES | Partial: equivalence yes/no only; the guide also teaches decimal place value, % of an amount and adding fractions. The anchor calls it "Fraction Equivalence"; the game is "Fraction Snap" |
| fractions (KS3) | Play Percentage Flip → | `percentage-flip` | yes | yes (Year 6, KS3, GCSE) | yes (`gcse ks3`) | Default pool; Year 6 only via `?level=year6` | YES | Good for the percentages section: all 32 default-bank questions are "What is N% of N?", the guide's own worked-example shape |
| ratio-proportion (KS3) | Play Split It on MaffsGames → | `split-it` | yes | yes (KS3, GCSE) | yes (`gcse ks3`) | Level picker with KS3 and GCSE buttons | YES | Good |
| sequences (KS3) | Play Sequence Solver on MaffsGames → | `sequence-solver` | yes | yes (KS3, GCSE, A-Level, L4) | yes | KS3 (`let level='ks3'`) | YES | Good |
| area-perimeter (KS3) | Play New Shapes on MaffsGames | `new-shapes` | yes | yes (Year 6) | yes (`ks3 year6`) | Year 6 bank | PARTLY | **Poor.** Sections are parallelogram (15), trapezium (20), prism (15). The guide teaches rectangles, triangles, perimeter and compound shapes |
| angles (KS3) | Play Angle Ace on MaffsGames | `angle-ace` | yes | yes (Year 6, KS3, GCSE) | yes (`gcse ks3`, bare link) | **GCSE** (`selectLevel('gcse')` default). The only buttons are Year 6 ("This is real KS3 maths") and GCSE; there is no KS3 bank | PARTLY | Good |
| probability (KS3) | Play Probability Pioneer on MaffsGames | `probability-pioneer` | yes | yes (Year 6) | yes (`ks3 year6`) | Year 6 bank | PARTLY | Good |
| averages (KS3) | Play Stat Attack on MaffsGames | `stat-attack` | yes | yes (GCSE, Core, L4) | yes (`core gcse l4`) | Level picker: GCSE, Core, Level 4 | **NO** | **Poor.** Grouped frequency tables: modal class, median class, estimated mean, standard deviation. The guide teaches ungrouped mean, median, mode and range, and says the game practises exactly those |
| coordinates (KS3) | Play Four Quadrant Explorer on MaffsGames | `four-quadrant-explorer` | yes | yes (Year 6) | yes (`ks3 year6`) | Year 6 bank | PARTLY | Good |
| expanding-factorising (GCSE) | Practise Now on MaffsGames | `quadratic-factoriser` | yes | yes (GCSE, A-Level) | yes (`alevel gcse`) | `gcse` (a = 1), first of `IMPLEMENTED_LEVELS` | YES | Good for factorising; nothing practises expanding |
| simultaneous-equations (GCSE) | Practise Now on MaffsGames | `simultaneous-solver` | yes | yes (GCSE, A-Level) | yes | `gcse` | YES | Good |
| trigonometry (GCSE) | Play Trig Wars | `trig-wars` | yes | yes (GCSE, A-Level) | yes | One content set, no level param | YES | Partial: an artillery game (angle and power, V<sub>x</sub>/V<sub>y</sub> resolution). The guide calls it "fast rounds"; the game's briefing says "your first shot is not supposed to hit" |
| trigonometry (GCSE) | Play Trig Worms | `trig-worms` | yes | yes (GCSE, A-Level) | yes | One content set | YES | Good: SOH CAH TOA |
| circle-theorems (GCSE) | Practise Now on MaffsGames | `circle-theorem-spotter` | yes | yes (GCSE) | yes (`gcse`) | One content set | YES | Good. Open defect: to-do §1.3, Q48 has no solution |
| standard-form (GCSE) | Practise Now on MaffsGames | `standard-form-blitz` | yes | yes (GCSE, A-Level) | yes | `gcse` | YES | Good. The guide says "against the clock"; `.claude/rules/timer-policy.md` lists this game as a hidden count-up |
| indices-surds (GCSE) | Index Laws Game → | `index-laws` | yes | yes (GCSE, A-Level) | yes | One content set | YES | Good |
| indices-surds (GCSE) | Surd Simplifier Game → | `surd-simplifier` | yes | yes (GCSE, A-Level) | yes | `gcse` | YES | Good |
| graphs-transformations (GCSE) | Graph Transformer Game → | `graph-transformer` | yes | yes (GCSE, A-Level) | yes | `gcse`: "Translations and reflections only" | YES | Good. The game's scope is right and the guide's is not; see that guide |
| pythagoras (GCSE) | Coordinate Geometry Dash → | `coordinate-geometry-dash` | yes | yes (GCSE, A-Level) | yes | `gcse` | YES | **Poor.** 3 of its 45 questions use Pythagoras (distance between points), and one of them is defective (`:233`, below) |
| probability-trees (GCSE) | Probability Paradox Game → | `probability-paradox` | yes | yes (GCSE, Core) | yes (`core gcse`) | Mode picker | YES | Partial: tree diagrams are in the "Conditional Calculator" mode, which the game badges **A-Level** |
| statistics-data (GCSE) | Chart Interrogator Game → | `chart-interrogator` | yes | yes (GCSE, A-Level, Core, L4) | yes | Type and level picker, GCSE offered | YES | Good for histograms, cumulative frequency and box plots; scatter graphs and correlation not covered. Open defects: to-do §1.8, §1.15–1.18 |

The five `https://maffsgames.co.uk/schools` links (family C footers) resolve through
`schools/index.html`, a `window.location.replace('/')` stub. Their link text displays the redirect
path. On 28 Sep "MaffsGames Schools" became "MaffsGames" (PR #1, `docs/audit-schools-brand.md`).

**Live alternatives, for Jon's relinking decision.** These are matched on portal metadata and, where
noted, the game's source. None was played.

| Guide | Live games that fit better or add coverage | Portfolio gap |
|---|---|---|
| algebra-basics | `equation-builder` (KS3, GCSE, L4: building equations from word problems, the guide's plumber example) | — |
| fractions | `decimal-detective` (Year 6/KS3 card: decimal place value and ordering) for the place-value section | — |
| area-perimeter | `formula-plug-in` (Year 6 bank, KS3 on the portal): 25 of its 50 items substitute into area and perimeter formulas for rectangles, squares and triangles. A closer fit than New Shapes, though substitution only | **No game is built around KS3 area and perimeter**; nothing practises compound shapes |
| angles | Same game, linked as `?level=year6` if KS3 is to match the Year 6 bank's "This is real KS3 maths" | No KS3 bank |
| averages | — | **No game is built around ungrouped mean, median, mode and range.** They appear only as scattered items in the reasoning games (`maths-court`, `spot-the-error`, `terrible-advice` among them) and as 5 "Mean" substitution items in `formula-plug-in` |
| trigonometry | `trig-identity-duel` (GCSE: exact values, which the guide uses for sin 30°) | — |
| pythagoras | — | **No game is built around Pythagoras.** It appears only as individual items in the reasoning games (`maths-court`, `terrible-advice`, `spot-the-muppet` among them) and in 3 of Coordinate Geometry Dash's 45 questions |
| probability-trees | `given-that` (GCSE+: two-way tables, Venn diagrams, frequency trees) | No GCSE-badged probability tree practice |
| statistics-data | `correlation-or-coincidence` (GCSE) for the scatter graph and correlation section | — |

---

## TEMPLATE section

Every sentence that appears verbatim or near-verbatim in 3 or more guides, found by a scripted
sentence count across all 20 files, plus the whole index page.

### Template sentences

| # | Sentence | Where | Verdict | Reason |
|---|---|---|---|---|
| T1a | "No sign-up" (in "No sign-up, no data collected, completely safe for children." and "Free game(s) on MaffsGames — no sign-up, no data collected, safe for children:") | Families A and D (10) and the index FAQ | OK | `privacy/index.html`: "There are no accounts, no logins, and no registration." |
| T1b | "no data collected" (same two sentences) | Families A and D (10) and the index FAQ | WRONG | `privacy/index.html` says MaffsGames collects no **personal** data. It does collect anonymous gameplay events, portal filter and search events, and cookieless GA4 page data, and stores voluntary leaderboard initials. "No personal data collected" is the claim the privacy page supports |
| T1c | "(completely) safe for children" (same two sentences) | Families A and D (10) and the index FAQ | CHECK | The privacy page claims "safe to use on school networks without ICT approval barriers". "Completely safe for children" is broader: the leaderboard publishes filtered initials. Jon's wording |
| T2a | Cookie banner: "We use cookies for analytics to improve your experience." | All 21 pages | WRONG | For MaffsGames. `privacy/index.html`: "No cookies are stored on your device … MaffsGames does not require a cookie consent banner under PECR." The banner, its Accept/Decline handlers and the `mw_cookies` localStorage key must not migrate |
| T2b | Cookie banner: "No personal data is sold or shared." | All 21 pages | OK | True of MaffsGames, which holds no personal data from play. Goes with T2a regardless |
| T3 | "Free parent guides from a working maths tutor." / meta "A parent's guide from a working maths tutor" | Family D footers (5), four family A meta descriptions, the index footer and body | CHECK | An author claim about Jon's role; to-do §1.6 already flags the About page's out-of-date role. Jon to word |
| T4 | "Schools? Visit maffsgames.co.uk/schools for free classroom games." | Family C footers (5) | WRONG | Points at a redirect stub and prints the stub path as its text. The "Schools" brand was retired on 28 Sep (PR #1). Once migrated it is a link from MaffsGames to itself |
| T5 | "Free parent guides — no account needed." | Family C footers (5) | OK | True |
| T6 | "It's free, (it's fun / it works on any device / works on any device), and there's no sign-up needed." | Family B practise blurbs (5) | CHECK | "Free" and "no sign-up" are true. "Works on any device" is not something MaffsGames tests or documents; several games are canvas-based |
| T7 | Section heading "What Your Child Is Learning" | All 20 | OK | Heading |
| T8 | Section heading "How Schools Teach It Now" | All 20 | CHECK | Implies one national method. What sits under it is a mix of common practice and the author's preference; each guide's (e) list is Jon's to rule on |
| T9 | Section heading "Common Mistakes to Watch For" | All 20 | OK | Heading |
| T10 | Section heading "Try It Together" | All 20 | OK | Heading |
| T11 | Section heading "Let Them Practise" | All 20 | OK | Heading |
| T12 | Badge "GCSE Parent Guide" | Families C and D (10) | CHECK | No Foundation/Higher distinction; several topics are wholly or partly Higher-only (header, above) |
| T13 | Badge "KS3 Parent Guide" / "KS3" | Families A and B (10) | OK | Correct level label. The links under it are another matter (link table) |
| T14 | Subtitle "A parent's guide to X — what it is, how schools teach it, and how to help." | Family A (5) | OK | — |
| T15 | Opener "This might look intimidating …, but the method is actually very straightforward / logical once you see …" | `expanding-factorising`, `simultaneous-equations`, `circle-theorems` | OK | Tone only |
| T16 | Labels "Parent tip", "Classic mistake", "Watch out", "Conversation starter", "Easy marks lost" | Family C (5) | OK | Labels |
| T17 | "Free interactive practice — …" / "We have (built) a free interactive tool / a free game / two free games …" / "Practise Now on MaffsGames" | Family C (5) | OK | True as far as it goes; per-game descriptions are checked in the guides |
| T18 | Navigation and copyright text: "← All Parent Guides", "All Parent Guides →", "← Back to all guides", "Back to all parent guides", "© 2026 MathsWins …", "All rights reserved.", "Terms of Use", "Contact" | All 20, by family | OK | Brand and navigation text, replaced on migration. Family D has two back links in one nav bar |

### The index page (`/parents/`)

**Its FAQ, in full:**

| # | Claim | Verdict | Reason |
|---|---|---|---|
| F1 | "Methods have evolved to build deeper understanding." | CHECK | Pedagogy |
| F2 | "Long division, grid multiplication, and bar models replace the shortcuts you learned." | WRONG | Long division **is** the traditional method most parents learned. The National Curriculum names it as the Year 6 formal written method ("divide numbers up to 4 digits by a two-digit whole number using the formal written method of long division"); it replaced nothing. Grid multiplication is a transitional method on the way to the formal columnar one, not its replacement. Bar models are CHECK |
| F3 | "The answers are the same — the routes are different." | OK | — |
| F4 | "Do I need to be good at maths to help? No. These guides assume you've forgotten everything. They start from scratch and explain in plain English." | CHECK | True of the KS3 guides. The GCSE guides assume FOIL, function notation and quartiles without building them |
| F5 | "What if I teach them the wrong method? Show them you're interested, not that you know the method. These guides show the method schools use now…" | CHECK | Advice is sound; "the method schools use now" is the T8 claim again |
| F6 | "How much should I help with homework? Guide, don't do. … The struggle is where learning happens." | CHECK | Pedagogy (productive struggle). Jon's call |
| F7 | "MaffsGames is a free schools platform — no sign-up, no data collected, safe for children." | WRONG | "No data collected": see T1b. "Schools platform" is the retired brand framing (PR #1) |
| F8 | "Every game linked from these guides is completely free." | OK | — |

**Its intro and footer:**

| # | Claim | Verdict | Reason |
|---|---|---|---|
| I1 | "Maths has changed since you were at school. The methods are different, the language is different, and the curriculum has expanded." | CHECK | Pedagogy and curriculum history |
| I2 | "…show you exactly how schools teach it now…" | CHECK | See T8 |
| I3 | "No sign-up. No cost. Just clear explanations from a working maths tutor." | CHECK | See T3 |
| I4 | Section labels "KS3 Topics Years 7–9", "GCSE Topics Years 10–11" | OK | Correct |

**Its cards, checked against the guides they link to.** Five cards promise content the guide
doesn't have:

| # | Card text | Verdict | Reason |
|---|---|---|---|
| C1 | Coordinates: "…and drawing straight-line graphs." | WRONG | The guide covers no straight-line graphs; it only says plotting shapes "builds towards" them |
| C2 | Expanding & Factorising: "…and the difference of two squares." | WRONG | The guide never mentions the difference of two squares |
| C3 | Circle Theorems: "…and the proofs behind them." | WRONG | The guide says "Your child does not need to prove these theorems" |
| C4 | Probability Trees: "…independent and dependent events, and conditional probability." | WRONG | The guide never mentions independence, dependent events or conditional probability |
| C5 | Graph Transformations: "Translations, reflections, stretches…" | WRONG | Stretches are not GCSE content (DfE A13; see that guide) |

The other 15 cards match their guides. Trigonometry's "finding sides and angles" is partly met, since
the guide never shows finding an angle. The index card hrefs were corrected in `562a2ee`; all 20 now
point at the right guide.

---

## Per-guide sections

Conventions: verdicts are **OK**, **WRONG** or **CHECK** (a pedagogy or factual point for Jon).
Every "how schools teach it" claim is **CHECK** by the contract's rule; where there is evidence
either way, it is noted. DfE references are to `data/dfe-gcse-parts.json` (bold = Higher only).
The level-fit and topic-fit detail for every link is in the link table above; each (b) below gives
the one-line result.

---

### 1. Negative Numbers

**(a)** `https://mathswins.co.uk/parents/negative-numbers/` · "Negative Numbers — A Parent's Guide" · KS3 · family A

**(b)** "Play Negative Number Line on MaffsGames →" → `negative-number-line`. It is in `games/` and the
roster, and live on the portal. Level fit PARTLY: Year 6 bank only.

**(c) Worked examples**

| Example | Guide's answer | Recomputed | Result |
|---|---|---|---|
| −3 + 5 (number-line walk) | 2 | 2 | ✓ |
| 4 + (−3), 4 − (−3) | 1, 7 | 1, 7 | ✓ |
| 5 − (−2); −3 + (−4) | 7; −7 | 7; −7 | ✓ |
| 2 − 5 (counted through zero) | −3 | −3 | ✓ |
| Try it: start at 4, subtract 7 | −3 | −3 | ✓ |
| Try another: −2 + 6 | 4 | 4 | ✓ |

**(d) Mathematical claims**

| Claim | Verdict | Reason |
|---|---|---|
| "The further left you go, the smaller the number." | OK | — |
| "−3°C is colder (and therefore smaller) than −1°C." | OK | — |
| "Adding always means moving right. Subtracting means moving left." | WRONG | Adding a negative moves left, which the guide itself says two paragraphs later. Holds only for adding and subtracting positive numbers |
| "Adding a negative is the same as subtracting; subtracting a negative is the same as adding." | OK | — |
| "two negatives make a positive" is used "only when the signs are next to each other (like −(−3))" / "This rule only applies when the signs are directly next to each other" | WRONG | Excludes multiplication and division, (−2) × (−3) = 6, which is the main place the phrase is used. The guide says children will "multiply and divide with negative numbers" but never gives that rule |
| "−3 + 5 = −8" named as adding magnitudes and keeping the sign | OK | A real misconception, correctly described |
| "Up until now, your child has mostly worked with counting numbers" | CHECK | National Curriculum: negatives are met through zero in Year 4, in context in Year 5, and with intervals across zero in Year 6. "Mostly" softens it; KS3 extends negatives rather than introducing them |

**(e) "How schools teach it" claims**

| Claim | Verdict | Note |
|---|---|---|
| "Schools use the number line heavily to make this visual and concrete." | CHECK | — |
| "Schools use the number line as the primary tool." | CHECK | — |
| "Your child will physically (or mentally) 'walk' along the number line." | CHECK | — |
| "Schools sometimes use the phrase 'two negatives make a positive'…" | CHECK | The practice claim; its mathematical restriction is WRONG in (d) |

**(f) Notation not in LaTeX:** the number-line strip (−5 … 5) is plain HTML with ASCII hyphen-minus
for the negative sign. In-line maths is otherwise LaTeX. `\(-3°\)C` puts a Unicode ° in maths mode.
KaTeX renders it but warns in strict mode.

**(g) Data/privacy claims:** "No sign-up, no data collected, completely safe for children." See T1a–c.
Cookie banner: T2.

**(h) Internal contradictions:** "Adding always means moving right" (How Schools Teach, step 2)
against "adding a negative is the same as subtracting" (the same section, and What Your Child Is
Learning).

---

### 2. Algebra Basics

**(a)** `https://mathswins.co.uk/parents/algebra-basics/` · "Algebra Basics — A Parent's Guide" · KS3 · family A

**(b)** Two links, both live and on the roster:

- "Play Like Terms Collector →" → `like-terms-collector`
- "Play Think of a Number →" → `think-of-a-number`

Level fit PARTLY for both: Year 6 banks only.

**(c) Worked examples**

| Example | Guide's answer | Recomputed | Result |
|---|---|---|---|
| 3x + 4 + 2x − 1 | 5x + 3 | 5x + 3 | ✓ |
| Plumber: £30 call-out + £20/hour | 20h + 30 | 20h + 30 | ✓ |
| 3(x + 4) | 3x + 12 | 3x + 12 | ✓ |
| Double, add 5, get 17 | x = 6 | 6 | ✓ |
| Try another: ×3, −4, get 11 | 5 | 5 | ✓ |

**(d) Mathematical claims**

| Claim | Verdict | Reason |
|---|---|---|
| "When they see 3x, it means '3 times that unknown number' — not 'thirty-something'." | OK | — |
| "x² = 'x times x' (not 2x)" | OK | — |
| "3x + 2 = you can't simplify this" / "Writing 3x + 2 = 5x is very common." | OK | — |
| "An expression … doesn't have an equals sign. An equation … does. You simplify expressions. You solve equations." | OK | — |
| "In primary school, x was the multiplication symbol." | CHECK | The primary multiplication symbol is ×, not the letter x. The confusion is real, but the sentence says they are the same symbol |
| "the multiplication sign is written differently (a dot or just putting things next to each other)" | OK | — |
| "Schools call this 'expanding brackets'." | OK | Standard term |

**(e) "How schools teach it" claims**

| Claim | Verdict | Note |
|---|---|---|
| "Schools start with collecting like terms." | CHECK | — |
| "Schools also teach forming expressions from word problems." | CHECK | — |
| "Translating real life into algebra is a key skill at KS3." | CHECK | — |

**(f) Notation not in LaTeX:** the quick-translation strings "not thirty-x" and "(not 2x)" are plain
text. The quick-translation block also writes `\(3x + 2x = 5x\) = collecting like terms`, which reads
as an equation whose right side is a phrase.

**(g)** T1a–c; T2.

**(h)** None.

---

### 3. Fractions, Decimals & Percentages

**(a)** `https://mathswins.co.uk/parents/fractions/` · "Fractions, Decimals & Percentages — A Parent's Guide" · KS3 · family A

**(b)** Two links, both live and on the roster:

- "Play Fraction Equivalence →" → `fraction-equivalence`. Level fit YES; topic fit partial. The game's
  name is "Fraction Snap".
- "Play Percentage Flip →" → `percentage-flip`. Level fit YES; topic fit good for the percentages section.

**(c) Worked examples**

| Example | Guide's answer | Recomputed | Result |
|---|---|---|---|
| Conversion table: ½, ¼, ¾, ⅕, 1⁄10, ⅓ | 0.5/50%, 0.25/25%, 0.75/75%, 0.2/20%, 0.1/10%, 0.333…/33.3…% | same | ✓ |
| 35% of 80 via 10% and 5% | 28 | 28 | ✓ |
| ½ + ⅓ | 5⁄6 | 5⁄6 | ✓ |
| 20% of 60 (and the misconception 60 ÷ 20) | 12 (misconception 3) | 12 (3) | ✓ |
| ¾ of 20 | 15 | 15 | ✓ |
| Try another: 15% of £60 | £9 | £9 | ✓ |

**(d) Mathematical claims**

| Claim | Verdict | Reason |
|---|---|---|
| "three different ways of writing the same thing" | OK | — |
| Numerator and denominator definitions | OK | — |
| "the digit after the decimal point is tenths, the next is hundredths" | OK | — |
| "Thinking 0.3 is bigger than 0.25 'because 3 is bigger than 25.' … In this case they happen to be right, but their reasoning is wrong. The same logic would wrongly suggest 0.3 is bigger than 0.125." | WRONG | Garbled. 3 is not bigger than 25. The real misconception is "0.25 > 0.3 because 25 > 3". And 0.3 **is** bigger than 0.125, so nothing "wrongly" follows. The bullet needs rewriting from scratch |
| "'Divide by the percentage' only works for finding 1%." | WRONG | a ÷ p equals p% of a exactly when p² = 100, so it works only for **10%**. Dividing by 1 gives 100%, not 1%. Checked for p = 1…100 |
| "The word 'of' in maths almost always means multiply." | OK | — |
| "This 'building blocks' method … works for any percentage without a calculator." | OK | True with 1% and halving available; awkward for, say, 17.5%, but not false |

**(e) "How schools teach it" claims**

| Claim | Verdict | Note |
|---|---|---|
| "Schools use three main tools: bar models for fractions, place value grids for decimals, and the 'of means multiply' rule for percentages." | CHECK | — |
| "Schools teach all three forms together." | CHECK | — |
| "schools teach building from 10% and 1%" | CHECK | The worked example uses 10% and 5%, not 1% |

**(f) Notation not in LaTeX:** decimals and percentages in the table and prose are plain, which is
fine by canon §7.1.1. Two expressions are plain text: "0.3 = 0.30" and "10% of 60 = 6, so 20% = 12".

**(g)** T1a–c; T2.

**(h)** The percentages method is headed "of means multiply", but the method under it is building
from 10% (partitioning, not multiplying). It also promises "10% and 1%" and uses 10% and 5%.

---

### 4. Ratio & Proportion

**(a)** `https://mathswins.co.uk/parents/ratio-proportion/` · "Ratio & Proportion — A Parent's Guide" · KS3 · family A

**(b)** "Play Split It on MaffsGames →" → `split-it`. It is in `games/` and the roster, and live on the
portal. Level fit YES; topic fit good.

**(c) Worked examples**

| Example | Guide's answer | Recomputed | Result |
|---|---|---|---|
| 3 cakes : 6 eggs → 6 cakes | 12 eggs | 12 | ✓ |
| Share £60 in 2:3 (twice) | £24, £36 | £24, £36 | ✓ |
| Misconception: £60 ÷ 2 and ÷ 3 | £30 + £20 = £50 | £50 | ✓ |
| 2:3 as a fraction of the total | 2⁄5 | 2⁄5 | ✓ |
| 6:9 simplified | 2:3 | 2:3 | ✓ |
| Try another: £45 in 4:5 | £20, £25 | £20, £25 | ✓ |

**(d) Mathematical claims**

| Claim | Verdict | Reason |
|---|---|---|
| "A ratio compares two (or more) quantities … the ratio stays the same" | OK | — |
| "Proportion is the related idea that things scale up or down together." | OK | Direct proportion; inverse proportion is not KS3-core |
| "In a 2:3 ratio, the first share is 2⁄5 of the total (not 2⁄3)." | OK | — |
| "Ratios simplify like fractions — by dividing both sides by the same number." | OK | — |
| "The order in the ratio matches the order in the words." | OK | — |

**(e) "How schools teach it" claims**

| Claim | Verdict | Note |
|---|---|---|
| "Schools use the 'total parts' method combined with bar models. It's systematic and works every time." | CHECK | — |
| "Schools draw bar models alongside this method." | CHECK | — |

**(f) Notation not in LaTeX:** ratios (2:3, 4:5, 6:9, 3:2) are plain text throughout, and the bar-model
labels are HTML. Whether a bare ratio counts as an expression under canon §7.1.1 is Jon's call. One
plain-text sum: "£30 + £20 = £50".

**(g)** T1a–c; T2.

**(h)** None.

---

### 5. Sequences & Patterns

**(a)** `https://mathswins.co.uk/parents/sequences/` · "Sequences & Patterns — A Parent's Guide" · KS3 · family A

**(b)** "Play Sequence Solver on MaffsGames →" → `sequence-solver`. It is in `games/` and the roster,
and live on the portal. It opens on KS3. Level fit YES; topic fit good.

**(c) Worked examples**

| Example | Guide's answer | Recomputed | Result |
|---|---|---|---|
| 2, 5, 8, 11, 14 → next; nth term; 100th | 17; 3n − 1; 299 | 17; 3n − 1; 299 | ✓ |
| Diagram 5, 8, 11, 14, 17 → next | 20 | 20 | ✓ |
| nth term of 5, 8, 11, 14; checks n = 1, 2, 3 | 3n + 2; 5, 8, 11 | same | ✓ |
| 50th term of 3n + 2 | 152 | 152 | ✓ |
| Differences of 1, 4, 9, 16, 25 | 3, 5, 7, 9 | same | ✓ |
| 1, 4, 7, 10 | 3n − 2 | 3n − 2 | ✓ |
| Try another: 4, 7, 10, 13 | 3n + 1 | 3n + 1 | ✓ |

**(d) Mathematical claims**

| Claim | Verdict | Reason |
|---|---|---|
| "the rule is 3n + (−1), which we write as 3n − 1" | OK | — |
| "nth term = dn + c; d = common difference, c = first term minus d" | OK | — |
| "1, 4, 9, 16, 25… This is a quadratic sequence (square numbers)." | OK | — |
| "At KS3, most sequences will be linear." | OK | KS3 also meets quadratic and geometric sequences, which the guide acknowledges |
| "The quickest way to catch errors is to substitute n = 1 … If it doesn't give the first term … something is wrong." | CHECK | True, but one term is not enough: 5n passes n = 1 for 5, 8, 11. The guide's own worked check uses three terms, the better habit |

**(e) "How schools teach it" claims**

| Claim | Verdict | Note |
|---|---|---|
| "schools don't just want children to spot the next number. They want them to find a formula…" | CHECK | — |
| "Schools teach a systematic method for finding the nth term…" (compare with the times table, find the adjustment) | CHECK | — |

**(f) Notation not in LaTeX:** the diagram's "+3 →" labels and "Common difference = 3. Next term = 20."
are plain HTML. Sequences written as number lists are fine.

**(g)** T1a–c; T2.

**(h)** None.

---

### 6. Area & Perimeter

**(a)** `https://mathswins.co.uk/parents/area-perimeter/` · "Area & Perimeter — A Parent's Guide" · KS3 · family B

**(b)** "Play New Shapes on MaffsGames" → `new-shapes`. It is in `games/` and the roster, and live on
the portal. Level fit PARTLY: Year 6 bank. Topic fit **poor**: parallelograms, trapezia and prisms,
none of which the guide teaches.

**(c) Worked examples**

| Example | Guide's answer | Recomputed | Result |
|---|---|---|---|
| 8 cm × 5 cm rectangle: area, perimeter | 40 cm², 26 cm | 40, 26 | ✓ |
| 10 cm × 4 cm: area, perimeter | 40 cm², 28 cm | 40, 28 | ✓ |
| Triangle, base 6, height 4 | 12 cm² | 12 | ✓ |

**(d) Mathematical claims**

| Claim | Verdict | Reason |
|---|---|---|
| Area is in square units; perimeter is a length | OK | — |
| "A shape can have a large area but a small perimeter, or vice versa." | OK | True comparing two shapes, as the 8 × 5 against 10 × 4 example shows. Not without limit, since area ≤ P² ÷ 4π, but the guide doesn't claim that |
| "Perimeter of a rectangle = 2 × (length + width)"; area formulas | OK | — |
| "a triangle is exactly half of a rectangle (if you imagine doubling the triangle to make a rectangle)" | WRONG | Two copies of a triangle make a parallelogram; they make a rectangle only if it is right-angled. The standard argument is half the rectangle on the same base and height |
| "Remind them: a triangle is half a rectangle, so you always halve it." | CHECK | The mnemonic inherits the problem above |
| "If they're finding perimeter, they're adding. If they're finding area, they're multiplying." | CHECK | A rectangle-only heuristic. The guide's own perimeter formula multiplies, and compound area adds |
| "The height here must be the perpendicular height" | OK | — |
| "If the triangle is tilted, the height isn't one of the visible sides" | CHECK | The condition is whether the triangle is right-angled, not how it is drawn |
| "marks are lost for this in exams" (cm against cm²) | CHECK | An assessment claim; mark schemes vary on units |

**(e) "How schools teach it" claims**

| Claim | Verdict | Note |
|---|---|---|
| "The approach in schools today is very hands-on at first, then builds towards formulae." | CHECK | — |
| "Students start by drawing shapes on squared paper and literally counting the squares." | CHECK | — |
| "The key insight schools teach is that a triangle is exactly half of a rectangle." | CHECK | The mathematical form of this is WRONG in (d) |
| "Schools spend real time on this distinction." | CHECK | — |
| "Eventually, students tackle L-shapes … by splitting them into rectangles." | CHECK | — |

**(f) Notation not in LaTeX:** "Students often calculate base × height and forget to halve" (plain
expression) and "Forgetting the ½ for triangles" (Unicode fraction). Units (cm²) are fine by §7.1.1.

**(g)** "It's free, it's fun, and there's no sign-up needed." See T6. Cookie banner: T2.

**(h)** "If they're finding perimeter, they're adding" against the guide's own
"Perimeter = 2 × (length + width)".

---

### 7. Angles

**(a)** `https://mathswins.co.uk/parents/angles/` · "Angles — A Parent's Guide" · KS3 · family B

**(b)** "Play Angle Ace on MaffsGames" → `angle-ace`. It is in `games/` and the roster, and live on the
portal. Level fit PARTLY: a bare link opens **GCSE**, and the game has no KS3 bank. Topic fit good.

**(c) Worked examples**

| Example | Guide's answer | Recomputed | Result |
|---|---|---|---|
| Straight line, one angle 65° | 115° | 115 | ✓ |
| 42°; 90° | 138°; 90° | 138; 90 | ✓ |
| Triangle 50°, 70° | 60° | 60 | ✓ |
| Triangle 40°, 60°, exterior angle | 80°, then 100° | 80, 100 | ✓ with a note: "One side of the triangle continues as a straight line … the angle between the straight line and the triangle's third side" does not say at which vertex. 100° assumes the 80° vertex; at the other two vertices it is 140° or 120° |

**(d) Mathematical claims**

| Claim | Verdict | Reason |
|---|---|---|
| 90°, 180° and 360° landmarks; angles on a line sum to 180°, at a point to 360° | OK | — |
| "Vertically opposite angles are equal … 'vertical' here means they share the same vertex" | OK | Correct, including the etymology |
| "The three interior angles of any triangle always sum to 180°." | OK | — |
| "Measuring from the wrong baseline on a protractor. Protractors have two scales … Students often read the wrong scale" | CHECK | The heading names one error (the baseline) and the text describes another (the scale) |
| "At KS3 and especially at GCSE, students lose marks for writing just the number. Schools expect a reason." | CHECK | GCSE awards marks for reasons when the question asks for them; otherwise the value earns the marks |

**(e) "How schools teach it" claims**

| Claim | Verdict | Note |
|---|---|---|
| "Schools build up angle facts in layers." | CHECK | — |
| "At KS3, your child moves beyond just measuring angles with a protractor." | CHECK | — |
| "Schools expect a reason" | CHECK | See (d) |

**(f) Notation not in LaTeX:** the landmark list writes "Right angle = 90°", "Straight line = 180°",
"Full turn = 360°" as plain text. Otherwise LaTeX.

**(g)** "It's free, works on any device, and there's no sign-up needed." See T6. Cookie banner: T2.

**(h)** None.

---

### 8. Probability

**(a)** `https://mathswins.co.uk/parents/probability/` · "Probability — A Parent's Guide" · KS3 · family B

**(b)** "Play Probability Pioneer on MaffsGames" → `probability-pioneer`. It is in `games/` and the
roster, and live on the portal. Level fit PARTLY: Year 6 bank. Topic fit good.

**(c) Worked examples**

| Example | Guide's answer | Recomputed | Result |
|---|---|---|---|
| P(7), P(< 7), P(3) on a die | 0, 1, 1⁄6 | 0, 1, 1⁄6 | ✓ |
| P(heads) | ½ | ½ | ✓ |
| 30% rain → no rain | 70% | 70% | ✓ |
| P(even) on a die | 3⁄6 = ½ | ½ | ✓ |
| Bag, 3 red and 7 blue: P(red), P(blue), sum | 3⁄10, 7⁄10, 1 | same | ✓ |
| Spinner 1–8, P(prime) | 4⁄8 = ½ (2, 3, 5, 7) | ½ | ✓ |
| Lottery "≈ 1 in 45 million" | — | C(59, 6) = 45,057,474 | ✓ for the UK Lotto jackpot |

**(d) Mathematical claims**

| Claim | Verdict | Reason |
|---|---|---|
| "The scale runs from 0 (impossible) to 1 (certain)." | OK | — |
| P(event) = favourable outcomes ÷ total possible outcomes, "Students learn a single formula" | WRONG | The formula holds only for **equally likely** outcomes, and the guide never says so. Without that condition it gives P(win the lottery) = ½, against the guide's own "≈ 1 in 45 million". DfE P2 names equally likely events explicitly |
| "To convert a fraction to a decimal, divide the top by the bottom. To get a percentage, multiply the decimal by 100." | OK | — |
| "If the probability of something happening is P, then the probability of it not happening is 1 − P." | OK | — |
| "Probabilities of all possible outcomes always add up to 1." | OK | True for an exhaustive set of mutually exclusive outcomes, which is what is meant (DfE P4) |
| "the numerator can never be larger than the denominator" | OK | — |
| Gambler's fallacy; "Each flip is independent." | OK | — |
| "An event is only impossible if its probability is exactly 0." | OK | — |
| "Winning the lottery is extremely unlikely (≈ 1 in 45 million), but someone wins most weeks." | CHECK | The odds are right for the Lotto jackpot. "Someone wins most weeks" is a factual claim this audit could not verify |

**(e) "How schools teach it" claims**

| Claim | Verdict | Note |
|---|---|---|
| "The approach is structured and logical. Students learn a single formula, then practise applying it…" | CHECK | — |
| "Schools expect students to move fluently between all three." | CHECK | — |
| "Students start with dice, coins, and spinners." | CHECK | — |
| "Schools want students to do this automatically." | CHECK | — |

**(f) Notation not in LaTeX:** "The probability of rolling a 3: 1/6" (an ASCII fraction; every other
fraction in the guide is LaTeX); "Total outcomes = 3 + 7 = 10" and "Favourable outcomes = 3" in the
solution panel. "50/50" is idiom and fine.

**(g)** "It's free, it works on any device, and there's no sign-up needed." See T6. Cookie banner: T2.

**(h)** The core formula (no equally-likely condition) against the lottery example.

---

### 9. Mean, Median & Mode

**(a)** `https://mathswins.co.uk/parents/averages/` · "Mean, Median & Mode — A Parent's Guide" · KS3 · family B

**(b)** "Play Stat Attack on MaffsGames" → `stat-attack`. It is in `games/` and the roster, and live on
the portal. Level fit **NO**: GCSE, Core and Level 4 only. Topic fit **poor**: grouped frequency.

**(c) Worked examples**

| Example | Guide's answer | Recomputed | Result |
|---|---|---|---|
| 3, 7, 7, 9, 14: mean, median, mode, range | 8, 7, 7, 11 | 8, 7, 7, 11 | ✓ |
| 14 changed to 100: mean, median | 25.2, 7 | 25.2, 7 | ✓ |
| 2, 5, 8, 12: median | 6.5 | 6.5 | ✓ |

**(d) Mathematical claims**

| Claim | Verdict | Reason |
|---|---|---|
| "there are actually three different types of average" | OK | True at school level |
| Mean formula; "one extreme value can pull it way up or way down" | OK | — |
| "If there's an even number of values, the median is the mean of the two middle ones." | OK | — |
| "The median is brilliant when you have extreme values (outliers), because it ignores them." | OK | Loosely put (the median is resistant, not blind), but right in substance |
| "If no value repeats, there's no mode." | OK | The usual school convention |
| "If two values appear the same number of times, there are two modes." | WRONG | Only if they tie for **most** often. In 1, 1, 2, 2, 3, 3, 3 the 1s and 2s appear equally often, and the mode is 3. The mistakes section later states it correctly |
| "The mode is the only average that works for non-numerical data" | OK | For categorical data |
| Range = highest − lowest; "it's not an average" | OK | — |
| "median = middle (like the median strip in a road…)" | CHECK | "Median strip" is American English; the UK term is "central reservation". The audience is British parents |
| "the mean salary in a company with one very highly paid CEO…" | OK | — |

**(e) "How schools teach it" claims**

| Claim | Verdict | Note |
|---|---|---|
| "Schools teach all three together so students can compare them…" | CHECK | — |
| "The teaching approach emphasises understanding when to use each average…" | CHECK | — |
| The range "is always taught alongside them" | CHECK | — |
| "Exam questions increasingly ask 'Which average best represents this data?'" | CHECK | An assessment-trend claim |
| "Schools spend real time on this reasoning." | CHECK | — |

**(f) Notation not in LaTeX:** none of note. Data lists are plain, which is fine.

**(g)**

| Claim | Verdict | Reason |
|---|---|---|
| "Our Stat Attack game gives your child hands-on practice with mean, median, mode, and range." | WRONG | Stat Attack practises modal class, median class, estimated mean and standard deviation from grouped tables; it has no range and no ungrouped data |

T6 and T2 apply too.

**(h)** "If two values appear the same number of times, there are two modes" (What Your Child Is
Learning) against "multiple modes (if several values tie for most frequent)" (Common Mistakes).

---

### 10. Coordinates & Quadrants

**(a)** `https://mathswins.co.uk/parents/coordinates/` · "Coordinates & Quadrants — A Parent's Guide" · KS3 · family B

**(b)** "Play Four Quadrant Explorer on MaffsGames" → `four-quadrant-explorer`. It is in `games/` and
the roster, and live on the portal. Level fit PARTLY: Year 6 bank. Topic fit good.

**(c) Worked examples**

| Example | Guide's answer | Recomputed | Result |
|---|---|---|---|
| Plot (−3, 4) | Quadrant 2 | Quadrant 2 | ✓ |
| (4, 2), (−1, −5), (6, −3) | Q1, Q3, Q4 | Q1, Q3, Q4 | ✓ |
| Dropped sign: (−3, 4) plotted as (3, 4) | Q1 instead of Q2 | same | ✓ |
| "Plot (2, 1), (5, 1), (5, 4), and (2, 4). What shape have you made?" | "A rectangle." | Sides 3 and 3: a **square** | Correct but misleading. A square is a rectangle, but a child who answers "square" is more precise and would be told otherwise |
| "A point in quadrant 2" | x negative, y positive | same | ✓ |

**(d) Mathematical claims**

| Claim | Verdict | Reason |
|---|---|---|
| (x, y): first horizontal, second vertical; origin (0, 0); axes named correctly | OK | — |
| "The four sections of the grid are numbered 1 to 4, going anticlockwise from the top-right" and the sign table | OK | — |
| "In primary school, your child probably worked with coordinates that were all positive … At KS3, the grid expands. The axes now cross in the middle, creating four sections, and the numbers can be negative." | WRONG | National Curriculum, Year 6 (Geometry, position and direction): "describe positions on the full coordinate grid (all four quadrants)". Four quadrants are KS2 content, and MaffsGames' own Four Quadrant Explorer is a Year 6 game |
| "Swapping x and y. This is the most common error by far." | CHECK | — |
| "exam questions that reference quadrants by number" | CHECK | Uncommon at GCSE |

**(e) "How schools teach it" claims**

| Claim | Verdict | Note |
|---|---|---|
| "Along the Corridor, Up the Stairs … the memory trick that every maths teacher uses" | CHECK | "Every" is an overclaim; the mnemonic itself is common |
| "Students also practise the reverse…" | CHECK | — |
| "A common extension is to plot several points and join them to make a shape." | CHECK | — |

**(f) Notation not in LaTeX:** the quadrant table's signs "(+, +)", "(−, +)", "(−, −)", "(+, −)" use
ASCII hyphen-minus; "number them from -6 to 6"; the four vertices "(2, 1), (5, 1), (5, 4), and (2, 4)"
are plain while every other coordinate is LaTeX; variable letters (x, y) in prose.

**(g)** "It's free, works on any device, and there's no sign-up needed." See T6. Cookie banner: T2.

**(h)** None within the guide. Against the index card, see C1.

---

### 11. Expanding & Factorising

**(a)** `https://mathswins.co.uk/parents/expanding-factorising/` · "Expanding & Factorising — A Parent's Guide to GCSE Algebra" · GCSE · family C.
DfE A4: expanding two binomials and factorising x² + bx + c are underlined (both tiers). Factorising
ax² + bx + c is **bold** (Higher).

**(b)** "Practise Now on MaffsGames" → `quadratic-factoriser`, plus the `/schools` footer link (T4).
In `games/` and the roster, and live on the portal. Level fit YES; topic fit good for factorising,
none for expanding.

**(c) Worked examples**

| Example | Guide's answer | Recomputed | Result |
|---|---|---|---|
| (x + 3)(x + 2) by FOIL | x² + 5x + 6 | x² + 5x + 6 | ✓ |
| (x + 3)² | x² + 6x + 9 | x² + 6x + 9 | ✓ |
| x² − x − 6 | (x − 3)(x + 2), not (x + 3)(x − 2) | same | ✓ |
| Factorise x² + 7x + 12, and check | (x + 3)(x + 4) | same | ✓ |
| Multiply to 20, add to 9 | 4 and 5 | 4, 5 | ✓ |

**(d) Mathematical claims**

| Claim | Verdict | Reason |
|---|---|---|
| Expanding and factorising are inverse processes | OK | — |
| "Find two numbers that multiply to give the last number (6) and add to give the middle number (5)." | OK | Correct for x² + bx + c |
| Parent tip: "find two numbers that multiply to give ___ and add to give ___. That is genuinely the entire method." | WRONG | Only when the coefficient of x² is 1. Factorising ax² + bx + c (DfE A4, Higher), the difference of two squares and taking out a common factor are all GCSE, and MaffsGames' own Quadratic Factoriser has a Higher (a > 1) level |
| "(x + 3)² … The correct answer is x² + 6x + 9. That 6x … comes from x × 3 appearing twice." | OK | — |
| "This is probably the single most common expanding error at GCSE." | CHECK | — |
| "after factorising, always expand the answer to check" | OK | — |

**(e) "How schools teach it" claims**

| Claim | Verdict | Note |
|---|---|---|
| "If you did maths at school, you might remember just being told to 'multiply everything out.' Today, schools use more structured methods…" and "the two most common methods are FOIL … Grid method" | CHECK | FOIL is a long-standing, originally American mnemonic, not a new method. The grid method is also widely used in UK schools |
| "For factorising, the standard method is…" | CHECK | Standard for a = 1 |

**(f) Notation not in LaTeX:** none.

**(g)** "no login, no cost, just maths". OK. Footer: T5, T4. Cookie banner: T2.

**(h)** None within the guide. Against the index card, see C2 (the difference of two squares).

---

### 12. Simultaneous Equations

**(a)** `https://mathswins.co.uk/parents/simultaneous-equations/` · "Simultaneous Equations — A Parent's Guide" · GCSE · family C.
DfE A19: linear/linear is underlined (both tiers); linear/quadratic is bold (Higher).

**(b)** "Practise Now on MaffsGames" → `simultaneous-solver`, plus the `/schools` footer (T4). In
`games/` and the roster, and live on the portal. Level fit YES; topic fit good.

**(c) Worked examples**

| Example | Guide's answer | Recomputed | Result |
|---|---|---|---|
| 3x + y = 10, x + y = 4 | x = 3, y = 1 | 3, 1 | ✓ |
| Subtract (2) from (1) | 2x = 6 | 2x = 6 | ✓ |
| Check in (1) | 9 + 1 = 10 | 10 | ✓ |
| Rearranged (1) | y = 10 − 3x | same | ✓ |
| Two numbers sum 10, differ by 4 | 7 and 3 | 7, 3 | ✓ |

**(d) Mathematical claims**

| Claim | Verdict | Reason |
|---|---|---|
| "There is exactly one pair of values (x = 3, y = 1)" | OK | — |
| Same signs subtract, different signs add | OK | — |
| "If the second equation has −2y and they are subtracting, that −2y becomes +2y." | OK | — |
| "the question almost always carries a mark for checking" | CHECK | Likely false. GCSE mark schemes award method and accuracy marks; this audit knows of no standard "checking" mark. Jon to rule |
| "Parent tip … you can add or subtract whole equations from each other without breaking the balance." | OK | — |

**(e) "How schools teach it" claims**

| Claim | Verdict | Note |
|---|---|---|
| "Schools teach two main methods." | CHECK | DfE A19 also names graphical solution ("find approximate solutions using a graph") |
| "Elimination (the most common method at GCSE)" | CHECK | — |

**(f) Notation not in LaTeX:** none.

**(g)** Footer: T5, T4. Cookie banner: T2.

**(h)** None.

---

### 13. Trigonometry

**(a)** `https://mathswins.co.uk/parents/trigonometry/` · "Trigonometry (SOH CAH TOA) — A Parent's Guide" · GCSE · family C.
DfE G20 and G21: right-angled trigonometry and exact values are underlined (both tiers).

**(b)** Two links, plus the `/schools` footer (T4). Both are in `games/` and the roster, and live on
the portal:

- "Play Trig Wars" → `trig-wars`. Level fit YES; topic fit partial.
- "Play Trig Worms" → `trig-worms`. Level fit YES; topic fit good.

**(c) Worked examples**

| Example | Guide's answer | Recomputed | Result |
|---|---|---|---|
| 30°, hypotenuse 10 cm → opposite | 5 cm | 10 × sin 30° = 5 | ✓ |
| 20 m from a building, looking up at 45° | 20 m | 20 × tan 45° = 20 | ✓ with a note: it assumes the angle is measured from ground level; from eye level, add eye height |
| Twin diagrams, "Looking from angle A" and "Looking from angle B" | Labels swap | Checked against the SVG coordinates. The triangle is (20,160)–(200,160)–(200,30) with the right angle at (200,160). From A, adjacent is the base and opposite the vertical side; from B, they swap; the hypotenuse is the sloping side | ✓ |

**(d) Mathematical claims**

| Claim | Verdict | Reason |
|---|---|---|
| Hypotenuse, opposite, adjacent definitions; "the hypotenuse never changes" | OK | — |
| sin, cos and tan ratio definitions | OK | — |
| "At GCSE, angles are always in degrees." | OK | DfE A12: "with arguments in degrees" |
| Calculator "D"/"DEG" against "R"/"RAD" | OK | — |
| "We know sin(30°) = 0.5" | OK | DfE G21 exact values |
| "The method your child follows is always the same three steps: label, choose, rearrange and solve … use a calculator" | CHECK | The guide says trigonometry finds "sides and angles", but never shows finding an angle, which needs the inverse functions (sin⁻¹ etc.). The index card promises both |
| "This is the single most common mistake" / "number one source of wrong answers" | CHECK | — |
| Trig Wars described as "Battle-style trig practice — fast rounds, instant feedback" | CHECK | Trig Wars is an artillery game (set angle and power; V<sub>x</sub>/V<sub>y</sub> panel), not quick SOH CAH TOA rounds (`.claude/rules/help-audit.md`) |

**(e) "How schools teach it" claims**

| Claim | Verdict | Note |
|---|---|---|
| "The mnemonic SOH CAH TOA is still the standard way to remember the three ratios." | CHECK | — |
| "The method your child follows is always the same three steps" | CHECK | See (d) |

**(f) Notation not in LaTeX:** the three SOH CAH TOA cards read "Sin = Opp / Hyp", "Cos = Adj / Hyp",
"Tan = Opp / Adj" as plain text with ASCII "/". The same ratios are LaTeX fractions two lines below.

**(g)** Footer: T5, T4. Cookie banner: T2.

**(h)** None.

---

### 14. Circle Theorems

**(a)** `https://mathswins.co.uk/parents/circle-theorems/` · "Circle Theorems — A Parent's Guide to GCSE Geometry" · GCSE · family C.
**Wholly Higher tier**: DfE G10 is bold. The guide does not say so.

**(b)** "Practise Now on MaffsGames" → `circle-theorem-spotter`, plus the `/schools` footer (T4). In
`games/` and the roster, and live on the portal. Level fit YES; topic fit good. Open defect: to-do
§1.3.

**(c) Worked examples**

| Example | Guide's answer | Recomputed | Result |
|---|---|---|---|
| Angle at the centre 80° → at the circumference | 40° | 40 | ✓ |
| Misconception: doubling | 160° | 160 | ✓ |

**(d) Mathematical claims**

| Claim | Verdict | Reason |
|---|---|---|
| Theorems 1–7 as stated (centre, semicircle, same segment, cyclic quadrilateral, tangent and radius, two tangents, alternate segment) | OK | Each is correctly stated |
| "there are only seven to learn" / "seven main theorems" | CHECK | Lists vary. Many include "the perpendicular from the centre to a chord bisects the chord", which is not here. MaffsGames' own game also says seven |
| "Your child does not need to prove these theorems — they just need to recognise which one applies and state it by name." | WRONG | DfE G10: "apply and **prove** the standard circle theorems … and use them to prove related results". The index card says "the proofs behind them" |
| "At GCSE, both the angle and the reason are required for full marks." / "Finding the correct angle is only half the marks." | CHECK | True when the question asks for reasons, which the guide then says ("The exam will say 'give a reason'"). "Half the marks" varies by question |
| "this topic is less about calculation and more about pattern recognition" | CHECK | Pedagogy |
| Conversation starter: "the centre angle should be exactly double the circumference angle" | OK | True when the circumference point is on the major arc, which the described construction implies |

**(e) "How schools teach it" claims**

| Claim | Verdict | Note |
|---|---|---|
| "Schools teach students to learn each theorem, recognise it in a diagram, and — crucially — state the theorem as the reason." | CHECK | — |

**(f) Notation not in LaTeX:** none. Angles in words ("80 degrees") are prose.

**(g)** Footer: T5, T4. Cookie banner: T2.

**(h)** None within the guide. Against the index card, see C3 (proofs).

---

### 15. Standard Form

**(a)** `https://mathswins.co.uk/parents/standard-form/` · "Standard Form — A Parent's Guide" · GCSE · family C.
DfE N9 is standard (both tiers).

**(b)** "Practise Now on MaffsGames" → `standard-form-blitz`, plus the `/schools` footer (T4). In
`games/` and the roster, and live on the portal. Level fit YES; topic fit good.

**(c) Worked examples**

| Example | Guide's answer | Recomputed | Result |
|---|---|---|---|
| 3,400,000; 0.00045 | 3.4 × 10⁶; 4.5 × 10⁻⁴ | same | ✓ |
| Sun distance | 1.5 × 10⁸ km | 150,000,000 | ✓ |
| Table: 56,000; 7,200,000; 0.003; 0.0000081 | 5.6 × 10⁴; 7.2 × 10⁶; 3 × 10⁻³; 8.1 × 10⁻⁶ | same | ✓ |
| 34 × 10⁵ is not standard form | = 3.4 × 10⁶ | same value | ✓ |
| 4.5 × 10⁴ against 4.5 × 10⁻⁴ | 45,000 against 0.00045 | same | ✓ |
| (3 × 10⁴)(2 × 10³) | 6 × 10⁷ | 6 × 10⁷ | ✓ |
| Earth "5,970,000,000,000,000,000,000,000 kg" | 5.97 × 10²⁴ | 25 digits → 10²⁴ | ✓ |

**(d) Mathematical claims**

| Claim | Verdict | Reason |
|---|---|---|
| "the first number must be between 1 and 10 (including 1, but not 10)" | OK | — |
| Big numbers get positive powers, small numbers negative | OK | For numbers ≥ 10 and < 1; 1 ≤ n < 10 gets 10⁰ |
| "The power tells you 'how many zeros' in a sense — 10⁶ means a million" | CHECK | The "number of zeros" reading is the misconception teachers try to head off: 3.4 × 10⁶ = 3,400,000 has five zeros. True only of the bare power of 10 |
| "when multiplying, add the powers. When dividing, subtract them. And always check the result is still in standard form." | OK | The front numbers multiply too; the example shows it |
| "This loses marks every time." (34 × 10⁵) | CHECK | An assessment claim |
| Practise blurb: "convert numbers against the clock" / "a fast-paced challenge" | CHECK | `.claude/rules/timer-policy.md` lists Standard Form Blitz under **hidden count-up**: no visible clock, time shown only on the results screen |

**(e) "How schools teach it" claims**

| Claim | Verdict | Note |
|---|---|---|
| "The method is based on counting how many places the decimal point moves" | CHECK | Much current UK guidance (NCETM, for example) teaches that the digits move against a fixed decimal point |

**(f) Notation not in LaTeX:** the table's "Power" column (+4, +6, -3, -6) is plain text with ASCII
hyphen-minus. Large numbers written out in full are fine.

**(g)** Footer: T5, T4. Cookie banner: T2.

**(h)** None.

---

### 16. Indices & Surds

**(a)** `https://mathswins.co.uk/parents/indices-surds/` · "Indices & Surds — A Parent's Guide to GCSE Maths" · GCSE · family D.
**Partly Higher**: surds are DfE N8 (bold); fractional indices are N7 (bold). The guide does not say so.

**(b)** Two links, both in `games/` and the roster, and live on the portal:

- "Index Laws Game →" → `index-laws`. Level fit YES; topic fit good.
- "Surd Simplifier Game →" → `surd-simplifier`. Level fit YES; topic fit good.

**(c) Worked examples**

| Example | Guide's answer | Recomputed | Result |
|---|---|---|---|
| √50 | 5√2 | 7.0711 = 5 × 1.4142 | ✓ |
| x³ × x⁴ | x⁷ | x⁷ | ✓ |
| √8 | 2√2 | 2.8284 = 2 × 1.4142 | ✓ |
| 2⁻³ | 1⁄8 | 1⁄8 | ✓ |
| 3² × 3⁴ | 3⁶ = 729 | 729 | ✓ |

**(d) Mathematical claims**

| Claim | Verdict | Reason |
|---|---|---|
| "The small raised number … tells you how many times to multiply the base by itself." | CHECK | x³ = x × x × x multiplies the base by itself twice. The usual precise wording is "how many times the base is used as a factor" |
| "Surds are roots that can't be written as exact decimals." | CHECK | Right for roots of whole numbers. Wrong in general: √(1⁄9) = 1⁄3 has no exact decimal and is not a surd. The standard definition is an irrational root |
| "Students learn six index laws that cover every situation" | WRONG | The list has no (ab)ⁿ = aⁿbⁿ, which GCSE needs for, say, (2x³)⁴ = 16x¹² |
| Multiply, divide, power-of-a-power, negative and fractional index laws | OK | — |
| "Zero index: anything to the power 0 is 1 — x⁰ = 1" | WRONG | Minor: needs x ≠ 0 |
| "find the largest square number that divides into it" | OK | — |
| "exam questions often say 'give your answer in exact form'" | OK | — |

**(e) "How schools teach it" claims**

| Claim | Verdict | Note |
|---|---|---|
| "Students learn six index laws" | CHECK | See (d) |
| "For surds, the key skill is simplifying by finding square factors" | CHECK | GCSE also asks for rationalising denominators (DfE N8), which the guide omits |

**(f) Notation not in LaTeX:** none. "1.41421356…" is a decimal, which is fine.

**(g)** "Free games on MaffsGames — no sign-up, no data collected, safe for children". See T1a–c.
Cookie banner: T2.

**(h)** None.

---

### 17. Graph Transformations

**(a)** `https://mathswins.co.uk/parents/graphs-transformations/` · "Graph Transformations — A Parent's Guide" · GCSE · family D.
**Wholly Higher**: DfE A13 is bold, and it covers **translations and reflections only**.

**(b)** "Graph Transformer Game →" → `graph-transformer`. It is in `games/` and the roster, and live on
the portal. Level fit YES; topic fit good.

**(c) Worked examples**

| Example | Guide's answer | Recomputed | Result |
|---|---|---|---|
| y = (x − 3)² from y = x² | right 3, vertex (3, 0) | same | ✓ |
| y = x² + 3 | up 3, vertex (0, 3) | same | ✓ |
| Table examples: f(x) + 3, f(x + 2), −f(x), f(−x) | up 3, left 2, reflect in x-axis, reflect in y-axis | same | ✓ |
| f(x + 2) as a column vector | (−2, 0) | (−2, 0) | ✓ |

**(d) Mathematical claims**

| Claim | Verdict | Reason |
|---|---|---|
| "Your child is learning to transform graphs — … translations, … reflections, and stretching or squashing them." (and the subtitle, and examiners wanting "stretch") | WRONG | Stretches are not GCSE content: DfE A13 is "sketch translations and reflections of a given function". MaffsGames' own Graph Transformer: "GCSE: Translations and reflections only. A-Level: Adds vertical and horizontal stretches." |
| The four-row table (f(x) + a, f(x + a), −f(x), f(−x)) | OK | All correct |
| "changes inside the bracket … do the opposite of what you'd expect … Changes outside the bracket … do exactly what you'd expect" | OK | As a heuristic for these four transformations |
| "f(x + 2) reaches each y-value 2 units sooner" | OK | — |
| "This is the single most common error." | CHECK | — |
| "Marks are lost for imprecise descriptions." | CHECK | An assessment claim; plausible |

**(e) "How schools teach it" claims**

| Claim | Verdict | Note |
|---|---|---|
| "Students learn four core transformations using function notation" | CHECK | The count is right for GCSE, and contradicts the guide's own stretches |
| "Schools insist on precise language: say 'translate' not 'move'…" | CHECK | — |

**(f) Notation not in LaTeX:** none. "(\(U\)-shape)" sets a prose letter in maths italic; cosmetic.

**(g)** "Free game on MaffsGames — no sign-up, no data collected, safe for children". See T1a–c.
Cookie banner: T2.

**(h)** The introduction, subtitle and mistakes section include stretches; the table of transformations
schools teach has four rows and no stretch. Against the index card, see C5.

---

### 18. Pythagoras' Theorem

**(a)** `https://mathswins.co.uk/parents/pythagoras/` · "Pythagoras' Theorem — A Parent's Guide" · GCSE · family D.
DfE G20 is underlined (both tiers). Pythagoras is also KS3 National Curriculum content.

**(b)** "Coordinate Geometry Dash →" → `coordinate-geometry-dash`. It is in `games/` and the roster, and
live on the portal. Level fit YES. Topic fit **poor**: 3 of 45 questions, one of them defective
(below).

**(c) Worked examples**

| Example | Guide's answer | Recomputed | Result |
|---|---|---|---|
| Legs 6, 8 | 10 | 10 | ✓ |
| Hypotenuse 13, leg 5 | 12 | 12 | ✓ |
| c² = 169 misconception | 13 | 13 | ✓ |
| Legs 5 cm, 12 cm | 13 cm | 13 | ✓ |
| Hypotenuse 10, leg 6 | 8 | 8 | ✓ |

**(d) Mathematical claims**

| Claim | Verdict | Reason |
|---|---|---|
| a² + b² = c², with c the hypotenuse, "always opposite the right angle" | OK | — |
| "The other two sides are called the 'legs' or 'shorter sides'." | CHECK | "Legs" is American usage; UK teaching says "shorter sides" |
| "It only works in right-angled triangles (for other triangles, they'll use trigonometry or the cosine rule later)." | OK | — |
| "If the triangle doesn't have one, the formula gives a wrong answer — no error message" | OK | — |
| "if the answer comes out bigger than the hypotenuse, something has gone wrong" | OK | — |

**(e) "How schools teach it" claims**

| Claim | Verdict | Note |
|---|---|---|
| "The method follows three clear steps" | CHECK | — |

**(f) Notation not in LaTeX:** none. Units run into numbers ("5cm", `13\text{cm}`); style only.

**(g)** T1a–c; T2.

**(h)** None.

---

### 19. Probability Trees

**(a)** `https://mathswins.co.uk/parents/probability-trees/` · "Probability Trees — A Parent's Guide" · GCSE · family D.
DfE P8, tree diagrams for combined events, is underlined (both tiers). P9, conditional probability,
is bold (Higher).

**(b)** "Probability Paradox Game →" → `probability-paradox`. It is in `games/` and the roster, and live
on the portal. Level fit YES; topic fit partial: its tree-diagram mode is badged A-Level.

**(c) Worked examples**

| Example | Guide's answer | Recomputed | Result |
|---|---|---|---|
| Rain both days, 0.3 each | 0.09 (not 0.6) | 0.09 | ✓ |
| P(no rain) | 0.7 | 0.7 | ✓ |
| At least one head in two flips | HH, HT, TH | 3 paths | ✓ |
| Rain at least once | 1 − 0.49 = 0.51 | 0.51 | ✓ |

**(d) Mathematical claims**

| Claim | Verdict | Reason |
|---|---|---|
| "Along a branch (AND) = multiply. Between branches (OR) = add." | OK | For the paths of a tree, which are mutually exclusive |
| "At each split, the probabilities must add up to 1." / all end probabilities total 1 | OK | — |
| "P(at least one) = 1 − P(none)" | OK | — |
| Rain example: "the probability of rain on any day is 0.3", and both-days = 0.3 × 0.3 | CHECK | Assumes independence without saying so. DfE P8 asks students to "know the underlying assumptions", and consecutive days' weather is not independent. The guide never mentions independence or how second-branch probabilities change for dependent events, though it cites "picking two sweets from a bag" |
| "Check: slightly more likely than not … there's a 30% chance each day, so over two days you'd expect rain more often than not." | CHECK | The intuition offered is 30% + 30%, the adding misconception the same guide warns against. 0.51 is only just over ½ |

**(e) "How schools teach it" claims**

| Claim | Verdict | Note |
|---|---|---|
| "The method is systematic: draw, label, multiply along, add paths" | CHECK | — |

**(f) Notation not in LaTeX:** "P(rain) = 0.3", "P(rain again) = 0.3" and "P(no rain) must be 0.7" are
plain text; the other probabilities in the guide are LaTeX.

**(g)** T1a–c; T2.

**(h)** The "intuitive" check leans on addition, which Common Mistakes forbids. Against the index card,
see C4 (dependent events, conditional probability).

---

### 20. Statistics & Data

**(a)** `https://mathswins.co.uk/parents/statistics-data/` · "Statistics & Data — A Parent's Guide to GCSE Maths" · GCSE · family D.
**Partly Higher**: histograms and cumulative frequency are DfE S3 (bold); box plots are S4 (bold).
The guide does not say so.

**(b)** "Chart Interrogator Game →" → `chart-interrogator`. It is in `games/` and the roster, and live
on the portal. Level fit YES; topic fit good. Open defects: to-do §1.8 and §1.15–1.18.

**(c) Worked examples**

| Example | Guide's answer | Recomputed | Result |
|---|---|---|---|
| Box plot Q1 = 30, Q3 = 60 → IQR | 30 | 30 | ✓ |

**(d) Mathematical claims**

| Claim | Verdict | Reason |
|---|---|---|
| "Histograms — displaying grouped continuous data using frequency density (not just bar height)" | CHECK | Muddled. In a histogram the bar **height** is frequency density and the **area** represents frequency. The phrase suggests density is something other than height |
| Box plot five values | OK | — |
| Positive, negative and no correlation definitions | OK | — |
| IQR = Q3 − Q1, "the spread of the middle 50%", "more reliable than the range because it ignores outliers" | OK | "Ignores" is loose (resistant is the idea) but right in substance |
| "on cumulative frequency diagrams, students read across from the frequency axis when they should read up from it (or vice versa)" | CHECK | Muddled. You read across from the cumulative frequency axis to the curve and down to the value axis, or up from the value axis; you cannot "read up from" the vertical axis |
| "'the more hours you revise, the more marks you get' loses marks. The correct phrasing is 'there is a positive correlation…'" | CHECK | GCSE mark schemes commonly accept "as x increases, y increases" in context as a description of positive correlation. It is the guide's own definition two sections earlier |
| "An IQR of 30 means there is a fairly wide spread in the central half of the data." | CHECK | Spread is only "wide" against something; the guide's own advice is to compare distributions |
| "What fraction of the data lies between 30 and 60? Answer: exactly half (50%), by definition of quartiles." | WRONG | Approximately half. With the 7 values 1–7 and the (n + 1)/4 convention, Q1 = 2 and Q3 = 6 enclose 5 of 7 |

**(e) "How schools teach it" claims**

| Claim | Verdict | Note |
|---|---|---|
| "Students are taught to compare distributions using two measures: an average (usually the median) and a measure of spread (usually the range or interquartile range)" | CHECK | — |
| "For scatter graphs, they learn to describe correlation" | CHECK | — |
| "…is what examiners want" (answering in context) | CHECK | — |

**(f) Notation not in LaTeX:** "(Q1)" and "(Q3)" in prose are plain, against LaTeX `Q_3 - Q_1` in the
formula; the box-plot values list "Minimum = 15" etc. as plain labels.

**(g)** T1a–c; T2.

**(h)** "Positive correlation — as one variable increases, so does the other" (How Schools Teach)
against "'the more hours you revise, the more marks you get' loses marks" (Common Mistakes).

---

## Redirect map (proposal only; nothing is created)

`mathswins.co.uk` is on Cloudflare (the MathsWins repo's `cloudflare-worker/wrangler.toml` names the
zone), so the same edge Redirect Rule used for `maffsgames.com` (`docs/domain-maffsgames-com.md`)
would give a real 301 here, provided the apex records are Proxied (the trap that doc records). GitHub Pages alone cannot. `maffsgames.co.uk` has no `/parents/` path
today, so there are no collisions. The MathsWins `sitemap.xml` lists all 21 URLs and would need them
removed.

| Old URL | Proposed new URL |
|---|---|
| `https://mathswins.co.uk/parents/` | `https://maffsgames.co.uk/parents/` |
| `https://mathswins.co.uk/parents/negative-numbers/` | `https://maffsgames.co.uk/parents/negative-numbers/` |
| `https://mathswins.co.uk/parents/algebra-basics/` | `https://maffsgames.co.uk/parents/algebra-basics/` |
| `https://mathswins.co.uk/parents/fractions/` | `https://maffsgames.co.uk/parents/fractions/` |
| `https://mathswins.co.uk/parents/ratio-proportion/` | `https://maffsgames.co.uk/parents/ratio-proportion/` |
| `https://mathswins.co.uk/parents/sequences/` | `https://maffsgames.co.uk/parents/sequences/` |
| `https://mathswins.co.uk/parents/area-perimeter/` | `https://maffsgames.co.uk/parents/area-perimeter/` |
| `https://mathswins.co.uk/parents/angles/` | `https://maffsgames.co.uk/parents/angles/` |
| `https://mathswins.co.uk/parents/probability/` | `https://maffsgames.co.uk/parents/probability/` |
| `https://mathswins.co.uk/parents/averages/` | `https://maffsgames.co.uk/parents/averages/` |
| `https://mathswins.co.uk/parents/coordinates/` | `https://maffsgames.co.uk/parents/coordinates/` |
| `https://mathswins.co.uk/parents/expanding-factorising/` | `https://maffsgames.co.uk/parents/expanding-factorising/` |
| `https://mathswins.co.uk/parents/simultaneous-equations/` | `https://maffsgames.co.uk/parents/simultaneous-equations/` |
| `https://mathswins.co.uk/parents/trigonometry/` | `https://maffsgames.co.uk/parents/trigonometry/` |
| `https://mathswins.co.uk/parents/circle-theorems/` | `https://maffsgames.co.uk/parents/circle-theorems/` |
| `https://mathswins.co.uk/parents/standard-form/` | `https://maffsgames.co.uk/parents/standard-form/` |
| `https://mathswins.co.uk/parents/indices-surds/` | `https://maffsgames.co.uk/parents/indices-surds/` |
| `https://mathswins.co.uk/parents/graphs-transformations/` | `https://maffsgames.co.uk/parents/graphs-transformations/` |
| `https://mathswins.co.uk/parents/pythagoras/` | `https://maffsgames.co.uk/parents/pythagoras/` |
| `https://mathswins.co.uk/parents/probability-trees/` | `https://maffsgames.co.uk/parents/probability-trees/` |
| `https://mathswins.co.uk/parents/statistics-data/` | `https://maffsgames.co.uk/parents/statistics-data/` |

---

## Outside (a)–(h): things the migration must not carry across

These are not claims, so they have no verdict, but each page carries them and each would be wrong on
MaffsGames:

- **MathsWins' GA4 property `G-7GTLYCZMXN`** in consent mode, with the cookie banner that grants
  `analytics_storage` on Accept. It is on all 21 pages. MaffsGames uses `G-992JLHLP2D` via `mfg()`,
  cookieless.
- **`<script src="/auth/mw-auth.js">`**, MathsWins' sign-in script, on all 21 pages.
- **Canonical, `og:url`, `og:image` and `twitter:image`** pointing at `mathswins.co.uk`, and the
  MathsWins brand colours and fonts (Bebas Neue, Crimson Pro). The section gets a look of its own,
  not the portal's and not the games' (Jon's ruling, below).
- **KaTeX 0.16.9** from jsDelivr with auto-render on `$$…$$` and `\(…\)`. The math delimiters carry
  over as they are, but mixed prose and maths should go through `MaffsText` (canon §7.1).

## A live MaffsGames defect found in passing (not in this contract; reported, not fixed)

`games/coordinate-geometry-dash/index.html:233`: "A = (0, 0) and B = (5, 5). Distance AB?" has
options `5√2`, `10`, `5`, `√50`, with `correct: "5√2"`. √50 **is** 5√2, so a student who picks √50 is
marked wrong for a correct answer. The question never asks for simplest form, and the game's own
explanation concedes it: "Note: 5√2 and √50 are the same — pick the simplified form."

`check-banks.py` B2 compares options as strings, so it cannot see equal values written differently;
this is layer C territory (`docs/checker-tier4-design.md`). It is one of the three Pythagoras
questions the Pythagoras guide's link leads to. By the to-do's own rule, a live bug goes in §1 as a
bug. Filing it is Jon's call, since this contract permits no other file.

**Update, 28 Sep (after this audit merged):** fixed in PR #8, filed as to-do §1.24. The √50 option is
now 50, the forgotten-square-root error, by Jon's ruling. The scan it prompted found the same shape in
10 more games (`docs/scan-value-equivalent-options.md`).

## Method

- **Guides:** every guide was read in full, from source HTML and from a text extraction that keeps
  the LaTeX, headings, SVG labels and links (scripts in the session scratchpad, not committed).
- **Template sentences:** found by a scripted count of every sentence of 12 or more characters across
  the 20 files, keeping those in 3 or more. Near-verbatim variants were grouped by hand.
- **Arithmetic:** recomputed by a script with exact fractions where it matters. 65 assertions, 0
  failures. This includes the p² = 100 check behind the fractions finding and C(59, 6) for the
  lottery.
- **Links:** each checked against:
  - `games/<slug>/index.html` on `origin/main`;
  - the roster;
  - the portal's cards (all 94 roster games have one; `the-perfect-prank` is the only folder
    without);
  - each game's own level-routing code, for what a bare link opens.
- **Notation (f):** a scripted scan for operators, fractions, ASCII minus signs and powers outside
  `\(…\)`/`$$…$$`, then read by hand against canon §7.1.1's scope (expressions, not units).
- **Curriculum:** GCSE tier and content references are from `data/dfe-gcse-parts.json`, derived from
  the vendored DfE PDF. KS2 and KS3 references are to the 2014 National Curriculum programmes of
  study and were not re-read from a vendored source here, so Jon should treat them as the auditor's
  citation.
- **Not verified here:** the live pages (network refused); the contract's note that Google Search
  Console shows 8 linked MaffsGames targets; whether the UK Lotto jackpot is won "most weeks".

## Jon's rulings, 28 Sep 2026

Recorded here so the migration contract starts from them. Verbatim:

- **Audience.** "this is a parents section to help with homework, it's not about resit students.
  It's aimed a parents who want to help with homework but lack the skills or the confidence to do
  so."
- **Design.** "I'm happy for the entire parents section to have the same look. It's a stand alone
  section that should have its own feel. Grown up, for adults."
- **Accessibility.** "yes, carry the Aa toggle across."

What follows from them for the findings above:

- **The four template families collapse to one design.** Every TEMPLATE finding (T1–T18) is fixed
  once, in the new template.
- **Its own feel is a new design row.** Canon §7.5 has rows for the portal and for each tier of game,
  but none for adult-facing content. Canon §7.5.1 (theme by lowest tier) does not apply, because the
  reader is the parent, not the child. A KS3 guide and a GCSE guide share one look.
- **The Aa toggle comes across, as one shared component for the whole section.** Today the
  OpenDyslexic font is shared (`schools/assets/opendyslexic.css`, self-hosted), but the toggle itself
  is an inline script copied into each game (90 game files reference its `mfg_accessible` key).
  The parents section should load one shared script, not add another copy.
- **Reuse the `mfg_accessible` key rather than adding one.** `privacy/index.html` says local storage
  is used for exactly "two purposes", accessibility and leaderboard initials. A second
  accessibility key would make that sentence stale. The cost is that on a shared family device, a
  child's setting also applies to the parent, and the reverse. That trade is for the migration
  contract to confirm.

