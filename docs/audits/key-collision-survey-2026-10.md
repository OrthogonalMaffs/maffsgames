# Key-collision survey, October 2026

Contract KEY-COLLISION-SURVEY (Jon, 20 Oct 2026; verbatim in `docs/history/contracts/2026-10-20-key-collision-survey.md`).
Report only: no game, verifier, shared module, findings file, register or workflow was changed.

**The question.** In every game that generates its questions, is there a question where a named or common error,
rounded as the game rounds its key, gives the key? The game marks by value (typed answers) or by the option the
student picks (multiple choice), so a student using that wrong method is marked right.

**The script.** `scripts/survey-key-collisions.py` (not wired into CI). Every count below is its output, pasted
unedited from one run (`python scripts/survey-key-collisions.py`, 20 Oct 2026, on main at dd22aa0). It loads each game through the stub server, reads the question space from the page itself
(the game's own pools, or its own generator driven through every choice it can make: `rInt`/`randInt` and
`Math.random` replaced by a counter and every path walked), then recomputes every key and every error in Python,
exactly (fractions, integer square roots, or 50-digit `mpmath` for trigonometry and logs), from the numbers the
question shows, rounded exactly as the game rounds its key.

**The control.** Just Pythag It, Bruv reported 7 before #453 (PYTHAG-KEY-COLLIDE). It reports **0** here, over all
2,041 questions its pools can produce.

## How to read the counts

- A **collision** is one (error, question) pair where the error, rounded as the key is, equals the key. A
  question that two errors land on counts twice.
- **coincidence**: the wrong method is a different calculation, and its value happens to equal the key on that
  question (2 + 2 = 2 x 2; 60% of 150 = 150 - 60). A student holding that misconception is marked right, and
  nothing about the question could tell. These are the cases #453 fixed in Just Pythag It, Bruv.
- **methods agree**: on that question the wrong method is the same calculation as the right one, so no
  question of that shape can tell them apart (halving "simplifies" a ratio whose HCF is 2; sharing equally is
  right when the ratio is 3:3; reading 7/100 as 7% is right). A student holding the misconception is still
  marked right; whether that matters is a design question (how often a game should ask the questions that
  separate the methods), not a wrong key.
- **two-way**: a rule of thumb's agreement with a two-way choice (which card has more factors; equivalent or
  not; which pack is better value). Chance alone gives about half. Reported, never counted as a collision.

## Headline (this script's output)

| game | listed | parts surveyed | coincidence collisions | methods-agree collisions |
|---|---|---|---|---|
| just-pythag-it-bruv | yes | 1 | 0 | 0 |
| six-sevens-bruv | yes | 1 | 1 | 0 |
| split-it | yes | 12 | 109 | 1786 |
| free-daily-pizza | yes | 4 | 2 | 80 |
| trig-worms | yes | 3 | 128 | 0 |
| distinctly-average | yes | 12 | 2 | 241 |
| quadratic-factoriser | yes | 3 | 15 | 1188 |
| modular-battle | yes | 1 | 231 | 0 |
| factor-race | yes | 1 | 0 | 0 |
| fraction-equivalence | yes | 1 | 0 | 0 |
| bearing-blitz | yes | 2 | 0 | 24 |
| shape-shifter | yes | 1 | 0 | 0 |
| equatle | yes | 1 | 0 | 3093 |
| log-laws | yes | 6 | 0 | 46 |
| **all** | | 49 | **488** | **6458** |

## STOP IF: wrong methods marked right in listed games (for Jon)

