# Heatwave Mutiny: full breakdown for a sanity check

> ## CORRECTIONS FROM REVIEW, 13/09/2026 — these override everything below
>
> 1. **Premise.** Banks is no longer the trust's chief executive. He is a **facilities / energy
>    contractor**: a ridiculous individual, not a critique of a system. **No pay rise funded by the
>    cuts.** The radio interview, the reporter, the golf and the Student Supervisors all survive.
> 2. **Third lock.** The wire becomes a **disruptor emitting a signal in hertz**. Same inequality, same
>    prime condition, same dial range. The fiction needs one clear sentence on why only the exact match
>    shuts it down.
> 3. **Freezers dropped entirely.** A wrong frequency costs 45 seconds and nothing else. The
>    misconception keeps its named response (with the canteen wording removed). The freezer picture is
>    **not filed** and has been deleted.
>
> 4. **Motive and ending (Jon, 13/09).** The school is on a **fixed-price energy contract**: it pays the
>    same whatever it uses, so the energy company makes less money when the air conditioning runs.
>    Banks disabled it to protect the margin, and **his bonus depends on it**. He gains if the students
>    lose and loses out if they win. **Same ending shape:** he finds out from his **end-of-month report**,
>    and his bonus takes the hit. "Five times the bill" becomes "five times the usage his bonus was
>    worked out on", because the school's bill doesn't change on a fixed contract.
>
> **ENGINE WORK CANCELLED, NOT DEFERRED.** Both options in section 8 — (a) per-lock misconception
> pictures and (b) three-strikes second ending — are cancelled. Neither is an outstanding job. Do not
> queue either.

**Prepared 13/09/2026, before anything is built.** Nothing in `room.js`, `index.html`, `teacher.html` or
`engine.js` has been touched. The only changes on disk are four pictures filed to `docs/art/` (uncommitted).

**To the reviewer.** You are reading this cold, and that is the point. Please check it against the
standing rules in section 2 and tell us what is wrong, weak or contradictory. Do not rewrite the room in
your own voice. The whole project exists because a teacher said the text read as if no human wrote it,
so the character and the premise have to stay Jon's. Point at problems; don't replace his answers with yours.
Section 9 lists the specific questions we most want answered.

---

## 1. Context

**MaffsGames** (maffsgames.co.uk) is a free maths games site for UK secondary schools. It has a set of
eight **narrative maths escape rooms**, each **under 15 minutes**, played by small groups on one screen
at the end of a lesson. Each room has **three locks**. Each lock is a real maths problem, and the
difficulty comes from not knowing which of eight searchable objects belongs to which lock (six carry
clues, two are blank). Numbers are drawn per play from a verified library, so no figure is ever written
into the prose; everything is a `{{key.token}}` filled at run time.

**Why this rewrite exists.** On 08/09/2026 a teacher wrote in to say that every room was obviously
AI-generated, the prose had no author behind it, and "as it stands, none of this is usable". Jon
accepted it. The maths was sound; the voice wasn't there. All eight rooms are being rewritten one per
session around a **named antagonist drawn out of Jon by interview** (never invented for him), with new
hand-inked art. Rooms 1–4 are done and live. **This is room 5, The Heatwave Mutiny.** It is currently
withdrawn behind a noindex holding page.

**How a room is built:** read the room → interview Jon → character sheet → draft text in chat → Jon
reviews → write `room.js` → checker → play it in a browser → art → release.

## 2. Standing rules the room must meet

1. The students are always the heroes. They win by **putting something right**, not by stealing,
   deceiving or breaking things for their own sake.
2. **One enforceable failure** per room, and it must be able to reach the students **during play**.
3. **A character who isn't present cannot be the threat.** They can be the standard, or the cause.
4. Wrong-entry lines never mock the student or their answer, only the lock.
5. The antagonist **loses graciously, with no humiliation**. "Idiot" and "stupid" never appear.
6. British English. No year anywhere. **No brand names.** The school is **St Martha's Secondary**. UK
   schools finish at **3:30**, so timings must sit sensibly around the school day.
