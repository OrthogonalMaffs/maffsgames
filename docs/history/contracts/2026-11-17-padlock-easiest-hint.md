LANE: cloud (Claude Code on the web). Exception to one lane at a time (Jon, 17 Nov 2026): this starts while the home lane's merge-pr.py waits on PR #807.
RECOMMENDED: Opus 5.5, high effort. It changes the shared padlock search and the self-tests behind every pack.

TASK: PADLOCK-EASIEST-HINT. The final-padlock search takes the easiest difficulty class that gives enough sets. The final-padlock hint card and the key's final-padlock line are worded from each pack's padlock shape.

ROOT CAUSE:
(1) tools/pack-generator/build_pack.py choose() (about line 867) shuffles the classes by the seed:
    random.Random("%s-class" % seed).shuffle(classes)
    So a pack can get a harder class than it needs. Car Trap got 1-digit x 3-digit (products 645-1,935) when 90-270 was possible; Library Jam and PE Shed Rebellion are the same. Jon's ruling, 17 Nov 2026: easiest first.
(2) The final-padlock wording assumes a multiplication. build_pack.py FINAL_HINT (about line 1804) reads "Is the target close to a round number? Which two of your answers multiply to about that?". The key's "About this room" (about line 1761) reads "find the two answers whose product is close". Heatwave Mutiny's padlock is plus-and-minus (rooms/heatwave-mutiny/config.json "final_shape"), so neither helps.

CLASS CHECK: Both are architectural.
(1) choose() is shared by all ten packs, so the order is fixed there, once.
(2) The wording is a property of the shape. It goes beside the shape's rule in final.py SHAPES (the single source), with a check that every shape has its wording and that no pack prints another shape's wording. A Heatwave-only override would leave the same trap for the next plus-and-minus room.

EXACT CHANGE:
0. Before starting: make sure PR #807 (FINAL-PADLOCK-FAIR) is merged on main. Run git fetch origin main and look for "FINAL-PADLOCK-FAIR" in git log origin/main. If it is not there, check again every 5 minutes for up to 60 minutes. Branch from origin/main only once it is there. First commit: the #807 close-out, per AGENTS.md's close-out rule. It records the merge commit, main's check-site and phone-fit-full run IDs on it, and moves the contract to docs/history/contracts/.
1. Easiest class first.
   - Add finalpad.ease(klass) in tools/pack-generator/final.py, a sort key.
   - For ("x", sig): each product's digit counts are already sorted ascending, e.g. (1, 2). The key is the hardest product in sig, compared as (fewer digits in the smaller factor, then fewer in the larger), then the number of products. This puts 1x1 < 1x2 < 1x3 < 1x4 < 2x2 < 2x3: short multiplication comes before long.
   - For ("+-", n): the key is n.
   - In build_pack.py choose(), replace the seeded shuffle of classes with sorted(classes, key=finalpad.ease).
   - Keep everything else as it is: each class's windows smallest product first, and the seeded draw order within a class. The first class and window that reach N sets win.
   - Update the docstrings that say the classes are tried in a seeded order (final.py about line 24, build_pack.py about line 857), the README, and the canon standing ruling #807 added (docs/canon.md escape-room/print-pack section and §0.3). Add the line "easiest class first (Jon, 17 Nov 2026)".
2. Shape wording.
   - Give each entry in final.py SHAPES a student hint and a key line.
   - "times-and-plus-or-minus" keeps today's text exactly. Hint: "Is the target close to a round number? Which two of your answers multiply to about that?" Key: "Estimation is the intended route: round the target, then find the two answers whose product is close."
   - "plus-and-minus": Hint: "Which of your answers is closest to the target? Use the other two to make up the difference." Key: "Estimation is the intended route: find the answer closest to the target, then the two answers whose difference closes the gap."
   - build_pack.py takes both from the pack's shape. FINAL_HINT, and every use of it including the student-page text check (about line 2401), reads the shape's hint.
   - A build fails, naming the shape, if a shape has no hint or no key line.
3. Tests, in build_pack.py --selftest and scripts/test-pack-generator.py, with the ci-line updated to name them.
   Plants, each of which must be caught:
   - the classes tried in seeded order, with a harder class chosen where an easier one reaches N;
   - a SHAPES entry with no hint;
   - a plus-and-minus pack whose hint card or key says "multiply" or "product".
   Controls, each of which must pass:
   - ease() orders 1x2 < 1x3 < 2x2 < 2x3, and +- 3 < +- 4;
   - for every room, every class easier than the one chosen gives fewer than N sets;
   - Hamster Heist's hint as built (unchanged text);
   - Heatwave's hint and key as built (plus-and-minus text).
4. Rebuild all ten packs: nine with --final, Heatwave as DRAFT. Do not change any pack_version. None of #807's versions has been uploaded to Tes, so the names stay as #807 set them. Report each pack's class and product range before and after, and every set's padlock.
5. docs/todo.md:
   - PACKS-V2-UPLOAD: note that it waits for this merge.
   - Remove the hint-card item from Heatwave's approval row.
   - docs/handover/cloud.md: record the state.
6. Merge with scripts/merge-pr.py when the Gate is green. That is the only merge route.

DO NOT TOUCH:
- PRODUCT_MAX, RATIO_MAX, friendly(), the plus-and-minus class rule, the shapes themselves, any pack_version, page 1 (run it, 178 of 180 words), the student final-padlock section, the score sheet.
- Any room's locks or variants.
- Live games, schools/assets/, the site footer.
- Never commit or upload a PDF.
- No draft PR.

SUCCESS CONDITION:
- #807's close-out is committed.
- Every pack's class is the easiest that reaches N sets, and the test proves it for each room.
- Car Trap, Library Jam and PE Shed Rebellion get an easier class than in #807, or the report shows why not.
- Heatwave's hint card and key carry the plus-and-minus wording, and every multiplication pack's text is unchanged.
- --selftest and scripts/test-pack-generator.py catch every plant and pass every control; check-escape-rooms.py passes.
- All ten packs build: nine --final, Heatwave DRAFT.
- Merged by merge-pr.py, with its last line, the merge commit and main's check-site and phone-fit-full run IDs reported.
- Handover and todo committed.

STOP IF:
- #807 is not on main after 60 minutes.
- A pack reaches N sets in no class under the existing rules.
- Easiest-first changes a set's lock answers, as opposed to its padlock target, in a way that breaks distinct answers per lock.
- Any multiplication pack's hint or key text changes.
- Page 1 of any pack goes over 180 words.
- merge-pr.py refuses for a reason other than a transient 5xx it already retries.
