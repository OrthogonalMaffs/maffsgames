MARVIN-BALANCE (Project Claude, Wed 25 Nov 2026 08:20; checked against main 4b415e0)
Jon, 25 Nov 2026: 07:54 "as soon with a first to 10 against marvin you're almost certain to lose"; 07:59 "I want a 60-70% win chance on easy, and a 40-50% chance to win on hard"; 08:10 "please give me a contract for the change to the difficulty of marvin". Project Claude's simulation (25 Nov, 6,000-8,000 seeded games a cell, main deck, first to 10), the player modelled as picking their card's best category with probability p, otherwise a category at random:
  Marvin now:  Easy (random)   p=0: 50%  p=0.5: 84%  p=0.8: 96%  p=1: 99%
               Hard (always best)    3%         18%         42%        64%
  Chosen:      Easy best 30%        29%         67%         87%        95%
               Hard best 60%        14%         46%         72%        87%
Jon's targets are read for the typical student, p = 0.5: Easy 67%, Hard 46%.
RECOMMENDED: Opus 5.5, effort medium. A two-number change to one game's computer player, with a simulation in its verifier.
LANE: cloud (lane 1). SEND: now, straight after Jon's "yes" to #906 in the same session; start it only once #906 (BASE-60-PLAY) has merged and merge-pr.py has reported. One PR. Branch from current origin/main. No draft PR.
ORDER: this goes before TIER3-GUARD (claude/tier3-guard-contract), which follows it.

TASK: Make Marvin beatable: Easy picks his card's best category 30% of the time, Hard 60%, otherwise a category at random, so a typical student wins about two games in three on Easy and a little under half on Hard.

ROOT CAUSE: Shown in games/maffscards/index.html: the winner of a round chooses the next category (line 534-535 sets G.chooser), and Hard Marvin always takes hardChoice() (line 348), his card's best category, which wins about 86% of the rounds he chooses; once ahead he keeps choosing, so a student picking at random wins 3% of first-to-10 games against him. Easy Marvin always takes easyChoice() (line 357, a random category), so any student who plays their own best value wins 99%. Neither level is a contest.

CLASS CHECK: Local: one game's computer player. No other game has Marvin or this rule; nothing in schools/assets/ changes.

EXACT CHANGE:
0. First commit (after any claim commit): close-out for #906 BASE-60-PLAY per AGENTS.md line 62 (merge commit, route merge-pr.py, its last line, main's check-site, phone-fit-full and pages run IDs and conclusions, read back from the API); move its contract to docs/history/contracts/. Save this contract verbatim as docs/handover/contracts/2026-11-25-marvin-balance.md.
1. games/maffscards/index.html:
   a. One constant beside the other settings: MARVIN_BEST = { easy: 0.30, hard: 0.60 } with a comment naming this contract and the targets.
   b. Marvin's choice (line 456 and the functions at 348 and 357): with probability MARVIN_BEST[G.marvin], hardChoice(his card, pool); otherwise a category picked uniformly from all six (pickOne(CATS), which may be the best one). Use rng (line 326), so seeded runs stay reproducible. hardChoice itself is unchanged.
   c. The menu labels (lines 261-262): Easy's <small> "picks at random" becomes "sometimes spots his best"; Hard's "knows the deck" becomes "usually knows the deck". Nothing else on the menu changes.
   d. The test hook (around line 634): add MC.marvinBest (the constant) and keep MC.hardAll as it is (it reports the rule, which is unchanged).
2. scripts/verify-maffscards.py:
   a. The existing hard-choice check (hardAll against hard_choice, about line 248) stays: the rule for "best" is unchanged.
   b. New check, in the page with seeded play: over 2,000 of Marvin's choices per level, the share that equal his best is within 3 percentage points of 0.30 + 0.70 x (share of uniform picks that hit the best by chance) for Easy, and the same with 0.60 for Hard (compute the chance term from the deck; state it in the output).
   c. New check, in Python (the verifier's own judge and hard_choice, not the page's code), seeded and so deterministic: 2,000 first-to-10 games on the main deck for each level, a model player who picks their best category with probability 0.5, otherwise uniformly at random, the chooser rule as the page has it (the player chooses first; the round's winner chooses next; ties go to the middle pile and the chooser stays). Easy must give the player 60-74% wins, Hard 39-53% (Jon's targets with a margin for sampling). Print both rates.
   d. Plants that must fail: MARVIN_BEST.hard set to 1 (Hard back to always best); MARVIN_BEST.easy set to 0; the random branch made to choose the best category always.
   e. Update the ci-line and the docstring's "hard" description.
3. .claude/rules/game-roster.md row #114: "Marvin easy (random) or hard (the category his card beats most of the deck in)" becomes "Marvin easy (his card's best category 30% of the time, otherwise at random) or hard (60%), tuned so a typical student wins about two in three on easy and a little under half on hard (MARVIN-BALANCE, 25 Nov 2026)". Nothing else in the row.
4. The leaderboards: keep the four boards as they are (the game was listed on 24 Nov, so few scores exist). Report how many entries each board holds if the hub or Firebase shows it without new access; do not clear any.
5. updates/index.html, under November 2026 in its "Corrected" list (the page's headings are New, Corrected and Clarified; add a November "Corrected" heading in the page's form if there is none): "MaffsCards: Marvin can now be beaten. Easy is easier, and Hard is still hard but no longer unbeatable."
6. docs/handover/cloud.md entry. Merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600 on green; report its last line.

DO NOT TOUCH:
- cards.json, tools/maffscards/, the judge, the deck, the chooser rule (the winner chooses next), the tie rule, first to 10, the entire-deck cap, Marvin's lines, the boards and their keys.
- schools/assets/, every other game, canon, data/games.json.
- docs/todo.md beyond what the TODO-TRIM rule needs (no row exists for this; add none).

SUCCESS CONDITION:
- On the live page, Easy and Hard Marvin choose his best category about 30% and 60% of the time (plus chance hits), and the menu says so in plain words.
- verify-maffscards.py passes, prints the model player's win rates (inside 60-74% Easy and 39-53% Hard), and catches all three plants; the existing checks still pass.
- Roster row and /updates/ updated; #906's close-out recorded; merged through merge-pr.py; its last line reported; cloud.md records this task.

STOP IF:
- When you come to start this, #906 has not merged, or any of main's runs on its merge commit concluded anything but success.
- The verifier's model-player rates fall outside the bands with these two numbers: report the rates; do not tune the numbers yourself (Jon sets them).
- The verifier's run time grows by more than 60 seconds: report the time before and after.
- merge-pr.py cannot reach GitHub, or refuses: report its output, do not merge another way.
