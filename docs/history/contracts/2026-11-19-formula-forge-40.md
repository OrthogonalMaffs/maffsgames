FORMULA-FORGE-40, part 1 of 2. Do not start until part 2 has arrived; it ends with "END OF CONTRACT".
LANE: cloud. Send now; the cloud lane is free. TIER: Small. MODEL: Claude Code, Sonnet 5.5, medium effort.

TASK: Bring Formula Forge's GCSE bank (games/formula-forge/index.html, Q.gcse) from 29 to 40 items by adding the 11 below, verbatim. A-Level reuses Q.gcse, so it reaches 40 too.

ROOT CAUSE: Q.gcse has s1 8, s2 8, s3 7, s4 6 (29). A session deals 6 a stage, so Stage 4 deals its whole pool every play and Stage 3 nearly all of it. A class of 13 played it on 19 Nov 2026 (GA4), so students see the same items over and over.

CLASS CHECK: Local: this bank alone. Short banks are a class (todo's LEDGER-B4 rows), but each bank needs its own questions, so they're fixed one game at a time, as the rows already say.

EXACT CHANGE:
1. First commit: close out #833 FRACTION-SNAP-REBUILD (01c4c3a; main: check-site 44531744271 green on attempt 2, phone-fit-full 44531743898, pages build 44531742013; confirm from the API) in its cloud.md entry, and record the flake (attempt 1 red only because the timing upload failed with ECONNRESET; rerun once, green). Move its contract to docs/history/contracts/. Save this contract verbatim (both parts) as docs/handover/contracts/2026-11-19-formula-forge-40.md.
2. Append these items, verbatim, to the end of each Q.gcse stage array (after its last item, before its closing ]). Stage 1 gets the first block:

[s1, +2]
{formula:'A = lw',subject:'w',correct:'w = \\dfrac{A}{l}',distractors:['w = Al','w = A - l','w = \\dfrac{l}{A}'],
hint1:'w is multiplied by l. What undoes multiplying?',hint2:'Divide both sides by \\(l\\)',
steps:['A = lw','\\text{Divide both sides by } l','w = \\dfrac{A}{l}'],ctx:'Area of a rectangle'},

{formula:'D = \\dfrac{M}{V}',subject:'M',correct:'M = DV',distractors:['M = \\dfrac{D}{V}','M = \\dfrac{V}{D}','M = D + V'],
hint1:'M is divided by V. What undoes dividing?',hint2:'Multiply both sides by \\(V\\)',
steps:['D = \\dfrac{M}{V}','\\text{Multiply both sides by } V','M = DV'],ctx:'Density = mass ÷ volume'},

[s2, +2]
{formula:'y = 3x - 4',subject:'x',correct:'x = \\dfrac{y + 4}{3}',distractors:['x = \\dfrac{y - 4}{3}','x = \\dfrac{y}{3} + 4','x = 3(y + 4)'],
hint1:'Undo the subtraction first: add 4 to both sides.',hint2:'\\(y + 4 = 3x\\). Now divide by \\(3\\).',
steps:['y = 3x - 4','\\text{Add 4 to both sides}','y + 4 = 3x','\\text{Divide both sides by 3}','x = \\dfrac{y + 4}{3}'],
misconception:'Undo the operations in reverse order: the -4 was done last, so it is undone first.'},

{formula:'C = 20 + 5n',subject:'n',correct:'n = \\dfrac{C - 20}{5}',distractors:['n = \\dfrac{C + 20}{5}','n = \\dfrac{C}{5} - 20','n = 5(C - 20)'],
hint1:'Take the 20 away from both sides first.',hint2:'\\(C - 20 = 5n\\). Now divide by \\(5\\).',
steps:['C = 20 + 5n','\\text{Subtract 20 from both sides}','C - 20 = 5n','\\text{Divide both sides by 5}','n = \\dfrac{C - 20}{5}'],ctx:'A plumber charges £20 to turn up, then £5 an hour'},
[s3, +3]
{formula:'y = x^2 + 3',subject:'x',correct:'x = \\sqrt{y - 3}',distractors:['x = \\sqrt{y} - 3','x = \\sqrt{y + 3}','x = \\dfrac{y - 3}{2}'],
hint1:'Get x squared on its own first: subtract 3.',hint2:'\\(x^2 = y - 3\\). Now square root both sides.',
steps:['y = x^2 + 3','\\text{Subtract 3 from both sides}','x^2 = y - 3','\\text{Square root both sides}','x = \\sqrt{y - 3}'],
misconception:'Square root the whole side, not each term: the square root of y - 3 is not the square root of y, minus 3.'},

{formula:'V = x^3',subject:'x',correct:'x = \\sqrt[3]{V}',distractors:['x = \\dfrac{V}{3}','x = \\sqrt{V}','x = V^3'],
hint1:'x is cubed. What undoes cubing?',hint2:'Take the cube root of both sides.',
steps:['V = x^3','\\text{Cube root both sides}','x = \\sqrt[3]{V}'],ctx:'Volume of a cube',
misconception:'Cubing is not multiplying by 3, so dividing by 3 does not undo it.'},

