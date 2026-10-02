# Escape room scenarios — narratives to build

**Source:** Gemini, 2026-08-26, for A–H; Jon, 2026-08-31, for I and J. Three-lock scenarios that
wrap locks from the audited bank (`escape-puzzle-bank.md`) in a story.

## Status, 2026-08-31

| Room | Locks | Art | State |
|---|---|---|---|
| A — Coach Trip Hijack | 2 verified, 1 carries an arithmetic error | none | **not built** — needs a maths pass |
| B — Tuck Shop Heist | 1 verified, **2 rejected** | none | **not built** — needs a maths pass |
| C — P.E. Shed Rebellion | 3, all pass | complete | **built and live** |
| D — Prom Budget Embezzlement | 3, all pass | complete | **built and live** |
| E — Great Hamster Heist | 3, all pass | complete | **built and live** |
| F — Rugby Mud Sabotage | 3, all pass | complete | **built and live** |
| G — IT Teacher's Vengeance | 3, all pass | complete | **built and live** |
| H — Heatwave Mutiny | 3, all pass | complete | **built and live** |
| I — Canteen Menu Hack | 3, all pass | complete | **built and live** |
| J — Headteacher's Car Trap | 3, all pass | complete | **built and live** |

C-J are at `/escape-rooms/<slug>/`, unlisted and `noindex`, each with a teacher page, and all eight
are illustrated. I and J were built and drawn on 2026-08-31. The narratives
below are the source these were built from; the built rooms differ from them in two deliberate ways,
both described under "The warning that applies to all five":

- **the clues are pooled**, so no note names its own lock, and
- **the numbers are drawn per play** from a verified library, so the figures written into the
  scenarios below are only the first set of several.

Rooms A and B are the only ones not built. Both need a maths pass before any art.

**Read the warning under each before building.** Between them these two rooms reuse three locks
that the audit rejected or corrected, and neither narrative knows that.

---

## A. The Coach Trip Hijack — GCSE

> The sat-nav has mysteriously broken on the way to a very boring Geography museum. The class has
> to secretly reprogram the digital dashboard and divert the coach to a theme park without the
> driver noticing.

Strong hook. The premise does real work: a coach dashboard is a *natural* home for a bearing dial,
a tachometer and a fuel gauge, so three unrelated topics sit together without contrivance. That is
the hardest part of room design and this gets it for free.

| Lock | Instrument | Topic | From the bank | Status |
|---|---|---|---|---|
| Steering column | Bearing dial, 000–359 | 3-figure bearings, co-interior angles | #1 CCTV Blindspot | **Verified** — `054°` |
| Speed limiter | Tachometer, RPM | Circumference + compound units | #14 Conveyor Gearbox | **Verified** — `180 RPM` |
| Fuel gauge | Reserve-limit slider | Upper and lower bounds | #5 Server Room Thermal Bounds | ⚠️ **Corrected** — see below |

### ⚠️ Before building

**The fuel-gauge lock carries an arithmetic error.** Bank #5 states 145 × 2.45 = 355.225. It is
**355.25**. Re-derive whatever numbers the fuel version uses rather than transplanting them.

There is also a teaching subtlety worth keeping rather than smoothing away: an upper bound is a
value the quantity stays strictly *below*, so a "maximum consumption" dial is set to a figure that
is never actually reached. In a fuel context that is genuinely the right way round — you prove you
will not run dry by assuming the worst case you cannot quite hit.

**Timing.** The scenario says 40 minutes. Rooms now target **under 15** (see
`escape-rooms-concept.md` §5b). Three locks is right; the framing needs rewording.

---

## B. The Tuck Shop Heist — GCSE Higher / Core Maths

> The caretaker has accidentally set the heating to maximum and the premium chocolate is going to
> melt. The class must defeat the caretaker's eccentric homemade security system.

Good hook, and "eccentric homemade security system" is a licence to put any instrument in the room
without justifying it — useful.

| Lock | Instrument | Topic | From the bank | Status |
|---|---|---|---|---|
| Laser grid | Angular slider | Perpendicular gradients | #3 Laser Tripwire Deflector | ❌ **REJECTED** |
| Heavy grate | Weight slots on a ruler | Moments / levers | #17 Library Bookshelf Lever | ❌ **REJECTED** |
| The vault | Coordinate crosshairs | Linear inequalities, feasible region | #15 Drone Drop-Zone | **Verified** — `(2, 6)` |

### ❌ Two of these three cannot be built as they stand

