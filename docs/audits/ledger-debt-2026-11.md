# Check-ledger debt, November 2026

Read only, from `data/check-ledger.json` on origin/main b0b55245, 9 Nov 2026 (contract DOCS-BUNDLE). Every rule with status `fail`, per game. The ledger holds the known failures `scripts/check-banks.py` tolerates (CI fails only on a failure not in the ledger, or a ledger entry that no longer reproduces), so until now they were a second backlog: each group below has a `docs/todo.md` row pointing here.

**Totals: 167 entries in 43 games.** B4 96 entries in 41 games, B7 44 entries in 4 games, B6 18 entries in 6 games, B3 8 entries in 2 games, B2 1 entry in 1 game.

**No entry is a wrong answer or wrong maths a student can see.** B6's 18 hits were read in context; B2, B3 and B4 leave every key right; B7 is spacing. The ledger's `line` fields are not quoted: they go stale on every game edit (todo LEDGER-LINE-DRIFT), and a line number inside an entry's detail may be stale too. Find an entry by its `id`.

## B4: 96 entries in 41 games

**What it checks:** A level's bank has fewer than 40 questions (the platform minimum is 40-50).

No key is wrong; bank size alone never unlists a game (SR-19). Each level is content work. Already on todo rows: angle-ace (1.52), better-value, expected-damage and wrong-on-the-internet (§5, parked bank growth), glorious-gantt (1.71, unlisted), regression-rumble (1.26, withdrawn).

