# Escape room voice rewrite — the working document

**Started 08 September 2026. SIX ROOMS OF EIGHT ARE DONE AND LIVE** (Rugby Mud released 15/09), **plus two new
rooms built from scratch: The Comic Caper and The Kiln Disaster, both live 17/09.** Room five,
`heatwave-mutiny`, was written, reviewed by a second Claude, illustrated, play-tested by Jon and
released on 13 September — its full record is `docs/heatwave-mutiny-sanity-check.md` (read the
corrections box first). **Neither remaining rewrite can be opened cold:** IT Vengeance and Car
Trap both need the §7 premise/image conversation with Jon before their session starts.

> **State of the repo, end of 17/09/2026.** Everything is pushed; `origin/main` is at `7b29150`. **Eight rooms
> live** — rooms one to six, plus The Comic Caper (§5g) and The Kiln Disaster (§5i). IT Vengeance and Car Trap
> remain withdrawn behind noindex holding pages — see §5c. The same day also landed the **joint variant draw
> for every room** (§8, "Cross-lock collisions"), a `teacher.js` fix (§8), the **hub's replay figures deleted**
> (§5c) and **bank batch 7** with its three libraries.
>
> **Nothing is half-built.** The last session finished on a clean tree with every checker green:
> `check-escape-rooms.py`, `check-lock-bank.py docs/lock-bank-batch7.txt` and `check-canonical-links.py`.
>
> **Open, for Jon to order:**
> 1. **pe-shed-rebellion's variant 0 collides** — its own contract (§5h).
> 2. **IT Vengeance or Car Trap** — settle its premise/image clash with Jon (§7) before reading its `room.js`.
> 3. **Small Kiln follow-ups, none blocking** (§5i): `teacher.html` never names Mr Mudge; the teacher page
>    does not say that a group hitting only named misconceptions skips some of his wrong-entry lines; and the
>    fail and win pictures have frayed straps that read as fingers at thumbnail size.
>
> **THE SUITE SHIPS ROOM BY ROOM.** Jon's call on 08/09: release each room as it is finished rather
> than holding everything for one push. Releasing is part of finishing — see §5c, and do not skip
> it, because the hub card, the front-page card, the sitemap, and six counts
> all move with the room.
>
> **Still do not push without asking** — the change is what gets pushed, not the permission. Jon approved
> each push on 17/09 individually; none of that carries to the next change.
>
> A warning that still stands: the hamster rewrite once sat **uncommitted** for a whole day — five
> hours of work, one `git checkout` from gone. **Check `git status` at the start of a session, not
> the end.**

This is the file to read first if you are picking the rewrite up cold. It holds why the work is
happening, how a room gets done, what is finished, and the things that have already bitten.

The binding contract is `docs/escape-room-voice-contract.md`. This file is the running state.

---

## 1. Why

A teacher left this through the site feedback form on 08/09/2026, having found `/escape-rooms/`
unprompted:

> Every single aspect of every escape room is completely AI generated — the images look like the
> first attempt at image generation, and all of the text looks like a human wasn't involved at all.
> [...] I could just generate my own escape room(s) of exactly the same quality myself with a £15
> per month AI subscription that I already have anyway. Why would I use yours when I've no reason to
> believe a human even checked it? [...] As it stands, none of this is usable.

They were right, and the specific diagnosis is the useful part: **the puzzles and the maths are
sound; the prose has no author behind it.** Eight rooms were built fast over the summer with
generated narrative and no established voice, and it reads exactly like what it is.

Their concrete suggestion — *"think of a character or two with some personality and have all the
dialogue be written from their perspective"* — is what the rewrite does.

**Do not treat this as a polish pass.** Rewriting the same content in a livelier register
reproduces the defect. The fix is that a specific person, with a name and a way of speaking, is
behind the text in each room.

## 2. How a room gets done

One room per session. Do not start a second before the first is signed off.

1. **Read the room first.** `room.js` end to end, plus `index.html` and `teacher.html`. Do not ask
   Jon anything until you can describe the room back to him.
2. **Interview Jon** to establish the antagonist: name, what they have done and why they think it
   is justified, whether they understand the maths they have locked things behind, and how they
   speak. Ask open questions in prose. **Do not offer a menu of pre-written characters** — the
   whole risk is inventing the character for him, and the contract's STOP IF exists to guard it. If
   his answers are thin, say so; do not fill the gap.
3. **Write a character sheet** from his answers, marking anything you extrapolated so he can strike
   it.
4. **Draft the slots** — setup, lock-opens, wrong-entry, escape — and show them in the message. Do
   not touch a file yet.
5. **Jon reviews.** Expect the premise to move, not just the wording; see §3.
6. **Write `room.js`**, run `python scripts/check-escape-rooms.py`, and report.
7. **Art last**, once the narrative is settled, because the pictures are of what the room actually
   is. See §6.

## 3. The premise usually moves, and that is the point

The hamster room's first pass produced a good voice attached to a bad premise: three students
stealing an animal and fooling a technician with a toy. Two things were wrong and neither was
visible until the character work exposed them.

- **The students were thieves.** They win in every other room by putting something right. Here they
  won by deception.
- **The pressure was attached to somebody who could not reach them.** The technician's check
  happened after the students had gone home. That is an epilogue, not a consequence.

**Expect this.** Interviewing for voice surfaces premise faults, because a character who has to be
justified out loud cannot hide behind a summary. Budget for the premise to be rewritten in the
session, and read the corrected-premise contract in the git history of this file's sibling as the
worked example.

Two rules came out of it and apply to all eight:

- **One enforceable failure per room**, and it has to be able to reach the students during play.
- **A character who is not present cannot be the threat.** They can be the *standard* the work has
  to survive, which is a different and often better job.

**One deliberate exception, `kiln-disaster` (17/09/2026):** it has no antagonist at all. Smudgey is an ally, and the kiln's own countdown is the pressure. The rule exists to stop a threat that cannot reach the students during play — the Car Trap problem — and a countdown reaches them more reliably than any character. The reasoning is in §5i. **Do not "fix" that room to match the rule.**

## 4. Standing rules for the set

From the contract, plus what has been settled since:

- Students are always the heroes; the antagonist is the obstacle they overcome.
- Wrong-entry lines never mock the student or their answer — only the lock.
- The antagonist loses graciously. No humiliation. "Idiot" and "stupid" never appear; "muppet" is
  allowed.
- British English throughout. Caretaker not janitor, football not soccer, tea not coffee.
- **Characters may recur offstage across rooms, but each speaks only in their own room.** Otherwise
  all eight rooms contain the same three teachers and none of them feels distinct. Lungey is named
  as the cause of the hamster room and does not say a word in it.
- No year anywhere and no brand marks — this material is meant to be reused next September.
- The school is **St Martha's Secondary** throughout.
- UK schools finish at **3:30**. Any timing in a room has to sit sensibly around that.
- **Vary how the antagonist exits. Two of the first four rooms end on the adult never finding
  out** — Test Tube Dave ticks his box, Cinnamon never knows how close it was — while Lungey and
  Tension both see their defeat, which is the better variety. Each lands on its own, but a teacher
  running three rooms in a term will notice the repeat. **Rooms five to eight: no third
  never-knew ending** unless it is the only thing the premise supports, and say so if it is.
