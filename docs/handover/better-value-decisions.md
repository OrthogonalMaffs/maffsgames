# Better Value: decisions for Jon (BV-CLAIMS, 14 Oct 2026)

**Ruled by Jon, 15 Oct 2026 (contract BV-RULINGS, `docs/handover/contracts/2026-10-15-bv-rulings.md`):** every
item below except gcse_014, 015, 017 and 018 (batch 2); `docs/handover/cloud.md` lists old and new wording per item.

Options with the arithmetic, for the items where a measure or a ruling is yours to choose. **No option is chosen
here.** The current data (provisional where marked) is what `scripts/verify-better-value-claims.py` checks today;
each item's entries in its KNOWN go when the item is rewritten. Item text is quoted from the page;
`docs/handover/better-value-audit.md` has every item's full arithmetic.

## 1. Two measures in play

### core_031: per month, or the total over each contract (provisional: per month)

Advertised: £18 broadband + £10 line rental a month for 18 months, plus £60 installation. Rival: £32 a month
all-in for 12 months.

| Option | Advertised | Rival | Winner | What changes |
|---|---|---|---|---|
| A. Average monthly cost (the key and explanation today) | (18 × £28 + £60) ÷ 18 = £564 ÷ 18 = **£31.33** | £384 ÷ 12 = **£32** | Advertised, by 67p a month | C2 ("rival … better value over its contract — £384 … vs £564") is true under B's reading, so it must be rewritten false under A |
| B. Total you commit to | **£564** over 18 months | **£384** over 12 months | Rival | Key and explanation flip; the comparison is over unequal periods, so a criterion must make the lock-in itself the cost ("she may move in a year") |
| C. Equal period, with data added | needs the rival's price after month 12 | | | New data: a new real-world context, which stops for Jon (SR-26) |

C1 ("The advertised deal is cheaper — £18/month beats £32/month") passes under A by your ruling: right winner,
wrong figure, and the explanation states £31.33.

### core_037: net profit, or return on investment (provisional: net profit)

Standard: £180 to print, £800 of sales. Premium: £260 to print, £1,120 of sales (40% more).

| Option | Standard | Premium | Winner | What changes |
|---|---|---|---|---|
| A. Net profit (the explanation today) | £800 − £180 = **£620** | £1,120 − £260 = **£860** | Premium, by £240 | Key becomes a verdict ("Premium flyers are better value — £860 vs £620 profit"); C1 ("Standard flyers are better value overall — they cost £80 less") is true under B, so it must be rewritten |
| B. Return on investment | 620 ÷ 180 = **344%** | 860 ÷ 260 = **331%** | Standard | The key flips to standard; the explanation's "the cheaper option is not the better value here" goes |

A plain-words criterion decides it: "She wants the most profit from this one print run" (A), or "Her budget is
fixed and she will spend it all on flyers" (B, where each pound earns more on standard). The key today states
both facts and no verdict.

### core_050: direct cost, or cost including time (provisional: including time)

Buying lunch: 30 weeks × 5 × £5.50 = £825. Meal prep: £40 containers + 30 × £25 ingredients = £790 direct;
45 minutes a week at £11.44 an hour is 30 × 0.75 × £11.44 = £257.40, so £1,047.40 with time.

| Option | Buy | Prep | Winner | What changes |
|---|---|---|---|---|
| A. Direct cost | **£825** | **£790** | Prep, by £35 | C1 ("Meal prep is clearly cheaper — £790 vs £825 … time … costs nothing") becomes true, so it must be rewritten; key becomes a verdict for prep |
| B. Including time (provisional) | **£825** | **£1,047.40** | Buy, by £222.40 | Key becomes a verdict for buying; C4 ("Buying lunch is always better value because time is money") stays a judgement until "always" goes |

The criterion: "She would work those 45 minutes if she did not cook" (B) or "She would not earn in that time" (A).

## 2. Opposite rulings: core_011 against core_042

- **core_011** (sofa) keys wrong "The BNPL store is better because you keep your money for longer, interest-free".
- **core_042** (laptop) keys right "The 0% credit card is better value — she earns £15 interest while the laptop
  costs the same". That is the same reasoning: pay later and keep the money meanwhile.

