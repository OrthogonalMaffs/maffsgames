# The Headteacher’s Car Trap: draft for Jon’s review

**Phase 1 of the Car Trap rewrite (contract CAR-TRAP-DRAFT, 9 Oct 2026, 16:45).** Draft prose only. Nothing
served is touched: `escape-rooms/car-trap/` stays as it is, behind its holding page. Phase 2 (the build, the
variants, the art and the release) is a separate contract after you approve this.

How to read it:

- `{{key.token}}` is a figure filled from the drawn variant. There are no other figures in the prose; the
  exceptions are listed in "For Jon" below.
- Prose is shown with real quotation marks and apostrophes. In phase 2 they become entities (`&rsquo;` and
  so on) in every slot except the object and lock `name` and `where`, which are escaped and keep real
  characters (canon §11.3).
- **[X]** marks a detail I extrapolated rather than took from your brief. Strike any you don’t want.
- The Head never speaks. He speaks in Prom Budget, and each character speaks only in their own room (working
  doc §4). He is "the Head" throughout and is never named, so the D Tension initial joke stays Prom Budget’s.

---

## For Jon: decisions in this draft

1. **There is no `fail` slot in `room.js`.** The engine shows `stakes` twice: on the start screen, after
   "If you get it wrong." (`engine.js:238`), and on the time-out screen, after "And so:", under the failure
   picture (`engine.js:791`). So your Fail (the barrier, the clipboard, "disappointing") is written into
   `stakes`, and it has to read correctly after both lead-ins. It does in the draft below.
2. **`hook`, `brief` and `stakes` can’t carry tokens.** The engine writes them raw, not through `fill()`, so
   they hold no figures at all. That’s also why the Head’s arrival has no clock time.
3. **Your model line has a figure in it**: "Those two bays differ by 2.6 cm." I’ve used it as wrong-entry
   line 1 with the number in words ("two point six centimetres"), because it’s spoken and it’s your line. A
   numeral there would be the only one in the room’s prose. It isn’t a clue figure (wrong-entry lines aren’t
   counted in the collision rules), but a student hunting for numbers might read it as one. If you’d rather
   it went, line 1 becomes "That line is out. This is not how it is done in MY school."
4. **Lock 1’s precision is written as "to the nearest ten centimetres"**, in words. As a numeral, the 10 would
   count as a clue figure and collide with the barrier’s and the charger’s numbers. Measured with the checker’s
   own rules: **352 of 512 joint draws are VALID in words, 184 of 512 with a numeral.** The half-interval
   (0.05 m) is a token, so the hints and the worked solution carry no bare figure either.
5. **Lock 1’s named misconception is the stated width** (the width on the sheet, treated as exact), not the
   upper bound. My reasons: it’s the error the lock exists to teach, and the one a grade 4 student makes when
   they don’t open the bounds at all. The upper bound only comes from misreading "smallest", which the card
   states plainly. It is also never reached: 2.45 m rounds to 2.5 m, so a student who sets it gets the
   ordinary wrong-entry line, which is fair. If you want the upper bound named instead, only `miss`,
   `missTitle` and `missSays` change.
6. **"A statement of environmental leadership"** (your optional line) is in the hook as reported speech: the
   Head is said to call it that, but he doesn’t speak. Strike it and the hook loses one clause.
7. **The measuring wheel in the pictures.** Your art brief puts the wheel down on a bonnet or a bollard, but
   the prose has Strictman walking the row with it. The scene prompt props it against a bollard at the far end
   of the row, as if he has just put it down to write a bay up. The brief says he measures one bay at a time,
   so picture and prose agree.
8. **Why the students are in the car park at all [X].** They are the student welcome party, told to wait by
   the lift and look smart. The old room never said. Strike it if you have a better reason.
9. **Where the hatchback is parked [X].** In the deputy head’s bay, beside the Head’s. Narrowing the Head’s
   bay widened Strictman’s own bay, and he parked his daughter’s car in it. When the line goes back to
   specification, the car is across two bays. That is the mechanism behind your win.
