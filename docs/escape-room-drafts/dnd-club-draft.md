# The D&D Club: draft for Jon’s review

**Phase 1 of the D&D Club room (contract DND-ROOM-DRAFT, 15 Oct 2026).** Draft prose only. There is no
`escape-rooms/` directory for this room yet, and nothing served is touched. Phase 2 (the build, the variants,
the art filing and the release) is a separate contract after you approve this.

The idea is Mrs Rogers’s, who has agreed to her real name being used (Jon, 15 Oct 2026). The room is built
under the house process: `docs/escape-room-voice-rewrite.md`, canon §11 and the format of
`docs/escape-room-drafts/car-trap-draft.md`.

How to read it:

- `{{key.token}}` is a figure filled from the drawn variant. There are no other figures in the prose; the
  exceptions are listed in the checklist at the end.
- Prose is shown with real quotation marks and apostrophes. In phase 2 they become entities in every slot
  except the object and lock `name` and `where`, which keep real characters (canon §11.3).
- **[X]** marks a detail I extrapolated rather than took from your brief. Strike any you don’t want.
- **Mrs Rogers speaks only the lines she approved, word for word.** Every other thing she does is narrated, never
  quoted. The students’ lines are the ones in your brief; no student has a name.
- Three token keys: `gate` (lock 1), `plan` (lock 2), `fb` (lock 3).

---

## For Jon: decisions in this draft

**Items 1 and 16 were ruled on by Jon on 15 Oct 2026 (below); the draft now follows both rulings.**

1. **RULED (Jon, 15 Oct 2026): Strictmane’s defeat is gracious, in character.** The question was “he flees when
   beaten” against the voice contract’s *“The antagonist loses graciously at the escape. No humiliation.”* Jon’s
   ruling: *“keep the defeat, lose the scurrying, and let his own bureaucracy carry the comedy.”* So lock 3’s open
   keeps the panic as the fireball lands (“Formation! FORMATION! …Who authorised the fire?”, panic and not
   humiliation) and then he straightens his starched robes and withdraws in his own register: “A tactical
   withdrawal. I shall be submitting Form R-1, requesting a rematch.” A pause. “In triplicate.” It echoes the
   goblin’s Form G-14 as a running joke. The word “flees”, the creased robes and the scattering Strictmane are gone;
   the goblins still scatter. The left-behind re-match form I had proposed for the win is removed (the line now
   lives in lock 3’s open). Jon’s reason, for the record: Strictmane is a stand-in for a teacher, and a humiliated
   antagonist turns the room mean.
2. **Stars.** Your brief says ★★ and “GCSE Foundation (grades 1–3)”. Canon §11.3 derives the stars from the
   hardest lock’s `grade` field: ★★ Core is a hardest lock at grade 4–5, ★ Warm-up is grades 1–3. These do not
   conflict: “grades 1–3” is who the room is for (the audience line the Essentials page uses), the `grade`
   is the grade at which each skill is typically secure. **Proposed lock grades: gate 4, plans 3, fireball 4,
   so the derived rating is ★★ Core** and matches your call. I have added no star field and written no card
   markup; `grade` is the per-lock field every new room carries and is set in phase 2. Recorded in the
   handover for the difficulty contract.
3. **Numbers in words that your brief gave as numerals.**
   - *“This corridor is 2.6 cm narrower than the plans…”* is Strictmane’s line, so it stays, with the number in
     words (“two point six centimetres”), the Car Trap precedent (its “For Jon” 3).
   - **“Form G-14, in triplicate”** is kept as written, in the wrong-entry line and the first lock’s open (and
     Jon’s “Form R-1” in the third lock’s open), but **not in any clue** (a numeral in a clue is a clue figure, and 14 is variant 0’s persuasion DC). If you’d
     rather there were no coincidence at all, change the form number; it’s a flavour string.
   - **“nat 20”** is written `nat {{gate.die}}` (the die’s faces, a token that is 20 in every variant), so
     the page still says “nat 20” and no bare numeral is typed.
   - Your lock 3 note “(3 squares)” is kept out of the **clue** (the clue gives the radius in metres) and carried in
     `solve` as `{{fb.rsq}}`: with the squares in the clue, variant 0’s Charisma +3 and the 3 squares collide
     (rule a) and variant 0 is an INVALID draw. The square is fixed at 2 m, so the number is always r ÷ 2.
   - Your lock 2 hint 3, “Twenty what?”, becomes `{{plan.real}} what?`, which prints “20 what?” in variant 0.
     Your wording, with the figure as a token.
4. **There is no `fail` slot in `room.js`.** The engine shows `stakes` after “If you get it wrong.” on the start
   screen and after “And so:” on the time-out screen, so your fail is written into `stakes` and reads
   correctly after both (Car Trap “For Jon” 1). **The fail is the club ending**: the caretaker puts the chairs
   up, rolls the mat, boxes the goblins; she goes home without saying “next week”. That matches the fail
   picture you generated (chairs upturned on the tables, mat rolled, everything in tubs).