7. **Characters recur offstage but speak in only one room.** Voices already used: Mr Beaker (science),
   Test Tube Dave, Mr Barry Lunge "Lungey" (P.E.), Mr D Tension (headteacher), Ms Cinnamon (food tech).
8. **No third "the adult never finds out" ending.** Two of the four finished rooms already end that way.
9. **If the students use the antagonist's own method, the brief must say why it's different.**
   "Nobody noticed" is getting away with it, not being different.
10. Names: real-sounding, no innuendo, must not map onto a real identifiable person. The set's house
    style is an aptronym (Beaker in science, Lunge in P.E.).
11. **Hardcoded numbers in prose must never contradict a drawn variant.**
12. Maths, lock mechanics, variant libraries, answer checking, and the teacher page are **do-not-touch**
    unless explicitly agreed. Object `id`s must never change (the teacher page maps clues by them).
13. Art: hand-drawn cartoon, visible uneven ink linework, flat muted colour, **empty rooms, no people,
    no lettering, no logos**. Three pictures per room: scene, failure, victory.

## 3. The room as it currently exists (the version being replaced)

A 32°C heatwave; "the board" has switched the school air conditioning off to save money. Students sneak
down a corridor patrolled by prefects, open a keypad door into a control room, and pull the right wire
out of an override panel. Wrong wire → the failsafe cuts the canteen freezers instead. Win → air con back
on, and the board notices the bill in six weeks.

### The three locks (maths unchanged in the rewrite)

| Lock | Maths | Instrument | Named misconception (costs 45s, gets a specific response) |
|---|---|---|---|
| **Patrol window** | LCM of three lap times via prime factorisation. 5 variants: (12,15,18)→180, (7,16,28)→112, (6,14,18)→126, (5,7,20)→140, (7,11,14)→154 | Slider 1–200, "minutes after 12:00" | Adding the three lap times |
| **Security door** | Cube: total surface area → ÷6 → √ → cube it = volume = 4-digit code. 10 variants, edges 10–21 (1000–9261) | 4-digit keypad | Stopping at SA÷6 (one face) |
| **The wire nest** | Double inequality `lo < mf − k < hi` over integers leaves 3–5 whole numbers; a separate clue says the wire is **prime**, which leaves exactly one. 6 variants | Dial 0–50 Hz | Taking the largest candidate and ignoring the prime condition |

**Maths verified by hand on 13/09:** every inequality variant leaves exactly one prime; every
misconception value is the largest candidate; every LCM and cube is correct.

### Faults found in the read

- **The students win by breaking in and ripping out a wire.** That's sabotage, not putting something right.
- **Most UK secondary classrooms have no air conditioning**, and a teacher would notice.
- **Nobody is behind it.** "The board" is absent and faceless.
- **Timing fault in the LCM lock.** The clock reads 12:00 and the corridor clears 112–180 minutes later
  (13:52–15:00), inside a 15-minute room. The answer range spans 68 minutes, so no single fixed start
  time in the prose can place the moment inside the play window.
- "Cornetto" is a brand name.
- "Wire frequency in hertz" is physically nonsense.
- The old ending was close to "never finds out".
- **Teacher page bug:** it says "four candidate frequencies", but the variants give 3, 4 or 5.

## 4. What Jon decided in interview (his words, lightly tidied)

- **Antagonist: Mr Robin Banks**, chief executive of the trust that runs the school. His board is "all
  about saving money, to hell with the students and staff". The savings fund his **inflation-busting
  pay rise**.
- **He is not in the building.**
- **The school genuinely has air conditioning, covering the whole school.** The students turn it back on.
- **Win:** they get away with it until the **end of the month**, when the accounts come in, the
  electricity bill is **five times** what was expected, and the board has to **cancel the pay rises**.
  "It's not an immediate pay-off, but it works."