- **If the students use the antagonist's own method, the room has to say why that is different**,
  and say it in the brief where it reframes everything that follows — not in the win, where it can
  only report that nobody looked. Getting away with it is not the same as not having done it.
  Caught in review on `canteen-hack`, where the students work the same administrator session
  Cinnamon used; see §5e.

## 5. Per-room status

| Room | Slug | Antagonist | State |
|---|---|---|---|
| The Great Hamster Heist | `hamster-heist` | **Mr Beaker** (asleep) + Test Tube Dave (offstage) | **Done 08/09/2026**, then **reopened the same evening for five more fixes** — see §5d. All live |
| The P.E. **Store** Rebellion | `pe-shed-rebellion` | **Mr Barry Lunge, "Lungey"** | **Done 08/09/2026** — prose, all three pictures, retitled. Reviewed by a second reader, the notes applied, and Jon moved to room three without asking for more. Slug deliberately unchanged |
| The Prom Budget Embezzlement | `prom-budget` | **Mr D Tension** (on the phone next door) | **Done 08/09/2026** — prose, all three pictures, SEO and index card. Jon's green light is the only thing left. See §5b |
| The Rugby Mud **Bath** (was Sabotage) | `rugby-mud` | **Mr Mower**, groundskeeper (overheard through his hut window), on Mr Lunge's orders | **WRITTEN 15/09/2026, signed off by Jon + a cold Windows-Claude read.** Prose, teacher page, hub/front cards, sitemap and counts (six; 149 sets / 3,290 combinations) done locally. Win picture filed (edited to remove brand stripes on the boots). **RELEASED 15/09/2026** (`80007d7`), all three pictures filed. See §5f |
| The IT Teacher's Vengeance | `it-vengeance` | — | **WITHDRAWN from the live site 08/09/2026 — see §5c.** Not started. **Partial premise/image clash — see §7** |
| The Heatwave Mutiny | `heatwave-mutiny` | **Mr Robin Banks** (energy contractor, on a replayed radio clip) | **DONE AND LIVE 13/09/2026** — prose, scene (air con added)/fail/win pictures, SEO, teacher-page fixes, released. Five rooms now live: 125 number sets, over 2,800 combinations, 300 (heatwave) to 1,000 (canteen). Full record in `docs/heatwave-mutiny-sanity-check.md`, corrections box first. **The freezer failure was dropped, and the engine work it prompted (per-lock misconception pictures, three-strikes ending) is CANCELLED, not deferred** |
| The Canteen Menu Hack | `canteen-hack` | **Ms Cinnamon** (monologuing across the corridor) | **DONE AND LIVE 12/09/2026** — prose, all three pictures, SEO, cold review applied, released and pushed (`49c02d8`). See §5e |
| The Comic Caper (new room, not a rewrite) | `comic-caper` | **Ms Fromage** (outside the door, about her cruise) | **LIVE 17/09/2026** (`d2b27a2`, art `9e0bf8a`, wording `f6c25da`) — see §5g. GCSE resit, batch-6 locks. Scene, fail and win pictures filed 17/09. The fail picture shows the cupboard gone, so no lock may set `missArt`. **Timing: 3:16** — author solo play-through, knows the answers' methods, not a student baseline |
| The Kiln Disaster (new room, not a rewrite) | `kiln-disaster` | **None — Mr Stephen Mudge ("Smudgey"), who teaches Art, is an ally, and the kiln's countdown is the pressure** | **LIVE 17/09/2026** — see §5i. GCSE resit, batch-7 locks, built to a Project Claude contract rather than an interview. Scene (re-rolled for palette), fail and win pictures filed 17/09. The fail picture shows the suppression system fired, so no lock may set `missArt`. First two-digit keypad on the site. **320 VALID draws of 700** |
| The Headteacher's Car Trap | `car-trap` | — | **WITHDRAWN from the live site 08/09/2026 — see §5c.** Not started. **Premise/image clash, and it has lost its antagonist to room three — see §7** |

**The shared-engine job is DONE, 08/09/2026**, before room three as planned. `wrongLines` is read
and the instrument `<img>` is guarded; 32 lines in `engine.js`, 30 of them the comment recording the
misconception-consumes-an-index decision. Verified in a browser: all four lines in order across two
different locks with the last repeating, the six unconverted rooms printing the original string
unchanged, and one `.webp` request on the whole room (the scene, 200). **Rooms three to eight are now
written into a mechanic that exists.**

Rooms A and B (Coach Trip Hijack, Tuck Shop Heist) remain unbuilt and need a maths pass before
anything else — see `escape-rooms-scenarios.md`. They are not part of this rewrite.

## 5a. P.E. Store — what is written and what is outstanding

The premise moved, as §3 predicts. **The flood is the tool, not the failure.** Lungey holds the
store doorway and nothing moves while he is in it; setting the sprinkler to exactly the grounds
staff's limit sends him across the field at a sprint, too fast to take his coat. The coat then goes
behind his own padlock. Timeout is the single failure: the whistle goes, cross-country happens as
timetabled, and he does it dry.

The room is now a **breeze-block P.E. store**, not a timber shed — Jon redrew it. The title stays
`The P.E. Shed Rebellion` because `pe-shed-rebellion` is baked into the directory, the `slug`, the
image filenames, the canonical link, `og:url`, both index cards and the sitemap, and the page has
been live and indexed since 01/09. The mismatch is now a character beat: everyone calls it the
shed, Lungey calls it the store and corrects them.

**Scene art landed 08/09/2026.** `pe-shed-rebellion-scene.webp` rebuilt at 1600×873 from
`Downloads/PE Store Open.jpg` (one of eight new establishing shots saved that afternoon; the other
seven are still in Downloads under their own names). No watermark found — JPG downloads are clean.
The index card alt was swapped in the same pass, lifted verbatim from `room.js`.

**All three pictures are done, 08/09/2026**, in the new empty-room style at 1600x873, and all three
alts describe what is actually on disk. The failure picture is the store after the run, with the
coat dry on its hook among the soaked kit; the victory is the sports hall with the arena up and the
rain falling on an empty field. The two carried a watermark the detector could not see and could not
safely inpaint, so it was **framed out**; the crops differ between them and the reasoning is in
`docs/escape-room-image-prompts.md`.

**Outstanding before this room ships:** nothing on the art. Jon's green light on the prose is the
only thing left.

## 5d. Room one was reopened after it was called done — read this before calling one finished

`hamster-heist` was signed off, committed, illustrated and pushed. Jon then read it properly and found
**five things in one sitting**, on 2026-09-08. All are fixed and live. They are listed here because
they are the shape of what a "finished" room still contains:

