# 6 P's review fixes: report (27 Oct 2026; Jon's contract SIX-PS-REVIEW-FIXES, items 1-13)

**Result:** items 1-13 done. Eight rules (a)-(h) are in `scripts/six_ps_rules.py`, run over every question of every bank by `gen-six-ps.py --check`, each with a planted case that must be caught (`selftest()`, 20 cases, part of `--check`). The mechanical cases are fixed for every bank by `apply_review_fixes` in `gen-six-ps.py`, after the builders and before the diagram check; no bank is edited by hand and **no stored answer value changed** (the only option change is item 1's distractor). Probability Pioneer was fixed at source (`games/probability-pioneer/index.html`, its verifier `verify-probability-pioneer.py`, the `STAGE1` data). `gen-six-ps.py --check` passes on all 34 banks; `verify-the-6-ps.py` parts 1-4 pass; `verify-probability-pioneer.py` passes with 12 planted faults caught. Review sheet republished to https://claude.ai/artifact/FHXCnemqt489oVZXribfFS (version 6).

## The rules
| | Rule | Where fixed | Questions changed |
|---|---|---|---|
| a | no choice has two options of equal value | `powers-roots-7a198409` 25^3 -> 10^3 ("multiplied the base by the first power") | 1 |
| b | accept rule "simplest" says "simplest form" in the stem | `fix_simplest`, every bank | 18 (fdp-convert) |
| c | a slip is stored at full precision (a stated rounding is kept) | `fix_slips`: averages, compound-measures, pythagoras | 22 + 11 + 10 |
| d | the last worked line states the stored answer | `fix_answer_line` ("The answer: ..."), every bank | 79 |
| e | no raw backslash outside maths | `data/six-ps/authored.json` (4 occurrences of `\\'`) | 3 stems |
| f | a diagram whose working uses a right angle marks it | `right_angle_marked` (area); `area-594fb670` 12 m label moved to the dashed height line | 5 + 1 |
| g | a likelihood item stores `likelihood {n, d}`, the word matches its band | Probability Pioneer `STAGE1.p` -> `likelihood` | 10 |
| h | words never typeset inside KaTeX; `P( )` holds a short event only | `unword_maths` (141 linear-equations + 40 pythagoras working lines), Probability Pioneer stems | 181 + 27 |

## Counts changed per topic (against main before this PR)

| topic | questions | changed |
|---|---|---|
| area | 60 | diagram 6 |
| averages | 60 | slip 22 |
| basic-probability | 39 | stem 27, worked 15, options 10, slip 5 |
| compound-measures | 60 | slip 11 |
| direct-proportion | 60 | worked 30 |
| fdp-convert | 60 | stem 18, worked 5 |
| form-expressions | 30 | worked 1, stem 3 |
| fraction-operations | 60 | worked 60 |
| linear-equations | 141 | worked 141 |
| metric-units | 48 | worked 1 |
| pie-charts | 60 | worked 6 |
| powers-roots | 32 | worked 24, options 1 |
| pythagoras | 60 | slip 10, worked 40 |
| quadratics-factorise | 60 | slip 60 |
| sequences | 50 | worked 2, slip 2 |
| simultaneous | 48 | worked 2 |
| standard-form | 50 | worked 2 |

(`worked` = working lines, `slip` = slip values or lines, `diagram` = right-angle marks and one label, `options` = item 1's distractor and the rewritten Probability Pioneer statements, `stem` = the stems below. Stored answers changed: 0.)

## Items 9 and 10: Probability Pioneer, at source
**Stage 1 (the likelihood items): five judgement events replaced, every event now calculable; `p` stored for each.**
| was | now | p | word |
|---|---|---|---|
| You will breathe today | You will roll a number less than 7 on a standard dice | 6/6 | Certain |
| It will rain somewhere in Britain this week | You pick a card that is not a heart from a standard pack | 39/52 | Likely |
| You win the lottery with one ticket (sat at 0.25) | You flip two fair coins and get two heads | 1/4 | Unlikely |
| A baby born today is a boy | You roll a number greater than 2 on a dice | 4/6 | Likely |
| The sun will rise tomorrow | A randomly chosen month has fewer than 32 days | 12/12 | Certain |
Kept (already calculable): roll a 7 (0/6), flip heads (1/2), a month starting with J (3/12), a red card (26/52), an even number (3/6). The lottery snag is gone with the event: no event left sits on the scale at a value its probability does not give (the scale's points are 0, 0.25, 0.5, 0.75 and 1, and each event's probability is on its own point or in its word's band).

**Stage 2 (20 items): every `P(...)` stem is now the exam wording** ("A bag contains 8 red counters and 2 yellow counters. A counter is taken at random. Write down the probability that the counter is yellow."), in the game and in the bank (+ "Give your answer as a fraction."). **Stage 3: four statements rewritten** as sentences: "The probability of an impossible event is 0", "The probability of a certain event is 1", "A probability can be 1.5", "The probability of rolling a 7 on an ordinary dice is 7/6". **"die" -> "dice"** throughout the game (start line, 4 other places). The game verifier now holds: `p` stored and in its band, no `P( )` holding a situation, no "die", Stage 2 stems read by new readers (the key recomputed from the words), 5 new planted faults.

## Every stem rewritten, by topic

**basic-probability (27)**

- Which word best describes how likely this is? You will breathe today.  ->  Which word best describes how likely this is? You will roll a number less than 7 on a standard dice.
- Which word best describes how likely this is? You will roll a 7 on a standard die.  ->  Which word best describes how likely this is? You will roll a 7 on a standard dice.
- Which word best describes how likely this is? It will rain somewhere in Britain this week.  ->  Which word best describes how likely this is? You pick a card that is not a heart from a standard pack.
- Which word best describes how likely this is? You roll an even number on a die.  ->  Which word best describes how likely this is? You roll an even number on a dice.
- Which word best describes how likely this is? You win the lottery with one ticket.  ->  Which word best describes how likely this is? You flip two fair coins and get two heads.
- Which word best describes how likely this is? A baby born today is a boy.  ->  Which word best describes how likely this is? You roll a number greater than 2 on a dice.
- Which word best describes how likely this is? The sun will rise tomorrow.  ->  Which word best describes how likely this is? A randomly chosen month has fewer than 32 days.
- Work out \(P(\text{rolling a 6 on a fair die})\). Give your answer as a fraction.  ->  A fair dice is rolled. Write down the probability of rolling a 6. Give your answer as a fraction.
- Work out \(P(\text{picking red from 3 red, 7 blue})\). Give your answer as a fraction.  ->  A bag contains 3 red counters and 7 blue counters. A counter is taken at random. Write down the probability that the counter is red. Give your answer as a fraction.
- Work out \(P(\text{flipping tails on a fair coin})\). Give your answer as a fraction.  ->  A fair coin is flipped. Write down the probability of getting tails. Give your answer as a fraction.
- Work out \(P(\text{vowel from A, B, C, D, E})\). Give your answer as a fraction.  ->  Five cards show the letters A, B, C, D and E. A card is taken at random. Write down the probability that the letter is a vowel. Give your answer as a fraction.
- Work out \(P(\text{rolling less than 3 on a die})\). Give your answer as a fraction.  ->  A fair dice is rolled. Write down the probability of rolling a number less than 3. Give your answer as a fraction.
- Work out \(P(\text{blue from 4 red, 6 blue})\). Give your answer as a fraction.  ->  A bag contains 4 red counters and 6 blue counters. A counter is taken at random. Write down the probability that the counter is blue. Give your answer as a fraction.
- Work out \(P(\text{odd on a die})\). Give your answer as a fraction.  ->  A fair dice is rolled. Write down the probability of rolling an odd number. Give your answer as a fraction.
- Work out \(P(\text{heart from 52 cards})\). Give your answer as a fraction.  ->  A card is taken at random from a pack of 52 playing cards. Write down the probability that the card is a heart. Give your answer as a fraction.
- Work out \(P(\text{rolling greater than 4 on a dice})\). Give your answer as a fraction.  ->  A fair dice is rolled. Write down the probability of rolling a number greater than 4. Give your answer as a fraction.
- Work out \(P(\text{green from 5 red, 3 green, 2 yellow})\). Give your answer as a fraction.  ->  A bag contains 5 red counters, 3 green counters and 2 yellow counters. A counter is taken at random. Write down the probability that the counter is green. Give your answer as a fraction.
- Work out \(P(\text{multiple of 3 on a die})\). Give your answer as a fraction.  ->  A fair dice is rolled. Write down the probability of rolling a multiple of 3. Give your answer as a fraction.
- Work out \(P(\text{consonant from M, A, T, H, S})\). Give your answer as a fraction.  ->  Five cards show the letters M, A, T, H and S. A card is taken at random. Write down the probability that the letter is a consonant. Give your answer as a fraction.
- Work out \(P(\text{heads twice in a row with a fair coin})\). Give your answer as a fraction.  ->  A fair coin is flipped twice. Write down the probability of getting heads both times. Give your answer as a fraction.
- Work out \(P(\text{rolling 1 or 2 on a fair die})\). Give your answer as a fraction.  ->  A fair dice is rolled. Write down the probability of rolling a 1 or a 2. Give your answer as a fraction.
- Work out \(P(\text{picture card (J, Q or K) from a pack of 52})\). Give your answer as a fraction.  ->  A card is taken at random from a pack of 52 playing cards. Write down the probability that the card is a picture card (J, Q or K). Give your answer as a fraction.
- Work out \(P(\text{prime on a die})\). Give your answer as a fraction.  ->  A fair dice is rolled. Write down the probability of rolling a prime number. Give your answer as a fraction.
- Work out \(P(\text{yellow from 8 red, 2 yellow})\). Give your answer as a fraction.  ->  A bag contains 8 red counters and 2 yellow counters. A counter is taken at random. Write down the probability that the counter is yellow. Give your answer as a fraction.
- Work out \(P(\text{square number on a die})\). Give your answer as a fraction.  ->  A fair dice is rolled. Write down the probability of rolling a square number. Give your answer as a fraction.
- Work out \(P(\text{even from 1–8})\). Give your answer as a fraction.  ->  A number is chosen at random from 1, 2, 3, 4, 5, 6, 7, 8. Write down the probability that the number is even. Give your answer as a fraction.
- Work out \(P(\text{letter in MATHS also in GAMES})\). Give your answer as a fraction.  ->  A letter is chosen at random from the word MATHS. Write down the probability that the letter is also in the word GAMES. Give your answer as a fraction.

**fdp-convert (18)**

- Write \(0.5\) as a fraction.  ->  Write \(0.5\) as a fraction in its simplest form.
- Write \(50\%\) as a fraction.  ->  Write \(50\%\) as a fraction in its simplest form.
- Write \(75\%\) as a fraction.  ->  Write \(75\%\) as a fraction in its simplest form.
- Write \(0.2\) as a fraction.  ->  Write \(0.2\) as a fraction in its simplest form.
- Write \(60\%\) as a fraction.  ->  Write \(60\%\) as a fraction in its simplest form.
- Write \(0.8\) as a fraction.  ->  Write \(0.8\) as a fraction in its simplest form.
- Write \(0.7\) as a fraction.  ->  Write \(0.7\) as a fraction in its simplest form.
- Write \(70\%\) as a fraction.  ->  Write \(70\%\) as a fraction in its simplest form.
- Write \(0.\dot{6}\) as a fraction.  ->  Write \(0.\dot{6}\) as a fraction in its simplest form.
- Write \(66\dfrac{2}{3}\%\) as a fraction.  ->  Write \(66\dfrac{2}{3}\%\) as a fraction in its simplest form.
- Write \(0.375\) as a fraction.  ->  Write \(0.375\) as a fraction in its simplest form.
- Write \(37.5\%\) as a fraction.  ->  Write \(37.5\%\) as a fraction in its simplest form.
- Write \(0.35\) as a fraction.  ->  Write \(0.35\) as a fraction in its simplest form.
- Write \(35\%\) as a fraction.  ->  Write \(35\%\) as a fraction in its simplest form.
- Write \(0.03\) as a fraction.  ->  Write \(0.03\) as a fraction in its simplest form.
- Write \(3\%\) as a fraction.  ->  Write \(3\%\) as a fraction in its simplest form.
- Write \(0.21\) as a fraction.  ->  Write \(0.21\) as a fraction in its simplest form.
- Write \(21\%\) as a fraction.  ->  Write \(21\%\) as a fraction in its simplest form.

**form-expressions (3)**

- A bill of £\(b\) is shared equally between 3 people. Write an expression for each person\'s share, in pounds.  ->  A bill of £\(b\) is shared equally between 3 people. Write an expression for each person's share, in pounds.
- Priya is \(p\) years old. Her brother is 6 years younger than her. Write an expression for her brother\'s age.  ->  Priya is \(p\) years old. Her brother is 6 years younger than her. Write an expression for her brother's age.
- Sam is \(s\) years old. His mother is three times as old as Sam. Write an expression for his mother\'s age in 5 years\' time.  ->  Sam is \(s\) years old. His mother is three times as old as Sam. Write an expression for his mother's age in 5 years' time.

## Items 11-13, the page and the topic list
- **11 Results screen.** Not reproduced in Chromium (resume, a restored page, the page script run twice, a reload, Send: one of everything every time). Why #562's rule missed it: it made the two *lists* clear-then-draw (`fill`), but the legend, the Send button, the "Another six" button and the form around them were static markup no render touched, so a repeated copy of them (Jon saw the tick list from Quadratic graphs on, with two Send buttons: a tail that includes Send cannot come from the lists) was never cleared. Fixed at the cause: everything on the results screen is drawn into one container (`#resultsBody`, `replaceChildren`) on every render; delegated listeners on `#results`. New check `check_results_once` (part 3): one list, form, legend, Send, Another six, heading, each topic row and tick once, after the finish, after the page script runs twice, after Send, after a restore and a reload; two planted duplicates (a cloned form, a repeated tick) caught.
- **12 Marks wording.** "worth about N marks across the three Foundation papers" (page and verifier). The coming-soon line "about N marks a series" is left (a different, short phrase; say if it should follow).
- **13 Constructions** is `NOT_OFFERED` in `gen-exam-topics.py` (kept in the file under `not_offered` with its marks, so the audit still sums to 300 and a regeneration cannot bring it back as coming soon): not in "Coming soon", not in the tick list. The page has no "practised on paper" note, so it is left out entirely.
- **Header.** "Question k of 5 · Topic n of 6" is now "Question k of 5"; the slim title line carries the topic.
- **Item 8 (done, it was quick).** fraction-operations: the working no longer speaks of chocolate bars ("cut one whole into 3 equal pieces, take 1"), 60 questions. quadratics-factorise: slip lines say "the number on its own" and "the number in front of x" instead of b and c, 60 questions.

## Decided for you
- **Rule (d) is applied to every bank**, so 79 questions across 8 topics gained a closing line ("The answer: ..."), not only direct-proportion's 30 and metric-units' one; where a solution already had five lines the answer is joined to the last line.
- **Rule (c) counts more than the review's 22 / 16 / 10.** averages 22 (the 10 mean questions plus 12 mean slips stored at 1 d.p.), compound-measures 11, pythagoras 10; a question that states a rounding keeps its slips at that rounding (the rule's "no rounding instruction" condition).
- **Rule (h) is wider than the review**: it also unwords 141 linear-equations and 40 pythagoras working lines (`\text{Subtract } 7 \text{ from both sides}` became "Subtract 7 from both sides"); a single-word `\text{Mean}` label and units are allowed.
- **Statements that keep `P( )`**: "If P(rain) = 0.4, it will rain on exactly 4 out of every 10 days" (a short event, and a statement about what a probability means, not a likelihood item). Say if "rain" should go too.
- **Rule (d) for choices with a long text label** ("Yes, it's the family stand") compares the label's text with the last line; both were satisfied by the appended answer line.
- **`likelihood` is a new optional field** (docs/six-ps-schema.md); the page ignores it.
- Nothing needed the three STOP IFs: no other game's data was at fault, no cloud-lane file was touched, Probability Pioneer's bank stayed at 39 (10 + 20 + 9 true statements; 30 needed).
