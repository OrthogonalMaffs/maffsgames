CALC-IMPLIED-MULT, one part.
LANE: home. TOP PRIORITY (Jon, 20 Nov 2026): send before any other home task not yet started. TIER: Small. MODEL: Claude Code, Opus 5.5, high effort (shared calculator, 22 games).

TASK: The shared calculator gives implied multiplication priority over × and ÷, as a current Casio does, so 267÷2π = 42.49..., not 419.40...

ROOT CAUSE: Checked on main 527f8b8. schools/assets/calculator.js:172-180 term() treats implied multiplication (startsValue after a value) at the same level as × and ÷, left to right, so 267÷2π = (267÷2)×π. Jon found it in I Dropped My Ice Cream (radius from a circumference). Current Casio exam models (fx-83GT CW, fx-83GT X, fx-991CW UK) rank "multiplication where the multiplication sign is omitted" at priority 7, above × and ÷ at 9 (Casio's own example: 6 ÷ 2(1 + 2) = 6 ÷ (2(1 + 2)) = 1). The file's header (:26-28) claims Casio conventions, and canon §0.3 SR-28 already rules "implied multiplication binds tighter than ÷". A student who types what they would type in the exam gets a wrong value, then is marked wrong.

CLASS CHECK: Shared infrastructure: one parser used by 22 games. Fix it once in calculator.js's grammar; no game changes.

EXACT CHANGE:
1. First commit: if docs/handover/home.md shows a merged home contract whose close-out is still owed, do it (main's runs from the API; contract to docs/history/contracts/). Save this contract verbatim as docs/handover/contracts/2026-11-20-calc-implied-mult.md.
2. calculator.js: a new grammar level between term and unary, e.g.
     term    := implied (('×' | '÷') implied)*
     implied := unary (<implicit ×> power)*
   An implied factor never takes a leading sign (2-3 stays a subtraction). Update the header's grammar block and its prose: "a number, bracket, constant, function or √ straight after a value multiplies, and binds tighter than × and ÷, as on a current Casio: 6÷2(1+2) = 1, 267÷2π = 42.49...". Errors (÷0 and the rest) unchanged.
3. scripts/test-calculator-js.py: new cases, each exact to the display's precision: 267÷2π = 42.4943698...; 6÷2(1+2) = 1; 1÷2√(4) = 0.25; 10÷2π² = 0.5066059...; 2π÷4 = π/2; 8÷2(2) = 2; 6÷2×3 = 9 (explicit × stays left to right); 2-3 = -1; -2(3) = -6; 2(3)² = 18; 1÷0π is an error. Plants that must FAIL: the old flat term(); implied factor allowed a leading minus. Every existing case still passes; any existing case that asserted the old order is listed in the PR and changed to the new rule.
4. scripts/check-calculator.py and any game verifier that drives the calculator: run them; all pass.
5. One /updates/ line: "The calculator now reads 267÷2π as 267÷(2π), the same as your Casio." A short note in canon §4.4 (the calculator) pointing at SR-28. home.md entry.
6. PR, Gate and phone-fit-full green, merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600; report its last line. If main is red only on the Core papers' phone-fit (the cloud lane's #843), let merge-pr.py wait for it; fix nothing there.

DO NOT TOUCH: the calculator's keys, layout, CSS, modes (DEG/RAD) and its other rules (-3² = -9, ^ right-associative, √ opens a bracket, auto-closing brackets); any game file; docs/handover/cloud.md; the cloud lane's open PR and its files.

SUCCESS CONDITION: 267÷2π = 42.49... on every game's calculator; the new cases pass and both plants fail; all existing calculator tests and calculator-driving verifiers pass; header, canon note and /updates/ line in; merged GREEN; home.md records it all.

STOP IF: any game's answer key or marking depends on the old order (report the game and item; change nothing); a case in step 3 can't be met without changing another stated rule; merge-pr.py can't reach GitHub; anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies (report under "Decided for you").
END OF CONTRACT

Amendment 1 to CALC-IMPLIED-MULT (Jon, 20 Nov 2026): Enter is always equals.
ROOT CAUSE: calculator.js:440-444: Enter on a focused key presses that key, and a mouse click leaves focus on the key it clicked, so Enter repeats the last key clicked instead of =. PC calculators treat Enter as =.
CHANGE: in the panel's keydown handler, Enter (and =) always press = wherever focus is inside the panel; Space on a focused key still presses that key (keyboard-only users keep it). Update the comment at :440.
TESTS: in Chromium: click 7, then press Enter: the result is evaluated, 7 is not typed again; Tab to a key, Space presses it; Enter with focus on the panel itself is =. Plant that must FAIL: the old "Enter presses the focused key" branch restored.
/updates/: one line for both fixes: "The calculator now reads 267÷2π as 267÷(2π), the same as your Casio, and Enter always means equals."
Everything else in the contract stands.

Amendment 2 to CALC-IMPLIED-MULT (Jon, 20 Nov 2026): a correct answer clears the calculator.
RULING: only a correct answer auto-clears the calculator. A wrong answer never clears it (not on a retry, not on moving on); the student clears it with C.
ROOT CAUSE: calc.clear() exists (calculator.js, "A new question: the calculator display clears"), but 14 of the 22 calculator games never call it and most others only at game start (e.g. i-dropped-my-ice-cream:585), so a student starts the next question with the last one's sum on screen.
CLASS CHECK: one missing step in 22 games; fix it once in shared code, no game edits. Every game reports each answer through mfg('question_answered', {correct}) (schools/assets/analytics.js:84).
CHANGE:
1. analytics.js, mfg(): for question_answered, dispatch window CustomEvent 'maffs:answered' with detail {correct: !!params.correct} BEFORE the production-host gate, so it fires locally and in tests. Nothing else in mfg changes; no new data is sent anywhere.
2. calculator.js: every mounted calculator listens for 'maffs:answered'; on correct === true it does what clear() does now (display cleared, the calculator display selected). On false it does nothing.
TESTS: in Chromium: type 2+3= on a mounted calculator, fire mfg('question_answered',{correct:true}): display reads 0; repeat with correct:false: the sum stays. Two calculators on one page both clear. Plants that must FAIL: the dispatch moved after the production gate; the listener clearing on false.
Also run check-question-id and check-answer-lock in-play: unchanged.
/updates/: add to the same line: "...and Enter always means equals; a right answer clears the calculator for the next question."
STOP IF: any calculator game sends question_answered with correct:true before the student has finished the question (a part-marked step), so the clear would wipe working still needed: list them, change nothing.
Everything else in the contract stands.
