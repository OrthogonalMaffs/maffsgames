# The Rightful King: draft for Jon’s review

**Phase 1 of the replacement for the withdrawn `it-vengeance` room (contract RIGHTFUL-KING-DRAFT, 9 Oct 2026,
18:10; saved as `docs/history/contracts/2026-10-09-rightful-king-draft.md`).** This is draft prose only. Nothing
served is touched: `escape-rooms/it-vengeance/` stays as it is, behind its holding page. Phase 2 (slug, build,
variants, teacher page, retiring the old six pictures, release) and phase 3 (art) are separate contracts after
you approve this.

How to read it:

- `{{key.token}}` is a figure filled from the drawn variant. The prose has no other figures. Times are written
  in words ("fifteen minutes", "half past three"), as in Prom Budget and Kiln.
- Prose is shown with real quotation marks and apostrophes. In phase 2 they become entities (`&rsquo;` and so on)
  in every slot except the object and lock `name` and `where`, which are escaped and keep real characters
  (canon §11.3).
- **[X]** marks a detail I extrapolated rather than took from your brief. Strike any you don’t want.
- Your brief (the contract, and `docs/handover/contracts/2026-10-09-it-room-brief.md`) is followed throughout.
  Narry’s opening line and his prompt are quoted verbatim.

---

## For Jon: decisions in this draft

1. **There is no `fail` slot in `room.js`.** The engine shows `stakes` twice: on the start screen after "If you
   get it wrong." (`engine.js:244`), and on the time-out screen after "And so:" (`engine.js:797`). So your Fail
   (the bully crowned on a frightened vote) is written into `stakes`, and it reads correctly after both lead-ins.
   This follows the Car Trap draft.
2. **`hook`, `brief`, `stakes` and `win` can’t carry tokens.** The engine writes them raw, not through `fill()`.
   That is why the passcode, the overwrite rate and the vote totals appear only in clues, lock briefs, hints and
   solves.
3. **Lock 1 (the passcode): your four example sets don’t fit a three-digit keypad.** The engine won’t accept
   fewer digits than the keypad has. Its message is "Not enough digits. The keypad wants all 3 of them."
   (`engine.js:610`). So 60, 24 and 42 would have to be keyed as 060, 024 and 042, and Kiln’s keypad was built
   to avoid a leading zero. The generator also rejects 24 and 42 outright, because an answer must be clear of the
   ends of the instrument’s range (`keep()`, 4%).
   - The only sets where the answer and the misconception (kᴸ) are both three digits, with L at least three, are
     **k = 6, 7, 8, 9 with L = 3**: 120, 210, 336, 504. **That is a library of four** (k = 5, L = 4 also gives
     120, so the generator keeps only one of the two).
   - **For you:** four variants (my recommendation), or allow a leading zero (adds only k = 5, L = 3 → 060; the
     rest fail the end-of-range rule), or add L = 2 on large pads (k = 11 to 31, e.g. 17 keys → 272). I
     recommend against L = 2. With two keys it is barely the product rule, and it sits below ★★★.
   - **The cause is shared, not this lock’s.** The engine’s keypad takes exactly `digits` digits. The Library
     draft hits the same limit harder: its fines lock needs a two-digit answer and a four-digit misconception
     on one keypad. The fix belongs in the engine: an opt-in keypad that accepts *up to* `digits`, existing
     rooms unchanged. That is a home-lane change to shared code, not this draft’s, and the Library draft
     recommends it. With it, this lock could also take k = 5, L = 3 (60, miss 125).
4. **Variant 0 had to change on lock 1.** Your lead sets for locks 1 and 3 collide. k = 6, L = 3 gives 120, and
   your first audit set has 120 voters printed in its clue, which breaks the joint-draw rule that no answer
   appears in another lock’s clue. I lead lock 1 with **k = 7, L = 3 → 210 (miss 343)**. With it the variant-0
   draw is VALID.
5. **Lock 2 (the overwrite): four of the eight verified sets let the misconception score as right.** Your
   misconception is ⌈(1 − f) × 100 ÷ r⌉. When r divides (1 − f) × 100 exactly, the linear model lands **exactly
   on** f at that minute, not below it. A student reasoning linearly and strictly ("fewer than") then gives one
   minute more. For **r = 25, f = ½** that is 3, which is the right answer: the lock would mark the wrong method
   right. The four sets are 10 ½, 25 ½, 15 ¼ and 25 ¼, and all four have that ambiguity (one of them scores the
   misconception as correct). **I propose one more rejection rule: (1 − f) × 100 is not a multiple of r.** Your
   other four sets pass it and all four answers check (scratch run, exact fractions).