| Game | Count | Levels short (questions) | Example entry |
|---|---|---|---|
| `52dle` | 2 | ks3 20, gcse 20 | `52dle::ks3`: level 'ks3' has 20 question(s), below the 40 minimum |
| `angle-ace` | 1 | gcse 35 | `angle-ace::gcse`: level 'gcse' has 35 question(s), below the 40 minimum |
| `better-value` | 1 | gcse 20 | `better-value::gcse`: level 'gcse' has 20 question(s), below the 40 minimum |
| `characteristic-quest` | 2 | further 26, level4 26 | `characteristic-quest::further`: level 'further' has 26 question(s), below the 40 minimum |
| `component-crusher` | 3 | gcse 15, alevel 15, level4 15 | `component-crusher::gcse`: level 'gcse' has 15 question(s), below the 40 minimum |
| `constructions-lab` | 2 | ks3 10, gcse 10 | `constructions-lab::ks3`: level 'ks3' has 10 question(s), below the 40 minimum |
| `core-maths-paper1` | 1 | core 36 | `core-maths-paper1::core`: level 'core' has 36 question(s), below the 40 minimum |
| `core-maths-paper2a` | 1 | core 36 | `core-maths-paper2a::core`: level 'core' has 36 question(s), below the 40 minimum |
| `core-maths-paper2b` | 1 | core 36 | `core-maths-paper2b::core`: level 'core' has 36 question(s), below the 40 minimum |
| `core-maths-paper2c` | 1 | core 36 | `core-maths-paper2c::core`: level 'core' has 36 question(s), below the 40 minimum |
| `curling-friction` | 1 | level4 20 | `curling-friction::level4`: level 'level4' has 20 question(s), below the 40 minimum |
| `dimension-checker` | 1 | level4 28 | `dimension-checker::level4`: level 'level4' has 28 question(s), below the 40 minimum |
| `eigenvalue-extractor` | 2 | further 25, level4 25 | `eigenvalue-extractor::further`: level 'further' has 25 question(s), below the 40 minimum |
| `eigenvector-engine` | 2 | further 25, level4 25 | `eigenvector-engine::further`: level 'further' has 25 question(s), below the 40 minimum |
| `estimation-golf` | 5 | year6 20, ks3 9, gcse 9, alevel 9, level4 9 | `estimation-golf::year6`: level 'year6' has 20 question(s), below the 40 minimum |
| `expected-damage` | 3 | ks3 15, gcse 20, core 15 | `expected-damage::ks3`: level 'ks3' has 15 question(s), below the 40 minimum |
| `factor-race` | 2 | year6 20, ks3 20 | `factor-race::year6`: level 'year6' has 20 question(s), below the 40 minimum |
| `fermi-lab` | 5 | ks3 12, gcse 15, alevel 13, level4 10, core 15 | `fermi-lab::ks3`: level 'ks3' has 12 question(s), below the 40 minimum |
| `force-resolver` | 1 | level4 20 | `force-resolver::level4`: level 'level4' has 20 question(s), below the 40 minimum |
| `formula-forge` | 3 | gcse 29, alevel 29, level4 16 | `formula-forge::gcse`: level 'gcse' has 29 question(s), below the 40 minimum |
| `fraction-equivalence` | 3 | year6 20, ks3 20, gcse 20 | `fraction-equivalence::year6`: level 'year6' has 20 question(s), below the 40 minimum |
| `given-that` | 4 | gcse 25, alevel 25, core 20, level4 20 | `given-that::gcse`: level 'gcse' has 25 question(s), below the 40 minimum |
| `glorious-gantt` | 2 | core 15, level4 15 | `glorious-gantt::core`: level 'core' has 15 question(s), below the 40 minimum |
| `gradient-hunter` | 3 | gcse 15, core 20, alevel 10 | `gradient-hunter::gcse`: level 'gcse' has 15 question(s), below the 40 minimum |
| `graph-sketcher` | 3 | core 15, alevel 15, level4 15 | `graph-sketcher::core`: level 'core' has 15 question(s), below the 40 minimum |
| `growth-and-decay` | 3 | core 15, alevel 15, level4 15 | `growth-and-decay::core`: level 'core' has 15 question(s), below the 40 minimum |
| `maths-court` | 3 | ks3 15, gcse 20, core 10 | `maths-court::ks3`: level 'ks3' has 15 question(s), below the 40 minimum |
| `matrix-crunch` | 2 | further 35, level4 18 | `matrix-crunch::further`: level 'further' has 35 question(s), below the 40 minimum |
| `moments-master` | 1 | level4 20 | `moments-master::level4`: level 'level4' has 20 question(s), below the 40 minimum |
| `negative-number-line` | 1 | year6 30 | `negative-number-line::year6`: level 'year6' has 30 question(s), below the 40 minimum |
| `percentage-flip` | 3 | year6 32, ks3 32, gcse 32 | `percentage-flip::year6`: level 'year6' has 32 question(s), below the 40 minimum |
| `prisoners-dilemma` | 4 | ks3 9, gcse 9, alevel 9, core 9 | `prisoners-dilemma::ks3`: level 'ks3' has 9 question(s), below the 40 minimum |
| `probability-paradox` | 2 | gcse 38, core 38 | `probability-paradox::gcse`: level 'gcse' has 38 question(s), below the 40 minimum |
| `proof-builder` | 2 | alevel 33, further 10 | `proof-builder::alevel`: level 'alevel' has 33 question(s), below the 40 minimum |
| `regression-rumble` | 3 | core 12, alevel 14, level4 14 | `regression-rumble::core`: level 'core' has 12 question(s), below the 40 minimum |
| `screening-room` | 4 | gcse 20, alevel 20, core 15, level4 15 | `screening-room::gcse`: level 'gcse' has 20 question(s), below the 40 minimum |
| `seven-bridges` | 3 | ks3 25, gcse 25, alevel 25 | `seven-bridges::ks3`: level 'ks3' has 25 question(s), below the 40 minimum |
| `stat-attack` | 3 | gcse 12, core 12, level4 12 | `stat-attack::gcse`: level 'gcse' has 12 question(s), below the 40 minimum |
| `terrible-advice` | 3 | ks3 18, gcse 20, core 12 | `terrible-advice::ks3`: level 'ks3' has 18 question(s), below the 40 minimum |
| `truth-will-set-you-free` | 1 | level4 32 | `truth-will-set-you-free::level4`: level 'level4' has 32 question(s), below the 40 minimum |
| `wrong-on-the-internet` | 3 | ks3 15, gcse 20, core 10 | `wrong-on-the-internet::ks3`: level 'ks3' has 15 question(s), below the 40 minimum |

## B7: 44 entries in 4 games

**What it checks:** A student-facing string loses a space the source has beside a word when rendered (KaTeX half), or a 26+ letter run with no space.

