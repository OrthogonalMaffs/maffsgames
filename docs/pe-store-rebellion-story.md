# The P.E. Store Rebellion — story breakdown for sign-off

**Room 2 of 8 in the escape-room voice rewrite. Written 08 September 2026. Awaiting green light.**

Source of truth for the room itself is `escape-rooms/pe-shed-rebellion/room.js`. Contract:
`docs/escape-room-voice-contract.md`. Running state: `docs/escape-room-voice-rewrite.md`.

Everything below is prose only. No lock `id`, `key`, `instrument`, `variants`, `missTitle`,
`missSays`, `hints` or `solve` was changed, and the checker proves it.

---

## 1. The one-line version

Cross-country is on in freezing sideways rain because it is always on. The only way out is to
flood a bit of the field on purpose, precisely enough to send the Head of P.E. sprinting off to
save the cricket square without stopping for his coat — and then to be indoors, with the arena up,
before he gets back.

## 2. The antagonist

**Mr Barry Lunge — "Lungey".** Head of P.E., twenty-six years.

Old school. Believes running in freezing rain builds character, and means it — he is not being
cruel, he is being consistent. Padlocked the store because the equipment "has been walking off
since February", which in his view is standards, not meanness. **Does not understand the maths his
locks sit behind**, and would say that grit and understanding are the same thing if pressed.

*Speech:* short sentences, often no verb. One capitalised word per speech at most. Sporting
metaphor applied to things it does not fit. Calls them "son" and "you lot". Nostalgic asides that
go nowhere. **Never swears and never insults anybody** — he is a P.E. teacher in front of students,
not in the staffroom.

*The anecdote:* he walked twenty-six miles to this school. No shoes. And he was grateful. It
arrives in pieces across the wrong-entry lines and never finishes usefully.

*Would never say:* "Let me explain the reasoning." / "That's a clever bit of maths, that." /
"Fair enough, you've got me."

Everything in this section came from Jon. Nothing in it is extrapolated.

## 3. The premise, and why it changed

The first pass had the students **hiding a teacher's coat so it could not be found** — winning by
spite, the same fault the hamster room's first draft had. Jon's fix supplied the missing mechanism,
and it repairs the ethics as a side effect:

**The flood is the tool, not the failure.**

1. Lungey stands in the store doorway with the register. Nothing moves while he is in it.
2. The standpipe is round the gable end of the store, out of his eyeline — **the one thing they can
   reach with him standing in the doorway**, and the room's `brief` says so outright rather than
   leaving it to the summary. They open the sprinkler deliberately, far enough that the wet patch
   reaches exactly the limit the grounds staff are allowed on the cricket square, and no further.
3. That is an emergency he will run for. He goes **at a sprint, with no time to take his coat**.
4. While he is out there: the compressor is set, the arena inflates in the sports hall, the
   equipment locker gives up the dodgeballs.
5. The coat goes back on its hook and the store gets **his own padlock**, the one he fitted in
   February to keep things safe. His coat is now the thing being kept safe.
6. He returns soaked, finds the hall full, and takes charge of the dodgeball.

They never lie to him and never steal anything. They out-organise him, and he is beaten by his own
rule about the store.

**The maths did not move to accommodate any of this.** The named misconception on lock 1 has always
been an arc that is *too small* — so "short of the limit and he does not budge" is what the wrong
answer already did.

## 4. The three locks, and their fictional justification

| # | Lock | Maths | Why it is in the way |
|---|---|---|---|
| 1 | Sprinkler override | Area of a sector; the limit is given as `K·π` so the π cancels and never becomes a decimal | It is the diversion. Exactly at the grounds staff's limit: short of it he does not move, past it you have flooded the square |
| 2 | The compressor | Inverse proportion; find `k = P×V` before touching the gauge | Set it for the arena fully open, not folded flat, or the seams split |
| 3 | Equipment locker | Linear sequence recovered from **non-consecutive** terms | The dodgeballs are in it. Lungey's own daily code, from his own clipboard — the one lock that is actually his |

Only lock 3 was ever set by Lungey. He did not invent the sector-area problem; the sprinkler and
the compressor are simply the world being difficult, which is truer to a school than a P.E. teacher
who devises geometry.

## 5. The single failure state

**Running the clock out**, and nothing else.

The whistle goes and cross-country happens exactly as timetabled: six kilometres, sideways rain,
kit that will not be dry by Thursday. Lungey stands at the gate in the waxed coat with a flask and
counts them through, then counts them through again, because he always counts twice.

This satisfies the rule that came out of the hamster room: **the consequence reaches the students
during play, and the person enforcing it is present.**

## 6. The final prose

**Setup — Lungey speaking, then narration**

> Right. It's on. It is always on.
>
> Four degrees is not a reason, it's a temperature. A bit of weather never hurt anybody — it builds
> you. You'll thank me. Six kilometres. Round the field, up the lane, back past the tennis courts,
> and I'll be counting.
>
> Store's open. It's a store, not a shed — I have told you lot that since Year 7. And it's not a
> free-for-all either — nobody touches anything that isn't a BIB, because the equipment has been
> walking off since February and I have had enough of it. Padlock goes back on the second we're
> moving.
>
> Fifteen minutes. Get changed.
>
> *He plants himself in the doorway with the register. Bare breeze block, one small window, mud
> dried up the walls where forty terms of filthy kit has been thrown at them, and colder inside
> than it is out. The hooks along the back wall are empty but for one. His coat hangs on it, waxed,
> enormous and bone dry.*

