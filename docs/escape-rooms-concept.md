# Maths Escape Rooms — design concept

**Started:** 2026-08-26. Reference point: **Unlock!** — narrative escape-room games
with an app, hidden objects, card combination, penalties and a running clock.

**Nothing here is agreed.** This is a design position to argue with.

Kept separate from `idea-backlog-2026-08.md` (Gemini's list) and `jon-playtest-2026-08.md`
(Jon's play-testing). This is a format, and a much larger one than either of those files holds.

> **The brief, in Jon's words:** multiple rooms for each level. A real story that hooks students,
> where they solve maths puzzles to progress the narrative — save the princess, stop the countdown.
> Some existing questions can be reused, but **this has to be REALLY good.**

---

## 1. The thing that kills educational escape rooms

Almost every "maths escape room" already published is a worksheet with a story stapled on:

> Answer these six questions. Take the first digit of each. That's your code. You escaped!

The maths and the fiction never touch. Students learn instantly that the story is decoration and
start ignoring it, at which point it is a worksheet with extra reading. **This is the failure mode
to design against, and it is the default one** — it is what you get by accident.

The first draft of this document proposed exactly that, dressed up as "leverage the 93 existing
banks". Jon was right to reject it. Cheap is not the goal here.

## 2. What Unlock! actually does, and what transfers

| Unlock! mechanic | Why it works | Maths translation |
|---|---|---|
| **Combine two cards** — add their numbers, reveal a third | The *combining* is the verb; you act on the world | Objects carry quantities. The puzzle states the relationship. Arithmetic becomes the act of using two things together |
| **Hidden objects in illustrations** | Rewards looking closely | Numbers hidden in the scene: a scale on a plan, a reading on a dial, a date on a label |
| **Codes and locks** | Discrete, checkable, satisfying | Any answer that reduces to digits |
| **Penalties for wrong codes** | Real stakes; guessing costs you | Time penalty. Crucially this punishes *guessing*, so students must actually be sure |
| **Tiered hints** | Nobody gets truly stuck | Essential for a classroom — see §6 |
| **The "aha"** | The puzzle is working out *what* the puzzle is | **The most important one.** See below |

**The "aha" is the whole game.** In a good Unlock! puzzle the computation is trivial once you see
what to do; the pleasure is in seeing it. A maths escape room should put the insight *before* the
arithmetic, not after. That is also, not coincidentally, the exact skill exams test and drills
cannot: deciding which method the situation needs.

## 3. The design rule everything else follows from

> **The maths must be the action, not the toll gate.**

Bad: a door asks for a code; a question appears; you answer it; the door opens.
Good: the door has a dial marked 0–360, and the only way to know where to set it is to work out
the bearing from the map on the wall. **Setting the dial is the answer.** There is no question,
there is a situation.

Concretely, that means the interactions are *instruments*, not input boxes:

- a **dial** you turn to a bearing or an angle
- a **ruler** you drag across a scale drawing
- a **balance** that must be levelled
- **valves** you set to a ratio
- a **regulator** you raise until a rate matches
- a **number line** you place a value on

The site already has this kind of tooling: `constructions-lab` has a working compass-and-ruler
canvas, `bearing-blitz` has drag interaction, `graph-sketcher` and `negative-number-line` have
placement tools. **The instrument layer partly exists** — it has just never been used
diegetically.

## 4. A worked scene, so this is judgeable

*Room: "Cold Chain" — GCSE, scene 3 of 8.*

> The cold store holds the antiviral. Its door has a four-digit keypad. Pinned beside it is an
> architect's floor plan of the store, marked **1:50**. A handwritten note is taped to the keypad:
>
> *"Sick of forgetting this. Code is the floor area in square metres, to the nearest whole
> number — twice."*

The student drags a ruler across the plan, gets 8 cm × 6 cm, applies the scale, and enters it.

**The aha:** the plan is 1:50, so 8 cm is 4 m and 6 cm is 3 m — area 12 m², code `1212`. The
trap is converting the *area* by 50 instead of the lengths, or by 50 instead of 50². A student
who does that gets a wrong code, a time penalty, and — this is the point — **discovers their own
misconception through consequence rather than a red cross.**

That is `scale-factor-scaling` as an action. Same curriculum content as the existing game; utterly
different experience. The number the lock wants is not "the answer to question 3" — it is a fact
about the room.

**Why "twice"?** Because a 2-digit answer has to fill a 4-digit lock, and a diegetic reason to
repeat it is better than an arbitrary one. Small things like this are the difference between
"REALLY good" and "fine".

## 5. Engine vs content

- **The engine** (build once): scenes, inventory, examine/combine, locks and instruments, the
  clock, penalties, tiered hints, narrative delivery, **save state**, and an accessible fallback
  for every instrument.
- **A room** (build many): the story, the scenes, the art, the puzzle chain, the hint ladder.

The engine is the smaller half. **The content is the hard part and the part that decides whether
this is good** — which is exactly why the first draft's "assemble rooms from banks automatically"
idea was wrong.

Existing question banks still have a place: as *texture*. A terminal that needs three quick
percentage conversions before it boots is a fine use of `percentage-flip`'s bank. But a bank
question can never be the spine of a scene.

## 5b. Length — revised 2026-08-26

**Target is now under 15 minutes, two or three locks.** These end a lesson well rather than
filling one. That is a better product than a 40-minute room for three reasons: it fits the slot
teachers actually have spare, it survives a class that starts slowly, and it makes a room cheap
enough to build several of.

It changes the puzzle spec, not just the count. Each lock gets roughly four minutes for a group
of three or four *including the thinking*, so:

- **One insight per lock.** Multi-stage derivations belong in a long room; here they eat the
  whole budget.
- **Searching has to be quick.** Six to eight objects, not fourteen.
- **Hints matter more, not less.** There is no time to be stuck for five minutes.

`the-perfect-prank` is built to the old 40-minute spec and is now the outlier. Keep it as the
long-form example and build the short rooms to this section.

## 5c. Stakes — added 2026-08-26 (Jon)

**Every room states what failure costs, in the fiction, before it is built.** Not a lost score, not
a red cross: a consequence with a face on it. The Heatwave Mutiny got this first — pull the wrong
wire and the failsafe reroutes power from the canteen freezers, so every ice cream in the school
melts and the whole year group knows exactly whose fault it is.

Why it matters more than it looks:

- **It gives the penalty clock a reason to exist.** §2 lists penalties as the mechanic that stops
  guessing. A penalty that costs points punishes an abstraction. A penalty that costs the school's
  ice cream punishes *you*, and the difference is felt round a shared Chromebook.
- **It makes the wrong answer worth looking at.** Each lock already names the misconception a
  student is most likely to hit. Attach the failure image to that specific wrong value and the
  mistake becomes the funniest thing in the room instead of the most shameful.
- **It is free.** One paragraph per room, written at the same time as the hook.

Two rules learned immediately: keep the cost **comic and material** — melted ice cream, a soaked
kit bag, a bronze statue nobody wanted — never a person hurt or a student humiliated; and make it
**the class's own problem**, not a stranger's. Nobody has to save a city. They have to not be the
year group that cancelled ice cream.

Every room in `escape-rooms-scenarios.md` now carries an "If they fail" paragraph, and
`escape-room-image-prompts.md` gives each one a picture.

## 6. Classroom requirements — non-negotiable, and easy to forget

- **Progress must survive a refresh.** A class losing 30 minutes to a reload will never be given
  the format again. `schools/assets/score-history.js` already does device-local persistence.
- **Tiered hints, teacher-visible.** Three levels: nudge, method, answer. Without these the
  bottom third of a class stalls at scene 2 and the lesson dies.
- **Sized to the slot.** Under 15 minutes of play, so it ends a lesson rather than being one.
- **Group play round one device is a feature.** Escape rooms are social and schools are short of
  devices. Four students round one Chromebook is the intended experience, not a degraded one —
  nothing else on the site works that way.
- **A teacher page**: answers, the hint ladder, curriculum content, expected timings.

## 7. On the premises

"Stop the countdown" is a strong spine — a visible clock is genuinely motivating. Two practical
notes on the specific examples, offered as staffroom pragmatism rather than principle:

- **A deadly-virus outbreak** may land awkwardly in some schools, and will certainly land
  differently on some students, than it would have in 2019. A *containment* or *contamination*
  frame keeps every bit of the tension without the association.
- **"Save the princess"** is fine as shorthand between us, but as an actual room it starts the
  activity by telling half the class the story is not for them. Rescue plots work; it is worth
  the ten minutes to make the person in trouble someone any student can picture being.

Premises that carry maths naturally, one per level:

- **KS3 — "The Lock-In."** The class is locked in the school after hours and the caretaker's
  systems are failing. Scale plans, timetables, angles in corridors, money in the vending machine.
- **GCSE — "Cold Chain."** A refrigerated medical shipment is failing somewhere in the supply
  chain and the students have to find where. Rates, ratio, bounds, compound growth, graphs.
- **Core Maths / L4 — "The Audit."** Something in a company's numbers does not add up and the
  students have until the board meeting. Index numbers, expected value, hypothesis testing,
  break-even — Core Maths is *made* of this and the frame is genuinely adult.

## 8. Honest assessment

This is the biggest thing on the site by a distance. A good room is 8–12 bespoke puzzles with
custom interactions, written narrative, hint ladders and art — it is not a game, it is closer to a
small production. The engine amortises the mechanics but not the writing or the puzzle design.

That is an argument for **doing one properly**, not for doing it cheaply or not at all. One
excellent room is worth more than four thin ones, and it is the only way to find out whether the
format earns the effort. There is also a real number to test against: the site's completion rates
are 8–9% on its most-played games. If a room beats that substantially, the case is made.

## 9. Where this ended up — 2026-08-31

The proposed next step was one scene at full quality. What actually happened is that the engine
turned out to be small enough to build in one go, so the six buildable rooms of the day (C-H) went
live together — and by the end of it **eight rooms (C-J) are live and playable** at
`/escape-rooms/`, with a teacher page each. They went live on 2026-09-01 — indexed, in the sitemap
and led from the front page; the teacher pages stay `noindex` because they hold the answers. See the Escape Rooms section of
`CLAUDE.md` for the build and where the code lives.

**Two more went up the same day (I and J), from locks Jon wrote rather than Gemini.** They took a
morning each rather than a build, which is the real result here: with the engine, the generator and
the checker in place, a room is now six verified locks and an afternoon of prose. Both were drawn
the same day too. The set stood at forty-five images then; the eight victory pictures followed on
2026-09-01 and closed it at **fifty-three images across eight fully illustrated rooms**. Winning a
room had been paying off in prose over the establishing shot — the room as you found it, under
text describing everything you had just changed — which is the one thing this document's §5c did
not think to ask for.

Everything in section 5-6 is implemented: instruments rather than input boxes, a penalty clock, a
three-step hint ladder, save state that survives a refresh, a typed fallback on every instrument,
and a teacher page with answers, timings and the hint ladder.

Two things went further than this document asked for.

**The clues are pooled.** Section 3's difficulty rule said the puzzle is working out *what* the
puzzle is, and every scenario as written announced which clue belonged to which lock. Each room now
has eight searchable objects holding six clues and two blanks, and not one clue names its
instrument. Deciding which note goes where is the first real thinking in the room.

**Every lock draws its numbers.** A room with one fixed set of figures is single-use, which is not
much good to a department. Each lock carries a library of 2-10 verified number sets and draws one
per play — never the set it gave last time, so a replay shares no figures with the play before it.
The clue, the hints, the misconception response and the worked solution are all templated and move
together. Across the eight rooms that is 193 sets and just over 4,000 combinations. This is the
piece section 8 did not anticipate: it multiplies the value of a room for a fraction of the cost of
writing another one.

**Still untested against a class.** Every per-lock timing is the puzzle author's own and the
15-minute clock has never been run on anyone. That is the next thing, and section 8's benchmark
still stands: the site's most-played games complete at 8-9%, and a room has to beat that
substantially for the format to earn the effort.