Lost spaces in rendered text: the words and maths are right but run together ("Thismatrixissingular"). Each game renders through its own helper, so one fix per game (the FORGE-HINT-SPACES pattern, #718).

| Game | Count | Example entry |
|---|---|---|
| `characteristic-quest` | 7 | `characteristic-quest::B7::katex[QS.s[]]::db199f74d6e9#1`: QS.s[] at rkI:141: 'Diagonal matrix: (5-\\lambda)(2-\\lambda) = \\lambda^2 - 7\\lambda + 10 = 0' renders as 'Diagonalmatrix : (5 − λ)(2 − λ) = λ2 − 7λ + 10 = 0' (lost a space beside: Diagonal, matrix) |
| `eigenvalue-extractor` | 6 | `eigenvalue-extractor::B7::katex[QS.s[]]::4953b8128e09#1`: QS.s[] at rkI:140: 'Both eigenvalues are negative' renders as 'Botheigenvaluesarenegative' (lost a space beside: Both, are, eigenvalues, negative) |
| `equation-builder` | 1 | `equation-builder::B7::katex[QUESTIONS.slots[]]::02d9dd5fb6a1#1`: QUESTIONS.slots[] at renderContent:436, renderContent:438, renderContent:532: 'cos C' renders as 'cosC' (lost a space beside: cos) |
| `matrix-crunch` | 30 | `matrix-crunch::B7::katex[QUESTIONS.steps[]]::daa28352576b#1`: QUESTIONS.steps[] at rkStr:385: 'All rotation matrices have determinant 1' renders as 'Allrotationmatriceshavedeterminant1' (lost a space beside: All, determinant, have, matrices, rotation) |

## B6: 18 entries in 6 games

**What it checks:** A draft marker in student-facing prose ("let me", "wait", "hmm", ...).

Every hit read in context on 9 Nov 2026; none is a wrong answer. `terrible-advice`, `wrong-on-the-internet` and `maths-court` (two arguments marked `correct:false`) put the words in a character's deliberately flawed reasoning; `expected-damage`, `probability-paradox` and `test-the-claim` use "wait" in its ordinary sense (a wait at a bus stop, a waiting time). One fix across games: the rule needs a way to accept deliberate character voice and ordinary uses, then these 18 entries leave the ledger.

| Game | Count | Example entry |
|---|---|---|
| `expected-damage` | 2 | `expected-damage::65373feb50d7#1::B6`: QUESTIONS.core[3]: 'wait' in "Track A leads to a group of people who have just discovered their horoscope says today is 'a day of transformation'. Fou" |
| `maths-court` | 2 | `maths-court::830a63e2ae15#1::B6`: QUESTIONS.gcse[10]: 'wait' in 'IQR = 67 + 42 = 109... no wait.' |
| `probability-paradox` | 5 | `probability-paradox::ca42ff7e8e2f#1::B6`: PARADOX_QUESTIONS[9]: 'wait' in "What's the average time you'll wait?" |
| `terrible-advice` | 4 | `terrible-advice::88c23e93dd87#1::B6`: QUESTIONS.gcse[2]: 'wait' in '2x + y = 10 and x + y = 7. To solve, subtract the second from the first: x = 3. Then substitute: 3 + y = 7, so y = 4. Wa' |
| `test-the-claim` | 1 | `test-the-claim::d6f5a808697a#1::B6`: QUESTIONS.normal[7]: 'wait' in 'A hospital claims mean waiting time 45 minutes, σ = 12 minutes. A sample of 36 patients has mean wait 48.5 minutes. Test' |
| `wrong-on-the-internet` | 4 | `wrong-on-the-internet::c78e6636a74a#1::B6`: QUESTIONS.ks3[7]: 'wait' in "1, 4, 9, 16... next term is 25! Add 3, then 5, then 7, then 9. So add 9 to get 25. Wait that's right. I'm a genius." |

## B3: 8 entries in 2 games

**What it checks:** Duplicate questions within a level (exact, and separately whitespace/case-normalised).

No key is wrong. `moments-master`'s pair is two different questions that share a label and an answer (todo §4 item 11: B3 compares only that signature).

| Game | Count | Example entry |
|---|---|---|
| `angle-ace` | 7 | `angle-ace::B3::15b87acff70e#1+47973aeed575#1+b991f023ff76#1+e17606d98f26#1`: QUESTIONS_BY_LEVEL.year6[33]: exact duplicate of angle-ace::QUESTIONS_BY_LEVEL.year6[30]: 'What type of angle pair is this? :: Corresponding angles (equal)' |
| `moments-master` | 1 | `moments-master::B3::0ee1eced903f#1+6919f65f41d8#1`: QUESTIONS.alevel[29]: exact duplicate of moments-master::QUESTIONS.alevel[18]: '\\text{Moments about left support} :: 75 \\text{ N}' |

## B2: 1 entry in 1 game

**What it checks:** Duplicate options, the correct one included, compared as `dataset.val` compares them (`String(value)`).

The key is right; the duplicate leaves the question with 3 options, not 4. Already todo row 1.4 (a 4th distractor, Jon).

| Game | Count | Example entry |
|---|---|---|
| `matrix-crunch` | 1 | `matrix-crunch::0a3572e58f4d#1::B2`: QUESTIONS.further.det[13]: duplicate option(s): ['0'] in ['0', '12', '0', '6'] |
