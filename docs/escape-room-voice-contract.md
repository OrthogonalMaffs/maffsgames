# CC Task Contract — Escape Room Antagonist Voices

**Date:** 08 September 2026
**Project:** MaffsGames — `/escape-rooms/`
**Note on flow:** This is a deliberate divergence from the normal spec → implement split. CC is running creative elicitation, not executing a finished spec. The risk is CC generating character voices *for* Jon rather than drawing them out of him, which would reproduce the original defect. The STOP IF conditions exist to guard against that.

---

## TASK

Run eight separate interview sessions with Jon — one per escape room — to establish each antagonist's name, character and voice, then rewrite that room's narrative text in the agreed voice.

## ROOT CAUSE

The eight escape rooms at `/escape-rooms/` were built fast over summer 2026 with generated narrative text and no authored voice. A teacher's feedback via the site form (08/09/2026) identified the text as visibly AI-written and the rooms as unusable in class. The puzzles and the maths are sound; the prose has no author behind it.

## CLASS CHECK

**Architectural, not local.** The same defect — unauthored narrative voice — appears in all eight rooms and in the shared text slots (setup, lock-open, wrong-entry, escape) that every room uses. Fixing one room's prose leaves seven identical instances. The fix is to establish a voice per antagonist and rewrite against the shared slot structure, not to patch individual strings.

## EXACT CHANGE

Per room, in sequence, **one room per session**:

1. Read the room's existing setup text, puzzle flow and all narrative strings **before asking anything**.
2. Interview Jon to establish:
   - Antagonist name — comedy surname, real-sounding, no equipment puns, no playground-innuendo risk
   - What they've locked and why they think it's justified
   - Whether they understand the maths behind their own locks
   - How they speak — sentence length, vocabulary, verbal tics, three lines they would never say
3. Produce a written character sheet from Jon's answers.
4. Rewrite the room's four narrative slots in that voice: **setup**, **lock-opens**, **wrong-entry**, **escape**.
5. Jon reviews before any file is touched.

### Fixed constraints across all eight

- Students are always the heroes; the antagonist is the obstacle they overcome.
- Wrong-entry lines never mock the student or their answer — only the lock.
- The antagonist loses graciously at the escape. No humiliation.
- Voice is established through the room setup, not a narrator layer over the top.
- "Idiot" and "stupid" never appear. "Muppet" is permitted.
- British English throughout.

### Room 1 — already agreed, use as reference implementation

**The P.E. Shed Rebellion** (KS3/GCSE — sectors, inverse proportion, sequences)

**Mr Barry Lunge — "Lungey".** Head of P.E. for twenty-six years. Old-school, no-nonsense. Believes every problem yields to running faster or jumping higher. Padlocked the shed because the equipment was "getting soft" being borrowed by anyone who asked — in his view this is standards, not cruelty. **Does not understand the maths he has locked things behind.** He believes the locks test grit, and if told otherwise would say that's the same thing.

*Speech:* Short sentences, often no verb. Shouts sparingly — one capitalised word per speech at most. Sporting metaphor applied to everything, including things it does not fit. Calls students "son" and "you lot". Nostalgic asides that go nowhere. Never swears, never insults.

*Would never say:* "Let me explain the reasoning." / "That's a clever bit of maths, that." / "Fair enough, you've got me."

**Draft slots:**

> **Setup —** Right. Shed's locked. Don't look at me like that — the equipment's been walking off since February and I've had enough. Three locks. You want the cones, you go through them. In my day we didn't have a shed, we had a hedge, and we were grateful. Get on with it.

> **Lock opens —** Hah! There we are. That's what a bit of effort looks like. Two left.

> **Wrong entry —** Still locked, son. Push through it. Nobody ever got anywhere sitting there thinking about it.

> **Escape —** ...Right. Well. Fine. You've got in. That's — that's grit, that is. Twenty-six years and I've never seen a group crack all three. Go on, take the cones. Bring them back this time.

## DO NOT TOUCH

- Puzzle logic, question generation, number randomisation, answer validation
- Lock mechanics
- The teacher answer page
- The escape-rooms index page
- Room images
- Any of the 86 games
- `/games/the-perfect-prank/` — out of scope

**Text strings only.**

## SUCCESS CONDITION

Eight character sheets, each derived from Jon's own answers rather than CC's suggestions, and eight rewritten room texts signed off by Jon. Read side by side with the names removed, the eight antagonists are distinguishable by voice alone.

## STOP IF

- Jon's answers are thin and CC finds itself inventing the character rather than drawing it out — stop and say so rather than filling the gap.
- Any rewrite would require a change to puzzle logic or lock behaviour.
- A proposed name carries innuendo or maps onto a real, identifiable member of staff.
- More than one room is in progress at once. One room per session, reviewed before the next starts.
- The maths in a room appears wrong during the read — flag to Jon, do not fix in passing.

---

## Room reference

| Room | Level | Topics |
|---|---|---|
| The Great Hamster Heist | KS3 / GCSE | Circumference, upper bounds, gradient |
| The P.E. Shed Rebellion | KS3 / GCSE | Sectors, inverse proportion, sequences |
| The Canteen Menu Hack | KS3 / GCSE | Averages, simultaneous equations, fractions |
| The Heatwave Mutiny | KS3 / GCSE | LCM, surface area to volume, inequalities |
| The Prom Budget Embezzlement | GCSE / Core | Reverse percentages, compound growth, Venn |
| The Rugby Mud Sabotage | GCSE | Area scale factors, combined rates, indices |
| The Headteacher's Car Trap | GCSE / Core | Lower bounds, arc length, quadratics |
| The IT Teacher's Vengeance | GCSE Higher | Permutations, HCF, quadratic vertex |