**Laser grid — incoherent, not merely wrong.** A mirror reflects an *incoming* ray to an *outgoing*
one, and #3 never specifies where the beam comes from. Its working sets the mirror perpendicular
to the *outgoing* beam, which reflects the beam straight back along itself. Setting a mirror to a
perpendicular gradient does not aim it anywhere.

*Repair — pick one:*
- Give the source, and require the mirror to lie along the **bisector** of the incoming and
  outgoing rays. Correct optics, genuinely A-Level.
- Drop the reflection entirely. A laser that must be *blocked* by a barrier perpendicular to its
  path is honest, uses the same `m₁m₂ = −1`, and is the same difficulty.

The second is better for a 15-minute room. The first is a good puzzle for a longer one.

**Heavy grate — two answers, on an impossible ruler.** `30d₁ + 40d₂ = 120` on 0.1 m notches is
satisfied by both (1.6, 1.8) and (2.0, 1.5). Two answers is not a lock. #17 also describes a
**metre** ruler while both solutions sit past 1 m.

*Repair:* pin one weight and solve for the other. With the 30 N fixed at 2.0 m, the 40 N must
supply 120 − 60 = 60 N·m, so **d = 1.5 m**. Unique, still a real moments problem, and the fixed
weight is easy to justify diegetically — it is already bolted down.

**Level check.** With those repairs the room is Higher-only. The vault (inequalities) and the
lever are both fine for GCSE Higher; the laser is the one that decides whether this is a Higher
room or an A-Level one.

---

## What both scenarios get right

Worth naming, because it is the part that is hard to do and easy to lose in a rewrite.

**One setting, three instruments, no contrivance.** A coach dashboard and a jury-rigged security
system are both places where a dial, a slider and a grid can all plausibly live. Compare the
first draft of `the-perfect-prank`, where a chair and a clock had to be argued into the same room.

**The stakes are small and personal.** Melting chocolate and a boring museum are the right size for
a 15-minute end-of-lesson activity. Nobody has to save a city.

## What to check on the next scenario batch

The bank has a `STATUS` column for a reason. Both of these were written from the original twenty
without reference to the audit, so **three of the six locks used were either rejected or
corrected** — two rejected outright and one carrying an arithmetic error — and the narratives
inherited those faults silently.

Ask for scenarios to cite the lock IDs they use, then run:

```
python scripts/check-lock-bank.py <bank file>
```

and confirm every cited ID comes back `ok` before any narrative work starts.

---

# Batch 2 of scenarios — 2026-08-26

Five more, sent with their locks attached this time. **All fifteen locks are checked and pass**
(`docs/lock-bank-batch3.txt`, `15 usable, 0 rejected`), so unlike A and B these are buildable as
they stand. The audit — one fatal lock repaired, two guessable answers renumbered, five locks
written from scratch — is in `escape-puzzle-bank.md` §Batch 3.

## C. The P.E. Shed Rebellion — KS3 / GCSE

> Freezing, raining sideways, and cross-country is on. Twenty minutes to hack the P.E. shed,
> inflate the dodgeball arena inside the sports hall, and shut the teacher's waterproof coat in
> the shed.

| Lock | Instrument | Topic | ID |
|---|---|---|---|
| Sprinkler override | Radial arc slider | Area of a sector | `sprinkler-sector-area` |
| Compressor | Pressure gauge | Inverse proportion | `dodgeball-pressure-boyle` |
| Equipment locker | Combination dial | Linear sequences | `locker-nth-term` |

**If they fail:** the arc snaps to full and the sprinklers soak the kit bags stacked by the shed
door. Cross-country goes ahead exactly as planned — in sideways rain, in wet kit — while the P.E.
teacher watches from under a golf umbrella in a very dry coat.

The locker lock was named by the scenario and never written; it is written now. It gives day 3, 7
and 12 rather than three consecutive days, so the step has to be recovered by division.

## D. The Prom Budget Embezzlement — GCSE / Core Maths

> The £5,000 prom budget went on a life-sized bronze statue of the headteacher. The transfer
> clears in 35 minutes.

| Lock | Instrument | Topic | ID |
|---|---|---|---|
| Tax refund | Transfer keypad | Reverse percentages | `finance-reverse-percentage` |
| DJ deposit | Account-age slider | Compound growth | `dj-deposit-compound` |
| Network router | Bandwidth dial | Venn diagrams | `wifi-venn-router` |

**If they fail:** the transfer clears. Prom happens in the sports hall with the lights on, a
laptop playing someone's dad's playlist through one speaker, a single bowl of crisps — and the
life-sized bronze headteacher, delivered on time, beaming in the middle of the dance floor.