| Option | core_011 (BNPL £599 in 12 months vs £549 cash now) | core_042 (cash £500 now vs card £500 in month 12, 3% AER) |
|---|---|---|
| A. Interest earned counts in both | Needs a rate. At core_042's 3%, £549 kept for a year earns £16.47, so BNPL nets £599 − £16.47 = £582.53 > £549: cash still wins, and C3 is false *with the rate stated*. BNPL wins only above 599 ÷ 549 − 1 = **9.1%** | Unchanged: £500 − £15 = £485 < £500 |
| B. Interest never counts (price paid only) | Unchanged: £549 < £599 | The key becomes "They cost exactly the same either way" (£500 = £500), today's C4; the item is rewritten |
| C. Each item states its own measure | Add "she has no savings to earn interest on" (price only) | Add "count the interest she earns" (net cost) |

## 3. No computable measure: add data, or drop

### core_047: window cleaners (key is a judgement)

On the only figures the item gives, Cleaner A costs 13 × £10 = **£130** a year, against Cleaner B's 9 × £15 = **£135**. So C1 ("Cleaner A is
better value because each clean costs less") is true, and the key ("Cleaner B is better value overall") rests on
"keeps windows cleaner for longer", which is not quantified.

| Option | Arithmetic | What changes |
|---|---|---|
| A. Add how long each clean lasts | For example, if windows stay clean 3 weeks of A's 4-week cycle and all 6 weeks of B's: A 13 × 3 = 39 clean weeks, £130 ÷ 39 = **£3.33** a clean week; B 9 × 6 = 54, £135 ÷ 54 = **£2.50**. B wins | A new measure (cost per clean week) and new figures: a new real-world context, which stops for Jon (SR-26) |
| B. Drop the quality factor | Annual cost: A £130 < B £135 | The key becomes C1's verdict, A; the scenario's "values the longer-lasting clean" goes |
| C. Keep it as a judgement item | | The key stays out of the arithmetic (its KNOWN entries stay), or the item is retired from the bank |

### core_048: car insurance (key is a judgement)

Premiums: A £480, B £340. B is third party fire and theft (no cover for her own car, worth £4,500), with a £500
excess against A's £250.

| Option | Arithmetic | What changes |
|---|---|---|
| A. Add a claim chance p and a repair cost R | Expected yearly cost: A ≈ £480 + £250p; B ≈ £340 + pR. A wins when p(R − 250) > 140. So at R = £4,500, from p > **3.3%**; at R = £1,500, from p > **11.2%**. For example, p = 10% and R = £2,000 gives A **£505** against B **£540** | New data (risk figures): a new real-world context, which stops for Jon (SR-26) |
| B. Drop to premium only | B £340 < A £480 | The key becomes B, which teaches "cheapest is best", the opposite of the item's point |
| C. Keep it as a judgement item | | As core_047 C |

## 4. Found while building (not asked; for a ruling)

- **core_030 (crossover): the cost model admits a stepped reading.** The text says "ink cartridges at £18 per 200 pages".
  - **Linear reading** (the item and its explanation, and how it is encoded): £0.09 a page, so the home printer becomes cheaper above 4,000 pages, as keyed.
  - **Stepped reading** (cartridges bought whole): the printer costs £120 + £18 × ⌈pages ÷ 200⌉. It is first strictly cheaper at 4,151 pages, dearer again from 4,201 to 4,300 and from 4,401 to 4,450, and cheaper at every count from 4,451. So "more than 4,000" is false under this reading.
  - This is the amendment's STOP IF (costs that aren't fixed + linear), reported, not chosen.
- **The verifier reads crossover distractors as switch points; the s1-001 ruling read "if" claims as sufficient.**
  - These four read as the switch point, so they are false today. Read as sufficient conditions, they are true:
    - core_024 C2 "After 50 coffees the machine becomes better value" (true from the 35th);
    - core_026 C4 "pay for themselves after approximately 15 years";
    - core_027 C4 "Tariff B becomes better value above 160 minutes";
    - core_029 C4 "after approximately 8.5 years — in year 9".
  - `verify-better-value.py`'s BREAK_EVEN check covers that reading only for gcse_019, core_028 and core_033, and only for "is/are better value or worth it … at least/above N" wording. So it stays.
  - A ruling on "becomes … after N" decides whether these four join KNOWN.
- **gcse_014, gcse_015 and gcse_017 C4 against gcse_018 C4.**
  - The four options all say "X is better because it costs less (overall / in total)". The audit marked gcse_018's TRUE (true for a short stay) and the other three FALSE, though each is true if the buyer needs only the smaller pack.
  - The data reproduces the audit as it stands. All four items are already in KNOWN as quantity-unstated, so the criterion sentence (how much is needed) settles all four together.