10. **How Strictman is heard [X].** He dictates his survey into his phone in a parade-ground voice, which
    carries in a concrete car park. He never sees the students and never addresses them, so no line can mock
    them.
11. **How he loses [X].** Your brief says he explains at length that the car is his daughter’s and loses
    graciously. I have him finish with his own standard applied to himself: "Out of specification. My error.
    It will be corrected." He then moves the car himself, perfectly. He sees his defeat, so this isn’t the
    third never-knew ending §4 warns against. The Head never knows, but the Head isn’t the antagonist.

---

## Title

The Headteacher’s Car Trap

*(Unchanged. It is still a trap, set for the Head’s car. The slug, the save key and the indexed URL stay.)*

## Hook

It is the morning of the governors’ visit. The Head is driving in to meet them, in an old plug-in hybrid that
he calls a statement of environmental leadership and everybody else calls the dullest car in the county.

Nobody here has any illusions about the Head. But the school also has a deputy head, and the deputy head is Mr
Strictman: ex-military, marches between lessons, civvies starched so stiff they could stand to attention on
their own. He wants the Head’s job. He already talks as though he has it.

He is down in the staff car park now with a clipboard and a measuring wheel, doing what he calls an efficiency
survey of the bays. You are the student welcome party **[X]**. You were told to wait by the lift and look smart.

## Brief

It is not a survey. He was in before the caretaker this morning **[X]**. He has repainted the Head’s bay
narrower than the specification allows, set the barrier to come down early, and set the charging post to trip.
When the Head arrives in front of the governors it will be a farce, and the report Mr Strictman has already
half written will say that the school lacks discipline at the top.

He is at the far end of the row, measuring one bay at a time and marching towards you. That is your fifteen
minutes.

He set three machines against their own paperwork. You are setting each one back to it: the line where the
specification puts it, the barrier to its calibration, the charger inside its limit. All the paperwork is down
here with you. Every wrong setting makes a noise that carries in concrete, and costs you time.

## Stakes (also the fail screen; see "For Jon" 1)

The Head comes down the ramp in the dullest car in the county and stops at the barrier, its arm already down in
front of his bonnet, with the governors waiting on the other side of it. Mr Strictman steps forward with his
clipboard, looks at the car, and says one word: “Disappointing.” If the top job goes to him, it is drill in the
yard every morning and uniform inspections at the gate.

*(Read after "If you get it wrong." on the start screen and after "And so:" on the time-out screen; both
work.)*

## Win

The barrier lifts. The Head comes down the ramp at the speed of a man who knows he is being watched, and glides
into his bay without touching a line. He gets out, straightens his tie and goes to shake hands with the
governors, with no idea that anything has happened to him this morning. That is how he gets through most
mornings.

The governors aren’t looking at him. They are looking at the bay next door, where, with every line back to
specification, the one car in the row parked across two bays is a small hatchback with stick-on eyelashes on
its headlights.

Mr Strictman reaches the end of the row with his clipboard. He looks at the car. He looks at the line under it.
Then he explains, at some length and standing very straight, that the car is his daughter’s, that his own is in
the garage, and that it was parked correctly when he left it.

“Out of specification,” he says at last. “My error. It will be corrected.” **[X]** He moves it himself, in one
perfect manoeuvre, and marches off to start his report again from the beginning.

---

## wrongLines (four, escalating; the last repeats)

Each `head` is the car park’s reaction; each `body` is Strictman, dictating as he comes down the row. None of
them mentions the students. The bays and the standards take all of it.

1. **head:** The setting clears with a beep that carries.
   **body:** From the far end of the row, the tick of a measuring wheel, then a parade-ground voice dictating
   into a phone: “Those two bays differ by two point six centimetres. This is not how it is done in MY school.”
2. **head:** Something in a control box resets with a clunk.
   **body:** Closer. The wheel ticks along another line. “Paint wandering on the left-hand side. Bollard out of
   true. Noted.” A pen clicks. “When this is MY car park, the lines will be inspected every morning. By me.”