1. **The dream was implied, never stated.** The brief said Beaker was "asleep ... arguing with Geoffrey"
   and left the reader to join those up. It now says he is having the argument *in his sleep*, that
   Geoffrey is not in the store room, and that Geoffrey retired in 1994. The first `wrongLines` entry
   says "fast asleep and mid-argument" so it lands where the joke first fires.
2. **"ran out of plan" was too clever for the point it was making.** Now: he confiscated the hamster
   with total confidence, "and that was as far as the thinking went."
3. **A *yellowed* invoice said the wheel was "Fitted Tuesday"** — on a cage the brief says nobody has
   had cause to open in twenty years. Two contradictions in one clue, and neither is a typo: the object
   name, the clue and the room's own premise all disagreed. The date has now gone brown with the paper.
4. **Mr Beaker's mug rendered a literal `&rsquo;s`.** See the `esc()` gotcha in §8 — a whole class of
   bug, one instance across eight rooms.
5. **The room still had instrument art** on all three locks. It predates the set-wide decision to drop
   it, and nobody went back.

**And then a maths error, which is a bigger deal.** The feeder lock asked for the **greatest** volume
the hopper could hold. A depth recorded as D cm to the nearest centimetre lies in [D−0.5, D+0.5), so
D+0.5 is a supremum that is **never attained** — exactly 9.5 rounds *up* to 10 and could never have been
written down as 9. The lock asked for a volume the hopper cannot have, and a student sharp enough to
notice would have been right and marked wrong. It now asks for the **smallest** volume, which is real
and reached. Bank ANSWER 620 → 580.

**Three things worth carrying forward:**

- **"Done" means the checker passed and I played it. It does not mean Jon has read it.** Budget for a
  pass like this on every room.
- **Fix maths through `scripts/gen-escape-variants.py`, never by hand** — re-running is seeded, so no
  other room's library moves, and `check-escape-rooms.py` pins variant 0 to the bank's ANSWER, so the
  bank has to move with it.
- **An audited lock can carry its own disclaimer and still be wrong.** This one's AHA line said the
  answer worked "even though nothing measures exactly that". That is a defect report, not a
  justification. The standing rule is now in `docs/escape-puzzle-bank.md`: **bounds locks ask for the
  minimum.**

**One thing changed that is on the contract's DO NOT TOUCH list**, deliberately and with it said out
loud: `hamster-heist/teacher.html`'s topic, curriculum line and one `clueMap` label all said "upper
bound" / "greatest possible", and leaving them would have had the teacher page teaching the opposite of
the room.

## 5b. Prom Budget — what is written and what is outstanding

The premise moved, as §3 predicts, but it moved on a question Jon asked rather than on a character
fault: **the room used to be set on prom night.** A bronze cannot be cast, delivered and craned into
a hall between four o'clock and seven, and a prom cannot be rebuilt from nothing in the same window
either. It is now set **a week before**, and the statue **already exists** — cast, crated, on a
pallet in a foundry waiting for the money to land. That is why the practice maquette has stood on
his desk for months, and it makes him worse: he has been at this since the spring.

**The clock is the phone call, not the bank.** The old text ran two clocks — fifteen minutes in the
office, and a transfer clearing in thirty-five — and never explained the second. Cut. The portal
only reverses a commission from the account that placed it, his is logged in on that desk, and it
closes when he comes back and sits down.

**Mr D Tension**, headmaster, ten years, feels massively under-appreciated. He hoped the governors
would commission a statue of him unprompted; they did not, so he has stopped waiting, and when it
appears he will say the prom committee did it themselves. Long-winded, self-important, a bore.
Taught Business Studies for eleven years and will tell you so; he set these locks himself and is not
as good at maths as he thinks he is. He loses stoically and is crying inside. The initial is the
joke and is never spelled out.

**The wrong-entry slot is one half of an overheard phone call**, and every entry is one more
obstacle cleared on his end — his problems get solved while the players' do not. That is the same
escalation logic as Beaker and Lungey running on a completely different engine, which is the first
evidence that the pattern has range. The fourth line, "Right. So we're agreed.", repeats for the
rest of the game.

**One continuity trap, already closed.** Because that last line repeats, a player who keeps getting
it wrong hears him agree to conclude the call over and over without it ever concluding. `win`
therefore says *the corridor went quiet at some point and nobody noticed* rather than that nobody
heard him finish — which reads correctly at zero wrongs and at twelve. The reasoning is written into
`room.js` beside `wrongLines` so it does not get tidied back out.

**Verified in a browser, not by reading the file:** all four wrong-entry lines in order with the
fourth repeating three times; all three lock briefs carrying the new premise; every clue token
resolving; one `.webp` request on the whole room, so the instrument-art guard is holding; and the
room played through to the win screen.

**No maths moved, and it is provable** — every lock `id`, `key`, `instrument`, `variants`,
`missTitle`, `missSays`, `hints` and `solve` is byte-identical to the version at `HEAD`. The only
lock field that changed is the second lock's display `name`, "DJ deposit" to "The prom reserve",
because its clues are a forgotten reserve account with nothing to do with a DJ. The `id`
`dj-deposit-compound` is untouched.

**All three pictures landed the same day**, in the new empty-room style at 1600x873, and all three
alts describe what is actually on disk. The failure and victory pair came back with the sparkle on
the identical pixel, sitting on a court line in both, and the detector missed both again — they
were framed out on **one shared crop**, which works because they are the same hall from the same
camera and keeps the two framings matched. Two prose lines moved to match the pictures rather than
the reverse: the mirrorball is hung and turning, and the failure table has no speaker on it. The
first of those also settled a contradiction already inside `win`. Details in
`docs/escape-room-image-prompts.md`.

**Outstanding before this room ships:**

- **Jon's green light on the prose.** Nothing else on the room itself.
- **`teacher.html` still says "DJ deposit" in two `clueMap` labels.** The teacher page is on the
  contract's DO NOT TOUCH list so it has been left alone; the fix is two display strings and wants
  Jon's word. There is a larger problem in the same file — see §8.

## 5c. The unrewritten rooms are withdrawn from the live site

**TWO REMAIN WITHDRAWN as of 15/09/2026** — IT Vengeance and Car Trap.
Canteen Menu Hack came back up on 12/09, Heatwave Mutiny on 13/09 and Rugby Mud on 15/09; it was five, it is now two.

**Jon's call, 08/09/2026: release room by room.** The three rewritten rooms went live that day and
the other five came down until their turn comes. The reason is the feedback in §1 — leaving rooms
up in the voice a teacher called unusable undoes the point of fixing the others.

**They were not deleted, and nothing was lost.** All of them have been live and indexed since 01/09,
and the standing rule in this project is that an indexed path is not traded for tidiness while the
domain is still earning trust. So each of the five keeps its URL and serves a **noindex holding
page** saying the room is being rewritten and pointing back at the hub. No 404s, nothing crawlable,
and nobody can reach the un-rewritten prose. `room.js`, the teacher data block and every image are
untouched on disk — only `index.html` and `teacher.html` were replaced, and each holding page
carries the restore commands in an HTML comment.

**What came down with them:**

