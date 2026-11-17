TOOL: Claude Code (home lane; same session that stopped, worktree ~/mg-heatwave-pack). SIZE: medium-large. Recommended: Opus, high effort.
REISSUE: replaces HEATWAVE-PACK in full. Jon, 16 Nov 22:14: "1 pls" (to: add a 6th patrol variant so the pack keeps 6 sets).
MERGE TIMING: merge only after SHAPE-SHIFTER-FLAKE (cloud lane) has merged and main is green; if it is still open when your Gate is green, wait, rebase, then merge. One merge heading for main at a time.

TASK: Build The Heatwave Mutiny's print pack (pack generator, 6 sets, DRAFT) so Jon can proofread it, adding one patrol-lcm-timer variant so six sets can be chosen.

ROOT CAUSE: escape-rooms/heatwave-mutiny has no pack: no tools/pack-generator/rooms/heatwave-mutiny/config.json, no art in the generator, no lockcheck.py RECOMPUTE for its three locks (patrol-lcm-timer: slider; cube-surface-volume: keypad, 4 digits; canteen-freezer-inequality: dial; all kinds the generator already handles). Your STOP found patrol-lcm-timer has only 5 variants in escape-rooms/variants.json (answers 180, 112, 126, 140, 154), and choose() (build_pack.py:838) needs every lock's answers distinct across sets, so at most 5 sets. Art: 11 PNGs on origin/art/heatwave-mutiny-pack, named hw-01-rota.png … hw-11-disruptor-dial.png.

CLASS CHECK: The room's config, art and RECOMPUTE entries are local to this room. The variant shortage is local to one lock's library (scripts/gen-escape-variants.py's patrol-lcm-timer block). Any fault the build meets in tools/pack-generator/ is shared by every pack: fix it there as a general rule with a planted fault and a control, default today's behaviour. Every other pack must stay byte-identical. Letting answers repeat across sets is NOT an option (it would change every pack).

EXACT CHANGE:
First commit: PE-SHED-FINAL's close-out (AGENTS.md rule): #803 merged as 6e1f4e0 via merge-pr.py (second call; last line "main 6e1f4e0: NO RUN FOUND", exit 1, because it looked before main's push runs registered; the merge itself succeeded); check-site 43961875130 FAILURE (Shape Shifter verifier flake only, fixed by SHAPE-SHIFTER-FLAKE), phone-fit-full 43961875121 success. Fill in its home handover entry ("MERGED: pending") and move its contract to docs/history/contracts/. Save this contract verbatim at docs/handover/contracts/2026-11-16-heatwave-pack.md.
1. scripts/gen-escape-variants.py, patrol-lcm-timer block only: append at least one variant (enough that at least 6 exist), keeping the five existing variants' values unchanged (no reorder, no drop). Each new variant: three lap times whose LCM is in the slider's range (1-200, step 1), its answer different from 180, 112, 126, 140 and 154, accepted by keep()/check() and escape_set_checks.py unchanged, with its common wrong answer computed by the block's existing rule. Re-run the generator; the escape-rooms/variants.json and escape-rooms/heatwave-mutiny/room.js diffs must touch patrol-lcm-timer only. check-escape-rooms.py passes.
2. tools/pack-generator/rooms/heatwave-mutiny/config.json: 6 sets, seed 1, "wording_approved": null (DRAFT), certificate title in the room's voice (state it), roles and label boxes for all 11 images (measured by pixel inside each blank surface, ≥2% margin), "printed"/"caption" overrides only where a caption would read as a cut-off sentence (list each), red-herring words with no digit (state them), "answer_units" only if an answer is not whole on paper (state why), and "readout_voice" if the start read-out is spoken in a character's voice: draft one line saying who is speaking, where and why, and list it for Jon to approve.
3. tools/pack-generator/rooms/heatwave-mutiny/art/: the 11 PNGs as WebP at 1254 px, keeping the branch's hw-NN names (art branch untouched).
4. lockcheck.py: RECOMPUTE for the three locks, each working the answer and common wrong answer from the variant's givens by its own method (LCM of the lap times; cube surface area/volume; the freezer inequality), with a docstring line per lock.
5. Shared-generator fixes, if needed: per CLASS CHECK, each with a planted fault and a control in scripts/test-pack-generator.py, listed in the PR with why.
6. /updates/: one dated plain-words line only if the repo's rule counts a new live-room variant as student-visible.
7. docs/todo.md: row HEATWAVE-PACK-APPROVE (build command, page count). Home handover entry.

Lane exception (Jon, 22:14): this task edits scripts/gen-escape-variants.py, escape-rooms/variants.json and escape-rooms/heatwave-mutiny/room.js (patrol-lcm-timer variants only), as well as tools/pack-generator/ and scripts/test-pack-generator.py.

Run only the checks this contract names and the Gate: the pack build, test-pack-generator.py with self-test, check-escape-rooms.py. No optional all-game local runs.

DO NOT TOUCH: the other nine packs' configs, art or output; the live room's prose, hints, solutions or any variant other than the appended patrol ones; other locks' variant blocks; the art branches; final.py's friendliness and fixed-penalty rules except as a general fix under CLASS CHECK; scripts/verify-shape-shifter.py and escape-rooms/pe-shed-rebellion/ (SHAPE-SHIFTER-FLAKE is working there); scripts/audit-answers.py; Gate files; the cloud handover.

SUCCESS CONDITION:
- `python -X utf8 tools/pack-generator/build_pack.py heatwave-mutiny` builds 6 sets with DRAFT on pages 1 and 2; every lockcheck recompute agrees; every final padlock has one expression and needs no calculator.
- variants.json/room.js diffs touch patrol-lcm-timer only; the five existing patrol variants unchanged; check-escape-rooms.py passes.
- Each of the other nine packs built before and after is byte-identical (logs and HTML; PDFs apart from date fields and worktree paths); say how compared.
- test-pack-generator.py catches every planted fault and passes every control.
- PR merged on green via `python -X utf8 scripts/merge-pr.py <n>` (after SHAPE-SHIFTER-FLAKE, as above); report its last line and exit status, main's check-site and phone-fit-full run IDs and results on the merge commit (look them up if it prints NO RUN FOUND), the new patrol variant(s), the six sets' answers, common wrong answers and final padlock expressions, and every wording choice Jon must proofread. Home handover documented.

STOP IF:
- No new patrol variant can be admitted without changing a rule in escape_set_checks.py or keep().
- Fewer than 6 sets can be chosen even with the new variant(s).
- Re-running the generator changes any other lock or any existing patrol variant.
- Any other pack changes by one byte (beyond date fields and worktree paths).
- A lock needs a new kind of instrument or answer shape in the generator (report what; separate contract).
- A wording check fails on the room's own words and the only fix is rewording the live room.
- merge-pr.py reports it cannot reach GitHub (a 5xx during the Gate wait may be retried once with the same script).