⚠️ **Two of these three carry repaired numbers — use the bank file, not the original message.**
The deposit lock was unsolvable (£800 at 5% for 4 years is £972.405, not £972.40) and the router
lock's answer was a number printed in its own clue.

## E. The Great Hamster Heist — KS3 / GCSE

⚠ **Rewritten 2026-09-08 — the premise below is superseded.** See `escape-rooms/hamster-heist/room.js`
and `docs/escape-room-voice-rewrite.md` §3. There is no caretaker, no tea break and no stuffed toy:
Mr Lunge confiscated Pythagoras at lunchtime and shut him in the old cage at the back of Mr Beaker's
chemistry lab, and the class have until the 3:30 bell to get him home. The swap went because it made
the students thieves who won by deception; the tea break went because the person it belonged to could
never reach them during play. **The three locks and all of their maths are unchanged.**

> The caretaker has confiscated Pythagoras the class hamster on "health and safety" grounds.
> Fifteen minutes of tea break to swap him for a suspiciously similar stuffed toy.

| Lock | Instrument | Topic | ID |
|---|---|---|---|
| Hamster wheel | RPM slider | Circumference, compound units | `hamster-wheel-rpm` |
| The feeder | Volume slider | Lower bounds | `hamster-feeder-bounds` |
| Heat lamp | Rate slider | Gradient of a line | `heat-lamp-gradient` |

**If they fail:** the feeder empties the week's pellets in one go and the heat lamp goes to full.
Pythagoras wakes up delighted, sprints on the wheel like a man possessed, and the racket brings
the caretaker back mid-biscuit — to find a stuffed toy in the cage and a hamster on the loose.

The best hook of the five, and the cheapest to draw: one cage, three fittings on it. The feeder
uses a prism with an exact cross-section so the upper bound lands on a whole 620 cm³ — bounds and
π together give a number nobody can set on a dial.

## F. The Rugby Mud Sabotage — GCSE

> The undefeated rival team arrives in 30 minutes and the Geography teacher has locked the
> sprinklers to keep the pitch perfect for them. Flood it, then plug the split hose with a piece
> of his spare elbow patch so nobody can prove it was you.

| Lock | Instrument | Topic | ID |
|---|---|---|---|
| The elbow patch | Fabric cutting dial | Area scale factors | `elbow-patch-scale` |
| Sprinkler flow | Flood timer | Combined rates | `sprinkler-flow-rates` |
| The scoreboard | Two score dials | Index laws, simultaneous equations | `rugby-scoreboard-bases` |

**If they fail:** the flow reverses and floods the home changing rooms instead. The rival team
runs out onto a flawless pitch in spotless white; our lot squelch out behind them plastered in mud
from the knees down, and the Geography teacher is holding up one ruined elbow patch.

The flow lock changed shape: "ratio valves" as described is either trivial or has many answers, so
it is now two valves feeding one timer — 20 minutes and 30 minutes alone, 12 together.

## G. The IT Teacher's Vengeance — GCSE Higher

> The gym hall is locked and the gymnastics team is being made to listen to dial-up modem sounds
> instead of their routine music. The way in is his prized custom mechanical keyboard.

| Lock | Instrument | Topic | ID |
|---|---|---|---|
| Macro pad | Overload dial | Arrangements with repeats | `mechanical-keyboard-perms` |
| Vaulting horse | Height slider | Quadratic turning point | `vault-trajectory-vertex` |
| Mat tiling | Mat-size slider | Highest common factor | `mat-tiling-hcf` |

**If they fail:** the mats deploy at the wrong size and concertina into one enormous folded lump
in the middle of the floor, and the PA locks to dial-up modem tones at full volume for the whole
routine. The team performs around the lump. The IT teacher watches from the door, arms folded,
happier than he has ever been.

The hardest room of the five and the only one that is Higher throughout. The vault lock is the
longest single lock in the bank at 5 minutes — if a room has to lose one to timing, it is this.

---

## The warning that applies to all five

**Every one of these rooms announces which clue belongs to which lock.** The sprinkler clue is at
the sprinkler, the locker clue is on the locker. That is the exact structure Jon solved in six
minutes in `the-perfect-prank`, and the concept doc's difficulty rule says so plainly: difficulty
comes from not knowing which clue goes where, not from harder arithmetic.

The fix costs nothing at build time. Put the three clues in the room as objects — a clipboard, a
groundsman's log, a compressor label — and let the students decide which instrument each one is
about. Same locks, same maths, and the first real thinking happens before any of it.

