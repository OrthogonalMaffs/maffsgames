CANON-PRIORITY (Project Claude, Thu 26 Nov 2026 16:05; checked against main dd74964)
Jon, 26 Nov 2026: 13:40 "My students jump the queue most often, so they're probably top priority ... Resit is our core, and primary also gives core skills the resit crowd often need to improve anyway." 13:43 approved Project Claude's wording: "that's fine, I over ride it on a whim anyway but it's good to have it written. Only I know the urgency of certain tasks." 13:43 Holey Moley folds into I Dropped My Ice Cream; "d by dx? Why?" assessment probably the 3rd week of January, no building over Christmas. 13:56-13:57 "people on a phone will have to accept that the personality is secondary to useability, no point being pretty or cute if it's unplayable because of scroll issues"; "yes please" to SR-35. 14:11-14:14 on "d by dx? Why?": integration taught as reverse differentiation ("what do I need to differentiate to get this answer?"); a check step differentiating the answer back, mandatory, not scored; a missing + C is a wrong answer.
RECOMMENDED: Claude Code, Sonnet or Opus, effort low. Docs only, exact text given.
LANE: home. SEND: now, first of the evening (before BASE-60-LIST). First commit carries the home lane's previous merge's close-out per docs/handover/home.md (AGENTS.md:62).
TIER: Medium (merge on green).

TASK: Write Jon's new priority order into canon §0.2, add standing ruling SR-35, align SR-33, and record three backlog changes.

ROOT CAUSE: canon §0.2 (docs/canon.md:45-50) ranks the resit audience second and Level 4 fifth; Jon's ruling of 26 Nov puts his own classes' lesson and assessment needs second, after correctness. SR-33 (:95) cites "§0.2 priority 2" and "priority 6", which the new numbering moves. "d by dx? Why?" (Jon's Level 3 calculus game, scoped 17 Nov) has no backlog row. Holey Moley (docs/todo.md:180, "Game ideas, not yet built") is now part of I Dropped My Ice Cream.

CLASS CHECK: Local: one canonical document and the backlog. Searched on dd74964: no other file in docs/canon.md, AGENTS.md, CLAUDE.md or .claude/rules/ cites a numbered §0.2 priority (only SR-33 does).

EXACT CHANGE:
1. docs/canon.md §0.2: replace the numbered list (:45-50, "1. **Correctness on live games.**" to "6. **New builds for other audiences.**") with exactly:
1. **Correctness on live games.** Wrong maths or a broken game, first. A struggling student is the least able to spot a wrong answer.
2. **Jon's own classes.** What his current lessons and assessments need (Level 3 and Level 4 engineering apprentices), built to that need and no further, then maintained. It jumps the queue; once built, it serves every class on that unit. Only Jon knows a task's urgency, and he may reorder any of this list at any time (Jon, 26 Nov 2026).
3. **The core audience: resit and grade 1–3 students.** Their content, including the foundational skills behind it (SR-33), and making it findable by the people who teach it. Primary classes are served here through SR-33's one bank with two looks, because primary skills are the resit crowd's gaps.
4. **Gatekeeper trust.** Anything that makes the portal look less credible to a resit lecturer.
5. **Depth of the existing library.** Question-bank quality and quantity for live games.
6. **Level 4 / Further Maths beyond Jon's classes.** Maintained, not expanded ahead of the above.
7. **New builds for other audiences** (for example 8:53, or a game with a child-only look).
   Keep the paragraph above the list and the sentence after it ("This is the only copy in the repo...") unchanged.
2. docs/canon.md SR-33 (:95): "count as §0.2 priority 2 when built" becomes "count as §0.2 priority 3 when built"; "stays priority 6" becomes "stays priority 7". Nothing else in the row changes.
3. docs/canon.md §0.3: a new row after SR-33 (SR-34 stays reserved for large screens, todo LARGE-SCREEN-LAYER), in the table's format:
| SR-35 | **On a phone, playability beats personality.** Decoration (pictures, characters, art, animation) shrinks or steps aside before it costs the fold or adds a scroll; it grows only where the screen has room. "No point being pretty or cute if it's unplayable because of scroll issues." | 26 Nov 2026 | Jon, 26 Nov 2026 (chat) |
4. docs/todo.md (AGENTS.md row sizes):
   a. New row in §3, D-BY-DX: **"d by dx? Why?": Jon's Level 3 calculus game** (EAL AME3-004, assessment 004C, probably the 3rd week of January 2027). Scope (Jon, 17 Nov 2026): differentiation of power terms (including √(r³)) and cos(at); integration of power terms, ∫5/x² (not an ln question) and e^(5x); much easier than the calculus duels, one joined-up game, with his cheat sheet; a sequel in name to Y So Steep?. Rulings (Jon, 26 Nov 2026): one game, differentiation then integration; integration as reverse differentiation ("what do I need to differentiate to get this answer?"); every integration item has a check step differentiating the answer back, mandatory and not scored; a missing + C is a wrong answer. Built and played before the Christmas break (no building over Christmas). Owner: Project Claude (spec), then a lane.
   b. New row in §3, ICE-CREAM-GCSE: **I Dropped My Ice Cream gets GCSE-only stages before it is listed** (Jon, 26 Nov 2026): cylinder; arcs and sectors; sphere and hemisphere; the whole ice cream (a cone plus a hemisphere). Level 3 unchanged. Holey Moley folds in here (no separate circles game). Owner: Project Claude (spec and bank), then a lane.
   c. ICE-CREAM-LIST row (:111): add "Listing waits for ICE-CREAM-GCSE (Jon, 26 Nov 2026)."
   d. "Game ideas, not yet built", Other games (:180): remove the Holey Moley line; add "**Holey Moley**: folded into I Dropped My Ice Cream (ICE-CREAM-GCSE, Jon, 26 Nov 2026)." only if the list keeps a record of folded ideas, otherwise just remove it.
5. docs/handover/home.md entry. No /updates/ line.

DO NOT TOUCH:
- Any other canon section or standing ruling; SR-34's number (reserved).
- Any game, schools/assets/, scripts, workflows, the roster.
- Other todo rows than those named.
- PR #916 (the site bar pilot, open by Jon's ruling) and PR #927 (lane 2's large-screen layer, open).

SUCCESS CONDITION:
- canon §0.2 reads exactly as above, SR-33 cites priorities 3 and 7, SR-35 is in §0.3; check-context-size and every docs check pass.
- todo has D-BY-DX and ICE-CREAM-GCSE, ICE-CREAM-LIST's added sentence, and Holey Moley handled as step 4d.
- Merged on green through merge-pr.py; main green after; last line and main's runs reported; home.md records it.

STOP IF:
- Any file other than SR-33 turns out to cite a numbered §0.2 priority: report it before renumbering.
- A todo row would exceed AGENTS.md's size rule and cannot be shortened without losing a ruling.
- main is red when you come to merge: report it; do not use --override.
- merge-pr.py cannot reach GitHub or refuses: report its output; do not merge another way.
