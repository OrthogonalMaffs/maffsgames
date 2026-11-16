PERCENTAGE-FLIP-BANKS (Project Claude, Sun 15 Nov 2026 23:20; Jon's rulings 22:52)
Recommended: Opus, effort medium: one game rebuilt on a bank written and checked in full below; the work is routing, marking and a verifier, not content.
LANE: cloud. SEND: Mon 16 Nov, first thing (cloud lane free since #792; main unchanged at 14b8711 since this was written). A live-game correctness fix, so it goes ahead of PRINTABLES-CORE whenever Tes publishes the Core packs. TIER: Medium (merge on green; Project Claude reviews after the merge; Jon plays all three levels after it). One PR, branched from current origin/main.
LANE EXCEPTION (AGENTS.md: contract exceptions must be explicit): this PR also edits index.html (Percentage Flip's card only), essentials/index.html (its link only), spec-map/index.html (row N12's Percentage Flip link only), leaderboards/index.html (its row only) and /updates/, because the false claim and the missing GCSE entry point live there. It does not edit schools/assets/, canon, docs/todo.md, the roster's listed section or any Gate file.
CLOSE-OUT (first commit, AGENTS.md:61): CONTENT-SAFETY-COVERAGE merged #792, d64b788; main check-site 43764352225 and phone-fit-full 43764352219 green. Move docs/handover/contracts/2026-11-15-content-safety-coverage.md to docs/history/contracts/ with those figures and its merge route. Save this contract verbatim as docs/handover/contracts/2026-11-16-percentage-flip-banks.md in the same commit.
MERGE: python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600 on a green Gate; report its last line.

JON'S RULINGS (Sun 15 Nov 2026, 22:52, "All recommended"; quote them in the PR body):
1. GCSE range: grades 1-4 (percentage of an amount, increase and decrease, one number as a percentage of another, percentage change, simple interest) plus a small top band of reverse percentages; no compound interest.
2. Non-calculator throughout, numbers chosen for mental methods.
3. The Essentials page links the GCSE level once its bank exists.
4. "Questions get harder as you go" is made true: each game is served easiest first, in bands.

TASK: Rebuild Percentage Flip's question banks and routing so Year 6, KS3 and GCSE each draw from their own bank of 40 questions served easiest first, every typed answer is marked by MaffsAnswer, working is shown in KaTeX, and every link and leaderboard reaches the level it names.

ROOT CAUSE (main 14b8711, games/percentage-flip/index.html):
- One bank for two levels: gameLevel = 'year6' or else 'all' (:254); QUESTIONS_DEFAULT (12 items, :215-230) serves KS3 and GCSE alike; QUESTIONS_YEAR6 has 20 (:232-253). All three levels are below the 40 minimum (check-banks B4; data/check-ledger.json "percentage-flip::year6/ks3/gcse"; todo LEDGER-B4-PERCENTAGE-FLIP, 3.11). extract-banks reads the two flat arrays as one pool of 32 at every level.
- False claims: the start screen says "Questions get harder as you go" (:162) and the portal card "Gets progressively harder. Great GCSE prep." (index.html:1077), but startGame() takes shuffle(QUESTIONS).slice(0,10) (:263), which discards the order.
- No way into GCSE: the portal card (index.html), spec-map N12 and parents/fractions (:110) link ?level=ks3; the Essentials page links ?level=year6. The leaderboard hub lists ['year6','all'] (leaderboards/index.html:186).
- Marking (todo 1.36's class): <input type="number"> (:187), parseFloat and a ±0.01 band (:313, :337), in two places, checkAnswer() and flipCard(), each with its own copy. Money and percentage answers have no box of their own.
- Working is plain text with ASCII arrows ("50% = ÷2 → 80÷2 = 40"), set by textContent (:288): an expression outside KaTeX (canon §7.1.1). The page does not load KaTeX.
- Open finding percentage-flip-f1-001 (docs/audits/findings/percentage-flip.yml): at 320x568 a wrong answer's reason and Next sit below the fold (canon §7.6.1).

CLASS CHECK:
- Banks and routing: local. One game's data and its own level switch. The extract-banks miscount is fixed by giving the page one level-keyed QUESTIONS object, which extract-banks already scopes by level (scripts/extract-banks.py, "scoped" by path[0] == level); no shared script changes.
- Marking: the class (fixed ±band, parseFloat) already has its architectural fix, MaffsAnswer in schools/assets/answer.js (todo 1.36). This game adopts it; it does not get a local marker. Within the game, checkAnswer() and flipCard() are two paths to one mark: both call one markAnswer() function.
- A typed "%" is unreadable to MaffsAnswer (answer.js NUM accepts no unit). Not fixed here (shared asset, home lane): the % is shown fixed beside the box, the box is inputmode="decimal", and an unreadable answer gets MaffsAnswer.message(). If you find another listed game that marks a typed percentage, report it in the PR body and docs/handover/cloud.md as a proposed home-lane row PERCENT-SUFFIX; do not edit answer.js.
- Fold (f1-001): local to this game's layout unless the fix needs a shared asset; then STOP.

EXACT CHANGE (all in games/percentage-flip/index.html unless named):
1. Replace QUESTIONS_DEFAULT and QUESTIONS_YEAR6 with this one object, verbatim (every key, working line and band is checked; do not edit any of it):

const QUESTIONS = {
  year6: [
    {"band": 1, "q": "What is 50% of 80?", "a": 40, "w": ["50\\% = \\tfrac{1}{2}", "80 \\div 2 = 40"]},
    {"band": 1, "q": "What is 50% of 200?", "a": 100, "w": ["50\\% = \\tfrac{1}{2}", "200 \\div 2 = 100"]},
    {"band": 1, "q": "What is 50% of 60?", "a": 30, "w": ["50\\% = \\tfrac{1}{2}", "60 \\div 2 = 30"]},
    {"band": 1, "q": "What is 50% of 140?", "a": 70, "w": ["50\\% = \\tfrac{1}{2}", "140 \\div 2 = 70"]},
    {"band": 1, "q": "What is 50% of 100?", "a": 50, "w": ["50\\% = \\tfrac{1}{2}", "100 \\div 2 = 50"]},
    {"band": 1, "q": "What is 10% of 160?", "a": 16, "w": ["10\\% = \\tfrac{1}{10}", "160 \\div 10 = 16"]},
    {"band": 1, "q": "What is 10% of 90?", "a": 9, "w": ["10\\% = \\tfrac{1}{10}", "90 \\div 10 = 9"]},
    {"band": 1, "q": "What is 10% of 40?", "a": 4, "w": ["10\\% = \\tfrac{1}{10}", "40 \\div 10 = 4"]},
    {"band": 1, "q": "What is 10% of 120?", "a": 12, "w": ["10\\% = \\tfrac{1}{10}", "120 \\div 10 = 12"]},
    {"band": 1, "q": "What is 10% of 200?", "a": 20, "w": ["10\\% = \\tfrac{1}{10}", "200 \\div 10 = 20"]},
    {"band": 2, "q": "What is 25% of 120?", "a": 30, "w": ["25\\% = \\tfrac{1}{4}", "120 \\div 4 = 30"]},
    {"band": 2, "q": "What is 25% of 80?", "a": 20, "w": ["25\\% = \\tfrac{1}{4}", "80 \\div 4 = 20"]},
    {"band": 2, "q": "What is 25% of 200?", "a": 50, "w": ["25\\% = \\tfrac{1}{4}", "200 \\div 4 = 50"]},
    {"band": 2, "q": "What is 25% of 160?", "a": 40, "w": ["25\\% = \\tfrac{1}{4}", "160 \\div 4 = 40"]},
    {"band": 2, "q": "What is 25% of 40?", "a": 10, "w": ["25\\% = \\tfrac{1}{4}", "40 \\div 4 = 10"]},
    {"band": 2, "q": "What is 75% of 40?", "a": 30, "w": ["50\\% = 20, \\; 25\\% = 10", "75\\% = 20 + 10 = 30"]},
    {"band": 2, "q": "What is 75% of 120?", "a": 90, "w": ["50\\% = 60, \\; 25\\% = 30", "75\\% = 60 + 30 = 90"]},
    {"band": 2, "q": "What is 75% of 80?", "a": 60, "w": ["50\\% = 40, \\; 25\\% = 20", "75\\% = 40 + 20 = 60"]},
    {"band": 2, "q": "What is 75% of 200?", "a": 150, "w": ["50\\% = 100, \\; 25\\% = 50", "75\\% = 100 + 50 = 150"]},
    {"band": 2, "q": "What is 75% of 160?", "a": 120, "w": ["50\\% = 80, \\; 25\\% = 40", "75\\% = 80 + 40 = 120"]},
    {"band": 3, "q": "What is 20% of 60?", "a": 12, "w": ["10\\% = 6", "20\\% = 6 \\times 2 = 12"]},
    {"band": 3, "q": "What is 20% of 350?", "a": 70, "w": ["10\\% = 35", "20\\% = 35 \\times 2 = 70"]},
    {"band": 3, "q": "What is 5% of 80?", "a": 4, "w": ["10\\% = 8", "5\\% = 8 \\div 2 = 4"]},
    {"band": 3, "q": "What is 5% of 240?", "a": 12, "w": ["10\\% = 24", "5\\% = 24 \\div 2 = 12"]},
    {"band": 3, "q": "What is 30% of 90?", "a": 27, "w": ["10\\% = 9", "30\\% = 9 \\times 3 = 27"]},
    {"band": 3, "q": "What is 40% of 50?", "a": 20, "w": ["10\\% = 5", "40\\% = 5 \\times 4 = 20"]},
    {"band": 3, "q": "What is 60% of 70?", "a": 42, "w": ["10\\% = 7", "60\\% = 7 \\times 6 = 42"]},
    {"band": 3, "q": "What is 30% of 400?", "a": 120, "w": ["10\\% = 40", "30\\% = 40 \\times 3 = 120"]},
    {"band": 3, "q": "What is 40% of 120?", "a": 48, "w": ["10\\% = 12", "40\\% = 12 \\times 4 = 48"]},
    {"band": 3, "q": "What is 60% of 250?", "a": 150, "w": ["10\\% = 25", "60\\% = 25 \\times 6 = 150"]},
    {"band": 4, "q": "What is 15% of 360?", "a": 54, "w": ["10\\% = 36, \\; 5\\% = 18", "15\\% = 36 + 18 = 54"]},
    {"band": 4, "q": "What is 15% of 80?", "a": 12, "w": ["10\\% = 8, \\; 5\\% = 4", "15\\% = 8 + 4 = 12"]},
    {"band": 4, "q": "What is 35% of 60?", "a": 21, "w": ["10\\% = 6, \\; 5\\% = 3", "30\\% = 6 \\times 3 = 18", "35\\% = 18 + 3 = 21"]},
    {"band": 4, "q": "What is 45% of 200?", "a": 90, "w": ["10\\% = 20, \\; 5\\% = 10", "40\\% = 20 \\times 4 = 80", "45\\% = 80 + 10 = 90"]},
    {"band": 4, "q": "What is 1% of 600?", "a": 6, "w": ["1\\% = \\tfrac{1}{100}", "600 \\div 100 = 6"]},
    {"band": 4, "q": "What is 1% of 300?", "a": 3, "w": ["1\\% = \\tfrac{1}{100}", "300 \\div 100 = 3"]},
    {"band": 4, "q": "What is 35% of 140?", "a": 49, "w": ["10\\% = 14, \\; 5\\% = 7", "30\\% = 14 \\times 3 = 42", "35\\% = 42 + 7 = 49"]},
    {"band": 4, "q": "What is 12 out of 25 as a percentage?", "a": 48, "u": "%", "w": ["\\frac{12}{25} = \\frac{48}{100}", "= 48\\%"]},
    {"band": 4, "q": "What is 18 out of 50 as a percentage?", "a": 36, "u": "%", "w": ["\\frac{18}{50} = \\frac{36}{100}", "= 36\\%"]},
    {"band": 4, "q": "What is 7 out of 20 as a percentage?", "a": 35, "u": "%", "w": ["\\frac{7}{20} = \\frac{35}{100}", "= 35\\%"]},
  ],
  ks3: [
    {"band": 1, "q": "What is 20% of 45?", "a": 9, "w": ["10\\% = 4.5", "20\\% = 4.5 \\times 2 = 9"]},
    {"band": 1, "q": "What is 30% of 70?", "a": 21, "w": ["10\\% = 7", "30\\% = 7 \\times 3 = 21"]},
    {"band": 1, "q": "What is 75% of 64?", "a": 48, "w": ["50\\% = 32, \\; 25\\% = 16", "75\\% = 32 + 16 = 48"]},
    {"band": 1, "q": "What is 25% of 36?", "a": 9, "w": ["25\\% = \\tfrac{1}{4}", "36 \\div 4 = 9"]},
    {"band": 1, "q": "What is 40% of 35?", "a": 14, "w": ["10\\% = 3.5", "40\\% = 3.5 \\times 4 = 14"]},
    {"band": 1, "q": "What is 5% of 60?", "a": 3, "w": ["10\\% = 6", "5\\% = 6 \\div 2 = 3"]},
    {"band": 1, "q": "What is 60% of 45?", "a": 27, "w": ["10\\% = 4.5", "60\\% = 4.5 \\times 6 = 27"]},
    {"band": 1, "q": "What is 15% of 60?", "a": 9, "w": ["10\\% = 6, \\; 5\\% = 3", "15\\% = 6 + 3 = 9"]},
    {"band": 1, "q": "What is 90% of 50?", "a": 45, "w": ["10\\% = 5", "90\\% = 5 \\times 9 = 45"]},
    {"band": 1, "q": "What is 70% of 30?", "a": 21, "w": ["10\\% = 3", "70\\% = 3 \\times 7 = 21"]},
    {"band": 2, "q": "What is 35% of 80?", "a": 28, "w": ["10\\% = 8, \\; 5\\% = 4", "30\\% = 8 \\times 3 = 24", "35\\% = 24 + 4 = 28"]},
    {"band": 2, "q": "What is 12.5% of 64?", "a": 8, "w": ["12.5\\% = \\tfrac{1}{8}", "64 \\div 8 = 8"]},
    {"band": 2, "q": "What is 1% of 250?", "a": 2.5, "w": ["1\\% = \\tfrac{1}{100}", "250 \\div 100 = 2.5"]},
    {"band": 2, "q": "What is 2% of 350?", "a": 7, "w": ["1\\% = 3.5", "2\\% = 3.5 \\times 2 = 7"]},
    {"band": 2, "q": "What is 45% of 60?", "a": 27, "w": ["10\\% = 6, \\; 5\\% = 3", "40\\% = 6 \\times 4 = 24", "45\\% = 24 + 3 = 27"]},
    {"band": 2, "q": "What is 17.5% of 40?", "a": 7, "w": ["10\\% = 4, \\; 5\\% = 2, \\; 2.5\\% = 1", "17.5\\% = 4 + 2 + 1 = 7"]},
    {"band": 2, "q": "What is 65% of 40?", "a": 26, "w": ["10\\% = 4, \\; 5\\% = 2", "60\\% = 4 \\times 6 = 24", "65\\% = 24 + 2 = 26"]},
    {"band": 2, "q": "What is 15% of 180?", "a": 27, "w": ["10\\% = 18, \\; 5\\% = 9", "15\\% = 18 + 9 = 27"]},
    {"band": 2, "q": "What is 95% of 60?", "a": 57, "w": ["10\\% = 6, \\; 5\\% = 3", "95\\% = 60 - 3 = 57"]},
    {"band": 2, "q": "What is 55% of 120?", "a": 66, "w": ["10\\% = 12, \\; 5\\% = 6", "50\\% = 12 \\times 5 = 60", "55\\% = 60 + 6 = 66"]},
    {"band": 3, "q": "Increase 60 by 15%.", "a": 69, "w": ["10\\% = 6, \\; 5\\% = 3", "15\\% = 6 + 3 = 9", "60 + 9 = 69"]},
    {"band": 3, "q": "Decrease 80 by 35%.", "a": 52, "w": ["10\\% = 8, \\; 5\\% = 4", "30\\% = 8 \\times 3 = 24", "35\\% = 24 + 4 = 28", "80 - 28 = 52"]},
    {"band": 3, "q": "Increase 240 by 5%.", "a": 252, "w": ["10\\% = 24", "5\\% = 24 \\div 2 = 12", "240 + 12 = 252"]},
    {"band": 3, "q": "Decrease 150 by 20%.", "a": 120, "w": ["10\\% = 15", "20\\% = 15 \\times 2 = 30", "150 - 30 = 120"]},
    {"band": 3, "q": "A jacket costs £45. Its price is reduced by 20%. What is the new price?", "a": 36, "u": "£", "w": ["10\\% = 4.50", "20\\% = 4.50 \\times 2 = 9", "45 - 9 = 36"]},
    {"band": 3, "q": "A ticket costs £36. The price goes up by 25%. What is the new price?", "a": 45, "u": "£", "w": ["25\\% = \\tfrac{1}{4}", "36 \\div 4 = 9", "36 + 9 = 45"]},
    {"band": 3, "q": "A 500 g bag of rice is made 12% smaller. How many grams does the new bag hold?", "a": 440, "u": "g", "w": ["10\\% = 50, \\; 1\\% = 5", "2\\% = 10", "12\\% = 50 + 10 = 60", "500 - 60 = 440"]},
    {"band": 3, "q": "What is 18 as a percentage of 40?", "a": 45, "u": "%", "w": ["\\frac{18}{40} \\times 100 = 45\\%"]},
    {"band": 3, "q": "Sam got 27 out of 30 on a test. What percentage is that?", "a": 90, "u": "%", "w": ["\\frac{27}{30} \\times 100 = 90\\%"]},
    {"band": 3, "q": "14 of the 35 students in a class walk to school. What percentage walk?", "a": 40, "u": "%", "w": ["\\frac{14}{35} \\times 100 = 40\\%"]},
    {"band": 4, "q": "A number goes up from 40 to 50. What is the percentage increase?", "a": 25, "u": "%", "w": ["\\text{change} = 10", "\\frac{10}{40} \\times 100 = 25\\%"]},
    {"band": 4, "q": "A number goes down from 80 to 60. What is the percentage decrease?", "a": 25, "u": "%", "w": ["\\text{change} = 20", "\\frac{20}{80} \\times 100 = 25\\%"]},
    {"band": 4, "q": "A bike's price rises from £120 to £150. What is the percentage increase?", "a": 25, "u": "%", "w": ["\\text{change} = 30", "\\frac{30}{120} \\times 100 = 25\\%"]},
    {"band": 4, "q": "A crowd falls from 250 to 200 people. What is the percentage decrease?", "a": 20, "u": "%", "w": ["\\text{change} = 50", "\\frac{50}{250} \\times 100 = 20\\%"]},
    {"band": 4, "q": "A plant grows from 25 cm to 40 cm tall. What is the percentage increase?", "a": 60, "u": "%", "w": ["\\text{change} = 15", "\\frac{15}{25} \\times 100 = 60\\%"]},
    {"band": 4, "q": "£200 is saved at 3% simple interest per year. How much interest is earned in 4 years?", "a": 24, "u": "£", "w": ["\\text{one year: }1\\% = 2", "3\\% = 2 \\times 3 = 6", "\\text{interest} = 6 \\times 4 = 24"]},
    {"band": 4, "q": "£500 is saved at 2% simple interest per year. How much interest is earned in 3 years?", "a": 30, "u": "£", "w": ["\\text{one year: }1\\% = 5", "2\\% = 5 \\times 2 = 10", "\\text{interest} = 10 \\times 3 = 30"]},
    {"band": 4, "q": "£1200 is saved at 5% simple interest per year. How much interest is earned in 2 years?", "a": 120, "u": "£", "w": ["\\text{one year: }10\\% = 120", "5\\% = 120 \\div 2 = 60", "\\text{interest} = 60 \\times 2 = 120"]},
    {"band": 4, "q": "What is 150% of 40?", "a": 60, "w": ["10\\% = 4", "150\\% = 4 \\times 15 = 60"]},
    {"band": 4, "q": "What is 120% of 35?", "a": 42, "w": ["10\\% = 3.5", "120\\% = 3.5 \\times 12 = 42"]},
  ],
  gcse: [
    {"band": 1, "q": "What is 35% of 260?", "a": 91, "w": ["10\\% = 26, \\; 5\\% = 13", "30\\% = 26 \\times 3 = 78", "35\\% = 78 + 13 = 91"]},
    {"band": 1, "q": "What is 15% of 240?", "a": 36, "w": ["10\\% = 24, \\; 5\\% = 12", "15\\% = 24 + 12 = 36"]},
    {"band": 1, "q": "What is 45% of 80?", "a": 36, "w": ["10\\% = 8, \\; 5\\% = 4", "40\\% = 8 \\times 4 = 32", "45\\% = 32 + 4 = 36"]},
    {"band": 1, "q": "What is 12.5% of 96?", "a": 12, "w": ["12.5\\% = \\tfrac{1}{8}", "96 \\div 8 = 12"]},
    {"band": 1, "q": "What is 65% of 140?", "a": 91, "w": ["10\\% = 14, \\; 5\\% = 7", "60\\% = 14 \\times 6 = 84", "65\\% = 84 + 7 = 91"]},
    {"band": 1, "q": "What is 2.5% of 400?", "a": 10, "w": ["10\\% = 40", "2.5\\% = 40 \\div 4 = 10"]},
    {"band": 1, "q": "What is 85% of 60?", "a": 51, "w": ["10\\% = 6, \\; 5\\% = 3", "80\\% = 6 \\times 8 = 48", "85\\% = 48 + 3 = 51"]},
    {"band": 1, "q": "What is 32% of 50?", "a": 16, "w": ["1\\% = 0.5", "32\\% = 0.5 \\times 32 = 16"]},
    {"band": 1, "q": "What is 17.5% of 120?", "a": 21, "w": ["10\\% = 12, \\; 5\\% = 6, \\; 2.5\\% = 3", "17.5\\% = 12 + 6 + 3 = 21"]},
    {"band": 1, "q": "What is 1% of 3500?", "a": 35, "w": ["1\\% = \\tfrac{1}{100}", "3500 \\div 100 = 35"]},
    {"band": 2, "q": "A phone bill of £24 a month goes up by 15%. What is the new monthly bill?", "a": 27.6, "u": "£", "w": ["10\\% = 2.40, \\; 5\\% = 1.20", "15\\% = 2.40 + 1.20 = 3.60", "24 + 3.60 = 27.60"]},
    {"band": 2, "q": "A coat costs £85. It is reduced by 20% in a sale. What is the sale price?", "a": 68, "u": "£", "w": ["10\\% = 8.50", "20\\% = 8.50 \\times 2 = 17", "85 - 17 = 68"]},
    {"band": 2, "q": "Jo earns £9.60 an hour. She gets a 5% pay rise. What is her new hourly pay?", "a": 10.08, "u": "£", "w": ["10\\% = 0.96", "5\\% = 0.96 \\div 2 = 0.48", "9.60 + 0.48 = 10.08"]},
    {"band": 2, "q": "A TV costs £350. A sale takes 30% off. What is the sale price?", "a": 245, "u": "£", "w": ["10\\% = 35", "30\\% = 35 \\times 3 = 105", "350 - 105 = 245"]},
    {"band": 2, "q": "Rent of £650 a month goes up by 4%. What is the new monthly rent?", "a": 676, "u": "£", "w": ["1\\% = 6.50", "4\\% = 6.50 \\times 4 = 26", "650 + 26 = 676"]},
    {"band": 2, "q": "A train ticket costs £56. A railcard takes 25% off. What does the ticket cost with the railcard?", "a": 42, "u": "£", "w": ["25\\% = \\tfrac{1}{4}", "56 \\div 4 = 14", "56 - 14 = 42"]},
    {"band": 2, "q": "A meal costs £35 before VAT. VAT of 20% is added. What is the total cost?", "a": 42, "u": "£", "w": ["10\\% = 3.50", "20\\% = 3.50 \\times 2 = 7", "35 + 7 = 42"]},
    {"band": 2, "q": "Lena scored 42 out of 60 on a test. What percentage did she score?", "a": 70, "u": "%", "w": ["\\frac{42}{60} \\times 100 = 70\\%"]},
    {"band": 2, "q": "12 of the 30 people on a course drive to it. What percentage is that?", "a": 40, "u": "%", "w": ["\\frac{12}{30} \\times 100 = 40\\%"]},
    {"band": 2, "q": "Ali spends £18 of his £72 budget on food. What percentage of his budget is that?", "a": 25, "u": "%", "w": ["\\frac{18}{72} \\times 100 = 25\\%"]},
    {"band": 3, "q": "A price rises from £40 to £46. What is the percentage increase?", "a": 15, "u": "%", "w": ["\\text{change} = 6", "\\frac{6}{40} \\times 100 = 15\\%"]},
    {"band": 3, "q": "A price falls from £80 to £68. What is the percentage decrease?", "a": 15, "u": "%", "w": ["\\text{change} = 12", "\\frac{12}{80} \\times 100 = 15\\%"]},
    {"band": 3, "q": "Mo buys a car for £5000 and sells it for £4000. What is his percentage loss?", "a": 20, "u": "%", "w": ["\\text{change} = 1000", "\\frac{1000}{5000} \\times 100 = 20\\%"]},
    {"band": 3, "q": "A shop buys a mug for £12 and sells it for £15. What is the percentage profit?", "a": 25, "u": "%", "w": ["\\text{change} = 3", "\\frac{3}{12} \\times 100 = 25\\%"]},
    {"band": 3, "q": "A town's population grows from 2500 to 2800. What is the percentage increase?", "a": 12, "u": "%", "w": ["\\text{change} = 300", "\\frac{300}{2500} \\times 100 = 12\\%"]},
    {"band": 3, "q": "A weekly wage rises from £300 to £315. What is the percentage increase?", "a": 5, "u": "%", "w": ["\\text{change} = 15", "\\frac{15}{300} \\times 100 = 5\\%"]},
    {"band": 3, "q": "A concert ticket drops from £64 to £48. What is the percentage decrease?", "a": 25, "u": "%", "w": ["\\text{change} = 16", "\\frac{16}{64} \\times 100 = 25\\%"]},
    {"band": 3, "q": "£800 is saved at 3% simple interest per year. How much interest is earned in 5 years?", "a": 120, "u": "£", "w": ["\\text{one year: }1\\% = 8", "3\\% = 8 \\times 3 = 24", "\\text{interest} = 24 \\times 5 = 120"]},
    {"band": 3, "q": "£2400 is saved at 1.5% simple interest per year. How much interest is earned in 2 years?", "a": 72, "u": "£", "w": ["\\text{one year: }1\\% = 24, \\; 0.5\\% = 12", "1.5\\% = 24 + 12 = 36", "\\text{interest} = 36 \\times 2 = 72"]},
    {"band": 3, "q": "£600 is saved at 4% simple interest per year. How much is in the account after 3 years?", "a": 672, "u": "£", "w": ["\\text{one year: }1\\% = 6", "4\\% = 6 \\times 4 = 24", "\\text{interest} = 24 \\times 3 = 72", "600 + 72 = 672"]},
    {"band": 4, "q": "After a 20% increase, a price is £60. What was the price before the increase?", "a": 50, "u": "£", "w": ["60 \\text{ is } 120\\% \\text{ of the original}", "20\\% = 60 \\div 6 = 10", "100\\% = 10 \\times 5 = 50"]},
    {"band": 4, "q": "After a 10% reduction, a price is £45. What was the original price?", "a": 50, "u": "£", "w": ["45 \\text{ is } 90\\% \\text{ of the original}", "10\\% = 45 \\div 9 = 5", "100\\% = 5 \\times 10 = 50"]},
    {"band": 4, "q": "A jumper costs £36 in a 25% off sale. What was the price before the sale?", "a": 48, "u": "£", "w": ["36 \\text{ is } 75\\% \\text{ of the original}", "25\\% = 36 \\div 3 = 12", "100\\% = 12 \\times 4 = 48"]},
    {"band": 4, "q": "A bill is £84 including 20% VAT. What was the bill before VAT?", "a": 70, "u": "£", "w": ["84 \\text{ is } 120\\% \\text{ of the original}", "20\\% = 84 \\div 6 = 14", "100\\% = 14 \\times 5 = 70"]},
    {"band": 4, "q": "After a 5% pay rise, Kim earns £420 a week. What did she earn before the rise?", "a": 400, "u": "£", "w": ["420 \\text{ is } 105\\% \\text{ of the original}", "5\\% = 420 \\div 21 = 20", "100\\% = 20 \\times 20 = 400"]},
    {"band": 4, "q": "A pair of trainers costs £68 after 15% off. What was the original price?", "a": 80, "u": "£", "w": ["68 \\text{ is } 85\\% \\text{ of the original}", "5\\% = 68 \\div 17 = 4", "100\\% = 4 \\times 20 = 80"]},
    {"band": 4, "q": "A game costs £27 after 40% off. What was the original price?", "a": 45, "u": "£", "w": ["27 \\text{ is } 60\\% \\text{ of the original}", "20\\% = 27 \\div 3 = 9", "100\\% = 9 \\times 5 = 45"]},
    {"band": 4, "q": "After a 30% increase, a village has 1300 people. How many people lived there before?", "a": 1000, "w": ["1300 \\text{ is } 130\\% \\text{ of the original}", "10\\% = 1300 \\div 13 = 100", "100\\% = 100 \\times 10 = 1000"]},
    {"band": 4, "q": "After a 50% price rise, a haircut costs £33. What did it cost before?", "a": 22, "u": "£", "w": ["33 \\text{ is } 150\\% \\text{ of the original}", "50\\% = 33 \\div 3 = 11", "100\\% = 11 \\times 2 = 22"]},
    {"band": 4, "q": "A cereal box holds 440 g after a 12% cut. How many grams did it hold before?", "a": 500, "u": "g", "w": ["440 \\text{ is } 88\\% \\text{ of the original}", "4\\% = 440 \\div 22 = 20", "100\\% = 20 \\times 25 = 500"]},
  ],
};

   Fields: band 1-4 (1 easiest); q the question as plain text; a the key (a number); u the answer's unit: "£" money, "%" a percentage, "g" grams, absent for a plain number; w the working, one KaTeX string per line.
2. Routing: const gameLevel = MaffsLevel.resolve(...) as now, kept to 'year6' | 'ks3' | 'gcse' (fallback 'ks3'); the pool is QUESTIONS[gameLevel]. The value 'all' goes. gameLevel is what mfg events, MaffsScoreHistory and MaffsLeaderboard.submitScore receive, so KS3 and GCSE scores go to new boards percentage_flip_ks3 and percentage_flip_gcse (the Firebase rules accept any [a-z0-9_] board, firebase/database.rules.json:10; no rules deploy). The existing percentage_flip_all board stays in Firebase, untouched and off the hub.
3. Serving: each game is 10 questions, 3 from band 1, 3 from band 2, 2 from band 3, 2 from band 4, drawn at random without repeats within each band, served in band order (all of band 1 first). Replace the sort-based shuffle with Fisher-Yates. The start screen's "Questions get harder as you go" is now true and stays.
4. Marking: one function markAnswer(raw, q) used by checkAnswer() and flipCard() alike. u "£" -> MaffsAnswer.money(raw, q.a) with the box made a money box by MaffsAnswer.moneyInput(input, '£') for that question and moneyInput(input, null) for the others (a pence key needs exactly 2 d.p.; a right amount at 1 d.p. is 'format': the format message, no mark, no event, resubmit; canon §7.1.3, SR-2, SR-3). Every other unit -> MaffsAnswer.exact(raw, q.a). 'unreadable' -> MaffsAnswer.message(), no mark. The input becomes type="text" inputmode="decimal" autocomplete="off". For "%" and "g" a fixed label after the box shows the unit (aria-hidden; the box's aria-label names it: "Your answer, as a percentage" / "in grams"). Load schools/assets/answer.js as the other money games do.
5. The flip: tapping the card with an empty box reveals the answer and counts the question wrong, as now. Tapping it with an answer typed marks that answer first through markAnswer(); on 'format' or 'unreadable' the card does not flip and the message shows. One question_answered per question either way.
6. Working: load KaTeX as games/split-it/index.html does (same version, CSS and JS); render each w line with katex.render(line, el, {throwOnError:false, displayMode:false}) into its own line of #workingsText. For a "£" item, prefix the card's answer face with £ and show pence keys to 2 d.p. (27.60, not 27.6); for "%" show the % after the number; for "g" show " g".
7. Fold (f1-001): after a wrong answer, the reason and Next are above the fold at 320x568 and 375x667, by canon §7.6.1's layout. Set the finding to status: fixed with this PR's number.
8. Links and copy: index.html card: link ?level=gcse, description "Flip the card, check the percentage. Easiest first, then harder. Year 6, KS3 and GCSE." (plain wording; no "Great GCSE prep"). essentials/index.html: ?level=year6 -> ?level=gcse. spec-map N12: ?level=gcse. parents/fractions stays ?level=ks3 (it is the fractions guide). leaderboards/index.html:186 -> ['percentage-flip','Percentage Flip',['year6','ks3','gcse']].
9. Verifier: scripts/verify-percentage-flip.py with a ci-line in the content group that keeps every group under 4 minutes. It asserts, from the page itself: 40 questions per level and 10 per band; no repeat q within a level; every key recomputed independently from its own question text (parse the numbers; percentage of, increase/decrease, out of, change, simple interest, reverse), so the script never reads a or w to grade them; the last working line ends with the key; every key a whole number or (for "£") a whole number of pence, and every non-£ key exact (no rounding asked anywhere); every w line renders through the page's own KaTeX call with no error; a played game at each level serves 3/3/2/2 in band order; marking: 27.60 right, 27.6 format with no event, £27.60 right, 27.59 wrong, "35%" unreadable with no event, 35 right on a "%" item; ?level=gcse, ?level=ks3, ?level=year6 each draw only their own bank and submit their own level; the fold at 320x568 and 375x667 after a wrong answer. Plants, each must fail: a key changed by 1; a duplicate question; a working line that does not end with the key; a band served out of order; a pence key at 1 d.p. accepted as right; GCSE routed to the KS3 bank.
10. Ledger and register: the three B4 entries for percentage-flip leave data/check-ledger.json the way the repo removes a fixed entry (check-banks must then pass B4 for this game at every level, and extract-banks must count 40 at each level). docs/audits/findings/percentage-flip.yml updated as in 7.
11. /updates/: one line in the site's plain wording, e.g. "Percentage Flip: new questions for Year 6, KS3 and GCSE, easiest first, with the working shown step by step."
12. docs/handover/cloud.md: an entry for this PR, ending with the rows for the home lane to close in docs/todo.md: 3.11, LEDGER-B4-PERCENTAGE-FLIP, and the percentage-flip parts of 1.36 and 1.35 (extract-banks count); and any PERCENT-SUFFIX report.

DO NOT TOUCH: schools/assets/ (answer.js, lock, next, keypad, level, leaderboard: use, never edit); scripts/extract-banks.py, check-banks.py and every other shared script; the bank's text, keys, bands and working (if one is wrong, STOP; do not fix it); every other game; the roster; canon; docs/todo.md; the Gate files; Firebase rules and the existing percentage_flip_all board; parents/fractions's link; the local best key pf_best; the game's look (theme, card art, colours).

SUCCESS CONDITION: ?level=year6, ks3 and gcse each serve 10 questions from their own 40-question bank, 3/3/2/2 easiest first; every answer is marked by MaffsAnswer through one function, money to the penny with the format message for 1 d.p., percentages and grams exact with their unit shown beside the box; working renders in KaTeX; after a wrong answer the reason and Next are above the fold at 320x568 and 375x667; the portal card and Essentials link GCSE and the card no longer says "Great GCSE prep"; the hub lists year6, ks3 and gcse; check-banks B4 passes for percentage-flip at all three levels and its ledger entries are gone; verify-percentage-flip.py passes and every plant fails; f1-001 fixed; merged on green; main's check-site and phone-fit-full green on the merge commit, run IDs reported; cloud.md updated and the work committed, so the home lane knows the state of play.

STOP IF: the verifier's independent recomputation disagrees with any key or working line in the bank (report the item; change nothing in the bank); extract-banks cannot count the level-keyed object per level without a change to a shared script; MaffsAnswer.moneyInput cannot switch the £ off for a non-money question without editing answer.js; the fold fix needs a shared asset change; check-leaderboard-coverage or any other site-wide check fails for a reason outside this game; the PR would need a draft.
