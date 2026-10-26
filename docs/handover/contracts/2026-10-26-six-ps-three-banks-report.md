# SIX-PS-THREE-BANKS: stopped at step 1 (26-27 Oct 2026)

**Result:** the STOP IF fired for all three sources. Nothing was banked, no bank file or generator changed, and no review sheet was republished. Step 5 (the phone-fit roster) was never reached. Counts below were taken from the games on main at 137ed468.

## Counts (step 1)

| Source | What it holds | Bankable Foundation questions | Needed |
|---|---|---|---|
| `given-that` | 4 levels x 20-25 items: gcse 25 (table 12, venn 8, tree 5), alevel 25, core 20, level4 20. Each item has a phase 1 (a plain P(A) read off the table, Venn or tree) and a phase 2 (always a conditional P(A given B), Higher content, excluded). | **25** (gcse phase 1, all with the game's own four options) | 30 |
| `coordinate-geometry-dash` | gcse 24 (midpoints 3, gradients 5, equation of a line 3, parallel/perpendicular 3, distance 3, more equations 2, collinear 1, intersections 2, harder 2); alevel not Foundation. | **at most 21** (24 less the 3 perpendicular items); fewer if midpoints, distance, collinear and algebraic intersections are judged not Foundation | 30 |
| `constructions-lab` | 10 drawing tasks (the compass-and-ruler steps), **no questions and no answers at all**. | **0** | 30 |

## Notes for Project Claude

- **Set notation:** none in the 25 gcse items (the cap/cup/prime items are all A-Level: alevel_06, 09, 11, 13, 21, 22, 24), so nothing needs your check from the gcse pool.
- **Given That:** the 25 are all plain probabilities from a diagram. Venn 8, table 12 and tree 5 would each need an inline SVG (a Venn, a table grid, a frequency tree) through the diagram check; the answers fit `fraction` (or the game's own `choice`). Two ways to reach 30 without writing new questions: the 10 Core Maths two-way-table items' phase 1 (plain P from a table, 35 in all), and the 10 Level 4 table items (45). I did **not** include them: they are the game's Core and Level 4 content, and whether they count as Foundation is your call. The Core and Level 4 tree items need the total probability across branches, so I left those out of any count.
- **Coordinate Geometry Dash:** its answers are text options such as `(4, 5)`, `3/2`, `y = 2x - 1`, `5√2`. Coordinates fit `coordinates`, gradients `fraction`, equations only `choice`, and 'Undefined (vertical)' and 'Yes, all on y = x + 1' only `choice`. Nothing here needs a new answer format. It still cannot reach 30, so the rest would have to be written by you.
- **Constructions Lab:** nothing to bank. Every task is a drawing task, which the 6 P's answer formats cannot take, and the game holds no question list to draw from. The whole bank (30+) would have to be authored.
- **Bank count:** the repo has 32 banks, and 35 is right once these three land (pie charts make 36). The three would be new topic ids `venn-two-way`, `straight-line-graphs`, `constructions-loci`; the exam-topics table currently lists them as coming soon under the ids `venn`, `two-way-tables`, `straight-line-graphs` and `constructions`, so the slugs in the contract need reconciling with `gen-exam-topics.py` (and `venn` plus `two-way-tables` are two rows there, one topic in the contract) when the banks are written.

## What is left

Steps 2 to 6 of the contract, once Project Claude has either supplied the missing questions or ruled on the Core and Level 4 items. Step 5 also waits on the cloud lane's `measure-phone-fit.py` change.
