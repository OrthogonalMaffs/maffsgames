# Better Value: declared-measure audit (TRUE-DISTRACTORS follow-up)

Report only; nothing in `games/` or `scripts/` changes. Contract BETTER-VALUE MEASURE AUDIT (Jon, 14 Oct 2026; verbatim in `docs/history/contracts/2026-10-14-better-value-measure-audit.md`). Cloud lane, drafted by Claude; every verdict is mine, from the arithmetic shown, and Jon may overrule any of it.

**Bank:** `games/better-value/index.html` on main at the time of writing (after #392), read through `scripts/extract-banks.py`. **70 items** (20 GCSE, 50 Core), 280 conclusions, every one audited below.

**How to read an item.** "Measure" is what the key actually relies on. "Criterion" is a proposed plain-words sentence for the scenario: it says what the person wants, without naming the calculation, so the student still has to choose the measure. Each conclusion is then TRUE, FALSE or JUDGEMENT *under that measure*, with the arithmetic. JUDGEMENT means the claim cannot be settled from the numbers the item gives. A conclusion marked TRUE that is not the key is a finding.

**One key was wrong: core_039** (corrected by contract BV-CORE-039, 14 Oct 2026). Its "from month 8" treated the no-joining-fee gym as month to month; under the stated 12-month contract (£540 however soon you stop) the rolling gym (at most £495) is cheaper every month. This audit first called it true as written but misleading; Jon ruled it a wrong key. Every other key is true as written. Six items are not value-for-money comparisons (the other STOP IF), reported and audited with the rest: core_019 and gcse_016 (pay rate), core_046 (disposable income), core_021 (a charity's average donation), core_022 (fuel economy) and core_023 (a builder's hourly rate, with no question asked). Each still compares one measure, so the declared-measure design fits them.

## Findings in brief

- **Distractors TRUE under the measure or a plausible one (10 items):** core_007, core_020, core_031, core_037, core_047, gcse_003, gcse_011, gcse_012, gcse_013, gcse_018.
  - True under another measure the option does not name (the core_019 shape): core_020 C4, gcse_003 C1, gcse_011 C1, core_031 C2, core_037 C1, core_047 C1 (true on cost; the key is a judgement).
  - True conditionals or usage the scenario never fixes: core_007 C4, gcse_018 C4.
  - The verdict agrees with the key, but the reason or figure is false: core_031 C1, gcse_012 C1, gcse_013 C1. A student who picks the right verdict for a wrong reason is marked wrong. Whether that is intended is a ruling for Jon.
- **core_021 C2** ("February was better") is false under the scenario's stated criterion but true under total; the option names no measure.
- **Key, explanation and measure disagree (3):** core_037 (key: two facts, no verdict; explanation: net profit; C1 true under ROI), core_039 (break-even ignores the 12-month lock-in the explanation names), core_031 (per month vs total commitment).
- **No single measure fits (4):** core_047 and core_048 (judgement keys; computing them needs data the item lacks), core_050 (direct cost vs cost with time; the key states both), core_044 (judgement key; a usable-value measure fits once declared).
- **The verdict depends on a quantity the scenario never states (6):** core_014 (bottles needed), core_017, gcse_014, gcse_015, gcse_017 (how much is used) and gcse_018 (hours parked). The "X is better because it costs less overall" distractors are defensible until it is stated.
- **Cross-item inconsistency (1 pair):** core_011 keys "keep your money for longer, interest-free" wrong; core_042's key rewards the same reasoning (interest earned while paying later).
- **Scenarios that already state their criterion, the model for the design:** core_021 ("which month had better average giving"), core_038 ("Which has the shorter payback period?"), core_041 ("ignoring what the van is worth"), core_046 ("Compare monthly disposable income"), gcse_019 and gcse_020 ("worth it means cheaper, not the same price"). The break-even questions also ask for their quantity.

## Items

### bv_core_001 · core · direct

**Scenario (verbatim):** Aisha is choosing between two gym memberships for a year.

**Measure the key relies on:** total cost over the 12 months. **Proposed criterion:** Aisha wants to pay as little as possible over the year.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Gym A is better value — total cost £420 vs £396 for Gym B | wrong | FALSE | A 12 × £35 = £420; B £60 + 12 × £28 = £396. A costs £24 more. |
| C2 | Gym B is better value — total cost £396 vs £420 for Gym A | key | TRUE | B £396 < A £420. |
| C3 | They cost the same — both £35 per month | wrong | FALSE | The monthly fees are £35 and £28, and the totals £420 and £396. |
| C4 | Gym A is better value because it has no joining fee | wrong | FALSE | The premise is true (A has no joining fee), but A costs £24 more over 12 months. |

**Flags:** none.

### bv_core_002 · core · direct

**Scenario (verbatim):** A family is choosing a broadband provider for 18 months.

**Measure the key relies on:** total cost over the 18 months. **Proposed criterion:** The family wants to pay the least over the 18 months.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Provider A is better value — total cost £522 vs £481 for Provider B | wrong | FALSE | A 18 × £29 = £522; B £49 + 18 × £24 = £481. A costs £41 more. |
| C2 | Provider B is better value — total cost £481 vs £522 for Provider A | key | TRUE | B £481 < A £522. |
| C3 | Provider A is better because there is no setup fee | wrong | FALSE | The premise is true (no setup fee), but A costs £41 more. |
| C4 | They cost the same over 18 months | wrong | FALSE | £522 vs £481. |

**Flags:** none.

### bv_core_003 · core · direct

**Scenario (verbatim):** Marcus is buying coffee. He drinks one cup per working day (260 days/year).

**Measure the key relies on:** annual cost at 260 cups. **Proposed criterion:** Marcus wants to spend the least on coffee over a year.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The coffee shop is better value — annual cost £832 vs £284 for the subscription machine | wrong | FALSE | Shop 260 × £3.20 = £832; machine £180 + 260 × £0.40 = £284. |
| C2 | The subscription machine is better value — annual cost £284 vs £832 for the coffee shop | key | TRUE | £284 < £832. |
| C3 | The subscription machine is only worth it if he drinks more than 300 cups | wrong | FALSE | Break-even: 3.20n = 180 + 0.40n gives n = 64.3, so the machine is cheaper from the 65th cup, not 300. |
| C4 | They cost about the same over a year — both around £500 for 260 cups | wrong | FALSE | £832 vs £284; neither is near £500. |

**Flags:** none.

### bv_core_004 · core · direct

**Scenario (verbatim):** A student needs car insurance. She gets two quotes for annual cover.

**Measure the key relies on:** cost of a year's cover. **Proposed criterion:** She wants to pay the least for a year's cover.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Insurer A is better value — total cost £820 vs £888 per year for Insurer B | key | TRUE | A £820; B 12 × £74 = £888. |
| C2 | Insurer B is better value — £74 per month is less than £820 for Insurer A | wrong | FALSE | Compares one month with a year; B over the year is £888 > £820. |
| C3 | They cost the same — £820 is roughly 12 × £74 | wrong | FALSE | 12 × £74 = £888, £68 more than £820. |
| C4 | Insurer B is better because you can cancel monthly | wrong | FALSE | The premise is true (monthly payment can stop), but she needs a year of cover, which costs £68 more with B. |

**Flags:** none.

### bv_core_005 · core · direct

**Scenario (verbatim):** A school is buying exercise books in bulk. They need 500 books.

**Measure the key relies on:** cost of 500 books. **Proposed criterion:** The school wants 500 books for the least money.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Supplier A is better value — total cost £225 vs £190 | wrong | FALSE | A 500 × £0.45 = £225; B 5 × £38 = £190. |
| C2 | Supplier B is better value — total cost £190 vs £225 for Supplier A | key | TRUE | £190 < £225. |
| C3 | They cost the same per book | wrong | FALSE | A 45p a book; B £38 ÷ 100 = 38p a book. |
| C4 | Supplier A is cheaper because individual pricing is always the better deal | wrong | FALSE | A costs £35 more for the 500. |

**Flags:** none.

### bv_core_006 · core · direct

**Scenario (verbatim):** A couple wants to visit a theme park. They plan to go twice this year.

**Measure the key relies on:** cost of two visits, per person. **Proposed criterion:** The couple want to pay the least for their two visits.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Two day tickets are better value for two visits — £90 vs £75 for the annual pass | wrong | FALSE | Day tickets 2 × £45 = £90 > pass £75. |
| C2 | The annual pass is better value for two visits — £75 vs £90 for two day tickets | key | TRUE | £75 < £90. |
| C3 | The annual pass is only worth it for three or more visits in the year | wrong | FALSE | The pass is already cheaper at two visits (£75 vs £90); break-even £75 ÷ £45 = 1.67 visits. |
| C4 | They cost the same for two visits | wrong | FALSE | £90 vs £75. |

**Flags:** none.

### bv_core_007 · core · direct

**Scenario (verbatim):** A business is choosing between two photocopier lease options over 3 years. The business makes 2,000 copies per month.

**Measure the key relies on:** cost over 3 years at 2,000 copies a month. **Proposed criterion:** The business wants the lowest cost over the 3 years at its 2,000 copies a month.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Lease A is better value — 3-year cost £4,320 vs £4,500 for Lease B | key | TRUE | A 36 × £120 = £4,320; B 36 × (£85 + 2,000 × £0.02) = 36 × £125 = £4,500. |
| C2 | Lease B is better value — £85/month is much cheaper than £120/month | wrong | FALSE | B's £85 leaves out the copy charge; B is £125 a month. |
| C3 | They cost the same over 3 years | wrong | FALSE | £4,320 vs £4,500. |
| C4 | Lease B is better if the business makes fewer than 1,000 copies | wrong | **TRUE** | As a conditional this is true: B costs £85 + £0.02c, under £120 when c < 1,750. At 999 copies B is at most £104.98 a month. |

**Flags:** **True distractor (C4)**, true as a conditional even with the criterion. A false version: "Lease B is better if the business makes fewer than 2,500 copies" fails at the business's own 2,000 (break-even is 1,750).

### bv_core_008 · core · direct

**Scenario (verbatim):** A family is choosing an energy tariff. Their average monthly usage is 350 kWh.

**Measure the key relies on:** monthly bill at 350 kWh. **Proposed criterion:** The family wants the lowest monthly bill at 350 kWh.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Tariff A is cheaper — no standing charge makes it better value | wrong | FALSE | A 350 × £0.28 = £98; B 350 × £0.24 + £12 = £96. |
| C2 | Tariff B is better value — monthly cost £96 vs £98 for Tariff A | key | TRUE | £96 < £98. |
| C3 | They cost the same each month | wrong | FALSE | £98 vs £96. |
| C4 | Tariff A is better value — monthly cost £98 vs £108 for Tariff B | wrong | FALSE | B is £96, not £108. |

**Flags:** none.

### bv_core_009 · core · hidden

**Scenario (verbatim):** Tom wants to borrow £2,000 for 2 years, repaid monthly. He compares two loan options.

**Measure the key relies on:** total repaid. **Proposed criterion:** Tom wants to pay back the least in total.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The credit union is cheaper — total repayment £2,280 vs approximately £2,332 for the bank loan | wrong | FALSE | Credit union 24 × £95 = £2,280; bank 24 × £90.20 = £2,164.80. £2,332 is £2,000 × 1.08² (no repayments). |
| C2 | The bank loan is cheaper — total repayment £2,164.80 vs £2,280 for the credit union | key | TRUE | £2,164.80 < £2,280. |
| C3 | They cost the same — both around £2,300 | wrong | FALSE | £2,164.80 vs £2,280. |
| C4 | The credit union is cheaper because it charges no interest | wrong | FALSE | The credit union repays £2,280 on £2,000: £280 in charges. |

**Flags:** none.

### bv_core_010 · core · hidden

**Scenario (verbatim):** A phone contract advertises “£25/month — the cheapest on the market!” The contract runs for 24 months and has a £30 upfront cost. A SIM-only deal costs £12/month with a handset purchased outright for £280.

**Measure the key relies on:** total over 24 months, phone included. **Proposed criterion:** The buyer wants a phone and 24 months of service for the least money.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The contract is better value — £25 a month vs £12 a month plus £280 for the phone | wrong | FALSE | Contract £30 + 24 × £25 = £630; SIM-only £280 + 24 × £12 = £568. |
| C2 | The SIM-only deal is better value — total cost £568 vs £630 for the contract | key | TRUE | £568 < £630. |
| C3 | They cost the same over 24 months | wrong | FALSE | £630 vs £568. |
| C4 | The contract is better because you get the phone included | wrong | FALSE | Both include a phone (SIM-only buys it outright); the contract costs £62 more. |

**Flags:** none.

### bv_core_011 · core · hidden

**Scenario (verbatim):** A “sale” sofa is advertised at £599. Buy now pay later: nothing to pay for 12 months, then the full £599 is due if it has not been paid by then. A rival store sells the same sofa for £549 cash.

**Measure the key relies on:** total price paid. **Proposed criterion:** The buyer wants the sofa for the least money.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The BNPL store is free for 12 months so it is better value | wrong | FALSE | BNPL £599 > rival £549. |
| C2 | The rival store is better value if you can pay cash — £549 vs £599 | key | TRUE | £549 < £599. |
| C3 | The BNPL store is better because you keep your money for longer, interest-free | wrong | FALSE | False on total price (£599 vs £549). If interest earned counted, as in core_042, keeping £549 for 12 months would have to earn over £50 (9.1%) to win; no rate is given. At core_042's 3% it earns about £16.47. |
| C4 | They cost the same — both are around £600 | wrong | FALSE | £599 vs £549: £50 apart. |

**Flags:** **Cross-item inconsistency:** C3 ("keep your money for longer, interest-free") is keyed wrong here, but core_042's key rewards the same reasoning. The declared measure must say whether interest earned counts; with no rate stated, it cannot.

### bv_core_012 · core · hidden

**Scenario (verbatim):** An energy company offers a “smart meter discount” of £50 off annual bills. However, the tariff rate is 31p/kWh vs 27p/kWh on the standard tariff. A household uses 3,200 kWh per year.

**Measure the key relies on:** annual bill at 3,200 kWh. **Proposed criterion:** The household wants the lowest annual bill at 3,200 kWh.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The smart meter tariff is cheaper over the year, thanks to its £50 discount on annual bills | wrong | FALSE | Smart 3,200 × £0.31 − £50 = £942; standard 3,200 × £0.27 = £864. |
| C2 | The standard tariff is better value — annual cost £864 vs £942 for the smart meter tariff | key | TRUE | £864 < £942. |
| C3 | They cost about the same once the discount is applied | wrong | FALSE | £78 apart. |
| C4 | The smart meter tariff is better for high-usage households | wrong | FALSE | Smart is cheaper only when 0.31u − 50 < 0.27u, so u < 1,250 kWh: it suits low use, not high. |

**Flags:** none.

### bv_core_013 · core · hidden

**Scenario (verbatim):** A gym offers a “free month” promotion. Standard price: £40/month for 12 months. Free month deal: pay for 11 months upfront at £42/month, get the 12th free.

**Measure the key relies on:** total for 12 months. **Proposed criterion:** The member wants 12 months for the least money.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The standard monthly price is better value — total £480 vs £462 for the upfront deal | wrong | FALSE | Standard 12 × £40 = £480 > deal 11 × £42 = £462. |
| C2 | The free month deal is better value — total £462 vs £480 for standard | key | TRUE | £462 < £480. |
| C3 | They cost the same over 12 months | wrong | FALSE | £480 vs £462. |
| C4 | The free month deal is a scam — it costs more overall | wrong | FALSE | The deal costs £18 less. |

**Flags:** none.

### bv_core_014 · core · hidden

**Scenario (verbatim):** Two supermarkets sell the same brand of orange juice. Supermarket A: 2 for £2.50. Supermarket B: buy 3 get 1 free at £1.40 each.

**Measure the key relies on:** cost of the bottles needed (2, per the key). **Proposed criterion:** She needs exactly 2 bottles and wants to pay the least for them.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Supermarket A is better value per bottle if you only need 2 — £1.25 each vs £1.40 each | key | TRUE | A 2 for £2.50 (£1.25 each); B 2 × £1.40 = £2.80 (the free bottle needs 4). |
| C2 | Supermarket B is always better value per bottle, because you get a free bottle | wrong | FALSE | At 2 bottles B is £1.40 each; "always" fails. At 4, B is £4.20 ÷ 4 = £1.05 each. |
| C3 | They cost the same per bottle | wrong | FALSE | £1.25 vs £1.40 at 2 bottles. |
| C4 | Supermarket B is cheaper if you buy exactly 2 bottles, because of the free one | wrong | FALSE | The free bottle comes with the 4th; at 2, B is £2.80 > £2.50. |

**Flags:** **No quantity in the scenario.** The key's verdict holds only "if you only need 2"; the explanation shows B wins at 4. The criterion must state how many bottles.

### bv_core_015 · core · hidden

**Scenario (verbatim):** A student is choosing between two textbooks. Option A: new book £48. Option B: second-hand book £28, but it needs a £6 revision guide that the new book includes.

**Measure the key relies on:** cost of the book and the revision guide. **Proposed criterion:** The student wants the book and its revision guide for the least money.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The new book is better value because it includes everything you need in one | wrong | FALSE | New £48; second-hand £28 + £6 = £34. |
| C2 | The second-hand book is better value — total cost £34 vs £48 for the new book | key | TRUE | £34 < £48. |
| C3 | They cost the same when you add the revision guide | wrong | FALSE | £48 vs £34. |
| C4 | The second-hand book is worse because it might be outdated | wrong | JUDGEMENT | "Might be outdated" is an uncosted risk. Under the measure the second-hand book is £14 cheaper, so "worse" is false on cost. |

**Flags:** none.

### bv_core_016 · core · hidden

**Scenario (verbatim):** A landlord gets two quotes to repaint a flat. Decorator A: £800 all-inclusive. Decorator B: £600 labour, materials at cost. Materials end up costing £280.

**Measure the key relies on:** cost of the finished job. **Proposed criterion:** The landlord wants the flat repainted for the least money.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Decorator B was better value — £600 for labour vs £800 all-inclusive from Decorator A | wrong | FALSE | B £600 + £280 = £880 > A £800; the £600 leaves out materials. |
| C2 | Decorator A was better value — £800 vs £880 for Decorator B including materials | key | TRUE | £800 < £880. |
| C3 | They cost the same once materials are added | wrong | FALSE | £800 vs £880. |
| C4 | Decorator B is always better value, because its labour charge is £200 cheaper | wrong | FALSE | B costs £80 more in total. |

**Flags:** none.

### bv_core_017 · core · rate

**Scenario (verbatim):** A supermarket sells washing powder in two sizes. Small: 1.2 kg for £3.60. Large: 2.5 kg for £6.75.

**Measure the key relies on:** price per kg (all of it used). **Proposed criterion:** The shopper will use all of either box and wants the lowest price per kilogram.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The small box is better value — £3.00/kg vs £2.70/kg for the large box | wrong | FALSE | Small £3.60 ÷ 1.2 = £3.00/kg; large £6.75 ÷ 2.5 = £2.70/kg. |
| C2 | The large box is better value — £2.70/kg vs £3.00/kg for the small box | key | TRUE | £2.70 < £3.00 per kg. |
| C3 | They cost the same per kg | wrong | FALSE | £3.00 vs £2.70 per kg. |
| C4 | The small box is better because you waste less | wrong | JUDGEMENT | "You waste less" is true only if 2.5 kg would not be used; the criterion settles it (FALSE). |

**Flags:** **Usage not stated:** C4 is defensible until the scenario says the powder will all be used.

### bv_core_018 · core · rate

**Scenario (verbatim):** Petrol costs £1.52 per litre at Garage A. Garage B sells petrol at £6.84 per gallon. (1 gallon = 4.55 litres)

**Measure the key relies on:** price per litre. **Proposed criterion:** The driver wants the cheapest fuel per litre.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Garage A is cheaper — £1.52/litre vs £6.84 a gallon at Garage B | wrong | FALSE | B £6.84 ÷ 4.55 = £1.503/litre < A £1.52; the option compares a litre with a gallon. |
| C2 | Garage B is cheaper — £1.50/litre vs £1.52/litre at Garage A | key | TRUE | £1.50 < £1.52 per litre. |
| C3 | They cost the same per litre | wrong | FALSE | £1.52 vs £1.503. |
| C4 | Garage A is cheaper because litres are the standard unit | wrong | FALSE | The unit decides nothing; B is cheaper per litre. |

**Flags:** none.

### bv_core_019 · core · rate

**Scenario (verbatim):** A freelancer is offered two contracts. Contract A: £320 per day, 3 days per week. Contract B: £18,000 for a 12-week full-time project (5 days/week).

**Measure the key relies on:** pay per day worked. **Proposed criterion:** The freelancer wants the best pay for each day worked.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Contract B has the better day rate — £18,000 ÷ 12 = £1,500/day | wrong | FALSE | £18,000 ÷ 12 = £1,500 is per week; per day £18,000 ÷ 60 = £300. |
| C2 | Contract A has the better day rate — £320/day vs £300/day for Contract B | key | TRUE | A £320 vs B £18,000 ÷ (12 × 5) = £300 a day. |
| C3 | They pay the same daily rate | wrong | FALSE | £320 vs £300. |
| C4 | Contract B has the better day rate — £18,000 ÷ 36 = £500/day | wrong | FALSE | 36 days is A's (3 × 12); B is 60 days, so £300 a day. |

**Flags:** Not a purchase: a pay comparison (reported under STOP IF; the design fits it). Fixed in #392.

### bv_core_020 · core · rate

**Scenario (verbatim):** Two juice cartons: Brand A is 750ml for £1.89. Brand B is 1.25 litres for £2.99.

**Measure the key relies on:** price per litre (all of it used). **Proposed criterion:** The shopper will finish either carton and wants the lowest price per litre.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Brand A is better value — £2.52/litre vs £2.39/litre for Brand B | wrong | FALSE | A £1.89 ÷ 0.75 = £2.52/litre; B £2.99 ÷ 1.25 = £2.392/litre. |
| C2 | Brand B is better value — £2.39/litre vs £2.52/litre for Brand A | key | TRUE | £2.39 < £2.52 per litre. |
| C3 | They cost the same per litre | wrong | FALSE | £2.52 vs £2.39. |
| C4 | Brand A is cheaper because the carton costs less | wrong | **TRUE** | True per carton: £1.89 < £2.99. "Cheaper" names no measure. False per litre. |

**Flags:** **True distractor (C4)** under carton price: "cheaper" with no measure. The core_019 shape.

### bv_core_021 · core · rate

**Scenario (verbatim):** A charity collects donations. In January they received £4,200 from 350 donors. In February they received £5,100 from 510 donors. A trustee wants to know which month had better average giving.

**Measure the key relies on:** average donation per donor (stated in the scenario). **Proposed criterion:** (already stated: "which month had better average giving")

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | January had better average giving — £12 per donor vs £10 per donor in February | key | TRUE | Jan £4,200 ÷ 350 = £12; Feb £5,100 ÷ 510 = £10. |
| C2 | February was better — £5,100 is more than £4,200 | wrong | FALSE | False under the stated criterion. True under total (£5,100 > £4,200): "February was better" names no measure. |
| C3 | February had better average giving, because more donors means more given per person | wrong | FALSE | More donors gave less each: £10 vs £12. |
| C4 | They had the same average donation | wrong | FALSE | £12 vs £10. |

**Flags:** Not a purchase: a charity statistic (reported under STOP IF). C2 is true under total. The scenario's criterion decides it, but the option names no measure; reword it to "February had better giving".

### bv_core_022 · core · rate

**Scenario (verbatim):** A driver records fuel economy. Car A: travels 420 miles on 50 litres. Car B: travels 350 miles on 40 litres.

**Measure the key relies on:** miles per litre. **Proposed criterion:** The driver wants the car that goes furthest on each litre.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Car A is more fuel efficient — 420 miles is further than 350 miles | wrong | FALSE | A 420 ÷ 50 = 8.4; B 350 ÷ 40 = 8.75 miles per litre. |
| C2 | Car B is more fuel efficient — 8.75 miles per litre vs 8.4 miles per litre for Car A | key | TRUE | 8.75 > 8.4. |
| C3 | They have the same fuel efficiency | wrong | FALSE | 8.4 vs 8.75. |
| C4 | Car A is more fuel efficient — 8.4 miles per litre vs 8.75 miles per litre for Car B | wrong | FALSE | The figures are swapped: A is 8.4, B 8.75. |

**Flags:** Not a purchase: fuel economy (reported under STOP IF).

### bv_core_023 · core · rate

**Scenario (verbatim):** Two builders quote for a job. Builder A: £240 for 8 hours work. Builder B: £175 for 6 hours work.

**Measure the key relies on:** charge per hour. **Proposed criterion:** (none asked) Proposed: "Which builder charges more for each hour of work?"

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Builder A is cheaper per hour — £30/hour vs £29.17/hour | wrong | FALSE | A £240 ÷ 8 = £30/hour > B £175 ÷ 6 = £29.17/hour, so A is dearer per hour. |
| C2 | Builder B charges more per hour — £29.17/hour vs £30/hour for Builder A | wrong | FALSE | B £29.17 < A £30. |
| C3 | Builder A charges more per hour — £30/hour vs £29.17/hour for Builder B | key | TRUE | £30 > £29.17. |
| C4 | They charge the same hourly rate | wrong | FALSE | £30 vs £29.17. |

**Flags:** **The scenario asks nothing,** and the key is a rate fact, not a "better" verdict. Both builders quote "for a job", so a customer's natural measure is the job's price: B (£175) is £65 cheaper. A "who is better value" criterion would key B, not A. Reported under STOP IF (not a value verdict).

### bv_core_024 · core · breakeven

**Scenario (verbatim):** Option A: Buy a coffee machine for £85, pods cost £0.30 each. Option B: Buy coffee from a café for £2.80 each. After how many coffees does the machine become better value?

**Measure the key relies on:** number of coffees at which costs are equal. **Proposed criterion:** (already asked)

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | After 34 coffees the machine becomes better value — break-even at 34 cups | key | TRUE | 85 + 0.30n = 2.80n gives n = 34 (both £95.20); the machine is cheaper from the 35th. |
| C2 | After 50 coffees the machine becomes better value — break-even at 50 cups | wrong | FALSE | At 50 the machine (£100) is already cheaper than the café (£140). |
| C3 | The café is always cheaper | wrong | FALSE | At 100 cups: machine £115, café £280. |
| C4 | After 25 coffees the machine becomes better value — break-even at 25 cups | wrong | FALSE | At 25: machine £92.50 > café £70. |

**Flags:** none.

### bv_core_025 · core · breakeven

**Scenario (verbatim):** A National Rail card costs £30/year and gives 1/3 off all fares. Maya’s standard commute costs £9.60 per return journey. How many return journeys must she make for the railcard to be worth buying?

**Measure the key relies on:** journeys for the card to save money. **Proposed criterion:** (already asked; add "worth it means cheaper", as gcse_019 does)

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Maya needs to make at least 10 return journeys for the railcard to be worth it | key | TRUE | 30 + 6.40n < 9.60n gives n > 9.375. At 10: £94 vs £96; at 9: £87.60 vs £86.40. |
| C2 | Maya needs to make at least 5 return journeys for the railcard to be worth it | wrong | FALSE | At 5: £62 with the card vs £48 without. |
| C3 | Maya needs to make at least 15 return journeys for the railcard to be worth it | wrong | FALSE | It is worth it from 10, so 15 is not the minimum. |
| C4 | The railcard is always worth buying | wrong | FALSE | One journey: £36.40 vs £9.60. |

**Flags:** none.

### bv_core_026 · core · breakeven

**Scenario (verbatim):** Solar panels cost £4,500 to install and save £380 per year on energy bills. A homeowner wants to know how long before the panels pay for themselves.

**Measure the key relies on:** years until savings equal the cost. **Proposed criterion:** (already asked)

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The panels pay for themselves after approximately 11.8 years — around year 12 | key | TRUE | £4,500 ÷ £380 = 11.84 years. |
| C2 | The panels pay for themselves after approximately 8 years — around year 8 | wrong | FALSE | 8 years saves £3,040 < £4,500. |
| C3 | The panels never pay for themselves | wrong | FALSE | £380 a year passes £4,500 in year 12. |
| C4 | The panels pay for themselves after approximately 15 years — around year 15 | wrong | FALSE | It pays back at 11.84 years, before 15. |

**Flags:** none.

### bv_core_027 · core · breakeven

**Scenario (verbatim):** Tariff A charges 15p/min for calls with no monthly fee. Tariff B charges £8/month but only 5p/min. At what call duration per month does Tariff B become better value?

**Measure the key relies on:** minutes at which the bills are equal. **Proposed criterion:** (already asked)

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Tariff B becomes better value above 80 minutes of calls per month | key | TRUE | 0.15m = 8 + 0.05m gives m = 80. |
| C2 | Tariff B becomes better value above 50 minutes of calls per month | wrong | FALSE | At 50 min: A £7.50 < B £10.50. |
| C3 | Tariff A is always cheaper | wrong | FALSE | At 100 min: A £15 > B £13. |
| C4 | Tariff B becomes better value above 160 minutes of calls per month | wrong | FALSE | At 120 min B (£14) is already cheaper than A (£18). |

**Flags:** none.

### bv_core_028 · core · breakeven

**Scenario (verbatim):** A streaming service costs £9.99/month. Cinema tickets cost £12.50 each. At what point per month does the streaming service represent better value than cinema visits?

**Measure the key relies on:** films a month at which streaming is cheaper. **Proposed criterion:** (already asked)

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The streaming service is better value if you watch at least 1 film per month | key | TRUE | £9.99 ÷ £12.50 = 0.80 films; at 1 film £9.99 < £12.50. |
| C2 | The streaming service is only better value if you watch at least 3 films per month | wrong | FALSE | Streaming is cheaper from 1 film. |
| C3 | Cinema is always better value | wrong | FALSE | At 1 film cinema costs £12.50 > £9.99. |
| C4 | They cost the same for 2 films per month | wrong | FALSE | 2 films: £9.99 vs £25. |

**Flags:** none.

### bv_core_029 · core · breakeven

**Scenario (verbatim):** An electric car costs £5,000 more than a petrol equivalent. The electric car saves £1,200/year on fuel. How many years before the electric car becomes better value overall?

**Measure the key relies on:** years until fuel savings equal the premium. **Proposed criterion:** (already asked)

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The electric car becomes better value after approximately 4.2 years — in year 5 | key | TRUE | £5,000 ÷ £1,200 = 4.17 years, so in year 5. |
| C2 | The electric car becomes better value after approximately 2 years — in year 2 | wrong | FALSE | 2 years saves £2,400 < £5,000. |
| C3 | The electric car never pays for itself | wrong | FALSE | It pays back at 4.17 years. |
| C4 | The electric car becomes better value after approximately 8.5 years — in year 9 | wrong | FALSE | 8.5 years saves £10,200, double the premium. |

**Flags:** none.

### bv_core_030 · core · breakeven

**Scenario (verbatim):** A printer costs £120 and uses ink cartridges at £18 per 200 pages. A print shop charges £0.12 per page. How many pages must you print for the home printer to become better value?

**Measure the key relies on:** pages at which the costs are equal. **Proposed criterion:** (already asked)

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The home printer becomes better value after printing more than 4,000 pages | key | TRUE | £18 ÷ 200 = £0.09 a page; £120 ÷ (£0.12 − £0.09) = 4,000. |
| C2 | The home printer becomes better value after printing more than 1,500 pages | wrong | FALSE | At 1,500: printer £255 > shop £180. |
| C3 | The print shop is always cheaper | wrong | FALSE | At 10,000: printer £1,020 < shop £1,200. |
| C4 | The home printer becomes better value after printing more than 2,000 pages | wrong | FALSE | At 2,000: printer £300 > shop £240. |

**Flags:** none.

### bv_core_031 · core · hidden

**Scenario (verbatim):** A broadband provider advertises “£18/month broadband — cheapest in the UK!” The small print shows a £10/month line rental, a £60 installation fee, and an 18-month minimum contract. A rival offers £32/month all-inclusive with no installation fee on a 12-month contract.

**Measure the key relies on:** average monthly cost (key) vs total commitment (C2). **Proposed criterion:** The customer wants the lowest average monthly cost.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The advertised deal is cheaper — £18/month beats £32/month | wrong | **TRUE** | The verdict is TRUE per month (advertised £31.33 < £32), but the reason is false: £18 is the broadband alone, and the true monthly cost is £28 + the £60 installation. |
| C2 | The rival deal is better value over its contract — £384 for 12 months vs £564 for 18 months on the advertised deal | wrong | **TRUE** | The figures are true (rival 12 × £32 = £384; advertised 18 × £28 + £60 = £564). True under total commitment, false per month. |
| C3 | Per month the advertised deal is cheaper, at £31.33 vs £32 — but it locks you in for 6 extra months | key | TRUE | £564 ÷ 18 = £31.33 < £32; 18 − 12 = 6 extra months. |
| C4 | They cost the same per month once you add line rental | wrong | FALSE | With line rental: £28 vs £32, or £31.33 vs £32 with installation. |

**Flags:** **No single measure; two distractors true under other readings.** C1's verdict agrees with the key (reason false). C2 is true under total commitment. The scenario asks nothing. The key and the explanation use per month; the explanation's last line ("the true cost is £31.33/month") supports that.

### bv_core_032 · core · hidden

**Scenario (verbatim):** A furniture store advertises a £1,200 sofa with “0% interest over 3 years!” The small print includes a £145 admin fee and compulsory £5.99/month furniture protection. A competitor sells the same sofa for £1,050 cash.

**Measure the key relies on:** total paid for the sofa. **Proposed criterion:** The buyer wants the sofa for the least money.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The 0% deal is genuinely interest-free, so it must be the better deal overall | wrong | FALSE | Finance £1,200 + £145 + 36 × £5.99 = £1,560.64 > cash £1,050. |
| C2 | The cash purchase is better value — £1,050 vs £1,560.64 for the finance deal | key | TRUE | £1,050 < £1,560.64. |
| C3 | The 0% deal costs £1,345 — only £295 more than cash | wrong | FALSE | £1,345 leaves out 36 × £5.99 = £215.64; the true gap is £510.64. |
| C4 | They cost the same because 0% means no extra charges | wrong | FALSE | £1,560.64 vs £1,050. |

**Flags:** none.

### bv_core_033 · core · breakeven

**Scenario (verbatim):** A household is considering switching energy tariff. Their current tariff charges 28p/kWh with a 25p/day standing charge. A new tariff charges 24p/kWh with a 42p/day standing charge. The household uses an average of 12 kWh per day. At what daily usage does the new tariff become better value?

**Measure the key relies on:** daily use at which the bills are equal. **Proposed criterion:** (already asked)

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The new tariff is better value above 4.25 kWh per day, so at 12 kWh they should switch | key | TRUE | 28d + 25 = 24d + 42 gives d = 4.25. At 12 kWh: 361p vs 330p a day. |
| C2 | The current tariff is always cheaper because of the lower standing charge | wrong | FALSE | The new tariff is cheaper above 4.25 kWh. |
| C3 | The new tariff is only better value once usage is above 10 kWh per day | wrong | FALSE | From 4.25, not 10. |
| C4 | They cost the same at 12 kWh per day, so there is no point in switching | wrong | FALSE | 361p vs 330p at 12 kWh. |

**Flags:** none.

### bv_core_034 · core · hidden

**Scenario (verbatim):** An online retailer offers “free next-day delivery” on a £89.99 laptop bag. The same bag on a rival site costs £74.99 with £4.99 standard delivery (3–5 days) or £9.99 next-day delivery.

**Measure the key relies on:** total for next-day delivery. **Proposed criterion:** The buyer wants the bag delivered next day for the least money.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The rival site is better value even with next-day delivery — £84.98 vs £89.99 | key | TRUE | Rival £74.99 + £9.99 = £84.98 < £89.99. |
| C2 | The free delivery site is better value, because its next-day delivery is free | wrong | FALSE | Free delivery is built into the £89.99; it costs £5.01 more. |
| C3 | They cost the same with next-day delivery | wrong | FALSE | £84.98 vs £89.99. |
| C4 | The rival site is only cheaper with standard delivery | wrong | FALSE | The rival is cheaper with next-day too (£84.98). |

**Flags:** The criterion must name next-day delivery; the key compares next-day prices.

### bv_core_035 · core · direct

**Scenario (verbatim):** A landlord needs boiler insurance. Policy A costs £12/month with a £60 excess per claim and covers parts and labour. Policy B costs £8/month with a £150 excess per claim and covers parts only (labour charged at £80/hour). An average boiler repair takes 2 hours and happens once per year.

**Measure the key relies on:** yearly cost with one 2-hour repair. **Proposed criterion:** The landlord wants the lowest yearly cost, allowing for one 2-hour repair.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Policy B is better with one repair per year — only £8/month vs £12/month for Policy A | wrong | FALSE | A 12 × £12 + £60 = £204; B 12 × £8 + £150 + 2 × £80 = £406. |
| C2 | Policy A is better value with one repair per year — annual cost £204 vs £406 for Policy B | key | TRUE | £204 < £406. |
| C3 | They cost the same over a year with one repair, once the excess is paid | wrong | FALSE | £204 vs £406. |
| C4 | Policy B is better because the monthly cost is lower | wrong | FALSE | The premise is true (£8 < £12 a month), but B costs £202 more in the year. |

**Flags:** none.

### bv_core_036 · core · direct

**Scenario (verbatim):** A student is choosing between two train ticket options for a 40-week university year. She travels home every other weekend (20 return trips). An Anytime Return costs £48. An Advance Return costs £22 but is non-refundable and train-specific (she estimates she will miss 3 trains per year and have to buy replacements).

**Measure the key relies on:** cost of 20 trips with 3 missed trains. **Proposed criterion:** She wants to pay the least for her 20 trips, allowing for 3 missed trains.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Advance tickets are better value — total £584 vs £960 for Anytime, even with 3 missed trains | key | TRUE | Advance 20 × £22 + 3 × £48 = £584 < Anytime 20 × £48 = £960. |
| C2 | Anytime tickets are better value because you never waste money on missed trains or replacements | wrong | FALSE | Anytime costs £376 more; the replacements are already counted. |
| C3 | They cost about the same once missed trains are factored in | wrong | FALSE | £376 apart. |
| C4 | Advance tickets are only cheaper if she never misses a train | wrong | FALSE | Advance stays cheaper until 440 + 48k = 960, k = 10.8 misses. |

**Flags:** none.

### bv_core_037 · core · direct

**Scenario (verbatim):** A small business needs 10,000 flyers printed. Printer A charges £180 for 10,000 on standard 130gsm paper. Printer B charges £260 for 10,000 on premium 250gsm card with a gloss finish. The business owner estimates that premium flyers get a 40% higher response rate. Standard flyers typically generate £800 in sales from 10,000.

**Measure the key relies on:** net profit (explanation) vs ROI (true distractor). **Proposed criterion:** Either "The owner wants the most profit from the flyers" (net profit) or "The owner wants the most return for each pound spent" (ROI).

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Standard flyers are better value overall — they cost £80 less to print | wrong | **TRUE** | FALSE under net profit (standard £800 − £180 = £620 < premium £1,120 − £260 = £860). TRUE under ROI (620 ÷ 180 = 344% > 860 ÷ 260 = 331%). |
| C2 | Premium flyers give more net profit, £860 vs £620, but standard has the higher ROI | key | TRUE | Both facts are true: £860 > £620; 344% > 331%. |
| C3 | Standard flyers have the same ROI as premium, so neither is better value | wrong | FALSE | 344% vs 331%. |
| C4 | Premium flyers are only worth it if the response rate doubles, not rises 40% | wrong | FALSE | False under either measure. Premium already makes more profit at +40%. ROI parity needs sales of 260 × 4.444 = £1,155.6, i.e. +44.4%, not doubling. |

**Flags:** **Key, explanation and measure disagree.** The key states two facts and no verdict. The explanation concludes "the cheaper option is not the better value here", which means net profit. C1 is true under ROI. Declare one measure and key a verdict under it.

### bv_core_038 · core · breakeven

**Scenario (verbatim):** A household can install loft insulation for £450. This reduces heating bills by £68 per year. Alternatively, they can install cavity wall insulation for £1,200 which saves £195 per year. Both last 25+ years. Which has the shorter payback period?

**Measure the key relies on:** payback period (stated). **Proposed criterion:** (already asked: "Which has the shorter payback period?")

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Cavity wall insulation has the shorter payback — 6.15 years vs 6.62 years for loft insulation | key | TRUE | Cavity £1,200 ÷ £195 = 6.15; loft £450 ÷ £68 = 6.62 years. |
| C2 | Loft insulation has the shorter payback, because it costs £750 less to install | wrong | FALSE | A lower cost is not a shorter payback; 6.62 > 6.15. |
| C3 | They have the same payback period | wrong | FALSE | 6.62 vs 6.15. |
| C4 | Loft insulation has the shorter payback — about 4 years vs 6.15 years for cavity wall | wrong | FALSE | Loft is 6.62 years, not about 4. |

**Flags:** none.

### bv_core_039 · core · hidden

**Scenario (verbatim):** A gym advertises “No joining fee this January!” at £45/month on a 12-month contract. Another gym charges a £75 joining fee but only £35/month on a rolling contract (cancel anytime).

**Measure the key relies on:** cost for the months used (key) vs the 12-month total (explanation). **Proposed criterion:** The member will stay the full 12 months and wants to pay the least.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The no-joining-fee gym is better value, because there is no £75 upfront cost to pay | wrong | FALSE | No-fee 12 × £45 = £540 > rolling £75 + 12 × £35 = £495. |
| C2 | The rolling gym is better value from month 8 onwards — and you can cancel anytime | key | TRUE | True as written: rolling is cheaper in months 8 to 12. But the no-fee gym is a 12-month contract (£540, "locked in" in the explanation), so rolling (£75 + £35m, at most £495) is cheaper from month 1, and "from month 8" understates it. |
| C3 | They cost the same over 12 months | wrong | FALSE | £540 vs £495. |
| C4 | The no-joining-fee gym is always cheaper, whichever month you stop going | wrong | FALSE | The no-fee gym costs £540 whenever you stop; rolling at most £495. |

**Flags:** **Key, explanation and measure disagree.** The break-even (£75 ÷ £10 = 7.5 months) treats the no-fee gym as month-to-month, but the scenario and the explanation make it a 12-month contract. Jon ruled this a wrong key (14 Oct); corrected by BV-CORE-039 to "whichever month you stop — at most £495 vs £540".

### bv_core_040 · core · direct

**Scenario (verbatim):** A parent is choosing between two nurseries for childcare, 5 days per week, 50 weeks per year. Nursery A costs £55/day but includes all meals and nappies. Nursery B costs £48/day but meals are £5/day extra and parents must supply nappies (approximately £20/week).

**Measure the key relies on:** annual childcare cost. **Proposed criterion:** The parent wants the lowest cost for the year.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Nursery B is better value because its daily rate is £7 less than Nursery A's | wrong | FALSE | The premise is true (£48 < £55), but A 250 × £55 = £13,750 and B 250 × £48 + 250 × £5 + 50 × £20 = £14,250. |
| C2 | Nursery A is better value — annual cost £13,750 vs £14,250 for Nursery B | key | TRUE | £13,750 < £14,250. |
| C3 | They cost the same over a year | wrong | FALSE | £500 apart. |
| C4 | Nursery B is £1,000 cheaper per year | wrong | FALSE | B is £500 dearer, not £1,000 cheaper. |

**Flags:** none.

### bv_core_041 · core · direct

**Scenario (verbatim):** A tradesperson needs a van. Option A: buy a 3-year-old van for £12,000 cash. Expected repairs: £800/year. Insurance: £1,200/year. Option B: lease a new van for £350/month including maintenance. Insurance: £900/year. Compare over 3 years, ignoring what the van is worth at the end.

**Measure the key relies on:** 3-year cost, the van's end value set aside (stated). **Proposed criterion:** (already stated: "Compare over 3 years, ignoring what the van is worth at the end")

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Buying is cheaper — 3-year cost £18,000 vs £15,300 for leasing | wrong | FALSE | Buy £12,000 + 3 × £800 + 3 × £1,200 = £18,000 > lease 36 × £350 + 3 × £900 = £15,300; its own figures show buying is dearer. |
| C2 | Leasing is better value over 3 years — £15,300 vs £18,000 for buying | key | TRUE | £15,300 < £18,000. |
| C3 | Buying is better value because you own the van at the end of 3 years | wrong | FALSE | False under the stated criterion, which sets the van's end value aside. |
| C4 | They cost the same over 3 years | wrong | FALSE | £2,700 apart. |

**Flags:** none.

### bv_core_042 · core · direct

**Scenario (verbatim):** A student has £500 in savings earning 3% AER. She wants to buy a £500 laptop. Option A: pay cash now. Option B: take a 12-month 0% credit card and keep the £500 in savings for the year.

**Measure the key relies on:** net cost once interest earned is counted. **Proposed criterion:** She wants the laptop to cost her the least once interest earned is counted.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Paying cash is better value — it's simpler and the laptop costs £500 either way | wrong | FALSE | Cash net £500; card £500 − £500 × 3% = £485. |
| C2 | The 0% credit card is better value — she earns £15 interest while the laptop costs the same | key | TRUE | £485 < £500. |
| C3 | The credit card is worse value — hidden charges will cost more than the £15 | wrong | JUDGEMENT | No charges are stated on the 0% card, so false on the data; it assumes she clears the card in month 12. |
| C4 | They cost exactly the same either way | wrong | FALSE | £500 vs £485. |

**Flags:** See core_011: the same reasoning is keyed wrong there.

### bv_core_043 · core · direct

**Scenario (verbatim):** A commuter can drive to work (8 miles each way) or take the bus. Driving: 30 mpg, petrol at £1.55/litre (1 gallon = 4.55 litres), plus £5/day parking. Bus: £4.20 return ticket, or a monthly pass for £75 (22 working days/month).

**Measure the key relies on:** monthly commuting cost. **Proposed criterion:** The commuter wants the lowest monthly cost of getting to work.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Driving is cheaper because you control the costs | wrong | FALSE | Driving 22 × (16 ÷ 30 × 4.55 × £1.55 + £5) = 22 × (£3.76 + £5) = £192.75 > £75. |
| C2 | The bus pass is better value — monthly cost £75 vs approximately £193 for driving | key | TRUE | £75 < about £193. |
| C3 | Driving costs about £75 per month in fuel and parking, the same as the monthly bus pass | wrong | FALSE | Fuel alone 22 × £3.76 = £82.75; with parking £192.75. |
| C4 | The bus is only cheaper if petrol prices rise above £2/litre | wrong | FALSE | Parking alone is 22 × £5 = £110 > £75, so the bus wins at any petrol price. |

**Flags:** none.

### bv_core_044 · core · hidden

**Scenario (verbatim):** A subscription box advertises “£250 of products for just £29.99/month!” The 12-month contract costs £359.88 per year. The subscriber estimates she would actually buy about £80 of the products each box — the rest she doesn’t use.

**Measure the key relies on:** cost of the goods she would actually use. **Proposed criterion:** She wants the things she actually uses for the least money.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The subscription box is amazing value — £250 of products for £29.99 | wrong | JUDGEMENT | The verdict ("amazing value") agrees with the key's reading (£80 of usable goods for £29.99), but the £250 is RRP, not usable value. |
| C2 | Buying what you need is better value — you spend £80 on things you actually use vs paying £29.99 for £80 of usable products plus £170 of waste | wrong | FALSE | Buying costs £80 for the same £80 of goods; the box costs £29.99. The "£170 of waste" costs her nothing extra. |
| C3 | The box gives £80 of usable value for £29.99 a month — good, unless that money has a better use | key | JUDGEMENT | True under usable value (£80 for £29.99). "Unless that money has a better use" cannot be checked: a hedged judgement. |
| C4 | The subscription is worthless because you don’t use most of the products | wrong | FALSE | £80 of usable goods a month is not worthless. |

**Flags:** **Key is a judgement.** With the criterion the key could read: "The box is better value: £80 of things she uses for £29.99 vs £80 buying them".

### bv_core_045 · core · breakeven

**Scenario (verbatim):** A household is comparing two electricity tariffs for a year. Tariff A: variable rate, currently 29p/kWh, no exit fee. Tariff B: fixed rate at 26p/kWh for 12 months with a £75 exit fee if you leave early. The household uses 3,600 kWh per year. If variable rates rise by 4p/kWh after 6 months, which is better value?

**Measure the key relies on:** annual cost with the 4p rise. **Proposed criterion:** The household wants the lowest bill for the year, given the rise.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The fixed tariff saves money — annual cost £936 vs £1,116 for variable | key | TRUE | Fixed 3,600 × £0.26 = £936; variable 1,800 × £0.29 + 1,800 × £0.33 = £1,116. |
| C2 | The variable tariff is cheaper over the year because there is no £75 exit fee | wrong | FALSE | No exit fee is paid in a full year; £1,116 > £936. |
| C3 | They cost the same over the year | wrong | FALSE | £180 apart. |
| C4 | The fixed tariff is only better if rates rise by more than 10p | wrong | FALSE | Fixed wins even with no rise: 3,600 × £0.29 = £1,044 > £936. |

**Flags:** Typed "breakeven" but a direct comparison (label only).

### bv_core_046 · core · direct

**Scenario (verbatim):** Two job offers for a graduate. Job A: £28,000 salary in Manchester (average rent £650/month). Job B: £34,000 salary in London (average rent £1,200/month). Tax and NI are roughly a sixth of gross salary at these salaries. Compare monthly disposable income after rent.

**Measure the key relies on:** monthly income after tax, NI and rent (stated). **Proposed criterion:** (already stated: "Compare monthly disposable income after rent")

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The London job is better because the salary is £6,000 a year higher | wrong | FALSE | The premise is true (£6,000 more), but false under the stated measure. |
| C2 | The Manchester job gives more disposable income — about £1,294/month vs £1,161/month after tax and rent | key | TRUE | Manchester £28,000 × 5/6 ÷ 12 − £650 = £1,294.44; London £34,000 × 5/6 ÷ 12 − £1,200 = £1,161.11. |
| C3 | They give the same disposable income once tax and rent are taken off | wrong | FALSE | £1,294 vs £1,161. |
| C4 | The London job gives more disposable income because the salary is higher | wrong | FALSE | London gives £133 a month less. |

**Flags:** Not a purchase: pay (reported under STOP IF).

### bv_core_047 · core · direct

**Scenario (verbatim):** A homeowner is choosing between two window cleaners. Cleaner A: £10 per clean, visits every 4 weeks (13 times/year). Cleaner B: £15 per clean, visits every 6 weeks and uses a pure-water system that keeps windows cleaner for longer (roughly 9 times/year: use 9). The homeowner values the longer-lasting clean.

**Measure the key relies on:** none: annual cost favours A; the key rests on unquantified quality. **Proposed criterion:** Needs data: how long each clean lasts (then cost per week of clean windows), or a rewrite.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Cleaner A is better value because each clean costs less | wrong | **TRUE** | True on cost: A 13 × £10 = £130 < B 9 × £15 = £135, and £10 < £15 a clean. Only the scenario's unquantified preference makes it wrong. |
| C2 | Cleaner B is better value overall — £135 vs £130 a year, but the windows stay cleaner | key | JUDGEMENT | B costs £5 more a year; "better value overall" rests on "the windows stay cleaner", which is not quantified. |
| C3 | Cleaner A is the better value overall — it saves £50 a year | wrong | FALSE | A saves £5 a year, not £50. |
| C4 | They cost the same per year once the extra visits are counted | wrong | FALSE | £130 vs £135. |

**Flags:** **Key is a judgement that contradicts the only computable measure.** C1 is true on cost. No single measure fits.

### bv_core_048 · core · hidden

**Scenario (verbatim):** A car insurance comparison site shows: Insurer A at £480/year (comprehensive, £250 excess, courtesy car included). Insurer B at £340/year (third party fire and theft, £500 excess, no courtesy car). The car is worth £4,500.

**Measure the key relies on:** none: expected cost needs a claim probability and repair cost. **Proposed criterion:** Needs data: the chance of an own-fault claim and its cost (then expected yearly cost), or a rewrite.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Insurer B is better value — it's £140 cheaper per year for the same car | wrong | JUDGEMENT | The premise is true (£480 − £340 = £140), and "same car" is true, but the cover differs. Cannot be decided without risk data. |
| C2 | Insurer A is better value — £140 more buys full cover, a lower excess and a courtesy car | key | JUDGEMENT | Cannot be computed from the item. |
| C3 | They offer the same level of protection, so the cheaper one wins | wrong | FALSE | TPFT is not comprehensive cover. |
| C4 | Insurer B is better because you save money every month | wrong | JUDGEMENT | The premise is true (cheaper each month); the verdict needs risk data. |

**Flags:** **Key is a judgement.** With a claim chance p and a repair cost R (≤ £4,500): A ≈ £480 + £250p; B ≈ £340 + pR. The item gives neither.

### bv_core_049 · core · breakeven

**Scenario (verbatim):** A small business is choosing between hiring a part-time employee or outsourcing work. Employee: £15/hour for 20 hours/week, plus £180/month employer NI and pension. Outsourcing: £40/hour, estimated 8 hours/week needed. At what weekly outsourcing hours does hiring become cheaper?

**Measure the key relies on:** outsourced hours at which costs are equal. **Proposed criterion:** (already asked)

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Hiring becomes cheaper above approximately 8.5 hours per week of outsourced work | key | TRUE | Employee 20 × £15 + £180 ÷ 4.33 = £341.57 a week; 40h = 341.57 gives h = 8.54. |
| C2 | Outsourcing is always cheaper, because you only pay for the hours of work you need | wrong | FALSE | Above 8.54 hours, hiring is cheaper. |
| C3 | Hiring is always cheaper, because £15 an hour is less than £40 an hour | wrong | FALSE | At the estimated 8 hours, outsourcing (£320) is cheaper than £341.57. |
| C4 | Hiring becomes cheaper above 15 hours per week | wrong | FALSE | 8.54, not 15. |

**Flags:** none.

### bv_core_050 · core · direct

**Scenario (verbatim):** A student can buy lunch at university or meal-prep at home. Buying: average £5.50/meal, 5 days/week. Meal prep: £25/week for ingredients (makes 5 lunches), plus a one-off £40 for containers. Compare the cost over a 30-week academic year, and consider the 45 minutes/week spent meal-prepping (the student could work a part-time job at £11.44/hour instead).

**Measure the key relies on:** direct cost vs cost including time. **Proposed criterion:** Either "She would work those 45 minutes if she did not cook" (time counts) or "She would not use the time to earn" (direct cost only).

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Meal prep is clearly cheaper — £790 vs £825 for buying, because the time spent prepping costs nothing | wrong | FALSE | The scenario values the time; with it, prep costs £1,047.40. |
| C2 | Meal prep saves £35 in direct costs, but the 45 minutes a week could earn more than that | key | TRUE | Direct: £825 − (£40 + 30 × £25) = £35. Time: 30 × 0.75 × £11.44 = £257.40 > £35. |
| C3 | Meal prep saves over £200 per year | wrong | FALSE | It saves £35 directly. |
| C4 | Buying lunch is always better value because time is money | wrong | JUDGEMENT | "Always" fails if she would not work those hours (prep £35 cheaper); true if she would (£825 < £1,047.40). |

**Flags:** **No single measure.** The key states both; the explanation leaves the choice open. A criterion sentence decides C4.

### bv_gcse_001 · gcse · direct

**Scenario (verbatim):** Two pizza deals for a school party. Pizza Palace: £8 per pizza. Slice House: 3 pizzas for £21. The school needs 9 pizzas.

**Measure the key relies on:** cost of 9 pizzas. **Proposed criterion:** The school wants 9 pizzas for the least money.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Pizza Palace is cheaper — £72 vs £63 | wrong | FALSE | Palace 9 × £8 = £72 > Slice House 3 × £21 = £63; its own figures say so. |
| C2 | Slice House is cheaper — £63 vs £72 for Pizza Palace | key | TRUE | £63 < £72. |
| C3 | They cost the same for 9 pizzas | wrong | FALSE | £72 vs £63. |
| C4 | Pizza Palace is cheaper because individual pricing is better | wrong | FALSE | £9 dearer. |

**Flags:** none.

### bv_gcse_002 · gcse · direct

**Scenario (verbatim):** Sam wants a music streaming subscription for a year.

**Measure the key relies on:** cost of a year. **Proposed criterion:** Sam wants a year of music for the least money.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Plan A is cheaper — £5.99 per month sounds less | wrong | FALSE | A 12 × £5.99 = £71.88 > B £59.99. |
| C2 | Plan B is cheaper — £59.99 vs £71.88 for Plan A | key | TRUE | £59.99 < £71.88. |
| C3 | They cost the same over a year | wrong | FALSE | £11.89 apart. |
| C4 | Plan A is better because you can cancel anytime | wrong | FALSE | The premise is true (can cancel); for a year, A costs £11.89 more. |

**Flags:** none.

### bv_gcse_003 · gcse · direct

**Scenario (verbatim):** Two shops sell the same pack of coloured pencils.

**Measure the key relies on:** cost delivered. **Proposed criterion:** She wants the pencils delivered for the least money.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Shop A is cheaper — £4.50 vs £5.80 | wrong | **TRUE** | True by pack price (£4.50 < £5.80); false delivered (£6.50 vs £5.80). "Cheaper" names no measure. |
| C2 | Shop A is cheaper overall — £6.50 vs £5.80 for Shop B | wrong | FALSE | £6.50 > £5.80: its own figures show A dearer. |
| C3 | Shop B is cheaper overall — £5.80 vs £6.50 for Shop A | key | TRUE | £5.80 < £6.50. |
| C4 | They cost the same once delivery is added | wrong | FALSE | £6.50 vs £5.80. |

**Flags:** **True distractor (C1)** under pack price: the core_019 shape.

### bv_gcse_004 · gcse · direct

**Scenario (verbatim):** A family is choosing between two holiday parks for a 5-night stay.

**Measure the key relies on:** cost of 5 nights. **Proposed criterion:** The family wants the 5 nights for the least money.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Park A is cheaper — £400 vs £390 | wrong | FALSE | A 5 × £80 = £400 > B £40 + 5 × £70 = £390. |
| C2 | Park B is cheaper — £390 vs £400 for Park A | key | TRUE | £390 < £400. |
| C3 | They cost the same for 5 nights | wrong | FALSE | £400 vs £390. |
| C4 | Park A is better because there is no booking fee | wrong | FALSE | The premise is true (no fee); A is £10 dearer. |

**Flags:** none.

### bv_gcse_005 · gcse · direct

**Scenario (verbatim):** Ella buys a sandwich every school day (5 days a week). She compares buying from the canteen vs making her own.

**Measure the key relies on:** cost per week. **Proposed criterion:** Ella wants her week of sandwiches for the least money.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The canteen is cheaper — £2.50 per sandwich vs £6 per week for homemade | wrong | FALSE | Mixes a sandwich with a week; canteen 5 × £2.50 = £12.50 a week > £6. |
| C2 | Homemade is cheaper — £6 per week vs £12.50 per week for the canteen | key | TRUE | £6 < £12.50. |
| C3 | They cost the same per week | wrong | FALSE | £12.50 vs £6. |
| C4 | The canteen saves £6.50 per week | wrong | FALSE | Homemade saves £6.50. |

**Flags:** none.

### bv_gcse_006 · gcse · direct

**Scenario (verbatim):** Two taxi companies quote for a trip from school to the train station.

**Measure the key relies on:** fare for the trip. **Proposed criterion:** The school wants the trip for the least money.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Quick Cabs is cheaper — £12 vs £13 for City Taxis | key | TRUE | City £3 + 5 × £2 = £13 > Quick £12. |
| C2 | City Taxis is cheaper — its £3 base fare is lower than £12 | wrong | FALSE | The base fare is not the fare; City is £13. |
| C3 | They cost the same | wrong | FALSE | £12 vs £13. |
| C4 | City Taxis is cheaper at £10 | wrong | FALSE | City is £13, not £10. |

**Flags:** none.

### bv_gcse_007 · gcse · direct

**Scenario (verbatim):** A student needs a calculator for GCSE exams. Two shops have the same model.

**Measure the key relies on:** cost delivered or collected. **Proposed criterion:** The student wants the calculator for the least money.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The online store is cheaper — £22.49 vs £23.00 | key | TRUE | Online £18.50 + £3.99 = £22.49 < £23.00. |
| C2 | The high street shop is cheaper because there is no delivery | wrong | FALSE | The high-street shop is 51p dearer. |
| C3 | They cost the same | wrong | FALSE | £22.49 vs £23.00. |
| C4 | The online store costs £18.50 so it is much cheaper | wrong | FALSE | The direction agrees with the key, but online costs £22.49, not £18.50, and is 51p cheaper, not "much". |

**Flags:** C4's verdict direction agrees with the key; false only by its figure and "much".

### bv_gcse_008 · gcse · direct

**Scenario (verbatim):** Two cinemas show the same film. A group of 4 friends want to go.

**Measure the key relies on:** cost for 4 people. **Proposed criterion:** The four friends want to see the film for the least money.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Cineworld is cheaper — £44 vs £40 for Vue | wrong | FALSE | Cineworld 4 × £11 = £44 > Vue £40. |
| C2 | Vue is cheaper — £40 vs £44 for Cineworld | key | TRUE | £40 < £44. |
| C3 | They cost the same for 4 people | wrong | FALSE | £44 vs £40. |
| C4 | Cineworld is cheaper per person | wrong | FALSE | Per person: £11 vs £10. |

**Flags:** none.

### bv_gcse_009 · gcse · hidden

**Scenario (verbatim):** A new game costs £45 from the shop. An online marketplace has it for £38 but charges £4.99 delivery plus £3 for a protective case that the shop includes free.

**Measure the key relies on:** total cost with the case. **Proposed criterion:** The buyer wants the game and a case for the least money.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The online deal is cheaper overall — £38 vs £45 for the shop | wrong | FALSE | Online £38 + £4.99 + £3 = £45.99 > £45; £38 is not the total. |
| C2 | The shop is cheaper overall — £45 vs £45.99 for online | key | TRUE | £45 < £45.99. |
| C3 | They cost the same | wrong | FALSE | 99p apart. |
| C4 | Online saves £7 | wrong | FALSE | Online costs 99p more. |

**Flags:** none.

### bv_gcse_010 · gcse · hidden

**Scenario (verbatim):** A mobile top-up deal offers 500 minutes for £10. But calls to non-network numbers cost 20p/min extra. Jake makes 100 of his 500 minutes to non-network numbers. A rival offers unlimited calls for £15.

**Measure the key relies on:** cost for Jake's calls. **Proposed criterion:** Jake wants his calls for the least money.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The top-up deal is cheaper — just £10 vs £15 for the unlimited plan | wrong | FALSE | Top-up £10 + 100 × £0.20 = £30 > £15. |
| C2 | The unlimited plan is cheaper — £15 vs £30 for the top-up deal | key | TRUE | £15 < £30. |
| C3 | They cost the same | wrong | FALSE | £30 vs £15. |
| C4 | The top-up deal costs £12 in total | wrong | FALSE | £30, not £12. |

**Flags:** none.

### bv_gcse_011 · gcse · hidden

**Scenario (verbatim):** A “free delivery” website sells a hoodie for £25 but charges a £3.50 “service fee”. A shop sells the same hoodie for £27 with nothing extra to pay.

**Measure the key relies on:** total paid. **Proposed criterion:** The buyer wants the hoodie for the least money.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The website is cheaper — £25 vs £27 for the shop, with free delivery | wrong | **TRUE** | True by price tag (£25 < £27); false in total (£25 + £3.50 = £28.50 > £27). |
| C2 | The shop is cheaper — £27 vs £28.50 for the website | key | TRUE | £27 < £28.50. |
| C3 | They cost the same | wrong | FALSE | £28.50 vs £27. |
| C4 | The website saves £2 | wrong | FALSE | The website is £1.50 dearer. |

**Flags:** **True distractor (C1)** under the price tag: the core_019 shape.

### bv_gcse_012 · gcse · hidden

**Scenario (verbatim):** School trip option A: coach hire £200 shared between 40 students. Option B: parents drive — petrol costs £5 per car, 4 students per car, but parking is £8 per car.

**Measure the key relies on:** cost per student. **Proposed criterion:** The school wants the trip for the least money per student.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Cars are cheaper — £5 per car vs £200 for a coach | wrong | **TRUE** | The verdict is TRUE (cars £3.25 < coach £5 per student), but the reason is false: £5 a car leaves out £8 parking and compares a car with a coach. |
| C2 | The coach is cheaper — £5 per student vs £3.25 per student for the cars | wrong | FALSE | Its own figures show cars cheaper. |
| C3 | Cars are cheaper — £3.25 per student vs £5 per student for the coach | key | TRUE | 40 ÷ 4 = 10 cars × (£5 + £8) = £130 ÷ 40 = £3.25; coach £200 ÷ 40 = £5. |
| C4 | They cost the same per student | wrong | FALSE | £5 vs £3.25. |

**Flags:** **C1's verdict is true** (reason false): a student choosing "Cars are cheaper" is marked wrong for the right answer.

### bv_gcse_013 · gcse · hidden

**Scenario (verbatim):** A “headphones deal” offers £20 headphones with a “free” 2-year warranty that costs £4.99. The same headphones cost £26 elsewhere with a free 2-year warranty included.

**Measure the key relies on:** total with a 2-year warranty. **Proposed criterion:** The buyer wants the headphones and a 2-year warranty for the least money.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The deal store is cheaper at £20 | wrong | **TRUE** | The verdict is TRUE (deal store £24.99 < £26), but the figure is false: it costs £24.99, not £20. |
| C2 | The deal store is cheaper overall — £24.99 vs £26 | key | TRUE | £20 + £4.99 = £24.99 < £26. |
| C3 | The other store is cheaper, as its £26 includes the warranty | wrong | FALSE | £26 > £24.99. |
| C4 | They cost the same | wrong | FALSE | £24.99 vs £26. |

**Flags:** **C1's verdict is true** (figure false), as in gcse_012.

### bv_gcse_014 · gcse · rate

**Scenario (verbatim):** Two bags of rice at the supermarket. Bag A: 2 kg for £3.00. Bag B: 5 kg for £6.50.

**Measure the key relies on:** price per kg (all of it used). **Proposed criterion:** The family will use 5 kg of rice and wants the lowest price per kilogram.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Bag A is better value — £1.50/kg vs £1.30/kg for Bag B | wrong | FALSE | A £3.00 ÷ 2 = £1.50/kg > B £6.50 ÷ 5 = £1.30/kg. |
| C2 | Bag B is better value — £1.30/kg vs £1.50/kg for Bag A | key | TRUE | £1.30 < £1.50. |
| C3 | They cost the same per kg | wrong | FALSE | £1.50 vs £1.30. |
| C4 | Bag A is better because it costs less overall | wrong | FALSE | The premise is true (£3 < £6.50); false per kg, but true if only 2 kg is needed. |

**Flags:** **Usage not stated:** C4 is defensible until the criterion says how much is used.

### bv_gcse_015 · gcse · rate

**Scenario (verbatim):** Two packs of felt-tip pens. Pack A: 12 pens for £3.60. Pack B: 20 pens for £5.00.

**Measure the key relies on:** price per pen (all used). **Proposed criterion:** The class will use 20 pens and wants the lowest price per pen.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Pack A is better value — 30p per pen vs 25p per pen for Pack B | wrong | FALSE | A £3.60 ÷ 12 = 30p > B £5.00 ÷ 20 = 25p. |
| C2 | Pack B is better value — 25p per pen vs 30p per pen for Pack A | key | TRUE | 25p < 30p. |
| C3 | They cost the same per pen | wrong | FALSE | 30p vs 25p. |
| C4 | Pack A is better because it costs less | wrong | FALSE | The premise is true (£3.60 < £5); false per pen, but true if 12 pens are enough. |

**Flags:** **Usage not stated** (as gcse_014).

### bv_gcse_016 · gcse · rate

**Scenario (verbatim):** Two part-time jobs for a student. Job A pays £54 for a 6-hour shift. Job B pays £80 for a 9-hour shift.

**Measure the key relies on:** pay per hour. **Proposed criterion:** The student wants the best pay for each hour worked.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Job A pays better per hour — £9/hour vs £8.89/hour for Job B | key | TRUE | A £54 ÷ 6 = £9.00 > B £80 ÷ 9 = £8.89. |
| C2 | Job B pays better per hour, because £80 is more than £54 for Job A | wrong | FALSE | It names the measure (per hour), and £80 a shift is £8.89 an hour. |
| C3 | They pay the same hourly rate | wrong | FALSE | £9.00 vs £8.89. |
| C4 | Job B pays £10/hour | wrong | FALSE | £8.89, not £10. |

**Flags:** Not a purchase: pay (reported under STOP IF).

### bv_gcse_017 · gcse · rate

**Scenario (verbatim):** Two bottles of shampoo. Bottle A: 300 ml for £2.40. Bottle B: 500 ml for £3.50.

**Measure the key relies on:** price per ml (all used). **Proposed criterion:** The shopper will use 500 ml and wants the lowest price per ml.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Bottle A is cheaper per ml — 0.8p/ml vs 0.7p/ml for Bottle B | wrong | FALSE | A £2.40 ÷ 300 = 0.8p > B £3.50 ÷ 500 = 0.7p per ml. |
| C2 | Bottle B is better value — 0.7p/ml vs 0.8p/ml for Bottle A | key | TRUE | 0.7p < 0.8p. |
| C3 | They cost the same per ml | wrong | FALSE | 0.8p vs 0.7p. |
| C4 | Bottle A is better because it costs less in total | wrong | FALSE | The premise is true (£2.40 < £3.50); false per ml, true if 300 ml is enough. |

**Flags:** **Usage not stated** (as gcse_014).

### bv_gcse_018 · gcse · rate

**Scenario (verbatim):** Two car parks near school. Car Park A charges £6 for 4 hours. Car Park B charges £8 for 6 hours.

**Measure the key relies on:** price per hour (a 6-hour stay assumed). **Proposed criterion:** The parent needs to park for 6 hours and wants the lowest price per hour.

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | Car Park A is cheaper per hour — £1.50/hour vs £1.33/hour for Car Park B | wrong | FALSE | A £6 ÷ 4 = £1.50 > B £8 ÷ 6 = £1.33 an hour. |
| C2 | Car Park B is cheaper per hour — £1.33/hour vs £1.50/hour for Car Park A | key | TRUE | £1.33 < £1.50. |
| C3 | They cost the same per hour | wrong | FALSE | £1.50 vs £1.33. |
| C4 | Car Park A is better because it costs less overall | wrong | **TRUE** | True for a stay of 4 hours or less (A £6 vs B £8): the scenario gives no stay length. |

**Flags:** **True distractor (C4) for any stay of 4 hours or less.** The per-hour price matters only if the driver needs 6 hours; the criterion must say how long.

### bv_gcse_019 · gcse · breakeven

**Scenario (verbatim):** A school lunch pass costs £30 per month for unlimited lunches. Individual lunches cost £2.50 each. How many lunches per month make the pass worth it? (Worth it means cheaper, not the same price.)

**Measure the key relies on:** lunches at which the pass is cheaper (stated). **Proposed criterion:** (already stated: "Worth it means cheaper, not the same price")

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The pass is worth it if you eat more than 12 lunches per month — from the 13th lunch onwards | key | TRUE | £30 ÷ £2.50 = 12; at 13, £30 < £32.50. |
| C2 | The pass is worth it if you eat 8 or more lunches per month, about two a week | wrong | FALSE | At 8: £20 < £30. |
| C3 | Individual lunches are always cheaper, however many you eat in a month | wrong | FALSE | At 13: £32.50 > £30. |
| C4 | The pass is only worth it if you eat 15 or more lunches per month, three a week | wrong | FALSE | From 13, not 15. |

**Flags:** none.

### bv_gcse_020 · gcse · breakeven

**Scenario (verbatim):** A reusable water bottle costs £15. Buying bottled water costs £1 per bottle. How many bottles of water must you drink for the reusable bottle to save money? (Saving money means cheaper, not the same price.)

**Measure the key relies on:** bottles at which the reusable bottle is cheaper (stated). **Proposed criterion:** (already stated: "Saving money means cheaper, not the same price")

| # | Conclusion (verbatim) | Keyed | Under the measure | Arithmetic |
|---|---|---|---|---|
| C1 | The reusable bottle saves money from the 15th bottle of water onwards | wrong | FALSE | At 15 both cost £15, so it is not yet a saving. |
| C2 | The reusable bottle saves money after more than 15 bottles — from bottle 16 onwards | key | TRUE | From 16: £15 < £16. |
| C3 | Bottled water is always cheaper, however many bottles you drink | wrong | FALSE | At 20: £15 < £20. |
| C4 | The reusable bottle saves money from the 10th bottle of water onwards | wrong | FALSE | At 10: £15 > £10. |

**Flags:** none.

## Summary

**Items audited: 70 of 70** (bank total 70).

**Items per measure**

| Measure | Items | Ids |
|---|---|---|
| Total cost for a stated quantity or period | 36 | core_001, core_002, core_003, core_004, core_005, core_006, core_007, core_008, core_009, core_010, core_011, core_012, core_013, core_014, core_015, core_016, core_032, core_034, core_035, core_036, core_040, core_041, core_043, core_045, gcse_001, gcse_002, gcse_003, gcse_004, gcse_005, gcse_006, gcse_007, gcse_008, gcse_009, gcse_010, gcse_011, gcse_013 |
| Unit cost (per kg, litre, ml, pen, hour, student) | 9 | core_017, core_018, core_020, core_023, gcse_012, gcse_014, gcse_015, gcse_017, gcse_018 |
| Break-even quantity | 9 | core_024, core_025, core_027, core_028, core_030, core_033, core_049, gcse_019, gcse_020 |
| Payback period | 3 | core_026, core_029, core_038 |
| Pay rate (per day, per hour) | 2 | core_019, gcse_016 |
| Other rate (per donor, miles per litre) | 2 | core_021, core_022 |
| Net cost after interest earned | 1 | core_042 |
| Disposable income | 1 | core_046 |
| Cost of the goods actually used | 1 | core_044 |
| Disputed: two measures in play | 4 | core_031, core_037, core_039, core_050 |
| None computable from the item | 2 | core_047, core_048 |
| **Total** | **70** | |

**Items needing changes**

- **Criterion sentence:** 55 items need one added. 15 already ask or state theirs (core_021, core_024, core_025, core_026, core_027, core_028, core_029, core_030, core_033, core_038, core_041, core_046, core_049, gcse_019, gcse_020); of those, core_025 should add "worth it means cheaper", as gcse_019 does.
- **Content change beyond the criterion (a distractor, key or explanation must change): 23 items:** core_007, core_011, core_014, core_017, core_020, core_021, core_023, core_031, core_037, core_039, core_044, core_047, core_048, core_050, gcse_003, gcse_007, gcse_011, gcse_012, gcse_013, gcse_014, gcse_015, gcse_017, gcse_018. core_042 needs only its measure declared (with core_011); core_019 was fixed in #392.
- **Every item** needs its measure declared in data, under the proposed design.

**Current item fields** (all 70 items have exactly these):

- `id`, `level` (`gcse` | `core`), `type` (`direct` | `hidden` | `rate` | `breakeven`), `scenario` (prose)
- `optionA`, `optionB`: `{label, details: [{key, value}]}`, where `value` is display text (for example "£35", "28p per kWh", "12 weeks × 5 days"), not numbers
- `conclusions`: `[{text, correct}]`, free text and a boolean
- `explanation` (prose)

`type` does not determine the measure: `hidden` items use total cost, `rate` items use unit cost, pay or other rates, and core_045 is typed `breakeven` but is a direct comparison.

**Can the verifier compute each measure from existing data?** Today's `scripts/verify-better-value.py` does not read numbers from items. Its `REVIEW` table restates each item's figures by hand (the KEY and ALSO values, the WIN words and the ORDER), then checks that the keyed card and the explanation state them. It decides whether a distractor is true in one narrow case: `BREAK_EVEN` and a regular expression fail a wrong threshold option that is true, for three items only (gcse_019, core_028, core_033). `MUST_SAY` pins words in seven scenarios or cards. No other distractor is judged.

| Measure | From existing fields? | What is missing |
|---|---|---|
| Total cost | No | Quantities and periods are in the scenario prose (260 days, 350 kWh, 2,000 copies), not the deal cards; the cards hold display strings |
| Unit cost | Partly | Price and quantity are in the cards for core_017, 018, 020, 023 and gcse_014, 015, 017, 018, as strings ("1.2 kg", "£3.60") that a parser could read; gcse_012 needs the car count |
| Break-even, payback | No | The fixed and per-unit costs are in the cards as strings; the question's "cheaper, not the same" convention is in prose only |
| Pay, other rates | Partly | As unit cost |
| Net cost, disposable income, usable value | No | Rates (3% AER, a sixth for tax) are in the prose |
| Disputed, none computable | No | No declared measure; core_047 and 048 lack the data (how long a clean lasts; claim chance and cost) |

**For the verifier to fail a distractor that is true under the measure,** each item needs three new fields:
1. `measure`: one name from a fixed list.
2. `inputs`: numbers per option, plus the quantity or period.
3. A structured claim on each conclusion: which option it says wins, or "same", and any figure it states.

Free-text conclusions cannot be judged mechanically. The verdict-true, reason-false cases (core_031 C1, gcse_012 C1, gcse_013 C1) need the claim's figure checked as well as its winner.

**Does the evidence support the design?** Mostly, with three limits:
- **It fits 64 of 70 items** (every measure except the disputed and none-computable rows), once a criterion sentence and the missing quantities are added.
- **Four items have two defensible measures** (core_031, 037, 039, 050). The design forces a choice, which is the point, but the choice is Jon's.
- **Two items cannot be computed at all** without new data (core_047, 048). Either new data is added or the items are rewritten.
- **Three items are "right verdict, wrong reason" cases** (core_031 C1, gcse_012 C1, gcse_013 C1). A measure-only check would pass them, because the claimed winner is the key's winner. The verifier would need to check the stated figure too, or the option rewritten so that its verdict is also wrong.