{formula:'A = 4\\pi r^2',subject:'r',correct:'r = \\sqrt{\\dfrac{A}{4\\pi}}',distractors:['r = \\dfrac{A}{4\\pi}','r = \\sqrt{4\\pi A}','r = \\dfrac{\\sqrt{A}}{4\\pi}'],
hint1:'Get r squared on its own first: divide by 4π.',hint2:'\\(r^2 = \\dfrac{A}{4\\pi}\\). Now square root both sides.',
steps:['A = 4\\pi r^2','\\text{Divide both sides by } 4\\pi','r^2 = \\dfrac{A}{4\\pi}','\\text{Square root both sides}','r = \\sqrt{\\dfrac{A}{4\\pi}}'],ctx:'Surface area of a sphere'},
FORMULA-FORGE-40, part 2 of 2 (part 1 came first).

2 (continued).
[s4, +4]
{formula:'3x + a = x + b',subject:'x',correct:'x = \\dfrac{b - a}{2}',distractors:['x = \\dfrac{b + a}{2}','x = \\dfrac{a - b}{2}','x = \\dfrac{b - a}{4}'],
hint1:'Get every x on one side: subtract x from both sides.',hint2:'\\(2x + a = b\\). Subtract \\(a\\), then divide by \\(2\\).',
steps:['3x + a = x + b','\\text{Subtract } x \\text{ from both sides}','2x + a = b','\\text{Subtract } a','2x = b - a','x = \\dfrac{b - a}{2}'],
misconception:'Collect the x terms on one side before anything else.'},

{formula:'ax = bx + c',subject:'x',correct:'x = \\dfrac{c}{a - b}',distractors:['x = \\dfrac{c}{a + b}','x = \\dfrac{c}{b - a}','x = \\dfrac{bx + c}{a}'],
hint1:'Both sides have an x. Subtract bx from both sides.',hint2:'\\(ax - bx = c\\). Factorise: \\(x(a - b) = c\\).',
steps:['ax = bx + c','\\text{Subtract } bx','ax - bx = c','\\text{Factorise}','x(a - b) = c','x = \\dfrac{c}{a - b}'],
misconception:'An answer with x still on the right has not made x the subject.'},

{formula:'y = \\dfrac{2x + 1}{x}',subject:'x',correct:'x = \\dfrac{1}{y - 2}',distractors:['x = \\dfrac{1}{y + 2}','x = \\dfrac{y - 1}{2}','x = \\dfrac{1}{y} - 2'],
hint1:'Clear the fraction: multiply both sides by x.',hint2:'\\(xy = 2x + 1\\). Get the x terms together: \\(xy - 2x = 1\\).',
steps:['y = \\dfrac{2x + 1}{x}','\\text{Multiply both sides by } x','xy = 2x + 1','\\text{Subtract } 2x','xy - 2x = 1','\\text{Factorise}','x(y - 2) = 1','x = \\dfrac{1}{y - 2}']},

{formula:'p(x + q) = x',subject:'x',correct:'x = \\dfrac{pq}{1 - p}',distractors:['x = \\dfrac{pq}{p - 1}','x = \\dfrac{pq}{1 + p}','x = \\dfrac{q}{1 - p}'],
hint1:'Expand the bracket first.',hint2:'\\(px + pq = x\\). Get the x terms together: \\(pq = x - px\\).',
steps:['p(x + q) = x','\\text{Expand}','px + pq = x','\\text{Subtract } px','pq = x - px','\\text{Factorise}','pq = x(1 - p)','x = \\dfrac{pq}{1 - p}']},

   Result: s1 10, s2 10, s3 10, s4 10. Project Claude ran scripts/verify-formula-forge.py --against a copy of the page with these 11 added: PASS (56 items, every key solved back in SymPy, every option classified, 203 worked lines checked, every option pressed in Chromium).
3. Run verify-formula-forge.py and check-banks.py: both pass with no change to either script.
4. docs/todo.md row LEDGER-B4-FORMULA-FORGE: gcse and alevel are now 40 (FORMULA-FORGE-40, 19 Nov 2026); level4 16 stays open. todo.md must not grow. One /updates/ line: "Formula Forge: 11 more GCSE rearrangements, 10 in every stage." cloud.md entry.
5. PR, Gate and phone-fit-full green, then merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600; report its last line. No draft PR.

DO NOT TOUCH: the existing 45 items; Q.level4; the line that copies Q.gcse into Q.alevel; the verifier and check-banks.py; schools/assets/; canon; docs/handover/home.md; any other game.

SUCCESS CONDITION: Q.gcse has 10 items in each stage, the 11 above verbatim; the verifier and check-banks pass unchanged; the todo row and /updates/ are updated; the earlier PR is closed out; merged by merge-pr.py with a GREEN last line; cloud.md records it all.

STOP IF: the verifier or check-banks fails on any new item (report the item and the message; do not edit the item); a stage array isn't where this contract says; merge-pr.py can't reach GitHub; anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies (report under "Decided for you").
END OF CONTRACT