| Where | What changed |
|---|---|
| `escape-rooms/index.html` | room cards removed; "Eight narrative rooms" → the live count, plus a line saying more are coming; meta and og: descriptions |
| `index.html` (front page) | `.esc-card`s removed; band lede; "Open all eight rooms" → the live count; both meta descriptions |
| `sitemap.xml` | `<url>` entries removed; the hub and the live rooms stay |

**The replay statistics on the hub are computed from what is live and go stale silently.** Across
eight rooms they were "193 verified number sets and just over 4,000 combinations". Across the three
live on 08/09 they were 74 sets and 1,500 combinations. **Across the four live now they are 104
verified number sets and just over 2,500 combinations, from 400 in the prom office to 1,000 in the
canteen.** **Recompute these every time a room is released, from the room files** — do not add to
the previous figure. Releasing the canteen also moved the top of the *range*, because at 1,000
combinations it displaced the P.E. store, so the sentence named the wrong room as the maximum until
it was recomputed. Per-room counts as of 12/09: hamster 23 sets / 420, P.E. 27 / 720, prom 24 /
400, canteen 30 / 1,000. **Five live as of 13/09: 125 sets, 2,840 combinations ("over 2,800"),
heatwave 21 / 300 — which became the new MINIMUM of the range**, so the sentence now runs "from 300 in
the heatwave classroom to 1,000 in the canteen". **Six live as of 15/09: 149 sets, 3,290 combinations
("over 3,200"), rugby 24 / 450. Seven live as of 17/09: 172 sets, 3,650 combinations ("over 3,600"),
comic caper 23 / 360; the range is unchanged.** **Since `0907f6e` the engine only serves VALID draws
(§8), and those total 2,064 across the seven** — hamster 314, P.E. 248, heatwave 220, prom 342, canteen
600, rugby 156, comic 184 — so the hub's 3,600 and its 300–1,000 range describe combinations that are
never all served. **Settled 17/09 by Jon: the hub quotes no figure at all.** The sentence "Across the
seven rooms that is… to 1,000 in the canteen" was deleted, not updated, because it had gone stale twice
and any total or range needs recomputing whenever a room or lock changes. A suggested replacement, "no
two groups get the same room", was also dropped: each device draws independently, so at rugby's 156
VALID draws ten groups have about a 1 in 4 chance that two match, and the checker's floor is 20.
**Everything above in this paragraph is history — do not put a figure back.**

**The count appears in six places and one of them is a trap:** the front page uses the *same
string* for `meta name="description"` and `og:description`, so a single-occurrence replace fails
there. Grep for the old number, expect two hits on the front page, and change both.

**Releasing a room is therefore now part of finishing it.** On top of everything in §10, a room's
session must also:

1. Write its real `index.html` and `teacher.html` back (the rewrite writes a fresh `index.html`
   anyway, because the meta, og: and Twitter copy all carry the premise).
2. Add its card back to `escape-rooms/index.html` **and** the front-page band in `index.html`.
3. Add its `<url>` back to `sitemap.xml`.
4. Bump the room count everywhere. **Grep for the current count word — `seven` as of 17/09** (it was `three` when this was written) — it appears in both meta descriptions of
   the front page, the band lede, the "Open all three rooms" button, the hub lede, and the hub's
   meta and og: descriptions.
5. Nothing to recompute on the hub: it quotes no sets/combinations figure since 17/09 (see above).
6. `check-escape-rooms.py` reports a VALID variant 0 and at least 20 VALID combinations for this room.

**One stale-copy bug was found doing this and is fixed.** The hamster room's card on the hub still
sold the *rejected* premise — fifteen minutes of tea break to swap the hamster for a stuffed toy,
the version that made the students thieves — and its `alt` still described the old boiler-room
picture rather than the science prep room that is actually on disk. Room one's rewrite updated
`room.js` and the room's own `index.html` and missed both. **Check the hub card and the front-page
card as well as the room's own page**; §10 now lists this.

## 5e. Canteen Menu Hack — what is written and what is outstanding

**Written 12/09/2026.** Antagonist is **Ms Cinnamon**, the home economics teacher: vegan, animal
rights activist, respected by students, and this is the step too far. Jon's interview answers gave
the character and, crucially, the premise correction.

**The premise moved, as §3 predicts it will.** The room read as three students defeating a vegan and
getting the meat and cheese back, which made the students the villains of a cause and broke the
standing rule that they win by putting something right. The win no longer removes the kale; the
board ends the room carrying both, at prices a person can pay, which is the argument she should have
made at seven o'clock instead of acting overnight. The room is not about veganism. It is about
having the choice taken away without being asked.

**The step too far is the frame, not the kale — and the first draft got this backwards.** CC wrote
Cinnamon as ready to put her hand up and take the blame herself, which made her noble and the room
toothless. Jon's correction, 12/09: **she was laying the blame on the catering manager.** She set
Healthy Week up at seven o'clock on the manager's till, under the manager's administrator login, and
left it standing in the manager's name. That is what a respected teacher does not do, and it is the
whole reason the room exists.

**It is also what makes the clock real.** The manager will disprove it — she was not in the building
at seven and she can show it — and the moment she does, the question stops being about kale and
becomes about who used her account, with exactly one answer. Healthy Week would only have cost
Cinnamon an argument; letting somebody else carry it is the thing there is no coming back from in a
school. So the students roll the morning back before the bell: nothing to sign off, nothing to
disprove, no printout, no investigation. **They are saving the manager from carrying it and Cinnamon
from what she has already done, and she never finds out.** The win's last line is "She will never
know how close it was."

**Do not re-soften her.** If a later pass has her owning up or standing by it, that is the wrong
draft coming back. The `room.js` header carries the warning.

**Three things a cold read caught, 12/09/2026, all fixed:**

- **The login symmetry.** The students run all three locks on the same administrator session
  Cinnamon used, so mechanically they do the exact thing the room frames as the unforgivable act.
  The win text did not answer that — it said no printout, nothing to disprove, no question about
  whose login was open, which is *getting away with it* rather than *being different*. The answer is
  now in the **brief**, where it reframes every action that follows: everything on their list puts
  something back rather than sets something up, an entry goes in somebody's name and a reversal
  leaves nothing in anybody's. That clause is load-bearing and is flagged as such in the `room.js`
  header. This is now a standing rule for the set — see §4.
- **The stakes were the risk, not the monologue.** They ran to a four-step chain — minutes, her
  name, she disproves it, the question becomes whose login — and three Year 9s round a screen with a
  clock running will skim it. Compare Lungey's: six kilometres, sideways rain, kit not dry by
  Thursday. Instant. **Cut to two sentences**, and the monologue carries the rest. If a moral turn
  ever goes missing in one of these rooms, suspect the setup nobody read before suspecting the
  writing.
- **The name.** Ms Cinnamon is food-adjacent on a food teacher, which is the note that killed Mr
  Shuttlecock. Kept deliberately: every antagonist in the set is already an aptronym — Beaker in
  science, Lunge in P.E., D Tension the headteacher — so a name that comments on its owner is the
  house convention here rather than an exception, and Cinnamon is the mildest of the four and the
  most plausible as a real surname. Jon's to overrule.

