# Migration record: the parent guides, finding by finding

What happened to every finding in `docs/audit-parent-guides.md` when the 20 MathsWins
parent guides were ported to `maffsgames.co.uk/parents/` on 28 September 2026.

**Source.** `OrthogonalMaffs/MathsWins`, cloned read-only. `main` at `a0557fc`, one branch,
`parents/` last changed by `562a2ee`, five commits in that directory's history
(`080228f`, `cfe8413`, `3d8dbcd`, `530615e`, `562a2ee`), 21 HTML files. Identical to
what the audit quotes, so the contract's "source differs from the audit" STOP IF did not
fire. The clone was made outside this repo and is not vendored here.

**Result.** 19 guides published, 1 HELD. 20 URLs including the hub.

**Second pass, 29 Sep 2026: 20 guides published, 0 HELD, 21 URLs including the hub.** The sections
below are the 28 Sep record, left as written. Where the second pass changed a disposition, the
entry says so and points to **"Second pass"** at the end of this file, which records every change
it made, finding by finding.

---

## How each verdict was treated

The audit gives three verdicts. They are not the same kind of thing, and the migration
contract treats them differently.

| Verdict | Treatment | Why |
|---|---|---|
| **WRONG** | Fixed, with the minimum factual correction. Every numeric one recomputed in `scripts/verify-parent-guides.py`. | A factual error. The contract: "A maths error or contradiction gets the minimum factual correction." |
| **(h) contradiction** | Fixed the same way. | Same clause. |
| **CHECK** | **Carried across unchanged**, listed below so Jon can rule on it. | The audit's own definition of CHECK is "a pedagogy or factual point for Jon". The contract's DO NOT TOUCH forbids changing "wording in a guide beyond the minimum needed to correct a finding (pedagogy and voice are Jon's call)", and the audit was required to mark *every* "how schools teach it" claim CHECK, so treating CHECK as a defect would hold all 20 guides and publish nothing. |

Two consequences worth stating plainly:

- **Nothing in this migration is a rewrite.** Every per-guide change below is a swap of
  operands, a deleted false clause, or an added qualifier. The prose, the voice and the
  teaching approach are exactly as Jon's author left them.
- **The CHECK list is still open.** 86 per-guide CHECKs and 12 template/index CHECKs are
  live on the site as written. They are not errors, but several are worth Jon's eye; the
  ones this migration would flag first are at the end.

---

## Template findings — fixed once, in `parents/guide.css` / `parents/guide.js` / the page head

The audit found four template families, not one. Per Jon's 28 Sep ruling ("a stand alone
section that should have its own feel. Grown up, for adults") they collapse to a single
look, so every template finding lands in one place.