5. **The pressure that can reach the students** (the §3 rule, “One enforceable failure per room”) is the clock.
   Like the kiln, the club’s end time is a countdown that reaches students more reliably than any character,
   and the fail picture is exactly what it ends in. Strictmane is the BBEG of the adventure the students are
   running and speaks in the wrong-entry lines. He is present in the fiction, so “a character who is not
   present cannot be the threat” doesn’t apply.
6. **Wrong-answer feedback never gives the answer.** `missTitle` and `missSays` name the wrong figure and
   nudge; hint 3 on every lock stops one step short. The worked `solve` appears only on a solved lock’s panel
   and the end screen (`engine.js` lines 416 and 827) and on the teacher page. It is never shown for a wrong
   entry. (Some older rooms’ hint 3 spells out the answer; none here does.)
7. **Her lock-1 line is a variant constraint.** “Hang on, so the lower number isn’t the better bet?” is only true
   if the path with the lower DC is the worse bet. That is a constraint on every set (“Lock 1” below), so her line
   is true in every variant; in all nine sets the better path is persuasion, so the nat 20 on persuasion is
   always right. See 16 for what it costs.
8. **Where the explanations of the D&D terms are [X].** Each term is explained the first time it appears, in
   the narration or a clue, never in Mrs Rogers’s mouth (so she says nothing you haven’t approved):
   DM (hook), BBEG and roll for initiative (brief), species, Strength (Athletics) and Charisma (Persuasion)
   (her character sheet), DC (the DM screen), nat 20 (lock 1’s open), AoE (the fireball card).
9. **Where the approved lines sit.** Start: the end of the hook. Lock 1 opens: lock 1’s `onOpen`. Lock 2
   (Mr Strictman): lock 2’s `onOpen`. Ending and character choice: the win, in the order your brief lists them
   (the “wizard” exchange, then “barbarian” and the dwarf wizard). She asks for a wizard before she “chooses her
   own character”; if you’d rather the choice came first, the two blocks swap.
10. **Mr Strictman is a cameo, not a speaker.** She recognises him at lock 2. Strictmane (with an e) is the
    BBEG; both are invented and map to no real person (your brief). Mr Strictman says nothing in this room,
    keeping the “each character speaks only in their own room” rule.
11. **Trademark.** “D&D” is used in the title option and prose as the club’s name; there are no logos, no
    named creatures and no named characters: goblins, a fireball, a dwarf and a wizard only. “DM” is used
    throughout and the longer phrase never appears.
12. **No student is named anywhere**, in the room or in this document.
13. **The credit line** is in “Credit” below; consent is recorded in the handover.
14. **Objects.** Six clues and two blanks (the tea mug and the blank sign, as you suggested). The scene shows
    the DM screen as a cardboard folding screen at the far side of the table and the pinboard blank on the
    brick wall, so those are what the objects are.
15. **Statements the engine can’t make (checked, none fires).** All three answers are whole numbers on a
    keypad. A percentage is expressible (The Rightful King’s “percent of those who saw it” is a keypad).
    Every lock has exactly one settable answer.

16. **RULED (Jon, 15 Oct 2026): accept the nine-set pot; the “half climb-better” constraint is withdrawn.**
    The pot could not do all three things at once, and I had not changed Mrs Rogers’s line to make it. Your pot spec asks for (a) roughly half the sets with the climb as the better path, (b) a
    forgotten penalty that makes the **worse** path look better, and (c) (from your brief) her approved line,
    which needs the lower-DC path to be the worse bet.
    - **(a) and (b) cannot both hold.** The drizzle penalty applies to the climb only, so forgetting it can only
      make the climb look better. When the climb is already the better path, forgetting the penalty makes the
      better path look better still: a wrong number, not a wrong path. **0 of the 6 such sets flips the path;
      158 of the 323 persuade-better sets do.**
    - **(a) and (c) nearly cannot both hold either.** Climb-better sets that keep her line true need the climb to
      have the *higher* DC and still be the better path, which only six sets in the whole space do, all one shape
      (Strength +4, drizzle −1, persuasion +1, a one-point DC gap). Without her line there are 554 climb-better sets.
    - **What I built:** a pot where persuasion is the better path in all nine sets, the forgotten penalty flips
      the path in every one, and her line is true in every one. It breaks only “roughly half climbing”, and is
      limited to **nine** sets (the flipping sets have only nine distinct answers).
    - **The ruling.** Jon: *“The constraint was wrong; the pot is right. Replayability doesn’t suffer much: a student
      who learns ‘it’s always persuade’ still has to work out the percentage, and that changes across all nine
      sets. The code is the maths, not the choice.”* Option (i), as built: persuasion is the better path in every
      set, the forgotten penalty flips the path in every set, and her approved line is true in every set. No
      alternative line for Mrs Rogers is needed. He also accepted seven plan sets and five fireball sets as within
      the house range, and 182 valid joint combinations as plenty of replay; the widenings listed under locks 2
      and 3 are therefore not taken.
---

## Title

Propose three **[X]**; mark the one you want:

