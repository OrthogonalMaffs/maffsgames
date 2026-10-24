# Contract FOOTBALL-PITCHES (Jon, 23 Oct 2026), verbatim

Name given by the cloud lane (the contract arrived unnamed). Queued behind the TAKE-A-WALK-LIST checkpoint.

---

MODEL: Opus, medium effort. A new game from a full spec: a fixed landing stage, four generated stages, unit-choice answers and a verifier from the first PR.

LANE EXCEPTION (Jon, 23 Oct 2026, 23:05): the cloud lane may build this new game and edit the home-lane files a new unlisted game needs (roster Unlisted section, data/games.json if needed, scripts/check-leaderboard-coverage.js unlisted entry, and one board label "stage-5" → "Stage 5" in the shared label map in firebase-leaderboard.js, nothing else in that file), for this PR only. Record it in the PR and the cloud handover, with a shared-file note in docs/handover/home.md.

TASK: Build "Football Pitches per Squared Squirrel", a compound-measures game for grade 1-3 and resit students built on one idea: the units tell you what to do. Merge it unlisted for Jon to play.

ROOT CAUSE: New build (Jon, 23 Oct 2026). An audit of 18 OCR J560 Foundation papers (six series) found compound measures worth 8.2 marks a series, in every series, with no game: the biggest true gap on the site. Priority 2. Jon's classroom premise: "football pitches per squared squirrel" means football pitches ÷ squared squirrels; read the unit and you know the calculation.

