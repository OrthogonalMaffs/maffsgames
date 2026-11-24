HALF-THE-SIZE. Home lane. Tier: Medium: merge on green with merge-pr.py (no hold). Send: now (#893 merged as 28be68a; #892 merged as 65ae674; main green). Branch from origin/main (65ae674 or later).
From Project Claude; Jon, 23 Nov 2026: 16:47-16:50 (rename to "But It's Only Half the Size!", keep the slug, silly questions, keep the model car question and tag the game calculator required), 17:11 ("yes it does need to be katex as with every game. I like the new questions. lets run with it please").
Recommended: Claude Code, Opus, medium effort. Every value is given below. Project Claude applied the appendix, the level banks and the KaTeX rendering to a copy of main: the game's verifier, with the appendix's TARGETS and plants, PASSES (54 items, all 6 plants caught), and all 54 items' steps, notes and fraction options render through KaTeX with no raw TeX and no .katex-error (local KaTeX, Chromium, 390x844).

TASK: Rename Scale Factor Scaling to "But It's Only Half the Size!" (slug unchanged), replace its question prompts with the approved funny ones and add 8 questions, render its maths through KaTeX, serve every level at least 40 questions, and tag it calculator required.

ROOT CAUSE: Shown: games/scale-factor-scaling/index.html has no KaTeX: notation such as k², (1/2)³ = 1/8, √9 and 2.5×10⁹ is Unicode text set with textContent (:200) and innerHTML (:202); canon 7.1.1's table lists the game in group B ("no KaTeX at all"). Shown: startGame (:188) serves GCSE T1+T2+T3 = 38 questions, under the 40 minimum. Shown: the roster (.claude/rules/game-roster.md:77) tags the calculator "untagged" while T2[12] needs 4 ÷ 8000. Jon's ruling (23 Nov): the prompts are dull and the name has no character.

CLASS CHECK: Local. The prompts, the bank and the name are this game's own content. The rendering uses the existing shared layers (MaffsText for mixed prose and maths, KaTeX 0.16.9 as every KaTeX game loads it); no shared code changes. The other group-B games in canon 7.1.1 share the shape, but each one's notation is its own content and gets its own contract; this one is marked fixed in the table, as suvat is.

EXACT CHANGE:
1. First commit: the standing close-out for FORMULA-UNLOCKED-BANK (#893): record its merge commit 28be68a, route merge-pr.py, PR head runs (check-site 45233939506, phone-fit-full 45233939165) and main's (check-site 45236117062, phone-fit-full 45236117010, pages 45236116620) in docs/handover/home.md; git mv docs/handover/contracts/2026-11-23-formula-unlocked-bank.md docs/history/contracts/. In the same commit save this contract verbatim as docs/handover/contracts/2026-11-23-half-the-size.md.
2. The banks: in games/scale-factor-scaling/index.html, replace everything from "// TIER 1: AREA SCALE FACTORS" up to (not including) "function startGame(){" with APPENDIX A, verbatim (T1 15, T2 13, T3 10, T4 8, T5 8: 54 items). Every existing item keeps its answer, wrong options and order; prompts, worked steps and notes change. T5 is new.
3. Level banks (startGame, :187-190): GCSE = T1, T2, T3, T5 (46); A-Level and Level 4 = T1 to T5 (54). MAX_Q stays 20.
4. KaTeX:
   a. Load KaTeX 0.16.9 (katex.min.css, katex.min.js deferred, from cdn.jsdelivr.net, as games/suvat/index.html:18-19 does) and schools/assets/mathtext.js.
   b. Worked steps (q.s) and the note (q.mc) render through MaffsText.html(); they are authored with \( \) around the maths and plain prose around it.
   c. Options: an option whose value is a whole-number fraction a/b (e.g. 1/4, 2/27) shows as KaTeX \dfrac{a}{b}; every other option shows as text, as now. dataset.val stays the plain value (1/4, 4:25, 48 cm²): marking is unchanged and still by dataset.val. Units (cm², m³) and ratios of whole numbers (4:25) stay plain text (canon 7.1.1: a unit is not an expression).
   d. Prompts stay plain text (they hold no expressions), shown with textContent as now.
   e. The start screen: the sub-heading becomes "Length scales by \(k\). Area scales by \(k^2\). Volume scales by \(k^3\)." and the menu-info's "(2² = 4)" and "(2³ = 8)" become \(2^2 = 4\) and \(2^3 = 8\), rendered through MaffsText once KaTeX has loaded; the words are unchanged.
   f. Nothing renders before KaTeX has loaded (the script is deferred): render on its load, as the repo's other KaTeX games do. A question shown before it loads must not show raw \( \).
5. The name, "But It's Only Half the Size!", everywhere a student or teacher sees it: the h1 (:88); <title> and og:title become "But It's Only Half the Size! Area and Volume Scale Factors | MaffsGames"; the results line (:207, "Scale Factor Scaling — " becomes "But It's Only Half the Size! — "); index.html's card-title (:2032); leaderboards/index.html:242; schools/assets/firebase-leaderboard.js:87 (the name only; the key scale-factor-scaling unchanged; escape the apostrophe in single-quoted JS); spec-map/index.html:156 (link text); .claude/rules/game-roster.md:77 (name); .claude/rules/help-audit.md:44 (name). The slug, every URL, the leaderboard and localStorage keys, the GA4 game_slug, data/games.json's search_phrase and the meta description are unchanged.
6. Calculator required (canon 4.4): the roster's last column for the game becomes "required"; the page loads schools/assets/keypad.js and schools/assets/calculator.js, shows <span class="calc-badge" data-calc="required">Calculator required</span> on the start screen, and mounts MaffsCalc docked to the question card, as games/unit-converter/index.html:88-89, :103 and :252 do. scripts/check-calculator.py passes.
7. canon 7.1.1's table (docs/canon.md:905): mark `scale-factor-scaling` "✅fixed", as `suvat` is. Nothing else in canon.
8. scripts/verify-scale-factor-scaling.py:
   a. COUNTS gains 'T5': 8; TARGETS becomes APPENDIX B, verbatim; the sweep and the bank read include T5 (SWEEP_JS's tiers and the page.evaluate of the banks).
   b. PLANTS: s1-001 becomes ("T1[7]", same label, "biscuit is enlarged with length scale factor 4", "biscuit is enlarged with scale factor 4"); s1-003 becomes ("T3[8]", same label, "Two similar pies hold gravy in the ratio 8 : 27. What is the ratio of the areas", "Two pies hold gravy in the ratio 8 : 27. What is the ratio of the areas"); t1-001's "today's text" becomes APPENDIX A's T4[4] line exactly as it stands in the page (its old text unchanged). The other three plants are unchanged and still plant.
   c. A KaTeX check in Chromium, with KaTeX served from scripts/fonts/katex/ (as the repo's KaTeX checks serve it): for every item, its worked solution (showExplain) shows no raw \( or \), no .katex-error, and at least one .katex where a step or note has \( \); every fraction option shows a .katex. A new plant breaks one step's TeX (e.g. T1[1]'s \(k^2 = 3^2 = 9\) to \(k^2 = 3^2 = \dfrac{9}\)) and must be caught.
   d. The docstring's counts and level banks updated (54 items in five tiers; GCSE T1-T3 and T5, A-Level and Level 4 all five). The ci-line's text stays as it is (its label keys CI's timings).
9. /updates/: one dated line, e.g. "23 Nov 2026: Scale Factor Scaling is now But It's Only Half the Size!: funnier questions, 8 new ones, its maths in proper notation, and a calculator on screen."
10. Merge with merge-pr.py when the Gate is green; record the merge commit and main's run IDs in docs/handover/home.md; run end-task.

DO NOT TOUCH: any item's answer, wrong options or order, beyond APPENDIX A; scoring, MAX_Q, the timer policy, MaffsLock/MaffsNext use, the leaderboard key and localStorage keys; the slug and every URL; data/games.json; the portal card's description and hook (index.html:2033-2034: the title only); any other game; schools/assets/ beyond the one name in firebase-leaderboard.js; check-banks.py, bank_common.py, katex_page_common.py, check-site.py (if one needs changing, stop); data/check-ledger.json (regenerate its scale-factor-scaling entry only if CI's own ledger step requires it, and say so); canon beyond step 7, AGENTS.md, docs/todo.md, docs/handover/cloud.md; .github/workflows/, scripts/ci-*, merge-pr.py.

SUCCESS CONDITION: the page shows the new name, 54 items (T1 15, T2 13, T3 10, T4 8, T5 8), GCSE 46 and A-Level and Level 4 54; verify-scale-factor-scaling.py passes with every key recomputed from its prompt's words, every option clicked, the KaTeX check passing on all 54 items and all 7 plants caught; check-calculator.py passes with the badge and the calculator; the name is changed in every place in step 5 and nowhere else; Gate green (tier 3, B12, phone-fit included); merged; main green; home.md records it.

STOP IF: an APPENDIX A item fails the verifier (report the item and the failure; do not edit its maths or words: Project Claude rules); a plant cannot be planted or is missed; the calculator does not fit on a phone (phone-fit fails) after your second fix; a shared checker needs changing; the cloud lane has an open PR that edits games/scale-factor-scaling/ (report before pushing); a check still fails after your second fix (standing rule); merge-pr.py can't reach GitHub; anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies (report under "Decided for you").

APPENDIX A (verbatim; replaces the four tier arrays):
// TIER 1: AREA, TIER 2: VOLUME, TIER 3: REVERSE, TIER 4: CONTEXT, TIER 5: MORE (contract HALF-THE-SIZE, 23 Nov 2026)
const T1=[
{sec:'Area SF',p:'The rugby team\'s pizza is an enlargement of a normal pizza with length scale factor 2. By what factor does the area of topping grow?',c:'4',d:['2','8','16'],s:['Area SF \\(= k^2 = 2^2 = 4\\)'],mc:'Area scales by the SQUARE of the length scale factor.'},
{sec:'Area SF',p:'A herd of goats plays tug of war with a tea towel on the washing line, stretching it with length scale factor 3. By what factor has its area grown?',c:'9',d:['3','6','27'],s:['\\(k^2 = 3^2 = 9\\)']},
{sec:'Area SF',p:'Your selfie is blown up to poster size with length scale factor 4. By what factor does the area of your face grow?',c:'16',d:['4','8','64'],s:['\\(k^2 = 4^2 = 16\\)']},
{sec:'Area SF',p:'The flag for the Snail Olympics is enlarged with length scale factor 5. What is the area scale factor?',c:'25',d:['5','10','125'],s:['\\(k^2 = 5^2 = 25\\)']},
{sec:'Area SF',p:'Your teacher\'s tiny doodle of a duck is enlarged with length scale factor 10 to cover the whole classroom wall. What is the area scale factor?',c:'100',d:['10','20','1000'],s:['\\(k^2 = 10^2 = 100\\)']},
{sec:'Area SF',p:'A 12 cm² stamp showing a famous goat is enlarged so every length doubles. What is the area of the new stamp?',c:'48 cm²',d:['24 cm²','96 cm²','36 cm²'],s:['Area SF \\(= 2^2 = 4\\)','New area \\(= 12 \\times 4 = 48\\) cm²']},
{sec:'Area SF',p:'A 5 m² trampoline is rebuilt for an elephant, with every length 3 times as long. What is the new area?',c:'45 m²',d:['15 m²','125 m²','25 m²'],s:['Area SF \\(= 3^2 = 9\\)','\\(5 \\times 9 = 45\\) m²']},
{sec:'Area SF',p:'A 10 cm² biscuit is enlarged with length scale factor 4 for a giant\'s tea break. What is the new area?',c:'160 cm²',d:['40 cm²','640 cm²','80 cm²'],s:['Area SF \\(= 4^2 = 16\\)','\\(10 \\times 16 = 160\\) cm²']},
{sec:'Area SF',p:'A hamster\'s rug and its owner\'s rug are similar, with lengths in the ratio 2 : 5. What is the ratio of their areas?',c:'4:25',d:['2:5','8:125','4:5'],s:['Area ratio \\(= 2^2 : 5^2 = 4 : 25\\)']},
{sec:'Area SF',p:'Two similar triangular sandwiches have corresponding sides of 3 cm and 9 cm. What is the ratio of their areas?',c:'1:9',d:['1:3','1:27','1:6'],s:['Length SF \\(= 9 \\div 3 = 3\\)','Area ratio \\(= 1 : 3^2 = 1 : 9\\)']},
{sec:'Area SF',p:'Your favourite jumper goes in the tumble dryer and comes out with every length halved. By what factor has the area of its front changed?',c:'1/4',d:['1/2','1/8','1/16'],s:['\\(\\left(\\dfrac{1}{2}\\right)^2 = \\dfrac{1}{4}\\)'],mc:'Shrinking by half means area becomes a QUARTER, not half.'},
{sec:'Area SF',p:'A shrink ray makes the doormat one third as long in every direction. What is the area scale factor?',c:'1/9',d:['1/3','1/27','2/9'],s:['\\(\\left(\\dfrac{1}{3}\\right)^2 = \\dfrac{1}{9}\\)']},
{sec:'Area SF',p:'A 100 cm² beach towel goes on the wrong wash and every length halves. What is its new area?',c:'25 cm²',d:['50 cm²','12.5 cm²','200 cm²'],s:['Area SF \\(= \\left(\\dfrac{1}{2}\\right)^2 = \\dfrac{1}{4}\\)','\\(100 \\times \\dfrac{1}{4} = 25\\) cm²']},
{sec:'Area SF',p:'A herd of goats plays tug of war with Grandma\'s knickers on the washing line. They stretch by 50% in every direction: length scale factor 1.5. By what factor has their area grown?',c:'2.25',d:['1.5','3','4.5'],s:['\\(1.5^2 = 2.25\\)']},
{sec:'Area SF',p:'A 64 m² bouncy castle slowly deflates until every length is 0.5 times what it was. What is its new floor area?',c:'16 m²',d:['32 m²','8 m²','128 m²'],s:['\\(0.5^2 = 0.25\\)','\\(64 \\times 0.25 = 16\\) m²']},
];

const T2=[
{sec:'Volume SF',p:'A jelly mould for a wedding is twice as long in every direction as the normal one. How many times as much jelly does it hold?',c:'8',d:['2','4','16'],s:['Volume SF \\(= k^3 = 2^3 = 8\\)'],mc:'Volume scales by the CUBE of the length scale factor.'},
{sec:'Volume SF',p:'Your goldfish gets a similar bowl, 3 times as long in every direction. By what factor does the volume grow?',c:'27',d:['3','9','81'],s:['\\(k^3 = 3^3 = 27\\)']},
{sec:'Volume SF',p:'A garden gnome is enlarged with length scale factor 4 to scare off the neighbours. What is the volume scale factor?',c:'64',d:['4','16','256'],s:['\\(k^3 = 4^3 = 64\\)']},
{sec:'Volume SF',p:'A rubber duck is enlarged with length scale factor 5 for a very large bath. What is the volume scale factor?',c:'125',d:['5','25','625'],s:['\\(k^3 = 5^3 = 125\\)']},
{sec:'Volume SF',p:'A sugar cube is enlarged with length scale factor 10 for a horse with a sweet tooth. What is the volume scale factor?',c:'1000',d:['10','100','10000'],s:['\\(k^3 = 10^3 = 1000\\)']},
{sec:'Volume SF',p:'A 20 cm³ meatball is made with every length doubled for a spaghetti-eating contest. What is its new volume?',c:'160 cm³',d:['40 cm³','80 cm³','320 cm³'],s:['Volume SF \\(= 2^3 = 8\\)','\\(20 \\times 8 = 160\\) cm³']},
{sec:'Volume SF',p:'A 10 m³ hot tub is rebuilt 3 times as long in every direction, for a family of hippos. What is its new volume?',c:'270 m³',d:['30 m³','90 m³','810 m³'],s:['Volume SF \\(= 3^3 = 27\\)','\\(10 \\times 27 = 270\\) m³']},
{sec:'Volume SF',p:'A doll\'s teapot and a giant\'s teapot are similar, with lengths in the ratio 1 : 4. What is the ratio of their volumes?',c:'1:64',d:['1:4','1:16','1:256'],s:['\\(1^3 : 4^3 = 1 : 64\\)']},
{sec:'Volume SF',p:'Your teddy bear goes through the hot wash and comes out with every length halved. "But it\'s only half the size!" By what factor has its volume changed?',c:'1/8',d:['1/2','1/4','1/16'],s:['\\(\\left(\\dfrac{1}{2}\\right)^3 = \\dfrac{1}{8}\\)'],mc:'Halving the length gives ONE EIGHTH of the volume, not half.'},
{sec:'Volume SF',p:'A shrink ray hits the wheelie bin, making every length one third as long. What is the volume scale factor?',c:'1/27',d:['1/3','1/9','2/27'],s:['\\(\\left(\\dfrac{1}{3}\\right)^3 = \\dfrac{1}{27}\\)']},
{sec:'Volume SF',p:'A 1000 cm³ sandcastle bucket is copied for a toddler, with every length halved. What is its new volume?',c:'125 cm³',d:['500 cm³','250 cm³','62.5 cm³'],s:['\\(\\left(\\dfrac{1}{2}\\right)^3 = \\dfrac{1}{8}\\)','\\(1000 \\times \\dfrac{1}{8} = 125\\) cm³']},
{sec:'Volume SF',p:'The goats are back. This time they stretch a pillow by 50% in every direction: length scale factor 1.5. By what factor has its volume grown?',c:'3.375',d:['1.5','2.25','4.5'],s:['\\(1.5^3 = 3.375\\)']},
{sec:'Volume SF',p:'A toy model of the head teacher\'s car is built to a scale of 1 : 20. The real car\'s volume is 4 m³. What is the model\'s volume?',c:'0.0005 m³',d:['0.2 m³','0.01 m³','0.05 m³'],s:['Volume SF \\(= \\left(\\dfrac{1}{20}\\right)^3 = \\dfrac{1}{8000}\\)','\\(4 \\div 8000 = 0.0005\\) m³']},
];

const T3=[
{sec:'Reverse',p:'A giant\'s handkerchief is the same shape as yours, with 9 times the area. What is the length scale factor?',c:'3',d:['9','81','4.5'],s:['Length SF \\(= \\sqrt{\\text{area SF}} = \\sqrt{9} = 3\\)']},
{sec:'Reverse',p:'A poster of a cat is the same shape as the original photo, with 25 times the area. What is the length scale factor?',c:'5',d:['25','12.5','625'],s:['\\(\\sqrt{25} = 5\\)']},
{sec:'Reverse',p:'A pancake is similar to a sadder, smaller pancake, with 4 times the area. What is the length scale factor?',c:'2',d:['4','16','8'],s:['\\(\\sqrt{4} = 2\\)']},
{sec:'Reverse',p:'A big tub of ice cream is similar to a small one and holds 8 times as much. What is the length scale factor?',c:'2',d:['8','4','64'],s:['Length SF \\(= \\sqrt[3]{\\text{volume SF}} = \\sqrt[3]{8} = 2\\)']},
{sec:'Reverse',p:'A bucket of popcorn is similar to the kids\' size and holds 27 times as much. What is the length scale factor?',c:'3',d:['27','9','81'],s:['\\(\\sqrt[3]{27} = 3\\)']},
{sec:'Reverse',p:'A space hopper is pumped up, keeping its shape, until it holds 125 times its original volume. What is the length scale factor?',c:'5',d:['125','25','625'],s:['\\(\\sqrt[3]{125} = 5\\)']},
{sec:'Reverse',p:'Two similar paddling pools have floor areas in the ratio 16 : 49. What is the ratio of their lengths?',c:'4:7',d:['16:49','2:7','8:49'],s:['\\(\\sqrt{16} : \\sqrt{49} = 4 : 7\\)']},
{sec:'Reverse',p:'Two similar pies hold gravy in the ratio 8 : 27. What is the ratio of their lengths?',c:'2:3',d:['8:27','4:9','2:9'],s:['\\(\\sqrt[3]{8} : \\sqrt[3]{27} = 2 : 3\\)']},
{sec:'Reverse',p:'Two similar pies hold gravy in the ratio 8 : 27. What is the ratio of the areas of their pastry lids?',c:'4:9',d:['2:3','8:27','16:81'],s:['Length ratio \\(= 2 : 3\\)','Area ratio \\(= 2^2 : 3^2 = 4 : 9\\)'],mc:'To go from volume to area: cube root first (get the length ratio), then square.'},
{sec:'Reverse',p:'Two similar snowmen have surface areas in the ratio 9 : 25. What is the ratio of the amounts of snow in them?',c:'27:125',d:['9:25','3:5','81:625'],s:['Length ratio \\(= 3 : 5\\)','Volume ratio \\(= 3^3 : 5^3 = 27 : 125\\)']},
];

const T4=[
{sec:'Context',p:'A 5 cm cube of cheese is enlarged with scale factor 3 for a mouse\'s birthday. What is its new volume?',c:'3375 cm³',d:['375 cm³','1125 cm³','125 cm³'],s:['Original volume \\(= 5^3 = 125\\) cm³','Volume SF \\(= 3^3 = 27\\)','\\(125 \\times 27 = 3375\\) cm³']},
{sec:'Context',p:'A gobstopper of radius 2 cm is enlarged so its radius triples. By what factor does its surface area (the bit you lick) grow?',c:'9',d:['3','27','6'],s:['Surface area is an area, so its SF \\(= k^2 = 3^2 = 9\\)']},
{sec:'Context',p:'Two similar bottles of very fizzy pop are 10 cm and 30 cm tall. What is the ratio of their volumes?',c:'1:27',d:['1:3','1:9','1:81'],s:['Length SF \\(= 30 \\div 10 = 3\\)','Volume ratio \\(= 1 : 3^3 = 1 : 27\\)']},
{sec:'Context',p:'On a pirate\'s treasure map with scale 1 : 50 000, a crocodile-filled lake covers 4 cm². What is its real area?',c:'1,000,000 m²',d:['200,000 m²','50,000 m²','10,000 m²'],s:['Length SF \\(= 50\\,000\\), so area SF \\(= 50\\,000^2 = 2.5 \\times 10^9\\)','\\(4 \\times 2.5 \\times 10^9 = 1 \\times 10^{10}\\) cm²','\\(1\\) m² \\(= 100 \\times 100 = 10^4\\) cm²','\\(1 \\times 10^{10} \\div 10^4 = 1\\,000\\,000\\) m²']},
{sec:'Context',p:'Paint covers 10 m² per litre. A shed with surface area 10 m² is rebuilt with every length doubled, for a very large lawnmower. How many litres does the new shed need?',c:'4 litres',d:['2 litres','8 litres','1 litre'],s:['Surface area scales by \\(k^2 = 2^2 = 4\\)','New surface area \\(= 10 \\times 4 = 40\\) m²','\\(40 \\div 10 = 4\\) litres'],mc:'Paint covers area, so it scales by \\(k^2\\), not \\(k\\).'},
{sec:'Context',p:'A 1 : 100 model of the school weighs 50 g. The real school is made of the same stuff. How much does it weigh?',c:'50,000 kg',d:['5000 kg','500 kg','5 kg'],s:['Volume SF \\(= 100^3 = 1\\,000\\,000\\)','\\(50 \\times 1\\,000\\,000 = 50\\,000\\,000\\) g \\(= 50\\,000\\) kg'],mc:'Mass scales with volume (same material), so mass SF \\(= k^3\\).'},
{sec:'Context',p:'Two similar ice-cream cones have diameters of 6 cm and 18 cm. The small one holds 24 cm³. How much does the large one hold?',c:'648 cm³',d:['72 cm³','216 cm³','1944 cm³'],s:['Length SF \\(= 18 \\div 6 = 3\\)','Volume SF \\(= 3^3 = 27\\)','\\(24 \\times 27 = 648\\) cm³']},
{sec:'Context',p:'A photo of your dog wearing sunglasses is enlarged with scale factor 2.5. The original\'s area is 60 cm². What is the new area?',c:'375 cm²',d:['150 cm²','937.5 cm²','240 cm²'],s:['Area SF \\(= 2.5^2 = 6.25\\)','\\(60 \\times 6.25 = 375\\) cm²']},
];

const T5=[
{sec:'Area SF',p:'A slice of toast is enlarged with length scale factor 2 for a giant\'s breakfast. The normal slice has 15 cm² of butter. What area of butter does the giant\'s slice need?',c:'60 cm²',d:['30 cm²','120 cm²','225 cm²'],s:['Area SF \\(= 2^2 = 4\\)','\\(15 \\times 4 = 60\\) cm²']},
{sec:'Area SF',p:'A hamster\'s wheel is copied for a horse, with every length 6 times as long. What is the area scale factor?',c:'36',d:['6','12','216'],s:['\\(k^2 = 6^2 = 36\\)']},
{sec:'Volume SF',p:'A 2 cm³ chocolate button is enlarged so every length is 3 times as long. What is its new volume?',c:'54 cm³',d:['6 cm³','18 cm³','162 cm³'],s:['Volume SF \\(= 3^3 = 27\\)','\\(2 \\times 27 = 54\\) cm³']},
{sec:'Area SF',p:'Your sock comes out of the wash with every length 0.8 times what it was. By what factor has its area changed?',c:'0.64',d:['0.8','1.6','0.512'],s:['\\(0.8^2 = 0.64\\)']},
{sec:'Volume SF',p:'A giant\'s mug is similar to your teacher\'s and 4 times as tall. The teacher\'s holds 300 ml of tea. How much does the giant\'s hold?',c:'19.2 litres',d:['1.2 litres','4.8 litres','76.8 litres'],s:['Volume SF \\(= 4^3 = 64\\)','\\(300 \\times 64 = 19\\,200\\) ml \\(= 19.2\\) litres']},
{sec:'Area SF',p:'Two similar garden ponds have lengths in the ratio 3 : 7. What is the ratio of their surface areas?',c:'9:49',d:['3:7','9:14','27:343'],s:['\\(3^2 : 7^2 = 9 : 49\\)']},
{sec:'Reverse',p:'Two similar sandcastles have volumes in the ratio 1 : 64. What is the ratio of their heights?',c:'1:4',d:['1:8','1:16','1:64'],s:['\\(\\sqrt[3]{1} : \\sqrt[3]{64} = 1 : 4\\)']},
{sec:'Reverse',p:'A cat who has eaten all the treats gets a similar bed with 4 times the floor area. How many times as long is the new bed?',c:'2',d:['4','8','16'],s:['\\(\\sqrt{4} = 2\\)']},
];

APPENDIX B (verbatim; replaces TARGETS in scripts/verify-scale-factor-scaling.py; each answer computed from its prompt's quantities):
TARGETS = {
    'T1': [
        ('length scale factor 2. By what factor does the area', N(2 ** 2)),
        ('length scale factor 3. By what factor has its area', N(3 ** 2)),
        ('length scale factor 4. By what factor does the area', N(4 ** 2)),
        ('length scale factor 5. What is the area scale factor', N(5 ** 2)),
        ('length scale factor 10 to cover the whole classroom wall. What is the area scale factor', N(10 ** 2)),
        ('A 12 cm² stamp showing a famous goat is enlarged so every length doubles', N(12 * 2 ** 2, 'cm²')),
        ('A 5 m² trampoline is rebuilt for an elephant, with every length 3 times as long', N(5 * 3 ** 2, 'm²')),
        ('A 10 cm² biscuit is enlarged with length scale factor 4', N(10 * 4 ** 2, 'cm²')),
        ('are similar, with lengths in the ratio 2 : 5. What is the ratio of their areas', R(2 ** 2, 5 ** 2)),
        ('Two similar triangular sandwiches have corresponding sides of 3 cm and 9 cm', R(1, (9 // 3) ** 2)),
        ('comes out with every length halved. By what factor has the area', N(F(1, 2) ** 2)),
        ('one third as long in every direction. What is the area scale factor', N(F(1, 3) ** 2)),
        ('A 100 cm² beach towel goes on the wrong wash and every length halves', N(100 * F(1, 2) ** 2, 'cm²')),
        ('length scale factor 1.5. By what factor has their area', N(F(3, 2) ** 2)),
        ('A 64 m² bouncy castle slowly deflates until every length is 0.5 times', N(64 * F(1, 2) ** 2, 'm²')),
    ],
    'T2': [
        ('twice as long in every direction as the normal one. How many times as much jelly', N(2 ** 3)),
        ('3 times as long in every direction. By what factor does the volume', N(3 ** 3)),
        ('length scale factor 4 to scare off the neighbours. What is the volume scale factor', N(4 ** 3)),
        ('length scale factor 5 for a very large bath. What is the volume scale factor', N(5 ** 3)),
        ('length scale factor 10 for a horse with a sweet tooth. What is the volume scale factor', N(10 ** 3)),
        ('A 20 cm³ meatball is made with every length doubled', N(20 * 2 ** 3, 'cm³')),
        ('A 10 m³ hot tub is rebuilt 3 times as long in every direction', N(10 * 3 ** 3, 'm³')),
        ('are similar, with lengths in the ratio 1 : 4. What is the ratio of their volumes', R(1 ** 3, 4 ** 3)),
        ('comes out with every length halved. "But it\'s only half the size!" By what factor has its volume', N(F(1, 2) ** 3)),
        ('making every length one third as long. What is the volume scale factor', N(F(1, 3) ** 3)),
        ('A 1000 cm³ sandcastle bucket is copied for a toddler, with every length halved', N(1000 * F(1, 2) ** 3, 'cm³')),
        ('length scale factor 1.5. By what factor has its volume', N(F(3, 2) ** 3)),
        ("built to a scale of 1 : 20. The real car's volume is 4 m³", N(4 * F(1, 20) ** 3, 'm³')),
    ],
    'T3': [
        ('is the same shape as yours, with 9 times the area. What is the length scale factor', N(3)),  # 3 ** 2 = 9
        ('is the same shape as the original photo, with 25 times the area. What is the length scale factor', N(5)),  # 5 ** 2 = 25
        ('is similar to a sadder, smaller pancake, with 4 times the area. What is the length scale factor', N(2)),  # 2 ** 2 = 4
        ('is similar to a small one and holds 8 times as much. What is the length scale factor', N(2)),  # 2 ** 3 = 8
        ("is similar to the kids' size and holds 27 times as much. What is the length scale factor", N(3)),  # 3 ** 3 = 27
        ('keeping its shape, until it holds 125 times its original volume. What is the length scale factor', N(5)),  # 5 ** 3 = 125
        ('Two similar paddling pools have floor areas in the ratio 16 : 49. What is the ratio of their lengths', R(4, 7)),  # 4 ** 2 : 7 ** 2 = 16 : 49
        ('Two similar pies hold gravy in the ratio 8 : 27. What is the ratio of their lengths', R(2, 3)),  # 2 ** 3 : 3 ** 3 = 8 : 27
        ('Two similar pies hold gravy in the ratio 8 : 27. What is the ratio of the areas', R(2 ** 2, 3 ** 2)),  # lengths 2 : 3 from 8 : 27
        ('Two similar snowmen have surface areas in the ratio 9 : 25', R(3 ** 3, 5 ** 3)),  # lengths 3 : 5 from 9 : 25
    ],
    'T4': [
        ('A 5 cm cube of cheese is enlarged with scale factor 3', N(5 ** 3 * 3 ** 3, 'cm³')),
        ('enlarged so its radius triples. By what factor does its surface area', N(3 ** 2)),
        ('Two similar bottles of very fizzy pop are 10 cm and 30 cm tall', R(1, (30 // 10) ** 3)),
        ('with scale 1 : 50 000, a crocodile-filled lake covers 4 cm²', N(F(4 * 50000 ** 2, 100 ** 2), 'm²')),
        ('Paint covers 10 m² per litre. A shed with surface area 10 m²', N(F(10 * 2 ** 2, 10), 'litres')),  # 1 litre covers 10 m²; doubled, the area is 4 x 10 m²
        ('A 1 : 100 model of the school weighs 50 g. The real school is made of the same stuff', N(F(50 * 100 ** 3, 1000), 'kg')),
        ('Two similar ice-cream cones have diameters of 6 cm and 18 cm. The small one holds 24 cm³', N(24 * (18 // 6) ** 3, 'cm³')),
        ("enlarged with scale factor 2.5. The original's area is 60 cm²", N(60 * F(5, 2) ** 2, 'cm²')),
    ],
    'T5': [
        ("length scale factor 2 for a giant's breakfast. The normal slice has 15 cm² of butter", N(15 * 2 ** 2, 'cm²')),
        ('with every length 6 times as long. What is the area scale factor', N(6 ** 2)),
        ('A 2 cm³ chocolate button is enlarged so every length is 3 times as long', N(2 * 3 ** 3, 'cm³')),
        ('with every length 0.8 times what it was. By what factor has its area', N(F(4, 5) ** 2)),
        ("is similar to your teacher's and 4 times as tall. The teacher's holds 300 ml", N(F(300 * 4 ** 3, 1000), 'litres')),
        ('Two similar garden ponds have lengths in the ratio 3 : 7. What is the ratio of their surface areas', R(3 ** 2, 7 ** 2)),
        ('Two similar sandcastles have volumes in the ratio 1 : 64. What is the ratio of their heights', R(1, 4)),  # 1 ** 3 : 4 ** 3 = 1 : 64
        ('gets a similar bed with 4 times the floor area. How many times as long', N(2)),  # 2 ** 2 = 4
    ],
}