- [ ] **Roll for Initiative** *(the phrase every table says first; a nice irony, since the first thing she
  learns is that the lower number isn’t the better bet)*
- [ ] **The Commandant’s Fortress**
- [ ] **The D&D Club**

*(The slug is phase 2’s business. Whichever you pick, the hub and card strings come from it.)*

## Hook

Mrs Rogers runs the school D&D club. It exists because you asked her to start it. She has never played.
She has watched you do it for weeks, nodded politely at the dice, and marked a great deal of homework at the end
of the table.

Tonight you are the DMs. You explain to her that a DM is the player who runs the game: you describe the
world, you play everybody in it, and you teach the rules to anyone who needs them. She is the new player. You’ve
built her a short adventure, and because making a character from nothing is a lot to ask on a first night, you
have handed her a ready-made one: an adventurer with golden curls, in battered blue plate armour, engraved all
over.

She sits down with a mug of tea and a pile of marking, picks up a twenty-sided die and turns it over.

“Right. I’ve got my tea, I’ve got my marking, and I’ve got… a twenty-sided dice. Remind me why there are twenty
sides?”

## Brief

Every adventure needs a villain. You tell her that the one in charge, the big bad evil guy, is called the BBEG,
and yours is Commandant Strictmane: a tyrant in starched robes who has built a fortress and measured every inch of
it. He has put three obstacles between her adventurer and the end of the story, and none of them is a monster.
Each one is a rule, and each one is a number she has to be shown how to find.

When you get one right, she will start to want the next. That is what you are here for. The club ends when the
caretaker comes round to stack the chairs, and every wrong setting costs you time.

When the three obstacles are down, there is a last piece of ceremony: you tell her to roll for initiative, which
is how a game decides who goes first, and the fight starts. *(Phase 2: the engine’s end screen carries this;
it is a sentence in the win, not a mechanic.)*

## Stakes (also the fail screen; see “For Jon” 4)

The caretaker puts the chairs up on the tables, rolls up the mat and boxes the goblins. Mrs Rogers finishes her
tea, gathers her marking and says, kindly, that it was lovely to try something new. She does not say next week.
The club goes back to being something she watches from the end of the table.

*(Read after “If you get it wrong.” on the start screen and after “And so:” on the time-out screen; both
work. No numbers, no names.)*

## Win

The last goblin helmet stops smouldering. Mrs Rogers looks at the mat, at the scorch mark, at the goblins lying
every which way, and then at you, as if she has only just noticed that the room is full of people who know exactly
what they’re doing.

“Same time next week? I want to be a wizard. One that throws fireballs.”

“You can’t cast fireball until fifth level, Miss.”

“Then I suppose we’d better play every week.”

She slides the golden-curled adventurer in its battered blue armour to the edge of the mat and picks up a blank
character sheet.

“Miss, you’d definitely be a barbarian.”

“Everyone keeps telling me what I’d be. Dwarf. Wizard. Final answer.” She writes it in the species box, and
then, after a beat: “Don’t tell my husband he was right.”

---

## wrongLines (four, escalating; the last repeats)

Each `head` is the room’s reaction; each `body` is Strictmane, gloating about the lock, from somewhere beyond
it. Every line is about the fortress and the forms. None mentions the students.

1. **head:** The setting clears with a clunk that echoes down a stone corridor.
   **body:** Beyond the lock, the scratch of a pen on a plan. “This corridor is two point six centimetres
   narrower than the plans. This is not how it is done in MY fortress.”
2. **head:** Nothing opens. The goblin on the gate stamps a form, very slowly, and slides it back across the
   table.
   **body:** “Form G-14 is incomplete. Form G-14 is always incomplete. That is rather the point of Form G-14.”
3. **head:** The setting slides back to where it was.
   **body:** “Every gate in this fortress is inspected at dawn. Every lock is measured twice. No intruder has
   ever got through all three. I have the paperwork to prove it.”
4. **head:** Another one. The pen is nearer than it was.
   **body:** “Next form.”

*(Line 4 repeating is the joke, as “Next bay.” was in Car Trap: he just keeps coming. Line 1 is your line, with
the number in words. Line 2’s G-14 is the form’s name, not a clue; see “For Jon” 3.)*

---

## Objects (eight: six clues, two blanks)

Clue objects get the ids below; `teacher.html` maps clues to locks by `id` and phase 2 writes that map from
this table. The two blanks are `mug` and `sign`.