**Wrong entry** — indexed by how many wrong settings have been made; the last repeats forever.

| # | | |
|---|---|---|
| 1 | Nothing gives. | Somewhere behind you, not looking up: "Two minutes, you lot. Two." |
| 2 | The setting slides back to where it was. | "Nobody ever got round that field standing still thinking about it." He is not talking to you. He is talking to the register. |
| 3 | Something resets itself with a clack. | "I walked to this school. Twenty-six miles. No shoes." Nobody has asked. |
| 4 | Another one. The whistle is no further off than it was. | "…and I was grateful." |

**Lock opens — the sprinkler**

> The head clunks round and settles, and through the little window the far edge of the arc walks out
> across the grass toward the cricket square. Behind you the register hits the floor. He doesn't say
> anything. He just goes.

**Escape**

> He goes across that field like a man half his age — no coat, no flask, nothing over the tracksuit,
> because the cricket square does not wait while you find your coat.
>
> By the time he has the standpipe shut off the compressor is running, and the folded nylon block in
> the corner has begun, slowly and then all at once, to become a room. The arena goes up between the
> badminton posts with a noise like a held breath. The locker gives up twelve dodgeballs and,
> inexplicably, a kettle. The coat goes back on its hook in the store, and the store gets the
> padlock he put on it in February.
>
> He appears in the hall doorway seven minutes later, wet through to the shoulders, and stands
> dripping on the parquet while twenty-eight people who were supposed to be running six kilometres
> carry on not doing it.
>
> "Right," he says. "Builds character, this."
>
> Then he gets his whistle out. "Two teams. Bibs on. And somebody fetch my coat, I'm not asking
> twice."
>
> He is asking twice. He asks four more times before the end of the lesson.

He loses without ever conceding — he turns his own creed on himself instead, which keeps "Fair
enough, you've got me" out of his mouth and still lets him lose graciously.

## 7. What is Jon's and what is not

**Jon's, verbatim or near:** the character sheet; running in the rain builds character; the
twenty-six-mile walk with no shoes; the flood-as-diversion mechanism and the coat left behind;
the store being breeze block, freezing, with mud on the walls; the room being a store, not a shed.

**Extrapolated — strike freely:** "Builds character, this" as the losing line; "Two teams, bibs on";
counting the class through twice; "I have told you lot that since Year 7"; the kettle and the
dodgeballs (both already in the room from the original build).

**Extrapolated but kept by decision:** the register hitting the floor. Mine, not Jon's, but it is
the moment the room turns and it does that work without any narration.

**Changed to match the picture:** the setup first said the back-wall hooks were "empty but for one",
with the coat on it. The filed picture shows that rail completely bare, so the coat moved to the
hook by the door — which also puts it behind him as he stands in the doorway, which is what the
escape needs anyway.

## 8. Verification

- `scripts/check-escape-rooms.py` — 24 locks, 193 variants, every room agrees with the audited
  bank and with `variants.json`, all tokens resolve
- Locks region byte-identical apart from the deliberately rewritten sprinkler `brief` and the
  dropped instrument art; all 8 object ids intact; all 27 tokens present
- Played in Chrome: intro, room and lock screens render, no page console errors

## 9. Outstanding before it ships

1. ~~The scene picture~~ **Filed 08/09/2026.** `docs/art/pe-shed-rebellion-scene.webp`, 1600×873,
   from `Downloads/PE Store Open.jpg` — no watermark found, as expected for a JPG. Verified in the
   browser: room page and index card both show the store.
2. ~~The card alt~~ **Done.** `escape-rooms/index.html` now carries the new `sceneAlt` verbatim,
   lifted straight out of `room.js` so the two cannot drift.
3. ~~Failure and victory pictures~~ **Done 08/09/2026.** Both drawn to the empty-room brief and
   filed at 1600×873, with `failAlt` and `winAlt` rewritten to match. Both PNGs carried a watermark
   the detector could not see and could not safely inpaint — one mark sat against the door frame,
   the other on a court-line vertex — so it was **framed out**. The crops differ between the two
   because the strips differ: the failure picture's right-hand strip is the coat the whole picture
   is about, so it lost its floor and left edge instead.
4. ~~The URL~~ **Settled: the slug stays `pe-shed-rebellion`.** The title is The P.E. Store
   Rebellion everywhere a human sees it; the directory, `slug`, image filenames, canonical link and
   sitemap entry do not move. The page has been live and indexed since 01/09 and the domain has a
   known indexing problem — 68 URLs discovered-not-indexed — so trading an indexed path for
   semantic tidiness is the wrong trade today. Revisit when the domain has trust.
5. **The two shared-engine jobs now block rooms 3–8, not just this one.** Two rooms already carry
   written wrong-entry escalation the engine cannot read. The engine contract — read `wrongLines`
   instead of the one hardcoded string, and guard the instrument `<img>` so a lock with no art does
   not request a missing file — should land **before room three**, so the remaining six are written
   into a mechanic that exists rather than one that is pending.
