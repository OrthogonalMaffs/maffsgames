TOOL: Claude Code (home lane). SIZE: medium-large (new room config + art, lockcheck recomputes, likely shared-generator fixes). Recommended: Opus, high effort.
MERGE TIMING: merge only after PR #800 (BEARING-BLITZ-GOAT, cloud lane) has merged; if #800 is still open when your Gate is green, wait for it, rebase, then merge. One merge heading for main at a time.

TASK: Build The PE Shed Rebellion's print pack (pack generator, 6 sets, DRAFT) so Jon can proofread it, the way The Great Hamster Heist's was built (#798, #799).

ROOT CAUSE: escape-rooms/pe-shed-rebellion has no pack: no tools/pack-generator/rooms/pe-shed-rebellion/config.json, no art in the generator, no lockcheck.py RECOMPUTE for its three locks (sprinkler-sector-area, dodgeball-pressure-boyle, locker-nth-term; all dials). Its eleven pictures are on branch origin/art/pe-shed-rebellion-pack as PNGs at the top level ("Blank groundsman’s logbook by school tap-1.png" … "Black Combination Dial, Blank White Label-11.png"). Separately, docs/todo.md row 47 PE-SHED-VARIANT-0 (Jon ruled 29 Sep 2026: fix it) records variant 0's collisions (48 psi vs "48π"; 12 m vs "day 12"), which the pack's figure checks may also meet.

CLASS CHECK: The room's config, art and RECOMPUTE entries are local to this room. Any fault the build meets in tools/pack-generator/ (build_pack.py, final.py, lockcheck.py, plant_common) is shared by every pack: fix it there as a general rule with a planted fault and a control, defaulting to today's behaviour, never as a PE-Shed-only flag. Every other pack must stay byte-identical. Variant 0 is local to this room's bank (scripts/gen-escape-variants.py's PE Shed blocks and escape-rooms/variants.json), fixed there.

EXACT CHANGE:
1. tools/pack-generator/rooms/pe-shed-rebellion/config.json: 6 sets, seed 1, "wording_approved": null (DRAFT), certificate title in the room's voice (state it), roles and label boxes for the eleven images (measured by pixel inside each blank surface, ≥2% margin), "printed"/"caption" overrides only where a caption would read as a cut-off sentence (list each), red-herring words with no digit (state them), "answer_units" only if a lock's answer is not whole on paper (state why).
2. tools/pack-generator/rooms/pe-shed-rebellion/art/: the eleven PNGs from origin/art/pe-shed-rebellion-pack as WebP at 1254 px, named pe-01-… to pe-11-… in the branch's number order (the art branch untouched).
3. lockcheck.py: RECOMPUTE for the three locks, each working the answer and common wrong answer from the variant's givens by its own method (sector area, Boyle's law, nth term), with a docstring line per lock.
4. Shared-generator fixes, if the build needs any: per CLASS CHECK, each with a planted fault and a control in scripts/test-pack-generator.py, listed in the PR with why.
5. PE-SHED-VARIANT-0 (todo row 47): fix variant 0 per the ruling so scripts/check-escape-rooms.py no longer reports it INVALID; the regenerated variants.json and room.js diffs touch PE Shed's locks only; close row 47.
6. docs/todo.md: a row PE-SHED-PACK-APPROVE for Jon to proofread (build command, page count). Home handover entry; contract saved verbatim at docs/handover/contracts/2026-11-16-pe-shed-pack.md.

Lane exception (Jon, 16 Nov 19:19, "send a pack to that lane"): this task edits tools/pack-generator/, scripts/test-pack-generator.py, scripts/gen-escape-variants.py, escape-rooms/variants.json and escape-rooms/pe-shed-rebellion/room.js (variant 0 only).

Run only the checks this contract names and the Gate: the pack build, test-pack-generator.py with self-test, check-escape-rooms.py. No optional all-game local runs (phone-fit, all verifiers); CI covers them.

DO NOT TOUCH: the other seven packs' configs, art or output; the live room's prose, hints, solutions or any variant other than variant 0; the art branches; final.py's friendliness rule and the fixed-penalty rules except as a general fix under CLASS CHECK; Gate files (workflow, scripts/ci-*, merge-pr.py); the cloud-lane handover; anything PR #800 touches (games/bearing-blitz/, scripts/verify-bearing-blitz.py).

SUCCESS CONDITION:
- `python -X utf8 tools/pack-generator/build_pack.py pe-shed-rebellion` builds 6 sets with DRAFT on pages 1 and 2; every lockcheck recompute agrees; every final padlock has one expression and no calculator needed.
- Each of the other seven packs built before and after is byte-identical page for page, no padlock target moved; say how compared.
- check-escape-rooms.py reports no INVALID variant for pe-shed-rebellion; test-pack-generator.py catches every planted fault and passes every control.
- PR merged on green via `python -X utf8 scripts/merge-pr.py <n>` (after #800, as above); report its last line and exit status, main's check-site and phone-fit-full run IDs and results on the merge commit, the six sets' answers, common wrong answers and final padlock expressions, and every wording choice Jon must proofread. Home handover documented.

STOP IF:
- Fewer than 6 sets can be chosen.
- Any other pack changes by one byte.
- A lock needs a new kind of instrument or answer shape in the generator (report what; that is a separate contract).
- Fixing variant 0 changes any other variant or any other lock.
- A wording check fails on the room's own words and the only fix is rewording the live room.
- merge-pr.py reports it cannot reach GitHub (a 5xx during the Gate wait may be retried once with the same script).