| # | Finding | Verdict | Disposition |
|---|---|---|---|
| T1a | "No sign-up" | OK | Carried. |
| **T1b** | **"no data collected"** | **WRONG** | **FIXED.** Deleted from all 10 guides and the index FAQ. Replaced by one sentence on every guide: "MaffsGames needs no account and no sign-up; what it records while your child plays is set out on the privacy page", linking `/privacy/`. `grep -r "no data collected" parents/` returns nothing; `verify-parent-guides.py` asserts it. |
| T1c | "(completely) safe for children" | CHECK | Removed as a side effect of T1b — it was in the same sentence. Not replaced. Recorded here because the deletion was incidental, not a ruling. |
| **T2a** | **Cookie banner, "We use cookies for analytics"** | **WRONG** | **FIXED.** The banner, its Accept/Decline handlers, the `mw_cookies` key and GA4 consent mode are not migrated. MaffsGames is cookieless (canon 1.1, `storage: 'none'`) and `privacy/index.html` says it needs no banner. |
| T2b | "No personal data is sold or shared." | OK | Dropped with T2a. True either way; it lived only in the banner. |
| T3 | "from a working maths tutor" | CHECK | Carried on the hub only (the guide footers it appeared in are replaced). Jon's role wording; to-do §1.6 already flags the About page for the same reason. |
| **T4** | **`maffsgames.co.uk/schools` footer link** | **WRONG** | **FIXED.** Gone. All 20 pages carry the standard portal footer. `check-canonical-links.py` passes. |
| T5 | "Free parent guides — no account needed." | OK | Replaced by the portal footer. |
| T6 | "It's free, works on any device, and there's no sign-up needed." | CHECK | **Carried unchanged** on the five family-B guides. "Works on any device" is not something MaffsGames tests or documents. Jon's call. |
| T7–T11 | The five section headings | OK | Carried, normalised to one form. Family B wrote them upper case, family C prefixed "Section N", family D numbered them "1." to "5."; all now read Title Case with no number. Presentation only, no wording changed. |
| **T12** | **"GCSE Parent Guide" makes no tier distinction** | **CHECK** | **FIXED** — see the tier section below. The contract required it. |
| T13 | "KS3 Parent Guide" | OK | Carried as a "KS3" badge. |
| T14 | Family A subtitle shape | OK | Carried. |
| T15 | "This might look intimidating…" | OK | Carried. |
| T16 | "Parent tip" / "Classic mistake" / "Watch out" labels | OK | Carried, restyled. |
| T17 | "Free interactive practice…" | OK | Carried. |
| T18 | MathsWins nav and copyright text | OK | Replaced: MaffsGames nav, one portal footer, one "All parent guides" back link (family D's duplicate second one is gone). |

Also removed, from the audit's "things the migration must not carry across":

- MathsWins' GA4 property `G-7GTLYCZMXN` in consent mode → canon 1.1's `G-992JLHLP2D`
  snippet plus `schools/assets/analytics.js`.
- `<script src="/auth/mw-auth.js">` (MathsWins sign-in) → gone.
- MathsWins canonical, `og:url`, `og:image`, `twitter:image` → canon 2.1's block with
  `https://maffsgames.co.uk/parents/<slug>/`.
- Bebas Neue, Crimson Pro, DM Mono → Outfit (canon 7.5, portal row).
- KaTeX 0.16.9 auto-render on `$$…$$` and `\(…\)` is kept as-is. It is the static-HTML
  equivalent of `MaffsText` (canon 7.1): it renders only the delimited spans and leaves
  the prose between them alone, so the word-spacing defect that rule exists to prevent
  cannot occur. `throwOnError:false` added.

### The Aa toggle

Carried across per Jon's ruling, as **one shared script** (`parents/guide.js`), not a 21st
inline copy. It reuses the existing `mfg_accessible` key, so `privacy/index.html`'s
"two purposes" sentence stays true. The cost the audit named stands: on a shared family
device a child's setting also applies to the parent. Confirmed here as accepted. The
font is the existing self-hosted `schools/assets/opendyslexic.css`.

### GCSE tier badging (T12)

> **Superseded 29 Sep** by one shared badge component and Jon's wording; the hand-written
> `.tier-note` paragraphs below are gone. See "Second pass", step 3.

Read at sub-clause level from `data/dfe-gcse-parts.json` (bold = Higher only), not
flattened to a per-reference yes/no.

| Guide | DfE | Badge | Note on the page |
|---|---|---|---|
| circle-theorems | G10 wholly bold | GCSE · Higher tier | "Higher tier only… if your child is entered for Foundation, this topic will not come up" |
| graphs-transformations | A13 wholly bold | GCSE · Higher tier | same shape |
| indices-surds | N7.1/N7.3 underlined (roots, integer indices), **N7.2 bold** (fractional); N8.2/N8.4 bold (surds) | GCSE · Higher tier in part | names which half is Higher |
| statistics-data | S3 wholly bold; S4.2 bold (box plots), S4.4 bold (quartiles, IQR); S4.1/S4.3 standard | GCSE · Higher tier in part | names which parts are Higher |
| expanding-factorising | A4.7 underlined (x²+bx+c, incl. difference of two squares); A4.8 bold (ax²+bx+c) | GCSE | The guide teaches only the a = 1 case, which is both tiers. The false universality claim is fixed separately (EF-1). |
| simultaneous-equations | A19.1 underlined (linear/linear); A19.2 bold | GCSE | Guide is linear/linear only. |
| trigonometry | G20, G21 underlined | GCSE | Both tiers. |
| pythagoras | G20.1 underlined | GCSE | Both tiers. |
| standard-form | N9 standard | GCSE | Both tiers. |
| probability-trees | P8 underlined; P9 bold (conditional) | GCSE | The guide never covers conditional probability — see C4. |

---

## The hub page, `/parents/`

| # | Finding | Verdict | Disposition |
|---|---|---|---|
| F1 | "Methods have evolved…" | CHECK | Carried. |
| **F2** | **"Long division, grid multiplication, and bar models replace the shortcuts you learned."** | **WRONG** | **FIXED.** Long division *is* the traditional method; the National Curriculum names it as the Year 6 formal written method. Grid multiplication is a step towards the columnar method, not its replacement. Now: "Grid multiplication and bar models are steps on the way to the written methods you learned, rather than replacements for them; long division is still the formal written method the National Curriculum names for Year 6." |
| F3 | "The answers are the same…" | OK | Carried. |
| F4 | "Do I need to be good at maths to help?" | CHECK | Carried. |
| F5 | "What if I teach them the wrong method?" | CHECK | Carried. |
| F6 | "How much should I help with homework?" | CHECK | Carried. |
| **F7** | **"MaffsGames is a free schools platform — no sign-up, no data collected, safe for children."** | **WRONG** | **FIXED.** Now: "MaffsGames is free to use, with no accounts and no sign-up. What it records while your child plays is set out on the privacy page." Retired brand framing gone with it. |
| F8 | "Every game linked… is completely free." | OK | Carried. |
| I1–I3 | Intro claims | CHECK | Carried verbatim, including "from a working maths tutor" (T3). |
| I4 | "KS3 Topics Years 7–9" / "GCSE Topics Years 10–11" | OK | Carried. |
| **C1** | Coordinates card promised "drawing straight-line graphs" | **WRONG** | **FIXED.** → "Plotting points and reading coordinates across all four quadrants." |
| **C2** | Expanding card promised "the difference of two squares" | **WRONG** | **FIXED.** → "Multiplying out brackets and factorising quadratics." |
| **C3** | Circle Theorems card promised "the proofs behind them" | **WRONG** | **FIXED.** → "Angles in circles, tangent rules, and naming the right theorem." |
| **C4** | Probability Trees card promised "independent and dependent events, and conditional probability" | **WRONG** | **FIXED.** → "Tree diagrams, multiplying along branches, and adding between paths." |
| **C5** | Graph Transformations card promised stretches | **WRONG** | **FIXED.** → "Translations, reflections, and how f(x) notation describes them." |
| C6 | Trigonometry card promised "finding sides and angles"; the guide never finds an angle | (audit: "partly met") | **FIXED** the same way. → "SOH CAH TOA, and finding a missing side in a right-angled triangle." |

**Two deliberate departures on the hub, both for Jon:**

1. **The averages card is gone**, because the guide is HELD and a card would 404. 9 KS3
   cards, not 10.
2. **One FAQ entry was ADDED, not ported:** "What do 'Higher tier' and 'Foundation tier'
   mean?" The new tier badges are meaningless to a reader who does not know what a tier
   is, and this audience is defined as parents who lack the confidence to judge the maths.
   It states that the school chooses the tier, Foundation is graded 1–5 and Higher 4–9.
   This is the only prose on the whole section that is neither ported nor a correction.
   Delete it if it is not wanted.

---

## Per-guide record

Every WRONG and every (h) contradiction, guide by guide. CHECK findings are carried and
are not repeated here individually; they are in the audit.

### 1. Negative Numbers — **FIXED**

| ID | Finding | Change |
|---|---|---|
| NN-1 | (d) WRONG + (h): "Adding always means moving right. Subtracting means moving left." Contradicted two paragraphs later by the guide's own "adding a negative is the same as subtracting". | → "Adding a **positive number** means moving right. Subtracting a **positive number** means moving left." Verified: 4 + (−3) = 1, which moved left. |
| NN-2a | (d) WRONG: "two negatives make a positive… only when the signs are next to each other" excludes multiplication and division, the main place the phrase is used. | Added the missing case: "…and when two negative numbers are multiplied or divided (like (−2) × (−3) = 6)". |
| NN-2b | (d) WRONG: the same restriction, restated in Common Mistakes. | Same addition. Verified: (−2) × (−3) = 6, (−6) ÷ (−3) = 2. |

### 2. Algebra Basics — **FIXED** (no WRONG findings; template, links and head only)

### 3. Fractions, Decimals & Percentages — **FIXED**

| ID | Finding | Change |
|---|---|---|
| FR-1 | (d) WRONG: the 0.3 against 0.25 bullet is written backwards ("because 3 is bigger than 25"), and its follow-up is false (0.3 **is** bigger than 0.125). | Operands swapped so the bullet states the real misconception and then refutes it: "Thinking **0.25** is bigger than **0.3** 'because 25 is bigger than 3.'… 30 hundredths is bigger than 25 hundredths, so 0.3 is the larger number. The same faulty logic would wrongly suggest **0.125** is bigger than **0.3**." The now-false sentence "In this case they happen to be right, but their reasoning is wrong" is deleted. |
| FR-2 | (d) WRONG: "'Divide by the percentage' only works for finding 1%." | → **10%**. Recomputed: a ÷ p equals p% of a exactly when p² = 100, scanned over p = 1…100 for four values of a; the only solution is p = 10. |

> **Judgement call, flagged for Jon.** The audit's verdict on FR-1 says "The bullet needs
> rewriting from scratch", which under the contract's STOP IF would hold the whole guide.
> It was not held, because the repair turned out to be two operand swaps and one deleted
> sentence — the bullet's structure, voice and place-value argument are untouched, and the
> corrected text is checkable arithmetic (0.25 < 0.3 and 0.125 < 0.3, both asserted in the
> verify script). If Jon reads that as more than a minimal correction, revert this one
> bullet; nothing else in the guide depends on it.

### 4. Ratio & Proportion — **FIXED** (no WRONG findings)

### 5. Sequences & Patterns — **FIXED** (no WRONG findings)

### 6. Area & Perimeter — **FIXED**

| ID | Finding | Change |
|---|---|---|
| AP-1 | (d) WRONG: "a triangle is exactly half of a rectangle (if you imagine doubling the triangle to make a rectangle)". Two copies of a triangle make a **parallelogram** unless it is right-angled. | → "a triangle is exactly half of **the rectangle with the same base and the same perpendicular height**". Verified with (0,0) (6,0) (1,4): adjacent sides have dot product 6 ≠ 0, so the doubled shape has no right angle; the triangle's area is 12 = ½ × 6 × 4, half the 6 × 4 rectangle. |
| AP-2 | (h) contradiction: "If they're finding perimeter, they're adding" against the guide's own "Perimeter = 2 × (length + width)". | → "they're **adding up the side lengths**". Verified: 2 × (8 + 5) = 8 + 5 + 8 + 5 = 26, so the formula *is* the addition. |

### 7. Angles — **FIXED** (no WRONG findings)

One thing **not** changed, deliberately: the audit's note on the exterior-angle example
("One side of the triangle continues as a straight line" does not say at which vertex —
100° assumes the 80° one; at the others it is 140° or 120°). The audit rated the example
**✓ with a note**, not a MISMATCH: the arithmetic is right and the stated answer is right
for the intended reading. Naming the vertex means rewriting the question stem without
giving the third angle away, which is a question-design decision. **Left for Jon.**

### 8. Probability — **FIXED**

| ID | Finding | Change |
|---|---|---|
| PR-1 | (d) WRONG + (h): P = favourable ÷ total is given with no "equally likely" condition. Without it the formula gives P(win the lottery) = ½, against the guide's own "≈ 1 in 45 million". DfE P2 names equally likely events explicitly. | Two minimal insertions: the formula's lead-in now reads "as long as every outcome is **equally likely** — a fair die, a fair coin, a bag of identical balls", and the plain-English restatement ends "— provided each of those outcomes is equally likely." Verified: C(59, 6) = 45,057,474 ≠ 2. |

### 9. Mean, Median & Mode — **HELD. NOT PUBLISHED.** *(Published 29 Sep against Distinctly Average: see "Second pass".)*

This is the one guide the contract's per-item STOP IF fired on. Three findings, and the
third cannot be closed without a teaching decision:

| ID | Finding | Status |
|---|---|---|
| AV-1 | (d) WRONG + (h): "If two values appear the same number of times, there are two modes." Only if they tie for **most** often — in 1, 1, 2, 2, 3, 3, 3 the mode is 3. The guide's own Common Mistakes states it correctly. | Would be a one-clause fix. Not applied: the guide is not published. |
| AV-2 | (d) CHECK: "median strip" is American English; the UK term is central reservation. | Would be carried (CHECK). |
| **AV-3** | **(g) WRONG: "Our Stat Attack game gives your child hands-on practice with mean, median, mode, and range."** Stat Attack practises modal class, median class, estimated mean and standard deviation from grouped frequency tables. It has no range and no ungrouped data. **Level fit NO**: it declares GCSE, Core and L4, so there is no KS3 level to pass. | **Cannot be fixed minimally.** |

**Why it is held.** The contract's link rule is to pass an explicit `?level=` the game
declares. For a KS3 averages guide, Stat Attack declares none. The alternatives are all
decisions the contract reserves for Jon:

- delete the Let Them Practise section, leaving a guide with no practice;
- keep the link, correct the claim, and recommend a GCSE grouped-data game from a KS3
  guide on ungrouped averages;
- substitute a different game — but the audit's own portfolio scan concludes "**No game
  is built around ungrouped mean, median, mode and range**"; they appear only as scattered
  items in `maths-court`, `spot-the-error`, `terrible-advice` and as 5 "Mean" substitution
  items in `formula-plug-in`.

That is a teaching judgement and a portfolio gap, not a correction. **Jon's ruling needed.**
Once he rules, the guide needs AV-1 applied and the practice section settled; everything
else in it (three worked examples, all recomputed clean by the audit) is ready.

### 10. Coordinates & Quadrants — **FIXED**

| ID | Finding | Change |
|---|---|---|
| CO-1 | (d) WRONG: "At KS3, the grid expands… creating four sections". The full four-quadrant grid is **Year 6** National Curriculum content ("describe positions on the full coordinate grid (all four quadrants)"), and MaffsGames' own Four Quadrant Explorer is a Year 6 game. | → "In the early years of primary school… **By Year 6 the grid has already expanded**: the axes cross in the middle… At KS3 your child keeps working on that full grid." |
| CO-2 | (c) correct but misleading: "Plot (2, 1), (5, 1), (5, 4), (2, 4). What shape have you made?" answered "(A rectangle.)" — it is a square, and a child answering "square" is more precise. | → "(A square, with sides of 3 units — and a square is also a rectangle, because all four of its angles are right angles.)" Verified: all four sides 3.0, diagonals equal. |

### 11. Expanding & Factorising — **FIXED**

| ID | Finding | Change |
|---|---|---|
| EF-1 | (d) WRONG: "find two numbers that multiply to ___ and add to ___. That is genuinely the entire method." False once the coefficient of x² is not 1 (DfE A4.8, Higher), and MaffsGames' own Quadratic Factoriser has an a > 1 level. | → "That is genuinely the entire method **whenever there is nothing in front of the x²**." Verified: no integers multiply to 3 and add to 7, yet 2x² + 7x + 3 = (2x + 1)(x + 3), checked by expansion at x = −5…5. |

### 12. Simultaneous Equations — **FIXED** (no WRONG findings)

Carried as CHECK: "the question almost always carries a mark for checking", which the audit
believes is likely false and flags for Jon's ruling. **Worth his eye** — it is an
assessment claim a parent may act on.

### 13. Trigonometry — **FIXED** (no WRONG findings)

Carried as CHECK: the Trig Wars description ("fast rounds") against a game whose own
briefing says "your first shot is not supposed to hit".

### 14. Circle Theorems — **FIXED**

| ID | Finding | Change |
|---|---|---|
| CT-1 | (d) WRONG: "Your child does not need to prove these theorems". DfE G10 is "apply **and prove** the standard circle theorems… and use them to prove related results". | → "The DfE subject content for Higher tier asks students to apply *and prove* the standard circle theorems, but most exam questions ask your child to recognise which one applies and state it by name." |
| — | Tier | Badge "GCSE · Higher tier" + note. G10 is wholly bold. |

### 15. Standard Form — **FIXED** (no WRONG findings)

Carried as CHECK: "against the clock" / "fast-paced challenge" for Standard Form Blitz,
which `.claude/rules/timer-policy.md` lists as a **hidden count-up** with no visible clock.
**Worth Jon's eye** — it describes a game behaviour that does not exist.

### 16. Indices & Surds — **FIXED**

| ID | Finding | Change |
|---|---|---|
| IS-1 | (d) WRONG: "six index laws that cover every situation". The list has no (ab)ⁿ = aⁿbⁿ, which GCSE needs for e.g. (2x³)⁴. | → "six index laws that **cover most of what they will meet**". Verified: (2x³)⁴ = 16x¹² for x = 1…6, which needs the missing law. **The law itself was not added** — that is new teaching content, Jon's call. |
| IS-2 | (d) WRONG (minor): "anything to the power 0 is 1 — x⁰ = 1", with no x ≠ 0. | → "anything **except zero**, to the power 0, is 1 — x⁰ = 1 for x ≠ 0". Verified: 0ⁿ = 0 for n = 1…4, so the usual xⁿ/xⁿ route to x⁰ divides by zero at x = 0. |
| — | Tier | Badge "GCSE · Higher tier in part" + note naming surds and fractional indices. |

### 17. Graph Transformations — **FIXED**

| ID | Finding | Change |
|---|---|---|
| GT-1 | (d) WRONG + (h): stretches taught as GCSE content in three places. DfE A13 is "sketch translations **and reflections** of a given function", and MaffsGames' own Graph Transformer says "GCSE: Translations and reflections only. A-Level: Adds… stretches." The guide's own four-row table already had no stretch. | Three deletions, no rewriting: subtitle "Moving, **stretching**, and reflecting" → "Moving and reflecting"; intro "…and stretching or squashing them" deleted; Common Mistakes "translate", "reflect", and "stretch" → "translate" and "reflect" (and the matching "move", "flip", "squash"). The three MathsWins meta descriptions that also named stretches are replaced by a new canon 2.1 description that does not. |
| — | Tier | Badge "GCSE · Higher tier" + note. A13 is wholly bold. |

**Not added:** a line saying stretches are A-Level. Deleting the wrong claim is the
minimum; telling the reader where stretches *do* belong is an addition. Jon may want it.

### 18. Pythagoras' Theorem — **FIXED** (no WRONG findings)

Its one link, `coordinate-geometry-dash`, is level-fit YES (`?level=gcse`) but **topic fit
poor**: 3 of its 45 questions use Pythagoras. The guide makes no false claim about the
game — it says only "Free game on MaffsGames" — so there is nothing to correct, and the
audit's portfolio scan records that **no game is built around Pythagoras**. Published with
the link as-is; the gap is Jon's to fill or relink.

### 19. Probability Trees — **FIXED**

| ID | Finding | Change |
|---|---|---|
| PT-1 | (h) contradiction: the "intuitive" check argues "there's a 30% chance each day, so over two days you'd expect rain more often than not" — the adding misconception the same guide forbids two sections earlier. | The false justification is deleted, the conclusion kept: "**Check:** 0.51 is just over a half, so rain at some point over the two days is slightly more likely than not." Verified: 1 − 0.7² = 0.51, while 0.3 + 0.3 = 0.6. |

Carried as CHECK: the guide assumes independence without saying so (DfE P8 asks students
to "know the underlying assumptions", and consecutive days' weather is not independent).
**This is the CHECK most worth Jon's ruling in the whole set** — it is arguably a
mathematical gap rather than a pedagogy preference, but closing it means writing new
teaching content about independence, which the contract does not permit.

### 20. Statistics & Data — **FIXED**

| ID | Finding | Change |
|---|---|---|
| ST-1 | (d) WRONG: "What fraction of the data lies between 30 and 60? Answer: exactly half (50%), by definition of quartiles." It is approximately half. | → "Answer: about half (roughly 50%) — the quartiles cut off roughly a quarter of the data at each end, so with a small data set it will not be exactly a half." Verified: 1…7 with the (n+1)/4 convention gives Q1 = 2, Q3 = 6, enclosing 5 of 7 values. |
| — | Tier | Badge "GCSE · Higher tier in part" + note naming histograms, cumulative frequency, box plots and quartiles/IQR. |

Carried as CHECK: the frequency-density wording, the cumulative-frequency "read across /
read up" wording, and the claim that "the more hours you revise, the more marks you get"
loses marks. The audit rates all three muddled or doubtful. **Worth Jon's eye.**

---

## Game links

Every link now carries an explicit `?level=` **where the game parses one**, chosen from
what the game actually serves, never a bare link resting on a default.

| Guide | Game | Link | Why |
|---|---|---|---|
| negative-numbers | negative-number-line | `?level=year6` | Roster: Year 6 only. Game hard-codes `LEVEL = 'year6'`; the param is inert but states the intent. |
| algebra-basics | like-terms-collector, think-of-a-number | `?level=year6` | Same. |
| fractions | fraction-equivalence, percentage-flip | `?level=ks3` | Both parse `level` and recognise only `year6`; anything else selects the default KS3/GCSE pool, which is what a KS3 guide wants (audit: level fit YES). `ks3` is the roster's declared level and selects that pool. |
| ratio-proportion | split-it | `?level=ks3` | Real `ks3` bank. Note: `split-it` only acts on `level` when `mode` is also given, so the level picker still appears. Game-side, not touched. |
| sequences | sequence-solver | `?level=ks3` | Real `ks3` bank, selected by the param. |
| area-perimeter | new-shapes | `?level=year6` | Roster: Year 6 only. |
| **angles** | **angle-ace** | **`?level=year6`** | **The defect the rule exists for.** A bare link ran `selectLevel('gcse')` — a KS3 guide opening the GCSE bank. `QUESTIONS_BY_LEVEL` has exactly `year6` and `gcse`; there is no KS3 bank. `year6` is the audit's own recommendation, since that bank's button reads "This is real KS3 maths". |
| probability | probability-pioneer | `?level=year6` | Roster: Year 6 only. |
| coordinates | four-quadrant-explorer | `?level=year6` | Roster: Year 6 only. |
| expanding-factorising | quadratic-factoriser | `?level=gcse` | `IMPLEMENTED_LEVELS = ['gcse','higher','formula']`; `gcse` is the a = 1 level the guide teaches. |
| simultaneous-equations | simultaneous-solver | `?level=gcse` | Real `gcse` bank. |
| trigonometry | trig-wars, trig-worms | *(none)* | Neither game parses a level param at all — one content set each (audit-confirmed). There is no level to pass and no default to rest on. |
| circle-theorems | circle-theorem-spotter | *(none)* | Same: one content set, no param. |
| standard-form | standard-form-blitz | `?level=gcse` | Real `gcse` bank. |
| indices-surds | index-laws *(none)*, surd-simplifier `?level=gcse` | | index-laws has one content set and no param; surd-simplifier has a real `gcse` bank. |
| graphs-transformations | graph-transformer | `?level=gcse` | The game only branches on `alevel`; `gcse` is its declared default level and has a `data-level` button. Passing it makes the GCSE ("translations and reflections only") bank explicit. |
| pythagoras | coordinate-geometry-dash | `?level=gcse` | Same shape. |
| probability-trees | probability-paradox | *(none)* | Mode picker, no level param. |
| statistics-data | chart-interrogator | `?level=gcse` | Type and level picker; `gcse` is a real `data-level`. |
| ~~averages~~ | ~~stat-attack~~ | — | **HELD.** No KS3 level exists. |

Links are now site-relative (`../../games/<slug>/`) and no longer carry
`target="_blank" rel="noopener"`, which described a cross-site jump that no longer exists.

---

## STOP IF log

| Condition | Fired? | What happened |
|---|---|---|
| A finding needs rewording beyond a minimal correction, or a teaching judgement | **Yes, once** | `averages` HELD. See above. The FR-1 call is flagged for Jon as a near-miss. |
| `check-site.py` does not discover `/parents/` without a change to the checker | **Yes** | Reported, checker **not** edited. `build_page_list()` globs `games/` and `escape-rooms/` and otherwise walks a hard-coded list of root pages; `/parents/` matches none of it. A whole-site run after the migration gives the same 345 loads as before it, which is the proof. A throwaway Playwright script in the session scratchpad loaded all 20 pages under tier 1's own bar (uncaught exception, console.error, local 404, hung main thread, write hosts blocked): **20 PASS, 0 FAIL**, KaTeX rendering on every guide and the Aa toggle flipping `body.accessible` on all 20. **Open item for Jon: the section is unchecked by CI.** |
| The MathsWins source differs from what the audit quoted | No | `a0557fc` / `562a2ee` / five commits / 21 files, exactly as quoted. |
| More than 5 of 20 guides would be HELD | No | 1 of 20. |
| Any change would need files outside DO NOT TOUCH | No | Nothing under `games/` or `escape-rooms/` changed, no shared JS in `schools/assets/`, no privacy wording, no MathsWins repo write. |

---

## Verification

| Check | Result |
|---|---|
| `scripts/verify-parent-guides.py` | **157 checks, 0 failed.** Recomputes every corrected numeric claim and then asserts the published page carries the corrected wording and not the old one. |
| `scripts/check-site.py` (tiers 1+2) | **345 PASS, 0 FAIL, 0 WARN**, network guard clean. Does not cover `/parents/` — see the STOP IF log. |
| `scripts/check-canonical-links.py` | 170 files scanned, no links to `/schools/` redirects. |
| `scripts/check-banks.py --ci` | Matches the ledger exactly, 94 games. Nothing it covers was touched. |
| Scratchpad Playwright load of `/parents/` | 20 pages, 20 PASS, 0 FAIL. |
| `grep -r "no data collected" parents/` | 0 hits. |
| `sitemap.xml` | 130 URLs, all distinct, parses under `xml.etree`. |

---

## Open for Jon, in the order this migration would ask

> **29 Sep:** items 1, 3, 4, 5 and 6 below were ruled on or closed by the second pass; item 2
> (CI coverage of `/parents/`, to-do item 10) and items 7–9 stay open. The current list is under
> "Second pass" → "Open for Jon now".

1. **`averages`.** Rule on the practice section, then it can ship. Everything else in the
   guide is ready.
2. **`/parents/` is not covered by CI.** Either `check-site.py` gains the section (a
   checker change this contract forbade) or it stays manually checked.
3. **FR-1.** The fractions bullet was corrected rather than held. Read the diff.
4. **The added tier FAQ** on the hub. Keep or delete.
5. **Four CHECK findings that describe something untrue about a game or an exam**, which
   a parent could act on: simultaneous-equations' "mark for checking"; standard-form's
   "against the clock"; trigonometry's "fast rounds" for Trig Wars; averages' Stat Attack
   claim (held with the guide).
6. **probability-trees' unstated independence assumption** (DfE P8 asks for the underlying
   assumptions). Closing it means new teaching content.
7. **T3 / T6** — the author claim ("a working maths tutor") and "works on any device".
8. **Portfolio gaps the audit named**, now visible to parents: no game built around KS3
   area and perimeter, ungrouped averages, or Pythagoras.
9. **The MathsWins redirects.** Not in this contract. The audit's redirect map is a
   proposal; `mathswins.co.uk` is on Cloudflare, so an edge Redirect Rule can give real
   301s, provided the apex records are Proxied. Its `sitemap.xml` must drop all 21 URLs.

---

## Second pass, 29 Sep 2026: Jon's approved corrections, the averages guide, tier badges

The contract: rebase PR #9 onto `main`; apply Jon's approved wording, replacing PR #9's where
it differs; publish the held averages guide against Distinctly Average; badge the four
Higher-tier guides with one shared component; make the recomputation script read from the
pages. **Precondition met:** Distinctly Average is on `main` (PR #10, `597821f`), the roster
declares `KS3, GCSE`, and the game's `IMPLEMENTED_LEVELS = ['ks3', 'gcse']`.

Status words in the tables: **APPLIED** (changed to the approved wording), **KEPT** (PR #9's text
was already correct and equally clear, so left alone), **HELD-FOR-JON** (not edited: it needs more
than a minimal correction, or a teaching call).

### Step 1: rebase and counts

The rebase was onto `origin/main` at `76082fb`. Three files conflicted, all docs: `CLAUDE.md` (the
sitemap line), `docs/canon.md` (the total-games rows) and `docs/todo.md` (the header and START
block). All three were resolved by keeping both sides. Every count was then recomputed from the
tree, not taken from either side:

| Count | PR #9 said | Now | Computed from |
|---|---|---|---|
| Games on the portal | 94 | **95** | roster rows (`.claude/rules/game-roster.md`) |
| `games/` directories | 95 | **96** | `games/*/` (the extra is `the-perfect-prank`) |
| `sitemap.xml` URLs | 130 | **132** = 95 games + 8 rooms + 8 pages + 21 parents | `<loc>` entries, all distinct |
| `/parents/` URLs | 20 | **21** (20 guides + hub) | `parents/*/index.html` + hub; sitemap agrees |
| Guides published | 19 | **20** | same |
| Canonical tags | 137 | **139** (118 on `main` + 21) | `rel="canonical"` across `**/*.html` |
| `check-canonical-links.py` files | 170 | **172** | its own output |
| `verify-parent-guides.py` checks | 157 | **353** | its own output |
| canon: roster rows / portal cards / games the rooms are "not counted in" | 93 / "~130 for 93" / 93 (stale on `main` since before PR #10) | **95 / 133 for 95 / 95** | roster rows; `class="game-card` in `index.html`, and distinct `games/<slug>` on those cards |

Not changed, and flagged instead: canon's **"Coverage (94 live games)"** section. Its body is
leaderboard accounting ("91 games call `submitScore()`", 3 excluded, and now 3 held, including
log-laws' partial gate). Moving only the heading to 95 would make its arithmetic visibly wrong, and
reconciling the body is leaderboard work outside this contract. For reference,
`check-leaderboard-coverage.js` reports 96 directories, 3 excluded, 3 held, coverage OK.

### Step 2: corrections, finding by finding

**`averages`: written, family B content in the new template**, from the MathsWins source at
`a0557fc`, with every earlier audit correction applied.

| Finding | Was (MathsWins) | Now | Status |
|---|---|---|---|
| AV-1, mode | "The value that appears most often. That's it. If no value repeats, there's no mode. If two values appear the same number of times, there are two modes." | "The mode is the value that appears most often. If two values tie for most often, there are two modes. If no value repeats, there is no mode." | APPLIED, verbatim. The non-numerical-data sentence after it is kept (audit OK) |
| Median rule | "The middle value when you put all the numbers in order. If there's an even number of values, the median is the mean of the two middle ones." | "Put the values in order. The median's position is \((n + 1) \div 2\), where \(n\) is how many values there are. For 7 values that's the 4th. For 2, 5, 8, 12 it's \((4 + 1) \div 2 = 2.5\), so halfway between 5 and 8, which is 6.5." | APPLIED, verbatim, with KaTeX for the two expressions. It uses the same terms as Distinctly Average's scaffold card ("(n + 1) ÷ 2", "halfway between"); the script reads both the guide and the game's `renderScaffoldCard` to check this. The outlier sentences after it are kept (audit OK) |
| AV-2 | "median strip" | "central reservation" | APPLIED. See the flags below |
| Exam claim | "Exam questions increasingly ask 'Which average best represents this data? Explain why.'" | "Exam questions often ask which average suits the data best, and why." | APPLIED |
| AV-3 | "Our Stat Attack game gives your child hands-on practice with mean, median, mode, and range." → `stat-attack` | "Our Distinctly Average game gives your child hands-on practice with mean, median, mode, and range." → `../../games/distinctly-average/?level=ks3` | APPLIED. The claim is checked against the game's own KS3 item categories (mean, median, modeUnique, modeBimodal, range) |
| Worked examples | 3, 7, 7, 9, 14 → 8, 7, 7, 11; 14 → 100 gives 25.2 and 7; 2, 5, 8, 12 → 6.5 | unchanged | KEPT, and recomputed from the page |
| T6, T8, (e) CHECKs | "works on any device"; "How Schools Teach It Now" | unchanged | Carried as CHECK, as on the other four family B guides |

**Other guides:**

| Guide | Finding | Was (PR #9) | Now | Status |
|---|---|---|---|---|
| fractions | FR-1 | "Thinking 0.25 is bigger than 0.3 'because 25 is bigger than 3.' Remind them to think about place value: 0.3 = 0.30, and 30 hundredths is bigger than 25 hundredths, so 0.3 is the larger number. The same faulty logic would wrongly suggest 0.125 is bigger than 0.3." | "Thinking 0.25 is bigger than 0.3 because 25 is bigger than 3. Compare in hundredths: 0.30 against 0.25, and 30 beats 25." | APPLIED, verbatim. The 0.125 sentence is deleted. This supersedes PR #9's FR-1 judgement call |
| fractions | FR-2 | "Finding a percentage by dividing by the percentage. To find 20% of 60, some children divide 60 by 20 and get 3. The correct method: 10% of 60 = 6, so 20% = 12. 'Divide by the percentage' only works for finding 10%." | "Dividing by the percentage number (\(60 \div 20 = 3\)) doesn't find 20%. It only happens to work for 10%. To find 20%, find 10% (6) and double it: 12." | APPLIED, verbatim, with KaTeX on the division |
| probability-trees | independence | "Given: the probability of rain on any day is 0.3." | "…is 0.3, assuming the two days are independent (the question will tell you to)." | APPLIED. This closes the CHECK PR #9 called "most worth Jon's ruling" |
| probability-trees | without replacement | none | "With sweets taken out of a bag and not replaced, the second-branch probabilities change." Added after the guide's own sweets example in What Your Child Is Learning | APPLIED |
| probability-trees | PT-1 sense-check | "Check: 0.51 is just over a half, so rain at some point over the two days is slightly more likely than not." | "Check: the chance of rain at least once must be more than 0.3 (one day alone gives that) and less than 0.6 (adding double-counts the both-days case). 0.51 fits." | APPLIED. 0.6 − 0.51 = 0.09 = P(both days), and the script checks exactly that |
| circle-theorems | CT-1 | "The DfE subject content for Higher tier asks students to apply *and prove* the standard circle theorems, but most exam questions ask your child to recognise which one applies and state it by name." | "At Higher tier, your child may be asked to prove theorems as well as apply them." The tip's closing sentence ("If they can match the diagram to the rule, they are most of the way there.") is kept | APPLIED |
| circle-theorems | hub card (C3) | "Angles in circles, tangent rules, and naming the right theorem." | "Angles in circles, tangent rules, and the proofs behind them." (the MathsWins original) | APPLIED. See the flags below |
| graphs-transformations | stretches | removed by PR #9 from the subtitle, intro, mistakes, hub card and meta | unchanged | KEPT: already correct. The script checks that neither "stretch" nor "squash" appears anywhere on the page, head included |
| simultaneous-equations | "mark for checking" | "But the question almost always carries a mark for checking — substitute…" | "Checking catches slips — substitute the values back into both original equations and confirm they work." | APPLIED |
| statistics-data | correlation | "'the more hours you revise, the more marks you get' loses marks. The correct phrasing is 'there is a *positive correlation* between hours of revision and marks scored'. Use the mathematical vocabulary." | "'the more hours you revise, the more marks you get' states it as a certainty. Describe correlation in context, e.g. 'as hours revised increase, marks tend to increase'." | APPLIED. "States it as a certainty" is the one phrase added beyond the contract's words, so that the bullet's kept label and example still read as a mistake. See the flags below |
| statistics-data | ST-1 | "Answer: about half (roughly 50%) — the quartiles cut off roughly a quarter of the data at each end, so with a small data set it will not be exactly a half." | "Answer: about half (roughly 50%), by definition of quartiles." | APPLIED. **PR #9's added clause was itself false**, so it is not kept. For the data 1, …, 8 with the (n + 1)/4 convention, Q1 = 2.25 and Q3 = 6.75, and 4 of the 8 values lie between them: exactly half. For 1, …, 7 it is 5 of 7. "About" is right, and "never exactly" is wrong |
| standard-form | zeros gloss | "The power tells you 'how many zeros' in a sense — \(10^6\) means a million, \(10^{-4}\) means a ten-thousandth." | "…tiny numbers get negative powers — \(10^6\) means a million, \(10^{-4}\) means a ten-thousandth." | APPLIED. The gloss is deleted; its two true examples are kept, joined to the sentence before by the dash |
| hub FAQ | Foundation/Higher | "GCSE maths is sat at one of two tiers, and the school decides which. Foundation is graded 1 to 5; Higher is graded 4 to 9. Some topics are only examined at Higher tier. Where that applies, the guide says so at the top, and the card above is marked." | "GCSE maths has two tiers. Foundation tier is graded 1 to 5. Higher tier is graded 4 to 9, and a grade 3 is allowed on the Higher tier." | APPLIED. I read the contract's "keep only if it states…" as "keep it, stating exactly these facts"; PR #9's version never mentioned the allowed grade 3. Deleted: who decides the tier, and the two sentences about the site's own badges |

**Examiner and mark-scheme claims, softened in one pass.** Every claim of this kind in the guide
bodies and meta descriptions was found by a search for mark and exam wording. The script's EXAM
check fails on any that is left unqualified.

| # | Guide | Was | Now |
|---|---|---|---|
| 1 | angles | "students lose marks for writing just the number" | "students often lose marks…" |
| 2 | area-perimeter | "marks are lost for this in exams" | "marks are often lost…" |
| 3 | circle-theorems | "both the angle and the reason are required for full marks" | "…are usually required…" |
| 4 | circle-theorems | "Finding the correct angle is only half the marks." | "…is often only half the marks." |
| 5 | circle-theorems | "The exam will say 'give a reason for your answer'" | "The exam will usually say…" |
| 6 | circle-theorems | "Just writing '80' with no reason loses them." | "…usually loses them." |
| 7 | circle-theorems | meta and og description: "the reasons examiners want to see" | "…examiners usually want to see" (2 tags) |
| 8 | graphs-transformations | "examiners want 'translate' and 'reflect'" | "examiners usually want…" |
| 9 | graphs-transformations | "Marks are lost for imprecise descriptions." | "Marks are often lost…" |
| 10 | standard-form | "This loses marks every time." | "This usually loses marks." |
| 11 | standard-form | meta and og description: "the mistakes that lose marks" | "…that often lose marks" (2 tags) |
| 12 | statistics-data | "…is what examiners want." | "…is usually what examiners want." |
| 13 | statistics-data | "…the more marks you get' loses marks." | removed by the approved correlation wording |
| 14 | trigonometry | meta and og description: "the labelling mistakes that cost marks" | "…that often cost marks" (2 tags) |
| 15 | simultaneous-equations | "almost always carries a mark for checking" | removed by the contract's own correction |
| 16 | averages | "Exam questions increasingly ask…" | "…often ask…" (the contract's own wording) |

Deliberately not changed:
- **indices-surds'** "exam questions often say 'give your answer in exact form'" is already
  qualified.
- **The two "Easy marks lost" box labels** (circle-theorems, simultaneous-equations) name a
  category rather than assert a mark scheme; the audit rates them T16 OK. They are left as they
  are, for Jon.

**The four CHECK findings that describe something untrue a parent could act on** (PR #9's list, item 5):

| # | Guide | Claim | Outcome |
|---|---|---|---|
| 1 | simultaneous-equations | "the question almost always carries a mark for checking" | Corrected, in the contract's wording (above) |
| 2 | trigonometry | Trig Wars: "Battle-style trig practice — fast rounds, instant feedback." | **WRONG, corrected:** "Battle-style trig practice — instant feedback." Evidence from `games/trig-wars/index.html`: it is turn-based ("You and your opponent fire in turn"); its briefing says "Your first shot is not supposed to hit… Bracketing the target over two or three shots"; and every shot gets a response ("Overshot. Try less power or a shallower angle"). So "instant feedback" is true and "fast rounds" is not. There is no numeric claim to recompute |
| 3 | standard-form | Standard Form Blitz: "a fast-paced challenge", "speed-round practice — convert numbers against the clock" | **HELD-FOR-JON, not edited: the finding's premise is wrong.** The CHECK rested on `timer-policy.md`, which lists the game as a hidden count-up with no score multiplier. The game as built contradicts that doc. Its HUD shows a "Time" cell counting up every 250 ms (`games/standard-form-blitz/index.html:106`, `:231–232`); the hiding rule at `:77` targets the class `.timer`, which never matches the element `#timer`. Correct answers also score `100 / (1 + 0.15·ln(1 + s))`, so a faster answer scores more (`:224`, `:233`). The guide is therefore true of the live game. Which of the game and the policy is wrong is Jon's call, and `games/` is outside this contract. If the game is brought into line with the policy, this blurb becomes false and needs correcting then. Separately, a second, static "0s" (`.timer-text#timerDisplay`, `:108`) sits under the HUD and never updates |
| 4 | averages | "Our Stat Attack game…" | Corrected by the relink to Distinctly Average (above) |

### Step 3: tier badging, one component

**The component.** `parents/guide.js` holds a `TIERS` table (strict JSON between two markers), one
`tierText()` holding the two approved sentences, and `renderTierBadges()`. `parents/guide.css`
adds `.tier-badge` and `.higher-mark`. A guide carries `<p class="tier-badge"
data-tier-badge="<slug>"></p>` directly under its `<h1>`; its hub card carries the same element as
a `<span>`. No page contains badge wording, so a guide and its card cannot drift apart.

The words carry the meaning; the amber is only there to catch the eye. PR #9's hand-written
`.tier-note` paragraphs and its "GCSE · Higher tier" / "Higher in part" badge text are gone from
all four guides and their cards, and the level badge now reads plain "GCSE".

- **Wholly Higher:** "Higher tier only. Foundation-tier students are not examined on this topic."
- **Partly Higher:** "Includes Higher tier content: [sections]."

**What each badge is built from**, read from `data/dfe-gcse-parts.json` (bold = Higher only):

| Guide | Kind | DfE parts (all bold) | Sections named | "Higher" markers in the body |
|---|---|---|---|---|
| circle-theorems | wholly | G10.1 (G10's only part) | none | none; the whole guide is Higher |
| graphs-transformations | wholly | A13.1 (A13's only part) | none | none |
| indices-surds | partly | N7.2 "and fractional" [indices]; N8.2 "surds"; N8.4 "simplify surd expressions… and rationalise denominators" | fractional indices; surds | 6: the fractional-index law; the surds paragraph; the surds method; "Thinking surds can't be simplified"; the √50 worked example; the Surd Simplifier link |
| statistics-data | partly | S3.1 (histograms with equal and unequal class intervals, cumulative frequency graphs); S4.2 (box plots); S4.4 (quartiles and inter-quartile range) | histograms; cumulative frequency; box plots; the interquartile range | 7: the histograms, cumulative frequency and box plots bullets; the IQR paragraph; the two cumulative-frequency mistakes; the box plot worked example |

What was not marked, and why:
- **N7.1 and N7.3** (roots, and integer indices including negative ones) are underlined, so both
  tiers.
- **S4.1 and S4.3** are standard.
- **The Chart Interrogator link** is not marked, because the game also offers stem-and-leaf,
  which both tiers are assessed on.
- **"usually the range or interquartile range"** is not marked, because it is a passing mention
  beside the range.

**One departure from the contract's list, as it instructed.** The contract's audit points named S3
and S4 box plots. The data file also marks **S4.4 (quartiles and interquartile range) bold**, so
it is included. Quartiles appear in the guide only inside the IQR paragraph, the box plot example
and the cumulative frequency bullet, all of which are marked, so the section is named "the
interquartile range".

The script checks four things:
- every listed part is bold;
- a "wholly" guide's statement is bold in every part;
- the badge sits directly under the title;
- the markers on each partly-Higher page match its named sections exactly.

No other guide carries a badge or a marker.

### Step 4: the recomputation script now reads the pages

**Before.** 157 checks. The arithmetic was computed from literals typed into the script, and the
text checks matched fixed phrases. Proof that it never read a figure off a page: on PR #9's own
committed pages, changing area-perimeter's "8 × 5 = 40 cm²" to "= 41" still gave **157 checks, 0
failed**, with the line "PASS 8 x 5 rectangle: area 40 cm2".

**After.** Every check finds its claim on the published page, with the KaTeX source normalised to
plain symbols. It then pulls out the operands and the stated answer, and recomputes the answer
from those operands. A claim it cannot find is a FAIL.

- **353 checks.** 340 read their values from a guide or the hub; 13 read `guide.js`'s `TIERS`
  table and the DfE data.
- **100 of them recompute a figure a page states.**
- **None compares against an answer typed into the script.** One check, PR-1, supplies operands
  the page does not print: UK Lotto's 6-from-59 rule, to test the page's rounded "1 in 45 million".
- **Covered:**
  - the new averages guide throughout;
  - the 10%-only rule, as a scan of r = 1…100 using the page's own 60;
  - the (n + 1) ÷ 2 examples;
  - 0.51 and its bounds;
  - every earlier corrected claim;
  - the tier table against the DfE data;
  - the hub, the sitemap and the guide directories against each other;
  - the audit's own guide count (20: KS3 10, GCSE 10).

**Fault injection, each reverted byte-identical afterwards:**

| Page | Change | Result |
|---|---|---|
| averages | "jump to 25.2" → "25.3" | FAIL AV: "[3, 7, 7, 9, 100] -> mean 253/10" |
| probability-trees | "0.51 fits" → "0.52 fits" | FAIL PT-1, two checks |
| area-perimeter | "= 40 cm²" → "= 41" | FAIL AP-2, two checks (the same fault the old script passed) |

**Why each old wording was false,** recorded here rather than re-proved by the script, because the
text they disprove is no longer on any page. All recomputed on 29 Sep:

- **AV-1:** in 1, 1, 2, 2, 3, 3, 3 the mode is 3 alone.
- **FR-1:** 0.3 > 0.125.
- **ST-1:** for 1, …, 8, exactly half the values lie between Q1 and Q3.
- **EF-1:** no integers multiply to 3 and add to 7, yet 2x² + 7x + 3 = (2x + 1)(x + 3).
- **IS-1:** (2x³)⁴ = 16x¹².
- **AP-1:** the triangle (0,0), (6,0), (1,4) has a dot product of 6 at (0,0), so it has no right
  angle there and its double is a parallelogram; its area is 12 = ½ × 6 × 4.

The script is **still not in CI**; wiring it in is outside this contract. Now that it reads the
pages, a one-line step would make it a guard rather than a record, and that is Jon's call.

### Verification, 29 Sep

| Check | Result |
|---|---|
| `scripts/verify-parent-guides.py` | 353 checks, 0 failed |
| Throwaway Playwright pass over all 21 `/parents/` URLs (tier 1's bar, with `check-site.py`'s write guard imported, since `check-site.py` still does not discover the section: to-do item 10) | **21 PASS, 0 FAIL**. KaTeX renders on all 20 guides (no `katex-error`, no raw delimiters). Each badge's rendered text matches the contract's wording exactly on 4 guides and 4 hub cards, directly under the `<h1>`. 13 markers render. Aa toggles on all 21. The averages link is `?level=ks3`. The tier FAQ opens. 21 write requests blocked, 0 escaped |
| `scripts/check-canonical-links.py` | 172 files, no links to `/schools/` redirects |
| `scripts/check-leaderboard-coverage.js` | Coverage OK |
| `scripts/check-banks.py --ci` | Unreliable in this container, not a result: see the note below. Its inputs (`games/`, the ledger, the bank scripts) are byte-identical to `main`, which CI passes |

**Environment notes.**
- **KaTeX.** This session's egress policy refuses `cdn.jsdelivr.net` (proxy 403 on CONNECT), so
  KaTeX cannot load from its CDN here. For the Playwright pass only, the identical package
  (`katex@0.16.9`) was fetched from the npm registry and served for the CDN URLs. No page was
  changed.
- **Bank extraction.** `extract-banks.py` is nondeterministic here. `boolean-blitz` is read on
  some runs as a 14-item bank from its `LAWS` reference table, which trips B4, and on others as an
  unreadable generator, with other games wobbling too under 4 workers.

### Flags on approved wording (applied as approved, raised for Jon)

1. **Circle theorems hub card, "the proofs behind them".** The guide now says Higher-tier students
   may be asked to prove theorems, but it shows no proof. The card promises a little more than the
   page delivers.
2. **"Central reservation".** The MathsWins line was a word-link: the word "median" is inside
   "median strip". With "central reservation" it becomes a plain analogy (the middle of the road).
3. **Statistics correlation bullet.** It keeps its label ("Describing correlation casually") and
   its example, bridged by "states it as a certainty". Dropping the example would be the cleaner
   edit, but that is a wording call.
4. **Circle theorems tip.** The kept closing sentence ("If they can match the diagram to the rule…")
   has lost the "recognise which one applies and state it by name" that led into it.

### Open for Jon now

1. ~~**HELD-FOR-JON: Standard Form Blitz against `timer-policy.md`**~~ **Ruled by Jon, 29 Sep:
   the game is wrong; `timer-policy.md` stands.** The guide's blurb stays as it is (true of the
   game today). To-do queue item 12 fixes the game and the blurb in the same change.
2. **CI does not cover `/parents/`** (to-do item 10, a separate `check-site.py` contract). Wiring
   `verify-parent-guides.py` into CI is a smaller, separate step.
3. **The four flags** above.
4. **Canon's "Coverage (94 live games)" section** is stale on `main` (step 1). It is leaderboard
   accounting, not a page count, so it is left for its own pass.
5. **Carried from the 28 Sep list:** T3 / T6 (the author claim, "works on any device"); the
   portfolio gaps (KS3 area and perimeter, Pythagoras; ungrouped averages is now filled); the
   MathsWins 301 redirects, which are the next contract.
