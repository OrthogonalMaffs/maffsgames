ESTIMATION-FOUNDATION (Project Claude, Sat 28 Nov 2026 09:20; checked against main 9072d16)
RECOMMENDED: Claude Code, Sonnet 5.5, effort medium. Exact bank lines and wording are given.
LANE: cloud. SEND: now. First commit carries 3-GON-LINE-UP-BUILD's close-out (AGENTS.md): #943 squash-merged as c5d9d70 by merge-pr.py, its last line "main c5d9d70 run 46125518930: GREEN"; main's runs on c5d9d70: check-site 46125518930, phone-fit-full 46125518849, pages 46125518642, each success, first attempt; end-task.py refused (branch checked out in the primary checkout, the known cloud case; nothing deleted). Move docs/handover/contracts/2026-11-28-3-gon-line-up-build.md, -amendment-1.md and -amendment-2.md to docs/history/contracts/. Save this contract verbatim as docs/handover/contracts/2026-11-28-estimation-foundation.md in the same commit.
TIER: Small (one game and its own verifier): merges on green.

TASK: Make Estimation Engine's estimates that divide by a decimal Foundation-paper standard: replace the two items whose divisors are not, show the method whenever a student divides by a decimal, and make the verifier enforce the standard.

ROOT CAUSE: Jon, playing the live site on 28 Nov 2026, met D09, "(197 × 0.62) ÷ 0.31", in this Essentials game (N14.1, CORE in the grade 1-3 banding): "likely non calc. and estimation on the essentials strand, and this comes up?" Ruling (Jon, 28 Nov 2026, 08:13): "leave the type but make it proper foundation paper fodder". Shown, games/estimation-engine/index.html on 9072d16:
- 7 of 45 items divide by a number under 1. Five round it to 0.5 or 0.2, the Foundation staples (B06 ÷0.5, B07 ÷0.2, D01 ÷0.5, D03 ÷0.2, D05 ÷0.5). Two do not: C07 (line 249, 0.392 ÷ 0.0021, rounded 0.4 ÷ 0.002) and D09 (line 259, rounded (200 × 0.6) ÷ 0.3).
- EE.deal (line 333) serves one item from each group A-F in order, so every run reaches a C and a D item by about question 5.
- The feedback (line 475) shows the rounded calculation and its result, but nowhere shows how to divide by a decimal.

CLASS CHECK: The two items are content, so they are fixed in the bank. The missing guard is the class: nothing stops a future item from using a divisor no Foundation paper would, so the rule goes in scripts/verify-estimation-engine.py's check_bank, with a self-test plant. The method line is computed from the item's own rounded divisor, so it applies to every item that needs it, present and future. Report only (no change) for any other game: if games/estimation-golf/index.html has items dividing by a number under 1, list them in the PR body.

EXACT CHANGE:
1. First commit: the close-out and contract save in the LANE line above.

2. The bank, games/estimation-engine/index.html between BANK-START and BANK-END. Replace line 249 (C07) and line 259 (D09) with exactly these lines:
  {"id": "C07", "group": "C", "nums": ["0.83", "0.21"], "shape": "a/b", "rounded": ["0.8", "0.2"], "estimate": "4", "exact": "3.952", "show": "0.83 ÷ 0.21", "tex": "0.83 \\div 0.21", "approx": true},
  {"id": "D09", "group": "D", "nums": ["197", "0.62", "0.52"], "shape": "(a*b)/c", "rounded": ["200", "0.6", "0.5"], "estimate": "240", "exact": "234.9", "show": "(197 × 0.62) ÷ 0.52", "tex": "(197 \\times 0.62) \\div 0.52", "approx": true},
   (Checked by Project Claude: 0.83 and 0.21 are 0.8 and 0.2 at 1 s.f.; 0.8 ÷ 0.2 = 4; 0.83 ÷ 0.21 = 3.95238…, 3.952 to 4 s.f. 197, 0.62 and 0.52 are 200, 0.6 and 0.5; 120 ÷ 0.5 = 240; 197 × 0.62 ÷ 0.52 = 234.884…, 234.9 to 4 s.f. No exact halves.) Match the neighbouring lines' indentation and escaping exactly. No other item changes.

3. The method line. In the step-2 feedback (line 475), directly after the fb-work line, add one line whenever the item's rounded divisor is a number under 1, for every shape with a divisor:
   - divisor 0.5: "Dividing by 0.5 is the same as multiplying by 2."
   - divisor 0.2: "Dividing by 0.2 is the same as multiplying by 5."
   The divisor is the rounded value of the shape's denominator (b in a/b, c in (a*b)/c, (a+b)/c and (a-b)/c, the product c*d in (a*b)/(c*d), b in a**2/b, a in b/a). Use the existing fb-line class. It shows on right and wrong answers alike, before Next.

4. The verifier, scripts/verify-estimation-engine.py:
   a. check_bank (line 133): for every item, compute the rounded denominator from its shape; if it is under 1, it must be 0.5 or 0.2, else fail with "<id>: divides by <d>; a Foundation estimate divides by 0.5 or 0.2". Update the docstring's list of checks.
   b. A new self-test plant: D01's rounded divisor set to "0.3" (and its estimate recomputed to match, so only the new rule can catch it); it must fail.
   c. In the Chromium pass, D01's feedback shows the 0.5 method line, and A01's shows none.
   d. Update the ci-line comment (line 2) if it lists the checks.

5. Phone fit: checked by the PR's own phone-fit run for estimation-engine (AGENTS.md: never measure locally in its place). The new line must not push Next below the fixed footer (canon §7.6.1, the game's own nextInView at line 484).

6. /updates/: one line: "Estimation Engine: every estimate that divides by a decimal is now Foundation-paper standard (÷ 0.5 or ÷ 0.2), with the method shown."

7. Merge on green: python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600, run from main's checkout (merge main in and re-run the Gate if main moves first). Record its last line and main's run IDs in docs/handover/cloud.md.

DO NOT TOUCH: any other bank item; EE.deal and the run order; the marking (MaffsAnswer, exact match); any other game, including estimation-golf (report only); schools/assets/; every checker except verify-estimation-engine.py; canon; docs/todo.md; the roster. No force-push.

SUCCESS CONDITION: C07 and D09 are exactly the lines above; no item divides by a number under 1 other than 0.5 or 0.2; the method line shows for every such item and for no other; verify-estimation-engine.py passes with the new rule and its new plant caught, and the old plants still caught; the PR's phone-fit run is green; the /updates/ line is in; merged with merge-pr.py, main green.

STOP IF: (1) Your independent recomputation (the verifier's own) disagrees with either new line. (2) The method line cannot fit above the footer at any phone-fit size without smaller text or removed content: report the figures. (3) A shared check needs an exemption. (4) A check still fails after your second fix (standing rule). (5) merge-pr.py can't reach GitHub, or a push is refused (never force). (6) main is red when you come to merge: report it; do not use --override. (7) Anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies: report it under "Decided for you", and never use it to override a STOP IF.