**What the review singled out as working:** the suggestions box. Thirty-eight slips saying "chips",
one saying "chips please", and the food bank note with "yes" written under it in green pen. The
green pen is her, it is on a blank object most players never open, and it is why the frame lands —
she is established as a good person in one detail, so the thing she has done reads as a fall rather
than a character.

**Her voice is the monologue.** She never appears and never speaks to the players. The four
`wrongLines` are her going at full flow through the serving hatch from her room across the corridor,
at a Year 8 who went in to ask whether there was anything at lunch that was not kale and has not
been released. Line four repeats for the rest of the game, which is the joke: "She has started again
from the beginning."

Line four is where the frame shows without her ever admitting it: *"If that costs somebody an
awkward afternoon then I am sorry for it, I am. But they did not write the contract either, and they
will understand that."* She has decided, on someone else's behalf, that they will understand. She
has not asked them. That is the character in one sentence, and it is the line that had to be
rewritten when the blame direction was corrected.

**The £5 cookie was the §8 hardcoded-number fault, and it was live.** The figure sat in the hook,
the stakes, the till lock's `onOpen` and both alt texts, while the till lock draws last term's
cookie baseline from a library running £1–£7. In one variant the two matched exactly; in another the
baseline was £7, so Healthy Week had made the cookie *cheaper*. **It is now £8.40** — above every
drawn baseline, and unrounded because she costed it rather than picked it. The constraint is written
into the `room.js` header because any future edit to that figure has to clear the same bar. Verified
in a play that drew the £7 variant.

**Verified in a browser, not by reading:** all four `wrongLines` in order with the last repeating;
all three lock briefs opened and read (none carried stale premise — the P.E. sprinkler fault does
not recur here); the named misconception firing with its own response; the room solved to the win
screen; and **one `.webp` request for the whole room with all three locks open** — the scene, so the
instrument-art drop is clean.

**No maths moved, and it was proved rather than eyeballed.** Every `id`, `key`, `instrument`,
`variants`, `missTitle`, `missSays`, `hints` and `solve` was extracted from HEAD and from the
working tree and compared: 25 protected fields, identical sha256.

**NOTHING IS OUTSTANDING. All three pictures are filed** in the new empty-room style at 1600×873,
none carrying a watermark, and all three were checked on screen under the right text. **Released and
pushed as `49c02d8`** and verified on the live site, not only locally.

**Two traps the release step caught, both of which would have shipped:**

- **The hub and front-page cards had to be written fresh, not restored from git.** The old hub card
  still sold the rejected premise — "put the cookie up to £5… get pizza back on the menu" — and its
  `alt` described a HEALTHY WEEK chalkboard that is not in the new picture. That is exactly the
  hamster-card bug §5c records, and `git show`-ing the card back would have reproduced it on the
  most-visited page in the set. **Restoring a withdrawn room's cards is always wrong after a
  premise change.**
- **The image labels arrived swapped.** Jon labelled the pizza/receipt picture "fail" and the
  kale/cookie picture "win"; the content said the opposite, unambiguously — the receipt coiled on
  the floor is in `winAlt` and the cookie under the dome on a doily is in `failAlt`. Filed by
  content and flagged. **Check what a picture shows against its alt text before filing it, whatever
  the file is called or labelled.**

`canteen scene.jpg` in Downloads is NOT a candidate for this room: it is the old-style heatwave
picture, full of figures and garbled signage.

## 5f. Rugby Mud Bath — what is written and what is outstanding

**Written 15/09/2026.** Jon settled the §7 premise in conversation before the room was read. The
Geography teacher, the betting rival coach and the elbow-patch vandalism are all gone.

**Antagonist: Mr Mower, the groundskeeper.** He loves his grass, would keep every child off every
pitch he looks after, and dreams of a medal at the Chelsea Flower Show. **He acts on Mr Lunge's
orders** — parents' letters about kit coming home under three inches of mud — and it is the one order
he has ever been glad of. Lunge is named offstage as the cause and says nothing (§4). His voice is
**overheard through the hut window**, costing up a rare-grass order for his home lawn; a phone call was
ruled out because prom-budget already owns the overheard call. Our lot are the **Year 9 mixed team**;
the girls love the mud even more than the boys.

**Why this is not sabotage** (the brief carries it): a rugby pitch is for playing rugby on, and he has
turned an order about washing into "nobody plays properly on my grass". Retitled **The Rugby Mud Bath**
for the same reason; the slug, the analytics `game_slug` and the save key are unchanged.

**The premise moved on timing, at Jon's prompt.** A pitch cannot be soaked in fifteen minutes, and a
soaked pitch cannot be recovered in a day, so the room is set **the afternoon before**. The flow lock's
numbers were therefore re-read as HOURS (answers 4 to 24), which changed the wording of the unit,
missSays, hints and solve and no number. **A consequence caught while building, not in review:** from
about 3:40, the long draws have the taps still running the next morning, so a Mower on site would
simply turn them off. **He is out the next day until just before kick-off, collecting the grass he is
ordering** — the brief says so, and the win never puts a clock time on when the drains were beaten.

**One scale, a "full soaking"**: his log, the timer and the referee's threshold are all measured in it.
Short of one, the drains win; over it, the pitch is waterlogged and the match is called off, which is
what Mower wants. The dial is labelled **Tap timer**, not Flood timer, because flooding is now a way to
lose (Windows Claude's catch, Jon's yes).

**Ending:** he watches from the touchline, says nothing for eighty minutes, and "Chelsea's in May."
He sees his defeat — not a never-knew ending.

**Proved, not eyeballed:** protected-field diff against HEAD shows exactly the declared wording edits;
`id`, `key`, `variants` and `missTitle` identical on all three locks; object ids identical;
`check-escape-rooms.py` clean.

**All three pictures filed 15/09/2026**, alts written against what is on disk (room.js and hub card).
The win is Jon's `Rugby Open.jpg` after an edit to take **three diagonal brand stripes off the
boots**; the fail is an edit of that, so the pair share one camera. The scene's tap timer has a few
scribbled marks on its face — **left on Jon's call**: about 25px across at 1600px and unreadable.
The scene renders a shade softer and warmer than the doorway pair.

**Powers render as superscripts, Jon's catch on his look (15/09).** The padlock clue printed
`2^H × 4^A = 2^13`. Every caret on that lock — clue, missTitle, missSays, the method hint, solve, and
the teacher page's clueMap label — is now `<sup>`; all of them go through `fill()`, so HTML renders.
Notation only, same indices; checked on screen. "4 = 2²" beside 2<sup>2A</sup> became 2<sup>2</sup>
so the two match. **Then fixed set-wide at Jon's ask:** the generator's `sup()` wrote `^4` for any
index above 3, so `heatwave-mutiny`'s LCM factorisations showed "16 = 2^4". It now writes `<sup>` for
EVERY index, so "2<sup>4</sup>" and "3<sup>2</sup>" match within one factorisation; the re-run moved only
those `factors`/`lcmfactors` tokens (heatwave room.js + variants.json), every other room byte-identical.
A sweep found no other caret anywhere in the set; `²`/`³` in units and single squares (cm², t², x²)
were left as they are, which is correct typography. **Standing rule: no `^` in anything a student reads.**

