TOOL: Claude Code (home lane). SIZE: large (shared generator learns the "pair" answer; new room config + art; lockcheck recomputes). Recommended: Opus, high effort.
MERGE TIMING: one merge heading for main at a time. CORE-PAPER-EXIT (#816, cloud) may be merging; if any other PR is in its Gate or merge when yours is green, wait for it, rebase, then merge.

TASK: Build The Canteen Hack's print pack (6 sets, DRAFT) so Jon can proofread it, teaching the shared generator to print a two-value "pair" lock, with the pair counting as the sum of its two values in the final padlock.

ROOT CAUSE: escape-rooms/canteen-hack has no pack: no tools/pack-generator/rooms/canteen-hack/config.json, no art in the generator, no lockcheck.py RECOMPUTE for its locks: canteen-mean-calories (slider 0-1000), cookie-price-simultaneous (instrument kind 'pair', room.js:294: a = Cookie dial 0-10, b = Pizza dial 0-10, whole pounds; answer stored as an ordered pair, e.g. [2, 3], miss [3, 2], the swap) and kale-fraction-drain (dial 0-200). Each has 10 variants in escape-rooms/variants.json. The generator has never printed a 'pair' lock: answers_of() (build_pack.py, "A lock with several accepted answers cannot take part") stops on a list, checker.flat() (scripts/check-escape-rooms.py:153) treats a list as several ACCEPTED answers (a set), and miss_is_answer() compares those sets, so [2,3] vs its miss [3,2] would read as equal. Pictures: branch origin/art/canteen-hack-pack.

JON'S RULING (17 Nov 2026 19:25, verbatim in the PR body): "I agree that you add the 2 numbers for cookie." (to: the pair lock counts in the final padlock as the total of its two prices, e.g. £2 and £3 → 5).

CLASS CHECK: The pair handling is architectural: it lives in the shared generator (build_pack.py, final.py inputs, lockcheck.py) and must be a general rule for any room's 'pair' lock, not a Canteen flag. A pair is an ORDERED pair of values, never a set of alternatives: every place that reads a pair's answer or miss (answer box, key, miss_is_answer, answer distinctness across sets, answers_of for the final padlock, lockcheck comparison) handles kind 'pair' explicitly, while single-value locks and multi-accepted-answer locks keep today's behaviour exactly. The room's config, art and RECOMPUTE entries are local. Every other pack stays byte-identical.

EXACT CHANGE:
First commit: the home close-outs owed (AGENTS.md rule): FINAL-PADLOCK-FAIR (#807, 65c7ebd) if home.md still says "MERGED: pending", and any other home entry still pending; look up merge commits and main's check-site and phone-fit-full run IDs with gh. Save this contract verbatim at docs/handover/contracts/2026-11-17-canteen-pack.md.
1. build_pack.py, pair locks (instrument kind 'pair'), general:
   - Student locks page: one answer area with two labelled boxes from the instrument's a.label and b.label (here "Cookie £" and "Pizza £"), same minimum write size as other boxes.
   - Key and worked solutions: both values with their labels, and the common wrong answer the same way (e.g. "Cookie £3, Pizza £2: the prices swapped").
   - miss_is_answer(), answer distinctness across sets and lockcheck comparisons: compare pairs as ordered pairs (a, b).
   - answers_of() (final padlock input): a pair contributes a + b. The final padlock instruction on the student page and the key say so in plain words for that lock (e.g. "For the price tags, use the two prices added together"); the score sheet is unchanged.
   - Every existing rule applies to the result: PRODUCT_MAX 10,000, one difficulty class per pack, easiest class first, no miss printed as the answer.
2. lockcheck.py RECOMPUTE for the three locks, each by its own method from the variant's givens: the missing fifth value from a mean of five (canteen-mean-calories); the 2×2 simultaneous equations solved by elimination, as an ordered pair (cookie-price-simultaneous); the fraction-drain amount (kale-fraction-drain); each with its common wrong answer by the room's stored rule (state it). Docstring line per lock.
3. tools/pack-generator/rooms/canteen-hack/config.json: 6 sets, seed 1, "wording_approved": null (DRAFT), pack_version 1, certificate title in the room's voice (state it), roles and label boxes for every image (pixel-measured, ≥2% margin), "printed"/"caption" overrides only where needed (list each), red-herring words with no digit (state them), "readout_voice" only if the start read-out is a character speaking (draft one line for Jon). Final shape: the default unless the rules force plus-and-minus (report which).
4. tools/pack-generator/rooms/canteen-hack/art/: the branch's PNGs as WebP at 1254 px, named in the branch's order (art branch untouched).
5. scripts/test-pack-generator.py: plants that must be caught: a pair compared as a set (miss [3,2] read as the answer [2,3]); a pair's final-padlock input that is not a + b; a pair answer box missing one of its two boxes; a pair key line missing a label. Controls: a correct pair lock passes; single-value and multi-accepted locks unchanged. Every existing plant still caught.
6. docs/todo.md: row CANTEEN-PACK-APPROVE (build command, page count); then bundles (Jon, 17 Nov 19:24: "wait for canteen and list the bundles at the same time"): one row CORE-BUNDLES-2 for Jon: list Core bundle 2 (Hamster, P.E. Store, Heatwave, Canteen) and an all-seven Core bundle once Canteen is live. docs/todo.md is within ~150 bytes of its 153,600-byte cap: archive closed rows to docs/history/todo-done.md as the repo does before adding these. Home handover entry.

Run only the checks this contract names and the Gate: the Canteen build, test-pack-generator.py with self-test, check-escape-rooms.py. No optional all-game local runs. Show the other nine packs byte-identical (logs and HTML; PDFs apart from date fields and worktree paths); say how compared.

DO NOT TOUCH: the live room's room.js, variants, hints and wording; the online engine's pair handling (escape-rooms/assets/engine.js); scripts/check-escape-rooms.py's flat() for single and multi-accepted locks; the other nine packs' configs and art; final.py's rules (PRODUCT_MAX, classes, easiest-first) except to feed them the pair's sum; Gate files; scripts/merge-pr.py; the cloud handover; anything CORE-PAPER-EXIT (#816) touches (schools/assets/stage-exit.*, games/core-maths-paper*).

SUCCESS CONDITION:
- `python -X utf8 tools/pack-generator/build_pack.py canteen-hack` builds 6 sets, DRAFT on pages 1 and 2, file canteen-hack-pack-v1.pdf; every lockcheck recompute agrees; every final padlock meets the standing rules and has one expression; each set's pair prints as two labelled boxes and its key shows both values and the swapped common wrong answer.
- The other nine packs byte-identical as above.
- test-pack-generator.py catches every planted fault and passes every control.
- PR merged on green via `python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600`; report its last line and exit status, main's check-site and phone-fit-full run IDs and results on the merge commit, the six sets' answers (pairs as Cookie/Pizza), common wrong answers, final padlock expressions and targets, and every wording choice Jon must proofread. Home handover documented.

STOP IF:
- Fewer than 6 sets can be chosen under the standing padlock rules with the pair as a + b.
- Supporting 'pair' would change any other pack by one byte, or change how a multi-accepted-answer lock is judged.
- A lock needs any change to the live room's text or variants.
- merge-pr.py refuses for a reason other than a transient 5xx it already retries.