| # | id | name | where | clue or flavour |
|---|---|---|---|---|
| 1 | `charsheet` | Her character sheet | at her place at the table | **ADVENTURER.** Species: human *(her species is what kind of person she is: human, dwarf, elf; it’s the first box on every sheet)*. Golden curls, battered blue plate armour, engraved. **Strength (Athletics): +{{gate.str}}** *(Strength is how strong she is; Athletics is what she uses it for: climbing, jumping)*. **Charisma (Persuasion): +{{gate.cha}}** *(Charisma is how well she gets on with people; Persuasion is talking them round)*. |
| 2 | `dmscreen` | The DM screen | standing at the far side of the table | **THE GATE.** *Climb the wall*: Strength (Athletics), **DC {{gate.dcc}}**. *Talk to the guard*, who wants the paperwork in triplicate: Charisma (Persuasion), **DC {{gate.dcp}}**. *(DC means difficulty class: the number the roll has to reach.)* To make a check, roll the twenty-sided die, add your bonus, and **meet or beat the DC**. Every face is equally likely. |
| 3 | `window` | The window | over the radiator | Rain runs down the glass: proper drizzle, the kind that gets into everything. A card is stuck to the frame in the club’s handwriting: **HOUSE RULE: WET WEATHER. −{{gate.wet}} to Strength (Athletics) checks.** |
| 4 | `plans` | Strictmane’s plans | folded inside the marking pile, where you hid them so she wouldn’t peek | **DRAWN TO REGULATION.** Scale **1 : {{plan.S}}**. Main corridor on the plan: **{{plan.L}} cm.** Signed, in very straight capitals: COMMANDANT STRICTMANE. *(Only the plan’s words are on the object; the units are written in.)* |
| 5 | `mat` | The battle mat | spread across the tables | In pen along the edge, the club’s own rule: **ONE SQUARE = {{plan.sq}} m.** *(“Homebrew”: a rule the club made up and the rulebooks don’t have.)* |
| 6 | `dice` | The dice | in a heap beside the mat, a spell card under them | **FIREBALL.** *AoE: area of effect, everything inside the blast.* The blast is a **circle, radius {{fb.r}} m**, centred on the target. |
| 7 | `mug` | The tea mug | by the marking | *(blank)* Her tea, gone lukewarm. The pile beside it has not moved. A tea ring has appeared on the top essay. |
| 8 | `sign` | The blank sign | pinned to the brick wall by the whiteboard | *(blank)* A pinboard with nothing on it but a label in the corner in very straight capitals: NOTICES. Nothing has been noticed. **[X]** |

No numeral is typed into any clue, so the only clue figures are the tokens (the kiln rule, working doc §5i).
The die’s faces are described as “twenty-sided” in words.

---

## Locks

All three keypads, no instrument art (set-wide) and no `missArt` on any lock (the fail picture is the end of
the club, which is only true at time-out; the kiln and comic rule). **Proposed grades: gate 4, plans 3,
fireball 4; derived rating ★★ Core** (“For Jon” 2).

### Lock 1: the gate (probability with modifiers)

- **id:** `gate-modifiers-probability` (proposed) · **key:** `gate` · **grade:** 4
- **name:** The gate
- **brief:** The fortress gate is shut, and it is drizzling. There are two ways through: climb the wall, or talk
  to the guard and his paperwork. Her adventurer can try either. Work out which path she is more likely to pass,
  and tell the DM its chance of success, as a percentage.
- **instrument:** keypad · **label:** CHANCE OF SUCCESS (%) · `maxDigits: 3` · **verb:** Enter chance
- **missTitle:** {{gate.miss}}% is the climb on a dry day.
- **missSays:** {{gate.miss}}% is how often she’d get over the wall if it weren’t raining. The card on the
  window is there for a reason.
- **hints:**
  1. Have you looked outside? It’s drizzling.
  2. A bonus helps her. Does she need a higher roll or a lower one?
  3. Count the rolls that succeed on each path, out of {{gate.die}}.
- **solve:** Climb: the penalty takes {{gate.wet}} off her bonus, so she needs {{gate.needC}} or more on the die,
  which is {{gate.chC}} faces out of {{gate.die}}, {{gate.pc}}%. Persuade: she needs {{gate.needP}} or more,
  which is {{gate.chP}} out of {{gate.die}}, {{gate.pp}}%. Persuasion is the better path, at
  **{{gate.answer}}%**.
- **onOpen:** She rolls for the guard and the die stops on a nat {{gate.die}}: a natural twenty, the die itself
  showing the top number, no adding needed. The guard salutes and stamps her Form G-14. Mrs Rogers looks at
  the die, then at the two DCs on the screen. “Hang on, so the lower number isn’t the better bet? That’s
  actually quite clever.”

**Variant pot for lock 1 (proposals only; `gen-escape-variants.py` and `escape_set_checks.py` are not touched).**
Your ranges, applied as written: climb DC and persuade DC 10–16, ability modifiers +1 to +4, drizzle penalty −1
to −3 on the climb only, every required roll (including the forgotten-penalty roll) between 2 and 20, chances
that differ, answers whole multiples of 5, no clue number equal to the answer.

Derived, with the die’s faces `die` = 20: climb needs `needC` = `dcc` − `str` + `wet`; persuade needs `needP` =
`dcp` − `cha`; a path’s chance is (21 − need)/20 as a percentage. `answer` is the better path’s chance and `miss`
is the climb’s chance with the drizzle forgotten (need = `dcc` − `str`).

- **Instrument:** keypad, up to three digits; `answer` and `miss` (5–95) are settable. A keypad has no travel, so
  the end-of-travel rule does not apply.
