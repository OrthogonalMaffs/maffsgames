LANE: cloud (Claude Code on the web). SEND: now (#813 merged as 9bf8c65; main green). Two PRs in this one session, in order, each merged before the next is branched. Re-checked against main ea7bcaa, 17 Nov 14:15: every count, path and line number below still holds.
RECOMMENDED: Opus 5.5, high effort. A site rule held by a new check, applied in 12 games, with care for negative answers on phones.

TASK: ANSWER-BOX-TEXT. Make every typed answer box a text box (type="text"), never type="number", in every game, and add a check that fails any type="number" answer box.

ROOT CAUSE: A type="number" box does two things wrong.
(1) It changes its value when its arrows are clicked or the mouse wheel turns over it. In Graph Sketcher that submits and wipes the answer: games/graph-sketcher/index.html:701 builds each table cell as <input type="number" step="any" ... onchange="checkCell(this)">. Jon, 15 Nov 2026: "click up or down and it auto deletes it. this is properly broken".
(2) It silently empties on any string it cannot parse, such as a typed £ or "1,000". MaffsAnswer then receives "" and can never give its 'format' message, against the canon rule that MaffsAnswer reads the raw typed string (schools/assets/answer.js:3).
On main ea7bcaa, 12 games still use type="number" answer boxes:
- 52dle (1), chart-interrogator (2), component-crusher (6), estimation-golf (1), glorious-gantt (4), graph-sketcher (5);
- growth-and-decay (2), like-terms-collector (1, built in script at :408, inp.type='number');
- split-it (13), stat-attack (7), tax-theft (1), test-the-claim (8).
Ten of them mark through MaffsAnswer. estimation-golf and glorious-gantt mark with their own code.
(percentage-flip is no longer one: #793 gave it a text box.)

CLASS CHECK: A class. The same input type is in 12 games, and the fault is in what a type="number" box does, not in any one game. So the fix is:
- a site rule (every typed numeric answer box is type="text", never type="number");
- held by a check that fails any type="number" input in a game page or a shared game script;
- applied in all 12 games.
Two things are not in scope:
- escape-rooms/assets/engine.js, the slider's typed fallback ("Or type the setting"). It sets an instrument and is not marked on change; it stays as it is, and the check's scope (games/ and schools/assets/) leaves it out. Say so in the docstring.
- schools/assets/answer.js:87 has the words type="number" in a COMMENT. The check must match real inputs (markup, and script that sets an input's type), not prose. If it cannot tell them apart, STOP and report; do not edit answer.js.

JON'S RULINGS (verbatim in each PR body):
- 15 Nov 10:25: "click up or down and it auto deletes it. this is properly broken," (Graph Sketcher's table).
- 15 Nov 10:29: "yes" (to: fix it as a site rule across every game with a type="number" answer box, with a check so it cannot come back).
- 17 Nov 11:51: "fix the live bug first" (ahead of the When will I use this? build).
- 17 Nov 12:00: the canon sentence waits for the home lane's next docs PR. This lane does NOT edit docs/canon.md.

EXACT CHANGE:
0. First commit of PR 1: the close-out of #813 (ITS-A-SINE example D and the keywords) per AGENTS.md's close-out rule: merged as 9bf8c65 via merge-pr.py, last line "main 9bf8c65 run 44098582649: GREEN"; main on 9bf8c65: check-site 44098582649, phone-fit-full 44098582913, pages build 44098581439, all success. Move its contract to docs/history/contracts/. Also any earlier close-out not already on main.

PR 1: the check and the ten MaffsAnswer games.
1. scripts/check-answer-inputs.py, in CI, wired the way the repo's other site-wide checks are (a ci-line, as scripts/check-start-back-link.py does).
   - It fails any <input type="number"> under games/ and schools/assets/: in markup, in an HTML string a script builds, or set by script (.type = 'number', setAttribute('type', 'number')).
   - Comments and prose are not inputs.
   - It has a named EXEMPT list, with a reason per entry. Its scope is games/ and schools/assets/ only.
   - --selftest plants, each of which must fail:
     - a type="number" box in a game page;
     - one built in a script string;
     - one set by .type = 'number';
     - a stale EXEMPT entry.
   - A control that must pass: a comment containing type="number".
2. The ten MaffsAnswer games: 52dle, chart-interrogator, component-crusher, graph-sketcher, growth-and-decay, like-terms-collector, split-it, stat-attack, tax-theft, test-the-claim.
   - Every answer box becomes type="text".
   - On phones: inputmode="decimal" where the answer can never be negative. Where it can be negative, the shared MaffsKeypad with keys: {minus: true} (schools/assets/keypad.js:15), because the iPhone's decimal keypad has no minus key.
   - Decide each box from the game's own answer pool, and state per box in the PR body: can it be negative, and which you chose.
   - Any onchange/oninput that marks an answer keeps its event but now receives the raw string.
   - Graph Sketcher's table no longer marks on an arrow click, because there are no arrows.
   - Keep every placeholder, id, aria-label and width.
3. Each touched game's verifier gains a test that its answer boxes are type="text" and that a typed £ or comma reaches MaffsAnswer (the 'format' message where it applies).
4. /updates/: one line in the site's plain wording ("Answer boxes no longer change when you scroll or click their arrows").
5. docs/todo.md row ANSWER-BOX-CANON (home lane): add to canon §7.1.3 that every typed numeric answer is type="text", never type="number", with the two reasons above and the phone rule (inputmode="decimal", or MaffsKeypad {minus: true} where the answer can be negative). Dated, Jon 15 Nov 2026.
6. docs/handover/cloud.md entry.
7. Merge with scripts/merge-pr.py when the Gate is green.

PR 2 (branched from main after PR 1 merges): the two games with their own marking.
8. estimation-golf and glorious-gantt get the same input change. Their own marking code stays exactly as it is (moving them to MaffsAnswer is a separate change).
   - Prove by test that each marks every item in its pool exactly as before when the same string is typed.
   - Remove both from the check's EXEMPT list if PR 1 had to list them. PR 1 may exempt them by name, with the reason "PR 2 of ANSWER-BOX-TEXT".
9. Each verifier gains the type="text" test.
10. /updates/ line if the wording differs from PR 1's; otherwise none.
11. docs/todo.md row MAFFSANSWER-OWN-MARKING: estimation-golf and glorious-gantt still mark by their own code (canon §7.1.3 REQUIRED).
12. docs/handover/cloud.md entry.
13. Merge with scripts/merge-pr.py when the Gate is green.

DO NOT TOUCH:
- Any game's questions, keys, tolerances or marking logic.
- MaffsAnswer's behaviour and schools/assets/answer.js.
- MaffsKeypad and calculator.js: use them, do not edit them.
- escape-rooms/: engine.js's fallback stays type="number".
- The money boxes already made by MaffsAnswer.moneyInput().
- docs/canon.md (home lane).
- Gate files beyond wiring the new check as the existing site-wide checks are wired.
- No draft PR.

SUCCESS CONDITION:
- No type="number" answer box in any game: the check passes, and its plants fail.
- On a phone, every box whose answer can be negative can take a minus.
- Every game marks every pool item exactly as before for the same typed string.
- Graph Sketcher's arrows are gone.
- phone-fit, answer-lock and every touched verifier pass without loosening.
- Both PRs merged by merge-pr.py, in order. Each reported with the script's last line, its merge commit, and main's check-site and phone-fit-full run IDs.
- todo and handover committed.

STOP IF:
- A game's marking changes for any typed string that was marked before (report the game, item and string).
- A box needing a minus cannot take MaffsKeypad without breaking phone fit.
- A game reads input.valueAsNumber or relies on min/max/step validation in a way the change would alter.
- The check cannot tell a comment from an input without editing answer.js.
- Wiring the check needs a Gate file changed beyond the existing pattern.
- merge-pr.py refuses for a reason other than a transient 5xx it already retries.

AMENDMENT 1 (Jon, 17 Nov 2026, in session, answering two questions from the implementer):
1. Q: "ANSWER-BOX-TEXT premise gap: 9 answer boxes in 3 games read the typed value with parseFloat, not MaffsAnswer: chart-interrogator's Phase 1 reading (non-money) and Phase 2 count; graph-sketcher's read, extrapolate and turning-point x/y boxes; test-the-claim's scaled λ and the discrete critical-region boxes. [...] How should these boxes read the typed value?"
   A: "Read via MaffsAnswer.parse (Recommended)": swap parseFloat(x) for MaffsAnswer.parse(x) (null → NaN, the existing 'not a number' path) at those reads only; keys and tolerances untouched; proven by test that every string a number box accepts reads the same, and "1,250"/"12abc" are refused, not marked.
   (Correction by the implementer: the question also said a typed Unicode minus "−" would be read. It is not: MaffsAnswer.parse takes the ASCII hyphen only, which is what MaffsKeypad types. One new acceptance: a leading £ or € in these boxes is read, e.g. "£5" as 5.)
2. Q: "Graph Sketcher's table on a phone [...] in keypad mode only (touch screens; never drawn with a mouse), a Check button under the table sends each typed cell that same change event, so checkCell marks it exactly as before. Accept?"
   A: "Yes, Check in keypad mode (Recommended)".