3. **head:** The setting slides back to where it was.
   **body:** “Drill in the yard, eight sharp, every morning. Uniform inspected at the gate, top button to
   toecap. Standards start at the top.” The wheel ticks on. “And the top is about to change.”
4. **head:** Another one. The ticking is closer than it was.
   **body:** “Next bay.”

*(Line 4 repeating is the joke: he just keeps coming. "Eight sharp" is a time in words, not a figure.)*

---

## Objects (eight: six clues, two blanks)

Clue-carrying object `id`s are kept from the current room, because `teacher.html` maps clues to locks by `id`
(canon §11.3). The two blanks are new objects, so they get new ids.

| # | id | name | where | clue or flavour |
|---|---|---|---|---|
| 1 | `spec` | The bay specification | on a clipboard hooked to the reserved sign | **HEADTEACHER’S BAY.** Width **{{bay.W}} m**, to the nearest ten centimetres. Lines to be maintained to specification. |
| 2 | `botcard` | Card on the line marker | taped to the handle | “RE-MARKING: measures from the line next door. Set it to **the smallest width the specification allows**. Anything wider comes out of the bay next door.” |
| 3 | `maintlog` | Barrier maintenance log | in a plastic wallet zip-tied to the barrier post | BOOM ARM: **{{gate.r}} m** from pivot to tip. Counterweight checked. Arm replaced last term after the incident with the fish van. Today’s entry, in very straight capitals: SETTINGS REVISED. EFFICIENCY. Initialled. |
| 4 | `sensor` | Calibration sheet | taped inside the barrier control box | “The control box resets to its proper swing when it is given **the angle the arm turns through while its tip travels an arc of exactly {{gate.kpi}} metres**. It measures how far the tip travels round the pivot, not how high the arm lifts.” |
| 5 | `commission` | Charger commissioning label | stuck inside the charging post cover | LOAD LIMITER: **L(x) = x² − {{amp.b}}x + {{amp.c}}**, for a charging current of x amps. **Commissioning completes at zero load.** |
| 6 | `alarmnote` | Note from the site electrician | biro on the back of a delivery slip | “Anything **above {{amp.lim}} A** on that circuit and the network alarm goes off in the front office. It has done it twice this term and they blame me both times.” |
| 7 | `hatchback` | A small hatchback | in the deputy head’s bay | *(blank)* It has stick-on eyelashes on both headlights and a fluffy cover on the steering wheel. It is parked in the deputy head’s bay, which this morning is the widest bay in the row, and it is using all of it. **[X: the steering-wheel cover]** |
| 8 | `sign` | The reserved sign | on a post at the end of the Head’s bay | *(blank)* RESERVED, in old enamel. Underneath, a new laminated label has been stuck on perfectly level: UNDER REVIEW. **[X]** |

No numerals are typed into any clue, so the only clue figures are the tokens (the kiln rule, working doc §5i).
In the commissioning label, "x²" is written with the `&sup2;` entity, which the collision rules strip.

---

## Locks (all ★★ Core, grades 4–5)

### Lock 1: the Head’s bay (new; replaces `visitor-space-bounds`, which is ★★★)

- **id:** `head-bay-lower-bound` (proposed) · **key:** `bay`
- **name:** The line marker
- **brief:** Mr Strictman narrowed the Head’s bay with this. The marker measures from the line next door and
  paints a new line at whatever width it is set to. The card on its handle says which width to give it.
- **instrument:** slider · **label:** Bay width · **unit:** m · 2.00 to 3.00, step 0.01, 2 decimals, starts at
  2.00 · **verb:** Set the width. *(A slider so every value is reachable; the engine adds a "type the setting"
  box under every slider, so 0.01 steps need no fine dragging.)*
- **missTitle:** {{bay.mTxt}} m is the width on the sheet, not the smallest it allows.
- **missSays:** The specification says {{bay.W}} m to the nearest ten centimetres, so any width from {{bay.lb}} m
  up to (but not reaching) {{bay.ub}} m would have been written down as {{bay.W}} m. {{bay.mTxt}} m is in the
  middle of that range. The marker wants the bottom of it.