---

## H. The Heatwave Mutiny — KS3 / GCSE

> The board has switched the air conditioning off through a 32°C heatwave and the control room is
> on the prefects' patrol route. Pull the wrong wire and the failsafe takes the canteen freezers
> instead — every Cornetto in the school, gone, and everyone will know whose fault it was.

| Lock | Instrument | Topic | ID |
|---|---|---|---|
| Patrol window | Countdown timer | Lowest common multiple | `patrol-lcm-timer` |
| Security door | 4-digit keypad | Surface area to volume | `cube-surface-volume` |
| The wire nest | Frequency tuner | Inequalities with a prime constraint | `canteen-freezer-inequality` |

Sent with all three locks attached and all three pass unaltered (`docs/lock-bank-batch4.txt`).

**The stakes are the best thing here — Jon's idea, and it is now a rule** (see
`escape-rooms-concept.md` §5c). Every other room as first written had a reward for winning; this
one has a *cost for guessing* that lives inside the fiction — a wrong wire melts the ice cream.
That is the Unlock! penalty mechanic arriving from the story rather than being bolted onto it.

**Retrofitted to C–G on 2026-08-26.** Each of those rooms now carries an "If they fail" paragraph,
and every new room needs one before it is built.

**Framing.** The hook says 35 minutes; the three locks total 11. Reword to the 15-minute target
rather than rebuilding the room — the same edit scenario A needs.

**And the same warning as C–G:** each clue is found on the instrument it belongs to. Put the rota,
the sticky note and the wiring manual in the room as objects and let the students work out which
is which.

---

## I. The Canteen Menu Hack — KS3 / GCSE

> Healthy Week has replaced the chips with baked kale and put a chocolate cookie up to £5. The
> class has until the lunch bell to get into the central smart till, put the prices back and get
> pizza onto the menu.

| Lock | Instrument | Topic | ID |
|---|---|---|---|
| The dietary slider | Calorie slider, 0–1000 kcal | Mean averages, missing value | `canteen-mean-calories` |
| The price tags | Two dials, £0–£10 | Simultaneous equations | `cookie-price-simultaneous` |
| The disposal chute | Portion dial, 0–200 | Fractions of an amount | `kale-fraction-drain` |

Sent by Jon with all three locks attached and all three pass (`docs/lock-bank-batch5.txt`). Built
the same day at `/escape-rooms/canteen-hack/`.

**The stakes are already in the fiction, which is now the rule** (§5c of the concept doc): fail and
Healthy Week is signed off as a success and kept for the term. The chute has a second cost written
into it — empty the shelf completely and the inspection fails — so the lock has a wrong answer that
is wrong in the story as well as in the arithmetic.

**The best of the three is the chute**, and it is the one to keep for the plenary. The letter says
what must *remain*; the dial counts what is *destroyed*. A student can do every calculation
correctly and still set it wrong, which is a comprehension error dressed as a maths one.

**Framing.** The hook as sent says twenty minutes; the built room says fifteen and the three locks
total ten, which leaves five for searching. Same edit as scenarios A and H needed.

## J. The Headteacher's Car Trap — GCSE / Core Maths

> The Headteacher has bought a ridiculously expensive electric sports car and taken the three best
> bays for it. Fifteen minutes to reprogram the car park before he comes down the ramp, and leave
> him one place to put it.

| Lock | Instrument | Topic | ID |
|---|---|---|---|
| The line-painting bot | Paint-volume dial, 0–20 litres | Upper and lower bounds | `visitor-space-bounds` |
| The boom gate | Angle dial, 0–180° | Arc length | `boom-gate-sector` |
| The charging post | Current dial, 0–15 A | Quadratics with a constraint | `ev-charger-quadratic` |

Sent by Jon with all three locks attached and all three pass (`docs/lock-bank-batch5.txt`). Built
the same day at `/escape-rooms/car-trap/`.

**A car park is as good a home for three instruments as the coach dashboard in scenario A** — a
paint robot, a barrier and a charging post are all things that genuinely take a number, so three
unrelated topics sit together without contrivance. That is the hardest part of room design and this
premise gets it for free.

**The comic cost is aimed squarely at the management**, which is the rule: fail and he parks across
all three bays, the minibus stays on the verge, and there is a slide about it at Monday's briefing.
No student is the butt of anything in either room.

**One thing was softened in the build.** The storyline asks the barrier to clip his paintwork.
The built room has it fold his wing mirror in instead — the same beat, without a room full of
teenagers being asked to enjoy damaging a car. The maths is untouched.