CLASS CHECK: Not a bug; a new game. Follow Take a Walk (games/take-a-walk/, #495-#504) and How Many Parts? for structure: stages played one at a time, each its own board and analytics mode, a stepped worked example first, easiest first, "Next: Stage N+1", generated enumerated pools, verifier with plants (SR-30), the calculator tag `by stage` (#494), MaffsKeypad/MaffsAnswer for typed answers with the unit chosen from buttons. Use shared modules as they are; no new shared code beyond the one board label.

EXACT CHANGE: games/squared-squirrel/index.html, scripts/verify-squared-squirrel.py, docs/audits/findings/squared-squirrel.yml (findings: []), the registrations above. Title "Football Pitches per Squared Squirrel". Roster levels KS3, GCSE; light palette; adult register; standard header; the START-MOUNT start-screen mount; noindex and an UNLISTED comment. Keys `ks3`, `gcse`, no level picker (Free Daily Pizza / Take a Walk pattern). Boards and modes `stage-1`..`stage-5`. Visible count-up, scored. Calculator: none in stages 1-3, scientific on-screen calculator in stages 4-5 (`by stage`). Leave contexts' jokes plain: Jon writes them.

STAGE 1, "Read the unit": a fixed ramp, not a pool, served in this order every time. Worked example first (tap-through: "Crisps are 80p per bag: 80p for each bag." "Per" means "for each"), then:
1 "The sign says 30 mph." What does it mean? [30 miles every hour] / 30 hours every mile / 30 miles in total
2 "Apples are £2 per kg." [£2 for each kg] / £2 for all the apples / 2 kg for each £1
3 "Miles per hour is…" [miles ÷ hours] / hours ÷ miles / miles × hours
4 "km/h is…" [km ÷ h] / h ÷ km / km × h
5 "£/kg is said…" [pounds per kilogram] / kilograms per pound / pounds times kilograms
6 "m² means…" [m × m] / m × 2 / m + m
7 "cm³ means…" [cm × cm × cm] / cm × 3 / cm + cm + cm
8 "g/cm³ is…" [g ÷ (cm × cm × cm)] / (cm × cm × cm) ÷ g / g × cm × 3
9 "Football pitches per squared squirrel is…" (deadpan, as if a normal unit) [football pitches ÷ (squirrel × squirrel)] / (squirrel × squirrel) ÷ football pitches / football pitches ÷ (squirrel × 2)
10 "12 miles in 3 hours. How many miles per hour?" typed: 4, unit mph
Options shown in a shuffled order; each wrong option is a named slip with a one-line reason. Questions 1-3: a wrong answer shows the reason and lets the student try again without losing the mark (one question_answered, correct only when finally right on the first try? No: log correct:false on a wrong first try, but score is not reduced). Stage 1 is exempt from the 40-question pool rule (a fixed ramp; Jon's ruling); record that in the roster row.

STAGES 2-5, generated pools of at least 40 distinct questions each, easiest first by a measure stated in a code comment:
2 Find the rate: speed, density, pressure, unit price; "per" means divide; whole-number answers, non-calculator friendly numbers.
3 Use the rate: find distance, time, mass or cost from a rate; multiply or divide as the units say; non-calculator friendly numbers.
4 Units that don't match: minutes to hours (1 h 30 min = 1.5 h), rates over minutes, m/s ↔ km/h (× 3.6 / ÷ 3.6); calculator.
5 Mixed and backwards: compare two rates (which is faster / better value), work back from a total; calculator.
A nonsense-unit question appears now and then in stages 2-5 (about 1 in 10), built on the same structure as a real one, as a check that the student reads the unit.

ANSWERS: typed number plus a unit chosen from buttons offering the units in play (e.g. km/h, km, h). An answer submitted with no unit chosen is treated as squirrels (or squared/cubed squirrels, matching the quantity's dimension) and gets: "42 squirrels? Pick the unit, or that's what the examiner will read." (use the student's number); fix and resubmit, no penalty, not marked (SR-3 pattern). Right number, wrong unit: the existing unit-format message, no penalty. Calculator-stage answers to the precision the question states.

NO FORMULA TRIANGLES anywhere: no triangle drawing, wording or hint. Hints and wrong-answer help point to the unit ("km/h means km ÷ h, so…").

NAMED WRONG ANSWERS (each with a one-line reason and, for the first three per session, a worked line on the question's numbers): multiplied instead of divided and the reverse; divided the wrong way round (h ÷ km); 1 h 30 min as 1.3 h (and similar minutes-as-decimals); a per-hour rate used with minutes unconverted; m/s ↔ km/h by the wrong factor or direction. A question leaves its pool if any named slip equals the key (canon §12, SR-5).

VERIFIER (in CI from this PR): recomputes every key independently from the question's data; checks unit dimensions (the answer's unit matches the quantity asked); checks no named slip equals the key; checks stage 1 is exactly the fixed sequence above in order; checks no formula-triangle wording or drawing anywhere in the page; checks the no-unit "squirrels" message appears and does not mark; checks the calculator mounts in stages 4-5 only; checks ordering by the measure; plays every stage to its results screen at 1280 and 320 px with no sideways scroll. Plants, each caught: a key computed by multiplying where it should divide; a stage 1 question out of order; a named slip equal to a key; the word "triangle" in a hint; a no-unit answer marked wrong; the calculator in stage 2; a stage 4 key using 1.3 for 1 h 30 min.

DO NOT TOUCH: Any other game; shared modules beyond the one label; the workflow; canon; docs/todo.md; the portal, Essentials, sitemap, spec map and hub (listing comes after Jon plays it).

SUCCESS CONDITION: The game plays all five stages at its URL, unlisted and noindex; stages 2-5 each have at least 40 distinct questions; stage 1 is the fixed ramp; the verifier passes and catches every plant; check-changed.py finishes before the first push; merged through merge-pr.py on a green Gate with no skip-CI words in the PR title, body or commit message; main's full run green (confirm it started).

STOP IF: Any of stages 2-5 has fewer than 40 distinct questions (report the counts); MaffsAnswer cannot take a number plus a chosen unit with a "no unit" state; a shared module needs a change beyond the board label; or a stage's friendly-number constraint cannot be met for a context the spec names.

FINISH: Merged; docs/handover/cloud.md records the entry, the lane exception, PR, main run and each stage's pool size. Tell Jon it is ready to play at https://maffsgames.co.uk/games/squared-squirrel/.
