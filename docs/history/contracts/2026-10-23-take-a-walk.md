# Contract TAKE-A-WALK (Jon, 23 Oct 2026), verbatim

Stopped by the cloud lane on 23 Oct on its STOP IF (the calculator tag could not express "Stage 4 only"); Jon then sent
contract CALC-BY-STAGE (`docs/history/contracts/2026-10-23-calc-by-stage.md`), after which this is built with roster value
`by stage`.

MODEL: Opus, medium effort. A new game from a full spec: generated pools, a stepped worked example, two animations and a verifier from the first PR.

LANE EXCEPTION (Jon, 23 Oct 2026, 08:32): the cloud lane may build this new game and edit the home-lane files a new unlisted game needs (roster Unlisted section, data/games.json if the game needs an entry, scripts/check-leaderboard-coverage.js NOT_ON_HUB / unlisted entry, any game-listing check's suite), for this PR only. Record it in the PR and the cloud handover.

TASK: Build Take a Walk, a new area-and-perimeter game for grade 1-3 and resit students, set on sports pitches, merged unlisted for Jon to play.

ROOT CAUSE: New build (Jon, 23 Oct 2026). Area and perimeter, including circles, is on every GCSE Foundation paper and has no dedicated game; Essentials' Geometry section has four games, one pitched at Year 6. Priority 2 (canon §0.2). Jon's premise: "Are we walking around the outside, or are we covering every blade of grass?"

CLASS CHECK: Not a bug; a new game. Follow How Many Parts? (games/how-many-parts/, #491) for structure: stages played one at a time, each its own board and analytics mode, a stepped worked example first, easiest-first ordering, "Next: Stage N+1", generated enumerated pools, verifier with plants (SR-30: verifier in the first PR, findings file, one build in flight). Use shared modules as they are (MaffsAnswer, MaffsKeypad, MaffsCalc scientific with its π key, MaffsLevel, analytics.js, submitScore); no new shared code.

EXACT CHANGE: games/take-a-walk/index.html, scripts/verify-take-a-walk.py, docs/audits/findings/take-a-walk.yml (findings: []), plus the registrations the exception allows. Slug `take-a-walk`, title "Take a Walk". Roster levels KS3, GCSE; light palette; adult register; standard header (back link, Aa); noindex and an UNLISTED comment like How Many Parts? had.

THE PREMISE. Every shape is a sports pitch or part of one (football, rugby, hockey, tennis, netball, cricket square, five-a-side; penalty area, six-yard box, centre circle, the D where they fit), drawn to scale on a grid with its lengths labelled.
- Walk (perimeter): a small figure walks the edge and a distance counter counts up as it goes.
- Cover (area): the grass is mown in stripes and the squares fill in.
- After a wrong answer, the right picture replays on that question's numbers (adding the sides for an area shows the walk, not the mowing), with a one-line explanation of the named mistake, then the correct working, then Next. Next is available at once; nothing auto-advances.
- Leave the walker's lines, the mower and the results-screen text plain: Jon writes any jokes.

STRUCTURE. Four stages, all offered on the start screen, played one at a time, each with its own leaderboard and analytics `mode` (boards and modes `stage-1`..`stage-4`; one level key, `ks3`, as Just Pythag It, Bruv). On screen "Stage 1".."Stage 4", never "Level". Each stage: one worked example (the shape with its walk or mowing, explained one step per tap on its own numbers, ending on the answer; no score, no question_answered), then 10 questions, easiest first by a measure stated in a code comment (fewest parts, then smallest numbers, perimeter and area before working backwards). Visible count-up, scored (canon §7.3). Results screen offers "Next: Stage N+1" (none after 4).

| Stage | Shapes | Information |
| 1 | Squares and rectangles; compound shapes made only of rectangles in the later questions | Every length given |
| 2 | Squares, rectangles and compound rectangles | One length missing, found from the drawing |
| 3 | Compound shapes that can include triangles (a triangle on its own first) | Two lengths missing |
| 4 | Compound shapes that can include circles, semicircles and parallelograms (each on its own first) | Three lengths missing |

RULES.
1. Walk or cover (Stage 1, every question): the student first chooses Walk (perimeter) or Cover (area) from the context ("a fence round the pitch", "new turf for the pitch"), then calculates. A wrong choice shows the walk or the mowing and asks again (no score lost for the choice, one question_answered for the calculation). From Stage 2 the choice is not asked; it returns as part of the feedback after a wrong answer.
2. Missing lengths are found from the drawing by comparing with the opposite side(s). Every missing length must be uniquely determined by the labelled ones; never a second unknown.
3. Find it first: the first question of each stage that has a missing length opens with "Click the side with missing information." The student must tap the unlabelled side before calculating; a wrong tap highlights the opposite sides to compare.
4. Working backwards ("The area is 48 m² and the length is 8 m. How wide is it?", and the perimeter version) in the later questions of every stage.
5. Stage 4 shows both formulas on screen, A = πr² and C = πd, and mounts the shared on-screen calculator in scientific mode (π key). Stages 1-3: no calculator. Roster calculator tag as the shared check requires for a game that shows it in one stage; if the tag model cannot express "Stage 4 only", STOP.
6. Answers are typed on MaffsKeypad, with the unit chosen from two buttons, m or m². The right number with the wrong unit gets a format message ("That would lose the mark in the exam. Check the unit."), fix and resubmit, never marked right or wrong (SR-3 pattern, as money answers). Stage 4 answers to 1 d.p.; a numerically right answer in another form gets the format message.
7. Numbers: whole metres in Stages 1-3 (Stage 1 sides up to 20 m, growing later); Stage 4 radii and diameters whole metres, answers to 1 d.p.

NAMED WRONG ANSWERS (each offered as a recognised slip with its own one-line explanation and picture; the first three per session get a worked example on the question's numbers, then a nudge, as How Many Parts?):
- area worked as perimeter (added the sides); perimeter worked as area (multiplied)
- rectangle perimeter as l + w (two sides only)
- compound perimeter missing the unlabelled sides, or including an inside join line
- compound area from the outer sides, or an overlap counted twice
- a missing length copied from the nearest label instead of the opposite sides
- triangle not halved; triangle or parallelogram using the slant side instead of the perpendicular height
- circle: diameter used for radius and the reverse; πr² for a walk or πd for a cover; (πr)² instead of πr²
- semicircle walk using the full circumference, or leaving out the straight diameter

POOLS AND CHECKS. Questions generated from parameters into enumerated pools (no rejection loops, canon §12, SR-5); at least 40 distinct questions per stage. The verifier, in CI from this PR: recomputes every key from the drawn lengths independently of the game's code; checks every missing length is determined by the drawing and that the number missing matches the stage (1, 2, 3); checks no named wrong answer equals the key on any question (key-collision survey form); checks the drawing's labels match the data and the shape is drawn to scale within 1 px per unit; checks ordering is non-decreasing by the measure; checks the worked example fires no question_answered; plays every stage to its results screen at 1280 and 320 px with no sideways scroll; checks the Stage 1 walk-or-cover step and the find-it-first tap. Plants (each caught): a key computed as l + w; a stage-3 question with a missing length that cannot be determined; a named wrong answer equal to the key; a stage-1 question with a missing length; the worked example logging an event; a reversed order; the calculator mounted at Stage 2.

DO NOT TOUCH: Any other game; shared modules in schools/assets/ and scripts/; the workflow; canon; docs/todo.md; the portal, Essentials, sitemap, spec map and leaderboard hub (listing is a later contract, after Jon plays it); How Many Parts?.

SUCCESS CONDITION: The game plays all four stages at its URL, unlisted and noindex; each stage has at least 40 distinct questions; the verifier passes and catches every plant; the roster's Unlisted section has the row; check-changed.py finishes before the first push; merged through merge-pr.py on a green Gate; main green.

STOP IF: Any stage's pool is under 40 distinct questions (report the counts); a shared module needs a change (MaffsAnswer cannot take a number-plus-unit answer, MaffsCalc's scientific mode cannot mount for one stage only, the calculator tag cannot express Stage 4 only); a missing length cannot be made uniquely determined for a shape type the spec requires; or the scale drawing cannot fit 320 px for the largest Stage 4 shape.

FINISH: Merged; docs/handover/cloud.md records the entry, the lane exception, PR, main run, each stage's pool size and the ordering measure. Tell Jon it is ready to play at https://maffsgames.co.uk/games/take-a-walk/.