- **His voice is delivered through a local radio interview**, in which he justifies his salary and explains
  why TAs are "so 20th century".
- **The interviewer** is an incredulous reporter who **doorstepped him leaving the golf course after 36
  holes** instead of doing his job. She is gobsmacked that a chief executive would be this openly honest
  about how little he cares.
- **Everyone is sweltering except the Student Supervisors**, pupil monitors who each have a **little fan
  on their uniform**.
- **He doesn't understand the maths.** He understands very little except that his salary should be
  higher for the minimal work he does.
- **Failure is two-fold:** run out of time → endure the heat for the whole heatwave. Wrong wire → the
  freezer ending.
- **Jon's sample of Banks, verbatim:**
  > "In our trust, we are developing the next generation of worker, they need to be able to work in these
  > conditions, global warming, which I don't think is real, means the temperatures are going to be much
  > lovelier in the future, these are the kind of insights that show why I'm underpaid for the
  > extra-ordinary leadership and vision I provide"
- **Three things he would never say:** "Our students deserve…" / "Of course TAs are important" / "Our
  staff work hard"

### One of Jon's ideas that was declined

Jon wanted the Student Supervisors known as **"the SS"**, with an **SS logo** on their uniforms. Claude
declined to put it in. To most adults it reads as the Nazi SS, a logo makes that deliberate, a teacher
couldn't project it to a Year 9 class, and the art rules forbid logos anyway. Jon hasn't replied on this
point. **Reviewer: tell us if you think that call was wrong.**

### Name check

"Robin Banks" is an obvious "robbing banks" pun, in line with the set's aptronym convention. A web search on
13/09 found no UK academy trust chief executive or trustee of that name. The only hits were US
individuals with no UK education connection.

## 5. Character sheet: Mr Robin Banks

Unmarked lines come from Jon. **[C]** marks Claude's reading or extrapolation, which Jon may strike.

- **Role:** chief executive of the trust. Not in the building; heard on the radio.
- **What he's done:** switched off the air conditioning in every school in the trust mid-heatwave, and cut
  teaching assistants. The savings fund his above-inflation pay rise.
- **Justification:** toughening up "the next generation of worker". Global warming isn't real, *and* it will
  make temperatures lovelier.
- **Maths:** doesn't understand it. Understands only his salary.
- **Enforcers:** the Student Supervisors, the only cool people in the school, each with a clip-on fan.
- **How he loses:** month-end accounts, bill five times the budget, pay rises cancelled. He sees his
  defeat, a month late.
- **Voice:**
  - Management language for plain hardship ("next generation of worker", "insights", "leadership and vision").
  - Contradicts himself within a sentence and doesn't notice.
  - Every answer returns to his pay.
  - **[C]** Long sentences strung together with commas; no gap for the interviewer.
  - **[C]** "Worker", singular, never "people". He's talking about a resource.
  - **[C]** He sincerely believes he's underpaid. He isn't a cynic; in his own head he's the wronged party.
  - **[C]** The centre of the character: he can't manage even the platitudes every real trust leader says
    automatically. It has never occurred to him to say them.
- **Would never say:** "Our students deserve…" / "Of course TAs are important" / "Our staff work hard"

## 6. Assumptions Claude made that Jon hasn't confirmed

1. **The room happens before school.** The chairs are still up (they are in all three classroom
   pictures), the teacher's jacket is on the chair because they're at morning briefing, the bell is the
   15-minute clock, and the radio breakfast show is **replaying** yesterday evening's doorstep clip. That
   is also why the last wrong-entry line repeats: they restart the clip.
2. **The freezer failure is a mid-game consequence, not a second game-over.** See section 8.
3. **The locks were fitted by the trust's contractor.** Estates were told not to give out the door code,
   so they left a puzzle instead.