- **Solver** (for `LOCKS`): `lambda x, v: x == max(v["pc"], v["pp"])`; `clue_numbers`: `[str, cha, dcc, dcp, wet]`.
  One value on the whole-number grid solves it.
- **Constraints in the pot:** (1) every roll from 2 to 20; (2) the two paths’ chances differ; (3) the penalty
  forgotten makes the **worse** path look better, so `pc < pp < pc0`, and `miss` = `pc0`; (4) her approved line is
  true: the **lower-DC path is the worse bet** (`dcc < dcp`, with the climb the lower and the worse); (5) answer
  and miss settable and different; no clue figure equal to the answer.
- **Result: 9 verified sets, not 10, and persuasion is the better path in all nine.** There are 158 sets that
  meet (1) to (5), but only **nine distinct answers** among them (30, 35 … 70), and the generator’s spread
  rule wants answers a gap apart. See “For Jon” 16 for why the pot cannot be half climb-better.

| DC climb | Str | wet | DC persuade | Cha | needs (climb / persuade) | climb % | persuade % | **answer** | miss (penalty forgotten) |
|---|---|---|---|---|---|---|---|---|---|
| 12 | +2 | −2 | 14 | +3 | 12 / 11 | 45 | 50 | **50** | 55 |
| 11 | +1 | −3 | 13 | +1 | 13 / 12 | 40 | 45 | **45** | 55 |
| 11 | +2 | −2 | 13 | +3 | 11 / 10 | 50 | 55 | **55** | 60 |
| 13 | +1 | −2 | 14 | +1 | 14 / 13 | 35 | 40 | **40** | 45 |
| 13 | +1 | −3 | 16 | +2 | 15 / 14 | 30 | 35 | **35** | 45 |
| 14 | +1 | −3 | 16 | +1 | 16 / 15 | 25 | 30 | **30** | 40 |
| 11 | +3 | −2 | 12 | +3 | 10 / 9 | 55 | 60 | **60** | 65 |
| 10 | +3 | −2 | 11 | +3 | 9 / 8 | 60 | 65 | **65** | 70 |
| 10 | +4 | −2 | 11 | +4 | 8 / 7 | 65 | 70 | **70** | 75 |

*(Variant 0 is yours, the first row. Every row’s penalty is `wet` on the climb only.)*

### Lock 2: Strictmane’s plans (scale)

- **id:** `fortress-plan-scale` (proposed) · **key:** `plan` · **grade:** 3
- **name:** Strictmane’s plans
- **brief:** The plans say the main corridor is drawn to regulation, at the Commandant’s scale. The party has to
  walk it. The club moves in squares on the mat, and the club has its own rule for how big a square is. Tell the
  DM how many squares the party must move.
- **instrument:** keypad · **label:** SQUARES TO MOVE · `maxDigits: 4` · **verb:** Enter squares
- **missTitle:** {{plan.miss}} comes from squares counted straight off the centimetres.
- **missSays:** The scale gives centimetres, and the mat is measured in metres. {{plan.miss}} would be a corridor
  longer than the whole fortress.
- **hints:**
  1. Did you use the Commandant’s scale?
  2. Those are still centimetres. How many in a metre?
  3. {{plan.real}} what? She’s moving in squares, not metres.
- **solve:** The corridor is {{plan.L}} cm on the plan and the scale is 1 : {{plan.S}}, so it is
  {{plan.L}} × {{plan.S}} = {{plan.cm}} cm. That is {{plan.real}} m. One square is {{plan.sq}} m, so the party
  moves **{{plan.answer}} squares**.
- **onOpen:** The corridor’s plan flips over in the dark and every square of it is exactly where it should be.
  Somewhere beyond it a pen stops writing. Mrs Rogers leans in. “Is that… is that Mr Strictman? You’ve put Mr
  Strictman in the game? I’m totally in.”

  *(The pen stopping, then Strictmane’s own wrong-entry line 1, “narrower than the plans”, is why the voice
  fits: it is the Car Trap voice moved into the fortress.)*

**Variant pot for lock 2.** Your ranges: scales 1 : 100, 1 : 200, 1 : 250, 1 : 500; plan lengths in whole
centimetres, 2–9; the club’s square **fixed at 2 m for the whole room** (`{{plan.sq}}` is 2 in every set, and
lock 3’s radius depends on it); `answer` a whole number from 4 to 30 and never equal to the plan length in
centimetres; `miss` the no-conversion value. Derived: `cm` = `L` × `S`; `real` = `cm` ÷ 100; `answer` = `real` ÷ 2;
`miss` = `cm` ÷ 2 (100 × `answer`, so `maxDigits: 4` is needed for answers up to 30).

- **Solver:** `lambda x, v: x * v["sq"] * 100 == v["L"] * v["S"]`; `clue_numbers`: `[S, L, sq]`.
- **Constraints:** `answer` whole and 4–30; **`L ≠ answer`**; `miss` settable and not the answer; no clue figure
  (`S`, `L`, 2) equal to the answer.