**Outstanding:** Jon's look at the released page, then commit and push on his say-so.

## 5g. The Comic Caper — built 17/09/2026

**Not a rewrite: a new room**, built from a site user's request for a GCSE maths resit class (grade 3/4).
Wording came from Jon via Project Claude contracts; nothing was drafted without approval.

- **Premise.** Mr Babel's French comics are locked in the old cupboard ("the Chokey") that Estates take
  away at the end of the day. Ms Fromage is outside the door telling a colleague about her cruise — her
  lines are the wrong-entry slot. The blanks carry a joke: *M. Tortue* (her tortoise) is her "emotional
  support reptile" travel buddy, and the itinerary underlines Brest.
- **Locks — batch 6** (`docs/lock-bank-batch6.txt`): number of factors of the asset number (dial 0–20),
  how many volume numbers 1–V are prime (dial 0–30), most identical bundles of grammar books and
  dictionaries (HCF, slider 0–120). Libraries 4 / 9 / 10. **Four clue objects and four blanks**, the HCF
  lock taking its two figures from two objects.
- **Decisions worth not re-deriving.** The factor misconception response no longer says "a factor pair
  short" — that let a student add 2 without finding the pair; it is now "Not every factor is there." The
  dial briefs say what each opens at without quoting a figure. The stock card reads DICTIONARIES (was
  READERS). The primes hint's 1, 2, 3, 5, 7 and 49 are method constants, allowed.
- **`missArt` is forbidden in this room.** The failure picture shows the cupboard gone, which is only true
  at time-out; `room.js` records the rule.