4. **LCM timing is fixed by wording, not numbers.** Remove "12:00". The timer counts "minutes after they set
   off", and no text says what time they set off or what time it is now. **Honest caveat: this hides the
   fault rather than fixing it.** A reader who asks "set off when?" still gets a patrol that began 2–3
   hours before 8:20 am. The real fix is regenerating the variants with shorter lap times, which is a maths
   change and needs Jon's sign-off.
5. Changing **three protected text strings** on the patrol lock (numbers untouched): the instrument label
   ("minutes after 12:00" → "minutes after they set off"), the misconception title ("full of prefects" →
   "full of Supervisors"), and hint 1 ("prefects" → "Supervisors"). The hints still say the patrol returns
   to the **staffroom**, and that is kept to avoid touching more protected text. Pupils based in a staffroom
   is slightly odd.

## 7. Draft text (not yet in any file)

**hook**
> Thirty-two degrees at twenty past eight, and the air conditioning in every school in the trust has been
> off since Monday. The chairs are still up on the desks. On the radio, the breakfast show is playing a clip
> from yesterday evening: a reporter who caught the chief executive of the trust, Mr Robin Banks, in a golf
> club car park after thirty-six holes, and asked him about it. He told her. The only cool people in the
> building are the Student Supervisors, each with a small fan clipped to their uniform, and they are
> patrolling the corridor to the control room.

**brief**
> Fifteen minutes before the bell. Get past the patrol, through the control-room door, and take out the
> cut-off the trust had fitted into the air conditioning over the summer. You are not switching on anything
> the school does not already own. You are taking out the one wire somebody put in to stop it.