- **Result: 7 verified sets, short of the 8–10 target, and the shortfall is the spec itself.** With the square at
  2 m, **1 cm on a 1 : 200 plan is exactly 1 square, so `answer` = `L` for every length and the whole 1 : 200
  scale is excluded** (your rule, working as intended). 1 : 100 gives one set (8 cm → 4 squares), 1 : 250 two and
  1 : 500 four.
- **Two ways to reach the target, if you want it (not in the table, your call):** widen the plan length to 2–12 cm
  (**12 sets**), or add 1 : 400 to the scales (**15 sets**; every length 2–9 works because the answer is twice
  the length).

| scale 1 : | plan cm | real m | 1 square = | **answer** | miss |
|---|---|---|---|---|---|
| 500 | 4 | 20 | 2 m | **10** | 1000 |
| 100 | 8 | 8 | 2 m | **4** | 400 |
| 250 | 4 | 10 | 2 m | **5** | 500 |
| 250 | 8 | 20 | 2 m | **10** | 1000 |
| 500 | 2 | 10 | 2 m | **5** | 500 |
| 500 | 6 | 30 | 2 m | **15** | 1500 |
| 500 | 8 | 40 | 2 m | **20** | 2000 |

*(Variant 0 is yours, the first row.)*

### Lock 3: the fireball (area of a circle)

- **id:** `fireball-circle-area` (proposed) · **key:** `fb` · **grade:** 4
- **name:** The fireball
- **brief:** Strictmane’s goblins stand drilled in a grid, one square each, in perfect ranks. The fireball is an
  AoE, an area of effect: everything inside the blast is hit. Tell the DM how much ground it covers, to the
  nearest square metre.
- **instrument:** keypad · **label:** AREA COVERED (SQUARE METRES) · `maxDigits: 3` · **verb:** Enter area
- **missTitle:** {{fb.miss}} is the distance round the edge.
- **missSays:** {{fb.miss}} is what you get from the length round the blast, not the ground inside it. The
  fireball fills the inside.
- **hints:**
  1. That’s the distance round the edge. The fireball fills the inside.
  2. Area is in square metres. Did you square something?
  3. That’s the square the circle sits in, {{fb.sq}}. The corners aren’t on fire.
- **solve:** The radius is {{fb.r}} m ({{fb.rsq}} squares at {{plan.sq}} m each). Area = π × r² =
  π × {{fb.r}}² = {{fb.exact}}, which is **{{fb.answer}} m²** to the nearest square metre. (With π = 3.14 the
  answer is the same.)
- **onOpen:** The fireball lands. The goblins scatter with smouldering helmets, ranks knocked flat, and
  Commandant Strictmane cries out. “Formation! FORMATION! …Who authorised the fire?” Then he straightens his
  starched robes. “A tactical withdrawal. I shall be submitting Form R-1, requesting a rematch.” A pause. “In
  triplicate.”

  *(Jon’s lines, 15 Oct 2026; see “For Jon” 1. “Form R-1” answers the goblin’s Form G-14, and neither is ever in a
  clue. “π”, “r” and “²” are the method, as the kept lock text in Car Trap has its 2 × π × r.)*

**Variant pot for lock 3.** Your rule: the radius is a whole even number of metres, 4–12 m (whole squares at the
room’s fixed 2 m), and the area to the nearest square metre must be **the same whether π or 3.14 is used**. The
clue gives the radius in metres only; `{{fb.rsq}}` (the radius in squares) is used in `solve` and the hints, not in
the clue (see “For Jon” 3). `answer` = round(π × `r`²); `miss` = round(2π × `r`), the circumference; `sqr` =
(2 × `r`)², the square the circle sits in (the figure hint 3 addresses).

- **Solver, with the check stated:** `lambda x, v: x == round(pi * v["r"] ** 2) == round(3.14 * v["r"] ** 2)`.
  A radius where the two roundings differ makes the set unsolvable and the generator rejects it. One value on the
  keypad’s grid solves it.
- **Constraints:** `miss` settable and not the answer; the clue radius not equal to the answer; π and 3.14 agree.
- **Result: 5 verified sets, short of 8–10, and again it is the spec:** an even radius from 4 to 12 gives exactly
  five radii (4, 6, 8, 10, 12), and **all five pass the π/3.14 test** (nothing is rejected). Two caveats: with
  π = 22/7 the 12 m set would round to 453 (the engine takes one answer; Foundation papers give a calculator),
  and a radius of 2 m is outside your range anyway because its circumference and area coincide.
- **One way to reach the target, if you want it:** allow whole-metre radii (not only whole squares). 7, 9 and 11
  pass the π/3.14 test (5 is a half and rounds ambiguously), giving **8 sets**, but those radii are not whole
  squares at 2 m, which is the property you set. Your call.

| r (m) | squares | π: area | 3.14: area | **answer** | miss (circumference) | square (hint 3) |
|---|---|---|---|---|---|---|
| 6 | 3 | 113.10 | 113.04 | **113** | 38 | 144 |
| 4 | 2 | 50.27 | 50.24 | **50** | 25 | 64 |
| 8 | 4 | 201.06 | 200.96 | **201** | 50 | 256 |
| 10 | 5 | 314.16 | 314.00 | **314** | 63 | 400 |
| 12 | 6 | 452.39 | 452.16 | **452** | 75 | 576 |

