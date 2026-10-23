# Contract CALC-BY-STAGE (Jon, 23 Oct 2026), verbatim

MODEL: Sonnet, medium effort. One shared check, its selftest, a canon row and a roster value; small and well bounded.

LANE EXCEPTION (Jon, 23 Oct 2026, 09:45): the cloud lane may edit scripts/check-calculator.py, docs/canon.md §4.4 and the roster's calculator-value list for this PR only, then build Take a Walk on top of it. The home lane is idle until evening. Record it in the PR and the cloud handover, with a one-line shared-file note in docs/handover/home.md.

TASK: Let a game's calculator tag be set per stage, so a staged game can be non-calculator in some stages and calculator in others, with the check enforcing it exactly as it does a whole-game tag.

ROOT CAUSE: The calculator tag (canon §4.4) and scripts/check-calculator.py allow one value per game, read from the roster's last column. Take a Walk needs no calculator in Stages 1-3 and the scientific calculator (π key) in Stage 4 (Jon's ruling, 23 Oct 2026); the planned pie-chart game is likely to need the same in some stages. Tagging the whole game `scientific` would tell a Stage 1 student they need a calculator; leaving it out breaks the ruling. The cloud lane stopped Take a Walk on this (23 Oct).

CLASS CHECK: Yes: shared infrastructure (one check over every game's tag) that cannot express a shape every staged game may need. Fix it in the tag model and the check, once, not by mis-tagging one game.

EXACT CHANGE:
1. A new roster value, `by stage`. A game with it declares its stages once in its page: <script type="application/json" id="maffs-calc-stages">{"stage-1":"not allowed","stage-2":"not allowed","stage-3":"not allowed","stage-4":"scientific"}</script>. Keys are the game's stage/mode keys; each value is one of the existing values except `untagged` and `by stage`.
2. On the page, each stage's choice on the start screen shows that stage's badge (the existing `<span class="calc-badge" data-calc="…">` markup and wording, from theme.css, never restyled), and the game header shows the badge of the stage being played.
3. check-calculator.py, for a `by stage` game: the map is present, is valid JSON, and every value is allowed; there is one badge per stage, matching its value; if any stage is `required` or `scientific`, the page includes calculator.js and keypad.js; if any stage is `scientific`, it mounts MaffsCalc with keys: 'scientific'; if no stage needs a calculator, it does not include calculator.js. A map on a game whose roster value is not `by stage` fails, and so does `by stage` with no map. Whole-game values behave exactly as now. That the calculator mounts only in the calculator stages is the game's own verifier's job, as the play-through is; say so in the check's docstring.
4. Selftest plants, each caught: `by stage` with no map; a map value outside the list; a stage badge disagreeing with its map value; a scientific stage with no scientific mount; a map that needs a calculator but no calculator.js; calculator.js on a map with no calculator stage; a map on a whole-game-tagged page. Every existing case still passes unchanged.
5. Canon §4.4: add the `by stage` row and one paragraph on the map, the per-stage badges and what the check enforces.

DO NOT TOUCH: MaffsCalc, keypad.js, theme.css and the badge styling; every existing game's tag, page and badge (no game's output changes); the roster's other values; any game other than Take a Walk (which adopts `by stage` in its own PR); the workflow.

SUCCESS CONDITION: The check passes on main unchanged for every existing game; the selftest catches all seven plants; canon §4.4 documents `by stage`; check-changed.py finishes before the first push; merged through merge-pr.py on a green Gate; main green. Then build Take a Walk (its contract, already sent) with roster value `by stage` and the map above, its verifier asserting the calculator is mounted in Stage 4 only.

STOP IF: Any existing game's result changes under the new check; the stage keys of a staged game cannot be read statically from its page (the map would need runtime code to check); or the badge per stage needs a change to theme.css or a shared module.

FINISH: Merged; docs/handover/cloud.md records the entry, the lane exception, PR and main run; docs/handover/home.md gets the one-line shared-file note (check-calculator.py, canon §4.4) so the home lane rebases knowingly.