*The last two sentences exist to satisfy rule 9 (why this isn't sabotage).*

**stakes** (shown only on running out of time)
> Miss the bell and the air conditioning stays off for as long as the heatwave lasts: every lesson, every
> day, thirty-two degrees and climbing. The Student Supervisors will be fine.

**win**
> Under the floor the compressors shudder and start, and then every room in the building starts with them.
> Nobody has even taken the chairs down yet, and the air is already cold enough to notice. Nobody at the
> trust notices anything, because nobody at the trust is ever in the building. They notice at the end of
> the month, when the accounts come in and the electricity bill is five times what was budgeted, and the
> board cancels this year's pay rises to cover it, his included. Mr Banks has described this to the board
> as a development opportunity.

*(The chairs line was changed from "the chairs are down" to match the pictures.)*

### wrongLines: one step of the radio clip per wrong entry; line 4 repeats for the rest of the game

1. **The lock stays exactly where it is.** A car park, and a golf bag going into a boot. "Mr Banks, every
   school in your trust is at thirty-two degrees." "Which is precisely the point, we are developing the
   next generation of worker, and the next generation of worker is going to have to work in the heat, so
   really the heat is part of the curriculum." She asks him to say that again. He does.
2. **Something clicks and thinks better of it.** "You cut the teaching assistants in September."
   "Teaching assistants are a very twentieth-century solution, and I say that as somebody with a great
   deal of vision, which I would argue is not properly rewarded." There is a pause while she works out
   whether he meant to say that.
3. **The panel resets with a clunk.** "Have you really just played thirty-six holes?" "Thirty-six holes is
   a great deal of thinking time, and I would say global warming, which in my view is not real, is going to
   make the weather a lot lovelier, and those are the kind of insights that do not show up on a payslip."
   She says "Sorry, what?" on air.
4. **The lock gives nothing back at all.** "Is there anything you would like to say to the staff at St
   Martha's?" A long pause. The boot shuts. "I would say that I am underpaid for the extraordinary
   leadership and vision I provide." The breakfast show has gone back to the start of the clip.

*Line 4 is designed so she sets up "our staff work hard" and he misses it. Engine note: a misconception hit
uses up a line index without printing it, so a player may skip a line; the lines don't depend on each other.*

### Locks: brief, and text when opened

| Lock | brief | onOpen |
|---|---|---|
| Patrol window | A countdown timer wired into the corridor door release. Set it to the number of minutes after the Supervisors set off when it is safe to cross, and it will let you through at that moment and no other. | At that many minutes after they set off, all three Student Supervisors are back in the staffroom at once, comparing fans. The corridor is empty for about ninety seconds. You use forty of them. |
| Security door | A four-digit keypad on the control-room door. The trust told Estates not to give the code to anyone. Estates left a note instead. | Four worn buttons, one flat clack each, and the bolt goes back. The air conditioning panel inside is in perfect working order. There is nothing wrong with it except that it is off. |
| The wire nest | Behind the panel: forty-odd coloured wires, each humming at its own frequency, and one of them is the trust's cut-off. The tuner isolates one wire. Choose it by its frequency in hertz. | One wire comes out of the block with a click you feel more than hear, and somewhere under the floor a compressor coughs into life. |

**Unchanged and protected:** wire-nest misconception text reads "…and the failsafe has just found the canteen."

### Objects (ids unchanged)

| id | Name / where | Text |
|---|---|---|
| `rota` | Student Supervisors' rota, pinned inside the store cupboard | **CORRIDOR PATROL — Student Supervisors.** Supervisor A: one lap every {{lcm.a}} minutes. B: every {{lcm.b}}. C: every {{lcm.c}}. All three set off together from the staffroom. |
| `clock` | Wall clock, above the door, note taped to the glass | The clock stopped at some point in the night, which in this heat is fair enough. The note: "Corridor is only clear when all three Supervisors are back in the staffroom *at the same time*. Not before." |
| `sticky` | Sticky note, under a desk | "The trust has told me not to give this code to anyone, and I have not. The code is what the coolant tank *holds*, in cubic centimetres." — Estates |
| `label` | Maintenance label | Unchanged: COOLANT TANK. A perfect cube. Total surface area {{cube.SA}} cm². Do not overfill. Do not repaint. |
| `manual` | Wiring manual | "Cut-off module, isolation procedure": the inequality, unchanged |
| `memo` | Crumpled memo, in the bin | "…and for the last time, the cut-off only comes out on a **prime** frequency. Anything else trips the failsafe onto the canteen freezers, because that was the cheapest circuit to wire it into. I will not be explaining that to the kitchen again." |
| `fan` (blank) | Desk fan, on the teacher's desk | Unplugged. Taped to the plug is a note from the trust setting out what a desk fan costs to run for a year, and the sum is wrong. |
| `thermo` (blank) | Jacket, over the teacher's chair | Your teacher's, left there on the way to the morning briefing. Nobody has needed a jacket in this building since Monday. |

## 8. Art and engine

**Four pictures generated and filed (1600×873 WebP, no watermark, no lettering, checked at zoom):**

| File | Alt text (written from what is drawn) |
|---|---|
| `heatwave-mutiny-scene.webp` | An empty secondary school classroom before the day starts, the chairs still upside down on the desks. Hard white sunlight pours through half-open blinds, one hanging crooked, and lays bright stripes across the floor. Two air-conditioning units sit high on the wall, silent. A desk fan stands on the teacher's desk, a dark jacket hangs over the teacher's chair, and a plastic water bottle lies on its side on a desk by the window. |
| `heatwave-mutiny-fail.webp` | The same classroom at the end of another day of the heatwave. The air-conditioning units are still shut, the light through the blinds has turned a heavy orange, and the room is hazy with heat. Empty water bottles lie among exercise books left open, a crumpled worksheet sits abandoned, the desk fan is still unplugged with its lead trailing to the floor, and a plant on the windowsill has wilted flat. |
| `heatwave-mutiny-win.webp` | The same classroom a few minutes before the bell, gone cool and blue. Both air-conditioning units are running, pale streams of cold air curling out across the room, while the sun outside is still a hot yellow-white. A water bottle is beaded with condensation, the jacket still hangs over the teacher's chair, and the chairs are still up on the desks. |
| `heatwave-mutiny-freezer.webp` (new) | The back of the school canteen kitchen, hot sunlight through a high window. Three white chest freezers stand dead with their lids open, water dripping from the rims, and a wide puddle of melted pink, vanilla and chocolate ice cream spreads across the tiles around soggy cones, lolly sticks and a tipped-over tub. Above them an electrical box hangs open with a wire pulled loose. |

**Known picture issues:**
- The freezer picture's electrical box cover carries a **small hazard pictogram with a stick figure**,
  which breaks the no-signage rule. It could be inpainted flat.
- The left air-con unit slightly overlaps the projector-screen casing. Minor.

**Engine limits (verified in `engine.js`):**
- Only running out of time ends a game badly. A wrong answer never ends the game; it costs 45 seconds.
- There is no per-lock wrong counter.
- A room has **one** failure picture, used both on the timeout screen and as the thumbnail shown on a lock's
  named misconception.

**Options for the two-fold failure:**
- **(a) Recommended.** Timeout = heatwave ending. The wire-nest misconception shows the **freezer** picture
  mid-game and play continues. Needs a ~4-line engine change so a lock can name its own misconception
  picture. No saved-game version bump; other rooms unaffected.
- **(b)** Jon's literal "three wrong wires = freezer ending". Needs a per-lock counter (a saved-game version
  bump that wipes in-progress games), a second end state, a second stakes string and a second failure
  screen. That's a shared-engine job, to be done under its own contract before this room.

