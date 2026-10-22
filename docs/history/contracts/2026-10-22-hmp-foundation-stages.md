# Contract HMP-FOUNDATION-STAGES (Jon, 22 Oct 2026), verbatim

MODEL: Opus, medium effort. One game, but it restructures its level and session logic and adds a stepped worked example.

TASK: Rebuild How Many Parts?' Foundation level as five stages a student plays one at a time, each one idea, easiest first, opening with a worked example, so a grade 1-3 student is never moved on before they are ready.

ROOT CAUSE: Jon's play-test (22 Oct): Foundation escalates too fast for resit students. H.LEVELS.ks3 runs stages a-d in one 20-question session, 5 per stage (games/how-many-parts/index.html:341), so a student meets four ideas in 20 questions. Stage c draws from one pool for every unrelated pair with a common denominator up to 24 (H.STAGE_OF, H.MAX_PARTS), so 1/3 + 1/4 (product works) and 1/12 + 5/8 (lowest common denominator 24, not 96) are the same stage. The bar shows before answering on the first 3 questions of every stage (H.BAR_FIRST = 3), so the answer can be counted off the screen, and it has no explanation (Jon: "the bar without an explanation is not helping at all").

CLASS CHECK: Local. The level structure, pools, bar and session builder are this game's own code, used by no other game. Simultaneous Solver's staged Foundation (one mode per stage, own board each) is the site's precedent for the shape and is followed, not shared.

EXACT CHANGE (games/how-many-parts/index.html and scripts/verify-how-many-parts.py only):
1. Foundation becomes five stages, each a mode the student picks on the start screen, all five offered from the start, and each with its own leaderboard (follow simultaneous-solver's foundation-s1..s4 pattern for mode keys, boards and analytics `mode`; the level stays `ks3`):
   1 Same bottom number (today's pool a)
   2 One bottom a multiple of the other (pool b)
   3 Different bottom numbers, multiply them (pool c where lcm(b,d) = b*d)
   4 Different bottom numbers, a smaller common one (pool c where lcm(b,d) < b*d)
   5 Multiply (today's stage d)
   Show them as "Stage 1"..."Stage 5" with today's stage labels updated to match.
2. A stage is 1 worked example followed by 10 questions. Within a stage, questions are served easiest first by a stated measure (common denominator ascending, then an answer that needs no simplifying before one that does; record the measure in a code comment). About half add and half take away in stages 1-4, as now.
3. The worked example (question 1 of every Foundation stage): the bar, with an explanation revealed one tap at a time on the question's own numbers, ending on the answer. For 1/12 + 5/8: (1) each bar is one whole chocolate bar; (2) 1/12: cut into 12, take 1; (3) 5/8: cut into 8, take 5; (4) you can only add pieces the same size: cut each twelfth into 2 and each eighth into 3, both are now 24ths; (5) 1/12 is 2 pieces, 5/8 is 15: 2 + 15 = 17, so 17/24. Step 4 is worded per stage (stage 1: already the same size, just count; stage 2: only one bar needs cutting; stage 5: the multiply slab, explained the same way). No score, no question_answered event, not counted in the 10.
4. Questions 2 onwards: no bar before answering. After any wrong answer: the bar with the same stepped explanation on that question's numbers (replacing the bar shown alone today), then the existing line and Next.
5. Finishing a stage: results as now, plus a "Next: Stage N+1" button (none after 5).
6. Advanced (gcse): unchanged in stages, counts and boards, except the bar rule in 3-4 (worked example on question 1 of each stage, bar after a wrong answer only).
7. The wrong-answer line's split brackets at 320 px (docs/audits/k-punctuation-scan-2026-10.md, how-many-parts, 5 screens): keep a bracket with its maths in renderLine so no line starts with ")" or ends with "(".
8. Verifier: each Foundation stage's pool contains only its idea (stage 3 lcm = product, stage 4 lcm < product); ordering is non-decreasing by the measure; question 1 is the worked example and fires no question_answered; no bar before answering on questions 2-11; the bar and steps appear after a wrong answer; every mode logs its own `mode` and posts to its own board; the 320 px bracket check over every wrong-answer line. Plants: a stage 4 pair in stage 3, a bar before answering on question 2, the worked example logging an event, a reversed order; each caught.
9. Roster row 99 updated to the new structure; the game stays unlisted.

DO NOT TOUCH: Any other game; shared files (schools/assets/, scripts/ shared modules, the workflow, canon, docs/todo.md); the question pools' contents beyond splitting pool c; marking (MaffsAnswer.fractionForm, the error lists, SR-3 format handling); Advanced's stages and boards; the chocolate bar's drawing style; the listing status.

SUCCESS CONDITION: Foundation offers five stages, each 1 worked example + 10 questions easiest first; stage 3 never serves a pair whose lowest common denominator is smaller than the product, and stage 4 only such pairs; no bar before answering after question 1; the verifier passes and catches every plant; check-changed.py finishes before the first push; merged through merge-pr.py on a green Gate; main green.

STOP IF: Any Foundation stage's pool has fewer than 40 distinct questions after the split (report the counts); the leaderboard or analytics pattern needs a shared-file change (hub registry, leaderboard coverage, analytics.js); Simultaneous Solver's mode pattern doesn't fit and a new pattern would be needed; or the worked example needs anything beyond this game's file.

FINISH: Merged; docs/handover/cloud.md records the entry, PR, main run, each stage's pool size and the ordering measure. Tell Jon it's ready to play again at https://maffsgames.co.uk/games/how-many-parts/.