- **hints:**
  1. “To the nearest ten centimetres” is a range, not a number. What is the narrowest the bay could be and still
     be written down as {{bay.W}} m?
  2. Half of ten centimetres is five centimetres, which is {{bay.half}} m. A width that rounds to {{bay.W}} m can
     be up to {{bay.half}} m below it.
  3. {{bay.W}} − {{bay.half}} = **{{bay.aTxt}} m**. That width really does round to {{bay.W}} m, so the
     specification allows it.
- **solve:** To the nearest ten centimetres, {{bay.lb}} m ≤ width < {{bay.ub}} m. The smallest width allowed is
  **{{bay.aTxt}} m**.
- **onOpen:** The marker trundles down the old line and lays a new one beside it, crisp and wet, exactly where the
  specification says. The bay next door has lost a little. Something in it is now sitting on a line.

**Proposed variant parameters, for `gen-escape-variants.py`.** These are proposals only; the generator is not
touched in this phase.

| | value |
|---|---|
| Stated width `W` | 2.4 m (variant 0, the bank’s), then 2.2, 2.3, 2.5, 2.6, 2.7, 2.8, 2.9 m: eight variants, every realistic bay width, no whole metres |
| Precision | to the nearest 0.1 m, written "ten centimetres" in the prose (see "For Jon" 4) |
| Instrument | slider, 2.00 to 3.00 m, step 0.01 |
| `answer` | W − 0.05 (2.15 to 2.85) |
| `miss` | W, the stated width (2.20 to 2.90) |
| Upper bound | W + 0.05, never reached, never settable as a right answer (it rounds up to the next width) |
| Tokens | `W` ("2.4"), `half` ("0.05"), `lb` (= answer, "2.35"), `ub` ("2.45"), `aTxt` ("2.35"), `mTxt` ("2.40") |

Solver for the generator’s uniqueness test: the real constraint, not a restatement. It asks which settings on
the grid round, half up, to W at 0.1 m, then takes the smallest:
`sols = [x for x in grid(2, 3, 0.01) if (round(x * 100) + 5) // 10 == W * 10]`, answer `min(sols)`.

**Checked, in a scratch run against today’s tools (nothing committed):**
- Every one of the eight variants passes the generator’s `keep()` rules: answer and miss on the grid and
  different, answer not printed in its own clue, answer clear of the slider’s ends. Each has exactly one
  smallest settable width that rounds to W: ten settings round to W, and the lowest is W − 0.05.
- `check-lock-bank.py` passes the bank entry below: `head-bay-lower-bound  ok  unique (2.35)`.
- Joint draws with the room’s two kept libraries, by `check-escape-rooms.py`’s own collision rules:
  **352 of 512 VALID, variant 0 VALID** (the floor is 20).

Proposed bank entry, for a new batch file in phase 2:

```
ID:          head-bay-lower-bound
LEVEL:       GCSE / Core
TOPIC:       Number / Error intervals (lower bound)
INSTRUMENT:  Bay-width slider, 2.00 to 3.00 m, 0.01 m steps.
CONTEXT:     The line marker re-marks a bay at whatever width it is set to, measured from the line next door. Its card says to re-mark at the smallest width the specification allows.
CLUE:        "Bay width 2.4 m, to the nearest ten centimetres." / "Re-mark to the smallest width the specification allows."
ANSWER:      2.35
AHA:         A width given to the nearest ten centimetres is a range, not a number; the smallest it can be is five centimetres below the stated width, and that width really does round to it.
MISCONCEPTION: 2.40 (the stated width, treated as exact).
SOLVE:       2.35 m <= width < 2.45 m, so the smallest width is 2.35 m.
TIME:        2
VERIFY_MIN:  [c / 100 for c in range(200, 301) if (c + 5) // 10 == 24]
```

The lower bound is attained (2.35 rounds half up to 2.4), so the lock asks for a width the bay can really have.
This is the standing rule from the hamster room: bounds locks ask for the minimum (working doc §5d).