**Narrative tension in (a):** once the freezers have gone, the game carries on and the players can still
win. The win text never mentions the freezers. Is that a contradiction a player would notice?

## 9. What we most want the reviewer to check

1. **Rule 1 and rule 9.** Does "you are taking out the one wire somebody put in to stop it" genuinely make
   the students heroes putting something right? Or is it still a break-in plus sabotage with a
   justification bolted on?
2. **Rule 2 and rule 3.** Banks is absent, so the in-play threat is the Supervisors' patrol plus the clock
   plus the freezer trap. Is that enough, or does the room have no real opponent on the day?
3. **Rule 8.** The win ends with the board finding out a month later. Does that count as the antagonist
   seeing his defeat, or is it an off-stage epilogue, a disguised "never finds out"?
4. **Rule 5.** Is "Mr Banks has described this to the board as a development opportunity" a gracious loss
   or a humiliation?
5. **Classroom suitability.** The satire targets trust leader pay (a live, real controversy in UK
   education) and includes climate denial from the villain. Could a teacher at a real academy trust
   reasonably refuse to run this? Is anything here a real political-impartiality problem for a school, or
   is it clearly character comedy?
6. **Realism a UK teacher would catch:** a whole-school air-conditioning system; pupils patrolling out of
   a staffroom; a patrol that must have set off hours before 8:20 am (assumption 4); wires "in hertz";
   "five times the bill".
7. **Electrical safety optics.** The students remove a wire from a panel, and the freezer picture shows a
   loose wire. Is that a problem in a resource for 12–14-year-olds?
8. **Voice.** Read the four wrongLines. Does Banks sound like one specific person, distinct from a pompous
   headteacher (Tension) or a gruff P.E. teacher (Lungey)? Do the reporter's lines carry "incredulous"
   without narration doing the work?
9. **The SS decision** (section 4). Right call?
10. **Anything contradictory** between hook, brief, stakes, win, objects, lock text and pictures:
    time of day, chairs, jacket, radio, the staffroom, the freezers.
11. **Hardcoded numbers:** "thirty-two degrees", "thirty-six holes", "five times", "forty-odd wires",
    "ninety seconds / forty of them". Do any collide with a drawn variant? (We believe not; the
    frequency dial runs 0–50 and the answers run 7–37.)
