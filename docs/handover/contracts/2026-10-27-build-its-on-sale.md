TASK: Build It's on Sale!, the percentages-with-money game, on the existing bank (#568), unlisted.
ROOT CAUSE: Percentages with money carry 80 OCR Foundation marks at the grade-4 borderline, and no game covers them. The bank is merged; the game imports its generator (bank-first rule).
CLASS CHECK: Local: a new game. The stage-5 board label is the same shared gap as in Contract 1; ship stage 5 without a leaderboard.
EXACT CHANGE:
1. games/its-on-sale/. Five stages as the bank defines them (percentage of an amount; increase and decrease; percentage change; reverse percentages; interest and depreciation), same pattern as Contract 1 (the pie-chart game: five stages, each its own board/analytics mode, played one at a time: a stepped worked example, then 10 questions easiest first, then "Next: Stage N+1", the Take a Walk pattern): worked example, 10 questions easiest first, "Next: Stage N+1".
2. Mechanic: price tags on a high-street shop's shelf through the year (summer sale, Black Friday, January sales, prices going up), with a bank counter and a car dealer for stage 5. The student types the answer onto the tag: a £ box to 2 d.p., or a box with "%" beside it for percentage change. No multiple choice.
3. Calculator: stages 1-4 calculator-optional, with "Try without a calculator" on items the bank marks as friendly; stage 5 says a calculator is needed. Worked lines from the bank (build-up method for stages 1-4, multiplier for stage 5).
4. Marking by value; the bank's named slips as feedback. No "better deal" stage: Better Value covers that.
5. Theme from the roster levels; phone fit and verifier as in Contract 1 (phone fit with the keypad open at 320x568, 360x640, 375x667, 390x844; verifier through a separate code path, with planted faults).
DO NOT TOUCH: As Contract 1 (the bank's questions and answers; shared files and the lists (games.json, sitemap, homepage, Essentials); any other game).
SUCCESS CONDITION: As Contract 1 (merged once CI is green, unlisted, main green; build.md records the state, a "Decided for you" list, one screenshot per stage at 375x667 in your scratchpad).
STOP IF: As Contract 1 (a bank answer is wrong: leave that question out of the game, report it with the correct answer, carry on, don't edit the bank; the bank lacks items a stage needs: build the stages it supports, 'Coming soon' on the rest, report the gap; a stage can't fit at 320x568: park it on the known-failures list and report).

(Build lane queue, 27 Oct afternoon: "Report at each merge. When the queue is done, say so and stop." Both contracts: new files only, unlisted, roster row Unlisted, same lane rules.)
