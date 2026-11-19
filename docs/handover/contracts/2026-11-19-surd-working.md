# SURD-WORKING (Jon, 19 Nov 2026), verbatim, four parts

SURD-WORKING, part 1 of 4. Do not start until parts 2, 3 and 4 have arrived; part 4 ends with "END OF CONTRACT".
LANE: cloud. Send now; FACTOR-RACE-Y6-40 has merged (#836, f7fd9ad). TIER: Medium. MODEL: Claude Code, Opus 5.5, medium effort.

TASK: Surd Simplifier (games/surd-simplifier/index.html) shows a worked solution on every wrong answer, at both levels; its GCSE 1/7 item becomes 0.\dot{6}\dot{3}; its duplicate GCSE item 35 becomes 12/\sqrt{6}.

ROOT CAUSE: On main 1f88f36 a wrong answer only marks the right option and waits on Next (handle(), :294-303); no item has any working. Canon 7.6: "Any pause must have something on screen worth reading ... Show the working". Jon, 19 Nov 2026: "we need to teach WHY". Separately, GCSE :196 (0.\dot{1}4285\dot{7} = 1/7) needs 142857/999999 cancelled without a calculator, which is not GCSE method; Jon: replace at GCSE only, A-Level keeps it.

CLASS CHECK: Missing working on a wrong pause is a class (canon 7.6 names it). This contract fixes this game only, because each game's working is its own content; item 7 reports the class.

EXACT CHANGE:
1. First commit: close out #836 FACTOR-RACE-Y6-40 (f7fd9ad; read main's runs on its merge commit from the API, record them in its cloud.md entry, move its contract to docs/history/contracts/). Save this contract verbatim (all four parts) as docs/handover/contracts/2026-11-19-surd-working.md.
2. Line 196 only (the first of the two identical lines; :243 in QUESTIONS.alevel is unchanged). Replace
  {q:'0.\\dot{1}4285\\dot{7}',ask:'Convert to a fraction in its simplest form',correct:'\\dfrac{1}{7}',d:['\\dfrac{142857}{999999}','\\dfrac{1}{9}','\\dfrac{14}{99}']},
with
  {q:'0.\\dot{6}\\dot{3}',ask:'Convert to a fraction in its simplest form',correct:'\\dfrac{7}{11}',d:['\\dfrac{63}{100}','\\dfrac{63}{99}','\\dfrac{2}{3}']},
2b. GCSE item 35 (:182) repeats item 34's stem (8/\sqrt{32}) with different wording. Jon, 19 Nov 2026: replace it. Replace
  {q:'\\dfrac{8}{\\sqrt{32}}',ask:'Simplify fully',correct:'\\sqrt{2}',d:['2','2\\sqrt{2}','4']},
with
  {q:'\\dfrac{12}{\\sqrt{6}}',ask:'Rationalise and simplify',correct:'2\\sqrt{6}',d:['12\\sqrt{6}','\\sqrt{2}','2']},
   (Distractors: top multiplied only; \sqrt{12/6}; \sqrt{6} "cancelled" to leave 12/6.) Project Claude ran the verifier against a copy with items 2 and 2b: PASS (100 items).
3. Working, built two ways. Each line is a KaTeX string.
 (a) TEMPLATES, computed in the page, for:
   - "Simplify" items whose stem is \sqrt{n} or k\sqrt{n} (GCSE items 1-16, A-Level 1-3). With a^2 the biggest square factor of n and b = n/a^2:
     '\text{Biggest square factor of } n \text{ is } a^2' (the number, e.g. 36)
     '[k]\sqrt{n} = [k]\sqrt{a^2}\times\sqrt{b}'
     then '= a\sqrt{b}' when there is no k, or '= k\times a\sqrt{b} = (ka)\sqrt{b}' when there is (e.g. 2\sqrt{8}: '= 2\times 2\sqrt{2} = 4\sqrt{2}').
   - Recurring decimals (GCSE 36-48 and 50, A-Level 31-38 and 40). p = digits before the recurring part, r = the period's length, N/D the unsimplified fraction:
     'x = 0.dddddd\ldots' (the value to 6 decimal places, truncated)
     '(10^{p+r} as a whole number)x = (that multiple to 6 d.p.)\ldots', then, when p > 0, '(10^p)x = (to 6 d.p.)\ldots'
     '\text{Subtract: } Dx = N'
     'x = \dfrac{N}{D}', followed by ' = \dfrac{n}{d}' when it cancels.
     Example 0.08\dot{3}: x = 0.083333\ldots | 1000x = 83.333333\ldots | 100x = 8.333333\ldots | \text{Subtract: } 900x = 75 | x = \dfrac{75}{900} = \dfrac{1}{12}
   - 0.\dot{9} (GCSE 49, A-Level 37): x = 0.999999\ldots | 10x = 9.999999\ldots | \text{Subtract: } 9x = 9 | x = 1
 (b) DATA, a WORKING object keyed 'level-itemNumber' (1-based, as listed), verbatim from parts 2 and 3, for every other item. A data entry overrides a template (A-Level 39, 1/7, has one).
4. On a wrong answer, before MaffsNext.wrong, show the item's working in a box under the options (one line each, KaTeX, \text rendered as words), titled "How to get there". A right answer advances as now. The box clears with the next question. It must fit the phone sizes the game fits now.
5. Project Claude checked every line of all 100 workings in SymPy: in each line, every "="-separated part is equal (decimals within the 6th place; in recurring items x is the key), and the last part of the last line is the key. 0 failures.

SURD-WORKING, part 2 of 4. The WORKING data, first half (paste inside one object with part 3):
'gcse-17':['\\sqrt{27} = 3\\sqrt{3}','\\text{so }\\sqrt{27} + \\sqrt{3} = 3\\sqrt{3} + \\sqrt{3} = 4\\sqrt{3}'],
'gcse-18':['\\sqrt{50} = 5\\sqrt{2}\\text{ and }\\sqrt{8} = 2\\sqrt{2}','\\sqrt{50} - \\sqrt{8} = 5\\sqrt{2} - 2\\sqrt{2} = 3\\sqrt{2}'],
'gcse-19':['\\sqrt{20} = 2\\sqrt{5}\\text{ and }\\sqrt{45} = 3\\sqrt{5}','\\sqrt{20} + \\sqrt{45} = 2\\sqrt{5} + 3\\sqrt{5} = 5\\sqrt{5}'],
'gcse-20':['\\text{Multiply the numbers, then the surds}','2\\sqrt{3} \\times 3\\sqrt{3} = 6 \\times \\sqrt{3}\\times\\sqrt{3} = 6 \\times 3 = 18'],
'gcse-21':['\\text{Multiply top and bottom by }\\sqrt{2}','\\dfrac{1}{\\sqrt{2}} = \\dfrac{1\\times\\sqrt{2}}{\\sqrt{2}\\times\\sqrt{2}} = \\dfrac{\\sqrt{2}}{2}'],
'gcse-22':['\\text{Multiply top and bottom by }\\sqrt{3}','\\dfrac{1}{\\sqrt{3}} = \\dfrac{\\sqrt{3}}{\\sqrt{3}\\times\\sqrt{3}} = \\dfrac{\\sqrt{3}}{3}'],
'gcse-23':['\\text{Multiply top and bottom by }\\sqrt{5}','\\dfrac{1}{\\sqrt{5}} = \\dfrac{\\sqrt{5}}{\\sqrt{5}\\times\\sqrt{5}} = \\dfrac{\\sqrt{5}}{5}'],
'gcse-24':['\\text{Multiply top and bottom by }\\sqrt{3}','\\dfrac{2}{\\sqrt{3}} = \\dfrac{2\\sqrt{3}}{\\sqrt{3}\\times\\sqrt{3}} = \\dfrac{2\\sqrt{3}}{3}'],
'gcse-25':['\\text{Multiply top and bottom by }\\sqrt{2}','\\dfrac{3}{\\sqrt{2}} = \\dfrac{3\\sqrt{2}}{\\sqrt{2}\\times\\sqrt{2}} = \\dfrac{3\\sqrt{2}}{2}'],
'gcse-26':['\\text{Multiply top and bottom by }\\sqrt{8}','\\dfrac{4}{\\sqrt{8}} = \\dfrac{4\\sqrt{8}}{8} = \\dfrac{\\sqrt{8}}{2} = \\dfrac{2\\sqrt{2}}{2} = \\sqrt{2}'],
'gcse-27':['\\text{Multiply top and bottom by }\\sqrt{12}','\\dfrac{6}{\\sqrt{12}} = \\dfrac{6\\sqrt{12}}{12} = \\dfrac{\\sqrt{12}}{2} = \\dfrac{2\\sqrt{3}}{2} = \\sqrt{3}'],
'gcse-28':['\\text{Multiply top and bottom by }\\sqrt{50}','\\dfrac{10}{\\sqrt{50}} = \\dfrac{10\\sqrt{50}}{50} = \\dfrac{\\sqrt{50}}{5} = \\dfrac{5\\sqrt{2}}{5} = \\sqrt{2}'],
'gcse-29':['\\text{Multiply top and bottom by }\\sqrt{5}','\\dfrac{5}{\\sqrt{5}} = \\dfrac{5\\sqrt{5}}{5} = \\sqrt{5}'],
'gcse-30':['\\text{Multiply top and bottom by }\\sqrt{3}','\\dfrac{1}{2\\sqrt{3}} = \\dfrac{\\sqrt{3}}{2\\sqrt{3}\\times\\sqrt{3}} = \\dfrac{\\sqrt{3}}{2\\times 3} = \\dfrac{\\sqrt{3}}{6}'],
'gcse-31':['\\text{Multiply top and bottom by }\\sqrt{7}','\\dfrac{3}{\\sqrt{7}} = \\dfrac{3\\sqrt{7}}{\\sqrt{7}\\times\\sqrt{7}} = \\dfrac{3\\sqrt{7}}{7}'],
'gcse-32':['\\dfrac{\\sqrt{2}}{\\sqrt{6}} = \\sqrt{\\dfrac{2}{6}} = \\sqrt{\\dfrac{1}{3}} = \\dfrac{1}{\\sqrt{3}}','\\text{Multiply top and bottom by }\\sqrt{3}\\text{: }\\dfrac{1}{\\sqrt{3}} = \\dfrac{\\sqrt{3}}{3}'],
'gcse-33':['\\dfrac{\\sqrt{3}}{\\sqrt{12}} = \\sqrt{\\dfrac{3}{12}} = \\sqrt{\\dfrac{1}{4}} = \\dfrac{1}{2}'],
'gcse-34':['\\sqrt{32} = 4\\sqrt{2}\\text{, so }\\dfrac{8}{\\sqrt{32}} = \\dfrac{8}{4\\sqrt{2}} = \\dfrac{2}{\\sqrt{2}}','\\text{Multiply top and bottom by }\\sqrt{2}\\text{: }\\dfrac{2}{\\sqrt{2}} = \\dfrac{2\\sqrt{2}}{2} = \\sqrt{2}'],
'gcse-35':['\\text{Multiply top and bottom by }\\sqrt{6}','\\dfrac{12}{\\sqrt{6}} = \\dfrac{12\\sqrt{6}}{\\sqrt{6}\\times\\sqrt{6}} = \\dfrac{12\\sqrt{6}}{6} = 2\\sqrt{6}'],
'alevel-4':['3\\sqrt{50} = 3\\times 5\\sqrt{2} = 15\\sqrt{2}','2\\sqrt{18} = 2\\times 3\\sqrt{2} = 6\\sqrt{2}','3\\sqrt{50} - 2\\sqrt{18} = 15\\sqrt{2} - 6\\sqrt{2} = 9\\sqrt{2}'],
'alevel-5':['\\sqrt{75} = 5\\sqrt{3}','2\\sqrt{27} = 2\\times 3\\sqrt{3} = 6\\sqrt{3}','\\sqrt{75} + 2\\sqrt{27} = 5\\sqrt{3} + 6\\sqrt{3} = 11\\sqrt{3}'],
'alevel-6':['(2\\sqrt{3})^2 = 2^2 \\times (\\sqrt{3})^2 = 4 \\times 3 = 12'],
'alevel-7':['\\sqrt{2} \\times \\sqrt{8} = \\sqrt{16} = 4'],
'alevel-8':['\\sqrt{6} \\times \\sqrt{24} = \\sqrt{144} = 12'],
'alevel-9':['\\dfrac{\\sqrt{48}}{\\sqrt{3}} = \\sqrt{\\dfrac{48}{3}} = \\sqrt{16} = 4'],
'alevel-10':['\\sqrt{5}(\\sqrt{5}+\\sqrt{20}) = \\sqrt{5}\\times\\sqrt{5} + \\sqrt{5}\\times\\sqrt{20} = 5 + \\sqrt{100} = 5 + 10 = 15'],
'alevel-11':['\\text{Multiply top and bottom by the conjugate }\\sqrt{3}+1','\\dfrac{1}{\\sqrt{3}-1} = \\dfrac{\\sqrt{3}+1}{(\\sqrt{3}-1)(\\sqrt{3}+1)} = \\dfrac{\\sqrt{3}+1}{3-1} = \\dfrac{\\sqrt{3}+1}{2}'],
'alevel-12':['\\text{Multiply top and bottom by the conjugate }\\sqrt{5}-2','\\dfrac{1}{\\sqrt{5}+2} = \\dfrac{\\sqrt{5}-2}{(\\sqrt{5}+2)(\\sqrt{5}-2)} = \\dfrac{\\sqrt{5}-2}{5-4} = \\sqrt{5}-2'],
'alevel-13':['\\text{Multiply top and bottom by the conjugate }\\sqrt{2}-1','\\dfrac{1}{\\sqrt{2}+1} = \\dfrac{\\sqrt{2}-1}{(\\sqrt{2}+1)(\\sqrt{2}-1)} = \\dfrac{\\sqrt{2}-1}{2-1} = \\sqrt{2}-1'],

SURD-WORKING, part 3 of 4. The WORKING data, second half:
'alevel-14':['\\text{Multiply top and bottom by the conjugate }\\sqrt{7}+2','\\dfrac{1}{\\sqrt{7}-2} = \\dfrac{\\sqrt{7}+2}{(\\sqrt{7}-2)(\\sqrt{7}+2)} = \\dfrac{\\sqrt{7}+2}{7-4} = \\dfrac{\\sqrt{7}+2}{3}'],
'alevel-15':['\\text{Multiply top and bottom by the conjugate }\\sqrt{3}-1','\\dfrac{2}{\\sqrt{3}+1} = \\dfrac{2(\\sqrt{3}-1)}{(\\sqrt{3}+1)(\\sqrt{3}-1)} = \\dfrac{2(\\sqrt{3}-1)}{3-1} = \\sqrt{3}-1'],
'alevel-16':['\\text{Multiply top and bottom by the conjugate }\\sqrt{5}+1','\\dfrac{3}{\\sqrt{5}-1} = \\dfrac{3(\\sqrt{5}+1)}{(\\sqrt{5}-1)(\\sqrt{5}+1)} = \\dfrac{3(\\sqrt{5}+1)}{5-1} = \\dfrac{3(\\sqrt{5}+1)}{4}'],
'alevel-17':['\\text{Multiply top and bottom by the conjugate }2-\\sqrt{3}','\\dfrac{4}{2+\\sqrt{3}} = \\dfrac{4(2-\\sqrt{3})}{(2+\\sqrt{3})(2-\\sqrt{3})} = \\dfrac{4(2-\\sqrt{3})}{4-3} = 8-4\\sqrt{3}'],
'alevel-18':['\\text{Multiply top and bottom by the conjugate }\\sqrt{2}+1','\\dfrac{\\sqrt{2}}{\\sqrt{2}-1} = \\dfrac{\\sqrt{2}(\\sqrt{2}+1)}{(\\sqrt{2}-1)(\\sqrt{2}+1)} = \\dfrac{2+\\sqrt{2}}{2-1} = 2+\\sqrt{2}'],
'alevel-19':['\\text{Multiply top and bottom by the conjugate }\\sqrt{6}-1','\\dfrac{5}{\\sqrt{6}+1} = \\dfrac{5(\\sqrt{6}-1)}{(\\sqrt{6}+1)(\\sqrt{6}-1)} = \\dfrac{5(\\sqrt{6}-1)}{6-1} = \\sqrt{6}-1'],
'alevel-20':['\\text{Multiply top and bottom by the conjugate }2\\sqrt{3}-3','\\dfrac{1}{2\\sqrt{3}+3} = \\dfrac{2\\sqrt{3}-3}{(2\\sqrt{3}+3)(2\\sqrt{3}-3)} = \\dfrac{2\\sqrt{3}-3}{12-9} = \\dfrac{2\\sqrt{3}-3}{3}'],
'alevel-21':['\\text{Difference of two squares}\\;(a+b)(a-b) = a^2 - b^2','(\\sqrt{3}+1)(\\sqrt{3}-1) = 3 - 1 = 2'],
'alevel-22':['\\text{Difference of two squares}\\;(a+b)(a-b) = a^2 - b^2','(\\sqrt{5}+2)(\\sqrt{5}-2) = 5 - 4 = 1'],
'alevel-23':['\\text{Difference of two squares}\\;(a+b)(a-b) = a^2 - b^2','(\\sqrt{7}+3)(\\sqrt{7}-3) = 7 - 9 = -2'],
'alevel-24':['(2+\\sqrt{3})^2 = (2+\\sqrt{3})(2+\\sqrt{3})','= 4 + 2\\sqrt{3} + 2\\sqrt{3} + 3 = 7+4\\sqrt{3}'],
'alevel-25':['(3-\\sqrt{2})^2 = (3-\\sqrt{2})(3-\\sqrt{2})','= 9 - 3\\sqrt{2} - 3\\sqrt{2} + 2 = 11-6\\sqrt{2}'],
'alevel-26':['(1+\\sqrt{5})(2+\\sqrt{5}) = 2 + \\sqrt{5} + 2\\sqrt{5} + 5 = 7+3\\sqrt{5}'],
'alevel-27':['\\text{Difference of two squares}\\;(a+b)(a-b) = a^2 - b^2','(\\sqrt{2}+\\sqrt{3})(\\sqrt{2}-\\sqrt{3}) = 2 - 3 = -1'],
'alevel-28':['(\\sqrt{6}+1)^2 = (\\sqrt{6}+1)(\\sqrt{6}+1)','= 6 + \\sqrt{6} + \\sqrt{6} + 1 = 7+2\\sqrt{6}'],
'alevel-29':['(2\\sqrt{3}+1)(\\sqrt{3}-2) = 2\\sqrt{3}\\times\\sqrt{3} - 4\\sqrt{3} + \\sqrt{3} - 2','= 6 - 3\\sqrt{3} - 2 = 4-3\\sqrt{3}'],
'alevel-30':['(\\sqrt{5}+\\sqrt{2})^2 = 5 + \\sqrt{10} + \\sqrt{10} + 2 = 7+2\\sqrt{10}'],
'alevel-41':['\\text{Multiply top and bottom by }\\sqrt{3}+1','\\dfrac{\\sqrt{3}+1}{\\sqrt{3}-1} = \\dfrac{(\\sqrt{3}+1)^2}{(\\sqrt{3}-1)(\\sqrt{3}+1)} = \\dfrac{4+2\\sqrt{3}}{2} = 2+\\sqrt{3}'],
'alevel-42':['\\text{Multiply top and bottom by }\\sqrt{5}+\\sqrt{2}','\\dfrac{\\sqrt{5}+\\sqrt{2}}{\\sqrt{5}-\\sqrt{2}} = \\dfrac{(\\sqrt{5}+\\sqrt{2})^2}{(\\sqrt{5}-\\sqrt{2})(\\sqrt{5}+\\sqrt{2})} = \\dfrac{7+2\\sqrt{10}}{5-2} = \\dfrac{7+2\\sqrt{10}}{3}'],
'alevel-43':['\\text{Multiply top and bottom by }\\sqrt{3}-\\sqrt{2}','\\dfrac{1}{\\sqrt{2}+\\sqrt{3}} = \\dfrac{\\sqrt{3}-\\sqrt{2}}{(\\sqrt{3}+\\sqrt{2})(\\sqrt{3}-\\sqrt{2})} = \\dfrac{\\sqrt{3}-\\sqrt{2}}{3-2} = \\sqrt{3}-\\sqrt{2}'],
'alevel-44':['\\dfrac{6}{\\sqrt{3}} = \\dfrac{6\\sqrt{3}}{3} = 2\\sqrt{3}\\text{ and }\\sqrt{27} = 3\\sqrt{3}','\\dfrac{6}{\\sqrt{3}}+\\sqrt{27} = 2\\sqrt{3} + 3\\sqrt{3} = 5\\sqrt{3}'],
'alevel-45':['\\sqrt{50} = 5\\sqrt{2}\\text{ and }\\sqrt{8} = 2\\sqrt{2}','\\dfrac{\\sqrt{50}+\\sqrt{8}}{\\sqrt{2}} = \\dfrac{5\\sqrt{2}+2\\sqrt{2}}{\\sqrt{2}} = \\dfrac{7\\sqrt{2}}{\\sqrt{2}} = 7'],
'alevel-46':['\\text{Difference of two squares}\\;(a+b)(a-b) = a^2 - b^2','(3+\\sqrt{5})(3-\\sqrt{5}) = 9 - 5 = 4'],
'alevel-47':['\\sqrt{8} = 2\\sqrt{2}\\text{, so }\\sqrt{2}(3\\sqrt{2}-\\sqrt{8}) = \\sqrt{2}(3\\sqrt{2}-2\\sqrt{2}) = \\sqrt{2}\\times\\sqrt{2} = 2'],
'alevel-48':['\\text{Squaring undoes the square root: }(\\sqrt{a})^2 = a'],
'alevel-49':['x^4 = (x^2)^2\\text{, so }\\sqrt{x^4} = x^2'],
'alevel-50':['\\dfrac{8}{\\sqrt{2}} \\times \\dfrac{1}{\\sqrt{2}} = \\dfrac{8}{\\sqrt{2}\\times\\sqrt{2}} = \\dfrac{8}{2} = 4'],
'alevel-39':['x = 0.142857\\ldots','1000000x = 142857.142857\\ldots','\\text{Subtract: } 999999x = 142857','999999 = 7 \\times 142857','x = \\dfrac{142857}{999999} = \\dfrac{1}{7}'],

SURD-WORKING, part 4 of 4 (parts 1-3 came first).

EXACT CHANGE (continued):
6. scripts/verify-surd-simplifier.py: add the check Project Claude ran (item 5) for every item at both levels, reading the working the page builds (templates and data alike); and in Chromium, a wrong answer shows that item's lines in the box before Next. Plants that must FAIL: one line made false (\sqrt{4}\times\sqrt{3} written as \sqrt{4}\times\sqrt{5} in GCSE item 1); a template whose biggest square factor is wrong; the box not shown on a wrong answer. Every existing check passes.
7. Report only: games whose wrong-answer pause shows no working or reason (canon 7.6), in the PR body and cloud.md.
7b. docs/todo.md §4: add one row, EXTRACT-BANKS-MISREAD: scripts/extract-banks.py counts a level's fixed list for a generated level (factor-race KS3 and fraction-equivalence KS3/GCSE were reported as 20) and missed negative-number-line's Place It list (45 items, reported 30); data/check-ledger.json B4 entries built on those counts are not real. Found 19 Nov 2026 (bank audit; FACTOR-RACE-Y6-40). Owner: home lane. todo.md must not grow by more than this row.
8. One /updates/ line: "Surd Simplifier: get one wrong and it now shows you how to get there, step by step." cloud.md entry.
9. PR, Gate and phone-fit-full green, then merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600; report its last line. No draft PR.

DO NOT TOUCH: every item's stem, options and key (except :196 and :182); :243; marking and scoring; schools/assets/; canon; docs/handover/home.md; any other game.

SUCCESS CONDITION: :196 and :182 replaced, :243 unchanged; every item at both levels has working (template or data) that passes item 5's check; the box shows on a wrong answer; plants fail; phone fit no worse; FACTOR-RACE-Y6-40 closed out; merged by merge-pr.py with a GREEN last line; cloud.md records it all.

STOP IF: :196 or :182 doesn't match the quoted text; any working line fails item 5's check (report it; don't edit it); the box can't fit a phone size the game fits now (report sizes); merge-pr.py can't reach GitHub; anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies (report under "Decided for you").
END OF CONTRACT