6. **Lock 2’s library uses whole-number rates from 5% to 40%, not only multiples of five.** With multiples of
   five and the rule above, only five distinct answers survive (3, 4, 5, 7, 14). With any whole-number rate the
   library is ten. Either way **this lock needs a calculator** (0.91⁸ is not mental arithmetic), which a ★★★ room
   can expect. Phase 2’s teacher page should say so. **For you:** whole-number rates (my recommendation), or
   multiples of five and a library of five.
7. **Lock 3 (the audit): one of your three verified sets prints its own answer.** 150, 70, 50, 60 gives 60%, and
   "neither" is 60 in the same clue. The generator rejects that (`keep()`: "answer is printed in its own
   clue"). Another, 200, 90, 60, 80, passes the rules but barely carries the story. Of those who saw the page
   50% voted for him; of those who didn’t, 43%. The audit is meant to *show* the leak changed the result
   (your brief: "The re-vote opens only once the audit shows the leak changed the result").
   - **I propose story rules for the generator:** he has 30–60% of the votes (a plausible leader), 20–60% of
     voters saw the page, and P(voted for him | saw it) is at least twenty points above P(voted for him | didn’t).
   - I also require the four clue figures to differ, and S ≠ 100, because dividing by 100 does nothing.
   - Your first set passes all of these and stays variant 0.
8. **All three old locks go, not two.** The contract’s ROOT CAUSE says "two of its three locks are being
   replaced", but EXACT CHANGE specifies three new locks (passcode, overwrite, audit), and the brief’s lock list
   has no mat lock. The draft follows EXACT CHANGE: `mat-tiling-hcf` leaves the room too, with
   `mechanical-keyboard-perms` and `vault-trajectory-vertex`. Their bank entries and libraries stay as history,
   as Car Trap’s `visitor-space-bounds` did.
9. **Why Narry can’t just log in [X].** He never knew his passcode: he let the AI choose it, and the only thing
   he wrote down is the rule it follows. That is his flaw again, and it is why the guard has to be answered rather
   than typed past. Strike it if you have a better reason.
10. **When the result goes up [X].** At half past three, on every screen in the school, with a crown and a drum
    roll the AI added because the prompt asked for a pop concert. That is the countdown. UK schools finish at
    3:30 (working doc §4), so the announcement is the end of the day.
11. **How the win lands [X].** The fresh vote runs overnight with the ballot secret, and the result goes up at
    registration the next morning. Narry’s last lines own it ("It was my prompt"). Then he writes a new prompt by
    hand whose first line is a question he should have asked first. That is the lesson shown, not stated: AI as
    a tool, thinking first.
12. **The bully [X].** He is "a boy in the year who knew where to look" and nothing else: no name, no looks, no
    type. One clause says he made sure people knew he was looking, because otherwise nothing explains why they
    were frightened. He is never on stage and is not mentioned in the win: he simply doesn’t win. Strike the
    clause if it says too much.
13. **The audit uses totals only.** The students never open the leaky page or look at a single ballot. The brief
    says so, the audit object says so, and the lock brief says so. That is how the room answers the rule "if
    the students use the antagonist’s method, say why it is different": the leak shows names, and the audit counts.
14. **`prom-budget` read in full; nothing contradicts the premise.** It never mentions a vote, a king, a
    ballot or Mr Narry. Its one IT detail is an "IT department note" about the network filter, which fits a
    school with an IT teacher. Its prom is a Friday a week after its own room; this room says only "prom king"
    and never dates itself against it. The Head does not appear or speak here.

---

## Title

The Rightful King

*(Your title, 18:06. **Proposed slug: `rightful-king`**, decided in phase 2. A new slug breaks any shared link
to the withdrawn `it-vengeance`, which is noindex, so the cost is small. Phase 2 also decides what the old URL
serves.)*

## Hook

Mr Brian Narry teaches IT. He loves his job, he likes nearly all of you, and last month he built the online vote
for prom king the way he builds most things now: he asked an AI to do it. His prompt is printed out and pinned to
the corkboard behind his desk, with a gold star on it **[X]**.

He meets you at the door of the IT suite before you are properly through it.

“You have to help me, my coding had a bug, and it’s about to be unrecoverable.”

## Brief

It wasn’t his coding, and it isn’t a bug. The AI did exactly what it was asked. The voting screen is a
pop-concert stage, all neon and sparkles, and it looks amazing. Nobody asked for the vote to be secret, so it
isn’t: anyone who knows where to look can see who voted for whom.

One boy in the year knew where to look, and made sure people knew he was looking **[X]**. A lot of them voted for
him. The kindest boy in the year would have won a free vote.

The result goes up on every screen in the school at half past three, with a crown and a drum roll. That is your
fifteen minutes.

Nobody in this room changes a vote, his or anyone else’s. You are going to close the leak, save the vote log
before it is overwritten, and prove from the totals that the leak changed the result, so a fresh vote opens with
the ballot secret again. Then everyone can vote for whoever they like. The audit counts; it never names anyone.

Every wrong setting costs you time, and Mr Narry’s hand keeps drifting back towards the chat window.

## Stakes (also the fail screen; see "For Jon" 1)

At half past three the drum roll plays on every screen in the school, the crown comes down, and his name goes up
under it in neon. The year group claps, because everyone can see who is clapping. Mr Narry watches it from the
back of the IT suite, and for once he doesn’t reach for the keyboard. There is nothing left to ask it.

*(Read after "If you get it wrong." on the start screen and after "And so:" on the time-out screen; both work.)*

## Win

The leak page is gone, the old log is safe, and the audit is on the Head’s desk in one line of totals **[X]**. The
fresh vote runs overnight. Nobody can see anybody’s ballot, and this time nobody tries.

At registration the drum roll plays, the crown comes down, and the name under it is the kindest boy in the year.
He looks round as though somebody has made a mistake. Nobody has.

Mr Narry takes his prompt down off the corkboard and peels the gold star off it.

“It wasn’t a bug,” he says. “And it wasn’t my coding. It did exactly what I asked it to.” He turns the sheet
over. “It was my prompt.”

He writes a new one on the back, by hand, slowly. The first line is a question: *who should be able to see the
votes?* **[X]**

*(The Head is mentioned once, offstage, as the person the audit goes to; he does not speak. Strike "on the Head’s
desk" if you would rather he were not in the room at all.)*

---

## wrongLines (four, escalating; the last repeats)

Each `head` is the room’s reaction; each `body` is Narry. He reaches for the AI and stops himself, a little
harder each time. None of them mentions the students or their answer.

1. **head:** A burst of sparkles, and the setting clears.
   **body:** Mr Narry’s hand goes to the chat window. “I’ll just ask it what we— no. No. That’s how we got
   here.”
2. **head:** The screen flashes and resets.
   **body:** He has typed “how do I fix” before he notices, and deletes it a letter at a time. “Habit. Sorry.
   Carry on.”
3. **head:** The setting slides back. The countdown doesn’t care.
   **body:** “I used to do all this on paper, you know. Flowcharts. I had a pencil I liked.” He looks at his hand
   as if the pencil might still be in it.
4. **head:** Another one. The countdown keeps going.
   **body:** He reaches for the keyboard, stops, and puts both hands in his pockets.

*(Line 4 repeating is the point: every time, he chooses not to hand it over.)*

---

## Objects (eight: six clues, two blanks)

All ids are new. Phase 2 writes a new `teacher.html` whose `clueMap` uses them, because every lock is new
("For Jon" 8). No numeral is typed into any clue, so the only clue figures are the tokens (the kiln rule, working
doc §5i).

| # | id | name | where | clue or flavour |
|---|---|---|---|---|
| 1 | `sticky-note` | Sticky note | on the edge of Mr Narry’s monitor | In his handwriting: **ADMIN PASSCODE: {{pc.L}} DIFFERENT KEYS, NEVER THE SAME KEY TWICE.** Under it, underlined twice: “The AI picked it. Ask the AI.” **[X]** |
| 2 | `login-pad` | The admin login | on the big screen, under the sparkles | A pad of **{{pc.k}} keys**, every one a different glittering shape. Under it, in small grey type: too many wrong guesses; reset only by answering the guard. |
| 3 | `server-log` | Server log | scrolling on the monitor inside the server cupboard | OVERWRITE RUNNING. **Each minute, {{ow.r}}% of the original records still left are replaced.** |
| 4 | `audit-policy` | Audit policy | pinned inside the server cupboard door | “A vote can only be audited from its original records. **Once fewer than {{ow.part}} of them survive, the log is unrecoverable.**” |
| 5 | `results-page` | Results page | behind the sparkles, if you scroll down | VOTES CAST: **{{au.N}}**. His name is at the top, with **{{au.V}}** votes. You don’t need to read it twice. |
| 6 | `access-log` | Access log | still warm in the printer tray | A printout of totals, no names. **Opened the ballot page before voting: {{au.S}}. Never opened it and did not vote for him: {{au.neither}}.** |
| 7 | `prompt` | The prompt | pinned to the corkboard, with a gold star on it | *(blank)* One line, printed large: “Make sure the voting screen looks amazing, like a proper pop-concert stage with neon and sparkles, concentrate on aesthetics over all other considerations.” Underneath, in biro: “Nailed it.” **[X: the biro line]** |
| 8 | `stage-screen` | The voting screen | on the big display at the front | *(blank)* Neon, sparkles, a spotlight sweeping an empty stage, and a crown turning slowly over a space where a name will go. It does look amazing. That was the whole brief. |

`{{ow.part}}` is a word ("half" or "a quarter"), so lock 2’s second clue carries no figure. Clue 2’s grey type is
prose, not a figure.

---

## Locks (★★★ Challenge, grades 6–9)

Every lock is new. Proposed ids, keys and instruments; the parameter sets are proposals for
`gen-escape-variants.py`, which this phase does not touch. **Phase 2 also adds a bank batch file**, because
`check-escape-rooms.py` checks every lock against the audited bank. The three entries are drafted at the end of
this section and pass `check-lock-bank.py` in a scratch run.

### Lock 1: the admin login (product rule, grade 6–7)

- **id:** `admin-passcode-product-rule` · **key:** `pc`
- **name:** The admin login
- **brief:** Mr Narry is locked out of his own system. He never knew the passcode; he let the AI choose it. The
  guard lets a new passcode be set only by someone who can tell it exactly how many different passcodes it would
  have to try to be sure of getting in.
- **instrument:** keypad · **digits:** 3 · **label:** PASSCODES TO TRY · **verb:** Enter count
- **hints:**
  1. How many keys could go first? Once one is used, how many are left to go second?
  2. No key is used twice, so each position has one fewer choice than the one before it. Multiply the choices.
  3. {{pc.prod}}: one factor for each of the {{pc.L}} keys in the passcode.
- **missTitle:** That count lets a key be used twice.
- **missSays:** {{pc.miss}} is {{pc.k}} multiplied by itself {{pc.L}} times, which allows the same key again. The
  note says never the same key twice, so every key used leaves one fewer for the next.
- **solve:** {{pc.k}} choices, then one fewer each time: {{pc.prod}} = **{{pc.answer}}**.
- **onOpen:** The guard accepts the count and asks for a new passcode. Mr Narry types one himself, slowly, and
  writes nothing down. Then he takes the ballot page offline. The leak is shut.

| # | k | L | answer | miss (kᴸ) | `prod` token |
|---|---|---|---|---|---|
| 0 | 7 | 3 | 210 | 343 | 7 × 6 × 5 |
| 1 | 6 | 3 | 120 | 216 | 6 × 5 × 4 |
| 2 | 8 | 3 | 336 | 512 | 8 × 7 × 6 |
| 3 | 9 | 3 | 504 | 729 | 9 × 8 × 7 |

Generator rules: keypad (0, 999, 1); answer = k(k−1)…(L factors); miss = kᴸ; **answer and miss both 100 to 999**
(no leading zero; the miss settable); L ≥ 3 ("For Jon" 3). Solver for the uniqueness test: brute-force count of
L-tuples of distinct keys from k, not a restatement.

### Lock 2: the vote log (exponential decay by iteration, grade 7)

- **id:** `vote-log-overwrite` · **key:** `ow`
- **name:** The recovery tool
- **brief:** The overwrite can’t be stopped from here, only outrun. The recovery tool will copy the original
  records out, but it has to be given its deadline: the number of whole minutes until fewer than {{ow.part}} of
  them survive.
- **instrument:** dial · **label:** MINUTES UNTIL UNRECOVERABLE · 1 to 20, step 1, 0 decimals, starts at 1 ·
  **verb:** Set deadline
- **hints:**
  1. Each minute takes {{ow.r}}% of what is *left*, not of what there was at the start, so each minute takes a
     little less than the one before.
  2. Keeping {{ow.keep}}% each minute means multiplying by {{ow.mult}} each minute. Keep multiplying, and count
     the minutes.
  3. Find the first whole minute when {{ow.mult}} to that power is below {{ow.fdec}}.
- **missTitle:** That takes the same amount every minute.
- **missSays:** {{ow.miss}} minutes is what you get if each minute replaced {{ow.r}}% of the *original* records.
  It replaces {{ow.r}}% of what is left, so it slows down, and the records last longer than that.
- **solve:** After n minutes, {{ow.mult}}ⁿ of the records survive. {{ow.mult}}^{{ow.prev}} = {{ow.prevval}} is not yet
  below {{ow.fdec}}; {{ow.mult}}^{{ow.answer}} = {{ow.ansval}} is. **{{ow.answer}} minutes.** *(The powers are
  `<sup>` in phase 2.)*
- **onOpen:** The recovery tool runs ahead of the overwrite and copies every original record into a sealed file.
  Nobody opens it. It only has to exist.

| # | r | f (`part`) | answer | miss | `mult` | before the answer | at the answer |
|---|---|---|---|---|---|---|---|
| 0 | 20% | half | 4 | 3 | 0.8 | 0.8³ = 0.512 | 0.8⁴ = 0.410 |
| 1 | 8% | a quarter | 17 | 10 | 0.92 | 0.92¹⁶ = 0.263 | 0.92¹⁷ = 0.242 |
| 2 | 29% | a quarter | 5 | 3 | 0.71 | 0.71⁴ = 0.254 | 0.71⁵ = 0.180 |
| 3 | 20% | a quarter | 7 | 4 | 0.8 | 0.8⁶ = 0.262 | 0.8⁷ = 0.210 |
| 4 | 7% | half | 10 | 8 | 0.93 | 0.93⁹ = 0.520 | 0.93¹⁰ = 0.484 |
| 5 | 9% | half | 8 | 6 | 0.91 | 0.91⁷ = 0.517 | 0.91⁸ = 0.470 |
| 6 | 40% | a quarter | 3 | 2 | 0.6 | 0.6² = 0.360 | 0.6³ = 0.216 |
| 7 | 11% | a quarter | 12 | 7 | 0.89 | 0.89¹¹ = 0.278 | 0.89¹² = 0.247 |
| 8 | 12% | a quarter | 11 | 7 | 0.88 | 0.88¹⁰ = 0.279 | 0.88¹¹ = 0.245 |
| 9 | 9% | a quarter | 15 | 9 | 0.91 | 0.91¹⁴ = 0.267 | 0.91¹⁵ = 0.243 |

Generator rules: dial (1, 20, 1); r a whole number 5 to 40; f ½ or ¼; answer = smallest n with (1 − r/100)ⁿ < f,
**computed in exact fractions**. Reject:
- answer = miss;
- any exact hit (1 − r/100)ⁿ = f;
- answers of 2 or less;
- **(1 − f) × 100 a multiple of r** (proposed, "For Jon" 5).

Tokens: `keep` (100 − r), `mult`, `fdec` (0.5 or 0.25), `prev` (answer − 1), and `prevval` and `ansval` to three
decimal places. Your four sets that pass the proposed rule (20 ½, 15 ½, 20 ¼, 30 ¼) are all valid; the seeded
search kept 20 ½ and 20 ¼ above.

### Lock 3: the audit (Venn diagram and conditional probability, grade 7–8)

- **id:** `leak-audit-conditional` · **key:** `au`
- **name:** The audit
- **brief:** The fresh vote opens only if the audit shows the leak changed the result. It asks one question: of
  the voters who opened the ballot page before voting, what percentage voted for him? It works from totals only.
  Nobody’s vote gets looked at.
- **instrument:** keypad · **digits:** 2 · **label:** PERCENT OF THOSE WHO SAW IT · **verb:** Enter
- **hints:**
  1. Draw two overlapping circles: voted for him, and opened the page. The voters who did neither go outside
     both.
  2. Everyone inside the circles is {{au.N}} − {{au.neither}}. The two circles added together come to more than
     that, because the overlap gets counted twice.
  3. Find the overlap, then ask what percentage it is of the {{au.S}} who opened the page.
- **missTitle:** That is out of every voter.
- **missSays:** {{au.miss}}% is {{au.both}} out of all {{au.N}} voters. The audit asked about the ones who opened
  the page, so the {{au.both}} is out of {{au.S}}.
- **solve:** Inside the circles: {{au.N}} − {{au.neither}} = {{au.inside}}. Overlap: {{au.V}} + {{au.S}} −
  {{au.inside}} = {{au.both}}. {{au.both}} out of {{au.S}} is **{{au.answer}}%**.
- **onOpen:** The audit prints one line. Of the voters who saw the page, {{au.answer}}% voted for him. Of those
  who never saw it, {{au.notS}}. A fresh vote opens across the year group, secret this time.

| # | N | V | S | neither | both | answer | miss | his share | P(him given didn’t see) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 120 | 50 | 40 | 60 | 30 | 75 | 25 | 42% | 25% |
| 1 | 200 | 100 | 50 | 90 | 40 | 80 | 20 | 50% | 40% |
| 2 | 240 | 80 | 120 | 100 | 60 | 50 | 25 | 33% | 16.7% |
| 3 | 230 | 130 | 125 | 90 | 115 | 92 | 50 | 57% | 14.3% |
| 4 | 100 | 40 | 50 | 45 | 35 | 70 | 35 | 40% | 10% |
| 5 | 120 | 45 | 50 | 55 | 30 | 60 | 25 | 38% | 21.4% |
| 6 | 150 | 45 | 75 | 60 | 30 | 40 | 20 | 30% | 20% |

Generator rules: keypad (0, 99, 1); N 100 to 240 in tens; V, S and neither in fives; both = V + S − (N −
neither), with 0 < both < min(V, S). Require:
- the answer 100 × both ÷ S and the miss 100 × both ÷ N both whole and two-digit, so no leading zero;
- the answer not printed in its own clue;
- **(proposed, "For Jon" 7)** V/N 30–60%; S/N 20–60%; P(V | S) − P(V | not S) ≥ twenty points; the four clue
  figures all different; S ≠ 100.

Token `notS` is that percentage as text, written "25%" when whole and "about 17%" when rounded. Token `inside` is
N − neither.

### Bank entries for phase 2 (scratch-checked)

`check-lock-bank.py` on these three, in a scratch file: `admin-passcode-product-rule ok unique (210)`,
`vote-log-overwrite ok unique (4)`, `leak-audit-conditional ok unique (75)`.

```
ID:          admin-passcode-product-rule
LEVEL:       GCSE Higher
TOPIC:       Number / Counting (product rule, no repeats)
INSTRUMENT:  Three-digit keypad.
CONTEXT:     The admin passcode is 3 different keys from a pad of 7, no key used twice. The brute-force guard resets only when told exactly how many passcodes it would have to try.
CLUE:        "ADMIN PASSCODE: 3 different keys, never the same key twice." / "A pad of 7 keys."
ANSWER:      210
AHA:         Each key used leaves one fewer for the next position, so the choices multiply down: 7 x 6 x 5.
MISCONCEPTION: 343 (repeats allowed, 7 x 7 x 7).
SOLVE:       7 x 6 x 5 = 210.
TIME:        2
VERIFY:      [n for n in range(1000) if n - len([(a, b, c) for a in range(7) for b in range(7) for c in range(7) if len({a, b, c}) == 3]) == 0]

ID:          vote-log-overwrite
LEVEL:       GCSE Higher
TOPIC:       Ratio / Exponential decay by iteration
INSTRUMENT:  Dial 1 to 20 minutes, step 1.
CONTEXT:     20% of the remaining original records are overwritten each minute. The log is unrecoverable once fewer than half survive. How many whole minutes until then?
CLUE:        "Each minute, 20% of the original records still left are replaced." / "Once fewer than half survive, the log is unrecoverable."
ANSWER:      4
AHA:         Each minute takes 20% of what is left, so 0.8 of the records survive each minute: 0.8^3 = 0.512, 0.8^4 = 0.4096.
MISCONCEPTION: 3 (linear: 20% of the original each minute, half gone after 2.5 minutes).
SOLVE:       0.8^3 = 0.512 is not below 0.5; 0.8^4 = 0.4096 is. 4 minutes.
TIME:        3
VERIFY_MIN:  [n for n in range(1, 21) if Fraction(4, 5) ** n < Fraction(1, 2)]

ID:          leak-audit-conditional
LEVEL:       GCSE Higher
TOPIC:       Probability / Venn diagrams and conditional probability
INSTRUMENT:  Two-digit keypad.
CONTEXT:     120 voters; 50 voted for him; 40 opened the leak page; 60 did neither. Of those who opened the page, what percentage voted for him?
CLUE:        "Votes cast: 120. Leading: 50." / "Opened the leak page before voting: 40. Never opened it and did not vote for him: 60."
ANSWER:      75
AHA:         Inside the circles are 120 - 60 = 60 voters; 50 + 40 = 90 counts the overlap twice, so 30 are in both; 30 out of the 40 who saw it.
MISCONCEPTION: 25 (30 out of all 120 voters: the wrong denominator).
SOLVE:       Both = 50 + 40 - (120 - 60) = 30. 30 / 40 = 75%.
TIME:        3
VERIFY:      [n for n in range(100) if n * 40 - 100 * (50 + 40 - (120 - 60)) == 0]
```

### Joint draw (canon §11.3)

Measured with `check-escape-rooms.py`’s own `clue_strings()` and `draw_is_valid()`, run on the six clue strings
above as they would appear in `room.js`: **183 of 280 joint draws VALID; variant 0 VALID.** The floor is 20.
The 97 invalid draws break down as follows (a draw can fail more than one way):
- 42: lock 2’s answer is lock 1’s printed L (3) or k (6 to 9);
- 36: two locks print the same clue figure (lock 2’s rate is one of lock 1’s k values or one of the audit’s
  totals);
- 30: lock 1’s 120 is printed in an audit clue (120 voters in sets 0 and 5, 120 who saw the page in set 2);
- 4: the audit’s answer is printed in another lock’s clue. Every library was built under the generator’s own `keep()`
rules in a scratch copy: settable answer and miss, exactly one solution, answer not in its own clue, clear of the
ends, spread. Nothing was committed to the generator.

---

## Picture alts (empty of people, no lettering; to be checked against the pictures in phase 3)

- **sceneAlt:** A school IT suite after the last lesson. Rows of monitors are switched off except one big display
  at the front, glowing with a neon pop-concert stage: sparkles, a sweeping spotlight, and a crown hanging over
  an empty space. At the back a server cupboard stands open, its lights blinking. On the side wall a corkboard
  holds a single printed sheet with a gold star stuck to it, and the desk by the door has a keyboard pushed back
  and a mug of tea gone cold.
- **failAlt:** The same IT suite, the room lights off. The big display blazes: the crown lowered and glowing, the
  spotlight full on, sparkles frozen mid-fall. The server cupboard is shut and the chairs are pushed in.
- **winAlt:** The same IT suite in morning light. The big display is calm and dark blue, with a small plain crown in
  one corner and no sparkles. On the desk a printed sheet lies face down beside a pencil, and the gold star is
  stuck to the edge of the monitor.

*(No art prompts, per DO NOT TOUCH. The win alt’s pencil and face-down sheet are the new prompt written by hand.)*

## Hub card line and meta description

- **Hub card:** The prom king vote looks amazing and isn’t secret. Mr Narry needs it put right before the result
  goes up at half past three.
  Topics line: Counting · Exponential decay · Conditional probability
- **Meta description** (159 characters; the same string for `description` and `og:description`): A 15-minute GCSE
  Higher maths escape room. The prom king vote isn’t secret. Close the leak before the result goes up. Counting,
  decay, conditional probability.

## Teacher page line (for lecturers who want to discuss it)

This room is about using AI as a tool, not as a replacement for thinking. Mr Narry asked for a vote that looked
amazing and got exactly that; nobody asked who should see the votes. Worth asking a class: what should his prompt
have said, and what should he have checked himself?

---

## Checklist: the voice contract and the room rules

Voice contract (`docs/escape-room-voice-contract.md`, fixed constraints) and its STOP IF:

| Rule | Result |
|---|---|
| Students are the heroes; the antagonist is the obstacle | **Pass, with a note.** The students do all three locks. There is no antagonist on stage by design (your brief): Narry is an ally and the bully is offstage. The obstacle is the countdown, the Kiln precedent (working doc §3, §5i) |
| Wrong-entry lines never mock the student or their answer, only the lock | **Pass.** Every line is Narry and his own habit; none mentions the students or what they set |
| The antagonist loses graciously; no humiliation | **Pass.** Narry owns it ("It was my prompt"), as your arc says. The bully is not humiliated; he is not in the win at all |
| Voice through the room setup, not a narrator layer | **Pass, with a note.** The hook and brief are narration, as in the reference room; Narry’s voice carries his opening line, the wrong-entry slot and the win |
| "Idiot" and "stupid" never appear | **Pass** |
| British English | **Pass.** IT suite, registration, biro, tea, prom king |
| Name: real-sounding, no equipment puns, no innuendo | **Pass.** Mr Brian Narry is your name. **For you:** I can’t check whether it maps onto a real, identifiable member of staff |
| STOP IF: inventing the character rather than drawing it out | **Did not fire.** Your brief gives the premise, character, flaw, opening line, arc, win, fail and the wrong-line shape. Every extrapolation is marked **[X]** |
| STOP IF: a change to puzzle logic or lock behaviour | **Not applicable as written.** This is a new room, and its three new locks are the ones your contract specifies |

Room rules (working doc §3, §4, §8; canon §11.3) and this contract:

| Rule | Result |
|---|---|
| One enforceable failure, able to reach the students during play | **Pass.** The countdown to the half-past-three announcement, on the voting screen in the room |
| A character who is not present cannot be the threat | **Pass.** The bully is offstage and is not the threat; the countdown is |
| Each character speaks only in their own room | **Pass.** Narry is new and speaks only here. The Head is mentioned once, offstage, and does not speak |
| No third never-knew ending | **Pass.** Narry sees it all and owns it; nobody ends the room not knowing |
| If the students use the antagonist’s method, say why it is different, in the brief | **Pass.** The audit uses totals and never names anyone ("For Jon" 13); the brief says so |
| Students win by putting something right | **Pass.** They close a leak, save a log and open a fair vote. **They change no vote** (your ruling) |
| The joke lands on the prompt, never on AI itself | **Pass.** The prompt object, the sticky note and the wrong lines are all about Narry handing over his thinking; the AI "did exactly what it was asked" |
| His opening line verbatim, and "my prompt" by the win | **Pass.** Hook and win |
| Narry’s prompt quoted verbatim; no brand or franchise name | **Pass.** Object 7, word for word |
| No picture of him; pictures empty of people | **Pass.** No alt has a person |
| No figure in the prose outside `{{tokens}}` | **Pass.** No numeral anywhere in the prose. "Fifteen minutes" and "half past three" are words, as in Prom Budget and Kiln. The method constants in the hints (100 − r, 0.5 or 0.25) are tokens too |
| No tokens in `hook`, `brief`, `stakes`, `win` | **Pass** |
| Never "Ofsted", in any form | **Pass** |
| No brand names; no year | **Pass** |
| St Martha’s Secondary | **Pass.** The school isn’t named in this room’s prose, so nothing contradicts it |
| UK school timings | **Pass.** The announcement is at half past three, the end of the day; the result goes up at registration |
| Nothing in `prom-budget` contradicted (STOP IF) | **Pass.** Read in full ("For Jon" 14) |
| Eight objects, at least two blanks | **Pass.** Six clues, two blanks |
| Every lock has exactly one settable answer on its instrument (STOP IF) | **Pass.** Checked in scratch: `check-lock-bank.py` unique on all three, and every variant above passes the generator’s `keep()` rules |
| Joint draw at least 20 VALID (STOP IF) | **Pass.** 183 of 280, variant 0 VALID |
| No `missArt` | **Pass.** The fail picture shows the crown already down, which is only true at time-out, so no lock may set `missArt` (the kiln and comic rule) |
| Meta description 150–160 characters | **Pass.** 159 |
| ★★★ Challenge, grades 6–9 | **Pass, with a note.** Product rule (6–7), decay by iteration (7, calculator), conditional probability from a Venn diagram (7–8) |
