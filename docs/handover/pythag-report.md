# Just Pythag It, Bruv: the hypotenuse step, scoring, questions and misconception feedback (PYTHAG-REPORT)

Contract PYTHAG-REPORT (Project Claude for Jon, 19 Oct 2026, 10:24; verbatim in
`docs/history/contracts/2026-10-19-pythag-report.md`). Research only: nothing in the game changed. Read from
`games/just-pythag-it-bruv/index.html` on main (597a8b3); the measurement ran against the live page in Chromium.

## CLASS CHECK: whose code is it?

The round structure, the hypotenuse step, question building, the add-instead-of-subtract diagnosis, scoring and
the results screen are the **game's own code** (`window.JPIB`: `J.STAGES`, `J.buildSession`, `J.isHypTap`,
`J.isAddError`, `J.scoreFor`, `nextQuestion`/`tapSide`/`submit`/`finish`). No shared stage, step or unlock layer
exists in `schools/assets/` (Matrix Crunch's "streak of 5 unlocks next stage" is in its own page too). What is
shared: the marking primitives (`MaffsAnswer.exact` and `MaffsAnswer.decimal`, `answer.js`), the session-length
buttons (`MaffsSession`, `session-length.js`), the answer lock and Next control, the on-screen calculator, the
leaderboard and score history. A "Formula only" mode would change this game's flow, not the shared layer; it
would call the same shared marking.

## 1. The hypotenuse tap

- **Round 1 only, not every question.** A session is 20 questions in three rounds, in order: round 1 (7
  questions, whole-number triangles), round 2 (7, decimal answers), round 3 (6, in context). Only round 1
  (`q.stage === 'a'`) opens in the tap state: the prompt is "Tap the hypotenuse." and the answer box is not
  open. Rounds 2 and 3 open straight on the calculation. So 7 of every 20 questions ask for the tap.
- **A wrong tap blocks the calculation until the right side is tapped.** `tapSide`: the hypotenuse (side `r`)
  marks it and opens the answer box; any other side is marked as a miss and shows "The hypotenuse is opposite
  the right angle, and always the longest side." The student stays in the tap state, with unlimited tries.
- The unknown side shows "?" in round 1 and "x" after; labels are styled alike, so the styling never gives
  the hypotenuse away.

## 2. Scoring

- **The tap earns nothing and costs nothing.** No score, no event, no penalty (code comment: "No score, no
  event, no penalty"). Each answer's score is timed from when the answer box opens (`scoreStart` is set in
  `openAnswer`), so time spent tapping never lowers the score.
- **Per question:** a right answer scores `max(1, round(100 / (1 + 0.15 · ln(1 + seconds))))` (canon §7.3,
  BASE 100, T_K 0.15); a wrong answer scores 0.
- **Leaderboard:** `MaffsLeaderboard.submitScore('just-pythag-it-bruv', 'ks3', score, 20)`, the summed score.
- **On-device:** `MaffsScoreHistory.record('just-pythag-it-bruv', 'ks3', score)` and the personal best
  `jpib_best_ks3` in localStorage.
- **Session length: always 20.** `J.LENGTH = 20`; `MaffsSession` is offered only 20, so the start screen shows
  one button. The session clock (shown, and on the results screen) does count tap time; the score does not.
- Results: score, right out of 20, time, per-round right counts (7/7/6), and "Added instead of subtracting: N".

## 3. Questions and marking

- **Generated each session from fixed pools** (seeded `mulberry32`), never a stored list of questions:
  - Round 1: 7 of the **14** entries in `J.TRIPLES`. These are 3-4-5 times 1-8 and 10, 5-12-13 times 1-3,
    8-15-17 and 7-24-25. The roster says "15 triples"; the code has 14.
  - Round 2: 7 from `J.POOL_B`. `hyp` is legs 3 to 20 with no square sum, 164 pairs; `short` is a hypotenuse
    of 6 to 25 and a leg, with no square difference, 236 pairs.
  - Round 3: 6 from five situations, all five every session: ladder, TV, ramp (hyp only), field and roof.
    The pools come from realistic bounds: 1,083 hyp and 523 short.
- **Every question asks for one side:** the hypotenuse (`hyp`: two legs given) or a shorter side (`short`:
  the hypotenuse and one leg given). 7 or 8 are `hyp` per session, so 12 or 13 of 20 are `short`, and no
  three in a row are the same type.
- **Keys:** exact `sqrt(S)/D`, rounded half up (SR-1) to 1 d.p. in rounds 2-3. Round 1 answers are exact
  whole numbers. Rounds 2-3 never draw a perfect square, so "to 1 decimal place" always matters.
- **Marking, no tolerance:**
  - Round 1: `MaffsAnswer.exact`, the whole number, so "10" or "10.0" is right.
  - Rounds 2-3: `MaffsAnswer.decimal(raw, key, 1)`. The 1 d.p. value must equal the key ("5.8", "5.80"). An
    unrounded answer that rounds half up to the key ("5.83") gets a "round to 1 d.p." message and is not
    marked; anything else is wrong.

## 4. Wrong-answer diagnosis now

- One diagnosis exists: **added instead of subtracting**, on `short` questions only (`J.isAddError`). A wrong
  answer equal to sqrt(c² + a²), rounded as the question asks, counts. In round 1 that is the whole number
  or 1 d.p.
  - The first three in a session get a worked example on the question's own numbers ("You added instead of
    subtracting").
  - After that, a one-line nudge: "Is the side you're finding the longest one?"
  - The results screen counts them.
- The engine guarantees that value is at least 0.1 (or 1) away from the key.
- A wrong tap gets its one fixed line (item 1). Every other wrong answer gets the worked solution only.

## 5. Feasibility: collisions among the candidate errors

All 2,048 distinct questions the pools can produce, each computed exactly (integers and 60-digit square roots)
and rounded half up as the game rounds: round 1 to a whole number, rounds 2-3 to 1 d.p.

| Question type | Candidate errors |
|---|---|
| Finding c from legs a, b | sqrt(\|b²−a²\|), a²+b², a+b, sqrt(2a+2b) |
| Finding a shorter side from c, a | sqrt(c²+a²), c²−a², c−a, sqrt(2c−2a) |

Script output (scratch script, not committed):

```
Questions the game can ask: 2048 (round 1: 42; round 2: 400; round 3: 1606)
round  type   questions  candidate=key  two candidates equal  either
1      hyp           14              0                     1       1
1      short         28              0                     7       7
2      hyp          164              0                    15      15
2      short        236              0                    18      18
3      hyp         1083              5                    43      48
3      short        523              2                    11      13
total              2048              7                    95     102

All candidate = key cases:
  round 3 ladder [8, 24] (hyp): key 2.5; sqrt(2a+2b) = key 2.5
  round 3 ladder [9, 24] (hyp): key 2.6; sqrt(2a+2b) = key 2.6
  round 3 ladder [11, 24] (hyp): key 2.6; sqrt(2a+2b) = key 2.6
  round 3 ladder [8, 25] (hyp): key 2.6; sqrt(2a+2b) = key 2.6
  round 3 ladder [11, 25] (hyp): key 2.7; sqrt(2a+2b) = key 2.7
  round 3 ladder [45, 44] (short): key 0.9; c^2-a^2 = key 0.9
  round 3 ladder [50, 49] (short): key 1.0; c^2-a^2 = key 1.0
Two-candidate collisions by pair:
  round 1 hyp   sqrt(|b^2-a^2|) = sqrt(2a+2b)    1
  round 1 short c-a = sqrt(2c-2a)                7
  round 2 hyp   sqrt(|b^2-a^2|) = sqrt(2a+2b)    15
  round 2 short c-a = sqrt(2c-2a)                18
  round 3 hyp   sqrt(|b^2-a^2|) = sqrt(2a+2b)    43
  round 3 short c-a = sqrt(2c-2a)                3
  round 3 short sqrt(c^2+a^2) = c^2-a^2          8
Examples of two-candidate collisions:
  round 1 3-4-5 (short, whole): key 4; c-a = sqrt(2c-2a) = 2      (c 5, a 3: 5-3 = 2 and sqrt(4) = 2)
  round 1 6-8-10 (hyp, whole): key 10; sqrt(|b^2-a^2|) = sqrt(2a+2b) = 5
  round 2 legs 3, 5 (hyp, to 1 d.p.): key 5.8; sqrt(|b^2-a^2|) = sqrt(2a+2b) = 4.0
```

The ladder pools are in tenths of a metre, so [8, 24] means a 0.8 m foot and a 2.4 m height.

What the numbers say:
- **A candidate equals the key on 7 questions, all round-3 ladders.**
  - In each, the lengths are small numbers of metres, below about 3. There, squaring and doubling land
    close together (0.8² + 2.4² = 6.40 and 2·0.8 + 2·2.4 = 6.4), and when c and a differ by about 0.1 m,
    c² − a² rounds to the same as its root.
  - A "wrong" answer there would be marked right: the game marks by value, so the student is right whatever
    their method. A diagnosis would simply never fire on those 7.
- **Two candidates agree on 95 questions (4.6%).** Almost all are the same two pairs:
  - c − a = sqrt(2c − 2a): this happens whenever c − a = 2.
  - sqrt(|b² − a²|) = sqrt(2a + 2b): this happens whenever b − a = 2 (b² − a² = (b−a)(b+a) = 2(a+b)).
  - These are exact identities, not rounding accidents. On those questions the feedback would have to name
    both mistakes or neither. Eight round-3 shorts (small ladder and roof lengths) also tie sqrt(c² + a²) with
    c² − a².
- On the other 1,946 questions (95%), every candidate gives a different answer from the key and from each
  other, so a value-based diagnosis can tell them apart.

## 6. A mode on the start screen

- The start screen has room for one. Its "Questions" panel holds the session-length chooser (`#sessionSelect`,
  one button, 20) above Start, and a mode row can sit there.
- Other games keep modes in three ways:
  - **Mode cards** on the start screen: Shape Shifter's four, Probability Paradox's three.
  - **Stage modes with their own leaderboard boards:** Simultaneous Solver's `foundation-s1` to `-s4`, where
    `submitScore(SLUG, BOARD, …)` takes the board from the mode.
  - **Practice and daily modes with separate boards:** Free Daily Pizza.
- A "Formula only" mode needs one decision first: its own board or the `ks3` board. **Because the tap never
  costs score, a Formula-only run scores the same as a normal run on the same answers at the same speed,** so
  sharing `ks3` would not by itself make the board unfair. Only Jon's design, for example different questions
  in the mode, would change that.