- **Art.** Three pictures from one viewpoint. The first scene was rerolled for lettering ("TRAVEL
  BROCHURE") and a cupboard that did not match the win picture. Accepted: the clock is centred above the
  cupboard in the scene and above-right in fail and win.
- **Cards.** A room card is one link, so the "Built from a site user's request… Let us know" line sits
  directly under the card in the same grid cell, linking to `/feedback/`.
- **Timing.** 3:16, Jon solo — author, knows the methods, not a student baseline.
- **Outstanding:** nothing on this room.

## 5h. Open — pe-shed-rebellion's variant 0 collides

Found by the collision check on 17/09. **Variant 0 of the audited bank locks collides twice:** the pressure
lock's answer, 48 psi, is printed in the sprinkler clue as "48π", and the sprinkler's 12 m reach and the
locker's "day 12" share a figure. The engine never serves that draw, and the checker only warns, so
nothing a student sees is wrong. **It is a content defect in the bank locks and needs its own contract**
(the audited variant 0 has to move, which touches the bank, the generator and the teacher page's example).
The two withdrawn rooms also have invalid variant-0 draws; handle them in their own rewrites.

## 5i. The Kiln Disaster — built 17/09/2026

**The first room built to a written contract rather than an interview.** Jon and Project Claude settled the
premise, the prose and the approved alt text in advance; this session built the locks (bank batch 7), then the
room against them. There is no antagonist: **Mr Stephen Mudge, who teaches Art and has been Smudgey since about
his first week, is an ally**, and the pressure is the
kiln's own countdown. That is a departure from the rule that a room needs an obstacle with a face, and it
works because the countdown can reach the students during play, which is what §3 actually asks for.

**The maths:** multiples (the highest sensor ID under a network limit), LCM (two fan cycles restarting
together) and order of operations (the cancel code). GCSE resit, grade 3/4, nothing above 99, no calculator.
The locks are bank batch 7; the libraries hold 10, 7 and 10 sets.

**Not one numeral is typed into a clue string.** The VALID-draw count was measured at 320 before `room.js`
existed, from the bank's CLUE lines alone; a literal number written into clue text counts as a clue figure and
would have cut it. The built room reports **320 VALID of 700**, which is how we know nothing slipped in.
Anyone editing this room's clues should re-run `check-escape-rooms.py` and expect that number back.

**The site's first two-digit keypad** (`digits: 2`). Every answer and misconception in that lock's library is
two digits, so there is no leading-zero case. The engine needed no change.

**The hook was fixed after release** (`7b29150`): it opened by calling him Smudgey before anyone had been
told who that was. He is **Mr Stephen Mudge, who teaches Art**, Smudgey since about his first week, and the
introduction now carries the joke instead of assuming it. Jon's two approved sentences follow it unchanged.

**Left open, none of it blocking:** `teacher.html` never names him, so a teacher opening it cold meets a
nickname; the notes do not mention that a group making only named mistakes skips some of his lines; and one
drawn variant reads `2 + 48 ÷ 2`, where the starting number is small enough that the sum is nearly all
division. All three are Jon's call, not defects.

**Render-tested locally** on `serve-stubbed.py`: all three locks opened on variant 0 and on a second draw,
each misconception showed its response with no picture, the four wrong-entry lines appeared in order, the
time-out screen showed the failure picture above the stakes line, the win screen showed the victory picture,
and the teacher page followed the live draw. **Misconceptions count as wrong entries**, so they advance the
wrong-line ladder — worth knowing when testing the lines in order.

## 6. Art — what changed in September

Jon has redrawn all eight establishing shots in a new style: hand-drawn cartoon, visible ink
linework of uneven weight, flat colour with limited cel shading, muted desaturated palette, one
dominant light source. They are **empty rooms with no people and no lettering**, which is a
deliberate change — figures are where the generation fails, and an empty room carries no text to
garble.

**Each room now needs three pictures, not six:** scene, failure, victory. The instrument art is
dropped; the engine draws the live control anyway. **The failure picture is not optional** — it
fires on the lock's one named misconception, which is a designed mechanic, not decoration.

The style block to paste at the top of every prompt:

> Hand-drawn cartoon illustration, visible ink linework with slightly uneven weight, flat colour
> fills with limited cel-shading, muted desaturated palette, single dominant light source, slight
> perspective distortion. British secondary school setting, contemporary, mundane and specific.
> Empty room, no people, no figures. No text, no signage, no numbers, no logos.

**Judging rules:** visible linework or bin it; any figure, text or lettering and bin it; and lay it
beside the other scene images before accepting — it has to look like the same hand.

**Filing is one command**, and it must be run on every image:

```
python scripts/strip-gen-watermark.py --width 1600 "in.png" docs/art/<slug>-<kind>.webp
```

House frame is **1600×873 WebP q80**.

**No art field, no request (contract ART-PENDING, 10 Oct 2026).** Art comes after the room is settled, so a
room is built and played before its pictures exist. Until they are filed, its `room.js` has **no top-level
`art:` field**: the engine then emits no scene, fail or win `<img>` and requests nothing (the same rule as a lock
with no `art`, canon §11.3), the teacher page does not mention the mid-game failure picture, and
`check-escape-rooms.py` lists the room as "art pending". Add `art: '<slug>'` in the same PR that files the three
pictures. Never name art that is not drawn: a named picture that is missing 404s, and check-site's tier 1 fails
the page. The room's hub card in `escape-rooms/index.html` writes its own `<img>`: leave it out until the art lands.
`scripts/test-escape-art.py` checks both halves.

## 7. Open decisions Jon still owns

**Three of the eight new scene images do not match their room.** These need the premise
conversation before their rewrite session, not during it:

- **Rugby Mud Sabotage** — the new image shows an *already ruined* pitch. The room's premise is
  that you have to ruin it. The picture is the ending, not the beginning. Jon has agreed a re-gen.
- **Headteacher's Car Trap** — the new image is a corridor with lockers and a cleaner's trolley.
  The room is set in an underground car park with a barrier and a charging post. No relationship at
  all.
- **IT Teacher's Vengeance** — softer version of the same. The new image is a server room, which
  suits the IT teacher, but two of his three locks are a vaulting horse and gym mats. Picture and
  puzzles are now in different buildings.

**Car Trap has lost its antagonist.** Mr D Tension is the headteacher, and as of 08/09/2026 he
speaks in `prom-budget`. The standing rule in §4 is that a character may recur offstage but speaks
only in their own room, so `car-trap` — which is *about* him and his sports car — needs either a
different voice (a site manager, a deputy, whoever loses their bay) or a reason its antagonist is
not the head at all. That conversation has to happen before its session, on top of the image clash
above. He is already named offstage in `prom-budget`'s header so the continuity is recorded.

**Escalating wrong-entry is written but not wired.** See §8. *(Wired 2026-09-08 — kept here because
§8 records the decision behind it.)*

## 8. Gotchas — every one of these has already cost time

**`teacher.html` couples to `room.js` by object id.** Its `clueMap` maps clue → lock using the
`id` field of each object in `room.js`. Rename an id while rewriting an object's visible text and
the teacher page silently stops mapping that clue. **Change `name`, `where` and `clue` freely;
never change `id`.** This applies to all eight rooms.

**The wrong-entry line used to be hardcoded. It is not any more — wired 2026-09-08.** Rooms carry a
`wrongLines: [{head, body}, ...]` array and `wrongLine()` in `engine.js` selects from it by
`st.wrongs - 1`, clamped so the last entry repeats for the rest of the game. A room with no array
gets the original fixed string unchanged, which is what the six unconverted rooms run on.

**A misconception hit consumes an index without printing a line, and that is intended** — the
escalation is the cost of getting things wrong, and the player was handed a better and more specific
response instead. Keeping a separate count would need new state and a `SAVE_V` bump, invalidating
every in-progress save to buy something no player can perceive. Written up in `engine.js` so it
reads as a decision.

**The instrument frame is guarded too**: a lock with no `art` emits no `<img>` and makes no request.

**Each lock has its own `brief`, and it carries premise too.** The room-level `hook`/`brief`/
`stakes`/`win` are the obvious slots and it is easy to rewrite all four and think you are finished.
The P.E. sprinkler lock still said "and there will be a dry strip to cross" — the *old* premise —
after every room-level slot had been rewritten, and it was only caught by playing the room in a
browser rather than reading the file. **Open all three locks and read their briefs before calling a
room done.**

**Cross-lock collisions — fixed 17/09/2026 (`0907f6e`).** Libraries are verified lock by lock, but a room
serves one variant per lock together, and independent draws collided — Jon saw ASSET No. 24 beside
DICTIONARIES: 24 while play-testing. `pickVariants()` now draws the room jointly and serves only VALID
draws: no clue figure in two locks' clues, no answer in another lock's clues, no answer equal to another
lock's misconception, no shared answers. Clue figures are every number the student reads in a clue,
including numerals typed into the clue text; the first two rules ignore figures of 2 or less.
`check-escape-rooms.py` applies the same rules, reports every room's VALID count and fails a room under 20.
**The engine and the checker implement the same rules — change them together.** Games saved before the
fix resume with their stored draw, so an old collision can still appear until those games finish.

**`teacher.js` used to tell every room its failure picture appears mid-game.** Only a lock with `missArt`
does that (today only `canteen-hack`), so six teacher pages were wrong. Fixed 17/09 (`215b084`): the
paragraph renders only when a lock sets `missArt`.

**Hub and front-page card images take `onerror="this.remove()"`.** A room released before its art exists
shows a card with no picture instead of a broken-image icon. Keep the attribute on every new card.

**Dropping the instrument art leaves the engine emitting a frame anyway.** `engine.js` line 303
writes an instrument `<img>` unconditionally, so a lock with no `art` field requests
`undefined.webp`, 404s, and `mfgArtFallback` removes the frame. Correct and silent on screen, one
dead request per lock in the network log. The guard is two lines and belongs with the `wrongLines`
wiring in a shared-engine job, not in a room's session.

**A hardcoded figure in prose contradicts a drawn variant, and it reads fine until it doesn't.**
The prom hook said "the entire £5,000 prom budget" while the invoice on screen draws one of ten
totals ranging £1,812 to £8,470. It survived a build and a review because the sentence is not
wrong in isolation — it only breaks when the drawn number differs, which is nine plays in ten.
**Grep each remaining room for bare amounts, counts and percentages in its prose before rewriting
it**, rather than finding them one room at a time. Jon's call, 08/09/2026, and it applies to all
five rooms left.

**The same bug is live in `teacher.html`, and is NOT fixed.** Its `clueMap` values are literal
strings — `teacher.js` does not pass them through `fill()` — and prom-budget's name specific
numbers from the *first* variant: "£2160 including the 20% levy", "£1000 at 10% compound",
"£1610.51". The page draws its own variant for everything else, so those three labels disagree with
the rest of the page most of the time. **The teacher answer page is on the contract's DO NOT TOUCH
list and has been left alone.** Worth checking across all eight rooms and fixing in one deliberate
pass with Jon's say-so, not in passing during a voice rewrite.

**Object and lock `name` and `where` go through `esc()`, so an HTML entity in one renders
literally.** `engine.js` escapes `&` in those fields before writing them into the object list and the
lock buttons, so `name: 'Mr Beaker&rsquo;s mug'` displayed the raw `&rsquo;` on screen for a week.
The clue, flavour and every narrative slot go through `fill()` instead and DO render entities, which
is why this is easy to miss — the same file wants `&rsquo;` in one field and a real `’` in the next.
**Use real characters in `name` and `where`.** Caught by Jon 2026-09-08; one instance across all
eight rooms, now fixed. Grep for it: `grep -nE "(name|where): '[^']*&[a-z]+;" escape-rooms/*/room.js`

**Prose and maths are coupled through `{{key.token}}`.** Every figure in the text is filled at run
time from the drawn variant. Rewrite *around* the tokens; deleting one fails
`check-escape-rooms.py`. Never hand-edit a `variants:` block.

**Alt text and pictures drift.** `winAlt` and `failAlt` describe pictures. If the prose changes and
the art has not been redrawn yet, the room will show the old picture under new text — this is the
exact bug Jon hit in September, when winning the P.E. room showed the shed in the rain. **Do not
ship prose and picture that disagree.** Sequence the art immediately after the rewrite.

**SEO copy lives in `index.html` and goes stale silently.** The room's meta description, og:
description and Twitter card all repeat the premise. The hamster room shipped for a week telling
Google and every link preview that "the caretaker has confiscated the class hamster", which was
wrong on the premise *and* the character. **Check `index.html` whenever a premise changes.** Keep
it to 150–160 characters per `canon.md`.

**PNG downloads carry a generator watermark.** Gemini stamps a four-pointed sparkle into the
bottom-right corner of PNG downloads. Nothing already on the site has one — the 53 filed images
and every JPG download are clean — but it arrived with a generator change and it is on every PNG
from September 2026 onwards. Given *why* this whole pass exists, shipping one would be
unforgivable. `scripts/strip-gen-watermark.py` removes it and is a no-op on a clean image, so run
it on everything.

## 9. The reference implementation

`escape-rooms/hamster-heist/room.js` is the room to copy the shape from. Worth reading for:

- **`hook` / `brief` / `stakes` / `win`** — the four narrative slots, in a settled voice.
- **`wrongLines`** — Mr Beaker asleep in the store room, arguing the hull-first horizon proof with
  a colleague who retired in 1994, getting nowhere and never waking. The penalty has a face without
  the antagonist ever entering the room.
- **The objects** — six clue-carriers and two blanks. The blanks earn their place: a solar system
  model with Pluto glued back on by hand, more than once, is the character in one object.
- **The offstage cause** — Lungey confiscated the hamster and is named for it in two sentences,
  without speaking.

What was deliberately left alone: every lock `id`, `key`, `instrument`, `variants`, `missTitle`,
`missSays`, `hints` and `solve`. **No maths moved.** The rewrite is text, and the checker proves it.

---

## 10. Picking up the next room cold

> **Room five is DONE (13/09/2026).** The Heatwave Mutiny notes below are kept as the record. Three
> lessons from it bind rooms six to eight: **(1)** a second-Claude sanity check of the full breakdown,
> before any file is touched, moved the premise twice (trust CEO → energy contractor, "a ridiculous
> individual, not a critique of a system") and cut a failure mode; **(2)** an antagonist's lines must
> stay inside his actual authority — Banks only controls the electricity, so every line about running
> the school had to go; **(3)** when a failure mechanic is dropped, say the engine work it prompted is
> CANCELLED, not deferred, or it sits in a queue. **Next room: none is openable cold — have the §7
> conversation with Jon first.**

**Room five was The Heatwave Mutiny (`heatwave-mutiny`).** Read §2 and §4 first; this section only
confirms the choice and lists the traps that are now standing.

### Which room

**Heatwave Mutiny is the only one openable cold.** Its new establishing shot maps onto its existing
premise, so the session can go straight to the read-then-interview method. Canteen Menu Hack was the
other and was taken on 12/09/2026 — see §5e.

**Expect its premise to move, and say so early.** The heatwave room currently has the students
breaking into a control room and rewiring a failsafe. That is the hamster problem in a different
building: they win by breaking in rather than by putting something right. Surface it in the
interview, not after the prose is written — that is twice now that the read found the premise fault
before the character work did.

**It must not end on the adult never finding out.** Two of the four finished rooms already do —
Test Tube Dave ticks his box, Cinnamon never knows how close it was — while Lungey and Tension both
see their defeat. See the rule in §4. If the premise genuinely supports nothing else, say so to Jon
rather than writing a third one quietly.

**Three are not openable cold.** Do not open Rugby Mud, IT Vengeance or Car Trap without the §7
conversation first — all three have a scene image that does not match the room, and Car Trap has
additionally lost its antagonist to room three, because the headteacher speaks in `prom-budget`
now.

### Do this before you type anything to Jon

Read the room's `room.js` end to end, plus its `index.html` and `teacher.html`. Do not ask him a
single question until you can describe the room back to him. All three finished rooms went better
for it, and in two of the three the read is what surfaced the premise fault.

### What every room from here gets

1. **`wrongLines` works** — four entries, last repeating, indexed by `st.wrongs - 1`. Verify it by
   playing the room, not by reading the file.
2. **Instrument art is dropped set-wide.** Remove every lock's `art`/`artAlt` pair; the engine draws
   the live control and emits no element at all when there is no art.
3. **Three pictures, not six** — scene, failure, victory. The failure picture is not optional.
4. **The establishing shot is probably already on disk.** All eight are in the local Downloads folder (path in `CLAUDE.local.md`)
   under their own names — `heatwave open.jpg`, `Canteen Open.jpg`, `Rugby Open.jpg`, `it open.jpg`,
   `head teacher open.jpg`. **Look there before asking Jon for it.** They are JPGs, so they carry no
   watermark, and they are already 2816x1536, so `--width 1600` alone files them.

### Before you call it done

Every one of these has cost time on a finished room:

- **Grep the prose for hardcoded numbers first.** `£5,000` in the prom hook contradicted a drawn
  invoice nine plays in ten and read perfectly well in isolation. See §8 — Jon asked for this to be
  a per-room check rather than a discovery.
- **Open all three locks in a browser and read their briefs.** Each lock's `brief` carries premise.
  The P.E. sprinkler still argued the old premise after every room-level slot had been rewritten.
- **Check THREE places for premise copy, not one:** the room's own `index.html` (meta, og: and
  Twitter), its card in `escape-rooms/index.html`, and its card in the front-page band in
  `index.html`. All of them repeat the premise and all of them go stale silently — the hamster
  room's hub card was still selling its rejected premise a day after the room was rewritten.
  150–160 characters per `canon.md`, and lift card `alt` text verbatim from `room.js`.
- **Re-release the room**, which is now a step of its own — see §5c for the five files it
  touches and the counts that have to move with it.
- **Never change an object `id`** — `teacher.html` maps clues to locks by it.
- **Do not ship prose and picture that disagree.** Sequence the art immediately after the prose, and
  if the pictures cannot be drawn in the session, say so in the `room.js` header the way
  `prom-budget` does.
- **Run `python scripts/check-escape-rooms.py`**, and prove no maths moved by diffing every lock's
  `id`, `key`, `instrument`, `variants`, `missTitle`, `missSays`, `hints` and `solve` against
  `HEAD` — not by eye.
- **Check `git status` at the start of the session.** See the box at the top of this file.

### Playing a room locally

`file://` is blocked for the browser tooling. Serve the repo instead and drive it from
`127.0.0.1`:

```
python -m http.server 8765 --bind 127.0.0.1
```

Then `http://127.0.0.1:8765/escape-rooms/<slug>/`. Wrong-entry escalation can be exercised by
submitting a value that is neither the answer nor the lock's named `miss` — a misconception hit
consumes an index without printing a line, so it will mislead you if you use it.