*(Variant 0 is yours, the first row.)*

### Checked in a scratch run against today’s tools (nothing committed)

I ran every set above through `escape_set_checks.check_set` with the proposed solvers and clue figures, then
through the engine’s joint-draw rules (a to d in `check-escape-rooms.py`), with the square fixed at 2 m.

- **All 21 sets pass `check_set`:** 9 gate, 7 plans, 5 fireball. Each has exactly one solving setting on its
  keypad, the answer and misconception settable and different, no clue figure equal to the answer.
- **The joint pot: 9 × 7 × 5 = 315 combinations, of which 182 are VALID** (no clue figure in two locks’ clues,
  no answer in another lock’s clues, no answer equal to another lock’s misconception, no two locks with the same
  answer). **Variant 0 is a VALID draw.** The floor is 20. The gate sets were chosen greedily to keep that count
  high.
- **If you take the widenings:** plan length to 2–12 cm gives 12 plan sets, **288 of 540 VALID**; 1 : 400 added
  gives 15, **365 of 675**; whole-metre radii give 8 fireball sets, **324 of 504**.
- **Why `{{fb.rsq}}` is out of the clue:** with it in, variant 0 (Charisma +3 against “3 squares”) printed a 3 in
  two locks’ clues and was an INVALID draw (rule a); with the radius in metres only, variant 0 is VALID.
- The new locks need entries in `escape_set_checks.LOCKS` and bank entries (a new batch file) in phase 2; that is
  where the solvers above go. The engine’s “a lock never repeats the set it gave last time” rule applies as it
  stands. No script was changed here.

---

## Picture alts (from the three images you generated; to be re-checked against what is filed)

- **sceneAlt:** A school classroom after the last lesson, rain running down the tall window. Four tables are
  pushed together under strip lights with a gridded battle mat across them, three drilled blocks of small green
  goblin figures standing in ranks and a pair of figures in the middle. Character sheets, pencils and handfuls
  of dice sit at the places. A cardboard folding screen stands at the far side, a mug of tea and a tall pile of
  marking on the right, and on the brick wall by the whiteboard a blank pinboard.
- **failAlt:** The same classroom, the lights off and the rain still falling. Chairs are stacked upside down on
  the tables, the battle mat is rolled up under an elastic band, and the dice and goblin figures are boxed in
  clear tubs. A closed folder of papers sits where the character sheets were.
- **winAlt:** The same classroom, lights on. On the battle mat the goblins lie scattered and knocked over
  around a scorched black ring. On the nearest character sheet a twenty-sided die shows its top number beside a
  small drawing of a flame. The tea mug and the marking stand to the right.

## Hub card line and meta description

- **Hub card:** A teacher who has never played D&D is about to be taught by her own club, and the villain has
  drawn his fortress to regulation.
  Topics line: Probability · Scale · Area of a circle
- **Meta description** (153 characters; the same string for `description` and `og:description`): A 15-minute
  GCSE escape room. Teach a teacher her first D&D adventure, then see off the Commandant: probability, scale
  drawings and the area of a circle.

*(Both lines say the topic and level only, never the student, canon §7.5.3, and carry no year-group or
key-stage wording, SR-11.)*

## Credit

Proposed line, for the teacher page footer and the `room.js` header (and the start screen if you want it
student-facing): **“Built from a teacher’s idea. Thank you, Mrs Rogers.”** It names her, as she has agreed, and
carries no school, role or other identifying detail (the premise says she runs a club; the credit does not).
**Consent is recorded in the handover** (Jon, 15 Oct 2026).

## Art (phase 2)

Three files, filed by phase 2 from the pictures you generated, each first through
`scripts/strip-gen-watermark.py --width 1600 --frame 1600x873` (the Gemini PNG sparkle; a no-op on a clean
image):

- `docs/art/dnd-club-scene.webp`
- `docs/art/dnd-club-fail.webp`
- `docs/art/dnd-club-win.webp`

Nothing is placed in `docs/art/` in this phase. The three pictures read as one room at one time of day (same
camera, same window, same table), and each matches its alt above; zoom-check before filing that the pinboard,
the character sheets and the die’s faces carry no readable writing.

---

## Checklist: the voice contract, SR-14, SR-11, §7.5.3 and the room rules

**Voice contract** (`docs/escape-room-voice-contract.md`, fixed constraints) and its STOP IF:

| Rule | Result |
|---|---|
| Students are always the heroes; the antagonist is the obstacle | **Pass.** The students are the DMs and the experts; Mrs Rogers is the learner and is never mocked; Strictmane is what they beat |
| Wrong-entry lines never mock the student or their answer, only the lock | **Pass.** Every line is Strictmane about plans, forms and gates; none addresses or mentions a student |
| The antagonist loses graciously; no humiliation | **Pass.** Ruled by Jon, 15 Oct 2026 (“For Jon” 1): panic as the fireball lands, then a tactical withdrawal and a rematch request in his own bureaucratic register; no scurrying, no flight, nobody laughs at him |
| Voice through the room setup, not a narrator layer | **Pass, with a note.** Hook and brief are narration, as in `hamster-heist`; Strictmane’s voice carries the wrong-entry slot |
| “Idiot” and “stupid” never appear | **Pass** |
| British English | **Pass.** Tea, marking, caretaker, “Miss” |
| Name: real-sounding, no equipment puns, no innuendo, no real person | **Pass.** Strictmane is an aptronym, the house convention, and invented per your brief. **For you:** the cameo of Mr Strictman |
| STOP IF: inventing the character rather than drawing it out | **Did not fire.** Premise, voice, lines, locks, stakes and fail are yours; every extrapolation is **[X]** |
| STOP IF: a change to puzzle logic or lock behaviour | **Did not fire.** The maths is yours; the only added constraint is `dcc < dcp` (“For Jon” 7) |

**SR-14 (sensitive content)** and the scan (`scripts/check-content-safety.py`):

| Check | Result |
|---|---|
| Tier (a) words (death, kill, dead, weapon, violence, abuse…) | **Pass.** None in the prose. The goblins are knocked over and scattered, the helmets smoulder, nobody dies |
| Tier (b) in humour (illness, injury, crash…) | **Pass.** None |
| “Battle mat”, “fireball”, “goblins” | **Pass.** Not in the lists; fantasy with no harm to a person |

**SR-11 (age-neutral labels)** and **§7.5.3 (name the maths, never the student):**

| Check | Result |
|---|---|
| No year group or key stage, no “primary”/“secondary school” on a student surface | **Pass.** “School D&D club” only; the school is not named |
| No “resit”, “retake” or “post-16” | **Pass.** The grades 1–3 audience note appears only here and in the handover (teacher surfaces) |
| Level label | **Pass.** “GCSE” only on the meta and card lines |

**Room rules** (working doc §3, §4, §8; canon §11.3):

| Rule | Result |
|---|---|
| One enforceable failure, able to reach the students during play | **Pass.** The club’s end time (a clock); fail = the caretaker closes the room |
| A character who is not present cannot be the threat | **Pass.** Strictmane is in the fiction the students are running |
| Each character speaks only in their own room | **Pass.** Mr Strictman is recognised, never speaks |
| No third never-knew ending for the antagonist | **Pass.** He sees his defeat |
| Students win by putting something right | **Pass.** They teach her, and each lock is a rule she is shown |
| If the students use the antagonist’s own method, the brief says why it is different | **Pass.** They do not; he measures a fortress to rule it, they read the same plans to teach |
| No figure in the prose outside `{{tokens}}` | **Pass, with five exceptions in words or fixed names, all flagged:** “two point six centimetres” (his line); “Form G-14” and “Form R-1” (form names, in the wrong-entry line, lock 1’s open and lock 3’s open, never a clue); “nat 20” is `nat {{gate.die}}`; the method π, r and ² in lock 3; “fifth level”, “twenty-sided” and “every face” are words. No numeral is typed into any clue |
| No tokens in `hook`, `brief`, `stakes` (written raw by the engine) | **Pass.** None |
| Never “Ofsted”; no brand names; no year | **Pass.** “D&D” is the club’s name (“For Jon” 11); no logo, creature or character is named |
| “Dungeon Master” never appears | **Pass.** “DM” throughout |
| Wizards of the Coast logos, creatures, named characters | **Pass.** Generic goblins, fireball, dwarf, wizard only |
| No real child named | **Pass.** No student is named in the room or in this document |
| Mrs Rogers’s approved lines used as written | **Pass.** Start, lock 1, lock 2, ending and character choice, word for word (including “a twenty-sided dice”) |
| Wrong-answer feedback never gives the answer | **Pass.** Misconception text and hints stop short on every lock; the worked solution is in `solve` only |
| UK school timings; St Martha’s | **Pass.** After the last lesson; no clock time; the school is not named |
| Eight objects, at least two blanks | **Pass.** Six clues, two blanks (`mug`, `sign`) |
| Each lock’s `brief` carries the new premise | **Pass.** All three |
| Every lock has exactly one settable answer; the engine can express them | **Pass.** Three keypads, a percentage included |
| Variant pot: 8–10 verified sets per lock, drawn jointly | **Pass, accepted by Jon 15 Oct 2026.** Gate 9, plans 7, fireball 5 (within the house range; the plan and fireball counts follow the spec’s own ranges); 182 of 315 joint draws VALID, variant 0 VALID. Lock 1 is persuasion-better in all nine sets by ruling (“For Jon” 16) |
| No `missArt` | **Pass.** The fail picture is the end of the club |
| The pictures are of what the room is | **Pass.** The three you generated: scene, fail, win |
| Meta description 150–160 characters | **Pass.** 153 |
| ★★ | **Pass.** Proposed grades 4, 3, 4 derive ★★ Core; no star field added |