### Lock 2: the barrier (kept: `boom-gate-sector`; framing only)

Unchanged: `id`, `key` (`gate`), `instrument` (dial, 0 to 180, step 5, label "Barrier swing angle", verb "Set
the angle"), `variants`, `missTitle`, `hints` and `solve`. Only the framing below changes.

- **name:** The barrier *(was "The boom gate")*
- **brief:** Mr Strictman has changed the barrier’s swing, so the arm comes down before a car is clear of it.
  The control box goes back to its proper setting only when it is given its calibration angle.
- **missTitle (unchanged):** {{gate.miss}}° is what you get from half the circumference.
- **missSays:** That is the angle you land on if the circle round the pivot is worked out as π × {{gate.r}}
  rather than 2 × π × {{gate.r}}. Halving the circumference doubles the angle you need to cover the same arc,
  and the control box won’t calibrate to it. *(Only the last clause changes; it used to say the arm was "well
  clear of the car".)*
- **hints and solve:** unchanged, word for word.
- **onOpen:** The arm lifts, settles and stays up. A car could go under it now and come out the other side with
  both wing mirrors.

### Lock 3: the charging post (kept: `ev-charger-quadratic`; framing only)

Unchanged: `id`, `key` (`amp`), `instrument` (dial, 0 to 15 A, step 1, label "Charging current", verb "Set the
current"), `variants`, `missTitle`, `hints` and `solve`.

- **name:** The charging post
- **brief:** The Head’s plug-in hybrid charges here, and Mr Strictman has set the post to trip the moment anything
  is plugged in. Take it back through commissioning: set a current that balances its load limiter and it goes
  back to normal. The circuit is also wired to the front office.
- **missTitle (unchanged):** {{amp.miss}} A balances the limiter and brings the office down here.
- **missSays:** Both {{amp.answer}} and {{amp.miss}} make the load zero, and the equation has no opinion about
  which one you use. The electrician’s note does: {{amp.miss}} is above {{amp.lim}} A, so that root resets the
  post and sets the alarm off at the same time. *(Only "unlocks the bay" became "resets the post".)*
- **hints and solve:** unchanged, word for word. Hint 1’s "the biro note by the post" still matches object 6.
- **onOpen:** The post clicks, thinks, and its light goes from red to a calm green. No alarm. When the Head plugs
  in, the dullest car in the county will charge in the dullest possible way.

---

## Picture alts (to be checked against what is filed, and rewritten to match, before release)

- **sceneAlt:** An underground staff car park under cold strip lighting, early morning, with concrete pillars and
  a wet floor. In a row of bays by the lift, one bay is plainly narrower than the rest, its new white line bright
  beside the faint ghost of the old one. A small hatchback with stick-on eyelashes on its headlights is parked in
  the wide bay beside it. A walk-behind line-marking machine stands by the fresh line. A charging post with its
  cover open is at the head of the narrow bay, a barrier arm is down at the foot of the entrance ramp, and at the
  far end of the row a measuring wheel leans against a bollard.
- **failAlt:** The same car park from the foot of the ramp. A plain, sensible grey hybrid car has stopped at the
  barrier, its arm down across the lane just in front of the bonnet. Beyond the arm the row of bays stands
  waiting, the narrow bay among them, and a clipboard rests on top of the barrier post.
- **winAlt:** The same row of bays. Every line is crisp and even. The grey hybrid is parked squarely in its bay,
  its charging cable plugged in and a small green light on the post. In the bay beside it, the eyelash hatchback
  sits across the new white line, half in one bay and half in the next. The barrier arm is up.

## Hub card line and meta description

- **Hub card:** The governors are coming, the deputy head has rigged the staff car park, and the Head is about to
  drive straight into all of it.
  Topics line: Bounds · Arc length · Quadratics
- **Meta description** (158 characters; the same string for `description` and `og:description`): A 15-minute
  GCSE and Core Maths escape room. The deputy head has rigged the car park before the governors arrive. Three
  locks: bounds, arc length, quadratics.

---

## Art prompts (canon §11.6; the format of `docs/escape-room-image-prompts.md`)

Paste the style block at the top of each prompt, then the prompt, then the negative. Generate all three, lay
them side by side, and file only once they read as one car park at one time of day (the kiln lesson). File every
image through `scripts/strip-gen-watermark.py --width 1600 --frame 1600x873`. Fail and win want the same camera
as each other: attach the filed scene as the reference for both.

**Style block (every prompt):**

> Hand-drawn cartoon illustration, visible ink linework with slightly uneven weight, flat colour fills with
> limited cel-shading, muted desaturated palette, single dominant light source, slight perspective distortion.
> British secondary school setting, contemporary, mundane and specific. Empty room, no people, no figures. No
> text, no signage, no numbers, no logos.

### `car-trap-scene`

An underground staff car park beneath a school, early morning, cold strip lighting, concrete pillars, a damp
floor with a few shallow puddles. A row of parking bays runs along one wall towards lift doors. One bay in the
middle of the row is plainly narrower than the bays either side: its new white line is fresh and bright, with
the faint ghost of an older line a little further over. In the wide bay beside it is a small, cheerful hatchback
in a pale colour, with large stick-on eyelashes on both headlights. A walk-behind line-marking machine with a
paint roller stands beside the fresh line. At the head of the narrow bay a charging post stands with its cover
hinged open and its cable coiled on a hook. A blank metal sign on a post marks the end of the narrow bay, with
a clipboard hanging from it. At the foot of the entrance ramp, with grey daylight beyond, a red and white
barrier arm is down. At the far end of the row a measuring wheel leans against a yellow bollard, as if just put
down.

**Negative:** photograph, photorealistic, 3D render, CGI, depth of field, bokeh, film grain, people, figures,
driver, text, lettering, numbers, number plate, badges, logos, brand marks, readable signs, year, sports car,
orange car, American signage.

**Zoom-check before filing:** the sign, the clipboard, the charging post’s display and both cars’ plates must be
blank.

### `car-trap-fail`

The same underground car park, seen from the foot of the entrance ramp looking along the row of bays, same cold
light. A plain, boxy, sensible grey hybrid car, the dullest car imaginable, has stopped at the barrier, the red
and white arm down across the lane just in front of its bonnet. Its headlights are on. Beyond the arm the row of
bays waits, the narrow bay among them, empty. A clipboard rests on top of the barrier’s control post.

**Negative:** as the scene, plus: damage, crash, broken barrier, smoke.

### `car-trap-win`

The same row of bays from the scene’s viewpoint, same light. Every bay line is crisp, even and freshly painted.
The plain grey hybrid car is parked squarely in its bay, its charging cable plugged in, a small green light on the
charging post. In the bay beside it, the small hatchback with stick-on eyelashes sits across the new white line,
half in one bay and half in the next. The barrier arm at the foot of the ramp is up. The line-marking machine is
parked neatly against the wall.

**Negative:** as the scene, plus: tyre marks, damage, crash.

*(The old prompt’s lesson stands: put the comedy in geometry the generator renders reliably. Here that is a car
straddling a line, not a facial expression or a folded mirror.)*

---

## Checklist: the voice contract and the room rules

Voice contract (`docs/escape-room-voice-contract.md`, fixed constraints) and its STOP IF:

| Rule | Result |
|---|---|
| Students are the heroes; the antagonist is the obstacle | **Pass.** They restore three machines to specification; Strictman is what they beat |
| Wrong-entry lines never mock the student or their answer, only the lock | **Pass.** Strictman never sees or addresses them; every line is about bays and standards |
| The antagonist loses graciously; no humiliation | **Pass.** He explains, then applies his own standard to himself: "My error. It will be corrected." Nobody laughs and nobody comments |
| Voice through the room setup, not a narrator layer | **Pass, with a note.** The hook and brief are narration, as in the reference room (`hamster-heist`); Strictman’s voice carries the wrong-entry slot and his lines in the win |
| "Idiot" and "stupid" never appear | **Pass** |
| British English | **Pass.** Car park, bonnet, caretaker, civvies, "eight sharp" |
| Name: real-sounding, no equipment puns, no innuendo | **Pass.** Strictman is your name for him and an aptronym, the house convention (working doc §5e: Beaker, Lunge, D Tension, Cinnamon). **For you:** I can’t check whether it maps onto a real, identifiable member of staff |
| STOP IF: inventing the character rather than drawing it out | **Did not fire.** Your brief gives his history, motive, method, voice, stakes, win and fail. Every extrapolation is marked **[X]** above |
| STOP IF: a change to puzzle logic or lock behaviour | **Did not fire.** Locks 2 and 3 keep every maths field; lock 1 is the new lock your contract specifies |

Room rules (working doc §3, §4, §8; canon §11.3):

| Rule | Result |
|---|---|
| One enforceable failure, able to reach the students during play | **Pass.** Strictman marches the row towards them (the clock); time-out is the barrier farce |
| A character who is not present cannot be the threat | **Pass.** Strictman is in the car park. The Head is the person the students protect, never the threat |
| Each character speaks only in their own room | **Pass.** The Head never speaks. "A statement of environmental leadership" is reported speech (see "For Jon" 6) |
| No third never-knew ending for the antagonist | **Pass.** Strictman sees his defeat. The Head never knows, as your brief says, but he is not the antagonist |
| If the students use the antagonist’s method, the brief says why it is different | **Pass.** Same machines, opposite direction. In the brief: "He set three machines against their own paperwork. You are setting each one back to it" |
| Students win by putting something right | **Pass.** Every setting restores the specification |
| No figure in the prose outside `{{tokens}}` | **Pass, with two exceptions in words, both flagged.** "Two point six centimetres" (your line, "For Jon" 3) and "ten centimetres"/"five centimetres" (lock 1’s constant precision, "For Jon" 4). "Fifteen minutes" and "eight sharp" are words, as in Prom Budget and Kiln. The method constants already in the kept lock text stay (the 2 in 2 × π × r in lock 2’s missSays, the squared x in lock 3’s label), as the comic room’s primes hint keeps its 1, 2, 3, 5, 7. No numeral is typed into any clue |
| No tokens in `hook`, `brief`, `stakes` (written raw by the engine) | **Pass.** None there |
| Never "Ofsted", in any form | **Pass** |
| No brand names; no year | **Pass.** "Plug-in hybrid", "hatchback"; the art negatives exclude badges, plates and logos |
| St Martha’s Secondary | **Pass.** The school isn’t named in this room’s prose, so nothing contradicts it |
| UK school timings | **Pass.** A morning, before the governors arrive; no clock time is stated |
| Eight objects, at least two blanks | **Pass.** Six clues, two blanks |
| Clue-carrying object `id`s unchanged | **Pass.** `spec`, `botcard`, `maintlog`, `sensor`, `commission`, `alarmnote` kept. `cone` and `trolley` are replaced by the new blanks `hatchback` and `sign`. Phase 2 rewrites `teacher.html` for the new lock 1 anyway |
| Each lock’s `brief` carries the new premise | **Pass.** All three rewritten; no "VIP bay", "visitor space" or "sports car" survives |
| Every lock has exactly one settable answer | **Pass.** Locks 2 and 3 are unchanged and verified. Lock 1 was checked in scratch (above) |
| A bounds lock asks for the minimum | **Pass** |
| No `missArt` | **Pass.** The fail picture shows the barrier down at the end of the clock, which is only true at time-out, so no lock may set `missArt` (the kiln and comic rule). Phase 2 records this in the `room.js` header |
| The pictures are of what the room is | **Pass.** Underground staff car park, the narrowed bay, the barrier, the wheel on a bollard, the eyelash hatchback; the old corridor-and-lockers scene (§7’s clash) is replaced |
| Meta description 150–160 characters | **Pass.** 158 |
| ★★ Core, grades 4–5 | **Pass, with a note.** Lock 1 is a one-step lower bound. Locks 2 and 3 are unchanged; whether they sit at ★★ is the existing bank’s grading, which this contract keeps |
