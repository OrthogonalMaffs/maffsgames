# Brief for Gemini — escape-room lock generation

Paste everything below the line. Written 2026-08-26 after auditing the first batch of 20
(`escape-puzzle-bank.md`). The output format is the important part: it is designed so every lock
can be verified mechanically by `scripts/check-lock-bank.py` before anyone builds it.

---

## Feedback on your first twenty

The generation was strong. Fourteen of the twenty are correct as written, and several are better
than anything in our prototype room — the coolant mixture, the fuseboard simultaneous equations,
the congruence channel-tuner and the conditional-probability Venn are all going straight into
rooms. The diegetic instinct is right: instruments rather than input boxes, and the maths as the
action.

Six had faults. Three of those are fatal for an escape room specifically, and the reason is worth
stating as a rule:

> **A lock has exactly one answer. If two values open it, it is not a lock.**

- **Vending machine.** `2x + 5y = 37` with an odd coin count has two solutions: 16×20p + 1×50p
  (17 coins) and 6×20p + 5×50p (11 coins). You found both and wrote "select either". That is fine
  for a worksheet and unusable for a lock, because the puzzle no longer has a determinate state.
  *(Adding "and as few coins as possible" fixes it and makes it a better puzzle.)*
- **Bookshelf lever.** `30d₁ + 40d₂ = 120` on 0.1 m notches has two solutions, (1.6, 1.8) and
  (2.0, 1.5). It also describes a **metre** ruler while both answers sit past 1 m.
- **Laser deflector.** Incoherent. A mirror reflects an *incoming* ray to an *outgoing* one, and no
  incoming ray is given. The working takes the gradient from mirror to sensor — the outgoing beam —
  and sets the mirror perpendicular to it. A mirror perpendicular to a ray reflects it straight back
  along itself, so the beam never reaches the sensor.

Two more had answers that fail their own stated constraint:

- **Thermal bounds.** 145 × 2.45 = **355.25**, not 355.225.
- **Fire escape ramp.** The exact distance is 6.0183 m. Rounding down to 6.0 m gives an incline of
  **28.07°** against a stated 28° maximum — the answer breaks the rule the puzzle is about. With a
  safety bound you round the safe way: 6.1 m.

And one reached the right answer via working that contradicted itself:

- **Prime hash.** 2592 is genuinely unique in range. But your working explicitly rejects it
  — *"no factor of 7, invalid"* — and then selects it five lines later. The clue wording
  "prime factors include only 2, 3 and 7" also reads as requiring all three, which would exclude it.

None of this is a criticism of the ideas. It is a request for one extra step before you write an
answer down: **enumerate the solution space and confirm the count is one.**

## What we are building now

Short rooms. **Two or three locks, solvable in under 15 minutes**, designed to end a lesson well
rather than fill one. That changes what we need from you:

- **Each lock should take a group of three or four students about four minutes** once they have the
  clue in hand — including the thinking, not just the calculation. Not thirty seconds, not ten
  minutes.
- **One insight per lock.** The best of your first batch had a single "aha" and then clean
  arithmetic. Multi-stage derivations belong in longer rooms; here they burn the whole budget.
- **The instrument should carry the answer.** A dial set to a bearing, a plunger stopped at a
  volume, two valves at a ratio. Not "type the number in a box" unless the number genuinely is a
  code.
- **Assume the clue text is all they get.** No teacher explanation, no worked example on screen.

**The answer must not be a number the student can read off the clue.** Added after batch 3, where
two locks were mathematically perfect and still unbuildable: a pressure gauge whose answer was
48 psi worked, but the version sent answered **30 psi** with "30 cubic metres" printed in its own
clue, and a Venn dial answered **15** with "15 idle" in its own clue. A group that dials in a
number they can see and gets a green light has learned that guessing works. Check the answer
against every figure in the clue text before sending it.

**Every scenario needs a STAKES line: what failure costs, inside the fiction.** The strongest
thing in batch 4 was a consequence with a face on it - pull the wrong wire and the canteen
freezers lose power, so every ice cream in the school melts and the whole year group knows whose
fault it is. Keep it comic and material (melted ice cream, a soaked kit bag, a bronze statue
nobody wanted), keep it the class's own problem, and never make it a person hurt or a student
humiliated.

**If a scenario names three instruments, send three lock blocks.** Batch 3's five storylines named
five locks that never arrived — an equipment locker, a feeder, a heat lamp, a set of sprinkler
valves and a mat-tiling grid — and each had to be written this end to make the room buildable.

## What to send back

**As many as you can — we want a large bank to draw from.** Spread across KS3, GCSE, GCSE Higher,
A-Level and Core Maths, and across topic areas (number, algebra, ratio and proportion, geometry,
statistics and probability). Repeats of a topic are fine if the instrument is genuinely different.

Use exactly this format per lock, one block each:

```
ID:          short-kebab-name
LEVEL:       KS3 | GCSE | GCSE Higher | A-Level | Core Maths
TOPIC:       e.g. Inverse proportion
INSTRUMENT:  what the student physically sets, and its range/granularity
             e.g. "dial, 000-359 degrees, whole degrees"
CONTEXT:     1-2 sentences of diegetic setup
CLUE:        the exact text the student reads. This is all they get.
ANSWER:      the single value the instrument must be set to
AHA:         the one insight, in a sentence. What must they realise?
MISCONCEPTION: the specific wrong answer a student is most likely to reach, and its value
SOLVE:       3-5 lines of working
TIME:        your honest estimate in minutes for a group of 3-4 at that level
VERIFY:      a one-line Python expression that enumerates the FULL candidate space
             and filters it by every constraint, returning a list.
             It must return exactly one element.
```

**The VERIFY line is the part we most need**, and the part that was missing last time. Examples of
what it should look like:

```python
# a 3-digit code with several constraints
[n for n in range(100,1000) if len(set(str(n)))==3 and sum(map(int,str(n)))==9 and n%2==0 and n<500]

# a dial in whole degrees
[d for d in range(360) if (d + 126) % 180 == 0]

# two coupled valves, whole litres
[(a,b) for a in range(16) for b in range(16) if a+b==15 and 0.2*a+0.7*b==0.4*15]

# a length in cm to 1 d.p., where a bound must be respected
[round(d,1) for d in [i/10 for i in range(1,200)] if math.degrees(math.atan(3.2/d)) <= 28][:1]
```

Rules for VERIFY:
- Enumerate the **whole space the instrument can be set to**, not just the values you had in mind.
  If the dial goes 0–359, iterate all 360.
- For continuous instruments, discretise at the granularity the instrument actually offers.
- Include **every** constraint from the CLUE, and no constraint that is not in the CLUE. If a
  constraint is needed to make the answer unique, it must appear in the clue text the student reads.
- Then state the length of the result. **If it is not exactly 1, fix the puzzle before sending it.**

Standard library only, `math` allowed. Keep it to one line where you can.

## What makes one good, for calibration

The strongest in your first batch was the **coolant mixture**: two valves, one balance equation,
a genuine misconception waiting (adding percentages), a unique answer, and the instrument *is* the
answer. Aim at that.

The weakest pattern to avoid is a lock that announces what it wants — "set the hands to 105°"
is a toll gate wearing a costume, because nothing has to be worked out except the sum. Prefer a
clue that describes a *situation* and leaves the student to work out what the instrument should
therefore read.