The contract stops on "a collision where a wrong method is marked right in a listed game". Every game below is
listed. Coincidence collisions (the closest match to #453's), with the clearest example of each:

- **six-sevens-bruv (1):** "2 x 2 = ?": adding gives 4.
- **split-it (109):** "Share £8 in the ratio 2 : 2" (and every 2 : 2 share, KS3 95, GCSE 14): dividing the amount
  by one part, not the total, gives each share.
- **free-daily-pizza (2):** "60% of 150" (subtracting the percentage, 150 - 60, gives 90); "10% as a fraction"
  (putting the percentage number on the bottom gives 1/10).
- **trig-worms (128, all "find the angle"):** rounding the ratio to 1 d.p. before the inverse (76), tan-1 of the
  ratio upside down (38), tan-1 for sin-1 or cos-1 (8) and the other inverse (6) give the same whole number of
  degrees, e.g. 75 deg from adjacent and hypotenuse with tan-1 of hyp/adj. The game already lists most of these
  errors and silently drops the ones that coincide (`questionFrom` keeps "three named errors ... only if they
  differ from the key"), so the student using them picks the key.
- **distinctly-average (2):** two bimodal items whose two largest (or two smallest) values are the modes.
- **quadratic-factoriser (15):** GCSE "x^2 + 4x + 4": swapping sum and product gives (x + 2)(x + 2); Higher guided
  step 2 (find ac): a x b, b x c or a + c equals ac on 14 trinomials (b = c, a = b, or a = c = 2).
- **modular-battle (231):** the remainder equals the first digit after the point of a / b (88: every a / 9 with a remainder, and
  others such as 11 mod 8, 1.375), the last digit of a (65), b - r (53, when b = 2r) or the quotient (25).

Methods-agree collisions are listed per game below; the largest are split-it (1,786: mostly "the HCF of the first
two parts" for three-part ratios, and sharing equally when the parts are equal), quadratic-factoriser (1,188: every
error still ends at "No real solutions" on the 184 no-real-roots items; swapping the constants when p = r or
q = s), equatle (3,093 of 4,430 mixed-operation equations give the same value worked left to right), and
distinctly-average (241: on every one of its 73 mean items the median equals the mean, and on 43 the mode does,
by its pair-swap construction).

Nothing was fixed (the contract forbids it, even under SR-30; no standing ruling decides these cases).

## Which games generate their questions, and how that was decided

Every game in the roster (96 live, Regression Rumble withdrawn) was read: a game counts as generated if any
question's numbers are produced by code at runtime or by enumerating parameter lists in code; a game whose
questions are written out literally (randomness only shuffling the order or the options) is a fixed bank. The
roster's descriptions name five ("generated" or "from parameters": split-it, just-pythag-it-bruv,
quadratic-factoriser, simultaneous-solver, free-daily-pizza); reading the code found the rest, and showed that
simultaneous-solver's bank is generated offline (`scripts/gen-simultaneous.py`) and stored literally, so it is a
fixed bank at runtime. Fourteen generate some or all of their questions; all fourteen are surveyed.

## Per game (the script's output)

### just-pythag-it-bruv: all three rounds (control)
- question space: 2041 questions (every pool entry, every variant); enumerated (pools read from window.JPIB)
- marking: typed; round 1 exact whole number, rounds 2-3 to 1 d.p. half up (MaffsAnswer)
- collisions with the key: **0**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| sqrt(\|b^2-a^2\|): subtract instead of add (hyp) | coincidence | 1256 | 0 |
| a^2+b^2: no square root (hyp) | coincidence | 1256 | 0 |
| a+b: add the sides (hyp) | coincidence | 1256 | 0 |
| sqrt(2a+2b): double instead of square (hyp) | coincidence | 1256 | 0 |
| sqrt(c^2+a^2): add instead of subtract (the game's own diagnosis) (short) | coincidence | 785 | 0 |
| c^2-a^2: no square root (short) | coincidence | 785 | 0 |
| c-a: subtract the sides (short) | coincidence | 785 | 0 |
| sqrt(2c-2a): double instead of square (short) | coincidence | 785 | 0 |

### six-sevens-bruv: times tables 2-12
- question space: 341 questions (66 facts x swap x form); enumerated (SSB.FACTS, SSB.formsFor, SSB.makeQuestion)
- marking: typed whole number, exact (parseInt === answer)
- collisions with the key: **1**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| x+y: add instead of multiply (product form) | coincidence | 121 | 1 |
| x(y-1) or (x-1)y: one lot short (product form) | coincidence | 121 | 0 |
| x(y+1) or (x+1)y: one lot over (product form) | coincidence | 121 | 0 |
| c - given: subtract instead of divide (missing factor) | coincidence | 220 | 0 |
| c x given: multiply instead of divide (missing factor) | coincidence | 220 | 0 |
| the given factor copied (missing factor) | coincidence | 220 | 0 |
  - x+y: add instead of multiply (product form): 2 × 2 = ?: key 4

### split-it: simplify, ks3
- question space: 296 distinct questions (4080 paths walked, 48 redraw paths cut); enumerated (generators[mode] driven through every rInt and Math.random choice)
- marking: typed, every box must be right (MaffsAnswer.exact / .money / .decimal 1 d.p.; fractions exact numerator and denominator)
- collisions with the key: **42**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| parts in the wrong order (reversed) | agree | 296 | 0 |
| halved once (divided by 2 only) | agree | 296 | 42 |
  - halved once (divided by 2 only): Write 4 : 2 in its simplest form.: key 2:1
  - halved once (divided by 2 only): Write 4 : 6 in its simplest form.: key 2:3
  - halved once (divided by 2 only): Write 4 : 10 in its simplest form.: key 2:5
  - halved once (divided by 2 only): Write 4 : 14 in its simplest form.: key 2:7
  - halved once (divided by 2 only): Write 6 : 2 in its simplest form.: key 3:1

### split-it: simplify, gcse
- question space: 810 distinct questions (2064 paths walked, 24 redraw paths cut); enumerated (generators[mode] driven through every rInt and Math.random choice)
- marking: typed, every box must be right (MaffsAnswer.exact / .money / .decimal 1 d.p.; fractions exact numerator and denominator)
- collisions with the key: **915**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| parts in the wrong order (reversed) | agree | 810 | 112 |
| halved once (divided by 2 only) | agree | 810 | 180 |
| divided by the HCF of the first two parts only | agree | 810 | 623 |
  - parts in the wrong order (reversed): Write 6 : 9 : 6 in its simplest form.: key 2:3:2
  - parts in the wrong order (reversed): Write 6 : 12 : 6 in its simplest form.: key 1:2:1
  - parts in the wrong order (reversed): Write 6 : 15 : 6 in its simplest form.: key 2:5:2
  - parts in the wrong order (reversed): Write 6 : 18 : 6 in its simplest form.: key 1:3:1
  - parts in the wrong order (reversed): Write 6 : 3 : 6 in its simplest form.: key 2:1:2
  - halved once (divided by 2 only): Write 4 : 2 : 2 in its simplest form.: key 2:1:1
  - halved once (divided by 2 only): Write 4 : 4 : 2 in its simplest form.: key 2:2:1
  - halved once (divided by 2 only): Write 4 : 4 : 6 in its simplest form.: key 2:2:3
  - halved once (divided by 2 only): Write 4 : 4 : 10 in its simplest form.: key 2:2:5
  - halved once (divided by 2 only): Write 4 : 6 : 2 in its simplest form.: key 2:3:1
  - divided by the HCF of the first two parts only: Write 6 : 3 : 3 in its simplest form.: key 2:1:1
  - divided by the HCF of the first two parts only: Write 6 : 6 : 12 in its simplest form.: key 1:1:2
  - divided by the HCF of the first two parts only: Write 6 : 6 : 18 in its simplest form.: key 1:1:3
  - divided by the HCF of the first two parts only: Write 6 : 9 : 3 in its simplest form.: key 2:3:1
  - divided by the HCF of the first two parts only: Write 6 : 9 : 6 in its simplest form.: key 2:3:2

### split-it: equivalent, ks3
- question space: 1134 distinct questions (1134 paths walked, 0 redraw paths cut); enumerated (generators[mode] driven through every rInt and Math.random choice)
- marking: typed, every box must be right (MaffsAnswer.exact / .money / .decimal 1 d.p.; fractions exact numerator and denominator)
- collisions with the key: **126**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| additive: add the difference instead of multiplying | agree | 1134 | 126 |
  - additive: add the difference instead of multiplying: 1 : 1 = 2 : ?: key 2
  - additive: add the difference instead of multiplying: 2 : 2 = 4 : ?: key 4
  - additive: add the difference instead of multiplying: 2 : 2 = 6 : ?: key 6
  - additive: add the difference instead of multiplying: 2 : 2 = ? : 6: key 6
  - additive: add the difference instead of multiplying: 2 : 2 = 8 : ?: key 8

### split-it: equivalent, gcse
- question space: 567 distinct questions (567 paths walked, 0 redraw paths cut); enumerated (generators[mode] driven through every rInt and Math.random choice)
- marking: typed, every box must be right (MaffsAnswer.exact / .money / .decimal 1 d.p.; fractions exact numerator and denominator)
- collisions with the key: **63**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| additive: add the difference instead of multiplying | agree | 567 | 63 |
  - additive: add the difference instead of multiplying: If 1 : 1 = x : 3, find x.: key 3
  - additive: add the difference instead of multiplying: If 2 : 2 = x : 6, find x.: key 6
  - additive: add the difference instead of multiplying: If 2 : 2 = x : 8, find x.: key 8
  - additive: add the difference instead of multiplying: If 2 : 2 = x : 10, find x.: key 10
  - additive: add the difference instead of multiplying: If 2 : 2 = x : 12, find x.: key 12

### split-it: divide, ks3
- question space: 3420 distinct questions (3420 paths walked, 0 redraw paths cut); enumerated (generators[mode] driven through every rInt and Math.random choice)
- marking: typed, every box must be right (MaffsAnswer.exact / .money / .decimal 1 d.p.; fractions exact numerator and denominator)
- collisions with the key: **665**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| shared equally (amount / number of parts) | agree | 3420 | 570 |
| amount / each ratio part (divide by one part, not the total) | coincidence | 3420 | 95 |
  - shared equally (amount / number of parts): Share £4 in the ratio 1 : 1: key 2:2
  - shared equally (amount / number of parts): Share £8 in the ratio 2 : 2: key 4:4
  - shared equally (amount / number of parts): Share £12 in the ratio 2 : 2: key 6:6
  - shared equally (amount / number of parts): Share 12  in the ratio 2 : 2: key 6:6
  - shared equally (amount / number of parts): Share 12 kg in the ratio 2 : 2: key 6:6
  - amount / each ratio part (divide by one part, not the total): Share £8 in the ratio 2 : 2: key 4:4
  - amount / each ratio part (divide by one part, not the total): Share £12 in the ratio 2 : 2: key 6:6
  - amount / each ratio part (divide by one part, not the total): Share 12  in the ratio 2 : 2: key 6:6
  - amount / each ratio part (divide by one part, not the total): Share 12 kg in the ratio 2 : 2: key 6:6
  - amount / each ratio part (divide by one part, not the total): Share 12 ml in the ratio 2 : 2: key 6:6

### split-it: divide, gcse
- question space: 1750 distinct questions (1750 paths walked, 0 redraw paths cut); enumerated (generators[mode] driven through every rInt and Math.random choice)
- marking: typed, every box must be right (MaffsAnswer.exact / .money / .decimal 1 d.p.; fractions exact numerator and denominator)
- collisions with the key: **84**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| shared equally (amount / number of parts) | agree | 1750 | 70 |
| amount / each ratio part (divide by one part, not the total) | coincidence | 1750 | 14 |
  - shared equally (amount / number of parts): Divide 6 in the ratio 1 : 1 : 1: key 2:2:2
  - shared equally (amount / number of parts): Divide 12 in the ratio 2 : 2 : 2: key 4:4:4
  - shared equally (amount / number of parts): Divide 18 in the ratio 2 : 2 : 2: key 6:6:6
  - shared equally (amount / number of parts): Divide 24 in the ratio 2 : 2 : 2: key 8:8:8
  - shared equally (amount / number of parts): Divide 30 in the ratio 2 : 2 : 2: key 10:10:10
  - amount / each ratio part (divide by one part, not the total): Divide 18 in the ratio 3 : 3 : 3: key 6:6:6
  - amount / each ratio part (divide by one part, not the total): Divide 27 in the ratio 3 : 3 : 3: key 9:9:9
  - amount / each ratio part (divide by one part, not the total): Divide 36 in the ratio 3 : 3 : 3: key 12:12:12
  - amount / each ratio part (divide by one part, not the total): Divide 45 in the ratio 3 : 3 : 3: key 15:15:15
  - amount / each ratio part (divide by one part, not the total): Divide 54 in the ratio 3 : 3 : 3: key 18:18:18

### split-it: fractions, ks3
- question space: 84 distinct questions (84 paths walked, 0 redraw paths cut); enumerated (generators[mode] driven through every rInt and Math.random choice)
- marking: typed, every box must be right (MaffsAnswer.exact / .money / .decimal 1 d.p.; fractions exact numerator and denominator)
- collisions with the key: **0**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| part over the other part(s), not over the total | coincidence | 84 | 0 |

### split-it: fractions, gcse
- question space: 90 distinct questions (90 paths walked, 0 redraw paths cut); enumerated (generators[mode] driven through every rInt and Math.random choice)
- marking: typed, every box must be right (MaffsAnswer.exact / .money / .decimal 1 d.p.; fractions exact numerator and denominator)
- collisions with the key: **0**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| part over the other part(s), not over the total | coincidence | 90 | 0 |

### split-it: scale, ks3
- question space: 120 distinct questions (120 paths walked, 0 redraw paths cut); enumerated (generators[mode] driven through every rInt and Math.random choice)
- marking: typed, every box must be right (MaffsAnswer.exact / .money / .decimal 1 d.p.; fractions exact numerator and denominator)
- collisions with the key: **0**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| additive: add the change in servings to each amount | coincidence | 120 | 0 |
| multiplied by the new servings, not the scale factor | coincidence | 120 | 0 |

### split-it: scale, gcse
- question space: 26 distinct questions (156 paths walked, 0 redraw paths cut); enumerated (generators[mode] driven through every rInt and Math.random choice)
- marking: typed, every box must be right (MaffsAnswer.exact / .money / .decimal 1 d.p.; fractions exact numerator and denominator)
- collisions with the key: **0**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| additive: add the change in servings to each amount | coincidence | 26 | 0 |
| multiplied by the new servings, not the scale factor | coincidence | 26 | 0 |

### split-it: unitary, ks3
- question space: 21000 distinct questions (21000 paths walked, 0 redraw paths cut); enumerated (generators[mode] driven through every rInt and Math.random choice)
- marking: typed, every box must be right (MaffsAnswer.exact / .money / .decimal 1 d.p.; fractions exact numerator and denominator)
- collisions with the key: **0**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| inverse operation (divide where it multiplies, or n/m for m/n) | coincidence | 21000 | 0 |
| skipped the unit step (multiplied the total by the new quantity) | coincidence | 21000 | 0 |

### split-it: unitary, gcse
- question space: 44045 distinct questions (44885 paths walked, 0 redraw paths cut); enumerated (generators[mode] driven through every rInt and Math.random choice)
- marking: typed, every box must be right (MaffsAnswer.exact / .money / .decimal 1 d.p.; fractions exact numerator and denominator)
- collisions with the key: **0**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| inverse operation (divide where it multiplies, or n/m for m/n) | coincidence | 2920 | 0 |
| skipped the unit step (multiplied the total by the new quantity) | coincidence | 2920 | 0 |
| best value: the bigger pack (two-way choice; chance is about half) | two-way | 41125 | 25375 |
| best value: the cheaper pack overall (two-way choice) | two-way | 41125 | 26047 |
  - best value: the bigger pack (two-way choice; chance is about half): A 4 for 80p, B 6 for 90p: key B
  - best value: the bigger pack (two-way choice; chance is about half): A 5 for 100p, B 7 for 105p: key B
  - best value: the bigger pack (two-way choice; chance is about half): A 5 for 105p, B 7 for 105p: key B
  - best value: the bigger pack (two-way choice; chance is about half): A 5 for 105p, B 8 for 120p: key B
  - best value: the bigger pack (two-way choice; chance is about half): A 5 for 105p, B 8 for 128p: key B
  - best value: the cheaper pack overall (two-way choice): A 5 for 105p, B 7 for 105p: key B
  - best value: the cheaper pack overall (two-way choice): A 5 for 105p, B 8 for 176p: key A
  - best value: the cheaper pack overall (two-way choice): A 5 for 105p, B 8 for 184p: key A
  - best value: the cheaper pack overall (two-way choice): A 5 for 105p, B 8 for 192p: key A
  - best value: the cheaper pack overall (two-way choice): A 5 for 105p, B 8 for 200p: key A

### free-daily-pizza: stage 1
- question space: 90 items (the whole bank); enumerated (FDP.BANK, built by FDP.buildBank from its parameter lists)
- marking: multiple choice, the option's key (form and exact value; a simplest-form fraction by the numbers shown)
- collisions with the key: **3**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| denominator-as-decimal: the bottom number read as the decimal (b/10) | coincidence | 60 | 0 |
| inversion: the fraction turned upside down | coincidence | 90 | 0 |
| place-value: x by 10 | coincidence | 90 | 0 |
| place-value: / by 10 | coincidence | 90 | 0 |
| place-value: x by 100 | coincidence | 90 | 0 |
| place-value: / by 100 | coincidence | 90 | 0 |
| raw-part: the top number as the percentage (a%) | agree | 30 | 2 |
| digit-reading: the digits after the point as a denominator (1/digits) | coincidence | 11 | 0 |
| digit-reading: the percentage number as a denominator (1/p) | coincidence | 11 | 1 |
  - raw-part: the top number as the percentage (a%): S1:conv:f>p:1/100 (offered: place-value, place-value, inversion)
  - raw-part: the top number as the percentage (a%): S1:conv:d>p:1/100 (offered: place-value, place-value, place-value)
  - digit-reading: the percentage number as a denominator (1/p): S1:conv:p>f:1/10 (offered: place-value, inversion, place-value)

### free-daily-pizza: stage 2
- question space: 206 items (the whole bank); enumerated (FDP.BANK, built by FDP.buildBank from its parameter lists)
- marking: multiple choice, the option's key (form and exact value; a simplest-form fraction by the numbers shown)
- collisions with the key: **24**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| denominator-as-decimal: the bottom number read as the decimal (b/10) | coincidence | 18 | 0 |
| inversion: the fraction turned upside down | coincidence | 138 | 0 |
| place-value: x by 10 | coincidence | 138 | 0 |
| place-value: / by 10 | coincidence | 138 | 0 |
| place-value: x by 100 | coincidence | 138 | 0 |
| place-value: / by 100 | coincidence | 138 | 0 |
| raw-part: the top number as the percentage (a%) | agree | 46 | 24 |
| digit-reading: the digits after the point as a denominator (1/digits) | coincidence | 19 | 0 |
| digit-reading: the percentage number as a denominator (1/p) | coincidence | 20 | 0 |
| subtract-instead: the same number taken off top and bottom | coincidence | 68 | 0 |
| inversion: upside down | coincidence | 68 | 0 |
| one-side-only: the top divided, not the bottom | coincidence | 68 | 0 |
  - raw-part: the top number as the percentage (a%): S2:conv:f>p:3/100 (offered: place-value, place-value, place-value)
  - raw-part: the top number as the percentage (a%): S2:conv:d>p:3/100 (offered: place-value, place-value, place-value)
  - raw-part: the top number as the percentage (a%): S2:conv:f>p:7/100 (offered: place-value, place-value, place-value)
  - raw-part: the top number as the percentage (a%): S2:conv:d>p:7/100 (offered: place-value, place-value, place-value)
  - raw-part: the top number as the percentage (a%): S2:conv:f>p:9/100 (offered: place-value, place-value, place-value)

### free-daily-pizza: stage 3
- question space: 138 items (the whole bank); enumerated (FDP.BANK, built by FDP.buildBank from its parameter lists)
- marking: multiple choice, the option's key (form and exact value; a simplest-form fraction by the numbers shown)
- collisions with the key: **51**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| one-part-only: N/b, not scaled up | agree | 90 | 36 |
| complement: the part left over | agree | 138 | 10 |
| no-divide: multiplied by the top only | coincidence | 90 | 0 |
| inversion: divided by the fraction | coincidence | 90 | 0 |
| place-value: x10 | coincidence | 138 | 0 |
| place-value: /10 | coincidence | 138 | 0 |
| denominator-as-decimal: N x b/10 | coincidence | 72 | 0 |
| subtract-percent: N - p | coincidence | 48 | 1 |
| one-part-only: 10% only (N/10) | agree | 48 | 4 |
| inversion: N divided by p% | coincidence | 48 | 0 |
  - one-part-only: N/b, not scaled up: S3:frac:1/2:6 (offered: inversion, denominator-as-decimal, place-value)
  - one-part-only: N/b, not scaled up: S3:frac:1/2:8 (offered: inversion, denominator-as-decimal, place-value)
  - one-part-only: N/b, not scaled up: S3:frac:1/2:12 (offered: inversion, denominator-as-decimal, place-value)
  - one-part-only: N/b, not scaled up: S3:frac:1/2:14 (offered: inversion, denominator-as-decimal, place-value)
  - one-part-only: N/b, not scaled up: S3:frac:1/2:18 (offered: inversion, denominator-as-decimal, place-value)
  - complement: the part left over: S3:frac:1/2:6 (offered: inversion, denominator-as-decimal, place-value)
  - complement: the part left over: S3:frac:1/2:8 (offered: inversion, denominator-as-decimal, place-value)
  - complement: the part left over: S3:frac:1/2:12 (offered: inversion, denominator-as-decimal, place-value)
  - complement: the part left over: S3:frac:1/2:14 (offered: inversion, denominator-as-decimal, place-value)
  - complement: the part left over: S3:frac:1/2:18 (offered: inversion, denominator-as-decimal, place-value)
  - subtract-percent: N - p: S3:pct:60:150 (offered: one-part-only, complement, place-value)
  - one-part-only: 10% only (N/10): S3:pct:10:70 (offered: subtract-percent, complement, place-value)
  - one-part-only: 10% only (N/10): S3:pct:10:150 (offered: subtract-percent, complement, place-value)
  - one-part-only: 10% only (N/10): S3:pct:10:230 (offered: subtract-percent, complement, place-value)
  - one-part-only: 10% only (N/10): S3:pct:10:480 (offered: subtract-percent, complement, place-value)

### free-daily-pizza: stage 4
- question space: 84 items (the whole bank); enumerated (FDP.BANK, built by FDP.buildBank from its parameter lists)
- marking: multiple choice, the option's key (form and exact value; a simplest-form fraction by the numbers shown)
- collisions with the key: **4**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| inversion: the whole over the part | coincidence | 84 | 0 |
| part-to-part: the part over the rest | coincidence | 84 | 0 |
| complement: the rest over the whole | agree | 84 | 4 |
| raw-part: the part as the percentage (A%) | agree | 42 | 0 |
| place-value: x10 | coincidence | 42 | 0 |
| place-value: /10 | coincidence | 42 | 0 |
  - complement: the rest over the whole: S4:f:7/14 (offered: unsimplified, inversion, part-to-part)
  - complement: the rest over the whole: S4:p:7/14 (offered: raw-part, part-to-part, inversion)
  - complement: the rest over the whole: S4:f:15/30 (offered: unsimplified, inversion, part-to-part)
  - complement: the rest over the whole: S4:p:15/30 (offered: raw-part, part-to-part, inversion)

### trig-worms: find the angle
- question space: 588 questions (POOL: every angle, hypotenuse and ratio served); enumerated (POOL, read from the page)
- marking: multiple choice; angles to the nearest degree, sides to 1 d.p. (half up), each computed from the sides as shown (1 d.p.)
- collisions with the key: **128**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| other inverse: sin<->cos (or sin/cos for tan) | coincidence | 588 | 6 |
| tan-1 of the ratio (wrong inverse) | coincidence | 414 | 8 |
| ratio upside down | coincidence | 588 | 38 |
| ratio rounded to 1 d.p. first | coincidence | 556 | 76 |
| the other angle: 90 - theta | coincidence | 588 | 0 |
| calculator in radians (radians read as degrees) | coincidence | 588 | 0 |
| cos-1 instead of tan-1 (of the smaller over the larger) | coincidence | 174 | 0 |
  - other inverse: sin<->cos (or sin/cos for tan): angle 15 deg, hyp 9, TOA: key 15 deg
  - other inverse: sin<->cos (or sin/cos for tan): angle 15 deg, hyp 11, TOA: key 15 deg
  - other inverse: sin<->cos (or sin/cos for tan): angle 15 deg, hyp 14, TOA: key 15 deg
  - other inverse: sin<->cos (or sin/cos for tan): angle 15 deg, hyp 16, TOA: key 15 deg
  - other inverse: sin<->cos (or sin/cos for tan): angle 15 deg, hyp 19, TOA: key 15 deg
  - tan-1 of the ratio (wrong inverse): angle 15 deg, hyp 8, SOH: key 15 deg
  - tan-1 of the ratio (wrong inverse): angle 15 deg, hyp 10, SOH: key 15 deg
  - tan-1 of the ratio (wrong inverse): angle 15 deg, hyp 13, SOH: key 15 deg
  - tan-1 of the ratio (wrong inverse): angle 15 deg, hyp 15, SOH: key 15 deg
  - tan-1 of the ratio (wrong inverse): angle 15 deg, hyp 17, SOH: key 15 deg
  - ratio upside down: angle 75 deg, hyp 8, CAH: key 75 deg
  - ratio upside down: angle 75 deg, hyp 10, CAH: key 75 deg
  - ratio upside down: angle 75 deg, hyp 13, CAH: key 75 deg
  - ratio upside down: angle 75 deg, hyp 15, CAH: key 75 deg
  - ratio upside down: angle 75 deg, hyp 17, CAH: key 75 deg
  - ratio rounded to 1 d.p. first: angle 35 deg, hyp 8, TOA: key 35 deg
  - ratio rounded to 1 d.p. first: angle 35 deg, hyp 9, TOA: key 35 deg
  - ratio rounded to 1 d.p. first: angle 35 deg, hyp 10, TOA: key 35 deg
  - ratio rounded to 1 d.p. first: angle 35 deg, hyp 12, TOA: key 35 deg
  - ratio rounded to 1 d.p. first: angle 35 deg, hyp 13, TOA: key 35 deg

### trig-worms: find the side
- question space: 412 questions (POOL: every angle, hypotenuse and ratio served); enumerated (POOL, read from the page)
- marking: multiple choice; angles to the nearest degree, sides to 1 d.p. (half up), each computed from the sides as shown (1 d.p.)
- collisions with the key: **0**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| the other ratio (sin<->cos) | coincidence | 412 | 0 |
| tan instead | coincidence | 412 | 0 |
| divided instead of multiplied | coincidence | 412 | 0 |
| calculator in radians | coincidence | 412 | 0 |

### trig-worms: find the hypotenuse
- question space: 204 questions (POOL: every angle, hypotenuse and ratio served); enumerated (POOL, read from the page)
- marking: multiple choice; angles to the nearest degree, sides to 1 d.p. (half up), each computed from the sides as shown (1 d.p.)
- collisions with the key: **0**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| multiplied instead of divided | coincidence | 204 | 0 |
| cos instead of sin | coincidence | 204 | 0 |
| tan instead of sin | coincidence | 204 | 0 |
| calculator in radians | coincidence | 204 | 0 |

### distinctly-average: mean
- question space: 73 items (the whole pool, KS3 and GCSE); enumerated (window.DA_ITEMS: the items the page itself builds)
- marking: multiple choice, by dataset.val string
- collisions with the key: **116**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| the total, not divided | coincidence | 73 | 0 |
| divided by n - 1 | coincidence | 73 | 0 |
| divided by n + 1 | coincidence | 73 | 0 |
| the median instead of the mean | agree | 73 | 73 |
| the mode instead of the mean | agree | 43 | 43 |
| the largest value | coincidence | 73 | 0 |
  - the median instead of the mean: ks3_mean_0: data [1, 3, 2, 2, 2], key 2
  - the median instead of the mean: ks3_mean_1: data [5, 9, 7, 7, 7], key 7
  - the median instead of the mean: ks3_mean_2: data [2, 16, 9, 9, 9], key 9
  - the median instead of the mean: ks3_mean_3: data [7, 15, 11, 11, 11], key 11
  - the median instead of the mean: ks3_mean_4: data [12, 14, 13, 13, 13], key 13
  - the mode instead of the mean: ks3_mean_0: data [1, 3, 2, 2, 2], key 2
  - the mode instead of the mean: ks3_mean_1: data [5, 9, 7, 7, 7], key 7
  - the mode instead of the mean: ks3_mean_2: data [2, 16, 9, 9, 9], key 9
  - the mode instead of the mean: ks3_mean_3: data [7, 15, 11, 11, 11], key 11
  - the mode instead of the mean: ks3_mean_4: data [12, 14, 13, 13, 13], key 13

### distinctly-average: median
- question space: 58 items (the whole pool, KS3 and GCSE); enumerated (window.DA_ITEMS: the items the page itself builds)
- marking: multiple choice, by dataset.val string
- collisions with the key: **0**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| middle of the list as given (not sorted) | coincidence | 58 | 0 |
| the position (n+1)/2, not the value | coincidence | 58 | 0 |
| the mean instead of the median | agree | 58 | 0 |
| one of the two middle values (even n) | agree | 21 | 0 |
| the mode instead of the median | agree | 0 | 0 |

### distinctly-average: modeUnique
- question space: 33 items (the whole pool, KS3 and GCSE); enumerated (window.DA_ITEMS: the items the page itself builds)
- marking: multiple choice, by dataset.val string
- collisions with the key: **44**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| the frequency, not the value | coincidence | 33 | 0 |
| the largest value | coincidence | 33 | 0 |
| the smallest value | coincidence | 33 | 0 |
| the median instead of the mode | agree | 33 | 31 |
| the mean instead of the mode | agree | 33 | 13 |
  - the median instead of the mode: ks3_modeU_160: data [3, 6, 4, 5, 4], key 4
  - the median instead of the mode: ks3_modeU_161: data [6, 8, 7, 7, 7], key 7
  - the median instead of the mode: ks3_modeU_162: data [10, 13, 11, 12, 11], key 11
  - the median instead of the mode: ks3_modeU_163: data [13, 16, 14, 15, 14], key 14
  - the median instead of the mode: ks3_modeU_164: data [16, 18, 17, 17, 17], key 17
  - the mean instead of the mode: ks3_modeU_161: data [6, 8, 7, 7, 7], key 7
  - the mean instead of the mode: ks3_modeU_164: data [16, 18, 17, 17, 17], key 17
  - the mean instead of the mode: ks3_modeU_168: data [9, 13, 10, 12, 11, 11], key 11
  - the mean instead of the mode: ks3_modeU_169: data [12, 16, 13, 15, 14, 14], key 14
  - the mean instead of the mode: ks3_modeU_173: data [5, 9, 6, 8, 7, 7, 7], key 7

### distinctly-average: modeBimodal
- question space: 42 items (the whole pool, KS3 and GCSE); enumerated (window.DA_ITEMS: the items the page itself builds)
- marking: multiple choice, by dataset.val string
- collisions with the key: **2**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| the two largest values | coincidence | 42 | 1 |
| the two smallest values | coincidence | 42 | 1 |
  - the two largest values: ks3_modeB_220: data [14, 20, 15, 20, 16, 18, 17, 18], key 18 and 20
  - the two smallest values: ks3_modeB_201: data [1, 5, 1, 4, 3, 3], key 1 and 3

### distinctly-average: range
- question space: 53 items (the whole pool, KS3 and GCSE); enumerated (window.DA_ITEMS: the items the page itself builds)
- marking: multiple choice, by dataset.val string
- collisions with the key: **3**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| the largest value | coincidence | 53 | 0 |
| the smallest value | coincidence | 53 | 0 |
| the mean instead of the range | coincidence | 53 | 0 |
| last minus first, in the order given | agree | 53 | 3 |
  - last minus first, in the order given: ks3_range_255: data [7, 9, 7, 9, 8, 9], key 2
  - last minus first, in the order given: ks3_range_256: data [9, 10, 9, 10, 9, 10], key 1
  - last minus first, in the order given: ks3_range_289: data [13, 14, 13, 14, 13, 14, 13, 14, 13, 14], key 1

### distinctly-average: freqMean
- question space: 20 items (the whole pool, KS3 and GCSE); enumerated (window.DA_ITEMS: the items the page itself builds)
- marking: multiple choice, by dataset.val string
- collisions with the key: **0**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| ignored the frequencies (mean of the values) | coincidence | 20 | 0 |
| sum of fx, not divided | coincidence | 20 | 0 |
| divided by the number of rows | coincidence | 20 | 0 |
| mean of the frequencies | coincidence | 20 | 0 |
| the median instead of the mean | agree | 20 | 0 |
| the modal value instead of the mean | agree | 20 | 0 |

### distinctly-average: freqMedian
- question space: 20 items (the whole pool, KS3 and GCSE); enumerated (window.DA_ITEMS: the items the page itself builds)
- marking: multiple choice, by dataset.val string
- collisions with the key: **14**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| the middle row's value (ignored the frequencies) | agree | 20 | 11 |
| the position (n+1)/2, not the value | coincidence | 20 | 0 |
| the mean instead of the median | agree | 20 | 0 |
| the modal value instead of the median | agree | 10 | 3 |
  - the middle row's value (ignored the frequencies): gcse_freqMedian_329: data {"values": [1, 5, 9], "freqs": [3, 4, 4]}, key 5
  - the middle row's value (ignored the frequencies): gcse_freqMedian_330: data {"values": [1, 8, 15], "freqs": [4, 4, 5]}, key 8
  - the middle row's value (ignored the frequencies): gcse_freqMedian_332: data {"values": [3, 4, 5], "freqs": [3, 4, 4]}, key 4
  - the middle row's value (ignored the frequencies): gcse_freqMedian_335: data {"values": [4, 9, 14], "freqs": [3, 4, 4]}, key 9
  - the middle row's value (ignored the frequencies): gcse_freqMedian_336: data {"values": [5, 8, 11], "freqs": [4, 4, 5]}, key 8
  - the modal value instead of the median: gcse_freqMedian_345: data {"values": [2, 6, 10, 14], "freqs": [3, 3, 4, 3]}, key 10
  - the modal value instead of the median: gcse_freqMedian_348: data {"values": [5, 8, 11, 14], "freqs": [3, 3, 4, 3]}, key 11
  - the modal value instead of the median: gcse_freqMedian_351: data {"values": [10, 11, 12, 13], "freqs": [3, 3, 4, 3]}, key 12

### distinctly-average: missing
- question space: 15 items (the whole pool, KS3 and GCSE); enumerated (window.DA_ITEMS: the items the page itself builds)
- marking: multiple choice, by dataset.val string
- collisions with the key: **0**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| the mean itself | agree | 15 | 0 |
| the total of the known values | coincidence | 15 | 0 |
| mean x (n - 1) minus the knowns | coincidence | 15 | 0 |
| mean x n (the total, not less the knowns) | coincidence | 15 | 0 |

### distinctly-average: compareMean
- question space: 18 items (the whole pool, KS3 and GCSE); enumerated (window.DA_ITEMS: the items the page itself builds)
- marking: multiple choice, by dataset.val string
- collisions with the key: **45**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| compared the medians | agree | 18 | 18 |
| compared the totals | agree | 18 | 18 |
| compared the largest values | agree | 18 | 9 |
  - compared the medians: gcse_cmpMean_388: data {"a": [2, 6, 4, 4, 4], "b": [4, 6, 5, 5, 5]}, key B
  - compared the medians: gcse_cmpMean_390: data {"a": [3, 11, 7, 7, 7], "b": [14, 18, 16, 16, 16]}, key B
  - compared the medians: gcse_cmpMean_392: data {"a": [6, 12, 9, 9, 9], "b": [12, 14, 13, 13, 13]}, key B
  - compared the medians: gcse_cmpMean_394: data {"a": [6, 14, 10, 10, 10], "b": [15, 17, 16, 16, 16]}, key B
  - compared the medians: gcse_cmpMean_396: data {"a": [8, 16, 12, 12, 12], "b": [2, 12, 7, 7, 7]}, key A
  - compared the totals: gcse_cmpMean_388: data {"a": [2, 6, 4, 4, 4], "b": [4, 6, 5, 5, 5]}, key B
  - compared the totals: gcse_cmpMean_390: data {"a": [3, 11, 7, 7, 7], "b": [14, 18, 16, 16, 16]}, key B
  - compared the totals: gcse_cmpMean_392: data {"a": [6, 12, 9, 9, 9], "b": [12, 14, 13, 13, 13]}, key B
  - compared the totals: gcse_cmpMean_394: data {"a": [6, 14, 10, 10, 10], "b": [15, 17, 16, 16, 16]}, key B
  - compared the totals: gcse_cmpMean_396: data {"a": [8, 16, 12, 12, 12], "b": [2, 12, 7, 7, 7]}, key A
  - compared the largest values: gcse_cmpMean_390: data {"a": [3, 11, 7, 7, 7], "b": [14, 18, 16, 16, 16]}, key B
  - compared the largest values: gcse_cmpMean_392: data {"a": [6, 12, 9, 9, 9], "b": [12, 14, 13, 13, 13]}, key B
  - compared the largest values: gcse_cmpMean_394: data {"a": [6, 14, 10, 10, 10], "b": [15, 17, 16, 16, 16]}, key B
  - compared the largest values: gcse_cmpMean_396: data {"a": [8, 16, 12, 12, 12], "b": [2, 12, 7, 7, 7]}, key A
  - compared the largest values: gcse_cmpMean_400: data {"a": [13, 17, 15, 15, 15], "b": [1, 11, 6, 6, 6]}, key A

### distinctly-average: compareRange
- question space: 18 items (the whole pool, KS3 and GCSE); enumerated (window.DA_ITEMS: the items the page itself builds)
- marking: multiple choice, by dataset.val string
- collisions with the key: **3**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| picked the bigger range | agree | 18 | 3 |
| compared the means (lower = more consistent) | agree | 18 | 0 |
  - picked the bigger range: gcse_cmpRange_421: data {"a": [3, 5, 4, 4, 4], "b": [4, 6, 5, 5, 5]}, key They are the same
  - picked the bigger range: gcse_cmpRange_422: data {"a": [13, 19, 16, 16, 16], "b": [6, 12, 9, 9, 9]}, key They are the same
  - picked the bigger range: gcse_cmpRange_423: data {"a": [6, 8, 7, 7, 7, 7], "b": [8, 10, 9, 9, 9, 9]}, key They are the same

### distinctly-average: outlierId
- question space: 16 items (the whole pool, KS3 and GCSE); enumerated (window.DA_ITEMS: the items the page itself builds)
- marking: multiple choice, by dataset.val string
- collisions with the key: **16**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| picked the largest value | agree | 16 | 8 |
| picked the smallest value | agree | 16 | 8 |
  - picked the largest value: gcse_outId_424: data [32, 20, 22, 21, 19], key 32
  - picked the largest value: gcse_outId_425: data [28, 26, 24, 41, 25], key 41
  - picked the largest value: gcse_outId_426: data [23, 46, 24, 28, 26], key 46
  - picked the largest value: gcse_outId_427: data [6, 21, 6, 9, 7, 8, 7], key 21
  - picked the largest value: gcse_outId_428: data [20, 24, 21, 23, 22, 20, 39], key 39
  - picked the smallest value: gcse_outId_432: data [30, 32, 31, 18, 33], key 18
  - picked the smallest value: gcse_outId_433: data [17, 1, 21, 16, 19], key 1
  - picked the smallest value: gcse_outId_434: data [43, 37, 41, 39, 17], key 17
  - picked the smallest value: gcse_outId_435: data [22, 25, 22, 24, 23, 10, 26], key 10
  - picked the smallest value: gcse_outId_436: data [20, 22, 21, 2, 24, 19, 23], key 2

### distinctly-average: outlierMean, outlierCompare
- question space: 32 items; enumerated (window.DA_ITEMS)
- marking: multiple choice, worded options
- collisions with the key: **0**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
- note: not recomputed: three worded options, each wrong one a named error that is a different word from the key

### quadratic-factoriser: GCSE, x^2 + bx + c = (x + p)(x + q)
- question space: 174 questions (the whole pool); enumerated (QF_POOLS.gcse)
- marking: the pair p, q picked from a grid, exact, either order
- collisions with the key: **13**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| signs flipped: the roots, not the factors (-p, -q) | agree | 174 | 12 |
| sum and product swapped (p + q = c, pq = b) | coincidence | 174 | 1 |
  - signs flipped: the roots, not the factors (-p, -q): x^2 +0x -1 = (x +1)(x -1)
  - signs flipped: the roots, not the factors (-p, -q): x^2 +0x -4 = (x +2)(x -2)
  - signs flipped: the roots, not the factors (-p, -q): x^2 +0x -9 = (x +3)(x -3)
  - signs flipped: the roots, not the factors (-p, -q): x^2 +0x -16 = (x +4)(x -4)
  - signs flipped: the roots, not the factors (-p, -q): x^2 +0x -25 = (x +5)(x -5)
  - sum and product swapped (p + q = c, pq = b): x^2 +4x +4 = (x +2)(x +2)

### quadratic-factoriser: GCSE Higher, ax^2 + bx + c
- question space: 3760 questions (the whole pool, base and HCF); enumerated (QF_POOLS.higher)
- marking: guided steps (multiple choice), then the factors
- collisions with the key: **454**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| the two constants swapped: (px + s)(rx + q) | agree | 3760 | 440 |
| both signs flipped: (px - q)(rx - s) | coincidence | 3760 | 0 |
| step 2 (find ac): a x b | coincidence | 752 | 7 |
| step 2 (find ac): b x c | coincidence | 752 | 5 |
| step 2 (find ac): a + c | coincidence | 752 | 2 |
| step 2 (find ac): a - c | coincidence | 752 | 0 |
  - the two constants swapped: (px + s)(rx + q): 2x^2 -15x +25 = (1x -5)(2x -5)
  - the two constants swapped: (px + s)(rx + q): 2x^2 -9x +9 = (1x -3)(2x -3)
  - the two constants swapped: (px + s)(rx + q): 2x^2 -3x +1 = (1x -1)(2x -1)
  - the two constants swapped: (px + s)(rx + q): 2x^2 +3x +1 = (1x +1)(2x +1)
  - the two constants swapped: (px + s)(rx + q): 2x^2 +9x +9 = (1x +3)(2x +3)
  - step 2 (find ac): a x b: 2x^2 -1x -1: ac = -2
  - step 2 (find ac): a x b: 2x^2 +9x +9: ac = 18
  - step 2 (find ac): a x b: 3x^2 -4x -4: ac = -12
  - step 2 (find ac): a x b: 3x^2 +16x +16: ac = 48
  - step 2 (find ac): a x b: 4x^2 -9x -9: ac = -36
  - step 2 (find ac): b x c: 4x^2 +4x -15: ac = -60
  - step 2 (find ac): b x c: 4x^2 +4x -3: ac = -12
  - step 2 (find ac): b x c: 4x^2 +4x +1: ac = 4
  - step 2 (find ac): b x c: 9x^2 +9x -4: ac = -36
  - step 2 (find ac): b x c: 9x^2 +9x +2: ac = 18
  - step 2 (find ac): a + c: 2x^2 -5x +2: ac = 4
  - step 2 (find ac): a + c: 2x^2 +5x +2: ac = 4

### quadratic-factoriser: the quadratic formula
- question space: 1254 questions (the whole pool: 1070 real, 184 no real roots); enumerated (QF_POOLS.formula)
- marking: two typed roots, each round2 (2 d.p., Math.round), either order; or 'No real solutions'
- collisions with the key: **736**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| +b instead of -b (the game's own diagnosis), real roots | coincidence | 1070 | 0 |
| only the square root divided by 2a (the game's own diagnosis), real roots | coincidence | 1070 | 0 |
| divided by a, not 2a (the game's own diagnosis), real roots | coincidence | 1070 | 0 |
| b^2 taken as negative (the game's own diagnosis), real roots | coincidence | 1070 | 0 |
| b^2 + 4ac (sign of 4ac slipped), real roots | coincidence | 1070 | 0 |
| +b instead of -b (the game's own diagnosis), no real roots | agree | 184 | 184 |
| only the square root divided by 2a (the game's own diagnosis), no real roots | agree | 184 | 184 |
| divided by a, not 2a (the game's own diagnosis), no real roots | agree | 184 | 184 |
| b^2 taken as negative (the game's own diagnosis), no real roots | agree | 184 | 184 |
| b^2 + 4ac (sign of 4ac slipped), no real roots | agree | 184 | 0 |
  - +b instead of -b (the game's own diagnosis), no real roots: 1x^2 -5x +7: no real roots
  - +b instead of -b (the game's own diagnosis), no real roots: 1x^2 -4x +5: no real roots
  - +b instead of -b (the game's own diagnosis), no real roots: 1x^2 -4x +8: no real roots
  - +b instead of -b (the game's own diagnosis), no real roots: 1x^2 -3x +4: no real roots
  - +b instead of -b (the game's own diagnosis), no real roots: 1x^2 -3x +7: no real roots
  - only the square root divided by 2a (the game's own diagnosis), no real roots: 1x^2 -5x +7: no real roots
  - only the square root divided by 2a (the game's own diagnosis), no real roots: 1x^2 -4x +5: no real roots
  - only the square root divided by 2a (the game's own diagnosis), no real roots: 1x^2 -4x +8: no real roots
  - only the square root divided by 2a (the game's own diagnosis), no real roots: 1x^2 -3x +4: no real roots
  - only the square root divided by 2a (the game's own diagnosis), no real roots: 1x^2 -3x +7: no real roots
  - divided by a, not 2a (the game's own diagnosis), no real roots: 1x^2 -5x +7: no real roots
  - divided by a, not 2a (the game's own diagnosis), no real roots: 1x^2 -4x +5: no real roots
  - divided by a, not 2a (the game's own diagnosis), no real roots: 1x^2 -4x +8: no real roots
  - divided by a, not 2a (the game's own diagnosis), no real roots: 1x^2 -3x +4: no real roots
  - divided by a, not 2a (the game's own diagnosis), no real roots: 1x^2 -3x +7: no real roots
  - b^2 taken as negative (the game's own diagnosis), no real roots: 1x^2 -5x +7: no real roots
  - b^2 taken as negative (the game's own diagnosis), no real roots: 1x^2 -4x +5: no real roots
  - b^2 taken as negative (the game's own diagnosis), no real roots: 1x^2 -4x +8: no real roots
  - b^2 taken as negative (the game's own diagnosis), no real roots: 1x^2 -3x +4: no real roots
  - b^2 taken as negative (the game's own diagnosis), no real roots: 1x^2 -3x +7: no real roots

### modular-battle: a mod b
- question space: 408 questions (408 paths walked); enumerated (generateQ driven through every randInt choice)
- marking: multiple choice of residues 0..b-1 (random others, none named); exact
- collisions with the key: **231**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| the quotient instead of the remainder | coincidence | 408 | 25 |
| b - r (counted the other way) | coincidence | 408 | 53 |
| the last digit of a | coincidence | 408 | 65 |
| the first digit after the point of a / b | coincidence | 408 | 88 |
  - the quotient instead of the remainder: 12 mod 5: key 2
  - the quotient instead of the remainder: 14 mod 6: key 2
  - the quotient instead of the remainder: 15 mod 4: key 3
  - the quotient instead of the remainder: 16 mod 7: key 2
  - the quotient instead of the remainder: 18 mod 5: key 3
  - b - r (counted the other way): 11 mod 2: key 1
  - b - r (counted the other way): 12 mod 8: key 4
  - b - r (counted the other way): 13 mod 2: key 1
  - b - r (counted the other way): 14 mod 4: key 2
  - b - r (counted the other way): 15 mod 2: key 1
  - the last digit of a: 10 mod 2: key 0
  - the last digit of a: 11 mod 2: key 1
  - the last digit of a: 11 mod 5: key 1
  - the last digit of a: 12 mod 5: key 2
  - the last digit of a: 13 mod 5: key 3
  - the first digit after the point of a / b: 11 mod 8: key 3
  - the first digit after the point of a / b: 11 mod 9: key 2
  - the first digit after the point of a / b: 12 mod 9: key 3
  - the first digit after the point of a / b: 13 mod 6: key 1
  - the first digit after the point of a / b: 13 mod 9: key 4

### factor-race: KS3/GCSE pairs
- question space: 2694 ordered pairs (VALID_PAIRS); enumerated (VALID_PAIRS)
- marking: two cards: which has more factors (exact counts)
- collisions with the key: **0**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| the bigger number has more factors | two-way | 2694 | 1718 |
| the even number has more factors (pairs of mixed parity) | two-way | 1506 | 1438 |
  - the bigger number has more factors: 2 v 4
  - the bigger number has more factors: 2 v 6
  - the bigger number has more factors: 2 v 8
  - the bigger number has more factors: 2 v 9
  - the bigger number has more factors: 2 v 10
  - the even number has more factors (pairs of mixed parity): 3 v 4
  - the even number has more factors (pairs of mixed parity): 3 v 6
  - the even number has more factors (pairs of mixed parity): 3 v 8
  - the even number has more factors (pairs of mixed parity): 3 v 10
  - the even number has more factors (pairs of mixed parity): 3 v 12

### fraction-equivalence: KS3/GCSE
- question space: 940 distinct questions (5580 paths walked); enumerated (generateQ driven through every randInt and Math.random choice)
- marking: Yes / No: equivalent?
- collisions with the key: **0**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| additive: equivalent when top and bottom differ by the same amount | two-way | 940 | 705 |
| only the tops checked (numerator a multiple: always yes) | two-way | 940 | 235 |
  - additive: equivalent when top and bottom differ by the same amount: 1/2 v 2/5: key False
  - additive: equivalent when top and bottom differ by the same amount: 2/3 v 4/7: key False
  - additive: equivalent when top and bottom differ by the same amount: 2/3 v 6/10: key False
  - additive: equivalent when top and bottom differ by the same amount: 2/3 v 6/11: key False
  - additive: equivalent when top and bottom differ by the same amount: 2/3 v 6/12: key False
  - only the tops checked (numerator a multiple: always yes): 1/2 v 2/4
  - only the tops checked (numerator a multiple: always yes): 2/3 v 4/6
  - only the tops checked (numerator a multiple: always yes): 2/3 v 6/9
  - only the tops checked (numerator a multiple: always yes): 2/3 v 8/12
  - only the tops checked (numerator a multiple: always yes): 2/3 v 10/15

### bearing-blitz: the 16 fixed bearings (in every game)
- question space: 16 bearings; enumerated (generateBearings' fixed list read from the page; the random ones are Math.floor(Math.random()*360))
- marking: needle within 5 degrees (TOLERANCE)
- collisions with the key: **4**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| anticlockwise from north (360 - b) | agree | 16 | 2 |
| the back bearing (b + 180) | coincidence | 16 | 0 |
| the maths angle: anticlockwise from east (90 - b) | agree | 16 | 2 |
| clockwise from east (b - 90) | coincidence | 16 | 0 |
  - anticlockwise from north (360 - b): target 000
  - anticlockwise from north (360 - b): target 180
  - the maths angle: anticlockwise from east (90 - b): target 045
  - the maths angle: anticlockwise from east (90 - b): target 225

### bearing-blitz: every bearing 0-359 (the 8 random ones per game)
- question space: 360 bearings; enumerated (generateBearings' fixed list read from the page; the random ones are Math.floor(Math.random()*360))
- marking: needle within 5 degrees (TOLERANCE)
- collisions with the key: **20**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| anticlockwise from north (360 - b) | agree | 360 | 10 |
| the back bearing (b + 180) | coincidence | 360 | 0 |
| the maths angle: anticlockwise from east (90 - b) | agree | 360 | 10 |
| clockwise from east (b - 90) | coincidence | 360 | 0 |
  - anticlockwise from north (360 - b): target 000
  - anticlockwise from north (360 - b): target 001
  - anticlockwise from north (360 - b): target 002
  - anticlockwise from north (360 - b): target 178
  - anticlockwise from north (360 - b): target 179
  - the maths angle: anticlockwise from east (90 - b): target 043
  - the maths angle: anticlockwise from east (90 - b): target 044
  - the maths angle: anticlockwise from east (90 - b): target 045
  - the maths angle: anticlockwise from east (90 - b): target 046
  - the maths angle: anticlockwise from east (90 - b): target 047

### shape-shifter: Rotation
- question space: 15 questions (ROTATION_QUESTIONS, built once at load); enumerated
- marking: multiple choice of 4 shapes (named-error options)
- collisions with the key: **0**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| wrong direction (-angle) | coincidence | 15 | 0 |
| reflected in the y-axis | coincidence | 15 | 0 |
| reflected in the x-axis | coincidence | 15 | 0 |
| wrong centre (1, 1) | coincidence | 15 | 0 |
| 90 for 180, or 180 for 90 | coincidence | 15 | 0 |

### equatle: the equation bank
- question space: 23399 equations (getBank(); 4430 mix + or - with x or /); enumerated (getBank)
- marking: the guess must be a true equation (JavaScript precedence) and the exact target string
- collisions with the key: **3093**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| left to right, ignoring x and / first (mixed-operation equations) | agree | 4430 | 3093 |
  - left to right, ignoring x and / first (mixed-operation equations): 2*3-4=02
  - left to right, ignoring x and / first (mixed-operation equations): 7*8+5=61
  - left to right, ignoring x and / first (mixed-operation equations): 6*5-8=22
  - left to right, ignoring x and / first (mixed-operation equations): 63/7-2=7
  - left to right, ignoring x and / first (mixed-operation equations): 66/6-2=9

### log-laws: Solve, F1
- question space: 94 items (the whole family); enumerated (LL_SOLVE.families, built from parameter lists; no random draw)
- marking: typed, to 3 significant figures (an unrounded value is a format notice, not marked)
- collisions with the key: **0**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| the game's own misDivide: log(b/a) (base 10) | coincidence | 94 | 0 |
| the game's own misDivide: ln(b/a) | coincidence | 94 | 0 |
| ratio upside down: log a / log b | coincidence | 94 | 0 |
| no logs: b / a | coincidence | 94 | 0 |
| log for ln, mixed: log b / ln a | coincidence | 94 | 0 |
| subtracted the logs: log b - log a | coincidence | 94 | 0 |

### log-laws: Solve, F2
- question space: 108 items (the whole family); enumerated (LL_SOLVE.families, built from parameter lists; no random draw)
- marking: typed, to 3 significant figures (an unrounded value is a format notice, not marked)
- collisions with the key: **0**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| the game's own misDivide: log(b/a) / k (base 10) | coincidence | 48 | 0 |
| the game's own misDivide: ln(b/a) / k | coincidence | 48 | 0 |
| the game's own misK: k left out | coincidence | 48 | 0 |
| multiplied by k instead of dividing | coincidence | 48 | 0 |
| ratio upside down: k log a / log b | coincidence | 48 | 0 |
| log for ln, mixed: log b / (k ln a) | coincidence | 48 | 0 |
| the game's own misDivide: log(b/a) - k (base 10) | coincidence | 60 | 0 |
| the game's own misDivide: ln(b/a) - k | coincidence | 60 | 0 |
| the game's own misK: the shift left out | coincidence | 60 | 0 |
| the shift's sign slipped (+k for -k) | coincidence | 60 | 0 |
| ratio upside down, then the shift | coincidence | 60 | 0 |

### log-laws: Solve, F3
- question space: 76 items (the whole family); enumerated (LL_SOLVE.families, built from parameter lists; no random draw)
- marking: typed, to 3 significant figures (an unrounded value is a format notice, not marked)
- collisions with the key: **10**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| the game's own misK: k left out (ln b) | coincidence | 28 | 0 |
| multiplied by k instead of dividing | coincidence | 26 | 0 |
| log for ln: log b / k | coincidence | 28 | 0 |
| multiplied by k instead of dividing [where it is the same calculation] | agree | 2 | 2 |
| the sign of k dropped (k negative) | coincidence | 4 | 0 |
| the game's own misK: the time constant left out (-ln(V/V0)) | coincidence | 40 | 0 |
| the minus sign dropped: RC ln(V/V0) | coincidence | 48 | 0 |
| log for ln: -RC log(V/V0) | coincidence | 48 | 0 |
| RC taken as R x C without the powers of ten | coincidence | 48 | 0 |
| the game's own misK: the time constant left out (-ln(V/V0)) [where it is the same calculation] | agree | 8 | 8 |
  - multiplied by k instead of dividing [where it is the same calculation]: F3-e--1-0.2: key 1.61
  - multiplied by k instead of dividing [where it is the same calculation]: F3-e--1-0.5: key 0.693
  - the game's own misK: the time constant left out (-ln(V/V0)) [where it is the same calculation]: F3-rc-12-6-10-100: key 0.693
  - the game's own misK: the time constant left out (-ln(V/V0)) [where it is the same calculation]: F3-rc-12-3.5-10-100: key 1.23
  - the game's own misK: the time constant left out (-ln(V/V0)) [where it is the same calculation]: F3-rc-12-2-10-100: key 1.79
  - the game's own misK: the time constant left out (-ln(V/V0)) [where it is the same calculation]: F3-rc-9-3-10-100: key 1.1
  - the game's own misK: the time constant left out (-ln(V/V0)) [where it is the same calculation]: F3-rc-9-4.5-10-100: key 0.693

### log-laws: Solve, F4
- question space: 80 items (the whole family); enumerated (LL_SOLVE.families, built from parameter lists; no random draw)
- marking: typed, to 3 significant figures (an unrounded value is a format notice, not marked)
- collisions with the key: **16**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| the -1 dropped: x = a / b | coincidence | 80 | 0 |
| multiplied instead of divided: x = a(b - 1) [where it is the same calculation] | agree | 16 | 16 |
| the quotient upside down: x/(x + a) = b | coincidence | 80 | 0 |
| multiplied instead of divided: x = a(b - 1) | coincidence | 64 | 0 |
  - multiplied instead of divided: x = a(b - 1) [where it is the same calculation]: F4-log-1-2: key 1.0
  - multiplied instead of divided: x = a(b - 1) [where it is the same calculation]: F4-log-2-2: key 2.0
  - multiplied instead of divided: x = a(b - 1) [where it is the same calculation]: F4-log-3-2: key 3.0
  - multiplied instead of divided: x = a(b - 1) [where it is the same calculation]: F4-log-4-2: key 4.0
  - multiplied instead of divided: x = a(b - 1) [where it is the same calculation]: F4-log-5-2: key 5.0

### log-laws: Solve, F5 (product law)
- question space: 83 items; enumerated (LL_SOLVE.families)
- marking: multiple choice: x = r, x = -s or both
- collisions with the key: **0**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
- note: not recomputed: the three options are different roots or 'both'; the game's own misRoot (keeping the negative root) is the option 'both' or x = -s, never the key

### log-laws: Solve, F6
- question space: 60 items (the whole family); enumerated (LL_SOLVE.families, built from parameter lists; no random draw)
- marking: typed, to 3 significant figures (an unrounded value is a format notice, not marked)
- collisions with the key: **20**

| error tested | kind | questions it applies to | collisions |
|---|---|---|---|
| a sign slipped (the answer's sign) | coincidence | 60 | 0 |
| k dropped [where it is the same calculation] | agree | 20 | 20 |
| ln a + ln b in the denominator | coincidence | 60 | 0 |
| ln(a/b) read as ln a / ln b | coincidence | 60 | 0 |
| k dropped | coincidence | 40 | 0 |
  - k dropped [where it is the same calculation]: F6-2-3-1: key 2.71
  - k dropped [where it is the same calculation]: F6-2-5-1: key 1.76
  - k dropped [where it is the same calculation]: F6-2-6-1: key 1.63
  - k dropped [where it is the same calculation]: F6-2-7-1: key 1.55
  - k dropped [where it is the same calculation]: F6-3-2-1: key -1.71

## Not surveyed, and why

**Fixed banks** (questions written out literally; random only shuffles): sequence-solver, estimation-golf,
prime-factorisation (a literal list of numbers), prime-or-composite, percentage-flip, 52dle, word-problem-decoder,
equation-builder, spot-the-error, gradient-hunter, truth-buster, spot-the-muppet, terrible-advice,
wrong-on-the-internet, maths-court, expected-damage, negative-number-line, think-of-a-number, formula-plug-in,
decimal-detective, four-quadrant-explorer, like-terms-collector, probability-pioneer, new-shapes, higher-power,
index-laws, surd-simplifier, proportion-blaster, trig-identity-duel, standard-form-blitz, simultaneous-solver
(generated offline, stored literally), circle-theorem-spotter, probability-paradox, angle-ace,
coordinate-geometry-dash, graph-transformer, formula-unlocked, scale-factor-scaling, unit-converter, formula-forge,
correlation-or-coincidence, chart-interrogator, component-crusher, expectation-station, better-value, given-that,
screening-room, estimation-engine, linear-equation-solver, core-maths-paper1, core-maths-paper2a,
core-maths-paper2b, core-maths-paper2c, tax-theft (20 literal salaries; its keys are computed, so it could be
surveyed the same way if wanted), stat-attack, growth-and-decay, graph-sketcher, test-the-claim,
differentiation-duel, integration-duel, suvat, curling-friction, force-resolver, moments-master, binomial-blaster,
partial-fractions-duel, proof-builder, normal-navigator, fermi-lab, dimension-checker, factor-theorem,
boolean-blitz, truth-will-set-you-free, complex-converter, matrix-crunch, characteristic-quest,
eigenvalue-extractor, eigenvector-engine, glorious-gantt (unlisted; literal networks). Several compute their keys
in code from literal data (chart-interrogator, screening-room, stat-attack, simultaneous-solver, glorious-gantt);
their numbers are still fixed, so they are outside this contract.

**No keyed answer:** trig-wars (artillery simulation), constructions-lab (unmarked construction tasks),
prisoners-dilemma (no right or wrong choice), seven-bridges (fixed graph puzzles, nothing numeric).

**Parts of surveyed games left out:** log-laws' Laws mode and shape-shifter's Translation and Reflection sets
(fixed banks); factor-race's and fraction-equivalence's Year 6 banks (fixed); log-laws F5 and distinctly-average's
outlierMean and outlierCompare (worded multiple choice whose wrong options are different words from the key by
construction); quadratic-factoriser Higher's Independent-mode pickers (the final factorised form is surveyed; the
guided steps other than step 2 are not); bearing-blitz's back bearing and east-based errors are tested, its
scoring bands are not.
